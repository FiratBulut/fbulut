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


# ============================================================================================
# Planer (rezept.OrtKontext): flacher stempeln, Halde, Verkleidung
# ============================================================================================
_GEF = {"geladen": False, "biome": {}}


def biom_netze(biom):
    """Netzlisten des Bioms aus dem Regelwerk Auftrag 15 (gefaelle_regeln.json: biome.<biom>.netze/lagen):
    'wand' (Klippen/Waende), 'schutt', 'bloecke', 'riegel', 'kies' ... und 'lagen'."""
    if not _GEF["geladen"]:
        import json
        pf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gefaelle", "gefaelle_regeln.json")
        try:
            with open(pf, "r", encoding="utf-8") as f:
                _GEF["biome"] = json.load(f).get("biome", {})
        except (OSError, ValueError):
            _GEF["biome"] = {}
        _GEF["geladen"] = True
    b = _GEF["biome"].get(biom) or {}
    out = dict(b.get("netze") or {})
    out["_lagen"] = b.get("lagen") or {}
    return out


def _bach_zonen(ctx, X, Y):
    """Je Bach (bach_plan): Abstand d, Projektion sp und Laenge L im Stempelraster (nur Box um die Linie)."""
    from . import stempel as _stm
    out = []
    for wid, pl in sorted(ctx.bach_plan.items()):
        P = np.stack([np.asarray(pl["x"]), np.asarray(pl["y"])], 1)
        if len(P) < 2:
            continue
        B = float(pl["B"])
        R = 40.0
        x0, y0 = P.min(0) - R
        x1, y1 = P.max(0) + R
        box = (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
        if not box.any():
            continue
        d = np.full(X.shape, np.inf)
        sp = np.full(X.shape, -1.0)
        dd, ss, _ = _stm.polylinie_abstand(X[box], Y[box], P)
        d[box] = dd
        sp[box] = ss
        out.append({"id": wid, "d": d, "sp": sp, "L": float(_stm.polylinie_laenge(P)), "B": B,
                    "tiefe": float(pl.get("tiefe", 0.3))})
    return out


def bach_kern_m(B, zelle_m):
    """Kernzone eines Bachs (Netzrand + Uferring + 0,5 m): dort bleibt das Querprofil 13f/13g unangetastet."""
    from . import bach as _b
    return _b.ufer_abstand(B, zelle_m) + _b.RING_BREITE_M + 0.5


def bach_einschnitt_begrenzen(ctx, delta_vor):
    """13h (vgl. 13i K1): ausserhalb der Kernzone (Netzrand + Uferring) senkt das Bachprofil hoechstens
    tiefe + 0,5 m unter das Gelaende vor den Baechen - keine Keile mit senkrechter Wand am Rand der Reichweite.
    Spiegel, Stufen und Kern bleiben unveraendert. Rueckgabe: zurueckgenommene Flaeche m2."""
    st = ctx.stempel
    if not ctx.bach_plan:
        return 0.0
    z = float(st.z)
    vor = np.asarray(delta_vor, np.float64)
    neu = st.delta.copy()
    kern = np.zeros(neu.shape, bool)
    zonen = _bach_zonen(ctx, st.X, st.Y)
    for b in zonen:
        kern |= b["d"] <= bach_kern_m(b["B"], z)
    for b in zonen:
        aussen = (b["d"] < np.inf) & ~kern
        grenze = vor - (b["tiefe"] + 0.5)
        m = aussen & (neu < grenze)
        neu = np.where(m, grenze, neu)
    n = float((np.abs(neu - st.delta) > 0.01).sum()) * z * z
    st.delta = neu
    ctx._bach_kern = kern
    return n


def _fest_maske(ctx):
    """Zellen, die die Boeschung nicht aendern darf: Rand, Weg-/Orts-/Wasserschutz, Seeflaeche (+ Lippe),
    Bach-Kernzone (nur entlang der Linie - hinter dem Bachanfang darf eine Quellnische entstehen)."""
    from . import rezept as _rz
    st = ctx.stempel
    g = ctx.r.get("gelaende") or {}
    fest = st.randfaktor() < 0.999
    if g.get("schutz", True):
        aus = ctx._ausnahme_maske(wasser_ausnahmen=True)
        fest |= st.schutz_faktor(float(g.get("schutz_weg_m", 3.0)), not g.get("wasser_frei", False), 4.0, aus) < 0.999
    min_h = np.full(st.delta.shape, -np.inf)
    for sid, sv in ctx.see.items():
        if sv.get("klein"):
            continue
        fest |= _rz._in_polygon(st.X, st.Y, sv["umriss_m"])
        # Uferring: darf abgetragen werden, aber nie unter Spiegel + 0,3 m (Ufer haelt)
        ring = ctx._im_see_puffer(st.X, st.Y, sv, float(sv.get("ufer_m", 6.0)) + 2.0)
        min_h = np.where(ring, np.maximum(min_h, float(sv["spiegel_m"]) + 0.3), min_h)
        if sv.get("auslass_m"):
            ax, ay = sv["auslass_m"]
            fest |= np.hypot(st.X - ax, st.Y - ay) <= float(sv.get("lippe_m", 1.5)) + 2.0 * st.z
    for b in _bach_zonen(ctx, st.X, st.Y):
        kern = (b["d"] <= bach_kern_m(b["B"], st.z)) & (b["sp"] > 0.01) & (b["sp"] < b["L"] - 0.01)
        kern |= b["d"] <= 0.5 * b["B"] + st.z           # benetztes Bett auch an den Enden
        fest |= kern
    return fest, min_h


def boeschung_anwenden(ctx):
    """13h: nach fertig() - neue Steilflaechen auf max_neigung_grad (Standard 38 Grad, Halde 30-35 Grad + Reserve
    fuer die 1-m-Interpolation) bringen, ausser in 'steil_erlaubt'-Zonen (gewollte Waende, die verkleidet werden).
    Regeln im gelaende-Block: "max_neigung_grad": 38 | false, "max_auftrag_m": 3, "max_abtrag_m": 3,
    "steil_erlaubt": [{"bei": ref, "r_m": 12} | {"punkte": [...], "breite_m": 6}], "halde": {"lage", "wert",
    "bloecke": palette | false, "dichte_je_m2"} | false."""
    from . import stempel as _stm
    st = ctx.stempel
    g = ctx.r.get("gelaende") or {}
    mg = g.get("max_neigung_grad", 38.0)
    if mg is False or mg is None:
        return
    fest, min_h = _fest_maske(ctx)
    for z_ in g.get("steil_erlaubt") or []:
        if z_.get("punkte"):
            d, _, _ = _stm.polylinie_abstand(st.X, st.Y, ctx.linie(z_["punkte"]))
            fest |= d <= float(z_.get("breite_m", 6.0)) / 2.0
        else:
            x, y = ctx.punkt(z_.get("bei", "mitte"))
            fest |= np.hypot(st.X - x, st.Y - y) <= float(z_.get("r_m", 10.0))
    if not (np.abs(st.delta) > MIN_DELTA_M).any():
        return
    h_vor = st.h0 + st.delta
    auf, ab = st.boeschung(float(mg), fest=fest, max_auftrag_m=float(g.get("max_auftrag_m", 3.0)),
                           max_abtrag_m=float(g.get("max_abtrag_m", 3.0)))
    # Uferring: nie unter Spiegel + 0,3 m abtragen (ausser es lag schon vorher tiefer)
    grenze = np.minimum(min_h, h_vor)
    unten = (st.h0 + st.delta) < grenze
    if unten.any():
        st.delta = np.where(unten, grenze - st.h0, st.delta)
        st.max_aenderung_m = float(np.abs(st.delta).max())
    if auf + ab > 0:
        ctx.melde("HINWEIS", "Boeschung (13h): neue Steilflaechen auf <= %.0f Grad - %.0f m2 aufgeschuettet (Halde), "
                             "%.0f m2 abgetragen" % (float(mg), auf, ab))
    hc = g.get("halde", {})
    if hc is False or getattr(st, "halde", None) is None or st.halde.sum() * st.z * st.z < 10.0:
        return
    hc = hc if isinstance(hc, dict) else {}
    bn = biom_netze(ctx.biom)
    lage = hc.get("lage") or ((bn["_lagen"].get("wandfuss") or ["Geroell"])[0])
    ctx.r.setdefault("lagen", []).append({"lage": lage, "form": "halde", "wert": float(hc.get("wert", 190)),
                                          "flecken": float(hc.get("flecken", 0.3))})
    bl = hc.get("bloecke", bn.get("schutt") or bn.get("bloecke"))
    if bl:
        ctx._halde_gruppe = {"name": "halde_bloecke", "ebene": "schutt", "rolle": "fels",
                             "warum": "13h: Schutthalde 30-35 Grad statt Erdwand - Bloecke auf der Halde",
                             "palette": bl, "dichte_je_m2": float(hc.get("dichte_je_m2", 0.06)),
                             "verteilung": {"typ": "halde"}, "abstand_m": float(hc.get("abstand_m", 1.5)),
                             "groesse_m": hc.get("groesse_m", [0.5, 1.4]), "im_wasser": "nein"}


def halde_punkte(ctx, g, rng):
    """Zufallspunkte auf den Halde-Zellen (Boeschung) fuer Gruppen mit verteilung.typ 'halde'."""
    st = ctx.stempel
    h = getattr(st, "halde", None)
    if h is None or not h.any():
        return np.zeros(0), np.zeros(0), np.zeros(0)
    ii, jj = np.nonzero(h)
    fl = len(ii) * st.z * st.z
    n = int(round(float(g.get("dichte_je_m2", 0.05)) * fl)) if "anzahl" not in g else int(g["anzahl"])
    k = rng.choice(len(ii), size=max(n * 4, 1), replace=True)
    xs = st.X[ii[k], jj[k]] + rng.uniform(-0.5, 0.5, len(k)) * st.z
    ys = st.Y[ii[k], jj[k]] + rng.uniform(-0.5, 0.5, len(k)) * st.z
    return xs, ys, np.zeros(len(xs)), n


def halde_lage(ctx, lg):
    """Gewichtsmaske 0..1 der Halde im Lagenraster."""
    from . import stempel as _stm
    st = ctx.stempel
    h = getattr(st, "halde", None)
    if h is None:
        return np.zeros(lg.X.shape)
    from . import gelaende as _g
    w = _g.glaetten(h.astype(np.float32), 1.0).astype(np.float64)
    return np.clip(_stm._bilinear_fenster(w, st.fe, ctx.welt, lg.X, lg.Y, 0.0) * 1.6, 0.0, 1.0)


PLANER_GRENZE_GRAD = 41.0   # Planer rechnet im nativen Raster (2 m): Reserve fuer die 1-m-Interpolation des Pruefers


def _steil_im_stempel(ctx, grenze_grad=PLANER_GRENZE_GRAD):
    """Neu steile Zellen im Stempelraster (ohne Seegrund und benetztes Bachbett)."""
    from . import rezept as _rz
    st = ctx.stempel
    h1 = st.h0 + st.delta
    aus = np.zeros(h1.shape, bool)
    for sid, sv in ctx.see.items():
        if sv.get("klein"):
            continue
        aus |= _rz._in_polygon(st.X, st.Y, sv["umriss_m"]) & (h1 <= float(sv["spiegel_m"]) + 0.05)
    from . import bach as _b
    for b in _bach_zonen(ctx, st.X, st.Y):
        aus |= b["d"] <= _b.halbe_breite_eff(b["B"], st.z) + 1.0
    return neue_steil_maske(st.h0, h1, st.z, grenze_grad=grenze_grad, ausnahme=aus), h1


def verkleiden(ctx, g):
    """Gruppe mit verteilung.typ 'steilwand': belegt die neuen Steilflaechen (> 45 Grad) des Orts mit Wand-/
    Klippennetzen - gierige Ueberdeckung von unten nach oben: an der tiefsten ungedeckten Zelle ein Netz, Front zur
    Talseite (hangab), Vorderkante auf der Zelle (front_an_linie), dann die gedeckten Zellen abziehen. Netze
    ueberlappen (meide: null). verteilung: {"typ": "steilwand", "bei": ref, "r_m": R (optional Bereich),
    "min_flaeche_m2": 4, "max_anzahl": 30, "versatz_m": 0.3 (Front vor die Wand)}. Ohne palette/netz: Wandnetze des
    Bioms aus dem Regelwerk A15 (gefaelle_regeln.json biome.<biom>.netze.wand)."""
    from . import instanzen as _ins
    from . import stempel as _stm
    from . import rezept as _rz
    v = dict(g.get("verteilung") or {})
    name = g["name"]
    st = ctx.stempel
    if not (g.get("netz") or g.get("palette")):
        g = dict(g, palette=biom_netze(ctx.biom).get("wand") or [])
    rng = _ins.rng_fuer(ctx.seed, ctx.id, name)
    namen, gew = ctx.palette(g)
    if not namen:
        ctx.melde("FEHLER", "Gruppe %s: keine Wandnetze" % name)
        return []
    steil, h1 = _steil_im_stempel(ctx)
    if v.get("bei") is not None or v.get("r_m") is not None:
        x, y = ctx.punkt(v.get("bei", "mitte"))
        steil &= np.hypot(st.X - x, st.Y - y) <= float(v.get("r_m", 30.0))
    z2 = st.z * st.z
    lab, gr = komponenten(steil)
    mf = float(v.get("min_flaeche_m2", 4.0))
    for k, n in enumerate(gr, start=1):
        if n * z2 < mf:
            steil[lab == k] = False
    if not steil.any():
        ctx.melde("HINWEIS", "Gruppe %s: keine neuen Steilflaechen zu verkleiden" % name)
        return []
    g2 = dict(g)
    g2["verteilung"] = dict(v, front_an_linie=True)
    g2.setdefault("meide", None)
    g2.setdefault("akteur", True)
    g2.setdefault("kollision", True)
    g2.setdefault("rolle", "fels")
    g2.setdefault("eingraben", [0.08, 0.15])
    g2.setdefault("ausrichtung", "aufrecht")
    g2.setdefault("bezug", "min")
    ebene = g2.get("ebene", "begleiter")
    # schon gesetzte Fels-Akteure des Orts (z. B. eine Schwelle aus einer frueheren Gruppe) zaehlen mit
    vorher = []
    for gn, liste in ctx.gruppen.items():
        for s_ in liste:
            e_ = s_.get("stueck") or {}
            if e_.get("akteur") and (e_.get("rolle") in ("fels", "stein") or ist_fels(e_.get("pfad"))):
                vorher.append(abdruck(ctx.inv.netz(e_["pfad"]), e_["q"], e_["s"], e_["x"], e_["y"], e_["z"]))
    offen = steil & ~deckung(st.X, st.Y, h1, vorher, rand_m=0.0, z_tol_m=Z_TOL_M, nur=steil)
    versucht = np.zeros(steil.shape, bool)
    out = []
    max_n = int(v.get("max_anzahl", 30))
    vers = float(v.get("versatz_m", 0.3))
    while len(out) < max_n:
        kand = offen & ~versucht
        if not kand.any():
            break
        ii, jj = np.nonzero(kand)
        k = int(np.lexsort((jj, ii, h1[ii, jj]))[0])        # tiefste Zelle zuerst (deterministisch)
        i, j = int(ii[k]), int(jj[k])
        versucht[i, j] = True
        x, y = float(st.X[i, j]), float(st.Y[i, j])
        yaw = float(st.hangab_grad_bei_m(x, y, max(2.0, 1.5 * st.z)))
        ux, uy = _stm.kompass_vektor(yaw)
        x, y = x + ux * vers, y + uy * vers
        if not ctx._filter(g2, np.array([x]), np.array([y]), "steilwand")[0]:
            continue
        netz = namen[int(rng.choice(len(namen), p=gew))]
        info = ctx.inv.netz(netz)
        stk = ctx._ein_stueck(g2, info, x, y, 0.0, rng, yaw)
        if stk is None:
            continue
        a = abdruck(info, stk["q"], stk["s"], stk["x"], stk["y"], stk["z"])
        neu_ged = deckung(st.X, st.Y, h1, [a], rand_m=0.0, z_tol_m=Z_TOL_M, nur=offen) & offen
        if neu_ged.sum() < 2 and a["zmin"] < h1[i, j] - 0.5 * (a["zmax"] - a["zmin"]):
            # hohe Wand: das Netz sackt bis zum Wandfuss ab und deckt den oberen Teil nicht - hoeher ansetzen
            # (gestapelt, Unterkante 35 % der Netzhoehe unter der Zelle; ruht auf dem Netz darunter -> z_frei)
            g3 = dict(g2, z_bezug="z:%.3f" % (h1[i, j] - 0.35 * (a["zmax"] - a["zmin"])))
            stk = ctx._ein_stueck(g3, info, x, y, 0.0, rng, yaw)
            if stk is None:
                continue
            a = abdruck(info, stk["q"], stk["s"], stk["x"], stk["y"], stk["z"])
            neu_ged = deckung(st.X, st.Y, h1, [a], rand_m=0.0, z_tol_m=Z_TOL_M, nur=offen) & offen
        if neu_ged.sum() < 2:
            continue
        offen &= ~neu_ged
        stk["netz"] = info["name"]
        xx, yy = stk.pop("_x", x), stk.pop("_y", y)
        e = ctx.ebene.neu(ctx.id, name, ebene, netz, stk["x"], stk["y"], stk["z"], stk["q"], stk["s"],
                          kollision=stk["kollision"], akteur=stk["akteur"], sichtweite=g2.get("sichtweite"),
                          schatten=g2.get("schatten"), material=ctx._material(g2), z_frei=stk.get("z_frei", False),
                          rolle="fels",
                          extra=dict({"hoehe_m": round(stk["hoehe_m"], 2), "boden_z": round(stk["boden_z_m"] * 100, 1),
                                      "unterkante_z": round(stk["unterkante_z_m"] * 100, 1)},
                                     **_rz._pivot_front_extra(info, stk)) if stk["akteur"] else None)
        stk["stueck"] = e
        stk["x_m"], stk["y_m"] = xx, yy
        out.append(stk)
        if stk.get("massiv"):
            ctx._massiv.add(xx, yy, stk["kern_r_m"])
    ctx.gruppen[name] = ctx.gruppen.get(name, []) + out
    rest = float(offen.sum()) * z2
    ges = float(steil.sum()) * z2
    ctx.melde("HINWEIS", "Gruppe %s (13h): %d Wandnetze verkleiden %.0f von %.0f m2 neuer Steilflaeche (Rest %.0f m2)"
              % (name, len(out), ges - rest, ges, rest))
    return out


def pruefe_orte_steil(d, basis, welt, sw_ordner, inv):
    """Pruefer-Einstieg (sehens_pruefen.pruefe_orte): Regel 13h fuer alle Orte einer orte.json."""
    from . import instanzen as _ins
    if welt is None or inv is None or not basis:
        return []
    akteure = []
    if sw_ordner and os.path.isdir(sw_ordner):
        for feld, (plan, _arr) in sorted(_ins.lies_ebene(sw_ordner).items()):
            akteure += plan.get("akteure") or []
    b = []
    for o in d.get("orte") or []:
        b += pruefe_ort_steil(o, basis, welt, fels_abdruecke(akteure, inv, o.get("id")))
    return b
