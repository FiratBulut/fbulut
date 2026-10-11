#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gefaelle_plan.py - Planer fuer steile Fluss-/Bachstrecken (Auftrag 15): Felsstufen, Kaskaden, Faelle, Klamm, Uferklippen.

Je Lauf (Bach aus baeche_alle.json oder Epic-Fluss eines Felds aus wasser_welt.json) werden alle steilen Strecken aus
vorlagen/daten/gefaelle/steile_strecken.json umgebaut, die laut Prioritaetenliste (antworten/gefaelle/prioritaet.json)
planbar sind (offen | teilweise_sehens | gebaut_teilweise). ALLE Zahlen kommen aus gefaelle_regeln.json (Regelwerk,
Quellen in antworten/15-gefaelle-regelwerk.md); dieses Skript enthaelt nur den Ablauf (regeln["ablauf"]).

Ablauf je Strecke (Regelwerk 'ablauf'):
  1. Mittellinie, Spiegel (monoton), Breite B aus den Laufpunkten; feste Zonen, in denen der Spiegel bleibt:
     Wege/Pfade (+ Uebergang), Orte, Staedte, Sehenswuerdigkeiten (Radius + 10 m), Umbau durch Sehens-Planer,
     andere Gewaesser (Zufluesse), Abschnittsgrenzen langer Strecken.
  2. S im Fenster klassen.fenster, S_lok in klassen.fenster_lokal, Klasse je Punkt.
  3. Knickpunkte: Fenster mit faelle.einzelfall_statt_kette -> EIN Fall (gebuendelt ueber faelle.einzelfall.buendeln).
  4. Uebrige Abschnitte: Stufen nach stufen.abstand_L (Fluss: abstand_L_fluss), Zufall stufen.zufall, Lippe am
     steilsten Punkt im Fenster (Knick). Die Lippe liegt auf dem alten Spiegel, das Becken danach faellt mit
     becken.gefaelle bis zur naechsten Lippe -> D = S*L - S_Becken*(L - Stufenlaenge) und die Summe ist exakt D_ges.
     Der neue Spiegel ist nie hoeher als der alte (nur Eintiefen, kein Damm).
  5. Spiegel: Stufe/Fall = zwei Punkte (stufen.zwei_punkte), Schnelle = Rampe, kurze Becken -> Kaskade (Teilstufen).
  6. Gelaende (Delta, nur absenken): Bett = Spiegel - Tiefe, Lippe als Krone, Kolk je Stufe, Uferboeschung; steil
     (Uferklippe/Klamm) wo ufer_klippen.wann / klamm.wann; Schutz an Wegen, Orten, anderem Wasser, Rand 0.
  7. Netze je Biom am Stufenort (biome.<biom>.netze): Riegel/Lippe/Holz, Fallwand, Uferwaende, Sturzbloecke,
     Beckenbloecke, Wandschutt, Kies, Moos (Kontakt).
  8. Lagen (lagen.zonen + biome.<biom>.lagen), Effekte (effekte, <= 3 je Stufe, <= 6 gleichzeitig), Kameras
     _vorher/_nachher (Augenhoehe -170) fuer Pilot-Strecken, Epic-Flussstuecke (Luecke >= 1,2 m, keine Ueberlappung).

Aufruf (python -I, NumPy + Pillow):
  python -I gefaelle_plan.py [--laeufe ID ...] [--strecken ID ...] [--alle] [--daten2m DIR] [--aus DIR] [--bild]
  Ohne --laeufe/--strecken/--alle: alle Laeufe der 20 Pilot-Strecken aus prioritaet.json.
  Ohne --daten2m: 1-m-Originale aus <basis>/export/unreal/welt, Ausgabe <basis>/export/unreal/welt/gefaelle/<lauf>/.
  Cloud-Test: --daten2m recherche/vorlagen/daten/sehens --aus <scratchpad>/a15/plan
Ausgabe je Lauf (<aus>/<lauf>/): plan.json, gelaende/<abschnitt>.f32, lagen/<abschnitt>_<Lage>.r8,
  instanzen/<Feld>/plan.json + <Netz>.f32 (FORMAT.md §3, Ebene 'gefaelle'); --bild: test_<strecke>.png je Pilot-Strecke.
Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.
Quellen: auftraege/15-gefaelle-felsstufen-klippen.md, antworten/15-gefaelle-regelwerk.md, vorlagen/SEHENS_FORMAT.md
  §3/§6/§8/§9, vorlagen/FORMAT.md §3, vorlagen/daten/wasser_fx/stufen_fluss_teile.json (C2-Teilung), sehens_lib.
