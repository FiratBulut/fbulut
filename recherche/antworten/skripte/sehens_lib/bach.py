"""bach.py - Baeche der Sehenswuerdigkeiten nach Auftrag 13f (A4, A8, A9, A12, A13).

Ein Bach (Regel "wasser" mit typ "bach") wird in drei Schritten gebaut:
  1. Enden (A4, A9, A13):  am Umriss des eigenen Sees abschneiden (Endpunkt auf dem Umriss, Spiegel = Seespiegel
     + 2 cm), Abfluss beginnt am Auslass auf dem Seespiegel; Muendung nur in Epic-Gewaesser (baeche_alle.json,
     wasser_welt.json Fluesse/Seen, teiche.json) - Houdini-Raster (karte_wasser) zaehlt nicht; sonst entlang der
     Tiefenlinie weiter, bis ein Epic-Gewaesser erreicht ist, oder 'versickert' mit mindestens 25 m Laenge.
     Ein Bachende liegt nie unter dem Spiegel des Zielgewaessers.
  2. Spiegel als Treppe (A8, Regelwerk Auftrag 15 'gefaelle_regeln.json'): Becken (<= 3 % Gefaelle, >= 3 m lang,
     Laenge nach stufen.abstand_L / becken.laenge_min) und Stufen (Lippe -> Fuss <= 1 m). Die Stufen stehen
     explizit im Bach ("stufen": [{"lippe_cm", "fuss_cm", "fall_m", "art"}]) - keine Vorhaenge aus vielen kleinen
     Faellen.
  3. Querprofil wie Auftrag 15b (A12): Wasserkante innen (0,3-0,5 m innerhalb der halben Breite, mind. 0,75 Zellen
     von der Mitte), Bett = Spiegel - Tiefe, Boeschung 35 Grad, Ufer beidseits >= Spiegel + 5 cm, Uferring auf
     Spiegel + 0,15 m bis Netzrand + 1,5 m (hebt hoechstens 1 m). Neben dem Fuss einer Stufe gilt 1,5 m lang der
     Oberwasser-Spiegel (Seitenwand des Falls).
Der Spiegel im Plan IST das gestempelte Bett + Tiefe (nicht das Bestandsgelaende).

Die Zahlen fuer Becken/Stufen kommen aus recherche/antworten/skripte/gefaelle/gefaelle_regeln.json ueber
gefaelle_regelwerk.Regelwerk (nur gelesen/importiert); fehlt es, gelten die Ersatzwerte unten.
"""

import importlib.util
import math
import os

import numpy as np

from . import log

HIER = os.path.dirname(os.path.abspath(__file__))
TAN_B = math.tan(math.radians(35.0))     # Boeschung 35 Grad (15b)
UFER_MIN_M = 0.05                        # Ufer >= Spiegel + 5 cm (A12)
RING_UEBER_M = 0.15                      # Uferring Spiegel + 0,15 m (15b)
NETZRAND_M = 0.4                         # Netzrand = halbe Breite + 0,4 m (15b)
RING_BREITE_M = 1.5
RING_AUSLAUF = 0.5                       # 1:2
WULST_MAX_M = 1.0                        # Uferring hebt hoechstens 1 m
EINBETTUNG_M = 0.05                      # Spiegel liegt so weit unter dem Gelaende (Huellkurve)
BECKEN_MIN_M = 3.0                       # A8: Becken >= 3 m
BECKEN_GEF_MAX = 0.03                    # A8: Becken <= 3 %
STUFE_MIN_M = 0.15                       # kleinere Spruenge bleiben Gefaelle
STUFE_L_M = 0.5                          # Lippe -> Fuss (Regelwerk stufen.zwei_punkte.abstand_ziel)
MUENDUNG_SEE_M = 0.02                    # A4: Endpunkt am eigenen See = Seespiegel + 2 cm
VERSICKERT_MIN_M = 25.0                  # A9
ZIEL_SUCHE_M = 6.0                       # Epic-Gewaesser naeher als (halbe Breite + das) am Ende = Muendung


# ============================================================================================
# Regelwerk Auftrag 15 (nur lesen)
# ============================================================================================
_RW = {"geladen": False, "rw": None}


