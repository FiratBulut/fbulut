# -*- coding: utf-8 -*-
"""bach_anfaenge_pruefen.py - Pruefer fuer die Ausgabe von bach_anfaenge_plan.py (Auftrag 19).

Prueft (FEHLER = Exit 1):
  P1 alle 83 e-Faelle und alle 8 versickernden Enden des Befunds haben genau einen Plan, keine ersetzten C2-Laeufe
  P2 Splinepunkte: 6 Werte, endlich; Breite > 0; Tiefe >= 10 cm; Tempo > 0; Abstand je Punkt <= 12 m
  P3 Spiegel faellt in Fliessrichtung (Toleranz 1 cm) im neuen Kopf, im Anhang und im neuen Ende; Anschluss an den
     bleibenden Rest (Abstand <= 12 m, Kopf nicht tiefer als der Rest)
  P4 Quellen-Profil: Bach-Quellen beginnen mit <= 0,6 m; Tiefe im Anfangsbereich <= Breite/4 + 1 cm (Bach)
  P5 Instanzen: Netz im Inventar, kein Saegeschnitt, nicht gesperrt, Biom-Sperre (IcelandicBoulder), Quaternion normiert,
     Skala 0,3-3, z nicht mehr als 3 m vom Gelaende; Kollision genau fuer Felsen/Platten >= 0,8 m; kein Fels mit
     Kollision im Wasserband; <= 40 Instanzen und 0 Akteure je Ort
  P6 Effekte: Niagara nur /Game/NatureWaterFX/FX/ und nur an der Kaskade K1 (keine an Quellen, kein Schaum an Quellen)
  P7 FORMAT 3: je Feld plan.json, f32-Groesse = 40 Byte x anzahl, Summe = Instanzen, jede Instanz liegt in ihrem Feld
  P8 Neu-Backen-Liste enthaelt jedes Gewaesser mit Spline-Aenderung, kein ersetzter Lauf
  --vergleich DIR: zweite Ausgabe byte-gleich (alle Dateien)
Aufruf: python -I recherche/antworten/skripte/bach_anfaenge/bach_anfaenge_pruefen.py [--aus DIR] [--vergleich DIR2]
"""

import argparse
import hashlib
import json
import math
import os
import struct
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
SKRIPTE = os.path.dirname(HIER)
ANTWORTEN = os.path.dirname(SKRIPTE)
RECHERCHE = os.path.dirname(ANTWORTEN)
sys.path.insert(0, SKRIPTE)
sys.path.insert(0, HIER)

from sehens_lib import daten as D            # noqa: E402
from sehens_lib.inventar import Inventar     # noqa: E402

BEF = []


def melde(stufe, code, text):
    BEF.append((stufe, code, text))


def lese(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def abstand_band(x, y, pk):
    best = 1e18
    for i in range(len(pk) - 1):
        ax, ay, bx, by = pk[i][0] / 100, pk[i][1] / 100, pk[i + 1][0] / 100, pk[i + 1][1] / 100
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2))
        b = (pk[i][3] + t * (pk[i + 1][3] - pk[i][3])) / 200
        best = min(best, math.hypot(x - ax - t * dx, y - ay - t * dy) - b)
    return best


