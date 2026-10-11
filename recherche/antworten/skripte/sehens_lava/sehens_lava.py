#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sehens_lava.py - Sehenswuerdigkeiten-Planer Lava (Auftrag 13, Phase 2, Biom-Agent B7).

Baut die 8 Lava-Orte aus sehens/lava/standorte.json nach den Rezepten in sehens_lava_regeln.json
(Katalog sehens/lava/katalog.md inkl. 'Abgleich mit Inventar 13b und Entscheidungen 13c', asset_bedarf.json) und
schreibt das Lieferformat vorlagen/SEHENS_FORMAT.md (Muster: skripte/sehens_bergwald/):
  <aus>/orte.json, <aus>/gelaende/<id>.f32, <aus>/lagen/<id>_<Lage>.r8      (§2, §3)
  <sw>/<Feld>/plan.json + <Netz>.f32 (Ebene sw_lava, FORMAT.md §3)              (§4)
  Wasser §5, Effekte §6 (Niagara optional), Materialwuensche §7 (6 von 6), Kameras §8 (aus standorte.json), §9
  Bild je Ort test_<id>.png (--bild)

Aufruf (python -I, NumPy + Pillow):
  python -I sehens_lava.py --daten2m recherche/vorlagen/daten/sehens --aus <Ordner> [--ort ID ...] [--bild]
  python -I sehens_lava.py --basis <production>            # 1 m aus export/unreal/welt, Ausgabe dort
Optionen wie sehens_bergwald.py: --orte/--ort, --bild, --bild-ordner, --sw-aus, --regeln, --inventar, --sehens,
  --cache, --ohne-pruefung. Exit-Code: 0 ok, 1 Pruefer meldet FEHLER, 2 Pflichtdatei fehlt.

Eigener Code (Hooks, alles andere steht in den Regeln):
  - 'zugang' (Regel-Schluessel): Ort am Steig (pfad_id) bekommt ZUSAETZLICH seinen Fussweg pfad_cm (Steig -> Ort)
    als Bodenband + Felsstufen; orte.json "pfad_zugang" (gleicher Aufbau wie "pfad").
  - 'pfade_zusatz' (Regel-Schluessel): ganze Steige aus standorte.json["pfade"] als volles Bodenband in Kacheln
    <= 400 m (lagen/<ort>__<kurz>_<k>_<Lage>.r8), orte.json "pfade_zusatz". Damit liefert der Planer Kratersteig
    West/Ost und den Gipfelsteig (fuer = [], Serpentine - die Kehren rechnet Ferats Werkzeug) vollstaendig.
  - 'gelaende.senken_erlaubt' (Regel-Schluessel): gewollte geschlossene Senken (Roehrenfenster, Glutschacht,
    Krater) mit Begruendung -> HINWEIS statt WARNUNG, nur wenn die Senke ganz im erlaubten Kreis liegt.
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

BIOM = "lava"


def _log(*t):
    from sehens_lib import ascii_text
    sys.stdout.write("[sehens_%s] %s\n" % (BIOM, " ".join(ascii_text(x) for x in t)))
    sys.stdout.flush()


def abbruch(text, code=2):
    _log("FEHLER:", text)
    sys.exit(code)


# ----------------------------------------------------------------------------------------------------------------------
# Hooks (Formen, die sich nicht als Regel ausdruecken lassen)
# ----------------------------------------------------------------------------------------------------------------------
def _vereinfachen(P, tol):
    from sehens_lib import rezept
    return rezept._vereinfachen(P, tol)


def _pfad_dict(ctx, P, regel, art, quelle):
    from sehens_lib import gelaende as gl
    P = _vereinfachen(P, float(regel.get("vereinfachen_m", 1.5)))
    prof = gl.pfad_profil(ctx.welt, P)
    if art in (None, "auto"):
        art = "serpentine" if prof["max_steigung_prozent"] > 15.0 else "trampelpfad"
    br = max(120, min(200, int(regel.get("breite_cm", 150))))
    return {"punkte_m": P, "punkte_cm": [[round(p[0] * 100), round(p[1] * 100)] for p in P], "breite_cm": br,
            "art": art, "quelle": quelle, "laenge_m": prof["laenge_m"], "max_steigung_grad": prof["max_steigung_grad"]}