def regelwerk():
    """gefaelle_regelwerk.Regelwerk (Auftrag 15) oder None. Wird per Dateipfad geladen (kein Paket noetig)."""
    if _RW["geladen"]:
        return _RW["rw"]
    _RW["geladen"] = True
    pf = os.path.normpath(os.path.join(HIER, "..", "gefaelle", "gefaelle_regelwerk.py"))
    try:
        spec = importlib.util.spec_from_file_location("_sehens_gefaelle_regelwerk", pf)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _RW["rw"] = mod.Regelwerk.lade()
    except Exception as ex:      # noqa: BLE001 - Regelwerk fehlt/kaputt: Ersatzwerte
        log("Hinweis: Regelwerk Auftrag 15 nicht geladen (%s) - Ersatzwerte fuer Becken/Stufen" % ex)
        _RW["rw"] = None
    return _RW["rw"]


def becken_laenge(S, B):
    """Beckenlaenge (m) zwischen zwei Stufen bei lokalem Gefaelle S: Regelwerk stufen.abstand_L (Krone-Krone) minus
    Stufenlaenge, mindestens becken.laenge_min und 3 m (A8)."""
    rw = regelwerk()
    L = BECKEN_MIN_M
    if rw is not None:
        try:
            L = max(L, rw.becken_laenge_min(B), rw.abstand_L(max(S, 0.03), B) - STUFE_L_M)
        except Exception:        # noqa: BLE001
            pass
    else:
        L = max(L, 0.8 * B, B * min(max(0.4 * max(S, 0.03) ** -0.7, 0.8), 4.0) - STUFE_L_M)
    return float(min(L, 12.0))


def becken_gefaelle():
    rw = regelwerk()
    try:
        return float(min(rw.becken_gefaelle_hart(), BECKEN_GEF_MAX)) if rw is not None else BECKEN_GEF_MAX
    except Exception:            # noqa: BLE001
        return BECKEN_GEF_MAX


def stufen_art(D):
    """schnelle | stufe | fall nach Regelwerk stufen.arten (D in m)."""
    rw = regelwerk()
    for art in ("fall", "stufe", "schnelle"):
        try:
            lo, hi = rw.art_bereich(art) if rw is not None else {"fall": (2.0, 1e9), "stufe": (0.8, 2.0),
                                                                    "schnelle": (0.15, 0.8)}[art]
        except Exception:        # noqa: BLE001
            lo, hi = {"fall": (2.0, 1e9), "stufe": (0.8, 2.0), "schnelle": (0.15, 0.8)}[art]
        if D >= lo:
            return art
    return "schnelle"


def fall_max():
    rw = regelwerk()
    try:
        return float(rw.hoehe_max_einzeln()) if rw is not None else 25.0
    except Exception:            # noqa: BLE001
        return 25.0


# ============================================================================================
# Querprofil (15b)
# ============================================================================================
def kantenabstand(B):
    half = 0.5 * float(B)
    return min(0.5, max(0.3, 0.3 * half))


def wasserkante(B, zelle_m):
    """Abstand Mitte -> Wasserkante (Gelaende = Spiegel): 0,3-0,5 m innerhalb der halben Breite (15b), aber mind.
    0,75 Zellen - sonst liegt die bilineare Mitte eines schmalen Bachs auf dem Ufer (Gelaende ueber dem Spiegel)."""
    return max(0.5 * float(B) - kantenabstand(B), 0.75 * float(zelle_m))


def halbe_breite_eff(B, zelle_m):
    return max(0.5 * float(B), wasserkante(B, zelle_m) + kantenabstand(B))


def ufer_abstand(B, zelle_m):
    """Pruefstelle 'Ufer' (A12): Netzrand (halbe Breite + 0,4 m); bei Baechen schmaler als das Raster dort, wo die
    Boeschung das Ufer sicher ueber den Spiegel bringt (Wasserkante + 0,3 m)."""
    return max(0.5 * float(B) + NETZRAND_M, wasserkante(B, zelle_m) + 0.3)


