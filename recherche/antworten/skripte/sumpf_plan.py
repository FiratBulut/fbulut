#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien – Planer „Sumpf“ (Biom sumpf, Velen/Crookback-Bog-Typ; Auftrag 11 Teil B6).
Legt vier Ebenen in EINEM Ausgabeordner an: 0 boden (Laub, Zweige, Pilze, Moospolster, Schlammsteine),
1 mittel (Rohrkolben-Landteil, Seggenbulten, Schachtelhalm, Pestwurz, Adlerfarn, Weidengebüsch, liegendes Totholz,
Stümpfe, Wurzelteller), 2 baum (Weiden, tote Bäume im Flachwasser und an Land, Erlen-Ersatz, Jungweiden),
5 wasserkante (Rohrkolben/Binsen im Flachwasser nach Wassertiefe, Seerosen auf dem Spiegel, Seggen und Moos am Spiegel,
Treibholz im Flachwasser) sowie eine Punktliste für Wasserlinsen-Flecken (kein Netz im Inventar).
Fels (3) und Spuren (4) kommen aus Teil C/D; die Overrides dafür stehen in sumpf_regeln.json.

Aufruf (lokal, production-Wurzel):
    python -I scripts/sumpf/sumpf_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]

Liest (alle relativ zu --basis, Standard '.'):
    export/unreal/welt/hoehe.f32 (Pflicht, memmap, Fenster Feld + 64 m), karte_wasser.r8, karte_weg.r8, karte_ort.r8,
    eigner.r8 + welt.json (Biom je Zelle, Fallback aus Regeln je Feld, sonst aue), lage_<Name>.r8 (optional),
    teiche/teiche.json und wasser_welt.json[seen] (Umrisse, Spiegelhöhen; Fallback Spiegel = Geländehöhe am Wasserrand),
    bestand/<Feld>/, witcher/<Feld>/, ufer/foliage_<Feld>/, instanzen/instanzen.json (optional; Abstände zu Bäumen/Steinen),
    daten/netze.csv (Netzpfade prüfen; sonst vorlagen/daten/netze.csv neben dem Repo).
Schreibt:
    export/unreal/welt/sumpf/<Feld>/<Netzname>.f32 (je Instanz 10 float32 LE: x,y,z cm | qx,qy,qz,qw | sx,sy,sz)
    export/unreal/welt/sumpf/<Feld>/plan.json (FORMAT.md §3, je Datei zusätzlich "ebene"), bei --bild
    docs/pruefung/sumpf/<Feld>.png (1 px = 1 m; Zonen, Wasser mit Tiefe, Instanzen je Klasse).

Methode: Wasserfläche = karte_wasser ∪ Teich-/See-Umrisse. Wasserrand-Zellen sind Saatpunkte eines Jump-Flooding-Distanzfelds
(NumPy, exakt euklidisch bis 64 m); jede Zelle kennt so ihren nächsten Uferpunkt. Spiegel einer Wasserzelle = Höhe dieses
Uferpunkts (3-m-Glättung innerhalb des Wassers), überschrieben durch spiegel_cm aus teiche.json/wasser_welt.json.
Wassertiefe = Spiegel − Grund, Höhe über Spiegel (Land) = Grund − Spiegel des nächsten Ufers. Daraus Zonen flachwasser (≤ 0,5 m),
tiefwasser, spiegel (±0,2 m, ≤ 2 m), ufer (≤ 3 m, ≤ 0,8 m), bult (3–18 m; zusätzlich jede Nassfläche aus Schlamm/Algen-Lagen ohne
offenes Wasser in 18 m, weil H5 nur 0,4 % kartiertes Wasser hat), hinterland. karte_wasser-Zellen über dem Spiegel werden für die
Zonierung als Land behandelt, bleiben aber für alle Landklassen gesperrt (FORMAT §3: nichts auf Wasser). Dichte je Klasse = Basis × Zone ×
Bodenlagen × Hang × Höhe über Spiegel/Tiefe × Biom/Nässe × --faktor. Gruppen (Zentren + Mitglieder im Radius), Zufall aus
Hash(Rasterkoordinate, Seed, Kanal) → deterministisch, Nachbarfelder nahtlos. Nur NumPy; numba optional (nicht benötigt).

Quellen: FORMAT.md §1–§5; antworten/bildkritik-witcher-messlatte.md (TEICH1, Top 5); antworten/ufer-kies-coast-dunes.md (Frage 3);
antworten/assets-taxonomie.json (Biom sumpf); Rohrkolben 10–50 cm Tiefe (teichpflanzen-teichbau.com); Nymphaea alba 0,3–1,5 m
(first-nature.com); Snag-Dichte überfluteter Wälder 2 → 105/ha (ScienceDirect 2025, Ecological Indicators); Baumsterben ab 0,7–1,3 m
Überstau (USDA Forest Service, Lake Ocklawaha); GDC 2014 Gollent „Landscape Creation and Rendering in REDengine 3“ (Wasser-/Licht-
Simulation für Vegetation); 80.lv „World building of Witcher 3“ (Biom-Pinsel Sumpf).

