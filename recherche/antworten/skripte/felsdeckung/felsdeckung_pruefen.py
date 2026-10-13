#!/usr/bin/env python3
"""felsdeckung_pruefen.py - Pruefer fuer den Pilotplan Auftrag 21 (FORMAT-§3-Themen, Akteure, Masken, A15-Variante B).

Aufruf (Repo-Wurzel):
  python -I recherche/antworten/skripte/felsdeckung/felsdeckung_pruefen.py --plan recherche/antworten/felsdeckung
  python -I .../felsdeckung_pruefen.py --plan <ordner> --determinismus     # Planer zweimal laufen lassen, Bytevergleich

Prueft unabhaengig vom Planer (nur Regeln, Inventar, Gelaende werden geteilt):
  Format     f32 = 10 float32 je Instanz, Anzahl = plan.json, endlich, Quaternion normiert, Skala 0,3-3,0, Feld B5,
             im Fenster; Kuerzel/ft_praefix nie BACH*; Akteur-Dateien = Liste akteure
  Netze      jedes Netz in netze.csv, nicht gesperrt, nicht unvollstaendig, kein Saegeschnitt (Wildnis)
  Sperren    kein Stueck im Uferband 0-10 m (Auftrag 20), auf Weg (4 m), Ort, Meer
  Schweben   Felsen: Unterseite (lokal) ganz im Boden (Toleranz 0,15 m); Baender/Wand: tiefste 12 % der Box;
             Baeume/Pflanzen: Pivot -1,0 bis +0,3 m am Boden
  Form       keine wuerfeligen/stehenden Bloecke > 1,5 m
  Dichte     Halde: Bloecke > 2 m / > 4 m je 100 m2 je 48-m-Zelle; ausserhalb Halde > 35 Grad: Runde-5-Grenze 0,67
  Deckung    Grundriss-Netzdeckung je Zone gegen pruef_schwellen (Fussabdruck-Ellipse x 0,85, Raster 0,5 m),
             Fussflaechen-Summe (wie Zensus 6h), Fels-Lage >= 38 Grad ohne Netz
  Baeume     baumfreie Felszone >= 35 %, keine Grat-Reihe > 3, jeder Baum mit Block >= 1 m im Radius 3 m
  Budget     Instanzen je Thema, Kollision gesamt, Akteure gesamt
  Masken     Groesse/Fenster der Lagen-, Gras-, Ausduenn-, Zonenmasken; Ausduennen nur 0/255
  A15 (B)    Groesse, nur anheben, |Delta| <= max_aenderung, 0 im Wasserabstand 12 m und am Fensterrand
Ausgabe: Bericht (ASCII) auf stdout und <plan>/pruefbericht_<Feld>.txt; Rueckgabe 1 bei FEHLER.
"""

import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
SKRIPTE = os.path.normpath(os.path.join(HIER, ".."))
for p in (SKRIPTE, HIER):
    if p not in sys.path:
        sys.path.insert(0, p)

from sehens_lib import daten as D          # noqa: E402
from sehens_lib import instanzen as INS    # noqa: E402
from sehens_lib import inventar as INV     # noqa: E402
import felsdeckung_plan as FP              # noqa: E402

FEHLER, WARNUNG, HINWEIS = "FEHLER", "WARNUNG", "HINWEIS"
FELS_LOKAL = {"teppich", "block", "platte", "fussblock", "totholz", "akteur_halde"}
FELS_WELT = {"band", "wandreihe", "gratkrone", "turm"}
PFLANZE = {"baum_jung", "baum_mittel", "baum_hoch", "baum_tot", "latsche", "fuge"}


class Bericht:
    def __init__(self):
        self.z = []

    def __call__(self, stufe, text):
        self.z.append((stufe, text))

    def zahl(self, stufe):
        return sum(1 for s, _ in self.z if s == stufe)


def lies_themen(plan_ordner, feld):
    out = {}
    for thema in FP.THEMEN:
        o = os.path.join(plan_ordner, "%s_%s" % (thema, feld))
        pj = os.path.join(o, "plan.json")
        if not os.path.exists(pj):
            out[thema] = None
            continue
        with open(pj, "r", encoding="utf-8") as f:
            plan = json.load(f)
        arr = {}
        for key in plan.get("dateien", {}):
            pf = os.path.join(o, key + ".f32")
            arr[key] = np.fromfile(pf, dtype="<f4") if os.path.exists(pf) else None
        out[thema] = (plan, arr)
    return out


