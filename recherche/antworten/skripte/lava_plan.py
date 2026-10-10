#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lava_plan.py – Planer Biom „Lava“ (Auftrag 11, Teil B, Gruppe 8) für Eldarien (UE 5.8.3, 1-m-Raster 9577 × 7057).

*** UNGETESTET MIT ECHTDATEN *** – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern rauchgetestet (Feld C6: Schlackenkegel,
Lavastrom, See, Weg, Ort; 42 169 Instanzen in 4 s, deterministisch; Randfeld J7 ohne Lava: 0 Instanzen, kein Fehler).
Korrekturen bitte als auftraege/verteilung-lava-korrektur.md.

Was das Skript tut
------------------
Je Gitterfeld wird ein Fenster (Feld + 64 m Rand) aus hoehe.f32 per np.memmap gelesen; Hang, Normale und Krümmung kommen aus
NumPy-Faltungen. Aus eigner.r8 + welt.json (Vulkanregion = lava; Kennzahl 0 = Weltgelände → Lage-Erkennung Lavafels+Lavasand)
entsteht die Lava-Maske; der Abstand zum Biomrand wird per Dilatation (2-m-Stufe) berechnet. Daraus die **Zonierung nach Alter
des Lavastroms** (alter 0..1 aus Lage Moos/Gras, Randnähe, 300-m-Wertrauschen, Lavafels-Abzug):
  frisch   schwarz-kahl: Schlacke, Lavakiesel-Ersatz, Fumarolen; keine Pflanzen
  alt      Moospolster, Flechtensteine (Wulstlava-Ersatz), einzelne verkohlte Stümpfe
  rand     Pioniersträucher, Horstgras, Krüppelkiefern, tote Bäume
  uebergang außerhalb der Lava bis 100 m: Aschestaub-Saum in Aue/Bergwald (verkohltes Holz, Totbäume, Gras)
Schlackenkegel (lokale Maxima mit Prominenz ≥ 15 m) bekommen Flanken-Faktoren (Schlacke 2,2×, Pflanzen 0,3×).
Schichten: 0 boden (schlacke, kiesel, asche), 1 mittel (moos, flechtenstein, pionier, kiefer_strauch, verkohlt_*, gras),
2 baum (baum_tot, baum_kiefer; nur rand/uebergang), 5 wasserkante (ufer_block, schwarzkies, saeule als Akteure).
3 fels / 4 spuren setzen felsgruppen_plan.py / spuren_plan.py mit den Overrides, die dieses Skript in plan.json schreibt.
Punktliste `punkte` (Fumarolen mit Stärke/Radius/Schwefel, Dampf an Wasserkanten, Kegelgipfel, Spire-/Höhlen-/Schwefelgruben-/
Opferstätten-Vorschläge) für Niagara, Teil C und Teil D.
Zufall deterministisch: 64-bit-Hash aus (Seed, Klasse, Weltraster-Koordinate); Nachbarfelder liefern im Rand dieselben Instanzen.

Aufruf
------
  python -I scripts/lava/lava_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
  --basis   production-Wurzel (Default "."), darunter export/unreal/welt/, daten/netze.csv, daten/netze_masse.json, docs/
  --regeln  Regeldatei (Default: lava_regeln.json neben dem Skript)
  --faktor  Dichtefaktor für alle Klassen (Budget-Deckel bleibt)
  --bild    Draufsicht docs/pruefung/lava/<Feld>.png (1 px = 1 m; Hintergrund = Zone, Punkte = Instanzen, Kreuze = punkte)

Eingaben (export/unreal/welt/): hoehe.f32 (Pflicht), lage_<Name>.r8 (optional), karte_wasser/weg/ort.r8 (optional),
eigner.r8 + welt.json (optional, sonst Feld-Fallback + Lage-Erkennung), bestand/<Feld>/, witcher/<Feld>/, ufer/foliage_<Feld>/,
instanzen/instanzen.json (optional, Abstand). daten/netze.csv (Pflicht: Netzmaße, Pfadprüfung), daten/netze_masse.json (optional).

Ausgabe (FORMAT.md §3)
----------------------
  export/unreal/welt/lava/<Feld>/<Netzname>.f32        10 float32 LE je Instanz: x,y,z cm; qx,qy,qz,qw; sx,sy,sz
  export/unreal/welt/lava/<Feld>/akteur_<Netzname>.f32  Akteure (Basaltsäulen-Ersatz), dateien-Eintrag rolle "akteur"
  export/unreal/welt/lava/<Feld>/plan.json              stand, feld, ebene, instanzen, dateien{pfad, anzahl, gruppe, rolle, schicht,
                                                        sichtweite, schatten, kollision, hinweis}, entfernen, ft_ordner, ft_praefix,
                                                        punkte[], zonen, felsgruppen_overrides, spuren_overrides, hinweise

