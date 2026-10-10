#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dschungel_plan.py – Planer „Dschungel inkl. Karst-Kalktürme“ (Auftrag 11, Teil B7) für Eldarien (UE 5.8.3, 1-m-Raster 9577 × 7057).
Stand: Korrektur Runde 1 (10.10.2026) nach antworten/verteilung-KONVENTIONEN.md §1–§5.

Korrektur Runde 3b: `entfernen` (Witcher-Lianen sm_vines_01a, keine Bäume) nur mit Freigabe (--ersetzen oder Regel entfernen_aktiv,
Standard aus); ohne Freigabe bleibt plan.json["entfernen"] leer und die Kandidaten stehen mit Zahl in plan.json["entfernen_vorschlag"].
Mit Freigabe nur, wenn die Landzellen des Feldes >= zustaendigkeit.entfernen_min_anteil_land Dschungel sind und <= entfernen_max_fremd_anteil
der Kandidaten in Saum-/Fremdzellen stehen (der Filter des Setzers gilt feldweit). Die Bäume der Witcher-/Bestand-Ebene bleiben immer.

*** UNGETESTET MIT ECHTDATEN *** – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern (H6, G4, G5) rauchgetestet.
Korrekturen bitte als auftraege/verteilung-dschungel-korrektur.md.

Zuständigkeit (Konventionen §1)
-------------------------------
Biom je Zelle = eigner.r8 + welt.json["kacheln"][k]["rezept"]; Kennzahl 0 (Weltgelände) → aue, Vulkanregion → lava. Nur wenn
eigner.r8/welt.json fehlen, gilt das dominante Feldbiom aus daten/biome_je_feld.json (Hinweis im Log). biome_eigen = [dschungel]:
bebaut werden nur Dschungel-Zellen plus ein 30-m-Saum (Dichtefaktor 1 an der Grenze, linear auf 0 bei 30 m außerhalb,
Distanztransformation). Anteil der eigenen Biome im Fenster (Feld + Rand) < 2 % → leerer plan.json (instanzen 0, keine f32).

Was das Skript tut (Ebenen-Abgrenzung, Konventionen §4)
-------------------------------------------------------
Plant je Gitterfeld vier Schichten als Foliage-Instanzen (HISM):
  2 baum         Emergenten/Laubriesen (AsianTemple), Palmen (Bazaar, Palms_Pack), Jungpalmen – sehr dicht in Kernen,
                 Lichtungen (Wertrauschen 110 m, 16 %) und lichte Karstfüße
  1 mittel       NUR Dschungel-Sonderformen: Lianen/Efeu an Stämmen der eigenen Laubbäume (Epiphyten-Ersatz, Satelliten),
                 Kletterpflanzen in Karstspalten und Steilwänden 40–78°, Moospolster (Karstfuß, Wurzeln, Steilhänge bis 75°)
  0 boden        Laubstreu, Bodendecker, Zweige, Keimlinge, Blüteninseln
  5 wasserkante  Moossteine, Uferfarne, Schilf/Rohrkolben, Schachtelhalm im Band 0,3–7 m am Wasser
Die generischen Mittelschicht-Klassen (farn, strauch, jungbaum, hochstaude, grasbueschel, totholz_liegend/stumpf/ast, pilz, beere)
setzt mittelschicht_plan.py (Teil D) mit der Dschungel-Palette aus `mittelschicht_overrides` in dschungel_regeln.json (inkl.
Zusatzklassen Riesenfarn-Inseln, Staudenflur, Bananen-Ersatz). Schicht 3 fels (Karsttürme als Akteure, Moosblöcke, Karstplatten) und
4 spuren (Tempelruine, Pfad) planen Teil C/D mit `felsgruppen_overrides` / `spuren_overrides`; dieses Skript liefert dafür in plan.json
`karst` (Wand-/Fußzellen, Türme) und `blickziele` (Karstturm, Wasserfall, Doline, Tempelruinen-Standort, nur auf Dschungel-Zellen).

Dichte je Zelle = Kern-Dichte · Zuständigkeit (Biom + Saum) · Lage (lage_*.r8) · Licht (Beschattung aus Kronendach: bestand/,
witcher/, instanzen.json, eigene Bäume) · Hang · Höhenstufe (Talboden/Hang/Karst) · Karstlage (Fuß/Spalte/Gipfel/Wand) ·
Gruppen-Wertrauschen · Wasser-/Weg-/Ort-Abstände. Streuung über gejitterte Gitterzellen (Zellgröße ≈ Mindestabstand);
Zufall = Hash aus (Weltraster-Koordinate, Seed, Kanal) → deterministisch, Nachbarfelder nahtlos (Fenster Feld + 64 m).

Budget (Konventionen §3): ≤ 60 000 Instanzen je Feld (Ziel 50 000), ≤ 3 000 mit Kollision – erst proportionale Hash-Ausdünnung
nach Priorität, dann exakte Kappung; Satelliten (Lianen) werden erst nach der Baum-Ausdünnung erzeugt (keine verwaisten Lianen).

Aufruf
------
  python -I scripts/dschungel/dschungel_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD] [--ersetzen]
  --ersetzen Freigabe fuer den entfernen-Filter (Standard aus: entfernen leer, Kandidaten in entfernen_vorschlag)
  --basis   production-Wurzel (Default "."), darunter export/unreal/welt/, daten/netze.csv, daten/biome_je_feld.json, docs/
  --regeln  Regeldatei (Default: dschungel_regeln.json neben dem Skript)
  --faktor  Dichtefaktor auf alle Klassen (Budget bleibt)
  --bild    Draufsicht docs/pruefung/dschungel/<Feld>.png (1 px = 1 m, Farben je Klasse, Karstwand weiß)
Exit-Code 2 bei fehlender Pflichtdatei (hoehe.f32, Regeln) oder unbekanntem Feld. Alle Log-Zeilen nur ASCII (Konventionen §5).

Ein-/Ausgabe (FORMAT.md §1–§5)
-----------------------------
Liest:    export/unreal/welt/hoehe.f32 (np.memmap, nur Fenster), lage_<Name>.r8 (optional), karte_wasser/weg/ort.r8 (optional),
          eigner.r8 + welt.json (sonst daten/biome_je_feld.json), bestand/<Feld>/, witcher/<Feld>/ (+ 8 Nachbarn),
          instanzen/instanzen.json (+ instanzen/<name>.f32, optional), docs/staedte/standorte.json (optional), daten/netze.csv.
Schreibt: export/unreal/welt/dschungel/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm; qx,qy,qz,qw; sx,sy,sz)
          export/unreal/welt/dschungel/<Feld>/plan.json (FORMAT §3: stand, feld, instanzen, dateien{pfad, anzahl, gruppe, rolle,
          sichtweite, schatten, kollision, ebene}, entfernen, ft_ordner, ft_praefix; Konventionen §2: biome_fenster,
          zellen_zustaendig, biome_eigen, kollision_anzahl; dazu statistik, karst, blickziele, hinweise)
          docs/pruefung/dschungel/<Feld>.png bei --bild.
Nur NumPy (numba optional, wird nicht benötigt); Laufzeit-Ziel ≤ 60 s je Feld.

