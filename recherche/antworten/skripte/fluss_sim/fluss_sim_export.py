#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fluss_sim_export.py - Exporter fuer Entscheidung 16 (Shallow Water River fuer alle Baeche und Fluesse).

Liest NUR die vorhandenen Planer-Ausgaben (gefaelle_plan.py: <lauf>/plan.json + instanzen/, Sehens-Planer:
<biom>/orte.json + sw_<biom>/) und die Weltdaten. Aendert nichts an Planern, Stufen, Becken oder Gelaende
(13f-Regel: die Treppen der Sehens-Baeche bleiben exakt). Format v3 (16c, Ferat 12.10.2026):

  Gewaesser         EIN WaterBodyRiver je Gewaesser von der Quelle bis zur Muendung (See, Fluss/Bach, Meer), ueber
                    alle Faelle und Feldgrenzen hinweg. Die Welt-Laeufe (wasser_welt.json je Feld, baeche_alle.json,
                    mit Gefaelle-Plan oder roh) werden an ihren Enden verkettet; Sehens-Baeche sind je ein Gewaesser.
  water_body        die eine Spline (x, y, z, Breite, Tiefe, Tempo je Punkt) mit Punktrollen; jede Stufe hat einen
                    Punkt an der Lippe (Oberwasser) und einen am Fuss (Unterwasser), dazwischen 2-4 m (roh 5-10 m).
  muendung          Art (meer, see, fluss, bach, versickert, wasserfall, offen), Ziel, Muendungspunkt; zufluesse.
  bereiche          die frueheren Abschnitte zwischen den Faellen nur noch als s-Bereiche mit Rolle
  faelle            je Einzelabsturz >= fall_schwelle_m: Lippe/Fuss, Effekte, vorhang (Regel 16b) und nur dann
                    Kaskadennetz-Bereich und schaum_objekte (wie 16/16a; Vorhaenge warten auf Ferat)
  swr_bereiche      EINE ShallowWaterRiver je Gewaesser (16c Nachtrag 17:45): Rechteck um den Fluss, resolution_max_axis =
                    laengste Seite / Zielzelle (Bach 0,25 m, Fluss 0,35 m) bis 2048; nur wenn die Zelle dann ueber
                    0,30 m (Bach) bzw. 0,35 m (Fluss) laege, wenige lange Teilstuecke auf demselben Fluss (kleinste
                    Rechteckflaeche, nicht an Faellen). Je SWR Hindernis-Akteur WH_<swr> und Fingerabdruck.
  wasser_kollision  alle festen Instanzen/Akteure im Wasser oder <= 1 m daneben (ueberspannte ohne, 16a E5)

und global back_liste.json (je SWR-Bereich: Fingerabdruck, Reihenfolge) sowie zusammenfassung.json.

Aufruf (Cloud, 2 m):
  python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py \
      --gefaelle <scratch>/gef --sehens <scratch>/sehens --daten2m recherche/vorlagen/daten/sehens --aus <scratch>/fs
Lokal (1 m):
  python -I .../fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle --sehens export/unreal/welt/sehens \
      --sw-ordner export/unreal/welt --daten1m export/unreal/welt --aus export/unreal/welt/fluss_sim
Optionen: --nur ID ... (Gewaesser-, Lauf- oder Ort-IDs; verkettet wird immer ueber alle Laeufe), --regeln DATEI.

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
NETZE_CSV = os.path.join(RECHERCHE, "vorlagen", "daten", "netze.csv")
NETZE_MASSE = os.path.join(RECHERCHE, "vorlagen", "daten", "netze_masse.json")
BIOME = ("aue", "bergwald", "canyon", "dschungel", "elfenwald", "fjord", "frost", "gletscher", "heide",
         "kueste", "lava", "oedland", "sumpf", "tundra", "wueste")
FORMAT_VERSION = "fluss_sim_v3"
BACK_FORMAT = "back_liste_v3"


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
    zeilen = ["G|r=%d|x0=%d|y0=%d|nx=%d|ny=%d|q=%d" % (qrund(raster_cm, 1), qrund(x0_cm, 1), qrund(y0_cm, 1),
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
                            "z_unten": zu, "fall_m": float(t["fall_m"]), "rampe": bool(t.get("rampe")) or rampe_st,
                            "versatz_m": None, "holz": bool(st.get("holzstufe")), "klasse": st.get("klasse")})
        else:
            sl = float(st["s_m"])
            zo = float(st["lippe_cm"][0][2]) if st.get("lippe_cm") else linie.z_bei(sl, "oben")
            zu = float(st.get("fuss_z_cm", zo - 100 * st["fall_m"]))
            # Versatz Lippe -> Fuss (horizontal, m): Ueberfall-Mitte bzw. Mitte der Lippenpunkte gegen den Fuss
            lp = st.get("ueberfall_cm")
            if not lp and st.get("lippe_cm"):
                lp = list(np.mean(np.asarray(st["lippe_cm"], float)[:, :2], axis=0))
            fp = st.get("fuss_cm")
            versatz = math.hypot(lp[0] - fp[0], lp[1] - fp[1]) / 100.0 if (lp and fp) else None
            out.append({"id": st["id"], "stufe": st["id"], "teil": 0, "art": st.get("art"), "art_regel": st.get("art_regel"),
                        "s_lippe": sl, "z_oben": zo, "z_unten": zu, "fall_m": float(st["fall_m"]), "rampe": rampe_st,
                        "versatz_m": versatz, "holz": bool(st.get("holzstufe")), "klasse": st.get("klasse")})
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
                    "fall_m": float(st["fall_m"]), "rampe": st.get("art") == "schnelle", "s_fuss_proj": sf_proj,
                    "versatz_m": math.hypot(lp[0] - fp[0], lp[1] - fp[1]) / 100.0, "holz": False, "klasse": None})
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


def segmente_bilden(linie, faelle, regeln):
    """Becken-Segmente zwischen den Faellen; Reste am Laufrand weg, zu kurze Becken talwaerts zusammenfassen."""
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
    return seg


# ======================================================================================================================
# Vorhang-Regel (16b), Zelle, Typ
# ======================================================================================================================
def vorhang_regel(d, regeln):
    """Vorhang (Kaskadennetz) + Schaumobjekte nur an einer echten Fallkante (16b). Rueckgabe (bool, grund)."""
    V = regeln["vorhang"]
    if d.get("rampe"):
        return False, "schnelle/rampe"
    if d.get("teil"):
        return False, "kaskaden-teilstufe (Simulation zeichnet Rinne)"
    D = float(d["fall_m"])
    if D >= V["ab_m"] - 1e-9:
        return True, "einzelabsturz >= %.1f m" % V["ab_m"]
    vs = d.get("versatz_m")
    if (D >= V["senkrecht_ab_m"] - 1e-9 and vs is not None and vs <= V["senkrecht_versatz_max_anteil"] * D + 1e-9
            and d.get("art") in V["felsstufe_arten"] and not d.get("holz")):
        return True, "senkrechte felslippe (versatz %.2f m <= %.1f x fall)" % (vs, V["senkrecht_versatz_max_anteil"])
    if D >= V["senkrecht_ab_m"] - 1e-9:
        return False, "%.1f-%.1f m ohne senkrechte felslippe (versatz %s)" % (
            V["senkrecht_ab_m"], V["ab_m"], "unbekannt" if vs is None else "%.2f m" % vs)
    return False, "unter %.1f m (Simulation zeichnet Rinne)" % V["senkrecht_ab_m"]


def zelle_fuer(achse_m, ziel_m, S):
    res = int(math.ceil(achse_m / ziel_m / S["resolution_schritt"] - 1e-9)) * S["resolution_schritt"]
    res = max(S["resolution_min"], min(S["resolution_max"], res))
    return res, achse_m / res


def swr_typ(linie, abst, extra, regeln):
    """bach: Abstuerze im Plan oder Median der Breite < fluss_breite_median_ab_m; sonst fluss."""
    S = regeln["swr"]
    ds = np.diff(linie.s)
    bm = 0.5 * (linie.b[1:] + linie.b[:-1]) if len(linie.s) > 1 else linie.b
    if len(ds) and ds.sum() > 0:
        o = np.argsort(bm)
        c = np.cumsum(ds[o])
        med = float(bm[o][int(np.searchsorted(c, 0.5 * c[-1]))]) / 100.0
    else:
        med = float(np.median(linie.b)) / 100.0
    hat_stufen = any(d["fall_m"] > 0 for d in abst)
    return ("bach" if (hat_stufen or med < S["fluss_breite_median_ab_m"]) else "fluss"), med
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
             "becken": becken_aus(abst, linie), "zufluesse": plan.get("zufluesse") or []}
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
# v3 (16c): Gewaesser = ein WaterBodyRiver von der Quelle bis zur Muendung
# ======================================================================================================================
class Teil:
    """Ein Lauf als Baustein eines Gewaessers: Welt-Lauf (Gefaelle-Plan oder roh) oder Sehens-Bach."""

    def __init__(self, tid, art, herkunft, g, linie, abst, extra, familie=None, netz=None, feld=None, anschluss=None,
                 sehens=None):
        self.id = tid
        self.art = art                  # fluss | bach | sehens_bach
        self.herkunft = herkunft        # plan | roh | sehens
        self.g = g
        self.linie = linie
        self.abst = abst
        self.extra = extra
        self.familie = familie
        self.netz = netz
        self.feld = feld
        self.anschluss = anschluss or {}
        self.sehens = sehens
        L = linie
        h = np.maximum(L.b, 10.0) / 2.0
        self.box = (float((L.x - h).min()), float((L.y - h).min()), float((L.x + h).max()), float((L.y + h).max()))
        self.s0, self.s1 = float(L.s[0]), float(L.s[-1])

    @property
    def roh(self):
        return bool(self.extra.get("roh"))


def projektion(L, x_cm, y_cm):
    """Lot eines Punkts auf die Mittellinie L (Linie). Rueckgabe (abstand_m, s_m, z_cm, breite_cm)."""
    if len(L.s) < 2:
        return math.hypot(L.x[0] - x_cm, L.y[0] - y_cm) / 100.0, float(L.s[0]), float(L.z[0]), float(L.b[0])
    ax, ay, bx, by = L.x[:-1], L.y[:-1], L.x[1:], L.y[1:]
    abx, aby = bx - ax, by - ay
    t = np.clip(((x_cm - ax) * abx + (y_cm - ay) * aby) / np.maximum(abx * abx + aby * aby, 1e-9), 0.0, 1.0)
    d = np.hypot(x_cm - (ax + t * abx), y_cm - (ay + t * aby))
    k = int(np.argmin(d))
    s = float(L.s[k] + t[k] * (L.s[k + 1] - L.s[k]))
    return float(d[k]) / 100.0, s, float(L.z[k] + t[k] * (L.z[k + 1] - L.z[k])), float(L.b[k] + t[k] * (L.b[k + 1] - L.b[k]))


def punkt_in_polygon(U, x, y):
    U = np.asarray(U, float)
    x1, y1 = U[:, 0], U[:, 1]
    x2, y2 = np.roll(x1, -1), np.roll(y1, -1)
    kreuz = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / np.where(y2 - y1 == 0, 1e-12, y2 - y1) + x1)
    return bool(np.count_nonzero(kreuz) % 2)


def abstand_polygon(U, x, y):
    """Abstand (m) eines Punkts (cm) zum Rand des Polygons U (cm); 0 innen."""
    if punkt_in_polygon(U, x, y):
        return 0.0
    U = np.asarray(U, float)
    A, B = U, np.roll(U, -1, axis=0)
    AB = B - A
    t = np.clip(((x - A[:, 0]) * AB[:, 0] + (y - A[:, 1]) * AB[:, 1]) / np.maximum((AB ** 2).sum(1), 1e-9), 0, 1)
    return float(np.hypot(x - (A[:, 0] + t * AB[:, 0]), y - (A[:, 1] + t * AB[:, 1])).min()) / 100.0