def _band(lg, pf, lagen):
    """Bodenband wie rezept.lagen_bauen (Hauptlage volle Breite, Nebenlage 70 %)."""
    br = pf["breite_cm"] / 100.0
    for name, wert in (lagen or {"Erde": 220, "Kies": 110}).items():
        lg.band(name, pf["punkte_m"], br * (1.0 if wert >= 180 else 0.7), float(wert), rand_m=0.8, flecken=0.15,
                flecken_m=3.0)


def _stufen(ctx, pf, ts, praefix):
    """Trittsteine (Pfad quert Wasser) und Felsstufen (Steigung ENTLANG >= stufen_ab_grad) wie rezept.pfad_bauen."""
    import numpy as np
    from sehens_lib import gelaende as gl
    P = pf["punkte_m"]
    x, y, s = gl.polylinie_proben(P, float(ts.get("abstand_m", 0.9)))
    nass = ctx.im_wasser(x, y, 0.5)
    steil = np.zeros(len(x), bool)
    if ts.get("stufen_ab_grad") and len(x) > 2:
        zz = np.asarray(ctx.boden(x, y), np.float64)
        h = np.degrees(np.arctan(np.abs(np.gradient(zz, s)) if np.all(np.diff(s) > 0) else np.zeros(len(x))))
        steil = h >= float(ts["stufen_ab_grad"])
        k = np.round(s / float(ts.get("stufen_abstand_m", 2.5)))
        _, erste = np.unique(np.where(steil, k, -1), return_index=True)
        maske = np.zeros(len(x), bool)
        maske[erste] = True
        steil &= maske
    steil &= ~nass
    for name, sel, pal, gr in ((praefix + "_trittsteine", nass, ts.get("palette"), ts.get("groesse_m", [0.7, 1.1])),
                               (praefix + "_stufen", steil, ts.get("stufen_palette", ts.get("palette")),
                                ts.get("stufen_groesse_m", ts.get("groesse_m", [0.9, 1.4])))):
        if not sel.any() or not pal:
            continue
        ctx.gruppe({"name": name, "ebene": "pfad", "rolle": "stein", "palette": pal, "groesse_m": gr,
                    "warum": "Pfad: Trittstein im Wasser / Felsstufe im steilen Stueck",
                    "verteilung": {"typ": "punkte", "punkte": [{"pos_m": [float(a), float(b)]}
                                                               for a, b in zip(x[sel], y[sel])]},
                    "eingraben": ts.get("eingraben", [0.45, 0.6]), "im_wasser": "egal", "weg_abstand_m": 0,
                    "meide": None, "kollision": True, "akteur": False, "ausrichtung": "normale"})
    pf["trittsteine"] = len(ctx.gruppen.get(praefix + "_trittsteine", []))
    pf["stufen"] = len(ctx.gruppen.get(praefix + "_stufen", []))


