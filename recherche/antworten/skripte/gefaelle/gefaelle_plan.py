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
  6. Gelaende (Delta): Bett = Spiegel - max(Tiefe, 0,5 m), Lippe als Krone, Kolk je Stufe, Uferboeschung; steil
     (Uferklippe/Klamm) wo ufer_klippen.wann / klamm.wann; Uferwulst (Spiegel + 0,15 m, hoechstens 1 m anheben) fuer
     die 14b-Pruefung 'Ufer am Netzrand'; Schutz an Wegen (4 + 4 m), Orten, anderem Wasser (3 m), Rand 0.
  7. Netze je Biom am Stufenort (biome.<biom>.netze): Riegel/Lippe/Holz, Fallwand, Uferwaende, Sturzbloecke,
     Beckenbloecke, Wandschutt, Kies, Moos (Kontakt).
  8. Lagen (lagen.zonen + biome.<biom>.lagen), Effekte (effekte, <= 3 je Stufe, <= 6 gleichzeitig; unter 3 m nur
     NS_Waterfall_Small + NS_Impact_Small, Koordinator/14b), Kameras _vorher/_nachher (+ _weg_vorher/_nachher,
     Augenhoehe -170) fuer Pilot-Strecken.
  9. Wasser (Befund 14b, Variante A verbindlich): wasser_koerper = Epic-River ober-/unterhalb jeder Stufenstrecke
     + Kaskadennetz (statisches SLW-Netz) dazwischen, 0,5 m Ueberlappung; keine Flussstuecke mit Luecken, keine
     Schaumscheiben. --variante C gibt zusaetzlich den gestuften Einzelspline + eigene Bach-Zone aus.

Aufruf (python -I, NumPy + Pillow):
  python -I gefaelle_plan.py [--laeufe ID ...] [--strecken ID ...] [--alle] [--daten2m DIR] [--aus DIR] [--bild]
                             [--bild-ordner DIR] [--variante A|C] [--ohne-pruefung]
  Ohne --laeufe/--strecken/--alle: alle Laeufe der 20 Pilot-Strecken aus prioritaet.json.
  Ohne --daten2m: 1-m-Originale aus <basis>/export/unreal/welt, Ausgabe <basis>/export/unreal/welt/gefaelle/<lauf>/.
  Cloud-Test: --daten2m recherche/vorlagen/daten/sehens --aus <scratchpad>/a15/plan
Ausgabe je Lauf (<aus>/<lauf>/): plan.json (spiegel_neu_cm, stufen, wasser_koerper, abschnitte, effekte, kameras),
  gelaende/<abschnitt>.f32, lagen/<abschnitt>_<Lage>.r8,
  instanzen/<Feld>/plan.json + <Netz>.f32 (FORMAT.md §3, Ebene 'gefaelle'); --bild: test_<strecke>.png je Pilot-Strecke.
Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.
Quellen: auftraege/15-gefaelle-felsstufen-klippen.md, antworten/15-gefaelle-regelwerk.md, vorlagen/SEHENS_FORMAT.md
  §3/§6/§8/§9, vorlagen/FORMAT.md §3, antworten/14b-befund-geteilte-baeche.md (Kaskadennetz), sehens_lib.
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
# Epic-River-Punkte (Tempo wie C2, vorlagen/daten/wasser_fx/stufen_fluss_teile.json["regel"])
TEIL = {"velocity_becken_cm_s": 80.0, "velocity_schnelle_cm_s": 300.0, "max_segment_m": 5.0}
NIAGARA_KLEIN = {"D_min": 0.8, "D_max": 3.0, "systeme": ["/Game/NatureWaterFX/FX/NS_Waterfall_Small",
                                                          "/Game/NatureWaterFX/FX/NS_Impact_Small"],
                 "quelle": "Koordinator 11.10. (Befund 14b): kleine Stufen < ~3 m mit Nature Water FX statt Vorhang-Netz"}
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

    markiere(gel.abstand_weg[i, j] <= 4.0 + 4.0 + B / 2.0 + 2.0, "Weg/Pfad")      # = Stempelschutz 4 m + 4 m
    markiere(gel.abstand_ort[i, j] <= 5.0 + 4.0 + B / 2.0 + 2.0, "Ort")
    try:
        markiere(gel.abstand_stadt[i, j] <= 20.0, "Stadt")
    except Exception:  # noqa: BLE001 - Stadtabstand optional (keine Staedte in den Daten)
        pass
    m = np.zeros(len(idx), bool)
    for o in orte:   # Schutzradius wie schutz_orte (Radius + 10 m + 8 m Uebergang) + halbe Breite
        m |= np.hypot(x - o["x_m"], y - o["y_m"]) <= o["radius_m"] + 10.0 + 8.0 + B / 2.0
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
    # fremdes Wasser im Raster (karte_wasser > 0, nicht dieser Lauf): Schutz wuerde den Bettaushub dort abschneiden
    from sehens_lib import gelaende as gel_mod, stempel as stm
    Bmax = float(B.max())
    fe = welt.fenster_box(float(x.min()) - 25, float(y.min()) - 25, float(x.max()) + 25, float(y.max()) + 25)
    wm = fe.get("wasser") > 0
    if wm.any():
        X, Y = fe.gitter_m()
        lin = np.stack([pr.x[max(0, idx[0] - 40):idx[-1] + 40], pr.y[max(0, idx[0] - 40):idx[-1] + 40]], axis=1)[::4]
        dl, _, _ = stm.polylinie_abstand(X[wm], Y[wm], lin)
        fremd = np.zeros(wm.shape, bool)
        fremd[wm] = dl > Bmax / 2.0 + 3.0
        if fremd.any():
            df = gel_mod.abstand(fremd, welt.zelle_m, 40.0)
            fi, fj = fe.lokal(x, y)
            fi = np.clip(np.rint(fi).astype(int), 0, df.shape[0] - 1)
            fj = np.clip(np.rint(fj).astype(int), 0, df.shape[1] - 1)
            markiere(df[fi, fj] <= 4.0 + 4.0 + B / 2.0 + 10.0, "fremdes Wasser (Raster)")
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


def andere_gewaesser(lauf_id, pr, wasser_welt, baeche):
    """Polylinien (m) anderer Fluesse/Baeche und Seeumrisse im Umfeld des Laufs (Zufluesse -> feste Zonen)."""
    bx = (pr.x.min() - 60, pr.x.max() + 60, pr.y.min() - 60, pr.y.max() + 60)
    out = []
    quellen = [(f["id"], f["punkte"]) for f in (wasser_welt.get("fluesse") or [])] + [(b["id"], b["punkte"]) for b in baeche]
    for oid, pk in quellen:
        if oid == lauf_id or not pk or len(pk) < 2:
            continue
        P = np.asarray(pk, np.float64)[:, :2] / 100.0
        if P[:, 0].max() < bx[0] or P[:, 0].min() > bx[1] or P[:, 1].max() < bx[2] or P[:, 1].min() > bx[3]:
            continue
        out.append(P)
    for s_ in wasser_welt.get("seen") or []:
        P = np.asarray(s_.get("umriss") or [[0, 0]], np.float64)[:, :2] / 100.0
        if len(P) >= 3 and not (P[:, 0].max() < bx[0] or P[:, 0].min() > bx[1] or P[:, 1].max() < bx[2] or P[:, 1].min() > bx[3]):
            out.append(np.vstack([P, P[:1]]))
    return out


