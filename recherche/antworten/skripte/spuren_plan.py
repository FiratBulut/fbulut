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

    def __init__(self, hoehe, nx, ny, nz, win, im_feld, sperre_land, sperre_wasser):
        self.h, self.nx, self.ny, self.nz, self.win, self.im_feld = hoehe, nx, ny, nz, win, im_feld
        self.sperre_land = sperre_land      # Wasser | Weg | Ort: hier steht nie eine Instanz
        self.sperre_wasser = sperre_wasser  # Weg | Ort: für Steg-Teile, die bewusst über dem Wasser stehen
        self.H, self.W = hoehe.shape
        self.rows = []
        self.akteure = []
        self.gesperrt = 0

    def add(self, pfade, fi, fj, gruppe, kollision=True, sichtweite=(0, 45000), massstab=1.0, yaw=None, kippen=0.3,
            eingraben_cm=5.0, z_offset_m=None, roll=None, akteur=False, netz_wahl=None, seed=0, kanal=0, nur_feld=True, z_abs_m=None,
            auf_wasser=False):
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
        frei = ~(self.sperre_wasser if auf_wasser else self.sperre_land)[mi, mj]
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
            koll_je_name[r['name']] = koll_je_name.get(r['name'], False) or r['kollision']
        for r in self.rows:
            r['kollision'] = koll_je_name[r['name']]  # ein Foliage-Typ je Netz → eine Kollisionseinstellung (Vereinigung)

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