def _zugang(ctx):
    """Ort am Steig: Fussweg pfad_cm (Steig -> Ort) zusaetzlich als Bodenband + Felsstufen."""
    zr = ctx.r.get("zugang")
    if not zr or not ctx.st.get("pfad_cm") or not ctx.pfad or not str(ctx.pfad.get("quelle", "")).startswith("pfade:"):
        return
    if zr.get("punkte"):
        P = [list(ctx.punkt(r)) for r in zr["punkte"]]
        quelle = "Planer (%s)" % zr.get("warum", "eigener Zugang")
    else:
        P = [[q[0] / 100.0, q[1] / 100.0] for q in ctx.st["pfad_cm"]][::-1]
        quelle = "pfad_cm (Fussweg vom %s zum Ort)" % ctx.pfad["quelle"][6:]
        if zr.get("ende"):                         # nicht bis in die Hohlform, sondern zum Blickpunkt
            ab = float(zr["ende"].get("ab_m", 20.0))
            k = next((i for i, (x, y) in enumerate(P) if math.hypot(x - ctx.mx, y - ctx.my) <= ab), len(P))
            P = P[:k] + [list(ctx.punkt(r)) for r in zr["ende"]["punkte"]]
            quelle += ", Ende zum Blickpunkt"
    pf = _pfad_dict(ctx, P, zr, zr.get("art", "auto"), quelle)
    if ctx.lagen is not None:
        _band(ctx.lagen, pf, zr.get("lagen"))
    if zr.get("trittsteine"):
        _stufen(ctx, pf, zr["trittsteine"], "zugang")
    ctx.zugang = pf


def _pfade_zusatz(ctx):
    """Ganze Steige aus standorte.json["pfade"] als Bodenband in Kacheln <= 400 m (Lagen-Fenster §9)."""
    import numpy as np
    from sehens_lib import stempel as stm
    out = []
    for pz in ctx.r.get("pfade_zusatz") or []:
        pid = pz["pfad_id"]
        p = next((q for q in ctx.pfade_biom if q.get("id") == pid), None)
        if p is None:
            ctx.melde("FEHLER", "pfade_zusatz: Pfad %s nicht in standorte.json" % pid)
            continue
        P = [[q[0] / 100.0, q[1] / 100.0] for q in p["punkte_cm"]]
        regel = dict(pz)
        regel.setdefault("breite_cm", p.get("breite_cm", 150))
        regel.setdefault("vereinfachen_m", 1.0)
        pf = _pfad_dict(ctx, P, regel, pz.get("art", p.get("art", "trampelpfad")), "pfade:%s (ganzer Pfad)" % pid)
        pf["id"] = pid
        pf["fuer"] = list(p.get("fuer") or [])
        if pz.get("hinweis"):
            pf["hinweis"] = pz["hinweis"]
        kachel = min(400.0, float(pz.get("kachel_m", 400.0))) - 4.0
        A = np.asarray(pf["punkte_m"])
        x0, y0 = A.min(axis=0) - 6.0
        x1, y1 = A.max(axis=0) + 6.0
        nx, ny = max(1, int(math.ceil((x1 - x0) / kachel))), max(1, int(math.ceil((y1 - y0) / kachel)))
        kacheln = []
        for a in range(ny):
            for b in range(nx):
                bx0, bx1 = x0 + (x1 - x0) * b / nx, x0 + (x1 - x0) * (b + 1) / nx
                by0, by1 = y0 + (y1 - y0) * a / ny, y0 + (y1 - y0) * (a + 1) / ny
                lg = stm.Lagen(ctx.welt, bx0, by0, bx1, by1, seed=ctx.seed)
                _band(lg, pf, pz.get("lagen"))
                if lg.namen():
                    kacheln.append(lg)
        pf["_kacheln"] = kacheln
        pf["kurz"] = pz.get("kurz", pid.replace(BIOM + "_pfad_", ""))
        out.append(pf)
        ctx.melde("HINWEIS", "pfade_zusatz %s: %.0f m, %s, Bodenband in %d Kachel(n)" % (pid, pf["laenge_m"], pf["art"],
                                                                                    len(kacheln)))
    ctx.pfade_zusatz = out


def _komponenten(m):
    """8-Nachbar-Komponenten einer bool-Maske (ohne SciPy) -> (label-Array, Anzahl)."""
    import numpy as np
    lab = np.zeros(m.shape, np.int32)
    n = 0
    for i, j in zip(*np.nonzero(m)):
        if lab[i, j]:
            continue
        n += 1
        lab[i, j] = n
        stapel = [(i, j)]
        while stapel:
            a, b = stapel.pop()
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    x, y = a + da, b + db
                    if 0 <= x < m.shape[0] and 0 <= y < m.shape[1] and m[x, y] and not lab[x, y]:
                        lab[x, y] = n
                        stapel.append((x, y))
    return lab, n


