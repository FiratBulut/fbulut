"""kandidaten.py - Kandidatensuche je Biom, Merkmale, Abstandsauswahl, Erreichbarkeit.

Regeln (Auftrag 13): 80-300 m von Wegen, nie in Orten, >= 150 m vom Rand geplanter Staedte, >= 350 m
zueinander (kleine Biome 200 m), im Biom-Inneren (kleine Biome: bis 150 m ueber die Grenze).

API:
  maske = filter_maske(welt, gel, biom, weg_min_m=80, weg_max_m=300, stadt_min_m=150, ort_min_m=30,
                       innen_min_m=None, wasser_ok=False, max_neigung=None, zusatz=None)
  liste = kandidaten(welt, gel, biom, score, n=10, abstand_m=None, maske=None, belegt=None, raster_m=10)
  m = merkmale(welt, gel, x_m, y_m, radius_m=40)          # dict fuer Begruendung/Scoring
  e = erreichbarkeit(welt, gel, x_m, y_m, max_grad=25)    # Fussweg vom naechsten Weg (Dijkstra, 4-m-Raster)
  Score-Hilfen: norm(a, lo, hi), glocke(a, mitte, breite), score_praegnanz(welt, gel), score_mulde(welt, gel),
               score_kante(welt, gel)  (Signatur (welt, gel) -> Array, direkt als score= nutzbar)
"""

import heapq

import numpy as np

from . import log
from . import daten as _daten
from . import gelaende as _gel


# ============================================================================================
# Filter
# ============================================================================================
def filter_maske(welt, gel, biom, weg_min_m=80.0, weg_max_m=300.0, stadt_min_m=150.0, ort_min_m=30.0,
                 innen_min_m=None, wasser_ok=False, meer_ok=False, max_neigung=None, zusatz=None):
    """bool-Raster der erlaubten Ortsmitten.

    innen_min_m: Mindestabstand zur Biomgrenze (> 0 innen). Standard: 30 m (grosse Biome),
                 -150 m fuer kleine Biome (Mitte darf bis 150 m ueber die Grenze).
    wasser_ok:   Mitte darf auf Suesswasser liegen (Quelltopf, Wasserfall im Bach ...).
    zusatz:      optionale bool-Maske (UND).
    """
    if innen_min_m is None:
        innen_min_m = -150.0 if _daten.ist_kleines_biom(biom) else 30.0
    m = gel.biom_abstand(biom) >= innen_min_m   # biom_abstand reicht 400 m nach aussen
    dw = gel.abstand_weg
    m &= (dw >= weg_min_m) & (dw <= weg_max_m)
    m &= welt.ort == 0
    m &= gel.abstand_ort >= ort_min_m
    m &= gel.abstand_stadt >= stadt_min_m
    if not meer_ok:
        m &= ~welt.meer
    if not wasser_ok:
        m &= welt.wasser == 0
    if max_neigung is not None:
        m &= gel.neigung <= max_neigung
    if zusatz is not None:
        m &= zusatz
    return m


# ============================================================================================
# Score-Hilfen
# ============================================================================================
def norm(a, lo, hi):
    """Linear auf 0..1 (gekappt)."""
    return np.clip((a - lo) / float(hi - lo), 0.0, 1.0).astype(np.float32)


def glocke(a, mitte, breite):
    """Gauss-Glocke 0..1 um mitte."""
    return np.exp(-0.5 * ((a - mitte) / float(breite)) ** 2).astype(np.float32)


def score_praegnanz(welt, gel, r_m=50):
    """Hohe, frei stehende Formen (Leuchtfeuer): TPI positiv + Steilheit."""
    return (norm(gel.tpi(r_m), 0, 15) * 0.7 + norm(gel.neigung, 10, 45) * 0.3).astype(np.float32)


def score_mulde(welt, gel, r_m=50):
    """Verborgene Mulden/Kessel (Fundstuecke): TPI negativ + maessig steil umrahmt."""
    return (norm(-gel.tpi(r_m), 0, 10) * 0.7 + norm(gel.senkentiefe, 0, 4) * 0.3).astype(np.float32)


def score_kante(welt, gel, sigma_m=10):
    """Gelaendestufen/Abbruchkanten (Wasserfall, Klippe): steil + profilkonvex."""
    p, _ = gel.kruemmung(sigma_m)
    return (norm(gel.neigung, 25, 55) * 0.6 + norm(p, 0, 0.05) * 0.4).astype(np.float32)


