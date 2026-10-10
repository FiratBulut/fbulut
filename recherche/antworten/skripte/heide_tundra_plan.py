#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien – Planer „Heide/Tundra“ (Auftrag 11, Teil B3): Ebene `heide_tundra` für die Biome heide und tundra
(Felder D2, C2, C3, D3, E3, E2; F4, G4, F5, G5). Schichten:
  0 boden        Kiesel, Flechtensteine (< 0,8 m), Torf-/Streumatten, Zweige
  1 mittel       Heidekraut-Flecken (Zwergstrauch), Grasbüschel verschiedener Höhe, Wacholder-Stellvertreter, Krüppelkiefern,
                 Moorbirken-Jungwuchs, Heideblüte (Farbakzent), liegendes Totholz, Stümpfe
  2 baum         Einzelkiefern (windschief auf Kuppen, Gruppen 2–5 in Mulden), Moorbirken am Moorrand, Totbäume – Baumgrenze nach Höhe
  5 wasserkante  Wollgras-Stellvertreter, Seggen/Binsen, Moorsteine, Treibholz an Moortümpeln
  3 fels / 4 spuren kommen aus felsgruppen_plan.py / spuren_plan.py (Overrides in heide_tundra_regeln.json).

Aufruf (lokal, production-Wurzel):
    python -I scripts/heide_tundra/heide_tundra_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
                                                        [--entfernen "praefix1,praefix2"]

Liest:   export/unreal/welt/hoehe.f32 (np.memmap, Fenster Feld + 64 m, NY=7057 × NX=9577, J-Spalte geklippt), lage_*.r8 (optional),
         karte_wasser/weg/ort.r8 (optional, Warnung), eigner.r8 + welt.json (Biom je Zelle, Fallback je Feld bzw. aue),
         bestand/<Feld>/, witcher/<Feld>/ (+ Nachbarn) für Kronendach/Stammabstand, instanzen/instanzen.json (Houdini-Bäume, optional),
         ufer/foliage_<Feld>/ (wenn vorhanden: Klasse moorstein entfällt), daten/netze.csv (Pfadprüfung + Netzhöhen).
Schreibt: export/unreal/welt/heide_tundra/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm, qx,qy,qz,qw, sx,sy,sz) + plan.json (FORMAT §3,
         zusätzlich "ebene", "klassen", "schichten"), bei --bild docs/pruefung/heide_tundra/<Feld>.png (1 px = 1 m).

Nur NumPy-Vektoroperationen (Box-/Gauß-Faltung über Summenbilder, Jump-Flooding-Distanz, Hash-Zufall aus absoluter Rasterkoordinate →
deterministisch und nahtlos zu Nachbarfeldern). numba optional (nur Meldung), Pillow optional (sonst PPM). Ziel ≤ 60 s je Feld.

Quellen: vorlagen/FORMAT.md §1–§5; antworten/assets-taxonomie.md (Paletten heide/tundra); antworten/bildkritik-witcher-messlatte.md;
antworten/boden-kleinzeug-gras.md; antworten/verteilung-heide-tundra.md §1 (Witcher-Analyse mit Web-Quellen: 80.lv „World Building of
Witcher 3“, SpeedTree-Fallstudie W3, JNCC NVC M19/H4030, Irish Vegetation Classification HE3F/BG2E).

