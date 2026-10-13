# -*- coding: utf-8 -*-
"""ufer_plan_p2.py - 16h Nachtrag 3: Plan je Querschnitt fuer Erlenbach p2 nach bachbett_ufer_regeln.json, Teil C.2-C.4
(Lagen auf steilen Ufern, Kante mit Bewuchs, Steine) und felsige Prallhaenge ab 1,5 m (Erdanriss oben, Blockfuss).

Eingabe: Ferats Querschnitte (antworten/fluss_sim/p2_lokal/querschnitte_p2.json: s, seite, d ab der Wasserkante, z).
Ausgabe: antworten/ufer_p2/ufer_plan_p2.json in BACH-KOORDINATEN (s, seite, d). Ferats Kette (brush_uebernahme.py /
sehens_einbau) rechnet (s, seite, d) mit derselben p2-Spline in Weltkoordinaten um, aus der die Querschnitte stammen;
z = Gelaende - Einbettung x Netzhoehe (FORMAT.md §3). Instanzen gruppiert je Netz wie FORMAT.md §3 'dateien' (pfad, rolle,
gruppe, kollision, sichtweite), Netze und Pfade nur aus vorlagen/daten/netze.csv (geprueft, nicht gesperrt).

Deterministisch (Zufall aus s, Seite, Art, Nummer). Eingebaute Pruefung (Exit 1 bei FEHLER).

  python -I recherche/antworten/skripte/ufer_regeln/ufer_plan_p2.py [--abschnitte talkaskade kiesbett muendung] [--alle]
"""
import argparse
import csv
import hashlib
import json
import math
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import ufer_regeln as u  # noqa: E402

ANTW = os.path.normpath(os.path.join(HIER, "..", ".."))
DATEN = os.path.normpath(os.path.join(ANTW, "..", "vorlagen", "daten"))
SPALTEN = ["s_m", "seite", "d_m", "skala", "yaw_rel_grad", "kipp_grad", "einbettung", "h_ueber_spiegel_m"]


def zufall(*teile):
    h = hashlib.sha256("|".join(str(t) for t in teile).encode("utf-8")).digest()
    return int.from_bytes(h[:8], "little") / 2.0 ** 64


def zw(a, b, *teile):
    return a + (b - a) * zufall(*teile)


def netze_lesen():
    with open(os.path.join(DATEN, "netze.csv"), encoding="utf-8") as f:
        R = {r["name"]: r for r in csv.DictReader(f, delimiter=";")}
    with open(os.path.join(DATEN, "netz_sperre.json"), encoding="utf-8") as f:
        sperre = set(json.load(f))
    return R, sperre


def neigungen(P):
    """Neigung (Grad) je Punkt aus zentralen Differenzen."""
    out = []
    for i in range(len(P)):
        a, b = P[max(i - 1, 0)], P[min(i + 1, len(P) - 1)]
        dd = b[0] - a[0]
        out.append(math.degrees(math.atan2(abs(b[1] - a[1]), dd)) if dd > 0 else 0.0)
    return out


def wandhoehe(P, n, spiegel, d_max=6.0):
    """Hoehe der zusammenhaengenden Boeschung >= 30 Grad ueber dem Spiegel (Beginn bis 1 m ab der Kante)."""
    h = 0.0
    im = False
    for (d, z), g in zip(P, n):
        if d > d_max:
            break
        if g >= 30.0:
            if im or d <= 1.0:
                im = True
                h = max(h, z - spiegel)
        elif im:
            break
    return round(h, 3)


def schulter(P, n, d_max=6.0):
    """Boeschungsschulter: erster Punkt nach einer Strecke >= 30 Grad, an dem die Neigung unter 20 Grad faellt."""
    steil = False
    for (d, z), g in zip(P, n):
        if d > d_max:
            break
        if g >= 30.0:
            steil = True
        elif steil and g < 20.0:
            return d, z
    return None


def netz_fuer(liste, groesse, R, key):
    """Netz aus der Liste, dessen Skala (Zielgroesse / groesste Ausdehnung) in [0,35; 1,8] liegt; deterministisch."""
    ok = []
    for n in liste:
        r = R[n]
        m = max(float(r["groesse_x_m"]), float(r["groesse_y_m"]), float(r["groesse_z_m"]))
        sk = groesse / m
        if 0.35 <= sk <= 1.8:
            ok.append((n, round(sk, 3)))
    if not ok:
        return None, None
    return ok[int(zufall(*key) * len(ok)) % len(ok)]


