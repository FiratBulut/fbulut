# -*- coding: utf-8 -*-
"""p2_bett_welt.py - 16h Nachtrag 6c, LOKAL: rechnet den p2-Bettplan (Bach-Koordinaten s, u) ueber lauf_p2.json in
Weltzellen um und schreibt ihn im A15-Format (wie gefaelle/<lauf>/: plan.json + gelaende/<id>.f32 mit fenster_ij,
instanzen/<Feld>/plan.json + <Netz>.f32 nach FORMAT.md §3) sowie die Spiegelpunkte fuer die SWR-Spline.

Eingabe:
  --plan DIR     antworten/p2_bett/ (bettplan_p2.json, talkaskade_soll.f32)
  --lauf DATEI   lauf_p2.json (Ferat 6e: Schluessel i, j = Zeile/Spalte des 1-m-Rasters, X = (j - 4730,5) m,
                 Y = (i - 4060,5) m, s in m auf den 1-m-Punkten; dazu sohle, spiegel, tiefe, breite, marken_s_m).
                 Erkannt werden Spaltenform {i: [...], j: [...], s: [...]}, Liste von Punkten oder ein Objekt mit einer
                 Punktliste ('punkte', 'mittellinie', 'linie', 'spline', 'points'); Punkt = [x, y, ...] oder
                 {x|x_cm|X, y|y_cm|Y} oder {i, j}. Einheit automatisch (i/j = Raster, |Wert| > 20000 = cm), sonst
                 --einheit cm|m|raster. s aus 's'/'s_m' je Punkt, sonst Bogenlaenge (wie querschnitte_p2.json).
  --welt DIR     export/unreal/welt (hoehe.f32, NY x NX float32, FORMAT.md §2)
Ausgabe (--aus, Standard <welt>/p2_bett/ERLENBACH_P2):
  plan.json                   abschnitte[] je Feld mit gelaende {datei, fenster_ij [i0, j0, hoehe, breite], max_aenderung_m}
  gelaende/<id>_<Feld>.f32    Delta (m) im 1-m-Raster, Fenster zeilenweise
  instanzen/<Feld>/...        Bloecke und Kies (Ebene p2_bett, FT_EL_P2B_*)
  pruefband/<ab>_<Feld>.u8    1 = neues Bett, 2 = Band 0,25-2 m hinter der Bettkante (6b: nach dem Bake <= 5 % nass)
  spline_spiegel.json         [s, x_cm, y_cm, z_cm] je Meter: Z der SWR-Spline = neuer Spiegel
  delta_welt.png (--bild)     Delta in Weltlage (1 m = 3 px)

Normale wie in Ferats Querschnitten: Tangente = Sehne ueber +-3 Punkte, links = (-t_j, t_i) im Raster; u > 0 links.

  python -I p2_bett_welt.py --plan recherche/antworten/p2_bett --lauf <lauf_p2.json> --welt export/unreal/welt [--bild]
  python -I p2_bett_welt.py --selbsttest     (Cloud: kuenstliche Spline + Gelaende, Rueckrechnung gegen den Plan)
"""
import argparse
import csv
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
ANTW = os.path.normpath(os.path.join(HIER, "..", ".."))
DATEN = os.path.normpath(os.path.join(ANTW, "..", "vorlagen", "daten"))
NX, NY = 9577, 7057
OFF_J, OFF_I = 4730.5, 4060.5
FELD_M = 1008
SPALTEN = "ABCDEFGHIJ"
LAUF_ID = "ERLENBACH_P2"


