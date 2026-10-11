"""selbsttest.py - Selbsttest der sehens_lib auf den echten 2-m-Daten.

  python -I antworten/skripte/sehens_lib/selbsttest.py [--biom bergwald] [--aus <Ordner>] [--cache <Ordner>]
  (oder: cd antworten/skripte && python -m sehens_lib.selbsttest)

Schritte: Laden -> Ganze-Welt-Raster (Cache) -> Hang/Abfluss fuer ein Feld -> 10 Kandidaten im Biom ->
Sicht/Verdeckung/Blickposition fuer 3 -> Erreichbarkeit -> Kameras + standorte.json + Pruefer ->
1 Draufsicht + Biom-Uebersicht -> Pfade (Testpfad rastern, Abstaende, Pfad-Pruefer, Ruecksetzen) -> Phase 2 (Inventar-
Pruefung, Quaternionen, Stempel mit allen Werkzeugen, Ort aus Rezept zweimal = byteidentisch, orte.json + sw_<biom>,
Vorschau, Pruefer 0 FEHLER, absichtlich kaputte Faelle). Ausgaben NUR nach --aus (Standard: Scratchpad a13/), nie ins Repo.
"""

import os
import sys
import time

if __name__ == "__main__" and __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "sehens_lib"
    import sehens_lib  # noqa: F401

import numpy as np  # noqa: E402

from . import log, Uhr  # noqa: E402
from . import daten, gelaende, sicht, kandidaten, zeichnen, sehens_pruefen  # noqa: E402
from . import format as sfmt  # noqa: E402

STANDARD_AUS = os.path.join(os.path.dirname(gelaende.STANDARD_CACHE), "")


def _pfad_test(welt, gel, c, e, a):
    """Testpfad: Fussweg des Testorts umgedreht (Weg -> Ort), die letzten 100 m vor dem Ort weggelassen.
    Prueft Rastern (welt.weg / weg_basis), Abstaende, pruefe_pfad (gueltig + absichtlich kaputt), Ruecksetzen.
    Rueckgabe: Zahl der fehlgeschlagenen Pruefungen."""
    fehl = 0

    def ok(bed, text):
        nonlocal fehl
        log("  %s %s" % ("ok  " if bed else "FEHLT", text))
        fehl += 0 if bed else 1

    alt_pfade = list(welt.pfade)
    pm = [p[:2] for p in (e.get("pfad_m") or [])][::-1]
    pm = [p for p in pm if np.hypot(p[0] - c["x_m"], p[1] - c["y_m"]) >= 100.0] or pm[:2]
    if len(pm) < 2:   # kein Fussweg -> gerade Linie vom naechsten Wegpunkt aus
        wx, wy = welt.flat_zu_m(int(gel.weg_naechst[welt.m_zu_ij(c["x_m"], c["y_m"])]))
        pm = [[float(wx), float(wy)], [float(wx + 0.5 * (c["x_m"] - wx)), float(wy + 0.5 * (c["y_m"] - wy))]]
    n_wp0 = sicht.Wegpunkte(welt, 20).n
    p = sfmt.pfad("%s_pfad_selbsttest" % a.biom, "trampelpfad", pm, welt=welt, anschluss="Selbsttest",
                  fuer=["%s_01_test_ort_1" % a.biom])
    log("  Testpfad %d Punkte, %.0f m, max %.1f Grad" % (len(pm), p["laenge_m"], p["max_steigung_grad"]))
    welt.setze_pfade(alt_pfade + [p])
    gel2 = gelaende.Gelaende(welt, cache=a.cache)
    ok(gel2.cache == gel.cache, "Pfade aendern den Cache-Ordner nicht (nur abstand_weg_p<Kennung>)")
    xm, ym = pm[-1]
    i, j = welt.m_zu_ij(xm, ym)
    ok(welt.weg[i, j] > 0 and welt.pfade_aktiv(), "Pfadende ist Weg (welt.weg > 0, Pfade aktiv)")
    ok(float(gel2.abstand_weg[i, j]) < 3.0, "abstand_weg am Pfadende %.1f m (mit Pfaden)" % gel2.abstand_weg[i, j])
    ok(float(gel2.abstand_weg_basis[i, j]) >= 60.0,
       "abstand_weg_basis (ohne Pfade) am Pfadende %.0f m" % gel2.abstand_weg_basis[i, j])
    wp2 = sicht.Wegpunkte(welt, 20)
    ok(wp2.n > n_wp0, "Wegpunkte fuer Sicht: %d -> %d mit Testpfad" % (n_wp0, wp2.n))
    bef = sehens_pruefen.pruefe_pfad(p, a.biom, welt, gel2, welt.pfade)
    ok(not any(s == sehens_pruefen.FEHLER for s, _, _ in bef), "gueltiger Testpfad ohne FEHLER")
    kaputt = dict(p, id="falsch", art="strasse", breite_cm=300,
                  punkte_cm=[[q[0] + 20000, q[1]] for q in p["punkte_cm"]])
    bk = [t for s, _, t in sehens_pruefen.pruefe_pfad(kaputt, a.biom, welt, gel2, welt.pfade)
          if s == sehens_pruefen.FEHLER]
    ok(len(bk) >= 4, "kaputter Pfad: %d FEHLER (id, art, breite, Anschluss)" % len(bk))
    d = {"biom": a.biom, "orte": [{"id": "%s_01_x" % a.biom, "pfad_id": "%s_pfad_gibtsnicht" % a.biom}],
         "pfade": [p]}
    bo = sehens_pruefen.pruefe_pfade_datei(d, a.biom, welt, gel2)
    ok(any(s == sehens_pruefen.FEHLER and "pfad_id" in t for s, _, t in bo), "unbekannte pfad_id -> FEHLER")
    welt.setze_pfade(alt_pfade)
    ok((welt.weg is welt.weg_basis) == (not alt_pfade), "Ruecksetzen auf den alten Pfadstand")
    return fehl


