#!/usr/bin/env python3
"""felsdeckung_plan.py - Referenzplaner Auftrag 21 (Felsdeckung je Neigung und Zone), Pilot B5-Ost.

Kurz: teilt das Gelaende im Pilotfenster in Zonen (Wand >= 50 Grad, Schrofen 38-50, Halde 26-40 unter Waenden,
Hangfuss 12-26, Hangwald, Tal, Grat, Sperre) und plant je Zone Netze im FORMAT-§3-Setzerformat:
  halde_<Feld>        Schutt-Teppich (flache Scan-Bodenplatten) + Bloecke 0,8-9 m (Fall-Sortierung, Potenzgesetz)
  klippenband_<Feld>  Felsbaender entlang der Schichtlinien (Schrofen), Wandreihen (Reihenlogik klippen_plan 2.1),
                      Gratkronen, 1 Turmklotz je Front (Akteur)
  platten_<Feld>      Platten 3-10 m am Hangfuss, eingegraben, mit Fugenbewuchs (Gras/Farn/Moos)
  baumgruppen_<Feld>  Nadelbaum-Gruppen 3-8 in 3 Hoehenklassen, Fussblock je Baum, Latschen, Totholz
Dazu Bodenlagen (Geroell/Fels/Felsplatte), Grasdichte-Maske, Ausduenn-Maske fuer den Altbestand und optional
(Variante B) einen Hoehenplan im A15-Format (Schuettkegel an Rinnenausgaengen).

Aufruf (Repo-Wurzel, Cloud 2-m-Daten):
  python -I recherche/antworten/skripte/felsdeckung/felsdeckung_plan.py --aus recherche/antworten/felsdeckung --bild
Lokal mit 1-m-Daten:
  python -I .../felsdeckung_plan.py --daten1m export/unreal/welt --aus export/unreal/welt/felsdeckung --bild
Variante B (Instanzen auf dem Gelaende NACH den Schuettkegeln):
  python -I .../felsdeckung_plan.py --gelaende --aus <ordner_b>

Regeln: felsdeckung_regeln.json (gleicher Ordner). Kein Unreal-Import. Deterministisch (Zufall nur aus crc32 von
Schluesseln, keine Zeitstempel). Quellen: siehe antworten/21-detailgrad-landschaft-felsdeckung.md.
"""

import argparse
import json
import math
import os
import sys
import time
import zlib

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
SKRIPTE = os.path.normpath(os.path.join(HIER, ".."))
if SKRIPTE not in sys.path:
    sys.path.insert(0, SKRIPTE)

from sehens_lib import daten as D          # noqa: E402
from sehens_lib import gelaende as G       # noqa: E402
from sehens_lib import instanzen as INS    # noqa: E402
from sehens_lib import inventar as INV     # noqa: E402
from sehens_lib import stempel as ST       # noqa: E402

STAND = "2026-10-13 (Auftrag 21, Entwurf 1)"
THEMEN = {"halde": "HALDE", "klippenband": "KBAND", "platten": "PLATTE", "baumgruppen": "BGRP"}
ZONEN = {"tal": 0, "fuss": 1, "hangwald": 2, "halde": 3, "schrofen": 4, "wand": 5, "sperre": 9}


def log(*t):
    s = " ".join(str(x) for x in t)
    sys.stdout.write(s.encode("ascii", "replace").decode("ascii") + "\n")
    sys.stdout.flush()


# ============================================================================================
# Zufall (deterministisch, nur aus Schluesseln)
# ============================================================================================
def u01(*keys):
    return zlib.crc32(("|".join(str(k) for k in keys)).encode("ascii")) / 4294967296.0


def u_bereich(lo_hi, *keys):
    lo, hi = lo_hi
    return lo + (hi - lo) * u01(*keys)


