#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fluss_sim_pruefen.py - Pruefer fuer die Ausgaben von fluss_sim_export.py (Entscheidung 16).

Aufruf:  python -I fluss_sim_pruefen.py <aus> [--gefaelle DIR] [--sehens DIR] [--sw-ordner DIR]
                                         [--daten2m DIR | --daten1m DIR] [--vergleich <aus2>]
         <aus> = Ausgabeordner des Exporters (fluss_sim.json-Dateien, back_liste.json).
Exit-Code 1 bei FEHLER.

Geprueft:
  Spline     je Abschnitt >= 2 Punkte, z nie steigend, Becken flach (<= becken_gefaelle_max, sonst FEHLER), keine
             Luecke im Grundriss (Punktabstand <= punkt_abstand + 1 %), Abschnitte eines Gewaessers lueckenlos: an
             offenen Grenzen gemeinsamer Endpunkt, an Faellen Ende = Lippe (Oberwasser), Anfang = Fuss (Unterwasser).
  Werte      RiverWidth, Depth > 0, WaterVelocityScalar in [0; 1024] cm/s, Punkttypen/Tangenten so lang wie Punkte.
  Faelle     (mit --gefaelle/--sehens aus den QUELLEN neu gezaehlt) jeder Einzelabsturz >= fall_schwelle_m ohne Rampe
             ist ein Fall-Eintrag mit existierendem oberen/unteren Abschnitt (oder im Abschnitt), Lippe/Fuss-Hoehe
             wie in der Quelle (+-2 cm).
  Becken     (aus der Quelle) kein Becken ohne Abschnitt; Spiegel des Abschnitts am Becken = Quellspiegel (+-2 cm).
  Kollision  (mit Quellen) jedes feste, ausreichend grosse Objekt, dessen Mittelpunkt im Wasserstreifen liegt
             (Abstand zur Spline < halbe Breite, Unterkante <= Spiegel + 0,5 m), steht in wasser_kollision; jeder
             Verweis existiert (Datei/Index bzw. Akteur) und hat wasser_kollision = true.
  Schaum     Art bekannt, Groesse > 0, Lage im Wasserstreifen des eigenen Gewaessers (+ 0,5 m).
  Kacheln    jeder Abschnitt in genau einer Kachel; back_liste deckt alle Kacheln; Fingerabdruck (Splines und
             Objekte aus den Dateien, Gelaende mit --daten2m/--daten1m) nach README neu gerechnet = gespeichert.
  Determinismus  mit --vergleich: alle Dateien byte-gleich.
