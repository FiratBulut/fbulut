#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
felsgruppen_plan.py – Planer „Fels organisch“ (Auftrag 11, Teil C) für Eldarien (UE 5.8.3, 1-m-Raster 9577 × 7057).

*** UNGETESTET MIT ECHTDATEN *** – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern rauchgetestet (B4-Fenster).
Korrekturen bitte als auftraege/verteilung-felsgruppen-korrektur.md.

Was das Skript tut
------------------
Liest je Gitterfeld ein Fenster (Feld + 64 m Rand) aus hoehe.f32 (np.memmap, kein Volllesen), berechnet Hang, Normale,
Krümmung (Hessian einer Gauß-geglätteten Höhe, separierbare Faltung, keine Python-Schleifen über Zellen) und leitet daraus
geologische Lagen ab:
  grat       Grate/Kämme (negative Hauptkrümmung) → Hauptfels + 2–5 Nebenblöcke + Steine + Kiesel, Hauptrichtung = Gratachse
  band       Felsbänder in gleicher Höhenlage mit per-Berg-konstanter Schichtneigung (Strike/Dip aus 512-m-Wertrauschen)
  wand       Felsnasen an Wänden > 50° (plan-konvex) → Schalen/Klippen als Akteure
  fuss       Schuttfächer unter Wänden > 50° (Fächer ≤ 64 m, Größe nimmt hangabwärts ab, 4 Stufen)
  blockstrom Blockströme am Hangfuß (konkav, Wand ≥ 25 m darüber in ≤ 128 m)
  kuppe      Einzelblöcke auf Kuppen (lokale Maxima, 32 m Umkreis)
  prallhang  Felsnasen an Flussprallhängen (Krümmung der Flusspolylinie aus wasser_welt.json)
Nichts in Mulden ohne Wand darüber, nichts auf Wasser/Weg/Ort, Abstand zu Bäumen (bestand/) und Felsschalen (felsschalen/).
Zufall ist deterministisch: 64-bit-Hash aus (Seed, Klasse, Weltraster-Koordinate) → Gleichverteilte je Instanz; Nachbarfelder
erzeugen dieselben Gruppen im Überlappungsrand (kein Nahtsprung).

Aufruf
------
  python -I scripts/felsgruppen/felsgruppen_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
  --basis   production-Wurzel (Default "."), darunter export/unreal/welt/, daten/netze.csv, daten/netze_masse.json, docs/
  --regeln  Regeldatei (Default: felsgruppen_regeln.json neben dem Skript, sonst scripts/felsgruppen/felsgruppen_regeln.json)
  --faktor  Dichtefaktor (multipliziert alle Annahme-Wahrscheinlichkeiten und die Kiesel-Dichte)
  --bild    Draufsicht docs/pruefung/felsgruppen/<Feld>.png (1 px = 1 m, Farben je Klasse)

Ausgabe (FORMAT.md §3)
----------------------
  export/unreal/welt/felsgruppen/<Feld>/<Netzname>.f32   10 float32 LE je Instanz: x,y,z cm; qx,qy,qz,qw; sx,sy,sz
  export/unreal/welt/felsgruppen/<Feld>/plan.json        dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision},
                                                         akteure[] (große Stücke, rolle "akteur"), entfernen, ft_ordner, ft_praefix
  Akteur-Instanzen liegen zusätzlich in akteur_<Netzname>.f32 (gleiches Format), damit ein generischer Setzer sie nicht als
  Foliage setzt: dateien-Eintrag trägt rolle "akteur".

Quellen (Regeln, Zahlen): antworten/verteilung-fels-organisch.md, antworten/klippennetze-a5.md (Eingraben 25–45 %,
Schichtneigung je Front, Gruppen 2–5), antworten/bildkritik-witcher-messlatte.md (Cluster statt Stufenkanten, Floating-Check),
vorlagen/FORMAT.md (Raster, Instanzformat, Budgets). Geologie: Schutthalden 30–38° (Richtwert), Sturzsortierung optional.
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

try:  # numba ist optional; alles läuft auch rein mit NumPy
    import numba  # noqa: F401
    HAVE_NUMBA = True
except Exception:  # pragma: no cover
    HAVE_NUMBA = False

NX, NY, FELD = 9577, 7057, 1008
X0, Y0 = 4730.5, 4060.5  # X_m = j - X0, Y_m = i - Y0
BIOME = ["aue", "bergwald", "gletscher", "tundra", "canyon", "oedland", "heide", "elfenwald", "dschungel", "kueste", "wueste",
         "lava", "frost", "sumpf", "fjord"]
ROLLEN_ORDNUNG = ["hero", "wand", "band", "block", "platte", "stein", "kiesel"]
U64 = np.uint64


def log(*a):
    print("[felsgruppen]", *a, flush=True)


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
    """teile: int-Arrays/Skalare (broadcastbar). Liefert uint64-Hash."""
    h = None
    for t in teile:
        a = np.atleast_1d(np.asarray(t)).astype(np.int64).astype(U64)
        h = a * U64(0x9E3779B97F4A7C15) if h is None else _mix(h ^ (a + U64(0x9E3779B97F4A7C15)))
    return _mix(h)


def uni(h, salz):
    """Gleichverteilte in [0,1) aus Hash h und Salz (int)."""
    return (_mix(h ^ U64(salz * 0x9E3779B97F4A7C15 & 0xFFFFFFFFFFFFFFFF)) >> U64(11)).astype(np.float64) * (1.0 / 9007199254740992.0)


def zwischen(h, salz, lo, hi):
    return lo + (hi - lo) * uni(h, salz)


def ganz(h, salz, lo, hi):
    """Ganzzahl in [lo, hi] (inklusiv)."""
    return lo + np.minimum((uni(h, salz) * (hi - lo + 1)).astype(np.int64), hi - lo)


# ----------------------------------------------------------------------------------------------------------------------
# Raster-Operatoren (rein NumPy, separierbar)
# ----------------------------------------------------------------------------------------------------------------------
def gauss1d(a, sigma, axis):
    r = max(1, int(3.0 * sigma + 0.5))
    x = np.arange(-r, r + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sigma) ** 2)
    k /= k.sum()
    pad = [(0, 0), (0, 0)]
    pad[axis] = (r, r)
    ap = np.pad(a, pad, mode="edge")
    out = np.zeros(a.shape, dtype=np.float64)
    n = a.shape[axis]
    for t in range(len(k)):
        sl = [slice(None), slice(None)]
        sl[axis] = slice(t, t + n)
        out += k[t] * ap[tuple(sl)]
    return out


def gauss(a, sigma):
    return gauss1d(gauss1d(a.astype(np.float64), sigma, 0), sigma, 1)


def _shift(a, d, axis, fill):
    out = np.full_like(a, fill)
    n = a.shape[axis]
    if abs(d) >= n:
        return out
    src = [slice(None), slice(None)]
    dst = [slice(None), slice(None)]
    if d > 0:
        src[axis] = slice(0, n - d)
        dst[axis] = slice(d, n)
    else:
        src[axis] = slice(-d, n)
        dst[axis] = slice(0, n + d)
    out[tuple(dst)] = a[tuple(src)]
    return out


def boxmax(a, r, fill=-np.inf):
    """Max-Filter mit Chebyshev-Radius ≥ r (Verdopplungsschritte; effektiver Radius = nächste 2^k-1 ≥ r)."""
    m = a
    for axis in (0, 1):
        step = 1
        while step <= r:
            m = np.maximum(m, np.maximum(_shift(m, step, axis, fill), _shift(m, -step, axis, fill)))
            step *= 2
    return m


def boxmin(a, r):
    return -boxmax(-a, r, fill=-np.inf)


def dilate(mask, r):
    if r <= 0:
        return mask.copy()
    return boxmax(mask.astype(np.uint8), r, fill=0) > 0


def hessian(hs):
    gy, gx = np.gradient(hs)
    hxx = np.gradient(gx, axis=1)
    hyy = np.gradient(gy, axis=0)
    hxy = np.gradient(gx, axis=0)
    tr = 0.5 * (hxx + hyy)
    dd = np.sqrt((0.5 * (hxx - hyy)) ** 2 + hxy ** 2)
    lam1 = tr + dd  # größte Krümmung (positiv = konkav/Mulde)
    lam2 = tr - dd  # kleinste (negativ = konvex/Grat)
    theta1 = 0.5 * np.arctan2(2.0 * hxy, hxx - hyy)  # Richtung des Eigenvektors zu lam1 (= Gratachse, Winkel in (x,y))
    return lam1, lam2, theta1