def profil(d, W, Wu, B, tiefe_m, zelle_m):
    """Ziel-Gelaende (nur absenken) und Uferring (nur anheben) im Abstand d von der Mittellinie.
    W = Spiegel an der Stelle, Wu = Oberwasser-Spiegel (Spiegel 1,5 m stromauf; Seitenwand neben dem Fuss einer
    Stufe). Rueckgabe (T_absenken, R_anheben, ring_maske)."""
    d = np.asarray(d, np.float64)
    wk = wasserkante(B, zelle_m)
    he = halbe_breite_eff(B, zelle_m)
    bett = W - max(float(tiefe_m), 0.03)
    boesch = W + (d - wk) * TAN_B
    innen = np.maximum(bett, boesch)
    aussen = np.maximum(boesch, np.maximum(Wu, W) + UFER_MIN_M + (d - he) * TAN_B)
    T = np.where(d <= he, innen, aussen)
    plateau = ufer_abstand(B, zelle_m) + RING_BREITE_M
    anstieg = np.minimum(np.maximum(d - wk, 0.0) * TAN_B, RING_UEBER_M)
    R = np.where(d < he, W, np.maximum(Wu, W)) + anstieg - np.maximum(d - plateau, 0.0) * RING_AUSLAUF
    ring = d >= wk
    return T, R, ring


def reichweite(B, zelle_m, tiefe_max_m):
    """Wie weit (m von der Mitte) das Profil wirken kann: Uferring + Auslauf, Boeschung bis zur groessten Eintiefung."""
    return halbe_breite_eff(B, zelle_m) + max(RING_BREITE_M + NETZRAND_M + WULST_MAX_M / RING_AUSLAUF + 0.5,
                                              min(tiefe_max_m / TAN_B + 1.0, 30.0))


# ============================================================================================
# Spiegel als Treppe (A8)
# ============================================================================================
def huelle(g, W0=None, e=EINBETTUNG_M):
    """Monotone Huellkurve: laufendes Minimum von (Gelaende - e), Start hoechstens W0."""
    M = np.minimum.accumulate(np.asarray(g, np.float64) - e)
    if W0 is not None:
        M = np.minimum(M, float(W0))
    return M


