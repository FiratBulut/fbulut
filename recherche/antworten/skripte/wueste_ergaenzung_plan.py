#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wueste_ergaenzung_plan.py – Planer „Wüste/Canyon/Ödland – Ergänzung“ (Auftrag 11, Teil B9) für Eldarien
(UE 5.8.3, 1-m-Raster NX 9577 × NY 7057, World Partition).

*** UNGETESTET MIT ECHTDATEN *** – in der Cloud nur syntaxgeprüft (py_compile) und mit synthetischen Rastern
rauchgetestet (10.10.2026): D4 (Wüstenfeld, Ergänzungsmodus, Canyon-Schichtstufen + Rinne + 3 000 WU-Instanzen als belegt)
14 998 Instanzen / 164 Kollision / 6,5 s; E6 (Ödland voll, Kuppen/Senken/Rinnen) 49 966 / 345 / 4,2 s; zweiter Lauf
byte-identisch; 0 Instanzen auf Wasser/Weg/Ort. Korrekturen bitte als auftraege/verteilung-wueste-korrektur.md.

Was das Skript tut
------------------
Plant je Gitterfeld eine NEUE Foliage-Ebene „wueste_ergaenzung“ (FT_EL_WE_*) für die Biome wueste, canyon, oedland:
  Schicht 0 boden        Kiesel, Steine 0,2–0,6 m, Lehm-/Trockenbett-Platten (Trockenriss-Ersatz), Geröll-Platten,
                         dürre Zweige, Knochen-Ersatz (Rindenstücke), Trockenlaub
  Schicht 1 mittel       Trockengras-Büschel (3 Höhen), Dornsträucher, Trockenhang-Sträucher, Sukkulenten/Agaven-Ersatz,
                         Totholz liegend (klein ohne / Stämme mit Kollision), Stümpfe
  Schicht 2 baum         tote Bäume groß/klein, lebende Einzelbäume nur bei Restfeuchte (Rinnen/Senken/Ufer),
                         Krüppelkiefern an Terrassenkanten, Köcherbäume (außerhalb C3–E5)
  Schicht 5 wasserkante  Rohrkolben und grünes Gras an Oasen/Rinnen mit Restfeuchte
Schicht 3 fels liefert felsgruppen_plan.py (Teil C), Schicht 4 spuren liefert spuren_plan.py (Teil D); Vorschläge dafür
stehen als felsgruppen_overrides / spuren_overrides in der Regeldatei.

Geländeableitung (nur NumPy, Fenster Feld + 64 m): Hang und Normale aus Gradient, Rinnen = konkave Krümmung (positiver
Laplace der geglätteten Höhe, zwei Maßstäbe), Kuppen = konvex + lokal höchste Zelle, Senken = Höhe unter dem 24-m-Mittel,
Wandfuß/Schuttfächer = flache Zellen unter Wänden > 35° (bis 30 m, Stein-Größe nimmt hangabwärts ab), Terrassenkanten =
flache Zellen mit Abbruch ≥ 3 m darunter, Restfeuchte aus Wassernähe + Senke + Rinne + Lagen (Lehm/Schlamm/Moos/Wiese).

Wüstenfelder C3 C4 D3 D4 D5 E3 E4 E5 (eigener Namaqualand-Planer, FT_EL_WU_*): NUR ERGÄNZEN. Klassen mit
wuestenfeld_faktor 0 (Namaqualand-Sträucher/Sukkulenten/Köcherbäume) werden dort nicht gestreut, Namaqualand-Netze durch
netze_wuestenfeld ersetzt, Budget 15 000 Instanzen, KEIN „entfernen“ im plan.json. Die vorhandene Wüsten-Ebene wird – wenn
auffindbar – als belegt geladen (Abstand). Ihr Pfad ist in der Cloud unbekannt: --wueste_ebene PFAD.

