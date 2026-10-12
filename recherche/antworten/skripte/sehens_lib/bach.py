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
     Spiegel + 0,2 m bis Netzrand + 1,5 m (hebt hoechstens 2 m; Koordinator 13f: Reserve, die Spiegelplanung
     rechnet unveraendert mit 0,15 m / 1 m); die letzte Zelle innen an der Wasserkante wird bis zur Boeschung
     aufgefuellt. Neben dem Fuss einer Stufe gilt 1,5 m lang der Oberwasser-Spiegel (Seitenwand des Falls).
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
RING_UEBER_M = 0.20                      # Uferring Spiegel + 0,2 m (15b/15e, Koordinator 13f: mit Reserve)
NETZRAND_M = 0.4                         # Netzrand = halbe Breite + 0,4 m (15b)
RING_BREITE_M = 1.5
RING_AUSLAUF = 0.5                       # 1:2
WULST_MAX_M = 2.0                        # Uferring hebt hoechstens 2 m (Koordinator 13f: Reserve)
# Spiegelplanung (Treppe, Stufen) rechnet weiter mit den Werten von 13f (Ring + 0,15 m, hebt <= 1 m): Ferat 13g -
# die Stufen bleiben genau wie in 13f; die Reserve wirkt nur im Stempel (Ufer hoeher, Spiegel und Stufen gleich)
PLAN_RING_UEBER_M = 0.15
PLAN_WULST_MAX_M = 1.0
EINBETTUNG_M = 0.30                      # Spiegel liegt so weit unter dem Gelaende (Huellkurve): Bach eingetieft
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
    du = ufer_abstand(B, zelle_m)
    plateau = du + RING_BREITE_M
    # Boeschung bis eine halbe Zelle hinter die Pruefstelle (Netzrand) durchgehend 35 Grad (konvexes Profil: die
    # bilineare Abfrage am Netzrand liegt dann nie unter dem Profil), danach Ring auf Spiegel + 0,15 ... 0,5 m
    r_max = max(RING_UEBER_M, min((du + 0.5 * float(zelle_m) - wk) * TAN_B, 0.5))
    anstieg = np.minimum(np.maximum(d - wk, 0.0) * TAN_B, r_max)
    R = np.where(d < he, W, np.maximum(Wu, W)) + anstieg - np.maximum(d - plateau, 0.0) * RING_AUSLAUF
    ring = d >= wk
    return T, R, ring


def absenk_grenze(d, B, tiefe_m, zelle_m):
    """13i K1: wie tief das Querprofil im Abstand d (m) von der Mitte hoechstens unter das bisherige Gelaende absenkt:
    innerhalb der Wasserkante (+ 0,5 Zellen) unbegrenzt (Bett), ausserhalb tiefe + 0,5 m bis Netzrand + Uferring (ufer_abstand +
    RING_BREITE_M), danach weich (2 m) auf 0 - die Boeschung laeuft in den Hang aus, statt ihn abzutragen."""
    d = np.asarray(d, np.float64)
    wk = wasserkante(B, zelle_m)
    rand = ufer_abstand(B, zelle_m) + RING_BREITE_M
    t = np.clip((d - rand) / 2.0, 0.0, 1.0)
    g = (float(tiefe_m) + 0.5) * (1.0 - t * t * (3.0 - 2.0 * t))
    # eine halbe Zelle Reserve: die bilineare Abfrage in der Bachmitte mischt die Zellen bis 0,7 Zellen daneben
    return np.where(d <= wk + 0.5 * float(zelle_m), np.inf, g)


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
        # 13i K5: Fuss an der Probe, die Lippe + STUFE_L_M am naechsten liegt (bei Proben < 0,5 m Abstand rutschte er
        # sonst eine Probe weiter -> Stufe 1 m lang, Becken danach nur 2,5 m); Lippe, Hoehe und Zahl bleiben
        kf = int(np.argmin(np.abs(s[k:min(k + 4, n)] - (s[k - 1] + STUFE_L_M)))) + k
        kf = min(max(kf, k), n - 1)
        # Spiegel wie 13f: bis zur bisherigen Fuss-Probe auf dem Unterwasser (Lage/Hoehe/Zahl der Stufen gleich)
        kf_alt = min(max(int(np.searchsorted(s, s[k - 1] + STUFE_L_M - 1e-6)), k), n - 1)
        kf = min(kf, kf_alt)
        for q in range(k, kf_alt + 1):
            W[q] = neu
        stufen.append((float(s[k - 1]), float(s[kf]), float(W[k - 1]), float(neu), float(s[kf_alt])))
        k = kf_alt + 1
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
            stufen = [e for e in stufen if e[4] <= s[kl] + 1e-6]
            if stufen and s[kl] - stufen[-1][1] < BECKEN_MIN_M - 1e-6:
                # 13i K5: davor bliebe < 3 m Becken - die Schluss-Stufe geht in der letzten Stufe auf (Lippe und Oberwasser
                # wie bisher, Fuss am Ende auf dem Zielspiegel)
                a_, b_, wo_, wu_, _ = stufen.pop()
                ka_ = int(np.clip(np.searchsorted(s, a_ - 1e-6), 0, n - 1))
                stufen.append((a_, float(s[-1]), wo_, we, float(s[-1])))
                W[ka_ + 1:] = we
            else:
                stufen.append((float(s[kl]), float(s[-1]), float(W[kl]), we, float(s[-1])))
                W[kl + 1:] = we
        W[-1] = we
        W = np.maximum(W, we)
        W = np.minimum.accumulate(W)
    # Stufen nach dem Anheben (Zielspiegel, Furten) aus dem endgueltigen W neu ablesen
    neu_st = []
    for a, b, wo, wu, b_alt in stufen:
        ka = int(np.clip(np.searchsorted(s, a - 1e-6), 0, n - 1))
        kb = int(np.clip(np.searchsorted(s, b - 1e-6), 0, n - 1))
        # Hoehe wie 13f an der bisherigen Fuss-Probe gemessen (13i K5: nur die Lage des Fusses ist korrigiert)
        kb_alt = int(np.clip(np.searchsorted(s, b_alt - 1e-6), 0, n - 1))
        if W[ka] - W[kb_alt] >= STUFE_MIN_M:
            neu_st.append((float(s[ka]), float(s[kb]), float(W[ka]), float(W[kb_alt])))
    stufen = neu_st
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