Quellen: vorlagen/FORMAT.md; antworten/verteilung-KONVENTIONEN.md; antworten/assets-taxonomie.md (Paletten/Lücken dschungel);
antworten/bildkritik-witcher-messlatte.md (Größenstaffelung, Lichtungen 15–25 %, Waldkanten-Falloff); antworten/klippennetze-a5.md
(Eingraben 25–45 %, Gruppen 2–5); UN-REDD 2011 „Forest ecological stratification Vietnam“ (Kalkwald < 700 m: fünfstöckig, Oberstand
> 40 m; auf Kalk 1–2 Stockwerke 8–15 m); UNEP-WCMC South China Karst (Sukzession Moos/Flechte → Kraut → Strauch → Wald);
Azoren-Laurisilva-Feldführer (dicht, Epiphyten, Farnkrautschicht); Yakushima-Reiseführer (> 100 Moosarten auf Granitblöcken).
"""
import argparse
import csv
import json
import math
import os
import sys
import time

import numpy as np

try:  # numba optional – nur Meldung, alles läuft rein mit NumPy
    import numba  # noqa: F401
    NUMBA = True
except Exception:  # pragma: no cover
    NUMBA = False

NX, NY = 9577, 7057
FELD_M = 1008
X0, Y0 = 4730.5, 4060.5          # X_cm = (j − 4730,5)·100, Y_cm = (i − 4060,5)·100
WELT = os.path.join('export', 'unreal', 'welt')
SCHICHTEN = ('2 baum', '1 mittel', '0 boden', '5 wasserkante')
BAUM_WORTE = ('baum', 'tree', 'palm', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'eiche', 'weide', 'pappel', 'hainbuche', 'hornbeam', 'beech', 'pine', 'poplar', 'willow')


ASCII_ERSATZ = (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('Ä', 'Ae'), ('Ö', 'Oe'), ('Ü', 'Ue'), ('ß', 'ss'), ('–', '-'), ('—', '-'),
                ('→', '->'), ('←', '<-'), ('…', '...'), ('≤', '<='), ('≥', '>='), ('°', ' Grad'), ('×', 'x'), ('²', '2'), ('·', '*'),
                ('„', '"'), ('“', '"'), ('”', '"'), ('‚', "'"), ('‘', "'"), ('’', "'"), ('±', '+-'), ('≈', '~'), ('µ', 'u'))


def ascii_text(s):
    """Log-Text nur ASCII (Konventionen §5: Logs werden unter Windows mit cp1252 weiterverarbeitet)."""
    s = str(s)
    for a, b in ASCII_ERSATZ:
        s = s.replace(a, b)
    return s.encode('ascii', 'replace').decode('ascii')


def meld(*a):
    print(ascii_text(' '.join(['[dschungel]'] + [str(x) for x in a])), flush=True)


def abbruch(text, code=2):
    """Klare Meldung, Exit-Code 2 (fehlende Pflichtdatei, unbekanntes Feld)."""
    meld('FEHLER: ' + text)
    sys.exit(code)


# ----------------------------------------------------------------------------- Raster-Helfer
def feld_fenster(feld, rand):
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        abbruch('Unbekanntes Feld %r (A1 ... J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        abbruch('Unbekanntes Feld %r (A1 ... J7)' % feld)
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX)   # J-Spalte: 9072..9577 (geklippt)
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY)
    win = (max(0, i0 - rand), min(NY, i1 + rand), max(0, j0 - rand), min(NX, j1 + rand))
    return (i0, i1, j0, j1), win


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
            abbruch('Pflichtdatei %s hat falsche Groesse' % pfad)
        return None
    mm = np.memmap(pfad, dtype=dtype, mode='r', shape=(NY, NX))
    return np.array(mm[wi0:wi1, wj0:wj1])


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


def minmax_filter(a, r, op):
    """Separierbares Min-/Max-Filter (Fenster 2r+1) über Verschiebungen."""
    out = a.copy()
    for d in range(1, r + 1):
        out = op(out, verschiebe(a, d, 0, a[0, 0]))
        out = op(out, verschiebe(a, -d, 0, a[0, 0]))
    b = out.copy()
    for d in range(1, r + 1):
        out = op(out, verschiebe(b, 0, d, b[0, 0]))
        out = op(out, verschiebe(b, 0, -d, b[0, 0]))
    return out


def distanz(mask, max_m=64.0):
    """Euklidische Distanz (m) zur nächsten True-Zelle (Jump-Flooding, vektorisiert); > max_m → 2·max_m."""
    H, W = mask.shape
    fern = np.float32(max_m * 2.0)
    if not mask.any():
        return np.full((H, W), fern, np.float32)
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


def wertrauschen(win, wl, seed, kanal):
    """Wertrauschen 0–1 (zwei Oktaven) auf Weltkoordinaten, bilinear mit Smoothstep – nahtlos über Feldgrenzen."""
    wi0, wi1, wj0, wj1 = win
    ii, jj = np.indices((wi1 - wi0, wj1 - wj0), dtype=np.float32)
    ii += wi0
    jj += wj0
    out = np.zeros_like(ii)
    for ok, (w, amp) in enumerate(((wl, 1.0), (wl / 2.0, 0.35))):
        gi, gj = ii / w, jj / w
        i0, j0 = np.floor(gi).astype(np.int64), np.floor(gj).astype(np.int64)
        ti, tj = gi - i0, gj - j0
        ti = ti * ti * (3 - 2 * ti)
        tj = tj * tj * (3 - 2 * tj)
        k = kanal * 4 + ok
        a = hash01(i0, j0, seed, k)
        b = hash01(i0, j0 + 1, seed, k)
        c = hash01(i0 + 1, j0, seed, k)
        d = hash01(i0 + 1, j0 + 1, seed, k)
        out += amp * ((a * (1 - tj) + b * tj) * (1 - ti) + (c * (1 - tj) + d * tj) * ti)
    return (out / 1.35).astype(np.float32)


def bilinear(h, fi, fj):
    H, W = h.shape
    fi = np.clip(fi, 0, H - 1.001)
    fj = np.clip(fj, 0, W - 1.001)
    i0 = fi.astype(np.int32)
    j0 = fj.astype(np.int32)
    ti = (fi - i0).astype(np.float32)
    tj = (fj - j0).astype(np.float32)
    return ((h[i0, j0] * (1 - ti) + h[i0 + 1, j0] * ti) * (1 - tj) + (h[i0, j0 + 1] * (1 - ti) + h[i0 + 1, j0 + 1] * ti) * tj)


def quat_mul(a, b):
    ax, ay, az, aw = a.T
    bx, by, bz, bw = b.T
    return np.stack([aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
                     aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz], axis=1)


def quaternionen(nx, ny, nz, kippen, yaw):
    """Z-Achse um Anteil `kippen` auf die Geländenormale kippen, davor Zufalls-Yaw → (n,4) x,y,z,w."""
    n = len(nx)
    tz = (1 - kippen) + kippen * nz
    tx, ty = kippen * nx, kippen * ny
    l = np.sqrt(tx * tx + ty * ty + tz * tz) + 1e-9
    tx, ty, tz = tx / l, ty / l, tz / l
    qt = np.stack([-ty, tx, np.zeros(n, np.float32), 1 + tz], axis=1)
    qt /= (np.linalg.norm(qt, axis=1, keepdims=True) + 1e-9)
    qy = np.stack([np.zeros(n, np.float32), np.zeros(n, np.float32), np.sin(yaw / 2), np.cos(yaw / 2)], axis=1)
    q = quat_mul(qt, qy)
    return (q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-9)).astype(np.float32)


# ----------------------------------------------------------------------------- Inventar / Regeln
def lade_inventar(basis):
    """daten/netze.csv → {pfad: {'z': Höhe m, 'nanite': bool, 'koll': int}} (None, wenn fehlt)."""
    p = os.path.join(basis, 'daten', 'netze.csv')
    if not os.path.isfile(p):
        meld('Hinweis: %s fehlt – Netzpfade werden nicht geprüft' % p)
        return None
    inv = {}
    with open(p, encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f, delimiter=';'):
            try:
                inv[row['pfad']] = {'z': float(row.get('groesse_z_m') or 0), 'nanite': row.get('nanite') == '1', 'koll': int(row.get('kollision_primitive') or 0)}
            except Exception:
                continue
    return inv


def pruefe_klassen(regeln, inv, hinweise):
    """Pfade normieren (/Game/ ergänzen), gegen Inventar prüfen, fehlende Netze streichen."""
    for kname, kl in regeln['klassen'].items():
        if kname.startswith('_'):
            continue
        gut = []
        for p in kl['netze']:
            p = p if p.startswith('/Game/') else '/Game/' + p
            if inv is not None and p not in inv:
                hinweise.append('Netz fehlt im Inventar, gestrichen: %s (Klasse %s)' % (p, kname))
                continue
            gut.append(p)
        kl['netze'] = gut
        if not gut:
            hinweise.append('Klasse %s hat kein gültiges Netz – wird übersprungen' % kname)
        if 'hoehe_m' not in kl:
            kl['hoehe_m'] = max([inv[p]['z'] for p in gut if inv and p in inv] or [1.0])


# ----------------------------------------------------------------------------- Weltdaten
def dominantes_feldbiom(basis, feld, namen):
    """Nur wenn eigner.r8/welt.json fehlen: dominantes Biom des Feldes aus daten/biome_je_feld.json, sonst aue."""
    skript_dir = os.path.dirname(os.path.abspath(__file__))
    for k in (os.path.join(basis, 'daten', 'biome_je_feld.json'), os.path.join(skript_dir, 'biome_je_feld.json')):
        if not os.path.isfile(k):
            continue
        try:
            d = json.load(open(k, encoding='utf-8'))
            e = d.get('felder', d).get(feld)
            bp = e.get('biome_prozent') if isinstance(e, dict) else None
            if bp:
                b = str(sorted(bp, key=lambda x: -float(x[1]))[0][0]).lower()
                if b in namen:
                    return b, k
        except Exception as ex:
            meld('Hinweis: %s nicht auswertbar (%s)' % (k, ex))
    return 'aue', 'Standard aue (biome_je_feld.json fehlt)'


def lade_biome(basis, win, namen, feld, hinweise):
    """Biom-Index je Zelle (Konventionen §1): eigner.r8 + welt.json-Rezept; Kennzahl 0 und unbekannte Kennzahlen → aue,
    Rezept mit 'vulkan'/'lava' → lava. Fallback dominantes Feldbiom nur, wenn eigner.r8 oder welt.json fehlen/unlesbar sind."""
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
        fb, quelle = dominantes_feldbiom(basis, feld, namen)
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


def lade_ebene(ordner, win, inv):
    """Instanzen einer gesetzten Ebene im Fenster → Liste (fi, fj, kronenradius_m) für Bäume, sonst (fi, fj) klein."""
    baum, klein = [], []
    pj = os.path.join(ordner, 'plan.json')
    if not os.path.isfile(pj):
        return baum, klein
    try:
        plan = json.load(open(pj, encoding='utf-8'))
    except Exception:
        return baum, klein
    for name, info in plan.get('dateien', {}).items():
        f = os.path.join(ordner, name + '.f32')
        if not os.path.isfile(f):
            continue
        a = np.fromfile(f, dtype='<f4')
        if a.size % 10:
            continue
        a = a.reshape(-1, 10)
        fj = a[:, 0] / 100.0 + X0 - win[2]
        fi = a[:, 1] / 100.0 + Y0 - win[0]
        m = (fi >= 0) & (fi < win[1] - win[0]) & (fj >= 0) & (fj < win[3] - win[2])
        if not m.any():
            continue
        txt = (str(info.get('rolle', '')) + ' ' + str(info.get('gruppe', '')) + ' ' + name).lower()
        ist_baum = any(w in txt for w in BAUM_WORTE) and not any(w in txt for w in ('tot', 'stump', 'log', 'fallen', 'branch', 'root'))
        if ist_baum:
            z = inv[info.get('pfad', '')]['z'] if inv and info.get('pfad', '') in inv else 10.0
            baum.append(np.stack([fi[m], fj[m], a[m, 9] * z], axis=1))
        else:
            klein.append(np.stack([fi[m], fj[m]], axis=1))
    return baum, klein


def lade_fremde_baeume(basis, feld, win, inv, hinweise):
    """Bäume aus bestand/, witcher/ (Feld + 8 Nachbarn) und instanzen/ → (n,3) fi, fj, Höhe m."""
    s, r = ord(feld[0]) - ord('A'), int(feld[1:])
    baum, quellen = [], []
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(ord('A') + ss) + str(rr)
            for ebene in ('bestand', 'witcher'):
                b, _ = lade_ebene(os.path.join(basis, WELT, ebene, nf), win, inv)
                if b:
                    quellen.append('%s/%s' % (ebene, nf))
                    baum += b
    ij = os.path.join(basis, WELT, 'instanzen', 'instanzen.json')
    if not os.path.isfile(ij):
        meld('Hinweis: %s fehlt – Houdini-Bestand wird nicht ins Kronendach gerechnet (optional)' % ij)
    if os.path.isfile(ij):
        try:
            verz = json.load(open(ij, encoding='utf-8')).get('verzeichnis', [])
            for e in verz:
                txt = (str(e.get('klasse', '')) + ' ' + str(e.get('ref', '')) + ' ' + str(e.get('name', ''))).lower()
                if not any(w in txt for w in BAUM_WORTE):
                    continue
                g = e.get('grenzen_cm')
                if g and len(g) >= 4:
                    gj0, gj1 = min(g[0], g[2]) / 100.0 + X0, max(g[0], g[2]) / 100.0 + X0
                    gi0, gi1 = min(g[1], g[3]) / 100.0 + Y0, max(g[1], g[3]) / 100.0 + Y0
                    if gj1 < win[2] or gj0 > win[3] or gi1 < win[0] or gi0 > win[1]:
                        continue
                f = os.path.join(basis, WELT, 'instanzen', str(e.get('name', '')) + '.f32')
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
                    z = inv[e.get('ref', '')]['z'] if inv and e.get('ref', '') in inv else 12.0
                    baum.append(np.stack([fi[m], fj[m], a[m, 9] * z], axis=1))
                    quellen.append('instanzen/' + str(e.get('name', '')))
        except Exception as ex:
            hinweise.append('instanzen.json nicht nutzbar: %s' % ex)
    if quellen:
        meld('Fremde Bäume aus:', ', '.join(quellen[:12]), '…' if len(quellen) > 12 else '')
    else:
        hinweise.append('Keine gesetzten Baum-Ebenen (bestand/witcher/instanzen) gefunden – Kronendach nur aus eigener Baumschicht')
    return np.concatenate(baum, axis=0) if baum else np.zeros((0, 3), np.float32)


def lade_standorte(basis, win):
    """docs/staedte/standorte.json (nur lokal) → Maske frei zu haltender Zellen (Kreis radius_m, Default 60 m)."""
    p = os.path.join(basis, 'docs', 'staedte', 'standorte.json')
    H, W = win[1] - win[0], win[3] - win[2]
    m = np.zeros((H, W), bool)
    if not os.path.isfile(p):
        return m
    try:
        d = json.load(open(p, encoding='utf-8'))
        eintraege = d.get('standorte', d) if isinstance(d, dict) else d
        if isinstance(eintraege, dict):
            eintraege = list(eintraege.values())
        ii, jj = np.indices((H, W), dtype=np.float32)
        for e in eintraege:
            if not isinstance(e, dict):
                continue
            pos = e.get('position', e.get('pos', e))
            x = pos.get('x_cm', pos.get('x')) if isinstance(pos, dict) else pos[0]
            y = pos.get('y_cm', pos.get('y')) if isinstance(pos, dict) else pos[1]
            if x is None or y is None:
                continue
            rad = float(e.get('radius_m', 60.0))
            fj = float(x) / 100.0 + X0 - win[2]
            fi = float(y) / 100.0 + Y0 - win[0]
            m |= (ii - fi) ** 2 + (jj - fj) ** 2 <= rad * rad
    except Exception as ex:
        meld('Hinweis: standorte.json nicht lesbar (%s) – ignoriert' % ex)
    return m


# ----------------------------------------------------------------------------- Kronendach
def kronendach(baeume, H, W, regeln):
    """Beschattung 0–1 aus Baumliste (fi, fj, Höhe m): Kronenscheiben je Radius-Stufe, Zählung, 1 − exp(−k·n)."""
    L = regeln['licht']
    zaehl = np.zeros((H, W), np.float32)
    if baeume.shape[0] == 0:
        return zaehl
    r = np.clip(baeume[:, 2] * L['kronen_faktor'], L['kronen_radius_min_m'], L['kronen_radius_max_m'])
    ri = np.clip(np.round(r).astype(np.int32), 1, int(L['kronen_radius_max_m']))
    mi = np.clip(np.round(baeume[:, 0]).astype(np.int32), 0, H - 1)
    mj = np.clip(np.round(baeume[:, 1]).astype(np.int32), 0, W - 1)
    for rad in np.unique(ri):
        m = np.zeros((H, W), bool)
        sel = ri == rad
        m[mi[sel], mj[sel]] = True
        zaehl += dilate(m, int(rad)).astype(np.float32)
    zaehl = gauss_blur(zaehl, 1.5)
    return (1.0 - np.exp(-L['k'] * zaehl)).astype(np.float32)


# ----------------------------------------------------------------------------- Streuung
def streue(lam, zell, seed, kanal, wi0, wj0):
    """Gejittertes Weltgitter (Zelle zell m): je Zelle ein Kandidat, Annahme mit p = lam·zell²; p > 1 → mehrere Durchläufe."""
    H, W = lam.shape
    zell = max(1, int(zell))
    pmax = float(lam.max()) * zell * zell if lam.size else 0.0
    if pmax <= 0:
        return np.zeros(0, np.float32), np.zeros(0, np.float32)
    n_pass = int(min(6, max(1, math.ceil(pmax))))
    ci = np.arange(wi0 // zell, (wi0 + H + zell - 1) // zell + 1, dtype=np.int64)
    cj = np.arange(wj0 // zell, (wj0 + W + zell - 1) // zell + 1, dtype=np.int64)
    CI, CJ = np.meshgrid(ci, cj, indexing='ij')
    CI, CJ = CI.ravel(), CJ.ravel()
    outi, outj = [], []
    for k in range(n_pass):
        u = hash01(CI, CJ, seed, kanal * 16 + 3 * k + 1)
        v = hash01(CI, CJ, seed, kanal * 16 + 3 * k + 2)
        fi = (CI + u) * zell - wi0
        fj = (CJ + v) * zell - wj0
        ok = (fi >= 0) & (fi < H) & (fj >= 0) & (fj < W)
        fi, fj, ci_, cj_ = fi[ok], fj[ok], CI[ok], CJ[ok]
        p = lam[fi.astype(np.int32), fj.astype(np.int32)] * (zell * zell) / n_pass
        an = hash01(ci_, cj_, seed, kanal * 16 + 3 * k + 3) < p
        outi.append(fi[an].astype(np.float32))
        outj.append(fj[an].astype(np.float32))
    return np.concatenate(outi), np.concatenate(outj)


def licht_faktor(b, kurve):
    """Faktor aus Beschattung b (0–1) über 4 Stützstellen (linear)."""
    k = np.asarray(kurve, np.float32)
    x = np.clip(b, 0, 1) * 3.0
    i0 = np.clip(x.astype(np.int32), 0, 2)
    t = x - i0
    return (k[i0] * (1 - t) + k[i0 + 1] * t).astype(np.float32)


# ----------------------------------------------------------------------------- Hauptplanung
def pruefe_entfernen(kand, regeln, inv):
    """Runde 3b: ein entfernen-Praefix bleibt nur, wenn jedes Inventarnetz, das mit ihm beginnt, ein Netz dieses Planers ist
    (der feldweite Netznamen-Filter darf nur ersetzen, was der Planer selbst neu setzt). Ohne Inventar: Praefixe ungeprueft."""
    if not kand or inv is None:
        return list(kand), []
    eigen = set()
    for kname, kl in regeln['klassen'].items():
        if not kname.startswith('_'):
            eigen |= {str(n).rsplit('/', 1)[-1].lower() for n in kl.get('netze', [])}
    namen = sorted({str(q).rsplit('/', 1)[-1].lower() for q in inv})
    gut, warn = [], []
    for p in kand:
        treffer = [n for n in namen if n.startswith(p)]
        fremd = [n for n in treffer if n not in eigen]
        if fremd or not treffer:
            warn.append('entfernen-Praefix %r verworfen (%s)' % (p, ('traefe fremde Netze: ' + ', '.join(fremd[:6])) if fremd else 'kein Inventarnetz'))
        else:
            gut.append(p)
    return gut, warn


def zaehle_entfernen(basis, feld, win, praefixe, eigen, zust_m, land_m, im_feld):
    """Runde 3b: alte Instanzen (witcher/ + bestand/, Feld + 8 Nachbarn, Position im Feld), deren Netzname mit einem Praefix beginnt;
    getrennt nach eigenen Biomzellen, Saum und fremden Zellen."""
    out = {'gesamt': 0, 'eigen': 0, 'saum': 0, 'fremd': 0, 'wasser': 0, 'je_netz': {}, 'je_ebene': {}}
    if not praefixe:
        return out
    H, W = eigen.shape
    s, r = ord(feld[0]) - ord('A'), int(feld[1:])
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(ord('A') + ss) + str(rr)
            for ebene in ('bestand', 'witcher'):
                ordner = os.path.join(basis, WELT, ebene, nf)
                pj = os.path.join(ordner, 'plan.json')
                if not os.path.isfile(pj):
                    continue
                try:
                    plan = json.load(open(pj, encoding='utf-8'))
                except Exception:
                    continue
                for name in sorted(plan.get('dateien', {})):
                    if not any(name.lower().startswith(p) for p in praefixe):
                        continue
                    f = os.path.join(ordner, name + '.f32')
                    if not os.path.isfile(f):
                        continue
                    a = np.fromfile(f, dtype='<f4')
                    if a.size == 0 or a.size % 10:
                        continue
                    a = a.reshape(-1, 10)
                    fi = a[:, 1] / 100.0 + Y0 - win[0]
                    fj = a[:, 0] / 100.0 + X0 - win[2]
                    ii = np.clip(np.round(fi).astype(np.int64), 0, H - 1)
                    jj = np.clip(np.round(fj).astype(np.int64), 0, W - 1)
                    m = im_feld[ii, jj] & (fi >= -0.5) & (fi < H - 0.5) & (fj >= -0.5) & (fj < W - 0.5)
                    if not m.any():
                        continue
                    ii, jj = ii[m], jj[m]
                    e = eigen[ii, jj]
                    sm = ~e & zust_m[ii, jj]
                    n = int(m.sum())
                    for k, v in (('gesamt', n), ('eigen', int(e.sum())), ('saum', int(sm.sum())), ('fremd', int((~e & ~sm).sum())),
                                 ('wasser', int((~land_m[ii, jj]).sum()))):
                        out[k] += v
                    out['je_netz'][name] = out['je_netz'].get(name, 0) + n
                    out['je_ebene'][ebene] = out['je_ebene'].get(ebene, 0) + n
    out['je_netz'] = dict(sorted(out['je_netz'].items()))
    return out


def schreibe_leerplan(feld, ausgabe, regeln, biome_fenster, anteil_eigen, ds_anteil, biom_quelle, hinweise, t0):
    """Konventionen §1: Eigenanteil < min_anteil_fenster -> leerer plan.json (instanzen 0, keine f32), nie Text statt plan.json."""
    Z = regeln['zustaendigkeit']
    os.makedirs(ausgabe, exist_ok=True)
    for f in os.listdir(ausgabe):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    hinweise.append('Anteil eigener Biome %s im Fenster %.4f < %.2f - kein Plan' % (Z['biome_eigen'], anteil_eigen, Z['min_anteil_fenster']))
    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': 0, 'dateien': {}, 'entfernen': '',
            'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'biome_fenster': biome_fenster, 'zellen_zustaendig': 0, 'biome_eigen': list(Z['biome_eigen']), 'kollision_anzahl': 0,
            'statistik': {'je_klasse': {}, 'anteil_eigen_fenster': round(anteil_eigen, 4), 'dschungel_anteil_feld': round(ds_anteil, 4),
                          'biom_quelle': biom_quelle, 'laufzeit_s': round(time.time() - t0, 1)},
            'hinweise': hinweise, 'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet (UNGETESTET MIT ECHTDATEN)'}
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s: Anteil %s im Fenster %.2f %% < %.0f %% - leerer plan.json (instanzen 0)' % (
        feld, '/'.join(Z['biome_eigen']), 100 * anteil_eigen, 100 * Z['min_anteil_fenster']))
    return plan


def plane_feld(feld, basis, regeln, faktor, bild, ersetzen=False):
    t0 = time.time()
    hinweise = []
    seed = int(regeln['seed'])
    rand = int(regeln.get('fenster_rand_m', 64))
    fb_, win = feld_fenster(feld, rand)
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    ausgabe = os.path.join(basis, WELT, regeln.get('ausgabe_ordner', 'dschungel'), feld)
    im_feld = np.zeros((H, W), bool)
    im_feld[fb_[0] - wi0:fb_[1] - wi0, fb_[2] - wj0:fb_[3] - wj0] = True

    # --- Höhe (Pflicht) und Zuständigkeit nach Biom-Zellen (Konventionen §1)
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), np.float32, win, pflicht=True)
    namen = regeln['biome']
    Z = regeln['zustaendigkeit']
    eigen_idx = [namen.index(b) for b in Z['biome_eigen'] if b in namen]
    bio, biom_quelle = lade_biome(basis, win, namen, feld, hinweise)
    werte, zahl = np.unique(bio, return_counts=True)
    biome_fenster = {namen[int(k)]: round(float(c) / bio.size, 4) for k, c in sorted(zip(werte, zahl), key=lambda x: -x[1])}
    eigen = np.isin(bio, eigen_idx)
    anteil_eigen = float(eigen.mean())
    ds_anteil = float(eigen[im_feld].mean())
    if anteil_eigen < float(Z['min_anteil_fenster']):
        return schreibe_leerplan(feld, ausgabe, regeln, biome_fenster, anteil_eigen, ds_anteil, biom_quelle, hinweise, t0)
    saum_m = float(Z['saum_m'])
    if eigen.all():
        zust = np.ones((H, W), np.float32)
    else:
        d_eigen = distanz(eigen, max(64.0, 2 * saum_m))
        zust = np.where(eigen, 1.0, np.clip(1.0 - d_eigen / saum_m, 0, 1)).astype(np.float32)
    zellen_zustaendig = int(((zust > 0) & im_feld).sum())
    meld('%s: Biome im Fenster %s, eigen %.1f %%, zustaendig %d Zellen im Feld (inkl. Saum %d m)' % (
        feld, {k: v for k, v in list(biome_fenster.items())[:4]}, 100 * anteil_eigen, zellen_zustaendig, int(saum_m)))

    feld_info = regeln['felder'].get(feld, {'dschungel': 0.0, 'karst': False, 'entfernen': ''})
    if feld not in regeln['felder']:
        hinweise.append('Feld %s steht nicht in regeln["felder"] - geplant mit Biom-Maske aus eigner.r8, ohne entfernen/Karst' % feld)
    karstfeld = bool(feld_info.get('karst', False))
    inv = lade_inventar(basis)
    pruefe_klassen(regeln, inv, hinweise)

    # --- Hang, Normale, Relief
    hs = gauss_blur(hoehe, 1.0)
    dzdi = (verschiebe(hs, 1, 0, 0) - verschiebe(hs, -1, 0, 0)) * 0.5
    dzdj = (verschiebe(hs, 0, 1, 0) - verschiebe(hs, 0, -1, 0)) * 0.5
    dzdi[0, :] = dzdi[-1, :] = 0
    dzdj[:, 0] = dzdj[:, -1] = 0
    hang = np.degrees(np.arctan(np.sqrt(dzdi * dzdi + dzdj * dzdj))).astype(np.float32)
    hang3 = minmax_filter(hang, 1, np.maximum)   # steilste Zelle im 3×3-Umfeld: Nicht-Kletterer meiden auch Wandkanten
    nl = np.sqrt(dzdi * dzdi + dzdj * dzdj + 1.0)
    n_x, n_y, n_z = (-dzdj / nl).astype(np.float32), (-dzdi / nl).astype(np.float32), (1.0 / nl).astype(np.float32)
    Hh = regeln['hoehe']
    rel_r = int(Hh['relief_umkreis_m'] // 2)
    hmin_lokal = minmax_filter(hs, rel_r, np.minimum)
    relief = (hs - hmin_lokal).astype(np.float32)

    # --- Masken
    wasser = lade_raster(os.path.join(basis, WELT, 'karte_wasser.r8'), np.uint8, win)
    weg = lade_raster(os.path.join(basis, WELT, 'karte_weg.r8'), np.uint8, win)
    ort = lade_raster(os.path.join(basis, WELT, 'karte_ort.r8'), np.uint8, win)
    for nm, a in (('karte_wasser', wasser), ('karte_weg', weg), ('karte_ort', ort)):
        if a is None:
            hinweise.append('%s.r8 fehlt – ohne %s geplant' % (nm, nm.split('_')[1]))
    wasser_m = (wasser > 0) if wasser is not None else np.zeros((H, W), bool)
    weg_m = (weg > 0) if weg is not None else np.zeros((H, W), bool)
    ort_m = (ort > 0) if ort is not None else np.zeros((H, W), bool)
    meer = (hoehe <= 0.05)
    d_wasser = distanz(wasser_m | meer, 64)
    d_weg = distanz(weg_m, 32)
    d_ort = distanz(ort_m, 32)
    standorte = lade_standorte(basis, win)
    A = regeln['abstand_m']
    sperre_klein = wasser_m | meer | (d_weg < A['weg_klein']) | (d_ort < A['ort']) | standorte | (d_wasser < A['wasser_klein'])
    sperre_gross = wasser_m | meer | (d_weg < A['weg_gross']) | (d_ort < A['ort']) | standorte | (d_wasser < A['wasser_gross'])
    biom_f = zust

    # --- Lagen
    lagen_namen = sorted({n for g in regeln['lagen'].values() if isinstance(g, dict) for n in g})
    lagen = {}
    for n in lagen_namen:
        a = lade_raster(os.path.join(basis, WELT, 'lage_%s.r8' % n), np.uint8, win)
        if a is not None:
            lagen[n] = a.astype(np.float32) / 255.0
    if not lagen:
        hinweise.append('Keine lage_*.r8 gefunden – Lagenfaktor = %.2f überall' % regeln['lagen']['ohne_lagen'])
    lagen_f = {}
    for gname, gew in regeln['lagen'].items():
        if not isinstance(gew, dict):
            continue
        if not lagen:
            lagen_f[gname] = np.full((H, W), regeln['lagen']['ohne_lagen'], np.float32)
            continue
        num = np.zeros((H, W), np.float32)
        den = np.zeros((H, W), np.float32)
        for n, w in gew.items():
            if n in lagen:
                num += w * lagen[n]
                den += lagen[n]
        lagen_f[gname] = np.where(den > 0.05, num / np.maximum(den, 1e-3), regeln['lagen']['ohne_lagen']).astype(np.float32)

    # --- Karst
    K = regeln['karst']
    wand = hang > K['wand_grad']
    d_wand = distanz(wand, 64)
    fuss = (d_wand <= K['fuss_m']) & (hang < K['fuss_hang_max']) & ~wand
    spalte = (hang >= K['spalte_grad'][0]) & (hang <= K['spalte_grad'][1])
    steilwand = hang > K['spalte_grad'][1]
    gipfel = (relief > K['gipfel_relief_m']) & (hang < K['gipfel_hang_max']) & (d_wand <= K['gipfel_wand_m']) & ~fuss
    wand_feld = wand & im_feld & eigen
    n_wand = int(wand_feld.sum())
    turm = n_wand >= K['turm_min_zellen'] and (float(hoehe[wand_feld].max() - hoehe[wand_feld].min()) if n_wand else 0.0) >= K['turm_min_hoehenspanne_m']
    if karstfeld and not turm:
        hinweise.append('Karstfeld ohne Wandzellen > %d° im Feld (%d Zellen) – keine Karst-Lagen wirksam' % (K['wand_grad'], n_wand))

    # --- Höhenstufen
    wk = np.clip((relief - Hh['karst_relief_m']) / 15.0, 0, 1)
    wt = np.clip((Hh['talboden_max_m'] - hoehe) / 10.0, 0, 1) * (1 - wk)
    wh = 1.0 - wt - wk

    # --- Lichtung und Kronendach
    L = regeln['licht']
    licht_r = wertrauschen(win, L['lichtung']['wellenlaenge_m'], seed, 901)
    schwelle = float(np.quantile(licht_r, L['lichtung']['anteil']))
    lichtung = licht_r < schwelle
    fremd = lade_fremde_baeume(basis, feld, win, inv, hinweise)
    baeume_alle = [fremd]
    beschattung = kronendach(fremd, H, W, regeln)
    belegt_gross = np.zeros((H, W), bool)
    if fremd.shape[0]:
        belegt_gross[np.clip(np.round(fremd[:, 0]).astype(np.int32), 0, H - 1), np.clip(np.round(fremd[:, 1]).astype(np.int32), 0, W - 1)] = True
    belegt_gross = dilate(belegt_gross, A['baum_fremd_gross'])

    rauschen = {}

    def gruppe_f(name):
        if name not in rauschen:
            g = regeln['gruppen'][name]
            r = wertrauschen(win, g['wellenlaenge_m'], seed, 100 + list(regeln['gruppen']).index(name))
            f = np.clip((r - g['schwelle']) / max(1e-3, 1.0 - g['schwelle']), 0, 1) ** g['kontrast'] + g['rest']
            rauschen[name] = np.clip(f, 0, 1).astype(np.float32)
        return rauschen[name]

    klassen = {k: v for k, v in regeln['klassen'].items() if not k.startswith('_') and v['netze']}
    kidx = {k: i for i, k in enumerate(regeln['klassen'])}
    WK = regeln['wasserkante']
    aus = []     # je Klasse: dict mit fi, fj, mi, mj
    stat = {}

    def lambda_karte(kname, kl):
        lam = np.full((H, W), kl['dichte'] * faktor, np.float32)
        lam *= biom_f
        lam *= lagen_f.get(kl.get('lagengruppe', 'feucht'), lagen_f['feucht'])
        b = beschattung
        if kl['schicht'] == '2 baum':
            lam *= np.where(lichtung, L['lichtung_baum_faktor'], 1.0)
        else:
            b = np.where(lichtung, b * 0.3, b)
        lam *= licht_faktor(b, kl['licht'])
        st = kl.get('stufe', {})
        lam *= wt * st.get('talboden', 1) + wh * st.get('hang', 1) + wk * st.get('karst_hoch', 1)
        kf = kl.get('karst', {})
        if kl.get('nur_karstfeld') and not karstfeld:
            lam[:] = 0
        kmap = np.ones((H, W), np.float32)
        kmap = np.where(gipfel, kf.get('gipfel', 1), kmap)
        kmap = np.where(fuss, kf.get('fuss', 1), kmap)
        kmap = np.where(spalte, kf.get('spalte', 0), kmap)
        kmap = np.where(steilwand, kf.get('wand', 0), kmap)
        lam *= kmap
        hmax = kl.get('hang_max', 40)
        if not kl.get('kletter'):
            hmax = min(hmax, regeln['hang']['hang_max_pflanze'])
            lam[hang3 > hmax] = 0          # Nicht-Kletterer: auch keine Zelle neben einer steileren
        else:
            hmax = min(hmax, regeln['hang']['hang_max_kletter'])
            lam[hang > hmax] = 0
        if 'hang_min' in kl:
            lam[hang < kl['hang_min']] = 0
        lam *= gruppe_f(kl.get('gruppe', 'gleich'))
        if kl['schicht'] == '5 wasserkante':
            band = kl.get('wasser', WK['band_m'])
            lam[(d_wasser < band[0]) | (d_wasser > band[1]) | (hang > WK['hang_max'])] = 0
            lam[wasser_m | meer | (d_weg < A['weg_klein']) | (d_ort < A['ort']) | standorte] = 0
        else:
            if 'wasser' in kl:
                lam[(d_wasser < kl['wasser'][0]) | (d_wasser > kl['wasser'][1])] = 0
            lam[sperre_gross if kl.get('gross') else sperre_klein] = 0
        if kl.get('gross'):
            lam[belegt_gross] = 0
        return lam

    def satelliten(kname, kl, pi, pj):
        """Satelliten-Instanzen um Elternpositionen (fi, fj)."""
        s = kl.get('satelliten')
        if not s or s['klasse'] not in klassen or pi.size == 0:
            return
        sk = klassen[s['klasse']]
        nmax = int(s['n'][1])
        gi, gj = np.round(pi).astype(np.int64) + wi0, np.round(pj).astype(np.int64) + wj0
        kan = 3000 + kidx[kname] * 7
        n = s['n'][0] + (hash01(gi, gj, seed, kan) * (nmax - s['n'][0] + 1)).astype(np.int32)
        fi_l, fj_l = [], []
        for k in range(nmax):
            sel = n > k
            if not sel.any():
                break
            ang = hash01(gi[sel], gj[sel], seed, kan + 1 + 2 * k) * 2 * math.pi
            rad = s['radius_m'][0] + (s['radius_m'][1] - s['radius_m'][0]) * hash01(gi[sel], gj[sel], seed, kan + 2 + 2 * k)
            fi_l.append(pi[sel] + rad * np.sin(ang))
            fj_l.append(pj[sel] + rad * np.cos(ang))
        fi = np.concatenate(fi_l)
        fj = np.concatenate(fj_l)
        ok = (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1)
        fi, fj = fi[ok], fj[ok]
        mi, mj = np.round(fi).astype(np.int32), np.round(fj).astype(np.int32)
        ok = ~(wasser_m[mi, mj] | meer[mi, mj] | weg_m[mi, mj] | ort_m[mi, mj]) & im_feld[mi, mj] & (zust[mi, mj] > 0)
        if not sk.get('kletter'):
            ok &= hang3[mi, mj] <= min(sk.get('hang_max', 40), regeln['hang']['hang_max_pflanze'])
        else:
            ok &= hang[mi, mj] <= min(sk.get('hang_max', 78), regeln['hang']['hang_max_kletter'])
        fi, fj, mi, mj = fi[ok], fj[ok], mi[ok], mj[ok]
        if fi.size:
            aus.append(dict(klasse=s['klasse'], fi=fi.astype(np.float32), fj=fj.astype(np.float32), mi=mi, mj=mj))
            stat[s['klasse']] = stat.get(s['klasse'], 0) + int(fi.size)

    # Reihenfolge: Bäume (groß → klein, Kronendach wächst mit), dann Mittel, Boden, Wasserkante
    reihenfolge = []
    for sch in SCHICHTEN:
        for kname, kl in klassen.items():
            if kl['schicht'] == sch and not kl.get('nur_satellit'):
                reihenfolge.append(kname)
    for kname in reihenfolge:
        kl = klassen[kname]
        lam = lambda_karte(kname, kl)
        if float(lam.max()) <= 0:
            continue
        fi, fj = streue(lam, kl['zelle_m'], seed, kidx[kname] + 1, wi0, wj0)
        if fi.size == 0:
            continue
        mi, mj = np.clip(fi.astype(np.int32), 0, H - 1), np.clip(fj.astype(np.int32), 0, W - 1)
        if kl['schicht'] == '2 baum':
            # eigene Bäume: Abstand untereinander (Zelle) + Kronendach + Belegung für folgende Klassen (auch im Rand)
            hoe = kl['hoehe_m'] * (kl['massstab'][0] + kl['massstab'][1]) * 0.5
            neu = np.stack([fi, fj, np.full(fi.size, hoe, np.float32)], axis=1)
            baeume_alle.append(neu)
            beschattung = np.maximum(beschattung, kronendach(neu, H, W, regeln))
            bm = np.zeros((H, W), bool)
            bm[mi, mj] = True
            belegt_gross |= dilate(bm, A['baum_fremd_gross'])
        ok = im_feld[mi, mj]
        fi, fj, mi, mj = fi[ok], fj[ok], mi[ok], mj[ok]
        if fi.size == 0:
            continue
        aus.append(dict(klasse=kname, fi=fi, fj=fj, mi=mi, mj=mj))
        stat[kname] = stat.get(kname, 0) + int(fi.size)
    # kleine Klassen: nicht in Baumstämme
    stamm = np.zeros((H, W), bool)
    for b in baeume_alle:
        if b.shape[0]:
            stamm[np.clip(np.round(b[:, 0]).astype(np.int32), 0, H - 1), np.clip(np.round(b[:, 1]).astype(np.int32), 0, W - 1)] = True
    stamm = dilate(stamm, A['baum_fremd_klein'])
    for a in aus:
        if not klassen[a['klasse']].get('gross') and klassen[a['klasse']].get('rolle') != 'kletterpflanze':
            keep = ~stamm[a['mi'], a['mj']]
            for k in ('fi', 'fj', 'mi', 'mj'):
                a[k] = a[k][keep]
    stat = {}
    for a in aus:
        stat[a['klasse']] = stat.get(a['klasse'], 0) + int(a['fi'].size)

    # --- Budget (Konventionen §3): proportionale Hash-Ausduennung, Satelliten, dann exakte Kappung
    B = regeln['budget']
    ausduenn = {}
    kleinzeug = set(B.get('kleinzeug_an_gras', []))

    def duenne(klassen_liste, ziel, ist, grund):
        if ist <= ziel:
            return
        ueber = ist - ziel
        pool, summe = [], 0
        for kname in klassen_liste:
            n = stat.get(kname, 0) * ausduenn.get(kname, 1.0)   # schon ausgeduennte Klassen zaehlen mit ihrem Rest
            if n <= 0:
                continue
            pool.append(kname)
            summe += n
            if summe * 0.6 >= ueber:
                break
        f = max(0.0, 1.0 - ueber / float(max(1.0, summe)))
        for kname in pool:
            ausduenn[kname] = ausduenn.get(kname, 1.0) * f       # Faktoren multiplizieren sich
        hinweise.append('WARNUNG %s: %d -> %d, Ausduennung %s' % (grund, ist, ziel, {k: round(ausduenn[k], 2) for k in pool}))
        if kleinzeug & set(pool):
            hinweise.append('Kleinzeug %s ausgeduennt - Flaeche soll Landschafts-Gras (GT_*) tragen' % sorted(kleinzeug & set(pool)))

    koll = sum(stat.get(k, 0) for k in klassen if klassen[k].get('kollision'))
    duenne(B['kollision_prioritaet'], B['kollision_je_feld'], koll, 'Kollisionsbudget')
    for sch, ziel in B['je_schicht'].items():
        ist = sum(stat.get(k, 0) * ausduenn.get(k, 1.0) for k in klassen if klassen[k]['schicht'] == sch)
        duenne([k for k in B['prioritaet'] if k in klassen and klassen[k]['schicht'] == sch], ziel, int(ist), 'Budget Schicht %s' % sch)
    gesamt = sum(stat.get(k, 0) * ausduenn.get(k, 1.0) for k in klassen)
    duenne([k for k in B['prioritaet'] if k in klassen], B['ziel_instanzen_je_feld'], int(gesamt), 'Gesamtbudget')
    for a in aus:
        f = ausduenn.get(a['klasse'], 1.0)
        if f < 1.0:
            keep = hash01(a['mi'] + wi0, a['mj'] + wj0, seed, 7000 + kidx[a['klasse']]) < f
            for k in ('fi', 'fj', 'mi', 'mj'):
                a[k] = a[k][keep]

    # Satelliten (Lianen an Staemmen) erst jetzt: nur an Baeumen, die das Budget ueberlebt haben
    for a in list(aus):
        kl = klassen[a['klasse']]
        if kl.get('satelliten') and a['fi'].size:
            satelliten(a['klasse'], kl, a['fi'], a['fj'])

    def kappe(klassen_liste, ziel, zaehlt, grund):
        """Exakte Kappung: in Prioritaetsreihenfolge fallen je Klasse die Instanzen mit dem hoechsten Hash zuerst."""
        ist = sum(int(a['fi'].size) for a in aus if zaehlt(a['klasse']))
        if ist <= ziel:
            return
        ueber = ist - ziel
        weg_je = {}
        for kname in klassen_liste:
            if ueber <= 0:
                break
            teile = [a for a in aus if a['klasse'] == kname and a['fi'].size]
            if not teile or not zaehlt(kname):
                continue
            hv = np.concatenate([hash01(a['mi'] + wi0, a['mj'] + wj0, seed, 7500 + kidx[kname]) +
                                 1e-4 * hash01(np.round(a['fi'] * 5).astype(np.int64), np.round(a['fj'] * 5).astype(np.int64), seed, 7600)
                                 for a in teile])
            n = int(hv.size)
            k = min(ueber, n)
            raus = np.zeros(n, bool)
            raus[np.argsort(-hv, kind='stable')[:k]] = True
            o = 0
            for a in teile:
                m = a['fi'].size
                keep = ~raus[o:o + m]
                o += m
                for kk in ('fi', 'fj', 'mi', 'mj'):
                    a[kk] = a[kk][keep]
            ueber -= k
            weg_je[kname] = k
        hinweise.append('WARNUNG %s hart: %d -> %d, gestrichen %s' % (grund, ist, ziel, weg_je))

    kappe(B['kollision_prioritaet'], int(B['kollision_je_feld']), lambda k: bool(klassen[k].get('kollision')), 'Kollisionsdeckel')
    kappe(B['prioritaet'] + [k for k in klassen if k not in B['prioritaet']], int(B.get('hart_instanzen_je_feld', 60000)),
          lambda k: True, 'Instanzdeckel')

    # --- Instanzen bauen und schreiben
    ausgabe = os.path.join(basis, WELT, regeln.get('ausgabe_ordner', 'dschungel'), feld)
    os.makedirs(ausgabe, exist_ok=True)
    for f in os.listdir(ausgabe):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    dateien, netz_inst, stat, nk = {}, {}, {}, 0
    for a in aus:
        n = int(a['fi'].size)
        if n == 0:
            continue
        kl = klassen[a['klasse']]
        gi, gj = a['mi'].astype(np.int64) + wi0, a['mj'].astype(np.int64) + wj0
        kan = 5000 + kidx[a['klasse']] * 5
        sub = (np.round(a['fi'] * 5).astype(np.int64), np.round(a['fj'] * 5).astype(np.int64))
        hv = (hash01(gi, gj, seed, kan) + 0.41 * hash01(sub[0], sub[1], seed, kan + 1)) % 1.0
        netzl = kl['netze']
        nidx = np.minimum((hv * len(netzl)).astype(np.int32), len(netzl) - 1)
        ms = kl['massstab'][0] + (kl['massstab'][1] - kl['massstab'][0]) * hash01(sub[0], sub[1], seed, kan + 2)
        yaw = hash01(sub[0], sub[1], seed, kan + 3) * 2 * math.pi
        if kl.get('yaw_hang'):
            asp = np.arctan2(-n_y[a['mi'], a['mj']], -n_x[a['mi'], a['mj']])   # hangabwärts
            yaw = asp + math.pi / 2 + (hash01(sub[0], sub[1], seed, kan + 4) - 0.5) * math.radians(50)
        z = bilinear(hoehe, a['fi'], a['fj']) - kl['eingraben_cm'] / 100.0
        inst = np.zeros((n, 10), np.float32)
        inst[:, 0] = (a['fj'] + wj0 - X0) * 100.0
        inst[:, 1] = (a['fi'] + wi0 - Y0) * 100.0
        inst[:, 2] = z * 100.0
        inst[:, 3:7] = quaternionen(n_x[a['mi'], a['mj']], n_y[a['mi'], a['mj']], n_z[a['mi'], a['mj']], float(kl['kippen']), yaw.astype(np.float32))
        inst[:, 7] = inst[:, 8] = inst[:, 9] = ms
        for ni in np.unique(nidx):
            m = nidx == ni
            p = netzl[ni]
            name = p.rsplit('/', 1)[-1]
            netz_inst.setdefault(name, []).append(inst[m])
            if name not in dateien:
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': a['klasse'], 'rolle': kl.get('rolle', 'dschungel'),
                                 'sichtweite': list(kl['sichtweite']), 'schatten': bool(kl.get('schatten', True)),
                                 'kollision': bool(kl.get('kollision', False)), 'ebene': kl['schicht']}
                if inv is not None and p in inv and not inv[p]['nanite']:
                    dateien[name]['nanite'] = False
            dateien[name]['anzahl'] += int(m.sum())
        stat[a['klasse']] = stat.get(a['klasse'], 0) + n
        if kl.get('kollision'):
            nk += n
    gesamt = 0
    for name, teile in netz_inst.items():
        arr = np.concatenate(teile, axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]

    # --- Blickziele und Karst-Info (für Teil C/D)
    blick = []
    hf = hoehe.copy()
    hf[~im_feld] = -1e9

    def welt(i, j):
        return {'i': int(i + wi0), 'j': int(j + wj0), 'x_cm': round(float((j + wj0 - X0) * 100), 1), 'y_cm': round(float((i + wi0 - Y0) * 100), 1), 'z_cm': round(float(hoehe[i, j] * 100), 1)}

    def top(masse, bewert, n, art, hinweis, sperr_m=150):
        bew = np.where(masse & im_feld & eigen, bewert, -np.inf)
        for _ in range(n):
            if not np.isfinite(bew).any():
                break
            k = int(np.argmax(bew))
            i, j = divmod(k, W)
            e = welt(i, j)
            e.update({'art': art, 'hinweis': hinweis})
            blick.append(e)
            ii, jj = np.indices((H, W))
            bew[(ii - i) ** 2 + (jj - j) ** 2 <= sperr_m * sperr_m] = -np.inf
    if turm:
        top(wand | gipfel, hoehe, 3, 'karstturm', 'höchste Zelle eines Wand-Clusters (Hang > %d°) – Akteur-Schale aus felsgruppen_overrides' % K['wand_grad'])
    hmin10 = minmax_filter(hs, 10, np.minimum)
    top(wasser_m & ((hs - hmin10) >= 8), hs - hmin10, 2, 'wasserfall', 'Wasserzelle mit ≥ 8 m Abfall in 10 m – Gischt/Partikel, Moos + Farne im Umkreis 15 m', 120)
    hmin40, hmax40 = minmax_filter(hs, 40, np.minimum), minmax_filter(hs, 40, np.maximum)
    top((hs <= hmin40 + 0.05) & ((hmax40 - hs) >= 8) & ~wasser_m & ~meer & (d_weg > 5), hmax40 - hs, 2, 'doline', 'geschlossene Senke (Relief ≥ 8 m in 40 m) – Farne/Moos dicht, Nebel-Volumen', 200)
    top((d_wand >= 10) & (d_wand <= 40) & (hang < 8) & (d_weg <= 60) & ~wasser_m & ~meer, -(hang + d_weg / 60.0), 2, 'tempelruine', 'flacher Karstfuß nahe Weg – AncientRuins-Ersatz (spuren_overrides), Lianen/Moos ×2', 250)

    # --- entfernen (Korrektur Runde 3b): nur mit Freigabe, nur wenn der feldweite Filter praktisch nur eigene Zellen trifft
    kand = [p.strip().lower() for p in str(feld_info.get('entfernen', '') or '').split(',') if p.strip()]
    kand, warn = pruefe_entfernen(kand, regeln, inv)
    hinweise.extend(warn)
    entf, entf_info = '', None
    if kand:
        land_m = ~(wasser_m | meer)
        land_feld = land_m & im_feld
        anteil_land = float((eigen & land_feld).sum()) / float(max(1, int(land_feld.sum())))
        zl = zaehle_entfernen(basis, feld, win, kand, eigen, zust > 0, land_m, im_feld)
        fremd_anteil = (zl['saum'] + zl['fremd']) / float(zl['gesamt']) if zl['gesamt'] else 0.0
        e_min = float(Z.get('entfernen_min_anteil_land', 0.85))
        e_fremd = float(Z.get('entfernen_max_fremd_anteil', 0.05))
        freigabe = bool(ersetzen) or bool(regeln.get('entfernen_aktiv', False))
        if not freigabe:
            grund = 'keine Freigabe (Schalter --ersetzen oder Regel entfernen_aktiv)'
        elif anteil_land < e_min:
            grund = 'Dschungel-Anteil der Landzellen im Feld %.0f %% < %.0f %% (Filter gilt feldweit)' % (100 * anteil_land, 100 * e_min)
        elif fremd_anteil > e_fremd:
            grund = '%.1f %% der Kandidaten in Saum-/Fremdzellen > %.0f %% (Filter gilt feldweit)' % (100 * fremd_anteil, 100 * e_fremd)
        elif zl['gesamt'] == 0:
            grund = 'keine passenden alten Instanzen in witcher/bestand im Feld'
        else:
            grund = ''
            entf = ','.join(kand)
        entf_info = {'praefixe': ','.join(kand), 'anzahl': zl['gesamt'], 'anzahl_eigene_zellen': zl['eigen'], 'anzahl_saum': zl['saum'],
                     'anzahl_fremde_zellen': zl['fremd'], 'anzahl_auf_wasser': zl['wasser'], 'je_netz': zl['je_netz'], 'je_ebene': zl['je_ebene'],
                     'baeume': 0, 'anteil_eigen_land_feld': round(anteil_land, 4), 'anteil_saum_fremd': round(fremd_anteil, 4),
                     'freigabe': freigabe, 'aktiv': bool(entf), 'grund': grund or 'aktiv', 'nur_ft_praefixe': list(regeln.get('entfernen_nur_ft', []))}
        if entf:
            hinweise.append('entfernen aktiv (%s): %d alte Instanzen im Feld (eigene Zellen %d, Saum %d, fremd %d), davon Baeume 0'
                            % (entf, zl['gesamt'], zl['eigen'], zl['saum'], zl['fremd']))
        else:
            hinweise.append('entfernen nicht gesetzt: %s; Vorschlag %d Instanzen (eigene Zellen %d) in plan.json["entfernen_vorschlag"]'
                            % (grund, zl['gesamt'], zl['eigen']))

    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': int(gesamt), 'dateien': dateien,
            'entfernen': entf, 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'biome_fenster': biome_fenster, 'zellen_zustaendig': zellen_zustaendig, 'biome_eigen': list(Z['biome_eigen']),
            'kollision_anzahl': int(nk),
            'statistik': {'je_klasse': stat, 'je_schicht': {s: int(sum(stat.get(k, 0) for k in klassen if klassen[k]['schicht'] == s)) for s in SCHICHTEN},
                          'kollision': int(nk), 'anteil_eigen_fenster': round(anteil_eigen, 4), 'dschungel_anteil_feld': round(ds_anteil, 4),
                          'biom_quelle': biom_quelle, 'saum_m': saum_m,
                          'beschattung_mittel_feld': round(float(beschattung[im_feld].mean()), 3), 'lichtung_anteil': round(float(lichtung[im_feld].mean()), 3),
                          'fremde_baeume_fenster': int(fremd.shape[0]), 'faktor': faktor, 'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA},
            'karst': {'karstfeld': karstfeld, 'turm': bool(turm), 'wand_zellen_feld': n_wand, 'fuss_zellen_feld': int((fuss & im_feld).sum()),
                      'spalte_zellen_feld': int((spalte & im_feld).sum()), 'gipfel_zellen_feld': int((gipfel & im_feld).sum()),
                      'wand_hoehe_min_max_m': [round(float(hoehe[wand_feld].min()), 1), round(float(hoehe[wand_feld].max()), 1)] if n_wand else None},
            'blickziele': blick, 'hinweise': hinweise,
            'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet (UNGETESTET MIT ECHTDATEN)'}
    if entf_info is not None:
        if entf:
            plan['entfernen_zaehlung'] = entf_info
            if entf_info['nur_ft_praefixe']:
                plan['entfernen_nur_ft'] = entf_info['nur_ft_praefixe']
        else:
            plan['entfernen_vorschlag'] = entf_info
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s: %d Instanzen (%d mit Kollision), %d Netze, Schichten %s, %.1f s' % (feld, gesamt, nk, len(dateien), plan['statistik']['je_schicht'], time.time() - t0))
    for h in hinweise:
        meld('  Hinweis:', h)

    if bild:
        try:
            from PIL import Image
        except Exception:
            meld('Pillow fehlt – kein Prüfbild')
            return plan
        fi0, fi1, fj0, fj1 = fb_[0] - wi0, fb_[1] - wi0, fb_[2] - wj0, fb_[3] - wj0
        hh = hoehe[fi0:fi1, fj0:fj1]
        g = np.clip((hh - hh.min()) / max(1e-3, float(hh.max() - hh.min())), 0, 1) * 110 + 60
        rgb = np.stack([g, g, g], axis=2).astype(np.float32)
        F = regeln['bild_farben']
        b = beschattung[fi0:fi1, fj0:fj1]
        rgb[..., 0] *= (1 - 0.45 * b)
        rgb[..., 2] *= (1 - 0.45 * b)
        rgb[lichtung[fi0:fi1, fj0:fj1]] = rgb[lichtung[fi0:fi1, fj0:fj1]] * 0.75 + np.array(F['_lichtung']) * 0.25
        rgb[fuss[fi0:fi1, fj0:fj1]] = F['_karst_fuss']
        rgb[wand[fi0:fi1, fj0:fj1]] = F['_karst_wand']
        rgb[(wasser_m | meer)[fi0:fi1, fj0:fj1]] = F['_wasser']
        rgb[weg_m[fi0:fi1, fj0:fj1]] = F['_weg']
        rgb[ort_m[fi0:fi1, fj0:fj1]] = F['_ort']
        for sch in ('0 boden', '5 wasserkante', '1 mittel', '2 baum'):
            for a in aus:
                if a['fi'].size == 0 or klassen[a['klasse']]['schicht'] != sch:
                    continue
                c = F.get(a['klasse'], [255, 255, 255])
                pi = np.clip(a['mi'] - fi0, 0, fi1 - fi0 - 1)
                pj = np.clip(a['mj'] - fj0, 0, fj1 - fj0 - 1)
                rgb[pi, pj] = c
                if klassen[a['klasse']].get('gross'):
                    rgb[np.minimum(pi + 1, fi1 - fi0 - 1), pj] = c
                    rgb[pi, np.minimum(pj + 1, fj1 - fj0 - 1)] = c
        for e in blick:
            i, j = e['i'] - wi0 - fi0, e['j'] - wj0 - fj0
            rgb[max(0, i - 4):i + 5, max(0, j - 4):j + 5] = (255, 0, 255)
        od = os.path.join(basis, 'docs', 'pruefung', 'dschungel')
        os.makedirs(od, exist_ok=True)
        Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(os.path.join(od, feld + '.png'))
        meld('Prüfbild:', os.path.join(od, feld + '.png'))
    return plan


def main():
    ap = argparse.ArgumentParser(description='Eldarien Dschungel-Planer (Boden, Sonderformen Mittel, Baum, Wasserkante; Karst-Info fuer Teil C/D)')
    ap.add_argument('felder', nargs='+')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    ap.add_argument('--ersetzen', action='store_true',
                    help='Freigabe fuer den entfernen-Filter (Witcher-Lianen); ohne Schalter bleibt plan.json["entfernen"] leer und die '
                         'Kandidaten stehen mit Zahl in plan.json["entfernen_vorschlag"] (Korrektur Runde 3b)')
    a = ap.parse_args()
    rp = a.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dschungel_regeln.json')
    if not os.path.isfile(rp):
        abbruch('Regeldatei fehlt: %s' % rp)
    try:
        regeln = json.load(open(rp, encoding='utf-8'))
    except Exception as ex:
        abbruch('Regeldatei %s nicht lesbar: %s' % (rp, ex))
    if not NUMBA:
        meld('numba nicht verfügbar – reiner NumPy-Pfad (ausreichend)')
    if a.ersetzen or regeln.get('entfernen_aktiv'):
        meld('Freigabe entfernen: ja (%s)' % ('--ersetzen' if a.ersetzen else 'Regel entfernen_aktiv'))
    else:
        meld('Freigabe entfernen: nein - plan.json["entfernen"] bleibt leer, Kandidaten in "entfernen_vorschlag"')
    for feld in a.felder:
        plane_feld(feld.strip().upper(), a.basis, json.loads(json.dumps(regeln)), a.faktor, a.bild, ersetzen=a.ersetzen)


if __name__ == '__main__':
    main()
