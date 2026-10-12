"""bachbett.py - Bachbett-Ausstattung: Totholz, Schlamm, nasser Uferstreifen (Auftrag 16c, Nachtrag 18:15, Ferat:
"Felsen, totes Holz und Schlamm gehoeren in jedes Bachbett").

Gemeinsame Logik fuer den Gefaelle-Planer (gefaelle_plan.py, A15) und die Sehens-Bach-Planer (rezept.OrtKontext).
Zahlen und Netze: bachbett_regeln.json (Dichten je Biom mit Quellen).

Bausteine
  Regeln.lade()                       Regeln, .biom(name) (unbekannt -> tundra-artig ohne Holz)
  wald_faktor(welt, punkte_m, R, b)   Dichte nach Waldnaehe (Anteil 4-m-Baumzellen im Radius)
  Kanal(...)                          Gerinne entlang s: Lage, Spiegel, Wasserbreite, Stufen -> Lippenzonen, Ruhe, Kruemmung
  totholz_setzen(ctx, kanal, segm.)   liegende Staemme am Ufer (teils im Wasser), Verklausungen oberhalb von Lippen und an
                                      Engstellen (verkeilt), ueberspannende Staemme, Wurzelstoecke, Aeste, Zweige
                                      -> Gruppen 'bb_<art>_<nr>' im OrtKontext (Instanzen, nie Akteure)
  bett_lagen(...)                     Schlamm in ruhigen tiefen Becken und am Gleithang, Uferstreifen 0-1 m ueber dem Spiegel
  lagen_mischen(arr, zusatz)          Landschaftsgras im Streifen und Kies unter dem Schlamm daempfen
  stuecke_block(ebene, ort, inv, ...) Liste der gesetzten Stuecke (nach dem Ausduennen) fuer plan.json / orte.json
  Pruefer-Helfer: lippen_zonen, in_zonen, achse_enden, dichte_bewerten, streifen_bewerten

Regeln (gelten in beiden Planern):
  - Stufen, Becken, Lippen, Effekte, Spiegel und Gelaende aendern sich nicht (13f-Regel) - nur Instanzen und Lagen.
  - Kein Totholz mit der Achse in einer Lippenzone (Lippe - 0,5 m - Schraegversatz bis Fuss + 1 m; an Stufen >= 1 m
    Lippe - 1 m bis Fuss + 2,5 m).
  - Grosses Holz im Wasser oder <= 1 m daneben: kollision true (fluss_sim-Export: Wasser-Kollision). Ueberspannende
    Staemme liegen mit der Unterkante >= Spiegel + 0,25 m auf beiden Ufern (Export: 'ueberspannt', keine Wasser-Kollision).
  - Nur natuerliche Netze (Saegeschnitt verboten), liegend modelliert -> 'normale', Skala 0,6-1,8 (Aeste <= 1,8).
"""

import json
import math
import os

import numpy as np

from . import instanzen as _ins
from . import stempel as _st

HIER = os.path.dirname(os.path.abspath(__file__))
REGELN_PFAD = os.path.join(HIER, "bachbett_regeln.json")
PRAEFIX = "bb_"
ARTEN_LW = ("stamm", "verklausung", "ueberspannt", "wurzel")       # grosses Totholz (Dichte-Regel)
ARTEN = ARTEN_LW + ("ast", "zweig")
SKALA = (0.6, 1.8)                                                 # wie inventar.LIEGEND_SKALA / A15 netz_skala


# ======================================================================================================================
# Regeln
# ======================================================================================================================
class Regeln:
    def __init__(self, daten, pfad=""):
        self.r = daten
        self.pfad = pfad
        self.a = daten["allgemein"]
        self.version = daten.get("version", 1)

    @classmethod
    def lade(cls, pfad=None):
        pfad = pfad or REGELN_PFAD
        with open(pfad, "r", encoding="utf-8") as f:
            return cls(json.load(f), pfad)

    def biom(self, name):
        b = self.r["biome"]
        if name in b:
            return name, b[name]
        return "tundra", b["tundra"]

    def quellen(self, name):
        _, b = self.biom(name)
        return [self.r["quellen"][q] for q in b.get("quelle", []) if q in self.r["quellen"]]


_REGELN = None


def regeln():
    global _REGELN
    if _REGELN is None:
        _REGELN = Regeln.lade()
    return _REGELN


def wald_faktor(welt, punkte_m, R=None, biom="bergwald"):
    """Dichte-Faktor nach Waldnaehe: Anteil der 4-m-Zellen mit Baeumen (welt.baeume4 > 0) im Radius wald_radius_m um
    die Punkte; faktor = clip(min + (max - min) x Anteil / (2 x Bezug), min, max). Biome ohne 'wald': 1."""
    R = R or regeln()
    _, b = R.biom(biom)
    if not b.get("wald"):
        return 1.0, None
    return _wald_faktor_aus(welt, punkte_m, R)


def _glatt(t):
    t = float(np.clip(t, 0.0, 1.0))
    return t * t * (3.0 - 2.0 * t)


def _faktor(anteil, R):
    lo, hi = R.a["wald_faktor"]
    return float(np.clip(lo + (hi - lo) * anteil / (2.0 * float(R.a["wald_bezug"])), lo, hi))


def baum_anteil(welt, punkte_m, R=None):
    """Anteil der 4-m-Zellen mit Baeumen (welt.baeume4 > 0, Netzhoehe >= 5 m) im Radius wald_radius_m um die Punkte
    (Proben alle 10 m) - fuer jedes Biom (16c Nachtrag 3). None ohne Baumraster/Punkte."""
    R = R or regeln()
    P = np.asarray(punkte_m, np.float64).reshape(-1, 2) if len(punkte_m) else np.zeros((0, 2))
    if len(P) == 0 or getattr(welt, "baeume4", None) is None:
        return None
    f, anteil = _wald_faktor_aus(welt, P, R)
    return anteil


def dichte(welt, punkte_m, biom, R=None, oberlauf_m=None):
    """Totholz-Rahmen eines Segments nach Waldnaehe statt nur nach Biom-Etikett (16c Nachtrag 3, Koordinator):
    - Waldbiome ('wald': true): wie bisher Biom-Dichte x Waldfaktor (0,6-1,4 aus dem Baumanteil im Radius).
    - Uebrige Biome: Gewicht g = glatt((Anteil - a0) / (a1 - a0)) (ufer_wald_anteil). Mit Baeumen am Ufer gilt die
      Dichte des Ersatz-Waldbioms ('wald_ersatz', z. B. Tundra -> Bergwald) x Waldfaktor, ohne Baeume die Biom-Dichte
      ('kaum' bzw. 0): Rahmen = (1 - g) x Biom + g x Wald.
    - Treibholz: baumlose Strecken (1 - g) bekommen zusaetzlich 'treibholz' x h, h = glatt aus dem Baumanteil am
      Oberlauf (oberlauf_m: Punkte der letzten treibholz.oberlauf_m Meter oberhalb des Segments).
    Rueckgabe dict: biom, wald_biom, wald_anteil, wald_faktor, wald_gewicht, oberlauf_anteil, treibholz, lw [min, Ziel,
    max], verklausung, ast, zweig (je 100 m), palette (Biom der Netz-Paletten; 'treibholz' = allgemeine Palette)."""
    R = R or regeln()
    A = R.a
    bn, Rb = R.biom(biom)
    an = baum_anteil(welt, punkte_m, R)
    a_ = 0.0 if an is None else float(an)
    f = _faktor(a_, R) if an is not None else 1.0
    out = {"biom": bn, "wald_biom": None, "wald_anteil": None if an is None else round(a_, 4), "wald_faktor": 1.0,
           "wald_gewicht": 0.0, "oberlauf_anteil": None, "treibholz": 0.0, "palette": bn}
    T = A["treibholz"]
    keys = ("verklausung_je_100m", "ast_je_100m", "zweig_je_100m")
    if Rb.get("wald"):
        f_ = f if an is not None else 1.0
        out.update(wald_biom=bn, wald_faktor=round(f_, 3), wald_gewicht=1.0)
        lw = [float(v) * f_ for v in Rb["lw_je_100m"]]
        rest = [float(Rb[k]) * f_ for k in keys]
    else:
        wb = Rb.get("wald_ersatz")
        a0, a1 = A["ufer_wald_anteil"]
        g = _glatt((a_ - a0) / max(a1 - a0, 1e-6)) if (wb and an is not None) else 0.0
        h = 0.0
        if oberlauf_m is not None and len(oberlauf_m) >= 2 and (1.0 - g) > 0.0:
            ao = baum_anteil(welt, oberlauf_m, R)
            if ao is not None:
                out["oberlauf_anteil"] = round(float(ao), 4)
                h = _glatt((float(ao) - a0) / max(a1 - a0, 1e-6))
        t = (1.0 - g) * h
        Wb = R.biom(wb)[1] if wb else Rb
        lw = [(1.0 - g) * float(b_) + g * float(w_) * f + t * float(tt) for b_, w_, tt in
              zip(Rb["lw_je_100m"], Wb["lw_je_100m"], T["lw_je_100m"])]
        lw[0] = (1.0 - g) * float(Rb["lw_je_100m"][0]) + g * float(Wb["lw_je_100m"][0]) * f    # Treibholz: kein Minimum
        rest = [(1.0 - g) * float(Rb[k]) + g * float(Wb[k]) * f + t * float(T[k]) for k in keys]
        out.update(wald_biom=wb, wald_faktor=round(f if g > 0 else 1.0, 3), wald_gewicht=round(g, 3),
                   treibholz=round(t, 3))
        if g >= 0.5:
            out["palette"] = wb
        elif not Rb["stamm"] and t > 0:
            out["palette"] = "treibholz"
    # volle Genauigkeit (Anzahlen wie vor 16c Nachtrag 3); gerundet wird erst in der Planausgabe
    out["lw"] = [float(v) for v in lw]
    out["verklausung"], out["ast"], out["zweig"] = (float(v) for v in rest)
    return out


def paletten(R, d):
    """Netz-Paletten (stamm, ast, zweig, wurzel) zum Ergebnis von dichte(): Biom, Ersatz-Waldbiom oder Treibholz;
    leere Biom-Paletten werden mit Treibholz aufgefuellt, wenn die Dichte > 0 ist."""
    T = R.a["treibholz"]
    if d["palette"] == "treibholz":
        src = T
    else:
        src = R.biom(d["palette"])[1]
    out = {}
    for k in ("stamm", "ast", "zweig", "wurzel"):
        out[k] = list(src.get(k) or []) or (list(T.get(k) or []) if d["lw"][1] > 0 or d["ast"] > 0 else [])
    return out


