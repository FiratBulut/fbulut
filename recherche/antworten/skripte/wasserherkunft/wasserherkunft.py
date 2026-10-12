# -*- coding: utf-8 -*-
"""wasserherkunft.py - Auftrag 17: Woher kommt das Wasser unserer Wasserfaelle?

Liest NUR (aendert keinen Planer, kein Gelaende):
  - Weltdaten 2 m (sehens_lib.daten.lade): Hoehe, Biom, Boden, Wasser, Meer, wasser_welt.json (Welt-Wasserfaelle)
  - fluss_sim-Export (--fs): gewaesser/*/fluss_sim.json und sehens/*/*/fluss_sim.json -> Faelle mit Vorhang,
    Anfang/Muendung der Gewaesser (Muendung "wasserfall")
  - Sehens-Planer-Ausgaben (--sehens): <biom>/orte.json -> wasser typ "wasserfall", Baeche und Seen am Fall
  - wasser_fx/plan.json (Breite der Welt-Wasserfaelle)

Rechnet je Fall (D8 auf dem 2-m-Raster, Senken gefuellt, sehens_lib.gelaende):
  Einzugsgebiet oberhalb der Lippe, mittlerer Abfluss (Niederschlag x Abflussbeiwert je Biom, Nebelzuschlag),
  Bedarf aus der Fallbreite (Poleni), Lauflaenge oberhalb (geplantes Wasser und laengster Fliessweg im Gelaende),
  Gipfel ueber der Lippe, sichtbare Rinne, Quellmerkmale (See, Schnee/Eis im Einzugsgebiet), Biom, Insel.
  Bewertung plausibel / fragwuerdig / aus_dem_nichts, Empfehlung, Vorschlagspunkte fuer einen Oberlauf.

Aufruf (Cloud, 2 m):
  python -I recherche/antworten/skripte/wasserherkunft/wasserherkunft.py --daten2m recherche/vorlagen/daten/sehens \
      --fs <s>/fs --sehens <s>/sehens --aus recherche/antworten/wasserherkunft [--cache <ordner>] [--bild]

Deterministisch: feste Reihenfolgen (sortierte Pfade/IDs), keine Zufallszahlen, Rundung der Ausgaben.
"""

import argparse
import collections
import glob
import hashlib
import json
import math
import os
import sys

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
SKRIPTE = os.path.dirname(HIER)
ANTWORTEN = os.path.dirname(SKRIPTE)
sys.path.insert(0, SKRIPTE)

from sehens_lib import daten as D          # noqa: E402
from sehens_lib import gelaende as G       # noqa: E402
from sehens_lib import log, Uhr            # noqa: E402

REGELN_STANDARD = os.path.join(HIER, "wasserherkunft_regeln.json")
WASSER_FX_PLAN = os.path.join(ANTWORTEN, "wasser_fx", "plan.json")
SEK_JAHR = 365.25 * 86400.0
VERSION = 1


def r(x, n=1):
    return None if x is None else round(float(x), n)


def lese(pf):
    with open(pf, "r", encoding="utf-8") as f:
        return json.load(f)


# ======================================================================================================================
# Ganze-Welt-Raster: gewichtete Akkumulation, hoechster Punkt und laengster Fliessweg oberhalb
# ======================================================================================================================
def oberhalb_rechnen(rec, h, z, gewichte):
    """Kahn-Topologie ueber das Empfaenger-Feld (wie gelaende.akkumulation).

    gewichte: dict name -> flaches float-Array (je Zelle). Rueckgabe dict name -> Summe oberhalb (inkl. Zelle),
    dazu 'max_h' (hoechster Punkt oberhalb inkl. Zelle) und 'l_max' (laengster Fliessweg oberhalb, m)."""
    rec = rec.reshape(-1)
    N = rec.size
    nx = h.shape[1]
    summen = {k: v.reshape(-1).astype(np.float64).copy() for k, v in gewichte.items()}
    mh = h.reshape(-1).astype(np.float32).copy()
    lm = np.zeros(N, np.float32)
    gueltig = rec >= 0
    indeg = np.bincount(rec[gueltig], minlength=N).astype(np.int32)
    F = np.flatnonzero(indeg == 0).astype(np.int32)
    runden = 0
    while F.size:
        runden += 1
        t = rec[F]
        m = t >= 0
        F = F[m]
        t = t[m]
        if not t.size:
            break
        ut, inv = np.unique(t, return_inverse=True)
        for k in summen:
            a = summen[k]
            a[ut] += np.bincount(inv, weights=a[F])
        np.maximum.at(mh, t, mh[F])
        d = np.abs(t.astype(np.int64) - F)
        schritt = np.where((d == nx - 1) | (d == nx + 1), z * 1.4142135, z).astype(np.float32)
        np.maximum.at(lm, t, lm[F] + schritt)
        indeg[ut] -= np.bincount(inv).astype(np.int32)
        F = ut[indeg[ut] == 0]
    out = {k: v.astype(np.float32).reshape(h.shape) for k, v in summen.items()}
    out["max_h"] = mh.reshape(h.shape)
    out["l_max"] = lm.reshape(h.shape)
    log("Oberhalb-Raster: %d Runden" % runden)
    return out


def niederschlag_raster(welt, R):
    """Abflusshoehe je Zelle in m/a = P (mm/a) x Abflussbeiwert, mit Nebelzuschlag (Biome, Hoehe)."""
    P = np.zeros(256, np.float32)
    C = np.zeros(256, np.float32)
    for k, n in enumerate(D.BIOME):
        P[k] = R["niederschlag_mm_a"][n]
        C[k] = R["abflussbeiwert"][n]
    P[D.BIOM_MEER] = 0.0
    p = P[welt.biom]
    nb = R["nebel_zuschlag"]
    nebel = np.zeros(welt.biom.shape, bool)
    for n in nb["biome"]:
        nebel |= welt.biom == D.BIOME.index(n)
    nebel &= welt.hoehe >= nb["ab_hoehe_m"]
    p = np.where(nebel, p * (1.0 + nb["faktor"]), p)
    return (p * C[welt.biom] / 1000.0).astype(np.float32)


def regel_kennung(R, seen):
    teile = {k: R[k] for k in ("niederschlag_mm_a", "abflussbeiwert", "nebel_zuschlag", "quellmerkmal")}
    teile["seen"] = [[s["id"], [[round(a, 1), round(b, 1)] for a, b in s["umriss_m"]]] for s in seen]
    return hashlib.sha1(json.dumps(teile, sort_keys=True).encode()).hexdigest()[:10]


def seen_maske(welt, seen):
    """Seen/Teiche (Polygone in m) auf das native Raster (PIL, deterministisch)."""
    from PIL import Image, ImageDraw
    img = Image.new("L", (welt.nx, welt.ny), 0)
    d = ImageDraw.Draw(img)
    for s in seen:
        i, j = welt.m_zu_ij(np.array([p[0] for p in s["umriss_m"]]), np.array([p[1] for p in s["umriss_m"]]),
                            runden=False)
        if len(i) >= 3:
            d.polygon([(float(b), float(a)) for a, b in zip(i, j)], fill=1)
    return np.array(img) > 0