# ============================================================================================
# 13g: Wasserkoerper im A15/14b-Format (river + kaskadennetz) - Adapter auf gefaelle_plan.bauen_wasser_A
# ============================================================================================
STUFE_NETZ_MIN_M = 0.5          # 13g: Baeche mit Stufen ab 0,5 m Fall bekommen wasser_koerper
_GP = {"geladen": False, "mod": None}


def gefaelle_plan():
    """recherche/antworten/skripte/gefaelle/gefaelle_plan.py (Auftrag 15, nur importiert, nicht geaendert) oder None."""
    if _GP["geladen"]:
        return _GP["mod"]
    _GP["geladen"] = True
    pf = os.path.normpath(os.path.join(HIER, "..", "gefaelle", "gefaelle_plan.py"))
    try:
        spec = importlib.util.spec_from_file_location("_sehens_gefaelle_plan", pf)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _GP["mod"] = mod
    except Exception as ex:      # noqa: BLE001
        log("Hinweis: gefaelle_plan (Auftrag 15) nicht geladen (%s) - keine wasser_koerper" % ex)
        _GP["mod"] = None
    return _GP["mod"]


class _LaufProfil:
    """Minimal-Profil fuer gefaelle_plan.bauen_wasser_A: Bachlinie auf dem Planraster (0,5 m), z0 = geplanter Spiegel
    (die Stufen sind schon im Spiegel; 'alter Spiegel' = neuer -> River-Tempo aus v)."""

    def __init__(self, s, x, y, W, tiefe_m, v_cm_s):
        self.s = np.asarray(s, np.float64)
        self.x = np.asarray(x, np.float64)
        self.y = np.asarray(y, np.float64)
        tx, ty = np.gradient(self.x), np.gradient(self.y)
        n = np.maximum(np.hypot(tx, ty), 1e-9)
        self.tx, self.ty = tx / n, ty / n
        self.z0 = np.minimum.accumulate(np.asarray(W, np.float64))
        self.n = len(self.s)
        self.tiefe = np.full(self.n, float(tiefe_m))
        self.v = np.full(self.n, float(v_cm_s))

    def i(self, s):
        return int(np.clip(np.searchsorted(self.s, s - 1e-9), 0, self.n - 1))

    def xy(self, s):
        return float(np.interp(s, self.s, self.x)), float(np.interp(s, self.s, self.y))

    def tang(self, s):
        k = self.i(s)
        return float(self.tx[k]), float(self.ty[k])