def oberlauf_punkte(S, X, Y, a, L):
    """Punkte (m) der Linie (S, X, Y) von s = a - L bis a, alle 5 m (Treibholz vom Oberlauf); None, wenn < 5 m."""
    S = np.asarray(S, np.float64)
    a0 = max(float(S[0]), float(a) - float(L))
    if float(a) - a0 < 5.0:
        return None
    ss = np.arange(a0, float(a) + 1e-6, 5.0)
    return np.stack([np.interp(ss, S, X), np.interp(ss, S, Y)], 1)


def _wald_faktor_aus(welt, punkte_m, R):
    A = R.a
    P = np.asarray(punkte_m, np.float64)[:, :2]
    if len(P) == 0 or getattr(welt, "baeume4", None) is None:
        return 1.0, None
    # Proben alle 10 m
    kum = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))]) if len(P) > 1 else np.zeros(1)
    ss = np.arange(0.0, kum[-1] + 1e-6, 10.0) if kum[-1] > 0 else np.zeros(1)
    px = np.interp(ss, kum, P[:, 0])
    py = np.interp(ss, kum, P[:, 1])
    r = float(A["wald_radius_m"])
    from . import daten as _d
    i0, j0 = _d.m_zu_pixel(px.min() - r, py.min() - r, 4.0)
    i1, j1 = _d.m_zu_pixel(px.max() + r, py.max() + r, 4.0)
    b4 = welt.baeume4
    i0, i1 = int(max(0, math.floor(min(i0, i1)))), int(min(b4.shape[0] - 1, math.ceil(max(i0, i1))))
    j0, j1 = int(max(0, math.floor(min(j0, j1)))), int(min(b4.shape[1] - 1, math.ceil(max(j0, j1))))
    if i1 < i0 or j1 < j0:
        return 1.0, None
    jj, ii = np.meshgrid(np.arange(j0, j1 + 1), np.arange(i0, i1 + 1))
    x4 = jj * 4.0 + 1.5 - 4730.5
    y4 = ii * 4.0 + 1.5 - 4060.5
    nah = np.zeros(x4.shape, bool)
    for x_, y_ in zip(px, py):
        nah |= (x4 - x_) ** 2 + (y4 - y_) ** 2 <= r * r
    if not nah.any():
        return 1.0, None
    anteil = float((np.asarray(b4[i0:i1 + 1, j0:j1 + 1])[nah] > 0).mean())
    lo, hi = A["wald_faktor"]
    f = float(np.clip(lo + (hi - lo) * anteil / (2.0 * float(A["wald_bezug"])), lo, hi))
    return f, anteil


# ======================================================================================================================
# Kanal
# ======================================================================================================================
def lippen_versatz(st, u):
    """Laengsversatz (m, + = stromab) einer schraegen/gekruemmten Lippe an der Seitenlage u (+ = links), wie
    gefaelle_plan.lippen_versatz mit den wirksamen Werten aus plan.json lippe_form: tan(winkel_grad), pfeil_m, h = B/2."""
    tn, pf, h = float(st.get("tan", 0.0)), float(st.get("pfeil", 0.0)), max(float(st.get("h", 0.5)), 0.5)
    uc = np.clip(np.asarray(u, np.float64), -h, h)
    return tn * uc + pf * (1.0 - (uc / h) ** 2) - pf * 2.0 / 3.0


def lippen_zonen(stufen, R=None, zuschlag=0.0):
    """stufen: [{"s_lippe", "s_fuss", "fall", "gross" (bool), "tan", "pfeil", "h", "halb"}] -> [(a, b, halb_frei,
    stufe)]: verbotene Bereiche fuer Totholz in der Lippen-Koordinate s - Versatz(u) (Lippe, Absturz, Vorhang/Aufprall),
    quer nur bis halb_frei = Lippenbreite/2 - lippe_rand_frei_m ('mitten in der Lippe'; an den Lippenenden darf Holz
    verkeilt liegen)."""
    A = (R or regeln()).a
    out = []
    for st in stufen:
        if st.get("gross") or float(st.get("fall", 0.0)) >= float(A["lippe_gross_ab_m"]):
            a, b = float(A["lippe_gross_vor_m"]), float(A["lippe_gross_nach_m"])
        else:
            a, b = float(A["lippe_vor_m"]), float(A["lippe_nach_m"])
        hf = float(st.get("halb", 1e9)) - float(A["lippe_rand_frei_m"]) + zuschlag
        out.append((float(st["s_lippe"]) - a - zuschlag, float(st["s_fuss"]) + b + zuschlag, hf, st))
    return sorted(out, key=lambda v: v[0])


def in_zonen(s, zonen, u=None):
    """True, wo (s, u) in einer Lippenzone liegt (u = Seitenlage, + = links: Schraegversatz und Querbegrenzung;
    None = ohne Versatz, ganze Breite)."""
    s = np.asarray(s, np.float64)
    m = np.zeros(s.shape, bool)
    for a, b, hf, st in zonen:
        if u is None:
            m |= (s >= a) & (s <= b)
            continue
        se = s - lippen_versatz(st, u)
        m |= (se >= a) & (se <= b) & (np.abs(np.asarray(u, np.float64)) <= hf)
    return m


class Lippenfeld:
    """s_eff(s, u) = s - Versatz(s, u) wie gefaelle_plan.LippenFeld, aus Lippen-Dicts (s_lippe, tan, pfeil, h) und
    Segmenten [(a, b)]: zwischen benachbarten Lippen linear ueberblendet, an Segmentgrenzen 0 (Pruefer: Spiegel an
    schraegen Lippen)."""

    def __init__(self, stufen, segmente):
        anker = []
        for a, b in sorted(segmente):
            anker.append((float(a), None))
            for st in sorted(stufen, key=lambda v: v["s_lippe"]):
                if a - 1e-6 <= st["s_lippe"] <= b + 1e-6 and "tan" in st:
                    anker.append((float(st["s_lippe"]), st))
            anker.append((float(b), None))
        anker.sort(key=lambda v: v[0])
        self.S = np.array([v[0] for v in anker]) if anker else np.zeros(0)
        self.G = [v[1] for v in anker]

    def versatz(self, s, u):
        s, u = np.broadcast_arrays(np.asarray(s, np.float64), np.asarray(u, np.float64))
        out = np.zeros(s.shape)
        if len(self.S) < 2:
            return out
        i = np.clip(np.searchsorted(self.S, s, side="right") - 1, 0, len(self.S) - 2)
        for k in np.unique(i):
            m = i == k
            s0, s1 = self.S[k], self.S[k + 1]
            w = np.clip((s[m] - s0) / max(s1 - s0, 1e-6), 0.0, 1.0)
            g0, g1 = self.G[k], self.G[k + 1]
            v0 = lippen_versatz(g0, u[m]) if g0 else 0.0
            v1 = lippen_versatz(g1, u[m]) if g1 else 0.0
            innen = (s[m] >= self.S[0]) & (s[m] <= self.S[-1])
            out[m] = np.where(innen, (1.0 - w) * v0 + w * v1, 0.0)
        return out

    def s_eff(self, s, u):
        return np.asarray(s, np.float64) - self.versatz(s, u)


def projektion_schnell(x, y, P, block=4096):
    """Wie stempel.polylinie_abstand (Abstand, Bogenlaenge, Seitenabstand + = links), aber vektorisiert ueber alle
    Segmente (Punkte in Bloecken) - fuer viele Abfragen an langen Linien."""
    P = np.asarray(P, np.float64)[:, :2]
    x = np.asarray(x, np.float64)
    y = np.asarray(y, np.float64)
    shp = np.broadcast(x, y).shape
    xf = np.broadcast_to(x, shp).ravel()
    yf = np.broadcast_to(y, shp).ravel()
    if len(P) < 2:
        return _st.polylinie_abstand(x, y, P)
    A = P[:-1]
    AB = P[1:] - A
    L2 = np.maximum((AB ** 2).sum(1), 1e-12)
    L = np.sqrt(L2)
    kum = np.concatenate([[0.0], np.cumsum(L)])[:-1]
    d_out = np.empty(len(xf))
    s_out = np.empty(len(xf))
    u_out = np.empty(len(xf))
    for k in range(0, len(xf), block):
        X = xf[k:k + block, None]
        Y = yf[k:k + block, None]
        t = np.clip(((X - A[None, :, 0]) * AB[None, :, 0] + (Y - A[None, :, 1]) * AB[None, :, 1]) / L2[None, :], 0.0, 1.0)
        d = np.hypot(X - (A[None, :, 0] + t * AB[None, :, 0]), Y - (A[None, :, 1] + t * AB[None, :, 1]))
        j = np.argmin(d, axis=1)
        r = np.arange(len(j))
        d_out[k:k + block] = d[r, j]
        s_out[k:k + block] = kum[j] + t[r, j] * L[j]
        u_out[k:k + block] = ((X[:, 0] - A[j, 0]) * AB[j, 1] - (Y[:, 0] - A[j, 1]) * AB[j, 0]) / L[j]
    return d_out.reshape(shp), s_out.reshape(shp), u_out.reshape(shp)


