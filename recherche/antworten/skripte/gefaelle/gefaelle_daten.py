# -*- coding: utf-8 -*-
"""gefaelle_daten.py - gemeinsame Daten fuer Auftrag 15 (steile Fluss-/Bachstrecken): Strecken, Laeufe, Sehens-Orte.

Wird von gefaelle_prioritaet.py, gefaelle_plan.py und gefaelle_pruefen.py importiert (python -I: der Planer setzt
seinen Ordner selbst in sys.path).

  strecken = lade_strecken(pfad)            # 161 Strecken mit stabiler id <lauf>_s<k> (k = Reihenfolge im Lauf),
                                            # ohne die Strecken ersetzter Laeufe (16h, fluss_sim/ersetzt.json): 157
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
# Feldgrenzen: Ueberlappung zweier Welt-Laeufe (16d Antwort Punkt 3, 16c Nachtrag 3)
# ----------------------------------------------------------------------------------------------------------------------
FORTSETZUNG_STANDARD = {"fortsetzung_abstand_m": 8.0, "fortsetzung_ueberlappung_max_m": 40.0, "fortsetzung_quer_m": 1.0,
                        "ueberlappung_dz_max_cm": 500.0}
FLUSS_SIM_REGELN = os.path.join(SKRIPTE, "fluss_sim", "fluss_sim_regeln.json")


def fortsetzung_regeln():
    """Kriterien wie fluss_sim_regeln.json 'gewaesser' (gleiche Verkettung wie der Export), sonst Standardwerte."""
    r = dict(FORTSETZUNG_STANDARD)
    try:
        g = lese_json(FLUSS_SIM_REGELN)["gewaesser"]
        for k in r:
            if k in g:
                r[k] = float(g[k])
    except (OSError, KeyError, ValueError):
        pass
    return r


# ----------------------------------------------------------------------------------------------------------------------
# Ersetzte Laeufe (Auftrag 16h): lokal durch einen eigenen Lauf ersetzt (Erlenbach p2) -> alle Planer ueberspringen sie
# ----------------------------------------------------------------------------------------------------------------------
ERSETZT_STANDARD = os.path.join(SKRIPTE, "fluss_sim", "ersetzt.json")
_ERSETZT = {}


def ersetzt_daten(pfad=None):
    """Inhalt von fluss_sim/ersetzt.json (16h); {} ohne Datei. Gecacht je Pfad."""
    pfad = pfad or ERSETZT_STANDARD
    if pfad not in _ERSETZT:
        try:
            _ERSETZT[pfad] = lese_json(pfad)
        except (OSError, ValueError):
            _ERSETZT[pfad] = {}
    return _ERSETZT[pfad]


def ersetzte_laeufe(pfad=None):
    """{lauf_id: eintrag} der ersetzten Welt-Laeufe (Eintraege mit 'aktiv': false zaehlen nicht)."""
    L = ersetzt_daten(pfad).get("laeufe") or {}
    return {k: v for k, v in sorted(L.items()) if v.get("aktiv", True)}


def ist_ersetzt(lauf_id, pfad=None):
    return lauf_id in ersetzte_laeufe(pfad)


def ohne_ersetzte(wasser_welt, baeche, pfad=None):
    """Kopien von wasser_welt (nur 'fluesse' gefiltert) und der Bachliste ohne ersetzte Laeufe."""
    E = ersetzte_laeufe(pfad)
    ww = dict(wasser_welt or {})
    if "fluesse" in ww:
        ww["fluesse"] = [f for f in ww.get("fluesse") or [] if f.get("id") not in E]
    return ww, [b for b in (baeche or []) if b.get("id") not in E]


def alle_laeufe(welt, baeche=None, wasser_welt=None, mit_ersetzten=False):
    """{id: Lauf} aller Welt-Laeufe (wasser_welt.json 'fluesse', Baeche), ohne die ersetzten (16h, ersetzt.json)."""
    ww = wasser_welt if wasser_welt is not None else (welt.wasser_welt or {})
    E = {} if mit_ersetzten else ersetzte_laeufe()
    out = {}
    for f in ww.get("fluesse", []) or []:
        if f["id"] in E:
            continue
        out[f["id"]] = Lauf(f["id"], "fluss", f["punkte"], f.get("feld"), "wasser_welt.json")
    for b in (baeche if baeche is not None else welt.baeche) or []:
        if b["id"] in E:
            continue
        if b["id"] not in out and len(b.get("punkte") or []) >= 2:
            out[b["id"]] = Lauf(b["id"], "bach", b["punkte"], b.get("feld"), "baeche_alle.json")
    return out


def _feld_bei(lauf, s):
    from sehens_lib import daten as _d
    d = lauf.bei_s(np.atleast_1d(np.asarray(s, np.float64)))
    return [_d.feld_von_m(float(x), float(y)) for x, y in zip(d["x"], d["y"])]


def _ueberlappung(P, N, G):
    """Wie fluss_sim_export.fortsetzung_test (art 'ueberlappung'): Ende von P liegt <= quer auf N bei s <= max, Anfang
    von N <= quer auf P bei s >= Laenge - max, kein Anschluss (Ende-Anfang > fortsetzung_abstand_m)."""
    ex, ey = P.xy[-1]
    ax, ay = N.xy[0]
    if math.hypot(ex - ax, ey - ay) <= G["fortsetzung_abstand_m"]:
        return None
    ue = G["fortsetzung_ueberlappung_max_m"]
    sn, dn = N.s_von_m(ex, ey)
    if dn > G["fortsetzung_quer_m"] or not (0.0 < sn <= ue):
        return None
    if abs(float(np.interp(sn, N.s, N.z)) - float(P.z[-1])) * 100.0 > G["ueberlappung_dz_max_cm"]:
        return None
    sp, dp = P.s_von_m(ax, ay)
    if dp > G["fortsetzung_quer_m"] or not (P.laenge_m - ue <= sp < P.laenge_m):
        return None
    return sp, sn


def feldgrenzen(lauf_id, laeufe, schritt_m=0.25):
    """Ueberlappungen des Laufs mit Nachbarlaeufen an Feldgrenzen (zwei Plaene uebereinander). Regel (Koordinator 16c
    Nachtrag 3): Eine Stufe gehoert nur in EINEN Plan. Der Plan, in dessen Feld die Lippe liegt, behaelt sie; der
    andere laesst die Ueberlappung frei (Spiegel bleibt dort alt, der Plan schliesst mit passendem Spiegel an).
    Liegen beide Laeufe im selben Feld (Verlaengerungen wie *_1V_C2 -> *_2_C2), gehoert die Ueberlappung dem oberen.
    Passender Spiegel: Der untere Lauf schliesst erst dort an, wo sein alter Spiegel nicht ueber dem des oberen liegt
    (die Feld-Stuecke weichen in der Ueberlappung bis ~0,7 m voneinander ab); seine Lippen davor entfallen.
    Rueckgabe: Liste {nachbar, seite ('ende' = Lauf ist oben, 'anfang' = Lauf ist unten), ueberlappung_s_m (eigenes s),
    feldgrenze_s_m (Feldwechsel), grenze_s_m (eigenes s: Anschluss, hier schneidet der Export die Kette), fremd_s_m
    ([a, b] oder None: dort setzt dieser Lauf keine Stufe), eigen_feld, nachbar_feld, regel}."""
    G = fortsetzung_regeln()
    X = laeufe[lauf_id]
    out = []
    for nid in sorted(laeufe):
        if nid == lauf_id:
            continue
        Y = laeufe[nid]
        for P, N, seite in ((X, Y, "ende"), (Y, X, "anfang")):
            r = _ueberlappung(P, N, G)
            if r is None:
                continue
            sp, sn = r
            gleich = not P.feld or not N.feld or P.feld == N.feld
            if gleich:
                g_p, g_n = P.laenge_m, sn
                regel = "gleiches Feld %s: Ueberlappung gehoert dem oberen Lauf" % (P.feld,)
            else:
                ss_p = np.arange(sp, P.laenge_m + 1e-9, schritt_m)
                fp = _feld_bei(P, ss_p)
                k = next((i for i, f in enumerate(fp) if f != P.feld), None)
                g_p = float(ss_p[k]) if k is not None else P.laenge_m
                ss_n = np.arange(0.0, sn + 1e-9, schritt_m)
                fn = _feld_bei(N, ss_n)
                k = next((i for i, f in enumerate(fn) if f == N.feld), None)
                g_n = float(ss_n[k]) if k is not None else sn
                regel = "Feldgrenze %s/%s: Lippe gehoert dem Plan ihres Felds" % (P.feld, N.feld)
            # passender Spiegel: der untere Lauf schliesst erst dort an, wo sein (alter) Spiegel nicht ueber dem des
            # oberen liegt (die Feld-Laeufe weichen in der Ueberlappung bis ~0,7 m voneinander ab); davor setzt er keine
            # Lippe. Schnitt = Anschluss: unten bei s_n*, oben bei der Projektion desselben Punkts.
            ss_a = np.arange(g_n, sn + 1e-9, schritt_m)
            dn_ = N.bei_s(ss_a)
            s_an = sn
            for k_, (x_, y_, z_) in enumerate(zip(dn_["x"], dn_["y"], dn_["z"])):
                sp_k, _ = P.s_von_m(float(x_), float(y_))
                if float(z_) <= float(np.interp(sp_k, P.s, P.z)) + 0.02:
                    s_an = float(ss_a[k_])
                    break
            xa, ya = float(np.interp(s_an, N.s, N.xy[:, 0])), float(np.interp(s_an, N.s, N.xy[:, 1]))
            s_ap = min(P.s_von_m(xa, ya)[0], P.laenge_m)
            if seite == "ende":
                ue_s = [round(sp, 2), round(X.laenge_m, 2)]
                grenze, fg_ = s_ap, g_p
                fremd = [round(g_p, 2), round(X.laenge_m, 2)] if g_p < X.laenge_m - 1e-6 else None
            else:
                ue_s = [0.0, round(sn, 2)]
                grenze, fg_ = s_an, g_n
                fremd = [0.0, round(s_an, 2)] if s_an > 1e-6 else None
            out.append({"nachbar": nid, "seite": seite, "ueberlappung_s_m": ue_s, "grenze_s_m": round(grenze, 2),
                        "feldgrenze_s_m": round(fg_, 2), "fremd_s_m": fremd, "eigen_feld": X.feld,
                        "nachbar_feld": Y.feld, "regel": regel + ("; Anschluss erst bei passendem Spiegel (unten s %.1f "
                                                                   "statt %.1f m)" % (s_an, g_n) if s_an > g_n + 0.01
                                                                   else "")})
    return out


# ----------------------------------------------------------------------------------------------------------------------
# Strecken
# ----------------------------------------------------------------------------------------------------------------------
def lade_strecken(pfad=None, welt=None, baeche=None, wasser_welt=None):
    """Liste der steilen Strecken (steile_strecken.json) mit stabiler id <lauf>_s<k> (k ab 1 in Fliessrichtung).
    Mit welt: zusaetzlich s0_m/s1_m (Bogenlaenge auf dem Lauf) und abstand_projektion_m."""
    d = lese_json(pfad or STRECKEN_STANDARD)
    E = ersetzte_laeufe()
    st = [dict(x) for x in d["strecken"] if x["lauf"] not in E]
    d = dict(d, ersetzt_uebersprungen=sorted({x["lauf"] for x in d["strecken"] if x["lauf"] in E}),
             ersetzt_strecken=sum(1 for x in d["strecken"] if x["lauf"] in E))
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


# 16h (13.10.): C2 (F_ERLENBACH_1_C2/_1V_C2/_2_C2, B_R3_K10_TUNDRA_01) ist lokal durch Erlenbach p2 ersetzt
# (fluss_sim/ersetzt.json). lade_strecken/alle_laeufe ueberspringen diese Laeufe; die Eintraege unten bleiben nur als
# Geschichte (wirken nicht mehr, weil es keinen C2-Plan mehr gibt).
# 14b (11.10.): C2 auf einen durchgehenden Fluss zurueckgestellt, Stufen-Akteure entfernt -> nicht mehr "gebaut";
# A15 plant C2 vollstaendig (Kaskadennetz) und ersetzt die A14-Eintraege (Koordinator 11.10.)
ZURUECKGESTELLT = {"F_ERLENBACH_1V_C2": "14b: durchgehender Fluss, Stufen-Akteure entfernt; A15 ersetzt A14 (C2_A-C2_E)"}
PILOT_VORGABE = {"F_ERLENBACH_1V_C2_s1": "Koordinator 11.10.: C2 als Pilot Rang 1 (Ferat schaut dort hin)"}


def vorgabe_stufen(lauf_id):
    """Gebaute/geplante Stufenlagen aus vorlagen/daten/wasser_fx/stufen.json (Vorgabe fuer C2/H4)."""
    if not os.path.exists(STUFEN_FX):
        return []
    return [s for s in lese_json(STUFEN_FX).get("stufen", []) if s.get("fluss") == lauf_id]


def a14_gruppen(lauf_id):
    """Effekt-Gruppen aus antworten/wasser_fx/plan.json fuer einen Lauf: {gruppe: [effekt-ziele]}."""
    if not os.path.exists(WASSER_FX_PLAN):
        return {}
    out = {}
    for e in lese_json(WASSER_FX_PLAN).get("effekte", []):
        if str(e.get("ziel", "")).startswith(lauf_id):
            out.setdefault(e.get("gruppe"), []).append("%s:%s" % (e.get("ziel"), str(e.get("asset", "")).rsplit("/", 1)[-1]))
    return out


def gebaute_stufen():
    """Schon mit Stufen gebaute Laeufe (vorlagen/daten/wasser_fx/stufen.json) + Wasser-FX-Gruppen aus Auftrag 14
    (antworten/wasser_fx/plan.json). Rueckgabe dict lauf -> {stufen, fx_gruppen, fx_effekte}."""
    out = {}
    if os.path.exists(STUFEN_FX):
        d = lese_json(STUFEN_FX)
        for s in d.get("stufen", []):
            if s["fluss"] in ZURUECKGESTELLT:
                continue
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


# ======================================================================================================================
# 1-m-Hoehenfenster (Auftrag 15b): heutiges Gelaende in 1 m um die Pilotlaeufe, fuer exakte Bett-/Uferpruefung
# ======================================================================================================================
HOEHE1M_STANDARD = os.path.join(RECHERCHE, "vorlagen", "daten", "gefaelle", "hoehe_1m_fenster")
OFF_J_1M, OFF_I_1M = 4730.5, 4060.5          # Zelle (j, i) -> X = j - 4730,5 m, Y = i - 4060,5 m


class Hoehe1m:
    """Hoehenfenster in 1 m (uint16-PNG, H = 300 + (v - 32768) / 64 m) aus fenster.json. hoehe(x, y) bilinear in den
    Fenstern, ausserhalb Rueckfall (z. B. welt 2 m bilinear). Fenster ueberlappen nicht oder sind dort gleich."""

    def __init__(self, ordner, rueckfall=None):
        from PIL import Image
        with open(os.path.join(ordner, "fenster.json"), "r", encoding="utf-8") as f:
            meta = json.load(f)
        self.ordner = ordner
        self.rueckfall = rueckfall
        self.fenster = []
        for fid, w in sorted(meta["fenster"].items()):
            a = np.asarray(Image.open(os.path.join(ordner, w["datei"])), dtype=np.float64)
            a = 300.0 + (a - 32768.0) / 64.0
            if a.shape != (w["ni"], w["nj"]):
                raise ValueError("%s: Groesse %s != %s" % (w["datei"], a.shape, (w["ni"], w["nj"])))
            self.fenster.append((fid, int(w["i0"]), int(w["j0"]), a))

    def ids(self):
        return [f[0] for f in self.fenster]

    def deckt(self, x_m, y_m):
        x = np.asarray(x_m, np.float64)
        y = np.asarray(y_m, np.float64)
        m = np.zeros(np.broadcast(x, y).shape, bool)
        for _, i0, j0, a in self.fenster:
            fi, fj = y + OFF_I_1M - i0, x + OFF_J_1M - j0
            m |= (fi >= 0) & (fi <= a.shape[0] - 1) & (fj >= 0) & (fj <= a.shape[1] - 1)
        return m

    def hoehe(self, x_m, y_m):
        x = np.asarray(x_m, np.float64)
        y = np.asarray(y_m, np.float64)
        shp = np.broadcast(x, y).shape
        x, y = np.broadcast_to(x, shp), np.broadcast_to(y, shp)
        out = np.full(shp, np.nan)
        for _, i0, j0, a in self.fenster:
            fi, fj = y + OFF_I_1M - i0, x + OFF_J_1M - j0
            innen = (fi >= 0) & (fi <= a.shape[0] - 1) & (fj >= 0) & (fj <= a.shape[1] - 1) & np.isnan(out)
            if not innen.any():
                continue
            i = np.clip(np.floor(fi[innen]).astype(np.int64), 0, a.shape[0] - 2)
            j = np.clip(np.floor(fj[innen]).astype(np.int64), 0, a.shape[1] - 2)
            di = np.clip(fi[innen] - i, 0, 1)
            dj = np.clip(fj[innen] - j, 0, 1)
            out[innen] = (a[i, j] * (1 - di) * (1 - dj) + a[i, j + 1] * (1 - di) * dj + a[i + 1, j] * di * (1 - dj) +
                          a[i + 1, j + 1] * di * dj)
        rest = np.isnan(out)
        if rest.any():
            if self.rueckfall is None:
                raise ValueError("Punkt ausserhalb der 1-m-Fenster und kein Rueckfall")
            out[rest] = self.rueckfall(x[rest], y[rest])
        return out

    def raster(self, i0, j0, ni, nj):
        """1-m-Raster (ni x nj) ab globaler 1-m-Zelle (i0, j0): Zellmitten X = j - 4730,5, Y = i - 4060,5."""
        jj, ii = np.meshgrid(np.arange(j0, j0 + nj, dtype=np.float64), np.arange(i0, i0 + ni, dtype=np.float64))
        return self.hoehe(jj - OFF_J_1M, ii - OFF_I_1M)


class BodenNachStempel1m:
    """Wie sehens_lib.sehens_pruefen.BodenNachStempel (Gelaende + 1-m-Deltas aus gelaende/*.f32), nur mit den
    1-m-Hoehenfenstern als altem Gelaende (Auftrag 15b: exakte Bett-/Uferpruefung auf 1 m)."""

    def __init__(self, welt, abschnitte, basis, h1m):
        from sehens_lib.sehens_pruefen import BodenNachStempel
        self._b = BodenNachStempel(welt, abschnitte, basis)
        self.h1m = h1m

    def delta(self, x_m, y_m):
        return self._b.delta(x_m, y_m)

    def alt(self, x_m, y_m):
        return self.h1m.hoehe(x_m, y_m)

    def hoehe(self, x_m, y_m):
        return self.h1m.hoehe(x_m, y_m) + self._b.delta(x_m, y_m)