def fortsetzung_test(P, N, G):
    """Faengt N dort an, wo P endet? Rueckgabe dict (art anschluss/ueberlappung) oder None."""
    LP, LN = P.linie, N.linie
    ex, ey, ez = float(LP.x[-1]), float(LP.y[-1]), float(LP.z[-1])
    ax, ay, az = float(LN.x[0]), float(LN.y[0]), float(LN.z[0])
    d = math.hypot(ex - ax, ey - ay) / 100.0
    dzmax = G["fortsetzung_dz_max_cm"]
    if d <= G["fortsetzung_abstand_m"] and az <= ez + dzmax:
        return {"art": "anschluss", "abstand_m": d, "s_n": N.s0, "s_p": P.s1}
    ue = G["fortsetzung_ueberlappung_max_m"]
    dn, sn, zn, _ = projektion(LN, ex, ey)
    if dn > G["fortsetzung_quer_m"] or not (N.s0 < sn <= N.s0 + ue) or abs(zn - ez) > G["ueberlappung_dz_max_cm"]:
        return None
    dp, sp, _, _ = projektion(LP, ax, ay)
    if dp > G["fortsetzung_quer_m"] or not (P.s1 - ue <= sp < P.s1):
        return None
    return {"art": "ueberlappung", "abstand_m": dn, "s_n": sn, "s_p": sp}


def familie_name(teile, vergeben):
    fam = [t.familie for t in teile if t.art == "fluss" and t.familie]
    if fam:
        pre = os.path.commonprefix(fam).rstrip("_")
        name = pre if len(pre) >= 4 else fam[0]
    else:
        name = teile[0].id
    if name in vergeben:
        name = "%s__%s" % (name, teile[0].id)
    return name


def ausschnitt(L, a, b):
    """Punkte der Linie L im Bereich [a, b] (lokales s) inklusive interpolierter Randpunkte."""
    m = (L.s > a + 1e-6) & (L.s < b - 1e-6)
    ia = int(np.clip(np.searchsorted(L.s, a), 0, len(L.s) - 1))
    ib = int(np.clip(np.searchsorted(L.s, b) - 1, 0, len(L.s) - 1))
    wa, wb = L.bei(a), L.bei(b)
    S = np.concatenate([[a], L.s[m], [b]])
    out = {"s": S}
    for k in ("x", "y", "z", "b", "t", "v"):
        out[k] = np.concatenate([[float(wa[k])], getattr(L, k)[m], [float(wb[k])]])
    za = L.z_bei(a, "unten")
    out["z"][0] = min(za, out["z"][0]) if a > L.s[0] + 1e-6 else float(L.z[0])
    out["z"][-1] = float(L.z[-1]) if b >= L.s[-1] - 1e-6 else float(out["z"][-1])
    out["knick"] = [L.knick[ia]] + [L.knick[i] for i in np.where(m)[0]] + [L.knick[ib]]
    return out


def zusammenfuegen(kette, links, regeln):
    """Verkettet die Linien der Teile zu einer Gewaesser-Linie. An Ueberlappungen (Feldgrenzen) wird das Teil ohne Plan
    gekuerzt, sonst das untere. Rueckgabe (linie, abst, extra, laeufe)."""
    cut = [[t.s0, t.s1] for t in kette]
    for i, l in enumerate(links):
        if l["art"] == "ueberlappung":
            P, N = kette[i], kette[i + 1]
            if N.herkunft == "plan" and P.herkunft != "plan":
                cut[i][1] = l["s_p"]
            else:
                cut[i + 1][0] = l["s_n"]
    S, X, Y, Z, B, T, V, K = [], [], [], [], [], [], [], []
    abst, eff, strahl, vorhang, kns = [], [], {}, set(), []
    ufer = {"s_m": [], "einzug_links_m": [], "einzug_rechts_m": []}
    laeufe = []
    ende = None
    for i, t in enumerate(kette):
        a, b = cut[i]
        A = ausschnitt(t.linie, a, b)
        if ende is None:
            off = -a
        else:
            gap = max(math.hypot(A["x"][0] - ende[0], A["y"][0] - ende[1]) / 100.0, 1e-3)
            off = ende[2] + gap - a
        S += list(A["s"] + off)
        X += list(A["x"]); Y += list(A["y"]); Z += list(A["z"]); B += list(A["b"]); T += list(A["t"]); V += list(A["v"])
        K += list(A["knick"])
        ende = (float(A["x"][-1]), float(A["y"][-1]), float(A["s"][-1] + off))
        weg = []
        for d in t.abst:
            if a - 1e-6 <= d["s_lippe"] <= b + 1e-6:
                e = dict(d)
                for k in ("s_lippe", "s_fuss", "s_fuss_proj"):
                    if e.get(k) is not None:
                        e[k] = e[k] + off
                e["s_fuss"] = min(e["s_fuss"], b + off)
                e["lauf"] = t.id
                abst.append(e)
            else:
                weg.append(d["id"])
        stufen_da = {d["stufe"] for d in t.abst if d["id"] not in weg}
        for e in t.extra.get("effekte") or []:
            if e.get("stufe") and e["stufe"] not in stufen_da and any(d["stufe"] == e["stufe"] for d in t.abst):
                continue
            eff.append(e)
        strahl.update(t.extra.get("strahl") or {})
        vorhang |= set(t.extra.get("vorhang") or set())
        for k in t.extra.get("kaskadennetze") or []:
            if k["s_m"][1] >= a - 1e-6 and k["s_m"][0] <= b + 1e-6:
                kns.append({"id": k["id"], "s_m": [k["s_m"][0] + off, k["s_m"][1] + off]})
        u = t.extra.get("ufer_rand") or {}
        su = u.get("s_m") or []
        if su and all(len(u.get(k_) or []) == len(su) for k_ in ("einzug_links_m", "einzug_rechts_m")):
            for j, s_ in enumerate(su):
                if a - 1e-6 <= s_ <= b + 1e-6:
                    ufer["s_m"].append(s_ + off)
                    ufer["einzug_links_m"].append(u["einzug_links_m"][j])
                    ufer["einzug_rechts_m"].append(u["einzug_rechts_m"][j])
        q = dict(t.g["quelle"])
        laeufe.append({"id": t.id, "art": t.art, "herkunft": t.herkunft, "feld": t.feld,
                       "s_m": [r1(a + off, 2), r1(b + off, 2)], "s_quelle_m": [r1(a, 2), r1(b, 2)],
                       "gekuerzt_m": [r1(a - t.s0, 2), r1(t.s1 - b, 2)], "quelle": q,
                       "abstuerze_entfallen": sorted(weg),
                       "anschluss_oben": None if i == 0 else links[i - 1]["art"]})
    linie = Linie(S, X, Y, Z, B, T, V, K)
    abst.sort(key=lambda d: (d["s_lippe"], d["id"]))
    extra = {"effekte": eff, "strahl": strahl, "vorhang": vorhang, "kaskadennetze": kns,
             "ufer_rand": ufer if ufer["s_m"] else None, "roh": all(t.roh for t in kette)}
    return linie, abst, extra, laeufe


def stufen_ordnen(abst, s0, s1, regeln):
    """Lippe/Fuss je Absturz so, dass jede Stufe zwei Splinepunkte bekommt: Fuss >= Lippe + stufe_dx_min_m, Fuss <=
    naechste Lippe (sonst teilen sich Fuss und naechste Lippe einen Punkt), alles in [s0, s1]."""
    dx = regeln["spline"]["stufe_dx_min_m"]
    abst.sort(key=lambda d: (d["s_lippe"], d["id"]))
    for i, d in enumerate(abst):
        d["s_lippe"] = min(max(d["s_lippe"], s0), s1)
        nxt = abst[i + 1]["s_lippe"] if i + 1 < len(abst) else s1
        d["s_fuss"] = min(max(d["s_fuss"], d["s_lippe"] + dx), max(nxt, d["s_lippe"]), s1)
    return abst


def gewaesser_spline(linie, abst, roh_bei, regeln):
    """Die eine Spline des Gewaessers: Anfang, Ende, je Stufe Lippe (Oberwasser) und Fuss (Unterwasser), dazwischen
    gleichmaessig mit Abstand >= ziel (2 m; roh 5 m). Rueckgabe dict (water_body.spline) + Punkt-Index je Stufe."""
    SP = regeln["spline"]
    R = regeln["abschnitt"]
    s0, s1 = float(linie.s[0]), float(linie.s[-1])
    zus = SP["zusammen_m"]
    anker = []
    for d in abst:
        anker.append((d["s_lippe"], 1, "lippe", d))
        anker.append((d["s_fuss"], 0, "fuss", d))
    anker.sort(key=lambda t_: (t_[0], t_[1], t_[3]["id"]))
    gruppen = []
    for it in anker:
        if gruppen and it[0] - gruppen[-1]["s"] < zus:
            gruppen[-1]["teile"].append(it)
        else:
            gruppen.append({"s": it[0], "teile": [it]})
    if not gruppen or gruppen[0]["s"] > s0 + zus:
        gruppen.insert(0, {"s": s0, "teile": []})
    else:
        gruppen[0]["s"] = s0 if gruppen[0]["s"] - s0 < zus else gruppen[0]["s"]
    if gruppen[-1]["s"] < s1 - zus:
        gruppen.append({"s": s1, "teile": []})
    else:
        gruppen[-1]["s"] = s1
    ss, gr = [], []
    for k, gq in enumerate(gruppen):
        if k > 0:
            vor = gruppen[k - 1]
            sturz = any(r == "lippe" and any(r2 == "fuss" and d2 is d for _, _, r2, d2 in gq["teile"])
                        for _, _, r, d in vor["teile"])
            g_ = gq["s"] - vor["s"]
            if not sturz:
                roh_ = all(roh_bei(x) for x in (vor["s"], 0.5 * (vor["s"] + gq["s"]), gq["s"]))
                ziel = SP["abstand_roh_m"] if roh_ else SP["abstand_m"]
                n = max(1, int(math.floor(g_ / ziel + 1e-9)))
                for m in range(1, n):
                    ss.append(vor["s"] + g_ * m / n)
                    gr.append(None)
        ss.append(gq["s"])
        gr.append(gq)
    ss = np.asarray(ss, float)
    w = linie.bei(ss)
    z, rollen, ptyp = [], [], []
    stufe_punkt = {}
    for i, (s_, gq) in enumerate(zip(ss, gr)):
        if gq is not None and gq["teile"]:
            zz = []
            rr = set()
            for _, _, r, d in gq["teile"]:
                zz.append(d["z_oben"] if r == "lippe" else d["z_unten"])
                rr.add(r)
                stufe_punkt.setdefault(d["id"], {})[r] = i
            z.append(min(zz))
            rollen.append("fuss_lippe" if len(rr) == 2 else rr.pop())
            ptyp.append("LINEAR")
            continue
        z.append(linie.z_bei(s_, "unten"))
        ptyp.append("CURVE_CLAMPED")
        k = int(np.clip(np.searchsorted(linie.s, s_), 0, len(linie.s) - 1))
        kk = [j for j in (k - 1, k) if 0 <= j < len(linie.s)]
        r_ = [linie.knick[j] for j in kk]
        rollen.append("becken" if all(x in ("becken", "uebergang", "fuss") for x in r_) else
                      ("rampe" if "rampe" in r_ else ("gerinne" if "gerinne" in r_ else
                                                      (r_[-1] if r_[-1] in ("river", "roh") else "rinne"))))
    z = np.minimum.accumulate(np.asarray(z, float))
    # Becken nur, wo der Spiegel wirklich flach ist (Sehens-Linien haben zwischen Stufen teils Gefaelle)
    for i, r in enumerate(rollen):
        if r == "becken":
            for j in (i - 1, i + 1):
                if 0 <= j < len(ss) and abs(ss[j] - ss[i]) > 0.2 and \
                        abs(z[i] - z[j]) / 100.0 / abs(ss[j] - ss[i]) > R["becken_gefaelle_max"]:
                    rollen[i] = "rinne"
    v = np.clip(w["v"], R["velocity_min_cm_s"], R["velocity_max_cm_s"])
    pts = [[r1(w["x"][i]), r1(w["y"][i]), r1(z[i]), r1(max(w["b"][i], 10.0)), r1(max(w["t"][i], R["tiefe_min_cm"])), r1(v[i])]
           for i in range(len(ss))]
    P = np.array([p[:3] for p in pts])
    tang = []
    for i in range(len(pts)):
        p0 = P[max(i - 1, 0)]
        p1 = P[min(i + 1, len(pts) - 1)]
        den = 2.0 if 0 < i < len(pts) - 1 else 1.0
        t = (p1 - p0) / den
        dz0 = P[i][2] - P[i - 1][2] if i > 0 else None
        dz1 = P[i + 1][2] - P[i][2] if i < len(pts) - 1 else None
        if ptyp[i] == "LINEAR" or (dz0 is not None and abs(dz0) < 0.5) or (dz1 is not None and abs(dz1) < 0.5):
            t[2] = 0.0
        else:
            cand = [abs(x) for x in (dz0, dz1) if x is not None]
            t[2] = -min(cand) if cand else 0.0
        tang.append([r1(t[0]), r1(t[1]), r1(t[2])])
    sp = {"s_m": [r1(s0, 2), r1(s1, 2)], "punkte": pts,
          "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
          "punkt_typen": ptyp, "tangenten_cm": tang, "punkte_s_m": [r1(x, 2) for x in ss], "punkt_rollen": rollen}
    return sp, stufe_punkt


