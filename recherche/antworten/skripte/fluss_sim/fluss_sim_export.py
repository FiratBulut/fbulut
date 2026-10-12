#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fluss_sim_export.py - Exporter fuer Entscheidung 16 (Shallow Water River fuer alle Baeche und Fluesse).

Liest NUR die vorhandenen Planer-Ausgaben (gefaelle_plan.py: <lauf>/plan.json + instanzen/, Sehens-Planer:
<biom>/orte.json + sw_<biom>/) und die Weltdaten. Aendert nichts an Planern, Stufen, Becken oder Gelaende
(13f-Regel: die Treppen der Sehens-Baeche bleiben exakt). Schreibt je Gewaesser eine fluss_sim.json:

  abschnitte        WaterBodyRiver-Abschnitte zwischen den Faellen: Splinepunkte (cm) mit RiverWidth, Depth,
                    WaterVelocityScalar (UWaterSplineMetadata), Punkttyp + Tangente, Anschluss an die Becken
  faelle            je Einzelabsturz >= fall_schwelle_m: oberer/unterer Abschnitt, Fallhoehe, Lippe, Strahlbreite,
                    Kaskadennetz-Bereich (Vorhang) und Effekte, dazu schaum_objekte (Aufprallteppich,
                    Schaumstrassen, Kehrwasser)
  wasser_kollision  alle festen Instanzen/Akteure im Wasser oder <= 1 m daneben, mit eindeutigem Verweis
  sim_bereiche      Back-Kacheln (je ein ShallowWaterRiver) mit Eingabe-Fingerabdruck

und global back_liste.json (Kachel, Fingerabdruck, Abschnitte) sowie zusammenfassung.json.

Aufruf (Cloud, 2 m):
  python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py \
      --gefaelle <scratch>/gef/alle --sehens <scratch>/sehens --daten2m recherche/vorlagen/daten/sehens --aus <scratch>/fs
Lokal (1 m):
  python -I .../fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle --sehens export/unreal/welt/sehens \
      --sw-ordner export/unreal/welt --daten1m export/unreal/welt --aus export/unreal/welt/fluss_sim
Optionen: --nur ID ... (Lauf-, Fluss- oder Ort-IDs), --ohne-fluesse, --ohne-roh, --regeln DATEI.

