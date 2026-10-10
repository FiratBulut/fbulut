#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hochgebirge_plan.py – Planer Teil B4 „Gletscher/Frost/Hochgebirge“ (Auftrag 11) für Eldarien (UE 5.8.3, 1-m-Raster 9577 × 7057).

*** UNGETESTET MIT ECHTDATEN *** – in der Cloud nur syntaxgeprüft (py_compile) und mit synthetischen Rastern rauchgetestet
(D2-Fenster: Bergmassiv 0–700 m, Grat, Kar, Gletscherbach). Korrekturen bitte als auftraege/verteilung-hochgebirge-korrektur.md.

Was das Skript tut
------------------
Liest je Gitterfeld ein Fenster (Feld + 64 m Rand) aus hoehe.f32 (np.memmap), berechnet Hang, Normale, Exposition
(Sonnigkeit aus der Südkomponente der Normale), Krümmung (Laplace der Gauß-geglätteten Höhe; negativ = Grat, positiv = Rinne)
und leitet daraus je Zelle die **Höhenstufe** ab:
   0 bergwald   unter Baumgrenze − 60 m
   1 krummholz  Baumgrenze − 60 … + 40 m (Latschen, Krüppelkiefern, windschiefe Einzelbäume, Totholz)
   2 matte      bis Schneegrenze (Zwergstrauchheide/Alpenrosen-Ersatz, Polster, Grasbüschel, Flechtensteine)
   3 fels_schnee über Schneegrenze oder lage_Schnee/Eis hoch (Schutt, Schnee-Sims-Kleinzeug, Eiszapfen)
Baum- und Schneegrenze = Basis je Biom (eigner.r8 + welt.json) + Exposition (Südhang +45 m) − Hang (bis −30 m) − Grat (−40 m)
± Rauschen (320-m-Gitter, ±35 m) + Schlucht-Bonus (+70 m in konkaven Rinnen ≤ 25 m vom Bach → Schluchtwald).
Schichten: 0 boden (Schutt-Kiesel, Flechtensteine, Schneefleck-Platten, Schuttfächer-Platten), 1 mittel (Latsche, Krüppelkiefer,
Alpenrose, Polster, Grasbüschel, Totholz, Wurzelteller, Flechtenblöcke), 2 baum (Bergwald-Kiefer, Krummholz-Baum, Schluchtwald,
Totbaum), 5 wasserkante (Bachblöcke, Moossteine, Bachkiesel, Wasserfall-Sturzblöcke, Eiszapfen). 3 fels / 4 spuren liefern
Teil C/D; biomspezifische Überschreibungen stehen in hochgebirge_regeln.json („felsgruppen_overrides“, „spuren_overrides“).
Nichts auf Wasser/Weg/Ort, Abstand zu Bäumen (bestand/, witcher/, instanzen/) und Felsschalen (felsschalen/plan_<Feld>.json);
Hang > 40° nur Steine/Eiszapfen. Zufall deterministisch: 64-bit-Hash aus (Seed, Klasse, Weltraster-Koordinate, Mitglied).

Aufruf
------
  python -I scripts/hochgebirge/hochgebirge_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
  --basis   production-Wurzel (Default "."), darunter export/unreal/welt/, daten/netze.csv, daten/netze_masse.json, docs/
  --regeln  Regeldatei (Default hochgebirge_regeln.json neben dem Skript)
  --faktor  Dichtefaktor auf alle Klassen
  --bild    Draufsicht docs/pruefung/hochgebirge/<Feld>.png (1 px = 1 m; Grau = Höhenstufe, Farben je Klasse)

Ausgabe (FORMAT.md §3)
----------------------
  export/unreal/welt/hochgebirge/<Feld>/<Netzname>.f32   10 float32 LE je Instanz: x,y,z cm; qx,qy,qz,qw; sx,sy,sz
  export/unreal/welt/hochgebirge/<Feld>/plan.json        stand, feld, instanzen, dateien{pfad, anzahl, gruppe, rolle, sichtweite,
                                                         schatten, kollision, ebene}, entfernen, ft_ordner, ft_praefix, statistik