def kachel_index(ss, a, b):
    """Index-Bereich der Splinepunkte, der [a, b] ganz abdeckt (letzter Punkt <= a bis erster Punkt >= b)."""
    ss = np.asarray(ss, float)
    i0 = int(np.searchsorted(ss, a + 1e-6, side="right") - 1)
    i1 = int(np.searchsorted(ss, b - 1e-6, side="left"))
    return max(i0, 0), min(i1, len(ss) - 1)


def box_punkte(P, i0, i1):
    Q = np.asarray(P, float)[i0:i1 + 1]
    h = Q[:, 3] / 2.0
    return [float((Q[:, 0] - h).min()), float((Q[:, 1] - h).min()), float((Q[:, 0] + h).max()), float((Q[:, 1] + h).max())]


def achse_von(box):
    return max(box[2] - box[0], box[3] - box[1]) / 100.0


def swr_teilen(sp, abst, becken, regeln, L_max):
    """Teilt die Simulation eines Gewaessers in moeglichst wenige SWR-Bereiche (Nachtrag 17:45): Rechteck je Bereich
    (Splinepunkte des Simulationsbereichs inkl. halber Ueberlappung je Naht, +- halbe Breite) mit laengster Seite <=
    L_max (Array je Splinepunkt; je Bereich gilt das Minimum). Unter den Teilungen mit der kleinsten Anzahl wird die mit
    der kleinsten Rechteckflaeche gewaehlt (gewundene/diagonale Laeufe). Naht an einem Splinepunkt, nicht naeher als
    naht_abstand_absturz_m an einer Stufe. Rueckgabe Liste {a, b, naht_oben, naht_unten}."""
    T = regeln["swr"]["teilung"]
    ue = T["ueberlappung_m"] / 2.0
    ss = np.asarray(sp["punkte_s_m"], float)
    P = np.asarray(sp["punkte"], float)
    LM = np.broadcast_to(np.asarray(L_max, float), ss.shape)
    n = len(ss)
    s0, s1 = float(ss[0]), float(ss[-1])
    sperr = [(d["s_lippe"] - T["naht_abstand_absturz_m"], d["s_fuss"] + T["naht_abstand_absturz_m"]) for d in abst]
    kand = [0] + [i for i in range(1, n - 1)
                  if ss[i] - s0 >= T["min_teil_m"] and s1 - ss[i] >= T["min_teil_m"]
                  and not any(a_ <= ss[i] <= b_ for a_, b_ in sperr)] + [n - 1]
    h = P[:, 3] / 2.0
    lo_x, hi_x, lo_y, hi_y = P[:, 0] - h, P[:, 0] + h, P[:, 1] - h, P[:, 1] + h
    i_lo = [kachel_index(ss, max(s0, ss[k] - ue), max(s0, ss[k] - ue))[0] if k > 0 else 0 for k in kand]
    i_hi = [kachel_index(ss, min(s1, ss[k] + ue), min(s1, ss[k] + ue))[1] if k < n - 1 else n - 1 for k in kand]
    m = len(kand)
    INF = (10 ** 9, float("inf"))
    best = [INF] * m
    vor = [-1] * m
    best[0] = (0, 0.0)
    for a in range(m - 1):
        if best[a] == INF:
            continue
        i0 = i_lo[a]
        x0, x1, y0, y1 = lo_x[i0], hi_x[i0], lo_y[i0], hi_y[i0]
        lim = float(LM[i0])
        j = i0
        for b in range(a + 1, m):
            i1 = i_hi[b]
            while j < i1:
                j += 1
                x0, x1, y0, y1 = min(x0, lo_x[j]), max(x1, hi_x[j]), min(y0, lo_y[j]), max(y1, hi_y[j])
                lim = min(lim, float(LM[j]))
            if max(x1 - x0, y1 - y0) / 100.0 > lim + 1e-9:
                break
            c = (best[a][0] + 1, best[a][1] + (x1 - x0) * (y1 - y0) / 1e4)
            if c < best[b]:
                best[b], vor[b] = c, a
    if best[m - 1] == INF:                       # nicht teilbar (Breite allein > L_max): an jedem Kandidaten teilen
        wege = list(range(m))
    else:
        wege, k = [], m - 1
        while k >= 0:
            wege.append(k)
            k = vor[k]
        wege.reverse()
    nahte = [float(ss[kand[k]]) for k in wege]

    def art(x):
        return "becken" if any(bk["s_m"][0] <= x <= bk["s_m"][1] for bk in becken) else "lauf"
    out = []
    for q in range(len(nahte) - 1):
        a_, b_ = nahte[q], nahte[q + 1]
        out.append({"a": a_, "b": b_,
                    "naht_oben": {"art": "quelle", "s_m": s0} if q == 0 else {"art": art(a_), "s_m": a_},
                    "naht_unten": {"art": "muendung", "s_m": s1} if q == len(nahte) - 2 else {"art": art(b_), "s_m": b_}})
    return out


def kollision_v3(pool, pts, ss, regeln):
    """Wasser-Kollision entlang der einen Spline. Rueckgabe Liste (k, s_m, rand_m, lage, d_m, halb_m, ueber_m)."""
    R = regeln["kollision"]
    if not len(pool.recs) or len(pts) < 2:
        return []
    P = np.asarray(pts, float) / np.array([100, 100, 100, 100, 100, 1.0])
    ss = np.asarray(ss, float)
    A, Bp = P[:-1], P[1:]
    bmax = float(P[:, 3].max())
    rand_ = bmax / 2 + R["abstand_m"] + 30
    xmin, xmax = P[:, 0].min() - rand_, P[:, 0].max() + rand_
    ymin, ymax = P[:, 1].min() - rand_, P[:, 1].max() + rand_
    kand = np.where(pool.fest & (pool.cx >= xmin) & (pool.cx <= xmax) & (pool.cy >= ymin) & (pool.cy <= ymax))[0]
    out = []
    if not len(kand):
        return out
    AB = Bp[:, :2] - A[:, :2]
    L2 = np.maximum((AB ** 2).sum(1), 1e-9)
    for c0 in range(0, len(kand), 256):
        kk = kand[c0:c0 + 256]
        px = pool.cx[kk][:, None]
        py = pool.cy[kk][:, None]
        t = np.clip(((px - A[None, :, 0]) * AB[None, :, 0] + (py - A[None, :, 1]) * AB[None, :, 1]) / L2[None, :], 0, 1)
        d = np.hypot(px - (A[None, :, 0] + t * AB[None, :, 0]), py - (A[None, :, 1] + t * AB[None, :, 1]))
        halb = (A[None, :, 3] + t * (Bp[None, :, 3] - A[None, :, 3])) / 2.0
        zw_ = A[None, :, 2] + t * (Bp[None, :, 2] - A[None, :, 2])
        tw = A[None, :, 4] + t * (Bp[None, :, 4] - A[None, :, 4])
        rad = pool.rad[kk][:, None]
        rand = d - rad - halb
        zlo = pool.lo[kk, 2][:, None] / 100.0
        zhi = pool.hi[kk, 2][:, None] / 100.0
        ok = (rand <= R["abstand_m"]) & (zlo <= zw_ + R["ueber_spiegel_max_m"]) & (zhi >= zw_ - tw - R["unter_bett_toleranz_m"])
        rand_m = np.where(ok, rand, np.inf)
        best = np.argmin(rand_m, 1)
        for i, k in enumerate(kk):
            j = best[i]
            if not np.isfinite(rand_m[i, j]):
                continue
            s_ = float(ss[j] + t[i, j] * (ss[j + 1] - ss[j]))
            lage = "im_wasser" if d[i, j] - rad[i, 0] < halb[i, j] else "ufer"
            out.append((int(k), s_, float(rand_m[i, j]), lage, float(d[i, j]), float(halb[i, j]), float(zlo[i, 0] - zw_[i, j])))
    out.sort(key=lambda t_: pool.ref_text(t_[0]))
    return out


def bereich_rolle(a, b, linie, abst_innen, becken, roh):
    if roh:
        return "lauf"
    L = max(b - a, 1e-6)
    anteil = sum(max(0.0, min(b, q) - max(a, p)) for p, q in (bk["s_m"] for bk in becken)) / L
    if anteil >= 0.5:
        return "becken"
    m = (linie.s >= a) & (linie.s <= b)
    kn = {linie.knick[i] for i in np.where(m)[0]}
    if abst_innen or "rampe" in kn:
        return "rinne"
    return "gerinne"