class Plan:
    def __init__(self, R, sperre, regeln):
        self.R, self.sperre, self.regeln = R, sperre, regeln
        self.inst = {}
        self.fehler = []

    def setze(self, netz, rolle, gruppe, kollision, sicht, s, seite, d, skala, yaw, kipp, einb, h):
        if netz not in self.R:
            self.fehler.append("Netz %s nicht in netze.csv" % netz)
            return
        r = self.R[netz]
        if r["pfad"] in self.sperre:
            self.fehler.append("Netz %s gesperrt" % netz)
            return
        e = self.inst.setdefault(netz, {"pfad": r["pfad"], "rolle": rolle, "gruppe": gruppe, "kollision": kollision,
                                        "sichtweite": sicht, "groesse_m": [float(r["groesse_x_m"]), float(r["groesse_y_m"]),
                                                                            float(r["groesse_z_m"])], "eintraege": []})
        e["eintraege"].append([round(s, 2), seite, round(d, 2), round(skala, 3), round(yaw, 1), round(kipp, 1),
                               round(einb, 2), round(h, 2)])


def plane(Q, R, sperre, regeln, abschnitte, prallhaenge):
    C = regeln["C_ufer"]
    BK, ST = C["bewuchs_kante"], C["steine"]
    P_ = Plan(R, sperre, regeln)
    lagen, kanten = [], []
    zus = {}
    for x in Q:
        if x["abschnitt"] not in abschnitte:
            continue
        s, seite, ab = float(x["s"]), x["seite"], x["abschnitt"]
        prof = [(float(d), float(z)) for d, z in x["profil"]]
        sp = float(x["spiegel_m"])
        n = neigungen(prof)
        wh = wandhoehe(prof, n, sp)
        prall = any(a <= s <= b and seite == sd for a, b, sd in prallhaenge)
        felsig = prall and wh >= C["profil"]["lage"]["prallhang"]["felsig_ab_hoehe_m"]
        z_ = zus.setdefault(ab, {"querschnitte": 0, "lagen_segmente": 0, "kanten": 0, "prallhang_felsig": 0})
        z_["querschnitte"] += 1
        z_["prallhang_felsig"] += felsig
        # C.2 Lagen auf steilen Ufern (nur >= 20 Grad, bis 6 m); felsiger Prallhang: oben Erdanriss, darunter Fels
        seg = None
        for (d, z), g in zip(prof, n):
            if d > 6.0:
                break
            h = z - sp
            if g < 20.0:
                m, kl = None, None
            elif felsig and h >= wh - C["profil"]["lage"]["prallhang"]["erdanriss_m"][1]:
                m, kl = u._klasse(regeln, "erdanriss")["lagen"], "erdanriss_oben"
            elif felsig:
                m, kl = u._klasse(regeln, "fels_wand")["lagen"], "prallhang_fels"
            else:
                m = u.steil_mischung(regeln, g, wh)
                kl = "steil"
            if m is None:
                seg = None
                continue
            m = {k: v for k, v in sorted(m.items())}
            if seg and seg["lagen"] == m and seg["klasse"] == kl:
                seg["d_m"][1] = d
                continue
            seg = {"s_m": s, "seite": seite, "d_m": [d, d], "klasse": kl, "neigung_grad": round(g, 1), "lagen": m,
                   "streifen_vorn": h < 0.65}
            lagen.append(seg)
            z_["lagen_segmente"] += 1
        # C.3 Kante und Bewuchs
        sch = schulter(prof, n)
        fels_kante = wh >= 3.0
        if sch and not fels_kante:
            dk, zk = sch
            kanten.append({"s_m": s, "seite": seite, "d_m": dk, "h_m": round(zk - sp, 2), "wandhoehe_m": wh,
                           "prallhang": prall})
            z_["kanten"] += 1
            G = BK["ueberhaengendes_gras"]
            anz = int(round(zw(*G["anteil_kantenlaenge"], s, seite, "ga") * 2.0 / zw(*G["abstand_m"], s, seite, "gb")))
            for k in range(anz):
                netz = G["netze"][int(zufall(s, seite, "gn", k) * len(G["netze"]))]
                P_.setze(netz, "ufergras", "bb_kante", False, [0, 9000], s - 1.0 + 2.0 * (k + 0.5) / max(anz, 1),
                         seite, dk - zw(*G["ueberhang_m"], s, seite, "gu", k), zw(*G["skala"], s, seite, "gs", k),
                         zw(-180, 180, s, seite, "gy", k), -zw(*G["neigung_zum_wasser_grad"], s, seite, "gk", k), 0.02,
                         zk - sp)
            if prall and felsig:
                W = BK["wurzeln"]
                if zufall(s, seite, "wp") < 2.0 / zw(3.0, 6.0, s, seite, "wa"):
                    netz = W["netze"][int(zufall(s, seite, "wn") * len(W["netze"]))]
                    P_.setze(netz, "wurzel_bedingt_baum_6m", "bb_kante", False, [0, 15000], s + zw(-1, 1, s, seite, "ws"),
                             seite, dk - zw(*W["herausragen_m"], s, seite, "wr"), zw(0.6, 1.0, s, seite, "wk"),
                             zw(-30, 30, s, seite, "wy"), 0.0, 0.0, zk - sp - zw(*W["unter_kante_m"], s, seite, "wu"))
        # Moospolster (0-1,2 m ueber dem Spiegel)
        M = BK["moospolster"]
        if zufall(s, seite, "mp") < 2.0 * zw(*M["je_m_ufer"], s, seite, "mq"):
            kand = [(d, z) for d, z in prof if 0.0 <= z - sp <= 1.2 and d <= 3.0]
            if kand:
                d0, z0 = kand[int(zufall(s, seite, "md") * len(kand)) % len(kand)]
                for k in range(int(round(zw(M["gruppe"][0], M["gruppe"][1] + 0.99, s, seite, "mg")))):
                    netz = M["netze"][int(zufall(s, seite, "mn", k) * 5) % 5]          # nur Kleinzeug (Clumps, moss_01/02)
                    P_.setze(netz, "moos", "bb_kante", False, [0, 6000], s + zw(-0.8, 0.8, s, seite, "ms", k), seite,
                             d0 + zw(-0.3, 0.3, s, seite, "mo", k), zw(0.8, 1.4, s, seite, "mk", k),
                             zw(-180, 180, s, seite, "my", k), 0.0, 0.02, z0 - sp)
        # C.4 Steine
        if prall:
            F = ST["prallhang_fuss"]
            for k in range(1 if zufall(s, seite, "pb") < 0.75 else 2):
                gr = zw(*F["groesse_m"], s, seite, "pg", k)
                netz, sk = netz_fuer(["skjsL_tier_0", "texndcpda_tier_0", "SM_mountain_rock_big_02_2"], gr, R,
                                     (s, seite, "pn", k))
                if netz:
                    P_.setze(netz, "uferblock", "bb_steine", gr >= 0.8, [0, 45000], s + zw(-1, 1, s, seite, "ps", k),
                             seite, zw(*F["u_m"], s, seite, "pu", k), sk, zw(-20, 20, s, seite, "py", k),
                             zw(10, 20, s, seite, "pk", k), zw(*F["einbettung"], s, seite, "pe", k), 0.0)
            if felsig and wh >= 2.5 and zufall(s, seite, "uf") < 0.5:
                gr = zw(1.5, 2.5, s, seite, "ufg")
                netz, sk = netz_fuer(["SM_mountain_rock_big_02_2", "SM_mountain_rock_big_02_1"], gr, R, (s, seite, "ufn"))
                if netz:
                    P_.setze(netz, "uferfels", "bb_steine", True, [0, 60000], s, seite, zw(0.3, 1.0, s, seite, "ufd"), sk,
                             zw(-20, 20, s, seite, "ufy"), 0.0, zw(0.5, 0.6, s, seite, "ufe"), 0.0)
        elif sch or wh >= 0.5:
            K = ST["gerade"]
            if zufall(s, seite, "kp") < 2.0 * zw(*K["je_10m_ufer"], s, seite, "kq") / 10.0:
                gr = zw(*K["groesse_m"], s, seite, "kg")
                netz, sk = netz_fuer(K["netze"], gr, R, (s, seite, "kn"))
                if netz:
                    P_.setze(netz, "kopfstein", "bb_steine", False, [0, 9000], s + zw(-1, 1, s, seite, "ks"), seite,
                             zw(*K["u_m"], s, seite, "ku"), sk, zw(-20, 20, s, seite, "ky"), zw(10, 20, s, seite, "kk"),
                             zw(*K["einbettung"], s, seite, "ke"), 0.0)
        else:
            Gh = ST["gleithang"]
            for k in range(int(round(2.0 * zw(*Gh["kiespacks_je_10m"], s, seite, "gp") / 10.0 + zufall(s, seite, "gr")))):
                netz = Gh["netze"][int(zufall(s, seite, "gpn", k) * len(Gh["netze"]))]
                P_.setze(netz, "kiesel", "bb_steine", False, [0, 3500], s + zw(-1, 1, s, seite, "gps", k), seite,
                         zw(-0.3, 1.5, s, seite, "gpd", k), zw(1.0, 2.0, s, seite, "gpk", k), zw(-180, 180, s, seite, "gpy", k),
                         0.0, 0.3, 0.0)
    return P_, lagen, kanten, zus