def netz_breite(B, zelle_m):
    """Breite von River/Kaskadennetz (m): Bachbreite, mindestens die Wasserbreite im Gelaende (2 x Wasserkante),
    so dass der Netzrand (halbe Breite + 0,4 m) an der Uferpruefstelle des Querprofils liegt (ufer_abstand)."""
    return max(float(B), 2.0 * (ufer_abstand(B, zelle_m) - 0.4))


def bett_min(tiefe_m):
    """Bett-Regel der Netze (A15: >= 0,2 m unter dem Spiegel) fuer das unveraenderte 13f-Querprofil (Bett = Spiegel -
    tiefe_cm, Wasserkante innen, 35-Grad-Boeschung): tiefster Bettpunkt >= min(0,2 m; halbe Rezepttiefe)."""
    return round(min(0.2, 0.5 * float(tiefe_m)), 3)


# ============================================================================================
# 13k: Schaum der Sehens-Treppenbaeche (Pilot 2: 78-86 % der quer-Eintraege Schaum > 0,5, Deckung ueberall 1)
# ============================================================================================
# Die 15g-Logik (quer_ergaenzen: Querpunkte, smoothstep-Kanten, Rauschen, Deckung zum Ufer, Lipschitz-Huelle) wird
# wiederverwendet - mit Sehens-Parametern (eigene Kopie des Regelwerks, C2/A15 unveraendert) und einer Kerbe in
# Strahlbreite statt ueber die ganze Lippe. Danach begrenzt eine Laengshuelle den Schaum: Becken/Gumpen <= 0,2,
# Lippensaum <= 0,5, Fallflaeche <= 0,45 (Fall-Optik macht das Material), Fallfuss Spitze 0,65-0,85 und Abklingen ueber
# 2-4 m; Schnellen <= 0,45. Treppe, Querprofil und Effekt-Positionen bleiben wie 13f (nur Schaum/Deckung/Tiefe).
SCHAUM_SEHENS = {"saum_m": 0.3, "oben_m": 0.3, "saum_seite": 0.05, "zunge_seite": 0.08, "aufprall_anteil_max": 0.15,
                 "aus_unten_anteil": 0.5, "aus_unten_m": [2.0, 4.0]}
SCHAUM_HUELLE = {"becken": 0.2, "saum": 0.5, "saum_m": 0.8, "fall": 0.45, "rampe": 0.45, "fuss_spitze": [0.65, 0.85],
                 "fuss_kern_m": 0.2, "abklingen_m": [2.0, 4.0], "abklingen_exp": 4.0}
STRAHL_SEITE_DECKUNG = 0.3      # Deckung neben dem Strahl auf Zunge/Fallflaeche (duenner Film, Fels scheint durch)
G_ERDE = 9.81


def _rw_sehens(rw, tiefe_m):
    """Kopie des Regelwerks mit den Sehens-Schaumparametern (das Original fuer A15/C2 bleibt unberuehrt)."""
    import copy
    r2 = copy.deepcopy(rw.r)
    u = r2.setdefault("stufen", {}).setdefault("unregelmaessig", {})
    sch = dict(u.get("schaum") or {})
    sch.update(SCHAUM_SEHENS)
    u["schaum"] = sch
    du = dict(u.get("deckung_ufer") or {})
    # Deckung zum Ufer weich wie 15g, Vollwert ab 80 % der Rezepttiefe (Sehensbaeche sind 8-30 cm tief, C2 bis 4 m)
    du["tiefe_m"] = float(np.clip(0.8 * float(tiefe_m), 0.1, 0.6))
    u["deckung_ufer"] = du
    return type(rw)(r2, getattr(rw, "pfad", ""))


