"""gelaende.py - Gelaendeanalyse auf den Welt-Rastern (2 m oder 1 m).

Reine Array-Funktionen (h = Hoehe in m, z = Zellgroesse in m):
  glaetten(a, sigma_px), box_mittel(a, r_px), max_filter(a, r_px), min_filter(a, r_px)
  hangneigung(h, z) [Grad], exposition(h, z) [Grad, 0 = Nord (-Y), 90 = Ost (+X), Richtung hangab]
  kruemmung(h, z, sigma_m) -> (profil, plan) [1/m]; > 0 konvex (Kante/Ruecken), < 0 konkav (Hangfuss/Rinne)
  tpi(h, z, radius_m) [m] = h - Mittel im Quadrat 2r
  abfluss(h, z, auslass) -> dict(gefuellt, empfaenger, akkumulation_m2, becken_zahl, ...)  (D8, Senken gefuellt)
  abstand(maske, z, max_m) -> (Abstand m, naechster Index)   (exakt; SciPy falls vorhanden, sonst Felzenszwalb)
  landformen(tpi_klein, tpi_gross, neigung) -> Klassen 1..10 (Weiss 2001, LANDFORMEN)

Klasse Gelaende(welt, cache=...) rechnet Ganze-Welt-Raster einmal und legt sie als .npy ab:
  gel.neigung, gel.exposition, gel.gefuellt, gel.senkentiefe, gel.empfaenger, gel.akkumulation (m2),
  gel.haupt_zufluss, gel.abstand_weg, gel.weg_naechst, gel.abstand_ort, gel.abstand_wasser,
  gel.abstand_meer, gel.abstand_stadt (zum Stadtrand), gel.tpi(r), gel.kruemmung(sigma),
  gel.landformen(), gel.tiefenlinien(min_m2), gel.gerinne_anfaenge(min_m2), gel.stufen(...),
  gel.kuppen(...), gel.kessel(...), gel.biom_abstand(name)  (> 0 innen, < 0 aussen)
"""

import hashlib
import heapq
import json
import os
import time

import numpy as np

from . import log, Uhr, __version__
from . import daten as _daten

try:  # optional
    from scipy import ndimage as _ndi  # noqa
except Exception:  # pragma: no cover
    _ndi = None

STANDARD_CACHE = "/tmp/claude-0/-home-user-fbulut/a2c581ba-c24a-5bce-9c65-c37d036a756e/scratchpad/a13/cache"

RICHTUNGEN = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

LANDFORMEN = {1: "Schlucht/Kessel", 2: "Rinne am Hang", 3: "Hochmulde", 4: "Talboden (U-Tal)",
              5: "Ebene", 6: "offener Hang", 7: "Oberhang/Plateaukante", 8: "Sporn im Tal",
              9: "Ruecken/Grat am Hang", 10: "Kuppe/Gipfel"}


# ============================================================================================
# Filter
# ============================================================================================
def _paar(di, dj, ny, nx):
    """Slices (quelle, nachbar) mit nachbar = quelle + (di, dj)."""
    s = (slice(max(0, -di), ny - max(0, di)), slice(max(0, -dj), nx - max(0, dj)))
    n = (slice(max(0, di), ny - max(0, -di)), slice(max(0, dj), nx - max(0, -dj)))
    return s, n


def _box1d(a, r, achse):
    """Normiertes Kastenmittel (Fenster am Rand gekappt) entlang einer Achse (ohne Umkopieren der Achse)."""
    if r <= 0:
        return a.astype(np.float32, copy=True)
    n = a.shape[achse]
    nd = a.ndim

    def S(start, stop):
        t = [slice(None)] * nd
        t[achse] = slice(start, stop)
        return tuple(t)

    def I(idx):
        t = [slice(None)] * nd
        t[achse] = idx
        return tuple(t)

    form = [1] * nd
    form[achse] = -1
    cs = np.cumsum(a, axis=achse, dtype=np.float64)
    pad = [(0, 0)] * nd
    pad[achse] = (1, 0)
    c = np.pad(cs, pad)
    del cs
    out = np.empty(a.shape, np.float32)
    if n - 2 * r > 0:
        out[S(r, n - r)] = (c[S(2 * r + 1, n + 1)] - c[S(0, n - 2 * r)]) / float(2 * r + 1)
    rand = np.unique(np.concatenate([np.arange(min(r, n)), np.arange(max(n - r, 0), n)]))
    if rand.size:
        hi = np.minimum(rand + r, n - 1) + 1
        lo = np.maximum(rand - r, 0)
        out[I(rand)] = (c[I(hi)] - c[I(lo)]) / (hi - lo).astype(np.float64).reshape(form)
    return out


def box_mittel(a, r_px):
    """Mittel im Quadrat (2r+1)^2, am Rand normiert."""
    r = int(round(r_px))
    return _box1d(_box1d(a, r, 0), r, 1)