def pruefe(P_, lagen, regeln):
    f = list(P_.fehler)
    namen = set(regeln["lagen_namen"])
    for L in lagen:
        if abs(sum(L["lagen"].values()) - 100.0) > 0.6:
            f.append("Lagen s %s %s: Summe %s" % (L["s_m"], L["seite"], sum(L["lagen"].values())))
        f += ["Lage %s unbekannt" % k for k in L["lagen"] if k not in namen]
    for netz, e in P_.inst.items():
        for r in e["eintraege"]:
            if r[2] < -0.6:
                f.append("%s bei s %s im Wasser (d %s)" % (netz, r[0], r[2]))
    return f


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quer", default=os.path.join(ANTW, "fluss_sim", "p2_lokal", "querschnitte_p2.json"))
    ap.add_argument("--aus", default=os.path.join(ANTW, "ufer_p2", "ufer_plan_p2.json"))
    ap.add_argument("--abschnitte", nargs="+", default=["talkaskade", "kiesbett", "muendung"])
    ap.add_argument("--alle", action="store_true", help="auch Bergrinne und Durchbruch (Ferat: sehen gut aus)")
    a = ap.parse_args(argv)
    regeln = u.lade()
    R, sperre = netze_lesen()
    Q = json.load(open(a.quer, encoding="utf-8"))["querschnitte"]
    ab = sorted({x["abschnitt"] for x in Q}) if a.alle else a.abschnitte
    ph = [(float(p["s_m"][0]), float(p["s_m"][1]), p["seite"]) for p in regeln["C_ufer"]["prallhaenge_p2"]["liste"]]
    P_, lagen, kanten, zus = plane(Q, R, sperre, regeln, set(ab), ph)
    f = pruefe(P_, lagen, regeln)
    for netz, e in P_.inst.items():
        e["anzahl"] = len(e["eintraege"])
    out = {"format": "ufer_plan_p2_v1", "stand": "16h Nachtrag 3", "quelle": os.path.relpath(a.quer, ANTW),
           "regeln": "bachbett_ufer_regeln.json (C_ufer)", "abschnitte": ab,
           "koordinaten": "Bach: s = m entlang p2 wie die Querschnitte, seite wie dort, d = m ab der Wasserkante (aussen +). "
                          "Welt-x/y ueber die p2-Spline (wie querschnitte_p2.json), z = Gelaende - einbettung x Netzhoehe "
                          "(Netzhoehe = groesse_m[2] x skala); h_ueber_spiegel_m nur zur Kontrolle.",
           "spalten": SPALTEN,
           "hinweise": ["Lippenzonen und Stufen-Widerlager sind in den Querschnitten nicht enthalten: Ferats Kette filtert mit "
                        "den Lippen des Bachdekors (bachbett_regeln.json lippe_*).",
                        "Farne werden nicht gesetzt: es fehlen Nordseite und Baumnaehe je Querschnitt.",
                        "rolle 'wurzel_bedingt_baum_6m': nur setzen, wenn ein Baum/Strauch <= 6 m von der Kante steht, "
                        "sonst durch ein Grasbueschel ersetzen.",
                        "streifen_vorn: der Uferstreifen (bachbett_regeln.json) bleibt dort vorn."],
           "zusammenfassung": {"je_abschnitt": zus, "lagen_segmente": len(lagen), "kanten": len(kanten),
                               "instanzen": {k: v["anzahl"] for k, v in sorted(P_.inst.items())},
                               "instanzen_summe": sum(v["anzahl"] for v in P_.inst.values())},
           "lagen": lagen, "kanten": kanten,
           "instanzen": {k: P_.inst[k] for k in sorted(P_.inst)}}
    os.makedirs(os.path.dirname(a.aus), exist_ok=True)
    with open(a.aus, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    print(json.dumps(out["zusammenfassung"], ensure_ascii=False))
    for x in f:
        print("FEHLER", x)
    print("[ufer_plan_p2] %d FEHLER" % len(f))
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
