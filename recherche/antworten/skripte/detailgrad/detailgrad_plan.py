# -*- coding: utf-8 -*-
"""detailgrad_plan.py - Auftrag 20: Detailgrad Bachufer (Felsen, Schutt, Stapel, Ritzen-Bewuchs, Wasserkante) fuer die p2-Talkaskade.

Grundlage ist der Bettplan p2 (skripte/p2_bett/p2_bettplan.py: Gelaende nach 6c/6f, Bettkante, Spiegel, Prall-/Gleitseite, Bloecke
im Bett). Er wird nicht doppelt gerechnet, sondern importiert. Dieser Planer setzt das UFER 0-10 m ab der Wasserkante (Grenze zu
Auftrag 21 Felsdeckung = 10 m) nach skripte/detailgrad/detailgrad_regeln.json, Biom tundra:
  1. Kantensaum aus Steinen 0,3-0,6 m + Kanten-Platten (Wasserkante aus Stein, Erdkante <= 5 %), Grasluecken 5-10 % (Gleitufer)
  2. Steine mit Fuss im Wasser (Oberkante 0,15-0,4 m ueber dem Spiegel)
  3. Haufen 5-15 Stueck im Uferband 1-3 m mit Luecken 1-3 m (Prallhang laenger/dichter), Wachstum mit Kontakt, 2. Lage verkeilt,
     gemeinsame Kippung je Haufen, Bodenplatte unter langen Haufen, Kleinschutt in den Fugen, Begleiter um Bloecke
  4. Gruppen im Hang 3-10 m, Felskoerper > 3 m am Prallhang, Wandverkleidung an Boeschungen >= 1 m / >= 30 Grad + Schuttband
  5. Bewuchs NACH dem Steinsatz: Gras in Ritzen, Farne in Luecken (Gleitufer; Nordufer-Zusatz), Ueberhang-Gras nur in Grasluecken,
     Moos-Polster erst ab 1 m ueber Spiegel, Buesche am Stein, Gehoelzgruppen auf flacher Schulter mit Steinen am Fuss
Ausgabe (--aus, Standard skripte/detailgrad/): plan_p2_talkaskade.json (Instanzen je Netz wie FORMAT §3 'dateien', Eintraege in
Bach-Koordinaten s/u; Welt ueber skripte/p2_bett/p2_bett_welt.py --instanzen-plan), Kennzahlen je 10 m und Seite, Pruefung;
Bilder (--bild, nach --bild-aus = antworten/detailgrad/): querschnitt_ufer.png, draufsicht_10m.png, stapel_beispiel.png.

  python -I recherche/antworten/skripte/detailgrad/detailgrad_plan.py [--aus DIR] [--bild] [--selbsttest]
"""
import argparse
import csv
import hashlib
import json
import math
import os
import sys

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
ANTW = os.path.normpath(os.path.join(HIER, "..", ".."))
DATEN = os.path.normpath(os.path.join(ANTW, "..", "vorlagen", "daten"))
sys.path.insert(0, os.path.join(ANTW, "skripte", "p2_bett"))
sys.path.insert(0, HIER)
import p2_bettplan as pb  # noqa: E402

REGELN = os.path.join(HIER, "detailgrad_regeln.json")
FORMAT_ID = "detailgrad_plan_v1"
SPALTEN = ["s_m", "u_m", "skala", "yaw_rel_grad", "kipp_grad", "einbettung", "groesse_m", "z_plan_m", "swr_hindernis",
           "nr", "z_absolut", "z_rel_m", "rolle", "seite", "d_m", "haufen", "lage"]
EBENE = {"stapel": "held", "kies": "kleinzeug", "schutt": "kleinzeug", "stein": "schutt", "fussstein": "schutt", "block": "schutt",
         "platte": "schutt", "haufen_kern": "schutt", "wand": "begleiter", "fels": "held", "gras_ritze": "bewuchs",
         "gras_kante": "bewuchs", "farn_ritze": "bewuchs", "farn": "bewuchs", "moos_boden": "kontakt", "busch": "bewuchs",
         "gehoelz": "held"}
KLASSE_SW = {"stapel": "K4_block", "kies": "K1_kies", "schutt": "K2_schutt", "stein": "K3_stein", "fussstein": "K3_stein", "block": "K4_block",
             "platte": "platte", "haufen_kern": "K4_block", "wand": "wand", "fels": "fels", "gras_ritze": "gras",
             "gras_kante": "gras", "farn_ritze": "farn", "farn": "farn", "moos_boden": "moos", "busch": "busch",
             "gehoelz": "gehoelz"}
NETZFORM = {"ab_m": 1.5, "verhaeltnis_min": 1.4}
STEINROLLEN = ("stein", "fussstein", "block", "haufen_kern", "stapel")


def zufall(*t):
    return pb.zufall("detailgrad", *t)


def zw(a, b, *t):
    return a + (b - a) * zufall(*t)


def r2(v, n=2):
    return float(round(float(v), n))


# ======================================================================================================================
class Gelaende:
    """Gelaende und Wasser aus dem Bettplan; jenseits des Plan-Rasters das Ist aus Ferats Querschnitten."""

    def __init__(self, X):
        self.X = X
        G = X["G"]
        self.S, self.U, self.Z, self.W = G["S"], G["U"], X["z_neu"], G["W"]
        self.EL, self.ER, self.UC = G["EL"], G["ER"], G["UC"]
        self.ist = X["ist"]
        self.pidx = G["pidx"]

    def zeile(self, s):
        return int(np.clip(round((s - self.S[0]) / pb.DS), 0, len(self.S) - 1))

    def z(self, s, u):
        if abs(u) <= self.U[-1] - 0.3:
            x = (s - self.S[0]) / pb.DS
            y = (u - self.U[0]) / pb.DU
            i0 = int(np.clip(math.floor(x), 0, len(self.S) - 2))
            j0 = int(np.clip(math.floor(y), 0, len(self.U) - 2))
            fx, fy = min(max(x - i0, 0.0), 1.0), min(max(y - j0, 0.0), 1.0)
            Z = self.Z
            return float(Z[i0, j0] * (1 - fx) * (1 - fy) + Z[i0 + 1, j0] * fx * (1 - fy) + Z[i0, j0 + 1] * (1 - fx) * fy +
                         Z[i0 + 1, j0 + 1] * fx * fy)
        sd = "links" if u > 0 else "rechts"
        Bo = float(np.interp(s, self.ist.s, self.ist.B))
        return self.ist.ufer(s, sd, abs(u) - Bo / 2.0)

    def kante(self, s, sg):
        i = self.zeile(s)
        return float(self.EL[i] if sg > 0 else self.ER[i])

    def u_von(self, s, sg, d):
        return self.kante(s, sg) + sg * d

    def spiegel(self, s, sg):
        i = self.zeile(s)
        e = self.kante(s, sg)
        j = int(np.clip(round((e - sg * 0.05 - self.U[0]) / pb.DU), 0, len(self.U) - 1))
        return float(self.W[i, j])

    def neigung(self, s, sg, d, h=0.5):
        za = self.z(s, self.u_von(s, sg, max(d - h, 0.0)))
        zb = self.z(s, self.u_von(s, sg, d + h))
        return math.degrees(math.atan2(abs(zb - za), (d + h) - max(d - h, 0.0)))

    def prallseite(self, s):
        i = self.zeile(s)
        j = int(np.argmin(np.abs(self.U - self.UC[i])))
        p = int(self.pidx[i, j])
        if 0 <= p < len(self.X["becken"]):
            return self.X["becken"][p]["prall"]
        return "links"

    def nahe_lippe(self, s, u, d):
        for L in self.X["lippen"]:
            if L.art == "bestand":
                continue
            if abs(s - float(L.linie(u, L.uc))) < d:
                return True
        return False


class Netze:
    def __init__(self):
        with open(os.path.join(DATEN, "netze.csv"), encoding="utf-8") as f:
            self.R = {r["name"]: r for r in csv.DictReader(f, delimiter=";")}
        with open(os.path.join(DATEN, "netz_sperre.json"), encoding="utf-8") as f:
            self.sperre = set(json.load(f))
        mp = os.path.join(DATEN, "netze_masse.json")
        self.masse = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}

    def gr(self, n):
        r = self.R[n]
        return float(r["groesse_x_m"]), float(r["groesse_y_m"]), float(r["groesse_z_m"])

    def waehle(self, liste, groesse, key, skala=(0.3, 1.8)):
        ok = []
        for n in liste:
            r = self.R.get(n)
            if r is None or r["pfad"] in self.sperre:
                continue
            gx, gy, gz = self.gr(n)
            if groesse > NETZFORM["ab_m"] and max(gx, gy) / max(gz, 1e-6) < NETZFORM["verhaeltnis_min"]:
                continue                                  # Netzform-Regel (Auftrag 21 / felsgruppen Runde 5)
            m = max(gx, gy, gz)
            sk = groesse / m
            if skala[0] <= sk <= skala[1]:
                ok.append((n, sk))
        if not ok:
            return None, None
        return ok[int(zufall(*key) * len(ok)) % len(ok)]


