#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sehens_dschungel.py - Sehenswuerdigkeiten-Planer Dschungel (Auftrag 13, Phase 2, Agent B3).

Baut die 8 Dschungel-Orte aus sehens/dschungel/standorte.json nach den Rezepten in sehens_dschungel_regeln.json
(Katalog sehens/dschungel/katalog.md inkl. 'Abgleich 13b/13c', asset_bedarf.json) und schreibt das Lieferformat
vorlagen/SEHENS_FORMAT.md:
  <aus>/orte.json, <aus>/gelaende/<id>.f32, <aus>/lagen/<id>_<Lage>.r8      (§2, §3)
  <sw>/<Feld>/plan.json + <Netz>.f32 (Ebene sw_dschungel, FORMAT.md §3)          (§4)
  Wasser §5, Effekte §6 (Niagara optional), Materialwuensche §7, Kameras §8 (aus standorte.json), Budgets §9
  Bild je Ort test_<id>.png (--bild)

Aufruf (python -I, NumPy + Pillow):
  python -I sehens_dschungel.py --daten2m recherche/vorlagen/daten/sehens --aus <Ordner> [--ort ID ...] [--bild]
  python -I sehens_dschungel.py --basis <production>            # 1 m aus export/unreal/welt, Ausgabe dort
Optionen: --orte/--ort ID ... (nur diese Orte; Orte in denselben Feldern werden mitgeplant, damit plan.json
  vollstaendig bleibt), --bild (test_<id>.png), --bild-ordner, --sw-aus (Ebene sw_dschungel), --regeln, --inventar,
  --sehens (Ordner mit <biom>/standorte.json), --cache, --ohne-pruefung.
Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.

Ort-spezifischer Code (alles andere steht in den Regeln): Hook 'cenote_umriss' (Blaues Auge) beschneidet das
Seebecken auf die echte Schachtkontur (Umriss sternfoermig aus dem Gelaende, Vertiefung nur im Schacht), damit der
Stempel die Schachtwaende nicht anschneidet.
Quellen: vorlagen/SEHENS_FORMAT.md, vorlagen/FORMAT.md §3, antworten/verteilung-KONVENTIONEN.md,
auftraege/13-, 13b-, 13c-*.md, antworten/skripte/sehens_lib/ (README.md, PLANER_ANLEITUNG.md).
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

BIOM = "dschungel"


def _log(*t):
    from sehens_lib import ascii_text
    sys.stdout.write("[sehens_%s] %s\n" % (BIOM, " ".join(ascii_text(x) for x in t)))
    sys.stdout.flush()


def abbruch(text, code=2):
    _log("FEHLER:", text)
    sys.exit(code)


# ----------------------------------------------------------------------------------------------------------------------
# Hooks (Formen, die sich nicht als Regel ausdruecken lassen)
# ----------------------------------------------------------------------------------------------------------------------
def _zusammenhang(m, i0, j0):
    """Zusammenhaengende Zellen von m ab (i0, j0) (4er-Nachbarschaft, ohne SciPy)."""
    import numpy as np
    out = np.zeros_like(m)
    if not m[i0, j0]:
        return out
    stapel = [(i0, j0)]
    out[i0, j0] = True
    H, W = m.shape
    while stapel:
        i, j = stapel.pop()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < H and 0 <= b < W and m[a, b] and not out[a, b]:
                out[a, b] = True
                stapel.append((a, b))
    return out


def _erodiere(m, n):
    import numpy as np
    r = m.copy()
    for _ in range(int(n)):
        q = r.copy()
        q[1:, :] &= r[:-1, :]
        q[:-1, :] &= r[1:, :]
        q[:, 1:] &= r[:, :-1]
        q[:, :-1] &= r[:, 1:]
        r = q
    return r


