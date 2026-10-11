# -*- coding: utf-8 -*-
"""gefaelle_daten.py - gemeinsame Daten fuer Auftrag 15 (steile Fluss-/Bachstrecken): Strecken, Laeufe, Sehens-Orte.

Wird von gefaelle_prioritaet.py, gefaelle_plan.py und gefaelle_pruefen.py importiert (python -I: der Planer setzt
seinen Ordner selbst in sys.path).

  strecken = lade_strecken(pfad)            # 161 Strecken mit stabiler id <lauf>_s<k> (k = Reihenfolge im Lauf)
  lauf = Lauf.aus_welt(welt, lauf_id, baeche=..., wasser_welt=...)   # Punkte [x, y, z, breite, tiefe, v] in cm
  lauf.s_von_cm(x, y) -> Bogenlaenge (m) der Projektion; lauf.abschnitt(s0, s1, schritt_m) -> Proben
  orte = sehens_orte(sehens_ordner)         # 120 Orte (standorte.json): mitte, radius, kameras
  umbau = sehens_umbau(p2_ordner)           # Wasser/Gelaende der Sehens-Planer (orte.json Phase 2)

Koordinaten wie vorlagen/FORMAT.md §1 (cm in Unreal, m intern). Keine Unreal-Importe.
"""

import glob
import json
import math
import os

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
SKRIPTE = os.path.dirname(HIER)                       # recherche/antworten/skripte
ANTWORTEN = os.path.dirname(SKRIPTE)                  # recherche/antworten
RECHERCHE = os.path.dirname(ANTWORTEN)                # recherche
STRECKEN_STANDARD = os.path.join(RECHERCHE, "vorlagen", "daten", "gefaelle", "steile_strecken.json")
DATEN2M_STANDARD = os.path.join(RECHERCHE, "vorlagen", "daten", "sehens")
SEHENS_STANDARD = os.path.join(ANTWORTEN, "sehens")
P2_STANDARD = "/tmp/claude-0/-home-user-fbulut/a2c581ba-c24a-5bce-9c65-c37d036a756e/scratchpad/a13/p2"
WASSER_FX_PLAN = os.path.join(ANTWORTEN, "wasser_fx", "plan.json")
STUFEN_FX = os.path.join(RECHERCHE, "vorlagen", "daten", "wasser_fx", "stufen.json")
BIOME_SEHENS = ("aue", "bergwald", "canyon", "dschungel", "elfenwald", "fjord", "frost", "gletscher", "heide",
                "kueste", "lava", "oedland", "sumpf", "tundra", "wueste")