def planbarer_anteil(lauf, welt, gel, orte, umbau, wasser_welt, baeche, s0, s1):
    """Laenge (m) der Strecke ausserhalb der festen Zonen (Wege, Orte, Sehenswuerdigkeiten, Umbau, Zufluesse)."""
    pr = Profil(lauf)
    fix, gruende = feste_zonen(pr, welt, gel, orte, umbau, andere_gewaesser(lauf.id, pr, wasser_welt, baeche), s0, s1)
    m = (pr.s >= s0) & (pr.s <= s1)
    return float((~fix[m]).sum() * DS), gruende


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
        elif "kaskade" in arten and D0 >= rw.art_bereich("kaskade")[0]:
            art = "kaskade"                       # kleiner als eine Blockstufe -> Kaskade (Teilstufe)
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
        if art == "stufe" and D > rw.art_bereich("stufe")[1] + 1e-6:
            if "kaskade" in arten:
                art = "kaskade"                   # zu hoch fuer eine Blockstufe -> Teilstufen
            elif "fall" in arten:
                art = "fall"
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
        for e in out:
            if e["art"] == "kaskade":
                self._teilstufen_teilen(e, k_hi)
        return out

    def _teilstufen_teilen(self, e, k_hi):
        """Teilstufen ueber kaskade.D_max in n gleiche Teilstufen im Abstand stufen.abstand_L_kaskade teilen."""
        rw = self.rw
        neu = []
        for n_t, t in enumerate(e["teil"]):
            if t["D"] <= k_hi + 1e-6:
                neu.append(t)
                continue
            # verfuegbare Laenge bis zur naechsten Teilstufe bzw. bis zur naechsten Lippe
            nxt = e["teil"][n_t + 1]["p"] if n_t + 1 < len(e["teil"]) else e["q"]
            pr, gb = self.pr, e["gb"]
            z_nxt = pr.zi(nxt)
            gewaehlt = None
            for n in range(int(math.ceil(t["D"] / (0.95 * k_hi))), 7):
                Dt = t["D"] / n
                # Teil-Lippen dort, wo der alte Spiegel um i*Dt gefallen ist -> neuer Spiegel nie ueber dem alten
                ps = [t["p"]] + [float(np.interp(-(t["u"] - i * Dt), -pr.z0, pr.s)) for i in range(1, n)]
                ok = all(ps[i] - ps[i - 1] >= t["l"] + 0.5 for i in range(1, n)) and nxt - ps[-1] >= t["l"] + 0.5
                if not ok:
                    continue
                teile, u = [], t["u"]
                for i in range(n):
                    if i < n - 1:
                        d = u - Dt
                    else:
                        d = z_nxt + gb * (nxt - ps[i] - t["l"])
                    teile.append({"p": ps[i], "u": u, "d": d, "D": u - d, "l": t["l"]})
                    if i < n - 1:
                        u = d - gb * (ps[i + 1] - ps[i] - t["l"])
                if all(0.0 < x_["D"] <= k_hi + 1e-6 for x_ in teile):
                    gewaehlt = teile
                    break
            neu += gewaehlt if gewaehlt else [t]
        e["teil"] = neu
        e["l"] = neu[-1]["p"] + neu[-1]["l"] - neu[0]["p"]
        e["d"] = neu[-1]["d"]


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
    rang = {"alt": 0, "becken": 1, "rampe": 2, "fuss": 2, "lippe": 3}
    for s_, z_, k_ in pkt:
        if out and abs(out[-1][0] - s_) < 1e-4:
            # gleicher Ort: Stufenpunkte (Lippe/Fuss) gehen vor alten Laufpunkten, Hoehe = Minimum
            k_neu = k_ if rang[k_] >= rang[out[-1][2]] else out[-1][2]
            out[-1] = (s_, min(z_, out[-1][1]), k_neu)
            continue
        if out and s_ - out[-1][0] < 0.25 and k_ == "alt" and out[-1][2] in ("lippe", "fuss", "rampe"):
            continue                                       # alter Laufpunkt direkt an einer Stufe: weglassen
        if out and s_ - out[-1][0] < 0.25 and out[-1][2] == "alt" and k_ in ("lippe", "fuss", "rampe"):
            out[-1] = (s_, min(z_, out[-1][1]), k_)
            continue
        out.append((s_, z_, k_))
    # alte Laufpunkte dicht (< 0,3 m) an Stufenpunkten entfernen (keine Mini-Segmente mit Scheingefaelle)
    stufig = ("lippe", "fuss", "rampe")
    out = [t for k, t in enumerate(out) if t[2] != "alt" or k in (0, len(out) - 1) or not (
        (k > 0 and out[k - 1][2] in stufig and t[0] - out[k - 1][0] < 0.3) or
        (k + 1 < len(out) and out[k + 1][2] in stufig and out[k + 1][0] - t[0] < 0.3))]
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
    core = 0.5 * Bw
    z_sp = spiegel_bei(sp, s)
    bett = z_sp - np.maximum(np.interp(s, pr.s, pr.tiefe), KN["bett_min_tiefe_m"])   # 14b: Bett >= 0,2 m im Mittel
    # Bett-Tiefe hinter dem Kaskadennetz bis zum Segmentende ausblenden (kein Absatz unter Wasser am Anschluss)
    st_seg = [e for e in stufen if seg_a - 1e-6 <= e["p"] <= seg_b + 1e-6]
    if st_seg:
        kn_ende = max((e.get("teil") or [e])[-1]["p"] + (e.get("teil") or [e])[-1]["l"] for e in st_seg) + \
            KN["nach_unten_m"] + KN["ueberlapp_m"] + 0.5
        lang = max(seg_b - kn_ende, 0.5)
        bett = np.where(s > kn_ende, z_sp - (z_sp - bett) * glatt01((seg_b - s) / lang), bett)
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
    # Uferwulst (14b, Pruefung 'Ufer am Rand ueber Spiegel'): ausserhalb der Wasserbreite mindestens Spiegel + 0,15 m
    # bis Netzrand + 0,6 m, dann 1:2 auslaufen - hebt nur, wo das alte Ufer zu niedrig ist
    wulst = z_sp + 0.15 - np.maximum(d - (half + KN["rand_ueberstand_m"] + 0.6), 0.0) * 0.5
    wulst = np.minimum(wulst, cur + 1.0)                       # hoechstens 1 m anheben (kein Damm ueber Rinnen)
    neu = np.where(innen & (d >= half), np.maximum(neu, wulst), neu)
    alt = st.delta[band]
    dn = neu - cur
    # mehrere Segmente im Fenster: Absenken - tiefster Wert gilt; Wulst - hoechster Wert, wo nichts abgesenkt wird
    st.delta[band] = np.where((alt < 0) | (dn < 0), np.minimum(alt, dn), np.maximum(alt, dn))
    korr = np.zeros(X.shape, bool)
    korr[band] = d <= np.maximum(half + 6.0, 8.0)          # eigenes Wasser (auch ausserhalb des Segments) nicht schuetzen
    st._lauf_maske = getattr(st, "_lauf_maske", np.zeros(X.shape, bool))
    st._lauf_maske[band] |= innen & (d <= half + 10.0)       # fuer die Senken-Pruefung (Becken/Kolke sind Wasser)
    return korr


def neue_senken(st, wasser, min_tiefe_m=0.3, min_flaeche_m2=8.0):
    """Geschlossene Senken, die der Stempel NEU erzeugt (Fuelltiefe nachher - vorher > min_tiefe), ausserhalb des
    Laufs (Becken/Kolke sind Wasser) und ausserhalb bestehenden Wassers."""
    from sehens_lib import gelaende as gel_mod
    z = st.z
    vor = st.h0.astype(np.float32)
    nach = (st.h0 + st.delta).astype(np.float32)
    leer = np.zeros(vor.shape, bool)
    t0 = gel_mod.abfluss(vor, z, leer)["gefuellt"] - vor
    t1 = gel_mod.abfluss(nach, z, leer)["gefuellt"] - nach
    m = (t1 - t0 > min_tiefe_m) & ~wasser & (st.fe.get("wasser") == 0)
    fl = float(m.sum() * z * z)
    return {"flaeche_m2": fl if fl >= min_flaeche_m2 else 0.0, "max_tiefe_m": float((t1 - t0)[m].max()) if m.any() else 0.0}


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
            netz, h = wand_netz(inv, N["wand"], e["D"] + 0.5 * ko["tiefe"] + 0.3, ctx_rng(ctx, "fw", k))
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
        netz, h = wand_netz(inv, N["wand"], float(np.clip(wz["hoehe"], 2.0, 40.0)), ctx_rng(ctx, "wz", wz["nr"]))
        info = inv.netz(netz)
        breite = info["groesse_m"][0] * h / max(info["groesse_m"][2], 0.1)
        lin_name = "wl_%02d" % wz["nr"]
        ctx.linien[lin_name] = pr.polylinie(wz["a"], wz["b"], 1.0)
        ueb = 0.5 * sum(K["klamm"]["ueberlappung"])
        h_soll = float(np.clip(wz["hoehe"], 2.0, 40.0))
        reihen = int(min(3, math.ceil(h_soll / max(h, 0.5) - 0.15)))      # hohe Waende: Netze uebereinander
        for r_ in range(max(1, reihen)):
            gruppe(ctx, {"name": nm if r_ == 0 else "%s_r%d" % (nm, r_ + 1), "ebene": "begleiter", "netz": netz, "rolle": "fels",
                         "verteilung": {"typ": "reihe", "punkte": lin_name, "abstand_m": max(2.0, breite * (1.0 - ueb)),
                                        "versatz_m": wz["versatz"] + 0.4 * r_, "versatz_streuung_m": 0.4,
                                        "seiten": ["links", "rechts"], "blick": "zur_linie", "front_an_linie": True},
                         "groesse_m": [h * 0.9, h * 1.05], "groesse_achse": "z", "front_achse": "+y", "ausrichtung": "aufrecht",
                         "z_bezug": "z:%.3f" % (wz["z_wasser"] - 0.3 + r_ * 0.85 * h), "akteur": True, "kollision": True,
                         "im_wasser": "egal", "meide": None, "weg_abstand_m": 4.0, "yaw_streuung_grad": 6.0,
                         "warum": "Uferwand %s (ufer_klippen/klamm), %.1f m hoch, Reihe %d" % (wz["grund"], h_soll, r_ + 1)})
        fels_gruppen += [nm] + ["%s_r%d" % (nm, r_ + 1) for r_ in range(1, max(1, reihen))]
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


def wand_netz(inv, liste, h, rng, max_skala=3.0):
    """Wandnetz fuer eine Wandhoehe h: bevorzugt stehende Netze (Hoehe >= 0,35 x Grundriss), deren Hoehe am
    besten passt; Massstab hoechstens max_skala (sonst wird die Wand niedriger). Rueckgabe (netz, hoehe_m)."""
    kand = []
    for n in liste:
        gx, gy, gz_ = inv.netz(n)["groesse_m"]
        if gz_ < 0.35 * max(gx, gy):
            continue
        kand.append((abs(math.log(max(h, 0.5) / (1.2 * max(gz_, 0.1)))), n, gz_))
    if not kand:
        kand = [(abs(math.log(max(h, 0.5) / max(inv.netz(n)["groesse_m"][2], 0.1))), n, inv.netz(n)["groesse_m"][2])
                for n in liste]
    kand.sort()
    _, n, gz_ = kand[int(rng.integers(min(3, len(kand))))]
    return n, float(min(h, max_skala * gz_))


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
        if a == "stufe" and not (NIAGARA_KLEIN["D_min"] <= e["D"] < NIAGARA_KLEIN["D_max"]):
            r3 = n_art % 3
            if r3 == 2:
                continue
            systeme = systeme if r3 == 0 else (opt[:1] or systeme)
        if a == "fall_klein" and "2." in hf and n_art % 2 == 1 and e.get("abstand_vorher", 99) < 15.0:
            systeme = [s_ for s_ in systeme if "Waterfall" not in s_]
        B = e["B"]
        nb = ea.get("nach_breite") or ea.get("wenn_B_ab") or {}
        klein = e["art"] in ("stufe", "kaskade", "fall") and NIAGARA_KLEIN["D_min"] <= e["D"] < NIAGARA_KLEIN["D_max"]
        if klein:
            # Koordinator 14b (11.10.): an kleinen Stufen Nature Water FX statt eigenem Vorhang-Netz
            systeme, opt = list(NIAGARA_KLEIN["systeme"]), []
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
            cull = ea.get("cull", gz["cull"][0]) if not klein else gz["cull_klein"]
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
    ps = np.arange(max(0.0, s_min), min(pr.s[-1], s_max) + 1e-6, 1.0)
    px = np.interp(ps, pr.s, pr.x)
    py = np.interp(ps, pr.s, pr.y)
    zahl = np.zeros(len(ps), int)
    out = []
    weg = 0
    je_stufe = {}
    for d in kand:
        x, y = d["pos_cm"][0] / 100.0, d["pos_cm"][1] / 100.0
        nah = np.hypot(px - x, py - y) <= d["cull_m"] + 2.0     # Reserve gegen andere Probenlagen im Pruefer
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
                                   r_max_m=max(90.0, 6.0 * e["B"]), gel=gel, bevorzugt_grad=(fl + 180.0) % 360.0,
                                   anzahl=40, n_ringe=8)
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
# Wasserkoerper (Befund 14b, Variante A verbindlich): River ober-/unterhalb + Kaskadennetz in der Stufenstrecke
# ======================================================================================================================
KN = {"material": "/Game/Eldarien/Welt/Wasser/Stufenfall/MI_EL_Kaskade_SLW", "rand_ueberstand_m": 0.4, "zelle_m": 0.5,
      "ueberlapp_m": 0.5, "unter_river_cm": 2, "v_kante_m_s": 2.4, "bogen_x_m": 0.45, "bogen_punkte": 3,
      "abstand_bett_wand_cm": 20, "fuss_unter_spiegel_m": 0.3, "bett_unter_spiegel_min_m": 0.2,
      "ufer_ueber_spiegel_am_rand_m": 0.1, "tempo": {"becken": 80, "lippe": 240, "bogen": 300, "wand": 300, "fuss": 150,
                                                       "rampe": 300},
      "vorhang_ab_m": 3.0, "nach_unten_m": 1.0, "bett_min_tiefe_m": 0.5,
      "quelle": "antworten/14b-befund-geteilte-baeche.md Abschnitt 3 (Empfehlung A) und 4, Entscheidungen Koordinator"}