def hash01_arr(i, j, salt):
    """Vektorisiert: gleichverteilte Zahl je (i, j) - 64-bit-Mischung (splitmix-artig)."""
    v = (np.asarray(i, np.uint64) * np.uint64(0x9E3779B97F4A7C15)) ^ (np.asarray(j, np.uint64) * np.uint64(0xC2B2AE3D27D4EB4F))
    v = v ^ np.uint64((int(salt) * 0x165667B19E3779F9) & 0xFFFFFFFFFFFFFFFF)
    v = (v ^ (v >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    v = (v ^ (v >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    v = v ^ (v >> np.uint64(31))
    return (v >> np.uint64(11)).astype(np.float64) / float(1 << 53)


def potenz_d(lo, hi, a, u):
    """Inverse CDF eines abgeschnittenen Potenzgesetzes N(>d) ~ d^-a auf [lo, hi]."""
    la, ha = lo ** (-a), hi ** (-a)
    return (la - u * (la - ha)) ** (-1.0 / a)


def kompass(dx, dy):
    return float(math.degrees(math.atan2(dx, -dy)) % 360.0)


# ============================================================================================
# Netze
# ============================================================================================
class Netze:
    def __init__(self, inv, regeln):
        self.inv = inv
        self.info = {}
        self.fehler = []
        for pal, namen in regeln["paletten"].items():
            if pal.startswith("_"):
                continue
            for n in namen:
                b = inv.netz_pruefen(n, wildnis=True)
                if any(s == INV.FEHLER for s, _ in b):
                    self.fehler.append("%s: %s" % (n, "; ".join(t for _, t in b)))
                    continue
                self.info[n] = inv.netz(n)
        self.wuerfel_v = float(regeln.get("wuerfel_verhaeltnis", 1.4))

    def g(self, n):
        return self.info[n]["groesse_m"]

    def form(self, n):
        x, y, z = self.g(n)
        lang, kurz = max(x, y, z), max(min(x, y, z), 1e-3)
        if z >= max(x, y) * 0.999:
            return "stehend"
        if lang / kurz < self.wuerfel_v:
            return "wuerfel"
        if z <= 0.5 * max(x, y):
            return "plattig"
        return "laenglich"


# ============================================================================================
# Kontext: Fenster, Zonen, Felder
# ============================================================================================
class Kontext:
    def __init__(self, welt, regeln, delta=None):
        self.welt = welt
        self.R = regeln
        P = regeln["pilot"]
        self.feld = P["feld"]
        x0, y0, x1, y1 = P["fenster_m"]
        self.fenster_m = (x0, y0, x1, y1)
        rand = float(P["rand_m"])
        self.fe = welt.fenster_box(x0 - rand, y0 - rand, x1 + rand, y1 + rand)
        self.z = float(welt.zelle_m)
        z = self.z
        h = self.fe.get("hoehe").astype(np.float64)
        if delta is not None:
            h = h + delta
        self.h = h
        Z = regeln["zonen"]
        self.X, self.Y = self.fe.gitter_m()
        n_roh = G.hangneigung(h, z).astype(np.float64)
        gx, gy = G.gradient(h, z)
        self.n, self.gx, self.gy = n_roh, gx.astype(np.float64), gy.astype(np.float64)
        # Zonen aus geglaetteter Neigung (Kasten +-glaettung_m), sonst flackern Halde/Schrofen im 1-2-m-Rauschen
        n = G.box_mittel(n_roh.astype(np.float32), max(1, int(round(Z.get("glaettung_m", 3.0) / z)))).astype(np.float64)
        self.n_zone = n
        rp = max(1, int(round(Z["wand_relief_radius_m"] / z)))
        rel = G.max_filter(h.astype(np.float32), rp) - G.min_filter(h.astype(np.float32), rp)
        wand = (n >= Z["wand_grad"]) & (rel >= Z["wand_relief_m"])
        rp2 = max(1, int(round(20.0 / z)))
        rel2 = G.max_filter(h.astype(np.float32), rp2) - G.min_filter(h.astype(np.float32), rp2)
        self.wand_hoch = wand & (rel2 >= Z["wand_hoch_relief_m"])
        self.d_wand = G.abstand(wand, z, 400.0).astype(np.float64)
        kr = max(1, int(round(Z["halde_wandhoehe_radius_m"] / z)))
        hw = G.box_mittel((h * wand).astype(np.float32), kr)
        cw = G.box_mittel(wand.astype(np.float32), kr)
        mw = np.where(cw > 1e-6, hw / np.maximum(cw, 1e-6), 1e9)
        unter = h < mw
        g0, g1 = Z["halde_grad"]
        halde = (n >= g0) & (n < g1) & (self.d_wand <= Z["halde_max_abstand_wand_m"]) & unter & ~wand
        s0, s1 = Z["schrofen_grad"]
        schrofen = (n >= s0) & (n < s1) & ~halde & ~wand
        self.d_halde = G.abstand(halde, z, 400.0).astype(np.float64)
        f0, f1 = Z["fuss_grad"]
        fuss = (n >= f0) & (n < f1) & ((self.d_wand <= Z["fuss_max_abstand_wand_m"]) | (self.d_halde <= 40.0))
        self.fuss_nah = fuss & ((self.d_wand <= Z["fuss_nah_m"]) | (self.d_halde <= Z["fuss_nah_m"]))
        w0, w1 = Z["hangwald_grad"]
        hangwald = (n >= w0) & (n < w1) & ~halde & ~schrofen & ~wand
        self.t_halde = np.clip(self.d_wand / Z["halde_max_abstand_wand_m"], 0.0, 1.0)
        self.grat = (G.tpi(h.astype(np.float32), z, Z["grat_tpi_radius_m"]) >= Z["grat_tpi_min_m"]) & (n >= 10.0)
        self.d_grat = G.abstand(self.grat, z, 400.0).astype(np.float64)
        # Sperren
        S = Z["sperre"]
        wasser = (self.fe.get("wasser") > 0) | self.fe.get("meer")
        self.d_wasser = G.abstand(wasser, z, 400.0).astype(np.float64)
        self.d_weg = G.abstand(self.fe.get("weg") > 0, z, 400.0).astype(np.float64)
        self.d_ort = G.abstand(self.fe.get("ort") > 0, z, 400.0).astype(np.float64)
        sperre = (self.d_wasser < S["wasser_m"]) | (self.d_weg < S["weg_m"]) | (self.d_ort < S["ort_m"]) | \
            self.fe.get("meer") | (h <= 0.2)
        self.uebergang = (~sperre) & (self.d_wasser < S["wasser_uebergang_m"])
        zone = np.full(h.shape, ZONEN["tal"], np.uint8)
        zone[fuss] = ZONEN["fuss"]
        zone[hangwald] = ZONEN["hangwald"]
        zone[schrofen] = ZONEN["schrofen"]
        zone[halde] = ZONEN["halde"]
        zone[wand] = ZONEN["wand"]
        zone[sperre] = ZONEN["sperre"]
        self.zone = zone
        # Fenster-Innen (nur hier wird gesetzt)
        self.innen = (self.X >= x0) & (self.X < x1) & (self.Y >= y0) & (self.Y < y1)
        # Rauschen
        RS = regeln["rauschen"]
        sd = int(regeln["seed"])
        self.n_kegel = ST.rauschen(self.X, self.Y, RS["kegel_wellenlaenge_m"], sd + 11)
        self.n_luecke = ST.rauschen(self.X, self.Y, RS["luecken_wellenlaenge_m"], sd + 23)
        self.n_baum = ST.rauschen(self.X, self.Y, RS["baum_wellenlaenge_m"], sd + 37)
        # Schichtfunktion
        sch = regeln["schichtung"]
        a = math.radians(sch["streichen_grad"])
        self.f_schicht = h - math.tan(math.radians(sch["fallen_grad"])) * (self.X * math.cos(a) + self.Y * math.sin(a))

    # --- Abfragen an Weltpunkten (m) ------------------------------------------------------------
    def _ij(self, x, y):
        fi, fj = self.fe.lokal(np.asarray(x, np.float64), np.asarray(y, np.float64))
        return np.asarray(fi, np.float64), np.asarray(fj, np.float64)

    def bilinear(self, a, x, y):
        fi, fj = self._ij(x, y)
        h, w = a.shape
        fi = np.clip(fi, 0, h - 1.000001)
        fj = np.clip(fj, 0, w - 1.000001)
        i0 = np.floor(fi).astype(np.int64)
        j0 = np.floor(fj).astype(np.int64)
        di, dj = fi - i0, fj - j0
        r = (a[i0, j0] * (1 - di) * (1 - dj) + a[i0 + 1, j0] * di * (1 - dj) + a[i0, j0 + 1] * (1 - di) * dj +
             a[i0 + 1, j0 + 1] * di * dj)
        return float(r) if np.ndim(r) == 0 else r

    def naechst(self, a, x, y):
        fi, fj = self._ij(x, y)
        h, w = a.shape
        i = np.clip(np.rint(fi), 0, h - 1).astype(np.int64)
        j = np.clip(np.rint(fj), 0, w - 1).astype(np.int64)
        r = a[i, j]
        return r.item() if np.ndim(r) == 0 else r

    def boden(self, x, y):
        return self.bilinear(self.h, x, y)

    def normale(self, x, y):
        gx = self.bilinear(self.gx, x, y)
        gy = self.bilinear(self.gy, x, y)
        v = np.array([-gx, -gy, 1.0])
        return v / np.linalg.norm(v)

    def hang_grad(self, x, y):
        gx = self.bilinear(self.gx, x, y)
        gy = self.bilinear(self.gy, x, y)
        return math.degrees(math.atan(math.hypot(gx, gy)))

    def hangab(self, x, y):
        gx = self.bilinear(self.gx, x, y)
        gy = self.bilinear(self.gy, x, y)
        nrm = math.hypot(gx, gy)
        if nrm < 1e-6:
            return (1.0, 0.0)
        return (-gx / nrm, -gy / nrm)

    def im_feld(self, x, y):
        return D.feld_von_m(x, y) == self.feld

    def frei(self, x, y, wasser_uebergang_ok=True):
        if not self.innen_pkt(x, y):
            return False
        if self.naechst(self.zone, x, y) == ZONEN["sperre"]:
            return False
        if float(self.bilinear(self.d_wasser, x, y)) < self.R["zonen"]["sperre"]["wasser_m"] + 0.5:
            return False
        if not wasser_uebergang_ok and self.naechst(self.uebergang, x, y):
            return False
        return self.im_feld(x, y)

    def innen_pkt(self, x, y):
        x0, y0, x1, y1 = self.fenster_m
        return x0 <= x < x1 and y0 <= y < y1

    def kandidaten(self, maske, schritt_m, salt):
        """Gejitterte Gitterpunkte (Weltkoordinaten) in maske & innen, sortiert nach Hash-Prioritaet."""
        x0, y0, x1, y1 = self.fenster_m
        nx = int(math.ceil((x1 - x0) / schritt_m))
        ny = int(math.ceil((y1 - y0) / schritt_m))
        jj, ii = np.meshgrid(np.arange(nx), np.arange(ny))
        jx = hash01_arr(ii, jj, salt * 2 + 1)
        jy = hash01_arr(ii, jj, salt * 2 + 2)
        x = x0 + (jj + jx) * schritt_m
        y = y0 + (ii + jy) * schritt_m
        x, y = x.ravel(), y.ravel()
        ok = (x < x1) & (y < y1)
        x, y = x[ok], y[ok]
        m = self.naechst(maske.astype(np.uint8), x, y).astype(bool) & self.naechst(self.innen.astype(np.uint8), x, y).astype(bool)
        x, y = x[m], y[m]
        pr = hash01_arr(np.round(x * 10).astype(np.int64) & 0xFFFFFFF, np.round(y * 10).astype(np.int64) & 0xFFFFFFF, salt + 7)
        o = np.argsort(pr, kind="stable")
        return x[o], y[o]


class Gitter:
    """Raeumliches Hash-Gitter fuer Mindestabstaende."""

    def __init__(self, zelle=4.0):
        self.z = float(zelle)
        self.d = {}

    def frei(self, x, y, r, faktor, such_r):
        k = int(math.ceil(such_r / self.z))
        ci, cj = int(math.floor(x / self.z)), int(math.floor(y / self.z))
        for a in range(ci - k, ci + k + 1):
            for b in range(cj - k, cj + k + 1):
                for (px, py, pr) in self.d.get((a, b), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < (faktor * (r + pr)) ** 2:
                        return False
        return True

    def naechster(self, x, y, such_r):
        k = int(math.ceil(such_r / self.z))
        ci, cj = int(math.floor(x / self.z)), int(math.floor(y / self.z))
        best = 1e9
        for a in range(ci - k, ci + k + 1):
            for b in range(cj - k, cj + k + 1):
                for (px, py, pr) in self.d.get((a, b), ()):
                    best = min(best, math.hypot(px - x, py - y))
        return best

    def add(self, x, y, r):
        self.d.setdefault((int(math.floor(x / self.z)), int(math.floor(y / self.z))), []).append((x, y, r))


# ============================================================================================
# Planer
# ============================================================================================
class Planer:
    def __init__(self, welt, regeln, inv, delta=None, variante="A"):
        self.R = regeln
        self.K = Kontext(welt, regeln, delta)
        self.N = Netze(inv, regeln)
        self.inv = inv
        self.variante = variante
        self.stuecke = []
        self.stat = {}
        self.seed = int(regeln["seed"])
        self.bio = regeln["biome"].get(regeln["pilot"]["biom"], {"deckung": 1.0, "baeume": 1.0})
        self.g_block = Gitter(4.0)      # alle Fels-Stuecke (Bloecke, Platten, Fussbloecke) fuer Baum-Block-Regel
        self.front = regeln.get("front_achse_annahme", "-y")

    # --- Stueck anlegen -----------------------------------------------------------------------
    def setze(self, thema, rolle, netz, x, y, q, s, eingraben_m=0.0, bezug="min", kontakt="welt", kol=False,
              akteur=False, sicht="block", zone=None, d_m=None, extra=None):
        info = self.N.info[netz]
        p = INS.platziere(info, x, y, q, s, self.K.boden, eingraben_m=eingraben_m, bezug=bezug, kontakt=kontakt)
        if not self.K.frei(p["mx_m"], p["my_m"]):
            return None
        e = {"thema": thema, "rolle": rolle, "netz": netz, "pfad": info["pfad"], "x": p["x"], "y": p["y"],
             "z": p["z"], "q": tuple(q), "s": tuple(float(v) for v in s), "kol": bool(kol), "akteur": bool(akteur),
             "sicht": list(self.R["sichtweite_cm"][sicht]), "zone": zone,
             "d_m": float(d_m if d_m is not None else max(info["groesse_m"]) * max(s)),
             "fuss": (p["mx_m"], p["my_m"], p["fuss_a_m"], p["fuss_b_m"], p["fuss_winkel"]),
             "hoehe_m": p["hoehe_m"], "extra": extra or {}}
        # Feldzuordnung wie der Setzer (float32)
        fx, fy = float(np.float32(e["x"])) / 100.0, float(np.float32(e["y"])) / 100.0
        if D.feld_von_m(fx, fy) != self.K.feld:
            return None
        self.stuecke.append(e)
        return e

    def _skala_auf(self, netz, d, achse="lang"):
        g = self.N.g(netz)
        ref = max(g) if achse == "lang" else (g[2] if achse == "z" else max(g[0], g[1]))
        return d / max(ref, 1e-3)

    def _waehle(self, palette, schluessel, d=None, ausschluss=(), achse="lang", s_bereich=(0.5, 2.5)):
        """Netz aus Palette: bevorzugt Netze, deren Skala fuer Zielgroesse d in s_bereich liegt."""
        kand = [n for n in self.R["paletten"][palette] if n in self.N.info and self.N.form(n) not in ausschluss]
        if not kand:
            kand = [n for n in self.R["paletten"][palette] if n in self.N.info]
        if d is not None:
            gut = [n for n in kand if s_bereich[0] <= self._skala_auf(n, d, achse) <= s_bereich[1]]
            if gut:
                kand = gut
        return kand[int(u01(*schluessel) * len(kand)) % len(kand)]

    # --- Halde ----------------------------------------------------------------------------------
    def plane_halde(self):
        K, H = self.K, self.R["halde"]
        halde = K.zone == ZONEN["halde"]
        # 1) Schutt-Teppich: Zieldeckung je 8-m-Zelle
        cz = float(H["teppich_zelle_m"])
        x0, y0, _, _ = K.fenster_m
        belegt = {}
        g_t = Gitter(4.0)
        xs, ys = K.kandidaten(halde, 2.0, self.seed + 101)
        n_t = 0
        for k, (x, y) in enumerate(zip(xs, ys)):
            if not K.frei(x, y):
                continue
            t = float(K.bilinear(K.t_halde, x, y))
            mod = 1.0 + H["kegel_modulation"] * float(K.bilinear(K.n_kegel, x, y))
            if float(K.bilinear(K.n_kegel, x, y)) < H["rasenzunge_schwelle"]:
                mod *= H["rasenzunge_faktor"]
            ziel = (H["deckung_oben"] + (H["deckung_unten"] - H["deckung_oben"]) * t) * mod * self.bio["deckung"]
            if K.naechst(K.uebergang, x, y):
                ziel *= 0.5
            ci, cj = int((x - x0) // cz), int((y - y0) // cz)
            if belegt.get((ci, cj), 0.0) >= ziel * cz * cz:
                continue
            netz = self._waehle("teppich", ("tep", k, round(x, 2), round(y, 2)))
            gx, gy, gz = self.N.g(netz)
            s1 = u_bereich(H["teppich_skala"], "tsk", round(x, 2), round(y, 2))
            r = 0.5 * math.sqrt(gx * gy) * s1
            if not g_t.frei(x, y, r, H["teppich_mindestabstand_faktor"], 2 * r + 6.0):
                continue
            dx, dy = K.hangab(x, y)
            yaw = kompass(dx, dy) + (u01("tyaw", k, round(x, 2)) - 0.5) * 2 * H["teppich_yaw_streuung_grad"]
            nrm = K.normale(x, y)
            front = "+x" if gx >= gy else "+y"
            q = INS.orientierung("aufrecht", yaw_grad=yaw, normale=nrm, normale_anteil=1.0, front_achse=front)
            hang = math.radians(K.hang_grad(x, y))
            e_anteil = 0.5 if gz * s1 >= 0.5 else 0.3
            ein = e_anteil * gz * s1 / max(math.cos(hang), 0.3)
            e = self.setze("halde", "teppich", netz, x, y, q, (s1, s1, s1), eingraben_m=ein, kontakt="lokal",
                           kol=False, sicht="teppich", zone="halde", d_m=max(gx, gy) * s1)
            if e is None:
                continue
            g_t.add(x, y, r)
            belegt[(ci, cj)] = belegt.get((ci, cj), 0.0) + 0.8 * gx * gy * s1 * s1
            n_t += 1
        # 2) Bloecke je Groessenklasse (Fall-Sortierung: grosse unten)
        klassen = [(0.8, 1.5, "block_klein"), (1.5, 3.0, "block_mittel"), (3.0, 6.0, "block_gross"), (6.0, 9.0, "block_hero")]
        n_b = {}
        # harte Quote je 48-m-Zelle (wie Runde 5, Halde-Grenzen aus pruef_schwellen x 0,9)
        PS = self.R["pruef_schwellen"]
        qz = 48.0
        hz = halde & K.innen
        ci_ = ((K.X - x0) // qz).astype(int)
        cj_ = ((K.Y - y0) // qz).astype(int)
        fl_q = {}
        for a_, b_ in zip(ci_[hz].tolist(), cj_[hz].tolist()):
            fl_q[(a_, b_)] = fl_q.get((a_, b_), 0.0) + K.z * K.z
        quote2 = {k_: int(math.floor(0.9 * PS["halde_bloecke_gt2_je_100m2_max"] * v_ / 100.0)) for k_, v_ in fl_q.items()}
        quote4 = {k_: int(math.floor(0.9 * PS["halde_bloecke_gt4_je_100m2_max"] * v_ / 100.0)) for k_, v_ in fl_q.items()}
        z2, z4 = {}, {}
        a_kand = 1.5 * 1.5
        for (lo, hi, pal) in reversed(klassen):          # gross zuerst (Platzvorrang)
            key = "%g-%g" % (lo, hi)
            oben, unten = H["bloecke_je_100m2"][key]
            xs, ys = K.kandidaten(halde, 1.5, self.seed + 200 + int(lo * 10))
            n_b[key] = 0
            for k, (x, y) in enumerate(zip(xs, ys)):
                t = float(K.bilinear(K.t_halde, x, y))
                dichte = (oben + (unten - oben) * t) * self.bio["deckung"]
                mod = max(0.15, 1.0 + H["kegel_modulation"] * float(K.bilinear(K.n_kegel, x, y)))
                if u01("bp", key, k, round(x, 2), round(y, 2)) >= dichte * mod * a_kand / 100.0:
                    continue
                if not K.frei(x, y):
                    continue
                d = potenz_d(lo, hi, 2.2, u01("bd", key, k, round(x, 2)))
                hang = K.hang_grad(x, y)
                aus = ("wuerfel", "stehend") if (d > self.R["pruef_schwellen"]["wuerfel_max_d_m"] or hang > 30) else ()
                netz = self._waehle(pal, ("bn", key, k, round(x, 2)), d=d, ausschluss=aus)
                if d > self.R["pruef_schwellen"]["wuerfel_max_d_m"] and self.N.form(netz) in ("wuerfel", "stehend"):
                    continue
                s1 = max(0.45, min(2.6, self._skala_auf(netz, d)))
                s = (s1 * u_bereich((0.92, 1.08), "bsx", k, key), s1 * u_bereich((0.92, 1.08), "bsy", k, key), s1)
                gg_ = self.N.g(netz)
                d = max(gg_[0] * s[0], gg_[1] * s[1], gg_[2] * s[2])
                r = 0.5 * d
                if not self.g_block.frei(x, y, r, H["block_mindestabstand_faktor"], r + 6.0):
                    continue
                qk = (int((x - x0) // qz), int((y - y0) // qz))
                if d > 2.0 and z2.get(qk, 0) >= quote2.get(qk, 0):
                    continue
                if d > 4.0 and z4.get(qk, 0) >= quote4.get(qk, 0):
                    continue
                gx, gy, gz = self.N.g(netz)
                dx, dy = K.hangab(x, y)
                yaw = kompass(dx, dy) + (u01("byaw", k, key) - 0.5) * 2 * H["block_achse_falllinie_grad"]
                front = "+x" if gx >= gy else "+y"
                q = INS.orientierung("aufrecht", yaw_grad=yaw, normale=K.normale(x, y), normale_anteil=1.0, front_achse=front)
                ea = u_bereich(H["block_eingraben_senkrecht"], "bein", k, key)
                ein = ea * gz * s[2] / max(math.cos(math.radians(hang)), 0.3)
                akteur = d >= H["akteur_ab_d_m"]
                e = self.setze("halde", "akteur" if akteur else "block", netz, x, y, q, s, eingraben_m=ein,
                               kontakt="lokal", kol=True, akteur=akteur, sicht="block_klein" if d < 1.5 else "block",
                               zone="halde", d_m=d)
                if e is None:
                    continue
                self.g_block.add(x, y, r)
                n_b[key] += 1
                if d > 2.0:
                    z2[qk] = z2.get(qk, 0) + 1
                if d > 4.0:
                    z4[qk] = z4.get(qk, 0) + 1
        self.stat["halde"] = {"teppich": n_t, "bloecke": n_b}

    # --- Klippenband: Schrofen-Baender, Wandreihen, Gratkronen, Turm ------------------------------
    def _schichtlinien(self, maske, dz, jitter, salt):
        """Kreuzungspunkte der Schichtlinien f = L_k in maske & innen. Rueckgabe Liste (k, x, y)."""
        K = self.K
        f = K.f_schicht
        kmin = int(math.floor(f[maske].min() / dz)) - 1 if maske.any() else 0
        kmax = int(math.ceil(f[maske].max() / dz)) + 1 if maske.any() else 0
        pts = []
        for k in range(kmin, kmax + 1):
            L = k * dz + (u01("lev", salt, k) - 0.5) * 2 * jitter
            g = f - L
            for di, dj in ((0, 1), (1, 0)):
                a = g[: g.shape[0] - di, : g.shape[1] - dj]
                b = g[di:, dj:]
                m = (np.sign(a) != np.sign(b)) & maske[: g.shape[0] - di, : g.shape[1] - dj] & \
                    K.innen[: g.shape[0] - di, : g.shape[1] - dj]
                ii, jj = np.nonzero(m)
                if ii.size == 0:
                    continue
                tt = a[ii, jj] / (a[ii, jj] - b[ii, jj])
                x = K.X[ii, jj] + tt * dj * K.z
                y = K.Y[ii, jj] + tt * di * K.z
                for xx, yy in zip(x.tolist(), y.tolist()):
                    pts.append((k, xx, yy))
        pts.sort(key=lambda p: (p[0], u01("lp", salt, p[0], round(p[1], 2), round(p[2], 2))))
        return pts

    def plane_klippenband(self):
        K, SR, WR = self.K, self.R["schrofen"], self.R["wand"]
        n_band = n_wand = n_grat = 0
        # 1) Schrofen-Baender
        schrofen = (K.zone == ZONEN["schrofen"])
        pts = self._schichtlinien(schrofen, SR["band_dz_m"], SR["band_dz_streuung_m"], 1)
        nb = ST.rauschen(K.X, K.Y, 22.0, self.seed + 5)
        rn = (K.bilinear(nb, np.array([p[1] for p in pts]), np.array([p[2] for p in pts])) if pts else np.zeros(0))
        rn = np.atleast_1d(np.asarray(rn, np.float64))
        thr = float(np.quantile(rn, 1.0 - SR["band_kontinuitaet"])) if rn.size else 0.0
        g = {}
        for idx, (k, x, y) in enumerate(pts):
            if rn[idx] < thr or not K.frei(x, y, wasser_uebergang_ok=False):
                continue
            netz = self._waehle("band", ("band", k, round(x, 1), round(y, 1)))
            gx, gy, gz = self.N.g(netz)
            hz = u_bereich(SR["band_hoehe_m"], "bh", k, round(x, 1))
            s1 = max(0.8, min(2.4, hz / max(gz, 0.2)))
            lang = max(gx, gy) * s1
            eff = lang * (1.0 - SR["band_ueberlappung"])
            gg = g.setdefault(k, Gitter(6.0))
            if not gg.frei(x, y, 0.5 * eff, 1.0, eff + 8.0):
                continue
            dx, dy = K.hangab(x, y)
            vers = u_bereich(SR["band_versatz_m"], "bv", k)
            tiefe = min(gx, gy) * s1
            px, py = x - dx * (vers + 0.25 * tiefe), y - dy * (vers + 0.25 * tiefe)
            if not K.frei(px, py, wasser_uebergang_ok=False):
                continue
            front = self.front if gx >= gy else ("-x" if self.front.endswith("y") else "-y")
            q = INS.orientierung("aufrecht", yaw_grad=kompass(dx, dy), front_achse=front,
                                 kipp_richtung_grad=kompass(-dx, -dy), kipp_grad=SR["band_rueckneigung_grad"])
            e = self.setze("klippenband", "band", netz, px, py, q, (s1, s1, s1), eingraben_m=0.15 * gz * s1,
                           kontakt="welt", kol=True, sicht="band", zone="schrofen", d_m=lang, extra={"band": k})
            if e is None:
                continue
            gg.add(x, y, 0.5 * eff)
            n_band += 1
        # 2) Wandreihen (nur hohe Waende)
        wh = K.wand_hoch & (K.zone == ZONEN["wand"])
        pal = [n for n in self.R["paletten"]["wand"] if n in self.N.info]
        hmed = float(np.median([self.N.g(n)[2] for n in pal])) if pal else 10.0
        dzw = WR["reihe_dz_faktor"] * hmed
        pts = self._schichtlinien(wh, dzw, 0.0, 2)
        gw = {}
        for (k, x, y) in pts:
            if n_wand >= WR["max_module"]:
                break
            if not K.frei(x, y, wasser_uebergang_ok=False):
                continue
            netz = self._waehle("wand", ("wand", k, round(x, 1), round(y, 1)))
            gx, gy, gz = self.N.g(netz)
            s1 = u_bereich((0.8, 1.15), "ws", k, round(x, 1))
            lang = max(gx, gy) * s1
            eff = lang * (1.0 - WR["ueberlappung"])
            gg = gw.setdefault(k, Gitter(8.0))
            if not gg.frei(x, y, 0.5 * eff, 1.0, eff + 10.0):
                continue
            dx, dy = K.hangab(x, y)
            tiefe = min(gx, gy) * s1
            px, py = x - dx * 0.25 * tiefe, y - dy * 0.25 * tiefe
            if not K.frei(px, py, wasser_uebergang_ok=False):
                continue
            front = self.front if gx >= gy else ("-x" if self.front.endswith("y") else "-y")
            q = INS.orientierung("aufrecht", yaw_grad=kompass(dx, dy), front_achse=front,
                                 kipp_richtung_grad=kompass(-dx, -dy), kipp_grad=u_bereich(WR["kipp_grad"], "wk", k, round(x, 1)))
            e = self.setze("klippenband", "wandreihe", netz, px, py, q, (s1, s1, s1), eingraben_m=WR["eingraben"] * gz * s1 * 0.3,
                           kontakt="welt", kol=True, sicht="wand", zone="wand", d_m=lang, extra={"reihe": k})
            if e is None:
                continue
            gg.add(x, y, 0.5 * eff)
            n_wand += 1
        # 3) Gratkronen
        gr = K.grat & (K.n >= 25.0) & (K.zone != ZONEN["sperre"])
        xs, ys = K.kandidaten(gr, 6.0, self.seed + 301)
        g_g = Gitter(12.0)
        for k, (x, y) in enumerate(zip(xs, ys)):
            if not K.frei(x, y, wasser_uebergang_ok=False):
                continue
            if not g_g.frei(x, y, 0.5 * WR["gratkrone_abstand_m"], 1.0, WR["gratkrone_abstand_m"]):
                continue
            netz = self._waehle("gratkrone", ("gk", k, round(x, 1)))
            gx, gy, gz = self.N.g(netz)
            s1 = max(0.35, min(1.4, u_bereich((4.0, 7.0), "gkh", k) / gz))
            dx, dy = K.hangab(x, y)
            front = self.front if gx >= gy else ("-x" if self.front.endswith("y") else "-y")
            q = INS.orientierung("aufrecht", yaw_grad=kompass(dx, dy), front_achse=front)
            e = self.setze("klippenband", "gratkrone", netz, x, y, q, (s1, s1, s1), eingraben_m=0.25 * gz * s1,
                           kontakt="welt", kol=True, sicht="wand", zone="grat", d_m=max(gx, gy) * s1)
            if e is None:
                continue
            g_g.add(x, y, 0.5 * WR["gratkrone_abstand_m"])
            n_grat += 1
        # 4) Turmklotz: markanteste Wandnase im Fenster (TPI 40 m), Akteur
        n_turm = 0
        wand_i = (K.zone == ZONEN["wand"]) & K.innen & (K.d_wasser > 30.0)
        if wand_i.any() and WR["turm_je_front"] > 0:
            tp = G.tpi(K.h.astype(np.float32), K.z, 40.0).astype(np.float64)
            tp = np.where(wand_i, tp, -1e9)
            i, j = np.unravel_index(int(np.argmax(tp)), tp.shape)
            x, y = float(K.X[i, j]), float(K.Y[i, j])
            netz = self.R["paletten"]["turm"][0]
            if netz in self.N.info and K.frei(x, y, wasser_uebergang_ok=False):
                gx, gy, gz = self.N.g(netz)
                dx, dy = K.hangab(x, y)
                grat_h = float(G.max_filter(K.h.astype(np.float32), int(round(60.0 / K.z)))[i, j])
                s1 = 1.0
                q = INS.orientierung("aufrecht", yaw_grad=kompass(dx, dy), front_achse="+x" if gx >= gy else "+y")
                e = self.setze("klippenband", "akteur", netz, x - dx * 4.0, y - dy * 4.0, q, (s1, s1, s1),
                               eingraben_m=0.25 * gz * s1, kontakt="welt", kol=True, akteur=True, sicht="wand",
                               zone="wand", d_m=max(gx, gy, gz), extra={"turm": True})
                if e is not None:
                    ober = (e["z"] / 100.0) + gz * s1 * (1 - 0.0)
                    e["extra"]["ueber_grat_m"] = round(ober - grat_h, 1)
                    n_turm = 1
        self.stat["klippenband"] = {"band": n_band, "wandreihe": n_wand, "gratkrone": n_grat, "turm": n_turm,
                                    "band_dz_m": self.R["schrofen"]["band_dz_m"], "wand_dz_m": round(dzw, 2)}

    # --- Platten --------------------------------------------------------------------------------
    def plane_platten(self):
        K, P = self.K, self.R["platten"]
        fuss = K.zone == ZONEN["fuss"]
        cz = float(P["zelle_m"])
        x0, y0, _, _ = K.fenster_m
        belegt = {}
        xs, ys = K.kandidaten(fuss, 2.0, self.seed + 401)
        n_p = n_f = 0
        sch = self.R["schichtung"]
        for k, (x, y) in enumerate(zip(xs, ys)):
            if not K.frei(x, y):
                continue
            if float(K.bilinear(K.n_kegel, x, y)) < P.get("feld_schwelle", -1.0):
                continue
            nah = bool(K.naechst(K.fuss_nah, x, y))
            ziel = (P["deckung_nah"] if nah else P["deckung_fern"]) * self.bio["deckung"]
            ziel *= max(0.2, 0.8 + 0.6 * float(K.bilinear(K.n_kegel, x, y)))
            ci, cj = int((x - x0) // cz), int((y - y0) // cz)
            if belegt.get((ci, cj), 0.0) >= ziel * cz * cz:
                continue
            L = potenz_d(P["laenge_m"][0], P["laenge_m"][1], P["laenge_exponent"], u01("pl", k, round(x, 2)))
            netz = self._waehle("platte", ("pn", k, round(x, 2)), d=L, achse="xy", s_bereich=(0.7, 2.5))
            gx, gy, gz = self.N.g(netz)
            s1 = max(0.6, min(2.6, L / max(gx, gy)))
            r = 0.5 * L
            if not self.g_block.frei(x, y, r, P["mindestabstand_faktor"], r + 8.0):
                continue
            yaw = sch["streichen_grad"] + 90.0 + (u01("pyaw", k) - 0.5) * 50.0
            hang = math.radians(K.hang_grad(x, y))
            ea = u_bereich(P["eingraben"], "pein", k)
            q = INS.orientierung("aufrecht", yaw_grad=yaw, normale=K.normale(x, y), normale_anteil=1.0,
                                 front_achse="+x" if gx >= gy else "+y")
            e = self.setze("platten", "platte", netz, x, y, q, (s1, s1, s1), eingraben_m=ea * gz * s1 / max(math.cos(hang), 0.3),
                           kontakt="lokal", kol=True, sicht="platte", zone="fuss", d_m=L)
            if e is None:
                continue
            self.g_block.add(x, y, r)
            belegt[(ci, cj)] = belegt.get((ci, cj), 0.0) + 0.8 * gx * gy * s1 * s1
            n_p += 1
            n_f += self._fugen(e, k)
        self.stat["platten"] = {"platten": n_p, "fugenbewuchs": n_f}

    def _fugen(self, platte, k):
        K, P = self.K, self.R["platten"]
        mx, my, a, b, w = platte["fuss"]
        umfang = math.pi * (a + b)
        n = int(round(umfang * P["fugen_je_m_rand"] * u_bereich((0.7, 1.3), "fn", k)))
        anz = 0
        for i in range(n):
            th = 2 * math.pi * u01("fth", k, i)
            rf = u_bereich((1.0, 1.12), "frf", k, i)
            lx, ly = a * rf * math.cos(th), b * rf * math.sin(th)
            x = mx + lx * math.cos(w) - ly * math.sin(w)
            y = my + lx * math.sin(w) + ly * math.cos(w)
            if not K.frei(x, y):
                continue
            uu = u01("fart", k, i)
            fa = P["fugen_anteil"]
            pal = "fuge_gras" if uu < fa["gras"] else ("fuge_farn" if uu < fa["gras"] + fa["farn"] else "fuge_moos")
            netz = self._waehle(pal, ("fz", k, i))
            s1 = u_bereich((0.8, 1.3), "fs", k, i)
            q = INS.orientierung("aufrecht", yaw_grad=360.0 * u01("fy", k, i), normale=K.normale(x, y), normale_anteil=0.3)
            if self.setze("platten", "fuge", netz, x, y, q, (s1, s1, s1), eingraben_m=0.03, bezug="mitte",
                          kol=False, sicht="fuge", zone="fuge") is not None:
                anz += 1
        return anz

    # --- Baumgruppen ----------------------------------------------------------------------------
    def plane_baumgruppen(self):
        K, B = self.K, self.R["baumgruppen"]
        zonen_ok = {"fuss": ZONEN["fuss"], "hangwald": ZONEN["hangwald"], "halde": ZONEN["halde"], "schrofen": ZONEN["schrofen"]}
        maske = np.isin(K.zone, list(zonen_ok.values())) & (K.d_wasser >= self.R["zonen"]["sperre"]["wasser_m"])
        xs, ys = K.kandidaten(maske, 12.0, self.seed + 501)
        g_z = Gitter(16.0)
        g_baum = Gitter(4.0)
        grat_zentren = Gitter(20.0)
        n_g = n_b = n_fb = n_tl = n_ts = 0
        baum_nr = 0
        for k, (x, y) in enumerate(zip(xs, ys)):
            if not K.frei(x, y, wasser_uebergang_ok=False):
                continue
            zc = int(K.naechst(K.zone, x, y))
            zn = [n for n, v in zonen_ok.items() if v == zc][0]
            if zn == "halde" and float(K.bilinear(K.t_halde, x, y)) < 0.6:
                continue
            if float(K.bilinear(K.n_baum, x, y)) < B["luecke_schwelle"]:
                continue
            if u01("gp", k, round(x, 1)) >= B["wahrscheinlichkeit"][zn] * self.bio["baeume"]:
                continue
            ab = B["zentrum_abstand_m"][zn]
            if not g_z.frei(x, y, 0.5 * ab, 1.0, ab):
                continue
            am_grat = float(K.bilinear(K.d_grat, x, y)) < B["grat_abstand_m"]
            if am_grat and grat_zentren.naechster(x, y, B["grat_gruppen_abstand_m"]) < B["grat_gruppen_abstand_m"]:
                continue
            nmax = B["grat_max_gruppe"] if am_grat else B["groesse"][1]
            nmin = min(B["groesse"][0], nmax)
            N = nmin + int(u01("gn", k) * (nmax - nmin + 1))
            R = u_bereich(B["radius_m"], "gr", k)
            g_z.add(x, y, 0.5 * ab)
            if am_grat:
                grat_zentren.add(x, y, 0.0)
            n_g += 1
            gesetzt = 0
            for i in range(N * 4):
                if gesetzt >= N:
                    break
                rr = R * math.sqrt(u01("tr", k, i))
                th = 2 * math.pi * u01("tt", k, i)
                bx, by = x + rr * math.cos(th), y + rr * math.sin(th)
                if not K.frei(bx, by, wasser_uebergang_ok=False) or float(K.bilinear(K.d_wasser, bx, by)) < 10.0:
                    continue
                if int(K.naechst(K.zone, bx, by)) == ZONEN["wand"] or K.hang_grad(bx, by) > 46.0:
                    continue
                if not g_baum.frei(bx, by, 0.5 * B["baum_mindestabstand_m"], 1.0, B["baum_mindestabstand_m"] + 1):
                    continue
                baum_nr += 1
                uu = u01("kl", k, i)
                kl = B["klassen"]
                klasse = "jung" if uu < kl["jung"] else ("mittel" if uu < kl["jung"] + kl["mittel"] else "hoch")
                tot = (baum_nr % int(B["totholz_stehend_je_baeume"]) == 0) and klasse != "jung"
                pal = "baum_tot" if tot else "baum_" + klasse
                hz = u_bereich(self.R["baum_hoehe_m"]["tot" if tot else klasse], "bh", k, i)
                netz = self._waehle(pal, ("bn", k, i), d=hz, achse="z", s_bereich=(0.45, 1.4))
                s1 = hz / self.N.g(netz)[2]
                q = INS.orientierung("aufrecht", yaw_grad=360.0 * u01("by", k, i), normale=K.normale(bx, by), normale_anteil=0.05)
                e = self.setze("baumgruppen", "baum_tot" if tot else "baum_" + klasse, netz, bx, by, q, (s1, s1, s1),
                               eingraben_m=0.15, bezug="mitte", kol=True, sicht="baum", zone=zn, d_m=hz,
                               extra={"gruppe": n_g, "grat": am_grat})
                if e is None:
                    continue
                g_baum.add(bx, by, 0.5 * B["baum_mindestabstand_m"])
                gesetzt += 1
                n_b += 1
                if tot:
                    n_ts += 1
                # Fussblock-Regel: Block 1-3 m im Radius 3 m
                if self.g_block.naechster(bx, by, B["block_radius_m"] + 3.0) > B["block_radius_m"]:
                    if self._fussblock(bx, by, k, i):
                        n_fb += 1
            # Totholz liegend
            if gesetzt and u01("tl", k) < B["totholz_liegend_je_gruppe"]:
                th = 2 * math.pi * u01("tlt", k)
                tx, ty = x + (R + 2.0) * math.cos(th), y + (R + 2.0) * math.sin(th)
                if K.frei(tx, ty, wasser_uebergang_ok=False) and int(K.naechst(K.zone, tx, ty)) != ZONEN["wand"]:
                    netz = self._waehle("totholz", ("tlh", k))
                    gx, gy, gz = self.N.g(netz)
                    s1 = u_bereich((0.85, 1.2), "tls", k)
                    dx, dy = K.hangab(tx, ty)
                    yaw = kompass(-dy, dx) + (u01("tly", k) - 0.5) * 60.0
                    q = INS.orientierung("aufrecht", yaw_grad=yaw, normale=K.normale(tx, ty), normale_anteil=1.0,
                                         front_achse="+x" if gx >= gy else "+y")
                    if self.setze("baumgruppen", "totholz", netz, tx, ty, q, (s1, s1, s1), eingraben_m=0.25 * gz * s1,
                                  kontakt="lokal", kol=True, sicht="totholz", zone=zn) is not None:
                        n_tl += 1
        # Latschen in Schrofen und am oberen Haldenrand
        lm = ((K.zone == ZONEN["schrofen"]) | ((K.zone == ZONEN["halde"]) & (K.t_halde > 0.5)))
        xs, ys = K.kandidaten(lm, 10.0, self.seed + 551)
        g_l = Gitter(12.0)
        n_l = 0
        p_l = self.R["schrofen"]["latschen_gruppen_je_ha"] * (10.0 * 10.0) / 10000.0 * 2.2
        for k, (x, y) in enumerate(zip(xs, ys)):
            if not K.frei(x, y, wasser_uebergang_ok=False) or u01("lp", k) >= p_l:
                continue
            if not g_l.frei(x, y, 12.0, 1.0, 25.0):
                continue
            g_l.add(x, y, 12.0)
            for i in range(2 + int(u01("ln", k) * 4)):
                rr = 3.0 * math.sqrt(u01("lr", k, i))
                th = 2 * math.pi * u01("lt", k, i)
                lx, ly = x + rr * math.cos(th), y + rr * math.sin(th)
                if not K.frei(lx, ly, wasser_uebergang_ok=False) or not g_baum.frei(lx, ly, 0.8, 1.0, 3.0):
                    continue
                netz = self._waehle("latsche", ("ln", k, i))
                s1 = u_bereich((0.8, 1.2), "ls", k, i)
                q = INS.orientierung("aufrecht", yaw_grad=360.0 * u01("ly", k, i), normale=K.normale(lx, ly), normale_anteil=0.4)
                if self.setze("baumgruppen", "latsche", netz, lx, ly, q, (s1, s1, s1), eingraben_m=0.05, bezug="mitte",
                              kol=False, sicht="latsche", zone="latsche") is not None:
                    g_baum.add(lx, ly, 0.8)
                    n_l += 1
        self.stat["baumgruppen"] = {"gruppen": n_g, "baeume": n_b, "davon_tot_stehend": n_ts, "fussbloecke": n_fb,
                                    "totholz_liegend": n_tl, "latschen": n_l}

    def _fussblock(self, bx, by, k, i):
        K = self.K
        dx, dy = K.hangab(bx, by)
        for v in range(4):
            a = math.atan2(dy, dx) + (u01("fba", k, i, v) - 0.5) * math.radians(80)
            rr = u_bereich((1.6, 2.6), "fbr", k, i, v)
            x, y = bx + rr * math.cos(a), by + rr * math.sin(a)
            if not K.frei(x, y):
                continue
            d = u_bereich((1.0, 2.5), "fbd", k, i)
            netz = self._waehle("fussblock", ("fb", k, i), d=d, ausschluss=("wuerfel", "stehend"))
            gx, gy, gz = self.N.g(netz)
            s1 = max(0.4, min(2.2, d / max(gx, gy, gz)))
            hang = math.radians(K.hang_grad(x, y))
            q = INS.orientierung("aufrecht", yaw_grad=kompass(dx, dy), normale=K.normale(x, y), normale_anteil=1.0,
                                 front_achse="+x" if gx >= gy else "+y")
            e = self.setze("baumgruppen", "fussblock", netz, x, y, q, (s1, s1, s1),
                           eingraben_m=0.45 * gz * s1 / max(math.cos(hang), 0.3), kontakt="lokal", kol=True,
                           sicht="block", zone="fussblock", d_m=d)
            if e is not None:
                self.g_block.add(x, y, 0.5 * d)
                return True
        return False

    # --- Budget ---------------------------------------------------------------------------------
    def budget(self):
        B = self.R["budget"]
        kol = [e for e in self.stuecke if e["kol"] and not e["akteur"]]
        if len(kol) > B["kollision_gesamt"]:
            kol.sort(key=lambda e: (e["d_m"], e["x"], e["y"]))
            for e in kol[: len(kol) - B["kollision_gesamt"]]:
                e["kol"] = False
            log("Hinweis Budget: %d kleinste Stuecke ohne Kollision" % (len(kol) - B["kollision_gesamt"]))
        ak = [e for e in self.stuecke if e["akteur"]]
        if len(ak) > B["akteure_gesamt"]:
            ak.sort(key=lambda e: (e["d_m"], e["x"]))
            for e in ak[: len(ak) - B["akteure_gesamt"]]:
                e["akteur"] = False

    def plane(self):
        self.plane_klippenband()
        self.plane_halde()
        self.plane_platten()
        self.plane_baumgruppen()
        self.budget()


# ============================================================================================
# Schreiben
# ============================================================================================
def schreibe_themen(pl, aus):
    feld = pl.K.feld
    akteure_alle = []
    zusammen = {}
    for thema, kuerzel in THEMEN.items():
        ordner = os.path.join(aus, "%s_%s" % (thema, feld))
        os.makedirs(ordner, exist_ok=True)
        for fn in sorted(os.listdir(ordner)):
            if fn.endswith(".f32") or fn == "plan.json":
                os.remove(os.path.join(ordner, fn))
        st = [e for e in pl.stuecke if e["thema"] == thema]
        gruppen = {}
        for e in st:
            key = ("akteur_" if e["akteur"] else "") + pl.N.info[e["netz"]]["name"] + ("_kol" if e["kol"] else "")
            gruppen.setdefault(key, []).append(e)
        dateien = {}
        akteure = []
        for key in sorted(gruppen):
            g = gruppen[key]
            rec = np.array([[e["x"], e["y"], e["z"], e["q"][0], e["q"][1], e["q"][2], e["q"][3],
                             e["s"][0], e["s"][1], e["s"][2]] for e in g], dtype="<f4")
            rec.tofile(os.path.join(ordner, key + ".f32"))
            rollen = sorted({e["rolle"] for e in g})
            sw = [0, 0] if any(e["sicht"][1] == 0 for e in g) else [min(e["sicht"][0] for e in g), max(e["sicht"][1] for e in g)]
            dateien[key] = {"pfad": g[0]["pfad"], "anzahl": len(g), "gruppe": thema, "rolle": "/".join(rollen),
                            "sichtweite": sw, "schatten": True, "kollision": bool(g[0]["kol"]),
                            "nanite": bool(pl.N.info[g[0]["netz"]]["nanite"]),
                            "akteur": bool(g[0]["akteur"])}
            if g[0]["akteur"]:
                dateien[key]["rolle"] = "akteur"
                for e in g:
                    a = {"netz": pl.N.info[e["netz"]]["name"], "pfad": e["pfad"], "thema": thema,
                         "klasse": e["rolle"] if e["rolle"] != "akteur" else ("turm" if e["extra"].get("turm") else "hero_block"),
                         "x": round(e["x"], 1), "y": round(e["y"], 1), "z": round(e["z"], 1),
                         "qx": round(e["q"][0], 6), "qy": round(e["q"][1], 6), "qz": round(e["q"][2], 6), "qw": round(e["q"][3], 6),
                         "sx": round(e["s"][0], 4), "sy": round(e["s"][1], 4), "sz": round(e["s"][2], 4),
                         "groesse_m": round(e["d_m"], 2), "kollision": bool(e["kol"]),
                         "nanite": bool(pl.N.info[e["netz"]]["nanite"])}
                    for kk, vv in sorted(e["extra"].items()):
                        a[kk] = vv
                    akteure.append(a)
        n = sum(d["anzahl"] for k, d in dateien.items() if not d["akteur"])
        kol = sum(d["anzahl"] for k, d in dateien.items() if d["kollision"] and not d["akteur"])
        plan = {"stand": STAND, "feld": feld, "thema": thema, "kuerzel": kuerzel, "variante": pl.variante,
                "instanzen": n, "kollision_anzahl": kol, "akteure_anzahl": len(akteure),
                "fenster_m": list(pl.K.fenster_m),
                "dateien": dateien, "akteure": akteure, "entfernen": "",
                "ft_ordner": "/Game/Eldarien/Welt/Foliage/Felsdeckung/%s" % thema.capitalize(),
                "ft_praefix": "FT_EL_%s_" % kuerzel,
                "ziel_ordner_lokal": "export/unreal/welt/%s/%s/" % (thema, feld),
                "hinweis_setzer": ("Generischer FORMAT-§3-Setzer: f32 je Netz (10 float32), Foliage-Typ = ft_praefix + "
                                   "Dateischluessel; Dateien mit 'akteur_' bzw. rolle 'akteur' als StaticMeshActor "
                                   "(Liste 'akteure', identisch in akteure_%s.json). z enthaelt das Eingraben. "
                                   "Reihenfolge: 1. Ausduenn-Maske anwenden, 2. Lagen, 3. Themen klippenband -> halde -> "
                                   "platten -> baumgruppen setzen. Kuerzel nie 'BACH*'." % feld)}
        with open(os.path.join(ordner, "plan.json"), "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=1)
        akteure_alle.extend(akteure)
        zusammen[thema] = {"instanzen": n, "kollision": kol, "akteure": len(akteure), "dateien": len(dateien)}
        log("geschrieben %s: %d Instanzen (%d Kollision), %d Akteure, %d Dateien" % (ordner, n, kol, len(akteure), len(dateien)))
    with open(os.path.join(aus, "akteure_%s.json" % feld), "w", encoding="utf-8") as f:
        json.dump({"stand": STAND, "feld": feld, "variante": pl.variante, "anzahl": len(akteure_alle),
                   "hinweis": "Grosse Module als StaticMeshActor (Turmklotz, Hero-Bloecke >= 6 m). Wand-/Bandreihen "
                              "sind bewusst Foliage (ISM, Kollision) - Akteur-Budget <= 40 je Fenster (Ladehaenger ab "
                              "200+ Akteuren je Zelle).",
                   "akteure": akteure_alle}, f, ensure_ascii=False, indent=1)
    return zusammen


def rastere_fussabdruecke(pl, fe, zelle_m, nur=None, saum_m=0.0):
    """Bool-Maske (Fenster fe, Zellgroesse zelle_m) der Fussabdruck-Ellipsen (x 0,85 = Netz ist keine Box)."""
    X, Y = fe.gitter_m() if hasattr(fe, "gitter_m") else fe
    m = np.zeros(X.shape, bool)
    x0, y0 = float(X[0, 0]), float(Y[0, 0])
    for e in pl.stuecke:
        if nur is not None and e["thema"] + ":" + e["rolle"] not in nur and e["thema"] not in nur:
            continue
        mx, my, a, b, w = e["fuss"]
        a, b = a * 0.85 + saum_m, b * 0.85 + saum_m
        r = max(a, b)
        j0 = max(0, int((mx - r - x0) / zelle_m))
        j1 = min(X.shape[1], int((mx + r - x0) / zelle_m) + 2)
        i0 = max(0, int((my - r - y0) / zelle_m))
        i1 = min(X.shape[0], int((my + r - y0) / zelle_m) + 2)
        if j1 <= j0 or i1 <= i0:
            continue
        xx = X[i0:i1, j0:j1] - mx
        yy = Y[i0:i1, j0:j1] - my
        c, s = math.cos(w), math.sin(w)
        u = (xx * c + yy * s) / max(a, 0.05)
        v = (-xx * s + yy * c) / max(b, 0.05)
        m[i0:i1, j0:j1] |= (u * u + v * v) <= 1.0
    return m


def schreibe_masken(pl, welt, aus):
    """Lagen (A15/s38-Format lagen/<id>_<Lage>.r8), Grasdichte, Ausduenn-Maske, Zonenkarte (alle 1 m, Fenster)."""
    K, R = pl.K, pl.R
    x0, y0, x1, y1 = K.fenster_m
    feld = K.feld
    lg = ST.Lagen(welt, x0, y0, x1 - 0.01, y1 - 0.01, seed=pl.seed)
    fe = lg.fe
    sl_i = slice(fe.i0 - K.fe.i0, fe.i1 - K.fe.i0)
    sl_j = slice(fe.j0 - K.fe.j0, fe.j1 - K.fe.j0)
    zone = K.zone[sl_i, sl_j]
    t = K.t_halde[sl_i, sl_j]
    L = R["lagen"]
    alle = rastere_fussabdruecke(pl, fe, K.z, nur=["halde", "klippenband", "platten", "baumgruppen:fussblock",
                                                    "baumgruppen:totholz"], saum_m=L["stueck_saum_m"])
    platten = rastere_fussabdruecke(pl, fe, K.z, nur=["platten:platte"], saum_m=0.5)
    lg.maske("Geroell", ((zone == ZONEN["halde"]) * (1.0 - 0.35 * t)).astype(np.float64), L["geroell_halde"])
    lg.maske("Geroell", alle.astype(np.float64), L["geroell_unter_stueck"])
    lg.maske("Felsplatte", platten.astype(np.float64), L["felsplatte_unter_platte"])
    lg.maske("Fels", np.isin(zone, [ZONEN["schrofen"], ZONEN["wand"]]).astype(np.float64), L["fels_schrofen_wand"])
    blk = lg.schreibe(aus, "felsdeckung_%s" % feld)
    # Grasdichte (Faktor), Ausduennen, Zonen
    Gr = R["gras"]
    unter = rastere_fussabdruecke(pl, fe, K.z, nur=["halde", "klippenband", "platten:platte", "baumgruppen:fussblock"])
    ring = rastere_fussabdruecke(pl, fe, K.z, nur=["halde:block", "platten:platte", "baumgruppen:fussblock"],
                                 saum_m=Gr["fugen_ring_m"][1]) & ~rastere_fussabdruecke(
        pl, fe, K.z, nur=["halde:block", "platten:platte", "baumgruppen:fussblock"], saum_m=Gr["fugen_ring_m"][0])
    X, Y = fe.gitter_m()
    fl = ST.rauschen(X, Y, Gr["flecken_wellenlaenge_m"], pl.seed + 61)
    thr_h = float(np.quantile(fl, 1.0 - Gr["flecken_anteil_halde"]))
    thr_f = float(np.quantile(fl, 1.0 - Gr["flecken_anteil_fuss"]))
    gras = np.full(zone.shape, 255.0)
    fels = np.isin(zone, [ZONEN["halde"], ZONEN["schrofen"], ZONEN["wand"]])
    gras[fels] = np.where(fl[fels] >= thr_h, 255.0, 0.0)
    fz = zone == ZONEN["fuss"]
    gras[fz] = np.where(fl[fz] >= thr_f, 255.0, 60.0)
    gras[ring] = 255.0
    gras[unter] = 0.0
    A = R["ausduennen"]
    luecke = K.n_luecke[sl_i, sl_j]
    weg = (zone == ZONEN["wand"]) | ((zone == ZONEN["halde"]) & (t < A["halde_bis_t"])) | \
        ((zone == ZONEN["schrofen"]) & (luecke < A["schrofen_insel_schwelle"])) | \
        (K.d_grat[sl_i, sl_j] < A["grat_band_m"]) | \
        (np.isin(zone, [ZONEN["fuss"], ZONEN["hangwald"]]) & (luecke < A["luecke_schwelle"]))
    weg &= zone != ZONEN["sperre"]
    namen = {}
    os.makedirs(os.path.join(aus, "masken"), exist_ok=True)
    for name, a in (("grasdichte", gras), ("ausduennen", weg.astype(np.float64) * 255.0),
                    ("zonen", zone.astype(np.float64))):
        a1 = ST.nach_1m(a, K.z)
        if name == "zonen":
            a1 = np.repeat(np.repeat(zone, int(round(K.z)), 0), int(round(K.z)), 1)[: a1.shape[0], : a1.shape[1]]
        elif name == "ausduennen":
            a1 = np.where(a1 >= 127.5, 255.0, 0.0)
        rel = "masken/%s_%s.u8" % (name, feld)
        np.ascontiguousarray(np.clip(np.rint(a1), 0, 255).astype(np.uint8)).tofile(os.path.join(aus, rel))
        namen[name] = {"datei": rel, "form": [int(a1.shape[0]), int(a1.shape[1])]}
    fij = [int(v) for v in fe.fenster_ij_1m()]
    meta = {"stand": STAND, "feld": feld, "fenster_ij": fij, "fenster_m": list(K.fenster_m),
            "lagen": blk, "masken": namen,
            "zonen_codes": ZONEN,
            "grasdichte_hinweis": "Faktor 0-255 auf die GT-Dichtekarten (welt/*.r8) im Fenster multiplizieren, dann "
                                  "rebuild_grass_maps + grass.FlushCache; 0 = kein Gras (unter Stuecken), 255 = Fugenring "
                                  "und Flecken.",
            "ausduennen_hinweis": "255 = Altbestand entfernen (remove_foliage_by_mask), NUR Baum-Typen des Altbestands "
                                  "(Houdini-Baeume, FT_EL_WIT_* Hangwald/Haine, FT_EL_BST_*), nie FT_EL_FS_*/FT_EL_FG_*/"
                                  "Bachdekor/Ufer. Vor dem Setzen der neuen Themen anwenden.",
            "anteil_ausduennen_fenster": round(float(weg.mean()), 3)}
    with open(os.path.join(aus, "masken_%s.json" % feld), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return meta


# ============================================================================================
# Variante B: Schuettkegel (A15)
# ============================================================================================
def plane_kegel(welt, regeln):
    """Delta (m, natives Fensterraster inkl. Rand) fuer Schuettkegel. Rueckgabe (delta, kegel_liste)."""
    K = Kontext(welt, regeln)
    Gk = regeln["gelaende"]
    z = K.z
    rand = np.zeros(K.h.shape, bool)
    ab = G.abfluss(K.h.astype(np.float32), z, rand)
    acc = ab["akkumulation_m2"].astype(np.float64)
    wand = K.zone == ZONEN["wand"]
    fuss_kante = (~wand) & (K.d_wand <= 1.5 * z) & (K.d_wand > 0) & (K.n < 45.0) & K.innen & \
        (K.d_wasser > Gk["wasser_frei_m"] + Gk["kegel_radius_m"] * 0.6) & (K.d_weg > 10.0)
    rp = int(round(40.0 / z))
    oben = G.max_filter(K.h.astype(np.float32), rp).astype(np.float64) - K.h
    fuss_kante &= oben >= Gk["min_relief_oben_m"]
    x0, y0, x1, y1 = K.fenster_m
    R_ = Gk["kegel_radius_m"]
    fuss_kante &= (K.X - x0 >= R_) & (x1 - K.X >= R_) & (K.Y - y0 >= R_) & (y1 - K.Y >= R_)
    ii, jj = np.nonzero(fuss_kante)
    o = np.lexsort((jj, ii, -acc[ii, jj]))
    schutz = ST.abfall(K.d_wasser, Gk["wasser_frei_m"] + 2.0, Gk["wasser_frei_m"] + 6.0)   # +2 m: 2-m-Raster bilinear
    schutz = np.maximum(schutz, ST.abfall(K.d_weg, Gk["weg_frei_m"], Gk["weg_frei_m"] + 4.0))
    dr = np.minimum(np.minimum(K.X - x0, x1 - K.X), np.minimum(K.Y - y0, y1 - K.Y))
    randf = ST.glatt01((dr - z) / Gk["rand_m"]) * K.innen
    kegel = []
    delta = np.zeros(K.h.shape)
    n_gepr = 0
    for k in o:
        if len(kegel) >= Gk["kegel_anzahl"] or n_gepr >= 400:
            break
        x, y = float(K.X[ii[k], jj[k]]), float(K.Y[ii[k], jj[k]])
        if any(math.hypot(x - c["x_m"], y - c["y_m"]) < Gk["kegel_abstand_m"] for c in kegel):
            continue
        n_gepr += 1
        c = {"x_m": round(x, 2), "y_m": round(y, 2), "z_m": round(float(K.h[ii[k], jj[k]]), 2),
             "einzug_m2": round(float(acc[ii[k], jj[k]]), 0)}
        r9 = int(round(5.0 / z))
        i, j = int(ii[k]), int(jj[k])
        gx = float(K.gx[max(0, i - r9): i + r9 + 1, max(0, j - r9): j + r9 + 1].mean())
        gy = float(K.gy[max(0, i - r9): i + r9 + 1, max(0, j - r9): j + r9 + 1].mean())
        nn = math.hypot(gx, gy) or 1.0
        dx, dy = -gx / nn, -gy / nn
        c["fallrichtung_kompass"] = round(kompass(dx, dy), 1)
        vx, vy = K.X - x, K.Y - y
        r = np.hypot(vx, vy)
        cosphi = (vx * dx + vy * dy) / np.maximum(r, 1e-6)
        phi = np.degrees(np.arccos(np.clip(cosphi, -1, 1)))
        S = Gk["kegel_sektor_grad"]
        ws = ST.abfall(phi, 0.6 * S, S)
        wr = ST.abfall(r, 0.75 * R_, R_)
        a_o, a_u = math.radians(Gk["kegel_winkel_oben_grad"]), math.radians(Gk["kegel_winkel_unten_grad"])
        alpha = a_o + (a_u - a_o) * np.clip(r / (2 * R_), 0, 0.5)
        zc = c["z_m"] + 0.5 - r * np.tan(alpha)
        d = np.maximum(0.0, zc - K.h) * ws * wr
        d = Gk["kegel_max_m"] * np.tanh(d / Gk["kegel_max_m"])
        d = d * (1.0 - schutz) * randf
        vol = float(d.sum() * z * z)
        if vol < Gk["min_volumen_m3"]:
            continue
        delta = np.maximum(delta, d)
        c["max_auftrag_m"] = round(float(d.max()), 2)
        c["volumen_m3"] = round(vol, 0)
        kegel.append(c)
    delta[~K.innen] = 0.0
    return delta, kegel, K


def schreibe_gelaende(welt, regeln, aus):
    delta, kegel, K = plane_kegel(welt, regeln)
    x0, y0, x1, y1 = K.fenster_m
    fe = welt.fenster_box(x0, y0, x1 - 0.01, y1 - 0.01)
    sl_i = slice(fe.i0 - K.fe.i0, fe.i1 - K.fe.i0)
    sl_j = slice(fe.j0 - K.fe.j0, fe.j1 - K.fe.j0)
    d1 = ST.nach_1m(delta[sl_i, sl_j], K.z).astype("<f4")
    ordner = os.path.join(aus, "gelaende_%s_variante_b" % K.feld)
    os.makedirs(os.path.join(ordner, "gelaende"), exist_ok=True)
    rel = "gelaende/halde_kegel_%s.f32" % K.feld
    np.ascontiguousarray(d1).tofile(os.path.join(ordner, rel))
    plan = {"stand": STAND, "format": "A15 (wie gefaelle/<lauf>/plan.json, p2_bett_welt.py)", "variante": "B (optional)",
            "abschnitte": [{"id": "halde_kegel_%s" % K.feld, "feld": K.feld,
                            "gelaende": {"datei": rel, "fenster_ij": [int(v) for v in fe.fenster_ij_1m()],
                                         "max_aenderung_m": round(float(np.abs(d1).max()), 2), "modus": "add",
                                         "einheit": "Delta in m, 1-m-Raster, float32 LE zeilenweise"}}],
            "kegel": kegel,
            "volumen_auftrag_m3": round(float(delta.sum() * K.z * K.z), 0),
            "regeln": {k: v for k, v in regeln["gelaende"].items() if not k.startswith("_")},
            "reihenfolge_lokal": ["Feld B5 komplett: hoehen -> 40 s -> lagen -> rest (a15_einbau / s38-Kette)",
                                  "Gras-Karten neu (grass_maps_check 'falsch 0 max 0'), Nanite je Teil",
                                  "shift_foliage_by_height_delta fuer Bestand im Fenster",
                                  "Planer mit --gelaende neu laufen lassen (Instanzen auf dem neuen Boden), dann setzen"],
            "hinweis": "Nur anheben (Auftrag), >= 12 m vom Wasser (Uferband A20 unberuehrt), >= 4 m von Wegen, Rand 8 m weich."}
    with open(os.path.join(ordner, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    log("Variante B: %d Kegel, max %.2f m, Auftrag %.0f m3 -> %s" % (len(kegel), float(np.abs(d1).max()),
                                                                   plan["volumen_auftrag_m3"], ordner))
    return delta, kegel, plan


# ============================================================================================
# Statistik
# ============================================================================================
def statistik(pl, aus):
    K = pl.K
    x0, y0, x1, y1 = K.fenster_m
    fl = {}
    for name, code in ZONEN.items():
        fl[name] = round(float(((K.zone == code) & K.innen).sum() * K.z * K.z) / 10000.0, 3)
    je = {}
    for e in pl.stuecke:
        k = "%s:%s" % (e["thema"], e["rolle"])
        je[k] = je.get(k, 0) + 1
    tri = 0
    for e in pl.stuecke:
        tri += int(pl.inv.netze[e["pfad"]].get("dreiecke") or 0) if hasattr(pl.inv, "netze") and e["pfad"] in pl.inv.netze else 0
    st = {"stand": STAND, "feld": K.feld, "variante": pl.variante, "fenster_m": list(K.fenster_m),
          "fenster_ha": round((x1 - x0) * (y1 - y0) / 10000.0, 2), "zonen_ha": fl, "je_rolle": dict(sorted(je.items())),
          "planer": pl.stat, "stuecke": len(pl.stuecke),
          "akteure": sum(1 for e in pl.stuecke if e["akteur"]),
          "kollision": sum(1 for e in pl.stuecke if e["kol"] and not e["akteur"]),
          "netze_unterschiedlich": len({e["pfad"] for e in pl.stuecke}),
          "dreiecke_summe_quellnetze": tri,
          "netz_fehler": pl.N.fehler}
    with open(os.path.join(aus, "statistik_%s.json" % K.feld), "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    return st


# ============================================================================================
def main(argv=None):
    ap = argparse.ArgumentParser(description="Felsdeckung Auftrag 21 - Pilotplaner (FORMAT-3)")
    ap.add_argument("--regeln", default=os.path.join(HIER, "felsdeckung_regeln.json"))
    ap.add_argument("--aus", required=True, help="Ausgabeordner (z. B. recherche/antworten/felsdeckung)")
    ap.add_argument("--daten2m", default=None)
    ap.add_argument("--daten1m", default=None, help="export/unreal/welt (lokal, 1 m)")
    ap.add_argument("--inventar", default=None, help="Ordner mit netze.csv usw. (Standard vorlagen/daten)")
    ap.add_argument("--gelaende", action="store_true", help="Variante B: Instanzen auf dem Gelaende nach den Schuettkegeln")
    ap.add_argument("--bild", action="store_true", help="Bilder (Draufsicht, Delta-Karte, Querschnitte, Skizze)")
    a = ap.parse_args(argv)
    t0 = time.time()
    with open(a.regeln, "r", encoding="utf-8") as f:
        regeln = json.load(f)
    try:
        welt = D.lade(daten2m=a.daten2m, daten1m=a.daten1m, pfade=False)
    except FileNotFoundError as e:
        log("FEHLER Weltdaten fehlen: %s" % e)
        return 2
    inv = INV.Inventar.lade(a.inventar)
    os.makedirs(a.aus, exist_ok=True)
    delta_b, kegel, plan_b = schreibe_gelaende(welt, regeln, a.aus)
    pl = Planer(welt, regeln, inv, delta=delta_b if a.gelaende else None, variante="B" if a.gelaende else "A")
    if pl.N.fehler:
        for t in pl.N.fehler:
            log("HINWEIS Netz ausgelassen: %s" % t)
    pl.plane()
    zus = schreibe_themen(pl, a.aus)
    meta = schreibe_masken(pl, welt, a.aus)
    st = statistik(pl, a.aus)
    st["themen"] = zus
    if a.bild:
        import felsdeckung_bilder as FB
        FB.alle(pl, welt, regeln, a.aus, delta_b, kegel)
    log("fertig: %d Stuecke (%d Akteure, %d Kollision) in %.1f s" % (st["stuecke"], st["akteure"], st["kollision"],
                                                                    time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, HIER)
    sys.exit(main())