def alle_seen(welt, sehens):
    """Seen (wasser_welt), Teiche (teiche.json ueber welt.teiche) und Sehens-Seen (orte.json) als Polygone in m."""
    out = []
    for s in (welt.wasser_welt or {}).get("seen", []) or []:
        if s.get("umriss"):
            out.append({"id": s["id"], "umriss_m": [[p[0] / 100.0, p[1] / 100.0] for p in s["umriss"]]})
    for s in welt.teiche or []:
        if s.get("umriss"):
            out.append({"id": s["id"], "umriss_m": [[p[0] / 100.0, p[1] / 100.0] for p in s["umriss"]]})
    for biom in D.BIOME:
        pf = os.path.join(sehens, biom, "orte.json")
        if not os.path.exists(pf):
            continue
        for o in lese(pf).get("orte", []):
            for w in o.get("wasser") or []:
                if w.get("typ") == "see" and w.get("umriss_cm"):
                    out.append({"id": "%s/%s" % (o["id"], w.get("id")),
                                "umriss_m": [[p[0] / 100.0, p[1] / 100.0] for p in w["umriss_cm"]]})
    out.sort(key=lambda s: s["id"])
    return out


def welt_raster(welt, gel, R, seen):
    """Abflussraster (gecacht neben dem Gelaende-Cache)."""
    namen = ("q_m3a", "schnee_m2", "see_m2", "max_h", "l_max")
    ordner = os.path.join(gel.cache, "wasserherkunft_%s" % regel_kennung(R, seen)) if gel.cache else None
    if ordner and all(os.path.exists(os.path.join(ordner, n + ".npy")) for n in namen):
        log("Cache geladen: %s" % ordner)
        return {n: np.load(os.path.join(ordner, n + ".npy"), mmap_mode="r") for n in namen}
    z = welt.zelle_m
    abfluss_h = niederschlag_raster(welt, R) * (z * z)                         # m3/a je Zelle
    codes = [D.BODEN.index(b) for b in R["quellmerkmal"]["schnee_boeden"]]
    boden = welt.boden
    schnee = np.isin(boden, codes) | (welt.biom == D.BIOME.index("gletscher"))
    see = seen_maske(welt, seen) & ~welt.meer
    with Uhr("berechne Oberhalb-Raster (Abfluss, Schnee, See, Gipfel, Fliessweg)"):
        o = oberhalb_rechnen(gel.empfaenger, welt.hoehe, z,
                             {"q_m3a": abfluss_h, "schnee_m2": schnee.astype(np.float32) * (z * z),
                              "see_m2": see.astype(np.float32) * (z * z)})
    if ordner:
        os.makedirs(ordner, exist_ok=True)
        for n in namen:
            tmp = os.path.join(ordner, n + ".tmp.npy")
            np.save(tmp, o[n])
            os.replace(tmp, os.path.join(ordner, n + ".npy"))
    return o