Deterministisch (keine Zeitstempel, sortierte Ausgabe, Zufall aus SHA-256 der IDs). Keine Unreal-Importe.
Die Funktion fingerabdruck() ist die Referenz fuer das lokale Werkzeug (Handaenderungen im Editor).
"""

import argparse
import glob
import hashlib
import json
import math
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
SKRIPTE = os.path.dirname(HIER)
sys.path.insert(0, SKRIPTE)
sys.path.insert(0, os.path.join(SKRIPTE, "gefaelle"))

import numpy as np  # noqa: E402

ANTWORTEN = os.path.dirname(SKRIPTE)
RECHERCHE = os.path.dirname(ANTWORTEN)
REGELN_STANDARD = os.path.join(HIER, "fluss_sim_regeln.json")
STRECKEN_STANDARD = os.path.join(RECHERCHE, "vorlagen", "daten", "gefaelle", "steile_strecken.json")
NETZE_CSV = os.path.join(RECHERCHE, "vorlagen", "daten", "netze.csv")
NETZE_MASSE = os.path.join(RECHERCHE, "vorlagen", "daten", "netze_masse.json")
BIOME = ("aue", "bergwald", "canyon", "dschungel", "elfenwald", "fjord", "frost", "gletscher", "heide",
         "kueste", "lava", "oedland", "sumpf", "tundra", "wueste")
FORMAT_VERSION = "fluss_sim_v1"


def log(*t):
    sys.stdout.write("[fluss_sim] " + " ".join(str(x) for x in t) + "\n")
    sys.stdout.flush()


def lese_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _kompakt(o):
    return json.dumps(o, ensure_ascii=True, separators=(",", ":"))


def json_text(o, tiefe=0, max_tiefe=4):
    """Lesbar bis max_tiefe, darunter (und Listen aus Zahlen bzw. kurzen Eintraegen) kompakt in einer Zeile."""
    ein = " " * tiefe
    if isinstance(o, dict) and tiefe < max_tiefe and o:
        teile = ['%s %s: %s' % (ein, json.dumps(k, ensure_ascii=True), json_text(v, tiefe + 1, max_tiefe).lstrip())
                 for k, v in o.items()]
        return "{\n" + ",\n".join(teile) + "\n" + ein + "}"
    if isinstance(o, list) and tiefe < max_tiefe and o and any(isinstance(v, dict) for v in o):
        teile = [ein + " " + json_text(v, tiefe + 1, max_tiefe).lstrip() for v in o]
        return "[\n" + ",\n".join(teile) + "\n" + ein + "]"
    return _kompakt(o)


def schreibe_json(p, d, max_tiefe=4):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json_text(d, 0, max_tiefe))
        f.write("\n")


def r1(v, n=1):
    return float(round(float(v), n))


def zufall(*teile):
    """Deterministische Zahl in [0, 1) aus SHA-256 der Teile."""
    h = hashlib.sha256("|".join(str(t) for t in teile).encode("utf-8")).digest()
    return int.from_bytes(h[:8], "little") / 2.0 ** 64


def zw(a, b, *teile):
    return a + (b - a) * zufall(*teile)


def qrund(v, q):
    """Quantisierung fuer den Fingerabdruck: floor(v / q + 0,5) (kein Banker's Rounding)."""
    return int(math.floor(float(v) / float(q) + 0.5))


# ======================================================================================================================
# Fingerabdruck (Referenz fuer das lokale Werkzeug)
# ======================================================================================================================
def fp_gelaende_text(x0_cm, y0_cm, raster_cm, hoehen_cm, q_cm):
    """hoehen_cm: 2-D (ny, nx), Zeile = y aufsteigend, Spalte = x aufsteigend, Punkt (k, j) bei
    (x0 + j*raster, y0 + k*raster) cm. Text: Kopfzeile + je Zeile die quantisierten Hoehen."""
    H = np.asarray(hoehen_cm, np.float64)
    ny, nx = H.shape
    zeilen = ["G|r=%d|x0=%d|y0=%d|nx=%d|ny=%d|q=%d" % (int(round(raster_cm)), int(round(x0_cm)), int(round(y0_cm)),
                                                       nx, ny, int(q_cm))]
    Q = np.floor(H / float(q_cm) + 0.5).astype(np.int64)
    for k in range(ny):
        zeilen.append(",".join(str(int(v)) for v in Q[k]))
    return "\n".join(zeilen) + "\n"


def fp_splines_text(splines, q_cm):
    """splines: Liste (abschnitt_id, punkte [[x, y, z, breite, tiefe, velocity] in cm bzw. cm/s])."""
    zeilen = []
    for aid, pts in sorted(splines, key=lambda t: t[0]):
        zeilen.append("S|%s|%d" % (aid, len(pts)))
        for p in pts:
            zeilen.append(",".join(str(qrund(v, q_cm)) for v in p[:6]))
    return "\n".join(zeilen) + "\n"


def quat_kanonisch(q):
    q = [float(v) for v in q]
    n = math.sqrt(sum(v * v for v in q)) or 1.0
    q = [v / n for v in q]
    # q und -q sind dieselbe Drehung: erstes von 0 verschiedenes Element ab qw (Reihenfolge qw, qz, qy, qx) positiv
    for v in (q[3], q[2], q[1], q[0]):
        if abs(v) > 1e-9:
            if v < 0:
                q = [-x for x in q]
            break
    return q


def fp_objekte_text(objekte, pos_q_cm, quat_q, skala_q):
    """objekte: Liste (netzpfad, x, y, z [cm], qx, qy, qz, qw, sx, sy, sz). Zeilen sortiert (Text-Sortierung)."""
    zeilen = []
    for o in objekte:
        q = quat_kanonisch(o[4:8])
        zeilen.append("O|%s|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d" % (
            o[0], qrund(o[1], pos_q_cm), qrund(o[2], pos_q_cm), qrund(o[3], pos_q_cm),
            qrund(q[0] * quat_q, 1), qrund(q[1] * quat_q, 1), qrund(q[2] * quat_q, 1), qrund(q[3] * quat_q, 1),
            qrund(o[8] * skala_q, 1), qrund(o[9] * skala_q, 1), qrund(o[10] * skala_q, 1)))
    zeilen.sort()
    return "\n".join(zeilen) + "\n"


def fingerabdruck(gelaende_text, splines_text, objekte_text, version="FLUSS_SIM_FP1"):
    """Fingerabdruck = SHA-256(version + SHA-256 je Teil). Rueckgabe (gesamt, {teil: sha256})."""
    teile = {"gelaende": hashlib.sha256(gelaende_text.encode("ascii")).hexdigest(),
             "splines": hashlib.sha256(splines_text.encode("ascii")).hexdigest(),
             "objekte": hashlib.sha256(objekte_text.encode("ascii")).hexdigest()}
    ges = hashlib.sha256(("%s\n%s\n%s\n%s\n" % (version, teile["gelaende"], teile["splines"], teile["objekte"]))
                         .encode("ascii")).hexdigest()
    return ges, teile


# ======================================================================================================================
# Netz-Masse (Bounds) fuer Grundriss und Hoehe der Instanzen
# ======================================================================================================================
class Masse:
    def __init__(self):
        self.box = {}
        try:
            d = lese_json(NETZE_MASSE)
            for k, v in d.items():
                if isinstance(v, dict) and "min" in v and "max" in v:
                    self.box[k] = (np.asarray(v["min"], float), np.asarray(v["max"], float))
        except OSError:
            pass
        self.csv = {}
        try:
            with open(NETZE_CSV, "r", encoding="utf-8") as f:
                kopf = f.readline().strip().split(";")
                ix = {n: i for i, n in enumerate(kopf)}
                for z in f:
                    t = z.rstrip("\n").split(";")
                    try:
                        g = [float(t[ix["groesse_x_m"]]), float(t[ix["groesse_y_m"]]), float(t[ix["groesse_z_m"]])]
                    except (ValueError, IndexError):
                        continue
                    self.csv[t[ix["pfad"]]] = g
        except OSError:
            pass

    def bounds(self, pfad):
        """(min, max) in cm im Netzraum; ohne Messung 'unten Mitte' aus netze.csv, sonst 1-m-Wuerfel."""
        p = pfad.split(".")[0]
        if p in self.box:
            return self.box[p], "bounds"
        g = self.csv.get(p)
        if g:
            return (np.array([-g[0] * 50.0, -g[1] * 50.0, 0.0]), np.array([g[0] * 50.0, g[1] * 50.0, g[2] * 100.0])), \
                "netze_csv"
        return (np.array([-50.0, -50.0, 0.0]), np.array([50.0, 50.0, 100.0])), "angenommen"


def quat_drehe(q, v):
    """q: (N, 4) [qx, qy, qz, qw]; v: (N, 3) -> gedrehte Vektoren."""
    u = q[:, :3]
    w = q[:, 3:4]
    t = 2.0 * np.cross(u, v)
    return v + w * t + np.cross(u, t)


# ======================================================================================================================
# Objekt-Pool: alle Instanz-Ebenen und Akteure (gefaelle + Sehens)
# ======================================================================================================================
class Pool:
    def __init__(self, regeln, masse):
        self.r = regeln["kollision"]
        self.masse = masse
        self.recs = []          # dict je Objekt
        self.dateien_n = {}     # (quelle, datei) -> Anzahl

    def lade_ebene(self, plan_pfad, ref_quelle):
        """plan_pfad: <...>/<Feld>/plan.json einer Instanz-Ebene (FORMAT.md §3); ref_quelle: stabiler Verweis."""
        p = lese_json(plan_pfad)
        ordner = os.path.dirname(plan_pfad)
        for key in sorted(p.get("dateien") or {}):
            info = p["dateien"][key]
            f = os.path.join(ordner, key + ".f32")
            if not os.path.exists(f):
                continue
            a = np.fromfile(f, dtype="<f4")
            if a.size % 10:
                continue
            a = a.reshape(-1, 10).astype(np.float64)
            self.dateien_n[(ref_quelle, key)] = len(a)
            for i in range(len(a)):
                self.recs.append({"quelle": ref_quelle, "datei": key, "index": i, "pfad": info.get("pfad", key),
                                  "netz": key[:-4] if key.endswith("_kol") else key,
                                  "kollision": bool(info.get("kollision")), "gruppe": info.get("gruppe", ""),
                                  "v": a[i]})
        for i, ak in enumerate(p.get("akteure") or []):
            if not all(k_ in ak for k_ in ("x", "y", "z", "qx", "qy", "qz", "qw")):
                continue
            v = np.array([ak["x"], ak["y"], ak["z"], ak["qx"], ak["qy"], ak["qz"], ak["qw"],
                          ak.get("sx", 1.0), ak.get("sy", 1.0), ak.get("sz", 1.0)], np.float64)
            self.recs.append({"quelle": ref_quelle, "liste": "akteure", "index": i, "pfad": ak.get("pfad", ak.get("netz")),
                              "netz": ak.get("netz", ""), "kollision": bool(ak.get("kollision")),
                              "gruppe": ak.get("klasse", ""), "v": v})

    def fertig(self):
        n = len(self.recs)
        V = np.array([r["v"] for r in self.recs]) if n else np.zeros((0, 10))
        self.V = V
        lo = np.zeros((n, 3))
        hi = np.zeros((n, 3))
        holz = re.compile(self.r["holz_muster"], re.I)
        pflanze = re.compile(self.r["pflanze_muster"], re.I)
        try:
            from sehens_lib.steilwand import ist_fels
        except Exception:                                          # pragma: no cover
            def ist_fels(s):
                return bool(re.search(r"(rock|cliff|boulder|stone|_tier_\d)", str(s), re.I))
        cache = {}
        fest = np.zeros(n, bool)
        art = []
        ecken = np.array([[i, j, k] for i in (0, 1) for j in (0, 1) for k in (0, 1)], float)
        for pfad in sorted({r["pfad"] for r in self.recs}):
            (bmin, bmax), quelle = self.masse.bounds(pfad)
            name = pfad.rsplit("/", 1)[-1]
            if pflanze.search(name):
                a = "pflanze"
            elif ist_fels(pfad):
                a = "fels"
            elif holz.search(name):
                a = "holz"
            else:
                a = "sonstiges"
            cache[pfad] = (bmin, bmax, quelle, a)
        idx_je_pfad = {}
        for k, r in enumerate(self.recs):
            idx_je_pfad.setdefault(r["pfad"], []).append(k)
        for pfad, ix in idx_je_pfad.items():
            bmin, bmax, quelle, a = cache[pfad]
            ix = np.asarray(ix)
            P = V[ix]
            q = P[:, 3:7]
            s = P[:, 7:10]
            ext = []
            for e in ecken:
                c = bmin + (bmax - bmin) * e
                ext.append(quat_drehe(q, c[None, :] * s))
            E = np.stack(ext, 1)                                   # (m, 8, 3)
            lo[ix] = P[:, None, :3].squeeze(1) + E.min(1)
            hi[ix] = P[:, None, :3].squeeze(1) + E.max(1)
        self.lo, self.hi = lo, hi
        for k, r in enumerate(self.recs):
            a = cache[r["pfad"]][3]
            r["art"] = a
            r["masse_quelle"] = cache[r["pfad"]][2]
            groesse = (hi[k] - lo[k]) / 100.0
            gross = max(groesse[0], groesse[1]) >= self.r["min_ausdehnung_m"] and groesse[2] >= self.r["min_hoehe_m"]
            fest[k] = (a != "pflanze") and (r["kollision"] or a in ("fels", "holz")) and gross
            art.append(a)
        self.fest = fest
        self.cx = (lo[:, 0] + hi[:, 0]) / 200.0 if n else np.zeros(0)
        self.cy = (lo[:, 1] + hi[:, 1]) / 200.0 if n else np.zeros(0)
        self.rad = (np.hypot(hi[:, 0] - lo[:, 0], hi[:, 1] - lo[:, 1]) / 200.0) if n else np.zeros(0)
        log("Objekt-Pool: %d Objekte, davon %d fest und gross genug" % (n, int(fest.sum())))

    def ref(self, k):
        r = self.recs[k]
        if "liste" in r:
            return {"quelle": r["quelle"], "liste": "akteure", "index": r["index"]}
        return {"quelle": r["quelle"], "datei": r["datei"], "index": r["index"]}

    def ref_text(self, k):
        r = self.recs[k]
        return "%s#%s#%d" % (r["quelle"], r.get("datei", "akteure"), r["index"])


# ======================================================================================================================
# Gelaende nach den Stempeln (Welt + alle 1-m-Deltas)
# ======================================================================================================================
class Gelaende:
    def __init__(self, welt):
        self.welt = welt
        self.deltas = []

    def delta_hinzu(self, basis, eintraege):
        from sehens_lib import daten as _d
        for e in eintraege or []:
            g = e.get("gelaende") or {}
            fij = g.get("fenster_ij")
            if not (g.get("datei") and isinstance(fij, list) and len(fij) == 4):
                continue
            pf = os.path.join(basis, g["datei"])
            if os.path.exists(pf) and os.path.getsize(pf) == fij[2] * fij[3] * 4:
                i0, j0, hh, ww = fij
                box = (j0 - _d.OFF_J, i0 - _d.OFF_I, j0 + ww - 1 - _d.OFF_J, i0 + hh - 1 - _d.OFF_I)
                self.deltas.append((tuple(fij), box, pf))

    def delta(self, x, y):
        from sehens_lib import daten as _d
        out = np.zeros(np.broadcast(x, y).shape)
        x0, x1, y0, y1 = float(np.min(x)), float(np.max(x)), float(np.min(y)), float(np.max(y))
        for (i0, j0, hh, ww), box, pf in self.deltas:
            if box[2] < x0 or box[0] > x1 or box[3] < y0 or box[1] > y1:
                continue
            a = np.fromfile(pf, dtype="<f4").reshape(hh, ww).astype(np.float64)
            fi = y + _d.OFF_I - i0
            fj = x + _d.OFF_J - j0
            innen = (fi >= 0) & (fi <= hh - 1) & (fj >= 0) & (fj <= ww - 1)
            if not innen.any():
                continue
            i = np.clip(np.floor(fi).astype(np.int64), 0, hh - 2)
            j = np.clip(np.floor(fj).astype(np.int64), 0, ww - 2)
            di = np.clip(fi - i, 0, 1)
            dj = np.clip(fj - j, 0, 1)
            v = (a[i, j] * (1 - di) * (1 - dj) + a[i, j + 1] * (1 - di) * dj + a[i + 1, j] * di * (1 - dj) +
                 a[i + 1, j + 1] * di * dj)
            out = np.where(innen, out + v, out)
        return out

    def raster(self, bereich_cm):
        """Abtastpunkte = Pixelmitten des Planrasters im Bereich; Hoehe (cm) = Rasterhoehe + Deltas."""
        from sehens_lib import daten as _d
        w = self.welt
        z = w.zelle_m
        xmin, ymin, xmax, ymax = [v / 100.0 for v in bereich_cm]
        fi0, fj0 = _d.m_zu_pixel(xmin, ymin, z)
        fi1, fj1 = _d.m_zu_pixel(xmax, ymax, z)
        i0, i1 = max(int(math.ceil(float(fi0))), 0), min(int(math.floor(float(fi1))), w.ny - 1)
        j0, j1 = max(int(math.ceil(float(fj0))), 0), min(int(math.floor(float(fj1))), w.nx - 1)
        I, J = np.meshgrid(np.arange(i0, i1 + 1), np.arange(j0, j1 + 1), indexing="ij")
        X, Y = _d.pixel_zu_m(I, J, z)
        H = w.hoehe[I, J].astype(np.float64) + self.delta(X, Y)
        x0, y0 = _d.pixel_zu_m(i0, j0, z)
        return float(x0) * 100.0, float(y0) * 100.0, z * 100.0, H * 100.0


# ======================================================================================================================
# Wasserlinie eines Gewaessers (River + Kaskadennetz bzw. roher Lauf)
# ======================================================================================================================
class Linie:
    """Zusammengefuehrte Mittellinie in Laufkoordinate s (m): x, y, z, breite, tiefe (cm), v (cm/s), knick."""

    def __init__(self, s, x, y, z, b, t, v, knick):
        o = np.argsort(np.asarray(s), kind="stable")
        self.s = np.asarray(s, float)[o]
        self.x = np.asarray(x, float)[o]
        self.y = np.asarray(y, float)[o]
        self.z = np.minimum.accumulate(np.asarray(z, float)[o])
        self.b = np.asarray(b, float)[o]
        self.t = np.asarray(t, float)[o]
        self.v = np.asarray(v, float)[o]
        self.knick = [knick[i] for i in o]

    def bei(self, s):
        s = np.asarray(s, float)
        return {"x": np.interp(s, self.s, self.x), "y": np.interp(s, self.s, self.y),
                "z": np.interp(s, self.s, self.z), "b": np.interp(s, self.s, self.b),
                "t": np.interp(s, self.s, self.t), "v": np.interp(s, self.s, self.v)}

    def z_bei(self, s, seite="unten"):
        """Wasserhoehe bei s; an senkrechten Spruengen (gleiches s) die untere bzw. obere Hoehe."""
        k = np.searchsorted(self.s, s, side="right" if seite == "unten" else "left")
        if seite == "unten" and k > 0 and abs(self.s[k - 1] - s) < 1e-6:
            return float(self.z[k - 1])
        return float(np.interp(s, self.s, self.z))

    def tangente(self, s):
        d = 0.5
        a = self.bei(max(s - d, self.s[0]))
        b = self.bei(min(s + d, self.s[-1]))
        tx, ty = float(b["x"] - a["x"]), float(b["y"] - a["y"])
        n = math.hypot(tx, ty) or 1.0
        return tx / n, ty / n

    def s_projektion(self, x_cm, y_cm, z_cm=None, z_tol_cm=3.0):
        d = np.hypot(self.x - x_cm, self.y - y_cm)
        if z_cm is not None:
            ok = np.abs(self.z - z_cm) <= z_tol_cm
            if ok.any():
                d = np.where(ok, d, np.inf)
        return float(self.s[int(np.argmin(d))])

    def s_fuss(self, s_lippe, z_unten_cm, s_max=None):
        """Erstes s hinter der Lippe, an dem die Wasserlinie den unteren Spiegel erreicht."""
        k = np.where((self.s > s_lippe + 1e-6) & (self.z <= z_unten_cm + 1.0))[0]
        if len(k) == 0:
            return min(s_lippe + 0.5, float(self.s[-1]))
        s = float(self.s[k[0]])
        return s if s_max is None else min(s, s_max)


def _s_entlang(P):
    P = np.asarray(P, float)
    if len(P) < 2:
        return np.zeros(len(P))
    return np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(P[:, :2], axis=0).T))]) / 100.0