def treppe(s, g, B, W0=None, W_boden=None, W_ende=None, start_fest=False, boden_arr=None, flach_bis_m=0.0):
    """Wasserspiegel W(s) als Treppe aus Becken (<= 3 %, >= becken_laenge) und Stufen (Lippe -> Fuss STUFE_L_M).
    s: Bogenlaenge (aufsteigend, ~0,5 m), g: Gelaende entlang der Linie (nach den bisherigen Stempeln),
    W0: Startspiegel (Abfluss: Seespiegel; start_fest -> genau dieser Wert), W_boden: Spiegel nie darunter
    (Zielgewaesser + 2 cm), W_ende: Endpunkt genau auf diesen Wert (eigener See: Spiegel + 2 cm).
    boden_arr: Spiegel je Probe nie darunter (Furt: Gelaende + 3 cm; muss stromab nicht steigend sein).
    Rueckgabe (W, stufen) mit stufen = [(s_lippe, s_fuss, W_oben, W_unten)]."""
    s = np.asarray(s, np.float64)
    g = np.asarray(g, np.float64)
    n = len(s)
    M = huelle(g, W0)
    if boden_arr is not None:
        M = np.maximum(M, np.maximum.accumulate(np.asarray(boden_arr, np.float64)[::-1])[::-1])
    if start_fest and W0 is not None:
        M[0] = float(W0)
    sb = becken_gefaelle()
    W = np.empty(n)
    W[0] = M[0]
    stufen = []
    k = 1
    # lokales Gefaelle der Huelle (Fenster ~ klassen.fenster_lokal = clamp(2 B, 8, 20))
    fen = min(max(2.0 * B, 8.0), 20.0)
    while k < n:
        ds = s[k] - s[k - 1]
        if s[k] <= flach_bis_m:
            # Auslass eines Sees: Spiegel bleibt bis hinter die Lippe auf dem Seespiegel (keine Stufe in der Lippe)
            W[k] = W[k - 1]
            k += 1
            continue
        if M[k] >= W[k - 1] - sb * ds:
            # Huelle faellt flacher als das Becken: Spiegel folgt ihr (Riffel <= 3 %) bzw. bleibt flach darunter
            W[k] = min(W[k - 1], max(M[k], W[k - 1] - sb * ds))
            k += 1
            continue
        # Huelle faellt steiler: Stufe an der Lippe s[k-1]; neues Becken so tief, dass es becken_laenge weit unter
        # der Huelle bleibt (flach, die naechste Stufe folgt, wenn die Huelle es wieder unterschreitet)
        j1 = int(np.searchsorted(s, s[k - 1] + fen))
        S_lok = max((M[k - 1] - M[min(j1, n - 1)]) / max(s[min(j1, n - 1)] - s[k - 1], 1e-6), 0.0)
        Lb = becken_laenge(S_lok, B)
        j = int(np.searchsorted(s, s[k - 1] + STUFE_L_M + Lb, side="right"))
        j = min(max(j, k + 1), n)
        neu = float(M[k:j].min())
        if W_boden is not None:
            neu = max(neu, float(W_boden))
        D = W[k - 1] - neu
        if D < STUFE_MIN_M:
            W[k] = max(M[k], neu)
            W[k] = min(W[k], W[k - 1])
            k += 1
            continue
        # Fuss STUFE_L_M hinter der Lippe
        kf = int(np.searchsorted(s, s[k - 1] + STUFE_L_M - 1e-6))
        kf = min(max(kf, k), n - 1)
        for q in range(k, kf + 1):
            W[q] = neu
        stufen.append((float(s[k - 1]), float(s[kf]), float(W[k - 1]), float(neu)))
        k = kf + 1
    if W_boden is not None:
        W = np.maximum(W, float(W_boden))
        W = np.minimum.accumulate(W)
    if boden_arr is not None:
        W = np.maximum(W, np.maximum.accumulate(np.asarray(boden_arr, np.float64)[::-1])[::-1])
    if W_ende is not None and n > 1:
        we = float(W_ende)
        if W[-1] > we + STUFE_MIN_M:
            # letzte Stufe am Ende (z. B. vom Uferring des Sees auf den Seespiegel); eine Stufe, die schon in diesem
            # Stueck liegt, geht darin auf
            kl = int(np.searchsorted(s, s[-1] - STUFE_L_M))
            kl = min(max(kl, 0), n - 2)
            stufen = [e for e in stufen if e[1] <= s[kl] + 1e-6]
            stufen.append((float(s[kl]), float(s[-1]), float(W[kl]), we))
            W[kl + 1:] = we
        W[-1] = we
        W = np.maximum(W, we)
        W = np.minimum.accumulate(W)
    return W, stufen


def stufen_zusammenfassen(stufen, W_fn=None):
    """Stufen < STUFE_MIN_M fallen weg; Liste von dicts {s_lippe, s_fuss, oben, unten, fall_m, art}."""
    out = []
    for a, b, wo, wu in stufen:
        D = wo - wu
        if D < STUFE_MIN_M:
            continue
        out.append({"s_lippe": a, "s_fuss": b, "oben": wo, "unten": wu, "fall_m": D, "art": stufen_art(D)})
    return out


# ============================================================================================
# Linien
# ============================================================================================
def bogen(P):
    P = np.asarray(P, np.float64)[:, :2]
    seg = np.hypot(*np.diff(P, axis=0).T) if len(P) > 1 else np.zeros(0)
    return np.concatenate([[0.0], np.cumsum(seg)])


def punkt_bei(P, kum, sd):
    P = np.asarray(P, np.float64)[:, :2]
    sd = np.clip(np.asarray(sd, np.float64), 0.0, kum[-1])
    j = np.clip(np.searchsorted(kum, sd, side="right") - 1, 0, len(P) - 2)
    seg = np.maximum(kum[j + 1] - kum[j], 1e-9)
    f = (sd - kum[j]) / seg
    return P[j, 0] + (P[j + 1, 0] - P[j, 0]) * f, P[j, 1] + (P[j + 1, 1] - P[j, 1]) * f


def linien_stueck(P, a_m, b_m):
    """Teil der Polylinie zwischen den Bogenlaengen a_m und b_m (geklemmt) als Array n x 2."""
    P = np.asarray(P, np.float64)[:, :2]
    kum = bogen(P)
    a = float(np.clip(a_m, 0.0, kum[-1]))
    b = float(np.clip(b_m, a, kum[-1]))
    s = np.concatenate([[a], kum[(kum > a) & (kum < b)], [b]])
    x, y = punkt_bei(P, kum, s)
    return np.stack([x, y], 1)


