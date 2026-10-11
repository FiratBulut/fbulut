#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stufen_vergleich.py - vergleicht die Bach-Stufen zweier Planer-Ausgaben (Auftrag 13g: "Stufen unveraendert
gegenueber 13f").

Aufruf:  python -I stufen_vergleich.py <alt>/orte.json <neu>/orte.json [...weitere Paare]
         oder   python -I stufen_vergleich.py --ordner <alt_wurzel> <neu_wurzel> <muster>
                (<wurzel>/<biom><muster>/orte.json fuer alle 15 Biome, z. B. muster "_basis" bzw. "_k6")

Je Bach (Ort + id) werden die Stufen verglichen: Lippe/Fuss (x, y, z in cm), fall_m und art. Ergebnis je Bach:
  gleich      alle Stufen identisch
  verlaengert Stufen des alten Laufs identisch, der neue Lauf hat zusaetzliche Stufen hinter dem alten Ende
  anders      sonst (mit der ersten Abweichung)
  neu / weg   Bach nur in einer der beiden Ausgaben
Exit-Code 0, wenn kein Bach 'anders' ist.
"""

import json
import os
import sys

BIOME = ["aue", "bergwald", "canyon", "dschungel", "elfenwald", "fjord", "frost", "gletscher", "heide", "kueste",
         "lava", "oedland", "sumpf", "tundra", "wueste"]


def baeche(pfad):
    d = json.load(open(pfad, encoding="utf-8"))
    out = {}
    for o in d.get("orte") or []:
        for w in o.get("wasser") or []:
            if w.get("typ") == "bach":
                st = [(tuple(e["lippe_cm"]), tuple(e["fuss_cm"]), round(float(e["fall_m"]), 2), e.get("art"))
                      for e in w.get("stufen") or []]
                out[(o["id"], w.get("id"))] = {"stufen": st, "ende": tuple(w["punkte_cm"][-1][:2]) if w.get("punkte_cm")
                                               else None, "laenge_m": w.get("laenge_m")}
    return out


def vergleiche(alt, neu):
    A, N = baeche(alt), baeche(neu)
    zeilen = []
    for k in sorted(set(A) | set(N)):
        if k not in N:
            zeilen.append((k, "weg", ""))
            continue
        if k not in A:
            zeilen.append((k, "neu", "%d Stufen" % len(N[k]["stufen"])))
            continue
        a, n = A[k]["stufen"], N[k]["stufen"]
        if a == n:
            zeilen.append((k, "gleich", "%d Stufen" % len(a)))
        elif len(n) > len(a) and n[:len(a)] == a and (N[k]["laenge_m"] or 0) > (A[k]["laenge_m"] or 0):
            zeilen.append((k, "verlaengert", "%d gleiche + %d neue Stufen (Lauf %.1f -> %.1f m)"
                           % (len(a), len(n) - len(a), A[k]["laenge_m"] or 0, N[k]["laenge_m"] or 0)))
        else:
            i = next((j for j in range(min(len(a), len(n))) if a[j] != n[j]), min(len(a), len(n)))
            zeilen.append((k, "anders", "%d -> %d Stufen, erste Abweichung Stufe %d: %s -> %s"
                           % (len(a), len(n), i, a[i] if i < len(a) else "-", n[i] if i < len(n) else "-")))
    return zeilen


def main(argv):
    paare = []
    if argv and argv[0] == "--ordner":
        aw, nw, mu = argv[1], argv[2], argv[3]
        mu_alt = argv[4] if len(argv) > 4 else mu
        for b in BIOME:
            paare.append((b, os.path.join(aw, b + mu_alt, "orte.json"), os.path.join(nw, b + mu, "orte.json")))
    else:
        for i in range(0, len(argv) - 1, 2):
            paare.append((os.path.basename(os.path.dirname(argv[i + 1])), argv[i], argv[i + 1]))
    summe = {}
    anders = 0
    for b, pa, pn in paare:
        for (oid, wid), art, txt in vergleiche(pa, pn):
            summe[art] = summe.get(art, 0) + 1
            if art != "gleich":
                print("%-10s %-34s %-16s %-11s %s" % (b, oid, wid, art, txt))
            anders += art == "anders"
    print("Summe: " + ", ".join("%s %d" % (k, v) for k, v in sorted(summe.items())))
    return 1 if anders else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