class Kanal:
    """Gerinne entlang der Laufkoordinate s (m): Mittellinie x/y, Spiegel z, Wasserbreite B, Stufen.
    halb_fn(s, u) -> halbe Wasserbreite auf der Seite von u (+ = links); s_eff(s, u) fuer schraege Lippen (A15)."""

    def __init__(self, s, x, y, z, B, stufen=(), s_eff=None, halb_fn=None, R=None, zonen_zuschlag_m=0.0, z_fn=None,
                 ruhe_fn=None):
        self.s = np.asarray(s, np.float64)
        self.x = np.asarray(x, np.float64)
        self.y = np.asarray(y, np.float64)
        self.zs = np.asarray(z, np.float64)
        self.B = np.asarray(B, np.float64)
        self.stufen = list(stufen)
        self._s_eff = s_eff
        self._halb = halb_fn
        self._z_fn = z_fn
        self._ruhe_fn = ruhe_fn
        self.R = R or regeln()
        self.zonen = lippen_zonen(self.stufen, self.R, zonen_zuschlag_m)
        self.linie = np.stack([self.x, self.y], 1)
        # Projektion: Bogenlaenge der Sehnen-Polylinie -> s (wie der Pruefer an spiegel_neu_cm / punkte_cm)
        self.cum = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(self.x), np.diff(self.y)))])
        # Kruemmung (1/m, + = Linkskurve), geglaettet ueber ~6 m
        if len(self.s) >= 3:
            tx, ty = np.gradient(self.x, self.s), np.gradient(self.y, self.s)
            th = np.unwrap(np.arctan2(ty, tx))
            k = np.gradient(th, self.s)
            # y zeigt nach Sueden (Norden oben): mathematisch positive Drehung in (x, y) ist im Kartenbild eine
            # Rechtskurve -> Vorzeichen drehen, damit + = links (wie u)
            k = -k
            ds = max(float(np.median(np.diff(self.s))), 0.1)
            n = max(1, int(round(3.0 / ds)))
            ker = np.ones(2 * n + 1) / (2 * n + 1)
            self.k = np.convolve(np.pad(k, n, mode="edge"), ker, mode="valid")
        else:
            self.k = np.zeros(len(self.s))

    def xy(self, s):
        return np.interp(s, self.s, self.x), np.interp(s, self.s, self.y)

    def tang(self, s, h=0.5):
        x0, y0 = self.xy(np.asarray(s) - h)
        x1, y1 = self.xy(np.asarray(s) + h)
        L = np.maximum(np.hypot(x1 - x0, y1 - y0), 1e-9)
        return (x1 - x0) / L, (y1 - y0) / L

    def punkt(self, s, u):
        """Punkt bei s mit Seitenabstand u (+ = links in Laufrichtung, Norden oben)."""
        x, y = self.xy(s)
        tx, ty = self.tang(s)
        return x + ty * u, y - tx * u

    def s_eff(self, s, u):
        return self._s_eff(s, u) if self._s_eff is not None else np.asarray(s, np.float64)

    def z(self, s, u=0.0):
        if self._z_fn is not None:
            return np.asarray(self._z_fn(self.s_eff(s, u)), np.float64)
        return np.interp(self.s_eff(s, u), self.s, self.zs)

    def halb_netz(self, s):
        """Halbe Netz-/Bachbreite (B/2) - Bezug der Lippenregel (wie der Pruefer)."""
        return np.interp(s, self.s, self.B) / 2.0

    def halb(self, s, u=1.0):
        if self._halb is not None:
            return np.asarray(self._halb(s, u), np.float64)
        return np.interp(s, self.s, self.B) / 2.0

    def B_bei(self, s):
        return np.interp(s, self.s, self.B)

    def kruemmung(self, s):
        return np.interp(s, self.s, self.k)

    def projektion(self, x, y):
        d, c, u = projektion_schnell(x, y, self.linie, 1024)
        return d, np.interp(c, self.cum, self.s), u

    def in_lippe(self, s, u=None):
        return in_zonen(s, self.zonen, u)

    def ruhe(self, s):
        """0..1: ruhiges Becken (1) vs. Lippe, Absturz, Kolk-Anfang, Schnelle (0). Becken zwischen Fuss + Abstand
        und naechster Lippe - Abstand; vor der ersten bzw. nach der letzten Stufe ruhig."""
        A = self.R.a
        s = np.asarray(s, np.float64)
        if self._ruhe_fn is not None:                   # Roh-Laeufe ohne Stufen: Ruhe aus dem Spiegelgefaelle
            return np.asarray(self._ruhe_fn(s), np.float64)
        r = np.ones(s.shape)
        a_f, a_l = float(A["schlamm_ruhe_nach_fuss_m"]), float(A["schlamm_ruhe_vor_lippe_m"])
        for st in self.stufen:
            l0, f0 = float(st["s_lippe"]), float(st["s_fuss"])
            gross = 2.0 if (st.get("gross") or float(st.get("fall", 0.0)) >= 1.0) else 1.0
            unten = _st.glatt01((s - f0 - a_f * gross) / 2.0)
            oben = _st.glatt01((l0 - a_l - s) / 1.5)
            r *= np.where(s >= l0, unten, np.where(s <= l0, oben, 1.0))
        return r


# ======================================================================================================================
# Totholz
# ======================================================================================================================
def _netz_nach_laenge(inv, palette, L, rng, skala=SKALA):
    """13k-Logik (wie gefaelle_plan.holz_setzen): Netze mit L / Netzlaenge in [min; max], sonst das naechstliegende;
    Laenge auf skala x Netzlaenge begrenzt. Rueckgabe (netz, L_neu, netzlaenge, hoehe_m_bei_skala)."""
    form = {n: inv.stamm_form(n)[0] for n in palette}
    ok = [n for n in palette if skala[0] * form[n] <= L <= skala[1] * form[n]]
    if ok:
        n = ok[int(rng.integers(len(ok)))]
    else:
        n = min(palette, key=lambda n_: (abs(math.log(L / max(form[n_], 1e-3))), n_))
    L2 = float(np.clip(L, skala[0] * form[n], skala[1] * form[n]))
    g = inv.netz(n)["groesse_m"]
    return n, L2, form[n], float(min(g) * L2 / max(form[n], 1e-3))


def _yaw(tx, ty):
    """Kompass (0 = Nord, 90 = Ost) eines Vektors (x Ost, y Sued)."""
    return math.degrees(math.atan2(tx, -ty)) % 360.0


def _richtung(yaw):
    return math.sin(math.radians(yaw)), -math.cos(math.radians(yaw))


def _hang_grad(ctx, x, y, L):
    """Hangneigung (Grad) am Punkt, Radius wie rezept._ein_stueck (0,3 x Laenge, 1-4 m)."""
    r = float(np.clip(0.3 * L, 1.0, 4.0))
    gx = (float(ctx.boden(x + r, y)) - float(ctx.boden(x - r, y))) / (2.0 * r)
    gy = (float(ctx.boden(x, y + r)) - float(ctx.boden(x, y - r))) / (2.0 * r)
    return math.degrees(math.atan(math.hypot(gx, gy)))


def _neigung_zur_normalen(ctx, inv, e):
    """Winkel Hochachse <-> Hangnormale wie sehens_pruefen.pruefe_liegendes_holz (Normale am Pivot, Radius 0,3 x
    Netzlaenge x Skala, 1-4 m), hier gegen den Boden des Planers."""
    from .sehens_pruefen import liegend_neigung_grad
    xm, ym = e["x"] / 100.0, e["y"] / 100.0
    r = float(np.clip(0.3 * inv.stamm_form(e["pfad"])[0] * max(e["s"]), 1.0, 4.0))
    gx = (float(ctx.boden(xm + r, ym)) - float(ctx.boden(xm - r, ym))) / (2.0 * r)
    gy = (float(ctx.boden(xm, ym + r)) - float(ctx.boden(xm, ym - r))) / (2.0 * r)
    return float(liegend_neigung_grad(inv, e["pfad"], [e["q"]], [[-gx, -gy, 1.0]])[0])


class _Massiv:
    """Massive Stuecke (Bloecke, Riegel, Waende) des Kontexts fuer den Achsentest."""

    def __init__(self, ctx):
        pts = [(s_["x_m"], s_["y_m"], s_.get("kern_r_m", 0.5)) for g, lst in ctx.gruppen.items()
               if not g.startswith(PRAEFIX) for s_ in lst if s_.get("massiv")]
        self.P = np.asarray(pts, np.float64).reshape(-1, 3)

    def frei(self, x0, y0, x1, y1, r, anteil=(0.2, 0.8)):
        if not len(self.P):
            return True
        t = np.linspace(anteil[0], anteil[1], 7)
        xs, ys = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        d = np.hypot(self.P[:, 0][:, None] - xs[None, :], self.P[:, 1][:, None] - ys[None, :])
        return not bool((d < self.P[:, 2][:, None] + r).any())