def pruefe_punkte(name, pk, fallend=True, abstand_max=12.0):
    for i, p in enumerate(pk):
        if len(p) != 6 or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in p):
            melde("FEHLER", "P2", "%s Punkt %d: 6 endliche Werte erwartet" % (name, i))
            return
        if p[3] <= 0 or p[4] < 10 - 1e-6 or p[5] <= 0:
            melde("FEHLER", "P2", "%s Punkt %d: Breite/Tiefe/Tempo %s" % (name, i, p[3:]))
    for i in range(1, len(pk)):
        d = math.hypot(pk[i][0] - pk[i - 1][0], pk[i][1] - pk[i - 1][1]) / 100
        if d > abstand_max:
            melde("FEHLER", "P2", "%s Punkt %d: Abstand %.1f m > %.0f m" % (name, i, d, abstand_max))
        if fallend and pk[i][2] > pk[i - 1][2] + 1.0:
            melde("FEHLER", "P3", "%s Punkt %d: Spiegel steigt (%.1f -> %.1f cm)" % (name, i, pk[i - 1][2], pk[i][2]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aus", default=os.path.join(ANTWORTEN, "bach_anfaenge"))
    ap.add_argument("--vergleich", default=None)
    ap.add_argument("--welt", default=os.path.join(RECHERCHE, "vorlagen", "daten", "sehens"))
    a = ap.parse_args()
    plan = lese(os.path.join(a.aus, "bach_anfaenge_plan.json"))
    R = lese(os.path.join(HIER, "bach_anfaenge_regeln.json"))
    befund = lese(os.path.join(RECHERCHE, "auftraege", "daten", "bach_anfaenge", "bach_anfaenge.json"))
    ersetzt = set(lese(os.path.join(SKRIPTE, "fluss_sim", "ersetzt.json"))["laeufe"])
    fels = lese(os.path.join(SKRIPTE, "felsgruppen_regeln.json"))
    ww = lese(os.path.join(a.welt, "wasser_welt.json"))
    ba = lese(os.path.join(a.welt, "baeche_alle.json"))
    spl = {f["id"]: f["punkte"] for f in ww["fluesse"]}
    spl.update({b["id"]: b["punkte"] for b in ba["baeche"]})
    inv = Inventar.lade()
    welt = D.lade(daten2m=a.welt)
    # P1
    e_ids = sorted(g["id"] for g in befund["gewaesser"] if g["klasse"] == "e")
    n_ids = sorted(g["id"] for g in befund["gewaesser"] if g["ende"]["klasse"] == "nichts")
    f_ids = [f["id"] for f in plan["faelle"]]
    if sorted(f_ids) != e_ids or len(set(f_ids)) != len(f_ids):
        melde("FEHLER", "P1", "Faelle %d statt %d (oder doppelt)" % (len(f_ids), len(e_ids)))
    if sorted(e["id"] for e in plan["enden"]) != n_ids:
        melde("FEHLER", "P1", "Enden passen nicht zum Befund (%d)" % len(n_ids))
    if len(e_ids) != 83 or len(n_ids) != 8:
        melde("WARNUNG", "P1", "Befund hat %d e-Faelle und %d versickernde Enden (erwartet 83/8)" % (len(e_ids), len(n_ids)))
    for f in plan["faelle"] + plan["enden"]:
        if f["id"] in ersetzt:
            melde("FEHLER", "P1", "ersetzter Lauf geplant: %s" % f["id"])
    # P2/P3/P4
    for f in plan["faelle"]:
        sp = f.get("spline")
        if not sp:
            if f["loesung"] not in ("kaskade_k1",) and not f.get("lokal"):
                melde("FEHLER", "P1", "%s ohne Spline-Aenderung" % f["id"])
            continue
        pk = sp["punkte"]
        pruefe_punkte(f["id"], pk, abstand_max=12.0 if f["art"] == "bach" else 20.0)
        alt = spl[f["id"]]
        k = sp["alt_bis_index_exkl"]
        if sp["alt_punkte"] != len(alt):
            melde("FEHLER", "P3", "%s: alt_punkte %d != %d" % (f["id"], sp["alt_punkte"], len(alt)))
        if k < len(alt):
            d = math.hypot(pk[-1][0] - alt[k][0], pk[-1][1] - alt[k][1]) / 100
            if d > 12.0 or pk[-1][2] < alt[k][2] - 1.0:
                melde("FEHLER", "P3", "%s: Kopf schliesst nicht an Punkt %d an (%.1f m, z %.1f/%.1f)" % (
                    f["id"], k, d, pk[-1][2], alt[k][2]))
        bach = f["art"] == "bach"
        if bach and f["loesung"] not in ("seeabfluss", "nebenarm") and pk[0][3] > 60.0 + 1e-6:
            melde("FEHLER", "P4", "%s: Quelle beginnt mit %.0f cm" % (f["id"], pk[0][3]))
        if bach:
            for i, p in enumerate(pk):
                if p[4] > max(10.0, p[3] / 4) + 1.0 and p[3] < 160:
                    melde("FEHLER", "P4", "%s Punkt %d: Tiefe %.0f cm > Breite/4 (%.0f cm)" % (f["id"], i, p[4], p[3]))
    k1 = plan["kaskade_k1"]
    pruefe_punkte("K1", k1["spline"]["punkte"])
    hf2 = spl["F_HAUPTFLUSS_2_B4"]
    hf3 = spl["F_HAUPTFLUSS_3_C4"]
    p0, pe = k1["spline"]["punkte"][0], k1["spline"]["punkte"][-1]
    if math.hypot(p0[0] - hf2[-1][0], p0[1] - hf2[-1][1]) / 100 > 12 or p0[2] > hf2[-1][2] + 1:
        melde("FEHLER", "P3", "K1 schliesst nicht an das Ende von F_HAUPTFLUSS_2_B4 an")
    if math.hypot(pe[0] - hf3[0][0], pe[1] - hf3[0][1]) > 1 or abs(pe[2] - hf3[0][2]) > 1:
        melde("FEHLER", "P3", "K1 endet nicht am Anfang von F_HAUPTFLUSS_3_C4")
    for e in plan["enden"]:
        sp = e.get("spline")
        if not sp:
            continue
        alt = spl[e["id"]]
        pk = sp["punkte"]
        if sp["modus"] == "anhaengen":
            pruefe_punkte("Ende " + e["id"], [alt[-1]] + pk)
        else:
            pruefe_punkte("Ende " + e["id"], alt[:sp["alt_ab_index"]][-1:] + pk)
            if pk[-1][3] > alt[-1][3] * R["enden"]["rest_breite_anteil"] + 1:
                melde("FEHLER", "P3", "Ende %s: Restbreite %.0f cm zu breit" % (e["id"], pk[-1][3]))
    for v in plan["verjuengung_alle"]:
        for i, b, t, vv in v.get("punkte", []):
            if b <= 0 or t < 10 - 1e-6 or vv <= 0:
                melde("FEHLER", "P2", "Verjuengung %s Punkt %d: %s" % (v["id"], i, [b, t, vv]))
        if v.get("punkte") and v["id"] in spl and len(spl[v["id"]]) <= v["punkte"][-1][0]:
            melde("FEHLER", "P2", "Verjuengung %s: Index ausserhalb" % v["id"])
    # P5
    nur = fels["netz_nur_biome"]["netze"]
    gesperrt = set(fels["gesperrt"]["netze"])
    QF = R["quellfassung"]
    netze = plan["netze"]
    geprueft = {}
    for key, n in netze.items():
        bef = inv.netz_pruefen(n["pfad"], wildnis=True)
        if bef or n["pfad"] in gesperrt or inv.saegeschnitt(n["pfad"]):
            melde("FEHLER", "P5", "Netz %s: %s" % (key, bef or "gesperrt/Saegeschnitt"))
        geprueft[key] = inv.netz(n["pfad"])
    for f in plan["faelle"] + plan["enden"]:
        li = f.get("instanzen", [])
        if len(li) > QF["max_instanzen"]:
            melde("FEHLER", "P5", "%s: %d Instanzen > %d" % (f["id"], len(li), QF["max_instanzen"]))
        if f.get("akteure", 0) != 0:
            melde("FEHLER", "P5", "%s: Akteure" % f["id"])
        pk_w = None
        if f.get("spline") and f["spline"].get("modus") == "kopf_ersetzen":
            pk_w = f["spline"]["punkte"]
        for ins in li:
            key, x, y, z, qx, qy, qz, qw, s = ins
            n = netze.get(key)
            if n is None:
                melde("FEHLER", "P5", "%s: Netz %s fehlt in 'netze'" % (f["id"], key))
                continue
            qn = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
            if abs(qn - 1) > 1e-3:
                melde("FEHLER", "P5", "%s: Quaternion nicht normiert" % f["id"])
            if not 0.3 <= s <= 3.0:
                melde("FEHLER", "P5", "%s: Skala %.2f %s" % (f["id"], s, key))
            hz = welt.hoehe_bei_m(x / 100, y / 100) * 100
            if abs(z - hz) > 300:
                melde("FEHLER", "P5", "%s: z %.0f cm weit vom Gelaende %.0f" % (f["id"], z, hz))
            biom = welt.biom_bei_m(x / 100, y / 100)
            if n["pfad"] in nur and biom not in nur[n["pfad"]]:
                melde("FEHLER", "P5", "%s: %s im Biom %s verboten" % (f["id"], key, biom))
            hoehe = geprueft[key]["groesse_m"][2] * s
            soll_kol = n["rolle"] in ("fels", "platte") and hoehe >= QF["kollision_ab_m"]
            if bool(n["kollision"]) != soll_kol:
                melde("FEHLER", "P5", "%s: Kollision %s passt nicht zu Hoehe %.2f m" % (f["id"], key, hoehe))
            if n["kollision"] and pk_w and abstand_band(x / 100, y / 100, pk_w) < 0.0:
                melde("FEHLER", "P5", "%s: Fels mit Kollision im Wasserband (%s)" % (f["id"], key))
    # P6
    for e in k1.get("effekte", []):
        if not e["asset"].startswith("/Game/NatureWaterFX/FX/"):
            melde("FEHLER", "P6", "Effekt nicht aus NatureWaterFX: %s" % e["asset"])
    if len(k1.get("effekte", [])) > 2 * R["kaskade_k1"]["effekte_max_faelle"]:
        melde("FEHLER", "P6", "zu viele Effekte an K1")
    for f in plan["faelle"] + plan["enden"]:
        if f.get("effekte") or "schaum" in json.dumps(f.get("quellfassung", {})).lower():
            melde("FEHLER", "P6", "%s: Effekt/Schaum an einer Quelle" % f["id"])
    # P7
    summe = 0
    for feld in plan["zusammenfassung"]["felder"]:
        d = os.path.join(a.aus, "instanzen", feld)
        pj = lese(os.path.join(d, "plan.json"))
        if pj["feld"] != feld:
            melde("FEHLER", "P7", "%s: plan.json feld %s" % (feld, pj["feld"]))
        n_feld = 0
        for key, info in pj["dateien"].items():
            p = os.path.join(d, key + ".f32")
            gr = os.path.getsize(p)
            if gr != 40 * info["anzahl"]:
                melde("FEHLER", "P7", "%s/%s: %d Byte fuer %d Instanzen" % (feld, key, gr, info["anzahl"]))
            with open(p, "rb") as fh:
                daten = fh.read()
            for k in range(info["anzahl"]):
                v = struct.unpack_from("<10f", daten, 40 * k)
                if D.feld_von_cm(v[0], v[1]) != feld:
                    melde("FEHLER", "P7", "%s/%s: Instanz %d liegt in %s" % (feld, key, k, D.feld_von_cm(v[0], v[1])))
            n_feld += info["anzahl"]
            if not inv.netz_pfad(info["pfad"]):
                melde("FEHLER", "P7", "%s/%s: Pfad nicht im Inventar" % (feld, key))
        if n_feld != pj["instanzen"]:
            melde("FEHLER", "P7", "%s: Summe %d != %d" % (feld, n_feld, pj["instanzen"]))
        summe += n_feld
    if summe != plan["zusammenfassung"]["instanzen"]:
        melde("FEHLER", "P7", "Instanzen gesamt %d != %d" % (summe, plan["zusammenfassung"]["instanzen"]))
    # P8
    backen = {x["gewaesser"] for x in plan["neu_backen"]["liste"]}
    for f in plan["faelle"]:
        if f.get("spline") and f.get("gewaesser") and f["gewaesser"] not in backen:
            melde("FEHLER", "P8", "%s (%s) fehlt in der Neu-Backen-Liste" % (f["gewaesser"], f["id"]))
    for e in plan["enden"]:
        if e.get("spline") and e["gewaesser"] not in backen:
            melde("FEHLER", "P8", "%s fehlt in der Neu-Backen-Liste" % e["gewaesser"])
    for g in ("F_HAUPTFLUSS_2", "F_HAUPTFLUSS_3"):
        if g not in backen:
            melde("FEHLER", "P8", "%s fehlt (K1)" % g)
    if backen & ersetzt:
        melde("FEHLER", "P8", "ersetzte Laeufe in der Liste: %s" % sorted(backen & ersetzt))
    # Vergleich
    if a.vergleich:
        def hashes(wurzel):
            out = {}
            for dp, dn, fn in os.walk(wurzel):
                for n in fn:
                    p = os.path.join(dp, n)
                    with open(p, "rb") as fh:
                        out[os.path.relpath(p, wurzel)] = hashlib.sha256(fh.read()).hexdigest()
            return out
        h1, h2 = hashes(a.aus), hashes(a.vergleich)
        if h1 != h2:
            diff = sorted(k for k in set(h1) | set(h2) if h1.get(k) != h2.get(k))
            melde("FEHLER", "V", "Laeufe nicht byte-gleich: %s" % diff[:10])
        else:
            melde("HINWEIS", "V", "zwei Laeufe byte-gleich (%d Dateien)" % len(h1))
    z = {"FEHLER": 0, "WARNUNG": 0, "HINWEIS": 0}
    for st, code, t in BEF:
        z[st] += 1
        print("%s %s %s" % (st, code, t))
    zs = plan["zusammenfassung"]
    print("Faelle %d, Enden %d, Instanzen %d, Neu backen %d" % (zs["faelle_e"], zs["enden"], zs["instanzen"], zs["neu_backen"]))
    print("FEHLER %d, WARNUNG %d, HINWEIS %d" % (z["FEHLER"], z["WARNUNG"], z["HINWEIS"]))
    sys.exit(1 if z["FEHLER"] else 0)


if __name__ == "__main__":
    main()
