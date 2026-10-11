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
  Assets    Netze (Instanz-Ebene + Akteure) in netze.csv, nicht gesperrt; Niagara in inventar_extra.json.
  Budget    je Abschnitt <= SEHENS_FORMAT §9 (sehens_pruefen.pruefe_ebene), Effekte <= 3 je Stufe, <= 6 gleichzeitig
            (Proben alle 2 m entlang des Spiegels, Cull-Radius), Cull 30-150 m; je Feld <= 60 000.
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


def pruefe_wasser(p, ordner, welt, b, tag):
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
    if len(rv) > 1:
        ue = ueberlappungen([{"punkte": w["punkte"]} for w in rv])
        if ue:
            b.append((FEHLER, tag, "River-Abschnitte ueberlappen in der Draufsicht: %s" % ue[:5]))
    kn = [w for w in wk if w["typ"] == "kaskadennetz"]
    for e in p.get("stufen") or []:
        if not any(w["s_m"][0] - 1e-3 <= e["s_m"] <= w["s_m"][1] + 1e-3 for w in kn):
            b.append((FEHLER, tag, "%s liegt in keinem Kaskadennetz" % e["id"]))
    # (d) Niagara oder Vorhang je Stufe
    fx = {e["stufe"] for e in p.get("effekte") or []}
    ohne = [sid for w in kn for sid in w.get("stufen", []) if sid not in fx and sid not in (w.get("vorhang_an_stufen") or [])]
    if ohne:
        b.append((WARNUNG, tag, "%d Stufen ohne Niagara und ohne Vorhang (Grenze <= 6 gleichzeitig; Schaum nur im Netz): %s"
                  % (len(ohne), ", ".join(x_[-3:] for x_ in ohne[:12]))))
    # (a) Bett >= 0,2 m unter dem Spiegel, (b) Ufer am Netzrand >= 0,1 m ueber dem Spiegel - Gelaende NACH dem Stempel
    if welt is None:
        return
    orte = [{"id": a["id"], "gelaende": a.get("gelaende")} for a in p.get("abschnitte") or []]
    from gefaelle_plan import nahe_stufe
    boden = BodenNachStempel(welt, orte, ordner)
    for w in kn:
        M = np.asarray(w["mittellinie"], np.float64)
        kn_ = w["knick"]
        n_bett = n_ufer = n_b = 0
        nah = nahe_stufe(w["mittellinie"], kn_, max(welt.zelle_m - 1.0, 0.0))
        for k in range(len(M)):
            if kn_[k] != "becken" or nah[k]:
                continue
            n_b += 1
            if k + 1 < len(M):
                t = M[k + 1, :2] - M[k, :2]
            else:
                t = M[k, :2] - M[k - 1, :2]
            L = max(float(np.hypot(*t)), 1e-6)
            tx, ty = t / L
            x, y, zs, br = M[k, 0] / 100.0, M[k, 1] / 100.0, M[k, 2] / 100.0, M[k, 3] / 100.0
            zus = max(welt.zelle_m - 1.0, 0.0)          # 2-m-Naeherung (siehe gefaelle_plan.RASTER_ZUSCHLAG)
            off = np.linspace(-1, 1, 7) * max(0.45 * br - zus, 0.15 * br)
            bett = float(np.mean(boden.hoehe(x + ty * off, y - tx * off)))
            if zs - bett < KN["bett_unter_spiegel_min_m"] - 0.005:
                n_bett += 1
            r_ = br / 2.0 + w.get("rand_ueberstand_m", 0.4) + zus
            hz = boden.hoehe(np.array([x + ty * r_, x - ty * r_]), np.array([y - tx * r_, y + tx * r_]))
            if float(np.min(hz)) < zs + KN["ufer_ueber_spiegel_am_rand_m"] - 0.005:
                n_ufer += 1
        from gefaelle_plan import raster_stufe, raster_text
        zus = max(welt.zelle_m - 1.0, 0.0)
        if n_bett:
            b.append((raster_stufe(n_bett, n_b, zus), tag, "%s: Bett an %d von %d Beckenpunkten < 0,2 m unter dem Spiegel%s"
                      % (w["id"], n_bett, n_b, raster_text(n_bett, n_b, zus))))
        if n_ufer:
            b.append((raster_stufe(n_ufer, n_b, zus), tag, "%s: Ufer am Netzrand an %d von %d Beckenpunkten < 0,1 m ueber "
                      "dem Spiegel%s" % (w["id"], n_ufer, n_b, raster_text(n_ufer, n_b, zus))))