def tiefe_aus_kn(kn, i, M, regeln):
    Q = kn.get("quer")
    if Q and i < len(Q) and Q[i]:
        q = np.asarray(Q[i], float)
        if q.ndim == 2 and q.shape[1] >= 4:
            n = len(q)
            anteil = regeln["abschnitt"]["tiefe_quer_anteil"]
            a = int(round((1 - anteil) / 2 * (n - 1)))
            return float(np.max(q[a:n - a, 3]))
    return float(M[i][7])


def linie_aus_koerper(koerper, regeln):
    S, X, Y, Z, B, T, V, K = [], [], [], [], [], [], [], []
    kn_ber = [(w["s_m"][0], w["s_m"][1]) for w in koerper if w["typ"] == "kaskadennetz"]
    for w in koerper:
        if w["typ"] == "kaskadennetz":
            M = w["mittellinie"]
            ss = w.get("mittellinie_s_m") or list(w["s_m"][0] + _s_entlang(M))
            for i, (p, s_) in enumerate(zip(M, ss)):
                kn_ = w["knick"][i] if i < len(w.get("knick") or []) else "becken"
                t = tiefe_aus_kn(w, i, M, regeln) if kn_ not in ("bogen", "wand") else float("nan")
                S.append(float(s_)); X.append(p[0]); Y.append(p[1]); Z.append(p[2]); B.append(p[3])
                T.append(t); V.append(float(p[4])); K.append(kn_)
        elif w["typ"] == "river":
            P = w["punkte"]
            a, b = w["s_m"]
            sl = _s_entlang(P)
            ss = a + sl * ((b - a) / sl[-1] if sl[-1] > 0 else 0.0)
            for p, s_ in zip(P, ss):
                if any(ka + 1e-3 < s_ < kb - 1e-3 for ka, kb in kn_ber):
                    continue
                S.append(float(s_)); X.append(p[0]); Y.append(p[1]); Z.append(p[2]); B.append(p[3])
                T.append(float(p[4])); V.append(float(p[5])); K.append("river")
    T = np.asarray(T, float)
    S_ = np.asarray(S, float)
    ok = np.isfinite(T)
    if ok.any() and not ok.all():
        T[~ok] = np.interp(S_[~ok], S_[ok], T[ok])
    T = np.maximum(T, regeln["abschnitt"]["tiefe_min_cm"])
    # gleiche s: Reihenfolge hoch -> tief, minimaler Versatz, damit z(s) eine Funktion bleibt
    o = sorted(range(len(S)), key=lambda i: (S[i], -Z[i]))
    S2, last = [], None
    for i in o:
        s_ = S[i]
        if last is not None and s_ <= last + 1e-5:
            s_ = last + 1e-4
        S2.append((i, s_))
        last = s_
    idx = [i for i, _ in S2]
    return Linie([s for _, s in S2], [X[i] for i in idx], [Y[i] for i in idx], [Z[i] for i in idx],
                 [B[i] for i in idx], [T[i] for i in idx], [V[i] for i in idx], [K[i] for i in idx])


def linie_aus_punkten(P, regeln, schritt_m=None):
    """Roher Lauf (wasser_welt/baeche_alle bzw. Bach ohne Stufen): Punkte [x, y, z, breite, tiefe, v]."""
    P = np.asarray(P, float)
    if P.shape[1] < 6:
        P = np.hstack([P, np.zeros((len(P), 6 - P.shape[1]))])
    s = _s_entlang(P)
    t = np.maximum(P[:, 4], regeln["abschnitt"]["tiefe_min_cm"])
    return Linie(s, P[:, 0], P[:, 1], P[:, 2], P[:, 3], t, P[:, 5], ["roh"] * len(P))


# ======================================================================================================================
# Abstuerze, Faelle, Becken, Abschnitte
# ======================================================================================================================
def abstuerze_gefaelle(plan, linie):
    out = []
    for st in plan.get("stufen") or []:
        teil = st.get("teilstufen")
        if isinstance(teil, str):
            try:
                teil = json.loads(teil)
            except ValueError:
                teil = None
        rampe_st = st.get("art") == "schnelle"
        if teil:
            for k, t in enumerate(teil):
                sl = float(t["s_m"])
                zu = float(t.get("unten_z_cm", linie.z_bei(sl) - 100 * t["fall_m"]))
                out.append({"id": "%s_T%d" % (st["id"], k + 1), "stufe": st["id"], "teil": k + 1, "art": st.get("art"),
                            "art_regel": st.get("art_regel"), "s_lippe": sl, "z_oben": float(t.get("oben_z_cm", linie.z_bei(sl, "oben"))),
                            "z_unten": zu, "fall_m": float(t["fall_m"]), "rampe": bool(t.get("rampe")) or rampe_st})
        else:
            sl = float(st["s_m"])
            zo = float(st["lippe_cm"][0][2]) if st.get("lippe_cm") else linie.z_bei(sl, "oben")
            zu = float(st.get("fuss_z_cm", zo - 100 * st["fall_m"]))
            out.append({"id": st["id"], "stufe": st["id"], "teil": 0, "art": st.get("art"), "art_regel": st.get("art_regel"),
                        "s_lippe": sl, "z_oben": zo, "z_unten": zu, "fall_m": float(st["fall_m"]), "rampe": rampe_st})
    out.sort(key=lambda d: (d["s_lippe"], d["id"]))
    for d in out:
        d["s_fuss"] = linie.s_fuss(d["s_lippe"], d["z_unten"])
    return out


