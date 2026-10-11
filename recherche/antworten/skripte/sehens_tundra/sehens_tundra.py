#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sehens_tundra.py - Sehenswuerdigkeiten-Planer Tundra (Auftrag 13, Phase 2; Muster: sehens_bergwald).

Baut die 8 Tundra-Orte aus sehens/tundra/standorte.json nach den Rezepten in sehens_tundra_regeln.json
(Katalog sehens/tundra/katalog.md, asset_bedarf.json, Entscheidungen Ferat in sehens-STATUS.md) und schreibt das
Lieferformat vorlagen/SEHENS_FORMAT.md:
  <aus>/orte.json, <aus>/gelaende/<id>.f32, <aus>/lagen/<id>_<Lage>.r8      (§2, §3)
  <sw>/<Feld>/plan.json + <Netz>.f32 (Ebene sw_tundra, FORMAT.md §3)            (§4)
  Wasser §5, Effekte §6 (Niagara optional), Materialwuensche §7, Kameras §8 (aus standorte.json), Budgets §9
  Bild je Ort test_<id>.png (--bild)

Aufruf (python -I, NumPy + Pillow):
  python -I sehens_tundra.py --daten2m recherche/vorlagen/daten/sehens --aus <Ordner> [--ort ID ...] [--bild]
  python -I sehens_tundra.py --basis <production>            # 1 m aus export/unreal/welt, Ausgabe dort
Optionen wie sehens_bergwald.py, dazu --ohne-sicht (keine Verdeckungspruefung der Fundstuecke).
Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.

Ort-spezifischer Code (alles andere steht in den Regeln; Zufall deterministisch aus Seed + Ort-ID):
  - gelaende.daemme (alle Orte): Waelle/Graeben entlang Linien (Stempel.damm), nach den ops und Seebecken
  - Fliesstreppe: Solifluktionsloben (Zunge mit flacher Lauf- und steiler Stirnflaeche) + Anker an den Stirnen
  - Steinringe: sortierte Steinringe (Zellen auf einem verwackelten Sechseckgitter, grobe Steine aussen, Grus innen)
  - Wabenmoor: Eiskeilpolygone (Voronoi: Randwall, Graben auf der Grenze, Tuempel in der Zellmitte als see)
  - Ende (Fundstuecke): Verdeckung vom Weg mit Stempel + geplanten Stuecken (sehens_lib/verdeckung.py) als HINWEIS