def pruefe_effekte(p, rw, inv, b, tag):
    ef = p.get("effekte") or []
    gz = gr.effekt_grenzen(rw)
    je = {}
    for e in ef:
        je[e["stufe"]] = je.get(e["stufe"], 0) + 1
        if inv is not None:
            for st, t in inv.asset_pruefen("niagara", e["asset"], bool(e.get("optional"))):
                b.append((st, tag, "Effekt %s: %s" % (e["stufe"], t)))
        if not (gz["cull_klein"] - TOL <= e["cull_m"] <= max(gz["cull_held"]) + TOL):
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
        for e in ef:
            zahl += (np.hypot(px - e["pos_cm"][0] / 100.0, py - e["pos_cm"][1] / 100.0) <= e["cull_m"]).astype(int)
        if zahl.max() > gz["gleichzeitig"]:
            b.append((FEHLER, tag, "bis %d Effekte gleichzeitig aktiv (> %d)" % (zahl.max(), gz["gleichzeitig"])))


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


def pruefe_gelaende(p, ordner, welt, orte, b, tag):
    from sehens_lib import gelaende as gel_mod
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


def pruefe_instanzen(p, ordner, welt, inv, b, tag):
    from sehens_lib import sehens_pruefen as sp_
    from sehens_lib import instanzen as ins
    io = os.path.join(ordner, (p.get("instanzen") or {}).get("ordner", "instanzen"))
    if not os.path.isdir(io):
        if (p.get("instanzen") or {}).get("anzahl", 0) or p.get("akteure"):
            b.append((FEHLER, tag, "Instanz-Ordner fehlt"))
        return
    orte = [{"id": a["id"], "gelaende": a.get("gelaende"), "budget": a.get("budget")} for a in p.get("abschnitte") or []]
    for st, oid, t in sp_.pruefe_ebene(io, "gefaelle", inv=inv, orte=orte, welt=welt, basis=ordner):
        if "nicht in orte.json" in t:
            st = FEHLER
        b.append((st, oid, t.replace("orte.json", "plan.json abschnitte")))
    if welt is None:
        return
    n_ort = 0
    for feld, (plan, arr) in ins.lies_ebene(io).items():
        for a in arr.values():
            if a.ndim == 2 and len(a):
                i, j = welt.m_zu_ij(a[:, 0] / 100.0, a[:, 1] / 100.0)
                n_ort += int((welt.ort[i, j] > 0).sum())
        for e in plan.get("akteure") or []:
            i, j = welt.m_zu_ij(e["x"] / 100.0, e["y"] / 100.0)
            n_ort += int(welt.ort[i, j] > 0)
    if n_ort:
        b.append((FEHLER, tag, "%d Instanzen/Akteure auf Ortsflaechen" % n_ort))


def pruefe_lauf(ordner, welt=None, inv=None, rw=None, gel=None, orte=None):
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
    pruefe_wasser(p, ordner, welt, b, tag)
    pruefe_effekte(p, rw, inv, b, tag)
    pruefe_kameras(p, b, tag)
    pruefe_gelaende(p, ordner, welt, orte if orte is not None else gd.sehens_orte(), b, tag)
    pruefe_instanzen(p, ordner, welt, inv, b, tag)
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
    from sehens_lib import daten, inventar
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    rw = gr.Regelwerk.lade(a.regeln)
    inv = inventar.Inventar.lade()
    welt = None
    if not a.ohne_daten:
        welt = daten.lade(a.daten2m or (None if a.daten1m else gd.DATEN2M_STANDARD), a.daten1m, pfade=a.sehens)
    orte = gd.sehens_orte(a.sehens)
    laeufe = []
    for o in a.ordner:
        if os.path.exists(os.path.join(o, "plan.json")):
            laeufe.append(o)
        else:
            laeufe += sorted(os.path.join(o, d) for d in os.listdir(o) if os.path.exists(os.path.join(o, d, "plan.json")))
    gesamt = {FEHLER: 0, WARNUNG: 0, HINWEIS: 0}
    for o in laeufe:
        z = melde(pruefe_lauf(o, welt=welt, inv=inv, rw=rw, orte=orte), os.path.basename(o))
        for k in gesamt:
            gesamt[k] += z[k]
    sys.stdout.write("[gefaelle_pruefen] GESAMT %d Laeufe: %d FEHLER, %d WARNUNG, %d HINWEIS\n"
                     % (len(laeufe), gesamt[FEHLER], gesamt[WARNUNG], gesamt[HINWEIS]))
    return 1 if gesamt[FEHLER] else 0


if __name__ == "__main__":
    sys.exit(main())
