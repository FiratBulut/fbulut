#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stufen_vergleich.py - vergleicht die Bach-Stufen zweier Planer-Ausgaben (Auftrag 13g: "Stufen unveraendert
gegenueber 13f").

Aufruf:  python -I stufen_vergleich.py <alt>/orte.json <neu>/orte.json [...weitere Paare]
         oder   python -I stufen_vergleich.py --ordner <alt_wurzel> <neu_wurzel> <muster>
                (<wurzel>/<biom><muster>/orte.json fuer alle 15 Biome, z. B. muster "_basis" bzw. "_k6")

Je Bach (Ort + id) werden die Stufen verglichen: Lippe/Fuss (x, y, z in cm), fall_m und art. Ergebnis je Bach:
  gleich      alle Stufen identisch
  fuss        Lippe, Hoehen und Zahl gleich, nur der Fuss in der Lage <= 60 cm verschoben (13i K5)
  schluss     wie fuss, die Schluss-Stufe am See ist in der letzten Stufe aufgegangen (13i K5)
  verlaengert Stufen des alten Laufs identisch, der neue Lauf hat zusaetzliche Stufen hinter dem alten Ende
  gelaende13h Bach im 13h-Gelaende (Liste GELAENDE_13H, Koordinator 13i-Nachtrag): Stufen folgen dem neuen Gelaende;
              Zahl, Fallhoehen (Summe, groesste) und Lippenversatz werden mit ausgegeben
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


# Koordinator 13i-Nachtrag: diese vier Gletscherbaeche laufen durch Gelaende, das 13h umgebaut hat (Boeschung, Halde,
# Wandverkleidung; gletscher_03 zusaetzlich der getrennte Seeabfluss). Ihre Stufen duerfen sich minimal aendern.
GELAENDE_13H = {("gletscher_01_gletschertor", "gletscherbach"), ("gletscher_03_moraenensee", "firnrinnsal"),
                ("gletscher_03_moraenensee", "seeabfluss"), ("gletscher_05_die_waechte", "muehlenbach")}


def _gelaende_text(a, n, la, ln):
    t = "Gelaendeaenderung 13h: %d -> %d Stufen, Fall Summe %.2f -> %.2f m, groesste %.2f -> %.2f m, Lauf %.1f -> %.1f m" % (
        len(a), len(n), sum(p[2] for p in a), sum(p[2] for p in n), max([p[2] for p in a] + [0]),
        max([p[2] for p in n] + [0]), la or 0, ln or 0)
    if len(a) == len(n):
        lv = [((p[0][0] - q[0][0]) ** 2 + (p[0][1] - q[0][1]) ** 2) ** 0.5 for p, q in zip(a, n)]
        dh = [abs(p[2] - q[2]) for p, q in zip(a, n)]
        t += ", Lippen bis %.0f cm versetzt, %d Fallhoehen geaendert (bis %.2f m)" % (
            max(lv), sum(1 for d in dh if d > 0.011), max(dh))
    return t


def _fuss_weg(p, q):
    return ((p[1][0] - q[1][0]) ** 2 + (p[1][1] - q[1][1]) ** 2) ** 0.5


def _nur_fuss(p, q):
    """Gleiche Lippe (x, y, z) und Hoehen (Fuss-z +-1 cm, Fall +-0,01 m, Art), Fuss in der Lage <= 60 cm verschoben."""
    return p[0] == q[0] and abs(p[1][2] - q[1][2]) <= 1 and abs(p[2] - q[2]) <= 0.011 and p[3] == q[3] and \
        _fuss_weg(p, q) <= 60.0


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
        elif len(a) == len(n) and all(_nur_fuss(p, q) for p, q in zip(a, n)):
            mx = max(_fuss_weg(p, q) for p, q in zip(a, n))
            zeilen.append((k, "fuss", "%d Stufen: Lippe, Hoehen, Zahl gleich; Fuss bis %.0f cm verschoben (13i K5)"
                           % (len(a), mx)))
        elif len(n) == len(a) - 1 and all(_nur_fuss(p, q) for p, q in zip(a[:-2], n[:-1])) and \
                a[-2][0] == n[-1][0] and abs(a[-1][1][2] - n[-1][1][2]) <= 1:
            zeilen.append((k, "schluss", "Schluss-Stufe in der letzten Stufe aufgegangen (Becken davor < 3 m, 13i K5); "
                           "uebrige %d Stufen: Lippe/Hoehen gleich" % (len(n) - 1)))
        elif len(n) > len(a) and n[:len(a)] == a and (N[k]["laenge_m"] or 0) > (A[k]["laenge_m"] or 0):
            zeilen.append((k, "verlaengert", "%d gleiche + %d neue Stufen (Lauf %.1f -> %.1f m)"
                           % (len(a), len(n) - len(a), A[k]["laenge_m"] or 0, N[k]["laenge_m"] or 0)))
        elif k in GELAENDE_13H:
            zeilen.append((k, "gelaende13h", _gelaende_text(a, n, A[k]["laenge_m"], N[k]["laenge_m"])))
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
