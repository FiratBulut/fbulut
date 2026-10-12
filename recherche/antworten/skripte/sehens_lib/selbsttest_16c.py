"""selbsttest_16c.py - Schritt 14 des Selbsttests (Auftrag 16c, Nachtrag 18:15): Bachbett-Regeln (Netze natuerlich und im
Inventar, Dichten je Biom), Lippenzonen (schraeg, quer begrenzt), schnelle Projektion, Schlamm/Uferstreifen-Lagen,
Gras-Daempfung, Dichte- und Streifen-Bewertung, Erkennbarkeit im fluss_sim-Export. Nur synthetische Faelle (plus
Inventar und Regeldateien); schreibt nichts.

Aufruf ueber selbsttest.py (Schritt 14) oder direkt: python -I selbsttest_16c.py
"""

import json
import os
import re
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


def test_16c(inv=None):
    """Rueckgabe: Anzahl FEHLER."""
    from . import bachbett as bb, inventar as _inv, stempel as _st
    f = []
    R = bb.regeln()
    inv = inv or _inv.Inventar.lade()
    # --- 1 Regeln: Netze im Inventar, natuerlich (kein Saegeschnitt), keine Pflanzen; Lagen exakt FORMAT.md
    fs_pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fluss_sim", "fluss_sim_regeln.json")
    pflanze = holz = None
    if os.path.exists(fs_pfad):
        with open(fs_pfad, "r", encoding="utf-8") as fh:
            k = json.load(fh)["kollision"]
        pflanze, holz = re.compile(k["pflanze_muster"], re.I), re.compile(k["holz_muster"], re.I)
    fehlt, saege, pfl, lagen_falsch = [], [], [], []
    for bn, b in R.r["biome"].items():
        for art in ("stamm", "ast", "zweig", "wurzel"):
            for n in b[art]:
                if inv.netz_pfad(n) is None:
                    fehlt.append(n)
                elif inv.saegeschnitt(n):
                    saege.append(n)
                if pflanze is not None and pflanze.search(n):
                    pfl.append(n)
        for n in list(b["streifen"]) + [b["becken"]]:
            if n not in _st.LAGEN:
                lagen_falsch.append(n)
    _pruefe(not fehlt, "alle Bachbett-Netze in netze.csv (%s)" % (", ".join(fehlt[:3]) or "-"), f)
    _pruefe(not saege, "kein Saegeschnitt in den Bachbett-Paletten (inventar.saegeschnitt)", f)
    _pruefe(not pfl, "kein Bachbett-Netz faellt unter fluss_sim pflanze_muster (Wasser-Kollision moeglich)", f)
    _pruefe(not lagen_falsch, "Streifen-/Beckenlagen exakt aus FORMAT.md (Schlamm, Erde, Moos, ...)", f)
    _pruefe(R.biom("Schlamm")[0] == "tundra" and "Schlamm" in _st.LAGEN, "Lage 'Schlamm' vorhanden, unbekanntes Biom -> tundra", f)
    zl = {bn: b["lw_je_100m"] for bn, b in R.r["biome"].items()}
    _pruefe(all(a <= z <= c for a, z, c in zl.values()), "Dichten min <= Ziel <= max je Biom", f)
    wald = min(zl[b][1] for b in ("bergwald", "aue", "elfenwald", "sumpf", "dschungel"))
    karg = max(zl[b][1] for b in ("tundra", "wueste", "lava", "gletscher", "frost"))
    _pruefe(wald >= 3 * karg and all(zl[b][2] == 0 for b in ("lava", "gletscher", "frost")),
            "Waldbiome >= 3 x Tundra/Wueste, Lava/Gletscher/Frost ohne Holz (Ziel Wald %.0f, karg %.0f)" % (wald, karg), f)
    if holz is not None:
        _pruefe(all(holz.search(n) for n in ("SM_OldFallenTree_01", "SM_LargeFallenTree_02", "SM_FallenSpruceTree_01")),
                "Staemme erkennt der fluss_sim-Export auch am Namen als Holz", f)
    # --- 2 Lippenzonen: gerade, schraeg, quer begrenzt; Vorhang groesser
    st_g = {"s_lippe": 10.0, "s_fuss": 10.5, "fall": 0.6, "gross": False, "halb": 2.0}
    z = bb.lippen_zonen([st_g], R)
    _pruefe(bool(bb.in_zonen(np.array([10.2]), z, np.array([0.0]))[0]) and not bool(bb.in_zonen(np.array([11.5]), z,
                                                                                                    np.array([0.0]))[0]),
            "Lippenzone gerade: s 10,2 drin, 11,5 frei (Fuss + 0,5 m)", f)
    _pruefe(not bool(bb.in_zonen(np.array([10.2]), z, np.array([1.9]))[0]),
            "an den Lippenenden (|u| > Lippenbreite/2 - 0,3 m) frei (verkeiltes Holz erlaubt)", f)
    st_v = dict(st_g, fall=3.5, gross=True)
    zv = bb.lippen_zonen([st_v], R)
    _pruefe(bool(bb.in_zonen(np.array([11.8]), zv, np.array([0.0]))[0]), "Vorhang/Stufe >= 1 m: Aufprall bis Fuss + 1,5 m", f)
    st_s = dict(st_g, tan=0.5, pfeil=0.0, h=2.0)
    zs = bb.lippen_zonen([st_s], R)
    _pruefe(bool(bb.in_zonen(np.array([10.8]), zs, np.array([1.0]))[0]) and
            not bool(bb.in_zonen(np.array([10.8]), zs, np.array([-1.0]))[0]),
            "schraege Lippe: Zone folgt dem Versatz (u +1 drin, u -1 frei)", f)
    lfd = bb.Lippenfeld([st_s], [(0.0, 20.0)])
    _pruefe(abs(float(lfd.s_eff(10.0, 1.0)) - 9.5) < 1e-9 and abs(float(lfd.s_eff(0.0, 1.0))) < 1e-9,
            "Lippenfeld: s_eff an der Lippe = s - Versatz, an der Segmentgrenze 0", f)
    # --- 3 Projektion wie stempel.polylinie_abstand
    rng = np.random.default_rng(16)
    P = np.cumsum(rng.normal(size=(80, 2)), 0)
    x, y = rng.uniform(-10, 10, 400), rng.uniform(-10, 10, 400)
    a1 = _st.polylinie_abstand(x, y, P)
    a2 = bb.projektion_schnell(x, y, P, 64)
    _pruefe(all(float(np.abs(p - q).max()) < 1e-9 for p, q in zip(a1, a2)), "projektion_schnell = polylinie_abstand", f)
    # --- 4 Lagen: Uferstreifen 0-1 m ueber dem Spiegel, Schlamm im ruhigen tiefen Becken, Gleithang
    X, Y = np.meshgrid(np.arange(-10.0, 10.5, 0.5), np.zeros(1))
    X, Y = X.ravel(), Y.ravel()
    d = np.abs(X)
    halb = np.full(X.shape, 2.0)
    zsp = np.zeros(X.shape)
    F = np.where(d < 2.0, -0.8, np.where(d < 4.0, 0.3, 2.0))      # Bett, flaches Ufer 0,3 m, dann 2 m hoch
    ruhe = np.ones(X.shape)
    kr = np.zeros(X.shape)
    lg, ws, wsch = bb.bett_lagen(X, Y, F, zsp, d, halb, ruhe, kr, "bergwald", np.ones(X.shape), R, seed=1)
    summe = sum(lg.get(n, 0.0) for n in R.biom("bergwald")[1]["streifen"])
    i_ufer = np.flatnonzero((d >= 2.5) & (d <= 3.5))
    i_hoch = np.flatnonzero(d >= 4.5)
    _pruefe(float(np.min(summe[i_ufer])) >= 250.0 and float(np.max(ws[i_hoch])) < 0.01,
            "Uferstreifen: 0,3 m ueber dem Spiegel deckend (>= 250), 2 m ueber dem Spiegel nichts", f)
    i_mitte = np.flatnonzero(d <= 1.0)
    _pruefe(float(np.min(wsch[i_mitte])) > 0.5, "Schlamm im ruhigen, 0,8 m tiefen Becken", f)
    lg0, ws0, wsch0 = bb.bett_lagen(X, Y, F, zsp, d, halb, np.zeros(X.shape), kr, "bergwald", np.ones(X.shape), R, seed=1)
    _pruefe(float(np.max(wsch0[i_mitte])) < 0.01, "kein Schlamm an Lippe/Schnelle (ruhe 0) -> Kies bleibt", f)
    Fg = np.where(d < 1.0, -0.8, np.where(d < 2.0, -0.2, 0.3))
    lgg, _, wschg = bb.bett_lagen(X, Y, Fg, zsp, d, halb, np.full(X.shape, 0.4), np.where(X > 0, 0.05, -0.05),
                                  "bergwald", np.ones(X.shape), R, seed=1)
    ig = np.flatnonzero((X > 1.0) & (X < 2.0))
    ia = np.flatnonzero((X < -1.0) & (X > -2.0))
    _pruefe(float(np.mean(wschg[ig])) > float(np.mean(wschg[ia])) + 0.2, "Gleithang (Innenufer, flach) mit Schlamm, "
            "Prallhang ohne", f)
    arr = {"Trockengras": np.full(X.shape, 160.0), "Kies": np.full(X.shape, 200.0)}
    bb.lagen_mischen(arr, lg, ws, wsch, R)
    _pruefe(float(np.max(arr["Trockengras"][i_ufer])) < 1.0 and float(np.min(arr["Trockengras"][i_hoch])) > 150.0,
            "Trockengras im Uferstreifen gedaempft (wie Nadelstreu 13k), weiter oben unveraendert", f)
    _pruefe(float(np.mean(arr["Kies"][i_mitte])) < 120.0 and float(np.min(arr["Kies"][i_hoch])) > 199.0,
            "Kies unter dem Schlamm gedaempft (Mittel %.0f), abseits unveraendert" % float(np.mean(arr["Kies"][i_mitte])), f)
    lgl, wsl, _ = bb.bett_lagen(X, Y, F, zsp, d, halb, ruhe, kr, "lava", np.ones(X.shape), R, seed=1)
    _pruefe("Schlamm" not in lgl and "Lavasand" in lgl, "Lava: Lavasand statt Schlamm", f)
    # --- 5 Bewertungen
    st, _ = bb.dichte_bewerten("bergwald", 1.0, 200.0, 30, 0, R, 30)
    _pruefe(st is None, "Dichte Bergwald 15/100 m im Rahmen", f)
    st, _ = bb.dichte_bewerten("bergwald", 1.0, 200.0, 80, 0, R, 80)
    _pruefe(st == "FEHLER", "Dichte Bergwald 40/100 m -> FEHLER (zu dicht)", f)
    st, _ = bb.dichte_bewerten("bergwald", 1.0, 200.0, 2, 0, R, 2)
    _pruefe(st == "FEHLER", "Dichte Bergwald 1/100 m auf 200 m -> FEHLER (zu duenn)", f)
    st, _ = bb.dichte_bewerten("bergwald", 1.0, 30.0, 0, 0, R, 0)
    _pruefe(st == "HINWEIS", "kurze Strecke ohne Holz -> nur HINWEIS", f)
    st, _ = bb.dichte_bewerten("tundra", 1.0, 200.0, 20, 0, R, 0)
    _pruefe(st == "HINWEIS", "Bestand (Holzstufen) ueber max, nichts dazugesetzt -> HINWEIS", f)
    st, _ = bb.dichte_bewerten("lava", 1.0, 200.0, 1, 0, R, 1)
    _pruefe(st == "FEHLER", "Lava mit Totholz -> FEHLER", f)
    h = np.array([0.1, 0.2, 0.3, 0.4, 1.5])
    dd = np.array([2.5, 2.5, 2.5, 2.5, 2.5])
    n, ant = bb.streifen_bewerten(h, dd, np.full(5, 2.0), np.ones(5, bool), np.array([255, 255, 255, 0, 0.0]), R)
    _pruefe(n == 4 and abs(ant - 0.75) < 1e-9, "Uferstreifen-Bewertung: 4 Uferzellen, 75 %% belegt (%d, %.2f)" % (n, ant), f)
    f += test_16c3(inv, R)
    f += test_16c4(R)
    return len(f)


