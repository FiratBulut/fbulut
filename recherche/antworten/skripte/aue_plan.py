#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien – Planer „Aue/Flussauen“ (Auftrag 11, Teil B2, Biom aue; Velen / Weißgarten / Kovir-Auen).
Eine Ebene `aue` mit vier Schichten: `0 boden` (Laub, Zweige, Kiesel, Bodendecker), `1 mittel` nur Aue-Sonderformen
(Blumeninseln der Auenwiese, Wegsaum-Hecken), `2 baum` (Weiden/Pappeln am Wasser, Hainbuchen-/Buchen-Haine auf der Terrasse,
Kiefern-Gruppen, Solitäre, Totbäume), `5 wasserkante` (Schilfgürtel, Seggen, Uferstauden-Saum, Uferwurzeln).
Höhenstufen Ufer → Aue → Terrasse aus Abstand und relativer Höhe zum nächsten Wasser.

Korrektur Runde 1 (antworten/verteilung-KONVENTIONEN.md, verbindlich):
  §1 Zuständigkeit: Biom je Zelle aus eigner.r8 + welt.json (Kennzahl 0 = Weltgelände → aue, Vulkan/Lava → lava; Fallback
     dominantes Feldbiom aus daten/biome_je_feld.json nur, wenn eigner.r8 oder welt.json fehlt). biome_eigen = [aue].
     Bebaut werden nur aue-Zellen plus ein 30-m-Saum (Dichtefaktor linear 1 → 0, Jump-Flooding-Distanzfeld). Eigenanteil im
     Fenster < 2 % → leerer plan.json (instanzen 0, keine f32). Keine Biomfaktoren für fremde Biome.
  §2 plan.json zusätzlich: biome_fenster, zellen_zustaendig, biome_eigen, kollision_anzahl (auch im Leerplan).
  §3 Budget hart: ≤ 60 000 Instanzen je Feld, ≤ 3 000 mit Kollision; Ziel 45 000–52 000; Ausdünnung deterministisch nach
     Priorität mit WARNUNG im Log; Kleinzeug-Hinweis Landschafts-Gras (plan.json an_landschaftsgras).
  §4 Ebenen: generische Mittelschicht-Klassen (strauch, jungbaum, farn, totholz_*, hochstaude, grasbueschel, beere, pilz) setzt
     nur mittelschicht_plan.py; ihre Aue-Paletten/Dichten stehen in aue_regeln.json["mittelschicht_overrides"]. Felsen > 0,8 m
     nur über felsgruppen_overrides (Teil C), Spuren (Kopfweiden-Reihen, Feldrand-Hecken, Zäune) nur über spuren_overrides.
  §5 print() nur ASCII; fehlende Pflichtdatei (hoehe.f32, Regeldatei, netze.csv, Weltordner) → Meldung, Exit-Code 2.
  Wüstenfelder C3 C4 D3 D4 D5 E3 E4 E5: nur ergänzen (Faktor 0,6, Sand/Sandstein ≥ 0,5 gesperrt), nie `entfernen`.

Aufruf (lokal, production-Wurzel):
    python -I scripts/aue/aue_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD] [--inventar PFAD]

Liest:   export/unreal/welt/hoehe.f32 (memmap, nur Fenster Feld + 64 m), lage_*.r8 (optional), karte_wasser/weg/ort.r8,
         eigner.r8 + welt.json (Biom je Zelle), wasser_welt.json / teiche/teiche.json (Stillwasser-Umrisse, optional),
         bestand/<Feld>/, witcher/<Feld>/ (+ Nachbarn), ufer/foliage_<Feld>/, instanzen/instanzen.json (optional),
         docs/staedte/standorte.json (optional), daten/netze.csv (Pflicht; auch neben dem Skript), daten/biome_je_feld.json (Fallback).
Schreibt: export/unreal/welt/aue/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm, qx,qy,qz,qw, sx,sy,sz) + plan.json
          (FORMAT.md §3, je Datei zusätzlich `ebene`), bei --bild docs/pruefung/aue/<Feld>.png (1 px = 1 m).
