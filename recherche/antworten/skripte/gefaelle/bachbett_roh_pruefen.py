# -*- coding: utf-8 -*-
"""bachbett_roh_pruefen.py - Pruefer der Roh-Lauf-Ebene (bachbett_roh.py, Auftrag 16c Nachtrag 3).

Je <aus>/<lauf>/plan.json (art bachbett_roh | bachbett_rest):
  - Format: art, Lauflinie (spiegel_neu_cm/_s_m gleich lang, Spiegel nie steigend), KEINE Stufen, KEIN Gelaende
    (kein gelaende/-Ordner, abschnitte[].gelaende leer) - FEHLER;
  - Instanz-Ebene wie die Gefaelle-Plaene (sehens_pruefen.pruefe_ebene, Kontext gefaelle: Format, Inventar, Saegeschnitt,
    Feldrechteck, Budget je Abschnitt, Schweben, Weg; nichts auf Ortsflaechen), keine Akteure (FEHLER);
  - Bachbett wie gefaelle_pruefen.pruefe_bachbett: Liste <-> Ebene, Kollision des grossen Holzes am Wasser,
    Dichte im Rahmen nach Waldnaehe (nachgerechnet, mit Treibholz vom Oberlauf), Uferstreifen >= 80 % der Uferzellen;
  - Felsen: gelistete Felsen in der Ebene, Bloecke >= kollision_ab_m mit Kollision, Dichte >= pruef_min_je_100m je
    Segment ab 30 m (ausser in Feldern mit lokaler Ufer-Ebene) - FEHLER;
  - kein Totholz in Feldern mit lokaler Ufer-Ebene (bachbett.totholz_ohne_felder, 16c Nachtrag 4) - FEHLER;
  - nichts in Sehenswuerdigkeiten (Radius + 10 m) und nichts in den ausgesparten Bereichen (Achse, +-1 m) - FEHLER.

Aufruf: python -I recherche/antworten/skripte/gefaelle/bachbett_roh_pruefen.py <aus> [--daten2m DIR | --daten1m DIR]
        [--laeufe ID ...]   (Exit 1 bei FEHLER)
"""

import argparse
import math
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(HIER))

import numpy as np  # noqa: E402

import gefaelle_daten as gd  # noqa: E402
import gefaelle_pruefen as gpr  # noqa: E402
import gefaelle_regelwerk as gr  # noqa: E402

FEHLER, WARNUNG, HINWEIS = gpr.FEHLER, gpr.WARNUNG, gpr.HINWEIS


