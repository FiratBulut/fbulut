#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gefaelle_prioritaet.py - Prioritaetenliste der 161 steilen Fluss-/Bachstrecken (Auftrag 15).

Kriterien (Gewichte in GEWICHTE, Begruendung je Strecke im Ergebnis):
  sicht    Sichtlinien vom Weg/Pfad (sehens_lib.sicht, Gelaende + Baeume): Proben alle 10 m entlang der Strecke,
           Ziel 2 m (Stufe/Gischt), Wegpunkte (20-m-Raster, Wege + Pfade aller Biome) bis 300 m. Gezaehlt:
           Wegpunkte, die >= 30 % der Silhouette mindestens einer Probe sehen; naechster solcher Wegpunkt;
           Anteil der Strecke, die von irgendeinem Wegpunkt gesehen wird; kleinster Wegabstand.
  sehens   Naehe zu den 120 Sehenswuerdigkeiten (antworten/sehens/*/standorte.json; Abstand zum Ortsrand) und
           Kameras der Orte (SEHENS_FORMAT §8), die die Strecke im Bild haben (Blickkegel +-35 Grad, Sichtlinie
           frei) - starkes Signal: dort schaut Ferat ohnehin hin.
  physik   Fallhoehe (log), mittleres Gefaelle, Laenge.
Status (statt Score-Abzug bzw. zusaetzlich):
  umgebaut_von_sehens  ein Sehens-Planer baut das Wasser dort selbst um (Bach-Ersatz/Wasserfall/See oder
                       gelaende.ist_wasser in <p2>/<biom>/orte.json, >= 50 % der Strecke oder Rest < 30 m) -> nicht planen
  teilweise_sehens     kleinere Ueberlappung -> planen, Abschnitt am Ort aussparen (Planer)
  gebaut_stufen        schon mit Stufen gebaut (vorlagen/daten/wasser_fx/stufen.json, Auftrag 14), Stufen decken
                       >= 50 % des Falls -> nur Feinschliff
  gebaut_teilweise     einzelne Stufen gebaut (< 50 % des Falls) -> Rest planen, Score x (1 - Anteil), FX abstimmen
  kaum_planbar         < 15 m oder < 30 % der Strecke ausserhalb fester Zonen (gefaelle_plan.feste_zonen: Wege + Uebergang,
                       Orte, Staedte, Sehenswuerdigkeiten Radius + 10 m, Zufluesse) -> kein Pilot
  offen                normal
Pilot = die 20 hoechsten Scores mit Status offen/teilweise_sehens.

Aufruf:  python -I gefaelle_prioritaet.py [--daten2m DIR | --daten1m DIR] [--aus prioritaet.json] [--p2 DIR]
Standard-Ausgabe: recherche/antworten/gefaelle/prioritaet.json
Quellen: auftraege/15-gefaelle-felsstufen-klippen.md, vorlagen/SEHENS_FORMAT.md §8, sehens_lib/README.md.
"""

import argparse
import math
import os
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(HIER))

import numpy as np  # noqa: E402

import gefaelle_daten as gd  # noqa: E402
import gefaelle_plan as gp  # noqa: E402

GEWICHTE = {"sicht": 0.40, "sehens": 0.30, "physik": 0.30}
ZIEL_HOEHE_M = 2.0
SICHT_R_MAX_M = 300.0
PROBE_M = 10.0
KAMERA_KEGEL_GRAD = 35.0
KAMERA_R_MAX_M = 400.0
UMBAU_MIN_ANTEIL = 0.50       # >= 50 % der Strecke baut ein Sehens-Ort um -> ganz auslassen
UMBAU_REST_MIN_M = 30.0       # oder es bleiben < 30 m uebrig
GESTUFT_MIN_ANTEIL = 0.50     # gebaute Stufen decken >= 50 % des Falls -> nur Feinschliff
PLANBAR_MIN_M = 15.0          # ausserhalb fester Zonen (Weg, Ort, Sehenswuerdigkeit, Zufluss) mindestens 15 m ...
PLANBAR_MIN_ANTEIL = 0.30     # ... und 30 % der Strecke, sonst 'kaum_planbar' (kein Pilot)
N_PILOT = 20


def _log(*t):
    from sehens_lib import ascii_text
    sys.stdout.write("[gefaelle_prio] %s\n" % " ".join(ascii_text(str(x)) for x in t))
    sys.stdout.flush()


def gebaut_in_strecke(g, lauf, x):
    """Gebaute Stufen (stufen.json) dieses Laufs, deren Lippe in der Strecke liegt; Anteil am Fall der Strecke."""
    if not g:
        return None
    d = gd.lese_json(gd.STUFEN_FX)
    st = [s for s in d.get("stufen", []) if s["id"] in g["stufen"]]
    drin = []
    for s in st:
        sl, _ = lauf.s_von_m(s["lippe_cm"][0] / 100.0, s["lippe_cm"][1] / 100.0)
        if x["s0_m"] - 5.0 <= sl <= x["s1_m"] + 5.0:
            drin.append(s)
    if not drin:
        return None
    fall = sum(s["fall_m"] for s in drin)
    return {"stufen": [s["id"] for s in drin], "fall_gestuft_m": round(fall, 2),
            "anteil_fall": round(fall / max(x["hoehe_m"], 0.1), 3), "fx_gruppen": g["fx_gruppen"]}


def sicht_strecke(welt, wp, gel, pr):
    from sehens_lib import sicht
    x, y = pr["x"], pr["y"]
    wp_best = {}
    probe_best = np.zeros(len(x))
    for k in range(len(x)):
        idx, d = wp.im_ring(float(x[k]), float(y[k]), 0.0, SICHT_R_MAX_M)
        if not idx.size:
            continue
        an, _, dd = sicht.sichtanteil(welt, wp.x_m[idx], wp.y_m[idx], float(x[k]), float(y[k]), ZIEL_HOEHE_M)
        probe_best[k] = float(an.max())
        for i_, a_, d_ in zip(idx, an, dd):
            b = wp_best.get(int(i_))
            if b is None or a_ > b[0]:
                wp_best[int(i_)] = (float(a_), float(d_))
    sehen = {i: v for i, v in wp_best.items() if v[0] >= 0.3}
    i, j = welt.m_zu_ij(x, y)
    weg_min = float(np.min(gel.abstand_weg[i, j]))
    return {"wegpunkte_im_umkreis": len(wp_best), "wegpunkte_sehen": len(sehen),
            "anteil_wegpunkte": round(len(sehen) / max(len(wp_best), 1), 3),
            "naechste_sicht_m": round(min(v[1] for v in sehen.values()), 1) if sehen else None,
            "anteil_strecke_sichtbar": round(float((probe_best >= 0.3).mean()), 3),
            "weg_abstand_min_m": round(weg_min, 1)}


def kamera_treffer(welt, orte, pr):
    """Kameras der Sehens-Orte, die die Strecke im Blickkegel haben und frei sehen."""
    from sehens_lib import sicht
    x, y = pr["x"], pr["y"]
    treffer = []
    for o in orte:
        for kam in o["kameras"]:
            try:
                _, kx, ky, zx, zy, zz, name, hoch = kam[:8]
            except ValueError:
                continue
            kx, ky, zx, zy, zz = kx / 100.0, ky / 100.0, zx / 100.0, zy / 100.0, zz / 100.0
            d = np.hypot(x - kx, y - ky)
            dz = math.hypot(zx - kx, zy - ky)
            if d.min() > min(KAMERA_R_MAX_M, 1.5 * dz + 60.0):
                continue
            ziel_g = math.degrees(math.atan2(zx - kx, -(zy - ky)))
            g = np.degrees(np.arctan2(x - kx, -(y - ky)))
            diff = np.abs((g - ziel_g + 180.0) % 360.0 - 180.0)
            sel = (diff <= KAMERA_KEGEL_GRAD) & (d <= min(KAMERA_R_MAX_M, 1.5 * dz + 60.0)) & (d >= 3.0)
            if not sel.any():
                continue
            boden = float(welt.hoehe_bei_m(kx, ky))
            ez = boden + abs(hoch) / 100.0 if hoch < 0 else max(boden + hoch / 100.0, zz + 3.0)
            xs, ys = x[sel], y[sel]
            zmin, _ = sicht.mindesthoehe(welt, np.full(len(xs), kx), np.full(len(xs), ky), np.full(len(xs), ez), xs, ys)
            zb = welt.hoehe_bei_m(xs, ys)
            an = np.clip((zb + ZIEL_HOEHE_M - zmin) / ZIEL_HOEHE_M, 0, 1)
            if (an >= 0.3).any():
                treffer.append({"kamera": name, "ort": o["id"], "abstand_m": round(float(d[sel][an >= 0.3].min()), 1)})
    return treffer


def ort_naehe(orte, pr):
    best = None
    for o in orte:
        d = float(np.min(np.hypot(pr["x"] - o["x_m"], pr["y"] - o["y_m"]))) - o["radius_m"]
        if best is None or d < best[0]:
            best = (d, o["id"])
    return {"ort": best[1], "abstand_rand_m": round(max(best[0], 0.0), 1), "abstand_rand_roh_m": round(best[0], 1)}


def scores(e):
    s = e["sicht"]
    if s["wegpunkte_sehen"]:
        sicht = 0.45 * min(1.0, s["wegpunkte_sehen"] / 15.0) + 0.35 * math.exp(-s["naechste_sicht_m"] / 120.0) + \
            0.20 * s["anteil_strecke_sichtbar"]
    else:
        sicht = 0.05 * math.exp(-s["weg_abstand_min_m"] / 300.0)
    k = e["sehens"]
    sehens = min(1.0, 0.45 * len(k["kameras"])) * 0.6 + 0.4 * math.exp(-k["naehe"]["abstand_rand_m"] / 150.0)
    phys = 0.55 * min(1.0, math.log1p(e["fall_m"]) / math.log1p(60.0)) + \
        0.30 * min(1.0, e["gefaelle_mittel"] / 0.30) + 0.15 * min(1.0, e["laenge_m"] / 300.0)
    tot = 100.0 * (GEWICHTE["sicht"] * sicht + GEWICHTE["sehens"] * sehens + GEWICHTE["physik"] * phys)
    if e["status"] == "gebaut_teilweise":       # Stufen teils gebaut -> nur der Rest, mit Auftrag 14 abstimmen
        tot *= 1.0 - e["gebaut"]["anteil_fall"]
    return {"sicht": round(sicht, 3), "sehens": round(sehens, 3), "physik": round(phys, 3), "gesamt": round(tot, 1)}


def begruendung(e):
    t = []
    s = e["sicht"]
    if s["wegpunkte_sehen"]:
        t.append("vom Weg/Pfad sichtbar: %d Wegpunkte (naechster %.0f m), %.0f %% der Strecke"
                 % (s["wegpunkte_sehen"], s["naechste_sicht_m"], 100 * s["anteil_strecke_sichtbar"]))
    else:
        t.append("vom Weg nicht sichtbar (Weg %.0f m)" % s["weg_abstand_min_m"])
    k = e["sehens"]
    if k["kameras"]:
        orte = sorted({c["ort"] for c in k["kameras"]})
        t.append("im Bild von %d Sehens-Kamera(s) (%s)" % (len(k["kameras"]), ", ".join(orte)))
    if k["naehe"]["abstand_rand_m"] <= 150:
        t.append("%.0f m vom Rand von %s" % (k["naehe"]["abstand_rand_m"], k["naehe"]["ort"]))
    t.append("%.1f m Fall auf %.0f m (Mittel %.0f %%, max %.0f %%)" % (e["fall_m"], e["laenge_m"],
                                                                        100 * e["gefaelle_mittel"], 100 * e["gefaelle_max"]))
    if e["status"] == "gebaut_stufen":
        t.append("schon mit Stufen gebaut (%s) - nur Feinschliff, FX aus Auftrag 14 (%s)"
                 % (", ".join(e["gebaut"]["stufen"][:3]) + ("..." if len(e["gebaut"]["stufen"]) > 3 else ""),
                    ", ".join(e["gebaut"]["fx_gruppen"])))
    elif e["status"] == "gebaut_teilweise":
        t.append("teils gestuft gebaut (%s, %.1f m = %.0f %% des Falls) - Rest planen, FX mit Auftrag 14 (%s) abstimmen"
                 % (", ".join(e["gebaut"]["stufen"]), e["gebaut"]["fall_gestuft_m"], 100 * e["gebaut"]["anteil_fall"],
                    ", ".join(e["gebaut"]["fx_gruppen"])))
    elif e["status"] == "kaum_planbar":
        t.append("nur %.0f m ausserhalb fester Zonen (%s) - kein Pilot" % (e.get("planbar_m", 0),
                                                                          ", ".join(e.get("feste_zonen", []))))
    elif e["status"] == "umgebaut_von_sehens":
        t.append("wird von %s umgebaut - nicht doppelt planen" % e["umbau"][0]["ort"])
    elif e["status"] == "teilweise_sehens":
        t.append("beruehrt %s (%.0f m) - Abschnitt aussparen" % (e["umbau"][0]["ort"], e["umbau"][0]["laenge_m"]))
    return "; ".join(t)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Prioritaetenliste der steilen Strecken (Auftrag 15)")
    ap.add_argument("--strecken", default=gd.STRECKEN_STANDARD)
    ap.add_argument("--aus", default=os.path.join(gd.ANTWORTEN, "gefaelle", "prioritaet.json"))
    ap.add_argument("--p2", default=gd.P2_STANDARD, help="Planausgaben der Sehens-Planer (<p2>/<biom>/orte.json)")
    ap.add_argument("--sehens", default=gd.SEHENS_STANDARD)
    ap.add_argument("--pilot", type=int, default=N_PILOT)
    from sehens_lib import daten
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    T0 = time.perf_counter()
    from sehens_lib import gelaende, sicht
    from sehens_lib import format as sfmt
    welt = daten.lade(a.daten2m or (None if a.daten1m else gd.DATEN2M_STANDARD), a.daten1m, pfade=a.sehens)
    gel = gelaende.Gelaende(welt, cache=a.cache)
    wp = sicht.Wegpunkte(welt, 20.0)
    _log(welt.info(), "| Wegpunkte", wp.n)
    strecken, roh = gd.lade_strecken(a.strecken, welt)
    orte = gd.sehens_orte(a.sehens)
    umbau = gd.sehens_umbau(a.p2)
    if not umbau:
        _log("WARNUNG: keine Sehens-Planausgaben in %s - Umbau-Erkennung aus" % a.p2)
    gebaut = gd.gebaute_stufen()
    _log("%d Strecken, %d Sehens-Orte (%d Kameras), %d Orte mit Wasserumbau, gebaut: %s"
         % (len(strecken), len(orte), sum(len(o["kameras"]) for o in orte), len(umbau), ", ".join(gebaut)))
    liste = []
    for n, x in enumerate(strecken):
        lauf = gd.Lauf.aus_welt(welt, x["lauf"])
        pr = lauf.proben(x["s0_m"], x["s1_m"], PROBE_M)
        pr2 = lauf.proben(x["s0_m"], x["s1_m"], 2.0)
        mx, my = float(np.mean(pr["x"])), float(np.mean(pr["y"]))
        e = {"id": x["id"], "lauf": x["lauf"], "art": x["art"], "feld": x["feld"], "biom": welt.biom_bei_m(mx, my),
             "laenge_m": x["laenge_m"], "fall_m": x["hoehe_m"], "gefaelle_mittel": x["gefaelle_mittel"],
             "gefaelle_max": x["gefaelle_max"], "breite_m": x["breite_m"], "s0_m": x["s0_m"], "s1_m": x["s1_m"],
             "mitte_cm": [round(mx * 100), round(my * 100)]}
        e["sicht"] = sicht_strecke(welt, wp, gel, pr)
        e["sehens"] = {"naehe": ort_naehe(orte, pr), "kameras": kamera_treffer(welt, orte, pr)}
        e["umbau"] = gd.umbau_ueberlappung(pr2, umbau)
        e["gebaut"] = gebaut_in_strecke(gebaut.get(x["lauf"]), lauf, x)
        um = sum(u["laenge_m"] for u in e["umbau"])
        if e["gebaut"] and e["gebaut"]["anteil_fall"] >= GESTUFT_MIN_ANTEIL:
            e["status"] = "gebaut_stufen"
        elif e["gebaut"]:
            e["status"] = "gebaut_teilweise"
        elif e["umbau"] and (um >= UMBAU_MIN_ANTEIL * x["laenge_m"] or x["laenge_m"] - um < UMBAU_REST_MIN_M):
            e["status"] = "umgebaut_von_sehens"
        elif e["umbau"]:
            e["status"] = "teilweise_sehens"
        else:
            e["status"] = "offen"
        if e["status"] in ("offen", "teilweise_sehens", "gebaut_teilweise"):
            pl, gr_ = gp.planbarer_anteil(lauf, welt, gel, orte, umbau, welt.wasser_welt, welt.baeche,
                                          x["s0_m"], x["s1_m"])
            e["planbar_m"] = round(pl, 1)
            e["feste_zonen"] = sorted({g[2] for g in gr_})
            if pl < PLANBAR_MIN_M or pl < PLANBAR_MIN_ANTEIL * x["laenge_m"]:
                e["status"] = "kaum_planbar"
        e["score"] = scores(e)
        liste.append(e)
        if (n + 1) % 20 == 0:
            _log("%d/%d  %.0f s" % (n + 1, len(strecken), time.perf_counter() - T0))
    liste.sort(key=lambda e: (-e["score"]["gesamt"], e["id"]))
    rang = 0
    pilot = []
    for e in liste:
        rang += 1
        e["rang"] = rang
        e["pilot"] = e["status"] in ("offen", "teilweise_sehens", "gebaut_teilweise") and len(pilot) < a.pilot
        if e["pilot"]:
            pilot.append(e["id"])
        e["begruendung"] = begruendung(e)
    out = {"stand": sfmt.heute(), "auftrag": "15 - steile Fluss-/Bachstrecken: Prioritaet",
           "erzeugt_von": "recherche/antworten/skripte/gefaelle/gefaelle_prioritaet.py",
           "daten": welt.quelle.split(":")[0], "strecken_quelle": "vorlagen/daten/gefaelle/steile_strecken.json (%s)"
           % roh.get("stand"),
           "kriterien": {"gewichte": GEWICHTE, "ziel_hoehe_m": ZIEL_HOEHE_M, "sicht_r_max_m": SICHT_R_MAX_M,
                         "probe_m": PROBE_M, "kamera_kegel_grad": KAMERA_KEGEL_GRAD,
                         "umbau_min_anteil": UMBAU_MIN_ANTEIL, "umbau_rest_min_m": UMBAU_REST_MIN_M,
                         "gestuft_min_anteil": GESTUFT_MIN_ANTEIL,
                         "sicht": "0,45 min(1, Wegpunkte/15) + 0,35 exp(-naechste/120 m) + 0,2 Anteil sichtbar",
                         "sehens": "0,6 min(1, 0,45 Kameras) + 0,4 exp(-Abstand Ortsrand/150 m)",
                         "physik": "0,55 log(1+Fall)/log(61) + 0,3 min(1, Gefaelle/0,3) + 0,15 min(1, Laenge/300 m)"},
           "status_anzahl": {s: sum(1 for e in liste if e["status"] == s)
                             for s in ("offen", "teilweise_sehens", "umgebaut_von_sehens", "gebaut_teilweise",
                                       "gebaut_stufen", "kaum_planbar")},
           "pilot": pilot, "strecken": liste}
    os.makedirs(os.path.dirname(os.path.abspath(a.aus)), exist_ok=True)
    with open(a.aus, "w", encoding="utf-8") as f:
        import json
        json.dump(out, f, ensure_ascii=False, indent=1)
    _log("geschrieben:", a.aus, "| Status", out["status_anzahl"], "| %.0f s" % (time.perf_counter() - T0))
    for e in liste[:30]:
        _log("%3d %-28s %-9s %5.1f %s %s" % (e["rang"], e["id"], e["status"][:9], e["score"]["gesamt"],
                                              "PILOT" if e["pilot"] else "     ", e["begruendung"][:120]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
