"""selbsttest_13h.py - Schritt 12 des Selbsttests (Auftrag 13h): Steilflaechen-Regel, Boeschung, Kameras, Leuchtfeuer,
Bloecke im See. Synthetische Faelle plus ein Stempel in der 2-m-Welt (Karsee B5); schreibt nichts.

Aufruf ueber selbsttest.py (Schritt 12) oder direkt: python -I selbsttest_13h.py
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


def test_13h(welt=None, inv=None):
    """Rueckgabe: Anzahl FEHLER."""
    from . import steilwand as sw, kamera_frei as kf, see_bloecke as sb, stempel as stm, instanzen as ins
    from . import inventar as _inv, daten as _daten
    f = []
    # --- 1 Steilflaechen-Regel (synthetisch, 1 m)
    X, Y = np.meshgrid(np.arange(60, dtype=float), np.arange(60, dtype=float))
    h0 = 100.0 + 0.36 * X                                     # ~20 Grad
    h1 = h0.copy()
    wand = (X >= 30) & (X < 34) & (Y >= 10) & (Y < 50)
    h1[X >= 30] -= 6.0                                        # 6-m-Abbruch (senkrecht)
    neu = sw.neue_steil_maske(h0, h1, 1.0)
    lab, gr = sw.komponenten(neu)
    _pruefe(max(gr or [0]) > sw.MIN_FLAECHE_M2, "Abbruch 6 m -> neu steil %d m2 > 20 m2 (FEHLER-Fall)" % max(gr or [0]), f)
    a = {"poly": [[27.0, -1.0], [36.0, -1.0], [36.0, 61.0], [27.0, 61.0]], "zmin": 80.0, "zmax": 130.0,
         "box": (27.0, -1.0, 36.0, 61.0)}
    ged = sw.deckung(X, Y, h1, [a], nur=neu) & neu
    _pruefe(int((neu & ~ged).sum()) == 0, "Fels-Abdruck ueber der Kante deckt alle Zellen", f)
    a2 = dict(a, zmin=200.0, zmax=210.0)
    ged2 = sw.deckung(X, Y, h1, [a2], nur=neu) & neu
    _pruefe(int(ged2.sum()) == 0, "Abdruck auf falscher Hoehe (+100 m) deckt nichts", f)
    _pruefe(sw.ist_fels("/Game/Fab/Megascans/3D/Sharp_Cliff_rcygn/Raw/rcygn_tier_0/StaticMeshes/rcygn_tier_0")
            and sw.ist_fels("SM_big_rock_wall_01") and not sw.ist_fels("SM_Forest_pine_09")
            and not sw.ist_fels("SM_stones_roots_04"), "Fels-Heuristik (Klippe/Wand ja, Baum/Wurzel nein)", f)
    hu = sw.huelle([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)])
    _pruefe(len(hu) == 4, "konvexe Huelle", f)
    # --- 2 Boeschung im Stempel (2-m-Welt, Bachterrasse am Saeulenhain B5, Hang ~15 Grad)
    if welt is not None:
        st = stm.Stempel.um(welt, -2764.0, 104.0, 120.0)
        st.mulde(-2764.0, 104.0, 12.0, 7.0, rand_m=1.0, boden=0.9)
        st.fertig(schutz=False)
        vor = sw.neue_steil_maske(st.h0, st.h0 + st.delta, st.z, grenze_grad=40.0).sum()
        fest = st.randfaktor() < 0.999
        auf, ab = st.boeschung(35.0, fest=fest, max_auftrag_m=4.0, max_abtrag_m=4.0)
        nach = sw.neue_steil_maske(st.h0, st.h0 + st.delta, st.z, grenze_grad=40.0).sum()
        _pruefe(vor > 0 and nach < 0.2 * vor, "Boeschung 35 Grad: neue Steilzellen %d -> %d (Halde %.0f m2, Abtrag %.0f m2)"
                % (vor, nach, auf, ab), f)
        _pruefe(bool(getattr(st, "halde", np.zeros(1)).any()), "Halde-Maske fuer Geroell/Bloecke gesetzt", f)
    # --- 3 Kameras (Kronenabstand, Strahl)
    inv = inv or _inv.Inventar.lade()
    info = inv.netz("Fir_07_Forest")
    q = ins.orientierung("aufrecht", 0.0)
    s = (2.6, 2.6, 2.6)
    baum = kf._hindernis(info, info["pfad"], 0.0, 0.0, 10000.0, q, s, ort="t_01_x", gruppe="riesen", ebene="held")
    _pruefe(baum["typ"] == "baum" and baum["r_krone"] > 5.0, "Fir_07_Forest x2,6 = Baum, Kronenradius %.1f m"
            % baum.get("r_krone", 0), f)
    boden = (lambda x, y: np.full(np.shape(np.asarray(x, float)), 100.0) if np.ndim(x) else 100.0)
    ort = {"id": "t_01_x", "wasser": [], "art": "fundstueck", "mitte_cm": [0, 0], "radius_m": 20.0}
    if welt is not None:
        k_nah = ["A1", 400, 0, 2000, 0, 10100, "t_01_x_nah", -170]          # 4 m neben dem Stamm
        b1 = kf.pruefe_kamera(k_nah, ort, welt, boden, [baum], bestand=False)
        _pruefe(any("Kronenradius" in t for _, t in b1), "Kamera 4 m vom Stamm -> FEHLER Kronenabstand", f)
        k_frei = ["A1", 0, 3000, 2500, 3000, 10100, "t_01_x_nah", -170]     # 30 m daneben, Strahl frei
        b2 = kf.pruefe_kamera(k_frei, ort, welt, boden, [baum], bestand=False)
        _pruefe(not b2, "Kamera mit Abstand und freiem Strahl -> 0 FEHLER", f)
        k_durch = ["A1", -2500, 0, 2500, 0, 10500, "t_01_x_nah", -170]      # Strahl durch die Krone
        b3 = kf.pruefe_kamera(k_durch, ort, welt, boden, [baum], bestand=False)
        _pruefe(any("verdeckt" in t for _, t in b3), "Strahl durch die Krone -> FEHLER verdeckt", f)
    # --- 4 Leuchtfeuer: Riesen-Regel gegen den Bestand (Saeulenhain B5)
    if welt is not None:
        mx, my = -2764.0, 104.0
        bz = float(welt.hoehe_bei_m(mx, my))
        hoch = [kf._hindernis(info, info["pfad"], (mx + dx) * 100, (my + dy) * 100, bz * 100, q, s, ort="t_03_x",
                              gruppe="riesen", ebene="held") for dx, dy in ((0, 0), (10, 5), (-8, 6))]
        klein = [kf._hindernis(info, info["pfad"], (mx + dx) * 100, (my + dy) * 100, bz * 100, q, (1.0, 1.0, 1.0),
                               ort="t_03_x", gruppe="riesen", ebene="held") for dx, dy in ((0, 0), (10, 5), (-8, 6))]
        o3 = {"id": "t_03_x", "art": "leuchtfeuer", "mitte_cm": [mx * 100, my * 100], "radius_m": 45.0, "kameras": []}
        bh, _ = kf.pruefe_leuchtfeuer(o3, welt, welt.hoehe_bei_m, hoch)
        bk, _ = kf.pruefe_leuchtfeuer(o3, welt, welt.hoehe_bei_m, klein)
        _pruefe(not bh and any("1.5 x Bestand" in t for _, t in bk),
                "Riesen 57 m bestehen, 22-m-Tannen nicht (>= 1,5 x Bestand)", f)
    # --- 5 Bloecke im See (Nachtrag 01:00)
    _pruefe(sb._im_band(255.0, 256.0) and not sb._im_band(256.4, 256.0) and not sb._im_band(254.4, 256.0),
            "Band: Oberkante -1,0 m FEHLER, +0,4 m und -1,6 m erlaubt", f)
    log("  Schritt 12 (13h): %d FEHLER" % len(f))
    return len(f)


if __name__ == "__main__":
    from . import daten as _d
    sys.exit(1 if test_13h(_d.lade(pfade=False)) else 0)