def pruefe_lauf(ordner, welt=None, inv=None, rw=None, orte=None):
    from sehens_lib import bachbett as bb
    pj = os.path.join(ordner, "plan.json")
    tag = os.path.basename(os.path.normpath(ordner))
    b = []
    if not os.path.exists(pj):
        return [(FEHLER, tag, "plan.json fehlt")]
    p = gd.lese_json(pj)
    R = bb.regeln()
    if p.get("art") not in ("bachbett_roh", "bachbett_rest"):
        b.append((FEHLER, tag, "art %r (erwartet bachbett_roh/bachbett_rest)" % p.get("art")))
    if p.get("stufen"):
        b.append((FEHLER, tag, "Roh-Lauf mit Stufen (16c Nachtrag 3: Stufen werden nicht erfunden)"))
    if os.path.isdir(os.path.join(ordner, "gelaende")) or any(a.get("gelaende") for a in p.get("abschnitte") or []):
        b.append((FEHLER, tag, "Roh-Lauf mit Gelaendeaenderung (nur Instanzen und Lagen erlaubt)"))
    N = np.asarray(p.get("spiegel_neu_cm") or [], np.float64)
    S = np.asarray(p.get("spiegel_neu_s_m") or [], np.float64)
    if len(N) < 2 or len(N) != len(S):
        b.append((FEHLER, tag, "Lauflinie spiegel_neu_cm/_s_m fehlt oder ungleich lang"))
        return b
    if (np.diff(N[:, 2]) > 0.05).any():
        b.append((FEHLER, tag, "Spiegel steigt an %d Stellen" % int((np.diff(N[:, 2]) > 0.05).sum())))
    if not p.get("abschnitte"):
        b.append((HINWEIS, tag, p.get("hinweis", "kein Bachbett")))
        return b
    if (p.get("instanzen") or {}).get("akteure") or p.get("akteure"):
        b.append((FEHLER, tag, "Roh-Ebene mit Akteuren (nur Instanzen)"))
    gpr.pruefe_instanzen(p, ordner, welt, inv, b, tag)
    gpr.pruefe_bachbett(p, ordner, welt, inv, rw, b, tag, None)
    # Felsen
    F = R.a["roh"]["felsen"]
    io = os.path.join(ordner, (p.get("instanzen") or {}).get("ordner", "instanzen"))
    idx = gpr._ebene_index(io) if os.path.isdir(io) else []
    je_netz = {}
    for r in idx:
        je_netz.setdefault(r[0], []).append(r)
    P = N[:, :2] / 100.0
    cum = gpr._s_entlang(p["spiegel_neu_cm"])
    ohne = set((p.get("bachbett") or {}).get("felsen_ohne_felder") or [])
    from sehens_lib import daten as _d
    alle_pos = []
    for aid, blk in sorted(((p.get("bachbett") or {}).get("abschnitte") or {}).items()):
        n_fehlt, n_kol = 0, 0
        fs = blk.get("felsen") or []
        for st in fs:
            k = [r for r in je_netz.get(st["netz"], []) if abs(r[2] - st["pos_cm"][0]) <= 2.0 and
                 abs(r[3] - st["pos_cm"][1]) <= 2.0 and abs(r[4] - st["pos_cm"][2]) <= 2.0]
            if not k:
                n_fehlt += 1
                continue
            if st["art"] in ("fels_ufer", "fels_wasser") and st["lage"] in ("wasser", "ufer") and not k[0][1]:
                g = inv.netz(k[0][7] or st["pfad"])["groesse_m"] if inv is not None else [0, 0, 0]
                if max(g) * max(k[0][6]) >= float(F["kollision_ab_m"]) + 0.05:
                    n_kol += 1
        if n_fehlt:
            b.append((FEHLER, aid, "Felsen: %d von %d gelisteten Felsen nicht in der Instanz-Ebene" % (n_fehlt, len(fs))))
        if n_kol:
            b.append((FEHLER, aid, "Felsen: %d Bloecke >= %.1f m am Wasser ohne Kollision" % (n_kol, float(F["kollision_ab_m"]))))
        for seg in blk.get("felsen_bilanz") or []:
            a_, b_ = seg["s_m"]
            L = b_ - a_
            n = sum(1 for st in fs if a_ - 1.0 <= st["s_m"] <= b_ + 1.0 and st["art"] != "fels_kies")
            sx, sy = np.interp((a_ + b_) / 2.0, S, P[:, 0]), np.interp((a_ + b_) / 2.0, S, P[:, 1])
            if L >= 30.0 and _d.feld_von_m(float(sx), float(sy)) not in ohne and \
                    100.0 * n / L < float(F["pruef_min_je_100m"]) and not seg.get("ohne"):
                b.append((FEHLER, aid, "Felsen %.0f-%.0f m: %.1f Ufer-/Stoersteine je 100 m (< %.1f)"
                          % (a_, b_, 100.0 * n / L, float(F["pruef_min_je_100m"]))))
        # 16c Nachtrag 4: kein Totholz in Feldern mit lokaler Ufer-Ebene (die hat dort schon Treibholz)
        ohne_th = set((p.get("bachbett") or {}).get("totholz_ohne_felder") or [])
        if ohne_th:
            n_th = sum(1 for st in blk.get("stuecke") or []
                       if _d.feld_von_m(st["pos_cm"][0] / 100.0, st["pos_cm"][1] / 100.0) in ohne_th)
            if n_th:
                b.append((FEHLER, aid, "%d Totholz-Stuecke in Feldern mit Ufer-Ebene (%s)" % (n_th, ", ".join(sorted(ohne_th)))))
        alle_pos += [(st["pos_cm"][0] / 100.0, st["pos_cm"][1] / 100.0) for st in fs]
        alle_pos += [(st["pos_cm"][0] / 100.0, st["pos_cm"][1] / 100.0) for st in blk.get("stuecke") or []]
    # nichts in Sehenswuerdigkeiten und in ausgesparten Bereichen
    if alle_pos:
        Q = np.asarray(alle_pos, np.float64)
        n_o = 0
        for o in orte or []:
            n_o += int((np.hypot(Q[:, 0] - o["x_m"], Q[:, 1] - o["y_m"]) <= float(o["radius_m"]) + 10.0 - 0.01).sum())
        if n_o:
            b.append((FEHLER, tag, "%d Bachbett-Stuecke in Sehenswuerdigkeiten (Radius + 10 m)" % n_o))
        d, sp_, _ = bb.projektion_schnell(Q[:, 0], Q[:, 1], P, 2048)
        s_q = np.interp(sp_, cum, S)
        aus = [(a_, b_) for a_, b_, g in (p.get("bereiche") or {}).get("ausgespart") or [] if "Lauf" not in g]
        n_a = 0
        for a_, b_ in aus:
            n_a += int(((s_q > a_ + 1.0) & (s_q < b_ - 1.0) & (d <= 6.0)).sum())
        if n_a:
            b.append((FEHLER, tag, "%d Bachbett-Stuecke in ausgesparten Bereichen (Ueberlappung, fremdes Wasser, "
                                   "Sehenswuerdigkeit, Stufenstrecke)" % n_a))
    for m in p.get("meldungen") or []:
        if m["stufe"] == FEHLER:
            b.append((FEHLER, tag, "Planer: %s" % m["text"]))
    return b