"""

import argparse
import json
import math
import os
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(HIER))

import numpy as np  # noqa: E402

import gefaelle_daten as gd  # noqa: E402
import gefaelle_regelwerk as gr  # noqa: E402

DS = 0.5                     # Profil-Raster entlang des Laufs (m)
EBENE = "gefaelle"
FT_PRAEFIX = "FT_EL_GEF_"
SEED = 1515
PLANBAR = ("offen", "teilweise_sehens", "gebaut_teilweise")
FELS_LAGEN = ("Fels", "Felsplatte", "Sandstein", "Lavafels")
# Teilung der Epic-Flussstuecke wie C2 (vorlagen/daten/wasser_fx/stufen_fluss_teile.json["regel"])
TEIL = {"ende_hinter_kante_m": 0.5, "luecke_min_m": 1.2, "luecke_start_m": 1.3, "luecke_max_m": 6.0,
        "velocity_becken_cm_s": 80.0, "velocity_schnelle_cm_s": 300.0, "max_segment_m": 5.0}
BOESCHUNG_GRAD = 35.0        # normale Uferboeschung (schutt.wandfuss_kegel_neigung als Naeherung, s. README)


def _log(*t):
    from sehens_lib import ascii_text
    sys.stdout.write("[gefaelle] %s\n" % " ".join(ascii_text(str(x)) for x in t))
    sys.stdout.flush()


def _r(v, n=1):
    return round(float(v), n)


def glatt01(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ======================================================================================================================
# Profil eines Laufs
# ======================================================================================================================
class Profil:
    """Lauf auf DS-Raster: s, x, y, Tangente, z0 (alter Spiegel, monoton), B, Tiefe (m), v (cm/s)."""

    def __init__(self, lauf):
        self.lauf = lauf
        n = int(math.floor(lauf.laenge_m / DS)) + 1
        s = np.arange(n) * DS
        if s[-1] < lauf.laenge_m - 1e-6:
            s = np.append(s, lauf.laenge_m)
        d = lauf.bei_s(s)
        self.s = s
        self.x, self.y = d["x"], d["y"]
        self.tx, self.ty = d["tx"], d["ty"]
        self.z_roh = d["z"]
        self.z0 = np.minimum.accumulate(d["z"])
        self.B = np.maximum(d["breite"], 1.0)
        self.tiefe = np.clip(d["tiefe"] / 100.0, 0.2, 3.0)
        self.v = d["v"]
        self.n = len(s)

    def i(self, s):
        return int(np.clip(np.searchsorted(self.s, s - 1e-9), 0, self.n - 1))

    def zi(self, s):
        return float(np.interp(s, self.s, self.z0))

    def xy(self, s):
        return float(np.interp(s, self.s, self.x)), float(np.interp(s, self.s, self.y))

    def tang(self, s):
        k = self.i(s)
        return float(self.tx[k]), float(self.ty[k])

    def Bi(self, s):
        return float(np.interp(s, self.s, self.B))

    def gefaelle(self, s, w):
        a, b = max(0.0, s - w / 2.0), min(self.s[-1], s + w / 2.0)
        return max(0.0, (self.zi(a) - self.zi(b)) / max(b - a, 1e-6))

    def gefaelle_ab(self, s, w):
        b = min(self.s[-1], s + w)
        return max(0.0, (self.zi(s) - self.zi(b)) / max(b - s, 1e-6))

    def polylinie(self, a, b, schritt=2.0):
        n = max(2, int(math.ceil((b - a) / schritt)) + 1)
        ss = np.linspace(a, b, n)
        return [[float(np.interp(v, self.s, self.x)), float(np.interp(v, self.s, self.y))] for v in ss]

    def versatz_linie(self, a, b, versatz, schritt=2.0):
        """Linie parallel zur Mittellinie (versatz > 0 = links in Fliessrichtung)."""
        n = max(2, int(math.ceil((b - a) / schritt)) + 1)
        out = []
        for v in np.linspace(a, b, n):
            x, y = self.xy(v)
            tx, ty = self.tang(v)
            out.append([x + ty * versatz, y - tx * versatz])
        return out


def kompass(tx, ty):
    return float(math.degrees(math.atan2(tx, -ty)) % 360.0)


# ======================================================================================================================
# Feste Zonen (Spiegel bleibt)
# ======================================================================================================================
def feste_zonen(pr, welt, gel, orte, umbau, andere, s0, s1):
    """Bool-Array je Profilpunkt: True = alter Spiegel bleibt. Gruende als Liste [(a, b, grund)]."""
    fix = np.zeros(pr.n, bool)
    gruende = []
    sel = (pr.s >= s0 - 1) & (pr.s <= s1 + 1)
    idx = np.flatnonzero(sel)
    if not idx.size:
        return fix, gruende
    x, y, B = pr.x[idx], pr.y[idx], pr.B[idx]
    i, j = welt.m_zu_ij(x, y)

    def markiere(m, grund):
        if not m.any():
            return
        fix[idx[m]] = True
        k = idx[m]
        # zusammenhaengende Bereiche fuer das Protokoll
        st = k[0]
        for a, b in zip(k[:-1], k[1:]):
            if b != a + 1:
                gruende.append((_r(pr.s[st]), _r(pr.s[a]), grund))
                st = b
        gruende.append((_r(pr.s[st]), _r(pr.s[k[-1]]), grund))

    markiere(gel.abstand_weg[i, j] <= 3.0 + 4.0 + B / 2.0 + 2.0, "Weg/Pfad")
    markiere(gel.abstand_ort[i, j] <= 5.0 + 4.0 + B / 2.0 + 2.0, "Ort")
    try:
        markiere(gel.abstand_stadt[i, j] <= 20.0, "Stadt")
    except Exception:  # noqa: BLE001 - Stadtabstand optional (keine Staedte in den Daten)
        pass
    m = np.zeros(len(idx), bool)
    for o in orte:
        m |= np.hypot(x - o["x_m"], y - o["y_m"]) <= o["radius_m"] + 10.0
    markiere(m, "Sehenswuerdigkeit")
    if umbau:
        pr2 = {"x": x, "y": y, "s": pr.s[idx]}
        m = np.zeros(len(idx), bool)
        for o in umbau:
            innen = gd.im_fenster_ij(x, y, o["fenster_ij"]) if o["fenster_ij"] else \
                (np.hypot(x - o["x_m"], y - o["y_m"]) <= o["radius_m"] + 40.0)
            for _, _, P in o["geo"]:
                m |= innen & (gd.abstand_punkte_polylinie(x, y, P) <= 15.0)
            if o["ist_wasser"]:
                m |= innen & (np.hypot(x - o["x_m"], y - o["y_m"]) <= o["radius_m"])
        if m.any():
            mm = m.copy()
            w = int(10.0 / DS)
            for k in np.flatnonzero(m):
                mm[max(0, k - w):k + w + 1] = True
            markiere(mm, "Umbau Sehens-Planer")
        del pr2
    m = np.zeros(len(idx), bool)
    for P in andere:
        bx = (P[:, 0].min() - 30, P[:, 0].max() + 30, P[:, 1].min() - 30, P[:, 1].max() + 30)
        nah = (x >= bx[0]) & (x <= bx[1]) & (y >= bx[2]) & (y <= bx[3])
        if nah.any():
            d = np.full(len(x), np.inf)
            d[nah] = gd.abstand_punkte_polylinie(x[nah], y[nah], P)
            m |= d <= B / 2.0 + 6.0
    if m.any():
        mm = m.copy()
        w = int(8.0 / DS)
        for k in np.flatnonzero(m):
            mm[max(0, k - w):k + w + 1] = True
        markiere(mm, "anderes Gewaesser (Zufluss/See)")
    return fix, gruende


# ======================================================================================================================
# Stufen legen
# ======================================================================================================================
class Stufenleger:
    def __init__(self, rw, pr, welt, art_daten, rng, biom_fn, fels_fn):
        self.rw, self.pr, self.welt, self.rng = rw, pr, welt, rng
        self.art_daten = art_daten
        self.biom_fn, self.fels_fn = biom_fn, fels_fn
        self.zp_ziel, self.zp_max = rw.zwei_punkte()
        self.Ls, self.Dsd = rw.zufall()

    def art_lauf(self, s):
        return self.rw.art_lauf(self.art_daten, self.pr.Bi(s))

    def klasse(self, s, S=None):
        B = self.pr.Bi(s)
        if S is None:
            S = self.pr.gefaelle(s, self.rw.fenster(B))
        return self.rw.klasse(self.art_lauf(s), S), S

    def einzelfaelle(self, a, b):
        """Knickpunkte (faelle.einzelfall_statt_kette): Liste (oben, unten) gebuendelt."""
        S_min, D_min, D_fels = self.rw.einzelfall()
        pr = self.pr
        ks = np.flatnonzero((pr.s >= a) & (pr.s <= b))
        if ks.size < 3:
            return []
        steil = np.array([pr.gefaelle(pr.s[k], self.rw.fenster_lokal(pr.B[k])) >= S_min for k in ks])
        laeufe = []
        st = None
        for n, k in enumerate(ks):
            if steil[n] and st is None:
                st = pr.s[k]
            if (not steil[n] or n == len(ks) - 1) and st is not None:
                laeufe.append([st, pr.s[k]])
                st = None
        if not laeufe:
            return []
        # buendeln: Steilstuecke naeher als buendel_L zusammenziehen
        geb = [laeufe[0]]
        for l0, l1 in laeufe[1:]:
            if l0 - geb[-1][1] <= self.rw.buendel_L(pr.Bi(l0)):
                geb[-1][1] = l1
            else:
                geb.append([l0, l1])
        out = []
        for o, u in geb:
            B = pr.Bi(o)
            wl = self.rw.fenster_lokal(B)
            o2, u2 = max(a, o - wl / 2.0), min(b, u + wl / 2.0)
            D = pr.zi(o2) - pr.zi(u2)
            fels = self.fels_fn(o2, pr.gefaelle(o2, self.rw.fenster(B)))
            if D >= (D_fels if fels else D_min) and u2 - o2 >= 1.0:
                out.append((o2, u2, D, fels))
        return out

    def lege(self, a, b):
        """Lippen im Segment [a, b] (Spiegel bleibt bei a und b). Rueckgabe Liste Stufen-dicts (ohne Kaskaden)."""
        pr, rw = self.pr, self.rw
        faelle = self.einzelfaelle(a, b)
        stufen = []
        p = a
        fi = 0
        hmax = rw.hoehe_max_einzeln()
        while p < b - 0.5:
            # Einzelfall direkt hier?
            if fi < len(faelle) and faelle[fi][0] <= p + 0.25:
                o, u, D, fels = faelle[fi]
                fi += 1
                n_teil = max(1, int(math.ceil(D / hmax)))
                grenzen = [o + (u - o) * k / n_teil for k in range(n_teil + 1)]
                if n_teil > 1:     # zwei Faelle mit Zwischengumpe: Grenze dort, wo der Spiegel die Haelfte erreicht
                    zz = [pr.zi(o) - D * k / n_teil for k in range(n_teil + 1)]
                    grenzen = [o] + [float(np.interp(-z, -pr.z0, pr.s)) for z in zz[1:-1]] + [u]
                for k in range(n_teil):
                    stufen.append({"p": grenzen[k], "q": grenzen[k + 1], "erzwungen": True, "fels": fels})
                p = u
                continue
            B = pr.Bi(p)
            S = pr.gefaelle(p, rw.fenster(B))
            kl, S = self.klasse(p, S)
            arten = kl.get("stufenarten") or []
            if not arten:
                # keine Stufen in dieser Klasse: Spiegel bleibt bis die Klasse wechselt (Weiterruecken)
                p = p + max(2.0, B)
                if stufen and stufen[-1].get("q") is None:
                    stufen[-1]["q"] = p
                stufen.append({"p": p, "q": None, "leer": True})
                continue
            gb = rw.becken_gefaelle(S)
            fels = self.fels_fn(p, S)
            if self.art_lauf(p) == "fluss":
                L_nom = gr.abstand_L_fluss(rw, S, B, kl["id"])
            else:
                L_nom = rw.abstand_L(S, B)
            D_nom = max(S - gb, 1e-3) * L_nom
            lo = min(rw.art_bereich(a_)[0] for a_ in arten)
            hi = max(rw.art_bereich(a_)[1] for a_ in arten)
            if "fall" in arten and not fels and len(arten) > 1:
                hi = max(rw.art_bereich(a_)[1] for a_ in arten if a_ != "fall")   # Fall nur an Fels
            if kl["id"] in ("fallkette", "fall_klamm", "fall_schlucht", "katarakt_fels") and "fall" in arten and fels:
                # Fallkette: Glieder nach faelle.kette_glied (D_ges = Fall des steilen Fensters)
                w_end = p
                while w_end < b and self.klasse(w_end)[0]["id"] == kl["id"]:
                    w_end += 2.0
                D_nom = rw.kette_glied(pr.zi(p) - pr.zi(min(w_end, b)), B)
            hi = min(hi, hmax)
            D_t = float(np.clip(D_nom, lo, hi))
            D_t = float(np.clip(D_t * (1.0 + self.rng.uniform(-self.Dsd, self.Dsd)), lo, hi))
            L_t = D_t / max(S - gb, 1e-3)
            L_min = max(gr.min_abstand_stufen(rw, B), 100.0 / rw.max_stufen_je_100m())
            L_t = max(L_t * (1.0 + self.rng.uniform(-self.Ls, self.Ls)), L_min)
            # naechster Einzelfall begrenzt das Fenster
            grenze = faelle[fi][0] if fi < len(faelle) else b
            q0, q1 = p + 0.75 * L_t, p + 1.25 * L_t
            if q0 >= grenze - 0.5 * L_min:
                q = grenze
            else:
                kand = np.arange(q0, min(q1, grenze) + 1e-6, DS)
                wl = rw.fenster_lokal(B)
                sc = np.array([pr.gefaelle_ab(c, wl) for c in kand]) + self.rng.uniform(0, 0.02, len(kand))
                q = float(kand[int(np.argmax(sc))])
                if b - q < L_min:
                    q = b
            stufen.append({"p": p, "q": q, "erzwungen": False, "fels": fels, "klasse": kl["id"]})
            p = q
        # Leere Platzhalter entfernen und q schliessen
        out = []
        for k, st in enumerate(stufen):
            if st.get("leer"):
                continue
            if st.get("q") is None:
                st["q"] = b
            out.append(st)
        return out

    def ausarbeiten(self, roh, a, b):
        """D, Art, Stufenlaenge je Lippe; zu kleine Stufen zusammenlegen, zu grosse teilen."""
        pr, rw = self.pr, self.rw
        st = sorted(roh, key=lambda e: e["p"])
        # q = naechste Lippe bzw. Segmentende
        for k, e in enumerate(st):
            e["q"] = st[k + 1]["p"] if k + 1 < len(st) else b
        geaendert = True
        runde = 0
        while geaendert and runde < 20:
            geaendert = False
            runde += 1
            for k, e in enumerate(st):
                self._rechne(e)
                lo_global = rw.art_bereich("schnelle")[0]
                if e["D"] < lo_global and not e["erzwungen"]:
                    # zu klein: Lippe weglassen (Becken davor laeuft weiter)
                    if k > 0:
                        st[k - 1]["q"] = e["q"]
                        del st[k]
                        geaendert = True
                        break
                    elif len(st) > 1:
                        st[1]["p"] = e["p"]
                        del st[0]
                        geaendert = True
                        break
                if e["art"] != "fall" and e["D"] > e["D_max"] + 1e-6 and e["q"] - e["p"] > 2 * e["L_min"]:
                    # zu gross fuer die Art: Einheit an der Haelfte des Spiegelfalls teilen
                    zm = 0.5 * (pr.zi(e["p"]) + pr.zi(e["q"]))
                    sm = float(np.interp(-zm, -pr.z0, pr.s))
                    sm = float(np.clip(sm, e["p"] + e["L_min"], e["q"] - e["L_min"]))
                    neu = {"p": sm, "q": e["q"], "erzwungen": False, "fels": e["fels"], "klasse": e.get("klasse")}
                    e["q"] = sm
                    st.insert(k + 1, neu)
                    geaendert = True
                    break
        for e in st:
            self._rechne(e)
        return st

    def _rechne(self, e):
        pr, rw = self.pr, self.rw
        p, q = e["p"], e["q"]
        B = pr.Bi(p)
        L = max(q - p, 0.5)
        S_e = max((pr.zi(p) - pr.zi(q)) / L, 0.0)
        kl, _ = self.klasse(p, S_e)
        arten = kl.get("stufenarten") or ["schnelle"]
        gb = rw.becken_gefaelle(S_e)
        e["S"], e["L"], e["B"], e["klasse"] = S_e, L, B, kl["id"]
        e["L_min"] = max(gr.min_abstand_stufen(rw, B), 1.0)
        e["u"] = pr.zi(p)
        # Stufenart nach D (vorlaeufig mit Zwei-Punkt-Laenge)
        D0 = e["u"] - pr.zi(q) - gb * max(L - self.zp_ziel, 0.0)
        if e.get("erzwungen"):
            art = "fall"
        elif D0 >= 2.0 and "fall" in arten and e["fels"]:
            art = "fall"
        elif D0 >= rw.art_bereich("stufe")[0] and "stufe" in arten:
            art = "stufe"
        elif "kaskade" in arten and D0 >= rw.art_bereich("kaskade")[0] and "stufe" not in arten:
            art = "kaskade"
        elif "schnelle" in arten and D0 <= rw.art_bereich("schnelle")[1]:
            art = "schnelle"
        elif "stufe" in arten:
            art = "stufe"
        elif "kaskade" in arten:
            art = "kaskade"
        elif "fall" in arten:
            art = "fall"
        else:
            art = arten[0]
        if art == "schnelle":
            l_st, _ = rw.rampe(max(D0, 0.15))
            l_st = min(l_st, 0.5 * L)
        else:
            l_st = self.zp_ziel
        D = e["u"] - pr.zi(q) - gb * max(L - l_st, 0.0)
        if D < 0:
            D = 0.0
        e["art"], e["l"], e["D"], e["gb"] = art, l_st, D, gb
        e["d"] = e["u"] - D
        lo, hi = rw.art_bereich(art)
        e["D_min"], e["D_max"] = lo, (hi if art != "fall" else rw.hoehe_max_einzeln())

    def kaskaden(self, st):
        """Stufen mit zu kurzen Becken (< becken.laenge_min bzw. > 20 je 100 m) zu Kaskaden mit Teilstufen buendeln.
        Teilstufen bleiben je zwei Punkte; im Plan zaehlt die Kaskade als EINE Stufe (Epic-Teilung an der Kaskade)."""
        rw = self.rw
        k_lo, k_hi = rw.art_bereich("kaskade")
        out = []
        k = 0
        while k < len(st):
            e = st[k]
            gruppe = [e]
            while True:
                last = gruppe[-1]
                becken = last["L"] - last["l"]
                kurz = becken < 1.5 * max(rw.becken_laenge_min(last["B"]), last["L_min"])
                if (k + len(gruppe) < len(st) and kurz and last["art"] in ("stufe", "kaskade") and len(gruppe) < 4 and
                        st[k + len(gruppe)]["art"] in ("stufe", "kaskade") and k_lo <= last["D"] <= k_hi and
                        k_lo <= st[k + len(gruppe)]["D"] <= k_hi):
                    gruppe.append(st[k + len(gruppe)])
                else:
                    break
            if len(gruppe) >= 2:
                kk = {"p": gruppe[0]["p"], "q": gruppe[-1]["q"], "art": "kaskade", "erzwungen": False,
                      "fels": any(g["fels"] for g in gruppe), "klasse": gruppe[0]["klasse"],
                      "teil": [{"p": g["p"], "u": g["u"], "d": g["d"], "D": g["D"], "l": g["l"]} for g in gruppe],
                      "u": gruppe[0]["u"], "d": gruppe[-1]["d"], "D": sum(g["D"] for g in gruppe),
                      "S": gruppe[0]["S"], "B": gruppe[0]["B"], "gb": gruppe[-1]["gb"],
                      "L": gruppe[-1]["q"] - gruppe[0]["p"], "L_min": gruppe[0]["L_min"],
                      "l": gruppe[-1]["p"] + gruppe[-1]["l"] - gruppe[0]["p"], "D_min": k_lo, "D_max": k_hi}
                out.append(kk)
            else:
                if e["art"] == "kaskade":            # einzelne 'kaskade' = Blockstufe mit einer Teilstufe
                    e["teil"] = [{"p": e["p"], "u": e["u"], "d": e["d"], "D": e["D"], "l": e["l"]}]
                out.append(e)
            k += len(gruppe)
        return out


# ======================================================================================================================
# Spiegel, Flussstuecke
# ======================================================================================================================
def spiegel_punkte(pr, alle_stufen, segmente):
    """Bruchpunkte (s, z) des neuen Spiegels ueber den ganzen Lauf + Kennzeichen je Punkt
    ('alt' | 'becken' | 'lippe' | 'fuss' | 'rampe')."""
    pkt = []
    # alte Laufpunkte ausserhalb der Segmente
    for s_ in pr.lauf.s:
        if not any(a - 1e-6 <= s_ <= b + 1e-6 for a, b in segmente):
            pkt.append((float(s_), pr.zi(s_), "alt"))
    for a, b in segmente:
        st = [e for e in alle_stufen if a - 1e-6 <= e["p"] <= b + 1e-6]
        pkt.append((a, pr.zi(a), "alt"))
        for k, e in enumerate(st):
            q = st[k + 1]["p"] if k + 1 < len(st) else b
            teile = e.get("teil") or [{"p": e["p"], "u": e["u"], "d": e["d"], "l": e["l"]}]
            for n, t in enumerate(teile):
                pkt.append((t["p"], t["u"], "lippe"))
                if e["art"] == "schnelle":
                    pkt.append((t["p"] + t["l"], t["d"], "rampe"))
                else:
                    pkt.append((t["p"] + t["l"], t["d"], "fuss"))
                # Mini-Becken zwischen Teilstufen
                if n + 1 < len(teile):
                    pass
            ende = e["p"] + e["l"]
            # Becken bis zur naechsten Lippe / Segmentende, Zwischenpunkte <= max_segment
            z_a, z_b = e["d"], pr.zi(q)
            nseg = max(1, int(math.ceil((q - ende) / TEIL["max_segment_m"])))
            for m in range(1, nseg):
                ss = ende + (q - ende) * m / nseg
                pkt.append((ss, z_a + (z_b - z_a) * m / nseg, "becken"))
        pkt.append((b, pr.zi(b), "alt"))
    pkt.sort(key=lambda t: (t[0], -t[1]))
    # doppelte s zusammenfassen (Monotonie absichern)
    out = []
    for s_, z_, k_ in pkt:
        if out and abs(out[-1][0] - s_) < 1e-4:
            if z_ < out[-1][1]:
                out[-1] = (s_, z_, k_)
            continue
        out.append((s_, z_, k_))
    zs = np.minimum.accumulate(np.array([t[1] for t in out]))
    return [(t[0], float(z), t[2]) for t, z in zip(out, zs)]


def spiegel_bei(sp, s):
    S = np.array([t[0] for t in sp])
    Z = np.array([t[1] for t in sp])
    return np.interp(s, S, Z)


# ======================================================================================================================
# Gelaende
# ======================================================================================================================
def gelaende_abschnitt(ctx_g, pr, sp, stufen, seg_a, seg_b, breite_fn, winkel_fn, rw, welt, gel, orte):
    """Delta-Hoehe (nur absenken) im Fenster: Bett/Kolk/Lippe/Boeschung/Klippe entlang [seg_a, seg_b]."""
    from sehens_lib import stempel as stm, gelaende as gel_mod
    st = ctx_g
    X, Y = st.X, st.Y
    h0 = st.h0
    linie = pr.polylinie(seg_a, seg_b, 1.0)
    P = np.asarray(linie)
    # grob: Abstand zur Mittellinie (Rasterlinie) -> nur Zellen im Band rechnen
    fe = st.fe
    m_lin = np.zeros(X.shape, bool)
    li, lj = fe.lokal(P[:, 0], P[:, 1])
    li = np.clip(np.rint(li).astype(int), 0, X.shape[0] - 1)
    lj = np.clip(np.rint(lj).astype(int), 0, X.shape[1] - 1)
    m_lin[li, lj] = True
    reach = 60.0
    dgrob = gel_mod.abstand(m_lin, welt.zelle_m, reach + 5.0)
    band = dgrob <= reach
    xs, ys = X[band], Y[band]
    d, s_loc, _ = stm.polylinie_abstand(xs, ys, linie)
    s = seg_a + s_loc
    innen = (s > seg_a + 0.01) & (s < seg_b - 0.01)
    Bw = breite_fn(s)
    half = Bw / 2.0
    core = 0.35 * Bw
    z_sp = spiegel_bei(sp, s)
    bett = z_sp - np.interp(s, pr.s, pr.tiefe)
    # Bett-Tiefe am Segmentende ausblenden (kein Absatz unter Wasser am Anschluss)
    bett = z_sp - (z_sp - bett) * glatt01((seg_b - s) / 6.0)
    # Lippen-Krone und Kolke
    for e in stufen:
        teile = e.get("teil") or [{"p": e["p"], "u": e["u"], "d": e["d"], "D": e["D"], "l": e["l"]}]
        for t in teile:
            krone = (s >= t["p"] - 1.0) & (s <= t["p"] + 0.05)
            bett = np.where(krone, np.minimum(bett, t["u"] - 0.15), bett)
        if e["art"] == "schnelle":
            continue
        ko = e["kolk"]
        k0 = e["p"] + e["l"]
        rel = (s - k0) / max(ko["laenge"], 0.5)
        form = np.where(rel < 0.2, glatt01(rel / 0.2), np.where(rel < 0.6, 1.0, 1.0 - glatt01((rel - 0.6) / 0.4)))
        form = np.where((rel >= 0) & (rel <= 1), form, 0.0)
        kolk = e["d"] - ko["tiefe"] * form
        bett = np.where(form > 0, np.minimum(bett, kolk), bett)
    t = np.tan(np.radians(winkel_fn(s)))
    T = np.where(d <= core, bett,
                 np.where(d <= half, bett + (z_sp + 0.05 - bett) * glatt01((d - core) / np.maximum(half - core, 0.1)),
                          z_sp + 0.05 + (d - half) * t))
    cur = h0[band]
    neu = np.where(innen, np.minimum(cur, T), cur)
    st.delta[band] = np.minimum(st.delta[band], neu - cur)      # mehrere Segmente im Fenster: tiefster Wert gilt
    korr = np.zeros(X.shape, bool)
    korr[band] = innen & (d <= np.maximum(half + 4.0, 6.0))
    return korr


def schutz_orte(st, welt, gel, orte):
    """Kein Eingriff an Orten (karte_ort, 5 m + 4 m Uebergang) und in Sehenswuerdigkeiten (Radius + 10 m)."""
    from sehens_lib import gelaende as gel_mod
    fe = st.fe
    m = fe.get("ort") > 0
    if m.any():
        d = gel_mod.abstand(m, welt.zelle_m, 20.0)
        st.delta *= glatt01((d - 5.0) / 4.0)
    for o in orte:
        d = np.hypot(st.X - o["x_m"], st.Y - o["y_m"]) - (o["radius_m"] + 10.0)
        if (d < 8.0).any():
            st.delta *= glatt01(d / 8.0)


# ======================================================================================================================
# Instanzen (sehens_lib.rezept.OrtKontext als Baukasten: Platzieren, Eingraben, Abstaende, Filter, Budget)
# ======================================================================================================================
def netze_pruefen(inv, liste, melde, was):
    ok = []
    for n in liste or []:
        bef = inv.netz_pruefen(n)
        if any(s == "FEHLER" for s, _ in bef):
            melde("HINWEIS", "Regelwerk %s: Netz %s uebersprungen (%s)" % (was, n, "; ".join(t for _, t in bef)))
            continue
        ok.append(n)
    return ok


def setze(ctx, name, ebene, palette, punkte, yaws=None, **kw):
    """Gruppe an festen Punkten (Anker <name>__nnn, optional Yaw je Punkt)."""
    if not punkte or not palette:
        return []
    for i, (x, y) in enumerate(punkte):
        ctx.anker["%s__%03d" % (name, i)] = (float(x), float(y))
        if yaws is not None:
            ctx.richtungen["%s__%03d" % (name, i)] = float(yaws[i]) % 360.0
    g = {"name": name, "ebene": ebene, "palette": list(palette), "verteilung": {"typ": "anker", "praefix": name + "__"}}
    g.update(kw)
    try:
        return ctx.gruppe(g)
    except (KeyError, ValueError) as ex:
        ctx.melde("FEHLER", "Gruppe %s: %s" % (name, ex))
        return []


def gruppe(ctx, g):
    try:
        return ctx.gruppe(g)
    except (KeyError, ValueError) as ex:
        ctx.melde("FEHLER", "Gruppe %s: %s" % (g.get("name"), ex))
        return []


def lippe_linie(pr, rw, e, rng):
    """Lippe quer zum Lauf (links -> rechts mit Blick talwaerts), flacher Bogen mit Scheitel stromab."""
    x, y = pr.xy(e["p"])
    tx, ty = pr.tang(e["p"])
    lx, ly = ty, -tx                                          # links (Norden oben)
    B = e["B"]
    br = rw.lippe_breite(B)
    n_min, n_max = gr.lippe_punkte(rw)
    n = int(np.clip(round(br / 2.0) + 1, n_min, n_max))
    pf = rw.lippe_pfeil() * B
    pts = []
    for k in range(n):
        t = -0.5 + k / (n - 1)
        bog = pf * (1.0 - (2 * t) ** 2)
        pts.append([x + lx * (-t) * br + tx * bog, y + ly * (-t) * br + ty * bog])   # t=-0.5 -> links
    ub = rw.ueberfall_breite(B)
    vers = float(rng.uniform(-0.25, 0.25)) * max(B - ub, 0.0)
    ue = [x + lx * vers + tx * pf, y + ly * vers + ty * pf]
    return pts, ue, ub, br


def bauen_instanzen(ctx, K, pr, abschnitt_stufen, segmente, wandzonen, biom_netze, eintr):
    """Alle Gruppen eines Abschnitts. biom_netze: dict biom -> (biom_name, netze-dict gefiltert)."""
    rw, inv = K["rw"], K["inv"]
    hz = gr.holzstufe(rw)
    # 1. Fallwaende (held), 2. Riegel/Lippe/Holz, 3. Uferwaende, 4. Sturzbloecke, 5. Beckenbloecke, 6. Wandschutt,
    # 7. Kies, 8. Moos (Kontakt)
    fels_gruppen = []
    for e in abschnitt_stufen:
        bn, N = biom_netze[e["biom"]]
        k = e["nr"]
        fl = kompass(*pr.tang(e["p"]))
        quer = (fl + 90.0) % 360.0
        if e["art"] == "fall" and N["wand"]:
            ko = e["kolk"]
            h = e["D"] + 0.5 * ko["tiefe"] + 0.3
            netz = N["wand"][int(ctx_rng(ctx, "fw", k).integers(len(N["wand"])))]
            info = inv.netz(netz)
            gz = max(info["groesse_m"][2], 0.1)
            breite = info["groesse_m"][0] * h / gz
            br = e["lippe_breite_m"]
            n = 1 if breite >= 0.8 * br else min(3, int(math.ceil(br / max(breite * 0.85, 0.5))))
            x, y = pr.xy(e["p"] + 0.3)
            tx, ty = pr.tang(e["p"])
            pts = [(x + ty * o, y - tx * o) for o in np.linspace(-(n - 1) / 2.0, (n - 1) / 2.0, n) * min(breite * 0.85, br / n)]
            g = setze(ctx, "fallwand_%02d" % k, "held", [netz], pts, [fl] * n, rolle="fels", groesse_m=[h * 0.95, h * 1.05],
                      groesse_achse="z", front_achse="+y", ausrichtung="aufrecht", z_bezug="z:%.3f" % (e["d"] - 0.5 * ko["tiefe"]),
                      akteur=True, kollision=True, im_wasser="egal", meide=None, weg_abstand_m=4.0, yaw_streuung_grad=4.0,
                      warum="Felsriegel unter der Lippe: Fallwand %.1f m (faelle.wand_neigung, Ruecksprung)" % e["D"])
            fels_gruppen.append("fallwand_%02d" % k)
        teile = e.get("teil") or [{"p": e["p"], "u": e["u"], "d": e["d"], "D": e["D"], "l": e["l"]}]
        if e.get("holz") and N["holz"]:
            pts = [pr.xy(t["p"]) for t in teile]
            setze(ctx, "holz_%02d" % k, "begleiter", N["holz"], pts, [quer] * len(pts), rolle="stamm",
                  ausrichtung="liegend", groesse_m=[e["lippe_breite_m"] * 0.85, e["lippe_breite_m"] * 1.0],
                  groesse_achse="max", zentrieren=True, akteur=False, kollision=True, im_wasser="egal", meide=None,
                  eingraben=[0.3, 0.4], warum="Holzstufe (stufen.holzstufe): Stamm quer ueber die Lippe")
            continue
        if e["art"] == "fall":
            dick = float(np.clip(gr.formel(rw.r["faelle"]["riegel_dicke"]["formel"], D=e["D"]), 1.0, 4.0))
            n = max(2, int(math.ceil(e["lippe_breite_m"] / max(dick, 0.5))))
            lin = e["_lippe_m"]
            pts = _entlang(lin, n)
            setze(ctx, "riegel_%02d" % k, "begleiter", N["riegel"] or N["lippe"], pts, [quer] * n, rolle="fels",
                  groesse_m=[dick * 0.85, dick * 1.1], groesse_achse="max", akteur=False, kollision=True,
                  im_wasser="egal", meide=None, eingraben=[0.35, 0.5], weg_abstand_m=4.0,
                  warum="durchgehende Lippe aus Riegel-Netzen (faelle.riegel_dicke)")
            if N["lippe"]:
                setze(ctx, "lippe_%02d" % k, "schutt", N["lippe"], _entlang(lin, max(2, n - 1)), [quer] * max(2, n - 1),
                      rolle="fels", groesse_m=[0.8, 1.6], groesse_achse="max", akteur=False, im_wasser="egal",
                      meide=None, eingraben=[0.3, 0.45], normale_anteil=0.6,
                      warum="Felsplatten der Deckschicht an der Krone")
            fels_gruppen += ["riegel_%02d" % k, "lippe_%02d" % k]
            continue
        # Blockstufe / Kaskade / Schnelle: Stufenbloecke, Keystone in der Mitte
        for n_t, t in enumerate(teile):
            H = t["D"] + (e["kolk"]["tiefe"] if e["art"] != "schnelle" else 0.0)
            d_blk, n_blk = gr.stufenblock(rw, H, e["B"], e["lippe_breite_m"])
            d_blk = float(np.clip(d_blk, 0.4, 3.0))
            if e["art"] == "schnelle":
                n_blk = max(2, min(n_blk, 4))
                d_blk = float(np.clip(d_blk, 0.4, 1.5))
            e_t = dict(e, p=t["p"])
            lin, _, _, _ = lippe_linie(pr, rw, e_t, ctx_rng(ctx, "lip", k, n_t))
            pts = _entlang(lin, n_blk)
            mid = (n_blk - 1) / 2.0
            kern = [pts[int(round(mid))]]
            flanke = [p_ for i_, p_ in enumerate(pts) if i_ != int(round(mid))]
            nm = "riegel_%02d_%d" % (k, n_t)
            setze(ctx, nm + "k", "begleiter" if d_blk >= 1.2 else "schutt", N["riegel"] or N["bloecke"], kern, [quer],
                  rolle="fels", groesse_m=[d_blk * 0.95, d_blk * 1.05], groesse_achse="max", akteur=d_blk >= 2.5,
                  im_wasser="egal", meide=None, eingraben=[0.3, 0.45], weg_abstand_m=4.0,
                  warum="Keystone der Blockstufe (schutt.stufenblock_D)")
            setze(ctx, nm + "f", "schutt", N["riegel"] or N["bloecke"], flanke, [quer] * len(flanke), rolle="fels",
                  groesse_m=[d_blk * 0.55, d_blk * 0.85], groesse_achse="max", akteur=False, im_wasser="egal",
                  meide=None, eingraben=[0.3, 0.45], weg_abstand_m=4.0, warum="Stufenbloecke neben dem Keystone")
            fels_gruppen += [nm + "k", nm + "f"]
    # 3. Uferwaende
    for wz in wandzonen:
        bn, N = biom_netze[wz["biom"]]
        if not N["wand"]:
            continue
        nm = "wand_%02d" % wz["nr"]
        netz = N["wand"][int(ctx_rng(ctx, "wz", wz["nr"]).integers(len(N["wand"])))]
        info = inv.netz(netz)
        h = float(np.clip(wz["hoehe"], 2.0, 40.0))
        breite = info["groesse_m"][0] * h / max(info["groesse_m"][2], 0.1)
        lin_name = "wl_%02d" % wz["nr"]
        ctx.linien[lin_name] = pr.polylinie(wz["a"], wz["b"], 1.0)
        ueb = 0.5 * sum(K["klamm"]["ueberlappung"])
        gruppe(ctx, {"name": nm, "ebene": "begleiter", "netz": netz, "rolle": "fels",
                     "verteilung": {"typ": "reihe", "punkte": lin_name, "abstand_m": max(2.0, breite * (1.0 - ueb)),
                                    "versatz_m": wz["versatz"], "versatz_streuung_m": 0.4, "seiten": ["links", "rechts"],
                                    "blick": "zur_linie", "front_an_linie": True},
                     "groesse_m": [h * 0.9, h * 1.1], "groesse_achse": "z", "front_achse": "+y", "ausrichtung": "aufrecht",
                     "z_bezug": "z:%.3f" % (wz["z_wasser"] - 0.3), "akteur": True, "kollision": True,
                     "im_wasser": "egal", "meide": None, "weg_abstand_m": 4.0, "yaw_streuung_grad": 6.0,
                     "warum": "Uferwand %s (ufer_klippen/klamm), %.1f m hoch" % (wz["grund"], h)})
        fels_gruppen.append(nm)
        # 6. Wandschutt (Kegel am Wandfuss)
        kl, _ = gr.kegel(rw, h)
        for seite, sg in (("l", 1.0), ("r", -1.0)):
            ln = "ws_%02d_%s" % (wz["nr"], seite)
            ctx.linien[ln] = pr.versatz_linie(wz["a"], wz["b"], sg * (wz["versatz"] - 0.2 - kl / 2.0), 2.0)
            n = int(max(3, (wz["b"] - wz["a"]) * 0.6))
            gruppe(ctx, {"name": "wandschutt_%02d_%s" % (wz["nr"], seite), "ebene": "schutt", "palette": N["schutt"] or N["bloecke"],
                         "anzahl": n, "verteilung": {"typ": "band", "punkte": ln, "breite_m": max(kl, 1.0)},
                         "abstand_m": 0.8, "groesse_m": [0.3, 1.0], "rolle": "fels", "im_wasser": "nein",
                         "warum": "Schuttkegel am Wandfuss (schutt.kegel_laenge)"})
    # 4. Sturzbloecke unter Faellen
    for e in abschnitt_stufen:
        if e["art"] != "fall":
            continue
        bn, N = biom_netze[e["biom"]]
        gm, n = gr.unter_fall(rw, e["D"])
        x, y = pr.xy(e["p"] + e["l"] + e["kolk"]["x_strahl"])
        ctx.anker["sturz_%02d" % e["nr"]] = (x, y)
        gruppe(ctx, {"name": "sturz_%02d" % e["nr"], "ebene": "schutt", "palette": N["bloecke"], "anzahl": n,
                     "verteilung": {"typ": "faecher", "bei": "sturz_%02d" % e["nr"], "richtung": kompass(*pr.tang(e["p"])),
                                    "laenge_m": e["kolk"]["laenge"] + e["B"], "oeffnung_grad": 70},
                     "abstand_m": 0.8, "groesse_m": [gm * 0.7, gm * 1.3], "rolle": "fels", "im_wasser": "egal",
                     "warum": "Sturzbloecke in und neben der Gumpe (schutt.unter_fall)"})
    # 5. Beckenbloecke + 7. Kies je Segment
    korn = gr.becken_korn(rw)
    for n_s, (a, b, biom) in enumerate(segmente):
        bn, N = biom_netze[biom]
        ln = "seg_%02d" % n_s
        ctx.linien[ln] = pr.polylinie(a, b, 1.0)
        B = float(np.mean(pr.B[(pr.s >= a) & (pr.s <= b)])) if b > a else 3.0
        if N["bloecke"]:
            gruppe(ctx, {"name": "beckenbloecke_%02d" % n_s, "ebene": "wasser", "palette": N["bloecke"],
                         "anzahl": max(1, int((b - a) / max(3.0 * B, 6.0))),
                         "verteilung": {"typ": "band", "punkte": ln, "breite_m": 0.8 * B}, "abstand_m": 2.0,
                         "groesse_m": [0.4, 0.9], "rolle": "stein", "im_wasser": "egal",
                         "warum": "einzelne Bloecke im Becken (grob an Stufen, fein im Becken)"})
        if N["kies"]:
            gruppe(ctx, {"name": "kies_%02d" % n_s, "ebene": "kleinzeug", "palette": N["kies"],
                         "anzahl": int(min(4000, (b - a) * (B + 2.0) * 0.35)),
                         "verteilung": {"typ": "band", "punkte": ln, "breite_m": B + 2.0}, "abstand_m": 0.45,
                         "skala": [0.6, 1.1], "rolle": "stein", "im_wasser": "egal",
                         "warum": "Kies im Becken und am Ufer (schutt.becken_korn %.2f-%.2f m)" % korn})
    # 8. Moos (Kontakt) an allen Felsgruppen
    moos = {}
    for e in abschnitt_stufen:
        bn, N = biom_netze[e["biom"]]
        moos.setdefault(bn, [n for n in N["extra"] if "oss" in n and "Embankment" not in n])
    m_netze = sorted({n for v in moos.values() for n in v})
    vorhanden = [g for g in fels_gruppen if ctx.gruppen.get(g)]
    if m_netze and vorhanden:
        gruppe(ctx, {"name": "moos", "ebene": "kontakt", "palette": m_netze,
                     "verteilung": {"typ": "um_gruppe", "gruppe": vorhanden, "ring": [0.6, 1.1], "je": [1, 3],
                                    "seite": "nord"}, "rolle": "streu", "im_wasser": "nein", "meide": "kern",
                     "warum": "Moos auf der Nordseite der Felsen (Spruehzone, Schatten)"})


def ctx_rng(ctx, *teile):
    from sehens_lib import instanzen as ins
    return ins.rng_fuer(SEED, ctx.id, *teile)


def _entlang(lin, n):
    P = np.asarray(lin, np.float64)
    seg = np.hypot(*np.diff(P, axis=0).T)
    kum = np.concatenate([[0.0], np.cumsum(seg)])
    L = kum[-1]
    out = []
    for k in range(n):
        sd = L * (k + 0.5) / n
        j = int(np.clip(np.searchsorted(kum, sd, side="right") - 1, 0, len(seg) - 1))
        f = (sd - kum[j]) / max(seg[j], 1e-9)
        out.append((float(P[j, 0] + (P[j + 1, 0] - P[j, 0]) * f), float(P[j, 1] + (P[j + 1, 1] - P[j, 1]) * f)))
    return out


# ======================================================================================================================
# Lagen
# ======================================================================================================================
def bauen_lagen(lg, K, pr, stufen, segmente, wandzonen, biom_lagen, breite_fn):
    rw = K["rw"]
    rand = gr.rand_weich(rw)

    def zone(z, biom, standard=None):
        return gr.lagen_zone(rw, z, biom_lagen[biom], standard)

    def band(namen_g, punkte, breite):
        g, namen = namen_g
        for i_, n in enumerate(namen):
            lg.band(n, punkte, max(breite, 1.0), g * (1.0 if i_ == 0 else 0.7), rand_m=rand, flecken=0.25)

    def kreis(namen_g, x, y, r):
        g, namen = namen_g
        for i_, n in enumerate(namen):
            lg.kreis(n, x, y, max(r, 1.0), g * (1.0 if i_ == 0 else 0.7), rand_m=rand, flecken=0.3, flecken_m=4.0)

    for a, b, biom in segmente:
        lin = pr.polylinie(a, b, 2.0)
        Bm = float(np.max(breite_fn(np.linspace(a, b, 20))))
        band(zone("ufer_nah", biom), lin, Bm + 4.0)
        band(zone("bett_becken", biom), lin, Bm)
    for e in stufen:
        biom = e["biom"]
        if e["art"] == "fall":
            band(zone("bett_fels", biom), pr.polylinie(e["p"] - 1.5, e["p"] + e["l"] + 1.0, 0.5), e["B"] + 2.0)
            x, y = pr.xy(e["p"] + e["l"] + e["kolk"]["x_strahl"])
            kreis(zone("kolk", biom), x, y, e["kolk"]["radius"])
            r = gr.formel(rw.r["lagen"]["zonen"]["ufer_gischt"].get("radius_formel", "clamp(1.5 * D, 3, 25)"), D=e["D"])
            kreis(zone("ufer_gischt", biom), x, y, r)
        else:
            band(zone("bett_stufe", biom), pr.polylinie(e["p"] - 1.0, e["p"] + e["l"] + 1.0, 0.5), e["B"] + 2.0)
            if e["art"] != "schnelle":
                x, y = pr.xy(e["p"] + e["l"] + 0.4 * e["kolk"]["laenge"])
                kreis(zone("kolk", biom), x, y, e["kolk"]["radius"])
    for wz in wandzonen:
        g, namen = zone("wandfuss", wz["biom"])
        bf = gr.formel(rw.r["lagen"]["zonen"]["wandfuss"].get("breite_formel", "0.6 * wandhoehe"), wandhoehe=wz["hoehe"])
        for sg in (1.0, -1.0):
            band((g, namen), pr.versatz_linie(wz["a"], wz["b"], sg * (wz["versatz"] - bf / 2.0), 2.0), bf)
        if wz["grund"].startswith("Klamm"):
            band(zone("bett_fels", wz["biom"]), pr.polylinie(wz["a"], wz["b"], 2.0), wz["sohle"])


# ======================================================================================================================
# Effekte
# ======================================================================================================================
def bauen_effekte(K, pr, stufen, breite_fn):
    from sehens_lib import instanzen as ins
    rw, inv = K["rw"], K["inv"]
    gz = gr.effekt_grenzen(rw)
    ref = rw.r["effekte"].get("skala_referenz_m") or {}
    eins = rw.r["effekte"].get("einstellungen") or {}
    kand = []
    zaehler = {}
    for e in stufen:
        ea = gr.effekt_art(rw, e["art"], e["D"])
        if ea is None:
            continue
        a = ea["art"]
        n_art = zaehler.get(a, 0)
        zaehler[a] = n_art + 1
        hf = str(ea.get("haeufigkeit", ""))
        systeme = list(ea.get("systeme") or [])
        opt = list(ea.get("optional") or [])
        if a == "schnelle" and "2." in hf and n_art % 2 == 1:
            continue
        if a == "stufe":
            r3 = n_art % 3
            if r3 == 2:
                continue
            systeme = systeme if r3 == 0 else (opt[:1] or systeme)
        if a == "fall_klein" and "2." in hf and n_art % 2 == 1 and e.get("abstand_vorher", 99) < 15.0:
            systeme = [s_ for s_ in systeme if "Waterfall" not in s_]
        B = e["B"]
        nb = ea.get("nach_breite") or ea.get("wenn_B_ab") or {}
        for i_s, sys_ in enumerate(systeme[:gz["je_stufe"]] + ([] if len(systeme) >= gz["je_stufe"] else opt[:gz["je_stufe"] - len(systeme)])):
            name = sys_.rsplit("/", 1)[-1]
            if "Stream" in name and nb:
                for b_ab, ers in sorted(((float(k), v) for k, v in nb.items())):
                    if B >= b_ab:
                        sys_, name = ers, ers.rsplit("/", 1)[-1]
            fl = kompass(*pr.tang(e["p"]))
            ko = e.get("kolk") or {"x_strahl": 0.0, "radius": B / 2.0}
            if "Waterfall" in name:
                s_pos, z = e["p"] + 0.2, e["u"] + 0.05
                rolle = "fall"
            elif "Impact" in name:
                s_pos = e["p"] + e["l"] + (ko["x_strahl"] if e["art"] == "fall" else 0.4)
                z, rolle = e["d"] + 0.10, "aufprall"
            elif "Wake" in name:
                s_pos = e["p"] + e["l"] + ko["x_strahl"] + (4.0 if "Medium" in name or "Large" in name else 2.0)
                z, rolle = e["d"] + 0.03, "wake"
            else:
                if e["art"] == "stufe":
                    s_pos, z = e["p"] - 1.0, e["u"] + 0.10
                else:
                    s_pos = e["p"] + 0.5 * e["l"]
                    z = 0.5 * (e["u"] + e["d"]) + 0.10
                rolle = "stroemung"
            x, y = pr.xy(s_pos)
            groesse = name.rsplit("_", 1)[-1]
            if "Waterfall" in name:
                rb = (ref.get("waterfall") or {}).get(groesse, [3, 5])[0]
                sk = B / float(rb)
            elif "Stream" in name:
                rb = (ref.get("stream") or {}).get(groesse, [2, 5])[0]
                sk = B / float(rb)
            else:
                rd = float((ref.get("impact_wake_durchmesser") or {}).get(groesse, 3))
                sk = min(2.0 * ko["radius"], B * 1.2) / rd
            sk = float(np.clip(sk, 0.5, 2.0))
            cull = ea.get("cull", gz["cull"][0])
            if isinstance(cull, list):
                cull = cull[min(i_s, len(cull) - 1)]
            pfad = inv.niagara_pfad(sys_) or sys_
            kand.append({"typ": "niagara", "asset": pfad, "pos_cm": [round(x * 100), round(y * 100), round(z * 100)],
                         "rot_q": [round(v, 5) for v in ins.q_yaw_kompass(fl)], "kompass_grad": _r(fl),
                         "skala": round(sk, 2), "cull_m": float(cull), "sort_priority": int(eins.get("sort_priority", 2)),
                         "cast_shadow": bool(eins.get("cast_shadow", False)), "optional": False,
                         "stufe": e["id"], "rolle": rolle, "effekt_art": a,
                         "zweck": "%s an %s (%s %.1f m)" % (rolle, e["id"], e["art"], e["D"]), "_prio": -e["D"],
                         "_s": s_pos})
    # gleichzeitig <= gz['gleichzeitig']: Proben alle 2 m entlang des Laufs, Faelle zuerst
    kand.sort(key=lambda d: (d["_prio"], d["stufe"], d["rolle"]))
    if not kand:
        return [], 0
    s_min = min(d["_s"] for d in kand) - 60
    s_max = max(d["_s"] for d in kand) + 60
    ps = np.arange(max(0.0, s_min), min(pr.s[-1], s_max) + 1e-6, 2.0)
    px = np.interp(ps, pr.s, pr.x)
    py = np.interp(ps, pr.s, pr.y)
    zahl = np.zeros(len(ps), int)
    out = []
    weg = 0
    je_stufe = {}
    for d in kand:
        x, y = d["pos_cm"][0] / 100.0, d["pos_cm"][1] / 100.0
        nah = np.hypot(px - x, py - y) <= d["cull_m"]
        if (nah.any() and zahl[nah].max() >= gz["gleichzeitig"]) or je_stufe.get(d["stufe"], 0) >= gz["je_stufe"]:
            weg += 1
            continue
        zahl[nah] += 1
        je_stufe[d["stufe"]] = je_stufe.get(d["stufe"], 0) + 1
        out.append({k: v for k, v in d.items() if not k.startswith("_")})
    for d in out:
        for st_, txt in inv.asset_pruefen("niagara", d["asset"], False):
            K["melde"](st_, txt)
    out.sort(key=lambda d: (d["stufe"], d["rolle"]))
    return out, weg


# ======================================================================================================================
# Kameras (SEHENS_FORMAT §8): _vorher/_nachher von unten auf die groesste Stufe, _weg_vorher/_nachher vom Weg
# ======================================================================================================================
def bauen_kameras(K, pr, sid, stufen, breite_fn, stempel_liste):
    from sehens_lib import sicht, daten
    from sehens_lib import format as sfmt
    welt, gel, wp = K["welt"], K["gel"], K["wp"]
    kand = [e for e in stufen if e["art"] != "schnelle"] or stufen
    if not kand:
        return []
    e = max(kand, key=lambda e: (e["D"], -e["p"]))
    sz = e["p"] + e["l"]
    zx, zy = pr.xy(sz)
    zz = 0.5 * (e["u"] + e["d"])
    fl = kompass(*pr.tang(e["p"]))
    feld = daten.feld_von_m(zx, zy)

    def stempel_ok(x, y):
        for st in stempel_liste:
            x0, y0, x1, y1 = st.fe.grenzen_m()
            if x0 <= x <= x1 and y0 <= y <= y1:
                from sehens_lib.stempel import _bilinear_fenster
                if abs(float(_bilinear_fenster(st.delta, st.fe, welt, x, y, 0.0))) > 0.3:
                    return False
        return True

    hl = sicht.beste_blickposition(welt, zx, zy, max(e["D"], 2.0), r_min_m=max(12.0, 2.0 * e["B"]),
                                   r_max_m=max(60.0, 6.0 * e["B"]), gel=gel, bevorzugt_grad=(fl + 180.0) % 360.0,
                                   anzahl=12)
    kams = []
    lin = np.asarray(pr.polylinie(max(0.0, sz - 80), min(pr.s[-1], sz + 80), 2.0))
    for h in hl:
        dmin = float(np.min(np.hypot(lin[:, 0] - h["x_m"], lin[:, 1] - h["y_m"])))
        if dmin >= e["B"] / 2.0 + 5.0 and stempel_ok(h["x_m"], h["y_m"]):
            for nm in ("vorher", "nachher"):
                kams.append(sfmt.kamera(feld, h["x_m"] * 100, h["y_m"] * 100, zx * 100, zy * 100, zz * 100,
                                        "%s_%s" % (sid, nm), -170))
            break
    # vom Weg/Pfad (so sieht der Spieler die Strecke)
    idx, d = wp.im_ring(zx, zy, 15.0, 250.0)
    if idx.size:
        an, _, dd = sicht.sichtanteil(welt, wp.x_m[idx], wp.y_m[idx], zx, zy, max(e["D"], 2.0))
        sc = an - 0.0015 * dd
        k = int(np.argmax(sc))
        if an[k] >= 0.3:
            for nm in ("weg_vorher", "weg_nachher"):
                kams.append(sfmt.kamera(feld, wp.x_m[idx[k]] * 100, wp.y_m[idx[k]] * 100, zx * 100, zy * 100, zz * 100,
                                        "%s_%s" % (sid, nm), -170))
    return kams


# ======================================================================================================================
# Epic-Flussstuecke
# ======================================================================================================================
def bauen_flussstuecke(pr, sp, stufen, breite_fn, lauf_id, ramp_s):
    """Teilung an jeder Zwei-Punkt-Stufe (stufe/fall) und jeder Kaskade: oberes Stueck endet 0,5 m hinter der Kante
    (Spiegel der Lippe), unteres beginnt >= 1,2 m danach (C2-Regel). Rueckgabe (stuecke, luecken, meldungen)."""
    trenn = []
    for e in sorted(stufen, key=lambda e: e["p"]):
        if e["art"] == "schnelle":
            continue
        teile = e.get("teil") or [{"p": e["p"], "l": e["l"]}]
        ende_stufe = teile[-1]["p"] + teile[-1]["l"]
        trenn.append({"stufe": e["id"], "p": e["p"], "u": e["u"], "ende": ende_stufe,
                      "luecke": TEIL["luecke_start_m"]})
    meld = []
    for runde in range(12):
        grenzen = []
        a = 0.0
        for t in trenn:
            ob = t["p"] + TEIL["ende_hinter_kante_m"]
            un = max(t["ende"] + 0.3, ob + t["luecke"])
            grenzen.append((a, ob, t))
            a = un
        grenzen.append((a, pr.s[-1], None))
        stuecke = []
        for n, (a, b, t) in enumerate(grenzen):
            if b - a < 1.0:
                meld.append(("FEHLER", "Flussstueck %d zu kurz (%.1f m)" % (n, b - a)))
            ss = [a] + [s_ for s_, _, _ in sp if a + 0.05 < s_ < b - 0.05] + [b]
            dicht = [ss[0]]
            for s_ in ss[1:]:
                nseg = max(1, int(math.ceil((s_ - dicht[-1]) / TEIL["max_segment_m"])))
                for m in range(1, nseg + 1):
                    dicht.append(dicht[-1] + (s_ - dicht[-1]) * m / nseg if m < nseg else s_)
            dicht = sorted(set(round(v, 3) for v in dicht))
            pts = []
            for s_ in dicht:
                x, y = pr.xy(s_)
                z = float(spiegel_bei(sp, s_))
                if t is not None and s_ >= b - 1e-3:
                    z = t["u"]                                     # Zunge: Spiegel der Lippe bis 0,5 m hinter die Kante
                k = pr.i(s_)
                in_rampe = any(r0 - 1e-3 <= s_ <= r1 + 1e-3 for r0, r1 in ramp_s)
                geplant = abs(z - pr.z0[k]) > 0.01 or in_rampe
                v = TEIL["velocity_schnelle_cm_s"] if in_rampe else (TEIL["velocity_becken_cm_s"] if geplant else float(pr.v[k]))
                pts.append([round(x * 100, 1), round(y * 100, 1), round(z * 100, 1), round(float(breite_fn(s_)) * 100, 1),
                            round(float(pr.tiefe[k]) * 100, 1), round(v, 1)])
            zs = np.minimum.accumulate([p_[2] for p_ in pts])
            for p_, z_ in zip(pts, zs):
                p_[2] = round(float(z_), 1)
            stuecke.append({"id": "%s_T%02d" % (lauf_id, n), "s_m": [_r(a, 2), _r(b, 2)], "laenge_m": _r(b - a, 2),
                            "spiegel_m": [_r(pts[0][2] / 100.0, 2), _r(pts[-1][2] / 100.0, 2)],
                            "punkte": pts, "punkt_typen": ["CURVE"] + ["CURVE_CLAMPED"] * (len(pts) - 2) + ["CURVE"],
                            "nach_stufe": t["stufe"] if t else None})
        ueb = ueberlappungen(stuecke)
        if not ueb:
            break
        for i_, j_ in ueb:
            if j_ == i_ + 1 and i_ < len(trenn):
                trenn[i_]["luecke"] = min(trenn[i_]["luecke"] + 0.5, TEIL["luecke_max_m"])
    else:
        meld.append(("FEHLER", "Flussstuecke ueberlappen nach 12 Runden: %s" % ueberlappungen(stuecke)))
    luecken = []
    for n in range(len(stuecke) - 1):
        a, b = stuecke[n], stuecke[n + 1]
        luecken.append({"oben": a["id"], "unten": b["id"], "stufe": a["nach_stufe"],
                        "luecke_entlang_m": _r(b["s_m"][0] - a["s_m"][1], 2),
                        "luecke_m": _r(math.hypot((b["punkte"][0][0] - a["punkte"][-1][0]) / 100.0,
                                                  (b["punkte"][0][1] - a["punkte"][-1][1]) / 100.0), 2)})
    return stuecke, luecken, meld


def streifen_polygone(punkte_cm):
    """Draufsicht eines Flussstuecks als Folge von Vierecken (m)."""
    P = np.asarray(punkte_cm, np.float64)
    xy = P[:, :2] / 100.0
    br = P[:, 3] / 200.0
    out = []
    for k in range(len(P) - 1):
        d = xy[k + 1] - xy[k]
        L = max(float(np.hypot(*d)), 1e-6)
        nx, ny = -d[1] / L, d[0] / L
        a, b = xy[k], xy[k + 1]
        out.append([(a[0] + nx * br[k], a[1] + ny * br[k]), (b[0] + nx * br[k + 1], b[1] + ny * br[k + 1]),
                    (b[0] - nx * br[k + 1], b[1] - ny * br[k + 1]), (a[0] - nx * br[k], a[1] - ny * br[k])])
    return out


def ueberlappungen(stuecke, zelle=0.25):
    """Paare (i, j) von Stuecken, deren Draufsichten sich ueberlappen (Raster 0,25 m)."""
    from PIL import Image, ImageDraw
    polys = [streifen_polygone(s["punkte"]) for s in stuecke]
    alle = [p for ps in polys for q in ps for p in q]
    if not alle:
        return []
    x0 = min(p[0] for p in alle) - 1
    y0 = min(p[1] for p in alle) - 1
    x1 = max(p[0] for p in alle) + 1
    y1 = max(p[1] for p in alle) + 1
    W, H = int((x1 - x0) / zelle) + 2, int((y1 - y0) / zelle) + 2
    besitz = np.full((H, W), -1, np.int32)
    out = set()
    for i, ps in enumerate(polys):
        img = Image.new("1", (W, H), 0)
        dr = ImageDraw.Draw(img)
        for q in ps:
            dr.polygon([((x - x0) / zelle, (y - y0) / zelle) for x, y in q], fill=1)
        m = np.array(img, bool)
        if not m.any():
            continue
        # Rand eine Zelle schrumpfen (Rasterfehler an Kanten)
        m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
        alt = besitz[m]
        for j in np.unique(alt[alt >= 0]):
            out.add((int(j), i))
        besitz[m & (besitz < 0)] = i
    return sorted(out)