_ZELLE = [1.0]


def RASTER_ZUSCHLAG():
    """Pruef-Zuschlag fuer die Rasterweite: 0 auf 1-m-Daten, 1 m auf 2-m-Daten (ein 4-m-Bach ist dort 2 Zellen breit;
    die bilineare Abfrage verschmiert Bett und Ufer). Lokal auf 1 m gilt die Pruefung streng."""
    return max(_ZELLE[0] - 1.0, 0.0)


def raster_stufe(n_fehl, n_ges, zuschlag=None):
    """FEHLER; auf grobem Raster (2 m) WARNUNG, wenn hoechstens 1 Punkt bzw. 10 % betroffen sind (Rasterverschmierung
    an kurzen Kaskadenbecken) - lokal auf 1 m gilt streng FEHLER."""
    z = RASTER_ZUSCHLAG() if zuschlag is None else zuschlag
    return "WARNUNG" if z > 0 and n_fehl <= max(1, int(0.1 * n_ges)) else "FEHLER"


def raster_text(n_fehl, n_ges, zuschlag=None):
    return " (2-m-Raster: lokal auf 1 m pruefen)" if raster_stufe(n_fehl, n_ges, zuschlag) == "WARNUNG" else ""


def nahe_stufe(mitte, knick, zuschlag):
    """True fuer Beckenpunkte, die auf grobem Raster (zuschlag > 0) naeher als 1,5 x Zelle an einer Lippe/einem Fuss
    liegen: dort mischt die bilineare Abfrage Ober- und Unterwasser (2-m-Naeherung; auf 1 m wird alles geprueft)."""
    if zuschlag <= 0:
        return [False] * len(mitte)
    M = np.asarray(mitte, np.float64)[:, :2] / 100.0
    s = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(M, axis=0).T))])
    st = s[[k for k, r in enumerate(knick) if r in ("lippe", "fuss")]]
    grenze = 1.5 * (zuschlag + 1.0)
    return [bool(st.size and np.min(np.abs(st - s[k])) < grenze) for k in range(len(mitte))]


def river_punkte(pr, sp, a, b, breite_fn):
    ss = [a] + [s_ for s_, _, _ in sp if a + 0.05 < s_ < b - 0.05] + [b]
    dicht = [ss[0]]
    for s_ in ss[1:]:
        nseg = max(1, int(math.ceil((s_ - dicht[-1]) / TEIL["max_segment_m"])))
        basis = dicht[-1]
        for m in range(1, nseg + 1):
            dicht.append(basis + (s_ - basis) * m / nseg)
    pts = []
    for s_ in dicht:
        x, y = pr.xy(s_)
        k = pr.i(s_)
        z = float(spiegel_bei(sp, s_))
        geplant = abs(z - pr.z0[k]) > 0.01
        v = TEIL["velocity_becken_cm_s"] if geplant else float(pr.v[k])
        pts.append([round(x * 100, 1), round(y * 100, 1), round(z * 100, 1), round(float(breite_fn(s_)) * 100, 1),
                    round(float(pr.tiefe[k]) * 100, 1), round(v, 1)])
    zs = np.minimum.accumulate([p_[2] for p_ in pts])
    for p_, z_ in zip(pts, zs):
        p_[2] = round(float(z_), 1)
    return pts


def kn_bereiche(pr, stufen, segmente):
    """Stufenstrecken: je Segment von der ersten Lippe bis Fuss der letzten Stufe + nach_unten + Ueberlappung."""
    bereiche = []
    for sa, sb in sorted(segmente):
        st = sorted([e for e in stufen if sa - 1e-6 <= e["p"] <= sb + 1e-6], key=lambda e: e["p"])
        if not st:
            continue
        a = st[0]["p"]
        ende = max((e.get("teil") or [e])[-1]["p"] + (e.get("teil") or [e])[-1]["l"] for e in st)
        b = min(float(pr.s[-1]), ende + KN["nach_unten_m"] + KN["ueberlapp_m"])
        if bereiche and a - bereiche[-1][1] < 2.0 * KN["ueberlapp_m"] + 1.0:
            bereiche[-1] = (bereiche[-1][0], b, bereiche[-1][2] + st)          # zu kurzer River dazwischen: zusammen
        else:
            bereiche.append((a, b, st))
    return bereiche


def bauen_wasser_A(pr, sp, stufen, segmente, breite_fn, lauf_id, boden_fn, melde):
    """Variante A (14b, verbindlich): je Stufenstrecke ein Kaskadennetz (statisches SLW-Netz) von der ersten Lippe bis
    1,5 m hinter den Fuss der letzten Stufe; Epic-River nur ober- und unterhalb, 0,5 m Ueberlappung, Netz 2 cm unter
    dem River (Bauhinweis). z der Mittellinie = spiegel_neu_cm (+ Ueberfallbogen an den Stufen)."""
    g = 9.81
    bereiche = kn_bereiche(pr, stufen, segmente)
    grenzen = [0.0]
    for a, b, _ in bereiche:
        grenzen += [a + KN["ueberlapp_m"], b - KN["ueberlapp_m"]]
    grenzen.append(float(pr.s[-1]))
    rivers = []
    for k in range(0, len(grenzen), 2):
        ra, rb = grenzen[k], grenzen[k + 1]
        if rb - ra < 0.5:
            continue
        pts = river_punkte(pr, sp, ra, rb, breite_fn)
        rivers.append({"id": "%s_R%d" % (lauf_id, len(rivers)), "typ": "river", "s_m": [_r(ra, 2), _r(rb, 2)],
                       "punkte": pts, "punkt_typen": ["CURVE"] + ["CURVE_CLAMPED"] * (len(pts) - 2) + ["CURVE"],
                       "zone": "<Feld>_Wasserzone", "overlap_material_priority": 0})
    kns = []
    for n, (a, b, st) in enumerate(bereiche):
        mitte, knick = [], []
        pkt = [(s_, z_, k_) for s_, z_, k_ in sp if a - 1e-6 <= s_ <= b + 1e-6]
        if not pkt or pkt[-1][0] < b - 0.05:
            pkt.append((b, float(spiegel_bei(sp, b)), "becken"))
        auf = []                                                   # (s_aufprall, radius) fuer den Schaum
        for e in st:
            if e["art"] == "schnelle":
                continue
            for t in (e.get("teil") or [e]):
                xs_ = e.get("kolk", {}).get("x_strahl", 0.0) if e["art"] == "fall" else 0.3
                auf.append((t["p"] + t["l"] + xs_, float(np.clip(0.5 * t["D"] + 0.5, 1.0, 3.0))))

        def schaum(s_, rolle):
            if rolle in ("lippe", "bogen", "wand"):
                return 1.0
            if rolle == "rampe":
                return 0.5
            w = 0.0
            for sa_, r_ in auf:
                d_ = abs(s_ - sa_)
                w = max(w, 1.0 if d_ <= r_ else max(0.0, 1.0 - (d_ - r_) / 3.0))
            return round(w, 2)

        def punkt(s_, z_, rolle, abstand_bett_cm=None):
            x, y = pr.xy(s_)
            br = float(breite_fn(s_))
            if abstand_bett_cm is None:
                tx, ty = pr.tang(s_)
                off = np.linspace(-1, 1, 7) * max(0.45 * br - RASTER_ZUSCHLAG(), 0.15 * br)
                bett = float(np.mean(boden_fn(x + ty * off, y - tx * off)))
                abstand_bett_cm = (z_ - bett) * 100.0
            mitte.append([round(x * 100, 1), round(y * 100, 1), round(z_ * 100, 1), round(br * 100, 1),
                          KN["tempo"][rolle], 1.0 if rolle in ("bogen", "wand") else (0.5 if rolle == "rampe" else 0.0),
                          schaum(s_, rolle), round(abstand_bett_cm, 1)])
            knick.append(rolle)

        for k, (s_, z_, k_) in enumerate(pkt):
            rolle = {"alt": "becken", "becken": "becken", "lippe": "lippe", "fuss": "fuss", "rampe": "rampe"}[k_]
            if rolle == "fuss" and mitte and knick[-1] == "lippe":
                # Ueberfallbogen x = v t, z = -g t^2 / 2, dann Wandpunkt vor der Felswand, Fuss auf dem unteren Spiegel
                s_l, z_l = pkt[k - 1][0], pkt[k - 1][1]
                D = z_l - z_
                t_end = min(KN["bogen_x_m"] / KN["v_kante_m_s"], math.sqrt(2.0 * max(D, 0.01) / g))
                for i in range(1, KN["bogen_punkte"] + 1):
                    t_ = t_end * i / KN["bogen_punkte"]
                    punkt(s_l + KN["v_kante_m_s"] * t_, max(z_l - 0.5 * g * t_ * t_, z_), "bogen", KN["abstand_bett_wand_cm"])
                s_w = s_l + KN["v_kante_m_s"] * t_end
                z_b = mitte[-1][2] / 100.0
                if z_b - z_ > 0.3:
                    punkt(s_w, 0.5 * (z_b + z_), "wand", KN["abstand_bett_wand_cm"])
                punkt(max(s_, s_w), z_, "fuss", KN["abstand_bett_wand_cm"])
                continue
            punkt(s_, z_, rolle)
        zs = [q[2] for q in mitte]
        if any(zs[i + 1] > zs[i] + 1e-6 for i in range(len(zs) - 1)):
            melde("FEHLER", "Kaskadennetz %d: Mittellinie steigt" % n)
        # Pruefungen (a) Bett >= 0,2 m unter dem Spiegel (Becken), (b) Ufer am Rand >= 0,1 m ueber dem Spiegel
        n_bett = n_ufer = n_bk = 0
        nah_stufe = nahe_stufe(mitte, knick, RASTER_ZUSCHLAG())
        for q, rolle, ns_ in zip(mitte, knick, nah_stufe):
            if rolle != "becken" or ns_:
                continue
            n_bk += 1
            if q[7] < KN["bett_unter_spiegel_min_m"] * 100.0 - 0.5:
                n_bett += 1
        ss = [q for q, r_k, ns_ in zip(mitte, knick, nah_stufe) if r_k == "becken" and not ns_]
        for q in ss:
            k_ = mitte.index(q)
            q2 = mitte[k_ + 1] if k_ + 1 < len(mitte) else mitte[k_ - 1]
            t = np.array([q2[0] - q[0], q2[1] - q[1]], np.float64) * (1 if k_ + 1 < len(mitte) else -1)
            tx, ty = t / max(float(np.hypot(*t)), 1e-6)
            x, y = q[0] / 100.0, q[1] / 100.0
            r_ = q[3] / 200.0 + KN["rand_ueberstand_m"] + RASTER_ZUSCHLAG()
            hz = boden_fn(np.array([x + ty * r_, x - ty * r_]), np.array([y - tx * r_, y + tx * r_]))
            if float(np.min(hz)) < q[2] / 100.0 + KN["ufer_ueber_spiegel_am_rand_m"] - 5e-3:
                n_ufer += 1
        vorhang = [e["id"] for e in st if e["art"] != "schnelle" and e["D"] >= KN["vorhang_ab_m"] and not e.get("teil")]
        kn = {"id": "%s_KN%d" % (lauf_id, n), "typ": "kaskadennetz", "s_m": [_r(a, 2), _r(b, 2)],
              "mittellinie": mitte, "mittellinie_felder": ["x_cm", "y_cm", "z_cm", "breite_cm", "tempo_cm_s", "fallanteil",
                                                          "schaum", "abstand_bett_cm"],
              "knick": knick, "rand_ueberstand_m": KN["rand_ueberstand_m"], "zelle_m": KN["zelle_m"],
              "anfang_unter_river_cm": KN["unter_river_cm"], "ende_unter_river_cm": KN["unter_river_cm"],
              "fuss_unter_spiegel_m": KN["fuss_unter_spiegel_m"], "material": KN["material"],
              "nanite": False, "schatten": False, "kollision": "keine",
              "stufen": [e["id"] for e in st], "vorhang_an_stufen": vorhang,
              "pruefung": {"bett_unter_spiegel_min_m": KN["bett_unter_spiegel_min_m"],
                           "ufer_ueber_spiegel_am_rand_m": KN["ufer_ueber_spiegel_am_rand_m"],
                           "becken_punkte": n_bk, "bett_zu_flach": n_bett, "ufer_proben": int(len(ss)),
                           "ufer_zu_tief": n_ufer},
              "quelle": KN["quelle"]}
        kns.append(kn)
        if n_bett:
            melde(raster_stufe(n_bett, n_bk), "%s: Bett an %d von %d Beckenpunkten < %.1f m unter dem Spiegel%s"
                  % (kn["id"], n_bett, n_bk, KN["bett_unter_spiegel_min_m"], raster_text(n_bett, n_bk)))
        if n_ufer:
            melde(raster_stufe(n_ufer, len(ss)), "%s: Ufer am Netzrand an %d von %d Proben < %.1f m ueber dem Spiegel%s"
                  % (kn["id"], n_ufer, len(ss), KN["ufer_ueber_spiegel_am_rand_m"], raster_text(n_ufer, len(ss))))
    koerper = sorted(rivers + kns, key=lambda k_: k_["s_m"][0])
    for k_ in range(len(koerper) - 1):
        o, u = koerper[k_], koerper[k_ + 1]
        ue = _r(o["s_m"][1] - u["s_m"][0], 2)
        if o["typ"] == "river":
            o["anschluss_unten"] = {"an": u["id"], "ueberlapp_m": ue}
        else:
            u["anschluss_oben"] = {"an": o["id"], "ueberlapp_m": ue}
    return koerper


