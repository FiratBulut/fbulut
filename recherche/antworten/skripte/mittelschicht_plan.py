#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien – Planer „Mittelschicht“ (Schicht 1, 0,3–3 m): Sträucher, Jungbäume, Farn-/Beereninseln, Hochstauden,
Grasbüschel, Schilf, liegendes Totholz, Stümpfe, Äste, Wurzeln, Pilze, Kletterpflanzen, stehende Totbäume.
Füllt die „Leere“ zwischen Boden-Kleinzeug und Baumkronen nach Lichtverhältnis (Kronendach aus Baum-Ebenen),
Waldrand-Saum, Feuchte, Hang, Höhe und Biom (eigner.r8 + welt.json).

Aufruf (lokal, production-Wurzel):
    python -I scripts/mittelschicht/mittelschicht_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]

Liest:   export/unreal/welt/hoehe.f32 (memmap, Fenster Feld + 64 m), lage_*.r8 (optional), karte_wasser/weg/ort.r8,
         eigner.r8 + welt.json (Biom je Zelle, Fallback aus Regeln/aue), bestand/<Feld>/, witcher/<Feld>/ (+ Nachbarfelder),
         instanzen/instanzen.json (Houdini-Bäume, optional) für Kronendach und Abstände.
Schreibt: export/unreal/welt/mittelschicht/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm, qx,qy,qz,qw, sx,sy,sz)
          + plan.json (FORMAT.md §3), bei --bild docs/pruefung/mittelschicht/<Feld>.png (1 px = 1 m).
Regeln:  scripts/mittelschicht/mittelschicht_regeln.json (neben dem Skript) oder --regeln PFAD.

Nur NumPy (separierbare Box-Faltungen, Jump-Flooding-Distanzfeld, Hash-Zufall aus Rasterkoordinate → deterministisch,
Nachbarfelder nahtlos). numba wird nicht benötigt (Import nur zur Meldung). Laufzeit-Ziel ≤ 60 s je Feld.

Quellen: FORMAT.md §1–§5; antworten/bildkritik-witcher-messlatte.md (Waldstruktur, Top 5); antworten/boden-kleinzeug-gras.md;
Naturschutzbund „Waldränder“ (Strauchgürtel 5–10 m, Waldmantel 10–20 m); Harms et al. 2004 Biotropica (Jungwuchs 0,7–7,5/m²);
80.lv „World building of Witcher 3“ (Biom-Pinsel, ~20 Baum-/Straucharten); SpeedTree-Fallstudie Witcher 3 (~200 Pflanzentypen).

UNGETESTET MIT ECHTDATEN – in der Cloud nur mit synthetischen Rastern rauchgetestet (siehe verteilung-leere-fuellen.md §5).
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

try:  # numba optional – wird nicht benötigt, nur Meldung
    import numba  # noqa: F401
    NUMBA = True
except Exception:  # pragma: no cover
    NUMBA = False

NX, NY = 9577, 7057
FELD_M = 1008
X0, Y0 = 4730.5, 4060.5  # X_cm = (j - 4730.5)*100, Y_cm = (i - 4060.5)*100
WELT = os.path.join('export', 'unreal', 'welt')
BAUM_ROLLEN = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel', 'palme', 'hainbuche')


# ----------------------------------------------------------------------------- kleine Helfer
def meld(*a):
    print('[mittelschicht]', *a, flush=True)


def feld_fenster(feld, rand):
    """Feld 'G4' → (i0, i1, j0, j1) des Feldes und des Fensters (geklippt auf das Raster)."""
    feld = feld.strip().upper()
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    j0, j1 = s * FELD_M, (s + 1) * FELD_M
    i0, i1 = (r - 1) * FELD_M, r * FELD_M
    wi0, wi1 = max(0, i0 - rand), min(NY, i1 + rand)
    wj0, wj1 = max(0, j0 - rand), min(NX, j1 + rand)
    return (i0, min(i1, NY), j0, min(j1, NX)), (wi0, wi1, wj0, wj1)


