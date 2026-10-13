#!/usr/bin/env python3
"""felsdeckung_hochrechnung.py - Hochrechnung des Pilot-Regelwerks (Auftrag 21) auf alle Felder (Antwort Tabelle d).

Aufruf (Repo-Wurzel):
  python -I recherche/antworten/skripte/felsdeckung/felsdeckung_hochrechnung.py --plan recherche/antworten/felsdeckung
Schreibt <plan>/hochrechnung_felder.json.

Verfahren: Zonen (gleiche Funktion wie der Planer) je 1008-m-Feld aus den Weltdaten; Raten = Stuecke je ha Zone aus dem
Pilotplan (Mittelpunkt-Zone je Stueck, je Thema, Akteure getrennt); Biomfaktor (regeln.biome: deckung fuer Fels-Themen,
baeume fuer baumgruppen) nach dem vorherrschenden Biom des Felds (vorlagen/daten/biome_je_feld.json). Wuesten-Felder
C3-E5 mit eigenem Planer: Faktor wueste. Speicher: Bytes je Instanz als Spanne (siehe Antwort d).
"""

import argparse
import copy
import json
import math
import os
import sys

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
SKRIPTE = os.path.normpath(os.path.join(HIER, ".."))
for p in (SKRIPTE, HIER):
    if p not in sys.path:
        sys.path.insert(0, p)

from sehens_lib import daten as D          # noqa: E402
from sehens_lib import inventar as INV     # noqa: E402
import felsdeckung_plan as FP              # noqa: E402
import felsdeckung_pruefen as PR           # noqa: E402

BYTES_JE_INSTANZ = (200, 600)    # Editor+Laufzeit je Foliage-Instanz (ISM-Daten 64 B GPU + Foliage/HISM/Undo), Spanne


ZIELZONEN = {"halde": ("halde",), "klippenband": ("schrofen", "wand"), "platten": ("fuss",),
             "baumgruppen": ("fuss", "hangwald", "halde", "schrofen")}


def raten(plan, regeln, welt, inv):
    """Stuecke je ha der Zielzonen des Themas (Mittelpunkte, die in Nachbarzonen fallen, zaehlen mit)."""
    K = FP.Kontext(welt, regeln)
    th = PR.lies_themen(plan, regeln["pilot"]["feld"])
    fl = {name: float(((K.zone == code) & K.innen).sum() * K.z * K.z) / 1e4 for name, code in FP.ZONEN.items()}
    out = {}
    for thema, t in th.items():
        p, arr = t
        n_i = sum(d["anzahl"] for d in p["dateien"].values() if not d.get("akteur"))
        n_a = sum(d["anzahl"] for d in p["dateien"].values() if d.get("akteur"))
        ha = sum(fl[z] for z in ZIELZONEN[thema])
        out[thema] = {"inst": n_i / ha, "akteur": n_a / ha, "zonen": list(ZIELZONEN[thema])}
    return out, fl


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--regeln", default=os.path.join(HIER, "felsdeckung_regeln.json"))
    ap.add_argument("--daten2m", default=None)
    ap.add_argument("--daten1m", default=None)
    a = ap.parse_args(argv)
    with open(a.regeln, "r", encoding="utf-8") as f:
        regeln = json.load(f)
    welt = D.lade(daten2m=a.daten2m, daten1m=a.daten1m, pfade=False)
    inv = INV.Inventar.lade()
    r, fl_pilot = raten(a.plan, regeln, welt, inv)
    bj = os.path.join(SKRIPTE, "..", "..", "vorlagen", "daten", "biome_je_feld.json")
    with open(bj, "r", encoding="utf-8") as f:
        biome = json.load(f)
    felder = biome.get("felder", biome) if isinstance(biome, dict) else {}
    erg = {}
    for s_ in range(10):
        for z_ in range(1, 8):
            feld = "ABCDEFGHIJ"[s_] + str(z_)
            x0, y0, x1, y1 = D.feld_grenzen_m(feld)
            R = copy.deepcopy(regeln)
            R["pilot"]["fenster_m"] = [x0, y0, x1, y1]
            R["pilot"]["feld"] = feld
            try:
                K = FP.Kontext(welt, R)
            except Exception:
                continue
            land = float(((K.h > 0.2) & K.innen).sum() * K.z * K.z) / 1e4
            if land < 1.0:
                continue
            fl = {name: round(float(((K.zone == code) & K.innen).sum() * K.z * K.z) / 1e4, 2) for name, code in FP.ZONEN.items()}
            info = felder.get(feld) if isinstance(felder, dict) else None
            bdom = "bergwald"
            if isinstance(info, dict):
                bb = info.get("biome_prozent") or info.get("biome") or {}
                if isinstance(bb, dict) and bb:
                    bdom = max(bb.items(), key=lambda kv: kv[1])[0]
                elif isinstance(bb, list) and bb:
                    bdom = bb[0][0] if isinstance(bb[0], (list, tuple)) else str(bb[0])
            fak = regeln["biome"].get(bdom, {"deckung": 0.5, "baeume": 0.5})
            inst = {}
            ak = 0.0
            for thema, rr in r.items():
                f_ = fak["baeume"] if thema == "baumgruppen" else fak["deckung"]
                ha = sum(fl[z] for z in rr["zonen"])
                inst[thema] = int(round(rr["inst"] * ha * f_))
                ak += rr["akteur"] * ha * f_
            summe = sum(inst.values())
            erg[feld] = {"biom": bdom, "land_ha": round(land, 1), "zonen_ha": fl, "instanzen": inst, "summe": summe,
                         "akteure": int(round(ak)),
                         "ram_mb": [round(summe * BYTES_JE_INSTANZ[0] / 1e6, 1), round(summe * BYTES_JE_INSTANZ[1] / 1e6, 1)]}
    welt_summe = sum(v["summe"] for v in erg.values())
    top = sorted(erg.items(), key=lambda kv: -kv[1]["summe"])[:12]
    out = {"stand": FP.STAND, "raten_je_ha_zielzone": {t: {"inst": round(rr["inst"], 1), "akteur": round(rr["akteur"], 3), "zonen": rr["zonen"]}
                                                       for t, rr in r.items()},
           "zonen_codes": FP.ZONEN, "pilot_zonen_ha": {k: round(v, 2) for k, v in fl_pilot.items()},
           "bytes_je_instanz": BYTES_JE_INSTANZ, "welt_summe": welt_summe,
           "welt_zonen_ha": {n: round(sum(v["zonen_ha"][n] for v in erg.values()), 1) for n in FP.ZONEN},
           "top12": [[k, v["summe"], v["akteure"], v["biom"]] for k, v in top], "felder": erg}
    with open(os.path.join(a.plan, "hochrechnung_felder.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("Welt: %d neue Instanzen; Top: %s" % (welt_summe, ", ".join("%s %d" % (k, s) for k, s, _, _ in out["top12"])))
    print("Zonen Welt ha:", out["welt_zonen_ha"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