def _senken_begruendet(ctx):
    """Geschlossene Senken nach dem Stempel einzeln bewerten:
    - Bestandsmulden (|Delta| < 0,3 m in der ganzen Mulde; nur am Stempelrand mitgezaehlt) -> HINWEIS
    - gewollte Hohlformen im Kreis gelaende.senken_erlaubt [{bei, r_m, grund}] -> HINWEIS mit Grund
    Bleibt danach >= 8 m2 uebrig, bleibt die WARNUNG und ein HINWEIS nennt die Lage der Restsenke."""
    import numpy as np
    erl = (ctx.r.get("gelaende") or {}).get("senken_erlaubt") or []
    if ctx.stempel is None:
        return
    idx = [k for k, m in enumerate(ctx.meldungen) if m[0] == "WARNUNG" and "geschlossene Senke" in m[2]]
    if not idx:
        return
    st = ctx.stempel
    sk = st.senken(wasser=ctx._wasser_maske_fenster(st.fe))
    X, Y = st.X, st.Y
    ok = np.zeros(X.shape, bool)
    for e in erl:
        x, y = ctx.punkt(e.get("bei", "mitte"))
        ok |= np.hypot(X - x, Y - y) <= float(e.get("r_m", 10.0))
    lab, n = _komponenten(sk["maske"])
    rest = np.zeros(X.shape, bool)
    bestand, gewollt = 0.0, 0.0
    a2 = st.z * st.z
    for k in range(1, n + 1):
        m = lab == k
        if float(np.abs(st.delta[m]).max()) < 0.3:
            bestand += m.sum() * a2
        elif (m & ~ok).sum() * a2 < 8.0:
            gewollt += m.sum() * a2
        else:
            rest |= m & ~ok
    if rest.sum() * a2 >= 8.0:
        ii, jj = np.nonzero(rest)
        ctx.melde("HINWEIS", "Restsenke %.0f m2 bei [%.0f, %.0f] (Box %.0f..%.0f / %.0f..%.0f m relativ)" % (
            rest.sum() * a2, X[ii, jj].mean() - ctx.mx, Y[ii, jj].mean() - ctx.my, X[ii, jj].min() - ctx.mx,
            X[ii, jj].max() - ctx.mx, Y[ii, jj].min() - ctx.my, Y[ii, jj].max() - ctx.my))
        return
    gruende = "; ".join(e.get("grund", "") for e in erl)
    text = "geschlossene Senken begruendet: %.0f m2 gewollte Hohlform%s, %.0f m2 Bestandsmulden (|Delta| < 0,3 m, nur " \
           "am Stempelrand beruehrt)" % (gewollt, (" (" + gruende + ")") if gewollt and gruende else "", bestand)
    for k in idx:
        ctx.meldungen[k] = ("HINWEIS", ctx.id, text)


def hook_ende(ctx):
    _senken_begruendet(ctx)
    _zugang(ctx)
    _pfade_zusatz(ctx)
    for m in ctx.r.get("materialien_mit") or []:      # Materialwunsch, den nur ein Decal/Effekt nutzt
        ctx.mat_benutzt.add(m)


HOOKS_ALLE = {"anker": hook_anker, "nach_gelaende": hook_nach_gelaende, "gruppen": hook_gruppen, "ende": hook_ende}
HOOKS = {}


