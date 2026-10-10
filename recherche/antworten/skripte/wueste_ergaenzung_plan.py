#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wueste_ergaenzung_plan.py – Planer „Wüste/Canyon/Ödland – Ergänzung“ (Auftrag 11, Teil B9) für Eldarien
(UE 5.8.3, 1-m-Raster NX 9577 × NY 7057, World Partition). Fassung Korrektur Runde 1 (10.10.2026).

*** UNGETESTET MIT ECHTDATEN *** – in der Cloud nur py_compile + Rauchtest mit synthetischen Rastern (Bericht
antworten/verteilung-wueste.md, Abschnitt „Korrektur Runde 1“). Echtlauf 10.10. (alte Fassung): A5/G4/E1/C6 je 0 Instanzen (korrekt).

Korrektur Runde 1 (verteilung-KONVENTIONEN.md §1–§6)
----------------------------------------------------
§1 Zuständigkeit: biome_eigen = wueste, canyon, oedland. Biom je Zelle aus eigner.r8 + welt.json["kacheln"][k]["rezept"]
   (Kennzahl 0 = Weltgelände → aue, Vulkan/Lava-Rezept → lava, unbekanntes Rezept → aue mit WARNUNG; rezept_alias in den
   Regeln). Nur wenn eigner.r8/welt.json fehlen: dominantes Feldbiom aus daten/biome_je_feld.json (Hinweis), danach
   feld_biom_fallback. Bebaut werden nur eigene Zellen plus 30-m-Saum nach außen (Dichtefaktor linear 1 → 0, Jump-Flooding-
   Distanz; im Saum gelten die Regeln des nächsten eigenen Bioms). Bezug sind die Landzellen (ohne karte_wasser).
   Eigenanteil im Fenster < 2 % → leerer plan.json (instanzen 0, dateien {}, alte f32 gelöscht), eine Logzeile.
§2 plan.json: biome_fenster, biome_fenster_bezug ("land"), zellen_zustaendig, biome_eigen, kollision_anzahl, entfernen
   (immer leer: nichts wird ersetzt), dateien[].ebene (0/1/2/5).
§3 Budget hart 60 000 Instanzen / 3 000 Kollision (Ziel 50 000); Wüstenfelder C3–E5 15 000 / 1 200. Ausdünnung
   proportional, danach exakte Kappung per Hash-Rang; WARNUNG im Log und in plan.json["hinweise"].
§4 Ebenen: generische Mittelschicht-Klassen (Trockengras-Büschel, Trockenhang-Sträucher, Totholz, Stümpfe, Zweige) setzt
   nur noch mittelschicht_plan.py (Block mittelschicht_overrides: palette/faktor/parameter/je_biom/faktor_je_feld);
   Felsen > 0,8 m, Geröllplatten, Terrassenkanten, Felsnadeln setzt felsgruppen_plan.py (felsgruppen_overrides.zusatzklassen);
   Knochen-Ersatz, Karren, Brunnen, Galgen-Ersatz setzt spuren_plan.py (spuren_overrides). Hier bleiben:
     Schicht 0 boden        Kiesel, Steine < 0,8 m, Trockenbett-Platten (Trockenriss-Ersatz), Trockenlaub unter toten Bäumen
     Schicht 1 mittel       nur Sonderformen: Dornbusch-Ödland, Sukkulenten-Polster
     Schicht 2 baum         tote Bäume groß/klein, Einzelbäume bei Restfeuchte, Krüppelkiefern an Terrassen, Köcherbäume
     Schicht 5 wasserkante  Rohrkolben und grünes Gras an Oasen/Rinnen mit Restfeuchte
§5 print() nur ASCII; fehlende Pflichtdatei (hoehe.f32, Regeldatei, daten/netze.csv) oder ungültiges Feld → FEHLER-Zeile,
   Exit-Code 2; fehlende optionale Dateien → Hinweis. Deterministisch (Hash aus Weltraster-Koordinate, Seed, Kanal).

