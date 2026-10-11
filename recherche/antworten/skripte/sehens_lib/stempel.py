"""stempel.py - Gelaendestempel (gelaende/<id>.f32) und Bodenlagen (lagen/<id>_<Lage>.r8), SEHENS_FORMAT §3.

Gerechnet wird im nativen Raster der Welt (2 m im Cloud-Test, 1 m lokal); geschrieben wird IMMER im 1-m-Raster
(Fenster fenster_ij in 1-m-Zellen, bilinear hochgerechnet), damit die Dateien zu orte.json passen.

Gelaende:
  st = Stempel.um(welt, x_m, y_m, breite_m, hoehe_m=None, rand_m=8)      # oder Stempel(welt, x0, y0, x1, y1)
  Werkzeuge (alle mit weichem Rand 'rand_m' und 'modus'):
    st.mulde(x, y, radius_m, tiefe_m, rand_m=6, boden=0.4, streckung=(1, 1), richtung_grad=0)
    st.kuppe(x, y, radius_m, hoehe_m, rand_m=6, plateau=0.2, streckung, richtung_grad)
    st.rinne(punkte_m, breite_m, tiefe_m, rand_m=3, sohle_z=None)          # sohle_z=(z_anfang, z_ende): Sohle absolut, fallend
    st.terrasse(x, y, radius_m, ziel_z, rand_m=6, streckung, richtung_grad) # Plateau auf absolute Hoehe
    st.abbruch(kante_m, hoehe_m, breite_m=4, reichweite_m=25, seite="links", verteilung="oben")
    st.glaetten(x, y, radius_m, staerke=1, sigma_m=3, rand_m=4)
    st.buckel(x, y, radius_m, amplitude_m, wellenlaenge_m=8, rand_m=6)    # buckelig (Halde, Blockfeld)
    st.see_becken(x, y, a_m, b_m, richtung_grad, spiegel_z, tiefe_m, ufer_m=6, freibord_m=0.5) -> Umriss (gegen Uhrzeigersinn)
  modus: "add" (Standard, relativ), "min" (nur absenken), "max" (nur anheben), "setzen" (Ziel beidseitig).
  Blending mit dem Bestand: min/max/setzen arbeiten gegen die AKTUELLE Hoehe (Bestand + bisherige Werkzeuge) -
  vorhandenes Gelaende bleibt, wo es schon tiefer (Mulde) bzw. hoeher (Schwelle) liegt.
  st.schuetzen(weg_m=3, wasser=True, uebergang_m=4)   # keine Aenderung <= 3 m an Wegen/bestehendem Wasser (§3)
  st.fertig()  -> Rand Delta = 0 (weicher Uebergang >= 8 m), Schutz; danach st.max_aenderung_m
  st.hoehe_bei_m(x, y), st.normale_bei_m(x, y), st.hang_grad_bei_m(x, y)    # Boden NACH dem Stempel (§4)
  st.senken(min_tiefe_m=0.3, wasser=None) -> geschlossene Senken ohne Wasser (Pruefung §3)
  st.schreibe(ordner, ort_id) -> orte.json-Block {"datei", "fenster_ij", "max_aenderung_m"}
Grenzen (§3): |Delta| <= 40 m nur Richtwert - Ferat (11.10.) erlaubt mehr, dann 'begruendung' setzen (Pruefer: HINWEIS).

Bodenlagen:
  lg = Lagen(welt, x0, y0, x1, y1)  oder  Lagen.um(...);  lg.setze(name, gewicht_0_255) (max-Kombination)
  lg.kreis(name, x, y, r_m, wert, rand_m=3, flecken=0.0, streckung, richtung_grad, innen_r_m=0)  (Ring mit innen_r_m)
  lg.band(name, punkte_m, breite_m, wert, rand_m=1, flecken=0.0)       # Pfad-Bodenband, Ufer, Rinnen
  lg.maske(name, w01, wert)                                             # beliebige Gewichtsmaske 0..1 im Fenster
  lg.schreibe(ordner, ort_id) -> orte.json-Block {"datei_praefix", "fenster_ij", "lagen"}
  Namen exakt wie FORMAT.md §2; weiche Raender >= 3 m, 'flecken' 0..1 macht das Muster fleckig statt kreisrund.
"""