def abstuerze_sehens(lauf_id, bach, linie):
    out = []
    for k, st in enumerate(bach.get("stufen") or []):
        lp, fp = st.get("lippe_cm"), st.get("fuss_cm")
        if not (lp and fp):
            continue
        sl = linie.s_projektion(lp[0], lp[1], lp[2])
        sf_proj = linie.s_projektion(fp[0], fp[1], fp[2])
        out.append({"id": "%s_S%02d" % (lauf_id, k), "stufe": "%s_S%02d" % (lauf_id, k), "teil": 0, "art": st.get("art"),
                    "art_regel": st.get("art"), "s_lippe": sl, "z_oben": float(lp[2]), "z_unten": float(fp[2]),
                    "fall_m": float(st["fall_m"]), "rampe": st.get("art") == "schnelle", "s_fuss_proj": sf_proj})
    out.sort(key=lambda d: (d["s_lippe"], d["id"]))
    for d in out:
        d["s_fuss"] = max(linie.s_fuss(d["s_lippe"], d["z_unten"]), d["s_lippe"])
    return out


def becken_aus(abst, linie):
    """Becken = Wasser zwischen Fuss eines Absturzes und Lippe des naechsten (auch Laufanfang/-ende)."""
    grenzen = [(float(linie.s[0]), None)]
    out = []
    a = float(linie.s[0])
    vor = None
    for d in abst:
        if d["s_lippe"] - a > 0.05:
            out.append({"s_m": [a, d["s_lippe"]], "oben": vor, "unten": d["id"]})
        a = max(a, d["s_fuss"])
        vor = d["id"]
    if float(linie.s[-1]) - a > 0.05:
        out.append({"s_m": [a, float(linie.s[-1])], "oben": vor, "unten": None})
    del grenzen
    return out


def abschnitte_bilden(linie, faelle, regeln):
    """Abschnitte zwischen den Faellen; zu kurze Becken talwaerts zusammenfassen; lange teilen."""
    R = regeln["abschnitt"]
    s0, s1 = float(linie.s[0]), float(linie.s[-1])
    seg = []
    a, vor = s0, None
    for f in faelle:
        seg.append({"a": a, "b": f["s_lippe"], "oben": vor, "unten": f["id"], "innen": []})
        a, vor = f["s_fuss"], f["id"]
    seg.append({"a": a, "b": s1, "oben": vor, "unten": None, "innen": []})
    # Reste am Laufanfang/-ende (Fall direkt am Laufrand): kein eigener Abschnitt
    if len(seg) > 1 and seg[0]["b"] - seg[0]["a"] < R["rest_am_laufende_m"]:
        seg[1]["rest_oben"] = True
        seg = seg[1:]
    if len(seg) > 1 and seg[-1]["b"] - seg[-1]["a"] < R["rest_am_laufende_m"]:
        seg[-2]["rest_unten"] = True
        seg = seg[:-1]
    # zu kurze Becken mit dem talwaerts folgenden (am Laufende: mit dem oberen) Abschnitt zusammenfassen
    while len(seg) > 1:
        k = next((i for i, g in enumerate(seg) if g["b"] - g["a"] < R["min_laenge_m"]), None)
        if k is None:
            break
        j = k + 1 if k + 1 < len(seg) else k - 1
        o, u = (seg[k], seg[j]) if j > k else (seg[j], seg[k])
        neu = {"a": o["a"], "b": u["b"], "oben": o["oben"], "unten": u["unten"],
               "innen": o["innen"] + [o["unten"]] + u["innen"]}
        for key in ("rest_oben",):
            if o.get(key):
                neu[key] = True
        if u.get("rest_unten"):
            neu["rest_unten"] = True
        i0 = min(k, j)
        seg[i0:i0 + 2] = [neu]
    # lange Abschnitte teilen (gleich lange Teile, gemeinsamer Endpunkt); breite Fluesse kuerzer, damit Abschnitt
    # + Breite + 2 x Rand in eine Kachel passen (mindestens 1/4 Kachel)
    K = regeln["kacheln"]
    out = []
    for g in seg:
        L = g["b"] - g["a"]
        ss_ = np.linspace(g["a"], g["b"], 9)
        bmax = float(np.max(linie.bei(ss_)["b"])) / 100.0
        lmax = min(R["max_laenge_m"], max(K["groesse_m"] - 2 * K["rand_m"] - bmax, 0.25 * K["groesse_m"]))
        n = max(1, int(math.ceil(L / lmax - 1e-9)))
        for m in range(n):
            h = dict(g)
            h["a"] = g["a"] + L * m / n
            h["b"] = g["a"] + L * (m + 1) / n
            h["teil"] = (m + 1, n)
            if m > 0:
                h["oben"] = None
                h.pop("rest_oben", None)
            if m < n - 1:
                h["unten"] = None
                h.pop("rest_unten", None)
            out.append(h)
    return out


def spline_punkte(linie, g, abst, regeln, roh=False):
    """Splinepunkte eines Abschnitts: Anfang, Ende, Lippe/Fuss aller Abstuerze darin, sonst <= punkt_abstand_m."""
    R = regeln["abschnitt"]
    a, b = g["a"], g["b"]
    fest = {a: "CURVE_CLAMPED", b: "CURVE_CLAMPED"}
    for d in abst:
        if a + 1e-4 < d["s_lippe"] < b - 1e-4:
            fest[d["s_lippe"]] = "LINEAR"
            if d["s_fuss"] < b - 1e-4:
                fest[d["s_fuss"]] = "LINEAR"
    if roh:
        for s_ in linie.s:
            if a + 0.05 < s_ < b - 0.05:
                fest.setdefault(float(s_), "CURVE_CLAMPED")
    schritt = R["punkt_abstand_roh_m"] if roh else R["punkt_abstand_m"]
    ks = sorted(fest)
    ss, typ = [ks[0]], [fest[ks[0]]]
    for s_ in ks[1:]:
        n = max(1, int(math.ceil((s_ - ss[-1]) / schritt - 1e-9)))
        # innerhalb eines Absturzes (Lippe -> Fuss) keine Zwischenpunkte
        im_sturz = any(abs(ss[-1] - d["s_lippe"]) < 1e-6 and abs(s_ - d["s_fuss"]) < 1e-6 for d in abst)
        if im_sturz:
            n = 1
        basis = ss[-1]
        for m in range(1, n):
            ss.append(basis + (s_ - basis) * m / n)
            typ.append("CURVE_CLAMPED")
        ss.append(s_)
        typ.append(fest[s_])
    ss = np.asarray(ss)
    w = linie.bei(ss)
    z = np.array([linie.z_bei(s_, "oben") if t == "LINEAR" and any(abs(s_ - d["s_lippe"]) < 1e-6 for d in abst)
                  else linie.z_bei(s_, "unten") for s_, t in zip(ss, typ)])
    # Lippe = Oberwasser, Fuss = Unterwasser; Anfang des Abschnitts nach einem Fall = Unterwasser
    z = np.minimum.accumulate(z)
    v = np.clip(w["v"], R["velocity_min_cm_s"], R["velocity_max_cm_s"])
    pts = []
    for i in range(len(ss)):
        pts.append([r1(w["x"][i]), r1(w["y"][i]), r1(z[i]), r1(max(w["b"][i], 10.0)), r1(max(w["t"][i], R["tiefe_min_cm"])),
                    r1(v[i])])
    # Tangenten (Catmull-Rom in xy, monoton in z: 0 an flachen Nachbarn und an LINEAR-Punkten)
    tang = []
    P = np.array([p[:3] for p in pts])
    for i in range(len(pts)):
        if len(pts) == 1:
            tang.append([0.0, 0.0, 0.0])
            continue
        p0 = P[max(i - 1, 0)]
        p1 = P[min(i + 1, len(pts) - 1)]
        den = 2.0 if 0 < i < len(pts) - 1 else 1.0
        t = (p1 - p0) / den
        dz0 = P[i][2] - P[max(i - 1, 0)][2] if i > 0 else None
        dz1 = P[min(i + 1, len(pts) - 1)][2] - P[i][2] if i < len(pts) - 1 else None
        if typ[i] == "LINEAR" or (dz0 is not None and abs(dz0) < 0.5) or (dz1 is not None and abs(dz1) < 0.5):
            t[2] = 0.0
        else:
            cand = [abs(x) for x in (dz0, dz1) if x is not None]
            t[2] = -min(cand) if cand else 0.0
        tang.append([r1(t[0]), r1(t[1]), r1(t[2])])
    # Rolle je Punkt (aus dem Knick der Quelle): becken/uebergang = Becken (waagrecht), rampe/river/roh = Gerinne
    rollen = []
    for s_, t_ in zip(ss, typ):
        if t_ == "LINEAR":
            rollen.append("lippe" if any(abs(s_ - d["s_lippe"]) < 1e-6 for d in abst) else "fuss")
            continue
        k = int(np.clip(np.searchsorted(linie.s, s_), 0, len(linie.s) - 1))
        kk = [i for i in (k - 1, k) if 0 <= i < len(linie.s)]
        r_ = [linie.knick[i] for i in kk]
        rollen.append("becken" if all(x in ("becken", "uebergang", "fuss") for x in r_) else
                      ("rampe" if "rampe" in r_ else ("gerinne" if "gerinne" in r_ else r_[-1])))
    return ss, pts, typ, tang, rollen