def totholz_setzen(ctx, kanal, segmente, R=None, welt=None, bestand_lw=None, seed_teil="bb", see_fn=None, name_teil="",
                   oberlauf_fn=None):
    """Totholz eines Gerinnes in den OrtKontext ctx setzen. segmente: [(a, b, biom)] (s-Bereiche des Gerinnes).
    bestand_lw: {segment_index: Anzahl schon vorhandener grosser Holzstuecke (Holzstufen, Totholz quer)} - wird von der
    Ziel-Anzahl abgezogen. see_fn(x, y) -> True, wo kein Holz liegen darf (z. B. Seen). oberlauf_fn(a) -> Punkte (m)
    der Strecke oberhalb von s = a (Treibholz, 16c Nachtrag 3). Rueckgabe Bilanz je Segment."""
    R = R or regeln()
    A = R.a
    welt = welt or ctx.welt
    inv = ctx.inv
    massiv = _Massiv(ctx)
    gitter = {"lw": _ins.Abstandsgitter(4.0), "ast": _ins.Abstandsgitter(2.0), "zweig": _ins.Abstandsgitter(1.0)}
    bilanz = []
    zaehler = {"n": 0}

    def rng(*t):
        return _ins.rng_fuer(ctx.seed, ctx.id, seed_teil, *t)

    def frei_lippe(x0, y0, x1, y1):
        t = np.linspace(0.0, 1.0, 9)
        xs, ys = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        d, s, u = kanal.projektion(xs, ys)
        return not bool(kanal.in_lippe(s, u).any())

    def setze_stueck(art, netz, L, x, y, yaw, ebene, rolle, kol, extra=None):
        nm = "%s%s%s_%03d" % (PRAEFIX, name_teil, art, zaehler["n"])
        zaehler["n"] += 1
        ctx.anker[nm + "__000"] = (float(x), float(y))
        ctx.richtungen[nm + "__000"] = float(yaw) % 360.0
        g = {"name": nm, "ebene": ebene, "palette": [netz], "verteilung": {"typ": "anker", "praefix": nm + "__"},
             "rolle": rolle, "groesse_m": [L, L], "groesse_achse": "max", "akteur": False, "kollision": bool(kol),
             "im_wasser": "egal", "meide": None, "yaw_streuung_grad": 0.0, "boden_min_m": 0.2, "zentrieren": True,
             "warum": "Bachbett-Totholz (16c Nachtrag 18:15): %s" % art}
        if rolle == "stamm":
            g["ausrichtung"] = "liegend"            # rezept: liegend modelliert -> 'normale', lange Achse = Yaw
        else:
            g["ausrichtung"] = "normale"
            g["normale_anteil"] = 0.8
        if extra:
            g.update(extra)
        if "z_bezug" in g:
            # verkeilt/ueberspannend: so weit der Hangnormalen folgen, dass die Hochachse <= neigung_frei_grad von ihr
            # abweicht (Pruefer pruefe_liegendes_holz: > 45 Grad = 'steht')
            th = _hang_grad(ctx, x, y, L)
            if th > float(A["neigung_frei_grad"]):
                g["normale_anteil"] = max(float(g.get("normale_anteil", 0.0)), 1.0 - float(A["neigung_frei_grad"]) / th)
        try:
            out = ctx.gruppe(g)
        except (KeyError, ValueError) as ex:
            ctx.melde("WARNUNG", "Bachbett %s: %s" % (nm, ex))
            return None
        if not out:
            return None
        stk = out[0]
        e = stk.get("stueck")
        if e is not None:
            # Achse des tatsaechlich gesetzten Netzes (wie der Pruefer: gedrehte Bounds) gegen die Lippenzonen
            (x0, y0, x1, y1), _, _ = achse_enden(inv, e["pfad"], e["q"], e["s"], (e["x"], e["y"]))
            if inv.liegendes_holz(e["pfad"]) and _neigung_zur_normalen(ctx, inv, e) > float(A["neigung_max_grad"]):
                # wie der Pruefer (Normale am Pivot, Radius 0,3 x Laenge, 1-4 m) mit Reserve fuer den 1-m-Boden
                ctx.ebene.stuecke = [s_ for s_ in ctx.ebene.stuecke if s_ is not e]
                ctx.gruppen[nm] = []
                grund["neigung"] = grund.get("neigung", 0) + 1
                return None
            if not frei_lippe(x0, y0, x1, y1):
                ctx.ebene.stuecke = [s_ for s_ in ctx.ebene.stuecke if s_ is not e]
                ctx.gruppen[nm] = []
                grund["lippe_nach_setzen"] = grund.get("lippe_nach_setzen", 0) + 1
                return None
        return stk

    for n_seg, (a, b, biom) in enumerate(segmente):
        bn, Rb = R.biom(biom)
        L_seg = float(b - a)
        bil = {"segment": n_seg, "s_m": [round(float(a), 2), round(float(b), 2)], "biom": bn, "laenge_m": round(L_seg, 1),
               "gesetzt": {k: 0 for k in ARTEN}, "blockiert": 0, "ziel": {}, "abgelehnt": {}}
        grund = bil["abgelehnt"]
        bilanz.append(bil)
        if L_seg < float(A["min_laenge_m"]):
            continue
        ss = np.linspace(a, b, max(2, int(L_seg / 2.0) + 1))
        ober = oberlauf_fn(a) if oberlauf_fn is not None else None
        dz = dichte(welt, np.stack(kanal.xy(ss), 1), bn, R, ober)
        f = float(dz["wald_faktor"])
        bil["wald_faktor"] = dz["wald_faktor"]
        bil["wald_anteil"] = None if dz["wald_anteil"] is None else round(float(dz["wald_anteil"]), 3)
        for k_ in ("wald_biom", "wald_gewicht", "oberlauf_anteil", "treibholz", "palette"):
            bil[k_] = dz[k_]
        bil["rahmen_lw"] = [round(v, 3) for v in dz["lw"]]
        r_ = rng("seg", n_seg)
        lw_ziel = float(dz["lw"][1]) * L_seg / 100.0
        n_best = int((bestand_lw or {}).get(n_seg, 0))
        n_lw = max(0, int(math.floor(lw_ziel + r_.uniform())) - n_best)
        n_jam = int(math.floor(float(dz["verklausung"]) * L_seg / 100.0 + r_.uniform()))
        n_ast = int(math.floor(float(dz["ast"]) * L_seg / 100.0 + r_.uniform()))
        n_zw = int(math.floor(float(dz["zweig"]) * L_seg / 100.0 + r_.uniform()))
        bil["ziel"] = {"lw": round(lw_ziel, 2), "lw_bestand": n_best, "lw_neu": n_lw, "verklausung": n_jam,
                       "ast": n_ast, "zweig": n_zw}
        pal = paletten(R, dz)
        stamm_pal = [n for n in pal["stamm"] if inv.netz_pfad(n)]
        ast_pal = [n for n in pal["ast"] if inv.netz_pfad(n)]
        zw_pal = [n for n in pal["zweig"] if inv.netz_pfad(n)]
        wu_pal = [n for n in pal["wurzel"] if inv.netz_pfad(n)]

        def ok_ort(x, y):
            if see_fn is not None and bool(np.any(see_fn(np.array([x]), np.array([y])))):
                return False
            return True

        # ---- 1. Verklausungen: oberhalb von Lippen (Becken davor >= 3 m) und an Engstellen
        n_lw_rest = n_lw
        if stamm_pal and n_jam > 0 and n_lw_rest > 0:
            kand = []
            prev_f = a
            for st in sorted(kanal.stufen, key=lambda v: v["s_lippe"]):
                l0 = float(st["s_lippe"])
                if a + 2.0 <= l0 <= b and l0 - prev_f >= 3.0:
                    kand.append(("lippe", l0, float(st.get("fall", 0.0))))
                prev_f = max(prev_f, float(st["s_fuss"]))
            sB = np.arange(a + 3.0, b - 3.0, 1.0)
            if len(sB) >= 5:
                Bv = kanal.B_bei(sB)
                med = float(np.median(Bv))
                for k in range(2, len(sB) - 2):
                    if Bv[k] <= Bv[k - 2:k + 3].min() + 1e-6 and Bv[k] <= float(A["engstelle_B_anteil"]) * med:
                        kand.append(("engstelle", float(sB[k]), 0.0))
            r_.shuffle(kand)
            kand.sort(key=lambda v: (v[0] != "lippe", -v[2]))
            n_ok = 0
            for art_k, s0, _ in kand:
                if n_ok >= n_jam or n_lw_rest <= 0:
                    break
                rj = rng("jam", n_seg, round(s0, 2))
                B_ = float(kanal.B_bei(s0))
                n_st = int(rj.integers(A["verklausung_staemme"][0], A["verklausung_staemme"][1] + 1))
                vor = float(rj.uniform(*A["verklausung_vor_lippe_m"]))
                sg = 1.0 if rj.uniform() < 0.5 else -1.0
                gesetzt = []
                z_top = None
                for i in range(n_st):
                    L = float(np.clip(B_ * rj.uniform(*A["verklausung_laenge_B"]), A["stamm_laenge_m"][0],
                                      A["stamm_laenge_m"][1]))
                    netz, L, Ln, H = _netz_nach_laenge(inv, stamm_pal, L, rj)
                    w = sg * (1 if i % 2 == 0 else -1) * float(rj.uniform(*A["verklausung_winkel_grad"]))
                    tx, ty = kanal.tang(s0)
                    yaw = (_yaw(tx, ty) + 90.0 + w) % 360.0
                    ex = 0.5 * L * abs(math.sin(math.radians(w)))       # Laengsausdehnung der schraegen Achse
                    sc = s0 - (vor + ex + 0.55 * i) if art_k == "lippe" else s0 - 0.55 * i
                    u = float(rj.uniform(-0.15, 0.15)) * B_
                    xc, yc = kanal.punkt(sc, u)
                    dx, dy = _richtung(yaw)
                    x0, y0, x1, y1 = xc - dx * L / 2, yc - dy * L / 2, xc + dx * L / 2, yc + dy * L / 2
                    if not frei_lippe(x0, y0, x1, y1) or not ok_ort(xc, yc) or not gitter["lw"].frei_min(xc, yc, 0.4):
                        bil["blockiert"] += 1
                        continue
                    zs = float(kanal.z(sc, u))
                    bz = float(ctx.boden(xc, yc))
                    # verkeilt: Unterkante zwischen Bett und Spiegel - H x Eintauchen (ragt aus dem Wasser), auf dem
                    # vorigen Stamm, wenn der hoeher liegt
                    zu = max(bz - 0.15 * H, zs - float(A["verklausung_eintauchen"]) * H)
                    if z_top is not None:
                        zu = max(zu, z_top - 0.55 * H)
                    stk = setze_stueck("verklausung", netz, L, xc, yc, yaw, "begleiter", "stamm", True,
                                       {"z_bezug": "z:%.3f" % zu, "normale_anteil": 0.15})
                    if stk is None:
                        bil["blockiert"] += 1
                        continue
                    stk["_bb"] = {"art": "verklausung", "s": sc, "u": u, "typ": art_k}
                    gitter["lw"].add(xc, yc, 0.0)
                    z_top = stk["oberkante_z_m"]
                    gesetzt.append(stk)
                    bil["gesetzt"]["verklausung"] += 1
                    n_lw_rest -= 1
                if gesetzt:
                    n_ok += 1
                    # Aeste obenauf (Treibgut)
                    for i in range(int(rj.integers(A["verklausung_aeste"][0], A["verklausung_aeste"][1] + 1))):
                        if not ast_pal:
                            break
                        L = float(rj.uniform(*A["ast_laenge_m"]))
                        netz, L, Ln, H = _netz_nach_laenge(inv, ast_pal, L, rj, (0.3, SKALA[1]))
                        st0 = gesetzt[i % len(gesetzt)]
                        xa, ya = st0["x_m"] + rj.uniform(-0.6, 0.6), st0["y_m"] + rj.uniform(-0.6, 0.6)
                        yaw = (st0["yaw"] + rj.uniform(-40, 40)) % 360.0
                        dx, dy = _richtung(yaw)
                        if not frei_lippe(xa - dx * L / 2, ya - dy * L / 2, xa + dx * L / 2, ya + dy * L / 2):
                            continue
                        stk = setze_stueck("ast", netz, L, xa, ya, yaw, "schutt", "stamm", True,
                                           {"z_bezug": "z:%.3f" % (st0["oberkante_z_m"] - 0.5 * H), "normale_anteil": 0.2})
                        if stk is not None:
                            stk["_bb"] = {"art": "ast", "typ": "verklausung"}
                            bil["gesetzt"]["ast"] += 1
            bil["verklausungen"] = n_ok
        # ---- 2. Ueberspannende Staemme (schmale Becken)
        n_ue = int(round(float(A["ueberspannt_anteil"]) * n_lw))
        if stamm_pal and n_ue > 0 and n_lw_rest > 0:
            for k in range(6 * n_ue):
                if bil["gesetzt"]["ueberspannt"] >= n_ue or n_lw_rest <= 0:
                    break
                rk = rng("ue", n_seg, k)
                sc = float(rk.uniform(a + 2.0, b - 2.0))
                B_ = float(kanal.B_bei(sc))
                if B_ > float(A["ueberspannt_B_max_m"]) or kanal.in_lippe(sc, 0.0):
                    continue
                hl, hr = float(kanal.halb(sc, 1.0)), float(kanal.halb(sc, -1.0))
                ue = float(rk.uniform(*A["ueberspannt_ueberstand_m"]))
                L = hl + hr + 2.0 * ue
                netz, L2, Ln, H = _netz_nach_laenge(inv, stamm_pal, L, rk)
                if L2 < hl + hr + 1.2:
                    continue
                w = float(rk.uniform(-20, 20))
                tx, ty = kanal.tang(sc)
                yaw = (_yaw(tx, ty) + 90.0 + w) % 360.0
                um = 0.5 * (hl - hr)
                xc, yc = kanal.punkt(sc, um)
                dx, dy = _richtung(yaw)
                x0, y0, x1, y1 = xc - dx * L2 / 2, yc - dy * L2 / 2, xc + dx * L2 / 2, yc + dy * L2 / 2
                if not frei_lippe(x0, y0, x1, y1) or not ok_ort(xc, yc) or not gitter["lw"].frei_min(xc, yc, 2.0):
                    continue
                if not massiv.frei(x0, y0, x1, y1, 0.3):
                    continue
                # Auflage: Ufer an beiden Enden (0,3 m innen vom Ende), Unterkante >= Spiegel + Mindestabstand
                bz = [float(ctx.boden(x0 + dx * 0.3, y0 + dy * 0.3)), float(ctx.boden(x1 - dx * 0.3, y1 - dy * 0.3))]
                zs = float(kanal.z(sc, um))
                zu = min(bz) - 0.05
                if zu < zs + float(A["ueberspannt_unterkante_min_m"]) or max(bz) - min(bz) > 0.8 * L2:
                    continue
                stk = setze_stueck("ueberspannt", netz, L2, xc, yc, yaw, "begleiter", "stamm", True,
                                   {"z_bezug": "z:%.3f" % zu, "normale_anteil": 0.0})
                if stk is None:
                    continue
                stk["_bb"] = {"art": "ueberspannt", "s": sc, "u": um}
                gitter["lw"].add(xc, yc, 0.0)
                bil["gesetzt"]["ueberspannt"] += 1
                n_lw_rest -= 1
        # ---- 3. Wurzelstoecke und 4. Staemme am Ufer (teils im Wasser)
        n_wu = int(round(float(A["wurzel_anteil"]) * n_lw)) if wu_pal else 0
        for art, n_soll, pal in (("wurzel", min(n_wu, n_lw_rest), wu_pal), ("stamm", None, stamm_pal)):
            if not pal:
                continue
            if n_soll is None:
                n_soll = n_lw_rest
            n_gesetzt = 0
            for k in range(8 * n_soll + 4):
                if n_gesetzt >= n_soll:
                    break
                rk = rng(art, n_seg, k)
                sc = float(rk.uniform(a + 1.0, b - 1.0))
                sg = 1.0 if rk.uniform() < 0.5 else -1.0
                h_ = float(kanal.halb(sc, sg))
                B_ = float(kanal.B_bei(sc))
                if art == "wurzel":
                    L = float(rk.uniform(*A["wurzel_groesse_m"]))
                    netz, L, Ln, H = _netz_nach_laenge(inv, pal, L, rk, (0.7, 1.6))
                    u = sg * (h_ + float(rk.uniform(-0.2, 0.8)))
                    yaw = float(rk.uniform(0, 360))
                else:
                    # Laenge gleichverteilt bis zur Bachbreite (breite Baeche: ganze Spanne, viele Netze)
                    L = float(rk.uniform(A["stamm_laenge_m"][0],
                                         float(np.clip(B_ * A["stamm_laenge_B"][1], A["stamm_laenge_m"][0] + 0.5,
                                                       A["stamm_laenge_m"][1]))))
                    netz, L, Ln, H = _netz_nach_laenge(inv, pal, L, rk)
                    u = sg * (h_ + float(rk.uniform(*A["ufer_u_m"])))
                    tx, ty = kanal.tang(sc)
                    w = float(rk.uniform(*A["ufer_winkel_grad"])) * (1 if rk.uniform() < 0.5 else -1)
                    yaw = (_yaw(tx, ty) + w) % 360.0
                xc, yc = kanal.punkt(sc, u)
                dx, dy = _richtung(yaw)
                x0, y0, x1, y1 = xc - dx * L / 2, yc - dy * L / 2, xc + dx * L / 2, yc + dy * L / 2
                if not frei_lippe(x0, y0, x1, y1) or not ok_ort(xc, yc):
                    bil["blockiert"] += 1
                    grund["lippe_ort"] = grund.get("lippe_ort", 0) + 1
                    continue
                if not gitter["lw"].frei_min(xc, yc, max(float(A["abstand_lw_m"]), 0.35 * L)):
                    grund["abstand"] = grund.get("abstand", 0) + 1
                    continue
                if not massiv.frei(x0, y0, x1, y1, 0.25):
                    grund["block"] = grund.get("block", 0) + 1
                    continue
                if art == "wurzel":
                    stk = setze_stueck("wurzel", netz, L, xc, yc, yaw, "begleiter", "wurzel", True,
                                       {"groesse_achse": "xy", "eingraben": [0.2, 0.35]})
                else:
                    stk = setze_stueck("stamm", netz, L, xc, yc, yaw, "begleiter", "stamm", True,
                                       {"eingraben": [0.15, 0.3]})
                if stk is None:
                    bil["blockiert"] += 1
                    grund["filter"] = grund.get("filter", 0) + 1
                    continue
                stk["_bb"] = {"art": art, "s": sc, "u": u}
                gitter["lw"].add(xc, yc, 0.0)
                bil["gesetzt"][art] += 1
                n_gesetzt += 1
                n_lw_rest -= 1
        # ---- 5. Aeste am Ufer, 6. Zweige auf Kiesbaenken / am Gleithang (Innenufer)
        for art, n_soll, pal, eb in (("ast", n_ast, ast_pal, "schutt"), ("zweig", n_zw, zw_pal, "kleinzeug")):
            if not pal or n_soll <= 0:
                continue
            n_gesetzt = 0
            for k in range(5 * n_soll + 4):
                if n_gesetzt >= n_soll:
                    break
                rk = rng(art, n_seg, k)
                sc = float(rk.uniform(a + 0.5, b - 0.5))
                if art == "zweig":
                    kr = float(kanal.kruemmung(sc))
                    # Innenufer = Seite, zu der der Bach dreht (+ links); gerade Strecken: zufaellig
                    sg = (1.0 if kr > 0 else -1.0) if abs(kr) >= 0.004 and rk.uniform() < 0.8 else \
                        (1.0 if rk.uniform() < 0.5 else -1.0)
                    u = sg * (float(kanal.halb(sc, sg)) + float(rk.uniform(*A["zweig_u_m"])))
                    netz = pal[int(rk.integers(len(pal)))]
                    Ln = inv.stamm_form(netz)[0]
                    L = Ln * float(rk.uniform(*A["zweig_skala"]))
                    L = min(L, SKALA[1] * Ln)
                else:
                    sg = 1.0 if rk.uniform() < 0.5 else -1.0
                    u = sg * (float(kanal.halb(sc, sg)) + float(rk.uniform(*A["ast_u_m"])))
                    L = float(rk.uniform(*A["ast_laenge_m"]))
                    netz, L, Ln, H = _netz_nach_laenge(inv, pal, L, rk, (0.3, SKALA[1]))
                yaw = float(rk.uniform(0, 360))
                xc, yc = kanal.punkt(sc, u)
                dx, dy = _richtung(yaw)
                x0, y0, x1, y1 = xc - dx * L / 2, yc - dy * L / 2, xc + dx * L / 2, yc + dy * L / 2
                if not frei_lippe(x0, y0, x1, y1) or not ok_ort(xc, yc):
                    continue
                gi = gitter[art]
                if not gi.frei_min(xc, yc, float(A["abstand_%s_m" % art])):
                    continue
                if not massiv.frei(x0, y0, x1, y1, 0.05, (0.35, 0.65)):
                    continue
                h_ = float(kanal.halb(sc, sg))
                kol = art == "ast" and abs(u) - h_ <= float(A["kollision_ufer_m"]) and L >= 0.8
                stk = setze_stueck(art, netz, L, xc, yc, yaw, eb, "stamm", kol, {"eingraben": [0.1, 0.25]})
                if stk is None:
                    continue
                stk["_bb"] = {"art": art, "s": sc, "u": u}
                gi.add(xc, yc, 0.0)
                bil["gesetzt"][art] += 1
                n_gesetzt += 1
        bil["lw_neu_gesetzt"] = sum(bil["gesetzt"][k] for k in ARTEN_LW)
    return bilanz


