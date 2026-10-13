# -*- coding: utf-8 -*-
"""bachbett_roh.py - Bachbett fuer Laeufe ohne Stufenplan (Auftrag 16c, Nachtrag 3; Koordinator Punkt 4).

Ferat: "Felsen, totes Holz und Schlamm gehoeren in jedes Bachbett." Der Gefaelle-Planer (gefaelle_plan.py) stattet nur
die Stufenstrecken aus. Dieses Skript gibt den uebrigen Welt-Laeufen dieselbe Bachbett-Ausstattung
(sehens_lib/bachbett.py, Zahlen in sehens_lib/bachbett_regeln.json):

  - Roh-Laeufe: Welt-Laeufe (wasser_welt.json 'fluesse', baeche_alle.json) ohne Gefaelle-Plan mit Stufen;
  - Reststrecken: die Teile geplanter Laeufe ausserhalb ihrer Stufenstrecken (Abstand roh.abstand_planstrecke_m),
    abschaltbar mit --ohne-reststrecken.

Je Lauf: Felsen (Ufersteine, Stoersteine im Wasser, Kies/Steinpackungen; nicht in Feldern mit lokaler Ufer-Ebene),
Totholz nach Waldnaehe mit Hangeintrag (nicht in Feldern mit lokaler Ufer-Ebene, 16c Nachtrag 4) (Staemme, Verklausungen an Engstellen, ueberspannende Staemme, Wurzelstoecke, Aeste, Zweige),
Schlamm in ruhigen, tiefen Strecken (Ruhe aus dem Spiegelgefaelle), Kies im Bett an Schnellen und der nasse
Uferstreifen. Stufen werden NICHT erfunden, das Gelaende bleibt unveraendert - nur Instanzen und Lagen.

Ausgabe je Lauf wie die Gefaelle-Plaene (<aus>/<lauf>/):
  plan.json            art 'bachbett_roh' | 'bachbett_rest', spiegel_neu_cm (Lauflinie = Spiegel), abschnitte
                       (Lagen-Fenster, Budget), bachbett.abschnitte[<id>] (stuecke, felsen, dichte, lagen), bereiche
                       (behalten / ausgespart mit Grund); keine Stufen, kein Gelaende
  instanzen/<Feld>/    Instanz-Ebene 'bachbett_roh' (FORMAT.md 3, FT-Praefix FT_EL_BBR_), nie Akteure
  lagen/<id>_<Lage>.r8 Zielgewichte 1 m (SEHENS_FORMAT 3: neu = max(alt, ziel), uebrige Lagen skaliert)

Aufruf:
  python -I recherche/antworten/skripte/gefaelle/bachbett_roh.py --gefaelle <gefaelle-Ausgabe> [--laeufe ID ...]
         [--daten2m DIR | --daten1m DIR] [--aus DIR] [--ufer-felder FELD ...] [--ohne-reststrecken] [--ohne-pruefung]
  Lokal (1 m): --basis <production> -> liest export/unreal/welt/, --gefaelle export/unreal/welt/gefaelle, schreibt nach
  export/unreal/welt/bachbett_roh/. Felder mit gesetzter Ufer-Ebene (export/unreal/welt/ufer/foliage_<Feld>/) bekommen
  keine Felsen und (16c Nachtrag 4) kein Totholz: die Ufer-Ebene hat dort schon Kiesel, Kopfsteine, Bloecke und Treibholz.
  Schlamm, Kies im Bett und Uferstreifen bleiben (Regel roh.ufer_ebene_ohne).
  Pruefer: gefaelle/bachbett_roh_pruefen.py (auch eingebaut, ausser --ohne-pruefung).
"""

import argparse
import json
import math
import os
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(HIER))

import numpy as np  # noqa: E402

import gefaelle_daten as gd  # noqa: E402
import gefaelle_regelwerk as gr  # noqa: E402

EBENE = "bachbett_roh"
FT_PRAEFIX = "FT_EL_BBR_"
SEED = 1663


def _log(*t):
    from sehens_lib import ascii_text
    print("[bachbett_roh]", ascii_text(" ".join(str(x) for x in t)), flush=True)


def _r(v, n=2):
    return round(float(v), n)


def plan_mit_stufen(gef, lauf):
    pf = os.path.join(gef, lauf, "plan.json") if gef else None
    if not pf or not os.path.exists(pf):
        return None
    p = gd.lese_json(pf)
    return p if p.get("stufen") and "wasser_koerper" in p else None