def baue_gewaesser_v3(gw, regeln, pool):
    """gw: dict id, kategorie, art, linie, abst, extra, laeufe, muendung, anfang, roh_bei. Rueckgabe Eintrag (ohne
    Fingerabdruecke und WH)."""
    R = regeln
    S = R["swr"]
    gid = gw["id"]
    linie, abst, extra = gw["linie"], gw["abst"], gw["extra"]
    s0, s1 = float(linie.s[0]), float(linie.s[-1])
    abst = stufen_ordnen(abst, s0, s1, R)
    schw = R["fall_schwelle_m"]
    faelle = [d for d in abst if d["fall_m"] >= schw - 1e-9 and not d["rampe"]]
    for f in faelle:
        f["vorhang"], f["vorhang_grund"] = vorhang_regel(f, R)
    becken = becken_aus(abst, linie)
    sp, stufe_punkt = gewaesser_spline(linie, abst, gw["roh_bei"], R)
    ss = np.asarray(sp["punkte_s_m"], float)
    P = np.asarray(sp["punkte"], float)
    wbr = "WBR_" + gid
    # Bereiche (fruehere Abschnitte) zwischen den Faellen
    segs = segmente_bilden(linie, faelle, R)
    bereiche = []
    for n, g_ in enumerate(segs):
        a, b = g_["a"], g_["b"]
        innen = [d["id"] for d in abst if a + 1e-6 < d["s_lippe"] < b - 1e-6]
        bec = []
        for bk in becken:
            m = 0.5 * (bk["s_m"][0] + bk["s_m"][1])
            if a - 1e-6 <= m <= b + 1e-6:
                bec.append({"s_m": [r1(bk["s_m"][0], 2), r1(bk["s_m"][1], 2)],
                            "spiegel_cm": [r1(linie.z_bei(bk["s_m"][0], "unten")), r1(linie.z_bei(bk["s_m"][1], "oben"))],
                            "oben": bk["oben"], "unten": bk["unten"]})
        laeufe_in = [l_["id"] for l_ in gw["laeufe"] if l_["s_m"][0] < b - 1e-6 and l_["s_m"][1] > a + 1e-6]
        bereiche.append({"id": "%s_A%02d" % (gid, n), "s_m": [r1(a, 2), r1(b, 2)], "laenge_m": r1(b - a, 2),
                         "rolle": bereich_rolle(a, b, linie, innen, becken, all(gw["roh_bei"](x) for x in (a, 0.5 * (a + b), b))),
                         "oben_fall": g_["oben"], "unten_fall": g_["unten"], "faelle_innen": g_["innen"],
                         "abstuerze_innen": innen, "becken": bec, "laeufe": laeufe_in,
                         "rest_oben": bool(g_.get("rest_oben")), "rest_unten": bool(g_.get("rest_unten"))})
    # SWR-Bereiche (Nachtrag 17:45): eine SWR je Gewaesser, Aufloesung bis 2048; nur sehr grosse Rechtecke teilen
    typ_pkt = [gw["typ_bei"](x) for x in ss]
    zmax_pkt = np.array([S["zelle_max_bach_m"] if t_ == "bach" else S["zelle_max_fluss_m"] for t_ in typ_pkt], float)
    L_max = S["resolution_max"] * zmax_pkt
    achse_ges = achse_von(box_punkte(P, 0, len(P) - 1))
    if achse_ges <= float(L_max.min()) + 1e-9:
        teile_ = [{"a": s0, "b": s1, "naht_oben": {"art": "quelle", "s_m": s0}, "naht_unten": {"art": "muendung", "s_m": s1}}]
    else:
        teile_ = swr_teilen(sp, abst, becken, R, L_max)
    ue = S["teilung"]["ueberlappung_m"] / 2.0
    n_k = len(teile_)
    einzel = n_k == 1
    rand = S["rand_m"] * 100.0
    kacheln = []
    bid_ = (lambda k: gid) if einzel else (lambda k: "%s_T%02d" % (gid, k))
    for k, e in enumerate(teile_):
        kid = bid_(k)
        a_sim = max(s0, e["a"] - (ue if k > 0 else 0.0))
        b_sim = min(s1, e["b"] + (ue if k < n_k - 1 else 0.0))
        i0, i1 = kachel_index(ss, a_sim, b_sim)
        box = box_punkte(P, i0, i1)
        typ = "bach" if "bach" in typ_pkt[i0:i1 + 1] else "fluss"
        ziel = S["zelle_ziel_bach_m"] if typ == "bach" else S["zelle_ziel_fluss_m"]
        zmax = S["zelle_max_bach_m"] if typ == "bach" else S["zelle_max_fluss_m"]
        med = float(np.median(P[i0:i1 + 1, 3])) / 100.0
        lx, ly = (box[2] - box[0]) / 100.0, (box[3] - box[1]) / 100.0
        achse = max(lx, ly)
        res, zelle = zelle_fuer(achse, ziel, S)
        kurz = int(math.ceil(res * min(lx, ly) / max(achse, 1e-6) - 1e-9))
        raster = [res, kurz] if lx >= ly else [kurz, res]

        def naht(nh):
            d = {"art": nh["art"], "s_m": r1(nh["s_m"], 2)}
            if nh["art"] not in ("quelle", "muendung"):
                d["ueberlappung_m"] = r1(2 * ue, 2)
                d["ueberlappung_s_m"] = [r1(max(s0, nh["s_m"] - ue), 2), r1(min(s1, nh["s_m"] + ue), 2)]
            elif nh["art"] == "muendung":
                d["muendung"] = gw["muendung"]["art"]
            return d

        kacheln.append({
            "id": kid, "s_m": [r1(e["a"], 2), r1(e["b"], 2)], "laenge_m": r1(e["b"] - e["a"], 2),
            "s_sim_m": [r1(a_sim, 2), r1(b_sim, 2)], "punkt_index": [i0, i1],
            "rechteck_cm": [r1(box[0]), r1(box[1]), r1(box[2]), r1(box[3])], "rechteck_m": [r1(lx, 2), r1(ly, 2)],
            "bereiche": [b_["id"] for b_ in bereiche if b_["s_m"][0] < e["b"] - 1e-6 and b_["s_m"][1] > e["a"] + 1e-6],
            "faelle_innen": [f["id"] for f in faelle if e["a"] - 1e-6 <= f["s_lippe"] < e["b"] - 1e-6 or
                             (k == n_k - 1 and abs(f["s_lippe"] - e["b"]) < 1e-6)],
            "naht_oben": naht(e["naht_oben"]), "naht_unten": naht(e["naht_unten"]),
            "vorgaenger": [bid_(k - 1)] if k > 0 else [],
            "nachfolger": [bid_(k + 1)] if k < n_k - 1 else [],
            "back_reihenfolge": k,
            "geteilt": not einzel,
            "swr": {"id": "SWR_" + kid, "klasse": "ShallowWaterRiver", "typ": typ, "breite_median_m": r1(med, 2),
                    "zelle_ziel_m": ziel, "zelle_max_m": zmax, "achse_m": r1(achse, 2), "box_m": [r1(lx, 2), r1(ly, 2)],
                    "resolution_max_axis": res, "zelle_m": r1(zelle, 3), "raster_erwartet": raster,
                    "source_river_water_bodies": [wbr], "sink_river_water_bodies": [wbr],
                    "bottom_contour_tags": [S["hindernis_tag"]], "bottom_contour_actors": [],
                    "bottom_contour_landscape_actors": "lokal", "use_capture": True,
                    "match_spline": True if einzel else "lokal testen",
                    "begrenzung": ({"art": "rechteck_um_fluss", "hinweis": "SWR-Bereich = achsparalleles Rechteck um den Fluss (16c Nachtrag 17:45)"}
                                   if einzel else
                                   {"art": "rechteck_teil", "rechteck_cm": [r1(box[0]), r1(box[1]), r1(box[2]), r1(box[3])],
                                    "zentrum_cm": [r1(0.5 * (box[0] + box[2])), r1(0.5 * (box[1] + box[3]))],
                                    "hinweis": S["teilung"]["geteilt_hinweis"]}),
                    "render_state": dict(S["render_state"]),
                    "material": {"water_body": S["material_spiel"], "baked_sim_material": S["material_spiel"]}},
            "bereich_cm": [r1(box[0] - rand), r1(box[1] - rand), r1(box[2] + rand), r1(box[3] + rand)],
            "zufluesse": [], "hindernis_akteur": None})

    def kachel_bei(s_):
        for kc in kacheln:
            if kc["s_m"][0] - 1e-6 <= s_ <= kc["s_m"][1] + 1e-6:
                return kc["id"]
        return kacheln[-1]["id"] if s_ > s1 else kacheln[0]["id"]

    def bereich_bei(s_, oben):
        kand = [b_["id"] for b_ in bereiche if b_["s_m"][0] - 1e-3 <= s_ <= b_["s_m"][1] + 1e-3]
        if not kand:
            return None
        return kand[0] if oben else kand[-1]

    for b_ in bereiche:
        b_["swr_bereiche"] = [kc["id"] for kc in kacheln if kc["s_m"][0] < b_["s_m"][1] - 1e-6 and kc["s_m"][1] > b_["s_m"][0] + 1e-6] \
            or [kachel_bei(b_["s_m"][0])]
    # Wasser-Kollision an der einen Spline
    kol = kollision_v3(pool, sp["punkte"], ss, R)
    wk, ohne, randbloecke = [], [], []
    kante = R["kollision"]["randblock_kante_m"]
    ue_max = R["kollision"]["ueberspannt_unterkante_max_m"]
    for k, s_, rnd, lage, d, halb, ueber in kol:
        rec = pool.recs[k]
        gro = (pool.hi[k] - pool.lo[k]) / 100.0
        e = {"ref": pool.ref(k), "netz": rec["netz"], "pfad": rec["pfad"], "art": rec["art"],
             "pos_cm": [r1(rec["v"][0]), r1(rec["v"][1]), r1(rec["v"][2])],
             "groesse_m": [r1(gro[0], 2), r1(gro[1], 2), r1(gro[2], 2)], "lage": lage,
             "abstand_rand_m": r1(rnd, 2), "s_m": r1(s_, 2), "bereich": bereich_bei(s_, True), "swr_bereich": kachel_bei(s_),
             "unterkante_ueber_spiegel_m": r1(ueber, 2), "kollision_im_plan": rec["kollision"]}
        if lage == "im_wasser" and ueber > ue_max + 1e-9:
            e["wasser_kollision"] = False
            e["grund"] = "ueberspannt"
            ohne.append(e)
            continue
        e["wasser_kollision"] = True
        wk.append(e)
        if abs(d - halb) <= pool.rad[k] + kante:
            p = linie.bei(s_)
            tx_, ty_ = linie.tangente(s_)
            u = ((pool.cx[k] * 100 - p["x"]) * -ty_ + (pool.cy[k] * 100 - p["y"]) * tx_) / 100.0
            randbloecke.append({"s": s_, "u": float(u), "r": float(pool.rad[k]), "ref": pool.ref(k)})
    randbloecke.sort(key=lambda t_: (t_["s"], t_["u"]))
    # Faelle
    fl = []
    KN = R["kaskadennetz"]
    for f in faelle:
        nxt = [d["s_lippe"] for d in abst if d["s_lippe"] > f["s_fuss"] + 1e-6]
        becken_ende = min(nxt) if nxt else s1
        b_o = bereich_bei(f["s_lippe"], True)
        b_u = bereich_bei(f["s_fuss"], False)
        if b_u is not None and abs(f["s_fuss"] - s1) < 1e-6 and not any(b_["s_m"][0] >= f["s_fuss"] - 1e-3 for b_ in bereiche):
            b_u = None
        innen = b_o is not None and b_o == b_u
        pl, pf_ = linie.bei(f["s_lippe"]), linie.bei(f["s_fuss"])
        strahl = extra["strahl"].get(f["stufe"])
        kn_id = next((k["id"] for k in extra["kaskadennetze"] if k["s_m"][0] - 1e-3 <= f["s_lippe"] <= k["s_m"][1] + 1e-3), None)
        eff = [e for e in extra["effekte"] if e.get("stufe") == f["stufe"]]
        if f["teil"]:
            gesch = [d for d in faelle if d["stufe"] == f["stufe"]]
            eff = [e for e in eff if min(gesch, key=lambda d: math.hypot(
                linie.bei(d["s_fuss"])["x"] - e["pos_cm"][0], linie.bei(d["s_fuss"])["y"] - e["pos_cm"][1]))["id"] == f["id"]]
        vh = f["vorhang"]
        sp_i = stufe_punkt.get(f["id"], {})
        eintrag = {
            "id": f["id"], "stufe": f["stufe"], "teil": f["teil"], "lauf": f.get("lauf"), "art": f["art"],
            "art_regel": f.get("art_regel"),
            "fall_m": r1(f["fall_m"], 2), "s_lippe_m": r1(f["s_lippe"], 2), "s_fuss_m": r1(f["s_fuss"], 2),
            "punkt_lippe": sp_i.get("lippe"), "punkt_fuss": sp_i.get("fuss"),
            "bereich_oben": b_o, "bereich_unten": b_u, "im_bereich": innen,
            "swr_bereich": kachel_bei(f["s_lippe"]),
            "lippe_cm": [r1(pl["x"]), r1(pl["y"]), r1(f["z_oben"])], "fuss_cm": [r1(pf_["x"]), r1(pf_["y"]), r1(f["z_unten"])],
            "lippe_breite_m": r1(float(pl["b"]) / 100.0, 2),
            "versatz_m": None if f.get("versatz_m") is None else r1(f["versatz_m"], 2), "holzstufe": bool(f.get("holz")),
            "vorhang": vh, "vorhang_grund": f["vorhang_grund"], "vorhang_status": R["vorhang"]["status"],
            "strahl_breite_m": strahl.get("strahl_breite_m") if strahl else None,
            "strahl_quelle": strahl.get("quelle") if strahl else None,
            "kaskadennetz": {"id": kn_id,
                             "bereich_s_m": [r1(f["s_lippe"] - KN["vor_lippe_m"], 2), r1(f["s_fuss"] + KN["nach_fuss_m"], 2)] if vh else None,
                             "vorhang": vh, "vorhang_planer": f["stufe"] in extra["vorhang"]},
            "effekte": [{"quelle": e["_quelle"], "index": e["_index"], "asset": e.get("asset"), "rolle": e.get("rolle"),
                         "cull_m": e.get("cull_m"), "pos_cm": e.get("pos_cm")} for e in eff],
            "gischt": f["fall_m"] >= R["schaum"]["gischt_ab_m"],
            "schaum": "objekte" if vh else "simulation",
            "schaum_objekte": schaum_fuer_fall(f, linie, becken_ende, (strahl or {}).get("strahl_breite_m"), R,
                                               randbloecke, extra.get("ufer_rand")) if vh else []}
        if eintrag["gischt"]:
            eintrag["gischt_hinweis"] = "Gischt = vorhandene Nature-Water-FX-Effekte dieser Stufe (cull_m aus 13k), kein neues Objekt"
        fl.append(eintrag)
    abst_out = []
    for d in abst:
        sp_i = stufe_punkt.get(d["id"], {})
        abst_out.append({"id": d["id"], "lauf": d.get("lauf"), "s_lippe_m": r1(d["s_lippe"], 2), "s_fuss_m": r1(d["s_fuss"], 2),
                         "fall_m": r1(d["fall_m"], 2), "rampe": d["rampe"], "z_oben_cm": r1(d["z_oben"]),
                         "z_unten_cm": r1(d["z_unten"]), "punkt_lippe": sp_i.get("lippe"), "punkt_fuss": sp_i.get("fuss")})
    eintrag = {
        "id": gid, "kategorie": gw["kategorie"], "art": gw["art"], "laenge_m": r1(s1 - s0, 2),
        "laeufe": gw["laeufe"], "anfang": gw["anfang"], "muendung": gw["muendung"], "zufluesse": [],
        "water_body": {"id": wbr, "klasse": "WaterBodyRiver", "affects_landscape": False,
                       "overlap_material_priority": None, "spline": sp},
        "abstuerze": abst_out, "bereiche": bereiche, "faelle": fl, "swr_bereiche": kacheln,
        "wasser_kollision": wk, "ohne_wasser_kollision": ohne,
        "effekte_ohne_fall": sorted({e["_quelle"] + "[%d]" % e["_index"] for e in extra["effekte"]}
                                    - {x["quelle"] + "[%d]" % x["index"] for f in fl for x in f["effekte"]})}
    for k_ in ("quelle_sehens",):
        if gw.get(k_):
            eintrag[k_] = gw[k_]
    return eintrag


