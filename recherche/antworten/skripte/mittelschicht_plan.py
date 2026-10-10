#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien – Planer „Mittelschicht“ (Schicht 1, 0,3–3 m), Korrektur Runde 1 (10.10.2026).

Einziger Planer der generischen Mittelschicht-Klassen in allen 15 Biomen (verteilung-KONVENTIONEN.md §4):
strauch, jungbaum, farn, totholz_liegend, totholz_stumpf, totholz_ast, hochstaude, grasbueschel, beere, pilz
(+ eigene Zusatzklassen wurzel, kletter, totbaum, wo kein Biom-Planer sie als Sonderform setzt).
Biom je Zelle strikt aus eigner.r8 + welt.json (0 = Weltgelände → aue, Vulkanregion → lava); nur ohne eigner.r8
Fallback dominantes Feldbiom aus daten/biome_je_feld.json. Palette und Dichtefaktoren je Biom aus
mittelschicht_regeln.json["biome"][biom], überschrieben von `mittelschicht_overrides` des zuständigen Biom-Planers
(<thema>_regeln.json im selben Ordner wie die eigene Regeldatei, sonst ../<thema>/). Override-Schema:
    {"palette": {klasse: [pfade]}, "faktor": {klasse: float}, "zusatzklassen": {name: klassendef},
     optional "je_biom": {biom: {palette/faktor/zusatzklassen}}, "faktor_je_feld": {Feld: {klasse: float}}}
Kronendach aus bestand/, witcher/, instanzen.json und den Baum-Dateien (ebene 2) der Biom-Planer-Ebenen
nordkueste/ aue/ heide_tundra/ hochgebirge/ elfenwald/ sumpf/ dschungel/ lava/ wueste_ergaenzung/ (Feld + 8 Nachbarn);
deren Nicht-Boden-Instanzen im Feld gelten als belegt.

Aufruf (lokal, production-Wurzel):
    python -I scripts/mittelschicht/mittelschicht_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]

Liest:   export/unreal/welt/hoehe.f32 (Pflicht, memmap, Fenster Feld + 64 m), lage_*.r8, karte_wasser/weg/ort.r8,
         eigner.r8 + welt.json, daten/biome_je_feld.json, Baum-/Biom-Ebenen (s. o.), daten/netze.csv (Pfadprüfung).
Schreibt: export/unreal/welt/mittelschicht/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm, qx,qy,qz,qw, sx,sy,sz)
          + plan.json (FORMAT.md §3 + Pflichtschlüssel biome_fenster, zellen_zustaendig, biome_eigen, kollision_anzahl;
          dateien[].ebene = 1), bei --bild docs/pruefung/mittelschicht/<Feld>.png (1 px = 1 m).
          Landanteil im Fenster < 2 % → leerer plan.json (instanzen 0, keine f32).
Budget:  ≤ 60 000 Instanzen (Ziel 52 000), ≤ 3 000 mit Kollision; Ausdünnung deterministisch nach Priorität, WARNUNG im Log.
Logs:    nur ASCII (Windows/cp1252). Fehlende Pflichtdatei → Meldung, Exit-Code 2.

Nur NumPy (separierbare Box-Faltungen, Jump-Flooding-Distanzfeld, Hash-Zufall aus globaler Rasterkoordinate →
deterministisch, Nachbarfelder nahtlos). numba wird nicht benötigt. Laufzeit-Ziel ≤ 60 s je Feld.

Quellen: FORMAT.md §1–§5; verteilung-KONVENTIONEN.md; verteilung-dschungel.md §3 (verbindliche Dschungel-Palette);
bildkritik-witcher-messlatte.md; boden-kleinzeug-gras.md; Naturschutzbund „Waldränder“; Harms et al. 2004 Biotropica.

Echtdaten-Lauf der Vorfassung lokal (A5/G4/E1/C6) ohne Absturz; diese Fassung in der Cloud nur synthetisch rauchgetestet.
"""
import argparse
import copy
import json
import math
import os
import sys
import time
import zlib

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
SKRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EBENE = 1  # Schicht 1 mittel
BIOME15 = ['aue', 'bergwald', 'gletscher', 'tundra', 'canyon', 'oedland', 'heide', 'elfenwald', 'dschungel', 'kueste',
           'wueste', 'lava', 'frost', 'sumpf', 'fjord']
BIOM_PLANER_VORGABE = {'fjord': 'nordkueste', 'kueste': 'nordkueste', 'bergwald': 'nordkueste', 'aue': 'aue',
                       'heide': 'heide_tundra', 'tundra': 'heide_tundra', 'gletscher': 'hochgebirge', 'frost': 'hochgebirge',
                       'elfenwald': 'elfenwald', 'sumpf': 'sumpf', 'dschungel': 'dschungel', 'lava': 'lava',
                       'wueste': 'wueste_ergaenzung', 'canyon': 'wueste_ergaenzung', 'oedland': 'wueste_ergaenzung'}
BIOM_EBENEN = ('nordkueste', 'aue', 'heide_tundra', 'hochgebirge', 'elfenwald', 'sumpf', 'dschungel', 'lava', 'wueste_ergaenzung')
KLASSEN_ALIAS = {'totholz': 'totholz_liegend', 'stamm_liegend': 'totholz_liegend', 'stumpf': 'totholz_stumpf', 'ast': 'totholz_ast'}
KLASSE_VORGABE = {"netze": [], "dichte": [0.002, 0.002], "gruppe": [1, 1], "radius_m": 2.0, "massstab": [0.8, 1.2],
                  "eingraben_cm": 4, "kippen": 0.3, "sichtweite": [0, 30000], "kollision": False, "saum": 1.0,
                  "feuchte": [1.0, 1.0], "hang_max": 35, "hoehe_max_m": 9999, "lichtungsrand": 1.0,
                  "laengs_hang": False, "an_baum": False}
BAUM_ROLLEN = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel', 'palme',
               'hainbuche', 'tanne', 'pine', 'beech', 'palm', 'oak', 'birch', 'spruce', 'fir_', 'willow', 'poplar', 'hornbeam')
TOT_WORTE = ('tot', 'dead', 'stump', 'stumpf', 'log', 'verkohlt', 'fallen', 'schnag', 'branch', 'ast_', 'root', 'wurzel')


# ----------------------------------------------------------------------------- Ausgabe (nur ASCII)
_ASCII = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss', '→': '->', '←': '<-', '…': '...',
          '≤': '<=', '≥': '>=', '–': '-', '—': '-', '²': '2', '³': '3', '°': ' Grad', '×': 'x', '·': '*', '„': '"',
          '“': '"', '”': '"', '‚': "'", '‘': "'", '’': "'", '±': '+/-', '≈': '~', 'µ': 'u', '−': '-', '§': 'Par.'}


def asc(s):
    """Text auf ASCII abbilden (Umlaute → ae/oe/ue/ss, Pfeile/Zeichen → ASCII, Rest → '?')."""
    s = str(s)
    for k, v in _ASCII.items():
        s = s.replace(k, v)
    return s.encode('ascii', 'replace').decode('ascii')


def meld(*a):
    print(asc(' '.join(['[mittelschicht]'] + [str(x) for x in a])), flush=True)


def abbruch(text):
    """Pflichtdatei/Regelfehler: klare Meldung, Exit-Code 2 (KONVENTIONEN §5)."""
    meld('FEHLER: ' + str(text))
    sys.exit(2)


# ----------------------------------------------------------------------------- kleine Helfer
def feld_fenster(feld, rand):
    """Feld 'G4' → (i0, i1, j0, j1) des Feldes und des Fensters (geklippt auf das Raster)."""
    feld = feld.strip().upper()
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        abbruch('Unbekanntes Feld %r (A1 ... J7)' % feld)
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
            abbruch('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        meld('WARNUNG: %s hat %d Werte, erwartet %d - Datei wird ignoriert' % (pfad, n, NX * NY))
        if pflicht:
            abbruch('Pflichtdatei hat falsche Groesse: %s' % pfad)
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



# ----------------------------------------------------------------------------- Biom je Zelle (KONVENTIONEN §1)
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
    """Biom-Index (in BIOME15) je Fensterzelle. eigner.r8 + welt.json; Kennzahl 0 = Weltgelände → aue.
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
        bio = np.where(unbek, BIOME15.index(fb), bio).astype(np.int16)
    return bio.astype(np.int16), 'eigner.r8 + welt.json'