# ============================================================================================
# Merkmale
# ============================================================================================
def merkmale(welt, gel, x_m, y_m, radius_m=40.0, biom=None):
    """Kennzahlen eines Punkts (fuer Begruendung und Scoring). biom: Bezug fuer biom_abstand_m."""
    i, j = welt.m_zu_ij(x_m, y_m)
    fe = welt.fenster(x_m, y_m, radius_m)
    X, Y = fe.gitter_m()
    kreis = np.hypot(X - x_m, Y - y_m) <= radius_m
    h = fe.get("hoehe")[kreis]
    bo = fe.get("boden")[kreis]
    werte, anz = np.unique(bo, return_counts=True)
    o = np.argsort(-anz)
    boden_ant = {_daten.boden_name(werte[k]): round(float(anz[k]) / bo.size, 2) for k in o[:4]}
    acc = fe.get(gel.akkumulation)[kreis]
    b4 = fe.get("baeume_nativ")[kreis]
    bh = fe.get("baumhoehe_nativ")[kreis]
    nw = gel.weg_naechst[i, j]
    wx, wy = welt.flat_zu_m(nw) if nw >= 0 else (None, None)
    lf = int(gel.landformen()[i, j])
    sd, st = gel.stadt_abstand_punkt(x_m, y_m)
    return {
        "x_m": round(float(x_m), 1), "y_m": round(float(y_m), 1),
        "x_cm": int(round(x_m * 100)), "y_cm": int(round(y_m * 100)),
        "z_m": round(float(welt.hoehe[i, j]), 2), "feld": _daten.feld_von_m(x_m, y_m),
        "biom": _daten.biom_name(welt.biom[i, j]), "boden": _daten.boden_name(welt.boden[i, j]),
        "boden_anteile": boden_ant,
        "neigung_grad": round(float(gel.neigung[i, j]), 1),
        "neigung_max_grad": round(float(fe.get(gel.neigung)[kreis].max()), 1),
        "exposition_grad": round(float(gel.exposition[i, j]), 0),
        "tpi25_m": round(float(gel.tpi(25)[i, j]), 2), "tpi100_m": round(float(gel.tpi(100)[i, j]), 2),
        "relief_m": round(float(h.max() - h.min()), 1),
        "landform": _gel.LANDFORMEN.get(lf, "?"),
        "einzugsflaeche_max_m2": round(float(acc.max()), 0),
        "senkentiefe_m": round(float(gel.senkentiefe[i, j]), 2),
        "abstand_weg_m": round(float(gel.abstand_weg[i, j]), 1),
        "naechster_weg_m": [round(float(wx), 1), round(float(wy), 1)] if wx is not None else None,
        "abstand_wasser_m": round(float(gel.abstand_wasser[i, j]), 1),
        "abstand_meer_m": round(float(gel.abstand_meer[i, j]), 1),
        "abstand_ort_m": round(float(gel.abstand_ort[i, j]), 1),
        "abstand_stadt_m": round(float(sd), 1), "naechste_stadt": (st or {}).get("id"),
        "biom_abstand_m": round(float(gel.biom_abstand(biom)[i, j]), 1) if biom in _daten.BIOME else None,
        "baeume_im_radius": int(b4.sum()), "baumhoehe_max_m": int(bh.max()) if bh.size else 0,
    }