def ruhe_aus_gefaelle(s, z, R=None):
    """Roh-Laeufe (16c Nachtrag 3): Ruhe 0..1 je s aus dem Spiegelgefaelle ueber roh.ruhe_fenster_m - flach (<= ruhe
    Gefaelle [0]) ruhig (Schlamm), steil (>= [1]) Schnelle (Kies). Rueckgabe Funktion s -> Ruhe."""
    A = (R or regeln()).a["roh"]
    s = np.asarray(s, np.float64)
    z = np.asarray(z, np.float64)
    h = float(A["ruhe_fenster_m"]) / 2.0
    S = (np.interp(s - h, s, z) - np.interp(s + h, s, z)) / np.maximum(np.minimum(s + h, s[-1]) - np.maximum(s - h, s[0]),
                                                                         1e-3)
    g0, g1 = A["ruhe_gefaelle"]
    r = 1.0 - np.clip((S - g0) / max(g1 - g0, 1e-6), 0.0, 1.0)
    r = r * r * (3.0 - 2.0 * r)
    return lambda s_: np.interp(np.asarray(s_, np.float64), s, r), S


def felsen_setzen(ctx, kanal, segmente, pal_fn, R=None, see_fn=None, gefaelle_fn=None, name_teil="", ohne_fn=None):
    """Bachbett-Felsen fuer Laeufe ohne Stufenplan (16c Nachtrag 3, Roh-Laeufe): Ufersteine/-bloecke an der Wasserkante,
    Stoersteine im Wasser (teils aus dem Wasser ragend) und Kies-/Steinpackungen am Ufer und im Bett. Dichte je 100 m
    nach dem Gefaelle (roh.felsen), Netze je Biom aus pal_fn(biom) -> {'bloecke': [...], 'kies': [...]} (Paletten des
    Gefaelle-Regelwerks). Bloecke ab kollision_ab_m mit Kollision (fluss_sim: Wasser-Kollision im Wasser bzw. <= 1 m
    daneben). ohne_fn(x, y) -> True, wo keine Felsen gesetzt werden (Felder mit lokaler Ufer-Ebene). Gruppen
    'bbf_<teil><art>_<nr>'. Rueckgabe Bilanz je Segment."""
    R = R or regeln()
    F = R.a["roh"]["felsen"]
    zaehler = {"n": 0}
    gitter = {"block": _ins.Abstandsgitter(4.0), "kies": _ins.Abstandsgitter(2.0)}
    out = []

    def rng(*t):
        return _ins.rng_fuer(ctx.seed, ctx.id, "bbf", *t)

    for n_seg, (a, b, biom) in enumerate(segmente):
        L = float(b - a)
        bil = {"segment": n_seg, "s_m": [round(float(a), 2), round(float(b), 2)], "biom": R.biom(biom)[0],
               "gesetzt": {"ufer": 0, "wasser": 0, "kies": 0}, "ziel": {}, "ohne": 0}
        out.append(bil)
        if L < float(R.a["min_laenge_m"]):
            continue
        pal = pal_fn(biom) or {}
        bl = [n for n in pal.get("bloecke") or [] if ctx.inv.netz_pfad(n)]
        ki = [n for n in pal.get("kies") or [] if ctx.inv.netz_pfad(n)] or bl
        if not bl:
            continue
        S = float(np.clip(np.median(gefaelle_fn(np.linspace(a, b, 9))) if gefaelle_fn else 0.0, 0.0, 1.0))
        g0, g1 = F["gefaelle_bezug"]
        t = float(np.clip((S - g0) / max(g1 - g0, 1e-6), 0.0, 1.0))
        r_ = rng("seg", n_seg)
        ziel = {k: int(math.floor((F[k + "_je_100m"][0] + t * (F[k + "_je_100m"][1] - F[k + "_je_100m"][0])) * L / 100.0
                                  + r_.uniform())) for k in ("ufer", "wasser", "kies")}
        bil["ziel"] = dict(ziel, gefaelle=round(S, 4))
        for art in ("ufer", "wasser", "kies"):
            n_soll = ziel[art]
            n_g = 0
            for k in range(6 * n_soll + 4):
                if n_g >= n_soll:
                    break
                rk = rng(art, n_seg, k)
                sc = float(rk.uniform(a + 0.5, b - 0.5))
                sg = 1.0 if rk.uniform() < 0.5 else -1.0
                h_ = float(kanal.halb(sc, sg))
                B_ = float(kanal.B_bei(sc))
                if art == "ufer":
                    u = sg * (h_ + float(rk.uniform(*F["ufer_u_m"])))
                    gr = list(F["ufer_groesse_m"])
                    pal_ = bl
                    eb = "schutt"
                elif art == "wasser":
                    u = sg * h_ * float(rk.uniform(0.0, F["wasser_u_anteil"]))
                    gmax = float(np.clip(F["wasser_groesse_B"][1] * B_, F["wasser_groesse_m"][0], F["wasser_groesse_m"][1]))
                    gr = [float(F["wasser_groesse_m"][0]), max(gmax, float(F["wasser_groesse_m"][0]) + 0.1)]
                    pal_ = bl
                    eb = "schutt"
                else:
                    u = sg * (h_ + float(rk.uniform(*F["kies_u_m"])))
                    gr = list(F["kies_groesse_m"])
                    pal_ = ki
                    eb = "kleinzeug"
                xc, yc = kanal.punkt(sc, u)
                if see_fn is not None and bool(np.any(see_fn(np.array([xc]), np.array([yc])))):
                    continue
                if ohne_fn is not None and ohne_fn(xc, yc):
                    bil["ohne"] += 1
                    continue
                gi = gitter["kies" if art == "kies" else "block"]
                if not gi.frei_min(xc, yc, float(F["abstand_%s_m" % ("kies" if art == "kies" else "block")])):
                    continue
                groesse = float(rk.uniform(*gr))
                nm = "bbf_%s%s_%03d" % (name_teil, art, zaehler["n"])
                zaehler["n"] += 1
                ctx.anker[nm + "__000"] = (float(xc), float(yc))
                ctx.richtungen[nm + "__000"] = float(rk.uniform(0.0, 360.0))
                kol = art != "kies" and groesse >= float(F["kollision_ab_m"])
                g = {"name": nm, "ebene": eb, "palette": [pal_[int(rk.integers(len(pal_)))]],
                     "verteilung": {"typ": "anker", "praefix": nm + "__"}, "rolle": "fels",
                     "groesse_m": [groesse, groesse], "groesse_achse": "max", "akteur": False, "kollision": kol,
                     "im_wasser": "egal", "meide": None, "eingraben": list(F["eingraben"]), "boden_min_m": 0.2,
                     "weg_abstand_m": 4.0 if art != "kies" else 2.5, "yaw_streuung_grad": 0.0,
                     "warum": "Bachbett-Felsen Roh-Lauf (16c Nachtrag 3): %s" % art}
                try:
                    stk = ctx.gruppe(g)
                except (KeyError, ValueError) as ex:
                    ctx.melde("WARNUNG", "Bachbett-Felsen %s: %s" % (nm, ex))
                    continue
                if not stk:
                    continue
                stk[0]["_bb"] = {"art": "fels_" + art, "s": sc, "u": u}
                gi.add(xc, yc, 0.0)
                bil["gesetzt"][art] += 1
                n_g += 1
    return out


