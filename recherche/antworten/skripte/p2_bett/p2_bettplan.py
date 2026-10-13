# -*- coding: utf-8 -*-
"""p2_bettplan.py - 16h Nachtrag 6c: natuerlicher Bettplan (Step-Pool) fuer Erlenbach p2, Talkaskade s 389-579.

Ferat (6c): Die Becken wirken kuenstlich - rund, gleich gross, alle 3-4 m eine Stufe (Brush 'Kasten-U'). Gewuenscht sind
unregelmaessige Abstaende (1-4 Bachbreiten, nach dem Gefaelle), verschiedene Fallhoehen, laengliche, seitlich versetzte
Becken (Talweg pendelt), einzelne ruhige Strecken, Stufen aus Bloecken; Becken 0,8-1,2 m, Uferstufe 0,2-0,5 m, Rinnen
0,2-0,4 m (Antwort 18). Grundlage sind die Regeln aus 15f/15g (schraege, gekruemmte, gekerbte Lippen, Buchten,
Eck- und Randbloecke) - hier eigenstaendig in Bach-Koordinaten umgesetzt, weil die p2-Spline (lauf_p2.json) und das
gegrabene Gelaende nur lokal vorliegen.

Eingabe:  antworten/fluss_sim/p2_lokal/querschnitte_p2.json (Ferat 13.10.: Spiegel, Breite, Uferprofile alle 2 m)
          skripte/p2_bett/p2_bett_regeln.json, skripte/gefaelle/gefaelle_regeln.json (Tundra-Palette),
          vorlagen/daten/netze.csv + netz_sperre.json (Inventar)
Ausgabe (--aus, Standard antworten/p2_bett/):
  bettplan_p2.json        Einheiten, Lippen, Becken, Spiegel je Meter (SWR-Spline), Instanzen (s, u), Kennzahlen, Pruefung
  talkaskade_soll.f32     Gelaende-Soll in Bach-Koordinaten, float32 LE, Form [5, ns, nu]:
                          z_min, z_max (NaN = keine Grenze), Gewicht 0..1, Wasserspiegel, Abtrag_max (NaN = frei),
                          Abstand zur neuen Bettkante (m, 0 im Bett; fuer die 2-m-Band-Pruefung nach dem Bake).
                          Neu = max(Ist + w * (clip(Ist, z_min, z_max) - Ist), Ist - Abtrag_max). Bett: z_min = z_max
                          (setzen); Schulter: z_min = Spiegel + Uferstufe (anheben); Boeschung: z_max = 35 Grad
                          (zuruecklegen), Abtrag hoechstens so tief wie der Einschnitt gegen den alten Spiegel.
  talkaskade_zonen.u8     Zone je Zelle (uint8, [ns, nu]): 0 aussen, 1 Bett, 2 Kolk, 3 Lippenkrone, 4 Stufenwand/Rampe,
                          5 Uferstufe, 6 Schulter, 7 Boeschung
  Bilder (p2_bett_bilder.py): talkaskade_delta.png, talkaskade_tiefe.png, talkaskade_laengsprofil.png,
                          talkaskade_querschnitte.png
Welt (lokal): p2_bett_welt.py rechnet (s, u) ueber lauf_p2.json in Weltzellen um und schreibt das A15-Format.

Koordinaten: s = m entlang lauf_p2 wie querschnitte_p2.json; u = m quer, u > 0 links (Ferat: links = (-t_j, t_i)).
Deterministisch (Zufall = sha256 aus Schluesseln). Eingebaute Pruefung, Exit 1 bei FEHLER.

  python -I recherche/antworten/skripte/p2_bett/p2_bettplan.py [--aus DIR] [--ohne-bilder] [--selbsttest]
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
REGELN = os.path.join(HIER, "p2_bett_regeln.json")
GEF_REGELN = os.path.join(ANTW, "skripte", "gefaelle", "gefaelle_regeln.json")
QUER = os.path.join(ANTW, "fluss_sim", "p2_lokal", "querschnitte_p2.json")

DS = 0.5          # Rasterweite laengs (m)
DU = 0.25         # Rasterweite quer (m)
U_MAX = 12.5      # Raster quer +-U_MAX
FORMAT = "p2_bett_v1"
ZONEN = {0: "aussen", 1: "bett", 2: "kolk", 3: "lippenkrone", 4: "stufenwand_rampe", 5: "uferstufe", 6: "schulter",
         7: "boeschung"}
SPALTEN = ["s_m", "u_m", "skala", "yaw_rel_grad", "kipp_grad", "einbettung", "groesse_m", "z_plan_m", "swr_hindernis",
           "nr", "z_absolut"]


# ======================================================================================================================
# Zufall, Formen
# ======================================================================================================================
def zufall(*teile):
    h = hashlib.sha256("|".join(str(t) for t in teile).encode("utf-8")).digest()
    return int.from_bytes(h[:8], "little") / 2.0 ** 64


def zw(a, b, *teile):
    return a + (b - a) * zufall(*teile)


def glatt(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def clamp(x, a, b):
    return max(a, min(b, x))


_KNOTEN = {}


def rauschen1(s, seed, wl):
    """1-D Wertrauschen in [-1, 1], Knoten alle wl m, glatt interpoliert (deterministisch)."""
    s = np.asarray(s, dtype=float)
    x = s / wl
    i0 = np.floor(x).astype(np.int64)
    f = glatt(x - i0)

    def h(i):
        k = (seed, round(wl, 6), int(i))
        if k not in _KNOTEN:
            _KNOTEN[k] = 2.0 * zufall("rauschen", seed, round(wl, 6), int(i)) - 1.0
        return _KNOTEN[k]
    hv = np.vectorize(h, otypes=[float])
    return hv(i0) * (1.0 - f) + hv(i0 + 1) * f


def r2(v, n=2):
    return float(round(float(v), n))


# ======================================================================================================================
# Ist-Daten aus Ferats Querschnitten
# ======================================================================================================================
def profil_h(P, d):
    """Hoehe des Profils (d ab Wasserkante, z) am Abstand d; ausserhalb Randwert."""
    if d <= P[0][0]:
        return P[0][1]
    for (d0, z0), (d1, z1) in zip(P, P[1:]):
        if d0 <= d <= d1:
            return z0 + (z1 - z0) * (d - d0) / max(d1 - d0, 1e-9)
    return P[-1][1]


class Ist:
    def __init__(self, Q, R):
        sec = {}
        for q in Q:
            e = sec.setdefault(float(q["s"]), {"ab": q["abschnitt"]})
            e["sp"] = float(q["spiegel_m"])
            e["B"] = float(q["breite_m"])
            e[q["seite"]] = [(float(d), float(z)) for d, z in q["profil"]]
        self.s = np.array(sorted(sec))
        self.sec = [sec[s] for s in self.s]
        self.sp = np.array([e["sp"] for e in self.sec])
        self.B = np.array([e["B"] for e in self.sec])
        dr = R["narbe"]["d_ref_m"]
        self.T_seite = {sd: np.array([profil_h(e[sd], dr) if sd in e else np.nan for e in self.sec])
                        for sd in ("links", "rechts")}
        T = np.fmin(self.T_seite["links"], self.T_seite["rechts"])
        n1 = max(1, int(round(R["narbe"]["glaetten"]["min_fenster_m"] / 2.0 / 2.0)))
        n2 = max(1, int(round(R["narbe"]["glaetten"]["mittel_fenster_m"] / 2.0 / 2.0)))
        T1 = np.array([np.nanmin(T[max(0, i - n1):i + n1 + 1]) for i in range(len(T))])
        T2 = np.array([np.nanmean(T1[max(0, i - n2):i + n2 + 1]) for i in range(len(T1))])
        self.T = np.minimum.accumulate(T2)
        nb = max(1, int(round(R["breite"]["median_fenster_m"] / 2.0 / 2.0)))
        self.Bm = np.array([float(np.median(self.B[max(0, i - nb):i + nb + 1])) for i in range(len(self.B))])

    def narbe(self, s):
        return float(np.interp(s, self.s, self.T))

    def narbe_seite(self, s, sd):
        return float(np.interp(s, self.s, self.T_seite[sd]))

    def breite(self, s):
        return float(np.interp(s, self.s, self.Bm))

    def _i(self, s):
        return int(np.clip(np.round((s - self.s[0]) / 2.0), 0, len(self.s) - 1))

    def spiegel_alt(self, s):
        """Alter Plan-Spiegel: Wert des naechsten Querschnitts (Stufen liegen zwischen den 2-m-Schnitten)."""
        return float(self.sp[self._i(s)])

    def ufer(self, s, sd, d):
        """Ist-Gelaende neben dem alten Bett: Profil d ab alter Kante, linear zwischen den Querschnitten."""
        x = (s - self.s[0]) / 2.0
        i0 = int(np.clip(np.floor(x), 0, len(self.s) - 1))
        i1 = min(i0 + 1, len(self.s) - 1)
        t = float(np.clip(x - i0, 0.0, 1.0))
        z0 = profil_h(self.sec[i0][sd], d)
        z1 = profil_h(self.sec[i1][sd], d)
        return z0 + (z1 - z0) * t

    def alte_lippen(self, s0, s1):
        """Alte Stufen (Spiegelwechsel zwischen zwei Schnitten) im Bereich: Liste (s_lippe, fall)."""
        out = []
        for i in range(len(self.s) - 1):
            a, b = self.s[i], self.s[i + 1]
            if s0 <= a and b <= s1 and self.sp[i] - self.sp[i + 1] > 0.05:
                out.append((float((a + b) / 2.0), float(self.sp[i] - self.sp[i + 1])))
        return out

    def ist_raster(self, S, U):
        """Ist-Gelaende auf dem Plan-Raster. Ufer aus den Querschnitten; altes Bett ANGENOMMEN nach Ferats Kennzahlen
        (Kasten-U, Tiefe am Fuss 1,0 m, vor der Lippe 0,55 m; 6c: 0,76-1,20 / 0,36-0,71 m)."""
        Z = np.zeros((len(S), len(U)))
        lip = [l for l, _ in self.alte_lippen(S[0] - 10, S[-1] + 10)]
        for a, s in enumerate(S):
            B = float(np.interp(s, self.s, self.B))
            h = B / 2.0
            sp = self.spiegel_alt(s)
            vor = [l for l in lip if l <= s]
            nach = [l for l in lip if l > s]
            fu = (vor[-1] + 0.5) if vor else s - 2.0
            li = nach[0] if nach else s + 2.0
            t = float(np.clip((s - fu) / max(li - fu, 0.5), 0.0, 1.0))
            dc = 1.0 - 0.45 * t
            for b, u in enumerate(U):
                if abs(u) <= h:
                    x = abs(u) / h
                    Z[a, b] = sp - dc * (1.0 - glatt((x - 0.6) / 0.4))
                else:
                    Z[a, b] = self.ufer(s, "links" if u > 0 else "rechts", abs(u) - h)
        return Z


# ======================================================================================================================
# Einheiten: Stufe/Kaskade/Schnelle + Becken bis zur naechsten Lippe
# ======================================================================================================================
def wand_m(D):
    return clamp(0.3 * D + 0.3, 0.4, 1.0)


def teilung(D, kl, St, seed, k):
    """Fallhoehen einer Einheit: eine Stufe oder eine Blockkaskade (Teilhoehen streuen, jede im Bereich)."""
    smax = kl.get("stufe_max_m", St["D_einzeln_max_m"])
    if D <= smax:
        return [D]
    ziel = kl.get("teil_ziel_m", St["kaskade"]["teil_ziel_m"])
    lo, hi = St["kaskade"]["teil_m"]
    hi = max(hi, smax)
    n_min = max(2, int(math.ceil(D / hi - 1e-9)))
    n_max = max(n_min, int(math.floor(D / lo + 1e-9)))
    n = int(clamp(int(math.ceil(D / ziel - 1e-9)), n_min, n_max))
    sr = St["kaskade"]["teilhoehen_streuung"]
    w = [1.0 + sr * (2.0 * zufall(seed, "teil", k, n, i) - 1.0) for i in range(n)]
    h = [D * x / sum(w) for x in w]
    for _ in range(20):
        h = [clamp(x, lo, hi) for x in h]
        f = D / sum(h)
        h = [x * f for x in h]
        if all(lo - 1e-6 <= x <= hi + 1e-6 for x in h):
            return h
    return [D / n] * n


def kaskade_laenge(h, B, St, seed, k):
    """Laenge der Teilbecken + Waende einer Kaskade (ohne Hauptbecken)."""
    if len(h) <= 1:
        return 0.0, []
    tb = [zw(*St["kaskade"]["teilbecken_B"], seed, "tb", k, i) * B for i in range(len(h) - 1)]
    return sum(wand_m(x) for x in h[:-1]) + sum(tb), tb


def plane_einheiten(ist, R, ab, seed):
    A = R["abschnitte"][ab]
    s0, s1 = A["s_m"]
    P_vor, P0 = ist.spiegel_alt(s0 - 1.0), ist.spiegel_alt(s0 + 1.0)
    P_end, P_nach = ist.spiegel_alt(s1 - 1.0), ist.spiegel_alt(s1 + 1.0)
    E, St, Uf = R["einheit"], R["stufe"], R["uferstufe"]
    KL = {k["name"]: k for k in E["klassen"]}

    def fak(s):
        S = max((ist.narbe(s - 5.0) - ist.narbe(s + 5.0)) / 10.0, 0.05)
        return clamp((E["gefaelle_bezug"] / S) ** E["gefaelle_exponent"], *E["gefaelle_faktor"])

    def klasse(k, verlauf, s, s_ruhig):
        for v in range(12):
            r = zufall(seed, "klasse", k, v)
            acc = 0.0
            kl = E["klassen"][-1]
            for x in E["klassen"]:
                acc += x["anteil"]
                if r < acc:
                    kl = x
                    break
            if kl["name"] == "ruhig" and s - s_ruhig < E["ruhig_abstand_min_m"]:
                continue
            m = E["gleiche_klasse_max_folge"]
            if len(verlauf) >= m and all(x == kl["name"] for x in verlauf[-m:]):
                continue
            return kl
        return KL["mittel"]

    B0 = ist.breite(s0)
    U0 = zw(*Uf["einheit_m"], seed, "U", 0)
    EH = [{"k": 0, "a": s0, "b": s0 + zw(1.0, 1.4, seed, "L", 0) * B0, "P": P0, "D": P_vor - P0, "U": U0,
           "klasse": "anschluss", "teile": [P_vor - P0], "tb": [], "fest": True}]
    verlauf, s_ruhig, k = [], -1e9, 1
    while EH[-1]["b"] < s1 - 1e-6:
        a, Pp = EH[-1]["b"], EH[-1]["P"]
        kl = klasse(k, verlauf, a, s_ruhig)
        B = ist.breite(a)
        L = zw(*kl["L_B"], seed, "L", k) * B * fak(a)
        U = zw(*Uf["einheit_m"], seed, "U", k)
        final = False
        L_max = 1.05 * kl["L_B"][1] * B
        kurz_haupt = False
        for _ in range(80):
            b = a + L
            final = s1 - b < 1.0 * ist.breite(b)
            if final:
                b = s1
            P = P_end if final else max(ist.narbe(b) - U, P_end + 0.15)
            D = Pp - P
            h = teilung(D, kl, St, seed, k) if D > 0 else [D]
            kas, tb = kaskade_laenge(h, B, St, seed, k)
            if final:
                break
            need = kas + wand_m(h[-1]) + St["hauptbecken_min_B"] * B
            kopf = ist.narbe(a + kas + wand_m(h[-1])) - P
            if (D > St["D_einheit_max_m"] or kopf > kl["kopf_ufer_max_m"]) and L > 1.0 * B + 0.05:
                L = max(L * 0.92, 1.0 * B)
                continue
            if D < St["D_min_m"] and L < L_max:
                L = min(L * 1.15, L_max)
                continue
            if L < need - 1e-6:
                if L < L_max and D < St["D_einheit_max_m"]:
                    L = min(need + 0.05, L_max)
                    continue
                kurz_haupt = True
            break
        EH.append({"k": k, "a": a, "b": b, "P": P, "D": D, "U": U, "klasse": kl["name"], "teile": h, "tb": tb,
                   "final": final, "kopf_m": ist.narbe(a + kas + wand_m(h[-1])) - P, "hauptbecken_kurz": kurz_haupt})
        verlauf.append(kl["name"])
        if kl["name"] == "ruhig":
            s_ruhig = a
        k += 1
    # zu kleine Schlusseinheit mit der vorletzten zusammenlegen
    if len(EH) > 2 and EH[-1]["D"] < St["D_min_m"]:
        last = EH.pop()
        e = EH[-1]
        e["b"], e["P"], e["final"] = last["b"], last["P"], True
        e["D"] = EH[-2]["P"] - e["P"]
        kl = KL.get(e["klasse"], KL["mittel"])
        e["teile"] = teilung(e["D"], kl, St, seed, e["k"])
        _, e["tb"] = kaskade_laenge(e["teile"], ist.breite(e["a"]), St, seed, e["k"])
    for e in EH[1:]:
        if "kopf_m" not in e or e.get("final"):
            kas = sum(wand_m(x) for x in e["teile"][:-1]) + sum(e["tb"])
            e["kopf_m"] = ist.narbe(e["a"] + kas + wand_m(e["teile"][-1])) - e["P"]
    return EH, {"P_vor": P_vor, "P0": P0, "P_end": P_end, "P_nach": P_nach, "s0": s0, "s1": s1}


# ======================================================================================================================
# Lippen und Becken
# ======================================================================================================================
class Lippe:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def off(self, u, uc):
        """Laengsversatz der Lippenlinie gegen ihre Mitte (schraeg + Bogen, Scheitel stromab); im Ufer konstant."""
        u = np.asarray(u, dtype=float)
        h = max(self.Bl / 2.0, 0.3)
        x = np.clip((u - uc) / h, -1.0, 1.0)
        ut = np.clip(u - uc, -(h + 1.2), h + 1.2)
        return math.tan(math.radians(self.theta)) * ut - self.pfeil * x * x

    def linie(self, u, uc):
        return self.s + self.off(u, uc)

    def krone_tiefe(self, u, uc):
        """Wassertiefe ueber der Krone quer zur Lippe: Kerben (Rinne) tief, daneben duenn."""
        u = np.asarray(u, dtype=float)
        t = np.full(u.shape, self.krone)
        for (ur, w, tk) in self.kerben:
            d = np.abs(u - (uc + ur)) - (w / 2.0 - self.kerbe_rand)
            g = 1.0 - glatt(d / self.kerbe_rand)
            t = np.maximum(t, self.krone + (tk - self.krone) * g)
        return t


def baue_lippen_becken(EH, ist, R, rand, seed):
    St, Lr, Bk, Uf = R["stufe"], R["lippe"], R["becken"], R["uferstufe"]
    s0, s1 = rand["s0"], rand["s1"]
    Pd = R["lauf_pendel"]

    def uc(s):
        s = np.asarray(s, dtype=float)
        B = np.interp(s, ist.s, ist.Bm)
        amp = np.minimum(Pd["amp_B"] * B, Pd["amp_max_m"])
        wl = zw(*Pd["wellenlaenge_m"], seed, "pendel_wl")
        f = glatt((s - s0) / 6.0) * glatt((s1 - s) / 6.0)
        return amp * rauschen1(s, seed + "|pendel", wl) * f

    lippen = []
    # Kopf: bestehende Durchbruch-Stufe (unveraendert)
    lippen.append(Lippe(nr=0, s=s0, P_up=rand["P_vor"], P_dn=rand["P0"], D=rand["P_vor"] - rand["P0"], art="bestand",
                        einheit=0, teil=0, theta=0.0, pfeil=0.0, Bl=ist.breite(s0), kerben=[], krone=0.05,
                        kerbe_rand=0.3, wand=0.5, seite=0))
    for e in EH[1:]:
        a, Pp = e["a"], EH[e["k"] - 1]["P"]
        pos, lvl = a, Pp
        n = len(e["teile"])
        B_e = ist.breite(a)
        schlupf = e["b"] - (a + sum(wand_m(x) for x in e["teile"]) + sum(e["tb"])) - St["hauptbecken_min_B"] * B_e
        for i, hgt in enumerate(e["teile"]):
            art = "stufe" if n == 1 else "kaskade_teil"
            rampe = clamp(3.0 * hgt, 1.5, 3.0)
            if n == 1 and hgt <= St["schnelle"]["D_max_m"] and zufall(seed, "schnelle", e["k"]) < St["schnelle"]["anteil"]:
                art = "schnelle"
            elif n > 1 and hgt <= St["kaskade"]["rampe_bis_m"] and rampe - wand_m(hgt) <= schlupf and \
                    zufall(seed, "rampe", e["k"], i) < St["kaskade"]["rampe_anteil"]:
                art = "schnelle"
                schlupf -= rampe - wand_m(hgt)
            w = rampe if art == "schnelle" else wand_m(hgt)
            lippen.append(Lippe(nr=len(lippen), s=pos, P_up=lvl, P_dn=lvl - hgt, D=hgt, art=art, einheit=e["k"], teil=i,
                                wand=w))
            lvl -= hgt
            if i < n - 1:
                pos += w + e["tb"][i]
    lippen.append(Lippe(nr=len(lippen), s=s1, P_up=rand["P_end"], P_dn=rand["P_nach"], D=rand["P_end"] - rand["P_nach"],
                        art="ende", einheit=EH[-1]["k"] + 1, teil=0, wand=wand_m(rand["P_end"] - rand["P_nach"])))
    # Form: Winkel, Bogen, Kerben, Seitenwechsel
    seite = 1.0 if zufall(seed, "seite0") < 0.5 else -1.0
    th_haupt = 0.0
    for L in lippen[1:]:
        B = ist.breite(L.s)
        L.Bl = B * Lr["einschnuerung"]
        if L.teil == 0:
            if zufall(seed, "wechsel", L.nr) < Lr["seitenwechsel_anteil"]:
                seite = -seite
            sg = 1.0 if zufall(seed, "thsg", L.nr) < 0.5 else -1.0
            L.theta = sg * zw(*Lr["winkel_grad"], seed, "th", L.nr)
            th_haupt = L.theta
        else:
            if zufall(seed, "wechsel", L.nr) < Lr["seitenwechsel_anteil"]:
                seite = -seite
            sp = Lr["kaskade_winkel_streuung_grad"]
            L.theta = math.copysign(clamp(abs(th_haupt) + zw(-sp, sp, seed, "th", L.nr), 8.0, 32.0), th_haupt)
        L.seite = seite
        L.pfeil = zw(*Lr["pfeil_B"], seed, "pf", L.nr) * L.Bl
        K = Lr["kerbe"]
        if L.art == "schnelle":
            w = clamp(zw(0.3, 0.45, seed, "kw", L.nr) * L.Bl, *K["breite_m"])
        else:
            w = clamp(zw(*K["breite_B"], seed, "kw", L.nr) * L.Bl, *K["breite_m"])
        ur = seite * zw(*K["lage_B"], seed, "kl", L.nr) * L.Bl
        ur = math.copysign(min(abs(ur), L.Bl / 2.0 - w / 2.0 - 0.15), ur) if abs(ur) > 0 else ur
        L.kerben = [(ur, w, zw(*K["tiefe_m"], seed, "kt", L.nr))]
        if B >= K["zwei_ab_B_m"] and zufall(seed, "k2", L.nr) < K["zwei_anteil"]:
            w2 = 0.7 * w
            u2 = -seite * zw(0.12, 0.3, seed, "k2l", L.nr) * L.Bl
            if abs(u2 - ur) >= (w + w2) / 2.0 + 0.3 and abs(u2) + w2 / 2.0 <= L.Bl / 2.0 - 0.1:
                L.kerben.append((u2, w2, zw(0.12, 0.2, seed, "k2t", L.nr)))
        L.krone = zw(*Lr["krone_unter_spiegel_m"], seed, "kr", L.nr)
        L.kerbe_rand = K["rand_m"]
        L.uc = float(uc(L.s))
    lippen[0].uc = float(uc(s0))
    # Letzte Lippe faellt auf das unveraenderte Kiesbett: nur wenig schraeg, damit der Spiegel bei s1 - 1 bleibt
    lippen[-1].theta = math.copysign(min(abs(lippen[-1].theta), 10.0), lippen[-1].theta)
    lippen[-1].pfeil = min(lippen[-1].pfeil, 0.05 * lippen[-1].Bl)
    # Versatz begrenzen: Linien schneiden sich nie, Becken an jeder Stelle >= halbe Nennlaenge (und >= 0,5 m)
    uu = np.arange(-U_MAX, U_MAX + 1e-9, DU)
    for j in range(1, len(lippen)):
        A_, B_ = lippen[j - 1], lippen[j]
        nenn = B_.s - A_.s - A_.wand
        for _ in range(14):
            gap = B_.linie(uu, B_.uc) - (A_.linie(uu, A_.uc) + A_.wand)
            if gap.min() >= max(0.5, 0.5 * nenn):
                break
            B_.theta *= 0.7
            B_.pfeil *= 0.7
        else:
            B_.theta, B_.pfeil = 0.0, 0.0
    # Becken
    becken = []
    for j in range(len(lippen) - 1):
        A_, N_ = lippen[j], lippen[j + 1]
        if A_.art == "bestand":
            typ = "anschluss"
        elif A_.art == "schnelle":
            typ = "lauf"
        elif N_.teil > 0 and N_.einheit == A_.einheit:
            typ = "teil"
        else:
            typ = "haupt"
        Lp = N_.s - A_.s - A_.wand
        B = ist.breite(A_.s + A_.wand + Lp / 2.0)
        u_rel = A_.kerben[0][0] if A_.kerben else 0.0
        l = clamp(zw(*Bk["kolk_laenge_anteil"], seed, "kl_l", j) * Lp, Bk["kolk_laenge_m"][0], Bk["kolk_laenge_m"][1])
        l = min(l, 0.9 * Lp)
        w = zw(*Bk["kolk_breite_B"], seed, "kl_w", j) * B
        if l < Bk["kolk_streckung_min"] * w:
            w = l / Bk["kolk_streckung_min"]
        if typ == "haupt" or typ == "anschluss":
            dk = clamp(0.62 + Bk["kolk_tiefe_je_m_fall"] * max(A_.D, 0.3) * zw(0.8, 1.6, seed, "kl_d", j) +
                       zw(0.05, 0.25, seed, "kl_d2", j), *Bk["kolk_tiefe_m"])
        elif typ == "teil":
            dk = zw(0.55, 0.8, seed, "kl_d", j)
        else:
            dk = zw(0.5, 0.7, seed, "kl_d", j)
        uk = A_.uc + 0.9 * u_rel + zw(-0.15, 0.15, seed, "kl_u", j)
        a_up = Bk["kolk_lage_oben_anteil"] * l
        sk = float(A_.linie(uk, A_.uc)) + 0.5 * A_.wand + 0.8 * a_up
        if A_.art == "schnelle":
            sk = float(A_.linie(uk, A_.uc)) + A_.wand + 0.6 * a_up
        U_eh = EH[min(A_.einheit, len(EH) - 1)]["U"]
        Us ={sd: clamp(U_eh + zw(-Uf["seite_streuung_m"], Uf["seite_streuung_m"], seed, "Us", j, sd),
                        Uf["min_m"], Uf["max_m"]) for sd in ("links", "rechts")}
        prall = "links" if uk >= A_.uc else "rechts"
        becken.append({"nr": j, "typ": typ, "oben": j, "unten": j + 1, "P": A_.P_dn, "laenge_m": Lp, "B": B,
                       "kolk": {"s": sk, "u": uk, "l": l, "w": w, "a_up": a_up, "a_dn": l - a_up, "tiefe": dk},
                       "rinne": zw(*Bk["rinne_tiefe_m"], seed, "rinne", j), "rand": zw(*Bk["rand_tiefe_m"], seed, "rand", j),
                       "exp": zw(*Bk["quer_exponent"], seed, "exp", j),
                       "wf": zw(*(Bk["breite_faktor"] if typ != "teil" else [1.0, 1.1]), seed, "wf", j),
                       "U": Us, "prall": prall,
                       "r_face": {sd: zw(*R["ufer_profil"]["stufe_lauf_m"]["prall" if sd == prall else "gleit"],
                                         seed, "rf", j, sd) for sd in ("links", "rechts")}})
    return lippen, becken, uc


# ======================================================================================================================
# Raster: Bett, Ufer, Wasserspiegel
# ======================================================================================================================
def raster(ist, R, lippen, becken, uc, rand, seed, ab):
    s0, s1 = rand["s0"], rand["s1"]
    S = np.round(np.arange(s0, s1 + 1.5 + 1e-9, DS), 3)
    U = np.round(np.arange(-U_MAX, U_MAX + 1e-9, DU), 3)
    ns, nu = len(S), len(U)
    Lr, UP, Bu = R["lippe"], R["ufer_profil"], R["buchten"]
    zur = R["abschnitte"][ab].get("zuruecklegen", True)
    tanb = math.tan(math.radians(UP["boeschung_grad"]))
    UC = uc(S)
    BB = np.interp(S, ist.s, ist.Bm)
    # Linien je Lippe (je Spalte)
    LIN = np.array([L.linie(U, L.uc) for L in lippen])          # [nl, nu]
    # Becken je Zelle: letzte Lippe mit Linie <= s (Lippe j -> Becken j); hinter der letzten Lippe: Kiesbett (-1)
    pidx = np.full((ns, nu), -1, dtype=int)
    for j in range(len(lippen)):
        pidx[S[:, None] >= LIN[j][None, :]] = j
    nb = len(becken)
    # Wasserspiegel
    W = np.zeros((ns, nu))
    face_t = np.full((ns, nu), np.nan)
    for j, L in enumerate(lippen):
        m = pidx == j
        if not m.any():
            continue
        srel = (S[:, None] - LIN[j][None, :])
        t = np.clip(srel / L.wand, 0.0, 1.0)
        if L.art == "schnelle":
            wv = L.P_up - (L.P_up - L.P_dn) * t
        else:
            wv = L.P_up - (L.P_up - L.P_dn) * glatt(t)
        W[m] = wv[m]
        ft = np.where(srel < L.wand, t, np.nan)
        face_t[m] = ft[m]
    # Kanten je Zeile (Mitte, Halbbreite, Buchten)
    pc = np.array([pidx[i, int(np.argmin(np.abs(U - UC[i])))] for i in range(ns)])
    wf = np.ones(ns)
    for i in range(ns):
        p = pc[i]
        if 0 <= p < nb:
            bk = becken[p]
            d_l = min(abs(S[i] - lippen[bk["oben"]].s - lippen[bk["oben"]].wand), abs(lippen[bk["unten"]].s - S[i]))
            g = glatt(d_l / Lr["einschnuerung_laenge_m"])
            wf[i] = Lr["einschnuerung"] + (bk["wf"] - Lr["einschnuerung"]) * g
        else:
            wf[i] = 1.0
    HW = 0.5 * BB * wf
    E = {}
    for sd, sg in (("links", 1.0), ("rechts", -1.0)):
        amp = np.clip(0.2 * BB - 0.3, 0.0, 0.8)
        wl1 = zw(*Bu["wellenlaenge_m"], seed, "bucht_wl", sd)
        n = (rauschen1(S, seed + "|bucht|" + sd, wl1) + 0.5 * rauschen1(S, seed + "|bucht2|" + sd, wl1 * 0.43)) / 1.5
        bay = amp * glatt((n - 0.3) / 0.45)
        u_kante = UC + sg * HW
        frei = np.ones(ns)
        for j, L in enumerate(lippen):
            sl = np.interp(u_kante, U, LIN[j])
            dist = np.abs(S - sl)
            frei = np.minimum(frei, glatt((dist - Bu["lippe_frei_m"]) / 1.0))
        frei *= glatt((S - s0 - 1.0) / 2.0) * glatt((s1 - S) / 2.0)
        E[sd] = UC + sg * (HW + bay * frei)
    EL, ER = E["links"], E["rechts"]
    # Bett und Ufer
    ZLO = np.full((ns, nu), np.nan)
    ZHI = np.full((ns, nu), np.nan)
    WG = np.zeros((ns, nu))
    ZON = np.zeros((ns, nu), dtype=np.uint8)
    UU = np.broadcast_to(U[None, :], (ns, nu))
    SS = np.broadcast_to(S[:, None], (ns, nu))
    innen = (UU <= EL[:, None]) & (UU >= ER[:, None])
    d_out = np.where(UU > EL[:, None], UU - EL[:, None], np.where(UU < ER[:, None], ER[:, None] - UU, 0.0))
    seite_l = UU >= UC[:, None]
    ZB = np.full((ns, nu), np.nan)          # Bett (auch neben dem Bett gerechnet, fuer die Uferkante)
    for p, bk in enumerate(becken):
        m = pidx == p
        if not m.any():
            continue
        A_, N_ = lippen[bk["oben"]], lippen[bk["unten"]]
        K = bk["kolk"]
        Ss, Us = SS[m], UU[m]
        ii = np.nonzero(m)[0]
        el, er = EL[ii], ER[ii]
        # Talweg: vom Kolk zur Hauptkerbe der naechsten Lippe
        u_end = N_.uc + (N_.kerben[0][0] if N_.kerben else 0.0)
        s_end = float(N_.linie(u_end, N_.uc)) - Lr["krone_zone_m"]
        tt = np.clip((Ss - K["s"]) / max(s_end - K["s"], 0.3), 0.0, 1.0)
        ut = K["u"] + (u_end - K["u"]) * (0.5 - 0.5 * np.cos(np.pi * tt))
        ut = np.clip(ut, er + 0.3, el - 0.3)
        span = np.where(Us >= ut, np.maximum(el - ut, 0.2), np.maximum(ut - er, 0.2))
        wq = np.clip(np.abs(Us - ut) / span, 0.0, 1.0)
        dq = bk["rand"] + (bk["rinne"] - bk["rand"]) * (1.0 - wq ** bk["exp"])
        a = np.where(Ss < K["s"], K["a_up"], K["a_dn"])
        rr = ((Ss - K["s"]) / a) ** 2 + ((Us - K["u"]) / (K["w"] / 2.0)) ** 2
        g = 1.0 - glatt((np.sqrt(rr) - 0.3) / 0.7)              # Schuessel: Kern r < 0,3 voll tief, weich bis r = 1
        dk = dq + max(K["tiefe"] - bk["rinne"], 0.0) * g
        # Krone der naechsten Lippe
        s_bis = N_.linie(Us, N_.uc) - Ss
        tk = glatt(1.0 - s_bis / Lr["krone_zone_m"])
        dk = dk + (N_.krone_tiefe(Us, N_.uc) - dk) * tk
        zb = bk["P"] - dk
        # Stufenwand / Rampe der oberen Lippe
        ft = face_t[m]
        inw = ~np.isnan(ft)
        if A_.art != "bestand":
            kz = A_.P_up - A_.krone_tiefe(Us, A_.uc)
            if A_.art == "schnelle":
                wv = W[m]
                zr = wv - A_.krone_tiefe(Us, A_.uc)
                zb = np.where(inw, zr + (zb - zr) * glatt(np.nan_to_num(ft) * 1.5 - 0.5), zb)
            else:
                zb = np.where(inw, kz + (zb - kz) * glatt(np.nan_to_num(ft)), zb)
        ZB[m] = zb
    # Kiesbett hinter der letzten Lippe: flaches Rinnenprofil
    m = pidx == len(lippen) - 1
    if m.any():
        L = lippen[-1]
        wq = np.clip(np.abs(UU[m] - UC[np.nonzero(m)[0]]) / np.maximum(0.5 * BB[np.nonzero(m)[0]], 0.5), 0, 1)
        zb = L.P_dn - (0.05 + 0.25 * (1 - wq ** 2))
        kz = L.P_up - L.krone_tiefe(UU[m], L.uc)
        ft = face_t[m]
        ZB[m] = np.where(~np.isnan(ft), kz + (zb - kz) * glatt(np.nan_to_num(ft)), zb)
    # Zonen und Grenzen
    ZLO[innen] = ZB[innen]
    ZHI[innen] = ZB[innen]
    WG[innen] = 1.0
    ZON[innen] = 1
    # Ufer je Seite
    for sd in ("links", "rechts"):
        msd = (~innen) & (seite_l if sd == "links" else ~seite_l)
        Uv = np.zeros((ns, nu))
        RF = np.zeros((ns, nu))
        RD = np.zeros((ns, nu))
        for p, bk in enumerate(becken):
            mm = (pidx == p)
            Uv[mm] = bk["U"][sd]
            RF[mm] = bk["r_face"][sd]
            RD[mm] = bk["rand"]
        mm = pidx == len(lippen) - 1
        Uv[mm], RF[mm], RD[mm] = 0.3, 0.6, 0.05
        mm = pidx < 0
        Uv[mm], RF[mm], RD[mm] = 0.3, 0.6, 0.05
        N = W + Uv
        d = d_out
        f1 = msd & (d < RF)
        zf = (W - RD) + (N - W + RD) * glatt(d / np.maximum(RF, 0.1))
        ZLO[f1], ZHI[f1], WG[f1], ZON[f1] = zf[f1], zf[f1], 1.0, 5
        f2 = msd & (d >= RF) & (d < RF + UP["schulter_m"])
        ZLO[f2] = N[f2]
        if zur:
            ZHI[f2] = (N + tanb * (d - RF))[f2]
        WG[f2], ZON[f2] = 1.0, 6
        f3 = msd & (d >= RF + UP["schulter_m"]) & (d < UP["korridor_m"] + UP["uebergang_m"])
        if zur:
            ZHI[f3] = (N + tanb * (d - RF))[f3]
        WG[f3] = np.clip((UP["korridor_m"] + UP["uebergang_m"] - d[f3]) / UP["uebergang_m"], 0.0, 1.0)
        ZON[f3] = 7
    # Abtrag in Schulter und Boeschung begrenzen: nur so tief wie der neue Spiegel unter dem alten liegt (+0,3 m),
    # nach aussen bis zum Korridorrand auf 0 abnehmend - die Talflanke selbst wird nicht abgegraben
    SPALT = np.array([ist.spiegel_alt(float(s)) for s in S])
    EIN = np.maximum(SPALT[:, None] - W, 0.0)
    AMAX = np.full((ns, nu), np.nan)
    for sd in ("links", "rechts"):
        RF = np.zeros((ns, nu))
        for p, bk in enumerate(becken):
            RF[pidx == p] = bk["r_face"][sd]
        RF[(pidx < 0) | (pidx == len(lippen) - 1)] = 0.6
        msd = (~innen) & (seite_l if sd == "links" else ~seite_l) & (d_out >= RF)
        f = np.clip(1.0 - (d_out - RF) / max(UP["korridor_m"] - 0.6, 0.5), 0.0, 1.0)
        AMAX[msd] = ((EIN + UP["abtrag_zugabe_m"]) * f)[msd]
    # Zonen im Bett: Kolk, Krone, Wand
    for p, bk in enumerate(becken):
        K = bk["kolk"]
        rr = ((SS - K["s"]) / np.where(SS < K["s"], K["a_up"], K["a_dn"])) ** 2 + ((UU - K["u"]) / (K["w"] / 2.0)) ** 2
        ZON[innen & (pidx == p) & (rr < 0.6)] = 2
    for j, L in enumerate(lippen):
        if L.art == "bestand":
            continue
        dl = SS - LIN[j][None, :]
        ZON[innen & (dl > -Lr["krone_zone_m"] * 0.6) & (dl <= 0.0)] = 3
        ZON[innen & (pidx == j) & (dl > 0) & (dl < L.wand)] = 4
    # Uebergang am Kopf (unveraenderte Durchbruch-Stufe) und am Fuss (Kiesbett)
    fs = glatt((S - s0) / 1.0) * np.clip((s1 + 1.5 - S) / 1.0, 0.0, 1.0)
    WG *= fs[:, None]
    return {"S": S, "U": U, "ZLO": ZLO, "ZHI": ZHI, "WG": WG, "W": W, "AMAX": AMAX, "ZON": ZON, "ZB": ZB, "EL": EL, "ER": ER,
            "UC": UC,
            "LIN": LIN, "pidx": pidx, "BB": BB, "d_out": d_out, "innen": innen}


def anwenden(ist_z, G):
    lo = np.where(np.isnan(G["ZLO"]), -np.inf, G["ZLO"])
    hi = np.where(np.isnan(G["ZHI"]), np.inf, G["ZHI"])
    neu = ist_z + G["WG"] * (np.clip(ist_z, lo, hi) - ist_z)
    am = np.where(np.isnan(G["AMAX"]), np.inf, G["AMAX"])
    return np.maximum(neu, ist_z - am)


# ======================================================================================================================
# Instanzen (Bach-Koordinaten)
# ======================================================================================================================
def netze_lesen():
    with open(os.path.join(DATEN, "netze.csv"), encoding="utf-8") as f:
        Rn = {r["name"]: r for r in csv.DictReader(f, delimiter=";")}
    with open(os.path.join(DATEN, "netz_sperre.json"), encoding="utf-8") as f:
        sperre = set(json.load(f))
    return Rn, sperre


def palette():
    with open(GEF_REGELN, encoding="utf-8") as f:
        return json.load(f)["biome"]["tundra"]["netze"]


class Instanzen:
    def __init__(self, Rn, sperre, skala):
        self.Rn, self.sperre, self.skala = Rn, sperre, skala
        self.inst = {}
        self.fehler = []
        self.n = 0

    def netz_fuer(self, liste, groesse, key, flach_ok=True):
        ok = []
        for n in liste:
            r = self.Rn.get(n)
            if r is None or r["pfad"] in self.sperre:
                continue
            gx, gy, gz = float(r["groesse_x_m"]), float(r["groesse_y_m"]), float(r["groesse_z_m"])
            if not flach_ok and gz < self.flach * max(gx, gy):
                continue
            m = max(gx, gy, gz)
            sk = groesse / m
            if self.skala[0] <= sk <= self.skala[1]:
                ok.append((n, round(sk, 3)))
        if not ok:
            return None, None
        return ok[int(zufall(*key) * len(ok)) % len(ok)]

    def setze(self, liste, groesse, key, rolle, ebene, kollision, sicht, s, u, yaw, kipp, einb, z_plan, hind=False,
              z_abs=False, skala_fest=None):
        if skala_fest is not None:
            netz = liste[int(zufall(*key) * len(liste)) % len(liste)]
            netz = netz if netz in self.Rn and self.Rn[netz]["pfad"] not in self.sperre else None
            sk = skala_fest
        else:
            netz, sk = self.netz_fuer(liste, groesse, key,
                                      flach_ok=rolle in ("lippe", "kies") or not self.flach_nur_lippe)
        if netz is None:
            self.fehler.append("kein Netz fuer %s %.2f m" % (rolle, groesse))
            return None
        r = self.Rn[netz]
        e = self.inst.setdefault(netz + ("_kol" if kollision else ""), {"netz": netz, "pfad": r["pfad"], "rolle": rolle,
                                                                       "ebene": ebene, "kollision": kollision,
                                        "sichtweite": sicht,
                                        "groesse_m": [float(r["groesse_x_m"]), float(r["groesse_y_m"]),
                                                      float(r["groesse_z_m"])], "rollen": {}, "eintraege": []})
        e["rollen"][rolle] = e["rollen"].get(rolle, 0) + 1
        row = [r2(s), r2(u), r2(sk, 3), r2(yaw, 1), r2(kipp, 1), r2(einb), r2(groesse), r2(z_plan, 3), bool(hind), self.n,
               bool(z_abs)]
        e["eintraege"].append(row)
        self.n += 1
        return {"netz": netz, "rolle": rolle, "s": s, "u": u, "g": groesse, "hind": hind, "row": row, "kol": kollision,
                "z": z_plan, "z_abs": z_abs}


def plane_instanzen(G, lippen, becken, R, seed, Rn, sperre, z_neu):
    Bl = R["bloecke"]
    Sw = R["swr"]
    pal = dict(palette())
    # Lippenbloecke: Riegel + Bloecke + kleine Bergfelsen der Tundra-Palette (mehr Vielfalt bei 0,5-1,2 m)
    ohne = tuple(Bl.get("lippe_ohne_6e", {}).get("praefix", []))
    pal["lippe_mix"] = [n for n in dict.fromkeys(pal["riegel"] + pal["bloecke"] + Bl["zusatz_netze"] +
                                                 [n for n in pal["schutt"] if n.startswith("SM_mountain_rock_small")])
                        if not (ohne and n.startswith(ohne))]
    pal["riegel"] = list(dict.fromkeys(pal["riegel"] + Bl["zusatz_netze"]))
    pal["bloecke"] = list(dict.fromkeys(pal["bloecke"] + Bl["zusatz_netze"]))
    I = Instanzen(Rn, sperre, Bl["skala"])
    I.flach, I.flach_nur_lippe = Bl["flach_grenze"], Bl["flach_nur_lippe"]
    S, U = G["S"], G["U"]
    liste = []

    def zp(s, u):
        i = int(np.clip(round((s - S[0]) / DS), 0, len(S) - 1))
        j = int(np.clip(round((u - U[0]) / DU), 0, len(U) - 1))
        return float(z_neu[i, j])

    def kanten(s):
        i = int(np.clip(round((s - S[0]) / DS), 0, len(S) - 1))
        return float(G["EL"][i]), float(G["ER"][i]), float(G["UC"][i])

    kol = lambda g: g >= Sw["kollision_ab_m"]
    for L in lippen:
        if L.art == "bestand":
            continue
        el, er, ucc = kanten(L.s)
        D = max(L.D, 0.3)
        eb_l, eb_r = zw(*R["lippe"]["einbindung_ufer_m"], seed, "eb", L.nr, "l"), zw(*R["lippe"]["einbindung_ufer_m"],
                                                                                     seed, "eb", L.nr, "r")
        u = er - eb_r
        B_l = el - er
        g_key = clamp(min(0.7 * D + 0.3, 0.22 * B_l + 0.2), 0.5, 1.1)      # 6f: nach Breite und Fall
        g_lip = clamp(0.65 * g_key, 0.35, 0.8)
        frei = [(L.uc + ur, w / 2.0 + Bl["lippe"]["kerbe_frei_m"]) for ur, w, _ in L.kerben]
        # Keystones an den Kerbenraendern (Hauptkerbe)
        keys = []
        if L.kerben and L.D >= Bl["keystone"]["ab_fall_m"]:
            ur, w, _ = L.kerben[0]
            for sg in (-1.0, 1.0):
                g = min(g_key * zw(0.85, 1.15, seed, "keyg", L.nr, sg), 1.1)
                uk = L.uc + ur + sg * (w / 2.0 + Bl["lippe"]["kerbe_frei_m"] + 0.45 * g)
                if er - eb_r <= uk <= el + eb_l:
                    keys.append(uk)
                    sk_ = float(L.linie(uk, L.uc)) + zw(-0.1, 0.15, seed, "keys", L.nr, sg)
                    liste.append(I.setze(pal["riegel"], g, (seed, "key", L.nr, sg), "keystone", "schutt", kol(g),
                                         [0, 45000], sk_, uk, L.theta + 90.0 + zw(-15, 15, seed, "keyy", L.nr, sg),
                                         zw(5, 15, seed, "keyk", L.nr, sg), zw(*Bl["keystone"]["einbettung"], seed, "keye",
                                                                                L.nr, sg), zp(sk_, uk)))
        n = 0
        while u <= el + eb_l:
            g = g_lip * (1.0 + Bl["lippe"]["streuung"] * (2 * zufall(seed, "lg", L.nr, n) - 1))
            if L.art == "schnelle":
                g *= 0.7
            g = max(g, 0.35)
            uz = u + 0.5 * g
            ok = all(abs(uz - a) > b + 0.4 * g for a, b in frei) and all(abs(uz - k) > 0.75 * g_key for k in keys)
            if ok and (L.art != "schnelle" or zufall(seed, "lsch", L.nr, n) < 0.6 or uz > el or uz < er):
                sk_ = float(L.linie(uz, L.uc)) + zw(-0.1, 0.15, seed, "ls", L.nr, n)
                liste.append(I.setze(pal["lippe_mix"], g, (seed, "lip", L.nr, n), "lippe", "schutt", kol(g), [0, 45000],
                                     sk_, uz, L.theta + 90.0 + zw(-20, 20, seed, "ly", L.nr, n),
                                     zw(0, 12, seed, "lk", L.nr, n), zw(*Bl["lippe"]["einbettung"], seed, "le", L.nr, n),
                                     zp(sk_, uz)))
            u += Bl["lippe"]["abstand_faktor"] * g + 0.25 * g
            n += 1
        # Eckbloecke an beiden Lippenenden
        if L.art in ("stufe", "kaskade_teil", "ende"):
            for sd, ue, sg in (("l", el, 1.0), ("r", er, -1.0)):
                p_eck = Bl["eckblock"]["anteil"] if L.teil == 0 else Bl["eckblock"]["anteil_teilstufe"]
                if zufall(seed, "eck", L.nr, sd) < p_eck:
                    g = clamp((0.18 * B_l + 0.35 * D + 0.2) * zw(0.85, 1.15, seed, "eg", L.nr, sd), 0.6, 1.3)
                    uu = ue + sg * (zw(*Bl["eckblock"]["aussen_m"], seed, "ea", L.nr, sd) + 0.35 * g)
                    ss = float(L.linie(ue, L.uc)) + zw(*Bl["eckblock"]["stromab_m"], seed, "es", L.nr, sd)
                    liste.append(I.setze(pal["bloecke"], g, (seed, "eck", L.nr, sd), "eckblock", "schutt", kol(g),
                                         [0, 45000], ss, uu, zw(-40, 40, seed, "ey", L.nr, sd),
                                         zw(0, 10, seed, "ek", L.nr, sd), zw(*Bl["eckblock"]["einbettung"], seed, "ee",
                                                                             L.nr, sd), zp(ss, uu)))
    for bk in becken:
        if bk["typ"] == "anschluss":
            pass
        A_, N_ = lippen[bk["oben"]], lippen[bk["unten"]]
        sa, sb = A_.s + A_.wand + 1.0, N_.s - 1.0
        # Randbloecke
        for sd, sg in (("links", 1.0), ("rechts", -1.0)):
            s = sa + zw(0.0, 2.0, seed, "rb0", bk["nr"], sd)
            n = 0
            while s < sb:
                if zufall(seed, "rb", bk["nr"], sd, n) < Bl["randblock"]["anteil"]:
                    el, er, _ = kanten(s)
                    g = zw(*Bl["randblock"]["groesse_m"], seed, "rbg", bk["nr"], sd, n)
                    uu = (el if sg > 0 else er) + sg * (zw(*Bl["randblock"]["aussen_m"], seed, "rba", bk["nr"], sd, n)
                                                       + 0.3 * g)
                    liste.append(I.setze(pal["bloecke"], g, (seed, "rand", bk["nr"], sd, n), "randblock", "schutt",
                                         kol(g), [0, 45000], s, uu, zw(-20, 20, seed, "rby", bk["nr"], sd, n),
                                         zw(0, 10, seed, "rbk", bk["nr"], sd, n),
                                         zw(*Bl["randblock"]["einbettung"], seed, "rbe", bk["nr"], sd, n), zp(s, uu)))
                s += zw(*Bl["randblock"]["abstand_m"], seed, "rbs", bk["nr"], sd, n)
                n += 1
        # Beckenbloecke (nicht im Strahl, nicht im Kolkkern)
        K = bk["kolk"]
        if bk["typ"] in ("haupt", "lauf") and bk["laenge_m"] >= 4.0:
            nbl = int(zw(*Bl["beckenblock"]["je_10m_becken"], seed, "bbn", bk["nr"]) * bk["laenge_m"] / 10.0 +
                      zufall(seed, "bbr", bk["nr"]))
            for n in range(nbl):
                for v in range(6):
                    s = zw(sa, sb, seed, "bbs", bk["nr"], n, v)
                    el, er, ucc = kanten(s)
                    g = zw(*Bl["beckenblock"]["groesse_m"], seed, "bbg", bk["nr"], n, v)
                    uu = zw(er + 0.4 * g, el - 0.4 * g, seed, "bbu", bk["nr"], n, v)
                    rr = ((s - K["s"]) / (K["a_up"] if s < K["s"] else K["a_dn"])) ** 2 + ((uu - K["u"]) / (K["w"] / 2)) ** 2
                    if rr > 1.0 and abs(uu - K["u"]) > Bl["beckenblock"]["strahl_frei_m"] + g / 2.0 and \
                            min(abs(s - A_.s), abs(N_.s - s)) > 1.0:
                        liste.append(I.setze(pal["bloecke"], g, (seed, "bb", bk["nr"], n), "beckenblock", "schutt",
                                             kol(g), [0, 45000], s, uu, zw(-20, 20, seed, "bby", bk["nr"], n),
                                             zw(10, 20, seed, "bbk", bk["nr"], n),
                                             zw(*Bl["beckenblock"]["einbettung"], seed, "bbe", bk["nr"], n), zp(s, uu),
                                             hind=True))
                        break
        # Kies im Kolk (Faecher stromab des tiefsten Punkts)
        if bk["typ"] in ("haupt", "anschluss", "teil"):
            nk = int(round(zw(*Bl["kies_kolk"]["anzahl"], seed, "kn", bk["nr"]) * (0.5 if bk["typ"] == "teil" else 1)))
            for n in range(nk):
                s = K["s"] + zw(0.2, 1.0, seed, "kss", bk["nr"], n) * K["a_dn"]
                uu = K["u"] + zw(-0.5, 0.5, seed, "ksu", bk["nr"], n) * K["w"]
                liste.append(I.setze(pal["kies"], zw(0.15, 0.3, seed, "ksg", bk["nr"], n), (seed, "kies", bk["nr"], n),
                                     "kies", "kleinzeug", False, [0, 3500], s, uu, zw(-180, 180, seed, "ksy", bk["nr"], n),
                                     0.0, 0.3, zp(s, uu)))
    liste = [x for x in liste if x]
    # SWR-Hindernisse nach dem N5-Filter (Rolle, Groesse, Wassernaehe, Teil der Breite, je Meter)
    je_m = {}
    for x in liste:
        if not x["hind"]:
            continue
        el, er, _ = kanten(x["s"])
        B = el - er
        ok = x["rolle"] not in Sw["rollen_nie"] and x["g"] >= Sw["hindernis_min_m"] and x["g"] <= Sw["anteil_breite_max"] * B
        m = int(math.floor(x["s"]))
        if ok and je_m.get(m, 0.0) + x["g"] > Sw["anteil_je_m_max"] * B:
            ok = False
        if ok:
            je_m[m] = je_m.get(m, 0.0) + x["g"]
        x["hind"] = ok
        x["row"][8] = ok
    return I, liste


def plane_ausstattung(G, lippen, becken, R, seed, I, Rn):
    """16h Nachtrag 6e: Kantengras, Moos am Ufer, Farne (Kandidaten, Nordufer filtert das Weltwerkzeug), Totholz quer."""
    A = R["ausstattung_6e"]
    S, U, W = G["S"], G["U"], G["W"]
    out = []

    def zeile(s):
        return int(np.clip(round((s - S[0]) / DS), 0, len(S) - 1))

    def becken_bei(s):
        i = zeile(s)
        j = int(np.argmin(np.abs(U - G["UC"][i])))
        p = int(G["pidx"][i, j])
        return becken[p] if 0 <= p < len(becken) else None

    def nahe_lippe(s, d):
        return any(abs(s - L.s) < d for L in lippen if L.art != "bestand")

    s0, s1 = float(S[0]) + 1.0, lippen[-1].s - 0.5
    akt = A.get("aktiv_20", {})
    for sd, sg in (("links", 1.0), ("rechts", -1.0)) if any(akt.get(k, True) for k in ("kantengras", "moos_ufer", "farne")) \
            else ():
        E_ = G["EL"] if sg > 0 else G["ER"]
        # Kantengras: Fuss auf der Schulter (Spiegel + Uferstufe), haengt 0,15-0,35 m ueber die Uferstufe
        K = A["kantengras"]
        s, n = s0, 0
        while s < s1:
            bk = becken_bei(s)
            if bk and not nahe_lippe(s, K["lippe_frei_m"]) and zufall(seed, "kg_p", sd, n) < zw(*K["anteil_kantenlaenge"], seed, "kg_a", sd):
                i = zeile(s)
                rf = bk["r_face"][sd]
                u = float(E_[i]) + sg * (rf - zw(*K["ueberhang_m"], seed, "kg_u", sd, n))
                j = int(np.clip(round((u - U[0]) / DU), 0, len(U) - 1))
                if int(G["pidx"][i, j]) != bk["nr"] or abs(float(W[i, j]) - bk["P"]) > 0.01:
                    s += zw(*K["abstand_m"], seed, "kg_d", sd, n)
                    n += 1
                    continue                   # Stufenwand einer schraegen Lippe: dort kein Kantengras
                z = bk["P"] + bk["U"][sd] - 0.02
                out.append(I.setze(K["netze"], 0.0, (seed, "kg_n", sd, n), "kantengras", "bewuchs", False, [0, 9000], s, u,
                                   -sg * 90.0 + zw(-25, 25, seed, "kg_y", sd, n), zw(*K["neigung_zum_wasser_grad"], seed, "kg_k", sd, n),
                                   0.02, z, z_abs=True, skala_fest=zw(*K["skala"], seed, "kg_s", sd, n)))
            s += zw(*K["abstand_m"], seed, "kg_d", sd, n)
            n += 1
        # Moos an Uferstufe und Schulter (0,05-1,2 m ueber dem Spiegel)
        M = A["moos_ufer"]
        s, n = s0, 0
        while s < s1:
            bk = becken_bei(s)
            if bk and zufall(seed, "mo_p", sd, n) < zw(*M["je_m_ufer"], seed, "mo_a", sd, n) * 2.0:
                i = zeile(s)
                for k in range(int(zw(M["gruppe"][0], M["gruppe"][1] + 0.99, seed, "mo_g", sd, n))):
                    d = zw(0.05, bk["r_face"][sd] + 0.6, seed, "mo_d", sd, n, k)
                    ss = s + zw(-0.6, 0.6, seed, "mo_s", sd, n, k)
                    out.append(I.setze(M["netze"], 0.0, (seed, "mo_n", sd, n, k), "moos", "kontakt", False, [0, 12000],
                                       ss, float(E_[zeile(ss)]) + sg * d, zw(-180, 180, seed, "mo_y", sd, n, k), 0.0, 0.0,
                                       0.0, skala_fest=zw(0.8, 1.4, seed, "mo_k", sd, n, k)))
            s += 2.0
            n += 1
        # Farne (Kandidaten; das Weltwerkzeug behaelt nur das Nordufer = Boeschung schaut nach Norden)
        Fa = A["farne"]
        s, n = s0 + zw(0, 4, seed, "fa0", sd), 0
        while s < s1:
            bk = becken_bei(s)
            if bk:
                for k in range(int(zw(Fa["gruppe"][0], Fa["gruppe"][1] + 0.99, seed, "fa_g", sd, n))):
                    ss = s + zw(-1.0, 1.0, seed, "fa_s", sd, n, k)
                    d = bk["r_face"][sd] + R["ufer_profil"]["schulter_m"] * 0.3 + zw(*Fa["d_hinter_schulter_m"], seed, "fa_d", sd, n, k)
                    out.append(I.setze(Fa["netze"], 0.0, (seed, "fa_n", sd, n, k), "farn", "bewuchs", False, [0, 25000], ss,
                                       float(E_[zeile(ss)]) + sg * d, zw(-180, 180, seed, "fa_y", sd, n, k), 0.0, 0.03, 0.0,
                                       skala_fest=zw(*Fa["skala"], seed, "fa_k", sd, n, k)))
            s += zw(*Fa["abstand_gruppen_m"], seed, "fa_a", sd, n)
            n += 1
    # Totholz: quer ueber ein Hauptbecken (auf beiden Schultern) oder schraeg am Lippenende (auf dem Eckblock)
    T = A["totholz"]
    s, n = s0 + zw(5, 15, seed, "th0"), 0
    haupt = [b for b in becken if b["typ"] == "haupt" and b["laenge_m"] >= 4.5]
    while s < s1 and haupt:
        bk = min(haupt, key=lambda b: abs((lippen[b["oben"]].s + lippen[b["unten"]].s) / 2 - s))
        A_, N_ = lippen[bk["oben"]], lippen[bk["unten"]]
        quer = zufall(seed, "th_art", n) < T["arten"]["quer_ueber_becken"]
        if quer:
            sm = A_.s + A_.wand + zw(0.45, 0.65, seed, "th_s", n) * bk["laenge_m"]
            i = zeile(sm)
            breite = float(G["EL"][i] - G["ER"][i]) + bk["r_face"]["links"] + bk["r_face"]["rechts"]
            ziel = breite * zw(*T["laenge_ueber_breite"], seed, "th_l", n)
            um = float(G["UC"][i])
            # Laengsausdehnung des schraeg liegenden Stamms bleibt im Becken (0,5 m Abstand zu beiden Lippen)
            frei = min(sm - (A_.s + A_.wand), N_.s - sm) - 0.5
            dw = math.degrees(math.asin(clamp(frei / max(ziel / 2.0, 0.1), 0.0, 1.0)))
            yaw = 90.0 + clamp(zw(-20, 20, seed, "th_y", n), -dw, dw)
            z = bk["P"] + min(bk["U"].values()) + zw(*T["auflage_ueber_spiegel_m"], seed, "th_z", n)
        else:
            sg = 1.0 if zufall(seed, "th_sd", n) < 0.5 else -1.0
            sm = N_.s - zw(0.3, 0.8, seed, "th_s", n)
            i = zeile(sm)
            um = float(G["EL"][i] if sg > 0 else G["ER"][i]) - sg * zw(0.2, 0.6, seed, "th_u", n)
            ziel = zw(2.0, 3.5, seed, "th_l", n)
            yaw = sg * zw(30, 60, seed, "th_y", n)
            z = N_.P_up + zw(*T["auflage_ueber_spiegel_m"], seed, "th_z", n)
        kand = []
        for nm in T["netze"]:
            r = Rn.get(nm)
            if r is None:
                continue
            Lm = max(float(r["groesse_x_m"]), float(r["groesse_y_m"]))
            sk = ziel / Lm
            if T["skala"][0] <= sk <= T["skala"][1]:
                kand.append((nm, sk, float(r["groesse_y_m"]) > float(r["groesse_x_m"])))
        if kand:
            nm, sk, y_lang = kand[int(zufall(seed, "th_n", n) * len(kand)) % len(kand)]
            out.append(I.setze([nm], ziel, (seed, "th_k", n), "totholz", "schutt", True, [0, 45000], sm, um,
                               yaw + (90.0 if y_lang else 0.0), zw(0, 6, seed, "th_k2", n), 0.0, z, z_abs=True,
                               skala_fest=round(sk, 3)))
        s += zw(*T["abstand_m"], seed, "th_d", n)
        n += 1
    return [x for x in out if x]


# ======================================================================================================================
# Pruefung und Kennzahlen
# ======================================================================================================================
def cv(a):
    a = np.asarray(a, dtype=float)
    return float(a.std() / a.mean()) if len(a) > 1 and a.mean() > 0 else 0.0


def pruefen(EH, lippen, becken, G, z_neu, ist_z, I, liste, R, rand, ist):
    P = R["pruefung"]
    F, Wn = [], []
    S, U, W = G["S"], G["U"], G["W"]
    j0 = int(np.argmin(np.abs(U)))
    # 1 Spiegel faellt nie (je Spalte im Bett)
    for j in range(len(U)):
        col = W[:, j]
        if np.any(np.diff(col) > 1e-6):
            F.append("Spiegel steigt in Spalte u %.2f" % U[j])
            break
    # 2 Anschluesse
    i1 = int(round((rand["s0"] + 1.0 - S[0]) / DS))
    if abs(W[i1, j0] - rand["P0"]) > 0.01:
        F.append("Kopf: Spiegel %.3f statt %.3f" % (W[i1, j0], rand["P0"]))
    ie = int(round((rand["s1"] - 1.0 - S[0]) / DS))
    if abs(W[ie, j0] - rand["P_end"]) > 0.01:
        F.append("Fuss: Spiegel %.3f statt %.3f" % (W[ie, j0], rand["P_end"]))
    if abs(W[-1, j0] - rand["P_nach"]) > 0.01:
        F.append("Kiesbett: Spiegel %.3f statt %.3f" % (W[-1, j0], rand["P_nach"]))
    # 3 Linien schneiden sich nicht
    LIN = G["LIN"]
    for j in range(1, len(lippen)):
        if np.any(LIN[j] - LIN[j - 1] < lippen[j - 1].wand + 0.3):
            F.append("Lippen %d/%d schneiden sich" % (j - 1, j))
    # 4 Abstaende, Faelle, Seitenwechsel
    haupt = [e for e in EH[1:]]
    LB = [(e["b"] - e["a"]) / ist.breite(e["a"]) for e in haupt]
    for e, x in zip(haupt, LB):
        if not (P["laenge_B"][0] - 0.05 <= x <= P["laenge_B"][1] + 0.05):
            (Wn if e.get("final") else F).append("Einheit %d: L = %.2f B" % (e["k"], x))
    abst = [e["b"] - e["a"] for e in haupt if not e.get("final")]
    if cv(abst) < P["cv_abstand_min"]:
        F.append("Abstaende zu gleichmaessig: CV %.2f" % cv(abst))
    falle = [L.D for L in lippen if L.art not in ("bestand",)]
    if cv(falle) < P["cv_fall_min"]:
        F.append("Fallhoehen zu gleichmaessig: CV %.2f" % cv(falle))
    hl = [L for L in lippen if L.art not in ("bestand",)]
    la = np.diff([L.s for L in hl])
    if cv(la) < P["cv_lippen_abstand_min"]:
        F.append("Lippenabstaende zu gleichmaessig: CV %.2f" % cv(la))
    wechsel = sum(1 for a, b in zip(hl, hl[1:]) if a.seite != b.seite) / max(len(hl) - 1, 1)
    if wechsel < P["seitenwechsel_min"]:
        F.append("Seitenwechsel nur %.0f %%" % (100 * wechsel))
    nruhig = sum(1 for e in haupt if e["klasse"] == "ruhig")
    if nruhig < P["ruhig_min"]:
        Wn.append("nur %d ruhige Strecken" % nruhig)
    # 5 Becken: Kolktiefe, Streckung, Rinne
    tiefen = {}
    for p, bk in enumerate(becken):
        m = (G["pidx"] == p) & G["innen"]
        if not m.any():
            continue
        dmax = float((bk["P"] - G["ZB"])[m].max())
        tiefen[p] = dmax
        if bk["typ"] in ("haupt", "anschluss"):
            if not (P["kolk_tiefe_m"][0] - 0.01 <= dmax <= P["kolk_tiefe_m"][1] + 0.01):
                F.append("Becken %d (%s): Kolktiefe %.2f m" % (p, bk["typ"], dmax))
            if bk["typ"] == "haupt" and bk["laenge_m"] < R["stufe"]["hauptbecken_min_B"] * bk["B"] - 0.05:
                Wn.append("Becken %d: Hauptbecken nur %.1f m" % (p, bk["laenge_m"]))
            if bk["kolk"]["l"] < 1.3 * bk["kolk"]["w"] - 1e-6:
                F.append("Becken %d: Kolk nicht laenglich" % p)
    for L in lippen:
        if L.art in ("bestand",) or not L.kerben:
            continue
        if not (P["rinne_tiefe_m"][0] - 1e-6 <= L.kerben[0][2] <= P["rinne_tiefe_m"][1] + 1e-6):
            F.append("Lippe %d: Rinne %.2f m" % (L.nr, L.kerben[0][2]))
    # 6 Uferstufe: Schulter liegt mindestens 0,2 m ueber dem Spiegel
    sch = (G["ZON"] == 6) & (G["WG"] >= 0.999)
    if sch.any():
        um = float((z_neu - W)[sch].min())
        if um < P["uferstufe_min_m"] - 0.005:
            F.append("Uferstufe nur %.2f m" % um)
    # Aufschuettung ueber die alte Narbe (je Becken und Seite)
    auf = []
    for p, bk in enumerate(becken):
        A_, N_ = lippen[bk["oben"]], lippen[bk["unten"]]
        for sd in ("links", "rechts"):
            for s in np.arange(A_.s + A_.wand, N_.s, 1.0):
                need = bk["P"] + bk["U"][sd] - ist.narbe_seite(float(s), sd)
                auf.append(need)
    auf = np.array(auf) if auf else np.zeros(1)
    if auf.max() > R["uferstufe"]["aufschuettung_max_m"] + 0.01:
        Wn.append("Schulter muss bis %.2f m ueber die alte Narbe angehoben werden" % auf.max())
    # 7 2-m-Band neben dem Bett ueber dem Spiegel (geometrisch, mit angenommenem Ist im alten Bett)
    band = (~G["innen"]) & (G["d_out"] > R["swr"]["band_ab_m"]) & (G["d_out"] <= R["swr"]["band_m"]) & (G["WG"] > 0.5)
    nass = float(((z_neu < W) & band).sum()) / max(int(band.sum()), 1)
    if nass > R["swr"]["band_nass_max"]:
        F.append("2-m-Band zu %.1f %% unter dem Spiegel" % (100 * nass))
    # 8 Instanzen
    F += I.fehler
    for x in liste:
        if x["rolle"] in ("lippe", "eckblock", "randblock", "beckenblock"):
            for L in lippen:
                if L.art == "bestand" or not L.kerben:
                    continue
                ur, w, _ = L.kerben[0]
                sl = float(L.linie(x["u"], L.uc))
                if abs(x["s"] - sl) <= 0.75 and abs(x["u"] - (L.uc + ur)) < w / 2.0:
                    F.append("%s %s im Hauptstrahl der Lippe %d (s %.1f)" % (x["rolle"], x["netz"], L.nr, x["s"]))
        if x["hind"] and x["rolle"] in R["swr"]["rollen_nie"]:
            F.append("SWR-Hindernis mit Rolle %s" % x["rolle"])
        if x["kol"] != (x["g"] >= R["swr"]["kollision_ab_m"]) and x["rolle"] != "kies":
            F.append("Kollision falsch: %s %.2f m" % (x["netz"], x["g"]))
    for x in liste:
        if x["rolle"] in ("kantengras", "totholz"):
            i = int(np.clip(round((x["s"] - S[0]) / DS), 0, len(S) - 1))
            j = int(np.clip(round((x["u"] - U[0]) / DU), 0, len(U) - 1))
            if x["z"] < W[i, j] + 0.15:
                F.append("%s bei s %.1f liegt nur %.2f m ueber dem Spiegel" % (x["rolle"], x["s"], x["z"] - W[i, j]))
        if x["rolle"] == "totholz":
            for L in lippen:
                if L.art == "bestand" or not L.kerben:
                    continue
                if abs(x["s"] - float(L.linie(x["u"], L.uc))) < 0.3 and abs(x["u"] - (L.uc + L.kerben[0][0])) < 1.0:
                    F.append("Totholz im Hauptstrahl der Lippe %d" % L.nr)
    return F, Wn, {"band_nass": nass, "aufschuettung_max_m": float(auf.max()), "kolktiefen": tiefen,
                   "seitenwechsel": wechsel, "cv_abstand": cv(abst), "cv_lippen_abstand": cv(la),
                   "lippen_abstand": [float(la.min()), float(np.median(la)), float(la.max())], "cv_fall": cv(falle), "ruhig": nruhig}


# ======================================================================================================================
# Hauptlauf
# ======================================================================================================================
def rechne(ab="talkaskade", seed=None):
    with open(REGELN, encoding="utf-8") as f:
        R = json.load(f)
    with open(QUER, encoding="utf-8") as f:
        Q = json.load(f)["querschnitte"]
    seed = seed or "p2_bett|%s|%s" % (ab, R["stand"])
    ist = Ist(Q, R)
    EH, rand = plane_einheiten(ist, R, ab, seed)
    lippen, becken, uc = baue_lippen_becken(EH, ist, R, rand, seed)
    G = raster(ist, R, lippen, becken, uc, rand, seed, ab)
    ist_z = ist.ist_raster(G["S"], G["U"])
    z_neu = anwenden(ist_z, G)
    Rn, sperre = netze_lesen()
    I, liste = plane_instanzen(G, lippen, becken, R, seed, Rn, sperre, z_neu)
    liste += plane_ausstattung(G, lippen, becken, R, seed, I, Rn)
    F, Wn, K = pruefen(EH, lippen, becken, G, z_neu, ist_z, I, liste, R, rand, ist)
    return {"R": R, "ist": ist, "EH": EH, "rand": rand, "lippen": lippen, "becken": becken, "G": G, "ist_z": ist_z,
            "z_neu": z_neu, "I": I, "liste": liste, "F": F, "Wn": Wn, "K": K, "ab": ab, "seed": seed}


def kennzahlen(X):
    ist, EH, lippen, becken, G, K = X["ist"], X["EH"], X["lippen"], X["becken"], X["G"], X["K"]
    eh = EH[1:]
    L_m = [e["b"] - e["a"] for e in eh]
    L_B = [(e["b"] - e["a"]) / ist.breite(e["a"]) for e in eh]
    gepl = [L for L in lippen if L.art != "bestand"]
    dz = X["z_neu"] - X["ist_z"]
    zelle = DS * DU
    haupt_t = [K["kolktiefen"][p] for p, b in enumerate(becken) if b["typ"] in ("haupt", "anschluss") and p in K["kolktiefen"]]
    sch = (G["ZON"] == 6) & (G["WG"] >= 0.999)
    ust = (X["z_neu"] - G["W"])[sch]
    return {
        "alt": {"quelle": "Ferat, 16h Nachtrag 6c (lauf_p2.json)", "stufen": 26, "abstand_m": "3-4",
                "fall_m": [0.68, 3.74], "becken": "3-4 m lang, ~4 m breit (rund), Tiefe am Fuss 0,76-1,20 m, vor der Lippe "
                                                  "0,36-0,71 m; alle mit Brush 'Kasten-U'",
                "ufer_0_5m_ueber_spiegel_median_m": 0.16},
        "neu": {
            "einheiten": len(eh), "klassen": {k: sum(1 for e in eh if e["klasse"] == k) for k in
                                              ("kurz", "mittel", "lang", "ruhig")},
            "lippen": len(gepl), "lippen_je_art": {a: sum(1 for L in gepl if L.art == a) for a in
                                                   ("stufe", "kaskade_teil", "schnelle", "ende")},
            "einheit_laenge_m": [r2(min(L_m)), r2(float(np.median(L_m))), r2(max(L_m))],
            "einheit_laenge_B": [r2(min(L_B)), r2(float(np.median(L_B))), r2(max(L_B))],
            "cv_abstand_einheiten": r2(K["cv_abstand"]), "cv_lippen_abstand": r2(K["cv_lippen_abstand"]),
            "lippen_abstand_m": [r2(x) for x in K["lippen_abstand"]], "cv_fall": r2(K["cv_fall"]),
            "fall_m": [r2(min(L.D for L in gepl)), r2(float(np.median([L.D for L in gepl]))), r2(max(L.D for L in gepl))],
            "einheit_fall_m": [r2(min(e["D"] for e in eh)), r2(max(e["D"] for e in eh))],
            "kolktiefe_haupt_m": [r2(min(haupt_t)), r2(float(np.median(haupt_t))), r2(max(haupt_t))],
            "kolk_streckung_haupt": [r2(min(b["kolk"]["l"] / b["kolk"]["w"] for b in becken if b["typ"] == "haupt")),
                                     r2(float(np.median([b["kolk"]["l"] / b["kolk"]["w"] for b in becken if b["typ"] == "haupt"]))),
                                     r2(max(b["kolk"]["l"] / b["kolk"]["w"] for b in becken if b["typ"] == "haupt"))],
            "kolk_laenge_haupt_m": [r2(min(b["kolk"]["l"] for b in becken if b["typ"] == "haupt")),
                                    r2(float(np.median([b["kolk"]["l"] for b in becken if b["typ"] == "haupt"]))),
                                    r2(max(b["kolk"]["l"] for b in becken if b["typ"] == "haupt"))],
            "becken_laenge_haupt_m": [r2(min(b["laenge_m"] for b in becken if b["typ"] == "haupt")),
                                      r2(float(np.median([b["laenge_m"] for b in becken if b["typ"] == "haupt"]))),
                                      r2(max(b["laenge_m"] for b in becken if b["typ"] == "haupt"))],
            "seitenwechsel_anteil": r2(K["seitenwechsel"]),
            "lippen_winkel_grad": [r2(min(abs(L.theta) for L in gepl), 1), r2(float(np.median([abs(L.theta) for L in gepl])), 1),
                                   r2(max(abs(L.theta) for L in gepl), 1)],
            "uferstufe_schulter_m": [r2(ust.min()), r2(float(np.median(ust))), r2(np.percentile(ust, 90))] if ust.size else None,
            "kopf_ufer_m": [r2(min(e["kopf_m"] for e in eh)), r2(float(np.median([e["kopf_m"] for e in eh]))),
                            r2(max(e["kopf_m"] for e in eh))],
            "tiefe_bett_m": {"median": r2(float(np.median((G["W"] - X["z_neu"])[G["innen"]]))),
                             "p90": r2(float(np.percentile((G["W"] - X["z_neu"])[G["innen"]], 90))),
                             "hinweis": "alle Bettzellen; die Kolke sind nur ein kleiner Teil der Bettflaeche. Fuer 0,8-1,2 m "
                                        "die tiefste Stelle je Hauptbecken messen (kolktiefe_haupt_m)"},
            "band_2m_unter_spiegel_anteil": r2(K["band_nass"], 3),
            "aufschuettung_ueber_alter_narbe_max_m": r2(K["aufschuettung_max_m"]),
            "abtrag_m3_geschaetzt": r2(float(-dz[dz < 0].sum() * zelle), 0),
            "auftrag_m3_geschaetzt": r2(float(dz[dz > 0].sum() * zelle), 0),
            "delta_m": [r2(dz.min()), r2(dz.max())],
            "instanzen": X["I"].n,
            "instanzen_je_rolle": {r: sum(1 for x in X["liste"] if x["rolle"] == r) for r in
                                   ("lippe", "keystone", "eckblock", "randblock", "beckenblock", "kies", "kantengras", "moos",
                                    "farn", "totholz")},
            "kollision": sum(1 for x in X["liste"] if x["kol"]),
            "swr_hindernisse": sum(1 for x in X["liste"] if x["hind"]),
        }}


def netze_masse():
    pf = os.path.join(DATEN, "netze_masse.json")
    if not os.path.exists(pf):
        return {}
    with open(pf, encoding="utf-8") as f:
        return json.load(f)


def spline_stufenpunkte(X):
    """16h N6f: Spline-Punkte fuer die SWR: je Lippe Lippe (Spiegel oben) und Fuss (Spiegel unten) auf u = 0, dazwischen
    alle 1 m, kein Punkt naeher als 0,25 m an einem anderen. Punkttyp linear."""
    G, Sp = X["G"], X["R"]["spline_6f"]
    S, U, W = G["S"], G["U"], G["W"]
    j0 = int(np.argmin(np.abs(U)))
    fest = []
    for L in X["lippen"]:
        s_l = float(L.linie(0.0, L.uc))
        fest.append((s_l - 0.02, L.P_up))
        fest.append((s_l + L.wand + 0.02, L.P_dn))
    pts = list(fest)
    for s in np.arange(math.ceil(S[0]), math.floor(S[-1]) + 1e-9, Sp["abstand_m"]):
        if all(abs(s - a) >= Sp["min_abstand_m"] for a, _ in fest):
            pts.append((float(s), float(np.interp(s, S, W[:, j0]))))
    pts.sort()
    out = []
    for s, z in pts:
        if out and s - out[-1][0] < 0.05:
            continue
        out.append([r2(s, 2), r2(z, 3)])
    return out


def effekte_vorschlag(X):
    """16h N6b (c): nur Vorschlag, Ferat entscheidet (\"warte mit Wasserfaellen\"). Namen aus inventar_extra.json."""
    out = []
    beste = {}
    for L in X["lippen"]:
        if L.art in ("bestand", "schnelle") or L.D < 1.0:
            continue
        if L.einheit not in beste or L.D > beste[L.einheit].D:
            beste[L.einheit] = L
    for L in sorted(beste.values(), key=lambda x: x.nr):
        ur = L.kerben[0][0] if L.kerben else 0.0
        e = {"lippe": L.nr, "fall_m": r2(L.D), "s_m": r2(float(L.linie(L.uc + ur, L.uc)) + L.wand + 0.3),
             "u_m": r2(L.uc + ur), "z_m": r2(L.P_dn + 0.05, 3), "asset": "/Game/NatureWaterFX/FX/NS_Impact_Small"}
        out.append(e)
        if L.D >= 1.8:
            out.append({"lippe": L.nr, "fall_m": r2(L.D), "s_m": r2(float(L.linie(L.uc + ur, L.uc)) + 0.1),
                        "u_m": r2(L.uc + ur), "z_m": r2(L.P_up + 0.05, 3), "asset": "/Game/NatureWaterFX/FX/NS_Waterfall_Small"})
    return {"hinweis": "Nur Vorschlag zu 16h Nachtrag 6b (c), noch nicht setzen: je Einheit an der hoechsten Stufe ab 1 m "
                       "freiem Fall NS_Impact_Small am Fuss unter der Hauptkerbe, ab 1,8 m zusaetzlich NS_Waterfall_Small an der Lippe; Cull 30-45 m und "
                       "hoechstens 6 aktive Systeme je Standort wie Antwort 14.", "liste": out,
            "anzahl": {"NS_Impact_Small": sum(1 for e in out if e["asset"].endswith("Impact_Small")),
                       "NS_Waterfall_Small": sum(1 for e in out if e["asset"].endswith("Waterfall_Small"))}}


def schreiben(X, aus):
    G, ab = X["G"], X["ab"]
    os.makedirs(aus, exist_ok=True)
    kante = np.where(G["innen"], 0.0, G["d_out"])
    arr = np.stack([G["ZLO"], G["ZHI"], G["WG"], G["W"], G["AMAX"], kante]).astype("<f4")
    fn = "%s_soll.f32" % ab
    arr.tofile(os.path.join(aus, fn))
    G["ZON"].astype(np.uint8).tofile(os.path.join(aus, "%s_zonen.u8" % ab))
    S, U, W = G["S"], G["U"], G["W"]
    j0 = int(np.argmin(np.abs(U)))
    rand = X["rand"]
    sj = np.arange(math.ceil(rand["s0"]), math.floor(rand["s1"] + 1) + 1, 1.0)
    spm = [[r2(s, 1), r2(float(np.interp(s, S, W[:, j0])), 3)] for s in sj]
    lip_out = []
    for L in X["lippen"]:
        lip_out.append({"nr": L.nr, "art": L.art, "einheit": L.einheit, "teil": L.teil, "s_m": r2(L.s),
                        "s_bei_u0_m": r2(float(L.linie(0.0, L.uc))), "spiegel_oben_m": r2(L.P_up, 3),
                        "spiegel_unten_m": r2(L.P_dn, 3), "fall_m": r2(L.D), "wand_m": r2(L.wand),
                        "winkel_grad": r2(L.theta, 1), "pfeil_m": r2(L.pfeil), "mitte_u_m": r2(L.uc),
                        "breite_m": r2(L.Bl), "kerben": [{"u_m": r2(L.uc + a), "breite_m": r2(b), "tiefe_m": r2(c)}
                                                         for a, b, c in L.kerben],
                        "krone_unter_spiegel_m": r2(L.krone)})
    bk_out = []
    for b in X["becken"]:
        K = b["kolk"]
        bk_out.append({"nr": b["nr"], "typ": b["typ"], "lippe_oben": b["oben"], "lippe_unten": b["unten"],
                       "spiegel_m": r2(b["P"], 3), "laenge_m": r2(b["laenge_m"]), "breite_faktor": r2(b["wf"]),
                       "kolk": {"s_m": r2(K["s"]), "u_m": r2(K["u"]), "laenge_m": r2(K["l"]), "breite_m": r2(K["w"]),
                                "tiefe_m": r2(K["tiefe"]), "tiefste_gemessen_m": r2(X["K"]["kolktiefen"].get(b["nr"], 0))},
                       "rinne_m": r2(b["rinne"]), "uferstufe_m": {k: r2(v) for k, v in b["U"].items()},
                       "prallseite": b["prall"]})
    eh_out = [{"k": e["k"], "klasse": e["klasse"], "von_m": r2(e["a"]), "bis_m": r2(e["b"]),
               "laenge_B": r2((e["b"] - e["a"]) / X["ist"].breite(e["a"])), "spiegel_m": r2(e["P"], 3),
               "fall_m": r2(e["D"]), "teile_m": [r2(x) for x in e["teile"]], "uferstufe_m": r2(e["U"]),
               "kopf_ufer_m": r2(e.get("kopf_m", 0.0))} for e in X["EH"]]
    I = X["I"]
    inst = {}
    mv = X["R"]["bloecke"]["material_vorschlag_6f"]["nach_paket_mi"]
    masse = netze_masse()
    for k in sorted(I.inst):
        e = dict(I.inst[k])
        e["anzahl"] = len(e["eintraege"])
        mats = (masse.get(e["pfad"]) or {}).get("mats") or []
        if mats:
            pm = mats[0].split("/")[-1].split(".")[0]
            e["paket_mi"] = pm
            for muster, vorschlag in mv.items():
                if pm == muster or (muster.endswith("*") and pm.startswith(muster[:-1])):
                    e["material_vorschlag"] = vorschlag
        inst[k] = e
    out = {"format": FORMAT, "stand": X["R"]["stand"], "abschnitt": ab,
           "quelle": os.path.relpath(QUER, ANTW).replace(os.sep, "/"),
           "regeln": "skripte/p2_bett/p2_bett_regeln.json",
           "koordinaten": "Bach: s = m entlang lauf_p2 wie querschnitte_p2.json, u = m quer (u > 0 links = (-t_j, t_i) im "
                          "Raster). Welt ueber p2_bett_welt.py (lauf_p2.json, hoehe.f32).",
           "anschluss": {k: r2(v, 3) for k, v in X["rand"].items()},
           "gelaende": {"datei": fn, "form": [6, len(S), len(U)],
                        "kanaele": ["z_min", "z_max", "gewicht", "spiegel", "abtrag_max", "kante_abstand"],
                        "s0_m": r2(S[0]), "ds_m": DS, "u0_m": r2(U[0]), "du_m": DU, "nan": "keine Grenze",
                        "regel": "neu = max(ist + gewicht * (clip(ist, z_min, z_max) - ist), ist - abtrag_max); Bett: z_min = "
                                 "z_max; Schulter: z_min = Spiegel + Uferstufe; Boeschung: z_max = 35 Grad ab der Uferstufe "
                                 "(zuruecklegen), abtrag_max = Einschnitt gegen den alten Spiegel + 0,3 m, nach aussen auf 0",
                        "zonen": {"datei": "%s_zonen.u8" % ab, "werte": ZONEN}},
           "spiegel_je_m": {"hinweis": "Wasserspiegel auf der lauf_p2-Mittellinie (u = 0) je Meter, fuer die Z der "
                                       "SWR-Spline. Stufen liegen zwischen zwei Punkten; genaue Lage in 'lippen'.",
                            "spalten": ["s_m", "z_m"], "punkte": spm},
           "spline_stufenpunkte": {"hinweis": "16h N6f: je Lippe ein Punkt auf der Lippe (Spiegel oben) und am Fuss der "
                                              "Stufenwand (Spiegel unten), sonst alle 1 m; Punkttyp linear. Ersetzt die 54 "
                                              "Editor-Punkte in s 389-580.", "spalten": ["s_m", "z_m"],
                                   "punkte": spline_stufenpunkte(X)},
           "einheiten": eh_out, "lippen": lip_out, "becken": bk_out,
           "effekte_vorschlag": effekte_vorschlag(X),
           "instanzen_spalten": SPALTEN,
           "instanzen_hinweis": "Schluessel = Netz bzw. Netz_kol (mit Kollision: Bloecke >= 0,8 m, Totholz). z_absolut = "
                                "true: z_plan_m ist die absolute Hoehe der Netzmitte unten (Kantengras auf der Schulter, Totholz "
                                "auf Schultern/Eckblock). Rolle farn: nur am Ufer behalten, dessen Boeschung nach Norden schaut. "
                                "z = neues Gelaende(x, y) - einbettung x groesse (Netzhoehe x skala); z_plan_m nur zur "
                                "Kontrolle (Plan mit angenommenem Ist). yaw_rel_grad gegen die Fliessrichtung (Tangente "
                                "von lauf_p2), kipp_grad stromauf. swr_hindernis nach dem N5-Filter; kollision >= 0,8 m.",
           "instanzen": inst,
           "kennzahlen": kennzahlen(X),
           "pruefung": {"fehler": X["F"], "warnungen": X["Wn"]}}
    with open(os.path.join(aus, "bettplan_p2.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--aus", default=os.path.join(ANTW, "p2_bett"))
    ap.add_argument("--abschnitt", default="talkaskade")
    ap.add_argument("--ohne-bilder", action="store_true")
    ap.add_argument("--selbsttest", action="store_true", help="zweimal rechnen, byte-gleich pruefen")
    a = ap.parse_args(argv)
    X = rechne(a.abschnitt)
    out = schreiben(X, a.aus)
    if not a.ohne_bilder:
        sys.path.insert(0, HIER)
        import p2_bett_bilder as bb
        bb.alle(X, a.aus)
    print(json.dumps(out["kennzahlen"], ensure_ascii=False))
    for w in X["Wn"]:
        print("WARNUNG", w)
    for f in X["F"]:
        print("FEHLER", f)
    rc = 1 if X["F"] else 0
    if a.selbsttest:
        import tempfile
        h = []
        for _ in range(2):
            _KNOTEN.clear()
            d = tempfile.mkdtemp()
            schreiben(rechne(a.abschnitt), d)
            hh = {}
            for fn in sorted(os.listdir(d)):
                with open(os.path.join(d, fn), "rb") as f:
                    hh[fn] = hashlib.sha256(f.read()).hexdigest()
            h.append(hh)
        gleich = h[0] == h[1]
        with open(os.path.join(a.aus, "bettplan_p2.json"), "rb") as f:
            gleich_aus = hashlib.sha256(f.read()).hexdigest() == h[0]["bettplan_p2.json"]
        print("[selbsttest] zwei Laeufe byte-gleich: %s; gleich der Ausgabe: %s; %s" %
              (gleich, gleich_aus, {k: v[:12] for k, v in h[0].items()}))
        if not (gleich and gleich_aus):
            rc = 1
    print("[p2_bettplan] %d FEHLER, %d WARNUNGEN" % (len(X["F"]), len(X["Wn"])))
    return rc


if __name__ == "__main__":
    sys.exit(main())
