#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien – Planer „Aue/Flussauen“ (Auftrag 11, Teil B2, Biom aue; Velen / Weißgarten / Kovir-Auen).
Eine Ebene `aue` mit vier Schichten: `0 boden` (Laub, Zweige, Kiesel, Pilze, Bodendecker), `1 mittel` (Grasbüschel,
Blumeninseln, Hochstauden, Sträucher, Wegsaum-Hecken, Jungbäume, Farn, Totholz, Stümpfe), `2 baum` (Weiden/Pappeln am
Wasser, Hainbuchen-/Buchen-Haine auf der Terrasse, Kiefern-Gruppen, Solitäre, Totbäume), `5 wasserkante` (Schilfgürtel,
Seggen, Uferstauden, Uferwurzeln). Höhenstufen Ufer → Aue → Terrasse aus Abstand und relativer Höhe zum nächsten Wasser.
Schichten 3 (Fels) und 4 (Spuren) kommen aus felsgruppen_plan.py / spuren_plan.py; Überschreibungen dafür stehen in
aue_regeln.json (`felsgruppen_overrides`, `spuren_overrides`).

Aufruf (lokal, production-Wurzel):
    python -I scripts/aue/aue_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]

Liest:   export/unreal/welt/hoehe.f32 (memmap, nur Fenster Feld + 64 m), lage_*.r8 (optional), karte_wasser/weg/ort.r8,
         eigner.r8 + welt.json (Biom je Zelle, Fallback aue), wasser_welt.json / teiche/teiche.json (Stillwasser-Umrisse,
         optional), bestand/<Feld>/, witcher/<Feld>/ (+ Nachbarn), ufer/foliage_<Feld>/, instanzen/instanzen.json (optional),
         docs/staedte/standorte.json (optional), daten/netze.csv (Pfadprüfung).
Schreibt: export/unreal/welt/aue/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm, qx,qy,qz,qw, sx,sy,sz) + plan.json
          (FORMAT.md §3, je Datei zusätzlich `ebene`), bei --bild docs/pruefung/aue/<Feld>.png (1 px = 1 m).
Regeln:  scripts/aue/aue_regeln.json (neben dem Skript) oder --regeln PFAD.

Nur NumPy-Vektoroperationen (Box-Faltungen, Dilatation, Jump-Flooding-Distanzfeld mit Höhe des nächsten Wassers,
Hash-Zufall aus globaler Rasterkoordinate → deterministisch und nahtlos zu Nachbarfeldern). numba optional, nicht nötig.
Laufzeit-Ziel ≤ 60 s je Feld (Cloud-Rauchtest E5 synthetisch: siehe verteilung-aue.md §4).

Quellen: FORMAT.md §1–§5; antworten/assets-taxonomie.md (Paletten aue); antworten/bildkritik-witcher-messlatte.md
(W6FIN_E5, BACH3_G5: Weiden 20–40 m vom Wasser, Clumping 40–100 m, Büsche 3–7er-Gruppen); antworten/ufer-kies-coast-dunes.md
(Kiesbänke/Treibholz = Ufer-Ebene); GDC 2014 „Landscape Creation and Rendering in REDengine 3“ (Vegetation nach Wasser/Licht);
80.lv „World building of Witcher 3“ (Biom-Pinsel je Geländetyp, Spacing/Scale-Variation); CDPR-Pressemitteilung State of
Unreal 2025 (Nanite Foliage, Kovir). Alle Web-Quellen nur als Suchauszüge gelesen.

