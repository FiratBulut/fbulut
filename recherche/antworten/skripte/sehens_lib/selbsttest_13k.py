"""selbsttest_13k.py - Schritt 13 des Selbsttests (Auftrag 13k): Saegeschnitt-Regel, Fern-Achse (Gelaende und
Baumkronen), Flaechen > 60 Grad, Strahlbreite an der Lippe, Schaumhuelle der Treppenbaeche, Cull der Vorhang-Stufen,
Seefarbe bergsee. Nur synthetische Faelle (plus Inventar); schreibt nichts.

Aufruf ueber selbsttest.py (Schritt 13) oder direkt: python -I selbsttest_13k.py
"""

import math
import os
import sys

import numpy as np

if __name__ == "__main__" and __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "sehens_lib"
    import sehens_lib  # noqa: F401

from . import log  # noqa: E402


def _pruefe(bed, text, fehler):
    log(("  ok    " if bed else "  FEHLER ") + text)
    if not bed:
        fehler.append(text)


class _WeltBaum:
    """Minimal-Welt fuer die Kronenpruefung: 4-m-Baumraster mit einem Baum (20 m) bei (40, 0) m."""

    def __init__(self):
        from . import daten as _d
        self.baeume4 = np.zeros((1800, 2400), np.uint8)
        self.baumhoehe4 = np.zeros((1800, 2400), np.float32)
        i, j = _d.m_zu_pixel(np.array([40.0]), np.array([0.0]), 4.0)
        self.i, self.j = int(round(float(i[0]))), int(round(float(j[0])))