def wasser_C(pr, sp, stufen, breite_fn, lauf_id):
    """Variante C (nur mit --variante C): ein gestufter WaterBodyRiver + eigene Bach-Zone (14b Rueckfall C)."""
    pts, typen = [], []
    ramp = [(e["p"], e["p"] + e["l"]) for e in stufen if e["art"] == "schnelle"]
    for s_, z_, k_ in sp:
        x, y = pr.xy(s_)
        k = pr.i(s_)
        in_r = any(r0 - 1e-3 <= s_ <= r1 + 1e-3 for r0, r1 in ramp)
        geplant = abs(z_ - pr.z0[k]) > 0.01 or k_ != "alt"
        v = TEIL["velocity_schnelle_cm_s"] if (in_r or k_ in ("lippe", "fuss")) else \
            (TEIL["velocity_becken_cm_s"] if geplant else float(pr.v[k]))
        pts.append([round(x * 100, 1), round(y * 100, 1), round(z_ * 100, 1), round(float(breite_fn(s_)) * 100, 1),
                    round(float(pr.tiefe[k]) * 100, 1), round(v, 1)])
        typen.append("LINEAR" if k_ in ("lippe", "fuss", "rampe") else "CURVE_CLAMPED")
    typen[0] = typen[-1] = "CURVE"
    st = sorted(stufen, key=lambda e: e["p"])
    xs = [pr.xy(v)[0] for v in np.linspace(st[0]["p"], st[-1]["p"], 20)]
    ys = [pr.xy(v)[1] for v in np.linspace(st[0]["p"], st[-1]["p"], 20)]
    return {"variante": "gestufter_spline", "quelle": "14b Rueckfall C (nur auf Schalter --variante C)",
            "zone_neu": {"id": "%s_Bach_Wasserzone" % lauf_id,
                         "mitte_cm": [round(float(np.mean(xs)) * 100), round(float(np.mean(ys)) * 100)],
                         "ausdehnung_m": [round(float(np.ptp(xs)) + 20.0), round(float(np.ptp(ys)) + 20.0)],
                         "texel_m": 0.25, "half_precision": False, "overlap_priority": 10, "tile_size_cm": 1200},
            "river": {"id": "%s_GS" % lauf_id, "punkte": pts, "punkt_typen": typen, "shape_dilation_cm": 200}}


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


# ======================================================================================================================
# Ein Lauf
# ======================================================================================================================
def fels_funktion(K, pr):
    welt, gel, rw = K["welt"], K["gel"], K["rw"]
    fr = rw.fels_regel()
    from sehens_lib import daten
    codes = {daten.BODEN.index(n) for n in FELS_LAGEN if n in daten.BODEN}

    def f(s, S):
        x, y = pr.xy(s)
        tx, ty = pr.tang(s)
        B = pr.Bi(s)
        r = fr["radius"]
        px = np.array([x, x + r, x - r, x, x, x + ty * (B / 2 + 2), x - ty * (B / 2 + 2)])
        py = np.array([y, y, y, y + r, y - r, y - tx * (B / 2 + 2), y + tx * (B / 2 + 2)])
        i, j = welt.m_zu_ij(px, py)
        if any(int(c) in codes for c in welt.boden[i, j]):
            return True
        if float(np.max(gel.neigung[i[5:], j[5:]])) > fr["hang_grad"]:
            return True
        return welt.biom_bei_m(x, y) in fr["biome"] and S >= fr["S_fels"]
    return f


def eintiefung(K, pr, sp, s_arr):
    """Gelaende quer zum Lauf (B/2+1 ... 2B, je Seite das Maximum, dann das Minimum beider Seiten) ueber dem neuen
    Spiegel (ufer_klippen.wann / klamm.wann)."""
    welt = K["welt"]
    out = np.zeros(len(s_arr))
    for n, s in enumerate(s_arr):
        x, y = pr.xy(s)
        tx, ty = pr.tang(s)
        B = pr.Bi(s)
        off = np.linspace(B / 2.0 + 1.0, max(2.0 * B, B / 2.0 + 2.0), 5)
        hl = welt.hoehe_bei_m(x + ty * off, y - tx * off)
        hr = welt.hoehe_bei_m(x - ty * off, y + tx * off)
        out[n] = min(float(np.max(hl)), float(np.max(hr))) - float(spiegel_bei(sp, s))
    return out