def nachtrag(d, kontexte, aus):
    """orte.json-Erweiterungen aus den Hooks: pfad_zugang, pfade_zusatz (+ Kachel-Dateien unter lagen/)."""
    from sehens_lib import format as sfmt
    geaendert = False
    je = {o["id"]: o for o in d["orte"]}
    for ctx in kontexte:
        e = je.get(ctx.id)
        if e is None:
            continue
        if getattr(ctx, "pfad_angepasst", None) and e.get("pfad"):
            e["pfad"]["quelle"] = ctx.pfad_angepasst
            geaendert = True
        zg = getattr(ctx, "zugang", None)
        if zg:
            e["pfad_zugang"] = {k: zg[k] for k in ("punkte_cm", "breite_cm", "art", "quelle", "laenge_m",
                                                   "max_steigung_grad", "trittsteine", "stufen") if k in zg}
            geaendert = True
        pzl = getattr(ctx, "pfade_zusatz", None) or []
        if pzl:
            liste = []
            for pf in pzl:
                ein = {k: pf[k] for k in ("id", "punkte_cm", "breite_cm", "art", "quelle", "laenge_m",
                                          "max_steigung_grad", "fuer", "hinweis") if k in pf}
                ein["bodenband"] = [b for b in (lg.schreibe(aus, "%s__%s_%d" % (ctx.id, pf["kurz"], k))
                                                for k, lg in enumerate(pf["_kacheln"])) if b]
                liste.append(ein)
            e["pfade_zusatz"] = liste
            geaendert = True
    if geaendert:
        sfmt.schreibe_orte(os.path.join(aus, "orte.json"), d["biom"], d["orte"], stand=d.get("stand"), pruefen=False)
    return geaendert


def pruefe_nachtrag(d, aus):
    """Eigene Pruefung der Erweiterungen (der Pruefer kennt pfade_zusatz nicht): Schema, Kachel <= 400 m, Dateigroesse."""
    from sehens_lib import daten
    bef = []
    for o in d["orte"]:
        for pk in ("pfad_zugang",):
            pf = o.get(pk)
            if pf and (len(pf.get("punkte_cm") or []) < 2 or not 120 <= pf.get("breite_cm", 0) <= 200
                       or pf.get("art") not in daten.PFAD_ARTEN):
                bef.append(("FEHLER", o["id"], "%s: Schema (punkte_cm, breite_cm 120-200, art)" % pk))
        for pz in o.get("pfade_zusatz") or []:
            if len(pz.get("punkte_cm") or []) < 2 or not 120 <= pz.get("breite_cm", 0) <= 200 \
                    or pz.get("art") not in daten.PFAD_ARTEN:
                bef.append(("FEHLER", o["id"], "pfade_zusatz %s: Schema" % pz.get("id")))
            for b in pz.get("bodenband") or []:
                i0, j0, hh, ww = b["fenster_ij"]
                if max(hh, ww) > 400:
                    bef.append(("FEHLER", o["id"], "pfade_zusatz %s: Kachel %dx%d > 400 m" % (pz["id"], hh, ww)))
                for n in b["lagen"]:
                    if n not in daten.BODEN:
                        bef.append(("FEHLER", o["id"], "pfade_zusatz: Lage %s unbekannt" % n))
                    pf = os.path.join(aus, b["datei_praefix"] + n + ".r8")
                    if not os.path.exists(pf) or os.path.getsize(pf) != hh * ww:
                        bef.append(("FEHLER", o["id"], "pfade_zusatz: Datei %s fehlt/Groesse" % pf))
    for s, oid, t in bef:
        _log("  %-7s %-28s %s" % (s, oid[:28], t))
    _log("Pruefung Erweiterungen (pfad_zugang, pfade_zusatz): %d FEHLER" % len(bef))
    return len(bef)