Geländeableitung (nur NumPy, Fenster Feld + 64 m): Hang und Normale aus Gradient, Rinnen = konkave Krümmung (positiver
Laplace der geglätteten Höhe, zwei Maßstäbe), Kuppen = Prominenz über dem 24-m-Mittel + lokal höchste Zelle, Senken = Höhe
unter dem 24-m-Mittel, Wandfuß = flache Zellen unter Wänden > 35°, Terrassenkanten = flache Zellen mit Abbruch ≥ 3 m in 6 m
(dieselbe Definition wie felsgruppen_overrides.zusatzklassen.terrassenkanten), Restfeuchte aus Wassernähe + Senke + Rinne + Lagen.

Wüstenfelder C3 C4 D3 D4 D5 E3 E4 E5 (eigener Namaqualand-Planer, FT_EL_WU_*): NUR ERGÄNZEN. Klassen mit
wuestenfeld_faktor 0 werden dort nicht gestreut, Namaqualand-Netze durch netze_wuestenfeld ersetzt, Budget 15 000, nichts
wird entfernt. Die vorhandene Wüsten-Ebene wird – wenn auffindbar – als belegt geladen (Abstand): --wueste_ebene PFAD.

Aufruf
------
  python -I scripts/wueste_ergaenzung/wueste_ergaenzung_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD]
         [--regeln PFAD] [--netze PFAD] [--wueste_ebene PFAD]
  --basis         production-Wurzel (Default "."): darunter export/unreal/welt/, daten/netze.csv, daten/biome_je_feld.json
  --regeln        Regeldatei (Default: wueste_ergaenzung_regeln.json neben dem Skript)
  --netze         Inventar netze.csv (Default: <basis>/daten/netze.csv, sonst neben dem Skript bzw. vorlagen/daten/)
  --wueste_ebene  Ordner der vorhandenen Wüsten-Ebene (<PFAD>/<Feld>/plan.json + *.f32 oder <PFAD>/*.f32)
  --faktor        Dichtefaktor auf alle Klassen
  --bild          Draufsicht docs/pruefung/wueste_ergaenzung/<Feld>.png (1 px = 1 m; Saum grau, fremde Biome dunkel)

Liest   export/unreal/welt/hoehe.f32 (Pflicht, np.memmap, nur Fenster), lage_*.r8, karte_wasser/weg/ort.r8 (optional),
        eigner.r8 + welt.json, daten/biome_je_feld.json (Fallback), vorhandene Ebenen bestand/ witcher/ mittelschicht/
        felsgruppen/ spuren/ ufer/ wueste/ (<Feld>/plan.json + f32) und instanzen/instanzen.json (belegt).
Schreibt export/unreal/welt/wueste_ergaenzung/<Feld>/<Netzname>.f32 (10 float32 LE: x,y,z cm; qx,qy,qz,qw; sx,sy,sz)
        + plan.json (FORMAT.md §3 + KONVENTIONEN §2, plus "ebene", "modus", "statistik", "hinweise").

Quellen: vorlagen/FORMAT.md; antworten/verteilung-KONVENTIONEN.md; antworten/assets-taxonomie.md (Lücken wueste/canyon/
oedland); antworten/bildkritik-witcher-messlatte.md; antworten/verteilung-wueste.md (Herleitung der Dichten, Korrektur Runde 1).
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


def fehler(text):
    """Fehlende Pflichtdatei / falscher Aufruf: eine FEHLER-Zeile (ASCII) und Exit-Code 2 (KONVENTIONEN par. 5)."""
    print('[wueste_ergaenzung] FEHLER: ' + ascii_(text), flush=True)
    sys.exit(2)


# ----------------------------------------------------------------------------- Raster-Helfer
def feld_fenster(feld, rand):
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        fehler('Unbekanntes Feld %r (A1 ... J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        fehler('Unbekanntes Feld %r (A1 ... J7)' % feld)
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
            fehler('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        meld('WARNUNG: %s hat %d Werte, erwartet %d (NY %d × NX %d) – ignoriert' % (pfad, n, NX * NY, NY, NX))
        if pflicht:
            fehler('Pflichtdatei hat falsche Groesse: %s' % pfad)
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


def distanz(mask, max_m=64.0, quelle=False):
    """Euklidische Distanz (m) zur nächsten True-Zelle per Jump-Flooding; > max_m → 2·max_m.
    quelle=True: zusätzlich (si, sj) = Fensterindex der nächsten True-Zelle (-1, wenn keine in Reichweite)."""
    H, W = mask.shape
    fern = np.float32(max_m * 2.0)
    if not mask.any():
        d = np.full((H, W), fern, np.float32)
        if quelle:
            return d, np.full((H, W), -1, np.int32), np.full((H, W), -1, np.int32)
        return d
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
    d = np.minimum(d, fern).astype(np.float32)
    if quelle:
        return d, si, sj
    return d


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
    kandidaten.append(os.path.join(hier, 'netze.csv'))
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
    fehler('Pflichtdatei fehlt: daten/netze.csv (gesucht: %s)' % ', '.join(kandidaten))


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
    # Override-Blöcke für Teil C/D: nur prüfen und melden (die Querschnitts-Planer verwerfen fehlende Pfade selbst)
    def pfade(o):
        if isinstance(o, str):
            return [o] if o.startswith('/Game/') else []
        if isinstance(o, dict):
            return [p for v in o.values() for p in pfade(v)]
        if isinstance(o, list):
            return [p for v in o for p in pfade(v)]
        return []
    for blk in ('mittelschicht_overrides', 'felsgruppen_overrides', 'spuren_overrides'):
        alle = pfade({k: v for k, v in regeln.get(blk, {}).items() if not str(k).startswith('herkunft')})
        fehlt = sorted(set(p for p in alle if p not in inv))
        meld('%s: %d Netzpfade, %d nicht im Inventar%s' % (blk, len(set(alle)), len(fehlt), (' (' + ', '.join(fehlt[:4]) + ')') if fehlt else ''))


def netz_hoehe(inv, pfad, default=0.3):
    if inv and pfad in inv and inv[pfad]['hoehe_m'] > 0:
        return inv[pfad]['hoehe_m']
    return default


# ----------------------------------------------------------------------------- Weltdaten
def dominantes_feldbiom(basis, feld, regeln):
    """Fallback (nur ohne eigner.r8/welt.json): dominantes Biom des Feldes aus daten/biome_je_feld.json, sonst
    feld_biom_fallback der Regeln, sonst aue."""
    hier = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(basis, 'daten', 'biome_je_feld.json'), os.path.join(hier, 'biome_je_feld.json'),
              os.path.join(hier, '..', '..', 'vorlagen', 'daten', 'biome_je_feld.json')):
        if not os.path.isfile(p):
            continue
        try:
            d = json.load(open(p, encoding='utf-8'))
            tab = d.get('biome') if isinstance(d.get('biome'), dict) else d.get('felder', {})
            bp = tab[feld]['biome_prozent']
            if bp:
                return str(max(bp, key=lambda e: e[1])[0]), p
        except Exception:
            continue
    fb = regeln.get('feld_biom_fallback', {}).get(feld)
    if fb:
        return fb, 'feld_biom_fallback (Regeldatei)'
    return 'aue', 'Standard aue'


def lade_biome(basis, win, regeln, feld, hinweise):
    """Biom je Zelle (KONVENTIONEN par. 1) als Index in regeln['biome']: eigner.r8 + welt.json["kacheln"][k]["rezept"];
    Kennzahl 0 = Weltgelände → aue, Vulkan/Lava → lava, rezept_alias, unbekanntes Rezept → aue (WARNUNG).
    Nur wenn eigner.r8 oder welt.json fehlt: dominantes Feldbiom (biome_je_feld.json) für alle Zellen."""
    namen = list(regeln['biome'])
    Z = regeln['zustaendigkeit']
    null_biom = Z.get('eigner0_biom', 'aue')
    alias = {str(k).lower(): v for k, v in regeln.get('rezept_alias', {}).items() if not str(k).startswith('_')}
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    welt = None
    if eig is not None and os.path.isfile(wj):
        try:
            welt = json.load(open(wj, encoding='utf-8'))
        except Exception as e:
            hinweise.append('welt.json unlesbar (%s)' % e)
    if eig is None or welt is None:
        fb, q = dominantes_feldbiom(basis, feld, regeln)
        if fb not in namen:
            fb = 'aue'
        hinweise.append('eigner.r8/welt.json fehlen - Biom je Zelle = dominantes Feldbiom %r (%s)' % (fb, q))
        return np.full((H, W), namen.index(fb), np.int16), 'Fallback %s (%s)' % (fb, os.path.basename(q))
    kacheln = welt.get('kacheln', {})
    tabelle = np.full(256, namen.index(null_biom), np.int16)
    unbekannt = {}

    def biom_aus_rezept(rz):
        rz = str(rz).strip().lower()
        if rz in namen:
            return rz
        for k in sorted(alias, key=len, reverse=True):
            if k in rz and alias[k] in namen:
                return alias[k]
        if 'vulkan' in rz or 'lava' in rz:
            return 'lava'
        for n in sorted(namen, key=len, reverse=True):
            if n in rz:
                return n
        return None
    eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
    for k, v in eintraege:
        try:
            kk = int(v.get('kennzahl', v.get('id', k))) if isinstance(v, dict) else int(k)
        except Exception:
            continue
        if 0 < kk < 256:
            rz = v.get('rezept', '') if isinstance(v, dict) else v
            b = biom_aus_rezept(rz)
            if b is None:
                unbekannt[kk] = str(rz)
                b = null_biom
            tabelle[kk] = namen.index(b)
    tabelle[0] = namen.index(null_biom)  # 0 = Weltgelände → aue
    bio = tabelle[eig]
    if unbekannt:
        da = [kk for kk in unbekannt if (eig == kk).any()]
        if da:
            hinweise.append('WARNUNG: Kennzahlen ohne erkennbares Rezept -> %s: %s' % (null_biom, ', '.join('%d=%s' % (kk, unbekannt[kk]) for kk in da[:6])))
    return bio, 'eigner.r8 + welt.json'


def zustaendigkeit(bio, land, regeln, im_feld):
    """KONVENTIONEN par. 1: eigene Zellen (Land) Gewicht 1, Saum nach außen linear 1 → 0 über saum_m (Distanz per Jump-Flooding),
    im Saum gilt das nächste eigene Biom; zwischen eigenen Biomen weicher Wechsel (Box-Mittel saum_innen_m).
    Rückgabe: {biom: Gewicht H×W}, Saumfaktor s (H×W), Kennzahlen-Dict."""
    namen = list(regeln['biome'])
    Z = regeln['zustaendigkeit']
    eigen_l = [b for b in Z['biome_eigen'] if b in namen]
    saum = float(Z.get('saum_m', 30.0))
    innen = int(Z.get('saum_innen_m', 6))
    eidx = np.array([namen.index(b) for b in eigen_l], np.int16)
    eigen_m = np.isin(bio, eidx) & land
    d, si, sj = distanz(eigen_m, max_m=saum + 2.0, quelle=True)
    s = np.where(eigen_m, 1.0, np.clip(1.0 - d / max(1e-3, saum), 0.0, 1.0)).astype(np.float32)
    s = np.where(land, s, 0.0).astype(np.float32)
    naechst = np.where(si >= 0, bio[np.clip(si, 0, None), np.clip(sj, 0, None)], -1)
    gew = {}
    weich = {}
    for b, k in zip(eigen_l, eidx):
        ind = (bio == k) & land
        if ind.any():
            weich[b] = box_blur(ind.astype(np.float32), innen) if innen > 0 else ind.astype(np.float32)
    summe = sum(weich.values()) if weich else None
    for b, k in zip(eigen_l, eidx):
        if b not in weich:
            continue
        g_innen = np.where(eigen_m, weich[b] / np.maximum(summe, 1e-6), 0.0)
        g_saum = np.where(~eigen_m & (naechst == k), s, 0.0)
        gew[b] = (g_innen + g_saum).astype(np.float32)
    n_land = int(land.sum())
    kz = {'zellen_eigen_feld': int((eigen_m & im_feld).sum()),
          'zellen_saum_feld': int(((s > 0) & ~eigen_m & im_feld).sum()),
          'zellen_zustaendig': int(((s > 0) & im_feld).sum()),
          'anteil_eigen_fenster': round(float(eigen_m.sum()) / max(1, n_land), 4),
          'anteil_eigen_feld': round(float((eigen_m & im_feld).sum()) / max(1, int((land & im_feld).sum())), 4),
          'saum_m': saum}
    return gew, s, kz


def biome_anteile(bio, maske, namen):
    """Anteile aller Biome in der Maske (Summe 1), absteigend."""
    if not maske.any():
        maske = np.ones(bio.shape, bool)
    z = np.bincount(bio[maske].astype(np.int64), minlength=len(namen))
    n = max(1, int(z.sum()))
    return dict(sorted(((namen[k], round(float(z[k]) / n, 4)) for k in np.flatnonzero(z)), key=lambda e: -e[1]))


def plan_kopf(feld, regeln, modus, biome_fenster, kz, biome_eigen):
    return {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': 0, 'ebene': regeln.get('ebene', 'wueste_ergaenzung'),
            'modus': modus, 'kollision_anzahl': 0, 'biome_eigen': biome_eigen, 'biome_fenster': biome_fenster,
            'biome_fenster_bezug': regeln['zustaendigkeit'].get('bezug', 'land'), 'zellen_zustaendig': int(kz.get('zellen_zustaendig', 0)),
            'dateien': {}, 'entfernen': '', 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix']}


def ausgabe_leeren(ausgabe):
    os.makedirs(ausgabe, exist_ok=True)
    for f in os.listdir(ausgabe):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))


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

    # --- Biome und Zuständigkeit (KONVENTIONEN par. 1, Bezug Landzellen)
    namen = list(regeln['biome'])
    Zs = regeln['zustaendigkeit']
    biome_eigen = [b for b in Zs['biome_eigen'] if b in namen]
    bio, bio_quelle = lade_biome(basis, win, regeln, feld, hinweise)
    land = ~wasser_m
    biome_fenster = biome_anteile(bio, land, namen)
    bio_anteil = biome_anteile(bio, land & im_feld, namen)
    biom_gew, saum_s, kz = zustaendigkeit(bio, land, regeln, im_feld)
    kz['quelle'] = bio_quelle
    min_anteil = float(Zs.get('min_anteil_eigen_fenster', 0.02))
    ausgabe = os.path.join(basis, regeln['ausgabe']['ordner'], feld)
    if kz['anteil_eigen_fenster'] < min_anteil or kz['zellen_zustaendig'] == 0:
        ausgabe_leeren(ausgabe)
        kz_leer = dict(kz, zellen_zustaendig=0)
        plan = plan_kopf(feld, regeln, modus, biome_fenster, kz_leer, biome_eigen)
        hinweise.append('Anteil %s im Fenster %.1f %% (Land) < %.0f %% oder keine zustaendige Zelle im Feld - leerer Plan'
                        % ('/'.join(biome_eigen), 100 * kz['anteil_eigen_fenster'], 100 * min_anteil))
        plan['statistik'] = {'zustaendigkeit': kz, 'biome_anteil_feld': bio_anteil, 'laufzeit_s': round(time.time() - t0, 1)}
        plan['hinweise'] = hinweise
        with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=1)
        meld('%s: Eigenanteil %.2f %% < %.0f %% (%s) - leerer plan.json, 0 Instanzen' % (feld, 100 * kz['anteil_eigen_fenster'], 100 * min_anteil, bio_quelle))
        return plan

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
    rinne = np.where(wasser_m, 0, rinne).astype(np.float32)
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
                mi = np.clip(np.round(fi).astype(np.int32), 0, H - 1)
                mj = np.clip(np.round(fj).astype(np.int32), 0, W - 1)
                ok = lam[mi, mj] > 0  # Jitter nie aus der Zuständigkeit (Saum) oder auf Sperrzellen
                fi, fj, mi, mj = fi[ok], fj[ok], mi[ok], mj[ok]
                d_mitte = np.zeros(fi.size, np.float32)
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

    # --- Budget (KONVENTIONEN par. 3): proportional, danach exakte Kappung
    B = regeln['budget']
    hart = min(60000, int(B['wuestenfeld_instanzen'] if wf else B.get('hart_instanzen_je_feld', 60000)))
    ziel = min(hart, int(B['wuestenfeld_instanzen'] if wf else B['ziel_instanzen_je_feld']))
    koll_max = min(3000, int(B['wuestenfeld_kollision'] if wf else B['kollision_je_feld']))
    roh_gesamt = sum(a['fi'].size for a in aus)
    roh_koll = sum(a['fi'].size for a in aus if a['kollision'])
    ausduenn = {}
    kleinzeug_gekuerzt = False

    def warn(t):
        hinweise.append('WARNUNG: ' + t)
    if roh_koll > koll_max:
        f = koll_max / float(roh_koll)
        for a in aus:
            if a['kollision']:
                ausduenn[a['klasse']] = ausduenn.get(a['klasse'], 1.0) * f
        warn('Kollisionsbudget: %d -> %d (Faktor %.2f auf Kollisionsklassen)' % (roh_koll, koll_max, f))
    erwartet = {k: v * ausduenn.get(k, 1.0) for k, v in stat_roh.items()}
    gesamt = sum(erwartet.values())
    if gesamt > ziel:
        ueber = gesamt - ziel
        reihe = [k for k in B['ausduenn_reihenfolge'] if k in erwartet]
        pool, summe = [], 0.0
        for k in reihe:
            pool.append(k)
            summe += erwartet[k]
            if summe * 0.6 >= ueber:
                break
        f = max(0.0, 1.0 - ueber / float(max(1.0, summe)))
        for k in pool:
            ausduenn[k] = ausduenn.get(k, 1.0) * f
            kleinzeug_gekuerzt |= klassen[k]['schicht'] == '0_boden'
        warn('Instanzbudget: %d -> Ziel %d (%s), Ausduennung %s' % (int(gesamt), ziel, modus, {k: round(v, 2) for k, v in ausduenn.items()}))
    for a in aus:
        f = ausduenn.get(a['klasse'], 1.0)
        if f < 1.0:
            keep = hash01(np.round(a['fi'] * 7).astype(np.int64) + wi0 * 7, np.round(a['fj'] * 7).astype(np.int64) + wj0 * 7, seed, 99991 + kidx[a['klasse']]) < f
            for key in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw', 'eing'):
                a[key] = a[key][keep]

    def kappe(limit, nur_koll):
        """Exakte Kappung: niedrigste Priorität (ausduenn_reihenfolge) zuerst, innerhalb der Klasse nach Hash-Rang."""
        sel = [a for a in aus if (a['kollision'] or not nur_koll)]
        ueber = sum(a['fi'].size for a in sel) - limit
        if ueber <= 0:
            return 0
        weg = 0
        reihe = [k for k in B['ausduenn_reihenfolge'] if k in kidx] + [k for k in knamen if k not in B['ausduenn_reihenfolge']]
        for k in reihe:
            for a in sel:
                if a['klasse'] != k or a['fi'].size == 0 or ueber <= 0:
                    continue
                n = a['fi'].size
                drop = min(n, ueber)
                h = hash01(np.round(a['fi'] * 7).astype(np.int64) + wi0 * 7, np.round(a['fj'] * 7).astype(np.int64) + wj0 * 7, seed, 77777 + kidx[k])
                keep = np.sort(np.argsort(h, kind='stable')[drop:])
                for key in ('fi', 'fj', 'mi', 'mj', 'netz', 'massstab', 'yaw', 'eing'):
                    a[key] = a[key][keep]
                ueber -= drop
                weg += drop
        return weg
    w = kappe(koll_max, True)
    if w:
        warn('Kollision exakt gekappt: %d Instanzen entfernt (Deckel %d)' % (w, koll_max))
    w = kappe(hart, False)
    if w:
        warn('Instanzen exakt gekappt: %d entfernt (Deckel %d)' % (w, hart))
    if kleinzeug_gekuerzt:
        hinweise.append('Kleinzeug (Schicht 0) gekuerzt - Landschafts-Gras (GT_*) uebernimmt Kiesel/Laub-Anteil (KONVENTIONEN par. 3)')

    # --- Instanzen bauen und schreiben
    ausgabe_leeren(ausgabe)
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
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': a['klasse'], 'rolle': a['schicht'], 'ebene': int(a['schicht'][0]),
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
    plan = plan_kopf(feld, regeln, modus, biome_fenster, kz, biome_eigen)
    plan.update({'instanzen': int(gesamt), 'kollision_anzahl': int(nk), 'dateien': dateien})
    plan['statistik'] = {'je_klasse': stat, 'je_schicht': stat_schicht, 'kollision': int(nk), 'roh_vor_budget': {'gesamt': int(roh_gesamt), 'kollision': int(roh_koll)},
                         'budget': {'ziel': ziel, 'hart': hart, 'kollision': koll_max}, 'zustaendigkeit': kz, 'biome_anteil_feld': bio_anteil,
                         'gelaende': gel, 'faktor': faktor, 'wuestenfeld': wf, 'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA}
    plan['overrides_geliefert'] = {blk: sorted(k for k in regeln.get(blk, {}) if not str(k).startswith(('_', 'hinweis', 'herkunft', 'entscheidung')))
                                   for blk in ('mittelschicht_overrides', 'felsgruppen_overrides', 'spuren_overrides')}
    plan['hinweise'] = hinweise
    plan['ungetestet'] = 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet'
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s [%s]: %d Instanzen (%d mit Kollision), %d Netze, Eigenanteil Fenster %.1f %%, zustaendig %d Zellen, %.1f s -> %s' % (
        feld, modus, gesamt, nk, len(dateien), 100 * kz['anteil_eigen_fenster'], kz['zellen_zustaendig'], time.time() - t0, ausgabe))
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
        sf = saum_s[fi0:fi1, fj0:fj1]
        rgb = np.where((sf <= 0)[..., None], rgb * 0.45, rgb)  # fremde Biome (nicht zustaendig) abgedunkelt
        rgb = np.where(((sf > 0) & (sf < 1))[..., None], rgb * 0.8 + np.array([90, 90, 90], np.float32) * 0.2, rgb)  # Saum grau
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
        fehler('Pflichtdatei fehlt: Regeldatei %s' % rp)
    try:
        regeln = json.load(open(rp, encoding='utf-8'))
    except Exception as e:
        fehler('Regeldatei unlesbar: %s (%s)' % (rp, e))
    if 'zustaendigkeit' not in regeln:
        fehler('Regeldatei %s ohne Block zustaendigkeit (Fassung vor Korrektur Runde 1?)' % rp)
    if not os.path.isfile(os.path.join(a.basis, WELT, 'hoehe.f32')):
        fehler('Pflichtdatei fehlt: hoehe.f32 unter %s (--basis auf die production-Wurzel setzen)' % os.path.join(a.basis, WELT))
    for f in a.felder:
        feld_fenster(f, 0)  # ungueltiges Feld -> Exit 2 vor dem ersten Lauf
    if not NUMBA:
        meld('numba nicht verfügbar – reiner NumPy-Pfad (ausreichend)')
    inv = lade_inventar(a.basis, a.netze)
    pruefe_paletten(regeln, inv)
    for feld in a.felder:
        plane_feld(feld, a.basis, regeln, inv, a.faktor, a.bild, a.wueste_ebene)


if __name__ == '__main__':
    main()