def abtasten(P, schritt_m):
    """Gleichmaessige Proben entlang der Polylinie -> (s, x, y)."""
    kum = bogen(P)
    L = float(kum[-1])
    n = max(2, int(math.ceil(L / schritt_m)) + 1)
    s = np.linspace(0.0, L, n)
    x, y = punkt_bei(P, kum, s)
    return s, x, y


def schnitt_polygon(P, poly):
    """Erster Eintritt der Polylinie P in das Polygon poly -> (Segmentindex k, Punkt) oder None."""
    from .rezept import _in_polygon
    P = np.asarray(P, np.float64)[:, :2]
    Q = np.asarray(poly, np.float64)[:, :2]
    innen = _in_polygon(P[:, 0], P[:, 1], Q)
    if innen[0]:
        return 0, (float(P[0, 0]), float(P[0, 1]))
    for k in range(len(P) - 1):
        if not innen[k + 1]:
            continue
        a, b = P[k], P[k + 1]
        best = None
        for m in range(len(Q)):
            c, dd = Q[m], Q[(m + 1) % len(Q)]
            r, sv = b - a, dd - c
            den = r[0] * sv[1] - r[1] * sv[0]
            if abs(den) < 1e-12:
                continue
            t = ((c[0] - a[0]) * sv[1] - (c[1] - a[1]) * sv[0]) / den
            u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0 and (best is None or t < best):
                best = t
        if best is None:
            best = 1.0
        return k, (float(a[0] + (b[0] - a[0]) * best), float(a[1] + (b[1] - a[1]) * best))
    return None


def naechster_umrisspunkt(poly, x, y):
    Q = np.asarray(poly, np.float64)[:, :2]
    best, bp = 1e18, None
    for m in range(len(Q)):
        c, dd = Q[m], Q[(m + 1) % len(Q)]
        ab = dd - c
        t = float(np.clip(((x - c[0]) * ab[0] + (y - c[1]) * ab[1]) / max(float((ab ** 2).sum()), 1e-12), 0.0, 1.0))
        px, py = c[0] + t * ab[0], c[1] + t * ab[1]
        d = math.hypot(px - x, py - y)
        if d < best:
            best, bp = d, (float(px), float(py))
    return bp, best


def puffer_polygon(P, breite_m, n_kappe=6):
    """Umriss (gegen den Uhrzeigersinn) eines Bands der Breite breite_m um die Polylinie P (fuer Houdini-Masken)."""
    P = np.asarray(P, np.float64)[:, :2]
    if len(P) < 2:
        return []
    r = 0.5 * float(breite_m)
    links, rechts = [], []
    for k in range(len(P)):
        a = P[max(k - 1, 0)]
        b = P[min(k + 1, len(P) - 1)]
        t = b - a
        t = t / max(np.hypot(*t), 1e-9)
        n = np.array([t[1], -t[0]])
        links.append(P[k] + n * r)
        rechts.append(P[k] - n * r)
    poly = links + rechts[::-1]
    from .stempel import flaeche
    poly = [[float(p[0]), float(p[1])] for p in poly]
    if flaeche(poly) < 0:
        poly = poly[::-1]
    return poly


