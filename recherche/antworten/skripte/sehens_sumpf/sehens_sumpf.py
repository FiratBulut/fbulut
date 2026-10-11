#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sehens_sumpf.py - Sehenswuerdigkeiten-Planer Sumpf (Auftrag 13, Phase 2), nach dem Muster sehens_bergwald.

Baut die 8 Sumpf-Orte aus sehens/sumpf/standorte.json nach den Rezepten in sehens_sumpf_regeln.json
(Katalog sehens/sumpf/katalog.md, asset_bedarf.json) und schreibt das Lieferformat vorlagen/SEHENS_FORMAT.md:
  <aus>/orte.json, <aus>/gelaende/<id>.f32, <aus>/lagen/<id>_<Lage>.r8      (§2, §3)
  <sw>/<Feld>/plan.json + <Netz>.f32 (Ebene sw_sumpf, FORMAT.md §3)            (§4)
  Wasser §5, Effekte §6, Materialwuensche §7, Kameras §8 (aus standorte.json), Budgets §9
  Bild je Ort test_<id>.png (--bild)

Das Sumpfwasser steht NICHT in karte_wasser: es ist der Epic-See T_2954_391 (Spiegel 1,58 m) plus Teiche gleichen
Spiegels aus wasser_welt.json. Jede Regel laedt sie als "bestandswasser" (sehens_lib: nass nur unter dem Spiegel).

Aufruf (python -I, NumPy + Pillow):
  python -I sehens_sumpf.py --daten2m recherche/vorlagen/daten/sehens --aus <Ordner> [--ort ID ...] [--bild]
  python -I sehens_sumpf.py --basis <production>            # 1 m aus export/unreal/welt, Ausgabe dort
Optionen wie sehens_bergwald (--orte, --bild, --bild-ordner, --sw-aus, --regeln, --inventar, --sehens, --cache,
  --ohne-pruefung) plus --ohne-verdeckung. Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.

Ort-spezifischer Code (alles andere steht in den Regeln):
  - Hook 'zugang' (alle Orte): Fussweg Ort -> Weg aus kandidaten.erreichbarkeit (standorte.json hat keine pfad_cm),
    nasse Abschnitte im Epic-See werden ein Bultenruecken (Stempel, Spiegel + 0,22 m); Wasser im Ortskern bleibt frei.
  - Verdeckungsprobe (Regel 'verdeckung'): Erlenbruch wird erst durch seinen Gehoelzring verdeckt - geprueft mit
    sehens_lib.verdeckung gegen alle Wegpunkte (WARNUNG, wenn sichtbar).