# ----------------------------------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Sehenswuerdigkeiten-Planer Lava (Auftrag 13, Phase 2)")
    ap.add_argument("--orte", "--ort", nargs="+", default=None, dest="orte", help="nur diese Ort-IDs (Standard: alle 8)")
    ap.add_argument("--bild", action="store_true", help="Testbild test_<id>.png je geplantem Ort")
    ap.add_argument("--bild-ordner", default=None, help="Ordner fuer test_<id>.png (Standard: --aus)")
    ap.add_argument("--aus", default=None, help="Ausgabeordner (Standard <basis>/export/unreal/welt/sehens/lava)")
    ap.add_argument("--sw-aus", default=None, help="Ebene sw_lava (Standard: <aus>/sw_lava bzw. <basis>/export/unreal/welt/sw_lava)")
    ap.add_argument("--basis", default=".", help="production-Wurzel (1-m-Daten in export/unreal/welt)")
    ap.add_argument("--regeln", default=os.path.join(HIER, "sehens_lava_regeln.json"))
    ap.add_argument("--inventar", default=None, help="Ordner mit netze.csv, inventar_extra.json (Standard vorlagen/daten)")
    ap.add_argument("--sehens", default=None, help="Ordner antworten/sehens (standorte.json aller Biome)")
    ap.add_argument("--ohne-pruefung", action="store_true")
    ap.add_argument("--daten2m", default=None, help="2-m-PNGs (Cloud-Test): recherche/vorlagen/daten/sehens")
    ap.add_argument("--daten1m", default=None, help="1-m-Originale (Standard <basis>/export/unreal/welt)")
    ap.add_argument("--cache", default=None)
    ap.add_argument("--gruppen", action="store_true", help="je Ort die Stueckzahl je Gruppe ausgeben (Rezept-Abgleich)")
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

    ebene = instanzen.Ebene(BIOM, inv, stand=sfmt.heute())
    kontexte = []
    for oid in planen:
        t0 = time.perf_counter()
        regel = copy.deepcopy(R["orte"][oid])
        ctx = rezept.OrtKontext(welt, gel, inv, ebene, alle[oid], regel, BIOM, seed=R.get("seed", 0),
                                pfade_biom=pfade_biom, paletten=R.get("paletten"), materialien=R.get("materialwuensche"))
        hooks = dict(HOOKS_ALLE)
        hooks.update(HOOKS.get(oid, {}))
        ctx.baue(hooks)
        kontexte.append(ctx)
        if a.gruppen:
            for g in ctx.r.get("gruppen") or []:
                n = len(ctx.gruppen.get(g["name"], []))
                soll = g.get("anzahl", "-")
                _log("    %-22s %-9s %5d  (anzahl %s)" % (g["name"], g.get("ebene", ""), n, soll))
            for k in sorted(ctx.gruppen):
                if k.startswith(("pfad_", "zugang_")):
                    _log("    %-22s %-9s %5d" % (k, "pfad", len(ctx.gruppen[k])))
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
    nachtrag(d, kontexte, aus)

    # --- Bilder
    if a.bild:
        bo = a.bild_ordner or aus
        for ctx in kontexte:
            if ctx.id in gewaehlt:
                p = vorschau.vorschau(ctx, os.path.join(bo, "test_%s.png" % ctx.id))
                _log("Bild:", p)

    # --- Meldungen der Orte
    meld = [m for c in kontexte for m in c.meldungen]
    for st in ("FEHLER", "WARNUNG"):
        for s, oid, t in meld:
            if s == st:
                _log("  %-7s %-28s %s" % (s, oid[:28], t))
    _log("Planer: %d FEHLER, %d WARNUNG, %d HINWEIS" % tuple(sum(1 for m in meld if m[0] == s)
                                                         for s in ("FEHLER", "WARNUNG", "HINWEIS")))
    rc = 1 if any(m[0] == "FEHLER" for m in meld) else 0

    # --- Pruefer (SEHENS_FORMAT) + eigene Erweiterungen
    if not a.ohne_pruefung:
        bef = sehens_pruefen.pruefe_orte(d, basis=aus, inv=inv, welt=welt, sw_ordner=sw)
        z = sehens_pruefen.melde(bef, "orte.json + sw_%s" % BIOM)
        if z["FEHLER"]:
            rc = 1
        if pruefe_nachtrag(d, aus):
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
