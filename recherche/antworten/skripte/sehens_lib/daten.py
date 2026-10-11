"""daten.py - Laden der Weltdaten (2 m PNG oder 1 m Original), Legende, Koordinaten, Fenster.

Koordinaten (vorlagen/FORMAT.md 1 und legende.json):
  1-m-Zelle (i, j): X_cm = (j - 4730,5) * 100, Y_cm = (i - 4060,5) * 100   (i = Zeile Nord->Sued, j = Spalte West->Ost)
  Raster mit Zellgroesse z (1, 2, 4 m): Pixel (iz, jz) deckt 1-m-Zellen z*iz ... z*iz+z-1; Mitte
      X_cm = (z*jz + (z-1)/2 - 4730,5) * 100, Y_cm = (z*iz + (z-1)/2 - 4060,5) * 100
  Felder A1..J7 je 1008 m: Spalte s = j // 1008 (A=0), Zeile r = i // 1008 + 1.
  Norden = kleine i = negatives Y. Meeresspiegel Z = 0.

Hauptfunktionen:
  welt = lade(daten2m=None, daten1m=None, pfade=True)   # Standard: vorlagen/daten/sehens (2 m)
  welt.hoehe, welt.biom, welt.boden, welt.weg, welt.ort, welt.wasser, welt.meer   (NY x NX, native Zelle)
  Pfade (Auftrag 13c, "pfade" in antworten/sehens/*/standorte.json, alle Biome): welt.weg = Wege + Pfade,
  welt.weg_basis = nur Wege, welt.pfade, welt.pfad_maske, welt.setze_pfade(liste); lade_pfade(ordner)
  welt.baeume4, welt.baumhoehe4  (4 m), welt.baumhoehe_nativ (auf native Zelle hochgerechnet)
  welt.m_zu_ij(x_m, y_m), welt.ij_zu_m(i, j), welt.cm_zu_ij, welt.ij_zu_cm
  welt.hoehe_bei_m(x_m, y_m) (bilinear), welt.baumhoehe_bei_m(x_m, y_m)
  welt.fenster(x_m, y_m, radius_m) -> Fenster (Ausschnitt mit Achsen)
  feld_von_m(x_m, y_m) -> "E5"; feld_grenzen_m("E5") -> (x0, y0, x1, y1)
"""

import json
import os

import numpy as np
from PIL import Image

from . import log

Image.MAX_IMAGE_PIXELS = None

# --- Konstanten -------------------------------------------------------------------------------
NX_1M = 9577
NY_1M = 7057
OFF_J = 4730.5
OFF_I = 4060.5
FELD_M = 1008
FELD_SPALTEN = "ABCDEFGHIJ"
FELD_ZEILEN = 7

BIOME = ["aue", "bergwald", "gletscher", "tundra", "canyon", "oedland", "heide", "elfenwald",
         "dschungel", "kueste", "wueste", "lava", "frost", "sumpf", "fjord"]
BIOM_MEER = 255
KLEINE_BIOME = ("canyon", "sumpf", "fjord", "kueste", "frost")
BODEN = ["Wiese", "Gras", "Trockengras", "Laub", "Nadeln", "Moos", "Heide", "Kraut", "Erde", "Lehm",
         "Schlamm", "Sand", "Kies", "Geroell", "Fels", "Felsplatte", "Sandstein", "Schnee", "Eis",
         "Lavafels", "Lavasand", "Algen"]
BODEN_KEINE = 255

# Welt-Grenzen in m (Rand der 1-m-Zellen)
X_MIN_M = (-0.5 - OFF_J)
X_MAX_M = (NX_1M - 0.5 - OFF_J)
Y_MIN_M = (-0.5 - OFF_I)
Y_MAX_M = (NY_1M - 0.5 - OFF_I)


def standard_pfad_2m():
    """vorlagen/daten/sehens relativ zu dieser Datei (antworten/skripte/sehens_lib -> Repo)."""
    hier = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(hier, "..", "..", "..", "vorlagen", "daten", "sehens"))


# --- Koordinaten (Modulebene, beliebige Zellgroesse) --------------------------------------------
def pixel_zu_m(i, j, zelle_m):
    """Pixelmitte (i, j) eines Rasters mit Zellgroesse zelle_m -> Welt (x_m, y_m). Arrays erlaubt."""
    z = float(zelle_m)
    i = np.asarray(i, dtype=np.float64)
    j = np.asarray(j, dtype=np.float64)
    return (z * j + (z - 1.0) / 2.0 - OFF_J), (z * i + (z - 1.0) / 2.0 - OFF_I)