# ----------------------------------------------------------------------------------------------------------------------
def feld_ij(i, j):
    return "%s%d" % (SPALTEN[int(j) // FELD_M], int(i) // FELD_M + 1)


def feld_cm(x_cm, y_cm):
    j = x_cm / 100.0 + OFF_J
    i = y_cm / 100.0 + OFF_I
    return feld_ij(math.floor(i + 0.5), math.floor(j + 0.5)) if 0 <= j < NX and 0 <= i < NY else None


def lauf_lesen(pfad, einheit=None):
    with open(pfad, encoding="utf-8") as f:
        d = json.load(f)
    P = None
    if isinstance(d, dict) and isinstance(d.get("i"), list) and isinstance(d.get("j"), list):
        # Spaltenform (Ferat 6e: Schluessel i, j, s, sohle, spiegel, tiefe, breite je als Liste)
        n = min(len(d["i"]), len(d["j"]))
        ss = d.get("s") if isinstance(d.get("s"), list) and len(d["s"]) >= n else None
        P = [{"i": d["i"][k], "j": d["j"][k], **({"s": ss[k]} if ss else {})} for k in range(n)]
    elif isinstance(d, list):
        P = d
    else:
        for k in ("punkte", "mittellinie", "linie", "spline", "points", "punkte_1m"):
            if isinstance(d.get(k), list) and len(d[k]) >= 10:
                P = d[k]
                break
        if P is None:
            for k in sorted(d):
                if isinstance(d[k], list) and len(d[k]) >= 10:
                    P = d[k]
                    break
    if not P:
        raise SystemExit("lauf_p2.json: keine Punktliste gefunden (Schluessel: %s)" % (sorted(d) if isinstance(d, dict) else "Liste"))
    a, b, s = [], [], []
    art = einheit
    for p in P:
        if isinstance(p, dict):
            if "i" in p and "j" in p:
                a.append(float(p["i"])), b.append(float(p["j"]))
                art = art or "raster"
            else:
                x = next(p[k] for k in ("x_cm", "x", "X") if k in p)
                y = next(p[k] for k in ("y_cm", "y", "Y") if k in p)
                b.append(float(x)), a.append(float(y))
            sv = p.get("s", p.get("s_m"))
            s.append(None if sv is None else float(sv))
        else:
            b.append(float(p[0])), a.append(float(p[1]))
            s.append(None)
    a, b = np.array(a), np.array(b)
    if art is None:
        art = "cm" if max(np.abs(a).max(), np.abs(b).max()) > 20000 else None
    if art is None:
        raise SystemExit("lauf_p2.json: Einheit nicht eindeutig - bitte --einheit cm|m|raster angeben")
    if art == "cm":
        I, J = a / 100.0 + OFF_I, b / 100.0 + OFF_J
    elif art == "m":
        I, J = a + OFF_I, b + OFF_J
    else:
        I, J = a, b
    if all(v is not None for v in s):
        S = np.array(s)
    else:
        S = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(I), np.diff(J)))])
    return I, J, S, art


class Lauf:
    """Mittellinie im 1-m-Raster (i, j) mit Ferats Normale (Sehne +-3 Punkte, links = (-t_j, t_i))."""

    def __init__(self, I, J, S):
        self.I, self.J, self.S = I, J, S
        n = len(I)
        ti = np.array([I[min(k + 3, n - 1)] - I[max(k - 3, 0)] for k in range(n)])
        tj = np.array([J[min(k + 3, n - 1)] - J[max(k - 3, 0)] for k in range(n)])
        L = np.hypot(ti, tj)
        self.ti, self.tj = ti / L, tj / L

    def punkt(self, s, u=0.0):
        i = np.interp(s, self.S, self.I)
        j = np.interp(s, self.S, self.J)
        ti = np.interp(s, self.S, self.ti)
        tj = np.interp(s, self.S, self.tj)
        L = np.hypot(ti, tj)
        ti, tj = ti / L, tj / L
        return i + u * (-tj), j + u * ti, ti, tj

    def bach(self, ci, cj, s0, s1):
        """Weltzellen -> (s, u): naechster Punkt auf der Mittellinie zwischen s0 und s1, u ueber Ferats Normale."""
        k0 = max(int(np.searchsorted(self.S, s0)) - 2, 0)
        k1 = min(int(np.searchsorted(self.S, s1)) + 2, len(self.S) - 1)
        Ai, Aj = self.I[k0:k1], self.J[k0:k1]
        Bi, Bj = self.I[k0 + 1:k1 + 1], self.J[k0 + 1:k1 + 1]
        Sa, Sb = self.S[k0:k1], self.S[k0 + 1:k1 + 1]
        best_d = np.full(ci.shape, np.inf)
        best_s = np.zeros(ci.shape)
        for a in range(len(Ai)):
            di, dj = Bi[a] - Ai[a], Bj[a] - Aj[a]
            ll = di * di + dj * dj
            t = np.clip(((ci - Ai[a]) * di + (cj - Aj[a]) * dj) / max(ll, 1e-9), 0.0, 1.0)
            pi, pj = Ai[a] + t * di, Aj[a] + t * dj
            d = (ci - pi) ** 2 + (cj - pj) ** 2
            m = d < best_d
            best_d[m] = d[m]
            best_s[m] = (Sa[a] + t * (Sb[a] - Sa[a]))[m]
        i0, j0, ti, tj = self.punkt(best_s)
        u = (ci - i0) * (-tj) + (cj - j0) * ti
        s_korr = best_s + (ci - i0) * ti + (cj - j0) * tj      # Rest laengs (Kurveninnenseite), meist ~0
        return s_korr, u