# ======================================================================================================================
# Verkettung der Laeufe, Muendungen
# ======================================================================================================================
def b2_zu_id(i):
    return ("B_R2_" + i[3:]) if isinstance(i, str) and i.startswith("B2_") else i


class Wasserkarte:
    """Seen (Welt + Sehens), Meer, Welt-Wasserfaelle fuer Anfang/Muendung."""

    def __init__(self, welt, sehens_seen, G):
        self.G = G
        self.welt = welt
        ww = welt.wasser_welt or {}
        self.seen = [{"id": s["id"], "quelle": "wasser_welt.json", "umriss": np.asarray(s["umriss"], float),
                      "spiegel_cm": float(s["spiegel_cm"])} for s in ww.get("seen", []) or [] if s.get("umriss")]
        self.seen += sehens_seen
        for s in self.seen:
            U = s["umriss"]
            s["box"] = (float(U[:, 0].min()), float(U[:, 1].min()), float(U[:, 0].max()), float(U[:, 1].max()))
        self.wf = []
        for w in ww.get("wasserfaelle", []) or []:
            k = w.get("kante_xz")
            if k:
                self.wf.append({"id": w["WasserfallID"], "parent": w.get("ParentWaterBodyID"),
                                "x": float(k[0]) * 100.0, "y": float(k[1]) * 100.0, "fall_m": w.get("fallhoehe_m")})
        m = welt.meer
        self.meer = m() if callable(m) else m

    def see_bei(self, x, y, halb_m, tol_m):
        best = None
        for s in self.seen:
            b = s["box"]
            r = (halb_m + tol_m) * 100.0
            if x < b[0] - r or x > b[2] + r or y < b[1] - r or y > b[3] + r:
                continue
            d = abstand_polygon(s["umriss"], x, y)
            if d <= halb_m + tol_m and (best is None or (d, s["id"]) < (best[0], best[1]["id"])):
                best = (d, s)
        return best

    def meer_bei(self, x, y, radius_m):
        from sehens_lib import daten as _d
        w = self.welt
        fi, fj = _d.m_zu_pixel(x / 100.0, y / 100.0, w.zelle_m)
        r = int(math.ceil(radius_m / w.zelle_m))
        i0, i1 = max(int(fi) - r, 0), min(int(fi) + r + 1, w.ny)
        j0, j1 = max(int(fj) - r, 0), min(int(fj) + r + 1, w.nx)
        if i0 >= i1 or j0 >= j1:
            return None
        I, J = np.meshgrid(np.arange(i0, i1), np.arange(j0, j1), indexing="ij")
        d = np.hypot(I - fi, J - fj) * w.zelle_m
        sel = self.meer[i0:i1, j0:j1] & (d <= radius_m)
        return float(d[sel].min()) if sel.any() else None

    def wasserfall_bei(self, x, y, radius_m):
        best = None
        for w in self.wf:
            d = math.hypot(w["x"] - x, w["y"] - y) / 100.0
            if d <= radius_m and (best is None or d < best[0]):
                best = (d, w)
        return best


def muendung_suchen(kette, teile_welt, karte, G, teil_ort):
    """Muendung am Ende der Kette. Reihenfolge: ausdruecklich (Sehens 'muendung', R2 'anschluss.ende'), Fluss/Bach
    (Ende im Wasserstreifen eines anderen Laufs), See, Meer, Welt-Wasserfall, sonst offen."""
    t = kette[-1]
    L = t.linie
    ex, ey, ez = float(L.x[-1]), float(L.y[-1]), float(L.z[-1])
    halb = float(L.b[-1]) / 200.0
    eigene = {k.id for k in kette}
    pkt = [r1(ex), r1(ey), r1(ez)]

    def lauf_ziel(Q, quelle, hinweis=None):
        d, s, z, b = projektion(Q.linie, ex, ey)
        m = {"art": "fluss" if Q.art == "fluss" else "bach", "ziel_lauf": Q.id, "ziel_s_lauf_m": r1(s, 2),
             "abstand_m": r1(d, 2), "rand_m": r1(d - b / 200.0, 2), "spiegel_ziel_cm": r1(z), "dz_cm": r1(ez - z),
             "punkt_cm": pkt, "quelle": quelle}
        if hinweis:
            m["hinweis"] = hinweis
        if d - b / 200.0 > G["muendung_toleranz_m"]:
            m["luecke_m"] = r1(d - b / 200.0, 2)
            m["hinweis"] = "Ende liegt %.1f m neben dem Wasser des Ziels: Spline lokal bis ins Ziel verlaengern" % (d - b / 200.0)
        return m, d - b / 200.0

    # 1. ausdruecklich
    sh = t.sehens or {}
    if sh:
        art = sh.get("muendung_art")
        mu = sh.get("muendung")
        if art == "versickert":
            return {"art": "versickert", "punkt_cm": pkt, "quelle": "sehens"}
        if art == "see_eigen":
            sid = "%s/%s" % (sh["ort"], mu)
            s = next((x for x in karte.seen if x["id"] == sid), None)
            if s is not None:
                return {"art": "see", "ziel": sid, "see_quelle": "sehens", "spiegel_ziel_cm": r1(s["spiegel_cm"]),
                        "abstand_m": r1(abstand_polygon(s["umriss"], ex, ey), 2), "punkt_cm": pkt, "quelle": "sehens"}
        if art in ("bach", "fluss") and mu in teil_ort:
            m, rnd = lauf_ziel(teil_ort[mu], "sehens")
            if rnd <= G["ausdruecklich_rand_max_m"]:
                return m
        if art == "houdini" and mu and mu != "houdini":
            kand = sorted((projektion(Q.linie, ex, ey)[0] - 0.0, Q.id) for Q in teile_welt if Q.netz == mu)
            if kand:
                m, rnd = lauf_ziel(teil_ort[kand[0][1]], "sehens (netz %s)" % mu)
                if rnd <= G["ausdruecklich_rand_max_m"]:
                    return m
    ende = (t.anschluss or {}).get("ende") or {}
    if ende.get("epic"):
        zid = b2_zu_id(ende["epic"])
        if zid in teil_ort and zid not in eigene:
            m, rnd = lauf_ziel(teil_ort[zid], "anschluss_r2")
            if rnd <= G["ausdruecklich_rand_max_m"]:
                return m
        s = next((x for x in karte.seen if x["id"] == zid), None)
        if s is not None:
            d = abstand_polygon(s["umriss"], ex, ey)
            if d <= halb + G["ausdruecklich_rand_max_m"]:
                return {"art": "see", "ziel": zid, "see_quelle": s["quelle"], "spiegel_ziel_cm": r1(s["spiegel_cm"]),
                        "abstand_m": r1(d, 2), "punkt_cm": pkt, "quelle": "anschluss_r2"}
    # 2. Fluss/Bach geometrisch (Ende im Wasserstreifen eines anderen Laufs bzw. nah daneben)
    def lauf_naechst(tol_m, dz_unter_cm, dz_ueber_cm):
        best = None
        r = tol_m * 100.0 + 15000.0
        for Q in teile_welt:
            if Q.id in eigene:
                continue
            b = Q.box
            if ex < b[0] - r or ex > b[2] + r or ey < b[1] - r or ey > b[3] + r:
                continue
            d, s, z, bq = projektion(Q.linie, ex, ey)
            rnd = d - bq / 200.0
            if rnd <= tol_m and z - dz_unter_cm <= ez <= z + dz_ueber_cm:
                key = (round(max(rnd, 0.0), 3), -bq, Q.id)
                if best is None or key < best[0]:
                    best = (key, Q)
        return best

    best = lauf_naechst(G["muendung_toleranz_m"], G["muendung_dz_unter_cm"], 1e9)
    if best is not None:
        return lauf_ziel(best[1], "geometrie")[0]
    # 3. See
    sb = karte.see_bei(ex, ey, halb, G["see_toleranz_m"])
    if sb is not None:
        d, s = sb
        return {"art": "see", "ziel": s["id"], "see_quelle": s["quelle"], "spiegel_ziel_cm": r1(s["spiegel_cm"]),
                "abstand_m": r1(d, 2), "punkt_cm": pkt, "quelle": "geometrie"}
    # 4. Meer (Meer-Raster nah am Ende, bzw. Ende auf Strandhoehe und Meer in Strandbreite)
    dm = karte.meer_bei(ex, ey, halb + G["meer_radius_m"])
    if dm is None and ez <= G["meer_strand_z_max_cm"]:
        dm = karte.meer_bei(ex, ey, G["meer_strand_radius_m"])
    if dm is not None:
        return {"art": "meer", "ziel": "meer", "abstand_m": r1(dm, 2), "punkt_cm": pkt, "quelle": "geometrie (Meer-Raster)"}
    # 5. nah neben einem Lauf bzw. See (Luecke in den Weltdaten): Muendung mit Luecke
    best = lauf_naechst(G["nah_toleranz_m"], G["muendung_dz_unter_cm"], G["nah_dz_ueber_cm"])
    if best is not None:
        return lauf_ziel(best[1], "geometrie (nah)")[0]
    sb = karte.see_bei(ex, ey, halb, G["nah_toleranz_m"])
    if sb is not None and ez >= sb[1]["spiegel_cm"] - G["muendung_dz_unter_cm"]:
        d, s = sb
        return {"art": "see", "ziel": s["id"], "see_quelle": s["quelle"], "spiegel_ziel_cm": r1(s["spiegel_cm"]),
                "abstand_m": r1(d, 2), "luecke_m": r1(max(d - halb, 0.0), 2), "punkt_cm": pkt, "quelle": "geometrie (nah)",
                "hinweis": "Ende liegt neben dem See: Spline lokal bis ins Wasser verlaengern"}
    # 6. Welt-Wasserfall
    wf = karte.wasserfall_bei(ex, ey, G["wasserfall_radius_m"])
    if wf is not None:
        return {"art": "wasserfall", "ziel": wf[1]["id"], "abstand_m": r1(wf[0], 2), "punkt_cm": pkt, "quelle": "geometrie",
                "hinweis": "Wasserfaelle warten (Ferat 16c); Unterlauf ist ein eigenes Gewaesser"}
    naechst = None
    for Q in teile_welt:
        if Q.id in eigene:
            continue
        d, s, z, bq = projektion(Q.linie, ex, ey)
        key = (round(d - bq / 200.0, 2), Q.id)
        if naechst is None or key < naechst[0]:
            naechst = (key, {"lauf": Q.id, "rand_m": r1(d - bq / 200.0, 1), "dz_cm": r1(ez - z)})
    sb = karte.see_bei(ex, ey, halb, 1e6)
    m = {"art": "offen", "punkt_cm": pkt, "quelle": "geometrie",
         "hinweis": "kein Ziel in Reichweite (Fluss/Bach %.0f m, nah %.0f m, See %.0f m, Meer %.0f m, Wasserfall %.0f m)"
                    % (G["muendung_toleranz_m"], G["nah_toleranz_m"], G["see_toleranz_m"], G["meer_radius_m"], G["wasserfall_radius_m"]),
         "naechster_lauf": naechst[1] if naechst else None,
         "naechster_see": {"see": sb[1]["id"], "abstand_m": r1(sb[0], 1)} if sb else None}
    if sh.get("muendung_art") == "houdini":
        m["quelle"] = "sehens (houdini %s, kein Lauf in Reichweite)" % sh.get("muendung")
    return m