def hook_cenote_umriss(ctx):
    """Blaues Auge: der Schacht ist kein Ellipsenbecken. Nach dem Seebecken (Ellipse, die den Schacht ganz
    abdeckt) wird der Stempel auf den echten Schacht beschnitten: Seeumriss = Kontur des Schachts (Gelaende
    < schacht.kante_m, zusammenhaengend ab der Schachtmitte), Vertiefung nur im Schacht und mind. rand_zellen
    Zellen von seiner Wand entfernt (dort bleibt der Bestandsgrund als Uferstufe), ausserhalb kein Delta.
    So schneidet das Becken die Schachtwaende nicht an, und es entsteht keine neue geschlossene Senke."""
    import numpy as np
    from sehens_lib import stempel as stm
    c = ctx.r.get("schacht") or {}
    sid = c.get("see", "auge")
    s = ctx.see[sid]
    st = ctx.stempel
    i0, j0 = np.unravel_index(int(np.argmin(np.hypot(st.X - s["x"], st.Y - s["y"]))), st.X.shape)
    m0 = _zusammenhang(st.h0 < float(c.get("kante_m", 0.8)), i0, j0)
    m_in = _erodiere(m0, int(c.get("rand_zellen", 3)))
    st.delta = np.where(m_in, st.delta, 0.0)
    # Umriss: sternfoermig von der Schachtmitte (Strahlen alle 5 Grad, letzte Schachtzelle)
    cx, cy = float(st.X[m0].mean()), float(st.Y[m0].mean())
    pts = []
    for g in np.arange(0.0, 360.0, 5.0):
        ux, uy = stm.kompass_vektor(float(g))
        r_last = 0.0
        for r in np.arange(0.0, 80.0, 0.5):
            x, y = cx + ux * r, cy + uy * r
            i, j = int(round((y - st.Y[0, 0]) / st.z)), int(round((x - st.X[0, 0]) / st.z))
            if not (0 <= i < m0.shape[0] and 0 <= j < m0.shape[1]) or not m0[i, j]:
                break
            r_last = r
        pts.append([cx + ux * max(r_last + 0.5, 1.0), cy + uy * max(r_last + 0.5, 1.0)])
    if stm.flaeche(pts) < 0:
        pts = pts[::-1]
    s.update(umriss_m=pts, x=cx, y=cy)
    ctx.linien["ufer_" + sid] = pts + [pts[0]]
    ctx.anker[sid + "_mitte"] = (cx, cy)
    ctx.melde("HINWEIS", "see %s: Umriss = Schachtkontur (%d Punkte, %.0f m2), Vertiefung nur im Schacht"
              % (sid, len(pts), float(m0.sum()) * st.z * st.z))


HOOKS = {"dschungel_04_blaues_auge": {"nach_gelaende": hook_cenote_umriss}}


# ----------------------------------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Sehenswuerdigkeiten-Planer Dschungel (Auftrag 13, Phase 2)")
    ap.add_argument("--orte", "--ort", nargs="+", default=None, dest="orte", help="nur diese Ort-IDs (Standard: alle 8)")
    ap.add_argument("--bild", action="store_true", help="Testbild test_<id>.png je geplantem Ort")
    ap.add_argument("--bild-ordner", default=None, help="Ordner fuer test_<id>.png (Standard: --aus)")
    ap.add_argument("--aus", default=None, help="Ausgabeordner (Standard <basis>/export/unreal/welt/sehens/dschungel)")
    ap.add_argument("--sw-aus", default=None, help="Ebene sw_dschungel (Standard: <aus>/sw_dschungel bzw. <basis>/export/unreal/welt/sw_dschungel)")
    ap.add_argument("--basis", default=".", help="production-Wurzel (1-m-Daten in export/unreal/welt)")
    ap.add_argument("--regeln", default=os.path.join(HIER, "sehens_dschungel_regeln.json"))
    ap.add_argument("--inventar", default=None, help="Ordner mit netze.csv, inventar_extra.json (Standard vorlagen/daten)")
    ap.add_argument("--sehens", default=None, help="Ordner antworten/sehens (standorte.json aller Biome)")
    ap.add_argument("--ohne-pruefung", action="store_true")
    ap.add_argument("--daten2m", default=None, help="2-m-PNGs (Cloud-Test): recherche/vorlagen/daten/sehens")
    ap.add_argument("--daten1m", default=None, help="1-m-Originale (Standard <basis>/export/unreal/welt)")
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    T0 = time.perf_counter()

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

    ebene = instanzen.Ebene(BIOM, inv, stand=sfmt.heute())
    kontexte = []
    for oid in planen:
        t0 = time.perf_counter()
        regel = copy.deepcopy(R["orte"][oid])
        ctx = rezept.OrtKontext(welt, gel, inv, ebene, alle[oid], regel, BIOM, seed=R.get("seed", 0),
                                pfade_biom=pfade_biom, paletten=R.get("paletten"), materialien=R.get("materialwuensche"))
        ctx.baue(HOOKS.get(oid))
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
