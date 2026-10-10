#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nordkueste_plan.py – Planer Biomgruppe 1 „Nordküste“ (biome_eigen = fjord, kueste, bergwald) für Eldarien (UE 5.8.3, 1-m-Raster 9577 × 7057).
Auftrag 11, Teil B1, Stand Korrektur Runde 1 (10.10.2026, verteilung-KONVENTIONEN.md §1–§5).
Korrektur Runde 2: Platten-Klassen (platten_regel; Rolle platte/geroell_platte oder RockyGround-/flat_rock-Netze) nur auf
lage_Kies/Geroell/Fels/Felsplatte >= 100, nie wo Gras/Wiese staerker deckt, >= 50 % eingegraben, an der Normale; Kiesel mit
teppich_sperre nur auf/um Geroell-Lagen, am Weg und am Ufer (kein Hangteppich).

Schichten dieses Planers: 0 boden (Nadelstreu, Kiesel, Moos, Bodendecker), 1 NUR Nordküsten-Sonderformen (Windflucht-Krüppelkiefer,
Windflucht-Küstenkiefer, Strandhafer, Klippenwiesen-Blumen, Efeu an Fels, Wurzelanläufe an Stämmen), 2 baum, 5 wasserkante (Tang, Treibholz, Strandkiesel/-platten).
Generische Mittelschicht-Klassen (strauch, jungbaum, farn, totholz_liegend/_stumpf/_ast, hochstaude, grasbueschel, beere, pilz) setzt nur
mittelschicht_plan.py; dieser Planer liefert dafür `mittelschicht_overrides` (Palette, Faktor, Zusatzklassen wie Blaubeer-Teppiche) in
nordkueste_regeln.json. Felsblöcke > 0,8 m (auch Fjord-Felsufer) → `felsgruppen_overrides`, Spuren → `spuren_overrides`.

*** UNGETESTET MIT ECHTDATEN *** – in der Cloud nur py_compile und synthetische Rauchtests (verteilung-nordkueste.md, Korrektur Runde 1).

Was das Skript tut
------------------
Je Gitterfeld wird ein Fenster (Feld + 64 m Rand) aus hoehe.f32 per np.memmap gelesen. Biom je Zelle aus eigner.r8 + welt.json
(rezept; Kennzahl 0 = Weltgelände → aue, Vulkanregion → lava); nur ohne eigner.r8 dominantes Feldbiom aus daten/biome_je_feld.json.
Zuständig sind Zellen mit Biom in biome_eigen plus ein 30-m-Saum nach außen: exakte euklidische Distanztransformation (separierbar,
NumPy), Dichtefaktor linear 1 → 0, im Saum gelten die Regeln des nächstgelegenen eigenen Bioms. Anteil der eigenen Biome im Fenster
< 2 % → leerer plan.json (instanzen 0, keine f32), eine Hinweiszeile, Exit-Code 0.
Danach wie bisher: Hang, Normale, Nordhang, Meeres-Wasserlinie (Abstandsfeld bis 500 m), Sperrzonen (Weg/Ort/Wasser/Standorte),
Lagenfaktoren, vorhandene Bäume (bestand/, witcher/, 8 Nachbarfelder, instanzen/instanzen.json), Kronendach → Beschattung, Wald,
Waldsaum, Lichtungen. Dichtefeld je Klasse = Licht × Biom × Zuständigkeit/Saum × Lagen × Hang × Höhe × Küste × Wasser × Saum/Lichtung ×
Klumpung × Fels-/Baumnähe; Jitter-Gitter-Streuung mit Hash-Zufall aus Weltrasterkoordinaten → deterministisch, Nachbarfelder nahtlos.
Reihenfolge: Ebene 2 (Bäume) → Kronendach → Ebenen 1, 0, 5. Budget: Schicht-Ziele, dann ≤ 60 000 Instanzen je Feld (Ziel 50 000),
≤ 3 000 mit Kollision; Ausdünnung deterministisch (Hash-Rang, exakte Anzahl) nach Priorität, Warnung im Log.

Aufruf
------
  python -I scripts/nordkueste/nordkueste_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
  --basis   production-Wurzel (Default "."), darunter export/unreal/welt/, daten/netze.csv, daten/netze_masse.json, docs/
  --regeln  Regeldatei (Default: nordkueste_regeln.json neben dem Skript)
  --faktor  Dichtefaktor auf alle Klassen
  --bild    Draufsicht docs/pruefung/nordkueste/<Feld>.png (1 px = 1 m; fremde Biome abgedunkelt, Saum orange, Biomgrenze weiß)
  Exit-Code 0 = alles geplant (auch leere Pläne), 2 = Pflichtdatei fehlt (hoehe.f32, Regeln, daten/netze.csv) oder Feldname ungültig.
  Alle Konsolenausgaben sind ASCII (Umlaute als ae/oe/ue/ss), Logs werden unter Windows mit cp1252 weiterverarbeitet.

Ausgabe (FORMAT.md §3 + Konventionen §2)
----------------------------------------
  export/unreal/welt/nordkueste/<Feld>/<Netzname>.f32   10 float32 LE je Instanz: x,y,z cm; qx,qy,qz,qw; sx,sy,sz
  export/unreal/welt/nordkueste/<Feld>/plan.json        instanzen, dateien{pfad, anzahl, gruppe, rolle, ebene, sichtweite, schatten,
                                                         kollision}, biome_fenster, zellen_zustaendig, biome_eigen, kollision_anzahl,
                                                         entfernen (nur baum_modus ersetzen), ft_ordner, ft_praefix, hinweise, statistik
  Ein Netz, das in zwei Ebenen vorkommt, bekommt in der zweiten Ebene den Dateinamen <Netzname>_e<Ebene>.f32.