def wertrauschen(x, y, gitter, seed, salz):
    """Bilinear interpoliertes Gitterrauschen in [0,1) (x, y in m, Weltkoordinaten), deterministisch."""
    gx = np.floor(x / gitter)
    gy = np.floor(y / gitter)
    fx = x / gitter - gx
    fy = y / gitter - gy
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    gx = gx.astype(np.int64)
    gy = gy.astype(np.int64)

    def v(dx, dy):
        return uni(hash64(seed, 7001 + salz, gx + dx, gy + dy), 3)

    return (v(0, 0) * (1 - fx) + v(1, 0) * fx) * (1 - fy) + (v(0, 1) * (1 - fx) + v(1, 1) * fx) * fy


# ----------------------------------------------------------------------------------------------------------------------
# Daten laden
# ----------------------------------------------------------------------------------------------------------------------
def feld_bereich(name):
    name = name.strip().upper()
    if len(name) < 2 or not name[0].isalpha() or not name[1:].isdigit():
        raise ValueError("Feldname wie 'B4' erwartet, nicht %r" % name)
    s = ord(name[0]) - 65
    r = int(name[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise ValueError("Feld %s außerhalb A1…J7" % name)
    j0, i0 = s * FELD, (r - 1) * FELD
    return i0, min(i0 + FELD, NY), j0, min(j0 + FELD, NX)


def lade_raster(pfad, dtype, win, pflicht=False, name=""):
    """Fenster (i0,i1,j0,j1) aus NY×NX-Raster per memmap; None wenn fehlt (oder Abbruch bei pflicht)."""
    if not os.path.isfile(pfad):
        if pflicht:
            sys.exit("FEHLT (Pflicht): %s" % pfad)
        log("Hinweis: %s fehlt (%s) – wird ohne fortgesetzt." % (name or os.path.basename(pfad), pfad))
        return None
    itemsize = np.dtype(dtype).itemsize
    groesse = os.path.getsize(pfad)
    if groesse != NX * NY * itemsize:
        msg = "%s hat %d Byte, erwartet %d (NY=%d × NX=%d × %d)" % (pfad, groesse, NX * NY * itemsize, NY, NX, itemsize)
        if pflicht:
            sys.exit("FEHLER: " + msg)
        log("Hinweis: " + msg + " – ignoriert.")
        return None
    mm = np.memmap(pfad, dtype=dtype, mode="r", shape=(NY, NX))
    i0, i1, j0, j1 = win
    return np.array(mm[i0:i1, j0:j1])


def lade_netze(basis, skriptdir):
    kandidaten = [os.path.join(basis, "daten", "netze.csv"), os.path.join(skriptdir, "netze.csv"),
                  os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "netze.csv")]
    for p in kandidaten:
        if os.path.isfile(p):
            netze = {}
            with open(p, encoding="utf-8") as f:
                for r in csv.DictReader(f, delimiter=";"):
                    netze[r["pfad"]] = {"name": r["name"], "paket": r["paket"], "nanite": r["nanite"] == "1",
                                        "sx": float(r["groesse_x_m"] or 0), "sy": float(r["groesse_y_m"] or 0),
                                        "sz": float(r["groesse_z_m"] or 0),
                                        "kollision": int(r["kollision_primitive"] or 0)}
            log("Inventar: %d Netze aus %s" % (len(netze), p))
            return netze
    sys.exit("FEHLT (Pflicht): daten/netze.csv (gesucht: %s)" % ", ".join(kandidaten))


def lade_masse(basis, skriptdir):
    for p in [os.path.join(basis, "daten", "netze_masse.json"), os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "netze_masse.json")]:
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            return {k: (v["min"], v["max"]) for k, v in d.items() if "min" in v and "max" in v}
    log("Hinweis: daten/netze_masse.json fehlt – Pivot-Lage aus Regeln (netz_pivot_mitte) bzw. Annahme Pivot unten.")
    return {}


def dominantes_biom(basis, skriptdir, feld):
    """Dominantes Biom des Feldes aus daten/biome_je_feld.json (für Kennzahl 0 = Weltgelände); None wenn unbekannt."""
    for p in [os.path.join(basis, "daten", "biome_je_feld.json"), os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "biome_je_feld.json")]:
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                bp = d["felder"][feld]["biome_prozent"]
                bn = sorted(bp, key=lambda t: -t[1])[0][0]
                return bn if bn in BIOME else None
            except Exception as e:
                log("Hinweis: biome_je_feld.json unlesbar (%s)" % e)
                return None
    return None


def lade_biome(welt_dir, win, basis, skriptdir, feld, regeln, hang):
    """Biom-Index je Zelle (Index in BIOME) aus eigner.r8 + welt.json; Kennzahl 0 → dominantes Feldbiom, Fallback aue."""
    eig = lade_raster(os.path.join(welt_dir, "eigner.r8"), np.uint8, win, name="eigner.r8")
    E0 = regeln.get("eigner0", {})
    dom = dominantes_biom(basis, skriptdir, feld)
    b0 = BIOME.index(dom) if dom else 0
    tab = np.full(256, b0, dtype=np.int16)
    wj = os.path.join(welt_dir, "welt.json")
    if eig is None or not os.path.isfile(wj):
        if eig is not None:
            log("Hinweis: welt.json fehlt – Biom überall '%s'." % BIOME[b0])
        out = np.full((win[1] - win[0], win[3] - win[2]), b0, dtype=np.int16)
        if dom is None and hang is not None:
            out[hang >= E0.get("fallback_hang_grad", 25)] = BIOME.index(E0.get("fallback_biom", "bergwald"))
        return out
    with open(wj, encoding="utf-8") as f:
        welt = json.load(f)
    kacheln = welt.get("kacheln", welt)
    eintraege = []
    if isinstance(kacheln, dict):
        for k, v in kacheln.items():
            try:
                eintraege.append((int(k), v))
            except ValueError:
                if isinstance(v, dict) and "id" in v:
                    eintraege.append((int(v["id"]), v))
    elif isinstance(kacheln, list):
        for idx, v in enumerate(kacheln):
            k = v.get("id", v.get("kennzahl", idx)) if isinstance(v, dict) else idx
            eintraege.append((int(k), v))
    unbekannt = set()
    for k, v in eintraege:
        if not (0 <= k < 256):
            continue
        rez = v.get("rezept", v.get("biom", "")) if isinstance(v, dict) else str(v)
        rez = str(rez).lower()
        b = 0
        if k == 0 or rez in ("", "0", "welt", "weltgelaende", "weltgelände"):
            b = 0
        else:
            for i, bn in enumerate(BIOME):
                if bn in rez:
                    b = i
                    break
            else:
                if "vulkan" in rez or "lava" in rez:
                    b = BIOME.index("lava")
                elif "glet" in rez or "eis" in rez:
                    b = BIOME.index("gletscher")
                elif "wald" in rez:
                    b = BIOME.index("bergwald")
                else:
                    unbekannt.add(rez)
        tab[k] = b0 if k == 0 else b
    if unbekannt:
        log("Hinweis: unbekannte Rezepte in welt.json → aue: %s" % ", ".join(sorted(unbekannt))[:300])
    out = tab[eig]
    if dom is None and hang is not None:
        steil = (eig == 0) & (hang >= E0.get("fallback_hang_grad", 25))
        out[steil] = BIOME.index(E0.get("fallback_biom", "bergwald"))
        log("Hinweis: biome_je_feld.json fehlt – Weltgelände (0) = aue, steile Zellen (≥ %s°) = %s" % (E0.get("fallback_hang_grad", 25), E0.get("fallback_biom", "bergwald")))
    else:
        log("Biome: Kennzahl 0 (Weltgelände) → %s; Anteile im Fenster: %s" % (
            BIOME[b0], ", ".join("%s %.0f%%" % (BIOME[i], 100 * (out == i).mean()) for i in np.unique(out))))
    return out


def finde_polylinien(obj, out, tiefe=0):
    """Sucht rekursiv dicts mit 'punkte' (Liste von [x_cm, y_cm, (z), (breite_cm), …])."""
    if tiefe > 6:
        return
    if isinstance(obj, dict):
        p = obj.get("punkte")
        if isinstance(p, list) and len(p) >= 3 and isinstance(p[0], (list, tuple)) and len(p[0]) >= 2:
            out.append(p)
        for v in obj.values():
            finde_polylinien(v, out, tiefe + 1)
    elif isinstance(obj, list):
        for v in obj:
            finde_polylinien(v, out, tiefe + 1)


def lade_fluesse(welt_dir):
    p = os.path.join(welt_dir, "wasser_welt.json")
    if not os.path.isfile(p):
        log("Hinweis: wasser_welt.json fehlt – Klasse prallhang entfällt.")
        return []
    with open(p, encoding="utf-8") as f:
        w = json.load(f)
    out = []
    finde_polylinien(w.get("fluesse", w), out)
    log("Flüsse: %d Polylinien aus wasser_welt.json" % len(out))
    return out


