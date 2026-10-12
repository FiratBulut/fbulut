#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fluss_sim_pruefen.py - Pruefer fuer die Ausgaben von fluss_sim_export.py (Entscheidung 16, Format v3 / 16c).

Aufruf:  python -I fluss_sim_pruefen.py <aus> [--gefaelle DIR] [--sehens DIR] [--sw-ordner DIR]
                                         [--daten2m DIR | --daten1m DIR] [--vergleich <aus2>]
                                         [--gebaut LAUF ...] [--einbau DIR] [--ohne-erkennung]
         <aus> = Ausgabeordner des Exporters (fluss_sim.json-Dateien, back_liste.json, vorschlaege.json).
Exit-Code 1 bei FEHLER.

Geprueft (FEHLER, wenn nicht anders gesagt):
  Ein Fluss  je Gewaesser genau ein WaterBodyRiver (WBR_<gewaesser>, global eindeutig), jede SWR nennt ihn als Quelle
             und Senke; jeder Welt-Lauf in genau einem Gewaesser (mit --daten: alle Laeufe aus wasser_welt.json und
             baeche_alle.json kommen vor), Laeufe lueckenlos hintereinander.
  Spline     >= 2 Punkte, Felder gleich lang, s steigend von 0 bis laenge_m, durchgehend (kein Grundriss-Sprung,
             Abstand <= 2 x Ziel ausser zwischen Lippe und Fuss), z nie steigend, Breite/Tiefe > 0, Tempo in
             [0; 1024]; Becken-Punkte flach (<= 3 %) und auf dem Becken-Spiegel (+-2 cm).
  Stufen     jede Stufe (Absturz) hat einen Lippen- und einen Fusspunkt: Index gueltig, Rolle, s (+-2 cm) und z =
             Ober- bzw. Unterwasser (+-2 cm); mit --gefaelle/--sehens Abstuerze und Faelle aus den QUELLEN neu gezaehlt
             (Lippe/Fuss-Hoehe wie die Quelle, entfallene nur an gekuerzten Laufenden).
  Bereiche   lueckenlos von 0 bis laenge_m (bis auf die Faelle), jeder Bereich von SWR-Bereichen abgedeckt.
  SWR        Kette von 0 bis laenge_m, Ueberlappung an den Naehten, keine Naht an einer Stufe; Rechteck und Achse aus den
             Splinepunkten neu gerechnet, resolution_max_axis Vielfaches von 32 und <= 2048, Zelle = Achse /
             Aufloesung <= zelle_max + 0,005 m; eine SWR je Gewaesser, wenn das Rechteck es erlaubt (sonst FEHLER).
  Muendung   Art bekannt; Ziel (Gewaesser/See) existiert, Muendungspunkt = Spline-Ende, bei Fluss/Bach im Wasserstreifen
             des Ziels (+ Luecke) und in dessen zufluesse; offen = HINWEIS.
  Faelle     Vorhang-Regel 16b, Schaum/Kaskadennetz nur an Vorhang-Faellen, Lippe/Fuss-Punkt wie Absturz.
  Kollision, Schaum, Hindernis-Akteure (je SWR), Back-Liste mit Fingerabdruck (neu gerechnet), Determinismus wie v2.
  16d        nur Lauf-Plaene (Archivordner/Feld-Plaene wie beim Export uebersprungen); Gelaende ohne die Deltas gebauter
             Laeufe (back_liste.gelaende.deltas_ohne), Erkennung heute anders = WARNUNG; Toepfe (Bereich topf, Punkt
             auf dem Spiegel, SWR-Rechteck schliesst den Topf ein, < Grenze, nur in einem Gewaesser, kein See-Ziel);
             Vorschlaege (am Spline-Ende, z nie steigend, Punktabstand, Ziel erreicht, = vorschlaege.json).