# ======================================================================================================================
class Plan:
    def __init__(self, R, N, G, X):
        self.R, self.N, self.G, self.X = R, N, G, X
        self.T = R["biome"]["tundra"]
        self.inst = []
        self.fehler = []
        self.abschnitte = []
        self.rhythmus = {}
        self.gleit_laenge = {}
        self.grasluecken = {}
        self.k3 = {}                                      # (seite, abschnitt) -> Steine 0,3-1 m im Band 0-3 m
        self.scheiben = {"links": [], "rechts": []}       # (s, d, r) belegte Kreise je Seite
        for x in [x for x in X["liste"] if x]:            # Bloecke des Bettplans belegen den Platz
            if x["rolle"] in ("kies",):
                continue
            for sd, sg in (("links", 1.0), ("rechts", -1.0)):
                d = sg * (x["u"] - G.kante(x["s"], sg))
                if -1.5 <= d <= 10.5:
                    self.scheiben[sd].append((x["s"], d, 0.45 * x["g"]))

    def abschnitt(self, s):
        for i, (a, b) in enumerate(self.abschnitte):
            if a <= s < b:
                return i
        return None

    # ---------------------------------------------------------------- Belegung
    def frei(self, sd, s, d, r, faktor=0.45, ausser=()):
        for (s2, d2, r2_) in self.scheiben[sd]:
            if (s2, d2) in ausser:
                continue
            if (s - s2) ** 2 + (d - d2) ** 2 < (faktor * (r + r2_)) ** 2:
                return False
        return True

    def setze(self, rolle, liste, groesse, key, sd, s, d, einb=0.0, yaw=0.0, kipp=0.0, z_abs=None, z_rel=None,
              haufen=-1, lage=1, skala_fest=None, belegen=True, skala=(0.3, 1.8), prio=0, deckel=None):
        G, N = self.G, self.N
        sg = 1.0 if sd == "links" else -1.0
        if skala_fest is not None:
            n = liste[int(zufall(*key) * len(liste)) % len(liste)]
            if n not in N.R or N.R[n]["pfad"] in N.sperre:
                self.fehler.append("Netz %s fehlt/gesperrt" % n)
                return None
            sk = skala_fest
        else:
            n, sk = N.waehle(liste, groesse, key, skala)
            if n is None:
                self.fehler.append("kein Netz fuer %s %.2f m" % (rolle, groesse))
                return None
        gx, gy, gz = N.gr(n)
        g = max(gx, gy, gz) * sk
        zaehlt = rolle in STEINROLLEN and 0.3 <= g < 1.0 and -0.6 <= d <= 3.0
        ai = self.abschnitt(s)
        if zaehlt and deckel is not None and ai is not None:
            a_, b_ = self.abschnitte[ai]
            hi = self.T["je_10m"]["K3_stein"][1] * (b_ - a_) / 10.0
            if deckel == "reserve":
                hi -= self.T["je_10m"]["fuss_im_wasser"][1] * (b_ - a_) / 10.0
            if self.k3.get((sd, ai), 0) >= math.floor(hi):
                return None
        if rolle == "platte":
            # Platten liegen in der Boeschung: X-Achse zum Wasser (yaw_rel = +90 links / -90 rechts), Nase um die Neigung nach
            # unten (kipp > 0 = Nase runter, wie p2_bett_welt.quat_yaw_pitch); halb gedreht mit negativer Neigung fuer Vielfalt
            ng = G.neigung(s, sg, max(d, 0.0), 0.6)
            dreh = zufall(*key, "dreh") < 0.5
            yaw = sg * 90.0 + (180.0 if dreh else 0.0) + zw(-25.0, 25.0, *key, "pyaw")
            kipp = (-ng if dreh else ng) + zw(-4.0, 4.0, *key, "pkipp")
        u = G.u_von(s, sg, d)
        zt = G.z(s, u)
        h = gz * sk
        if z_abs is not None:
            z = z_abs
        elif z_rel is not None:
            z = zt + z_rel
        else:
            z = zt - einb * h
        e = {"rolle": rolle, "netz": n, "skala": sk, "s": s, "u": u, "d": d, "seite": sd, "g": g, "h": h, "z": z,
             "top": z + h, "zt": zt, "einb": einb, "yaw": yaw, "kipp": kipp, "z_abs": z_abs is not None,
             "z_rel": z_rel, "haufen": haufen, "lage": lage, "kol": (g >= self.T["kollision_ab_m"] and rolle in
                                                                       ("stein", "fussstein", "block", "haufen_kern", "stapel",
                                                                        "wand", "fels", "gehoelz")),
             "hind": False, "flach": gz < 0.35 * max(gx, gy), "prio": prio}
        self.inst.append(e)
        if zaehlt and ai is not None:
            self.k3[(sd, ai)] = self.k3.get((sd, ai), 0) + 1
        if belegen:
            r = 0.5 * math.sqrt(gx * gy) * sk if rolle in ("platte", "wand", "fels") else 0.45 * g
            self.scheiben[sd].append((s, d, r * (0.6 if rolle in ("platte",) else 1.0)))
        return e


# ======================================================================================================================
def rhythmus(G, T, sd, s0, s1, seed):
    """Haufen/Luecken entlang s (je Seite): Liste (a, b, art) mit art 'haufen' oder 'luecke'."""
    H = T["haufen"]
    out, s, k = [], s0 + zw(0.0, 1.5, seed, "rh0", sd), 0
    while s < s1:
        prall = G.prallseite(s) == sd
        L = zw(*H["laenge_m"]["prall" if prall else "gleit"], seed, "rhL", sd, k)
        out.append((s, min(s + L, s1), "haufen", prall))
        s += L
        Lu = zw(*H["luecke_m"]["prall" if prall else "gleit"], seed, "rhG", sd, k)
        out.append((s, min(s + Lu, s1), "luecke", prall))
        s += Lu
        k += 1
    return out