import os
import zlib

import numpy as np

from . import log
from . import daten as _daten
from . import gelaende as _gel

LAGEN = tuple(_daten.BODEN)


# ============================================================================================
# Hilfen
# ============================================================================================
def kompass_vektor(grad):
    """Kompassrichtung (0 = Nord = -Y, 90 = Ost = +X) -> Einheitsvektor (dx, dy) in Weltkoordinaten."""
    a = np.radians(grad)
    return float(np.sin(a)), float(-np.cos(a))


def vektor_kompass(dx, dy):
    return float(np.degrees(np.arctan2(dx, -dy)) % 360.0)


def glatt01(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def abfall(d, innen, aussen):
    """1 fuer d <= innen, weicher Kosinus-Abfall auf 0 bei d >= aussen."""
    if aussen <= innen:
        return (d <= innen).astype(np.float64)
    t = np.clip((d - innen) / (aussen - innen), 0.0, 1.0)
    return 0.5 * (1.0 + np.cos(np.pi * t))


def rauschen(X, Y, wellenlaenge_m, seed=0, oktaven=2):
    """Deterministisches Wert-Rauschen (-1..1) auf Weltkoordinaten (m) - fuer fleckige Lagen und Buckel."""
    out = np.zeros(np.shape(X), np.float64)
    amp, summe = 1.0, 0.0
    X = np.asarray(X, np.float64)
    Y = np.asarray(Y, np.float64)
    for o in range(oktaven):
        w = wellenlaenge_m / (2 ** o)
        gx, gy = X / w, Y / w
        x0, y0 = np.floor(gx), np.floor(gy)
        fx, fy = glatt01(gx - x0), glatt01(gy - y0)

        def h(a, b):
            v = (a.astype(np.int64) * 73856093) ^ (b.astype(np.int64) * 19349663) ^ (int(seed) * 83492791 + o * 2654435761)
            v = (v ^ (v >> 13)) * 1274126177
            v = v ^ (v >> 16)
            return ((v & 0xFFFF) / 32767.5) - 1.0

        n = (h(x0, y0) * (1 - fx) * (1 - fy) + h(x0 + 1, y0) * fx * (1 - fy) +
             h(x0, y0 + 1) * (1 - fx) * fy + h(x0 + 1, y0 + 1) * fx * fy)
        out += amp * n
        summe += amp
        amp *= 0.5
    return out / summe


def ellipsen_abstand(X, Y, x, y, radius_m, streckung=(1.0, 1.0), richtung_grad=0.0):
    """'Radius-Abstand' (m) zu (x, y): Ellipse mit Halbachsen radius*streckung[0] entlang richtung_grad und
    radius*streckung[1] quer; Rueckgabe so skaliert, dass der Ellipsenrand den Wert radius_m hat."""
    ux, uy = kompass_vektor(richtung_grad)
    dx, dy = X - x, Y - y
    a = dx * ux + dy * uy
    b = -dx * uy + dy * ux
    sa, sb = float(streckung[0]), float(streckung[1])
    return np.hypot(a / sa, b / sb)


def polylinie_abstand(X, Y, punkte_m):
    """Abstand (m) zur Polylinie, Bogenlaenge s des Fusspunkts, vorzeichenbehafteter Seitenabstand
    (> 0 links in Laufrichtung, Karte mit Norden oben) - Arrays wie X."""
    P = np.asarray(punkte_m, np.float64)[:, :2]
    X = np.asarray(X, np.float64)
    Y = np.asarray(Y, np.float64)
    best = np.full(X.shape, np.inf)
    s_out = np.zeros(X.shape)
    seite = np.zeros(X.shape)
    kum = 0.0
    if len(P) == 1:
        return np.hypot(X - P[0, 0], Y - P[0, 1]), s_out, seite
    for a, b in zip(P[:-1], P[1:]):
        ab = b - a
        L2 = max(float((ab ** 2).sum()), 1e-12)
        L = np.sqrt(L2)
        t = np.clip(((X - a[0]) * ab[0] + (Y - a[1]) * ab[1]) / L2, 0.0, 1.0)
        px, py = a[0] + t * ab[0], a[1] + t * ab[1]
        d = np.hypot(X - px, Y - py)
        m = d < best
        best = np.where(m, d, best)
        s_out = np.where(m, kum + t * L, s_out)
        # links in Laufrichtung (Norden oben, Y nach Sueden): n_links = (dy, -dx)
        sd = ((X - a[0]) * ab[1] - (Y - a[1]) * ab[0]) / L
        seite = np.where(m, sd, seite)
        kum += L
    return best, s_out, seite


def polylinie_laenge(punkte_m):
    P = np.asarray(punkte_m, np.float64)[:, :2]
    return float(np.hypot(*np.diff(P, axis=0).T).sum()) if len(P) > 1 else 0.0


def nach_1m(a, zelle_m):
    """Natives Fensterraster (z m) -> 1-m-Raster (z*h x z*w), bilinear an den 1-m-Zellmitten."""
    z = int(round(zelle_m))
    if z == 1:
        return np.asarray(a, np.float64)
    h, w = a.shape
    fi = np.clip((np.arange(z * h) - (z - 1) / 2.0) / z, 0, h - 1)
    fj = np.clip((np.arange(z * w) - (z - 1) / 2.0) / z, 0, w - 1)
    i0 = np.minimum(np.floor(fi).astype(np.int64), h - 2 if h > 1 else 0)
    j0 = np.minimum(np.floor(fj).astype(np.int64), w - 2 if w > 1 else 0)
    di = (fi - i0)[:, None]
    dj = (fj - j0)[None, :]
    i1 = np.minimum(i0 + 1, h - 1)
    j1 = np.minimum(j0 + 1, w - 1)
    a = np.asarray(a, np.float64)
    return (a[i0][:, j0] * (1 - di) * (1 - dj) + a[i0][:, j1] * (1 - di) * dj +
            a[i1][:, j0] * di * (1 - dj) + a[i1][:, j1] * di * dj)


def _fenster_aus_box(welt, x0, y0, x1, y1):
    return welt.fenster_box(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def _bilinear_fenster(a, fe, welt, x_m, y_m, aussen=0.0):
    """Bilineare Abfrage eines Fenster-Arrays an Weltpunkten; ausserhalb -> aussen."""
    fi, fj = fe.lokal(np.asarray(x_m, np.float64), np.asarray(y_m, np.float64))
    fi = np.asarray(fi, np.float64)
    fj = np.asarray(fj, np.float64)
    h, w = a.shape
    innen = (fi >= 0) & (fi <= h - 1) & (fj >= 0) & (fj <= w - 1)
    fi_c = np.clip(fi, 0, max(h - 1.000001, 0))
    fj_c = np.clip(fj, 0, max(w - 1.000001, 0))
    i0 = np.floor(fi_c).astype(np.int64)
    j0 = np.floor(fj_c).astype(np.int64)
    i1 = np.minimum(i0 + 1, h - 1)
    j1 = np.minimum(j0 + 1, w - 1)
    di, dj = fi_c - i0, fj_c - j0
    r = (a[i0, j0] * (1 - di) * (1 - dj) + a[i0, j1] * (1 - di) * dj + a[i1, j0] * di * (1 - dj) +
         a[i1, j1] * di * dj)
    return np.where(innen, r, aussen)


# ============================================================================================
# Gelaendestempel
# ============================================================================================
class Stempel:
    MODI = ("add", "min", "max", "setzen")

    def __init__(self, welt, x0_m, y0_m, x1_m, y1_m, rand_m=8.0, seed=0):
        self.welt = welt
        self.fe = _fenster_aus_box(welt, x0_m, y0_m, x1_m, y1_m)
        self.z = welt.zelle_m
        self.h0 = self.fe.get("hoehe").astype(np.float64)
        self.delta = np.zeros_like(self.h0)
        self.X, self.Y = self.fe.gitter_m()
        self.rand_m = float(rand_m)
        self.seed = int(seed)
        self.protokoll = []
        self.ist_fertig = False
        self.max_aenderung_m = 0.0
        self.begruendung = ""
        self.ist_wasser = False

    @classmethod
    def um(cls, welt, x_m, y_m, breite_m, hoehe_m=None, rand_m=8.0, seed=0):
        hoehe_m = breite_m if hoehe_m is None else hoehe_m
        return cls(welt, x_m - breite_m / 2.0, y_m - hoehe_m / 2.0, x_m + breite_m / 2.0, y_m + hoehe_m / 2.0,
                   rand_m=rand_m, seed=seed)

    # -- Zugriff --
    @property
    def aktuell(self):
        return self.h0 + self.delta

    def hoehe_bei_m(self, x_m, y_m):
        """Bodenhoehe (m) NACH dem Stempel (Welt bilinear + Delta bilinear; ausserhalb nur Welt)."""
        h = self.welt.bilinear(self.welt.hoehe, np.asarray(x_m, np.float64), np.asarray(y_m, np.float64))
        d = _bilinear_fenster(self.delta, self.fe, self.welt, x_m, y_m, 0.0)
        r = h + d
        return float(r) if np.ndim(r) == 0 else r

    def normale_bei_m(self, x_m, y_m, schritt_m=None):
        """Gelaendenormale (nx, ny, nz) nach dem Stempel (Differenzen +-schritt, Standard = Zelle)."""
        s = float(schritt_m or max(1.0, self.z))
        x = np.asarray(x_m, np.float64)
        y = np.asarray(y_m, np.float64)
        dzx = (self.hoehe_bei_m(x + s, y) - self.hoehe_bei_m(x - s, y)) / (2 * s)
        dzy = (self.hoehe_bei_m(x, y + s) - self.hoehe_bei_m(x, y - s)) / (2 * s)
        n = np.stack([-np.asarray(dzx), -np.asarray(dzy), np.ones_like(np.asarray(dzx, np.float64))], axis=-1)
        return n / np.linalg.norm(n, axis=-1, keepdims=True)

    def hang_grad_bei_m(self, x_m, y_m):
        n = self.normale_bei_m(x_m, y_m)
        return np.degrees(np.arccos(np.clip(n[..., 2], -1, 1)))

    def hangab_grad_bei_m(self, x_m, y_m, radius_m=6.0):
        """Kompassrichtung hangab (gemittelt ueber radius_m)."""
        s = float(radius_m)
        dzx = self.hoehe_bei_m(x_m + s, y_m) - self.hoehe_bei_m(x_m - s, y_m)
        dzy = self.hoehe_bei_m(x_m, y_m + s) - self.hoehe_bei_m(x_m, y_m - s)
        return vektor_kompass(-dzx, -dzy)

    def enthaelt(self, x_m, y_m):
        x0, y0, x1, y1 = self.fe.grenzen_m()
        return (x0 <= x_m <= x1) and (y0 <= y_m <= y1)

    # -- Kern --
    def _anwenden(self, w, rel=None, ziel=None, modus="add", name=""):
        if modus not in self.MODI:
            raise ValueError("modus %r (add/min/max/setzen)" % modus)
        if self.ist_fertig:
            raise RuntimeError("Stempel ist schon fertig() - keine Werkzeuge mehr")
        cur = self.h0 + self.delta
        if rel is not None:
            neu = cur + np.asarray(rel, np.float64) * w
        else:
            neu = cur + w * (np.asarray(ziel, np.float64) - cur)
        if modus == "min":
            neu = np.minimum(cur, neu)
        elif modus == "max":
            neu = np.maximum(cur, neu)
        self.delta = neu - self.h0
        if name:
            self.protokoll.append(name)

    def mulde(self, x, y, radius_m, tiefe_m, rand_m=6.0, boden=0.4, streckung=(1.0, 1.0), richtung_grad=0.0,
              modus="add", ziel_z=None):
        """Mulde: tiefe_m relativ (add) oder bis auf absolute Sohle ziel_z (modus min). boden: Anteil flacher Sohle."""
        d = ellipsen_abstand(self.X, self.Y, x, y, radius_m, streckung, richtung_grad)
        w = abfall(d, boden * radius_m, radius_m + rand_m)
        if ziel_z is not None:
            self._anwenden(w, ziel=float(ziel_z), modus="min" if modus == "add" else modus, name="mulde")
        else:
            self._anwenden(w, rel=-abs(tiefe_m), modus=modus, name="mulde")

    def kuppe(self, x, y, radius_m, hoehe_m, rand_m=6.0, plateau=0.2, streckung=(1.0, 1.0), richtung_grad=0.0,
              modus="add"):
        d = ellipsen_abstand(self.X, self.Y, x, y, radius_m, streckung, richtung_grad)
        w = abfall(d, plateau * radius_m, radius_m + rand_m)
        self._anwenden(w, rel=abs(hoehe_m), modus=modus, name="kuppe")

    def rinne(self, punkte_m, breite_m, tiefe_m, rand_m=3.0, sohle_z=None, modus="add"):
        """Rinne entlang Polylinie: Querprofil flach auf breite/2, weicher Rand. sohle_z=(z0, z1): Sohle absolut,
        linear entlang der Linie (nur absenken)."""
        d, s, _ = polylinie_abstand(self.X, self.Y, punkte_m)
        w = abfall(d, breite_m / 2.0, breite_m / 2.0 + rand_m)
        if sohle_z is not None:
            L = max(polylinie_laenge(punkte_m), 1e-6)
            z = sohle_z[0] + (sohle_z[1] - sohle_z[0]) * np.clip(s / L, 0, 1)
            self._anwenden(w, ziel=z, modus="min", name="rinne")
        else:
            self._anwenden(w, rel=-abs(tiefe_m), modus=modus, name="rinne")

    def terrasse(self, x, y, radius_m, ziel_z, rand_m=6.0, streckung=(1.0, 1.0), richtung_grad=0.0, modus="setzen"):
        d = ellipsen_abstand(self.X, self.Y, x, y, radius_m, streckung, richtung_grad)
        w = abfall(d, radius_m, radius_m + rand_m)
        self._anwenden(w, ziel=float(ziel_z), modus=modus, name="terrasse")

    def abbruch(self, kante_m, hoehe_m, breite_m=4.0, reichweite_m=25.0, seite="links", verteilung="oben",
                modus="add"):
        """Gelaendestufe an einer Kante (Polylinie): Seite 'links'/'rechts' (Laufrichtung, Norden oben) wird
        hoeher. verteilung: 'oben' (nur anheben), 'unten' (nur absenken), 'beide' (+-hoehe/2).
        Steile Zone breite_m, Wirkung klingt bis reichweite_m ab."""
        d, _, sd = polylinie_abstand(self.X, self.Y, kante_m)
        if seite == "rechts":
            sd = -sd
        t = glatt01((sd + breite_m / 2.0) / max(breite_m, 1e-6))
        if verteilung == "oben":
            prof = t
        elif verteilung == "unten":
            prof = t - 1.0
        else:
            prof = t - 0.5
        g = abfall(d, max(reichweite_m * 0.4, breite_m), reichweite_m)
        self._anwenden(g, rel=hoehe_m * prof, modus=modus, name="abbruch")

    def glaetten(self, x, y, radius_m, staerke=1.0, sigma_m=3.0, rand_m=4.0):
        cur = self.h0 + self.delta
        gl = _gel.glaetten(cur.astype(np.float32), max(0.5, sigma_m / self.z)).astype(np.float64)
        d = np.hypot(self.X - x, self.Y - y)
        w = abfall(d, radius_m, radius_m + rand_m) * float(staerke)
        self._anwenden(w, ziel=gl, modus="setzen", name="glaetten")

    def buckel(self, x, y, radius_m, amplitude_m, wellenlaenge_m=8.0, rand_m=6.0, streckung=(1.0, 1.0),
               richtung_grad=0.0, seed=None):
        d = ellipsen_abstand(self.X, self.Y, x, y, radius_m, streckung, richtung_grad)
        w = abfall(d, radius_m, radius_m + rand_m)
        n = rauschen(self.X, self.Y, wellenlaenge_m, self.seed if seed is None else seed)
        self._anwenden(w, rel=amplitude_m * n, modus="add", name="buckel")

    def see_becken(self, x, y, a_m, b_m, richtung_grad, spiegel_z, tiefe_m, ufer_m=6.0, freibord_m=0.5,
                   boden=0.45, n_umriss=48, auslass_grad=None, auslass_sektor_grad=35.0, lippe_m=1.5):
        """Seebecken mit Ufer rundum ueber dem Spiegel (§5): innen Sohle bis spiegel - tiefe (nur absenken),
        aussen Uferring auf >= spiegel + freibord (nur anheben): volles Freibord bis plateau_m (in Metern hinter
        der Uferlinie), weicher Auslauf bis ufer_m. auslass_grad: Kompassrichtung des Abflusses - dort nur eine
        schmale Lippe (lippe_m, Freibord 0,05 m) statt eines Damms; der Abfluss-Bach beginnt an der Lippe.
        Rueckgabe: Umriss [[x, y], ...] in m, gegen den Uhrzeigersinn (Flaeche > 0 in X/Y)."""
        r = max(a_m, b_m)
        st = (a_m / r, b_m / r)
        d = ellipsen_abstand(self.X, self.Y, x, y, r, st, richtung_grad) / r      # 1 = Uferlinie
        innen = d < 1.0
        prof = abfall(d, boden, 1.0)
        sohle = spiegel_z - tiefe_m * prof - 0.05 * (1.0 - d)          # leicht unter dem Spiegel bis zum Ufer
        w_in = innen.astype(np.float64)
        self._anwenden(w_in, ziel=np.where(innen, sohle, 0.0), modus="min", name="see_becken")
        # metrischer Abstand hinter der Uferlinie (entlang des Strahls von der Mitte)
        pd = np.hypot(self.X - x, self.Y - y)
        m = np.where(d > 1.0, pd * (1.0 - 1.0 / np.maximum(d, 1e-6)), 0.0)
        plateau_m = np.full(d.shape, max(0.5 * ufer_m, 2.5 * self.z + 0.5))
        aus_m = np.full(d.shape, max(ufer_m, plateau_m.max() + 2.0))
        fb = np.full(d.shape, float(freibord_m))
        if auslass_grad is not None:
            lippe_m = max(float(lippe_m), 2.0 * self.z + 0.5)      # mind. 2 Zellen, sonst verwischt die Lippe
            g = np.degrees(np.arctan2(self.X - x, -(self.Y - y))) % 360.0
            dg = np.abs((g - auslass_grad + 180.0) % 360.0 - 180.0)
            im_auslass = dg <= auslass_sektor_grad
            plateau_m = np.where(im_auslass, lippe_m, plateau_m)
            aus_m = np.where(im_auslass, lippe_m + 1.5, aus_m)
            fb = np.where(im_auslass, 0.05, fb)
        ring = (d >= 1.0) & (m < aus_m)
        ufer_ziel = spiegel_z + fb * glatt01(m / 0.6)
        auslauf = 0.5 * (1.0 + np.cos(np.pi * np.clip((m - plateau_m) / np.maximum(aus_m - plateau_m, 1e-6), 0, 1)))
        w_r = np.where(ring, np.where(m <= plateau_m, 1.0, auslauf), 0.0)
        self._anwenden(w_r, ziel=ufer_ziel, modus="max", name="see_ufer")
        ux, uy = kompass_vektor(richtung_grad)
        t = np.linspace(0, 2 * np.pi, n_umriss, endpoint=False)
        pa, pb = a_m * np.cos(t), b_m * np.sin(t)
        px = x + pa * ux - pb * uy
        py = y + pa * uy + pb * ux
        um = [[float(u), float(v)] for u, v in zip(px, py)]
        if flaeche(um) < 0:
            um = um[::-1]
        return um

    # -- Schutz / Abschluss --
    def schuetzen(self, weg_m=3.0, wasser=True, uebergang_m=4.0, ausnahme_maske=None):
        """Keine Aenderung <= weg_m an Wegen (welt.weg inkl. Pfade) und an bestehendem Suesswasser (wasser=True),
        ausser in ausnahme_maske (der Ort IST dieses Wasser)."""
        m = self.fe.get("weg") > 0
        if wasser:
            m = m | (self.fe.get("wasser") > 0)
        if ausnahme_maske is not None:
            m = m & ~ausnahme_maske
        if not m.any():
            return
        d = _gel.abstand(m, self.z, max_m=weg_m + uebergang_m + 5.0)
        w = glatt01((d - weg_m) / max(uebergang_m, 1e-6))
        self.delta *= w
        self.protokoll.append("schutz")

    def randfaktor(self):
        """0 am Fensterrand (mind. 2 Zellen), weich auf 1 nach rand_m (>= 8 m)."""
        h, w = self.delta.shape
        ii = np.arange(h)[:, None]
        jj = np.arange(w)[None, :]
        dz = np.minimum(np.minimum(ii, h - 1 - ii), np.minimum(jj, w - 1 - jj)).astype(np.float64) * self.z
        return glatt01((dz - 2 * self.z) / max(self.rand_m, 8.0))

    def fertig(self, schutz=True, weg_m=3.0, wasser=True, ausnahme_maske=None):
        if self.ist_fertig:
            return self
        if schutz:
            self.schuetzen(weg_m=weg_m, wasser=wasser, ausnahme_maske=ausnahme_maske)
        self.delta *= self.randfaktor()
        self.delta[np.abs(self.delta) < 0.005] = 0.0
        self.max_aenderung_m = float(np.abs(self.delta).max()) if self.delta.size else 0.0
        self.ist_fertig = True
        return self

    def leer(self):
        return self.max_aenderung_m < 0.01

    def senken(self, min_tiefe_m=0.3, wasser=None, min_flaeche_m2=8.0):
        """Geschlossene Senken (gefuellt - Boden > min_tiefe) im Fenster, die nicht in 'wasser' (bool-Maske
        im Fenster, geplantes + bestehendes Wasser) liegen. Rueckgabe dict(flaeche_m2, max_tiefe_m, maske)."""
        cur = (self.h0 + self.delta).astype(np.float32)
        r = _gel.abfluss(cur, self.z, np.zeros(cur.shape, bool))
        tief = r["gefuellt"] - cur
        m = tief > min_tiefe_m
        nur_neu = m.copy()
        if wasser is not None:
            nur_neu &= ~wasser
        nur_neu &= (self.fe.get("wasser") == 0)
        # nur Senken, die der Stempel erzeugt/vertieft hat (Delta < 0 oder Rand angehoben)
        nur_neu &= (np.abs(self.delta) > 0.05) | (_gel.max_filter(np.abs(self.delta).astype(np.float32), 3) > 0.05)
        fl = float(nur_neu.sum() * self.z * self.z)
        return {"flaeche_m2": fl if fl >= min_flaeche_m2 else 0.0,
                "max_tiefe_m": float(tief[nur_neu].max()) if nur_neu.any() else 0.0, "maske": nur_neu}

    def schreibe(self, ordner, ort_id, begruendung=None):
        """gelaende/<id>.f32 (1 m, Delta in m) -> Block fuer orte.json. Leerer Stempel -> None (nichts schreiben)."""
        if not self.ist_fertig:
            self.fertig()
        if self.leer():
            return None
        a = nach_1m(self.delta, self.z).astype("<f4")
        rel = "gelaende/%s.f32" % ort_id
        pf = os.path.join(ordner, rel)
        os.makedirs(os.path.dirname(pf), exist_ok=True)
        np.ascontiguousarray(a).tofile(pf)
        blk = {"datei": rel, "fenster_ij": [int(v) for v in self.fe.fenster_ij_1m()],
               "max_aenderung_m": round(float(np.abs(a).max()), 2)}
        if begruendung or self.begruendung:
            blk["begruendung"] = begruendung or self.begruendung
        if self.ist_wasser:
            blk["ist_wasser"] = True      # §3: der Ort IST das bestehende Wasser (Aenderung dort erlaubt)
        blk["werkzeuge"] = sorted(set(self.protokoll))
        return blk


def flaeche(umriss):
    """Vorzeichenbehaftete Flaeche (Schnuersenkel) in X/Y; > 0 = gegen den Uhrzeigersinn im Sinne von
    SEHENS_FORMAT §5 / wasser_welt.json."""
    u = np.asarray(umriss, np.float64)[:, :2]
    if len(u) < 3:
        return 0.0
    x, y = u[:, 0], u[:, 1]
    return 0.5 * float((x * np.roll(y, -1) - np.roll(x, -1) * y).sum())


# ============================================================================================
# Bodenlagen
# ============================================================================================
class Lagen:
    def __init__(self, welt, x0_m, y0_m, x1_m, y1_m, seed=0):
        self.welt = welt
        self.fe = _fenster_aus_box(welt, x0_m, y0_m, x1_m, y1_m)
        self.z = welt.zelle_m
        self.X, self.Y = self.fe.gitter_m()
        self.ziel = {}
        self.seed = int(seed)

    @classmethod
    def um(cls, welt, x_m, y_m, breite_m, hoehe_m=None, seed=0):
        hoehe_m = breite_m if hoehe_m is None else hoehe_m
        return cls(welt, x_m - breite_m / 2.0, y_m - hoehe_m / 2.0, x_m + breite_m / 2.0, y_m + hoehe_m / 2.0, seed)

    def _flecken(self, w, flecken, flecken_m, name):
        if flecken <= 0:
            return w
        n = rauschen(self.X, self.Y, flecken_m, self.seed + zlib.crc32(name.encode()) % 9973)
        # Rand aufbrechen: Schwelle steigt nach aussen
        return np.clip(w * (1.0 + flecken * 1.6 * n) - flecken * 0.35 * (1.0 - w), 0.0, 1.0)

    def setze(self, name, wert_0_255):
        if name not in LAGEN:
            raise ValueError("Bodenlage %r unbekannt (FORMAT.md §2: %s)" % (name, ", ".join(LAGEN)))
        a = np.clip(np.asarray(wert_0_255, np.float64), 0, 255)
        self.ziel[name] = np.maximum(self.ziel.get(name, np.zeros_like(a)), a)

    def maske(self, name, w01, wert, flecken=0.0, flecken_m=6.0):
        w = self._flecken(np.clip(np.asarray(w01, np.float64), 0, 1), flecken, flecken_m, name)
        self.setze(name, w * float(wert))

    def kreis(self, name, x, y, r_m, wert, rand_m=3.0, flecken=0.0, flecken_m=6.0, streckung=(1.0, 1.0),
              richtung_grad=0.0, innen_r_m=0.0):
        d = ellipsen_abstand(self.X, self.Y, x, y, r_m, streckung, richtung_grad)
        w = abfall(d, r_m, r_m + max(rand_m, 3.0))
        if innen_r_m > 0:
            w = w * (1.0 - abfall(d, max(innen_r_m - max(rand_m, 3.0), 0.0), innen_r_m))
        self.maske(name, w, wert, flecken, flecken_m)

    def band(self, name, punkte_m, breite_m, wert, rand_m=1.0, flecken=0.0, flecken_m=4.0):
        d, _, _ = polylinie_abstand(self.X, self.Y, punkte_m)
        w = abfall(d, breite_m / 2.0, breite_m / 2.0 + rand_m)
        self.maske(name, w, wert, flecken, flecken_m)

    def namen(self):
        return [n for n in LAGEN if n in self.ziel and float(self.ziel[n].max()) >= 1.0]

    def schreibe(self, ordner, ort_id):
        """lagen/<id>_<Lage>.r8 (1 m) -> Block fuer orte.json; ohne Lagen -> None."""
        namen = self.namen()
        if not namen:
            return None
        rel = "lagen/%s_" % ort_id
        for n in namen:
            a = nach_1m(self.ziel[n], self.z)
            pf = os.path.join(ordner, rel + n + ".r8")
            os.makedirs(os.path.dirname(pf), exist_ok=True)
            np.ascontiguousarray(np.clip(np.rint(a), 0, 255).astype(np.uint8)).tofile(pf)
        return {"datei_praefix": rel, "fenster_ij": [int(v) for v in self.fe.fenster_ij_1m()], "lagen": namen}
