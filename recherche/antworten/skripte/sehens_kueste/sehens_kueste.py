#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sehens_kueste.py - Sehenswuerdigkeiten-Planer Kueste (Auftrag 13, Phase 2, nach dem Bergwald-Referenzplaner).

Baut die 8 Kuesten-Orte aus sehens/kueste/standorte.json nach den Rezepten in sehens_kueste_regeln.json
(Katalog sehens/kueste/katalog.md, asset_bedarf.json, Entscheidungen Ferat in sehens-STATUS.md) und schreibt das
Lieferformat vorlagen/SEHENS_FORMAT.md:
  <aus>/orte.json, <aus>/gelaende/<id>.f32, <aus>/lagen/<id>_<Lage>.r8      (§2, §3)
  <sw>/<Feld>/plan.json + <Netz>.f32 (Ebene sw_kueste, FORMAT.md §3)            (§4)
  Wasser §5, Effekte §6 (Niagara optional), Materialwuensche §7, Kameras §8 (aus standorte.json), Budgets §9
  Bild je Ort test_<id>.png (--bild)

Aufruf (python -I, NumPy + Pillow):
  python -I sehens_kueste.py --daten2m recherche/vorlagen/daten/sehens --aus <Ordner> [--ort ID ...] [--bild]
  python -I sehens_kueste.py --basis <production>            # 1 m aus export/unreal/welt, Ausgabe dort
Optionen: --orte/--ort ID ... (nur diese Orte; Orte in denselben Feldern werden mitgeplant, damit plan.json
  vollstaendig bleibt), --bild (test_<id>.png), --bild-ordner, --sw-aus (Ebene sw_kueste), --regeln, --inventar,
  --sehens (Ordner mit <biom>/standorte.json), --cache, --ohne-pruefung, --ohne-verdeckung.
Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.

Ort-spezifischer Code (alles andere steht in den Regeln):
  KuesteKontext._filter  Gruppen-Schluessel "boden_min_m" (nur Akteure): Brandungsbloecke, Stuempfe und Pfeiler stehen
                         auf der gestempelten Brandungsplattform UNTER dem Meeresspiegel (Foliage bleibt bei > -0,3 m,
                         Pruefer-Regel "Instanzen im Meer"); "boden_ab_m": Sicherheitsabstand fuer Foliage an steilen
                         Stempelkanten; Meer (Gelaende nach Stempel < 0) zaehlt fuer den Senken-Check als Wasser.
  hook_tuempel_anker     Gezeitenbank: 8-12 Tuempel (see) zufaellig, aber deterministisch auf der Felsbank verteilt.
  hook_seefall_ende      Seefall: Fallfuss auf Meereshoehe (Schaumkessel ist mit dem Meer verbunden).
  hook_duene             Duenenkamm: Kamm als Wall (Stempel.damm) entlang der Kammlinie, Luv flach, Lee steil.
Nach dem Bauen prueft der Planer fuer die vier Fundstuecke die Verdeckung mit Stempel + Stuecken (verdeckung.py).
Quellen: vorlagen/SEHENS_FORMAT.md, vorlagen/FORMAT.md §3, auftraege/13-, 13b-, 13c-*.md,
antworten/skripte/sehens_lib/ (README.md, PLANER_ANLEITUNG.md), antworten/sehens-STATUS.md.
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

BIOM = "kueste"


def _log(*t):
    from sehens_lib import ascii_text
    sys.stdout.write("[sehens_%s] %s\n" % (BIOM, " ".join(ascii_text(x) for x in t)))
    sys.stdout.flush()


def abbruch(text, code=2):
    _log("FEHLER:", text)
    sys.exit(code)


# ----------------------------------------------------------------------------------------------------------------------
# Kontext mit Meeres-Akteuren
# ----------------------------------------------------------------------------------------------------------------------
def kontext_klasse():
    import numpy as np
    from sehens_lib import rezept

    class KuesteKontext(rezept.OrtKontext):
        """OrtKontext mit "boden_min_m" fuer Akteur-Gruppen: Die Lib sperrt Boden < -0,3 m (Meer) fuer alle Stuecke.
        Pfeilerfuesse, Stuempfe und Brandungsbloecke stehen aber auf der Brandungsplattform (-1 ... -3 m). Akteure
        prueft der Pruefer nicht auf 'Meer' (nur Foliage-Dateien); Foliage bleibt bei der Lib-Regel."""

        def _wasser_maske_fenster(self, fe):
            """Wie die Lib, zusaetzlich das Meer (Gelaende nach dem Stempel < 0 m): Mulden unter dem Meeresspiegel
            (Brandungsplattform, Torgang, Gang des Blaslochs) sind keine 'geschlossenen Senken ohne Wasser'."""
            m = super()._wasser_maske_fenster(fe)
            st = self.stempel
            if st is not None and getattr(st, "delta", None) is not None and st.delta.shape == m.shape:
                m = m | ((st.h0 + st.delta) < 0.0)
            else:
                m = m | (np.asarray(fe.get(self.welt.hoehe)) < 0.0)
            return m

        def _filter(self, g, xs, ys, typ):
            ok = self._filter_meer(g, xs, ys, typ)
            ab = g.get("boden_ab_m")                  # Foliage am Wasser: Sicherheitsabstand zum Meeresspiegel
            if ab is not None and len(xs):
                ok &= np.asarray(self.boden(xs, ys), np.float64) > float(ab)
            return ok

        def _filter_meer(self, g, xs, ys, typ):
            bm = g.get("boden_min_m")
            if bm is None or not g.get("akteur"):
                return super()._filter(g, xs, ys, typ)
            echt = rezept.OrtKontext.boden.__get__(self)
            grenze = float(bm)

            def boden_meer(x, y):
                h = np.asarray(echt(x, y), np.float64)
                return np.where(h > grenze, np.maximum(h, 0.0), h)    # bis boden_min_m gilt als "trocken"

            self.boden = boden_meer
            try:
                return super()._filter(g, xs, ys, typ)
            finally:
                del self.boden

    return KuesteKontext


