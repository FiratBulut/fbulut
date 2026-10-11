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
    # Entscheidungen 13 (E34, E35, E45): Material-Fix-Ausnahmen, Pivot/Front, Niagara-Kopien
    fa = inv.material_fix_ausnahmen()
    ok(len(fa) > 0 and all(inv.material_fix_ausnahme(p_) for p_ in fa) and not inv.material_fix_ausnahme(
        "SM_NordicBoulder_01"), "E34: %d Eis-/Schnee-Netze ohne Material-Fix" % len(fa))
    nb = inv.netz("SM_NordicBoulder_01")
    ok(all(k in nb for k in ("pivot_z_anteil", "pivot_xy_versatz_m", "front_achse", "front_quelle")),
       "E35: Pivot/Front-Felder (pivot_z_anteil %.2f, front %s/%s)" % (nb["pivot_z_anteil"], nb["front_achse"],
                                                                      nb["front_quelle"]))
    ok(not inv.kopie_pruefen("NS_EL_SW_Test", "NS_Smoke_Plume") and
       any(t == "FEHLER" for t, _ in inv.kopie_pruefen("NS_EL_SW_Test", "/Game/X/NS_Fehlt")) and
       any(t == "FEHLER" for t, _ in inv.kopie_pruefen("NS_Smoke_Plume", "NS_Smoke_Plume")),
       "E45: Niagara-Kopie NS_EL_SW_* mit kopie_von geprueft")
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
                   {"typ": "bach", "id": "ablauf", "abfluss_von": "teich", "laenge_m": 35, "breite_m": 1.0}],
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
    o2["effekte"].append({"typ": "niagara", "asset": "/Game/Eldarien/Welt/FX/Sehens/NS_EL_SW_Test", "pos_cm": [0, 0, 0]})
    o2["bestand_ausblenden"] = [{"art": "bach", "id": "B_Test"}]
    bk = [t for s_, _, t in sehens_pruefen.pruefe_orte(d2, basis=aus, inv=inv, welt=welt, sw_ordner=sw) if s_ == "FEHLER"]
    ok(len(bk) >= 5, "kaputte orte.json: %d FEHLER (Uhrzeigersinn, Niagara fehlt, Budget != Ebene, NS_EL_SW_ ohne "
                     "kopie_von, bestand_ausblenden ohne von/bis)" % len(bk))
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


