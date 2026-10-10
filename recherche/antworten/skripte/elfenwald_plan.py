#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien - Planer "Elfenwald" (Auftrag 11, Teil B5, Biom elfenwald): alter Laubwald mit Lichtungen nach Witcher-Messlatte.
Stand Korrektur Runde 1 (10.10.2026, verbindlich: antworten/verteilung-KONVENTIONEN.md).
Korrektur Runde 4 (Konventionen par. 1b): karte_wasser.r8 ist nur Suesswasser. Meer = hoehe < 0 UND karte_wasser == 0;
wasser_alle = Suesswasser | Meer fuer Sperren (abstand_m.wasser), Waldgebiet, Ring-an-Baum, Kuppe und Feuchte (Wassernaehe).
Bachsaum (Schicht 5), Bach/Fluss-Erkennung, bach_dichte und Schrein an der Bachquerung bleiben bei karte_wasser. Kuestensaum
(< +0,3 m, <= 30 m zum Meer): nur Schicht/Rolle wasserkante, strand:true, meer_rolle:true; im Meer nur meer_rolle -0,3...0 m.
Schlussfilter am Instanzort (bilineare Gelaendehoehe) in merke(); plan.json meldet meer_zellen und meer_gefiltert.
Landzellen-Bezug (Konventionen par. 1): biome_fenster, Eigenanteil (2-%-Schwelle) und 30-m-Saum nur ueber Landzellen ohne
wasser_alle; plan.json["biome_fenster_bezug"] = "land".

Zustaendigkeit (Konventionen par. 1): Biom je Zelle aus eigner.r8 + welt.json (rezept; Kennzahl 0 = Weltgelaende -> aue,
Vulkanregion -> lava; nur wenn eigner.r8/welt.json fehlen: dominantes Feldbiom aus daten/biome_je_feld.json). biome_eigen =
[elfenwald]. Bebaut werden nur elfenwald-Zellen plus 30-m-Saum (Dichte linear 1 -> 0, Distanzfeld). Eigenanteil im Fenster
< 2 % -> leerer plan.json (instanzen 0, keine f32).

Schichten einer Ebene (FT_EL_EW_*):
  2_baum        Modus ergaenzen (Bestand-Ebene vorhanden): Hero-Altbaeume am Lichtungsrand + stehendes Totholz; Modus voll:
                Altersmix (hero/alt/mittel/jung/tot) + Pappel/Birke/Weide, Gruppen 8-40 m, Lichtungen 15-25 %.
  1_mittel      NUR Elfenwald-Sonderformen: Wurzelanlauf- und Efeu-Ring am Stamm alter Baeume, Moos-Stamm (Baumleiche) neben
                stehendem Totholz/Altbaeumen, Lichtungsblumen-Inseln. Die generischen Klassen (strauch, jungbaum, farn,
                totholz_liegend/stumpf/ast, hochstaude, grasbueschel, beere, pilz) setzt ausschliesslich mittelschicht_plan.py
                (Teil D) mit den mittelschicht_overrides aus elfenwald_regeln.json (Palette, Faktor, Zusatzklassen, Farninseln).
  0_boden       Laubhaufen, Zweige, Moospolster, Sauerklee, Kleinsteine (Dichten seit Runde 1 -30 bis -38 %; Flaechenstreu
                kommt vom Landschafts-Gras GT_Kraut/GT_Steinchen).
  5_wasserkante Bachsaum 0,5-6 m: Moossteine, Farne, Schachtelhalm, Binsen, Moos, Boeschungsstuecke (Fluss/See gedaempft).
Schicht 3 (Fels > 0,8 m) und 4 (Spuren) kommen von felsgruppen_plan.py / spuren_plan.py (felsgruppen_overrides, spuren_overrides).
Budget (par. 3, hart): <= 60 000 Instanzen je Feld, Ziel 45 000-52 000, <= 3 000 mit Kollision (auch Baeume).

Aufruf (lokal, production-Wurzel):
    python -I -X utf8 scripts/elfenwald/elfenwald_plan.py FELD [FELD ...] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
                                                  [--schichten 0,1,2,5] [--baum auto|voll|ergaenzen] [--mittel zusatz|voll]
                                                  [--inventar PFAD]
    --mittel: nur noch Kompatibilitaet. zusatz (Standard) ist der einzige Modus; voll verhaelt sich wie zusatz (Hinweis im Log).

Liest:   export/unreal/welt/hoehe.f32 (Pflicht; np.memmap, Fenster Feld + 64 m), lage_*.r8, karte_wasser/weg/ort.r8,
         eigner.r8 + welt.json, bestand/<Feld>/ und witcher/<Feld>/ (+ Nachbarfelder; Baeume -> Kronendach),
         instanzen/instanzen.json (optional), daten/netze.csv (Pflicht, Inventar-Pruefung), daten/biome_je_feld.json (Fallback).
Schreibt: export/unreal/welt/elfenwald/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm, qx,qy,qz,qw, sx,sy,sz) + plan.json
         (FORMAT.md par. 3 + Pflichtschluessel biome_fenster, zellen_zustaendig, biome_eigen, kollision_anzahl), bei --bild
         docs/pruefung/elfenwald/<Feld>.png (1 px = 1 m). Fehlende Pflichtdatei -> Meldung, Exit-Code 2. Logs nur ASCII.

Nur NumPy-Vektoroperationen (Box-/Gauss-Faltung, Jump-Flooding-Distanzfeld, Hash-Zufall aus der globalen Rasterkoordinate ->
deterministisch und nahtlos). numba optional. Laufzeit-Ziel <= 60 s je Feld.

Quellen: FORMAT.md par. 1-5; verteilung-KONVENTIONEN.md; verteilung-korrektur-runde1.md; antworten/assets-taxonomie.md;
antworten/bildkritik-witcher-messlatte.md; antworten/boden-kleinzeug-gras.md; 80.lv "World Building of Witcher 3";
Nagel et al. 2013 PLOS ONE (Totholz in Buchen-Urwaeldern); Runkle-Typ Lueckenanteile 3-18 %.

