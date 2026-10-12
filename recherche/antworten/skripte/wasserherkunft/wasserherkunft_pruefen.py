# -*- coding: utf-8 -*-
"""wasserherkunft_pruefen.py - VORSCHLAG der Pruefregel "Ein Fall braucht nachweisbare Herkunft" (Auftrag 17).

Nicht in Planer/Pruefer eingebaut (Folgeauftrag). Liest faelle_herkunft.json (wasserherkunft.py) und meldet je Fall:

  FEHLER   H1  keine sichtbare Herkunft: weniger als 30 m Wasser oberhalb und kein Quellmerkmal
               (See/Teich/Topf, Schnee/Eis im Einzugsgebiet, geplante Quelle)
  FEHLER   H2  Einzugsgebiet unter dem Mindestwert (Breite x 5 l/s je m x 0,1 / Abflussspende des Bioms, mindest_ha)
               UND kein Quellmerkmal (Karstquelle/Quellaustritt/Schneefeld zaehlen als Merkmal)
  WARNUNG  H3  sonst V = Abfluss / Bedarf < 0,1 (Wasser reicht nur fuer einen schmaleren Fall: breite_passend_m)
  HINWEIS  H4  Gewaesser beginnt weniger als 30 m oberhalb der Lippe (Quelle direkt an der Kante)
  HINWEIS  H5  (nicht plausibel) Gipfel >= 80 m ueber der Lippe auf Insel/Waldbiom: Wolkenkappe/Nebel als Erklaerung moeglich

Aufruf:  python -I wasserherkunft_pruefen.py recherche/antworten/wasserherkunft/faelle_herkunft.json [--nur-fehler]
Exit-Code 1 bei FEHLER.
"""

import argparse
import collections
import json
import math
import os
import sys

REGELN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wasserherkunft_regeln.json")
SEK_JAHR = 365.25 * 86400.0


def mindest_ha(breite_m, biom, R):
    """Mindest-Einzugsgebiet (ha) fuer einen geschlossenen Vorhang dieser Breite im Biom, mit Spielfaktor:
    A = Breite x q_vorhang x v_plausibel / Abflussspende(Biom). q_vorhang nach Poleni (h = 2 cm) ~ 5 l/s je m."""
    F = R["fall"]
    q_m = 2.0 / 3.0 * F["mu"] * math.sqrt(2 * 9.81) * F["h_vorhang_m"] ** 1.5        # m3/s je m Breite
    spende = R["niederschlag_mm_a"].get(biom, 1000) * R["abflussbeiwert"].get(biom, 0.5) / 1000.0 / SEK_JAHR
    if spende <= 0:
        return float("inf")
    return breite_m * q_m * R["bewertung"]["v_plausibel"] / spende / 1e4


def pruefe(f, R):
    out = []
    qm = f.get("quellmerkmale") or []
    B = R["bewertung"]
    if not f.get("herkunft_sichtbar"):
        out.append(("FEHLER", "H1", "keine sichtbare Herkunft (Wasser oberhalb %.0f m < %.0f m, kein Quellmerkmal)"
                    % (f.get("wasser_oberhalb_m") or 0, B["wasser_oberhalb_min_m"])))
    b = f.get("breite_m") or R["fall"]["breite_standard_m"]
    amin = mindest_ha(b, f.get("biom"), R)
    h2 = (f.get("einzugsgebiet_ha") or 0) < amin and not qm
    if h2:
        out.append(("FEHLER", "H2", "Einzugsgebiet %.2f ha < %.1f ha (Mindestwert %s, %.1f m breit) und kein Quellmerkmal"
                    % (f.get("einzugsgebiet_ha") or 0, amin, f.get("biom"), b)))
    if not h2 and (f.get("verhaeltnis") or 0) < B["v_plausibel"]:
        out.append(("WARNUNG", "H3", "Abfluss %.2f l/s fuer Bedarf %.1f l/s (V = %.3f): Wasser reicht fuer ~%.2f m Breite"
                    % (f.get("abfluss_mittel_l_s") or 0, f.get("bedarf_vorhang_l_s") or 0, f.get("verhaeltnis") or 0,
                       f.get("breite_passend_m") or 0)))
    wo = f.get("wasser_oberhalb") or {}
    if (f.get("wasser_oberhalb_m") or 0) < B["wasser_oberhalb_min_m"] and wo.get("anfang_art") in (None, "quelle"):
        out.append(("HINWEIS", "H4", "Wasser beginnt %.0f m oberhalb der Lippe" % (f.get("wasser_oberhalb_m") or 0)))
    if f.get("bewertung") != "plausibel" and (f.get("gipfel_ueber_lippe_m") or 0) >= R["gipfel"]["nebel_ab_m"] and (
            f.get("insel") or f.get("biom") in ("dschungel", "elfenwald", "kueste", "lava", "bergwald", "fjord")):
        out.append(("HINWEIS", "H5", "Gipfel %.0f m ueber der Lippe: Nebel/Wolkenkappe als Wasserquelle zeigen"
                    % f["gipfel_ueber_lippe_m"]))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pruefregel nachweisbare Herkunft (Vorschlag)")
    ap.add_argument("datei")
    ap.add_argument("--nur-fehler", action="store_true")
    ap.add_argument("--regeln", default=REGELN)
    a = ap.parse_args(argv)
    with open(a.regeln, "r", encoding="utf-8") as fh:
        R = json.load(fh)
    with open(a.datei, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    z = collections.Counter()
    for f in d["faelle"]:
        for stufe, code, text in pruefe(f, R):
            z[(stufe, code)] += 1
            if a.nur_fehler and stufe != "FEHLER":
                continue
            print("%-7s %s %-55s %s" % (stufe, code, f["id"][:55], text))
    print("Summe: " + ", ".join("%s %s: %d" % (s, c, n) for (s, c), n in sorted(z.items())))
    return 1 if any(s == "FEHLER" for s, _ in z) else 0


if __name__ == "__main__":
    sys.exit(main())
