#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien – Planer „Spuren von Leben“ (Schicht 4), Korrektur Runde 1 (10.10.2026): Zäune und Trockenmauern um Feldstreifen und am Ortsrand, Obstgärten,
Steinmänner (Kuppen, Pässe, Wegmarken), Wegkreuze/Schreine, verlassene Karren, Fischerstege an flachen Seeufern,
Holzschlag-Lichtungen, Köhlerplätze (Meiler), Friedhöfe und Einzelgräber, Rauchsäulen-Punkte für Partikel, Blickziel-Vorschläge.

Aufruf (lokal, production-Wurzel):
    python -I scripts/spuren/spuren_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]

Liest:   export/unreal/welt/hoehe.f32 (memmap, Fenster Feld + 64 m), karte_ort.r8 (Orte = Zusammenhangskomponenten → Mittelpunkt,
         Radius), karte_weg.r8 (Wege, Tangente aus Distanzfeld), karte_wasser.r8 (Seen = Wasserkomponenten ≥ 2 500 m² und ≥ 15 m breit),
         lage_*.r8 (optional), eigner.r8 + welt.json (Biom), bestand/<Feld>/, witcher/<Feld>/, instanzen/instanzen.json (Kronendach).
Schreibt: export/unreal/welt/spuren/<Feld>/<Netzname>.f32 + plan.json (FORMAT.md §3; Großobjekte zusätzlich als akteur_<Netzname>.f32
          mit rolle akteur und Liste `akteure` (Konvention wie felsgruppen_plan.py), `punkte` für Rauchsäulen, `flaechen` für Feldstreifen/Meilerplätze (Lagen-Vorschlag), `blickziele`),
          bei --bild docs/pruefung/spuren/<Feld>.png (1 px = 1 m).
Regeln:  scripts/spuren/spuren_regeln.json (neben dem Skript) oder --regeln PFAD.

Nur NumPy (Jump-Flooding-Distanzfeld mit Seed-Rückgabe, Komponenten-Beschriftung auf 4-m-Raster, Hash-Zufall je Rasterzelle).
numba wird nicht benötigt. Laufzeit-Ziel ≤ 60 s je Feld.

Quellen: FORMAT.md; antworten/strassen-splines-bruecken.md (Frage 4: Straße zuerst, Dorf als Restfläche, Felder/Zäune per Spline-Sampling);
Electric Dreams „Spline → Bounds → Difference“ (Wald um Pfad/Dorf freischneiden); 80.lv/GameBanshee Witcher-3-Interviews
(Orte nach Einwohnerzahl, keine Rasterplatzierung, Wege führen zu Blickzielen); Naturschutzbund „Waldränder“.

Korrektur Runde 1 (verteilung-KONVENTIONEN.md): Querschnitts-Planer, biome_eigen = alle 15 Biome; Biom je Zelle strikt aus
eigner.r8 + welt.json (0 = Weltgelände → aue, Vulkanregion → lava), nur ohne eigner.r8 dominantes Feldbiom aus
daten/biome_je_feld.json; plan.json mit biome_fenster, zellen_zustaendig, biome_eigen, kollision_anzahl, dateien[].ebene = 4;
Landanteil im Fenster < 2 % → leerer plan.json; Budget 60 000 / 3 000 Kollision (inkl. Akteure) mit WARNUNG im Log;
keine Instanz auf Wasser/Weg/Ort (Ausnahme: Steg-Planken/-Pfosten über Wasser); Kronendach zusätzlich aus den
Baum-Dateien (ebene 2) der Biom-Planer-Ebenen; Logs nur ASCII; fehlende Pflichtdatei → Exit-Code 2.