def raster_probe(A, s0, ds, u0, du, s, u):
    """Bilinear, wo alle vier Nachbarn endlich sind, sonst naechster Nachbar (NaN = keine Grenze bleibt NaN)."""
    ns, nu = A.shape
    x = (s - s0) / ds
    y = (u - u0) / du
    i0 = np.clip(np.floor(x).astype(int), 0, ns - 2)
    j0 = np.clip(np.floor(y).astype(int), 0, nu - 2)
    fx = np.clip(x - i0, 0, 1)
    fy = np.clip(y - j0, 0, 1)
    a, b, c, d = A[i0, j0], A[i0 + 1, j0], A[i0, j0 + 1], A[i0 + 1, j0 + 1]
    bil = a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy
    ni = np.clip(np.round(x).astype(int), 0, ns - 1)
    nj = np.clip(np.round(y).astype(int), 0, nu - 1)
    nah = A[ni, nj]
    ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(c) & np.isfinite(d)
    return np.where(ok, bil, nah)


def quat_yaw_pitch(yaw_grad, pitch_grad):
    """Quaternion (x, y, z, w): erst Neigung um die Querachse (Y), dann Drehung um Z (Unreal: Z oben)."""
    y, p = math.radians(yaw_grad) / 2.0, math.radians(pitch_grad) / 2.0
    cy, sy, cp, sp = math.cos(y), math.sin(y), math.cos(p), math.sin(p)
    return (-sy * sp, cy * sp, sy * cp, cy * cp)


def hoehe_laden(welt):
    pf = os.path.join(welt, "hoehe.f32")
    if not os.path.exists(pf):
        raise SystemExit("hoehe.f32 fehlt: %s" % pf)
    return np.memmap(pf, dtype="<f4", mode="r", shape=(NY, NX))


def bilinear_welt(H, i, j):
    i0, j0 = int(math.floor(i)), int(math.floor(j))
    fi, fj = i - i0, j - j0
    a = H[i0, j0] * (1 - fi) * (1 - fj) + H[i0 + 1, j0] * fi * (1 - fj) + H[i0, j0 + 1] * (1 - fi) * fj + \
        H[i0 + 1, j0 + 1] * fi * fj
    return float(a)


