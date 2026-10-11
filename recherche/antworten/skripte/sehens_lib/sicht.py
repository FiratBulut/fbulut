"""sicht.py - Sichtlinien vom Weg zum Ort (Gelaende + Baumhoehe), Blickpositionen, Verdeckung.

Modell: Auge auf Boden + augenhoehe_m; Hindernis je Probe = Gelaende (bilinear) bzw. Gelaende + Baumhoehe (4 m,
falls dort Baeume stehen, mal baum_faktor). Gelaende sperrt sofort, Kronen erst ab baum_block (3) Proben unter
der Krone (Einzelbaeume lassen Luecken). Proben im Abstand schritt_m (Standard 4 m)
von nah_m hinter dem Auge bis ziel_rand_m vor dem Ziel.
Je Strahl wird die MINDESTHOEHE am Ziel berechnet, ab der eine Linie frei ist:
    z_min = max_t ( z_auge + (o(t) - z_auge) * d / t )
Sichtbarer Anteil der Silhouette [Boden_Ziel, Boden_Ziel + ziel_hoehe] = (Boden + H - z_min) / H (0..1).

API:
  wp = Wegpunkte(welt, abstand_m=20)                         # Wegzellen ausgeduennt (einmal je Welt)
  sicht_von_wegen(welt, wp, x_m, y_m, ziel_hoehe_m, r_min_m=300, r_max_m=800) -> dict
  verdeckt_vom_weg(welt, wp, x_m, y_m, ziel_hoehe_m=3, r_max_m=400) -> dict  (Fundstueck-Pruefung)
  beste_blickposition(welt, x_m, y_m, ziel_hoehe_m, r_min_m=30, r_max_m=150, gel=None) -> Liste dict
  sichtanteil(welt, ex, ey, tx, ty, ziel_hoehe_m, ...) -> (anteil, z_min) fuer beliebige Strahlen
  kameras_vorschlagen(welt, wp, ort_id, x_m, y_m, art, ziel_hoehe_m, gel=None, pfad_m=None) -> Liste §8
  zz_augenhoehe(welt, kx, ky, zx, zy, zz) -> ZZ so, dass die Kamera nach §8 auf Augenhoehe bleibt
"""

import numpy as np

from . import daten as _daten


class Wegpunkte:
    """Wegzellen auf ein Gitter von abstand_m ausgeduennt (je Gitterzelle die zur Mitte naechste Wegzelle)."""

    def __init__(self, welt, abstand_m=20.0):
        self.welt = welt
        self.abstand_m = float(abstand_m)
        ii, jj = np.nonzero(welt.weg > 0)
        x, y = welt.ij_zu_m(ii, jj)
        bx = np.floor((x - _daten.X_MIN_M) / abstand_m).astype(np.int64)
        by = np.floor((y - _daten.Y_MIN_M) / abstand_m).astype(np.int64)
        cx = _daten.X_MIN_M + (bx + 0.5) * abstand_m
        cy = _daten.Y_MIN_M + (by + 0.5) * abstand_m
        d = (x - cx) ** 2 + (y - cy) ** 2
        key = by * 100000 + bx
        o = np.lexsort((d, key))
        k = key[o]
        erst = np.ones(k.size, bool)
        erst[1:] = k[1:] != k[:-1]
        sel = o[erst]
        self.x_m = x[sel]
        self.y_m = y[sel]
        self.i = ii[sel]
        self.j = jj[sel]
        self.z_m = welt.hoehe[self.i, self.j].astype(np.float64)
        self.n = self.x_m.size

    def im_ring(self, x_m, y_m, r_min_m, r_max_m):
        d = np.hypot(self.x_m - x_m, self.y_m - y_m)
        return np.flatnonzero((d >= r_min_m) & (d <= r_max_m)), d

    def naechster(self, x_m, y_m):
        d = np.hypot(self.x_m - x_m, self.y_m - y_m)
        k = int(np.argmin(d))
        return k, float(d[k])