# ======================================================================================================================
# Stuecke nach dem Ausduennen (plan.json / orte.json)
# ======================================================================================================================
def achse_enden(inv, pfad, q, s, pos_cm):
    """Lange waagrechte Achse eines gedrehten Netzes: (x0, y0, x1, y1) in m, Mitte, Laenge."""
    info = inv.netz(pfad)
    P = _ins.gedrehte_box(info, q, s)
    xy = P[:, :2] / 100.0
    c = xy.mean(0)
    Q = xy - c
    w_, V = np.linalg.eigh(Q.T @ Q)
    v = V[:, -1]
    pr = Q @ v
    a, b = float(pr.min()), float(pr.max())
    cx, cy = float(pos_cm[0]) / 100.0 + c[0], float(pos_cm[1]) / 100.0 + c[1]
    return (cx + v[0] * a, cy + v[1] * a, cx + v[0] * b, cy + v[1] * b), (cx, cy), b - a


def stuecke_block(ctx, kanal, inv, bilanz=None, gruppen_praefix=PRAEFIX):
    """Liste der gesetzten Bachbett-Stuecke dieses Orts/Abschnitts (nach dem Ausduennen, wie geschrieben)."""
    out = []
    ids = {}
    for g, lst in ctx.gruppen.items():
        if g.startswith(gruppen_praefix):
            for s_ in lst:
                if s_.get("stueck") is not None:
                    ids[id(s_["stueck"])] = s_
    for e in ctx.ebene.vom_ort(ctx.id):
        if not e["gruppe"].startswith(gruppen_praefix):
            continue
        stk = ids.get(id(e))
        bb = (stk or {}).get("_bb", {})
        (x0, y0, x1, y1), (cx, cy), L = achse_enden(inv, e["pfad"], e["q"], e["s"], (e["x"], e["y"]))
        d, s, u = kanal.projektion(np.array([cx, x0, x1]), np.array([cy, y0, y1]))
        zs = float(kanal.z(s[0], u[0]))
        uk = (stk or {}).get("unterkante_z_m")
        halb = float(kanal.halb(s[0], u[0]))
        lage = "wasser" if d[0] < halb else ("ufer" if d[0] <= halb + 1.0 else "land")
        art = bb.get("art") or (e["gruppe"][len(gruppen_praefix):].rsplit("_", 1)[0] if isinstance(gruppen_praefix, str)
                                else "bestand")
        out.append({"gruppe": e["gruppe"], "art": art,
                    "typ": bb.get("typ"), "netz": e["netz"], "pfad": e["pfad"], "ebene": e["ebene"],
                    "pos_cm": [round(e["x"], 1), round(e["y"], 1), round(e["z"], 1)],
                    "achse_cm": [[round(x0 * 100, 1), round(y0 * 100, 1)], [round(x1 * 100, 1), round(y1 * 100, 1)]],
                    "laenge_m": round(L, 2), "s_m": round(float(s[0]), 2), "u_m": round(float(u[0]), 2),
                    "s_enden_m": [round(float(s[1]), 2), round(float(s[2]), 2)],
                    "lage": lage, "spiegel_cm": round(zs * 100, 1),
                    "unterkante_ueber_spiegel_m": None if uk is None else round(float(uk) - zs, 2),
                    "kollision": bool(e["kollision"]), "z_frei": bool(e.get("z_frei")),
                    "skala": round(float(max(e["s"])), 3)})
    return out


def dichte_zusammenfassen(stuecke, bilanz, bestand_stuecke=None):
    """Dichte grosses Totholz je Segment (neu + Bestand) -> Liste fuer plan.json."""
    out = []
    for bil in bilanz or []:
        a, b = bil["s_m"]
        n_neu = sum(1 for st in stuecke if st["art"] in ARTEN_LW and a - 1.0 <= st["s_m"] <= b + 1.0)
        n_best = sum(1 for st in (bestand_stuecke or []) if a - 1.0 <= st["s_m"] <= b + 1.0)
        L = max(float(bil["laenge_m"]), 1e-6)
        d = dict(bil)
        d["lw_neu"] = n_neu
        d["lw_bestand"] = n_best
        d["lw_je_100m"] = round(100.0 * (n_neu + n_best) / L, 2)
        d["aeste"] = sum(1 for st in stuecke if st["art"] == "ast" and a - 1.0 <= st["s_m"] <= b + 1.0)
        d["zweige"] = sum(1 for st in stuecke if st["art"] == "zweig" and a - 1.0 <= st["s_m"] <= b + 1.0)
        out.append(d)
    return out


# ======================================================================================================================
# Lagen: Schlamm, Uferstreifen
# ======================================================================================================================
def _max3(W):
    """3 x 3-Maximum (Rand: Kante wiederholt)."""
    P = np.pad(W, 1, mode="edge")
    out = W.copy()
    for di in (0, 1, 2):
        for dj in (0, 1, 2):
            out = np.maximum(out, P[di:di + W.shape[0], dj:dj + W.shape[1]])
    return out


def bett_lagen(X, Y, F, z_sp, d, halb, ruhe, kr_seite, biom, nah, R=None, seed=0, w_str_min=None):
    """Ziel-Lagen (0-255) auf einem Raster. F Boden nach dem Stempel, z_sp Spiegel, d Abstand zur Mittellinie, halb
    halbe Wasserbreite (Seite der Zelle), ruhe 0..1, kr_seite Kruemmung zur Seite der Zelle (> 0: Zelle am Innenufer),
    nah: Zellen, die zum Gerinne gehoeren (Projektion innerhalb der Segmente). Rueckgabe (lagen, w_streifen,
    w_schlamm)."""
    R = R or regeln()
    A = R.a
    bn, Rb = R.biom(biom)
    h = F - z_sp
    tiefe = -h
    h0, h1, h2 = A["streifen_hoehe_m"]
    w_h = np.where(h <= h1, _st.glatt01((h - (h0 - 0.15)) / 0.15), 1.0 - _st.glatt01((h - h1) / (h2 - h1)))
    br, rd = float(A["streifen_breite_m"]), float(A["streifen_rand_m"])
    w_d = 1.0 - _st.glatt01((d - halb - br) / rd)
    w_d = w_d * _st.glatt01((d - (halb - 0.8)) / 0.4)
    w_str = np.clip(w_h * w_d, 0.0, 1.0) * nah
    if w_str_min is not None:
        w_str = np.maximum(w_str, np.clip(w_str_min, 0.0, 1.0) * nah * (1.0 - _st.glatt01((d - halb - br) / rd)))
    # Mischung je Biom mit Rauschen (fleckig, Summe = Deckung)
    teile = list(Rb["streifen"].items())
    gew = []
    for k, (n, f) in enumerate(teile):
        rz = _st.rauschen(X, Y, 4.0, seed + 977 * (k + 1))
        gew.append(float(f) * np.clip(0.55 + 0.6 * rz, 0.05, None))
    summe = np.maximum(sum(gew), 1e-6)
    lagen = {}
    for (n, _), g in zip(teile, gew):
        lagen[n] = np.maximum(lagen.get(n, 0.0), 255.0 * w_str * g / summe)
    # Schlamm im ruhigen, tiefen Becken (Uebergang zu Kies an den Schnellen ueber 'ruhe') und am Gleithang
    t0, t1 = A["schlamm_tiefe_m"]
    w_b = ruhe * _st.glatt01((tiefe - t0) / max(t1 - t0, 1e-3)) * _st.glatt01((halb - float(A["schlamm_rand_m"]) - d) / 0.6)
    gl = (kr_seite >= float(A["gleithang_kruemmung_min"])) & (tiefe >= -0.05) & \
        (tiefe <= float(A["gleithang_tiefe_max_m"])) & (d >= halb - 1.6)
    w_g = 0.7 * gl * np.clip(ruhe + 0.3, 0.0, 1.0) * _st.glatt01(np.abs(kr_seite) / 0.03)
    rz = _st.rauschen(X, Y, 3.0, seed + 4441)
    w_sch = np.clip(np.maximum(w_b, w_g) * (0.75 + 0.35 * rz), 0.0, 1.0) * nah
    lagen[Rb["becken"]] = np.maximum(lagen.get(Rb["becken"], 0.0), float(Rb["becken_wert"]) * w_sch)
    return lagen, w_str, w_sch