# ----------------------------------------------------------------------------------------------------------------------
def welt_rechnen(plan_dir, lauf, H, aus, bild=False):
    with open(os.path.join(plan_dir, "bettplan_p2.json"), encoding="utf-8") as f:
        P = json.load(f)
    g = P["gelaende"]
    A = np.fromfile(os.path.join(plan_dir, g["datei"]), dtype="<f4").reshape(g["form"]).astype(float)
    ZLO, ZHI, WG, WS, AM, KA = A
    ns, nu = WG.shape
    s0, ds, u0, du = g["s0_m"], g["ds_m"], g["u0_m"], g["du_m"]
    s1, u1 = s0 + (ns - 1) * ds, u0 + (nu - 1) * du
    # Weltzellen im Korridor
    ss = np.arange(s0, s1 + 1e-9, 0.5)
    pi, pj, _, _ = lauf.punkt(ss)
    r = abs(u0) + 2.0
    i_lo, i_hi = int(math.floor(pi.min() - r)), int(math.ceil(pi.max() + r))
    j_lo, j_hi = int(math.floor(pj.min() - r)), int(math.ceil(pj.max() + r))
    i_lo, j_lo = max(i_lo, 0), max(j_lo, 0)
    i_hi, j_hi = min(i_hi, NY - 1), min(j_hi, NX - 1)
    ci, cj = np.meshgrid(np.arange(i_lo, i_hi + 1, dtype=float), np.arange(j_lo, j_hi + 1, dtype=float), indexing="ij")
    s, u = lauf.bach(ci, cj, s0 - 1.0, s1 + 1.0)
    innen = (s >= s0) & (s <= s1) & (u >= u0) & (u <= u1)
    ist = np.asarray(H[i_lo:i_hi + 1, j_lo:j_hi + 1], dtype=float)
    lo = raster_probe(ZLO, s0, ds, u0, du, s, u)
    hi = raster_probe(ZHI, s0, ds, u0, du, s, u)
    w = np.clip(raster_probe(WG, s0, ds, u0, du, s, u), 0, 1)
    am = raster_probe(AM, s0, ds, u0, du, s, u)
    w = np.where(innen, w, 0.0)
    lo_ = np.where(np.isfinite(lo), lo, -np.inf)
    hi_ = np.where(np.isfinite(hi), hi, np.inf)
    neu = ist + w * (np.clip(ist, lo_, hi_) - ist)
    neu = np.maximum(neu, ist - np.where(np.isfinite(am), am, np.inf))
    delta = np.where(innen, neu - ist, 0.0)
    ka = raster_probe(KA, s0, ds, u0, du, s, u)
    # Pruefband fuer den naechsten Bake (6b): 1 = neues Bett, 2 = Band 0,25-2 m hinter der Bettkante (Ziel <= 5 % nass)
    band = np.zeros(delta.shape, dtype=np.uint8)
    band[innen & (ka <= 0.0)] = 1
    band[innen & (ka > 0.25) & (ka <= 2.0) & (w > 0.5)] = 2
    os.makedirs(aus, exist_ok=True)
    for sub in ("gelaende", "instanzen", "pruefband"):
        if os.path.isdir(os.path.join(aus, sub)):
            shutil.rmtree(os.path.join(aus, sub))
    os.makedirs(os.path.join(aus, "gelaende"))
    os.makedirs(os.path.join(aus, "pruefband"))
    ab = P["abschnitt"]
    abschnitte = []
    felder = sorted({feld_ij(i, j) for i, j in zip(ci[np.abs(delta) > 0.005].astype(int), cj[np.abs(delta) > 0.005].astype(int))})
    for fe in felder:
        fs, fr = SPALTEN.index(fe[0]), int(fe[1:]) - 1
        m = (np.abs(delta) > 0.005) & (cj // FELD_M == fs) & (ci // FELD_M == fr)
        ii, jj = np.nonzero(m)
        a0, a1, b0, b1 = ii.min(), ii.max(), jj.min(), jj.max()
        win = np.zeros((a1 - a0 + 1, b1 - b0 + 1), dtype="<f4")
        sub = delta[a0:a1 + 1, b0:b1 + 1]
        msub = m[a0:a1 + 1, b0:b1 + 1]
        win[msub] = sub[msub]
        rel = "gelaende/%s_%s_%s.f32" % (LAUF_ID, ab, fe)
        win.tofile(os.path.join(aus, rel))
        bw = band[a0:a1 + 1, b0:b1 + 1].astype(np.uint8)
        bw.tofile(os.path.join(aus, "pruefband", "%s_%s.u8" % (ab, fe)))
        abschnitte.append({"id": "%s_%s_%s" % (LAUF_ID, ab, fe), "felder": [fe],
                           "gelaende": {"datei": rel, "fenster_ij": [int(i_lo + a0), int(j_lo + b0), int(a1 - a0 + 1),
                                                                     int(b1 - b0 + 1)],
                                        "max_aenderung_m": round(float(np.abs(win).max()), 2),
                                        "begruendung": "16h Nachtrag 6c: natuerlicher Bettplan p2 (Step-Pool, Uferstufe)",
                                        "werkzeuge": ["p2_bett_welt"]},
                           "pruefband": {"datei": "pruefband/%s_%s.u8" % (ab, fe), "fenster_ij": [int(i_lo + a0), int(j_lo + b0),
                                                                                                  int(a1 - a0 + 1), int(b1 - b0 + 1)],
                                         "werte": {"1": "neues Bett", "2": "Band 0,25-2 m hinter der Bettkante"}}})
    # Instanzen
    with open(os.path.join(DATEN, "netze.csv"), encoding="utf-8") as f:
        Rn = {r_["name"]: r_ for r_ in csv.DictReader(f, delimiter=";")}
    sp = P["instanzen_spalten"]
    ix = {k: n for n, k in enumerate(sp)}
    je_feld = {}
    farn_weg = 0
    for schl, e in sorted(P["instanzen"].items()):
        netz = e.get("netz", schl)
        hz = float(e["groesse_m"][2])
        for row in e["eintraege"]:
            sv, uv = row[ix["s_m"]], row[ix["u_m"]]
            i_, j_, ti, tj = lauf.punkt(sv, uv)
            gi = bilinear_welt(H, float(i_), float(j_))
            # neues Gelaende an der Stelle: Ist + Delta (Delta aus dem Fenster, naechste Zelle)
            a_, b_ = int(round(float(i_))) - i_lo, int(round(float(j_))) - j_lo
            dz = float(delta[a_, b_]) if 0 <= a_ < delta.shape[0] and 0 <= b_ < delta.shape[1] else 0.0
            z = gi + dz - row[ix["einbettung"]] * hz * row[ix["skala"]]
            if "z_absolut" in ix and row[ix["z_absolut"]]:
                z = row[ix["z_plan_m"]]
            if "farn" in e.get("rollen", {}):
                # nur Nordufer: Aussennormale (vom Bach zum Ufer) zeigt nach +Y (Sueden) -> Boeschung schaut nach Norden
                o_i = (1.0 if uv > 0 else -1.0) * float(ti)          # links = (-t_j, t_i): i-Anteil = t_i
                if o_i <= 0.3:
                    farn_weg += 1
                    continue
            x_cm = (float(j_) - OFF_J) * 100.0
            y_cm = (float(i_) - OFF_I) * 100.0
            kurs = math.degrees(math.atan2(float(ti), float(tj)))         # Fliessrichtung in Welt (X = j, Y = i)
            q = quat_yaw_pitch(kurs + row[ix["yaw_rel_grad"]], row[ix["kipp_grad"]])
            sk = row[ix["skala"]]
            fe = feld_cm(x_cm, y_cm)
            key = schl
            je_feld.setdefault(fe, {}).setdefault(key, {"netz": netz, "e": e, "rec": [], "hind": 0})
            je_feld[fe][key]["rec"].append([x_cm, y_cm, z * 100.0, q[0], q[1], q[2], q[3], sk, sk, sk])
            je_feld[fe][key]["hind"] += bool(row[ix["swr_hindernis"]])
    hindernisse = []
    for fe, dd in sorted(je_feld.items()):
        ordner = os.path.join(aus, "instanzen", fe)
        os.makedirs(ordner, exist_ok=True)
        dateien = {}
        for key, v in sorted(dd.items()):
            np.array(v["rec"], dtype="<f4").tofile(os.path.join(ordner, key + ".f32"))
            e = v["e"]
            dateien[key] = {"pfad": e["pfad"], "anzahl": len(v["rec"]), "gruppe": e["ebene"],
                            "rolle": "/".join(sorted(e["rollen"])), "sichtweite": e["sichtweite"],
                            "schatten": e["ebene"] != "kleinzeug", "kollision": bool(e["kollision"]),
                            "nanite": Rn.get(v["netz"], {}).get("nanite", "0") == "1", "ebene": "p2_bett"}
            if v["hind"]:
                dateien[key]["swr_hindernis_anzahl"] = v["hind"]
                hindernisse.append({"feld": fe, "datei": key + ".f32", "anzahl": v["hind"]})
        n = sum(d["anzahl"] for d in dateien.values())
        with open(os.path.join(ordner, "plan.json"), "w", encoding="utf-8") as f:
            json.dump({"stand": P["stand"], "feld": fe, "ebene": "p2_bett", "instanzen": n,
                       "kollision_anzahl": sum(d["anzahl"] for d in dateien.values() if d["kollision"]),
                       "ft_praefix": "FT_EL_P2B_", "ft_ordner": "/Game/Eldarien/Welt/Foliage/p2_bett",
                       "hinweis_setzer": "z enthaelt das Eingraben; Bloecke >= 0,8 m mit Kollision; swr_hindernis_anzahl = "
                                         "Eintraege mit SWR-Hindernis (Spalte in bettplan_p2.json), nur Beckenbloecke",
                       "dateien": dateien}, f, ensure_ascii=False, indent=1)
            f.write("\n")
    # Spline-Spiegel
    spl = []
    for sv, zv in P["spiegel_je_m"]["punkte"]:
        i_, j_, _, _ = lauf.punkt(sv)
        spl.append([sv, round((float(j_) - OFF_J) * 100.0, 1), round((float(i_) - OFF_I) * 100.0, 1), round(zv * 100.0, 1)])
    with open(os.path.join(aus, "spline_spiegel.json"), "w", encoding="utf-8") as f:
        json.dump({"hinweis": "Z der SWR-Spline (cm) je Meter auf der lauf_p2-Mittellinie im Bereich des Plans; ausserhalb "
                              "unveraendert lassen.", "spalten": ["s_m", "x_cm", "y_cm", "z_cm"], "punkte": spl}, f)
        f.write("\n")
    plan = {"stand": P["stand"], "lauf": LAUF_ID, "quelle": "p2_bett_welt.py aus bettplan_p2.json", "felder": felder,
            "abschnitte": abschnitte, "spline_spiegel": "spline_spiegel.json", "swr_hindernisse": hindernisse,
            "kennzahlen": {"zellen_geaendert": int((np.abs(delta) > 0.005).sum()),
                           "delta_m": [round(float(delta.min()), 2), round(float(delta.max()), 2)],
                           "farne_nicht_nordufer_weggelassen": farn_weg,
                           "abtrag_m3": round(float(-delta[delta < 0].sum()), 0),
                           "auftrag_m3": round(float(delta[delta > 0].sum()), 0)}}
    with open(os.path.join(aus, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
        f.write("\n")
    if bild:
        from PIL import Image
        t = np.clip(np.abs(delta) / 2.0, 0, 1) ** 0.7
        rgb = np.full(delta.shape + (3,), 240.0)
        blau, rot = np.array([16, 66, 129.0]), np.array([130, 30, 30.0])
        neg, pos = delta < -0.05, delta > 0.05
        rgb[neg] = (np.array([240, 239, 236.0]) * (1 - t[neg, None]) + blau * t[neg, None])
        rgb[pos] = (np.array([240, 239, 236.0]) * (1 - t[pos, None]) + rot * t[pos, None])
        im = Image.fromarray(rgb.astype(np.uint8)).resize((delta.shape[1] * 3, delta.shape[0] * 3), Image.NEAREST)
        im.save(os.path.join(aus, "delta_welt.png"))
    return plan, (ci, cj, s, u, delta, i_lo, j_lo)


# ----------------------------------------------------------------------------------------------------------------------
def selbsttest():
    """Kuenstliche, gekruemmte Spline in einem Feld, Gelaende = angenommenes Ist des Plans; Rueckrechnung: das Delta der
    Weltzellen muss dem Plan-Delta an derselben Stelle (s, u) entsprechen."""
    sys.path.insert(0, HIER)
    import p2_bettplan as pb
    tmp = tempfile.mkdtemp()
    plan_dir = os.path.join(tmp, "plan")
    X = pb.rechne()
    pb.schreiben(X, plan_dir)
    # Spline: Bogen in Feld C2 (i ~ 1500, j ~ 2400), 1-m-Punkte, s 0..786
    n = 787
    t = np.arange(n, dtype=float)
    ang = 0.6 + 0.0015 * t + 0.25 * np.sin(t / 90.0)
    di, dj = np.sin(ang), np.cos(ang)
    I = 1300.0 + np.concatenate([[0], np.cumsum(di[:-1])])
    J = 2100.0 + np.concatenate([[0], np.cumsum(dj[:-1])])
    lauf_pf = os.path.join(tmp, "lauf_p2.json")
    with open(lauf_pf, "w") as f:
        json.dump({"punkte": [{"i": round(a, 4), "j": round(b, 4), "s": float(k)} for k, (a, b) in enumerate(zip(I, J))]}, f)
    Il, Jl, Sl, art = lauf_lesen(lauf_pf)
    lauf_sp = os.path.join(tmp, "lauf_p2_spalten.json")
    with open(lauf_sp, "w") as f:
        json.dump({"i": [round(a, 4) for a in I], "j": [round(b, 4) for b in J], "s": [float(k) for k in range(n)],
                   "spiegel": [0.0] * n, "breite": [3.0] * n, "marken_s_m": [0.0, 200.0]}, f)
    I2, J2, S2, art2 = lauf_lesen(lauf_sp)
    spalten_ok = art2 == "raster" and np.allclose(I2, Il) and np.allclose(J2, Jl) and np.allclose(S2, Sl)
    lauf = Lauf(Il, Jl, Sl)
    # Gelaende: Ist des Plans (angenommenes Bett + Ufer aus den Querschnitten), ausserhalb Narbe
    welt = os.path.join(tmp, "welt")
    os.makedirs(welt)
    pf = os.path.join(welt, "hoehe.f32")
    with open(pf, "wb") as f:
        f.truncate(NX * NY * 4)                 # duenn belegte Datei
    H = np.memmap(pf, dtype="<f4", mode="r+", shape=(NY, NX))
    G = X["G"]
    pi_, pj_, _, _ = lauf.punkt(np.arange(G["S"][0] - 20, G["S"][-1] + 20, 1.0))
    a0, a1 = int(pi_.min()) - 25, int(pi_.max()) + 25
    b0, b1 = int(pj_.min()) - 25, int(pj_.max()) + 25
    ci, cj = np.meshgrid(np.arange(a0, a1, dtype=float), np.arange(b0, b1, dtype=float), indexing="ij")
    s, u = lauf.bach(ci, cj, G["S"][0] - 30, G["S"][-1] + 30)
    S, U = G["S"], G["U"]
    m = (s >= S[0]) & (s <= S[-1]) & (np.abs(u) <= U[-1])
    z = np.full(ci.shape, 0.0)
    z[m] = pb_raster(X["ist_z"], S, U, s[m], u[m])
    # ausserhalb: Narbe + 2 m (hoch genug, nie im Plan)
    z[~m] = np.interp(s[~m], X["ist"].s, X["ist"].T) + 2.0
    H[a0:a1, b0:b1] = z.astype("<f4")
    H.flush()
    aus = os.path.join(tmp, "aus")
    plan, (ci2, cj2, s2, u2, delta, i_lo, j_lo) = welt_rechnen(plan_dir, lauf, H, aus, bild=True)
    # Vergleich: Plan-Delta an (s, u) der Weltzellen
    d_plan = X["z_neu"] - X["ist_z"]
    mm = (s2 >= S[0] + 1) & (s2 <= S[-1] - 1) & (np.abs(u2) <= 9.0)
    ref = pb_raster(d_plan, S, U, s2[mm], u2[mm])
    fehl = np.abs(delta[mm] - ref)
    ok = float(np.percentile(fehl, 95)) < 0.15
    zus = {"zellen": int(mm.sum()), "abweichung_median_m": round(float(np.median(fehl)), 3),
           "abweichung_p95_m": round(float(np.percentile(fehl, 95)), 3), "felder": plan["felder"],
           "abschnitte": len(plan["abschnitte"]), "instanzen_felder": sorted(os.listdir(os.path.join(aus, "instanzen"))),
           "kennzahlen": plan["kennzahlen"]}
    # Determinismus
    aus2 = os.path.join(tmp, "aus2")
    welt_rechnen(plan_dir, lauf, H, aus2)
    gleich = True
    for root, _, files in os.walk(aus):
        for fn in files:
            if fn.endswith(".png"):
                continue
            p1 = os.path.join(root, fn)
            p2 = os.path.join(aus2, os.path.relpath(p1, aus))
            with open(p1, "rb") as f1, open(p2, "rb") as f2:
                gleich &= hashlib.sha256(f1.read()).digest() == hashlib.sha256(f2.read()).digest()
    zus["zwei_laeufe_byte_gleich"] = gleich
    zus["lauf_spaltenform_gelesen"] = bool(spalten_ok)
    gleich = gleich and spalten_ok
    print(json.dumps(zus, ensure_ascii=False))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok and gleich else 1


def pb_raster(A, S, U, s, u):
    return raster_probe(A, float(S[0]), float(S[1] - S[0]), float(U[0]), float(U[1] - U[0]), s, u)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default=os.path.join(ANTW, "p2_bett"))
    ap.add_argument("--lauf")
    ap.add_argument("--welt")
    ap.add_argument("--aus")
    ap.add_argument("--einheit", choices=["cm", "m", "raster"])
    ap.add_argument("--bild", action="store_true")
    ap.add_argument("--selbsttest", action="store_true")
    a = ap.parse_args(argv)
    if a.selbsttest:
        rc = selbsttest()
        print("[p2_bett_welt] selbsttest %s" % ("OK" if rc == 0 else "FEHLER"))
        return rc
    if not (a.lauf and a.welt):
        ap.error("--lauf und --welt sind noetig (oder --selbsttest)")
    I, J, S, art = lauf_lesen(a.lauf, a.einheit)
    H = hoehe_laden(a.welt)
    aus = a.aus or os.path.join(a.welt, "p2_bett", LAUF_ID)
    plan, _ = welt_rechnen(a.plan, Lauf(I, J, S), H, aus, a.bild)
    print(json.dumps({"felder": plan["felder"], "abschnitte": len(plan["abschnitte"]), "kennzahlen": plan["kennzahlen"],
                      "lauf_einheit": art}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