def lese_json(pfad):
    with open(pfad, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------------------------------------------------------------------------------------
# Laeufe (Fluesse aus wasser_welt.json, Baeche aus baeche_alle.json)
# ----------------------------------------------------------------------------------------------------------------------
class Lauf:
    """Ein Gewaesserlauf (Epic-Fluss eines Felds oder Bach): Punkte N x 6 [x, y, z, breite, tiefe, v] in cm."""

    def __init__(self, lauf_id, art, punkte, feld=None, quelle=""):
        self.id = lauf_id
        self.art = art
        self.feld = feld
        self.quelle = quelle
        P = np.asarray(punkte, np.float64)
        if P.ndim != 2 or P.shape[0] < 2:
            raise ValueError("Lauf %s: zu wenige Punkte" % lauf_id)
        if P.shape[1] < 6:
            P = np.hstack([P, np.zeros((P.shape[0], 6 - P.shape[1]))])
        self.P = P
        self.xy = P[:, :2] / 100.0
        seg = np.hypot(*np.diff(self.xy, axis=0).T)
        self.s = np.concatenate([[0.0], np.cumsum(seg)])
        self.laenge_m = float(self.s[-1])
        self.z = P[:, 2] / 100.0
        self.breite = P[:, 3] / 100.0

    @classmethod
    def aus_welt(cls, welt, lauf_id, baeche=None, wasser_welt=None):
        ww = wasser_welt if wasser_welt is not None else (welt.wasser_welt or {})
        for f in ww.get("fluesse", []) or []:
            if f.get("id") == lauf_id:
                return cls(lauf_id, "fluss", f["punkte"], f.get("feld"), "wasser_welt.json")
        for b in (baeche if baeche is not None else welt.baeche) or []:
            if b.get("id") == lauf_id:
                return cls(lauf_id, "bach", b["punkte"], b.get("feld"), "baeche_alle.json")
        raise KeyError("Lauf %s weder in wasser_welt.json['fluesse'] noch in den Baechen" % lauf_id)

    def s_von_m(self, x, y):
        """Bogenlaenge (m) der Projektion eines Punkts auf die Polylinie."""
        a, b = self.xy[:-1], self.xy[1:]
        ab = b - a
        t = np.clip(((x - a[:, 0]) * ab[:, 0] + (y - a[:, 1]) * ab[:, 1]) / np.maximum((ab ** 2).sum(1), 1e-9), 0, 1)
        d = np.hypot(x - (a[:, 0] + t * ab[:, 0]), y - (a[:, 1] + t * ab[:, 1]))
        k = int(np.argmin(d))
        return float(self.s[k] + t[k] * (self.s[k + 1] - self.s[k])), float(d[k])

    def bei_s(self, s):
        """Interpolation bei Bogenlaenge s (Array): x, y, z, breite (m), tiefe (cm), v (cm/s), Tangente."""
        s = np.clip(np.asarray(s, np.float64), 0, self.laenge_m)
        x = np.interp(s, self.s, self.xy[:, 0])
        y = np.interp(s, self.s, self.xy[:, 1])
        z = np.interp(s, self.s, self.z)
        br = np.interp(s, self.s, self.breite)
        k = np.clip(np.searchsorted(self.s, s, side="right") - 1, 0, len(self.s) - 2)
        d = self.xy[k + 1] - self.xy[k]
        n = np.maximum(np.hypot(d[..., 0], d[..., 1]), 1e-9)
        return {"x": x, "y": y, "z": z, "breite": br, "tx": d[..., 0] / n, "ty": d[..., 1] / n,
                "tiefe": np.interp(s, self.s, self.P[:, 4]), "v": np.interp(s, self.s, self.P[:, 5])}

    def proben(self, s0=0.0, s1=None, schritt_m=2.0):
        s1 = self.laenge_m if s1 is None else s1
        n = max(2, int(math.ceil((s1 - s0) / schritt_m)) + 1)
        s = np.linspace(s0, s1, n)
        d = self.bei_s(s)
        d["s"] = s
        return d


# ----------------------------------------------------------------------------------------------------------------------
# Strecken
# ----------------------------------------------------------------------------------------------------------------------
def lade_strecken(pfad=None, welt=None, baeche=None, wasser_welt=None):
    """Liste der steilen Strecken (steile_strecken.json) mit stabiler id <lauf>_s<k> (k ab 1 in Fliessrichtung).
    Mit welt: zusaetzlich s0_m/s1_m (Bogenlaenge auf dem Lauf) und abstand_projektion_m."""
    d = lese_json(pfad or STRECKEN_STANDARD)
    st = [dict(x) for x in d["strecken"]]
    laeufe = {}
    for x in st:
        laeufe.setdefault(x["lauf"], []).append(x)
    for lid, liste in laeufe.items():
        lauf = None
        if welt is not None:
            lauf = Lauf.aus_welt(welt, lid, baeche, wasser_welt)
            for x in liste:
                a, da = lauf.s_von_m(x["von_cm"][0] / 100.0, x["von_cm"][1] / 100.0)
                b, db = lauf.s_von_m(x["bis_cm"][0] / 100.0, x["bis_cm"][1] / 100.0)
                x["s0_m"], x["s1_m"] = round(min(a, b), 2), round(max(a, b), 2)
                x["abstand_projektion_m"] = round(max(da, db), 2)
            liste.sort(key=lambda x: x["s0_m"])
        else:
            liste.sort(key=lambda x: (-x["von_cm"][2], x["von_cm"][0]))
        for k, x in enumerate(liste):
            x["id"] = "%s_s%d" % (lid, k + 1)
    return st, d


# ----------------------------------------------------------------------------------------------------------------------
# Sehenswuerdigkeiten (Auftrag 13)
# ----------------------------------------------------------------------------------------------------------------------
def sehens_orte(sehens_ordner=None):
    """Alle Orte aus <sehens>/<biom>/standorte.json (Phase 1): id, biom, name, art, x_m, y_m, z_m, radius_m, kameras."""
    out = []
    for f in sorted(glob.glob(os.path.join(sehens_ordner or SEHENS_STANDARD, "*", "standorte.json"))):
        biom = os.path.basename(os.path.dirname(f))
        for o in lese_json(f).get("orte", []):
            m = o["mitte_cm"]
            out.append({"id": o["id"], "biom": biom, "name": o.get("name", ""), "art": o.get("art"),
                        "x_m": m[0] / 100.0, "y_m": m[1] / 100.0, "z_m": (m[2] / 100.0) if len(m) > 2 else None,
                        "radius_m": float(o.get("radius_m", 30.0)), "kameras": o.get("kameras", [])})
    return out


def _poly(p):
    return np.asarray(p, np.float64)[:, :2] / 100.0


def sehens_umbau(p2_ordner=None):
    """Wasser der Sehens-Planer (Phase 2, <p2>/<biom>/orte.json): je Ort mit Wasser oder gelaende.ist_wasser
    eine Liste Geometrien (Polylinien in m) + Fenster. Ordner fehlt -> leere Liste (Hinweis im Aufrufer)."""
    out = []
    p2 = p2_ordner or P2_STANDARD
    for biom in BIOME_SEHENS:
        f = os.path.join(p2, biom, "orte.json")
        if not os.path.exists(f):
            continue
        for o in lese_json(f).get("orte", []):
            g = o.get("gelaende") or {}
            geo = []
            for w in o.get("wasser") or []:
                if w.get("typ") == "bach" and w.get("punkte_cm"):
                    geo.append(("bach", w.get("id"), _poly(w["punkte_cm"])))
                elif w.get("typ") == "wasserfall" and w.get("kante_cm"):
                    geo.append(("wasserfall", w.get("id"), _poly(w["kante_cm"])))
                elif w.get("typ") == "see" and w.get("umriss_cm"):
                    u = _poly(w["umriss_cm"])
                    geo.append(("see", w.get("id"), np.vstack([u, u[:1]])))
            if not geo and not g.get("ist_wasser"):
                continue
            m = o.get("mitte_cm") or [0, 0]
            out.append({"id": o["id"], "biom": biom, "x_m": m[0] / 100.0, "y_m": m[1] / 100.0,
                        "radius_m": float(o.get("radius_m", 40.0)), "ist_wasser": bool(g.get("ist_wasser")),
                        "fenster_ij": g.get("fenster_ij"), "geo": geo, "quelle": f})
    return out


def abstand_punkte_polylinie(x, y, P):
    """Abstand vieler Punkte (Arrays) zu einer Polylinie P (N x 2, m)."""
    x = np.asarray(x, np.float64)[:, None]
    y = np.asarray(y, np.float64)[:, None]
    if len(P) == 1:
        return np.hypot(x - P[0, 0], y - P[0, 1])[:, 0]
    a, b = P[:-1], P[1:]
    ab = b - a
    t = np.clip(((x - a[:, 0]) * ab[:, 0] + (y - a[:, 1]) * ab[:, 1]) / np.maximum((ab ** 2).sum(1), 1e-9), 0, 1)
    d = np.hypot(x - (a[:, 0] + t * ab[:, 0]), y - (a[:, 1] + t * ab[:, 1]))
    return d.min(axis=1)


def im_fenster_ij(x, y, fij):
    """Punkte (m) im 1-m-Fenster [i0, j0, hoehe, breite] (SEHENS_FORMAT §2)?"""
    if not fij:
        return np.zeros(np.shape(x), bool)
    i0, j0, h, w = fij
    i = np.asarray(y) + 4060.5
    j = np.asarray(x) + 4730.5
    return (i >= i0) & (i < i0 + h) & (j >= j0) & (j < j0 + w)


def umbau_ueberlappung(proben, umbau, abstand_m=15.0):
    """Je Sehens-Ort: Laenge (m) der Strecke, die im Gelaendefenster liegt UND <= abstand_m von dessen Wasser
    verlaeuft (bei ist_wasser auch <= Ortsradius von der Mitte). proben: dict x, y, s (2-m-Proben).
    Rueckgabe Liste {ort, biom, laenge_m, anteil, geo: [Kennungen]} (> 0 m)."""
    x, y, s = proben["x"], proben["y"], proben["s"]
    ds = np.gradient(s) if len(s) > 1 else np.ones(1)
    out = []
    for o in umbau:
        innen = im_fenster_ij(x, y, o["fenster_ij"]) if o["fenster_ij"] else \
            (np.hypot(x - o["x_m"], y - o["y_m"]) <= o["radius_m"] + 40.0)
        if not innen.any():
            continue
        nah = np.zeros(len(x), bool)
        kenn = []
        for art, wid, P in o["geo"]:
            d = abstand_punkte_polylinie(x, y, P)
            m = d <= abstand_m
            if (m & innen).any():
                kenn.append("%s:%s" % (art, wid))
            nah |= m
        if o["ist_wasser"]:
            m = np.hypot(x - o["x_m"], y - o["y_m"]) <= o["radius_m"]
            if (m & innen).any():
                kenn.append("ist_wasser")
            nah |= m
        sel = innen & nah
        L = float(ds[sel].sum())
        if L > 0:
            out.append({"ort": o["id"], "biom": o["biom"], "laenge_m": round(L, 1),
                        "anteil": round(L / max(float(ds.sum()), 1e-6), 3), "geo": kenn})
    out.sort(key=lambda e: -e["laenge_m"])
    return out


def gebaute_stufen():
    """Schon mit Stufen gebaute Laeufe (vorlagen/daten/wasser_fx/stufen.json) + Wasser-FX-Gruppen aus Auftrag 14
    (antworten/wasser_fx/plan.json). Rueckgabe dict lauf -> {stufen, fx_gruppen, fx_effekte}."""
    out = {}
    if os.path.exists(STUFEN_FX):
        d = lese_json(STUFEN_FX)
        for s in d.get("stufen", []):
            e = out.setdefault(s["fluss"], {"stufen": [], "fx_gruppen": set(), "fx_effekte": 0})
            e["stufen"].append(s["id"])
    if os.path.exists(WASSER_FX_PLAN):
        p = lese_json(WASSER_FX_PLAN)
        for e in p.get("effekte", []):
            z = str(e.get("ziel", ""))
            for lid in out:
                if z.startswith(lid):
                    out[lid]["fx_gruppen"].add(e.get("gruppe"))
                    out[lid]["fx_effekte"] += 1
    for v in out.values():
        v["fx_gruppen"] = sorted(g for g in v["fx_gruppen"] if g)
    return out