# ============================================================================================
# Auswahl
# ============================================================================================
def kandidaten(welt, gel, biom, score, n=10, abstand_m=None, maske=None, belegt=None, raster_m=10.0,
               min_score=None, mit_merkmalen=True, **filter_kw):
    """Beste n Ortsmitten im Biom (greedy nach Score mit Mindestabstand).

    score:     2D-Array (Welt-Raster) oder Funktion (welt, gel) -> Array.
    abstand_m: Mindestabstand untereinander (Standard 350 m, kleine Biome 200 m).
    maske:     eigene Filtermaske (sonst filter_maske(welt, gel, biom, **filter_kw)).
    belegt:    Liste dict(x_m, y_m[, biom]) bereits vergebener Orte (alle Biome; format.belegte_punkte) -
               Abstand je Paar nach format.mindestabstand_m.
    raster_m:  Vorauswahl: bester Punkt je raster_m x raster_m Block.
    Rueckgabe: Liste dict (Merkmale + score), beste zuerst.
    """
    from . import format as _fmt
    if callable(score):
        score = score(welt, gel)
    if maske is None:
        maske = filter_maske(welt, gel, biom, **filter_kw)
    if abstand_m is None:
        abstand_m = 200.0 if _daten.ist_kleines_biom(biom) else 350.0
    ii, jj = np.nonzero(maske)
    if not ii.size:
        log("kandidaten(%s): Filtermaske leer" % biom)
        return []
    sc = score[ii, jj].astype(np.float64)
    ok = np.isfinite(sc)
    if min_score is not None:
        ok &= sc >= min_score
    ii, jj, sc = ii[ok], jj[ok], sc[ok]
    b = max(1, int(round(raster_m / welt.zelle_m)))
    key = (ii // b).astype(np.int64) * 100000 + (jj // b)
    o = np.lexsort((-sc, key))
    k = key[o]
    erst = np.ones(k.size, bool)
    erst[1:] = k[1:] != k[:-1]
    sel = o[erst]
    ii, jj, sc = ii[sel], jj[sel], sc[sel]
    x, y = welt.ij_zu_m(ii, jj)
    bel = belegt or []
    bx = np.array([p["x_m"] for p in bel], np.float64)
    by = np.array([p["y_m"] for p in bel], np.float64)
    bmin = np.array([_fmt.mindestabstand_m(biom, p.get("biom", biom)) for p in bel], np.float64)
    o = np.argsort(-sc, kind="stable")
    gx, gy, out = [], [], []
    for kk in o:
        if bx.size and np.any(np.hypot(bx - x[kk], by - y[kk]) < bmin):
            continue
        if gx and np.min(np.hypot(np.asarray(gx) - x[kk], np.asarray(gy) - y[kk])) < abstand_m:
            continue
        gx.append(x[kk])
        gy.append(y[kk])
        e = merkmale(welt, gel, x[kk], y[kk], biom=biom) if mit_merkmalen else \
            {"x_m": float(x[kk]), "y_m": float(y[kk]), "feld": _daten.feld_von_m(x[kk], y[kk])}
        e["score"] = round(float(sc[kk]), 4)
        out.append(e)
        if len(out) >= n:
            break
    return out


# ============================================================================================
# Erreichbarkeit
# ============================================================================================
def _douglas_peucker(p, tol):
    if len(p) < 3:
        return list(range(len(p)))
    a, b = p[0], p[-1]
    ab = b - a
    L = np.hypot(*ab)
    if L < 1e-9:
        d = np.hypot(*(p - a).T)
    else:
        d = np.abs(ab[0] * (p[:, 1] - a[1]) - ab[1] * (p[:, 0] - a[0])) / L
    k = int(np.argmax(d))
    if d[k] <= tol:
        return [0, len(p) - 1]
    l1 = _douglas_peucker(p[:k + 1], tol)
    l2 = _douglas_peucker(p[k:], tol)
    return l1[:-1] + [k + v for v in l2]


def _block(a, b, fn):
    ny, nx = a.shape
    ny2, nx2 = ny // b * b, nx // b * b
    a = a[:ny2, :nx2].reshape(ny2 // b, b, nx2 // b, b)
    return fn(fn(a, axis=3), axis=1)


def erreichbarkeit(welt, gel, x_m, y_m, max_grad=25.0, raster_m=4.0, rand_m=120.0, max_quer_grad=38.0,
                   ziel_m=None):
    """Fussweg vom naechsten Weg zum Ort (Dijkstra auf grobem Raster).

    Kante erlaubt (streng), wenn Steigung der Kante <= max_grad, Hang am Knoten <= max_quer_grad, kein Wasser.
    Kosten = Laenge * (1 + (Steigung/max_grad)^2). Findet 'streng' keinen Weg, sucht 'weich' (Steiles x15,
    Wasser x30 erlaubt) -> Pfadvorschlag (pfad_noetig = True).
    ziel_m: optional (x, y) eines bestimmten Wegpunkts statt 'irgendeine Wegzelle'.
    Rueckgabe dict: erreichbar, modus, laenge_m, luftlinie_m, umweg_faktor, max_steigung_grad,
    steil_laenge_m, pfad_noetig, weg_punkt_m, pfad_m [[x, y, z], ...] (vereinfacht, vom Ort zum Weg), pfad_cm.
    """
    z = welt.zelle_m
    b = max(1, int(round(raster_m / z)))
    i, j = welt.m_zu_ij(x_m, y_m)
    nw = int(gel.weg_naechst[i, j])
    if nw < 0:
        return {"erreichbar": False, "modus": "kein_weg", "pfad_noetig": True, "pfad_m": [], "pfad_cm": []}
    wx, wy = welt.flat_zu_m(nw)
    wx, wy = float(wx), float(wy)
    if ziel_m is not None:
        wx, wy = float(ziel_m[0]), float(ziel_m[1])
    x0, x1 = min(x_m, wx) - rand_m, max(x_m, wx) + rand_m
    y0, y1 = min(y_m, wy) - rand_m, max(y_m, wy) + rand_m
    fe = welt.fenster_box(x0, y0, x1, y1)
    h = _block(fe.get("hoehe").astype(np.float64), b, np.mean)
    weg = _block(fe.get("weg"), b, np.max) > 0
    wa = _block(fe.get("wasser"), b, np.max) > 0
    me = _block(fe.get("meer").astype(np.uint8), b, np.max) > 0
    ng = _block(fe.get(gel.neigung), b, np.mean)
    gy_, gx_ = h.shape
    if ziel_m is not None:
        ti, tj = (welt.m_zu_ij(wx, wy)[0] - fe.i0) // b, (welt.m_zu_ij(wx, wy)[1] - fe.j0) // b
        weg = np.zeros_like(weg)
        weg[min(max(ti, 0), gy_ - 1), min(max(tj, 0), gx_ - 1)] = True
    si = min(max((i - fe.i0) // b, 0), gy_ - 1)
    sj = min(max((j - fe.j0) // b, 0), gx_ - 1)
    cell = b * z
    tanmax = np.tan(np.radians(max_grad))
    hl = h.ravel().tolist()
    wegl = weg.ravel().tolist()
    sperr = (wa | me).ravel().tolist()
    steil = (ng > max_quer_grad).ravel().tolist()
    nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    nbl = [(di, dj, cell * (1.4142135 if di and dj else 1.0)) for di, dj in nb]

    def suche(weich):
        N = gy_ * gx_
        dist = [float("inf")] * N
        vor = [-1] * N
        s = si * gx_ + sj
        dist[s] = 0.0
        heap = [(0.0, s)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            if wegl[u]:
                return u, dist, vor
            ui, uj = divmod(u, gx_)
            hu = hl[u]
            for di, dj, L in nbl:
                vi, vj = ui + di, uj + dj
                if vi < 0 or vj < 0 or vi >= gy_ or vj >= gx_:
                    continue
                v = vi * gx_ + vj
                g = abs(hl[v] - hu) / L
                f = 1.0 + (g / tanmax) ** 2
                if g > tanmax or steil[v]:
                    if not weich:
                        continue
                    f *= 15.0
                if sperr[v] and not wegl[v]:
                    if not weich:
                        continue
                    f *= 30.0
                nd = d + L * f
                if nd < dist[v]:
                    dist[v] = nd
                    vor[v] = u
                    heapq.heappush(heap, (nd, v))
        return -1, dist, vor

    modus = "streng"
    ziel, dist, vor = suche(False)
    if ziel < 0:
        modus = "weich"
        ziel, dist, vor = suche(True)
    if ziel < 0:
        return {"erreichbar": False, "modus": "kein_pfad", "pfad_noetig": True, "pfad_m": [], "pfad_cm": []}
    kette = []
    u = ziel
    while u >= 0:
        kette.append(u)
        u = vor[u]
    kette = kette[::-1]  # Ort -> Weg
    ci = np.array([k // gx_ for k in kette])
    cj = np.array([k % gx_ for k in kette])
    px, py = welt.ij_zu_m(fe.i0 + ci * b + (b - 1) / 2.0, fe.j0 + cj * b + (b - 1) / 2.0)
    px[0], py[0] = x_m, y_m
    pz = np.array([hl[k] for k in kette])
    seg = np.hypot(np.diff(px), np.diff(py))
    gr = np.degrees(np.arctan(np.abs(np.diff(pz)) / np.maximum(seg, 1e-6)))
    steil_L = float(seg[gr > max_grad].sum()) if seg.size else 0.0
    laenge = float(seg.sum())
    luft = float(np.hypot(px[-1] - x_m, py[-1] - y_m))
    P = np.stack([px, py], 1)
    keep = _douglas_peucker(P, 2.0)
    pfad = [[round(float(px[k]), 1), round(float(py[k]), 1), round(float(pz[k]), 2)] for k in keep]
    return {"erreichbar": modus == "streng", "modus": modus, "laenge_m": round(laenge, 1),
            "luftlinie_m": round(luft, 1), "umweg_faktor": round(laenge / max(luft, 1.0), 2),
            "max_steigung_grad": round(float(gr.max()) if gr.size else 0.0, 1),
            "mittel_steigung_grad": round(float(np.average(gr, weights=seg)) if seg.sum() > 0 else 0.0, 1),
            "steil_laenge_m": round(steil_L, 1), "pfad_noetig": modus != "streng",
            "weg_punkt_m": [round(float(px[-1]), 1), round(float(py[-1]), 1)],
            "pfad_m": pfad, "pfad_cm": [[int(p[0] * 100), int(p[1] * 100), int(p[2] * 100)] for p in pfad]}