def lauf_linie(lauf, schritt_m=2.0):
    """Lauflinie als Spiegel: Punkte der Welt-Daten plus Zwischenpunkte alle schritt_m, Spiegel nie steigend,
    auf 1 mm gerundet (wie plan.json spiegel_neu_cm; Planer und Pruefer rechnen auf denselben Zahlen)."""
    s = np.unique(np.round(np.concatenate([lauf.s, np.arange(0.0, lauf.laenge_m, schritt_m), [lauf.laenge_m]]), 2))
    s = s[np.concatenate([[True], np.diff(s) >= 0.05])]          # keine doppelten/zu nahen s (Kruemmung, Gradient)
    d = lauf.bei_s(s)
    z = np.minimum.accumulate(d["z"])
    x = np.round(d["x"] * 100.0, 1) / 100.0
    y = np.round(d["y"] * 100.0, 1) / 100.0
    z = np.round(z * 100.0, 1) / 100.0
    B = np.round(np.maximum(d["breite"], 0.5) * 100.0, 1) / 100.0
    return np.round(s, 2), x, y, z, B


def bereiche_abziehen(a, b, aus):
    """[a, b] ohne die Intervalle aus [(a_, b_, grund)] -> Liste [(a, b)]."""
    rest = [(a, b)]
    for a_, b_, _ in sorted(aus):
        neu = []
        for x0, x1 in rest:
            if b_ <= x0 or a_ >= x1:
                neu.append((x0, x1))
                continue
            if a_ > x0:
                neu.append((x0, a_))
            if b_ < x1:
                neu.append((b_, x1))
        rest = neu
    return rest


def masken_intervalle(s, m, grund, min_m=0.0):
    """Zusammenhaengende True-Bereiche einer Maske ueber s -> [(a, b, grund)]."""
    out = []
    k = 0
    n = len(s)
    while k < n:
        if not m[k]:
            k += 1
            continue
        k1 = k
        while k1 + 1 < n and m[k1 + 1]:
            k1 += 1
        a, b = float(s[max(k - 1, 0)]), float(s[min(k1 + 1, n - 1)])
        if b - a >= min_m:
            out.append((a, b, grund))
        k = k1 + 1
    return out


def ausgespart(lauf_id, lauf, S, X, Y, B, K, plan):
    """Bereiche (a, b, grund), in denen dieser Lauf kein Bachbett bekommt."""
    from sehens_lib import bachbett as bb
    A = bb.regeln().a["roh"]
    L = float(S[-1])
    aus = [(0.0, float(A["rand_lauf_m"]), "Laufanfang"), (L - float(A["rand_lauf_m"]), L, "Laufende")]
    # Stufenstrecken des eigenen Plans (Reststrecken-Modus)
    if plan is not None:
        r_ = float(A["abstand_planstrecke_m"])
        for x_ in plan.get("strecken") or []:
            for a_, b_ in x_.get("segmente_m") or []:
                aus.append((a_ - r_, b_ + r_, "Stufenstrecke %s (gefaelle_plan.py) + %.0f m" % (x_["id"], r_)))
        for e in (plan.get("feldgrenzen") or {}).get("ueberlappungen") or []:
            if e.get("fremd_s_m") and e.get("nachbar_plan"):
                aus.append((e["fremd_s_m"][0], e["fremd_s_m"][1], "Feldgrenze: gehoert zum Plan %s" % e["nachbar"]))
    # Ueberlappungen an Feldgrenzen (wie der fluss_sim-Export kuerzt: das Teil ohne Plan, sonst das untere)
    for e in gd.feldgrenzen(lauf_id, K["laeufe"]):
        nachbar_plan = e["nachbar"] in K["geplant"]
        ue = e["ueberlappung_s_m"]
        if plan is None and (e["seite"] == "anfang" or nachbar_plan):
            aus.append((ue[0] - 0.5, ue[1] + 0.5, "Ueberlappung mit %s (Export kuerzt diesen Lauf)" % e["nachbar"]))
    # fremdes Wasser: andere Laeufe (Muendung, Zusammenfluss), Seen und Teiche
    ss = np.arange(0.0, L + 1e-6, 1.0)
    px, py = np.interp(ss, S, X), np.interp(ss, S, Y)
    m_w = np.zeros(len(ss), bool)
    m_s = np.zeros(len(ss), bool)
    bx = (px.min() - 60.0, px.max() + 60.0, py.min() - 60.0, py.max() + 60.0)
    partner = {e["nachbar"] for e in gd.feldgrenzen(lauf_id, K["laeufe"])}
    for oid, o in K["laeufe"].items():
        if oid == lauf_id or oid in partner:
            continue
        if o.xy[:, 0].max() < bx[0] or o.xy[:, 0].min() > bx[1] or o.xy[:, 1].max() < bx[2] or o.xy[:, 1].min() > bx[3]:
            continue
        d, sp_, _ = bb.projektion_schnell(px, py, o.xy, 2048)
        hb = np.interp(sp_, o.s, o.breite) / 2.0
        m_w |= d <= hb + float(A["fremd_wasser_rand_m"])
    # 16h: ersetzte Welt-Laeufe (C2 -> Erlenbach p2) liegen ungefaehr dort, wo lokal der Ersatz fliesst (Muendung in den
    # C3-Lauf): wie fremdes Wasser aussparen, damit dort keine Felsen/kein Totholz im Ersatz-Bett oder seiner Muendung liegt
    m_e = np.zeros(len(ss), bool)
    for oid, o in (K.get("ersetzt") or {}).items():
        if o.xy[:, 0].max() < bx[0] or o.xy[:, 0].min() > bx[1] or o.xy[:, 1].max() < bx[2] or o.xy[:, 1].min() > bx[3]:
            continue
        d, sp_, _ = bb.projektion_schnell(px, py, o.xy, 2048)
        hb = np.interp(sp_, o.s, o.breite) / 2.0
        m_e |= d <= hb + float(A["fremd_wasser_rand_m"])
    for see in K["seen"]:
        U = see["umriss_m"]
        if U[:, 0].max() < bx[0] or U[:, 0].min() > bx[1] or U[:, 1].max() < bx[2] or U[:, 1].min() > bx[3]:
            continue
        m_s |= see_maske(px, py, U, float(A["see_puffer_m"]))
    # Orte/Bauwerke (karte_ort) bis halbe Breite + 4 m neben dem Lauf: dort setzt keine Ebene etwas
    welt = K["welt"]
    m_ort = np.zeros(len(ss), bool)
    tx, ty = np.gradient(px), np.gradient(py)
    tn = np.maximum(np.hypot(tx, ty), 1e-9)
    hb = np.interp(ss, S, B) / 2.0 + 4.0
    for f_ in np.linspace(-1.0, 1.0, 9):
        qx, qy = px + ty / tn * hb * f_, py - tx / tn * hb * f_
        ok = welt.im_raster_m(qx, qy)
        i, j = welt.m_zu_ij(np.where(ok, qx, px), np.where(ok, qy, py))
        m_ort |= ok & (welt.ort[i, j] > 0)
    aus += masken_intervalle(ss, m_ort, "Ort/Bauwerk (karte_ort)")
    aus += masken_intervalle(ss, m_w, "fremdes Wasser (Muendung/Zusammenfluss)")
    aus += masken_intervalle(ss, m_s, "See/Teich")
    aus += masken_intervalle(ss, m_e, "Ersatz-Gewaesser (ersetzt.json, 16h: Erlenbach p2 lokal)")
    # Sehenswuerdigkeiten (Radius + abstand_sehens_m): die Sehens-Planer bauen dort selbst
    m_o = np.zeros(len(ss), bool)
    for o in K["orte"]:
        r_ = float(o["radius_m"]) + float(A["abstand_sehens_m"])
        m_o |= np.hypot(px - o["x_m"], py - o["y_m"]) <= r_
    aus += masken_intervalle(ss, m_o, "Sehenswuerdigkeit (Radius + %.0f m)" % float(A["abstand_sehens_m"]))
    return aus