def test_13k(inv=None):
    """Rueckgabe: Anzahl FEHLER."""
    from . import inventar as _inv, kamera_frei as kf, steilwand as sw, bach as _b, format as _fmt
    from . import sehens_pruefen as sp
    f = []
    # --- 1 Saegeschnitt (Inventar)
    inv = inv or _inv.Inventar.lade()
    _pruefe(inv.saegeschnitt("SM_Forest_pine_04_01_log") is not None, "SM_Forest_pine_04_01_log = Saegeschnitt", f)
    _pruefe(inv.saegeschnitt("SM_Forest_pine_08_log") is not None, "SM_Forest_pine_08_log = Saegeschnitt", f)
    _pruefe(inv.saegeschnitt("SM_OldFallenTree_01") is None and inv.saegeschnitt("SM_detail_branches_01") is None
            and inv.saegeschnitt("SM_OldTreeBranch_04") is None, "OldFallenTree/detail_branches/OldTreeBranch erlaubt", f)
    _pruefe(any(s == "FEHLER" for s, _ in inv.netz_pruefen("SM_Forest_pine_04_02_log", wildnis=True)),
            "netz_pruefen(wildnis=True): gesaegtes Stueck -> FEHLER", f)
    _pruefe(not any(s == "FEHLER" for s, _ in inv.netz_pruefen("SM_Forest_pine_04_02_log")),
            "netz_pruefen ohne wildnis (A15) unveraendert", f)
    # --- 2 Bestandskronen (synthetisch): Strahl durch eine Krone sperrt, daneben frei
    w = _WeltBaum()
    w.baeume4[w.i, w.j] = 1
    w.baumhoehe4[w.i, w.j] = 20.0
    from . import daten as _d
    cx, cy = _d.pixel_zu_m(w.i, w.j, 4.0)
    boden = lambda x, y: np.zeros(np.broadcast(np.asarray(x), np.asarray(y)).shape)   # noqa: E731
    X = np.array([float(cx), float(cx), float(cx) + 8.0])
    Y = np.array([float(cy), float(cy), float(cy)])
    Z = np.array([12.0, 3.0, 12.0])
    t = kf.bestand_kronen_treffer(w, boden, X, Y, Z)
    _pruefe(bool(t[0]) and not t[1] and not t[2], "Krone 20 m: Punkt in 12 m Hoehe getroffen, in 3 m (Stamm) und 8 m "
                                                     "daneben frei", f)
    ok1, _ = kf._strahl_frei(w, boden, [], None, float(cx) - 30.0, float(cy), 12.0, float(cx) + 400.0, float(cy), 12.0,
                             10.0)
    ok2, _ = kf._strahl_frei(w, boden, [], None, float(cx) - 30.0, float(cy) + 12.0, 12.0, float(cx) + 400.0,
                             float(cy) + 12.0, 12.0, 10.0)
    _pruefe((not ok1) and ok2, "Fern-Strahl durch die Krone gesperrt, 12 m daneben frei", f)
    # --- 3 Flaechen > 60 Grad: Wand zum Ort gewandt wird erfasst, abgewandte nicht
    X, Y = np.meshgrid(np.arange(80, dtype=float), np.arange(80, dtype=float))
    h = np.where(X < 50, 100.0, 100.0 + (X - 50) * 3.0)          # Wand steigt nach Osten (~72 Grad), schaut nach Westen
    s1 = sw.neigung_grad(h, 1.0)
    m = sw.steil60_bereich_maske(X, Y, h, s1, 20.0, 40.0, 60.0, np.zeros(h.shape, bool))
    _pruefe(int(m.sum()) > 100, "Wand > 60 Grad zum Ort gewandt: %d m2 erfasst (bis zur Oberkante)" % int(m.sum()), f)
    h2 = np.where(X > 30, 100.0, 100.0 + (30 - X) * 3.0)         # Wand faellt nach Osten (Ort im Westen sieht Rueckseite)
    s2 = sw.neigung_grad(h2, 1.0)
    m3 = sw.steil60_bereich_maske(X, Y, h2, s2, 75.0, 40.0, 40.0, np.zeros(h.shape, bool))
    _pruefe(int(m3.sum()) == 0, "abgewandte Wand ausserhalb 40 m: nichts erfasst", f)
    # --- 4 Strahlbreite an der Lippe (Trapez wie das 13f-Querprofil)
    B, tief = 2.5, 0.3
    bett = lambda x, y: np.where(np.abs(np.asarray(y)) <= B / 2 - tief / _b.TAN_B, 99.7,   # noqa: E731
                                  99.7 + (np.abs(np.asarray(y)) - (B / 2 - tief / _b.TAN_B)) * _b.TAN_B) + 0 * np.asarray(x)
    sb = _b.lippen_strahl(0.0, 0.0, 1.0, 0.0, 100.0, B, bett, 0.8, tief)
    _pruefe(sb is not None and 0.5 < sb["strahl_breite_m"] < sb["wasserbreite_m"] <= B + 0.2
            and sb["strahl_breite_m"] < sb["lippe_breite_m"],
            "Strahl %.2f m < Wasserbreite %.2f m < Lippe %.2f m (Q %.3f m3/s, krit. Tiefe %.3f m)"
            % (sb["strahl_breite_m"], sb["wasserbreite_m"], sb["lippe_breite_m"], sb["abfluss_m3_s"], sb["krit_tiefe_m"])
            if sb else "Strahlbreite berechnet", f)
    # --- 5 Schaumhuelle: Becken <= 0,2, Fallfuss mit Abklingen, Fallflaeche <= 0,45
    S = np.arange(0.0, 12.0, 0.1)
    c = _b.schaum_huelle(S, [(1.0, 1.5, 3.0, "fall", 8.0), (8.0, 8.5, 1.5, "fall", 14.0)])
    becken = (S > 1.5 + 0.3 + 2.5 + 0.1) & (S < 8.0 - 0.8)
    _pruefe(float(c[becken].max()) <= 0.2 + 1e-9, "Becken hinter dem Abklingen <= 0,2 (max %.2f)" % float(c[becken].max()), f)
    _pruefe(float(c[(S > 1.05) & (S < 1.45)].max()) <= 0.5 and float(c[(S >= 1.5) & (S <= 1.8)].min()) >= 0.64,
            "Fallflaeche <= 0,5 (Saum)/0,45, Fallfuss-Spitze >= 0,65", f)
    _pruefe(c[np.searchsorted(S, 2.8)] < c[np.searchsorted(S, 2.0)], "Schaum klingt hinter dem Fuss ab", f)
    # Pruefer: Becken mit Schaum 0,6 -> FEHLER
    kb = {"id": "T_KN0", "knick": ["lippe", "bogen", "fuss"] + ["becken"] * 12 + ["lippe"],
          "mittellinie_s_m": [0.0, 0.3, 0.5] + list(np.arange(1.0, 7.0, 0.5)) + [7.5],
          "mittellinie": [[0, 0, 300, 250, 0, 0, 0, 0], [0, 0, 250, 250, 0, 0, 0, 0], [0, 0, 100, 250, 0, 0, 0, 0]] +
                         [[0, 0, 100, 250, 0, 0, 0, 0]] * 13}
    kb["quer"] = [[[0.0, 1.0, 0.6, 30.0]] * 21 for _ in range(16)]
    _pruefe(any(s_ == "FEHLER" and "Becken" in t_ for s_, _, t_ in sp.pruefe_schaum_sehens(kb, "T")),
            "Pruefer: Schaum 0,6 im Becken -> FEHLER", f)
    kb["quer"] = [[[0.0, 1.0, 0.1, 30.0]] * 21 for _ in range(16)]
    _pruefe(not [1 for s_, _, t_ in sp.pruefe_schaum_sehens(kb, "T") if s_ == "FEHLER"], "Pruefer: Becken 0,1 -> ok", f)
    # --- 6 Cull an Vorhang-Stufen
    _pruefe(_b.cull_vorhang(3.0) == 60.0 and _b.cull_vorhang(10.8) == 80.0 and 60.0 < _b.cull_vorhang(6.0) < 80.0,
            "Cull 60 m bei 3 m, 80 m ab 10 m Fall", f)
    # --- 7 Seefarbe bergsee
    wf = _fmt.wasser_farben_block(["bergsee", "tiefblau"])
    _pruefe(wf and wf["bergsee"]["absorption"] == [8, 45, 40, 8] and "bergsee" in sp.FARBEN,
            "Seefarbe bergsee (Ferat C: Absorption 8/45/40/8 cm) in FARBEN und orte.json", f)
    return len(f)


if __name__ == "__main__":
    n = test_13k()
    log("Selbsttest 13k: %d FEHLER" % n)
    sys.exit(1 if n else 0)