def plane(seed="detailgrad|p2|talkaskade"):
    with open(REGELN, encoding="utf-8") as f:
        R = json.load(f)
    X = pb.rechne()
    G = Gelaende(X)
    N = Netze()
    P = Plan(R, N, G, X)
    T = P.T
    NR = R["netze_rollen"]
    s_a = X["rand"]["s0"] + 1.0
    s_b = X["rand"]["s1"] - 0.5
    abschnitte = []
    a = s_a
    while a < s_b - 1e-6:
        abschnitte.append((a, min(a + 10.0, s_b)))
        a += 10.0
    P.abschnitte = abschnitte
    for sd, sg in (("links", 1.0), ("rechts", -1.0)):
        rh = rhythmus(G, T, sd, s_a, s_b, seed)
        P.rhythmus[sd] = rh
        # ---- 1. Kantensaum + Grasluecken
        gl_anteil = zw(*T["kante"]["gras_ueberhang_anteil"], seed, "gl", sd)
        # Grasluecken (Ueberhang-Gras) nur am Gleitufer, 5-10 % von dessen Kantenlaenge, in Haufen-Luecken
        grasluecken = []
        gleit_l = sum(b_ - a_ for (a_, b_, art, prall) in rh if not prall)
        kand = sorted([(zufall(seed, "glp", sd, a_), a_, b_) for (a_, b_, art, prall) in rh if art == "luecke" and not prall
                       and b_ - a_ >= 0.8])
        summe = 0.0
        for (_, a_, b_) in kand:
            if summe >= gl_anteil * gleit_l:
                break
            m = (a_ + b_) / 2.0
            Lg = min(zw(0.8, 1.5, seed, "gll", sd, a_), b_ - a_ - 0.1)
            grasluecken.append((m - Lg / 2.0, m + Lg / 2.0))
            summe += Lg
        grasluecken.sort()
        P.gleit_laenge[sd] = gleit_l
        k = 0
        for (a_, b_, art, prall) in rh:
            if art != "luecke":
                continue
            s = a_ + zw(0.1, 0.4, seed, "s0", sd, a_)
            while s < b_ - 0.15:
                if any(x0 <= s <= x1 for x0, x1 in grasluecken):
                    s += 0.3
                    continue
                g = zw(0.3, 0.6, seed, "sg", sd, k)
                d = zw(*T["kante"]["saum_d_m"], seed, "sd", sd, k)
                if not G.nahe_lippe(s, G.u_von(s, sg, d), 0.35) and P.frei(sd, s, d, 0.45 * g, 0.5):
                    fam = "K3_plattig" if zufall(seed, "sf", sd, k) < 0.35 else ("K3_kantig" if zufall(seed, "sf2", sd, k) < 0.8
                                                                               else "K3_gerundet")
                    P.setze("stein", NR[fam], g, (seed, "sn", sd, k), sd, s, d, einb=zw(*T["eingraben"]["K3"], seed, "se", sd, k),
                            yaw=zw(-30, 30, seed, "sy", sd, k), kipp=zw(5, 20, seed, "sk", sd, k), haufen=-2, deckel="reserve")
                s += zw(*T["kante"]["saum_abstand_m"], seed, "sa", sd, k)
                k += 1
        P.grasluecken[sd] = grasluecken
        # ---- 2. Haufen im Uferband (und Kanten-Platten / Fuss im Wasser je Abschnitt)
        hk = 0
        for (a_, b_, art, prall) in rh:
            if art != "haufen":
                continue
            L = b_ - a_
            H = T["haufen"]
            n = int(round(clamp_i(L * zw(*H["stuecke_je_m"], seed, "hn", sd, hk), H["stuecke"][0], H["stuecke"][1] - 2)))
            sm = (a_ + b_) / 2.0
            dm = zw(*H["mitte_d_m"], seed, "hd", sd, hk)
            dip = zw(*H["kipp_gruppe_grad"], seed, "hdip", sd, hk)
            dip_yaw = zw(-40, 40, seed, "hdy", sd, hk)
            if L >= H["bodenplatte_ab_laenge_m"]:
                P.setze("platte", NR["platte_boden"], 0.0, (seed, "hpl", sd, hk), sd, sm, dm, einb=zw(*T["eingraben"]["platte"], seed, "hpe", sd, hk),
                        yaw=zw(-90, 90, seed, "hpy", sd, hk), kipp=dip * 0.5, haufen=hk, skala_fest=zw(0.18, 0.3, seed, "hps", sd, hk),
                        belegen=False)
            stuecke = []
            n_keim = max(1, int(round(L / 1.4)))
            for i in range(n):
                g = [0.35, 0.55, 0.8][int(zufall(seed, "hgs", sd, hk, i) * 3) % 3] * zw(0.85, 1.15, seed, "hgf", sd, hk, i)
                fam = "K3_plattig" if zufall(seed, "hf", sd, hk, i) < 0.4 else ("K3_kantig" if zufall(seed, "hf2", sd, hk, i) < 0.85
                                                                              else "K3_gerundet")
                for v in range(10):
                    if i < n_keim and v < 4:
                        # Keime entlang der Haufenlaenge (Haufen 1,5-5 m lang, nicht nur ein runder Klumpen)
                        s_ = a_ + (i + 0.5) * L / n_keim + zw(-0.25, 0.25, seed, "hks", sd, hk, i, v)
                        d_ = dm + zw(-0.5, 0.5, seed, "hkd", sd, hk, i, v)
                    elif not stuecke:
                        s_, d_ = sm, dm
                    else:
                        bs = stuecke[int(zufall(seed, "hb", sd, hk, i, v) * len(stuecke)) % len(stuecke)]
                        ang = zw(0, 2 * math.pi, seed, "ha", sd, hk, i, v)
                        dist = zw(*H["kontakt_abstand_faktor"], seed, "hk", sd, hk, i, v) * (bs["g"] + g) / 2.0
                        s_, d_ = bs["s"] + dist * math.cos(ang), bs["d"] + dist * math.sin(ang) * 0.8
                    if not (-0.2 <= d_ <= 3.0 and a_ - 0.3 <= s_ <= b_ + 0.3):
                        continue
                    if d_ < 0.4 and G.nahe_lippe(s_, G.u_von(s_, sg, d_), 0.4):
                        continue
                    ausser = {(x["s"], x["d"]) for x in stuecke}
                    if P.frei(sd, s_, d_, 0.45 * g, 0.45, ausser):
                        e = P.setze("stein", NR[fam], g, (seed, "hn2", sd, hk, i), sd, s_, d_,
                                    einb=zw(*T["eingraben"]["K3"], seed, "he", sd, hk, i),
                                    yaw=dip_yaw + zw(-T["haufen"]["kipp_stein_streuung_grad"], T["haufen"]["kipp_stein_streuung_grad"], seed, "hy", sd, hk, i),
                                    kipp=dip + zw(-8, 8, seed, "hkk", sd, hk, i), haufen=hk, deckel="reserve")
                        if e:
                            stuecke.append(e)
                        break
            # mindestens 5 Stueck je Haufen (Referenz 5-15): kleine Steine 0,3-0,4 m nachsetzen, auch ueber die K3-Reserve
            for i in range(30):
                if len(stuecke) >= H["stuecke"][0]:
                    break
                bs = stuecke[i % len(stuecke)] if stuecke else None
                g = zw(0.3, 0.4, seed, "hmg", sd, hk, i)
                if bs is None:
                    s_, d_ = sm + zw(-0.4, 0.4, seed, "hms", sd, hk, i), dm
                else:
                    ang = zw(0, 2 * math.pi, seed, "hma", sd, hk, i)
                    dist = 0.6 * (bs["g"] + g) / 2.0
                    s_, d_ = bs["s"] + dist * math.cos(ang), bs["d"] + dist * math.sin(ang) * 0.8
                if not (-0.2 <= d_ <= 3.0) or not P.frei(sd, s_, d_, 0.45 * g, 0.4, {(x["s"], x["d"]) for x in stuecke}):
                    continue
                e = P.setze("stein", NR["K3_kantig"] + NR["K3_plattig"], g, (seed, "hmn", sd, hk, i), sd, s_, d_,
                            einb=zw(*T["eingraben"]["K3"], seed, "hme", sd, hk, i), yaw=dip_yaw, kipp=dip, haufen=hk)
                if e:
                    stuecke.append(e)
            # zweite Lage (verkeilt), Haufen gesamt hoechstens 15 Stueck
            anteil2 = H["zweite_lage_anteil"]["prall" if prall else "gleit"]
            for i, bs in enumerate(list(stuecke)):
                if len(stuecke) >= H["stuecke"][1]:
                    break
                if zufall(seed, "l2", sd, hk, i) >= anteil2 or bs["g"] < 0.45:
                    continue
                g = bs["g"] * zw(0.5, 0.75, seed, "l2g", sd, hk, i)
                off = zw(*H["zweite_lage_versatz"], seed, "l2o", sd, hk, i) * bs["g"]
                s_, d_ = bs["s"] + zw(-0.5, 0.5, seed, "l2s", sd, hk, i) * off, bs["d"] + off
                e = P.setze("stein", NR["K3_plattig"] + NR["K3_kantig"], g, (seed, "l2n", sd, hk, i), sd, s_, d_,
                            einb=0.0, yaw=dip_yaw + zw(-15, 15, seed, "l2y", sd, hk, i), kipp=dip + zw(-6, 6, seed, "l2k", sd, hk, i),
                            haufen=hk, lage=2, belegen=False, skala=(0.25, 1.8), deckel="reserve")
                if e:
                    zrel = (bs["top"] - H["zweite_lage_verkeilt"] * e["h"]) - e["zt"]
                    e["z_rel"] = zrel
                    e["z"] = e["zt"] + zrel
                    e["top"] = e["z"] + e["h"]
                    e["einb"] = max(0.0, (e["zt"] - e["z"]) / max(e["h"], 1e-6))
                    stuecke.append(e)
            # Kleinschutt in den Fugen
            # je Stein nur die Fuge zum naechsten Nachbarn (sonst wird der Haufen unter Schutt begraben)
            m = 0
            paare = set()
            for i, A in enumerate(stuecke):
                nb = [(math.hypot(A["s"] - B["s"], A["d"] - B["d"]), j) for j, B in enumerate(stuecke) if j != i]
                if nb:
                    paare.add(tuple(sorted((i, min(nb)[1]))))
            for i, j in sorted(paare):
                if True:
                    A, B = stuecke[i], stuecke[j]
                    dd = math.hypot(A["s"] - B["s"], A["d"] - B["d"])
                    if dd <= 0.6 * (A["g"] + B["g"]):
                        for q in range(int(zw(T["schutt"]["fugen_je_kontakt"][0], T["schutt"]["fugen_je_kontakt"][1] + 0.99, seed, "fq", sd, hk, i, j))):
                            t = zw(0.35, 0.65, seed, "ft", sd, hk, i, j, q)
                            s_ = A["s"] + (B["s"] - A["s"]) * t + zw(-0.15, 0.15, seed, "fs", sd, hk, i, j, q)
                            d_ = A["d"] + (B["d"] - A["d"]) * t + zw(-0.15, 0.15, seed, "fd", sd, hk, i, j, q)
                            P.setze("schutt", NR["K2_schutt"], zw(0.12, 0.28, seed, "fg", sd, hk, i, j, q), (seed, "fn", sd, hk, i, j, q),
                                    sd, s_, d_, einb=zw(*T["eingraben"]["K2"], seed, "fe", sd, hk, i, j, q),
                                    yaw=zw(-180, 180, seed, "fy", sd, hk, i, j, q), kipp=zw(0, 25, seed, "fk", sd, hk, i, j, q),
                                    haufen=hk, belegen=False, prio=0)
                            m += 1
            hk += 1
        # ---- 3. Abschnittsquoten: Fuss im Wasser, Bloecke mit Begleitern, Hanggruppe, Kantenplatten, Schutt-/Kies-Auffuellung
        for ai, (a_, b_) in enumerate(abschnitte):
            Lf = (b_ - a_) / 10.0
            q = T["je_10m"]
            nfw = int(round(zw(q["fuss_im_wasser"][0], q["fuss_im_wasser"][1] + 0.99, seed, "fw", sd, ai) * Lf))
            for i in range(max(nfw, 1 if Lf > 0.5 else 0)):
                for v in range(12):
                    s_ = zw(a_ + 0.3, b_ - 0.3, seed, "fws", sd, ai, i, v)
                    d_ = zw(*T["kante"]["fuss_im_wasser_d_m"], seed, "fwd", sd, ai, i, v)
                    g = zw(*T["kante"]["fuss_groesse_m"], seed, "fwg", sd, ai, i, v)
                    u_ = G.u_von(s_, sg, d_)
                    if G.nahe_lippe(s_, u_, 0.9) or not P.frei(sd, s_, d_, 0.45 * g, 0.5):
                        continue
                    W = G.spiegel(s_, sg)
                    rolle = "block" if g >= 1.0 else "fussstein"
                    liste = NR["K4_block"] if g >= 1.0 else NR["K3_kantig"]
                    n_, sk = N.waehle(liste, g, (seed, "fwn", sd, ai, i, v))
                    if n_ is None:
                        continue
                    h = N.gr(n_)[2] * sk
                    top = W + zw(*T["kante"]["fuss_oberkante_ueber_spiegel_m"], seed, "fwo", sd, ai, i, v)
                    e = P.setze(rolle, [n_], g, (seed, "fwx", sd, ai, i, v), sd, s_, d_, z_abs=top - h,
                                yaw=zw(-30, 30, seed, "fwy", sd, ai, i, v), kipp=zw(5, 15, seed, "fwk", sd, ai, i, v),
                                skala_fest=sk, haufen=-3)
                    if e:
                        e["einb"] = max(0.0, (e["zt"] - e["z"]) / max(e["h"], 1e-6))
                        begleiter(P, e, sd, seed, ("fwb", ai, i))
                    break
            # Blockstapel 1,5-5 m (Komposition wie die Demo-Karten: grosse Bloecke gestapelt statt mehr Kleinzeug)
            stapel(P, sd, sg, a_, b_, seed, ai)
            # Bloecke im Uferband (mit Begleitern), Quote minus Fuss-Bloecke
            nb_ziel = int(round(zw(q["K4_block"][0], q["K4_block"][1] + 0.99, seed, "nb", sd, ai) * Lf))
            nb_ist = sum(1 for e in P.inst if e["seite"] == sd and e["rolle"] == "block" and a_ <= e["s"] < b_)
            for i in range(max(0, nb_ziel - nb_ist)):
                for v in range(12):
                    s_ = zw(a_ + 0.5, b_ - 0.5, seed, "bs", sd, ai, i, v)
                    d_ = zw(1.0, 3.0, seed, "bd", sd, ai, i, v)
                    g = zw(1.0, 1.8, seed, "bg", sd, ai, i, v)
                    if not P.frei(sd, s_, d_, 0.45 * g, 0.5):
                        continue
                    e = P.setze("block", NR["K4_block"], g, (seed, "bn", sd, ai, i, v), sd, s_, d_,
                                einb=zw(*T["eingraben"]["K4"], seed, "be", sd, ai, i, v), yaw=zw(-180, 180, seed, "by", sd, ai, i, v),
                                kipp=zw(5, 20, seed, "bk", sd, ai, i, v), haufen=-4)
                    if e:
                        begleiter(P, e, sd, seed, ("bb", ai, i))
                    break
            # Hanggruppe 3-10 m (>= 5 Steine) - je 10 m eine
            for v in range(10):
                s_ = zw(a_ + 1.0, b_ - 1.0, seed, "gs", sd, ai, v) if b_ - a_ > 2.0 else (a_ + b_) / 2.0
                d_ = zw(3.5, 8.5, seed, "gd", sd, ai, v)
                if P.frei(sd, s_, d_, 0.8, 0.5):
                    ng = int(round(zw(T["aufteilung_K3"]["gruppe_hang"][0], T["aufteilung_K3"]["gruppe_hang"][1] + 0.99, seed, "gn", sd, ai) * min(Lf, 1.0)))
                    gruppe = []
                    for i in range(ng):
                        for w in range(8):
                            if not gruppe:
                                s2, d2 = s_, d_
                            else:
                                bs = gruppe[int(zufall(seed, "gb", sd, ai, i, w) * len(gruppe)) % len(gruppe)]
                                ang = zw(0, 2 * math.pi, seed, "ga", sd, ai, i, w)
                                gg = zw(0.35, 0.8, seed, "gg0", sd, ai, i)
                                dist = 0.6 * (bs["g"] + gg) / 2.0
                                s2, d2 = bs["s"] + dist * math.cos(ang), bs["d"] + dist * math.sin(ang)
                            gg = zw(0.35, 0.8, seed, "gg0", sd, ai, i)
                            if 3.0 <= d2 <= 9.8 and P.frei(sd, s2, d2, 0.45 * gg, 0.45, {(x["s"], x["d"]) for x in gruppe}):
                                e = P.setze("stein", NR["K3_kantig"] + NR["K3_plattig"], gg, (seed, "gnn", sd, ai, i), sd, s2, d2,
                                            einb=zw(*T["eingraben"]["K3"], seed, "ge", sd, ai, i), yaw=zw(-60, 60, seed, "gy", sd, ai, i),
                                            kipp=zw(5, 20, seed, "gk", sd, ai, i), haufen=1000 + ai, deckel="voll")
                                if e:
                                    gruppe.append(e)
                                break
                    for i in range(int(len(gruppe) * 1.5)):
                        bs = gruppe[i % len(gruppe)]
                        P.setze("schutt", NR["K2_schutt"], zw(0.12, 0.28, seed, "gsch", sd, ai, i), (seed, "gscn", sd, ai, i), sd,
                                bs["s"] + zw(-0.6, 0.6, seed, "gss", sd, ai, i), bs["d"] + zw(-0.6, 0.6, seed, "gsd", sd, ai, i),
                                einb=zw(*T["eingraben"]["K2"], seed, "gse", sd, ai, i), yaw=zw(-180, 180, seed, "gsy", sd, ai, i),
                                haufen=1000 + ai, belegen=False, prio=2)
                    break
            # Kanten-Platten bis zur Bedeckung, dann Schutt/Kies bis zur Quote
            fuellen(P, sd, sg, a_, b_, seed, ai)
        # ---- 4. Fels > 3 m (Prallhang), Wandverkleidung + Schuttband
        wand_und_fels(P, sd, sg, s_a, s_b, seed)
        # ---- 5. Bewuchs nach den Steinen
        bewuchs(P, sd, sg, s_a, s_b, abschnitte, rh, grasluecken, seed)
        for ai, (a_, b_) in enumerate(abschnitte):
            k2_quote(P, sd, a_, b_, seed, ai)
    swr_filter(P)
    return P, abschnitte, X


