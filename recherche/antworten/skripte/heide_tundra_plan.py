#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eldarien – Planer „Heide/Tundra“ (Auftrag 11, Teil B3, Korrektur Runde 1): Ebene `heide_tundra` für die Biome heide und tundra
(Felder D2, C2, C3, D3, E3, E2; F4, G4, F5, G5). Schichten:
  0 boden        Kiesel, Flechtensteine (< 0,8 m), Torf-/Streumatten
  1 mittel       NUR Heide/Tundra-Sonderformen: Heidekraut-Flecken (Zwergstrauch-Polster in Rausch-Flecken), Wacholder-Gruppen,
                 windschiefe Krüppelkiefern, Wollgras-Büschel am Moor
  2 baum         Einzelkiefern (windschief auf Kuppen, Gruppen 2–5 in Mulden), Moorbirken am Moorrand, Totbäume – Baumgrenze nach Höhe
  5 wasserkante  Seggen/Binsen, Moorsteine, Treibholz an Moortümpeln
  Generische Mittelschicht-Klassen (strauch, jungbaum, farn, totholz_liegend/_stumpf/_ast, hochstaude, grasbueschel, beere, pilz) setzt
  ausschließlich mittelschicht_plan.py (Teil D) – Palette/Faktoren dafür stehen in heide_tundra_regeln.json["mittelschicht_overrides"].
  Felsen > 0,8 m / Spuren kommen aus felsgruppen_plan.py / spuren_plan.py (`felsgruppen_overrides` / `spuren_overrides`).

Zuständigkeit (Konventionen §1): Biom je Zelle aus eigner.r8 + welt.json["kacheln"][k]["rezept"]; Kennzahl 0 und Kennzahlen ohne
erkennbares Biom → aue, Rezept mit vulkan/lava → lava. Nur wenn eigner.r8 oder welt.json fehlen, gilt das dominante Feldbiom aus
daten/biome_je_feld.json (Hinweis im Log). biome_eigen = [heide, tundra]: bebaut werden nur eigene Zellen plus ein 30-m-Saum mit linear
fallender Dichte (Jump-Flooding-Distanz); im Saum gilt das Profil der nächsten eigenen Zelle. Eigenanteil im Fenster < 2 % → leerer
plan.json (instanzen 0, keine f32). Wüstenfelder (C3 C4 D3 D4 D5 E3 E4 E5): nur ergänzen, Faktor 0,7, kein Saum, Sand-Sperre, kein entfernen.
Korrektur Runde 4 (Konventionen §1b): karte_wasser ist nur Suesswasser. Meer = hoehe < 0 und karte_wasser == 0 (eigner 0 = aue);
wasser_alle = Suesswasser | Meer fuer Biom-Anteil/Leerplan-Schwelle und Saum (Landzellen-Bezug), zellen_zustaendig, Sperre und
Abstand (wasser_min, Ufer-Kieselmaske). Suesswasser-spezifisch bleiben Wasserkante-Band (Moortuempel), wasser_bonus (Moorbirke).
Unter -0,3 m nichts, -0,3 .. 0 m nur Klassen mit meer_rolle (heide_tundra hat keine), 0 .. +0,3 m im Kuestensaum (<= 30 m zum
Meer) nur Schicht 5 wasserkante / strand. Schlussfilter mit der Gelaendehoehe bilinear am Instanzort; plan.json meldet
meer_zellen und meer_gefiltert.

Aufruf (lokal, production-Wurzel):
    python -I scripts/heide_tundra/heide_tundra_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
                                                        [--entfernen "praefix1,praefix2"]

Liest:   export/unreal/welt/hoehe.f32 (Pflicht; np.memmap, nur Fenster Feld + 64 m; NY=7057 × NX=9577, J-Spalte bei NX geklippt),
         lage_*.r8 (optional, alle 22 Namen aus FORMAT §2), karte_wasser/weg/ort.r8 (optional, Warnung),
         eigner.r8 + welt.json (Biom je Zelle, s. o.), bestand/<Feld>/, witcher/<Feld>/, mittelschicht/, felsgruppen/ (Feld + 8
         Nachbarn: Kronendach, Stamm-/Objektabstand), ufer/foliage_<Feld>/ (vorhanden → Klasse moorstein entfällt),
         instanzen/instanzen.json (Houdini-Bestand, optional, Meldung wenn fehlt), daten/netze.csv (Pfadprüfung, Netzhöhen, 0,8-m-Grenze).
Schreibt: export/unreal/welt/heide_tundra/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm, qx,qy,qz,qw, sx,sy,sz) + plan.json
         (FORMAT §3: stand, feld, instanzen, dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene},
         entfernen, ft_ordner, ft_praefix; Konventionen §2: biome_fenster, zellen_zustaendig, biome_eigen, kollision_anzahl;
         zusätzlich ebene, klassen, schichten, profil_anteil_feld, statistik, hinweise),
         bei --bild docs/pruefung/heide_tundra/<Feld>.png (Draufsicht 1 px = 1 m).
Budget (Konventionen §3, hart): Ziel 48 000, Deckel 60 000 Instanzen und 3 000 mit Kollision je Feld; Überschuss wird nach
`budget.prioritaet` per Hash ausgedünnt und danach exakt gekappt, jede Ausdünnung als WARNUNG in Log und plan.json["hinweise"].
Logs nur ASCII (§5); fehlende Pflichtdatei (hoehe.f32, Regeldatei) oder unbekanntes Feld → FEHLER-Zeile, Exit-Code 2.

Nur NumPy-Vektoroperationen (Box-/Gauß-Faltung über Summenbilder, Jump-Flooding-Distanz, Hash-Zufall aus absoluter
Rasterkoordinate → deterministisch und nahtlos zu Nachbarfeldern). numba optional (nur Meldung), Pillow optional (sonst PPM).
Ziel ≤ 60 s je Feld.

Quellen: vorlagen/FORMAT.md §1–§5; antworten/verteilung-KONVENTIONEN.md §1–§5; antworten/assets-taxonomie.md (Paletten/Lücken heide,
tundra); antworten/bildkritik-witcher-messlatte.md; antworten/verteilung-heide-tundra.md (Witcher-Analyse, Korrektur Runde 1).
Korrektur Runde 2: Kiesel mit `teppich_sperre` nur auf/um Kies-/Geroell-/Fels-Lagen, am Weg und am Ufer (kein Hangteppich).

UNGETESTET MIT ECHTDATEN – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern (D2, G5, E1, F4) rauchgetestet.
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
               'hainbuche', 'hornbeam', 'poplar', 'willow', 'beech', 'pine', 'fir', 'tanne', 'birch')
NICHT_BAUM = ('tot', 'dead', 'stump', 'log', 'plant', 'sapling', 'seedling', 'leaves', 'branch', 'root')
LAGEN_NAMEN = ['Wiese', 'Gras', 'Trockengras', 'Laub', 'Nadeln', 'Moos', 'Heide', 'Kraut', 'Erde', 'Lehm', 'Schlamm', 'Sand', 'Kies',
               'Geroell', 'Fels', 'Felsplatte', 'Sandstein', 'Schnee', 'Eis', 'Lavafels', 'Lavasand', 'Algen']
BIOME15 = ('aue', 'bergwald', 'gletscher', 'tundra', 'canyon', 'oedland', 'heide', 'elfenwald', 'dschungel', 'kueste', 'wueste',
           'lava', 'frost', 'sumpf', 'fjord')
SCHICHT_KURZ = {'0 boden': 'boden', '1 mittel': 'mittel', '2 baum': 'baum', '5 wasserkante': 'wasserkante'}
# Konventionen §4: diese Klassen setzt nur mittelschicht_plan.py (Teil D); der Planer verweigert sie in Schicht 1
GENERISCHE_MITTEL = ('strauch', 'jungbaum', 'farn', 'totholz_liegend', 'totholz_stumpf', 'totholz_ast', 'hochstaude', 'grasbueschel',
                     'beere', 'pilz')