def m_zu_pixel(x_m, y_m, zelle_m):
    """Welt (x_m, y_m) -> fraktionale Pixelkoordinate (i, j) (Pixelmitte = ganze Zahl)."""
    z = float(zelle_m)
    x_m = np.asarray(x_m, dtype=np.float64)
    y_m = np.asarray(y_m, dtype=np.float64)
    return (y_m + OFF_I - (z - 1.0) / 2.0) / z, (x_m + OFF_J - (z - 1.0) / 2.0) / z


def feld_von_m(x_m, y_m):
    """Gitterfeld ("E5") eines Weltpunkts in m; None ausserhalb."""
    j1 = int(np.floor(float(x_m) + OFF_J + 0.5))
    i1 = int(np.floor(float(y_m) + OFF_I + 0.5))
    if not (0 <= j1 < NX_1M and 0 <= i1 < NY_1M):
        return None
    s = j1 // FELD_M
    r = i1 // FELD_M + 1
    if s >= len(FELD_SPALTEN) or r > FELD_ZEILEN:
        return None
    return "%s%d" % (FELD_SPALTEN[s], r)


def feld_von_cm(x_cm, y_cm):
    return feld_von_m(float(x_cm) / 100.0, float(y_cm) / 100.0)


def feld_grenzen_m(feld):
    """(x0, y0, x1, y1) in m eines Felds (Rand der 1-m-Zellen; letzte Felder an Weltrand gekappt)."""
    s = FELD_SPALTEN.index(feld[0].upper())
    r = int(feld[1:])
    j0, j1 = s * FELD_M, min((s + 1) * FELD_M, NX_1M)
    i0, i1 = (r - 1) * FELD_M, min(r * FELD_M, NY_1M)
    return (j0 - 0.5 - OFF_J, i0 - 0.5 - OFF_I, j1 - 0.5 - OFF_J, i1 - 0.5 - OFF_I)


def felder_im_kreis(x_m, y_m, radius_m):
    """Alle Felder, die ein Kreis beruehrt (sortiert)."""
    out = set()
    for dx in (-radius_m, 0, radius_m):
        for dy in (-radius_m, 0, radius_m):
            f = feld_von_m(x_m + dx, y_m + dy)
            if f:
                out.add(f)
    return sorted(out)


def biom_code(name):
    return BIOME.index(name)


def biom_name(code):
    code = int(code)
    if code == BIOM_MEER:
        return "meer"
    return BIOME[code] if 0 <= code < len(BIOME) else "?"


def boden_name(code):
    code = int(code)
    if code == BODEN_KEINE:
        return "keine"
    return BODEN[code] if 0 <= code < len(BODEN) else "?"


def ist_kleines_biom(name):
    return name in KLEINE_BIOME


def _lese_json(pfad, pflicht=False):
    if not os.path.exists(pfad):
        if pflicht:
            raise FileNotFoundError("Datei fehlt: %s" % pfad)
        log("Hinweis: Datei fehlt (optional):", pfad)
        return None
    with open(pfad, "r", encoding="utf-8") as f:
        return json.load(f)