def stapel(P, sd, sg, a_, b_, seed, ai):
    """1 Stapel aus 2-4 grossen Bloecken je 10 m am Prallhang (Gleitufer 0,5): Basisblock 2,5-4,5 m, Nachbarn 1,5-3 m
    ueberlappend (Abstand 0,35-0,55 x mittlere Groesse), am Prallhang 1 Block in 2. Lage verkeilt; Mitte 1,5-6 m ab der Kante."""
    T, G = P.T, P.G
    St = T["stapel"]
    prall = G.prallseite((a_ + b_) / 2.0) == sd
    rate = St["je_10m"]["prall" if prall else "gleit"] * (b_ - a_) / 10.0
    anzahl = int(math.floor(rate)) + (1 if zufall(seed, "stw", sd, ai) < rate - math.floor(rate) else 0)
    for k in range(anzahl):
        stapel_eins(P, sd, sg, a_, b_, seed, (ai, k), prall)


def stapel_eins(P, sd, sg, a_, b_, seed, ai, prall):
    T, NR = P.T, P.R["netze_rollen"]
    St = T["stapel"]
    for v in range(12):
        s0 = zw(a_ + 1.5, b_ - 1.5, seed, "sts", sd, ai, v) if b_ - a_ > 3.5 else (a_ + b_) / 2.0
        d0 = zw(*St["mitte_d_m"], seed, "std", sd, ai, v)
        g0 = zw(*St["basis_m"], seed, "stg", sd, ai, v)
        if not P.frei(sd, s0, d0, 0.45 * g0, 0.45):
            continue
        basis = P.setze("stapel", NR["stapel_block"], g0, (seed, "stn", sd, ai), sd, s0, d0,
                        einb=zw(*St["eingraben"], seed, "ste", sd, ai), yaw=sg * 90.0 + zw(-35, 35, seed, "sty", sd, ai),
                        kipp=zw(5, 15, seed, "stk", sd, ai), haufen=2000 + 10 * ai[0] + ai[1])
        if not basis:
            return
        teile = [basis]
        n = int(zw(St["bloecke"][0], St["bloecke"][1] + 0.99, seed, "stn2", sd, ai))
        for i in range(1, n):
            for w in range(10):
                bs = teile[int(zufall(seed, "stb", sd, ai, i, w) * len(teile)) % len(teile)]
                g = zw(*St["nachbar_m"], seed, "stng", sd, ai, i, w)
                ang = zw(0, 2 * math.pi, seed, "sta", sd, ai, i, w)
                dist = zw(*St["abstand_faktor"], seed, "stdf", sd, ai, i, w) * (bs["g"] + g) / 2.0
                s_, d_ = bs["s"] + dist * math.cos(ang), bs["d"] + dist * math.sin(ang)
                if not (1.0 <= d_ <= 10.0 - 0.6 * g):
                    continue
                if P.frei(sd, s_, d_, 0.45 * g, 0.45, {(x["s"], x["d"]) for x in teile}):
                    e = P.setze("stapel", NR["stapel_block"], g, (seed, "stx", sd, ai, i), sd, s_, d_,
                                einb=zw(*St["eingraben"], seed, "ste2", sd, ai, i),
                                yaw=basis["yaw"] + zw(-25, 25, seed, "sty2", sd, ai, i), kipp=zw(5, 20, seed, "stk2", sd, ai, i),
                                haufen=2000 + 10 * ai[0] + ai[1])
                    if e:
                        teile.append(e)
                    break
        if prall and len(teile) >= 2:
            bs = max(teile, key=lambda x: x["g"])
            g = zw(*St["oben_m"], seed, "sto", sd, ai)
            e = P.setze("stapel", NR["stapel_block"], g, (seed, "stox", sd, ai), sd, bs["s"] + zw(-0.4, 0.4, seed, "stos", sd, ai),
                        bs["d"] + zw(0.2, 0.5, seed, "stod", sd, ai) * bs["g"], yaw=bs["yaw"] + zw(-20, 20, seed, "stoy", sd, ai),
                        kipp=zw(8, 20, seed, "stok", sd, ai), haufen=2000 + 10 * ai[0] + ai[1], lage=2, belegen=False)
            if e:
                zrel = (bs["top"] - St["oben_verkeilt"] * e["h"]) - e["zt"]
                e["z_rel"], e["z"] = zrel, e["zt"] + zrel
                e["top"] = e["z"] + e["h"]
                e["einb"] = max(0.0, (e["zt"] - e["z"]) / max(e["h"], 1e-6))
        begleiter(P, basis, sd, seed, ("st", ai))
        return


def clamp_i(x, a, b):
    return max(a, min(b, x))


def begleiter(P, blk, sd, seed, key):
    T, NR = P.T, P.R["netze_rollen"]
    B = T["begleiter"]
    ns = int(zw(B["steine_umkreis_2m"][0], B["steine_umkreis_2m"][1] + 0.99, seed, "bgn", sd, *key))
    da = sum(1 for e in P.inst if e is not blk and e["seite"] == sd and e["rolle"] in STEINROLLEN and
             math.hypot(e["s"] - blk["s"], e["d"] - blk["d"]) <= 0.45 * blk["g"] + 2.0)
    for i in range(max(0, ns - da)):
        for v in range(8):
            ang = zw(0, 2 * math.pi, seed, "bga", sd, *key, i, v)
            g = zw(0.3, 0.7, seed, "bgg", sd, *key, i, v)
            dist = 0.55 * (blk["g"] + g) / 2.0 + zw(0.0, 0.6, seed, "bgd", sd, *key, i, v)
            s_, d_ = blk["s"] + dist * math.cos(ang), blk["d"] + dist * math.sin(ang)
            if d_ < -0.4 or d_ > 9.8:
                continue
            if P.frei(sd, s_, d_, 0.45 * g, 0.45, {(blk["s"], blk["d"])}):
                P.setze("stein", NR["K3_kantig"] + NR["K3_plattig"], g, (seed, "bgx", sd, *key, i), sd, s_, d_,
                        einb=zw(*T["eingraben"]["K3"], seed, "bge", sd, *key, i), yaw=zw(-180, 180, seed, "bgy", sd, *key, i),
                        kipp=zw(5, 20, seed, "bgk", sd, *key, i), haufen=-5, deckel="reserve")
                break
    nk = int(zw(B["schutt_umkreis_1m"][0], B["schutt_umkreis_1m"][1] + 0.99, seed, "bkn", sd, *key))
    dk = sum(1 for e in P.inst if e["seite"] == sd and e["rolle"] == "schutt" and
             math.hypot(e["s"] - blk["s"], e["d"] - blk["d"]) <= 0.45 * blk["g"] + 1.0)
    for i in range(max(0, nk - dk)):
        ang = zw(0, 2 * math.pi, seed, "bka", sd, *key, i)
        dist = 0.45 * blk["g"] + zw(0.05, 0.9, seed, "bkd", sd, *key, i)
        d_ = blk["d"] + dist * math.sin(ang)
        if d_ < -0.3:
            continue
        P.setze("schutt", NR["K2_schutt"], zw(0.12, 0.28, seed, "bkg", sd, *key, i), (seed, "bkx", sd, *key, i), sd,
                blk["s"] + dist * math.cos(ang), d_, einb=zw(*T["eingraben"]["K2"], seed, "bke", sd, *key, i),
                yaw=zw(-180, 180, seed, "bky", sd, *key, i), haufen=-5, belegen=False, prio=1)


def bedeckung(P, sd, a, b, d0, d1, raster=0.1):
    """Anteil der Flaeche (s in [a, b], d in [d0, d1]) unter Stein-Fussabdruecken (Kreise; Platten als Ellipse)."""
    ss = np.arange(a + raster / 2, b, raster)
    dd = np.arange(d0 + raster / 2, d1, raster)
    S, D = np.meshgrid(ss, dd, indexing="ij")
    M = np.zeros(S.shape, dtype=bool)
    for e in P.inst:
        if e["seite"] != sd or e["rolle"] not in ("kies", "schutt", "stein", "fussstein", "block", "platte", "haufen_kern",
                                                   "wand", "fels", "stapel"):
            continue
        if e["s"] < a - 4 or e["s"] > b + 4:
            continue
        gx, gy, gz = P.N.gr(e["netz"])
        if e["rolle"] in ("platte", "wand", "fels"):
            ra, rb = 0.5 * gx * e["skala"] * 0.85, 0.5 * gy * e["skala"] * 0.85
        else:
            sicht = max(0.15, 1.0 - e["einb"]) ** 0.3
            ra = rb = 0.5 * math.sqrt(gx * gy) * e["skala"] * 0.9 * sicht
        w = math.radians(e["yaw"])
        ds, dn = S - e["s"], D - e["d"]
        x = ds * math.cos(w) + dn * math.sin(w)
        y = -ds * math.sin(w) + dn * math.cos(w)
        M |= (x / max(ra, 0.02)) ** 2 + (y / max(rb, 0.02)) ** 2 <= 1.0
    return float(M.mean()) if M.size else 0.0


def bedeckung_ziel(P, sd, a_, b_, band):
    T = P.T
    z = T["bedeckung_stein_min"][band]
    if band in ("kante", "ufer") and P.G.prallseite((a_ + b_) / 2.0) == sd:
        z += T["bedeckung_prall_zuschlag"]
    return z


