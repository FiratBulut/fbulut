# -*- coding: utf-8 -*-
"""zuruecklegen_p2.py - 16h Nachtrag 2: Kasten-Statistik und Zuruecklege-Plan fuer Erlenbach p2 aus Ferats Querschnitten
(antworten/fluss_sim/p2_lokal/querschnitte_p2.json). Regeln: bachbett_ufer_regeln.json -> C_ufer.profil.
Optional --fels JSON mit [{s, seite, fels_anteil}] (Fels + Felsplatte vor dem Graben, 0..1), sonst gilt die Regel je
Abschnitt (bergrinne/durchbruch: Fels unbekannt -> nur melden, nicht zuruecklegen).

  python -I recherche/antworten/skripte/ufer_regeln/zuruecklegen_p2.py [--fels DATEI] [--aus DATEI]
"""
import argparse
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import ufer_regeln as u  # noqa: E402

ANTW = os.path.normpath(os.path.join(HIER, "..", ".."))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quer", default=os.path.join(ANTW, "fluss_sim", "p2_lokal", "querschnitte_p2.json"))
    ap.add_argument("--fels", default=None)
    ap.add_argument("--aus", default=os.path.join(ANTW, "ufer_p2", "zuruecklegen_p2.json"))
    a = ap.parse_args(argv)
    R = u.lade()
    Z = R["C_ufer"]["profil"]["zuruecklegen_16h2"]
    Q = json.load(open(a.quer, encoding="utf-8"))["querschnitte"]
    fels = {}
    if a.fels:
        for e in json.load(open(a.fels, encoding="utf-8")):
            fels[(float(e["s"]), e["seite"])] = float(e["fels_anteil"])
    E = []
    for x in Q:
        P = [tuple(p) for p in x["profil"]]
        k_voll = u.kasten_hoehe(P)
        k_nah = u.kasten_nah(P, Z["kasten_d_max_m"])
        neu, ds = u.boeschung_zweistufig(P, 0.0, Z["grad_unten"], Z["h_wechsel_m"], Z["grad_oben"], Z["korridor_max_m"])
        fa = fels.get((float(x["s"]), x["seite"]))
        if fa is None and x["abschnitt"] in Z["fels_unbekannt_nicht_in"]:
            fa = 1.0                       # ohne Lagen-Pruefung: Felsrinne/Durchbruch als Fels behandeln
        E.append({"s": x["s"], "seite": x["seite"], "abschnitt": x["abschnitt"], "kasten_voll_m": k_voll,
                  "kasten_nah_m": k_nah, "kasten": k_nah > Z["kasten_m"], "fels_anteil": fa,
                  "d_schnitt_m": ds, "abtrag_m3": u.abtrag_m3(P, neu) if ds is not None else 0.0,
                  "rest_kasten_m": u.kasten_hoehe([p for p in neu if p[0] <= (ds or Z["korridor_max_m"]) + 1.0])})
    mf = Z["min_folge"]
    sel = set()
    for ab in sorted({e["abschnitt"] for e in E}):
        n = mf.get(ab, mf["standard"]) if isinstance(mf, dict) else int(mf)
        sel |= u.strecken_auswahl([e for e in E if e["abschnitt"] == ab], Z["fels_max"], n)
    zus = {}
    for e in E:
        e["zuruecklegen"] = (e["s"], e["seite"]) in sel and bool(e["d_schnitt_m"])
        e["uferfels"] = (e["s"], e["seite"]) in sel and e["kasten"] and e["d_schnitt_m"] is None
        z = zus.setdefault(e["abschnitt"], {"querschnitte": 0, "kasten_voll": 0, "kasten_nah": 0, "zuruecklegen": 0,
                                             "uferfels": 0, "abtrag_m3": 0.0, "s": []})
        z["querschnitte"] += 1
        z["kasten_voll"] += e["kasten_voll_m"] > Z["kasten_m"]
        z["kasten_nah"] += e["kasten"]
        if e["zuruecklegen"]:
            z["zuruecklegen"] += 1
            z["abtrag_m3"] = round(z["abtrag_m3"] + e["abtrag_m3"], 1)
            z["s"].append([e["s"], e["seite"]])
        if e["uferfels"]:
            z["uferfels"] += 1
    out = {"quelle": os.path.relpath(a.quer, ANTW), "regel": Z, "zusammenfassung": zus,
           "querschnitte": [e for e in E if e["kasten"] or e["kasten_voll_m"] > Z["kasten_m"]]}
    os.makedirs(os.path.dirname(a.aus), exist_ok=True)
    with open(a.aus, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for k, v in zus.items():
        print("%-10s %s" % (k, {kk: vv for kk, vv in v.items() if kk != "s"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
