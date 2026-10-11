"""selbsttest.py - Selbsttest der sehens_lib auf den echten 2-m-Daten.

  python -I antworten/skripte/sehens_lib/selbsttest.py [--biom bergwald] [--aus <Ordner>] [--cache <Ordner>]
  (oder: cd antworten/skripte && python -m sehens_lib.selbsttest)

Schritte: Laden -> Ganze-Welt-Raster (Cache) -> Hang/Abfluss fuer ein Feld -> 10 Kandidaten im Biom ->
Sicht/Verdeckung/Blickposition fuer 3 -> Erreichbarkeit -> Kameras + standorte.json + Pruefer ->
1 Draufsicht + Biom-Uebersicht -> Pfade (Testpfad rastern, Abstaende, Pfad-Pruefer, Ruecksetzen). Ausgaben NUR nach --aus (Standard: Scratchpad a13/), nie ins Repo.
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
    log("-" * 60)
    for u in zeiten:
        log("%-44s %7.2f s" % (u.name, u.sek))
    log("%-44s %7.2f s" % ("GESAMT", time.perf_counter() - T0))
    return 0 if z["FEHLER"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