Quellen: vorlagen/SEHENS_FORMAT.md, vorlagen/FORMAT.md §3, auftraege/13-, 13b-, 13c-*.md,
antworten/skripte/sehens_lib/ (README.md, PLANER_ANLEITUNG.md).
"""

import argparse
import copy
import json
import math
import os
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))          # antworten/skripte (python -I setzt das nicht)

BIOM = "tundra"
_WP = {}


def _log(*t):
    from sehens_lib import ascii_text
    sys.stdout.write("[sehens_%s] %s\n" % (BIOM, " ".join(ascii_text(x) for x in t)))
    sys.stdout.flush()


def abbruch(text, code=2):
    _log("FEHLER:", text)
    sys.exit(code)


def _wegpunkte(welt):
    if "wp" not in _WP:
        from sehens_lib import sicht
        _WP["wp"] = sicht.Wegpunkte(welt, 20)
    return _WP["wp"]


# ----------------------------------------------------------------------------------------------------------------------
# Allgemeine Hooks
# ----------------------------------------------------------------------------------------------------------------------
def hook_daemme(ctx):
    """gelaende.daemme: [{"punkte": [ref, ...] | Linienname, "breite_m", "hoehe_m" (< 0 = Graben), "krone",
    "verjuengung_m", "geschlossen", "modus", "warum"}] - nach den ops und den Seebecken (Stempel.damm)."""
    for d in (ctx.r.get("gelaende") or {}).get("daemme") or []:
        ctx.stempel.damm(ctx.linie(d["punkte"]), float(d["breite_m"]), float(d["hoehe_m"]), float(d.get("krone", 0.3)),
                         d.get("verjuengung_m"), bool(d.get("geschlossen", False)), d.get("modus", "add"))


def hook_sicht(ctx):
    """Fundstuecke: Verdeckung vom Weg (Wege + Pfade) mit Stempel und geplanten Stuecken (nur Meldung)."""
    if ctx.st.get("art") != "fundstueck" or _WP.get("aus"):
        return
    from sehens_lib import verdeckung
    sp = ctx.r.get("sicht") or {}
    res = verdeckung.pruefe_ort(ctx, _wegpunkte(ctx.welt), ziel_hoehe_m=sp.get("ziel_hoehe_m"),
                                probe_r_m=sp.get("probe_r_m"), kern_m=sp.get("kern_m"))
    ctx.sicht_ergebnis = res
    ctx.melde("HINWEIS", res["text"])


# ----------------------------------------------------------------------------------------------------------------------
# Ort-Hooks
# ----------------------------------------------------------------------------------------------------------------------
def hook_loben_anker(ctx):
    """Fliesstreppe: Lobenmitten ('lobe_k'), Stirnpunkte ('stirn_k_n', Richtung hangab) und Steinstreifen zwischen den
    Loben (Linien 'streifen_k'). Regel 'loben': {"hangab": grad, "liste": [[versatz_hangab_m, versatz_quer_m], ...],
    "laenge_m", "breite_m", "hoehe_m", "stirn_m", "stirn_abstand_m"}."""
    from sehens_lib import instanzen as ins, stempel as stm
    L = ctx.r["loben"]
    ha = float(L.get("hangab", ctx.richtung("hangab")))
    ux, uy = stm.kompass_vektor(ha)
    vx, vy = uy, -ux                                              # quer (links in Laufrichtung hangab)
    rng = ins.rng_fuer(ctx.seed, ctx.id, "loben")
    hl, hb = float(L["laenge_m"]) / 2.0, float(L["breite_m"]) / 2.0
    ctx._loben = []
    for k, (a, b) in enumerate(L["liste"]):
        f = 1.0 + 0.15 * float(rng.uniform(-1, 1))
        cx, cy = ctx.mx + a * ux + b * vx, ctx.my + a * uy + b * vy
        lo = {"x": cx, "y": cy, "hl": hl * f, "hb": hb * (2.0 - f)}
        ctx._loben.append(lo)
        ctx.anker["lobe_%d" % k] = (cx, cy)
        ctx.anker["lobe_%d_stirn" % k] = (cx + ux * lo["hl"], cy + uy * lo["hl"])
        # Stirnbogen: Halbellipse vor der Lobenmitte (a > 0)
        ab = float(L.get("stirn_abstand_m", 1.2))
        n = max(6, int(math.pi * (lo["hl"] + lo["hb"]) / 2.0 / ab))
        for m in range(n + 1):
            t = -math.pi / 2 + math.pi * m / n
            ea, eb = lo["hl"] * math.cos(t) * 0.97, lo["hb"] * math.sin(t) * 0.97
            px, py = cx + ea * ux + eb * vx, cy + ea * uy + eb * vy
            ctx.anker["stirn_%d_%02d" % (k, m)] = (px, py)
            # Blick von der Stirn nach aussen (Normale der Ellipse)
            nx_, ny_ = math.cos(t) / lo["hl"], math.sin(t) / lo["hb"]
            ctx.richtungen["stirn_%d_%02d" % (k, m)] = stm.vektor_kompass(nx_ * ux + ny_ * vx, nx_ * uy + ny_ * vy)
    # Steinstreifen hangab zwischen benachbarten Loben (Material wandert seitlich ab)
    los = sorted(ctx._loben, key=lambda o: (o["x"] - ctx.mx) * vx + (o["y"] - ctx.my) * vy)
    for k in range(len(los) - 1):
        a_, b_ = los[k], los[k + 1]
        mx_, my_ = (a_["x"] + b_["x"]) / 2.0, (a_["y"] + b_["y"]) / 2.0
        ctx.linien["streifen_%d" % k] = [[mx_ - ux * 16, my_ - uy * 16], [mx_ + ux * 18, my_ + uy * 18]]


def hook_loben_gelaende(ctx):
    """Fliesserde-Zungen: Laufflaeche steigt von hinten (0) zur Stirn (hoehe_m), Stirn auf stirn_m steil."""
    import numpy as np
    from sehens_lib import stempel as stm
    L = ctx.r["loben"]
    st = ctx.stempel
    ha = float(L.get("hangab", ctx.richtung("hangab")))
    ux, uy = stm.kompass_vektor(ha)
    vx, vy = uy, -ux
    h = float(L["hoehe_m"])
    f = float(L.get("stirn_m", 3.0))
    for lo in ctx._loben:
        dx, dy = st.X - lo["x"], st.Y - lo["y"]
        a = dx * ux + dy * uy
        b = dx * vx + dy * vy
        r_vorn = np.hypot(np.maximum(a, 0.0) / lo["hl"], b / lo["hb"])
        rand = 1.0 - stm.glatt01((r_vorn - (1.0 - f / lo["hl"])) / (f / lo["hl"]))
        lauf = stm.glatt01((a + 1.8 * lo["hl"]) / (1.8 * lo["hl"]))
        w = np.where(a < -2.0 * lo["hl"], 0.0, rand * lauf)
        st._anwenden(w, rel=h * (1.0 + 0.1 * float(np.sin(lo["x"]))), modus="max" if L.get("nur_heben", True) else "add",
                     name="lobe")


def hook_ringe_anker(ctx):
    """Steinringe: Zellmitten auf einem verwackelten Sechseckgitter in der Ellipse; je Ring Anker fuer grobe Steine auf
    dem Ring ('rsg_' groesste, 'rs_' uebrige), Grus innen ('rg_'), Ringmitte ('rm_'). Regel 'ringe':
    {"bei", "a_m", "b_m", "richtung", "abstand_m", "r_m": [a, b], "stein_abstand_m", "grus_je": [a, b]}."""
    from sehens_lib import instanzen as ins, stempel as stm
    R = ctx.r["ringe"]
    rng = ins.rng_fuer(ctx.seed, ctx.id, "ringe")
    x0, y0 = ctx.punkt(R.get("bei", "mitte"))
    A, B = float(R["a_m"]), float(R["b_m"])
    rg = ctx.richtung(R.get("richtung", 0.0), R.get("bei", "mitte"))
    ux, uy = stm.kompass_vektor(rg)
    d = float(R.get("abstand_m", 4.4))
    zellen = []
    for i in range(-8, 9):
        for j in range(-8, 9):
            px = (j + 0.5 * (i % 2)) * d + float(rng.uniform(-0.18, 0.18)) * d
            py = i * d * 0.866 + float(rng.uniform(-0.18, 0.18)) * d
            if (px / A) ** 2 + (py / B) ** 2 > 1.0:
                continue
            zellen.append((x0 + px * ux - py * uy, y0 + px * uy + py * ux))
    sa = float(R.get("stein_abstand_m", 0.42))
    r0, r1 = R.get("r_m", [0.9, 1.7])
    for k, (cx, cy) in enumerate(zellen):
        rr = float(rng.uniform(r0, r1)) * min(1.0, 0.5 * d / max(r1, 0.1) + 0.2)
        ctx.anker["rm_%02d" % k] = (cx, cy)
        n = max(8, int(2 * math.pi * rr / sa))
        phase = float(rng.uniform(0, 2 * math.pi))
        for m in range(n):
            t = phase + 2 * math.pi * m / n
            q = rr * (1.0 + 0.12 * float(rng.uniform(-1, 1)))
            px, py = cx + q * math.cos(t), cy + q * math.sin(t)
            name = ("rsg_%02d_%02d" if m % 3 == 0 else "rs_%02d_%02d") % (k, m)
            ctx.anker[name] = (px, py)
        for m in range(int(rng.integers(int(R.get("grus_je", [6, 10])[0]), int(R.get("grus_je", [6, 10])[1]) + 1))):
            t = float(rng.uniform(0, 2 * math.pi))
            q = rr * 0.7 * math.sqrt(float(rng.uniform(0, 1)))
            ctx.anker["rg_%02d_%02d" % (k, m)] = (cx + q * math.cos(t), cy + q * math.sin(t))
    ctx._ringe = len(zellen)


def hook_waben_gelaende(ctx):
    """Wabenmoor: Eiskeilpolygone im Terrassenfenster - Voronoi-Zellen (verwackeltes Sechseckgitter), Randwall +rand_m
    beidseits eines Grabens (graben_m) auf der Zellgrenze, Zellmitte flach eingesenkt; in den 'tuempel' Zellen
    ein see (schwarz_spiegel) - die Seebecken werden hier nach dem Relief gestempelt. Regel 'waben':
    {"bei", "r_m", "abstand_m", "rand_m", "graben_m", "mitte_m", "tuempel": n, "tuempel_r_m": [a, b]}."""
    import numpy as np
    from sehens_lib import instanzen as ins, stempel as stm
    W = ctx.r["waben"]
    st = ctx.stempel
    rng = ins.rng_fuer(ctx.seed, ctx.id, "waben")
    x0, y0 = ctx.punkt(W.get("bei", "mitte"))
    R = float(W["r_m"])
    d = float(W.get("abstand_m", 10.5))
    C = []
    for i in range(-5, 6):
        for j in range(-5, 6):
            px = (j + 0.5 * (i % 2)) * d + float(rng.uniform(-0.15, 0.15)) * d
            py = i * d * 0.866 + float(rng.uniform(-0.15, 0.15)) * d
            if math.hypot(px, py) <= R + d:
                C.append((x0 + px, y0 + py))
    C = np.asarray(C)
    X, Y = st.X, st.Y
    D = np.sqrt((X[..., None] - C[:, 0]) ** 2 + (Y[..., None] - C[:, 1]) ** 2)
    Ds = np.sort(D, axis=-1)
    e = (Ds[..., 1] - Ds[..., 0]) / 2.0                           # Abstand zur Zellgrenze
    maske = 1.0 - stm.glatt01((np.hypot(X - x0, Y - y0) - R) / 6.0)
    rand = float(W.get("rand_m", 0.4)) * np.exp(-((e - 1.6) / 1.1) ** 2)
    graben = -float(W.get("graben_m", 0.3)) * (1.0 - stm.glatt01(e / 0.9))
    mitte = -float(W.get("mitte_m", 0.25)) * stm.glatt01((e - 2.0) / 2.0)
    st._anwenden(maske, rel=rand + graben + mitte, modus="add", name="waben")
    # Tuempel in den inneren Zellen (nicht auf der Boeschung): die naechsten zur Mitte
    innen = [k for k in np.argsort(np.hypot(C[:, 0] - x0, C[:, 1] - y0)) if math.hypot(C[k, 0] - x0, C[k, 1] - y0) <= R - 3]
    n = int(W.get("tuempel", 7))
    w_neu = []
    for m, k in enumerate(innen[:n]):
        r_ = float(rng.uniform(*W.get("tuempel_r_m", [1.6, 2.4])))
        w = {"typ": "see", "id": "tuempel_%d" % (m + 1), "bei": {"pos_m": [float(C[k, 0]), float(C[k, 1])]},
             "spiegel": "boden+%.2f" % float(W.get("spiegel_m", 0.12)), "tiefe_m": float(W.get("tiefe_m", 0.5)),
             "farbe": W.get("farbe", "schwarz_spiegel"),
             "becken": {"a_m": r_ * 1.1, "b_m": r_ * 0.9, "richtung": float(rng.uniform(0, 180)), "ufer_m": 1.2,
                        "freibord_m": 0.06, "boden": 0.35, "auslass": None}}
        w_neu.append(w)
        ctx.anker["zelle_%d" % m] = (float(C[k, 0]), float(C[k, 1]))
    for k in range(len(C)):
        ctx.anker["wabe_%02d" % k] = (float(C[k, 0]), float(C[k, 1]))
    # Grabenpunkte (Zellgrenzen) als Anker 'grenz_###' (zufaellig nummeriert, damit 'anzahl' eine Auswahl streut)
    gi = np.flatnonzero(((e < 0.6) & (np.hypot(X - x0, Y - y0) <= R - 1.0)).ravel())
    if gi.size:
        gi = gi[rng.permutation(gi.size)][:int(W.get("graben_punkte", 160))]
        for m, k in enumerate(gi):
            ctx.anker["grenz_%03d" % m] = (float(X.ravel()[k] + rng.uniform(-0.4, 0.4)), float(Y.ravel()[k] + rng.uniform(-0.4, 0.4)))
    for w in w_neu:
        ctx.r.setdefault("wasser", []).append(w)
        ctx._see_becken(w)
    ctx._waben = len(C)


HOOKS = {
    "tundra_04_die_fliesstreppe": {"anker": hook_loben_anker, "nach_gelaende": hook_loben_gelaende},
    "tundra_07_die_steinringe": {"anker": hook_ringe_anker},
    "tundra_08_das_wabenmoor": {"nach_gelaende": hook_waben_gelaende},
}


def _hooks(oid):
    h = {"anker": [], "nach_gelaende": [hook_daemme], "ende": [hook_sicht]}
    for k, f in (HOOKS.get(oid) or {}).items():
        h.setdefault(k, []).insert(0 if k != "nach_gelaende" else len(h[k]), f)
    return {k: (lambda ctx, fs=fs: [f(ctx) for f in fs]) for k, fs in h.items() if fs}


# ----------------------------------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Sehenswuerdigkeiten-Planer %s (Auftrag 13, Phase 2)" % BIOM)
    ap.add_argument("--orte", "--ort", nargs="+", default=None, dest="orte", help="nur diese Ort-IDs (Standard: alle 8)")
    ap.add_argument("--bild", action="store_true", help="Testbild test_<id>.png je geplantem Ort")
    ap.add_argument("--bild-ordner", default=None, help="Ordner fuer test_<id>.png (Standard: --aus)")
    ap.add_argument("--aus", default=None, help="Ausgabeordner (Standard <basis>/export/unreal/welt/sehens/%s)" % BIOM)
    ap.add_argument("--sw-aus", default=None, help="Ebene sw_%s (Standard: <aus>/sw_%s)" % (BIOM, BIOM))
    ap.add_argument("--basis", default=".", help="production-Wurzel (1-m-Daten in export/unreal/welt)")
    ap.add_argument("--regeln", default=os.path.join(HIER, "sehens_%s_regeln.json" % BIOM))
    ap.add_argument("--inventar", default=None, help="Ordner mit netze.csv, inventar_extra.json (Standard vorlagen/daten)")
    ap.add_argument("--sehens", default=None, help="Ordner antworten/sehens (standorte.json aller Biome)")
    ap.add_argument("--ohne-pruefung", action="store_true")
    ap.add_argument("--ohne-sicht", action="store_true", help="keine Verdeckungspruefung der Fundstuecke")
    ap.add_argument("--daten2m", default=None, help="2-m-PNGs (Cloud-Test): recherche/vorlagen/daten/sehens")
    ap.add_argument("--daten1m", default=None, help="1-m-Originale (Standard <basis>/export/unreal/welt)")
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    T0 = time.perf_counter()
    _WP["aus"] = bool(a.ohne_sicht)

    from sehens_lib import daten, gelaende, inventar, instanzen, rezept, vorschau, sehens_pruefen, log  # noqa: F401
    from sehens_lib import format as sfmt

    # --- Regeln, Inventar, Standorte
    if not os.path.exists(a.regeln):
        abbruch("Regeln fehlen: %s" % a.regeln)
    with open(a.regeln, "r", encoding="utf-8") as f:
        R = json.load(f)
    try:
        inv = inventar.Inventar.lade(a.inventar)
    except FileNotFoundError as ex:
        abbruch(str(ex))
    sehens = a.sehens or daten.standard_pfad_sehens()
    st_pfad = os.path.join(sehens, BIOM, "standorte.json")
    if not os.path.exists(st_pfad):
        abbruch("standorte.json fehlt: %s" % st_pfad)
    standorte = sfmt.lade_standorte(st_pfad)
    pfade_biom = [p for p in (standorte.get("pfade") or [])]

    # --- Daten
    daten1m = a.daten1m
    if not a.daten2m and not daten1m:
        daten1m = os.path.join(a.basis, "export", "unreal", "welt")
        if not os.path.isdir(daten1m):
            abbruch("weder --daten2m noch 1-m-Daten (%s) gefunden" % daten1m)
    try:
        welt = daten.lade(a.daten2m, daten1m, pfade=sehens)
    except (FileNotFoundError, ValueError) as ex:
        abbruch("Daten: %s" % ex)
    gel = gelaende.Gelaende(welt, cache=a.cache)
    _log(welt.info())

    # --- Ausgabe
    if a.aus:
        aus = os.path.abspath(a.aus)
        sw = os.path.abspath(a.sw_aus or os.path.join(aus, "sw_" + BIOM))
    else:
        aus = os.path.join(a.basis, "export", "unreal", "welt", "sehens", BIOM)
        sw = a.sw_aus or os.path.join(a.basis, "export", "unreal", "welt", "sw_" + BIOM)
    os.makedirs(aus, exist_ok=True)

    # --- Orte waehlen (mit --orte: alle Orte in denselben Feldern mitplanen, plan.json bleibt vollstaendig)
    alle = {o["id"]: o for o in standorte["orte"]}
    gewaehlt = list(alle) if not a.orte else a.orte
    for oid in gewaehlt:
        if oid not in alle:
            abbruch("Ort %s nicht in %s" % (oid, st_pfad))
        if oid not in R["orte"]:
            abbruch("Ort %s hat kein Rezept in %s" % (oid, a.regeln))
    felder = {f for oid in gewaehlt for f in alle[oid].get("felder", [])}
    planen = [oid for oid in alle if oid in gewaehlt or felder & set(alle[oid].get("felder", []))]
    if len(planen) > len(gewaehlt):
        _log("mitgeplant (gleiche Felder): %s" % ", ".join(sorted(set(planen) - set(gewaehlt))))
    mitten = {oid: (o["mitte_cm"][0] / 100.0, o["mitte_cm"][1] / 100.0) for oid, o in alle.items()}

    ebene = instanzen.Ebene(BIOM, inv, stand=sfmt.heute())
    kontexte = []
    for oid in planen:
        t0 = time.perf_counter()
        regel = copy.deepcopy(R["orte"][oid])
        ctx = rezept.OrtKontext(welt, gel, inv, ebene, alle[oid], regel, BIOM, seed=R.get("seed", 0),
                                pfade_biom=pfade_biom, paletten=R.get("paletten"), materialien=R.get("materialwuensche"),
                                orte_mitten=mitten)
        ctx.baue(_hooks(oid))
        kontexte.append(ctx)
        z = ebene.zaehle(oid)
        _log("%-30s %5d Instanzen (%4d Kollision), %3d Akteure, Stempel %.1f m  %.1f s"
             % (oid, z["instanzen"], z["kollision"], z["akteure"], ctx.stempel.max_aenderung_m, time.perf_counter() - t0))

    # alte Eintraege (bei --orte) erhalten
    alte = None
    pj = os.path.join(aus, "orte.json")
    if a.orte and os.path.exists(pj):
        with open(pj, "r", encoding="utf-8") as f:
            alte = json.load(f).get("orte", [])
    d, info = rezept.schreibe_biom(aus, sw, BIOM, kontexte, ebene, R.get("materialwuensche", []), inv, alte_orte=alte)

    # --- Bilder
    if a.bild:
        bo = a.bild_ordner or aus
        for ctx in kontexte:
            if ctx.id in gewaehlt:
                p = vorschau.vorschau(ctx, os.path.join(bo, "test_%s.png" % ctx.id))
                _log("Bild:", p)

    # --- Meldungen der Orte
    meld = [m for c in kontexte for m in c.meldungen]
    for st in ("FEHLER", "WARNUNG"):
        for s, oid, t in meld:
            if s == st:
                _log("  %-7s %-28s %s" % (s, oid[:28], t))
    for c in kontexte:
        if getattr(c, "sicht_ergebnis", None):
            _log("  SICHT   %-28s %s" % (c.id[:28], c.sicht_ergebnis["text"]))
    _log("Planer: %d FEHLER, %d WARNUNG, %d HINWEIS" % tuple(sum(1 for m in meld if m[0] == s)
                                                         for s in ("FEHLER", "WARNUNG", "HINWEIS")))
    rc = 1 if any(m[0] == "FEHLER" for m in meld) else 0

    # --- Pruefer (SEHENS_FORMAT)
    if not a.ohne_pruefung:
        bef = sehens_pruefen.pruefe_orte(d, basis=aus, inv=inv, welt=welt, sw_ordner=sw)
        z = sehens_pruefen.melde(bef, "orte.json + sw_%s" % BIOM)
        if z["FEHLER"]:
            rc = 1
    # --- Zusammenfassung
    _log("-" * 72)
    for o in d["orte"]:
        b = o["budget"]
        _log("%-30s Inst %5d  Koll %4d  Akt %3d  Licht %d  Niagara %d  Nebel %d  Decal %2d  Stempel %4.1f m"
             % (o["id"], b["instanzen"], b["kollision"], b["akteure"], b["lichter"], b["niagara"], b.get("nebel", 0),
                b["decals"], (o.get("gelaende") or {}).get("max_aenderung_m", 0.0)))
    for feld, i in sorted(info.items()):
        _log("Feld %s: %d Instanzen, %d Kollision, %d Akteure (%s)" % (feld, i["instanzen"], i["kollision"],
                                                                         i["akteure"], ", ".join(i["orte"])))
    for h in ebene.hinweise:
        _log("Hinweis:", h)
    _log("Ausgabe: %s  |  Ebene: %s  |  %.1f s" % (aus, sw, time.perf_counter() - T0))
    return rc


if __name__ == "__main__":
    sys.exit(main())
