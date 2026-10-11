#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sehens_gletscher.py - Sehenswuerdigkeiten-Planer Gletscher (Auftrag 13, Phase 2; Muster: sehens_bergwald).

Baut die 8 Gletscher-Orte aus sehens/gletscher/standorte.json nach den Rezepten in sehens_gletscher_regeln.json
(Katalog sehens/gletscher/katalog.md inkl. 'Abgleich 13b/13c', asset_bedarf.json) und schreibt das Lieferformat
vorlagen/SEHENS_FORMAT.md:
  <aus>/orte.json, <aus>/gelaende/<id>.f32, <aus>/lagen/<id>_<Lage>.r8      (§2, §3)
  <sw>/<Feld>/plan.json + <Netz>.f32 (Ebene sw_gletscher, FORMAT.md §3)         (§4)
  Wasser §5, Effekte §6 (Niagara optional), Materialwuensche §7, Kameras §8 (aus standorte.json), Budgets §9
  Bild je Ort test_<id>.png (--bild)

Aufruf (python -I, NumPy + Pillow):
  python -I sehens_gletscher.py --daten2m recherche/vorlagen/daten/sehens --aus <Ordner> [--ort ID ...] [--bild]
  python -I sehens_gletscher.py --basis <production>            # 1 m aus export/unreal/welt, Ausgabe dort
Optionen: --orte/--ort ID ... (nur diese Orte; Orte in denselben Feldern werden mitgeplant, damit plan.json
  vollstaendig bleibt), --bild (test_<id>.png), --bild-ordner, --sw-aus (Ebene sw_gletscher), --regeln, --inventar,
  --sehens (Ordner mit <biom>/standorte.json), --cache, --ohne-pruefung, --ohne-sicht (keine Verdeckungspruefung).
Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.

Eigener Code (alles andere steht in den Regeln), fuer alle Orte gleich:
  - Hook 'rahmen' (nach_gelaende, vor nach_ops): Sichtrahmen fuer Fundstuecke. Sucht die Weg-/Steigpunkte (<= r_max_m), die den Ort heute
    sehen, legt in ihrer Richtung einen Wall (Moraene, Schneewall, Felsriegel) im Abstand abstand_m um den Ort, so hoch,
    wie die Sichtlinien es verlangen (begrenzt auf hoehe_max_m), und setzt die Linie 'rahmen_<name>' fuer Gruppen
    (Felsen, Gehoelz auf dem Wall). Zufall deterministisch aus Seed + Ort-ID.
  - Hook 'nach_ops' (nach_gelaende): Werkzeuge, die rezept.py nicht als Regel kennt (damm = Stempel.damm).
  - Hook 'see_fuellen' (anker): See fuellt eine bestehende geschlossene Senke bis knapp unter den Ueberlauf.
  - Hook 'ende': Wasser-Regeln mit "eis": true / "material_wunsch" / "hinweis" werden in orte.json uebernommen
    (zugefrorene Flaechen, Mountain-Fluss-/Wasserfallmaterial);
    Fundstuecke: Verdeckungspruefung mit Stempel + geplanten Stuecken (sehens_lib/verdeckung.py) als HINWEIS.