"""

import argparse
import hashlib
import json
import math
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(HIER))
sys.path.insert(0, os.path.join(os.path.dirname(HIER), "gefaelle"))

import numpy as np  # noqa: E402

import fluss_sim_export as fx  # noqa: E402

FEHLER, WARNUNG, HINWEIS = "FEHLER", "WARNUNG", "HINWEIS"
SCHAUM_ARTEN = ("aufprallteppich", "schaumstrasse", "kehrwasser")
MUENDUNG_ARTEN = ("meer", "see", "fluss", "bach", "versickert", "wasserfall", "offen", "topf")


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
                    sys.stdout.write("  %-7s %-30s %s\n" % (s, str(oid)[:30], t))
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


def roh_bei(g, s):
    for l_ in g["laeufe"]:
        if l_["s_m"][0] - 1e-3 <= s <= l_["s_m"][1] + 1e-3:
            return l_["herkunft"] == "roh" or (l_["herkunft"] == "sehens" and not (l_["quelle"] or {}).get("wasser_koerper"))
    return True


# ----------------------------------------------------------------------------------------------------------------------
def pruefe_spline(g, regeln, b):
    SP = regeln["spline"]
    R = regeln["abschnitt"]
    gid = g["id"]
    wb = g["water_body"]
    if wb.get("id") != "WBR_" + gid or wb.get("klasse") != "WaterBodyRiver":
        b.append((FEHLER, gid, "water_body heisst %r (soll WBR_%s, WaterBodyRiver)" % (wb.get("id"), gid)))
    sp = wb["spline"]
    P = np.asarray(sp["punkte"], float)
    if len(P) < 2:
        b.append((FEHLER, gid, "Spline < 2 Punkte"))
        return None
    for k in ("punkt_typen", "tangenten_cm", "punkte_s_m", "punkt_rollen"):
        if len(sp.get(k) or []) != len(P):
            b.append((FEHLER, gid, "spline.%s nicht so lang wie punkte" % k))
            return None
    ss = np.asarray(sp["punkte_s_m"], float)
    ds = np.diff(ss)
    if (ds <= 0).any():
        b.append((FEHLER, gid, "punkte_s_m nicht streng steigend"))
    if abs(ss[0]) > 0.011 or abs(ss[-1] - g["laenge_m"]) > 0.011:
        b.append((FEHLER, gid, "Spline s %.2f-%.2f statt 0-%.2f" % (ss[0], ss[-1], g["laenge_m"])))
    if (np.diff(P[:, 2]) > 0.05).any():
        i = int(np.argmax(np.diff(P[:, 2])))
        b.append((FEHLER, gid, "Spline steigt (+%.1f cm bei s %.1f)" % (float(np.diff(P[:, 2])[i]), ss[i])))
    if (P[:, 3] <= 0).any() or (P[:, 4] <= 0).any():
        b.append((FEHLER, gid, "RiverWidth/Depth <= 0"))
    if (P[:, 5] < 0).any() or (P[:, 5] > R["velocity_max_cm_s"] + 1e-6).any():
        b.append((FEHLER, gid, "WaterVelocityScalar ausserhalb [0; %d]" % R["velocity_max_cm_s"]))
    d = np.hypot(*np.diff(P[:, :2], axis=0).T) / 100.0
    if (d > np.maximum(ds, 0.01) * 1.5 + 1.0).any():
        i = int(np.argmax(d - ds))
        b.append((FEHLER, gid, "Grundriss-Sprung bei s %.1f (Spline nicht durchgehend)" % ss[i]))
    rol = sp["punkt_rollen"]
    typ = sp["punkt_typen"]
    for i in range(len(ds)):
        if "lippe" in rol[i] and "fuss" in rol[i + 1]:
            continue
        roh_ = roh_bei(g, ss[i]) or roh_bei(g, ss[i + 1]) or roh_bei(g, 0.5 * (ss[i] + ss[i + 1]))
        lim = 2 * (SP["abstand_roh_m"] if roh_ else SP["abstand_m"])
        if ds[i] > lim + 0.011:
            b.append((FEHLER, gid, "Splinepunkte %.2f m auseinander (> %.1f m) bei s %.1f" % (ds[i], lim, ss[i])))
            break
    for i, r in enumerate(rol):
        if r in ("lippe", "fuss", "fuss_lippe") and typ[i] != "LINEAR":
            b.append((FEHLER, gid, "Stufenpunkt %d nicht LINEAR" % i))
            break
    # Becken flach und auf dem Becken-Spiegel
    for i in range(len(ds)):
        if rol[i] == "becken" and rol[i + 1] == "becken" and ds[i] > 0.2:
            gef = (P[i, 2] - P[i + 1, 2]) / 100.0 / ds[i]
            if gef > R["becken_gefaelle_max"] + 1e-3:
                b.append((FEHLER, gid, "Becken-Gefaelle %.1f %% bei s %.1f" % (100 * gef, ss[i])))
                break
    bec = [bk for br in g["bereiche"] for bk in br["becken"]]
    for bk in bec:
        (a, c), (za, zc) = bk["s_m"], bk["spiegel_cm"]
        if abs(za - zc) > 2.0:
            continue
        m = (ss >= a + 0.02) & (ss <= c - 0.02) & np.array([r == "becken" for r in rol])
        if m.any() and (np.abs(P[m, 2] - za) > 2.0 + 1e-6).any():
            b.append((FEHLER, gid, "Becken s %.1f-%.1f nicht gefuellt (Spline %.1f statt %.1f cm)"
                      % (a, c, float(P[m, 2][np.argmax(np.abs(P[m, 2] - za))]), za)))
    return ss, P


def pruefe_stufen(g, ss, P, b):
    rol = g["water_body"]["spline"]["punkt_rollen"]
    for d in g["abstuerze"]:
        for teil, s_, z_ in (("lippe", d["s_lippe_m"], d["z_oben_cm"]), ("fuss", d["s_fuss_m"], d["z_unten_cm"])):
            i = d.get("punkt_" + teil)
            if i is None or not (0 <= i < len(ss)):
                b.append((FEHLER, d["id"], "Stufe ohne %s-Punkt" % teil))
                continue
            if teil not in rol[i]:
                b.append((FEHLER, d["id"], "%s-Punkt %d hat Rolle %s" % (teil, i, rol[i])))
            if abs(ss[i] - s_) > 0.06:
                b.append((FEHLER, d["id"], "%s-Punkt bei s %.2f statt %.2f" % (teil, ss[i], s_)))
            if abs(P[i, 2] - z_) > 2.0 + 1e-6:
                b.append((FEHLER, d["id"], "%s-Punkt z %.1f statt %s %.1f cm" % (teil, P[i, 2], "Oberwasser" if teil == "lippe"
                                                                                    else "Unterwasser", z_)))
        if d.get("punkt_lippe") is not None and d.get("punkt_fuss") is not None and d["punkt_fuss"] <= d["punkt_lippe"] \
                and d["fall_m"] > 0.05:
            b.append((FEHLER, d["id"], "Fuss-Punkt nicht hinter dem Lippen-Punkt"))


def quell_abstuerze(lauf, quellen):
    """Abstuerze eines Laufs neu aus der Quelle: Liste (id, fall, rampe, z_oben, z_unten, s_lokal) oder None/'ohne'."""
    q = lauf.get("quelle") or {}
    if "plan" in q:
        if not quellen.get("gefaelle"):
            return "ohne"
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
    if "orte" in q:
        if not quellen.get("sehens"):
            return "ohne"
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
                    return [("%s_S%02d" % (lauf["id"], k), float(st["fall_m"]), st.get("art") == "schnelle",
                             float(st["lippe_cm"][2]), float(st["fuss_cm"][2]), None)
                            for k, st in enumerate(w.get("stufen") or []) if st.get("lippe_cm") and st.get("fuss_cm")]
        return None
    return []


def pruefe_faelle(g, quellen, regeln, b):
    schw = regeln["fall_schwelle_m"]
    ab = {d["id"]: d for d in g["abstuerze"]}
    fl = {f["id"]: f for f in g["faelle"]}
    br = {x["id"] for x in g["bereiche"]}
    for l_ in g["laeufe"]:
        qa = quell_abstuerze(l_, quellen)
        if qa == "ohne":
            quellen["_ohne"] = quellen.get("_ohne", 0) + 1
            continue
        if qa is None:
            b.append((WARNUNG, l_["id"], "Quelle nicht gefunden - Stufen nicht gegen die Quelle geprueft"))
            continue
        off = l_["s_m"][0] - l_["s_quelle_m"][0]
        weg = set(l_.get("abstuerze_entfallen") or [])
        for fid, fall, rampe, zo, zu, s_ in qa:
            if fid in weg:
                if s_ is not None and l_["s_quelle_m"][0] + 0.05 < s_ < l_["s_quelle_m"][1] - 0.05:
                    b.append((FEHLER, fid, "Stufe als entfallen markiert, liegt aber im behaltenen Teil des Laufs"))
                continue
            d = ab.get(fid)
            if d is None:
                b.append((FEHLER, fid, "Stufe der Quelle fehlt in abstuerze"))
                continue
            if abs(d["z_oben_cm"] - zo) > 2.0 or abs(d["z_unten_cm"] - zu) > 2.0:
                b.append((FEHLER, fid, "Lippe/Fuss-Hoehe weicht von der Quelle ab"))
            if s_ is not None and abs(d["s_lippe_m"] - (s_ + off)) > 0.06 and s_ > l_["s_quelle_m"][0] + 0.05:
                b.append((FEHLER, fid, "Lippe s %.2f statt %.2f" % (d["s_lippe_m"], s_ + off)))
            if fall >= schw - 1e-9 and not rampe and fid not in fl:
                b.append((FEHLER, fid, "Stufe %.2f m >= %.1f m ohne Fall-Eintrag" % (fall, schw)))
    for f in g["faelle"]:
        if f["id"] not in ab:
            b.append((FEHLER, f["id"], "Fall ohne Absturz"))
            continue
        d = ab[f["id"]]
        if f["punkt_lippe"] != d["punkt_lippe"] or f["punkt_fuss"] != d["punkt_fuss"]:
            b.append((FEHLER, f["id"], "Lippe/Fuss-Punkt des Falls != Absturz"))
        if f["fall_m"] < schw - 1e-9:
            b.append((FEHLER, f["id"], "Fall %.2f m < Schwelle" % f["fall_m"]))
        for k in ("bereich_oben", "bereich_unten"):
            if f[k] is not None and f[k] not in br:
                b.append((FEHLER, f["id"], "%s %s existiert nicht" % (k, f[k])))
        soll, _ = fx.vorhang_regel({"rampe": False, "teil": f["teil"], "fall_m": f["fall_m"], "versatz_m": f.get("versatz_m"),
                                    "art": f["art"], "holz": f.get("holzstufe")}, regeln)
        if bool(f.get("vorhang")) != soll:
            b.append((FEHLER, f["id"], "vorhang=%s, Regel 16b ergibt %s" % (f.get("vorhang"), soll)))
        if f.get("vorhang"):
            if not any(s["art"] == "aufprallteppich" for s in f.get("schaum_objekte") or []):
                b.append((FEHLER, f["id"], "Vorhang-Fall ohne Aufprallteppich"))
            if not f["kaskadennetz"].get("bereich_s_m"):
                b.append((FEHLER, f["id"], "Vorhang-Fall ohne Kaskadennetz-Bereich"))
        else:
            if f.get("schaum_objekte"):
                b.append((FEHLER, f["id"], "Schaumobjekte an einem Fall ohne Vorhang"))
            if f["kaskadennetz"].get("bereich_s_m"):
                b.append((FEHLER, f["id"], "Kaskadennetz-Bereich an einem Fall ohne Vorhang"))


def pruefe_laeufe_bereiche(g, b):
    # Laeufe und Toepfe (16d) hintereinander: Topf fuellt die Luecke zwischen Zulauf und Abfluss bzw. Anfang/Ende
    L = sorted([dict(l_, _topf=False) for l_ in g["laeufe"]] +
               [{"id": "Topf " + tp["see"], "s_m": tp["s_m"], "_topf": True} for tp in g.get("toepfe") or []],
               key=lambda x: (x["s_m"][0], x["s_m"][1]))
    for i in range(1, len(L)):
        luecke = 0.011 if (L[i]["_topf"] or L[i - 1]["_topf"]) else 15.0
        if L[i]["s_m"][0] < L[i - 1]["s_m"][1] - 0.011 or L[i]["s_m"][0] - L[i - 1]["s_m"][1] > luecke:
            b.append((FEHLER, g["id"], "Laeufe %s -> %s nicht hintereinander" % (L[i - 1]["id"], L[i]["id"])))
    if abs(L[0]["s_m"][0]) > 0.011 or abs(L[-1]["s_m"][1] - g["laenge_m"]) > 0.011:
        b.append((FEHLER, g["id"], "Laeufe decken das Gewaesser nicht von 0 bis laenge_m"))
    pruefe_toepfe(g, b)
    br = g["bereiche"]
    fl = {f["id"]: f for f in g["faelle"]}
    for i in range(1, len(br)):
        of = br[i]["oben_fall"]
        if of in fl:
            if abs(br[i - 1]["s_m"][1] - fl[of]["s_lippe_m"]) > 0.02 or abs(br[i]["s_m"][0] - fl[of]["s_fuss_m"]) > 0.02:
                b.append((FEHLER, br[i]["id"], "Bereich-Grenze an Fall %s passt nicht zu Lippe/Fuss" % of))
        elif abs(br[i]["s_m"][0] - br[i - 1]["s_m"][1]) > 0.02:
            b.append((FEHLER, br[i]["id"], "Luecke zwischen Bereichen"))
    rest = regeln_global["abschnitt"]["rest_am_laufende_m"]
    iv = _vereinigt([tuple(x["s_m"]) for x in br] + [(f["s_lippe_m"], f["s_fuss_m"]) for f in g["faelle"]])
    if not iv or iv[0][0] > rest + 0.01 or g["laenge_m"] - iv[-1][1] > rest + 0.01 or len(iv) > 1:
        b.append((FEHLER, g["id"], "Bereiche und Faelle decken das Gewaesser nicht lueckenlos (%s)" % iv[:3]))
    for x in br:
        if x.get("rolle") not in ("becken", "rinne", "gerinne", "lauf", "topf"):
            b.append((FEHLER, x["id"], "Bereich-Rolle %r" % x.get("rolle")))


def pruefe_toepfe(g, b):
    """16d: Topf = Bereich mit Rolle topf, Splinepunkt in der Topfmitte auf dem Spiegel, SWR-Rechteck schliesst den Topf
    ein, kein WaterBodyLake; Groesse < Grenze."""
    mx = fx.toepfe_max(regeln_global)
    sp = g["water_body"]["spline"]
    P = np.asarray(sp["punkte"], float)
    ss = np.asarray(sp["punkte_s_m"], float)
    rol = sp["punkt_rollen"]
    br_topf = {x.get("topf"): x for x in g["bereiche"] if x.get("rolle") == "topf"}
    for tp in g.get("toepfe") or []:
        sid = tp["see"]
        if tp.get("ausdehnung_m", 1e9) >= mx:
            b.append((FEHLER, sid, "Topf %.1f m >= Grenze %.0f m" % (tp["ausdehnung_m"], mx)))
        if tp.get("water_body_lake") is not False:
            b.append((FEHLER, sid, "Topf ohne water_body_lake: false"))
        x = br_topf.get(sid)
        if x is None:
            b.append((FEHLER, sid, "kein Bereich mit Rolle topf"))
        elif x["s_m"][0] > tp["s_m"][0] + 0.06 or x["s_m"][1] < tp["s_m"][1] - 0.06:
            b.append((FEHLER, sid, "Topf-Bereich %s deckt den Topf %s nicht" % (x["s_m"], tp["s_m"])))
        m = (ss >= tp["s_m"][0] - 0.011) & (ss <= tp["s_m"][1] + 0.011)
        mitte = [i for i in np.where(m)[0] if abs(P[i, 0] - tp["mitte_cm"][0]) < 1.0 and abs(P[i, 1] - tp["mitte_cm"][1]) < 1.0]
        if not mitte and not any(rol[i] == "topf" for i in np.where(m)[0]):
            b.append((FEHLER, sid, "kein Splinepunkt im Topf"))
        if (np.abs(P[m, 2] - tp["spiegel_cm"]) > 3.0).any():
            b.append((FEHLER, sid, "Splinepunkte im Topf nicht auf dem Spiegel %.0f cm" % tp["spiegel_cm"]))
        r = tp["rechteck_cm"]
        for e in g.get("swr_bereiche") or []:
            if e["s_sim_m"][0] - 0.011 <= tp["s_m"][0] and tp["s_m"][1] <= e["s_sim_m"][1] + 0.011:
                q = e["rechteck_cm"]
                if q[0] > r[0] + 1.0 or q[1] > r[1] + 1.0 or q[2] < r[2] - 1.0 or q[3] < r[3] - 1.0:
                    b.append((FEHLER, sid, "SWR-Rechteck %s schliesst den Topf %s nicht ein" % (e["id"], r)))


def pruefe_swr(g, ss, P, regeln, b):
    S = regeln["swr"]
    T = S["teilung"]
    gid = g["id"]
    E = g.get("swr_bereiche") or []
    if not E:
        b.append((FEHLER, gid, "keine swr_bereiche"))
        return
    wbr = g["water_body"]["id"]
    L = g["laenge_m"]
    ue = T["ueberlappung_m"] / 2.0
    n = len(E)
    if abs(E[0]["s_m"][0]) > 0.011 or abs(E[-1]["s_m"][1] - L) > 0.011:
        b.append((FEHLER, gid, "SWR-Bereiche decken das Gewaesser nicht (0-%.2f)" % L))
    abd = sorted((e["s_sim_m"][0], e["s_sim_m"][1]) for e in E)
    reich = 0.0
    for a, c in abd:
        if a > reich + 0.011:
            b.append((FEHLER, gid, "Luecke in der SWR-Abdeckung bei s %.2f" % reich))
        reich = max(reich, c)
    if reich < L - 0.011:
        b.append((FEHLER, gid, "SWR-Abdeckung endet bei s %.2f" % reich))
    for x in g["bereiche"]:
        if not any(a - 0.011 <= x["s_m"][0] and x["s_m"][1] <= c + 0.011 for a, c in _vereinigt(abd)):
            b.append((FEHLER, x["id"], "Bereich nicht von einem SWR-Bereich abgedeckt"))
        soll = [e["id"] for e in E if e["s_m"][0] < x["s_m"][1] - 1e-6 and e["s_m"][1] > x["s_m"][0] + 1e-6] or None
        if soll is not None and x.get("swr_bereiche") != soll:
            b.append((FEHLER, x["id"], "swr_bereiche %s statt %s" % (x.get("swr_bereiche"), soll)))
    abst = g["abstuerze"]
    ids = [(gid if n == 1 else "%s_T%02d" % (gid, k)) for k in range(n)]
    for k, e in enumerate(E):
        sw = e["swr"]
        if e["id"] != ids[k] or sw["id"] != "SWR_" + ids[k]:
            b.append((FEHLER, e["id"], "ID passt nicht (soll %s / SWR_%s)" % (ids[k], ids[k])))
        if sw["source_river_water_bodies"] != [wbr] or sw["sink_river_water_bodies"] != [wbr]:
            b.append((FEHLER, e["id"], "Quelle/Senke != der eine WaterBodyRiver %s" % wbr))
        if k > 0 and abs(E[k - 1]["s_m"][1] - e["s_m"][0]) > 0.011:
            b.append((FEHLER, e["id"], "Kette der SWR-Bereiche hat eine Luecke"))
        a_soll = max(0.0, e["s_m"][0] - (ue if k > 0 else 0.0))
        c_soll = min(L, e["s_m"][1] + (ue if k < n - 1 else 0.0))
        if abs(e["s_sim_m"][0] - a_soll) > 0.011 or abs(e["s_sim_m"][1] - c_soll) > 0.011:
            b.append((FEHLER, e["id"], "Simulationsbereich %s statt [%.2f, %.2f] (Ueberlappung)" % (e["s_sim_m"], a_soll, c_soll)))
        if k < n - 1:
            sn = e["s_m"][1]
            if any(d["s_lippe_m"] - T["naht_abstand_absturz_m"] + 0.01 < sn < d["s_fuss_m"] + T["naht_abstand_absturz_m"] - 0.01
                   for d in abst):
                b.append((FEHLER, e["id"], "Naht bei s %.1f an einer Stufe" % sn))
        i0, i1 = e["punkt_index"]
        j0, j1 = fx.kachel_index(ss, e["s_sim_m"][0], e["s_sim_m"][1])
        if (i0, i1) != (j0, j1):
            b.append((FEHLER, e["id"], "punkt_index %s statt %s" % ([i0, i1], [j0, j1])))
            continue
        box = fx.box_punkte(P, i0, i1)
        lx, ly = (box[2] - box[0]) / 100.0, (box[3] - box[1]) / 100.0
        achse = max(lx, ly)
        if abs(achse - sw["achse_m"]) > 0.011 or abs(lx - e["rechteck_m"][0]) > 0.011 or abs(ly - e["rechteck_m"][1]) > 0.011:
            b.append((FEHLER, e["id"], "Rechteck/Achse aus der Spline %.2f x %.2f, gespeichert %s / %.2f" % (lx, ly, e["rechteck_m"], sw["achse_m"])))
        res = sw["resolution_max_axis"]
        if res % S["resolution_schritt"] or not (S["resolution_min"] <= res <= S["resolution_max"]):
            b.append((FEHLER, e["id"], "resolution_max_axis %d nicht in [%d; %d] bzw. kein Vielfaches von %d"
                      % (res, S["resolution_min"], S["resolution_max"], S["resolution_schritt"])))
        zelle = achse / res
        if abs(zelle - sw["zelle_m"]) > 0.0011:
            b.append((FEHLER, e["id"], "zelle_m %.3f != Achse/Aufloesung %.3f" % (sw["zelle_m"], zelle)))
        zmax = S["zelle_max_bach_m"] if sw["typ"] == "bach" else S["zelle_max_fluss_m"]
        if zelle > zmax + S.get("zelle_toleranz_m", 0.005):
            b.append((FEHLER, e["id"], "Zelle %.3f m > %.2f m + Toleranz (%s)" % (zelle, zmax, sw["typ"])))
        ziel = S["zelle_ziel_bach_m"] if sw["typ"] == "bach" else S["zelle_ziel_fluss_m"]
        res_soll, _ = fx.zelle_fuer(achse, ziel, S)
        if res != res_soll:
            b.append((FEHLER, e["id"], "resolution_max_axis %d, Regel ergibt %d" % (res, res_soll)))
        if bool(e.get("geteilt")) != (n > 1):
            b.append((FEHLER, e["id"], "geteilt-Kennung passt nicht"))
        wh = e.get("hindernis_akteur")
        if wh and wh["id"] not in sw["bottom_contour_actors"]:
            b.append((FEHLER, e["id"], "eigener Hindernis-Akteur fehlt in bottom_contour_actors"))
        if not e.get("fingerabdruck"):
            b.append((FEHLER, e["id"], "kein Fingerabdruck"))
    # eine SWR, wenn das ganze Rechteck es erlaubt
    if n > 1:
        typen = {e["swr"]["typ"] for e in E}
        zmax = S["zelle_max_bach_m"] if "bach" in typen else S["zelle_max_fluss_m"]
        if fx.achse_von(fx.box_punkte(P, 0, len(P) - 1)) <= S["resolution_max"] * zmax - 0.5:
            b.append((FEHLER, gid, "geteilt, obwohl das ganze Rechteck mit %d Zellen <= %.2f m passt" % (S["resolution_max"], zmax)))
        b.append((HINWEIS, gid, "Simulation in %d SWR-Bereiche geteilt (Rechteck %.0f m): Naht lokal pruefen"
                  % (n, fx.achse_von(fx.box_punkte(P, 0, len(P) - 1)))))


def _vereinigt(iv):
    out = []
    for a, c in sorted(iv):
        if out and a <= out[-1][1] + 0.011:
            out[-1] = (out[-1][0], max(out[-1][1], c))
        else:
            out.append((a, c))
    return out


def pruefe_muendung(g, alle, seen_ids, b):
    mu = g["muendung"]
    gid = g["id"]
    if mu.get("art") not in MUENDUNG_ARTEN:
        b.append((FEHLER, gid, "Muendung-Art %r" % mu.get("art")))
        return
    P = g["water_body"]["spline"]["punkte"]
    pk = mu.get("punkt_cm")
    if not pk or abs(pk[0] - P[-1][0]) > 1.0 or abs(pk[1] - P[-1][1]) > 1.0:
        b.append((FEHLER, gid, "Muendungspunkt != Spline-Ende"))
    if mu["art"] in ("fluss", "bach"):
        z = alle.get(mu.get("ziel"))
        if z is None:
            b.append((FEHLER, gid, "Muendungsziel %r fehlt" % mu.get("ziel")))
            return
        if z is g:
            b.append((FEHLER, gid, "Gewaesser muendet in sich selbst"))
        if not (0 <= mu["ziel_s_m"] <= z["laenge_m"] + 0.01):
            b.append((FEHLER, gid, "ziel_s_m ausserhalb des Ziels"))
        if not any(x["gewaesser"] == gid for x in z["zufluesse"]):
            b.append((FEHLER, gid, "fehlt in zufluesse von %s" % z["id"]))
        Q = np.asarray(z["water_body"]["spline"]["punkte"], float) / 100.0
        d, halb, _, _ = streifen_alle((Q[:-1], Q[1:]), [pk[0] / 100.0], [pk[1] / 100.0])
        rnd = float((d - halb).min())
        tol = (mu.get("luecke_m") or 0.0) + 5.0
        if rnd > tol:
            b.append((FEHLER, gid, "Muendungspunkt %.1f m neben dem Wasser von %s (Toleranz %.1f m)" % (rnd, z["id"], tol)))
        if mu.get("luecke_m"):
            b.append((HINWEIS, gid, "Muendung in %s mit Luecke %.1f m (Vorschlag %s)" % (z["id"], mu["luecke_m"], kurz_vorschlag(mu))))
    elif mu["art"] == "see":
        if mu.get("ziel") not in seen_ids:
            b.append((FEHLER, gid, "See %r unbekannt" % mu.get("ziel")))
        if mu.get("ziel") in toepfe_global:
            b.append((FEHLER, gid, "Muendung in See %s, der ein Topf von %s ist" % (mu["ziel"], toepfe_global[mu["ziel"]])))
    elif mu["art"] == "topf":
        z = alle.get(mu.get("gewaesser"))
        if z is None or not any(tp["see"] == mu.get("ziel") for tp in z.get("toepfe") or []):
            b.append((FEHLER, gid, "Topf %r nicht in Gewaesser %r" % (mu.get("ziel"), mu.get("gewaesser"))))
    elif mu["art"] == "offen":
        b.append((HINWEIS, gid, "Muendung offen (%s), Vorschlag %s" % ((mu.get("naechster_lauf") or {}).get("lauf"), kurz_vorschlag(mu))))
    if mu["art"] == "offen" or mu.get("luecke_m"):
        pruefe_vorschlag(g, mu, alle, b)
    elif mu.get("vorschlag"):
        b.append((FEHLER, gid, "Vorschlag an einer Muendung ohne Luecke / nicht offen"))


def kurz_vorschlag(mu):
    v = mu.get("vorschlag")
    if not v:
        return "-"
    z = v.get("ziel") or {}
    return "%s %.0f m -> %s %s" % (v.get("methode"), v.get("laenge_m") or 0.0, z.get("art"), z.get("id"))


def pruefe_vorschlag(g, mu, alle, b):
    """16d: Vorschlag getrennt von der Spline; beginnt am Spline-Ende, z nie steigend, Punktabstand, Ziel erreicht."""
    gid = g["id"]
    v = mu.get("vorschlag")
    if not v:
        b.append((WARNUNG, gid, "kein Vorschlag fuer %s" % ("offenes Ende" if mu["art"] == "offen" else "Luecke")))
        return
    V = regeln_global["gewaesser"]["vorschlag"]
    soll = "offen" if mu["art"] == "offen" else "luecke"
    if v.get("art") != soll:
        b.append((FEHLER, gid, "Vorschlag-Art %r statt %s" % (v.get("art"), soll)))
    Q = np.asarray(v.get("punkte") or [], float)
    if len(Q) < 2 or Q.shape[1] < 3:
        b.append((FEHLER, gid, "Vorschlag mit < 2 Punkten"))
        return
    E = g["water_body"]["spline"]["punkte"][-1]
    if abs(Q[0, 0] - E[0]) > 1.0 or abs(Q[0, 1] - E[1]) > 1.0 or abs(Q[0, 2] - E[2]) > 1.0:
        b.append((FEHLER, gid, "Vorschlag beginnt nicht am Spline-Ende"))
    if (np.diff(Q[:, 2]) > 0.05).any():
        b.append((FEHLER, gid, "Vorschlag steigt"))
    d = np.hypot(*np.diff(Q[:, :2], axis=0).T) / 100.0
    if (d > V["punkt_abstand_m"] + 0.05).any():
        b.append((FEHLER, gid, "Vorschlag-Punkte %.1f m auseinander (> %.1f m)" % (float(d.max()), V["punkt_abstand_m"])))
    if abs(float(d.sum()) - (v.get("laenge_m") or 0.0)) > 0.05:
        b.append((FEHLER, gid, "Vorschlag laenge_m passt nicht"))
    z = v.get("ziel")
    if z is None:
        if soll == "luecke" or v.get("ziel_gefunden", True):
            b.append((FEHLER, gid, "Vorschlag ohne Ziel"))
        return
    x, y = Q[-1, 0], Q[-1, 1]
    if z["art"] in ("fluss", "bach"):
        zg = alle.get(z["id"])
        if zg is None:
            b.append((FEHLER, gid, "Vorschlag-Ziel %s fehlt" % z["id"]))
            return
        if zg is g:
            b.append((FEHLER, gid, "Vorschlag fuehrt in das eigene Gewaesser"))
        P2 = np.asarray(zg["water_body"]["spline"]["punkte"], float) / 100.0
        dd, halb, _, _ = streifen_alle((P2[:-1], P2[1:]), [x / 100.0], [y / 100.0])
        rnd = float((dd - np.maximum(halb, 2.0)).min())
        if rnd > V["raster_m"]:
            b.append((FEHLER, gid, "Vorschlag endet %.1f m neben dem Wasser von %s" % (rnd, z["id"])))
    elif z["art"] == "see":
        U = seen_umriss.get(z["id"])
        if U is not None:
            dd = fx.abstand_polygon(U, x, y)
            if dd > V["raster_m"]:
                b.append((FEHLER, gid, "Vorschlag endet %.1f m neben See %s" % (dd, z["id"])))
        if z["id"] in toepfe_global:
            b.append((FEHLER, gid, "Vorschlag-Ziel %s ist ein Topf" % z["id"]))
    elif z["art"] == "meer" and welt_global is not None:
        from sehens_lib import daten as _d
        w = welt_global
        r = int(math.ceil(V["raster_m"] / w.zelle_m))
        fi, fj = _d.m_zu_pixel(x / 100.0, y / 100.0, w.zelle_m)
        i0, j0 = int(round(float(fi))), int(round(float(fj)))
        if not np.asarray(w.meer)[max(i0 - r, 0):i0 + r + 1, max(j0 - r, 0):j0 + r + 1].any():
            b.append((FEHLER, gid, "Vorschlag endet nicht am Meer"))


def streifen(g):
    P = np.asarray(g["water_body"]["spline"]["punkte"], float) / 100.0
    if len(P) < 2:
        return None
    return P[:-1], P[1:]


def streifen_alle(st, x, y):
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
    ohne = {json.dumps(o["ref"], sort_keys=True): o for o in g.get("ohne_wasser_kollision") or []}
    ue_max = regeln["kollision"]["ueberspannt_unterkante_max_m"]
    for key, o in liste.items():
        if not o.get("wasser_kollision"):
            b.append((FEHLER, g["id"], "wasser_kollision != true: %s" % key))
        if pool is not None and key not in pool["refs"]:
            b.append((FEHLER, g["id"], "Verweis existiert nicht: %s" % key))
        if o["lage"] == "im_wasser" and o.get("unterkante_ueber_spiegel_m", 0.0) > ue_max + 0.005:
            b.append((FEHLER, g["id"], "ueberspanntes Objekt mit Wasser-Kollision: %s" % key))
    for key, o in ohne.items():
        if key in liste:
            b.append((FEHLER, g["id"], "Objekt in wasser_kollision UND ohne_wasser_kollision: %s" % key))
        if o.get("wasser_kollision") or o.get("grund") != "ueberspannt" or o["lage"] != "im_wasser" \
                or o.get("unterkante_ueber_spiegel_m", 0.0) <= ue_max - 0.005:
            b.append((FEHLER, g["id"], "ohne_wasser_kollision erfuellt die Regel 'ueberspannt' nicht: %s" % key))
    if pool is None:
        return
    A, B = st
    xmin, xmax = min(A[:, 0].min(), B[:, 0].min()) - 120, max(A[:, 0].max(), B[:, 0].max()) + 120
    ymin, ymax = min(A[:, 1].min(), B[:, 1].min()) - 120, max(A[:, 1].max(), B[:, 1].max()) + 120
    Pp = pool["p"]
    R = regeln["kollision"]
    kand = np.where(pool["fest"] & (Pp.cx >= xmin) & (Pp.cx <= xmax) & (Pp.cy >= ymin) & (Pp.cy <= ymax))[0]
    fehlt = []
    for c0 in range(0, len(kand), 256):
        kk = kand[c0:c0 + 256]
        d, halb, z, tf = streifen_alle(st, Pp.cx[kk], Pp.cy[kk])
        zlo = Pp.lo[kk, 2][:, None] / 100.0
        zhi = Pp.hi[kk, 2][:, None] / 100.0
        im = ((d < halb) & (zlo <= z + R["ueber_spiegel_max_m"]) & (zhi >= z - tf - R["unter_bett_toleranz_m"])).any(1)
        for k in kk[im]:
            key = json.dumps(Pp.ref(int(k)), sort_keys=True)
            if key not in liste and key not in ohne:
                fehlt.append(key)
    if fehlt:
        b.append((FEHLER, g["id"], "%d Objekte im Wasser ohne wasser_kollision, z. B. %s" % (len(fehlt), fehlt[0])))


def pruefe_schaum(g, b):
    st = streifen(g)
    if st is None:
        return
    pts, wer = [], []
    for f in g["faelle"]:
        if f["bereich_unten"] is None and f.get("schaum_objekte"):
            b.append((HINWEIS, f["id"], "Fuss am Gewaesserende (Muendung): Schaumobjekte dort nicht gegen die eigene Spline geprueft"))
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
    ok_xy = d <= halb + 0.5
    ok = (ok_xy & (np.abs(P[:, 2][:, None] - z) <= 0.5)).any(1)
    raus = np.where(~ok_xy.any(1))[0]
    if len(raus):
        b.append((FEHLER, g["id"], "%d Schaumpunkte ausserhalb des Wassers (z. B. %s)" % (len(raus), wer[raus[0]])))
    falsch_z = np.where(ok_xy.any(1) & ~ok)[0]
    if len(falsch_z):
        b.append((FEHLER, g["id"], "%d Schaumpunkte nicht auf dem Spiegel (z. B. %s)" % (len(falsch_z), wer[falsch_z[0]])))


def pruefe_hindernis_global(alle_swr, alle_kol, regeln, b):
    pflanze = re.compile(regeln["kollision"]["pflanze_muster"], re.I)
    in_wh, wh_ids = {}, set()
    for eid, (e, g) in alle_swr.items():
        wh = e.get("hindernis_akteur")
        if not wh:
            continue
        wh_ids.add(wh["id"])
        if wh["id"] != "WH_" + eid:
            b.append((FEHLER, eid, "Hindernis-Akteur heisst %s" % wh["id"]))
        n = 0
        for c in wh["komponenten"]:
            if pflanze.search(c["netz"].rsplit("/", 1)[-1]):
                b.append((FEHLER, eid, "Pflanzennetz im Hindernis-Akteur: %s" % c["netz"]))
            for inst in c["instanzen"]:
                in_wh.setdefault(json.dumps(inst["ref"], sort_keys=True), []).append(eid)
                n += 1
        for inst in wh["akteure_mit_tag"]:
            in_wh.setdefault(json.dumps(inst["ref"], sort_keys=True), []).append(eid)
        if n != wh["n_instanzen"] or len(wh["akteure_mit_tag"]) != wh["n_akteure_mit_tag"]:
            b.append((FEHLER, eid, "n_instanzen/n_akteure_mit_tag passen nicht zur Liste"))
    for key, vork in alle_kol.items():
        e_ = in_wh.get(key, [])
        if len(e_) != 1:
            b.append((FEHLER, vork[0][1], "Objekt in %d Hindernis-Akteuren (soll 1): %s" % (len(e_), key)))
            continue
        for o, gid in vork:
            if o.get("hindernis_akteur") != "WH_" + e_[0]:
                b.append((FEHLER, gid, "hindernis_akteur %s, Objekt steht in WH_%s" % (o.get("hindernis_akteur"), e_[0])))
    for key in in_wh:
        if key not in alle_kol:
            b.append((FEHLER, "WH", "Objekt ohne wasser_kollision im Hindernis-Akteur: %s" % key))
    for eid, (e, g) in alle_swr.items():
        for w in e["swr"]["bottom_contour_actors"]:
            if w not in wh_ids:
                b.append((FEHLER, eid, "bottom_contour_actors verweist auf fehlenden %s" % w))


regeln_global = None
toepfe_global = {}
seen_umriss = {}
welt_global = None


def main(argv=None):
    global regeln_global, welt_global
    ap = argparse.ArgumentParser(description="Pruefer Entscheidung 16 (fluss_sim v3)")
    ap.add_argument("aus")
    ap.add_argument("--gefaelle", default=None)
    ap.add_argument("--sehens", default=None)
    ap.add_argument("--sw-ordner", default=None)
    ap.add_argument("--regeln", default=fx.REGELN_STANDARD)
    ap.add_argument("--vergleich", default=None, help="zweiter Ausgabeordner: Dateien muessen byte-gleich sein")
    ap.add_argument("--daten2m", default=None)
    ap.add_argument("--daten1m", default=None)
    ap.add_argument("--gebaut", nargs="+", default=None, help="wie beim Exporter (nur zum Abgleich der Erkennung)")
    ap.add_argument("--einbau", default=None, help="wie beim Exporter (sehens_einbau/)")
    ap.add_argument("--ohne-erkennung", action="store_true")
    a = ap.parse_args(argv)
    regeln = fx.lese_json(a.regeln)
    regeln_global = regeln
    gesamt = {FEHLER: 0, WARNUNG: 0, HINWEIS: 0}
    quellen = {"gefaelle": a.gefaelle, "sehens": a.sehens}
    gef_plaene, eingabe_weg = fx.lauf_plaene(a.gefaelle)
    quellen["gef_plaene"] = gef_plaene
    pool = None
    if a.gefaelle or a.sehens:
        P = fx.Pool(regeln, fx.Masse())
        for lauf in sorted(gef_plaene):
            for pf in fx.feld_plaene(os.path.join(a.gefaelle, lauf, "instanzen"))[0]:
                P.lade_ebene(pf, "gefaelle/%s/instanzen/%s/plan.json" % (lauf, os.path.basename(os.path.dirname(pf))))
        if a.sehens:
            for biom in fx.BIOME:
                if not os.path.exists(os.path.join(a.sehens, biom, "orte.json")):
                    continue
                sw = fx.finde_sw(a.sehens, a.sw_ordner, biom)
                if sw:
                    for pf in fx.feld_plaene(sw)[0]:
                        P.lade_ebene(pf, "sw_%s/%s/plan.json" % (biom, os.path.basename(os.path.dirname(pf))))
        P.fertig()
        pool = {"p": P, "fest": P.fest, "refs": {json.dumps(P.ref(k), sort_keys=True) for k in range(len(P.recs))}}
    welt = None
    if a.daten2m or a.daten1m:
        from sehens_lib import daten
        welt = daten.lade(a.daten2m, a.daten1m, pfade=False)
    # alle Dateien laden
    alle, datei_von = {}, {}
    befunde_datei = {}
    for pf in dateien_finden(a.aus):
        d = fx.lese_json(pf)
        rel = os.path.relpath(pf, a.aus)
        b = befunde_datei.setdefault(rel, [])
        if d.get("format") != fx.FORMAT_VERSION:
            b.append((FEHLER, rel, "format %r" % d.get("format")))
        for g in d.get("gewaesser") or []:
            if g["id"] in alle:
                b.append((FEHLER, g["id"], "Gewaesser-ID doppelt"))
            alle[g["id"]] = g
            datei_von[g["id"]] = rel
    seen_ids = set()
    welt_global = welt
    seen_umriss.clear()
    if welt is not None:
        seen_ids |= {s["id"] for s in (welt.wasser_welt or {}).get("seen", []) or []}
        for s_ in (welt.wasser_welt or {}).get("seen", []) or []:
            if s_.get("umriss"):
                seen_umriss[s_["id"]] = np.asarray(s_["umriss"], float)[:, :2]
    if a.sehens:
        for biom in fx.BIOME:
            po = os.path.join(a.sehens, biom, "orte.json")
            if os.path.exists(po):
                for o in fx.lese_json(po).get("orte") or []:
                    seen_ids |= {"%s/%s" % (o["id"], w["id"]) for w in o.get("wasser") or [] if w.get("typ") == "see"}
                    for w in o.get("wasser") or []:
                        if w.get("typ") == "see" and w.get("umriss_cm"):
                            seen_umriss["%s/%s" % (o["id"], w["id"])] = np.asarray(w["umriss_cm"], float)[:, :2]
    if welt is None or not a.sehens:
        seen_ids |= {g["muendung"]["ziel"] for g in alle.values() if g["muendung"]["art"] == "see"}
    alle_swr, alle_kol, lauf_in = {}, {}, {}
    wbrs = {}
    toepfe_global.clear()
    for gid in sorted(alle):
        for tp in alle[gid].get("toepfe") or []:
            if tp["see"] in toepfe_global:
                befunde_datei[datei_von[gid]].append((FEHLER, tp["see"], "Topf in zwei Gewaessern"))
            toepfe_global[tp["see"]] = gid
    for gid in sorted(alle):
        g = alle[gid]
        b = befunde_datei[datei_von[gid]]
        wbrs.setdefault(g["water_body"]["id"], []).append(gid)
        for l_ in g["laeufe"]:
            lauf_in.setdefault(l_["id"], []).append(gid)
        r = pruefe_spline(g, regeln, b)
        if r is None:
            continue
        ss, P = r
        pruefe_stufen(g, ss, P, b)
        pruefe_laeufe_bereiche(g, b)
        pruefe_faelle(g, quellen, regeln, b)
        pruefe_swr(g, ss, P, regeln, b)
        pruefe_muendung(g, alle, seen_ids, b)
        pruefe_kollision(g, pool, regeln, b)
        pruefe_schaum(g, b)
        for e in g.get("swr_bereiche") or []:
            if e["id"] in alle_swr:
                b.append((FEHLER, e["id"], "SWR-ID doppelt"))
            alle_swr[e["id"]] = (e, g)
        for o in g["wasser_kollision"]:
            alle_kol.setdefault(json.dumps(o["ref"], sort_keys=True), []).append((o, g["id"]))
    for rel in sorted(befunde_datei):
        if befunde_datei[rel]:
            z = melde(befunde_datei[rel], rel)
            for k_ in gesamt:
                gesamt[k_] += z[k_]
    # ein Fluss je Gewaesser, jeder Lauf genau einmal
    b = []
    for w, gs in sorted(wbrs.items()):
        if len(gs) != 1:
            b.append((FEHLER, w, "WaterBodyRiver in %d Gewaessern: %s" % (len(gs), gs)))
    for l_, gs in sorted(lauf_in.items()):
        if len(gs) != 1:
            b.append((FEHLER, l_, "Lauf in %d Gewaessern: %s" % (len(gs), gs)))
    if welt is not None:
        soll = {f["id"] for f in (welt.wasser_welt or {}).get("fluesse", []) or []} | {x["id"] for x in welt.baeche or []}
        fehlt = sorted(soll - set(lauf_in))
        if fehlt:
            b.append((FEHLER, "Laeufe", "%d Welt-Laeufe in keinem Gewaesser, z. B. %s" % (len(fehlt), fehlt[:3])))
        else:
            b.append((HINWEIS, "Laeufe", "alle %d Welt-Laeufe in genau einem Gewaesser" % len(soll)))
    pruefe_hindernis_global(alle_swr, alle_kol, regeln, b)
    pv = os.path.join(a.aus, "vorschlaege.json")
    mit_v = {gid: g["muendung"]["vorschlag"] for gid, g in alle.items() if g["muendung"].get("vorschlag")}
    if not os.path.exists(pv):
        b.append((FEHLER, "vorschlaege.json", "fehlt"))
    else:
        vl = fx.lese_json(pv).get("vorschlaege") or []
        if {o["gewaesser"]: o["vorschlag"] for o in vl} != mit_v or len(vl) != len(mit_v):
            b.append((FEHLER, "vorschlaege.json", "passt nicht zu muendung.vorschlag (%d / %d)" % (len(vl), len(mit_v))))
        else:
            arten = {}
            for o in vl:
                k_ = o["vorschlag"]["art"]
                arten[k_] = arten.get(k_, 0) + 1
            b.append((HINWEIS, "vorschlaege.json", "%d Vorschlaege %s (getrennt von der Spline)" % (len(vl), arten)))
    z = melde(b, "Ein Fluss je Gewaesser / Hindernis-Akteure (global)")
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
        if bl.get("format") != fx.BACK_FORMAT:
            b.append((FEHLER, "back_liste", "format %r" % bl.get("format")))
        ids = [k["swr_bereich"] for k in bl.get("swr_bereiche") or []]
        if set(ids) != set(alle_swr) or len(ids) != len(set(ids)):
            b.append((FEHLER, "back_liste", "SWR-Bereiche in back_liste != Dateien (%d / %d)" % (len(set(ids)), len(alle_swr))))
        gel = None
        if welt is not None:
            # Gelaende wie beim Export: Deltas schon gebauter Laeufe (back_liste.gelaende.deltas_ohne) nicht addieren
            gel = fx.Gelaende(welt)
            blg = bl.get("gelaende") or {}
            ohne = set(blg.get("deltas_ohne") or [])
            gi = fx.gelaende_laden(gel, a.gefaelle, gef_plaene, a.sehens, ohne_dateien=ohne)
            if len(gi["ohne_dateien"]) != len(ohne):
                b.append((FEHLER, "back_liste", "deltas_ohne nennt %d Dateien, gefunden %d" % (len(ohne), len(gi["ohne_dateien"]))))
            # Erkennung heute (lauf.json, --gebaut) gegen den Export
            if not a.ohne_erkennung:
                einbau = fx.einbau_ordner_finden(a.einbau, a.daten1m, a.gefaelle, a.sehens, a.sw_ordner)
                jetzt = fx.gelaende_laden(fx.Gelaende(welt), a.gefaelle, gef_plaene, a.sehens, a.gebaut or (), einbau)
                if set(jetzt["ohne_dateien"]) != ohne:
                    b.append((WARNUNG, "gebaut", "Erkennung jetzt %s, beim Export %s (lauf.json seit dem Export geaendert?)"
                              % (sorted(g["id"] for g in jetzt["gebaut"]), blg.get("gebaut"))))
            if blg.get("gebaut"):
                b.append((HINWEIS, "gebaut", "Gelaende-Deltas ohne %d Datei(en) gebauter Laeufe: %s" % (len(ohne), blg["gebaut"])))
        Pp = pool["p"] if pool else None
        ref_k = {json.dumps(Pp.ref(k), sort_keys=True): k for k in range(len(Pp.recs))} if Pp else {}
        kol_k = np.array(sorted(ref_k[k_] for k_ in alle_kol if k_ in ref_k), int) if Pp else np.zeros(0, int)
        for e in bl.get("swr_bereiche") or []:
            if e["swr_bereich"] not in alle_swr:
                continue
            ei, g = alle_swr[e["swr_bereich"]]
            wer = e["swr_bereich"]
            if e["fingerabdruck"] != ei.get("fingerabdruck") or e["bereich_cm"] != ei["bereich_cm"] \
                    or e["punkt_index"] != ei["punkt_index"]:
                b.append((FEHLER, wer, "Fingerabdruck/Bereich/punkt_index back_liste != fluss_sim.json"))
            i0, i1 = ei["punkt_index"]
            wb = g["water_body"]
            st = fx.fp_splines_text([(wb["id"], wb["spline"]["punkte"][i0:i1 + 1])], fpr["spline_quant_cm"])
            if hashlib.sha256(st.encode("ascii")).hexdigest() != e["teile"]["splines"]:
                b.append((FEHLER, wer, "Fingerabdruck Splines neu gerechnet != gespeichert"))
            bx = e["bereich_cm"]
            if Pp is not None:
                objs = []
                if len(kol_k):
                    lo, hi = Pp.lo[kol_k], Pp.hi[kol_k]
                    sel = (hi[:, 0] >= bx[0]) & (lo[:, 0] <= bx[2]) & (hi[:, 1] >= bx[1]) & (lo[:, 1] <= bx[3])
                    for kk in kol_k[sel]:
                        objs.append([Pp.recs[kk]["pfad"]] + [float(v) for v in Pp.recs[kk]["v"][:10]])
                ot = fx.fp_objekte_text(objs, fpr["pos_quant_cm"], fpr["quat_quant"], fpr["skala_quant"])
                if hashlib.sha256(ot.encode("ascii")).hexdigest() != e["teile"]["objekte"]:
                    b.append((FEHLER, wer, "Fingerabdruck Objekte neu gerechnet != gespeichert"))
            if gel is not None:
                x0, y0, rcm, H = gel.raster(bx)
                gt = fx.fp_gelaende_text(x0, y0, rcm, H, fpr["hoehe_quant_cm"])
                if hashlib.sha256(gt.encode("ascii")).hexdigest() != e["teile"]["gelaende"]:
                    b.append((FEHLER, wer, "Fingerabdruck Gelaende neu gerechnet != gespeichert"))
            kombi = hashlib.sha256(("%s\n%s\n%s\n%s\n" % (fpr["version"], e["teile"]["gelaende"], e["teile"]["splines"],
                                                          e["teile"]["objekte"])).encode("ascii")).hexdigest()
            if kombi != e["fingerabdruck"]:
                b.append((FEHLER, wer, "Gesamt-Fingerabdruck != SHA-256 der Teile"))
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
        b.append((HINWEIS, "Quellen", "%d Laeufe ohne --gefaelle/--sehens: Stufen nicht gegen die Quelle geprueft" % quellen["_ohne"]))
    z = melde(b, "back_liste/Determinismus")
    for k_ in gesamt:
        gesamt[k_] += z[k_]
    sys.stdout.write("[fluss_sim_pruefen] GESAMT: %d FEHLER, %d WARNUNG, %d HINWEIS\n" % (gesamt[FEHLER], gesamt[WARNUNG], gesamt[HINWEIS]))
    return 1 if gesamt[FEHLER] else 0


if __name__ == "__main__":
    sys.exit(main())