Quellen: vorlagen/SEHENS_FORMAT.md, vorlagen/FORMAT.md §3, auftraege/13-, 13b-, 13c-*.md,
antworten/skripte/sehens_lib/ (README.md, PLANER_ANLEITUNG.md).
"""

import argparse
import copy
import json
import os
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))          # antworten/skripte (python -I setzt das nicht)

BIOM = "sumpf"


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
def _nass_laeufe(nass):
    """Zusammenhaengende True-Laeufe -> Liste (a, b) Indizes (b exklusiv)."""
    out, a = [], None
    for k, v in enumerate(list(nass) + [False]):
        if v and a is None:
            a = k
        elif not v and a is not None:
            out.append((a, k))
            a = None
    return out


def hook_zugang_anker(ctx):
    """Zugang (alle Sumpforte): standorte.json hat fuer den Sumpf weder 'pfade' noch 'pfad_cm' (Phase 1: 'keine Pfade
    noetig'), der Fussweg fuehrt aber 0-94 m durch den Epic-See. Der Hook rechnet den Fussweg mit
    kandidaten.erreichbarkeit (Ort -> naechster Weg), kuerzt ihn am Ort auf das erste Ufer (Wasser im Ortskern bleibt
    frei: Ertrunkener Wald, Tellerweiher) und merkt die nassen Abschnitte weiter draussen fuer den Bultenruecken vor.
    Regel 'zugang': {"frei_r_m": Kernradius ohne Ruecken, "breite_m", "ueber_spiegel_m"}."""
    import numpy as np
    from sehens_lib import kandidaten, gelaende as _g
    z = ctx.r.get("zugang") or {}
    if ctx.st.get("pfad_cm") or z.get("aus"):
        return
    e = kandidaten.erreichbarkeit(ctx.welt, ctx.gel, ctx.mx, ctx.my)
    P = [list(map(float, p[:2])) for p in e.get("pfad_m") or []]           # Ort -> Weg
    if len(P) < 2:
        ctx.melde("HINWEIS", "zugang: kein Fussweg gefunden")
        return
    x, y, s = _g.polylinie_proben(P, 1.0)
    nass = np.asarray(ctx.im_wasser(x, y), bool)
    d = np.hypot(x - ctx.mx, y - ctx.my)
    frei = float(z.get("frei_r_m", 0.6 * float(ctx.st["radius_m"])))
    # vom Ort aus: solange im Kern und nass -> Pfad beginnt erst am Ufer
    k0 = 0
    while k0 < len(x) - 2 and nass[k0] and d[k0] < frei:
        k0 += 1
    pts = [[float(x[k0]), float(y[k0])]] + [p for p in P if np.hypot(p[0] - ctx.mx, p[1] - ctx.my) > d[k0] + 1.0]
    ctx.st["pfad_cm"] = [[round(p[0] * 100), round(p[1] * 100), round(float(ctx.welt.hoehe_bei_m(p[0], p[1])) * 100)]
                         for p in pts]
    ctx.linien["zugang"] = pts[::-1]                                        # Weg -> Ort
    ctx.anker["zugang_ende"] = tuple(pts[0])
    laeufe = []
    for a, b in _nass_laeufe(nass[k0:]):
        a, b = a + k0, b + k0
        a2, b2 = max(k0, a - 3), min(len(x), b + 3)
        laeufe.append([[float(x[i]), float(y[i])] for i in range(a2, b2)])
    ctx._bulten_laeufe = laeufe
    n_nass = int(nass[k0:].sum())
    ctx.melde("HINWEIS", "zugang (Planer, erreichbarkeit): %.0f m, davon %d m nass -> Bultenruecken; Kern %.0f m frei"
              % (float(s[-1] - s[k0]), n_nass, frei))
    if laeufe:
        # Gelaendefenster so legen, dass die nassen Abschnitte drin liegen (<= 400 m)
        g = ctx.r.setdefault("gelaende", {})
        Q = np.asarray([p for l_ in laeufe for p in l_] + [[ctx.mx, ctx.my]])
        x0, y0 = Q.min(axis=0) - 14.0
        x1, y1 = Q.max(axis=0) + 14.0
        fm = g.get("fenster_m") or [2 * (ctx.st["radius_m"] + 25)] * 2
        bx, by = ctx.punkt(g.get("bei", "mitte"))
        x0, x1 = min(x0, bx - fm[1] / 2.0), max(x1, bx + fm[1] / 2.0)
        y0, y1 = min(y0, by - fm[0] / 2.0), max(y1, by + fm[0] / 2.0)
        g["fenster_m"] = [min(400.0, y1 - y0), min(400.0, x1 - x0)]
        g["bei"] = {"pos_m": [(x0 + x1) / 2.0, (y0 + y1) / 2.0]}


def hook_zugang_gelaende(ctx):
    """Bultenruecken: wo der Zugang durch den Epic-See fuehrt, hebt der Stempel einen schmalen Ruecken aus
    Seggenbulten auf Spiegel + ueber_spiegel_m (nur anheben, weich auslaufend) - kein Steg, keine Menschenspur."""
    from sehens_lib import stempel as stm
    laeufe = getattr(ctx, "_bulten_laeufe", None)
    if not laeufe or not ctx.bestand_seen:
        return
    z = ctx.r.get("zugang") or {}
    br = float(z.get("breite_m", 2.2))
    zz = max(s["spiegel_m"] for s in ctx.bestand_seen) + float(z.get("ueber_spiegel_m", 0.22))
    st = ctx.stempel
    for L in laeufe:
        if len(L) < 2:
            continue
        d, _, _ = stm.polylinie_abstand(st.X, st.Y, L)
        w = stm.abfall(d, br / 2.0, br / 2.0 + 1.6)
        st._anwenden(w, ziel=zz, modus="max", name="bultenruecken")
    ctx.linien["bultenruecken"] = [p for L in laeufe for p in L]


def _kette(*hooks):
    """Mehrere Hook-Tabellen zu einer verbinden (Reihenfolge bleibt)."""
    out = {}
    for h in hooks:
        for k, f in h.items():
            if k in out:
                g = out[k]
                out[k] = (lambda g_, f_: (lambda c: (g_(c), f_(c))))(g, f)
            else:
                out[k] = f
    return out


ZUGANG = {"anker": hook_zugang_anker, "nach_gelaende": hook_zugang_gelaende}
HOOKS = {}


def hooks_fuer(oid):
    return _kette(ZUGANG, HOOKS.get(oid, {}))


# ----------------------------------------------------------------------------------------------------------------------
def verdeckung_pruefen(ctx, wp):
    """Regel 'verdeckung' {"probe_r_m", "ziel_hoehe_m"}: Fundstueck MIT Stempel und geplantem Gehoelz pruefen."""
    from sehens_lib import verdeckung
    v = ctx.r.get("verdeckung") or {}
    r = verdeckung.pruefe_ort(ctx, wp, ziel_hoehe_m=v.get("ziel_hoehe_m"), probe_r_m=v.get("probe_r_m"),
                              kern_m=v.get("kern_m"))
    ctx.melde("HINWEIS" if r["verdeckt"] else "WARNUNG", r["text"])
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sehenswuerdigkeiten-Planer Sumpf (Auftrag 13, Phase 2)")
    ap.add_argument("--orte", "--ort", nargs="+", default=None, dest="orte", help="nur diese Ort-IDs (Standard: alle 8)")
    ap.add_argument("--bild", action="store_true", help="Testbild test_<id>.png je geplantem Ort")
    ap.add_argument("--bild-ordner", default=None, help="Ordner fuer test_<id>.png (Standard: --aus)")
    ap.add_argument("--aus", default=None, help="Ausgabeordner (Standard <basis>/export/unreal/welt/sehens/sumpf)")
    ap.add_argument("--sw-aus", default=None, help="Ebene sw_sumpf (Standard: <aus>/sw_sumpf bzw. <basis>/export/unreal/welt/sw_sumpf)")
    ap.add_argument("--basis", default=".", help="production-Wurzel (1-m-Daten in export/unreal/welt)")
    ap.add_argument("--regeln", default=os.path.join(HIER, "sehens_sumpf_regeln.json"))
    ap.add_argument("--inventar", default=None, help="Ordner mit netze.csv, inventar_extra.json (Standard vorlagen/daten)")
    ap.add_argument("--sehens", default=None, help="Ordner antworten/sehens (standorte.json aller Biome)")
    ap.add_argument("--ohne-pruefung", action="store_true")
    ap.add_argument("--ohne-verdeckung", action="store_true", help="Verdeckungsprobe der Fundstuecke auslassen")
    ap.add_argument("--daten2m", default=None, help="2-m-PNGs (Cloud-Test): recherche/vorlagen/daten/sehens")
    ap.add_argument("--daten1m", default=None, help="1-m-Originale (Standard <basis>/export/unreal/welt)")
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    T0 = time.perf_counter()

    from sehens_lib import daten, gelaende, inventar, instanzen, rezept, vorschau, sehens_pruefen, sicht  # noqa: F401
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
    mitten = {oid: (o["mitte_cm"][0] / 100.0, o["mitte_cm"][1] / 100.0) for oid, o in alle.items()}
    wp = None
    kontexte = []
    for oid in planen:
        t0 = time.perf_counter()
        regel = copy.deepcopy(R["orte"][oid])
        ctx = rezept.OrtKontext(welt, gel, inv, ebene, copy.deepcopy(alle[oid]), regel, BIOM, seed=R.get("seed", 0),
                                pfade_biom=pfade_biom, paletten=R.get("paletten"), materialien=R.get("materialwuensche"),
                                orte_mitten=mitten)
        zp = regel.get("zugang_punkte")
        if zp:
            # Zugang neu gefuehrt (z. B. um den neuen Teich herum): Ort -> Weg, relativ zur Mitte; Endpunkt am Weg wie Phase 1
            ctx.st["pfad_cm"] = [[round((ctx.mx + p[0]) * 100), round((ctx.my + p[1]) * 100),
                                  round(float(welt.hoehe_bei_m(ctx.mx + p[0], ctx.my + p[1])) * 100)] for p in zp]
        for h in regel.get("hinweise") or []:
            ctx.melde("HINWEIS", h)
        ctx.baue(hooks_fuer(oid))
        if ctx.pfad and not alle[oid].get("pfad_cm"):
            ctx.pfad["quelle"] = "Planer: kandidaten.erreichbarkeit (Ort -> naechster Weg), am Ort auf das Ufer gekuerzt"
        if zp and ctx.pfad:
            ctx.pfad["quelle"] = "zugang_punkte (Planer: Fussweg aus Phase 1 um das neue Wasser herumgefuehrt)"
        if regel.get("verdeckung") and not a.ohne_verdeckung:
            if wp is None:
                wp = sicht.Wegpunkte(welt, 20)
            r = verdeckung_pruefen(ctx, wp)
            _log("  %s" % r["text"])
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