def lade_raster(pfad, dtype, win, pflicht=False):
    """Fenster-Ausschnitt eines NY×NX-Rasters per memmap (nur das Fenster wird gelesen)."""
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            raise SystemExit('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        meld('WARNUNG: %s hat %d Werte, erwartet %d – Datei wird ignoriert' % (pfad, n, NX * NY))
        if pflicht:
            raise SystemExit('Pflichtdatei hat falsche Größe')
        return None
    mm = np.memmap(pfad, dtype=dtype, mode='r', shape=(NY, NX))
    return np.array(mm[wi0:wi1, wj0:wj1])


def box_blur(a, r):
    """Separierbarer Box-Filter (Radius r Zellen) über Summenbild, Rand gespiegelt."""
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
    """3 Box-Durchläufe ≈ Gauß (sigma in Zellen)."""
    w = math.sqrt(12.0 * sigma * sigma / 3.0 + 1.0)
    r = max(1, int(round((w - 1) / 2)))
    out = a
    for _ in range(3):
        out = box_blur(out, r)
    return out


def verschiebe(a, di, dj, fill):
    """Array um (di, dj) verschieben: out[i, j] = a[i + di, j + dj]."""
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
    """Binäre Dilatation mit ≈ Kreisscheibe (Radius r Zellen, Oktagon durch Wechsel 4er/8er-Nachbarschaft)."""
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
    """Euklidische Distanz (m) zur nächsten True-Zelle per Jump-Flooding (vektorisiert). Größer max_m → max_m*2."""
    H, W = mask.shape
    fern = np.float32(max_m * 2.0)
    if not mask.any():
        return np.full((H, W), fern, np.float32)
    ii, jj = np.indices((H, W), dtype=np.int32)
    si = np.where(mask, ii, -1).astype(np.int32)
    sj = np.where(mask, jj, -1).astype(np.int32)
    INF = np.int32(2 ** 30)
    d2 = np.where(mask, 0, INF).astype(np.int32)
    schritt = 1
    while schritt * 2 <= max_m:
        schritt *= 2
    schritte = []
    s = schritt
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
                gueltig = csi >= 0
                cd2 = (ii - csi) ** 2 + (jj - csj) ** 2
                besser = gueltig & (cd2 < d2)
                d2 = np.where(besser, cd2, d2)
                si = np.where(besser, csi, si)
                sj = np.where(besser, csj, sj)
    d = np.sqrt(d2.astype(np.float32))
    d[d2 >= INF] = fern
    return np.minimum(d, fern).astype(np.float32)


def hash01(i, j, seed, kanal):
    """Deterministische Zufallszahl [0,1) je (Rasterzeile, Rasterspalte, Seed, Kanal)."""
    i = np.asarray(i).astype(np.int64)
    j = np.asarray(j).astype(np.int64)
    h = (i * 73856093) ^ (j * 19349663) ^ (int(seed) * 83492791 + int(kanal) * 2654435761)
    h = h & 0xFFFFFFFF
    h = h.astype(np.uint32)
    with np.errstate(over='ignore'):
        h ^= h >> np.uint32(16)
        h *= np.uint32(0x7FEB352D)
        h ^= h >> np.uint32(15)
        h *= np.uint32(0x846CA68B)
        h ^= h >> np.uint32(16)
    return (h & np.uint32(0xFFFFFF)).astype(np.float32) / np.float32(16777216.0)


def bilinear(h, fi, fj):
    """Höhe an Fließkomma-Fensterkoordinaten (fi, fj)."""
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


def quaternionen(nx, ny, nz, kippen, yaw):
    """Z-Achse um Anteil `kippen` auf die Geländenormale kippen, davor Zufalls-Yaw. Ergebnis (n,4) = x,y,z,w."""
    n = len(nx)
    tz = (1 - kippen) + kippen * nz
    tx = kippen * nx
    ty = kippen * ny
    l = np.sqrt(tx * tx + ty * ty + tz * tz) + 1e-9
    tx, ty, tz = tx / l, ty / l, tz / l
    # Rotation von (0,0,1) nach t: Achse = z × t = (-ty, tx, 0), w = 1 + tz
    qt = np.stack([-ty, tx, np.zeros(n, np.float32), 1 + tz], axis=1)
    qt /= (np.linalg.norm(qt, axis=1, keepdims=True) + 1e-9)
    qy = np.stack([np.zeros(n, np.float32), np.zeros(n, np.float32), np.sin(yaw / 2), np.cos(yaw / 2)], axis=1)
    q = quat_mul(qt, qy)
    return (q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-9)).astype(np.float32)