# ----------------------------------------------------------------------------- Inventar und Overrides
def lade_inventar(basis):
    """Netzpfade aus daten/netze.csv (Spalte pfad, Trenner ;) mit Netzhöhe groesse_z_m; None, wenn nicht gefunden."""
    kandidaten = [os.path.join(basis, 'daten', 'netze.csv'), os.path.join(SKRIPT_DIR, 'netze.csv'),
                  os.path.join(SKRIPT_DIR, '..', '..', 'daten', 'netze.csv')]
    csv = next((p for p in kandidaten if os.path.isfile(p)), None)
    if csv is None:
        return None, None
    inventar = {}  # pfad -> Netzhöhe in m (groesse_z_m) oder None
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
                inventar[t[sp].strip()] = z
    return inventar, csv


def lade_overrides(regeln, regel_pfad):
    """mittelschicht_overrides der Biom-Planer: {thema: (block, pfad)} + Hinweisliste.
    Gesucht: <thema>_regeln.json neben der eigenen Regeldatei, sonst ../<thema>/<thema>_regeln.json."""
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
        blk = d.get('mittelschicht_overrides')
        schluessel = ('palette', 'faktor', 'zusatzklassen', 'parameter', 'je_biom', 'faktor_je_feld', 'vorlage_biom', 'biom_faktor', 'entfernen_je_feld')
        if not isinstance(blk, dict) or not any(k in blk for k in schluessel):
            hinw.append('Override: %s ohne Block mittelschicht_overrides - eigene Werte fuer %s' % (os.path.basename(p), ', '.join(biome)))
            continue
        ov[thema] = (blk, p)
        hinw.append('Override: %s gelesen (%s) fuer %s' % (os.path.basename(p), ', '.join(k for k in schluessel if k in blk), ', '.join(biome)))
        ub = unbekannte_schluessel(blk)
        if ub:
            hinw.append('Override %s: unbekannte Schluessel ignoriert %s' % (os.path.basename(p), ub))
    return ov, zuordnung, hinw


SCHEMA6 = ('palette', 'rolle', 'dichte_je_ha', 'hang_grad', 'hoehe_m', 'wasser_abstand_m', 'lagen_min', 'kruemmung', 'massstab',
           'eingraben_anteil', 'gruppe', 'kollision', 'sichtweite', 'akteur')
KLASSEN_SCHLUESSEL = set(KLASSE_VORGABE) | set(SCHEMA6) | {
    'lagen_faktor', 'lagen', 'netze_massstab', 'netze_gewicht', 'biome', 'biom_faktor', 'schatten', 'farbe', 'lichtung', 'wegrand',
    'nah_baum', 'mulde', 'an_totholz', 'basisklasse', 'stufe', 'stufen', 'hoehe_rel_baumgrenze_m', 'hoehe_min_m'}
BLOCK_SCHLUESSEL = {'palette', 'faktor', 'zusatzklassen', 'parameter', 'je_biom', 'faktor_je_feld', 'vorlage_biom', 'biom_faktor',
                    'entfernen_je_feld', 'biom', 'gilt_fuer', 'alias', 'klassen_alias', 'klassen_alias_mittelschicht', 'herkunft'}


def doku_schluessel(k):
    k = str(k)
    return k.startswith('_') or k.startswith('herkunft') or k.endswith(('doku', 'hinweis', 'begruendung', 'quelle'))


def unbekannte_schluessel(blk):
    """Unbekannte Schlüssel eines Override-Blocks: {'block': [...], '<klasse>': [...]} (Doku-Schlüssel ausgenommen)."""
    out = {}
    ub = sorted(k for k in blk if k not in BLOCK_SCHLUESSEL and not doku_schluessel(k))
    if ub:
        out['block'] = ub
    teile = [('', blk)] + [(b + '/', t) for b, t in (blk.get('je_biom') or {}).items() if isinstance(t, dict)]
    for pre, t in teile:
        for name, kd in (t.get('zusatzklassen') or {}).items():
            if isinstance(kd, dict):
                u = sorted(k for k in kd if k not in KLASSEN_SCHLUESSEL and not doku_schluessel(k))
                if u:
                    out[pre + str(name)] = u
        for name, par in (t.get('parameter') or {}).items():
            if isinstance(par, dict):
                u = sorted(k for k in par if k not in KLASSEN_SCHLUESSEL and not doku_schluessel(k))
                if u:
                    out[pre + 'parameter.' + str(name)] = u
    return out


def schema6_klasse(kd, inventar):
    """Zusatzklasse im Mindestschema KONVENTIONEN §6 (oder im mittelschicht-Format) → mittelschicht-Klassendefinition."""
    kd = copy.deepcopy(kd)
    if 'netze' not in kd and isinstance(kd.get('palette'), list):
        kd['netze'] = kd['palette']
    rolle = str(kd.get('rolle', '')).lower()
    fest = any(r in rolle for r in ('fels', 'stein', 'block', 'stamm', 'totholz_liegend', 'baum'))
    if 'dichte' not in kd and isinstance(kd.get('dichte_je_ha'), (int, float)):
        d = float(kd['dichte_je_ha']) / 10000.0
        kd['dichte'] = [d, d]
    g = kd.get('gruppe')
    if isinstance(g, dict):
        kd['gruppe'] = list(g.get('groesse', [1, 1]))
        if 'radius_m' in g and 'radius_m' not in kd:
            kd['radius_m'] = float(g['radius_m'])
    if isinstance(kd.get('hang_grad'), list) and len(kd['hang_grad']) == 2:
        kd['hang_bereich'] = [float(x) for x in kd['hang_grad']]
        kd.setdefault('hang_max', 90)  # harte Maske statt Abfall
    if isinstance(kd.get('hoehe_m'), list) and len(kd['hoehe_m']) == 2:
        kd['hoehe_bereich'] = [float(x) for x in kd['hoehe_m']]
    if 'kollision' not in kd and fest:
        kd['kollision'] = True
    if 'eingraben_cm' not in kd:
        ant = kd.get('eingraben_anteil', [0.25, 0.45] if fest else None)
        if isinstance(ant, list) and len(ant) == 2:
            zs = [inventar.get(p) for p in kd.get('netze', [])] if isinstance(inventar, dict) else []
            zs = [z for z in zs if z]
            hz = (sum(zs) / len(zs)) if zs else 1.0
            ms = kd.get('massstab', [1.0, 1.0])
            kd['eingraben_cm'] = round(100.0 * hz * 0.5 * (ant[0] + ant[1]) * 0.5 * (ms[0] + ms[1]), 1)
    if fest:
        kd.setdefault('kippen', 0.8)
    return kd


def _klasse(name):
    return KLASSEN_ALIAS.get(str(name), str(name))


