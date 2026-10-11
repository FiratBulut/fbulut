#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plan_pruefen.py - prueft recherche/antworten/wasser_fx/plan.json (Auftrag 14).

  python -I plan_pruefen.py <repo-wurzel>

1) Assets: alle Niagara-Pfade (auch sehens13) in inventar_extra.json -> niagara, alle Klang-Cues in -> klaenge,
   alle Material-Pfade in -> wasser_materialien, alle Parameternamen im Master M_EL_Wasserfall2 (material_parameter.json).
2) Orte: jede Position liegt an ihrem Fall / ihrer Stufe (Abstand zu Lippe/Kante, gischt_cm, Fuss, Schnelle) und ist
   eindeutig zugeordnet (naechste Stufe = eigene Stufe); Drehung = Fliessrichtung.
3) Budgets: <= 3 Niagara je Fall/Gruppe, <= 6 gleichzeitig aktiv (Betrachter entlang des Bachs, Cull-Distanzen),
   GPU/kein Schatten/Sort 2; sehens13: <= 3 je Ort, kein Effekt doppelt zu unseren Zielen.
"""
import json
import math
import os
import sys

FEHLER, OK, WARN = [], [], []


def pruef(bed, text):
    (OK if bed else FEHLER).append(text)


def d2(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def d3(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    R = lambda *p: os.path.join(repo, "recherche", *p)
    plan = json.load(open(R("antworten", "wasser_fx", "plan.json"), encoding="utf-8"))
    inv = json.load(open(R("vorlagen", "daten", "inventar_extra.json"), encoding="utf-8"))
    mp = json.load(open(R("vorlagen", "daten", "material_parameter.json"), encoding="utf-8"))
    wf = json.load(open(R("vorlagen", "daten", "wasser_fx", "wasserfaelle.json"), encoding="utf-8"))["wasserfaelle"]
    netze = json.load(open(R("vorlagen", "daten", "wasser_fx", "stufen_netze.json"), encoding="utf-8"))
    teile = json.load(open(R("vorlagen", "daten", "wasser_fx", "stufen_fluss_teile.json"), encoding="utf-8"))

    # ---------- 1) Assets
    niag = set(inv["niagara"])
    cues = set(inv["klaenge"]["SoundCue"]["beispiele"])
    mats = set(inv["wasser_materialien"])
    eff = plan["effekte"]
    for e in eff:
        pruef(e["asset"] in niag, "Asset im Inventar: %s (%s)" % (e["asset"], e["ziel"]))
    for o in plan.get("sehens13", {}).get("orte", []):
        for e in o["effekte"]:
            pruef(e["asset"] in niag, "sehens13 Asset im Inventar: %s (%s)" % (e["asset"], o["ort"]))
    for k in plan["klang"]:
        pruef(k["asset"] in cues, "Klang im Inventar: %s" % k["asset"])
    master = [m for m in mp if m["name"] == "M_EL_Wasserfall2"][0]
    pnamen = set(master["skalar"]) | set(master["vektor"])
    for name, m in plan["material"].items():
        if not isinstance(m, dict):
            continue
        pruef(m["pfad"] in mats, "Material im Inventar: %s" % m["pfad"])
        for blk in ("parameter", "falls_probe_S01_gut"):
            for p in m.get(blk, {}):
                pruef(p in pnamen, "Parameter %s.%s existiert im Master" % (name, p))

    # ---------- Stufen-Referenz
    ab = {a["id"]: a for f in teile["fluesse"] for a in f["abschnitte"]}
    stufen = {}
    for v in netze["verzeichnis"].values():
        for s in v.get("stufen", []):
            if "fall_teil" in s:
                s = dict(s)
                s["_kante"] = ab[s["fall_teil"]["oberes_stueck"]]["punkte"][-2][:3]
                s["_unten"] = ab[s["fall_teil"]["unteres_stueck"]]["punkte"][0][:3]
            if s["id"] not in stufen or "_kante" in s:
                stufen[s["id"]] = s

    def richtung_ok(e, dx, dy):
        q = e["rot_q"]
        yaw = math.degrees(2 * math.atan2(q[2], q[3]))
        soll = math.degrees(math.atan2(dy, dx))
        dw = (yaw - soll + 180) % 360 - 180
        return abs(dw) < 3.0, dw

    # ---------- 2) Orte
    for e in eff:
        p, z, rolle = e["pos_cm"], e["ziel"], e["rolle"]
        if z in wf:
            w = wf[z]
            L, G = w["lippe"], w["gischt"]
            lip = (L["x_cm"], L["y_cm"], L["spiegel_m"] * 100)
            fz = w["becken"]["spiegel_cm"]
            r_becken = math.sqrt(w["becken"]["flaeche_m2"] / math.pi) * 100
            ok, dw = richtung_ok(e, *L["richtung_fall"])
            pruef(ok, "%s %s: Yaw = Fallrichtung (Abw. %.1f Grad)" % (z, rolle, dw))
            if rolle == "fall":
                a = d2(p, lip)
                pruef(a <= 100 and 0 <= p[2] - lip[2] <= 20, "%s Fall: %.2f m von der Lippe, %.0f cm ueber dem Spiegel" % (z, a / 100, p[2] - lip[2]))
            elif rolle == "aufprall":
                a = d2(p, (G["x_cm"], G["y_cm"]))
                af = d2(p, (w["fuss"]["x_cm"], w["fuss"]["y_cm"]))
                pruef(a <= 50 and 0 <= p[2] - fz <= 30, "%s Aufprall: %.2f m von gischt, %.2f m vom Fuss, %.0f cm ueber Becken" % (z, a / 100, af / 100, p[2] - fz))
            elif rolle == "wake":
                a = d2(p, (G["x_cm"], G["y_cm"]))
                pruef(300 <= a <= min(800, r_becken) and 0 <= p[2] - fz <= 10,
                      "%s Wake: %.1f m hinter gischt (Becken-Radius ~%.0f m), %.0f cm ueber Becken" % (z, a / 100, r_becken / 100, p[2] - fz))
            continue
        s = stufen[z]
        lippe, fuss = s["lippe_cm"], s["fuss_cm"]
        if "_kante" in s:
            dx, dy = s["_unten"][0] - s["_kante"][0], s["_unten"][1] - s["_kante"][1]
        else:
            dx, dy = fuss[0] - lippe[0], fuss[1] - lippe[1]
        l = math.hypot(dx, dy)
        dx, dy = dx / l, dy / l
        ok, dw = richtung_ok(e, dx, dy)
        pruef(ok, "%s %s: Yaw = Fliessrichtung (Abw. %.1f Grad)" % (z, rolle, dw))
        if rolle == "fall":
            k = s["_kante"]
            a = d2(p, k)
            pruef(a <= 50 and 0 <= p[2] - k[2] <= 10, "%s Fall: %.2f m von der Kante, %.0f cm ueber Spiegel oben" % (z, a / 100, p[2] - k[2]))
        elif rolle == "aufprall":
            g = s["gischt_cm"]
            a = d2(p, g)
            af = d2(g, fuss)
            zu = s["_unten"][2]
            pruef(a <= 30 and af <= 150 and 0 <= p[2] - zu <= 20,
                  "%s Aufprall: %.2f m von gischt_cm (gischt %.2f m vom Fuss), %.0f cm ueber Spiegel unten" % (z, a / 100, af / 100, p[2] - zu))
        elif rolle == "stroemung":
            k = s["_kante"]
            t = ((p[0] - k[0]) * dx + (p[1] - k[1]) * dy) / 100
            pruef(-1.5 <= t <= -0.5 and 0 <= p[2] - k[2] <= 15, "%s Stream: %.2f m stromauf der Kante" % (z, -t))
        elif rolle == "schnelle":
            vx, vy = fuss[0] - lippe[0], fuss[1] - lippe[1]
            ll = vx * vx + vy * vy
            t = ((p[0] - lippe[0]) * vx + (p[1] - lippe[1]) * vy) / ll
            quer = abs((p[0] - lippe[0]) * vy - (p[1] - lippe[1]) * vx) / math.sqrt(ll) / 100
            pruef(0.3 <= t <= 0.7 and quer <= 1.0, "%s Schnelle: t = %.2f auf Lippe->Fuss, %.2f m quer" % (z, t, quer))
        elif rolle == "wake":
            a = d2(p, fuss)
            pruef(100 <= a <= 300, "%s Wake: %.1f m hinter dem Fuss" % (z, a / 100))
        # eindeutige Zuordnung: naechste Stufe (Lippe/Fuss/Kante/Gischt) ist die eigene
        best, bd = None, 1e18
        for sid, t in stufen.items():
            for q in [t["lippe_cm"], t["fuss_cm"], t.get("_kante"), t.get("gischt_cm")]:
                if q is not None and d2(p, q) < bd:
                    bd, best = d2(p, q), sid
        pruef(best == z or rolle == "schnelle", "%s: naechste Stufe ist %s (%.1f m)" % (z, best, bd / 100))

    # ---------- 3) Budgets und Einstellungen
    je = {}
    for e in eff:
        je.setdefault(e["gruppe"], []).append(e)
        # Cull 30-150 m; E28: optionaler S02-Impact mit Cull 20 m erlaubt
        cmin = 20 if (e.get("optional") and e["asset"].endswith("NS_Impact_Small")) else 30
        pruef(e["sort_priority"] == 2 and e["cast_shadow"] is False and cmin <= e["cull_m"] <= 150,
              "%s %s: Sort 2, kein Schatten, Cull %d m" % (e["ziel"], e["rolle"], e["cull_m"]))
        if "cull_rueckfall_m" in e:
            # E27: Rueckfallstufe kleiner als der Cull, nicht unter 30 m
            pruef(30 <= e["cull_rueckfall_m"] < e["cull_m"], "%s %s: Rueckfall-Cull %d m < Cull %d m (E27)"
                  % (e["ziel"], e["rolle"], e["cull_rueckfall_m"], e["cull_m"]))
    for g, l in je.items():
        pruef(len(l) <= 3, "Gruppe %s: %d Niagara (<= 3)" % (g, len(l)))
    # gleichzeitig aktiv: Betrachter auf Augenhoehe ueber jedem Flusspunkt und 8 m seitlich
    betrachter = []
    for f in teile["fluesse"]:
        for a in f["abschnitte"]:
            for pt in a["punkte"]:
                for off in (-800, 0, 800):
                    betrachter.append((pt[0] + off, pt[1], pt[2] + 170))
                    betrachter.append((pt[0], pt[1] + off, pt[2] + 170))
    for s in stufen.values():
        for q in (s["lippe_cm"], s["fuss_cm"]):
            betrachter.append((q[0], q[1], q[2] + 170))
    mx, wo = 0, None
    for b in betrachter:
        n = sum(1 for e in eff if d3(b, e["pos_cm"]) <= e["cull_m"] * 100)
        if n > mx:
            mx, wo = n, b
    pruef(mx <= plan["budget"]["gleichzeitig_aktiv_ziel_max"], "C2/H4: hoechstens %d Systeme gleichzeitig aktiv (bei %s)" % (mx, [round(v) for v in wo]))
    mx_alle = sum(1 for e in eff if e["ziel"].startswith("F_ERLENBACH") and not e["optional"])
    OK.append("Info: C2 gesamt %d Systeme (%d Pflicht), H4 %d" % (sum(1 for e in eff if e["ziel"].startswith("F_ERLENBACH")), mx_alle,
                                                                 sum(1 for e in eff if e["ziel"].startswith("F_ELFENFLUSS"))))
    s13 = plan.get("sehens13", {}).get("orte", [])
    for o in s13:
        pruef(o["niagara_gesamt"] <= 3, "sehens13 %s: %d Niagara (<= 3)" % (o["ort"], o["niagara_gesamt"]))
        for e in o["effekte"]:
            nd = min(d3(e["pos_cm"], x["pos_cm"]) for x in eff) / 100
            if nd <= 150 and e.get("konflikt"):
                WARN.append("sehens13 %s %s: %.1f m zum naechsten A14-Effekt - als Konflikt markiert: %s" % (o["ort"], e["asset"].split("/")[-1], nd, e["konflikt"]))
            else:
                pruef(nd > 150, "sehens13 %s %s: %.0f m zum naechsten A14-Effekt (nicht doppelt)" % (o["ort"], e["asset"].split("/")[-1], nd))

    for t in OK:
        print("OK     ", t)
    for t in WARN:
        print("WARNUNG", t)
    for t in FEHLER:
        print("FEHLER ", t)
    print("\n%d OK, %d WARNUNG, %d FEHLER" % (len(OK), len(WARN), len(FEHLER)))
    sys.exit(1 if FEHLER else 0)


if __name__ == "__main__":
    main()