def _phase2_test(welt, gel, ort, a):
    """Phase 2 (Auftrag 13): Stempel (alle Werkzeuge), Lagen, Instanzen (Streuung, Gruppen, Kontakt, Akteure),
    Wasser, Effekte, Klaenge, Pfad, orte.json + sw_<biom>, Vorschau, Pruefer; danach absichtlich kaputte Faelle.
    Rueckgabe: Zahl der fehlgeschlagenen Pruefungen."""
    import copy
    import json as _json
    from . import inventar, instanzen, rezept, vorschau, stempel
    fehl = 0

    def ok(bed, text):
        nonlocal fehl
        log("  %s %s" % ("ok  " if bed else "FEHLT", text))
        fehl += 0 if bed else 1

    inv = inventar.Inventar.lade()
    ok(len(inv.netze) > 1000 and len(inv.niagara) > 0, "Inventar: %d Netze, %d Niagara, %d Decals, %d Klaenge (Beispiele)"
       % (len(inv.netze), len(inv.niagara), len(inv.decals), len(inv.klaenge)))
    ok(any(t == "FEHLER" for t, _ in inv.netz_pruefen("SM_GibtEsNicht_99")), "unbekanntes Netz -> FEHLER")
    ok(all(t != "FEHLER" for t, _ in inv.netz_pruefen("SM_NordicBoulder_01", optional=True)), "bekanntes Netz ok")
    ok(any(t == "HINWEIS" for t, _ in inv.asset_pruefen("niagara", "/Game/X/NS_Fehlt", optional=True)),
       "fehlendes Niagara mit optional -> HINWEIS")
    ok(any(t == "FEHLER" for t, _ in inv.asset_pruefen("niagara", "/Game/X/NS_Fehlt")), "fehlendes Niagara -> FEHLER")
    ok(any(t == "FEHLER" for t, _ in inv.netz_pruefen("SW_Houdini_Test")), "Houdini SW_* -> FEHLER")
    ok(any(t == "FEHLER" for t, _ in inv.material_pruefen({"name": "MI_EL_SW_X", "basis": "M_EL_Fels_MS",
                                                         "parameter": {"GibtEsNicht": 1}})), "Materialparameter unbekannt -> FEHLER")
    # Quaternion-Selbstpruefung: liegend legt die Z-Achse in Kompassrichtung 90 (Ost = +X)
    q = instanzen.orientierung("liegend", 90.0)
    v = instanzen.q_drehe(q, [0, 0, 1])
    ok(abs(v[0] - 1) < 1e-6 and abs(v[2]) < 1e-6, "orientierung liegend: Z -> Ost (%.2f, %.2f, %.2f)" % tuple(v))
    q = instanzen.orientierung("aufrecht", 180.0)
    v = instanzen.q_drehe(q, [1, 0, 0])
    ok(abs(v[1] - 1) < 1e-6, "orientierung aufrecht: Front +X -> Sued (+Y)")
    # Stempel: alle Werkzeuge
    x, y = ort["mitte_cm"][0] / 100.0, ort["mitte_cm"][1] / 100.0
    st = stempel.Stempel.um(welt, x, y, 140, rand_m=10)
    st.mulde(x + 20, y + 20, 8, 2.0)
    st.kuppe(x - 20, y + 10, 6, 3.0)
    st.rinne([[x - 30, y - 30], [x, y - 40], [x + 30, y - 30]], 3, 1.5)
    st.terrasse(x, y, 6, float(welt.hoehe_bei_m(x, y)), 5)
    st.abbruch([[x - 40, y + 30], [x - 10, y + 40]], 4.0, seite="links")
    st.buckel(x + 30, y - 10, 12, 0.6)
    st.glaetten(x, y, 10, 0.5)
    um = st.see_becken(x + 25, y - 25, 6, 4, 30.0, float(welt.hoehe_bei_m(x + 25, y - 25)), 1.5, auslass_grad=90.0)
    st.fertig()
    rand = np.concatenate([st.delta[0], st.delta[-1], st.delta[:, 0], st.delta[:, -1]])
    ok(np.abs(rand).max() < 1e-6 and st.max_aenderung_m > 1.0,
       "Stempel: 8 Werkzeuge, Rand = 0, max %.1f m" % st.max_aenderung_m)
    ok(stempel.flaeche(um) > 0, "see_becken-Umriss gegen den Uhrzeigersinn (Flaeche > 0)")
    blk = st.schreibe(os.path.join(a.aus, "phase2_stempel"), "test")
    fi = blk["fenster_ij"]
    ok(os.path.getsize(os.path.join(a.aus, "phase2_stempel", blk["datei"])) == fi[2] * fi[3] * 4,
       "gelaende f32 im 1-m-Raster: %d x %d" % (fi[2], fi[3]))
    # Ort mit Rezept (kleiner Bergwald-Ausschnitt), zweimal -> deterministisch
    regel = {
        "kurz": "Selbsttest", "marker": {"titel": "Test", "text": "Selbsttest-Ort."},
        "anker": {"kopf": {"suche": "hoechster", "r_m": 10}, "unten": {"von": "kopf", "richtung": "hangab", "abstand_m": 25}},
        "gelaende": {"fenster_m": [100, 100], "ops": [{"op": "mulde", "bei": "unten", "radius_m": 6, "tiefe_m": 1.0}]},
        "wasser": [{"typ": "see", "id": "teich", "bei": "unten", "r_m": 5, "spiegel": "boden", "tiefe_m": 1.2,
                    "farbe": "klar", "becken": {"ufer_m": 4}},
                   {"typ": "bach", "id": "ablauf", "abfluss_von": "teich", "laenge_m": 20, "breite_m": 1.0}],
        "gruppen": [
            {"name": "held", "ebene": "held", "netz": "SM_NordicBoulder_01", "verteilung": {"typ": "punkt", "bei": "kopf"},
             "skala": 1.2},
            {"name": "begleit", "ebene": "begleiter", "palette": ["SM_Big_Rock_01", "SM_Big_Rock_02"], "anzahl": 4,
             "verteilung": {"typ": "ring", "bei": "kopf", "r_m": [6, 12]}},
            {"name": "schutt", "ebene": "schutt", "palette": ["SM_mountain_rock_big_01_1", "SM_ground_rock_01"],
             "anzahl": 40, "verteilung": {"typ": "faecher", "bei": "kopf", "richtung": "hangab", "laenge_m": 25},
             "abstand_m": 0.8, "gradient": {"von": 0.8, "bis": 1.4}},
            {"name": "kies", "ebene": "kleinzeug", "palette": ["SM_stone_04", "SM_stone_06"], "anzahl": 200,
             "verteilung": {"typ": "kreis", "bei": "kopf", "r_m": 15}, "abstand_m": 0.3, "rolle": "stein"},
            {"name": "baum", "ebene": "bewuchs", "netz": "SM_dwarf_pine_big_01", "anzahl": 3,
             "verteilung": {"typ": "ring", "bei": "kopf", "r_m": [12, 20]}, "rolle": "baum"},
            {"name": "moos", "ebene": "kontakt", "palette": ["SM_moss_01"], "rolle": "streu",
             "verteilung": {"typ": "um_gruppe", "gruppe": ["held", "begleit"], "ring": [0.9, 1.3], "je": [3, 5], "seite": "nord"}},
            {"name": "uferkies", "ebene": "kontakt", "palette": ["SM_stone_05"], "dichte_je_m2": 0.3, "rolle": "stein",
             "verteilung": {"typ": "ufer", "bei": "unten", "r_m": 15, "band_m": [0, 2]}}],
        "lagen": [{"lage": "Kies", "form": "ring", "bei": "kopf", "r_m": [4, 9], "wert": 200, "flecken": 0.4},
                  {"lage": "Moos", "form": "um_gruppe", "gruppe": "begleit", "ring": [0.8, 1.5], "wert": 170}],
        "pfad": {"breite_cm": 130, "trittsteine": {"palette": ["SM_flat_rock_04"], "stufen_ab_grad": 25}},
        "effekte": [{"typ": "lokaler_nebel", "bei": "unten", "hoehe_m": 2, "radius_m": 10, "dichte": 0.05},
                    {"typ": "punktlicht", "bei": "kopf", "hoehe_m": 2, "intensitaet_cd": 200, "radius_m": 8},
                    {"typ": "niagara", "asset": "NS_Smoke_Plume", "optional": True},
                    {"typ": "decal", "material": "MI_Leakage_04", "bei": "kopf"}],
        "klaenge": [{"asset": "CUE_Water_Stream_V_Cue", "bei": "unten"}]}
    erg = []
    for lauf in (1, 2):
        aus = os.path.join(a.aus, "phase2_lauf%d" % lauf)
        eb = instanzen.Ebene(a.biom, inv, stand="selbsttest")
        ctx = rezept.OrtKontext(welt, gel, inv, eb, ort, copy.deepcopy(regel), a.biom, seed=7)
        ctx.baue()
        d, info = rezept.schreibe_biom(aus, os.path.join(aus, "sw_" + a.biom), a.biom, [ctx], eb,
                                       [{"name": "MI_EL_SW_Test", "basis": "M_EL_Fels_MS", "parameter": {"Nass_Dunkel": 0.5}}],
                                       inv, stand="selbsttest")
        erg.append((aus, d, ctx))
    (aus, d, ctx), (aus2, _, _) = erg
    gleich = all(open(os.path.join(r, f), "rb").read() == open(os.path.join(r.replace(aus, aus2), f), "rb").read()
                 for r, _, fs in os.walk(aus) for f in fs)
    ok(gleich, "zwei Laeufe byteidentisch (deterministisch)")
    o = d["orte"][0]
    de = o["detail_ebenen"]
    ok(all(k in de for k in ("held", "begleiter", "schutt", "kleinzeug", "bewuchs", "kontakt")),
       "Detail-Ebenen: %s" % ", ".join("%s %d" % (k, v["anzahl"]) for k, v in de.items()))
    ok(o["budget"]["instanzen"] > 100 and o["budget"]["lichter"] == 1 and o["budget"]["niagara"] == 1,
       "Budget %s" % _json.dumps(o["budget"]))
    ok(any(w["typ"] == "see" for w in o["wasser"]) and any(w["typ"] == "bach" for w in o["wasser"]), "Wasser see + bach")
    ok("pfad" in o and o["pfad"]["art"] in ("trampelpfad", "serpentine"), "Pfad (13c) aus pfad_cm: %s, %s m"
       % (o.get("pfad", {}).get("art"), o.get("pfad", {}).get("laenge_m")))
    p = vorschau.vorschau(ctx, os.path.join(a.aus, "phase2_test.png"))
    ok(os.path.exists(p), "Vorschau %s" % p)
    sw = os.path.join(aus, "sw_" + a.biom)
    bef = sehens_pruefen.pruefe_orte(d, basis=aus, inv=inv, welt=welt, sw_ordner=sw)
    z = sehens_pruefen.melde(bef, "phase2 orte.json + sw")
    ok(z["FEHLER"] == 0, "Pruefer Phase 2: 0 FEHLER")
    # absichtlich kaputt
    d2 = copy.deepcopy(d)
    o2 = d2["orte"][0]
    see = [w for w in o2["wasser"] if w["typ"] == "see"][0]
    see["umriss_cm"] = see["umriss_cm"][::-1]
    o2["effekte"].append({"typ": "niagara", "asset": "/Game/X/NS_Fehlt", "pos_cm": [0, 0, 0]})
    o2["budget"]["instanzen"] += 5
    bk = [t for s_, _, t in sehens_pruefen.pruefe_orte(d2, basis=aus, inv=inv, welt=welt, sw_ordner=sw) if s_ == "FEHLER"]
    ok(len(bk) >= 3, "kaputte orte.json: %d FEHLER (Uhrzeigersinn, Niagara fehlt, Budget != Ebene)" % len(bk))
    feld = sorted(os.listdir(sw))[0]
    pj = os.path.join(sw, feld, "plan.json")
    with open(pj, "r", encoding="utf-8") as f:
        plan = _json.load(f)
    k = sorted(plan["dateien"])[0]
    plan["dateien"][k]["anzahl"] += 1
    plan["dateien"]["SM_GibtEsNicht"] = {"pfad": "/Game/X/SM_GibtEsNicht", "anzahl": 1, "sichtweite": [0, 0], "kollision": False}
    with open(pj, "w", encoding="utf-8") as f:
        _json.dump(plan, f)
    be = [t for s_, _, t in sehens_pruefen.pruefe_ebene(sw, a.biom, inv, d["orte"], welt, aus) if s_ == "FEHLER"]
    ok(len(be) >= 2, "kaputte Ebene: %d FEHLER (anzahl, fehlende Datei/Netz)" % len(be))
    return fehl


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Selbsttest sehens_lib")
    ap.add_argument("--biom", default="bergwald")
    ap.add_argument("--feld", default="B4")
    ap.add_argument("--aus", default=STANDARD_AUS)
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    repo = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    if os.path.abspath(a.aus).startswith(repo + os.sep):
        log("Abbruch: --aus liegt im Repo (%s) - bitte Scratchpad/temp verwenden" % a.aus)
        return 2
    os.makedirs(a.aus, exist_ok=True)
    zeiten = []
    T0 = time.perf_counter()

    def schritt(name):
        u = Uhr(name)
        zeiten.append(u)
        return u

    with schritt("1 Laden (2 m)"):
        welt = daten.lade(a.daten2m, a.daten1m)
    log(welt.info())
    with schritt("2 Ganze-Welt-Raster (Cache)"):
        gel = gelaende.Gelaende(welt, cache=a.cache)
        gel.vorrechnen()
        _ = gel.biom_abstand(a.biom), gel.landformen()
    log("Cache-Ordner:", gel.cache)

    # 3 Hang/Abfluss fuer ein Feld (lokal gerechnet, Vergleich mit Ganze-Welt-Cache)
    with schritt("3 Hang/Abfluss Feld %s (lokal)" % a.feld):
        x0, y0, x1, y1 = daten.feld_grenzen_m(a.feld)
        fe = welt.fenster_box(x0, y0, x1, y1)
        h = fe.get("hoehe")
        ng = gelaende.hangneigung(h, welt.zelle_m)
        r = gelaende.abfluss(h, welt.zelle_m, fe.get("meer"))
        kr = gelaende.kruemmung_mehrskalig(h, welt.zelle_m, (10, 25, 50))
    acc = r["akkumulation_m2"]
    log("  Feld %s: %dx%d Zellen, Hang Mittel %.1f / max %.1f Grad, Einzugsflaeche max %.0f m2, "
        "%d Becken gefuellt, Profilkruemmung(25 m) %.4f..%.4f 1/m"
        % (a.feld, h.shape[1], h.shape[0], float(ng.mean()), float(ng.max()), float(acc.max()),
           r["becken_zahl"], float(kr[25][0].min()), float(kr[25][0].max())))
    st = gel.stufen(maske=welt.biom_maske(a.biom))
    log("  Gefaellsspruenge im Biom %s: %d (groesster Fall %.1f m)"
        % (a.biom, st["idx"].size, float(st["fall_m"].max()) if st["idx"].size else 0.0))
    kp = gel.kuppen(maske=welt.biom_maske(a.biom))
    ks = gel.kessel(maske=welt.biom_maske(a.biom))
    log("  Kuppen: %d, Kessel: %d, Gerinne-Anfaenge (>= 5000 m2) welt: %d"
        % (kp["idx"].size, ks["idx"].size, gel.gerinne_anfaenge(5000).size))

    # 4 Kandidaten
    belegt = sfmt.belegte_punkte(os.path.join(repo, "antworten", "sehens"), ausser_biom=a.biom)
    with schritt("4 10 Kandidaten (%s)" % a.biom):
        liste = kandidaten.kandidaten(welt, gel, a.biom, kandidaten.score_praegnanz, n=10, belegt=belegt)
    for k, c in enumerate(liste, 1):
        log("  K%02d %s x=%7.1f y=%7.1f z=%6.1f Weg %5.1f m  Hang %4.1f  TPI100 %5.1f  %-22s score %.3f"
            % (k, c["feld"], c["x_m"], c["y_m"], c["z_m"], c["abstand_weg_m"], c["neigung_grad"],
               c["tpi100_m"], c["landform"], c["score"]))
    if not liste:
        log("FEHLER: keine Kandidaten")
        return 1

    # 5 Sicht
    with schritt("5a Wegpunkte (20 m)"):
        wp = sicht.Wegpunkte(welt, 20.0)
    log("  %d Wegpunkte" % wp.n)
    drei = liste[:3]
    with schritt("5b Sicht fuer 3 (Ring 300-800 m, H 15 m)"):
        sichten = [sicht.sicht_von_wegen(welt, wp, c["x_m"], c["y_m"], 15.0) for c in drei]
    with schritt("5c Verdeckung + Blickposition fuer 3"):
        verd = [sicht.verdeckt_vom_weg(welt, wp, c["x_m"], c["y_m"], 3.0) for c in drei]
        blick = [sicht.beste_blickposition(welt, c["x_m"], c["y_m"], 15.0, gel=gel, anzahl=1) for c in drei]
    for c, s, v, b in zip(drei, sichten, verd, blick):
        log("  (%.0f, %.0f): %d/%d Wegpunkte sehen >= 30 %% (bis %.0f m), mittlerer Anteil %.2f; "
            "Fundstueck-verdeckt=%s (max %.2f); Held-Blick %s"
            % (c["x_m"], c["y_m"], s["n_sichtbar"], s["n_wegpunkte"], s["sichtbar_ab_m"], s["mittel_anteil"],
               v["verdeckt"], v["max_anteil"],
               ("%.0f m, %.0f Grad, Anteil %.2f" % (b[0]["abstand_m"], b[0]["richtung_grad"], b[0]["anteil"]))
               if b else "-"))

    # 6 Erreichbarkeit
    with schritt("6 Erreichbarkeit fuer 3 (Dijkstra 4 m)"):
        err = [kandidaten.erreichbarkeit(welt, gel, c["x_m"], c["y_m"]) for c in drei]
    for c, e in zip(drei, err):
        log("  (%.0f, %.0f): %s, Modus %s, Laenge %s m (Luftlinie %s), max %s Grad, steil %s m, quer-steil %s m, "
            "Wasser %s m, %d Pfadpunkte"
            % (c["x_m"], c["y_m"], "erreichbar" if e["erreichbar"] else "PFAD NOETIG", e["modus"],
               e.get("laenge_m"), e.get("luftlinie_m"), e.get("max_steigung_grad"), e.get("steil_laenge_m"),
               e.get("quer_steil_laenge_m"), e.get("wasser_laenge_m"), len(e.get("pfad_m", []))))

    # 7 Kameras + standorte.json + Pruefer
    with schritt("7 Kameras + standorte.json + Pruefer"):
        orte = []
        for k, (c, s, e) in enumerate(zip(drei, sichten, err), 1):
            art = "leuchtfeuer" if s["n_sichtbar"] > 0 else "fundstueck"
            oid = sfmt.ort_id(a.biom, k, "test_ort_%d" % k)
            pfad = [p[:2] for p in e.get("pfad_m", [])]
            kams = sicht.kameras_vorschlagen(welt, wp, oid, c["x_m"], c["y_m"], art, 15.0, gel=gel,
                                             pfad_m=pfad or None, sicht=s)
            orte.append(sfmt.standort(oid, "Testort %d" % k, art, c["x_m"], c["y_m"], 40, kams, welt=welt,
                                      ziel_hoehe_m=15, standort_begruendung="Selbsttest (%s)" % c["landform"],
                                      sicht={"naechster_weg_m": c["abstand_weg_m"],
                                             "sichtbar_ab_m": s["sichtbar_ab_m"],
                                             "wegpunkte_sichtbar": s["n_sichtbar"]},
                                      erreichbar={kk: e.get(kk) for kk in ("erreichbar", "modus", "laenge_m",
                                                                           "max_steigung_grad")},
                                      pfad_cm=e.get("pfad_cm", [])))
        pf = os.path.join(a.aus, "selbsttest_%s" % a.biom, "standorte.json")
        d = sfmt.schreibe_standorte(pf, a.biom, orte, pruefen=False)
        bef = sehens_pruefen.pruefe_standorte(d, welt, gel)
        z = sehens_pruefen.melde(bef, "selbsttest standorte.json")

    # 8 Draufsicht + Uebersicht
    with schritt("8 Draufsicht 1 Ort + Biom-Uebersicht"):
        o = orte[0]
        c = drei[0]
        el = [{"typ": "kreis", "pos_m": [c["x_m"], c["y_m"]], "radius_m": o["radius_m"], "farbe": "#ff3030",
               "name": "Ort (Radius %d m)" % o["radius_m"]},
              {"typ": "punkt", "pos_m": [c["x_m"], c["y_m"]], "farbe": "#ff3030", "name": "Held (geplant)"}]
        if err[0].get("pfad_m"):
            el.append({"typ": "linie", "punkte_m": [p[:2] for p in err[0]["pfad_m"]], "farbe": "#ffffff",
                       "breite": 2, "name": "Zugang (%s)" % err[0]["modus"]})
        for kk in range(min(5, st["idx"].size)):
            if np.hypot(st["x_m"][kk] - c["x_m"], st["y_m"][kk] - c["y_m"]) < 300:
                el.append({"typ": "punkt", "pos_m": [float(st["x_m"][kk]), float(st["y_m"][kk])],
                           "farbe": "#30c0ff", "name": "Gefaellssprung %.0f m" % st["fall_m"][kk]})
        bild = zeichnen.draufsicht(welt, c["x_m"], c["y_m"], os.path.join(a.aus, "%s.png" % o["id"]),
                                   groesse_m=500, skala=2, elemente=el, kameras=o["kameras"],
                                   titel=o["id"], untertitel=o["art"], gel=gel)
        ueb = zeichnen.uebersicht(welt, os.path.join(a.aus, "uebersicht_%s.png" % a.biom), biom=a.biom,
                                  punkte=[{"x_m": cc["x_m"], "y_m": cc["y_m"], "name": "K%d" % n}
                                          for n, cc in enumerate(liste, 1)])
    log("Draufsicht:", bild)
    log("Uebersicht:", ueb)

    # 9 Pfade (Auftrag 13c): Testpfad vom Weg Richtung Ort 1 rastern, Abstaende, Pruefer
    with schritt("9 Pfade (rastern, Abstand, Pruefer)"):
        z9 = _pfad_test(welt, gel, drei[0], err[0], a)
    z["FEHLER"] += z9

    # 10 Phase 2: Stempel, Lagen, Instanzen, Wasser, Effekte, Pfad, orte.json, Ebene, Vorschau, Pruefer
    with schritt("10 Phase 2 (Stempel, Instanzen, Pruefer)"):
        z10 = _phase2_test(welt, gel, orte[0], a)
    z["FEHLER"] += z10
    log("-" * 60)
    for u in zeiten:
        log("%-44s %7.2f s" % (u.name, u.sek))
    log("%-44s %7.2f s" % ("GESAMT", time.perf_counter() - T0))
    return 0 if z["FEHLER"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