def anfang_suchen(t, karte, G):
    L = t.linie
    ax, ay = float(L.x[0]), float(L.y[0])
    halb = float(L.b[0]) / 200.0
    sh = t.sehens or {}
    if sh.get("abfluss_von"):
        sid = "%s/%s" % (sh["ort"], sh["abfluss_von"])
        return {"art": "see", "ziel": sid, "quelle": "sehens", "punkt_cm": [r1(ax), r1(ay), r1(L.z[0])]}
    sb = karte.see_bei(ax, ay, halb, G["see_toleranz_m"])
    if sb is not None:
        return {"art": "see", "ziel": sb[1]["id"], "abstand_m": r1(sb[0], 2), "quelle": "geometrie",
                "punkt_cm": [r1(ax), r1(ay), r1(L.z[0])]}
    wf = karte.wasserfall_bei(ax, ay, G["wasserfall_radius_m"])
    if wf is not None:
        return {"art": "wasserfall", "ziel": wf[1]["id"], "abstand_m": r1(wf[0], 2), "quelle": "geometrie",
                "punkt_cm": [r1(ax), r1(ay), r1(L.z[0])]}
    return {"art": "quelle", "punkt_cm": [r1(ax), r1(ay), r1(L.z[0])]}


def endstueck_anpassen(linie, eintrag_zufluss):
    """Gefaelle-Plan 'zufluesse' (Hauptlauf senkt sein Becken): Endstueck des Zuflusses ab punkte_neu_cm[0] auf die neuen
    Hoehen setzen (nur absenken). Rueckgabe Beschreibung oder None."""
    pn = eintrag_zufluss.get("punkte_neu_cm") or []
    if len(pn) < 2:
        return None
    d, sa, _, _ = projektion(linie, pn[0][0], pn[0][1])
    if d > 5.0:
        return None
    s1 = float(linie.s[-1])
    m = linie.s >= sa - 1e-6
    if s1 - sa < 1e-3:
        return None
    zn = np.interp(linie.s[m], [sa, s1], [float(pn[0][2]), float(pn[-1][2])])
    linie.z[m] = np.minimum(linie.z[m], zn)
    linie.z = np.minimum.accumulate(linie.z)
    return {"s_m": [r1(sa, 2), r1(s1, 2)], "z_cm": [r1(pn[0][2]), r1(pn[-1][2])], "absenkung_m": eintrag_zufluss.get("absenkung_m")}


# ======================================================================================================================
# Hauptlauf
# ======================================================================================================================
def finde_sw(sehens_basis, sw_ordner, biom):
    for c in ([os.path.join(sw_ordner, "sw_" + biom)] if sw_ordner else []) + \
             [os.path.join(sehens_basis, biom, "sw_" + biom), os.path.join(sehens_basis, "..", "sw_" + biom)]:
        if os.path.isdir(c):
            return c
    return None


def gewaesser_bilden(welt, gef, sehens, regeln, log_=log):
    """Alle Laeufe laden, verketten, Muendungen bestimmen. Rueckgabe (gewaesser, teile, karte, info)."""
    import gefaelle_daten as gd
    G = regeln["gewaesser"]
    ww = welt.wasser_welt or {}
    teile_welt = []
    for f in sorted(ww.get("fluesse", []) or [], key=lambda f: f["id"]):
        teile_welt.append(("fluss", f["id"], f.get("fluss"), None, f.get("feld"), None))
    for b in sorted(welt.baeche or [], key=lambda b: b["id"]):
        teile_welt.append(("bach", b["id"], None, b.get("netz"), b.get("feld"), b.get("anschluss")))
    teile = []
    for art, tid, fam, netz, feld, ans in teile_welt:
        pf = os.path.join(gef, tid, "plan.json") if gef else None
        r = gefaelle_gewaesser(gef, tid, regeln) if (pf and os.path.exists(pf)) else None
        if r:
            g, linie, abst, extra = r
            her = "plan"
        else:
            lauf = gd.Lauf.aus_welt(welt, tid)
            g, linie, abst, extra = roh_gewaesser(lauf, regeln, art)
            her = "roh"
        teile.append(Teil(tid, art, her, g, linie, abst, extra, familie=fam, netz=netz, feld=feld, anschluss=ans))
    teil_ort = {t.id: t for t in teile}
    # Sehens-Baeche und -Seen
    sehens_teile, sehens_seen = [], []
    for biom, ort, rel in sehens:
        for w in ort.get("wasser") or []:
            if w.get("typ") == "see" and w.get("umriss_cm"):
                sehens_seen.append({"id": "%s/%s" % (ort["id"], w["id"]), "quelle": "sehens/%s/orte.json" % biom,
                                    "umriss": np.asarray(w["umriss_cm"], float)[:, :2], "spiegel_cm": float(w.get("spiegel_cm") or 0.0)})
        for g, linie, abst, extra in sehens_gewaesser(biom, ort, regeln):
            w = next(x for x in ort["wasser"] if x.get("typ") == "bach" and x.get("id") == g["bach"])
            sh = {"ort": ort["id"], "biom": biom, "bach": w.get("id"), "muendung": w.get("muendung"),
                  "muendung_art": w.get("muendung_art"), "abfluss_von": w.get("abfluss_von"), "rel": rel}
            sehens_teile.append(Teil(g["id"], "sehens_bach", "sehens", g, linie, abst, extra, sehens=sh))
    karte = Wasserkarte(welt, sehens_seen, G)
    # Fortsetzungen (Welt-Laeufe)
    nach, vor = {}, {}
    kand = []
    for P in teile:
        for N in teile:
            if N is P:
                continue
            b, r = N.box, (G["fortsetzung_abstand_m"] + 1.0) * 100.0
            ex, ey = float(P.linie.x[-1]), float(P.linie.y[-1])
            if ex < b[0] - r or ex > b[2] + r or ey < b[1] - r or ey > b[3] + r:
                continue
            f = fortsetzung_test(P, N, G)
            if f:
                kand.append((round(f["abstand_m"], 4), P.id, N.id, f))
    kand.sort(key=lambda t_: (t_[0], t_[1], t_[2]))
    for _, pid, nid, f in kand:
        if pid in nach or nid in vor:
            continue
        nach[pid] = (nid, f)
        vor[nid] = pid
    # Ketten
    ketten = []
    for t in teile:
        if t.id in vor:
            continue
        k, links = [t], []
        while k[-1].id in nach:
            nid, f = nach[k[-1].id]
            if any(x.id == nid for x in k):
                break
            k.append(teil_ort[nid])
            links.append(f)
        ketten.append((k, links))
    ketten += [([t], []) for t in sehens_teile]
    # Namen, Muendung, Zusammenfuegen
    gewaesser, vergeben = [], set()
    for k, links in ketten:
        if k[0].art == "sehens_bach":
            gid = k[0].id
            kat, art = "sehens", "sehens_bach"
        else:
            gid = familie_name(k, vergeben)
            kat, art = "welt", ("fluss" if any(t.art == "fluss" for t in k) else "bach")
        vergeben.add(gid)
        mu = muendung_suchen(k, teile, karte, G, teil_ort)
        an = anfang_suchen(k[0], karte, G)
        linie, abst, extra, laeufe = zusammenfuegen(k, links, regeln)
        typen = {t.id: swr_typ(t.linie, t.abst, t.extra, regeln)[0] for t in k}
        for l_ in laeufe:
            l_["swr_typ"] = typen[l_["id"]]
        rohe = [(l_["s_m"][0], l_["s_m"][1], l_["herkunft"] == "roh" or (l_["herkunft"] == "sehens" and k[0].roh), l_["swr_typ"])
                for l_ in laeufe]

        def roh_bei(s_, rohe=rohe):
            for a_, b_, r_, _ in rohe:
                if a_ - 1e-6 <= s_ <= b_ + 1e-6:
                    return r_
            return rohe[-1][2]

        def typ_bei(s_, rohe=rohe):
            for a_, b_, _, t_ in rohe:
                if a_ - 1e-6 <= s_ <= b_ + 1e-6:
                    return t_
            return rohe[-1][3]

        gw = {"id": gid, "kategorie": kat, "art": art, "linie": linie, "abst": abst, "extra": extra, "laeufe": laeufe,
              "muendung": mu, "anfang": an, "roh_bei": roh_bei, "typ_bei": typ_bei, "teile": k}
        if kat == "sehens":
            sh = k[0].sehens
            gw["quelle_sehens"] = {"biom": sh["biom"], "ort": sh["ort"], "bach": sh["bach"]}
            gw["rel"] = sh["rel"]
        else:
            gw["rel"] = os.path.join("gewaesser", gid, "fluss_sim.json")
        gewaesser.append(gw)
    # Muendungsziel -> Gewaesser, Zufluss-Endstuecke aus den Plaenen
    lauf_gw = {}
    for gw in gewaesser:
        for l_ in gw["laeufe"]:
            lauf_gw[l_["id"]] = gw
    for gw in gewaesser:
        mu = gw["muendung"]
        if mu["art"] in ("fluss", "bach") and mu.get("ziel_lauf") in lauf_gw:
            zg = lauf_gw[mu["ziel_lauf"]]
            lz = next(l_ for l_ in zg["laeufe"] if l_["id"] == mu["ziel_lauf"])
            s_ = mu["ziel_s_lauf_m"] - lz["s_quelle_m"][0] + lz["s_m"][0]
            mu["ziel"] = zg["id"]
            mu["ziel_s_m"] = r1(min(max(s_, lz["s_m"][0]), lz["s_m"][1]), 2)
            if mu["art"] == "bach" and zg["art"] == "fluss":
                mu["art"] = "fluss"
            Q = teil_ort.get(mu["ziel_lauf"])
            for z_ in (Q.extra.get("zufluesse") or []) if Q is not None else []:
                if z_.get("id") == gw["teile"][-1].id:
                    a_ = endstueck_anpassen(gw["linie"], z_)
                    if a_:
                        a_["quelle"] = "gefaelle/%s/plan.json#zufluesse" % Q.id
                        mu["endstueck_angepasst"] = a_
    info = {"teile_welt": len(teile), "teile_plan": sum(1 for t in teile if t.herkunft == "plan"),
            "teile_roh": sum(1 for t in teile if t.herkunft == "roh"), "sehens_baeche": len(sehens_teile),
            "fortsetzungen": {a_: sum(1 for _, (n_, f) in nach.items() if f["art"] == a_) for a_ in ("anschluss", "ueberlappung")}}
    return gewaesser, teile, karte, info