# ======================================================================================================================
# Wasser-Kollision
# ======================================================================================================================
def kollision_fuer(pool, abschnitte_pts, regeln):
    """abschnitte_pts: Liste (abschnitt_id, pts). Rueckgabe Liste (k, abschnitt_id, abstand_m, lage)."""
    R = regeln["kollision"]
    if not len(pool.recs):
        return []
    segs = []
    for aid, pts in abschnitte_pts:
        P = np.asarray(pts, float) / np.array([100, 100, 100, 100, 100, 1.0])
        for i in range(len(P) - 1):
            segs.append((aid, P[i], P[i + 1]))
        if len(P) == 1:
            segs.append((aid, P[0], P[0]))
    if not segs:
        return []
    A = np.array([s[1] for s in segs])
    Bp = np.array([s[2] for s in segs])
    bmax = float(max(A[:, 3].max(), Bp[:, 3].max()))
    xmin = min(A[:, 0].min(), Bp[:, 0].min()) - bmax / 2 - R["abstand_m"] - 30
    xmax = max(A[:, 0].max(), Bp[:, 0].max()) + bmax / 2 + R["abstand_m"] + 30
    ymin = min(A[:, 1].min(), Bp[:, 1].min()) - bmax / 2 - R["abstand_m"] - 30
    ymax = max(A[:, 1].max(), Bp[:, 1].max()) + bmax / 2 + R["abstand_m"] + 30
    kand = np.where(pool.fest & (pool.cx >= xmin) & (pool.cx <= xmax) & (pool.cy >= ymin) & (pool.cy <= ymax))[0]
    out = []
    if not len(kand):
        return out
    AB = Bp[:, :2] - A[:, :2]
    L2 = np.maximum((AB ** 2).sum(1), 1e-9)
    for c0 in range(0, len(kand), 512):
        kk = kand[c0:c0 + 512]
        px = pool.cx[kk][:, None]
        py = pool.cy[kk][:, None]
        t = np.clip(((px - A[None, :, 0]) * AB[None, :, 0] + (py - A[None, :, 1]) * AB[None, :, 1]) / L2[None, :], 0, 1)
        qx = A[None, :, 0] + t * AB[None, :, 0]
        qy = A[None, :, 1] + t * AB[None, :, 1]
        d = np.hypot(px - qx, py - qy)
        halb = (A[None, :, 3] + t * (Bp[None, :, 3] - A[None, :, 3])) / 2.0
        zw_ = A[None, :, 2] + t * (Bp[None, :, 2] - A[None, :, 2])
        tw = A[None, :, 4] + t * (Bp[None, :, 4] - A[None, :, 4])
        rad = pool.rad[kk][:, None]
        rand = d - rad - halb
        zlo = pool.lo[kk, 2][:, None] / 100.0
        zhi = pool.hi[kk, 2][:, None] / 100.0
        ok = (rand <= R["abstand_m"]) & (zlo <= zw_ + R["ueber_spiegel_max_m"]) & \
             (zhi >= zw_ - tw - R["unter_bett_toleranz_m"])
        rand_m = np.where(ok, rand, np.inf)
        best = np.argmin(rand_m, 1)
        for i, k in enumerate(kk):
            j = best[i]
            if not np.isfinite(rand_m[i, j]):
                continue
            lage = "im_wasser" if d[i, j] - rad[i, 0] < halb[i, j] else "ufer"
            out.append((int(k), segs[j][0], float(rand_m[i, j]), lage, float(d[i, j]), float(halb[i, j])))
    out.sort(key=lambda t: pool.ref_text(t[0]))
    return out


# ======================================================================================================================
# Schaumobjekte (Nachtrag Datei 16)
# ======================================================================================================================
def schaum_fuer_fall(f, linie, becken_ende_s, strahl_m, regeln, randbloecke, ufer_rand):
    R = regeln["schaum"]
    D = f["fall_m"]
    sf = f["s_fuss"]
    Lp = max(becken_ende_s - sf, 0.0)
    tx, ty = linie.tangente(min(sf + 0.3, float(linie.s[-1])))
    yaw = math.degrees(math.atan2(ty, tx))
    nx_, ny_ = -ty, tx                                             # links in Fliessrichtung
    wf = linie.bei(sf)
    B = float(wf["b"]) / 100.0
    z_sp = linie.z_bei(sf, "unten")
    out = []
    # Aufprallteppich
    fak = zw(R["aufprall_faktor"][0], R["aufprall_faktor"][1], f["id"], "aufprall")
    r = max(R["aufprall_radius_min_m"], fak * D)
    breite = min(2 * r, 0.9 * B)
    if strahl_m:
        breite = max(min(breite, 0.9 * B), min(strahl_m + 0.4, 0.9 * B))
    laenge = 2 * r * R["aufprall_laenge_streckung"]
    if Lp > 0:
        laenge = min(laenge, max(R["aufprall_becken_anteil_max"] * Lp, 0.5))
    laenge = max(laenge, 0.5)
    sm = sf + 0.4 * laenge
    pm = linie.bei(min(sm, float(linie.s[-1])))
    out.append({"art": "aufprallteppich", "pos_cm": [r1(pm["x"]), r1(pm["y"]), r1(z_sp + 1.0)],
                "groesse_m": [r1(laenge, 2), r1(breite, 2)], "drehung_yaw_grad": r1(yaw, 1),
                "form": "unregelmaessig, Rand ausgefranst", "seed": int(zufall(f["id"], "seed") * 1e9),
                "s_m": [r1(sf, 2), r1(sf + laenge, 2)]})
    # Schaumstrassen
    n_str = int(round(min(max(2 + 0.8 * D, R["strassen_anzahl"][0]), R["strassen_anzahl"][1])))
    s_start = sf + 0.8 * laenge
    platz = becken_ende_s - s_start - 0.3
    if platz >= R["strassen_min_laenge_m"]:
        spreiz = min(0.6 * B / 2, (strahl_m or B * 0.5) / 2 + 0.5)
        for k in range(n_str):
            u0 = -spreiz + 2 * spreiz * (k + 0.5) / n_str + zw(-0.15, 0.15, f["id"], "u", k)
            Ls = min(zw(R["strassen_laenge_m"][0], R["strassen_laenge_m"][1], f["id"], "L", k), platz)
            wb = zw(R["strassen_breite_m"][0], R["strassen_breite_m"][1], f["id"], "b", k)
            bogen = zw(-R["strassen_bogen_m"], R["strassen_bogen_m"], f["id"], "bogen", k)
            pts = []
            for m in range(5):
                s_ = s_start + Ls * m / 4.0
                p = linie.bei(min(s_, float(linie.s[-1])))
                tx_, ty_ = linie.tangente(min(s_, float(linie.s[-1])))
                u = u0 + bogen * math.sin(math.pi * m / 4.0)
                umax = max(float(p["b"]) / 200.0 - wb / 2.0 - 0.1, 0.0)
                u = max(-umax, min(umax, u))
                pts.append([r1(p["x"] - ty_ * u * 100), r1(p["y"] + tx_ * u * 100), r1(linie.z_bei(s_, "unten") + 1.0)])
            out.append({"art": "schaumstrasse", "punkte_cm": pts, "pos_cm": pts[0],
                        "groesse_m": [r1(Ls, 2), r1(wb, 2)], "drehung_yaw_grad": r1(yaw, 1), "auslaufend": True,
                        "folgt": "Stroemung (Shallow Water) sonst mittellinie"})
    # Kehrwasser neben dem Aufprall (beide Seiten), wo Platz neben dem Strahl ist
    re_ = min(max(R["kehrwasser_radius_m"][0], 0.12 * B), R["kehrwasser_radius_m"][1])
    s_k = sf + min(0.5 * Lp, 0.7 * laenge)
    pk = linie.bei(s_k)
    uk = B / 2 - re_ - 0.2
    n_k = 0
    if Lp >= 2 * re_ + 0.5 and uk > (strahl_m or 0.5 * B) / 2 + 0.3:
        for sgn, seite in ((1, "links"), (-1, "rechts")):
            out.append({"art": "kehrwasser", "pos_cm": [r1(pk["x"] + nx_ * sgn * uk * 100), r1(pk["y"] + ny_ * sgn * uk * 100),
                                                        r1(linie.z_bei(s_k, "unten") + 1.0)],
                        "groesse_m": [r1(2 * re_, 2), r1(2 * re_, 2)], "drehung_yaw_grad": r1(yaw, 1),
                        "grund": "neben dem Aufprall (%s)" % seite, "ruhend": True})
            n_k += 1
    # Kehrwasser im Lee von Randbloecken dieses Beckens: stromab des Blocks, zur Wassermitte hin ins Wasser geschoben
    for rb in randbloecke:
        if n_k >= R["kehrwasser_je_becken_max"]:
            break
        s_e = rb["s"] + rb["r"] + re_
        if not (sf + 0.5 <= rb["s"] and s_e <= becken_ende_s - 0.3):
            continue
        p = linie.bei(s_e)
        tx_, ty_ = linie.tangente(s_e)
        u = min(abs(rb["u"]), float(p["b"]) / 200.0 - re_ - 0.1)
        if u <= 0:
            continue
        sg = 1.0 if rb["u"] >= 0 else -1.0
        out.append({"art": "kehrwasser", "pos_cm": [r1(p["x"] - ty_ * sg * u * 100), r1(p["y"] + tx_ * sg * u * 100),
                                                    r1(linie.z_bei(s_e, "unten") + 1.0)],
                    "groesse_m": [r1(2 * re_, 2), r1(2 * re_, 2)], "drehung_yaw_grad": r1(math.degrees(math.atan2(ty_, tx_)), 1),
                    "grund": "hinter Randblock", "block": rb["ref"], "ruhend": True})
        n_k += 1
    if ufer_rand:
        S = np.asarray(ufer_rand.get("s_m") or [], float)
        for seite, sgn in (("einzug_links_m", 1), ("einzug_rechts_m", -1)):
            if n_k >= R["kehrwasser_je_becken_max"] or not len(S):
                break
            E = np.asarray(ufer_rand.get(seite) or [], float)
            if len(E) != len(S):
                continue
            for i in range(1, len(S)):
                if not (sf + 0.5 <= S[i] <= becken_ende_s - 0.5):
                    continue
                if E[i - 1] >= R["bucht_einzug_min_m"] and E[i] < 0.1:
                    s_b = float(S[i]) + 0.5
                    p = linie.bei(s_b)
                    tx_, ty_ = linie.tangente(s_b)
                    u = float(p["b"]) / 200.0 - re_ - 0.1
                    out.append({"art": "kehrwasser", "pos_cm": [r1(p["x"] - ty_ * sgn * u * 100), r1(p["y"] + tx_ * sgn * u * 100),
                                                                r1(linie.z_bei(s_b, "unten") + 1.0)],
                                "groesse_m": [r1(2 * re_, 2), r1(2 * re_, 2)], "drehung_yaw_grad": r1(math.degrees(math.atan2(ty_, tx_)), 1),
                                "grund": "Bucht hinter Vorsprung (%s)" % ("links" if sgn > 0 else "rechts"), "ruhend": True})
                    n_k += 1
                    break
    return out


