"""steilwand.py - Auftrag 13h: neue steile Gelaendeflaechen nur mit Fels-Verkleidung.

Befund aus dem ersten Editor-Pilot (Karsee): Der Stempel schnitt fast senkrechte, glatte Erdwaende aus dem Hang. Auf
solchen Flaechen dehnt das Landschaftsmaterial die UV (senkrechte Streifen) - "Steinbruch statt Kar". Regel (Ferat):
neue Flaechen steiler als 45 Grad nur dort, wo Fels-Akteure (Wand-/Klippennetze) sie verkleiden; sonst flacher stempeln.

Pruefer-Regel (sehens_pruefen, FEHLER):
  Nach dem Stempel > 20 m2 zusammenhaengend (8er-Nachbarschaft, 1-m-Raster) mit > 45 Grad Neigung, die der Stempel
  neu geschaffen hat (|Delta| > 0,25 m und Neigung um > 5 Grad steiler als vorher), ohne Fels-Akteur, der die Zellen
  deckt (XY-Huelle seiner gedrehten Bounds, Bodenhoehe der Zelle zwischen Unter- und Oberkante +- 1 m).
  Ausgenommen: unter dem Spiegel eigener Seen (Seegrund) und das benetzte Bett der Baeche (halbe Breite + 1 m;
  Stufen bleiben wie 13f, Ferat 13g).

Werkzeuge (Planer):
  Stempel.boeschung(...)          -> stempel.py: Schuettkegel-Begrenzung (nur auffuellen, 30-35 Grad Halde)
  Gruppe "verteilung": {"typ": "steilwand", ...} -> rezept.py: verkleidet die neuen steilen Flaechen automatisch mit
                                     Wand-/Klippennetzen (gierige Ueberdeckung, Front zur Talseite, front_an_linie)
  Ort-Feld "gelaende": {"max_neigung_grad": 35}  -> flacher stempeln (Schuettkegel), wo nicht verkleidet wird

API:
  neigung_grad(h, zelle_m)                       -> Grad
  neue_steil_maske(h0, h1, ...)                  -> bool (neu steil)
  komponenten(maske)                             -> (labels int32, flaechen_zellen list)  (ohne SciPy)
  huelle(punkte)                                 -> konvexe Huelle [[x, y], ...]
  in_polygon(x, y, poly)                         -> bool Array
  ist_fels(name_oder_pfad)                       -> True fuer Fels-/Klippen-/Wandnetze (Heuristik ueber den Namen)
  abdruck(info, q, s, x_cm, y_cm, z_cm)          -> {"poly": [[x, y] m], "zmin", "zmax"}
  deckung(X, Y, H, abdruecke, rand_m, z_tol_m)   -> bool (gedeckte Zellen)
  pruefe_ort_steil(o, basis, welt, akteure, inv) -> Befunde (FEHLER/HINWEIS)
"""

import math
import os
import re

import numpy as np

from . import daten as _daten

GRENZE_GRAD = 45.0          # Ferat 13h: "steiler als ~45 Grad"
MIN_FLAECHE_M2 = 20.0       # zusammenhaengend > 20 m2 -> FEHLER
MIN_DELTA_M = 0.25          # nur Zellen, die der Stempel merklich geaendert hat
MEHR_GRAD = 5.0             # ... und die dadurch steiler geworden sind (bestehende Felswaende zaehlen nicht)
RAND_M = 0.5                # Abdruck-Toleranz (Netze ragen ueber die Box-Huelle hinaus, Interpolation)
Z_TOL_M = 1.0

FELS_MUSTER = re.compile(r"(rock|cliff|boulder|stone|basalt|fels|wall|formation|ledge|slab|crag|outcrop|scree|"
                         r"_tier_\d|embankment|lava_wall|spire|pillar)", re.I)
KEIN_FELS_MUSTER = re.compile(r"(root|tree|pine|fir_|log|branch|moss_|mossclump|fern|grass|bush|plant|stump|"
                              r"mushroom|leaf|decal|stones_roots)", re.I)