# --- Welt -------------------------------------------------------------------------------------
class Welt:
    """Alle Raster in nativer Zellgroesse (2 m oder 1 m) + Vektordaten.

    Raster (NY x NX): hoehe (float32, m), biom (uint8, 255 = Meer), boden (uint8, 255 = keine),
    weg, ort, wasser (uint8, > 0 = belegt). 4-m-Raster: baeume4 (Anzahl), baumhoehe4 (m).
    Vektoren: baeche, teiche, wasser_welt (dict), staedte (Liste mit x_m, y_m, radius_m, id, name, art).
    """

    def __init__(self, zelle_m, hoehe, biom, boden, weg, ort, wasser, baeume4, baumhoehe4,
                 baeche=None, teiche=None, wasser_welt=None, staedte=None, quelle=""):
        self.zelle_m = float(zelle_m)
        self.hoehe = hoehe
        self.biom = biom
        self._boden = boden
        self.weg = weg
        self.ort = ort
        self.wasser = wasser
        self.baeume4 = baeume4
        self.baumhoehe4 = baumhoehe4
        self.baeche = baeche or []
        self.teiche = teiche or []
        self.wasser_welt = wasser_welt or {}
        self.staedte = staedte or []
        self.quelle = quelle
        self.ny, self.nx = hoehe.shape
        self._meer = None
        self._baumhoehe_nativ = None
        self._baeume_nativ = None
        self._boden_lader = None
        # Pfade (standorte.json "pfade", alle Biome): weg_basis = Wegenetz ohne Pfade; weg = Wege + Pfade
        self.weg_basis = weg
        self.pfade = []
        self.pfad_maske = None
        self.pfade_kennung = ""
        self._weg_mit_pfaden = None

    # -- Pfade --
    def setze_pfade(self, pfade):
        """Rastert Pfade (Liste dict mit punkte_m/punkte_cm, breite_cm) zusaetzlich zum Wegenetz als Weg.
        weg_basis bleibt unveraendert; weg = weg_basis + Pfadzellen (Wert PFAD_WERT). Leere Liste -> Ursprung."""
        self.pfade = [normiere_pfad(p) for p in (pfade or [])]
        self.pfade = [p for p in self.pfade if p is not None]
        if not self.pfade:
            self.weg = self.weg_basis
            self.pfad_maske = None
            self.pfade_kennung = ""
            self._weg_mit_pfaden = None
            return self
        self.pfad_maske = pfad_maske(self, self.pfade)
        w = np.array(self.weg_basis, copy=True)
        w[self.pfad_maske & (w == 0)] = PFAD_WERT
        self.weg = w
        self._weg_mit_pfaden = w
        self.pfade_kennung = pfade_kennung(self.pfade)
        return self

    def pfade_aktiv(self):
        """True, wenn weg die gerasterten Pfade enthaelt (und nicht nachtraeglich ersetzt wurde)."""
        return bool(self.pfade) and self.weg is self._weg_mit_pfaden

    # -- abgeleitete Raster --
    @property
    def boden(self):
        if self._boden is None and self._boden_lader is not None:
            self._boden = self._boden_lader()
        return self._boden

    @property
    def meer(self):
        """Meer = Hoehe < 0 und kein Suesswasser (FORMAT.md 2, Korrektur 10.10.)."""
        if self._meer is None:
            self._meer = (self.hoehe < 0) & (self.wasser == 0)
        return self._meer

    def _vier_zu_nativ(self, a4):
        z = self.zelle_m
        ii = np.floor((z * np.arange(self.ny) + (z - 1) / 2.0) / 4.0).astype(np.int64)
        jj = np.floor((z * np.arange(self.nx) + (z - 1) / 2.0) / 4.0).astype(np.int64)
        ii = np.clip(ii, 0, a4.shape[0] - 1)
        jj = np.clip(jj, 0, a4.shape[1] - 1)
        return a4[ii][:, jj]

    @property
    def baumhoehe_nativ(self):
        """Baumhoehe (m) auf das native Raster hochgerechnet (naechster Nachbar)."""
        if self._baumhoehe_nativ is None:
            self._baumhoehe_nativ = self._vier_zu_nativ(self.baumhoehe4)
        return self._baumhoehe_nativ

    @property
    def baeume_nativ(self):
        if self._baeume_nativ is None:
            self._baeume_nativ = self._vier_zu_nativ(self.baeume4)
        return self._baeume_nativ

    # -- Koordinaten --
    def ij_zu_m(self, i, j):
        return pixel_zu_m(i, j, self.zelle_m)

    def ij_zu_cm(self, i, j):
        x, y = pixel_zu_m(i, j, self.zelle_m)
        return x * 100.0, y * 100.0

    def m_zu_ij(self, x_m, y_m, runden=True):
        """Welt m -> Pixel (i, j). runden=True: int-Index (gekappt auf Raster)."""
        i, j = m_zu_pixel(x_m, y_m, self.zelle_m)
        if not runden:
            return i, j
        i = np.clip(np.rint(i), 0, self.ny - 1).astype(np.int64)
        j = np.clip(np.rint(j), 0, self.nx - 1).astype(np.int64)
        if i.ndim == 0:
            return int(i), int(j)
        return i, j

    def cm_zu_ij(self, x_cm, y_cm, runden=True):
        return self.m_zu_ij(np.asarray(x_cm, dtype=np.float64) / 100.0,
                            np.asarray(y_cm, dtype=np.float64) / 100.0, runden)

    def im_raster_m(self, x_m, y_m):
        i, j = self.m_zu_ij(x_m, y_m, runden=False)
        return (i >= -0.5) & (i < self.ny - 0.5) & (j >= -0.5) & (j < self.nx - 0.5)

    def flat_index(self, i, j):
        return np.asarray(i, dtype=np.int64) * self.nx + np.asarray(j, dtype=np.int64)

    def flat_zu_m(self, idx):
        idx = np.asarray(idx, dtype=np.int64)
        return self.ij_zu_m(idx // self.nx, idx % self.nx)

    # -- Abfragen --
    def bilinear(self, a, x_m, y_m):
        """Bilineare Abfrage eines nativen Rasters an Weltpunkten (m)."""
        fi, fj = m_zu_pixel(x_m, y_m, self.zelle_m)
        fi = np.clip(fi, 0, self.ny - 1.000001)
        fj = np.clip(fj, 0, self.nx - 1.000001)
        i0 = np.floor(fi).astype(np.int64)
        j0 = np.floor(fj).astype(np.int64)
        di = fi - i0
        dj = fj - j0
        a00 = a[i0, j0]
        a01 = a[i0, j0 + 1]
        a10 = a[i0 + 1, j0]
        a11 = a[i0 + 1, j0 + 1]
        r = (a00 * (1 - di) * (1 - dj) + a01 * (1 - di) * dj + a10 * di * (1 - dj) + a11 * di * dj)
        return r

    def naechster(self, a, x_m, y_m):
        i, j = self.m_zu_ij(x_m, y_m)
        return a[i, j]

    def hoehe_bei_m(self, x_m, y_m):
        r = self.bilinear(self.hoehe, x_m, y_m)
        return float(r) if np.ndim(r) == 0 else r

    def hoehe_bei_cm(self, x_cm, y_cm):
        """Bodenhoehe in cm an Weltpunkt in cm."""
        r = self.bilinear(self.hoehe, np.asarray(x_cm) / 100.0, np.asarray(y_cm) / 100.0) * 100.0
        return float(r) if np.ndim(r) == 0 else r

    def baumhoehe_bei_m(self, x_m, y_m):
        i4, j4 = m_zu_pixel(x_m, y_m, 4.0)
        i4 = np.clip(np.rint(i4), 0, self.baumhoehe4.shape[0] - 1).astype(np.int64)
        j4 = np.clip(np.rint(j4), 0, self.baumhoehe4.shape[1] - 1).astype(np.int64)
        r = self.baumhoehe4[i4, j4]
        return float(r) if np.ndim(r) == 0 else r

    def biom_bei_m(self, x_m, y_m):
        return biom_name(self.naechster(self.biom, x_m, y_m))

    def boden_bei_m(self, x_m, y_m):
        return boden_name(self.naechster(self.boden, x_m, y_m))

    def feld(self, x_m, y_m):
        return feld_von_m(x_m, y_m)

    def biom_maske(self, name):
        return self.biom == biom_code(name)

    def fenster(self, x_m, y_m, radius_m):
        return Fenster(self, x_m, y_m, radius_m)

    def fenster_box(self, x0_m, y0_m, x1_m, y1_m):
        """Fenster aus Weltrechteck (m)."""
        cx, cy = (x0_m + x1_m) / 2.0, (y0_m + y1_m) / 2.0
        f = Fenster(self, cx, cy, 0.0)
        i0, j0 = self.m_zu_ij(x0_m, y0_m)
        i1, j1 = self.m_zu_ij(x1_m, y1_m)
        f._setze(min(i0, i1), min(j0, j1), max(i0, i1) + 1, max(j0, j1) + 1)
        return f

    # -- Vektoren --
    def staedte_m(self):
        """Arrays (x_m, y_m, radius_m) der geplanten Staedte/Orte aus standorte.json."""
        if not self.staedte:
            return np.zeros(0), np.zeros(0), np.zeros(0)
        x = np.array([s["x_m"] for s in self.staedte], dtype=np.float64)
        y = np.array([s["y_m"] for s in self.staedte], dtype=np.float64)
        r = np.array([s["radius_m"] for s in self.staedte], dtype=np.float64)
        return x, y, r

    def info(self):
        return ("Welt %s: %d x %d Zellen a %.0f m (%.1f x %.1f km), Hoehe %.1f..%.1f m, "
                "%d Baeche, %d Teiche, %d Fluesse, %d Seen, %d Staedte"
                % (self.quelle, self.nx, self.ny, self.zelle_m, self.nx * self.zelle_m / 1000.0,
                   self.ny * self.zelle_m / 1000.0, float(self.hoehe.min()), float(self.hoehe.max()),
                   len(self.baeche), len(self.teiche), len(self.wasser_welt.get("fluesse", [])),
                   len(self.wasser_welt.get("seen", [])), len(self.staedte)))


class Fenster:
    """Rechteckiger Ausschnitt (native Zellen) um einen Punkt.

    f.sl            (slice, slice) fuer native Raster
    f.i0, f.j0, f.hoehe_px, f.breite_px
    f.get(name)     Ausschnitt eines Welt-Rasters ("hoehe", "weg", "baumhoehe_nativ", ...) oder eines
                    beliebigen gleich grossen Arrays: f.get(array)
    f.x_m, f.y_m    1D-Achsen (Pixelmitten), f.gitter_m() -> 2D (X, Y)
    f.lokal(x_m, y_m) -> fraktionale (i, j) im Fenster
    """

    def __init__(self, welt, x_m, y_m, radius_m):
        self.welt = welt
        self.mx, self.my = float(x_m), float(y_m)
        r_px = int(np.ceil(radius_m / welt.zelle_m))
        ci, cj = welt.m_zu_ij(x_m, y_m)
        self._setze(ci - r_px, cj - r_px, ci + r_px + 1, cj + r_px + 1)

    def _setze(self, i0, j0, i1, j1):
        w = self.welt
        self.i0 = int(max(0, i0))
        self.j0 = int(max(0, j0))
        self.i1 = int(min(w.ny, i1))
        self.j1 = int(min(w.nx, j1))
        self.hoehe_px = self.i1 - self.i0
        self.breite_px = self.j1 - self.j0
        self.sl = (slice(self.i0, self.i1), slice(self.j0, self.j1))
        self.x_m = pixel_zu_m(0, np.arange(self.j0, self.j1), w.zelle_m)[0]
        self.y_m = pixel_zu_m(np.arange(self.i0, self.i1), 0, w.zelle_m)[1]

    def get(self, name):
        if isinstance(name, str):
            return getattr(self.welt, name)[self.sl]
        return name[self.sl]

    def gitter_m(self):
        return np.meshgrid(self.x_m, self.y_m)

    def lokal(self, x_m, y_m):
        i, j = self.welt.m_zu_ij(x_m, y_m, runden=False)
        return i - self.i0, j - self.j0

    def grenzen_m(self):
        z = self.welt.zelle_m / 2.0
        return (self.x_m[0] - z, self.y_m[0] - z, self.x_m[-1] + z, self.y_m[-1] + z)

    def fenster_ij_1m(self):
        """[i0, j0, hoehe, breite] im 1-m-Raster (fuer orte.json 'fenster_ij')."""
        z = int(round(self.welt.zelle_m))
        return [self.i0 * z, self.j0 * z, self.hoehe_px * z, self.breite_px * z]


# --- Laden ------------------------------------------------------------------------------------
def _png(pfad, pflicht=True):
    if not os.path.exists(pfad):
        if pflicht:
            raise FileNotFoundError("Datei fehlt: %s" % pfad)
        return None
    return np.array(Image.open(pfad))


def _staedte_aus_json(d):
    out = []
    if not d:
        return out
    for o in d.get("orte", []):
        u = o.get("unreal_cm")
        if not u:
            continue
        out.append({"id": o.get("id"), "name": o.get("name"), "art": o.get("art"),
                    "x_m": float(u[0]) / 100.0, "y_m": float(u[1]) / 100.0,
                    "radius_m": float(o.get("radius_m", 0) or 0), "biom": o.get("rezept")})
    return out


def _vektoren(baeche_pfad, teiche_pfad, wasser_pfad, standorte_pfad):
    b = _lese_json(baeche_pfad) if baeche_pfad else None
    t = _lese_json(teiche_pfad) if teiche_pfad else None
    w = _lese_json(wasser_pfad) if wasser_pfad else None
    s = _lese_json(standorte_pfad) if standorte_pfad else None
    return ((b or {}).get("baeche", []), (t or {}).get("teiche", []), w or {}, _staedte_aus_json(s))


def lade_2m(ordner=None):
    """Laedt die 2-m-PNGs aus vorlagen/daten/sehens (oder ordner)."""
    ordner = ordner or standard_pfad_2m()
    if not os.path.isdir(ordner):
        raise FileNotFoundError("Ordner fehlt: %s" % ordner)
    p = lambda n: os.path.join(ordner, n)
    v = _png(p("hoehe_2m.png"))
    hoehe = (300.0 + (v.astype(np.float32) - 32768.0) / 64.0).astype(np.float32)
    biom = _png(p("biom_2m.png")).astype(np.uint8)
    boden = _png(p("boden_2m.png")).astype(np.uint8)
    weg = _png(p("weg_2m.png")).astype(np.uint8)
    ort = _png(p("ort_2m.png")).astype(np.uint8)
    wasser = _png(p("wasser_2m.png")).astype(np.uint8)
    b4 = _png(p("baeume_4m.png"), pflicht=False)
    bh4 = _png(p("baumhoehe_4m.png"), pflicht=False)
    ny4, nx4 = (NY_1M + 3) // 4, (NX_1M + 3) // 4
    if b4 is None:
        log("Hinweis: baeume_4m.png fehlt -> keine Baeume")
        b4 = np.zeros((ny4, nx4), np.uint8)
    if bh4 is None:
        bh4 = np.zeros((ny4, nx4), np.uint8)
    for n, a in (("biom", biom), ("boden", boden), ("weg", weg), ("ort", ort), ("wasser", wasser)):
        if a.shape != hoehe.shape:
            raise ValueError("Rastergroesse %s %s != hoehe %s" % (n, a.shape, hoehe.shape))
    baeche, teiche, ww, st = _vektoren(p("baeche_alle.json"), p("teiche.json"), p("wasser_welt.json"),
                                       p("standorte.json"))
    return Welt(2.0, hoehe, biom, boden, weg, ort, wasser, b4.astype(np.uint8), bh4.astype(np.uint8),
                baeche, teiche, ww, st, quelle="2m:" + ordner)


def _r8(pfad, ny, nx, pflicht=True):
    if not os.path.exists(pfad):
        if pflicht:
            raise FileNotFoundError("Datei fehlt: %s" % pfad)
        return None
    a = np.fromfile(pfad, dtype=np.uint8)
    if a.size != ny * nx:
        raise ValueError("%s: %d Bytes, erwartet %d" % (pfad, a.size, ny * nx))
    return a.reshape(ny, nx)


def lade_1m(ordner, daten2m=None, standorte_pfad=None, boden=True):
    """Laedt die 1-m-Originale (export/unreal/welt): hoehe.f32, karte_*.r8, eigner.r8 + welt.json, lage_*.r8.

    Baeume gibt es nur in 4 m: aus daten2m (baeume_4m.png, baumhoehe_4m.png), falls angegeben/vorhanden.
    boden: True -> vorherrschende Lage (argmax lage_*.r8) wird beim ersten Zugriff blockweise berechnet.
    """
    if not os.path.isdir(ordner):
        raise FileNotFoundError("Ordner fehlt: %s" % ordner)
    p = lambda *n: os.path.join(ordner, *n)
    wj = _lese_json(p("welt.json")) or {}
    nx = int(wj.get("nx", wj.get("NX", NX_1M)))
    ny = int(wj.get("ny", wj.get("NY", NY_1M)))
    h = np.fromfile(p("hoehe.f32"), dtype="<f4")
    if h.size != nx * ny:
        raise ValueError("hoehe.f32: %d Werte, erwartet %d" % (h.size, nx * ny))
    hoehe = h.reshape(ny, nx).astype(np.float32)
    weg = _r8(p("karte_weg.r8"), ny, nx)
    ort = _r8(p("karte_ort.r8"), ny, nx)
    wasser = _r8(p("karte_wasser.r8"), ny, nx)
    # Biom aus eigner.r8 + welt.json["kacheln"][k]["rezept"]
    eig = _r8(p("eigner.r8"), ny, nx, pflicht=False)
    lut = np.zeros(256, np.uint8)  # 0 = aue (Weltgelaende)
    kach = wj.get("kacheln", {})
    items = kach.items() if isinstance(kach, dict) else enumerate(kach)
    for k, v in items:
        try:
            k = int(k)
        except (TypeError, ValueError):
            k = int(v.get("id", -1)) if isinstance(v, dict) else -1
        if not (0 <= k < 256) or not isinstance(v, dict):
            continue
        rz = str(v.get("rezept", "aue")).lower()
        if rz in BIOME:
            lut[k] = BIOME.index(rz)
        elif "vulkan" in rz or "lava" in rz:
            lut[k] = BIOME.index("lava")
        else:
            lut[k] = 0
    biom = lut[eig] if eig is not None else np.zeros((ny, nx), np.uint8)
    meer = (hoehe < 0) & (wasser == 0)
    biom[meer] = BIOM_MEER
    # Baeume (4 m) aus dem 2-m-Ordner
    d2 = daten2m or standard_pfad_2m()
    b4 = _png(os.path.join(d2, "baeume_4m.png"), pflicht=False)
    bh4 = _png(os.path.join(d2, "baumhoehe_4m.png"), pflicht=False)
    ny4, nx4 = (ny + 3) // 4, (nx + 3) // 4
    if b4 is None or bh4 is None:
        log("Hinweis: keine baeume_4m/baumhoehe_4m gefunden -> Sicht ohne Baeume")
        b4 = np.zeros((ny4, nx4), np.uint8)
        bh4 = np.zeros((ny4, nx4), np.uint8)
    # Vektoren
    bae = p("baeche", "baeche.json")
    baeche, teiche, ww, _ = _vektoren(bae, p("teiche", "teiche.json"), p("wasser_welt.json"), None)
    if os.path.exists(p("baeche", "baeche_r2.json")):
        b2 = _lese_json(p("baeche", "baeche_r2.json")) or {}
        baeche = list(baeche) + list(b2.get("baeche", []))
    if standorte_pfad is None:
        standorte_pfad = os.path.normpath(p("..", "..", "..", "docs", "staedte", "standorte.json"))
        if not os.path.exists(standorte_pfad):
            standorte_pfad = os.path.join(d2, "standorte.json")
    st = _staedte_aus_json(_lese_json(standorte_pfad))
    w = Welt(1.0, hoehe, biom, None, weg, ort, wasser, b4.astype(np.uint8), bh4.astype(np.uint8),
             baeche, teiche, ww, st, quelle="1m:" + ordner)
    w._meer = meer
    if boden:
        w._boden_lader = lambda: _boden_1m(ordner, ny, nx)
    else:
        w._boden = np.full((ny, nx), BODEN_KEINE, np.uint8)
    return w


def _boden_1m(ordner, ny, nx, block=512):
    """Vorherrschende Lage = argmax ueber lage_<Name>.r8 (blockweise, speichersparend)."""
    maps = []
    for k, n in enumerate(BODEN):
        pf = os.path.join(ordner, "lage_%s.r8" % n)
        if os.path.exists(pf):
            maps.append((k, np.memmap(pf, dtype=np.uint8, mode="r", shape=(ny, nx))))
    log("Boden 1 m: argmax ueber %d Lagen ..." % len(maps))
    out = np.full((ny, nx), BODEN_KEINE, np.uint8)
    if not maps:
        log("Hinweis: keine lage_*.r8 gefunden -> Boden 'keine'")
        return out
    codes = np.array([k for k, _ in maps], np.uint8)
    for i0 in range(0, ny, block):
        st = np.stack([m[i0:i0 + block] for _, m in maps])
        am = st.argmax(axis=0)
        mx = st.max(axis=0)
        o = codes[am]
        o[mx == 0] = BODEN_KEINE
        out[i0:i0 + block] = o
    return out


def lade(daten2m=None, daten1m=None, pfade=True, **kw):
    """Einheitlicher Einstieg: daten1m gesetzt -> 1-m-Originale, sonst 2-m-PNGs (Standardordner).

    pfade: True (Standard) = Pfade aller Biome aus antworten/sehens/*/standorte.json ("pfade") als Wege
    rastern; Ordnername = Pfade aus diesem sehens-Ordner; Liste = diese Pfade; False/None = ohne Pfade
    (altes Verhalten). Ohne Pfade in den Dateien ist das Ergebnis identisch zum alten Verhalten."""
    if daten1m:
        w = lade_1m(daten1m, daten2m=daten2m, **kw)
    else:
        w = lade_2m(daten2m)
    if pfade:
        liste = pfade if isinstance(pfade, (list, tuple)) else lade_pfade(
            pfade if isinstance(pfade, str) else None)
        w.setze_pfade(liste)
        if w.pfade:
            log("Pfade als Wege gerastert: %d (%s)" % (len(w.pfade), ", ".join(p["id"] for p in w.pfade)))
    return w


# --- Pfade (Auftrag 13c: standorte.json "pfade") ------------------------------------------------
PFAD_ARTEN = ("trampelpfad", "serpentine", "trittsteine")
PFAD_WERT = 255           # Rasterwert der Pfadzellen in welt.weg (> 0 = Weg)


def standard_pfad_sehens():
    """antworten/sehens relativ zu dieser Datei."""
    hier = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(hier, "..", "..", "sehens"))


