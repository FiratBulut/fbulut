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
    return len(f)


if __name__ == "__main__":
    sys.exit(1 if test_16c() else 0)