# ----------------------------------------------------------------------------------------------------------------------
# Hooks (Formen, die sich nicht als Regel ausdruecken lassen)
# ----------------------------------------------------------------------------------------------------------------------
def hook_tuempel_anker(ctx):
    """Gezeitenbank: Tuempel als kleine Seen auf der Felsbank (Regel 'tuempel'). Jeder Tuempel bekommt ein Becken
    (Sohle nur absenken, Uferring ueber dem Spiegel); Spiegel knapp unter der Bankoberflaeche."""
    from sehens_lib import instanzen as ins, stempel as stm
    t = ctx.r["tuempel"]
    rng = ins.rng_fuer(ctx.seed, ctx.id, "tuempel")
    bx, by = ctx.punkt(t.get("bei", "mitte"))
    a, b = float(t["a_m"]), float(t["b_m"])
    ux, uy = stm.kompass_vektor(ctx.richtung(t.get("richtung", 0.0), t.get("bei", "mitte")))
    vx, vy = -uy, ux
    n = int(t.get("anzahl", 10))
    r0, r1 = t.get("r_m", [0.8, 1.8])
    tf0, tf1 = t.get("tiefe_m", [0.3, 0.8])
    ab = float(t.get("abstand_m", 1.2))
    pools = []
    for _ in range(3000):
        if len(pools) >= n:
            break
        r = float(rng.uniform(r0, r1))
        u, v = rng.uniform(-1, 1), rng.uniform(-1, 1)
        rand = float(t.get("rand_m", 2.5)) + r
        if (u * (a - rand) / max(a, 1e-6)) ** 2 + (v * (b - rand) / max(b, 1e-6)) ** 2 > 1.0 or a <= rand or b <= rand:
            continue
        x = bx + u * (a - rand) * ux + v * (b - rand) * vx
        y = by + u * (a - rand) * uy + v * (b - rand) * vy
        if all(math.hypot(x - px, y - py) >= r + pr + ab for px, py, pr in pools):
            pools.append((x, y, r))
    wasser = ctx.r.setdefault("wasser", [])
    for k, (x, y, r) in enumerate(pools):
        ctx.anker["tuempel_%02d" % k] = (x, y)
        ctx._massiv.add(x, y, r + 0.3)            # Felsplatten und Brocken (meide: massiv) lassen die Tuempel frei
        st = float(rng.uniform(1.0, 1.5))
        wasser.append({"typ": "see", "id": "tuempel_%02d" % (k + 1), "bei": {"pos_m": [x, y]},
                       "becken": {"a_m": round(r * st ** 0.5, 2), "b_m": round(r / st ** 0.5, 2),
                                  "richtung": float(rng.uniform(0, 180)), "ufer_m": 1.2, "freibord_m": 0.08,
                                  "boden": 0.35, "auslass": None},
                       "spiegel": t.get("spiegel", "boden-0.1"), "tiefe_m": round(float(rng.uniform(tf0, tf1)), 2),
                       "farbe": t.get("farbe", "klar")})
    ctx.melde("HINWEIS", "Tuempel: %d von %d auf der Felsbank verteilt" % (len(pools), n))


def hook_seefall_ende(ctx):
    """Seefall: Der Fall endet im Schaumkessel, der zum Meer hin offen ist -> Fussz = Meeresspiegel (0 m), nicht der
    gestempelte Kesselgrund."""
    for w in ctx.wasser:
        if w.get("typ") == "wasserfall" and w.get("id") == "seefall":
            fuss = max(0.0, w["fuss_z_cm"] / 100.0)
            w["fuss_z_cm"] = int(round(fuss * 100))
            w["fallhoehe_m"] = round(w["kante_cm"][0][2] / 100.0 - fuss, 1)
            w["hinweis"] = "Fuss im Schaumkessel auf Meereshoehe; Kessel ueber eine Rinne mit dem Meer verbunden"