def main(argv=None):
    ap = argparse.ArgumentParser(description="Exporter Entscheidung 16 (v3, 16c): fluss_sim.json je Gewaesser + back_liste.json")
    ap.add_argument("--gefaelle", default=None, help="Ordner mit <lauf>/plan.json (gefaelle_plan.py)")
    ap.add_argument("--sehens", default=None, help="Ordner mit <biom>/orte.json (Sehens-Planer)")
    ap.add_argument("--sw-ordner", default=None, help="Ordner mit sw_<biom>/ (Standard: <sehens>/<biom>/sw_<biom>)")
    ap.add_argument("--aus", required=True)
    ap.add_argument("--regeln", default=REGELN_STANDARD)
    ap.add_argument("--nur", nargs="+", default=None)
    from sehens_lib import daten
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    regeln = lese_json(a.regeln)
    welt = daten.lade(a.daten2m or (None if a.daten1m else os.path.join(RECHERCHE, "vorlagen", "daten", "sehens")),
                      a.daten1m, pfade=False)
    masse = Masse()
    pool = Pool(regeln, masse)
    gel = Gelaende(welt)
    if a.gefaelle and os.path.isdir(a.gefaelle):
        for lauf in sorted(os.listdir(a.gefaelle)):
            pf = os.path.join(a.gefaelle, lauf, "plan.json")
            if not os.path.exists(pf):
                continue
            plan = lese_json(pf)
            gel.delta_hinzu(os.path.join(a.gefaelle, lauf), plan.get("abschnitte"))
            for feld_plan in sorted(glob.glob(os.path.join(a.gefaelle, lauf, "instanzen", "*", "plan.json"))):
                feld = os.path.basename(os.path.dirname(feld_plan))
                pool.lade_ebene(feld_plan, "gefaelle/%s/instanzen/%s/plan.json" % (lauf, feld))
    sehens = []
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
                sehens.append((biom, ort, os.path.join("sehens", biom, ort["id"], "fluss_sim.json")))
    pool.fertig()
    gewaesser, teile, karte, info = gewaesser_bilden(welt, a.gefaelle if a.gefaelle and os.path.isdir(a.gefaelle) else None,
                                                     sehens, regeln)
    nur = set(a.nur) if a.nur else None
    if nur:
        gewaesser = [gw for gw in gewaesser if gw["id"] in nur or any(l_["id"] in nur for l_ in gw["laeufe"])
                     or (gw.get("quelle_sehens") or {}).get("ort") in nur]
    log("Laeufe: %d Welt (%d mit Plan, %d roh), %d Sehens-Baeche; Fortsetzungen %s; Gewaesser: %d, Gelaende-Deltas %d"
        % (info["teile_welt"], info["teile_plan"], info["teile_roh"], info["sehens_baeche"], info["fortsetzungen"],
           len(gewaesser), len(gel.deltas)))
    # je Gewaesser bauen
    dateien = {}
    alle = []
    for gw in gewaesser:
        e = baue_gewaesser_v3(gw, regeln, pool)
        alle.append(e)
        dateien.setdefault(gw["rel"], []).append(e)
    nach_id = {e["id"]: e for e in alle}
    # Zufluesse und Rang (overlap_material_priority: Hauptlauf vor Zufluss)
    for e in alle:
        mu = e["muendung"]
        if mu["art"] in ("fluss", "bach") and mu.get("ziel") in nach_id:
            z = nach_id[mu["ziel"]]
            kc = next((k for k in z["swr_bereiche"] if k["s_m"][0] - 1e-6 <= mu["ziel_s_m"] <= k["s_m"][1] + 1e-6),
                      z["swr_bereiche"][-1])
            mu["ziel_swr_bereich"] = kc["id"]
            z["zufluesse"].append({"gewaesser": e["id"], "art": e["art"], "s_m": mu["ziel_s_m"], "swr_bereich": kc["id"],
                                   "water_body": e["water_body"]["id"]})
            kc["zufluesse"].append(e["water_body"]["id"])
    for e in alle:
        e["zufluesse"].sort(key=lambda z_: (z_["s_m"], z_["gewaesser"]))
        for kc in e["swr_bereiche"]:
            kc["zufluesse"] = sorted(set(kc["zufluesse"]))

    def stufe(e, seen=()):
        mu = e["muendung"]
        if mu["art"] in ("fluss", "bach") and mu.get("ziel") in nach_id and e["id"] not in seen:
            return 1 + stufe(nach_id[mu["ziel"]], seen + (e["id"],))
        return 0
    prio_max = regeln["swr"]["prioritaet_hauptlauf"]
    for e in alle:
        e["water_body"]["overlap_material_priority"] = max(1, prio_max - stufe(e))
        e["muendung"]["stufe"] = stufe(e)
    # Wasser-Kollision global: jedes Objekt genau einem Hindernis-Akteur WH_<kachel> zuordnen (naechste Kachel)
    fpr = regeln["fingerabdruck"]
    kol_global, kand_kachel = {}, {}
    for rel in sorted(dateien):
        for e in dateien[rel]:
            for o in e["wasser_kollision"]:
                key = json.dumps(o["ref"], sort_keys=True)
                kol_global[key] = o
                kand_kachel.setdefault(key, []).append((o["abstand_rand_m"], o["swr_bereich"]))
    zuordnung = {k_: min(v)[1] for k_, v in kand_kachel.items()}
    kol_keys = sorted(kol_global)
    ref_index = {json.dumps(pool.ref(k), sort_keys=True): k for k in range(len(pool.recs))}
    kol_k = np.array([ref_index[k_] for k_ in kol_keys], int) if kol_keys else np.zeros(0, int)
    je_kachel = {}
    for key in kol_keys:
        je_kachel.setdefault(zuordnung[key], []).append(key)
    alle_kacheln = {}
    for e in alle:
        for o in e["wasser_kollision"]:
            o["hindernis_akteur"] = "WH_" + zuordnung[json.dumps(o["ref"], sort_keys=True)]
        for kc in e["swr_bereiche"]:
            alle_kacheln[kc["id"]] = kc
    S = regeln["swr"]
    for kid in sorted(je_kachel):
        kc = alle_kacheln[kid]
        b_ = kc["bereich_cm"]
        komp, akt = {}, []
        for key in je_kachel[kid]:
            k = ref_index[key]
            rec = pool.recs[k]
            v = rec["v"]
            q = quat_kanonisch(v[3:7])
            inst = {"ref": pool.ref(k), "pos_cm": [r1(v[0]), r1(v[1]), r1(v[2])],
                    "quat_xyzw": [round(float(x), 6) for x in q], "skala": [round(float(x), 4) for x in v[7:10]],
                    "lage": kol_global[key]["lage"]}
            if rec.get("liste") == "akteure":
                akt.append(inst)
            else:
                komp.setdefault(rec["pfad"], []).append(inst)
        kc["hindernis_akteur"] = {
            "id": "WH_" + kid, "klasse": "Actor", "label": "WH_" + kid, "tags": [S["hindernis_tag"], "SWR_B_" + kid],
            "ursprung_cm": [r1(0.5 * (b_[0] + b_[2])), r1(0.5 * (b_[1] + b_[3])), 0.0],
            "komponenten": [{"netz": pf, "klasse": "HISM", "nanite": None, "kollision": "wie_quelle", "instanzen": komp[pf]}
                            for pf in sorted(komp)],
            "akteure_mit_tag": akt,
            "n_instanzen": sum(len(v_) for v_ in komp.values()), "n_komponenten": len(komp), "n_akteure_mit_tag": len(akt),
            "umzug": "verschieben"}

    # Fingerabdruecke je SWR-Kachel (Back-Einheit)
    def fp_bereich(bx, splines):
        x0, y0, rcm, H = gel.raster(bx)
        gt = fp_gelaende_text(x0, y0, rcm, H, fpr["hoehe_quant_cm"])
        st = fp_splines_text(splines, fpr["spline_quant_cm"])
        objs, whs = [], set()
        if len(kol_k):
            lo, hi = pool.lo[kol_k], pool.hi[kol_k]
            sel = (hi[:, 0] >= bx[0]) & (lo[:, 0] <= bx[2]) & (hi[:, 1] >= bx[1]) & (lo[:, 1] <= bx[3])
            for i in np.where(sel)[0]:
                k = kol_k[i]
                v = pool.recs[k]["v"]
                objs.append([pool.recs[k]["pfad"]] + [float(x) for x in v[:10]])
                whs.add("WH_" + zuordnung[kol_keys[i]])
        ot = fp_objekte_text(objs, fpr["pos_quant_cm"], fpr["quat_quant"], fpr["skala_quant"])
        ges, teile_ = fingerabdruck(gt, st, ot, fpr["version"])
        return ges, teile_, int(H.size), r1(rcm, 1), len(objs), sorted(whs), float(H.max()) if H.size else None

    back = []
    hoehe_kachel = []
    for rel in sorted(dateien):
        for e in dateien[rel]:
            wb = e["water_body"]
            pts = wb["spline"]["punkte"]
            for kc in e["swr_bereiche"]:
                i0, i1 = kc["punkt_index"]
                ges, teile_, nh, rcm, no, whs, hmax = fp_bereich(kc["bereich_cm"], [(wb["id"], pts[i0:i1 + 1])])
                kc["fingerabdruck"] = ges
                kc["fingerabdruck_teile"] = teile_
                kc["n_hoehen"] = nh
                kc["raster_cm"] = rcm
                kc["n_objekte"] = no
                kc["gelaende_max_cm"] = r1(hmax) if hmax is not None else None
                kc["swr"]["bottom_contour_actors"] = whs
                hoehe_kachel.append((hmax or 0.0, kc["id"]))
                sw = kc["swr"]
                back.append({"swr_bereich": kc["id"], "gewaesser": e["id"], "datei": rel.replace(os.sep, "/"),
                             "swr": sw["id"], "water_body_river": wb["id"], "punkt_index": kc["punkt_index"],
                             "hindernis_akteur": kc["hindernis_akteur"]["id"] if kc["hindernis_akteur"] else None,
                             "bereich_cm": kc["bereich_cm"], "s_m": kc["s_m"], "s_sim_m": kc["s_sim_m"],
                             "naht_oben": kc["naht_oben"]["art"], "naht_unten": kc["naht_unten"]["art"],
                             "vorgaenger": kc["vorgaenger"], "nachfolger": kc["nachfolger"],
                             "back_reihenfolge": kc["back_reihenfolge"], "geteilt": kc["geteilt"],
                             "resolution_max_axis": sw["resolution_max_axis"], "zelle_m": sw["zelle_m"],
                             "fingerabdruck": ges, "teile": teile_, "n_hoehen": nh, "n_objekte": no})
    # schreiben
    for rel in sorted(dateien):
        d = {"format": FORMAT_VERSION, "regeln_version": regeln["version"], "fall_schwelle_m": regeln["fall_schwelle_m"],
             "daten": "1m" if a.daten1m else "2m (Cloud-Test)", "gewaesser": dateien[rel]}
        schreibe_json(os.path.join(a.aus, rel), d)
    zus = zusammenfassung(alle, regeln, info, kol_global, pool, karte, hoehe_kachel, gewaesser)
    zus["daten"] = "1m" if a.daten1m else "2m (Cloud-Test)"
    zus["format"] = FORMAT_VERSION
    zus["dateien"] = len(dateien)
    schreibe_json(os.path.join(a.aus, "zusammenfassung.json"), zus)
    schreibe_json(os.path.join(a.aus, "back_liste.json"),
                  {"format": BACK_FORMAT, "fingerabdruck": dict(fpr, formel="siehe README fluss_sim, Abschnitt Fingerabdruck"),
                   "einheit": "SWR-Bereich (eine SWR je Gewaesser; Teilstuecke nur bei sehr grossem Rechteck)", "swr_bereiche": back})
    s_ = zus["summe"]
    log("geschrieben: %d Dateien, %d Gewaesser (%d mit einer SWR), %d SWR-Bereiche, Aufloesung %s, Muendungen %s, %d Faelle "
        "(%d mit Vorhang), %d Kollisionsobjekte (%d eindeutig, %d ueberspannt), %d Hindernis-Akteure"
        % (len(dateien), s_["gewaesser"], s_["gewaesser_eine_swr"], s_["swr_bereiche"], zus["swr"]["aufloesung"], zus["muendungen"],
           s_["faelle"], s_["faelle_vorhang"], s_["kollision"], len(kol_global), s_["ueberspannt"], zus["swr"]["hindernis_akteure"]))
    return 0