Echtdaten-Lauf der Vorfassung lokal (A5 51, G4 591, E1 55, C6 393 Instanzen); diese Fassung in der Cloud nur synthetisch rauchgetestet.
"""
import argparse
import json
import math
import os
import sys
import time
import copy
import zlib

import numpy as np

try:  # numba optional (nicht benötigt)
    import numba  # noqa: F401
    NUMBA = True
except Exception:  # pragma: no cover
    NUMBA = False

NX, NY = 9577, 7057
FELD_M = 1008
X0, Y0 = 4730.5, 4060.5
WELT = os.path.join('export', 'unreal', 'welt')
SKRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EBENE = 4  # Schicht 4 spuren
BIOME15 = ['aue', 'bergwald', 'gletscher', 'tundra', 'canyon', 'oedland', 'heide', 'elfenwald', 'dschungel', 'kueste',
           'wueste', 'lava', 'frost', 'sumpf', 'fjord']
BIOM_EBENEN = ('nordkueste', 'aue', 'heide_tundra', 'hochgebirge', 'elfenwald', 'sumpf', 'dschungel', 'lava', 'wueste_ergaenzung')
BAUM_ROLLEN = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel', 'palme', 'hainbuche',
               'tanne', 'pine', 'beech', 'palm', 'oak', 'birch', 'spruce', 'fir_', 'willow', 'poplar', 'hornbeam')
TOT_WORTE = ('tot', 'dead', 'stump', 'stumpf', 'log', 'verkohlt', 'fallen', 'schnag', 'branch', 'ast_', 'root', 'wurzel')
NADEL_BIOME = ('bergwald', 'fjord', 'kueste', 'tundra', 'gletscher', 'frost', 'lava')
_ASCII = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss', '→': '->', '←': '<-', '…': '...',
          '≤': '<=', '≥': '>=', '–': '-', '—': '-', '²': '2', '³': '3', '°': ' Grad', '×': 'x', '·': '*', '„': '"',
          '“': '"', '”': '"', '‚': "'", '‘': "'", '’': "'", '±': '+/-', '≈': '~', 'µ': 'u', '−': '-', '§': 'Par.'}


def asc(s):
    """Text auf ASCII abbilden (Logs werden unter Windows mit cp1252 weiterverarbeitet, KONVENTIONEN §5)."""
    s = str(s)
    for k, v in _ASCII.items():
        s = s.replace(k, v)
    return s.encode('ascii', 'replace').decode('ascii')


def meld(*a):
    print(asc(' '.join(['[spuren]'] + [str(x) for x in a])), flush=True)


def abbruch(text):
    """Pflichtdatei/Regelfehler: klare Meldung, Exit-Code 2."""
    meld('FEHLER: ' + str(text))
    sys.exit(2)


# ----------------------------------------------------------------------------- Raster-Helfer (wie mittelschicht_plan.py)
def feld_fenster(feld, rand):
    feld = feld.strip().upper()
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        abbruch('Unbekanntes Feld %r (A1 ... J7)' % feld)
    j0, j1 = s * FELD_M, (s + 1) * FELD_M
    i0, i1 = (r - 1) * FELD_M, r * FELD_M
    return (i0, min(i1, NY), j0, min(j1, NX)), (max(0, i0 - rand), min(NY, i1 + rand), max(0, j0 - rand), min(NX, j1 + rand))


def lade_raster(pfad, dtype, win, pflicht=False):
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            abbruch('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        meld('WARNUNG: %s hat %d Werte, erwartet %d – ignoriert' % (pfad, n, NX * NY))
        if pflicht:
            abbruch('Pflichtdatei hat falsche Groesse: %s' % pfad)
        return None
    return np.array(np.memmap(pfad, dtype=dtype, mode='r', shape=(NY, NX))[wi0:wi1, wj0:wj1])


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


def max_filter(a, r):
    """Gleitendes Maximum über Fenster (2r+1)² durch Verdopplungs-Schritte (separierbar, exakt; Rand wird geklippt)."""
    out = a.astype(np.float32)
    L = 2 * r + 1
    for achse in (0, 1):
        pad = ((r, r), (0, 0)) if achse == 0 else ((0, 0), (r, r))
        m = np.pad(out, pad, mode='constant', constant_values=-np.inf)

        def sh(x, k):
            return verschiebe(x, k, 0, np.float32(-np.inf)) if achse == 0 else verschiebe(x, 0, k, np.float32(-np.inf))
        s = 1
        while s * 2 <= L:
            m = np.maximum(m, sh(m, s))  # m[i] = max a[i .. i+2s-1]
            s *= 2
        res = np.maximum(m, sh(m, L - s))  # res[i] = max über [i, i+L) im gepolsterten Array = [i-r, i+r] im Original
        out = res[:out.shape[0], :] if achse == 0 else res[:, :out.shape[1]]
    return out


def distanz(mask, max_m=64.0, seeds=False):
    """Euklidische Distanz (m) zur nächsten True-Zelle (Jump-Flooding); optional Index (si, sj) der nächsten Zelle."""
    H, W = mask.shape
    fern = np.float32(max_m * 2.0)
    ii, jj = np.indices((H, W), dtype=np.int32)
    if not mask.any():
        d = np.full((H, W), fern, np.float32)
        return (d, np.full((H, W), -1, np.int32), np.full((H, W), -1, np.int32)) if seeds else d
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
                cd2 = (ii - csi) ** 2 + (jj - csj) ** 2
                besser = (csi >= 0) & (cd2 < d2)
                d2 = np.where(besser, cd2, d2)
                si = np.where(besser, csi, si)
                sj = np.where(besser, csj, sj)
    d = np.sqrt(d2.astype(np.float32))
    d[d2 >= INF] = fern
    d = np.minimum(d, fern).astype(np.float32)
    return (d, si, sj) if seeds else d


def hash01(i, j, seed, kanal):
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


def h1(i, j, seed, kanal):
    """Skalarer Hash."""
    return float(hash01(np.array([i]), np.array([j]), seed, kanal)[0])


def bilinear(h, fi, fj):
    H, W = h.shape
    fi = np.clip(np.asarray(fi, np.float32), 0, H - 1.001)
    fj = np.clip(np.asarray(fj, np.float32), 0, W - 1.001)
    i0 = fi.astype(np.int32)
    j0 = fj.astype(np.int32)
    ti = fi - i0
    tj = fj - j0
    return ((h[i0, j0] * (1 - ti) + h[i0 + 1, j0] * ti) * (1 - tj) + (h[i0, j0 + 1] * (1 - ti) + h[i0 + 1, j0 + 1] * ti) * tj)


def quat_mul(a, b):
    ax, ay, az, aw = a.T
    bx, by, bz, bw = b.T
    return np.stack([aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
                     aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz], axis=1)


def quaternionen(nx, ny, nz, kippen, yaw, roll=None):
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
    if roll is not None:  # Zusatzneigung um die Objekt-Längsachse (X) – umgekippte Karren, schiefe Kreuze
        qr = np.stack([np.sin(roll / 2), np.zeros(n, np.float32), np.zeros(n, np.float32), np.cos(roll / 2)], axis=1)
        q = quat_mul(q, qr)
    return (q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-9)).astype(np.float32)


def komponenten(mask):
    """Zusammenhangskomponenten (4er-Nachbarschaft) durch Min-Label-Ausbreitung. Rückgabe: Label-Array (0 = keine)."""
    H, W = mask.shape
    lab = np.where(mask, np.arange(1, H * W + 1, dtype=np.int32).reshape(H, W), 0).astype(np.int32)
    for _ in range(4 * max(H, W)):
        neu = lab.copy()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c = verschiebe(lab, di, dj, np.int32(0))
            neu = np.where(mask & (c > 0) & (c < neu), c, neu)
        if np.array_equal(neu, lab):
            break
        lab = neu
    _, inv = np.unique(lab, return_inverse=True)
    inv = inv.reshape(H, W).astype(np.int32)
    inv[~mask] = 0
    return inv


def wahl_je_raster(mask, score, raster, ii, jj):
    """Je Rasterzelle (raster m) die Zelle mit kleinstem score innerhalb mask. Rückgabe: Indizes (i, j) Arrays."""
    idx = np.flatnonzero(mask)
    if idx.size == 0:
        return np.zeros(0, np.int32), np.zeros(0, np.int32)
    ci, cj = ii.ravel()[idx], jj.ravel()[idx]
    zelle = (ci // raster) * 100000 + (cj // raster)
    sc = score.ravel()[idx]
    o = np.lexsort((sc, zelle))
    zelle_s = zelle[o]
    erster = np.concatenate([[True], zelle_s[1:] != zelle_s[:-1]])
    sel = o[erster]
    return ci[sel], cj[sel]


# ----------------------------------------------------------------------------- Weltdaten
def feld_dominantes_biom(basis, feld, regeln):
    """Dominantes Biom des Feldes aus daten/biome_je_feld.json (felder[FELD].biome_prozent), sonst Regel-Tabelle, sonst aue."""
    for p in (os.path.join(basis, 'daten', 'biome_je_feld.json'), os.path.join(SKRIPT_DIR, 'biome_je_feld.json'),
              os.path.join(SKRIPT_DIR, '..', '..', 'daten', 'biome_je_feld.json'),
              os.path.join(SKRIPT_DIR, '..', '..', 'vorlagen', 'daten', 'biome_je_feld.json')):
        if not os.path.isfile(p):
            continue
        try:
            bp = json.load(open(p, encoding='utf-8'))['felder'][feld]['biome_prozent']
            b = str(sorted(bp, key=lambda e: -float(e[1]))[0][0]).lower()
            if b in BIOME15:
                return b, 'biome_je_feld.json'
        except Exception:
            continue
    fb = regeln.get('feld_biom_fallback', {}).get(feld)
    if fb in BIOME15:
        return fb, 'Regeln feld_biom_fallback'
    return 'aue', 'Vorgabe aue'


def biom_aus_rezept(rz):
    """welt.json-Rezept → Biomname (exakt, Vulkan/Lava → lava, Teilwort); None wenn unbekannt."""
    rz = str(rz).strip().lower()
    if rz in BIOME15:
        return rz
    if 'vulkan' in rz or 'lava' in rz:
        return 'lava'
    for n in sorted(BIOME15, key=len, reverse=True):
        if n in rz:
            return n
    return None


def lade_biome(basis, win, regeln, feld, hinweise):
    """Biom-Index (in BIOME15) je Fensterzelle (KONVENTIONEN §1): eigner.r8 + welt.json, Kennzahl 0 = Weltgelände → aue.
    Nur wenn eigner.r8 fehlt: dominantes Feldbiom (biome_je_feld.json) für alle Zellen."""
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    if eig is None:
        fb, q = feld_dominantes_biom(basis, feld, regeln)
        hinweise.append('eigner.r8 fehlt - Biom je Zelle = dominantes Feldbiom %s (%s)' % (fb, q))
        return np.full((H, W), BIOME15.index(fb), np.int16), 'Fallback ' + fb
    tabelle = np.full(256, -1, np.int16)
    tabelle[0] = BIOME15.index('aue')
    wj = os.path.join(basis, WELT, 'welt.json')
    kacheln = {}
    if os.path.isfile(wj):
        try:
            kacheln = json.load(open(wj, encoding='utf-8')).get('kacheln', {})
        except Exception as e:
            hinweise.append('welt.json unlesbar (%s) - nur Kennzahl 0 (aue) bekannt' % e)
    else:
        hinweise.append('welt.json fehlt - nur Kennzahl 0 (aue) bekannt')
    eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
    for k, v in eintraege:
        try:
            kk = int(v.get('kennzahl', v.get('id', k))) if isinstance(v, dict) else int(k)
        except Exception:
            continue
        if 1 <= kk < 256:
            b = biom_aus_rezept(v.get('rezept', '') if isinstance(v, dict) else v)
            if b is not None:
                tabelle[kk] = BIOME15.index(b)
    bio = tabelle[eig]
    unbek = bio < 0
    if unbek.any():
        fb, q = feld_dominantes_biom(basis, feld, regeln)
        kz = sorted(int(x) for x in np.unique(eig[unbek]))[:12]
        hinweise.append('WARNUNG: %d Zellen mit unbekanntem Rezept (Kennzahlen %s) -> dominantes Feldbiom %s (%s)' % (int(unbek.sum()), kz, fb, q))
        bio = np.where(unbek, BIOME15.index(fb), bio)
    return bio.astype(np.int16), 'eigner.r8 + welt.json'


def ebene_art(info, name):
    """'baum' (Kronendach), 'boden' oder 'sonst' aus dateien[].ebene/schicht bzw. rolle/gruppe/Name."""
    txt = (str(info.get('rolle', '')) + ' ' + str(info.get('gruppe', '')) + ' ' + str(info.get('klasse', '')) + ' ' + name).lower()
    e = str(info.get('ebene', info.get('schicht', ''))).lower().strip()
    if e.startswith('2') or 'baum' in e:
        art = 'baum'
    elif e:
        return 'sonst'
    else:
        art = 'baum' if any(r in txt for r in BAUM_ROLLEN) else 'sonst'
    return 'sonst' if any(t in txt for t in TOT_WORTE) else art


def lade_baeume(basis, feld, win):
    """Baum-Positionen (Fenster-i, Fenster-j) aus bestand/, witcher/ (Feld + Nachbarn) und instanzen/."""
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    H, W = win[1] - win[0], win[3] - win[2]
    teile = []

    def lies(f, ist_baum):
        if not ist_baum:
            return
        try:
            a = np.fromfile(f, dtype='<f4')
        except Exception:
            return
        if a.size == 0 or a.size % 10:
            return
        a = a.reshape(-1, 10)
        fj = a[:, 0] / 100.0 + X0 - win[2]
        fi = a[:, 1] / 100.0 + Y0 - win[0]
        m = (fi >= 0) & (fi < H) & (fj >= 0) & (fj < W)
        if m.any():
            teile.append(np.stack([fi[m], fj[m]], axis=1))
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(ord('A') + ss) + str(rr)
            for ebene in ('bestand', 'witcher') + BIOM_EBENEN:  # Biom-Planer: nur Dateien mit ebene 2 (Baum)
                ordner = os.path.join(basis, WELT, ebene, nf)
                pj = os.path.join(ordner, 'plan.json')
                if not os.path.isfile(pj):
                    continue
                try:
                    plan = json.load(open(pj, encoding='utf-8'))
                except Exception:
                    continue
                for name, info in (plan.get('dateien') or {}).items():
                    f = os.path.join(ordner, name + '.f32')
                    if isinstance(info, dict) and os.path.isfile(f):
                        lies(f, ebene_art(info, name) == 'baum')
    ij = os.path.join(basis, WELT, 'instanzen', 'instanzen.json')
    if os.path.isfile(ij):
        try:
            for e in json.load(open(ij, encoding='utf-8')).get('verzeichnis', []):
                f = os.path.join(basis, WELT, 'instanzen', e.get('datei') or (str(e.get('name', '')) + '.f32'))
                txt = (str(e.get('klasse', '')) + ' ' + str(e.get('name', ''))).lower()
                if os.path.isfile(f):
                    lies(f, any(k in txt for k in BAUM_ROLLEN) and not any(t in txt for t in TOT_WORTE))
        except Exception:
            pass
    return np.concatenate(teile, axis=0) if teile else np.zeros((0, 2), np.float32)


# ----------------------------------------------------------------------------- Instanz-Sammler
class Sammler:
    """Sammelt Instanzen je Netz; baut am Ende f32-Arrays, plan.json-Einträge und Akteurliste."""

    def __init__(self, hoehe, nx, ny, nz, win, im_feld, sperre_land, sperre_wasser, sperre_weg):
        self.h, self.nx, self.ny, self.nz, self.win, self.im_feld = hoehe, nx, ny, nz, win, im_feld
        self.sperre_land = sperre_land      # Wasser | Weg | Ort: hier steht nie eine Instanz
        self.sperre_wasser = sperre_wasser  # Weg | Ort: für Steg-Teile/Pfähle, die bewusst im Wasser stehen
        self.sperre_weg = sperre_weg        # Wasser | Ort: für den Knüppeldamm, der bewusst auf dem Weg liegt
        self.H, self.W = hoehe.shape
        self.rows = []
        self.akteure = []
        self.gesperrt = 0

    def add(self, pfade, fi, fj, gruppe, kollision=True, sichtweite=(0, 45000), massstab=1.0, yaw=None, kippen=0.3,
            eingraben_cm=5.0, z_offset_m=None, roll=None, akteur=False, netz_wahl=None, seed=0, kanal=0, nur_feld=True, z_abs_m=None,
            auf_wasser=False, auf_weg=False):
        fi = np.asarray(fi, np.float32).ravel()
        fj = np.asarray(fj, np.float32).ravel()
        n = fi.size
        if n == 0:
            return 0
        mi = np.clip(np.round(fi).astype(np.int32), 0, self.H - 1)
        mj = np.clip(np.round(fj).astype(np.int32), 0, self.W - 1)
        ok = (fi >= 0) & (fi < self.H) & (fj >= 0) & (fj < self.W)
        if nur_feld:
            ok &= self.im_feld[mi, mj]
        frei = ~(self.sperre_wasser if auf_wasser else (self.sperre_weg if auf_weg else self.sperre_land))[mi, mj]
        self.gesperrt += int((ok & ~frei).sum())
        ok &= frei
        if not ok.any():
            return 0

        def arr(v, dflt=None):
            if v is None:
                return None if dflt is None else np.full(n, dflt, np.float32)
            v = np.asarray(v, np.float32)
            return np.full(n, float(v), np.float32) if v.ndim == 0 else v.ravel()
        ms = arr(massstab)
        gi, gj = mi + self.win[0], mj + self.win[2]
        yw = arr(yaw) if yaw is not None else hash01(gi, gj, seed, kanal + 1) * 2 * math.pi
        rl = arr(roll)
        zo = arr(z_offset_m, 0.0)
        if z_abs_m is None:
            z = bilinear(self.h, fi, fj) - float(eingraben_cm) / 100.0 + zo
        else:
            z = arr(z_abs_m) + zo
        q = quaternionen(self.nx[mi, mj], self.ny[mi, mj], self.nz[mi, mj], float(kippen), yw, rl)
        if netz_wahl is None:
            netz_wahl = np.minimum((hash01(gi, gj, seed, kanal + 2) * len(pfade)).astype(np.int32), len(pfade) - 1)
        netz_wahl = np.asarray(netz_wahl).ravel()
        inst = np.zeros((n, 10), np.float32)
        inst[:, 0] = (fj + self.win[2] - X0) * 100.0
        inst[:, 1] = (fi + self.win[0] - Y0) * 100.0
        inst[:, 2] = z * 100.0
        inst[:, 3:7] = q
        inst[:, 7] = inst[:, 8] = inst[:, 9] = ms
        for k in np.unique(netz_wahl[ok]):
            m = ok & (netz_wahl == k)
            p = pfade[int(k)]
            # Akteure in eigene Dateien akteur_<Netz>.f32 (Konvention wie felsgruppen_plan.py), damit ein Setzer sie nicht als Foliage setzt
            self.rows.append(dict(pfad=p, name=('akteur_' if akteur else '') + p.rsplit('/', 1)[-1], inst=inst[m], gruppe=gruppe, kollision=bool(kollision),
                                  sichtweite=list(sichtweite), akteur=bool(akteur), fi=fi[m], fj=fj[m]))
            if akteur:
                for row in inst[m]:
                    self.akteure.append({'netz': p.rsplit('/', 1)[-1], 'pfad': p, 'gruppe': gruppe, 'rolle': 'akteur',
                                         'x': round(float(row[0]), 1), 'y': round(float(row[1]), 1), 'z': round(float(row[2]), 1),
                                         'q': [round(float(v), 5) for v in row[3:7]], 's': round(float(row[7]), 3)})
        return int(ok.sum())

    def budget(self, max_inst, max_koll, seed, prio, hinweise):
        """Deckel je Feld (FORMAT.md §3): erst Gesamtzahl, dann Kollision. Gedünnt wird deterministisch (Hash je Instanz)
        in der Reihenfolge `prio` (unwichtigste Gruppe zuerst), je Runde höchstens 60 % einer Gruppe; Akteure bleiben."""
        koll_je_name = {}
        for r in self.rows:
            koll_je_name.setdefault(r['name'], set()).add(bool(r['kollision']))
        for r in self.rows:  # Netz mit und ohne Kollision genutzt → eigene Datei/Foliage-Typ <Netz>_ohne_koll (keine Vereinigung)
            if len(koll_je_name[r['name']]) == 2 and not r['kollision'] and not r['akteur']:
                r['name'] = r['name'] + '_ohne_koll'

        def zaehle(nur_koll):
            return sum(int(r['inst'].shape[0]) for r in self.rows if not r['akteur'] and (r['kollision'] or not nur_koll))

        def duenne(gruppe, faktor, kanal):
            for r in self.rows:
                if r['gruppe'] != gruppe or r['akteur']:
                    continue
                gi = np.round(r['fi'] * 4).astype(np.int64) + self.win[0]
                gj = np.round(r['fj'] * 4).astype(np.int64) + self.win[2]
                keep = hash01(gi, gj, seed, kanal) < faktor
                r['inst'], r['fi'], r['fj'] = r['inst'][keep], r['fi'][keep], r['fj'][keep]
        n_akt = sum(int(r['inst'].shape[0]) for r in self.rows if r['akteur'])
        n_akt_k = sum(int(r['inst'].shape[0]) for r in self.rows if r['akteur'] and r['kollision'])
        # Akteure werden nie gedünnt, zählen aber in den Deckel (instanzen / kollision_anzahl im plan.json)
        extra = sorted({r['gruppe'] for r in self.rows} - set(prio))  # Zusatz-/Sonderformen ohne Eintrag: früh dünnen
        prio = list(prio[:1]) + extra + list(prio[1:])
        for nur_koll, deckel, txt in ((False, max_inst - n_akt, 'Instanzbudget'), (True, max_koll - n_akt_k, 'Kollisionsbudget')):
            ist = zaehle(nur_koll)
            if ist <= deckel:
                continue
            vorher, runde = ist, 0
            while ist > deckel and runde < 12:
                runde += 1
                for g in prio:
                    n = sum(int(r['inst'].shape[0]) for r in self.rows if r['gruppe'] == g and not r['akteur'] and (r['kollision'] or not nur_koll))
                    if n == 0:
                        continue
                    f = max(0.4, 1.0 - (ist - deckel) / float(n))
                    duenne(g, f, 9000 + runde * 50 + prio.index(g))
                    ist = zaehle(nur_koll)
                    if ist <= deckel:
                        break
            hinweise.append('WARNUNG %s: %d -> %d (Deckel ohne Akteure %d), gedünnt in Reihenfolge %s' % (txt, vorher, ist, deckel, ', '.join(prio)))
        self.rows = [r for r in self.rows if r['inst'].shape[0] > 0]

    def schreibe(self, ordner):
        os.makedirs(ordner, exist_ok=True)
        for f in os.listdir(ordner):
            if f.endswith('.f32'):
                os.remove(os.path.join(ordner, f))
        dateien, gesamt, koll, je_gruppe = {}, 0, 0, {}
        by = {}
        for r in self.rows:
            by.setdefault(r['name'], []).append(r)
        for name, rs in by.items():
            arr = np.concatenate([r['inst'] for r in rs], axis=0).astype('<f4')
            arr.tofile(os.path.join(ordner, name + '.f32'))
            r0 = rs[0]
            koll_n = any(r['kollision'] for r in rs)
            dateien[name] = {'pfad': r0['pfad'], 'anzahl': int(arr.shape[0]), 'gruppe': '+'.join(sorted({r['gruppe'] for r in rs})),
                             'rolle': 'akteur' if r0['akteur'] else 'spuren', 'sichtweite': [min(r['sichtweite'][0] for r in rs), 0 if any(r['sichtweite'][1] == 0 for r in rs) else max(r['sichtweite'][1] for r in rs)],
                             'schatten': True, 'kollision': koll_n, 'ebene': EBENE}
            gesamt += arr.shape[0]
            if koll_n:  # kollision_anzahl zählt alle Instanzen mit Kollision, Akteure eingeschlossen
                koll += arr.shape[0]
            for r in rs:
                je_gruppe[r['gruppe']] = je_gruppe.get(r['gruppe'], 0) + int(r['inst'].shape[0])
        return dateien, gesamt, koll, je_gruppe


# ----------------------------------------------------------------------------- Geometrie-Bausteine
def linie_punkte(p0, p1, schritt):
    """Punkte entlang der Strecke p0→p1 (Fensterkoordinaten i,j) mit Abstand `schritt`, Mittelpunkte der Segmente. Rückgabe fi, fj, yaw."""
    p0 = np.asarray(p0, np.float32)
    p1 = np.asarray(p1, np.float32)
    L = float(np.linalg.norm(p1 - p0))
    n = int(L // schritt)
    if n == 0:
        return np.zeros(0, np.float32), np.zeros(0, np.float32), 0.0
    t = (np.arange(n, dtype=np.float32) + 0.5) * schritt / L
    pts = p0[None, :] + t[:, None] * (p1 - p0)[None, :]
    yaw = math.atan2(float(p1[0] - p0[0]), float(p1[1] - p0[1]))  # Richtung (Y=i, X=j) → atan2(dy, dx)
    return pts[:, 0], pts[:, 1], yaw


def rechteck_ecken(ci, cj, a, b, winkel):
    """Vier Ecken (i, j) eines Rechtecks (a entlang Winkel, b quer) um (ci, cj)."""
    c, s = math.cos(winkel), math.sin(winkel)
    ex = np.array([s, c]) * a / 2  # Richtung entlang winkel in (i, j): (sin, cos)
    ey = np.array([-c, s]) * b / 2
    ctr = np.array([ci, cj])
    return [ctr - ex - ey, ctr + ex - ey, ctr + ex + ey, ctr - ex + ey]


def rechteck_frei(ecken, erlaubt, H, W, n=7):
    """Prüft Rechteck auf n×n Stützpunkten gegen Maske `erlaubt`."""
    p0, p1, p2, p3 = ecken
    t = np.linspace(0.05, 0.95, n)
    u, v = np.meshgrid(t, t)
    pts = p0[None, :] + u.ravel()[:, None] * (p1 - p0)[None, :] + v.ravel()[:, None] * (p3 - p0)[None, :]
    i = np.round(pts[:, 0]).astype(np.int32)
    j = np.round(pts[:, 1]).astype(np.int32)
    if (i < 0).any() or (j < 0).any() or (i >= H).any() or (j >= W).any():
        return False
    return bool(erlaubt[i, j].all())


def ecken_welt(ecken, win):
    return [[round(float((e[1] + win[2] - X0) * 100), 1), round(float((e[0] + win[0] - Y0) * 100), 1)] for e in ecken]


# ----------------------------------------------------------------------------- Spuren-Overrides der Biom-Planer
BIOM_PLANER_VORGABE = {'fjord': 'nordkueste', 'kueste': 'nordkueste', 'bergwald': 'nordkueste', 'aue': 'aue',
                       'heide': 'heide_tundra', 'tundra': 'heide_tundra', 'gletscher': 'hochgebirge', 'frost': 'hochgebirge',
                       'elfenwald': 'elfenwald', 'sumpf': 'sumpf', 'dschungel': 'dschungel', 'lava': 'lava',
                       'wueste': 'wueste_ergaenzung', 'canyon': 'wueste_ergaenzung', 'oedland': 'wueste_ergaenzung'}
SEKTIONEN = ('ort', 'feldstreifen', 'obstgarten', 'zaun_weg', 'mauer', 'steinmann', 'wegkreuz', 'karren', 'steg', 'holzschlag',
             'koehler', 'graeber', 'rauch', 'blickziele')
# Override-Gruppenname → Tor (Objekt-Entscheidung im Planer)
TOR_ALIAS = {'feldstreifen': 'feld', 'feld': 'feld', 'obstgarten': 'obstgarten', 'obstbaum': 'obstgarten', 'zaun_weg': 'zaun_weg',
             'zaun': 'zaun', 'zaun_holz': 'zaun', 'mauer': 'mauer', 'mauer_stein': 'mauer', 'steinmann': 'steinmann',
             'wegkreuz': 'wegkreuz', 'kreuz': 'wegkreuz', 'schrein': 'schrein', 'saeule': 'schrein', 'karren': 'karren',
             'steg': 'steg', 'holzschlag': 'holzschlag', 'koehler': 'koehler', 'grab': 'grab', 'graeber': 'grab',
             'graeber_friedhof': 'friedhof', 'friedhof': 'friedhof', 'rauch': 'rauch', 'brunnen': 'brunnen',
             'kopfweiden_reihe': 'kopfweiden', 'pferch': 'pferch', 'steinkreis': 'steinkreis', 'ruine': 'ruine',
             'tempelruine': 'ruine', 'mauerrest': 'ruine', 'galgen_ersatz': 'galgen', 'pfaehle': 'pfaehle',
             'knueppeldamm': 'knueppeldamm', 'opferstaette': 'opferstaette', 'schwefelgrube': 'schwefelgrube',
             'hecke_am_feldrand': 'hecke', 'muehle': 'muehle', 'huegelgrab': 'huegelgrab'}
# Palette-Schlüssel → Netzschlüssel in spuren_regeln.json["netze"] (Listen = mehrere Ziele)
PALETTE_ALIAS = {'holzschlag_stumpf': ['stumpf_nadel', 'stumpf_laub'], 'obstbaum': ['obstbaum'], 'obstgarten': ['obstbaum'],
                 'stein': ['mauer_stein'], 'zaun': ['zaun_holz']}
# Netzlisten innerhalb einer Sektion → Netzschlüssel
SEKTION_NETZE = {('steinmann', 'netze'): 'steinmann', ('steinmann', 'netze_zusatz'): '+steinmann', ('karren', 'netze'): 'karren',
                 ('karren', 'beiwerk_netze'): 'karren_beiwerk', ('mauer', 'steine'): 'mauer_stein', ('steg', 'pfahl_netze'): 'steg_pfosten',
                 ('steg', 'planken_netze'): 'steg_planke', ('wegkreuz', 'schrein_netz'): 'saeule', ('obstgarten', 'netze_aue'): 'obstbaum',
                 ('obstgarten', 'netze'): 'obstbaum', ('graeber', 'netze'): 'huegelgrab'}
SONDERFORMEN = ('kopfweiden_reihe', 'pferch', 'steinkreis', 'ruine', 'tempelruine', 'galgen_ersatz', 'brunnen', 'pfaehle',
                'knueppeldamm', 'opferstaette', 'schwefelgrube', 'schrein', 'zusatzklassen')
NICHT_UMGESETZT = {'muehle': 'keine Netze geliefert (netze leer)', 'boot': 'keine Netze geliefert', 'laternen': 'keine Netze geliefert',
                   'steinbruecke': 'keine Netze geliefert', 'knochen': 'keine Netze geliefert', 'gipfelkreuz': 'netz null (Einkaufsliste)',
                   'unterstand': 'netz null', 'seilbruecke_steg': 'netz null', 'verkohlte_huette': 'leerer Block', 'elfenpfad': 'leerer Block',
                   'tempelpfad': 'Steinplatten auf dem Weg = Boden/Felsgruppen', 'torfstich': 'Hoehenpass/Decal im Editor, keine Instanzen',
                   'huette': 'keine Netze geliefert', 'gletscherzunge_regel': 'Blickziel-Regel (nicht in spuren)',
                   'totbaum_solitaer': 'Blickziel-Sonderform (sumpf) nicht umgesetzt', 'pfahlbau_ruine': 'Blickziel-Sonderform nicht umgesetzt'}
# Zählparameter, die ein Faktor > 1 skaliert (Faktor < 1 wirkt als deterministische Ausdünnung je Objekt)
FAKTOR_PARAMETER = {'steinmann': [('steinmann', 'frei_je_km2', 1), ('steinmann', 'weg_schritt_m', -1)],
                    'karren': [('karren', 'je_km_weg', 1)], 'grab': [('graeber', 'einzel_je_km_weg', 1)],
                    'steg': [('steg', 'max_je_feld', 1)], 'holzschlag': [('holzschlag', 'max_je_feld', 1)],
                    'koehler': [('koehler', 'max_je_feld', 1)], 'feld': [('feldstreifen', 'anteil_zellen', 1), ('feldstreifen', 'max_je_ort', 1)],
                    'wegkreuz': [('wegkreuz', 'schritt_m', -1)], 'zaun_weg': [('zaun_weg', 'je_ort', 1)],
                    'obstgarten': [('obstgarten', 'max_je_ort', 1)]}


DOKU_TEXT = ('lage', 'regel', 'bedingung', 'stelle', 'umsetzung', 'limits', 'kandidat_zwischenloesung')
SPEZIAL_ZUSATZ = {'knueppeldamm': ('auf_weg', 'nur_nass', 'schritt_m', 'breite_m', 'yaw', 'eingraben_cm', 'jitter_cm', 'max_laenge_m_je_feld'),
                  'pfaehle': ('neigung_grad', 'eingraben_cm', 'je_km_ufer', 'radius_m', 'tiefe_max_m', 'zone')}


def doku_schluessel(k):
    k = str(k)
    return k.startswith('_') or k.startswith('herkunft') or k.endswith(('doku', 'hinweis', 'begruendung', 'quelle_text')) or k in DOKU_TEXT


def lade_inventar(basis):
    """daten/netze.csv → ({pfad: Netzhöhe m oder None}, csv-Pfad); (None, None) ohne Inventar."""
    kandidaten = [os.path.join(basis, 'daten', 'netze.csv'), os.path.join(SKRIPT_DIR, 'netze.csv'),
                  os.path.join(SKRIPT_DIR, '..', '..', 'daten', 'netze.csv')]
    csv = next((p for p in kandidaten if os.path.isfile(p)), None)
    if csv is None:
        return None, None
    inv = {}
    with open(csv, encoding='utf-8', errors='replace') as f:
        kopf = f.readline().rstrip('\n').split(';')
        sp = kopf.index('pfad') if 'pfad' in kopf else 0
        sz = kopf.index('groesse_z_m') if 'groesse_z_m' in kopf else -1
        for zeile in f:
            t = zeile.rstrip('\n').split(';')
            if len(t) > sp:
                z = None
                if 0 <= sz < len(t):
                    try:
                        z = float(t[sz])
                    except ValueError:
                        z = None
                inv[t[sp].strip()] = z
    return inv, csv


class Pfade:
    """Netzpfade aus Overrides gegen das Inventar auflösen (voller /Game-Pfad oder eindeutige Endung wie 'AncientRuins/Meshes/SM_Column_02')."""

    def __init__(self, inventar):
        self.inv = inventar
        self.je_name = {}
        for p in (inventar or {}):
            self.je_name.setdefault(p.rsplit('/', 1)[-1].lower(), []).append(p)

    def __call__(self, p):
        if not isinstance(p, str) or not p.strip():
            return None
        p = p.strip()
        if self.inv is None:
            return p if p.startswith('/Game/') else None
        if p in self.inv:
            return p
        kand = [q for q in self.je_name.get(p.rsplit('/', 1)[-1].lower(), []) if q.lower().endswith('/' + p.lstrip('/').lower())]
        return kand[0] if len(kand) == 1 else None

    def liste(self, pf, fehlt):
        out = []
        for p in (pf if isinstance(pf, list) else [pf]):
            q = self(p)
            if q:
                out.append(q)
            elif isinstance(p, str):
                fehlt.add(p)
        return out


def lade_spuren_overrides(regeln, regel_pfad):
    """spuren_overrides der Biom-Planer: {thema: (block, pfad)}, Zuordnung Biom → Thema, Hinweise."""
    zuordnung = dict(BIOM_PLANER_VORGABE)
    zuordnung.update(regeln.get('biom_planer', {}))
    ordner = os.path.dirname(os.path.abspath(regel_pfad))
    ov, hinw = {}, []
    for thema in sorted(set(zuordnung.values())):
        biome = sorted(b for b, t in zuordnung.items() if t == thema)
        kand = [os.path.join(ordner, thema + '_regeln.json'), os.path.join(ordner, '..', thema, thema + '_regeln.json')]
        p = next((x for x in kand if os.path.isfile(x)), None)
        if p is None:
            hinw.append('Override: %s_regeln.json nicht gefunden - eigene Werte fuer %s' % (thema, ', '.join(biome)))
            continue
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            hinw.append('Override: %s unlesbar (%s) - eigene Werte fuer %s' % (os.path.basename(p), e, ', '.join(biome)))
            continue
        blk = d.get('spuren_overrides')
        if not isinstance(blk, dict) or not [k for k in blk if not doku_schluessel(k)]:
            hinw.append('Override: %s ohne Block spuren_overrides - eigene Werte fuer %s' % (os.path.basename(p), ', '.join(biome)))
            continue
        ov[thema] = (blk, p)
    return ov, zuordnung, hinw


def _merge(ziel, quelle):
    for k, v in quelle.items():
        if doku_schluessel(k):
            continue
        if isinstance(v, dict) and isinstance(ziel.get(k), dict):
            _merge(ziel[k], v)
        else:
            ziel[k] = copy.deepcopy(v)


def spuren_aufloesen(R, blk, thema, biom, feld, pfade, info):
    """Regeln für ein Biom nach dem Override-Block (Overrides gewinnen). Rückgabe RB (mit RB['_tor'] = Faktoren je Tor und
    RB['_extra'] = Sonderformen) oder None, wenn der Block in diesem Feld nicht gilt (z. B. dschungel 'felder')."""
    if feld is not None and isinstance(blk.get('felder'), list) and feld not in blk['felder']:
        info['nicht_in_feld'] = True
        return None
    RB = copy.deepcopy(R)
    RB['_extra'], tor = {}, {}
    N = RB['netze']
    fehlt = set()

    def um(k):
        info.setdefault('umgesetzt', set()).add(k)

    def nu(k, grund):
        info.setdefault('nicht_umgesetzt', {})[k] = grund

    def unb(k):
        info.setdefault('unbekannte_schluessel', set()).add(k)

    def netz_setzen(ziel, liste):
        liste = pfade.liste(liste, fehlt)
        if not liste:
            return
        if ziel.startswith('+'):
            N[ziel[1:]] = list(dict.fromkeys(N.get(ziel[1:], []) + liste))
        elif ziel == 'obstbaum':
            N['obstbaum'] = dict(N.get('obstbaum', {}))
            N['obstbaum'][biom] = liste
        else:
            N[ziel] = liste

    teile = [blk]
    if isinstance(blk.get(biom), dict):
        teile.append(blk[biom])
    if isinstance((blk.get('je_biom') or {}).get(biom), dict):
        teile.append(blk['je_biom'][biom])
    for t in teile:
        for k, v in t.items():
            if doku_schluessel(k) or k in ('biom', 'gilt_fuer', 'felder', 'je_biom') or k in BIOME15:
                if k in BIOME15 or k in ('felder', 'je_biom'):
                    um(k)
                continue
            if k == 'aus' and isinstance(v, list):
                for g in v:
                    if g in TOR_ALIAS:
                        tor[TOR_ALIAS[g]] = 0.0
                    else:
                        unb('aus.' + str(g))
                um(k)
            elif k == 'verbote' and isinstance(v, dict):
                for g in (v.get(biom) or []):
                    if g in TOR_ALIAS:
                        tor[TOR_ALIAS[g]] = 0.0
                    else:
                        nu('verbote.' + str(g), 'kein eigenes Tor (Variante einer Spur)')
                um(k)
            elif k == 'faktor' and isinstance(v, dict):
                if v and all(isinstance(x, dict) for x in v.values()):
                    v = v.get(biom, {})
                for g, f in v.items():
                    if not isinstance(f, (int, float)):
                        continue
                    if g in TOR_ALIAS:
                        tor[TOR_ALIAS[g]] = float(f)
                    elif g in ('zaun_latten', 'zaun_pfahl'):
                        nu('faktor.' + g, 'Teilnetz des Zauns; Netzwahl über palette')
                    else:
                        unb('faktor.' + str(g))
                um(k)
            elif k == 'palette' and isinstance(v, dict):
                for nk, pf in v.items():
                    if nk in ('hecke_am_feldrand', 'kopfweiden_reihe'):
                        RB['_extra'].setdefault(nk, {})['netze'] = pfade.liste(pf, fehlt)
                    elif nk in N or nk in PALETTE_ALIAS:
                        for ziel in PALETTE_ALIAS.get(nk, [nk]):
                            netz_setzen(ziel, pf)
                    else:
                        unb('palette.' + str(nk))
                um(k)
            elif k == 'zusatzklassen' and isinstance(v, dict):
                allg = {}
                for zn, kd in v.items():
                    if not isinstance(kd, dict):
                        continue
                    if kd.get('aktiv') is False:
                        nu('zusatzklassen.' + str(zn), 'aktiv: false')
                        continue
                    if not kd.get('palette') and not kd.get('netze'):
                        nu('zusatzklassen.' + str(zn), 'palette fehlt (Pflicht nach KONVENTIONEN Par. 6)')
                        continue
                    bekannt = set(SCHEMA6) | {'netze', 'radius_m', 'farbe', 'aktiv'} | set(SPEZIAL_ZUSATZ.get(zn, ()))
                    for zk in kd:
                        if zk not in bekannt and not doku_schluessel(zk):
                            unb('zusatzklassen.%s.%s' % (zn, zk))
                    if zn in SPEZIAL_ZUSATZ:  # Sumpf-Spurtypen mit eigener Logik (Knüppeldamm auf dem Weg, Pfähle am Ufer)
                        sv = copy.deepcopy(kd)
                        sv['netze'] = pfade.liste(kd.get('palette') or kd.get('netze'), fehlt)
                        RB['_extra'][zn] = sv
                    else:
                        allg[zn] = copy.deepcopy(kd)
                if allg:
                    RB['_extra']['zusatzklassen'] = allg
                um(k)
            elif k == 'parameter' and isinstance(v, dict):
                for sek, sv in v.items():
                    if sek in SEKTIONEN and isinstance(sv, dict):
                        _sektion(RB, sek, sv, biom, tor, netz_setzen, um, nu, unb)
                    elif not doku_schluessel(sek):
                        unb('parameter.' + str(sek))
                um(k)
            elif k == 'blickziele_typ' and isinstance(v, dict):
                RB['blickziele'].setdefault('typ_je_biom', {}).update(copy.deepcopy(v))
                um(k)
            elif k == 'wueste_felder_faktor' and isinstance(v, (int, float)):
                RB['wuesten_feld_faktor'] = float(v)
                um(k)
            elif k == 'feldstreifen_verlassen' and isinstance(v, dict):
                if v.get('aktiv', True) and biom in (v.get('biome') or [biom]):
                    Fs = RB['feldstreifen']
                    Fs['anteil_frucht'] = 0.0
                    if 'zaun_lueckenanteil' in v:
                        Fs['zaun_lueckenanteil'] = v['zaun_lueckenanteil']
                    if isinstance(v.get('zaun_kippen_grad'), list):
                        Fs['zaun_kippen_grad'] = max(v['zaun_kippen_grad'])
                    if v.get('stoppel_netze'):
                        netz_setzen('stoppel', v['stoppel_netze'])
                um(k)
            elif k == 'blickziele' and isinstance(v, list):
                RB['blickziele'].setdefault('typ_je_biom', {})[biom] = [str(x).split(' ')[0] for x in v]
                um(k)
            elif k in SEKTIONEN and isinstance(v, dict):
                _sektion(RB, k, v, biom, tor, netz_setzen, um, nu, unb)
            elif k in SONDERFORMEN and isinstance(v, dict):
                sv = copy.deepcopy(v)
                for nk in ('netze', 'netze_foliage', 'netze_akteur', 'steinkreis_netze', 'netze_ersatz'):
                    if nk in sv:
                        sv[nk] = pfade.liste(sv[nk], fehlt)
                for nk in ('saeule', 'netz'):
                    if isinstance(sv.get(nk), str):
                        sv[nk] = pfade(sv[nk])
                for bk, bv in list((sv.get('beiwerk') or {}).items()) if isinstance(sv.get('beiwerk'), dict) else []:
                    sv['beiwerk'][bk] = pfade(bv) if isinstance(bv, str) else pfade.liste(bv, fehlt)
                for bk in ('bewuchs', 'beigaben'):
                    if isinstance(sv.get(bk), dict):
                        for nk, nv in sv[bk].items():
                            if isinstance(nv, list) and nv and isinstance(nv[0], str):
                                sv[bk][nk] = pfade.liste(nv, fehlt)
                if 'bauteile' in sv and isinstance(sv['bauteile'], list):
                    for bt in sv['bauteile']:
                        if isinstance(bt, dict):
                            bt['netz'] = pfade(bt.get('netz'))
                for kk, vv in (RB['_extra'].get(k) or {}).items():  # Netze aus palette bleiben erhalten
                    if kk not in sv or not sv[kk]:
                        sv[kk] = vv
                RB['_extra'][k] = sv
                um(k)
            elif k in NICHT_UMGESETZT:
                nu(k, NICHT_UMGESETZT[k])
            else:
                unb(str(k))
    h = RB['_extra'].get('hecke_am_feldrand')
    if h and 'netze_roh' in h:
        if not h.get('netze'):
            h['netze'] = pfade.liste(h['netze_roh'], fehlt)
        del h['netze_roh']
    if fehlt:
        info.setdefault('netze_verworfen', set()).update(fehlt)
    if 'steinmann' in RB['_extra'] or any('steinmann' in t for t in teile):
        if biom not in RB['steinmann']['biome']:
            RB['steinmann']['biome'] = list(RB['steinmann']['biome']) + [biom]
    for gt, f in tor.items():  # Faktor > 1 skaliert Zählparameter, Faktor < 1 dünnt je Objekt
        if f > 1.0:
            for sek, sk, rich in FAKTOR_PARAMETER.get(gt, []):
                w = RB.get(sek, {}).get(sk)
                if isinstance(w, (int, float)):
                    RB[sek][sk] = w * f if rich > 0 else w / f
                elif isinstance(w, list) and all(isinstance(x, (int, float)) for x in w):
                    RB[sek][sk] = [x * f if rich > 0 else x / f for x in w]
            if gt not in FAKTOR_PARAMETER:
                info.setdefault('faktor_gt1_ohne_wirkung', set()).add(gt)
    if isinstance(RB['feldstreifen'].get('anteil_zellen'), (int, float)):
        RB['feldstreifen']['anteil_zellen'] = min(1.0, RB['feldstreifen']['anteil_zellen'])
    for sek, sk in (('feldstreifen', 'max_je_ort'), ('feldstreifen', 'max_je_feld'), ('steg', 'max_je_feld'), ('holzschlag', 'max_je_feld'),
                    ('koehler', 'max_je_feld'), ('obstgarten', 'max_je_ort')):
        if isinstance(RB[sek].get(sk), float):
            RB[sek][sk] = int(round(RB[sek][sk]))
    zw = RB['zaun_weg'].get('je_ort')
    if isinstance(zw, (int, float)):
        RB['zaun_weg']['je_ort'] = [int(zw), int(zw)]
    elif isinstance(zw, list):
        RB['zaun_weg']['je_ort'] = [int(round(x)) for x in zw]
    RB['_tor'] = tor
    return RB


def _sektion(RB, sek, v, biom, tor, netz_setzen, um, nu, unb):
    """Eine Sektion des Overrides (Name wie in spuren_regeln.json) in RB einmischen."""
    S = RB[sek]
    for sk, sv in v.items():
        if doku_schluessel(sk):
            continue
        name = '%s.%s' % (sek, sk)
        if sk == 'faktor' and isinstance(sv, (int, float)):
            tor[TOR_ALIAS.get(sek, sek)] = float(sv)
        elif (sek, sk) in SEKTION_NETZE:
            if sek == 'graeber':
                continue  # Hügelgrab unten
            netz_setzen(SEKTION_NETZE[(sek, sk)], sv)
        elif sek == 'steinmann' and sk == 'biome_zusatz' and isinstance(sv, list):
            S['biome'] = list(dict.fromkeys(list(S['biome']) + sv))
        elif sek == 'steinmann' and sk == 'steine_je_mann':
            S['steine'] = sv
        elif sek == 'steinmann' and sk == 'je_feld' and isinstance(sv, list):
            S['frei_je_km2'] = 0.5 * (sv[0] + sv[1])
        elif sk == 'je_feld' and 'max_je_feld' in S:
            S['max_je_feld'] = sv[1] if isinstance(sv, list) else sv
        elif sek == 'feldstreifen' and sk == 'hecke_am_feldrand' and isinstance(sv, dict):
            RB['_extra'].setdefault('hecke_am_feldrand', {}).update({k: x for k, x in sv.items() if k != 'netze'})
            if sv.get('netze'):
                RB['_extra']['hecke_am_feldrand']['netze_roh'] = sv['netze']
        elif sek == 'mauer' and sk in ('je_km2', 'verlauf', 'luecken_anteil', 'flechten'):
            RB['_extra'].setdefault('freie_mauern', {})[sk] = sv
        elif sek == 'zaun_weg' and sk == 'material':
            S['material'] = sv
        elif sek == 'graeber' and sk in ('art', 'radius_m', 'stuecke', 'lage', 'je_feld'):
            RB['_extra'].setdefault('huegelgrab', {})[sk] = sv
            if sk == 'art':
                tor['friedhof'] = 0.0
        elif sek == 'rauch' and sk in ('quelle', 'typ'):
            RB['_extra'].setdefault('rauch_quelle', {})[sk] = sv
        elif sek == 'steg' and sk == 'nur_stillwasser':
            pass  # Stege stehen ohnehin nur an Seen (Wasserkomponenten >= see_min_m2)
        elif sek == 'blickziele':
            if sk.startswith('typ_je_biom') and isinstance(sv, (dict, list)):
                tj = RB['blickziele'].setdefault('typ_je_biom', {})
                if isinstance(sv, dict):
                    tj.update(copy.deepcopy(sv))
                else:
                    tj[biom] = list(sv)
            elif isinstance(sv, (int, float, list)) and sk in S:
                S[sk] = sv
            else:
                nu(name, 'Blickziel-Sonderform nicht umgesetzt')
                continue
        elif sk in S:
            if isinstance(sv, dict) and isinstance(S[sk], dict):
                _merge(S[sk], sv)
            else:
                S[sk] = copy.deepcopy(sv)
        else:
            unb(name)
            continue
    if sek == 'graeber' and 'huegelgrab' in RB['_extra'] and v.get('netze'):
        netz_setzen('huegelgrab', v['netze'])
    if sek == 'blickziele' and isinstance(v, list):
        RB['blickziele'].setdefault('typ_je_biom', {})[biom] = v
    um(sek)


SCHEMA6 = ('palette', 'rolle', 'dichte_je_ha', 'hang_grad', 'hoehe_m', 'wasser_abstand_m', 'lagen_min', 'kruemmung', 'massstab',
           'eingraben_anteil', 'gruppe', 'kollision', 'sichtweite', 'akteur')


class Zone:
    """Zuständigkeit eines Biom-Overrides: Zellen des Bioms (Anteil 1) plus 30-m-Saum (Anteil linear auf 0). Je Zelle bilden
    die Zonen eine Zerlegung von [0, 1); eine Objekt-Verankerung gehört der Zone, in deren Intervall ihr Zell-Hash U fällt."""

    def __init__(self, name, R, lo, hi, U, seed, win, thema=None, biom=None):
        self.name, self.R, self.lo, self.hi, self.U, self.seed, self.win = name, R, lo, hi, U, seed, win
        self.thema, self.biom = thema, biom
        self.tor = R.get('_tor', {})
        self.extra = R.get('_extra', {})
        self.maske = hi > lo
        self.anteil = (hi - lo).astype(np.float32)
        self.H, self.W = U.shape

    def _ij(self, a, b):
        return min(self.H - 1, max(0, int(round(float(a))))), min(self.W - 1, max(0, int(round(float(b)))))

    def drin(self, a, b):
        a, b = self._ij(a, b)
        return bool(self.lo[a, b] <= self.U[a, b] < self.hi[a, b])

    def tor_faktor(self, tor):
        return float(self.tor.get(tor, 1.0))

    def gate(self, tor, a, b):
        """Objekt bei (a, b) setzen? Zone + Tor-Faktor (< 1 deterministisch ausgedünnt, 0 = aus)."""
        if not self.drin(a, b):
            return False
        f = self.tor_faktor(tor)
        if f >= 1.0:
            return True
        if f <= 0.0:
            return False
        a, b = self._ij(a, b)
        return h1(a + self.win[0], b + self.win[2], self.seed, 6000 + zlib.crc32(tor.encode()) % 997) < f

    def gate_vec(self, tor, ci, cj):
        ci = np.clip(np.round(np.asarray(ci)).astype(np.int32), 0, self.H - 1)
        cj = np.clip(np.round(np.asarray(cj)).astype(np.int32), 0, self.W - 1)
        ok = (self.lo[ci, cj] <= self.U[ci, cj]) & (self.U[ci, cj] < self.hi[ci, cj])
        f = self.tor_faktor(tor)
        if f <= 0.0:
            return np.zeros(ci.shape, bool)
        if f < 1.0:
            ok &= hash01(ci + self.win[0], cj + self.win[2], self.seed, 6000 + zlib.crc32(tor.encode()) % 997) < f
        return ok


def _anzahl(spanne, a, b, seed, kanal):
    """Ganzzahl aus [min, max] (Liste) oder Zahl, deterministisch je Ort."""
    if isinstance(spanne, (int, float)):
        x = float(spanne)
        return int(x) + int(h1(a, b, seed, kanal) < x - int(x))
    if isinstance(spanne, list) and len(spanne) == 2:
        return int(spanne[0] + h1(a, b, seed, kanal) * (spanne[1] - spanne[0] + 1))
    return 0


def _spanne(v, a, b, seed, kanal, dflt):
    if isinstance(v, list) and len(v) == 2 and all(isinstance(x, (int, float)) for x in v):
        return v[0] + (v[1] - v[0]) * h1(a, b, seed, kanal)
    if isinstance(v, (int, float)):
        return float(v)
    return dflt


def _netzhoehe(K, pfade, dflt=1.0):
    zs = [K.inv.get(p) for p in pfade] if isinstance(K.inv, dict) else []
    zs = [z for z in zs if z]
    return sum(zs) / len(zs) if zs else dflt


def _top(K, maske, score, raster, n):
    ci, cj = wahl_je_raster(maske, score, max(1, int(raster)), K.ii, K.jj)
    if ci.size == 0 or n <= 0:
        return []
    o = np.argsort(score[ci, cj], kind='stable')[:n]
    return list(zip(ci[o].tolist(), cj[o].tolist()))


def _kontur_yaw(K, a, b):
    return math.atan2(float(K.dzdx[a, b]), float(-K.dzdy[a, b]))


def _welt(K, a, b):
    return round(float((b + K.wj0 - X0) * 100), 1), round(float((a + K.wi0 - Y0) * 100), 1)


def hecke_setzen(K, Z, ecken, a, b):
    """aue: Hecke an Feldrändern (Anteil der Ränder, Abstand, Lücken), 1,5 m außerhalb des Zauns."""
    cfg = Z.extra.get('hecke_am_feldrand')
    if not cfg or not cfg.get('netze') or not Z.gate('hecke', a, b):
        return 0
    n = 0
    ctr = np.array([a, b], np.float32)
    for k in range(4):
        if h1(a, b, K.seed, 700 + k) >= float(cfg.get('anteil_raender', 0.5)):
            continue
        p0, p1 = np.asarray(ecken[k], np.float32), np.asarray(ecken[(k + 1) % 4], np.float32)
        aussen = 0.5 * (p0 + p1) - ctr
        aussen /= (np.linalg.norm(aussen) + 1e-6)
        fi_, fj_, _ = linie_punkte(p0 + aussen * 1.5, p1 + aussen * 1.5, float(cfg.get('abstand_m', 2.5)))
        if fi_.size == 0:
            continue
        gk = np.round(fi_ * 3).astype(np.int64) + K.wi0
        gl = np.round(fj_ * 3).astype(np.int64) + K.wj0
        keep = hash01(gk, gl, K.seed, 710 + k) >= float(cfg.get('luecken_anteil', 0.3))
        ms0, ms1 = cfg.get('massstab', [0.9, 1.4])
        ms = ms0 + (ms1 - ms0) * hash01(gk, gl, K.seed, 720 + k)
        n += K.S.add(cfg['netze'], fi_[keep], fj_[keep], 'hecke', False, (0, 30000), ms[keep], None, 0.3, 4.0, seed=K.seed, kanal=730)
    return n


def sf_kopfweiden(K, Z, orte):
    cfg = Z.extra.get('kopfweiden_reihe')
    netze = (cfg or {}).get('netze') or (cfg or {}).get('netze_ersatz')
    if not cfg or not netze:
        return 0
    ms_r = cfg.get('massstab_ersatz', [0.9, 1.1]) if not cfg.get('netze') or cfg.get('netze') == cfg.get('netze_ersatz') else cfg.get('massstab', [0.9, 1.1])
    r0, r1 = cfg.get('ring_m', [30, 300])
    entlang = cfg.get('entlang', ['weg', 'bach'])
    hm = float(cfg.get('hang_max_grad', 8))
    basis = K.frei_basis & Z.maske & (K.hang <= hm) & (K.lab_voll == 0) & (K.d_ort >= r0) & (K.d_ort <= r1)
    linie = np.zeros(K.hang.shape, bool)
    if 'weg' in entlang:
        linie |= np.abs(K.d_weg - 4.0) < 0.7
    if 'bach' in entlang or 'graben' in entlang:
        linie |= (np.abs(K.d_wasser - 4.0) < 0.7) & (K.d_wasser <= float(cfg.get('d_wasser_max_m', 25)))
    n_baum, n_reihe = 0, 0
    for o in orte:
        nr = _anzahl(cfg.get('je_ort', [1, 3]), o['i'], o['j'], K.seed, 801)
        m = basis & linie & (np.hypot(K.ii - o['i'], K.jj - o['j']) < o['radius'] + r1)
        for a, b in _top(K, m, hash01(K.gi, K.gj, K.seed, 802), 60, nr):
            if not Z.gate('kopfweiden', a, b):
                continue
            if abs(K.d_weg[a, b] - 4.0) < 0.7:
                yaw = float(K.tang_yaw[a, b])
            else:
                vi, vj = float(K.ws_i[a, b] - a), float(K.ws_j[a, b] - b)
                l = math.hypot(vi, vj) + 1e-6
                yaw = math.atan2(-vj / l, vi / l)
            L = _spanne(cfg.get('laenge_m', [30, 90]), a, b, K.seed, 803, 50)
            abst = _spanne(cfg.get('abstand_m', [6, 9]), a, b, K.seed, 804, 7)
            k = np.arange(int(L // abst) + 1)
            fi_ = a + k * abst * math.sin(yaw) + (hash01(k + a, k + b, K.seed, 805) - 0.5) * 0.8
            fj_ = b + k * abst * math.cos(yaw) + (hash01(k + b, k + a, K.seed, 806) - 0.5) * 0.8
            mi = np.clip(np.round(fi_).astype(np.int32), 0, K.H - 1)
            mj = np.clip(np.round(fj_).astype(np.int32), 0, K.W - 1)
            ok = (fi_ >= 0) & (fi_ < K.H) & (fj_ >= 0) & (fj_ < K.W) & K.frei_basis[mi, mj] & (K.hang[mi, mj] <= hm)
            if ok.sum() < 3:
                continue
            ms = ms_r[0] + (ms_r[1] - ms_r[0]) * hash01(mi + K.wi0, mj + K.wj0, K.seed, 807)
            n_baum += K.S.add(netze, fi_[ok], fj_[ok], 'kopfweiden', bool(cfg.get('kollision', True)), (0, 0), ms[ok], None, 0.05, 10.0,
                              akteur=str(cfg.get('rolle', 'akteur')) == 'akteur', seed=K.seed, kanal=808)
            n_reihe += 1
    K.stat['kopfweiden_reihen'] = K.stat.get('kopfweiden_reihen', 0) + n_reihe
    return n_baum


def _rechteck_mauer(K, Z, e, oeffnung_m, a, b, kanal):
    for k in range(4):
        p0, p1 = np.asarray(e[k], np.float32), np.asarray(e[(k + 1) % 4], np.float32)
        if k == 0 and oeffnung_m > 0:
            pm = 0.5 * (p0 + p1)
            d = (p1 - p0) / (np.linalg.norm(p1 - p0) + 1e-6)
            mauer_setzen(K.S, p0, pm - d * oeffnung_m / 2, Z.R, K.seed, kanal + k, a, b)
            mauer_setzen(K.S, pm + d * oeffnung_m / 2, p1, Z.R, K.seed, kanal + 10 + k, a, b)
        else:
            mauer_setzen(K.S, p0, p1, Z.R, K.seed, kanal + k, a, b)


def sf_pferch(K, Z, orte):
    cfg = Z.extra.get('pferch')
    if not cfg:
        return 0
    hm = float(cfg.get('hang_max_grad', 8))
    erlaubt = K.frei_basis & Z.maske & (K.hang <= hm) & (K.d_weg > 4) & (K.lab_voll == 0)
    r0, r1 = cfg.get('ort_ring_m', [40, 220])
    gm = cfg.get('groesse_m', [[8, 14], [8, 14]])
    bw = cfg.get('beiwerk') or {}
    N = Z.R['netze']
    kandidaten = []
    for o in orte:
        n = _anzahl(cfg.get('je_ort', [1, 2]), o['i'], o['j'], K.seed, 821)
        m = erlaubt & (K.d_ort >= r0) & (K.d_ort <= r1) & (np.hypot(K.ii - o['i'], K.jj - o['j']) < o['radius'] + r1)
        kandidaten += _top(K, m, hash01(K.gi, K.gj, K.seed, 822), 40, n * 3)[:n * 3]
    nf = _anzahl(cfg.get('frei_je_feld', [0, 1]), K.wi0, K.wj0, K.seed, 823)
    m = erlaubt & (K.d_wasser <= float(cfg.get('frei_wasser_max_m', 90))) & (K.d_ort > 150)
    kandidaten += _top(K, m, hash01(K.gi, K.gj, K.seed, 824), 120, nf)
    gesetzt = 0
    for a, b in kandidaten:
        if not Z.gate('pferch', a, b) or not K.im_feld[a, b]:
            continue
        la = _spanne(gm[0], a, b, K.seed, 825, 10)
        lb = _spanne(gm[1], a, b, K.seed, 826, 10)
        wk = float(K.tang_yaw[a, b]) if K.d_weg[a, b] < 80 else _kontur_yaw(K, a, b)
        e = rechteck_ecken(a, b, la, lb, wk)
        if not rechteck_frei(e, erlaubt, K.H, K.W):
            continue
        if any(math.hypot(f[0] - a, f[1] - b) < (math.hypot(f[2], f[3]) + math.hypot(la, lb)) / 2 + 3 for f in K.felder_ok):
            continue
        _rechteck_mauer(K, Z, e, float(cfg.get('oeffnung_m', 1.8)), a, b, 830)
        if isinstance(bw.get('trog'), str):
            K.S.add([bw['trog']], [a + 1.0], [b], 'pferch', True, (0, 25000), 1.0, [wk], 0.5, 4.0, seed=K.seed, kanal=840)
        if isinstance(bw.get('heu'), str):
            K.S.add([bw['heu']], [a - 1.5], [b + 1.0], 'pferch', False, (0, 25000), 1.0, None, 0.5, 6.0, seed=K.seed, kanal=841)
        if isinstance(bw.get('pfahl'), str):
            p0, p1 = np.asarray(e[0]), np.asarray(e[1])
            pm = 0.5 * (p0 + p1)
            d = (p1 - p0) / (np.linalg.norm(p1 - p0) + 1e-6)
            o_ = float(cfg.get('oeffnung_m', 1.8)) / 2 + 0.2
            K.S.add([bw['pfahl']], [pm[0] - d[0] * o_, pm[0] + d[0] * o_], [pm[1] - d[1] * o_, pm[1] + d[1] * o_], 'pferch', False, (0, 30000),
                    1.0, None, 0.1, 30.0, seed=K.seed, kanal=842)
        K.felder_ok.append((a, b, la, lb, wk, None))
        K.flaechen.append({'typ': 'pferch', 'ecken_cm': ecken_welt(e, K.win), 'lage_vorschlag': 'Erde', 'umfriedung': 'mauer'})
        gesetzt += 1
    K.stat['pferche'] = K.stat.get('pferche', 0) + gesetzt
    return gesetzt


def sf_freie_mauern(K, Z):
    cfg = Z.extra.get('freie_mauern')
    if not cfg or 'je_km2' not in cfg:
        return 0
    flaeche_km2 = float((Z.anteil * K.im_feld).sum()) / 1e6
    je = cfg['je_km2']
    dichte = 0.5 * (je[0] + je[1]) if isinstance(je, list) else float(je)
    n = int(round(dichte * flaeche_km2))
    if n <= 0:
        return 0
    m = K.frei_basis & Z.maske & K.im_feld & (K.hang < 20) & (K.d_ort > 30) & (K.d_weg > 5)
    raster = math.sqrt(1e6 / max(0.1, dichte))
    M = Z.R['mauer']
    gesetzt = 0
    for a, b in _top(K, m, hash01(K.gi, K.gj, K.seed, 851), raster, n):
        if not Z.gate('mauer', a, b):
            continue
        yaw = float(K.tang_yaw[a, b]) if ('weg' in str(cfg.get('verlauf', '')) and K.d_weg[a, b] < 60) else _kontur_yaw(K, a, b)
        L = _spanne(M.get('laenge_m', [15, 60]), a, b, K.seed, 852, 30)
        nseg = max(1, int(L // 4.0))
        for s in range(nseg):
            t0 = -L / 2 + s * 4.0
            p0 = np.array([a + t0 * math.sin(yaw), b + t0 * math.cos(yaw)])
            p1 = np.array([a + (t0 + 4.0) * math.sin(yaw), b + (t0 + 4.0) * math.cos(yaw)])
            pm = 0.5 * (p0 + p1)
            ia, ib = int(round(pm[0])), int(round(pm[1]))
            if not (0 <= ia < K.H and 0 <= ib < K.W) or not K.frei_basis[ia, ib] or K.hang[ia, ib] > 30:
                continue
            if h1(a + s, b, K.seed, 853) < float(cfg.get('luecken_anteil', 0.12)):
                continue
            mauer_setzen(K.S, p0, p1, Z.R, K.seed, 860 + s % 7, a, b)
        gesetzt += 1
    K.stat['mauern_frei'] = K.stat.get('mauern_frei', 0) + gesetzt
    return gesetzt


def _ring(K, Z, a, b, radius, n, netze, gruppe, kollision, akteur, umgefallen, hoehe_m, eingraben, kanal):
    if not netze or n <= 0:
        return 0
    k = np.arange(n)
    ang = k * 2 * math.pi / n + (hash01(k + a, k + b, K.seed, kanal) - 0.5) * 0.3
    fi_ = a + radius * np.sin(ang)
    fj_ = b + radius * np.cos(ang)
    hz = _netzhoehe(K, netze, 1.0)
    h_lo, h_hi = (hoehe_m if isinstance(hoehe_m, list) else [hz, hz])
    hs = h_lo + (h_hi - h_lo) * hash01(k + b, k + a, K.seed, kanal + 1)
    ms = hs / max(0.05, hz)
    um = hash01(k * 3 + a, k + b, K.seed, kanal + 2) < umgefallen
    roll = np.where(um, math.radians(80), 0.0).astype(np.float32)
    ein = eingraben if isinstance(eingraben, list) else [0.3, 0.45]
    z_off = -(0.5 * (ein[0] + ein[1])) * hs * np.where(um, 0.3, 1.0)
    return K.S.add(netze, fi_, fj_, gruppe, kollision, (0, 0 if akteur else 50000), ms, ang + math.pi / 2, 0.3, 0.0,
                   z_offset_m=z_off, roll=roll, akteur=akteur, seed=K.seed, kanal=kanal + 3)


def sf_steinkreis(K, Z):
    cfg = Z.extra.get('steinkreis')
    if not cfg or not cfg.get('netze'):
        return 0
    m = K.frei_basis & Z.maske & K.im_feld & (K.hang < 12) & (K.prominenz >= float(cfg.get('kuppen_prominenz_m', 10)))
    m &= (K.hoehe >= max_filter(K.hoehe, 20) - 0.5)
    sc = -K.prominenz * 0.05 + hash01(K.gi, K.gj, K.seed, 871)
    n = 0
    for a, b in _top(K, m, sc, 300, int(cfg.get('max_je_feld', 1))):
        if not Z.gate('steinkreis', a, b):
            continue
        r = _spanne(cfg.get('radius_m', [6, 11]), a, b, K.seed, 872, 8)
        ns = _anzahl(cfg.get('steine', [5, 9]), a, b, K.seed, 873)
        n += _ring(K, Z, a, b, r, ns, cfg['netze'], 'steinkreis', bool(cfg.get('kollision', True)), str(cfg.get('rolle', '')) == 'akteur',
                   float(cfg.get('umgefallen_anteil', 0.25)), cfg.get('stein_hoehe_m'), cfg.get('eingraben', [0.3, 0.45]), 874)
        K.blickziele.append({'typ': 'steinkreis', 'x': _welt(K, a, b)[0], 'y': _welt(K, a, b)[1], 'z': round(float(K.hoehe[a, b] * 100), 1),
                             'regel': 'spuren_overrides %s steinkreis' % Z.thema})
    return n


def sf_huegelgrab(K, Z):
    cfg = Z.extra.get('huegelgrab')
    netze = Z.R['netze'].get('huegelgrab')
    if not cfg or not netze:
        return 0
    m = K.frei_basis & Z.maske & K.im_feld & K.lichtung & (K.hang < 6) & (K.d_weg >= 40)
    nz = _anzahl(cfg.get('je_feld', [0, 1]), K.wi0 + 7, K.wj0, K.seed, 881)
    n = 0
    for a, b in _top(K, m, hash01(K.gi, K.gj, K.seed, 882), 300, nz):
        if not Z.gate('huegelgrab', a, b):
            continue
        r = _spanne(cfg.get('radius_m', [4, 7]), a, b, K.seed, 883, 5)
        ns = _anzahl(cfg.get('stuecke', [7, 12]), a, b, K.seed, 884)
        n += _ring(K, Z, a, b, r, ns, netze, 'grab', True, False, 0.0, None, [0.2, 0.35], 885)
        K.flaechen.append({'typ': 'huegelgrab', 'mitte_cm': list(_welt(K, a, b)), 'radius_m': round(r, 1), 'lage_vorschlag': 'Moos'})
    return n


def sf_ruine(K, Z, schluessel):
    cfg = Z.extra.get(schluessel)
    if not cfg:
        return 0
    akt = cfg.get('netze_akteur') or (cfg.get('netze') if str(cfg.get('rolle', 'akteur')) == 'akteur' else [])
    fol = cfg.get('netze_foliage') or ([] if akt else cfg.get('netze', []))
    if not akt and not fol:
        return 0
    if schluessel == 'tempelruine':
        m = (K.hang < 10) & (K.d_weg >= 10) & (K.d_weg <= 60)
        wand = K.hang > 50
        if wand.any():
            m &= dilate(wand, 22)  # Karstfuß: nahe einer Wand
        ng = _anzahl(cfg.get('je_feld', [1, 2]), K.wi0, K.wj0 + 3, K.seed, 891)
        rad = 0.5 * _spanne(cfg.get('flaeche_m', [18, 30]), K.wi0, K.wj0, K.seed, 892, 24)
        stuecke = [4, 8]
    else:
        m = (K.hang < 12) & (K.d_weg >= 20) & (K.d_weg <= 80)
        ng = _anzahl(cfg.get('gruppen_je_feld', [1, 3]), K.wi0, K.wj0 + 3, K.seed, 891)
        rad = None
        stuecke = cfg.get('stuecke_je_gruppe', [3, 8])
    m &= K.frei_basis & Z.maske & K.im_feld & (K.d_ort > 60)
    sc = -0.05 * K.prominenz + hash01(K.gi, K.gj, K.seed, 893)
    n = 0
    bw = cfg.get('bewuchs') or {}
    for a, b in _top(K, m, sc, 150, ng):
        if not Z.gate('ruine', a, b):
            continue
        r = rad if rad else _spanne(cfg.get('radius_m', [6, 18]), a, b, K.seed, 894, 10)
        ns = max(1, _anzahl(stuecke, a, b, K.seed, 895))
        yaw0 = h1(a, b, K.seed, 896) * math.pi
        k = np.arange(ns)
        ang = yaw0 + (hash01(k + a, k + b, K.seed, 897) - 0.5) * 2 * math.pi
        rr = np.sqrt(hash01(k + b, k + a, K.seed, 898)) * r * 0.5
        fi_ = a + rr * np.sin(ang)
        fj_ = b + rr * np.cos(ang)
        yaw = yaw0 + (hash01(k * 5 + a, k + b, K.seed, 899) - 0.5) * math.radians(24)
        kg = cfg.get('kippen_grad', [2, 8])
        roll = np.radians(kg[0] + (kg[1] - kg[0]) * hash01(k + a, k * 7 + b, K.seed, 900)).astype(np.float32)
        ein = cfg.get('eingraben_anteil', [0.15, 0.35])
        n_akt = min(ns, 2) if akt else 0
        for teil, netze, akteur in ((slice(0, n_akt), akt, True), (slice(n_akt, ns), fol or akt, not fol)):
            if not netze or fi_[teil].size == 0:
                continue
            hz = _netzhoehe(K, netze, 2.0)
            n += K.S.add(netze, fi_[teil], fj_[teil], 'ruine', True, (0, 0 if akteur else 60000), 1.0, yaw[teil], 0.2,
                         100.0 * hz * 0.5 * (ein[0] + ein[1]), roll=roll[teil], akteur=akteur, seed=K.seed, kanal=901)
        for nk, anz, rad_b in (('moos_am_fuss', 'moos_je_stueck', 1.2), ('farn', 'farn_je_stueck', 1.6), ('bruchsteine', 'bruchsteine_je_stueck', 2.5)):
            if not bw.get(nk):
                continue
            for s in range(ns):
                c = _anzahl(bw.get(anz, [2, 5]), int(fi_[s] * 3), int(fj_[s] * 3), K.seed, 902)
                q = np.arange(c)
                an = hash01(q + s, q + a, K.seed, 903) * 2 * math.pi
                rq = 0.4 + hash01(q + a, q + s, K.seed, 904) * rad_b
                n += K.S.add(bw[nk], fi_[s] + rq * np.sin(an), fj_[s] + rq * np.cos(an), 'ruine', False, (0, 12000), 1.0, None, 0.8, 3.0,
                             seed=K.seed, kanal=905)
        if bw.get('efeu'):
            for s in range(n_akt):
                if h1(s, a + b, K.seed, 906) < float(bw.get('efeu_anteil_waende', 0.4)):
                    n += K.S.add(bw['efeu'], [fi_[s] + 0.3, fi_[s] - 0.3], [fj_[s], fj_[s] + 0.2], 'ruine', False, (0, 15000), 1.0, None, 0.5, 0.0,
                                 seed=K.seed, kanal=907)
        x, y = _welt(K, a, b)
        K.flaechen.append({'typ': schluessel, 'mitte_cm': [x, y], 'radius_m': round(float(r), 1), 'um_ruine': cfg.get('um_ruine', {}),
                           'lage_vorschlag': 'Erde'})
        K.blickziele.append({'typ': schluessel, 'x': x, 'y': y, 'z': round(float(K.hoehe[a, b] * 100), 1), 'regel': 'spuren_overrides %s %s' % (Z.thema, schluessel)})
    return n


def sf_galgen(K, Z):
    cfg = Z.extra.get('galgen_ersatz')
    teile = [t for t in (cfg or {}).get('bauteile', []) if isinstance(t, dict) and t.get('netz')]
    if not teile:
        return 0
    wa = cfg.get('weg_abstand_m', [6, 25])
    m = K.frei_basis & Z.maske & K.im_feld & (K.d_weg >= wa[0]) & (K.d_weg <= wa[1]) & (K.hang < 15) & (K.d_ort > 60)
    km_weg = float((K.weg_m & Z.maske & K.im_feld).sum()) / 3.0 / 1000.0
    n = _anzahl(float(cfg.get('je_km_weg', 0.4)) * km_weg, K.wi0, K.wj0 + 11, K.seed, 911)
    sc = hash01(K.gi, K.gj, K.seed, 912) - float(cfg.get('kuppen_bonus', 3.0)) * dilate(K.kuppe, 10)
    gesetzt = 0
    for a, b in _top(K, m, sc, 250, n):
        if not Z.gate('galgen', a, b):
            continue
        yaw = float(K.normal_yaw[a, b])
        z0 = float(K.hoehe[a, b])
        for t in teile:
            vx, vy, vz = (list(t.get('versatz_m', [0, 0, 0])) + [0, 0, 0])[:3]
            rx, ry, rz = (list(t.get('rot_grad', [0, 0, 0])) + [0, 0, 0])[:3]
            fi_ = a + vx * math.sin(yaw) + vy * math.cos(yaw)
            fj_ = b + vx * math.cos(yaw) - vy * math.sin(yaw)
            K.S.add([t['netz']], [fi_], [fj_], 'galgen', True, (0, 0), 1.0, [yaw + math.radians(rz)], 0.0, 0.0,
                    roll=np.array([math.radians(rx)], np.float32), akteur=True, z_abs_m=[z0 + vz], seed=K.seed, kanal=913)
        gesetzt += 1
    K.stat['galgen'] = K.stat.get('galgen', 0) + gesetzt
    return gesetzt


def sf_brunnen(K, Z, orte):
    cfg = Z.extra.get('brunnen')
    netze = (cfg or {}).get('netze') or Z.R['netze'].get('brunnen')
    if not cfg or not netze:
        return 0
    basis = K.frei_basis & Z.maske & (K.hang < 10) & (K.d_weg > 3)
    kand = []
    for o in orte:
        n = _anzahl(cfg.get('je_ort', [1, 2]), o['i'], o['j'], K.seed, 921)
        m = basis & (K.d_ort >= 5) & (K.d_ort <= 40) & (np.hypot(K.ii - o['i'], K.jj - o['j']) < o['radius'] + 40)
        kand += _top(K, m, hash01(K.gi, K.gj, K.seed, 922), 30, n)
    fk = float(cfg.get('frei_je_km2', 0.0))
    if fk > 0:
        nf = _anzahl(fk * float((Z.anteil * K.im_feld).sum()) / 1e6, K.wi0, K.wj0 + 5, K.seed, 923)
        m = basis & (K.d_ort > 100) & ((K.d_wasser <= 60) | (K.mulde() > 0.5))
        kand += _top(K, m, hash01(K.gi, K.gj, K.seed, 924), math.sqrt(1e6 / fk), nf)
    gesetzt = 0
    for a, b in kand:
        if not Z.gate('brunnen', a, b):
            continue
        gesetzt += K.S.add(netze, [a], [b], 'brunnen', True, (0, 0), 1.0, None, 0.0, 10.0, akteur=True, seed=K.seed, kanal=925)
    K.stat['brunnen'] = K.stat.get('brunnen', 0) + gesetzt
    return gesetzt


def sf_pfaehle(K, Z):
    cfg = Z.extra.get('pfaehle')
    if not cfg or not cfg.get('netze') or not K.wasser_m.any():
        return 0
    d_land = K.d_land()
    ufer_m = float(((d_land > 0) & (d_land <= 1.5) & Z.maske & K.im_feld).sum())
    n = _anzahl(float(cfg.get('je_km_ufer', 6)) * ufer_m / 1000.0, K.wi0 + 3, K.wj0, K.seed, 931)
    wa = cfg.get('wasser_abstand_m')
    if isinstance(wa, list) and len(wa) == 2:  # Uferband an Land (sumpf: 0,3-3 m)
        flach = (~K.wasser_m) & (K.d_wasser >= float(wa[0])) & (K.d_wasser <= float(wa[1])) & K.frei_basis
        im_wasser = False
    else:  # Flachwasser bis 3 m vom Ufer
        flach = K.wasser_m & (d_land > 0) & (d_land <= 3.0)
        im_wasser = True
    gesetzt = 0
    for a, b in _top(K, flach & Z.maske & K.im_feld, hash01(K.gi, K.gj, K.seed, 932), 30, n):
        if not Z.gate('pfaehle', a, b):
            continue
        c = _anzahl(cfg.get('gruppe', [2, 5]), a, b, K.seed, 933)
        q = np.arange(c)
        an = hash01(q + a, q + b, K.seed, 934) * 2 * math.pi
        rq = np.sqrt(hash01(q + b, q + a, K.seed, 935)) * float(cfg.get('radius_m', 3.0))
        fi_, fj_ = a + rq * np.sin(an), b + rq * np.cos(an)
        mi = np.clip(np.round(fi_).astype(np.int32), 0, K.H - 1)
        mj = np.clip(np.round(fj_).astype(np.int32), 0, K.W - 1)
        ok = flach[mi, mj]
        ng = cfg.get('neigung_grad', [3, 14])
        roll = np.radians(ng[0] + (ng[1] - ng[0]) * hash01(q * 3 + a, q + b, K.seed, 936)).astype(np.float32)
        msr = cfg.get('massstab', [0.8, 1.2])
        ms = msr[0] + (msr[1] - msr[0]) * hash01(mi + K.wi0, mj + K.wj0, K.seed, 938)
        gesetzt += K.S.add(cfg['netze'], fi_[ok], fj_[ok], 'pfaehle', bool(cfg.get('kollision', False)), tuple(cfg.get('sichtweite', (0, 30000))),
                           ms[ok], None, 0.0, float(cfg.get('eingraben_cm', 60)), roll=roll[ok], auf_wasser=im_wasser, seed=K.seed, kanal=937)
    return gesetzt


def sf_knueppeldamm(K, Z):
    cfg = Z.extra.get('knueppeldamm')
    if not cfg or not cfg.get('netze') or not K.weg_m.any():
        return 0
    nass = (K.d_wasser <= 12.0) | (K.lage('Schlamm') > 0.3) | (K.lage('Algen') > 0.3)
    m = K.weg_m & nass & Z.maske & K.im_feld
    idx = np.flatnonzero(m)
    if idx.size == 0:
        return 0
    ci, cj = K.ii.ravel()[idx], K.jj.ravel()[idx]
    ok = Z.gate_vec('knueppeldamm', ci, cj)
    ci, cj = ci[ok], cj[ok]
    o = np.lexsort((cj, ci, K.d_wasser[ci, cj]))[:int(cfg.get('max_laenge_m_je_feld', 400))]
    ci, cj = ci[o], cj[o]
    theta = K.weg_normale()[ci, cj]  # Stämme quer zum Weg = entlang der Wegnormale
    s = float(cfg.get('schritt_m', 0.45))
    fi_, fj_, yaw = [], [], []
    for off in (-0.5 * s, 0.5 * s):
        fi_.append(ci + off * np.cos(theta))
        fj_.append(cj - off * np.sin(theta))
        yaw.append(theta)
    fi_, fj_, yaw = np.concatenate(fi_), np.concatenate(fj_), np.concatenate(yaw)
    jit = float(cfg.get('jitter_cm', 8)) / 100.0
    gk = np.round(fi_ * 4).astype(np.int64) + K.wi0
    gl = np.round(fj_ * 4).astype(np.int64) + K.wj0
    fi_ = fi_ + (hash01(gk, gl, K.seed, 941) - 0.5) * 2 * jit
    yaw = yaw + (hash01(gl, gk, K.seed, 942) - 0.5) * math.radians(8)
    msr = cfg.get('massstab', [0.9, 1.1])
    ms = msr[0] + (msr[1] - msr[0]) * hash01(gk, gl, K.seed, 944)
    return K.S.add(cfg['netze'], fi_, fj_, 'knueppeldamm', bool(cfg.get('kollision', False)), tuple(cfg.get('sichtweite', (0, 25000))), ms, yaw, 1.0,
                   float(cfg.get('eingraben_cm', 6)), auf_weg=True, seed=K.seed, kanal=943)


def sf_lava_punkte(K, Z):
    """lava: Opferstätte, Schwefelgrube, Fumarolen-Rauch aus lava/<Feld>/plan.json["punkte"]."""
    ex = Z.extra
    if not any(k in ex for k in ('opferstaette', 'schwefelgrube', 'rauch_quelle')):
        return 0
    pts = K.lava_punkte()
    if pts is None:
        K.hinweise.append('lava/%s/plan.json fehlt - Opferstaette/Schwefelgrube/Fumarolen ohne Vorschlagspunkte' % K.feld)
        return 0
    N = Z.R['netze']
    n = 0
    for p in pts:
        a, b = p['i'], p['j']
        if not (0 <= a < K.H and 0 <= b < K.W) or not K.im_feld[int(a), int(b)] or not Z.drin(a, b):
            continue
        typ = str(p.get('typ', ''))
        if typ.startswith('opferstaette') and 'opferstaette' in ex and Z.gate('opferstaette', a, b):
            c = ex['opferstaette']
            if c.get('saeule'):
                n += K.S.add([c['saeule']], [a], [b], 'opferstaette', True, (0, 0), 1.0, None, 0.1, 20.0, akteur=True, seed=K.seed, kanal=951)
            ns = _anzahl(c.get('steine', [8, 12]), a, b, K.seed, 952)
            n += _ring(K, Z, a, b, float(c.get('radius_m', 3.0)), ns, c.get('steinkreis_netze') or N.get('steinmann'), 'opferstaette', False,
                       False, 0.0, None, [0.2, 0.3], 953)
        elif typ.startswith('schwefelgrube') and 'schwefelgrube' in ex and Z.gate('schwefelgrube', a, b):
            c = ex['schwefelgrube']
            namen = [x for x in (c.get('beiwerk') or ['kiste', 'fass']) if isinstance(x, str)]
            nb = _anzahl(c.get('beiwerk_n', [3, 6]), a, b, K.seed, 954)
            q = np.arange(nb)
            an = hash01(q + a, q + b, K.seed, 955) * 2 * math.pi
            rq = 2 + hash01(q + b, q + a, K.seed, 956) * (float(c.get('radius_m', 8)) - 2)
            for s in range(nb):
                nm = namen[s % len(namen)] if namen else 'kiste'
                netze = N.get(nm) if isinstance(N.get(nm), list) else None
                if netze:
                    n += K.S.add(netze, [a + rq[s] * math.sin(an[s])], [b + rq[s] * math.cos(an[s])], 'schwefelgrube', True, (0, 0 if nm == 'karren' else 25000),
                                 1.0, None, 0.5, 5.0, akteur=nm == 'karren', seed=K.seed, kanal=957 + s)
        elif 'rauch_quelle' in ex and typ == str(ex['rauch_quelle'].get('typ', 'fumarole')):
            x, y = _welt(K, a, b)
            K.punkte.append({'typ': typ, 'x': x, 'y': y, 'z': p.get('z', round(float(K.hoehe[int(a), int(b)] * 100), 1)), 'staerke': p.get('staerke', 0.7),
                             'quelle': 'lava/plan.json'})
    return n


def sf_schrein_stein(K, Z):
    """elfenwald: Bildstein an Wegkreuzung oder Bachquerung, mit Kiesel-/Blumen-Beigaben."""
    cfg = Z.extra.get('schrein')
    if not cfg or not cfg.get('netze'):
        return 0
    kreuz = K.kreuzung()
    m = K.frei_basis & Z.maske & K.im_feld & (K.d_weg >= 2) & (K.d_weg <= 4) & (K.hang < 12)
    m_nah = m & dilate(kreuz | (K.weg_m & dilate(K.wasser_m, 6)), 8)
    if m_nah.any():
        m = m_nah
    nz = _anzahl(cfg.get('je_feld', [1, 2]), K.wi0 + 9, K.wj0, K.seed, 961)
    n = 0
    bg = cfg.get('beigaben') or {}
    for a, b in _top(K, m, hash01(K.gi, K.gj, K.seed, 962), 200, nz):
        if not Z.gate('schrein', a, b):
            continue
        yaw = float(K.normal_yaw[a, b])
        n += K.S.add(cfg['netze'], [a], [b], 'schrein', True, (0, 0), 1.0, [yaw], 0.1, 15.0, akteur=True, seed=K.seed, kanal=963)
        for nk, anz in (('kiesel', 'kiesel_anzahl'), ('blumen', 'blumen_anzahl')):
            if bg.get(nk):
                c = _anzahl(bg.get(anz, [6, 12]), a, b, K.seed, 964)
                q = np.arange(c)
                an = hash01(q + a, q + b, K.seed, 965) * 2 * math.pi
                rq = 0.6 + hash01(q + b, q + a, K.seed, 966) * 0.9
                n += K.S.add(bg[nk], a + rq * np.sin(an), b + rq * np.cos(an), 'schrein', False, (0, 9000), 1.0, None, 0.8, 1.0, seed=K.seed, kanal=967)
    return n


def sf_zusatzklassen(K, Z):
    """Zusatzklassen nach KONVENTIONEN §6: Streuung mit dichte_je_ha im Biom + Saum, Masken Hang/Höhe/Wasser/Lagen/Krümmung."""
    zk = Z.extra.get('zusatzklassen') or {}
    n = 0
    for name in sorted(zk):
        kd = zk[name]
        if not isinstance(kd, dict):
            continue
        netze = kd.get('palette') or kd.get('netze') or []
        netze = K.pfade.liste(netze, set())
        if not netze:
            K.hinweise.append('Zusatzklasse %s/%s ohne gueltige palette - entfaellt' % (Z.thema, name))
            continue
        d = float(kd.get('dichte_je_ha', 1.0)) / 1e4
        g = kd.get('gruppe', {})
        gr = g.get('groesse', [1, 1]) if isinstance(g, dict) else (g if isinstance(g, list) else [1, 1])
        rad = float(g.get('radius_m', 3.0)) if isinstance(g, dict) else float(kd.get('radius_m', 3.0))
        lam = np.full(K.hang.shape, d / max(1.0, 0.5 * (gr[0] + gr[1])), np.float32) * Z.anteil
        m = K.frei_basis & Z.maske
        if isinstance(kd.get('hang_grad'), list):
            m &= (K.hang >= kd['hang_grad'][0]) & (K.hang <= kd['hang_grad'][1])
        if isinstance(kd.get('hoehe_m'), list):
            m &= (K.hoehe >= kd['hoehe_m'][0]) & (K.hoehe <= kd['hoehe_m'][1])
        if isinstance(kd.get('wasser_abstand_m'), list):
            m &= (K.d_wasser >= kd['wasser_abstand_m'][0]) & (K.d_wasser <= kd['wasser_abstand_m'][1])
        for ln, w in (kd.get('lagen_min') or {}).items():
            m &= K.lage(ln) * 255.0 >= float(w)
        kr = str(kd.get('kruemmung', 'egal'))
        if kr == 'konkav':
            m &= K.mulde() > 0.2
        elif kr == 'konvex':
            m &= K.mulde() < -0.2
        kanal = 980 + zlib.crc32(name.encode()) % 97 * 10
        idx = np.flatnonzero(m & (hash01(K.gi, K.gj, K.seed, kanal) < lam))
        if idx.size == 0:
            continue
        ci, cj = K.ii.ravel()[idx], K.jj.ravel()[idx]
        c = gr[0] + np.floor(hash01(ci + K.wi0, cj + K.wj0, K.seed, kanal + 1) * (gr[1] - gr[0] + 1)).astype(np.int32)
        rep = np.repeat(np.arange(ci.size), c)
        k = np.concatenate([np.arange(x) for x in c]) if c.size else np.zeros(0, np.int64)
        an = hash01(ci[rep] + 7 * k, cj[rep] + 13 * k, K.seed, kanal + 2) * 2 * math.pi
        rr = np.where(k == 0, 0.0, np.sqrt(hash01(ci[rep] + 3 * k, cj[rep] + 5 * k, K.seed, kanal + 3)) * rad)
        fi_, fj_ = ci[rep] + rr * np.sin(an), cj[rep] + rr * np.cos(an)
        rolle = str(kd.get('rolle', '')).lower()
        fest = any(x in rolle for x in ('fels', 'stein', 'block', 'stamm', 'baum'))
        koll = bool(kd.get('kollision', fest))
        akt = bool(kd.get('akteur', False))
        ms_r = kd.get('massstab', [0.8, 1.2])
        gk = np.round(fi_ * 3).astype(np.int64) + K.wi0
        gl = np.round(fj_ * 3).astype(np.int64) + K.wj0
        ms = ms_r[0] + (ms_r[1] - ms_r[0]) * hash01(gk, gl, K.seed, kanal + 4)
        ein = kd.get('eingraben_anteil', [0.25, 0.45] if fest else [0.02, 0.05])
        hz = _netzhoehe(K, netze, 1.0)
        sw = kd.get('sichtweite', [0, 0 if akt else 30000])
        n += K.S.add(netze, fi_, fj_, 'zusatz_' + name, koll, tuple(sw), ms, None, 0.8 if fest else 0.3,
                     100.0 * hz * 0.5 * (ein[0] + ein[1]) * float(np.mean(ms_r)), akteur=akt, seed=K.seed, kanal=kanal + 5)
    return n


class Kontext:
    """Fensterdaten für die Sonderform-Routinen; teure Zusatzfelder werden erst bei Bedarf berechnet."""

    def __init__(self, **kw):
        self.__dict__.update(kw)
        self._c = {}

    def mulde(self):
        if 'mulde' not in self._c:
            self._c['mulde'] = (gauss_blur(self.hoehe, 10.0) - self.hoehe).astype(np.float32)
        return self._c['mulde']

    def d_land(self):
        if 'd_land' not in self._c:
            self._c['d_land'] = distanz(~self.wasser_m, 16.0)
        return self._c['d_land']

    def lage(self, name):
        k = 'lage_' + str(name)
        if k not in self._c:
            a = lade_raster(os.path.join(self.basis, WELT, 'lage_%s.r8' % name), np.uint8, self.win)
            if a is None:
                self.hinweise.append('lage_%s.r8 fehlt - Bedingung auf diese Lage nicht erfuellbar' % name)
                self._c[k] = np.zeros((self.H, self.W), np.float32)
            else:
                self._c[k] = a.astype(np.float32) / 255.0
        return self._c[k]

    def kreuzung(self):
        if 'kreuz' not in self._c:
            f = box_blur(self.weg_m.astype(np.float32), 7)
            med = float(np.median(f[self.weg_m])) if self.weg_m.any() else 1.0
            self._c['kreuz'] = self.weg_m & (f > 1.6 * med)
        return self._c['kreuz']

    def weg_normale(self):
        """Richtung der Wegnormale je Zelle (Strukturtensor des geglätteten Wegrasters), als yaw = atan2(dY, dX)."""
        if 'wn' not in self._c:
            g = gauss_blur(self.weg_m.astype(np.float32), 2.0)
            gy, gx = np.gradient(g)
            jxx, jyy, jxy = gauss_blur(gx * gx, 3.0), gauss_blur(gy * gy, 3.0), gauss_blur(gx * gy, 3.0)
            self._c['wn'] = (0.5 * np.arctan2(2 * jxy, jxx - jyy)).astype(np.float32)
        return self._c['wn']

    def lava_punkte(self):
        """punkte aus lava/<Feld>/plan.json in Fensterkoordinaten (None, wenn die Lava-Ebene fehlt)."""
        if 'lava' not in self._c:
            p = os.path.join(self.basis, WELT, 'lava', self.feld, 'plan.json')
            pts = None
            if os.path.isfile(p):
                try:
                    pts = []
                    for q in json.load(open(p, encoding='utf-8')).get('punkte', []):
                        x, y = q.get('x_cm', q.get('x')), q.get('y_cm', q.get('y'))
                        if x is None or y is None:
                            continue
                        d = dict(q)
                        d['i'] = float(y) / 100.0 + Y0 - self.wi0
                        d['j'] = float(x) / 100.0 + X0 - self.wj0
                        if 'z_cm' in q:
                            d['z'] = q['z_cm']
                        pts.append(d)
                except Exception as e:
                    self.hinweise.append('lava/%s/plan.json unlesbar (%s)' % (self.feld, e))
                    pts = None
            self._c['lava'] = pts
        return self._c['lava']


def baue_zonen(R, ov, zuordnung, bio, feld, pfade, U, seed, win, saum_m):
    """Je Biom im Fenster mit spuren_overrides eine Zone (Biom + Saum, Anteile normiert), Rest = Zone 'standard' (spuren_regeln)."""
    gew, info_alle = [], {}
    for bidx, bname in enumerate(BIOME15):
        maske = bio == bidx
        if not maske.any():
            continue
        thema = zuordnung.get(bname)
        if thema not in ov:
            continue
        info = info_alle.setdefault(thema, {'datei': os.path.basename(ov[thema][1]), 'biome': []})
        RB = spuren_aufloesen(R, ov[thema][0], thema, bname, feld, pfade, info)
        if RB is None:
            continue
        info['biome'].append(bname)
        w = np.clip(1.0 - distanz(maske, saum_m + 2.0) / max(1e-3, saum_m), 0, 1).astype(np.float32)
        gew.append((bname, thema, RB, w))
    summe = sum((g[3] for g in gew), np.zeros(U.shape, np.float32))
    skal = np.maximum(1.0, summe)
    zonen, cum = [], np.zeros(U.shape, np.float32)
    for bname, thema, RB, w in gew:
        lo = cum / skal
        cum = cum + w
        zonen.append(Zone(bname, RB, lo, cum / skal, U, seed, win, thema, bname))
    rest = cum / skal
    if (rest < 1.0).any():
        R0 = copy.deepcopy(R)
        R0['_tor'], R0['_extra'] = {}, {}
        zonen.append(Zone('standard', R0, rest, np.ones(U.shape, np.float32), U, seed, win))
    for th, inf in info_alle.items():
        for k in list(inf):
            if isinstance(inf[k], set):
                inf[k] = sorted(inf[k])
    return zonen, info_alle


# ----------------------------------------------------------------------------- Planung
def plane_feld(feld, basis, regeln, faktor, bild, ov=None, zuordnung=None, inventar=None):
    t0 = time.time()
    R = regeln
    N = R['netze']
    seed = int(R['seed'])
    rand = int(R.get('fenster_rand_m', 64))
    fb, win = feld_fenster(feld, rand)
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    hinweise = []
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True)
    ii, jj = np.indices((H, W), dtype=np.int32)
    gi, gj = ii + wi0, jj + wj0
    im_feld = (gi >= fb[0]) & (gi < fb[1]) & (gj >= fb[2]) & (gj < fb[3])
    dzdy, dzdx = np.gradient(hoehe)
    hang = np.degrees(np.arctan(np.sqrt(dzdx ** 2 + dzdy ** 2))).astype(np.float32)
    nl = np.sqrt(dzdx ** 2 + dzdy ** 2 + 1.0)
    n_x, n_y, n_z = (-dzdx / nl).astype(np.float32), (-dzdy / nl).astype(np.float32), (1.0 / nl).astype(np.float32)
    biom_namen = BIOME15
    bio, bio_quelle = lade_biome(basis, win, R, feld, hinweise)
    hinweise.append('Biom je Zelle: ' + bio_quelle)
    feld_faktor = faktor * (R['wuesten_feld_faktor'] if feld in R['wuesten_felder'] else 1.0)

    def r8(name):
        a = lade_raster(os.path.join(basis, WELT, name), np.uint8, win)
        if a is None:
            hinweise.append('%s fehlt – Annahme: keine Fläche dieser Art' % name)
            return np.zeros((H, W), bool)
        return a > 0
    wasser_m, weg_m, ort_m = r8('karte_wasser.r8'), r8('karte_weg.r8'), r8('karte_ort.r8')
    ausgabe = os.path.join(basis, WELT, 'spuren', feld)

    # Pflichtschlüssel (KONVENTIONEN §2) und Leerplan bei < 2 % Land im Fenster (§1)
    biome_fenster = {BIOME15[k]: round(float((bio == k).mean()), 4) for k in np.unique(bio)}
    zellen_zustaendig = int((im_feld & ~wasser_m & ~weg_m & ~ort_m).sum())
    land_anteil = float((~wasser_m).mean())
    min_anteil = float(R.get('min_anteil_eigen_fenster', 0.02))
    if land_anteil < min_anteil or zellen_zustaendig == 0:
        os.makedirs(ausgabe, exist_ok=True)
        for f in os.listdir(ausgabe):
            if f.endswith('.f32'):
                os.remove(os.path.join(ausgabe, f))
        hinweise.append('Landanteil im Fenster %.1f %% < %.0f %% - leerer Plan' % (100 * land_anteil, 100 * min_anteil))
        plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'ebene': EBENE, 'instanzen': 0, 'dateien': {},
                'entfernen': R.get('entfernen', ''), 'ft_ordner': R['ft_ordner'], 'ft_praefix': R['ft_praefix'],
                'biome_fenster': biome_fenster, 'zellen_zustaendig': 0, 'biome_eigen': list(BIOME15), 'kollision_anzahl': 0,
                'akteure': [], 'punkte': [], 'flaechen': [], 'blickziele': [], 'hinweise': hinweise}
        with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=1)
        meld('%s: Landanteil %.1f %% < %.0f %% - leerer plan.json (instanzen 0)' % (feld, 100 * land_anteil, 100 * min_anteil))
        return plan
    d_wasser, ws_i, ws_j = distanz(wasser_m, 64.0, seeds=True)
    d_weg, wg_i, wg_j = distanz(weg_m, 64.0, seeds=True)
    d_ort = distanz(ort_m, 200.0)
    nah_wasser = dilate(wasser_m, R['abstand_m']['wasser'])
    # Wegtangente aus dem Distanzfeld (Richtung zum nächsten Wegpunkt → Normale, Tangente senkrecht dazu)
    vn_i = (wg_i - ii).astype(np.float32)
    vn_j = (wg_j - jj).astype(np.float32)
    vnl = np.sqrt(vn_i ** 2 + vn_j ** 2) + 1e-6
    vn_i, vn_j = vn_i / vnl, vn_j / vnl              # Einheitsvektor Zelle → nächster Wegpunkt (Normale)
    tang_yaw = np.arctan2(-vn_j, vn_i)               # Tangente (ti, tj) = (-vn_j, vn_i); yaw = atan2(dy=ti, dx=tj)
    normal_yaw = np.arctan2(vn_i, vn_j)              # Front zum Weg: yaw = atan2(dy=vn_i, dx=vn_j)

    # Bäume → Beschattung (wie Mittelschicht, vereinfacht)
    baeume = lade_baeume(basis, feld, win)
    lagen = {}
    for ln in ('Laub', 'Nadeln', 'Moos'):
        a = lade_raster(os.path.join(basis, WELT, 'lage_%s.r8' % ln), np.uint8, win)
        if a is not None:
            lagen[ln] = a.astype(np.float32) / 255.0
    baum_m = np.zeros((H, W), bool)
    if len(baeume):
        bi = np.clip(np.round(baeume[:, 0]).astype(np.int32), 0, H - 1)
        bj = np.clip(np.round(baeume[:, 1]).astype(np.int32), 0, W - 1)
        dichte = np.zeros((H, W), np.float32)
        np.add.at(dichte, (bi, bj), 1.0)
        beschattung = (1 - np.exp(-1.0 * math.pi * 4.5 ** 2 * gauss_blur(dichte, 6.0))).astype(np.float32)
        baum_m[bi, bj] = True
        hinweise.append('Kronendach aus %d Bäumen' % len(baeume))
    else:
        beschattung = np.zeros((H, W), np.float32)
        for ln, w in (('Laub', 0.9), ('Nadeln', 0.9), ('Moos', 0.3)):
            if ln in lagen:
                beschattung += w * lagen[ln]
        beschattung = np.clip(gauss_blur(beschattung, 8.0), 0, 0.7).astype(np.float32)
        hinweise.append('keine Baum-Ebene gefunden – Beschattung aus Lagen geschätzt (Holzschlag/Köhler/Lichtungen unsicher)')
    nah_baum = dilate(baum_m, R['abstand_m']['baumstamm']) if baum_m.any() else np.zeros((H, W), bool)
    wald = beschattung > 0.35
    wald_anteil_60 = box_blur(wald.astype(np.float32), 30)
    kante = wald & dilate(~wald, 1)
    d_kante = distanz(kante, 64.0)
    lichtung = (~wald) & (beschattung < 0.18) & (d_kante < 40) & (wald_anteil_60 > 0.3)

    # Kuppen (Prominenz) für Steinmänner, Wegkreuze, Blickziele
    Bz = R['blickziele']
    rk = int(Bz['kuppen_fenster_m'] // 2)
    lokal_max = max_filter(hoehe, rk)
    mittel = box_blur(hoehe, rk)
    prominenz = (hoehe - mittel).astype(np.float32)
    kuppe = (hoehe >= lokal_max - 0.01) & (prominenz >= R['steinmann']['kuppen_prominenz_m']) & ~wasser_m

    frei_basis0 = ~wasser_m & ~nah_wasser & ~ort_m & ~nah_baum
    S = Sammler(hoehe, n_x, n_y, n_z, win, im_feld, wasser_m | weg_m | ort_m, weg_m | ort_m, wasser_m | ort_m)
    punkte, flaechen, blickziele = [], [], []
    stat = {}

    def biom_an(i, j):
        return biom_namen[int(bio[int(i), int(j)])]

    # ------------------------------------------------------------------ Orte (Zusammenhangskomponenten auf 4-m-Raster)
    O = R['ort']
    rs = int(O['raster_m'])
    Hc, Wc = H // rs, W // rs
    ort_c = ort_m[:Hc * rs, :Wc * rs].reshape(Hc, rs, Wc, rs).any(axis=(1, 3))
    lab_c = komponenten(ort_c)
    orte = []
    for k in range(1, int(lab_c.max()) + 1):
        m = lab_c == k
        fl = float(m.sum()) * rs * rs
        ci, cj = np.nonzero(m)
        mi, mj = (ci.mean() + 0.5) * rs, (cj.mean() + 0.5) * rs
        orte.append(dict(id=k, flaeche_m2=fl, i=mi, j=mj, radius=math.sqrt(fl / math.pi), gross=fl >= O['min_flaeche_m2'],
                         biom=biom_an(min(H - 1, mi), min(W - 1, mj)), im_feld=bool(im_feld[int(min(H - 1, mi)), int(min(W - 1, mj))])))
    lab_fein = np.kron(lab_c, np.ones((rs, rs), np.int32))
    lab_voll = np.zeros((H, W), np.int32)
    lab_voll[:lab_fein.shape[0], :lab_fein.shape[1]] = lab_fein
    lab_voll[~ort_m] = 0
    hinweise.append('%d Ort-Komponenten (%d ≥ %d m²)' % (len(orte), sum(o['gross'] for o in orte), O['min_flaeche_m2']))

    # ------------------------------------------------------------------ Zonen der Biom-Overrides (KONVENTIONEN §4/§6: Biom + 30-m-Saum)
    felder_ok = []  # (a, b, la, lb, winkel, ort) aller Rechtecke (Felder, Obstgärten, Friedhöfe, Pferche) – zonenübergreifend
    lichtung_gross = box_blur(lichtung.astype(np.float32), 7) > 0.6  # ≈ 150 m² zusammenhängend
    orte_alle = orte
    pfade = Pfade(inventar)
    K = Kontext(basis=basis, feld=feld, win=win, wi0=wi0, wj0=wj0, H=H, W=W, ii=ii, jj=jj, gi=gi, gj=gj, seed=seed, hoehe=hoehe,
                hang=hang, dzdx=dzdx, dzdy=dzdy, d_weg=d_weg, d_wasser=d_wasser, d_ort=d_ort, ws_i=ws_i, ws_j=ws_j,
                tang_yaw=tang_yaw, normal_yaw=normal_yaw, wasser_m=wasser_m, weg_m=weg_m, ort_m=ort_m, frei_basis=frei_basis0,
                lab_voll=lab_voll, im_feld=im_feld, lichtung=lichtung, kuppe=kuppe, prominenz=prominenz, S=S, punkte=punkte,
                flaechen=flaechen, blickziele=blickziele, felder_ok=felder_ok, stat=stat, hinweise=hinweise, inv=inventar, pfade=pfade)
    zonen, ov_info = baue_zonen(R, ov or {}, zuordnung or BIOM_PLANER_VORGABE, bio, feld, pfade, hash01(gi, gj, seed, 4242), seed, win,
                                float(R.get('zusatz_saum_m', 30.0)))
    hinweise.append('Zonen: ' + ', '.join('%s (%s, Anteil Feld %.0f %%)' % (z.name, z.thema or 'spuren_regeln', 100.0 * float((z.anteil * im_feld).sum()) / max(1, int(im_feld.sum())))
                                         for z in zonen if (z.anteil * im_feld).sum() > 0))

    def zone_planen(R, zone):
        N = R['netze']
        feld_faktor = faktor * (R['wuesten_feld_faktor'] if feld in R['wuesten_felder'] else 1.0)
        frei_basis = frei_basis0 & zone.maske
        orte = [o for o in orte_alle if zone.drin(o['i'], o['j'])]
        orte_gross = [o for o in orte if o['gross']]
        # Rauchsäulen in Orten
        for o in orte:
            if not zone.gate('rauch', o['i'], o['j']):
                continue
            n = int(np.clip(round(o['flaeche_m2'] / 1000.0 * O['rauch_je_1000m2']), O['rauch_min'], O['rauch_max'])) if o['gross'] else int(h1(o['i'], o['j'], seed, 11) < 0.5)
            if n == 0:
                continue
            sc = hash01(gi, gj, seed, 12)
            ci, cj = wahl_je_raster(lab_voll == o['id'], sc, 30, ii, jj)
            if ci.size == 0:
                continue
            o2 = np.argsort(hash01(ci + wi0, cj + wj0, seed, 13))[:n]
            for a, b in zip(ci[o2], cj[o2]):
                if im_feld[a, b]:
                    punkte.append({'typ': R['rauch']['ort'], 'x': round(float((b + wj0 - X0) * 100), 1), 'y': round(float((a + wi0 - Y0) * 100), 1),
                                   'z': round(float((hoehe[a, b] + R['rauch']['hoehe_ueber_boden_m']) * 100), 1), 'staerke': 0.5 + 0.5 * float(h1(a, b, seed, 14)), 'ort': o['id']})

        # ------------------------------------------------------------------ Feldstreifen + Obstgärten um Orte
        Fs = R['feldstreifen']
        ring0, ring1 = Fs['ring_m']
        erlaubt_feld = frei_basis & (hang <= Fs['hang_max_grad']) & (beschattung <= Fs['beschattung_max']) & (d_weg > 6) & (d_ort > ring0 - 8)
        # Obstgarten je großem Ort
        Og = R['obstgarten']
        n_obst = 0
        for o in orte_gross:
            if o['radius'] < Og['min_ort_radius_m'] or not o['im_feld'] or not zone.gate('obstgarten', o['i'], o['j']):
                continue
            n_o = 0
            arten = N['obstbaum'].get(o['biom'], [])
            if not arten:
                continue
            kand = erlaubt_feld & (d_ort >= Og['ring_m'][0]) & (d_ort <= Og['ring_m'][1]) & (lab_voll == 0)
            sc = hash01(gi, gj, seed, 51) + np.hypot(ii - o['i'], jj - o['j']) / 400.0
            ci, cj = wahl_je_raster(kand, sc, 40, ii, jj)
            if ci.size == 0:
                continue
            for a, b in zip(ci[np.argsort(sc[ci, cj])][:40], cj[np.argsort(sc[ci, cj])][:40]):
                if n_o >= int(Og.get('max_je_ort', 1)):
                    break
                la = Og['groesse_m'][0][0] + (Og['groesse_m'][0][1] - Og['groesse_m'][0][0]) * h1(a, b, seed, 52)
                lb = Og['groesse_m'][1][0] + (Og['groesse_m'][1][1] - Og['groesse_m'][1][0]) * h1(a, b, seed, 53)
                wk = float(tang_yaw[a, b]) if d_weg[a, b] < 80 else h1(a, b, seed, 54) * math.pi
                ok = False
                for sh, dw in ((1.0, 0.0), (1.0, math.pi / 2), (0.75, 0.0), (0.75, math.pi / 2)):
                    e = rechteck_ecken(a, b, la * sh, lb * sh, wk + dw)
                    if rechteck_frei(e, erlaubt_feld, H, W):
                        ok = True
                        la, lb, wk = la * sh, lb * sh, wk + dw
                        break
                if not ok:
                    continue
                if any(math.hypot(f[0] - a, f[1] - b) < (math.hypot(f[2], f[3]) + math.hypot(la, lb)) / 2 + 4 for f in felder_ok):
                    continue
                c, s_ = math.cos(wk), math.sin(wk)
                u = (np.arange(int(la // Og['abstand_m'])) + 0.5) * Og['abstand_m'] - la / 2
                v = (np.arange(int(lb // Og['reihe_m'])) + 0.5) * Og['reihe_m'] - lb / 2
                uu, vv = np.meshgrid(u, v)
                fi_ = a + uu.ravel() * s_ - vv.ravel() * c + (hash01(uu.ravel().astype(np.int64) * 3 + a, vv.ravel().astype(np.int64) + b, seed, 55) - 0.5) * 1.2
                fj_ = b + uu.ravel() * c + vv.ravel() * s_ + (hash01(uu.ravel().astype(np.int64) + a, vv.ravel().astype(np.int64) * 5 + b, seed, 56) - 0.5) * 1.2
                ms = Og['massstab'][0] + (Og['massstab'][1] - Og['massstab'][0]) * hash01(np.round(fi_).astype(np.int64) + wi0, np.round(fj_).astype(np.int64) + wj0, seed, 57)
                S.add(arten, fi_, fj_, 'obstgarten', Og['kollision'], (0, 0), ms, None, 0.05, 4.0, seed=seed, kanal=58)
                felder_ok.append((a, b, la, lb, wk, o))
                flaechen.append({'typ': 'obstgarten', 'ecken_cm': ecken_welt(e, win), 'lage_vorschlag': 'Wiese', 'ort': o['id'], 'umfriedung': 'keine'})
                if int(Og.get('max_je_ort', 1)) <= 0:
                    break
                n_obst += 1
                n_o += 1
                if n_o >= int(Og.get('max_je_ort', 1)):
                    break
        stat['obstgaerten'] = stat.get('obstgaerten', 0) + (n_obst)
        neue_felder = []
        if orte_gross:
            kand = erlaubt_feld & (d_ort >= ring0) & (d_ort <= ring1)
            sc = hash01(gi, gj, seed, 21)
            ci, cj = wahl_je_raster(kand, sc, int(Fs['raster_m']), ii, jj)
            keep = hash01(ci + wi0, cj + wj0, seed, 22) < Fs['anteil_zellen'] * feld_faktor
            ci, cj = ci[keep], cj[keep]
            o3 = np.argsort(hash01(ci + wi0, cj + wj0, seed, 23))
            je_ort = {}
            for a, b in zip(ci[o3], cj[o3]):
                if len(neue_felder) >= Fs['max_je_feld']:
                    break
                if not zone.gate('feld', a, b):
                    continue
                # nächster Ort
                oo = min(orte_gross, key=lambda o: (o['i'] - a) ** 2 + (o['j'] - b) ** 2)
                if je_ort.get(oo['id'], 0) >= Fs['max_je_ort']:
                    continue
                # Ausrichtung: Wegtangente, sonst Höhenlinie
                if d_weg[a, b] < 80:
                    wk = float(tang_yaw[a, b])
                else:
                    wk = math.atan2(float(dzdx[a, b]), float(-dzdy[a, b]))  # Höhenlinie (senkrecht zum Gradienten)
                la = Fs['groesse_m'][0][0] + (Fs['groesse_m'][0][1] - Fs['groesse_m'][0][0]) * h1(a, b, seed, 24)
                lb = Fs['groesse_m'][1][0] + (Fs['groesse_m'][1][1] - Fs['groesse_m'][1][0]) * h1(a, b, seed, 25)
                ok = False
                for sh, dw in ((1.0, 0.0), (1.0, math.pi / 2), (0.7, 0.0), (0.7, math.pi / 2), (0.5, 0.0)):
                    e = rechteck_ecken(a, b, la * sh, lb * sh, wk + dw)
                    if rechteck_frei(e, erlaubt_feld, H, W):
                        ok = True
                        la, lb, wk = la * sh, lb * sh, wk + dw
                        break
                if not ok:
                    continue
                # Überlappung mit bereits gewählten Rechtecken (Kreisnäherung)
                if any(math.hypot(f[0] - a, f[1] - b) < (math.hypot(f[2], f[3]) + math.hypot(la, lb)) / 2 + 4 for f in felder_ok):
                    continue
                felder_ok.append((a, b, la, lb, wk, oo))
                neue_felder.append((a, b, la, lb, wk, oo))
                je_ort[oo['id']] = je_ort.get(oo['id'], 0) + 1
        for (a, b, la, lb, wk, oo) in neue_felder:
            e = rechteck_ecken(a, b, la, lb, wk)
            bm = biom_an(a, b)
            stein = bm in R['mauer']['biome_stein']
            umfrieden = zone.gate('mauer' if stein else 'zaun', a, b)
            hecke_setzen(K, zone, e, a, b)
            frucht = h1(a, b, seed, 26) < Fs['anteil_frucht']
            flaechen.append({'typ': 'feldstreifen', 'ecken_cm': ecken_welt(e, win), 'lage_vorschlag': Fs['lage_vorschlag_frucht'] if frucht else Fs['lage_vorschlag'],
                             'ort': oo['id'], 'umfriedung': 'mauer' if stein else 'zaun'})
            # Umfriedung
            for k in range(4 if umfrieden else 0):
                p0, p1 = e[k], e[(k + 1) % 4]
                if stein:
                    mauer_setzen(S, p0, p1, R, seed, 300 + k, a, b)
                else:
                    fi_, fj_, yw = linie_punkte(p0, p1, N['zaun_holz_laenge_m'])
                    if fi_.size:
                        luecke = hash01(np.round(fi_ * 3).astype(np.int64) + wi0, np.round(fj_ * 3).astype(np.int64) + wj0, seed, 31) < Fs['zaun_lueckenanteil']
                        roll = (hash01(np.round(fi_ * 3).astype(np.int64), np.round(fj_ * 3).astype(np.int64), seed, 32) - 0.5) * 2 * math.radians(Fs['zaun_kippen_grad'])
                        S.add(N['zaun_holz'], fi_[~luecke], fj_[~luecke], 'zaun', True, (0, 40000), 1.0, np.full((~luecke).sum(), yw, np.float32), 0.6, 6.0, roll=roll[~luecke], seed=seed, kanal=33)
            # Inhalt: Feldfrucht-Reihen oder Stoppeln, Heu
            c, s_ = math.cos(wk), math.sin(wk)
            if frucht:
                na = int(la // Fs['frucht_abstand_m'])
                nb = int(lb // Fs['frucht_reihe_m'])
                u = (np.arange(na) + 0.5) * Fs['frucht_abstand_m'] - la / 2
                v = (np.arange(nb) + 0.5) * Fs['frucht_reihe_m'] - lb / 2
                uu, vv = np.meshgrid(u, v)
                fi_ = a + uu.ravel() * s_ - vv.ravel() * c
                fj_ = b + uu.ravel() * c + vv.ravel() * s_
                ms = 0.6 + 0.3 * hash01(np.round(fi_ * 2).astype(np.int64) + wi0, np.round(fj_ * 2).astype(np.int64) + wj0, seed, 34)
                S.add(N['feldfrucht'], fi_, fj_, 'feld', False, (0, 12000), ms, None, 0.2, 3.0, seed=seed, kanal=35)
            else:
                n = int(la * lb * Fs['stoppel_je_m2'])
                u = (hash01(np.arange(n) + a * 7, np.arange(n) + b * 3, seed, 36) - 0.5) * la
                v = (hash01(np.arange(n) + a * 5, np.arange(n) + b * 11, seed, 37) - 0.5) * lb
                S.add(N['stoppel'], a + u * s_ - v * c, b + u * c + v * s_, 'feld', False, (0, 9000), 1.0, None, 0.6, 2.0, seed=seed, kanal=38)
            nh = int(Fs['heu_je_feld'][0] + h1(a, b, seed, 39) * (Fs['heu_je_feld'][1] - Fs['heu_je_feld'][0] + 1))
            if nh:
                u = (hash01(np.arange(nh) + a, np.arange(nh) + b * 2, seed, 40) - 0.5) * la * 0.8
                v = (hash01(np.arange(nh) + a * 3, np.arange(nh) + b, seed, 41) - 0.5) * lb * 0.8
                S.add(N['heu'], a + u * s_ - v * c, b + u * c + v * s_, 'feld', True, (0, 30000), 1.0, None, 0.5, 8.0, seed=seed, kanal=42)
        stat['feldstreifen'] = stat.get('feldstreifen', 0) + (len(neue_felder))


        # ------------------------------------------------------------------ Zäune/Mauern am Weg vor Orten
        Zw = R['zaun_weg']
        n_zw = 0
        for o in orte_gross:
            if not zone.gate('zaun_weg', o['i'], o['j']):
                continue
            nz = int(Zw['je_ort'][0] + h1(o['i'], o['j'], seed, 61) * (Zw['je_ort'][1] - Zw['je_ort'][0] + 1))
            for k in range(nz):
                o1 = Zw['ortsrand_m'][0] + h1(o['i'], o['j'] + k, seed, 62) * (Zw['ortsrand_m'][1] - Zw['ortsrand_m'][0])
                L = Zw['laenge_m'][0] + h1(o['i'] + k, o['j'], seed, 63) * (Zw['laenge_m'][1] - Zw['laenge_m'][0])
                seite = 1 if h1(o['i'], o['j'], seed, 64 + k) < 0.5 else -1
                # Zellen im Wegband auf einer Seite, Abstand zum Ort in [o1, o1+L], nahe diesem Ort
                band = (np.abs(d_weg - Zw['seitenabstand_m']) < 0.6) & (d_ort >= o1) & (d_ort <= o1 + L) & frei_basis
                band &= (np.hypot(ii - o['i'], jj - o['j']) < o['radius'] + o1 + L + 30)
                # Wegseite: Normale am Ortsmittelpunkt zeigt vom Ort zum Weg; Zellen mit gleichgerichteter Normale liegen auf der Ortsseite
                oi, oj = int(min(H - 1, o['i'])), int(min(W - 1, o['j']))
                seite_m = np.sign(vn_i * vn_i[oi, oj] + vn_j * vn_j[oi, oj])
                band &= seite_m == seite
                if not band.any():
                    continue
                ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 65), int(N['zaun_holz_laenge_m']), ii, jj)
                if ci.size == 0:
                    continue
                bm = o['biom']
                if bm in R['mauer']['biome_stein'] or Zw.get('material') == 'mauer':
                    for a, b in zip(ci, cj):  # kurze Mauerstücke je Rasterzelle entlang der Tangente
                        yw = float(tang_yaw[a, b])
                        p0 = np.array([a - math.sin(yw) * 1.6, b - math.cos(yw) * 1.6])
                        p1 = np.array([a + math.sin(yw) * 1.6, b + math.cos(yw) * 1.6])
                        mauer_setzen(S, p0, p1, R, seed, 66, a, b)
                else:
                    luecke = hash01(ci + wi0, cj + wj0, seed, 67) < Zw['lueckenanteil']
                    roll = (hash01(ci + wi0, cj + wj0, seed, 68) - 0.5) * 2 * math.radians(6)
                    S.add(N['zaun_holz'] + N['zaun_latten'][:1], ci[~luecke], cj[~luecke], 'zaun', True, (0, 40000), 1.0, tang_yaw[ci, cj][~luecke], 0.6, 6.0, roll=roll[~luecke], seed=seed, kanal=69)
                n_zw += int(ci.size)
        stat['zaun_weg_segmente'] = stat.get('zaun_weg_segmente', 0) + (n_zw)

        # ------------------------------------------------------------------ Steinmänner
        Sm = R['steinmann']
        stein_biome = set(Sm['biome'])
        bio_stein = np.isin(bio, [biom_namen.index(b) for b in stein_biome if b in biom_namen])
        n_sm = 0
        # a) Wegmarken
        band = bio_stein & frei_basis & (d_weg >= Sm['weg_abstand_m'][0]) & (d_weg <= Sm['weg_abstand_m'][1]) & (d_ort > 40)
        ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 71), int(0.5 * (Sm['weg_schritt_m'][0] + Sm['weg_schritt_m'][1])), ii, jj)
        keep = hash01(ci + wi0, cj + wj0, seed, 72) < 0.8 * feld_faktor
        for a, b in zip(ci[keep], cj[keep]):
            if zone.gate('steinmann', a, b):
                n_sm += steinmann_setzen(S, a, b, R, seed, 73)
        # b) Kuppen und Pässe (Weg über Kuppe)
        band = bio_stein & kuppe & frei_basis & (d_ort > 40)
        ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 74), int(Sm['kuppen_fenster_m']), ii, jj)
        for a, b in zip(ci, cj):
            if zone.gate('steinmann', a, b):
                n_sm += steinmann_setzen(S, a, b, R, seed, 75)
        # c) frei in der Landschaft
        raster = int(math.sqrt(1.0e6 / max(1.0, Sm['frei_je_km2'])))
        band = bio_stein & frei_basis & (d_weg > 20) & (d_ort > 60) & (hang < 25)
        ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 76), raster, ii, jj)
        keep = hash01(ci + wi0, cj + wj0, seed, 77) < 0.7 * feld_faktor
        for a, b in zip(ci[keep], cj[keep]):
            if zone.gate('steinmann', a, b):
                n_sm += steinmann_setzen(S, a, b, R, seed, 78)
        stat['steinmaenner'] = stat.get('steinmaenner', 0) + (n_sm)

        # ------------------------------------------------------------------ Wegkreuze / Schreine
        Wk = R['wegkreuz']
        band = frei_basis & (d_weg >= Wk['weg_abstand_m'][0]) & (d_weg <= Wk['weg_abstand_m'][1]) & (hang < 20)
        bonus = np.zeros((H, W), np.float32)
        bonus += Wk['kuppen_bonus'] * dilate(kuppe, 10)
        bonus += Wk['furt_bonus'] * ((d_wasser < 15) & (d_wasser > 2))
        bonus += 1.0 * ((d_ort >= Wk['ortsrand_m'][0]) & (d_ort <= Wk['ortsrand_m'][1]))
        score = 1.0 - hash01(gi, gj, seed, 81) - bonus  # klein = gut
        ci, cj = wahl_je_raster(band, score, int(Wk['schritt_m']), ii, jj)
        keep = (score[ci, cj] < 0.35) if ci.size else np.zeros(0, bool)
        n_wk = 0
        for a, b in zip(ci[keep], cj[keep]):
            if not zone.gate('wegkreuz', a, b):
                continue
            bm = biom_an(a, b)
            yw = float(normal_yaw[a, b])  # Front zum Weg
            schrein = bm in Wk['biome_schrein'] and h1(a, b, seed, 82) < Wk['schrein_anteil'] * min(1.0, zone.tor_faktor('schrein'))
            if schrein:
                S.add(N['saeule'][:1], [a], [b], 'schrein', True, (0, 0), 0.6 + 0.1 * h1(a, b, seed, 83), [yw], 0.1, 15.0, akteur=True, seed=seed, kanal=84)
                S.add(N['lampe'], [a + math.cos(yw) * 0.9], [b - math.sin(yw) * 0.9], 'schrein', False, (0, 20000), 1.0, [yw], 0.0, 1.0, seed=seed, kanal=85)
                S.add(N['strauch_ort'], [a - math.sin(yw) * 1.8, a + math.sin(yw) * 1.6], [b - math.cos(yw) * 1.8, b + math.cos(yw) * 1.4], 'schrein', False, (0, 30000), 1.0, None, 0.3, 4.0, seed=seed, kanal=86)
            else:
                ms = Wk['massstab'][0] + (Wk['massstab'][1] - Wk['massstab'][0]) * h1(a, b, seed, 87)
                roll = (h1(a, b, seed, 88) - 0.5) * math.radians(10)
                S.add(N['kreuz'], [a], [b], 'wegkreuz', True, (0, 0), ms, [yw], 0.1, 4.0, roll=np.array([roll], np.float32), akteur=True, seed=seed, kanal=89)
            ang = hash01(np.arange(Wk['steine']) + a, np.arange(Wk['steine']) + b, seed, 90) * 2 * math.pi
            S.add(N['steinmann'], a + 0.55 * np.sin(ang), b + 0.55 * np.cos(ang), 'wegkreuz', False, (0, 15000), 0.7 + 0.3 * hash01(np.arange(Wk['steine']) + b, np.arange(Wk['steine']) + a, seed, 91), None, 1.0, 10.0, seed=seed, kanal=92)
            n_wk += 1
        stat['wegkreuze_schreine'] = stat.get('wegkreuze_schreine', 0) + (n_wk)

        # ------------------------------------------------------------------ verlassene Karren
        Kr = R['karren']
        band = frei_basis & (d_weg >= Kr['weg_abstand_m'][0]) & (d_weg <= Kr['weg_abstand_m'][1]) & (d_ort > Kr['ort_min_m']) & (hang < 18)
        raster = int(1000.0 / max(0.1, Kr['je_km_weg']) / 1.6)
        ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 101), raster, ii, jj)
        keep = hash01(ci + wi0, cj + wj0, seed, 102) < 0.65 * feld_faktor
        n_kr = 0
        for a, b in zip(ci[keep], cj[keep]):
            if not zone.gate('karren', a, b):
                continue
            schwer = h1(a, b, seed, 103) < Kr['anteil_schwer']
            yw = float(tang_yaw[a, b]) + (h1(a, b, seed, 104) - 0.5) * math.radians(30)
            roll = math.radians(Kr['kippen_grad'][0] + h1(a, b, seed, 105) * (Kr['kippen_grad'][1] - Kr['kippen_grad'][0])) * (1 if h1(a, b, seed, 106) < 0.5 else -1)
            S.add(N['karren_schwer'] if schwer else N['karren'], [a], [b], 'karren', True, (0, 0), 1.0, [yw], 1.0, 8.0, roll=np.array([roll], np.float32), akteur=True, seed=seed, kanal=107)
            nb = int(Kr['beiwerk'][0] + h1(a, b, seed, 108) * (Kr['beiwerk'][1] - Kr['beiwerk'][0] + 1))
            ang = hash01(np.arange(nb) + a, np.arange(nb) + b, seed, 109) * 2 * math.pi
            rad = 1.4 + 1.6 * hash01(np.arange(nb) + b, np.arange(nb) + a, seed, 110)
            S.add(N.get('karren_beiwerk') or (N['fass'] + N['kiste'] + N['rad'] + N['sack']), a + rad * np.sin(ang), b + rad * np.cos(ang), 'karren', True, (0, 25000), 1.0, None, 0.5, 4.0, seed=seed, kanal=111)
            n_kr += 1
        stat['karren'] = stat.get('karren', 0) + (n_kr)

        # ------------------------------------------------------------------ Fischerstege an flachen Seeufern
        St = R['steg']
        n_st = 0
        if wasser_m.any():
            rs2 = 4
            Hc2, Wc2 = H // rs2, W // rs2
            w_c = wasser_m[:Hc2 * rs2, :Wc2 * rs2].reshape(Hc2, rs2, Wc2, rs2).any(axis=(1, 3))
            lab_w = komponenten(w_c)
            d_land = distanz(~wasser_m, 64.0)
            lab_wf = np.zeros((H, W), np.int32)
            lab_wf[:Hc2 * rs2, :Wc2 * rs2] = np.kron(lab_w, np.ones((rs2, rs2), np.int32))
            lab_wf[~wasser_m] = 0
            seen = []
            for k in range(1, int(lab_w.max()) + 1):
                m = lab_wf == k
                fl = float(m.sum())
                if fl >= St['see_min_m2'] and float(d_land[m].max()) >= St['see_min_breite_m']:
                    seen.append(k)
            hinweise.append('%d Wasserkomponenten, davon %d Seen/Meer (≥ %d m², ≥ %d m breit)' % (int(lab_w.max()), len(seen), St['see_min_m2'], St['see_min_breite_m']))
            if seen:
                see_lab = lab_wf[np.clip(ws_i, 0, H - 1), np.clip(ws_j, 0, W - 1)]
                ufer = (~wasser_m) & (d_wasser >= 1.0) & (d_wasser <= 2.0) & np.isin(see_lab, seen) & (hang <= St['ufer_hang_max_grad']) & ~ort_m & ~nah_baum
                ufer &= (d_ort <= St['ort_max_m']) | (d_weg <= St['weg_max_m'])
                ufer &= zone.maske
                # Richtung ins Wasser und Tiefe 6 m vom Ufer
                di_ = (ws_i - ii).astype(np.float32)
                dj_ = (ws_j - jj).astype(np.float32)
                dl = np.hypot(di_, dj_) + 1e-6
                di_, dj_ = di_ / dl, dj_ / dl
                tiefe6 = hoehe - bilinear(hoehe, ii + 6 * di_, jj + 6 * dj_)
                ufer &= (tiefe6 >= 0.3) & (tiefe6 <= St['tiefe_6m_max_m'])
                sc = hash01(gi, gj, seed, 121) + d_ort / 2000.0
                ci, cj = wahl_je_raster(ufer, sc, 250, ii, jj)
                o4 = np.argsort(sc[ci, cj]) if ci.size else []
                for a, b in zip(ci[o4][:St['max_je_feld']], cj[o4][:St['max_je_feld']]):
                    if not im_feld[a, b] or not zone.gate('steg', a, b):
                        continue
                    yw = math.atan2(float(di_[a, b]), float(dj_[a, b]))  # Richtung ins Wasser (dy, dx)
                    nseg = int(St['laenge_segmente'][0] + h1(a, b, seed, 122) * (St['laenge_segmente'][1] - St['laenge_segmente'][0] + 1))
                    seg = St['segment_m']
                    deck = float(hoehe[a, b]) + St['deck_ueber_wasser_m']
                    si_, sj_ = math.sin(yw), math.cos(yw)   # Einheitsvektor entlang Steg in (i, j)
                    qi, qj = math.cos(yw), -math.sin(yw)    # quer
                    for k in range(nseg):
                        along = (k + 0.5) * seg
                        for p in range(St['breite_planken']):
                            quer = (p - (St['breite_planken'] - 1) / 2) * St['planke_breite_m']
                            S.add(N['steg_planke'], [a + si_ * along + qi * quer], [b + sj_ * along + qj * quer], 'steg', St['kollision'], (0, 40000), 1.0, [yw], 0.0, 0.0, z_abs_m=[deck], seed=seed, kanal=123, nur_feld=False, auf_wasser=True)
                        for sgn in (-1, 1):
                            S.add(N['steg_pfosten'], [a + si_ * (k + 1) * seg + qi * sgn * 0.7], [b + sj_ * (k + 1) * seg + qj * sgn * 0.7], 'steg', St['kollision'], (0, 40000), 1.0, [yw], 0.0, 0.0, z_abs_m=[deck - 3.8], seed=seed, kanal=124, nur_feld=False, auf_wasser=True)
                        S.add(N['steg_balken'], [a + si_ * along + qi * 0.75], [b + sj_ * along + qj * 0.75], 'steg', False, (0, 40000), 1.0, [yw], 0.0, 0.0, z_abs_m=[deck + 0.12], seed=seed, kanal=125, nur_feld=False, auf_wasser=True)
                    S.add(N['steg_gelaender'], [a + si_ * (nseg * seg - 1.6) + qi * 0.75], [b + sj_ * (nseg * seg - 1.6) + qj * 0.75], 'steg', False, (0, 30000), 1.0, [yw], 0.0, 0.0, z_abs_m=[deck + 0.1], seed=seed, kanal=126, nur_feld=False, auf_wasser=True)
                    nb = int(St['beiwerk'][0] + h1(a, b, seed, 127) * (St['beiwerk'][1] - St['beiwerk'][0] + 1))
                    S.add(N['fass'] + N['kiste'] + N['trog'], a - si_ * (1.5 + np.arange(nb)) + qi * 1.2, b - sj_ * (1.5 + np.arange(nb)) + qj * 1.2, 'steg', True, (0, 25000), 1.0, None, 0.5, 4.0, seed=seed, kanal=128)
                    punkte.append({'typ': 'steg', 'x': round(float((b + wj0 - X0) * 100), 1), 'y': round(float((a + wi0 - Y0) * 100), 1), 'z': round(deck * 100, 1), 'yaw_rad': round(yw, 4), 'laenge_m': nseg * seg})
                    n_st += 1
        stat['stege'] = stat.get('stege', 0) + (n_st)

        # ------------------------------------------------------------------ Holzschlag-Lichtungen
        Hs = R['holzschlag']
        n_hs = 0
        band = lichtung_gross & frei_basis & (d_weg <= Hs['weg_max_m']) & (d_weg > 8) & (d_ort > 60) & (hang < 20)
        ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 131), 200, ii, jj)
        o5 = np.argsort(hash01(ci + wi0, cj + wj0, seed, 132)) if ci.size else []
        for a, b in zip(ci[o5][:Hs['max_je_feld']], cj[o5][:Hs['max_je_feld']]):
            if not zone.gate('holzschlag', a, b):
                continue
            rad = Hs['radius_m'][0] + h1(a, b, seed, 133) * (Hs['radius_m'][1] - Hs['radius_m'][0])
            kreis = (np.hypot(ii - a, jj - b) <= rad) & frei_basis & (d_weg > 3)
            bm = biom_an(a, b)
            stumpf = N['stumpf_nadel'] if bm in NADEL_BIOME else N['stumpf_laub']
            si_, sj_ = wahl_je_raster(kreis & (hash01(gi, gj, seed, 134) < Hs['stumpf_je_m2'] * 4), hash01(gi, gj, seed, 135), 2, ii, jj)
            S.add(stumpf, si_ + hash01(si_ + wi0, sj_ + wj0, seed, 136) - 0.5, sj_ + hash01(sj_ + wj0, si_ + wi0, seed, 137) - 0.5, 'holzschlag', Hs['kollision_stumpf'], (0, 40000), 0.8 + 0.4 * hash01(si_ + wi0, sj_ + wj0, seed, 138), None, 0.6, 8.0, seed=seed, kanal=139)
            ai, aj = wahl_je_raster(kreis & (hash01(gi, gj, seed, 140) < Hs['ast_je_m2'] * 4), hash01(gi, gj, seed, 141), 2, ii, jj)
            S.add(N['ast'], ai, aj, 'holzschlag', False, (0, 15000), 1.0, None, 1.0, 3.0, seed=seed, kanal=142)
            ns = int(Hs['staemme'][0] + h1(a, b, seed, 143) * (Hs['staemme'][1] - Hs['staemme'][0] + 1))
            yw0 = h1(a, b, seed, 144) * math.pi
            ang = hash01(np.arange(ns) + a, np.arange(ns) + b, seed, 145) * 2 * math.pi
            rr = hash01(np.arange(ns) + b, np.arange(ns) + a, seed, 146) * rad * 0.7
            S.add(N['stamm_liegend'], a + rr * np.sin(ang), b + rr * np.cos(ang), 'holzschlag', True, (0, 45000), 1.0, yw0 + (hash01(np.arange(ns) + a * 2, np.arange(ns) + b, seed, 147) - 0.5) * math.radians(40), 1.0, 20.0, seed=seed, kanal=148)
            nst = int(Hs['stapel'][0] + h1(a, b, seed, 149) * (Hs['stapel'][1] - Hs['stapel'][0] + 1))
            ang = hash01(np.arange(nst) + a * 3, np.arange(nst) + b, seed, 150) * 2 * math.pi
            S.add(N['holzstapel'], a + (3 + 3 * np.arange(nst)) * np.sin(ang), b + (3 + 3 * np.arange(nst)) * np.cos(ang), 'holzschlag', True, (0, 35000), 1.0, None, 0.4, 6.0, seed=seed, kanal=151)
            if h1(a, b, seed, 152) < Hs['karren_anteil']:
                S.add(N['karren'], [a + rad * 0.5], [b], 'holzschlag', True, (0, 0), 1.0, [yw0], 0.6, 6.0, akteur=True, seed=seed, kanal=153)
            if h1(a, b, seed, 154) < Hs['lagerfeuer_anteil']:
                ang = np.arange(5) * 2 * math.pi / 5
                S.add(N['steinmann'], a + 0.8 * np.sin(ang), b + 0.8 * np.cos(ang), 'holzschlag', False, (0, 12000), 0.8, None, 1.0, 10.0, seed=seed, kanal=155)
                punkte.append({'typ': R['rauch']['holzschlag'], 'x': round(float((b + wj0 - X0) * 100), 1), 'y': round(float((a + wi0 - Y0) * 100), 1), 'z': round(float((hoehe[a, b] + 1.0) * 100), 1), 'staerke': 0.3})
            n_hs += 1
        stat['holzschlag'] = stat.get('holzschlag', 0) + (n_hs)

        # ------------------------------------------------------------------ Köhlerplätze
        Ko = R['koehler']
        n_ko = 0
        band = frei_basis & (beschattung >= Ko['beschattung'][0]) & (beschattung <= Ko['beschattung'][1]) & (hang <= Ko['hang_max_grad'])
        band &= (d_weg >= Ko['weg_m'][0]) & (d_weg <= Ko['weg_m'][1]) & (d_ort > 80) & ~dilate(baum_m, Ko['platz_radius_m'])
        ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 161), 300, ii, jj)
        o6 = np.argsort(hash01(ci + wi0, cj + wj0, seed, 162)) if ci.size else []
        for a, b in zip(ci[o6][:Ko['max_je_feld']], cj[o6][:Ko['max_je_feld']]):
            if not zone.gate('koehler', a, b):
                continue
            ang = np.arange(Ko['stapel']) * 2 * math.pi / Ko['stapel'] + h1(a, b, seed, 163)
            S.add(N['holzstapel'][:1], a + Ko['radius_m'] * np.sin(ang), b + Ko['radius_m'] * np.cos(ang), 'koehler', True, (0, 35000), 0.9, ang + math.pi / 2, 0.3, 10.0, seed=seed, kanal=164)
            S.add(N['holzstapel'][:1], a + Ko['radius_m'] * 0.55 * np.sin(ang + 0.5), b + Ko['radius_m'] * 0.55 * np.cos(ang + 0.5), 'koehler', True, (0, 35000), 0.8, ang + 0.5 + math.pi / 2, 0.3, 10.0, z_offset_m=0.9, seed=seed, kanal=165)
            ang2 = hash01(np.arange(Ko['stuempfe']) + a, np.arange(Ko['stuempfe']) + b, seed, 166) * 2 * math.pi
            rr = 10 + 8 * hash01(np.arange(Ko['stuempfe']) + b, np.arange(Ko['stuempfe']) + a, seed, 167)
            S.add(N['stumpf_nadel'] if biom_an(a, b) in NADEL_BIOME else N['stumpf_laub'], a + rr * np.sin(ang2), b + rr * np.cos(ang2), 'koehler', True, (0, 40000), 1.0, None, 0.6, 8.0, seed=seed, kanal=168)
            S.add(N['holzstapel'][1:] + N['fass'] + N['kiste'], [a + 6, a + 7, a + 5.5], [b - 5, b - 4, b - 6.5], 'koehler', True, (0, 25000), 1.0, None, 0.4, 5.0, seed=seed, kanal=169)
            punkte.append({'typ': R['rauch']['koehler'], 'x': round(float((b + wj0 - X0) * 100), 1), 'y': round(float((a + wi0 - Y0) * 100), 1), 'z': round(float((hoehe[a, b] + R['rauch']['hoehe_ueber_boden_m']) * 100), 1), 'staerke': Ko['rauch_staerke']})
            flaechen.append({'typ': 'koehlerplatz', 'mitte_cm': [round(float((b + wj0 - X0) * 100), 1), round(float((a + wi0 - Y0) * 100), 1)], 'radius_m': Ko['platz_radius_m'], 'lage_vorschlag': 'Erde'})
            n_ko += 1
        stat['koehler'] = stat.get('koehler', 0) + (n_ko)

        # ------------------------------------------------------------------ Gräber
        Gr = R['graeber']
        n_fh, n_eg = 0, 0
        for o in orte_gross:
            if o['radius'] < Gr['friedhof_min_ort_radius_m'] or not o['im_feld']:
                continue
            if not zone.gate('friedhof', o['i'], o['j']) or not zone.gate('grab', o['i'], o['j']):
                continue
            kand = frei_basis & (hang < 10) & (d_ort >= Gr['friedhof_ring_m'][0]) & (d_ort <= Gr['friedhof_ring_m'][1]) & (d_weg > 5) & (lab_voll == 0)
            kand &= np.hypot(ii - o['i'], jj - o['j']) < o['radius'] + Gr['friedhof_ring_m'][1] + 10
            sc = hash01(gi, gj, seed, 171)
            ci, cj = wahl_je_raster(kand, sc, 30, ii, jj)
            platziert = False
            for a, b in zip(ci[np.argsort(sc[ci, cj])][:10], cj[np.argsort(sc[ci, cj])][:10]):
                la, lb = Gr['friedhof_groesse_m']
                wk = float(tang_yaw[a, b]) if d_weg[a, b] < 60 else h1(a, b, seed, 172) * math.pi
                e = rechteck_ecken(a, b, la, lb, wk)
                if not rechteck_frei(e, frei_basis & (hang < 12) & (d_weg > 4), H, W):
                    continue
                if any(math.hypot(f[0] - a, f[1] - b) < (math.hypot(f[2], f[3]) + math.hypot(la, lb)) / 2 + 3 for f in felder_ok):
                    continue
                c, s_ = math.cos(wk), math.sin(wk)
                ra = Gr['reihe_m'][0] + h1(a, b, seed, 173) * (Gr['reihe_m'][1] - Gr['reihe_m'][0])
                u = (np.arange(int((la - 2) // ra)) + 0.5) * ra - (la - 2) / 2
                v = (np.arange(int((lb - 2) // 2.2)) + 0.5) * 2.2 - (lb - 2) / 2
                uu, vv = np.meshgrid(u, v)
                fi_ = a + uu.ravel() * s_ - vv.ravel() * c
                fj_ = b + uu.ravel() * c + vv.ravel() * s_
                keep = hash01(np.round(fi_ * 3).astype(np.int64) + wi0, np.round(fj_ * 3).astype(np.int64) + wj0, seed, 174) < 0.7
                ms = Gr['kreuz_massstab'][0] + (Gr['kreuz_massstab'][1] - Gr['kreuz_massstab'][0]) * hash01(np.round(fi_).astype(np.int64), np.round(fj_).astype(np.int64), seed, 175)
                roll = (hash01(np.round(fi_ * 2).astype(np.int64), np.round(fj_ * 2).astype(np.int64), seed, 176) - 0.5) * 2 * math.radians(Gr['kreuz_kippen_grad'])
                S.add(N['kreuz'], fi_[keep], fj_[keep], 'grab', False, (0, 20000), ms[keep], np.full(int(keep.sum()), wk + math.pi / 2, np.float32), 0.2, 5.0, roll=roll[keep], seed=seed, kanal=177)
                stein = o['biom'] in R['mauer']['biome_stein']
                for k in range(4):
                    if stein:
                        mauer_setzen(S, e[k], e[(k + 1) % 4], R, seed, 178 + k, a, b)
                    else:
                        fi2, fj2, yw2 = linie_punkte(e[k], e[(k + 1) % 4], N['zaun_holz_laenge_m'])
                        S.add(N['zaun_holz'], fi2, fj2, 'grab', True, (0, 40000), 1.0, np.full(fi2.size, yw2, np.float32), 0.6, 6.0, seed=seed, kanal=182)
                if h1(a, b, seed, 183) < Gr['totbaum_anteil']:
                    S.add(N['totbaum'], [e[0][0] + 1.5], [e[0][1] + 1.5], 'grab', True, (0, 0), 1.0, None, 0.05, 15.0, akteur=True, seed=seed, kanal=184)
                flaechen.append({'typ': 'friedhof', 'ecken_cm': ecken_welt(e, win), 'lage_vorschlag': 'Wiese', 'ort': o['id'], 'umfriedung': 'mauer' if stein else 'zaun'})
                felder_ok.append((a, b, la, lb, wk, o))
                platziert = True
                n_fh += 1
                break
            if not platziert:
                hinweise.append('Ort %d: kein freier Friedhofsplatz gefunden' % o['id'])
        band = frei_basis & (d_weg >= Gr['einzel_weg_abstand_m'][0]) & (d_weg <= Gr['einzel_weg_abstand_m'][1]) & (d_ort > 100) & (hang < 15)
        raster = int(1000.0 / max(0.1, Gr['einzel_je_km_weg']) / 1.6)
        ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 185), raster, ii, jj)
        keep = hash01(ci + wi0, cj + wj0, seed, 186) < 0.6 * feld_faktor
        for a, b in zip(ci[keep], cj[keep]):
            if not zone.gate('grab', a, b):
                continue
            yw = float(normal_yaw[a, b])
            S.add(N['kreuz'], [a], [b], 'grab', False, (0, 20000), 1.0 + 0.3 * h1(a, b, seed, 187), [yw], 0.2, 5.0, roll=np.array([(h1(a, b, seed, 188) - 0.5) * 0.3], np.float32), seed=seed, kanal=189)
            ang = hash01(np.arange(Gr['einzel_steine']) + a, np.arange(Gr['einzel_steine']) + b, seed, 190) * 2 * math.pi
            S.add(N['steinmann'], a + 0.6 * np.sin(ang), b + 0.6 * np.cos(ang), 'grab', False, (0, 12000), 0.8, None, 1.0, 10.0, seed=seed, kanal=191)
            S.add(N['ast'], [a + 1.2], [b - 0.8], 'grab', False, (0, 12000), 1.0, None, 1.0, 3.0, seed=seed, kanal=192)
            n_eg += 1
        stat['friedhoefe'] = stat.get('friedhoefe', 0) + (n_fh)
        stat['einzelgraeber'] = stat.get('einzelgraeber', 0) + (n_eg)


        # Sonderformen der Biom-Planer (nur in dieser Zone)
        sf = {}
        for name, fn in (('kopfweiden_reihe', lambda: sf_kopfweiden(K, zone, orte_gross)), ('pferch', lambda: sf_pferch(K, zone, orte_gross)),
                         ('mauer_frei', lambda: sf_freie_mauern(K, zone)), ('steinkreis', lambda: sf_steinkreis(K, zone)),
                         ('huegelgrab', lambda: sf_huegelgrab(K, zone)), ('ruine', lambda: sf_ruine(K, zone, 'ruine')),
                         ('tempelruine', lambda: sf_ruine(K, zone, 'tempelruine')), ('galgen_ersatz', lambda: sf_galgen(K, zone)),
                         ('brunnen', lambda: sf_brunnen(K, zone, orte_gross)), ('pfaehle', lambda: sf_pfaehle(K, zone)),
                         ('knueppeldamm', lambda: sf_knueppeldamm(K, zone)), ('lava_punkte', lambda: sf_lava_punkte(K, zone)),
                         ('schrein_stein', lambda: sf_schrein_stein(K, zone)), ('zusatzklassen', lambda: sf_zusatzklassen(K, zone))):
            n = fn()
            if n:
                sf[name] = n
        if sf:
            stat.setdefault('sonderformen', {})[zone.name] = sf

    for zone in zonen:
        zone_planen(zone.R, zone)
    typen_ov = {}
    for zone in zonen:  # Blickziel-Typen der Biom-Overrides
        for k, v in (zone.R.get('blickziele', {}).get('typ_je_biom') or {}).items():
            if k in BIOME15 and zone.thema and (zuordnung or BIOM_PLANER_VORGABE).get(k) == zone.thema and isinstance(v, list) and v:
                typen_ov[k] = v

    # ------------------------------------------------------------------ Blickziele (Vorschläge, keine Instanzen)
    tiefer = 1.0 - box_blur((hoehe - mittel > 0).astype(np.float32), rk)  # Anteil der Umgebung, die tiefer liegt ≈ Sichtbarkeit
    kand = kuppe & (prominenz >= Bz['prominenz_min_m']) & (hang <= Bz['hang_max_grad']) & im_feld
    sc = -(prominenz + 20 * tiefer + 5 * (d_weg < 150)) + hash01(gi, gj, seed, 201)
    ci, cj = wahl_je_raster(kand, sc, 200, ii, jj)
    typen = dict(Bz['typ_je_biom'])
    typen.update(typen_ov)
    o7 = np.argsort(sc[ci, cj]) if ci.size else []
    for a, b in zip(ci[o7][:Bz['max_je_feld']], cj[o7][:Bz['max_je_feld']]):
        bm = biom_an(a, b)
        tl = typen.get(bm, ['ruine'])
        typ = tl[int(h1(a, b, seed, 202) * len(tl)) % len(tl)]
        if typ == 'blumenlichtung' and not lichtung[a, b]:
            typ = tl[0] if tl[0] != 'blumenlichtung' else 'solitaerbaum'
        if typ == 'solitaerbaum' and beschattung[a, b] > 0.15:
            typ = 'ruine'
        blickziele.append({'typ': typ, 'x': round(float((b + wj0 - X0) * 100), 1), 'y': round(float((a + wi0 - Y0) * 100), 1), 'z': round(float(hoehe[a, b] * 100), 1),
                           'prominenz_m': round(float(prominenz[a, b]), 1), 'sichtbar_anteil': round(float(tiefer[a, b]), 2), 'weg_m': round(float(d_weg[a, b]), 0),
                           'regel': 'Kuppe: lokales Maximum %d m, Prominenz ≥ %d m, Hang ≤ %d°, Typ nach Biom %s' % (Bz['kuppen_fenster_m'], Bz['prominenz_min_m'], Bz['hang_max_grad'], bm)})
    # Blumenlichtung als zusätzlicher Vorschlag (größte Lichtung im Feld)
    lg = lichtung_gross & im_feld & (d_weg < 200)
    if lg.any() and len(blickziele) < Bz['max_je_feld'] + 1:
        ci, cj = wahl_je_raster(lg, hash01(gi, gj, seed, 203), 1008, ii, jj)
        a, b = int(ci[0]), int(cj[0])
        blickziele.append({'typ': 'blumenlichtung', 'x': round(float((b + wj0 - X0) * 100), 1), 'y': round(float((a + wi0 - Y0) * 100), 1), 'z': round(float(hoehe[a, b] * 100), 1),
                           'regel': 'Lichtung ≥ 150 m² (Beschattung < 0,18) im Wald (Waldanteil 60 m > 0,3), Weg < 200 m'})

    # ------------------------------------------------------------------ Budget und Ausgabe
    hinweise[:] = list(dict.fromkeys(hinweise))
    S.budget(int(R['budget']['instanzen_je_feld'] * feld_faktor_budget(faktor)), int(R['budget']['kollision_je_feld']), seed,
             R['budget'].get('prioritaet', ['feld', 'mauer', 'zaun', 'grab', 'holzschlag', 'koehler', 'steg', 'wegkreuz', 'karren', 'steinmann', 'obstgarten', 'schrein']), hinweise)
    dateien, gesamt, koll, je_gruppe = S.schreibe(ausgabe)
    if S.gesperrt:
        hinweise.append('%d Instanzen auf Wasser/Weg/Ort verworfen (Steg-Teile über Wasser erlaubt)' % S.gesperrt)
    if koll > R['budget']['kollision_je_feld'] or gesamt > R['budget']['instanzen_je_feld']:
        hinweise.append('WARNUNG: %d Instanzen / %d mit Kollision (inkl. Akteure) über Deckel %d / %d' % (gesamt, koll, R['budget']['instanzen_je_feld'], R['budget']['kollision_je_feld']))
    if len(S.akteure) > R['budget']['akteure_je_feld']:
        hinweise.append('WARNUNG: %d Akteure > Budget %d' % (len(S.akteure), R['budget']['akteure_je_feld']))
    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'ebene': EBENE, 'instanzen': int(gesamt), 'dateien': dateien,
            'entfernen': R.get('entfernen', ''), 'ft_ordner': R['ft_ordner'], 'ft_praefix': R['ft_praefix'],
            'biome_fenster': biome_fenster, 'zellen_zustaendig': zellen_zustaendig, 'biome_eigen': list(BIOME15),
            'kollision_anzahl': int(koll), 'overrides': ov_info,
            'akteure': S.akteure, 'punkte': punkte, 'flaechen': flaechen, 'blickziele': blickziele,
            'orte': [{'id': o['id'], 'x': round(float((o['j'] + wj0 - X0) * 100), 1), 'y': round(float((o['i'] + wi0 - Y0) * 100), 1), 'radius_m': round(o['radius'], 1),
                      'flaeche_m2': int(o['flaeche_m2']), 'biom': o['biom'], 'im_feld': o['im_feld']} for o in orte],
            'statistik': dict(stat, je_gruppe=je_gruppe, kollision=int(koll), akteure=len(S.akteure), rauchpunkte=len(punkte), faktor=faktor,
                              laufzeit_s=round(time.time() - t0, 1), numba=NUMBA),
            'hinweis_setzer': "Einträge mit rolle 'akteur' (Dateien akteur_<Netz>.f32, Liste 'akteure') als StaticMeshActor setzen (Ordner Spuren/<Feld>), "
                             "alle anderen als HISM-Foliage FT_EL_SP_<Netz>; 'punkte' typ herd/meiler/lagerfeuer = Rauch-Partikel (Niagara) an x,y,z; "
                             "typ steg = Stegachse; 'flaechen' = Rechtecke/Kreise zum Malen der Landschaftslage (lage_vorschlag).",
            'hinweise': hinweise, 'ungetestet': 'Korrektur Runde 1: in der Cloud nur mit synthetischen Daten rauchgetestet'}
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s: %d Instanzen (%d Kollision), %d Akteure, %d Rauch-/Stegpunkte, %d Flächen, %d Blickziele, %.1f s' % (feld, gesamt, koll, len(S.akteure), len(punkte), len(flaechen), len(blickziele), time.time() - t0))
    for h in hinweise:
        meld('  Hinweis:', h)

    if bild:
        try:
            from PIL import Image, ImageDraw
        except Exception:
            meld('Pillow fehlt – kein Prüfbild')
            return plan
        fi0, fi1, fj0, fj1 = fb[0] - wi0, fb[1] - wi0, fb[2] - wj0, fb[3] - wj0
        hh = hoehe[fi0:fi1, fj0:fj1]
        g = np.clip((hh - hh.min()) / max(1e-3, float(hh.max() - hh.min())), 0, 1) * 110 + 70
        rgb = np.stack([g, g, g], axis=2)
        bsh = beschattung[fi0:fi1, fj0:fj1]
        rgb[..., 0] *= (1 - 0.5 * bsh)
        rgb[..., 2] *= (1 - 0.5 * bsh)
        rgb[wasser_m[fi0:fi1, fj0:fj1]] = (40, 80, 200)
        rgb[weg_m[fi0:fi1, fj0:fj1]] = (120, 80, 40)
        rgb[ort_m[fi0:fi1, fj0:fj1]] = (200, 40, 40)
        farben = R.get('bild_farben', {})
        for r in S.rows:
            c = farben.get(r['gruppe'], [255, 255, 255])
            pi = np.round(r['fi']).astype(np.int32) - fi0
            pj = np.round(r['fj']).astype(np.int32) - fj0
            ok = (pi >= 0) & (pi < fi1 - fi0) & (pj >= 0) & (pj < fj1 - fj0)
            rgb[pi[ok], pj[ok]] = c
        img = Image.fromarray(rgb.astype(np.uint8))
        d = ImageDraw.Draw(img)
        for p in punkte:
            x = p['x'] / 100 + X0 - wj0 - fj0
            y = p['y'] / 100 + Y0 - wi0 - fi0
            d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=tuple(farben.get('rauch', [255, 0, 0])))
        for bz in blickziele:
            x = bz['x'] / 100 + X0 - wj0 - fj0
            y = bz['y'] / 100 + Y0 - wi0 - fi0
            d.rectangle([x - 6, y - 6, x + 6, y + 6], outline=tuple(farben.get('blickziel', [0, 255, 255])))
        os.makedirs(os.path.join(basis, 'docs', 'pruefung', 'spuren'), exist_ok=True)
        img.save(os.path.join(basis, 'docs', 'pruefung', 'spuren', feld + '.png'))
    return plan


def feld_faktor_budget(faktor):
    """Der Deckel je Feld bleibt unabhängig von --faktor (FORMAT.md §3); --faktor skaliert nur Dichten."""
    return 1.0


def mauer_setzen(S, p0, p1, R, seed, kanal, a, b):
    """Trockenmauer aus Einzelsteinen entlang p0→p1: 3 Lagen, Steinabstand, seitlicher Jitter, Eingraben der Basislage."""
    M = R['mauer']
    N = R['netze']
    fi_, fj_, yw = linie_punkte(p0, p1, M['stein_abstand_m'])
    if fi_.size == 0:
        return 0
    n = 0
    qi, qj = math.cos(yw), -math.sin(yw)
    for li, (zl, anteil) in enumerate(zip(M['lagen'], M['lagen_anteil'])):
        k = np.arange(fi_.size)
        keep = hash01(k + int(a) * 3 + li, k + int(b) * 7 + li * 11, seed, kanal) < anteil
        jit = (hash01(k + int(a) + li * 5, k + int(b) * 2, seed, kanal + 1) - 0.5) * 2 * M['jitter_m']
        ms = M['massstab'][0] + (M['massstab'][1] - M['massstab'][0]) * hash01(k * 3 + int(a), k + int(b) + li, seed, kanal + 2)
        versatz = (li % 2) * M['stein_abstand_m'] * 0.5
        fi2 = fi_ + qi * jit + math.sin(yw) * versatz
        fj2 = fj_ + qj * jit + math.cos(yw) * versatz
        n += S.add(N['mauer_stein'] + N['mauer_stein_moos'][:1], fi2[keep], fj2[keep], 'mauer', M['kollision'], (0, 30000), ms[keep], None, 0.8,
                   M['eingraben_cm'] if li == 0 else 0.0, z_offset_m=np.full(int(keep.sum()), zl, np.float32), seed=seed, kanal=kanal + 3)
    return n


def steinmann_setzen(S, a, b, R, seed, kanal):
    """Steinmann: 5–9 Steine aufeinander, Maßstab nimmt nach oben ab, kleiner seitlicher Versatz."""
    Sm = R['steinmann']
    N = R['netze']
    n = int(Sm['steine'][0] + h1(a, b, seed, kanal) * (Sm['steine'][1] - Sm['steine'][0] + 1))
    k = np.arange(n)
    ms0 = Sm['basis_massstab'][0] + h1(a, b, seed, kanal + 1) * (Sm['basis_massstab'][1] - Sm['basis_massstab'][0])
    ms = ms0 * Sm['abnahme'] ** k
    z = np.cumsum(np.concatenate([[0.0], (Sm['hoehe_versatz_m'] * ms[:-1])])) - 0.10
    ang = hash01(k + int(a), k + int(b), seed, kanal + 2) * 2 * math.pi
    jit = 0.06 * np.sqrt(k)
    yaw = hash01(k * 7 + int(a), k + int(b), seed, kanal + 3) * 2 * math.pi
    S.add(N['steinmann'], a + jit * np.sin(ang), b + jit * np.cos(ang), 'steinmann', Sm['kollision'], (0, 30000), ms, yaw, 0.6, 0.0, z_offset_m=z, seed=seed, kanal=kanal + 4)
    return 1


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
        for p in fehlt:
            meld('   fehlt:', p)
        abbruch('%d Netzpfade der %s-Regeln fehlen im Inventar %s - Einkaufsliste/Regeln abgleichen' % (len(fehlt), thema, csv))
    meld('%d Netzpfade gegen %s geprüft: alle vorhanden' % (len(pfade), csv))


def main():
    ap = argparse.ArgumentParser(description='Eldarien Spuren-Planer (Zaeune, Mauern, Steinmaenner, Wegkreuze, Karren, Stege, Holzschlag, Koehler, Graeber, Rauch, Blickziele)')
    ap.add_argument('felder', nargs='+')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    a = ap.parse_args()
    rp = a.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spuren_regeln.json')
    if not os.path.isfile(rp):
        abbruch('Regeldatei fehlt: %s' % rp)
    try:
        regeln = json.load(open(rp, encoding='utf-8'))
    except Exception as e:
        abbruch('Regeldatei unlesbar: %s (%s)' % (rp, e))
    pruefe_netze(regeln, a.basis, 'Spuren')
    inventar, _ = lade_inventar(a.basis)
    ov, zuordnung, ov_hinw = lade_spuren_overrides(regeln, rp)
    for h in ov_hinw:
        meld(h)
    pfade = Pfade(inventar)
    for thema in sorted(ov):  # Überblick einmal je Lauf: was aus dem Block umgesetzt wird, was nicht, was unbekannt ist
        info = {}
        for b in sorted(x for x, t in zuordnung.items() if t == thema):
            spuren_aufloesen(regeln, ov[thema][0], thema, b, None, pfade, info)
        meld('Override %s: umgesetzt %s' % (os.path.basename(ov[thema][1]), ', '.join(sorted(info.get('umgesetzt', [])))))
        if info.get('nicht_umgesetzt'):
            meld('Override %s: nicht umgesetzt %s' % (os.path.basename(ov[thema][1]), info['nicht_umgesetzt']))
        if info.get('unbekannte_schluessel'):
            meld('Override %s: unbekannte Schluessel ignoriert %s' % (os.path.basename(ov[thema][1]), sorted(info['unbekannte_schluessel'])))
        if info.get('netze_verworfen'):
            meld('Override %s: Netze nicht im Inventar verworfen %s' % (os.path.basename(ov[thema][1]), sorted(info['netze_verworfen'])))
    if not NUMBA:
        meld('numba nicht verfügbar – reiner NumPy-Pfad (ausreichend)')
    for feld in a.felder:
        plane_feld(feld.strip().upper(), a.basis, regeln, a.faktor, a.bild, ov, zuordnung, inventar)


if __name__ == '__main__':
    main()