def hook_duene(ctx):
    """Duenenkamm: Wall entlang der Kammlinie (Stempel.damm, Kosinusprofil), dazu eine flache Luvschuerze zum Meer -
    zusammen Luv ~12 Grad, Lee ~28 Grad. Regel 'duene': linie, breite_m, hoehe_m, krone, luv_breite_m, luv_hoehe_m,
    luv_versatz_m (Richtung 'luv')."""
    from sehens_lib import stempel as stm
    d = ctx.r["duene"]
    P = ctx.linie(d["linie"])
    ctx.stempel.damm(P, float(d["breite_m"]), float(d["hoehe_m"]), krone=float(d.get("krone", 0.2)),
                     verjuengung_m=float(d.get("verjuengung_m", 12.0)))
    if d.get("luv_hoehe_m"):
        lx, ly = stm.kompass_vektor(ctx.richtung(d.get("luv", 90.0)))
        off = float(d.get("luv_versatz_m", 6.0))
        Q = [[p[0] + lx * off, p[1] + ly * off] for p in P]
        ctx.stempel.damm(Q, float(d["luv_breite_m"]), float(d["luv_hoehe_m"]), krone=0.4,
                         verjuengung_m=float(d.get("verjuengung_m", 12.0)))
    ctx.stempel.protokoll.append("damm")


HOOKS = {
    "kueste_04_der_seefall": {"ende": hook_seefall_ende},
    "kueste_05_die_gezeitenbank": {"anker": hook_tuempel_anker},
    "kueste_07_der_duenenkamm": {"nach_gelaende": hook_duene},
}


# ----------------------------------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Sehenswuerdigkeiten-Planer Kueste (Auftrag 13, Phase 2)")
    ap.add_argument("--orte", "--ort", nargs="+", default=None, dest="orte", help="nur diese Ort-IDs (Standard: alle 8)")
    ap.add_argument("--bild", action="store_true", help="Testbild test_<id>.png je geplantem Ort")
    ap.add_argument("--bild-ordner", default=None, help="Ordner fuer test_<id>.png (Standard: --aus)")
    ap.add_argument("--aus", default=None, help="Ausgabeordner (Standard <basis>/export/unreal/welt/sehens/kueste)")
    ap.add_argument("--sw-aus", default=None, help="Ebene sw_kueste (Standard: <aus>/sw_kueste bzw. <basis>/export/unreal/welt/sw_kueste)")
    ap.add_argument("--basis", default=".", help="production-Wurzel (1-m-Daten in export/unreal/welt)")
    ap.add_argument("--regeln", default=os.path.join(HIER, "sehens_kueste_regeln.json"))
    ap.add_argument("--inventar", default=None, help="Ordner mit netze.csv, inventar_extra.json (Standard vorlagen/daten)")
    ap.add_argument("--sehens", default=None, help="Ordner antworten/sehens (standorte.json aller Biome)")
    ap.add_argument("--ohne-pruefung", action="store_true")
    ap.add_argument("--ohne-verdeckung", action="store_true", help="Verdeckungspruefung der Fundstuecke auslassen")
    ap.add_argument("--gruppen", action="store_true", help="je Ort die gesetzten Stuecke je Gruppe ausgeben")
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

    Kontext = kontext_klasse()
    mitten = {o["id"]: (o["mitte_cm"][0] / 100.0, o["mitte_cm"][1] / 100.0) for o in standorte["orte"]}
    ebene = instanzen.Ebene(BIOM, inv, stand=sfmt.heute())
    kontexte = []
    for oid in planen:
        t0 = time.perf_counter()
        regel = copy.deepcopy(R["orte"][oid])
        ctx = Kontext(welt, gel, inv, ebene, alle[oid], regel, BIOM, seed=R.get("seed", 0), pfade_biom=pfade_biom,
                      paletten=R.get("paletten"), materialien=R.get("materialwuensche"), orte_mitten=mitten)
        ctx.baue(HOOKS.get(oid))
        kontexte.append(ctx)
        z = ebene.zaehle(oid)
        _log("%-30s %5d Instanzen (%4d Kollision), %3d Akteure, Stempel %.1f m  %.1f s"
             % (oid, z["instanzen"], z["kollision"], z["akteure"], ctx.stempel.max_aenderung_m, time.perf_counter() - t0))
        if a.gruppen:
            _log("   " + ", ".join("%s %d" % (n, len(s)) for n, s in ctx.gruppen.items()))

    # --- Fundstuecke: Verdeckung mit Stempel + geplanten Stuecken (Katalog: verdeckt durch Kliffkante/Schulter)
    if not a.ohne_verdeckung:
        from sehens_lib import sicht, verdeckung
        wp = None
        for ctx in kontexte:
            if ctx.st.get("art") != "fundstueck" or ctx.id not in gewaehlt:
                continue
            wp = wp or sicht.Wegpunkte(welt, 20)
            vk = (ctx.r.get("verdeckung") or {})
            res = verdeckung.pruefe_ort(ctx, wp, kern_m=ctx.punkt(vk["kern"]) if vk.get("kern") else None,
                                        probe_r_m=vk.get("probe_r_m"))
            _log("%-30s %s" % (ctx.id, res["text"]))
            ctx.melde("HINWEIS" if res["verdeckt"] else "WARNUNG", res["text"])

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