Regeln:  scripts/aue/aue_regeln.json (neben dem Skript) oder --regeln PFAD.

Nur NumPy-Vektoroperationen (Box-Faltungen, Dilatation, Jump-Flooding-Distanzfeld mit Höhe des nächsten Wassers,
Hash-Zufall aus globaler Rasterkoordinate → deterministisch und nahtlos zu Nachbarfeldern). numba optional, nicht nötig.
Laufzeit-Ziel ≤ 60 s je Feld (Cloud-Rauchtest synthetisch: siehe verteilung-aue.md, Abschnitt Korrektur Runde 1).

Quellen: FORMAT.md §1–§5; verteilung-KONVENTIONEN.md; antworten/assets-taxonomie.md (Paletten aue);
antworten/bildkritik-witcher-messlatte.md (W6FIN_E5, BACH3_G5: Weiden 20–40 m vom Wasser, Clumping 40–100 m);
antworten/ufer-kies-coast-dunes.md (Kiesbänke/Treibholz = Ufer-Ebene); GDC 2014 „Landscape Creation and Rendering in
REDengine 3“; 80.lv „World building of Witcher 3“; CDPR State of Unreal 2025 (Nanite Foliage). Web-Quellen nur als Suchauszüge.

UNGETESTET MIT ECHTDATEN – in der Cloud nur mit synthetischen Rastern (E5, H5, C6) rauchgetestet.
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
GEN_VORGABE = ('strauch', 'jungbaum', 'farn', 'totholz_liegend', 'totholz_stumpf', 'totholz_ast', 'hochstaude', 'grasbueschel',
               'beere', 'pilz')  # Konventionen par. 4: nur mittelschicht_plan.py
GEN = set(GEN_VORGABE)
GEN_ALIAS = {'stamm_liegend': 'totholz_liegend', 'totholz': 'totholz_liegend', 'totholz_klein': 'totholz_liegend',
             'totholz_gross': 'totholz_liegend', 'stumpf': 'totholz_stumpf', 'ast': 'totholz_ast'}


# ----------------------------------------------------------------------------- Helfer
_ASCII = (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('Ä', 'Ae'), ('Ö', 'Oe'), ('Ü', 'Ue'), ('ß', 'ss'),
          ('→', '->'), ('←', '<-'), ('≤', '<='), ('≥', '>='), ('…', '...'), ('×', 'x'),
          ('–', '-'), ('—', '-'), ('°', ' Grad'), ('²', '2'), ('³', '3'), ('„', '"'),
          ('“', '"'), ('”', '"'), ('‚', "'"), ('‘', "'"), ('’', "'"), ('·', '*'),
          ('±', '+-'), ('≈', '~'), (' ', ' '))


def ascii_text(s):
    """Text fuer Logs und hinweise (cp1252-Weiterverarbeitung): Umlaute -> ae/oe/ue/ss, Sonderzeichen -> ASCII, Rest -> '?'."""
    s = str(s)
    for a, b in _ASCII:
        s = s.replace(a, b)
    return s.encode('ascii', 'replace').decode('ascii')


def meld(*a):
    print(ascii_text(' '.join(['[aue]'] + [str(x) for x in a])), flush=True)


def fehler(text):
    """Klare Meldung (ASCII, stderr) und Exit-Code 2 (fehlende Pflichtdatei, falscher Aufruf)."""
    sys.stderr.write(ascii_text('[aue] FEHLER: %s' % text) + '\n')
    sys.stderr.flush()
    sys.exit(2)


def ausgabe_leeren(basis, regeln, feld):
    """Ausgabeordner anlegen und alte f32 loeschen (auch beim Leerplan)."""
    ausgabe = os.path.join(basis, regeln['ausgabe']['ordner'], feld)
    os.makedirs(ausgabe, exist_ok=True)
    for f in sorted(os.listdir(ausgabe)):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    return ausgabe