def _hindernis(welt, x, y, baum, baum_faktor):
    """(Gelaende, Gelaende + Krone oder -inf ohne Baum) an Probepunkten."""
    o = welt.bilinear(welt.hoehe, x, y)
    if not baum:
        return o, None
    i4, j4 = _daten.m_zu_pixel(x, y, 4.0)
    i4 = np.clip(np.rint(i4), 0, welt.baumhoehe4.shape[0] - 1).astype(np.int64)
    j4 = np.clip(np.rint(j4), 0, welt.baumhoehe4.shape[1] - 1).astype(np.int64)
    bh = welt.baumhoehe4[i4, j4].astype(np.float64)
    n = welt.baeume4[i4, j4]
    return o, np.where(n > 0, o + bh * baum_faktor, -np.inf)


def mindesthoehe(welt, ex, ey, ez, tx, ty, schritt_m=4.0, baum=True, baum_faktor=0.85, baum_block=3,
                 nah_m=6.0, ziel_rand_m=4.0):
    """Je Strahl Auge (ex, ey, ez absolut) -> Ziel (tx, ty): Mindesthoehe (absolut, m) am Ziel fuer freie Sicht.

    Gelaende sperrt sofort; Baumkronen erst ab baum_block Proben unter der Krone (lichte Einzelbaeume
    sperren nicht, ~baum_block * schritt_m Meter Kronendach schon).
    Alle Argumente Arrays gleicher Laenge (oder Skalare). Rueckgabe (z_min, d) Arrays.
    """
    ex, ey, ez, tx, ty = [np.atleast_1d(np.asarray(a, np.float64)) for a in (ex, ey, ez, tx, ty)]
    n = max(ex.size, tx.size)
    ex, ey, ez, tx, ty = [np.broadcast_to(a, (n,)) for a in (ex, ey, ez, tx, ty)]
    d = np.hypot(tx - ex, ty - ey)
    t_max = d - ziel_rand_m
    m = int(np.ceil(max(float(t_max.max()) - nah_m, 0.0) / schritt_m)) + 1
    t = nah_m + schritt_m * np.arange(m)[None, :]
    gueltig = t <= t_max[:, None]
    dd = np.maximum(d, 1e-6)[:, None]
    px = ex[:, None] + (tx - ex)[:, None] * t / dd
    py = ey[:, None] + (ty - ey)[:, None] * t / dd
    o, ob = _hindernis(welt, px, py, baum, baum_faktor)
    ez2 = ez[:, None]
    zreq = np.where(gueltig, ez2 + (o - ez2) * dd / t, -np.inf)
    z_min = zreq.max(axis=1) if m > 0 else np.full(n, -np.inf)
    if ob is not None and m > 0:
        zb = np.where(gueltig & np.isfinite(ob), ez2 + (np.where(np.isfinite(ob), ob, 0.0) - ez2) * dd / t, -np.inf)
        k = max(1, int(baum_block))
        if zb.shape[1] >= k:
            kte = -np.partition(-zb, k - 1, axis=1)[:, k - 1]
            z_min = np.maximum(z_min, kte)
    z_min = np.where(np.isfinite(z_min), z_min, ez)
    return z_min, d


def sichtanteil(welt, ex, ey, tx, ty, ziel_hoehe_m, augenhoehe_m=1.7, ziel_boden_m=None, **kw):
    """Sichtbarer Anteil (0..1) der Silhouette [Boden, Boden + ziel_hoehe_m] am Ziel von Augpunkten aus."""
    ex = np.atleast_1d(np.asarray(ex, np.float64))
    ey = np.atleast_1d(np.asarray(ey, np.float64))
    ez = welt.bilinear(welt.hoehe, ex, ey) + augenhoehe_m
    zb = welt.hoehe_bei_m(tx, ty) if ziel_boden_m is None else ziel_boden_m
    z_min, d = mindesthoehe(welt, ex, ey, ez, tx, ty, **kw)
    H = max(float(ziel_hoehe_m), 0.1)
    anteil = np.clip((zb + H - z_min) / H, 0.0, 1.0)
    return anteil, z_min, d