def fuellen(P, sd, sg, a_, b_, seed, ai):
    """Kanten-Platten bis zur Bedeckung im Kantenband; danach Schutt und Kies bis zur Quote je Abschnitt."""
    T, NR, G = P.T, P.R["netze_rollen"], P.G
    Lf = (b_ - a_) / 10.0
    Pl = T["platten"]
    for band, (d0, d1) in (("kante", (0.0, 1.0)), ("ufer", (1.0, 3.0)), ("hang", (3.0, 10.0))):
        liste, groesse = Pl[band]["netze"], Pl[band]["groesse_m"]
        ziel = bedeckung_ziel(P, sd, a_, b_, band) + 0.02
        for it in range(60):
            if bedeckung(P, sd, a_, b_, d0, d1, 0.1 if band != "hang" else 0.2) >= ziel:
                break
            best, bw = None, 2.0
            for v in range(6):
                s_ = zw(a_ + 0.2, b_ - 0.2, seed, "fp", band, sd, ai, it, v)
                d_ = zw(d0 + 0.1, d1 - 0.1, seed, "fpd", band, sd, ai, it, v)
                u_ = G.u_von(s_, sg, d_)
                if band == "kante" and G.nahe_lippe(s_, u_, 0.4):
                    continue
                c = bedeckung(P, sd, s_ - 0.5, s_ + 0.5, max(d0, d_ - 0.5), min(d1, d_ + 0.5), 0.1)
                if c < bw:
                    best, bw = (s_, d_), c
            if best is None:
                continue
            key = (seed, "fpn", band, sd, ai, it)
            n_ = liste[int(zufall(*key) * len(liste)) % len(liste)]
            sk = zw(*groesse, seed, "fps", band, sd, ai, it) / max(P.N.gr(n_)[:2])
            P.setze("platte", [n_], 0.0, key, sd, best[0], best[1],
                    einb=zw(*T["eingraben"]["platte"], seed, "fpe", band, sd, ai, it), skala_fest=round(sk, 3),
                    belegen=False, haufen=-6)
    # Quoten K3, K2, K1
    q = T["je_10m"]
    def zaehle(rollen, kl=None):
        n = 0
        for e in P.inst:
            if e["seite"] == sd and a_ <= e["s"] < b_ and e["rolle"] in rollen and -0.6 <= e["d"] <= 3.0 and e["haufen"] != -11:
                if kl is None or kl[0] <= e["g"] < kl[1]:
                    n += 1
        return n
    k3_min = int(math.ceil(q["K3_stein"][0] * Lf))
    i = 0
    while zaehle(("stein", "fussstein", "block"), (0.3, 1.0)) < k3_min and i < 80:
        s_ = zw(a_ + 0.2, b_ - 0.2, seed, "k3s", sd, ai, i)
        d_ = zw(0.2, 3.0, seed, "k3d", sd, ai, i)
        g = zw(0.32, 0.7, seed, "k3g", sd, ai, i)
        if P.frei(sd, s_, d_, 0.45 * g, 0.5) and not G.nahe_lippe(s_, G.u_von(s_, sg, d_), 0.35):
            P.setze("stein", NR["K3_kantig"] + NR["K3_plattig"], g, (seed, "k3n", sd, ai, i), sd, s_, d_,
                    einb=zw(*T["eingraben"]["K3"], seed, "k3e", sd, ai, i), yaw=zw(-180, 180, seed, "k3y", sd, ai, i),
                    kipp=zw(5, 20, seed, "k3k", sd, ai, i), haufen=-7)
        i += 1
    k1_ziel = int(round(zw(q["K1_kies"][0], q["K1_kies"][1], seed, "k1z", sd, ai) * Lf))
    for i in range(k1_ziel):
        s_ = zw(a_ + 0.1, b_ - 0.1, seed, "k1s", sd, ai, i)
        d_ = zw(-0.2, 2.0, seed, "k1d", sd, ai, i)
        P.setze("kies", NR["K1_kies"], zw(0.05, 0.1, seed, "k1g", sd, ai, i), (seed, "k1n", sd, ai, i), sd, s_, d_,
                einb=zw(0.3, 0.5, seed, "k1e", sd, ai, i), yaw=zw(-180, 180, seed, "k1y", sd, ai, i), haufen=-9, belegen=False,
                skala=(0.5, 2.5))


def k2_quote(P, sd, a_, b_, seed, ai):
    """Kleinschutt je 10 m und Seite (Band 0-3 m, ohne Schuttband) erst ausduennen, dann auffuellen - nach allen anderen Schritten."""
    T, NR = P.T, P.R["netze_rollen"]
    Lf = (b_ - a_) / 10.0
    q = T["je_10m"]

    def zaehle(rollen):
        return sum(1 for e in P.inst if e["seite"] == sd and a_ <= e["s"] < b_ and e["rolle"] in rollen and -0.6 <= e["d"] <= 3.0
                   and e["haufen"] != -11)
    k2_ziel = int(round(zw(q["K2_schutt"][0], q["K2_schutt"][1], seed, "k2z", sd, ai) * Lf))
    # Potenzgesetz (ent zu §8.7): K2 >= 2 x K3, hoechstens bis zur Referenz-Obergrenze K2_max_referenz
    n3 = sum(1 for e in P.inst if e["seite"] == sd and a_ <= e["s"] < b_ and e["rolle"] in ("stein", "fussstein", "block") and
             0.3 <= e["g"] < 1.0 and -0.6 <= e["d"] <= 3.0)
    k2_ziel = min(max(k2_ziel, int(math.ceil(T["verhaeltnis"]["K2_zu_K3"][0] * n3))), int(round(q["K2_max_referenz"] * Lf)))
    # ausduennen: Fugen > Begleiter > Saum/Gruppe > Fuellung (Prioritaet, dann Zufall)
    kand = [e for e in P.inst if e["seite"] == sd and a_ <= e["s"] < b_ and e["rolle"] == "schutt" and -0.6 <= e["d"] <= 3.0
            and e["haufen"] != -11]
    if len(kand) > k2_ziel:
        kand.sort(key=lambda e: (e["prio"], zufall(seed, "k2w", sd, r2(e["s"], 3), r2(e["d"], 3))))
        weg = {id(e) for e in kand[k2_ziel:]}
        P.inst = [e for e in P.inst if id(e) not in weg]
    i = 0
    while zaehle(("schutt",)) < k2_ziel and i < 400:
        s_ = zw(a_ + 0.1, b_ - 0.1, seed, "k2s", sd, ai, i)
        d_ = zw(0.0, 3.0, seed, "k2d", sd, ai, i)
        # Schutt sammelt sich an Steinen: naechster Stein <= 0,8 m
        near = [e for e in P.inst if e["seite"] == sd and e["rolle"] in STEINROLLEN and abs(e["s"] - s_) < 1.0 and
                abs(e["d"] - d_) < 1.0]
        if near:
            P.setze("schutt", NR["K2_schutt"], zw(0.12, 0.28, seed, "k2g", sd, ai, i), (seed, "k2n", sd, ai, i), sd, s_, d_,
                    einb=zw(*T["eingraben"]["K2"], seed, "k2e", sd, ai, i), yaw=zw(-180, 180, seed, "k2y", sd, ai, i),
                    kipp=zw(0, 25, seed, "k2k", sd, ai, i), haufen=-8, belegen=False, prio=3)
        i += 1


def wand_und_fels(P, sd, sg, s_a, s_b, seed):
    T, NR, G = P.T, P.R["netze_rollen"], P.G
    Wd = T["wand"]
    s, k = s_a + 0.5, 0
    while s < s_b - 0.5:
        W = G.spiegel(s, sg)
        hw = max(G.z(s, G.u_von(s, sg, d)) - W for d in (1.0, 2.0, 3.0, 4.0))
        ng = sum(G.neigung(s, sg, d) for d in (1.0, 1.5, 2.0, 2.5)) / 4.0
        if hw >= Wd["ab_hoehe_m"] and ng >= Wd["ab_neigung_grad"]:
            liste = NR["wand"][:2] if hw <= 1.8 else [NR["wand"][2]]
            n = liste[int(zufall(seed, "wn", sd, k) * len(liste)) % len(liste)]
            gx, gy, gz = P.N.gr(n)
            sk = clamp_i(hw / math.sin(math.radians(max(ng, 20.0))) / gx, 0.35, 1.2)
            dmid = 0.5 * (1.0 + 3.0)
            e = P.setze("wand", [n], 0.0, (seed, "wx", sd, k), sd, s, dmid, einb=zw(*Wd["eingraben"], seed, "we", sd, k),
                        yaw=sg * 90.0 + zw(-8, 8, seed, "wy", sd, k), kipp=ng, skala_fest=round(sk, 3), haufen=-10)
            if e:
                # Schuttband am Fuss (zwei Lagen nur hier)
                if hw >= T["schutt"]["schuttband_ab_wandhoehe_m"]:
                    breite = zw(*T["schutt"]["schuttband_breite_m"], seed, "sbb", sd, k)
                    laenge = gy * sk * Wd["modul_abstand_faktor"]
                    nsb = int(zw(*T["schutt"]["schuttband_je_m2"], seed, "sbn", sd, k) * breite * laenge)
                    for i in range(nsb):
                        P.setze("schutt", NR["K2_schutt"], zw(0.1, 0.3, seed, "sbg", sd, k, i), (seed, "sbx", sd, k, i), sd,
                                s + zw(-laenge / 2, laenge / 2, seed, "sbs", sd, k, i), zw(0.3, 0.3 + breite, seed, "sbd", sd, k, i),
                                einb=zw(0.2, 0.5, seed, "sbe", sd, k, i), yaw=zw(-180, 180, seed, "sby", sd, k, i),
                                kipp=zw(0, 30, seed, "sbk", sd, k, i), haufen=-11, belegen=False,
                                lage=1 + int(zufall(seed, "sbl", sd, k, i) < 0.35))
                s += gy * sk * Wd["modul_abstand_faktor"]
                k += 1
                continue
        s += 1.0
        k += 1
    # Fels > 3 m am Prallhang: 1-2 je 50 m
    s = s_a + zw(5, 15, seed, "fl0", sd)
    k = 0
    while s < s_b - 2:
        if G.prallseite(s) == sd:
            for v in range(8):
                d_ = zw(2.5, 6.0, seed, "fld", sd, k, v)
                s_ = s + zw(-3, 3, seed, "fls", sd, k, v)
                if P.frei(sd, s_, d_, 2.0, 0.4) and G.neigung(s_, sg, d_) >= 15:
                    n = NR["K5_fels"][int(zufall(seed, "fln", sd, k) * 2) % 2]
                    sk = zw(0.6, 0.85, seed, "flk", sd, k)
                    P.setze("fels", [n], 0.0, (seed, "flx", sd, k), sd, s_, d_, einb=zw(0.45, 0.6, seed, "fle", sd, k),
                            yaw=sg * 90.0 + zw(-25, 25, seed, "fly", sd, k), kipp=G.neigung(s_, sg, d_), skala_fest=round(sk, 3),
                            haufen=-12)
                    begleiter(P, P.inst[-1], sd, seed, ("fl", k))
                    break
            s += zw(25, 45, seed, "flab", sd, k)
        else:
            s += 5.0
        k += 1