# ============================================================================================
# Raster
# ============================================================================================
def neigung_grad(h, zelle_m=1.0):
    """Neigung (Grad) mit zentralen Differenzen (Rand einseitig)."""
    gy, gx = np.gradient(np.asarray(h, np.float64), float(zelle_m))
    return np.degrees(np.arctan(np.hypot(gx, gy)))


def neue_steil_maske(h0, h1, zelle_m=1.0, grenze_grad=GRENZE_GRAD, min_delta_m=MIN_DELTA_M, mehr_grad=MEHR_GRAD,
                     ausnahme=None):
    """Zellen, die der Stempel steiler als grenze_grad gemacht hat (|h1-h0| > min_delta, Neigung +mehr_grad)."""
    s0 = neigung_grad(h0, zelle_m)
    s1 = neigung_grad(h1, zelle_m)
    m = (s1 > grenze_grad) & (np.abs(np.asarray(h1) - np.asarray(h0)) > min_delta_m) & (s1 > s0 + mehr_grad)
    if ausnahme is not None:
        m &= ~ausnahme
    return m


def komponenten(maske):
    """Zusammenhaengende Gebiete (8er-Nachbarschaft). Rueckgabe (labels [0 = leer, 1..n], [Zellen je Label])."""
    m = np.asarray(maske, bool)
    lab = np.zeros(m.shape, np.int32)
    groessen = []
    h, w = m.shape
    ii, jj = np.nonzero(m)
    n = 0
    for a, b in zip(ii.tolist(), jj.tolist()):
        if lab[a, b]:
            continue
        n += 1
        lab[a, b] = n
        stapel = [(a, b)]
        k = 0
        while stapel:
            i, j = stapel.pop()
            k += 1
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    p, q = i + di, j + dj
                    if 0 <= p < h and 0 <= q < w and m[p, q] and not lab[p, q]:
                        lab[p, q] = n
                        stapel.append((p, q))
        groessen.append(k)
    return lab, groessen


# ============================================================================================
# Geometrie
# ============================================================================================
def huelle(punkte):
    """Konvexe Huelle (Andrew), gegen den Uhrzeigersinn in X/Y."""
    P = sorted(set((round(float(x), 4), round(float(y), 4)) for x, y in punkte))
    if len(P) <= 2:
        return [list(p) for p in P]

    def kreuz(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    unten, oben = [], []
    for p in P:
        while len(unten) >= 2 and kreuz(unten[-2], unten[-1], p) <= 0:
            unten.pop()
        unten.append(p)
    for p in reversed(P):
        while len(oben) >= 2 and kreuz(oben[-2], oben[-1], p) <= 0:
            oben.pop()
        oben.append(p)
    return [list(p) for p in unten[:-1] + oben[:-1]]


def in_polygon(x, y, poly, rand_m=0.0):
    """Punkte (Arrays) in einem konvexen oder einfachen Polygon; rand_m > 0 erweitert konvexe Polygone nach aussen."""
    x = np.asarray(x, np.float64)
    y = np.asarray(y, np.float64)
    U = np.asarray(poly, np.float64)
    n = len(U)
    if n < 3:
        return np.zeros(np.broadcast(x, y).shape, bool)
    innen = np.zeros(np.broadcast(x, y).shape, bool)
    j = n - 1
    for i in range(n):
        xi, yi = U[i]
        xj, yj = U[j]
        c = ((yi > y) != (yj > y)) & (x < (xj - xi) * (y - yi) / ((yj - yi) if yj != yi else 1e-12) + xi)
        innen ^= c
        j = i
    if rand_m > 0:
        # Abstand zu den Kanten <= rand_m zaehlt mit
        d = np.full(innen.shape, np.inf)
        for i in range(n):
            a = U[i]
            b = U[(i + 1) % n]
            ab = b - a
            L2 = max(float(ab @ ab), 1e-12)
            t = np.clip(((x - a[0]) * ab[0] + (y - a[1]) * ab[1]) / L2, 0, 1)
            d = np.minimum(d, np.hypot(a[0] + t * ab[0] - x, a[1] + t * ab[1] - y))
        innen |= d <= rand_m
    return innen


def ist_fels(s):
    """Fels-/Klippen-/Wandnetz? (Heuristik ueber Name/Pfad - Megascans-Scans *_tier_N zaehlen als Fels.)"""
    s = str(s or "")
    name = s.rsplit("/", 1)[-1]
    if KEIN_FELS_MUSTER.search(name):
        return False
    return bool(FELS_MUSTER.search(name) or ("/Rocks/" in s) or ("/Cliffs/" in s))


def abdruck(info, q, s, x_cm, y_cm, z_cm):
    """Grundriss (konvexe Huelle der gedrehten Bounds, m) und Hoehenbereich (m) eines gesetzten Netzes."""
    from . import instanzen as _ins
    P = _ins.gedrehte_box(info, q, s)
    xs = (x_cm + P[:, 0]) / 100.0
    ys = (y_cm + P[:, 1]) / 100.0
    zs = (z_cm + P[:, 2]) / 100.0
    return {"poly": huelle(zip(xs, ys)), "zmin": float(zs.min()), "zmax": float(zs.max()),
            "box": (float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max()))}