def sicht_von_wegen(welt, wp, x_m, y_m, ziel_hoehe_m, r_min_m=300.0, r_max_m=800.0, augenhoehe_m=1.7,
                    min_anteil=0.3, **kw):
    """Leuchtfeuer-Pruefung: von welchen Wegpunkten im Ring [r_min, r_max] ist die Silhouette lesbar?

    Rueckgabe dict: n_wegpunkte, n_sichtbar (Anteil >= min_anteil), anteil_wegpunkte, mittel_anteil,
    bester {x_m, y_m, z_m, abstand_m, anteil}, sichtbar_ab_m (groesster Abstand mit Sicht),
    idx, anteile (je Wegpunkt im Ring).
    """
    idx, d = wp.im_ring(x_m, y_m, r_min_m, r_max_m)
    out = {"n_wegpunkte": int(idx.size), "n_sichtbar": 0, "anteil_wegpunkte": 0.0, "mittel_anteil": 0.0,
           "bester": None, "sichtbar_ab_m": 0.0, "idx": idx, "anteile": np.zeros(0)}
    if not idx.size:
        return out
    anteil, _, dd = sichtanteil(welt, wp.x_m[idx], wp.y_m[idx], x_m, y_m, ziel_hoehe_m, augenhoehe_m, **kw)
    s = anteil >= min_anteil
    out["anteile"] = anteil
    out["n_sichtbar"] = int(s.sum())
    out["anteil_wegpunkte"] = float(s.mean())
    out["mittel_anteil"] = float(anteil.mean())
    if s.any():
        # bester: hoher Anteil, bei Gleichstand mittlerer Abstand (~500 m)
        sc = anteil - 0.0002 * np.abs(dd - 500.0)
        k = int(np.argmax(np.where(s, sc, -9)))
        kk = idx[k]
        out["bester"] = {"x_m": float(wp.x_m[kk]), "y_m": float(wp.y_m[kk]), "z_m": float(wp.z_m[kk]),
                         "abstand_m": float(dd[k]), "anteil": float(anteil[k])}
        out["sichtbar_ab_m"] = float(dd[s].max())
    return out


def verdeckt_vom_weg(welt, wp, x_m, y_m, ziel_hoehe_m=3.0, r_max_m=400.0, max_anteil=0.15,
                     augenhoehe_m=1.7, **kw):
    """Fundstueck-Pruefung: ist der Ort von keinem Wegpunkt bis r_max_m zu sehen?

    verdeckt = kein Wegpunkt sieht mehr als max_anteil der Silhouette. Rueckgabe dict mit naechster_sicht_m
    (Abstand des naechsten Wegpunkts, der mehr sieht) und n_sichtbar.
    """
    idx, d = wp.im_ring(x_m, y_m, 0.0, r_max_m)
    if not idx.size:
        return {"verdeckt": True, "max_anteil": 0.0, "n_sichtbar": 0, "n_wegpunkte": 0, "naechste_sicht_m": None}
    anteil, _, dd = sichtanteil(welt, wp.x_m[idx], wp.y_m[idx], x_m, y_m, ziel_hoehe_m, augenhoehe_m, **kw)
    s = anteil > max_anteil
    return {"verdeckt": not bool(s.any()), "max_anteil": float(anteil.max()), "n_sichtbar": int(s.sum()),
            "n_wegpunkte": int(idx.size), "naechste_sicht_m": float(dd[s].min()) if s.any() else None}