UNGETESTET MIT ECHTDATEN – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern rauchgetestet.
"""
import argparse
import csv
import json
import math
import os
import sys
import time

import numpy as np

try:  # numba optional – nicht benötigt
    import numba  # noqa: F401
    NUMBA = True
except Exception:  # pragma: no cover
    NUMBA = False

NX, NY = 9577, 7057
FELD_M = 1008
X0, Y0 = 4730.5, 4060.5
WELT = os.path.join('export', 'unreal', 'welt')
BAUM_ROLLEN = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel', 'palme',
               'hainbuche', 'pine', 'fir', 'tanne')
LAGEN_NAMEN = ['Wiese', 'Gras', 'Trockengras', 'Laub', 'Nadeln', 'Moos', 'Heide', 'Kraut', 'Erde', 'Lehm', 'Schlamm', 'Sand', 'Kies',
               'Geroell', 'Fels', 'Felsplatte', 'Sandstein', 'Schnee', 'Eis', 'Lavafels', 'Lavasand', 'Algen']


# ----------------------------------------------------------------------------- Helfer
def meld(*a):
    print('[heide_tundra]', *a, flush=True)


def feld_fenster(feld, rand):
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX)  # J-Spalte: 9072 … 9577 (nur 505 m)
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY)
    wi0, wi1 = max(0, i0 - rand), min(NY, i1 + rand)
    wj0, wj1 = max(0, j0 - rand), min(NX, j1 + rand)
    return feld, (i0, i1, j0, j1), (wi0, wi1, wj0, wj1)


def lade_raster(pfad, dtype, win, pflicht=False):
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            raise SystemExit('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        meld('WARNUNG: %s hat %d Werte, erwartet %d – ignoriert' % (pfad, n, NX * NY))
        if pflicht:
            raise SystemExit('Pflichtdatei hat falsche Größe: %s' % pfad)
        return None
    mm = np.memmap(pfad, dtype=dtype, mode='r', shape=(NY, NX))
    out = np.array(mm[wi0:wi1, wj0:wj1])
    del mm
    return out


def box_blur(a, r):
    if r <= 0:
        return a.astype(np.float32)
    p = np.pad(a.astype(np.float32), r, mode='reflect')
    c = np.cumsum(p, axis=0)
    c = np.concatenate([np.zeros((1, c.shape[1]), np.float32), c], axis=0)
    p = (c[2 * r + 1:, :] - c[:-2 * r - 1, :]) / (2 * r + 1)
    c = np.cumsum(p, axis=1)
    c = np.concatenate([np.zeros((c.shape[0], 1), np.float32), c], axis=1)
    return (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)


def gauss_blur(a, sigma):
    w = math.sqrt(12.0 * sigma * sigma / 3.0 + 1.0)
    r = max(1, int(round((w - 1) / 2)))
    out = a
    for _ in range(3):
        out = box_blur(out, r)
    return out


def verschiebe(a, di, dj, fill):
    H, W = a.shape
    out = np.full_like(a, fill)
    si0, si1 = max(0, di), min(H, H + di)
    sj0, sj1 = max(0, dj), min(W, W + dj)
    oi0, oi1 = max(0, -di), min(H, H - di)
    oj0, oj1 = max(0, -dj), min(W, W - dj)
    if si1 > si0 and sj1 > sj0:
        out[oi0:oi1, oj0:oj1] = a[si0:si1, sj0:sj1]
    return out


def dilate(mask, r):
    """Binäre Dilatation ≈ Kreisscheibe mit Radius r Zellen."""
    m = mask.copy()
    for k in range(int(math.ceil(r))):
        n = m.copy()
        n[1:, :] |= m[:-1, :]
        n[:-1, :] |= m[1:, :]
        n[:, 1:] |= m[:, :-1]
        n[:, :-1] |= m[:, 1:]
        if k % 2 == 1:
            n[1:, 1:] |= m[:-1, :-1]
            n[1:, :-1] |= m[:-1, 1:]
            n[:-1, 1:] |= m[1:, :-1]
            n[:-1, :-1] |= m[1:, 1:]
        m = n
    return m


def distanz(mask, max_m=64.0):
    """Euklidische Distanz (m) zur nächsten True-Zelle per Jump-Flooding (vektorisiert)."""
    H, W = mask.shape
    fern = np.float32(max_m * 2.0)
    if not mask.any():
        return np.full((H, W), fern, np.float32)
    ii, jj = np.indices((H, W), dtype=np.int32)
    si = np.where(mask, ii, -1).astype(np.int32)
    sj = np.where(mask, jj, -1).astype(np.int32)
    INF = np.int32(2 ** 30)
    d2 = np.where(mask, 0, INF).astype(np.int32)
    s = 1
    while s * 2 <= max_m:
        s *= 2
    schritte = []
    while s >= 1:
        schritte.append(s)
        s //= 2
    schritte.append(1)
    for s in schritte:
        for di in (-s, 0, s):
            for dj in (-s, 0, s):
                if di == 0 and dj == 0:
                    continue
                csi = verschiebe(si, di, dj, np.int32(-1))
                csj = verschiebe(sj, di, dj, np.int32(-1))
                cd2 = (ii - csi) ** 2 + (jj - csj) ** 2
                besser = (csi >= 0) & (cd2 < d2)
                d2 = np.where(besser, cd2, d2)
                si = np.where(besser, csi, si)
                sj = np.where(besser, csj, sj)
    d = np.sqrt(d2.astype(np.float32))
    d[d2 >= INF] = fern
    return np.minimum(d, fern).astype(np.float32)


def hash01(i, j, seed, kanal):
    """Deterministische Zufallszahl [0,1) je (absolute Rasterzeile, -spalte, Seed, Kanal); kanal darf Array sein."""
    i = np.asarray(i).astype(np.int64)
    j = np.asarray(j).astype(np.int64)
    k = np.asarray(kanal).astype(np.int64)
    h = (i * 73856093) ^ (j * 19349663) ^ (int(seed) * 83492791 + k * 2654435761)
    h = (h & 0xFFFFFFFF).astype(np.uint32)
    with np.errstate(over='ignore'):
        h ^= h >> np.uint32(16)
        h *= np.uint32(0x7FEB352D)
        h ^= h >> np.uint32(15)
        h *= np.uint32(0x846CA68B)
        h ^= h >> np.uint32(16)
    return (h & np.uint32(0xFFFFFF)).astype(np.float32) / np.float32(16777216.0)


def wertrauschen(ii_abs, jj_abs, skala_m, seed, kanal, oktaven=2):
    """Wertrauschen [0,1] auf absolutem Gitter (nahtlos über Feldgrenzen), bilinear, 2 Oktaven."""
    out = np.zeros(ii_abs.shape, np.float32)
    gew_sum = 0.0
    gew = 1.0
    sk = float(skala_m)
    for o in range(oktaven):
        fi = ii_abs / sk
        fj = jj_abs / sk
        gi = np.floor(fi).astype(np.int64)
        gj = np.floor(fj).astype(np.int64)
        ti = (fi - gi).astype(np.float32)
        tj = (fj - gj).astype(np.float32)
        ti = ti * ti * (3 - 2 * ti)
        tj = tj * tj * (3 - 2 * tj)
        v00 = hash01(gi, gj, seed, kanal + o * 7)
        v10 = hash01(gi + 1, gj, seed, kanal + o * 7)
        v01 = hash01(gi, gj + 1, seed, kanal + o * 7)
        v11 = hash01(gi + 1, gj + 1, seed, kanal + o * 7)
        v = (v00 * (1 - ti) + v10 * ti) * (1 - tj) + (v01 * (1 - ti) + v11 * ti) * tj
        out += gew * v
        gew_sum += gew
        gew *= 0.5
        sk *= 0.5
    return out / gew_sum


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def bilinear(h, fi, fj):
    H, W = h.shape
    fi = np.clip(fi, 0, H - 1.001)
    fj = np.clip(fj, 0, W - 1.001)
    i0 = fi.astype(np.int32)
    j0 = fj.astype(np.int32)
    ti = (fi - i0).astype(np.float32)
    tj = (fj - j0).astype(np.float32)
    return ((h[i0, j0] * (1 - ti) + h[i0 + 1, j0] * ti) * (1 - tj)
            + (h[i0, j0 + 1] * (1 - ti) + h[i0 + 1, j0 + 1] * ti) * tj)


def quat_mul(a, b):
    ax, ay, az, aw = a.T
    bx, by, bz, bw = b.T
    return np.stack([aw * bx + ax * bw + ay * bz - az * by,
                     aw * by - ax * bz + ay * bw + az * bx,
                     aw * bz + ax * by - ay * bx + az * bw,
                     aw * bw - ax * bx - ay * by - az * bz], axis=1)


def quaternionen(tx, ty, tz, yaw):
    """Z-Achse auf Zielvektor t kippen, davor Zufalls-Yaw. Ergebnis (n,4) = x,y,z,w."""
    n = len(tx)
    l = np.sqrt(tx * tx + ty * ty + tz * tz) + 1e-9
    tx, ty, tz = tx / l, ty / l, tz / l
    qt = np.stack([-ty, tx, np.zeros(n, np.float32), 1 + tz], axis=1)
    qt /= (np.linalg.norm(qt, axis=1, keepdims=True) + 1e-9)
    qy = np.stack([np.zeros(n, np.float32), np.zeros(n, np.float32), np.sin(yaw / 2), np.cos(yaw / 2)], axis=1)
    q = quat_mul(qt, qy)
    return (q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-9)).astype(np.float32)


# ----------------------------------------------------------------------------- Inventar
def lade_inventar(basis, skript_dir):
    """daten/netze.csv → {pfad: hoehe_m}; sucht production/daten, dann Repo-Vorlage neben dem Skript."""
    kandidaten = [os.path.join(basis, 'daten', 'netze.csv'),
                  os.path.join(skript_dir, 'netze.csv'),
                  os.path.join(skript_dir, '..', '..', 'vorlagen', 'daten', 'netze.csv')]
    for k in kandidaten:
        if os.path.isfile(k):
            inv = {}
            with open(k, encoding='utf-8') as f:
                for row in csv.DictReader(f, delimiter=';'):
                    try:
                        inv[row['pfad']] = float(row.get('groesse_z_m') or 0.3)
                    except Exception:
                        inv[row['pfad']] = 0.3
            meld('Inventar: %s (%d Netze)' % (k, len(inv)))
            return inv
    meld('WARNUNG: daten/netze.csv nicht gefunden – Pfadprüfung entfällt, Netzhöhen = 0,3 m')
    return None


def pruefe_paletten(regeln, inv):
    fehlt = []
    for kn, kl in regeln['klassen'].items():
        for prof, liste in kl['netze'].items():
            for p in liste:
                if inv is not None and p not in inv:
                    fehlt.append('%s/%s: %s' % (kn, prof, p))
    if fehlt:
        meld('FEHLER: %d Netzpfade nicht im Inventar:' % len(fehlt))
        for f in fehlt:
            meld('   ', f)
        raise SystemExit('Netzpfade fehlen – Regeln oder Inventar prüfen')


# ----------------------------------------------------------------------------- Weltdaten
def lade_biome(basis, win, regeln, feld):
    """Biom-Name je Zelle als Index in `namen` (Reihenfolge profil_je_biom)."""
    namen = list(regeln['profil_je_biom'].keys())
    fb = regeln.get('feld_biom_fallback', {}).get(feld, 'aue')
    if fb not in namen:
        fb = 'aue'
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    if eig is None or not os.path.isfile(wj):
        meld('Hinweis: eigner.r8/welt.json fehlen – Biom je Zelle = Fallback %r' % fb)
        return np.full((H, W), namen.index(fb), np.int16), namen, {fb: 1.0}
    try:
        welt = json.load(open(wj, encoding='utf-8'))
    except Exception as e:
        meld('Hinweis: welt.json unlesbar (%s) – Fallback %r' % (e, fb))
        return np.full((H, W), namen.index(fb), np.int16), namen, {fb: 1.0}
    kacheln = welt.get('kacheln', {})
    tabelle = np.full(256, namen.index(fb), np.int16)

    def biom_aus_rezept(rz):
        rz = str(rz).lower()
        if rz in namen:
            return rz
        if 'vulkan' in rz or 'lava' in rz:
            return 'lava'
        for n in namen:
            if n in rz:
                return n
        return fb
    eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
    for k, v in eintraege:
        try:
            kk = int(v.get('kennzahl', v.get('id', k))) if isinstance(v, dict) else int(k)
        except Exception:
            continue
        if 0 <= kk < 256:
            rz = v.get('rezept', '') if isinstance(v, dict) else ''
            tabelle[kk] = namen.index(biom_aus_rezept(rz) if rz else fb)
    tabelle[0] = namen.index(fb)  # Weltgelände → Feld-Fallback (FORMAT: aue; hier dominantes Feldbiom, s. Regeln)
    bio = tabelle[eig]
    ant = {namen[k]: round(float((bio == k).mean()), 3) for k in np.unique(bio)}
    return bio, namen, ant


def lade_ebene_positionen(ordner, win):
    baum, sonst = [], []
    pj = os.path.join(ordner, 'plan.json')
    if not os.path.isfile(pj):
        return baum, sonst
    try:
        plan = json.load(open(pj, encoding='utf-8'))
    except Exception:
        return baum, sonst
    for name, info in plan.get('dateien', {}).items():
        f = os.path.join(ordner, name + '.f32')
        if not os.path.isfile(f):
            continue
        try:
            a = np.fromfile(f, dtype='<f4')
        except Exception:
            continue
        if a.size % 10:
            continue
        a = a.reshape(-1, 10)
        fj = a[:, 0] / 100.0 + X0 - win[2]
        fi = a[:, 1] / 100.0 + Y0 - win[0]
        m = (fi >= 0) & (fi < win[1] - win[0]) & (fj >= 0) & (fj < win[3] - win[2])
        if not m.any():
            continue
        txt = (str(info.get('rolle', '')) + ' ' + str(info.get('gruppe', '')) + ' ' + name).lower()
        ist_baum = any(r in txt for r in BAUM_ROLLEN) and 'tot' not in txt and 'stump' not in txt and 'log' not in txt \
            and 'plant' not in txt and 'sapling' not in txt and 'seedling' not in txt
        (baum if ist_baum else sonst).append(np.stack([fi[m], fj[m]], axis=1))
    return baum, sonst


def lade_bestand(basis, feld, win):
    """Baum-Positionen (Fenster-Koordinaten) aus bestand/, witcher/ (Feld + 8 Nachbarn), instanzen.json; Sonstiges nur im Feld."""
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    baum, sonst, quellen = [], [], []
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(ord('A') + ss) + str(rr)
            for ebene in ('bestand', 'witcher', 'mittelschicht', 'felsgruppen'):
                b, so = lade_ebene_positionen(os.path.join(basis, WELT, ebene, nf), win)
                if b or so:
                    quellen.append('%s/%s' % (ebene, nf))
                baum += b
                sonst += so
    uf = os.path.join(basis, WELT, 'ufer', 'foliage_' + feld)
    ufer_da = os.path.isdir(uf)
    if ufer_da:
        b, so = lade_ebene_positionen(uf, win)
        sonst += b + so
        quellen.append('ufer/foliage_' + feld)
    ij = os.path.join(basis, WELT, 'instanzen', 'instanzen.json')
    if os.path.isfile(ij):
        try:
            inst = json.load(open(ij, encoding='utf-8'))
            for e in inst.get('verzeichnis', []):
                txt = (str(e.get('klasse', '')) + ' ' + str(e.get('name', ''))).lower()
                f = e.get('datei') or (str(e.get('name', '')) + '.f32')
                f = os.path.join(basis, WELT, 'instanzen', f)
                if not os.path.isfile(f):
                    continue
                a = np.fromfile(f, dtype='<f4')
                if a.size % 10:
                    continue
                a = a.reshape(-1, 10)
                fj = a[:, 0] / 100.0 + X0 - win[2]
                fi = a[:, 1] / 100.0 + Y0 - win[0]
                m = (fi >= 0) & (fi < win[1] - win[0]) & (fj >= 0) & (fj < win[3] - win[2])
                if m.any():
                    (baum if any(k in txt for k in BAUM_ROLLEN) else sonst).append(np.stack([fi[m], fj[m]], axis=1))
                    quellen.append('instanzen/' + os.path.basename(f))
        except Exception as e:
            meld('Hinweis: instanzen.json nicht auswertbar (%s)' % e)
    baum = np.concatenate(baum, axis=0) if baum else np.zeros((0, 2), np.float32)
    sonst = np.concatenate(sonst, axis=0) if sonst else np.zeros((0, 2), np.float32)
    return baum, sonst, quellen, ufer_da


def punkte_maske(pts, H, W):
    m = np.zeros((H, W), bool)
    if len(pts):
        ii = np.clip(np.round(pts[:, 0]).astype(np.int32), 0, H - 1)
        jj = np.clip(np.round(pts[:, 1]).astype(np.int32), 0, W - 1)
        m[ii, jj] = True
    return m


def lagen_faktor(lagen, gewichte):
    """Gewichtetes Mittel der Lagen-Gewichte über die Deckung; keine Lagen → 1."""
    if not lagen:
        return None
    num = None
    den = None
    for name, a in lagen.items():
        w = float(gewichte.get(name, gewichte.get('_default', 0.5)))
        d = a.astype(np.float32) / 255.0
        num = d * w if num is None else num + d * w
        den = d if den is None else den + d
    f = np.where(den > 0.02, num / np.maximum(den, 1e-3), 1.0).astype(np.float32)
    return f


def lagen_anteil(lagen, namen):
    out = None
    for n in namen:
        if n in lagen:
            d = lagen[n].astype(np.float32) / 255.0
            out = d if out is None else out + d
    return out


# ----------------------------------------------------------------------------- Planung je Feld
def plane_feld(feld_in, basis, regeln, faktor, bild, inv, entfernen_cli):
    t0 = time.time()
    rand = int(regeln.get('fenster_rand_m', 64))
    feld, fb, win = feld_fenster(feld_in, rand)
    i0, i1, j0, j1 = fb
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    seed = int(regeln.get('seed', 1))
    meld('Feld %s: Fenster i %d–%d, j %d–%d (%d × %d)' % (feld, wi0, wi1, wj0, wj1, H, W))

    # --- Raster
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True).astype(np.float32)
    wasser = lade_raster(os.path.join(basis, WELT, 'karte_wasser.r8'), np.uint8, win)
    weg = lade_raster(os.path.join(basis, WELT, 'karte_weg.r8'), np.uint8, win)
    ort = lade_raster(os.path.join(basis, WELT, 'karte_ort.r8'), np.uint8, win)
    for nm, a in (('karte_wasser.r8', wasser), ('karte_weg.r8', weg), ('karte_ort.r8', ort)):
        if a is None:
            meld('WARNUNG: %s fehlt – ohne Abstand geplant' % nm)
    wasser = (wasser > 0) if wasser is not None else np.zeros((H, W), bool)
    weg = (weg > 0) if weg is not None else np.zeros((H, W), bool)
    ort = (ort > 0) if ort is not None else np.zeros((H, W), bool)
    lagen = {}
    for n in LAGEN_NAMEN:
        a = lade_raster(os.path.join(basis, WELT, 'lage_%s.r8' % n), np.uint8, win)
        if a is not None:
            lagen[n] = a
    meld('Lagen vorhanden: %s' % (', '.join(sorted(lagen)) if lagen else 'keine (Faktor 1)'))
    bio, biom_namen, biom_anteile = lade_biome(basis, win, regeln, feld)
    meld('Biome im Fenster: %s' % biom_anteile)
    baum_pts, sonst_pts, quellen, ufer_da = lade_bestand(basis, feld, win)
    meld('Bestand: %d Bäume, %d Sonstige aus %s' % (len(baum_pts), len(sonst_pts), quellen or 'nichts'))

    # --- abgeleitete Felder
    ii, jj = np.indices((H, W), dtype=np.int32)
    ii_abs = ii + wi0
    jj_abs = jj + wj0
    g = regeln['gelaende']
    hs = gauss_blur(hoehe, float(g.get('hang_sigma_m', 2.0)))
    dhi = np.gradient(hs, axis=0)
    dhj = np.gradient(hs, axis=1)
    hang = np.degrees(np.arctan(np.sqrt(dhi * dhi + dhj * dhj))).astype(np.float32)
    nl = np.sqrt(dhi * dhi + dhj * dhj + 1.0)
    nx_, ny_, nz_ = (-dhj / nl).astype(np.float32), (-dhi / nl).astype(np.float32), (1.0 / nl).astype(np.float32)
    expo = np.clip((hoehe - gauss_blur(hoehe, float(g.get('expo_sigma_m', 40)))) / float(g.get('expo_norm_m', 8)), -1, 1).astype(np.float32)
    mulde = np.clip((gauss_blur(hoehe, float(g.get('mulde_sigma_m', 12))) - hoehe) / 3.0, 0, 1).astype(np.float32)
    land = hoehe > 0.05
    d_wasser = distanz(wasser, 64.0)
    ab = regeln['abstand_m']
    weg_klein = dilate(weg, ab.get('weg_klein', 2.5))
    weg_gross = dilate(weg, ab.get('weg_gross', 4.0))
    ort_m = dilate(ort, ab.get('ort', 5.0))
    baum_mask = punkte_maske(baum_pts, H, W)
    sonst_mask = punkte_maske(sonst_pts, H, W)
    stamm = dilate(baum_mask, ab.get('baumstamm', 1.5))
    sonst_nah = dilate(sonst_mask, ab.get('bestand_sonst', 1.0))
    kd = regeln['kronendach']
    kr = int(round(float(kd.get('radius_m', 4.5))))
    beschattung = np.clip(box_blur(baum_mask.astype(np.float32), kr) * (2 * kr + 1) ** 2 * float(kd.get('k', 0.9)), 0, 1)
    baum_nah = {}

    # --- Profil (heide/tundra) und Biomfaktor je Zelle
    pjb = regeln['profil_je_biom']
    prof_tab = np.array([0 if pjb[n][0] == 'heide' else 1 for n in biom_namen], np.int8)
    fak_tab = np.array([float(pjb[n][1]) for n in biom_namen], np.float32)
    profil = prof_tab[bio]
    biomfak = fak_tab[bio]
    for hw in regeln.get('lagen_biom_hinweis', []):
        ln = hw['lage']
        if ln not in lagen:
            continue
        d = lagen[ln].astype(np.float32) / 255.0
        m = d >= float(hw['ab_anteil'])
        if 'ab_hoehe_m' in hw:
            m &= hoehe >= float(hw['ab_hoehe_m'])
        verboten = np.isin(bio, [biom_namen.index(b) for b in hw.get('nicht_in', []) if b in biom_namen])
        m &= ~verboten
        profil = np.where(m, 0 if hw['profil'] == 'heide' else 1, profil).astype(np.int8)
        biomfak = np.where(m, np.maximum(biomfak, float(hw.get('faktor_min', 0.8))), biomfak).astype(np.float32)
    sperre = np.ones((H, W), np.float32)
    for sn, sp in regeln.get('sperren', {}).items():
        a = lagen_anteil(lagen, sp['lagen'])
        if a is not None:
            sperre = np.where(a >= float(sp['ab_anteil']), float(sp['faktor']), sperre).astype(np.float32)
    wf = regeln.get('wuesten_felder', {})
    sand_sperre = np.zeros((H, W), bool)
    if feld in wf.get('felder', []):
        sperre *= float(wf.get('faktor', 0.7))
        a = lagen_anteil(lagen, wf.get('sand_lagen', ['Sand', 'Sandstein']))
        if a is not None:
            ab_ = float(wf.get('sand_sperre_ab', 0.5))
            sperre *= np.clip(1.0 - a / max(ab_, 1e-3), 0, 1).astype(np.float32)
            sand_sperre = a >= ab_
        meld('Wüstenfeld: Faktor %.2f, Sand-Sperre %.1f %%' % (wf.get('faktor', 0.7), 100 * sand_sperre.mean()))
    basisfak = (biomfak * sperre * float(faktor)).astype(np.float32)
    schnee = lagen.get(regeln['schnee']['lage'])
    schnee = schnee.astype(np.float32) / 255.0 if schnee is not None else None
    ho = regeln['hoehe']
    anteil_prof = {'heide': float((profil == 0).mean()), 'tundra': float((profil == 1).mean())}
    meld('Profil: heide %.0f %%, tundra %.0f %%; mittlerer Basisfaktor %.2f' % (100 * anteil_prof['heide'], 100 * anteil_prof['tundra'], basisfak.mean()))

    # --- Flecken (Rauschen) je Name
    flecken = {}
    for fn, fp in regeln['flecken'].items():
        if not isinstance(fp, dict):
            continue
        n = wertrauschen(ii_abs, jj_abs, fp['skala_m'], seed, 1000 + 13 * len(flecken), int(fp.get('oktaven', 2)))
        flecken[fn] = smoothstep((n - float(fp['schwelle'])) / max(float(fp.get('weich', 0.1)), 1e-3))

    lagen_fak_cache = {}

    def lagen_fak(name):
        if name not in lagen_fak_cache:
            f = lagen_faktor(lagen, regeln['lagen_gewichte'][name]) if lagen else None
            lagen_fak_cache[name] = f
        return lagen_fak_cache[name]

    # --- Klassen
    wind = regeln['wind']
    lee = math.radians(float(wind.get('richtung_grad', 300)) + 180.0)  # leewärts (Kompass, 0 = N)
    lee_x, lee_y = math.sin(lee), -math.cos(lee)  # X = +j (Ost), Y = +i (Süd)
    ergebnis = {}  # klasse → dict(arrays)
    kanal = 10
    klassen = regeln['klassen']
    for kn, kl in klassen.items():
        kanal += 50
        if kn == 'moorstein' and ufer_da:
            meld('  %-14s übersprungen (Ufer-Ebene vorhanden)' % kn)
            continue
        netze_heide = kl['netze'].get('heide', kl['netze'].get('beide', []))
        netze_tundra = kl['netze'].get('tundra', kl['netze'].get('beide', []))
        d_h, d_t = float(kl['dichte'].get('heide', 0)), float(kl['dichte'].get('tundra', 0))
        if (d_h <= 0 or not netze_heide) and (d_t <= 0 or not netze_tundra):
            continue
        p = np.where(profil == 0, d_h if netze_heide else 0.0, d_t if netze_tundra else 0.0).astype(np.float32) * basisfak
        # Lagen
        lf = lagen_fak(kl.get('lagen', 'pflanze_trocken'))
        if lf is not None:
            p *= lf
        # Hang
        hv, hn = float(kl.get('hang_voll_bis', 28)), float(kl.get('hang_null_ab', 40))
        p *= np.clip((hn - hang) / max(hn - hv, 1e-3), 0, 1)
        # Höhe (nur tundra-Profil hat endliche Grenzen)
        if 'hoehe_grenze' in kl:
            for pi, pn in ((0, 'heide'), (1, 'tundra')):
                grenze = float(ho[pn].get(kl['hoehe_grenze'], 9999))
                ab_h = float(ho[pn].get(kl.get('hoehe_abnahme', ''), grenze - 20)) if grenze < 9000 else 9999
                if grenze < 9000:
                    fh = np.clip((grenze - hoehe) / max(grenze - ab_h, 1e-3), 0, 1)
                    p = np.where(profil == pi, p * fh, p)
        if 'hoehe_max_m_tundra' in kl:
            p = np.where((profil == 1) & (hoehe > float(kl['hoehe_max_m_tundra'])), 0, p)
        # Schnee
        if schnee is not None and kl.get('schnee'):
            fv = float(regeln['schnee']['faktor_steine_bei_voll' if kl['schnee'] == 'stein' else 'faktor_pflanzen_bei_voll'])
            p *= (1 - (1 - fv) * schnee)
        # Kronendach
        if not kl.get('ohne_kronen_faktor', False):
            p *= (1 - (1 - float(kd.get('pflanzen_faktor_bei_voll', 0.25))) * beschattung)
        # Flecken
        if kl.get('flecken') in flecken:
            p *= flecken[kl['flecken']]
        # Exposition / Mulde / Wasser / Baumnähe
        if 'expo_bonus' in kl:
            p *= (1 + float(kl['expo_bonus']) * np.clip(expo, 0, 1))
        if 'mulde_bonus' in kl and 'mulde_gruppe' not in kl:
            p *= (1 + (float(kl['mulde_bonus']) - 1) * mulde)
        if 'wasser_bonus' in kl:
            wb = float(kl.get('wasser_bonus_m', 40))
            p *= (1 + (float(kl['wasser_bonus']) - 1) * np.clip(1 - d_wasser / wb, 0, 1))
        if 'baum_naehe_bonus' in kl:
            r = int(kl.get('baum_naehe_m', 12))
            if r not in baum_nah:
                baum_nah[r] = dilate(baum_mask, r)
            p *= np.where(baum_nah[r], float(kl['baum_naehe_bonus']), 1.0)
        # Wasserkante-Band
        if 'wasser_band_m' in kl:
            a0, a1 = kl['wasser_band_m']
            band = ((d_wasser >= a0) & (d_wasser <= a1)).astype(np.float32)
            if kl.get('feucht_lagen_auch'):
                fa = lagen_anteil(lagen, kl['feucht_lagen_auch'])
                if fa is not None:
                    band = np.maximum(band, (fa >= float(kl.get('feucht_ab_anteil', 0.5))) * float(kl.get('feucht_faktor', 0.35)))
            p *= band
            ok = land & ~wasser & ~ort_m & ~sonst_nah & ~stamm
        else:
            ok = land & ~wasser & (d_wasser >= float(kl.get('wasser_min', 0.5))) & ~ort_m & ~sonst_nah & ~stamm
        ok &= ~(weg_gross if kl.get('weg', 'klein') == 'gross' else weg_klein)
        if 'baum_abstand_m' in kl:
            r = int(math.ceil(float(kl['baum_abstand_m'])))
            if ('b', r) not in baum_nah:
                baum_nah[('b', r)] = dilate(baum_mask, r)
            ok &= ~baum_nah[('b', r)]
        p = np.where(ok, p, 0).astype(np.float32)
        p = np.minimum(p, 0.95)

        # --- Ziehen: Einzel oder Gruppen (Zentren + Mitglieder)
        gmin, gmax = kl.get('gruppe', [1, 1])
        if 'mulde_gruppe' in kl:  # Bäume: Einzel auf Kuppen, Gruppen in Mulden
            mg0, mg1 = kl['mulde_gruppe']
            ist_mulde = mulde > 0.35
            n_mittel = np.where(ist_mulde, (mg0 + mg1) / 2.0, 1.0).astype(np.float32)
            p_center = p * np.where(ist_mulde, float(kl.get('mulde_bonus', 3.0)), 1.0) / n_mittel
        else:
            n_mittel = np.float32((gmin + gmax) / 2.0)
            p_center = p / n_mittel
        zent = hash01(ii_abs, jj_abs, seed, kanal) < p_center
        ci, cj = np.nonzero(zent)
        if len(ci) == 0:
            continue
        ci_abs, cj_abs = ci + wi0, cj + wj0
        if 'mulde_gruppe' in kl:
            im = ist_mulde[ci, cj]
            mg0, mg1 = kl['mulde_gruppe']
            n = np.where(im, mg0 + (hash01(ci_abs, cj_abs, seed, kanal + 1) * (mg1 - mg0 + 1)).astype(np.int32), 1).astype(np.int32)
            rad = np.where(im, float(kl.get('mulde_radius_m', 8)), 0.0).astype(np.float32)
        else:
            n = (gmin + hash01(ci_abs, cj_abs, seed, kanal + 1) * (gmax - gmin + 1)).astype(np.int32)
            rad = np.full(len(ci), float(kl.get('radius_m', 0)), np.float32)
        n = np.clip(n, 1, max(gmax, kl.get('mulde_gruppe', [1, 1])[1]))
        tot = int(n.sum())
        rep = np.repeat(np.arange(len(ci)), n)
        m_idx = np.arange(tot) - np.repeat(np.cumsum(n) - n, n)
        pci, pcj = ci_abs[rep], cj_abs[rep]
        ang = hash01(pci, pcj, seed, kanal + 2 + 3 * m_idx) * 2 * np.pi
        rr = np.sqrt(hash01(pci, pcj, seed, kanal + 3 + 3 * m_idx)) * rad[rep]
        rr = np.where(m_idx == 0, 0.0, rr)
        fi = ci[rep] + hash01(pci, pcj, seed, kanal + 4 + 3 * m_idx) + rr * np.sin(ang) - 0.5
        fj = cj[rep] + hash01(pci, pcj, seed, kanal + 6 + 3 * m_idx) + rr * np.cos(ang) - 0.5
        gi = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
        gj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
        gut = (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1) & ok[gi, gj]
        if 'mulde_gruppe' not in kl and gmax > 1:
            gut &= (p[gi, gj] > 0)  # Mitglieder nur dort, wo die Klasse überhaupt darf
        fi, fj, gi, gj, pci, pcj, m_idx = fi[gut], fj[gut], gi[gut], gj[gut], pci[gut], pcj[gut], m_idx[gut]
        if len(fi) == 0:
            continue
        # Mindestabstand innerhalb der Klasse für Bäume (eine Instanz je Zelle von baum_abstand_m)
        if 'baum_abstand_m' in kl:
            d = max(2, int(round(float(kl['baum_abstand_m']) * 0.7)))
            key = (gi // d).astype(np.int64) * 100000 + (gj // d)
            _, erste = np.unique(key, return_index=True)
            keep = np.zeros(len(fi), bool)
            keep[erste] = True
            fi, fj, gi, gj, pci, pcj, m_idx = fi[keep], fj[keep], gi[keep], gj[keep], pci[keep], pcj[keep], m_idx[keep]
        # --- Attribute
        nn = len(fi)
        kan = kanal + 20 + 3 * m_idx
        prof_i = profil[gi, gj]
        s0, s1 = kl['massstab']
        sk = (s0 + hash01(pci, pcj, seed, kan) * (s1 - s0)).astype(np.float32)
        if kl.get('wind'):
            ex = expo[gi, gj]
            mu = mulde[gi, gj]
            e0, e1 = wind.get('massstab_expo', [0.6, 0.85])
            m0, m1 = wind.get('massstab_mulde', [0.95, 1.25])
            sk = sk * np.where(ex > float(wind.get('expo_ab', 0.25)), e0 + (e1 - e0) * hash01(pci, pcj, seed, kan + 1), 1.0)
            sk = sk * np.where(mu > 0.35, m0 + (m1 - m0) * hash01(pci, pcj, seed, kan + 2), 1.0)
        sk = sk.astype(np.float32)
        # Netzwahl je Profil
        netz_idx = np.where(prof_i == 0,
                            (hash01(pci, pcj, seed, kan + 7) * len(netze_heide)).astype(np.int32),
                            (hash01(pci, pcj, seed, kan + 7) * len(netze_tundra)).astype(np.int32))
        netz = np.array([netze_heide[k] if pr == 0 else netze_tundra[k] for pr, k in zip(prof_i, netz_idx)], dtype=object)
        # Höhe/Eingraben
        z = bilinear(hoehe, fi, fj)
        if 'eingraben_anteil' in kl:
            nh = np.array([inv.get(pf, 0.3) if inv else 0.3 for pf in netz], np.float32)
            z = z - float(kl['eingraben_anteil']) * nh * sk
        else:
            z = z - float(kl.get('eingraben_cm', 3)) / 100.0
        # Rotation: Kippen auf Normale (Anteil), Wind-Lehnen, Yaw
        kip = float(kl.get('kippen', 0.3))
        tx = kip * nx_[gi, gj]
        ty = kip * ny_[gi, gj]
        tz = (1 - kip) + kip * nz_[gi, gj]
        if kl.get('wind'):
            ex = np.clip(expo[gi, gj], 0, 1)
            l0, l1 = wind.get('lehn_grad', [4, 12])
            lehn = np.radians(l0 + (l1 - l0) * hash01(pci, pcj, seed, kan + 3)) * (ex > float(wind.get('expo_ab', 0.25)))
            tx = tx + np.sin(lehn) * lee_x
            ty = ty + np.sin(lehn) * lee_y
        yaw = (hash01(pci, pcj, seed, kan + 4) * 2 * np.pi).astype(np.float32)
        if kl.get('rolle') == 'totholz' and kl.get('gruppe_name') != 'zweige':
            # liegende Stämme längs zum Hang (Fallrichtung) ± 25°
            yaw = (np.arctan2(dhi[gi, gj], dhj[gi, gj]) + (hash01(pci, pcj, seed, kan + 5) - 0.5) * np.radians(50)).astype(np.float32)
        q = quaternionen(tx.astype(np.float32), ty.astype(np.float32), tz.astype(np.float32), yaw)
        x_cm = ((fj + wj0) - X0) * 100.0
        y_cm = ((fi + wi0) - Y0) * 100.0
        im_feld = (gi + wi0 >= i0) & (gi + wi0 < i1) & (gj + wj0 >= j0) & (gj + wj0 < j1)
        ergebnis[kn] = {
            'x': x_cm.astype(np.float32), 'y': y_cm.astype(np.float32), 'z': (z * 100.0).astype(np.float32),
            'q': q, 's': sk, 'netz': netz, 'im_feld': im_feld, 'gi': gi, 'gj': gj,
            'thin': hash01(pci, pcj, seed, kan + 9), 'klasse': kl,
        }
        meld('  %-14s %7d Instanzen (%d im Feld), Dichte-Mittel %.4f/m²' % (kn, nn, int(im_feld.sum()), float(p.mean())))

    # --- Budget: Ausdünnen nach Priorität (nur Instanzen im Feld zählen)
    bud = regeln['budget']
    prio = list(bud.get('prioritaet', list(klassen.keys())))
    prio = [k for k in prio if k in ergebnis] + [k for k in ergebnis if k not in prio]
    maxi, maxk = int(bud.get('instanzen_je_feld', 60000)), int(bud.get('kollision_je_feld', 3000))

    def koll_flag(kn, netz):
        kl = klassen[kn]
        if not kl.get('kollision', False):
            return np.zeros(len(netz), bool)
        ab_h = float(kl.get('kollision_ab_hoehe_m', 0))
        return np.array([(inv.get(pf, 0.3) if inv else 0.3) >= ab_h for pf in netz], bool)

    for kn in ergebnis:
        ergebnis[kn]['koll'] = koll_flag(kn, ergebnis[kn]['netz'])
        ergebnis[kn]['keep'] = ergebnis[kn]['im_feld'].copy()
    gesamt = sum(int(e['keep'].sum()) for e in ergebnis.values())
    if gesamt > maxi:
        meld('Budget: %d > %d – dünne aus (niedrigste Priorität zuerst)' % (gesamt, maxi))
        for kn in reversed(prio):
            if gesamt <= maxi:
                break
            e = ergebnis[kn]
            n = int(e['keep'].sum())
            ziel = max(int(n * 0.25), n - (gesamt - maxi))
            if ziel < n:
                frac = ziel / max(n, 1)
                e['keep'] &= e['thin'] < frac
                gesamt -= n - int(e['keep'].sum())
    koll = sum(int((e['keep'] & e['koll']).sum()) for e in ergebnis.values())
    if koll > maxk:
        meld('Kollision: %d > %d – dünne Kollisionsklassen aus' % (koll, maxk))
        for kn in reversed(prio):
            if koll <= maxk:
                break
            e = ergebnis[kn]
            n = int((e['keep'] & e['koll']).sum())
            if n == 0:
                continue
            ziel = max(0, n - (koll - maxk))
            frac = ziel / max(n, 1)
            drop = e['koll'] & (e['thin'] >= frac)
            e['keep'] &= ~drop
            koll -= n - int((e['keep'] & e['koll']).sum())

    # --- Ausgabe
    out_dir = os.path.join(basis, regeln['ausgabe']['ordner'], feld)
    os.makedirs(out_dir, exist_ok=True)
    for alt in os.listdir(out_dir):
        if alt.endswith('.f32'):
            os.remove(os.path.join(out_dir, alt))
    dateien = {}
    schichten = {}
    klassen_n = {}
    total = 0
    for kn, e in ergebnis.items():
        kl = e['klasse']
        keep = e['keep']
        if not keep.any():
            continue
        klassen_n[kn] = int(keep.sum())
        schichten[kl['schicht']] = schichten.get(kl['schicht'], 0) + int(keep.sum())
        netz = e['netz'][keep]
        rows = np.concatenate([e['x'][keep, None], e['y'][keep, None], e['z'][keep, None], e['q'][keep],
                               e['s'][keep, None], e['s'][keep, None], e['s'][keep, None]], axis=1).astype('<f4')
        for pf in np.unique(netz):
            m = netz == pf
            name = pf.split('/')[-1]
            arr = rows[m]
            with open(os.path.join(out_dir, name + '.f32'), 'ab') as f:
                arr.tofile(f)
            d = dateien.setdefault(name, {'pfad': pf, 'anzahl': 0, 'gruppe': kl.get('gruppe_name', kn), 'rolle': kl.get('rolle', kn),
                                          'sichtweite': [int(v) for v in kl.get('sichtweite', [0, 0])],
                                          'schatten': bool(kl.get('schatten', False)),
                                          'kollision': bool(kl.get('kollision', False) and (inv.get(pf, 0.3) if inv else 0.3) >= float(kl.get('kollision_ab_hoehe_m', 0))),
                                          'schicht': kl['schicht'], 'klasse': kn})
            d['anzahl'] += int(m.sum())
            total += int(m.sum())
    koll_n = sum(d['anzahl'] for d in dateien.values() if d['kollision'])
    plan = {
        'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'ebene': regeln.get('ebene', 'heide_tundra'), 'instanzen': total,
        'dateien': dateien, 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
        'klassen': klassen_n, 'schichten': schichten, 'kollision_instanzen': koll_n,
        'profil_anteil': anteil_prof, 'biome_fenster': biom_anteile, 'quellen_bestand': quellen,
        'faktor': faktor, 'seed': seed, 'laufzeit_s': round(time.time() - t0, 1),
        'hinweis': 'UNGETESTET MIT ECHTDATEN; Setzer: HISM je Netz, Kollision nur wo kollision=true, sichtweite in cm.',
    }
    ent = entfernen_cli
    if ent is None:
        prof_dom = 'heide' if anteil_prof['heide'] >= anteil_prof['tundra'] else 'tundra'
        ent = regeln.get('entfernen', {}).get(prof_dom, '')
    if ent:
        plan['entfernen'] = ent
    with open(os.path.join(out_dir, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('Feld %s: %d Instanzen (%d mit Kollision) in %d Netzen → %s  [%.1f s]' % (feld, total, koll_n, len(dateien), out_dir, time.time() - t0))
    for s in sorted(schichten):
        meld('   Schicht %-14s %6d' % (s, schichten[s]))

    if bild:
        schreibe_bild(basis, regeln, feld, fb, win, hoehe, wasser, weg, ort, profil, sand_sperre, ergebnis)
    return plan


def schreibe_bild(basis, regeln, feld, fb, win, hoehe, wasser, weg, ort, profil, sand_sperre, ergebnis):
    i0, i1, j0, j1 = fb
    wi0, wi1, wj0, wj1 = win
    a0, a1, b0, b1 = i0 - wi0, i1 - wi0, j0 - wj0, j1 - wj0
    h = hoehe[a0:a1, b0:b1]
    H, W = h.shape
    fb_ = regeln.get('bild_farben', {})
    # Schummerung
    dj = np.gradient(h, axis=1)
    di = np.gradient(h, axis=0)
    shade = np.clip(0.55 + 0.45 * (-0.7 * dj - 0.5 * di) / np.sqrt(dj * dj + di * di + 1), 0.2, 1.0)
    img = np.zeros((H, W, 3), np.float32)
    ph = np.array(fb_.get('heide_profil', [70, 50, 70]), np.float32)
    pt = np.array(fb_.get('tundra_profil', [60, 70, 60]), np.float32)
    pr = profil[a0:a1, b0:b1]
    img[:] = np.where(pr[..., None] == 0, ph, pt) * (0.6 + 0.8 * shade[..., None])
    img[h <= 0.05] = [30, 40, 70]
    img[sand_sperre[a0:a1, b0:b1]] = fb_.get('sand_sperre', [210, 190, 140])
    img[wasser[a0:a1, b0:b1]] = fb_.get('wasser', [40, 80, 160])
    img[weg[a0:a1, b0:b1]] = fb_.get('weg', [230, 200, 120])
    img[ort[a0:a1, b0:b1]] = fb_.get('ort', [200, 60, 60])
    img = np.clip(img, 0, 255).astype(np.uint8)
    for kn, e in ergebnis.items():
        keep = e['keep']
        if not keep.any():
            continue
        gi, gj = e['gi'][keep] - a0, e['gj'][keep] - b0
        m = (gi >= 0) & (gi < H) & (gj >= 0) & (gj < W)
        col = np.array(e['klasse'].get('farbe', [255, 255, 255]), np.uint8)
        r = 1 if e['klasse']['schicht'].startswith('2') or kn in ('kruepelkiefer', 'totholz') else 0
        for di_ in range(-r, r + 1):
            for dj_ in range(-r, r + 1):
                gi2, gj2 = np.clip(gi[m] + di_, 0, H - 1), np.clip(gj[m] + dj_, 0, W - 1)
                img[gi2, gj2] = col
    out_dir = os.path.join(basis, regeln['ausgabe']['bild'])
    os.makedirs(out_dir, exist_ok=True)
    try:
        from PIL import Image
        Image.fromarray(img, 'RGB').save(os.path.join(out_dir, feld + '.png'))
        meld('Bild: %s' % os.path.join(out_dir, feld + '.png'))
    except Exception as ex:
        p = os.path.join(out_dir, feld + '.ppm')
        with open(p, 'wb') as f:
            f.write(b'P6 %d %d 255\n' % (W, H))
            f.write(img.tobytes())
        meld('Pillow fehlt (%s) – PPM geschrieben: %s' % (ex, p))


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description='Eldarien Heide/Tundra-Planer (Ebene heide_tundra)')
    ap.add_argument('felder', nargs='+', help='Gitterfelder, z. B. D2 G5')
    ap.add_argument('--bild', action='store_true', help='Draufsicht PNG nach docs/pruefung/heide_tundra/')
    ap.add_argument('--faktor', type=float, default=1.0, help='globaler Dichtefaktor')
    ap.add_argument('--basis', default='.', help='production-Wurzel (Standard: aktuelles Verzeichnis)')
    ap.add_argument('--regeln', default=None, help='Regeln-JSON (Standard: heide_tundra_regeln.json neben dem Skript)')
    ap.add_argument('--entfernen', default=None, help='Netznamen-Präfixe alter Instanzen für plan.json["entfernen"]')
    args = ap.parse_args()
    skript_dir = os.path.dirname(os.path.abspath(__file__))
    rp = args.regeln or os.path.join(skript_dir, 'heide_tundra_regeln.json')
    if not os.path.isfile(rp):
        raise SystemExit('Regeln fehlen: %s' % rp)
    regeln = json.load(open(rp, encoding='utf-8'))
    basis = os.path.abspath(args.basis)
    if not os.path.isfile(os.path.join(basis, WELT, 'hoehe.f32')):
        raise SystemExit('hoehe.f32 fehlt unter %s – --basis auf die production-Wurzel setzen' % os.path.join(basis, WELT))
    meld('numba %s, NumPy %s, Regeln %s (Seed %d)' % ('vorhanden' if NUMBA else 'nicht vorhanden (nicht nötig)', np.__version__, rp, regeln.get('seed', 0)))
    inv = lade_inventar(basis, skript_dir)
    pruefe_paletten(regeln, inv)
    for feld in args.felder:
        try:
            plane_feld(feld, basis, regeln, args.faktor, args.bild, inv, args.entfernen)
        except SystemExit:
            raise
        except MemoryError:
            meld('FEHLER: Speicher reicht nicht für Feld %s' % feld)
            sys.exit(2)


if __name__ == '__main__':
    main()