class _BaumWelt:
    """Minimale Welt fuer bachbett.dichte(): nur das 4-m-Baumraster (ganze Welt, wie welt.baeume4)."""

    def __init__(self):
        from . import daten as _d
        self.baeume4 = np.zeros((int(np.ceil(_d.NY_1M / 4.0)), int(np.ceil(_d.NX_1M / 4.0))), np.uint8)

    def baeume_um(self, x, y, r, dicht=1):
        """Baeume (>= 5 m) in jeder dicht-ten 4-m-Zelle im Radius r um (x, y)."""
        from . import daten as _d
        i0, j0 = _d.m_zu_pixel(x - r, y - r, 4.0)
        i1, j1 = _d.m_zu_pixel(x + r, y + r, 4.0)
        for i in range(int(i0), int(i1) + 1):
            for j in range(int(j0), int(j1) + 1):
                if (i + j) % dicht == 0:
                    self.baeume4[i, j] = 1


def test_16c3(inv, R):
    """16c Nachtrag 3: Totholz nach Waldnaehe (auch in der Tundra), Treibholz vom Oberlauf, Lava ohne Holz, Ruhe aus
    dem Gefaelle (Roh-Laeufe), Feldgrenzen (Stufe nur in einem Plan), Export-Holzmuster fuer Aeste/Moosbaeume.
    Rueckgabe Liste der FEHLER-Texte."""
    from . import bachbett as bb
    f = []
    P = np.stack([np.linspace(0.0, 100.0, 51), np.full(51, 0.0)], 1)      # 100-m-Bach bei y = 0
    W0 = _BaumWelt()
    d0 = bb.dichte(W0, P, "tundra", R)
    _pruefe(abs(d0["lw"][1] - 3.0) < 1e-6 and d0["wald_gewicht"] == 0.0,
            "Tundra ohne Baeume am Ufer: Ziel 3/100 m ('kaum', Gewicht 0)", f)
    W1 = _BaumWelt()
    W1.baeume_um(50.0, 0.0, 70.0, dicht=4)
    d1 = bb.dichte(W1, P, "tundra", R)
    _pruefe(d1["wald_gewicht"] >= 0.99 and d1["wald_biom"] == "bergwald" and d1["lw"][1] >= 12.0 and
            d1["palette"] == "bergwald",
            "Tundra mit Baeumen am Ufer: Wald-Dichte (Bergwald x Waldfaktor, Ziel %.1f, Anteil %.2f)"
            % (d1["lw"][1], d1["wald_anteil"] or 0), f)
    db = bb.dichte(W1, P, "bergwald", R)
    _pruefe(abs(db["lw"][1] - 15.0 * db["wald_faktor"]) < 0.01, "Bergwald unveraendert: Ziel = 15 x Waldfaktor", f)
    W2 = _BaumWelt()
    W2.baeume_um(-200.0, 0.0, 60.0, dicht=3)
    ober = np.stack([np.linspace(-300.0, 0.0, 61), np.zeros(61)], 1)
    d2 = bb.dichte(W2, P, "gletscher", R, ober)
    pal = bb.paletten(R, d2)
    _pruefe(d2["treibholz"] > 0.9 and 1.5 <= d2["lw"][1] <= 2.5 and d2["lw"][0] == 0.0 and pal["stamm"] and
            d2["palette"] == "treibholz",
            "Gletscher, Oberlauf bewaldet: vereinzelt Treibholz (Ziel %.1f/100 m, kein Minimum, Treibholz-Palette)"
            % d2["lw"][1], f)
    d3 = bb.dichte(W2, P, "gletscher", R, None)
    _pruefe(d3["lw"][1] == 0.0 and d3["ast"] == 0.0, "Gletscher ohne Baeume und ohne Oberlauf: kein Holz", f)
    d4 = bb.dichte(W1, P, "lava", R)
    _pruefe(d4["lw"][1] == 0.0 and d4["wald_gewicht"] == 0.0, "Lava bleibt ohne Holz (kein wald_ersatz)", f)
    st, _ = bb.dichte_bewerten("tundra", 1.0, 200.0, 4, 0, R, 4, rahmen=d1)
    _pruefe(st == "FEHLER", "Tundra mit Ufer-Wald und nur 2/100 m -> FEHLER (zu duenn nach Waldnaehe)", f)
    st, _ = bb.dichte_bewerten("tundra", 1.0, 200.0, 26, 0, R, 26, rahmen=d1)
    _pruefe(st is None, "Tundra mit Ufer-Wald und 13/100 m im Rahmen", f)
    seg = {"s_m": [0, 100], "wald_faktor": d0["wald_faktor"], "wald_gewicht": 0.0, "rahmen_lw": d0["lw"]}
    _pruefe(len(bb.rahmen_vergleichen(seg, d1, "t")) >= 1 and not bb.rahmen_vergleichen(seg, d0, "t"),
            "Pruefer: Rahmen im Plan gegen nachgerechnet (Abweichung = FEHLER)", f)
    # Ruhe aus dem Gefaelle (Roh-Laeufe)
    s_ = np.arange(0.0, 200.0, 2.0)
    z_ = np.where(s_ < 100.0, 10.0 - 0.001 * s_, 9.9 - 0.04 * (s_ - 100.0))
    rf, Sg = bb.ruhe_aus_gefaelle(s_, z_, R)
    _pruefe(float(rf(50.0)) > 0.95 and float(rf(150.0)) < 0.05, "Roh-Lauf: Ruhe 1 bei 0,1 % Gefaelle, 0 bei 4 %", f)
    # Export: Aeste und Moosbaeume sind Holz
    fs_pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fluss_sim", "fluss_sim_regeln.json")
    if os.path.exists(fs_pfad):
        with open(fs_pfad, "r", encoding="utf-8") as fh:
            k = json.load(fh)["kollision"]
        holz, pflanze = re.compile(k["holz_muster"], re.I), re.compile(k["pflanze_muster"], re.I)
        namen = ["SM_OldTreeBranch_06", "SM_BrokenTreeBranch_01", "SM_MossyTree_01", "SM_Pine_broken_branch_04",
                 "SM_mountain_branch_01_06", "SM_detail_branches_01"]
        _pruefe(all(holz.search(n) and not pflanze.search(n) for n in namen),
                "fluss_sim holz_muster: Aeste und Moosbaeume als holz (nicht sonstiges)", f)
        alle = {n for b in R.r["biome"].values() for a in ("stamm", "ast", "wurzel") for n in b[a]}
        alle |= {n for a in ("stamm", "ast", "wurzel") for n in R.a["treibholz"][a]}
        rest = sorted(n for n in alle if not holz.search(n))
        _pruefe(not rest, "alle Stamm-/Ast-/Wurzel-Netze erkennt der Export als holz (%s)" % (", ".join(rest[:3]) or "-"), f)
    # Treibholz-Palette im Inventar, natuerlich
    tp = [n for a in ("stamm", "ast", "zweig", "wurzel") for n in R.a["treibholz"][a]]
    _pruefe(all(inv.netz_pfad(n) and not inv.saegeschnitt(n) for n in tp), "Treibholz-Palette im Inventar, ohne Saegeschnitt", f)
    # Feldgrenzen: Stufe nur in einem Plan
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gefaelle"))
        import gefaelle_daten as gd
        from . import daten as _d
        xg = _d.X_MIN_M + _d.FELD_M * 3 + 0.5                        # Feldgrenze (Spalte 3/4)
        Pp = [[(xg - 200.0 + k * 10.0) * 100, 0.0, 1000.0 - k * 10.0, 400.0] for k in range(23)]   # P bis xg + 20
        Pn = [[(xg - 10.0 + k * 10.0) * 100, 0.0, 810.0 - k * 10.0, 400.0] for k in range(20)]    # N ab xg - 10
        L_ = {"P": gd.Lauf("P", "fluss", Pp, _d.feld_von_m(xg - 50.0, 0.0)),
              "N": gd.Lauf("N", "fluss", Pn, _d.feld_von_m(xg + 50.0, 0.0))}
        fp, fn = gd.feldgrenzen("P", L_), gd.feldgrenzen("N", L_)
        ok = (len(fp) == 1 and len(fn) == 1 and fp[0]["seite"] == "ende" and fn[0]["seite"] == "anfang" and
              abs(fp[0]["fremd_s_m"][0] - 200.0) <= 0.6 and abs(fn[0]["fremd_s_m"][1] - 10.0) <= 0.6)
        _pruefe(ok, "Feldgrenze: Ueberlappung geteilt an der Feldgrenze (P fremd ab %.1f m, N fremd bis %.1f m)"
                % (fp[0]["fremd_s_m"][0] if fp and fp[0]["fremd_s_m"] else -1,
                   fn[0]["fremd_s_m"][1] if fn and fn[0]["fremd_s_m"] else -1), f)
        Ph = [[x_, y_, z_ + 50.0, b_] for x_, y_, z_, b_ in Pn]                                  # N 0,5 m hoeher
        L_h = {"P": L_["P"], "N": gd.Lauf("N", "fluss", Ph, L_["N"].feld)}
        fh = gd.feldgrenzen("N", L_h)
        _pruefe(fh and fh[0]["fremd_s_m"][1] > 10.5 and fh[0]["grenze_s_m"] == fh[0]["fremd_s_m"][1],
                "Feldgrenze: unterer Lauf 0,5 m hoeher -> Anschluss erst bei passendem Spiegel (fremd bis %.1f m)"
                % (fh[0]["fremd_s_m"][1] if fh else -1), f)
        L_["N"].feld = L_["P"].feld
        fp, fn = gd.feldgrenzen("P", L_), gd.feldgrenzen("N", L_)
        _pruefe(fp[0]["fremd_s_m"] is None and abs(fn[0]["fremd_s_m"][1] - fn[0]["ueberlappung_s_m"][1]) < 1e-6,
                "Feldgrenze im selben Feld: Ueberlappung gehoert dem oberen Lauf", f)
    except Exception as ex:                                           # pragma: no cover
        _pruefe(False, "Feldgrenzen-Test: %s" % ex, f)
    return f