def beste_blickposition(welt, x_m, y_m, ziel_hoehe_m, r_min_m=30.0, r_max_m=150.0, n_richtungen=36,
                        n_ringe=6, augenhoehe_m=1.7, gel=None, max_neigung=32.0, bevorzugt_grad=None,
                        anzahl=5, **kw):
    """Sucht Kamerapositionen fuer den _held-Blick (Ringe um das Ziel).

    Bewertung: sichtbarer Anteil (Gewicht 1), leicht erhoeht bis +15 m (0,15), offenes Vorfeld
    (keine Baeume an der Kamera, 0,1), optional Naehe zu bevorzugt_grad (Blickrichtung Kamera -> Ziel in Grad,
    0 = Nord, 90 = Ost; 0,15). Ausgeschlossen: Wasser, Meer, Ort, Hang > max_neigung.
    Rueckgabe: Liste dict (x_m, y_m, z_m, abstand_m, richtung_grad, anteil, score), beste zuerst.
    """
    a = np.radians(np.arange(n_richtungen) * 360.0 / n_richtungen)
    r = np.linspace(r_min_m, r_max_m, n_ringe)
    A, R = np.meshgrid(a, r)
    # Richtung 'a' = Himmelsrichtung von der Kamera aus zum Ziel; Kamera liegt entgegengesetzt
    cx = x_m - np.sin(A).ravel() * R.ravel()
    cy = y_m + np.cos(A).ravel() * R.ravel()
    ok = welt.im_raster_m(cx, cy)
    cx, cy = cx[ok], cy[ok]
    ri = A.ravel()[ok]
    rr = R.ravel()[ok]
    i, j = welt.m_zu_ij(cx, cy)
    frei = (welt.wasser[i, j] == 0) & ~welt.meer[i, j] & (welt.ort[i, j] == 0)
    if gel is not None:
        frei &= gel.neigung[i, j] <= max_neigung
    else:
        e = 2.0 * welt.zelle_m
        gx = (welt.bilinear(welt.hoehe, cx + e, cy) - welt.bilinear(welt.hoehe, cx - e, cy)) / (2 * e)
        gy = (welt.bilinear(welt.hoehe, cx, cy + e) - welt.bilinear(welt.hoehe, cx, cy - e)) / (2 * e)
        frei &= np.degrees(np.arctan(np.hypot(gx, gy))) <= max_neigung
    if not frei.any():
        return []
    cx, cy, ri, rr, i, j = cx[frei], cy[frei], ri[frei], rr[frei], i[frei], j[frei]
    anteil, _, _ = sichtanteil(welt, cx, cy, x_m, y_m, ziel_hoehe_m, augenhoehe_m, **kw)
    zc = welt.hoehe[i, j].astype(np.float64)
    zt = welt.hoehe_bei_m(x_m, y_m)
    dz = zc - zt
    hoeher = np.clip(dz, 0, 15) / 15.0 - np.clip(-dz, 0, 30) / 60.0
    baum = welt.baeume_nativ[i, j] > 0
    sc = anteil + 0.15 * hoeher + 0.1 * (~baum)
    if bevorzugt_grad is not None:
        diff = np.abs(((np.degrees(ri) - bevorzugt_grad) + 180.0) % 360.0 - 180.0)
        sc += 0.15 * (1 - diff / 180.0)
    o = np.argsort(-sc, kind="stable")
    out = []
    for k in o[:max(1, anzahl)]:
        out.append({"x_m": float(cx[k]), "y_m": float(cy[k]), "z_m": float(zc[k]), "abstand_m": float(rr[k]),
                    "richtung_grad": float(np.degrees(ri[k]) % 360.0), "anteil": float(anteil[k]),
                    "score": float(sc[k])})
    return out


def richtung_grad(von_x, von_y, nach_x, nach_y):
    """Himmelsrichtung von -> nach in Grad (0 = Nord = -Y, 90 = Ost = +X)."""
    return float(np.degrees(np.arctan2(nach_x - von_x, -(nach_y - von_y))) % 360.0)


def zz_augenhoehe(welt, kx_m, ky_m, zx_m, zy_m, zz_m, hoch_cm=170, max_kipp_grad=20.0):
    """§8: Kamerahoehe = max(Boden + Hoch, ZZ + 3 m). Liegt das Ziel hoeher als die Kamera, hebt die Regel die
    Kamera an. Diese Hilfe senkt ZZ auf Boden_Kamera + Hoch - 3 m, solange sich die Blickrichtung dadurch
    hoechstens max_kipp_grad nach unten dreht (Ziel bleibt bei ~59 Grad vertikalem Bildwinkel im Bild).
    Sonst bleibt ZZ (Kamera wird nach §8 angehoben, der Pruefer meldet einen HINWEIS). Rueckgabe ZZ in m."""
    boden = welt.hoehe_bei_m(kx_m, ky_m)
    grenze = boden + hoch_cm / 100.0 - 3.0
    if zz_m <= grenze:
        return zz_m
    d = max(float(np.hypot(zx_m - kx_m, zy_m - ky_m)), 1e-3)
    if np.degrees(np.arctan2(zz_m - grenze, d)) <= max_kipp_grad:
        return grenze
    return zz_m