def bewuchs(P, sd, sg, s_a, s_b, abschnitte, rh, grasluecken, seed):
    T, NR, G = P.T, P.R["netze_rollen"], P.G
    Pf = T["pflanzen"]
    steine = [e for e in P.inst if e["seite"] == sd and e["rolle"] in STEINROLLEN and e["g"] >= 0.3]
    for ai, (a_, b_) in enumerate(abschnitte):
        Lf = (b_ - a_) / 10.0
        q = T["je_10m"]
        # Gras in Ritzen: Kontaktpunkte zweier Steine im Band 1-3 m
        kont = []
        loc = [e for e in steine if a_ <= e["s"] < b_ and 0.8 <= e["d"] <= 3.2]
        for i in range(len(loc)):
            for j in range(i + 1, len(loc)):
                A, B = loc[i], loc[j]
                if math.hypot(A["s"] - B["s"], A["d"] - B["d"]) <= 0.65 * (A["g"] + B["g"]):
                    kont.append((A, B))
        ngr = int(round(zw(q["gras_ritze"][0], q["gras_ritze"][1] + 0.99, seed, "grn", sd, ai) * Lf))
        for i in range(min(ngr, len(kont))):
            for v in range(8):
                A, B = kont[int(zufall(seed, "grk", sd, ai, i, v) * len(kont)) % len(kont)]
                t = zw(0.4, 0.6, seed, "grt", sd, ai, i)
                s_ = A["s"] + (B["s"] - A["s"]) * t
                d_ = A["d"] + (B["d"] - A["d"]) * t + 0.15
                if trocken_ok(G, s_, sg, d_):
                    break
            else:
                continue
            trocken = zufall(seed, "grtr", sd, ai, i) < zw(*Pf["trocken_anteil"], seed, "grta", sd)
            n_ = NR["gras_ritze"][int(zufall(seed, "grnn", sd, ai, i) * len(NR["gras_ritze"])) % len(NR["gras_ritze"])]
            gz = P.N.gr(n_)[2]
            sk = min(zw(0.7, 1.1, seed, "grs", sd, ai, i), Pf["gras_hoehe_max_band_0_3_m"] * 0.95 / gz)
            e = P.setze("gras_ritze", [n_], 0.0, (seed, "grx", sd, ai, i), sd, s_, d_, einb=0.03 / max(gz * sk, 0.05),
                        yaw=zw(-180, 180, seed, "gry", sd, ai, i), skala_fest=round(sk, 3), belegen=False)
            if e and trocken:
                e["trocken"] = True
        # Farne in Luecken: Gleitufer 2-3 je 10 m; Nordufer-Zusatz (Weltwerkzeug filtert Rolle 'farn')
        gleit = G.prallseite((a_ + b_) / 2.0) != sd
        nf = int(round(zw(q["farn_gleitufer"][0], q["farn_gleitufer"][1] + 0.99, seed, "fnn", sd, ai) * Lf)) if gleit else 0
        luecken = [(x0, x1) for (x0, x1, art, pr) in rh if art == "luecke" and x1 > a_ and x0 < b_]
        for i in range(nf):
            for v in range(10):
                if luecken:
                    x0, x1 = luecken[int(zufall(seed, "fl", sd, ai, i, v) * len(luecken)) % len(luecken)]
                    s_ = zw(max(x0, a_), min(x1, b_), seed, "fs", sd, ai, i, v)
                else:
                    s_ = zw(a_, b_, seed, "fs", sd, ai, i, v)
                d_ = zw(*Pf["farn_d_m"], seed, "fd", sd, ai, i, v)
                nah = [e for e in steine if abs(e["s"] - s_) < 1.5 and abs(e["d"] - d_) < 1.5 and e["g"] >= 0.5]
                if not nah:
                    continue
                st = min(nah, key=lambda e: math.hypot(e["s"] - s_, e["d"] - d_))
                dist = math.hypot(st["s"] - s_, st["d"] - d_)
                rand = 0.45 * st["g"] + 0.2
                if dist > 1e-6:
                    s_ = st["s"] + (s_ - st["s"]) * rand / dist
                    d_ = st["d"] + (d_ - st["d"]) * rand / dist
                if P.frei(sd, s_, d_, 0.25, 0.4) and trocken_ok(G, s_, sg, d_):
                    P.setze("farn_ritze", NR["farn"], 0.0, (seed, "fnx", sd, ai, i), sd, s_, d_, einb=0.03,
                            yaw=zw(-180, 180, seed, "fy", sd, ai, i), skala_fest=round(zw(0.7, 1.0, seed, "fk", sd, ai, i), 3))
                    break
        if not gleit and zufall(seed, "fnord", sd, ai) < 0.6:
            s_ = zw(a_ + 1, b_ - 1, seed, "fns", sd, ai)
            d_ = zw(1.2, 2.8, seed, "fnd", sd, ai)
            if P.frei(sd, s_, d_, 0.25, 0.4) and trocken_ok(G, s_, sg, d_):
                P.setze("farn", NR["farn"], 0.0, (seed, "fnox", sd, ai), sd, s_, d_, einb=0.03,
                        yaw=zw(-180, 180, seed, "fny", sd, ai), skala_fest=round(zw(0.7, 1.0, seed, "fnk", sd, ai), 3))
        # Moos-Polster erst ab 1 m ueber dem Spiegel
        nm = int(round(zw(*T["moos"]["boden_polster_je_10m"], seed, "mn", sd, ai) * Lf))
        for i in range(nm):
            for v in range(10):
                s_ = zw(a_, b_, seed, "ms", sd, ai, i, v)
                d_ = zw(1.0, 8.0, seed, "md", sd, ai, i, v)
                u_ = G.u_von(s_, sg, d_)
                if G.z(s_, u_) - G.spiegel(s_, sg) >= T["moos"]["ab_ueber_spiegel_m"] + 0.05:
                    P.setze("moos_boden", NR["moos_boden"], 0.0, (seed, "mx", sd, ai, i), sd, s_, d_, einb=0.0,
                            yaw=zw(-180, 180, seed, "my", sd, ai, i), skala_fest=round(zw(0.8, 1.3, seed, "mk", sd, ai, i), 3),
                            belegen=False)
                    break
        # Buesche am Stein (2-6 m)
        nbu = int(round(zw(q["busch"][0], q["busch"][1] + 0.99, seed, "bun", sd, ai) * Lf))
        for i in range(nbu):
            for v in range(10):
                cand = [e for e in steine if a_ <= e["s"] < b_ and 2.0 <= e["d"] <= 6.0]
                if not cand:
                    break
                st = cand[int(zufall(seed, "bus", sd, ai, i, v) * len(cand)) % len(cand)]
                ang = zw(0, 2 * math.pi, seed, "bua", sd, ai, i, v)
                s_ = st["s"] + (0.45 * st["g"] + 0.4) * math.cos(ang)
                d_ = st["d"] + (0.45 * st["g"] + 0.4) * math.sin(ang)
                if P.frei(sd, s_, d_, 0.45, 0.5) and trocken_ok(G, s_, sg, d_):
                    P.setze("busch", NR["busch"], 0.0, (seed, "bux", sd, ai, i), sd, s_, d_, einb=0.05,
                            yaw=zw(-180, 180, seed, "buy", sd, ai, i), skala_fest=round(zw(0.8, 1.1, seed, "buk", sd, ai, i), 3))
                    break
    # Gras-Ueberhang nur in den Grasluecken (Gleitufer), Fuss >= 0,3 m ueber dem Spiegel
    for i, (x0, x1) in enumerate(grasluecken):
        for t in (0.3, 0.7):
            s_ = x0 + (x1 - x0) * t
            W = G.spiegel(s_, sg)
            d_ = None
            for dd in np.arange(0.1, 2.5, 0.1):
                if G.z(s_, G.u_von(s_, sg, float(dd))) >= W + T["kante"]["gras_fuss_ueber_spiegel_min_m"]:
                    d_ = float(dd)
                    break
            if d_ is None:
                continue
            P.setze("gras_kante", ["SM_grass_bush_01", "SM_GrassyEmbankment_01"], 0.0, (seed, "gkx", sd, i, t),
                    sd, s_, d_, z_rel=-0.02, yaw=-sg * 90.0 + zw(-25, 25, seed, "gky", sd, i, t),
                    kipp=zw(20, 35, seed, "gkk", sd, i, t), skala_fest=round(zw(0.7, 0.85, seed, "gks", sd, i, t), 3), belegen=False)
    # Gehoelzgruppen: je 50 m eine (Seiten versetzt), Fuss 2-6 m, Neigung <= 30 Grad, 2-3 Steine am Fuss
    Gh = T["gehoelz"]
    s = s_a + (12.0 if sd == "links" else 37.0)
    k = 0
    while s < s_b - 3:
        for v in range(12):
            s_ = s + zw(-6, 6, seed, "ghs", sd, k, v)
            d_ = zw(*Gh["fuss_d_m"], seed, "ghd", sd, k, v)
            if G.neigung(s_, sg, d_, 1.0) <= Gh["neigung_max_grad"] and P.frei(sd, s_, d_, 1.0, 0.5):
                nb = int(zw(Gh["baeume_je_gruppe"][0], Gh["baeume_je_gruppe"][1] + 0.99, seed, "ghn", sd, k))
                for b in range(nb):
                    sb = s_ + b * zw(1.8, 3.5, seed, "ghb", sd, k, b)
                    db = d_ + zw(-0.8, 0.8, seed, "ghdb", sd, k, b)
                    e = P.setze("gehoelz", NR["gehoelz"], 0.0, (seed, "ghx", sd, k, b), sd, sb, db, einb=0.0,
                                yaw=zw(-180, 180, seed, "ghy", sd, k, b), skala_fest=round(zw(0.75, 1.0, seed, "ghk", sd, k, b), 3))
                    if e:
                        for m in range(int(zw(Gh["steine_am_fuss"][0], Gh["steine_am_fuss"][1] + 0.99, seed, "ghsn", sd, k, b))):
                            ang = zw(0, 2 * math.pi, seed, "ghsa", sd, k, b, m)
                            P.setze("stein", NR["K3_kantig"], zw(0.35, 0.6, seed, "ghsg", sd, k, b, m), (seed, "ghsx", sd, k, b, m), sd,
                                    sb + 0.9 * math.cos(ang), db + 0.9 * math.sin(ang), einb=0.4, yaw=zw(-180, 180, seed, "ghsy", sd, k, b, m),
                                    kipp=10, haufen=-13, belegen=False, deckel="voll")
                break
        s += zw(45, 60, seed, "ghab", sd, k)
        k += 1


def trocken_ok(G, s, sg, d, ueber=0.15):
    """Pflanzen nur auf Gelaende >= 0,15 m ueber dem Spiegel (Kolke/Becken reichen stellenweise ueber die Kantenlinie)."""
    return G.z(s, G.u_von(s, sg, d)) >= G.spiegel(s, sg) + ueber


def swr_filter(P):
    """N5-Filter (hindernisse_filter_p2): Steine >= 0,4 m im Wasser oder <= 1 m daneben, nicht Rolle block/wand/fels/...;
    Teil <= 40 % der Bettbreite; je Meter <= 50 % der Bettbreite."""
    Sw = P.R["swr_hindernis"]
    G = P.G
    je_m = {}
    for x in P.X["liste"]:                                 # Hindernisse des Bettplans zaehlen mit
        if x and x.get("hind"):
            m = int(math.floor(x["s"]))
            je_m[m] = je_m.get(m, 0.0) + x["g"]
    for e in sorted(P.inst, key=lambda x: (x["s"], x["seite"], x["d"])):
        if e["rolle"] in Sw["rollen_nie"] or e["g"] < Sw["min_m"] or e["d"] > Sw["abstand_wasser_m"]:
            continue
        i = G.zeile(e["s"])
        B = float(G.EL[i] - G.ER[i])
        if e["g"] > Sw["anteil_breite_max"] * B:
            continue
        m = int(math.floor(e["s"]))
        if je_m.get(m, 0.0) + e["g"] > Sw["anteil_je_m_max"] * B:
            continue
        je_m[m] = je_m.get(m, 0.0) + e["g"]
        e["hind"] = True