def _syn_welt_1m(n=420, weg_x=None, eben=False):
    """Kleine synthetische 1-m-Welt in der NW-Ecke der Welt (Zellen 0..n): Kerbtal nach Osten mit Steilstufe,
    flacher Mulde fuer einen See und flachem Unterlauf; optional ein Weg (Nord-Sued) bei x = weg_x (m)."""
    i = np.arange(n, dtype=np.float64)[:, None]
    j = np.arange(n, dtype=np.float64)[None, :]
    X, Y = np.broadcast_arrays(j - daten.OFF_J, i - daten.OFF_I)
    cx, cy = daten.X_MIN_M + n / 2.0, daten.Y_MIN_M + n / 2.0
    dx, dy = X - cx, Y - cy
    # Talboden: flach (5 %) - Steilstufe 60 % (dx -45..-15) - Seemulde (dx 0..35, flach) - Unterlauf 4 %
    boden = np.where(dx < -45, 300.0 - 0.05 * (dx + 45),
                     np.where(dx < -15, 300.0 - 0.6 * (dx + 45),
                              np.where(dx < 40, 282.0 - 0.01 * (dx + 15), 281.45 - 0.04 * (dx - 40))))
    h = (boden + 0.18 * np.abs(dy) + 0.4 * np.sin(dx / 7.0) * np.cos(dy / 9.0)).astype(np.float32)
    if eben:
        h = (200.0 - 0.01 * dx).astype(np.float32)       # schiefe Ebene 1 % (keine natuerlichen Senken)
    z8 = np.zeros((n, n), np.uint8)
    weg = z8.copy()
    if weg_x is not None:
        weg[(np.abs(X - weg_x) <= 1.0)] = 1
    b4 = np.zeros(((n + 3) // 4, (n + 3) // 4), np.uint8)
    w = daten.Welt(1.0, h, np.full((n, n), 1, np.uint8), np.full((n, n), 1, np.uint8), weg, z8.copy(), z8.copy(),
                   b4, b4.copy(), [], [], {}, [], quelle="selbsttest_syn1m")
    return w, cx, cy


def _test_13f(welt2, ort, a):
    """Auftrag 13f: neue Faelle fuer A1/A2 (1-m-Lader), A3 (Baumfuss), A4/A8/A12/A13 (Baeche an Seen, Stufen,
    Querprofil, Furt, Schutzzone) auf einer synthetischen 1-m-Welt, A5 (kleine Senken fuellen), A10 (Feldgrenze).
    Rueckgabe: Zahl der fehlgeschlagenen Pruefungen."""
    import copy
    import json as _json
    from . import inventar, instanzen, rezept, stempel, bach
    fehl = 0

    def ok(bed, text):
        nonlocal fehl
        log("  %s %s" % ("ok  " if bed else "FEHLT", text))
        fehl += 0 if bed else 1

    # --- A1/A2: synthetischer 1-m-Ordner (Biom ueber die Kennzahl, baeche_alle.json bevorzugt)
    d = os.path.join(a.aus, "syn1m_lader")
    os.makedirs(os.path.join(d, "baeche"), exist_ok=True)
    os.makedirs(os.path.join(d, "teiche"), exist_ok=True)
    ny, nx = 16, 24
    (np.arange(ny * nx, dtype="<f4") * 0.01 + 10.0).tofile(os.path.join(d, "hoehe.f32"))
    for k in ("weg", "ort", "wasser"):
        np.zeros(ny * nx, np.uint8).tofile(os.path.join(d, "karte_%s.r8" % k))
    eig = np.zeros((ny, nx), np.uint8)
    eig[:, : nx // 2] = 3
    eig[:, nx // 2:] = 5
    eig.tofile(os.path.join(d, "eigner.r8"))
    kach = [{"kennzahl": 1, "rezept": "aue"}, {"kennzahl": 2, "rezept": "heide"}, {"kennzahl": 3, "rezept": "fjord"},
            {"kennzahl": 4, "rezept": "tundra"}, {"kennzahl": 5, "rezept": None, "name": "VULKAN_REGION"}]
    with open(os.path.join(d, "welt.json"), "w", encoding="utf-8") as f:
        _json.dump({"nx": nx, "ny": ny, "kacheln": kach}, f)
    with open(os.path.join(d, "baeche", "baeche_alle.json"), "w", encoding="utf-8") as f:
        _json.dump({"baeche": [{"id": "B_R2_TEST_01", "punkte": [[0, 0, 1000, 100], [500, 0, 990, 100]]}]}, f)
    with open(os.path.join(d, "baeche", "baeche.json"), "w", encoding="utf-8") as f:
        _json.dump({"baeche": [{"id": "B2_ALT_01", "punkte": [[0, 0, 1000, 100], [500, 0, 990, 100]]}]}, f)
    with open(os.path.join(d, "teiche", "teiche.json"), "w", encoding="utf-8") as f:
        _json.dump({"teiche": []}, f)
    w1 = daten.lade_1m(d, daten2m=a.daten2m, boden=False)
    ok(daten.biom_name(int(w1.biom[0, 0])) == "fjord" and daten.biom_name(int(w1.biom[0, -1])) == "lava",
       "A1 1-m-Lader: Biom ueber die Kennzahl (3 = fjord, 5 ohne Rezept = lava)")
    ok([b["id"] for b in w1.baeche] == ["B_R2_TEST_01"], "A2 1-m-Lader: baeche_alle.json bevorzugt")

    # --- A10: Feldgrenze = Mitte der 1-m-Zelle j = 1008 s (Setzer/Landschaftskomponenten)
    xg = 1008.0 - daten.OFF_J
    yg = 3 * 1008.0 - daten.OFF_I
    ok(daten.feld_von_m(xg - 0.3, 0.0)[0] == "A" and daten.feld_von_m(xg + 0.01, 0.0)[0] == "B"
       and daten.feld_von_cm(round((xg - 0.3) * 100), 0)[0] == "A",
       "A10 Feldgrenze: x = %.1f m (s = floor((x_cm + 473050)/100800))" % xg)
    ok(daten.feld_von_m(0.0, yg - 0.3)[1:] == "3" and daten.feld_von_m(0.0, yg + 0.01)[1:] == "4",
       "A10 Feldgrenze in y: r = floor((y_cm + 406050)/100800) + 1")
    rng = np.random.default_rng(13)
    gut = True
    for _ in range(300):
        x, y = rng.uniform(daten.X_MIN_M, daten.X_MAX_M), rng.uniform(daten.Y_MIN_M, daten.Y_MAX_M)
        f = daten.feld_von_m(x, y)
        x0, y0, x1, y1 = daten.feld_grenzen_m(f)
        gut &= (x0 <= x < x1) and (y0 <= y < y1)
    ok(gut, "A10 feld_grenzen_m passt zu feld_von_m (300 Zufallspunkte; Pruefer nutzt dieselbe Grenze)")

    # --- A3: grosse Baeume (bezug mitte, Fuss >= 1,5 m) am Boden des Pivots
    inv = inventar.Inventar.lade()
    info = inv.netz("Fir_07_Forest")
    q = instanzen.orientierung("aufrecht", 30.0)
    sk = (2.3, 2.3, 2.3)

    def hang(x, y):
        return 100.0 + 0.6 * np.asarray(x, np.float64)

    p = instanzen.platziere(info, 10.0, 5.0, q, sk, hang, 0.5, "mitte")
    bp = float(hang(p["x"] / 100.0, p["y"] / 100.0)) * 100.0
    soll = bp - 50.0 - max(0.0, info["bounds_cm"][0][2] * sk[2])
    ok(p["fuss_r_m"] >= instanzen.FUSS_PIVOT_AB_M and abs(p["z"] - soll) < 1e-6 and p["unterkante_z_m"] <= bp / 100.0,
       "A3 Baum am Hang: z = Boden(Pivot) - eingraben - max(0, bmin_z*sz) (Fuss %.1f m)" % p["fuss_r_m"])
    # --- 13i K2: Pivot in der Netzmitte (wie SM_Fern_02a: bmin_z -25,8 cm bei 52,4 cm Hoehe) -> Unterkante auf den Boden
    info_m = copy.deepcopy(info)
    hz = info["bounds_cm"][1][2] - info["bounds_cm"][0][2]
    info_m["bounds_cm"] = [[info["bounds_cm"][0][0], info["bounds_cm"][0][1], -0.49 * hz],
                           [info["bounds_cm"][1][0], info["bounds_cm"][1][1], 0.51 * hz]]
    pm = instanzen.platziere(info_m, 10.0, 5.0, q, sk, hang, 0.1, "mitte")
    bpm = float(hang(pm["x"] / 100.0, pm["y"] / 100.0)) * 100.0
    ok(abs(pm["unterkante_z_m"] * 100.0 - (bpm - 10.0)) < 1.0,
       "13i K2 Pivot in der Netzmitte: Unterkante = Boden(Pivot) - eingraben (%.2f m statt halb im Boden)"
       % (pm["unterkante_z_m"] - bpm / 100.0))
    # --- 13i K3: Stueck genau auf der Feldgrenze -> 1 cm ins Feld, Feld aus dem float32-Wert
    eb3 = instanzen.Ebene(a.biom, inv, stand="selbsttest")
    y_g = 97949.992
    e3 = eb3.neu("syn", "g", "kleinzeug", "Fir_07_Forest", -100000.0, y_g, 0.0, (0.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0))
    if e3 is not None:
        x0_, y0_, x1_, y1_ = daten.feld_grenzen_m(e3["feld"])
        ok(y0_ * 100.0 + 0.99 <= float(np.float32(e3["y"])) <= y1_ * 100.0 - 0.99,
           "13i K3 Stueck auf der Feldgrenze: %s, y %.2f cm (>= 1 cm im Feld)" % (e3["feld"], e3["y"]))

    # --- A4/A8/A12/A13 auf der synthetischen 1-m-Welt
    welt, cx, cy = _syn_welt_1m(weg_x=None)
    welt_w, _, _ = _syn_welt_1m(weg_x=daten.X_MIN_M + 210.0 + 62.0)
    gel = gelaende.Gelaende(welt, cache=False)
    st_ort = {"id": "%s_01_syn_bach" % a.biom, "name": "Syn", "art": "fundstueck", "radius_m": 40,
              "mitte_cm": [round(cx * 100), round(cy * 100), 28000], "felder": ["A1"], "kameras": []}
    regel = {"kurz": "Selbsttest 13f", "gelaende": {"fenster_m": [140, 200], "bei": [0, 0], "rand_m": 10},
             "wasser": [{"typ": "see", "id": "see", "bei": [18, 0], "spiegel": "boden-0.2", "tiefe_m": 1.5, "farbe": "klar",
                         "becken": {"a_m": 9, "b_m": 6, "richtung": 90, "ufer_m": 4, "freibord_m": 0.4, "auslass": 90}},
                        {"typ": "bach", "id": "zulauf", "von": [-70, 0], "bis_see": "see", "laenge_m": 80, "breite_m": 1.2,
                         "tiefe_cm": 15, "farbe": "klar", "quelle": True},
                        {"typ": "bach", "id": "abfluss", "abfluss_von": "see", "laenge_m": 45, "breite_m": 1.6,
                         "tiefe_cm": 20, "farbe": "klar", "muendung": "versickert",
                         "furt": {"palette": ["SM_flat_rock_04"], "groesse_m": [0.7, 0.9]}}]}
    for name, wl in (("ohne Weg", welt), ("mit Weg (Furt)", welt_w)):
        eb = instanzen.Ebene(a.biom, inv, stand="selbsttest")
        ctx = rezept.OrtKontext(wl, gelaende.Gelaende(wl, cache=False), inv, eb, st_ort, copy.deepcopy(regel), a.biom, seed=3)
        ctx.anker_aufloesen()
        ctx.gelaende_bauen()
        ctx.wasser_bauen()
        ws = {w["id"]: w for w in ctx.wasser}
        see, zu, ab = ws["see"], ws["zulauf"], ws["abfluss"]
        sp = see["spiegel_cm"]
        U = np.asarray(see["umriss_cm"], np.float64) / 100.0
        if name == "ohne Weg":
            ende = zu["punkte_cm"][-1]
            d_um = sehens_pruefen._abstand_umriss(U, ende[0] / 100.0, ende[1] / 100.0)
            drin = rezept._in_polygon(np.array([q_[0] for q_ in zu["punkte_cm"][:-1]]) / 100.0,
                                      np.array([q_[1] for q_ in zu["punkte_cm"][:-1]]) / 100.0, U)
            ok(d_um < 0.5 and ende[2] == sp + 2 and not drin.any(),
               "A4 Zulauf endet auf dem Umriss (%.2f m), Spiegel = See + 2 cm, kein Punkt im See" % d_um)
            ok(ab["punkte_cm"][0][2] == sp and ab.get("abfluss_von") == "see", "A4 Abfluss beginnt auf dem Seespiegel")
            st_ = zu.get("stufen") or []
            ok(len(st_) >= 3 and all(s_["fall_m"] > 0 for s_ in st_), "A8 Zulauf: %d Stufen explizit (Lippe/Fuss)" % len(st_))
            # Becken zwischen den Stufen >= 3 m und <= 3 %
            P = np.asarray(zu["punkte_cm"], np.float64) / 100.0
            kum = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(P[:, 0]), np.diff(P[:, 1])))])
            lip = [kum[int(np.argmin(np.hypot(P[:, 0] - s_["lippe_cm"][0] / 100.0, P[:, 1] - s_["lippe_cm"][1] / 100.0)))]
                   for s_ in st_]
            fus = [kum[int(np.argmin(np.hypot(P[:, 0] - s_["fuss_cm"][0] / 100.0, P[:, 1] - s_["fuss_cm"][1] / 100.0)))]
                   for s_ in st_]
            becken = [(fus[k], lip[k + 1]) for k in range(len(st_) - 1)]
            gef = [(np.interp(b0, kum, P[:, 2]) - np.interp(b1, kum, P[:, 2])) / max(b1 - b0, 1e-6) for b0, b1 in becken]
            ok(all(b1 - b0 >= 3.0 - 1e-6 for b0, b1 in becken) and all(g_ <= 0.03 + 1e-6 for g_ in gef),
               "A8 Becken zwischen den Stufen >= 3 m (min %.1f m) und <= 3 %% (max %.1f %%)"
               % (min([b1 - b0 for b0, b1 in becken] or [0]), 100 * max(gef or [0])))

            class _Boden:
                def hoehe(self, x, y):
                    return ctx.boden(x, y)

            o = {"id": st_ort["id"], "wasser": ctx.wasser}
            bef = sehens_pruefen.pruefe_baeche(o, wl, _Boden())
            ok(not [b_ for b_ in bef if b_[0] == "FEHLER"], "A12 Querprofil (1 m): Pruefer 0 FEHLER (%s)"
               % "; ".join(t for s_, _, t in bef if s_ != "HINWEIS")[:160])
            o2 = copy.deepcopy(o)
            for w_ in o2["wasser"]:
                if w_["id"] == "abfluss":
                    for q_ in w_["punkte_cm"][4:]:
                        q_[2] += 60
                    w_["punkte_cm"] = [q_ for q_ in w_["punkte_cm"]]
                if w_["id"] == "zulauf":
                    w_["punkte_cm"][-1][2] = sp - 30
            bk = [t for s_, _, t in sehens_pruefen.pruefe_baeche(o2, wl, _Boden()) if s_ == "FEHLER"]
            ok(any("Ufer unter dem Spiegel" in t for t in bk) and any("unter dem Spiegel von see" in t for t in bk),
               "A12/A4 kaputt: Ufer unter Spiegel + Muendung unter Seespiegel -> FEHLER (%d)" % len(bk))
            o3 = copy.deepcopy(o)
            for w_ in o3["wasser"]:
                if w_["id"] == "abfluss":
                    for q_ in w_["punkte_cm"][4:]:
                        q_[2] -= 60
            bk3 = [t for s_, _, t in sehens_pruefen.pruefe_baeche(o3, wl, _Boden()) if s_ == "FEHLER"]
            ok(any("Gelaende ueber dem Spiegel" in t for t in bk3), "A12 kaputt: Gelaende ueber dem Spiegel -> FEHLER")
            # 13i K1: Querprofil senkt abseits des Bachs (Netzrand + Uferring + Boeschung + 1 m) nichts > 0,3 m ab
            pa_ = getattr(ctx.stempel, "profil_aussen", {})
            ok(bool(pa_) and all(v_[0] == 0 for v_ in pa_.values()) and
               all((w_.get("profil_absenkung_aussen") or {}).get("flaeche_m2", 0) == 0 for w_ in ctx.wasser),
               "13i K1 Querprofil: keine Absenkung > 0,3 m abseits des Bachs (%d Baeche)" % len(pa_))
            # 13g: Treppenbach (Stufe >= 0,5 m) mit wasser_koerper (river + kaskadennetz, A15/14b), Stufen unveraendert
            wk = zu.get("wasser_koerper") or []
            kn = [k_ for k_ in wk if k_["typ"] == "kaskadennetz"]
            rv = [k_ for k_ in wk if k_["typ"] == "river"]
            st5 = [s_ for s_ in st_ if s_["fall_m"] >= 0.5]
            ok(bool(st5) and bool(kn) and zu.get("wasser_koerper_lauf") == "SW_%s_zulauf" % st_ort["id"]
               and all(len(k_["knick"]) == len(k_["mittellinie"]) and len(k_["mittellinie"][0]) == 8 for k_ in kn)
               and all(r_["s_m"][1] - r_["s_m"][0] >= 15.0 - 1e-3 for r_ in rv),
               "13g wasser_koerper: %d Kaskadennetz(e), %d River >= 15 m, Lauf-ID, mittellinie 8 Felder"
               % (len(kn), len(rv)))
            lip_kn = all(any(k_["s_m"][0] - 0.6 <= lip[i] <= k_["s_m"][1] + 0.6 for k_ in kn)
                         for i, s_ in enumerate(st_) if s_["fall_m"] >= 0.5)
            ok(lip_kn and not [b_ for b_ in bef if b_[0] == "FEHLER" and "KN" in b_[2]],
               "13g jede Stufe >= 0,5 m liegt in einem Netz; Netzregeln (Bett/Ufer/Ueberlappung) 0 FEHLER")
            o4 = copy.deepcopy(o)
            for w_ in o4["wasser"]:
                if w_["id"] == "zulauf":
                    m_ = w_["wasser_koerper"][0].get("mittellinie") or w_["wasser_koerper"][0]["punkte"]
                    m_[-1][2] = m_[0][2] + 50          # Mittellinie steigt
                    w_["wasser_koerper"].append({"id": "x_R9", "typ": "river", "s_m": [70.0, 75.0],
                                                 "punkte": [[0, 0, 0, 100, 10, 80], [500, 0, 0, 100, 10, 80]]})
                if w_["id"] == "abfluss" and w_.get("stufen"):
                    w_["stufen"][0]["fall_m"] = 0.8
                    w_.pop("wasser_koerper", None)
            bk4 = [t for s_, _, t in sehens_pruefen.pruefe_baeche(o4, wl, _Boden()) if s_ == "FEHLER"]
            ok(any("steigt" in t for t in bk4) and any("< 15 m" in t for t in bk4),
               "13g kaputt: Netz-Mittellinie steigt, River < 15 m -> FEHLER (%d)" % len(bk4))
        else:
            fu = ab.get("furten") or []
            n_st = len([e for e in eb.stuecke if e["gruppe"].startswith("furt_")])
            st = ctx.stempel
            schutz = (st.fe.get("weg") > 0)
            dd = gelaende.abstand(schutz, 1.0, 10.0) - 0.5
            ok(len(fu) >= 1 and n_st >= 2, "A13 Furt: Abfluss quert den Weg (%d Furt, %d Trittsteine)" % (len(fu), n_st))
            ok(float(np.abs(st.delta[dd <= 3.0]).max()) == 0.0,
               "A13 Schutzzone 3 m am Weg hart 0 (bis %.2f m ausserhalb)" % float(np.abs(st.delta[(dd > 3.0) & (dd < 4.0)]).max()))

    # --- A5: kleine Senken fuellen (< 50 m2 und < 0,5 m), grosse bleiben
    welt_e, _, _ = _syn_welt_1m(eben=True)
    st = stempel.Stempel.um(welt_e, cx + 18, cy, 80, rand_m=10)
    st.mulde(cx + 5, cy, 2.5, 0.35, rand_m=1.0, boden=0.6)
    st.mulde(cx + 30, cy, 6.0, 1.2, rand_m=2.0, boden=0.6)
    st.fertig(schutz=False, senken_fuellen=True)
    sk = st.senken(min_tiefe_m=0.05)
    m = sk["maske"]
    klein = np.hypot(st.X - (cx + 5), st.Y - cy) < 4.0
    gross = np.hypot(st.X - (cx + 30), st.Y - cy) < 7.0
    ok(st.gefuellt_m2 > 0 and not (m & klein).any() and (m & gross).any(),
       "A5 kleine Senke aufgefuellt (%.0f m2, bis %.2f m), grosse bleibt (Begruendung/Rinne noetig)"
       % (st.gefuellt_m2, st.gefuellt_max_m))
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

    # 11 Auftrag 13f: 1-m-Lader, Feldgrenze, Baumfuss, Baeche an Seen/Stufen/Querprofil/Furt, Senken
    with schritt("11 Auftrag 13f/13g (A1-A5, A8, A10, A12, A13, wasser_koerper)"):
        z11 = _test_13f(welt, orte[0], a)
    z["FEHLER"] += z11
    # 12 Auftrag 13h: Steilflaechen-Regel, Boeschung/Halde, Kameras (Krone, Strahl), Leuchtfeuer, Bloecke im See
    with schritt("12 Auftrag 13h (Steilflaechen, Kameras, Leuchtfeuer, See-Bloecke)"):
        from .selbsttest_13h import test_13h
        z12 = test_13h(welt)
    z["FEHLER"] += z12
    log("-" * 60)
    for u in zeiten:
        log("%-44s %7.2f s" % (u.name, u.sek))
    log("%-44s %7.2f s" % ("GESAMT", time.perf_counter() - T0))
    return 0 if z["FEHLER"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