Quellen: vorlagen/FORMAT.md; antworten/verteilung-hochgebirge.md (Höhenstufen, Dichten, Quellen: Alpenverein „Höhenstufen der
Alpen“, Naturpark Ötztal, Wikipedia Scree, 80.lv „World Building of Witcher 3“); antworten/assets-taxonomie.json (Paletten);
antworten/skripte/felsgruppen_plan.py (Hash-Zufall, Raster-Operatoren – gleiche Konventionen).
Nur NumPy (separierbare Faltungen); numba optional, wird nicht benötigt. Laufzeit-Ziel ≤ 60 s je Feld.
"""
import argparse
import csv
import json
import math
import os
import sys
import time

import numpy as np

np.seterr(over="ignore")  # uint64-Hash darf überlaufen

try:  # optional
    import numba  # noqa: F401
    HAVE_NUMBA = True
except Exception:  # pragma: no cover
    HAVE_NUMBA = False

NX, NY, FELD = 9577, 7057, 1008
X0, Y0 = 4730.5, 4060.5
BIOME = ["aue", "bergwald", "gletscher", "tundra", "canyon", "oedland", "heide", "elfenwald", "dschungel", "kueste", "wueste",
         "lava", "frost", "sumpf", "fjord"]
EBENE_NAME = {0: "boden", 1: "mittel", 2: "baum", 5: "wasserkante"}
U64 = np.uint64
BAUM_WORTE = ("baum", "tree", "pine", "fir", "beech", "birch", "willow", "poplar", "hornbeam", "kiefer", "tanne", "buche", "birke",
              "weide", "pappel", "hainbuche", "palm", "cherry")


def log(*a):
    print("[hochgebirge]", *a, flush=True)


# ----------------------------------------------------------------------------------------------------------------------
# Hash-Zufall
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
    h = None
    for t in teile:
        a = np.atleast_1d(np.asarray(t)).astype(np.int64).astype(U64)
        h = a * U64(0x9E3779B97F4A7C15) if h is None else _mix(h ^ (a + U64(0x9E3779B97F4A7C15)))
    return _mix(h)


def uni(h, salz):
    return (_mix(h ^ U64((salz * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)) >> U64(11)).astype(np.float64) * (1.0 / 9007199254740992.0)


def zwischen(h, salz, lo, hi):
    return lo + (hi - lo) * uni(h, salz)


def ganz(h, salz, lo, hi):
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
    out = np.zeros_like(a, dtype=np.float64)
    n = a.shape[axis]
    for t, w in enumerate(k):
        sl = [slice(None), slice(None)]
        sl[axis] = slice(t, t + n)
        out += w * ap[tuple(sl)]
    return out


def gauss(a, sigma):
    if sigma <= 0:
        return a.astype(np.float64)
    return gauss1d(gauss1d(a.astype(np.float64), sigma, 0), sigma, 1)


def boxmax1d(a, r, axis):
    if r <= 0:
        return a
    pad = [(0, 0), (0, 0)]
    pad[axis] = (r, r)
    ap = np.pad(a, pad, mode="constant", constant_values=False if a.dtype == bool else 0)
    out = a.copy()
    n = a.shape[axis]
    for t in range(2 * r + 1):
        sl = [slice(None), slice(None)]
        sl[axis] = slice(t, t + n)
        out = np.maximum(out, ap[tuple(sl)])
    return out


def dilate(mask, r):
    """Quadratische Dilatation (Tschebyschow-Radius r) einer Boolmaske."""
    r = int(round(r))
    if r <= 0:
        return mask.copy()
    return boxmax1d(boxmax1d(mask, r, 0), r, 1)


def dist_cheb(mask, rmax):
    """Tschebyschow-Abstand (m, 0 … rmax, rmax+1 = weiter) zur Maske, per wiederholter Dilatation (rmax ≤ ~16)."""
    d = np.full(mask.shape, rmax + 1, dtype=np.int16)
    cur = mask.copy()
    d[cur] = 0
    for r in range(1, rmax + 1):
        nxt = boxmax1d(boxmax1d(cur, 1, 0), 1, 1)
        d[nxt & (d > r)] = r
        cur = nxt
    return d


def wertrauschen(ii, jj, gitter, seed, salz):
    """Bilinear interpoliertes Wertrauschen (0..1) auf Weltkoordinaten, Gitterweite gitter m."""
    gi = ii / float(gitter)
    gj = jj / float(gitter)
    i0 = np.floor(gi).astype(np.int64)
    j0 = np.floor(gj).astype(np.int64)
    fi = gi - i0
    fj = gj - j0
    fi = fi * fi * (3 - 2 * fi)
    fj = fj * fj * (3 - 2 * fj)

    def v(di, dj):
        return uni(hash64(seed, salz, i0 + di, j0 + dj), 7)

    return (v(0, 0) * (1 - fi) * (1 - fj) + v(0, 1) * (1 - fi) * fj + v(1, 0) * fi * (1 - fj) + v(1, 1) * fi * fj)


# ----------------------------------------------------------------------------------------------------------------------
# Laden
# ----------------------------------------------------------------------------------------------------------------------
def feld_bereich(name):
    name = name.strip().upper()
    if len(name) < 2 or not name[0].isalpha() or not name[1:].isdigit():
        raise ValueError("Feldname wie 'D2' erwartet, nicht %r" % name)
    s = ord(name[0]) - 65
    r = int(name[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise ValueError("Feld %s außerhalb A1…J7" % name)
    j0, i0 = s * FELD, (r - 1) * FELD
    return i0, min(i0 + FELD, NY), j0, min(j0 + FELD, NX)


def lade_raster(pfad, dtype, win, pflicht=False, name=""):
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
    a = np.array(mm[i0:i1, j0:j1])
    del mm
    return a


def lade_netze(basis, skriptdir):
    kandidaten = [os.path.join(basis, "daten", "netze.csv"), os.path.join(skriptdir, "netze.csv"),
                  os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "netze.csv")]
    for p in kandidaten:
        if os.path.isfile(p):
            netze = {}
            with open(p, encoding="utf-8", newline="") as f:
                for z in csv.DictReader(f, delimiter=";"):
                    try:
                        netze[z["pfad"]] = {"name": z["name"], "hoehe_m": float(z.get("groesse_z_m") or 0),
                                            "x_m": float(z.get("groesse_x_m") or 0), "y_m": float(z.get("groesse_y_m") or 0),
                                            "nanite": z.get("nanite") == "1", "kollision_prim": int(z.get("kollision_primitive") or 0)}
                    except (KeyError, ValueError):
                        continue
            log("Inventar: %d Netze aus %s" % (len(netze), p))
            return netze
    sys.exit("FEHLT (Pflicht): daten/netze.csv (gesucht: %s)" % ", ".join(kandidaten))


def lade_masse(basis, skriptdir):
    for p in (os.path.join(basis, "daten", "netze_masse.json"), os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "netze_masse.json")):
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:  # pragma: no cover
                log("Hinweis: netze_masse.json nicht lesbar (%s)" % e)
    log("Hinweis: daten/netze_masse.json fehlt – Pivot = Bodenmitte angenommen.")
    return {}


def min_z_m(masse, pfad, name):
    """min_z (m) aus netze_masse.json, falls vorhanden (Schlüssel Pfad oder Name; Felder min/max in cm)."""
    e = masse.get(pfad) or masse.get(name)
    if not isinstance(e, dict):
        return None
    for k in ("min", "min_cm", "bounds_min"):
        v = e.get(k)
        if isinstance(v, (list, tuple)) and len(v) >= 3:
            try:
                return float(v[2]) / 100.0
            except (TypeError, ValueError):
                return None
    if "min_z_cm" in e:
        try:
            return float(e["min_z_cm"]) / 100.0
        except (TypeError, ValueError):
            return None
    return None


def dominantes_biom(basis, skriptdir, feld):
    for p in (os.path.join(basis, "daten", "biome_je_feld.json"), os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "biome_je_feld.json")):
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                e = d.get("felder", d).get(feld)
                if e and e.get("biome_prozent"):
                    return e["biome_prozent"][0][0], e
            except Exception as ex:  # pragma: no cover
                log("Hinweis: biome_je_feld.json nicht auswertbar (%s)" % ex)
    return None, None


def lade_biome(welt_dir, win, basis, skriptdir, feld, regeln, hang, hoehe):
    eig = lade_raster(os.path.join(welt_dir, "eigner.r8"), np.uint8, win, name="eigner.r8")
    E0 = regeln.get("eigner0", {})
    dom, _ = dominantes_biom(basis, skriptdir, feld)
    b0 = BIOME.index(dom) if dom in BIOME else 0
    form = (win[1] - win[0], win[3] - win[2])
    fb = BIOME.index(E0.get("fallback_biom", "gletscher"))
    tab = np.full(256, b0, dtype=np.int16)
    wj = os.path.join(welt_dir, "welt.json")
    if eig is None or not os.path.isfile(wj):
        if eig is not None:
            log("Hinweis: welt.json fehlt – Biom überall '%s'." % BIOME[b0])
        out = np.full(form, b0, dtype=np.int16)
        if dom is None:
            out[(hang >= E0.get("fallback_hang_grad", 25)) | (hoehe >= E0.get("fallback_hoehe_m", 220))] = fb
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
        rez = str(v.get("rezept", v.get("biom", "")) if isinstance(v, dict) else v).lower()
        if k == 0 or rez in ("", "0", "welt", "weltgelaende", "weltgelände"):
            tab[k] = b0
            continue
        b = None
        for i, bn in enumerate(BIOME):
            if bn in rez:
                b = i
                break
        if b is None:
            if "vulkan" in rez or "lava" in rez:
                b = BIOME.index("lava")
            elif "glet" in rez or "eis" in rez or "schnee" in rez:
                b = BIOME.index("gletscher")
            elif "wald" in rez:
                b = BIOME.index("bergwald")
            else:
                unbekannt.add(rez)
                b = 0
        tab[k] = b
    if unbekannt:
        log("Hinweis: unbekannte Rezepte in welt.json → aue: %s" % ", ".join(sorted(unbekannt))[:300])
    out = tab[eig]
    if dom is None:
        steil = (eig == 0) & ((hang >= E0.get("fallback_hang_grad", 25)) | (hoehe >= E0.get("fallback_hoehe_m", 220)))
        out[steil] = fb
        log("Hinweis: biome_je_feld.json fehlt – Weltgelände (0) = aue, steile/hohe Zellen = %s" % BIOME[fb])
    anteile = ", ".join("%s %.0f%%" % (BIOME[i], 100 * (out == i).mean()) for i in np.unique(out))
    log("Biome: Kennzahl 0 → %s; Anteile im Fenster: %s" % (BIOME[b0], anteile))
    return out


def lade_positionen_f32(ordner, nur_baeume=None):
    """Alle *.f32 im Ordner → (x_cm, y_cm). nur_baeume: plan.json-Rollen auswerten (True = nur Bäume)."""
    xs, ys = [], []
    if not os.path.isdir(ordner):
        return None
    rollen = {}
    pj = os.path.join(ordner, "plan.json")
    if os.path.isfile(pj):
        try:
            with open(pj, encoding="utf-8") as f:
                for nm, info in json.load(f).get("dateien", {}).items():
                    rollen[nm] = (str(info.get("rolle", "")) + " " + str(info.get("gruppe", "")) + " " + nm).lower()
        except Exception:
            pass
    for fn in sorted(os.listdir(ordner)):
        if not fn.lower().endswith(".f32"):
            continue
        nm = fn[:-4]
        if nur_baeume:
            txt = rollen.get(nm, nm.lower())
            if not any(w in txt for w in BAUM_WORTE) or "stump" in txt or "log" in txt or "dead" in txt or "tot" in txt:
                continue
        a = np.fromfile(os.path.join(ordner, fn), dtype="<f4")
        if a.size and a.size % 10 == 0:
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
    i0, i1, j0, j1 = win
    m = np.zeros((i1 - i0, j1 - j0), dtype=bool)
    if pos is None or radius is None:
        return m
    x, y = pos
    j = np.round(x / 100.0 + X0).astype(np.int64) - j0
    i = np.round(y / 100.0 + Y0).astype(np.int64) - i0
    ok = (i >= 0) & (i < m.shape[0]) & (j >= 0) & (j < m.shape[1])
    m[i[ok], j[ok]] = True
    return dilate(m, int(round(radius)))


def lade_baeume(basis, welt_dir, feld, win):
    """Baumpositionen (cm) aus bestand/, witcher/ (Feld + 8 Nachbarn) und instanzen/instanzen.json."""
    s = ord(feld[0]) - 65
    r = int(feld[1:])
    xs, ys, quellen = [], [], []
    for ds in (-1, 0, 1):
        for dr in (-1, 0, 1):
            ss, rr = s + ds, r + dr
            if not (0 <= ss <= 9 and 1 <= rr <= 7):
                continue
            nf = chr(65 + ss) + str(rr)
            for ebene in ("bestand", "witcher"):
                p = lade_positionen_f32(os.path.join(welt_dir, ebene, nf), nur_baeume=True)
                if p is not None:
                    xs.append(p[0])
                    ys.append(p[1])
                    quellen.append("%s/%s" % (ebene, nf))
    ij = os.path.join(welt_dir, "instanzen", "instanzen.json")
    if os.path.isfile(ij):
        try:
            with open(ij, encoding="utf-8") as f:
                inst = json.load(f)
            n = 0
            for e in inst.get("verzeichnis", []):
                txt = (str(e.get("klasse", "")) + " " + str(e.get("name", "")) + " " + str(e.get("ref", ""))).lower()
                if not any(w in txt for w in BAUM_WORTE):
                    continue
                fdat = e.get("datei") or (str(e.get("name", "")) + ".f32")
                fdat = os.path.join(welt_dir, "instanzen", fdat)
                if not os.path.isfile(fdat):
                    continue
                a = np.fromfile(fdat, dtype="<f4")
                if a.size and a.size % 10 == 0:
                    a = a.reshape(-1, 10)
                    xs.append(a[:, 0])
                    ys.append(a[:, 1])
                    n += 1
            if n:
                quellen.append("instanzen/%d Dateien" % n)
            elif not quellen:
                log("Hinweis: instanzen.json ohne auswertbare Baum-Dateien (Positionen nur über <name>.f32 neben der JSON).")
        except Exception as e:
            log("Hinweis: instanzen.json nicht auswertbar (%s)" % e)
    else:
        log("Hinweis: instanzen/instanzen.json fehlt – kein Houdini-Bestand als Abstand.")
    if not xs:
        log("Hinweis: keine Baum-Ebene gefunden (bestand/, witcher/, instanzen/) – kein Baumabstand geprüft.")
        return None
    log("Baum-Ebenen: %s" % ", ".join(quellen))
    return np.concatenate(xs), np.concatenate(ys)


def lade_felsschalen(welt_dir, feld):
    p = os.path.join(welt_dir, "felsschalen", "plan_%s.json" % feld)
    if not os.path.isfile(p):
        log("Hinweis: felsschalen/plan_%s.json fehlt – kein Abstand zu Felsschalen geprüft." % feld)
        return None
    try:
        with open(p, encoding="utf-8") as f:
            obj = json.load(f)
    except Exception as e:
        log("Hinweis: felsschalen/plan_%s.json nicht lesbar (%s)" % (feld, e))
        return None
    out = []
    positionen_aus_json(obj, out)
    if not out:
        log("Hinweis: felsschalen/plan_%s.json ohne erkennbare Positionen (x/y) – keine Sperre." % feld)
        return None
    a = np.array(out, dtype=np.float64)
    return a[:, 0], a[:, 1]


# ----------------------------------------------------------------------------------------------------------------------
# Geometrie
# ----------------------------------------------------------------------------------------------------------------------
def bilinear(h, fi, fj):
    i = np.clip(np.floor(fi).astype(np.int64), 0, h.shape[0] - 2)
    j = np.clip(np.floor(fj).astype(np.int64), 0, h.shape[1] - 2)
    di = np.clip(fi - i, 0, 1)
    dj = np.clip(fj - j, 0, 1)
    return ((h[i, j] * (1 - dj) + h[i, j + 1] * dj) * (1 - di) + (h[i + 1, j] * (1 - dj) + h[i + 1, j + 1] * dj) * di)


def quat_aus_yaw_up(yaw, up):
    """Quaternion (x,y,z,w): erst Yaw um Z, dann Z-Achse auf 'up' (Unreal-Welt: X = +j, Y = +i, Z hoch) kippen."""
    n = yaw.shape[0]
    ux, uy, uz = up[:, 0], up[:, 1], up[:, 2]
    # kürzeste Drehung von (0,0,1) nach up: Achse = (0,0,1) × up = (-uy, ux, 0), Winkel = acos(uz)
    ang = np.arccos(np.clip(uz, -1, 1))
    ax = np.stack([-uy, ux, np.zeros(n)], axis=1)
    nrm = np.linalg.norm(ax, axis=1)
    ok = nrm > 1e-9
    ax[ok] /= nrm[ok, None]
    s = np.sin(ang / 2)
    qt = np.stack([ax[:, 0] * s, ax[:, 1] * s, ax[:, 2] * s, np.cos(ang / 2)], axis=1)
    qt[~ok] = [0, 0, 0, 1]
    qy = np.stack([np.zeros(n), np.zeros(n), np.sin(yaw / 2), np.cos(yaw / 2)], axis=1)
    # q = qt * qy
    x1, y1, z1, w1 = qt[:, 0], qt[:, 1], qt[:, 2], qt[:, 3]
    x2, y2, z2, w2 = qy[:, 0], qy[:, 1], qy[:, 2], qy[:, 3]
    return np.stack([w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                     w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
                     w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2], axis=1)


# ----------------------------------------------------------------------------------------------------------------------
# Gelände-Analyse
# ----------------------------------------------------------------------------------------------------------------------
def analyse(h, win, regeln):
    G = regeln.get("glaettung", {})
    hs = gauss(h, G.get("hang_sigma_m", 1.5))
    gi, gj = np.gradient(hs)  # dh/di (Süd), dh/dj (Ost), Zelle = 1 m
    hang = np.degrees(np.arctan(np.hypot(gi, gj)))
    nrm = np.stack([-gj, -gi, np.ones_like(hs)], axis=-1)  # Unreal: X=+j, Y=+i
    nrm /= np.linalg.norm(nrm, axis=-1)[..., None]
    g = np.hypot(gi, gj) + 1e-9
    sued = -gi / g  # Hang zeigt nach Süden (+i), wenn Höhe mit i fällt
    voll = regeln.get("exposition", {}).get("hang_voll_grad", 15)
    sonnig = 0.5 + 0.5 * sued * np.minimum(1.0, hang / float(voll))  # 0 = Nord, 1 = Süd, 0,5 = eben
    hk = gauss(h, G.get("kruemmung_sigma_m", 8.0))
    gki, gkj = np.gradient(hk)
    lap = np.gradient(gki)[0] + np.gradient(gkj)[1]  # Laplace: < 0 Grat/Kuppe, > 0 Rinne/Mulde
    hg = gauss(h, G.get("grat_sigma_m", 6.0))
    gi2, gj2 = np.gradient(hg)
    lap_g = np.gradient(gi2)[0] + np.gradient(gj2)[1]
    return hs, hang, nrm, sonnig, lap, lap_g


def hoehenstufen(h, hang, sonnig, lap, lap_g, biom, wasser, win, regeln):
    HS = regeln["hoehenstufen"]
    seed = int(regeln.get("seed", 1))
    i0, j0 = win[0], win[2]
    ii, jj = np.meshgrid(np.arange(win[0], win[1]), np.arange(win[2], win[3]), indexing="ij")
    bg = np.full(h.shape, float(HS["baumgrenze_m"].get("default", 320)))
    sg = np.full(h.shape, float(HS["schneegrenze_m"].get("default", 450)))
    for bi, bn in enumerate(BIOME):
        m = biom == bi
        if m.any():
            bg[m] = HS["baumgrenze_m"].get(bn, HS["baumgrenze_m"].get("default", 320))
            sg[m] = HS["schneegrenze_m"].get(bn, HS["schneegrenze_m"].get("default", 450))
    v = np.zeros_like(h, dtype=np.float64)
    v += (sonnig - 0.5) * 2.0 * HS.get("exposition_versatz_m", 45)
    HV = HS.get("hang_versatz", {})
    t = np.clip((hang - HV.get("ab_grad", 25)) / max(1e-6, HV.get("bis_grad", 45) - HV.get("ab_grad", 25)), 0, 1)
    v -= t * HV.get("versatz_m", 30)
    grat = np.clip(-lap_g / max(1e-9, HS.get("grat_staerke_min", 0.015)), 0, 1)
    v -= grat * HS.get("grat_versatz_m", 40)
    rausch = wertrauschen(ii, jj, regeln.get("glaettung", {}).get("rauschen_gitter_m", 320), seed, 11)
    v += (rausch - 0.5) * 2.0 * HS.get("rauschen_amplitude_m", 35)
    S = HS.get("schlucht", {})
    nah_wasser = dilate(wasser, S.get("wasser_m", 25)) if wasser is not None else np.zeros(h.shape, bool)
    schlucht = nah_wasser & (lap > S.get("kruemmung_min", 0.006)) & (hang >= 8)
    schlucht = dilate(schlucht, 6) & nah_wasser  # etwas verbreitern, bleibt bachnah
    v_bg = v + schlucht * S.get("bonus_m", 70)
    bg = bg + v_bg
    sg = sg + v
    kb = HS.get("krummholz_band_m", [-60, 40])
    stufe = np.zeros(h.shape, dtype=np.int8)
    stufe[h >= bg + kb[0]] = 1
    stufe[h >= bg + kb[1]] = 2
    stufe[h >= sg] = 3
    return stufe, bg, sg, schlucht, grat


# ----------------------------------------------------------------------------------------------------------------------
# Klassen-Planung
# ----------------------------------------------------------------------------------------------------------------------
def plane_klasse(name, K, ctx, faktor):
    """Liefert dict mit Arrays (fi, fj, netz_idx, h) der Mitglieder im Fenster (noch ohne Feld-Beschnitt)."""
    R = ctx["regeln"]
    seed = int(R.get("seed", 1)) + 1000 * ctx["klassen_index"][name]
    win = ctx["win"]
    form = ctx["form"]
    stufe = ctx["stufe"]
    hang = ctx["hang"]
    stf = np.array(K.get("stufen", [1, 1, 1, 1]), dtype=np.float64)
    p = np.full(form, float(K["dichte_je_m2"]) * faktor, dtype=np.float64)
    p *= stf[np.clip(stufe, 0, 3)]
    p *= ctx["biomf"]
    # Nicht-Kernbiome nur ab Stufe
    p[(~ctx["kern"]) & (stufe < R.get("nicht_kern_nur_ab_stufe", 1))] = 0
    # Lagen
    lf = np.ones(form)
    for ln, w in K.get("lagen", {}).items():
        cov = ctx["lagen"].get(ln)
        if cov is not None:
            lf += cov * (float(w) - 1.0)
    p *= np.clip(lf, 0.0, 3.0)
    # Hang
    hv, hn = K.get("hang", [30, 40])
    hf = np.clip(1.0 - (hang - hv) / max(1e-6, hn - hv), 0, 1)
    if "hang_min_grad" in K:
        hf *= (hang >= K["hang_min_grad"])
    p *= hf
    # Exposition
    en, es = K.get("exposition", [1.0, 1.0])
    p *= en + (es - en) * ctx["sonnig"]
    # Lagebedingungen
    if K.get("wasser_band_m"):
        lo, hi = K["wasser_band_m"]
        dw = ctx["dist_wasser"]
        p *= (dw >= max(1, lo)) & (dw <= hi)
    if K.get("nur_schlucht"):
        p *= ctx["schlucht"]
    if K.get("nur_wasserfall_fuss"):
        p *= ctx["wasserfall_fuss"]
    if K.get("nur_eiswand"):
        p *= ctx["eiswand"]
    # Ausschluss
    ebene = int(K.get("ebene", 1))
    p *= ~ctx["sperre"][ebene]
    p *= ~(ctx["weg_gross"] if K.get("weg", "klein") == "gross" else ctx["weg_klein"])
    if K.get("rolle") in ("kiesel", "stein", "block", "platte", "hero"):
        p *= hang <= R["ausschluss"].get("hang_max_stein_grad", 55)
    elif K.get("rolle") != "eis":
        p *= hang <= R["ausschluss"].get("hang_max_pflanze_grad", 40)
    # Saat
    G = K.get("gruppe", {"n": [1, 1], "radius_m": 1.0})
    nlo, nhi = int(G["n"][0]), int(G["n"][1])
    nmean = 0.5 * (nlo + nhi)
    psaat = np.clip(p / nmean, 0, 1)
    ii, jj = np.nonzero(psaat > 0)
    if ii.size == 0:
        return None
    I = ii + win[0]
    J = jj + win[2]
    hs = hash64(seed, I, J)
    sel = uni(hs, 1) < psaat[ii, jj]
    ii, jj, I, J, hs = ii[sel], jj[sel], I[sel], J[sel], hs[sel]
    S = ii.size
    if S == 0:
        return None
    n = ganz(hs, 2, nlo, nhi)
    rep = np.repeat(np.arange(S), n)
    k = np.arange(rep.size) - np.repeat(np.cumsum(n) - n, n)
    hm = hash64(seed, I[rep], J[rep], k + 1)
    ang = uni(hm, 3) * 2 * np.pi
    rad = float(G.get("radius_m", 1.0)) * np.sqrt(uni(hm, 4))
    rad[k == 0] = 0.0
    fi = ii[rep] + 0.5 + rad * np.sin(ang) + (uni(hm, 5) - 0.5) * 0.8
    fj = jj[rep] + 0.5 + rad * np.cos(ang) + (uni(hm, 6) - 0.5) * 0.8
    ok = (fi >= 1) & (fi < form[0] - 2) & (fj >= 1) & (fj < form[1] - 2)
    fi, fj, hm = fi[ok], fj[ok], hm[ok]
    ci = np.clip(np.round(fi).astype(np.int64), 0, form[0] - 1)
    cj = np.clip(np.round(fj).astype(np.int64), 0, form[1] - 1)
    # Mitglieder prüfen: Zielzelle muss gültig sein (p > 0) – damit Gruppen nicht auf Wasser/Weg laufen
    ok = p[ci, cj] > 0
    fi, fj, hm, ci, cj = fi[ok], fj[ok], hm[ok], ci[ok], cj[ok]
    if fi.size == 0:
        return None
    # Netzwahl mit Gewichten
    gew = np.array(K.get("gewichte", [1] * len(K["netze"])), dtype=np.float64)
    gew = gew[: len(K["netze"])]
    cdf = np.cumsum(gew) / gew.sum()
    nidx = np.minimum(np.searchsorted(cdf, uni(hm, 7)), len(K["netze"]) - 1)
    return {"fi": fi, "fj": fj, "ci": ci, "cj": cj, "h": hm, "netz": nidx}


def instanzen_bauen(name, K, M, ctx):
    """Positionen/Rotation/Maßstab (Arrays N×10) + Zusatzinfos je Instanz."""
    R = ctx["regeln"]
    win = ctx["win"]
    h = ctx["h"]
    nrm = ctx["nrm"]
    hm = M["h"]
    N = hm.size
    fi, fj, ci, cj = M["fi"], M["fj"], M["ci"], M["cj"]
    z0 = bilinear(h, fi, fj)
    # Maßstab
    s_lo, s_hi = K.get("massstab", [0.9, 1.1])
    s = zwischen(hm, 20, s_lo, s_hi)
    nu = float(K.get("nicht_uniform", 0.0))
    sx = s * (1 + (uni(hm, 21) - 0.5) * 2 * nu)
    sy = s * (1 + (uni(hm, 22) - 0.5) * 2 * nu)
    sz = s.copy()
    if K.get("z_stauchung"):
        zl, zh = K["z_stauchung"]
        sz = s * zwischen(hm, 23, zl, zh)
    # Rotation
    up = nrm[ci, cj].copy()
    kipp = float(K.get("kippen", 1.0))
    up = np.array([0, 0, 1.0])[None, :] * (1 - kipp) + up * kipp
    yaw_mode = K.get("yaw", "zufall")
    E = R.get("exposition", {})
    if yaw_mode == "zufall":
        yaw = uni(hm, 24) * 2 * np.pi
    elif yaw_mode == "hangab":
        # hangabwärts: Richtung −grad = (nrm_x, nrm_y) in Unreal-XY
        yaw = np.arctan2(up[:, 1], up[:, 0]) + np.radians((uni(hm, 24) - 0.5) * 2 * K.get("yaw_streuung_grad", 25))
    else:  # wind
        wr = math.radians(E.get("wind_richtung_grad", 90))
        yaw = wr + np.radians((uni(hm, 24) - 0.5) * 2 * E.get("wind_streuung_grad", 18))
        klo, khi = E.get("wind_kippen_grad", [6, 18])
        kg = np.radians(zwischen(hm, 25, klo, khi)) * kipp / max(kipp, 1e-6) * (1 if kipp > 0 else 0)
        up = np.array([0, 0, 1.0])[None, :] * (1 - kipp * 0.5) + nrm[ci, cj] * (kipp * 0.5)
        up = up + np.stack([np.cos(wr) * np.sin(kg), np.sin(wr) * np.sin(kg), np.zeros(N)], axis=1)
    up /= np.linalg.norm(up, axis=1)[:, None]
    q = quat_aus_yaw_up(yaw, up)
    # Eingraben / z
    hoehe = np.array([ctx["netze"].get(p, {}).get("hoehe_m", 0.5) for p in K["netze"]])[M["netz"]]
    minz = np.array([ctx["minz"].get(p, 0.0) for p in K["netze"]])[M["netz"]]
    z = z0.copy()
    if "eingraben_anteil" in K:
        z -= hoehe * sz * float(K["eingraben_anteil"])
    else:
        z -= float(K.get("eingraben_cm", 3)) / 100.0
    z -= minz * sz  # Netze mit Pivot über dem Fuß (min_z < 0) nicht schweben lassen
    if K.get("z_versatz_anteil"):
        z = z0 + hoehe * sz * float(K["z_versatz_anteil"])
    x_cm = (fj + win[2] - X0) * 100.0
    y_cm = (fi + win[0] - Y0) * 100.0
    out = np.stack([x_cm, y_cm, z * 100.0, q[:, 0], q[:, 1], q[:, 2], q[:, 3], sx, sy, sz], axis=1).astype("<f4")
    return out


# ----------------------------------------------------------------------------------------------------------------------
# Bild
# ----------------------------------------------------------------------------------------------------------------------
def bild_schreiben(pfad, ctx, ergebnisse, feld, rand):
    try:
        from PIL import Image, ImageDraw
    except Exception:
        log("Hinweis: Pillow fehlt – kein Bild.")
        return
    F = ctx["regeln"].get("bild_farben", {})
    i0, i1, j0, j1 = ctx["feld_in_win"]
    stufe = ctx["stufe"][i0:i1, j0:j1]
    hs = ctx["hs"][i0:i1, j0:j1]
    gi, gj = np.gradient(hs)
    shade = np.clip(0.75 + 0.25 * (-gj - gi) / (np.hypot(gi, gj) + 0.5), 0.5, 1.0)
    farben = np.array(F.get("stufe", [[70, 95, 60], [110, 120, 80], [150, 150, 140], [225, 230, 240]]), dtype=np.float64)
    img = farben[np.clip(stufe, 0, 3)] * shade[..., None]
    sch = ctx["schlucht"][i0:i1, j0:j1]
    img[sch] = img[sch] * 0.5 + np.array(F.get("schlucht", [60, 110, 90])) * 0.5
    wf = ctx["wasserfall_fuss"][i0:i1, j0:j1]
    img[wf] = F.get("wasserfall_fuss", [0, 200, 255])
    for nm, key in (("wasser", "wasser"), ("weg", "weg"), ("ort", "ort")):
        m = ctx.get("masken", {}).get(nm)
        if m is not None:
            img[m[i0:i1, j0:j1]] = F.get(key, [0, 0, 0])
    img = img.astype(np.uint8)
    for name, arr in ergebnisse:
        if arr is None or arr.shape[0] == 0:
            continue
        c = F.get(name, [255, 0, 255])
        jj = np.round(arr[:, 0] / 100.0 + X0).astype(np.int64) - (ctx["win"][2] + j0)
        ii = np.round(arr[:, 1] / 100.0 + Y0).astype(np.int64) - (ctx["win"][0] + i0)
        ok = (ii >= 0) & (ii < img.shape[0]) & (jj >= 0) & (jj < img.shape[1])
        img[ii[ok], jj[ok]] = c
    im = Image.fromarray(img, "RGB")
    try:
        d = ImageDraw.Draw(im)
        y = 4
        d.text((4, y), "%s hochgebirge: Grau=Höhenstufe 0..3 (dunkel→hell), blau=Wasser, cyan=Wasserfallfuß" % feld, fill=(255, 255, 0))
        for name, arr in ergebnisse:
            if arr is None or arr.shape[0] == 0:
                continue
            y += 11
            d.rectangle([4, y + 2, 12, y + 10], fill=tuple(F.get(name, [255, 0, 255])))
            d.text((16, y), "%s %d" % (name, arr.shape[0]), fill=(255, 255, 0))
    except Exception:
        pass
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    im.save(pfad)
    log("Bild: %s" % pfad)


# ----------------------------------------------------------------------------------------------------------------------
# Hauptplanung je Feld
# ----------------------------------------------------------------------------------------------------------------------
def plane_feld(feld, basis, regeln, netze, masse, faktor, bild, skriptdir):
    t0 = time.time()
    feld = feld.strip().upper()
    rand = int(regeln.get("fenster_rand_m", 64))
    fi0, fi1, fj0, fj1 = feld_bereich(feld)
    win = (max(0, fi0 - rand), min(NY, fi1 + rand), max(0, fj0 - rand), min(NX, fj1 + rand))
    form = (win[1] - win[0], win[3] - win[2])
    welt_dir = os.path.join(basis, "export", "unreal", "welt")
    log("Feld %s: Fenster i %d–%d, j %d–%d (%d × %d)" % (feld, win[0], win[1], win[2], win[3], form[0], form[1]))
    h = lade_raster(os.path.join(welt_dir, "hoehe.f32"), "<f4", win, pflicht=True, name="hoehe.f32").astype(np.float64)
    hs, hang, nrm, sonnig, lap, lap_g = analyse(h, win, regeln)
    biom = lade_biome(welt_dir, win, basis, skriptdir, feld, regeln, hang, h)

    def r8(nm):
        a = lade_raster(os.path.join(welt_dir, nm), np.uint8, win, name=nm)
        return a
    wasser = r8("karte_wasser.r8")
    weg = r8("karte_weg.r8")
    ort = r8("karte_ort.r8")
    wasser_m = (wasser > 0) if wasser is not None else np.zeros(form, bool)
    weg_m = (weg > 0) if weg is not None else np.zeros(form, bool)
    ort_m = (ort > 0) if ort is not None else np.zeros(form, bool)
    # Lagen
    lagen_namen = set()
    for K in regeln["klassen"].values():
        lagen_namen.update(K.get("lagen", {}).keys())
    lagen = {}
    for ln in sorted(lagen_namen):
        p = os.path.join(welt_dir, "lage_%s.r8" % ln)
        if os.path.isfile(p):
            a = lade_raster(p, np.uint8, win, name="lage_%s.r8" % ln)
            if a is not None:
                lagen[ln] = a.astype(np.float32) / 255.0
    log("Lagen gefunden: %s" % (", ".join(sorted(lagen)) or "keine (Faktor 1)"))
    HS = regeln["hoehenstufen"]
    stufe, bg, sg, schlucht, grat = hoehenstufen(h, hang, sonnig, lap, lap_g, biom, wasser_m, win, regeln)
    if "Schnee" in lagen:
        stufe[lagen["Schnee"] >= HS.get("lage_schnee_als_stufe3_ab", 0.55)] = 3
    if "Eis" in lagen:
        stufe[lagen["Eis"] >= HS.get("lage_eis_als_stufe3_ab", 0.4)] = 3
    stufe[wasser_m] = -1
    # Wasser-Ableitungen
    W = regeln.get("wasser", {})
    dist_wasser = dist_cheb(wasser_m, 16)
    steil_wasser = wasser_m & (hang >= W.get("steil_grad", 18))
    wasserfall_fuss = dilate(steil_wasser, W.get("fuss_radius_m", 10)) & ~wasser_m & (hang < W.get("fuss_hang_max_grad", 25))
    eiswand = (hang >= regeln["klassen"].get("eiszapfen", {}).get("hang_min_grad", 55)) & ((stufe >= 2) | dilate(steil_wasser, 3))
    # Biomfaktor
    BF = regeln.get("biom_faktor", {})
    biomf = np.zeros(form)
    kern = np.zeros(form, bool)
    for bi, bn in enumerate(BIOME):
        m = biom == bi
        if m.any():
            biomf[m] = float(BF.get(bn, 0.0))
            if bn in regeln.get("kern_biome", ["gletscher", "frost"]):
                kern[m] = True
    # Sperren
    A = regeln["ausschluss"]
    baeume = lade_baeume(basis, welt_dir, feld, win)
    schalen = lade_felsschalen(welt_dir, feld)
    basis_sperre = wasser_m | dilate(ort_m, A.get("ort_m", 5))
    weg_klein = dilate(weg_m, A.get("weg_klein_m", 2.5))
    weg_gross = dilate(weg_m, A.get("weg_gross_m", 4.0))
    sperre = {}
    for eb, en in EBENE_NAME.items():
        s = basis_sperre.copy()
        rb = A.get("baum_abstand_m", {}).get(en, 0)
        rs = A.get("felsschale_m", {}).get(en, 0)
        if baeume is not None and rb > 0:
            s |= sperrmaske(win, baeume, rb)
        if schalen is not None and rs > 0:
            s |= sperrmaske(win, schalen, rs)
        sperre[eb] = s
    anteil = lambda m: 100.0 * m.mean()
    log("Höhenstufen im Fenster: bergwald %.0f%%, krummholz %.0f%%, matte %.0f%%, fels/schnee %.0f%%, Wasser %.1f%%; Schlucht %.1f%%, Wasserfallfuß %.2f%%, Eiswand %.2f%%" % (
        anteil(stufe == 0), anteil(stufe == 1), anteil(stufe == 2), anteil(stufe == 3), anteil(stufe < 0), anteil(schlucht), anteil(wasserfall_fuss), anteil(eiswand)))
    log("Baumgrenze Fenster: %.0f–%.0f m (Mittel %.0f), Schneegrenze %.0f–%.0f m; Höhe %.0f–%.0f m; aktive Biomfläche %.0f%%" % (
        bg.min(), bg.max(), bg.mean(), sg.min(), sg.max(), h.min(), h.max(), anteil(biomf > 0)))
    minz = {}
    for K in regeln["klassen"].values():
        for p in K["netze"]:
            mz = min_z_m(masse, p, netze.get(p, {}).get("name", ""))
            if mz is not None and mz < -0.01:
                minz[p] = mz
    ctx = {"regeln": regeln, "win": win, "form": form, "h": h, "hs": hs, "hang": hang, "nrm": nrm, "sonnig": sonnig, "stufe": stufe,
           "schlucht": schlucht, "wasserfall_fuss": wasserfall_fuss, "eiswand": eiswand, "dist_wasser": dist_wasser, "lagen": lagen,
           "biomf": biomf, "kern": kern, "sperre": sperre, "weg_klein": weg_klein, "weg_gross": weg_gross, "netze": netze, "minz": minz,
           "klassen_index": {k: i for i, k in enumerate(regeln["klassen"])}, "masken": {"wasser": wasser_m, "weg": weg_m, "ort": ort_m},
           "feld_in_win": (fi0 - win[0], fi1 - win[0], fj0 - win[2], fj1 - win[2])}
    # Klassen planen
    ergebnisse = {}
    for name, K in regeln["klassen"].items():
        M = plane_klasse(name, K, ctx, faktor)
        if M is None:
            ergebnisse[name] = (np.zeros((0, 10), "<f4"), np.zeros(0, np.int64), np.zeros(0, U64))
            continue
        arr = instanzen_bauen(name, K, M, ctx)
        # Feld-Beschnitt (Rand nur für Nahtlosigkeit)
        im = M["fi"] + win[0]
        jm = M["fj"] + win[2]
        inner = (im >= fi0) & (im < fi1) & (jm >= fj0) & (jm < fj1)
        arr, nidx, hm = arr[inner], M["netz"][inner], M["h"][inner]
        # Klassen-Budget: deterministisch per Hash ausdünnen
        b = int(K.get("budget", 10 ** 9) * max(faktor, 1e-6) ** 0)  # Budget bleibt fix
        if arr.shape[0] > b:
            keep = np.argsort(uni(hm, 30))[:b]
            arr, nidx, hm = arr[keep], nidx[keep], hm[keep]
        ergebnisse[name] = (arr, nidx, hm)
    # Gesamt- und Kollisionsbudget
    B = regeln["budget"]
    prio = [k for k in B.get("prioritaet", []) if k in ergebnisse] + [k for k in ergebnisse if k not in B.get("prioritaet", [])]
    koll_ab = float(B.get("kollision_ab_hoehe_m", 0.8))

    def hat_kollision(name, nidx):
        K = regeln["klassen"][name]
        if not K.get("kollision", False):
            return np.zeros(nidx.size, bool)
        hoe = np.array([netze.get(p, {}).get("hoehe_m", 0.0) for p in K["netze"]])
        return hoe[nidx] >= koll_ab
    gesamt = sum(v[0].shape[0] for v in ergebnisse.values())
    ziel = int(B.get("ziel_instanzen_je_feld", B.get("instanzen_je_feld", 60000)))
    for name in reversed(prio):
        if gesamt <= ziel:
            break
        arr, nidx, hm = ergebnisse[name]
        n = arr.shape[0]
        if n == 0:
            continue
        ueber = gesamt - ziel
        b = max(0, n - ueber)
        keep = np.argsort(uni(hm, 31))[:b]
        ergebnisse[name] = (arr[keep], nidx[keep], hm[keep])
        gesamt -= n - b
        log("Budget: %s von %d auf %d ausgedünnt" % (name, n, b))
    koll_gesamt = sum(int(hat_kollision(nm, v[1]).sum()) for nm, v in ergebnisse.items())
    kmax = int(B.get("kollision_je_feld", 3000))
    for name in reversed(prio):
        if koll_gesamt <= kmax:
            break
        arr, nidx, hm = ergebnisse[name]
        km = hat_kollision(name, nidx)
        nk = int(km.sum())
        if nk == 0:
            continue
        ueber = koll_gesamt - kmax
        entf = min(nk, ueber)
        kidx = np.nonzero(km)[0]
        drop = kidx[np.argsort(uni(hm[kidx], 32))[:entf]]
        keep = np.ones(arr.shape[0], bool)
        keep[drop] = False
        ergebnisse[name] = (arr[keep], nidx[keep], hm[keep])
        koll_gesamt -= entf
        log("Kollisionsbudget: %s um %d reduziert" % (name, entf))
    # Ausgabe
    AUS = regeln["ausgabe"]
    out_dir = os.path.join(basis, AUS.get("ordner", "export/unreal/welt/hochgebirge"), feld)
    os.makedirs(out_dir, exist_ok=True)
    for fn in os.listdir(out_dir):
        if fn.lower().endswith(".f32"):
            os.remove(os.path.join(out_dir, fn))
    dateien = {}
    je_netz = {}
    statistik = {"je_klasse": {}, "je_ebene": {}, "je_stufe_flaeche_prozent": {}}
    for name, (arr, nidx, hm) in ergebnisse.items():
        K = regeln["klassen"][name]
        statistik["je_klasse"][name] = int(arr.shape[0])
        en = EBENE_NAME.get(int(K.get("ebene", 1)), str(K.get("ebene")))
        statistik["je_ebene"][en] = statistik["je_ebene"].get(en, 0) + int(arr.shape[0])
        for ni, pfad in enumerate(K["netze"]):
            m = nidx == ni
            if not m.any():
                continue
            nm = netze[pfad]["name"]
            je_netz.setdefault(nm, []).append(arr[m])
            hoe = netze[pfad]["hoehe_m"]
            d = dateien.get(nm)
            if d is None:
                dateien[nm] = {"pfad": pfad, "anzahl": 0, "gruppe": K.get("gruppe_name", name), "rolle": K.get("rolle", "sonst"),
                               "sichtweite": list(K.get("sichtweite", [0, 0])), "schatten": bool(K.get("schatten", True)),
                               "kollision": bool(K.get("kollision", False) and hoe >= koll_ab), "ebene": en,
                               "nanite": bool(netze[pfad].get("nanite", False))}
            dateien[nm]["anzahl"] += int(m.sum())
    for nm, teile in je_netz.items():
        np.concatenate(teile, axis=0).astype("<f4").tofile(os.path.join(out_dir, nm + ".f32"))
    for s in range(4):
        statistik["je_stufe_flaeche_prozent"][["bergwald", "krummholz", "matte", "fels_schnee"][s]] = round(float(anteil(ctx["stufe"][ctx["feld_in_win"][0]:ctx["feld_in_win"][1], ctx["feld_in_win"][2]:ctx["feld_in_win"][3]] == s)), 1)
    statistik["kollision"] = int(koll_gesamt)
    statistik["baumgrenze_m"] = [round(float(bg.min())), round(float(bg.mean())), round(float(bg.max()))]
    statistik["schneegrenze_m"] = [round(float(sg.min())), round(float(sg.mean())), round(float(sg.max()))]
    statistik["laufzeit_s"] = round(time.time() - t0, 1)
    plan = {"stand": time.strftime("%Y-%m-%d %H:%M"), "feld": feld, "instanzen": int(sum(d["anzahl"] for d in dateien.values())),
            "dateien": dateien, "entfernen": AUS.get("entfernen", ""), "ft_ordner": AUS.get("ft_ordner"), "ft_praefix": AUS.get("ft_praefix"),
            "thema": regeln.get("thema", "hochgebirge"), "faktor": faktor, "seed": regeln.get("seed"), "statistik": statistik,
            "hinweis": "UNGETESTET MIT ECHTDATEN; Eiszapfen-Pivot (z_versatz_anteil) am ersten Feld prüfen."}
    with open(os.path.join(out_dir, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    log("Feld %s: %d Instanzen (%s), Kollision %d, %d Netze, %.1f s → %s" % (
        feld, plan["instanzen"], ", ".join("%s %d" % kv for kv in statistik["je_ebene"].items()), koll_gesamt, len(dateien), time.time() - t0, out_dir))
    if bild:
        bild_schreiben(os.path.join(basis, AUS.get("bild", "docs/pruefung/hochgebirge"), feld + ".png"), ctx,
                       [(nm, v[0]) for nm, v in ergebnisse.items()], feld, rand)
    return plan


# ----------------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Eldarien Hochgebirge-Planer (Teil B4) – UNGETESTET MIT ECHTDATEN")
    ap.add_argument("felder", nargs="+", help="Gitterfelder, z. B. C2 D2 E1 E2")
    ap.add_argument("--bild", action="store_true")
    ap.add_argument("--faktor", type=float, default=1.0)
    ap.add_argument("--basis", default=".")
    ap.add_argument("--regeln", default=None)
    args = ap.parse_args()
    skriptdir = os.path.dirname(os.path.abspath(__file__))
    rp = args.regeln or os.path.join(skriptdir, "hochgebirge_regeln.json")
    if not os.path.isfile(rp):
        sys.exit("FEHLT (Pflicht): Regeldatei %s" % rp)
    with open(rp, encoding="utf-8") as f:
        regeln = json.load(f)
    log("Regeln: %s (Seed %s), numba %s" % (rp, regeln.get("seed"), "ja" if HAVE_NUMBA else "nein (NumPy)"))
    netze = lade_netze(args.basis, skriptdir)
    fehlend = sorted({p for K in regeln["klassen"].values() for p in K["netze"] if p not in netze})
    if fehlend:
        sys.exit("FEHLER: %d Paletten-Pfade nicht in netze.csv: %s" % (len(fehlend), fehlend[:5]))
    log("Paletten: alle %d Netzpfade im Inventar." % len({p for K in regeln["klassen"].values() for p in K["netze"]}))
    masse = lade_masse(args.basis, skriptdir)
    for feld in args.felder:
        try:
            plane_feld(feld, args.basis, regeln, netze, masse, args.faktor, args.bild, skriptdir)
        except ValueError as e:
            log("FEHLER: %s" % e)


if __name__ == "__main__":
    main()