# ======================================================================================================================
def kennzahlen(P, abschnitte):
    T = P.T
    out = []
    for sd in ("links", "rechts"):
        for (a, b) in abschnitte:
            Lf = (b - a) / 10.0
            sel = [e for e in P.inst if e["seite"] == sd and a <= e["s"] < b and -0.6 <= e["d"] <= 10.0]
            band = [e for e in sel if e["d"] <= 3.0 and e["haufen"] != -11]
            hang = [e for e in sel if e["d"] > 3.0]

            def n_kl(lo, hi, rollen=("stein", "fussstein", "block"), m=None):
                return sum(1 for e in (band if m is None else m) if e["rolle"] in rollen and lo <= e["g"] < hi)
            gross = [e for e in sel if e["rolle"] in ("stein", "fussstein", "block") and e["g"] >= 0.3]
            kontakt = 0
            for e in gross:
                for f in sel:
                    if f is e or f["rolle"] not in ("stein", "fussstein", "block", "schutt", "platte"):
                        continue
                    rf = 0.45 * f["g"] if f["rolle"] != "platte" else 0.4 * max(P.N.gr(f["netz"])[:2]) * f["skala"]
                    if math.hypot(e["s"] - f["s"], e["d"] - f["d"]) <= 0.45 * e["g"] + rf + 0.05:
                        kontakt += 1
                        break
            einb_ok = sum(1 for e in gross if e["einb"] >= 1.0 / 3.0 - 1e-6)
            ritze = [e for e in sel if e["rolle"] == "gras_ritze" or (e["rolle"] == "farn_ritze")]
            in_ritze = 0
            for e in ritze:
                if any(math.hypot(e["s"] - f["s"], e["d"] - f["d"]) - 0.45 * f["g"] <= T["pflanzen"]["ritze_abstand_stein_max_m"] + 0.05
                       for f in sel if f["rolle"] in STEINROLLEN and f["g"] >= 0.3):
                    in_ritze += 1
            out.append({"seite": sd, "s": [r2(a, 1), r2(b, 1)], "laenge_m": r2(b - a, 1),
                        "K1_kies": sum(1 for e in band if e["rolle"] == "kies"),
                        "K2_schutt": sum(1 for e in band if e["rolle"] == "schutt"),
                        "K3_stein": n_kl(0.3, 1.0), "K4_block": n_kl(1.0, 9.0),
                        "hang_K3": n_kl(0.3, 1.0, m=hang), "hang_K4": n_kl(1.0, 9.0, m=hang),
                        "schuttband": sum(1 for e in sel if e["haufen"] == -11),
                        "wand_module": sum(1 for e in sel if e["rolle"] == "wand"),
                        "formen_ab_0_5m": sum(1 for e in sel if e["rolle"] in STEINROLLEN + ("fels", "wand") and e["g"] >= 0.5
                                              and e["lage"] == 1),
                        "fuss_im_wasser": sum(1 for e in sel if e["rolle"] in ("fussstein", "block") and e["d"] <= 0.05),
                        "kontakt_anteil": r2(kontakt / max(len(gross), 1)), "eingraben_drittel_anteil": r2(einb_ok / max(len(gross), 1)),
                        "gras_ritze": sum(1 for e in sel if e["rolle"] == "gras_ritze"),
                        "ritze_anteil": r2(in_ritze / max(len(ritze), 1)),
                        "farn": sum(1 for e in sel if e["rolle"] in ("farn_ritze", "farn")),
                        "busch": sum(1 for e in sel if e["rolle"] == "busch"),
                        "bedeckung_kante": r2(bedeckung(P, sd, a, b, 0.0, 1.0)), "bedeckung_ufer": r2(bedeckung(P, sd, a, b, 1.0, 3.0)),
                        "bedeckung_hang": r2(bedeckung(P, sd, a, b, 3.0, 10.0, 0.2)), "faktor_laenge": r2(Lf)})
    return out


def pruefen(P, kz):
    T = P.T
    F, Wn = list(P.fehler), []
    q = T["je_10m"]
    for k in kz:
        Lf = k["faktor_laenge"]
        if Lf < 0.6:
            continue
        tag = "%s s %.0f-%.0f" % (k["seite"], k["s"][0], k["s"][1])
        for kl, key in (("K2_schutt", "K2_schutt"), ("K3_stein", "K3_stein"), ("K4_block", "K4_block")):
            lo, hi = q[key][0] * Lf, (q["K2_max_referenz"] if kl == "K2_schutt" else q[key][1]) * Lf
            if not (math.floor(lo) - 1 <= k[kl] <= math.ceil(hi) + 1):
                F.append("%s: %s %d ausserhalb %.0f-%.0f" % (tag, kl, k[kl], lo, hi))
        if k["fuss_im_wasser"] < max(1, int(q["fuss_im_wasser"][0] * Lf) - 1):
            F.append("%s: Fuss im Wasser %d" % (tag, k["fuss_im_wasser"]))
        for band in ("kante", "ufer", "hang"):
            zb = bedeckung_ziel(P, k["seite"], k["s"][0], k["s"][1], band)
            if k["bedeckung_" + band] < zb - 0.02:
                F.append("%s: Bedeckung %s %.2f < %.2f" % (tag, band, k["bedeckung_" + band], zb))
        if k["formen_ab_0_5m"] < T["lesbarkeit_30m"]["formen_ab_0_5m_je_10m_min"]:
            F.append("%s: nur %d Einzelformen >= 0,5 m (Lesbarkeit aus 30 m)" % (tag, k["formen_ab_0_5m"]))
        if k["kontakt_anteil"] < T["kontakt_min"]:
            F.append("%s: Kontakt %.2f" % (tag, k["kontakt_anteil"]))
        if k["eingraben_drittel_anteil"] < T["eingraben"]["anteil_min_ab_drittel"]:
            F.append("%s: Eingraben %.2f" % (tag, k["eingraben_drittel_anteil"]))
        if k["ritze_anteil"] < T["pflanzen"]["ritze_anteil_min"] and k["gras_ritze"] + k["farn"] > 0:
            F.append("%s: Ritzen-Anteil %.2f" % (tag, k["ritze_anteil"]))
        if k["K3_stein"] and k["K2_schutt"] / max(k["K3_stein"], 1) < T["verhaeltnis"]["K2_zu_K3"][0] - 0.3:
            Wn.append("%s: K2/K3 nur %.1f" % (tag, k["K2_schutt"] / max(k["K3_stein"], 1)))
    T_h = T["haufen"]["stuecke"]
    hz = {}
    for e in P.inst:
        if 0 <= e["haufen"] < 1000 and e["rolle"] in ("stein", "fussstein", "block"):
            hz[(e["seite"], e["haufen"])] = hz.get((e["seite"], e["haufen"]), 0) + 1
    for (sd, h), n in sorted(hz.items()):
        if not (T_h[0] <= n <= T_h[1]):
            F.append("%s Haufen %d: %d Stueck (Soll %d-%d)" % (sd, h, n, T_h[0], T_h[1]))
    for sd in ("links", "rechts"):
        gl = sum(b - a for a, b in P.grasluecken.get(sd, []))
        lo, hi = T["kante"]["gras_ueberhang_anteil"]
        if P.gleit_laenge.get(sd, 0) > 20 and not (lo - 0.01 <= gl / P.gleit_laenge[sd] <= hi + 0.02):
            F.append("%s: Grasluecken %.1f %% der Gleitufer-Kante (Soll %d-%d %%)" % (sd, 100 * gl / P.gleit_laenge[sd], 100 * lo, 100 * hi))
    Dz = dichte(P, P.abschnitte)
    for sd in ("links", "rechts"):
        if Dz[sd]["felsdeckung_obergrenze_prozent"] < Dz["soll"]["felsdeckung_obergrenze_min_prozent"]:
            F.append("%s: Felsdeckung (Obergrenze) %.0f %% < %d %%" % (sd, Dz[sd]["felsdeckung_obergrenze_prozent"],
                                                                     Dz["soll"]["felsdeckung_obergrenze_min_prozent"]))
        if Dz[sd]["anteil_felsdeckung_ab_1m"] < Dz["soll"]["anteil_felsdeckung_ab_1m_min"]:
            F.append("%s: Felsdeckung aus Netzen >= 1 m nur %.2f" % (sd, Dz[sd]["anteil_felsdeckung_ab_1m"]))
        if Dz[sd]["anteil_stehende_bloecke"] < Dz["soll"]["anteil_stehende_bloecke_min"]:
            F.append("%s: Felsdeckung aus stehenden Bloecken nur %.2f" % (sd, Dz[sd]["anteil_stehende_bloecke"]))
    if Dz["verschiedene_netze"] > Dz["soll"]["verschiedene_netze_max"]:
        F.append("verschiedene Netze %d > %d" % (Dz["verschiedene_netze"], Dz["soll"]["verschiedene_netze_max"]))
    G = P.G
    for e in P.inst:
        W = G.spiegel(e["s"], 1.0 if e["seite"] == "links" else -1.0)
        if e["rolle"] in ("gras_ritze", "gras_kante", "farn_ritze", "farn", "busch", "gehoelz") and e["zt"] < W + 0.05:
            F.append("%s im Wasser bei s %.1f" % (e["rolle"], e["s"]))
        if e["rolle"] == "gras_kante" and e["zt"] + (e["z_rel"] or 0) < W + T["kante"]["gras_fuss_ueber_spiegel_min_m"] - 0.03:
            F.append("Gras-Ueberhang Fuss < 0,3 m ueber Spiegel bei s %.1f" % e["s"])
        if e["rolle"] == "moos_boden" and e["zt"] < W + T["moos"]["ab_ueber_spiegel_m"]:
            F.append("Moos unter 1 m ueber Spiegel bei s %.1f" % e["s"])
        if e["rolle"] in ("gras_ritze",) and e["d"] <= 3.0 and e["h"] > T["pflanzen"]["gras_hoehe_max_band_0_3_m"] + 1e-6:
            F.append("Gras %.2f m hoch im Band 0-3 m" % e["h"])
        if e["kol"] != (e["g"] >= T["kollision_ab_m"] and e["rolle"] in ("stein", "fussstein", "block", "haufen_kern", "stapel", "wand", "fels",
                                                                          "gehoelz")):
            F.append("Kollision falsch %s" % e["netz"])
        if e["hind"] and e["rolle"] in P.R["swr_hindernis"]["rollen_nie"]:
            F.append("SWR-Hindernis mit Rolle %s" % e["rolle"])
        if e["d"] > P.R["grenze_auftrag_21_m"] + 0.3:
            F.append("%s jenseits 10 m (Auftrag 21) bei d %.1f" % (e["rolle"], e["d"]))
        if e["rolle"] in STEINROLLEN and e["g"] > NETZFORM["ab_m"]:
            gx, gy, gz = P.N.gr(e["netz"])
            if max(gx, gy) / max(gz, 1e-6) < NETZFORM["verhaeltnis_min"]:
                F.append("Netzform: %s %.1f m wuerfelig/stehend" % (e["netz"], e["g"]))
        if e["rolle"] in STEINROLLEN and e["z_abs"] and e["top"] < W + 0.1:
            F.append("Fuss-Stein ragt nicht aus dem Wasser bei s %.1f" % e["s"])
    return F, Wn