# ----------------------------------------------------------------------------- Weltdaten
def lade_biome(basis, win, regeln, feld):
    """Biom-Index je Zelle (Index in regeln['biome']-Reihenfolge), Fallback je Feld aus Regeln, sonst aue."""
    namen = list(regeln['biome'].keys())
    fb = regeln.get('feld_biom_fallback', {}).get(feld, 'aue')
    if fb not in namen:
        fb = 'aue'
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    if eig is None or not os.path.isfile(wj):
        meld('Hinweis: eigner.r8/welt.json fehlen – Biom je Zelle = Fallback %r' % fb)
        return np.full((H, W), namen.index(fb), np.int16), {fb: 1.0}
    try:
        welt = json.load(open(wj, encoding='utf-8'))
    except Exception as e:
        meld('Hinweis: welt.json unlesbar (%s) – Fallback %r' % (e, fb))
        return np.full((H, W), namen.index(fb), np.int16), {fb: 1.0}
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
    tabelle[0] = namen.index('aue')
    bio = tabelle[eig]
    ant = {namen[k]: float((bio == k).mean()) for k in np.unique(bio)}
    return bio, ant


def lade_ebene_positionen(ordner, win, rollen_baum=True):
    """Positionen (Fenster-i, Fenster-j float) aller Instanzen einer Ebene; Bäume und Sonstige getrennt."""
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
        ist_baum = any(r in txt for r in BAUM_ROLLEN) and 'tot' not in txt and 'stump' not in txt and 'log' not in txt
        (baum if ist_baum else sonst).append(np.stack([fi[m], fj[m], a[m, 9]], axis=1))
    return baum, sonst


def lade_baeume(basis, feld, win):
    """Baum-Positionen aus bestand/, witcher/ (Feld + 8 Nachbarn) und instanzen/instanzen.json."""
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    baum, sonst, quellen = [], [], []
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(ord('A') + ss) + str(rr)
            for ebene in ('bestand', 'witcher'):
                b, so = lade_ebene_positionen(os.path.join(basis, WELT, ebene, nf), win)
                if b or so:
                    quellen.append('%s/%s' % (ebene, nf))
                baum += b
                if ds == 0 and dr == 0:
                    sonst += so
    ij = os.path.join(basis, WELT, 'instanzen', 'instanzen.json')
    if os.path.isfile(ij):
        try:
            inst = json.load(open(ij, encoding='utf-8'))
            for e in inst.get('verzeichnis', []):
                txt = (str(e.get('klasse', '')) + ' ' + str(e.get('name', ''))).lower()
                if not any(k in txt for k in BAUM_ROLLEN):
                    continue
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
                    baum.append(np.stack([fi[m], fj[m], a[m, 9]], axis=1))
                    quellen.append('instanzen/' + os.path.basename(f))
        except Exception as e:
            meld('Hinweis: instanzen.json nicht auswertbar (%s)' % e)
    baum = np.concatenate(baum, axis=0) if baum else np.zeros((0, 3), np.float32)
    sonst = np.concatenate(sonst, axis=0) if sonst else np.zeros((0, 3), np.float32)
    return baum, sonst, quellen