def plan_grund(feld, regeln, anteile, zellen, kollision_anzahl, instanzen):
    """Pflichtschluessel nach FORMAT par. 3 und Konventionen par. 2 (auch im Leerplan)."""
    return {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': int(instanzen), 'dateien': {}, 'entfernen': '',
            'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'biome_fenster': {k: round(v, 4) for k, v in sorted(anteile.items(), key=lambda kv: (-kv[1], kv[0]))},
            'zellen_zustaendig': int(zellen), 'biome_eigen': list(regeln['zustaendigkeit']['biome_eigen']),
            'kollision_anzahl': int(kollision_anzahl)}


def schreibe_plan(ausgabe, plan):
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)


def feld_fenster(feld, rand):
    """'E5' → ((i0,i1,j0,j1) Feld, (wi0,wi1,wj0,wj1) Fenster), beides auf das Raster geklippt (J-Spalte endet bei NX)."""
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
    """Fenster eines NY×NX-Rasters per memmap (nur das Fenster wird gelesen)."""
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
def finde_inventar(basis, inventar_pfad):
    skript = os.path.dirname(os.path.abspath(__file__))
    kand = ([inventar_pfad] if inventar_pfad else []) + [
        os.path.join(basis, 'daten', 'netze.csv'), os.path.join(skript, 'netze.csv'),
        os.path.join(skript, '..', '..', 'daten', 'netze.csv'), os.path.join(skript, '..', '..', 'vorlagen', 'daten', 'netze.csv')]
    return next((k for k in kand if k and os.path.isfile(k)), None)


def override_pfade(o):
    """Alle Unreal-Pfade (Strings mit /Game/) in einem Override-Block."""
    if isinstance(o, dict):
        return [p for v in o.values() for p in override_pfade(v)]
    if isinstance(o, list):
        return [p for v in o for p in override_pfade(v)]
    return [o] if isinstance(o, str) and o.startswith('/Game/') else []


def pruefe_netze(basis, regeln, inventar_pfad=None):
    """Alle Netzpfade (Schichten + Override-Paletten) gegen daten/netze.csv pruefen (Pflichtdatei, sonst Exit 2);
    fehlende aus den Paletten streichen (mit Meldung). Rueckgabe: Pfad der netze.csv."""
    cp = finde_inventar(basis, inventar_pfad)
    if cp is None:
        fehler('Inventar daten/netze.csv nicht gefunden (Pflichtdatei; --inventar PFAD oder neben das Skript legen)')
    inv = set()
    try:
        with open(cp, encoding='utf-8', newline='') as f:
            for r in csv.DictReader(f, delimiter=';'):
                inv.add(r.get('pfad', ''))
    except Exception as e:
        fehler('Inventar %s unlesbar (%s)' % (cp, e))
    fehlt = []
    for sname, schicht in regeln['schichten'].items():
        for kname, kl in schicht.items():
            for p in kl['netze']:
                if p not in inv:
                    fehlt.append('%s/%s: %s' % (sname, kname, p))
            kl['netze'] = [p for p in kl['netze'] if p in inv]
    n_ov = 0
    for blk in ('mittelschicht_overrides', 'felsgruppen_overrides', 'spuren_overrides'):
        pf = override_pfade(regeln.get(blk, {}))
        n_ov += len(pf)
        fehlt += ['%s: %s' % (blk, p) for p in pf if p not in inv]
    pal = regeln.get('mittelschicht_overrides', {}).get('palette', {})
    for k in pal:
        pal[k] = [p for p in pal[k] if p in inv]
    if fehlt:
        meld('WARNUNG: %d Netzpfade nicht im Inventar, gestrichen:' % len(fehlt))
        for f in fehlt:
            meld('   ', f)
    meld('Inventar %s: %d Netze; Paletten geprueft (%d Override-Pfade), %d fehlen' % (cp, len(inv), n_ov, len(fehlt)))
    return cp


def dominantes_feldbiom(basis, feld, regeln):
    """Fallback (nur wenn eigner.r8/welt.json fehlen oder ein Rezept unbekannt ist): dominantes Biom des Feldes aus
    daten/biome_je_feld.json, sonst Tabelle feld_biom_fallback, sonst aue."""
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