# ----------------------------------------------------------------------------- Planung
def plane_feld(feld, basis, regeln, faktor, bild):
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

    frei_basis = ~wasser_m & ~nah_wasser & ~ort_m & ~nah_baum
    S = Sammler(hoehe, n_x, n_y, n_z, win, im_feld, wasser_m | weg_m | ort_m, weg_m | ort_m)
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

    # Rauchsäulen in Orten
    for o in orte:
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
    felder_ok = []  # (ci, cj, a, b, winkel) in Fensterkoordinaten
    orte_gross = [o for o in orte if o['gross']]
    # Obstgarten je großem Ort
    Og = R['obstgarten']
    n_obst = 0
    for o in orte_gross:
        if o['radius'] < Og['min_ort_radius_m'] or not o['im_feld']:
            continue
        arten = N['obstbaum'].get(o['biom'], [])
        if not arten:
            continue
        kand = erlaubt_feld & (d_ort >= Og['ring_m'][0]) & (d_ort <= Og['ring_m'][1]) & (lab_voll == 0)
        sc = hash01(gi, gj, seed, 51) + np.hypot(ii - o['i'], jj - o['j']) / 400.0
        ci, cj = wahl_je_raster(kand, sc, 40, ii, jj)
        if ci.size == 0:
            continue
        for a, b in zip(ci[np.argsort(sc[ci, cj])][:40], cj[np.argsort(sc[ci, cj])][:40]):
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
            n_obst += 1
            break
    stat['obstgaerten'] = n_obst
    if orte_gross:
        kand = erlaubt_feld & (d_ort >= ring0) & (d_ort <= ring1)
        sc = hash01(gi, gj, seed, 21)
        ci, cj = wahl_je_raster(kand, sc, int(Fs['raster_m']), ii, jj)
        keep = hash01(ci + wi0, cj + wj0, seed, 22) < Fs['anteil_zellen'] * feld_faktor
        ci, cj = ci[keep], cj[keep]
        o3 = np.argsort(hash01(ci + wi0, cj + wj0, seed, 23))
        je_ort = {}
        for a, b in zip(ci[o3], cj[o3]):
            if len(felder_ok) >= Fs['max_je_feld']:
                break
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
            je_ort[oo['id']] = je_ort.get(oo['id'], 0) + 1
    for (a, b, la, lb, wk, oo) in felder_ok:
        e = rechteck_ecken(a, b, la, lb, wk)
        bm = biom_an(a, b)
        stein = bm in R['mauer']['biome_stein']
        frucht = h1(a, b, seed, 26) < Fs['anteil_frucht']
        flaechen.append({'typ': 'feldstreifen', 'ecken_cm': ecken_welt(e, win), 'lage_vorschlag': Fs['lage_vorschlag_frucht'] if frucht else Fs['lage_vorschlag'],
                         'ort': oo['id'], 'umfriedung': 'mauer' if stein else 'zaun'})
        # Umfriedung
        for k in range(4):
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
    stat['feldstreifen'] = len(felder_ok)


    # ------------------------------------------------------------------ Zäune/Mauern am Weg vor Orten
    Zw = R['zaun_weg']
    n_zw = 0
    for o in orte_gross:
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
            if bm in R['mauer']['biome_stein']:
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
    stat['zaun_weg_segmente'] = n_zw

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
        n_sm += steinmann_setzen(S, a, b, R, seed, 73)
    # b) Kuppen und Pässe (Weg über Kuppe)
    band = bio_stein & kuppe & frei_basis & (d_ort > 40)
    ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 74), int(Sm['kuppen_fenster_m']), ii, jj)
    for a, b in zip(ci, cj):
        n_sm += steinmann_setzen(S, a, b, R, seed, 75)
    # c) frei in der Landschaft
    raster = int(math.sqrt(1.0e6 / max(1.0, Sm['frei_je_km2'])))
    band = bio_stein & frei_basis & (d_weg > 20) & (d_ort > 60) & (hang < 25)
    ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 76), raster, ii, jj)
    keep = hash01(ci + wi0, cj + wj0, seed, 77) < 0.7 * feld_faktor
    for a, b in zip(ci[keep], cj[keep]):
        n_sm += steinmann_setzen(S, a, b, R, seed, 78)
    stat['steinmaenner'] = n_sm

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
        bm = biom_an(a, b)
        yw = float(normal_yaw[a, b])  # Front zum Weg
        schrein = bm in Wk['biome_schrein'] and h1(a, b, seed, 82) < Wk['schrein_anteil']
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
    stat['wegkreuze_schreine'] = n_wk

    # ------------------------------------------------------------------ verlassene Karren
    Kr = R['karren']
    band = frei_basis & (d_weg >= Kr['weg_abstand_m'][0]) & (d_weg <= Kr['weg_abstand_m'][1]) & (d_ort > Kr['ort_min_m']) & (hang < 18)
    raster = int(1000.0 / max(0.1, Kr['je_km_weg']) / 1.6)
    ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 101), raster, ii, jj)
    keep = hash01(ci + wi0, cj + wj0, seed, 102) < 0.65 * feld_faktor
    n_kr = 0
    for a, b in zip(ci[keep], cj[keep]):
        schwer = h1(a, b, seed, 103) < Kr['anteil_schwer']
        yw = float(tang_yaw[a, b]) + (h1(a, b, seed, 104) - 0.5) * math.radians(30)
        roll = math.radians(Kr['kippen_grad'][0] + h1(a, b, seed, 105) * (Kr['kippen_grad'][1] - Kr['kippen_grad'][0])) * (1 if h1(a, b, seed, 106) < 0.5 else -1)
        S.add(N['karren_schwer'] if schwer else N['karren'], [a], [b], 'karren', True, (0, 0), 1.0, [yw], 1.0, 8.0, roll=np.array([roll], np.float32), akteur=True, seed=seed, kanal=107)
        nb = int(Kr['beiwerk'][0] + h1(a, b, seed, 108) * (Kr['beiwerk'][1] - Kr['beiwerk'][0] + 1))
        ang = hash01(np.arange(nb) + a, np.arange(nb) + b, seed, 109) * 2 * math.pi
        rad = 1.4 + 1.6 * hash01(np.arange(nb) + b, np.arange(nb) + a, seed, 110)
        S.add(N['fass'] + N['kiste'] + N['rad'] + N['sack'], a + rad * np.sin(ang), b + rad * np.cos(ang), 'karren', True, (0, 25000), 1.0, None, 0.5, 4.0, seed=seed, kanal=111)
        n_kr += 1
    stat['karren'] = n_kr

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
                if not im_feld[a, b]:
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
    stat['stege'] = n_st

    # ------------------------------------------------------------------ Holzschlag-Lichtungen
    Hs = R['holzschlag']
    n_hs = 0
    lichtung_gross = box_blur(lichtung.astype(np.float32), 7) > 0.6  # ≈ 150 m² zusammenhängend
    band = lichtung_gross & frei_basis & (d_weg <= Hs['weg_max_m']) & (d_weg > 8) & (d_ort > 60) & (hang < 20)
    ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 131), 200, ii, jj)
    o5 = np.argsort(hash01(ci + wi0, cj + wj0, seed, 132)) if ci.size else []
    for a, b in zip(ci[o5][:Hs['max_je_feld']], cj[o5][:Hs['max_je_feld']]):
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
    stat['holzschlag'] = n_hs

    # ------------------------------------------------------------------ Köhlerplätze
    Ko = R['koehler']
    n_ko = 0
    band = frei_basis & (beschattung >= Ko['beschattung'][0]) & (beschattung <= Ko['beschattung'][1]) & (hang <= Ko['hang_max_grad'])
    band &= (d_weg >= Ko['weg_m'][0]) & (d_weg <= Ko['weg_m'][1]) & (d_ort > 80) & ~dilate(baum_m, Ko['platz_radius_m'])
    ci, cj = wahl_je_raster(band, hash01(gi, gj, seed, 161), 300, ii, jj)
    o6 = np.argsort(hash01(ci + wi0, cj + wj0, seed, 162)) if ci.size else []
    for a, b in zip(ci[o6][:Ko['max_je_feld']], cj[o6][:Ko['max_je_feld']]):
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
    stat['koehler'] = n_ko

    # ------------------------------------------------------------------ Gräber
    Gr = R['graeber']
    n_fh, n_eg = 0, 0
    for o in orte_gross:
        if o['radius'] < Gr['friedhof_min_ort_radius_m'] or not o['im_feld']:
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
        yw = float(normal_yaw[a, b])
        S.add(N['kreuz'], [a], [b], 'grab', False, (0, 20000), 1.0 + 0.3 * h1(a, b, seed, 187), [yw], 0.2, 5.0, roll=np.array([(h1(a, b, seed, 188) - 0.5) * 0.3], np.float32), seed=seed, kanal=189)
        ang = hash01(np.arange(Gr['einzel_steine']) + a, np.arange(Gr['einzel_steine']) + b, seed, 190) * 2 * math.pi
        S.add(N['steinmann'], a + 0.6 * np.sin(ang), b + 0.6 * np.cos(ang), 'grab', False, (0, 12000), 0.8, None, 1.0, 10.0, seed=seed, kanal=191)
        S.add(N['ast'], [a + 1.2], [b - 0.8], 'grab', False, (0, 12000), 1.0, None, 1.0, 3.0, seed=seed, kanal=192)
        n_eg += 1
    stat['friedhoefe'] = n_fh
    stat['einzelgraeber'] = n_eg

    # ------------------------------------------------------------------ Blickziele (Vorschläge, keine Instanzen)
    tiefer = 1.0 - box_blur((hoehe - mittel > 0).astype(np.float32), rk)  # Anteil der Umgebung, die tiefer liegt ≈ Sichtbarkeit
    kand = kuppe & (prominenz >= Bz['prominenz_min_m']) & (hang <= Bz['hang_max_grad']) & im_feld
    sc = -(prominenz + 20 * tiefer + 5 * (d_weg < 150)) + hash01(gi, gj, seed, 201)
    ci, cj = wahl_je_raster(kand, sc, 200, ii, jj)
    typen = Bz['typ_je_biom']
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
            'kollision_anzahl': int(koll),
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
    if not NUMBA:
        meld('numba nicht verfügbar – reiner NumPy-Pfad (ausreichend)')
    for feld in a.felder:
        plane_feld(feld.strip().upper(), a.basis, regeln, a.faktor, a.bild)


if __name__ == '__main__':
    main()