Quellen: antworten/verteilung-lava.md (Regeln, Zahlen, Referenzen Island/Teneriffa/Hawaii/Ätna), antworten/skripte/lava_regeln.json,
vorlagen/FORMAT.md (Raster, Instanzformat, Budgets), antworten/assets-taxonomie.md (Paletten, Kollisionslücke Lava_Volcano),
antworten/bildkritik-witcher-messlatte.md (Größenstaffelung, Cluster, Eingraben). Nur NumPy; numba optional (nicht benötigt).
"""
import argparse
import csv
import json
import math
import os
import sys
import time

import numpy as np

np.seterr(over="ignore")  # uint64-Hash-Multiplikation darf überlaufen

try:  # numba ist optional; alles läuft rein mit NumPy
    import numba  # noqa: F401
    HAVE_NUMBA = True
except Exception:  # pragma: no cover
    HAVE_NUMBA = False

NX, NY, FELD = 9577, 7057, 1008
X0, Y0 = 4730.5, 4060.5  # X_m = j - X0, Y_m = i - Y0
WELT = os.path.join("export", "unreal", "welt")
U64 = np.uint64
ZONEN = ["sonst", "frisch", "alt", "rand", "uebergang"]  # Index 0..4
PFLANZEN_ROLLEN = ("bodendecker", "strauch", "grasbueschel", "baum_tot", "baum_kiefer_jung", "ast", "stumpf", "totholz",
                   "totholz_stehend")


def log(*a):
    print("[lava]", *a, flush=True)


# ----------------------------------------------------------------------------------------------------------------------
# Hash-Zufall (deterministisch aus Weltkoordinaten)
# ----------------------------------------------------------------------------------------------------------------------
def _mix(h):
    h = np.atleast_1d(h).astype(U64, copy=True)
    h ^= h >> U64(30)
    h *= U64(0xBF58476D1CE4E5B9)
    h ^= h >> U64(27)
    h *= U64(0x94D049BB133111EB)
    h ^= h >> U64(31)
    return h


def hash64(*teile):
    """teile: int-Arrays/Skalare (broadcastbar) → uint64-Hash."""
    h = None
    for t in teile:
        a = np.atleast_1d(np.asarray(t)).astype(np.int64).astype(U64)
        h = a * U64(0x9E3779B97F4A7C15) if h is None else _mix(h ^ (a + U64(0x9E3779B97F4A7C15)))
    return _mix(h)


def uni(h, salz):
    """Gleichverteilte in [0,1) aus Hash h und Salz (int)."""
    return (_mix(h ^ U64((salz * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)) >> U64(11)).astype(np.float64) \
        * (1.0 / 9007199254740992.0)


def zwischen(h, salz, lo, hi):
    return lo + (hi - lo) * uni(h, salz)


def ganz(h, salz, lo, hi):
    """Ganzzahl in [lo, hi] (inklusiv)."""
    return lo + np.minimum((uni(h, salz) * (hi - lo + 1)).astype(np.int64), hi - lo)


def wertrauschen(ii, jj, gitter_m, seed):
    """Bilinear interpoliertes Wert-Rauschen 0..1 auf einem Weltgitter (nahtlos zwischen Feldern)."""
    gi = np.floor(ii / gitter_m).astype(np.int64)
    gj = np.floor(jj / gitter_m).astype(np.int64)
    ti = (ii / gitter_m - gi).astype(np.float32)
    tj = (jj / gitter_m - gj).astype(np.float32)

    def w(di, dj):
        return uni(hash64(seed, 7, gi + di, gj + dj), 3).astype(np.float32)
    a = w(0, 0) * (1 - tj) + w(0, 1) * tj
    b = w(1, 0) * (1 - tj) + w(1, 1) * tj
    return a * (1 - ti) + b * ti


# ----------------------------------------------------------------------------------------------------------------------
# Raster-Operatoren (rein NumPy)
# ----------------------------------------------------------------------------------------------------------------------
def box_blur(a, r):
    """Separierbarer Box-Filter (Radius r Zellen) über Summenbild, Rand gespiegelt."""
    if r <= 0:
        return a.astype(np.float32)
    p = np.pad(a.astype(np.float32), r, mode="reflect")
    c = np.cumsum(p, axis=0)
    c = np.concatenate([np.zeros((1, c.shape[1]), np.float32), c], axis=0)
    p = (c[2 * r + 1:, :] - c[:-2 * r - 1, :]) / (2 * r + 1)
    c = np.cumsum(p, axis=1)
    c = np.concatenate([np.zeros((c.shape[0], 1), np.float32), c], axis=1)
    return (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)


def gauss_blur(a, sigma):
    """3 Box-Durchläufe ≈ Gauß (sigma in Zellen)."""
    r = max(1, int(round(sigma * 0.9)))
    for _ in range(3):
        a = box_blur(a, r)
    return a


def verschiebe(a, di, dj, fill):
    """Array um (di, dj) verschieben, freie Ränder mit fill."""
    out = np.full_like(a, fill)
    H, W = a.shape
    si0, si1 = max(0, di), min(H, H + di)
    sj0, sj1 = max(0, dj), min(W, W + dj)
    out[si0:si1, sj0:sj1] = a[si0 - di:si1 - di, sj0 - dj:sj1 - dj]
    return out


def dilate(mask, r):
    """Binäre Dilatation um r Zellen (oktagonal: abwechselnd Kreuz/Quadrat)."""
    m = mask.copy()
    for k in range(int(r)):
        n = m.copy()
        n |= verschiebe(m, 1, 0, False) | verschiebe(m, -1, 0, False) | verschiebe(m, 0, 1, False) | verschiebe(m, 0, -1, False)
        if k % 2 == 1:
            n |= verschiebe(m, 1, 1, False) | verschiebe(m, -1, -1, False) | verschiebe(m, 1, -1, False) | verschiebe(m, -1, 1, False)
        m = n
    return m


def distanz(mask, max_m, stufe=1):
    """Abstand (m) jeder Zelle zur Maske, gedeckelt auf max_m; stufe > 1 rechnet auf verkleinertem Raster (schneller)."""
    H, W = mask.shape
    if stufe > 1:
        Hs, Ws = (H + stufe - 1) // stufe, (W + stufe - 1) // stufe
        pad = np.zeros((Hs * stufe, Ws * stufe), bool)
        pad[:H, :W] = mask
        m = pad.reshape(Hs, stufe, Ws, stufe).any(axis=(1, 3))
    else:
        m = mask
    d = np.full(m.shape, np.float32(max_m), np.float32)
    d[m] = 0
    cur = m.copy()
    schritte = int(math.ceil(max_m / stufe))
    for k in range(1, schritte + 1):
        n = cur | verschiebe(cur, 1, 0, False) | verschiebe(cur, -1, 0, False) | verschiebe(cur, 0, 1, False) | verschiebe(cur, 0, -1, False)
        if k % 2 == 0:
            n |= verschiebe(cur, 1, 1, False) | verschiebe(cur, -1, -1, False) | verschiebe(cur, 1, -1, False) | verschiebe(cur, -1, 1, False)
        neu = n & ~cur
        if not neu.any():
            break
        d[neu] = min(k * stufe, max_m)
        cur = n
    if stufe > 1:
        d = np.repeat(np.repeat(d, stufe, axis=0), stufe, axis=1)[:H, :W]
    return d


def maxfilter(a, r):
    """Maximum im (2r+1)²-Fenster, separierbar mit Verdopplungsschritten."""
    out = a.copy()
    for axis in (0, 1):
        s = 1
        while s <= r:
            if axis == 0:
                out = np.maximum(out, np.maximum(verschiebe(out, s, 0, -1e9), verschiebe(out, -s, 0, -1e9)))
            else:
                out = np.maximum(out, np.maximum(verschiebe(out, 0, s, -1e9), verschiebe(out, 0, -s, -1e9)))
            s *= 2
    return out


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
    """Z-Achse um Anteil `kippen` auf die Geländenormale kippen, davor Zufalls-Yaw (rad). Ergebnis (n,4) = x,y,z,w."""
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


# ----------------------------------------------------------------------------------------------------------------------
# Dateien
# ----------------------------------------------------------------------------------------------------------------------
def feld_fenster(feld, rand):
    feld = feld.strip().upper()
    if len(feld) < 2 or not feld[0].isalpha() or not feld[1:].isdigit():
        raise SystemExit("Unbekanntes Feld %r (A1 … J7)" % feld)
    s = ord(feld[0]) - ord("A")
    r = int(feld[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise SystemExit("Unbekanntes Feld %r (A1 … J7)" % feld)
    j0, j1 = s * FELD, min((s + 1) * FELD, NX)  # J-Spalte: 9·1008 = 9072 … 9577 → geklippt
    i0, i1 = (r - 1) * FELD, min(r * FELD, NY)
    wi0, wi1 = max(0, i0 - rand), min(NY, i1 + rand)
    wj0, wj1 = max(0, j0 - rand), min(NX, j1 + rand)
    return feld, (i0, i1, j0, j1), (wi0, wi1, wj0, wj1)


def lade_raster(pfad, dtype, win, pflicht=False):
    """Fenster-Ausschnitt eines NY×NX-Rasters per memmap (nur das Fenster wird gelesen)."""
    wi0, wi1, wj0, wj1 = win
    if not os.path.isfile(pfad):
        if pflicht:
            raise SystemExit("Pflichtdatei fehlt: %s" % pfad)
        return None
    n = os.path.getsize(pfad) // np.dtype(dtype).itemsize
    if n != NX * NY:
        log("WARNUNG: %s hat %d Werte, erwartet %d – Datei wird ignoriert" % (pfad, n, NX * NY))
        if pflicht:
            raise SystemExit("Pflichtdatei %s hat falsche Größe" % pfad)
        return None
    mm = np.memmap(pfad, dtype=dtype, mode="r", shape=(NY, NX))
    return np.array(mm[wi0:wi1, wj0:wj1])


def lade_regeln(pfad):
    if not os.path.isfile(pfad):
        raise SystemExit("Regeldatei fehlt: %s" % pfad)
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


def lade_netze(basis):
    """daten/netze.csv → {pfad: {name, x, y, z, nanite, kollision}}; daten/netze_masse.json → min_z (cm)."""
    p = os.path.join(basis, "daten", "netze.csv")
    if not os.path.isfile(p):
        raise SystemExit("Inventar fehlt: %s (FORMAT.md §5: jeder Netzname muss im Inventar existieren)" % p)
    netze = {}
    with open(p, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            try:
                netze[row["pfad"]] = {"name": row["name"], "x": float(row["groesse_x_m"]), "y": float(row["groesse_y_m"]),
                                      "z": float(row["groesse_z_m"]), "nanite": row.get("nanite", "0") == "1",
                                      "kollision": int(row.get("kollision_primitive", "0") or 0) > 0}
            except (KeyError, ValueError):
                continue
    masse = {}
    pm = os.path.join(basis, "daten", "netze_masse.json")
    if os.path.isfile(pm):
        try:
            with open(pm, encoding="utf-8") as f:
                for k, v in json.load(f).items():
                    masse[k] = float(v["min"][2])
        except Exception as e:
            log("Hinweis: netze_masse.json unlesbar (%s) – Pivot aus Regeln" % e)
    else:
        log("Hinweis: daten/netze_masse.json fehlt – Pivot: 0 (unten) bzw. −H/2 für netz_pivot_mitte")
    return netze, masse


def pruefe_paletten(regeln, netze):
    """Entfernt Netze, die nicht im Inventar stehen; leere Klassen werden abgeschaltet."""
    fehlend, aus = [], []
    for kname, k in regeln["klassen"].items():
        ok_n, ok_w = [], []
        for pf, w in zip(k["netze"], k.get("netz_gewichte", [1] * len(k["netze"]))):
            if pf in netze:
                ok_n.append(pf)
                ok_w.append(w)
            else:
                fehlend.append((kname, pf))
        k["netze"], k["netz_gewichte"] = ok_n, ok_w
        if not ok_n:
            aus.append(kname)
    for kname, pf in fehlend:
        log("WARNUNG: Netz nicht im Inventar (%s): %s" % (kname, pf))
    for kname in aus:
        log("WARNUNG: Klasse %s hat keine gültigen Netze – wird übersprungen" % kname)
        regeln["klassen"].pop(kname)
    return fehlend


def lade_ebene_positionen(ordner, win):
    """Positionen (Fenster-i, Fenster-j) aller Instanzen einer Ebene; Bäume und Sonstige getrennt."""
    baum, sonst = [], []
    pj = os.path.join(ordner, "plan.json")
    if not os.path.isfile(pj):
        return baum, sonst
    try:
        with open(pj, encoding="utf-8") as f:
            plan = json.load(f)
    except Exception:
        return baum, sonst
    for name, info in plan.get("dateien", {}).items():
        fp = os.path.join(ordner, name + ".f32")
        if not os.path.isfile(fp):
            continue
        a = np.fromfile(fp, dtype="<f4")
        if a.size % 10:
            continue
        a = a.reshape(-1, 10)
        fj = a[:, 0] / 100.0 + X0 - win[2]
        fi = a[:, 1] / 100.0 + Y0 - win[0]
        m = (fi >= 0) & (fi < win[1] - win[0]) & (fj >= 0) & (fj < win[3] - win[2])
        if not m.any():
            continue
        txt = (str(info.get("rolle", "")) + " " + str(info.get("gruppe", "")) + " " + name).lower()
        ist_baum = any(r in txt for r in ("baum", "tree", "pine", "fir", "beech", "birch", "oak", "spruce")) \
            and "dead" not in txt and "stump" not in txt and "log" not in txt
        (baum if ist_baum else sonst).append(np.stack([fi[m], fj[m]], axis=1))
    return baum, sonst


def lade_belegt(basis, feld, win, A):
    """Belegt-Maske aus bestand/, witcher/, ufer/ (Feld + Nachbarn) und instanzen/instanzen.json."""
    H, W = win[1] - win[0], win[3] - win[2]
    s = ord(feld[0]) - ord("A")
    r = int(feld[1:])
    baum, sonst, quellen = [], [], []
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(ord("A") + ss) + str(rr)
            for ordner in (os.path.join(basis, WELT, "bestand", nf), os.path.join(basis, WELT, "witcher", nf),
                           os.path.join(basis, WELT, "ufer", "foliage_" + nf)):
                b, so = lade_ebene_positionen(ordner, win)
                if b or so:
                    quellen.append(os.path.relpath(ordner, os.path.join(basis, WELT)))
                baum += b
                sonst += so
    ij = os.path.join(basis, WELT, "instanzen", "instanzen.json")
    if os.path.isfile(ij):
        try:
            with open(ij, encoding="utf-8") as f:
                inst = json.load(f)
            for e in inst.get("verzeichnis", []):
                fp = e.get("datei") or (str(e.get("name", "")) + ".f32")
                fp = os.path.join(basis, WELT, "instanzen", fp)
                if not os.path.isfile(fp):
                    continue
                a = np.fromfile(fp, dtype="<f4")
                if a.size % 10:
                    continue
                a = a.reshape(-1, 10)
                fj = a[:, 0] / 100.0 + X0 - win[2]
                fi = a[:, 1] / 100.0 + Y0 - win[0]
                m = (fi >= 0) & (fi < H) & (fj >= 0) & (fj < W)
                if m.any():
                    txt = (str(e.get("klasse", "")) + " " + str(e.get("name", ""))).lower()
                    (baum if ("baum" in txt or "tree" in txt) else sonst).append(np.stack([fi[m], fj[m]], axis=1))
                    quellen.append("instanzen/" + os.path.basename(fp))
        except Exception as e:
            log("Hinweis: instanzen.json nicht auswertbar (%s)" % e)
    belegt = np.zeros((H, W), bool)
    n_b = n_s = 0
    if baum:
        b = np.concatenate(baum)
        n_b = len(b)
        mb = np.zeros((H, W), bool)
        mb[b[:, 0].astype(int), b[:, 1].astype(int)] = True
        belegt |= dilate(mb, int(round(A["bestand_baum_m"])))
    if sonst:
        so = np.concatenate(sonst)
        n_s = len(so)
        ms = np.zeros((H, W), bool)
        ms[so[:, 0].astype(int), so[:, 1].astype(int)] = True
        belegt |= dilate(ms, int(round(A["bestand_sonst_m"])))
    return belegt, n_b, n_s, quellen


def lade_lava_maske(basis, win, regeln, feld, lagen):
    """Lava-Maske je Zelle aus eigner.r8 + welt.json; Fallback Feld-Tabelle + Lage-Erkennung."""
    B = regeln["biom"]
    H, W = win[1] - win[0], win[3] - win[2]
    hinweise = []
    eig = lade_raster(os.path.join(basis, WELT, "eigner.r8"), np.uint8, win)
    wj = os.path.join(basis, WELT, "welt.json")
    tabelle = None
    if eig is not None and os.path.isfile(wj):
        try:
            with open(wj, encoding="utf-8") as f:
                welt = json.load(f)
            kacheln = welt.get("kacheln", {})
            tabelle = np.zeros(256, np.int8)  # 1 = lava, -1 = anderes Biom, 0 = Weltgelände/unbekannt
            eintraege = kacheln.items() if isinstance(kacheln, dict) else enumerate(kacheln)
            for k, v in eintraege:
                try:
                    kk = int(v.get("kennzahl", v.get("id", k))) if isinstance(v, dict) else int(k)
                except Exception:
                    continue
                if not (0 <= kk < 256) or kk == 0:
                    continue
                rz = str(v.get("rezept", "") if isinstance(v, dict) else "").lower()
                tabelle[kk] = 1 if ("lava" in rz or "vulkan" in rz) else -1
        except Exception as e:
            hinweise.append("welt.json unlesbar (%s) – Lava-Maske aus Feld-Fallback/Lagen" % e)
            tabelle = None
    else:
        hinweise.append("eigner.r8/welt.json fehlen – Lava-Maske aus Feld-Fallback/Lagen")
    lage_lava = None
    if "Lavafels" in lagen or "Lavasand" in lagen:
        lage_lava = np.zeros((H, W), np.float32)
        for n in ("Lavafels", "Lavasand"):
            if n in lagen:
                lage_lava += lagen[n].astype(np.float32)
        lage_lava = gauss_blur(lage_lava, B["maske_glaettung_m"]) >= B["lage_erkennung"]["schwelle"]
    fb_lava = B["feld_fallback"].get(feld, "aue") in B["lava_biome"]
    if tabelle is not None:
        kl = tabelle[eig]
        maske = kl == 1
        unbek = kl == 0
        if unbek.any():
            if lage_lava is not None and B.get("eigner0_ist_lava_wenn_lage", True):
                maske |= unbek & lage_lava
                hinweise.append("eigner=0 auf %.0f %% der Zellen → Lage-Erkennung Lavafels+Lavasand ≥ %d"
                                % (100 * unbek.mean(), B["lage_erkennung"]["schwelle"]))
            elif fb_lava:
                maske |= unbek
                hinweise.append("eigner=0 ohne Lagen → Feld-Fallback lava")
    elif lage_lava is not None:
        maske = lage_lava
        hinweise.append("Lava-Maske allein aus Lagen Lavafels+Lavasand")
    else:
        maske = np.full((H, W), fb_lava, bool)
        hinweise.append("keine Biomdaten, keine Lava-Lagen → ganzes Feld %s" % ("Lava" if fb_lava else "Nicht-Lava"))
    return maske, hinweise


# ----------------------------------------------------------------------------------------------------------------------
# Planung
# ----------------------------------------------------------------------------------------------------------------------
def _json_default(o):
    """NumPy-Skalare/Arrays JSON-fähig machen."""
    if isinstance(o, np.generic):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError("nicht serialisierbar: %r" % type(o))


def abstand_auswahl(pts, score, d_min, max_n):
    """Greedy: höchste Scores zuerst, Mindestabstand d_min (m); pts = (n,2) Fensterkoordinaten."""
    if len(pts) == 0:
        return np.zeros(0, np.int64)
    order = np.argsort(-score, kind="stable")[:4000]
    gew = []
    for idx in order:
        p = pts[idx]
        ok = True
        for g in gew:
            if (p[0] - pts[g][0]) ** 2 + (p[1] - pts[g][1]) ** 2 < d_min * d_min:
                ok = False
                break
        if ok:
            gew.append(idx)
            if len(gew) >= max_n:
                break
    return np.array(gew, np.int64)


def plane_feld(feld, basis, regeln, faktor, bild, netze, masse):
    t0 = time.time()
    seed = int(regeln["seed"])
    feld, fb, win = feld_fenster(feld, int(regeln["rand_m"]))
    i0, i1, j0, j1 = fb
    wi0, wi1, wj0, wj1 = win
    H, W = wi1 - wi0, wj1 - wj0
    A = regeln["ausschluss"]
    Z = regeln["zonen"]
    K = regeln["kegel"]
    hinweise = []
    log("Feld %s: Fenster i %d–%d, j %d–%d (%d × %d)" % (feld, wi0, wi1, wj0, wj1, H, W))

    # --- Höhe, Hang, Normale, Krümmung ---------------------------------------------------------------------------------
    h = lade_raster(os.path.join(basis, WELT, "hoehe.f32"), np.float32, win, pflicht=True).astype(np.float32)
    hs = gauss_blur(h, 1.5)
    gi, gj = np.gradient(hs)  # dh/di (Süd), dh/dj (Ost), m/m
    hang = np.degrees(np.arctan(np.sqrt(gi * gi + gj * gj))).astype(np.float32)
    nl = np.sqrt(gi * gi + gj * gj + 1.0)
    nx_, ny_, nz_ = (-gj / nl).astype(np.float32), (-gi / nl).astype(np.float32), (1.0 / nl).astype(np.float32)
    hangrichtung = np.arctan2(-gi, -gj).astype(np.float32)  # Yaw (rad) der Hangabwärtsrichtung, X = Ost, Y = Süd
    ii = (np.arange(wi0, wi1, dtype=np.int64)[:, None]).repeat(W, axis=1)
    jj = (np.arange(wj0, wj1, dtype=np.int64)[None, :]).repeat(H, axis=0)

    # --- Karten ----------------------------------------------------------------------------------------------------------
    def r8(name):
        return lade_raster(os.path.join(basis, WELT, name), np.uint8, win)
    wasser = r8("karte_wasser.r8")
    weg = r8("karte_weg.r8")
    ort = r8("karte_ort.r8")
    for n, a in (("karte_wasser.r8", wasser), ("karte_weg.r8", weg), ("karte_ort.r8", ort)):
        if a is None:
            hinweise.append("%s fehlt – ohne Abstandsregel" % n)
    wasser = wasser > 0 if wasser is not None else np.zeros((H, W), bool)
    weg = weg > 0 if weg is not None else np.zeros((H, W), bool)
    ort = ort > 0 if ort is not None else np.zeros((H, W), bool)
    lagen = {}
    for ln in regeln["lagen"]:
        a = r8("lage_%s.r8" % ln)
        if a is not None:
            lagen[ln] = a
    if not lagen:
        hinweise.append("keine lage_*.r8 gefunden – Lagenmix aus Zone geschätzt")
    else:
        log("Lagen gefunden: %s" % ", ".join(sorted(lagen)))

    # --- Lava-Maske, Zonen ------------------------------------------------------------------------------------------------
    lava, hw = lade_lava_maske(basis, win, regeln, feld, lagen)
    hinweise += hw
    d_rand_innen = distanz(~lava, Z["rand_innen_m"] + 2, stufe=2)     # Abstand zum Nicht-Lava (innerhalb der Lava)
    d_rand_aussen = distanz(lava, Z["uebergang_aussen_m"] + 2, stufe=2)  # Abstand zur Lava (außerhalb)
    d_wasser = distanz(wasser, 12.0) if wasser.any() else np.full((H, W), 12.0, np.float32)

    def lage01(name):
        return lagen[name].astype(np.float32) / 255.0 if name in lagen else None
    moos = lage01("Moos")
    gras = lage01("Gras")
    lavafels = lage01("Lavafels")
    g = Z["alter_gewichte"]
    alter = np.zeros((H, W), np.float32)
    if moos is not None:
        alter += g["moos"] * gauss_blur(moos, 3)
    if gras is not None:
        alter += g["gras"] * gauss_blur(gras, 3)
    alter += g["randnaehe"] * (1.0 - np.minimum(d_rand_innen / Z["rand_innen_m"], 1.0))
    alter += g["rauschen"] * (wertrauschen(ii, jj, Z["rauschen_gitter_m"], seed) - 0.5)
    if lavafels is not None:
        alter -= g["lavafels_abzug"] * gauss_blur(lavafels, 3) * (1.0 - (gauss_blur(moos, 3) if moos is not None else 0.0))
    if moos is None and gras is None:
        alter += 0.25 * (wertrauschen(ii, jj, 160, seed + 1) - 0.5)  # ohne Lagen etwas mehr Rauschen
    alter = np.clip(alter, 0, 1).astype(np.float32)
    zone = np.zeros((H, W), np.int8)  # 0 sonst
    zone[lava & (alter < Z["frisch_bis"])] = 1
    zone[lava & (alter >= Z["frisch_bis"]) & (alter < Z["alt_bis"])] = 2
    zone[lava & (alter >= Z["alt_bis"])] = 3
    zone[(~lava) & (d_rand_aussen <= Z["uebergang_aussen_m"])] = 4

    # --- Schlackenkegel --------------------------------------------------------------------------------------------------
    h80 = box_blur(h, int(K["glaettung_m"] // 2))
    prominenz = h - h80
    kegel_flanke = lava & (prominenz > 5) & (hang >= K["flanke_hang_grad"][0]) & (hang <= K["flanke_hang_grad"][1])
    hmax = maxfilter(h, int(K["gipfel_fenster_m"] // 2))
    gipfel = lava & (h >= hmax - 0.01) & (prominenz >= K["prominenz_min_m"])

    # --- Belegt / zulässig ----------------------------------------------------------------------------------------------
    belegt, n_b, n_s, quellen = lade_belegt(basis, feld, win, A)
    if quellen:
        log("vorhandene Ebenen berücksichtigt: %s (%d Bäume, %d Sonstige)" % (", ".join(sorted(set(quellen))), n_b, n_s))
    else:
        hinweise.append("keine vorhandenen Ebenen (bestand/witcher/ufer/instanzen) gefunden – keine Belegt-Abstände")
    sperre_klein = wasser | dilate(weg, int(round(A["weg_klein_m"]))) | dilate(ort, int(round(A["ort_m"]))) | belegt
    sperre_gross = wasser | dilate(weg, int(round(A["weg_gross_m"]))) | dilate(ort, int(round(A["ort_m"]))) | belegt
    wasser_nah = dilate(wasser, int(round(A["wasser_m"]))) if wasser.any() else wasser
    hoehe_f = np.clip(1.0 - (h - A["hoehe_pflanzen_abnahme_ab_m"]) / max(1.0, A["hoehe_pflanzen_null_ab_m"] - A["hoehe_pflanzen_abnahme_ab_m"]), 0, 1).astype(np.float32)

    # --- Lagenmix je Zelle (für Dichte) -------------------------------------------------------------------------------------
    lage_norm = {}
    if lagen:
        summe = np.zeros((H, W), np.float32)
        for ln, a in lagen.items():
            lage_norm[ln] = a.astype(np.float32) / 255.0
            summe += lage_norm[ln]
        rest = np.clip(1.0 - summe, 0, 1)
        ueber = summe > 1.0
        if ueber.any():  # Gewichte > 255 in Summe → normieren
            for ln in lage_norm:
                lage_norm[ln] = np.where(ueber, lage_norm[ln] / summe, lage_norm[ln])
        lage_norm["sonst"] = rest
    else:
        # Schätzung: Zone bestimmt Lagenmix
        lage_norm = {"Lavafels": np.select([zone == 1, zone == 2, zone == 3], [0.6, 0.5, 0.3], 0.0).astype(np.float32),
                     "Lavasand": np.select([zone == 1, zone == 2, zone == 3], [0.4, 0.25, 0.1], 0.0).astype(np.float32),
                     "Moos": np.select([zone == 2, zone == 3], [0.25, 0.35], 0.0).astype(np.float32),
                     "Gras": np.select([zone == 3], [0.25], 0.0).astype(np.float32),
                     "sonst": (zone == 4).astype(np.float32)}

    def dichte_karte(k):
        D = np.zeros((H, W), np.float32)
        dj = k["dichte_je_m2"]
        for ln, w in lage_norm.items():
            D += w * float(dj.get(ln, dj.get("sonst", 0.0)))
        zf = k["zone_faktor"]
        D *= np.select([zone == 1, zone == 2, zone == 3, zone == 4], [zf["frisch"], zf["alt"], zf["rand"], zf["uebergang"]], 0.0).astype(np.float32)
        return D

    # --- Punkte: Fumarolen, Dampf, Gipfel, Vorschläge ---------------------------------------------------------------------
    P = regeln["punkte"]
    punkte = []
    frei_fumarole = np.zeros((H, W), bool)
    innen = np.zeros((H, W), bool)
    innen[i0 - wi0:i1 - wi0, j0 - wj0:j1 - wj0] = True
    zone_name = {1: "frisch", 2: "alt", 3: "rand", 4: "uebergang"}

    def boden_z(fi, fj):
        return bilinear(h, fi, fj)

    # Fumarolen
    F = P["fumarole"]
    pf = np.zeros((H, W), np.float32)
    for zi, zn in zone_name.items():
        pf[zone == zi] = F["je_km2"].get(zn, 0.0) / 1e6
    pf *= np.where(kegel_flanke | (prominenz > 8), F["kegelflanke_faktor"], 1.0)
    pf[(hang > F["hang_max_grad"]) | sperre_gross | ~innen] = 0
    hf = hash64(seed, 101, ii, jj)
    kand = np.nonzero(uni(hf, 1) < pf * 12.0)  # 12× überzeichnen, dann Abstand/Deckel
    if len(kand[0]):
        pts = np.stack([kand[0], kand[1]], axis=1).astype(np.float32)
        score = uni(hf[kand], 2) + np.where(kegel_flanke[kand], 0.5, 0.0)
        ziel = int(round(min(F["max_je_feld"], pf[innen].sum())))
        sel = abstand_auswahl(pts, score, F["min_abstand_m"], max(0, ziel))
        for s_ in sel:
            fi, fj = pts[s_]
            hh = hash64(seed, 102, int(fi) + wi0, int(fj) + wj0)
            st = float(zwischen(hh, 1, *F["staerke"])[0])
            rad = float(zwischen(hh, 2, *F["radius_m"])[0])
            schwefel = bool(uni(hh, 3)[0] < F["schwefel_anteil"])
            punkte.append({"typ": "fumarole", "x_cm": round((fj + wj0 - X0) * 100, 1), "y_cm": round((fi + wi0 - Y0) * 100, 1),
                           "z_cm": round(float(boden_z(np.array([fi]), np.array([fj]))[0] + F["hoehe_ueber_boden_m"]) * 100, 1),
                           "staerke": round(st, 2), "radius_m": round(rad, 1), "schwefel": schwefel,
                           "zone": zone_name.get(int(zone[int(fi), int(fj)]), "sonst"), "kegelflanke": bool(kegel_flanke[int(fi), int(fj)])})
            r_ = int(math.ceil(rad))
            a0, a1 = max(0, int(fi) - r_), min(H, int(fi) + r_ + 1)
            b0, b1 = max(0, int(fj) - r_), min(W, int(fj) + r_ + 1)
            frei_fumarole[a0:a1, b0:b1] = True
    # Dampf an Wasserkanten
    Dp = P["dampf"]
    if wasser.any():
        zmask = np.zeros((H, W), bool)
        for zn in Dp["zonen"]:
            zmask |= zone == {v: k for k, v in zone_name.items()}[zn]
        band = lava & zmask & ~wasser & (d_wasser >= Dp["wasserband_m"][0]) & (d_wasser <= Dp["wasserband_m"][1]) & innen
        kand = np.nonzero(band & (uni(hash64(seed, 103, ii, jj), 1) < 0.02))
        if len(kand[0]):
            pts = np.stack([kand[0], kand[1]], axis=1).astype(np.float32)
            sel = abstand_auswahl(pts, uni(hash64(seed, 103, ii[kand], jj[kand]), 2), Dp["min_abstand_m"], Dp["max_je_feld"])
            for s_ in sel:
                fi, fj = pts[s_]
                hh = hash64(seed, 104, int(fi) + wi0, int(fj) + wj0)
                punkte.append({"typ": "dampf", "x_cm": round((fj + wj0 - X0) * 100, 1), "y_cm": round((fi + wi0 - Y0) * 100, 1),
                               "z_cm": round(float(boden_z(np.array([fi]), np.array([fj]))[0]) * 100, 1),
                               "staerke": round(float(zwischen(hh, 1, *Dp["staerke"])[0]), 2)})
    # Kegelgipfel
    kand = np.nonzero(gipfel & innen)
    if len(kand[0]):
        pts = np.stack([kand[0], kand[1]], axis=1).astype(np.float32)
        sel = abstand_auswahl(pts, prominenz[kand], K["gipfel_fenster_m"], P["kegel_gipfel"]["max_je_feld"])
        for s_ in sel:
            fi, fj = pts[s_]
            punkte.append({"typ": "kegel_gipfel", "x_cm": round((fj + wj0 - X0) * 100, 1), "y_cm": round((fi + wi0 - Y0) * 100, 1),
                           "z_cm": round(float(h[int(fi), int(fj)]) * 100, 1), "prominenz_m": round(float(prominenz[int(fi), int(fj)]), 1)})
    # Spire-Vorschläge (flache Kuppen im Kern)
    Sp = P["spire_vorschlag"]
    zm = np.zeros((H, W), bool)
    for zn in Sp["zonen"]:
        zm |= zone == {v: k for k, v in zone_name.items()}[zn]
    kand = np.nonzero(zm & innen & (hang <= Sp["hang_max_grad"]) & (prominenz >= Sp["kuppen_prominenz_m"]) & ~sperre_gross
                      & (uni(hash64(seed, 105, ii, jj), 1) < 0.01))
    if len(kand[0]):
        pts = np.stack([kand[0], kand[1]], axis=1).astype(np.float32)
        sel = abstand_auswahl(pts, prominenz[kand] + uni(hash64(seed, 105, ii[kand], jj[kand]), 2), Sp["min_abstand_m"], Sp["max_je_feld"])
        for n_, s_ in enumerate(sel):
            fi, fj = pts[s_]
            punkte.append({"typ": "spire_vorschlag", "x_cm": round((fj + wj0 - X0) * 100, 1), "y_cm": round((fi + wi0 - Y0) * 100, 1),
                           "z_cm": round(float(h[int(fi), int(fj)]) * 100, 1), "netz": Sp["netze"][n_ % len(Sp["netze"])],
                           "yaw_grad": round(float(uni(hash64(seed, 106, int(fi) + wi0, int(fj) + wj0), 1)[0] * 360), 1)})
    # Höhlen-Vorschläge (steile Lava-Wände)
    Hv = P["hoehle_vorschlag"]
    zm = np.zeros((H, W), bool)
    for zn in Hv["zonen"]:
        zm |= zone == {v: k for k, v in zone_name.items()}[zn]
    kand = np.nonzero(zm & innen & (hang >= Hv["hang_grad"][0]) & (hang <= Hv["hang_grad"][1]) & (d_rand_innen >= Hv["rand_abstand_min_m"])
                      & (uni(hash64(seed, 107, ii, jj), 1) < 0.02))
    if len(kand[0]):
        pts = np.stack([kand[0], kand[1]], axis=1).astype(np.float32)
        sel = abstand_auswahl(pts, uni(hash64(seed, 107, ii[kand], jj[kand]), 2), Hv["min_abstand_m"], Hv["max_je_feld"])
        for s_ in sel:
            fi, fj = pts[s_]
            punkte.append({"typ": "hoehle_vorschlag", "x_cm": round((fj + wj0 - X0) * 100, 1), "y_cm": round((fi + wi0 - Y0) * 100, 1),
                           "z_cm": round(float(h[int(fi), int(fj)]) * 100, 1), "hang_grad": round(float(hang[int(fi), int(fj)]), 1),
                           "hinweis": "kein Höhlen-Netz im Inventar"})
    # Schwefelgrube: stärkste Fumarole nahe Weg; Opferstätte: am Kegelfuß/Spire
    fum = [p for p in punkte if p["typ"] == "fumarole"]
    if fum and weg.any():
        d_weg = distanz(weg, P["schwefelgrube_vorschlag"]["weg_max_m"] + 2, stufe=2)
        best = None
        for p in fum:
            fi, fj = int(round(p["y_cm"] / 100 + Y0 - wi0)), int(round(p["x_cm"] / 100 + X0 - wj0))
            if 0 <= fi < H and 0 <= fj < W and d_weg[fi, fj] <= P["schwefelgrube_vorschlag"]["weg_max_m"]:
                if best is None or p["staerke"] > best["staerke"]:
                    best = p
        if best is not None:
            punkte.append({"typ": "schwefelgrube_vorschlag", "x_cm": best["x_cm"], "y_cm": best["y_cm"], "z_cm": best["z_cm"],
                           "hinweis": "verlassene Schwefelgrube an stärkster Fumarole mit Weg ≤ %d m" % P["schwefelgrube_vorschlag"]["weg_max_m"]})
    anker = [p for p in punkte if p["typ"] in ("spire_vorschlag", "kegel_gipfel")]
    if anker:
        a = anker[0]
        fi, fj = int(round(a["y_cm"] / 100 + Y0 - wi0)), int(round(a["x_cm"] / 100 + X0 - wj0))
        # 25 m hangabwärts vom Anker (Kegelfuß)
        yaw = float(hangrichtung[min(max(fi, 0), H - 1), min(max(fj, 0), W - 1)])
        fi2, fj2 = fi + 25 * math.sin(yaw), fj + 25 * math.cos(yaw)
        fi2, fj2 = min(max(fi2, 0), H - 1.01), min(max(fj2, 0), W - 1.01)
        punkte.append({"typ": "opferstaette_vorschlag", "x_cm": round((fj2 + wj0 - X0) * 100, 1), "y_cm": round((fi2 + wi0 - Y0) * 100, 1),
                       "z_cm": round(float(boden_z(np.array([fi2]), np.array([fj2]))[0]) * 100, 1), "anker": a["typ"]})

    # --- Klassen platzieren -------------------------------------------------------------------------------------------------
    klassen = regeln["klassen"]
    ergebnis = {}  # klasse -> dict(arrays)
    stein_naehe = np.zeros((H, W), bool)
    k_id = 0
    for kname, k in klassen.items():
        k_id += 1
        D = dichte_karte(k) * float(faktor)
        rolle = k["rolle"]
        pflanze = rolle in PFLANZEN_ROLLEN
        # Hang
        hg = k["hang_grad"]
        hang_ok = (hang >= hg[0]) & (hang <= hg[1])
        # Globale Obergrenze (FORMAT §3: Hang > 40° nur Felsen): Pflanzen/Totholz ≤ hang_pflanzen_max_grad, Steine ≤ hang_steine_max_grad
        hang_ok &= hang <= float(A["hang_pflanzen_max_grad"] if (pflanze or kname == "moos") else A["hang_steine_max_grad"])
        if "hang_bonus" in k:
            hb = k["hang_bonus"]
            D *= np.where((hang >= hb["ab_grad"]) & (hang <= hb["bis_grad"]), hb["faktor"], 1.0)
        if pflanze:
            D *= hoehe_f
            D *= np.where(kegel_flanke, K["flanke_faktor_pflanzen"], 1.0)
            D[frei_fumarole] = 0
        elif kname == "schlacke":
            D *= np.where(kegel_flanke, K["flanke_faktor_schlacke"], 1.0)
        if "an_stein_bonus" in k and stein_naehe.any():
            D *= np.where(stein_naehe, k["an_stein_bonus"], 1.0)
        # Wasserband (Wasserkante) oder normaler Wasserabstand
        if "wasserband_m" in k:
            wb = k["wasserband_m"]
            if not wasser.any():
                continue
            D *= ((d_wasser >= wb[0]) & (d_wasser <= wb[1]) & ~wasser).astype(np.float32)
            sperre = (dilate(weg, int(round(A["weg_gross_m"]))) | dilate(ort, int(round(A["ort_m"]))) | belegt | wasser)
        else:
            D[wasser_nah] = 0
            sperre = sperre_gross if (k.get("kollision") or rolle in ("baum_tot", "baum_kiefer_jung", "block", "akteur")) else sperre_klein
        D[sperre | ~hang_ok] = 0
        if not (D > 0).any():
            continue
        # Gruppenzentren
        gn = k["gruppe_n"]
        p_zentrum = D / (0.5 * (gn[0] + gn[1]))
        hz = hash64(seed, k_id, ii, jj)
        zm = uni(hz, 1) < p_zentrum
        ci, cj = np.nonzero(zm)
        if len(ci) == 0:
            continue
        hc = hz[ci, cj]
        n_mitgl = ganz(hc, 2, gn[0], gn[1])
        nmax = int(gn[1])
        rad = float(k["gruppe_radius_m"])
        # Mitglieder (k = 0 ist das Zentrum selbst)
        kk = np.arange(nmax)[None, :]
        gueltig = kk < n_mitgl[:, None]
        hm = _mix(hc[:, None] ^ (U64(0x9E3779B97F4A7C15) * (kk.astype(U64) + U64(1))))
        rr = rad * np.sqrt(uni(hm, 10)) * (kk > 0)
        ang = 2 * math.pi * uni(hm, 11)
        fi = ci[:, None] + rr * np.sin(ang)
        fj = cj[:, None] + rr * np.cos(ang)
        gueltig &= (fi >= 0) & (fi < H - 1) & (fj >= 0) & (fj < W - 1)
        fi = np.where(gueltig, fi, 0)
        fj = np.where(gueltig, fj, 0)
        zi = fi.astype(np.int32)
        zj = fj.astype(np.int32)
        gueltig &= (D[zi, zj] > 0)
        if "wasserband_m" not in k:
            gueltig &= ~wasser_nah[zi, zj]
        sel = np.nonzero(gueltig)
        if len(sel[0]) == 0:
            continue
        fi, fj, hm = fi[sel], fj[sel], hm[sel]
        zi, zj = zi[sel], zj[sel]
        # nur Instanzen im Feld (nicht im Rand) behalten
        im_feld = (fi + wi0 >= i0) & (fi + wi0 < i1) & (fj + wj0 >= j0) & (fj + wj0 < j1)
        fi, fj, hm, zi, zj = fi[im_feld], fj[im_feld], hm[im_feld], zi[im_feld], zj[im_feld]
        n = len(fi)
        if n == 0:
            continue
        # Netzwahl (gewichtet)
        gew = np.cumsum(np.asarray(k["netz_gewichte"], np.float64))
        gew /= gew[-1]
        netz_idx = np.searchsorted(gew, uni(hm, 12), side="right").clip(0, len(k["netze"]) - 1)
        # Maßstab
        ms = k["massstab"]
        s = zwischen(hm, 13, ms[0], ms[1]).astype(np.float32)
        nu = float(k.get("nicht_uniform", 0.0))
        sx = s * (1 + nu * (uni(hm, 14) - 0.5) * 2).astype(np.float32)
        sy = s * (1 + nu * (uni(hm, 15) - 0.5) * 2).astype(np.float32)
        sz = s
        # Yaw
        if k.get("yaw") == "hang":
            yaw = hangrichtung[zi, zj] + np.radians(zwischen(hm, 16, -35, 35)).astype(np.float32)
            if rolle == "akteur":
                yaw = yaw + np.float32(math.pi / 2)  # Säulenreihen quer zum Hang (= Uferrichtung)
            # Netze mit langer Y-Achse um 90° drehen, damit die Längsachse hangab liegt
            lang_y = np.array([netze[p]["y"] > netze[p]["x"] for p in k["netze"]], bool)[netz_idx]
            yaw = yaw + np.where(lang_y, np.float32(math.pi / 2), 0).astype(np.float32)
        else:
            yaw = (2 * math.pi * uni(hm, 16)).astype(np.float32)
        q = quaternionen(nx_[zi, zj], ny_[zi, zj], nz_[zi, zj], float(k["kippen"]), yaw)
        # Höhe / Eingraben
        boden = bilinear(h, fi, fj)
        Hn = np.array([netze[p]["z"] for p in k["netze"]], np.float32)[netz_idx]
        if "eingraben" in k:
            e = zwischen(hm, 17, k["eingraben"][0], k["eingraben"][1]).astype(np.float32)
            minz = []
            for p in k["netze"]:
                name = netze[p]["name"]
                if p in masse:
                    minz.append(masse[p] / 100.0)
                elif name in regeln["pivot"]["netz_pivot_mitte"]:
                    minz.append(-netze[p]["z"] / 2.0)
                else:
                    minz.append(0.0)
            minz = np.array(minz, np.float32)[netz_idx]
            z = boden - minz * sz - e * Hn * sz
        else:
            z = boden - float(k.get("eingraben_cm", 3)) / 100.0
        x_cm = ((fj + wj0 - X0) * 100).astype(np.float32)
        y_cm = ((fi + wi0 - Y0) * 100).astype(np.float32)
        ergebnis[kname] = {"x": x_cm, "y": y_cm, "z": (z * 100).astype(np.float32), "q": q, "s": np.stack([sx, sy, sz], axis=1),
                           "netz": netz_idx, "h": hm, "fi": fi, "fj": fj}
        if kname == "schlacke":
            m = np.zeros((H, W), bool)
            m[zi, zj] = True
            stein_naehe = dilate(m, 2)
        log("  %-16s %6d Instanzen" % (kname, n))

    # --- Budget ------------------------------------------------------------------------------------------------------------
    Bg = regeln["budget"]
    prio = Bg["prioritaet_behalten"]

    def ausduennen(kname, behalten):
        r_ = ergebnis[kname]
        n = len(r_["x"])
        if behalten >= n:
            return
        keep = uni(r_["h"], 99) < (behalten / float(n))
        for key in list(r_.keys()):
            r_[key] = r_[key][keep]
        hinweise.append("%s auf %d ausgedünnt (Budget)" % (kname, int(keep.sum())))
    for kname in list(ergebnis):
        ausduennen(kname, int(klassen[kname].get("max", 10 ** 9)))
    # Akteure
    for kname in list(ergebnis):
        if klassen[kname]["rolle"] == "akteur":
            ausduennen(kname, int(Bg["akteure"]))
    # Kollision
    koll = [kn for kn in ergebnis if klassen[kn].get("kollision")]
    nk = sum(len(ergebnis[kn]["x"]) for kn in koll)
    for kn in sorted(koll, key=lambda x: -prio.index(x) if x in prio else 0):
        if nk <= Bg["kollision"]:
            break
        cur = len(ergebnis[kn]["x"])
        ziel = max(0, cur - (nk - Bg["kollision"]))
        ausduennen(kn, ziel)
        nk -= cur - len(ergebnis[kn]["x"])
    # Gesamt
    gesamt = sum(len(r_["x"]) for r_ in ergebnis.values())
    for kn in sorted(ergebnis, key=lambda x: -prio.index(x) if x in prio else 0):
        if gesamt <= Bg["ziel"]:
            break
        cur = len(ergebnis[kn]["x"])
        ziel = max(0, cur - (gesamt - Bg["ziel"]))
        ausduennen(kn, ziel)
        gesamt -= cur - len(ergebnis[kn]["x"])
    gesamt = sum(len(r_["x"]) for r_ in ergebnis.values())

    # --- Schreiben -----------------------------------------------------------------------------------------------------------
    out = os.path.join(basis, regeln["ausgabe"]["ordner"], feld)
    os.makedirs(out, exist_ok=True)
    for f_ in os.listdir(out):
        if f_.endswith(".f32"):
            os.remove(os.path.join(out, f_))
    dateien = {}
    n_koll = 0
    for kname, r_ in ergebnis.items():
        k = klassen[kname]
        for ni, pfad in enumerate(k["netze"]):
            m = r_["netz"] == ni
            if not m.any():
                continue
            name = netze[pfad]["name"]
            if k["rolle"] == "akteur":
                dname = "akteur_" + name
            else:
                dname = name
            arr = np.concatenate([r_["x"][m, None], r_["y"][m, None], r_["z"][m, None], r_["q"][m], r_["s"][m]], axis=1).astype("<f4")
            with open(os.path.join(out, dname + ".f32"), "ab" if dname in dateien else "wb") as f:
                arr.tofile(f)
            if dname in dateien:
                dateien[dname]["anzahl"] += int(m.sum())
                continue
            kollision = bool(k.get("kollision", False))
            if k["rolle"] in ("block", "akteur", "totholz") and netze[pfad]["z"] * k["massstab"][1] > 0.8:
                kollision = True
            if kollision:
                n_koll += int(m.sum())
            e = {"pfad": pfad, "anzahl": int(m.sum()), "gruppe": k["gruppe"], "rolle": k["rolle"], "schicht": k["schicht"],
                 "sichtweite": list(k["sichtweite"]), "schatten": bool(k.get("schatten", True)), "kollision": kollision}
            hin = []
            if kollision and not netze[pfad]["kollision"]:
                hin.append("Netz ohne Kollisionsprimitive – Setzer: Komplex-als-Einfach oder Konvex-Hülle erzeugen")
            if not netze[pfad]["nanite"]:
                hin.append("kein Nanite – LOD/Sichtweite prüfen")
            if "material" in k.get("hinweis", "").lower() or kname.startswith("verkohlt") or kname in ("kiesel", "schwarzkies", "asche"):
                hin.append("dunkle/verkohlte Material-Instanz (siehe Regel-Hinweis)")
            if hin:
                e["hinweis"] = "; ".join(hin)
            dateien[dname] = e
    zonen_anteil = {}
    zi_feld = zone[i0 - wi0:i1 - wi0, j0 - wj0:j1 - wj0]
    for zi, zn in zone_name.items():
        zonen_anteil[zn] = round(float((zi_feld == zi).mean()), 4)
    zonen_anteil["sonst"] = round(float((zi_feld == 0).mean()), 4)
    fo = dict(regeln.get("felsgruppen_overrides", {}))
    fo["hero_akteur_punkte"] = [p for p in punkte if p["typ"] == "spire_vorschlag"]
    so = dict(regeln.get("spuren_overrides", {}))
    so["rauch_punkte"] = len([p for p in punkte if p["typ"] == "fumarole"])
    plan = {"stand": time.strftime("%Y-%m-%d %H:%M"), "feld": feld, "ebene": regeln["ausgabe"]["ebene"], "instanzen": int(gesamt),
            "instanzen_kollision": int(n_koll), "dateien": dateien,
            "entfernen": regeln["ausgabe"]["entfernen"], "ft_ordner": regeln["ausgabe"]["ft_ordner"], "ft_praefix": regeln["ausgabe"]["ft_praefix"],
            "punkte": punkte, "zonen": zonen_anteil, "lava_anteil": round(float(lava[i0 - wi0:i1 - wi0, j0 - wj0:j1 - wj0].mean()), 4),
            "felsgruppen_overrides": fo, "spuren_overrides": so, "faktor": faktor, "seed": seed,
            "quelle": "lava_plan.py (UNGETESTET MIT ECHTDATEN)", "hinweise": hinweise}
    with open(os.path.join(out, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1, default=_json_default)
    log("Feld %s: %d Instanzen (%d mit Kollision), %d Netzdateien, %d Punkte, Zonen %s, %.1f s"
        % (feld, gesamt, n_koll, len(dateien), len(punkte), zonen_anteil, time.time() - t0))

    if bild:
        schreibe_bild(basis, regeln, feld, fb, win, zone, wasser, weg, ort, ergebnis, punkte)
    return plan


def schreibe_bild(basis, regeln, feld, fb, win, zone, wasser, weg, ort, ergebnis, punkte):
    i0, i1, j0, j1 = fb
    wi0, wi1, wj0, wj1 = win
    Hf, Wf = i1 - i0, j1 - j0
    oi, oj = i0 - wi0, j0 - wj0
    Bz = regeln["bild"]
    img = np.zeros((Hf, Wf, 3), np.uint8)
    z = zone[oi:oi + Hf, oj:oj + Wf]
    for idx, zn in ((0, "sonst"), (1, "frisch"), (2, "alt"), (3, "rand"), (4, "uebergang")):
        img[z == idx] = Bz["hintergrund"][zn]
    img[wasser[oi:oi + Hf, oj:oj + Wf]] = Bz["hintergrund"]["wasser"]
    img[weg[oi:oi + Hf, oj:oj + Wf]] = Bz["hintergrund"]["weg"]
    img[ort[oi:oi + Hf, oj:oj + Wf]] = Bz["hintergrund"]["ort"]
    for kname, r_ in ergebnis.items():
        farbe = regeln["klassen"][kname]["farbe"]
        pi = (r_["fi"] - oi).astype(int)
        pj = (r_["fj"] - oj).astype(int)
        m = (pi >= 0) & (pi < Hf) & (pj >= 0) & (pj < Wf)
        img[pi[m], pj[m]] = farbe
    for p in punkte:
        farbe = Bz["punkte"].get(p["typ"], [255, 255, 255])
        pi = int(round(p["y_cm"] / 100 + Y0 - i0))
        pj = int(round(p["x_cm"] / 100 + X0 - j0))
        r = 4 if p["typ"] in ("fumarole", "kegel_gipfel", "spire_vorschlag") else 3
        for d in range(-r, r + 1):
            for (a, b) in ((pi + d, pj), (pi, pj + d)):
                if 0 <= a < Hf and 0 <= b < Wf:
                    img[a, b] = farbe
    od = os.path.join(basis, regeln["ausgabe"]["bild"])
    os.makedirs(od, exist_ok=True)
    pfad = os.path.join(od, feld + ".png")
    try:
        from PIL import Image
        Image.fromarray(img, "RGB").save(pfad)
    except Exception as e:
        pfad = os.path.join(od, feld + ".ppm")
        with open(pfad, "wb") as f:
            f.write(("P6\n%d %d\n255\n" % (Wf, Hf)).encode("ascii"))
            f.write(img.tobytes())
        log("Hinweis: Pillow fehlt (%s) – PPM geschrieben" % e)
    log("Bild: %s" % pfad)


# ----------------------------------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Eldarien – Planer Biom Lava (Schichten 0/1/2/5 + Punkte, Overrides für 3/4)")
    ap.add_argument("felder", nargs="+", help="Gitterfelder, z. B. C6 C7 C5")
    ap.add_argument("--bild", action="store_true", help="Draufsicht PNG nach docs/pruefung/lava/")
    ap.add_argument("--faktor", type=float, default=1.0, help="Dichtefaktor (Default 1.0)")
    ap.add_argument("--basis", default=".", help="production-Wurzel (Default .)")
    ap.add_argument("--regeln", default=None, help="Regeldatei (Default lava_regeln.json neben dem Skript)")
    a = ap.parse_args(argv)
    hier = os.path.dirname(os.path.abspath(__file__))
    rp = a.regeln or os.path.join(hier, "lava_regeln.json")
    if not os.path.isfile(rp):
        alt = os.path.join(a.basis, "scripts", "lava", "lava_regeln.json")
        rp = alt if os.path.isfile(alt) else rp
    regeln = lade_regeln(rp)
    log("Regeln: %s | NumPy %s | numba %s" % (rp, np.__version__, "ja" if HAVE_NUMBA else "nein (nicht nötig)"))
    netze, masse = lade_netze(a.basis)
    log("Inventar: %d Netze, %d mit Bounds" % (len(netze), len(masse)))
    pruefe_paletten(regeln, netze)
    hp = os.path.join(a.basis, WELT, "hoehe.f32")
    if not os.path.isfile(hp):
        raise SystemExit("Pflichtdatei fehlt: %s" % hp)
    for feld in a.felder:
        try:
            plane_feld(feld, a.basis, regeln, a.faktor, a.bild, netze, masse)
        except SystemExit:
            raise
        except Exception as e:  # ein Feld darf die anderen nicht abbrechen
            log("FEHLER in Feld %s: %s: %s" % (feld, type(e).__name__, e))
            import traceback
            traceback.print_exc()
    return 0


if __name__ == "__main__":
    sys.exit(main())