def lippen_strahl(xl, yl, tx, ty, oben, br, boden_fn, v_m_s, tiefe_m, B_rezept=None):
    """13k: Strahlbreite an einer Lippe aus Abfluss und Querprofil. Querschnitt 0,3 m oberhalb der Lippe auf dem
    gestempelten Gelaende (Bett), Wasserspiegel = Oberwasser. Abfluss Q = A(Becken) x v (A15-Beckentempo); an der
    Lippe stellt sich die kritische Tiefe ein (Q^2 T / (g A^3) = 1); der Strahl ist die Wasserspiegelbreite T_c bei
    kritischer Tiefe im selben Querprofil. Rueckgabe dict (strahl_breite_m, u_mitte_m, abfluss_m3_s, krit_tiefe_m,
    wasserbreite_m, lippe_breite_m) oder None."""
    h = br / 2.0 + NETZRAND_M
    u = np.arange(-h, h + 1e-6, 0.05)
    z = np.asarray(boden_fn(xl + ty * u, yl - tx * u), np.float64)
    quelle = "gelaende"
    k0 = int(np.argmin(z)) if np.isfinite(z).all() else 0
    zmin = float(z[k0]) if np.isfinite(z).all() else float("nan")
    if not (np.isfinite(z).all() and 0.5 * tiefe_m - 0.02 <= oben - zmin <= 1.5 * tiefe_m + 0.05):
        # Bett an der Lippe im Raster nicht sauber aufgeloest (2 m: die Fallkante verschmiert ins Unterwasser) -
        # 13f-Querprofil selbst: Bett = Spiegel - Tiefe zwischen den Wasserkanten, 35-Grad-Boeschung
        wk = (float(B_rezept) if B_rezept else br) / 2.0     # Rezeptbreite (das 2-m-Netz ist kuenstlich breiter)
        b0 = max(wk - tiefe_m / TAN_B, 0.1)
        z = np.where(np.abs(u) <= b0, oben - tiefe_m, oben - tiefe_m + (np.abs(u) - b0) * TAN_B)
        k0 = int(np.argmin(np.abs(u)))
        zmin = float(z[k0])
        quelle = "querprofil_13f"
    du = 0.05

    def flaeche(hh):
        nass = z < zmin + hh
        # zusammenhaengend um den tiefsten Punkt
        lo = k0
        while lo > 0 and nass[lo - 1]:
            lo -= 1
        hi = k0
        while hi < len(z) - 1 and nass[hi + 1]:
            hi += 1
        seg = slice(lo, hi + 1)
        A = float(np.sum(np.maximum(zmin + hh - z[seg], 0.0)) * du)
        return A, float((hi - lo + 1) * du), float(0.5 * (u[lo] + u[hi]))
    H = float(oben - zmin)
    A_b, T_b, _ = flaeche(H)
    Q = A_b * float(v_m_s)
    if Q <= 0.0 or A_b <= 0.0:
        return None
    f = lambda hh: Q * Q * flaeche(hh)[1] / (G_ERDE * max(flaeche(hh)[0], 1e-9) ** 3) - 1.0   # noqa: E731
    if f(H) > 0.0:
        hc = H                                        # schon im Becken schiessend (Froude >= 1): Strahl = Spiegel
    else:
        a, b = 0.002, H
        for _ in range(40):
            m = 0.5 * (a + b)
            if f(m) > 0.0:
                a = m
            else:
                b = m
        hc = 0.5 * (a + b)
    A_c, T_c, u_c = flaeche(hc)
    T_c = float(np.clip(T_c, 0.3, T_b))
    return {"strahl_breite_m": round(T_c, 2), "u_mitte_m": round(u_c, 2), "abfluss_m3_s": round(Q, 3),
            "krit_tiefe_m": round(hc, 3), "wasserbreite_m": round(T_b, 2), "lippe_breite_m": round(2.0 * h, 2),
            "querschnitt": quelle}


def schaum_huelle(S, lips):
    """13k: Laengshuelle c(s) fuer den Schaum (siehe SCHAUM_HUELLE). lips: [(s_lippe, s_fuss, D, art, s_naechste)]."""
    SH = SCHAUM_HUELLE
    S = np.asarray(S, np.float64)
    c = np.full(S.shape, SH["becken"])

    def glatt(t_):
        t_ = np.clip(t_, 0.0, 1.0)
        return t_ * t_ * (3.0 - 2.0 * t_)
    for s_l, s_f, D, art, s_n in lips:
        # Lippensaum: Anstieg ueber saum_m bis zur Lippe, danach in 0,3 m auf den Fallwert
        r = S - s_l
        saum = np.where(r <= 0.0, glatt((r + SH["saum_m"]) / SH["saum_m"]), 1.0 - glatt(r / 0.3))
        c = np.maximum(c, SH["becken"] + (SH["saum"] - SH["becken"]) * saum)
        if art == "schnelle":
            c = np.where((S > s_l) & (S <= s_f), np.maximum(c, SH["rampe"]), c)
            continue
        c = np.where((S > s_l) & (S < s_f), np.maximum(c, SH["fall"]), c)
        # Fallfuss: Spitze, dann Abklingen ueber 2-4 m (nie ueber 70 % des Beckens bis zur naechsten Lippe)
        P = float(np.clip(0.55 + 0.1 * D, *SH["fuss_spitze"]))
        A = float(np.clip(1.0 + 0.5 * D, *SH["abklingen_m"]))
        L_b = max(s_n - s_f, 1.0)
        A = min(A, max(0.7 * L_b, 1.0))
        x = S - s_f
        kern = SH["fuss_kern_m"]
        # Abklingen (1 - smoothstep)^4: steil am Anfang, nach A genau auf dem Beckenwert
        fu = np.where(x < -0.05, 0.0, np.where(x <= kern, P, SH["becken"] + (P - SH["becken"]) *
                                                 (1.0 - glatt((x - kern) / A)) ** SH["abklingen_exp"]))
        c = np.maximum(c, fu)
    return c