# ======================================================================================================================
# Gewaesser -> fluss_sim
# ======================================================================================================================
def baue_gewaesser(g, linie, abst, regeln, pool, extra):
    """g: dict id, art, quelle; abst: Abstuerze; extra: kaskadennetze, effekte, vorhang, strahl, ufer_rand, roh."""
    R = regeln
    schw = R["fall_schwelle_m"]
    faelle = [d for d in abst if d["fall_m"] >= schw - 1e-9 and not d["rampe"]]
    segs = abschnitte_bilden(linie, faelle, R)
    abschnitte = []
    for n, s in enumerate(segs):
        ss, pts, typ, tang, rollen = spline_punkte(linie, s, abst, R, roh=extra.get("roh", False))
        aid = "%s_A%02d" % (g["id"], n)
        s["id"] = aid
        bec = []
        for b in extra["becken"]:
            m = 0.5 * (b["s_m"][0] + b["s_m"][1])
            if s["a"] - 1e-6 <= m <= s["b"] + 1e-6:
                bec.append({"s_m": [r1(b["s_m"][0], 2), r1(b["s_m"][1], 2)],
                            "spiegel_cm": [r1(linie.z_bei(b["s_m"][0], "unten")), r1(linie.z_bei(b["s_m"][1], "oben"))],
                            "oben": b["oben"], "unten": b["unten"]})
        abschnitte.append({
            "id": aid, "s_m": [r1(s["a"], 2), r1(s["b"], 2)], "laenge_m": r1(s["b"] - s["a"], 2),
            "teil": list(s.get("teil", (1, 1))),
            "punkte": pts, "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
            "punkt_typen": typ, "tangenten_cm": tang, "punkte_s_m": [r1(v, 2) for v in ss], "punkt_rollen": rollen,
            "anschluss": {"oben_fall": s["oben"], "unten_fall": s["unten"],
                          "spiegel_anfang_cm": pts[0][2], "spiegel_ende_cm": pts[-1][2],
                          "rest_oben": bool(s.get("rest_oben")), "rest_unten": bool(s.get("rest_unten"))},
            "faelle_innen": s["innen"], "becken": bec,
            "water_body": {"klasse": "WaterBodyRiver", "affects_landscape": False,
                           "hinweis": "Gelaende kommt aus dem Planer-Delta; Depth nur fuer Water-Info/Simulation"}})
    a_id_je_s = [(a["s_m"][0], a["s_m"][1], a["id"]) for a in abschnitte]

    def abschnitt_bei(s_, oben):
        # oben (Lippe): Abschnitt, der an der Lippe endet bzw. sie enthaelt; unten (Fuss): der dort beginnt/enthaelt
        kand = [i for a, b, i in a_id_je_s if a - 1e-3 <= s_ <= b + 1e-3]
        if not kand:
            return None
        return kand[0] if oben else kand[-1]

    # Wasser-Kollision
    kol = kollision_fuer(pool, [(a["id"], a["punkte"]) for a in abschnitte], R)
    wk = []
    randbloecke = []
    kante = R["kollision"]["randblock_kante_m"]
    for k, aid, rand, lage, d, halb in kol:
        rec = pool.recs[k]
        gro = (pool.hi[k] - pool.lo[k]) / 100.0
        wk.append({"ref": pool.ref(k), "netz": rec["netz"], "pfad": rec["pfad"], "art": rec["art"],
                   "pos_cm": [r1(rec["v"][0]), r1(rec["v"][1]), r1(rec["v"][2])],
                   "groesse_m": [r1(gro[0], 2), r1(gro[1], 2), r1(gro[2], 2)], "lage": lage,
                   "abstand_rand_m": r1(rand, 2), "abschnitt": aid, "kollision_im_plan": rec["kollision"],
                   "wasser_kollision": True})
        if abs(d - halb) <= pool.rad[k] + kante:
            zm = (pool.lo[k, 2] + pool.hi[k, 2]) / 2.0
            s_ = linie.s_projektion(pool.cx[k] * 100, pool.cy[k] * 100, zm, z_tol_cm=150.0)
            p = linie.bei(s_)
            tx_, ty_ = linie.tangente(s_)
            u = ((pool.cx[k] * 100 - p["x"]) * -ty_ + (pool.cy[k] * 100 - p["y"]) * tx_) / 100.0
            randbloecke.append({"s": s_, "u": float(u), "r": float(pool.rad[k]), "ref": pool.ref(k)})
    randbloecke.sort(key=lambda t: (t["s"], t["u"]))
    # Faelle
    fl = []
    alle_s = sorted(abst, key=lambda d: d["s_lippe"])
    KN = R["kaskadennetz"]
    for f in faelle:
        nxt = [d["s_lippe"] for d in alle_s if d["s_lippe"] > f["s_fuss"] + 1e-6]
        becken_ende = min(nxt) if nxt else float(linie.s[-1])
        a_o = abschnitt_bei(f["s_lippe"], True)
        a_u = abschnitt_bei(f["s_fuss"], False)
        innen = a_o is not None and a_o == a_u
        pl, pf_ = linie.bei(f["s_lippe"]), linie.bei(f["s_fuss"])
        strahl = extra["strahl"].get(f["stufe"])
        kn_id = next((k["id"] for k in extra["kaskadennetze"] if k["s_m"][0] - 1e-3 <= f["s_lippe"] <= k["s_m"][1] + 1e-3), None)
        eff = [e for e in extra["effekte"] if e.get("stufe") == f["stufe"]]
        if f["teil"]:
            gesch = [d for d in faelle if d["stufe"] == f["stufe"]]
            eff = [e for e in eff if min(gesch, key=lambda d: math.hypot(
                linie.bei(d["s_fuss"])["x"] - e["pos_cm"][0], linie.bei(d["s_fuss"])["y"] - e["pos_cm"][1]))["id"] == f["id"]]
        eintrag = {
            "id": f["id"], "stufe": f["stufe"], "teil": f["teil"], "art": f["art"], "art_regel": f.get("art_regel"),
            "fall_m": r1(f["fall_m"], 2), "s_lippe_m": r1(f["s_lippe"], 2), "s_fuss_m": r1(f["s_fuss"], 2),
            "abschnitt_oben": a_o, "abschnitt_unten": a_u, "im_abschnitt": innen,
            "lippe_cm": [r1(pl["x"]), r1(pl["y"]), r1(f["z_oben"])], "fuss_cm": [r1(pf_["x"]), r1(pf_["y"]), r1(f["z_unten"])],
            "lippe_breite_m": r1(float(pl["b"]) / 100.0, 2),
            "strahl_breite_m": strahl.get("strahl_breite_m") if strahl else None,
            "strahl_quelle": strahl.get("quelle") if strahl else None,
            "kaskadennetz": {"id": kn_id, "bereich_s_m": [r1(f["s_lippe"] - KN["vor_lippe_m"], 2), r1(f["s_fuss"] + KN["nach_fuss_m"], 2)],
                             "vorhang": f["stufe"] in extra["vorhang"]},
            "effekte": [{"quelle": e["_quelle"], "index": e["_index"], "asset": e.get("asset"), "rolle": e.get("rolle"),
                         "cull_m": e.get("cull_m"), "pos_cm": e.get("pos_cm")} for e in eff],
            "gischt": f["fall_m"] >= R["schaum"]["gischt_ab_m"],
            "schaum_objekte": schaum_fuer_fall(f, linie, becken_ende, (strahl or {}).get("strahl_breite_m"), R,
                                               randbloecke, extra.get("ufer_rand"))}
        if eintrag["gischt"]:
            eintrag["gischt_hinweis"] = "Gischt = vorhandene Nature-Water-FX-Effekte dieser Stufe (cull_m aus 13k), kein neues Objekt"
        fl.append(eintrag)
    return abschnitte, fl, wk


def kacheln_bilden(gid, abschnitte, faelle, regeln):
    K = regeln["kacheln"]
    out = []
    cur = None

    def box(a):
        P = np.asarray(a["punkte"], float)
        h = P[:, 3] / 2.0
        return [float((P[:, 0] - h).min()), float((P[:, 1] - h).min()), float((P[:, 0] + h).max()), float((P[:, 1] + h).max())]

    fall_ids = {f["id"] for f in faelle}
    for a in abschnitte:
        b = box(a)
        if cur is not None:
            u = [min(cur["box"][0], b[0]), min(cur["box"][1], b[1]), max(cur["box"][2], b[2]), max(cur["box"][3], b[3])]
            if max(u[2] - u[0], u[3] - u[1]) / 100.0 + 2 * K["rand_m"] <= K["groesse_m"]:
                cur["box"] = u
                cur["abschnitte"].append(a["id"])
                continue
            out.append(cur)
        cur = {"box": b, "abschnitte": [a["id"]]}
    if cur is not None:
        out.append(cur)
    ab = {a["id"]: a for a in abschnitte}
    res = []
    for n, c in enumerate(out):
        r = K["rand_m"] * 100.0
        bx = [r1(c["box"][0] - r), r1(c["box"][1] - r), r1(c["box"][2] + r), r1(c["box"][3] + r)]
        erst, letzt = ab[c["abschnitte"][0]], ab[c["abschnitte"][-1]]
        go = erst["anschluss"]["oben_fall"]
        gu = letzt["anschluss"]["unten_fall"]
        res.append({"id": "%s_K%02d" % (gid, n), "bereich_cm": bx, "abschnitte": c["abschnitte"],
                    "source_river": c["abschnitte"][0], "sink_river": c["abschnitte"][-1],
                    "grenze_oben": "fall" if go in fall_ids else ("laufanfang" if n == 0 else "offen"),
                    "grenze_unten": "fall" if gu in fall_ids else ("laufende" if n == len(out) - 1 else "offen"),
                    "groesse_m": [r1((bx[2] - bx[0]) / 100.0, 1), r1((bx[3] - bx[1]) / 100.0, 1)]})
    return res