def zusammenfassung(alle, regeln, info, kol_global, pool, karte, hoehe_kachel, gewaesser):
    S = regeln["swr"]
    zus = {"laeufe": info}
    su = {"gewaesser": len(alle), "laenge_m": r1(sum(e["laenge_m"] for e in alle), 1), "swr_bereiche": 0, "gewaesser_eine_swr": 0,
          "faelle": 0, "faelle_vorhang": 0, "abstuerze": 0, "bereiche": 0, "kollision": 0, "kollision_im_wasser": 0,
          "ueberspannt": 0, "schaum": {}, "splinepunkte": 0}
    kat = {}
    for e in alle:
        k = kat.setdefault("%s/%s" % (e["kategorie"], e["art"]), {"gewaesser": 0, "laenge_m": 0.0, "swr_bereiche": 0, "eine_swr": 0,
                                                                  "laeufe": 0})
        k["gewaesser"] += 1
        k["laenge_m"] = r1(k["laenge_m"] + e["laenge_m"], 1)
        k["swr_bereiche"] += len(e["swr_bereiche"])
        k["eine_swr"] += 1 if len(e["swr_bereiche"]) == 1 else 0
        k["laeufe"] += len(e["laeufe"])
        su["swr_bereiche"] += len(e["swr_bereiche"])
        su["gewaesser_eine_swr"] += 1 if len(e["swr_bereiche"]) == 1 else 0
        su["faelle"] += len(e["faelle"])
        su["faelle_vorhang"] += sum(1 for f in e["faelle"] if f["vorhang"])
        su["abstuerze"] += len(e["abstuerze"])
        su["bereiche"] += len(e["bereiche"])
        su["kollision"] += len(e["wasser_kollision"])
        su["kollision_im_wasser"] += sum(1 for o in e["wasser_kollision"] if o["lage"] == "im_wasser")
        su["ueberspannt"] += len(e["ohne_wasser_kollision"])
        su["splinepunkte"] += len(e["water_body"]["spline"]["punkte"])
        for f in e["faelle"]:
            for s_ in f["schaum_objekte"]:
                su["schaum"][s_["art"]] = su["schaum"].get(s_["art"], 0) + 1
    su["schaum"] = {k_: su["schaum"][k_] for k_ in sorted(su["schaum"])}
    zus["summe"] = su
    zus["kategorien"] = {k_: kat[k_] for k_ in sorted(kat)}
    mv = {}
    for e in alle:
        mv.setdefault(e["muendung"]["art"], 0)
        mv[e["muendung"]["art"]] += 1
    zus["muendungen"] = {k_: mv[k_] for k_ in sorted(mv)}
    zus["muendungen_quelle"] = {}
    for e in alle:
        q = e["muendung"].get("quelle", "")
        zus["muendungen_quelle"][q] = zus["muendungen_quelle"].get(q, 0) + 1
    zus["muendungen_quelle"] = {k_: zus["muendungen_quelle"][k_] for k_ in sorted(zus["muendungen_quelle"])}
    zus["muendungen_offen"] = sorted(e["id"] for e in alle if e["muendung"]["art"] == "offen")
    zus["anfang"] = {}
    for e in alle:
        zus["anfang"][e["anfang"]["art"]] = zus["anfang"].get(e["anfang"]["art"], 0) + 1
    zus["anfang"] = {k_: zus["anfang"][k_] for k_ in sorted(zus["anfang"])}
    zus["zufluesse_mit_endstueck_aus_plan"] = sorted(e["id"] for e in alle if e["muendung"].get("endstueck_angepasst"))
    # Laengen und Achsen
    L = np.array([e["laenge_m"] for e in alle], float)
    ach = np.array([achse_von(box_punkte(e["water_body"]["spline"]["punkte"], 0, len(e["water_body"]["spline"]["punkte"]) - 1))
                    for e in alle], float)
    grenzen = [50, 100, 130, 180, 256, 500, 1000, 2000]
    def vert(x):
        out, lo = {}, 0
        for g_ in grenzen:
            out["<= %d" % g_] = int(((x > lo) & (x <= g_)).sum())
            lo = g_
        out["> %d" % grenzen[-1]] = int((x > grenzen[-1]).sum())
        return out
    zus["laenge_m"] = {"min": r1(L.min(), 1), "median": r1(np.median(L), 1), "max": r1(L.max(), 1), "verteilung": vert(L),
                       "laengste": [[e["id"], e["laenge_m"]] for e in sorted(alle, key=lambda e: (-e["laenge_m"], e["id"]))[:10]]}
    zus["box_achse_m"] = {"median": r1(np.median(ach), 1), "max": r1(ach.max(), 1), "verteilung": vert(ach)}
    # SWR-Bereiche
    ks = [kc for e in alle for kc in e["swr_bereiche"]]
    zellen = np.array([kc["swr"]["zelle_m"] for kc in ks], float)
    nv = {}
    for kc in ks:
        if kc["naht_unten"]["art"] != "muendung":
            nv[kc["naht_unten"]["art"]] = nv.get(kc["naht_unten"]["art"], 0) + 1
    res = np.array([kc["swr"]["resolution_max_axis"] for kc in ks], int)
    whs = [kc["hindernis_akteur"] for kc in ks if kc["hindernis_akteur"]]
    geteilt = sorted(((e["id"], len(e["swr_bereiche"]), e["laenge_m"]) for e in alle if len(e["swr_bereiche"]) > 1),
                     key=lambda t: (-t[1], t[0]))
    zv = {}
    for kc in ks:
        t = kc["swr"]["typ"]
        z_ = kc["swr"]["zelle_m"]
        lab = next(("<= %.2f" % x for x in (0.20, 0.25, 0.30, 0.35) if z_ <= x + 1e-9), "> 0.35")
        zv.setdefault(t, {}).setdefault(lab, 0)
        zv[t][lab] += 1
    zus["swr"] = {
        "anzahl": len(ks), "typ": {t: sum(1 for kc in ks if kc["swr"]["typ"] == t) for t in ("bach", "fluss")},
        "gewaesser_eine_swr": sum(1 for e in alle if len(e["swr_bereiche"]) == 1),
        "gewaesser_geteilt": len(geteilt), "swr_in_geteilten": sum(n for _, n, _ in geteilt),
        "geteilte": [list(x) for x in geteilt],
        "naehte": {k_: nv[k_] for k_ in sorted(nv)},
        "aufloesung": {"<= 512": int((res <= 512).sum()), "513-1024": int(((res > 512) & (res <= 1024)).sum()),
                       "1025-2048": int(((res > 1024) & (res <= 2048)).sum()), "> 2048": int((res > 2048).sum())},
        "aufloesung_median": int(np.median(res)), "aufloesung_max": int(res.max()),
        "zelle_m": {"min": r1(zellen.min(), 3), "median": r1(np.median(zellen), 3), "max": r1(zellen.max(), 3),
                    "verteilung": {t: {k_: zv[t][k_] for k_ in sorted(zv[t])} for t in sorted(zv)}},
        "rechteck_m": {"median_laengste_seite": r1(np.median([max(kc["rechteck_m"]) for kc in ks]), 1),
                       "max_laengste_seite": r1(max(max(kc["rechteck_m"]) for kc in ks), 1)},
        "zellen_mio": {"summe": r1(sum(kc["swr"]["raster_erwartet"][0] * kc["swr"]["raster_erwartet"][1] for kc in ks) / 1e6, 1)},
        "hindernis_akteure": len(whs), "hindernis_instanzen": sum(w["n_instanzen"] for w in whs),
        "hindernis_akteure_mit_tag": sum(w["n_akteure_mit_tag"] for w in whs),
        "swr_ohne_hindernis": len(ks) - len(whs),
        "gelaende_max_in_swr_m": r1(max(h for h, _ in hoehe_kachel) / 100.0, 2) if hoehe_kachel else None,
        "gelaende_max_swr": max(hoehe_kachel)[1] if hoehe_kachel else None}
    # Varianten der Zielzelle (Zielzelle, hoechste Zelle) fuer Bach / Fluss: wie viele Gewaesser muessten geteilt werden?
    var = {}
    for name, zb, mb, zf, mf in (("regel: bach 0.25 (max 0.30), fluss 0.35", S["zelle_ziel_bach_m"], S["zelle_max_bach_m"],
                                  S["zelle_ziel_fluss_m"], S["zelle_max_fluss_m"]),
                                 ("bach 0.25 (max 0.25), fluss 0.35", 0.25, 0.25, 0.35, 0.35),
                                 ("alle 0.25", 0.25, 0.25, 0.25, 0.25),
                                 ("bach 0.30, fluss 0.35", 0.30, 0.30, 0.35, 0.35),
                                 ("bis 512 (Zwischenregel 16c): bach 0.35, fluss 0.5", 0.35, 0.35, 0.5, 0.5)):
        n_t, n_k, rv = 0, 0, {"<= 512": 0, "513-1024": 0, "1025-2048": 0}
        rmax = 512 if "512" in name else S["resolution_max"]
        S2 = dict(S, resolution_max=rmax)
        for e, gw in zip(alle, gewaesser):
            ss_ = e["water_body"]["spline"]["punkte_s_m"]
            typ_ = [gw["typ_bei"](x) for x in ss_]
            Lm = np.array([rmax * (mb if t == "bach" else mf) for t in typ_], float)
            P = e["water_body"]["spline"]["punkte"]
            if achse_von(box_punkte(P, 0, len(P) - 1)) <= float(Lm.min()) + 1e-9:
                tl = [(0, len(P) - 1)]
            else:
                n_t += 1
                becken = becken_aus(gw["abst"], gw["linie"])
                ue = S["teilung"]["ueberlappung_m"] / 2.0
                tl = []
                for q in swr_teilen(e["water_body"]["spline"], gw["abst"], becken, dict(regeln, swr=S2), Lm):
                    tl.append(kachel_index(ss_, max(ss_[0], q["a"] - ue), min(ss_[-1], q["b"] + ue)))
            for i0, i1 in tl:
                n_k += 1
                t = "bach" if "bach" in typ_[i0:i1 + 1] else "fluss"
                r_, _ = zelle_fuer(achse_von(box_punkte(P, i0, i1)), zb if t == "bach" else zf, S2)
                rv["<= 512" if r_ <= 512 else ("513-1024" if r_ <= 1024 else "1025-2048")] += 1
        var[name] = {"gewaesser_geteilt": n_t, "gewaesser_eine_swr": len(alle) - n_t, "swr": n_k, "aufloesung": rv}
    zus["varianten_zelle"] = var
    # Hoehen (T2-10)
    hz = []
    for e in alle:
        P = np.asarray(e["water_body"]["spline"]["punkte"], float)
        hz.append((float(P[:, 2].max()), e["id"], e["kategorie"]))
    hz.sort(reverse=True)
    zus["hoehe"] = {"hoechste_spline_m": [[i, r1(z / 100.0, 2), k_] for z, i, k_ in hz[:8]],
                    "grenze_m": 655.04, "ueber_grenze": sum(1 for z, _, _ in hz if z > 65504.0)}
    zus["kollision_objekte_eindeutig"] = len(kol_global)
    zus["objekt_pool"] = {"objekte": len(pool.recs), "fest_und_gross": int(pool.fest.sum())}
    return zus


if __name__ == "__main__":
    sys.exit(main())