def plane_lauf(lauf_id, K, strecken_ids=None):
    from sehens_lib import daten, instanzen, rezept, stempel as stm
    from sehens_lib import format as sfmt
    welt, gel, inv, rw = K["welt"], K["gel"], K["inv"], K["rw"]
    meldungen = []

    def melde(stufe, text):
        meldungen.append((stufe, lauf_id, text))
    K["melde"] = melde
    lauf = gd.Lauf.aus_welt(welt, lauf_id, K["baeche"], K["wasser_welt"])
    pr = Profil(lauf)
    fels_fn = fels_funktion(K, pr)
    st_l = [x for x in K["strecken"] if x["lauf"] == lauf_id and (strecken_ids is None or x["id"] in strecken_ids)]
    # andere Gewaesser im Umfeld
    bx = (pr.x.min() - 60, pr.x.max() + 60, pr.y.min() - 60, pr.y.max() + 60)
    andere = andere_gewaesser(lauf_id, pr, K["wasser_welt"], K["baeche"])
    orte_nah = [o for o in K["orte"] if bx[0] - 300 < o["x_m"] < bx[1] + 300 and bx[2] - 300 < o["y_m"] < bx[3] + 300]
    biom_netze = {}

    def netze(biom):
        if biom not in biom_netze:
            bn, b = rw.biom(biom)
            N = {k: netze_pruefen(inv, v, melde, "%s.%s" % (bn, k)) for k, v in b["netze"].items()}
            for k in ("lippe", "riegel", "bloecke", "wand", "schutt", "kies", "holz", "extra"):
                N.setdefault(k, [])
            biom_netze[biom] = (bn, N)
        return biom_netze[biom]

    hz = gr.holzstufe(rw)
    strecken_out, alle_stufen, segmente = [], [], []
    abschnitte = []
    for x in st_l:
        pe = K["prio"].get(x["id"], {})
        status = pe.get("status", "offen")
        eintrag = {"id": x["id"], "status": status, "rang": pe.get("rang"), "pilot": bool(pe.get("pilot")),
                   "s_m": [x["s0_m"], x["s1_m"]], "laenge_m": x["laenge_m"], "fall_m": x["hoehe_m"],
                   "gefaelle_mittel": x["gefaelle_mittel"], "gefaelle_max": x["gefaelle_max"]}
        if status not in PLANBAR:
            eintrag["hinweis"] = {"gebaut_stufen": "schon mit Stufen gebaut (Auftrag 12/14) - nur Feinschliff, nicht geplant",
                                  "umgebaut_von_sehens": "baut ein Sehens-Planer um - nicht doppelt geplant"}.get(status, status)
            strecken_out.append(eintrag)
            continue
        s0, s1 = x["s0_m"], x["s1_m"]
        fix, gruende = feste_zonen(pr, welt, gel, orte_nah, K["umbau"], andere, s0, s1)
        L = s1 - s0
        n_ab = max(1, int(math.ceil(L / 420.0)))
        grenzen_ab = [s0 + L * k / n_ab for k in range(n_ab + 1)]
        for k in range(1, n_ab):
            m = np.abs(pr.s - grenzen_ab[k]) <= 10.0
            fix[m] = True
            gruende.append((_r(grenzen_ab[k] - 10), _r(grenzen_ab[k] + 10), "Abschnittsgrenze (Fenster <= 600 m)"))
        frei = []
        ks = np.flatnonzero((pr.s >= s0) & (pr.s <= s1))
        st = None
        for k in ks:
            if not fix[k] and st is None:
                st = pr.s[k]
            if (fix[k] or k == ks[-1]) and st is not None:
                e_ = pr.s[k] if not fix[k] else pr.s[max(k - 1, 0)]
                anschl = max(2.0 * pr.Bi(st), 3.0)            # ablauf 1: Anschluss 2 B fix
                st2, e2 = max(float(st), anschl), min(float(e_), pr.s[-1] - max(2.0 * pr.Bi(e_), 3.0))
                if e2 - st2 >= 2.0 * gr.min_abstand_stufen(rw, pr.Bi(st2)):
                    frei.append((st2, e2))
                st = None
        rng = np.random.default_rng(abs(hash_stabil(SEED, x["id"])))
        leger = Stufenleger(rw, pr, welt, x["art"], rng, None, fels_fn)
        st_x = []
        segs_x = []
        for a, b in frei:
            roh = leger.lege(a, b)
            if not roh:
                continue
            fertig = leger.ausarbeiten(roh, a, b)
            if not fertig:
                continue
            kk = leger.kaskaden(fertig)
            # Segmentanfang = erste Lippe (davor bleibt der Spiegel)
            a2 = kk[0]["p"]
            biome_seg = [welt.biom_bei_m(*pr.xy(v)) for v in np.linspace(a2, b, 7)]
            biom_seg = max(set(biome_seg), key=lambda v: (biome_seg.count(v), v))
            segs_x.append((a2, b, biom_seg, int(np.searchsorted(grenzen_ab, a2, side="right") - 1)))
            st_x += kk
        for n, e in enumerate(sorted(st_x, key=lambda e: e["p"])):
            e["nr"] = len(alle_stufen) + n
            e["id"] = "%s_S%02d" % (x["id"], n + 1)
            e["strecke"] = x["id"]
            b_ = welt.biom_bei_m(*pr.xy(e["p"]))
            e["biom"] = b_ if b_ in rw.r["biome"] or b_ in rw.ERSATZ else (segs_x[0][2] if segs_x else "aue")
            netze(e["biom"])
            letzter = e.get("teil", [{"D": e["D"]}])[-1]
            e["kolk"] = rw.kolk("fall" if e["art"] == "fall" else "stufe", e["D"] if e["art"] != "kaskade" else letzter["D"],
                                e["S"], e["L"], e["B"])
            e["lippe_breite_m"] = rw.lippe_breite(e["B"])
            lin, ue, ub, br = lippe_linie(pr, rw, e, np.random.default_rng(abs(hash_stabil(SEED, e["id"]))))
            e["_lippe_m"], e["_ueberfall"], e["_ueberfall_b"] = lin, ue, ub
            an = hz["anteil"].get(rw.biom(e["biom"])[0], 0.0)
            e["holz"] = bool(e["art"] in ("stufe", "kaskade", "schnelle") and e["D"] <= hz["D_max"] and e["B"] <= hz["B_max"]
                             and float(np.random.default_rng(abs(hash_stabil(SEED, e["id"], "holz"))).uniform()) < an)
        if st_x:
            sx = sorted(st_x, key=lambda e: e["p"])
            for k in range(1, len(sx)):
                sx[k]["abstand_vorher"] = sx[k]["p"] - sx[k - 1]["p"]
        alle_stufen += st_x
        segmente += [(a, b) for a, b, _, _ in segs_x]
        eintrag["ausgespart"] = [list(g) for g in gruende]
        eintrag["segmente_m"] = [[_r(a, 2), _r(b, 2)] for a, b, _, _ in segs_x]
        eintrag["_segs"] = segs_x
        eintrag["_n_ab"] = n_ab
        strecken_out.append(eintrag)
    plan = {"stand": sfmt.heute(), "auftrag": "15 - steile Strecken: Felsstufen, Klippen, Faelle", "lauf": lauf_id,
            "art": lauf.art, "quelle_lauf": lauf.quelle, "ebene": EBENE,
            "regeln": {"datei": "recherche/antworten/skripte/gefaelle/gefaelle_regeln.json", "version": rw.version,
                       "stand": rw.stand},
            "daten": "1m" if welt.zelle_m == 1.0 else "2m (Cloud-Test)", "strecken": []}
    if not alle_stufen:
        plan["strecken"] = [{k: v for k, v in e.items() if not k.startswith("_")} for e in strecken_out]
        plan["hinweis"] = "keine planbaren Stufen (alle Strecken gebaut, umgebaut oder in festen Zonen)"
        return plan, [], meldungen, pr, None
    sp = spiegel_punkte(pr, alle_stufen, segmente)
    # Breite, Boeschungswinkel, Wandzonen
    Bw = pr.B.copy()
    winkel = np.full(pr.n, BOESCHUNG_GRAD)
    wandzonen = []
    wv = gr.wand(rw)
    for e in alle_stufen:
        if e["art"] == "schnelle":
            continue
        k0, k1 = e["p"] + e["l"], e["p"] + e["l"] + e["kolk"]["laenge"]
        m = (pr.s >= k0) & (pr.s <= k1)
        Bw[m] = np.maximum(Bw[m], gr.formel(rw.r["becken"]["breite"]["formel"], B=e["B"]))
    s_eval = np.arange(0.0, pr.s[-1] + 1e-6, 1.0)
    in_seg = np.zeros(len(s_eval), bool)
    for a, b in segmente:
        in_seg |= (s_eval >= a) & (s_eval <= b)
    eint = np.zeros(len(s_eval))
    eint[in_seg] = eintiefung(K, pr, sp, s_eval[in_seg])
    roh_zonen = []
    for e in alle_stufen:
        if e["art"] == "fall" and e["D"] >= 2.0:
            w = gr.wand(rw, D=e["D"])
            kw = gr.klamm_werte(rw, e["B"], D=e["D"])
            klamm = e["S"] >= kw["S_min"] and e["D"] >= 4.0
            lang = max(w["laenge_unterhalb"], kw["laenge"] if klamm else 0.0)
            roh_zonen.append({"a": e["p"] + e["l"], "b": e["p"] + e["l"] + lang, "hoehe": w["hoehe_an_fall"],
                              "grund": "Klamm unter Fall %s" % e["id"] if klamm else "Fall %s" % e["id"],
                              "klamm": klamm, "sohle": kw["sohlbreite"], "biom": e["biom"], "D": e["D"]})
    # Uferwand entlang: S >= S_min und Eintiefung >= eintiefung_min
    S_eval = np.array([pr.gefaelle(s, rw.fenster(pr.Bi(s))) for s in s_eval])
    kw0 = gr.klamm_werte(rw, 4.0)
    m_u = in_seg & (S_eval >= wv["S_min"]) & (eint >= wv["eintiefung_min"])
    st_ = None
    for k in range(len(s_eval)):
        if m_u[k] and st_ is None:
            st_ = k
        if (not m_u[k] or k == len(s_eval) - 1) and st_ is not None:
            a, b = s_eval[st_], s_eval[k]
            if b - a >= 6.0:
                ee = float(np.median(eint[st_:k + 1]))
                Dk = max([e["D"] for e in alle_stufen if e["art"] == "fall" and a - 60 <= e["p"] <= b] or [ee])
                klamm = float(np.median(S_eval[st_:k + 1])) >= kw0["S_min"] and ee >= kw0["eintiefung_min"]
                bi = welt.biom_bei_m(*pr.xy(0.5 * (a + b)))
                bi = bi if bi in rw.r["biome"] or bi in rw.ERSATZ else alle_stufen[0]["biom"]
                roh_zonen.append({"a": a, "b": b, "hoehe": gr.wand(rw, eintiefung=ee, D_klamm=Dk)["hoehe_entlang"],
                                  "grund": "Klamm (Eintiefung %.1f m)" % ee if klamm else "Uferklippe (Eintiefung %.1f m)" % ee,
                                  "klamm": klamm, "sohle": gr.klamm_werte(rw, pr.Bi(a))["sohlbreite"], "biom": bi, "D": ee})
            st_ = None
    # Zonen vereinigen (je Ort die hoechste Wand), in Becken-Stuecke teilen (eine Wasserhoehe je Wandgruppe)
    wh = np.zeros(pr.n)
    wz_id = np.full(pr.n, -1)
    wk = np.zeros(pr.n, bool)
    in_seg_pr = np.zeros(pr.n, bool)
    for a, b in segmente:
        in_seg_pr |= (pr.s >= a) & (pr.s <= b)
    for n_z, z in enumerate(roh_zonen):
        m = (pr.s >= z["a"]) & (pr.s <= z["b"]) & in_seg_pr
        hoeher = m & (z["hoehe"] > wh)
        wh[hoeher] = z["hoehe"]
        wz_id[hoeher] = n_z
        if z["klamm"]:
            wk |= m
    lippen = sorted(e["p"] for e in alle_stufen)
    for e in alle_stufen:                                  # an jeder Stufe 1 m Abstand (Wasserhoehe wechselt)
        wh[(pr.s >= e["p"] - 0.5) & (pr.s < e["p"] + e["l"] + 1.0)] = 0.0
    k = 0
    while k < pr.n:
        if wh[k] <= 0:
            k += 1
            continue
        k1 = k
        while k1 + 1 < pr.n and wh[k1 + 1] > 0:
            k1 += 1
        a, b = float(pr.s[k]), float(pr.s[k1])
        if b - a >= 4.0:
            ids = wz_id[k:k1 + 1]
            z = roh_zonen[int(np.bincount(ids[ids >= 0]).argmax())]
            klamm = bool(wk[k:k1 + 1].mean() >= 0.5)
            m = (pr.s >= a) & (pr.s <= b)
            if klamm:
                Bw[m] = np.maximum(Bw[m], z["sohle"])
                winkel[m] = np.maximum(winkel[m], 85.0)
            else:
                wn = rw.r["faelle"].get("wand_neigung") or {"min": 70, "max": 90}
                w_ = 0.5 * sum(wv["neigung"]) if z["grund"].startswith("Ufer") else 0.5 * (float(wn["min"]) + float(wn["max"]))
                winkel[m] = np.maximum(winkel[m], min(w_, 85.0))
            wandzonen.append(dict(z, a=a, b=b, hoehe=float(wh[k:k1 + 1].max()), klamm=klamm,
                                  grund=("Klamm: " if klamm and not z["grund"].startswith("Klamm") else "") + z["grund"],
                                  z_wasser=float(spiegel_bei(sp, a + 0.5)), nr=len(wandzonen)))
        k = k1 + 1
    # Boeschungswinkel ueber die Stufen hinweg fortsetzen (Max-Filter +-2 m), sonst V-Kerbe an der Fallkante
    w_ = int(2.0 / DS)
    winkel = np.array([winkel[max(0, k - w_):k + w_ + 1].max() for k in range(pr.n)])
    # Breite glatt (Uebergaenge 3 m), dann Versatz der Waende
    kern = np.ones(int(3.0 / DS) * 2 + 1)
    Bw = np.maximum(pr.B, np.convolve(np.pad(Bw, len(kern) // 2, mode="edge"), kern / kern.sum(), mode="valid"))

    def breite_fn(s):
        return np.interp(s, pr.s, Bw)

    def winkel_fn(s):
        return np.interp(s, pr.s, winkel)
    for wz in wandzonen:
        wz["versatz"] = float(np.max(breite_fn(np.linspace(wz["a"], wz["b"], 8)))) / 2.0 + 0.5 * sum(wv["abstand"])
    # Abschnitte (Fenster) je Strecke und Abschnittsnummer
    ebene = instanzen.Ebene(EBENE, inv, stand=sfmt.heute(), ebene_name=EBENE, ft_praefix=FT_PRAEFIX)
    kontexte = []
    stempel_liste = []
    aus_lauf = os.path.join(K["aus"], lauf_id)
    for x in strecken_out:
        if "_segs" not in x:
            continue
        for n_ab in range(x["_n_ab"]):
            segs = [(a, b, bi) for a, b, bi, k in x["_segs"] if k == n_ab]
            if not segs:
                continue
            aid = x["id"] if x["_n_ab"] == 1 else "%s_a%d" % (x["id"], n_ab + 1)
            st_ab = [e for e in alle_stufen if e["strecke"] == x["id"] and any(a - 1e-6 <= e["p"] <= b + 1e-6 for a, b, _ in segs)]
            pts = np.vstack([np.asarray(pr.polylinie(a, b, 2.0)) for a, b, _ in segs])
            e_max = float(np.max(eint[np.isin(np.round(s_eval), np.round(np.concatenate(
                [np.arange(a, b, 1.0) for a, b, _ in segs])))])) if len(segs) else 0.0
            e_max = max(e_max, max([e["D"] + e.get("kolk", {}).get("tiefe", 0) for e in st_ab] or [0]))
            rand = min(70.0, 6.0 + float(Bw.max()) / 2.0 + e_max / math.tan(math.radians(BOESCHUNG_GRAD))) + 10.0
            x0, y0 = pts[:, 0].min() - rand, pts[:, 1].min() - rand
            x1, y1 = pts[:, 0].max() + rand, pts[:, 1].max() + rand
            if max(x1 - x0, y1 - y0) > 600.0:
                melde("WARNUNG", "%s: Fenster %.0f x %.0f m > 600 m" % (aid, x1 - x0, y1 - y0))
            st = stm.Stempel(welt, x0, y0, x1, y1, rand_m=8.0, seed=SEED)
            korr = np.zeros(st.X.shape, bool)
            for a, b, _ in segs:
                korr |= gelaende_abschnitt(st, pr, sp, st_ab, a, b, breite_fn, winkel_fn, rw, welt, gel, orte_nah)
            schutz_orte(st, welt, gel, orte_nah)
            # anderes Wasser: SEHENS_FORMAT §3 - keine Aenderung <= 3 m (+ 2 m Uebergang); Wege/Pfade 4 m + 4 m (Reserve
            # fuer die 1-m-Interpolation) ueber Stempel.fertig
            from sehens_lib import gelaende as gel_mod
            wm = (st.fe.get("wasser") > 0) & ~korr
            if wm.any():
                dw = gel_mod.abstand(wm, welt.zelle_m, 12.0)
                st.delta *= glatt01((dw - 3.0 - 0.5 * welt.zelle_m) / 2.0)
            st.fertig(schutz=True, weg_m=4.0, wasser=False)
            st.protokoll = ["Bett"] + (["Kolk"] if any(e["art"] != "schnelle" for e in st_ab) else []) + \
                (["Felsstufe"] if any(e["art"] == "fall" for e in st_ab) else []) + \
                (["Klamm"] if any(w["klamm"] for w in wandzonen if any(a <= w["a"] <= b for a, b, _ in segs)) else []) + \
                (["Uferklippen"] if any(not w["klamm"] for w in wandzonen if any(a <= w["a"] <= b for a, b, _ in segs)) else [])
            st.ist_wasser = True
            if st.max_aenderung_m > 40.0:
                st.begruendung = "Fallhoehe + Kolk eines Falls > 40 m (Regelwerk faelle/kolk)"
            sk = neue_senken(st, st._lauf_maske | korr)
            if sk["flaeche_m2"] > 0:
                melde("WARNUNG" if sk["flaeche_m2"] >= 30.0 else "HINWEIS", "%s: geschlossene Senke ausserhalb des Laufs %.0f m2, %.1f m tief"
                      % (aid, sk["flaeche_m2"], sk["max_tiefe_m"]))
            stempel_liste.append(st)
            cx, cy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
            biom_ab = max(set(bi for _, _, bi in segs), key=lambda v: sum(1 for _, _, b2 in segs if b2 == v))
            standort = {"id": aid, "name": "Gefaelle %s" % aid, "art": "fundstueck",
                        "mitte_cm": [round(cx * 100), round(cy * 100), round(float(welt.hoehe_bei_m(cx, cy)) * 100)],
                        "radius_m": 0.5 * math.hypot(x1 - x0, y1 - y0), "felder": sorted({daten.feld_von_m(px, py)
                                                                                         for px, py in pts}),
                        "kameras": []}
            ctx = rezept.OrtKontext(welt, gel, inv, ebene, standort, {"lagen": []}, biom_ab, seed=SEED)
            ctx.stempel = st
            ctx.linien["bach_haupt"] = pr.polylinie(max(0.0, segs[0][0] - 5), min(pr.s[-1], segs[-1][1] + 5), 1.0)
            wz_ab = [w for w in wandzonen if any(a - 1e-6 <= w["a"] <= b + 1e-6 for a, b, _ in segs)]
            bauen_instanzen(ctx, K, pr, st_ab, [(a, b, bi) for a, b, bi in segs], wz_ab, biom_netze, None)
            # nichts in Sehenswuerdigkeiten (Radius + 10 m)
            vorher = len(ebene.stuecke)
            ebene.stuecke = [s_ for s_ in ebene.stuecke if s_["ort"] != aid or not any(
                math.hypot(s_["x"] / 100.0 - o["x_m"], s_["y"] / 100.0 - o["y_m"]) <= o["radius_m"] + 10.0 for o in orte_nah)]
            if len(ebene.stuecke) < vorher:
                melde("HINWEIS", "%s: %d Instanzen in Sehenswuerdigkeiten entfernt" % (aid, vorher - len(ebene.stuecke)))
            lg = stm.Lagen(welt, *st.fe.grenzen_m(), seed=SEED)
            bauen_lagen(lg, K, pr, st_ab, [(a, b, bi) for a, b, bi in segs], wz_ab,
                        {bi: rw.biom(bi)[1]["lagen"] for bi in {e["biom"] for e in st_ab} | {bi for _, _, bi in segs}},
                        breite_fn)
            ctx.lagen = lg
            ebene.ausduennen(aid, 15000, 1500, 80)
            for s_, oid, t_ in ctx.meldungen:
                meldungen.append((s_, oid, t_))
            kontexte.append({"ctx": ctx, "id": aid, "strecke": x["id"], "stufen": st_ab, "segs": segs, "biom": biom_ab})
    # Effekte, Kameras, Flussstuecke
    effekte, eff_weg = bauen_effekte(K, pr, alle_stufen, breite_fn)
    from sehens_lib.stempel import _bilinear_fenster

    def boden_fn(x, y):
        x = np.asarray(x, np.float64)
        y = np.asarray(y, np.float64)
        h = welt.bilinear(welt.hoehe, x, y)
        for st_ in stempel_liste:
            h = h + _bilinear_fenster(st_.delta, st_.fe, welt, x, y, 0.0)
        return h
    wasser_koerper = bauen_wasser_A(pr, sp, alle_stufen, segmente, breite_fn, lauf_id, boden_fn, melde)
    kameras = []
    for x in strecken_out:
        if x.get("pilot") and x.get("_segs") and any(e["strecke"] == x["id"] for e in alle_stufen):
            kameras += bauen_kameras(K, pr, x["id"], [e for e in alle_stufen if e["strecke"] == x["id"]],
                                     breite_fn, stempel_liste)
            if not any(k[6].endswith("_vorher") and not k[6].endswith("weg_vorher") for k in kameras if k[6].startswith(x["id"])):
                melde("WARNUNG", "%s: keine freie Kameraposition fuer _vorher/_nachher gefunden" % x["id"])
    # Schreiben
    os.makedirs(aus_lauf, exist_ok=True)
    for sub in ("gelaende", "lagen", "instanzen"):
        p_ = os.path.join(aus_lauf, sub)
        if os.path.isdir(p_):
            import shutil
            shutil.rmtree(p_)
    ab_out = []
    for kx in kontexte:
        ctx = kx["ctx"]
        blk = ctx.stempel.schreibe(aus_lauf, kx["id"])
        lblk = ctx.lagen.schreibe(aus_lauf, kx["id"])
        z = ebene.zaehle(kx["id"])
        ab_out.append({"id": kx["id"], "strecke": kx["strecke"], "biom": kx["biom"],
                       "felder": ctx.st["felder"], "segmente_m": [[_r(a, 2), _r(b, 2)] for a, b, _ in kx["segs"]],
                       "gelaende": blk, "lagen": lblk,
                       "budget": {"instanzen": z["instanzen"], "kollision": z["kollision"], "akteure": z["akteure"],
                                  "niagara": sum(1 for e in effekte if e["stufe"] in {s_["id"] for s_ in kx["stufen"]})},
                       "detail_ebenen": {k: v for k, v in z["je_ebene"].items()}})
    info = ebene.schreibe(os.path.join(aus_lauf, "instanzen")) if ebene.stuecke else {}
    stufen_out = []
    for e in sorted(alle_stufen, key=lambda e: e["p"]):
        tx, ty = pr.tang(e["p"])
        fx, fy = pr.xy(e["p"] + e["l"])
        d = {"id": e["id"], "strecke": e["strecke"], "s_m": _r(e["p"], 2), "art": {"stufe": "kaskade"}.get(e["art"], e["art"]),
             "art_regel": e["art"], "fall_m": _r(e["D"], 2), "lippe_cm": [[round(p[0] * 100, 1), round(p[1] * 100, 1),
                                                                            round(e["u"] * 100, 1)] for p in e["_lippe_m"]],
             "lippe_breite_cm": round(e["lippe_breite_m"] * 100), "ueberfall_cm": [round(e["_ueberfall"][0] * 100, 1),
                                                                                   round(e["_ueberfall"][1] * 100, 1),
                                                                                   round(e["u"] * 100, 1)],
             "ueberfall_breite_cm": round(e["_ueberfall_b"] * 100), "fuss_cm": [round(fx * 100, 1), round(fy * 100, 1),
                                                                               round(e["d"] * 100, 1)],
             "fuss_z_cm": round(e["d"] * 100, 1), "richtung": [round(tx, 4), round(ty, 4)],
             "breite_m": _r(e["B"], 2), "abstand_naechste_m": _r(e["L"], 2), "gefaelle_einheit": round(e["S"], 3),
             "becken_gefaelle": round(e["gb"], 4), "klasse": e["klasse"], "biom": e["biom"],
             "felstyp": rw.biom(e["biom"])[1].get("felstyp", ""), "fels_anstehend": bool(e["fels"]),
             "erzwungen_knickpunkt": bool(e.get("erzwungen")), "holzstufe": bool(e.get("holz")),
             "vorhang": e["art"] != "schnelle" and e["D"] >= NIAGARA_KLEIN["D_max"],
             "vorhang_niagara": e["art"] != "schnelle" and NIAGARA_KLEIN["D_min"] <= e["D"] < NIAGARA_KLEIN["D_max"]}
        if e["art"] != "schnelle":
            ko = e["kolk"]
            kx_, ky_ = pr.xy(e["p"] + e["l"] + (ko["x_strahl"] if e["art"] == "fall" else 0.4 * ko["laenge"]))
            d["kolk"] = {"tiefe_m": _r(ko["tiefe"], 2), "laenge_m": _r(ko["laenge"], 2), "radius_m": _r(ko["radius"], 2),
                         "mitte_cm": [round(kx_ * 100, 1), round(ky_ * 100, 1), round((e["d"] - ko["tiefe"]) * 100, 1)]}
        else:
            d["rampe_m"] = _r(e["l"], 2)
        if e.get("teil"):
            d["teilstufen"] = [{"s_m": _r(t["p"], 2), "fall_m": _r(t["D"], 2), "oben_z_cm": round(t["u"] * 100, 1),
                                "unten_z_cm": round(t["d"] * 100, 1)} for t in e["teil"]]
        stufen_out.append(d)
    for x in strecken_out:
        x["stufen"] = [d["id"] for d in stufen_out if d["strecke"] == x["id"]]
        x["abschnitte"] = [a["id"] for a in ab_out if a["strecke"] == x["id"]]
        x["kameras"] = [k for k in kameras if k[6].startswith(x["id"] + "_")]
        x["arten"] = {a: sum(1 for d in stufen_out if d["strecke"] == x["id"] and d["art_regel"] == a)
                      for a in ("schnelle", "stufe", "kaskade", "fall")}
        x["fall_gestuft_m"] = _r(sum(d["fall_m"] for d in stufen_out if d["strecke"] == x["id"]), 2)
    plan.update({
        "strecken": [{k: v for k, v in e.items() if not k.startswith("_")} for e in strecken_out],
        "spiegel_alt_cm": [[round(float(p[0]), 1), round(float(p[1]), 1), round(float(p[2]), 1), round(float(p[3]), 1)]
                           for p in lauf.P],
        "spiegel_neu_cm": [[round(pr.xy(s_)[0] * 100, 1), round(pr.xy(s_)[1] * 100, 1), round(z_ * 100, 1),
                            round(float(breite_fn(s_)) * 100, 1)] for s_, z_, _ in sp],
        "spiegel_neu_art": [k_ for _, _, k_ in sp],
        "spiegel_neu_s_m": [_r(s_, 2) for s_, _, _ in sp],
        "stufen": stufen_out,
        "wasser_koerper": wasser_koerper,
        "wasser_hinweis": "Variante A (14b): Epic-River nur ober-/unterhalb der Stufenstrecken, dazwischen Kaskadennetz "
                          "(statisch, SLW); keine Flussstuecke mit Luecken, keine Schaumscheiben. Vorhang-Netz nur an "
                          "Stufen in vorhang_an_stufen (Fall >= 3 m), sonst Nature Water FX.",
        "abschnitte": ab_out,
        "wandzonen": [{"nr": w["nr"], "s_m": [_r(w["a"], 2), _r(w["b"], 2)], "grund": w["grund"], "hoehe_m": _r(w["hoehe"], 2),
                       "klamm": bool(w["klamm"]), "z_wasser_cm": round(w["z_wasser"] * 100, 1), "biom": w["biom"]}
                      for w in wandzonen],
        "instanzen": {"ordner": "instanzen", "ebene": EBENE, "ft_praefix": FT_PRAEFIX, "felder": info,
                      "anzahl": sum(v["instanzen"] for v in info.values()), "kollision": sum(v["kollision"] for v in info.values()),
                      "akteure": sum(v["akteure"] for v in info.values())},
        "akteure": sum(v["akteure"] for v in info.values()),
        "effekte": effekte, "effekte_ausgeduennt": eff_weg,
        "kameras": kameras,
        "felder": sorted({daten.feld_von_m(px, py) for px, py in zip(pr.x[::20], pr.y[::20])}),
    })
    for h in ebene.hinweise:
        melde("HINWEIS", h)
    if K.get("variante") == "C":
        plan["wasser_koerper_alternativ"] = wasser_C(pr, sp, alle_stufen, breite_fn, lauf_id)
    plan["meldungen"] = [{"stufe": s_, "text": t_} for s_, _, t_ in meldungen]
    with open(os.path.join(aus_lauf, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1, default=_json_np)
    return plan, kontexte, meldungen, pr, sp


def _json_np(o):
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o).__name__)


def hash_stabil(*teile):
    import zlib
    return zlib.crc32("|".join(str(t) for t in teile).encode("utf-8"))


# ======================================================================================================================
# Testbild: Draufsicht (sehens_lib.vorschau) + Laengsprofil vorher/nachher
# ======================================================================================================================
def testbild(kx, K, pr, sp, plan, pfad):
    from PIL import Image, ImageDraw
    from sehens_lib import vorschau, zeichnen as zz
    ctx = kx["ctx"]
    sid = kx["strecke"]
    # Wasser fuer die Draufsicht: neue Flussstuecke als Linien, Effekte, Kameras der Strecke
    def ausgeduennt(P):
        out = [P[0][:4]]
        for q in P[1:]:
            if math.hypot(q[0] - out[-1][0], q[1] - out[-1][1]) >= 150.0:     # Zeichnung: Punkte >= 1,5 m auseinander
                out.append(q[:4])
        return out if len(out) > 1 else [P[0][:4], P[-1][:4]]
    ctx.wasser = [{"typ": "bach", "punkte_cm": ausgeduennt(wk.get("punkte") or wk.get("mittellinie"))}
                  for wk in plan["wasser_koerper"]]
    ctx.effekte = [e for e in plan["effekte"] if e["stufe"] in {s_["id"] for s_ in kx["stufen"]}]
    ctx.st["kameras"] = [k for k in plan["kameras"] if k[6].startswith(sid + "_") and "nachher" in k[6]]
    ab = next(a for a in plan["abschnitte"] if a["id"] == kx["id"])
    ctx.eintrag = {"budget": ab["budget"], "detail_ebenen": {k: {"anzahl": v, "netze": {}} for k, v in ab["detail_ebenen"].items()}}
    x0, y0, x1, y1 = ctx.stempel.fe.grenzen_m()
    ctx.mx, ctx.my = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
    tmp = pfad + ".draufsicht.png"
    vorschau.vorschau(ctx, tmp, groesse_m=min(600.0, max(x1 - x0, y1 - y0)), breite_px=900)
    top = Image.open(tmp).convert("RGB")
    os.remove(tmp)
    # Laengsprofil
    W = top.size[0]
    H = 360
    img = Image.new("RGB", (W, H), (22, 22, 26))
    dr = ImageDraw.Draw(img)
    a = min(sg[0] for sg in kx["segs"]) - 15.0
    b = max(sg[1] for sg in kx["segs"]) + 15.0
    a, b = max(0.0, a), min(pr.s[-1], b)
    ss = np.arange(a, b, 0.5)
    xs, ys = np.interp(ss, pr.s, pr.x), np.interp(ss, pr.s, pr.y)
    g_alt = K["welt"].hoehe_bei_m(xs, ys)
    g_neu = ctx.stempel.hoehe_bei_m(xs, ys)
    z_alt = np.interp(ss, pr.s, pr.z0)
    z_neu = spiegel_bei(sp, ss)
    zmin, zmax = float(min(g_neu.min(), z_neu.min())) - 2, float(max(g_alt.max(), z_alt.max())) + 2
    L, R, T, Bm = 60, W - 20, 30, H - 40

    def P(s_, z_):
        return L + (s_ - a) / max(b - a, 1e-6) * (R - L), Bm - (z_ - zmin) / max(zmax - zmin, 1e-6) * (Bm - T)
    f = zz._font(12)
    for zl in np.arange(math.ceil(zmin / 5) * 5, zmax, 5 if zmax - zmin < 80 else 20):
        dr.line([P(a, zl), P(b, zl)], fill=(50, 50, 56))
        dr.text((4, P(a, zl)[1] - 7), "%.0f m" % zl, fill=(150, 150, 150), font=f)
    dr.line([P(s_, z_) for s_, z_ in zip(ss, g_alt)], fill=(140, 110, 80), width=1)
    dr.line([P(s_, z_) for s_, z_ in zip(ss, g_neu)], fill=(200, 160, 110), width=2)
    dr.line([P(s_, z_) for s_, z_ in zip(ss, z_alt)], fill=(150, 150, 150), width=2)
    dr.line([P(s_, z_) for s_, z_ in zip(ss, z_neu)], fill=(60, 150, 255), width=3)
    for e in kx["stufen"]:
        px, py = P(e["p"], e["u"])
        c = {"fall": (255, 80, 80), "kaskade": (255, 170, 40), "stufe": (250, 230, 60), "schnelle": (120, 220, 255)}[e["art"]]
        dr.line([(px, py - 4), (px, py - 14)], fill=c, width=2)
        if e["D"] >= 2.0:
            dr.text((px + 2, py - 28), "%.1f" % e["D"], fill=c, font=f)
    for wk in plan["wasser_koerper"]:
        c = (60, 150, 255) if wk["typ"] == "river" else (120, 230, 200)
        s0_, s1_ = max(a, wk["s_m"][0]), min(b, wk["s_m"][1])
        if s1_ > s0_:
            dr.line([(P(s0_, zmin)[0], Bm + 8), (P(s1_, zmin)[0], Bm + 8)], fill=c, width=4)
    leg = [("Gelaende alt", (140, 110, 80)), ("Gelaende neu", (200, 160, 110)), ("Spiegel alt", (150, 150, 150)),
           ("Spiegel neu", (60, 150, 255)), ("Fall", (255, 80, 80)), ("Kaskade", (255, 170, 40)),
           ("Blockstufe", (250, 230, 60)), ("Schnelle", (120, 220, 255)), ("River", (60, 150, 255)),
           ("Kaskadennetz", (120, 230, 200))]
    xl = L
    for t, c in leg:
        dr.rectangle([xl, 8, xl + 10, 18], fill=c)
        dr.text((xl + 14, 6), t, fill=(220, 220, 220), font=f)
        xl += 14 + 8 * len(t) + 14
    st = next(x for x in plan["strecken"] if x["id"] == sid)
    dr.text((L, H - 22), "%s  Laengsprofil s %.0f-%.0f m  |  %s  |  Fall %.1f m, gestuft %.1f m  |  Arten %s" % (
        kx["id"], a, b, st["status"], st["fall_m"], st.get("fall_gestuft_m", 0),
        ", ".join("%s %d" % (k, v) for k, v in (st.get("arten") or {}).items() if v)), fill=(230, 230, 230), font=f)
    out = Image.new("RGB", (W, top.size[1] + H), (22, 22, 26))
    out.paste(top, (0, 0))
    out.paste(img, (0, top.size[1]))
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    out.save(pfad, optimize=True)
    return pfad


# ======================================================================================================================
def main(argv=None):
    ap = argparse.ArgumentParser(description="Planer steile Strecken (Auftrag 15)")
    ap.add_argument("--laeufe", nargs="+", default=None, help="Lauf-IDs (Bach/Fluss), alle ihre Strecken")
    ap.add_argument("--strecken", nargs="+", default=None, help="Strecken-IDs <lauf>_s<k> (nur diese)")
    ap.add_argument("--alle", action="store_true", help="alle 161 Strecken")
    ap.add_argument("--aus", default=None, help="Ausgabeordner (Standard <basis>/export/unreal/welt/gefaelle)")
    ap.add_argument("--basis", default=".", help="production-Wurzel (1-m-Daten in export/unreal/welt)")
    ap.add_argument("--regeln", default=gr.REGELN_STANDARD)
    ap.add_argument("--prioritaet", default=os.path.join(gd.ANTWORTEN, "gefaelle", "prioritaet.json"))
    ap.add_argument("--strecken-datei", default=gd.STRECKEN_STANDARD)
    ap.add_argument("--sehens", default=gd.SEHENS_STANDARD)
    ap.add_argument("--p2", default=gd.P2_STANDARD, help="Sehens-Planausgaben (<p2>/<biom>/orte.json)")
    ap.add_argument("--baeche", default=None, help="baeche_alle.json (Standard: Daten-Ordner bzw. vorlagen/daten/sehens)")
    ap.add_argument("--inventar", default=None)
    ap.add_argument("--bild", action="store_true", help="test_<strecke>.png je Pilot-Strecke")
    ap.add_argument("--bild-ordner", default=None, help="Standard: <aus>/<lauf>/")
    ap.add_argument("--ohne-pruefung", action="store_true")
    ap.add_argument("--variante", choices=["A", "C"], default="A",
                    help="A = River + Kaskadennetz (Standard, 14b); C = zusaetzlich gestufter Spline + Bach-Zone")
    from sehens_lib import daten
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    T0 = time.perf_counter()
    from sehens_lib import gelaende, inventar, sicht
    try:
        rw = gr.Regelwerk.lade(a.regeln)
    except (FileNotFoundError, gr.RegelFehler) as ex:
        _log("FEHLER:", ex)
        return 2
    try:
        inv = inventar.Inventar.lade(a.inventar)
    except FileNotFoundError as ex:
        _log("FEHLER:", ex)
        return 2
    daten1m = a.daten1m
    if not a.daten2m and not daten1m:
        daten1m = os.path.join(a.basis, "export", "unreal", "welt")
        if not os.path.isdir(daten1m):
            _log("FEHLER: weder --daten2m noch 1-m-Daten (%s)" % daten1m)
            return 2
    try:
        welt = daten.lade(a.daten2m, daten1m, pfade=a.sehens)
    except (FileNotFoundError, ValueError) as ex:
        _log("FEHLER: Daten:", ex)
        return 2
    gel = gelaende.Gelaende(welt, cache=a.cache)
    _ZELLE[0] = welt.zelle_m
    _log(welt.info(), "| Regelwerk v%s (%s)" % (rw.version, rw.stand))
    # Baeche: baeche_alle.json (R1+R2+R3, IDs wie steile_strecken.json)
    bpfad = a.baeche
    if not bpfad:
        for c in ([os.path.join(daten1m, "baeche", "baeche_alle.json")] if daten1m else []) + \
                [os.path.join(a.daten2m or gd.DATEN2M_STANDARD, "baeche_alle.json"), os.path.join(gd.DATEN2M_STANDARD, "baeche_alle.json")]:
            if os.path.exists(c):
                bpfad = c
                break
    baeche = gd.lese_json(bpfad)["baeche"] if bpfad else welt.baeche
    aus = os.path.abspath(a.aus or os.path.join(a.basis, "export", "unreal", "welt", "gefaelle"))
    prio = {}
    pilot = []
    if os.path.exists(a.prioritaet):
        pd_ = gd.lese_json(a.prioritaet)
        prio = {e["id"]: e for e in pd_["strecken"]}
        pilot = pd_.get("pilot", [])
    else:
        _log("WARNUNG: Prioritaetenliste fehlt (%s) - alle Strecken 'offen', keine Pilot-Kameras" % a.prioritaet)
    strecken, _ = gd.lade_strecken(a.strecken_datei, welt, baeche, welt.wasser_welt)
    if a.strecken:
        ziel = [x for x in strecken if x["id"] in a.strecken]
    elif a.laeufe:
        ziel = [x for x in strecken if x["lauf"] in a.laeufe]
    elif a.alle:
        ziel = strecken
    else:
        ziel = [x for x in strecken if x["id"] in pilot]
    if not ziel:
        _log("FEHLER: keine Strecken gewaehlt")
        return 2
    laeufe = []
    for x in ziel:
        if x["lauf"] not in laeufe:
            laeufe.append(x["lauf"])
    umbau = gd.sehens_umbau(a.p2)
    if not umbau:
        _log("HINWEIS: keine Sehens-Planausgaben in %s - Umbau-Zonen nur aus der Prioritaetenliste" % a.p2)
    K = {"welt": welt, "gel": gel, "inv": inv, "rw": rw, "prio": prio, "strecken": strecken,
         "orte": gd.sehens_orte(a.sehens), "umbau": umbau, "baeche": baeche, "wasser_welt": welt.wasser_welt,
         "aus": aus, "wp": sicht.Wegpunkte(welt, 20.0), "klamm": gr.klamm_werte(rw, 4.0), "variante": a.variante}
    rc = 0
    alle_meld = []
    zusammen = []
    for lid in laeufe:
        t0 = time.perf_counter()
        ids = None if (a.laeufe or a.alle) and not a.strecken else {x["id"] for x in ziel if x["lauf"] == lid}
        plan, kontexte, meld, pr, sp = plane_lauf(lid, K, ids)
        alle_meld += meld
        ns = len(plan.get("stufen", []))
        wk = plan.get("wasser_koerper", [])
        _log("%-26s %3d Stufen, %d River + %d Netz, %5d Inst, %3d Akt, %2d FX  %.1f s" % (
            lid, ns, sum(1 for w in wk if w["typ"] == "river"), sum(1 for w in wk if w["typ"] == "kaskadennetz"),
            plan.get("instanzen", {}).get("anzahl", 0),
            plan.get("akteure", 0), len(plan.get("effekte", [])), time.perf_counter() - t0))
        zusammen.append(plan)
        if a.bild and kontexte:
            for kx in kontexte:
                st = next(x for x in plan["strecken"] if x["id"] == kx["strecke"])
                if st.get("pilot") or a.strecken:
                    ziel_b = os.path.join(a.bild_ordner or os.path.join(aus, lid), "test_%s.png" % kx["id"])
                    _log("Bild:", testbild(kx, K, pr, sp, plan, ziel_b))
        if not a.ohne_pruefung and plan.get("stufen"):
            import gefaelle_pruefen
            bef = gefaelle_pruefen.pruefe_lauf(os.path.join(aus, lid), welt=welt, inv=inv, rw=rw, gel=gel)
            z = gefaelle_pruefen.melde(bef, lid)
            if z["FEHLER"]:
                rc = 1
    for st_ in ("FEHLER", "WARNUNG"):
        for s_, oid, t_ in alle_meld:
            if s_ == st_:
                _log("  %-7s %-24s %s" % (s_, oid[:24], t_))
    n = {s_: sum(1 for m in alle_meld if m[0] == s_) for s_ in ("FEHLER", "WARNUNG", "HINWEIS")}
    _log("Planer: %d FEHLER, %d WARNUNG, %d HINWEIS | %d Laeufe, %d Stufen | %.0f s" % (
        n["FEHLER"], n["WARNUNG"], n["HINWEIS"], len(laeufe), sum(len(p.get("stufen", [])) for p in zusammen),
        time.perf_counter() - T0))
    if n["FEHLER"]:
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