def lade_positionen_f32(ordner):
    """Alle *.f32 in ordner → (x_cm, y_cm) Arrays."""
    xs, ys = [], []
    if not os.path.isdir(ordner):
        return None
    for fn in sorted(os.listdir(ordner)):
        if fn.lower().endswith(".f32"):
            a = np.fromfile(os.path.join(ordner, fn), dtype="<f4")
            if a.size % 10 == 0 and a.size:
                a = a.reshape(-1, 10)
                xs.append(a[:, 0])
                ys.append(a[:, 1])
    if not xs:
        return None
    return np.concatenate(xs), np.concatenate(ys)


def positionen_aus_json(obj, out, tiefe=0):
    if tiefe > 6:
        return
    if isinstance(obj, dict):
        if "x" in obj and "y" in obj and isinstance(obj["x"], (int, float)) and isinstance(obj["y"], (int, float)):
            out.append((float(obj["x"]), float(obj["y"])))
        for v in obj.values():
            positionen_aus_json(v, out, tiefe + 1)
    elif isinstance(obj, list):
        if len(obj) in (7, 10) and all(isinstance(v, (int, float)) for v in obj[:2]):
            out.append((float(obj[0]), float(obj[1])))
        else:
            for v in obj:
                positionen_aus_json(v, out, tiefe + 1)


def sperrmaske(win, pos, radius):
    """Boolesche Maske im Fenster: True in radius um Positionen (cm-Weltkoordinaten)."""
    i0, i1, j0, j1 = win
    m = np.zeros((i1 - i0, j1 - j0), dtype=bool)
    if pos is None:
        return m
    x, y = pos
    j = np.round(x / 100.0 + X0).astype(np.int64) - j0
    i = np.round(y / 100.0 + Y0).astype(np.int64) - i0
    ok = (i >= 0) & (i < m.shape[0]) & (j >= 0) & (j < m.shape[1])
    m[i[ok], j[ok]] = True
    return dilate(m, int(round(radius)))


# ----------------------------------------------------------------------------------------------------------------------
# Geometrie
# ----------------------------------------------------------------------------------------------------------------------
def bilinear(h, fi, fj):
    i = np.clip(np.floor(fi).astype(np.int64), 0, h.shape[0] - 2)
    j = np.clip(np.floor(fj).astype(np.int64), 0, h.shape[1] - 2)
    di = np.clip(fi - i, 0, 1)
    dj = np.clip(fj - j, 0, 1)
    return ((h[i, j] * (1 - dj) + h[i, j + 1] * dj) * (1 - di) + (h[i + 1, j] * (1 - dj) + h[i + 1, j + 1] * dj) * di)


def quat_aus_yaw_up(yaw_rad, up):
    """Rotation mit Z-Achse = up (N×3) und X-Achse ≈ (cos yaw, sin yaw); Quaternion (x,y,z,w). Basis X×Y=Z wie in UE."""
    f0 = np.stack([np.cos(yaw_rad), np.sin(yaw_rad), np.zeros_like(yaw_rad)], axis=1)
    right = np.cross(up, f0)
    nr = np.linalg.norm(right, axis=1, keepdims=True)
    nr[nr < 1e-6] = 1.0
    right /= nr
    fwd = np.cross(right, up)
    m = np.stack([fwd, right, up], axis=2)  # Spalten = Achsen: m[:, :, 0] = X
    m00, m11, m22 = m[:, 0, 0], m[:, 1, 1], m[:, 2, 2]
    tr = m00 + m11 + m22
    q = np.zeros((len(tr), 4))
    # Shepperd: vier Fälle, vektorisiert
    c0 = tr > 0
    s = np.sqrt(np.maximum(tr, 0) + 1.0) * 2
    s[~c0] = 1.0
    q[c0, 3] = 0.25 * s[c0]
    q[c0, 0] = (m[c0, 2, 1] - m[c0, 1, 2]) / s[c0]
    q[c0, 1] = (m[c0, 0, 2] - m[c0, 2, 0]) / s[c0]
    q[c0, 2] = (m[c0, 1, 0] - m[c0, 0, 1]) / s[c0]
    c1 = (~c0) & (m00 > m11) & (m00 > m22)
    s = np.sqrt(np.maximum(1.0 + m00 - m11 - m22, 1e-12)) * 2
    q[c1, 3] = (m[c1, 2, 1] - m[c1, 1, 2]) / s[c1]
    q[c1, 0] = 0.25 * s[c1]
    q[c1, 1] = (m[c1, 0, 1] + m[c1, 1, 0]) / s[c1]
    q[c1, 2] = (m[c1, 0, 2] + m[c1, 2, 0]) / s[c1]
    c2 = (~c0) & (~c1) & (m11 > m22)
    s = np.sqrt(np.maximum(1.0 + m11 - m00 - m22, 1e-12)) * 2
    q[c2, 3] = (m[c2, 0, 2] - m[c2, 2, 0]) / s[c2]
    q[c2, 0] = (m[c2, 0, 1] + m[c2, 1, 0]) / s[c2]
    q[c2, 1] = 0.25 * s[c2]
    q[c2, 2] = (m[c2, 1, 2] + m[c2, 2, 1]) / s[c2]
    c3 = (~c0) & (~c1) & (~c2)
    s = np.sqrt(np.maximum(1.0 + m22 - m00 - m11, 1e-12)) * 2
    q[c3, 3] = (m[c3, 1, 0] - m[c3, 0, 1]) / s[c3]
    q[c3, 0] = (m[c3, 0, 2] + m[c3, 2, 0]) / s[c3]
    q[c3, 1] = (m[c3, 1, 2] + m[c3, 2, 1]) / s[c3]
    q[c3, 2] = 0.25 * s[c3]
    q /= np.linalg.norm(q, axis=1, keepdims=True)
    return q