def kameras_vorschlagen(welt, wp, ort_id, x_m, y_m, art, ziel_hoehe_m, gel=None, pfad_m=None,
                        held=None, nah_abstand_m=10.0, sicht=None):
    """Kameras nach SEHENS_FORMAT §8: _anmarsch, _held, _nah (+ _fern fuer Leuchtfeuer).

    pfad_m: optional Zugangspfad [[x, y], ...] vom Weg zum Ort (aus kandidaten.erreichbarkeit) - die
    _anmarsch-Kamera steht dann dort, wo sich der Ort oeffnet (erste Stelle mit Anteil >= 0,5).
    sicht: Ergebnis von sicht_von_wegen (fuer _fern), sonst wird es berechnet (Leuchtfeuer).
    Rueckgabe: Liste [Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch] (cm, int).
    """
    from . import format as _fmt
    feld = _daten.feld_von_m(x_m, y_m)
    zt = welt.hoehe_bei_m(x_m, y_m)
    kams = []
    # _anmarsch
    ax = ay = None
    if pfad_m is not None and len(pfad_m) >= 2:
        from .gelaende import polylinie_proben
        px, py, s = polylinie_proben(np.asarray(pfad_m)[::-1], 4.0)  # vom Weg zum Ort
        dist = np.hypot(px - x_m, py - y_m)
        sel = dist >= 12.0
        if sel.any():
            an, _, _ = sichtanteil(welt, px[sel], py[sel], x_m, y_m, max(ziel_hoehe_m, 2.0))
            k = np.flatnonzero(an >= 0.5)
            kk = k[0] if k.size else int(np.argmax(an))
            ax, ay = float(px[sel][kk]), float(py[sel][kk])
    if ax is None:
        if art == "leuchtfeuer":
            idx, d = wp.im_ring(x_m, y_m, 60.0, 400.0)
            if idx.size:
                an, _, dd = sichtanteil(welt, wp.x_m[idx], wp.y_m[idx], x_m, y_m, ziel_hoehe_m)
                k = int(np.argmax(an - 0.001 * dd))
                ax, ay = float(wp.x_m[idx[k]]), float(wp.y_m[idx[k]])
        if ax is None:
            k, _ = wp.naechster(x_m, y_m)
            ax, ay = float(wp.x_m[k]), float(wp.y_m[k])
    zz = zz_augenhoehe(welt, ax, ay, x_m, y_m, zt + 1.0)
    kams.append(_fmt.kamera(feld, ax * 100, ay * 100, x_m * 100, y_m * 100, zz * 100,
                            ort_id + "_anmarsch", 170))
    # _held
    if held is None:
        bev = richtung_grad(ax, ay, x_m, y_m)
        hl = beste_blickposition(welt, x_m, y_m, ziel_hoehe_m, r_min_m=max(25.0, ziel_hoehe_m * 2.0),
                                 r_max_m=max(120.0, ziel_hoehe_m * 6.0), gel=gel, bevorzugt_grad=bev, anzahl=1)
        held = hl[0] if hl else {"x_m": ax, "y_m": ay}
    zz = zz_augenhoehe(welt, held["x_m"], held["y_m"], x_m, y_m, zt + min(1.5, 0.3 * ziel_hoehe_m))
    kams.append(_fmt.kamera(feld, held["x_m"] * 100, held["y_m"] * 100, x_m * 100, y_m * 100, zz * 100,
                            ort_id + "_held", 170))
    # _nah: auf der Linie Held -> Ziel, nah_abstand_m vor dem Ziel
    dx, dy = held["x_m"] - x_m, held["y_m"] - y_m
    L = max(np.hypot(dx, dy), 1e-6)
    nx_, ny_ = x_m + dx / L * nah_abstand_m, y_m + dy / L * nah_abstand_m
    kams.append(_fmt.kamera(feld, nx_ * 100, ny_ * 100, x_m * 100, y_m * 100, (zt + 0.5) * 100,
                            ort_id + "_nah", 170))
    # _fern
    if art == "leuchtfeuer":
        if sicht is None:
            sicht = sicht_von_wegen(welt, wp, x_m, y_m, ziel_hoehe_m)
        b = sicht.get("bester")
        if b is None:
            # notfalls Gelaendepunkt in 400 m mit bester Sicht
            hl = beste_blickposition(welt, x_m, y_m, ziel_hoehe_m, r_min_m=300, r_max_m=600, n_ringe=4,
                                     gel=gel, anzahl=1)
            b = hl[0] if hl else None
        if b is not None:
            zz = zz_augenhoehe(welt, b["x_m"], b["y_m"], x_m, y_m, zt + 1.0)
            kams.append(_fmt.kamera(feld, b["x_m"] * 100, b["y_m"] * 100, x_m * 100, y_m * 100,
                                    zz * 100, ort_id + "_fern", 170))
    return kams