def pruefe_alle(aus, welt=None, inv=None, rw=None, laeufe=None, orte=None, ausgabe=True):
    """Alle Laeufe unter aus pruefen. Rueckgabe Exit-Code (1 bei FEHLER)."""
    from sehens_lib import ascii_text
    rw = rw or gr.Regelwerk.lade()
    if inv is None:
        from sehens_lib import inventar
        inv = inventar.Inventar.lade()
    orte = orte if orte is not None else gd.sehens_orte()
    z = {FEHLER: 0, WARNUNG: 0, HINWEIS: 0}
    namen = sorted(n for n in os.listdir(aus) if os.path.isdir(os.path.join(aus, n)))
    if laeufe:
        namen = [n for n in namen if n in set(laeufe)]
    alle = []
    for n in namen:
        bef = pruefe_lauf(os.path.join(aus, n), welt, inv, rw, orte)
        for st, oid, t in bef:
            z[st] += 1
            alle.append((st, oid, t))
    if ausgabe:
        for st_ in (FEHLER, WARNUNG):
            for st, oid, t in alle:
                if st == st_:
                    print("  %-7s %-26s %s" % (st, oid[:26], ascii_text(t)))
        print("[bachbett_roh_pruefen] %d Laeufe: %d FEHLER, %d WARNUNG, %d HINWEIS" % (len(namen), z[FEHLER], z[WARNUNG],
                                                                                    z[HINWEIS]), flush=True)
    return 1 if z[FEHLER] else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pruefer der Roh-Lauf-Ebene (16c Nachtrag 3)")
    ap.add_argument("aus")
    ap.add_argument("--laeufe", nargs="+", default=None)
    ap.add_argument("--sehens", default=gd.SEHENS_STANDARD)
    from sehens_lib import daten
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    welt = None
    if a.daten2m or a.daten1m:
        welt = daten.lade(a.daten2m, a.daten1m, pfade=False)
    return pruefe_alle(a.aus, welt=welt, laeufe=a.laeufe, orte=gd.sehens_orte(a.sehens))


if __name__ == "__main__":
    sys.exit(main())