Quellen: vorlagen/SEHENS_FORMAT.md, vorlagen/FORMAT.md §3, auftraege/13-, 13b-, 13c-*.md,
antworten/skripte/sehens_lib/ (README.md, PLANER_ANLEITUNG.md).
"""

import argparse
import copy
import json
import math
import os
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HIER))          # antworten/skripte (python -I setzt das nicht)

BIOM = "gletscher"
_WP = {}


def _log(*t):
    from sehens_lib import ascii_text
    sys.stdout.write("[sehens_%s] %s\n" % (BIOM, " ".join(ascii_text(x) for x in t)))
    sys.stdout.flush()


def abbruch(text, code=2):
    _log("FEHLER:", text)
    sys.exit(code)


def _wegpunkte(welt):
    from sehens_lib import sicht
    if id(welt) not in _WP:
        _WP[id(welt)] = sicht.Wegpunkte(welt, 20)
    return _WP[id(welt)]


# ----------------------------------------------------------------------------------------------------------------------
# Hooks (Formen, die sich nicht als Regel ausdruecken lassen)
# ----------------------------------------------------------------------------------------------------------------------
def hook_rahmen(ctx):
    """Sichtrahmen (Fundstueck): Wall in Richtung der Weg-/Steigpunkte, die den Ort heute sehen.
    Regel "rahmen": [{"name", "bei", "ziel_hoehe_m" (3), "r_min_m" (0), "r_max_m" (800), "richtung_bereich" [g0, g1]
    (nur Blicke aus diesem Sektor), "abstand_m", "breite_m", "hoehe_min_m", "hoehe_max_m", "rand_grad" (Zugabe an den
    Bogenenden), "richtung" + "bogen_grad" (Bogen, falls heute niemand den Ort sieht), "krone"}].
    Je Blickpunkt wird die Wallhoehe berechnet, die seine Sichtlinie zur Zieloberkante im Abstand abstand_m schneidet;
    der Wall folgt den Blickrichtungen, die mit hoehe_max_m sperrbar sind. Ergebnis: gelaende.nach_ops += damm,
    Linie rahmen_<name>, Anker rahmen_<name>_mitte, Meldung (wie viele Blicke der Wall sperrt, Rest fuer Gehoelz/Felsen)."""
    import numpy as np
    from sehens_lib import sicht, verdeckung, stempel as stm
    if not ctx.r.get("rahmen"):
        return
    w_plan = verdeckung.welt_mit_plan(ctx.welt, ctx.stempel)     # Gelaende mit den bisherigen Stempeln (Terrasse, See)
    for k, rr in enumerate(ctx.r.get("rahmen") or []):
        name = rr.get("name", "r%d" % k)
        x, y = ctx.punkt(rr.get("bei", "mitte"))
        H = float(rr.get("ziel_hoehe_m", 3.0))
        wp = _wegpunkte(ctx.welt)
        idx, d = wp.im_ring(x, y, float(rr.get("r_min_m", 0.0)), float(rr.get("r_max_m", 800.0)))
        r = float(rr.get("abstand_m", 20.0))
        z_t = float(ctx.boden(x, y)) + H
        sel = np.zeros(0, int)
        if idx.size:
            a, _, dd = sicht.sichtanteil(w_plan, wp.x_m[idx], wp.y_m[idx], x, y, H)
            sel = np.flatnonzero(a > 0.15)
        g_v = np.array([stm.vektor_kompass(wp.x_m[idx[i]] - x, wp.y_m[idx[i]] - y) for i in sel])
        if rr.get("richtung_bereich") and len(sel):
            g0_, g1_ = rr["richtung_bereich"]
            innen = ((g_v - g0_) % 360.0) <= ((g1_ - g0_) % 360.0)
            sel, g_v = sel[innen], g_v[innen]
        h_max, h_min = float(rr.get("hoehe_max_m", 7.0)), float(rr.get("hoehe_min_m", 2.0))
        bedarf = []
        for i, gv in zip(sel, g_v):
            px, py = x + r * math.sin(math.radians(gv)), y - r * math.cos(math.radians(gv))
            D = max(float(d[idx[i]]), r + 1.0)
            z_e = float(wp.z_m[idx[i]]) + 1.7
            bedarf.append(z_t + (z_e - z_t) * r / D + 0.5 - float(ctx.boden(px, py)))
        bedarf = np.asarray(bedarf)
        sperrbar = bedarf <= h_max
        g_s = g_v[sperrbar] if sperrbar.any() else g_v
        if len(g_s):
            mx_, my_ = np.mean(np.sin(np.radians(g_s))), np.mean(-np.cos(np.radians(g_s)))
            g0 = stm.vektor_kompass(mx_, my_)
            dev = np.abs((g_s - g0 + 180.0) % 360.0 - 180.0)
            halb = min(180.0, float(dev.max()) + float(rr.get("rand_grad", 15.0)))
        else:
            g0 = ctx.richtung(rr.get("richtung", 0.0), rr.get("bei", "mitte"))
            halb = 0.0
        halb = max(halb, float(rr.get("bogen_grad", 60.0)) / 2.0)
        n = max(3, int(math.ceil(2 * halb * math.pi / 180.0 * r / 3.0)) + 1)
        gg = np.linspace(g0 - halb, g0 + halb, n) if halb < 180.0 else np.linspace(0, 360, n)
        P = [[x + r * math.sin(math.radians(g)), y - r * math.cos(math.radians(g))] for g in gg]
        h_req = float(bedarf[sperrbar].max()) if sperrbar.any() else 0.0
        hoehe = float(np.clip(h_req, h_min, h_max))
        ops = ctx.r.setdefault("gelaende", {}).setdefault("nach_ops", [])
        ops.insert(0, {"op": "damm", "punkte": [{"pos_m": p} for p in P], "breite_m": float(rr.get("breite_m", 14.0)),
                    "hoehe_m": hoehe, "krone": float(rr.get("krone", 0.3)), "modus": rr.get("modus", "add"),
                    "warum": "Sichtrahmen %s (Fundstueck)" % name})
        ctx.linien["rahmen_" + name] = P
        ctx.anker["rahmen_%s_mitte" % name] = (x + r * math.sin(math.radians(g0)), y - r * math.cos(math.radians(g0)))
        ctx.richtungen["rahmen_" + name] = g0
        rest = "" if sperrbar.all() else "; %d Blicke steiler (Wall muesste bis %.0f m hoch sein) - Gehoelz/Felsen auf " \
                                         "dem Wall, Rest siehe Verdeckung" % (int((~sperrbar).sum()), float(bedarf.max()))
        ctx.melde("HINWEIS", "Rahmen %s: %d Weg-/Steigpunkte sehen den Ort heute; Wall %.1f m in %.0f m Abstand, Richtung "
                             "%.0f +-%.0f Grad, sperrt %d%s" % (name, len(sel), hoehe, r, g0, halb, int(sperrbar.sum()), rest))


def hook_see_fuellen(ctx):
    """Seen mit "fuellen": {"r_such_m", "unter_rand_m"} fuellen eine bestehende geschlossene Senke bis knapp unter
    ihren Ueberlauf (Toteisloch): Mitte, Radius (flaechengleich) und Spiegel aus dem Bestand (gefuellt - Boden)."""
    import numpy as np
    from sehens_lib import gelaende as _g
    for w in ctx.r.get("wasser") or []:
        f = w.get("fuellen")
        if w.get("typ") != "see" or not f:
            continue
        x, y = ctx.punkt(w.get("bei", "mitte"))
        fe = ctx.welt.fenster(x, y, float(f.get("r_such_m", 40.0)))
        h = fe.get("hoehe").astype(np.float32)
        r_ = _g.abfluss(h, ctx.welt.zelle_m, np.zeros(h.shape, bool))
        tief = r_["gefuellt"] - h
        X, Y = fe.gitter_m()
        m = (tief > 0.2) & (np.hypot(X - x, Y - y) <= float(f.get("r_such_m", 40.0)) * 0.8)
        if not m.any():
            ctx.melde("HINWEIS", "see %s: keine Senke zum Fuellen gefunden" % w["id"])
            continue
        ueberlauf = float(r_["gefuellt"][m].max())
        spiegel = ueberlauf - float(f.get("unter_rand_m", 0.4))
        nass = m & (h < spiegel)
        if not nass.any():
            nass = m
        cx, cy = float(X[nass].mean()), float(Y[nass].mean())
        rad = max(3.0, math.sqrt(nass.sum() * ctx.welt.zelle_m ** 2 / math.pi) + 0.5)
        w["bei"] = {"pos_m": [cx, cy]}
        w["spiegel"] = round(spiegel, 2)
        w.pop("spiegel_rand_min", None)
        b = w.setdefault("becken", {})
        b["a_m"] = b["b_m"] = round(rad, 1)
        w.pop("r_m", None)
        ctx.melde("HINWEIS", "see %s gefuellt: Ueberlauf %.2f m, Spiegel %.2f m, Mitte %.0f/%.0f, r %.1f m"
                  % (w["id"], ueberlauf, spiegel, cx, cy, rad))


def hook_nach_ops(ctx):
    """gelaende.nach_ops: Werkzeuge nach den Seebecken (damm = Wall/Graben entlang einer Linie)."""
    for op in (ctx.r.get("gelaende") or {}).get("nach_ops") or []:
        if op["op"] == "damm":
            ctx.stempel.damm(ctx.linie(op["punkte"]), float(op["breite_m"]), float(op["hoehe_m"]),
                             krone=float(op.get("krone", 0.3)), verjuengung_m=op.get("verjuengung_m"),
                             geschlossen=bool(op.get("geschlossen", False)), modus=op.get("modus", "add"))
        else:
            ctx.melde("FEHLER", "gelaende.nach_ops: %r unbekannt" % op["op"])


def _senken_ort(ctx):
    """Lage geschlossener Senken (falls rezept.py WARNUNG meldet) als HINWEIS fuer die Nacharbeit."""
    import numpy as np
    st = ctx.stempel
    sk = st.senken(wasser=ctx._wasser_maske_fenster(st.fe))
    if sk["flaeche_m2"] <= 0:
        return
    m = sk["maske"]
    X, Y = st.X, st.Y
    # Zusammenhaengende Teile (4er-Nachbarschaft), die groessten zuerst
    frei = m.copy()
    teile = []
    for i0, j0 in zip(*np.nonzero(m)):
        if not frei[i0, j0]:
            continue
        stapel, zellen = [(i0, j0)], []
        frei[i0, j0] = False
        while stapel:
            i, j = stapel.pop()
            zellen.append((i, j))
            for a_, b_ in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a_ < m.shape[0] and 0 <= b_ < m.shape[1] and frei[a_, b_]:
                    frei[a_, b_] = False
                    stapel.append((a_, b_))
        ii, jj = np.array(zellen).T
        teile.append((len(zellen) * st.z * st.z, float(X[ii, jj].mean()), float(Y[ii, jj].mean())))
    teile.sort(key=lambda t: -t[0])
    ctx.melde("HINWEIS", "Senke: %.0f m2 in %d Teilen: %s" % (sk["flaeche_m2"], len(teile), ", ".join(
        "%.0f m2 bei %.0f/%.0f" % t for t in teile[:5])))


def hook_ende(ctx):
    """Eisflaechen markieren, Verdeckung der Fundstuecke pruefen (nur Meldung)."""
    _senken_ort(ctx)
    regeln = {w.get("id"): w for w in (ctx.r.get("wasser") or [])}
    for e in ctx.wasser:
        w = regeln.get(e.get("id")) or {}
        if w.get("eis"):
            e["eis"] = True
        for k in ("material_wunsch", "hinweis"):
            if w.get(k):
                e[k] = (e[k] + "; " + w[k]) if (k == "hinweis" and e.get(k)) else w[k]
    if ctx.st.get("art") == "fundstueck" and not ctx.r.get("_ohne_sicht"):
        from sehens_lib import verdeckung
        kern = ctx.punkt(ctx.r["sicht_kern"]) if ctx.r.get("sicht_kern") else None
        res = verdeckung.pruefe_ort(ctx, _wegpunkte(ctx.welt), ziel_hoehe_m=float(ctx.r.get("sicht_ziel_m", 3.0)),
                                    probe_r_m=float(ctx.r.get("sicht_probe_m", 0.0)) or None, kern_m=kern,
                                    r_max_m=float(ctx.r.get("sicht_r_max_m", 800.0)))
        ctx.sicht_ergebnis = res
        ctx.melde("HINWEIS", res["text"])
        if not res["verdeckt"]:
            # wer sieht den Kern noch? (Richtung, Abstand, Hoehe ueber dem Ziel) - fuer Nacharbeit und Bericht
            import numpy as np
            from sehens_lib import sicht, stempel as stm
            wp = _wegpunkte(ctx.welt)
            x, y = res["kern_m"]
            w2 = verdeckung.welt_mit_plan(ctx.welt, ctx.stempel, verdeckung.stuecke_aus_ctx(ctx))
            idx, d = wp.im_ring(x, y, 0.0, float(ctx.r.get("sicht_r_max_m", 800.0)))
            a, _, _ = sicht.sichtanteil(w2, wp.x_m[idx], wp.y_m[idx], x, y, res["ziel_hoehe_m"])
            zt = float(w2.hoehe_bei_m(x, y))
            sel = np.flatnonzero(a > 0.15)
            liste = sorted((round(stm.vektor_kompass(wp.x_m[idx[k]] - x, wp.y_m[idx[k]] - y)), round(float(d[idx[k]])),
                            round(float(wp.z_m[idx[k]]) - zt)) for k in sel)
            ctx.melde("HINWEIS", "Verdeckung Rest (Richtung/Abstand/dz): %s" % ", ".join("%d/%d/%+d" % t for t in liste[:12]))


def _hooks(oid, R):
    h = {"anker": [hook_see_fuellen], "nach_gelaende": [hook_rahmen, hook_nach_ops], "ende": [hook_ende]}
    for k, f in (HOOKS.get(oid) or {}).items():
        h.setdefault(k, []).insert(0, f)
    return {k: (lambda ctx, fs=fs: [f(ctx) for f in fs]) for k, fs in h.items()}


HOOKS = {}


# ----------------------------------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Sehenswuerdigkeiten-Planer %s (Auftrag 13, Phase 2)" % BIOM)
    ap.add_argument("--orte", "--ort", nargs="+", default=None, dest="orte", help="nur diese Ort-IDs (Standard: alle 8)")
    ap.add_argument("--bild", action="store_true", help="Testbild test_<id>.png je geplantem Ort")
    ap.add_argument("--bild-ordner", default=None, help="Ordner fuer test_<id>.png (Standard: --aus)")
    ap.add_argument("--aus", default=None, help="Ausgabeordner (Standard <basis>/export/unreal/welt/sehens/%s)" % BIOM)
    ap.add_argument("--sw-aus", default=None, help="Ebene sw_%s (Standard: <aus>/sw_%s)" % (BIOM, BIOM))
    ap.add_argument("--basis", default=".", help="production-Wurzel (1-m-Daten in export/unreal/welt)")
    ap.add_argument("--regeln", default=os.path.join(HIER, "sehens_%s_regeln.json" % BIOM))
    ap.add_argument("--inventar", default=None, help="Ordner mit netze.csv, inventar_extra.json (Standard vorlagen/daten)")
    ap.add_argument("--sehens", default=None, help="Ordner antworten/sehens (standorte.json aller Biome)")
    ap.add_argument("--ohne-pruefung", action="store_true")
    ap.add_argument("--ohne-sicht", action="store_true", help="keine Verdeckungspruefung der Fundstuecke")
    ap.add_argument("--daten2m", default=None, help="2-m-PNGs (Cloud-Test): recherche/vorlagen/daten/sehens")
    ap.add_argument("--daten1m", default=None, help="1-m-Originale (Standard <basis>/export/unreal/welt)")
    ap.add_argument("--cache", default=None)
    a = ap.parse_args(argv)
    T0 = time.perf_counter()

    from sehens_lib import daten, gelaende, inventar, instanzen, rezept, vorschau, sehens_pruefen, log  # noqa: F401
    from sehens_lib import format as sfmt

    # --- Regeln, Inventar, Standorte
    if not os.path.exists(a.regeln):
        abbruch("Regeln fehlen: %s" % a.regeln)
    with open(a.regeln, "r", encoding="utf-8") as f:
        R = json.load(f)
    try:
        inv = inventar.Inventar.lade(a.inventar)
    except FileNotFoundError as ex:
        abbruch(str(ex))
    sehens = a.sehens or daten.standard_pfad_sehens()
    st_pfad = os.path.join(sehens, BIOM, "standorte.json")
    if not os.path.exists(st_pfad):
        abbruch("standorte.json fehlt: %s" % st_pfad)
    standorte = sfmt.lade_standorte(st_pfad)
    pfade_biom = [p for p in (standorte.get("pfade") or [])]

    # --- Daten
    daten1m = a.daten1m
    if not a.daten2m and not daten1m:
        daten1m = os.path.join(a.basis, "export", "unreal", "welt")
        if not os.path.isdir(daten1m):
            abbruch("weder --daten2m noch 1-m-Daten (%s) gefunden" % daten1m)
    try:
        welt = daten.lade(a.daten2m, daten1m, pfade=sehens)
    except (FileNotFoundError, ValueError) as ex:
        abbruch("Daten: %s" % ex)
    gel = gelaende.Gelaende(welt, cache=a.cache)
    _log(welt.info())

    # --- Ausgabe
    if a.aus:
        aus = os.path.abspath(a.aus)
        sw = os.path.abspath(a.sw_aus or os.path.join(aus, "sw_" + BIOM))
    else:
        aus = os.path.join(a.basis, "export", "unreal", "welt", "sehens", BIOM)
        sw = a.sw_aus or os.path.join(a.basis, "export", "unreal", "welt", "sw_" + BIOM)
    os.makedirs(aus, exist_ok=True)

    # --- Orte waehlen (mit --orte: alle Orte in denselben Feldern mitplanen, plan.json bleibt vollstaendig)
    alle = {o["id"]: o for o in standorte["orte"]}
    gewaehlt = list(alle) if not a.orte else a.orte
    for oid in gewaehlt:
        if oid not in alle:
            abbruch("Ort %s nicht in %s" % (oid, st_pfad))
        if oid not in R["orte"]:
            abbruch("Ort %s hat kein Rezept in %s" % (oid, a.regeln))
    felder = {f for oid in gewaehlt for f in alle[oid].get("felder", [])}
    planen = [oid for oid in alle if oid in gewaehlt or felder & set(alle[oid].get("felder", []))]
    if len(planen) > len(gewaehlt):
        _log("mitgeplant (gleiche Felder): %s" % ", ".join(sorted(set(planen) - set(gewaehlt))))
    mitten = {o["id"]: (o["mitte_cm"][0] / 100.0, o["mitte_cm"][1] / 100.0) for o in standorte["orte"]}

    ebene = instanzen.Ebene(BIOM, inv, stand=sfmt.heute())
    kontexte = []
    for oid in planen:
        t0 = time.perf_counter()
        regel = copy.deepcopy(R["orte"][oid])
        if a.ohne_sicht:
            regel["_ohne_sicht"] = True
        ctx = rezept.OrtKontext(welt, gel, inv, ebene, alle[oid], regel, BIOM, seed=R.get("seed", 0),
                                pfade_biom=pfade_biom, paletten=R.get("paletten"), materialien=R.get("materialwuensche"),
                                orte_mitten=mitten)
        ctx.baue(_hooks(oid, R))
        kontexte.append(ctx)
        z = ebene.zaehle(oid)
        _log("%-30s %5d Instanzen (%4d Kollision), %3d Akteure, Stempel %.1f m  %.1f s"
             % (oid, z["instanzen"], z["kollision"], z["akteure"], ctx.stempel.max_aenderung_m, time.perf_counter() - t0))

    # alte Eintraege (bei --orte) erhalten
    alte = None
    pj = os.path.join(aus, "orte.json")
    if a.orte and os.path.exists(pj):
        with open(pj, "r", encoding="utf-8") as f:
            alte = json.load(f).get("orte", [])
    d, info = rezept.schreibe_biom(aus, sw, BIOM, kontexte, ebene, R.get("materialwuensche", []), inv, alte_orte=alte)

    # --- Bilder
    if a.bild:
        bo = a.bild_ordner or aus
        for ctx in kontexte:
            if ctx.id in gewaehlt:
                p = vorschau.vorschau(ctx, os.path.join(bo, "test_%s.png" % ctx.id), groesse_m=ctx.r.get("bild_groesse_m"))
                _log("Bild:", p)

    # --- Meldungen der Orte
    meld = [m for c in kontexte for m in c.meldungen]
    for st in ("FEHLER", "WARNUNG"):
        for s, oid, t in meld:
            if s == st:
                _log("  %-7s %-28s %s" % (s, oid[:28], t))
    for c in kontexte:
        for s, oid, t in c.meldungen:
            if s == "HINWEIS" and (t.startswith("Rahmen") or t.startswith("Verdeckung") or t.startswith("Senke") or t.startswith("see ")):
                _log("  %-7s %-28s %s" % (s, oid[:28], t))
    _log("Planer: %d FEHLER, %d WARNUNG, %d HINWEIS" % tuple(sum(1 for m in meld if m[0] == s)
                                                         for s in ("FEHLER", "WARNUNG", "HINWEIS")))
    rc = 1 if any(m[0] == "FEHLER" for m in meld) else 0

    # --- Pruefer (SEHENS_FORMAT)
    if not a.ohne_pruefung:
        bef = sehens_pruefen.pruefe_orte(d, basis=aus, inv=inv, welt=welt, sw_ordner=sw)
        z = sehens_pruefen.melde(bef, "orte.json + sw_%s" % BIOM)
        if z["FEHLER"]:
            rc = 1
    # --- Zusammenfassung
    _log("-" * 72)
    for o in d["orte"]:
        b = o["budget"]
        _log("%-30s Inst %5d  Koll %4d  Akt %3d  Licht %d  Niagara %d  Nebel %d  Decal %2d  Stempel %4.1f m"
             % (o["id"], b["instanzen"], b["kollision"], b["akteure"], b["lichter"], b["niagara"], b.get("nebel", 0),
                b["decals"], (o.get("gelaende") or {}).get("max_aenderung_m", 0.0)))
    for feld, i in sorted(info.items()):
        _log("Feld %s: %d Instanzen, %d Kollision, %d Akteure (%s)" % (feld, i["instanzen"], i["kollision"],
                                                                         i["akteure"], ", ".join(i["orte"])))
    for h in ebene.hinweise:
        _log("Hinweis:", h)
    _log("Ausgabe: %s  |  Ebene: %s  |  %.1f s" % (aus, sw, time.perf_counter() - T0))
    return rc


if __name__ == "__main__":
    sys.exit(main())
