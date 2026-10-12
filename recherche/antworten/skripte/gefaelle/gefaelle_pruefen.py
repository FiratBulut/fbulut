#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gefaelle_pruefen.py - Pruefer fuer die Planausgaben von gefaelle_plan.py (Auftrag 15).

Aufruf:  python -I gefaelle_pruefen.py <aus> [<aus> ...] [--daten2m DIR | --daten1m DIR] [--ohne-daten]
         <aus> = Ordner eines Laufs (mit plan.json) oder Ordner mit Lauf-Unterordnern.
Exit-Code 1 bei FEHLER.

Geprueft (Regelwerk = gefaelle_regeln.json, regeln_hart + Zahlen):
  Spiegel   spiegel_neu_cm nie steigend (Toleranz 0); Anfang/Ende des Laufs auf alter Hoehe; nie ueber dem alten
            Spiegel; Stufe = zwei Punkte <= stufen.zwei_punkte.abstand_max; Becken <= becken.gefaelle.absolut_max
            (FEHLER), > becken.gefaelle.max (WARNUNG); Schnelle-Rampe <= rampe_gefaelle_max.
  Stufen    Fall je Art in stufen.arten [D_min, D_max] (Fall <= faelle.hoehe_max_einzeln; Kaskade je Teilstufe),
            <= max_stufen_je_100m, lippe_cm 3-7 Punkte, fuss_z < Lippe.
  Wasser    (Befund 14b, Variante A) wasser_koerper = River + Kaskadennetz: Spiegel/Netz-Mittellinie monoton fallend,
            Nachbarn ueberlappen genau 0,5 m, sonst nichts (River auch in der Draufsicht), jede Stufe liegt in einem Netz,
            Bett >= 0,2 m unter dem Spiegel und Ufer am Netzrand >= 0,1 m darueber (Gelaende nach dem Stempel),
            je Stufe Niagara oder Vorhang (WARNUNG, wenn die Grenze 'gleichzeitig' das verhindert).
  Assets    Netze (Instanz-Ebene + Akteure) in netze.csv, nicht gesperrt, kein Saegeschnitt (13k, Wildnis);
            Niagara in inventar_extra.json.
  Budget    je Abschnitt <= SEHENS_FORMAT §9 (sehens_pruefen.pruefe_ebene, Kontext 'gefaelle'), Akteure <= 50 je 200 m
            Lauflaenge (gleitendes Fenster, 13k-Rueckfrage 6; die Sehens-Grenze 50 je Ort gilt hier nicht je
            Abschnitt), Effekte <= 3 je Stufe, <= 6 gleichzeitig (Proben alle 2 m entlang des Spiegels,
            Cull-Radius), Cull 30-150 m; je Feld <= 60 000.
  Eingriffe Gelaende-Delta: Rand 0, |Delta| > 40 m nur mit Begruendung, keine Aenderung <= 2 m an Wegen/Pfaden
            (FEHLER), <= 5 m an Orten (FEHLER), in Sehenswuerdigkeiten (Radius) (FEHLER); Instanzen nicht auf
            Wegen (WARNUNG) und Orten (FEHLER); Lagen-Dateien vorhanden.
  Kameras   §8-Format, _vorher/_nachher paarweise, Hoch = -170, je Pilot-Strecke vorhanden.