def deckung(X, Y, H, abdruecke, rand_m=RAND_M, z_tol_m=Z_TOL_M, nur=None):
    """Zellen (Mitten X/Y, Boden H), die ein Abdruck deckt (im Grundriss und Boden im Hoehenbereich +- z_tol)."""
    X = np.asarray(X, np.float64)
    Y = np.asarray(Y, np.float64)
    H = np.asarray(H, np.float64)
    g = np.zeros(X.shape, bool)
    for a in abdruecke:
        x0, y0, x1, y1 = a["box"]
        sel = (X >= x0 - rand_m) & (X <= x1 + rand_m) & (Y >= y0 - rand_m) & (Y <= y1 + rand_m)
        if nur is not None:
            sel &= nur
        if not sel.any():
            continue
        sel &= (H >= a["zmin"] - z_tol_m) & (H <= a["zmax"] + z_tol_m)
        if not sel.any():
            continue
        ii = np.nonzero(sel)
        g[ii] |= in_polygon(X[ii], Y[ii], a["poly"], rand_m)
    return g


# ============================================================================================
# Pruefer
# ============================================================================================
def _gitter_1m(fij):
    i0, j0, hh, ww = fij
    x = np.arange(j0, j0 + ww, dtype=np.float64) - _daten.OFF_J
    y = np.arange(i0, i0 + hh, dtype=np.float64) - _daten.OFF_I
    return np.meshgrid(x, y)