# ----------------------------------------------------------------------------------------------------------------------
# Planer
# ----------------------------------------------------------------------------------------------------------------------
class Planer:
    def __init__(self, regeln, netze, masse, basis, faktor, skriptdir="."):
        self.R = regeln
        self.skriptdir = skriptdir
        self.netze = netze
        self.masse = masse
        self.basis = basis
        self.faktor = faktor
        self.seed = int(regeln.get("seed", 1))
        self.pivot_mitte = set(regeln.get("netz_pivot_mitte", []))
        self.pal_info = {}
        fehlend = []
        for pal, rollen in regeln["paletten"].items():
            for rolle, pfade in rollen.items():
                for p in pfade:
                    if p not in netze:
                        fehlend.append(p)
        if fehlend:
            sys.exit("FEHLER: %d Paletten-Pfade nicht in netze.csv, z. B. %s" % (len(fehlend), fehlend[:3]))

    # Netz-Kennwerte -------------------------------------------------------------------------------------------------
    def netz_mass(self, pfad):
        n = self.netze[pfad]
        h_cm = n["sz"] * 100.0
        r_cm = 0.5 * max(n["sx"], n["sy"]) * 100.0
        if pfad in self.masse:
            mn, mx = self.masse[pfad]
            minz = mn[2]
            h_cm = mx[2] - mn[2]
            r_cm = 0.5 * max(mx[0] - mn[0], mx[1] - mn[1])
        elif pfad in self.pivot_mitte:
            minz = -0.5 * h_cm
        else:
            minz = 0.0
        return h_cm, r_cm, minz

    def palette_arrays(self, pal, rolle):
        pfade = self.R["paletten"][pal].get(rolle, [])
        if not pfade:
            return None
        key = (pal, rolle)
        if key not in self.pal_info:
            h, r, mz = zip(*[self.netz_mass(p) for p in pfade])
            self.pal_info[key] = (pfade, np.array(h), np.array(r), np.array(mz))
        return self.pal_info[key]

    # Hauptlauf ------------------------------------------------------------------------------------------------------
    def plane_feld(self, feld, welt_dir, bild):
        t0 = time.time()
        R = self.R
        rand = int(R.get("rand_m", 64))
        i0f, i1f, j0f, j1f = feld_bereich(feld)
        win = (max(0, i0f - rand), min(NY, i1f + rand), max(0, j0f - rand), min(NX, j1f + rand))
        i0, i1, j0, j1 = win
        self.win = win
        self.feld_box = (i0f, i1f, j0f, j1f)
        h = lade_raster(os.path.join(welt_dir, "hoehe.f32"), "<f4", win, pflicht=True, name="hoehe.f32").astype(np.float64)
        H, W = h.shape
        self.h = h
        ii, jj = np.mgrid[0:H, 0:W]
        self.ii, self.jj = ii, jj
        xg = (jj + j0) - X0  # Welt-m
        yg = (ii + i0) - Y0

        # Masken ---------------------------------------------------------------------------------------------------
        def r8(name):
            a = lade_raster(os.path.join(welt_dir, name), np.uint8, win, name=name)
            return a

        wasser = r8("karte_wasser.r8")
        weg = r8("karte_weg.r8")
        ort = r8("karte_ort.r8")
        A = R["ausschluss"]
        self.m_wasser = dilate(wasser > 0, A["wasser_m"]) if wasser is not None else (h <= 0.05)
        self.m_wasser_roh = (wasser > 0) if wasser is not None else (h <= 0.05)
        self.m_weg = dilate(weg > 0, A["weg_m"]) if weg is not None else np.zeros_like(self.m_wasser)
        self.m_weg_klein = dilate(weg > 0, int(math.ceil(2.5))) if weg is not None else np.zeros_like(self.m_wasser)
        self.m_ort = dilate(ort > 0, A["ort_m"]) if ort is not None else np.zeros_like(self.m_wasser)

        # Lagen (optional) → Faktor
        lagen = R.get("lagen", {})
        fels = np.zeros_like(h)
        for ln in lagen.get("fels_boost", []):
            a = lade_raster(os.path.join(welt_dir, "lage_%s.r8" % ln), np.uint8, win, name="lage_%s.r8" % ln)
            if a is not None:
                fels = np.maximum(fels, a / 255.0)
        ger = np.zeros_like(h)
        for ln in lagen.get("geroell_boost", []):
            a = lade_raster(os.path.join(welt_dir, "lage_%s.r8" % ln), np.uint8, win, name="lage_%s.r8" % ln)
            if a is not None:
                ger = np.maximum(ger, a / 255.0)
        schnee = lade_raster(os.path.join(welt_dir, "lage_%s.r8" % lagen.get("schnee_hemmung", "Schnee")), np.uint8, win, name="lage_Schnee.r8")
        schnee = schnee / 255.0 if schnee is not None else np.zeros_like(h)
        fmin, fmax = lagen.get("faktor_min", 0.5), lagen.get("faktor_max", 1.5)
        self.f_fels = np.clip(0.6 + 0.9 * fels - 0.3 * schnee, fmin, fmax)
        self.f_ger = np.clip(0.7 + 0.8 * ger, fmin, fmax)

        # Vorhandene Ebenen (Abstand) --------------------------------------------------------------------------------
        sperr = np.zeros_like(self.m_wasser)
        bst = lade_positionen_f32(os.path.join(welt_dir, "bestand", feld))
        if bst is None:
            log("Hinweis: bestand/%s/ fehlt – kein Baumabstand geprüft." % feld)
        else:
            sperr |= sperrmaske(win, bst, A["baum_m"])
            log("Bestand: %d Baum-Instanzen als Sperre (%.1f m)" % (len(bst[0]), A["baum_m"]))
        fs = os.path.join(welt_dir, "felsschalen", "plan_%s.json" % feld)
        if os.path.isfile(fs):
            with open(fs, encoding="utf-8") as f:
                pos = []
                positionen_aus_json(json.load(f), pos)
            if pos:
                p = np.array(pos)
                sperr |= sperrmaske(win, (p[:, 0], p[:, 1]), A["felsschale_m"])
                log("Felsschalen: %d Positionen aus plan_%s.json als Sperre (%.0f m)" % (len(pos), feld, A["felsschale_m"]))
            else:
                log("Hinweis: felsschalen/plan_%s.json ohne erkennbare Positionen (x/y) – keine Sperre." % feld)
        else:
            log("Hinweis: felsschalen/plan_%s.json fehlt – kein Abstand zu Felsschalen geprüft." % feld)
        self.m_sperr = sperr

        # Gelände-Ableitungen -----------------------------------------------------------------------------------------
        G = R["glaettung"]
        h1 = gauss(h, G["hang_sigma_m"])
        gy, gx = np.gradient(h1)
        gmag = np.hypot(gx, gy)
        self.hang = np.degrees(np.arctan(gmag))
        self.biom = lade_biome(welt_dir, win, self.basis, self.skriptdir, feld, R, self.hang)
        nz = 1.0 / np.sqrt(1.0 + gmag ** 2)
        self.normal = np.stack([-gx * nz, -gy * nz, nz], axis=2)
        gm = np.where(gmag > 1e-6, gmag, 1.0)
        self.abfall = np.stack([-gx / gm, -gy / gm], axis=2)  # Einheitsvektor hangabwärts (x,y)
        hs = gauss(h, G["kruemmung_sigma_m"])
        lam1, lam2, theta1 = hessian(hs)
        self.grat = -lam2  # > 0 konvex (Grat/Nase)
        self.mulde = lam1  # > 0 konkav (Rinne/Mulde)
        self.gratachse = theta1
        hs25 = gauss(h, G["massiv_sigma_m"])
        l1b, l2b, _ = hessian(hs25)
        self.hohl25 = l1b + l2b  # Laplace grob: > 0 Hangfuß/Mulde
        hs12 = gauss(h, G["kuppe_sigma_m"])
        self.hs12 = hs12
        self.land = h > 0.2

        # Wände und Schuttfächer
        K = R["klassen"]
        wand = self.hang >= K["fuss"]["wand_ab_grad"]
        relief = boxmax(hs, 12) - boxmin(hs, 12)
        grosse_wand = wand & (relief >= K["fuss"]["wand_hoehe_min_m"])
        wand_h = np.where(grosse_wand, h, -np.inf)
        self.fuss_stufe = np.full(h.shape, -1, dtype=np.int8)
        for si, st in reversed(list(enumerate(K["fuss"]["stufen"]))):
            d = int(st[1])
            oben = boxmax(wand_h, d) > h + 2.0
            self.fuss_stufe[oben] = si
        self.wand_ueber_128 = boxmax(wand_h, K["blockstrom"]["wand_umkreis_m"]) > h + K["blockstrom"]["wand_hoehe_min_m"]
        wand_nah = boxmax(wand_h, A["mulde_wand_umkreis_m"]) > h + A["mulde_wand_hoehe_min_m"]
        self.m_mulde = (self.mulde > A["mulde_staerke_min"]) & (~wand_nah)
        self.m_wand = wand
        self.xg, self.yg = xg, yg

        # Schichtung je Bergmassiv (Strike/Dip)
        S = R["schichtung"]
        st = wertrauschen(xg, yg, S["gitter_m"], self.seed, 1) * 2 * np.pi
        dip = np.radians(S["dip_grad"][0] + (S["dip_grad"][1] - S["dip_grad"][0]) * wertrauschen(xg, yg, S["gitter_m"], self.seed, 2))
        abst = S["band_abstand_m"][0] + (S["band_abstand_m"][1] - S["band_abstand_m"][0]) * wertrauschen(xg, yg, S["gitter_m"], self.seed, 3)
        self.strike, self.dip = st, dip
        phase = (hs - np.tan(dip) * (xg * np.cos(st) + yg * np.sin(st))) / abst
        self.m_band = (phase - np.floor(phase)) < S["band_breite_anteil"]

        # Allgemeine Ausschlüsse
        self.m_frei = self.land & ~self.m_wasser & ~self.m_weg & ~self.m_ort & (self.hang <= A["max_hang_grad"])
        self.m_frei_klein = self.land & ~self.m_wasser & ~self.m_weg_klein & ~self.m_ort & (self.hang <= A["max_hang_grad"])

        # Gruppen je Klasse -------------------------------------------------------------------------------------------
        inst = []  # Liste von dicts mit Arrays
        self.statistik = {}
        gruppen_gesamt = 0
        for kname in ["grat", "band", "wand", "fuss", "blockstrom", "kuppe", "prallhang"]:
            if kname == "prallhang":
                g = self.kandidaten_prallhang(welt_dir)
            elif kname == "kuppe":
                g = self.kandidaten_kuppe()
            else:
                g = self.kandidaten_gitter(kname)
            if g is None or len(g["ci"]) == 0:
                self.statistik[kname] = {"gruppen": 0}
                continue
            n_vor = len(g["ci"])
            teile = self.gruppe_erzeugen(kname, g)
            n_inst = int(sum(len(t["x"]) for t in teile))
            self.statistik[kname] = {"gruppen": n_vor, "instanzen": n_inst}
            gruppen_gesamt += n_vor
            inst.extend(teile)
        alle = self.zusammenfuehren(inst)
        alle = self.budget(alle)
        t1 = time.time()
        self.schreiben(feld, alle, welt_dir)
        if bild:
            self.bild(feld, alle)
        log("%s: %d Gruppen, %d Instanzen (%d mit Kollision, %d Akteure) in %.1f s (Planung %.1f s)" % (
            feld, gruppen_gesamt, len(alle["x"]), int(alle["koll"].sum()), int(alle["akteur"].sum()), time.time() - t0, t1 - t0))
        return alle

    # Kandidaten ----------------------------------------------------------------------------------------------------
    def _gitterpunkte(self, raster_m, salz):
        """Gejitterte Gitterpunkte (global deterministisch) im Fenster: Rasterkoordinaten (fi, fj) + Hash."""
        i0, i1, j0, j1 = self.win
        gi = np.arange(i0 // raster_m, (i1 - 1) // raster_m + 1)
        gj = np.arange(j0 // raster_m, (j1 - 1) // raster_m + 1)
        GI, GJ = np.meshgrid(gi, gj, indexing="ij")
        hsh = hash64(self.seed, salz, GI.ravel(), GJ.ravel())
        fi = (GI.ravel() + uni(hsh, 1)) * raster_m - i0
        fj = (GJ.ravel() + uni(hsh, 2)) * raster_m - j0
        ok = (fi >= 1) & (fi < self.h.shape[0] - 1) & (fj >= 1) & (fj < self.h.shape[1] - 1)
        return fi[ok], fj[ok], hsh[ok]

    def _klasse_erlaubt(self, kname, ci, cj):
        b = self.biom[ci, cj]
        aus = self.R.get("biom_klassen_aus", {})
        erlaubt = np.ones(len(ci), dtype=bool)
        for bn, kl in aus.items():
            if kname in kl and bn in BIOME:
                erlaubt &= b != BIOME.index(bn)
        bf = np.array([self.R["biom_faktor"].get(bn, 1.0) for bn in BIOME])
        return erlaubt, bf[b]

    def kandidaten_gitter(self, kname):
        K = self.R["klassen"][kname]
        salz = {"grat": 11, "band": 12, "wand": 13, "fuss": 14, "blockstrom": 15}[kname]
        fi, fj, hsh = self._gitterpunkte(K["raster_m"], salz)
        ci, cj = np.round(fi).astype(np.int64), np.round(fj).astype(np.int64)
        hang = self.hang[ci, cj]
        ok = self.m_frei[ci, cj] & (hang >= K["hang_grad"][0]) & (hang <= K["hang_grad"][1])
        p = np.full(len(ci), K["p"] * self.faktor)
        if kname == "grat":
            ok &= (self.grat[ci, cj] >= K["grat_staerke_min"]) & ~self.m_mulde[ci, cj]
            p *= self.f_fels[ci, cj] * np.clip(self.grat[ci, cj] / (3 * K["grat_staerke_min"]), 0.5, 1.5)
            yaw = self.gratachse[ci, cj]
        elif kname == "band":
            ok &= self.m_band[ci, cj] & ~self.m_mulde[ci, cj] & (self.grat[ci, cj] > -0.01)
            p *= self.f_fels[ci, cj]
            yaw = self.strike[ci, cj]
        elif kname == "wand":
            ok &= (self.grat[ci, cj] >= K["nase_min"])
            p *= self.f_fels[ci, cj]
            yaw = self.strike[ci, cj]
        elif kname == "fuss":
            ok &= (self.fuss_stufe[ci, cj] >= 0) & ~self.m_wand[ci, cj] & ~self.m_mulde[ci, cj]
            p *= self.f_ger[ci, cj]
            yaw = np.arctan2(self.abfall[ci, cj, 1], self.abfall[ci, cj, 0])
        else:  # blockstrom
            ok &= self.wand_ueber_128[ci, cj] & (self.hohl25[ci, cj] >= K["hohl_min"]) & ~self.m_wand[ci, cj]
            p *= self.f_ger[ci, cj]
            yaw = np.arctan2(self.abfall[ci, cj, 1], self.abfall[ci, cj, 0])
        erl, bf = self._klasse_erlaubt(kname, ci, cj)
        ok &= erl & (uni(hsh, 5) < p * bf)
        return {"ci": ci[ok], "cj": cj[ok], "fi": fi[ok], "fj": fj[ok], "h": hsh[ok], "yaw": yaw[ok],
                "stufe": self.fuss_stufe[ci[ok], cj[ok]] if kname == "fuss" else None}

    def kandidaten_kuppe(self):
        K = self.R["klassen"]["kuppe"]
        hs = self.hs12
        peak = (hs >= boxmax(hs, K["umkreis_m"]) - 1e-6) & self.land & (self.hang <= K["hang_grad"][1]) & self.m_frei & ~self.m_wand
        peak[:2, :] = False; peak[-2:, :] = False; peak[:, :2] = False; peak[:, -2:] = False  # Fensterrand ist kein Gipfel
        ci, cj = np.nonzero(peak)
        if len(ci) == 0:
            return None
        i0, i1, j0, j1 = self.win
        # eine Kuppe je Umkreis-Zelle (Plateaus mit gleichen Werten)
        key = (ci + i0) // K["umkreis_m"] * 100000 + (cj + j0) // K["umkreis_m"]
        _, idx = np.unique(key, return_index=True)
        ci, cj = ci[idx], cj[idx]
        hsh = hash64(self.seed, 16, ci + i0, cj + j0)
        erl, bf = self._klasse_erlaubt("kuppe", ci, cj)
        ok = erl & (uni(hsh, 5) < K["p"] * self.faktor * bf)
        return {"ci": ci[ok], "cj": cj[ok], "fi": ci[ok].astype(float), "fj": cj[ok].astype(float), "h": hsh[ok],
                "yaw": zwischen(hsh[ok], 6, 0, 2 * np.pi), "stufe": None}

    def kandidaten_prallhang(self, welt_dir):
        K = self.R["klassen"]["prallhang"]
        linien = lade_fluesse(welt_dir)
        if not linien:
            return None
        i0, i1, j0, j1 = self.win
        H, W = self.h.shape
        out = {"ci": [], "cj": [], "fi": [], "fj": [], "h": [], "yaw": []}
        for pts in linien:
            P = np.array([[p[0], p[1], (p[3] if len(p) > 3 else 400.0)] for p in pts], dtype=np.float64)
            fj = P[:, 0] / 100.0 + X0 - j0
            fi = P[:, 1] / 100.0 + Y0 - i0
            if not ((fi > -200) & (fi < H + 200) & (fj > -200) & (fj < W + 200)).any():
                continue
            if len(P) < 3:
                continue
            d1 = np.stack([fj[1:-1] - fj[:-2], fi[1:-1] - fi[:-2]], axis=1)
            d2 = np.stack([fj[2:] - fj[1:-1], fi[2:] - fi[1:-1]], axis=1)
            l1 = np.linalg.norm(d1, axis=1) + 1e-6
            l2 = np.linalg.norm(d2, axis=1) + 1e-6
            t1, t2 = d1 / l1[:, None], d2 / l2[:, None]
            kreuz = t1[:, 0] * t2[:, 1] - t1[:, 1] * t2[:, 0]
            punkt = np.clip((t1 * t2).sum(1), -1, 1)
            winkel = np.arctan2(kreuz, punkt)  # >0 Linkskurve (in (x,y)-Ebene)
            kappa = winkel / (0.5 * (l1 + l2))
            tang = t1 + t2
            tn = np.linalg.norm(tang, axis=1) + 1e-6
            tang /= tn[:, None]
            links = np.stack([-tang[:, 1], tang[:, 0]], axis=1)
            aussen = -np.sign(kappa)[:, None] * links  # Außenufer = gegen die Kurvenmitte
            s = np.concatenate([[0.0], np.cumsum(l1)])  # Bogenlänge an den Mittelpunkten
            stark = np.abs(kappa) >= K["kruemmung_min"]
            if not stark.any():
                continue
            idx = np.nonzero(stark)[0]
            # ein Kandidat je abstand_m Bogenlänge: stärkste Krümmung
            bucket = (s[idx] // K["abstand_m"]).astype(np.int64)
            order = np.lexsort((-np.abs(kappa[idx]), bucket))
            idx = idx[order]
            bucket = bucket[order]
            keep = np.concatenate([[True], bucket[1:] != bucket[:-1]])
            idx = idx[keep]
            hsh = hash64(self.seed, 17, np.round(P[idx + 1, 0]).astype(np.int64), np.round(P[idx + 1, 1]).astype(np.int64))
            ab = zwischen(hsh, 4, K["ufer_abstand_m"][0], K["ufer_abstand_m"][1]) + P[idx + 1, 2] / 200.0
            cj_f = fj[idx + 1] + aussen[idx, 0] * ab
            ci_f = fi[idx + 1] + aussen[idx, 1] * ab
            ok = (ci_f >= 1) & (ci_f < H - 1) & (cj_f >= 1) & (cj_f < W - 1)
            ci, cj = np.round(ci_f[ok]).astype(np.int64), np.round(cj_f[ok]).astype(np.int64)
            hsh, ci_f, cj_f = hsh[ok], ci_f[ok], cj_f[ok]
            yaw = np.arctan2(tang[idx[ok], 1], tang[idx[ok], 0])
            hang = self.hang[ci, cj]
            ok2 = self.m_frei[ci, cj] & (hang >= K["hang_grad"][0]) & (hang <= K["hang_grad"][1])
            erl, bf = self._klasse_erlaubt("prallhang", ci, cj)
            ok2 &= erl & (uni(hsh, 5) < self.faktor * bf)
            out["ci"].append(ci[ok2]); out["cj"].append(cj[ok2]); out["fi"].append(ci_f[ok2]); out["fj"].append(cj_f[ok2])
            out["h"].append(hsh[ok2]); out["yaw"].append(yaw[ok2])
        if not out["ci"]:
            return None
        g = {k: np.concatenate(v) for k, v in out.items()}
        g["stufe"] = None
        return g

    # Gruppen → Instanzen -------------------------------------------------------------------------------------------
    def gruppe_erzeugen(self, kname, g):
        K = self.R["klassen"][kname]
        GR = self.R["gruppe"]
        palname = np.array([self.R["biom_palette"].get(BIOME[b], "nordisch") for b in self.biom[g["ci"], g["cj"]]])
        teile = []
        for pal in np.unique(palname):
            sel = palname == pal
            gi, gj, gh, gyaw = g["fi"][sel], g["fj"][sel], g["h"][sel], g["yaw"][sel]
            stufe = g["stufe"][sel] if g.get("stufe") is not None else None
            n = len(gi)
            # Hauptstück: hero (mit Wahrscheinlichkeit) sonst block / band / wand / stufenrolle
            haupt_rolle = np.full(n, "block", dtype=object)
            if kname in ("grat", "kuppe", "prallhang"):
                haupt_rolle[uni(gh, 20) < K["hero_p"]] = "hero"
            elif kname == "band":
                haupt_rolle[:] = "band"
            elif kname == "wand":
                haupt_rolle[:] = "wand"
            elif kname == "fuss":
                st = np.array(K["stufen"], dtype=object)
                haupt_rolle = np.array([st[s][2] for s in stufe], dtype=object)
            # Anzahl Nebenstücke je Rolle
            def anzahl(rolle, salz):
                if rolle not in K:
                    return np.zeros(n, dtype=np.int64)
                lo, hi = K[rolle]
                return ganz(gh, salz, lo, hi)
            plan = []  # (rolle, anzahl-array, ist_haupt, radius-faktor-bereich, salz)
            plan.append(("__haupt__", np.ones(n, dtype=np.int64), True, (0, 0), 30))
            if kname == "band":
                plan.append(("band", np.maximum(anzahl("band", 31) - 1, 0), False, (0.7, 0.9), 31))
            elif kname == "wand":
                plan.append(("wand", np.maximum(anzahl("wand", 31) - 1, 0), False, (0.7, 0.9), 31))
                plan.append(("block", anzahl("block", 32), False, GR["neben_abstand_hero_r"], 32))
            elif kname == "fuss":
                plan.append(("__stufe__", np.maximum(anzahl("n", 31) - 1, 0), False, (0.8, 1.6), 31))
            else:
                plan.append(("block", anzahl("block", 32), False, GR["neben_abstand_hero_r"], 32))
            plan.append(("stein", anzahl("stein", 33), False, GR["stein_abstand_hero_r"], 33))
            if "platte" in self.R["paletten"][pal] and self.R["paletten"][pal]["platte"] and kname in ("blockstrom", "fuss", "kuppe"):
                plan.append(("platte", (uni(gh, 34) < 0.5).astype(np.int64), False, (1.0, 1.6), 34))
            # Hauptstück zuerst, um den Radius zu kennen
            haupt = self._stuecke(pal, kname, haupt_rolle, gi, gj, gh, gyaw, np.ones(n, dtype=np.int64), True, (0, 0), 30,
                                  None, stufe)
            if haupt is None:
                r_haupt = np.full(n, 150.0)
            else:
                r_haupt = haupt["r_haupt"]  # je Gruppe, cm
                teile.append(haupt)
            for rolle, cnt, _, rb, salz in plan[1:]:
                if cnt.sum() == 0:
                    continue
                if rolle == "__stufe__":
                    rl = haupt_rolle
                else:
                    rl = np.full(n, rolle, dtype=object)
                t = self._stuecke(pal, kname, rl, gi, gj, gh, gyaw, cnt, False, rb, salz, r_haupt, stufe)
                if t is not None:
                    teile.append(t)
            # Kiesel-Saum
            if "kiesel" in K and self.R["paletten"][pal].get("kiesel"):
                lo, hi = K["kiesel"]
                ring0, ring1 = GR["kiesel_ring_m"]
                d0, d1 = GR["kiesel_dichte_je_m2"]
                rh = r_haupt / 100.0
                flaeche = np.pi * ((rh + ring1) ** 2 - (rh + ring0) ** 2)
                dichte = zwischen(gh, 35, d0, d1) * self.faktor
                cnt = np.clip(np.round(flaeche * dichte), lo, hi).astype(np.int64)
                t = self._stuecke(pal, kname, np.full(n, "kiesel", dtype=object), gi, gj, gh, gyaw, cnt, False,
                                  (ring0, ring1), 36, r_haupt, stufe, ring=True)
                if t is not None:
                    teile.append(t)
        return [t for t in teile if t is not None and len(t["x"])]

    def _stuecke(self, pal, kname, rollen, gi, gj, gh, gyaw, cnt, ist_haupt, rb, salz, r_haupt, stufe, ring=False):
        """Erzeugt cnt[k] Stücke je Gruppe k mit Rolle rollen[k]. Liefert Instanz-Arrays (oder None)."""
        K = self.R["klassen"][kname]
        GR = self.R["gruppe"]
        RO = self.R["rollen"]
        idx = np.repeat(np.arange(len(gi)), cnt)
        if len(idx) == 0:
            return None
        m = np.arange(len(idx)) - np.repeat(np.cumsum(cnt) - cnt, cnt)  # Mitgliedsindex in der Gruppe
        hh = hash64(gh[idx], salz, m)
        rollen_i = rollen[idx]
        x = np.zeros(len(idx)); y = np.zeros(len(idx)); z = np.zeros(len(idx))
        pf_idx = np.zeros(len(idx), dtype=np.int64)
        pfade_alle = np.empty(len(idx), dtype=object)
        H_cm = np.zeros(len(idx)); R_cm = np.zeros(len(idx)); MZ = np.zeros(len(idx))
        sk = np.zeros(len(idx)); bury = np.zeros(len(idx)); kipp = np.zeros(len(idx)); nu = np.zeros(len(idx))
        koll = np.zeros(len(idx), dtype=bool); schatten = np.zeros(len(idx), dtype=bool)
        sicht = np.zeros((len(idx), 2))
        rolle_arr = np.empty(len(idx), dtype=object)
        for rolle in np.unique(rollen_i):
            s = rollen_i == rolle
            pa = self.palette_arrays(pal, rolle)
            if pa is None:
                # Rolle ohne Netze in dieser Palette → nächstkleinere Rolle
                for ersatz in ("block", "stein", "kiesel"):
                    pa = self.palette_arrays(pal, ersatz)
                    if pa is not None:
                        rolle = ersatz
                        break
                if pa is None:
                    continue
            pfade, hc, rc, mz = pa
            k = np.minimum((uni(hh[s], 40) * len(pfade)).astype(np.int64), len(pfade) - 1)
            ro = RO[rolle]
            sk_s = zwischen(hh[s], 41, ro["massstab"][0], ro["massstab"][1])
            if kname == "fuss":
                st = K["stufen"]
                f0 = np.array([st[v][3] for v in stufe[idx[s]]]); f1 = np.array([st[v][4] for v in stufe[idx[s]]])
                sk_s = sk_s * zwischen(hh[s], 42, f0, f1)
            if not ist_haupt and rolle in ("block", "band", "wand"):
                sk_s *= zwischen(hh[s], 43, 0.55, 0.9)  # Größenstaffelung: Nebenstücke kleiner als das Hauptstück
            pfade_alle[s] = np.array(pfade, dtype=object)[k]
            H_cm[s] = hc[k]; R_cm[s] = rc[k]; MZ[s] = mz[k]; sk[s] = sk_s
            eb = K.get("eingraben", ro["eingraben"]) if kname == "kuppe" else ro["eingraben"]
            bury[s] = zwischen(hh[s], 44, eb[0], eb[1])
            kipp[s] = np.radians(zwischen(hh[s], 45, ro["kippen_grad"][0], ro["kippen_grad"][1]))
            nu[s] = ro["nicht_uniform"]
            koll[s] = bool(ro["kollision"]); schatten[s] = bool(ro["schatten"]); sicht[s] = ro["sichtweite_cm"]
            rolle_arr[s] = rolle
        ok = np.array([p is not None for p in pfade_alle])
        if not ok.all():
            idx, m, hh, x, y = idx[ok], m[ok], hh[ok], x[ok], y[ok]
            pfade_alle, H_cm, R_cm, MZ, sk, bury, kipp, nu = (a[ok] for a in (pfade_alle, H_cm, R_cm, MZ, sk, bury, kipp, nu))
            koll, schatten, sicht, rolle_arr = koll[ok], schatten[ok], sicht[ok], rolle_arr[ok]
            if len(idx) == 0:
                return None
        r_eigen = R_cm * sk  # cm
        # Lage relativ zur Gruppenmitte
        gy = gyaw[idx]
        if ist_haupt:
            dist = np.zeros(len(idx)); ang = gy
        elif ring:
            dist = r_haupt[idx] + zwischen(hh, 46, rb[0], rb[1]) * 100.0
            ang = zwischen(hh, 47, 0, 2 * np.pi)
        elif rolle_arr[0] in ("band", "wand"):
            # entlang des Streichens aufgereiht, abwechselnd beide Seiten
            seite = np.where(m % 2 == 0, 1.0, -1.0)
            dist = (r_haupt[idx] + r_eigen) * zwischen(hh, 46, rb[0], rb[1]) * (1 + m // 2)
            ang = gy + np.where(seite > 0, 0.0, np.pi) + np.radians(zwischen(hh, 48, -8, 8))
        else:
            # Nebenblöcke/Steine: um die Hauptrichtung gestreut, Überlappung 10–30 % (nah) bzw. außen (Steine)
            streu = np.radians(GR["neben_yaw_streuung_grad"]) if rolle_arr[0] == "block" else np.pi
            seite = np.where(uni(hh, 49) < 0.5, 0.0, np.pi)
            ang = gy + seite + zwischen(hh, 48, -streu, streu)
            dist = (r_haupt[idx] + r_eigen) * zwischen(hh, 46, rb[0], rb[1])
            if kname in ("fuss", "blockstrom"):  # Falllinie: Stücke hangabwärts versetzt
                ang = gy + zwischen(hh, 48, -0.6, 0.6)
                dist = r_haupt[idx] * 0.5 + zwischen(hh, 46, rb[0], rb[1]) * 300.0
        fj = gj[idx] + np.cos(ang) * dist / 100.0
        fi = gi[idx] + np.sin(ang) * dist / 100.0
        # Gültigkeit: im Feld, frei
        i0, i1, j0, j1 = self.win
        i0f, i1f, j0f, j1f = self.feld_box
        H, W = self.h.shape
        inside = (fi >= 1) & (fi < H - 1) & (fj >= 1) & (fj < W - 1)
        fi_c = np.clip(fi, 1, H - 1.001); fj_c = np.clip(fj, 1, W - 1.001)
        ci, cj = np.round(fi_c).astype(np.int64), np.round(fj_c).astype(np.int64)
        im_feld = (fi + i0 >= i0f) & (fi + i0 < i1f) & (fj + j0 >= j0f) & (fj + j0 < j1f)
        klein = np.isin(rolle_arr.astype(str), ["stein", "kiesel", "platte"])
        frei = np.where(klein, self.m_frei_klein[ci, cj], self.m_frei[ci, cj] & ~self.m_sperr[ci, cj])
        # Floating-Check: Bodenhöhe unter dem Rand des Stücks darf nicht viel tiefer liegen als in der Mitte
        hz = bilinear(self.h, fi_c, fj_c)
        rr = np.clip(r_eigen / 100.0, 0.5, 20.0)
        hmin_rand = np.minimum.reduce([bilinear(self.h, np.clip(fi_c + d[0] * rr, 1, H - 1.001), np.clip(fj_c + d[1] * rr, 1, W - 1.001))
                                       for d in ((1, 0), (-1, 0), (0, 1), (0, -1))])
        # schwebend, wenn der Boden innerhalb des Stückradius tiefer abfällt als Eingrabtiefe + 60°-Hang erlauben
        nicht_schwebend = (hz - hmin_rand) <= bury * H_cm * sk / 100.0 + 0.3 + rr * np.tan(np.radians(60.0))
        ok = inside & im_feld & frei & nicht_schwebend
        if not ok.any():
            if ist_haupt:
                log("  %s/%s: alle %d Hauptstücke verworfen (im Fenster %d, im Feld %d, frei %d, nicht schwebend %d)" % (
                    kname, pal, len(ok), int(inside.sum()), int(im_feld.sum()), int(frei.sum()), int(nicht_schwebend.sum())))
            return None
        sel = ok
        idx, hh, fi, fj, ci, cj, hz = idx[sel], hh[sel], fi[sel], fj[sel], ci[sel], cj[sel], hz[sel]
        pfade_alle, H_cm, R_cm, MZ, sk, bury, kipp, nu = (a[sel] for a in (pfade_alle, H_cm, R_cm, MZ, sk, bury, kipp, nu))
        koll, schatten, sicht, rolle_arr, ang = koll[sel], schatten[sel], sicht[sel], rolle_arr[sel], ang[sel]
        gy = gyaw[idx]
        # Ausrichtung: Z auf Normale, Kippen in den Hang (Z-Achse Richtung bergauf), Yaw = Hauptrichtung ± Streuung
        n = self.normal[ci, cj]
        bergauf = -self.abfall[ci, cj]
        t = np.tan(kipp)[:, None]
        up = n + np.concatenate([bergauf * t, np.zeros((len(t), 1))], axis=1)
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        if rolle_arr[0] == "kiesel":
            yaw = zwischen(hh, 50, 0, 2 * np.pi)
        else:
            streu = np.radians(self.R["gruppe"]["yaw_streuung_grad"])
            yaw = gy + zwischen(hh, 50, -streu, streu)
        if kname == "band" or (kname == "wand"):
            # Schichtneigung: Z-Achse zusätzlich um die Streichrichtung um dip kippen
            d = self.dip[ci, cj]
            sv = np.stack([np.cos(gy), np.sin(gy), np.zeros_like(gy)], axis=1)  # Streichvektor
            # Rotation von up um sv um Winkel d (Rodrigues)
            up = up * np.cos(d)[:, None] + np.cross(sv, up) * np.sin(d)[:, None] + sv * (sv * up).sum(1, keepdims=True) * (1 - np.cos(d))[:, None]
            up /= np.linalg.norm(up, axis=1, keepdims=True)
        q = quat_aus_yaw_up(yaw, up)
        sx = sk * (1 + nu * (2 * uni(hh, 51) - 1))
        sy = sk * (1 + nu * (2 * uni(hh, 52) - 1))
        sz = sk
        x_cm = (fj + j0 - X0) * 100.0
        y_cm = (fi + i0 - Y0) * 100.0
        z_cm = hz * 100.0 - MZ * sz - bury * H_cm * sz
        hoehe_m = H_cm * sz / 100.0
        kol_ab = self.R.get("kollision_ab_hoehe_m", 0.8)
        koll = koll & (hoehe_m >= kol_ab)
        akteur_ab = self.R.get("akteur_ab_hoehe_m", 5.0)
        akteur = (rolle_arr.astype(str) == "wand") | ((rolle_arr.astype(str) == "hero") & (hoehe_m >= akteur_ab))
        if ist_haupt:
            r_haupt = np.zeros(len(gi))
            r_haupt[idx] = r_eigen[sel]
            fehl = r_haupt == 0
            r_haupt[fehl] = 150.0  # Hauptstück verworfen → Standardradius für Nebenstücke
        return {"x": x_cm, "y": y_cm, "z": z_cm, "q": q, "sx": sx, "sy": sy, "sz": sz, "pfad": pfade_alle,
                "rolle": rolle_arr.astype(str), "klasse": np.full(len(x_cm), kname), "koll": koll, "schatten": schatten,
                "sicht": sicht, "akteur": akteur, "hoehe_m": hoehe_m, "prio": uni(hh, 53),
                "r_haupt": r_haupt if ist_haupt else None, "ci": ci, "cj": cj}

    # Zusammenführen, Budget ------------------------------------------------------------------------------------------
    def zusammenfuehren(self, teile):
        keys = ["x", "y", "z", "q", "sx", "sy", "sz", "pfad", "rolle", "klasse", "koll", "schatten", "sicht", "akteur", "hoehe_m", "prio", "ci", "cj"]
        if not teile:
            return {k: np.zeros((0, 4) if k == "q" else (0, 2) if k == "sicht" else 0) for k in keys}
        return {k: np.concatenate([t[k] for t in teile]) for k in keys}

    def budget(self, a):
        B = self.R["budget"]
        n = len(a["x"])
        if n == 0:
            return a
        keep = np.ones(n, dtype=bool)
        rolle = a["rolle"]
        # je Rolle
        for ro, cap in B.get("je_rolle", {}).items():
            s = np.nonzero(keep & (rolle == ro))[0]
            if len(s) > cap:
                drop = s[np.argsort(-a["prio"][s])[: len(s) - cap]]
                keep[drop] = False
        # Kollision
        for ro in ["block", "band", "wand", "hero"]:
            nk = int((keep & a["koll"]).sum())
            if nk <= B["kollision"]:
                break
            s = np.nonzero(keep & a["koll"] & (rolle == ro))[0]
            drop = s[np.argsort(-a["prio"][s])[: min(len(s), nk - B["kollision"])]]
            keep[drop] = False
        # Akteure
        s = np.nonzero(keep & a["akteur"])[0]
        if len(s) > B["akteure"]:
            kleinste = s[np.argsort(a["hoehe_m"][s])[: len(s) - B["akteure"]]]
            a["akteur"][kleinste] = False  # bleiben als Foliage
        # Gesamt
        for ro in ["kiesel", "stein", "platte", "block", "band"]:
            ng = int(keep.sum())
            if ng <= B["gesamt"]:
                break
            s = np.nonzero(keep & (rolle == ro))[0]
            drop = s[np.argsort(-a["prio"][s])[: min(len(s), ng - B["gesamt"])]]
            keep[drop] = False
        if (~keep).any():
            log("Budget: %d Instanzen ausgedünnt (gesamt ≤ %d, Kollision ≤ %d, Akteure ≤ %d)" % (int((~keep).sum()), B["gesamt"], B["kollision"], B["akteure"]))
        return {k: v[keep] for k, v in a.items()}

    # Ausgabe --------------------------------------------------------------------------------------------------------
    def schreiben(self, feld, a, welt_dir):
        AU = self.R["ausgabe"]
        out = os.path.join(self.basis, AU["ordner"], feld)
        os.makedirs(out, exist_ok=True)
        for fn in os.listdir(out):
            if fn.endswith(".f32"):
                os.remove(os.path.join(out, fn))
        dateien = {}
        akteure = []
        n = len(a["x"])
        if n:
            rec = np.column_stack([a["x"], a["y"], a["z"], a["q"], a["sx"], a["sy"], a["sz"]]).astype("<f4")
            schluessel = np.char.add(np.where(a["akteur"], "akteur_", "").astype(str), np.array([self.netze[p]["name"] for p in a["pfad"]]).astype(str))
            for key in np.unique(schluessel):
                s = np.nonzero(schluessel == key)[0]
                rec[s].tofile(os.path.join(out, key + ".f32"))
                pf = a["pfad"][s[0]]
                ist_akteur = bool(a["akteur"][s[0]])
                sicht = a["sicht"][s]
                sw = [0, 0] if (sicht[:, 1] == 0).any() else [int(sicht[:, 0].min()), int(sicht[:, 1].max())]
                rollen = sorted(set(a["rolle"][s].tolist()))
                dateien[key] = {"pfad": pf, "anzahl": int(len(s)), "gruppe": "/".join(rollen),
                                "rolle": "akteur" if ist_akteur else "fels", "sichtweite": sw,
                                "schatten": bool(a["schatten"][s].any()), "kollision": bool(a["koll"][s].any()),
                                "nanite": bool(self.netze[pf]["nanite"]),
                                "klassen": sorted(set(a["klasse"][s].tolist()))}
                if ist_akteur:
                    for k in s:
                        akteure.append({"netz": self.netze[pf]["name"], "pfad": pf, "rolle": "akteur", "klasse": str(a["klasse"][k]),
                                        "x": float(a["x"][k]), "y": float(a["y"][k]), "z": float(a["z"][k]),
                                        "qx": float(a["q"][k, 0]), "qy": float(a["q"][k, 1]), "qz": float(a["q"][k, 2]), "qw": float(a["q"][k, 3]),
                                        "sx": float(a["sx"][k]), "sy": float(a["sy"][k]), "sz": float(a["sz"][k]),
                                        "hoehe_m": round(float(a["hoehe_m"][k]), 2)})
        stat = dict(self.statistik)
        stat["je_rolle"] = {ro: int((a["rolle"] == ro).sum()) for ro in ROLLEN_ORDNUNG}
        stat["kollision"] = int(a["koll"].sum())
        stat["akteure"] = len(akteure)
        plan = {"stand": time.strftime("%Y-%m-%d %H:%M"), "feld": feld, "instanzen": int(n), "ebene": "felsgruppen",
                "dateien": dateien, "akteure": akteure, "entfernen": AU.get("entfernen", ""),
                "ft_ordner": AU["ft_ordner"], "ft_praefix": AU["ft_praefix"], "seed": self.seed, "faktor": self.faktor,
                "statistik": stat, "quelle": "felsgruppen_plan.py (UNGETESTET MIT ECHTDATEN)",
                "hinweis_setzer": "Einträge mit rolle 'akteur' (Dateien akteur_*.f32, Liste 'akteure') als StaticMeshActor setzen, "
                                  "nicht als Foliage; Kollision nur wo kollision=true; Z enthält bereits das Eingraben."}
        with open(os.path.join(out, "plan.json"), "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=1)
        log("geschrieben: %s (%d Dateien, %d Akteure)" % (out, len(dateien), len(akteure)))

    def bild(self, feld, a):
        try:
            from PIL import Image
        except Exception:
            log("Hinweis: Pillow fehlt – kein Bild.")
            return
        AU = self.R["ausgabe"]
        i0, i1, j0, j1 = self.win
        i0f, i1f, j0f, j1f = self.feld_box
        si, sj = i0f - i0, j0f - j0
        H, W = i1f - i0f, j1f - j0f
        n = self.normal[si:si + H, sj:sj + W]
        licht = np.array([-0.5, -0.5, 0.707]); licht /= np.linalg.norm(licht)
        shade = np.clip((n * licht).sum(2), 0, 1) * 0.7 + 0.2
        img = np.stack([shade] * 3, axis=2) * 255
        wz = self.m_wasser_roh[si:si + H, sj:sj + W]
        img[wz] = [40, 80, 180]
        img[~self.land[si:si + H, sj:sj + W]] = [20, 40, 120]
        w = self.m_wand[si:si + H, sj:sj + W]
        img[w] = img[w] * 0.6 + np.array([80, 60, 40]) * 0.4
        img = img.astype(np.uint8)
        if len(a["x"]):
            ci = a["ci"] - si; cj = a["cj"] - sj
            ok = (ci >= 0) & (ci < H) & (cj >= 0) & (cj < W)
            farben = {k: np.array(v["farbe"], dtype=np.uint8) for k, v in self.R["klassen"].items()}
            gross = {"hero": 2, "wand": 2, "band": 1, "block": 1, "platte": 0, "stein": 0, "kiesel": 0}
            for rolle in ["kiesel", "stein", "platte", "block", "band", "wand", "hero"]:
                s = ok & (a["rolle"] == rolle)
                if not s.any():
                    continue
                r = gross[rolle]
                for kl in np.unique(a["klasse"][s]):
                    ss = s & (a["klasse"] == kl)
                    col = farben[kl]
                    if rolle == "kiesel":
                        col = (col.astype(int) * 0.5 + 100).astype(np.uint8)
                    for di in range(-r, r + 1):
                        for dj in range(-r, r + 1):
                            ii = np.clip(ci[ss] + di, 0, H - 1); jj = np.clip(cj[ss] + dj, 0, W - 1)
                            img[ii, jj] = col
        pfad = os.path.join(self.basis, AU["bild"])
        os.makedirs(pfad, exist_ok=True)
        Image.fromarray(img, "RGB").save(os.path.join(pfad, feld + ".png"))
        log("Bild: %s" % os.path.join(pfad, feld + ".png"))


# ----------------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Felsgruppen-Planer Eldarien (Auftrag 11 C). UNGETESTET MIT ECHTDATEN.")
    ap.add_argument("felder", nargs="+", help="Gitterfelder, z. B. B4 C2")
    ap.add_argument("--bild", action="store_true")
    ap.add_argument("--faktor", type=float, default=1.0)
    ap.add_argument("--basis", default=".")
    ap.add_argument("--regeln", default=None)
    args = ap.parse_args()
    skriptdir = os.path.dirname(os.path.abspath(__file__))
    regeln = args.regeln
    if regeln is None:
        for p in [os.path.join(skriptdir, "felsgruppen_regeln.json"), os.path.join(args.basis, "scripts", "felsgruppen", "felsgruppen_regeln.json")]:
            if os.path.isfile(p):
                regeln = p
                break
    if regeln is None or not os.path.isfile(regeln):
        sys.exit("FEHLT (Pflicht): felsgruppen_regeln.json (--regeln PFAD)")
    with open(regeln, encoding="utf-8") as f:
        R = json.load(f)
    log("Regeln: %s (Seed %s), numba: %s" % (regeln, R.get("seed"), "ja" if HAVE_NUMBA else "nein (NumPy-Fallback)"))
    welt_dir = os.path.join(args.basis, "export", "unreal", "welt")
    if not os.path.isdir(welt_dir):
        sys.exit("FEHLT (Pflicht): %s (production-Wurzel mit --basis angeben)" % welt_dir)
    netze = lade_netze(args.basis, skriptdir)
    masse = lade_masse(args.basis, skriptdir)
    pl = Planer(R, netze, masse, args.basis, args.faktor, skriptdir)
    for feld in args.felder:
        try:
            pl.plane_feld(feld.upper(), welt_dir, args.bild)
        except SystemExit:
            raise
        except ValueError as e:
            log("FEHLER: %s – Feld übersprungen." % e)
        except Exception as e:  # klare Meldung, weiter mit nächstem Feld
            import traceback
            traceback.print_exc()
            log("FEHLER in Feld %s: %s" % (feld, e))


if __name__ == "__main__":
    main()