# ----------------------------------------------------------------------------- Planung je Feld
def plane_feld(feld, basis, regeln, faktor, bild):
    t0 = time.time()
    rand = int(regeln.get('fenster_rand_m', 64))
    fb, win = feld_fenster(feld, rand)
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    if H <= 0 or W <= 0:
        meld('Feld %s liegt außerhalb des Rasters' % feld)
        return None
    hinweise = []
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True)
    ii, jj = np.indices((H, W), dtype=np.int32)
    gi, gj = ii + wi0, jj + wj0  # globale Rasterkoordinaten (Determinismus über Feldgrenzen)
    im_feld = (gi >= fb[0]) & (gi < fb[1]) & (gj >= fb[2]) & (gj < fb[3])

    # Gelände: Neigung, Normale
    dzdy, dzdx = np.gradient(hoehe)  # dzdy entlang i (Y), dzdx entlang j (X), 1 m Raster
    hang = np.degrees(np.arctan(np.sqrt(dzdx ** 2 + dzdy ** 2))).astype(np.float32)
    nl = np.sqrt(dzdx ** 2 + dzdy ** 2 + 1.0)
    n_x, n_y, n_z = (-dzdx / nl).astype(np.float32), (-dzdy / nl).astype(np.float32), (1.0 / nl).astype(np.float32)

    # Karten
    def r8(name):
        a = lade_raster(os.path.join(basis, WELT, name), np.uint8, win)
        return a
    wasser = r8('karte_wasser.r8')
    weg = r8('karte_weg.r8')
    ort = r8('karte_ort.r8')
    for nm, a in (('karte_wasser.r8', wasser), ('karte_weg.r8', weg), ('karte_ort.r8', ort)):
        if a is None:
            hinweise.append('%s fehlt – Annahme: keine Fläche dieser Art' % nm)
    wasser_m = (wasser > 0) if wasser is not None else np.zeros((H, W), bool)
    weg_m = (weg > 0) if weg is not None else np.zeros((H, W), bool)
    ort_m = (ort > 0) if ort is not None else np.zeros((H, W), bool)
    abst = regeln['abstand_m']
    d_wasser = distanz(wasser_m, max_m=64.0)
    nah_weg_klein = dilate(weg_m, abst['weg_klein'])
    nah_weg_gross = dilate(weg_m, abst['weg_gross'])
    nah_ort = dilate(ort_m, abst['ort'])
    nah_wasser = dilate(wasser_m, abst['wasser'])

    # Lagen (nur benötigte)
    lagen_namen = set(regeln['feuchte']['lagen']) | set(regeln['licht']['fallback_lagen']) | {regeln['schnee']['lage']}
    for b in regeln['biome'].values():
        for k in b.values():
            lagen_namen |= set(k.get('lagen_faktor', {}).keys())
    lagen = {}
    for ln in sorted(lagen_namen):
        if ln.startswith('ufer_'):
            continue
        a = r8('lage_%s.r8' % ln)
        if a is not None:
            lagen[ln] = a.astype(np.float32) / 255.0
    if not lagen:
        hinweise.append('keine lage_*.r8 gefunden – Feuchte nur aus Wassernähe, Kronendach nur aus Baum-Ebenen')

    # Biome
    bio, bio_anteil = lade_biome(basis, win, regeln, feld)
    biom_namen = list(regeln['biome'].keys())

    # Bäume → Kronendach / Beschattung, Stammabstand
    baeume, sonst, quellen = lade_baeume(basis, feld, win)
    L = regeln['licht']
    if len(baeume):
        bi = np.clip(np.round(baeume[:, 0]).astype(np.int32), 0, H - 1)
        bj = np.clip(np.round(baeume[:, 1]).astype(np.int32), 0, W - 1)
        gew = np.clip(baeume[:, 2], 0.3, 3.0) ** 2  # Kronenfläche ~ Maßstab²
        dichte = np.zeros((H, W), np.float32)
        np.add.at(dichte, (bi, bj), gew.astype(np.float32))
        dichte = gauss_blur(dichte, L['kronen_sigma_m'])
        deckung = math.pi * L['kronen_radius_m'] ** 2 * dichte
        beschattung = (1.0 - np.exp(-L['beschattung_k'] * deckung)).astype(np.float32)
        baum_m = np.zeros((H, W), bool)
        baum_m[bi, bj] = True
        hinweise.append('Kronendach aus %d Bäumen (%s)' % (len(baeume), ', '.join(quellen[:6]) + (' …' if len(quellen) > 6 else '')))
    else:
        beschattung = np.zeros((H, W), np.float32)
        for ln, w in L['fallback_lagen'].items():
            if ln in lagen:
                beschattung += w * lagen[ln]
        beschattung = np.clip(gauss_blur(beschattung, 8.0), 0, L['fallback_beschattung_max']).astype(np.float32)
        baum_m = np.zeros((H, W), bool)
        hinweise.append('keine Baum-Ebene gefunden (bestand/, witcher/, instanzen/) – Beschattung aus Lagen Laub/Nadeln/Moos geschätzt, max %.2f' % L['fallback_beschattung_max'])
    nah_baum = dilate(baum_m, abst['baumstamm']) if baum_m.any() else np.zeros((H, W), bool)
    ring_baum = (dilate(baum_m, 1.6) & ~nah_baum) if baum_m.any() else np.zeros((H, W), bool)
    nah_baum_3 = dilate(baum_m, 3.0) if baum_m.any() else np.zeros((H, W), bool)
    belegt = np.zeros((H, W), bool)
    if len(sonst):
        si = np.clip(np.round(sonst[:, 0]).astype(np.int32), 0, H - 1)
        sj = np.clip(np.round(sonst[:, 1]).astype(np.int32), 0, W - 1)
        belegt[si, sj] = True
        belegt = dilate(belegt, abst['bestand_sonst'])
        hinweise.append('%d vorhandene Nicht-Baum-Instanzen (Witcher/Bestand) als belegt (%.1f m) berücksichtigt' % (len(sonst), abst['bestand_sonst']))

    # Wald / Saum / Lichtung
    wald = beschattung > L['wald_schwelle']
    kante = wald & dilate(~wald, 1)
    d_kante = distanz(kante, max_m=64.0)
    saum_norm = np.where(wald, np.clip(1 - d_kante / L['saum_innen_m'], 0, 1), np.clip(1 - d_kante / L['saum_aussen_m'], 0, 1)).astype(np.float32)
    lichtung = (~wald) & (beschattung < L['lichtung_schwelle']) & (d_kante < 40)
    lichtungsrand = lichtung & (d_kante <= L['lichtungsrand_m'])

    # Feuchte, Hang, Höhe, Schnee
    F = regeln['feuchte']
    feuchte = np.clip(1 - d_wasser / F['wasser_radius_m'], 0, 1) * 0.8
    for ln, w in F['lagen'].items():
        if ln in lagen:
            feuchte += w * lagen[ln]
    feuchte = np.clip(feuchte, 0, 1).astype(np.float32)
    ufer_schilf = (d_wasser <= F['ufer_schilf_m']) & ~nah_wasser
    Hh = regeln['hoehe']
    f_hoehe = np.clip((Hh['null_ab_m'] - hoehe) / max(1.0, Hh['null_ab_m'] - Hh['abnahme_ab_m']), 0, 1).astype(np.float32)
    S = regeln['schnee']
    f_schnee = (1 - (1 - S['faktor_bei_voll']) * lagen[S['lage']]) if S['lage'] in lagen else np.ones((H, W), np.float32)
    voll_bis = regeln['hang']['voll_bis_grad']
    feld_faktor = faktor * (regeln['wuesten_feld_faktor'] if feld in regeln['wuesten_felder'] else 1.0)

    # ------------------------------------------------------------------ Streuung je Biom und Klasse
    seed = int(regeln['seed'])
    gross = set(regeln['gross_klassen'])
    farben = regeln.get('bild_farben', {})
    aus = []  # Listen von Arrays: fi, fj, klasse_idx, netz_idx, massstab, yaw
    klassen_namen = sorted({k for b in regeln['biome'].values() for k in b})
    klassen_idx = {k: n for n, k in enumerate(klassen_namen)}
    netze_je_klasse = {}
    for bname in biom_namen:
        for kname, kl in regeln['biome'][bname].items():
            netze_je_klasse.setdefault(kname, [])
            for p in kl['netze']:
                if p not in netze_je_klasse[kname]:
                    netze_je_klasse[kname].append(p)
    stat = {}
    for bidx, bname in enumerate(biom_namen):
        in_biom = bio == bidx
        if not in_biom.any():
            continue
        for kname, kl in regeln['biome'][bname].items():
            kidx = klassen_idx[kname]
            kanal = bidx * 1000 + kidx * 10
            d0, d1 = kl['dichte']
            lam = (d0 * (1 - beschattung) + d1 * beschattung).astype(np.float32)
            lam *= 1 + (kl['saum'] - 1) * saum_norm
            if kl.get('lichtungsrand', 1.0) != 1.0:
                lam = np.where(lichtungsrand, lam * kl['lichtungsrand'], lam)
            ft, fn = kl['feuchte']
            lam *= ft + (fn - ft) * feuchte
            hm = kl['hang_max']
            if hm < 60:
                lam *= np.clip((hm - hang) / max(1.0, hm - voll_bis), 0, 1)
            lam *= f_hoehe * f_schnee * feld_faktor
            if kl['hoehe_max_m'] < 9000:
                lam = np.where(hoehe > kl['hoehe_max_m'], 0, lam)
            lf = kl.get('lagen_faktor', {})
            for ln, w in lf.items():
                if ln.startswith('ufer_'):
                    lam = np.where(ufer_schilf, lam + w, lam)
                elif ln in lagen:
                    lam *= 1 + (w - 1) * lagen[ln]
            frei = in_biom & ~nah_wasser & ~belegt & ~nah_ort
            frei &= ~(nah_weg_gross if kname in gross else nah_weg_klein)
            if kl.get('an_baum'):
                frei &= ring_baum
            elif kname == 'totbaum':
                frei &= ~nah_baum_3
            else:
                frei &= ~nah_baum
            lam = np.where(frei, lam, 0).astype(np.float32)
            if kl.get('an_baum') and not baum_m.any():
                continue
            gmin, gmax = kl['gruppe']
            gmit = 0.5 * (gmin + gmax)
            if gmax <= 1:
                idx = np.flatnonzero(lam > 0)
                if idx.size == 0:
                    continue
                ci, cj = ii.ravel()[idx], jj.ravel()[idx]
                u = hash01(gi.ravel()[idx], gj.ravel()[idx], seed, kanal)
                keep = u < lam.ravel()[idx]
                ci, cj = ci[keep], cj[keep]
                fi = ci + hash01(ci + wi0, cj + wj0, seed, kanal + 1) - 0.5
                fj = cj + hash01(ci + wi0, cj + wj0, seed, kanal + 2) - 0.5
                mi, mj = ci, cj
            else:
                lamc = lam / gmit
                idx = np.flatnonzero(lamc > 0)
                if idx.size == 0:
                    continue
                ci, cj = ii.ravel()[idx], jj.ravel()[idx]
                u = hash01(gi.ravel()[idx], gj.ravel()[idx], seed, kanal)
                keep = u < lamc.ravel()[idx]
                ci, cj = ci[keep], cj[keep]
                if ci.size == 0:
                    continue
                n = gmin + np.floor(hash01(ci + wi0, cj + wj0, seed, kanal + 1) * (gmax - gmin + 1)).astype(np.int32)
                n = np.minimum(n, gmax)
                rep = np.repeat(np.arange(ci.size), gmax)
                k = np.tile(np.arange(gmax), ci.size)
                ok = k < n[rep]
                rep, k = rep[ok], k[ok]
                ang = hash01(ci[rep] + wi0 + 7 * k, cj[rep] + wj0 + 13 * k, seed, kanal + 3) * 2 * math.pi
                rad = np.sqrt(hash01(ci[rep] + wi0 + 3 * k, cj[rep] + wj0 + 5 * k, seed, kanal + 4)) * kl['radius_m']
                fi = ci[rep] + rad * np.sin(ang)
                fj = cj[rep] + rad * np.cos(ang)
                mi = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
                mj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
                ok = lam[mi, mj] > 0
                fi, fj, mi, mj = fi[ok], fj[ok], mi[ok], mj[ok]
            if fi.size == 0:
                continue
            # nur Instanzen im Feld ausgeben (Rand nur für Gruppen/Nahtlosigkeit)
            ok = im_feld[mi, mj]
            fi, fj, mi, mj = fi[ok], fj[ok], mi[ok], mj[ok]
            if fi.size == 0:
                continue
            gmi, gmj = mi + wi0, mj + wj0
            hv = hash01(gmi, gmj, seed, kanal + 5) + 0.37 * hash01(np.round(fi * 7).astype(np.int64), np.round(fj * 7).astype(np.int64), seed, kanal + 6)
            hv = hv % 1.0
            netzl = kl['netze']
            nidx = np.minimum((hv * len(netzl)).astype(np.int32), len(netzl) - 1)
            nglob = np.array([netze_je_klasse[kname].index(netzl[x]) for x in range(len(netzl))], np.int32)[nidx]
            ms = kl['massstab'][0] + (kl['massstab'][1] - kl['massstab'][0]) * hash01(gmi, gmj, seed, kanal + 7)
            yaw = hash01(gmi, gmj, seed, kanal + 8) * 2 * math.pi
            if kl.get('laengs_hang'):
                asp = np.arctan2(-dzdy[mi, mj], -dzdx[mi, mj])  # Richtung hangabwärts (X,Y)
                yaw = asp + (hash01(gmi, gmj, seed, kanal + 9) - 0.5) * math.radians(40) + np.where(hash01(gmi, gmj, seed, kanal + 8) < 0.5, 0, math.pi)
            aus.append(dict(fi=fi.astype(np.float32), fj=fj.astype(np.float32), mi=mi, mj=mj, klasse=kname, netz=nglob,
                            massstab=ms.astype(np.float32), yaw=yaw.astype(np.float32), kippen=kl['kippen'],
                            eingraben=kl['eingraben_cm'], kollision=bool(kl['kollision']), sichtweite=kl['sichtweite']))
            stat[kname] = stat.get(kname, 0) + int(fi.size)

    # ------------------------------------------------------------------ Budget
    Bg = regeln['budget']
    gesamt = sum(stat.values())
    koll = sum(int(a['fi'].size) for a in aus if a['kollision'])
    prio = Bg['prioritaet']
    ausduenn = {}
    if koll > Bg['kollision_je_feld']:
        f = Bg['kollision_je_feld'] / float(koll)
        for a in aus:
            if a['kollision']:
                ausduenn[a['klasse']] = min(ausduenn.get(a['klasse'], 1.0), f)
        hinweise.append('Kollisionsbudget: %d → %d (Faktor %.2f auf Totholz/Stümpfe/Totbäume)' % (koll, Bg['kollision_je_feld'], f))
    if gesamt > Bg['ziel_instanzen_je_feld']:
        ueber = gesamt - Bg['ziel_instanzen_je_feld']
        # gemeinsam proportional dünnen: von unten so viele Klassen einbeziehen, dass höchstens 50 % je Klasse wegfallen
        pool, summe = [], 0
        for kname in reversed(prio):
            n = stat.get(kname, 0)
            if n == 0:
                continue
            pool.append(kname)
            summe += n
            if summe * 0.5 >= ueber:
                break
        f = max(0.0, 1.0 - ueber / float(max(1, summe)))
        for kname in pool:
            ausduenn[kname] = min(ausduenn.get(kname, 1.0), f)
        hinweise.append('Instanzbudget: %d → Ziel %d, Ausdünnung %s' % (gesamt, Bg['ziel_instanzen_je_feld'], {k: round(v, 2) for k, v in ausduenn.items()}))
    for a in aus:
        f = ausduenn.get(a['klasse'], 1.0)
        if f < 1.0:
            keep = hash01(a['mi'] + wi0, a['mj'] + wj0, seed, 99991 + klassen_idx[a['klasse']]) < f
            for key in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw'):
                a[key] = a[key][keep]

    # ------------------------------------------------------------------ Instanzen bauen und schreiben
    ausgabe = os.path.join(basis, WELT, 'mittelschicht', feld)
    os.makedirs(ausgabe, exist_ok=True)
    for f in os.listdir(ausgabe):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    dateien = {}
    netz_inst = {}
    stat = {}
    nk = 0
    for a in aus:
        n = a['fi'].size
        if n == 0:
            continue
        z = bilinear(hoehe, a['fi'], a['fj']) - a['eingraben'] / 100.0
        x = (a['fj'] + wj0 - X0) * 100.0
        y = (a['fi'] + wi0 - Y0) * 100.0
        q = quaternionen(n_x[a['mi'], a['mj']], n_y[a['mi'], a['mj']], n_z[a['mi'], a['mj']], a['kippen'], a['yaw'])
        inst = np.zeros((n, 10), np.float32)
        inst[:, 0], inst[:, 1], inst[:, 2] = x, y, z * 100.0
        inst[:, 3:7] = q
        inst[:, 7] = inst[:, 8] = inst[:, 9] = a['massstab']
        pfade = netze_je_klasse[a['klasse']]
        for ni in np.unique(a['netz']):
            m = a['netz'] == ni
            p = pfade[ni]
            name = p.rsplit('/', 1)[-1]
            netz_inst.setdefault(name, []).append(inst[m])
            if name not in dateien:
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': a['klasse'], 'rolle': 'mittelschicht',
                                 'sichtweite': list(a['sichtweite']), 'schatten': a['klasse'] not in ('pilz', 'ast', 'grasbueschel', 'beere'),
                                 'kollision': a['kollision']}
            dateien[name]['anzahl'] += int(m.sum())
        stat[a['klasse']] = stat.get(a['klasse'], 0) + n
        if a['kollision']:
            nk += n
    gesamt = 0
    for name, teile in netz_inst.items():
        arr = np.concatenate(teile, axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]
    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': int(gesamt), 'dateien': dateien,
            'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'statistik': {'je_klasse': stat, 'kollision': int(nk), 'biome_anteil': {k: round(v, 3) for k, v in bio_anteil.items()},
                          'wald_anteil': round(float(wald[im_feld].mean()), 3), 'beschattung_mittel': round(float(beschattung[im_feld].mean()), 3),
                          'faktor': faktor, 'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA},
            'hinweise': hinweise, 'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet'}
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s: %d Instanzen (%d mit Kollision), %d Netze, %.1f s' % (feld, gesamt, nk, len(dateien), time.time() - t0))
    for h in hinweise:
        meld('  Hinweis:', h)

    if bild:
        try:
            from PIL import Image
        except Exception:
            meld('Pillow fehlt – kein Prüfbild')
            return plan
        fi0, fi1, fj0, fj1 = fb[0] - wi0, fb[1] - wi0, fb[2] - wj0, fb[3] - wj0
        hh = hoehe[fi0:fi1, fj0:fj1]
        g = np.clip((hh - hh.min()) / max(1e-3, float(hh.max() - hh.min())), 0, 1) * 110 + 70
        rgb = np.stack([g, g, g], axis=2)
        b = beschattung[fi0:fi1, fj0:fj1]
        rgb[..., 0] *= (1 - 0.5 * b)
        rgb[..., 2] *= (1 - 0.5 * b)
        rgb[wasser_m[fi0:fi1, fj0:fj1]] = (40, 80, 200)
        rgb[weg_m[fi0:fi1, fj0:fj1]] = (120, 80, 40)
        rgb[ort_m[fi0:fi1, fj0:fj1]] = (200, 40, 40)
        for a in aus:
            if a['fi'].size == 0:
                continue
            c = farben.get(a['klasse'], [255, 255, 255])
            pi = np.clip(np.round(a['fi']).astype(np.int32) - fi0, 0, fi1 - fi0 - 1)
            pj = np.clip(np.round(a['fj']).astype(np.int32) - fj0, 0, fj1 - fj0 - 1)
            rgb[pi, pj] = c
            if a['klasse'] in gross:
                rgb[np.minimum(pi + 1, fi1 - fi0 - 1), pj] = c
        os.makedirs(os.path.join(basis, 'docs', 'pruefung', 'mittelschicht'), exist_ok=True)
        Image.fromarray(rgb.astype(np.uint8)).save(os.path.join(basis, 'docs', 'pruefung', 'mittelschicht', feld + '.png'))
    return plan