def see_maske(x, y, U, puffer):
    """Punkte im Polygon U (m) oder <= puffer daneben."""
    from sehens_lib import bachbett as bb
    x = np.asarray(x, np.float64)
    y = np.asarray(y, np.float64)
    x1, y1 = U[:, 0], U[:, 1]
    x2, y2 = np.roll(x1, -1), np.roll(y1, -1)
    innen = np.zeros(len(x), bool)
    for k in range(len(U)):
        c = ((y1[k] > y) != (y2[k] > y)) & (x < (x2[k] - x1[k]) * (y - y1[k]) / ((y2[k] - y1[k]) or 1e-12) + x1[k])
        innen ^= c
    d, _, _ = bb.projektion_schnell(x, y, np.vstack([U, U[:1]]), 2048)
    return innen | (d <= puffer)


def segmente_bilden(behalten, welt, kanal, R):
    """Behaltene Bereiche -> Segmente <= segment_max_m mit Biom (Mehrheit aus 7 Proben)."""
    A = R.a["roh"]
    out = []
    for a, b in behalten:
        L = b - a
        if L < float(R.a["min_laenge_m"]):
            continue
        n = max(1, int(math.ceil(L / float(A["segment_max_m"]))))
        for k in range(n):
            a_, b_ = a + L * k / n, a + L * (k + 1) / n
            bi = [welt.biom_bei_m(*[float(v) for v in kanal.xy(t)]) for t in np.linspace(a_, b_, 7)]
            bi = [v for v in bi if v] or ["tundra"]
            out.append((float(a_), float(b_), max(set(bi), key=lambda v: (bi.count(v), v))))
    return out


def abschnitte_bilden(segs, R):
    """Segmente zu Abschnitten (Lagen-/Kontext-Fenster) mit Spannweite <= abschnitt_max_m gruppieren."""
    A = R.a["roh"]
    out, cur = [], []
    for sg in segs:
        if cur and (sg[1] - cur[0][0] > float(A["abschnitt_max_m"]) or sg[0] - cur[-1][1] > 30.0):
            out.append(cur)
            cur = []
        cur.append(sg)
    if cur:
        out.append(cur)
    return out