# ======================================================================================================================
# Quellen einlesen
# ======================================================================================================================
def gefaelle_gewaesser(gef_basis, lauf, regeln):
    pf = os.path.join(gef_basis, lauf, "plan.json")
    plan = lese_json(pf)
    wk = plan.get("wasser_koerper") or []
    if not wk:
        return None
    linie = linie_aus_koerper(wk, regeln)
    # Becken = geplanter Spiegel zwischen Fuss/Becken-Punkt und naechstem Becken-/Lippenpunkt (spiegel_neu_art);
    # 'alt' (feste Zonen, Bestand) und 'rampe' sind Gerinne, nicht Becken
    sa, art = plan.get("spiegel_neu_s_m") or [], plan.get("spiegel_neu_art") or []
    becken_iv = []
    if sa and len(sa) == len(art):
        for k in range(len(sa) - 1):
            if art[k] in ("fuss", "becken") and art[k + 1] in ("becken", "lippe"):
                becken_iv.append((float(sa[k]), float(sa[k + 1])))
    for i, s_ in enumerate(linie.s):
        if linie.knick[i] in ("becken", "uebergang", "fuss") and becken_iv:
            linie.knick[i] = "becken" if any(a_ - 1e-6 <= s_ <= b_ + 1e-6 for a_, b_ in becken_iv) else "gerinne"
    abst = abstuerze_gefaelle(plan, linie)
    eff = []
    for i, e in enumerate(plan.get("effekte") or []):
        e = dict(e)
        e["_quelle"] = "gefaelle/%s/plan.json#effekte" % lauf
        e["_index"] = i
        eff.append(e)
    strahl = {}
    for st in plan.get("stufen") or []:
        if st.get("strahl_breite_m") is not None:
            strahl[st["id"]] = {"strahl_breite_m": st["strahl_breite_m"], "quelle": "stufen.strahl_breite_m"}
        elif st.get("ueberfall_breite_cm"):
            strahl[st["id"]] = {"strahl_breite_m": r1(st["ueberfall_breite_cm"] / 100.0, 2), "quelle": "stufen.ueberfall_breite_cm"}
    vorhang = set()
    for k in wk:
        vorhang |= set(k.get("vorhang_an_stufen") or [])
    kns = [{"id": k["id"], "s_m": k["s_m"]} for k in wk if k["typ"] == "kaskadennetz"]
    g = {"id": lauf, "art": "gefaelle", "lauf_art": plan.get("art"),
         "quelle": {"plan": "gefaelle/%s/plan.json" % lauf, "wasser_koerper": [k["id"] for k in wk]},
         "strecken": [s["id"] for s in plan.get("strecken") or []]}
    extra = {"effekte": eff, "strahl": strahl, "vorhang": vorhang, "kaskadennetze": kns, "ufer_rand": plan.get("ufer_rand"),
             "becken": becken_aus(abst, linie)}
    return g, linie, abst, extra


def sehens_gewaesser(biom, ort, regeln):
    out = []
    for w in ort.get("wasser") or []:
        if w.get("typ") != "bach":
            continue
        lauf_id = w.get("wasser_koerper_lauf") or "SW_%s_%s" % (ort["id"], w.get("id"))
        wk = w.get("wasser_koerper") or []
        if wk:
            linie = linie_aus_koerper(wk, regeln)
            roh = False
        else:
            P = w.get("punkte_cm") or []
            if len(P) < 2:
                continue
            t = float(w.get("tiefe_cm") or regeln["abschnitt"]["tiefe_min_cm"])
            P = [[p[0], p[1], p[2], p[3] if len(p) > 3 else 100.0, t, 50.0] for p in P]
            linie = linie_aus_punkten(P, regeln)
            roh = True
        abst = abstuerze_sehens(lauf_id, w, linie)
        eff, strahl, vorhang, kns = [], {}, set(), []
        for kk, k in enumerate(wk):
            if k.get("typ") != "kaskadennetz":
                continue
            kns.append({"id": k["id"], "s_m": k["s_m"]})
            vorhang |= set(k.get("vorhang_an_stufen") or [])
            for i, e in enumerate(k.get("effekte") or []):
                e = dict(e)
                e["_quelle"] = "sehens/%s/orte.json#%s/%s/wasser_koerper[%d].effekte" % (biom, ort["id"], w.get("id"), kk)
                e["_index"] = i
                eff.append(e)
            for sb in k.get("stufen_strahl") or []:
                strahl[sb["stufe"]] = {"strahl_breite_m": sb.get("strahl_breite_m"), "quelle": "kaskadennetz.stufen_strahl (13k)"}
        g = {"id": lauf_id, "art": "sehens_bach", "bach": w.get("id"),
             "quelle": {"orte": "sehens/%s/orte.json" % biom, "ort": ort["id"], "bach": w.get("id"),
                        "wasser_koerper": [k["id"] for k in wk]}}
        extra = {"effekte": eff, "strahl": strahl, "vorhang": vorhang, "kaskadennetze": kns, "ufer_rand": None,
                 "becken": becken_aus(abst, linie), "roh": roh}
        out.append((g, linie, abst, extra))
    return out


def roh_gewaesser(lauf, regeln, art):
    linie = linie_aus_punkten(lauf.P, regeln)
    g = {"id": lauf.id, "art": art, "quelle": {"lauf": lauf.quelle, "id": lauf.id, "feld": lauf.feld}}
    extra = {"effekte": [], "strahl": {}, "vorhang": set(), "kaskadennetze": [], "ufer_rand": None,
             "becken": becken_aus([], linie), "roh": True}
    return g, linie, [], extra