def effektive_regeln(regeln, ov, zuordnung, feld, inventar, hinweise_feld, vorhanden=None):
    """Biom → Klasse → Klassendefinition (inkl. 'faktor', 'quelle') nach Regeln, Feldfaktoren und Overrides (Overrides gewinnen).
    Faktor je Klasse = Feldfaktor × Override-faktor × biom_faktor. Feldfaktor = override faktor_je_feld[Feld] oder
    mittelschicht feld_klassen_faktor (mit nur_ohne_override nur, solange der Biom-Planer keinen Override-Block hat).
    Override-Teile: flacher Block, danach je_biom[biom]; je Teil zusatzklassen → palette → parameter → faktor → faktor_je_feld."""
    vorgabe = dict(KLASSE_VORGABE)
    vorgabe.update(regeln.get('klasse_vorgabe', {}))

    def vorlage(kname, vb=None):
        for b in ([vb] if vb else []) + BIOME15:
            if kname in regeln['biome'].get(b, {}):
                return copy.deepcopy(regeln['biome'][b][kname])
        return None

    def pfade_pruefen(pfade, wo):
        pfade = [str(p) for p in pfade if isinstance(p, str)]
        if inventar is None:
            return pfade
        fehlt = [p for p in pfade if p not in inventar]
        if fehlt:
            hinweise.append('Override %s: %d Netze nicht im Inventar verworfen (%s)' % (wo, len(fehlt), ', '.join(p.rsplit('/', 1)[-1] for p in fehlt[:5])))
        return [p for p in pfade if p in inventar]

    def lagen_alias(kd):
        if 'lagen_faktor' not in kd and isinstance(kd.get('lagen'), dict):
            kd['lagen_faktor'] = {k: float(v) for k, v in kd['lagen'].items() if isinstance(v, (int, float))}

    eff = {}
    for biom in BIOME15:
        hinweise = []  # Hinweise nur für Biome, die im Fenster vorkommen
        kl = copy.deepcopy(regeln['biome'].get(biom, {}))
        ffeld, fov = {}, {}
        for k in kl:
            kl[k]['quelle'] = 'mittelschicht'
        thema = zuordnung.get(biom)
        fk = regeln.get('feld_klassen_faktor', {}).get(biom, {})
        if feld in fk.get('felder', []):
            if fk.get('nur_ohne_override') and thema in ov:
                hinweise.append('feld_klassen_faktor %s in %s inaktiv: %s hat mittelschicht_overrides (Klassen kommen nur noch von hier)' % (biom, feld, thema))
            else:
                for k, f in fk.get('faktor', {}).items():
                    ffeld[_klasse(k)] = float(f)
                hinweise.append('feld_klassen_faktor %s in %s: %s' % (biom, feld, fk.get('faktor', {})))
        bfaktor = 1.0
        if thema in ov:
            blk, pfad = ov[thema]
            teile = [blk]
            jb = blk.get('je_biom', {})
            if isinstance(jb, dict) and isinstance(jb.get(biom), dict):
                teile.append(jb[biom])
            for t in teile:
                vb = t.get('vorlage_biom') or blk.get('vorlage_biom') or {}
                for name, kd in (t.get('zusatzklassen') or {}).items():
                    if not isinstance(kd, dict):
                        continue
                    if isinstance(kd.get('biome'), list) and biom not in kd['biome']:
                        continue
                    neu = copy.deepcopy(vorgabe)
                    neu.update(schema6_klasse(kd, inventar))
                    lagen_alias(neu)
                    neu['ist_zusatz'] = True  # nur Zellen des liefernden Bioms + Saum (KONVENTIONEN §6)
                    neu['netze'] = pfade_pruefen(neu.get('netze', []), '%s/%s/%s' % (thema, biom, name))
                    if not neu['netze']:
                        hinweise.append('Override %s/%s: Zusatzklasse %s ohne gueltige Netze - entfaellt' % (thema, biom, name))
                        continue
                    neu['zusatz_biom_faktor'] = float((kd.get('biom_faktor') or {}).get(biom, 1.0)) if isinstance(kd.get('biom_faktor'), dict) else 1.0
                    neu['quelle'] = thema
                    kl[_klasse(name)] = neu
                for k, pf in (t.get('palette') or {}).items():
                    k = _klasse(k)
                    pf = pfade_pruefen(pf if isinstance(pf, list) else [], '%s/%s/%s' % (thema, biom, k))
                    if not pf:
                        continue
                    if k not in kl:
                        v = vorlage(k, vb.get(k) if isinstance(vb, dict) else None)
                        if v is None:
                            hinweise.append('Override %s/%s: Palette fuer unbekannte Klasse %s ohne Vorlage - ignoriert (als zusatzklassen angeben)' % (thema, biom, k))
                            continue
                        kl[k] = v
                    kl[k]['netze'] = pf
                    for zus in ('netze_massstab', 'netze_gewicht'):
                        if kl[k].get(zus):
                            kl[k][zus] = {p: v for p, v in kl[k][zus].items() if p in pf}
                    kl[k]['quelle'] = thema
                for k, par in (t.get('parameter') or {}).items():
                    k = _klasse(k)
                    if k in kl and isinstance(par, dict):
                        kl[k].update(copy.deepcopy({x: y for x, y in par.items() if x != 'netze'}))
                        lagen_alias(kl[k])
                for k, f in (t.get('faktor') or {}).items():
                    if isinstance(f, (int, float)):
                        fov[_klasse(k)] = float(f)
                for k, f in ((t.get('faktor_je_feld') or {}).get(feld) or {}).items():
                    if isinstance(f, (int, float)):
                        ffeld[_klasse(k)] = float(f)
                        fov.setdefault(_klasse(k), 1.0)  # Quelle = Biom-Planer
            bf = (blk.get('biom_faktor') or {}).get(biom)
            if isinstance(bf, (int, float)):
                bfaktor = float(bf)
                hinweise.append('Override %s: biom_faktor %s = %.2f auf alle Mittelschicht-Klassen' % (thema, biom, bfaktor))
        for k in kl:
            kl[k]['faktor'] = ffeld.get(k, 1.0) * fov.get(k, 1.0) * bfaktor * float(kl[k].pop('zusatz_biom_faktor', 1.0))
            if k in fov or k in ffeld:
                kl[k]['quelle'] = kl[k].get('quelle', 'mittelschicht') if k not in fov else (thema or 'mittelschicht')
        eff[biom] = kl
        if vorhanden is None or biom in vorhanden:
            hinweise_feld.extend(hinweise)
    return eff


def override_entfernen(ov, feld):
    """entfernen_je_feld der Override-Blöcke (Witcher-Netzpräfixe, die im Feld beim Setzen der Mittelschicht entfallen)."""
    teile = []
    for thema in sorted(ov):
        e = (ov[thema][0].get('entfernen_je_feld') or {}).get(feld)
        if isinstance(e, str) and e.strip():
            teile += [x.strip() for x in e.split(',') if x.strip()]
    return teile


# ----------------------------------------------------------------------------- vorhandene Ebenen (Kronendach, belegt)
def ebene_art(info, name):
    """'baum' (Kronendach), 'boden' (ignorieren) oder 'sonst' (belegt) aus dateien[].ebene/schicht bzw. rolle/gruppe/Name."""
    txt = (str(info.get('rolle', '')) + ' ' + str(info.get('gruppe', '')) + ' ' + str(info.get('klasse', '')) + ' ' + name).lower()
    e = str(info.get('ebene', info.get('schicht', ''))).lower().strip()
    if e.startswith('2') or 'baum' in e:
        art = 'baum'
    elif e.startswith('0') or 'boden' in e:
        return 'boden'
    elif e:
        return 'sonst'
    else:
        art = 'baum' if any(r in txt for r in BAUM_ROLLEN) else 'sonst'
    if art == 'baum' and any(t in txt for t in TOT_WORTE):
        return 'sonst'  # Totbäume, Stämme, Stümpfe: kein Kronendach, aber belegt
    return art


def lade_ebene(ordner, win):
    """[(art, arr[n,3] = fi, fj, Maßstab)] einer Ebene (plan.json + <Name>.f32), nur Instanzen im Fenster."""
    out = []
    pj = os.path.join(ordner, 'plan.json')
    if not os.path.isfile(pj):
        return out
    try:
        plan = json.load(open(pj, encoding='utf-8'))
    except Exception:
        return out
    H, W = win[1] - win[0], win[3] - win[2]
    for name, info in (plan.get('dateien') or {}).items():
        f = os.path.join(ordner, name + '.f32')
        if not isinstance(info, dict) or not os.path.isfile(f):
            continue
        art = ebene_art(info, name)
        if art == 'boden':
            continue
        try:
            a = np.fromfile(f, dtype='<f4')
        except Exception:
            continue
        if a.size == 0 or a.size % 10:
            continue
        a = a.reshape(-1, 10)
        fj = a[:, 0] / 100.0 + X0 - win[2]
        fi = a[:, 1] / 100.0 + Y0 - win[0]
        m = (fi >= 0) & (fi < H) & (fj >= 0) & (fj < W)
        if m.any():
            out.append((art, np.stack([fi[m], fj[m], a[m, 9]], axis=1)))
    return out