def paletten_fn(rw, inv):
    cache = {}

    def f(biom):
        if biom not in cache:
            bn, b = rw.biom(biom)
            n = b.get("netze") or {}
            cache[biom] = {"bloecke": [x for x in n.get("bloecke") or [] if inv.netz_pfad(x) and not inv.saegeschnitt(x)],
                           "kies": [x for x in n.get("kies") or [] if inv.netz_pfad(x) and not inv.saegeschnitt(x)]}
        return cache[biom]
    return f


def roh_lagen_1m(K, ctx, kanal, segs, fl, R):
    """Wie gefaelle_plan.bachbett_lagen_1m (Schlamm, Uferstreifen), dazu Kies im Bett an Schnellen (Ruhe < 0,6).
    Boden = altes Gelaende (keine Aenderung)."""
    import gefaelle_plan as gp
    from sehens_lib import bachbett as bb, stempel as stm
    zus, w_str, w_sch, kz = gp.bachbett_lagen_1m(K, ctx, kanal, segs, fl, ctx.stempel)
    i0, j0, ni, nj = [int(v) for v in fl]
    F = gp.alt_1m(K, fl)
    jj, ii = np.meshgrid(np.arange(j0, j0 + nj, dtype=np.float64), np.arange(i0, i0 + ni, dtype=np.float64))
    X, Y = jj - gd.OFF_J_1M, ii - gd.OFF_I_1M
    rand = float(np.max(kanal.B)) / 2.0 + 8.0
    box = (X >= kanal.x.min() - rand) & (X <= kanal.x.max() + rand) & (Y >= kanal.y.min() - rand) & \
        (Y <= kanal.y.max() + rand)
    kz["kies_m2"] = 0
    if not box.any():
        return zus, w_str, w_sch, kz
    BK = R.a["roh"]["bett_kies"]
    d, s, u = kanal.projektion(X[box], Y[box])
    halb = kanal.halb(s, u)
    z_sp = kanal.z(s, u)
    ru = kanal.ruhe(s)
    w_k = np.zeros(int(box.sum()))
    lage_k = {}
    for a, b, biom in segs:
        m = (s >= a) & (s <= b) & (d <= halb - 0.2) & (F[box] < z_sp)
        if not m.any():
            continue
        wk = np.where(m, np.clip((0.6 - ru) / 0.4, 0.0, 1.0), 0.0)
        wk = wk * (0.75 + 0.35 * stm.rauschen(X[box], Y[box], 3.0, SEED + 515))
        lage = BK.get(bb.regeln().biom(biom)[0], BK["standard"])
        lage_k.setdefault(lage, np.zeros(int(box.sum())))
        lage_k[lage] = np.maximum(lage_k[lage], np.clip(wk, 0.0, 1.0) * float(BK["wert"]))
        w_k = np.maximum(w_k, np.clip(wk, 0.0, 1.0))
    wsch_b = w_sch[box]
    for n, v in lage_k.items():
        v = v * (1.0 - float(R.a["kies_daempfung"]) * wsch_b)
        full = zus.get(n, np.zeros(X.shape))
        full[box] = np.maximum(full[box], v)
        zus[n] = full
    kz["kies_m2"] = int((w_k >= 0.3).sum())
    return zus, w_str, w_sch, kz