def normiere_pfad(p, biom=None, quelle=""):
    """Pfad-Eintrag -> dict mit id, biom, art, breite_cm, punkte_m [[x, y], ...] (+ Originalfelder).
    Ungueltige Eintraege (keine id, < 2 Punkte) -> None."""
    if not isinstance(p, dict):
        return None
    if "punkte_m" in p and p.get("_normiert"):
        return p
    pts = p.get("punkte_cm")
    if pts is not None:
        try:
            pm = [[float(q[0]) / 100.0, float(q[1]) / 100.0] for q in pts]
        except (TypeError, ValueError, IndexError):
            return None
    else:
        try:
            pm = [[float(q[0]), float(q[1])] for q in (p.get("punkte_m") or [])]
        except (TypeError, ValueError, IndexError):
            return None
    if not isinstance(p.get("id"), str) or len(pm) < 2:
        return None
    out = dict(p)
    out.update({"id": p["id"], "biom": p.get("biom") or biom, "art": p.get("art"),
                "breite_cm": p.get("breite_cm", 150), "punkte_m": pm, "quelle": quelle or p.get("quelle", ""),
                "_normiert": True})
    return out


def lade_pfade(sehens_ordner=None):
    """Alle Pfade aus <sehens_ordner>/*/standorte.json (Schluessel "pfade" auf oberster Ebene).
    Rueckgabe Liste normierter dicts (id, biom, art, breite_cm, punkte_m, fuer, anschluss, quelle)."""
    import glob
    ordner = sehens_ordner or standard_pfad_sehens()
    out = []
    for pf in sorted(glob.glob(os.path.join(ordner, "*", "standorte.json"))):
        try:
            with open(pf, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception as ex:  # defekte Datei -> Pruefer meldet; hier weiter
            log("Hinweis: %s nicht lesbar (%s) - Pfade daraus fehlen" % (pf, ex))
            continue
        biom = d.get("biom") or os.path.basename(os.path.dirname(pf))
        for p in d.get("pfade") or []:
            n = normiere_pfad(p, biom=biom, quelle=pf)
            if n is None:
                log("Hinweis: ungueltiger Pfad in %s uebersprungen" % pf)
                continue
            out.append(n)
    return out


def pfade_kennung(pfade):
    """Kurzer Hash ueber Geometrie und Breite aller Pfade (Cache-Schluessel)."""
    import hashlib
    h = hashlib.sha1()
    for p in sorted(pfade, key=lambda q: q["id"]):
        h.update(json.dumps([p["id"], p.get("breite_cm"), [[round(a, 2), round(b, 2)] for a, b in p["punkte_m"]]])
                 .encode())
    return h.hexdigest()[:10]


def polylinie_dichte(punkte_m, schritt_m):
    """Gleichmaessige Proben entlang einer Polylinie (inkl. Ecken) -> (x, y) Arrays."""
    P = np.asarray(punkte_m, np.float64)[:, :2]
    xs, ys = [P[0, 0]], [P[0, 1]]
    for a, b in zip(P[:-1], P[1:]):
        L = float(np.hypot(*(b - a)))
        n = max(1, int(np.ceil(L / schritt_m)))
        t = np.arange(1, n + 1) / n
        xs.extend(a[0] + (b[0] - a[0]) * t)
        ys.extend(a[1] + (b[1] - a[1]) * t)
    return np.asarray(xs), np.asarray(ys)


def pfad_maske(welt, pfade):
    """Bool-Raster (native Zelle) aller Pfadzellen: Mittellinie dicht abgetastet, Band breite_cm."""
    m = np.zeros((welt.ny, welt.nx), bool)
    z = welt.zelle_m
    for p in pfade:
        x, y = polylinie_dichte(p["punkte_m"], z / 2.0)
        r = max(0, int(np.floor((float(p.get("breite_cm") or 150) / 200.0) / z)))
        i, j = welt.m_zu_ij(x, y)
        for di in range(-r, r + 1):
            for dj in range(-r, r + 1):
                if di * di + dj * dj <= r * r:
                    m[np.clip(i + di, 0, welt.ny - 1), np.clip(j + dj, 0, welt.nx - 1)] = True
    return m


def argumente_hinzufuegen(parser):
    """Fuegt --daten2m / --daten1m / --cache zu einem argparse-Parser hinzu."""
    parser.add_argument("--daten2m", default=None, help="Ordner mit den 2-m-PNGs (vorlagen/daten/sehens)")
    parser.add_argument("--daten1m", default=None, help="Ordner export/unreal/welt (1-m-Originale)")
    parser.add_argument("--cache", default=None, help="Cache-Ordner fuer Ganze-Welt-Rechnungen (.npy)")
    return parser