# ======================================================================================================================
def schreiben(P, abschnitte, kz, F, Wn, aus):
    T, N = P.T, P.N
    os.makedirs(aus, exist_ok=True)
    mv = P.R["material_vorschlag"]
    dateien = {}
    for nr, e in enumerate(P.inst):
        key = e["netz"] + ("_kol" if e["kol"] else "") + ("_trocken" if e.get("trocken") else "")
        r = N.R[e["netz"]]
        if key not in dateien:
            mats = (N.masse.get(r["pfad"]) or {}).get("mats") or []
            pm = mats[0].split("/")[-1].split(".")[0] if mats else None
            paket = r["paket"]
            if "/Fab/" in r["pfad"] and e["rolle"] in STEINROLLEN + ("schutt", "kies", "platte", "wand", "fels"):
                mvs = "MI_EL_%s auf M_EL_Fels_MS2" % e["netz"]
            elif paket == "Mountain_Environment_Set" and e["rolle"] in STEINROLLEN + ("schutt", "kies", "wand", "fels"):
                basis = pm[3:] if pm and pm.startswith("MI_") else (pm or e["netz"])
                mvs = "MI_EL_NL_%s (Kind von M_EL_Mountain_NL, wie 6f)" % basis
            elif paket in ("Megascans",) and e["rolle"] in STEINROLLEN + ("schutt", "kies", "platte", "wand", "fels"):
                mvs = "vorhandene MI_EL_%s bzw. neu auf M_EL_Fels_MS2" % e["netz"]
            elif paket == "Namaqualand":
                mvs = mv["Namaqualand"]
            elif e["rolle"] in STEINROLLEN + ("schutt", "kies", "platte", "wand", "fels"):
                mvs = "MI_EL_NL_%s auf M_EL_Fels_MS2 (Kopie des Paket-MI %s, Nasslinie)" % (e["netz"], pm)
            else:
                mvs = None
            if e.get("trocken"):
                mvs = "MI_EL_%s_trocken (Kopie mit braunem Tint, Auftrag 20 §2)" % e["netz"]
            sw = T["sichtweite_cm"][KLASSE_SW[e["rolle"]]]
            dateien[key] = {"netz": e["netz"], "pfad": r["pfad"], "ebene": EBENE[e["rolle"]], "rollen": {}, "kollision": e["kol"],
                            "sichtweite": [0, sw], "schatten": EBENE[e["rolle"]] not in ("kleinzeug", "kontakt"),
                            "groesse_m": list(N.gr(e["netz"])), "nanite": r["nanite"] == "1", "paket": paket,
                            "paket_mi": pm, "material_vorschlag": mvs, "eintraege": []}
        dd = dateien[key]
        dd["rollen"][e["rolle"]] = dd["rollen"].get(e["rolle"], 0) + 1
        dd["eintraege"].append([r2(e["s"]), r2(e["u"]), r2(e["skala"], 3), r2(e["yaw"], 1), r2(e["kipp"], 1), r2(e["einb"]),
                                r2(e["g"]), r2(e["z"], 3), bool(e["hind"]), nr, bool(e["z_abs"]),
                                (r2(e["z_rel"], 3) if e["z_rel"] is not None else None), e["rolle"], e["seite"], r2(e["d"]),
                                int(e["haufen"]), int(e["lage"])])
    for k in sorted(dateien):
        dateien[k]["anzahl"] = len(dateien[k]["eintraege"])
    rollen = {}
    for e in P.inst:
        rollen[e["rolle"]] = rollen.get(e["rolle"], 0) + 1
    n_kol = sum(1 for e in P.inst if e["kol"])
    X = P.X
    bett_n = X["I"].n
    bett_kol = sum(1 for x in X["liste"] if x["kol"])
    out = {"format": FORMAT_ID, "stand": P.R["stand"], "biom": "tundra", "ebene": "detailgrad", "ft_praefix": "FT_EL_DG_", "abschnitt": "talkaskade s %.0f-%.0f" % (abschnitte[0][0], abschnitte[-1][1]),
           "quelle": "skripte/p2_bett/p2_bettplan.py (Gelaende 6c/6f, Bettkante, Spiegel) + skripte/detailgrad/detailgrad_regeln.json",
           "koordinaten": "Bach wie bettplan_p2.json: s = m entlang lauf_p2, u = m quer (u > 0 links), d = m aussen ab der Bettkante. "
                          "Welt: p2_bett_welt.py --instanzen-plan (FORMAT §3 je Feld, Ebene detailgrad, FT_EL_DG_*).",
           "z_regel": "z_absolut = true: z_plan_m absolut (Fuss-Steine: Oberkante 0,15-0,4 m ueber dem Spiegel); z_rel_m gesetzt: z = "
                      "Gelaende(x, y) + z_rel_m (2. Lage verkeilt, Gras-Ueberhang); sonst z = Gelaende(x, y) - einbettung x Netzhoehe.",
           "grenze": "nur 0-10 m ab der Wasserkante; darueber Auftrag 21 (skripte/felsdeckung/)",
           "spalten": SPALTEN,
           "budget": {"regel_je_feld": P.R["budget_je_feld"], "feld": "C2",
                      "detailgrad": {"instanzen": len(P.inst), "kollision": n_kol},
                      "bettplan_p2": {"instanzen": bett_n, "kollision": bett_kol},
                      "summe": {"instanzen": len(P.inst) + bett_n, "kollision": n_kol + bett_kol},
                      "hinweis": "ohne bachdekor (Bett) und Landschaftsgras; Talkaskade liegt in C2"},
           "rollen": dict(sorted(rollen.items())),
           "swr_hindernisse": sum(1 for e in P.inst if e["hind"]),
           "dichte_band_0_10m": dichte(P, abschnitte),
           "kennzahlen_je_10m": kz,
           "kennzahlen_mittel_je_10m_seite": mittel(kz),
           "pruefung": {"fehler": F, "warnungen": Wn},
           "dateien": {k: dateien[k] for k in sorted(dateien)}}
    with open(os.path.join(aus, "plan_p2_talkaskade.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    return out


FELSROLLEN = ("kies", "schutt", "stein", "fussstein", "block", "haufen_kern", "stapel", "platte", "wand", "fels")


def dichte(P, abschnitte):
    """Wie Ferats Dichte-Zensus (16h N6h), aber nur Band 0-10 m je Seite: Netze je 100 m2, Felsdeckung als Obergrenze
    (Summe Kasten-Grundflaeche x Skala^2, Ueberlappung mitgezaehlt), Anteil der Deckung aus Netzen >= 1 m, verschiedene Netze."""
    D = P.R["biome"]["tundra"]["dichte"]
    L = sum(b - a for a, b in abschnitte)
    out = {}
    for sd in ("links", "rechts"):
        sel = [e for e in P.inst if e["seite"] == sd and -0.6 <= e["d"] <= 10.0]
        flaeche = L * 10.0
        dk, dk1, dks = 0.0, 0.0, 0.0
        for e in sel:
            if e["rolle"] in FELSROLLEN:
                gx, gy, gz = P.N.gr(e["netz"])
                f = gx * gy * e["skala"] ** 2
                dk += f
                if e["g"] >= 1.0:
                    dk1 += f
                    if e["rolle"] != "platte":
                        dks += f
        out[sd] = {"flaeche_m2": r2(flaeche, 0), "netze_je_100m2": r2(100.0 * len(sel) / flaeche),
                   "klein_unter_0_5m_je_100m2": r2(100.0 * sum(1 for e in sel if e["g"] < 0.5) / flaeche),
                   "mittel_0_5_3m_je_100m2": r2(100.0 * sum(1 for e in sel if 0.5 <= e["g"] < 3.0) / flaeche),
                   "gross_ab_3m_je_100m2": r2(100.0 * sum(1 for e in sel if e["g"] >= 3.0) / flaeche, 3),
                   "felsdeckung_obergrenze_prozent": r2(100.0 * dk / flaeche, 1),
                   "anteil_felsdeckung_ab_1m": r2(dk1 / max(dk, 1e-9)),
                   "anteil_stehende_bloecke": r2(dks / max(dk, 1e-9))}
    out["verschiedene_netze"] = len({e["netz"] for e in P.inst})
    out["vergleich"] = {"RA2": {"netze_je_100m2": 8.74, "felsdeckung_obergrenze_prozent": 378.4, "verschiedene_netze": 53},
                        "C2_fenster_200m": {"netze_je_100m2": 24.03, "felsdeckung_obergrenze_prozent": 1.22, "verschiedene_netze": 181},
                        "quelle": "recherche/auftraege/daten/dichte/dichte_vergleich.md (Ferat, 13.10.2026)"}
    out["soll"] = {k: D[k] for k in ("felsdeckung_obergrenze_min_prozent", "anteil_felsdeckung_ab_1m_min", "anteil_stehende_bloecke_min",
                                     "verschiedene_netze_max")}
    return out


def mittel(kz):
    vs = [k for k in kz if k["faktor_laenge"] >= 0.99]
    out = {}
    for key in ("K1_kies", "K2_schutt", "K3_stein", "K4_block", "formen_ab_0_5m", "hang_K3", "schuttband", "fuss_im_wasser", "gras_ritze", "farn", "busch", "kontakt_anteil",
                "eingraben_drittel_anteil", "ritze_anteil", "bedeckung_kante", "bedeckung_ufer", "bedeckung_hang"):
        a = [k[key] for k in vs]
        out[key] = [r2(min(a)), r2(float(np.median(a))), r2(max(a))]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--aus", default=HIER, help="Ordner fuer plan_p2_talkaskade.json (Standard: skripte/detailgrad/)")
    ap.add_argument("--bild-aus", dest="bild_aus", default=os.path.join(ANTW, "detailgrad"))
    ap.add_argument("--bild", action="store_true")
    ap.add_argument("--selbsttest", action="store_true")
    a = ap.parse_args(argv)
    P, abschnitte, X = plane()
    kz = kennzahlen(P, abschnitte)
    F, Wn = pruefen(P, kz)
    out = schreiben(P, abschnitte, kz, F, Wn, a.aus)
    if a.bild:
        import detailgrad_bilder as db
        os.makedirs(a.bild_aus, exist_ok=True)
        db.alle(P, abschnitte, kz, out, a.bild_aus)
    print(json.dumps({"rollen": out["rollen"], "budget": out["budget"], "mittel": out["kennzahlen_mittel_je_10m_seite"],
                      "dichte": out["dichte_band_0_10m"],
                      "swr_hindernisse": out["swr_hindernisse"]}, ensure_ascii=False))
    for w in Wn[:20]:
        print("WARNUNG", w)
    for f in F[:40]:
        print("FEHLER", f)
    rc = 1 if F else 0
    if a.selbsttest:
        import tempfile
        h = []
        for _ in range(2):
            pb._KNOTEN.clear()
            d = tempfile.mkdtemp()
            P2, ab2, _x = plane()
            kz2 = kennzahlen(P2, ab2)
            F2, W2 = pruefen(P2, kz2)
            schreiben(P2, ab2, kz2, F2, W2, d)
            with open(os.path.join(d, "plan_p2_talkaskade.json"), "rb") as f:
                h.append(hashlib.sha256(f.read()).hexdigest())
        with open(os.path.join(a.aus, "plan_p2_talkaskade.json"), "rb") as f:
            h0 = hashlib.sha256(f.read()).hexdigest()
        print("[selbsttest] zwei Laeufe byte-gleich: %s; gleich der Ausgabe: %s; %s" % (h[0] == h[1], h0 == h[0], h0[:12]))
        if not (h[0] == h[1] == h0):
            rc = 1
    print("[detailgrad_plan] %d FEHLER, %d WARNUNGEN, %d Instanzen" % (len(F), len(Wn), len(P.inst)))
    return rc


if __name__ == "__main__":
    sys.exit(main())