def ausnahme_wasser(o, X, Y, H1, zelle_m=1.0):
    """Seegrund (im Umriss, unter dem Spiegel + 0,05 m) und benetztes Bachbett (halbe Breite + 1 m)."""
    from . import stempel as _stm
    from . import bach as _b
    aus = np.zeros(X.shape, bool)
    for w in o.get("wasser", []) or []:
        if w.get("typ") == "see" and w.get("umriss_cm") and isinstance(w.get("spiegel_cm"), (int, float)):
            U = np.asarray(w["umriss_cm"], np.float64)[:, :2] / 100.0
            aus |= in_polygon(X, Y, U) & (H1 <= float(w["spiegel_cm"]) / 100.0 + 0.05)
        elif w.get("typ") == "bach" and w.get("punkte_cm") and len(w["punkte_cm"]) >= 2:
            P = np.asarray(w["punkte_cm"], np.float64)
            r = _b.halbe_breite_eff(float(P[0][3]) / 100.0 if P.shape[1] > 3 else 2.0, zelle_m) + 1.0
            x0, y0 = P[:, 0].min() / 100.0 - r - 2, P[:, 1].min() / 100.0 - r - 2
            x1, y1 = P[:, 0].max() / 100.0 + r + 2, P[:, 1].max() / 100.0 + r + 2
            sel = (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
            if sel.any():
                d, _, _ = _stm.polylinie_abstand(X[sel], Y[sel], P[:, :2] / 100.0)
                tmp = np.zeros(X.shape, bool)
                tmp[sel] = d <= r
                aus |= tmp
        elif w.get("typ") == "wasserfall" and w.get("kante_cm"):
            pass
    return aus


def fels_abdruecke(akteure, inv, ort_id=None):
    """Abdruecke aller Fels-Akteure (eines Orts) aus plan.json-Akteuren."""
    out = []
    for e in akteure or []:
        if ort_id and not str(e.get("klasse", "")).startswith(ort_id + "_"):
            continue
        r = e.get("rolle")
        if not (r in ("fels", "stein") if r is not None else ist_fels(e.get("pfad") or e.get("netz"))):
            continue
        try:
            info = inv.netz(e.get("pfad") or e["netz"])
        except KeyError:
            continue
        q = (e["qx"], e["qy"], e["qz"], e["qw"])
        out.append(dict(abdruck(info, q, (e["sx"], e["sy"], e["sz"]), e["x"], e["y"], e["z"]), netz=e.get("netz")))
    return out


def steil_befund(o, basis, welt, abdruecke):
    """Rechnet die Regel fuer einen orte.json-Eintrag. Rueckgabe dict oder None (kein Stempel):
    {"komponenten": [(flaeche_m2, gedeckt_m2, ungedeckt_m2, (x, y))], "neu_m2", "gedeckt_m2"}"""
    g = o.get("gelaende") or {}
    fij = g.get("fenster_ij")
    if not (basis and g.get("datei") and isinstance(fij, list) and len(fij) == 4):
        return None
    pf = os.path.join(basis, g["datei"])
    if not (os.path.exists(pf) and os.path.getsize(pf) == fij[2] * fij[3] * 4):
        return None
    a = np.fromfile(pf, dtype="<f4").reshape(fij[2], fij[3]).astype(np.float64)
    if not (np.abs(a) > MIN_DELTA_M).any():
        return {"komponenten": [], "neu_m2": 0, "gedeckt_m2": 0}
    X, Y = _gitter_1m(fij)
    h0 = welt.bilinear(welt.hoehe, X, Y)
    h1 = h0 + a
    aus = ausnahme_wasser(o, X, Y, h1, welt.zelle_m)
    neu = neue_steil_maske(h0, h1, 1.0, ausnahme=aus)
    ged = deckung(X, Y, h1, abdruecke, nur=neu) & neu
    lab, gr = komponenten(neu & ~ged)
    kompo = []
    for k, n in enumerate(gr, start=1):
        if n <= 0:
            continue
        sel = lab == k
        kompo.append((int(n), (float(X[sel].mean()), float(Y[sel].mean())),
                      float(h1[sel].max() - h1[sel].min())))
    kompo.sort(key=lambda t: -t[0])
    return {"komponenten": kompo, "neu_m2": int(neu.sum()), "gedeckt_m2": int(ged.sum())}


def pruefe_ort_steil(o, basis, welt, abdruecke, min_flaeche_m2=MIN_FLAECHE_M2):
    """Befunde: FEHLER je Gebiet > min_flaeche_m2 neu steil ohne Fels-Deckung; HINWEIS mit der Bilanz."""
    oid = o.get("id", "?")
    r = steil_befund(o, basis, welt, abdruecke)
    if r is None:
        return []
    b = []
    gross = [k for k in r["komponenten"] if k[0] > min_flaeche_m2]
    for n, (x, y), dh in gross[:8]:
        b.append(("FEHLER", oid, "Gelaende: %d m2 zusammenhaengend > %.0f Grad neu steil ohne Fels-Akteur bei "
                                 "(%.0f, %.0f) m, %.1f m hoch (13h: verkleiden oder flacher stempeln)"
                  % (n, GRENZE_GRAD, x, y, dh)))
    if len(gross) > 8:
        b.append(("FEHLER", oid, "Gelaende: %d weitere steile Gebiete > %.0f m2" % (len(gross) - 8, min_flaeche_m2)))
    if r["neu_m2"]:
        rest = sum(k[0] for k in r["komponenten"])
        b.append(("HINWEIS", oid, "Steilflaechen (13h): %d m2 neu > %.0f Grad, davon %d m2 mit Fels verkleidet, %d m2 "
                                  "offen in Gebieten <= %.0f m2" % (r["neu_m2"], GRENZE_GRAD, r["gedeckt_m2"],
                                                                     rest - sum(k[0] for k in gross), min_flaeche_m2)))
    return b