# ======================================================================================================================
# Inseln
# ======================================================================================================================
def landmassen(welt, R):
    """Zusammenhaengende Landmassen (8-m-Raster). Rueckgabe (label8, liste), label 0 = Meer."""
    k = int(R["insel"]["raster_m"] / welt.zelle_m)
    ny, nx = welt.ny // k * k, welt.nx // k * k
    land = (~welt.meer[:ny, :nx]).reshape(ny // k, k, nx // k, k).mean(axis=(1, 3)) >= 0.5
    H, W = land.shape
    lab = np.zeros((H, W), np.int32)
    flach = land.reshape(-1)
    lf = lab.reshape(-1)
    liste = []
    n = 0
    for start in np.flatnonzero(flach):
        if lf[start]:
            continue
        n += 1
        lf[start] = n
        dq = collections.deque([int(start)])
        zellen = 0
        rand = False
        while dq:
            c = dq.popleft()
            zellen += 1
            i, j = divmod(c, W)
            if i == 0 or j == 0 or i == H - 1 or j == W - 1:
                rand = True
            for di in (-1, 0, 1):
                ii = i + di
                if ii < 0 or ii >= H:
                    continue
                for dj in (-1, 0, 1):
                    jj = j + dj
                    if jj < 0 or jj >= W:
                        continue
                    q = ii * W + jj
                    if flach[q] and not lf[q]:
                        lf[q] = n
                        dq.append(q)
        liste.append({"label": n, "zellen": zellen, "flaeche_km2": zellen * (k * welt.zelle_m) ** 2 / 1e6,
                      "beruehrt_weltrand": rand})
    # Hoehe, Mitte je Landmasse
    hk = welt.hoehe[:ny, :nx].reshape(H, k, W, k).max(axis=(1, 3))
    labs = lab.reshape(-1)
    hmax = np.full(n + 1, -1e9)
    np.maximum.at(hmax, labs, hk.reshape(-1))
    ii, jj = np.divmod(np.arange(H * W), W)
    cnt = np.bincount(labs, minlength=n + 1)
    si = np.bincount(labs, weights=ii, minlength=n + 1)
    sj = np.bincount(labs, weights=jj, minlength=n + 1)
    bk = welt.biom[:ny, :nx][k // 2::k, k // 2::k]
    for e in liste:
        L = e["label"]
        x, y = D.pixel_zu_m(si[L] / cnt[L], sj[L] / cnt[L], k * welt.zelle_m)
        e["mitte_cm"] = [int(round(x * 100)), int(round(y * 100))]
        e["hoehe_max_m"] = round(float(hmax[L]), 1)
        bc = np.bincount(bk[lab == L].astype(np.int64), minlength=256)
        top = [int(q) for q in np.argsort(-bc, kind="stable")[:3] if bc[q] > 0]
        e["biome"] = {D.biom_name(q): round(float(bc[q]) / max(float(bc.sum()), 1.0), 2) for q in top}
    liste.sort(key=lambda e: (-e["zellen"], e["label"]))
    haupt = liste[0]["label"] if liste else 0
    min_km2 = R["insel"]["min_flaeche_m2"] / 1e6
    nr = 0
    for e in liste:
        if e["label"] == haupt:
            e["id"] = "HAUPTLAND"
            e["art"] = "hauptland"
        elif e["flaeche_km2"] >= min_km2:
            nr += 1
            e["id"] = "INSEL_%02d" % nr
            e["art"] = "insel"
        else:
            e["id"] = None
            e["art"] = "klein"
    return lab, k, liste


def landmasse_bei(lab, k, liste, welt, x_m, y_m):
    i, j = welt.m_zu_ij(x_m, y_m)
    i8, j8 = min(i // k, lab.shape[0] - 1), min(j // k, lab.shape[1] - 1)
    L = int(lab[i8, j8])
    if L == 0:   # Lippe auf einer Meerzelle des 8-m-Rasters: naechste Landzelle im 5x5
        best = None
        for di in range(-2, 3):
            for dj in range(-2, 3):
                a, b = i8 + di, j8 + dj
                if 0 <= a < lab.shape[0] and 0 <= b < lab.shape[1] and lab[a, b]:
                    d = di * di + dj * dj
                    if best is None or d < best[0]:
                        best = (d, int(lab[a, b]))
        L = best[1] if best else 0
    for e in liste:
        if e["label"] == L:
            return e
    return None


# ======================================================================================================================
# Faelle sammeln
# ======================================================================================================================
def sammle_fluss_sim(fs):
    """Alle Gewaesser des Exports. Rueckgabe (gewaesser-Liste, faelle-Liste)."""
    pfade = sorted(glob.glob(os.path.join(fs, "gewaesser", "*", "fluss_sim.json")))
    pfade += sorted(glob.glob(os.path.join(fs, "sehens", "*", "*", "fluss_sim.json")))
    gew, faelle = [], []
    for pf in pfade:
        d = lese(pf)
        rel = os.path.relpath(pf, fs)
        for e in d.get("gewaesser", []):
            zfl = [{"gewaesser": z_.get("gewaesser"), "s_m": z_.get("s_m")} for z_ in e.get("zufluesse") or []]
            g = {"id": e["id"], "kategorie": e.get("kategorie"), "art": e.get("art"), "laenge_m": e.get("laenge_m"),
                 "anfang": e.get("anfang") or {}, "muendung": e.get("muendung") or {}, "zufluesse": zfl,
                 "datei": rel, "n_faelle": len(e.get("faelle") or [])}
            sp = ((e.get("water_body") or {}).get("spline") or {})
            if sp.get("punkte") and sp.get("punkte_s_m"):
                g["xy"] = np.asarray(sp["punkte"], float)[:, :2] / 100.0
                g["z"] = np.asarray(sp["punkte"], float)[:, 2] / 100.0
                g["s"] = np.asarray(sp["punkte_s_m"], float)
            gew.append(g)
            for f in e.get("faelle") or []:
                faelle.append({"quelle": "fluss_sim", "datei": rel, "gewaesser": e["id"],
                               "kategorie": e.get("kategorie"), "fall": f})
    return gew, faelle


def sammle_sehens(sehens):
    """Sehens-Wasserfaelle (orte.json wasser typ wasserfall) mit Baechen/Seen ihres Orts."""
    out = []
    for biom in D.BIOME:
        pf = os.path.join(sehens, biom, "orte.json")
        if not os.path.exists(pf):
            continue
        d = lese(pf)
        for o in d.get("orte", []):
            ws = o.get("wasser") or []
            for w in ws:
                if w.get("typ") == "wasserfall":
                    out.append({"quelle": "sehens", "datei": "%s/orte.json" % biom, "ort": o["id"], "biom_ort": biom,
                                "w": w, "wasser_ort": ws})
    return out


def welt_wasserfaelle(welt):
    breite = {}
    if os.path.exists(WASSER_FX_PLAN):
        for e in lese(WASSER_FX_PLAN).get("effekte", []):
            if e.get("rolle") == "fall" and str(e.get("ziel", "")).startswith("WF_"):
                b = ((e.get("user_parameter") or {}).get("wunsch") or {}).get("Breite_m")
                if b:
                    breite[e["ziel"]] = float(b)
    out = []
    for w in (welt.wasser_welt or {}).get("wasserfaelle", []) or []:
        k = w.get("kante_xz")
        if not k:
            continue
        out.append({"quelle": "wasser_welt", "id": w["WasserfallID"], "parent": w.get("ParentWaterBodyID"),
                    "kachel": w.get("kachel"), "x": float(k[0]), "y": float(k[1]),
                    "z": float(w.get("kante_spiegel_y") or 0.0), "fall_m": float(w.get("fallhoehe_gemessen_m")
                                                                             or w.get("fallhoehe_m") or 0.0),
                    "breite_m": breite.get(w["WasserfallID"])})
    return out


def bach_laenge(P):
    P = np.asarray(P, float)[:, :2]
    return float(np.hypot(*np.diff(P, axis=0).T).sum()) if len(P) > 1 else 0.0


def sehens_oberhalb(rec_s, kx, ky, kz):
    """Wasser oberhalb einer Sehens-Kante: Bach, der an der Kante endet (Laenge, Quelle?), oder See darueber."""
    best = None
    for w in rec_s["wasser_ort"]:
        if w.get("typ") == "bach" and w.get("punkte_cm"):
            P = np.asarray(w["punkte_cm"], float)
            d_ende = math.hypot(P[-1, 0] / 100 - kx, P[-1, 1] / 100 - ky)
            # Bach fliesst zur Kante: Ende nah oder Kante auf dem Bach (Lauf ueber die Kante hinweg)
            dd = np.hypot(P[:, 0] / 100 - kx, P[:, 1] / 100 - ky)
            k = int(np.argmin(dd))
            if dd[k] <= 15.0 and (d_ende <= 15.0 or k > 0):
                L = bach_laenge(P[:k + 1]) / 100.0
                if best is None or L > best["laenge_m"]:
                    best = {"art": "bach", "id": w.get("id"), "laenge_m": L, "quelle_geplant": bool(w.get("quelle")),
                            "abfluss_von": w.get("abfluss_von")}
    for w in rec_s["wasser_ort"]:
        if w.get("typ") == "see" and w.get("umriss_cm"):
            U = np.asarray(w["umriss_cm"], float) / 100.0
            d = float(np.min(np.hypot(U[:, 0] - kx, U[:, 1] - ky)))
            sp = float(w.get("spiegel_cm", 0)) / 100.0
            if d <= 15.0 and sp >= kz - 0.5:
                if best is None:
                    best = {"art": "see", "id": w.get("id"), "laenge_m": 0.0, "quelle_geplant": False}
                best["see_oberhalb"] = w.get("id")
    return best


# ======================================================================================================================
# Gelaende je Fall
# ======================================================================================================================
class Analyse:
    def __init__(self, welt, gel, o, R):
        self.welt, self.gel, self.o, self.R = welt, gel, o, R
        self.z = welt.zelle_m
        self.akk = gel.akkumulation
        self.rec = gel.empfaenger
        self.hz = gel.haupt_zufluss

    def schnappen(self, x, y):
        """Lippe -> D8-Zelle mit groesster Akkumulation im Radius (nicht tiefer als Gelaende - Toleranz)."""
        w = self.welt
        L = self.R["lippe"]
        i, j = w.m_zu_ij(x, y)
        h0 = float(w.hoehe[i, j])
        rp = int(math.ceil(L["radius_m"] / self.z))
        i0, i1 = max(i - rp, 0), min(i + rp + 1, w.ny)
        j0, j1 = max(j - rp, 0), min(j + rp + 1, w.nx)
        I, J = np.meshgrid(np.arange(i0, i1), np.arange(j0, j1), indexing="ij")
        d = np.hypot(I - i, J - j) * self.z
        ok = (d <= L["radius_m"]) & (w.hoehe[i0:i1, j0:j1] >= h0 - L["hoehen_toleranz_m"]) & ~w.meer[i0:i1, j0:j1]
        a = np.where(ok, self.akk[i0:i1, j0:j1], -1.0)
        k = int(np.argmax(a))
        if a.reshape(-1)[k] < 0:
            return i * w.nx + j
        return int(I.reshape(-1)[k]) * w.nx + int(J.reshape(-1)[k])

    def aufwaerts(self, c, max_m):
        """Haupt-Zufluss-Linie aufwaerts: Liste (idx, s_m)."""
        nx = self.welt.nx
        pfad = [(c, 0.0)]
        s = 0.0
        while s < max_m:
            n = int(self.hz[c])
            if n < 0:
                break
            d = abs(n - c)
            s += self.z * (1.4142135 if d in (nx - 1, nx + 1) else 1.0)
            c = n
            pfad.append((c, s))
        return pfad

    def wasser_oberhalb_raster(self, c, max_m=600.0, luecke_m=6.0):
        """Laenge (m) der Welt-Wasserflaeche (wasser_2m > 0) entlang der Tiefenlinie aufwaerts ab der Lippe."""
        wasser = (self.welt.wasser > 0).reshape(-1)
        letzt = 0.0
        for q, s in self.aufwaerts(c, max_m):
            if wasser[q]:
                letzt = s
            elif s - letzt > luecke_m:
                break
        return letzt

    def steilster_anstieg(self, c, max_m, flach=0.1, min_m=20.0):
        """Steilster Anstieg bis zum Kamm: Ende an einer Kuppe oder wo es flach wird (Steigung < flach nach min_m)."""
        w = self.welt
        nx = w.nx
        h = w.hoehe.reshape(-1)
        pfad = [(c, 0.0)]
        s = 0.0
        while s < max_m:
            i, j = divmod(c, nx)
            best = None
            for di, dj in G.RICHTUNGEN:
                ii, jj = i + di, j + dj
                if 0 <= ii < w.ny and 0 <= jj < w.nx:
                    q = ii * nx + jj
                    dist = self.z * (1.4142135 if di and dj else 1.0)
                    g = (h[q] - h[c]) / dist
                    if g > 0 and (best is None or g > best[0]):
                        best = (g, q, dist)
            if best is None or (s >= min_m and best[0] < flach):
                break
            c = best[1]
            s += best[2]
            pfad.append((c, s))
        return pfad

    def rinne(self, c):
        """Sichtbare Gelaende-Rinne oberhalb der Lippe (TPI entlang der Haupt-Zufluss-Linie)."""
        Rr = self.R["rinne"]
        pfad = [p for p in self.aufwaerts(c, Rr["bis_m"]) if p[1] >= Rr["von_m"]]
        if len(pfad) < 3:
            return {"rinne": False, "tpi_median_m": None, "flaeche_median_m2": None, "laenge_m": 0.0}
        w = self.welt
        idx = np.array([p[0] for p in pfad])
        I, J = np.divmod(idx, w.nx)
        rp = int(round(Rr["tpi_radius_m"] / self.z))
        i0, i1 = max(int(I.min()) - rp - 1, 0), min(int(I.max()) + rp + 2, w.ny)
        j0, j1 = max(int(J.min()) - rp - 1, 0), min(int(J.max()) + rp + 2, w.nx)
        hw = w.hoehe[i0:i1, j0:j1].astype(np.float64)
        tpi = hw - G.box_mittel(hw, rp)
        t = tpi[I - i0, J - j0]
        a = np.asarray(self.akk).reshape(-1)[idx]
        tm, am = float(np.median(t)), float(np.median(a))
        return {"rinne": bool(tm <= Rr["tpi_max_m"] and am >= Rr["flaeche_min_m2"]), "tpi_median_m": round(tm, 2),
                "flaeche_median_m2": round(am), "laenge_m": round(pfad[-1][1], 1)}

    def oberlauf_vorschlag(self, c, eigen_m=0.0):
        """Punkte (cm) entlang der Tiefenlinie aufwaerts bis zur Mulde (oder bis zu vorhandenem Wasser);
        ist die Tiefenlinie zu kurz: steilster Anstieg bis zum Kamm."""
        O = self.R["oberlauf"]
        w = self.welt
        akk = np.asarray(self.akk).reshape(-1)
        wasser = (w.wasser > 0).reshape(-1)
        pfad = []
        ende = "max_laenge"
        for q, s in self.aufwaerts(c, O["max_laenge_m"]):
            pfad.append((q, s))
            if s > eigen_m + 10.0 and wasser[q]:
                ende = "anschluss_wasser"
                break
            if akk[q] < O["mulde_m2"]:
                ende = "mulde"
                break
        if pfad[-1][1] < O["kamm_wenn_kuerzer_m"]:
            pfad = self.steilster_anstieg(c, O["kamm_max_m"], O["kamm_flach"])
            ende = "kamm" if pfad[-1][1] < O["kamm_max_m"] - 2 * self.z else "anstieg_max"
        if ende not in ("kamm", "anstieg_max") and pfad[-1][1] <= eigen_m + O["punkt_abstand_m"]:
            # vorhandenes Wasser reicht schon bis zur Quellmulde: kein Oberlauf moeglich, nur Menge/Quelle
            return {"ende": "wasser_reicht_bis_mulde", "ab_lippe_m": round(eigen_m, 1), "laenge_m": 0.0,
                    "punkte_cm": [], "hoehe_gewinn_m": 0.0, "flaeche_am_ende_m2": round(float(akk[pfad[-1][0]]))}
        ab = eigen_m if ende not in ("kamm", "anstieg_max") else 0.0
        punkte = []
        letzt = -1e9
        for k, (q, s) in enumerate(pfad):
            if s < ab - 1e-6:
                continue
            if s - letzt >= O["punkt_abstand_m"] or k == len(pfad) - 1:
                i, j = divmod(q, w.nx)
                x, y = w.ij_zu_m(i, j)
                punkte.append([int(round(float(x) * 100)), int(round(float(y) * 100)),
                               int(round(float(w.hoehe[i, j]) * 100))])
                letzt = s
        return {"ende": ende, "ab_lippe_m": round(ab, 1), "laenge_m": round(pfad[-1][1] - ab, 1), "punkte_cm": punkte,
                "hoehe_gewinn_m": round((punkte[-1][2] - punkte[0][2]) / 100.0, 1) if punkte else 0.0,
                "flaeche_am_ende_m2": round(float(akk[pfad[-1][0]]))}


# ======================================================================================================================
# Bewertung und Empfehlung
# ======================================================================================================================
def poleni_q(b, h, mu):
    return 2.0 / 3.0 * mu * math.sqrt(2 * 9.81) * b * h ** 1.5


def klasse_q(q, R):
    k = R["fall"]["klassen_m3s"][0][1]
    for grenze, name in R["fall"]["klassen_m3s"]:
        if q >= grenze:
            k = name
    return k


KARST_BIOME = ("dschungel", "canyon", "elfenwald", "heide")      # Kalk/Karst-Optik moeglich (Sinter, Karstaufstoss)
SCHNEE_BIOME = ("gletscher", "frost", "fjord", "tundra")


def bewerten(f, R):
    """Zwei Achsen: Herkunft sichtbar (Quellmerkmal oder Wasser oberhalb) und Menge (V = Angebot/Bedarf)."""
    B = R["bewertung"]
    V = f["verhaeltnis"]
    qm = bool(f["quellmerkmale"])
    herkunft = qm or f["wasser_oberhalb_m"] >= B["wasser_oberhalb_min_m"]
    f["herkunft_sichtbar"] = herkunft
    f["menge"] = "passt" if V >= B["v_plausibel"] else ("knapp" if V >= B["v_nichts"] else "viel_zu_wenig")
    if (not herkunft and V < B["v_plausibel"]) or \
            (not qm and V < B["v_nichts"] and f["wasser_oberhalb_m"] < B["nichts_kurz_m"]):
        return "aus_dem_nichts"
    if V >= B["v_plausibel"] and herkunft:
        return "plausibel"
    return "fragwuerdig"


def empfehlen(f, R):
    """Hauptmassnahme (erste) + Zusatz je Fall (Kennungen wie im Bericht, Texte in MASSNAHME_TEXT)."""
    m, zusatz = [], []
    biom = f["biom"]
    B = R["bewertung"]
    V = f["verhaeltnis"]
    bew = f["bewertung"]
    gipfel = (f["gipfel_ueber_lippe_m"] or 0.0) >= R["gipfel"]["nebel_ab_m"]
    schnee = biom in SCHNEE_BIOME or f["schnee_m2"] >= R["quellmerkmal"]["schnee_min_m2"]
    # noetige Vergroesserung des Einzugsgebiets mit Spielfaktor (V >= v_plausibel reicht)
    fak = f["flaeche_noetig_faktor"] * B["v_plausibel"] if f["flaeche_noetig_faktor"] is not None else None
    formbar = fak is not None and fak <= 3.0
    ol = f.get("oberlauf")
    if bew == "plausibel":
        m.append("keine_aenderung")
    else:
        kurz = f["wasser_oberhalb_m"] < B["wasser_oberhalb_min_m"] and not f["quellmerkmale"]
        if ol and ol["ende"] in ("mulde", "max_laenge", "anschluss_wasser") and ol["laenge_m"] >= 40:
            m.append("oberlauf_ergaenzen")
            if not f["rinne"]["rinne"]:
                zusatz.append("einzugsgebiet_formen")
        elif kurz:
            m.append("quellaustritt_felswand")
        if V < B["v_plausibel"]:
            if schnee:
                (zusatz if m else m).append("schneefeld_oberhalb")
            if formbar:
                (zusatz if m else m).append("einzugsgebiet_formen")
            if f["relief_flach_oben"] and not schnee:
                (zusatz if m else m).append("karsee_moor_oberhalb")
            (zusatz if m else m).append("fall_verkleinern")
        if not m:
            m.append("quellmerkmal_zeigen")
        if biom in KARST_BIOME and "quellaustritt_felswand" in m:
            zusatz.append("sinter_kalktuff")
    if gipfel and (f["insel"] or biom in ("dschungel", "elfenwald", "kueste", "lava", "bergwald", "fjord")) \
            and bew != "plausibel":
        zusatz.append("nebel_am_gipfel")
    if bew != "plausibel":
        zusatz.append("nassstreifen_moos")
    out = []
    for k in m + zusatz:
        if k not in out:
            out.append(k)
    return out


MASSNAHME_TEXT = {
    "keine_aenderung": "Herkunft passt - nichts tun",
    "quellmerkmal_zeigen": "Herkunft sichtbar machen (Quelle/Bach oberhalb in den Blick ruecken)",
    "oberlauf_ergaenzen": "Oberlauf ergaenzen: Bach-Spline entlang der Vorschlagspunkte bis in die Mulde",
    "quellaustritt_felswand": "Quellaustritt in der Felswand (Schicht-/Spaltenquelle): Wasser tritt sichtbar aus einem Band/Spalt aus",
    "einzugsgebiet_formen": "Gelaende-Einzugsgebiet vergroessern: Kar/Rinne ueber der Kante formen",
    "schneefeld_oberhalb": "Schneefeld/Gletscherrest oberhalb (Schmelzwasser)",
    "karsee_moor_oberhalb": "Karsee oder Moor oberhalb (Speicher, Ueberlauf)",
    "fall_verkleinern": "Fall verkleinern (Schleier/Faeden statt Vorhang) oder versetzen",
    "sinter_kalktuff": "Sinter/Kalktuff an der Austrittsstelle (Decal/Lage)",
    "nebel_am_gipfel": "Nebel/Wolkenkappe am Gipfel (lokaler Nebel / Volumetric Cloud)",
    "nassstreifen_moos": "Nass- und Moosstreifen entlang Quelllinie und Fallbahn (Decal/Lage)",
}


# ======================================================================================================================
# Hauptablauf
# ======================================================================================================================
def fall_eintrag(an, R, fid, quelle, x, y, z_lippe, fall_m, breite_m, breite_quelle, wasser_oberhalb_m,
                 wasser_info, extra, inseln):
    welt = an.welt
    o = an.o
    c = an.schnappen(x, y)
    i, j = divmod(c, welt.nx)
    xs, ys = welt.ij_zu_m(i, j)
    akk = float(np.asarray(an.akk)[i, j])
    q = float(o["q_m3a"][i, j]) / SEK_JAHR
    schnee = float(o["schnee_m2"][i, j])
    see = float(o["see_m2"][i, j])
    max_h = float(o["max_h"][i, j])
    l_max = float(o["l_max"][i, j])
    h_l = float(welt.hoehe[i, j])
    biom = D.biom_name(welt.biom[i, j])
    if biom == "meer":
        biom = welt.biom_bei_m(x, y)
    F = R["fall"]
    b = breite_m if breite_m else F["breite_standard_m"]
    q_bedarf = poleni_q(b, F["h_vorhang_m"], F["mu"])
    q_schleier = poleni_q(b, F["h_schleier_m"], F["mu"])
    V = q / q_bedarf if q_bedarf > 0 else 0.0
    pc = R["niederschlag_mm_a"].get(biom, 1000) * R["abflussbeiwert"].get(biom, 0.5) / 1000.0
    flaeche_noetig = q_bedarf * SEK_JAHR / pc if pc > 0 else None
    rin = an.rinne(c)
    w_raster = an.wasser_oberhalb_raster(c)
    w_plan = float(wasser_oberhalb_m or 0.0)
    wasser_oberhalb_m = max(w_plan, w_raster)
    lm = landmasse_bei(*inseln, welt, x, y)
    qm = []
    if see >= R["quellmerkmal"]["see_min_m2"]:
        qm.append("see_im_einzugsgebiet")
    if schnee >= R["quellmerkmal"]["schnee_min_m2"]:
        qm.append("schnee_eis_im_einzugsgebiet")
    if wasser_info and wasser_info.get("see_oberhalb"):
        qm.append("see_oberhalb_geplant")
    if wasser_info and wasser_info.get("quelle_geplant"):
        qm.append("quelle_geplant")
    if wasser_info and wasser_info.get("anfang_art") in ("see", "topf"):
        qm.append("gewaesser_beginnt_an_see")
    # Relief oberhalb flach? (Mittel der Hoehe ueber der Lippe auf 150 m Tiefenlinie gering)
    pf = an.aufwaerts(c, 150.0)
    dh = float(welt.hoehe.reshape(-1)[pf[-1][0]]) - h_l if pf else 0.0
    flach = pf[-1][1] >= 60 and dh / max(pf[-1][1], 1.0) < 0.12
    f = {"id": fid, "quelle": quelle,
         "lage": {"feld": D.feld_von_m(x, y), "lippe_cm": [int(round(x * 100)), int(round(y * 100)),
                                                           int(round(z_lippe * 100))],
                  "lippe_d8_cm": [int(round(float(xs) * 100)), int(round(float(ys) * 100)), int(round(h_l * 100))]},
         "fall_m": r(fall_m), "breite_m": r(b), "breite_quelle": breite_quelle if breite_m else "standard (unbekannt)",
         "biom": biom,
         "insel": bool(lm and lm["art"] == "insel"), "landmasse": lm["id"] if lm else None,
         "einzugsgebiet_m2": round(akk), "einzugsgebiet_ha": r(akk / 1e4, 2),
         "abfluss_mittel_l_s": r(q * 1000, 2), "abfluss_klasse": klasse_q(q, R),
         "bedarf_vorhang_l_s": r(q_bedarf * 1000, 1), "bedarf_schleier_l_s": r(q_schleier * 1000, 2),
         "verhaeltnis": round(V, 3),
         "flaeche_noetig_m2": round(flaeche_noetig) if flaeche_noetig else None,
         "flaeche_noetig_faktor": r(flaeche_noetig / max(akk, 1.0), 1) if flaeche_noetig else None,
         "breite_passend_m": r(q / poleni_q(1.0, F["h_vorhang_m"], F["mu"]), 2),
         "wasser_oberhalb_m": r(wasser_oberhalb_m), "wasser_oberhalb_plan_m": r(w_plan),
         "wasser_oberhalb_welt_m": r(w_raster), "wasser_oberhalb": wasser_info,
         "fliessweg_gelaende_m": r(l_max), "gipfel_m": r(max_h), "gipfel_ueber_lippe_m": r(max_h - h_l),
         "schnee_m2": round(schnee), "see_m2": round(see),
         "rinne": rin, "quellmerkmale": qm, "relief_flach_oben": bool(flach)}
    f.update(extra)
    f["bewertung"] = bewerten(f, R)
    f["oberlauf"] = None
    if f["bewertung"] != "plausibel" and not f["quellmerkmale"]:
        f["oberlauf"] = an.oberlauf_vorschlag(c, f["wasser_oberhalb_m"])
    f["massnahmen"] = empfehlen(f, R)
    f["empfehlung"] = MASSNAHME_TEXT[f["massnahmen"][0]]
    return f


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--daten2m", default=None)
    ap.add_argument("--daten1m", default=None)
    ap.add_argument("--cache", default=None)
    ap.add_argument("--fs", required=True, help="Ausgabe von fluss_sim_export.py")
    ap.add_argument("--sehens", required=True, help="Ausgaben der Sehens-Planer (<biom>/orte.json)")
    ap.add_argument("--regeln", default=REGELN_STANDARD)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--bild", action="store_true", help="Uebersichtskarte faelle_herkunft.png")
    a = ap.parse_args(argv)
    R = lese(a.regeln)
    welt = D.lade(daten2m=a.daten2m, daten1m=a.daten1m, pfade=False)
    log(welt.info())
    gel = G.Gelaende(welt, cache=a.cache)
    seen = alle_seen(welt, a.sehens)
    log("Seen/Teiche als Quellmerkmal: %d" % len(seen))
    o = welt_raster(welt, gel, R, seen)
    with Uhr("Landmassen"):
        inseln = landmassen(welt, R)
    lab, k8, liste = inseln
    log("Landmassen: %d (Inseln %d)" % (len(liste), sum(1 for e in liste if e["art"] == "insel")))
    an = Analyse(welt, gel, o, R)

    gew, fs_faelle = sammle_fluss_sim(a.fs)
    gew_by = {g["id"]: g for g in gew}
    seh = sammle_sehens(a.sehens)
    wf = welt_wasserfaelle(welt)
    log("Eingaben: %d Gewaesser, %d Faelle (fluss_sim, %d mit Vorhang), %d Sehens-Wasserfaelle, %d Welt-Wasserfaelle"
        % (len(gew), len(fs_faelle), sum(1 for f in fs_faelle if f["fall"].get("vorhang")), len(seh), len(wf)))

    # Sehens-Baeche mit geplanter Quelle (orte.json bach.quelle = true) -> Gewaesser SW_<ort>_<bach>
    seh_quelle = set()
    for biom in D.BIOME:
        pf_ = os.path.join(a.sehens, biom, "orte.json")
        if os.path.exists(pf_):
            for o_ in lese(pf_).get("orte", []):
                for w_ in o_.get("wasser") or []:
                    if w_.get("typ") == "bach" and w_.get("quelle"):
                        seh_quelle.add("SW_%s_%s" % (o_["id"], w_.get("id")))

    def oberhalb_fs(e):
        f = e["fall"]
        g = gew_by[e["gewaesser"]]
        s = float(f.get("s_lippe_m") or 0.0)
        zfl = [z_ for z_ in g["zufluesse"] if z_.get("s_m") is not None and z_["s_m"] < s]
        zl = 0.0
        for z_ in zfl:
            zl = max(zl, float((gew_by.get(z_["gewaesser"]) or {}).get("laenge_m") or 0.0))
        return s, {"art": "gewaesser", "id": g["id"], "s_lippe_m": r(s), "anfang_art": g["anfang"].get("art"),
                   "anfang_ziel": g["anfang"].get("ziel"), "zufluesse_oberhalb": len(zfl),
                   "laengster_zufluss_m": r(zl), "quelle_geplant": g["id"] in seh_quelle}

    def gewaesser_bei(x, y, tol_m, bevorzugt=None, z=None, dz_m=4.0):
        """Naechstes Gewaesser (Spline) an einem Punkt: (gewaesser, s_m, abstand_m) oder None."""
        best = None
        for g in gew:
            if "xy" not in g:
                continue
            d = np.hypot(g["xy"][:, 0] - x, g["xy"][:, 1] - y)
            if z is not None:
                d = np.where(np.abs(g["z"] - z) <= dz_m, d, np.inf)
            k = int(np.argmin(d))
            if d[k] > tol_m:
                continue
            key = (0 if bevorzugt and g["id"] == bevorzugt else 1, round(float(d[k]), 2), g["id"])
            if best is None or key < best[0]:
                best = (key, g, float(g["s"][k]), float(d[k]))
        return None if best is None else best[1:]

    def oberhalb_gw(g, s):
        zfl = [z_ for z_ in g["zufluesse"] if z_.get("s_m") is not None and z_["s_m"] < s]
        zl = max([float((gew_by.get(z_["gewaesser"]) or {}).get("laenge_m") or 0.0) for z_ in zfl] or [0.0])
        return {"art": "gewaesser", "id": g["id"], "s_lippe_m": r(s), "anfang_art": g["anfang"].get("art"),
                "anfang_ziel": g["anfang"].get("ziel"), "zufluesse_oberhalb": len(zfl), "laengster_zufluss_m": r(zl),
                "quelle_geplant": g["id"] in seh_quelle}

    eintraege = []
    benutzt = set()
    # 1) Welt-Wasserfaelle (wasser_welt.json), mit Gewaessern, die dort muenden
    for w in wf:
        mu = sorted(g["id"] for g in gew if (g["muendung"] or {}).get("art") == "wasserfall"
                    and g["muendung"].get("ziel") == w["id"])
        an_ = sorted(g["id"] for g in gew if (g["anfang"] or {}).get("art") == "wasserfall"
                     and g["anfang"].get("ziel") == w["id"])
        gb = gewaesser_bei(w["x"], w["y"], 25.0, bevorzugt=w["parent"], z=w["z"], dz_m=6.0)
        wo = 0.0
        info = {"art": "fluss", "id": w["parent"], "hinweis": "kein Gewaesser des Exports an der Kante"}
        if gb:
            wo = gb[1]
            info = oberhalb_gw(gb[0], gb[1])
            info["abstand_spline_m"] = r(gb[2])
        info.update({"muenden_hier": mu, "beginnen_hier": an_})
        nahe = [e for e in fs_faelle if e["fall"].get("vorhang") and math.hypot(
            e["fall"]["lippe_cm"][0] / 100 - w["x"], e["fall"]["lippe_cm"][1] / 100 - w["y"]) <= 30.0]
        for e in nahe:
            benutzt.add(e["fall"]["id"])
        extra = {"art": "welt_wasserfall", "gewaesser": w["parent"], "kachel": w["kachel"],
                 "fluss_sim_faelle": sorted(e["fall"]["id"] for e in nahe)}
        eintraege.append(fall_eintrag(an, R, w["id"], "wasser_welt.json", w["x"], w["y"], w["z"], w["fall_m"],
                                      w["breite_m"], "wasser_fx/plan.json (Breite_m)", wo, info, extra, inseln))
    # 2) Sehens-Wasserfaelle
    for e in seh:
        w = e["w"]
        K = np.asarray(w["kante_cm"], float)
        kx, ky, kz = float(K[:, 0].mean()) / 100, float(K[:, 1].mean()) / 100, float(K[0, 2]) / 100
        ob = sehens_oberhalb(e, kx, ky, kz)
        # Bach-Stufen desselben Orts im fluss_sim (gleiche Kante) nicht doppelt
        nahe = [x for x in fs_faelle if x["fall"].get("vorhang") and math.hypot(
            x["fall"]["lippe_cm"][0] / 100 - kx, x["fall"]["lippe_cm"][1] / 100 - ky) <= 10.0]
        for x in nahe:
            benutzt.add(x["fall"]["id"])
        wo = 0.0
        if ob and ob["art"] == "bach":
            wo = ob["laenge_m"]
        gb = gewaesser_bei(kx, ky, 8.0, z=kz)
        if gb and gb[1] > wo:
            inf_ = oberhalb_gw(gb[0], gb[1])
            inf_["abstand_spline_m"] = r(gb[2])
            if ob:
                for k_ in ("see_oberhalb", "quelle_geplant"):
                    if ob.get(k_):
                        inf_[k_] = ob[k_]
            wo, ob = gb[1], inf_
        fid = "%s/%s" % (e["ort"], w.get("id"))
        extra = {"art": "sehens_wasserfall", "ort": e["ort"], "gewaesser": None,
                 "fluss_sim_faelle": sorted(x["fall"]["id"] for x in nahe), "hinweis_planer": w.get("hinweis")}
        eintraege.append(fall_eintrag(an, R, fid, "sehens/%s" % e["datei"], kx, ky, kz, w.get("fallhoehe_m"),
                                      float(w.get("breite_cm", 0)) / 100.0 or None, "orte.json breite_cm", wo,
                                      ob, extra, inseln))
    # 3) fluss_sim-Faelle mit Vorhang
    for e in sorted(fs_faelle, key=lambda q: q["fall"]["id"]):
        f = e["fall"]
        if not f.get("vorhang") or f["id"] in benutzt:
            continue
        s, info = oberhalb_fs(e)
        b = f.get("strahl_breite_m") or f.get("lippe_breite_m")
        bq = "fluss_sim strahl_breite_m (%s)" % f.get("strahl_quelle") if f.get("strahl_breite_m") else \
            "fluss_sim lippe_breite_m"
        extra = {"art": "vorhang_fall", "gewaesser": e["gewaesser"], "kategorie": e["kategorie"],
                 "fall_art": f.get("art"), "vorhang_grund": f.get("vorhang_grund"), "fluss_sim_faelle": [f["id"]]}
        L = f["lippe_cm"]
        eintraege.append(fall_eintrag(an, R, f["id"], "fluss_sim/%s" % e["datei"], L[0] / 100, L[1] / 100, L[2] / 100,
                                      f.get("fall_m"), b, bq, s, info, extra, inseln))

    # Gewaesser je Fall gruppieren (Kaskaden: ein Gewaesser mit vielen Vorhaengen)
    # Nebenstatistik: alle fluss_sim-Faelle (auch ohne Vorhang), deren Gewaesser-Quelle kurz oberhalb liegt
    kurz = R["bewertung"]["quelle_kurz_m"]
    alle_kurz = []
    for e in fs_faelle:
        g = gew_by[e["gewaesser"]]
        s = float(e["fall"].get("s_lippe_m") or 0.0)
        if g["anfang"].get("art") == "quelle" and s < kurz:
            alle_kurz.append({"fall": e["fall"]["id"], "gewaesser": g["id"], "s_lippe_m": r(s),
                              "fall_m": r(e["fall"].get("fall_m")), "vorhang": bool(e["fall"].get("vorhang"))})
    alle_kurz.sort(key=lambda q: q["fall"])

    zaehl = collections.Counter(f["bewertung"] for f in eintraege)
    je_art = collections.defaultdict(collections.Counter)
    je_biom = collections.defaultdict(collections.Counter)
    massn = collections.Counter()
    for f in eintraege:
        je_art[f["art"]][f["bewertung"]] += 1
        je_biom[f["biom"]][f["bewertung"]] += 1
        massn[f["massnahmen"][0]] += 1
    gew_auswertung = []
    for gid in sorted({f["gewaesser"] for f in eintraege if f.get("gewaesser")}):
        fs_ = [f for f in eintraege if f.get("gewaesser") == gid]
        g = gew_by.get(gid) or {}
        gew_auswertung.append({"gewaesser": gid, "faelle": len(fs_),
                               "bewertung": dict(collections.Counter(f["bewertung"] for f in fs_)),
                               "anfang": (g.get("anfang") or {}).get("art"),
                               "muendung": (g.get("muendung") or {}).get("art"),
                               "einzugsgebiet_max_ha": max(f["einzugsgebiet_ha"] for f in fs_),
                               "oberster_fall": min(fs_, key=lambda q: q["wasser_oberhalb_m"])["id"]})
    zus = {"faelle": len(eintraege), "bewertung": {k: zaehl.get(k, 0) for k in
                                                   ("plausibel", "fragwuerdig", "aus_dem_nichts")},
           "je_art": {k: dict(v) for k, v in sorted(je_art.items())},
           "je_biom": {k: dict(v) for k, v in sorted(je_biom.items())},
           "hauptmassnahme": dict(sorted(massn.items())),
           "auf_inseln": sum(1 for f in eintraege if f["insel"]),
           "ohne_wasser_oberhalb": sum(1 for f in eintraege if f["wasser_oberhalb_m"] < kurz),
           "ohne_sichtbare_herkunft": sum(1 for f in eintraege if not f["herkunft_sichtbar"]),
           "mit_rinne": sum(1 for f in eintraege if f["rinne"]["rinne"]),
           "eingaben": {"gewaesser": len(gew), "faelle_fluss_sim": len(fs_faelle),
                        "faelle_vorhang": sum(1 for f in fs_faelle if f["fall"].get("vorhang")),
                        "sehens_wasserfaelle": len(seh), "welt_wasserfaelle": len(wf),
                        "muendung_wasserfall": sorted(g["id"] for g in gew
                                                      if (g["muendung"] or {}).get("art") == "wasserfall"),
                        "anfang_wasserfall": sorted(g["id"] for g in gew
                                                    if (g["anfang"] or {}).get("art") == "wasserfall")},
           "alle_faelle_quelle_kurz_oberhalb": {"anzahl": len(alle_kurz),
                                                "davon_vorhang": sum(1 for q in alle_kurz if q["vorhang"])}}
    out = {"format": "wasserherkunft_v1", "version": VERSION, "stand": R["stand"], "regeln_version": R["version"],
           "daten": "2m" if not a.daten1m else "1m", "erzeugt_von": "recherche/antworten/skripte/wasserherkunft/wasserherkunft.py",
           "hinweis": "Vorschlagsdaten (Auftrag 17). Nichts davon ist in einen Planer eingebaut. Einheiten: cm fuer Lagen, "
                      "m/m2/l/s sonst. Bewertung: verhaeltnis = mittlerer Abfluss / Bedarf eines geschlossenen Vorhangs "
                      "(Poleni, h = %.0f mm)." % (R["fall"]["h_vorhang_m"] * 1000),
           "zusammenfassung": zus,
           "massnahmen_text": MASSNAHME_TEXT,
           "landmassen": [{k_: v for k_, v in e.items() if k_ not in ("label", "zellen")} for e in liste
                          if e["art"] != "klein"],
           "landmassen_klein": sum(1 for e in liste if e["art"] == "klein"),
           "gewaesser": gew_auswertung,
           "faelle": eintraege,
           "faelle_quelle_kurz_oberhalb": alle_kurz}
    os.makedirs(a.aus, exist_ok=True)
    pf = os.path.join(a.aus, "faelle_herkunft.json")
    with open(pf, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=False)
        fh.write("\n")
    log("geschrieben: %s (%d Faelle: %s)" % (pf, len(eintraege), dict(zus["bewertung"])))
    if a.bild:
        bild(welt, eintraege, lab, k8, liste, os.path.join(a.aus, "faelle_herkunft.png"))
    return 0


def bild(welt, faelle, lab, k8, liste, pf):
    """Uebersichtskarte (8 m): Hoehe grau, Meer blau, Inseln getoent, Faelle farbig nach Bewertung."""
    from PIL import Image, ImageDraw
    k = k8
    H, W = lab.shape
    h = welt.hoehe[:H * k, :W * k].reshape(H, k, W, k).mean(axis=(1, 3))
    g = np.clip(h / max(float(h.max()), 1.0), 0, 1)
    rgb = np.stack([60 + 150 * g, 70 + 150 * g, 60 + 140 * g], -1)
    meer = lab == 0
    rgb[meer] = (40, 70, 120)
    art = {e["label"]: e["art"] for e in liste}
    lut = np.zeros(int(lab.max()) + 1, bool)
    for L_, a_ in art.items():
        lut[L_] = a_ == "insel"
    insel = lut[lab]
    rgb[insel & ~meer] = rgb[insel & ~meer] * 0.6 + np.array([200, 160, 60]) * 0.4
    img = Image.fromarray(rgb.astype(np.uint8))
    d = ImageDraw.Draw(img)
    for e in liste:
        if e["art"] != "klein" and e["flaeche_km2"] >= 0.25:
            i, j = D.m_zu_pixel(e["mitte_cm"][0] / 100.0, e["mitte_cm"][1] / 100.0, k * welt.zelle_m)
            d.text((float(j) - 25, float(i)), "%s %.1f km2" % (e["id"], e["flaeche_km2"]), fill=(255, 255, 255))
    farbe = {"plausibel": (40, 200, 60), "fragwuerdig": (250, 200, 30), "aus_dem_nichts": (230, 30, 30)}
    for f in sorted(faelle, key=lambda q: (("plausibel", "fragwuerdig", "aus_dem_nichts").index(q["bewertung"]), q["id"])):
        x, y = f["lage"]["lippe_cm"][0] / 100.0, f["lage"]["lippe_cm"][1] / 100.0
        i, j = D.m_zu_pixel(x, y, k * welt.zelle_m)
        rr = 6 if f["art"] != "vorhang_fall" else 4
        d.ellipse([float(j) - rr, float(i) - rr, float(j) + rr, float(i) + rr], fill=farbe[f["bewertung"]],
                  outline=(0, 0, 0))
    x0, y0 = W - 260, H - 80
    d.rectangle([x0, y0, W - 6, H - 6], fill=(255, 255, 255))
    for n, (t, c) in enumerate(farbe.items()):
        d.ellipse([x0 + 8, y0 + 8 + n * 20, x0 + 20, y0 + 20 + n * 20], fill=c, outline=(0, 0, 0))
        d.text((x0 + 28, y0 + 8 + n * 20), "%s (%d)" % (t, sum(1 for f in faelle if f["bewertung"] == t)),
               fill=(0, 0, 0))
    d.text((8, 8), "Auftrag 17 Wasserherkunft: gross = Sehens-/Welt-Wasserfall, klein = Vorhang-Fall (fluss_sim)",
           fill=(255, 255, 255))
    img.save(pf, optimize=True)
    log("Bild: %s" % pf)


if __name__ == "__main__":
    sys.exit(main())