# ============================================================================================
# Epic-Gewaesser (A9: nur sie zaehlen als Muendung)
# ============================================================================================
class EpicZiele:
    """Epic-Gewaesser der Welt: Baeche (baeche_alle.json), Fluesse und Seen (wasser_welt.json), Teiche
    (teiche.json). Houdini-Wasser (karte_wasser) ist KEIN Ziel."""

    def __init__(self, welt):
        self.linien = []        # (id, art, P[n,2] m, z[n] m, breite[n] m, box)
        self.flaechen = []      # (id, art, poly[n,2] m, spiegel m, box)
        for b in welt.baeche or []:
            self._linie(b, "bach")
        for f in (welt.wasser_welt or {}).get("fluesse", []) or []:
            self._linie(f, "fluss")
        for s in (welt.wasser_welt or {}).get("seen", []) or []:
            self._flaeche(s, "see")
        for t in welt.teiche or []:
            self._flaeche(t, "teich")

    def _linie(self, b, art):
        q = b.get("punkte") or []
        if len(q) < 2 or not b.get("id"):
            return
        A = np.asarray([p[:4] if len(p) >= 4 else list(p[:3]) + [200.0] for p in q], np.float64)
        P = A[:, :2] / 100.0
        self.linien.append((b["id"], art, P, A[:, 2] / 100.0, A[:, 3] / 100.0,
                            (P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max())))

    def _flaeche(self, s, art):
        if not s.get("umriss") or len(s["umriss"]) < 3 or s.get("eis") or not s.get("id"):
            return
        P = np.asarray(s["umriss"], np.float64)[:, :2] / 100.0
        self.flaechen.append((s["id"], art, P, float(s.get("spiegel_cm", 0.0)) / 100.0,
                              (P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max())))

    def bei(self, x, y, r_m):
        """Naechstes Epic-Gewaesser, dessen Wasserflaeche naeher als r_m an (x, y) liegt -> dict(id, art,
        spiegel_m, abstand_m, punkt_m) oder None. Bei Linien zaehlt der Abstand zum Ufer (Mitte - halbe Breite)."""
        from .rezept import _in_polygon
        best = None
        for bid, art, P, z, br, (x0, y0, x1, y1) in self.linien:
            if x < x0 - r_m - 50 or x > x1 + r_m + 50 or y < y0 - r_m - 50 or y > y1 + r_m + 50:
                continue
            A, Bp = P[:-1], P[1:]
            AB = Bp - A
            L2 = np.maximum((AB ** 2).sum(1), 1e-12)
            t = np.clip(((x - A[:, 0]) * AB[:, 0] + (y - A[:, 1]) * AB[:, 1]) / L2, 0.0, 1.0)
            Q = A + AB * t[:, None]
            dd = np.hypot(Q[:, 0] - x, Q[:, 1] - y)
            k = int(np.argmin(dd))
            zz = float(z[k] + (z[k + 1] - z[k]) * t[k])
            bb = float(br[k] + (br[k + 1] - br[k]) * t[k])
            d = max(float(dd[k]) - 0.5 * bb, 0.0)
            if d <= r_m and (best is None or d < best["abstand_m"]):
                best = {"id": bid, "art": art, "spiegel_m": zz, "abstand_m": d,
                        "punkt_m": [float(Q[k, 0]), float(Q[k, 1])]}
        for sid, art, P, sp, (x0, y0, x1, y1) in self.flaechen:
            if x < x0 - r_m or x > x1 + r_m or y < y0 - r_m or y > y1 + r_m:
                continue
            if bool(_in_polygon(x, y, P)):
                d = 0.0
                q = [x, y]
            else:
                q, d = naechster_umrisspunkt(P, x, y)
            if d <= r_m and (best is None or d < best["abstand_m"]):
                best = {"id": sid, "art": art, "spiegel_m": sp, "abstand_m": d, "punkt_m": [float(q[0]), float(q[1])]}
        return best

    def spiegel(self, wid, x, y):
        """Spiegel (m) des Epic-Gewaessers wid an der Stelle (x, y) (Linie: Projektion) oder None."""
        for bid, art, P, z, br, _ in self.linien:
            if bid != wid:
                continue
            A, Bp = P[:-1], P[1:]
            AB = Bp - A
            L2 = np.maximum((AB ** 2).sum(1), 1e-12)
            t = np.clip(((x - A[:, 0]) * AB[:, 0] + (y - A[:, 1]) * AB[:, 1]) / L2, 0.0, 1.0)
            Q = A + AB * t[:, None]
            k = int(np.argmin(np.hypot(Q[:, 0] - x, Q[:, 1] - y)))
            return float(z[k] + (z[k + 1] - z[k]) * t[k])
        for sid, art, P, sp, _ in self.flaechen:
            if sid == wid:
                return sp
        return None

    def kennt(self, wid):
        return any(e[0] == wid for e in self.linien) or any(e[0] == wid for e in self.flaechen)


def epic_ziele(welt):
    z = getattr(welt, "_epic_ziele", None)
    if z is None:
        z = EpicZiele(welt)
        welt._epic_ziele = z
    return z