ASCII_ERSATZ = (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('Ä', 'Ae'), ('Ö', 'Oe'), ('Ü', 'Ue'), ('ß', 'ss'), ('–', '-'), ('—', '-'),
                ('→', '->'), ('←', '<-'), ('…', '...'), ('≤', '<='), ('≥', '>='), ('°', ' Grad'), ('×', 'x'), ('²', '2'), ('·', '*'),
                ('„', '"'), ('“', '"'), ('”', '"'), ('‚', "'"), ('‘', "'"), ('’', "'"), ('±', '+-'), ('≈', '~'), ('µ', 'u'))


# ----------------------------------------------------------------------------- Helfer
def ascii_text(s):
    """Log-Text nur ASCII (Konventionen §5: Logs werden unter Windows mit cp1252 weiterverarbeitet)."""
    s = str(s)
    for a, b in ASCII_ERSATZ:
        s = s.replace(a, b)
    return s.encode('ascii', 'replace').decode('ascii')


def meld(*a):
    print(ascii_text(' '.join(['[heide_tundra]'] + [str(x) for x in a])), flush=True)


def abbruch(text, code=2):
    """Klare Meldung und Exit-Code 2 (fehlende Pflichtdatei, unbekanntes Feld, unlesbare Regeln)."""
    meld('FEHLER: ' + text)
    sys.exit(code)


def feld_fenster(feld, rand):
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        abbruch('Unbekanntes Feld %r (A1 ... J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        abbruch('Unbekanntes Feld %r (A1 ... J7)' % feld)
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX)  # J-Spalte: 9072 … 9577 (nur 505 m)
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY)
    wi0, wi1 = max(0, i0 - rand), min(NY, i1 + rand)
    wj0, wj1 = max(0, j0 - rand), min(NX, j1 + rand)
    return feld, (i0, i1, j0, j1), (wi0, wi1, wj0, wj1)