def schaum_kennzahlen(kb):
    """Anteil der quer-Eintraege mit Schaum > 0,5 / > 0,2, Becken-Maximum (Beckenpunkte ausserhalb Saum/Abklingen)."""
    Q = np.asarray(kb.get("quer") or [], np.float64)
    if Q.ndim != 3:
        return {}
    sc = Q[:, :, 2]
    return {"schaum_ueber_05": round(float((sc > 0.5).mean()), 3), "schaum_ueber_02": round(float((sc > 0.2).mean()), 3),
            "deckung_1": round(float((Q[:, :, 1] >= 0.999).mean()), 3)}


def wasser_koerper(lauf_id, s, x, y, W, stufen, B, tiefe_m, boden_fn, alt_fn, zelle_m, melde, niagara_frei=8):
    """13g: river + kaskadennetz (A15/14b Variante A) aus der fertigen 13f-Treppe - die Stufen werden NICHT neu
    geplant: Lippe/Fuss/Spiegel kommen unveraendert aus 'stufen' (s_lippe, s_fuss, oben, unten, fall_m, art) und W(s).
    Kaskadennetz je zusammenhaengender Stufenstrecke (Stufen >= 0,5 m), River >= 15 m dazwischen, kuerzere als Rampe
    im Netz (15c), Ueberlappung 0,5 m, Netz 2 cm unter dem River. Effekte nach A15 2.9: NS_Impact_Small (Cull 20 m)
    je Stufe >= 1 m, hoechstens niagara_frei; Vorhang nur an einem Einzelabsturz >= 3 m.
    Rueckgabe (koerper, effekte) oder (None, []) ohne Stufe >= 0,5 m."""
    gp = gefaelle_plan()
    if gp is None:
        return None, []
    st_netz = [e for e in stufen if e["fall_m"] >= STUFE_NETZ_MIN_M]
    if not st_netz:
        return None, []
    s = np.asarray(s, np.float64)
    W = np.minimum.accumulate(np.asarray(W, np.float64))
    x, y = np.asarray(x, np.float64), np.asarray(y, np.float64)
    # A15 legt das Ende des Ueberfallbogens und den Wandpunkt auf dasselbe s (Lippe + bogen_x_m); der Fuss muss
    # dahinter liegen, sonst stehen drei Punkte mit gleichem s und verschiedener Wasserhoehe im Netz (Pruefregel
    # 15f-Nachtrag 099f902). Liegt der 13f-Fuss naeher an der Lippe (Schluss-Stufe am Laufende), setzt NUR das Netz
    # seinen Fusspunkt auf Lippe + bogen_x_m + 5 cm; die Stufe (Treppe, 'stufen', Spiegel) bleibt wie 13f. Am Laufende
    # wird die Bachlinie dafuer geradeaus verlaengert (das Netz ragt dann bis 5 cm ins Muendungsbecken).
    bx = float(getattr(gp, "KN", {}).get("bogen_x_m", 0.45)) + 0.05
    fuss_netz = [max(float(e["s_fuss"]), float(e["s_lippe"]) + bx) if e["art"] != "schnelle" else float(e["s_fuss"])
                 for e in stufen]
    ueber = max(fuss_netz + [float(s[-1])]) - float(s[-1])
    if ueber > 1e-6 and len(s) >= 2:
        dx, dy = x[-1] - x[-2], y[-1] - y[-2]
        n_ = max(math.hypot(dx, dy), 1e-9)
        s = np.append(s, s[-1] + ueber)
        x = np.append(x, x[-1] + dx / n_ * ueber)
        y = np.append(y, y[-1] + dy / n_ * ueber)
        W = np.append(W, W[-1])
    pr = _LaufProfil(s, x, y, W, tiefe_m, gp.TEIL["velocity_becken_cm_s"])
    L = float(s[-1])
    # Spiegelpunkte (s, z, Rolle): Lippe/Fuss exakt aus den Stufen, dazwischen der geplante Spiegel alle ~2 m
    sp = [(0.0, float(W[0]), "becken")]
    spannen = []
    for e, sf in zip(stufen, fuss_netz):
        sp.append((float(e["s_lippe"]), float(e["oben"]), "lippe"))
        sp.append((sf, float(e["unten"]), "rampe" if e["art"] == "schnelle" else "fuss"))
        spannen.append((float(e["s_lippe"]), sf))
    for s_ in np.arange(2.0, L - 0.5, 2.0):
        if any(a - 0.3 <= s_ <= b + 0.3 for a, b in spannen):
            continue
        sp.append((float(s_), float(np.interp(s_, s, W)), "becken"))
    sp.append((L, float(W[-1]), "becken"))
    sp.sort(key=lambda t: (t[0], -t[1]))
    sp2 = []
    for t in sp:
        if sp2 and abs(t[0] - sp2[-1][0]) < 1e-4:
            if t[2] in ("lippe", "fuss", "rampe"):
                sp2[-1] = (t[0], min(t[1], sp2[-1][1]), t[2])
            continue
        sp2.append(t)
    zs = np.minimum.accumulate([t[1] for t in sp2])
    sp = [(t[0], float(z), t[2]) for t, z in zip(sp2, zs)]
    # Stufen im A15-Format; Segmente nur aus Stufen >= 0,5 m (kn_bereiche fasst Luecken < 15 m zu Rampen zusammen)
    st15 = []
    for k, (e, sf) in enumerate(zip(stufen, fuss_netz)):
        st15.append({"id": "%s_S%02d" % (lauf_id, k), "p": float(e["s_lippe"]),
                     "l": max(sf - float(e["s_lippe"]), 0.01), "D": float(e["fall_m"]),
                     "art": e["art"], "u": float(e["oben"]), "d": float(e["unten"]), "kolk": {"x_strahl": 0.0}})
    netz_ids = {st15[k]["id"] for k, e in enumerate(stufen) if e["fall_m"] >= STUFE_NETZ_MIN_M}
    segmente = [(e["p"], e["p"] + e["l"]) for e in st15 if e["id"] in netz_ids]
    st_in = [e for e in st15 if e["id"] in netz_ids]
    # Netzbreite = Wasserbreite im Gelaende (A12: Wasserkante mind. 0,75 Zellen von der Mitte) -> der Netzrand
    # (halbe Breite + 0,4 m) liegt an der Uferpruefstelle des Querprofils; Bett-Regel mit der Rezepttiefe, wenn der Bach
    # flacher als 0,2 m ist (Querprofil bleibt wie 13f)
    br = netz_breite(B, zelle_m)
    alt_z = gp._ZELLE[0]
    gp._ZELLE[0] = float(zelle_m)

    def melde_netz(st, txt):
        # die Bett-Regel prueft sehens_pruefen am tiefsten Bettpunkt (13f-Querprofil: Wasserkante innen, 35-Grad-
        # Boeschung - der A15-Mittelwert ueber 60 % der Breite misst dort die Boeschung mit)
        if "Bett an" in txt:
            return
        if "Ufer am Netzrand" in txt:
            # Pruefer (sehens_pruefen.pruefe_wasser_koerper) prueft mit den A12-Ausnahmen (Furten, Muendung, Seen)
            melde("HINWEIS", txt)
            return
        melde(st, txt)
    # 13j / 15f: Querprofil 'quer' (11 Stuetzpunkte dz_cm, deckung, schaum, tiefe_cm) - mit GERADEN Lippen
    # (Ferat: Stufen wie 13f, keine Lippen-Unregelmaessigkeit): Winkel 0, kein Pfeil, eine Kerbe ueber die ganze Breite
    # -> dz 0, Deckung 1, Schaum nur am Lippensaum und in Zunge/Aufprall, tiefe_cm aus dem gestempelten Bett
    lf = None
    rw = regelwerk()
    strahl = {}
    v_becken = float(gp.KN["tempo"]["becken"]) / 100.0
    for e in st_in:
        xl, yl = pr.xy(max(e["p"] - 0.3, 0.0))
        tx_, ty_ = pr.tang(e["p"])
        strahl[e["id"]] = lippen_strahl(xl, yl, tx_, ty_, float(e["u"]), br, boden_fn, v_becken, float(tiefe_m), float(B))
    if rw is not None and hasattr(gp, "LippenFeld") and hasattr(gp, "quer_ergaenzen"):
        rw = _rw_sehens(rw, tiefe_m)
        for e in st_in:
            e["B"] = br
            sb = strahl.get(e["id"])
            # 13k: Kerbe = Strahlbreite (Abfluss/Querprofil der Lippe) statt der ganzen Lippe; Krone bleibt gerade
            # (Tiefe 0: dz und Querprofil wie 13f), daneben duenner Film (Deckung 0,3)
            kerbe = (float(sb["u_mitte_m"]), float(sb["strahl_breite_m"]), 0.0) if sb else \
                (0.0, br + 2.0 * gp.KN["rand_ueberstand_m"], 0.0)
            e["geo"] = {"winkel_grad": 0.0, "tan": 0.0, "pfeil": 0.0, "h": max(br / 2.0, 0.5),
                        "kerben": [kerbe], "seite_deckung": STRAHL_SEITE_DECKUNG if sb else 1.0,
                        "skala": 1.0, "gerade": True}
        lf = gp.LippenFeld(st_in, segmente)
    try:
        koerper = gp.bauen_wasser_A(pr, sp, st_in, segmente, lambda s_: br, lauf_id,
                                    lambda xx, yy: np.asarray(boden_fn(xx, yy), np.float64), melde_netz, (),
                                    lambda xx, yy: np.asarray(alt_fn(xx, yy), np.float64), lf=lf, rw=rw)
    finally:
        gp._ZELLE[0] = alt_z
    # 13k: Laengshuelle des Schaums (Becken <= 0,2, Fallfuss mit Abklingen 2-4 m, Fallflaechen <= 0,45)
    lips_all = sorted((float(e["p"]), float(e["p"] + e["l"]), float(e["D"]), e["art"]) for e in st_in)
    for kb in koerper:
        if kb["typ"] != "kaskadennetz" or kb.get("quer") is None:
            continue
        S = np.asarray(kb["mittellinie_s_m"], np.float64)
        lips = [(a_, b_, d_, art_, lips_all[i + 1][0] if i + 1 < len(lips_all) else b_ + 6.0)
                for i, (a_, b_, d_, art_) in enumerate(lips_all)]
        c = schaum_huelle(S, lips)
        F = np.asarray([[q_[2] for q_ in r_] for r_ in kb["quer"]], np.float64)
        F = np.minimum(F, c[:, None])
        F = gp.schaum_weich(F, S, unreg_sch(gp, rw)) if hasattr(gp, "schaum_weich") else F
        for k_, r_ in enumerate(kb["quer"]):
            for j_, q_ in enumerate(r_):
                q_[2] = round(float(F[k_, j_]), 2)
            kb["mittellinie"][k_][6] = round(float(F[k_, len(r_) // 2]), 2)
        kb["schaum_regel"] = ("13k Sehens: Schaum nur in Strahlbreite (strahl_breite_m je Stufe); Becken/Gumpen <= %.1f, "
                              "Lippensaum <= %.2f, Fallflaeche <= %.2f (Fall-Optik macht das Material), Fallfuss Spitze "
                              "0,65-0,85 und Abklingen ueber 2-4 m (<= 70 %% des Beckens), Schnellen <= %.2f; weiche Kanten "
                              "wie 15g (smoothstep, Rauschen, Sprung <= 0,45)"
                              % (SCHAUM_HUELLE["becken"], SCHAUM_HUELLE["saum"], SCHAUM_HUELLE["fall"], SCHAUM_HUELLE["rampe"]))
        kb["stufen_strahl"] = [dict({"stufe": e["id"], "fall_m": round(float(e["D"]), 2)}, **(strahl.get(e["id"]) or {}))
                               for e in st_in if e["id"] in kb["stufen"]]
        kb["schaum_kennzahlen"] = schaum_kennzahlen(kb)
        mp = kb.get("material_parameter")
        if isinstance(mp, dict) and "SLW_Absorption_pro_m" in mp:
            # 13k (Ferat, Nachtrag 12:35, Test UE 5.8): der SLW-Knoten rechnet die Koeffizienten je cm. Die Werte hier
            # bleiben je m (unveraendert), dazu Einheit, Skalierung und die je-cm-Werte ausdruecklich
            mp["einheit"] = "je_m"
            mp["skalierung_ue"] = 0.01
            mp["SLW_Absorption_pro_cm"] = [round(v * 0.01, 5) for v in mp["SLW_Absorption_pro_m"]]
            mp["SLW_Streuung_pro_cm"] = [round(v * 0.01, 5) for v in mp.get("SLW_Streuung_pro_m", [])]
            mp["einheit_hinweis"] = ("SLW_*_pro_m sind Koeffizienten je Meter (Beer-Lambert); UE 5.8 rechnet je cm -> "
                                     "x skalierung_ue (0,01) bzw. direkt SLW_*_pro_cm eintragen (Ferat-Test 13k: x 1,0 "
                                     "leuchtet 20-30 cm tiefes Wasser tuerkis, x 0,01 klar). Nicht verwechseln mit "
                                     "wasserfarben.json 'absorption' = Absorptionslaenge in cm (1/Wert je cm)")
    for kb in koerper:
        kb["breite_bach_m"] = round(float(B), 2)
        if kb.get("quer") is not None and lf is not None:
            # dz_cm nach A15-Konvention (15f-Nachtrag 099f902): relativ zu z_cm des eigenen Punkts; die absolute
            # Wasserhoehe z + dz ist bei gleichem s identisch (Lippe/Bogen/Wand/Fuss)
            kb["lippen"] = "gerade (Sehens-Stufen wie 13f, keine Unregelmaessigkeit aus 15f)"
        if kb["typ"] == "kaskadennetz":
            kb["pruefung"]["bett_unter_spiegel_min_m"] = bett_min(tiefe_m)
            kb["pruefung"]["bett_messung"] = "tiefster Bettpunkt quer (13f-Querprofil), Regel min(0,2 m; halbe Tiefe)"
            kb["pruefung"].pop("bett_zu_flach", None)
    # Effekte (A15 2.9): NS_Impact_Small am Fuss jeder Stufe >= 1 m, Cull 20 m, groesste zuerst, hoechstens niagara_frei
    effekte = []
    hoch = sorted([e for e in st_in if e["D"] >= gp.NIAGARA["D_min_m"]], key=lambda e: -e["D"])
    for e in hoch[:max(int(niagara_frei), 0)]:
        fx, fy = pr.xy(e["p"] + e["l"])
        fe = {"typ": "niagara", "asset": gp.NIAGARA["zusatz_system"], "stufe": e["id"],
              "pos_cm": [round(fx * 100), round(fy * 100), round(e["d"] * 100)],
              "cull_m": gp.NIAGARA["zusatz_cull_m"], "zweck": "Aufprall am Fuss (A15 2.9)"}
        if e["D"] >= VORHANG_CULL["ab_m"]:
            # 13k: an Stufen >= 3 m ist NS_Impact_Small aus 30 m und mehr sonst unsichtbar -> Cull 60-80 m
            fe["cull_m"] = cull_vorhang(e["D"])
            fe["cull_grund"] = "13k: Stufe >= 3 m - Aufprall aus der Ferne sichtbar (60 m bei 3 m, 80 m ab 10 m Fall)"
        sb = strahl.get(e["id"])
        if sb:
            fe["strahl_breite_m"] = sb["strahl_breite_m"]
        effekte.append(fe)
    if len(hoch) > len(effekte):
        melde("HINWEIS", "%s: %d Stufen >= 1 m ohne NS_Impact_Small (Niagara-Grenze %d gleichzeitig)"
              % (lauf_id, len(hoch) - len(effekte), gp.NIAGARA["gleichzeitig_hart"]))
    for kb in koerper:
        if kb["typ"] == "kaskadennetz":
            kb["effekte"] = [f for f in effekte if f["stufe"] in kb["stufen"]]
            # 13k: Vorhaenge (Stufen >= 3 m) mit Strahlbreite, wenn das Wasser nur einen Teil der Lippe nutzt
            kb["vorhang"] = [dict({"stufe": sid}, **{k_: v_ for k_, v_ in (strahl.get(sid) or {}).items()})
                             for sid in kb.get("vorhang_an_stufen") or []]
    return koerper, effekte


VORHANG_CULL = {"ab_m": 3.0, "min_m": 60.0, "max_m": 80.0, "max_ab_m": 10.0}


def cull_vorhang(D):
    """13k: Cull der Aufprall-Effekte an Stufen >= 3 m: 60 m bei 3 m Fall, linear bis 80 m ab 10 m Fall."""
    v = VORHANG_CULL
    f = (float(D) - v["ab_m"]) / max(v["max_ab_m"] - v["ab_m"], 1e-6)
    return round(float(np.clip(v["min_m"] + f * (v["max_m"] - v["min_m"]), v["min_m"], v["max_m"])), 1)


def unreg_sch(gp, rw):
    """Sprung-Grenze der 15g-Lipschitz-Huelle aus dem Regelwerk (Standard 0,45)."""
    try:
        return float(gp.unreg(rw)["schaum"].get("sprung_max", 0.45))
    except Exception:            # noqa: BLE001
        return 0.45