class _HangWelt(_BaumWelt):
    """Baumraster plus analytisches Gelaende z = hoehe_fn(x, y) (fuer bachbett.baum_messung, 16c Nachtrag 4)."""

    def __init__(self, hoehe_fn):
        super().__init__()
        self.hoehe = "analytisch"
        self._h = hoehe_fn

    def bilinear(self, a, x, y):
        return self._h(np.asarray(x, np.float64), np.asarray(y, np.float64))


def test_16c4(R):
    """16c Nachtrag 4: Hangbaeume bis 150 m (oberhalb, zum Bach fallend, kein Ruecken dazwischen) zaehlen in den
    Nicht-Waldbiomen; Waldbiome unveraendert; Hindernis-Akteure: Komponenten nach Netz geteilt. Liste der FEHLER-Texte."""
    from . import bachbett as bb
    f = []
    P = np.stack([np.linspace(0.0, 100.0, 51), np.full(51, 0.0)], 1)      # 100-m-Bach bei y = 0, z = 0

    def tal(x, y):          # Nordhang (+y) 30 % Neigung; Sueden: Ruecken (15 m) bei y = -60, dahinter faellt es ab
        return np.where(y >= 0.0, 0.3 * y, np.where(y >= -60.0, 0.25 * -y, 15.0 - 0.3 * (-y - 60.0)))

    def baeume(W, y0, y1):
        from . import daten as _d
        for yy in np.arange(y0, y1 + 1e-6, 4.0):
            for xx in np.arange(0.0, 100.0 + 1e-6, 4.0):
                i, j = _d.m_zu_pixel(xx, yy, 4.0)
                W.baeume4[int(round(i)), int(round(j))] = 1
    W0 = _HangWelt(tal)
    d0 = bb.dichte(W0, P, "tundra", R)
    _pruefe(d0["wald_gewicht"] == 0.0 and d0.get("hang_anteil") == 0.0, "Hang ohne Baeume: kein Hang-Anteil", f)
    W1 = _HangWelt(tal)
    baeume(W1, 80.0, 120.0)
    d1 = bb.dichte(W1, P, "tundra", R)
    m1 = bb.baum_messung(W1, P, R, True)
    _pruefe(m1["ufer"] == 0.0 and m1["hang"] > 0.05 and d1["wald_gewicht"] >= 0.99 and d1["wald_biom"] == "bergwald",
            "Tundra, Baeume 80-120 m am Hang oberhalb: Hang-Anteil %.3f -> Wald-Dichte (Gewicht %.2f, Ziel %.1f/100 m)"
            % (m1["hang"], d1["wald_gewicht"], d1["lw"][1]), f)
    W2 = _HangWelt(tal)
    baeume(W2, -120.0, -80.0)
    m2 = bb.baum_messung(W2, P, R, True)
    _pruefe(m2["hang"] == 0.0 and m2["n_hang_baum"] > 0, "Baeume jenseits des Rueckens zaehlen nicht (%d Baumzellen, "
            "Gewicht %.3f)" % (m2["n_hang_baum"], m2["hang"]), f)
    W3 = _HangWelt(lambda x, y: np.zeros(np.shape(x)))
    baeume(W3, 80.0, 120.0)
    m3 = bb.baum_messung(W3, P, R, True)
    _pruefe(m3["hang"] == 0.0, "Baeume auf ebenem Gelaende 80-120 m zaehlen nicht (kein Hang)", f)
    W4 = _HangWelt(lambda x, y: -0.3 * np.abs(y))
    baeume(W4, 80.0, 120.0)
    m4 = bb.baum_messung(W4, P, R, True)
    _pruefe(m4["hang"] == 0.0, "Baeume tiefer als der Bach zaehlen nicht", f)
    W5 = _HangWelt(tal)
    baeume(W5, 156.0, 200.0)
    m5 = bb.baum_messung(W5, P, R, True)
    _pruefe(m5["hang"] == 0.0, "Baeume ueber 150 m zaehlen nicht", f)
    W6 = _HangWelt(tal)
    baeume(W6, 44.0, 60.0)
    m6 = bb.baum_messung(W6, P, R, True)
    _pruefe(m6["hang"] > m1["hang"] * (len(np.arange(44, 61, 4)) / len(np.arange(80, 121, 4))),
            "naehere Hangbaeume wiegen mehr (44-60 m: %.3f, 80-120 m: %.3f)" % (m6["hang"], m1["hang"]), f)
    db0, db1 = bb.dichte(W0, P, "bergwald", R), bb.dichte(W1, P, "bergwald", R)
    _pruefe(db0["lw"] == db1["lw"] and "hang_anteil" not in db1,
            "Waldbiom (Bergwald): Hangbaeume aendern nichts (Ufer-Anteil wie bisher)", f)
    seg = {"s_m": [0, 100], "wald_faktor": d1["wald_faktor"], "wald_gewicht": d1["wald_gewicht"], "rahmen_lw": d1["lw"]}
    _pruefe(not bb.rahmen_vergleichen(seg, bb.dichte(W1, P, "tundra", R), "t") and
            bb.rahmen_vergleichen(seg, bb.dichte(W2, P, "tundra", R), "t"),
            "Pruefer rechnet den Hang-Anteil nach (gleich: ok, Baeume hinter dem Ruecken: FEHLER)", f)
    # Hindernis-Akteure: mehr als instanzen_je_komponente_max Instanzen eines Netzes -> weitere Komponenten
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fluss_sim"))
        import fluss_sim_export as fx
        k = fx.hindernis_komponenten({"/G/A": list(range(9001)), "/G/B": list(range(3))}, {"instanzen_je_komponente_max": 4000})
        _pruefe([(c["netz"], len(c["instanzen"]), c.get("teil")) for c in k] ==
                [("/G/A", 4000, 1), ("/G/A", 4000, 2), ("/G/A", 1001, 3), ("/G/B", 3, None)],
                "WH_-Akteur: 9001 Instanzen eines Netzes -> 3 Komponenten (4000/4000/1001), kleines Netz ungeteilt", f)
    except Exception as ex:                                           # pragma: no cover
        _pruefe(False, "Hindernis-Komponenten-Test: %s" % ex, f)
    return f


if __name__ == "__main__":
    sys.exit(1 if test_16c() else 0)