def lade_baeume(basis, feld, win):
    """Baum-Positionen (Kronendach) aus bestand/, witcher/ und den Biom-Planer-Ebenen (Feld + 8 Nachbarn) sowie
    instanzen/instanzen.json; Nicht-Boden-Instanzen dieser Ebenen und felsgruppen/ im eigenen Feld = belegt."""
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    baum, sonst, quellen = [], [], []
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(ord('A') + ss) + str(rr)
            for ebene in ('bestand', 'witcher') + BIOM_EBENEN + ('felsgruppen',):
                teile = lade_ebene(os.path.join(basis, WELT, ebene, nf), win)
                if not teile:
                    continue
                quellen.append('%s/%s' % (ebene, nf))
                for art, arr in teile:
                    if art == 'baum' and ebene != 'felsgruppen':
                        baum.append(arr)
                    elif ds == 0 and dr == 0:
                        sonst.append(arr)
    ij = os.path.join(basis, WELT, 'instanzen', 'instanzen.json')
    if os.path.isfile(ij):
        try:
            inst = json.load(open(ij, encoding='utf-8'))
            for e in inst.get('verzeichnis', []):
                txt = (str(e.get('klasse', '')) + ' ' + str(e.get('name', ''))).lower()
                if not any(k in txt for k in BAUM_ROLLEN) or any(t in txt for t in TOT_WORTE):
                    continue
                f = os.path.join(basis, WELT, 'instanzen', e.get('datei') or (str(e.get('name', '')) + '.f32'))
                if not os.path.isfile(f):
                    continue
                a = np.fromfile(f, dtype='<f4')
                if a.size == 0 or a.size % 10:
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


# ----------------------------------------------------------------------------- Ausgabe
def leere_ausgabe(ausgabe):
    os.makedirs(ausgabe, exist_ok=True)
    for f in os.listdir(ausgabe):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))


def schreibe_plan(ausgabe, plan):
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)


def plan_kopf(feld, regeln, biome_fenster, zellen, n, nk, dateien, hinweise, entfernen=None):
    return {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'ebene': EBENE, 'instanzen': int(n), 'dateien': dateien,
            'entfernen': regeln.get('entfernen', '') if entfernen is None else entfernen, 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'biome_fenster': biome_fenster, 'zellen_zustaendig': int(zellen), 'biome_eigen': list(BIOME15),
            'kollision_anzahl': int(nk), 'hinweise': hinweise}


def klassen_kanal(bidx, kname):
    """Stabiler Hash-Kanal je Biom und Klasse (unabhängig davon, welche Zusatzklassen es sonst gibt)."""
    return bidx * 1000000 + (zlib.crc32(kname.encode('utf-8')) % 99991) * 10


# ----------------------------------------------------------------------------- Budget (KONVENTIONEN §3)
def budget_anwenden(aus, regeln, seed, wi0, wj0, hinweise):
    """Deckel 60 000 / Kollision 3 000 hart, Ziel 52 000; deterministische Ausdünnung (Hash je Zelle) nach Priorität."""
    Bg = regeln['budget']
    deckel, ziel, kdeckel = int(Bg['instanzen_je_feld']), int(Bg['ziel_instanzen_je_feld']), int(Bg['kollision_je_feld'])
    prio = [k for k in Bg['prioritaet']]
    zusatz = sorted({a['klasse'] for a in aus} - set(prio))  # Zusatzklassen der Biom-Planer: mittlere Priorität (nach hochstaude)
    pos = prio.index('hochstaude') + 1 if 'hochstaude' in prio else len(prio)
    prio = prio[:pos] + zusatz + prio[pos:]

    def zaehle():
        st = {}
        for a in aus:
            st[a['klasse']] = st.get(a['klasse'], 0) + int(a['fi'].size)
        return st, sum(st.values()), sum(int(a['fi'].size) for a in aus if a['kollision'])

    def duenne(faktoren, runde):
        for a in aus:
            f = faktoren.get(a['klasse'], 1.0)
            if f >= 1.0 or a['fi'].size == 0:
                continue
            keep = hash01(a['mi'] + wi0, a['mj'] + wj0, seed, 77777 + a['kanal'] + runde) < f
            for key in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw'):
                a[key] = a[key][keep]

    st, gesamt, koll = zaehle()
    roh, roh_k = gesamt, koll
    protokoll = {}
    for runde in range(6):  # Kollision
        if koll <= kdeckel:
            break
        f = kdeckel * (0.97 if runde == 0 else 0.9) / float(koll)
        fk = {a['klasse']: f for a in aus if a['kollision']}
        duenne(fk, runde * 13 + 1)
        for k in fk:
            protokoll[k] = round(protokoll.get(k, 1.0) * f, 3)
        st, gesamt, koll = zaehle()
    if roh_k > kdeckel:
        hinweise.append('WARNUNG Kollisionsbudget: %d -> %d (Deckel %d), gedünnt: %s' % (roh_k, koll, kdeckel, sorted({a['klasse'] for a in aus if a['kollision']})))
    vorher = gesamt
    for runde in range(6):  # Instanzen
        grenze = ziel if runde == 0 else deckel
        if gesamt <= grenze:
            break
        ueber = gesamt - (ziel if runde == 0 else int(deckel * 0.97))
        pool, summe = [], 0
        for kname in reversed(prio):  # von unten so viele Klassen, dass höchstens 50 % je Klasse wegfallen
            n = st.get(kname, 0)
            if n == 0:
                continue
            pool.append(kname)
            summe += n
            if summe * 0.5 >= ueber:
                break
        f = max(0.05, 1.0 - ueber / float(max(1, summe)))
        duenne({k: f for k in pool}, 100 + runde * 17)
        for k in pool:
            protokoll[k] = round(protokoll.get(k, 1.0) * f, 3)
        st, gesamt, koll = zaehle()
    if vorher > ziel:
        hinweise.append('WARNUNG Instanzbudget: %d -> %d (Ziel %d, Deckel %d), Ausduennung %s' % (vorher, gesamt, ziel, deckel, protokoll))
        if 'grasbueschel' in protokoll or 'pilz' in protokoll:
            hinweise.append('Kleinzeug (grasbueschel/pilz) gedünnt - Landschafts-Gras GT_* in diesen Biomen ggf. dichter stellen (KONVENTIONEN §3)')
    if gesamt > deckel or koll > kdeckel:
        hinweise.append('WARNUNG: Deckel nach Ausduennung noch ueberschritten (%d / %d Kollision)' % (gesamt, koll))
    return roh, protokoll


# ----------------------------------------------------------------------------- Höhenstufen (wie hochgebirge_plan.py)
HS_VORGABE = {"baumgrenze_m": {"gletscher": 230, "frost": 180, "tundra": 280, "fjord": 260, "bergwald": 420, "default": 320},
              "schneegrenze_m": {"gletscher": 370, "frost": 280, "tundra": 420, "fjord": 400, "bergwald": 540, "default": 470},
              "exposition_versatz_m": 45, "hang_versatz": {"ab_grad": 25, "bis_grad": 45, "versatz_m": 30}, "grat_versatz_m": 40,
              "grat_staerke_min": 0.015, "rauschen_amplitude_m": 35, "krummholz_band_m": [-60, 40],
              "schlucht": {"kruemmung_min": 0.006, "wasser_m": 25, "bonus_m": 70},
              "lage_schnee_als_stufe3_ab": 0.55, "lage_eis_als_stufe3_ab": 0.4}
U64 = np.uint64


def _hg_mix(h):
    h = np.atleast_1d(h).astype(U64, copy=True)
    with np.errstate(over='ignore'):
        h ^= h >> U64(30)
        h *= U64(0xBF58476D1CE4E5B9)
        h ^= h >> U64(27)
        h *= U64(0x94D049BB133111EB)
        h ^= h >> U64(31)
    return h


def _hg_hash64(*teile):
    h = None
    with np.errstate(over='ignore'):
        for t in teile:
            a = np.atleast_1d(np.asarray(t)).astype(np.int64).astype(U64)
            h = a * U64(0x9E3779B97F4A7C15) if h is None else _hg_mix(h ^ (a + U64(0x9E3779B97F4A7C15)))
    return _hg_mix(h)