def _gauss_boxen(sigma, n=3):
    w_ideal = np.sqrt(12.0 * sigma * sigma / n + 1.0)
    wl = int(np.floor(w_ideal))
    if wl % 2 == 0:
        wl -= 1
    wl = max(wl, 1)
    wu = wl + 2
    m = round((12.0 * sigma * sigma - n * wl * wl - 4 * n * wl - 3 * n) / (-4.0 * wl - 4.0))
    return [(wl - 1) // 2 if k < m else (wu - 1) // 2 for k in range(n)]


def glaetten(a, sigma_px):
    """Gauss-Glaettung (SciPy falls vorhanden, sonst 3 Kastenfilter)."""
    if sigma_px <= 0.3:
        return a.astype(np.float32, copy=True)
    if _ndi is not None:
        return _ndi.gaussian_filter(a.astype(np.float32), sigma_px, mode="nearest")
    out = a.astype(np.float32)
    for r in _gauss_boxen(float(sigma_px)):
        out = box_mittel(out, r)
    return out


def _ext1d(a, r, achse, fn, rand):
    if r <= 0:
        return a.copy()
    a = np.moveaxis(a, achse, 0)
    n = a.shape[0]
    pad = [(r, r)] + [(0, 0)] * (a.ndim - 1)
    cur = np.pad(a, pad, mode="constant", constant_values=rand)
    L = 2 * r + 1
    span = 1
    while span * 2 <= L:
        cur = fn(cur[:-span], cur[span:])
        span *= 2
    rest = L - span
    out = fn(cur[:n], cur[rest:rest + n])
    return np.moveaxis(out, 0, achse)


def max_filter(a, r_px):
    """Maximum im Quadrat (2r+1)^2 (O(N log r))."""
    r = int(round(r_px))
    if _ndi is not None:
        return _ndi.maximum_filter(a, size=2 * r + 1, mode="nearest")
    lo = np.iinfo(a.dtype).min if np.issubdtype(a.dtype, np.integer) else -np.inf
    return _ext1d(_ext1d(a, r, 0, np.maximum, lo), r, 1, np.maximum, lo)


def min_filter(a, r_px):
    r = int(round(r_px))
    if _ndi is not None:
        return _ndi.minimum_filter(a, size=2 * r + 1, mode="nearest")
    hi = np.iinfo(a.dtype).max if np.issubdtype(a.dtype, np.integer) else np.inf
    return _ext1d(_ext1d(a, r, 0, np.minimum, hi), r, 1, np.minimum, hi)


# ============================================================================================
# Ableitungen
# ============================================================================================
def gradient(h, z):
    """(dz/dx [Ost], dz/dy [Sued = +i])."""
    gy, gx = np.gradient(h.astype(np.float32), float(z))
    return gx, gy


def hangneigung(h, z):
    gx, gy = gradient(h, z)
    return np.degrees(np.arctan(np.hypot(gx, gy))).astype(np.float32)


def exposition(h, z):
    """Himmelsrichtung, in die der Hang abfaellt: 0 = Nord (-Y), 90 = Ost, 180 = Sued, 270 = West."""
    gx, gy = gradient(h, z)
    return (np.degrees(np.arctan2(-gx, gy)) % 360.0).astype(np.float32)


def kruemmung(h, z, sigma_m):
    """(profil, plan) in 1/m nach Glaettung mit sigma_m.

    profil > 0: konvex in Fallrichtung (Kante, Schulter); < 0: konkav (Hangfuss, Gefaellsknick unten).
    plan   > 0: konvex quer (Ruecken, Sporn, divergent); < 0: konkav (Rinne, Mulde, konvergent).
    """
    hs = glaetten(h, sigma_m / float(z))
    p, q = gradient(hs, z)
    r = np.gradient(p, float(z), axis=1)
    t = np.gradient(q, float(z), axis=0)
    s = np.gradient(p, float(z), axis=0)
    g2 = p * p + q * q
    g2s = np.maximum(g2, 1e-8)
    kn = (r * p * p + 2 * s * p * q + t * q * q) / g2s
    kt = (r * q * q - 2 * s * p * q + t * p * p) / g2s
    profil = -kn / np.power(1 + g2, 1.5)
    plan = -kt / np.sqrt(1 + g2)
    flach = g2 < 1e-6
    lap = -(r + t)
    profil = np.where(flach, lap * 0.5, profil).astype(np.float32)
    plan = np.where(flach, lap * 0.5, plan).astype(np.float32)
    return profil, plan


def kruemmung_mehrskalig(h, z, sigmas_m=(10, 25, 50)):
    return {s: kruemmung(h, z, s) for s in sigmas_m}


def tpi(h, z, radius_m):
    """Topographic Position Index: h - Mittel im Quadrat (Kantenlaenge 2r)."""
    return (h - box_mittel(h, radius_m / float(z))).astype(np.float32)


def landformen(tpi_klein, tpi_gross, neigung, std_klein=None, std_gross=None, flach_grad=5.0):
    """Landformklassen 1..10 nach Weiss (2001) aus standardisierten TPI zweier Skalen."""
    sk = std_klein or float(np.std(tpi_klein)) or 1.0
    sg = std_gross or float(np.std(tpi_gross)) or 1.0
    s = tpi_klein / sk
    g = tpi_gross / sg
    k = np.zeros(s.shape, np.uint8)
    sn, sm, sp = s <= -1, (s > -1) & (s < 1), s >= 1
    gn, gm, gp = g <= -1, (g > -1) & (g < 1), g >= 1
    k[sn & gn] = 1
    k[sn & gm] = 2
    k[sn & gp] = 3
    k[sm & gn] = 4
    k[sm & gm & (neigung <= flach_grad)] = 5
    k[sm & gm & (neigung > flach_grad)] = 6
    k[sm & gp] = 7
    k[sp & gn] = 8
    k[sp & gm] = 9
    k[sp & gp] = 10
    return k


# ============================================================================================
# Distanzen
# ============================================================================================
def _edt(maske):
    """Exakte euklidische Distanztransformation (Felzenszwalb & Huttenlocher), vektorisiert ueber Zeilen.

    Rueckgabe: (d2 in Zellen^2 als float64, naechste Zeile, naechste Spalte) - ohne Saat: d2 >= 1e12.
    """
    ny, nx = maske.shape
    BIG = 1e7
    # Phase 1: je Spalte Abstand zur naechsten Saat in derselben Spalte
    g = np.empty((ny, nx), np.float64)
    fr = np.empty((ny, nx), np.int32)
    gp = np.full(nx, BIG)
    rp = np.full(nx, -1, np.int32)
    for i in range(ny):
        m = maske[i]
        gp = np.where(m, 0.0, gp + 1.0)
        rp = np.where(m, i, rp)
        g[i] = gp
        fr[i] = rp
    gp = np.full(nx, BIG)
    rp = np.full(nx, -1, np.int32)
    for i in range(ny - 1, -1, -1):
        m = maske[i]
        gp = np.where(m, 0.0, gp + 1.0)
        rp = np.where(m, i, rp)
        b = gp < g[i]
        g[i] = np.where(b, gp, g[i])
        fr[i] = np.where(b, rp, fr[i])
    f = np.minimum(g, BIG) ** 2
    del g
    # Phase 2: je Zeile untere Einhuellende der Parabeln f(q) + (x - q)^2 (transponiert = zusammenhaengend)
    fT = np.ascontiguousarray(f.T)
    del f
    R = np.arange(ny)
    v = np.zeros((nx, ny), np.int32)
    zz = np.empty((nx + 1, ny), np.float64)
    zz[0] = -np.inf
    zz[1] = np.inf
    k = np.zeros(ny, np.int64)
    for q in range(1, nx):
        fq = fT[q] + q * q
        while True:
            vk = v[k, R]
            s = (fq - (fT[vk, R] + vk.astype(np.float64) ** 2)) / (2.0 * (q - vk))
            m = s <= zz[k, R]
            if not m.any():
                break
            k = np.where(m, k - 1, k)
        k = k + 1
        v[k, R] = q
        zz[k, R] = s
        zz[k + 1, R] = np.inf
    d2T = np.empty((nx, ny), np.float64)
    ncT = np.empty((nx, ny), np.int32)
    k = np.zeros(ny, np.int64)
    for q in range(nx):
        while True:
            m = zz[k + 1, R] < q
            if not m.any():
                break
            k = np.where(m, k + 1, k)
        vk = v[k, R]
        d2T[q] = (q - vk).astype(np.float64) ** 2 + fT[vk, R]
        ncT[q] = vk
    del v, zz, fT
    d2 = np.ascontiguousarray(d2T.T)
    nc = np.ascontiguousarray(ncT.T)
    del d2T, ncT
    nr = np.take_along_axis(fr, nc.astype(np.int64), axis=1)
    return d2, nr, nc


def abstand(maske, z, max_m=2000.0, indizes=False):
    """Euklidischer Abstand (m) jeder Zelle zur naechsten True-Zelle der Maske.

    Rueckgabe: abstand (float32, > max_m gekappt auf max_m) [, naechster flacher Index (int32, -1 = keiner)].
    Exakt: SciPy distance_transform_edt falls vorhanden, sonst eigene Felzenszwalb-Transformation.
    """
    ny, nx = maske.shape
    if not maske.any():
        d = np.full((ny, nx), max_m, np.float32)
        return (d, np.full((ny, nx), -1, np.int32)) if indizes else d
    if _ndi is not None:
        if indizes:
            d, ind = _ndi.distance_transform_edt(~maske, sampling=z, return_indices=True)
            idx = (ind[0].astype(np.int64) * nx + ind[1]).astype(np.int32)
            return np.minimum(d, max_m).astype(np.float32), idx
        d = _ndi.distance_transform_edt(~maske, sampling=z)
        return np.minimum(d, max_m).astype(np.float32)
    d2, nr, nc = _edt(maske)
    gueltig = (d2 < 1e11) & (nr >= 0)
    d = np.where(gueltig, np.minimum(np.sqrt(d2) * z, max_m), max_m).astype(np.float32)
    if not indizes:
        return d
    idx = np.where(gueltig, nr.astype(np.int64) * nx + nc, -1).astype(np.int32)
    return d, idx


# ============================================================================================
# Abfluss (D8) mit Senkenfuellung ueber Becken-Graph
# ============================================================================================
def _steilster(h, z, auslass):
    ny, nx = h.shape
    best = np.zeros((ny, nx), np.float32)
    rec = np.full((ny, nx), -1, np.int32)
    idx = np.arange(ny * nx, dtype=np.int32).reshape(ny, nx)
    for di, dj in RICHTUNGEN:
        d = z * (1.4142135 if di and dj else 1.0)
        s, n = _paar(di, dj, ny, nx)
        sl = (h[s] - h[n]) / d
        b = best[s]
        m = sl > b
        np.putmask(b, m, sl)
        np.putmask(rec[s], m, idx[n])
    rec[auslass] = -1
    return rec


def _flaechen_aufloesen(h, rec, auslass):
    """Zellen ohne tieferen Nachbarn: BFS durch gleich hohe Zellen zu einem Abfluss (Rueckgabe: offene Maske)."""
    ny, nx = h.shape
    N = ny * nx
    offen = (rec < 0) & ~auslass
    abfl = ~offen
    idx = np.arange(N, dtype=np.int32).reshape(ny, nx)
    neu = []
    for di, dj in RICHTUNGEN:
        s, n = _paar(di, dj, ny, nx)
        m = offen[s] & abfl[n] & (h[s] == h[n])
        if not m.any():
            continue
        np.putmask(rec[s], m, idx[n])
        o = offen[s]
        o[m] = False
        neu.append(idx[s][m])
    hf = h.reshape(-1)
    of = offen.reshape(-1)
    rf = rec.reshape(-1)
    F = np.concatenate(neu) if neu else np.zeros(0, np.int32)
    runden = 0
    while F.size:
        runden += 1
        fi = F // nx
        fj = F % nx
        neu = []
        for di, dj in RICHTUNGEN:
            ni = fi - di
            nj = fj - dj
            g = (ni >= 0) & (ni < ny) & (nj >= 0) & (nj < nx)
            X = (ni[g] * nx + nj[g]).astype(np.int32)
            Fg = F[g]
            m = of[X] & (hf[X] == hf[Fg])
            X = X[m]
            if X.size:
                rf[X] = Fg[m]
                of[X] = False
                neu.append(X)
        F = np.concatenate(neu) if neu else np.zeros(0, np.int32)
    return offen, runden


def akkumulation(rec, flaeche=1.0, gewicht=None):
    """Abflussakkumulation (Summe der Zuflussflaeche inkl. eigener Zelle) ueber Empfaenger-Feld.

    rec: flach (int32, -1 = Ende). Rueckgabe float32 (Einheit = flaeche * gewicht).
    """
    rec = rec.reshape(-1)
    N = rec.size
    acc = np.full(N, float(flaeche), np.float64) if gewicht is None else \
        gewicht.reshape(-1).astype(np.float64) * flaeche
    gueltig = rec >= 0
    indeg = np.bincount(rec[gueltig], minlength=N).astype(np.int32)
    F = np.flatnonzero(indeg == 0).astype(np.int32)
    while F.size:
        t = rec[F]
        m = t >= 0
        F = F[m]
        t = t[m]
        if not t.size:
            break
        ut, inv = np.unique(t, return_inverse=True)
        acc[ut] += np.bincount(inv, weights=acc[F])
        indeg[ut] -= np.bincount(inv).astype(np.int32)
        F = ut[indeg[ut] == 0]
    return acc.astype(np.float32)


def abfluss(h, z, auslass):
    """D8-Abfluss mit vollstaendiger Senkenfuellung.

    auslass: bool-Maske (Meer, Weltrand) - dort endet der Abfluss.
    Verfahren: steilster Abstieg -> Flaechen per BFS aufloesen -> Becken (Wurzeln) per Zeigersprung ->
    Becken-Graph mit Ueberlaufhoehen -> Prioritaetsflutung vom Auslass -> gefuellt = max(h, Pegel) ->
    D8 auf gefuelltem Gelaende + Flaechen-BFS -> Akkumulation (m2).
    Rueckgabe dict: gefuellt (f32), empfaenger (int32 flach, -1 = Ende), akkumulation_m2 (f32),
    becken_zahl, offene_rest (Zellen ohne Abfluss nach dem Fuellen, sollte 0 sein).
    """
    h = h.astype(np.float32)
    ny, nx = h.shape
    N = ny * nx
    auslass = auslass.copy()
    auslass[0, :] = auslass[-1, :] = True
    auslass[:, 0] = auslass[:, -1] = True
    # 1) Roh-D8 + Flaechen
    rec = _steilster(h, z, auslass)
    offen, _ = _flaechen_aufloesen(h, rec, auslass)
    # 2) Restsenken: auf gleich hohen offenen Nachbarn mit kleinerem Index zeigen (zyklenfrei)
    idx = np.arange(N, dtype=np.int32).reshape(ny, nx)
    for di, dj in ((-1, -1), (-1, 0), (-1, 1), (0, -1)):
        s, n = _paar(di, dj, ny, nx)
        m = offen[s] & offen[n] & (h[s] == h[n]) & (rec[s] < 0)
        np.putmask(rec[s], m, idx[n])
    # 3) Wurzeln / Becken
    rf = rec.reshape(-1)
    wurzel = rf < 0
    lab = rf.copy()
    W = np.flatnonzero(wurzel).astype(np.int32)
    lab[W] = W
    for _ in range(64):
        nl = lab[lab]
        if np.array_equal(nl, lab):
            break
        lab = nl
    innen = ~auslass.reshape(-1)[W]
    bmap = np.zeros(W.size, np.int32)
    bmap[innen] = np.arange(1, int(innen.sum()) + 1, dtype=np.int32)
    becken = bmap[np.searchsorted(W, lab)].reshape(ny, nx)
    del lab
    B = int(innen.sum()) + 1
    # 4) Kanten zwischen Becken mit Ueberlaufhoehe
    us, vs, ws = [], [], []
    for di, dj in ((0, 1), (1, 0), (1, 1), (1, -1)):
        s, n = _paar(di, dj, ny, nx)
        a = becken[s]
        b = becken[n]
        m = a != b
        if not m.any():
            continue
        aa, bb = a[m], b[m]
        us.append(np.minimum(aa, bb))
        vs.append(np.maximum(aa, bb))
        ws.append(np.maximum(h[s][m], h[n][m]))
    u = np.concatenate(us).astype(np.int64)
    v = np.concatenate(vs).astype(np.int64)
    w = np.concatenate(ws)
    key = u * B + v
    o = np.lexsort((w, key))
    key, u, v, w = key[o], u[o], v[o], w[o]
    erst = np.ones(key.size, bool)
    erst[1:] = key[1:] != key[:-1]
    u, v, w = u[erst], v[erst], w[erst]
    # 5) Prioritaetsflutung auf dem Becken-Graph
    uu = np.concatenate([u, v])
    vv = np.concatenate([v, u])
    ww = np.concatenate([w, w]).astype(np.float64)
    o = np.argsort(uu, kind="stable")
    uu, vv, ww = uu[o], vv[o], ww[o]
    ptr = np.searchsorted(uu, np.arange(B + 1)).tolist()
    adj = vv.tolist()
    wl = ww.tolist()
    pegel = [float("inf")] * B
    fertig = bytearray(B)
    pegel[0] = float("-inf")
    heap = [(float("-inf"), 0)]
    while heap:
        l, b = heapq.heappop(heap)
        if fertig[b]:
            continue
        fertig[b] = 1
        for k in range(ptr[b], ptr[b + 1]):
            c = adj[k]
            if fertig[c]:
                continue
            nl = wl[k] if wl[k] > l else l
            if nl < pegel[c]:
                pegel[c] = nl
                heapq.heappush(heap, (nl, c))
    peg = np.array(pegel, np.float64)
    peg[~np.isfinite(peg)] = -1e9
    gefuellt = np.maximum(h, peg[becken].astype(np.float32))
    del becken
    # 6) D8 auf gefuelltem Gelaende
    rec = _steilster(gefuellt, z, auslass)
    offen, runden = _flaechen_aufloesen(gefuellt, rec, auslass)
    rest = int(offen.sum())
    rec = rec.reshape(-1)
    acc = akkumulation(rec, flaeche=z * z)
    return {"gefuellt": gefuellt, "empfaenger": rec, "akkumulation_m2": acc.reshape(ny, nx),
            "becken_zahl": int(B), "offene_rest": rest, "flaechen_runden": runden}


def haupt_zufluss(rec, acc):
    """Je Zelle der Zufluss mit der groessten Akkumulation (-1 = keiner). Flach int32."""
    rec = rec.reshape(-1)
    acc = acc.reshape(-1)
    c = np.flatnonzero(rec >= 0)
    o = np.lexsort((acc[c], rec[c]))
    c = c[o]
    r = rec[c]
    letzt = np.ones(c.size, bool)
    letzt[:-1] = r[:-1] != r[1:]
    out = np.full(rec.size, -1, np.int32)
    out[r[letzt]] = c[letzt]
    return out


def _schrittlaenge(von, nach, nx, z):
    d = np.abs(nach.astype(np.int64) - von)
    diag = (d == nx - 1) | (d == nx + 1)
    return np.where(diag, z * 1.4142135, z)


def pfad_folgen(start, zeiger, schritte, nx, z):
    """Folgt einem Zeigerfeld (Empfaenger oder Haupt-Zufluss) 'schritte' Mal. -> (Ende, Laenge m)."""
    idx = np.asarray(start, np.int64).copy()
    laenge = np.zeros(idx.shape, np.float64)
    for _ in range(int(schritte)):
        nxt = zeiger[idx].astype(np.int64)
        ok = nxt >= 0
        laenge += np.where(ok, _schrittlaenge(idx, np.where(ok, nxt, idx), nx, z), 0.0)
        idx = np.where(ok, nxt, idx)
    return idx, laenge


def punkte_nms(x, y, wert, abstand_m, n_max=None):
    """Greedy-Auswahl (absteigend nach wert) mit Mindestabstand. Rueckgabe Indizes."""
    o = np.argsort(-np.asarray(wert), kind="stable")
    gew = []
    gx, gy = [], []
    a2 = abstand_m * abstand_m
    for k in o:
        if gx:
            dx = np.asarray(gx) - x[k]
            dy = np.asarray(gy) - y[k]
            if np.min(dx * dx + dy * dy) < a2:
                continue
        gew.append(int(k))
        gx.append(x[k])
        gy.append(y[k])
        if n_max and len(gew) >= n_max:
            break
    return np.array(gew, np.int64)


# ============================================================================================
# Ganze-Welt-Klasse mit Cache
# ============================================================================================
def cache_ordner_standard():
    return os.environ.get("SEHENS_CACHE") or STANDARD_CACHE


class Gelaende:
    """Lazy berechnete Ganze-Welt-Raster einer Welt, mit .npy-Cache.

    cache: Ordner (Standard: $SEHENS_CACHE oder STANDARD_CACHE), False = kein Cache.
    Unterordner je Datenstand (Fingerabdruck aus Hoehe, Weg, Ort, Wasser, Zellgroesse).
    """

    def __init__(self, welt, cache=None):
        self.welt = welt
        self.z = welt.zelle_m
        self._mem = {}
        if cache is False:
            self.cache = None
        else:
            basis = cache or cache_ordner_standard()
            self.cache = os.path.join(basis, self._fingerabdruck())
            os.makedirs(self.cache, exist_ok=True)

    def _fingerabdruck(self):
        w = self.welt
        hsh = hashlib.sha1()
        hsh.update(("v%s|%s|%s" % (__version__, w.zelle_m, w.hoehe.shape)).encode())
        for a in (w.hoehe, w.weg, w.ort, w.wasser, w.biom):
            hsh.update(np.ascontiguousarray(a.reshape(-1)[::97]).tobytes())
        st = json.dumps([(s["x_m"], s["y_m"], s["radius_m"]) for s in w.staedte]).encode()
        hsh.update(st)
        return "welt_%dm_%s" % (int(round(w.zelle_m)), hsh.hexdigest()[:12])

    def _get(self, name, fn):
        if name in self._mem:
            return self._mem[name]
        pf = os.path.join(self.cache, name + ".npy") if self.cache else None
        if pf and os.path.exists(pf):
            t0 = time.perf_counter()
            a = np.load(pf)
            log("Cache geladen: %s (%.2f s)" % (name, time.perf_counter() - t0))
        else:
            with Uhr("berechne " + name):
                a = fn()
            if pf:
                tmp = pf + ".tmp.npy"
                np.save(tmp, a)
                os.replace(tmp, pf)
        self._mem[name] = a
        return a

    def _speichern(self, name, a):
        self._mem[name] = a
        if self.cache:
            pf = os.path.join(self.cache, name + ".npy")
            tmp = pf + ".tmp.npy"
            np.save(tmp, a)
            os.replace(tmp, pf)

    def vorrechnen(self, alles=True):
        """Rechnet die Standard-Raster (fuer den Cache) einmal durch."""
        _ = self.neigung, self.akkumulation, self.abstand_weg, self.abstand_ort
        _ = self.abstand_wasser, self.abstand_meer, self.abstand_stadt
        if alles:
            _ = self.tpi(25), self.tpi(100), self.haupt_zufluss, self.exposition

    # -- Basis --
    @property
    def neigung(self):
        return self._get("neigung", lambda: hangneigung(self.welt.hoehe, self.z))

    @property
    def exposition(self):
        return self._get("exposition", lambda: exposition(self.welt.hoehe, self.z))

    def tpi(self, radius_m):
        r = int(round(radius_m))
        return self._get("tpi_%d" % r, lambda: tpi(self.welt.hoehe, self.z, r))

    def kruemmung(self, sigma_m):
        """(profil, plan) fuer sigma_m (10/25/50 m empfohlen)."""
        s = int(round(sigma_m))

        def f():
            p, q = kruemmung(self.welt.hoehe, self.z, s)
            return np.stack([p, q])
        a = self._get("kruemmung_%d" % s, f)
        return a[0], a[1]

    def landformen(self, r_klein=25, r_gross=100):
        def f():
            tk, tg = self.tpi(r_klein), self.tpi(r_gross)
            land = ~self.welt.meer
            return landformen(tk, tg, self.neigung, float(np.std(tk[land])), float(np.std(tg[land])))
        return self._get("landformen_%d_%d" % (r_klein, r_gross), f)

    # -- Abfluss --
    def _abfluss(self):
        if "gefuellt" in self._mem and "empfaenger" in self._mem and "akkumulation" in self._mem:
            return
        namen = ("gefuellt", "empfaenger", "akkumulation")
        if self.cache and all(os.path.exists(os.path.join(self.cache, n + ".npy")) for n in namen):
            for n in namen:
                self._get(n, None)
            return
        with Uhr("berechne Abfluss (D8, Senken fuellen)"):
            r = abfluss(self.welt.hoehe, self.z, self.welt.meer)
        log("Abfluss: %d Becken gefuellt, %d Zellen ohne Abfluss, %d BFS-Runden"
            % (r["becken_zahl"], r["offene_rest"], r["flaechen_runden"]))
        for n, a in (("gefuellt", r["gefuellt"]), ("empfaenger", r["empfaenger"]),
                     ("akkumulation", r["akkumulation_m2"])):
            self._speichern(n, a)

    @property
    def gefuellt(self):
        self._abfluss()
        return self._mem["gefuellt"]

    @property
    def empfaenger(self):
        """Flach int32: Index der Abflusszelle (D8 auf gefuelltem Gelaende), -1 = Meer/Rand."""
        self._abfluss()
        return self._mem["empfaenger"]

    @property
    def akkumulation(self):
        """Einzugsflaeche in m2 (inkl. Zelle)."""
        self._abfluss()
        return self._mem["akkumulation"]

    @property
    def senkentiefe(self):
        """gefuellt - hoehe (m): > 0 in geschlossenen Senken (Kessel, Seebecken, Dolinen)."""
        return self._get("senkentiefe", lambda: (self.gefuellt - self.welt.hoehe).astype(np.float32))

    @property
    def haupt_zufluss(self):
        return self._get("haupt_zufluss", lambda: haupt_zufluss(self.empfaenger, self.akkumulation))

    def tiefenlinien(self, min_flaeche_m2=5000.0):
        """bool: Zellen mit Einzugsgebiet >= min_flaeche_m2 (Tiefenlinien/Gerinne)."""
        return self.akkumulation >= min_flaeche_m2

    def gerinne_anfaenge(self, min_flaeche_m2=5000.0):
        """Flache Indizes der Gerinne-Anfaenge (Tiefenlinie ohne Tiefenlinien-Zufluss) - Quellen."""
        k = self.tiefenlinien(min_flaeche_m2).reshape(-1)
        rec = self.empfaenger
        c = np.flatnonzero(k & (rec >= 0))
        hat_zufluss = np.zeros(k.size, bool)
        hat_zufluss[rec[c]] = True
        return np.flatnonzero(k & ~hat_zufluss)

    def stufen(self, min_flaeche_m2=20000.0, kurz_m=12.0, lang_m=60.0, min_fall_m=3.0,
               faktor=2.5, nms_m=40.0, maske=None):
        """Gefaellsspruenge entlang der Tiefenlinien (Wasserfall-/Kaskadenorte).

        Je Gerinnezelle: Fall ueber kurz_m talab vs. Gefaelle ueber lang_m bergauf (Haupt-Zufluss).
        Stufe, wenn Fall >= min_fall_m und Gefaelle_kurz >= faktor * max(Gefaelle_oben, 0.02).
        Rueckgabe dict von Arrays (idx, x_m, y_m, fall_m, gefaelle_kurz, gefaelle_oben, flaeche_m2),
        nach Fall absteigend, Mindestabstand nms_m.
        """
        w = self.welt
        nx = w.nx
        h = w.hoehe.reshape(-1)
        k = self.tiefenlinien(min_flaeche_m2).reshape(-1)
        if maske is not None:
            k = k & maske.reshape(-1)
        C = np.flatnonzero(k)
        ks = max(1, int(round(kurz_m / self.z)))
        kl = max(1, int(round(lang_m / self.z)))
        e, ls = pfad_folgen(C, self.empfaenger, ks, nx, self.z)
        fall = h[C] - h[e]
        oben, lo = pfad_folgen(C, self.haupt_zufluss, kl, nx, self.z)
        g_s = fall / np.maximum(ls, 1e-3)
        g_o = (h[oben] - h[C]) / np.maximum(lo, 1e-3)
        g_o = np.where(lo > 0, g_o, 0.0)
        m = (fall >= min_fall_m) & (g_s >= faktor * np.maximum(g_o, 0.02))
        C, fall, g_s, g_o = C[m], fall[m], g_s[m], g_o[m]
        x, y = w.flat_zu_m(C)
        sel = punkte_nms(x, y, fall, nms_m)
        acc = self.akkumulation.reshape(-1)
        return {"idx": C[sel], "x_m": x[sel], "y_m": y[sel], "fall_m": fall[sel].astype(np.float32),
                "gefaelle_kurz": g_s[sel].astype(np.float32), "gefaelle_oben": g_o[sel].astype(np.float32),
                "flaeche_m2": acc[C[sel]]}

    def kuppen(self, radius_m=60.0, min_tpi_m=4.0, maske=None, nms_m=None):
        """Kuppen/Gipfel: lokales Hoehenmaximum im Radius und TPI(radius) >= min_tpi_m. -> dict von Arrays."""
        w = self.welt
        r = int(round(radius_m / self.z))
        h = w.hoehe
        t = self.tpi(int(radius_m))
        m = (h >= max_filter(h, r)) & (t >= min_tpi_m) & ~w.meer
        if maske is not None:
            m &= maske
        ii, jj = np.nonzero(m)
        x, y = w.ij_zu_m(ii, jj)
        sel = punkte_nms(x, y, t[ii, jj], nms_m or radius_m)
        return {"idx": (ii * w.nx + jj)[sel], "x_m": x[sel], "y_m": y[sel],
                "tpi_m": t[ii, jj][sel], "hoehe_m": h[ii, jj][sel]}

    def kessel(self, radius_m=60.0, max_tpi_m=-4.0, maske=None, nms_m=None):
        """Kessel/Mulden: lokales Minimum des TPI im Radius mit TPI <= max_tpi_m (zusaetzlich Senkentiefe)."""
        w = self.welt
        r = int(round(radius_m / self.z))
        t = self.tpi(int(radius_m))
        m = (t <= min_filter(t, r)) & (t <= max_tpi_m) & ~w.meer
        if maske is not None:
            m &= maske
        ii, jj = np.nonzero(m)
        x, y = w.ij_zu_m(ii, jj)
        sel = punkte_nms(x, y, -t[ii, jj], nms_m or radius_m)
        st = self.senkentiefe
        return {"idx": (ii * w.nx + jj)[sel], "x_m": x[sel], "y_m": y[sel],
                "tpi_m": t[ii, jj][sel], "senkentiefe_m": st[ii, jj][sel]}

    def grate(self, sigma_m=25, min_plan=0.004, min_tpi_m=2.0, r_tpi=50):
        """bool: Ruecken/Grate (plan-konvex, ueber der Umgebung)."""
        _, plan = self.kruemmung(sigma_m)
        return (plan >= min_plan) & (self.tpi(r_tpi) >= min_tpi_m) & ~self.welt.meer

    def kanten(self, min_grad=35.0, sigma_m=10, min_profil=0.01):
        """bool: Gelaendestufen/Abbruchkanten (steil und profilkonvex)."""
        p, _ = self.kruemmung(sigma_m)
        return (self.neigung >= min_grad) & (p >= min_profil)

    # -- Distanzen --
    @property
    def abstand_weg(self):
        """Abstand zum naechsten Weg (m, gekappt bei 2000)."""
        self._weg()
        return self._mem["abstand_weg"]

    @property
    def weg_naechst(self):
        """Flacher Index der naechsten Wegzelle (int32, -1 = keine)."""
        self._weg()
        return self._mem["weg_naechst"]

    def _weg(self):
        if "abstand_weg" in self._mem and "weg_naechst" in self._mem:
            return
        if self.cache and all(os.path.exists(os.path.join(self.cache, n + ".npy"))
                              for n in ("abstand_weg", "weg_naechst")):
            self._get("abstand_weg", None)
            self._get("weg_naechst", None)
            return
        with Uhr("berechne abstand_weg (+ naechster Wegpunkt)"):
            d, i = abstand(self.welt.weg > 0, self.z, 2000.0, indizes=True)
        self._speichern("abstand_weg", d)
        self._speichern("weg_naechst", i)

    @property
    def abstand_ort(self):
        return self._get("abstand_ort", lambda: abstand(self.welt.ort > 0, self.z, 2000.0))

    @property
    def abstand_wasser(self):
        """Abstand zum Suesswasser (m)."""
        return self._get("abstand_wasser", lambda: abstand(self.welt.wasser > 0, self.z, 2000.0))

    @property
    def abstand_meer(self):
        return self._get("abstand_meer", lambda: abstand(self.welt.meer, self.z, 2000.0))

    @property
    def abstand_stadt(self):
        """Abstand zum Rand der naechsten geplanten Stadt (m; < 0 innerhalb des Radius)."""
        def f():
            w = self.welt
            out = np.full((w.ny, w.nx), 5000.0, np.float32)
            xs, ys, rs = w.staedte_m()
            for x, y, r in zip(xs, ys, rs):
                reich = 2000.0 + r
                fe = w.fenster(x, y, reich)
                X, Y = fe.gitter_m()
                d = (np.hypot(X - x, Y - y) - r).astype(np.float32)
                o = out[fe.sl]
                np.minimum(o, d, out=o)
            return out
        return self._get("abstand_stadt", f)

    def biom_abstand(self, name, rand_m=400.0):
        """Vorzeichenbehafteter Abstand zur Biomgrenze (m): > 0 innen (Abstand zum Nicht-Biom inkl. Meer),
        < 0 aussen (Abstand zum Biom). Ausserhalb Biom-Rechteck + rand_m: -rand_m."""
        w = self.welt

        def f():
            m = w.biom_maske(name)
            out = np.full((w.ny, w.nx), -float(rand_m), np.float32)
            if not m.any():
                return out
            ii, jj = np.nonzero(m)
            r = int(np.ceil(rand_m / self.z))
            i0, i1 = max(0, ii.min() - r), min(w.ny, ii.max() + r + 1)
            j0, j1 = max(0, jj.min() - r), min(w.nx, jj.max() + r + 1)
            sub = m[i0:i1, j0:j1]
            innen = abstand(~sub, self.z, 2000.0)
            aussen = abstand(sub, self.z, rand_m)
            out[i0:i1, j0:j1] = np.where(sub, innen, -aussen)
            return out
        return self._get("biom_abstand_%s" % name, f)

    def stadt_abstand_punkt(self, x_m, y_m):
        """Abstand eines Punkts zum naechsten Stadtrand (m) + Stadt-Eintrag."""
        xs, ys, rs = self.welt.staedte_m()
        if not xs.size:
            return 1e9, None
        d = np.hypot(xs - x_m, ys - y_m) - rs
        k = int(np.argmin(d))
        return float(d[k]), self.welt.staedte[k]


# ============================================================================================
# Vektorhilfen
# ============================================================================================
def polylinie_proben(punkte_m, schritt_m=2.0):
    """Tastet eine Polylinie [[x, y], ...] (m) gleichmaessig ab -> (x, y, s) Arrays."""
    p = np.asarray(punkte_m, np.float64)[:, :2]
    if len(p) < 2:
        return p[:, 0], p[:, 1], np.zeros(len(p))
    seg = np.hypot(np.diff(p[:, 0]), np.diff(p[:, 1]))
    s = np.concatenate([[0], np.cumsum(seg)])
    n = max(2, int(s[-1] / schritt_m) + 1)
    ss = np.linspace(0, s[-1], n)
    return np.interp(ss, s, p[:, 0]), np.interp(ss, s, p[:, 1]), ss


def stufen_entlang_linie(welt, punkte_m, kurz_m=10.0, lang_m=50.0, min_fall_m=2.0, faktor=2.5,
                         z_spalte=None):
    """Gefaellsspruenge entlang einer Linie (z. B. Bach). punkte_m: [[x, y(, z)], ...] in m.

    z_spalte: Index der z-Spalte (m) in punkte_m, sonst Gelaendehoehe. Rueckgabe Liste von dict
    (x_m, y_m, s_m, fall_m, gefaelle_kurz, gefaelle_oben), Mindestabstand 2*kurz_m.
    """
    p = np.asarray(punkte_m, np.float64)
    x, y, s = polylinie_proben(p[:, :2], 2.0)
    if z_spalte is not None and p.shape[1] > z_spalte:
        seg = np.concatenate([[0], np.cumsum(np.hypot(np.diff(p[:, 0]), np.diff(p[:, 1])))])
        h = np.interp(s, seg, p[:, z_spalte])
    else:
        h = welt.bilinear(welt.hoehe, x, y)
    if s.size < 3:
        return []
    ds = s[1] - s[0]
    ks = max(1, int(round(kurz_m / ds)))
    kl = max(1, int(round(lang_m / ds)))
    out = []
    n = s.size
    fall = np.zeros(n)
    go = np.zeros(n)
    for k in range(n):
        e = min(n - 1, k + ks)
        a = max(0, k - kl)
        fall[k] = h[k] - h[e]
        go[k] = (h[a] - h[k]) / max(s[k] - s[a], 1e-3) if k > a else 0.0
    gs = fall / (ks * ds)
    m = (fall >= min_fall_m) & (gs >= faktor * np.maximum(go, 0.02))
    kk = np.flatnonzero(m)
    sel = punkte_nms(x[kk], y[kk], fall[kk], 2 * kurz_m)
    for i in kk[sel]:
        out.append({"x_m": float(x[i]), "y_m": float(y[i]), "s_m": float(s[i]), "fall_m": float(fall[i]),
                    "gefaelle_kurz": float(gs[i]), "gefaelle_oben": float(go[i])})
    return out


def bach_enden(welt, wasser_radius_m=6.0):
    """Anfang und Ende jedes Bachs aus welt.baeche (cm -> m) mit Lage zum Suesswasser.

    Rueckgabe Liste dict: id, feld, art ("quelle"/"ende"), x_m, y_m, z_m, im_wasser (anderes Gewaesser
    innerhalb wasser_radius_m ausser dem Bach selbst kann nicht getrennt werden -> Naeherung ueber Abstand
    des Endpunkts zum naechsten Wasser, das NICHT auf den letzten 20 m des Bachs liegt, wird hier nicht
    geprueft; im_wasser = Wasser im Radius am Endpunkt).
    """
    out = []
    r = max(1, int(round(wasser_radius_m / welt.zelle_m)))
    for b in welt.baeche:
        p = b.get("punkte") or []
        if len(p) < 2:
            continue
        for art, q in (("quelle", p[0]), ("ende", p[-1])):
            x, y = q[0] / 100.0, q[1] / 100.0
            i, j = welt.m_zu_ij(x, y)
            ws = welt.wasser[max(0, i - r):i + r + 1, max(0, j - r):j + r + 1]
            ms = welt.meer[max(0, i - r):i + r + 1, max(0, j - r):j + r + 1]
            out.append({"id": b.get("id"), "feld": b.get("feld"), "art": art, "x_m": x, "y_m": y,
                        "z_m": (q[2] / 100.0) if len(q) > 2 else welt.hoehe_bei_m(x, y),
                        "im_wasser": bool((ws > 0).mean() > 0.5), "am_meer": bool(ms.any())})
    return out


def meer_maske(welt):
    return welt.meer