"""

import argparse
import json
import math
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.dirname(HIER))

import numpy as np  # noqa: E402

import gefaelle_daten as gd  # noqa: E402
import gefaelle_regelwerk as gr  # noqa: E402

FEHLER, WARNUNG, HINWEIS = "FEHLER", "WARNUNG", "HINWEIS"
TOL = 1e-6


def _s_entlang(P):
    xy = np.asarray(P, np.float64)[:, :2] / 100.0
    return np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(xy, axis=0).T))])


def pruefe_spiegel(p, rw, b, tag):
    sp = p.get("spiegel_neu_cm") or []
    art = p.get("spiegel_neu_art") or ["?"] * len(sp)
    if len(sp) < 2:
        b.append((FEHLER, tag, "spiegel_neu_cm fehlt/leer"))
        return
    z = np.array([q[2] for q in sp], np.float64)
    steigt = np.flatnonzero(np.diff(z) > TOL)
    if steigt.size:
        b.append((FEHLER, tag, "Spiegel steigt an %d Stellen (erste bei Punkt %d: +%.3f m)"
                  % (steigt.size, steigt[0], (z[steigt[0] + 1] - z[steigt[0]]) / 100.0)))
    alt = np.array([q[2] for q in p["spiegel_alt_cm"]], np.float64)
    alt_m = np.minimum.accumulate(alt)
    for name, i_neu, i_alt in (("Anfang", 0, 0), ("Ende", -1, -1)):
        if abs(z[i_neu] - alt_m[i_alt]) > 2.0:
            b.append((FEHLER, tag, "%s des Laufs nicht auf alter Hoehe (%.2f statt %.2f m)"
                      % (name, z[i_neu] / 100.0, alt_m[i_alt] / 100.0)))
    s_neu = np.asarray(p.get("spiegel_neu_s_m") or _s_entlang(sp), np.float64)
    s_alt = _s_entlang(p["spiegel_alt_cm"])
    ueber = z - np.interp(s_neu, s_alt, alt_m)
    if (ueber > 5.0).any():
        b.append((WARNUNG, tag, "neuer Spiegel bis %.2f m ueber dem alten (Ufer pruefen)" % (ueber.max() / 100.0)))
    _, zp_max = rw.zwei_punkte()
    gb_max = float(rw.r["becken"]["gefaelle"].get("max", 0.02))
    gb_hart = rw.becken_gefaelle_hart()
    _, rampe_max = rw.rampe(0.5)
    n_zp = n_becken_w = 0
    z_alt_bei = np.interp(s_neu, s_alt, alt_m)
    for k in range(len(sp) - 1):
        dh = math.hypot((sp[k + 1][0] - sp[k][0]) / 100.0, (sp[k + 1][1] - sp[k][1]) / 100.0)
        dz = (z[k] - z[k + 1]) / 100.0
        a0, a1 = art[k], art[k + 1]
        if a1 == "lippe" and a0 in ("alt",) and abs(z[k] - z_alt_bei[k]) < 5.0 and abs(z[k + 1] - z_alt_bei[k + 1]) < 5.0:
            continue                                   # unveraenderter alter Lauf bis zur ersten Lippe
        if a0 == "lippe" and a1 == "fuss":
            if dh > zp_max + 0.01:
                n_zp += 1
        elif a0 == "lippe" and a1 == "rampe":
            if dh > 0 and dz / dh > rampe_max + 0.01:
                b.append((FEHLER, tag, "Schnelle-Rampe bei Punkt %d: %.0f %% > %.0f %%" % (k, 100 * dz / dh, 100 * rampe_max)))
        elif a0 != "alt" or a1 != "alt":
            if dh > 0.05:
                g = dz / dh
                if g > gb_hart + 1e-3:
                    b.append((FEHLER, tag, "Becken bei Punkt %d: Gefaelle %.1f %% > %.1f %% (hart)" % (k, 100 * g, 100 * gb_hart)))
                elif g > gb_max + 1e-3:
                    n_becken_w += 1
    if n_zp:
        b.append((FEHLER, tag, "%d Stufen: zwei Punkte weiter als %.1f m auseinander" % (n_zp, zp_max)))
    if n_becken_w:
        b.append((WARNUNG, tag, "%d Beckenabschnitte steiler als %.0f %%" % (n_becken_w, 100 * gb_max)))


def pruefe_stufen(p, rw, b, tag):
    st = p.get("stufen") or []
    hmax = rw.hoehe_max_einzeln()
    for e in st:
        a = e.get("art_regel", e.get("art"))
        lo, hi = rw.art_bereich(a)
        if a == "fall":
            hi = hmax
        D = e["fall_m"]
        if a == "kaskade" and e.get("teilstufen"):
            for t in e["teilstufen"]:
                if t["fall_m"] > hi + 0.01:
                    b.append((FEHLER, tag, "%s: Teilstufe %.2f m > Kaskade D_max %.1f m" % (e["id"], t["fall_m"], hi)))
                elif t["fall_m"] < lo - 0.01:
                    b.append((HINWEIS, tag, "%s: Teilstufe %.2f m < D_min %.1f m" % (e["id"], t["fall_m"], lo)))
        elif D > hi + 0.01:
            b.append((FEHLER, tag, "%s: %s %.2f m > D_max %.1f m (Regelwerk)" % (e["id"], a, D, hi)))
        elif D < lo - 0.01:
            b.append((HINWEIS, tag, "%s: %s %.2f m < D_min %.2f m" % (e["id"], a, D, lo)))
        if e["fuss_z_cm"] > e["lippe_cm"][0][2] + TOL:
            b.append((FEHLER, tag, "%s: Fuss hoeher als Lippe" % e["id"]))
        n_min, n_max = gr.lippe_punkte(rw)
        if not (n_min <= len(e["lippe_cm"]) <= n_max):
            b.append((WARNUNG, tag, "%s: lippe_cm hat %d Punkte (%d-%d)" % (e["id"], len(e["lippe_cm"]), n_min, n_max)))
        if e.get("art") not in ("fall", "kaskade", "schnelle"):
            b.append((FEHLER, tag, "%s: art %r (fall | kaskade | schnelle)" % (e["id"], e.get("art"))))
    # Dichte je 100 m
    mx = rw.max_stufen_je_100m()
    s = np.array(sorted(e["s_m"] for e in st))
    for k in range(len(s)):
        n = int(((s >= s[k]) & (s < s[k] + 100.0)).sum())
        if n > mx:
            b.append((WARNUNG, tag, "%d Stufen auf 100 m ab s = %.0f m (> %d)" % (n, s[k], mx)))
            break


def regelmaessigkeit(p):
    """15f: Kennzahlen je Strecke: Variationskoeffizient der Lippenabstaende (innerhalb eines Segments) und der
    Fallhoehen aller Lippen (Teilstufen einzeln), Streuung der Lippenwinkel (Grad), Anteil schraeger Lippen."""
    out = {}
    for x in p.get("strecken") or []:
        st = [e for e in p.get("stufen") or [] if e.get("strecke") == x["id"]]
        lips = []
        for e in st:
            if e.get("teilstufen"):
                for t_ in e["teilstufen"]:
                    lips.append((t_["s_m"], t_["fall_m"], (t_.get("lippe_form") or {}).get("winkel_grad")))
            else:
                lips.append((e["s_m"], e["fall_m"], (e.get("lippe_form") or {}).get("winkel_grad")))
        lips.sort()
        if len(lips) < 3:
            continue
        segs = x.get("segmente_m") or [[-1e9, 1e9]]
        abst = []
        for a_, b_ in segs:
            s_ = [v[0] for v in lips if a_ - 1e-6 <= v[0] <= b_ + 1e-6]
            abst += list(np.diff(s_))
        D = np.array([v[1] for v in lips])
        W = np.array([v[2] if v[2] is not None else 0.0 for v in lips])
        abst = np.array(abst) if abst else np.zeros(0)
        out[x["id"]] = {"lippen": len(lips),
                        "cv_abstand": float(abst.std() / abst.mean()) if len(abst) >= 2 and abst.mean() > 0 else 0.0,
                        "cv_hoehe": float(D.std() / D.mean()) if D.mean() > 0 else 0.0,
                        "winkel_streuung_grad": float(W.std()), "winkel_betrag_mittel_grad": float(np.abs(W).mean()),
                        "schraeg_anteil": float((np.abs(W) >= 10.0).mean())}
    return out


def pruefe_regelmaessigkeit(p, b, tag):
    """15f: Treppen-Verdacht als HINWEIS: CV Abstaende oder Hoehen < 0,2, Lippenwinkel alle gleich (Streuung < 3 Grad)."""
    for sid, r in regelmaessigkeit(p).items():
        if r["cv_abstand"] < 0.2:
            b.append((HINWEIS, sid, "Lippenabstaende zu regelmaessig (CV %.2f < 0,2)" % r["cv_abstand"]))
        if r["cv_hoehe"] < 0.2:
            b.append((HINWEIS, sid, "Fallhoehen zu regelmaessig (CV %.2f < 0,2)" % r["cv_hoehe"]))
        if r["winkel_streuung_grad"] < 3.0:
            b.append((HINWEIS, sid, "Lippenwinkel alle gleich (Streuung %.1f Grad)" % r["winkel_streuung_grad"]))


def pruefe_wasser(p, ordner, welt, b, tag, h1m=None):
    """Variante A (14b): River + Kaskadennetz. Monotonie, Ueberlappung nur 0,5 m, Bett/Ufer am Netz, jede Stufe im Netz."""
    from gefaelle_plan import ueberlappungen, KN
    from sehens_lib.sehens_pruefen import BodenNachStempel
    wk = p.get("wasser_koerper") or []
    if not wk:
        b.append((FEHLER, tag, "wasser_koerper fehlt"))
        return
    if p.get("flussstuecke"):
        b.append((FEHLER, tag, "flussstuecke mit Luecken sind abgeschafft (14b)"))
    for w in wk:
        if w.get("typ") not in ("river", "kaskadennetz", "custom", "statisch_platte"):
            b.append((FEHLER, tag, "%s: typ %r" % (w.get("id"), w.get("typ"))))
        P = w.get("punkte") or w.get("mittellinie") or []
        if len(P) < 2:
            b.append((FEHLER, tag, "%s: < 2 Punkte" % w.get("id")))
            continue
        z = [q[2] for q in P]
        if any(z[k + 1] > z[k] + TOL for k in range(len(z) - 1)):
            b.append((FEHLER, tag, "%s: %s steigt" % (w["id"], "Netz-Mittellinie" if w["typ"] == "kaskadennetz" else "Spiegel")))
        if w["typ"] == "kaskadennetz" and len(w.get("knick") or []) != len(P):
            b.append((FEHLER, tag, "%s: knick und mittellinie verschieden lang" % w["id"]))
    # Ueberlappung entlang des Laufs: Nachbarn genau ueberlapp_m, sonst keine
    o = sorted(wk, key=lambda w: w["s_m"][0])
    for k in range(len(o)):
        for j in range(k + 1, len(o)):
            ue = o[k]["s_m"][1] - o[j]["s_m"][0]
            if j == k + 1:
                if abs(ue - KN["ueberlapp_m"]) > 0.06:
                    b.append((FEHLER, tag, "%s/%s ueberlappen %.2f m (soll %.1f m)" % (o[k]["id"], o[j]["id"], ue,
                                                                                    KN["ueberlapp_m"])))
            elif ue > 1e-3:
                b.append((FEHLER, tag, "%s/%s ueberlappen (nicht benachbart)" % (o[k]["id"], o[j]["id"])))
    rv = [w for w in wk if w["typ"] == "river"]
    for w in rv:                                          # 15c: kurze River-Stuecke zeichnen trockene Becken (14b)
        if w["s_m"][1] - w["s_m"][0] < KN["river_min_m"] - 1e-3:
            b.append((FEHLER, tag, "%s: River %.1f m < %.0f m (gehoert als Rampe ins Kaskadennetz)"
                      % (w["id"], w["s_m"][1] - w["s_m"][0], KN["river_min_m"])))
    if len(rv) > 1:
        ue = ueberlappungen([{"punkte": w["punkte"]} for w in rv])
        if ue:
            b.append((FEHLER, tag, "River-Abschnitte ueberlappen in der Draufsicht: %s" % ue[:5]))
    kn = [w for w in wk if w["typ"] == "kaskadennetz"]
    for e in p.get("stufen") or []:
        if not any(w["s_m"][0] - 1e-3 <= e["s_m"] <= w["s_m"][1] + 1e-3 for w in kn):
            b.append((FEHLER, tag, "%s liegt in keinem Kaskadennetz" % e["id"]))
    # (d) Niagara oder Vorhang je Stufe
    from gefaelle_plan import NIAGARA
    fx = {e["stufe"] for e in p.get("effekte") or []}
    hoch = {e["id"] for e in p.get("stufen") or [] if e["fall_m"] >= NIAGARA["D_min_m"]}
    ohne = [sid for w in kn for sid in w.get("stufen", []) if sid in hoch and sid not in fx
            and sid not in (w.get("vorhang_an_stufen") or [])]
    if ohne:
        b.append((WARNUNG, tag, "%d Stufen >= 1 m ohne Niagara und ohne Vorhang (Grenze gleichzeitig; Schaum nur im Netz): %s"
                  % (len(ohne), ", ".join(x_[-3:] for x_ in ohne[:12]))))
    # (a) Bett >= 0,2 m unter dem Spiegel, (b) Ufer am Netzrand >= 0,1 m ueber dem Spiegel - Gelaende NACH dem Stempel
    if welt is None:
        return
    orte = [{"id": a["id"], "gelaende": a.get("gelaende")} for a in p.get("abschnitte") or []]
    from gefaelle_plan import nahe_stufe
    if h1m is not None:                                   # 15b: altes Gelaende aus den 1-m-Fenstern, exakt
        boden = gd.BodenNachStempel1m(welt, orte, ordner, h1m)
        alt_hoehe = h1m.hoehe
        zelle = 1.0
    else:
        boden = BodenNachStempel(welt, orte, ordner)
        alt_hoehe = lambda x_, y_: welt.bilinear(welt.hoehe, x_, y_)  # noqa: E731
        zelle = welt.zelle_m
    from gefaelle_plan import raster_stufe, raster_text, ufer_proben, quer_u
    zus = max(zelle - 1.0, 0.0)                         # 2-m-Naeherung (siehe gefaelle_plan.RASTER_ZUSCHLAG)
    for w in kn:
        M = np.asarray(w["mittellinie"], np.float64)
        kn_ = w["knick"]
        Q = w.get("quer")
        if Q is not None:
            # 15f: Querprofil - Laenge, Monotonie je Laengsstreifen (Spiegel steigt nie), Wertebereiche
            if len(Q) != len(M) or any(len(r) != w.get("quer_punkte", 0) for r in Q):
                b.append((FEHLER, tag, "%s: quer passt nicht zur Mittellinie" % w["id"]))
                Q = None
            else:
                ZQ = M[:, 2][:, None] + np.asarray([[c[0] for c in r] for r in Q], np.float64)
                steigt = int((np.diff(ZQ, axis=0) > 2.0).sum())
                if steigt:
                    b.append((FEHLER, tag, "%s: Querprofil-Wasserlinie steigt an %d Stellen (> 2 cm)" % (w["id"], steigt)))
                # 15f-Nachtrag: dz_cm ist relativ zu z_cm des eigenen Punkts. Massgeblich ist die absolute Wasserhoehe
                # z_cm + dz_cm: an Punkten mit gleichem s identisch, Spruenge laengs und quer hoechstens die groesste
                # Lippenhoehe des Netzes (+ 5 cm). Sonst wuerde das Netz reissen.
                sm_ = np.asarray(w.get("mittellinie_s_m") or [], np.float64)
                d_max = max([t_["fall_m"] for e_ in p.get("stufen") or [] if e_["id"] in (w.get("stufen") or [])
                             for t_ in (e_.get("teilstufen") or [e_])] + [0.0]) * 100.0 + 5.0
                if len(sm_) == len(ZQ):
                    gleich = np.abs(np.diff(sm_)) < 1e-6
                    if gleich.any() and float(np.abs(np.diff(ZQ, axis=0))[gleich].max()) > 1.0:
                        b.append((FEHLER, tag, "%s: Wasserhoehe (z + dz) an Punkten mit gleichem s verschieden" % w["id"]))
                if float(np.abs(np.diff(ZQ, axis=0)).max()) > d_max or float(np.abs(np.diff(ZQ, axis=1)).max()) > d_max:
                    b.append((FEHLER, tag, "%s: Wasserhoehe (z + dz) springt mehr als die groesste Lippenhoehe" % w["id"]))
                for kk_, nm_ in ((0, "Anfang"), (len(Q) - 1, "Ende")):
                    if max(abs(c[0]) for c in Q[kk_]) > 10.0:
                        b.append((FEHLER, tag, "%s: Querprofil am %s nicht eben (|dz| > 10 cm) - Anschluss an River"
                                  % (w["id"], nm_)))
                DS_ = np.asarray([[c[1:3] for c in r] for r in Q], np.float64)
                if DS_.min() < -1e-6 or DS_.max() > 1.0 + 1e-6:
                    b.append((FEHLER, tag, "%s: deckung/schaum ausserhalb 0-1" % w["id"]))
                pruefe_schaum_15g(w, M, Q, ZQ, sm_, b, tag)
        nah = nahe_stufe(w["mittellinie"], kn_, zus)
        ix = [k for k in range(len(M)) if kn_[k] == "becken" and not nah[k]]
        n_b = len(ix)
        n_bett = 0
        for k in ix:
            t = M[k + 1, :2] - M[k, :2] if k + 1 < len(M) else M[k, :2] - M[k - 1, :2]
            tx, ty = t / max(float(np.hypot(*t)), 1e-6)
            x, y, zs, br = M[k, 0] / 100.0, M[k, 1] / 100.0, M[k, 2] / 100.0, M[k, 3] / 100.0
            off = np.linspace(-1, 1, 7) * max(KN["bett_proben_anteil"] * br - zus, 0.15 * br)   # 15b: nasses Bett
            if Q is not None:                                 # 15f: Wasser an der jeweiligen Stelle (schraege Lippen)
                zw = zs + np.interp(off, quer_u(br, len(Q[k])), [c[0] / 100.0 for c in Q[k]])
            else:
                zw = np.full(len(off), zs)
            if float(np.mean(zw - boden.hoehe(x + ty * off, y - tx * off))) < KN["bett_unter_spiegel_min_m"] - 0.005:
                n_bett += 1
        # Ufer je Seite (15c): Muendung nur an der Zuflusslinie, Bestand nur bei altem Ufer unter Spiegel + 0,1 - 1 m
        mu = [{"breite_m": m_["breite_m"], "linie_m": (np.asarray(m_["linie_cm"], np.float64) / 100.0).tolist()}
              for m_ in w.get("muendungen") or []]
        pr_ = ufer_proben(w["mittellinie"], ix, boden.hoehe, alt_hoehe, mu, zus, Q,
                          w.get("mittellinie_s_m") if Q is not None else None)
        n_ufer = sum(1 for q in pr_ if q[6] == "fehl")
        n_bestand = sum(1 for q in pr_ if q[6] == "bestand")
        if n_bestand:
            b.append((WARNUNG, tag, "%s: Ufer am Netzrand an %d Proben schon im Bestand unter dem Spiegel (altes Ufer "
                      "> 0,75 m unter dem Spiegel, Uferring <= 1 m reicht nicht)" % (w["id"], n_bestand)))
        if n_bett:
            b.append((raster_stufe(n_bett, n_b, zus), tag, "%s: Bett an %d von %d Beckenpunkten < 0,2 m unter dem Spiegel%s"
                      % (w["id"], n_bett, n_b, raster_text(n_bett, n_b, zus))))
        if n_ufer:
            b.append((raster_stufe(n_ufer, 2 * n_b, zus), tag, "%s: Ufer am Netzrand an %d von %d Proben < 0,1 m ueber "
                      "dem Spiegel%s" % (w["id"], n_ufer, 2 * n_b, raster_text(n_ufer, 2 * n_b, zus))))


def pruefe_schaum_15g(w, M, Q, ZQ, S, b, tag):
    """15g: Querabstand <= 1 m (>= 21 Stuetzpunkte), weiche Schaumkanten (Nachbarsprung quer <= 0,5, laengs <= 0,5 je
    0,5 m), Schaum nur auf feinem Laengsraster (<= 0,6 m), Schaum >= 0,5 nicht in der Beckenmitte (je Laengsstreifen),
    tiefe_cm >= 0 - alles FEHLER; Schaum >= 0,5 auf > 25 % der Netzflaeche WARNUNG."""
    from gefaelle_plan import KN
    N = len(Q[0])
    A = np.asarray(Q, np.float64)
    sc, tf = A[:, :, 2], A[:, :, 3]
    du = (M[:, 3] / 100.0 + 2.0 * KN["rand_ueberstand_m"]) / max(N - 1, 1)
    if N < 21 or float(du.max()) > 1.0 + 1e-3:
        b.append((FEHLER, tag, "%s: Querprofil zu grob (%d Stuetzpunkte, Abstand bis %.2f m; verlangt >= 21 und <= 1 m)"
                  % (w["id"], N, float(du.max()))))
    if float(tf.min()) < -1e-6:
        b.append((FEHLER, tag, "%s: tiefe_cm < 0" % w["id"]))
    jq = np.abs(np.diff(sc, axis=1))
    if float(jq.max()) > 0.5 + 1e-6:
        b.append((FEHLER, tag, "%s: harte Schaumkante quer (Sprung %.2f > 0,5 zwischen Nachbarpunkten, %d Stellen)"
                  % (w["id"], float(jq.max()), int((jq > 0.5 + 1e-6).sum()))))
    if len(S) != len(M):
        return
    ds = np.diff(S)
    jl = np.abs(np.diff(sc, axis=0))
    erl = 0.5 * np.maximum(ds / 0.5, 1.0)[:, None] + 1e-6
    if (jl > erl).any():
        b.append((FEHLER, tag, "%s: harte Schaumkante laengs (Sprung bis %.2f je 0,5 m, %d Stellen)"
                  % (w["id"], float((jl / np.maximum(ds / 0.5, 1.0)[:, None]).max()), int((jl > erl).sum()))))
    grob = (np.maximum(sc[:-1], sc[1:]).max(axis=1) > 0.05) & (ds > 0.6)
    if grob.any():
        b.append((FEHLER, tag, "%s: Schaum auf grobem Laengsraster (%d Abschnitte > 0,6 m)" % (w["id"], int(grob.sum()))))
    gew = np.zeros(len(S))
    gew[:-1] += ds / 2.0
    gew[1:] += ds / 2.0
    W = (gew * du)[:, None] * np.ones((1, N))
    anteil = float((W * (sc >= 0.5)).sum() / max(float(W.sum()), 1e-9))
    if anteil > 0.25:
        b.append((WARNUNG, tag, "%s: Schaum >= 0,5 auf %.0f %% der Netzflaeche (> 25 %%, nur Lippen/Zunge/Aufprall; "
                  "dichte Fallkette?)" % (w["id"], 100.0 * anteil)))
    # je Laengsstreifen: Becken = Lauf ohne Absturz (absolute Wasserhoehe faellt < 3 cm); in Becken >= 6 m darf in
    # [Anfang + 0,5 L + 1,5 m, Ende - 1 m] kein Schaum >= 0,5 liegen (Aufprall <= 30 % L + Rand, Saum <= 0,5 m)
    n_mitte = 0
    for j in range(N):
        z = ZQ[:, j]
        brueche = np.flatnonzero(np.diff(z) < -3.0)
        starts = np.concatenate([[0], brueche + 1])
        enden = np.concatenate([brueche, [len(z) - 1]])
        for k0, k1 in zip(starts, enden):
            L = S[k1] - S[k0]
            if L < 6.0:
                continue
            m = (S[k0:k1 + 1] >= S[k0] + 0.5 * L + 1.5) & (S[k0:k1 + 1] <= S[k1] - 1.0)
            n_mitte += int((sc[k0:k1 + 1, j][m] >= 0.5).sum())
    if n_mitte:
        b.append((FEHLER, tag, "%s: Schaum >= 0,5 in der Beckenmitte (%d Stuetzpunkte)" % (w["id"], n_mitte)))


def pruefe_effekte(p, rw, inv, b, tag):
    from gefaelle_plan import NIAGARA
    ef = p.get("effekte") or []
    gz = gr.effekt_grenzen(rw)
    je = {}
    for e in ef:
        je[e["stufe"]] = je.get(e["stufe"], 0) + 1
        if inv is not None:
            for st, t in inv.asset_pruefen("niagara", e["asset"], bool(e.get("optional"))):
                b.append((st, tag, "Effekt %s: %s" % (e["stufe"], t)))
        cull_min = NIAGARA["zusatz_cull_m"] if e.get("effekt_art") == "zusatz_aufprall" else gz["cull_klein"]
        if not (cull_min - TOL <= e["cull_m"] <= max(gz["cull_held"]) + TOL):
            b.append((FEHLER, tag, "Effekt %s: cull %.0f m ausserhalb %.0f-%.0f m" % (e["stufe"], e["cull_m"], gz["cull_klein"],
                                                                                     max(gz["cull_held"]))))
        if e.get("typ") != "niagara" or len(e.get("rot_q", [])) != 4 or len(e.get("pos_cm", [])) != 3:
            b.append((FEHLER, tag, "Effekt %s: Format §6 (typ niagara, pos_cm, rot_q)" % e["stufe"]))
    for sid, n in je.items():
        if n > gz["je_stufe"]:
            b.append((FEHLER, tag, "%s: %d Effekte > %d je Stufe" % (sid, n, gz["je_stufe"])))
    sp = p.get("spiegel_neu_cm") or []
    if ef and len(sp) > 1:
        P = np.asarray(sp, np.float64)[:, :2] / 100.0
        s = _s_entlang(sp)
        ps = np.arange(0, s[-1], 2.0)
        px, py = np.interp(ps, s, P[:, 0]), np.interp(ps, s, P[:, 1])
        zahl = np.zeros(len(ps), int)
        alle = np.zeros(len(ps), int)
        for e in ef:
            m = (np.hypot(px - e["pos_cm"][0] / 100.0, py - e["pos_cm"][1] / 100.0) <= e["cull_m"]).astype(int)
            alle += m
            if e["cull_m"] >= 30.0 - TOL:
                zahl += m
        if zahl.max() > gz["gleichzeitig"]:
            b.append((FEHLER, tag, "bis %d Effekte (Cull >= 30 m) gleichzeitig aktiv (> %d)" % (zahl.max(), gz["gleichzeitig"])))
        if alle.max() > NIAGARA["gleichzeitig_hart"]:
            b.append((FEHLER, tag, "bis %d Effekte insgesamt gleichzeitig aktiv (> %d)" % (alle.max(), NIAGARA["gleichzeitig_hart"])))


def pruefe_kameras(p, b, tag):
    namen = set()
    for k in p.get("kameras") or []:
        if len(k) != 8 or not isinstance(k[6], str):
            b.append((FEHLER, tag, "Kamera %r: 8 Felder [Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch]" % (k,)))
            continue
        namen.add(k[6])
        if k[7] != -170:
            b.append((FEHLER, tag, "Kamera %s: Hoch %s (Augenhoehe -170)" % (k[6], k[7])))
        if math.hypot(k[1] - k[3], k[2] - k[4]) < 300:
            b.append((WARNUNG, tag, "Kamera %s: < 3 m vom Ziel" % k[6]))
    for n in namen:
        if n.endswith("_vorher") and n[:-7] + "_nachher" not in namen:
            b.append((FEHLER, tag, "Kamera %s ohne _nachher" % n))
    for st in p.get("strecken") or []:
        if st.get("pilot") and st.get("stufen") and not any(n.startswith(st["id"] + "_") and n.endswith("_vorher")
                                                            for n in namen):
            b.append((WARNUNG, tag, "Pilot-Strecke %s ohne Kamera _vorher/_nachher" % st["id"]))


def _lagen_summe(p, ordner):
    """Alle Lagen aller Abschnitte als Liste (fenster_ij, Summe 0..255*n)."""
    out = []
    for ab in p.get("abschnitte") or []:
        lg = ab.get("lagen")
        if not lg:
            continue
        li0, lj0, lh, lw = lg["fenster_ij"]
        s_ = np.zeros((lh, lw), np.float64)
        for n in lg["lagen"]:
            q = os.path.join(ordner, lg["datei_praefix"] + n + ".r8")
            if os.path.exists(q) and os.path.getsize(q) == lh * lw:
                s_ += np.fromfile(q, dtype=np.uint8).reshape(lh, lw)
        out.append(((li0, lj0, lh, lw), s_))
    return out


def _erlaubte_zone(p, X, Y):
    """15e: Abstand d zur neuen Wasserlinie und erlaubte Breite je Zelle: halbe Breite + Netzrand 0,4 + Uferring 1,5
    + Boeschung fuer die Eintiefung ((alter - neuer Spiegel + 0,5 m) / tan 35 deg) + 2 m Reserve; dazu die
    Zufluss-Endstuecke (Breite/2 + 4 m). Klamm/Wandzonen stecken in der Breite."""
    from gefaelle_plan import KN, RING, BOESCHUNG_GRAD
    from sehens_lib import stempel as stm
    N = np.asarray(p["spiegel_neu_cm"], np.float64)
    P = N[:, :2] / 100.0
    s_neu = np.asarray(p["spiegel_neu_s_m"], np.float64)
    cum = _s_entlang(p["spiegel_neu_cm"])
    d, s_p, _ = stm.polylinie_abstand(X, Y, P)
    s = np.interp(s_p, cum, s_neu)
    half = np.interp(s, s_neu, N[:, 3] / 200.0)
    A = np.asarray(p["spiegel_alt_cm"], np.float64)
    s_alt = _s_entlang(p["spiegel_alt_cm"])
    z_alt = np.minimum.accumulate(A[:, 2]) / 100.0
    eint = np.maximum(np.interp(s, s_alt, z_alt) - np.interp(s, s_neu, N[:, 2] / 100.0), 0.0)
    # Eintiefung im Umkreis +-3 m (Fallkanten) als Maximum
    # 15f: schraege Lippen verschieben den Absturz seitlich um bis zu ~0,6 x halbe Breite -> Fenster mitwachsen lassen
    fen = 3.0 + 0.6 * half
    eint = np.maximum.reduce([np.maximum(np.interp(s + f_ * fen, s_alt, z_alt) - np.interp(s + f_ * fen, s_neu,
                                                                                         N[:, 2] / 100.0), 0.0)
                              for f_ in np.linspace(-1.0, 1.0, 9)])
    breite = half + KN["rand_ueberstand_m"] + RING["breite_m"] + (eint + RING["abtrag_zuschlag_m"]) / np.tan(
        np.radians(BOESCHUNG_GRAD)) + 2.0                   # 2 m Reserve: 1-m-Raster und Kruemmung (Projektion)
    ok = d <= breite
    for z_ in p.get("zufluesse") or []:
        T_ = np.asarray(z_["punkte_neu_cm"], np.float64)
        if len(T_) >= 2:
            dz, _, _ = stm.polylinie_abstand(X, Y, T_[:, :2] / 100.0)
            ok |= dz <= T_[0, 3] / 200.0 + 4.0
    return ok, d


def pruefe_gelaende(p, ordner, welt, orte, b, tag):
    from sehens_lib import gelaende as gel_mod
    lagen_alle = _lagen_summe(p, ordner)
    for ab in p.get("abschnitte") or []:
        g = ab.get("gelaende")
        if not g:
            b.append((HINWEIS, ab["id"], "kein Gelaendestempel"))
            continue
        i0, j0, hh, ww = g["fenster_ij"]
        pf = os.path.join(ordner, g["datei"])
        if not os.path.exists(pf) or os.path.getsize(pf) != hh * ww * 4:
            b.append((FEHLER, ab["id"], "Gelaende-Datei fehlt oder falsche Groesse: %s" % g["datei"]))
            continue
        a = np.fromfile(pf, dtype="<f4").reshape(hh, ww)
        if not np.isfinite(a).all():
            b.append((FEHLER, ab["id"], "Gelaende: NaN/Inf"))
        rand = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
        if np.abs(rand).max() > 1e-4:
            b.append((FEHLER, ab["id"], "Gelaende: Rand nicht 0 (%.3f m)" % np.abs(rand).max()))
        if np.abs(a).max() > 40.0 and not g.get("begruendung"):
            b.append((WARNUNG, ab["id"], "|Delta| %.1f m > 40 m ohne Begruendung" % np.abs(a).max()))
        if max(hh, ww) > 600:
            b.append((WARNUNG, ab["id"], "Fenster %d x %d m > 600 m" % (hh, ww)))
        if a.max() > 1.0:
            b.append((WARNUNG, ab["id"], "Gelaende wird um %.2f m angehoben (Uferwulst soll < 1 m bleiben)" % a.max()))
        lg = ab.get("lagen")
        if lg:
            li0, lj0, lh, lw = lg["fenster_ij"]
            for n in lg["lagen"]:
                q = os.path.join(ordner, lg["datei_praefix"] + n + ".r8")
                if not os.path.exists(q) or os.path.getsize(q) != lh * lw:
                    b.append((FEHLER, ab["id"], "Lagen-Datei fehlt/falsch: %s" % n))
        # 15e: |Delta| > 0,3 m nur am Bach (Netzrand + Uferring + Boeschung der Eintiefung) und nie ohne Lage
        stark = np.abs(a) > 0.3
        if stark.any() and p.get("spiegel_neu_cm"):
            ii_, jj_ = np.nonzero(stark)
            Xs, Ys = (jj_ + j0) - 4730.5, (ii_ + i0) - 4060.5
            ok, d_ = _erlaubte_zone(p, Xs, Ys)
            if (~ok).any():
                b.append((FEHLER, ab["id"], "Gelaende aendert sich um > 0,3 m abseits des Bachs: %d m2, Delta bis %+.1f m, "
                          "%.0f m von der Wasserlinie (erlaubt: Netzrand + Uferring + Boeschung der Eintiefung)"
                          % (int((~ok).sum()), float(a[stark][~ok][np.argmax(np.abs(a[stark][~ok]))]),
                             float(d_[~ok].max()))))
            gi, gj = ii_ + i0, jj_ + j0
            hat = np.zeros(len(gi), bool)
            for (li0, lj0, lh, lw), s_ in lagen_alle:
                inn = (gi >= li0) & (gi < li0 + lh) & (gj >= lj0) & (gj < lj0 + lw)
                hat[inn] |= s_[gi[inn] - li0, gj[inn] - lj0] > 0
            if (~hat).any():
                b.append((FEHLER, ab["id"], "%d Zellen mit |Delta| > 0,3 m ohne Lagenzuweisung (z. B. X %.0f Y %.0f)"
                          % (int((~hat).sum()), float(Xs[~hat][0]), float(Ys[~hat][0]))))
        if welt is None:
            continue
        z = welt.zelle_m
        ii = np.clip((np.arange(i0, i0 + hh) // int(z)).astype(np.int64), 0, welt.ny - 1)
        jj = np.clip((np.arange(j0, j0 + ww) // int(z)).astype(np.int64), 0, welt.nx - 1)
        geaendert = np.abs(a) > 0.05
        if not geaendert.any():
            continue
        for name, m, grenze, stufe in (("Weg/Pfad", welt.weg[ii][:, jj] > 0, 2.0, FEHLER),
                                       ("Ort", welt.ort[ii][:, jj] > 0, 5.0, FEHLER)):
            if m.any():
                d = gel_mod.abstand(m, 1.0, 10.0)
                n = int((geaendert & (d <= grenze)).sum())
                if n:
                    b.append((stufe, ab["id"], "Gelaende aendert sich %d m2 naeher als %.0f m an %s" % (n, grenze, name)))
        Y = (np.arange(i0, i0 + hh) - 4060.5)[:, None]
        X = (np.arange(j0, j0 + ww) - 4730.5)[None, :]
        for o in orte:
            if abs(o["x_m"] - X.mean()) > ww + o["radius_m"] or abs(o["y_m"] - Y.mean()) > hh + o["radius_m"]:
                continue
            m = np.hypot(X - o["x_m"], Y - o["y_m"]) <= o["radius_m"]
            n = int((geaendert & m).sum())
            if n:
                b.append((FEHLER, ab["id"], "Gelaende aendert sich %d m2 in Sehenswuerdigkeit %s" % (n, o["id"])))


def akteure_s(p, ebene):
    """Laufkoordinate s (m, wie spiegel_neu_s_m) und Netz aller Akteure eines Laufs: Projektion auf die neue
    Wasserlinie."""
    sp = np.asarray(p.get("spiegel_neu_cm") or [], np.float64)
    if len(sp) < 2:
        return [], []
    P = sp[:, :2] / 100.0
    s_l = np.asarray(p.get("spiegel_neu_s_m") or _s_entlang(sp), np.float64)
    A = P[:-1]
    D = P[1:] - A
    L2 = np.maximum((D ** 2).sum(1), 1e-12)
    s_out, netze = [], []
    for _, (plan, _arr) in sorted(ebene.items()):
        for e in plan.get("akteure") or []:
            q = np.array([e["x"], e["y"]], np.float64) / 100.0
            t = np.clip(((q - A) * D).sum(1) / L2, 0.0, 1.0)
            d2 = ((A + D * t[:, None] - q) ** 2).sum(1)
            k = int(np.argmin(d2))
            s_out.append(float(s_l[k] + t[k] * (s_l[k + 1] - s_l[k])))
            netze.append(e.get("netz"))
    return s_out, netze


def pruefe_akteure_lauf(p, ebene, b, tag):
    """13k-Rueckfrage 6 (Koordinator): hoechstens 50 Akteure je 200 m Lauflaenge (gleitendes Fenster; eine
    Back-Kachel ist <= 128 m lang und liegt damit in einem Fenster). FEHLER darueber."""
    from sehens_lib import instanzen as ins
    s_a, _ = akteure_s(p, ebene)
    n, s0 = ins.akteure_je_fenster(s_a, ins.AKTEURE_GEFAELLE_FENSTER_M)
    if n > ins.AKTEURE_GEFAELLE_MAX:
        b.append((FEHLER, tag, "%d Akteure in %.0f m Lauflaenge ab s = %.1f m > %d (13k-Rueckfrage 6: wiederholte "
                  "Module als Instanzen)" % (n, ins.AKTEURE_GEFAELLE_FENSTER_M, s0, ins.AKTEURE_GEFAELLE_MAX)))
    elif n > 0.8 * ins.AKTEURE_GEFAELLE_MAX:
        b.append((HINWEIS, tag, "Akteure: %d gesamt, hoechstens %d je %.0f m Lauflaenge (nahe Grenze %d)"
                  % (len(s_a), n, ins.AKTEURE_GEFAELLE_FENSTER_M, ins.AKTEURE_GEFAELLE_MAX)))


def pruefe_instanzen(p, ordner, welt, inv, b, tag):
    from sehens_lib import sehens_pruefen as sp_
    from sehens_lib import instanzen as ins
    io = os.path.join(ordner, (p.get("instanzen") or {}).get("ordner", "instanzen"))
    if not os.path.isdir(io):
        if (p.get("instanzen") or {}).get("anzahl", 0) or p.get("akteure"):
            b.append((FEHLER, tag, "Instanz-Ordner fehlt"))
        return
    orte = [{"id": a["id"], "gelaende": a.get("gelaende"), "budget": a.get("budget")} for a in p.get("abschnitte") or []]
    # Kontext 'gefaelle': die 13k-Grenze "50 Akteure je Sehens-Ort" gilt hier nicht je Abschnitt, sondern je 200 m
    # Lauflaenge (pruefe_akteure_lauf); alle anderen Ebenen-Regeln (auch Saegeschnitt) wie in Sehens
    for st, oid, t in sp_.pruefe_ebene(io, "gefaelle", inv=inv, orte=orte, welt=welt, basis=ordner, kontext="gefaelle"):
        if "nicht in orte.json" in t:
            st = FEHLER
        b.append((st, oid, t.replace("orte.json", "plan.json abschnitte")))
    ebene = ins.lies_ebene(io)
    pruefe_akteure_lauf(p, ebene, b, tag)
    if welt is None:
        return
    n_ort = 0
    for feld, (plan, arr) in ebene.items():
        for a in arr.values():
            if a.ndim == 2 and len(a):
                i, j = welt.m_zu_ij(a[:, 0] / 100.0, a[:, 1] / 100.0)
                n_ort += int((welt.ort[i, j] > 0).sum())
        for e in plan.get("akteure") or []:
            i, j = welt.m_zu_ij(e["x"] / 100.0, e["y"] / 100.0)
            n_ort += int(welt.ort[i, j] > 0)
    if n_ort:
        b.append((FEHLER, tag, "%d Instanzen/Akteure auf Ortsflaechen" % n_ort))


def bachbett_stufen_aus_plan(p, rw):
    """Lippen (auch Teil-Lippen) aus plan.json fuer sehens_lib.bachbett.lippen_zonen - wie gefaelle_plan.bachbett_stufen
    (s_lippe, s_fuss = s + Zwei-Punkt-Abstand bzw. Rampe, Fall, gross >= 1 m oder Vorhang, Lippenform aus lippe_form)."""
    zp = rw.zwei_punkte()[0]
    out = []
    for st in p.get("stufen") or []:
        teile = st.get("teilstufen") or [{"s_m": st["s_m"], "fall_m": st["fall_m"], "rampe": "rampe_m" in st,
                                          "rampe_m": st.get("rampe_m"), "lippe_form": st.get("lippe_form")}]
        for t in teile:
            g = t.get("lippe_form") or {}
            l_ = float(t["rampe_m"]) if t.get("rampe") and t.get("rampe_m") is not None else zp
            d = {"s_lippe": float(t["s_m"]), "s_fuss": float(t["s_m"]) + l_, "fall": float(t["fall_m"]),
                 "gross": bool(float(t["fall_m"]) >= 1.0 or (not st.get("teilstufen") and st.get("vorhang"))),
                 "halb": float(st["lippe_breite_cm"]) / 200.0}
            if g:
                d.update(tan=math.tan(math.radians(float(g["winkel_grad"]))), pfeil=float(g["pfeil_m"]),
                         h=max(float(st["breite_m"]) / 2.0, 0.5))
            out.append(d)
    return out


def _ebene_index(io):
    """Instanz-Ebene -> Liste (netz, kollision, x, y, z, q, s) aller Instanzen (fuer den Abgleich der Bachbett-Liste)."""
    from sehens_lib import instanzen as ins
    out = []
    for feld, (plan, arr) in ins.lies_ebene(io).items():
        for key, a in arr.items():
            if a.ndim != 2 or not len(a):
                continue
            info = (plan.get("dateien") or {}).get(key, {})
            netz = key.split("__")[0]
            kol = bool(info.get("kollision", netz.endswith("_kol")))
            if netz.endswith("_kol"):
                netz = netz[:-4]
            for r in a:
                out.append((netz, kol, float(r[0]), float(r[1]), float(r[2]), tuple(float(v) for v in r[3:7]),
                            tuple(float(v) for v in r[7:10]), info.get("pfad")))
    return out


def pruefe_bachbett(p, ordner, welt, inv, rw, b, tag, h1m=None):
    """16c Nachtrag 18:15 (Ferat: Felsen, Totholz, Schlamm in jedes Bachbett), Regeln sehens_lib/bachbett_regeln.json:
    - plan.json 'bachbett' vorhanden; jedes gelistete Stueck steht so in der Instanz-Ebene (Lage +-2 cm, Netz);
    - grosses Totholz (Staemme, Verklausung, ueberspannt, Wurzelstock) im Wasser bzw. <= 1 m daneben mit Kollision
      (Datei <netz>_kol -> fluss_sim-Export: Wasser-Kollision);
    - kein Totholz-Stueck mit der Achse mitten in einer Lippe bzw. einem Vorhang (Lippenzonen, schraeger Versatz aus
      lippe_form);
    - Dichte grosses Totholz je Segment im Rahmen des Bioms x Waldfaktor (FEHLER ueber max, unter min ab 60 m);
    - Uferstreifen: Zellen 0,05-0,5 m ueber dem Spiegel bis 1,5 m neben dem Netzrand (ausserhalb der Lippenzonen) zu
      >= 80 % mit Streifen-Lagen (Schlamm/Erde/Moos je Biom) >= 200."""
    from sehens_lib import bachbett as bb
    R = bb.regeln()
    A = R.a
    blk = p.get("bachbett")
    if not blk or "abschnitte" not in blk:
        b.append((FEHLER, tag, "plan.json: 'bachbett' fehlt (16c Nachtrag 18:15: Totholz, Schlamm, Uferstreifen)"))
        return
    stufen = bachbett_stufen_aus_plan(p, rw)
    zonen = bb.lippen_zonen(stufen, R)
    zonen_voll = bb.lippen_zonen([dict(st, halb=1e9) for st in stufen], R, zuschlag=1.0)
    lfeld = bb.Lippenfeld(stufen, [tuple(sg) for x_ in p.get("strecken") or [] for sg in x_.get("segmente_m") or []])
    N = np.asarray(p["spiegel_neu_cm"], np.float64)
    P = N[:, :2] / 100.0
    s_neu = np.asarray(p["spiegel_neu_s_m"], np.float64)
    cum = _s_entlang(p["spiegel_neu_cm"])

    def proj(x, y):
        d, s_p, u = bb.projektion_schnell(x, y, P, 1024)
        return d, np.interp(s_p, cum, s_neu), u
    io = os.path.join(ordner, (p.get("instanzen") or {}).get("ordner", "instanzen"))
    idx = _ebene_index(io) if os.path.isdir(io) else []
    from collections import defaultdict
    je_netz = defaultdict(list)
    for r in idx:
        je_netz[r[0]].append(r)
    ab_by_id = {a["id"]: a for a in p.get("abschnitte") or []}
    for aid, ab in sorted(blk["abschnitte"].items()):
        stuecke = ab.get("stuecke") or []
        ok_st = []
        n_fehlt = 0
        for st in stuecke:
            kand = [r for r in je_netz.get(st["netz"], []) if abs(r[2] - st["pos_cm"][0]) <= 2.0 and
                    abs(r[3] - st["pos_cm"][1]) <= 2.0 and abs(r[4] - st["pos_cm"][2]) <= 2.0]
            if not kand:
                n_fehlt += 1
                continue
            ok_st.append((st, kand[0]))
        if n_fehlt:
            b.append((FEHLER, aid, "Bachbett: %d von %d gelisteten Totholz-Stuecken nicht in der Instanz-Ebene"
                      % (n_fehlt, len(stuecke))))
        n_lippe, n_kol, lippe_bsp = 0, 0, ""
        for st, r in ok_st:
            pfad = r[7] or st["pfad"]
            (x0, y0, x1, y1), (cx, cy), L = bb.achse_enden(inv, pfad, r[5], r[6], (r[2], r[3]))
            t = np.linspace(0.0, 1.0, 9)
            d, s, u = proj(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
            if bb.in_zonen(s, zonen, u).any():
                n_lippe += 1
                lippe_bsp = lippe_bsp or "%s (s %.1f m)" % (st["gruppe"], float(np.median(s)))
            if st["art"] in bb.ARTEN_LW:
                dc, sc, uc = proj([cx], [cy])
                halb = float(np.interp(sc[0], s_neu, N[:, 3] / 200.0))
                if dc[0] <= halb + float(A["kollision_ufer_m"]) and not r[1]:
                    n_kol += 1
        if n_lippe:
            b.append((FEHLER, aid, "Bachbett: %d Totholz-Stuecke mitten in einer Lippe/einem Vorhang, z. B. %s"
                      % (n_lippe, lippe_bsp)))
        if n_kol:
            b.append((FEHLER, aid, "Bachbett: %d grosse Totholz-Stuecke im Wasser bzw. <= 1 m daneben ohne Kollision "
                      "(fluss_sim-Export erkennt sie nicht als Wasser-Kollision)" % n_kol))
        # Dichte je Segment
        best = ab.get("bestand") or []
        for seg in ab.get("dichte") or []:
            a_, b_ = seg["s_m"]
            L = float(seg["laenge_m"])
            n_neu = sum(1 for st, _ in ok_st if st["art"] in bb.ARTEN_LW and a_ - 1.0 <= st["s_m"] <= b_ + 1.0)
            n_best = sum(1 for st in best if a_ - 1.0 <= st["s_m"] <= b_ + 1.0)
            f = float(seg.get("wald_faktor", 1.0))
            rahmen = None
            if welt is not None and L >= float(A["min_laenge_m"]):
                ss_ = np.linspace(a_, b_, max(2, int(L / 2.0) + 1))
                pts = np.stack([np.interp(ss_, s_neu, N[:, 0] / 100.0), np.interp(ss_, s_neu, N[:, 1] / 100.0)], 1)
                # 16c Nachtrag 3: Rahmen nach Waldnaehe (Ufer-Wald in jedem Biom, Treibholz vom Oberlauf)
                ober = bb.oberlauf_punkte(s_neu, N[:, 0] / 100.0, N[:, 1] / 100.0, a_,
                                                float(A["treibholz"]["oberlauf_m"]))
                rahmen = bb.dichte(welt, pts, seg["biom"], R, ober)
                for bf in bb.rahmen_vergleichen(seg, rahmen, aid, FEHLER):
                    b.append(bf)
                bi = [welt.biom_bei_m(float(x_), float(y_)) for x_, y_ in pts[::max(1, len(pts) // 7)]]
                maj = max(set(bi), key=lambda v: (bi.count(v), v))
                if R.biom(maj)[0] != seg["biom"]:
                    b.append((WARNUNG, aid, "Bachbett: Segment %.0f-%.0f m als %s geplant, Weltbiom ueberwiegend %s"
                              % (a_, b_, seg["biom"], maj)))
            stf, txt = bb.dichte_bewerten(seg["biom"], f, L, n_neu + n_best, int(seg.get("blockiert", 0)), R, n_neu,
                                          rahmen=rahmen)
            if stf:
                b.append((stf, aid, "Bachbett-Dichte " + txt))
        # Uferstreifen
        a_lg = ab_by_id.get(aid, {}).get("lagen")
        a_ge = ab_by_id.get(aid, {}).get("gelaende")
        if welt is None or not a_lg or not ab.get("dichte"):
            continue
        li0, lj0, lh, lw = [int(v) for v in a_lg["fenster_ij"]]
        from gefaelle_plan import alt_1m
        F = alt_1m({"welt": welt, "h1m": h1m}, [li0, lj0, lh, lw]).copy()
        if a_ge:
            gi0, gj0, gh, gw = [int(v) for v in a_ge["fenster_ij"]]
            pf = os.path.join(ordner, a_ge["datei"])
            if os.path.exists(pf) and os.path.getsize(pf) == gh * gw * 4:
                dl = np.fromfile(pf, dtype="<f4").reshape(gh, gw)
                i_a, i_b = max(gi0, li0), min(gi0 + gh, li0 + lh)
                j_a, j_b = max(gj0, lj0), min(gj0 + gw, lj0 + lw)
                if i_b > i_a and j_b > j_a:
                    F[i_a - li0:i_b - li0, j_a - lj0:j_b - lj0] += dl[i_a - gi0:i_b - gi0, j_a - gj0:j_b - gj0]
        jj, ii = np.meshgrid(np.arange(lj0, lj0 + lw, dtype=np.float64), np.arange(li0, li0 + lh, dtype=np.float64))
        X, Y = jj - gd.OFF_J_1M, ii - gd.OFF_I_1M
        for seg in ab["dichte"]:
            a_, b_ = seg["s_m"]
            _, Rb = R.biom(seg["biom"])
            hb = float(np.max(N[:, 3])) / 200.0 + 4.0
            sx = np.interp(np.linspace(a_, b_, 20), s_neu, N[:, 0] / 100.0)
            sy = np.interp(np.linspace(a_, b_, 20), s_neu, N[:, 1] / 100.0)
            box = (X >= sx.min() - hb) & (X <= sx.max() + hb) & (Y >= sy.min() - hb) & (Y <= sy.max() + hb)
            if not box.any():
                continue
            d, s, u = proj(X[box], Y[box])
            halb = np.interp(s, s_neu, N[:, 3] / 200.0)
            z_sp = np.interp(lfeld.s_eff(s, u), s_neu, N[:, 2] / 100.0)      # Spiegel an schraegen Lippen (15f)
            ok = (s >= a_ + 1.0) & (s <= b_ - 1.0) & ~bb.in_zonen(s, zonen_voll, u)
            summe = np.zeros(int(box.sum()))
            for n in Rb["streifen"]:
                if n in a_lg["lagen"]:
                    q = os.path.join(ordner, a_lg["datei_praefix"] + n + ".r8")
                    if os.path.exists(q) and os.path.getsize(q) == lh * lw:
                        summe += np.fromfile(q, dtype=np.uint8).reshape(lh, lw)[box]
            n_z, anteil = bb.streifen_bewerten(F[box] - z_sp, d, halb, ok, summe, R)
            if n_z >= 20 and anteil < float(A["streifen_anteil_min"]):
                b.append((FEHLER, aid, "Uferstreifen %s %.0f-%.0f m: nur %.0f %% von %d Uferzellen (0,05-0,5 m ueber "
                          "dem Spiegel) mit %s >= 200 (Regel >= %.0f %%)" % (seg["biom"], a_, b_, 100 * anteil, n_z,
                                                                          "/".join(Rb["streifen"]),
                                                                          100 * float(A["streifen_anteil_min"]))))
            elif n_z:
                b.append((HINWEIS, aid, "Uferstreifen %s %.0f-%.0f m: %.0f %% von %d Uferzellen belegt"
                          % (seg["biom"], a_, b_, 100 * anteil, n_z)))


_LAEUFE = {}


def pruefe_feldgrenzen(p, welt, b, tag):
    """16c Nachtrag 3 (Feldgrenzen mit zwei Plaenen): 'feldgrenzen' im Plan; keine Lippe (auch Teil-Lippe) in einer
    Ueberlappung, die dem Nachbarplan gehoert (FEHLER). Mit Weltdaten wird die Ueberlappung nachgerechnet."""
    blk = p.get("feldgrenzen")
    if blk is None:
        b.append((FEHLER, tag, "plan.json: 'feldgrenzen' fehlt (16c Nachtrag 3: Stufe nur in einem Plan)"))
        return
    liste = blk.get("ueberlappungen") or []
    if welt is not None:
        key = id(welt)
        if key not in _LAEUFE:
            _LAEUFE.clear()
            _LAEUFE[key] = gd.alle_laeufe(welt)
        if p["lauf"] in _LAEUFE[key]:
            neu = {(e["nachbar"], e["seite"]): e for e in gd.feldgrenzen(p["lauf"], _LAEUFE[key])}
            for e in liste:
                n = neu.get((e["nachbar"], e["seite"]))
                if n is None or (n["fremd_s_m"] or [0, 0]) != (e["fremd_s_m"] or [0, 0]):
                    b.append((FEHLER, tag, "Feldgrenze %s (%s): fremd_s_m im Plan %s, nachgerechnet %s"
                              % (e["nachbar"], e["seite"], e["fremd_s_m"], n and n["fremd_s_m"])))
            if len(neu) != len(liste):
                b.append((FEHLER, tag, "Feldgrenzen: %d Ueberlappungen im Plan, nachgerechnet %d" % (len(liste), len(neu))))
    lip = []
    for st in p.get("stufen") or []:
        for t in st.get("teilstufen") or [st]:
            lip.append((st["id"], float(t["s_m"])))
    for e in liste:
        fz = e.get("fremd_s_m")
        if not fz or not e.get("nachbar_plan"):
            continue
        drin = [sid for sid, s_ in lip if fz[0] - 1e-3 <= s_ <= fz[1] + 1e-3]
        segs = [sg for x_ in p.get("strecken") or [] for sg in x_.get("segmente_m") or []]
        seg_in = [sg for sg in segs if sg[1] > fz[0] + 0.05 and sg[0] < fz[1] - 0.05]
        if seg_in:
            b.append((FEHLER, tag, "Feldgrenze %s: Stufenstrecke %s reicht in die Ueberlappung %.1f-%.1f m (Spiegel dort "
                      "nicht alt, kein passender Anschluss)" % (e["nachbar"], seg_in[0], fz[0], fz[1])))
        if drin:
            b.append((FEHLER, tag, "Feldgrenze %s: %d Lippen in der Ueberlappung %.1f-%.1f m, die dem Plan %s gehoert (%s)"
                      % (e["nachbar"], len(drin), fz[0], fz[1], e["nachbar"], ", ".join(sorted(set(drin))[:3]))))
        else:
            b.append((HINWEIS, tag, "Feldgrenze %s (%s): Ueberlappung %.1f-%.1f m gehoert dem Nachbarplan, keine Lippe dort"
                      % (e["nachbar"], e["seite"], fz[0], fz[1])))
    for nl in blk.get("neu_gelegt") or []:
        b.append((HINWEIS, tag, "Feldgrenze: Strecke %s neu gelegt, %d Lippen bei s %s m lagen in %s (jetzt beim "
                                "Nachbarplan bzw. entfallen)" % (nl["strecke"], len(nl["lippen_vorher_s_m"]),
                                                                  nl["lippen_vorher_s_m"], nl["fremd_s_m"])))


def pruefe_lauf(ordner, welt=None, inv=None, rw=None, gel=None, orte=None, h1m=None):
    pj = os.path.join(ordner, "plan.json")
    tag = os.path.basename(os.path.normpath(ordner))
    b = []
    if not os.path.exists(pj):
        return [(FEHLER, tag, "plan.json fehlt")]
    with open(pj, "r", encoding="utf-8") as f:
        p = json.load(f)
    rw = rw or gr.Regelwerk.lade()
    for k in ("lauf", "stufen", "spiegel_neu_cm", "wasser_koerper", "abschnitte", "effekte", "kameras", "instanzen"):
        if k not in p:
            b.append((FEHLER, tag, "plan.json: %s fehlt" % k))
    if not p.get("stufen"):
        b.append((HINWEIS, tag, p.get("hinweis", "keine Stufen")))
        return b
    pruefe_spiegel(p, rw, b, tag)
    pruefe_stufen(p, rw, b, tag)
    pruefe_regelmaessigkeit(p, b, tag)
    pruefe_wasser(p, ordner, welt, b, tag, h1m)
    pruefe_effekte(p, rw, inv, b, tag)
    pruefe_kameras(p, b, tag)
    pruefe_gelaende(p, ordner, welt, orte if orte is not None else gd.sehens_orte(), b, tag)
    pruefe_instanzen(p, ordner, welt, inv, b, tag)
    if inv is not None:
        pruefe_bachbett(p, ordner, welt, inv, rw, b, tag, h1m)
    pruefe_feldgrenzen(p, welt, b, tag)
    for m in p.get("meldungen") or []:
        if m["stufe"] == FEHLER:
            b.append((FEHLER, tag, "Planer: %s" % m["text"]))
    return b


def melde(befunde, titel=""):
    from sehens_lib import ascii_text
    z = {FEHLER: 0, WARNUNG: 0, HINWEIS: 0}
    for st, _, _ in befunde:
        z[st] += 1
    sys.stdout.write("[gefaelle_pruefen] %s: %d FEHLER, %d WARNUNG, %d HINWEIS\n" % (titel, z[FEHLER], z[WARNUNG], z[HINWEIS]))
    for st in (FEHLER, WARNUNG, HINWEIS):
        for s, oid, t in befunde:
            if s == st:
                sys.stdout.write("  %-7s %-26s %s\n" % (s, ascii_text(str(oid))[:26], ascii_text(t)))
    sys.stdout.flush()
    return z


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pruefer Auftrag 15 (gefaelle_plan.py-Ausgaben)")
    ap.add_argument("ordner", nargs="+")
    ap.add_argument("--regeln", default=gr.REGELN_STANDARD)
    ap.add_argument("--ohne-daten", action="store_true")
    ap.add_argument("--sehens", default=gd.SEHENS_STANDARD)
    ap.add_argument("--hoehe1m-fenster", default=None, metavar="DIR",
                    help="1-m-Hoehenfenster (15b): Bett-/Uferpruefung exakt auf 1 m (altes Gelaende + 1-m-Delta)")
    from sehens_lib import daten, inventar
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    rw = gr.Regelwerk.lade(a.regeln)
    inv = inventar.Inventar.lade()
    welt = None
    if not a.ohne_daten:
        welt = daten.lade(a.daten2m or (None if a.daten1m else gd.DATEN2M_STANDARD), a.daten1m, pfade=a.sehens)
    orte = gd.sehens_orte(a.sehens)
    h1m = None
    if a.hoehe1m_fenster and welt is not None:
        h1m = gd.Hoehe1m(a.hoehe1m_fenster, lambda x_, y_: welt.bilinear(welt.hoehe, x_, y_))
    laeufe = []
    for o in a.ordner:
        if os.path.exists(os.path.join(o, "plan.json")):
            laeufe.append(o)
        else:
            laeufe += sorted(os.path.join(o, d) for d in os.listdir(o) if os.path.exists(os.path.join(o, d, "plan.json")))
    gesamt = {FEHLER: 0, WARNUNG: 0, HINWEIS: 0}
    for o in laeufe:
        z = melde(pruefe_lauf(o, welt=welt, inv=inv, rw=rw, orte=orte, h1m=h1m), os.path.basename(o))
        for k in gesamt:
            gesamt[k] += z[k]
    sys.stdout.write("[gefaelle_pruefen] GESAMT %d Laeufe: %d FEHLER, %d WARNUNG, %d HINWEIS\n"
                     % (len(laeufe), gesamt[FEHLER], gesamt[WARNUNG], gesamt[HINWEIS]))
    return 1 if gesamt[FEHLER] else 0


if __name__ == "__main__":
    sys.exit(main())