def ellipse(info, q, s, pos):
    P = INS.gedrehte_box(info, q, s)
    Q = P[:, :2] + np.array([pos[0], pos[1]])
    m = Q.mean(axis=0)
    C = (Q - m).T @ (Q - m)
    w_, V = np.linalg.eigh(C)
    ach = V[:, ::-1]
    pr = (Q - m) @ ach
    a, b = float(np.abs(pr[:, 0]).max()), float(np.abs(pr[:, 1]).max())
    return m[0] / 100.0, m[1] / 100.0, max(a, 5.0) / 100.0, max(b, 5.0) / 100.0, math.atan2(ach[1, 0], ach[0, 0]), P


def pruefe(plan_ordner, regeln, welt, inv, B):
    feld = regeln["pilot"]["feld"]
    PS = regeln["pruef_schwellen"]
    themen = lies_themen(plan_ordner, feld)
    # Variante aus den Plaenen
    var = {t[0].get("variante") for t in themen.values() if t}
    variante = var.pop() if len(var) == 1 else "A"
    delta = None
    if variante == "B":
        delta, _, _ = FP.plane_kegel(welt, regeln)
    K = FP.Kontext(welt, regeln, delta)
    x0, y0, x1, y1 = K.fenster_m
    stuecke = []
    budget_kol = 0
    budget_ak = 0
    for thema, t in themen.items():
        if t is None:
            B(FEHLER, "Thema %s_%s fehlt" % (thema, feld))
            continue
        plan, arr = t
        kz = str(plan.get("kuerzel", ""))
        if kz.upper().startswith("BACH") or str(plan.get("ft_praefix", "")).upper().startswith("FT_EL_BACH") or \
                thema.lower().startswith("bach"):
            B(FEHLER, "%s: Kuerzel/Praefix 'BACH*' verboten (Setzer loescht Bachdekor)" % thema)
        if plan.get("feld") != feld:
            B(FEHLER, "%s: feld %r != %s" % (thema, plan.get("feld"), feld))
        if not str(plan.get("ft_praefix", "")).startswith("FT_EL_"):
            B(FEHLER, "%s: ft_praefix muss mit FT_EL_ beginnen" % thema)
        n_inst = 0
        n_ak_dat = 0
        for key, d in plan["dateien"].items():
            a = arr.get(key)
            if a is None:
                B(FEHLER, "%s/%s.f32 fehlt" % (thema, key))
                continue
            if a.size % 10:
                B(FEHLER, "%s/%s.f32: Groesse kein Vielfaches von 10 float32" % (thema, key))
                continue
            a = a.reshape(-1, 10)
            if a.shape[0] != d["anzahl"]:
                B(FEHLER, "%s/%s: %d Instanzen, plan.json sagt %d" % (thema, key, a.shape[0], d["anzahl"]))
            if not np.isfinite(a).all():
                B(FEHLER, "%s/%s: NaN/Inf" % (thema, key))
                continue
            qn = np.linalg.norm(a[:, 3:7], axis=1)
            if (np.abs(qn - 1.0) > 1e-3).any():
                B(FEHLER, "%s/%s: Quaternion nicht normiert" % (thema, key))
            if ((a[:, 7:10] < 0.3) | (a[:, 7:10] > 3.0)).any():
                B(FEHLER, "%s/%s: Skala ausserhalb 0,3-3,0" % (thema, key))
            for b in inv.netz_pruefen(d["pfad"], wildnis=True):
                if b[0] == FEHLER:
                    B(FEHLER, "%s/%s: %s" % (thema, key, b[1]))
            ist_ak = key.startswith("akteur_")
            if ist_ak != bool(d.get("akteur")) or (ist_ak and d.get("rolle") != "akteur"):
                B(FEHLER, "%s/%s: Akteur-Kennung inkonsistent" % (thema, key))
            if ist_ak:
                n_ak_dat += a.shape[0]
            else:
                n_inst += a.shape[0]
                if d.get("kollision"):
                    budget_kol += a.shape[0]
            info = inv.netz(d["pfad"])
            rollen = d["rolle"].split("/")
            for r_ in range(a.shape[0]):
                stuecke.append({"thema": thema, "key": key, "info": info, "pos": a[r_, 0:3].astype(np.float64),
                                "q": tuple(float(v) for v in a[r_, 3:7]), "s": tuple(float(v) for v in a[r_, 7:10]),
                                "rollen": rollen, "akteur": ist_ak, "kol": bool(d.get("kollision"))})
        if n_inst != plan.get("instanzen"):
            B(FEHLER, "%s: instanzen %s != Summe %d" % (thema, plan.get("instanzen"), n_inst))
        if n_ak_dat != len(plan.get("akteure", [])):
            B(FEHLER, "%s: Akteur-Dateien %d != Liste %d" % (thema, n_ak_dat, len(plan.get("akteure", []))))
        budget_ak += n_ak_dat
        if n_inst > regeln["budget"]["instanzen_je_thema"]:
            B(FEHLER, "%s: %d Instanzen > Budget %d" % (thema, n_inst, regeln["budget"]["instanzen_je_thema"]))
        B(HINWEIS, "%s: %d Instanzen, %d Akteure, %d Dateien" % (thema, n_inst, n_ak_dat, len(plan["dateien"])))
    if budget_kol > regeln["budget"]["kollision_gesamt"]:
        B(FEHLER, "Kollision %d > %d" % (budget_kol, regeln["budget"]["kollision_gesamt"]))
    if budget_ak > regeln["budget"]["akteure_gesamt"]:
        B(FEHLER, "Akteure %d > %d" % (budget_ak, regeln["budget"]["akteure_gesamt"]))
    pj = os.path.join(plan_ordner, "akteure_%s.json" % feld)
    if os.path.exists(pj):
        with open(pj, "r", encoding="utf-8") as f:
            al = json.load(f)
        if len(al.get("akteure", [])) != budget_ak:
            B(FEHLER, "akteure_%s.json: %d != %d in den Themen" % (feld, len(al.get("akteure", [])), budget_ak))
    else:
        B(FEHLER, "akteure_%s.json fehlt" % feld)

    # --- Einzelpruefungen je Stueck ----------------------------------------------------------
    n_schweb = n_sperre = n_feld = n_fenster = n_wuerfel = 0
    fuss = []
    for st in stuecke:
        info, q, s, pos = st["info"], st["q"], st["s"], st["pos"]
        mx, my, a, b, w, P = ellipse(info, q, s, pos)
        x, y = float(np.float32(pos[0])) / 100.0, float(np.float32(pos[1])) / 100.0
        if D.feld_von_m(x, y) != feld:
            n_feld += 1
        if not (x0 - 0.5 <= mx < x1 + 0.5 and y0 - 0.5 <= my < y1 + 0.5):
            n_fenster += 1
        zc = int(K.naechst(K.zone, mx, my))
        dw = float(K.bilinear(K.d_wasser, mx, my))
        if zc == FP.ZONEN["sperre"] or dw < regeln["zonen"]["sperre"]["wasser_m"] - 0.5:
            n_sperre += 1
        rolle = st["rollen"][0]
        if st["akteur"]:
            rolle = "turm" if st["thema"] == "klippenband" else "akteur_halde"
        d = max(info["groesse_m"][0] * s[0], info["groesse_m"][1] * s[1], info["groesse_m"][2] * s[2])
        g = info["groesse_m"]
        lang, kurz = max(g), max(min(g), 1e-3)
        form_w = (g[2] >= max(g[0], g[1]) * 0.999) or (lang / kurz < regeln.get("wuerfel_verhaeltnis", 1.4))
        if rolle in ("block", "fussblock") and d > PS["wuerfel_max_d_m"] and form_w:
            n_wuerfel += 1
        # Schweben
        if rolle in FELS_LOKAL:
            bmin, bmax = info["bounds_cm"]
            gg = np.stack(np.meshgrid(np.linspace(bmin[0], bmax[0], 5), np.linspace(bmin[1], bmax[1], 5), [bmin[2]],
                                      indexing="ij"), axis=-1).reshape(-1, 3) * np.asarray(s)[None, :]
            W = INS.q_drehe(q, gg) + pos[None, :]
            gz = K.boden(W[:, 0] / 100.0, W[:, 1] / 100.0)
            if ((W[:, 2] / 100.0 - gz) > PS["schwebe_toleranz_m"]).any():
                n_schweb += 1
        elif rolle in FELS_WELT:
            Pw = P + pos[None, :]
            H = Pw[:, 2].max() - Pw[:, 2].min()
            unten = Pw[Pw[:, 2] <= Pw[:, 2].min() + 0.12 * H]
            gz = K.boden(unten[:, 0] / 100.0, unten[:, 1] / 100.0)
            if ((unten[:, 2] / 100.0 - gz) > PS["schwebe_toleranz_m"]).any():
                n_schweb += 1
        elif rolle in PFLANZE:
            pass
        fuss.append((st["thema"], rolle, mx, my, a * 0.85, b * 0.85, w, d, x, y, float(pos[2]) / 100.0))
    for zahl, text in ((n_feld, "Stuecke ausserhalb Feld %s" % feld), (n_fenster, "Stuecke ausserhalb des Fensters"),
                       (n_sperre, "Stuecke in Sperre (Uferband 0-10 m A20 / Weg / Ort / Meer)"),
                       (n_schweb, "schwebende Felsstuecke"), (n_wuerfel, "wuerfelige/stehende Bloecke > 1,5 m")):
        B(FEHLER if zahl else HINWEIS, "%s: %d" % (text, zahl))
    # Pflanzen: Pivot am Boden
    n_pfl = 0
    for (thema, rolle, mx, my, a, b, w, d, x, y, z) in fuss:
        if rolle in PFLANZE:
            gz = K.boden(x, y)
            if not (gz - 1.0 <= z <= gz + 0.3):   # Median der Kontaktpunkte am Steilhang
                n_pfl += 1
    B(FEHLER if n_pfl else HINWEIS, "Pflanzen/Baeume mit Pivot nicht am Boden: %d" % n_pfl)

    # --- Deckung je Zone (0,5 m) ------------------------------------------------------------
    zr = 0.5
    xs = np.arange(x0 + zr / 2, x1, zr)
    ys = np.arange(y0 + zr / 2, y1, zr)
    X, Y = np.meshgrid(xs, ys)
    cov = np.zeros(X.shape, bool)
    for (thema, rolle, mx, my, a, b, w, d, x, y, z) in fuss:
        if rolle in PFLANZE:
            continue
        r = max(a, b)
        j0 = max(0, int((mx - r - x0) / zr))
        j1 = min(X.shape[1], int((mx + r - x0) / zr) + 2)
        i0 = max(0, int((my - r - y0) / zr))
        i1 = min(X.shape[0], int((my + r - y0) / zr) + 2)
        if j1 <= j0 or i1 <= i0:
            continue
        xx = X[i0:i1, j0:j1] - mx
        yy = Y[i0:i1, j0:j1] - my
        c, s_ = math.cos(w), math.sin(w)
        u = (xx * c + yy * s_) / a
        v = (-xx * s_ + yy * c) / b
        cov[i0:i1, j0:j1] |= (u * u + v * v) <= 1.0
    zone = K.naechst(K.zone, X, Y)
    # Fussflaechen-Summe (wie Dichte-Zensus 6h 'Felsdeckung % Obergrenze', Ueberlappung NICHT abgezogen)
    summe = {}
    for (thema, rolle, mx, my, a, b, w, d, x, y, z) in fuss:
        if rolle in PFLANZE:
            continue
        zc = int(K.naechst(K.zone, mx, my))
        summe[zc] = summe.get(zc, 0.0) + math.pi * a * b
    for name in ("halde", "schrofen", "wand", "fuss"):
        code = FP.ZONEN[name]
        fl = float((zone == code).sum()) * zr * zr
        if fl > 0:
            B(HINWEIS, "Fussflaechen-Summe %s %.0f %% der Zonenflaeche (Obergrenze wie Zensus 6h, RA2 = 378 %%)"
              % (name, 100.0 * summe.get(code, 0.0) / fl))
    th = K.bilinear(K.t_halde, X, Y)
    nah = K.naechst(K.fuss_nah.astype(np.uint8), X, Y).astype(bool)
    deck = {}
    for name, m, schwelle in (("halde", zone == FP.ZONEN["halde"], PS["deckung_halde_min"]),
                              ("halde_oben", (zone == FP.ZONEN["halde"]) & (th < 0.33), PS["deckung_halde_oben_min"]),
                              ("schrofen", zone == FP.ZONEN["schrofen"], PS["deckung_schrofen_min"]),
                              ("wand", zone == FP.ZONEN["wand"], PS["deckung_wand_min"]),
                              ("fuss_nah", (zone == FP.ZONEN["fuss"]) & nah, PS["deckung_fuss_nah_min"]),
                              ("fuss_fern", (zone == FP.ZONEN["fuss"]) & ~nah, None),
                              ("hangwald", zone == FP.ZONEN["hangwald"], None),
                              ("felszone_gesamt", np.isin(zone, [3, 4, 5]), None)):
        if not m.any():
            deck[name] = None
            continue
        v = float(cov[m].mean())
        deck[name] = round(v, 3)
        if schwelle is not None:
            B(FEHLER if v < schwelle else HINWEIS, "Netzdeckung %s %.1f %% (Schwelle %.0f %%)" % (name, 100 * v, 100 * schwelle))
        else:
            B(HINWEIS, "Netzdeckung %s %.1f %%" % (name, 100 * v))

    # Fels-Lage >= 38 Grad ohne Netz (Cloud: vorherrschende Lage boden_2m == Fels/Felsplatte; lokal lage_Fels.r8 > 127)
    boden = K.naechst(K.fe.get("boden"), X, Y)
    fl38 = np.isin(boden, [D.BODEN.index("Fels"), D.BODEN.index("Felsplatte")]) & (K.bilinear(K.n, X, Y) >= 38.0) & \
        (zone != FP.ZONEN["sperre"])
    if fl38.any():
        v38 = float((~cov[fl38]).mean())
        g38 = PS.get("fels_lage_ohne_netz_max", 0.45)
        B(FEHLER if v38 > g38 else HINWEIS, "Fels-Lage >= 38 Grad ohne Netz: %.1f %% (%.2f ha; Grenze %.0f %%)"
          % (100.0 * v38, float(fl38.sum()) * zr * zr / 1e4, 100.0 * g38))
    # --- Dichte je 48-m-Zelle -----------------------------------------------------------------
    hz = (zone == FP.ZONEN["halde"])
    steil = K.bilinear(K.n, X, Y) > 35.0
    cz = 48.0
    ci = ((X - x0) // cz).astype(int)
    cj = ((Y - y0) // cz).astype(int)
    fl_h, fl_s = {}, {}
    for a_, b_, h_, s_ in zip(ci.ravel(), cj.ravel(), hz.ravel(), (steil & ~hz).ravel()):
        pass
    # vektorisiert: Flaechen je Zelle
    key = ci * 1000 + cj
    for kk, arr_ in (("h", hz), ("s", steil & ~hz)):
        u_, cnt = np.unique(key[arr_], return_counts=True)
        (fl_h if kk == "h" else fl_s).update({int(k_): c_ * zr * zr for k_, c_ in zip(u_, cnt)})
    cnt2h, cnt4h, cnt2s = {}, {}, {}
    for (thema, rolle, mx, my, a, b, w, d, x, y, z) in fuss:
        if rolle not in ("block", "fussblock", "akteur_halde"):
            continue
        if rolle == "teppich":
            continue
        k_ = int((mx - x0) // cz) * 1000 + int((my - y0) // cz)
        zc = int(K.naechst(K.zone, mx, my))
        if zc == FP.ZONEN["halde"]:
            if d > 2.0:
                cnt2h[k_] = cnt2h.get(k_, 0) + 1
            if d > 4.0:
                cnt4h[k_] = cnt4h.get(k_, 0) + 1
        elif K.hang_grad(mx, my) > 35.0 and d > 2.0:
            cnt2s[k_] = cnt2s.get(k_, 0) + 1

    def maxdichte(cnt, fl, min_fl=400.0):
        best = 0.0
        for k_, c_ in cnt.items():
            f_ = fl.get(k_, 0.0)
            if f_ >= min_fl:
                best = max(best, 100.0 * c_ / f_)
        return best
    d2h, d4h, d2s = maxdichte(cnt2h, fl_h), maxdichte(cnt4h, fl_h), maxdichte(cnt2s, fl_s)
    for v, gr, t_ in ((d2h, PS["halde_bloecke_gt2_je_100m2_max"], "Halde Bloecke > 2 m"),
                      (d4h, PS["halde_bloecke_gt4_je_100m2_max"], "Halde Bloecke > 4 m"),
                      (d2s, PS["ausserhalb_halde_gt2_je_100m2_max"], "Steilhang ausserhalb Halde Bloecke > 2 m")):
        B(FEHLER if v > gr else HINWEIS, "%s: max %.2f je 100 m2 je 48-m-Zelle (Grenze %.2f)" % (t_, v, gr))

    # --- Baeume -------------------------------------------------------------------------------
    baeume = [(x, y, d) for (thema, rolle, mx, my, a, b, w, d, x, y, z) in fuss if rolle.startswith("baum_")]
    bloecke = [(mx, my, d) for (thema, rolle, mx, my, a, b, w, d, x, y, z) in fuss
               if rolle in ("block", "fussblock", "platte", "akteur_halde") and d >= 1.0]
    felszone = np.isin(zone, [1, 2, 3, 4, 5])
    if baeume:
        bx = np.array([p[0] for p in baeume])
        by = np.array([p[1] for p in baeume])
        near = np.zeros(X.shape, bool)
        for xx_, yy_ in zip(bx, by):
            j0 = max(0, int((xx_ - 7.5 - x0) / zr)); j1 = min(X.shape[1], int((xx_ + 7.5 - x0) / zr) + 2)
            i0 = max(0, int((yy_ - 7.5 - y0) / zr)); i1 = min(X.shape[0], int((yy_ + 7.5 - y0) / zr) + 2)
            near[i0:i1, j0:j1] |= (X[i0:i1, j0:j1] - xx_) ** 2 + (Y[i0:i1, j0:j1] - yy_) ** 2 <= 56.25
        frei = float((~near[felszone]).mean()) if felszone.any() else 1.0
        B(FEHLER if frei < PS["baumfrei_felszone_min"] else HINWEIS,
          "baumfreie Felszone (kein Baum im Radius 7,5 m) %.1f %% (min %.0f %%)" % (100 * frei, 100 * PS["baumfrei_felszone_min"]))
        bl = np.array([[p[0], p[1]] for p in bloecke]) if bloecke else np.zeros((0, 2))
        mit = 0
        for xx_, yy_ in zip(bx, by):
            if bl.size and (np.hypot(bl[:, 0] - xx_, bl[:, 1] - yy_) <= 3.0 + 1.5).any():
                mit += 1
        anteil = mit / len(baeume)
        B(FEHLER if anteil < 0.9 else HINWEIS, "Baeume mit Block >= 1 m im Radius 3 m: %.1f %% (%d/%d), Block:Baum %.2f"
          % (100 * anteil, mit, len(baeume), len(bloecke) / max(len(baeume), 1)))
        # Grat-Reihen: Komponenten (Abstand <= 7 m) von Baeumen im Gratband
        gb = [(x_, y_) for (x_, y_, d_) in baeume if float(K.bilinear(K.d_grat, x_, y_)) < regeln["baumgruppen"]["grat_abstand_m"]]
        best = 0
        rest = list(range(len(gb)))
        while rest:
            stapel = [rest.pop(0)]
            komp = 0
            while stapel:
                i_ = stapel.pop()
                komp += 1
                nb = [j_ for j_ in rest if math.hypot(gb[i_][0] - gb[j_][0], gb[i_][1] - gb[j_][1]) <= 7.0]
                for j_ in nb:
                    rest.remove(j_)
                stapel.extend(nb)
            best = max(best, komp)
        B(FEHLER if best > PS["grat_reihe_max"] else HINWEIS, "groesste Baumkette am Grat: %d (max %d), Baeume im Gratband %d"
          % (best, PS["grat_reihe_max"], len(gb)))
        hs = sorted(p[2] for p in baeume)
        B(HINWEIS, "Baumhoehen min/median/max %.1f/%.1f/%.1f m, hoechster/niedrigster %.2f" %
          (hs[0], hs[len(hs) // 2], hs[-1], hs[-1] / max(hs[0], 0.1)))
    # --- Masken ---------------------------------------------------------------------------------
    mj = os.path.join(plan_ordner, "masken_%s.json" % feld)
    if not os.path.exists(mj):
        B(FEHLER, "masken_%s.json fehlt" % feld)
    else:
        with open(mj, "r", encoding="utf-8") as f:
            meta = json.load(f)
        fij = meta["fenster_ij"]
        for name, m in meta["masken"].items():
            pf = os.path.join(plan_ordner, m["datei"])
            if not os.path.exists(pf) or os.path.getsize(pf) != fij[2] * fij[3]:
                B(FEHLER, "Maske %s: fehlt oder Groesse != %d x %d" % (name, fij[2], fij[3]))
                continue
            a = np.fromfile(pf, np.uint8)
            if name == "ausduennen" and not np.isin(a, [0, 255]).all():
                B(FEHLER, "Ausduenn-Maske nicht nur 0/255")
            if name == "ausduennen":
                B(HINWEIS, "Ausduenn-Maske: %.1f %% des Fensters" % (100.0 * (a == 255).mean()))
        lb = meta.get("lagen") or {}
        for n in lb.get("lagen", []):
            pf = os.path.join(plan_ordner, lb["datei_praefix"] + n + ".r8")
            if not os.path.exists(pf) or os.path.getsize(pf) != lb["fenster_ij"][2] * lb["fenster_ij"][3]:
                B(FEHLER, "Lage %s: fehlt oder falsche Groesse" % n)
            if n not in D.BODEN:
                B(FEHLER, "Lage %s unbekannt (FORMAT §2)" % n)
    # --- A15 Variante B -------------------------------------------------------------------------
    gj = os.path.join(plan_ordner, "gelaende_%s_variante_b" % feld, "plan.json")
    if not os.path.exists(gj):
        B(FEHLER, "Hoehenplan Variante B fehlt")
    else:
        with open(gj, "r", encoding="utf-8") as f:
            gp = json.load(f)
        for ab in gp["abschnitte"]:
            g = ab["gelaende"]
            pf = os.path.join(os.path.dirname(gj), g["datei"])
            i0_, j0_, hh, ww = g["fenster_ij"]
            if not os.path.exists(pf) or os.path.getsize(pf) != hh * ww * 4:
                B(FEHLER, "A15 %s: Datei fehlt/Groesse" % ab["id"])
                continue
            dd = np.fromfile(pf, "<f4").reshape(hh, ww)
            if not np.isfinite(dd).all():
                B(FEHLER, "A15: NaN")
            if dd.min() < -1e-4:
                B(FEHLER, "A15: Abtrag %.3f m (nur anheben erlaubt)" % float(dd.min()))
            if float(np.abs(dd).max()) > g["max_aenderung_m"] + 0.011:
                B(FEHLER, "A15: |Delta| > max_aenderung_m")
            if max(np.abs(dd[0]).max(), np.abs(dd[-1]).max(), np.abs(dd[:, 0]).max(), np.abs(dd[:, -1]).max()) > 1e-4:
                B(FEHLER, "A15: Delta am Fensterrand != 0")
            ii, jj = np.nonzero(dd > 1e-3)
            if ii.size:
                xm, ym = D.pixel_zu_m(ii + i0_, jj + j0_, 1.0)
                dw = K.bilinear(K.d_wasser, xm, ym) if delta is None else FP.Kontext(welt, regeln).bilinear(K.d_wasser, xm, ym)
                n_w = int((np.asarray(dw) < regeln["gelaende"]["wasser_frei_m"] - 1.0).sum())
                B(FEHLER if n_w else HINWEIS, "A15: Zellen mit Auftrag naeher als %.0f m am Wasser: %d" % (regeln["gelaende"]["wasser_frei_m"], n_w))
            B(HINWEIS, "A15 %s: max %.2f m, Auftrag %.0f m3, %d Kegel" % (ab["id"], float(dd.max()), float(dd.sum()), len(gp.get("kegel", []))))
    return {"deckung": deck, "dichte_max": {"halde_gt2": round(d2h, 3), "halde_gt4": round(d4h, 3), "steil_gt2": round(d2s, 3)},
            "variante": variante}


def hash_ordner(o):
    h = {}
    for wurzel, _, dateien in os.walk(o):
        for fn in sorted(dateien):
            if fn.startswith("pruefbericht"):
                continue
            p = os.path.join(wurzel, fn)
            with open(p, "rb") as f:
                h[os.path.relpath(p, o).replace(os.sep, "/")] = hashlib.sha256(f.read()).hexdigest()
    return h


def determinismus(regeln_pfad, B, extra):
    plan = os.path.join(HIER, "felsdeckung_plan.py")
    t = tempfile.mkdtemp(prefix="fd_det_")
    try:
        hs = []
        for k, seed in ((1, "1"), (2, "4711")):
            o = os.path.join(t, "lauf%d" % k)
            env = dict(os.environ, PYTHONHASHSEED=seed)
            r = subprocess.run([sys.executable, "-I", plan, "--regeln", regeln_pfad, "--aus", o, "--bild"] + extra,
                               env=env, capture_output=True, text=True)
            if r.returncode != 0:
                B(FEHLER, "Determinismus: Lauf %d Fehler %s" % (k, r.stdout[-400:] + r.stderr[-400:]))
                return
            hs.append(hash_ordner(o))
        if hs[0] != hs[1]:
            diff = sorted(k for k in set(hs[0]) | set(hs[1]) if hs[0].get(k) != hs[1].get(k))
            B(FEHLER, "Determinismus: %d Dateien verschieden (%s)" % (len(diff), ", ".join(diff[:5])))
        else:
            B(HINWEIS, "Determinismus: zwei Laeufe (PYTHONHASHSEED 1/4711) byte-gleich, %d Dateien" % len(hs[0]))
    finally:
        shutil.rmtree(t, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pruefer Felsdeckung Auftrag 21")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--regeln", default=os.path.join(HIER, "felsdeckung_regeln.json"))
    ap.add_argument("--daten2m", default=None)
    ap.add_argument("--daten1m", default=None)
    ap.add_argument("--inventar", default=None)
    ap.add_argument("--determinismus", action="store_true")
    a = ap.parse_args(argv)
    with open(a.regeln, "r", encoding="utf-8") as f:
        regeln = json.load(f)
    welt = D.lade(daten2m=a.daten2m, daten1m=a.daten1m, pfade=False)
    inv = INV.Inventar.lade(a.inventar)
    B = Bericht()
    erg = pruefe(a.plan, regeln, welt, inv, B)
    if a.determinismus:
        extra = []
        if a.daten1m:
            extra += ["--daten1m", a.daten1m]
        if a.daten2m:
            extra += ["--daten2m", a.daten2m]
        determinismus(os.path.abspath(a.regeln), B, extra)
    zeilen = ["Pruefbericht Felsdeckung %s (Variante %s)" % (regeln["pilot"]["feld"], erg["variante"])]
    for s, t in B.z:
        zeilen.append("%-8s %s" % (s, t))
    zeilen.append("Ergebnis: %d FEHLER, %d WARNUNG, %d HINWEIS" % (B.zahl(FEHLER), B.zahl(WARNUNG), B.zahl(HINWEIS)))
    text = "\n".join(zeilen) + "\n"
    text = text.encode("ascii", "replace").decode("ascii")
    sys.stdout.write(text)
    with open(os.path.join(a.plan, "pruefbericht_%s.txt" % regeln["pilot"]["feld"]), "w", encoding="ascii") as f:
        f.write(text)
    return 1 if B.zahl(FEHLER) else 0


if __name__ == "__main__":
    sys.exit(main())