"""

import argparse
import hashlib
import json
import math
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(HIER))
sys.path.insert(0, os.path.join(os.path.dirname(HIER), "gefaelle"))

import numpy as np  # noqa: E402

import fluss_sim_export as fx  # noqa: E402

FEHLER, WARNUNG, HINWEIS = "FEHLER", "WARNUNG", "HINWEIS"
SCHAUM_ARTEN = ("aufprallteppich", "schaumstrasse", "kehrwasser")


def melde(befunde, titel=""):
    z = {FEHLER: 0, WARNUNG: 0, HINWEIS: 0}
    for st, _, _ in befunde:
        z[st] += 1
    sys.stdout.write("[fluss_sim_pruefen] %s: %d FEHLER, %d WARNUNG, %d HINWEIS\n" % (titel, z[FEHLER], z[WARNUNG], z[HINWEIS]))
    for st in (FEHLER, WARNUNG, HINWEIS):
        n = 0
        for s, oid, t in befunde:
            if s == st:
                n += 1
                if n <= 40:
                    sys.stdout.write("  %-7s %-26s %s\n" % (s, str(oid)[:26], t))
        if n > 40:
            sys.stdout.write("  %-7s ... %d weitere\n" % (st, n - 40))
    sys.stdout.flush()
    return z


def dateien_finden(aus):
    out = []
    for w, _, fs in os.walk(aus):
        for f in fs:
            if f == "fluss_sim.json":
                out.append(os.path.join(w, f))
    return sorted(out)


def _strecke(P):
    P = np.asarray(P, float)
    return np.hypot(*np.diff(P[:, :2], axis=0).T) / 100.0 if len(P) > 1 else np.zeros(0)


def pruefe_abschnitte(g, regeln, b):
    R = regeln["abschnitt"]
    tag = g["id"]
    abst = {d["id"]: d for d in g.get("abstuerze") or []}
    vor = None
    for a in g["abschnitte"]:
        P = np.asarray(a["punkte"], float)
        if len(P) < 2:
            b.append((FEHLER, a["id"], "< 2 Splinepunkte"))
            continue
        for k in ("punkt_typen", "tangenten_cm", "punkte_s_m"):
            if len(a.get(k) or []) != len(P):
                b.append((FEHLER, a["id"], "%s nicht so lang wie punkte" % k))
        if (np.diff(P[:, 2]) > 0.05).any():
            b.append((FEHLER, a["id"], "Spline steigt (max +%.1f cm)" % float(np.diff(P[:, 2]).max())))
        if (P[:, 3] <= 0).any():
            b.append((FEHLER, a["id"], "RiverWidth <= 0"))
        if (P[:, 4] <= 0).any():
            b.append((FEHLER, a["id"], "Depth <= 0"))
        if (P[:, 5] < 0).any() or (P[:, 5] > R["velocity_max_cm_s"] + 1e-6).any():
            b.append((FEHLER, a["id"], "WaterVelocityScalar ausserhalb [0; %d]" % R["velocity_max_cm_s"]))
        d = _strecke(P)
        s = np.asarray(a["punkte_s_m"], float)
        ds = np.diff(s)
        roh = g.get("kategorie") in ("fluesse", "gefaelle_roh") or not (g.get("quelle") or {}).get("wasser_koerper")
        lim = R["punkt_abstand_roh_m"] if roh else R["punkt_abstand_m"]
        # Absturz (LINEAR -> LINEAR) darf nicht unterteilt sein; sonst Abstand <= Grenze
        typ = a["punkt_typen"]
        for i in range(len(ds)):
            if typ[i] == "LINEAR" and typ[i + 1] == "LINEAR":
                continue
            if ds[i] > lim * 1.01 + 0.01:
                b.append((FEHLER, a["id"], "Splinepunkte %.2f m auseinander (> %.1f m) bei s %.1f" % (ds[i], lim, s[i])))
                break
        if (d > np.maximum(ds, 0.01) * 1.5 + 1.0).any():
            b.append((FEHLER, a["id"], "Grundriss-Sprung zwischen Splinepunkten (Spline nicht durchgehend)"))
        # Becken flach: Gefaelle zwischen Punkten, die nicht Lippe->Fuss eines Absturzes sind
        rol = a.get("punkt_rollen") or []
        if len(rol) != len(P):
            b.append((FEHLER, a["id"], "punkt_rollen nicht so lang wie punkte"))
            rol = ["?"] * len(P)
        for i in range(len(ds)):
            if not (rol[i] == "becken" and rol[i + 1] == "becken") or ds[i] <= 0.2:
                continue
            gef = (P[i, 2] - P[i + 1, 2]) / 100.0 / ds[i]
            if gef > R["becken_gefaelle_max"] + 1e-3:
                b.append((FEHLER, a["id"], "Becken-Gefaelle %.1f %% > %.0f %% zwischen s %.1f und %.1f (nicht waagrecht)"
                          % (100 * gef, 100 * R["becken_gefaelle_max"], s[i], s[i + 1])))
                break
        # Anschluss an den vorigen Abschnitt
        if vor is not None:
            Pv = np.asarray(vor["punkte"], float)
            of = a["anschluss"]["oben_fall"]
            if of and of in abst:
                f = abst[of]
                if abs(vor["s_m"][1] - f["s_lippe_m"]) > 0.02 or abs(a["s_m"][0] - f["s_fuss_m"]) > 0.02:
                    b.append((FEHLER, a["id"], "Anschluss an Fall %s passt nicht (Lippe/Fuss)" % of))
                if Pv[-1, 2] + 0.05 < P[0, 2]:
                    b.append((FEHLER, a["id"], "unterer Abschnitt liegt hoeher als der obere"))
            else:
                if np.abs(Pv[-1, :3] - P[0, :3]).max() > 1.0:
                    b.append((FEHLER, a["id"], "offene Grenze ohne gemeinsamen Endpunkt (Luecke %.1f cm)"
                              % float(np.abs(Pv[-1, :3] - P[0, :3]).max())))
        vor = a


def quell_abstuerze(g, quellen, regeln):
    """Abstuerze und Becken neu aus der Quelle (unabhaengig vom Export)."""
    q = g.get("quelle") or {}
    if ("plan" in q and not quellen.get("gefaelle")) or ("orte" in q and not quellen.get("sehens")):
        return "ohne_quelle"
    if "plan" in q and quellen.get("gefaelle"):
        pf = os.path.join(quellen["gefaelle"], os.path.relpath(q["plan"], "gefaelle"))
        if not os.path.exists(pf):
            return None
        plan = fx.lese_json(pf)
        out = []
        for st in plan.get("stufen") or []:
            teil = st.get("teilstufen")
            if isinstance(teil, str):
                teil = json.loads(teil)
            if teil:
                for k, t in enumerate(teil):
                    out.append(("%s_T%d" % (st["id"], k + 1), float(t["fall_m"]), bool(t.get("rampe")) or st.get("art") == "schnelle",
                                float(t["oben_z_cm"]), float(t["unten_z_cm"]), float(t["s_m"])))
            else:
                out.append((st["id"], float(st["fall_m"]), st.get("art") == "schnelle", float(st["lippe_cm"][0][2]),
                            float(st["fuss_z_cm"]), float(st["s_m"])))
        return out
    if "orte" in q and quellen.get("sehens"):
        pf = os.path.join(quellen["sehens"], os.path.relpath(q["orte"], "sehens"))
        if not os.path.exists(pf):
            return None
        od = quellen.setdefault("_cache", {}).get(pf) or fx.lese_json(pf)
        quellen["_cache"][pf] = od
        for o in od.get("orte") or []:
            if o["id"] != q["ort"]:
                continue
            for w in o.get("wasser") or []:
                if w.get("typ") == "bach" and w.get("id") == q["bach"]:
                    return [("%s_S%02d" % (g["id"], k), float(st["fall_m"]), st.get("art") == "schnelle",
                             float(st["lippe_cm"][2]), float(st["fuss_cm"][2]), None)
                            for k, st in enumerate(w.get("stufen") or []) if st.get("lippe_cm") and st.get("fuss_cm")]
        return None
    return []


def pruefe_faelle_becken(g, quellen, regeln, b):
    schw = regeln["fall_schwelle_m"]
    qa = quell_abstuerze(g, quellen, regeln)
    ab = {a["id"]: a for a in g["abschnitte"]}
    fl = {f["id"]: f for f in g["faelle"]}
    if qa == "ohne_quelle":
        quellen["_ohne"] = quellen.get("_ohne", 0) + 1
        qa_ids = None
    elif qa is None:
        b.append((WARNUNG, g["id"], "Quelle nicht gefunden - Faelle/Becken nicht gegen die Quelle geprueft"))
        qa_ids = None
    else:
        qa_ids = {x[0] for x in qa}
        for fid, fall, rampe, zo, zu, s_ in qa:
            if fall >= schw - 1e-9 and not rampe:
                f = fl.get(fid)
                if f is None:
                    b.append((FEHLER, g["id"], "Stufe %s (%.2f m >= %.1f m) ohne Fall-Eintrag" % (fid, fall, schw)))
                    continue
                if abs(f["lippe_cm"][2] - zo) > 2.0 or abs(f["fuss_cm"][2] - zu) > 2.0:
                    b.append((FEHLER, fid, "Lippe/Fuss-Hoehe weicht von der Quelle ab"))
                if s_ is not None and abs(f["s_lippe_m"] - s_) > 0.05:
                    b.append((FEHLER, fid, "Lippe s %.2f statt %.2f" % (f["s_lippe_m"], s_)))
        for fid in fl:
            if fid not in qa_ids:
                b.append((FEHLER, fid, "Fall-Eintrag ohne Stufe in der Quelle"))
    for f in g["faelle"]:
        if f["fall_m"] < schw - 1e-9:
            b.append((FEHLER, f["id"], "Fall %.2f m < Schwelle" % f["fall_m"]))
        for k in ("abschnitt_oben", "abschnitt_unten"):
            if f[k] is not None and f[k] not in ab:
                b.append((FEHLER, f["id"], "%s %s existiert nicht" % (k, f[k])))
        if f["abschnitt_oben"] is None and f["abschnitt_unten"] is None:
            b.append((FEHLER, f["id"], "Fall ohne oberen und unteren Abschnitt"))
        if f["im_abschnitt"] and f["id"] not in ab[f["abschnitt_oben"]]["faelle_innen"]:
            b.append((FEHLER, f["id"], "im_abschnitt, aber nicht in faelle_innen"))
        if not f.get("schaum_objekte"):
            b.append((FEHLER, f["id"], "keine schaum_objekte (mindestens Aufprallteppich)"))
        elif not any(s["art"] == "aufprallteppich" for s in f["schaum_objekte"]):
            b.append((FEHLER, f["id"], "kein Aufprallteppich"))
        if not f["kaskadennetz"].get("id") and g.get("kategorie") != "fluesse":
            b.append((WARNUNG, f["id"], "Fall ohne Kaskadennetz-Verweis (Vorhang lokal pruefen)"))
    # Becken: aus den Abstuerzen (Fuss -> naechste Lippe), Mitte muss in einem Abschnitt liegen
    abst = sorted(g.get("abstuerze") or [], key=lambda d: d["s_lippe_m"])
    s0 = min(a["s_m"][0] for a in g["abschnitte"]) if g["abschnitte"] else 0.0
    s1 = max(a["s_m"][1] for a in g["abschnitte"]) if g["abschnitte"] else 0.0
    if qa_ids is not None and {d["id"] for d in abst} != qa_ids:
        b.append((FEHLER, g["id"], "Absturzliste weicht von der Quelle ab"))
    grenzen = []
    a_ = 0.0
    for d in abst:
        if d["s_lippe_m"] - a_ > 0.05:
            grenzen.append((a_, d["s_lippe_m"]))
        a_ = max(a_, d["s_fuss_m"])
    grenzen.append((a_, g["laenge_m"]))
    for ba, bb in grenzen:
        if bb - ba < 0.05:
            continue
        m = 0.5 * (ba + bb)
        if m < s0 - 1e-3 or m > s1 + 1e-3:
            # Reste am Laufrand (Fall direkt am Laufanfang/-ende) sind erlaubt, wenn kuerzer als rest_am_laufende_m
            if bb - ba >= regeln["abschnitt"]["rest_am_laufende_m"]:
                b.append((FEHLER, g["id"], "Becken s %.1f-%.1f ohne Abschnitt" % (ba, bb)))
            continue
        if not any(a["s_m"][0] - 1e-3 <= m <= a["s_m"][1] + 1e-3 for a in g["abschnitte"]):
            b.append((FEHLER, g["id"], "Becken s %.1f-%.1f ohne Abschnitt" % (ba, bb)))
    for a in g["abschnitte"]:
        ss = np.asarray(a["punkte_s_m"], float)
        zz = np.asarray([p[2] for p in a["punkte"]], float)
        for bk in a.get("becken") or []:
            for s_, z_ in zip(bk["s_m"], bk["spiegel_cm"]):
                if a["s_m"][0] - 1e-3 <= s_ <= a["s_m"][1] + 1e-3:
                    k = int(np.argmin(np.abs(ss - s_)))
                    if abs(ss[k] - s_) < 0.02 and abs(zz[k] - z_) > 2.0:
                        b.append((FEHLER, a["id"], "Spline-Spiegel %.1f statt Becken %.1f cm bei s %.2f (Becken nicht gefuellt)"
                                  % (zz[k], z_, s_)))


def streifen(g):
    segs = []
    for a in g["abschnitte"]:
        P = np.asarray(a["punkte"], float)
        for i in range(len(P) - 1):
            segs.append((P[i], P[i + 1]))
    if not segs:
        return None
    A = np.array([s[0] for s in segs]) / 100.0
    B = np.array([s[1] for s in segs]) / 100.0
    return A, B


def streifen_alle(st, x, y):
    """Je Punkt x Segment: Abstand (m) zur Mittellinie, halbe Breite, Spiegel und Tiefe (m) am Lotpunkt."""
    A, B = st
    AB = B[:, :2] - A[:, :2]
    L2 = np.maximum((AB ** 2).sum(1), 1e-9)
    x = np.asarray(x, float)[:, None]
    y = np.asarray(y, float)[:, None]
    t = np.clip(((x - A[None, :, 0]) * AB[None, :, 0] + (y - A[None, :, 1]) * AB[None, :, 1]) / L2[None, :], 0, 1)
    d = np.hypot(x - (A[None, :, 0] + t * AB[None, :, 0]), y - (A[None, :, 1] + t * AB[None, :, 1]))
    halb = (A[None, :, 3] + t * (B[None, :, 3] - A[None, :, 3])) / 2.0
    z = A[None, :, 2] + t * (B[None, :, 2] - A[None, :, 2])
    tf = A[None, :, 4] + t * (B[None, :, 4] - A[None, :, 4])
    return d, halb, z, tf


def pruefe_kollision(g, pool, regeln, b):
    st = streifen(g)
    if st is None:
        return
    liste = {json.dumps(o["ref"], sort_keys=True): o for o in g["wasser_kollision"]}
    for key, o in liste.items():
        if not o.get("wasser_kollision"):
            b.append((FEHLER, g["id"], "wasser_kollision != true: %s" % key))
        if pool is not None and key not in pool["refs"]:
            b.append((FEHLER, g["id"], "Verweis existiert nicht: %s" % key))
    if pool is None:
        return
    A, B = st
    xmin, xmax = min(A[:, 0].min(), B[:, 0].min()) - 50, max(A[:, 0].max(), B[:, 0].max()) + 50
    ymin, ymax = min(A[:, 1].min(), B[:, 1].min()) - 50, max(A[:, 1].max(), B[:, 1].max()) + 50
    P = pool["p"]
    R = regeln["kollision"]
    kand = np.where(pool["fest"] & (P.cx >= xmin) & (P.cx <= xmax) & (P.cy >= ymin) & (P.cy <= ymax))[0]
    fehlt = []
    for c0 in range(0, len(kand), 512):
        kk = kand[c0:c0 + 512]
        d, halb, z, tf = streifen_alle(st, P.cx[kk], P.cy[kk])
        zlo = P.lo[kk, 2][:, None] / 100.0
        zhi = P.hi[kk, 2][:, None] / 100.0
        # Mittelpunkt im Wasserstreifen, Unterkante nicht ueber dem Spiegel + Toleranz, nicht ganz unter dem Bett
        im = ((d < halb) & (zlo <= z + R["ueber_spiegel_max_m"]) & (zhi >= z - tf - R["unter_bett_toleranz_m"])).any(1)
        for k in kk[im]:
            key = json.dumps(P.ref(int(k)), sort_keys=True)
            if key not in liste:
                fehlt.append(key)
    if fehlt:
        b.append((FEHLER, g["id"], "%d Objekte im Wasser ohne wasser_kollision, z. B. %s" % (len(fehlt), fehlt[0])))


def pruefe_schaum(g, b):
    st = streifen(g)
    if st is None:
        return
    pts, wer = [], []
    for f in g["faelle"]:
        if f["abschnitt_unten"] is None:
            b.append((HINWEIS, f["id"], "Fuss im Folgegewaesser (See/Fluss): Schaumobjekte dort nicht gegen eigene Abschnitte geprueft"))
            continue
        for s in f["schaum_objekte"]:
            if s["art"] not in SCHAUM_ARTEN:
                b.append((FEHLER, f["id"], "Schaum-Art %r" % s["art"]))
            if min(s["groesse_m"]) <= 0:
                b.append((FEHLER, f["id"], "Schaum-Groesse <= 0"))
            for p in (s.get("punkte_cm") or [s["pos_cm"]]):
                pts.append(p)
                wer.append(f["id"])
    if not pts:
        return
    P = np.asarray(pts, float) / 100.0
    d, halb, z, _ = streifen_alle(st, P[:, 0], P[:, 1])
    # im Wasser = an einem Segment innerhalb halbe Breite + 0,5 m UND dort auf dessen Spiegel (+-0,5 m)
    ok_xy = d <= halb + 0.5
    ok = (ok_xy & (np.abs(P[:, 2][:, None] - z) <= 0.5)).any(1)
    raus = np.where(~ok_xy.any(1))[0]
    if len(raus):
        k = raus[0]
        b.append((FEHLER, g["id"], "%d Schaumpunkte ausserhalb des Wassers (z. B. %s, %.1f m neben der Kante)"
                  % (len(raus), wer[k], float((d[k] - halb[k]).min()))))
    falsch_z = np.where(ok_xy.any(1) & ~ok)[0]
    if len(falsch_z):
        b.append((FEHLER, g["id"], "%d Schaumpunkte nicht auf dem Spiegel (z. B. %s)" % (len(falsch_z), wer[falsch_z[0]])))


def pruefe_kacheln(g, b):
    n = {}
    for k in g["sim_bereiche"]:
        for a in k["abschnitte"]:
            n[a] = n.get(a, 0) + 1
        if not k.get("fingerabdruck"):
            b.append((FEHLER, k["id"], "kein Fingerabdruck"))
    for a in g["abschnitte"]:
        if n.get(a["id"], 0) != 1:
            b.append((FEHLER, a["id"], "in %d Kacheln (soll 1)" % n.get(a["id"], 0)))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pruefer Entscheidung 16 (fluss_sim_export.py-Ausgaben)")
    ap.add_argument("aus")
    ap.add_argument("--gefaelle", default=None)
    ap.add_argument("--sehens", default=None)
    ap.add_argument("--sw-ordner", default=None)
    ap.add_argument("--regeln", default=fx.REGELN_STANDARD)
    ap.add_argument("--vergleich", default=None, help="zweiter Ausgabeordner: Dateien muessen byte-gleich sein")
    ap.add_argument("--daten2m", default=None)
    ap.add_argument("--daten1m", default=None)
    a = ap.parse_args(argv)
    regeln = fx.lese_json(a.regeln)
    gesamt = {FEHLER: 0, WARNUNG: 0, HINWEIS: 0}
    quellen = {"gefaelle": a.gefaelle, "sehens": a.sehens}
    pool = None
    if a.gefaelle or a.sehens:
        import glob
        P = fx.Pool(regeln, fx.Masse())
        if a.gefaelle:
            for pf in sorted(glob.glob(os.path.join(a.gefaelle, "*", "instanzen", "*", "plan.json"))):
                lauf = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(pf))))
                P.lade_ebene(pf, "gefaelle/%s/instanzen/%s/plan.json" % (lauf, os.path.basename(os.path.dirname(pf))))
        if a.sehens:
            for biom in fx.BIOME:
                sw = fx.finde_sw(a.sehens, a.sw_ordner, biom)
                if sw:
                    for pf in sorted(glob.glob(os.path.join(sw, "*", "plan.json"))):
                        P.lade_ebene(pf, "sw_%s/%s/plan.json" % (biom, os.path.basename(os.path.dirname(pf))))
        P.fertig()
        pool = {"p": P, "fest": P.fest, "refs": {json.dumps(P.ref(k), sort_keys=True) for k in range(len(P.recs))}}
    alle_kacheln = {}
    for pf in dateien_finden(a.aus):
        d = fx.lese_json(pf)
        rel = os.path.relpath(pf, a.aus)
        b = []
        if d.get("format") != fx.FORMAT_VERSION:
            b.append((FEHLER, rel, "format %r" % d.get("format")))
        for g in d.get("gewaesser") or []:
            pruefe_abschnitte(g, regeln, b)
            pruefe_faelle_becken(g, quellen, regeln, b)
            pruefe_kollision(g, pool, regeln, b)
            pruefe_schaum(g, b)
            pruefe_kacheln(g, b)
            for k in g["sim_bereiche"]:
                alle_kacheln[k["id"]] = (k, g)
        if b:
            z = melde(b, rel)
            for k_ in gesamt:
                gesamt[k_] += z[k_]
    # back_liste und Fingerabdruck
    b = []
    pb = os.path.join(a.aus, "back_liste.json")
    if not os.path.exists(pb):
        b.append((FEHLER, "back_liste", "back_liste.json fehlt"))
    else:
        bl = fx.lese_json(pb)
        fpr = regeln["fingerabdruck"]
        ids = {k["kachel"] for k in bl["kacheln"]}
        if ids != set(alle_kacheln):
            b.append((FEHLER, "back_liste", "Kacheln in back_liste != Kacheln der Dateien (%d / %d)" % (len(ids), len(alle_kacheln))))
        if len(ids) != len(bl["kacheln"]):
            b.append((FEHLER, "back_liste", "Kachel-IDs doppelt"))
        gel = None
        if a.daten2m or a.daten1m:
            from sehens_lib import daten
            welt = daten.lade(a.daten2m, a.daten1m, pfade=False)
            gel = fx.Gelaende(welt)
            if a.gefaelle:
                for pf in sorted(os.listdir(a.gefaelle)):
                    pp = os.path.join(a.gefaelle, pf, "plan.json")
                    if os.path.exists(pp):
                        gel.delta_hinzu(os.path.join(a.gefaelle, pf), fx.lese_json(pp).get("abschnitte"))
            if a.sehens:
                for biom in fx.BIOME:
                    po = os.path.join(a.sehens, biom, "orte.json")
                    if os.path.exists(po):
                        gel.delta_hinzu(os.path.join(a.sehens, biom), fx.lese_json(po).get("orte"))
        objekte_alle = {}
        for kid, (k, g) in alle_kacheln.items():
            for o in g["wasser_kollision"]:
                objekte_alle[json.dumps(o["ref"], sort_keys=True)] = o
        P = pool["p"] if pool else None
        ref_k = {json.dumps(P.ref(k), sort_keys=True): k for k in range(len(P.recs))} if P else {}
        for e in bl["kacheln"]:
            if e["kachel"] not in alle_kacheln:
                continue
            k, g = alle_kacheln[e["kachel"]]
            if e["fingerabdruck"] != k.get("fingerabdruck"):
                b.append((FEHLER, e["kachel"], "Fingerabdruck back_liste != fluss_sim.json"))
            ab = {x["id"]: x for x in g["abschnitte"]}
            st = fx.fp_splines_text([(i, ab[i]["punkte"]) for i in k["abschnitte"]], fpr["spline_quant_cm"])
            if hashlib.sha256(st.encode("ascii")).hexdigest() != e["teile"]["splines"]:
                b.append((FEHLER, e["kachel"], "Fingerabdruck Splines neu gerechnet != gespeichert"))
            if P is not None:
                bx = e["bereich_cm"]
                objs = []
                for key in objekte_alle:
                    kk = ref_k.get(key)
                    if kk is None:
                        continue
                    if P.hi[kk, 0] >= bx[0] and P.lo[kk, 0] <= bx[2] and P.hi[kk, 1] >= bx[1] and P.lo[kk, 1] <= bx[3]:
                        objs.append([P.recs[kk]["pfad"]] + [float(v) for v in P.recs[kk]["v"][:10]])
                ot = fx.fp_objekte_text(objs, fpr["pos_quant_cm"], fpr["quat_quant"], fpr["skala_quant"])
                if hashlib.sha256(ot.encode("ascii")).hexdigest() != e["teile"]["objekte"]:
                    b.append((FEHLER, e["kachel"], "Fingerabdruck Objekte neu gerechnet != gespeichert"))
            if gel is not None:
                x0, y0, rcm, H = gel.raster(e["bereich_cm"])
                gt = fx.fp_gelaende_text(x0, y0, rcm, H, fpr["hoehe_quant_cm"])
                if hashlib.sha256(gt.encode("ascii")).hexdigest() != e["teile"]["gelaende"]:
                    b.append((FEHLER, e["kachel"], "Fingerabdruck Gelaende neu gerechnet != gespeichert"))
            ges, _ = fx.fingerabdruck("", "", "", fpr["version"])
            kombi = hashlib.sha256(("%s\n%s\n%s\n%s\n" % (fpr["version"], e["teile"]["gelaende"], e["teile"]["splines"],
                                                          e["teile"]["objekte"])).encode("ascii")).hexdigest()
            if kombi != e["fingerabdruck"]:
                b.append((FEHLER, e["kachel"], "Gesamt-Fingerabdruck != SHA-256 der Teile"))
    if a.vergleich:
        def summen(o):
            out = {}
            for w, _, fs in os.walk(o):
                for f in fs:
                    p = os.path.join(w, f)
                    with open(p, "rb") as h:
                        out[os.path.relpath(p, o)] = hashlib.sha256(h.read()).hexdigest()
            return out
        s1, s2 = summen(a.aus), summen(a.vergleich)
        if s1 != s2:
            diff = sorted(k for k in set(s1) | set(s2) if s1.get(k) != s2.get(k))
            b.append((FEHLER, "Determinismus", "%d Dateien verschieden, z. B. %s" % (len(diff), diff[:3])))
        else:
            b.append((HINWEIS, "Determinismus", "%d Dateien byte-gleich mit %s" % (len(s1), a.vergleich)))
    if quellen.get("_ohne"):
        b.append((HINWEIS, "Quellen", "%d Gewaesser ohne --gefaelle/--sehens: Faelle/Becken/Kollision nicht gegen die "
                  "Quelle geprueft" % quellen["_ohne"]))
    z = melde(b, "back_liste/Determinismus")
    for k_ in gesamt:
        gesamt[k_] += z[k_]
    sys.stdout.write("[fluss_sim_pruefen] GESAMT: %d FEHLER, %d WARNUNG, %d HINWEIS\n" % (gesamt[FEHLER], gesamt[WARNUNG], gesamt[HINWEIS]))
    return 1 if gesamt[FEHLER] else 0


if __name__ == "__main__":
    sys.exit(main())