Aufruf
------
  python -I scripts/wueste_ergaenzung/wueste_ergaenzung_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD]
         [--regeln PFAD] [--netze PFAD] [--wueste_ebene PFAD]
  --basis         production-Wurzel (Default "."): darunter export/unreal/welt/, daten/netze.csv, docs/
  --regeln        Regeldatei (Default: wueste_ergaenzung_regeln.json neben dem Skript)
  --netze         Inventar netze.csv (Default: <basis>/daten/netze.csv, sonst vorlagen/daten/netze.csv relativ zum Skript)
  --wueste_ebene  Ordner der vorhandenen Wüsten-Ebene (<PFAD>/<Feld>/plan.json + *.f32 oder <PFAD>/*.f32)
  --faktor        Dichtefaktor auf alle Klassen
  --bild          Draufsicht docs/pruefung/wueste_ergaenzung/<Feld>.png (1 px = 1 m)

Liest   export/unreal/welt/hoehe.f32 (np.memmap, nur Fenster), lage_*.r8 (optional), karte_wasser/weg/ort.r8 (optional),
        eigner.r8 + welt.json (Biom je Zelle; Fallback je Feld aus Regeln, sonst aue → nichts), vorhandene Ebenen
        bestand/ witcher/ mittelschicht/ felsgruppen/ spuren/ ufer/ wueste/ (<Feld>/plan.json + f32) und instanzen/instanzen.json.
Schreibt export/unreal/welt/wueste_ergaenzung/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm; qx,qy,qz,qw; sx,sy,sz)
        + plan.json (FORMAT.md §3, plus "ebene", "modus"; in Wüstenfeldern ohne "entfernen").

Determinismus: alle Zufallszahlen aus Hash(Weltraster-Koordinate, Seed, Kanal) → Nachbarfelder nahtlos, Wiederholung identisch.
Laufzeit-Ziel ≤ 60 s je Feld (reine NumPy-Vektoroperationen; numba wird nicht benötigt, nur gemeldet).

Quellen: vorlagen/FORMAT.md §1–§5; antworten/assets-taxonomie.md (Lücken wueste/canyon/oedland); antworten/bildkritik-
witcher-messlatte.md (NORD3_D3: Blöcke nach Erosion, 3 Größenstufen, Eingraben 30 %); antworten/verteilung-wueste.md
(Referenzanalyse Velen/Toussaint/Monument Valley/Wadi Rum/Steppe, Herleitung der Dichten).
"""
import argparse
import csv
import glob
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
X0, Y0 = 4730.5, 4060.5  # X_cm = (j - X0) * 100, Y_cm = (i - Y0) * 100
WELT = os.path.join('export', 'unreal', 'welt')
BAUM_WORTE = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel', 'palme',
              'hainbuche', 'pine', 'beech', 'oak', 'poplar', 'quiver', 'hornbeam', 'willow', 'fir')


_ASCII = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss', '→': '->', '–': '-', '—': '-',
                        '≤': '<=', '≥': '>=', '×': 'x', '„': '"', '“': '"', '”': '"', '…': '...', '°': 'deg', '²': '2'})


def ascii_(t):
    return str(t).translate(_ASCII).encode('ascii', 'replace').decode('ascii')


def meld(*a):
    """Konsole nur ASCII (Windows-Logs werden mit cp1252 weiterverarbeitet, Korrektur Runde 1)."""
    print('[wueste_ergaenzung]', *(ascii_(x) for x in a), flush=True)


# ----------------------------------------------------------------------------- Raster-Helfer
def feld_fenster(feld, rand):
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX)  # J-Spalte: 9072 … 9577 (nur 505 m) – geklippt
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY)
    wi0, wi1 = max(0, i0 - rand), min(NY, i1 + rand)
    wj0, wj1 = max(0, j0 - rand), min(NX, j1 + rand)
    return (i0, i1, j0, j1), (wi0, wi1, wj0, wj1)


def lade_raster(pfad, dtype, win, pflicht=False):
    """Fensterausschnitt eines NY×NX-Rasters per memmap (nur das Fenster wird gelesen)."""
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            raise SystemExit('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        meld('WARNUNG: %s hat %d Werte, erwartet %d (NY %d × NX %d) – ignoriert' % (pfad, n, NX * NY, NY, NX))
        if pflicht:
            raise SystemExit('Pflichtdatei hat falsche Größe: %s' % pfad)
        return None
    mm = np.memmap(pfad, dtype=dtype, mode='r', shape=(NY, NX))
    a = np.array(mm[wi0:wi1, wj0:wj1])
    del mm
    return a


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
    """3 Box-Durchläufe ≈ Gauß (sigma in Zellen)."""
    if sigma <= 0:
        return a.astype(np.float32)
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
    """Binäre Dilatation ≈ Kreisscheibe (Radius r Zellen)."""
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


def fenster_max(a, r, fn):
    """Max- oder Min-Filter über Quadrat (2r+1)² in Doppelschritten (log r Operationen je Achse)."""
    out = a
    fill = -np.inf if fn is np.maximum else np.inf
    for axis in (0, 1):
        res = out
        s = 1
        reach = 0
        while reach < r:
            step = min(s, r - reach)
            res = fn(res, verschiebe(res, step if axis == 0 else 0, step if axis == 1 else 0, fill))
            res = fn(res, verschiebe(res, -step if axis == 0 else 0, -step if axis == 1 else 0, fill))
            reach += step
            s *= 2
        out = res
    return out


def distanz(mask, max_m=64.0):
    """Euklidische Distanz (m) zur nächsten True-Zelle per Jump-Flooding; > max_m → 2·max_m."""
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
    """Deterministische Zufallszahl [0,1) je (Weltzeile, Weltspalte, Seed, Kanal)."""
    i = np.asarray(i).astype(np.int64)
    j = np.asarray(j).astype(np.int64)
    h = (i * 73856093) ^ (j * 19349663) ^ (int(seed) * 83492791 + int(kanal) * 2654435761)
    h = (h & 0xFFFFFFFF).astype(np.uint32)
    with np.errstate(over='ignore'):
        h ^= h >> np.uint32(16)
        h *= np.uint32(0x7FEB352D)
        h ^= h >> np.uint32(15)
        h *= np.uint32(0x846CA68B)
        h ^= h >> np.uint32(16)
    return (h & np.uint32(0xFFFFFF)).astype(np.float32) / np.float32(16777216.0)


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


def quaternionen(nx, ny, nz, kippen, yaw):
    """Z-Achse um Anteil `kippen` auf die Geländenormale kippen, davor Zufalls-Yaw → (n,4) x,y,z,w."""
    n = len(nx)
    tz = (1 - kippen) + kippen * nz
    tx = kippen * nx
    ty = kippen * ny
    l = np.sqrt(tx * tx + ty * ty + tz * tz) + 1e-9
    tx, ty, tz = tx / l, ty / l, tz / l
    qt = np.stack([-ty, tx, np.zeros(n, np.float32), 1 + tz], axis=1)
    qt /= (np.linalg.norm(qt, axis=1, keepdims=True) + 1e-9)
    qy = np.stack([np.zeros(n, np.float32), np.zeros(n, np.float32), np.sin(yaw / 2), np.cos(yaw / 2)], axis=1)
    q = quat_mul(qt, qy)
    return (q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-9)).astype(np.float32)


# ----------------------------------------------------------------------------- Inventar
def lade_inventar(basis, netze_arg):
    """netze.csv (Trenner ;) → {pfad: hoehe_m}. Fehlt die Datei → None (Hinweis, keine Prüfung)."""
    kandidaten = []
    if netze_arg:
        kandidaten.append(netze_arg)
    kandidaten.append(os.path.join(basis, 'daten', 'netze.csv'))
    hier = os.path.dirname(os.path.abspath(__file__))
    kandidaten.append(os.path.normpath(os.path.join(hier, '..', '..', 'vorlagen', 'daten', 'netze.csv')))
    kandidaten.append(os.path.normpath(os.path.join(hier, '..', 'daten', 'netze.csv')))
    for p in kandidaten:
        if os.path.isfile(p):
            inv = {}
            with open(p, encoding='utf-8') as f:
                for r in csv.DictReader(f, delimiter=';'):
                    try:
                        inv[r['pfad']] = {'hoehe_m': float(r.get('groesse_z_m') or 0), 'nanite': r.get('nanite') == '1'}
                    except Exception:
                        continue
            meld('Inventar: %d Netze aus %s' % (len(inv), p))
            return inv
    meld('Hinweis: netze.csv nicht gefunden (%s) – Netzpfade werden NICHT geprüft, Netzhöhen aus Regeln geschätzt' % ', '.join(kandidaten[:2]))
    return None


def pruefe_paletten(regeln, inv):
    """Entfernt Netze, die nicht im Inventar stehen; meldet sie. Klassen ohne Netze werden abgeschaltet."""
    if inv is None:
        return
    fehlend = []
    for kname, kl in regeln['klassen'].items():
        for key in ('netze', 'netze_wuestenfeld'):
            lst = kl.get(key)
            if not lst:
                continue
            ok = [p for p in lst if p in inv]
            fehlend += [(kname, p) for p in lst if p not in inv]
            kl[key] = ok
        if not kl['netze']:
            meld('WARNUNG: Klasse %s hat kein gültiges Netz – abgeschaltet' % kname)
    for kname, p in fehlend:
        meld('WARNUNG: Netz nicht im Inventar (Klasse %s): %s' % (kname, p))
    if not fehlend:
        meld('Netzpaletten geprüft: alle Pfade im Inventar')


def netz_hoehe(inv, pfad, default=0.3):
    if inv and pfad in inv and inv[pfad]['hoehe_m'] > 0:
        return inv[pfad]['hoehe_m']
    return default


# ----------------------------------------------------------------------------- Weltdaten
def lade_biome(basis, win, regeln, feld, hinweise):
    namen = list(regeln['biome'])
    fb = regeln.get('feld_biom_fallback', {}).get(feld, 'aue')
    if fb not in namen:
        fb = 'aue'
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    if eig is None or not os.path.isfile(wj):
        hinweise.append('eigner.r8/welt.json fehlen – Biom je Zelle = Fallback %r' % fb)
        return np.full((H, W), namen.index(fb), np.int16), 'fallback'
    try:
        welt = json.load(open(wj, encoding='utf-8'))
    except Exception as e:
        hinweise.append('welt.json unlesbar (%s) – Fallback %r' % (e, fb))
        return np.full((H, W), namen.index(fb), np.int16), 'fallback'
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
    tabelle[0] = namen.index('aue')  # 0 = Weltgelände → aue
    return tabelle[eig], 'eigner.r8'


def lade_f32_ordner(ordner, win, plan_name='plan.json'):
    """Alle Instanzen eines Ebenen-Ordners (plan.json + *.f32 oder nur *.f32) → Liste (fi, fj, sz, ist_baum)."""
    out = []
    if not os.path.isdir(ordner):
        return out
    pj = os.path.join(ordner, plan_name)
    rollen = {}
    if os.path.isfile(pj):
        try:
            plan = json.load(open(pj, encoding='utf-8'))
            for name, info in plan.get('dateien', {}).items():
                rollen[name] = (str(info.get('rolle', '')) + ' ' + str(info.get('gruppe', ''))).lower()
        except Exception:
            pass
    for f in sorted(glob.glob(os.path.join(ordner, '*.f32'))):
        name = os.path.basename(f)[:-4]
        try:
            a = np.fromfile(f, dtype='<f4')
        except Exception:
            continue
        if a.size == 0 or a.size % 10:
            continue
        a = a.reshape(-1, 10)
        fj = a[:, 0] / 100.0 + X0 - win[2]
        fi = a[:, 1] / 100.0 + Y0 - win[0]
        m = (fi >= 0) & (fi < win[1] - win[0]) & (fj >= 0) & (fj < win[3] - win[2])
        if not m.any():
            continue
        txt = (rollen.get(name, '') + ' ' + name).lower()
        ist_baum = any(w in txt for w in BAUM_WORTE) and 'dead' not in txt and 'tot' not in txt and 'stump' not in txt and 'log' not in txt and 'branch' not in txt and 'leaf' not in txt
        out.append(np.stack([fi[m], fj[m], a[m, 9], np.full(int(m.sum()), 1.0 if ist_baum else 0.0, np.float32)], axis=1))
    return out


def lade_fremd(basis, feld, win, regeln, wueste_ebene, hinweise):
    """Vorhandene Ebenen (Feld + Nachbarn für Bäume) als belegte Positionen."""
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    teile, quellen = [], []
    for ebene in regeln.get('vorhandene_ebenen', []):
        if ebene == 'wueste':
            continue
        for ds in (-1, 0, 1):
            for dr in (-1, 0, 1):
                ss, rr = s + ds, r + dr
                if not (0 <= ss <= 9 and 1 <= rr <= 7):
                    continue
                nf = chr(ord('A') + ss) + str(rr)
                if ebene == 'ufer':
                    ordner = os.path.join(basis, WELT, 'ufer', 'foliage_' + nf)
                else:
                    ordner = os.path.join(basis, WELT, ebene, nf)
                t = lade_f32_ordner(ordner, win)
                if t:
                    teile += t
                    quellen.append('%s/%s' % (ebene, nf))
    # Wüsten-Ebene (Pfad unbekannt)
    wf = feld in regeln.get('wuesten_felder', [])
    if wf:
        kand = []
        if wueste_ebene:
            kand += [os.path.join(wueste_ebene, feld), wueste_ebene]
        kand.append(os.path.join(basis, regeln['wuesten_feld'].get('ebene_pfad_default', 'export/unreal/welt/wueste'), feld))
        gefunden = False
        for k in kand:
            t = lade_f32_ordner(k, win)
            if t:
                teile += t
                quellen.append('wueste:' + k)
                gefunden = True
                break
        if not gefunden:
            hinweise.append('Wüstenfeld %s: vorhandene Wüsten-Ebene (FT_EL_WU_*) nicht gefunden (%s) – Planung ohne Abstandsprüfung zur WU-Ebene; Pfad mit --wueste_ebene angeben' % (feld, ' | '.join(kand)))
    # Houdini-Bestand
    ij = os.path.join(basis, WELT, 'instanzen', 'instanzen.json')
    if os.path.isfile(ij):
        try:
            inst = json.load(open(ij, encoding='utf-8'))
            n_alt = len(teile)
            for e in inst.get('verzeichnis', []):
                f = e.get('datei') or (str(e.get('name', '')) + '.f32')
                f = os.path.join(basis, WELT, 'instanzen', f)
                if not os.path.isfile(f):
                    continue
                a = np.fromfile(f, dtype='<f4')
                if a.size == 0 or a.size % 10:
                    continue
                a = a.reshape(-1, 10)
                fj = a[:, 0] / 100.0 + X0 - win[2]
                fi = a[:, 1] / 100.0 + Y0 - win[0]
                m = (fi >= 0) & (fi < win[1] - win[0]) & (fj >= 0) & (fj < win[3] - win[2])
                if not m.any():
                    continue
                txt = (str(e.get('klasse', '')) + ' ' + str(e.get('name', ''))).lower()
                ist_baum = any(w in txt for w in BAUM_WORTE)
                teile.append(np.stack([fi[m], fj[m], a[m, 9], np.full(int(m.sum()), 1.0 if ist_baum else 0.0, np.float32)], axis=1))
            if len(teile) > n_alt:
                quellen.append('instanzen/instanzen.json')
        except Exception as e:
            hinweise.append('instanzen.json nicht auswertbar (%s)' % e)
    fremd = np.concatenate(teile, axis=0) if teile else np.zeros((0, 4), np.float32)
    return fremd, quellen


# ----------------------------------------------------------------------------- Planung je Feld
def plane_feld(feld, basis, regeln, inv, faktor, bild, wueste_ebene):
    t0 = time.time()
    feld = feld.strip().upper()
    rand = int(regeln.get('fenster_rand_m', 64))
    fb, win = feld_fenster(feld, rand)
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    if H <= 0 or W <= 0 or fb[1] <= fb[0] or fb[3] <= fb[2]:
        meld('Feld %s liegt außerhalb des Rasters' % feld)
        return None
    hinweise = []
    G = regeln['gelaende']
    A = regeln['abstand_m']
    wf = feld in regeln.get('wuesten_felder', [])
    modus = 'ergaenzung' if wf else 'voll'

    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True).astype(np.float32)
    ii, jj = np.indices((H, W), dtype=np.int32)
    gi, gj = ii + wi0, jj + wj0
    im_feld = (gi >= fb[0]) & (gi < fb[1]) & (gj >= fb[2]) & (gj < fb[3])

    # --- Gelände: Hang, Normale
    hs = gauss_blur(hoehe, G.get('hang_sigma_m', 1.5))
    dzdy, dzdx = np.gradient(hs)
    hang = np.degrees(np.arctan(np.sqrt(dzdx ** 2 + dzdy ** 2))).astype(np.float32)
    nl = np.sqrt(dzdx ** 2 + dzdy ** 2 + 1.0)
    n_x, n_y, n_z = (-dzdx / nl).astype(np.float32), (-dzdy / nl).astype(np.float32), (1.0 / nl).astype(np.float32)
    aspekt = np.arctan2(-dzdy, -dzdx).astype(np.float32)  # Richtung hangabwärts (X, Y)

    # --- Rinnen (konkav), Kuppen (konvex), Senken
    def laplace(a):
        p = np.pad(a, 1, mode='edge')
        return (p[2:, 1:-1] + p[:-2, 1:-1] + p[1:-1, 2:] + p[1:-1, :-2] - 4 * a).astype(np.float32)
    R = G['rinne']
    lk = laplace(gauss_blur(hoehe, R['sigma_klein_m']))
    lg = laplace(gauss_blur(hoehe, R['sigma_gross_m']))
    r_k = np.clip((lk - R['konkav_ab']) / max(1e-6, R['konkav_voll'] - R['konkav_ab']), 0, 1)
    sk = R['sigma_klein_m'] / R['sigma_gross_m']
    r_g = np.clip((lg - R['konkav_ab'] * sk) / max(1e-6, (R['konkav_voll'] - R['konkav_ab']) * sk), 0, 1)
    rinne = np.maximum(r_k, R['gewicht_gross'] * r_g).astype(np.float32)
    Kp = G['kuppe']
    S = G['senke']
    h_mittel = gauss_blur(hoehe, S['sigma_m'])  # 24-m-Mittel: Senke darunter, Kuppe darüber
    hmax_k = fenster_max(hoehe, int(Kp['umkreis_m']), np.maximum)
    prominenz = hoehe - gauss_blur(hoehe, Kp['sigma_m']) if Kp['sigma_m'] != S['sigma_m'] else hoehe - h_mittel
    kuppe = (np.clip((prominenz - Kp['prominenz_ab_m']) / max(1e-6, Kp['prominenz_voll_m'] - Kp['prominenz_ab_m']), 0, 1)
             * (hoehe >= hmax_k - Kp['toleranz_m'])).astype(np.float32)
    senke = np.clip((h_mittel - hoehe - S['tiefe_ab_m']) / max(1e-6, S['tiefe_voll_m'] - S['tiefe_ab_m']), 0, 1).astype(np.float32)

    # --- Wandfuß / Schuttfächer / Terrassenkanten
    Wd = G['wand']
    steil = hang > Wd['wand_ab_grad']
    d_steil = distanz(steil, max_m=float(Wd['schutt_reichweite_m']))
    hmax_w = fenster_max(hoehe, int(Wd['schutt_reichweite_m']), np.maximum)
    wand_oben = (hmax_w - hoehe) >= Wd['wandfuss_hoehe_min_m']
    wandfuss = (np.clip(1 - d_steil / float(Wd['schutt_reichweite_m']), 0, 1) * wand_oben * (~steil)).astype(np.float32)
    hmin_t = fenster_max(hoehe, int(Wd['terrasse_umkreis_m']), np.minimum)
    terrasse = ((hang < Wd['terrasse_hang_max_grad']) & ((hoehe - hmin_t) >= Wd['terrasse_abbruch_min_m'])).astype(np.float32)

    # --- Karten
    def r8(name):
        return lade_raster(os.path.join(basis, WELT, name), np.uint8, win)
    wasser = r8('karte_wasser.r8')
    weg = r8('karte_weg.r8')
    ort = r8('karte_ort.r8')
    for nm, a in (('karte_wasser.r8', wasser), ('karte_weg.r8', weg), ('karte_ort.r8', ort)):
        if a is None:
            hinweise.append('%s fehlt – Annahme: keine Fläche dieser Art' % nm)
    wasser_m = (wasser > 0) if wasser is not None else np.zeros((H, W), bool)
    weg_m = (weg > 0) if weg is not None else np.zeros((H, W), bool)
    ort_m = (ort > 0) if ort is not None else np.zeros((H, W), bool)
    d_wasser = distanz(wasser_m, max_m=64.0)
    d_weg = distanz(weg_m, max_m=96.0)
    nah_wasser = dilate(wasser_m, A['wasser'])
    nah_weg_klein = dilate(weg_m, A['weg_klein'])
    nah_weg_gross = dilate(weg_m, A['weg_gross'])
    nah_ort = dilate(ort_m, A['ort'])
    rinne = np.where(wasser_m, 0, rinne).astype(np.float32)

    # --- Lagen
    lagen = {}
    for ln in regeln.get('lagen', []):
        a = r8('lage_%s.r8' % ln)
        if a is not None:
            lagen[ln] = a.astype(np.float32) / 255.0
    if not lagen:
        hinweise.append('keine lage_*.r8 gefunden – Dichten aus dichte_ohne_lagen_je_m2')
    else:
        hinweise.append('Lagen geladen: ' + ', '.join(sorted(lagen)))

    # --- Restfeuchte
    RF = G['restfeuchte']
    restfeuchte = np.clip(1 - d_wasser / RF['wasser_radius_m'], 0, 1) + RF['senke_gewicht'] * senke + RF['rinne_gewicht'] * rinne
    for ln, w in RF['lagen'].items():
        if ln in lagen:
            restfeuchte += w * lagen[ln]
    restfeuchte = np.clip(restfeuchte, 0, 1).astype(np.float32)
    Sn = G['schnee']
    f_schnee = (1 - (1 - Sn['faktor_bei_voll']) * lagen[Sn['lage']]) if Sn['lage'] in lagen else np.ones((H, W), np.float32)

    # --- Biome (weicher Saum)
    bio, bio_quelle = lade_biome(basis, win, regeln, feld, hinweise)
    namen = list(regeln['biome'])
    biom_gew = {}
    saum = int(regeln.get('biom_saum_m', 6))
    for b, f in regeln['biom_faktor'].items():
        if f <= 0 or b not in namen:
            continue
        ind = (bio == namen.index(b))
        if ind.any():
            biom_gew[b] = box_blur(ind.astype(np.float32), saum) if saum > 0 else ind.astype(np.float32)
    bio_anteil = {namen[k]: round(float((bio[im_feld] == k).mean()), 3) for k in np.unique(bio[im_feld])}
    biome_fenster = {namen[k]: round(float((bio == k).mean()), 4) for k in np.unique(bio)}
    biome_eigen = [b for b, f in regeln['biom_faktor'].items() if f > 0 and b in namen]
    eigen_m = np.isin(bio, [namen.index(b) for b in biome_eigen])
    zellen_zustaendig = int(eigen_m[im_feld].sum())
    anteil_eigen_fenster = float(eigen_m.mean())
    min_anteil = float(regeln.get('min_anteil_eigen_fenster', 0.02))
    if anteil_eigen_fenster < min_anteil:
        hinweise.append('Feld %s: Anteil der Biome %s im Fenster %.1f %% < %.0f %% (Biom-Quelle %s: %s) - nichts geplant'
                        % (feld, '/'.join(biome_eigen), anteil_eigen_fenster * 100, min_anteil * 100, bio_quelle, bio_anteil))
        biom_gew = {}

    # --- Fremde Ebenen
    fremd, quellen = lade_fremd(basis, feld, win, regeln, wueste_ebene, hinweise)
    belegt_klein = np.zeros((H, W), bool)
    belegt_gross = np.zeros((H, W), bool)
    fremd_baum = np.zeros((H, W), bool)
    if len(fremd):
        fi_ = np.clip(np.round(fremd[:, 0]).astype(np.int32), 0, H - 1)
        fj_ = np.clip(np.round(fremd[:, 1]).astype(np.int32), 0, W - 1)
        m = np.zeros((H, W), bool)
        m[fi_, fj_] = True
        belegt_klein = dilate(m, A['fremd_klein'])
        belegt_gross = dilate(m, A['fremd_gross'])
        b = fremd[:, 3] > 0.5
        if b.any():
            mb = np.zeros((H, W), bool)
            mb[fi_[b], fj_[b]] = True
            fremd_baum = dilate(mb, A['fremd_baum'])
        hinweise.append('%d vorhandene Instanzen als belegt (%s)' % (len(fremd), ', '.join(quellen[:8]) + (' …' if len(quellen) > 8 else '')))
    else:
        hinweise.append('keine vorhandenen Ebenen im Fenster gefunden (bestand/witcher/mittelschicht/felsgruppen/spuren/ufer/wueste/instanzen)')

    # --- Streuung
    seed = int(regeln['seed'])
    klassen = regeln['klassen']
    knamen = [k for k in klassen if klassen[k]['netze']]
    kidx = {k: n for n, k in enumerate(knamen)}
    reihenfolge = regeln.get('planungs_reihenfolge', ['2_baum', '1_mittel', '0_boden', '5_wasserkante'])
    fels_kl = set(G.get('fels_klassen', []))
    hang_alle = float(G.get('hang_max_grad_alle', 40))
    wf_cfg = regeln['wuesten_feld']
    feld_faktor = faktor * (wf_cfg.get('global_faktor', 1.0) if wf else 1.0)
    aus = []
    eigen_baum = np.zeros((H, W), bool)
    totbaum_m = np.zeros((H, W), bool)
    stat_roh = {}
    for schicht in (reihenfolge if biom_gew else []):
        for kname in knamen:
            kl = klassen[kname]
            if kl['schicht'] != schicht:
                continue
            wff = kl.get('wuestenfeld_faktor', 0.0)
            if wf and wff <= 0:
                continue
            netzl = kl['netze']
            if wf and kl.get('netze_wuestenfeld'):
                netzl = kl['netze_wuestenfeld']
            # Biom-Gewicht
            lam = np.zeros((H, W), np.float32)
            for b, g in biom_gew.items():
                f = float(kl['biome'].get(b, 0.0))
                if f > 0:
                    lam += f * g
            if not lam.any():
                continue
            # Dichte aus Lagen
            if lagen:
                d = np.zeros((H, W), np.float32)
                for ln, w in kl['lage_dichte_je_m2'].items():
                    if ln in lagen:
                        d += w * lagen[ln]
            else:
                d = np.full((H, W), kl['dichte_ohne_lagen_je_m2'], np.float32)
            lam *= d
            # Hang
            hv, hn = kl['hang_voll_bis_grad'], kl['hang_null_ab_grad']
            if kname not in fels_kl:
                hn = min(hn, hang_alle)
            lam *= np.clip((hn - hang) / max(1.0, hn - hv), 0, 1)
            if kl['hoehe_max_m'] < 9000:
                lam = np.where(hoehe > kl['hoehe_max_m'], 0, lam)
            # Geländeformen
            for feldname, arr in (('rinne', rinne), ('kuppe', kuppe), ('senke', senke), ('wandfuss', wandfuss), ('terrasse', terrasse)):
                f = float(kl.get(feldname, 1.0))
                if f != 1.0:
                    lam *= 1 + (f - 1) * arr
            r0, r1 = kl['restfeuchte']
            if r0 != 1.0 or r1 != 1.0:
                lam *= r0 + (r1 - r0) * restfeuchte
            if kl.get('nur_restfeuchte_ab', 0) > 0:
                lam = np.where(restfeuchte >= kl['nur_restfeuchte_ab'], lam, 0)
            if kl.get('wasser_band_m'):
                a0, a1 = kl['wasser_band_m']
                lam = np.where((d_wasser >= a0) & (d_wasser <= a1), lam, 0)
            if kl.get('weg_band_m'):
                a0, a1, f = kl['weg_band_m']
                lam = np.where((d_weg >= a0) & (d_weg <= a1), lam * f, lam)
            if kl.get('nahe_totbaum') and totbaum_m.any():
                rad, f = kl['nahe_totbaum']
                lam = np.where(dilate(totbaum_m, rad), lam * f, lam)
            lam *= f_schnee * feld_faktor * (wff if wf else 1.0)
            # Freiflächen
            gross = bool(kl.get('gross', False))
            frei = ~nah_wasser & ~nah_ort & ~(nah_weg_gross if gross else nah_weg_klein)
            frei &= ~(belegt_gross if gross else belegt_klein)
            if schicht == '2_baum':
                frei &= ~fremd_baum
                if eigen_baum.any():
                    frei &= ~dilate(eigen_baum, A['eigen_baum_zu_baum'])
            elif eigen_baum.any():
                frei &= ~dilate(eigen_baum, 0.9)
            lam = np.where(frei, lam, 0).astype(np.float32)
            if not (lam > 0).any():
                continue
            kanal = 1000 + kidx[kname] * 20
            gmin, gmax = kl['gruppe']
            gmit = 0.5 * (gmin + gmax)
            lamc = lam / gmit
            idx = np.flatnonzero(lamc > 0)
            ci, cj = ii.ravel()[idx], jj.ravel()[idx]
            u = hash01(ci + wi0, cj + wj0, seed, kanal)
            keep = u < lamc.ravel()[idx]
            ci, cj = ci[keep], cj[keep]
            if ci.size == 0:
                continue
            if gmax <= 1:
                fi = ci + hash01(ci + wi0, cj + wj0, seed, kanal + 1) - 0.5
                fj = cj + hash01(ci + wi0, cj + wj0, seed, kanal + 2) - 0.5
                mi, mj = ci, cj
                d_mitte = np.zeros(ci.size, np.float32)
            else:
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
                d_mitte = rad[ok].astype(np.float32)
            ok = (fi + wi0 >= fb[0]) & (fi + wi0 < fb[1]) & (fj + wj0 >= fb[2]) & (fj + wj0 < fb[3])
            fi, fj, mi, mj, d_mitte = fi[ok], fj[ok], mi[ok], mj[ok], d_mitte[ok]
            if fi.size == 0:
                continue
            gmi, gmj = mi + wi0, mj + wj0
            sub_i = np.round(fi * 7).astype(np.int64)
            sub_j = np.round(fj * 7).astype(np.int64)
            hv_ = (hash01(gmi, gmj, seed, kanal + 5) + 0.37 * hash01(sub_i, sub_j, seed, kanal + 6)) % 1.0
            nidx = np.minimum((hv_ * len(netzl)).astype(np.int32), len(netzl) - 1)
            ms = kl['massstab'][0] + (kl['massstab'][1] - kl['massstab'][0]) * hash01(sub_i, sub_j, seed, kanal + 7)
            if kl.get('massstab_schutt_abnahme', 0) > 0:
                ms = ms * (1 - kl['massstab_schutt_abnahme'] * np.clip(d_steil[mi, mj] / float(Wd['schutt_reichweite_m']), 0, 1) * (wandfuss[mi, mj] > 0))
            yaw = hash01(sub_i, sub_j, seed, kanal + 8) * 2 * math.pi
            ausr = kl.get('ausrichtung', 'zufall')
            if ausr in ('hangabwaerts', 'quer_hang'):
                basisw = aspekt[mi, mj] + (math.pi / 2 if ausr == 'quer_hang' else 0.0)
                yaw = basisw + (hash01(sub_i, sub_j, seed, kanal + 9) - 0.5) * math.radians(50) + np.where(hash01(gmi, gmj, seed, kanal + 8) < 0.5, 0, math.pi)
                yaw = np.where(hang[mi, mj] < 3, hash01(sub_i, sub_j, seed, kanal + 8) * 2 * math.pi, yaw)
            # Eingraben (cm): Anteil der Netzhöhe × Maßstab oder fester Wert
            if kl.get('eingraben_anteil') is not None:
                hoehen = np.array([netz_hoehe(inv, p) for p in netzl], np.float32)[nidx]
                eing = kl['eingraben_anteil'] * hoehen * ms * 100.0
            else:
                eing = np.full(fi.size, float(kl.get('eingraben_cm') or 0), np.float32)
            aus.append(dict(fi=fi.astype(np.float32), fj=fj.astype(np.float32), mi=mi, mj=mj, klasse=kname, schicht=schicht,
                            netz=nidx, netzl=netzl, massstab=ms.astype(np.float32), yaw=yaw.astype(np.float32), eing=eing.astype(np.float32),
                            kippen=float(kl['kippen']), kollision=bool(kl['kollision']), sichtweite=list(kl['sichtweite']),
                            schatten=bool(kl.get('schatten', True))))
            stat_roh[kname] = int(fi.size)
            if schicht == '2_baum':
                eigen_baum[mi, mj] = True
                if kname.startswith('totbaum'):
                    totbaum_m[mi, mj] = True

    # --- Budget
    B = regeln['budget']
    ziel = B['wuestenfeld_instanzen'] if wf else B['ziel_instanzen_je_feld']
    koll_max = B['wuestenfeld_kollision'] if wf else B['kollision_je_feld']
    ausduenn = {}
    koll = sum(a['fi'].size for a in aus if a['kollision'])
    if koll > koll_max:
        f = koll_max / float(koll)
        for a in aus:
            if a['kollision']:
                ausduenn[a['klasse']] = min(ausduenn.get(a['klasse'], 1.0), f)
        hinweise.append('Kollisionsbudget: %d → %d (Faktor %.2f auf Kollisionsklassen)' % (koll, koll_max, f))
    gesamt = sum(a['fi'].size for a in aus)
    if gesamt > ziel:
        ueber = gesamt - ziel
        reihe = [k for k in B['ausduenn_reihenfolge'] if k in stat_roh]
        pool, summe = [], 0
        for k in reihe:
            pool.append(k)
            summe += stat_roh[k]
            if summe * 0.6 >= ueber:
                break
        f = max(0.0, 1.0 - ueber / float(max(1, summe)))
        for k in pool:
            ausduenn[k] = min(ausduenn.get(k, 1.0), f)
        hinweise.append('Instanzbudget: %d → Ziel %d (%s), Ausdünnung %s' % (gesamt, ziel, modus, {k: round(v, 2) for k, v in ausduenn.items()}))
    for a in aus:
        f = ausduenn.get(a['klasse'], 1.0)
        if f < 1.0:
            keep = hash01(np.round(a['fi'] * 7).astype(np.int64) + wi0 * 7, np.round(a['fj'] * 7).astype(np.int64) + wj0 * 7, seed, 99991 + kidx[a['klasse']]) < f
            for key in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw', 'eing'):
                a[key] = a[key][keep]

    # --- Instanzen bauen und schreiben
    ausgabe = os.path.join(basis, regeln['ausgabe']['ordner'], feld)
    os.makedirs(ausgabe, exist_ok=True)
    for f in os.listdir(ausgabe):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    dateien, netz_inst, stat, stat_schicht = {}, {}, {}, {}
    nk = 0
    for a in aus:
        n = a['fi'].size
        if n == 0:
            continue
        z = bilinear(hoehe, a['fi'], a['fj']) - a['eing'] / 100.0
        x = (a['fj'] + wj0 - X0) * 100.0
        y = (a['fi'] + wi0 - Y0) * 100.0
        q = quaternionen(n_x[a['mi'], a['mj']], n_y[a['mi'], a['mj']], n_z[a['mi'], a['mj']], a['kippen'], a['yaw'])
        inst = np.zeros((n, 10), np.float32)
        inst[:, 0], inst[:, 1], inst[:, 2] = x, y, z * 100.0
        inst[:, 3:7] = q
        inst[:, 7] = inst[:, 8] = inst[:, 9] = a['massstab']
        for ni in np.unique(a['netz']):
            m = a['netz'] == ni
            p = a['netzl'][ni]
            name = p.rsplit('/', 1)[-1]
            netz_inst.setdefault(name, []).append(inst[m])
            if name not in dateien:
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': a['klasse'], 'rolle': a['schicht'],
                                 'sichtweite': list(a['sichtweite']), 'schatten': a['schatten'], 'kollision': a['kollision']}
            dateien[name]['anzahl'] += int(m.sum())
        stat[a['klasse']] = stat.get(a['klasse'], 0) + n
        stat_schicht[a['schicht']] = stat_schicht.get(a['schicht'], 0) + n
        if a['kollision']:
            nk += n
    gesamt = 0
    for name, teile in netz_inst.items():
        arr = np.concatenate(teile, axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]
    gel = {'rinne_anteil': round(float((rinne[im_feld] > 0.3).mean()), 4), 'kuppe_anteil': round(float((kuppe[im_feld] > 0.3).mean()), 4),
           'senke_anteil': round(float((senke[im_feld] > 0.3).mean()), 4), 'wandfuss_anteil': round(float((wandfuss[im_feld] > 0.3).mean()), 4),
           'terrasse_anteil': round(float(terrasse[im_feld].mean()), 4), 'restfeuchte_mittel': round(float(restfeuchte[im_feld].mean()), 4),
           'hang_mittel_grad': round(float(hang[im_feld].mean()), 2), 'wasser_anteil': round(float(wasser_m[im_feld].mean()), 4)}
    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': int(gesamt), 'ebene': regeln.get('ebene', 'wueste_ergaenzung'),
            'modus': modus, 'kollision_anzahl': int(nk), 'biome_eigen': biome_eigen, 'biome_fenster': biome_fenster,
            'zellen_zustaendig': zellen_zustaendig, 'dateien': dateien, 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'statistik': {'je_klasse': stat, 'je_schicht': stat_schicht, 'kollision': int(nk), 'biome_anteil_feld': bio_anteil, 'biom_quelle': bio_quelle,
                          'gelaende': gel, 'faktor': faktor, 'wuestenfeld': wf, 'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA},
            'hinweise': hinweise, 'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet'}
    if not wf:
        plan['entfernen'] = ''  # ergänzt nur; nichts wird ersetzt
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s [%s]: %d Instanzen (%d mit Kollision), %d Netze, %.1f s → %s' % (feld, modus, gesamt, nk, len(dateien), time.time() - t0, ausgabe))
    meld('  je Schicht: %s' % stat_schicht)
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
        shade = np.clip(0.55 + 0.45 * (n_z[fi0:fi1, fj0:fj1] * 0.6 + (-n_x[fi0:fi1, fj0:fj1] * 0.5 + n_y[fi0:fi1, fj0:fj1] * 0.5) * 0.8), 0.2, 1.0)
        g = (np.clip((hh - hh.min()) / max(1e-3, float(hh.max() - hh.min())), 0, 1) * 70 + 90) * shade
        rgb = np.stack([g * 1.08, g * 0.98, g * 0.85], axis=2)
        F = regeln.get('bild_farben', {})
        GF = F.get('_gelaende', {})
        for key, arr in (('rinne', rinne), ('wandfuss', wandfuss), ('terrasse', terrasse), ('kuppe', kuppe)):
            c = np.array(GF.get(key, [255, 255, 255]), np.float32)
            a = np.clip(arr[fi0:fi1, fj0:fj1], 0, 1)[..., None] * 0.45
            rgb = rgb * (1 - a) + c * a
        rgb[wasser_m[fi0:fi1, fj0:fj1]] = GF.get('wasser', [40, 80, 200])
        rgb[weg_m[fi0:fi1, fj0:fj1]] = GF.get('weg', [120, 80, 40])
        rgb[ort_m[fi0:fi1, fj0:fj1]] = GF.get('ort', [200, 40, 40])
        for a in aus:
            if a['fi'].size == 0:
                continue
            c = F.get(a['klasse'], [255, 255, 255])
            pi = np.clip(np.round(a['fi']).astype(np.int32) - fi0, 0, fi1 - fi0 - 1)
            pj = np.clip(np.round(a['fj']).astype(np.int32) - fj0, 0, fj1 - fj0 - 1)
            rgb[pi, pj] = c
            if a['schicht'] == '2_baum' or a['kollision']:
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    rgb[np.clip(pi + di, 0, fi1 - fi0 - 1), np.clip(pj + dj, 0, fj1 - fj0 - 1)] = c
        bo = os.path.join(basis, regeln['ausgabe']['bild'])
        os.makedirs(bo, exist_ok=True)
        Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(os.path.join(bo, feld + '.png'))
        meld('  Prüfbild: %s' % os.path.join(bo, feld + '.png'))
    return plan


def main():
    ap = argparse.ArgumentParser(description='Eldarien – Planer Wüste/Canyon/Ödland (Ergänzung, Auftrag 11 B9)')
    ap.add_argument('felder', nargs='+', help='Gitterfelder, z. B. D4 E6')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    ap.add_argument('--netze', default=None)
    ap.add_argument('--wueste_ebene', default=None)
    a = ap.parse_args()
    rp = a.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wueste_ergaenzung_regeln.json')
    if not os.path.isfile(rp):
        raise SystemExit('Regeldatei fehlt: %s' % rp)
    regeln = json.load(open(rp, encoding='utf-8'))
    if not os.path.isfile(os.path.join(a.basis, WELT, 'hoehe.f32')):
        raise SystemExit('hoehe.f32 fehlt unter %s – --basis auf die production-Wurzel setzen' % os.path.join(a.basis, WELT))
    if not NUMBA:
        meld('numba nicht verfügbar – reiner NumPy-Pfad (ausreichend)')
    inv = lade_inventar(a.basis, a.netze)
    pruefe_paletten(regeln, inv)
    for feld in a.felder:
        plane_feld(feld, a.basis, regeln, inv, a.faktor, a.bild, a.wueste_ebene)


if __name__ == '__main__':
    main()
