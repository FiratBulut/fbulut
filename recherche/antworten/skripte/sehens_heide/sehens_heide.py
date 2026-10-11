#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sehens_heide.py - Sehenswuerdigkeiten-Planer Heide (Auftrag 13, Phase 2; Muster: sehens_bergwald).

Baut die 8 Heide-Orte aus sehens/heide/standorte.json nach den Rezepten in sehens_heide_regeln.json
(Katalog sehens/heide/katalog.md, asset_bedarf.json, Entscheidungen Ferat in sehens-STATUS.md) und schreibt das
Lieferformat vorlagen/SEHENS_FORMAT.md:
  <aus>/orte.json, <aus>/gelaende/<id>.f32, <aus>/lagen/<id>_<Lage>.r8      (§2, §3)
  <sw>/<Feld>/plan.json + <Netz>.f32 (Ebene sw_heide, FORMAT.md §3)            (§4)
  Wasser §5, Effekte §6 (Niagara optional), Materialwuensche §7, Kameras §8 (aus standorte.json), Budgets §9
  Bild je Ort test_<id>.png (--bild)

Aufruf (python -I, NumPy + Pillow):
  python -I sehens_heide.py --daten2m recherche/vorlagen/daten/sehens --aus <Ordner> [--ort ID ...] [--bild]
  python -I sehens_heide.py --basis <production>            # 1 m aus export/unreal/welt, Ausgabe dort
Optionen wie sehens_bergwald.py, dazu --ohne-sicht (keine Verdeckungspruefung der Fundstuecke).
Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.

Planer-Code (alles Ortsspezifische steht in den Regeln; Zufall deterministisch aus Seed + Ort-ID):
  - gelaende.daemme (alle Orte): Waelle/Graeben entlang Linien (Stempel.damm), nach den ops und Seebecken
    (Kesselkranz, Duenenkamm, Ufer West der Klamm, Kesselrand, Felsrahmen)
  - Zugang: Fussweg pfad_cm endet am Ufer bzw. pfad.ende_r_m vor der Mitte (nicht ueber den Held/ins Wasser)
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

BIOM = "heide"
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


def hook_zugang(ctx):
    """Fussweg pfad_cm (Phase 1, endet in der Ortsmitte) fuer das Bodenband kuerzen: nicht ins Wasser (See,
    Bach) und nicht ueber den Held - er endet am Ufer bzw. pfad.ende_r_m vor der Mitte (Regel pfad.ende_r_m)."""
    import numpy as np
    pr = ctx.r.get("pfad") or {}
    P = ctx.st.get("pfad_cm")
    if not pr or not P or len(P) < 2:
        return
    Q = np.asarray([[p[0] / 100.0, p[1] / 100.0] for p in P])      # Ort -> Weg
    seg = np.hypot(*np.diff(Q, axis=0).T)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    t = np.arange(0.0, s[-1] + 1e-6, 1.0)
    x = np.interp(t, s, Q[:, 0])
    y = np.interp(t, s, Q[:, 1])
    weg = (np.hypot(x - ctx.mx, y - ctx.my) < float(pr.get("ende_r_m", 0.0))) | np.asarray(ctx.im_wasser(x, y, 1.5))
    k = 0
    while k < len(t) - 2 and (weg[k] or weg[k + 1]):
        k += 1
    if k == 0:
        return
    neu = [[round(x[k] * 100), round(y[k] * 100)]] + [list(p[:2]) for p, sp in zip(P, s) if sp > t[k] + 0.5]
    if len(neu) >= 2:
        ctx.st = dict(ctx.st, pfad_cm=neu)
        ctx.melde("HINWEIS", "Zugang (pfad_cm) %.0f m vor der Mitte beendet (Ufer/Held frei)" % t[k])


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


HOOKS = {}


def _hooks(oid):
    h = {"anker": [], "nach_gelaende": [hook_daemme], "gruppen": [hook_zugang], "ende": [hook_sicht]}
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