def lagen_mischen(arr, zusatz, w_str, w_sch, R=None):
    """arr: dict Lage -> Array (wird geaendert). Gras-Lagen im Uferstreifen daempfen (wie die Nadelstreu in 13k),
    Kies unter dem Schlamm daempfen, dann die Zusatz-Lagen per Maximum dazu."""
    A = (R or regeln()).a
    neu = set(zusatz)
    for n in list(arr):
        if n in A["gras_lagen"]:
            arr[n] = arr[n] * (1.0 - w_str)                       # trockenes Gras direkt am Wasser: weg
        elif n not in neu:
            arr[n] = arr[n] * (1.0 - float(A["streifen_daempfung"]) * w_str)   # Kies/Geroell/Nadeln: Streifen vorn
    if "Kies" in arr:
        arr["Kies"] = arr["Kies"] * (1.0 - float(A["kies_daempfung"]) * w_sch)
    for n, v in zusatz.items():
        arr[n] = np.maximum(arr.get(n, np.zeros_like(v)), v) if n in arr else v
    return arr


# ======================================================================================================================
# Pruefer-Helfer
# ======================================================================================================================
def dichte_grenzen(biom, f, R=None):
    R = R or regeln()
    bn, Rb = R.biom(biom)
    lo, ziel, hi = Rb["lw_je_100m"]
    return bn, lo * f, ziel * f, hi * f


def dichte_bewerten(biom, f, laenge_m, n_lw, blockiert=0, R=None, n_neu=None, rahmen=None):
    """-> (stufe | None, text). FEHLER ueber max; unter min FEHLER ab pruef_min_laenge_m (WARNUNG mit blockierten
    Plaetzen, darunter HINWEIS). rahmen = dichte(...) (16c Nachtrag 3: Waldnaehe statt Biom-Etikett); ohne rahmen
    Biom-Dichte x f (alter Weg)."""
    R = R or regeln()
    if rahmen is not None:
        bn = rahmen["biom"]
        lo, ziel, hi = (float(v) for v in rahmen["lw"])
        f = float(rahmen.get("wald_faktor", 1.0))
    else:
        bn, lo, ziel, hi = dichte_grenzen(biom, f, R)
    if laenge_m < float(R.a["min_laenge_m"]):
        return None, ""
    je = 100.0 * n_lw / max(laenge_m, 1e-6)
    # Rundung: ein Stueck mehr/weniger als die Grenze auf kurzen Strecken ist erlaubt
    tol = 100.0 / max(laenge_m, 1e-6) if hi > 0 else 0.0
    zus = ""
    if rahmen is not None and rahmen.get("wald_biom") and rahmen["wald_biom"] != bn:
        zus = ", Ufer-Wald %s Gewicht %.2f, Treibholz %.2f" % (rahmen["wald_biom"], float(rahmen.get("wald_gewicht", 0)),
                                                              float(rahmen.get("treibholz", 0)))
    txt = "%s: %.1f grosse Totholzstuecke je 100 m (%d auf %.0f m), Rahmen %.1f-%.1f (Ziel %.1f, Waldfaktor %.2f%s)" % (
        bn, je, n_lw, laenge_m, lo, hi, ziel, f, zus)
    if je > hi + tol + 1e-9:
        if n_neu == 0:
            return "HINWEIS", txt + " - schon der Bestand (Holzstufen) liegt darueber, nichts dazugesetzt"
        return "FEHLER", txt + " - zu dicht"
    if je < lo - tol - 1e-9:
        if laenge_m >= float(R.a["pruef_min_laenge_m"]):
            return ("WARNUNG" if blockiert else "FEHLER"), txt + " - zu duenn" + (
                " (%d Plaetze durch Weg/Ort/See/Lippe blockiert)" % blockiert if blockiert else "")
        return "HINWEIS", txt + " - zu duenn (kurze Strecke)"
    return None, txt


def rahmen_vergleichen(seg, rahmen, tag, stufe="FEHLER"):
    """Pruefer: Waldfaktor, Ufer-Wald-Gewicht und Rahmen im Plan gegen nachgerechnet (dichte()). Liste von Befunden."""
    out = []
    f, f2 = float(seg.get("wald_faktor", 1.0)), float(rahmen["wald_faktor"])
    if abs(f2 - f) > 0.02:
        out.append((stufe, tag, "Bachbett: Waldfaktor %.3f im Plan, nachgerechnet %.3f" % (f, f2)))
    if "wald_gewicht" not in seg or "rahmen_lw" not in seg:
        out.append((stufe, tag, "Bachbett: Segment %s ohne wald_gewicht/rahmen_lw (16c Nachtrag 3: Totholz nach "
                                "Waldnaehe)" % (seg.get("s_m"),)))
        return out
    g, g2 = float(seg["wald_gewicht"]), float(rahmen["wald_gewicht"])
    z, z2 = float(seg["rahmen_lw"][1]), float(rahmen["lw"][1])
    if abs(g2 - g) > 0.02 or abs(z2 - z) > 0.05 * max(1.0, z2):
        out.append((stufe, tag, "Bachbett: Ufer-Wald-Gewicht %.3f / Ziel %.2f je 100 m im Plan, nachgerechnet %.3f / %.2f"
                    % (g, z, g2, z2)))
    return out


def streifen_bewerten(h, d, halb, nah_ok, summe_streifen, R=None):
    """Uferstreifen-Pruefung: Zellen h in streifen_pruef_hoehe_m, d <= halb + streifen_pruef_breite_m (ausserhalb der
    Lippenzonen: nah_ok) -> Anteil mit Streifen-Lagen >= 200. Rueckgabe (n_zellen, anteil)."""
    A = (R or regeln()).a
    a, b = A["streifen_pruef_hoehe_m"]
    m = nah_ok & (h >= a) & (h <= b) & (d <= halb + float(A["streifen_pruef_breite_m"])) & (d >= halb - 0.5)
    n = int(m.sum())
    if not n:
        return 0, 1.0
    return n, float((summe_streifen[m] >= 200.0).mean())


# ======================================================================================================================
# Sehens-Bach-Planer (rezept.OrtKontext): Adapter
# ======================================================================================================================
def sehens_kanal(ctx, wid, R=None):
    """Kanal eines geplanten Sehens-Bachs (ctx.bach_plan[wid], 13f): Spiegel-Treppe W(s), Breite B, gerade Lippen
    (quer ueber die ganze Breite), Wasserkante = bach.halbe_breite_eff."""
    from . import bach as _bach
    pl = ctx.bach_plan[wid]
    s, x, y, W = (np.asarray(pl[k], np.float64) for k in ("s", "x", "y", "W"))
    B = float(pl["B"])
    he = float(_bach.halbe_breite_eff(B, ctx.welt.zelle_m))
    stufen = [{"s_lippe": float(st["s_lippe"]), "s_fuss": float(st["s_fuss"]), "fall": float(st["fall_m"]),
               "gross": round(float(st["fall_m"]), 2) >= 1.0, "halb": B / 2.0} for st in pl["stufen"]]
    return Kanal(s, x, y, W, np.full(len(s), B), stufen, halb_fn=lambda s_, u_: np.full(np.shape(s_), he), R=R,
                 zonen_zuschlag_m=0.1)


def sehens_aktiv(ctx, wid):
    for w in ctx.r.get("wasser") or []:
        if w.get("typ") == "bach" and w.get("id") == wid:
            return w.get("bachbett", True) is not False
    return True


def sehens_totholz(ctx, R=None):
    """Totholz an allen geplanten Baechen eines Sehens-Orts (nach den Rezeptgruppen, vor dem Akteur-Buendeln).
    Gruppen 'bb_<bach>_<art>_<nr>'; Rezept-Feld je Bach 'bachbett': false schaltet ab."""
    R = R or regeln()
    ctx._bachbett = {}
    for wid in sorted(ctx.bach_plan):
        if not sehens_aktiv(ctx, wid):
            continue
        kanal = sehens_kanal(ctx, wid, R)
        L = float(kanal.s[-1])
        if L < float(R.a["min_laenge_m"]):
            ctx._bachbett[wid] = {"kanal": kanal, "bilanz": [], "name_teil": "%s_" % wid}
            continue

        def see_fn(x, y):
            m = np.zeros(np.shape(x), bool)
            for sv in ctx.see.values():
                if sv.get("umriss_m") is not None and len(sv["umriss_m"]) >= 3:
                    m |= ctx._im_see_puffer(x, y, sv, 1.0)
            return m
        segs = [(2.0, L - 2.0, ctx.biom)]
        bil = totholz_setzen(ctx, kanal, segs, R, ctx.welt, None, "bb_%s" % wid, see_fn, name_teil="%s_" % wid)
        ctx._bachbett[wid] = {"kanal": kanal, "bilanz": bil, "name_teil": "%s_" % wid}