def lade_raster(pfad, dtype, win, pflicht=False):
    """Fenster eines NY×NX-Rasters per memmap (nur das Fenster wird gelesen)."""
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            abbruch('Pflichtdatei fehlt: %s (--basis auf die production-Wurzel setzen)' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        if pflicht:
            abbruch('Pflichtdatei hat falsche Groesse: %s (%d Werte, erwartet %d)' % (pfad, n, NX * NY))
        meld('WARNUNG: %s hat %d Werte, erwartet %d - ignoriert' % (pfad, n, NX * NY))
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
    """Binäre Dilatation ≈ Kreisscheibe mit Radius r Zellen (Wechsel 4er/8er-Nachbarschaft → Oktagon)."""
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


def distanz(mask, max_m=64.0, mit_index=False):
    """Euklidische Distanz (m) zur nächsten True-Zelle per Jump-Flooding (vektorisiert); jenseits max_m = 2·max_m.
    mit_index=True liefert zusätzlich (si, sj) = Fensterindex der nächsten True-Zelle (−1, wenn keine gefunden)."""
    H, W = mask.shape
    fern = np.float32(max_m * 2.0)
    if not mask.any():
        d = np.full((H, W), fern, np.float32)
        return (d, np.full((H, W), -1, np.int32), np.full((H, W), -1, np.int32)) if mit_index else d
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
    d = np.minimum(d, fern).astype(np.float32)
    return (d, si, sj) if mit_index else d


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
    """Wertrauschen [0,1] auf absolutem Gitter (nahtlos über Feldgrenzen), bilinear mit Smoothstep, n Oktaven."""
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


# ----------------------------------------------------------------------------- Inventar / Regeln
def lade_inventar(basis, skript_dir):
    """daten/netze.csv → ({pfad: hoehe_m}, {pfad: groesste_kante_m}); sucht production/daten, dann neben dem Skript, dann Repo-Vorlage."""
    kandidaten = [os.path.join(basis, 'daten', 'netze.csv'),
                  os.path.join(skript_dir, 'netze.csv'),
                  os.path.join(skript_dir, '..', '..', 'vorlagen', 'daten', 'netze.csv')]
    for k in kandidaten:
        if os.path.isfile(k):
            inv, kante = {}, {}
            with open(k, encoding='utf-8') as f:
                for row in csv.DictReader(f, delimiter=';'):
                    try:
                        inv[row['pfad']] = float(row.get('groesse_z_m') or 0.3)
                    except Exception:
                        inv[row['pfad']] = 0.3
                    try:
                        kante[row['pfad']] = max(float(row.get('groesse_x_m') or 0), float(row.get('groesse_y_m') or 0),
                                                 float(row.get('groesse_z_m') or 0))
                    except Exception:
                        pass
            meld('Inventar: %s (%d Netze)' % (k, len(inv)))
            return inv, kante
    meld('WARNUNG: daten/netze.csv nicht gefunden - Pfadpruefung und 0,8-m-Grenze entfallen, Netzhoehen = 0,3 m')
    return None, {}


def pruefe_paletten(regeln, inv, kante):
    """Netzpfade der Klassen gegen das Inventar prüfen (fehlende streichen) und Konventionen §4 durchsetzen:
    keine generischen Mittelschicht-Klassen, Steine (rolle 'stein') mit Kante × Maßstab-Max > fels_grenze_m werden gestrichen
    (Felsen > 0,8 m setzt nur felsgruppen_plan.py)."""
    for kn in list(regeln['klassen']):
        if kn in GENERISCHE_MITTEL or regeln['klassen'][kn].get('generisch'):
            meld('WARNUNG: Klasse %s ist eine generische Mittelschicht-Klasse (Konventionen 4) - entfaellt, gehoert in '
                 'mittelschicht_overrides' % kn)
            del regeln['klassen'][kn]
    grenze = float(regeln.get('fels_grenze_m', 0.8))
    zu_gross = []
    for kn, kl in regeln['klassen'].items():
        if kl.get('rolle') != 'stein' or not kante:
            continue
        smax = float(kl['massstab'][1])
        for prof, liste in list(kl['netze'].items()):
            ok = [p for p in liste if kante.get(p, 0.0) * smax <= grenze + 1e-6]
            zu_gross += ['%s/%s: %s (%.2f m)' % (kn, prof, p.rsplit('/', 1)[-1], kante.get(p, 0) * smax) for p in liste if p not in ok]
            kl['netze'][prof] = ok
    if zu_gross:
        meld('WARNUNG: %d Steinnetze ueber %.1f m (Kante x Massstab-Max) gestrichen - gehoeren zu felsgruppen:' % (len(zu_gross), grenze))
        for z in zu_gross:
            meld('   ', z)
    if inv is None:
        return []
    fehlt = []
    for kn, kl in regeln['klassen'].items():
        for prof, liste in list(kl['netze'].items()):
            ok = [p for p in liste if p in inv]
            fehlt += ['%s/%s: %s' % (kn, prof, p) for p in liste if p not in inv]
            kl['netze'][prof] = ok
            if not ok:
                meld('WARNUNG: Klasse %s/%s hat nach der Inventarpruefung kein Netz mehr - Klasse entfaellt dort' % (kn, prof))
    if fehlt:
        meld('WARNUNG: %d Netzpfade nicht im Inventar, gestrichen:' % len(fehlt))
        for f in fehlt:
            meld('   ', f)
    else:
        n = sum(len(v) for kl in regeln['klassen'].values() for v in kl['netze'].values())
        meld('Netzpfade geprueft: alle %d Paletteneintraege im Inventar' % n)
    return fehlt


def dominantes_feldbiom(basis, skript_dir, feld):
    """Nur wenn eigner.r8/welt.json fehlen (Konventionen §1): dominantes Biom des Feldes aus daten/biome_je_feld.json, sonst aue."""
    kandidaten = [os.path.join(basis, 'daten', 'biome_je_feld.json'),
                  os.path.join(skript_dir, 'biome_je_feld.json'),
                  os.path.join(skript_dir, '..', '..', 'vorlagen', 'daten', 'biome_je_feld.json')]
    for k in kandidaten:
        if not os.path.isfile(k):
            continue
        try:
            d = json.load(open(k, encoding='utf-8'))
            e = d.get('felder', d).get(feld)
            bp = e.get('biome_prozent') if isinstance(e, dict) else None
            if bp:
                b = str(sorted(bp, key=lambda x: -float(x[1]))[0][0]).lower()
                if b in BIOME15:
                    return b, k
        except Exception as ex:
            meld('Hinweis: %s nicht auswertbar (%s)' % (k, ex))
    return 'aue', 'Standard aue (biome_je_feld.json fehlt)'


# ----------------------------------------------------------------------------- Weltdaten
def lade_biome(basis, skript_dir, win, feld, hinweise):
    """Biom-Index je Zelle (Index in BIOME15) nach Konventionen §1: eigner.r8 + welt.json-Rezept; Kennzahl 0 und Kennzahlen ohne
    erkennbares Biom → aue, Rezept mit 'vulkan'/'lava' → lava. Fallback dominantes Feldbiom nur, wenn eigner.r8 oder welt.json
    fehlen oder unlesbar sind (Hinweis im Log)."""
    namen = list(BIOME15)
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    welt, grund = None, ''
    if eig is None or not os.path.isfile(wj):
        grund = 'eigner.r8/welt.json fehlen'
    else:
        try:
            welt = json.load(open(wj, encoding='utf-8'))
        except Exception as e:
            grund = 'welt.json unlesbar (%s)' % e
    if welt is None:
        fb, quelle = dominantes_feldbiom(basis, skript_dir, feld)
        txt = '%s - Biom je Zelle = dominantes Feldbiom %r aus %s' % (grund, fb, quelle)
        meld('Hinweis:', txt)
        hinweise.append(txt)
        return np.full((H, W), namen.index(fb), np.int16), 'feldbiom:' + fb
    aue = namen.index('aue')
    tabelle = np.full(256, aue, np.int16)
    kacheln = welt.get('kacheln', {})
    eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
    bekannt, unklar = {0}, []
    for k, v in eintraege:
        try:
            kk = int(v.get('kennzahl', v.get('id', k))) if isinstance(v, dict) else int(k)
        except Exception:
            continue
        if not 0 <= kk < 256:
            continue
        rz = str(v.get('rezept', '')).lower() if isinstance(v, dict) else ''
        b = None
        if rz in namen:
            b = rz
        elif 'vulkan' in rz or 'lava' in rz:
            b = 'lava'
        else:
            for n in namen:
                if n in rz:
                    b = n
                    break
        if b is None:
            b = 'aue'
            if kk != 0:
                unklar.append('%d:%s' % (kk, rz or '-'))
        tabelle[kk] = namen.index(b)
        bekannt.add(kk)
    tabelle[0] = aue   # Kennzahl 0 = Weltgelaende -> aue (FORMAT §2, Konventionen §1)
    ohne = sorted(set(np.unique(eig).tolist()) - bekannt)
    if unklar or ohne:
        hinweise.append('Kennzahlen ohne erkennbares Biom -> aue: %s%s' % (', '.join(unklar[:10]),
                        (' / ohne welt.json-Eintrag: %s' % ohne[:10]) if ohne else ''))
    return tabelle[eig], 'eigner.r8'


def lade_ebene_positionen(ordner, win):
    """Instanzpositionen (Fenster-i, Fenster-j) einer Ebene (plan.json + f32), Bäume und Sonstige getrennt."""
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
        ist_baum = any(r in txt for r in BAUM_ROLLEN) and not any(s in txt for s in NICHT_BAUM)
        (baum if ist_baum else sonst).append(np.stack([fi[m], fj[m]], axis=1))
    return baum, sonst


def lade_bestand(basis, feld, win):
    """Baum-Positionen (Fensterkoordinaten) aus bestand/, witcher/, mittelschicht/, felsgruppen/ (Feld + 8 Nachbarn),
    Ufer-Ebene des Feldes, instanzen/instanzen.json (optional)."""
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    baum, sonst, quellen, hinweise = [], [], [], []
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
            n_dat = 0
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
                    n_dat += 1
            if n_dat == 0:
                hinweise.append('instanzen/instanzen.json gelesen, aber keine f32-Datei mit Instanzen im Fenster gefunden '
                                '(Houdini-Bestand wird dann nur über eigner.r8 berücksichtigt)')
        except Exception as e:
            hinweise.append('instanzen/instanzen.json nicht auswertbar (%s) – Houdini-Bestand ohne Abstandsprüfung' % e)
    else:
        hinweise.append('instanzen/instanzen.json fehlt (optional) – Houdini-Bäume/Felsen ohne Abstandsprüfung')
    baum = np.concatenate(baum, axis=0) if baum else np.zeros((0, 2), np.float32)
    sonst = np.concatenate(sonst, axis=0) if sonst else np.zeros((0, 2), np.float32)
    return baum, sonst, quellen, ufer_da, hinweise


def punkte_maske(pts, H, W):
    m = np.zeros((H, W), bool)
    if len(pts):
        ii = np.clip(np.round(pts[:, 0]).astype(np.int32), 0, H - 1)
        jj = np.clip(np.round(pts[:, 1]).astype(np.int32), 0, W - 1)
        m[ii, jj] = True
    return m


def lagen_faktor(lagen, gewichte):
    """Gewichtetes Mittel der Lagen-Gewichte über die Deckung (Σ w·d / Σ d); Zellen ohne Deckung → 1."""
    if not lagen:
        return None
    num = None
    den = None
    for name, a in lagen.items():
        w = float(gewichte.get(name, gewichte.get('_default', 0.5)))
        d = a.astype(np.float32) / 255.0
        num = d * w if num is None else num + d * w
        den = d if den is None else den + d
    return np.where(den > 0.02, num / np.maximum(den, 1e-3), 1.0).astype(np.float32)


def teppich_maske(lagen, ts, weg, d_wasser):
    """Kiesel/Steine < 0,5 m nicht als Hangteppich (Korrektur Runde 2): nur auf/um Geroell-Lagen (kontakt_m), am Weg (weg_m) und
    am Ufer (wasser_m). lagen = uint8 0-255."""
    fels = np.zeros(weg.shape, bool)
    for n in ts.get('lagen', ['Kies', 'Geroell', 'Fels', 'Felsplatte']):
        if n in lagen:
            fels |= lagen[n] >= int(ts.get('ab', 80))
    m = dilate(fels, float(ts.get('kontakt_m', 6))) if fels.any() else fels
    if weg.any():
        m |= dilate(weg, float(ts.get('weg_m', 3)))
    m |= d_wasser <= float(ts.get('wasser_m', 5))
    return m


def lagen_anteil(lagen, namen):
    out = None
    for n in namen:
        if n in lagen:
            d = lagen[n].astype(np.float32) / 255.0
            out = d if out is None else out + d
    return out


BEZUG_TEXT = 'Landzellen im Fenster (ohne karte_wasser und ohne Meer = hoehe < 0 und karte_wasser == 0)'


def meer_ok(h, ist_meer, d_meer, k_meer, k_strand, tief, saum_h, saum_m):
    """Schlussfilter Meer (Konventionen §1b, Runde 4): h = Gelaendehoehe bilinear am Instanzort. False = verwerfen: unter tief
    (-0,3 m) immer; unter 0 m oder auf einer Meerzelle nur Meeres-Rollen; 0 .. saum_h im Kuestensaum (<= saum_m zum Meer) nur
    Strand-/Wasserkante-Rollen."""
    ok = np.isfinite(h) & (h >= tief)
    if not k_meer:
        ok &= (h >= 0.0) & ~ist_meer
    if not k_strand:
        ok &= ~((h <= saum_h) & (d_meer <= saum_m))
    return ok


# ----------------------------------------------------------------------------- Planung je Feld
def schreibe_leerplan(feld, out_dir, regeln, biome_fenster, anteil_eigen, biom_quelle, hinweise, t0, meer_zellen=0):
    """Konventionen §1: Eigenanteil < min_anteil_fenster → leerer plan.json (instanzen 0, keine f32), nie Text statt plan.json."""
    Z = regeln['zustaendigkeit']
    os.makedirs(out_dir, exist_ok=True)
    for f in os.listdir(out_dir):
        if f.endswith('.f32'):
            os.remove(os.path.join(out_dir, f))
    hinweise.append('Anteil eigener Biome %s im Fenster %.4f < %.2f - kein Plan' % (
        '/'.join(Z['biome_eigen']), anteil_eigen, float(Z['min_anteil_fenster'])))
    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'ebene': regeln.get('ebene', 'heide_tundra'), 'instanzen': 0,
            'dateien': {}, 'entfernen': '', 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'biome_fenster': biome_fenster, 'biome_fenster_bezug': BEZUG_TEXT, 'zellen_zustaendig': 0,
            'biome_eigen': list(Z['biome_eigen']), 'kollision_anzahl': 0, 'meer_zellen': int(meer_zellen), 'meer_gefiltert': 0,
            'klassen': {}, 'schichten': {}, 'profil_anteil_feld': {'heide': 0.0, 'tundra': 0.0},
            'statistik': {'anteil_eigen_fenster': round(anteil_eigen, 4), 'biom_quelle': biom_quelle, 'saum_m': float(Z['saum_m']),
                          'laufzeit_s': round(time.time() - t0, 1)},
            'hinweise': hinweise,
            'ungetestet': 'UNGETESTET MIT ECHTDATEN - Cloud-Rauchtest nur mit synthetischen Rastern.'}
    with open(os.path.join(out_dir, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('Feld %s: Anteil %s im Fenster %.2f %% < %.0f %% - leerer plan.json (instanzen 0)' % (
        feld, '/'.join(Z['biome_eigen']), 100 * anteil_eigen, 100 * float(Z['min_anteil_fenster'])))
    return plan


def plane_feld(feld_in, basis, skript_dir, regeln, faktor, bild, inv, entfernen_cli):
    t0 = time.time()
    rand = int(regeln.get('fenster_rand_m', 64))
    feld, fb_, win = feld_fenster(feld_in, rand)
    i0, i1, j0, j1 = fb_
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    seed = int(regeln.get('seed', 1))
    hinweise = []
    out_dir = os.path.join(basis, regeln['ausgabe']['ordner'], feld)
    meld('Feld %s: Fenster i %d-%d, j %d-%d (%d x %d)' % (feld, wi0, wi1, wj0, wj1, H, W))

    # --- Höhe (Pflicht) und Zuständigkeit nach Biom-Zellen (Konventionen §1)
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True).astype(np.float32)
    ii, jj = np.indices((H, W), dtype=np.int32)
    ii_abs = ii + wi0
    jj_abs = jj + wj0
    im_feld_zelle = (ii_abs >= i0) & (ii_abs < i1) & (jj_abs >= j0) & (jj_abs < j1)
    Z = regeln['zustaendigkeit']
    # Wasser und Meer (Konventionen §1b, Runde 4): karte_wasser = nur Suesswasser; Meer = hoehe < 0 und karte_wasser == 0
    wasser_r = lade_raster(os.path.join(basis, WELT, 'karte_wasser.r8'), np.uint8, win)
    wasser = (wasser_r > 0) if wasser_r is not None else np.zeros((H, W), bool)
    meer = (hoehe < 0.0) & ~wasser
    wasser_alle = wasser | meer | ~np.isfinite(hoehe)
    land_z = ~wasser_alle
    meer_zellen = int(meer.sum())
    MR = regeln.get('meer', {})
    meer_tief = float(MR.get('tief_m', -0.3))
    meer_saum_h = float(MR.get('saum_hoehe_m', 0.3))
    meer_saum_m = float(MR.get('saum_m', 30.0))
    bio, biom_quelle = lade_biome(basis, skript_dir, win, feld, hinweise)
    bezug = land_z if land_z.any() else np.ones((H, W), bool)   # Meer (eigner 0 = aue) zaehlt nicht mit
    werte, zahl = np.unique(bio[bezug], return_counts=True)
    biome_fenster = {BIOME15[int(k)]: round(float(c) / max(1, int(bezug.sum())), 4)
                     for k, c in sorted(zip(werte, zahl), key=lambda x: (-x[1], x[0]))}
    eigen = np.isin(bio, [BIOME15.index(b) for b in Z['biome_eigen']]) & land_z
    anteil_eigen = float(eigen[bezug].mean())
    if anteil_eigen < float(Z['min_anteil_fenster']):
        meld('Biome im Fenster (Landzellen): %s' % biome_fenster)
        return schreibe_leerplan(feld, out_dir, regeln, biome_fenster, anteil_eigen, biom_quelle, hinweise, t0, meer_zellen)
    saum_m = float(Z['saum_m'])
    wf = regeln.get('wuesten_felder', {})
    wuestenfeld = feld in wf.get('felder', [])
    if eigen.all():
        zust = np.ones((H, W), np.float32)
        naechst_bio = bio
    else:
        d_eigen, si, sj = distanz(eigen, max(64.0, 2.0 * saum_m), mit_index=True)
        zust = np.where(eigen, 1.0, np.clip(1.0 - d_eigen / saum_m, 0, 1)).astype(np.float32)
        naechst_bio = np.where(si >= 0, bio[np.clip(si, 0, H - 1), np.clip(sj, 0, W - 1)], bio)
        if wuestenfeld and not wf.get('saum', False):   # Wüstenfeld: nur ergänzen, kein Saum in Wüsten-/Fremdzellen
            zust = eigen.astype(np.float32)
    zellen_zustaendig = int(((zust > 0) & im_feld_zelle & land_z).sum())
    meld('Biome im Fenster: %s; eigen (%s) %.1f %%, zustaendig %d Zellen im Feld (inkl. Saum %d m), Quelle %s' % (
        {k: v for k, v in list(biome_fenster.items())[:5]}, '/'.join(Z['biome_eigen']), 100 * anteil_eigen, zellen_zustaendig,
        int(saum_m), biom_quelle))

    # --- weitere Raster
    weg = lade_raster(os.path.join(basis, WELT, 'karte_weg.r8'), np.uint8, win)
    ort = lade_raster(os.path.join(basis, WELT, 'karte_ort.r8'), np.uint8, win)
    for nm, a in (('karte_wasser.r8', wasser_r), ('karte_weg.r8', weg), ('karte_ort.r8', ort)):
        if a is None:
            meld('WARNUNG: %s fehlt - ohne Abstand zu dieser Flaeche geplant' % nm)
            hinweise.append('%s fehlt – Annahme: keine Fläche dieser Art' % nm)
    weg = (weg > 0) if weg is not None else np.zeros((H, W), bool)
    ort = (ort > 0) if ort is not None else np.zeros((H, W), bool)
    lagen = {}
    for n in LAGEN_NAMEN:
        a = lade_raster(os.path.join(basis, WELT, 'lage_%s.r8' % n), np.uint8, win)
        if a is not None:
            lagen[n] = a
    meld('Lagen vorhanden: %s' % (', '.join(sorted(lagen)) if lagen else 'keine (Lagenfaktor 1)'))
    if not lagen:
        hinweise.append('keine lage_*.r8 gefunden – Lagenfaktoren = 1, keine Sand-/Wald-/Schnee-Dämpfung')
    baum_pts, sonst_pts, quellen, ufer_da, hw = lade_bestand(basis, feld, win)
    hinweise += hw
    meld('Bestand: %d Baeume, %d Sonstige aus %s' % (len(baum_pts), len(sonst_pts), quellen or 'nichts'))
    for h in hw:
        meld('Hinweis:', h)

    # --- abgeleitete Felder
    g = regeln['gelaende']
    hs = gauss_blur(hoehe, float(g.get('hang_sigma_m', 2.0)))
    dhi = np.gradient(hs, axis=0)
    dhj = np.gradient(hs, axis=1)
    hang = np.degrees(np.arctan(np.sqrt(dhi * dhi + dhj * dhj))).astype(np.float32)
    nl = np.sqrt(dhi * dhi + dhj * dhj + 1.0)
    nx_, ny_, nz_ = (-dhj / nl).astype(np.float32), (-dhi / nl).astype(np.float32), (1.0 / nl).astype(np.float32)
    expo = np.clip((hoehe - gauss_blur(hoehe, float(g.get('expo_sigma_m', 40)))) / float(g.get('expo_norm_m', 8)), -1, 1).astype(np.float32)
    mulde = np.clip((gauss_blur(hoehe, float(g.get('mulde_sigma_m', 12))) - hoehe) / 3.0, 0, 1).astype(np.float32)
    land = (hoehe > 0.05) & land_z
    d_wasser = distanz(wasser, 64.0)                     # Suesswasser: Wasserkante-Band, wasser_bonus
    d_meer = distanz(meer, 64.0) if meer.any() else np.full((H, W), 129.0, np.float32)
    d_wasser_alle = np.minimum(d_wasser, d_meer)          # Sperre/Abstand (wasser_min), Ufer-Kieselmaske
    kuestensaum = (hoehe >= 0.0) & (hoehe <= meer_saum_h) & (d_meer <= meer_saum_m) & ~wasser
    meer_gefiltert = 0
    meer_gefiltert_je = {}
    if meer.any():
        hinweise.append('Meer (hoehe < 0, karte_wasser == 0): %d Zellen im Fenster, Kuestensaum 0..%.1f m: %d Zellen; darunter %.1f m nichts'
                        % (meer_zellen, meer_saum_h, int(kuestensaum.sum()), meer_tief))
    ab = regeln['abstand_m']
    weg_klein = dilate(weg, ab.get('weg_klein', 2.5)) if weg.any() else weg
    weg_gross = dilate(weg, ab.get('weg_gross', 4.0)) if weg.any() else weg
    ort_m = dilate(ort, ab.get('ort', 5.0)) if ort.any() else ort
    baum_mask = punkte_maske(baum_pts, H, W)
    sonst_mask = punkte_maske(sonst_pts, H, W)
    stamm = dilate(baum_mask, ab.get('baumstamm', 1.5)) if baum_mask.any() else baum_mask
    sonst_nah = dilate(sonst_mask, ab.get('bestand_sonst', 1.0)) if sonst_mask.any() else sonst_mask
    kd = regeln['kronendach']
    kr = int(round(float(kd.get('radius_m', 4.5))))
    beschattung = np.clip(box_blur(baum_mask.astype(np.float32), kr) * (2 * kr + 1) ** 2 * float(kd.get('k', 0.9)), 0, 1)
    baum_nah = {}

    # --- Profil (heide/tundra) je Zelle: eigenes Biom, im Saum das der nächsten eigenen Zelle; Lagen schalten nur das Profil um
    profil = np.where(naechst_bio == BIOME15.index('heide'), 0, 1).astype(np.int8)
    for pl in regeln.get('profil_nach_lage', []):
        ln = pl['lage']
        if ln not in lagen:
            continue
        m = (lagen[ln].astype(np.float32) / 255.0 >= float(pl['ab_anteil'])) & (zust > 0)
        if 'ab_hoehe_m' in pl:
            m &= hoehe >= float(pl['ab_hoehe_m'])
        nur = [BIOME15.index(b) for b in pl.get('nur_in', Z['biome_eigen']) if b in BIOME15]
        m &= np.isin(naechst_bio, nur)
        profil = np.where(m, 0 if pl['profil'] == 'heide' else 1, profil).astype(np.int8)
    sperre = np.ones((H, W), np.float32)
    for sn, sp in regeln.get('sperren', {}).items():
        if not isinstance(sp, dict):
            continue
        a = lagen_anteil(lagen, sp['lagen'])
        if a is not None:
            sperre = np.where(a >= float(sp['ab_anteil']), float(sp['faktor']), sperre).astype(np.float32)
    sand_sperre = np.zeros((H, W), bool)
    if wuestenfeld:
        sperre *= float(wf.get('faktor', 0.7))
        a = lagen_anteil(lagen, wf.get('sand_lagen', ['Sand', 'Sandstein']))
        if a is not None:
            ab_ = float(wf.get('sand_sperre_ab', 0.5))
            sperre *= np.clip(1.0 - a / max(ab_, 1e-3), 0, 1).astype(np.float32)
            sand_sperre = a >= ab_
        meld('Wuestenfeld (nur ergaenzen): Faktor %.2f, kein Saum, Sand/Sandstein-Sperre %.1f %% des Fensters'
             % (wf.get('faktor', 0.7), 100 * sand_sperre.mean()))
        hinweise.append('Wüstenfeld: Faktor %.2f, nur heide/tundra-Zellen ohne Saum, Sand+Sandstein >= %.1f gesperrt, kein entfernen'
                        % (wf.get('faktor', 0.7), wf.get('sand_sperre_ab', 0.5)))
    basisfak = (zust * sperre * float(faktor)).astype(np.float32)
    schnee = lagen.get(regeln['schnee']['lage'])
    schnee = schnee.astype(np.float32) / 255.0 if schnee is not None else None
    ho = regeln['hoehe']
    zf = im_feld_zelle & (zust > 0)
    anteil_prof = {'heide': round(float((profil[zf] == 0).mean()), 3) if zf.any() else 0.0,
                   'tundra': round(float((profil[zf] == 1).mean()), 3) if zf.any() else 0.0}
    meld('Profil in zustaendigen Feldzellen: heide %.0f %%, tundra %.0f %%; mittlerer Basisfaktor im Feld %.3f'
         % (100 * anteil_prof['heide'], 100 * anteil_prof['tundra'], basisfak[im_feld_zelle].mean()))
    if not (basisfak[im_feld_zelle & land] > 0).any():
        hinweise.append('kein planbares Land im Feld (keine heide/tundra-Zelle im Feld, nur Saum außerhalb oder Wasser) – nichts zu planen')

    # --- Flecken (Rauschen) je Name
    flecken = {}
    for k_, (fn, fp) in enumerate(regeln['flecken'].items()):
        if not isinstance(fp, dict):
            continue
        n = wertrauschen(ii_abs, jj_abs, fp['skala_m'], seed, 90000 + 20 * k_, int(fp.get('oktaven', 2)))
        flecken[fn] = smoothstep((n - float(fp['schwelle'])) / max(float(fp.get('weich', 0.1)), 1e-3))

    lagen_fak_cache = {}

    def lagen_fak(name):
        if name not in lagen_fak_cache:
            lagen_fak_cache[name] = lagen_faktor(lagen, regeln['lagen_gewichte'][name]) if lagen else None
        return lagen_fak_cache[name]

    # --- Klassen
    wind = regeln['wind']
    lee = math.radians(float(wind.get('richtung_grad', 300)) + 180.0)  # leewärts (Kompass, 0 = N, Y wächst nach Süden)
    lee_x, lee_y = math.sin(lee), -math.cos(lee)
    ergebnis = {}
    klassen = regeln['klassen']
    for k_idx, (kn, kl) in enumerate(klassen.items()):
        kanal = 1000 + 500 * k_idx  # Kanäle: Zentren kanal, Gruppen kanal+1, Positionen kanal+100.., Attribute kanal+200..
        if kn == 'moorstein' and ufer_da:
            meld('  %-14s übersprungen (Ufer-Ebene ufer/foliage_%s vorhanden)' % (kn, feld))
            hinweise.append('moorstein entfällt: Ufer-Ebene vorhanden')
            continue
        netze_heide = kl['netze'].get('heide', kl['netze'].get('beide', []))
        netze_tundra = kl['netze'].get('tundra', kl['netze'].get('beide', []))
        d_h, d_t = float(kl['dichte'].get('heide', 0)), float(kl['dichte'].get('tundra', 0))
        if (d_h <= 0 or not netze_heide) and (d_t <= 0 or not netze_tundra):
            continue
        p = np.where(profil == 0, d_h if netze_heide else 0.0, d_t if netze_tundra else 0.0).astype(np.float32) * basisfak
        lf = lagen_fak(kl.get('lagen', 'pflanze_trocken'))
        if lf is not None:
            p *= lf
        if kl.get('teppich_sperre'):  # Runde 2: Kiesel nicht flaechig ueber ganze Haenge
            p *= teppich_maske(lagen, kl['teppich_sperre'], weg, d_wasser_alle)
        hv, hn = float(kl.get('hang_voll_bis', 28)), float(kl.get('hang_null_ab', 40))
        p *= np.clip((hn - hang) / max(hn - hv, 1e-3), 0, 1)
        if 'hoehe_grenze' in kl:  # Höhenstufen (nur Profil tundra hat endliche Grenzen)
            for pi, pn in ((0, 'heide'), (1, 'tundra')):
                grenze = float(ho[pn].get(kl['hoehe_grenze'], 9999))
                if grenze < 9000:
                    ab_h = float(ho[pn].get(kl.get('hoehe_abnahme', ''), grenze - 20))
                    fh = np.clip((grenze - hoehe) / max(grenze - ab_h, 1e-3), 0, 1)
                    p = np.where(profil == pi, p * fh, p)
        if 'hoehe_max_m_tundra' in kl:
            p = np.where((profil == 1) & (hoehe > float(kl['hoehe_max_m_tundra'])), 0, p)
        if schnee is not None and kl.get('schnee'):
            fv = float(regeln['schnee']['faktor_steine_bei_voll' if kl['schnee'] == 'stein' else 'faktor_pflanzen_bei_voll'])
            p *= (1 - (1 - fv) * schnee)
        if not kl.get('ohne_kronen_faktor', False):
            p *= (1 - (1 - float(kd.get('pflanzen_faktor_bei_voll', 0.25))) * beschattung)
        if kl.get('flecken') in flecken:
            p *= flecken[kl['flecken']]
        if 'expo_bonus' in kl:
            p *= (1 + float(kl['expo_bonus']) * np.clip(expo, 0, 1))
        if 'mulde_bonus' in kl and 'mulde_gruppe' not in kl:
            p *= (1 + (float(kl['mulde_bonus']) - 1) * mulde)
        if 'wasser_bonus' in kl:
            wb = float(kl.get('wasser_bonus_m', 40))
            p *= (1 + (float(kl['wasser_bonus']) - 1) * np.clip(1 - d_wasser / wb, 0, 1))
        if 'baum_naehe_bonus' in kl and baum_mask.any():
            r = int(kl.get('baum_naehe_m', 12))
            if r not in baum_nah:
                baum_nah[r] = dilate(baum_mask, r)
            p *= np.where(baum_nah[r], float(kl['baum_naehe_bonus']), 1.0)
        if 'wasser_band_m' in kl:  # Wasserkante: Band um Moortümpel/Bäche, zusätzlich feuchte Lagen
            a0, a1 = kl['wasser_band_m']
            band = ((d_wasser >= a0) & (d_wasser <= a1)).astype(np.float32)
            if kl.get('feucht_lagen_auch'):
                fa = lagen_anteil(lagen, kl['feucht_lagen_auch'])
                if fa is not None:
                    band = np.maximum(band, (fa >= float(kl.get('feucht_ab_anteil', 0.5))) * float(kl.get('feucht_faktor', 0.35)))
            p *= band
            ok = land & (d_wasser_alle >= float(a0)) & ~ort_m & ~sonst_nah & ~stamm
        else:
            ok = land & (d_wasser_alle >= float(kl.get('wasser_min', 0.5))) & ~ort_m & ~sonst_nah & ~stamm
        k_meer = bool(kl.get('meer_rolle'))
        k_strand = k_meer or bool(kl.get('strand')) or str(kl.get('schicht')) == '5 wasserkante'
        if k_meer:  # Meeres-Rolle: auch flaches Meer bis tief_m (nur Suesswasser-Abstand)
            ok |= (hoehe >= meer_tief) & ~wasser & (d_wasser >= float(kl.get('wasser_min', 0.5))) & ~ort_m & ~sonst_nah & ~stamm
        if not k_strand:
            ok &= ~kuestensaum  # Runde 4: 0 .. +0,3 m am Meer nur Wasserkante/Strand
        ok &= ~(weg_gross if kl.get('weg', 'klein') == 'gross' else weg_klein)
        if 'baum_abstand_m' in kl and baum_mask.any():
            r = int(math.ceil(float(kl['baum_abstand_m'])))
            if ('b', r) not in baum_nah:
                baum_nah[('b', r)] = dilate(baum_mask, r)
            ok &= ~baum_nah[('b', r)]
        p = np.where(ok, p, 0).astype(np.float32)
        p = np.minimum(p, 0.95)

        # --- Ziehen: Gruppenzentren (Bernoulli je Zelle) + Mitglieder im Radius
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
        kp = kanal + 100 + 4 * m_idx
        ang = hash01(pci, pcj, seed, kp) * 2 * np.pi
        rr = np.sqrt(hash01(pci, pcj, seed, kp + 1)) * rad[rep]
        rr = np.where(m_idx == 0, 0.0, rr)
        fi = ci[rep] + hash01(pci, pcj, seed, kp + 2) + rr * np.sin(ang) - 0.5
        fj = cj[rep] + hash01(pci, pcj, seed, kp + 3) + rr * np.cos(ang) - 0.5
        gi = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
        gj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
        gut = (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1) & ok[gi, gj] & (zust[gi, gj] > 0)  # nie jenseits des Saums
        if 'mulde_gruppe' not in kl and gmax > 1:
            gut &= (p[gi, gj] > 0)  # Mitglieder nur dort, wo die Klasse überhaupt darf
        fi, fj, gi, gj, pci, pcj, m_idx = fi[gut], fj[gut], gi[gut], gj[gut], pci[gut], pcj[gut], m_idx[gut]
        if len(fi) == 0:
            continue
        # Schlussfilter Meer (Runde 4, Sicherheitsnetz): Gelaendehoehe bilinear am Instanzort
        gut = meer_ok(bilinear(hoehe, fi, fj), meer[gi, gj], d_meer[gi, gj], k_meer, k_strand, meer_tief, meer_saum_h, meer_saum_m)
        if not gut.all():
            meer_gefiltert += int((~gut).sum())
            meer_gefiltert_je[kn] = meer_gefiltert_je.get(kn, 0) + int((~gut).sum())
            fi, fj, gi, gj, pci, pcj, m_idx = fi[gut], fj[gut], gi[gut], gj[gut], pci[gut], pcj[gut], m_idx[gut]
            if len(fi) == 0:
                continue
        if 'baum_abstand_m' in kl:  # Mindestabstand innerhalb der Klasse: eine Instanz je Zelle eines groben Rasters
            d = max(2, int(round(float(kl['baum_abstand_m']) * 0.7)))
            key = ((gi + wi0) // d).astype(np.int64) * 100003 + ((gj + wj0) // d)
            _, erste = np.unique(key, return_index=True)
            keep = np.zeros(len(fi), bool)
            keep[erste] = True
            fi, fj, gi, gj, pci, pcj, m_idx = fi[keep], fj[keep], gi[keep], gj[keep], pci[keep], pcj[keep], m_idx[keep]
        # --- Attribute
        nn = len(fi)
        kan = kanal + 200 + 16 * m_idx
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
        # Netzwahl je Profil (vektorisiert über Objekt-Arrays)
        nh_arr = np.array(netze_heide if netze_heide else [''], dtype=object)
        nt_arr = np.array(netze_tundra if netze_tundra else [''], dtype=object)
        hv_ = hash01(pci, pcj, seed, kan + 7)
        netz = np.where(prof_i == 0, nh_arr[(hv_ * len(nh_arr)).astype(np.int32)], nt_arr[(hv_ * len(nt_arr)).astype(np.int32)])
        # Höhe / Eingraben
        z = bilinear(hoehe, fi, fj)
        if 'eingraben_anteil' in kl:
            nh = np.array([inv.get(pf, 0.3) if inv else 0.3 for pf in netz], np.float32)
            z = z - float(kl['eingraben_anteil']) * nh * sk
        else:
            z = z - float(kl.get('eingraben_cm', 3)) / 100.0
        # Rotation: Kippen auf Normale (Anteil), Wind-Lehnen leewärts, Yaw
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
        # Runde 4: an der Kueste auch die Instanzhoehe (inkl. Eingraben) nie unter tief_m (-0,3 m)
        zk = (z >= meer_tief) | (d_meer[gi, gj] > meer_saum_m)
        if not zk.all():
            n_raus = int((~zk & im_feld).sum())
            if n_raus:
                meer_gefiltert += n_raus
                meer_gefiltert_je[kn] = meer_gefiltert_je.get(kn, 0) + n_raus
            im_feld &= zk
        ergebnis[kn] = {
            'x': x_cm.astype(np.float32), 'y': y_cm.astype(np.float32), 'z': (z * 100.0).astype(np.float32),
            'q': q, 's': sk, 'netz': netz, 'im_feld': im_feld, 'gi': gi, 'gj': gj,
            'thin': hash01(pci, pcj, seed, kan + 9), 'klasse': kl,
        }
        meld('  %-14s %7d Instanzen (%d im Feld), Dichte-Mittel %.4f/m²' % (kn, nn, int(im_feld.sum()), float(p[im_feld_zelle].mean())))

    # --- Budget (Konventionen §3, hart): nur Instanzen im Feld zählen
    bud = regeln['budget']
    prio = list(bud.get('prioritaet', list(klassen.keys())))      # zuerst genannte = wichtigste
    prio = [k for k in prio if k in ergebnis] + [k for k in ergebnis if k not in prio]
    maxi, maxk = int(bud.get('instanzen_je_feld', 60000)), int(bud.get('kollision_je_feld', 3000))
    ziel = min(int(bud.get('ziel_instanzen_je_feld', maxi)), maxi)
    kleinzeug = set(bud.get('kleinzeug_an_gras', []))

    def koll_flag(kn, netz):
        kl = klassen[kn]
        if not kl.get('kollision', False):
            return np.zeros(len(netz), bool)
        ab_h = float(kl.get('kollision_ab_hoehe_m', 0))
        return np.array([(inv.get(pf, 0.3) if inv else 0.3) >= ab_h for pf in netz], bool)

    for kn in ergebnis:
        ergebnis[kn]['koll'] = koll_flag(kn, ergebnis[kn]['netz'])
        ergebnis[kn]['keep'] = ergebnis[kn]['im_feld'].copy()

    def kappe(grenze, zaehlt, grund):
        """Exakte Kappung: von der niedrigsten Priorität aufwärts fallen je Klasse die Instanzen mit dem höchsten Hash zuerst."""
        ist = sum(int((e['keep'] & zaehlt(e)).sum()) for e in ergebnis.values())
        if ist <= grenze:
            return ist
        ueber, weg_je = ist - grenze, {}
        for kn in reversed(prio):
            if ueber <= 0:
                break
            e = ergebnis[kn]
            kand = np.nonzero(e['keep'] & zaehlt(e))[0]
            if kand.size == 0:
                continue
            k = min(ueber, int(kand.size))
            raus = kand[np.argsort(-e['thin'][kand], kind='stable')[:k]]
            e['keep'][raus] = False
            ueber -= k
            weg_je[kn] = k
        txt = 'WARNUNG %s: %d -> %d, gestrichen %s' % (grund, ist, grenze, weg_je)
        meld(txt)
        hinweise.append(txt)
        kz = 'Kleinzeug %s ausgedünnt – Fläche soll Landschafts-Gras (GT_*) tragen' % sorted(kleinzeug & set(weg_je))
        if kleinzeug & set(weg_je) and kz not in hinweise:
            hinweise.append(kz)
        return grenze

    # 1. Kollisionsdeckel exakt (Kollisionsklassen in Prioritätsreihenfolge)
    kappe(maxk, lambda e: e['koll'], 'Kollisionsdeckel (%d)' % maxk)
    # 2. Zielwert: weiche Ausdünnung von hinten nach prioritaet, je Klasse höchstens auf 25 %
    gesamt = sum(int(e['keep'].sum()) for e in ergebnis.values())
    gesamt_vor = gesamt
    if gesamt > ziel:
        weg_je = {}
        for kn in reversed(prio):
            if gesamt <= ziel:
                break
            e = ergebnis[kn]
            n = int(e['keep'].sum())
            z_ = max(int(n * 0.25), n - (gesamt - ziel))
            if z_ < n:
                e['keep'] &= e['thin'] < (z_ / max(n, 1))
                n2 = int(e['keep'].sum())
                gesamt -= n - n2
                weg_je[kn] = n - n2
        txt = 'WARNUNG Budget-Ziel: %d -> %d (Ziel %d, Deckel %d), ausgeduennt %s' % (gesamt_vor, gesamt, ziel, maxi, weg_je)
        meld(txt)
        hinweise.append(txt)
        kz = 'Kleinzeug %s ausgedünnt – Fläche soll Landschafts-Gras (GT_*) tragen' % sorted(kleinzeug & set(weg_je))
        if kleinzeug & set(weg_je) and kz not in hinweise:
            hinweise.append(kz)
    # 3. harter Deckel exakt
    kappe(maxi, lambda e: np.ones(len(e['keep']), bool), 'Instanzdeckel (%d)' % maxi)

    # --- Ausgabe
    os.makedirs(out_dir, exist_ok=True)
    for alt in os.listdir(out_dir):
        if alt.endswith('.f32'):
            os.remove(os.path.join(out_dir, alt))
    dateien = {}
    schichten = {}
    klassen_n = {}
    netz_rows = {}
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
            netz_rows.setdefault(name, []).append(rows[m])
            koll_ok = bool(kl.get('kollision', False) and (inv.get(pf, 0.3) if inv else 0.3) >= float(kl.get('kollision_ab_hoehe_m', 0)))
            if name in dateien and dateien[name]['klasse'] != kn:
                hinweise.append('Netz %s in Klassen %s und %s – Setzer-Einstellungen der ersten Klasse gelten' % (name, dateien[name]['klasse'], kn))
            d = dateien.setdefault(name, {'pfad': pf, 'anzahl': 0, 'gruppe': kl.get('gruppe_name', kn), 'rolle': kl.get('rolle', kn),
                                          'sichtweite': [int(v) for v in kl.get('sichtweite', [0, 0])],
                                          'schatten': bool(kl.get('schatten', False)), 'kollision': koll_ok,
                                          'ebene': SCHICHT_KURZ.get(kl['schicht'], kl['schicht']), 'schicht': kl['schicht'], 'klasse': kn})
            d['anzahl'] += int(m.sum())
            total += int(m.sum())
    for name, teile in netz_rows.items():
        np.concatenate(teile, axis=0).astype('<f4').tofile(os.path.join(out_dir, name + '.f32'))
    koll_n = sum(d['anzahl'] for d in dateien.values() if d['kollision'])
    if koll_n > maxk:   # nur möglich, wenn ein Netz in Klassen mit und ohne Kollision vorkommt (erste Klasse gilt)
        hinweise.append('WARNUNG: kollision_anzahl %d > %d, weil ein Netz in Klassen mit und ohne Kollision steht' % (koll_n, maxk))
        meld(hinweise[-1])
    ent = entfernen_cli
    if ent is None:
        prof_dom = 'heide' if anteil_prof['heide'] >= anteil_prof['tundra'] else 'tundra'
        ent = regeln.get('entfernen', {}).get(prof_dom, '')
    if ent and wuestenfeld:
        meld('Hinweis: Wuestenfeld %s - entfernen %r wird ignoriert (nur ergaenzen)' % (feld, ent))
        ent = ''
    plan = {
        'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'ebene': regeln.get('ebene', 'heide_tundra'), 'instanzen': total,
        'dateien': dateien, 'entfernen': ent or '', 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
        'biome_fenster': biome_fenster, 'biome_fenster_bezug': BEZUG_TEXT, 'zellen_zustaendig': zellen_zustaendig,
        'biome_eigen': list(Z['biome_eigen']), 'kollision_anzahl': int(koll_n), 'meer_zellen': meer_zellen, 'meer_gefiltert': int(meer_gefiltert),
        'klassen': klassen_n, 'schichten': schichten, 'profil_anteil_feld': anteil_prof,
        'statistik': {'anteil_eigen_fenster': round(anteil_eigen, 4),
                      'anteil_eigen_feld': round(float(eigen[im_feld_zelle & land_z].mean()), 4) if (im_feld_zelle & land_z).any() else 0.0,
                      'meer_gefiltert_je_klasse': meer_gefiltert_je, 'kuestensaum_zellen_feld': int((kuestensaum & im_feld_zelle).sum()),
                      'biom_quelle': biom_quelle, 'saum_m': saum_m, 'wuestenfeld': wuestenfeld,
                      'instanzen_vor_budget': int(sum(int(e['im_feld'].sum()) for e in ergebnis.values())),
                      'ausserhalb_eigener_zellen': int(sum(int((e['keep'] & ~eigen[e['gi'], e['gj']]).sum()) for e in ergebnis.values())),
                      'quellen_bestand': quellen, 'faktor': faktor, 'seed': seed, 'numba': NUMBA,
                      'laufzeit_s': round(time.time() - t0, 1)},
        'hinweise': hinweise,
        'ungetestet': 'UNGETESTET MIT ECHTDATEN - Cloud-Rauchtest nur mit synthetischen Rastern. Setzer: HISM je Netz, '
                      'Kollision nur wo kollision=true, sichtweite in cm.',
    }
    with open(os.path.join(out_dir, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('Feld %s: %d Instanzen (%d mit Kollision) in %d Netzen -> %s  [%.1f s]' % (feld, total, koll_n, len(dateien), out_dir, time.time() - t0))
    for s in sorted(schichten):
        meld('   Schicht %-14s %6d' % (s, schichten[s]))

    if bild:
        schreibe_bild(basis, regeln, feld, fb_, win, hoehe, wasser_alle, weg, ort, profil, sand_sperre, basisfak, ergebnis)
    return plan


def schreibe_bild(basis, regeln, feld, fb, win, hoehe, wasser, weg, ort, profil, sand_sperre, basisfak, ergebnis):
    i0, i1, j0, j1 = fb
    wi0, wi1, wj0, wj1 = win
    a0, a1, b0, b1 = i0 - wi0, i1 - wi0, j0 - wj0, j1 - wj0
    h = hoehe[a0:a1, b0:b1]
    H, W = h.shape
    fb_ = regeln.get('bild_farben', {})
    dj = np.gradient(h, axis=1)
    di = np.gradient(h, axis=0)
    shade = np.clip(0.55 + 0.45 * (-0.7 * dj - 0.5 * di) / np.sqrt(dj * dj + di * di + 1), 0.2, 1.0)
    img = np.zeros((H, W, 3), np.float32)
    ph = np.array(fb_.get('heide_profil', [70, 50, 70]), np.float32)
    pt = np.array(fb_.get('tundra_profil', [60, 70, 60]), np.float32)
    pr = profil[a0:a1, b0:b1]
    img[:] = np.where(pr[..., None] == 0, ph, pt) * (0.6 + 0.8 * shade[..., None])
    img[basisfak[a0:a1, b0:b1] <= 0] *= 0.5  # nicht planbare Biome dunkel
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
    ap = argparse.ArgumentParser(description='Eldarien Heide/Tundra-Planer (Ebene heide_tundra: Boden, Sonderformen Mittel, Baeume, Wasserkante)')
    ap.add_argument('felder', nargs='+', help='Gitterfelder, z. B. D2 G5')
    ap.add_argument('--bild', action='store_true', help='Draufsicht PNG nach docs/pruefung/heide_tundra/')
    ap.add_argument('--faktor', type=float, default=1.0, help='globaler Dichtefaktor')
    ap.add_argument('--basis', default='.', help='production-Wurzel (Standard: aktuelles Verzeichnis)')
    ap.add_argument('--regeln', default=None, help='Regeln-JSON (Standard: heide_tundra_regeln.json neben dem Skript)')
    ap.add_argument('--entfernen', default=None, help='Netznamen-Praefixe alter Instanzen fuer plan.json["entfernen"] (nicht in Wuestenfeldern)')
    args = ap.parse_args()
    skript_dir = os.path.dirname(os.path.abspath(__file__))
    rp = args.regeln or os.path.join(skript_dir, 'heide_tundra_regeln.json')
    if not os.path.isfile(rp):
        abbruch('Regeldatei fehlt: %s' % rp)
    try:
        regeln = json.load(open(rp, encoding='utf-8'))
    except Exception as ex:
        abbruch('Regeldatei %s nicht lesbar: %s' % (rp, ex))
    basis = os.path.abspath(args.basis)
    if not os.path.isfile(os.path.join(basis, WELT, 'hoehe.f32')):
        abbruch('hoehe.f32 fehlt unter %s - --basis auf die production-Wurzel setzen' % os.path.join(basis, WELT))
    meld('numba %s, NumPy %s, Regeln %s (Seed %d)' % ('vorhanden' if NUMBA else 'nicht vorhanden (nicht noetig)', np.__version__, rp,
                                                       regeln.get('seed', 0)))
    inv, kante = lade_inventar(basis, skript_dir)
    pruefe_paletten(regeln, inv, kante)
    for feld in args.felder:
        try:
            plane_feld(feld, basis, skript_dir, json.loads(json.dumps(regeln)), args.faktor, args.bild, inv, args.entfernen)
        except MemoryError:
            abbruch('Speicher reicht nicht fuer Feld %s' % feld)


if __name__ == '__main__':
    main()