def _hg_uni(h, salz):
    with np.errstate(over='ignore'):
        return (_hg_mix(h ^ U64((salz * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)) >> U64(11)).astype(np.float64) * (1.0 / 9007199254740992.0)


def _hg_wertrauschen(ii, jj, gitter, seed, salz):
    gi = ii / float(gitter)
    gj = jj / float(gitter)
    i0 = np.floor(gi).astype(np.int64)
    j0 = np.floor(gj).astype(np.int64)
    fi = gi - i0
    fj = gj - j0
    fi = fi * fi * (3 - 2 * fi)
    fj = fj * fj * (3 - 2 * fj)

    def v(di, dj):
        return _hg_uni(_hg_hash64(seed, salz, i0 + di, j0 + dj), 7)
    return v(0, 0) * (1 - fi) * (1 - fj) + v(0, 1) * (1 - fi) * fj + v(1, 0) * fi * (1 - fj) + v(1, 1) * fi * fj


def _hg_gauss1d(a, sigma, axis):
    r = max(1, int(3.0 * sigma + 0.5))
    x = np.arange(-r, r + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sigma) ** 2)
    k /= k.sum()
    pad = [(0, 0), (0, 0)]
    pad[axis] = (r, r)
    ap = np.pad(a, pad, mode='edge')
    out = np.zeros_like(a, dtype=np.float64)
    n = a.shape[axis]
    for t, w in enumerate(k):
        sl = [slice(None), slice(None)]
        sl[axis] = slice(t, t + n)
        out += w * ap[tuple(sl)]
    return out


def _hg_gauss(a, sigma):
    return a.astype(np.float64) if sigma <= 0 else _hg_gauss1d(_hg_gauss1d(a.astype(np.float64), sigma, 0), sigma, 1)


def _hg_dilate(mask, r):
    r = int(round(r))
    out = mask.copy()
    for axis in (0, 1):
        pad = [(0, 0), (0, 0)]
        pad[axis] = (r, r)
        ap = np.pad(out, pad, mode='constant', constant_values=False)
        acc = out.copy()
        n = out.shape[axis]
        for t in range(2 * r + 1):
            sl = [slice(None), slice(None)]
            sl[axis] = slice(t, t + n)
            acc = np.maximum(acc, ap[tuple(sl)])
        out = acc
    return out


def lade_hg_regeln(regel_pfad):
    """hoehenstufen/glaettung/seed aus hochgebirge_regeln.json (Ordner der eigenen Regeln, sonst ../hochgebirge/), sonst Vorgabe."""
    ordner = os.path.dirname(os.path.abspath(regel_pfad))
    for p in (os.path.join(ordner, 'hochgebirge_regeln.json'), os.path.join(ordner, '..', 'hochgebirge', 'hochgebirge_regeln.json')):
        if os.path.isfile(p):
            try:
                d = json.load(open(p, encoding='utf-8'))
                if isinstance(d.get('hoehenstufen'), dict):
                    return {'hoehenstufen': d['hoehenstufen'], 'glaettung': d.get('glaettung', {}), 'seed': d.get('seed', 1),
                            'exposition': d.get('exposition', {}), 'quelle': os.path.basename(p)}
            except Exception:
                pass
    return {'hoehenstufen': HS_VORGABE, 'glaettung': {}, 'seed': 4411, 'exposition': {}, 'quelle': 'Vorgabe (wie hochgebirge_regeln.json 10.10.)'}


def hoehenstufen(hoehe, bio, wasser_m, lage_fn, win, hg):
    """Höhenstufe je Zelle (0 bergwald, 1 krummholz, 2 matte, 3 fels/schnee) und lokale Baumgrenze (m), Rechenweg wie
    hochgebirge_plan.py (Baum-/Schneegrenze je Biom, Exposition, Hang, Grat, Wertrauschen, Schlucht-Bonus, Krummholzband)."""
    HS, G = hg['hoehenstufen'], hg.get('glaettung', {})
    seed = int(hg.get('seed', 1))
    hs = _hg_gauss(hoehe, G.get('hang_sigma_m', 1.5))
    gi_, gj_ = np.gradient(hs)
    hang = np.degrees(np.arctan(np.hypot(gi_, gj_)))
    g = np.hypot(gi_, gj_) + 1e-9
    voll = float(hg.get('exposition', {}).get('hang_voll_grad', 15))
    sonnig = 0.5 + 0.5 * (-gi_ / g) * np.minimum(1.0, hang / voll)
    hk = _hg_gauss(hoehe, G.get('kruemmung_sigma_m', 8.0))
    gki, gkj = np.gradient(hk)
    lap = np.gradient(gki)[0] + np.gradient(gkj)[1]
    hg_ = _hg_gauss(hoehe, G.get('grat_sigma_m', 6.0))
    gi2, gj2 = np.gradient(hg_)
    lap_g = np.gradient(gi2)[0] + np.gradient(gj2)[1]
    bgd, sgd = HS['baumgrenze_m'], HS['schneegrenze_m']
    bg = np.full(hoehe.shape, float(bgd.get('default', 320)))
    sg = np.full(hoehe.shape, float(sgd.get('default', 470)))
    for bi, bn in enumerate(BIOME15):
        m = bio == bi
        if m.any():
            bg[m] = bgd.get(bn, bgd.get('default', 320))
            sg[m] = sgd.get(bn, sgd.get('default', 470))
    v = (sonnig - 0.5) * 2.0 * HS.get('exposition_versatz_m', 45)
    HV = HS.get('hang_versatz', {})
    t = np.clip((hang - HV.get('ab_grad', 25)) / max(1e-6, HV.get('bis_grad', 45) - HV.get('ab_grad', 25)), 0, 1)
    v = v - t * HV.get('versatz_m', 30)
    v = v - np.clip(-lap_g / max(1e-9, HS.get('grat_staerke_min', 0.015)), 0, 1) * HS.get('grat_versatz_m', 40)
    ii, jj = np.meshgrid(np.arange(win[0], win[1]), np.arange(win[2], win[3]), indexing='ij')
    v = v + (_hg_wertrauschen(ii, jj, G.get('rauschen_gitter_m', 320), seed, 11) - 0.5) * 2.0 * HS.get('rauschen_amplitude_m', 35)
    S = HS.get('schlucht', {})
    nah_w = _hg_dilate(wasser_m, S.get('wasser_m', 25))
    schlucht = _hg_dilate(nah_w & (lap > S.get('kruemmung_min', 0.006)) & (hang >= 8), 6) & nah_w
    bg = bg + v + schlucht * S.get('bonus_m', 70)
    sg = sg + v
    kb = HS.get('krummholz_band_m', [-60, 40])
    stufe = np.zeros(hoehe.shape, np.int8)
    stufe[hoehe >= bg + kb[0]] = 1
    stufe[hoehe >= bg + kb[1]] = 2
    stufe[hoehe >= sg] = 3
    stufe[lage_fn('Schnee') >= HS.get('lage_schnee_als_stufe3_ab', 0.55)] = 3
    stufe[lage_fn('Eis') >= HS.get('lage_eis_als_stufe3_ab', 0.4)] = 3
    return stufe, bg.astype(np.float32)