UNGETESTET MIT ECHTDATEN - in der Cloud nur mit synthetischen Rastern rauchgetestet (verteilung-elfenwald.md, Korrektur Runde 1).
"""
import argparse
import csv
import json
import math
import os
import sys
import time
import zlib

import numpy as np

try:  # numba optional – nicht benötigt
    import numba  # noqa: F401
    NUMBA = True
except Exception:  # pragma: no cover
    NUMBA = False

NX, NY = 9577, 7057
FELD_M = 1008
X0, Y0 = 4730.5, 4060.5  # X_cm = (j - 4730.5)*100, Y_cm = (i - 4060.5)*100
WELT = os.path.join('export', 'unreal', 'welt')
THEMA = 'elfenwald'
BAUM_ROLLEN = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel', 'palme',
               'hainbuche', 'hornbeam', 'beech', 'poplar', 'pine', 'fir', 'birch', 'willow')
NICHT_BAUM = ('tot', 'dead', 'stump', 'log', 'fallen', 'plant', 'sapling', 'seedling', 'bush', 'branch', 'root', 'mossytree',
              'stamm', 'strauch', 'farn', 'fern', 'leaves', 'laub')
BAUM_REIHENFOLGE = ('hero', 'alt', 'tot', 'mittel', 'pappel', 'birke', 'weide', 'jung')
ROLLE_JE_SCHICHT = {'0_boden': 'boden', '1_mittel': 'mittelschicht', '2_baum': 'baum', '5_wasserkante': 'wasserkante'}


# ----------------------------------------------------------------------------- Helfer
_ASCII = (('\u00e4', 'ae'), ('\u00f6', 'oe'), ('\u00fc', 'ue'), ('\u00c4', 'Ae'), ('\u00d6', 'Oe'), ('\u00dc', 'Ue'),
          ('\u00df', 'ss'), ('\u2192', '->'), ('\u2190', '<-'), ('\u2264', '<='), ('\u2265', '>='), ('\u2026', '...'),
          ('\u00d7', 'x'), ('\u2013', '-'), ('\u2014', '-'), ('\u00b0', ' Grad'), ('\u00b2', '2'), ('\u00b3', '3'),
          ('\u201e', '"'), ('\u201c', '"'), ('\u201d', '"'), ('\u201a', "'"), ('\u2018', "'"), ('\u2019', "'"),
          ('\u00b7', '*'), ('\u00b1', '+-'), ('\u2248', '~'), ('\u00a0', ' '))


def ascii_text(s):
    """Text fuer Logs (cp1252-Weiterverarbeitung): Umlaute -> ae/oe/ue/ss, Sonderzeichen -> ASCII, Rest -> '?'."""
    s = str(s)
    for a, b in _ASCII:
        s = s.replace(a, b)
    return s.encode('ascii', 'replace').decode('ascii')


def meld(*a):
    print(ascii_text(' '.join(['[elfenwald]'] + [str(x) for x in a])), flush=True)


def fehler(text):
    """Klare Meldung (ASCII) und Exit-Code 2 (fehlende Pflichtdatei, falscher Aufruf)."""
    sys.stderr.write(ascii_text('[elfenwald] FEHLER: %s' % text) + '\n')
    sys.stderr.flush()
    sys.exit(2)


def kanal_von(name):
    """Deterministischer Kanal aus einem Klassennamen (Pythons eingebautes hash ist je Prozess zufällig)."""
    return zlib.crc32(name.encode('utf-8')) & 0xFFFFFFFF


def feld_fenster(feld, rand):
    """Feld 'G4' → (Feldgrenzen i0,i1,j0,j1), (Fenster wi0,wi1,wj0,wj1), geklippt auf NY×NX (J-Spalte endet bei NX=9577)."""
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        fehler('Unbekanntes Feld %r (A1 ... J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        fehler('Unbekanntes Feld %r (A1 ... J7)' % feld)
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX)
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY)
    wi0, wi1 = max(0, i0 - rand), min(NY, i1 + rand)
    wj0, wj1 = max(0, j0 - rand), min(NX, j1 + rand)
    return (i0, i1, j0, j1), (wi0, wi1, wj0, wj1)


def lade_raster(pfad, dtype, win, pflicht=False):
    """Fensterausschnitt eines NY×NX-Rasters per memmap; nur das Fenster wird gelesen."""
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            fehler('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        if pflicht:
            fehler('Pflichtdatei %s hat %d Werte, erwartet %d' % (pfad, n, NX * NY))
        meld('WARNUNG: %s hat %d Werte, erwartet %d - Datei wird ignoriert' % (pfad, n, NX * NY))
        return None
    mm = np.memmap(pfad, dtype=dtype, mode='r', shape=(NY, NX))
    a = np.array(mm[wi0:wi1, wj0:wj1])
    del mm
    return a


def box_blur(a, r):
    """Box-Filter Radius r (Zellen) über Summenbild, Rand gespiegelt."""
    if r <= 0:
        return a.astype(np.float32)
    p = np.pad(a.astype(np.float32), r, mode='reflect')
    c = np.cumsum(p, axis=0, dtype=np.float64)
    c = np.concatenate([np.zeros((1, c.shape[1])), c], axis=0)
    p = ((c[2 * r + 1:, :] - c[:-2 * r - 1, :]) / (2 * r + 1))
    c = np.cumsum(p, axis=1, dtype=np.float64)
    c = np.concatenate([np.zeros((c.shape[0], 1)), c], axis=1)
    return ((c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)).astype(np.float32)


def gauss_blur(a, sigma):
    """3 Box-Durchläufe ≈ Gauß (sigma in Zellen)."""
    if sigma <= 0.5:
        return a.astype(np.float32)
    w = math.sqrt(12.0 * sigma * sigma / 3.0 + 1.0)
    r = max(1, int(round((w - 1) / 2)))
    out = a
    for _ in range(3):
        out = box_blur(out, r)
    return out


def verschiebe(a, di, dj, fill):
    """out[i, j] = a[i + di, j + dj], außerhalb fill."""
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
    """Binäre Dilatation ≈ Kreisscheibe (Radius r Zellen; Wechsel 4er/8er-Nachbarschaft → Oktagon)."""
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
    """Maximum in Oktagon-Umgebung Radius r (für Kuppen/Bachbreite)."""
    m = a.copy()
    for k in range(int(math.ceil(r))):
        n = m.copy()
        np.maximum(n[1:, :], m[:-1, :], out=n[1:, :])
        np.maximum(n[:-1, :], m[1:, :], out=n[:-1, :])
        np.maximum(n[:, 1:], m[:, :-1], out=n[:, 1:])
        np.maximum(n[:, :-1], m[:, 1:], out=n[:, :-1])
        if k % 2 == 1:
            np.maximum(n[1:, 1:], m[:-1, :-1], out=n[1:, 1:])
            np.maximum(n[:-1, :-1], m[1:, 1:], out=n[:-1, :-1])
        m = n
    return m


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
    """Deterministische Zufallszahl [0,1) je (globale Zeile, globale Spalte, Seed, Kanal)."""
    i = np.asarray(i).astype(np.int64)
    j = np.asarray(j).astype(np.int64)
    h = (i * 73856093) ^ (j * 19349663) ^ np.int64(int(seed) * 83492791 + int(kanal) * 2654435761)
    h = (h & 0xFFFFFFFF).astype(np.uint32)
    with np.errstate(over='ignore'):
        h ^= h >> np.uint32(16)
        h *= np.uint32(0x7FEB352D)
        h ^= h >> np.uint32(15)
        h *= np.uint32(0x846CA68B)
        h ^= h >> np.uint32(16)
    return (h & np.uint32(0xFFFFFF)).astype(np.float32) / np.float32(16777216.0)


def wertrausch(gi, gj, seed, wellenlaenge, kanal):
    """Wertrauschen 0..1 (bilinear mit Smoothstep) aus Hash der Gitterpunkte im Abstand wellenlaenge (m), nahtlos."""
    fi = gi.astype(np.float32) / np.float32(wellenlaenge)
    fj = gj.astype(np.float32) / np.float32(wellenlaenge)
    i0 = np.floor(fi).astype(np.int64)
    j0 = np.floor(fj).astype(np.int64)
    ti = fi - i0
    tj = fj - j0
    ti = ti * ti * (3 - 2 * ti)
    tj = tj * tj * (3 - 2 * tj)
    v00 = hash01(i0, j0, seed, kanal)
    v10 = hash01(i0 + 1, j0, seed, kanal)
    v01 = hash01(i0, j0 + 1, seed, kanal)
    v11 = hash01(i0 + 1, j0 + 1, seed, kanal)
    return ((v00 * (1 - ti) + v10 * ti) * (1 - tj) + (v01 * (1 - ti) + v11 * ti) * tj).astype(np.float32)


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


MEER_STANDARD = {'nichts_unter_m': -0.3, 'kueste_bis_m': 0.3, 'kuesten_saum_m': 30, 'kueste_rollen': ['wasserkante', 'strand']}


def meer_regel(regeln):
    M = dict(MEER_STANDARD)
    M.update({k: v for k, v in (regeln.get('meer') or {}).items() if k in MEER_STANDARD})
    return M


def meer_behalten(g, ci, cj, meer, suess, kueste_nah, rolle, kl, M):
    """Konventionen par. 1b am Instanzort (g = bilineare Gelaendehoehe, Zelle ci/cj): im Meer (keine Suesswasserzelle und Meerzelle
    oder g < 0) nur meer_rolle zwischen nichts_unter_m und 0; im Kuestensaum (<= kuesten_saum_m zum Meer, g < kueste_bis_m) nur
    kueste_rollen, strand:true oder meer_rolle:true. Rueckgabe: Behalten-Maske."""
    s = suess[ci, cj]
    im_meer = ~s & (meer[ci, cj] | (g < 0.0))
    keep = ~im_meer
    if kl.get('meer_rolle'):
        keep |= im_meer & (g >= float(M['nichts_unter_m']))
    if not (kl.get('meer_rolle') or kl.get('strand') or rolle in M['kueste_rollen']):
        keep &= ~(~im_meer & ~s & kueste_nah[ci, cj] & (g < float(M['kueste_bis_m'])))
    return keep


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
    qt = np.stack([-ty, tx, np.zeros(n, np.float32), 1 + tz], axis=1)
    qt /= (np.linalg.norm(qt, axis=1, keepdims=True) + 1e-9)
    qy = np.stack([np.zeros(n, np.float32), np.zeros(n, np.float32), np.sin(yaw / 2), np.cos(yaw / 2)], axis=1)
    q = quat_mul(qt, qy)
    return (q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-9)).astype(np.float32)


# ----------------------------------------------------------------------------- Inventar / Regeln
def alle_pfade(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from alle_pfade(v)
    elif isinstance(o, list):
        for v in o:
            yield from alle_pfade(v)
    elif isinstance(o, str) and o.startswith('/Game/') and not o.endswith('/'):
        yield o


def pruefe_inventar(regeln, basis, inventar_pfad):
    """Netzpfade der Paletten gegen daten/netze.csv prüfen; fehlende Netze aus den Paletten streichen (Meldung)."""
    kandidaten = [inventar_pfad] if inventar_pfad else []
    for k in regeln.get('inventar_kandidaten', []):
        kandidaten.append(os.path.join(basis, k))
    skript = os.path.dirname(os.path.abspath(__file__))
    kandidaten += [os.path.join(skript, 'netze.csv'), os.path.join(skript, '..', '..', 'daten', 'netze.csv'),
                   os.path.join(skript, '..', '..', 'vorlagen', 'daten', 'netze.csv')]
    pfad = next((k for k in kandidaten if k and os.path.isfile(k)), None)
    if pfad is None:
        fehler('Inventar daten/netze.csv nicht gefunden (Pflichtdatei; --inventar PFAD oder neben das Skript legen)')
    inv = set()
    try:
        with open(pfad, encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f, delimiter=';'):
                inv.add(row.get('pfad', ''))
    except Exception as e:
        fehler('Inventar %s unlesbar (%s)' % (pfad, e))
    fehlend = sorted(set(p for p in alle_pfade(regeln) if p not in inv and p != regeln.get('ft_ordner')))
    if fehlend:
        meld('WARNUNG: %d Netzpfade fehlen im Inventar und werden aus den Paletten gestrichen:' % len(fehlend))
        for p in fehlend:
            meld('   ', p)
        fm = set(fehlend)

        def streiche(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == 'netze' and isinstance(v, list):
                        o[k] = [p for p in v if p not in fm]
                    else:
                        streiche(v)
            elif isinstance(o, list):
                for v in o:
                    streiche(v)
        streiche(regeln)
    meld('Inventar %s: %d Netze, %d fehlen' % (pfad, len(inv), len(fehlend)))
    return pfad, fehlend


# ----------------------------------------------------------------------------- Weltdaten
def dominantes_feldbiom(basis, feld, regeln):
    """Fallback (nur wenn eigner.r8/welt.json fehlen): dominantes Biom des Feldes aus daten/biome_je_feld.json,
    sonst Tabelle feld_biom_fallback, sonst aue."""
    skript = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(basis, 'daten', 'biome_je_feld.json'), os.path.join(skript, 'biome_je_feld.json'),
              os.path.join(skript, '..', '..', 'daten', 'biome_je_feld.json'),
              os.path.join(skript, '..', '..', 'vorlagen', 'daten', 'biome_je_feld.json')):
        if not os.path.isfile(p):
            continue
        try:
            bp = json.load(open(p, encoding='utf-8'))['felder'][feld]['biome_prozent']
            if bp:
                return str(max(bp, key=lambda e: e[1])[0]), 'daten/biome_je_feld.json'
        except Exception:
            continue
    fb = regeln.get('feld_biom_fallback', {}).get(feld)
    if fb:
        return fb, 'feld_biom_fallback (Regeldatei)'
    return 'aue', 'Standard aue'


def lade_biome(basis, win, regeln, feld, bezug=None):
    """Biom je Zelle (Konventionen par. 1). Rueckgabe: eigen (bool H x W: Zelle gehoert zu biome_eigen),
    anteile {biom: Anteil im Fenster}, quelle (Text)."""
    Z = regeln['zustaendigkeit']
    eigen_l = set(Z['biome_eigen'])
    alle = list(Z['biome_alle'])
    null_biom = Z.get('eigner0_biom', 'aue')
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    welt = None
    if eig is not None and os.path.isfile(wj):
        try:
            welt = json.load(open(wj, encoding='utf-8'))
        except Exception as e:
            meld('Hinweis: welt.json unlesbar (%s)' % e)
    if eig is None or welt is None:
        fb, q = dominantes_feldbiom(basis, feld, regeln)
        meld('Hinweis: eigner.r8/welt.json fehlen - Biom je Zelle = dominantes Feldbiom %r (%s)' % (fb, q))
        return np.full((H, W), fb in eigen_l, bool), {fb: 1.0}, 'Fallback %s aus %s' % (fb, q)
    kacheln = welt.get('kacheln', {})
    namen = [null_biom] * 256
    unbekannt = []

    def biom_aus_rezept(rz):
        rz = str(rz).lower()
        if rz in alle:
            return rz
        if 'vulkan' in rz or 'lava' in rz:
            return 'lava'
        for n in alle:
            if n in rz:
                return n
        unbekannt.append(rz)
        return null_biom
    eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
    for k, v in eintraege:
        try:
            kk = int(v.get('kennzahl', v.get('id', k))) if isinstance(v, dict) else int(k)
        except Exception:
            continue
        if 0 < kk < 256:
            rz = v.get('rezept', '') if isinstance(v, dict) else ''
            namen[kk] = biom_aus_rezept(rz) if rz else null_biom
    namen[0] = null_biom  # Kennzahl 0 = Weltgelaende -> aue (Konventionen par. 1)
    if unbekannt:
        meld('Hinweis: %d Rezepte ohne Biom-Zuordnung (-> %s): %s' % (len(unbekannt), null_biom, ', '.join(sorted(set(unbekannt))[:6])))
    lut = np.array([n in eigen_l for n in namen], bool)
    eigen = lut[eig]
    e_b = eig[bezug] if bezug is not None else eig.ravel()  # Konventionen par. 1: Anteile nur ueber Landzellen
    zahl = np.bincount(e_b, minlength=256).astype(np.float64) / max(1, e_b.size)
    anteile = {}
    for kk in np.flatnonzero(zahl):
        anteile[namen[kk]] = anteile.get(namen[kk], 0.0) + float(zahl[kk])
    return eigen, anteile, 'eigner.r8 + welt.json'


def lade_ebene(ordner, win):
    """Instanzen einer Ebene im Fenster: Liste (name, fi, fj, massstab, ist_baum)."""
    aus = []
    pj = os.path.join(ordner, 'plan.json')
    if not os.path.isfile(pj):
        return aus, None
    try:
        plan = json.load(open(pj, encoding='utf-8'))
    except Exception:
        return aus, None
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
        txt = (str(info.get('rolle', '')) + ' ' + str(info.get('gruppe', '')) + ' ' + name).lower()
        ist_baum = any(r in txt for r in BAUM_ROLLEN) and not any(r in txt for r in NICHT_BAUM)
        aus.append((name, fi[m], fj[m], a[m, 9], ist_baum))
    return aus, plan


def lade_bestand(basis, feld, win, entf_prefixe):
    """Bäume (fi, fj, massstab) und Sonstiges aus bestand/, witcher/ (Feld + Nachbarn) und instanzen/instanzen.json.
    Netze, deren Name mit einem entfernen-Präfix beginnt, werden ignoriert (sie werden im Editor gelöscht)."""
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    baum, sonst, quellen = [], [], []
    plaene = {}
    namen_je_ebene = {'bestand': set(), 'witcher': set()}

    def entfernt(name):
        n = name.lower()
        return any(n.startswith(p) for p in entf_prefixe)
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(ord('A') + ss) + str(rr)
            for ebene in ('bestand', 'witcher'):
                inst, plan = lade_ebene(os.path.join(basis, WELT, ebene, nf), win)
                if plan is not None and ds == 0 and dr == 0:
                    plaene[ebene] = plan
                    namen_je_ebene[ebene] = set(n.lower() for n in plan.get('dateien', {}).keys())
                if inst:
                    quellen.append('%s/%s' % (ebene, nf))
                for name, fi, fj, ms, ist_baum in inst:
                    if fi.size == 0 or entfernt(name):
                        continue
                    arr = np.stack([fi, fj, ms], axis=1)
                    if ist_baum:
                        baum.append(arr)
                    elif ds == 0 and dr == 0:
                        sonst.append(arr)
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
    return baum, sonst, quellen, plaene, namen_je_ebene


# ----------------------------------------------------------------------------- Streuung
class Ctx(object):
    """Alle Felder/Masken des Fensters, die die Klassen brauchen."""
    pass


def kronendach(baeume, H, W, L):
    """Beschattung 0..1 aus Baumpositionen (Kronenfläche ~ Maßstab²), Gauß-geglättet."""
    if len(baeume) == 0:
        return np.zeros((H, W), np.float32), np.zeros((H, W), bool)
    bi = np.clip(np.round(baeume[:, 0]).astype(np.int32), 0, H - 1)
    bj = np.clip(np.round(baeume[:, 1]).astype(np.int32), 0, W - 1)
    gew = np.clip(baeume[:, 2], 0.3, 3.0) ** 2
    dichte = np.zeros((H, W), np.float32)
    np.add.at(dichte, (bi, bj), gew.astype(np.float32))
    dichte = gauss_blur(dichte, L['kronen_sigma_m'])
    deckung = math.pi * L['kronen_radius_m'] ** 2 * dichte
    beschattung = (1.0 - np.exp(-L['beschattung_k'] * deckung)).astype(np.float32)
    baum_m = np.zeros((H, W), bool)
    baum_m[bi, bj] = True
    return beschattung, baum_m


def lagenfaktor(lam, kl, lagen):
    for ln, w in kl.get('lagen_faktor', {}).items():
        if ln in lagen:
            lam = lam * (1 + (w - 1) * lagen[ln])
    return lam


def dichtefeld_schicht(kl, c, faktor):
    """λ je Zelle (Instanzen/m²) für Klassen der Schichten 0/1."""
    d0, d1 = kl['dichte']
    lam = (d0 * (1 - c.beschattung) + d1 * c.beschattung).astype(np.float32)
    lam *= 1 + (kl.get('saum', 1.0) - 1) * c.saum_norm
    lam = np.where(c.lichtung, lam * kl.get('lichtung', 1.0), lam)
    lam = np.where(c.lichtungsrand, lam * kl.get('lichtungsrand', 1.0), lam)
    ft, fn = kl.get('feuchte', [1.0, 1.0])
    lam *= ft + (fn - ft) * c.feuchte
    hm = kl.get('hang_max', 40)
    if hm < 60:
        lam *= np.clip((hm - c.hang) / max(1.0, hm - c.voll_bis), 0, 1)
    lam = lagenfaktor(lam, kl, c.lagen)
    if kl.get('mulde', 1.0) != 1.0:
        lam = np.where(c.mulde, lam * kl['mulde'], lam)
    if kl.get('nah_baum', 1.0) != 1.0:
        lam = np.where(c.nah_baum_3, lam * kl['nah_baum'], lam)
    if kl.get('wegrand', 1.0) != 1.0:
        lam = np.where(c.wegrand, lam * kl['wegrand'], lam)
    if kl.get('an_totholz', 1.0) != 1.0 and c.nah_totholz is not None:
        lam = np.where(c.nah_totholz, lam * kl['an_totholz'], lam)
    lam *= c.biomf * faktor
    return lam.astype(np.float32)


def ziehe(lam, frei, kl, c, kanal):
    """Zellweise Bernoulli (Einzel) oder Gruppen (Zentren + Kinder im Radius). Gibt fi, fj, mi, mj (Fenster) zurück."""
    H, W = lam.shape
    lam = np.where(frei, lam, 0).astype(np.float32)
    gmin, gmax = kl.get('gruppe', [1, 1])
    seed = c.seed
    leer = (np.zeros(0, np.float32),) * 2 + (np.zeros(0, np.int32),) * 2
    if gmax <= 1:
        idx = np.flatnonzero(lam > 0)
        if idx.size == 0:
            return leer
        ci, cj = c.ii.ravel()[idx], c.jj.ravel()[idx]
        u = hash01(c.gi.ravel()[idx], c.gj.ravel()[idx], seed, kanal)
        keep = u < lam.ravel()[idx]
        ci, cj = ci[keep], cj[keep]
        fi = ci + hash01(ci + c.wi0, cj + c.wj0, seed, kanal + 1) - 0.5
        fj = cj + hash01(ci + c.wi0, cj + c.wj0, seed, kanal + 2) - 0.5
        return fi.astype(np.float32), fj.astype(np.float32), ci.astype(np.int32), cj.astype(np.int32)
    gmit = 0.5 * (gmin + gmax)
    lamc = lam / gmit
    idx = np.flatnonzero(lamc > 0)
    if idx.size == 0:
        return leer
    ci, cj = c.ii.ravel()[idx], c.jj.ravel()[idx]
    u = hash01(c.gi.ravel()[idx], c.gj.ravel()[idx], seed, kanal)
    keep = u < lamc.ravel()[idx]
    ci, cj = ci[keep], cj[keep]
    if ci.size == 0:
        return leer
    n = gmin + np.floor(hash01(ci + c.wi0, cj + c.wj0, seed, kanal + 1) * (gmax - gmin + 1)).astype(np.int32)
    n = np.minimum(n, gmax)
    rep = np.repeat(np.arange(ci.size), gmax)
    k = np.tile(np.arange(gmax), ci.size)
    ok = k < n[rep]
    rep, k = rep[ok], k[ok]
    ang = hash01(ci[rep] + c.wi0 + 7 * k, cj[rep] + c.wj0 + 13 * k, seed, kanal + 3) * 2 * math.pi
    rad = np.sqrt(hash01(ci[rep] + c.wi0 + 3 * k, cj[rep] + c.wj0 + 5 * k, seed, kanal + 4)) * kl.get('radius_m', 1.0)
    fi = ci[rep] + rad * np.sin(ang)
    fj = cj[rep] + rad * np.cos(ang)
    mi = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
    mj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
    # Kinder nur, wo λ > 0; weiche Gruppenränder über λ(Kind)/λ(Zentrum)
    lz = lam[ci[rep], cj[rep]]
    lk = lam[mi, mj]
    w = np.where(lz > 0, np.minimum(1.0, lk / np.maximum(lz, 1e-9)), 0)
    ok = (lk > 0) & (hash01(mi + c.wi0 + 17 * k, mj + c.wj0 + 23 * k, seed, kanal + 5) < w)
    return fi[ok].astype(np.float32), fj[ok].astype(np.float32), mi[ok], mj[ok]


def ziehe_raster(lam, frei, raster_m, c, kanal):
    """Jitter-Raster-Stichprobe (eine Kandidatin je Rasterzelle, Annahme ~ λ·s²) → Mindestabstand ≈ 0,2·s."""
    H, W = lam.shape
    s = float(raster_m)
    lam = np.where(frei, lam, 0).astype(np.float32)
    ri0, ri1 = int(math.floor(c.wi0 / s)), int(math.floor((c.wi0 + H - 1) / s))
    rj0, rj1 = int(math.floor(c.wj0 / s)), int(math.floor((c.wj0 + W - 1) / s))
    ri, rj = np.meshgrid(np.arange(ri0, ri1 + 1), np.arange(rj0, rj1 + 1), indexing='ij')
    ri, rj = ri.ravel(), rj.ravel()
    gfi = (ri + 0.1 + 0.8 * hash01(ri, rj, c.seed, kanal + 1)) * s
    gfj = (rj + 0.1 + 0.8 * hash01(ri, rj, c.seed, kanal + 2)) * s
    fi, fj = gfi - c.wi0, gfj - c.wj0
    ok = (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1)
    ri, rj, fi, fj = ri[ok], rj[ok], fi[ok], fj[ok]
    mi = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
    mj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
    p = np.minimum(1.0, lam[mi, mj] * s * s)
    keep = hash01(ri, rj, c.seed, kanal) < p
    return fi[keep].astype(np.float32), fj[keep].astype(np.float32), mi[keep], mj[keep]


def ring_an_baum(baeume, kl, c, kanal, frei):
    """Instanzen im Ring um Baumstaemme (Wurzelanlaeufe, Efeu, Moos-Stamm). baeume: (n,4) fi,fj,massstab,klassenindex.
    Anzahl je Baum: an_baum.je_baum bzw. je_baum_klasse; Yaw radial / zum Stamm."""
    ab = kl['an_baum']
    n = baeume.shape[0]
    if n == 0:
        return (np.zeros(0, np.float32),) * 3 + (np.zeros(0, np.int32),) * 2
    bi = np.round(baeume[:, 0]).astype(np.int64) + c.wi0
    bj = np.round(baeume[:, 1]).astype(np.int64) + c.wj0
    u = hash01(bi, bj, c.seed, kanal)
    je = np.full(n, float(ab['je_baum']), np.float32)
    if ab.get('je_baum_klasse') and baeume.shape[1] >= 4:
        for kname, wert in ab['je_baum_klasse'].items():
            if kname in BAUM_REIHENFOLGE:
                je[baeume[:, 3] == BAUM_REIHENFOLGE.index(kname)] = wert
    anz = np.minimum(np.floor(je + u).astype(np.int32), int(ab['max_je_baum']))
    rep = np.repeat(np.arange(n), anz)
    if rep.size == 0:
        return (np.zeros(0, np.float32),) * 3 + (np.zeros(0, np.int32),) * 2
    start = np.repeat(np.cumsum(anz) - anz, anz)
    k = (np.arange(rep.size) - start).astype(np.int64)
    ang = hash01(bi[rep] + 31 * k, bj[rep] + 37 * k, c.seed, kanal + 1) * 2 * math.pi
    r0, r1 = ab['ring_m']
    rad = (r0 + (r1 - r0) * hash01(bi[rep] + 41 * k, bj[rep] + 43 * k, c.seed, kanal + 2)) * np.clip(baeume[rep, 2], 0.6, 1.8)
    fi = baeume[rep, 0] + rad * np.sin(ang)
    fj = baeume[rep, 1] + rad * np.cos(ang)
    H, W = frei.shape
    mi = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
    mj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
    ok = frei[mi, mj] & (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1)
    # Yaw: radial = Blick vom Stamm weg; zum_stamm = Rückseite zum Stamm. Winkel in Unreal-XY (X=j, Y=i).
    yaw = np.arctan2(np.sin(ang), np.cos(ang))  # Richtung (dY, dX) → atan2(dy, dx)
    if ab.get('yaw') == 'zum_stamm':
        yaw = yaw + math.pi
    return fi[ok].astype(np.float32), fj[ok].astype(np.float32), yaw[ok].astype(np.float32), mi[ok], mj[ok]


# ----------------------------------------------------------------------------- plan.json
def ausgabe_leeren(basis, feld):
    ausgabe = os.path.join(basis, WELT, THEMA, feld)
    os.makedirs(ausgabe, exist_ok=True)
    for f in sorted(os.listdir(ausgabe)):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    return ausgabe


def plan_grund(feld, regeln, anteile, zellen, kollision_anzahl, instanzen):
    """Pflichtschluessel nach FORMAT par. 3 und Konventionen par. 2."""
    return {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': int(instanzen), 'dateien': {},
            'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'biome_fenster': {k: round(v, 4) for k, v in sorted(anteile.items(), key=lambda kv: (-kv[1], kv[0]))},
            'biome_fenster_bezug': 'land', 'zellen_zustaendig': int(zellen), 'biome_eigen': list(regeln['zustaendigkeit']['biome_eigen']),
            'kollision_anzahl': int(kollision_anzahl)}


def schreibe_plan(ausgabe, plan):
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)


# ----------------------------------------------------------------------------- Planung je Feld
def plane_feld(feld, basis, regeln, faktor, bild, schichten, baum_modus, mittel_modus='zusatz'):
    t0 = time.time()
    rand = int(regeln.get('fenster_rand_m', 64))
    fb, win = feld_fenster(feld, rand)
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    if H <= 2 or W <= 2:
        meld('Feld %s liegt ausserhalb des Rasters' % feld)
        return None
    hinweise = []
    c = Ctx()
    c.seed = int(regeln['seed'])
    c.wi0, c.wj0 = wi0, wj0
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True)
    c.ii, c.jj = np.indices((H, W), dtype=np.int32)
    c.gi, c.gj = c.ii + wi0, c.jj + wj0
    im_feld = (c.gi >= fb[0]) & (c.gi < fb[1]) & (c.gj >= fb[2]) & (c.gj < fb[3])

    # ------------------------------------------------------------------ Zustaendigkeit (Konventionen par. 1)
    # Meer (Runde 4, Konventionen par. 1b): karte_wasser = nur Suesswasser
    wasser = lade_raster(os.path.join(basis, WELT, 'karte_wasser.r8'), np.uint8, win)
    wasser_m = (wasser > 0) if wasser is not None else np.zeros((H, W), bool)
    MR = meer_regel(regeln)
    meer = (hoehe < 0.0) & ~wasser_m
    wasser_alle = wasser_m | meer
    meer_zellen = int(meer.sum())
    meer_gef = {}

    Z = regeln['zustaendigkeit']
    # Konventionen par. 1 (Landzellen-Bezug, Runde 4): Anteile, 2-%-Schwelle und Saum nur ueber Landzellen ohne wasser_alle
    land_z = ~wasser_alle
    bezug = land_z if land_z.any() else np.ones((H, W), bool)
    eigen, bio_anteil, bio_quelle = lade_biome(basis, win, regeln, feld, bezug)
    eigen &= land_z
    eigen_anteil = float(eigen[bezug].mean())
    eigen_anteil_feld = float(eigen[im_feld & bezug].mean()) if (im_feld & bezug).any() else 0.0
    if eigen_anteil < float(Z['min_eigenanteil_fenster']):
        ausgabe = ausgabe_leeren(basis, feld)
        plan = plan_grund(feld, regeln, bio_anteil, 0, 0, 0)
        plan.update({'leer': True, 'eigenanteil_fenster': round(eigen_anteil, 4), 'biom_quelle': bio_quelle,
                     'meer_zellen': meer_zellen, 'meer_gefiltert': 0,
                     'hinweise': [ascii_text('Elfenwald-Anteil im Fenster %.2f %% < %.0f %% - kein Plan (Konventionen par. 1)' % (
                         100 * eigen_anteil, 100 * float(Z['min_eigenanteil_fenster'])))]})
        schreibe_plan(ausgabe, plan)
        meld('%s: elfenwald-Anteil im Fenster %.2f %% < %.0f %% - leerer plan.json (instanzen 0)' % (
            feld, 100 * eigen_anteil, 100 * float(Z['min_eigenanteil_fenster'])))
        return plan
    saum_m = float(Z['saum_m'])
    if eigen.all():
        zust = np.ones((H, W), np.float32)
    else:
        d_eigen = distanz(eigen, max_m=max(32.0, saum_m + 2))
        zust = np.where(eigen, 1.0, np.where(land_z, np.clip(1.0 - d_eigen / saum_m, 0, 1), 0)).astype(np.float32)  # Saum nur auf Land

    # Gelände
    dzdy, dzdx = np.gradient(hoehe)
    c.hang = np.degrees(np.arctan(np.sqrt(dzdx ** 2 + dzdy ** 2))).astype(np.float32)
    nl = np.sqrt(dzdx ** 2 + dzdy ** 2 + 1.0)
    n_x, n_y, n_z = (-dzdx / nl).astype(np.float32), (-dzdy / nl).astype(np.float32), (1.0 / nl).astype(np.float32)
    c.voll_bis = regeln['hang']['voll_bis_grad']
    land = (hoehe > regeln['land']['min_hoehe_m']) & ~meer
    hs = gauss_blur(hoehe, regeln['mulde']['sigma_m'])
    lap = (verschiebe(hs, 1, 0, 0) + verschiebe(hs, -1, 0, 0) + verschiebe(hs, 0, 1, 0) + verschiebe(hs, 0, -1, 0) - 4 * hs)
    c.mulde = lap > regeln['mulde']['schwelle']

    # Karten
    def r8(name):
        return lade_raster(os.path.join(basis, WELT, name), np.uint8, win)
    weg, ort = r8('karte_weg.r8'), r8('karte_ort.r8')
    for nm, a in (('karte_wasser.r8', wasser), ('karte_weg.r8', weg), ('karte_ort.r8', ort)):
        if a is None:
            hinweise.append('%s fehlt – Annahme: keine Fläche dieser Art' % nm)
    weg_m = (weg > 0) if weg is not None else np.zeros((H, W), bool)
    ort_m = (ort > 0) if ort is not None else np.zeros((H, W), bool)
    abst = regeln['abstand_m']
    d_wasser = distanz(wasser_m, max_m=64.0)  # Suesswasser: Bachsaum, bach_dichte
    d_wasser_alle = distanz(wasser_alle, max_m=64.0) if meer.any() else d_wasser  # Wassernaehe allgemein (Feuchte)
    kueste_nah = (distanz(meer, max_m=max(32.0, float(MR['kuesten_saum_m']) + 2)) <= float(MR['kuesten_saum_m'])) if meer.any() \
        else np.zeros((H, W), bool)
    nah_weg_klein = dilate(weg_m, abst['weg_klein'])
    nah_weg_gross = dilate(weg_m, abst['weg_gross'])
    nah_ort = dilate(ort_m, abst['ort'])
    nah_wasser = dilate(wasser_alle, abst['wasser']) if abst['wasser'] >= 1 else wasser_alle
    d_weg = distanz(weg_m, max_m=64.0)
    Wr = regeln['wegrand']
    c.wegrand = (d_weg >= Wr['von_m']) & (d_weg <= Wr['bis_m'])
    # Bach vs. Fluss/See: Halbbreite der Wasserfläche nahe dem Ufer
    B = regeln['bach']
    if wasser_m.any():
        d_innen = distanz(~wasser_m, max_m=32.0)
        halbbreite = max_filter(np.where(wasser_m, d_innen, 0).astype(np.float32), 8)
        ist_bach = halbbreite <= B['max_halbbreite_m']
    else:
        ist_bach = np.zeros((H, W), bool)
    c.bach_faktor = np.where(ist_bach, 1.0, B['gross_faktor']).astype(np.float32)

    # Lagen
    lagen_namen = set(regeln['feuchte']['lagen']) | set(regeln['licht']['fallback_lagen'])
    for sch in regeln['schichten'].values():
        for kl in sch.values():
            lagen_namen |= set(kl.get('lagen_faktor', {}).keys())
    for kl in regeln['baum']['klassen'].values():
        lagen_namen |= set(kl.get('lagen_faktor', {}).keys())
    c.lagen = {}
    for ln in sorted(lagen_namen):
        a = r8('lage_%s.r8' % ln)
        if a is not None:
            c.lagen[ln] = a.astype(np.float32) / 255.0
    if not c.lagen:
        hinweise.append('keine lage_*.r8 gefunden – Feuchte nur aus Wassernähe, Lagenfaktoren = 1')

    # Zustaendigkeitsfaktor je Zelle (1 im Elfenwald, linear 1 -> 0 im 30-m-Saum, sonst 0) nur auf Land
    c.biomf = np.where(land, zust, 0).astype(np.float32)
    zellen_zustaendig = int(((c.biomf > 0) & im_feld).sum())

    # Feuchte
    F = regeln['feuchte']
    feuchte = np.clip(1 - d_wasser_alle / F['wasser_radius_m'], 0, 1) * 0.8
    for ln, w in F['lagen'].items():
        if ln in c.lagen:
            feuchte += w * c.lagen[ln]
    c.feuchte = np.clip(feuchte, 0, 1).astype(np.float32)

    # ------------------------------------------------------------------ vorhandene Ebenen, Modus, entfernen
    E = regeln['entfernen']
    bestand_da = os.path.isfile(os.path.join(basis, WELT, 'bestand', feld, 'plan.json'))
    if baum_modus == 'auto':
        baum_modus = 'ergaenzen' if bestand_da else 'voll'
    if '2' not in schichten:
        baum_modus = 'keine'
    entf = list(E['witcher_mit_bestand'] if bestand_da else E['witcher_ohne_bestand'])
    if baum_modus == 'voll':
        entf += E['witcher_baeume_bei_voll'] + E['bestand_bei_voll']
    entf = [p.lower() for p in entf]
    baeume_alt, sonst, quellen, plaene, namen_je_ebene = lade_bestand(basis, feld, win, entf)
    vorhanden = namen_je_ebene['witcher'] | namen_je_ebene['bestand']
    if E.get('nur_wenn_vorhanden', True):
        entf_aktiv = sorted(set(p for p in entf if any(n.startswith(p) for n in vorhanden)))
    else:
        entf_aktiv = sorted(set(entf))
    if entf_aktiv and eigen_anteil_feld < float(Z.get('entfernen_min_eigenanteil_feld', 0.5)):
        hinweise.append('entfernen-Filter nicht gesetzt: elfenwald-Anteil im Feld %.0f %% < %.0f %% (Fremdbiome behalten ihre Witcher-Ebene)' % (
            100 * eigen_anteil_feld, 100 * float(Z.get('entfernen_min_eigenanteil_feld', 0.5))))
        entf_aktiv = []
    hinweise.append('Baum-Modus %s (Bestand-Ebene %s); %d vorhandene Bäume, %d sonstige Instanzen aus %s' % (
        baum_modus, 'vorhanden' if bestand_da else 'fehlt', len(baeume_alt), len(sonst), ', '.join(quellen[:6]) + (' …' if len(quellen) > 6 else '')))
    if entf_aktiv:
        hinweise.append('entfernen-Filter (%d Präfixe, nur im Feld vorhandene): %s' % (len(entf_aktiv), ','.join(entf_aktiv[:12]) + (' …' if len(entf_aktiv) > 12 else '')))

    L = regeln['licht']
    besch_alt, baum_m_alt = kronendach(baeume_alt, H, W, L)
    belegt = np.zeros((H, W), bool)
    if len(sonst):
        si = np.clip(np.round(sonst[:, 0]).astype(np.int32), 0, H - 1)
        sj = np.clip(np.round(sonst[:, 1]).astype(np.int32), 0, W - 1)
        belegt[si, sj] = True
        belegt = dilate(belegt, abst['bestand_sonst'])

    # Waldgebiet (Biom) und Saum für die Baumschicht
    waldgebiet = (c.biomf > 0) & land & ~wasser_alle & ~ort_m
    kante_g = waldgebiet & dilate(~waldgebiet, 1)
    d_kante_g = distanz(kante_g, max_m=64.0)
    saum_g = np.where(waldgebiet, np.clip(1 - d_kante_g / L['saum_innen_m'], 0, 1), np.clip(1 - d_kante_g / L['saum_aussen_m'], 0, 1)).astype(np.float32)

    # Klumpen / Lichtungen (nahtloses Wertrauschen)
    K = regeln['baum']['klumpen']
    klump = np.zeros((H, W), np.float32)
    for wl, gw, kn in zip(K['wellen_m'], K['gewichte'], range(len(K['wellen_m']))):
        klump += gw * wertrausch(c.gi, c.gj, c.seed, wl, 900 + kn)
    licht_k = klump < K['lichtung_schwelle']
    k0, k1 = K['dichte_kern']
    kern = (k0 + (k1 - k0) * np.clip((klump - K['lichtung_schwelle']) / max(1e-6, 1 - K['lichtung_schwelle']), 0, 1)).astype(np.float32)
    klumpf = np.where(licht_k, K['dichte_in_lichtung'], kern).astype(np.float32)
    rand_k = licht_k & dilate(~licht_k, 1)
    d_rand_k = distanz(rand_k, max_m=32.0)
    lichtungsrand_k = (~licht_k) & (d_rand_k <= L['lichtungsrand_m'])  # Waldseite des Lichtungsrands (Baumschicht)
    Hh = regeln['hoehe']
    f_hoehe = np.clip((Hh['baum_null_ab_m'] - hoehe) / max(1.0, Hh['baum_null_ab_m'] - Hh['baum_abnahme_ab_m']), 0, 1).astype(np.float32)

    aus = []  # dict je Klasse: schicht, klasse, fi, fj, mi, mj, yaw(optional), ...
    stat = {}

    def meer_ok(schicht, kname, kl, fi, fj):
        """Runde 4: Meer-Schlussfilter am Instanzort; zaehlt nur verworfene Instanzen im Feld (meer_gefiltert)."""
        if fi.size == 0:
            return np.ones(0, bool)
        ci = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
        cj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
        keep = meer_behalten(bilinear(hoehe, fi, fj), ci, cj, meer, wasser_m, kueste_nah, ROLLE_JE_SCHICHT[schicht], kl, MR)
        imf = (fi + wi0 >= fb[0]) & (fi + wi0 < fb[1]) & (fj + wj0 >= fb[2]) & (fj + wj0 < fb[3])
        n = int((~keep & imf).sum())
        if n:
            meer_gef[schicht + '/' + kname] = meer_gef.get(schicht + '/' + kname, 0) + n
        return keep

    def merke(schicht, kname, kl, fi, fj, mi, mj, yaw=None, netz_hash=None):
        ok = (fi + wi0 >= fb[0]) & (fi + wi0 < fb[1]) & (fj + wj0 >= fb[2]) & (fj + wj0 < fb[3])  # exakte Feldgrenze
        ok &= meer_ok(schicht, kname, kl, fi, fj)  # Runde 4 (Konventionen par. 1b)
        fi, fj, mi, mj = fi[ok], fj[ok], mi[ok], mj[ok]
        if yaw is not None:
            yaw = yaw[ok]
        if fi.size == 0:
            return None
        gmi, gmj = mi + wi0, mj + wj0
        kanal = 50000 + (kanal_von(schicht + kname) % 9000) * 10
        hv = hash01(gmi, gmj, c.seed, kanal + 5) + 0.37 * hash01(np.round(fi * 7).astype(np.int64), np.round(fj * 7).astype(np.int64), c.seed, kanal + 6)
        hv = hv % 1.0
        netzl = kl['netze']
        nidx = np.minimum((hv * len(netzl)).astype(np.int32), len(netzl) - 1)
        ms = kl['massstab'][0] + (kl['massstab'][1] - kl['massstab'][0]) * hash01(gmi, gmj, c.seed, kanal + 7)
        if yaw is None:
            yaw = hash01(gmi, gmj, c.seed, kanal + 8) * 2 * math.pi
            if kl.get('laengs_hang'):
                asp = np.arctan2(-dzdy[mi, mj], -dzdx[mi, mj])
                yaw = asp + (hash01(gmi, gmj, c.seed, kanal + 9) - 0.5) * math.radians(40) + np.where(hash01(gmi, gmj, c.seed, kanal + 10) < 0.5, 0, math.pi)
        d = dict(schicht=schicht, klasse=kname, fi=fi.astype(np.float32), fj=fj.astype(np.float32), mi=mi, mj=mj, netz=nidx,
                 massstab=ms.astype(np.float32), yaw=yaw.astype(np.float32), kippen=kl['kippen'], eingraben=kl['eingraben_cm'],
                 kollision=bool(kl['kollision']), schatten=bool(kl.get('schatten', True)), sichtweite=list(kl['sichtweite']), netze=netzl)
        aus.append(d)
        stat.setdefault(schicht, {})[kname] = stat.get(schicht, {}).get(kname, 0) + int(fi.size)
        return d

    # ------------------------------------------------------------------ Schicht 2: Bäume
    baum_neu = []  # (fi, fj, massstab, klasse) im Fenster (inkl. Rand → Nahtlosigkeit des Kronendachs)
    belegt_baum = dilate(baum_m_alt, abst['bestand_baum_zu_neuem_baum']) if baum_m_alt.any() else np.zeros((H, W), bool)
    frei_baum_basis = waldgebiet & ~nah_wasser & ~nah_weg_gross & ~nah_ort & ~belegt
    BK = regeln['baum']['klassen']
    if baum_modus in ('voll', 'ergaenzen'):
        Eg = regeln['baum']['ergaenzen']
        if baum_modus == 'ergaenzen':
            # Lichtungen/Ränder aus dem vorhandenen Kronendach
            wald_e = besch_alt > L['wald_schwelle']
            kante_e = wald_e & dilate(~wald_e, 1)
            d_kante_e = distanz(kante_e, max_m=64.0)
            licht_e = (~wald_e) & (besch_alt < L['lichtung_schwelle']) & (d_kante_e < 40)
            rand_e = licht_e & (d_kante_e <= L['lichtungsrand_m'])
        for kname in BAUM_REIHENFOLGE:
            kl = BK.get(kname)
            if kl is None or not kl['netze']:
                continue
            if baum_modus == 'ergaenzen' and kname not in ('hero', 'tot'):
                continue
            kanal = 1000 + BAUM_REIHENFOLGE.index(kname) * 20
            d0, d1 = kl['dichte']
            if baum_modus == 'voll':
                lam = np.full((H, W), d0, np.float32) * klumpf
                lam = np.where(licht_k, np.full((H, W), d0, np.float32) * K['dichte_in_lichtung'] * kl.get('lichtung', 1.0), lam)
                lam = np.where(lichtungsrand_k, lam * kl.get('lichtungsrand', 1.0), lam)
                lam *= 1 + (kl.get('saum', 1.0) - 1) * saum_g
                if kl.get('bach_dichte'):
                    b0, b1 = kl['bach_band_m']
                    lam = np.where((d_wasser >= b0) & (d_wasser <= b1) & ist_bach, lam + kl['bach_dichte'], lam)
            else:
                je_ha = Eg['hero_je_ha'] if kname == 'hero' else Eg['tot_je_ha']
                lam = np.full((H, W), je_ha / 10000.0, np.float32)
                if kname == 'hero':
                    lam = np.where(rand_e, lam * 8.0, np.where(licht_e, lam * 0.5, lam * 0.15))
                else:
                    lam = np.where(wald_e, lam, lam * 0.3)
            ft, fn = kl.get('feuchte', [1.0, 1.0])
            lam *= ft + (fn - ft) * c.feuchte
            hm = kl.get('hang_max', 40)
            lam *= np.clip((hm - c.hang) / max(1.0, hm - c.voll_bis), 0, 1)
            lam = lagenfaktor(lam, kl, c.lagen)
            lam *= f_hoehe * c.biomf * faktor
            frei = frei_baum_basis & ~belegt_baum
            if kl.get('min_abstand_m', 0) > 0 and baum_neu:
                pass  # belegt_baum enthält bereits die größeren Klassen
            fi, fj, mi, mj = ziehe_raster(lam, frei, kl['raster_m'], c, kanal)
            mk = meer_ok('2_baum', kname, kl, fi, fj)  # Runde 4: Baeume am Meer auch nicht fuers Kronendach zaehlen
            fi, fj, mi, mj = fi[mk], fj[mk], mi[mk], mj[mk]
            if fi.size == 0:
                continue
            d = merke('2_baum', kname, kl, fi, fj, mi, mj)
            # alle (auch Rand) für Kronendach und Abstände
            ms_all = kl['massstab'][0] + (kl['massstab'][1] - kl['massstab'][0]) * hash01(mi + wi0, mj + wj0, c.seed, 50000 + (kanal_von('2_baum' + kname) % 9000) * 10 + 7)
            baum_neu.append(np.stack([fi, fj, ms_all.astype(np.float32), np.full(fi.size, BAUM_REIHENFOLGE.index(kname), np.float32)], axis=1))
            m_neu = np.zeros((H, W), bool)
            m_neu[mi, mj] = True
            r_ab = max(kl.get('min_abstand_m', 1.0), 1.0)
            belegt_baum |= dilate(m_neu, r_ab)
    if '2' in schichten and baum_modus == 'voll' and not stat.get('2_baum'):
        hinweise.append('Baumschicht leer – kein Waldgebiet (Biom/Land) im Fenster?')

    # Kronendach gesamt: vorhandene + neue Bäume
    baum_neu_arr = np.concatenate(baum_neu, axis=0) if baum_neu else np.zeros((0, 4), np.float32)
    alle_baeume = np.concatenate([baeume_alt, baum_neu_arr[:, :3]], axis=0) if len(baum_neu_arr) else baeume_alt
    if len(alle_baeume):
        c.beschattung, baum_m = kronendach(alle_baeume, H, W, L)
        hinweise.append('Kronendach aus %d Bäumen (%d vorhanden, %d neu)' % (len(alle_baeume), len(baeume_alt), len(baum_neu_arr)))
    else:
        c.beschattung = np.zeros((H, W), np.float32)
        for ln, w in L['fallback_lagen'].items():
            if ln in c.lagen:
                c.beschattung += w * c.lagen[ln]
        c.beschattung = np.clip(gauss_blur(c.beschattung, 8.0), 0, L['fallback_beschattung_max']).astype(np.float32)
        baum_m = np.zeros((H, W), bool)
        hinweise.append('keine Bäume (Ebenen fehlen, Baumschicht aus) – Beschattung aus Lagen geschätzt, max %.2f' % L['fallback_beschattung_max'])
    nah_baum = dilate(baum_m, abst['baumstamm']) if baum_m.any() else np.zeros((H, W), bool)
    c.nah_baum_3 = dilate(baum_m, 3.0) if baum_m.any() else np.zeros((H, W), bool)
    wald = c.beschattung > L['wald_schwelle']
    kante = wald & dilate(~wald, 1)
    d_kante = distanz(kante, max_m=64.0)
    c.saum_norm = np.where(wald, np.clip(1 - d_kante / L['saum_innen_m'], 0, 1), np.clip(1 - d_kante / L['saum_aussen_m'], 0, 1)).astype(np.float32)
    c.lichtung = (~wald) & (c.beschattung < L['lichtung_schwelle']) & (d_kante < 40) & waldgebiet
    c.lichtungsrand = c.lichtung & (d_kante <= L['lichtungsrand_m'])
    c.nah_totholz = None
    frei_basis = land & (c.biomf > 0) & ~nah_wasser & ~nah_ort & ~belegt

    # Bäume für an_baum-Klassen (alt/hero/tot): neue nach Klasse, vorhandene ab Maßstab 0.9 als „alt“
    def baeume_fuer(klassen):
        """(n,4) fi, fj, massstab, Klassenindex (BAUM_REIHENFOLGE); vorhandene Baeume ab Massstab 0.9 zaehlen als alt."""
        teile = []
        if len(baum_neu_arr):
            idx = np.array([BAUM_REIHENFOLGE.index(k) for k in klassen if k in BAUM_REIHENFOLGE], np.float32)
            m = np.isin(baum_neu_arr[:, 3], idx)
            teile.append(baum_neu_arr[m, :4].astype(np.float32))
        if len(baeume_alt) and ('alt' in klassen):
            a = baeume_alt[baeume_alt[:, 2] >= 0.9]
            teile.append(np.concatenate([a[:, :3], np.full((len(a), 1), BAUM_REIHENFOLGE.index('alt'), np.float32)], axis=1).astype(np.float32))
        return np.concatenate(teile, axis=0) if teile else np.zeros((0, 4), np.float32)

    # ------------------------------------------------------------------ Schichten 1 und 0
    gross = set(['moosstamm', 'embankment'])
    EB = regeln.get('ebenen', {})
    generisch = set(EB.get('generisch_mittelschicht', []))
    alias = EB.get('alias', {})
    if mittel_modus == 'voll':
        hinweise.append('--mittel voll ist seit Korrektur Runde 1 wirkungslos und verhaelt sich wie zusatz: generische Mittelschicht-Klassen '
                        '(%s) setzt nur mittelschicht_plan.py mit elfenwald_regeln.json[mittelschicht_overrides]' % ','.join(sorted(generisch)))
        mittel_modus = 'zusatz'
    # stehendes Totholz (neu) fuer Pilz-/Moos-Bonus an Totholz
    m_tot = np.zeros((H, W), bool)
    if len(baum_neu_arr):
        bt = baum_neu_arr[baum_neu_arr[:, 3] == BAUM_REIHENFOLGE.index('tot')]
        if len(bt):
            m_tot[np.clip(np.round(bt[:, 0]).astype(np.int32), 0, H - 1), np.clip(np.round(bt[:, 1]).astype(np.int32), 0, W - 1)] = True
    for schicht in ('1_mittel', '0_boden'):
        if schicht[0] not in schichten:
            continue
        for kidx, (kname, kl) in enumerate(regeln['schichten'][schicht].items()):
            if not kl['netze']:
                continue
            if kname in generisch or alias.get(kname) in generisch:
                hinweise.append('Klasse %s/%s uebersprungen: generische Mittelschicht (mittelschicht_plan.py, Konventionen par. 4)' % (schicht, kname))
                continue
            kanal = (3000 if schicht == '1_mittel' else 5000) + kidx * 20
            frei = frei_basis & ~(nah_weg_gross if kname in gross else nah_weg_klein)
            if kl.get('an_baum'):
                frei_ab = frei & ~wasser_alle
                bt = baeume_fuer(kl['an_baum']['klassen'])
                fi, fj, yaw, mi, mj = ring_an_baum(bt, kl, c, kanal, frei_ab)
                if fi.size:
                    keep = c.biomf[mi, mj] * faktor >= hash01(mi + wi0, mj + wj0, c.seed, kanal + 9)
                    merke(schicht, kname, kl, fi[keep], fj[keep], mi[keep], mj[keep], yaw=yaw[keep])
                continue
            frei = frei & ~nah_baum
            lam = dichtefeld_schicht(kl, c, faktor)
            fi, fj, mi, mj = ziehe(lam, frei, kl, c, kanal)
            if fi.size == 0:
                continue
            merke(schicht, kname, kl, fi, fj, mi, mj)
        if schicht == '1_mittel':
            # Totholz-Naehe (Moos-Staemme + stehendes Totholz) fuer Moos der Bodenschicht
            m = m_tot.copy()
            for a in aus:
                if a['schicht'] == '1_mittel' and regeln['schichten']['1_mittel'].get(a['klasse'], {}).get('ist_totholz'):
                    m[a['mi'], a['mj']] = True
            c.nah_totholz = dilate(m, 1.8) if m.any() else None

    # ------------------------------------------------------------------ Schicht 5: Wasserkante
    if '5' in schichten and wasser_m.any():
        for kidx, (kname, kl) in enumerate(regeln['schichten']['5_wasserkante'].items()):
            if not kl['netze']:
                continue
            kanal = 7000 + kidx * 20
            b0, b1 = kl['band_m']
            d0, d1 = kl['dichte_band']
            t = np.clip((d_wasser - b0) / max(0.1, b1 - b0), 0, 1)
            lam = np.where((d_wasser >= b0) & (d_wasser <= b1), d0 + (d1 - d0) * t, 0).astype(np.float32)
            hm = kl.get('hang_max', 40)
            lam *= np.clip((hm - c.hang) / max(1.0, hm - min(c.voll_bis, hm - 1)), 0, 1)
            if kl.get('hang_min', 0) > 0:
                lam = np.where(c.hang >= kl['hang_min'], lam, 0)
            lam = lagenfaktor(lam, kl, c.lagen)
            lam *= c.bach_faktor * c.biomf * faktor
            frei = land & ~nah_wasser & ~nah_ort & ~belegt & ~nah_baum & ~(nah_weg_gross if kname in gross else nah_weg_klein)
            fi, fj, mi, mj = ziehe(lam, frei, kl, c, kanal)
            if fi.size:
                merke('5_wasserkante', kname, kl, fi, fj, mi, mj)
    elif '5' in schichten:
        hinweise.append('keine Wasserfläche im Fenster – Wasserkante leer')

    # ------------------------------------------------------------------ Budget je Feld (Konventionen par. 3, hart)
    Bg = regeln['budget']
    deckel = int(Bg['deckel_je_feld'])
    ziel_lo, ziel_hi = [int(v) for v in Bg['ziel_je_feld']]
    auf = min(deckel, int(Bg.get('ausduennen_auf', ziel_hi)))
    koll_max = int(Bg['kollision_je_feld'])
    max_aus = float(Bg.get('max_ausduennung_je_klasse', 0.6))
    LG = regeln.get('landschaftsgras', {}).get('klassen', {})

    def je_klasse():
        st = {}
        for a in aus:
            k = a['schicht'] + '/' + a['klasse']
            st[k] = st.get(k, 0) + int(a['fi'].size)
        return st

    def duenne(key, f, stufe):
        """Deterministische Hash-Ausduennung einer Klasse auf Anteil f (Kanal je Klasse und Stufe)."""
        for a in aus:
            if a['schicht'] + '/' + a['klasse'] != key or f >= 1.0 or a['fi'].size == 0:
                continue
            keep = hash01(a['mi'] + wi0, a['mj'] + wj0, c.seed, 99991 + stufe * 7919 + (kanal_von(key) % 7919)) < f
            for k in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw'):
                a[k] = a[k][keep]

    st0 = je_klasse()
    vorher = sum(st0.values())
    ausduenn = {}
    if vorher > auf:
        prio = [k for k in Bg['prioritaet_ausduennen']] + sorted(k for k in st0 if k not in Bg['prioritaet_ausduennen'])
        ueber = vorher - auf
        for key in prio:  # Stufe 1: Klassen in Prioritaet, je hoechstens max_aus
            n = je_klasse().get(key, 0)
            if ueber <= 0:
                break
            if n == 0:
                continue
            f = 1.0 - min(float(ueber), n * max_aus) / n
            duenne(key, f, 1)
            n2 = je_klasse().get(key, 0)
            ueber -= (n - n2)
        stufe = 2
        while sum(je_klasse().values()) > auf and stufe < 8:  # Stufe 2+: alle Nicht-Baum-Klassen gleichmaessig
            st = je_klasse()
            nb = sum(v for k, v in st.items() if not k.startswith('2_baum'))
            ueber = sum(st.values()) - auf
            f = max(0.0, 1.0 - 1.02 * ueber / max(1, nb))
            for key in st:
                if not key.startswith('2_baum'):
                    duenne(key, f, stufe)
            stufe += 1
        st1 = je_klasse()
        for key, n in st0.items():
            if st1.get(key, 0) < n:
                ausduenn[key] = round(st1.get(key, 0) / float(n), 3)
        meld('WARNUNG: %s Budget: %d Instanzen > %d (Ziel %d-%d, Deckel %d) - deterministisch ausgeduennt: %s' % (
            feld, vorher, auf, ziel_lo, ziel_hi, deckel, ', '.join('%s x%.2f' % kv for kv in sorted(ausduenn.items()))))
        hinweise.append('Budget: %d -> %d Instanzen (Ziel %d-%d, Deckel %d); Ausduennung nach Prioritaet: %s' % (
            vorher, sum(st1.values()), ziel_lo, ziel_hi, deckel, ', '.join('%s x%.2f' % kv for kv in sorted(ausduenn.items()))))
    nachher = sum(je_klasse().values())
    if nachher > deckel:  # darf nach den Stufen nicht vorkommen - harte Sicherung
        f = deckel / float(nachher) * 0.99
        for key in je_klasse():
            duenne(key, f, 9)
        meld('WARNUNG: %s harte Deckel-Sicherung: %d -> %d' % (feld, nachher, sum(je_klasse().values())))
    an_gras = {}
    for kname, gt in LG.items():
        key = '0_boden/' + kname
        an_gras[kname] = {'grasart': gt, 'behalten_anteil': ausduenn.get(key, 1.0)}
    abgabe = ['%s %d %%' % (k, round(100 * (1 - v['behalten_anteil']))) for k, v in sorted(an_gras.items()) if v['behalten_anteil'] < 1.0]
    hinweise.append('Kleinzeug an Landschafts-Gras: Laub/Zweige/Moos/Kraut -> GT_Kraut, Kleinsteine -> GT_Steinchen (Lage Laub/Moos im Elfenwald '
                    'mit hoher Grasdichte malen); diese Ebene setzt nur Haufen in Mulden und am Stammfuss%s' % (
                        ('; wegen Budget abgegeben: ' + ', '.join(abgabe)) if abgabe else ''))

    # Kollision je Netz (Foliage-Typ) in Prioritaet bis kollision_je_feld (auch Baeume; keine Ausnahme mehr)
    kprio = list(Bg['kollision_prioritaet'])
    koll_prio = {}
    for a in aus:
        if not a['kollision'] or a['fi'].size == 0:
            continue
        pr = kprio.index(a['klasse']) if a['klasse'] in kprio else len(kprio)
        for ni in np.unique(a['netz']):
            nm = a['netze'][ni].rsplit('/', 1)[-1]
            koll_prio[nm] = min(koll_prio.get(nm, 99), pr)
    anz_netz = {}
    for a in aus:
        if a['fi'].size == 0:
            continue
        nis, cnt = np.unique(a['netz'], return_counts=True)
        for ni, cn in zip(nis, cnt):
            nm = a['netze'][ni].rsplit('/', 1)[-1]
            if nm in koll_prio:
                anz_netz[nm] = anz_netz.get(nm, 0) + int(cn)
    rest = koll_max
    koll_an, koll_aus = set(), []
    for nm in sorted(koll_prio, key=lambda n: (koll_prio[n], anz_netz.get(n, 0), n)):
        n = anz_netz.get(nm, 0)
        if n <= rest:
            koll_an.add(nm)
            rest -= n
        else:
            koll_aus.append(nm)
    if koll_aus:
        n_aus = sum(anz_netz[n] for n in koll_aus)
        kl_aus = sorted(set(kprio[koll_prio[n]] if koll_prio[n] < len(kprio) else '?' for n in koll_aus))
        hinweise.append('Kollisionsbudget %d: %d Instanzen in %d Netzen mit Kollision; %d Netze / %d Instanzen ohne Kollision (Klassen %s, '
                        'kleinere Baumklassen zuerst) - Konventionen par. 3' % (koll_max, koll_max - rest, len(koll_an), len(koll_aus), n_aus,
                                                                                 ','.join(kl_aus)))

    # ------------------------------------------------------------------ Blickziele (Vorschläge, keine Instanzen)
    blickziele = []
    try:
        Bz = regeln['blickziele']
        li = c.lichtung & im_feld
        if li.any():
            d_li = distanz(~li, max_m=48.0)
            d_li = np.where(im_feld, d_li, 0)
            k = int(np.argmax(d_li))
            pi, pj = k // W, k % W
            if d_li[pi, pj] >= Bz['lichtung']['min_radius_m']:
                blickziele.append({'art': 'lichtung_mit_blumen', 'x_cm': float((pj + wj0 - X0) * 100), 'y_cm': float((pi + wi0 - Y0) * 100),
                                   'z_cm': float(hoehe[pi, pj] * 100), 'radius_m': float(d_li[pi, pj]),
                                   'regel': 'größte Lichtung (max. Abstand zum Kronendach); Hero-Altbaum am Rand, Blumeninsel innen (blume_lichtung x%.1f im Umkreis)' % Bz['lichtung']['blumen_faktor']})
        hs25 = gauss_blur(hoehe, 12.0)
        kuppe = (hs25 >= max_filter(hs25, 15) - 0.01) & (c.hang < Bz['kuppe']['hang_max_grad']) & land & ~wasser_alle & im_feld
        kuppe &= (d_weg >= Bz['kuppe']['weg_abstand_m'][0]) & (d_weg <= Bz['kuppe']['weg_abstand_m'][1])
        if kuppe.any():
            k = int(np.argmax(np.where(kuppe, hs25, -1e9)))
            pi, pj = k // W, k % W
            blickziele.append({'art': 'ruine_auf_kuppe', 'x_cm': float((pj + wj0 - X0) * 100), 'y_cm': float((pi + wi0 - Y0) * 100),
                               'z_cm': float(hoehe[pi, pj] * 100), 'regel': 'lokales Höhenmaximum (geglättet) mit Hang < %d°, %d–%d m vom Weg: Ruinenwand SM_Wall_01 + 2–4 Säulen SM_Column_02 (spuren_overrides.ruine)' % (Bz['kuppe']['hang_max_grad'], Bz['kuppe']['weg_abstand_m'][0], Bz['kuppe']['weg_abstand_m'][1])})
        quer = dilate(weg_m, 6) & wasser_m & im_feld if weg_m.any() else np.zeros((H, W), bool)
        if quer.any():
            d_q = np.where(quer, distanz(~quer, max_m=16.0), 0)
            k = int(np.argmax(d_q))
            pi, pj = k // W, k % W
            blickziele.append({'art': 'schrein_an_bachquerung', 'x_cm': float((pj + wj0 - X0) * 100), 'y_cm': float((pi + wi0 - Y0) * 100),
                               'z_cm': float(hoehe[pi, pj] * 100), 'regel': 'Weg kreuzt Wasser: SM_Sviatovid_Stone 3 m neben dem Weg, Moossteine x2 im Umkreis 8 m (spuren_overrides.schrein)'})
    except Exception as e:  # Blickziele sind nur Vorschläge – nie den Lauf abbrechen
        hinweise.append('Blickziele nicht berechnet (%s)' % e)

    # ------------------------------------------------------------------ Instanzen bauen und schreiben
    ausgabe = ausgabe_leeren(basis, feld)
    dateien, netz_inst = {}, {}
    stat = {}
    nk = {'2_baum': 0, 'andere': 0}
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
            basisname = p.rsplit('/', 1)[-1]
            name = basisname
            if name in dateien and dateien[name]['ebene'] != a['schicht']:
                # Runde 4: gleiches Netz in anderer Schicht (z. B. SM_CustomMoss in 0_boden und 5_wasserkante) -> eigene Datei,
                # damit rolle/ebene je Datei stimmen
                name = '%s_e%s' % (basisname, a['schicht'][0])
            netz_inst.setdefault(name, []).append(inst[m])
            if name not in dateien:
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': a['klasse'], 'rolle': ROLLE_JE_SCHICHT[a['schicht']], 'ebene': a['schicht'],
                                 'sichtweite': list(a['sichtweite']), 'schatten': a['schatten'], 'kollision': basisname in koll_an}
            dateien[name]['anzahl'] += int(m.sum())
            if basisname in koll_an:
                nk['2_baum' if a['schicht'] == '2_baum' else 'andere'] += int(m.sum())
        stat.setdefault(a['schicht'], {})[a['klasse']] = stat.get(a['schicht'], {}).get(a['klasse'], 0) + n
    gesamt = 0
    for name in sorted(netz_inst):
        arr = np.concatenate(netz_inst[name], axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]
    kollision_anzahl = int(sum(d['anzahl'] for d in dateien.values() if d['kollision']))
    if gesamt > deckel or kollision_anzahl > koll_max:  # nie stillschweigend
        meld('WARNUNG: %s Budget verletzt: %d Instanzen (Deckel %d), Kollision %d (Deckel %d)' % (feld, gesamt, deckel, kollision_anzahl, koll_max))
    elif gesamt > ziel_hi:
        hinweise.append('Instanzen %d ueber Ziel %d (Deckel %d eingehalten)' % (gesamt, ziel_hi, deckel))
    je_schicht = {s_: int(sum(v.values())) for s_, v in stat.items()}
    lichtung_anteil = float((licht_k & waldgebiet & im_feld).sum() / max(1, (waldgebiet & im_feld).sum())) if baum_modus == 'voll' else float((c.lichtung & im_feld).sum() / max(1, (waldgebiet & im_feld).sum()))
    hinweise = [ascii_text(h) for h in hinweise]
    for b in blickziele:
        b['regel'] = ascii_text(b['regel'])
    plan = plan_grund(feld, regeln, bio_anteil, zellen_zustaendig, kollision_anzahl, gesamt)
    plan['dateien'] = dateien
    plan['meer_zellen'] = meer_zellen
    plan['meer_gefiltert'] = int(sum(meer_gef.values()))
    plan.update({'eigenanteil_fenster': round(eigen_anteil, 4), 'eigenanteil_feld': round(eigen_anteil_feld, 4), 'saum_m': saum_m,
                 'biom_quelle': bio_quelle, 'baum_modus': baum_modus, 'mittel_modus': mittel_modus,
                 'budget': {'deckel': deckel, 'ziel': [ziel_lo, ziel_hi], 'vor_ausduennung': int(vorher), 'ausduennung': ausduenn,
                            'kollision_deckel': koll_max, 'kollision_netze_aus': sorted(koll_aus)},
                 'an_landschaftsgras': an_gras,
                 'statistik': {'je_schicht': je_schicht, 'je_klasse': stat, 'kollision_baum': nk['2_baum'], 'kollision_andere': nk['andere'],
                               'waldgebiet_anteil': round(float(waldgebiet[im_feld].mean()), 3),
                               'lichtung_anteil': round(lichtung_anteil, 3),
                               'beschattung_mittel': round(float(c.beschattung[im_feld].mean()), 3),
                               'bach_zellen': int((ist_bach & wasser_m & im_feld).sum()), 'wasser_zellen': int((wasser_m & im_feld).sum()),
                               'meer': {'zellen_fenster': meer_zellen, 'zellen_feld': int((meer & im_feld).sum()),
                                        'kuesten_saum_zellen_feld': int((kueste_nah & ~wasser_alle & (hoehe < float(MR['kueste_bis_m'])) & im_feld).sum()),
                                        'gefiltert_je_klasse': dict(sorted(meer_gef.items()))},
                               'faktor': faktor, 'schichten': sorted(schichten), 'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA},
                 'blickziele': blickziele, 'hinweise': hinweise,
                 'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet'})
    if entf_aktiv:
        plan['entfernen'] = ','.join(entf_aktiv)
    schreibe_plan(ausgabe, plan)
    meld('%s: %d Instanzen (%s), Kollision %d (Baeume %d / andere %d), %d Netze, zustaendig %d Zellen (elfenwald %.1f %% im Feld), %.1f s' % (
        feld, gesamt, ', '.join('%s %d' % (k, v) for k, v in sorted(je_schicht.items())), kollision_anzahl, nk['2_baum'], nk['andere'],
        len(dateien), zellen_zustaendig, 100 * eigen_anteil_feld, time.time() - t0))
    meld('  Meer (Runde 4): %d Zellen im Fenster, Schlussfilter verwarf %d Instanzen%s' % (
        meer_zellen, plan['meer_gefiltert'], (' (' + ', '.join('%s %d' % kv for kv in sorted(meer_gef.items())) + ')') if meer_gef else ''))
    for h in hinweise:
        meld('  Hinweis:', h)
    for b in blickziele:
        meld('  Blickziel: %s bei X %.0f Y %.0f' % (b['art'], b['x_cm'], b['y_cm']))

    if bild:
        try:
            from PIL import Image
        except Exception:
            meld('Pillow fehlt – kein Prüfbild')
            return plan
        farben = regeln.get('bild_farben', {})
        fi0, fi1, fj0, fj1 = fb[0] - wi0, fb[1] - wi0, fb[2] - wj0, fb[3] - wj0
        hh = hoehe[fi0:fi1, fj0:fj1]
        g = np.clip((hh - hh.min()) / max(1e-3, float(hh.max() - hh.min())), 0, 1) * 110 + 70
        rgb = np.stack([g, g, g], axis=2).astype(np.float32)
        b = c.beschattung[fi0:fi1, fj0:fj1]
        rgb[..., 0] *= (1 - 0.5 * b)
        rgb[..., 2] *= (1 - 0.5 * b)
        rgb[wasser_m[fi0:fi1, fj0:fj1]] = (40, 80, 200)
        rgb[meer[fi0:fi1, fj0:fj1]] = (20, 40, 120)
        rgb[weg_m[fi0:fi1, fj0:fj1]] = (120, 80, 40)
        rgb[ort_m[fi0:fi1, fj0:fj1]] = (200, 40, 40)
        for a in sorted(aus, key=lambda a: a['schicht'], reverse=True):  # Bäume zuletzt (oben)
            if a['fi'].size == 0:
                continue
            col = farben.get(a['klasse'], [255, 255, 255])
            pi = np.clip(np.round(a['fi']).astype(np.int32) - fi0, 0, fi1 - fi0 - 1)
            pj = np.clip(np.round(a['fj']).astype(np.int32) - fj0, 0, fj1 - fj0 - 1)
            rgb[pi, pj] = col
            if a['schicht'] == '2_baum' or a['klasse'] in gross:
                rgb[np.minimum(pi + 1, fi1 - fi0 - 1), pj] = col
                rgb[pi, np.minimum(pj + 1, fj1 - fj0 - 1)] = col
        for bz in blickziele:
            pi = int(round(bz['y_cm'] / 100.0 + Y0 - fb[0]))
            pj = int(round(bz['x_cm'] / 100.0 + X0 - fb[2]))
            for d in range(-6, 7):
                for (a_, b_) in ((pi + d, pj), (pi, pj + d)):
                    if 0 <= a_ < fi1 - fi0 and 0 <= b_ < fj1 - fj0:
                        rgb[a_, b_] = (255, 0, 0)
        os.makedirs(os.path.join(basis, 'docs', 'pruefung', THEMA), exist_ok=True)
        Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(os.path.join(basis, 'docs', 'pruefung', THEMA, feld + '.png'))
    return plan


def main():
    ap = argparse.ArgumentParser(description='Eldarien Elfenwald-Planer (Schichten 0 Boden, 1 Mittel, 2 Baum, 5 Wasserkante)')
    ap.add_argument('felder', nargs='+')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    ap.add_argument('--inventar', default=None, help='Pfad zu daten/netze.csv (sonst Suche)')
    ap.add_argument('--schichten', default='0,1,2,5', help='Teilmenge von 0,1,2,5')
    ap.add_argument('--baum', default='auto', choices=['auto', 'voll', 'ergaenzen'])
    ap.add_argument('--mittel', default='zusatz', choices=['zusatz', 'voll'],
                    help='Kompatibilitaet: zusatz (Standard, einziger Modus); voll verhaelt sich wie zusatz (generische Klassen nur in mittelschicht_plan.py)')
    a = ap.parse_args()
    rp = a.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'elfenwald_regeln.json')
    if not os.path.isfile(rp):
        fehler('Regeldatei fehlt: %s' % rp)
    try:
        regeln = json.load(open(rp, encoding='utf-8'))
    except Exception as e:
        fehler('Regeldatei %s unlesbar (%s)' % (rp, e))
    if not NUMBA:
        meld('numba nicht verfuegbar - reiner NumPy-Pfad (ausreichend)')
    if not os.path.isdir(os.path.join(a.basis, WELT)):
        fehler('Weltdaten fehlen: %s (mit --basis auf die production-Wurzel zeigen)' % os.path.join(a.basis, WELT))
    pruefe_inventar(regeln, a.basis, a.inventar)
    schichten = set(s.strip() for s in a.schichten.split(',') if s.strip())
    for feld in a.felder:
        plane_feld(feld.strip().upper(), a.basis, regeln, a.faktor, a.bild, schichten, a.baum, a.mittel)


if __name__ == '__main__':
    main()