def sehens_lagen(ctx, R=None):
    """Schlamm und nasser Uferstreifen an allen geplanten Baechen (Lagen-Raster des Orts, Boden nach dem Stempel)."""
    R = R or regeln()
    lg = ctx.lagen
    if lg is None or not getattr(ctx, "_bachbett", None):
        return
    X, Y = lg.X, lg.Y
    F = np.asarray(ctx.boden(X, Y), np.float64)
    zus, w_str, w_sch = {}, np.zeros(X.shape), np.zeros(X.shape)
    for wid, info in sorted(ctx._bachbett.items()):
        kanal = info["kanal"]
        rand = float(np.max(kanal.B)) / 2.0 + 8.0
        box = (X >= kanal.x.min() - rand) & (X <= kanal.x.max() + rand) & (Y >= kanal.y.min() - rand) & \
            (Y <= kanal.y.max() + rand)
        if not box.any():
            continue
        xs, ys = X[box], Y[box]
        d, s, u = kanal.projektion(xs, ys)
        L = float(kanal.s[-1])
        nah = ((s >= 1.0) & (s <= L - 1.0) & (d <= kanal.halb_netz(s) + 6.0)).astype(np.float64)
        if not nah.any():
            continue
        kr = kanal.kruemmung(s) * np.where(u >= 0, 1.0, -1.0)
        arg = (xs, ys, F[box], kanal.z(s, u), d, kanal.halb(s, u), kanal.ruhe(s), kr, ctx.biom, nah, R)
        lg_, ws_, wsch_ = bett_lagen(*arg, seed=ctx.seed)
        if float(lg.z) > 1.0:
            # 2-m-Raster: ein 1-3 m breiter Bach hat nur 1-2 Zellen Ufer - Streifen um eine Zelle verbreitern, damit
            # er nach dem Hochrechnen auf 1 m die Uferzellen deckt
            W2 = np.zeros(X.shape)
            W2[box] = ws_
            lg_, ws_, wsch_ = bett_lagen(*arg, seed=ctx.seed, w_str_min=_max3(W2)[box])
        for n, v in lg_.items():
            full = zus.get(n, np.zeros(X.shape))
            full[box] = np.maximum(full[box], v)
            zus[n] = full
        w_str[box] = np.maximum(w_str[box], ws_)
        w_sch[box] = np.maximum(w_sch[box], wsch_)
        z_ = float(lg.z) ** 2
        info["lagen"] = {"streifen_m2": round(float((ws_ >= 0.5).sum()) * z_, 1),
                         "schlamm_m2": round(float((wsch_ >= 0.3).sum()) * z_, 1)}
    if zus:
        lagen_mischen(lg.ziel, zus, w_str, w_sch, R)


def sehens_eintrag(ctx):
    """orte.json: je Bach-Eintrag 'bachbett' (Stuecke nach dem Ausduennen, Dichte, Lagen-Kennzahlen)."""
    info_alle = getattr(ctx, "_bachbett", None) or {}
    for w in ctx.wasser or []:
        if w.get("typ") != "bach" or w.get("id") not in info_alle:
            continue
        info = info_alle[w["id"]]
        st = stuecke_block(ctx, info["kanal"], ctx.inv, gruppen_praefix=PRAEFIX + info["name_teil"])
        w["bachbett"] = {"regeln": "sehens_lib/bachbett_regeln.json", "version": regeln().version,
                         "stuecke": st, "bestand": [], "dichte": dichte_zusammenfassen(st, info["bilanz"]),
                         "lagen": info.get("lagen")}


# ======================================================================================================================
# Pruefer Sehens (orte.json + sw_<biom>)
# ======================================================================================================================
def pruefe_orte_bachbett(d, basis, welt, sw_ordner, inv):
    """16c Nachtrag 18:15 fuer die Sehens-Baeche (Regeln wie gefaelle_pruefen.pruefe_bachbett): Liste <-> Instanz-
    Ebene, Kollision grosses Totholz am Wasser, keine Stuecke mitten in einer Lippe, Dichte je Biom, Uferstreifen
    (auf 1 m FEHLER, auf 2 m WARNUNG - ein 1-3 m breiter Bach ist im 2-m-Raster nicht aufloesbar)."""
    from . import instanzen as _ins_
    from .sehens_pruefen import BodenNachStempel
    R = regeln()
    A = R.a
    b = []
    idx = {}
    if sw_ordner and os.path.isdir(sw_ordner):
        for feld, (plan, arr) in _ins_.lies_ebene(sw_ordner).items():
            for key, a in arr.items():
                if a.ndim != 2:
                    continue
                info = (plan.get("dateien") or {}).get(key, {})
                netz = key.split("__")[0]
                kol = bool(info.get("kollision", netz.endswith("_kol")))
                netz = netz[:-4] if netz.endswith("_kol") else netz
                for r in a:
                    idx.setdefault(netz, []).append((kol, r, info.get("pfad")))
    for o in d.get("orte") or []:
        oid = o.get("id", "?")
        for w in o.get("wasser") or []:
            if w.get("typ") != "bach" or len(w.get("punkte_cm") or []) < 2:
                continue
            tag = "%s/%s" % (oid, w.get("id"))
            bb = w.get("bachbett")
            if bb is None:
                b.append(("FEHLER", tag, "bach ohne 'bachbett' (16c Nachtrag 18:15: Totholz, Schlamm, Uferstreifen)"))
                continue
            Pq = np.asarray(w["punkte_cm"], np.float64) / 100.0
            P = Pq[:, :2]
            kum = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))])
            Bm = float(np.median(Pq[:, 3]))

            def proj(x, y):
                return projektion_schnell(x, y, P, 1024)
            stufen = []
            for st in w.get("stufen") or []:
                _, sl, _ = proj([st["lippe_cm"][0] / 100.0], [st["lippe_cm"][1] / 100.0])
                _, sf, _ = proj([st["fuss_cm"][0] / 100.0], [st["fuss_cm"][1] / 100.0])
                stufen.append({"s_lippe": float(sl[0]), "s_fuss": float(max(sf[0], sl[0])), "fall": float(st["fall_m"]),
                               "gross": float(st["fall_m"]) >= 1.0, "halb": Bm / 2.0})
            zonen = lippen_zonen(stufen, R)
            n_fehlt, n_lippe, n_kol = 0, 0, 0
            ok_st = []
            for st in bb.get("stuecke") or []:
                k = [(kol, r, pf) for kol, r, pf in idx.get(st["netz"], []) if abs(r[0] - st["pos_cm"][0]) <= 2.0 and
                     abs(r[1] - st["pos_cm"][1]) <= 2.0 and abs(r[2] - st["pos_cm"][2]) <= 2.0]
                if not k:
                    n_fehlt += 1
                    continue
                kol, r, pf = k[0]
                ok_st.append(st)
                (x0, y0, x1, y1), (cx, cy), L = achse_enden(inv, pf or st["pfad"], tuple(r[3:7]), tuple(r[7:10]),
                                                            (r[0], r[1]))
                t = np.linspace(0.0, 1.0, 9)
                dd, ss, uu = proj(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
                if in_zonen(ss, zonen, uu).any():
                    n_lippe += 1
                if st["art"] in ARTEN_LW:
                    dc, _, _ = proj([cx], [cy])
                    if dc[0] <= Bm / 2.0 + float(A["kollision_ufer_m"]) and not kol:
                        n_kol += 1
            if n_fehlt:
                b.append(("FEHLER", tag, "Bachbett: %d gelistete Totholz-Stuecke nicht in sw_<biom>" % n_fehlt))
            if n_lippe:
                b.append(("FEHLER", tag, "Bachbett: %d Totholz-Stuecke mitten in einer Lippe/einem Vorhang" % n_lippe))
            if n_kol:
                b.append(("FEHLER", tag, "Bachbett: %d grosse Totholz-Stuecke am Wasser ohne Kollision" % n_kol))
            for seg in bb.get("dichte") or []:
                a_, b_ = seg["s_m"]
                n_lw = sum(1 for st in ok_st if st["art"] in ARTEN_LW and a_ - 1.0 <= st["s_m"] <= b_ + 1.0)
                f = float(seg.get("wald_faktor", 1.0))
                rahmen = None
                if welt is not None and float(seg["laenge_m"]) >= float(A["min_laenge_m"]):
                    ss_ = np.linspace(a_, b_, max(2, int(float(seg["laenge_m"]) / 2.0) + 1))
                    pts = np.stack([np.interp(ss_, kum, P[:, 0]), np.interp(ss_, kum, P[:, 1])], 1)
                    rahmen = dichte(welt, pts, seg["biom"], R)
                    b.extend(rahmen_vergleichen(seg, rahmen, tag))
                stf, txt = dichte_bewerten(seg["biom"], f, float(seg["laenge_m"]), n_lw, int(seg.get("blockiert", 0)),
                                           R, n_lw, rahmen=rahmen)
                if stf:
                    b.append((stf, tag, "Bachbett-Dichte " + txt))
            # Uferstreifen (Lagen des Orts, Boden nach dem Stempel)
            lgb = o.get("lagen") or {}
            if welt is None or not lgb.get("fenster_ij") or not bb.get("dichte"):
                continue
            li0, lj0, lh, lw = [int(v) for v in lgb["fenster_ij"]]
            _, Rb = R.biom(bb["dichte"][0]["biom"])
            jj, ii = np.meshgrid(np.arange(lj0, lj0 + lw, dtype=np.float64), np.arange(li0, li0 + lh, dtype=np.float64))
            from . import daten as _d
            X, Y = jj - _d.OFF_J, ii - _d.OFF_I
            box = (X >= P[:, 0].min() - Bm - 4) & (X <= P[:, 0].max() + Bm + 4) & (Y >= P[:, 1].min() - Bm - 4) & \
                (Y <= P[:, 1].max() + Bm + 4)
            if not box.any():
                continue
            xs, ys = X[box], Y[box]
            F = BodenNachStempel(welt, [o], basis).hoehe(xs, ys)
            dd, ss, uu = proj(xs, ys)
            z_sp = np.interp(ss, kum, Pq[:, 2])
            Lb = float(kum[-1])
            zv = lippen_zonen([dict(st, halb=1e9) for st in stufen], R, zuschlag=1.0)
            ok = (ss >= 3.0) & (ss <= Lb - 3.0) & ~in_zonen(ss, zv, uu)
            for f_ in w.get("furten") or []:
                _, sa, _ = proj([f_["von_cm"][0] / 100.0], [f_["von_cm"][1] / 100.0])
                _, sb, _ = proj([f_["bis_cm"][0] / 100.0], [f_["bis_cm"][1] / 100.0])
                ok &= ~((ss >= min(sa[0], sb[0]) - 3.0) & (ss <= max(sa[0], sb[0]) + 3.0))
            summe = np.zeros(len(xs))
            for n in Rb["streifen"]:
                if n in (lgb.get("lagen") or []):
                    q = os.path.join(basis, lgb["datei_praefix"] + n + ".r8")
                    if os.path.exists(q) and os.path.getsize(q) == lh * lw:
                        summe += np.fromfile(q, dtype=np.uint8).reshape(lh, lw)[box]
            n_z, anteil = streifen_bewerten(F - z_sp, dd, np.full(len(xs), Bm / 2.0), ok, summe, R)
            if n_z >= 15 and anteil < float(A["streifen_anteil_min"]):
                b.append(("FEHLER" if welt.zelle_m <= 1.0 else "WARNUNG", tag,
                          "Uferstreifen: nur %.0f %% von %d Uferzellen (0,05-0,5 m ueber dem Spiegel) mit %s >= 200"
                          % (100 * anteil, n_z, "/".join(Rb["streifen"]))))
    return b