def lade_biome(basis, win, regeln, feld, land=None):
    """Biom je Zelle (Konventionen par. 1): eigner.r8 + welt.json["kacheln"][k]["rezept"], Kennzahl 0 = Weltgelaende -> aue,
    Vulkan/Lava -> lava, unbekanntes Rezept -> dominantes Feldbiom (Warnung). Nur wenn eigner.r8 oder welt.json fehlt:
    dominantes Feldbiom fuer alle Zellen. Rueckgabe: eigen (bool H x W, Biom in biome_eigen), Anteile {biom: Anteil im Fenster,
    bezogen auf die Landzellen `land` (ohne karte_wasser), sonst alle Zellen}, Quelle (Text). Keine Biomfaktoren fuer fremde Biome."""
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
    namen = [None] * 256
    unbekannt = []

    def biom_aus_rezept(rz):
        rz = str(rz).strip().lower()
        if rz in alle:
            return rz
        if 'vulkan' in rz or 'lava' in rz:
            return 'lava'
        for n in sorted(alle, key=len, reverse=True):
            if n in rz:
                return n
        unbekannt.append(rz)
        return None
    eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
    for k, v in eintraege:
        try:
            kk = int(v.get('kennzahl', v.get('id', k))) if isinstance(v, dict) else int(k)
        except Exception:
            continue
        if 0 < kk < 256:
            namen[kk] = biom_aus_rezept(v.get('rezept', '') if isinstance(v, dict) else v)
    namen[0] = null_biom  # Kennzahl 0 = Weltgelaende -> aue (Konventionen par. 1)
    zahl = np.bincount(eig.ravel() if land is None else eig[land], minlength=256)
    fehlt = [kk for kk in np.flatnonzero(zahl) if namen[kk] is None]
    if fehlt:
        fb, q = dominantes_feldbiom(basis, feld, regeln)
        meld('WARNUNG: %d Zellen mit Kennzahl ohne Biom-Zuordnung (%s; Rezepte %s) -> dominantes Feldbiom %s (%s)' % (
            int(sum(zahl[kk] for kk in fehlt)), ','.join(str(int(x)) for x in fehlt[:8]), ', '.join(sorted(set(unbekannt))[:4]) or '-', fb, q))
        for kk in fehlt:
            namen[kk] = fb
    lut = np.array([(n in eigen_l) for n in namen], bool)
    eigen = lut[eig]
    anteile = {}
    for kk in np.flatnonzero(zahl):
        anteile[namen[kk]] = anteile.get(namen[kk], 0.0) + float(zahl[kk]) / max(1, int(zahl.sum()))
    return eigen, anteile, 'eigner.r8 + welt.json'


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
    im_fenster = 0
    for um in umrisse:  # nur Umrisse zaehlen, die das Fenster beruehren
        try:
            pts = np.asarray(um, dtype=np.float64)
            px, py = pts[:, 0] / 100.0 + X0 - win[2], pts[:, 1] / 100.0 + Y0 - win[0]
            im_fenster += int(not (px.max() < 0 or px.min() > W or py.max() < 0 or py.min() > H))
        except Exception:
            continue
    return polygon_maske(H, W, win, umrisse), im_fenster


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
        meld('Feld %s liegt ausserhalb des Rasters' % feld)
        return None
    hinweise = []
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True)
    ii, jj = np.indices((H, W), dtype=np.int32)
    gi, gj = ii + wi0, jj + wj0
    im_feld = (gi >= fb[0]) & (gi < fb[1]) & (gj >= fb[2]) & (gj < fb[3])

    # ------------------------------------------------------------------ Zustaendigkeit (Konventionen par. 1)
    # Anteile und Saum nur ueber Landzellen: Kennzahl 0 (Weltgelaende -> aue) deckt auch Meer/Seen; sonst wuerde Wasser den
    # aue-Anteil in Kuestenfeldern (A5) aufblaehen und der Saum von Meereszellen in fremde Biome reichen.
    Z = regeln['zustaendigkeit']
    w0 = lade_raster(os.path.join(basis, WELT, 'karte_wasser.r8'), np.uint8, win)
    land_z = (w0 == 0) if w0 is not None else np.ones((H, W), bool)
    if not land_z.any():
        land_z = np.ones((H, W), bool)
    eigen, bio_anteil, bio_quelle = lade_biome(basis, win, regeln, feld, land_z)
    eigen &= land_z
    eigen_anteil = float(eigen[land_z].mean())
    eigen_anteil_feld = float(eigen[im_feld & land_z].mean()) if (im_feld & land_z).any() else 0.0
    if eigen_anteil < float(Z['min_eigenanteil_fenster']):
        ausgabe = ausgabe_leeren(basis, regeln, feld)
        plan = plan_grund(feld, regeln, bio_anteil, 0, 0, 0)
        plan.update({'leer': True, 'eigenanteil_fenster': round(eigen_anteil, 4), 'eigenanteil_feld': round(eigen_anteil_feld, 4),
                     'biome_fenster_bezug': 'Landzellen im Fenster (ohne karte_wasser)', 'biom_quelle': bio_quelle,
                     'hinweise': ['aue-Anteil im Fenster %.2f %% < %.0f %% - kein Plan (Konventionen par. 1)' % (
                         100 * eigen_anteil, 100 * float(Z['min_eigenanteil_fenster']))]})
        schreibe_plan(ausgabe, plan)
        meld('%s: aue-Anteil im Fenster %.2f %% < %.0f %% - leerer plan.json (instanzen 0)' % (
            feld, 100 * eigen_anteil, 100 * float(Z['min_eigenanteil_fenster'])))
        return plan
    saum_m = float(Z['saum_m'])
    if eigen.all():
        zust = np.ones((H, W), np.float32)
    else:
        d_eigen, _, _ = distanz_feld(eigen, max_m=max(32.0, saum_m + 2))
        zust = np.where(eigen, 1.0, np.clip(1.0 - d_eigen / saum_m, 0, 1)).astype(np.float32)

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

    # Wuestenfelder: nur ergaenzen (Faktor, Sand/Sandstein gesperrt; entfernen bleibt leer)
    feld_faktor = faktor
    wuestenfeld = feld in regeln['wuesten_felder']
    if wuestenfeld:
        feld_faktor *= regeln['wuesten_feld_faktor']
        WS = regeln['wuesten_lagen_sperre']
        for ln in WS['lagen']:
            if ln in lagen:
                zust = np.where(lagen[ln] < WS['ab_deckung'], zust, 0).astype(np.float32)
        hinweise.append('Wuestenfeld: nur ergaenzen - Faktor %.2f, Sand/Sandstein >= %.1f gesperrt, kein entfernen'
                        % (regeln['wuesten_feld_faktor'], WS['ab_deckung']))
    zellen_zustaendig = int(((zust > 0) & im_feld & ~wasser_m).sum())

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
            if kname in GEN or GEN_ALIAS.get(kname) in GEN:
                hinweise.append('Klasse %s/%s uebersprungen: generische Mittelschicht-Klasse (Konventionen par. 4, setzt mittelschicht_plan.py ueber mittelschicht_overrides)' % (sname, kname))
                continue
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
            lam *= f_hoehe * feld_faktor * zust  # Zustaendigkeit: aue-Zelle 1, Saum linear -> 0, sonst 0
            if ist_baum:
                lam = np.where(hang > regeln['hang']['baum_max_grad'], 0, lam)
            if kl.get('nur_band') == 'hecke_weg':
                lam = np.where(hecke_band, lam, 0)
            if kl.get('lichtung'):
                lam = np.where(lichtung_gate, lam, 0)
            frei = (zust > 0) & ~belegt & ~nah_ort & ~standort_m & ~ufer_belegt
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

    # ------------------------------------------------------------------ Budget (Konventionen par. 3, hart)
    Bg = regeln['budget']
    deckel = int(Bg['deckel_je_feld'])
    ziel_lo, ziel_hi = [int(v) for v in Bg['ziel_je_feld']]
    auf = min(deckel, int(Bg.get('ausduennen_auf', ziel_hi)))
    koll_max = int(Bg['kollision_je_feld'])
    max_aus = float(Bg.get('max_ausduennung_je_klasse', 0.6))
    schicht_von = {a['klasse']: a['schicht'] for a in aus}
    koll_klassen = sorted(set(a['klasse'] for a in aus if a['kollision']), key=lambda k: kidx_all[k])

    def anzahl(klassen=None):
        n = 0
        for a in aus:
            if klassen is None or a['klasse'] in klassen:
                n += int(a['fi'].size)
        return n

    def je_klasse():
        st = {}
        for a in aus:
            st[a['klasse']] = st.get(a['klasse'], 0) + int(a['fi'].size)
        return st

    def duenne(kname, f, stufe):
        """Deterministische Hash-Ausduennung einer Klasse auf Anteil f (eigener Kanal je Klasse und Stufe)."""
        if f >= 1.0:
            return
        for a in aus:
            if a['klasse'] != kname or a['fi'].size == 0:
                continue
            hv = hash01(np.round(a['fi'] * 7).astype(np.int64) + 7 * wi0, np.round(a['fj'] * 7).astype(np.int64) + 7 * wj0,
                        seed, 99991 + stufe * 7919 + kidx_all[kname])
            keep = hv < f
            for key in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw'):
                a[key] = a[key][keep]

    def duenne_bis(ziel, prio, gleich, stufe0):
        """Erst Klassen in Prioritaet (je hoechstens max_aus), dann alle Klassen aus `gleich` gleichmaessig. True = ausgeduennt."""
        alle = set(prio) | set(gleich)
        if anzahl(alle) <= ziel:
            return False
        ueber = anzahl(alle) - ziel
        for k in prio:
            if ueber <= 0:
                break
            n = anzahl([k])
            if n == 0:
                continue
            duenne(k, 1.0 - min(float(ueber), n * max_aus) / n, stufe0)
            ueber -= n - anzahl([k])
        st = stufe0 + 1
        while anzahl(alle) > ziel and st < stufe0 + 8 and gleich:
            n_g = anzahl(gleich)
            f = max(0.0, 1.0 - 1.02 * (anzahl(alle) - ziel) / max(1, n_g))
            for k in gleich:
                duenne(k, f, st)
            st += 1
        return True

    st0 = je_klasse()
    vorher = sum(st0.values())
    koll_vorher = anzahl(koll_klassen)
    prio_alle = [k for k in Bg['prioritaet_ausduennen'] if k in st0] + sorted(k for k in st0 if k not in Bg['prioritaet_ausduennen'])
    warnungen = []
    # 1) Kollision <= kollision_je_feld
    if koll_vorher > koll_max:
        kp = [k for k in Bg.get('kollision_prioritaet_ausduennen', []) if k in koll_klassen]
        kp += [k for k in koll_klassen if k not in kp]
        duenne_bis(koll_max, kp, koll_klassen, 10)
        warnungen.append('Kollision %d > %d -> %d (Klassen %s)' % (koll_vorher, koll_max, anzahl(koll_klassen), ','.join(kp)))
    # 2) weiche Schichtziele
    for sname, z in sorted(Bg.get('ziel_je_schicht', {}).items()):
        ks = [k for k in prio_alle if schicht_von.get(k) == sname]
        n_s = anzahl(ks)
        if ks and n_s > int(z):
            duenne_bis(int(z), ks, ks, 20 + 10 * (sorted(Bg['ziel_je_schicht']).index(sname)))
            warnungen.append('Schicht %s %d > Ziel %d -> %d' % (SCHICHT_KURZ.get(sname, sname), n_s, int(z), anzahl(ks)))
    # 3) Feldziel ausduennen_auf (zuerst Kleinzeug), dann gleichmaessig ohne Baeume, harte Sicherung Deckel
    n_vor3 = anzahl()
    if n_vor3 > auf:
        nicht_baum = [k for k in prio_alle if schicht_von.get(k) != '2 baum']
        duenne_bis(auf, prio_alle, nicht_baum, 80)
        warnungen.append('Feld %d > %d (Ziel %d-%d) -> %d' % (n_vor3, auf, ziel_lo, ziel_hi, anzahl()))
    if anzahl() > deckel:  # darf nach den Stufen nicht vorkommen - harte Sicherung
        n_h = anzahl()
        for k in list(st0):
            duenne(k, deckel / float(n_h) * 0.99, 95)
        warnungen.append('harte Deckel-Sicherung %d -> %d' % (n_h, anzahl()))
    st1 = je_klasse()
    ausduenn = {k: round(st1.get(k, 0) / float(n), 3) for k, n in st0.items() if n and st1.get(k, 0) < n}
    if warnungen:
        meld('WARNUNG: %s Budget: %s; Faktoren %s' % (feld, '; '.join(warnungen),
                                                       ', '.join('%s x%.2f' % kv for kv in sorted(ausduenn.items()))))
        hinweise.append('Budget (Konventionen par. 3): %s; deterministisch ausgeduennt: %s' % (
            '; '.join(warnungen), ', '.join('%s x%.2f' % kv for kv in sorted(ausduenn.items()))))
    LG = regeln.get('landschaftsgras', {}).get('klassen', {})
    an_gras = {k: {'grasart': gt, 'behalten_anteil': ausduenn.get(k, 1.0)} for k, gt in sorted(LG.items())}
    abgabe = ['%s %d %%' % (k, round(100 * (1 - v['behalten_anteil']))) for k, v in an_gras.items() if v['behalten_anteil'] < 1.0]
    hinweise.append('Kleinzeug an Landschafts-Gras: Laub/Zweige/Bodendecker -> GT_Kraut, Kiesel -> GT_Steinchen%s' % (
        ('; wegen Budget abgegeben: ' + ', '.join(abgabe)) if abgabe else ' (kein Budgetdruck, nichts abgegeben)'))

    # ------------------------------------------------------------------ Instanzen schreiben
    ausgabe = ausgabe_leeren(basis, regeln, feld)
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
    for name in sorted(netz_inst):
        arr = np.concatenate(netz_inst[name], axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]
    kollision_anzahl = int(sum(d['anzahl'] for d in dateien.values() if d['kollision']))
    if gesamt > deckel or kollision_anzahl > koll_max:  # nie stillschweigend
        meld('WARNUNG: %s Budget verletzt: %d Instanzen (Deckel %d), Kollision %d (Deckel %d)' % (feld, gesamt, deckel, kollision_anzahl, koll_max))
    # entfernen: nie in Wuestenfeldern (nur ergaenzen), sonst nur, wenn aue im Feld ueberwiegt
    entf = str(regeln.get('entfernen', '') or '')
    if entf and (wuestenfeld or eigen_anteil_feld < float(Z.get('entfernen_min_eigenanteil_feld', 0.5))):
        hinweise.append('entfernen %r nicht gesetzt (%s)' % (entf, 'Wuestenfeld: nur ergaenzen' if wuestenfeld else 'aue-Anteil im Feld < 50 %'))
        entf = ''
    land = im_feld & ~wasser_m
    plan = plan_grund(feld, regeln, bio_anteil, zellen_zustaendig, kollision_anzahl, gesamt)
    plan['dateien'] = dateien
    plan['entfernen'] = entf
    plan.update({'eigenanteil_fenster': round(eigen_anteil, 4), 'eigenanteil_feld': round(eigen_anteil_feld, 4), 'saum_m': saum_m,
                 'biome_fenster_bezug': 'Landzellen im Fenster (ohne karte_wasser)', 'biom_quelle': bio_quelle,
                 'budget': {'deckel': deckel, 'ziel': [ziel_lo, ziel_hi], 'ausduennen_auf': auf, 'vor_ausduennung': int(vorher),
                            'kollision_vor_ausduennung': int(koll_vorher), 'kollision_deckel': koll_max, 'ausduennung': ausduenn},
                 'an_landschaftsgras': an_gras,
                 'statistik': {'je_klasse': stat, 'je_schicht': stat_s, 'kollision': int(nk),
                               'saum_zellen_feld': int(((zust > 0) & (zust < 1) & im_feld & ~wasser_m).sum()),
                               'hoehenstufen_anteil': {'ufer': round(float(ufer[land].mean()), 3) if land.any() else 0,
                                                       'aue': round(float(aue[land].mean()), 3) if land.any() else 0,
                                                       'terrasse': round(float(terrasse[land].mean()), 3) if land.any() else 0},
                               'wasser_anteil': round(float(wasser_m[im_feld].mean()), 3),
                               'beschattung_mittel': round(float(beschattung[im_feld].mean()), 3),
                               'faktor': faktor, 'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA},
                 'hinweise': [ascii_text(h) for h in hinweise],
                 'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet (E5, H5, C6)'})
    schreibe_plan(ausgabe, plan)
    meld('%s: %d Instanzen (%d mit Kollision), %d Netze, %s, zustaendig %d Zellen (aue %.1f %% im Feld, %.1f %% im Fenster), %.1f s' % (
        feld, gesamt, kollision_anzahl, len(dateien), ', '.join('%s %d' % (SCHICHT_KURZ.get(k, k), v) for k, v in sorted(stat_s.items())),
        zellen_zustaendig, 100 * eigen_anteil_feld, 100 * eigen_anteil, time.time() - t0))
    for h in hinweise:
        meld('  Hinweis:', h)

    if bild:
        try:
            from PIL import Image
        except Exception:
            meld('Pillow fehlt - kein Pruefbild')
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
        rgb[zust[fi0:fi1, fj0:fj1] <= 0] *= 0.6
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
        meld('Pruefbild: %s' % os.path.join(od, feld + '.png'))
    return plan


NETZ_HOEHE = {}


def lade_netzhoehen(cp):
    """Netzhoehe (m) aus daten/netze.csv fuer das anteilige Eingraben liegender Staemme."""
    if not cp or not os.path.isfile(cp):
        return
    with open(cp, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f, delimiter=';'):
            try:
                NETZ_HOEHE[r['pfad']] = float(r['groesse_z_m'])
            except Exception:
                pass


def main():
    ap = argparse.ArgumentParser(description='Eldarien Aue-Planer (Boden, Aue-Sonderformen, Auwald, Wasserkante)')
    ap.add_argument('felder', nargs='+')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    ap.add_argument('--inventar', default=None, help='Pfad zu daten/netze.csv (sonst Suche: basis/daten, neben dem Skript, vorlagen/daten)')
    a = ap.parse_args()
    rp = a.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aue_regeln.json')
    if not os.path.isfile(rp):
        fehler('Regeldatei fehlt: %s' % rp)
    try:
        regeln = json.load(open(rp, encoding='utf-8'))
    except Exception as e:
        fehler('Regeldatei %s unlesbar (%s)' % (rp, e))
    if 'zustaendigkeit' not in regeln or 'budget' not in regeln:
        fehler('Regeldatei %s ohne Block zustaendigkeit/budget (Fassung vor Korrektur Runde 1?)' % rp)
    E = regeln.get('ebenen', {})
    GEN.update(E.get('generisch_mittelschicht', []))
    GEN_ALIAS.update(E.get('alias', {}))
    if not NUMBA:
        meld('numba nicht verfuegbar - reiner NumPy-Pfad (ausreichend)')
    if not os.path.isdir(os.path.join(a.basis, WELT)):
        fehler('Weltdaten fehlen: %s (Aufruf aus der production-Wurzel oder --basis PFAD)' % os.path.join(a.basis, WELT))
    inv_pfad = pruefe_netze(a.basis, regeln, a.inventar)
    lade_netzhoehen(inv_pfad)
    for feld in a.felder:
        plane_feld(feld.strip().upper(), a.basis, regeln, a.faktor, a.bild)


if __name__ == '__main__':
    main()