# ----------------------------------------------------------------------------- Planung je Feld
def plane_feld(feld, basis, regeln, faktor, bild, ov, zuordnung, ov_hinweise, inventar, hg=None):
    t0 = time.time()
    rand = int(regeln.get('fenster_rand_m', 64))
    fb, win = feld_fenster(feld, rand)
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    hinweise = list(ov_hinweise)
    ausgabe = os.path.join(basis, WELT, 'mittelschicht', feld)
    if H <= 0 or W <= 0 or fb[1] <= fb[0] or fb[3] <= fb[2]:
        leere_ausgabe(ausgabe)
        hinweise.append('Feld liegt ausserhalb des Rasters - leerer Plan')
        schreibe_plan(ausgabe, plan_kopf(feld, regeln, {}, 0, 0, 0, {}, hinweise))
        meld('%s: ausserhalb des Rasters - leerer plan.json' % feld)
        return None
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True)
    ii, jj = np.indices((H, W), dtype=np.int32)
    gi, gj = ii + wi0, jj + wj0  # globale Rasterkoordinaten (Determinismus über Feldgrenzen)
    im_feld = (gi >= fb[0]) & (gi < fb[1]) & (gj >= fb[2]) & (gj < fb[3])

    # Karten
    def r8(name):
        return lade_raster(os.path.join(basis, WELT, name), np.uint8, win)
    wasser = r8('karte_wasser.r8')
    weg = r8('karte_weg.r8')
    ort = r8('karte_ort.r8')
    for nm, a in (('karte_wasser.r8', wasser), ('karte_weg.r8', weg), ('karte_ort.r8', ort)):
        if a is None:
            hinweise.append('%s fehlt - Annahme: keine Flaeche dieser Art' % nm)
    wasser_m = (wasser > 0) if wasser is not None else np.zeros((H, W), bool)
    weg_m = (weg > 0) if weg is not None else np.zeros((H, W), bool)
    ort_m = (ort > 0) if ort is not None else np.zeros((H, W), bool)

    # Biome (KONVENTIONEN §1), Pflichtschlüssel, Leerplan bei < 2 % Land
    bio, bio_quelle = lade_biome(basis, win, regeln, feld, hinweise)
    hinweise.append('Biom je Zelle: ' + bio_quelle)
    biome_fenster = {BIOME15[k]: round(float((bio == k).mean()), 4) for k in np.unique(bio)}
    zellen_zustaendig = int((im_feld & ~wasser_m & ~weg_m & ~ort_m).sum())
    land_anteil = float((~wasser_m).mean())
    min_anteil = float(regeln.get('min_anteil_eigen_fenster', 0.02))
    if land_anteil < min_anteil or zellen_zustaendig == 0:
        leere_ausgabe(ausgabe)
        hinweise.append('Landanteil im Fenster %.1f %% < %.0f %% - leerer Plan' % (100 * land_anteil, 100 * min_anteil))
        schreibe_plan(ausgabe, plan_kopf(feld, regeln, biome_fenster, 0, 0, 0, {}, hinweise))
        meld('%s: Landanteil %.1f %% < %.0f %% - leerer plan.json (instanzen 0)' % (feld, 100 * land_anteil, 100 * min_anteil))
        return None
    eff = effektive_regeln(regeln, ov, zuordnung, feld, inventar, hinweise, set(biome_fenster))

    # Gelände: Neigung, Normale
    dzdy, dzdx = np.gradient(hoehe)  # dzdy entlang i (Y), dzdx entlang j (X), 1 m Raster
    hang = np.degrees(np.arctan(np.sqrt(dzdx ** 2 + dzdy ** 2))).astype(np.float32)
    nl = np.sqrt(dzdx ** 2 + dzdy ** 2 + 1.0)
    n_x, n_y, n_z = (-dzdx / nl).astype(np.float32), (-dzdy / nl).astype(np.float32), (1.0 / nl).astype(np.float32)
    abst = regeln['abstand_m']
    d_wasser = distanz(wasser_m, max_m=64.0)
    nah_weg_klein = dilate(weg_m, abst['weg_klein'])
    nah_weg_gross = dilate(weg_m, abst['weg_gross'])
    nah_ort = dilate(ort_m, abst['ort'])
    nah_wasser = dilate(wasser_m, abst['wasser'])

    # Lagen (nur benötigte)
    lagen_namen = set(regeln['feuchte']['lagen']) | set(regeln['licht']['fallback_lagen']) | {regeln['schnee']['lage']}
    for b in eff.values():
        for k in b.values():
            lagen_namen |= set(k.get('lagen_faktor', {}).keys())
            if isinstance(k.get('lagen_min'), dict):
                lagen_namen |= set(k['lagen_min'].keys())
    lagen = {}
    for ln in sorted(lagen_namen):
        if ln.startswith('ufer_'):
            continue
        a = r8('lage_%s.r8' % ln)
        if a is not None:
            lagen[ln] = a.astype(np.float32) / 255.0
    if not lagen:
        hinweise.append('keine lage_*.r8 gefunden - Feuchte nur aus Wassernaehe, Kronendach nur aus Baum-Ebenen')

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
        hinweise.append('Kronendach aus %d Baeumen (%s)' % (len(baeume), ', '.join(quellen[:8]) + (' ...' if len(quellen) > 8 else '')))
    else:
        beschattung = np.zeros((H, W), np.float32)
        for ln, w in L['fallback_lagen'].items():
            if ln in lagen:
                beschattung += w * lagen[ln]
        beschattung = np.clip(gauss_blur(beschattung, 8.0), 0, L['fallback_beschattung_max']).astype(np.float32)
        baum_m = np.zeros((H, W), bool)
        hinweise.append('keine Baum-Ebene gefunden (bestand/, witcher/, Biom-Planer-Ebenen, instanzen/) - Beschattung aus Lagen Laub/Nadeln/Moos geschaetzt, max %.2f' % L['fallback_beschattung_max'])
    nah_baum = dilate(baum_m, abst['baumstamm']) if baum_m.any() else np.zeros((H, W), bool)
    ring_baum = (dilate(baum_m, 1.6) & ~nah_baum) if baum_m.any() else np.zeros((H, W), bool)
    nah_baum_3 = dilate(baum_m, 3.0) if baum_m.any() else np.zeros((H, W), bool)
    belegt = np.zeros((H, W), bool)
    if len(sonst):
        si = np.clip(np.round(sonst[:, 0]).astype(np.int32), 0, H - 1)
        sj = np.clip(np.round(sonst[:, 1]).astype(np.int32), 0, W - 1)
        belegt[si, sj] = True
        belegt = dilate(belegt, abst['bestand_sonst'])
        hinweise.append('%d vorhandene Nicht-Baum-Instanzen (Witcher/Bestand/Biom-Planer/Felsgruppen, ohne Boden) als belegt (%.1f m)' % (len(sonst), abst['bestand_sonst']))

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
    ufer_band = (d_wasser <= F['ufer_schilf_m']) & ~nah_wasser
    Hh = regeln['hoehe']
    f_hoehe = np.clip((Hh['null_ab_m'] - hoehe) / max(1.0, Hh['null_ab_m'] - Hh['abnahme_ab_m']), 0, 1).astype(np.float32)
    S = regeln['schnee']
    f_schnee = (1 - (1 - S['faktor_bei_voll']) * lagen[S['lage']]) if S['lage'] in lagen else np.ones((H, W), np.float32)
    voll_bis = regeln['hang']['voll_bis_grad']
    feld_faktor = faktor * (regeln['wuesten_feld_faktor'] if feld in regeln['wuesten_felder'] else 1.0)
    sperre = wasser_m | weg_m | ort_m | nah_wasser | belegt | nah_ort
    ring_3 = (nah_baum_3 & ~nah_baum) if baum_m.any() else np.zeros((H, W), bool)
    mod_cache = {}

    def modulator(name):
        """Zusatzmasken für Override-Parameter lichtung, wegrand, nah_baum, mulde (nur bei Bedarf berechnet)."""
        if name not in mod_cache:
            if name == 'lichtung':
                mod_cache[name] = lichtung
            elif name == 'wegrand':
                mod_cache[name] = (distanz(weg_m, max_m=16.0) <= float(abst.get('wegrand_band_m', 8.0))) & ~weg_m
            elif name == 'nah_baum':
                mod_cache[name] = ring_3
            elif name in ('stufe', 'baumgrenze'):
                def lage_fn(ln):
                    if ln in lagen:
                        return lagen[ln]
                    a_ = r8('lage_%s.r8' % ln)
                    return a_.astype(np.float32) / 255.0 if a_ is not None else np.zeros((H, W), np.float32)
                hgr = hg or lade_hg_regeln(os.path.join(SKRIPT_DIR, 'mittelschicht_regeln.json'))
                st_, bg_ = hoehenstufen(hoehe, bio, wasser_m, lage_fn, win, hgr)
                st_[wasser_m] = -1
                mod_cache['stufe'], mod_cache['baumgrenze'] = st_, bg_
                anteile = {n_: round(float((st_[im_feld] == k_).mean()), 3) for k_, n_ in enumerate(('bergwald', 'krummholz', 'matte', 'fels_schnee'))}
                hinweise.append('Hoehenstufen (%s) im Feld: %s' % (hgr.get('quelle'), anteile))
            elif name == 'mulde_wert':
                mod_cache[name] = (gauss_blur(hoehe, 10.0) - hoehe).astype(np.float32)
            elif name == 'mulde':
                mod_cache[name] = modulator('mulde_wert') > float(regeln.get('mulde_tiefe_m', 0.4))
        return mod_cache[name]

    # ------------------------------------------------------------------ Streuung je Biom und Klasse
    seed = int(regeln['seed'])
    gross = set(regeln['gross_klassen'])
    farben = regeln.get('bild_farben', {})
    aus = []
    netze_je_klasse = {}
    for bname in BIOME15:
        for kname, kl in eff[bname].items():
            netze_je_klasse.setdefault(kname, [])
            for p in kl['netze']:
                if p not in netze_je_klasse[kname]:
                    netze_je_klasse[kname].append(p)
    quellen_klasse = {}
    saum_m = float(regeln.get('zusatz_saum_m', 30.0))
    meldungen = set()
    for bidx, bname in enumerate(BIOME15):
        in_biom = bio == bidx
        if not in_biom.any():
            continue
        saum_cache = {}
        for kname, kl in sorted(eff[bname].items(), key=lambda e: (1 if e[1].get('an_totholz') else 0, e[0])):
            fk = float(kl.get('faktor', 1.0))
            if fk <= 0 or not kl.get('netze'):
                continue
            kanal = klassen_kanal(bidx, kname)
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
            stufen_klasse = any(k_ in kl for k_ in ('stufe', 'stufen', 'hoehe_rel_baumgrenze_m'))
            lam *= (1.0 if stufen_klasse else f_hoehe) * f_schnee * (feld_faktor * fk)  # mit Stufenangabe kein pauschaler Abfall ab 350 m
            if kl['hoehe_max_m'] < 9000:
                lam = np.where(hoehe > kl['hoehe_max_m'], 0, lam)
            if isinstance(kl.get('hoehe_min_m'), (int, float)):
                lam = np.where(hoehe < float(kl['hoehe_min_m']), 0, lam)
            if stufen_klasse:  # relative Höhen: Höhenstufe bzw. Abstand zur lokalen Baumgrenze (wie hochgebirge_plan.py)
                st_ = modulator('stufe')
                stv = kl.get('stufe')
                if isinstance(stv, (int, float)):
                    stv = [stv, stv]
                if isinstance(stv, list) and len(stv) == 2:
                    lam = np.where((st_ >= stv[0]) & (st_ <= stv[1]), lam, 0)
                if isinstance(kl.get('stufen'), list) and len(kl['stufen']) == 4:
                    lam = lam * np.asarray(kl['stufen'], np.float32)[np.clip(st_, 0, 3)] * (st_ >= 0)
                rb = kl.get('hoehe_rel_baumgrenze_m')
                if isinstance(rb, list) and len(rb) == 2:
                    rel = hoehe - modulator('baumgrenze')
                    lam = np.where((rel >= rb[0]) & (rel <= rb[1]), lam, 0)
            for ln, w in kl.get('lagen_faktor', {}).items():
                if ln.startswith('ufer_'):
                    lam = np.where(ufer_band, lam + w * fk, lam)
                elif ln in lagen:
                    lam *= 1 + (w - 1) * lagen[ln]
            for mod in ('lichtung', 'wegrand', 'nah_baum', 'mulde'):
                if isinstance(kl.get(mod), (int, float)) and float(kl[mod]) != 1.0:
                    lam = np.where(modulator(mod), lam * float(kl[mod]), lam)
            if isinstance(kl.get('an_totholz'), (int, float)) and float(kl['an_totholz']) != 1.0:
                tm = np.zeros((H, W), bool)
                for a0 in aus:
                    if a0['klasse'] in ('totholz_liegend', 'totholz_stumpf') and a0['mi'].size:
                        tm[a0['mi'], a0['mj']] = True
                if tm.any():
                    lam = np.where(dilate(tm, 2.0), lam * float(kl['an_totholz']), lam)
            # Bedingungen aus dem Zusatzklassen-Schema (KONVENTIONEN §6)
            if isinstance(kl.get('hang_bereich'), list):
                lam = np.where((hang >= kl['hang_bereich'][0]) & (hang <= kl['hang_bereich'][1]), lam, 0)
            if isinstance(kl.get('hoehe_bereich'), list):
                lam = np.where((hoehe >= kl['hoehe_bereich'][0]) & (hoehe <= kl['hoehe_bereich'][1]), lam, 0)
            wa = kl.get('wasser_abstand_m')
            if isinstance(wa, list) and len(wa) == 2:
                lam = np.where((d_wasser >= float(wa[0])) & (d_wasser <= float(wa[1])), lam, 0)
            for ln, wmin in (kl.get('lagen_min') or {}).items():
                if ln in lagen:
                    lam = np.where(lagen[ln] * 255.0 >= float(wmin), lam, 0)
                else:
                    lam = lam * 0
                    if (kname, ln) not in meldungen:
                        meldungen.add((kname, ln))
                        hinweise.append('%s/%s: lage_%s.r8 fehlt - lagen_min nicht erfuellbar, Klasse entfaellt' % (bname, kname, ln))
            kr = str(kl.get('kruemmung', 'egal')).lower()
            if kr in ('konvex', 'konkav'):
                mul = modulator('mulde_wert')
                lam = np.where(mul > 0.2 if kr == 'konkav' else mul < -0.2, lam, 0)
            if kl.get('ist_zusatz'):  # Zusatzklassen eines Biom-Planers: Biom + weicher Saum (linear auf 0)
                if 'd' not in saum_cache:
                    saum_cache['d'] = distanz(in_biom, max_m=max(2.0, saum_m + 2.0))
                d_b = saum_cache['d']
                gebiet = d_b <= saum_m
                lam = lam * np.clip(1.0 - d_b / max(1e-3, saum_m), 0, 1)
            else:
                gebiet = in_biom
            frei = gebiet & ~sperre
            frei &= ~(nah_weg_gross if (kname in gross or kl.get('kollision')) else nah_weg_klein)
            if kl.get('an_baum'):
                if not baum_m.any():
                    continue
                frei &= ring_baum
            elif kname == 'totbaum':
                frei &= ~nah_baum_3
            else:
                frei &= ~nah_baum
            lam = np.where(frei, lam, 0).astype(np.float32)
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
            gw = kl.get('netze_gewicht') or {}
            if gw:  # gewichtete Netzwahl (z. B. Dschungel: Busch 4 : je Holunder 1)
                cw = np.cumsum([max(0.0, float(gw.get(p, 1.0))) for p in netzl])
                nidx = np.minimum(np.searchsorted(cw / cw[-1], hv, side='right'), len(netzl) - 1).astype(np.int32)
            else:
                nidx = np.minimum((hv * len(netzl)).astype(np.int32), len(netzl) - 1)
            nglob = np.array([netze_je_klasse[kname].index(p) for p in netzl], np.int32)[nidx]
            u_ms = hash01(gmi, gmj, seed, kanal + 7)
            ms_lo = np.full(fi.size, kl['massstab'][0], np.float32)
            ms_hi = np.full(fi.size, kl['massstab'][1], np.float32)
            for p, (lo, hi) in (kl.get('netze_massstab') or {}).items():  # Maßstab je Netz (z. B. Holunder als Bananen-Ersatz)
                if p in netzl:
                    m = nidx == netzl.index(p)
                    ms_lo[m], ms_hi[m] = lo, hi
            ms = ms_lo + (ms_hi - ms_lo) * u_ms
            yaw = hash01(gmi, gmj, seed, kanal + 8) * 2 * math.pi
            if kl.get('laengs_hang'):
                asp = np.arctan2(-dzdy[mi, mj], -dzdx[mi, mj])  # Richtung hangabwärts (X,Y)
                yaw = asp + (hash01(gmi, gmj, seed, kanal + 9) - 0.5) * math.radians(40) + np.where(hash01(gmi, gmj, seed, kanal + 8) < 0.5, 0, math.pi)
            aus.append(dict(fi=fi.astype(np.float32), fj=fj.astype(np.float32), mi=mi, mj=mj, klasse=kname, netz=nglob, kanal=kanal % 1000003,
                            massstab=ms.astype(np.float32), yaw=yaw.astype(np.float32), kippen=kl['kippen'],
                            eingraben=kl['eingraben_cm'], kollision=bool(kl['kollision']), sichtweite=kl['sichtweite'], biom=bname,
                            schatten=kl.get('schatten'), farbe=kl.get('farbe'), akteur=bool(kl.get('akteur'))))
            quellen_klasse.setdefault(bname, {})[kname] = kl.get('quelle', 'mittelschicht') + ('' if fk == 1.0 else ' x%.2f' % fk)

    # ------------------------------------------------------------------ Budget
    roh, protokoll = budget_anwenden(aus, regeln, seed, wi0, wj0, hinweise)

    # ------------------------------------------------------------------ Instanzen bauen und schreiben
    leere_ausgabe(ausgabe)
    dateien, netz_inst, stat, stat_biom = {}, {}, {}, {}
    nk = 0
    koll_netz = {}
    for a in aus:  # Netz mit und ohne Kollision genutzt → eigene Datei <Netz>_ohne_koll (eigener Foliage-Typ)
        if a['fi'].size:
            for ni in np.unique(a['netz']):
                nm = netze_je_klasse[a['klasse']][ni].rsplit('/', 1)[-1]
                koll_netz.setdefault(nm, set()).add(bool(a['kollision']))
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
            if len(koll_netz.get(name, ())) == 2 and not a['kollision']:
                name += '_ohne_koll'
            if a['akteur']:
                name = 'akteur_' + name  # Konvention felsgruppen/spuren: als StaticMeshActor setzen
            netz_inst.setdefault(name, []).append(inst[m])
            if name not in dateien:
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': a['klasse'], 'rolle': 'akteur' if a['akteur'] else 'mittelschicht', 'ebene': EBENE,
                                 'sichtweite': list(a['sichtweite']),
                                 'schatten': bool(a['schatten']) if isinstance(a['schatten'], bool) else a['klasse'] not in ('pilz', 'totholz_ast', 'grasbueschel', 'beere'),
                                 'kollision': bool(a['kollision'])}
            elif a['klasse'] not in dateien[name]['gruppe'].split('+'):
                dateien[name]['gruppe'] = '+'.join(sorted(dateien[name]['gruppe'].split('+') + [a['klasse']]))
            dateien[name]['anzahl'] += int(m.sum())
        stat[a['klasse']] = stat.get(a['klasse'], 0) + n
        stat_biom[a['biom']] = stat_biom.get(a['biom'], 0) + n
    gesamt = 0
    for name in sorted(netz_inst):
        arr = np.concatenate(netz_inst[name], axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]
        if dateien[name]['kollision']:
            nk += arr.shape[0]
    if nk > int(regeln['budget']['kollision_je_feld']) or gesamt > int(regeln['budget']['instanzen_je_feld']):
        hinweise.append('WARNUNG: geschrieben %d Instanzen / %d mit Kollision ueber Deckel (Kollision je Netz als Vereinigung)' % (gesamt, nk))
    entf = [x.strip() for x in str(regeln.get('entfernen', '')).split(',') if x.strip()] + override_entfernen(ov, feld)
    if override_entfernen(ov, feld):
        hinweise.append('entfernen aus Overrides (entfernen_je_feld): %s' % ', '.join(override_entfernen(ov, feld)))
    plan = plan_kopf(feld, regeln, biome_fenster, zellen_zustaendig, gesamt, nk, dateien, hinweise, ','.join(dict.fromkeys(entf)))
    plan['statistik'] = {'je_klasse': stat, 'je_biom': stat_biom, 'vor_budget': int(roh), 'ausduennung': protokoll,
                         'paletten_quelle': quellen_klasse, 'wald_anteil': round(float(wald[im_feld].mean()), 3),
                         'beschattung_mittel': round(float(beschattung[im_feld].mean()), 3), 'faktor': faktor,
                         'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA}
    plan['overrides'] = {thema: {'datei': os.path.basename(ov[thema][1]),
                                 'biome': sorted(b for b, t in zuordnung.items() if t == thema),
                                 'schluessel': sorted(k for k in ov[thema][0] if not doku_schluessel(k)),
                                 'zusatzklassen': sorted({k for b in BIOME15 if zuordnung.get(b) == thema for k, v in eff[b].items() if v.get('ist_zusatz')}),
                                 'unbekannte_schluessel': unbekannte_schluessel(ov[thema][0])} for thema in sorted(ov)}
    plan['ungetestet'] = 'Korrektur Runde 1: in der Cloud nur mit synthetischen Daten rauchgetestet'
    schreibe_plan(ausgabe, plan)
    meld('%s: %d Instanzen (%d mit Kollision), %d Netze, Biome %s, %.1f s' % (feld, gesamt, nk, len(dateien),
         ', '.join('%s %.0f%%' % (k, 100 * v) for k, v in sorted(biome_fenster.items(), key=lambda e: -e[1]) if v >= 0.01), time.time() - t0))
    for h in hinweise[len(ov_hinweise):]:  # Override-Hinweise stehen schon im Kopf des Logs
        meld('  Hinweis:', h)

    if bild:
        try:
            from PIL import Image
        except Exception:
            meld('Pillow fehlt - kein Pruefbild')
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
            c = a['farbe'] if isinstance(a.get('farbe'), list) and len(a['farbe']) == 3 else farben.get(a['klasse'], [255, 255, 255])
            pi = np.clip(np.round(a['fi']).astype(np.int32) - fi0, 0, fi1 - fi0 - 1)
            pj = np.clip(np.round(a['fj']).astype(np.int32) - fj0, 0, fj1 - fj0 - 1)
            rgb[pi, pj] = c
            if a['klasse'] in gross:
                rgb[np.minimum(pi + 1, fi1 - fi0 - 1), pj] = c
        os.makedirs(os.path.join(basis, 'docs', 'pruefung', 'mittelschicht'), exist_ok=True)
        Image.fromarray(rgb.astype(np.uint8)).save(os.path.join(basis, 'docs', 'pruefung', 'mittelschicht', feld + '.png'))
    return plan


def pruefe_netze(regeln, inventar, csv):
    """Alle /Game/-Pfade der eigenen Regeldatei gegen das Inventar prüfen. Fehlendes Inventar → Hinweis, keine Prüfung.
    Unbekannte Pfade → Abbruch mit Liste und Exit-Code 2 (FORMAT.md §5)."""
    pfade = set()

    def sammle(o):
        if isinstance(o, str):
            if o.startswith('/Game/'):
                pfade.add(o)
        elif isinstance(o, dict):
            for k, v in o.items():
                sammle(k)
                sammle(v)
        elif isinstance(o, list):
            for v in o:
                sammle(v)
    sammle(regeln)
    pfade.discard(regeln.get('ft_ordner', ''))
    if inventar is None:
        meld('Hinweis: daten/netze.csv nicht gefunden - %d Netzpfade der Regeln bleiben ungeprueft' % len(pfade))
        return
    fehlt = sorted(p for p in pfade if p not in inventar)
    if fehlt:
        for p in fehlt:
            meld('   fehlt:', p)
        abbruch('%d Netzpfade der Mittelschicht-Regeln fehlen im Inventar %s - Einkaufsliste/Regeln abgleichen' % (len(fehlt), csv))
    meld('%d Netzpfade gegen %s geprueft: alle vorhanden' % (len(pfade), csv))


def main():
    ap = argparse.ArgumentParser(description='Eldarien Mittelschicht-Planer (0,3-3 m, alle Biome)')
    ap.add_argument('felder', nargs='+')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    a = ap.parse_args()
    rp = a.regeln or os.path.join(SKRIPT_DIR, 'mittelschicht_regeln.json')
    if not os.path.isfile(rp):
        abbruch('Regeldatei fehlt: %s' % rp)
    try:
        regeln = json.load(open(rp, encoding='utf-8'))
    except Exception as e:
        abbruch('Regeldatei unlesbar: %s (%s)' % (rp, e))
    inventar, csv = lade_inventar(a.basis)
    pruefe_netze(regeln, inventar, csv)
    ov, zuordnung, ov_hinweise = lade_overrides(regeln, rp)
    for h in ov_hinweise:
        meld(h)
    if not NUMBA:
        meld('numba nicht verfuegbar - reiner NumPy-Pfad (ausreichend)')
    for feld in a.felder:
        plane_feld(feld.strip().upper(), a.basis, regeln, a.faktor, a.bild, ov, zuordnung, ov_hinweise, inventar, lade_hg_regeln(rp))


if __name__ == '__main__':
    main()