Quellen (Regeln, Zahlen): antworten/verteilung-nordkueste.md (Skellige-Analyse, Schichten, Testanleitung, Korrektur Runde 1),
antworten/verteilung-KONVENTIONEN.md, vorlagen/FORMAT.md (Raster, Instanzformat, Budgets, Abstände), antworten/assets-taxonomie.md,
antworten/bildkritik-witcher-messlatte.md, antworten/ufer-kies-coast-dunes.md, 80.lv „World building of Witcher 3“,
GDC 2014 Gollent „Landscape Creation and Rendering in REDengine 3“. Nur NumPy; numba optional (nicht benötigt).
"""
import argparse
import csv
import json
import math
import os
import sys
import time

import numpy as np

try:  # numba optional – nur Meldung
    import numba  # noqa: F401
    NUMBA = True
except Exception:  # pragma: no cover
    NUMBA = False

NX, NY = 9577, 7057
FELD_M = 1008
X0, Y0 = 4730.5, 4060.5  # X_cm = (j - 4730.5)*100, Y_cm = (i - 4060.5)*100
WELT = os.path.join('export', 'unreal', 'welt')
EBENEN = ['2', '1', '0', '5']  # Planungsreihenfolge: Bäume zuerst (Kronendach)
# Korrektur Runde 2 (Befund 2): flache Platten-Netze nur auf Kies-/Geroell-/Fels-Lagen, tief eingegraben, an der Normale
PLATTEN_MUSTER = ('erodedrockyground', 'nordicbeachrockyground', 'tundrarockyground', 'flat_rock_0')
PLATTEN_ROLLEN = ('platte', 'geroell_platte')
PLATTEN_STANDARD = {'lagen_min': {'Kies': 100, 'Geroell': 100, 'Fels': 100, 'Felsplatte': 100}, 'nicht_auf': ['Gras', 'Wiese'],
                    'eingraben_min_anteil': 0.5, 'kippen': 1.0}
BAUM_ROLLEN = ('baum', 'tree', 'nadel', 'laub', 'kiefer', 'buche', 'birke', 'fichte', 'tanne', 'eiche', 'weide', 'pappel',
               'palme', 'hainbuche', 'pine', 'fir', 'oak', 'poplar', 'hornbeam')


# ----------------------------------------------------------------------------- Helfer
def platten_regel(kl):
    """Platten-Regel (Runde 2) fuer eine Klasse: explizit `platten_regel`, sonst Standard fuer Rolle platte/geroell_platte oder
    Klassen mit flachen RockyGround-/flat_rock-Netzen; None = keine Platten-Klasse."""
    pr = kl.get('platten_regel')
    if pr is None and (str(kl.get('rolle', '')) in PLATTEN_ROLLEN
                       or any(m in str(n).lower() for n in kl.get('netze', []) for m in PLATTEN_MUSTER)):
        pr = {}
    if pr is None or pr is False:
        return None
    out = dict(PLATTEN_STANDARD)
    out.update({k: v for k, v in pr.items() if k in PLATTEN_STANDARD})
    return out


def platten_maske(lagen, pr, form):
    """True, wo mindestens eine der Lagen pr['lagen_min'] >= Schwelle (0-255) liegt und keine der Lagen pr['nicht_auf']
    (Gras/Wiese) staerker deckt als die staerkste Fels-Lage. Ohne Lagen: nirgends (Platten nie blind setzen)."""
    ok = np.zeros(form, bool)
    fels = np.zeros(form, np.float32)
    for ln, mn in pr['lagen_min'].items():
        if ln in lagen:
            ok |= lagen[ln] * 255.0 >= float(mn) - 1e-3
            fels = np.maximum(fels, lagen[ln])
    for ln in pr['nicht_auf']:
        if ln in lagen:
            ok &= lagen[ln] < fels
    return ok


def teppich_maske(lagen, ts, d_weg, d_wasser, form):
    """Kiesel/Steine < 0,5 m nicht als Hangteppich (Runde 2): erlaubt nur auf/um Geroell-Lagen (Kontakt kontakt_m), am Weg
    (weg_m) und am Ufer (wasser_m)."""
    fels = np.zeros(form, bool)
    for ln in ts.get('lagen', ['Kies', 'Geroell', 'Fels', 'Felsplatte']):
        if ln in lagen:
            fels |= lagen[ln] * 255.0 >= float(ts.get('ab', 80)) - 1e-3
    m = dilate(fels, float(ts.get('kontakt_m', 6))) if fels.any() else fels
    m |= d_weg <= float(ts.get('weg_m', 3))
    m |= d_wasser <= float(ts.get('wasser_m', 5))
    return m


_ASCII = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss', '→': '->', '←': '<-', '≤': '<=', '≥': '>=',
          '…': '...', '–': '-', '—': '-', '×': 'x', '°': ' Grad', 'π': 'pi', '²': '2', '„': '"', '“': '"', '”': '"', '‚': "'",
          '‘': "'", '’': "'", '±': '+/-', '·': '*', '≈': '~', '\u00a0': ' ', '\u202f': ' '}


def ascii_text(t):
    """Konsolentext nur ASCII (Konventionen §5): Umlaute -> ae/oe/ue/ss, Sonderzeichen ersetzt, Rest '?'."""
    t = str(t)
    for k, v in _ASCII.items():
        t = t.replace(k, v)
    return t.encode('ascii', 'replace').decode('ascii')


def meld(*a):
    print(ascii_text(' '.join(['[nordkueste]'] + [str(x) for x in a])), flush=True)


class Pflichtfehler(Exception):
    """Pflichtdatei fehlt oder Eingabe ungueltig -> Exit-Code 2."""


def feld_fenster(feld, rand):
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        raise Pflichtfehler('Unbekanntes Feld %r (A1 ... J7)' % feld)
    s = ord(feld[0]) - ord('A')
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise Pflichtfehler('Unbekanntes Feld %r (A1 ... J7)' % feld)
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX)
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY)
    win = (max(0, i0 - rand), min(NY, i1 + rand), max(0, j0 - rand), min(NX, j1 + rand))
    return (i0, i1, j0, j1), win


def lade_raster(pfad, dtype, win, pflicht=False):
    """Fensterausschnitt eines NY×NX-Rasters per memmap (nur das Fenster wird gelesen)."""
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            raise Pflichtfehler('Pflichtdatei fehlt: %s' % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        meld('WARNUNG: %s hat %d Werte, erwartet %d – ignoriert' % (pfad, n, NX * NY))
        if pflicht:
            raise Pflichtfehler('Pflichtdatei hat falsche Groesse: %s' % pfad)
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
    """3 Box-Durchläufe ≈ Gauß (sigma in Zellen), separierbar."""
    w = math.sqrt(12.0 * sigma * sigma / 3.0 + 1.0)
    r = max(1, int(round((w - 1) / 2)))
    out = a
    for _ in range(3):
        out = box_blur(out, r)
    return out


def dilate1(m, acht):
    n = m.copy()
    n[1:, :] |= m[:-1, :]
    n[:-1, :] |= m[1:, :]
    n[:, 1:] |= m[:, :-1]
    n[:, :-1] |= m[:, 1:]
    if acht:
        n[1:, 1:] |= m[:-1, :-1]
        n[1:, :-1] |= m[:-1, 1:]
        n[:-1, 1:] |= m[1:, :-1]
        n[:-1, :-1] |= m[1:, 1:]
    return n


def dilate(mask, r):
    m = mask.copy()
    for k in range(int(math.ceil(r))):
        m = dilate1(m, k % 2 == 1)
    return m


def distanz(mask, max_m, grob_m=4):
    """Abstand (m) zur nächsten True-Zelle durch iterierte Dilatation: fein (1 m) bis min(30, max_m), darüber grob (grob_m).
    Jenseits max_m: max_m + 1. Nur NumPy."""
    H, W = mask.shape
    out = np.full((H, W), float(max_m + 1), np.float32)
    if not mask.any():
        return out
    fein = int(min(30, max_m))
    m = mask.copy()
    out[m] = 0.0
    for k in range(1, fein + 1):
        n = dilate1(m, k % 2 == 1)
        out[n & ~m] = k
        m = n
    if max_m > fein:
        g = int(grob_m)
        Hg, Wg = (H + g - 1) // g, (W + g - 1) // g
        pad = np.zeros((Hg * g, Wg * g), bool)
        pad[:H, :W] = mask
        mg = pad.reshape(Hg, g, Wg, g).any(axis=(1, 3))
        og = np.full((Hg, Wg), float(max_m + 1), np.float32)
        og[mg] = 0.0
        schritte = int(math.ceil(max_m / g))
        for k in range(1, schritte + 1):
            n = dilate1(mg, k % 2 == 1)
            og[n & ~mg] = k * g
            mg = n
        of = np.repeat(np.repeat(og, g, axis=0), g, axis=1)[:H, :W]
        out = np.where(out <= fein, out, np.maximum(of, fein + 1.0)).astype(np.float32)
    return out


def edt_label(mask, lbl, max_m):
    """Exakte euklidische Distanz (m) zur naechsten True-Zelle, abgeschnitten bei max_m (darueber max_m + 1), plus Label der
    naechsten True-Zelle (lbl an dieser Zelle; -1 jenseits max_m). Separierbar: Zeilen-Scan (exakt, kumulatives Max/Min),
    dann Spalten-Minimum ueber |di| <= max_m (Saito-Toriwaki, abgeschnitten). Nur NumPy, keine Zellschleifen."""
    H, W = mask.shape
    gross = np.int64(10 ** 9)
    j = np.arange(W, dtype=np.int64)[None, :]
    links = np.maximum.accumulate(np.where(mask, j, -gross), axis=1)
    rechts = np.minimum.accumulate(np.where(mask, j, gross)[:, ::-1], axis=1)[:, ::-1]
    dl = j - links
    dr = rechts - j
    nimm_l = dl <= dr
    g = np.minimum(dl, dr)
    jpos = np.clip(np.where(nimm_l, links, rechts), 0, W - 1)
    zeilen = np.arange(H)[:, None]
    lh = np.where(g <= max_m, lbl[zeilen, jpos], -1).astype(np.int16)
    g = np.minimum(g, int(max_m) + 1).astype(np.float32)
    g2 = g * g
    best = g2.copy()
    lab = lh.copy()
    for di in range(1, int(max_m) + 1):
        d2 = np.float32(di * di)
        # Quelle unterhalb (i + di) -> Ziel i
        c = g2[di:, :] + d2
        upd = c < best[:-di, :]
        best[:-di, :] = np.where(upd, c, best[:-di, :])
        lab[:-di, :] = np.where(upd, lh[di:, :], lab[:-di, :])
        # Quelle oberhalb (i - di) -> Ziel i
        c = g2[:-di, :] + d2
        upd = c < best[di:, :]
        best[di:, :] = np.where(upd, c, best[di:, :])
        lab[di:, :] = np.where(upd, lh[:-di, :], lab[di:, :])
    dist = np.sqrt(best).astype(np.float32)
    weit = dist > max_m
    dist[weit] = float(max_m) + 1.0
    lab[weit] = -1
    return dist, lab


def hash01(i, j, seed, kanal):
    """Deterministische Zufallszahl [0,1) je (Weltzeile, Weltspalte, Seed, Kanal) – 32-bit-Mischer."""
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


def wertrauschen(H, W, wi0, wj0, skala_m, seed, kanal):
    """Wertrauschen 0..1 im Weltraster (Gitterweite skala_m, bilinear mit Smoothstep), 2 Oktaven – deterministisch."""
    ii = (np.arange(H, dtype=np.float64) + wi0)[:, None]
    jj = (np.arange(W, dtype=np.float64) + wj0)[None, :]

    def oktave(s, k):
        gi = np.floor(ii / s)
        gj = np.floor(jj / s)
        ti = (ii / s - gi)
        tj = (jj / s - gj)
        ti = ti * ti * (3 - 2 * ti)
        tj = tj * tj * (3 - 2 * tj)
        gi = gi.astype(np.int64)
        gj = gj.astype(np.int64)
        a = hash01(gi, gj, seed, k)
        b = hash01(gi, gj + 1, seed, k)
        c = hash01(gi + 1, gj, seed, k)
        d = hash01(gi + 1, gj + 1, seed, k)
        return (a * (1 - tj) + b * tj) * (1 - ti) + (c * (1 - tj) + d * tj) * ti
    n = 0.7 * oktave(float(skala_m), kanal) + 0.3 * oktave(max(2.0, skala_m / 3.0), kanal + 1)
    return n.astype(np.float32)


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
    """Z-Achse um Anteil `kippen` auf die Zielnormale kippen, davor Zufalls-Yaw. (n,4) = x,y,z,w."""
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


def trapez(x, p):
    d0, d1, d2, d3 = [float(v) for v in p]
    x = x.astype(np.float32)
    auf = np.clip((x - d0) / max(1e-6, d1 - d0), 0, 1) if d1 > d0 else (x >= d0).astype(np.float32)
    ab = np.clip((d3 - x) / max(1e-6, d3 - d2), 0, 1) if d3 > d2 else (x <= d3).astype(np.float32)
    return np.minimum(auf, ab).astype(np.float32)


def rampe_ab(x, voll_bis, null_ab):
    """1 bis voll_bis, linear auf 0 bei null_ab."""
    return np.clip((null_ab - x) / max(1e-6, null_ab - voll_bis), 0, 1).astype(np.float32)


def rampe_auf(x, null_bis, voll_ab):
    return np.clip((x - null_bis) / max(1e-6, voll_ab - null_bis), 0, 1).astype(np.float32)


def blockmittel(a, g):
    H, W = a.shape
    Hg, Wg = (H + g - 1) // g, (W + g - 1) // g
    p = np.zeros((Hg * g, Wg * g), np.float32)
    p[:H, :W] = a
    return p.reshape(Hg, g, Wg, g).mean(axis=(1, 3))


# ----------------------------------------------------------------------------- Weltdaten
def lade_netze(basis):
    """pfad → (sx, sy, sz) m aus daten/netze.csv; Pflicht für die Pfadprüfung."""
    p = os.path.join(basis, 'daten', 'netze.csv')
    if not os.path.isfile(p):
        raise Pflichtfehler('Pflichtdatei fehlt: %s (Inventar fuer Pfadpruefung und Netzhoehen)' % p)
    out = {}
    with open(p, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter=';'):
            try:
                out[r['pfad']] = (float(r['groesse_x_m']), float(r['groesse_y_m']), float(r['groesse_z_m']))
            except Exception:
                out[r['pfad']] = (1.0, 1.0, 0.5)
    return out


def lade_masse(basis):
    p = os.path.join(basis, 'daten', 'netze_masse.json')
    if not os.path.isfile(p):
        return {}
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception as e:
        meld('Hinweis: netze_masse.json unlesbar (%s)' % e)
        return {}


def feld_dominantes_biom(basis, feld):
    """Dominantes Biom des Feldes aus daten/biome_je_feld.json (felder[FELD].biome_prozent[0][0]); None, wenn unlesbar."""
    p = os.path.join(basis, 'daten', 'biome_je_feld.json')
    if not os.path.isfile(p):
        return None
    try:
        d = json.load(open(p, encoding='utf-8'))
        bp = d['felder'][feld]['biome_prozent']
        bp = sorted(bp, key=lambda e: -float(e[1]))
        return str(bp[0][0]).lower()
    except Exception as e:
        meld('Hinweis: daten/biome_je_feld.json nicht auswertbar für %s (%s)' % (feld, e))
        return None


def lade_biome(basis, win, regeln, feld, hoehe):
    """Biom je Zelle als Index in biome_alle + ['sonst'] (Konventionen §1).
    eigner.r8 + welt.json: Kennzahl -> rezept -> Biom; Kennzahl 0 = Weltgelaende -> aue; Rezept mit 'vulkan' -> lava.
    Nur wenn eigner.r8 (oder welt.json) fehlt: dominantes Feldbiom aus daten/biome_je_feld.json fuer das ganze Fenster;
    fehlt auch das: feld_biom_fallback aus den Regeln (mit Hoehengrenze feld_fallback_hoehe_max_m). Rueckgabe (bio, namen, quelle)."""
    alle = list(regeln['biome_alle'])
    namen = alle + ['sonst']
    sonst = len(alle)
    alias = regeln.get('rezept_alias', {})
    H, W = win[1] - win[0], win[3] - win[2]
    eig = lade_raster(os.path.join(basis, WELT, 'eigner.r8'), np.uint8, win)
    wj = os.path.join(basis, WELT, 'welt.json')
    welt = None
    if eig is not None and os.path.isfile(wj):
        try:
            welt = json.load(open(wj, encoding='utf-8'))
        except Exception as e:
            meld('Hinweis: welt.json unlesbar (%s) - Fallback dominantes Feldbiom' % e)
            welt = None
    if eig is not None and welt is not None:
        kacheln = welt.get('kacheln', {})
        tabelle = np.full(256, sonst, np.int16)
        nach_laenge = sorted(alle, key=lambda n: -len(n))

        def biom_aus_rezept(rz):
            rz = str(rz).lower().strip()
            if rz in alle:
                return alle.index(rz)
            for k, v in alias.items():
                if k in rz and v in alle:
                    return alle.index(v)
            for n in nach_laenge:
                if n in rz:
                    return alle.index(n)
            return sonst
        eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
        for k, v in eintraege:
            try:
                kk = int(v.get('kennzahl', v.get('id', k))) if isinstance(v, dict) else int(k)
            except Exception:
                continue
            if 0 <= kk < 256:
                rz = v.get('rezept', '') if isinstance(v, dict) else ''
                tabelle[kk] = biom_aus_rezept(rz) if rz else sonst
        tabelle[0] = alle.index('aue')  # Kennzahl 0 = Weltgelaende -> aue (Konventionen §1)
        return tabelle[eig], namen, 'eigner.r8'
    dom = feld_dominantes_biom(basis, feld)
    if dom in alle:
        meld('Hinweis: eigner.r8/welt.json fehlen - Biom im ganzen Fenster = dominantes Feldbiom %r (daten/biome_je_feld.json)' % dom)
        return np.full((H, W), alle.index(dom), np.int16), namen, 'biome_je_feld.json (dominant, Fallback)'
    fb = regeln.get('feld_biom_fallback', {}).get(feld)
    if fb in alle:
        bio = np.full((H, W), alle.index(fb), np.int16)
        hmax = regeln.get('feld_fallback_hoehe_max_m', {}).get(feld)
        if hmax is not None:
            bio[hoehe > float(hmax)] = sonst
        meld('Hinweis: eigner.r8 und biome_je_feld.json fehlen - Regel-Fallback %r%s' % (fb, (' bis %.0f m' % float(hmax)) if hmax is not None else ''))
        return bio, namen, 'feld_biom_fallback (Regeln)'
    meld('Hinweis: weder eigner.r8 noch biome_je_feld.json noch Regel-Fallback fuer %s - Biom unbekannt' % feld)
    return np.full((H, W), sonst, np.int16), namen, 'unbekannt'


def lade_ebene_positionen(ordner, win, entfernen_praefixe=()):
    """Positionen (Fenster-i, Fenster-j, Maßstab) aller Instanzen einer Ebene; Bäume und Sonstige getrennt.
    Namen, die mit einem entfernen-Präfix beginnen, werden übersprungen (sie werden ohnehin gelöscht)."""
    baum, sonst = [], []
    pj = os.path.join(ordner, 'plan.json')
    if not os.path.isfile(pj):
        return baum, sonst
    try:
        plan = json.load(open(pj, encoding='utf-8'))
    except Exception:
        return baum, sonst
    for name, info in plan.get('dateien', {}).items():
        if any(name.lower().startswith(p) for p in entfernen_praefixe):
            continue
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
        ist_baum = (info.get('rolle') == 'baum') or (any(r in txt for r in BAUM_ROLLEN) and 'tot' not in txt
                                                      and 'stump' not in txt and 'log' not in txt and 'plant' not in txt)
        (baum if ist_baum else sonst).append(np.stack([fi[m], fj[m], a[m, 9]], axis=1))
    return baum, sonst


def lade_baeume(basis, feld, win, entfernen_praefixe=()):
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
                b, so = lade_ebene_positionen(os.path.join(basis, WELT, ebene, nf), win, entfernen_praefixe)
                if b or so:
                    quellen.append('%s/%s' % (ebene, nf))
                baum += b
                if ds == 0 and dr == 0:
                    sonst += so
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
    else:
        meld('Hinweis: instanzen/instanzen.json fehlt – Houdini-Bestand unbekannt')
    baum = np.concatenate(baum, axis=0) if baum else np.zeros((0, 3), np.float32)
    sonst = np.concatenate(sonst, axis=0) if sonst else np.zeros((0, 3), np.float32)
    return baum, sonst, quellen


def lade_standorte(basis, win):
    """docs/staedte/standorte.json (optional, Format nur geraten): Liste/Dict mit x_cm/y_cm (oder x/y in m) und radius_m."""
    p = os.path.join(basis, 'docs', 'staedte', 'standorte.json')
    H, W = win[1] - win[0], win[3] - win[2]
    m = np.zeros((H, W), bool)
    if not os.path.isfile(p):
        return m, False
    try:
        d = json.load(open(p, encoding='utf-8'))
        eintraege = d if isinstance(d, list) else (d.get('standorte') or d.get('orte') or list(d.values()))
        ii, jj = np.indices((H, W), dtype=np.float32)
        for e in eintraege:
            if not isinstance(e, dict):
                continue
            if 'x_cm' in e:
                x, y = float(e['x_cm']) / 100.0, float(e['y_cm']) / 100.0
            elif 'x' in e:
                x, y = float(e['x']), float(e['y'])
                if abs(x) > 20000:
                    x, y = x / 100.0, y / 100.0
            else:
                continue
            rad = float(e.get('radius_m', e.get('radius', 60.0)))
            if rad > 2000:
                rad /= 100.0
            fj = x + X0 - win[2]
            fi = y + Y0 - win[0]
            if -rad <= fi <= H + rad and -rad <= fj <= W + rad:
                m |= (ii - fi) ** 2 + (jj - fj) ** 2 <= rad * rad
        return m, True
    except Exception as e:
        meld('Hinweis: standorte.json nicht auswertbar (%s)' % e)
        return m, False


def ufer_vorhanden(basis, feld):
    o = os.path.join(basis, WELT, 'ufer', 'foliage_' + feld)
    return os.path.isdir(o) and any(f.endswith('.f32') for f in os.listdir(o))


# ----------------------------------------------------------------------------- Kronendach
def kronendach(H, W, baum_fi, baum_fj, baum_s, licht):
    """Beschattung 0..1 aus Baumpositionen: Splat π·(r·s)² je Baum, Gauß-Glättung → Deckung, 1 − exp(−k·Deckung)."""
    deck = np.zeros((H, W), np.float32)
    if baum_fi.size:
        r = float(licht['kronen_radius_m']) * np.clip(baum_s, 0.3, 3.0)
        w = (math.pi * r * r).astype(np.float32)
        ii = np.clip(np.round(baum_fi).astype(np.int32), 0, H - 1)
        jj = np.clip(np.round(baum_fj).astype(np.int32), 0, W - 1)
        np.add.at(deck, (ii, jj), w)
        deck = gauss_blur(deck, float(licht['kronen_sigma_m']))
    besch = (1.0 - np.exp(-float(licht['beschattung_k']) * deck)).astype(np.float32)
    return besch


# ----------------------------------------------------------------------------- Streuung
def streue(lam1, raster_m, seed, kanal, wi0, wj0, H, W):
    """Jitter-Gitter-Streuung: lam1 = erwartete Instanzen je 1-m-Zelle. Liefert Fenster-Koordinaten (fi, fj) float."""
    g = max(1, int(raster_m))
    if g > 1:
        lam = blockmittel(lam1, g) * (g * g)
    else:
        lam = lam1
    Hg, Wg = lam.shape
    mx = float(lam.max()) if lam.size else 0.0
    if mx <= 0:
        return np.zeros(0, np.float32), np.zeros(0, np.float32)
    K = int(min(6, max(1, math.ceil(mx))))
    ci, cj = np.nonzero(lam > 0)
    lv = lam[ci, cj] / K
    gi = (ci * g + wi0)
    gj = (cj * g + wj0)
    fis, fjs = [], []
    for k in range(K):
        keep = hash01(gi, gj, seed, kanal * 16 + k) < lv
        if not keep.any():
            continue
        a, b = ci[keep], cj[keep]
        ui = hash01(gi[keep], gj[keep], seed, kanal * 16 + 8 + k)
        uj = hash01(gi[keep] + 7, gj[keep] + 3, seed, kanal * 16 + 8 + k)
        fis.append((a + ui) * g)
        fjs.append((b + uj) * g)
    if not fis:
        return np.zeros(0, np.float32), np.zeros(0, np.float32)
    fi = np.concatenate(fis).astype(np.float32)
    fj = np.concatenate(fjs).astype(np.float32)
    m = (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1)
    return fi[m], fj[m]


# ----------------------------------------------------------------------------- Ausgabe
def ausgabe_leeren(basis, feld):
    ausgabe = os.path.join(basis, WELT, 'nordkueste', feld)
    os.makedirs(ausgabe, exist_ok=True)
    for f in sorted(os.listdir(ausgabe)):
        if f.endswith('.f32'):
            os.remove(os.path.join(ausgabe, f))
    return ausgabe


def schreibe_leer(feld, basis, regeln, biome_fenster, zellen_zustaendig, statistik, hinweise):
    """Leerer plan.json (instanzen 0, keine f32) fuer Felder ohne eigene Biome (Konventionen §1)."""
    ausgabe = ausgabe_leeren(basis, feld)
    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': 0, 'dateien': {},
            'biome_fenster': biome_fenster, 'zellen_zustaendig': int(zellen_zustaendig), 'biome_eigen': list(regeln['biome_eigen']),
            'kollision_anzahl': 0, 'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'statistik': statistik, 'hinweise': hinweise}
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    return plan


def duenne_aus(aus, klassen_namen, ziel_je_klasse, seed):
    """Deterministische Ausduennung auf exakte Anzahl je Klasse: behalten werden die Instanzen mit dem kleinsten Hash-Rang."""
    for a in aus:
        n_ziel = ziel_je_klasse.get(a['klasse'])
        if n_ziel is None or a['fi'].size <= n_ziel:
            continue
        h = hash01(a['gmi'], a['gmj'], seed, 99991 + klassen_namen.index(a['klasse']))
        h = h + 1e-9 * np.arange(h.size, dtype=np.float64)  # stabile Reihenfolge bei gleichem Hash
        keep = np.sort(np.argsort(h, kind='stable')[:int(n_ziel)])
        for key in ('fi', 'fj', 'mi', 'mj', 'gmi', 'gmj', 'netz', 'ms', 'msz', 'yaw', 'nx', 'ny', 'nz'):
            a[key] = a[key][keep]


def budget_ziele(anzahl, klassen_reihe, ziel):
    """Ziel-Anzahl je Klasse, wenn die Summe ueber ziel liegt: von hinten (niedrigste Prioritaet) Klassen sammeln, bis 60 % ihrer
    Summe den Ueberschuss decken, diese gleichmaessig (floor) ausduennen. Liefert {klasse: neue_anzahl} (leer = nichts zu tun)."""
    gesamt = sum(anzahl.get(k, 0) for k in klassen_reihe)
    if gesamt <= ziel:
        return {}
    ueber = gesamt - ziel
    pool, summe = [], 0
    for kn in reversed(klassen_reihe):
        n = anzahl.get(kn, 0)
        if n == 0:
            continue
        pool.append(kn)
        summe += n
        if summe * 0.6 >= ueber:
            break
    f = max(0.0, 1.0 - ueber / float(max(1, summe)))
    return {kn: int(math.floor(anzahl[kn] * f)) for kn in pool}


# ----------------------------------------------------------------------------- Planung je Feld
def plane_feld(feld, basis, regeln, faktor, bild, netze, masse):
    t0 = time.time()
    rand = int(regeln.get('fenster_rand_m', 64))
    fb_, win = feld_fenster(feld, rand)
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    hinweise = []
    seed = int(regeln['seed'])
    klassen = regeln['klassen']
    klassen_namen = list(klassen.keys())
    A = regeln['abstand_m']
    meer_r = regeln['meer']
    licht = regeln['licht']

    # ---------------- Höhe, Hang, Normale
    hoehe = lade_raster(os.path.join(basis, WELT, 'hoehe.f32'), '<f4', win, pflicht=True).astype(np.float32)
    dzdi, dzdj = np.gradient(hoehe)  # m je m
    hang = np.degrees(np.arctan(np.sqrt(dzdi * dzdi + dzdj * dzdj))).astype(np.float32)
    nl = np.sqrt(dzdi * dzdi + dzdj * dzdj + 1.0)
    n_x = (-dzdj / nl).astype(np.float32)
    n_y = (-dzdi / nl).astype(np.float32)
    n_z = (1.0 / nl).astype(np.float32)
    nordhang = (n_y < -0.2) & (hang > 12)

    im_feld = np.zeros((H, W), bool)
    im_feld[fb_[0] - wi0:fb_[1] - wi0, fb_[2] - wj0:fb_[3] - wj0] = True

    # ---------------- Biome und Zustaendigkeit (Konventionen §1)
    planer = list(regeln['biome_eigen'])
    zr = regeln.get('zustaendigkeit', {})
    saum_m = float(zr.get('saum_m', 30))
    min_anteil = float(zr.get('min_anteil_eigen', 0.02))
    bio, bio_namen, bio_quelle = lade_biome(basis, win, regeln, feld, hoehe)

    def anteile(werte):
        ks, ns = np.unique(werte, return_counts=True)
        tot = float(max(1, werte.size))
        reihen = sorted(zip(ks.tolist(), ns.tolist()), key=lambda e: (-e[1], e[0]))
        return {bio_namen[k]: round(n / tot, 4) for k, n in reihen}
    biome_fenster = anteile(bio)
    biome_feld = anteile(bio[im_feld])
    eigen_m = np.isin(bio, [bio_namen.index(b) for b in planer])
    anteil_fenster = float(eigen_m.mean())
    anteil_feld = float(eigen_m[im_feld].mean())
    stat_zust = {'biom_quelle': bio_quelle, 'anteil_eigen_fenster': round(anteil_fenster, 4), 'anteil_eigen_feld': round(anteil_feld, 4),
                 'biome_feld': biome_feld, 'saum_m': saum_m, 'min_anteil_eigen': min_anteil}
    if anteil_fenster < min_anteil:
        meld('%s: Anteil fjord/kueste/bergwald im Fenster %.2f %% < %.1f %% (Quelle %s, Fenster %s) -> leerer plan.json (instanzen 0)'
             % (feld, anteil_fenster * 100, min_anteil * 100, bio_quelle, dict(list(biome_fenster.items())[:4])))
        return schreibe_leer(feld, basis, regeln, biome_fenster, 0, stat_zust,
                             ['Anteil eigener Biome im Fenster %.2f %% < %.1f %% - kein Plan' % (anteil_fenster * 100, min_anteil * 100)])
    lbl = np.full((H, W), -1, np.int16)
    for q, b in enumerate(planer):
        lbl[bio == bio_namen.index(b)] = q
    d_eigen, lbl_naechst = edt_label(eigen_m, lbl, saum_m)
    zust_f = np.where(eigen_m, 1.0, np.clip(1.0 - d_eigen / saum_m, 0.0, 1.0)).astype(np.float32)
    zust_m = zust_f > 0
    zellen_zustaendig = int((zust_m & im_feld).sum())
    stat_zust['zellen_eigen_feld'] = int((eigen_m & im_feld).sum())
    stat_zust['zellen_saum_feld'] = zellen_zustaendig - stat_zust['zellen_eigen_feld']
    if zellen_zustaendig == 0:
        meld('%s: eigene Biome nur im Rand, keine zustaendige Zelle im Feld -> leerer plan.json (instanzen 0)' % feld)
        return schreibe_leer(feld, basis, regeln, biome_fenster, 0, stat_zust, ['keine zustaendige Zelle im Feld'])
    meld('%s: Biome im Fenster %s (Quelle %s); eigen %.1f %% Fenster / %.1f %% Feld; zustaendig %d Zellen (davon Saum %d)'
         % (feld, dict(list(biome_fenster.items())[:5]), bio_quelle, anteil_fenster * 100, anteil_feld * 100,
            zellen_zustaendig, stat_zust['zellen_saum_feld']))

    # ---------------- Karten
    def r8(name):
        return lade_raster(os.path.join(basis, WELT, name + '.r8'), np.uint8, win)
    wasser = r8('karte_wasser')
    weg = r8('karte_weg')
    ort = r8('karte_ort')
    for nm, a in (('karte_wasser', wasser), ('karte_weg', weg), ('karte_ort', ort)):
        if a is None:
            hinweise.append('%s.r8 fehlt – als leer angenommen' % nm)
    wasser_m = (wasser > 0) if wasser is not None else np.zeros((H, W), bool)
    weg_m = (weg > 0) if weg is not None else np.zeros((H, W), bool)
    ort_m = (ort > 0) if ort is not None else np.zeros((H, W), bool)
    meer_m = wasser_m & (hoehe <= float(meer_r['hoehe_max_m']))
    hat_meer = bool(meer_m.any())
    d_meer = distanz(meer_m, float(meer_r['suche_bis_m']))
    d_wasser = distanz(wasser_m, 130.0)
    d_weg = distanz(weg_m, 6.0)
    d_ort = distanz(ort_m, 7.0)
    standort_m, hat_standorte = lade_standorte(basis, win)
    if hat_standorte:
        d_standort = distanz(standort_m, float(A.get('standort', 5.0)) + 1)
    else:
        d_standort = None
    # Küstentangente/Inlandrichtung aus dem Abstandsfeld (grob geglättet)
    dm_g = gauss_blur(np.minimum(d_meer, 60.0), 3.0)
    gmi, gmj = np.gradient(dm_g)
    gl = np.sqrt(gmi * gmi + gmj * gmj) + 1e-6
    inland_x = (gmj / gl).astype(np.float32)   # +X = +j
    inland_y = (gmi / gl).astype(np.float32)   # +Y = +i
    kueste_yaw = np.arctan2(inland_y, inland_x).astype(np.float32) + np.float32(math.pi / 2)

    # ---------------- Lagen
    lagen_namen = set(regeln.get('lagen_sperre', {}).keys()) | set(licht.get('fallback_lagen', {}).keys())
    for k in klassen.values():
        lagen_namen |= set(k.get('lagen', {}).keys())
        pr_ = platten_regel(k)
        if pr_:
            lagen_namen |= set(pr_['lagen_min']) | set(pr_['nicht_auf'])
        if k.get('teppich_sperre'):
            lagen_namen |= set(k['teppich_sperre'].get('lagen', ['Kies', 'Geroell', 'Fels', 'Felsplatte']))
    lagen = {}
    fehlend = []
    for ln in sorted(lagen_namen):
        a = r8('lage_' + ln)
        if a is None:
            fehlend.append(ln)
            continue
        lagen[ln] = a.astype(np.float32) / 255.0
    if fehlend:
        hinweise.append('Lagen fehlen (Faktor neutral): ' + ', '.join(fehlend))
    sperre = np.ones((H, W), np.float32)
    for ln, f in regeln.get('lagen_sperre', {}).items():
        if ln in lagen:
            sperre *= 1.0 - (1.0 - float(f)) * lagen[ln]
    fels_m = (lagen['Fels'] > 0.5) if 'Fels' in lagen else np.zeros((H, W), bool)
    d_fels = distanz(fels_m, 10.0)

    # ---------------- vorhandene Bäume, Modus
    modus = regeln.get('baum_modus', 'auto')
    bestand_da = os.path.isdir(os.path.join(basis, WELT, 'bestand', feld))
    if modus == 'auto':
        modus = 'ergaenzen' if bestand_da else 'ersetzen'
    entf = regeln.get('entfernen_bei_ersetzen', '') if modus == 'ersetzen' else ''
    ersetzen_min = float(zr.get('ersetzen_min_anteil', 0.85))
    if entf and anteil_feld < ersetzen_min:
        entf = ''
        hinweise.append('baum_modus ersetzen OHNE entfernen-Filter: Eigenanteil im Feld %.0f %% < %.0f %% (der Filter gilt feldweit und '
                        'wuerde Baeume fremder Biome loeschen); vorhandene Baeume bleiben und werden umpflanzt' % (anteil_feld * 100, ersetzen_min * 100))
    entf_praefixe = tuple(p.strip().lower() for p in entf.split(',') if p.strip())
    alt_baum, alt_sonst, quellen = lade_baeume(basis, feld, win, entf_praefixe)
    if not quellen:
        hinweise.append('keine vorhandenen Ebenen (bestand/witcher/instanzen) im Fenster gefunden')
    hinweise.append('baum_modus = %s (bestand/%s %s)' % (modus, feld, 'vorhanden' if bestand_da else 'fehlt'))
    ufer_da = ufer_vorhanden(basis, feld)
    if ufer_da:
        hinweise.append('Ufer-Ebene FT_EL_UF_* vorhanden – Strandkiesel/-platten auf Ergänzungsfaktor')

    alt_m = np.zeros((H, W), bool)
    if alt_baum.size:
        alt_m[np.clip(np.round(alt_baum[:, 0]).astype(np.int32), 0, H - 1), np.clip(np.round(alt_baum[:, 1]).astype(np.int32), 0, W - 1)] = True
    d_altbaum = distanz(alt_m, 6.0)
    sonst_m = np.zeros((H, W), bool)
    if alt_sonst.size:
        sonst_m[np.clip(np.round(alt_sonst[:, 0]).astype(np.int32), 0, H - 1), np.clip(np.round(alt_sonst[:, 1]).astype(np.int32), 0, W - 1)] = True

    # ---------------- Biomfaktor je Zelle je Ebene
    bfe = regeln['biom_faktor_ebene']

    def biom_faktor(kl, ebene):
        """Biomfaktor je Zelle (eigenes Biom, im Saum das naechste eigene Biom) x Zustaendigkeit (1 innen, linear 0 bei saum_m)."""
        f = np.zeros((H, W), np.float32)
        for q, b in enumerate(planer):
            fb = float(kl['biome'].get(b, 0.0)) * float(bfe.get(b, {}).get(str(ebene), 1.0))
            if fb > 0:
                f[lbl_naechst == q] = fb
        return f * zust_f

    # ---------------- harte Sperren
    hang_sperre = float(regeln.get('hang_sperre_grad', 40))
    sperr_basis = wasser_m | dilate(wasser_m, float(A['wasser'])) | (d_ort < float(A['ort'])) | ~np.isfinite(hoehe)
    if d_standort is not None:
        sperr_basis |= d_standort < float(A.get('standort', 5.0))
    sperr_klein = sperr_basis | (d_weg < float(A['weg_klein'])) | (d_altbaum < float(A['baum_klein'])) | dilate(sonst_m, 0.5)
    sperr_gross = sperr_basis | (d_weg < float(A['weg_gross'])) | (d_altbaum < float(A['bestand_baum']))

    # ---------------- Zustand
    aus = []           # Instanzlisten je Klasse
    neu_baum = []      # (fi, fj, s) der hier geplanten Bäume
    stat = {}
    besch = None
    wald = saum = lichtungsrand = None
    d_neubaum = np.full((H, W), 99.0, np.float32)

    def licht_felder(besch_):
        w = besch_ > float(licht['wald_schwelle'])
        aussen = dilate(w, float(licht['saum_aussen_m'])) & ~w
        innen = w & ~(~dilate(~w, float(licht['saum_innen_m'])))
        s = aussen | innen
        umgebung = dilate(w, 25.0)
        lichtung = umgebung & (besch_ < float(licht['lichtung_schwelle'])) & ~aussen
        lr = dilate(lichtung, float(licht['lichtungsrand_m'])) & w
        return w, s, lr

    for ebene in EBENEN:
        es = int(regeln['seed_je_ebene'].get(ebene, 0))
        eb_klassen = [kn for kn in klassen_namen if str(klassen[kn]['ebene']) == ebene]
        if ebene != '2' and besch is None:
            # Kronendach aus alten + neuen Bäumen
            fi_all = [alt_baum[:, 0]] + [b[0] for b in neu_baum]
            fj_all = [alt_baum[:, 1]] + [b[1] for b in neu_baum]
            s_all = [alt_baum[:, 2]] + [b[2] for b in neu_baum]
            fi_all = np.concatenate(fi_all) if fi_all else np.zeros(0, np.float32)
            fj_all = np.concatenate(fj_all) if fj_all else np.zeros(0, np.float32)
            s_all = np.concatenate(s_all) if s_all else np.zeros(0, np.float32)
            if fi_all.size == 0:
                besch = np.zeros((H, W), np.float32)
                for ln, f in licht.get('fallback_lagen', {}).items():
                    if ln in lagen:
                        besch = np.maximum(besch, lagen[ln] * float(f))
                besch = np.minimum(besch, float(licht.get('fallback_beschattung_max', 0.7)))
                hinweise.append('keine Bäume bekannt – Beschattung aus Lagen (Nadeln/Laub/Moos) geschätzt')
            else:
                besch = kronendach(H, W, fi_all, fj_all, s_all, licht)
            wald, saum, lichtungsrand = licht_felder(besch)
            nm = np.zeros((H, W), bool)
            for b in neu_baum:
                nm[np.clip(np.round(b[0]).astype(np.int32), 0, H - 1), np.clip(np.round(b[1]).astype(np.int32), 0, W - 1)] = True
            d_neubaum = distanz(nm, 10.0)
            d_baum = np.minimum(d_altbaum, d_neubaum)
        elif ebene == '2':
            # Bäume: Licht aus Lagen-Schätzung nur für Tanne (Schatten) – vereinfachend 0 (offen)
            d_baum = d_altbaum
            besch_b = np.zeros((H, W), np.float32)
            wald_b = dilate(alt_m, 8.0)
            saum_b = dilate(wald_b, float(licht['saum_aussen_m'])) & ~wald_b
            lr_b = np.zeros((H, W), bool)

        for kn in eb_klassen:
            kl = klassen[kn]
            kidx = klassen_namen.index(kn)
            kanal = 100 + kidx
            if ebene == '2':
                b_, w_, s_, lr_ = besch_b, wald_b, saum_b, lr_b
            else:
                b_, w_, s_, lr_ = besch, wald, saum, lichtungsrand
            # Dichte je 1-m-Zelle
            d0, d1 = [float(v) for v in kl['dichte']]
            d = d0 * (1 - b_) + d1 * b_
            if 'dichte_hang' in kl:
                d = np.full((H, W), float(kl['dichte_hang']), np.float32)
            d = d * biom_faktor(kl, ebene) * sperre
            # Lagen
            lg = kl.get('lagen', {})
            if lg:
                if kl.get('lagen_modus', 'gewicht') == 'nur':
                    f = np.zeros((H, W), np.float32)
                    for ln, w in lg.items():
                        if ln in lagen:
                            f += float(w) * lagen[ln]
                    if not any(ln in lagen for ln in lg):
                        f = np.ones((H, W), np.float32)  # ohne Lagen: neutral
                else:
                    f = np.ones((H, W), np.float32)
                    for ln, w in lg.items():
                        if ln in lagen:
                            f += (float(w) - 1.0) * lagen[ln]
                d *= np.clip(f, 0, 4)
            # Korrektur Runde 2: Platten nur auf Kies/Geroell/Fels/Felsplatte >= 100, nie auf Gras/Wiese; Kiesel kein Hangteppich
            pr = platten_regel(kl)
            if pr:
                d *= platten_maske(lagen, pr, (H, W))
                if not any(ln in lagen for ln in pr['lagen_min']):
                    hinweise.append('%s: keine Fels-Lagen gefunden - Platten-Klasse ohne Instanzen (Runde 2)' % kn)
            if kl.get('teppich_sperre'):
                d *= teppich_maske(lagen, kl['teppich_sperre'], d_weg, d_wasser, (H, W))
            # Hang
            hv, hn = kl.get('hang', [30, 40])
            d *= rampe_ab(hang, float(hv), float(hn))
            if 'hang_min' in kl:
                d *= rampe_auf(hang, float(kl['hang_min'][0]), float(kl['hang_min'][1]))
            if not kl.get('kletter'):
                d[hang > hang_sperre] = 0
            # Höhe
            if 'hoehe' in kl:
                d *= rampe_ab(hoehe, float(kl['hoehe'][0]), float(kl['hoehe'][1]))
            if 'hoehe_min' in kl:
                d *= rampe_auf(hoehe, float(kl['hoehe_min'][0]), float(kl['hoehe_min'][1]))
            # Küste / Wasser
            if 'kueste' in kl:
                if hat_meer:
                    d *= trapez(d_meer, kl['kueste'])
                elif kl.get('kueste_nur'):
                    d[:] = 0
            if 'wasser' in kl:
                fern = float(kl.get('wasser_faktor_fern', 1.0))
                d *= fern + (1 - fern) * trapez(d_wasser, kl['wasser'])
            # Saum / Lichtung / Waldgrenze / Nordhang
            if 'saum_faktor' in kl:
                d *= 1 + (float(kl['saum_faktor']) - 1) * s_
            if 'lichtung_faktor' in kl:
                d *= 1 + (float(kl['lichtung_faktor']) - 1) * lr_
            if 'nordhang_faktor' in kl:
                d *= 1 + (float(kl['nordhang_faktor']) - 1) * nordhang
            if 'waldgrenze_faktor' in kl:
                wg = regeln['waldgrenze']
                band = (hoehe > float(wg['voll_bis_m']) - 40) & (hoehe < float(wg['krueppel_bis_m']))
                d *= 1 + (float(kl['waldgrenze_faktor']) - 1) * band
            # Nähe Fels / Baum
            if 'fels_nah' in kl:
                d *= 1 + (float(kl['fels_nah']['faktor']) - 1) * (d_fels < float(kl['fels_nah']['bis_m']))
            if 'baum_nah' in kl:
                nah = d_baum < float(kl['baum_nah']['bis_m'])
                if kl.get('baum_nah_nur'):
                    d *= nah
                else:
                    d *= 1 + (float(kl['baum_nah']['faktor']) - 1) * nah
            if kl.get('ufer_vorhanden_faktor') is not None and ufer_da:
                d *= float(kl['ufer_vorhanden_faktor'])
            # Klumpung
            if 'klumpung' in kl:
                km = kl['klumpung']
                n = wertrauschen(H, W, wi0, wj0, float(km['skala_m']), seed + es, kanal * 2)
                t = np.clip((n - float(km['schwelle'])) / 0.3, 0, 1)
                d *= (1 - float(km['staerke'])) + float(km['staerke']) * t
            # Modus Bäume
            if ebene == '2' and modus == 'ergaenzen':
                d *= float(regeln.get('ergaenzen_faktor', 0.35))
            d *= faktor
            # Sperren
            gross = bool(kl.get('kollision')) or kl.get('abstand_weg') == 'gross' or kl.get('baum')
            d[sperr_gross if gross else sperr_klein] = 0
            if ebene == '2':
                d[d_baum < float(A['baum_baum'])] = 0
            if float(d.max()) <= 0:
                continue
            # Gruppen?
            if 'gruppe_n' in kl:
                ga, gb = int(kl['gruppe_n'][0]), int(kl['gruppe_n'][1])
                mittel = 0.5 * (ga + gb)
                cfi, cfj = streue(d / mittel, kl.get('raster_m', 1), seed + es, kanal, wi0, wj0, H, W)
                if cfi.size == 0:
                    continue
                gci = np.round(cfi).astype(np.int64) + wi0
                gcj = np.round(cfj).astype(np.int64) + wj0
                n = ga + np.minimum((hash01(gci, gcj, seed + es, kanal * 16 + 14) * (gb - ga + 1)).astype(np.int64), gb - ga)
                rep = np.repeat(np.arange(cfi.size), n)
                k = np.arange(rep.size, dtype=np.int64) - np.repeat(np.cumsum(n) - n, n)  # 0..n_g−1 je Gruppe, vektorisiert
                r0, r1 = [float(v) for v in kl['gruppe_radius_m']]
                rad = (r0 + (r1 - r0) * hash01(gci[rep], gcj[rep] + 11, seed + es, kanal * 16 + 15 + 0)) * np.sqrt(hash01(gci[rep] + k, gcj[rep], seed + es, kanal * 16 + 13))
                ang = hash01(gci[rep] + 3 * k, gcj[rep] + k, seed + es, kanal * 16 + 12) * 2 * math.pi
                fi = cfi[rep] + rad * np.sin(ang)
                fj = cfj[rep] + rad * np.cos(ang)
                ok = (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1)
                fi, fj = fi[ok], fj[ok]
                mi = np.round(fi).astype(np.int32)
                mj = np.round(fj).astype(np.int32)
                ok = d[mi, mj] > 0
                fi, fj, mi, mj = fi[ok], fj[ok], mi[ok], mj[ok]
            else:
                fi, fj = streue(d, kl.get('raster_m', 1), seed + es, kanal, wi0, wj0, H, W)
                if fi.size == 0:
                    continue
                mi = np.round(fi).astype(np.int32)
                mj = np.round(fj).astype(np.int32)
            if fi.size == 0:
                continue
            gmi, gmj = mi.astype(np.int64) + wi0, mj.astype(np.int64) + wj0
            # Bäume: Mindestabstand untereinander (eine je Zelle von baum_baum m) und zu schon geplanten Bäumen
            if ebene == '2':
                ok = d_neubaum[mi, mj] >= float(A['baum_baum'])
                fi, fj, mi, mj, gmi, gmj = fi[ok], fj[ok], mi[ok], mj[ok], gmi[ok], gmj[ok]
                if fi.size == 0:
                    continue
                cs = float(A['baum_baum'])
                zelle = (np.floor(fi / cs).astype(np.int64) * 100000 + np.floor(fj / cs).astype(np.int64))
                prio = hash01(gmi, gmj, seed + es, kanal * 16 + 11)
                ordn = np.lexsort((prio, zelle))
                zs = zelle[ordn]
                erste = np.ones(zs.size, bool)
                erste[1:] = zs[1:] != zs[:-1]
                keep = ordn[erste]
                fi, fj, mi, mj, gmi, gmj = fi[keep], fj[keep], mi[keep], mj[keep], gmi[keep], gmj[keep]
            # nur im Feld und nur auf Zellen mit Dichte > 0 (zustaendig, nicht gesperrt; Jitter-Gitter > 1 m kann sonst ueber die
            # Saumgrenze oder auf Sperrzellen fallen)
            ok = im_feld[mi, mj] & (d[mi, mj] > 0) & zust_m[mi, mj]
            fi, fj, mi, mj, gmi, gmj = fi[ok], fj[ok], mi[ok], mj[ok], gmi[ok], gmj[ok]
            if fi.size == 0:
                continue
            # Netzwahl, Maßstab, Yaw
            hv_ = (hash01(gmi, gmj, seed + es, kanal * 16 + 5) + 0.37 * hash01(np.round(fi * 7).astype(np.int64), np.round(fj * 7).astype(np.int64), seed + es, kanal * 16 + 6)) % 1.0
            netzl = kl['netze']
            nidx = np.minimum((hv_ * len(netzl)).astype(np.int32), len(netzl) - 1)
            m0, m1 = [float(v) for v in kl['massstab']]
            u_s = hash01(gmi, gmj, seed + es, kanal * 16 + 7)
            if kl.get('hoehe_kohaerenz'):
                sk = float(kl.get('gruppen_skala_m', 18))
                n = wertrauschen(H, W, wi0, wj0, sk, seed + es, kanal * 2 + 40)[mi, mj]
                u_s = (1 - float(kl['hoehe_kohaerenz'])) * u_s + float(kl['hoehe_kohaerenz']) * n
            ms = (m0 + (m1 - m0) * u_s).astype(np.float32)
            msz = ms.copy()
            yawmodus = kl.get('yaw', 'zufall')
            yr = hash01(gmi, gmj, seed + es, kanal * 16 + 8)
            if yawmodus == 'hang':
                asp = np.arctan2(-dzdi[mi, mj], -dzdj[mi, mj])  # hangabwärts, Winkel in (X=j, Y=i)
                yaw = asp + (yr - 0.5) * math.radians(40) + np.where(hash01(gmi, gmj, seed + es, kanal * 16 + 9) < 0.5, 0.0, math.pi)
            elif yawmodus == 'kueste' and hat_meer:
                yaw = kueste_yaw[mi, mj] + (yr - 0.5) * math.radians(40) + np.where(hash01(gmi, gmj, seed + es, kanal * 16 + 9) < 0.5, 0.0, math.pi)
            else:
                yaw = yr * 2 * math.pi
            # Normale (Gelände) und Windflucht
            nx_, ny_, nz_ = n_x[mi, mj], n_y[mi, mj], n_z[mi, mj]
            kipp = float(kl.get('kippen', 0.3))
            if pr:
                kipp = max(kipp, float(pr['kippen']))  # Platten an der Gelaendenormale
            if kl.get('kueste_windflucht') and hat_meer:
                wb = float(meer_r['windflucht_bis_m'])
                st = np.clip(1.0 - d_meer[mi, mj] / wb, 0, 1)  # 1 direkt am Wasser
                z0, z1 = [float(v) for v in meer_r['windflucht_z']]
                msz = ms * (z1 - (z1 - z0) * st)
                g0, g1 = [float(v) for v in meer_r['windflucht_neigung_grad']]
                neig = np.radians(g0 + (g1 - g0) * st) * (st > 0)
                tx = inland_x[mi, mj] * np.tan(neig)
                ty = inland_y[mi, mj] * np.tan(neig)
                # Lee-Neigung mit Geländenormale (Anteil kippen) mischen
                nx_ = kipp * nx_ + tx
                ny_ = kipp * ny_ + ty
                nz_ = kipp * nz_ + (1 - kipp)
                l = np.sqrt(nx_ * nx_ + ny_ * ny_ + nz_ * nz_) + 1e-9
                nx_, ny_, nz_ = nx_ / l, ny_ / l, nz_ / l
                kipp = 1.0
            aus.append(dict(klasse=kn, ebene=ebene, fi=fi.astype(np.float32), fj=fj.astype(np.float32), mi=mi, mj=mj, gmi=gmi, gmj=gmj,
                            netz=nidx, ms=ms, msz=msz.astype(np.float32), yaw=yaw.astype(np.float32), nx=nx_.astype(np.float32),
                            ny=ny_.astype(np.float32), nz=nz_.astype(np.float32), kippen=kipp, kollision=bool(kl.get('kollision'))))
            stat[kn] = int(fi.size)
            if ebene == '2':
                neu_baum.append((fi.astype(np.float32), fj.astype(np.float32), ms))
                nm = np.zeros((H, W), bool)
                nm[mi, mj] = True
                d_neubaum = np.minimum(d_neubaum, distanz(nm, 6.0))

    # ---------------- Budget (Konventionen §3): Schicht-Ziele, Feld-Ziel, Kollision; exakt und deterministisch
    Bg = regeln['budget']
    prio = [k for k in Bg['prioritaet'] if k in klassen]
    reihe = prio + sorted(k for k in klassen_namen if k not in prio)  # unbekannte Klassen = niedrigste Prioritaet
    hart = int(Bg.get('instanzen_je_feld', 60000))
    koll_hart = int(Bg.get('kollision_je_feld', 3000))

    def anzahl_je_klasse():
        n = {}
        for a in aus:
            n[a['klasse']] = n.get(a['klasse'], 0) + int(a['fi'].size)
        return n
    roh = sum(int(a['fi'].size) for a in aus)
    for ebene in EBENEN:
        ziel = min(int(Bg.get('ziel_je_ebene', {}).get(ebene, hart)), hart)
        anz = anzahl_je_klasse()
        r_e = [k for k in reihe if str(klassen[k]['ebene']) == ebene]
        z = budget_ziele(anz, r_e, ziel)
        if z:
            vor = sum(anz.get(k, 0) for k in r_e)
            duenne_aus(aus, klassen_namen, z, seed)
            meld('WARNUNG %s: Schicht %s %d > Ziel %d - ausgeduennt %s' % (feld, ebene, vor, ziel, {k: '%d->%d' % (anz[k], v) for k, v in z.items()}))
            hinweise.append('Schicht %s: %d -> Ziel %d, ausgeduennt %s' % (ebene, vor, ziel, sorted(z)))
            if ebene == '0':
                hinweise.append('Budget knapp: Kleinzeug (Nadelstreu/Kiesel/Moos) bevorzugt ueber Landschafts-Gras (GT_*) abdecken')
    ziel_feld = min(int(Bg.get('ziel_je_feld', hart)), hart)
    anz = anzahl_je_klasse()
    z = budget_ziele(anz, reihe, ziel_feld)
    if z:
        vor = sum(anz.values())
        duenne_aus(aus, klassen_namen, z, seed)
        meld('WARNUNG %s: Feld %d > Ziel %d - ausgeduennt %s' % (feld, vor, ziel_feld, {k: '%d->%d' % (anz[k], v) for k, v in z.items()}))
        hinweise.append('Feld: %d -> Ziel %d, ausgeduennt %s' % (vor, ziel_feld, sorted(z)))
    anz = anzahl_je_klasse()
    koll_kl = [k for k in reihe if klassen[k].get('kollision')]
    koll = sum(anz.get(k, 0) for k in koll_kl)
    if koll > koll_hart:
        f = koll_hart / float(koll)
        z = {k: int(math.floor(anz[k] * f)) for k in koll_kl if anz.get(k, 0)}
        duenne_aus(aus, klassen_namen, z, seed)
        meld('WARNUNG %s: Kollision %d > %d - alle Kollisionsklassen x %.3f' % (feld, koll, koll_hart, f))
        hinweise.append('Kollisionsbudget: %d -> <= %d (Faktor %.3f auf alle Kollisionsklassen)' % (koll, koll_hart, f))
    budget_info = {'roh': int(roh), 'ziel_je_feld': ziel_feld, 'hart_je_feld': hart, 'kollision_hart': koll_hart}

    # ---------------- Instanzen bauen und schreiben
    ausgabe = ausgabe_leeren(basis, feld)
    dateien, netz_inst, stat, nk = {}, {}, {}, 0
    name_ebene = {}
    for a in aus:
        n = a['fi'].size
        if n == 0:
            continue
        kl = klassen[a['klasse']]
        pfade = kl['netze']
        hz = np.array([(netze.get(p, (1, 1, 0.5))[2] if netze else 0.5) for p in pfade], np.float32)[a['netz']]
        minz = np.zeros(len(pfade), np.float32)
        for q, p in enumerate(pfade):
            if p in masse:
                try:
                    minz[q] = float(masse[p]['min'][2]) / 100.0
                except Exception:
                    pass
        minz = minz[a['netz']]
        eg = kl.get('eingraben', {'cm': 3})
        pr = platten_regel(kl)
        if 'anteil' in eg or pr:
            ant = float(eg.get('anteil', 0.0))
            if pr:
                ant = max(ant, float(pr['eingraben_min_anteil']))  # Runde 2: Platten >= 50 % der Netzhoehe eingraben
            ein = ant * hz * a['msz']
        else:
            ein = np.full(n, float(eg.get('cm', 3)) / 100.0, np.float32)
        z = bilinear(hoehe, a['fi'], a['fj']) - minz * a['msz'] - ein
        x = (a['fj'] + wj0 - X0) * 100.0
        y = (a['fi'] + wi0 - Y0) * 100.0
        q = quaternionen(a['nx'], a['ny'], a['nz'], a['kippen'], a['yaw'])
        inst = np.zeros((n, 10), np.float32)
        inst[:, 0], inst[:, 1], inst[:, 2] = x, y, z * 100.0
        inst[:, 3:7] = q
        inst[:, 7] = inst[:, 8] = a['ms']
        inst[:, 9] = a['msz']
        for ni in np.unique(a['netz']):
            m = a['netz'] == ni
            p = pfade[ni]
            base = p.rsplit('/', 1)[-1]
            name = base
            if base in name_ebene and name_ebene[base] != a['ebene']:
                name = '%s_e%s' % (base, a['ebene'])
            else:
                name_ebene[base] = a['ebene']
            netz_inst.setdefault(name, []).append(inst[m])
            if name not in dateien:
                dateien[name] = {'pfad': p, 'anzahl': 0, 'gruppe': a['klasse'], 'rolle': kl['rolle'], 'ebene': int(a['ebene']),
                                 'sichtweite': list(kl['sichtweite']), 'schatten': bool(kl.get('schatten', True)),
                                 'kollision': bool(kl.get('kollision', False))}
            dateien[name]['anzahl'] += int(m.sum())
        stat[a['klasse']] = stat.get(a['klasse'], 0) + n
        if a['kollision']:
            nk += n
    gesamt = 0
    je_ebene = {}
    for name, teile in netz_inst.items():
        arr = np.concatenate(teile, axis=0).astype('<f4')
        arr.tofile(os.path.join(ausgabe, name + '.f32'))
        gesamt += arr.shape[0]
        e = str(dateien[name]['ebene'])
        je_ebene[e] = je_ebene.get(e, 0) + arr.shape[0]
    if gesamt > hart or nk > koll_hart:  # darf nach der exakten Ausduennung nicht vorkommen
        raise RuntimeError('Budget verletzt: %d Instanzen / %d Kollision' % (gesamt, nk))
    stat_zust.update(budget_info)
    plan = {'stand': time.strftime('%Y-%m-%d %H:%M'), 'feld': feld, 'instanzen': int(gesamt), 'dateien': dateien,
            'biome_fenster': biome_fenster, 'zellen_zustaendig': zellen_zustaendig, 'biome_eigen': planer, 'kollision_anzahl': int(nk),
            'ft_ordner': regeln['ft_ordner'], 'ft_praefix': regeln['ft_praefix'],
            'statistik': {'je_klasse': stat, 'je_ebene': je_ebene, 'kollision': int(nk), 'zustaendigkeit': stat_zust,
                          'meer_im_fenster': hat_meer, 'wald_anteil': round(float(wald[im_feld].mean()), 3) if wald is not None else None,
                          'beschattung_mittel': round(float(besch[im_feld].mean()), 3) if besch is not None else None,
                          'alte_baeume_im_fenster': int(alt_baum.shape[0]), 'quellen': quellen, 'faktor': faktor,
                          'baum_modus': modus, 'laufzeit_s': round(time.time() - t0, 1), 'numba': NUMBA},
            'hinweise': hinweise, 'ungetestet': 'Planer in der Cloud nur mit synthetischen Daten rauchgetestet'}
    if entf:
        plan['entfernen'] = entf
    with open(os.path.join(ausgabe, 'plan.json'), 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    meld('%s: %d Instanzen (%d mit Kollision), je Ebene %s, %d Netze, %.1f s' % (feld, gesamt, nk, je_ebene, len(dateien), time.time() - t0))
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
        g = np.clip((hh - hh.min()) / max(1e-3, float(hh.max() - hh.min())), 0, 1) * 110 + 70
        rgb = np.stack([g, g, g], axis=2).astype(np.float32)
        if besch is not None:
            b = besch[fi0:fi1, fj0:fj1]
            rgb[..., 0] *= (1 - 0.4 * b)
            rgb[..., 2] *= (1 - 0.4 * b)
        rgb[hang[fi0:fi1, fj0:fj1] > hang_sperre] *= np.array([1.0, 0.85, 0.85], np.float32)
        rgb[wasser_m[fi0:fi1, fj0:fj1]] = (40, 80, 200)
        rgb[meer_m[fi0:fi1, fj0:fj1]] = (20, 50, 160)
        rgb[weg_m[fi0:fi1, fj0:fj1]] = (120, 80, 40)
        rgb[ort_m[fi0:fi1, fj0:fj1]] = (200, 40, 40)
        farben = regeln.get('farben', {})
        # Zustaendigkeit: fremde Biome abgedunkelt, Saum orange (Deckkraft mit dem Dichtefaktor), Biomgrenze weiss
        zf = zust_f[fi0:fi1, fj0:fj1]
        em = eigen_m[fi0:fi1, fj0:fj1]
        rgb[zf <= 0] *= float(farben.get('fremd_abdunkeln', 0.5))
        sm = (zf > 0) & ~em
        if sm.any():
            oc = np.array(farben.get('saum', [255, 150, 0]), np.float32)
            al = (0.2 + 0.5 * zf[sm])[:, None]
            rgb[sm] = rgb[sm] * (1 - al) + oc[None, :] * al
        rgb[em & dilate1(~em, False)] = (255, 255, 255)
        jk = farben.get('je_klasse', {})
        for e in ('0', '5', '1', '2'):
            for a in aus:
                if a['ebene'] != e or a['fi'].size == 0:
                    continue
                c = jk.get(a['klasse'], farben.get(e, [255, 255, 255]))
                pi = np.clip(np.round(a['fi']).astype(np.int32) - fi0, 0, fi1 - fi0 - 1)
                pj = np.clip(np.round(a['fj']).astype(np.int32) - fj0, 0, fj1 - fj0 - 1)
                rgb[pi, pj] = c
                if e == '2':
                    rgb[np.minimum(pi + 1, fi1 - fi0 - 1), pj] = c
                    rgb[pi, np.minimum(pj + 1, fj1 - fj0 - 1)] = c
        od = os.path.join(basis, 'docs', 'pruefung', 'nordkueste')
        os.makedirs(od, exist_ok=True)
        Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(os.path.join(od, feld + '.png'))
        meld('Pruefbild:', os.path.join(od, feld + '.png'))
    return plan


def _pfade_in(obj):
    """Alle Unreal-Pfade (Strings, die mit /Game/ beginnen) in einer verschachtelten JSON-Struktur."""
    if isinstance(obj, str):
        return [obj] if obj.startswith('/Game/') else []
    if isinstance(obj, dict):
        return [p for v in obj.values() for p in _pfade_in(v)]
    if isinstance(obj, list):
        return [p for v in obj for p in _pfade_in(v)]
    return []


def pruefe_netze(regeln, netze):
    """Jeden Netzpfad gegen daten/netze.csv pruefen; fehlende aus den Klassen entfernen (Warnung). Pfade in den Overrides
    (mittelschicht/felsgruppen/spuren) werden nur gemeldet - die lesenden Planer pruefen selbst."""
    for kn, kl in regeln['klassen'].items():
        ok = [p for p in kl['netze'] if p in netze]
        for p in kl['netze']:
            if p not in netze:
                meld('WARNUNG: Netz nicht im Inventar, uebersprungen: %s (Klasse %s)' % (p, kn))
        kl['netze'] = ok
    for kn in [kn for kn, kl in regeln['klassen'].items() if not kl['netze']]:
        meld('WARNUNG: Klasse %s hat kein gueltiges Netz - deaktiviert' % kn)
        del regeln['klassen'][kn]
    for ov in ('mittelschicht_overrides', 'felsgruppen_overrides', 'spuren_overrides'):
        fehl = sorted(set(p for p in _pfade_in(regeln.get(ov, {})) if p not in netze))
        for p in fehl:
            meld('WARNUNG: %s nennt ein Netz, das nicht im Inventar steht: %s' % (ov, p))


def main():
    ap = argparse.ArgumentParser(description='Eldarien Nordkuesten-Planer (biome_eigen fjord, kueste, bergwald): Schichten 0 boden, '
                                             '1 Sonderformen, 2 baum, 5 wasserkante')
    ap.add_argument('felder', nargs='+')
    ap.add_argument('--bild', action='store_true')
    ap.add_argument('--faktor', type=float, default=1.0)
    ap.add_argument('--basis', default='.')
    ap.add_argument('--regeln', default=None)
    a = ap.parse_args()
    rp = a.regeln or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nordkueste_regeln.json')
    if not os.path.isfile(rp):
        meld('FEHLER: Regeldatei fehlt: %s' % rp)
        sys.exit(2)
    try:
        regeln = json.load(open(rp, encoding='utf-8'))
    except Exception as e:
        meld('FEHLER: Regeldatei unlesbar: %s (%s)' % (rp, e))
        sys.exit(2)
    if not NUMBA:
        meld('numba nicht verfuegbar - reiner NumPy-Pfad (ausreichend)')
    try:
        netze = lade_netze(a.basis)
    except Pflichtfehler as e:
        meld('FEHLER: %s' % e)
        sys.exit(2)
    masse = lade_masse(a.basis)
    pruefe_netze(regeln, netze)
    rc = 0
    for feld in a.felder:
        feld = feld.strip().upper()
        try:
            plane_feld(feld, a.basis, regeln, a.faktor, a.bild, netze, masse)
        except Pflichtfehler as e:
            meld('ABBRUCH %s: %s' % (feld, e))
            rc = 2
        except MemoryError:
            meld('ABBRUCH %s: Speicher' % feld)
            rc = max(rc, 1)
    sys.exit(rc)


if __name__ == '__main__':
    main()