UNGETESTET MIT ECHTDATEN – in der Cloud nur mit synthetischen Rastern (E5) rauchgetestet.
"""
import argparse
import csv
import json
import math
import os
import sys
import time

import numpy as np

try:  # numba optional – wird nicht benötigt
    import numba  # noqa: F401
    NUMBA = True
except Exception:  # pragma: no cover
    NUMBA = False

NX, NY = 9577, 7057
FELD_M = 1008
X0, Y0 = 4730.5, 4060.5  # X_cm = (j - 4730.5)*100, Y_cm = (i - 4060.5)*100
WELT = os.path.join('export', 'unreal', 'welt')
BAUM_ROLLEN = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel',
               'palme', 'hainbuche', 'hornbeam', 'poplar', 'willow', 'beech', 'pine')
SCHICHT_KURZ = {'0 boden': 'boden', '1 mittel': 'mittel', '2 baum': 'baum', '5 wasserkante': 'wasserkante'}


# ----------------------------------------------------------------------------- Helfer
def meld(*a):
    print('[aue]', *a, flush=True)


def feld_fenster(feld, rand):
    """'E5' → ((i0,i1,j0,j1) Feld, (wi0,wi1,wj0,wj1) Fenster), beides auf das Raster geklippt (J-Spalte endet bei NX)."""
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise SystemExit('Unbekanntes Feld %r (A1 … J7)' % feld)
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX)
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY)
    wi0, wi1 = max(0, i0 - rand), min(NY, i1 + rand)
    wj0, wj1 = max(0, j0 - rand), min(NX, j1 + rand)
    return (i0, i1, j0, j1), (wi0, wi1, wj0, wj1)


def lade_raster(pfad, dtype, win, pflicht=False):
    """Fenster eines NY×NX-Rasters per memmap (nur das Fenster wird gelesen)."""
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
    """Binäre Dilatation ≈ Kreisscheibe Radius r (Wechsel 4er/8er-Nachbarschaft → Oktagon)."""
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


def distanz_feld(mask, max_m=128.0):
    """Euklidische Distanz (m) zur nächsten True-Zelle und Index (si, sj) dieser Zelle, per Jump-Flooding (Verschiebe-
    Faltung in NumPy). Jenseits max_m: Distanz = 2·max_m, Index −1."""
    H, W = mask.shape
    fern = np.float32(max_m * 2.0)
    ii, jj = np.indices((H, W), dtype=np.int32)
    if not mask.any():
        return np.full((H, W), fern, np.float32), np.full((H, W), -1, np.int32), np.full((H, W), -1, np.int32)
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
                gueltig = csi >= 0
                cd2 = (ii - csi) ** 2 + (jj - csj) ** 2
                besser = gueltig & (cd2 < d2)
                d2 = np.where(besser, cd2, d2)
                si = np.where(besser, csi, si)
                sj = np.where(besser, csj, sj)
    d = np.sqrt(d2.astype(np.float32))
    weit = d2 >= INF
    d[weit] = fern
    d = np.minimum(d, fern).astype(np.float32)
    si[weit | (d >= fern)] = -1
    sj[weit | (d >= fern)] = -1
    return d, si, sj


def hash01(i, j, seed, kanal):
    """Deterministische Zufallszahl [0,1) je (Rasterzeile, Rasterspalte, Seed, Kanal) – global, daher nahtlos."""
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
    """Z-Achse um Anteil `kippen` auf die Geländenormale kippen, davor Zufalls-/Richtungs-Yaw. (n,4) = x,y,z,w."""
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


def polygon_maske(H, W, win, umrisse_cm):
    """Rasterisiert Polygone ([[x_cm, y_cm], …]) ins Fenster (Even-Odd, vektorisiert je Kante)."""
    m = np.zeros((H, W), bool)
    for um in umrisse_cm:
        try:
            pts = np.asarray(um, dtype=np.float64)
            if pts.ndim != 2 or pts.shape[0] < 3:
                continue
            px = pts[:, 0] / 100.0 + X0 - win[2]  # Fensterspalte
            py = pts[:, 1] / 100.0 + Y0 - win[0]  # Fensterzeile
            if px.max() < 0 or px.min() > W or py.max() < 0 or py.min() > H:
                continue
            kreuz = np.zeros((H, W), np.int32)
            rows = np.arange(H, dtype=np.float64) + 0.5
            n = len(px)
            for k in range(n):
                x0, y0, x1, y1 = px[k], py[k], px[(k + 1) % n], py[(k + 1) % n]
                if y0 == y1:
                    continue
                lo, hi = min(y0, y1), max(y0, y1)
                sel = (rows >= lo) & (rows < hi)
                if not sel.any():
                    continue
                xs = x0 + (rows[sel] - y0) * (x1 - x0) / (y1 - y0)
                cols = np.clip(np.ceil(xs).astype(np.int64), 0, W)
                ri = np.flatnonzero(sel)
                ok = cols < W
                np.add.at(kreuz, (ri[ok], cols[ok]), 1)
            m |= (np.cumsum(kreuz, axis=1) % 2) == 1
        except Exception:
            continue
    return m


# ----------------------------------------------------------------------------- Weltdaten
def pruefe_netze(basis, regeln):
    """Alle Netzpfade gegen daten/netze.csv prüfen; fehlende aus den Paletten streichen (mit Meldung)."""
    cp = os.path.join(basis, 'daten', 'netze.csv')
    if not os.path.isfile(cp):
        meld('Hinweis: daten/netze.csv fehlt – Netzpfade werden nicht geprüft')
        return []
    inv = set()
    with open(cp, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter=';'):
            inv.add(r.get('pfad', ''))
    fehlt = []
    for sname, schicht in regeln['schichten'].items():
        for kname, kl in schicht.items():
            ok = [p for p in kl['netze'] if p in inv]
            for p in kl['netze']:
                if p not in inv:
                    fehlt.append('%s/%s: %s' % (sname, kname, p))
            kl['netze'] = ok
    if fehlt:
        meld('WARNUNG: %d Netzpfade nicht im Inventar, gestrichen:' % len(fehlt))
        for f in fehlt:
            meld('   ', f)
    else:
        meld('Netzpfade geprüft: alle im Inventar')
    return fehlt


def lade_biome(basis, win, regeln, feld):
    """True je Zelle, wo Biom = aue; Anteil-Statistik. Fallback aus Regeln (feld_biom_fallback)."""
    fb = regeln.get('feld_biom_fallback', {}).get(feld, 'aue')
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    if eig is None or not os.path.isfile(wj):
        meld('Hinweis: eigner.r8/welt.json fehlen – Biom je Zelle = Fallback %r' % fb)
        return np.full((H, W), fb == 'aue', bool), {fb: 1.0}
    try:
        welt = json.load(open(wj, encoding='utf-8'))
    except Exception as e:
        meld('Hinweis: welt.json unlesbar (%s) – Fallback %r' % (e, fb))
        return np.full((H, W), fb == 'aue', bool), {fb: 1.0}
    kacheln = welt.get('kacheln', {})
    tabelle = np.full(256, 0, np.int16)  # 0 = fallback-Biom, 1 = aue, 2 = anderes
    biome15 = ('aue', 'bergwald', 'gletscher', 'tundra', 'canyon', 'oedland', 'heide', 'elfenwald', 'dschungel', 'kueste',
               'wueste', 'lava', 'frost', 'sumpf', 'fjord')
    namen = np.array(['?'] * 256, dtype=object)
    namen[:] = fb

    def biom_aus_rezept(rz):
        rz = str(rz).lower()
        if rz in biome15:
            return rz
        if 'vulkan' in rz or 'lava' in rz:
            return 'lava'
        for n in biome15:
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
            namen[kk] = biom_aus_rezept(rz) if rz else fb
    namen[0] = 'aue'  # FORMAT §2: 0 = Weltgelände → aue
    ist_aue = (namen == 'aue')[eig]
    vals, cnt = np.unique(eig, return_counts=True)
    ant = {}
    for v, c in zip(vals, cnt):
        ant[namen[v]] = ant.get(namen[v], 0.0) + float(c) / eig.size
    return ist_aue, {k: round(v, 3) for k, v in ant.items()}


def lade_ebene_positionen(ordner, win):
    """Instanzpositionen (Fenster-i, Fenster-j, Maßstab) einer Ebene (plan.json + f32); Bäume und Sonstige getrennt."""
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
            and 'plant' not in txt and 'sapling' not in txt and 'seedling' not in txt and 'leaves' not in txt
        (baum if ist_baum else sonst).append(np.stack([fi[m], fj[m], a[m, 9]], axis=1))
    return baum, sonst


def lade_bestand(basis, feld, win):
    """Bäume aus bestand/, witcher/ (Feld + 8 Nachbarn), instanzen.json; Nicht-Bäume + Ufer-Ebene nur im Feld."""
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    baum, sonst, ufer, quellen = [], [], [], []
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
                sonst += so
            b, so = lade_ebene_positionen(os.path.join(basis, WELT, 'ufer', 'foliage_' + nf), win)
            if b or so:
                quellen.append('ufer/foliage_' + nf)
            ufer += b + so
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
    cat = lambda L: np.concatenate(L, axis=0) if L else np.zeros((0, 3), np.float32)
    return cat(baum), cat(sonst), cat(ufer), quellen


def lade_stillwasser(basis, win, H, W):
    """Maske See-/Teichumrisse aus wasser_welt.json und teiche/teiche.json (optional)."""
    umrisse = []
    for pfad, schl in ((os.path.join(basis, WELT, 'wasser_welt.json'), 'seen'),
                       (os.path.join(basis, WELT, 'teiche', 'teiche.json'), None)):
        if not os.path.isfile(pfad):
            continue
        try:
            d = json.load(open(pfad, encoding='utf-8'))
        except Exception:
            continue
        objs = d.get(schl, []) if schl else (d.get('teiche', d) if isinstance(d, dict) else d)
        if isinstance(objs, dict):
            objs = list(objs.values())
        for o in objs or []:
            if isinstance(o, dict) and 'umriss' in o:
                umrisse.append(o['umriss'])
    if not umrisse:
        return np.zeros((H, W), bool), 0
    return polygon_maske(H, W, win, umrisse), len(umrisse)


def lade_standorte(basis, win, H, W, radius_m):
    """docs/staedte/standorte.json (optional, Format unbekannt): Punkte x/y (cm oder m) + optional radius → Sperrmaske."""
    pfad = os.path.join(basis, 'docs', 'staedte', 'standorte.json')
    m = np.zeros((H, W), bool)
    if not os.path.isfile(pfad):
        return m, 0
    try:
        d = json.load(open(pfad, encoding='utf-8'))
    except Exception:
        return m, 0
    objs = d.get('standorte', d) if isinstance(d, dict) else d
    if isinstance(objs, dict):
        objs = list(objs.values())
    ii, jj = np.indices((H, W), dtype=np.float32)
    n = 0
    for o in objs or []:
        if not isinstance(o, dict):
            continue
        x = o.get('x_cm', o.get('x'))
        y = o.get('y_cm', o.get('y'))
        if x is None or y is None:
            p = o.get('position') or o.get('pos')
            if isinstance(p, (list, tuple)) and len(p) >= 2:
                x, y = p[0], p[1]
            else:
                continue
        try:
            x, y = float(x), float(y)
        except Exception:
            continue
        if 'x_cm' not in o and abs(x) < 20000 and abs(y) < 20000:  # vermutlich Meter
            x, y = x * 100.0, y * 100.0
        r = float(o.get('radius_m', o.get('radius', radius_m)))
        fj = x / 100.0 + X0 - win[2]
        fi = y / 100.0 + Y0 - win[0]
        if fi < -r or fi > H + r or fj < -r or fj > W + r:
            continue
        m |= (ii - fi) ** 2 + (jj - fj) ** 2 <= r * r
        n += 1
    return m, n


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
    gi, gj = ii + wi0, jj + wj0
    im_feld = (gi >= fb[0]) & (gi < fb[1]) & (gj >= fb[2]) & (gj < fb[3])

    # Gelände
    dzdy, dzdx = np.gradient(hoehe)
    hang = np.degrees(np.arctan(np.sqrt(dzdx ** 2 + dzdy ** 2))).astype(np.float32)
    nl = np.sqrt(dzdx ** 2 + dzdy ** 2 + 1.0)
    n_x, n_y, n_z = (-dzdx / nl).astype(np.float32), (-dzdy / nl).astype(np.float32), (1.0 / nl).astype(np.float32)

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
    A = regeln['abstand_m']
    HS = regeln['hoehenstufen']

    # Wasser: Distanz, Höhe des nächsten Wassers, relative Höhe, Stillwasser
    d_wasser, wsi, wsj = distanz_feld(wasser_m, max_m=float(HS['distanz_max_m']))
    hat_wasser = wasser_m.any()
    if hat_wasser:
        nah = wsi >= 0
        h_wasser = np.where(nah, hoehe[np.clip(wsi, 0, H - 1), np.clip(wsj, 0, W - 1)], hoehe)
        hrel = (hoehe - h_wasser).astype(np.float32)
    else:
        hrel = np.full((H, W), 99.0, np.float32)
    SW = regeln['stillwasser']
    still_poly, n_poly = lade_stillwasser(basis, win, H, W)
    if hat_wasser:
        anteil = box_blur(wasser_m.astype(np.float32), int(SW['schmal_fenster_m']))
        still = (still_poly | (anteil < SW['schmal_anteil_max'])) & (d_wasser < 20)
        hinweise.append('Stillwasser: %d Umrisse, %.1f %% der Uferzellen gelten als Altarm/Teich/schmal'
                        % (n_poly, 100.0 * float(still[(d_wasser < 20) & im_feld].mean()) if ((d_wasser < 20) & im_feld).any() else 0.0))
    else:
        still = np.zeros((H, W), bool)
    # Höhenstufen
    lagen_namen = set(HS['ohne_wasser']['aue_lagen']) | set(regeln['feuchte']['lagen']) | set(regeln['licht']['fallback_lagen'])
    lagen_namen |= set(regeln['wuesten_lagen_sperre']['lagen'])
    for sch in regeln['schichten'].values():
        for kl in sch.values():
            lagen_namen |= set(kl.get('lagen_faktor', {}).keys())
    lagen = {}
    for ln in sorted(lagen_namen):
        a = r8('lage_%s.r8' % ln)
        if a is not None:
            lagen[ln] = a.astype(np.float32) / 255.0
    if not lagen:
        hinweise.append('keine lage_*.r8 gefunden – Lagenfaktoren = 1, Feuchte nur aus Wassernähe')
    if hat_wasser:
        ufer = (d_wasser <= HS['ufer_d_max_m']) | ((hrel <= HS['ufer_hrel_max_m']) & (d_wasser <= HS['ufer_d_hrel_max_m']))
        aue = (~ufer) & (hrel <= HS['aue_hrel_max_m']) & (d_wasser <= HS['aue_d_max_m'])
    else:
        ufer = np.zeros((H, W), bool)
        deck = np.zeros((H, W), np.float32)
        for ln in HS['ohne_wasser']['aue_lagen']:
            if ln in lagen:
                deck += lagen[ln]
        aue = deck >= HS['ohne_wasser']['aue_lagen_min']
        hinweise.append('kein Wasser im Fenster – Höhenstufe aue aus Lagen %s' % HS['ohne_wasser']['aue_lagen'])
    ufer &= ~wasser_m
    terrasse = ~(ufer | aue | wasser_m)
    stufe = np.where(ufer, 0, np.where(aue, 1, 2)).astype(np.int8)

    # Sperrflächen
    nah_weg_klein = dilate(weg_m, A['weg_klein']) if weg_m.any() else weg_m
    nah_weg_gross = dilate(weg_m, A['weg_gross']) if weg_m.any() else weg_m
    nah_ort = dilate(ort_m, A['ort']) if ort_m.any() else ort_m
    nah_wasser_klein = dilate(wasser_m, A['wasser_klein']) if hat_wasser else wasser_m
    nah_wasser_gross = dilate(wasser_m, A['wasser_gross']) if hat_wasser else wasser_m
    standort_m, n_st = lade_standorte(basis, win, H, W, A['standort_frei'])
    if n_st:
        hinweise.append('%d Standorte aus docs/staedte/standorte.json freigehalten' % n_st)

    # Biom
    ist_aue, bio_anteil = lade_biome(basis, win, regeln, feld)
    if not ist_aue[im_feld].any():
        hinweise.append('Feld hat keine aue-Zellen – nichts zu planen')
    # Wüstenfelder: nur ergänzen
    feld_faktor = faktor
    if feld in regeln['wuesten_felder']:
        feld_faktor *= regeln['wuesten_feld_faktor']
        WS = regeln['wuesten_lagen_sperre']
        for ln in WS['lagen']:
            if ln in lagen:
                ist_aue &= lagen[ln] < WS['ab_deckung']
        hinweise.append('Wüstenfeld: Faktor %.2f, Sand/Sandstein >= %.1f gesperrt' % (regeln['wuesten_feld_faktor'], WS['ab_deckung']))

    # Bestand: Kronendach, Beschattung, Stammabstände, Ufer-Ebene
    baeume, sonst, uferinst, quellen = lade_bestand(basis, feld, win)
    L = regeln['licht']
    baum_m = np.zeros((H, W), bool)
    if len(baeume):
        bi = np.clip(np.round(baeume[:, 0]).astype(np.int32), 0, H - 1)
        bj = np.clip(np.round(baeume[:, 1]).astype(np.int32), 0, W - 1)
        gew = np.clip(baeume[:, 2], 0.3, 3.0) ** 2
        dichte = np.zeros((H, W), np.float32)
        np.add.at(dichte, (bi, bj), gew.astype(np.float32))
        dichte = gauss_blur(dichte, L['kronen_sigma_m'])
        beschattung = (1.0 - np.exp(-L['beschattung_k'] * math.pi * L['kronen_radius_m'] ** 2 * dichte)).astype(np.float32)
        baum_m[bi, bj] = True
        hinweise.append('Kronendach aus %d Bestandsbäumen (%s)' % (len(baeume), ', '.join(quellen[:6]) + (' …' if len(quellen) > 6 else '')))
    else:
        beschattung = np.zeros((H, W), np.float32)
        for ln, w in L['fallback_lagen'].items():
            if ln in lagen:
                beschattung += w * lagen[ln]
        beschattung = np.clip(gauss_blur(beschattung, 8.0), 0, L['fallback_beschattung_max']).astype(np.float32)
        hinweise.append('keine Baum-Ebene gefunden – Beschattung aus Lagen Laub/Nadeln/Moos geschätzt (max %.2f)' % L['fallback_beschattung_max'])
    nah_baum = dilate(baum_m, A['baumstamm']) if baum_m.any() else baum_m
    nah_baum_neu = dilate(baum_m, A['baum_neu_zu_bestand']) if baum_m.any() else baum_m
    belegt = np.zeros((H, W), bool)
    if len(sonst):
        belegt[np.clip(np.round(sonst[:, 0]).astype(np.int32), 0, H - 1), np.clip(np.round(sonst[:, 1]).astype(np.int32), 0, W - 1)] = True
        belegt = dilate(belegt, A['bestand_sonst'])
    ufer_belegt = np.zeros((H, W), bool)
    kiesbank = np.zeros((H, W), bool)
    if len(uferinst):
        ui = np.clip(np.round(uferinst[:, 0]).astype(np.int32), 0, H - 1)
        uj = np.clip(np.round(uferinst[:, 1]).astype(np.int32), 0, W - 1)
        ufer_belegt[ui, uj] = True
        cnt = np.zeros((H, W), np.float32)
        np.add.at(cnt, (ui, uj), 1.0)
        kiesbank = box_blur(cnt, 3) * 49.0 > 3.0  # > 3 Ufer-Instanzen im 7×7-Fenster
        ufer_belegt = dilate(ufer_belegt, A['ufer_ebene'])
        hinweise.append('Ufer-Ebene FT_EL_UF_*: %d Instanzen berücksichtigt, Kiesbank-Zellen %.1f %% der Uferzone'
                        % (len(uferinst), 100.0 * float(kiesbank[ufer].mean()) if ufer.any() else 0.0))
    else:
        hinweise.append('keine Ufer-Ebene (ufer/foliage_%s) gefunden – Schilf ohne Kiesbank-Dämpfung' % feld)

    # Wald, Saum, Lichtungsrand
    wald = beschattung > L['wald_schwelle']
    kante = wald & dilate(~wald, 1) if wald.any() else np.zeros((H, W), bool)
    d_kante, _, _ = distanz_feld(kante, max_m=64.0)
    saum_norm = np.where(wald, np.clip(1 - d_kante / L['saum_innen_m'], 0, 1), np.clip(1 - d_kante / L['saum_aussen_m'], 0, 1)).astype(np.float32)
    lichtungsrand = (~wald) & (d_kante <= 8.0)

    # Feuchte, Hang, Höhe
    F = regeln['feuchte']
    feuchte = np.clip(1 - d_wasser / F['wasser_radius_m'], 0, 1) * 0.8 if hat_wasser else np.zeros((H, W), np.float32)
    for ln, w in F['lagen'].items():
        if ln in lagen:
            feuchte = feuchte + w * lagen[ln]
    feuchte = np.clip(feuchte, 0, 1).astype(np.float32)
    Hh = regeln['hoehe']
    f_hoehe = np.clip((Hh['null_ab_m'] - hoehe) / max(1.0, Hh['null_ab_m'] - Hh['abnahme_ab_m']), 0, 1).astype(np.float32)
    voll_bis = regeln['hang']['voll_bis_grad']
    # Ort-Nähe (Stümpfe), Weg-Richtung (Hecken), Wegsaum-Band
    d_ort, _, _ = distanz_feld(ort_m, max_m=256.0) if ort_m.any() else (np.full((H, W), 512.0, np.float32), None, None)
    d_weg, _, _ = distanz_feld(weg_m, max_m=64.0) if weg_m.any() else (np.full((H, W), 128.0, np.float32), None, None)
    HW = regeln['hecke_weg']
    if weg_m.any():
        band = (d_weg >= HW['band_m'][0]) & (d_weg <= HW['band_m'][1]) & (d_ort > HW['ort_frei_m'])
        ab = int(HW['abschnitt_m'])
        gate = hash01(gi // ab, gj // ab, regeln['seed'], 777) < HW['abschnitt_anteil']
        hecke_band = band & gate
        gwi, gwj = np.gradient(gauss_blur(d_weg, 2.0))
        weg_yaw = np.arctan2(gwi, gwj) + math.pi / 2  # Tangente (X,Y-Winkel), senkrecht zum Gradienten
    else:
        hecke_band = np.zeros((H, W), bool)
        weg_yaw = np.zeros((H, W), np.float32)
    LI = regeln['lichtung']
    lichtung_gate = hash01(gi // int(LI['fenster_m']), gj // int(LI['fenster_m']), regeln['seed'], 778) >= LI['anteil']
    asp = np.arctan2(-dzdy, -dzdx).astype(np.float32)  # hangabwärts
    if hat_wasser:
        gwi2, gwj2 = np.gradient(gauss_blur(d_wasser, 1.5))
        wasser_yaw = (np.arctan2(gwi2, gwj2) + math.pi / 2).astype(np.float32)
    else:
        wasser_yaw = np.zeros((H, W), np.float32)

    # ------------------------------------------------------------------ Streuung je Schicht und Klasse
    seed = int(regeln['seed'])
    aus = []
    stat = {}
    kidx_all = {}
    for sname, schicht in regeln['schichten'].items():
        for kname, kl in schicht.items():
            kidx_all[kname] = len(kidx_all)
            if not kl['netze']:
                continue
            kidx = kidx_all[kname]
            kanal = 1000 + kidx * 20
            ist_baum = sname == '2 baum'
            gross = ist_baum or kl.get('kollision') or kname in ('strauch', 'hecke_weg', 'jungbaum', 'totholz_klein', 'stumpf')
            # Grunddichte je Höhenstufe
            dj = kl['dichte_je_m2']
            lam = np.where(stufe == 0, dj['ufer'], np.where(stufe == 1, dj['aue'], dj['terrasse'])).astype(np.float32)
            l0, l1 = kl.get('licht', [1.0, 1.0])
            lam *= (l0 * (1 - beschattung) + l1 * beschattung)
            if kl.get('saum', 1.0) != 1.0:
                lam *= 1 + (kl['saum'] - 1) * saum_norm
            if kl.get('lichtungsrand', 1.0) != 1.0:
                lam = np.where(lichtungsrand, lam * kl['lichtungsrand'], lam)
            if 'feuchte' in kl:
                ft, fn = kl['feuchte']
                lam *= ft + (fn - ft) * feuchte
            for ln, w in kl.get('lagen_faktor', {}).items():
                if ln in lagen:
                    lam *= 1 + (w - 1) * lagen[ln]
            SD = regeln.get('sand')
            if SD and SD['lage'] in lagen and kname not in SD.get('ausnahmen', []):
                lam *= 1 - (1 - SD['faktor_bei_voll']) * lagen[SD['lage']]
            hm = kl['hang_max_grad']
            if hm < 60:
                lam *= np.clip((hm - hang) / max(1.0, hm - min(voll_bis, hm - 1)), 0, 1)
            if 'hang_min_grad' in kl:
                lam = np.where(hang >= kl['hang_min_grad'], lam, 0)
            if 'd_wasser_m' in kl:
                a0, a1 = kl['d_wasser_m']
                lam = np.where((d_wasser >= a0) & (d_wasser <= a1), lam, 0)
            if 'stillwasser' in kl:
                lam = np.where(still, lam * kl['stillwasser'], lam)
            if 'kiesbank' in kl and kiesbank.any():
                lam = np.where(kiesbank, lam * kl['kiesbank'], lam)
            if 'ort_nah_faktor' in kl:
                rm, fm = kl['ort_nah_faktor']
                lam = np.where(d_ort <= rm, lam * fm, lam)
            lam *= f_hoehe * feld_faktor
            if ist_baum:
                lam = np.where(hang > regeln['hang']['baum_max_grad'], 0, lam)
            if kl.get('nur_band') == 'hecke_weg':
                lam = np.where(hecke_band, lam, 0)
            if kl.get('lichtung'):
                lam = np.where(lichtung_gate, lam, 0)
            frei = ist_aue & ~belegt & ~nah_ort & ~standort_m & ~ufer_belegt
            frei &= ~(nah_wasser_gross if gross else nah_wasser_klein)
            frei &= ~(nah_weg_gross if gross else nah_weg_klein)
            frei &= ~(nah_baum_neu if ist_baum else nah_baum)
            lam = np.where(frei, lam, 0).astype(np.float32)

            gmin, gmax = kl['gruppe']
            gmit = 0.5 * (gmin + gmax)
            if kl.get('raster') == 'solitaer':
                SO = regeln['solitaer']
                rz = int(SO['raster_m'])
                ci0 = (gi // rz) * rz + np.floor(hash01(gi // rz, gj // rz, seed, kanal + 1) * rz).astype(np.int64)
                cj0 = (gj // rz) * rz + np.floor(hash01(gi // rz, gj // rz, seed, kanal + 2) * rz).astype(np.int64)
                ist_zentrum = (ci0 == gi) & (cj0 == gj) & (hash01(gi // rz, gj // rz, seed, kanal + 3) < SO['p'])
                offen = gauss_blur(beschattung, 10.0) <= SO['beschattung_max']
                frei_s = (dilate(baum_m, SO['frei_radius_m']) == False) if baum_m.any() else np.ones((H, W), bool)
                ist_zentrum &= offen & frei_s & (lam > 0)
                idx = np.flatnonzero(ist_zentrum)
                if idx.size == 0:
                    continue
                ci, cj = ii.ravel()[idx], jj.ravel()[idx]
                fi, fj = ci.astype(np.float32), cj.astype(np.float32)
                mi, mj = ci, cj
            elif gmax <= 1:
                idx = np.flatnonzero(lam > 0)
                if idx.size == 0:
                    continue
                ci, cj = ii.ravel()[idx], jj.ravel()[idx]
                keep = hash01(gi.ravel()[idx], gj.ravel()[idx], seed, kanal) < lam.ravel()[idx]
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
                keep = hash01(gi.ravel()[idx], gj.ravel()[idx], seed, kanal) < lamc.ravel()[idx]
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
                if kl.get('mindestabstand_m') and fi.size:
                    # Mindestabstand innerhalb der Haine: ein Baum je Zelle eines groben Rasters (deterministisch)
                    ma = float(kl['mindestabstand_m'])
                    key = (np.floor(fi / ma).astype(np.int64) + wi0) * 100003 + (np.floor(fj / ma).astype(np.int64) + wj0)
                    _, first = np.unique(key, return_index=True)
                    first = np.sort(first)
                    fi, fj, mi, mj = fi[first], fj[first], mi[first], mj[first]
            if fi.size == 0:
                continue
            ok = im_feld[mi, mj]
            fi, fj, mi, mj = fi[ok], fj[ok], mi[ok], mj[ok]
            if fi.size == 0:
                continue
            gmi, gmj = mi + wi0, mj + wj0
            hv = (hash01(gmi, gmj, seed, kanal + 5) + 0.37 * hash01(np.round(fi * 7).astype(np.int64), np.round(fj * 7).astype(np.int64), seed, kanal + 6)) % 1.0
            netzl = kl['netze']
            nidx = np.minimum((hv * len(netzl)).astype(np.int32), len(netzl) - 1)
            if kl.get('insel_netz_anteil'):
                # Hauptart je Insel: aus der Zelle des Inselzentrums (grob 10 m) abgeleitet, 60 % der Instanzen
                haupt = np.minimum((hash01(gmi // 10, gmj // 10, seed, kanal + 9) * len(netzl)).astype(np.int32), len(netzl) - 1)
                nidx = np.where(hash01(gmi, gmj, seed, kanal + 10) < kl['insel_netz_anteil'], haupt, nidx)
            if kname == 'solitaer' and hat_wasser:
                # Weide als Solitär nur in Wassernähe
                wn = np.array(['willow' in p.lower() for p in netzl])
                nidx = np.where(wn[nidx] & (d_wasser[mi, mj] > 30), 0, nidx)
            ms = kl['massstab'][0] + (kl['massstab'][1] - kl['massstab'][0]) * hash01(gmi, gmj, seed, kanal + 7)
            yaw = hash01(gmi, gmj, seed, kanal + 8) * 2 * math.pi
            ym = kl.get('yaw')
            if ym == 'weg':
                yaw = weg_yaw[mi, mj] + (hash01(gmi, gmj, seed, kanal + 9) - 0.5) * math.radians(30)
            elif ym == 'hang':
                nahw = (d_wasser[mi, mj] < 12) if hat_wasser else np.zeros(mi.size, bool)
                basis_yaw = np.where(nahw, wasser_yaw[mi, mj], asp[mi, mj])
                yaw = basis_yaw + (hash01(gmi, gmj, seed, kanal + 9) - 0.5) * math.radians(40) \
                    + np.where(hash01(gmi, gmj, seed, kanal + 8) < 0.5, 0, math.pi)
            aus.append(dict(fi=fi.astype(np.float32), fj=fj.astype(np.float32), mi=mi, mj=mj, schicht=sname, klasse=kname,
                            netz=nidx.astype(np.int32), massstab=ms.astype(np.float32), yaw=yaw.astype(np.float32),
                            kippen=kl['kippen'], eingraben=kl['eingraben_cm'], eingraben_anteil=kl.get('eingraben_anteil', 0.0),
                            kollision=bool(kl.get('kollision')), schatten=bool(kl.get('schatten', True)),
                            sichtweite=kl['sichtweite'], netze=netzl))
            stat[kname] = stat.get(kname, 0) + int(fi.size)

    # ------------------------------------------------------------------ Budget
    Bg = regeln['budget']
    gesamt = sum(stat.values())
    koll = sum(int(a['fi'].size) for a in aus if a['kollision'])
    ausduenn = {}
    if koll > Bg['kollision_je_feld']:
        f = Bg['kollision_je_feld'] / float(koll)
        for a in aus:
            if a['kollision']:
                ausduenn[a['klasse']] = min(ausduenn.get(a['klasse'], 1.0), f)
        hinweise.append('Kollisionsbudget: %d → %d (Faktor %.2f auf alle Kollisionsklassen)' % (koll, Bg['kollision_je_feld'], f))
    ziel_s = Bg.get('ziel_je_schicht', {})
    for sname in regeln['schichten']:
        n_s = sum(stat.get(a['klasse'], 0) for a in aus if a['schicht'] == sname)
        z = ziel_s.get(sname)
        if z and n_s > z:
            f = z / float(n_s)
            for a in aus:
                if a['schicht'] == sname:
                    ausduenn[a['klasse']] = min(ausduenn.get(a['klasse'], 1.0), f)
            hinweise.append('Schichtbudget %s: %d → %d (Faktor %.2f)' % (sname, n_s, z, f))
    gesamt2 = sum(stat.get(a['klasse'], 0) * ausduenn.get(a['klasse'], 1.0) for a in aus)
    if gesamt2 > Bg['ziel_instanzen_je_feld']:
        ueber = gesamt2 - Bg['ziel_instanzen_je_feld']
        pool, summe = [], 0
        for kname in Bg['prioritaet_ausduennen']:
            n = stat.get(kname, 0) * ausduenn.get(kname, 1.0)
            if n == 0:
                continue
            pool.append(kname)
            summe += n
            if summe * 0.5 >= ueber:
                break
        f = max(0.0, 1.0 - ueber / float(max(1, summe)))
        for kname in pool:
            ausduenn[kname] = ausduenn.get(kname, 1.0) * f
        hinweise.append('Instanzbudget: %d → Ziel %d, Ausdünnung %s' % (int(gesamt2), Bg['ziel_instanzen_je_feld'], {k: round(v, 2) for k, v in ausduenn.items()}))
    for a in aus:
        f = ausduenn.get(a['klasse'], 1.0)
        if f < 1.0:
            keep = hash01(a['mi'] + wi0, a['mj'] + wj0, seed, 99991 + kidx_all[a['klasse']]) < f
            for key in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw'):
                a[key] = a[key][keep]

    # ------------------------------------------------------------------ Instanzen schreiben
    ausgabe = os.path.join(basis, regeln['ausgabe']['ordner'], feld)
    os.makedirs(ausgabe, exist_ok=True)
    for f in os.listdir(ausgabe):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    dateien, netz_inst, stat, stat_s = {}, {}, {}, {}
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
        for ni in np.unique(a['netz']):
            m = a['netz'] == ni
            p = a['netze'][ni]
            name = p.rsplit('/', 1)[-1]
            if a['eingraben_anteil'] > 0:
                inst[m, 2] -= a['eingraben_anteil'] * NETZ_HOEHE.get(p, 0.5) * 100.0 * a['massstab'][m]
            netz_inst.setdefault(name, []).append(inst[m])
            if name not in dateien:
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': a['klasse'], 'rolle': 'baum' if a['schicht'] == '2 baum' else a['klasse'],
                                 'sichtweite': list(a['sichtweite']), 'schatten': a['schatten'], 'kollision': a['kollision'],
                                 'ebene': SCHICHT_KURZ.get(a['schicht'], a['schicht'])}
            dateien[name]['anzahl'] += int(m.sum())
        stat[a['klasse']] = stat.get(a['klasse'], 0) + n
        stat_s[a['schicht']] = stat_s.get(a['schicht'], 0) + n
        if a['kollision']:
            nk += n
    gesamt = 0
    for name, teile in netz_inst.items():
        arr = np.concatenate(teile, axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]
    land = im_feld & ~wasser_m
    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': int(gesamt), 'dateien': dateien,
            'entfernen': regeln.get('entfernen', ''), 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'statistik': {'je_klasse': stat, 'je_schicht': stat_s, 'kollision': int(nk), 'biome_anteil': bio_anteil,
                          'aue_anteil_feld': round(float(ist_aue[im_feld].mean()), 3),
                          'hoehenstufen_anteil': {'ufer': round(float(ufer[land].mean()), 3) if land.any() else 0,
                                                  'aue': round(float(aue[land].mean()), 3) if land.any() else 0,
                                                  'terrasse': round(float(terrasse[land].mean()), 3) if land.any() else 0},
                          'wasser_anteil': round(float(wasser_m[im_feld].mean()), 3),
                          'beschattung_mittel': round(float(beschattung[im_feld].mean()), 3),
                          'faktor': faktor, 'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA},
            'hinweise': hinweise, 'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten (E5) rauchgetestet'}
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s: %d Instanzen (%d mit Kollision), %d Netze, %s, %.1f s' % (feld, gesamt, nk, len(dateien),
         ', '.join('%s %d' % (SCHICHT_KURZ.get(k, k), v) for k, v in sorted(stat_s.items())), time.time() - t0))
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
        g = np.clip((hh - hh.min()) / max(1e-3, float(hh.max() - hh.min())), 0, 1) * 90 + 90
        rgb = np.stack([g, g, g], axis=2)
        st = stufe[fi0:fi1, fj0:fj1]
        rgb[st == 0] *= np.array([0.75, 0.9, 1.0])
        rgb[st == 1] *= np.array([0.85, 1.0, 0.8])
        rgb[st == 2] *= np.array([1.0, 0.95, 0.8])
        b = beschattung[fi0:fi1, fj0:fj1]
        rgb[..., 0] *= (1 - 0.4 * b)
        rgb[..., 2] *= (1 - 0.4 * b)
        rgb[~ist_aue[fi0:fi1, fj0:fj1]] *= 0.6
        rgb[wasser_m[fi0:fi1, fj0:fj1]] = (40, 80, 200)
        rgb[still[fi0:fi1, fj0:fj1] & wasser_m[fi0:fi1, fj0:fj1]] = (60, 140, 200)
        rgb[weg_m[fi0:fi1, fj0:fj1]] = (120, 80, 40)
        rgb[ort_m[fi0:fi1, fj0:fj1]] = (200, 40, 40)
        farben = regeln.get('bild_farben', {})
        for a in aus:
            if a['fi'].size == 0:
                continue
            c = farben.get(a['klasse'], [255, 255, 255])
            pi = np.clip(np.round(a['fi']).astype(np.int32) - fi0, 0, fi1 - fi0 - 1)
            pj = np.clip(np.round(a['fj']).astype(np.int32) - fj0, 0, fj1 - fj0 - 1)
            rgb[pi, pj] = c
            if a['schicht'] == '2 baum' or a['kollision']:
                for di, dj in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    rgb[np.clip(pi + di, 0, fi1 - fi0 - 1), np.clip(pj + dj, 0, fj1 - fj0 - 1)] = c
        od = os.path.join(basis, regeln['ausgabe']['bild'])
        os.makedirs(od, exist_ok=True)
        Image.fromarray(rgb.astype(np.uint8)).save(os.path.join(od, feld + '.png'))
        meld('Prüfbild: %s' % os.path.join(od, feld + '.png'))
    return plan


NETZ_HOEHE = {}


def lade_netzhoehen(basis):
    """Netzhöhe (m) aus daten/netze.csv für das anteilige Eingraben liegender Stämme."""
    cp = os.path.join(basis, 'daten', 'netze.csv')
    if not os.path.isfile(cp):
        return
    with open(cp, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter=';'):
            try:
                NETZ_HOEHE[r['pfad']] = float(r['groesse_z_m'])
            except Exception:
                pass


def main():
    ap = argparse.ArgumentParser(description='Eldarien Aue-Planer (Boden, Mittelschicht, Auwald, Wasserkante)')
    ap.add_argument('felder', nargs='+')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    a = ap.parse_args()
    rp = a.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aue_regeln.json')
    if not os.path.isfile(rp):
        raise SystemExit('Regeldatei fehlt: %s' % rp)
    regeln = json.load(open(rp, encoding='utf-8'))
    if not NUMBA:
        meld('numba nicht verfügbar – reiner NumPy-Pfad (ausreichend)')
    if not os.path.isdir(os.path.join(a.basis, WELT)):
        raise SystemExit('Weltdaten fehlen: %s (Aufruf aus der production-Wurzel oder --basis PFAD)' % os.path.join(a.basis, WELT))
    pruefe_netze(a.basis, regeln)
    lade_netzhoehen(a.basis)
    for feld in a.felder:
        plane_feld(feld.strip().upper(), a.basis, regeln, a.faktor, a.bild)


if __name__ == '__main__':
    main()