# ======================================================================================================================
# Hauptlauf
# ======================================================================================================================
def finde_sw(sehens_basis, sw_ordner, biom):
    for c in ([os.path.join(sw_ordner, "sw_" + biom)] if sw_ordner else []) + \
             [os.path.join(sehens_basis, biom, "sw_" + biom), os.path.join(sehens_basis, "..", "sw_" + biom)]:
        if os.path.isdir(c):
            return c
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Exporter Entscheidung 16: fluss_sim.json je Gewaesser + back_liste.json")
    ap.add_argument("--gefaelle", default=None, help="Ordner mit <lauf>/plan.json (gefaelle_plan.py)")
    ap.add_argument("--sehens", default=None, help="Ordner mit <biom>/orte.json (Sehens-Planer)")
    ap.add_argument("--sw-ordner", default=None, help="Ordner mit sw_<biom>/ (Standard: <sehens>/<biom>/sw_<biom>)")
    ap.add_argument("--strecken", default=STRECKEN_STANDARD)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--regeln", default=REGELN_STANDARD)
    ap.add_argument("--nur", nargs="+", default=None)
    ap.add_argument("--ohne-fluesse", action="store_true")
    ap.add_argument("--ohne-roh", action="store_true", help="Laeufe der 161 Strecken ohne Plan nicht roh exportieren")
    from sehens_lib import daten
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    regeln = lese_json(a.regeln)
    welt = daten.lade(a.daten2m or (None if a.daten1m else os.path.join(RECHERCHE, "vorlagen", "daten", "sehens")),
                      a.daten1m, pfade=False)
    import gefaelle_daten as gd
    masse = Masse()
    pool = Pool(regeln, masse)
    gel = Gelaende(welt)
    gewaesser = []          # (kategorie, ausgabepfad, g, linie, abst, extra)
    nur = set(a.nur) if a.nur else None
    plan_laeufe = []
    if a.gefaelle and os.path.isdir(a.gefaelle):
        for lauf in sorted(os.listdir(a.gefaelle)):
            pf = os.path.join(a.gefaelle, lauf, "plan.json")
            if not os.path.exists(pf):
                continue
            plan_laeufe.append(lauf)
            plan = lese_json(pf)
            gel.delta_hinzu(os.path.join(a.gefaelle, lauf), plan.get("abschnitte"))
            for feld_plan in sorted(glob.glob(os.path.join(a.gefaelle, lauf, "instanzen", "*", "plan.json"))):
                feld = os.path.basename(os.path.dirname(feld_plan))
                pool.lade_ebene(feld_plan, "gefaelle/%s/instanzen/%s/plan.json" % (lauf, feld))
            if nur and lauf not in nur:
                continue
            r = gefaelle_gewaesser(a.gefaelle, lauf, regeln)
            if r:
                gewaesser.append(("gefaelle", os.path.join("gefaelle", lauf, "fluss_sim.json")) + r)
    if a.sehens and os.path.isdir(a.sehens):
        for biom in BIOME:
            po = os.path.join(a.sehens, biom, "orte.json")
            if not os.path.exists(po):
                continue
            od = lese_json(po)
            gel.delta_hinzu(os.path.join(a.sehens, biom), od.get("orte"))
            sw = finde_sw(a.sehens, a.sw_ordner, biom)
            if sw:
                for feld_plan in sorted(glob.glob(os.path.join(sw, "*", "plan.json"))):
                    feld = os.path.basename(os.path.dirname(feld_plan))
                    pool.lade_ebene(feld_plan, "sw_%s/%s/plan.json" % (biom, feld))
            for ort in od.get("orte") or []:
                if nur and ort["id"] not in nur:
                    continue
                for r in sehens_gewaesser(biom, ort, regeln):
                    gewaesser.append(("sehens", os.path.join("sehens", biom, ort["id"], "fluss_sim.json")) + r)
    # Laeufe der 161 Strecken ohne Plan (0 Stufen / kaum planbar) und Fluesse >= 15 m: roher Lauf
    strecken, _ = gd.lade_strecken(a.strecken)
    laeufe_161 = sorted({s["lauf"] for s in strecken})
    ww = welt.wasser_welt or {}
    fluss_ids = sorted(f["id"] for f in ww.get("fluesse", []) or []
                       if max(p[3] for p in f["punkte"]) / 100.0 >= regeln["fluesse"]["breite_min_m"])
    ohne_plan = [l_ for l_ in laeufe_161 if l_ not in plan_laeufe]
    roh = []
    if not a.ohne_roh:
        roh += [(l_, "lauf_ohne_plan") for l_ in ohne_plan]
    if not a.ohne_fluesse:
        roh += [(f, "fluss") for f in fluss_ids if f not in plan_laeufe and f not in ohne_plan]
    for lid, art in roh:
        if nur and lid not in nur:
            continue
        lauf = gd.Lauf.aus_welt(welt, lid)
        r = roh_gewaesser(lauf, regeln, art)
        gewaesser.append(("fluesse" if art == "fluss" else "gefaelle_roh", os.path.join(
            "fluesse" if art == "fluss" else "gefaelle", lid, "fluss_sim.json")) + r)
    pool.fertig()
    log("Gewaesser: %d (gefaelle %d, sehens %d, roh %d), Gelaende-Deltas %d"
        % (len(gewaesser), sum(1 for g in gewaesser if g[0] == "gefaelle"), sum(1 for g in gewaesser if g[0] == "sehens"),
           sum(1 for g in gewaesser if g[0] in ("fluesse", "gefaelle_roh")), len(gel.deltas)))
    # je Gewaesser bauen
    dateien = {}
    for kat, rel, g, linie, abst, extra in gewaesser:
        abschnitte, faelle, wk = baue_gewaesser(g, linie, abst, regeln, pool, extra)
        kach = kacheln_bilden(g["id"], abschnitte, faelle, regeln)
        eintrag = {"id": g["id"], "kategorie": kat, "art": g["art"], "quelle": g["quelle"], "laenge_m": r1(linie.s[-1] - linie.s[0], 2),
                   "abstuerze": [{"id": d["id"], "s_lippe_m": r1(d["s_lippe"], 2), "s_fuss_m": r1(d["s_fuss"], 2),
                                  "fall_m": r1(d["fall_m"], 2), "rampe": d["rampe"]} for d in abst],
                   "abschnitte": abschnitte, "faelle": faelle, "wasser_kollision": wk, "sim_bereiche": kach,
                   "effekte_ohne_fall": sorted({e["_quelle"] + "[%d]" % e["_index"] for e in extra["effekte"]}
                                               - {x["quelle"] + "[%d]" % x["index"] for f in faelle for x in f["effekte"]})}
        for key in ("strecken", "lauf_art", "bach"):
            if g.get(key) is not None:
                eintrag[key] = g[key]
        dateien.setdefault(rel, []).append(eintrag)
    # Fingerabdruecke je Kachel
    fpr = regeln["fingerabdruck"]
    kol_global = {}
    for rel, liste in dateien.items():
        for e in liste:
            for o in e["wasser_kollision"]:
                key = json.dumps(o["ref"], sort_keys=True)
                kol_global[key] = o
    kol_keys = sorted(kol_global)
    ref_index = {}
    for k, r in enumerate(pool.recs):
        ref_index[json.dumps(pool.ref(k), sort_keys=True)] = k
    kol_k = np.array([ref_index[k_] for k_ in kol_keys], int) if kol_keys else np.zeros(0, int)
    back = []
    for rel in sorted(dateien):
        for e in dateien[rel]:
            ab = {a_["id"]: a_ for a_ in e["abschnitte"]}
            for kc in e["sim_bereiche"]:
                bx = kc["bereich_cm"]
                x0, y0, rcm, H = gel.raster(bx)
                gt = fp_gelaende_text(x0, y0, rcm, H, fpr["hoehe_quant_cm"])
                st = fp_splines_text([(i, ab[i]["punkte"]) for i in kc["abschnitte"]], fpr["spline_quant_cm"])
                objs = []
                if len(kol_k):
                    lo, hi = pool.lo[kol_k], pool.hi[kol_k]
                    sel = (hi[:, 0] >= bx[0]) & (lo[:, 0] <= bx[2]) & (hi[:, 1] >= bx[1]) & (lo[:, 1] <= bx[3])
                    for k in kol_k[sel]:
                        v = pool.recs[k]["v"]
                        objs.append([pool.recs[k]["pfad"]] + [float(x) for x in v[:10]])
                ot = fp_objekte_text(objs, fpr["pos_quant_cm"], fpr["quat_quant"], fpr["skala_quant"])
                ges, teile = fingerabdruck(gt, st, ot, fpr["version"])
                kc["fingerabdruck"] = ges
                kc["fingerabdruck_teile"] = teile
                kc["n_hoehen"] = int(H.size)
                kc["raster_cm"] = r1(rcm, 1)
                kc["n_objekte"] = len(objs)
                back.append({"kachel": kc["id"], "gewaesser": e["id"], "datei": rel.replace(os.sep, "/"), "bereich_cm": bx,
                             "abschnitte": kc["abschnitte"], "grenze_oben": kc["grenze_oben"], "grenze_unten": kc["grenze_unten"],
                             "fingerabdruck": ges, "teile": teile, "n_hoehen": int(H.size), "n_objekte": len(objs)})
    # schreiben
    zus = {"kategorien": {}, "summe": {}}
    for rel in sorted(dateien):
        liste = dateien[rel]
        d = {"format": FORMAT_VERSION, "regeln_version": regeln["version"], "fall_schwelle_m": regeln["fall_schwelle_m"],
             "daten": "1m" if a.daten1m else "2m (Cloud-Test)", "gewaesser": liste}
        schreibe_json(os.path.join(a.aus, rel), d)
        for e in liste:
            z = zus["kategorien"].setdefault(e["kategorie"], {"dateien": set(), "gewaesser": 0, "abschnitte": 0, "faelle": 0,
                                                             "kollision": 0, "kollision_im_wasser": 0, "schaum": {},
                                                             "kacheln": 0, "laenge_m": 0.0, "abschnitte_innen_faelle": 0,
                                                             "abschnitte_kurz_m": []})
            z["dateien"].add(rel)
            z["gewaesser"] += 1
            z["abschnitte"] += len(e["abschnitte"])
            z["faelle"] += len(e["faelle"])
            z["kollision"] += len(e["wasser_kollision"])
            z["kollision_im_wasser"] += sum(1 for o in e["wasser_kollision"] if o["lage"] == "im_wasser")
            z["kacheln"] += len(e["sim_bereiche"])
            z["laenge_m"] += e["laenge_m"]
            z["abschnitte_innen_faelle"] += sum(len(a_["faelle_innen"]) for a_ in e["abschnitte"])
            for f in e["faelle"]:
                for s in f["schaum_objekte"]:
                    z["schaum"][s["art"]] = z["schaum"].get(s["art"], 0) + 1
    ges = {"gewaesser": 0, "abschnitte": 0, "faelle": 0, "kollision": 0, "kollision_im_wasser": 0, "kacheln": 0, "laenge_m": 0.0,
           "schaum": {}, "dateien": 0, "abschnitte_innen_faelle": 0}
    for k, z in zus["kategorien"].items():
        z["dateien"] = len(z["dateien"])
        z["laenge_m"] = r1(z["laenge_m"], 1)
        del z["abschnitte_kurz_m"]
        for key in ("gewaesser", "abschnitte", "faelle", "kollision", "kollision_im_wasser", "kacheln", "dateien",
                    "abschnitte_innen_faelle"):
            ges[key] += z[key]
        ges["laenge_m"] = r1(ges["laenge_m"] + z["laenge_m"], 1)
        for s, n in z["schaum"].items():
            ges["schaum"][s] = ges["schaum"].get(s, 0) + n
    zus["summe"] = ges
    zus["kollision_objekte_eindeutig"] = len(kol_global)
    zus["objekt_pool"] = {"objekte": len(pool.recs), "fest_und_gross": int(pool.fest.sum())}
    zus["fluesse_ab_15m"] = fluss_ids
    zus["laeufe_161_ohne_plan"] = ohne_plan
    zus["daten"] = "1m" if a.daten1m else "2m (Cloud-Test)"
    zus["kategorien"] = {k: zus["kategorien"][k] for k in sorted(zus["kategorien"])}
    schreibe_json(os.path.join(a.aus, "zusammenfassung.json"), zus)
    schreibe_json(os.path.join(a.aus, "back_liste.json"),
                  {"format": "back_liste_v1", "fingerabdruck": dict(fpr, formel="siehe README fluss_sim, Abschnitt Fingerabdruck"),
                   "kacheln": back})
    log("geschrieben: %d Dateien, %d Gewaesser, %d Abschnitte, %d Faelle, %d Kollisionsobjekte (%d eindeutig), %d Kacheln"
        % (len(dateien), ges["gewaesser"], ges["abschnitte"], ges["faelle"], ges["kollision"], len(kol_global), ges["kacheln"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