UNGETESTET MIT ECHTDATEN – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern rauchgetestet (verteilung-sumpf.md §4/§6).
"""
import argparse
import csv
import json
import math
import os
import sys
import time

import numpy as np

try:  # numba optional – nur Meldung, der NumPy-Pfad reicht
    import numba  # noqa: F401
    NUMBA = True
except Exception:  # pragma: no cover
    NUMBA = False

NX, NY = 9577, 7057
FELD_M = 1008
X0, Y0 = 4730.5, 4060.5  # X_cm = (j − 4730,5)·100, Y_cm = (i − 4060,5)·100
WELT = os.path.join('export', 'unreal', 'welt')
BAUM_HINWEISE = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel', 'palme',
                 'hainbuche', 'hornbeam', 'beech', 'pine', 'poplar', 'willow', 'birch', 'fir', 'palm')
BAUM_AUSSCHLUSS = ('tot', 'dead', 'stump', 'log', 'fallen', 'branch', 'root', 'plant', 'sapling', 'seedling', 'bush')
ZONEN = {'flachwasser': 1, 'tiefwasser': 2, 'spiegel': 3, 'ufer': 4, 'bult': 5, 'hinterland': 6}
WASSER_ZONEN = (1, 2)


# ----------------------------------------------------------------------------- kleine Helfer
def meld(*a):
    print('[sumpf]', *a, flush=True)


def feld_fenster(feld, rand):
    """'H5' → ((i0,i1,j0,j1) Feld, (wi0,wi1,wj0,wj1) Fenster), beides auf das Raster geklippt (J-Spalte endet bei NX)."""
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX)
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY)
    win = (max(0, i0 - rand), min(NY, i1 + rand), max(0, j0 - rand), min(NX, j1 + rand))
    return (i0, i1, j0, j1), win


def lade_raster(pfad, dtype, win, pflicht=False):
    """Fensterausschnitt eines NY×NX-Rasters (memmap, nur das Fenster wird gelesen). None wenn Datei fehlt."""
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            raise SystemExit('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        meld('WARNUNG: %s hat %d Werte, erwartet %d (NY×NX) – Datei wird ignoriert' % (pfad, n, NX * NY))
        if pflicht:
            raise SystemExit('Pflichtdatei hat falsche Größe: %s' % pfad)
        return None
    mm = np.memmap(pfad, dtype=dtype, mode='r', shape=(NY, NX))
    return np.array(mm[wi0:wi1, wj0:wj1])


def box_blur(a, r):
    """Separierbarer Box-Filter (Radius r Zellen), Rand gespiegelt."""
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


def masken_blur(a, maske, sigma):
    """Glättung nur innerhalb einer Maske (gewichteter Blur)."""
    w = maske.astype(np.float32)
    num = gauss_blur(a * w, sigma)
    den = gauss_blur(w, sigma)
    out = np.where(den > 1e-4, num / np.maximum(den, 1e-4), a)
    return np.where(maske, out, a).astype(np.float32)


def verschiebe(a, di, dj, fill):
    """out[i, j] = a[i + di, j + dj], außerhalb fill."""
    H, W = a.shape
    out = np.full_like(a, fill)
    si0, si1 = max(0, di), min(H, H + di)
    sj0, sj1 = max(0, dj), min(W, W + dj)
    di0, di1 = max(0, -di), min(H, H - di)
    dj0, dj1 = max(0, -dj), min(W, W - dj)
    if si1 > si0 and sj1 > sj0:
        out[di0:di1, dj0:dj1] = a[si0:si1, sj0:sj1]
    return out


def dilate(mask, r):
    """Binäre Dilatation ≈ Kreisscheibe (Radius r Zellen; Wechsel 4er/8er-Nachbarschaft)."""
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


def jfa(mask, max_m=64.0):
    """Jump-Flooding: euklidische Distanz (m) zur nächsten True-Zelle und deren Index (si, sj). Jenseits max_m: 2·max_m, Index −1."""
    H, W = mask.shape
    fern = np.float32(max_m * 2.0)
    if not mask.any():
        return np.full((H, W), fern, np.float32), np.full((H, W), -1, np.int32), np.full((H, W), -1, np.int32)
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
                ok = csi >= 0
                cd2 = (ii - csi) ** 2 + (jj - csj) ** 2
                besser = ok & (cd2 < d2)
                d2 = np.where(besser, cd2, d2)
                si = np.where(besser, csi, si)
                sj = np.where(besser, csj, sj)
    d = np.sqrt(d2.astype(np.float32))
    weit = (d2 >= INF) | (d > max_m)
    d[weit] = fern
    si = np.where(weit, -1, si).astype(np.int32)
    sj = np.where(weit, -1, sj).astype(np.int32)
    return d.astype(np.float32), si, sj


def hash01(i, j, seed, kanal):
    """Deterministische Zufallszahl [0,1) je (absolute Rasterzeile, -spalte, Seed, Kanal)."""
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


def quaternionen(nx, ny, nz, kippen, yaw, neigung=None, neig_phi=None):
    """Z-Achse um Anteil `kippen` auf die Geländenormale kippen, optional zusätzlich um `neigung` (rad) in Richtung phi
    lehnen, davor Zufalls-Yaw. Ergebnis (n,4) = x,y,z,w."""
    n = len(nx)
    tz = (1 - kippen) + kippen * nz
    tx = kippen * nx
    ty = kippen * ny
    if neigung is not None:
        tx = tx + np.sin(neigung) * np.cos(neig_phi)
        ty = ty + np.sin(neigung) * np.sin(neig_phi)
    l = np.sqrt(tx * tx + ty * ty + tz * tz) + 1e-9
    tx, ty, tz = tx / l, ty / l, tz / l
    qt = np.stack([-ty, tx, np.zeros(n, np.float32), 1 + tz], axis=1)
    qt /= (np.linalg.norm(qt, axis=1, keepdims=True) + 1e-9)
    qy = np.stack([np.zeros(n, np.float32), np.zeros(n, np.float32), np.sin(yaw / 2), np.cos(yaw / 2)], axis=1)
    q = quat_mul(qt, qy)
    return (q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-9)).astype(np.float32)


def polygon_maske(pi, pj, H, W):
    """Rasterzellen (Zentren) innerhalb eines Polygons (Fensterkoordinaten, float). Crossing-Number, je Kante vektorisiert."""
    out = np.zeros((H, W), bool)
    if len(pi) < 3:
        return out
    i0 = max(0, int(math.floor(pi.min())))
    i1 = min(H, int(math.ceil(pi.max())) + 1)
    j0 = max(0, int(math.floor(pj.min())))
    j1 = min(W, int(math.ceil(pj.max())) + 1)
    if i1 <= i0 or j1 <= j0:
        return out
    ii, jj = np.mgrid[i0:i1, j0:j1]
    ii = ii.astype(np.float32)
    jj = jj.astype(np.float32)
    innen = np.zeros(ii.shape, bool)
    n = len(pi)
    for k in range(n):
        ai, aj = pi[k], pj[k]
        bi, bj = pi[(k + 1) % n], pj[(k + 1) % n]
        if ai == bi:
            continue
        cond = ((ai > ii) != (bi > ii)) & (jj < (bj - aj) * (ii - ai) / (bi - ai) + aj)
        innen ^= cond
    out[i0:i1, j0:j1] = innen
    return out


# ----------------------------------------------------------------------------- Inventar / Regeln
def lade_regeln(pfad):
    if not os.path.isfile(pfad):
        raise SystemExit('Regeldatei fehlt: %s' % pfad)
    with open(pfad, encoding='utf-8') as f:
        return json.load(f)


def finde_netze_csv(basis):
    hier = os.path.dirname(os.path.abspath(__file__))
    kandidaten = [os.path.join(basis, 'daten', 'netze.csv'),
                  os.path.join(hier, 'netze.csv'),
                  os.path.join(hier, '..', '..', 'vorlagen', 'daten', 'netze.csv'),
                  os.path.join(hier, '..', 'daten', 'netze.csv')]
    for k in kandidaten:
        if os.path.isfile(k):
            return k
    return None


def pruefe_netze(regeln, basis):
    """Entfernt Netzpfade, die nicht im Inventar stehen; Klassen ohne Netz werden deaktiviert."""
    p = finde_netze_csv(basis)
    if p is None:
        meld('WARNUNG: daten/netze.csv nicht gefunden – Netzpfade ungeprüft')
        return
    pfade = set()
    with open(p, encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f, delimiter=';'):
            if row.get('pfad'):
                pfade.add(row['pfad'].strip())
    fehlt = []
    for kname, k in regeln['klassen'].items():
        ok = [n for n in k['netze'] if n in pfade]
        bad = [n for n in k['netze'] if n not in pfade]
        if bad:
            fehlt += bad
            if k.get('gewichte') and len(k['gewichte']) == len(k['netze']):
                k['gewichte'] = [g for n, g in zip(k['netze'], k['gewichte']) if n in pfade]
            k['netze'] = ok
        if not ok:
            k['dichte'] = 0.0
            meld('WARNUNG: Klasse %s hat kein Netz im Inventar – deaktiviert' % kname)
    # Override-Netze (Teil C/D) nur melden, nicht streichen
    ov = []

    def sammle(o):
        if isinstance(o, dict):
            for v in o.values():
                sammle(v)
        elif isinstance(o, list):
            for v in o:
                sammle(v)
        elif isinstance(o, str) and o.startswith('/Game/'):
            ov.append(o)
    sammle(regeln.get('felsgruppen_overrides', {}))
    sammle(regeln.get('spuren_overrides', {}))
    ov_fehlt = sorted(set(n for n in ov if n not in pfade))
    if ov_fehlt:
        meld('WARNUNG: %d Override-Netze (Teil C/D) nicht im Inventar: %s' % (len(ov_fehlt), ', '.join(ov_fehlt[:8])))
    if fehlt:
        meld('WARNUNG: %d Netzpfade nicht in %s: %s' % (len(fehlt), p, ', '.join(sorted(set(fehlt))[:8])))
    else:
        meld('Netzpfade geprüft gegen %s: alle %d Klassen-Netze vorhanden' % (p, len(set(n for k in regeln['klassen'].values() for n in k['netze']))))


# ----------------------------------------------------------------------------- Weltdaten
def lade_biome(basis, win, regeln, feld):
    """Biomfaktor je Zelle (0–1) und Maske 'biom sumpf'."""
    bf = regeln['biom_faktor']
    fb = regeln.get('felder', {}).get(feld, {}).get('biom_fallback', 'aue')
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    anteil = {}
    if eig is None or not os.path.isfile(wj):
        meld('Hinweis: eigner.r8/welt.json fehlen – Biom je Zelle = Fallback %r' % fb)
        f = float(bf.get(fb, 0.0))
        return np.full((H, W), f, np.float32), np.full((H, W), fb == 'sumpf', bool), {fb: 1.0}
    try:
        welt = json.load(open(wj, encoding='utf-8'))
    except Exception as e:
        meld('Hinweis: welt.json unlesbar (%s) – Fallback %r' % (e, fb))
        f = float(bf.get(fb, 0.0))
        return np.full((H, W), f, np.float32), np.full((H, W), fb == 'sumpf', bool), {fb: 1.0}
    kacheln = welt.get('kacheln', {})
    namen = list(bf.keys())

    def biom_aus_rezept(rz):
        rz = str(rz).lower()
        if rz in namen:
            return rz
        if 'vulkan' in rz or 'lava' in rz:
            return 'lava'
        for n in namen:
            if n in rz:
                return n
        return None

    tabelle = [None] * 256
    # Kennzahl 0 = Weltgelände ohne Houdini-Kachel: dominantes Feldbiom (Regeln 'felder' → biom_fallback), sonst aue (FORMAT §2)
    tabelle[0] = fb
    eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
    for k, v in eintraege:
        try:
            if isinstance(v, dict) and any(x in v for x in ('id', 'kennzahl', 'nr')):
                k = v.get('id', v.get('kennzahl', v.get('nr')))
            idx = int(k)
        except Exception:
            continue
        if 0 <= idx < 256:
            b = biom_aus_rezept(v.get('rezept', v.get('biom', '')) if isinstance(v, dict) else v)
            tabelle[idx] = b or tabelle[idx]
    fakt = np.zeros(256, np.float32)
    sumpf_t = np.zeros(256, bool)
    for idx in range(256):
        b = tabelle[idx] or fb
        fakt[idx] = float(bf.get(b, 0.0))
        sumpf_t[idx] = (b == 'sumpf')
    werte, zahl = np.unique(eig, return_counts=True)
    for w, c in zip(werte, zahl):
        b = tabelle[int(w)] or fb
        anteil[b] = anteil.get(b, 0.0) + float(c) / eig.size
    return fakt[eig], sumpf_t[eig], anteil


def lade_lagen(basis, win, namen):
    lagen = {}
    for n in sorted(set(namen)):
        if n == 'sonst':
            continue
        a = lade_raster(os.path.join(basis, WELT, 'lage_%s.r8' % n), np.uint8, win)
        if a is not None:
            lagen[n] = a.astype(np.float32) / 255.0
    return lagen


def lade_polygone(basis, win):
    """Teich-/See-Umrisse → Liste (maske, spiegel_m|None, name). Koordinaten cm Welt (Annahme)."""
    H, W = win[1] - win[0], win[3] - win[2]
    aus = []

    def umriss_zu_maske(pts):
        p = np.asarray(pts, np.float64)
        if p.ndim != 2 or p.shape[0] < 3:
            return None
        fj = p[:, 0] / 100.0 + X0 - win[2]
        fi = p[:, 1] / 100.0 + Y0 - win[0]
        if fi.max() < 0 or fi.min() >= H or fj.max() < 0 or fj.min() >= W:
            return None
        return polygon_maske(fi.astype(np.float32), fj.astype(np.float32), H, W)

    def spiegel_aus(e):
        for k in ('spiegel_cm', 'z_cm', 'hoehe_cm'):
            if k in e:
                try:
                    return float(e[k]) / 100.0
                except Exception:
                    pass
        for k in ('spiegel', 'z', 'spiegel_m'):
            if k in e:
                try:
                    return float(e[k])
                except Exception:
                    pass
        return None

    def sammle(obj, quelle):
        n = 0
        liste = obj
        if isinstance(obj, dict):
            for k in ('teiche', 'seen', 'liste', 'eintraege'):
                if isinstance(obj.get(k), list):
                    liste = obj[k]
                    break
            else:
                liste = list(obj.values()) if all(isinstance(v, dict) for v in obj.values()) else []
        if not isinstance(liste, list):
            return 0
        for e in liste:
            if not isinstance(e, dict):
                continue
            pts = e.get('umriss') or e.get('punkte') or e.get('polygon')
            if not pts:
                continue
            m = umriss_zu_maske(pts)
            if m is None or not m.any():
                continue
            aus.append((m, spiegel_aus(e), '%s:%s' % (quelle, e.get('name', e.get('id', len(aus))))))
            n += 1
        return n

    for rel, schluessel in (('teiche/teiche.json', None), ('wasser_welt.json', 'seen')):
        p = os.path.join(basis, WELT, rel)
        if not os.path.isfile(p):
            meld('Hinweis: %s fehlt – keine Umrisse/Spiegel daraus' % rel)
            continue
        try:
            obj = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            meld('Hinweis: %s unlesbar (%s)' % (rel, e))
            continue
        if schluessel:
            obj = obj.get(schluessel, [])
        n = sammle(obj, rel.split('/')[-1].split('.')[0])
        meld('%s: %d Umrisse im Fenster' % (rel, n))
    return aus


def lade_ebene(ordner, win):
    """Positionen (fi, fj) von Bäumen und Sonstigem einer vorhandenen Ebene (plan.json + f32; ohne plan.json alle f32)."""
    baum, sonst = [], []
    if not os.path.isdir(ordner):
        return baum, sonst
    info = {}
    pj = os.path.join(ordner, 'plan.json')
    if os.path.isfile(pj):
        try:
            info = json.load(open(pj, encoding='utf-8')).get('dateien', {})
        except Exception:
            info = {}
    for f in sorted(os.listdir(ordner)):
        if not f.endswith('.f32'):
            continue
        name = f[:-4]
        try:
            a = np.fromfile(os.path.join(ordner, f), dtype='<f4')
        except Exception:
            continue
        if a.size % 10 or a.size == 0:
            continue
        a = a.reshape(-1, 10)
        fj = a[:, 0] / 100.0 + X0 - win[2]
        fi = a[:, 1] / 100.0 + Y0 - win[0]
        m = (fi >= 0) & (fi < win[1] - win[0]) & (fj >= 0) & (fj < win[3] - win[2])
        if not m.any():
            continue
        e = info.get(name, {})
        txt = (str(e.get('rolle', '')) + ' ' + str(e.get('gruppe', '')) + ' ' + name).lower()
        ist_baum = any(r in txt for r in BAUM_HINWEISE) and not any(x in txt for x in BAUM_AUSSCHLUSS)
        (baum if ist_baum else sonst).append(np.stack([fi[m], fj[m]], axis=1))
    return baum, sonst


def lade_bestand(basis, feld, win):
    """Bäume aus bestand/, witcher/ (Feld + Nachbarn), Steine/Sonstiges aus ufer/foliage_<Feld>/, Houdini instanzen.json."""
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
                b, so = lade_ebene(os.path.join(basis, WELT, ebene, nf), win)
                if b or so:
                    quellen.append('%s/%s' % (ebene, nf))
                baum += b
                sonst += so
            b, so = lade_ebene(os.path.join(basis, WELT, 'ufer', 'foliage_' + nf), win)
            if b or so:
                quellen.append('ufer/foliage_%s' % nf)
            sonst += b + so
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
                if a.size % 10 or a.size == 0:
                    continue
                a = a.reshape(-1, 10)
                fj = a[:, 0] / 100.0 + X0 - win[2]
                fi = a[:, 1] / 100.0 + Y0 - win[0]
                m = (fi >= 0) & (fi < win[1] - win[0]) & (fj >= 0) & (fj < win[3] - win[2])
                if not m.any():
                    continue
                ist_baum = any(k in txt for k in BAUM_HINWEISE) and not any(x in txt for x in BAUM_AUSSCHLUSS)
                (baum if ist_baum else sonst).append(np.stack([fi[m], fj[m]], axis=1))
                quellen.append('instanzen/' + os.path.basename(f))
        except Exception as e:
            meld('Hinweis: instanzen.json nicht auswertbar (%s)' % e)
    baum = np.concatenate(baum, axis=0) if baum else np.zeros((0, 2), np.float32)
    sonst = np.concatenate(sonst, axis=0) if sonst else np.zeros((0, 2), np.float32)
    return baum, sonst, quellen


def punkte_maske(pts, H, W):
    m = np.zeros((H, W), bool)
    if len(pts):
        i = np.clip(np.round(pts[:, 0]).astype(np.int32), 0, H - 1)
        j = np.clip(np.round(pts[:, 1]).astype(np.int32), 0, W - 1)
        m[i, j] = True
    return m


# ----------------------------------------------------------------------------- Planung je Feld
def plane_feld(feld, basis, regeln, faktor, bild):
    t0 = time.time()
    rand = int(regeln.get('fenster_rand_m', 64))
    fb, win = feld_fenster(feld, rand)
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    seed = int(regeln.get('seed', 1))
    hinweise = []
    meld('Feld %s: Fenster %d×%d m (Rand %d m)' % (feld, H, W, rand))

    # --- Raster
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True).astype(np.float32)
    if not np.isfinite(hoehe).all():
        hoehe = np.nan_to_num(hoehe, nan=0.0, posinf=0.0, neginf=0.0)
        hinweise.append('hoehe.f32 enthielt NaN/Inf → 0')

    def r8(name):
        a = lade_raster(os.path.join(basis, WELT, name), np.uint8, win)
        if a is None:
            meld('Hinweis: %s fehlt – als leer behandelt' % name)
            hinweise.append('%s fehlt' % name)
            return np.zeros((H, W), bool)
        return a > 0

    wasser_k = r8('karte_wasser.r8')
    weg = r8('karte_weg.r8')
    ort = r8('karte_ort.r8')
    biomf, biom_sumpf, bio_anteil = lade_biome(basis, win, regeln, feld)

    lagen_namen = set(regeln['nass_maske']['lagen'].keys())
    for k in regeln['klassen'].values():
        lagen_namen |= set(k.get('lagen_faktor', {}).keys())
    lagen = lade_lagen(basis, win, lagen_namen)
    if not lagen:
        hinweise.append('keine lage_*.r8 gefunden – Lagenfaktoren = 1, Nassmaske nur aus Wassernähe')
    meld('Lagen geladen: %s' % (', '.join(sorted(lagen)) or 'keine'))

    # --- Gelände: Normale, Hang
    hg = gauss_blur(hoehe, 1.5)
    gi = np.gradient(hg, axis=0)
    gj = np.gradient(hg, axis=1)
    n_len = np.sqrt(gi * gi + gj * gj + 1.0)
    n_x = (-gj / n_len).astype(np.float32)  # Weltx ↔ Spalte j
    n_y = (-gi / n_len).astype(np.float32)  # Welty ↔ Zeile i
    n_z = (1.0 / n_len).astype(np.float32)
    hang = np.degrees(np.arctan(np.sqrt(gi * gi + gj * gj))).astype(np.float32)

    # --- Wasser und Spiegel
    polys = lade_polygone(basis, win)
    wasser0 = wasser_k.copy()
    for m, sp, name in polys:
        wasser0 |= m
    distmax = float(regeln['wasser'].get('distanz_max_m', 64.0))
    spiegel0 = hoehe.copy()
    if wasser0.any():
        rand0 = wasser0 & dilate(~wasser0, 1)
        d0, si0, sj0 = jfa(rand0, max_m=max(distmax, 128.0))
        hat = si0 >= 0
        sp_w = np.where(hat, hoehe[np.maximum(si0, 0), np.maximum(sj0, 0)], hoehe)
        sp_w = masken_blur(sp_w, wasser0, float(regeln['wasser'].get('spiegel_glaettung_sigma_m', 3.0)))
        spiegel0 = np.where(wasser0, sp_w, hoehe).astype(np.float32)
        n_sp = 0
        for m, sp, name in polys:
            if sp is not None:
                spiegel0[m] = np.float32(sp)
                n_sp += 1
        if polys:
            meld('%d Umrisse, davon %d mit expliziter Spiegelhöhe' % (len(polys), n_sp))
    wasser = wasser0 & (hoehe <= spiegel0 + 0.05)
    trocken_w = wasser0 & ~wasser  # als Wasser kartiert, aber über dem Spiegel: für die Zonierung Land, für Landklassen trotzdem gesperrt
    if wasser0.any() and not wasser.any():
        hinweise.append('Wasserflächen liegen komplett über dem abgeleiteten Spiegel – Umrisse/Spiegel prüfen')
    if trocken_w.any():
        hinweise.append('%d karte_wasser-Zellen liegen > 5 cm über dem Spiegel (Zonierung als Land, für Landklassen gesperrt)' % int(trocken_w.sum()))
    if wasser.any():
        rand_w = wasser & dilate(~wasser, 1)
        d_w, si, sj = jfa(rand_w, max_m=distmax)
        hat = si >= 0
        spiegel = np.where(wasser, spiegel0, np.where(hat, spiegel0[np.maximum(si, 0), np.maximum(sj, 0)], hoehe)).astype(np.float32)
    else:
        d_w = np.full((H, W), np.float32(distmax * 2.0))
        si = sj = np.full((H, W), -1, np.int32)
        hat = np.zeros((H, W), bool)
        spiegel = hoehe.copy()
        hinweise.append('kein Wasser im Fenster – nur Hinterland-Klassen')
    tiefe = np.where(wasser, np.maximum(spiegel - hoehe, 0.0), 0.0).astype(np.float32)
    h_ueber = np.where(wasser, 0.0, np.where(hat, hoehe - spiegel, 0.0)).astype(np.float32)
    fern = ~hat & ~wasser
    wasser_anteil = float(wasser[fb[0] - wi0:fb[1] - wi0, fb[2] - wj0:fb[3] - wj0].mean())
    meld('Wasser im Feld: %.2f %% der Fläche; Tiefe max %.2f m' % (100 * wasser_anteil, float(tiefe.max())))

    # --- Nassmaske
    nm = regeln['nass_maske']
    if lagen:
        summe = np.zeros((H, W), np.float32)
        for ln, f in nm['lagen'].items():
            if ln in lagen:
                summe += lagen[ln] * float(f)
        summe = gauss_blur(summe, float(nm.get('sigma_m', 6.0)))
        nass = (summe >= float(nm.get('schwelle', 0.35))) | (d_w <= 3.0)
    else:
        nass = d_w <= 12.0
    sumpfig = biom_sumpf | nass

    # --- Zonen
    Z = regeln['zonen']
    zone = np.zeros((H, W), np.int8)
    fw_max = float(Z['flachwasser']['tiefe_m'][1])
    zone[wasser & (tiefe <= fw_max)] = ZONEN['flachwasser']
    zone[wasser & (tiefe > fw_max)] = ZONEN['tiefwasser']
    land = ~wasser
    sp_lo, sp_hi = Z['spiegel']['hoehe_ueber_spiegel_m']
    sp_d = float(Z['spiegel'].get('abstand_wasser_max_m', 2.0))
    z_sp = land & hat & (h_ueber <= sp_hi) & (d_w <= sp_d)
    zone[z_sp] = ZONEN['spiegel']
    uf_d0, uf_d1 = Z['ufer']['abstand_wasser_m']
    uf_h = float(Z['ufer']['hoehe_ueber_spiegel_m'][1])
    z_uf = land & hat & (zone == 0) & (d_w <= uf_d1) & (h_ueber <= uf_h)
    zone[z_uf] = ZONEN['ufer']
    bu_d0, bu_d1 = Z['bult']['abstand_wasser_m']
    bu_h = float(Z['bult']['hoehe_ueber_spiegel_m'][1])
    z_bu = land & hat & (zone == 0) & (d_w <= bu_d1) & (h_ueber <= bu_h)
    zone[z_bu] = ZONEN['bult']
    hi_h = float(Z['hinterland']['hoehe_ueber_spiegel_m'][1])
    z_hi = land & (zone == 0) & ((h_ueber <= hi_h) | fern)
    zone[z_hi] = ZONEN['hinterland']
    # Nassflächen ohne offenes Wasser (Schlamm/Algen-Lagen > 18 m vom nächsten Wasser, z. B. H5 mit nur 0,4 % kartiertem Wasser)
    # zählen als Bultenzone: dort Seggen, Moos, Weidengebüsch statt nur Hinterland-Laub.
    nass_fern = (zone == ZONEN['hinterland']) & nass & (d_w > bu_d1)
    zone[nass_fern] = ZONEN['bult']
    im_feld = np.zeros((H, W), bool)
    im_feld[fb[0] - wi0:fb[1] - wi0, fb[2] - wj0:fb[3] - wj0] = True
    zstat = {name: int(((zone == idx) & im_feld & sumpfig).sum()) for name, idx in ZONEN.items()}
    zstat['bult_ohne_wasser'] = int((nass_fern & im_feld).sum())
    meld('Zonen im Feld (sumpfig, m²): %s' % zstat)

    # --- Faktoren
    HA = regeln['hoehe_ueber_spiegel_abnahme']
    h_f = np.clip(1.0 - (h_ueber - HA['voll_bis_m']) / max(1e-3, HA['null_ab_m'] - HA['voll_bis_m']), 0.0, 1.0).astype(np.float32)
    h_f[fern] = 1.0  # ohne Wasser in 64 m: Sumpfbiom gilt als flach
    HG = regeln['hang']
    hang_f = np.clip(1.0 - (hang - HG['voll_bis_grad']) / max(1e-3, HG['null_ab_grad'] - HG['voll_bis_grad']), 0.0, 1.0).astype(np.float32)
    nass_f = np.where(nass, 0.5, 0.0).astype(np.float32)
    biom_wasserkl = np.maximum(biomf, nass_f)  # Wasserzonen-Klassen auch außerhalb des Sumpfbioms (halbe Stärke)

    # --- Ausschlüsse
    A = regeln['abstand_m']
    weg_klein = dilate(weg, A['weg_klein']) if weg.any() else weg
    weg_gross = dilate(weg, A['weg_gross']) if weg.any() else weg
    ort_m = dilate(ort, A['ort']) if ort.any() else ort
    baum_pts, sonst_pts, quellen = lade_bestand(basis, feld, win)
    meld('Bestand: %d Bäume, %d Sonstige aus %s' % (len(baum_pts), len(sonst_pts), ', '.join(quellen) or 'nichts'))
    baum_m = punkte_maske(baum_pts, H, W)
    sonst_m = punkte_maske(sonst_pts, H, W)
    sonst_d = dilate(sonst_m, A['bestand_sonst']) if sonst_m.any() else sonst_m
    stamm_klein = dilate(baum_m, A['baumstamm_klein']) if baum_m.any() else baum_m
    eigene_baum_m = np.zeros((H, W), bool)   # von dieser Ebene gesetzte Bäume
    holz_m = np.zeros((H, W), bool)          # liegendes Totholz / Stümpfe dieser Ebene (für Pilze)
    baum_dil_cache = {}

    def baum_abstand_maske(r):
        key = round(float(r), 1)
        if key not in baum_dil_cache:
            bm = baum_m | eigene_baum_m
            baum_dil_cache[key] = dilate(bm, r) if bm.any() else bm
        return baum_dil_cache[key]

    # --- Klassen
    prio = list(regeln['budget']['prioritaet'])
    for kname in regeln['klassen']:
        if kname not in prio:
            prio.append(kname)
    K = regeln['klassen']
    klassen_idx = {k: n for n, k in enumerate(K.keys())}
    ergebnisse = []
    ii_abs, jj_abs = np.indices((H, W), dtype=np.int32)
    ii_abs += wi0
    jj_abs += wj0
    dw_blur = gauss_blur(d_w, 2.0)
    dgi = np.gradient(dw_blur, axis=0)
    dgj = np.gradient(dw_blur, axis=1)

    for kname in prio:
        k = K.get(kname)
        if k is None or float(k.get('dichte', 0)) <= 0 or not k.get('netze'):
            continue
        kidx = klassen_idx[kname]
        kan = kidx * 32
        zonen = [ZONEN[z] for z in k['zone']]
        zf = np.zeros(8, np.float32)
        for z, f in k.get('zonen_faktor', {}).items():
            zf[ZONEN[z]] = float(f)
        for z in zonen:
            if zf[z] == 0:
                zf[z] = 1.0
        dens = (float(k['dichte']) * faktor) * zf[zone]
        ist_wasserklasse = any(z in WASSER_ZONEN for z in zonen)
        # Lagen
        lf = k.get('lagen_faktor', {})
        if lagen and lf:
            akk = np.zeros((H, W), np.float32)
            rest = np.ones((H, W), np.float32)
            for ln, f in lf.items():
                if ln == 'sonst' or ln not in lagen:
                    continue
                w = lagen[ln]
                akk += w * float(f)
                rest -= w
            rest = np.clip(rest, 0.0, 1.0)
            akk += rest * float(lf.get('sonst', 0.5))
            lagen_f = np.clip(akk, 0.0, 2.0)
        else:
            lagen_f = np.ones((H, W), np.float32)
        dens = dens * lagen_f
        # Hang, Höhe/Tiefe
        hmax = float(k.get('hang_max_grad', HG['wasser_klassen_max_grad'] if ist_wasserklasse else HG['null_ab_grad']))
        if ist_wasserklasse:
            dens = dens * np.where(hang <= hmax, 1.0, 0.0)
            t0_, t1_ = k.get('tiefe_m', [0.0, fw_max])
            tf = ((tiefe >= t0_) & (tiefe <= t1_)).astype(np.float32)
            prof = k.get('tiefe_profil')
            if prof:
                xs = np.array(sorted(float(x) for x in prof), np.float32)
                ys = np.array([float(prof[str(x) if str(x) in prof else x]) for x in sorted(prof, key=float)], np.float32)
                tf = tf * np.interp(tiefe, xs, ys).astype(np.float32)
            dens = dens * tf
            # Landzellen der Spiegelzone (falls Klasse sie erlaubt): ohne Tiefenfilter, mit Hangfaktor
            if ZONEN['spiegel'] in zonen:
                dens = np.where(zone == ZONEN['spiegel'], (float(k['dichte']) * faktor) * zf[ZONEN['spiegel']] * lagen_f * hang_f, dens)
            dens = dens * biom_wasserkl
        else:
            dens = dens * hang_f * np.where(hang <= hmax, 1.0, 0.0) * h_f
            dens = dens * (biomf if k.get('biom_hinterland') else biom_wasserkl)
            dens = dens * np.where(zone == ZONEN['hinterland'], biomf, 1.0)
        dens = dens * np.where(sumpfig, 1.0, 0.0)
        # Ausschlüsse
        gross = bool(k.get('kollision')) or k['ebene'].startswith('2')
        erlaubt = ~ort_m & ~(weg_gross if gross else weg_klein) & ~sonst_d
        if ist_wasserklasse:
            erlaubt &= np.isin(zone, zonen)
        else:
            erlaubt &= land & ~trocken_w & np.isin(zone, zonen)  # FORMAT §3: nichts auf Wasser (karte_wasser gilt hart)
        ab = float(k.get('abstand_baum_m', 0.0))
        erlaubt &= ~(baum_abstand_maske(ab) if ab > 0 else stamm_klein)
        if k.get('abstand_ufer_min_m'):
            erlaubt &= d_w >= float(k['abstand_ufer_min_m'])
        # Nähe-Boni
        if k.get('an_totholz_m') and holz_m.any():
            nah = dilate(holz_m, float(k['an_totholz_m']))
            dens = dens * np.where(nah, float(k.get('an_totholz_faktor', 1.0)), 1.0)
        if k.get('an_baum_m') and (baum_m | eigene_baum_m).any():
            nah = dilate(baum_m | eigene_baum_m, float(k['an_baum_m']))
            dens = dens * np.where(nah, float(k.get('an_baum_faktor', 1.0)), 1.0)
        dens = np.where(erlaubt, dens, 0.0).astype(np.float32)
        if not (dens > 0).any():
            continue
        # Gruppenzentren
        g0, g1 = k.get('gruppe', [1, 1])
        gm = 0.5 * (g0 + g1)
        pc = np.minimum(dens / gm, 1.0)
        zent = hash01(ii_abs, jj_abs, seed, kan) < pc
        ci, cj = np.nonzero(zent)
        if ci.size == 0:
            continue
        ca_i, ca_j = ci + wi0, cj + wj0
        nmit = (g0 + np.floor(hash01(ca_i, ca_j, seed, kan + 1) * (g1 - g0 + 1))).astype(np.int32)
        nmit = np.clip(nmit, g0, g1)
        maxm = int(g1)
        rad = float(k.get('radius_m', 1.0))
        mi_l, mj_l, fi_l, fj_l = [], [], [], []
        for mm in range(maxm):
            sel = nmit > mm
            if not sel.any():
                break
            bi, bj = ca_i[sel], ca_j[sel]
            if mm == 0:
                off_i = (hash01(bi, bj, seed, kan + 2) - 0.5) * 0.9
                off_j = (hash01(bi, bj, seed, kan + 3) - 0.5) * 0.9
            else:
                r = rad * np.sqrt(hash01(bi, bj, seed, kan + 4 + 2 * mm))
                th = 2 * np.pi * hash01(bi, bj, seed, kan + 5 + 2 * mm)
                off_i = r * np.sin(th)
                off_j = r * np.cos(th)
            fi = ci[sel] + off_i
            fj = cj[sel] + off_j
            ok = (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1)
            fi, fj = fi[ok], fj[ok]
            mi = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
            mj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
            if mm > 0:
                # Mitglied nur, wenn Zelle erlaubt und Dichte dort nicht viel kleiner als am Zentrum
                dz = dens[ci[sel][ok], cj[sel][ok]]
                akz = (dens[mi, mj] > 0) & (hash01(mi + wi0, mj + wj0, seed, kan + 30) < np.minimum(dens[mi, mj] / np.maximum(dz, 1e-6), 1.0))
                fi, fj, mi, mj = fi[akz], fj[akz], mi[akz], mj[akz]
            mi_l.append(mi)
            mj_l.append(mj)
            fi_l.append(fi.astype(np.float32))
            fj_l.append(fj.astype(np.float32))
        if not fi_l:
            continue
        mi = np.concatenate(mi_l)
        mj = np.concatenate(mj_l)
        fi = np.concatenate(fi_l)
        fj = np.concatenate(fj_l)
        # Mindestabstand (grobes Gitter, kleinster Hash gewinnt)
        mind = float(k.get('min_abstand_m', 0.0))
        if mind > 0 and fi.size:
            gi_ = ((fi + wi0) / mind).astype(np.int64)
            gj_ = ((fj + wj0) / mind).astype(np.int64)
            key = gi_ * 100003 + gj_
            hv = hash01(mi + wi0, mj + wj0, seed, kan + 31)
            order = np.lexsort((hv, key))
            key_s = key[order]
            first = np.ones(key_s.size, bool)
            first[1:] = key_s[1:] != key_s[:-1]
            keep = np.zeros(fi.size, bool)
            keep[order[first]] = True
            mi, mj, fi, fj = mi[keep], mj[keep], fi[keep], fj[keep]
        # nur Instanzen im Feld ausgeben (Rand nur für Nahtlosigkeit)
        imf = im_feld[mi, mj]
        mi, mj, fi, fj = mi[imf], mj[imf], fi[imf], fj[imf]
        if fi.size == 0:
            continue
        ai, aj = mi + wi0, mj + wj0
        # Netzwahl (gewichtet), Maßstab, Yaw
        netze = k['netze']
        gew = np.array(k.get('gewichte') or [1.0] * len(netze), np.float32)
        if gew.size != len(netze):
            gew = np.ones(len(netze), np.float32)
        cum = np.cumsum(gew / gew.sum())
        netz = np.searchsorted(cum, hash01(ai, aj, seed, kan + 6), side='right')
        netz = np.clip(netz, 0, len(netze) - 1)
        s0, s1 = k.get('massstab', [1.0, 1.0])
        massstab = (s0 + (s1 - s0) * hash01(ai, aj, seed, kan + 7)).astype(np.float32)
        if k.get('yaw', 'zufall') == 'ufer':
            yaw = np.arctan2(dgj[mi, mj], dgi[mi, mj]).astype(np.float32)  # Richtung vom Wasser weg (Welt: x=j, y=i)
            yaw = yaw + (hash01(ai, aj, seed, kan + 8) - 0.5) * np.radians(40.0) + np.where(hash01(ai, aj, seed, kan + 9) < 0.5, 0.0, np.pi)
        else:
            yaw = (2 * np.pi * hash01(ai, aj, seed, kan + 8)).astype(np.float32)
        neig = None
        neig_phi = None
        if k.get('neigung_grad'):
            a0, a1 = k['neigung_grad']
            neig = np.radians(a0 + (a1 - a0) * hash01(ai, aj, seed, kan + 10)).astype(np.float32)
            neig_phi = (2 * np.pi * hash01(ai, aj, seed, kan + 11)).astype(np.float32)
        ergebnisse.append({'klasse': kname, 'ebene': k['ebene'], 'mi': mi, 'mj': mj, 'fi': fi, 'fj': fj, 'netz': netz,
                           'massstab': massstab, 'yaw': yaw, 'neig': neig, 'neig_phi': neig_phi, 'eingraben': float(k.get('eingraben_cm', 0)),
                           'kippen': float(k.get('kippen', 0.0)), 'auf_spiegel': bool(k.get('auf_spiegel')),
                           'spiegel_versatz': float(k.get('spiegel_versatz_cm', 1.0)), 'kollision': bool(k.get('kollision')),
                           'schatten': bool(k.get('schatten', True)), 'sichtweite': list(k.get('sichtweite', [0, 0]))})
        if k['ebene'].startswith('2'):
            eigene_baum_m[mi, mj] = True
            baum_dil_cache.clear()
        if kname in ('totholz_gross', 'totholz_klein', 'stumpf', 'treibholz_wasser'):
            holz_m[mi, mj] = True

    # --- Budget
    B = regeln['budget']
    stat = {e['klasse']: int(e['fi'].size) for e in ergebnisse}
    gesamt = sum(stat.values())
    nk = sum(n for kn, n in stat.items() if K[kn].get('kollision'))
    ausduenn = {}
    if nk > B['kollision_je_feld']:
        f = B['kollision_je_feld'] / float(nk)
        for kn in stat:
            if K[kn].get('kollision'):
                ausduenn[kn] = f
        hinweise.append('Kollisionsbudget: %d → %d, Faktor %.2f auf Kollisionsklassen' % (nk, B['kollision_je_feld'], f))
    ziel = int(B.get('ziel_instanzen_je_feld', B['instanzen_je_feld']))
    if gesamt > ziel:
        ueber = gesamt - ziel
        pool, summe = [], 0
        for kn in reversed(prio):
            n = stat.get(kn, 0)
            if n == 0:
                continue
            pool.append(kn)
            summe += n
            if summe * 0.6 >= ueber:
                break
        f = max(0.0, 1.0 - ueber / float(max(1, summe)))
        for kn in pool:
            ausduenn[kn] = min(ausduenn.get(kn, 1.0), f)
        hinweise.append('Instanzbudget: %d → Ziel %d, Ausdünnung %s' % (gesamt, ziel, {kn: round(v, 2) for kn, v in ausduenn.items()}))
    for e in ergebnisse:
        f = ausduenn.get(e['klasse'], 1.0)
        if f < 1.0:
            keep = hash01(e['mi'] + wi0, e['mj'] + wj0, seed, 99991 + klassen_idx[e['klasse']]) < f
            for key in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw', 'neig', 'neig_phi'):
                if e[key] is not None:
                    e[key] = e[key][keep]

    # --- Instanzen bauen und schreiben
    ausgabe = os.path.join(basis, regeln['ausgabe']['ordner'], feld)
    os.makedirs(ausgabe, exist_ok=True)
    for f in os.listdir(ausgabe):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    dateien, netz_inst, stat, ebenen_stat = {}, {}, {}, {}
    nk = 0
    for e in ergebnisse:
        n = e['fi'].size
        if n == 0:
            continue
        grund = bilinear(hoehe, e['fi'], e['fj'])
        if e['auf_spiegel']:
            z = bilinear(spiegel, e['fi'], e['fj']) + e['spiegel_versatz'] / 100.0
        else:
            z = grund - e['eingraben'] / 100.0 * e['massstab']
        x = (e['fj'] + wj0 - X0) * 100.0
        y = (e['fi'] + wi0 - Y0) * 100.0
        q = quaternionen(n_x[e['mi'], e['mj']], n_y[e['mi'], e['mj']], n_z[e['mi'], e['mj']], e['kippen'], e['yaw'], e['neig'], e['neig_phi'])
        inst = np.zeros((n, 10), np.float32)
        inst[:, 0], inst[:, 1], inst[:, 2] = x, y, z * 100.0
        inst[:, 3:7] = q
        inst[:, 7] = inst[:, 8] = inst[:, 9] = e['massstab']
        netze = K[e['klasse']]['netze']
        for ni in np.unique(e['netz']):
            m = e['netz'] == ni
            p = netze[int(ni)]
            name = p.rsplit('/', 1)[-1]
            netz_inst.setdefault(name, []).append(inst[m])
            if name not in dateien:
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': e['klasse'], 'rolle': e['ebene'].split(' ', 1)[-1],
                                 'sichtweite': list(e['sichtweite']), 'schatten': e['schatten'], 'kollision': e['kollision'],
                                 'ebene': e['ebene']}
            else:
                d = dateien[name]
                if e['klasse'] != d['gruppe'] and e['klasse'] not in d.get('gruppen', []):
                    d.setdefault('gruppen', [d['gruppe']]).append(e['klasse'])  # Netz von mehreren Klassen genutzt (anderes Eingraben)
                d['kollision'] = d['kollision'] or e['kollision']
                d['schatten'] = d['schatten'] or e['schatten']
                if e['sichtweite'][1] == 0 or (d['sichtweite'][1] != 0 and e['sichtweite'][1] > d['sichtweite'][1]):
                    d['sichtweite'] = list(e['sichtweite'])
            dateien[name]['anzahl'] += int(m.sum())
        stat[e['klasse']] = stat.get(e['klasse'], 0) + n
        ebenen_stat[e['ebene']] = ebenen_stat.get(e['ebene'], 0) + n
        if e['kollision']:
            nk += n
    gesamt = 0
    for name, teile in netz_inst.items():
        arr = np.concatenate(teile, axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]

    # --- Wasserlinsen-Flecken (Punktliste, kein Netz)
    WL = regeln.get('wasserlinsen_flecken', {})
    flecken = []
    if WL and wasser.any():
        t0_, t1_ = WL.get('tiefe_m', [0.0, 0.7])
        rm = int(WL.get('raster_m', 6))
        cand = wasser & (tiefe >= t0_) & (tiefe <= t1_) & (d_w <= float(WL.get('abstand_ufer_max_m', 6.0))) & im_feld & sumpfig
        cand &= (ii_abs % rm == 0) & (jj_abs % rm == 0)
        cand &= hash01(ii_abs, jj_abs, seed, 7001) < float(WL.get('anteil', 0.4))
        ci, cj = np.nonzero(cand)
        r0, r1 = WL.get('radius_m', [2.5, 6.0])
        rr = r0 + (r1 - r0) * hash01(ci + wi0, cj + wj0, seed, 7002)
        mx = int(WL.get('max_je_feld', 400))
        for a in range(min(ci.size, mx)):
            flecken.append([round(float((cj[a] + wj0 - X0) * 100.0), 1), round(float((ci[a] + wi0 - Y0) * 100.0), 1),
                            round(float(spiegel[ci[a], cj[a]] * 100.0), 1), round(float(rr[a] * 100.0), 1)])

    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': int(gesamt), 'dateien': dateien}
    if regeln['ausgabe'].get('entfernen'):
        plan['entfernen'] = regeln['ausgabe']['entfernen']
    plan.update({'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
                 'ebenen': ebenen_stat,
                 'extras': {'wasserlinsen_flecken': flecken,
                            'wasserlinsen_hinweis': 'x,y,z(Spiegel),radius in cm – für Decal/Material-Maske/Niagara; kein Netz im Inventar'},
                 'statistik': {'je_klasse': stat, 'kollision': int(nk), 'biome_anteil': {kk: round(v, 3) for kk, v in bio_anteil.items()},
                               'wasser_anteil_feld': round(wasser_anteil, 4), 'zonen_m2': zstat, 'faktor': faktor,
                               'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA, 'quellen_bestand': quellen},
                 'hinweise': hinweise, 'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet'})
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s: %d Instanzen (%d mit Kollision), %d Netze, %d Wasserlinsen-Flecken, %.1f s' % (feld, gesamt, nk, len(dateien), len(flecken), time.time() - t0))
    for eb in sorted(ebenen_stat):
        meld('  Ebene %-14s %6d' % (eb, ebenen_stat[eb]))
    for h in hinweise:
        meld('  Hinweis:', h)

    if bild:
        try:
            from PIL import Image
        except Exception:
            meld('Pillow fehlt – kein Prüfbild')
            return plan
        farben = regeln.get('bild_farben', {})
        fi0, fi1, fj0, fj1 = fb[0] - wi0, fb[1] - wi0, fb[2] - wj0, fb[3] - wj0
        hh = hoehe[fi0:fi1, fj0:fj1]
        g = np.clip((hh - hh.min()) / max(1e-3, float(hh.max() - hh.min())), 0, 1) * 100 + 80
        rgb = np.stack([g, g, g], axis=2).astype(np.float32)
        zz = zone[fi0:fi1, fj0:fj1]
        sf = sumpfig[fi0:fi1, fj0:fj1]
        for zname, col in (('bult', farben.get('bult')), ('ufer', farben.get('ufer')), ('spiegel', farben.get('spiegel'))):
            if col:
                m = (zz == ZONEN[zname]) & sf
                rgb[m] = 0.45 * rgb[m] + 0.55 * np.array(col, np.float32)
        tt = tiefe[fi0:fi1, fj0:fj1]
        ww = wasser[fi0:fi1, fj0:fj1]
        wc = np.array(farben.get('wasser', [30, 60, 140]), np.float32)
        fc = np.array(farben.get('flachwasser', [60, 120, 170]), np.float32)
        tnorm = np.clip(tt / 1.5, 0, 1)[..., None]
        rgb[ww] = (fc * (1 - tnorm) + wc * tnorm)[ww]
        rgb[weg[fi0:fi1, fj0:fj1]] = farben.get('weg', [120, 80, 40])
        rgb[ort[fi0:fi1, fj0:fj1]] = farben.get('ort', [200, 40, 40])
        for fl in flecken:
            pj = int(round(fl[0] / 100.0 + X0 - wj0)) - fj0
            pi = int(round(fl[1] / 100.0 + Y0 - wi0)) - fi0
            r = max(1, int(round(fl[3] / 100.0)))
            a0, a1 = max(0, pi - r), min(fi1 - fi0, pi + r + 1)
            b0, b1 = max(0, pj - r), min(fj1 - fj0, pj + r + 1)
            if a1 > a0 and b1 > b0:
                rgb[a0:a1, b0:b1] = farben.get('wasserlinse', [120, 255, 60])
        for e in ergebnisse:
            if e['fi'].size == 0:
                continue
            c = farben.get(e['klasse'], [255, 255, 255])
            pi = np.clip(np.round(e['fi']).astype(np.int32) - fi0, 0, fi1 - fi0 - 1)
            pj = np.clip(np.round(e['fj']).astype(np.int32) - fj0, 0, fj1 - fj0 - 1)
            rgb[pi, pj] = c
            if e['ebene'].startswith('2') or e['klasse'] == 'totholz_gross':
                rgb[np.minimum(pi + 1, fi1 - fi0 - 1), pj] = c
                rgb[pi, np.minimum(pj + 1, fj1 - fj0 - 1)] = c
                rgb[np.minimum(pi + 1, fi1 - fi0 - 1), np.minimum(pj + 1, fj1 - fj0 - 1)] = c
        od = os.path.join(basis, regeln['ausgabe']['bild'])
        os.makedirs(od, exist_ok=True)
        Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(os.path.join(od, feld + '.png'))
        meld('Prüfbild: %s' % os.path.join(od, feld + '.png'))
    return plan


def main():
    ap = argparse.ArgumentParser(description='Eldarien Sumpf-Planer (Boden, Mittel, Baum, Wasserkante; Biom sumpf)')
    ap.add_argument('felder', nargs='+', help='Gitterfelder, z. B. H5 I5 H4')
    ap.add_argument('--bild', action='store_true', help='Prüfbild docs/pruefung/sumpf/<Feld>.png schreiben')
    ap.add_argument('--faktor', type=float, default=1.0, help='globaler Dichtefaktor')
    ap.add_argument('--basis', default='.', help='production-Wurzel (enthält export/unreal/welt)')
    ap.add_argument('--regeln', default=None, help='Regeldatei (Standard: sumpf_regeln.json neben dem Skript)')
    args = ap.parse_args()
    regeln = lade_regeln(args.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sumpf_regeln.json'))
    if not NUMBA:
        meld('numba nicht verfügbar – reiner NumPy-Pfad (ausreichend)')
    pruefe_netze(regeln, args.basis)
    felder_bekannt = regeln.get('felder', {})
    for feld in args.felder:
        feld = feld.strip().upper()
        if felder_bekannt and feld not in felder_bekannt:
            meld('Hinweis: %s ist laut biome_je_feld.md kein Sumpffeld (bekannt: %s) – es wird nur geplant, wo eigner.r8 sumpf oder die Nassmaske greift' % (feld, ', '.join(felder_bekannt)))
        try:
            plane_feld(feld, args.basis, regeln, args.faktor, args.bild)
        except SystemExit as e:
            meld('ABBRUCH %s: %s' % (feld, e))
            sys.exit(1)


if __name__ == '__main__':
    main()