def pruefe_netze(regeln, basis, thema):
    """Alle /Game/-Pfade der Regeldatei gegen das Inventar daten/netze.csv (Spalte pfad, Trenner ;) prüfen.
    Fehlendes Inventar → Hinweis, keine Prüfung. Unbekannte Pfade → Abbruch mit Liste (FORMAT.md §5)."""
    pfade = set()

    def sammle(o):
        if isinstance(o, str):
            if o.startswith('/Game/'):
                pfade.add(o)
        elif isinstance(o, dict):
            for v in o.values():
                sammle(v)
        elif isinstance(o, list):
            for v in o:
                sammle(v)
    sammle(regeln)
    pfade.discard(regeln.get('ft_ordner', ''))
    kandidaten = [os.path.join(basis, 'daten', 'netze.csv'),
                  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'netze.csv'),
                  os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'daten', 'netze.csv')]
    csv = next((p for p in kandidaten if os.path.isfile(p)), None)
    if csv is None:
        meld('Hinweis: daten/netze.csv nicht gefunden – %d Netzpfade der Regeln bleiben ungeprüft' % len(pfade))
        return
    inventar = set()
    with open(csv, encoding='utf-8', errors='replace') as f:
        kopf = f.readline().rstrip('\n').split(';')
        try:
            sp = kopf.index('pfad')
        except ValueError:
            sp = 0
        for zeile in f:
            t = zeile.rstrip('\n').split(';')
            if len(t) > sp:
                inventar.add(t[sp].strip())
    fehlt = sorted(p for p in pfade if p not in inventar)
    if fehlt:
        meld('FEHLER: %d Netzpfade der %s-Regeln fehlen im Inventar %s:' % (len(fehlt), thema, csv))
        for p in fehlt:
            meld('   ', p)
        raise SystemExit('Regeldatei enthält Netze, die nicht im Inventar stehen – bitte Einkaufsliste/Regeln abgleichen')
    meld('%d Netzpfade gegen %s geprüft: alle vorhanden' % (len(pfade), csv))


def main():
    ap = argparse.ArgumentParser(description='Eldarien Mittelschicht-Planer (0,3–3 m)')
    ap.add_argument('felder', nargs='+')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    a = ap.parse_args()
    rp = a.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mittelschicht_regeln.json')
    if not os.path.isfile(rp):
        raise SystemExit('Regeldatei fehlt: %s' % rp)
    regeln = json.load(open(rp, encoding='utf-8'))
    pruefe_netze(regeln, a.basis, 'Mittelschicht')
    if not NUMBA:
        meld('numba nicht verfügbar – reiner NumPy-Pfad (ausreichend)')
    for feld in a.felder:
        plane_feld(feld.strip().upper(), a.basis, regeln, a.faktor, a.bild)


if __name__ == '__main__':
    main()