def plane_lauf(lauf_id, K, plan_gef=None):
    """Bachbett eines Laufs (roh) bzw. der Reststrecken eines geplanten Laufs. Rueckgabe plan (oder None)."""
    from sehens_lib import bachbett as bb, instanzen, rezept, stempel as stm
    from sehens_lib import format as sfmt
    import gefaelle_plan as gp
    welt, gel, inv, rw = K["welt"], K["gel"], K["inv"], K["rw"]
    R = bb.regeln()
    meldungen = []
    lauf = K["laeufe"][lauf_id]
    S, X, Y, Z, B = lauf_linie(lauf)
    art = "bachbett_rest" if plan_gef is not None else "bachbett_roh"
    aus = ausgespart(lauf_id, lauf, S, X, Y, B, K, plan_gef)
    behalten = [(a, b) for a, b in bereiche_abziehen(0.0, float(S[-1]), aus) if b - a >= float(R.a["min_laenge_m"])]
    ruhe_fn, gef_S = bb.ruhe_aus_gefaelle(S, Z, R)
    kanal = bb.Kanal(S, X, Y, Z, B, [], R=R, ruhe_fn=ruhe_fn)
    segs = segmente_bilden(behalten, welt, kanal, R)
    aus_lauf = os.path.join(K["aus"], lauf_id)
    plan = {"stand": sfmt.heute(), "auftrag": "16c Nachtrag 3: Bachbett fuer Laeufe ohne Stufenplan (Felsen, Totholz, "
            "Schlamm, Uferstreifen)", "lauf": lauf_id, "art": art, "lauf_art": lauf.art, "quelle_lauf": lauf.quelle,
            "feld": lauf.feld, "ebene": EBENE, "daten": "1m" if welt.zelle_m == 1.0 else "2m (Cloud-Test)",
            "regeln": {"datei": "recherche/antworten/skripte/sehens_lib/bachbett_regeln.json", "version": R.version},
            "laenge_m": _r(S[-1], 1), "stufen": [], "gelaende": None,
            "gelaende_hinweis": "keine Gelaendeaenderung: nur Instanzen und Lagen; keine Stufen (16c Nachtrag 3)",
            "spiegel_neu_cm": [[_r(x * 100, 1), _r(y * 100, 1), _r(z * 100, 1), _r(b * 100, 1)]
                               for x, y, z, b in zip(X, Y, Z, B)],
            "spiegel_neu_s_m": [float(v) for v in S],
            "spiegel_hinweis": "Lauflinie aus %s, Spiegel = Punkt-z nie steigend (fuer Totholz-Hoehen, Schlamm und "
                               "Uferstreifen)" % lauf.quelle,
            "bereiche": {"behalten_s_m": [[_r(a), _r(b)] for a, b in behalten],
                         "ausgespart": [[_r(a), _r(b), g] for a, b, g in sorted(aus)]},
            "strecken": [{"id": "%s_roh" % lauf_id, "segmente_m": [[_r(a), _r(b)] for a, b, _ in segs]}]}
    if plan_gef is not None:
        plan["plan_gefaelle"] = "gefaelle/%s/plan.json" % lauf_id
    if os.path.isdir(aus_lauf):
        import shutil
        shutil.rmtree(aus_lauf)
    if not segs:
        plan.update({"abschnitte": [], "bachbett": {"regeln": plan["regeln"]["datei"], "version": R.version,
                                                     "abschnitte": {}},
                     "instanzen": {"ordner": "instanzen", "ebene": EBENE, "ft_praefix": FT_PRAEFIX, "felder": {},
                                   "anzahl": 0, "kollision": 0, "akteure": 0},
                     "hinweis": "kein Bachbett: ganze Lauflaenge ausgespart oder kuerzer als %.0f m"
                                % float(R.a["min_laenge_m"])})
        os.makedirs(aus_lauf, exist_ok=True)
        with open(os.path.join(aus_lauf, "plan.json"), "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=1)
        return plan, meldungen
    ebene = instanzen.Ebene(EBENE, inv, stand=sfmt.heute(), ebene_name=EBENE, ft_praefix=FT_PRAEFIX)
    pal_fn = paletten_fn(rw, inv)
    ufer_felder = K["ufer_felder"]
    from sehens_lib import daten as _d
    ufer_ohne = set(R.a["roh"].get("ufer_ebene_ohne") or ["felsen"])

    def ohne_fn(x, y):
        return _d.feld_von_m(x, y) in ufer_felder

    felsen_ohne = ohne_fn if "felsen" in ufer_ohne and ufer_felder else None
    totholz_ohne = ohne_fn if "totholz" in ufer_ohne and ufer_felder else None

    rb = float(np.max(B)) / 2.0 + 60.0
    seen_nah = [see for see in K["seen"] if see["box"][0] - rb <= X.max() and see["box"][2] + rb >= X.min() and
                see["box"][1] - rb <= Y.max() and see["box"][3] + rb >= Y.min()]

    def see_fn(x, y):
        x, y = np.atleast_1d(np.asarray(x, np.float64)), np.atleast_1d(np.asarray(y, np.float64))
        m = np.zeros(x.shape, bool)
        for see in seen_nah:
            bx = see["box"]
            k = (x >= bx[0] - 1.0) & (x <= bx[2] + 1.0) & (y >= bx[1] - 1.0) & (y <= bx[3] + 1.0)
            if k.any():
                m[k] |= see_maske(x[k], y[k], see["umriss_m"], 1.0)
        return m

    def oberlauf_fn(a):
        return bb.oberlauf_punkte(S, X, Y, a, float(R.a["treibholz"]["oberlauf_m"]))

    def gef_fn(s_):
        return np.interp(s_, S, gef_S)

    ab_out = []
    bb_ab = {}
    for n_ab, gruppe in enumerate(abschnitte_bilden(segs, R)):
        aid = "%s_r%d" % (lauf_id, n_ab + 1)
        a0, b0 = gruppe[0][0], gruppe[-1][1]
        ss = np.arange(a0, b0 + 1e-6, 1.0)
        px, py = kanal.xy(ss)
        rand = float(np.max(B)) / 2.0 + 12.0
        x0, y0, x1, y1 = px.min() - rand, py.min() - rand, px.max() + rand, py.max() + rand
        st = stm.Stempel(welt, x0, y0, x1, y1, rand_m=8.0, seed=SEED)       # Delta bleibt 0 (kein Gelaende)
        cx, cy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
        standort = {"id": aid, "name": "Bachbett %s" % aid, "art": "fundstueck",
                    "mitte_cm": [round(cx * 100), round(cy * 100), round(float(welt.hoehe_bei_m(cx, cy)) * 100)],
                    "radius_m": 0.5 * math.hypot(x1 - x0, y1 - y0),
                    "felder": sorted({f_ for f_ in (_d.feld_von_m(float(u), float(v)) for u, v in zip(px, py)) if f_}),
                    "kameras": []}
        biom_ab = max(set(bi for _, _, bi in gruppe), key=lambda v: (sum(b_ - a_ for a_, b_, b2 in gruppe if b2 == v), v))
        ctx = rezept.OrtKontext(welt, gel, inv, ebene, standort, {"lagen": []}, biom_ab, seed=SEED)
        ctx.stempel = st
        fb = bb.felsen_setzen(ctx, kanal, gruppe, pal_fn, R, see_fn=see_fn, gefaelle_fn=gef_fn, ohne_fn=felsen_ohne)
        bil = bb.totholz_setzen(ctx, kanal, gruppe, R, welt, None, "bb", see_fn=see_fn, oberlauf_fn=oberlauf_fn,
                                ohne_fn=totholz_ohne)
        # nichts auf Ortsflaechen (Lage nach dem Zentrieren) und nichts in Sehenswuerdigkeiten (Radius + 10 m)
        def auf_ort(s_):
            i_, j_ = welt.m_zu_ij(s_["x"] / 100.0, s_["y"] / 100.0)
            return bool(welt.ort[i_, j_] > 0)
        ebene.stuecke = [s_ for s_ in ebene.stuecke if s_["ort"] != aid or not auf_ort(s_)]
        # 16c Nachtrag 4: kein Totholz in Feldern mit lokaler Ufer-Ebene (Lage nach dem Zentrieren, wie der Pruefer)
        if totholz_ohne is not None:
            ebene.stuecke = [s_ for s_ in ebene.stuecke if s_["ort"] != aid or not
                             str(s_.get("gruppe", "")).startswith(bb.PRAEFIX) or
                             not totholz_ohne(s_["x"] / 100.0, s_["y"] / 100.0)]
        # nichts in ausgesparten Bereichen (Lage nach dem Zentrieren; wie der Pruefer: Projektion, +-1 m, <= 6 m)
        zonen_aus = [(a_, b_) for a_, b_, g_ in aus if "Lauf" not in g_]
        eig = [s_ for s_ in ebene.stuecke if s_["ort"] == aid]
        if eig and zonen_aus:
            d_, sp_, _ = bb.projektion_schnell(np.array([e["x"] / 100.0 for e in eig]),
                                               np.array([e["y"] / 100.0 for e in eig]), np.stack([X, Y], 1), 2048)
            cum_ = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(X * 100.0), np.diff(Y * 100.0)) / 100.0)])
            s_e = np.interp(sp_, cum_, S)
            raus = {id(e) for e, dd, se in zip(eig, d_, s_e) if dd <= 6.0 and any(a_ + 1.0 < se < b_ - 1.0
                                                                                   for a_, b_ in zonen_aus)}
            ebene.stuecke = [s_ for s_ in ebene.stuecke if id(s_) not in raus]
        ebene.stuecke = [s_ for s_ in ebene.stuecke if s_["ort"] != aid or not any(
            math.hypot(s_["x"] / 100.0 - o["x_m"], s_["y"] / 100.0 - o["y_m"]) <= o["radius_m"] + 10.0
            for o in K["orte"])]
        ebene.ausduennen(aid, 15000, 1500, 80)
        lg = stm.Lagen(welt, *st.fe.grenzen_m(), seed=SEED)
        ctx.lagen = lg
        lblk = gp.schreibe_lagen_1m(lg, st, aus_lauf, aid, "Erde",
                                    bb_fn=lambda fl_, ctx=ctx, gruppe=gruppe: roh_lagen_1m(K, ctx, kanal, gruppe, fl_, R))
        kz = (lblk or {}).pop("_bachbett", None)
        blk = gp.bachbett_block(ctx, kanal, bil, inv)
        blk["lagen"] = kz
        fs = bb.stuecke_block(ctx, kanal, inv, gruppen_praefix="bbf_")
        for f_ in fs:
            f_["art"] = "fels_" + f_["gruppe"][4:].rsplit("_", 1)[0]
        blk["felsen"] = fs
        blk["felsen_bilanz"] = fb
        bb_ab[aid] = blk
        for s_, oid, t_ in ctx.meldungen:
            meldungen.append((s_, oid, t_))
        z = ebene.zaehle(aid)
        ab_out.append({"id": aid, "biom": biom_ab, "felder": standort["felder"],
                       "segmente_m": [[_r(a), _r(b)] for a, b, _ in gruppe], "gelaende": None, "lagen": lblk,
                       "budget": {"instanzen": z["instanzen"], "kollision": z["kollision"], "akteure": z["akteure"],
                                  "niagara": 0},
                       "detail_ebenen": {k: v for k, v in z["je_ebene"].items()}})
    os.makedirs(aus_lauf, exist_ok=True)
    info = ebene.schreibe(os.path.join(aus_lauf, "instanzen")) if ebene.stuecke else {}
    plan.update({"abschnitte": ab_out,
                 "bachbett": {"regeln": plan["regeln"]["datei"], "version": R.version,
                              "auftrag": "16c Nachtrag 3 (Roh-Laeufe: Felsen, Totholz, Schlamm, Uferstreifen)",
                              "felsen_ohne_felder": sorted(ufer_felder) if "felsen" in ufer_ohne else [],
                              "totholz_ohne_felder": sorted(ufer_felder) if "totholz" in ufer_ohne else [],
                              "abschnitte": bb_ab},
                 "instanzen": {"ordner": "instanzen", "ebene": EBENE, "ft_praefix": FT_PRAEFIX, "felder": info,
                               "anzahl": sum(v["instanzen"] for v in info.values()),
                               "kollision": sum(v["kollision"] for v in info.values()),
                               "akteure": sum(v["akteure"] for v in info.values())},
                 "akteure": sum(v["akteure"] for v in info.values())})
    plan["meldungen"] = [{"stufe": s_, "text": t_} for s_, _, t_ in meldungen]
    with open(os.path.join(aus_lauf, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1, default=gp._json_np)
    return plan, meldungen


def main(argv=None):
    ap = argparse.ArgumentParser(description="Bachbett fuer Laeufe ohne Stufenplan (16c Nachtrag 3)")
    ap.add_argument("--gefaelle", default=None, help="Ausgabe von gefaelle_plan.py (<lauf>/plan.json); Standard "
                                                     "<basis>/export/unreal/welt/gefaelle")
    ap.add_argument("--laeufe", nargs="+", default=None, help="nur diese Lauf-IDs")
    ap.add_argument("--aus", default=None, help="Ausgabeordner (Standard <basis>/export/unreal/welt/bachbett_roh)")
    ap.add_argument("--basis", default=".", help="production-Wurzel (1-m-Daten in export/unreal/welt)")
    ap.add_argument("--sehens", default=gd.SEHENS_STANDARD, help="Sehens-Standorte (Radius wird ausgespart)")
    ap.add_argument("--baeche", default=None)
    ap.add_argument("--inventar", default=None)
    ap.add_argument("--ufer-felder", nargs="*", default=None,
                    help="Felder mit lokaler Ufer-Ebene (keine Felsen, kein Totholz); Standard: Ordner ufer/foliage_<Feld> "
                         "der 1-m-Daten")
    ap.add_argument("--ohne-reststrecken", action="store_true", help="nur Roh-Laeufe, keine Reststrecken geplanter Laeufe")
    ap.add_argument("--ohne-pruefung", action="store_true")
    from sehens_lib import daten
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    T0 = time.perf_counter()
    from sehens_lib import gelaende, inventar
    rw = gr.Regelwerk.lade()
    inv = inventar.Inventar.lade(a.inventar)
    daten1m = a.daten1m
    if not a.daten2m and not daten1m:
        daten1m = os.path.join(a.basis, "export", "unreal", "welt")
        if not os.path.isdir(daten1m):
            _log("FEHLER: weder --daten2m noch 1-m-Daten (%s)" % daten1m)
            return 2
    welt = daten.lade(a.daten2m, daten1m, pfade=True)
    gel = gelaende.Gelaende(welt, cache=a.cache)
    gef = a.gefaelle or os.path.join(a.basis, "export", "unreal", "welt", "gefaelle")
    if not os.path.isdir(gef):
        _log("FEHLER: Gefaelle-Ausgabe %s fehlt (welche Laeufe einen Stufenplan haben, steht dort)" % gef)
        return 2
    bpfad = a.baeche
    if not bpfad:
        for c in ([os.path.join(daten1m, "baeche", "baeche_alle.json")] if daten1m else []) + \
                [os.path.join(a.daten2m or gd.DATEN2M_STANDARD, "baeche_alle.json")]:
            if os.path.exists(c):
                bpfad = c
                break
    baeche = gd.lese_json(bpfad)["baeche"] if bpfad else welt.baeche
    laeufe = gd.alle_laeufe(welt, baeche, welt.wasser_welt)
    geplant = {}
    for lid in laeufe:
        p = plan_mit_stufen(gef, lid)
        if p is not None:
            geplant[lid] = p
    seen = []
    for s_ in (welt.wasser_welt or {}).get("seen", []) or []:
        if s_.get("umriss") and len(s_["umriss"]) >= 3:
            seen.append({"id": s_["id"], "umriss_m": np.asarray(s_["umriss"], np.float64)[:, :2] / 100.0})
    for t_ in welt.teiche or []:
        U = t_.get("umriss") or t_.get("umriss_cm")
        if U and len(U) >= 3:
            seen.append({"id": t_.get("id"), "umriss_m": np.asarray(U, np.float64)[:, :2] / 100.0})
    for see in seen:
        U = see["umriss_m"]
        see["box"] = (float(U[:, 0].min()), float(U[:, 1].min()), float(U[:, 0].max()), float(U[:, 1].max()))
    if a.ufer_felder is not None:
        ufer = set(a.ufer_felder)
    else:
        ufer = set()
        if daten1m and os.path.isdir(os.path.join(daten1m, "ufer")):
            ufer = {n[len("foliage_"):] for n in os.listdir(os.path.join(daten1m, "ufer")) if n.startswith("foliage_")}
    aus = os.path.abspath(a.aus or os.path.join(a.basis, "export", "unreal", "welt", "bachbett_roh"))
    alle_mit = gd.alle_laeufe(welt, baeche, welt.wasser_welt, mit_ersetzten=True)
    K = {"welt": welt, "gel": gel, "inv": inv, "rw": rw, "laeufe": laeufe, "geplant": geplant, "seen": seen,
         "ersetzt": {k: v for k, v in alle_mit.items() if k not in laeufe},
         "orte": gd.sehens_orte(a.sehens), "aus": aus, "ufer_felder": ufer, "h1m": None}
    _log(welt.info(), "| %d Laeufe, %d mit Stufenplan, Ufer-Ebene (ohne Felsen und Totholz): %s" % (
        len(laeufe), len(geplant), ", ".join(sorted(ufer)) or "-"))
    ziel = sorted(a.laeufe) if a.laeufe else sorted(laeufe)
    alle_meld = []
    zus = {"roh": 0, "rest": 0}
    rc = 0
    ersetzt = gd.ersetzte_laeufe()
    if ersetzt:
        _log("Ersetzt (16h, fluss_sim/ersetzt.json), keine Roh-Ebene: %s" % ", ".join(
            "%s -> %s" % (k, v.get("ersetzt_durch")) for k, v in ersetzt.items()))
        alt = [n for n in ersetzt if os.path.isdir(os.path.join(aus, n))]
        if alt:
            _log("HINWEIS: alte Ausgaben ersetzter Laeufe in %s: %s - werden nicht mehr gelesen (fluss_sim, Pruefer), "
                 "Ordner koennen weg" % (aus, ", ".join(alt)))
    for lid in ziel:
        if lid in ersetzt:
            _log("HINWEIS: Lauf %s ist ersetzt durch %s - keine Roh-Ebene" % (lid, ersetzt[lid].get("ersetzt_durch")))
            continue
        if lid not in laeufe:
            _log("WARNUNG: Lauf %s unbekannt" % lid)
            continue
        pg = geplant.get(lid)
        if pg is not None and a.ohne_reststrecken:
            continue
        t0 = time.perf_counter()
        plan, meld = plane_lauf(lid, K, pg)
        alle_meld += meld
        zus["rest" if pg is not None else "roh"] += 1
        n_bb = sum(len(v["stuecke"]) for v in plan["bachbett"]["abschnitte"].values())
        n_fs = sum(len(v.get("felsen") or []) for v in plan["bachbett"]["abschnitte"].values())
        _log("%-28s %-5s %6.0f m, %5.0f m Bachbett, %4d Totholz, %4d Felsen, %5d Inst  %.1f s" % (
            lid, "rest" if pg is not None else "roh", plan["laenge_m"],
            sum(b - a for a, b in plan["bereiche"]["behalten_s_m"]), n_bb, n_fs, plan["instanzen"]["anzahl"],
            time.perf_counter() - t0))
    for st_ in ("FEHLER", "WARNUNG"):
        for s_, oid, t_ in alle_meld:
            if s_ == st_:
                _log("  %-7s %-24s %s" % (s_, oid[:24], t_))
    n = {s_: sum(1 for m in alle_meld if m[0] == s_) for s_ in ("FEHLER", "WARNUNG", "HINWEIS")}
    _log("Planer: %d FEHLER, %d WARNUNG, %d HINWEIS | %d Roh-Laeufe, %d Reststrecken | %.0f s" % (
        n["FEHLER"], n["WARNUNG"], n["HINWEIS"], zus["roh"], zus["rest"], time.perf_counter() - T0))
    if n["FEHLER"]:
        rc = 1
    if not a.ohne_pruefung:
        import bachbett_roh_pruefen
        rc = max(rc, bachbett_roh_pruefen.pruefe_alle(aus, welt=welt, inv=inv, rw=rw, laeufe=ziel,
                                                       orte=K["orte"]))
    return rc


if __name__ == "__main__":
    sys.exit(main())
