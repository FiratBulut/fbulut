#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fluss_sim_export.py - Exporter fuer Entscheidung 16 (Shallow Water River fuer alle Baeche und Fluesse).

Liest NUR die vorhandenen Planer-Ausgaben (gefaelle_plan.py: <lauf>/plan.json + instanzen/, Sehens-Planer:
<biom>/orte.json + sw_<biom>/) und die Weltdaten. Aendert nichts an Planern, Stufen, Becken oder Gelaende
(13f-Regel: die Treppen der Sehens-Baeche bleiben exakt). Format v3 (16c, Ferat 12.10.2026):

  Gewaesser         EIN WaterBodyRiver je Gewaesser von der Quelle bis zur Muendung (See, Fluss/Bach, Meer), ueber
                    alle Faelle und Feldgrenzen hinweg. Die Welt-Laeufe (wasser_welt.json je Feld, baeche_alle.json,
                    mit Gefaelle-Plan oder roh) werden an ihren Enden verkettet; Sehens-Baeche sind je ein Gewaesser,
                    ueber kleine Toepfe (< 30 m, 16d) verkettet: Zulauf -> Topf -> Abfluss = ein Gewaesser.
  water_body        die eine Spline (x, y, z, Breite, Tiefe, Tempo je Punkt) mit Punktrollen; jede Stufe hat einen
                    Punkt an der Lippe (Oberwasser) und einen am Fuss (Unterwasser), dazwischen 2-4 m (roh 5-10 m).
  muendung          Art (meer, see, fluss, bach, versickert, wasserfall, offen, topf), Ziel, Muendungspunkt; zufluesse.
                    Offene Enden und Luecken: muendung.vorschlag (Punkte, Ziel, Begruendung), NICHT in der Spline (16d).
  toepfe            kleine Sehens-Seen als Teil des Gewaessers (Bereich rolle topf, kein WaterBodyLake, 16d)
  bereiche          die frueheren Abschnitte zwischen den Faellen nur noch als s-Bereiche mit Rolle
  faelle            je Einzelabsturz >= fall_schwelle_m: Lippe/Fuss, Effekte, vorhang (Regel 16b) und nur dann
                    Kaskadennetz-Bereich und schaum_objekte (wie 16/16a; Vorhaenge warten auf Ferat)
  swr_bereiche      EINE ShallowWaterRiver je Gewaesser (16c Nachtrag 17:45): Rechteck um den Fluss, resolution_max_axis =
                    laengste Seite / Zielzelle (Bach 0,25 m, Fluss 0,35 m) bis 2048; nur wenn die Zelle dann ueber
                    0,30 m (Bach) bzw. 0,35 m (Fluss) laege, wenige lange Teilstuecke auf demselben Fluss (kleinste
                    Rechteckflaeche, nicht an Faellen). Je SWR Hindernis-Akteur WH_<swr> und Fingerabdruck.
  wasser_kollision  alle festen Instanzen/Akteure im Wasser oder <= 1 m daneben (ueberspannte ohne, 16a E5)

und global back_liste.json (je SWR-Bereich: Fingerabdruck, Reihenfolge), vorschlaege.json und zusammenfassung.json.

16e (Regeln Version 5): Tempo je Splinepunkt nach dem Spiegelgefaelle (tempo_regel: Manning-Strickler bei Normalabfluss,
Abfluss aus der Becken-Geometrie, geglaettet, tempo_faktor) -> spline.tempo_ms (m/s) und WaterVelocityScalar_cm_s
(= x 100); schaum_maske je Gewaesser (Kapseln nur an Vorhang-Faellen, Option B: Simulationsschaum nur dort); Baeche
bleiben bis zelle_max_bach_ungeteilt_m (0,40 m) ungeteilt, Teilstuecke halten zelle_max_bach_m (0,30 m).

16g Nachtrag (Regeln Version 10): Ursache des Stillstands war die zu grobe Wasser-Info der Water Zone (C2 1208 m /
1024 = 1,18 m je Pixel). Regel (Ferat): Pixel <= schmalste Bachbreite / 6. Je SWR-Bereich swr_bereiche[].water_info
(schmalste Breite, groesste Pixelgroesse, groesste Zone je Aufloesung, noetige Aufloesung in einer 1208-m-Zone); global
wasserzonen.json (Grundzone WZ_WELT + feine Zonen WZ_Fnn, gruppiert; Ausdehnung, Aufloesung, Speicher) und je Gewaesser
water_body.water_zone_vorschlag (WaterZoneOverride). Aendert weder Spline noch SWR-Werte noch Fingerabdruck.

16g Nachtrag 2 (Regeln Version 11): SWR-Vorgaben match_spline_height_amount 0,3 (0,1/0,2 bleiben bei s 76 stehen),
remove_outside_spline_amount 0 (F1: 50 macht das Bett 15 % flacher), band_zugabe_m 2 (RiverWidth im Editor = Bett + 2 m,
F2), source_size_cm >= 300; Regel water_info jetzt Pixel <= schmalstes Band / 12; Hindernis-Filter (swr.hindernis_filter):
Lippen-, Rand- und Bettfelsen, Teile > 40 % der Bettbreite und was je Meter ueber 50 % der Bettbreite hinausgeht,
bekommen keine Wasser-Kollision (bleiben Deko, ohne_wasser_kollision mit grund filter_*) -> Objektteil der
Fingerabdruecke aendert sich; wasserzonen.json je Zone Hoehenstufe der 16-Bit-Wasser-Info und half_precision_ok.

Eingaben (16d): gelesen werden nur Lauf-Plaene (<lauf>/plan.json mit 'wasser_koerper'); Ordner mit '.' im Namen oder
fuehrendem '_' (Archivkopien) und andere Plaene (Feld-Instanzplan gefaelle/C2/plan.json von a15_einbau.py) werden
uebersprungen und im Protokoll genannt, ebenso Archiv-Feldordner unter instanzen/ und sw_<biom>/.
Gelaende-Deltas schon gebauter Laeufe werden nicht addiert (lokal schon in welt/ eingestempelt): --gebaut LAUF ... oder
automatisch, wenn sehens_einbau/A15_<lauf>/lauf.json existiert und 'nachgezogen' das Feld enthaelt (siehe
nachgezogen_felder; fehlt die Datei, gilt der Lauf als ungebaut). Protokoll und zusammenfassung.json (gelaende_deltas)
nennen die gebauten Laeufe, back_liste.json (gelaende.deltas_ohne) die weggelassenen Delta-Dateien fuer den Pruefer.

Aufruf (Cloud, 2 m):
  python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py \
      --gefaelle <scratch>/gef --sehens <scratch>/sehens --daten2m recherche/vorlagen/daten/sehens --aus <scratch>/fs
Lokal (1 m):
  python -I .../fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle --sehens export/unreal/welt/sehens \
      --sw-ordner export/unreal/welt --daten1m export/unreal/welt --aus export/unreal/welt/fluss_sim
Optionen: --nur ID ... (Gewaesser-, Lauf- oder Ort-IDs; verkettet wird immer ueber alle Laeufe), --regeln DATEI,
  --gebaut LAUF ... (Gefaelle-Lauf, Sehens-Ort oder SW_<ort>_<bach>), --einbau DIR (sehens_einbau/; Standard
  <daten1m>/sehens_einbau bzw. neben --gefaelle), --ohne-erkennung (lauf.json nicht auswerten).

Deterministisch (keine Zeitstempel, sortierte Ausgabe, Zufall aus SHA-256 der IDs). Keine Unreal-Importe.
Die Funktion fingerabdruck() ist die Referenz fuer das lokale Werkzeug (Handaenderungen im Editor).
"""

import argparse
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
# 16f Rueckfrage (Epic Parameter Reference): SWR-Felder, die das Backen bestimmen, aber nicht im Fingerabdruck stehen
SIM_VORGABEN_FELDER = ("resolution_max_axis", "match_spline", "match_spline_height_amount", "remove_outside_spline_amount",
                       "source_size_cm", "sim_speed", "num_steps", "use_capture", "band_zugabe_m")


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
                                  "rolle": str(info.get("rolle", "")), "v": a[i]})
        for i, ak in enumerate(p.get("akteure") or []):
            if not all(k_ in ak for k_ in ("x", "y", "z", "qx", "qy", "qz", "qw")):
                continue
            v = np.array([ak["x"], ak["y"], ak["z"], ak["qx"], ak["qy"], ak["qz"], ak["qw"],
                          ak.get("sx", 1.0), ak.get("sy", 1.0), ak.get("sz", 1.0)], np.float64)
            self.recs.append({"quelle": ref_quelle, "liste": "akteure", "index": i, "pfad": ak.get("pfad", ak.get("netz")),
                              "netz": ak.get("netz", ""), "kollision": bool(ak.get("kollision")),
                              "gruppe": ak.get("klasse", ""), "rolle": None, "v": v})

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
        fest_alt = np.zeros(n, bool)
        ausdehnung = np.zeros(n)
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
        self.bounds_je_pfad = {pf: (c_[0], c_[1]) for pf, c_ in cache.items()}
        for k, r in enumerate(self.recs):
            a = cache[r["pfad"]][3]
            r["art"] = a
            r["masse_quelle"] = cache[r["pfad"]][2]
            groesse = (hi[k] - lo[k]) / 100.0
            # 16f Rueckfrage: Mindestgroesse = groesste Ausdehnung des Netzes x |Skala| (ohne Drehung), Hoehe wie bisher
            # aus den gedrehten Bounds (Kies, Steinpackungen bleiben ohne)
            bmin, bmax = cache[r["pfad"]][0], cache[r["pfad"]][1]
            aus_m = float(((bmax - bmin) * np.abs(V[k, 7:10])).max()) / 100.0
            ausdehnung[k] = aus_m
            fest_art = (a != "pflanze") and (r["kollision"] or a in ("fels", "holz"))
            gross_alt = max(groesse[0], groesse[1]) >= self.r["min_ausdehnung_m"] and groesse[2] >= self.r["min_hoehe_m"]
            gross = aus_m >= self.r["min_ausdehnung_m"] - 1e-9 and groesse[2] >= self.r["min_hoehe_m"]
            fest[k] = fest_art and gross
            fest_alt[k] = fest_art and gross_alt
            art.append(a)
        self.fest = fest
        self.fest_alt = fest_alt
        self.ausdehnung = ausdehnung
        self.cx = (lo[:, 0] + hi[:, 0]) / 200.0 if n else np.zeros(0)
        self.cy = (lo[:, 1] + hi[:, 1]) / 200.0 if n else np.zeros(0)
        self.rad = (np.hypot(hi[:, 0] - lo[:, 0], hi[:, 1] - lo[:, 1]) / 200.0) if n else np.zeros(0)
        log("Objekt-Pool: %d Objekte, davon %d fest und gross genug (groesste Ausdehnung >= %.2f m; Regel bis v7: %d)"
            % (n, int(fest.sum()), self.r["min_ausdehnung_m"], int(fest_alt.sum())))

    def ecken_cm(self, k):
        """8 Ecken der gedrehten Netz-Bounds x Skala in Weltkoordinaten (cm), (8, 3)."""
        r = self.recs[k]
        bmin, bmax = self.bounds_je_pfad[r["pfad"]]
        v = self.V[k]
        ecken = np.array([[i, j, l] for i in (0, 1) for j in (0, 1) for l in (0, 1)], float)
        c = (bmin + (bmax - bmin) * ecken) * v[7:10][None, :]
        return v[None, :3] + quat_drehe(np.repeat(v[None, 3:7], 8, 0), c)

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
        """Rueckgabe: Anzahl hinzugefuegter Deltas."""
        from sehens_lib import daten as _d
        n = 0
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
                n += 1
        return n

    def delta(self, x, y):
        from sehens_lib import daten as _d
        x, y = np.broadcast_arrays(np.asarray(x, float), np.asarray(y, float))
        out = np.zeros(x.shape)
        x0, x1, y0, y1 = float(np.min(x)), float(np.max(x)), float(np.min(y)), float(np.max(y))
        for (i0, j0, hh, ww), box, pf in self.deltas:
            if box[2] < x0 or box[0] > x1 or box[3] < y0 or box[1] > y1:
                continue
            # Vorauswahl der Punkte im Fenster (+ 1 cm), gerechnet wird wie bisher (Ergebnis bitgleich)
            sel = (x >= box[0] - 0.01) & (x <= box[2] + 0.01) & (y >= box[1] - 0.01) & (y <= box[3] + 0.01)
            if not sel.any():
                continue
            xs, ys = x[sel], y[sel]
            fi = ys + _d.OFF_I - i0
            fj = xs + _d.OFF_J - j0
            innen = (fi >= 0) & (fi <= hh - 1) & (fj >= 0) & (fj <= ww - 1)
            if not innen.any():
                continue
            a = np.fromfile(pf, dtype="<f4").reshape(hh, ww).astype(np.float64)
            i = np.clip(np.floor(fi).astype(np.int64), 0, hh - 2)
            j = np.clip(np.floor(fj).astype(np.int64), 0, ww - 2)
            di = np.clip(fi - i, 0, 1)
            dj = np.clip(fj - j, 0, 1)
            v = (a[i, j] * (1 - di) * (1 - dj) + a[i, j + 1] * (1 - di) * dj + a[i + 1, j] * di * (1 - dj) +
                 a[i + 1, j + 1] * di * dj)
            o = out[sel]
            out[sel] = np.where(innen, o + v, o)
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

    def hoehe_cm(self, x_cm, y_cm):
        """Gelaende (cm) an Weltpunkten (cm): Rasterhoehe bilinear + Deltas."""
        x = np.asarray(x_cm, float) / 100.0
        y = np.asarray(y_cm, float) / 100.0
        h = np.asarray(self.welt.bilinear(self.welt.hoehe, x, y), float)
        return (h + self.delta(x, y)) * 100.0


# ======================================================================================================================
# Eingaben (16d): nur echte Lauf-Plaene, keine Archivordner; schon gebaute Laeufe ohne Gelaende-Delta
# ======================================================================================================================
def ersetzte_laeufe():
    """16h: Welt-Laeufe, die lokal durch einen eigenen Lauf ersetzt sind (fluss_sim/ersetzt.json, gefaelle_daten)."""
    import gefaelle_daten as gd
    return gd.ersetzte_laeufe()


def ersetzt_grund(lauf_id):
    e = ersetzte_laeufe().get(lauf_id) or {}
    return "ersetzt durch %s (fluss_sim/ersetzt.json, 16h)" % e.get("ersetzt_durch", "?")


def ist_archiv(name):
    """Archiv- bzw. Ablageordner: Name mit '.' (F_..._C2.alt_v1_gebaut) oder fuehrendem '_' (_alt)."""
    return "." in name or name.startswith("_")


def lauf_plaene(gef_basis):
    """Lauf-Plaene unter --gefaelle: <lauf>/plan.json mit Schluessel 'wasser_koerper'. Archivordner und andere Plaene
    (z. B. Feld-Instanzplan gefaelle/C2/plan.json von a15_einbau.py) werden genannt und uebersprungen.
    Rueckgabe ({lauf: pfad}, [{ordner, grund}])."""
    plaene, weg = {}, []
    if not gef_basis or not os.path.isdir(gef_basis):
        return plaene, weg
    for name in sorted(os.listdir(gef_basis)):
        d = os.path.join(gef_basis, name)
        if not os.path.isdir(d):
            continue
        pf = os.path.join(d, "plan.json")
        if ist_archiv(name):
            weg.append({"ordner": name, "grund": "Archivordner ('.' im Namen bzw. fuehrendes '_')"})
            continue
        if not os.path.exists(pf):
            continue
        if name in ersetzte_laeufe():
            weg.append({"ordner": name, "grund": ersetzt_grund(name)})
            continue
        try:
            plan = lese_json(pf)
        except (OSError, ValueError):
            weg.append({"ordner": name, "grund": "plan.json nicht lesbar"})
            continue
        if not isinstance(plan, dict) or "wasser_koerper" not in plan:
            weg.append({"ordner": name, "grund": "kein Lauf-Plan (ohne 'wasser_koerper', z. B. Feld-Instanzplan von a15_einbau.py)"})
            continue
        plaene[name] = pf
        del plan
    return plaene, weg


def feld_plaene(ordner):
    """Instanz-Ebenen <ordner>/<Feld>/plan.json ohne Archivordner. Rueckgabe ([pfad], [{ordner, grund}])."""
    out, weg = [], []
    if not ordner or not os.path.isdir(ordner):
        return out, weg
    for name in sorted(os.listdir(ordner)):
        pf = os.path.join(ordner, name, "plan.json")
        if not os.path.isdir(os.path.join(ordner, name)):
            continue
        if ist_archiv(name):
            weg.append({"ordner": name, "grund": "Archivordner ('.' im Namen bzw. fuehrendes '_')"})
            continue
        if os.path.exists(pf):
            out.append(pf)
    return out, weg


def roh_ordner_finden(roh, gefaelle):
    """16c Nachtrag 3: Ordner der Roh-Lauf-Ebene (gefaelle/bachbett_roh.py): --roh, sonst 'bachbett_roh' neben --gefaelle
    (export/unreal/welt/gefaelle -> export/unreal/welt/bachbett_roh). None, wenn nicht vorhanden."""
    if roh:
        return roh if os.path.isdir(roh) else None
    if gefaelle:
        c = os.path.join(os.path.dirname(os.path.abspath(gefaelle.rstrip("/"))), "bachbett_roh")
        if os.path.isdir(c):
            return c
    return None


def roh_ebenen(roh_basis):
    """Instanz-Ebenen der Roh-Laeufe: <roh>/<lauf>/instanzen/<Feld>/plan.json (Plan mit art 'bachbett_roh').
    Rueckgabe ([(pfad, ref)], [{ordner, grund}])."""
    out, weg = [], []
    if not roh_basis or not os.path.isdir(roh_basis):
        return out, weg
    for name in sorted(os.listdir(roh_basis)):
        d = os.path.join(roh_basis, name)
        if not os.path.isdir(d):
            continue
        if ist_archiv(name):
            weg.append({"ordner": name, "grund": "Archivordner ('.' im Namen bzw. fuehrendes '_')"})
            continue
        if not os.path.exists(os.path.join(d, "plan.json")):
            continue
        if name in ersetzte_laeufe():
            weg.append({"ordner": name, "grund": ersetzt_grund(name)})
            continue
        fp_, w_ = feld_plaene(os.path.join(d, "instanzen"))
        weg += [dict(x, ordner="%s/instanzen/%s" % (name, x["ordner"])) for x in w_]
        for pf in fp_:
            out.append((pf, "bachbett_roh/%s/instanzen/%s/plan.json" % (name, os.path.basename(os.path.dirname(pf)))))
    return out, weg


def _wahr(v):
    if isinstance(v, str):
        return v.strip().lower() not in ("", "0", "nein", "false", "no", "offen", "aus")
    return bool(v)


def nachgezogen_felder(d, tiefe=0):
    """Liest 'nachgezogen' aus lauf.json (Format nicht festgelegt, daher defensiv). Rueckgabe (felder, form):
    felder = Menge der Feldnamen (gross), 'alle' (nachgezogen: true) oder None (kein Eintrag). Angenommene Formen:
      "nachgezogen": ["C2", "C3"]                               Liste von Feldnamen
      "nachgezogen": [{"feld": "C2", "ok": true, ...}, ...]       Liste von Objekten (feld/id/name; ok/nachgezogen/fertig)
      "nachgezogen": {"C2": true | {...}, "C3": false}            Objekt je Feld (Wert wahr = nachgezogen)
      "nachgezogen": {"felder": ["C2"]}                           Objekt mit Feldliste
      "nachgezogen": "C2" bzw. "C2,C3"                            Text
      "nachgezogen": true                                         alle Felder des Laufs
    Liegt 'nachgezogen' nicht oben, wird in Unterobjekten (bis Tiefe 3, Schluessel sortiert) gesucht."""
    if not isinstance(d, dict):
        return None, "kein Objekt"
    if "nachgezogen" not in d:
        if tiefe < 3:
            for k in sorted(d, key=str):
                if isinstance(d[k], dict):
                    f, form = nachgezogen_felder(d[k], tiefe + 1)
                    if f is not None:
                        return f, "%s.%s" % (k, form)
        return None, "ohne 'nachgezogen'"
    v = d["nachgezogen"]
    if v is True:
        return "alle", "true"
    if isinstance(v, str):
        return {t.upper() for t in re.split(r"[,;\s]+", v) if t}, "text"
    if isinstance(v, (list, tuple)):
        out = set()
        for x in v:
            if isinstance(x, str):
                out.add(x.strip().upper())
            elif isinstance(x, dict):
                ok = all(_wahr(x[k]) for k in ("ok", "nachgezogen", "fertig", "erledigt") if k in x)
                f = x.get("feld") or x.get("id") or x.get("name")
                if ok and isinstance(f, str):
                    out.add(f.strip().upper())
                if ok and isinstance(x.get("felder"), (list, tuple)):
                    out |= {str(f2).strip().upper() for f2 in x["felder"]}
            elif isinstance(x, (list, tuple)) and x and isinstance(x[0], str):
                out.add(x[0].strip().upper())
        return out, "liste"
    if isinstance(v, dict):
        if isinstance(v.get("felder"), (list, tuple)):
            return {str(f).strip().upper() for f in v["felder"]}, "objekt.felder"
        return {str(k).strip().upper() for k, w in v.items() if _wahr(w)}, "objekt"
    if not v:
        return set(), "leer"
    return None, "unbekannt (%s)" % type(v).__name__


def einbau_ordner_finden(einbau, daten1m, gefaelle, sehens, sw_ordner):
    """sehens_einbau/ im Welt-Export: --einbau, sonst <daten1m>/sehens_einbau, <Eltern von --gefaelle>/sehens_einbau,
    <sw-ordner>/sehens_einbau, <Eltern von --sehens>/sehens_einbau (erster vorhandener). Lokal liegen gefaelle/, sehens/
    und sehens_einbau/ alle in export/unreal/welt (= --daten1m)."""
    if einbau:
        return einbau if os.path.isdir(einbau) else None
    kand = [daten1m, os.path.dirname(os.path.abspath(gefaelle)) if gefaelle else None, sw_ordner,
            os.path.dirname(os.path.abspath(sehens)) if sehens else None]
    for b in kand:
        if b and os.path.isdir(os.path.join(b, "sehens_einbau")):
            return os.path.join(b, "sehens_einbau")
    return None


def lauf_json_lesen(einbau, lauf_id):
    """sehens_einbau/A15_<lauf>/lauf.json -> (felder|'alle'|None, form, rel) oder None (Datei fehlt = ungebaut)."""
    if not einbau:
        return None
    rel = "sehens_einbau/A15_%s/lauf.json" % lauf_id
    pf = os.path.join(einbau, "A15_" + lauf_id, "lauf.json")
    if not os.path.exists(pf):
        return None
    try:
        d = lese_json(pf)
    except (OSError, ValueError):
        return None, "nicht lesbar", rel
    f, form = nachgezogen_felder(d)
    return f, form, rel


def _deckt(fe, felder):
    if fe == "alle":
        return True
    return bool(fe) and bool(felder) and {str(f).upper() for f in felder} <= fe


def gelaende_laden(gel, gef_basis, gef_plaene, sehens_basis, gebaut_ids=(), einbau=None, ohne_dateien=None):
    """Gelaende-Deltas der Planer zu gel hinzufuegen. Deltas schon gebauter Laeufe (lokal bereits in welt/ eingestempelt)
    werden NICHT addiert (16d):
      - Lauf-ID (gefaelle) bzw. Ort-ID oder SW_<ort>_<bach> (Sehens) in gebaut_ids (--gebaut), oder
      - sehens_einbau/A15_<lauf>/lauf.json existiert und 'nachgezogen' enthaelt das Feld (alle Felder des Eintrags);
        Sehens: A15_<ort>/lauf.json oder A15_SW_<ort>_<bach>/lauf.json. Fehlt die Datei, gilt der Lauf als ungebaut.
    ohne_dateien (Pruefer): genau diese Delta-Dateien weglassen, keine Erkennung.
    Rueckgabe info (addiert, ohne, gebaut[], lauf_json_ungebaut[], ohne_dateien[])."""
    gebaut_ids = set(gebaut_ids or ())
    info = {"addiert": 0, "ohne": 0, "gebaut": [], "lauf_json_ungebaut": [], "ohne_dateien": []}

    def eintragen(basis, rel_basis, eintraege, wer, art, felder_std, quelle):
        rein = []
        n_ohne = 0
        for e in eintraege or []:
            g = e.get("gelaende") or {}
            if not g.get("datei"):
                continue
            rel = "%s/%s" % (rel_basis, g["datei"])
            if ohne_dateien is not None:
                weg = rel in ohne_dateien
            else:
                fel = e.get("felder") or felder_std
                weg = quelle is not None and (quelle[0] == "--gebaut" or _deckt(quelle[1], fel))
            if weg:
                n_ohne += 1
                info["ohne_dateien"].append(rel)
            else:
                rein.append(e)
        info["addiert"] += gel.delta_hinzu(basis, rein)
        info["ohne"] += n_ohne
        if n_ohne and ohne_dateien is None:
            info["gebaut"].append({"id": wer, "art": art, "quelle": quelle[0] if quelle[0] == "--gebaut" else quelle[2],
                                   "nachgezogen_form": None if quelle[0] == "--gebaut" else quelle[3],
                                   "felder": sorted(felder_std or []), "deltas_ohne": n_ohne})

    for lauf in sorted(gef_plaene or {}):
        plan = lese_json(gef_plaene[lauf])
        felder = plan.get("felder") or []
        quelle = None
        if ohne_dateien is None:
            if lauf in gebaut_ids:
                quelle = ("--gebaut", None, None, None)
            else:
                lj = lauf_json_lesen(einbau, lauf)
                if lj is not None:
                    quelle = ("lauf.json", lj[0], lj[2], lj[1])
                    if not _deckt(lj[0], felder):
                        info["lauf_json_ungebaut"].append({"id": lauf, "lauf_json": lj[2], "nachgezogen_form": lj[1],
                                                           "felder": sorted(felder)})
        eintragen(os.path.join(gef_basis, lauf), "gefaelle/%s" % lauf, plan.get("abschnitte"), lauf, "gefaelle", felder,
                  quelle)
        del plan
    if sehens_basis and os.path.isdir(sehens_basis):
        for biom in BIOME:
            po = os.path.join(sehens_basis, biom, "orte.json")
            if not os.path.exists(po):
                continue
            od = lese_json(po)
            for ort in od.get("orte") or []:
                if not (ort.get("gelaende") or {}).get("datei"):
                    continue
                oid = ort["id"]
                felder = ort.get("felder") or []
                quelle = None
                if ohne_dateien is None:
                    laeufe = [oid] + sorted(w.get("wasser_koerper_lauf") or "SW_%s_%s" % (oid, w.get("id"))
                                            for w in ort.get("wasser") or [] if w.get("typ") == "bach")
                    if any(g == oid or g.startswith("SW_%s_" % oid) for g in gebaut_ids):
                        quelle = ("--gebaut", None, None, None)
                    else:
                        for lid in laeufe:
                            lj = lauf_json_lesen(einbau, lid)
                            if lj is None:
                                continue
                            if _deckt(lj[0], felder):
                                quelle = ("lauf.json", lj[0], lj[2], lj[1])
                                break
                            info["lauf_json_ungebaut"].append({"id": lid, "lauf_json": lj[2], "nachgezogen_form": lj[1],
                                                               "felder": sorted(felder)})
                eintragen(os.path.join(sehens_basis, biom), "sehens/%s" % biom, [ort], oid, "sehens", felder, quelle)
    info["ohne_dateien"] = sorted(info["ohne_dateien"])
    return info


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


def _iv_teilen(a, b, iv):
    """[a, b] an den Intervallen iv (a_, b_, id) teilen: Liste (x0, x1, id|None), Stuecke < 5 cm entfallen."""
    st, x = [], a
    for p0, p1, sid in sorted(iv):
        if p1 <= a + 1e-6 or p0 >= b - 1e-6:
            continue
        p0, p1 = max(p0, a), min(p1, b)
        if p0 - x > 0.05:
            st.append([x, p0, None])
        elif st:
            st[-1][1] = p0
        else:
            p0 = x
        st.append([p0, p1, sid])
        x = p1
    if b - x > 0.05 or not st:
        st.append([x, b, None])
    else:
        st[-1][1] = b
    return st


def segmente_toepfe(segs, tp_iv):
    """Bereiche an den Toepfen teilen (16d): Topf = eigener Bereich mit Rolle 'topf'."""
    out = []
    for g in segs:
        st = _iv_teilen(g["a"], g["b"], tp_iv)
        for k, (x0, x1, sid) in enumerate(st):
            n = {"a": x0, "b": x1, "oben": g["oben"] if k == 0 else None, "unten": g["unten"] if k == len(st) - 1 else None,
                 "innen": g["innen"] if k == 0 else []}
            if k == 0 and g.get("rest_oben"):
                n["rest_oben"] = True
            if k == len(st) - 1 and g.get("rest_unten"):
                n["rest_unten"] = True
            if sid:
                n["topf"] = sid
            out.append(n)
    return out


def becken_ohne_toepfe(becken, tp_iv):
    out = []
    for bk in becken:
        st = [x for x in _iv_teilen(bk["s_m"][0], bk["s_m"][1], tp_iv) if x[2] is None]
        for k, (x0, x1, _) in enumerate(st):
            out.append({"s_m": [x0, x1], "oben": bk["oben"] if x0 <= bk["s_m"][0] + 1e-6 else None,
                        "unten": bk["unten"] if x1 >= bk["s_m"][1] - 1e-6 else None})
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


def zelle_max_ungeteilt(typ, S):
    """16e: hoechste Zelle, bis zu der ein Gewaesser mit EINER SWR auskommt (Bach 0,40 m, Fluss wie zelle_max_fluss_m)."""
    if typ == "bach":
        return S.get("zelle_max_bach_ungeteilt_m", S["zelle_max_bach_m"])
    return S["zelle_max_fluss_m"]


def tempo_regel(ss_m, z_cm, b_cm, t_cm, kst, rollen, T):
    """16e: Tempo je Splinepunkt aus dem Gefaelle des Wasserspiegels (Manning-Strickler bei Normalabfluss), Rueckgabe
    (tempo_ms, gefaelle). Rechnet nur mit den gerundeten Spline-Werten (s, z, Breite, Tiefe) und k_st je Punkt, damit
    der Pruefer exakt nachrechnen kann.
      I  = (z(s - w) - z(s + w)) / (2 w), w = fenster_halb_m (am Rand einseitig); Stufen zaehlen mit
      Q  = v_becken_ref * Median(b * h) ueber +-q_fenster_m (Abfluss: ein Becken mittlerer Groesse fliesst mit
           v_becken_ref), b = RiverWidth, h = max(Depth * tiefe_mittel_anteil, tiefe_min_m)
      q  = Q / b (Abfluss je Meter Breite: Engstellen schneller, breite Becken langsamer)
      v  = k_st^(3/5) * q^(2/5) * max(I, gefaelle_min)^(3/10)   (Manning, breites Gerinne R ~ h, h = Normaltiefe)
      Becken/Topf (Rueckstau von der Lippe, die Tiefe ist die Beckentiefe): v = min(v, q / h)  (Kontinuitaet)
      v  = clip(v, v_min_ms, v_max_ms), Gauss-Glaettung entlang s (glatt_sigma_m, Gewicht x halber Punktabstand),
           dann untere Huelle mit |dv/ds| <= aenderung_max_ms_je_m (nur Spitzen sinken)
      tempo_ms = round(tempo_faktor * v, 3)"""
    s = np.asarray(ss_m, float)
    z = np.asarray(z_cm, float) / 100.0
    b = np.maximum(np.asarray(b_cm, float) / 100.0, 0.1)
    h = np.maximum(np.asarray(t_cm, float) / 100.0 * T["tiefe_mittel_anteil"], T["tiefe_min_m"])
    k = np.asarray(kst, float)
    n = len(s)
    if n == 0:
        return np.zeros(0), np.zeros(0)
    w = T["fenster_halb_m"]
    lo = np.maximum(s - w, s[0])
    hi = np.minimum(s + w, s[-1])
    dz = np.interp(lo, s, z) - np.interp(hi, s, z)
    ds = hi - lo
    gef = np.where(ds > 1e-6, dz / np.where(ds > 1e-6, ds, 1.0), 0.0)
    gef = np.round(np.maximum(gef, 0.0), 4)
    A = b * h
    qf = T["q_fenster_m"]
    Q = np.empty(n)
    for i in range(n):
        j0 = int(np.searchsorted(s, s[i] - qf, side="left"))
        j1 = int(np.searchsorted(s, s[i] + qf, side="right"))
        Q[i] = T["v_becken_ref_ms"] * float(np.median(A[j0:j1]))
    q = Q / b
    v = k ** 0.6 * q ** 0.4 * np.maximum(gef, T["gefaelle_min"]) ** 0.3
    stau = np.array([r in T["rueckstau_rollen"] for r in rollen], bool)
    v = np.where(stau, np.minimum(v, q / h), v)
    v = np.clip(v, T["v_min_ms"], T["v_max_ms"])
    sig = T["glatt_sigma_m"]
    if n > 1 and sig > 0:
        gew = np.empty(n)
        gew[1:-1] = 0.5 * (s[2:] - s[:-2])
        gew[0] = 0.5 * (s[1] - s[0])
        gew[-1] = 0.5 * (s[-1] - s[-2])
        gew = np.maximum(gew, 1e-3)
        vg = np.empty(n)
        for i in range(n):
            j0 = int(np.searchsorted(s, s[i] - 3.0 * sig, side="left"))
            j1 = int(np.searchsorted(s, s[i] + 3.0 * sig, side="right"))
            d = (s[j0:j1] - s[i]) / sig
            wi = np.exp(-0.5 * d * d) * gew[j0:j1]
            vg[i] = float((wi * v[j0:j1]).sum() / wi.sum())
        v = vg
    g = T["aenderung_max_ms_je_m"]
    for i in range(1, n):
        v[i] = min(v[i], v[i - 1] + g * (s[i] - s[i - 1]))
    for i in range(n - 2, -1, -1):
        v[i] = min(v[i], v[i + 1] + g * (s[i + 1] - s[i]))
    tempo = np.round(T["tempo_faktor"] * v, 3)
    return tempo, gef


def schaum_maske(fl, sp, linie, regeln):
    """16e Option B: Kapseln fuer den Simulationsschaum nur an Vorhang-Faellen (Aufprall bis Ende des Aufprallteppichs)."""
    M = regeln["schaum"]["maske"]
    out = []
    for f in fl:
        if not f["vorhang"]:
            continue
        tep = next((o for o in f["schaum_objekte"] if o["art"] == "aufprallteppich"), None)
        sa = f["s_fuss_m"]
        if tep is not None:
            sb = min(max(tep["s_m"][1], sa), sa + M["nachlauf_max_m"])
            br = tep["groesse_m"][1]
        else:
            sb = min(sa + M["nachlauf_max_m"], float(linie.s[-1]))
            br = f["lippe_breite_m"]
        sb = min(sb, float(linie.s[-1]))
        rad = min(max(0.5 * br, M["radius_min_m"]), M["radius_max_m"])
        pa, pb = linie.bei(sa), linie.bei(sb)
        out.append({"fall": f["id"], "s_m": [r1(sa, 2), r1(sb, 2)],
                    "a_cm": [r1(pa["x"]), r1(pa["y"]), r1(linie.z_bei(sa, "unten"))],
                    "b_cm": [r1(pb["x"]), r1(pb["y"]), r1(linie.z_bei(sb, "unten"))],
                    "radius_m": r1(rad, 2),
                    "staerke": r1(min(max(f["fall_m"] / M["staerke_fall_m"], M["staerke_min"]), 1.0), 2)})
    return {"kapseln": out, "n": len(out), "slots_max": M["slots_max"], "ueber_slots": len(out) > M["slots_max"],
            "felder_material": "je Slot k: ELD_Fall_A_k = (a.x, a.y, radius_cm, staerke), ELD_Fall_B_k = (b.x, b.y, 0, 0) (Vorschlag)",
            "hinweis": "Option B (16e): Simulationsschaum nur innerhalb dieser Kapseln sichtbar, sonst Schaum aus. Nur Vorhang-Faelle."}


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
             "becken": becken_aus(abst, linie), "zufluesse": plan.get("zufluesse") or [],
             # 16c Nachtrag 3: Feldgrenzen mit zwei Plaenen - Besitzgrenze der Ueberlappung (gefaelle_daten.feldgrenzen)
             "feldgrenzen": {(e["nachbar"], e["seite"]): e for e in (plan.get("feldgrenzen") or {}).get("ueberlappungen") or []}}
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


def zusammenfuegen(kette, links, regeln, topf_oben=None, topf_unten=None):
    """Verkettet die Linien der Teile zu einer Gewaesser-Linie. An Ueberlappungen (Feldgrenzen) wird das Teil ohne Plan
    gekuerzt, sonst das untere. Toepfe (16d): Verbindung 'topf' fuehrt vom Ende des Zulaufs ueber die Topfmitte zum Anfang
    des Abflusses; topf_oben/topf_unten setzen die Topfmitte vor den Anfang bzw. hinter das Ende. Der Topfpunkt liegt auf
    dem Spiegel, Breite = groesste Rechteckseite + 2 x Rand (damit das SWR-Rechteck den Topf einschliesst).
    Rueckgabe (linie, abst, extra, laeufe)."""
    cut = [[t.s0, t.s1] for t in kette]
    if kette and (kette[0].extra.get("kopf") or {}).get("s_m") is not None:
        cut[0][0] = float(np.clip(kette[0].extra["kopf"]["s_m"], kette[0].s0, kette[0].s1))   # 16h Nachtrag 3
    for i, l in enumerate(links):
        if l["art"] == "ueberlappung":
            P, N = kette[i], kette[i + 1]
            gp = (P.extra.get("feldgrenzen") or {}).get((N.id, "ende"))
            gn = (N.extra.get("feldgrenzen") or {}).get((P.id, "anfang"))
            if N.herkunft == "plan" and P.herkunft != "plan":
                cut[i][1] = l["s_p"]
            elif P.herkunft == "plan" and N.herkunft == "plan" and gp and gn:
                # 16c Nachtrag 3: zwei Plaene - Schnitt an der Besitzgrenze (Lippe gehoert dem Plan ihres Felds), keine
                # Stufe entfaellt; beide Plaene haben dort den alten Spiegel
                cut[i][1] = float(np.clip(gp["grenze_s_m"], P.s0, P.s1))
                cut[i + 1][0] = float(np.clip(gn["grenze_s_m"], N.s0, N.s1))
                l["schnitt"] = "feldgrenze"
            else:
                cut[i + 1][0] = l["s_n"]
    S, X, Y, Z, B, T, V, K = [], [], [], [], [], [], [], []
    abst, eff, strahl, vorhang, kns = [], [], {}, set(), []
    ufer = {"s_m": [], "einzug_links_m": [], "einzug_rechts_m": []}
    laeufe = []
    ende = None
    toepfe = []
    vmin = regeln["abschnitt"]["velocity_min_cm_s"]

    def topf_punkt(tp, s_):
        S.append(s_); X.append(tp["mitte_cm"][0]); Y.append(tp["mitte_cm"][1]); Z.append(tp["spiegel_cm"])
        B.append(tp["breite_cm"]); T.append(tp["tiefe_cm"]); V.append(vmin); K.append("topf")

    def topf_eintrag(tp, s_a, s_b):
        toepfe.append({"see": tp["see"], "art": tp["art"], "s_m": [r1(s_a, 2), r1(s_b, 2)], "spiegel_cm": r1(tp["spiegel_cm"]),
                       "ausdehnung_m": tp["ausdehnung_m"], "rechteck_cm": [r1(v) for v in tp["rechteck_cm"]],
                       "mitte_cm": [r1(tp["mitte_cm"][0]), r1(tp["mitte_cm"][1])], "breite_spline_cm": r1(tp["breite_cm"]),
                       "tiefe_cm": r1(tp["tiefe_cm"]), "zulauf": tp["zulauf"], "abfluss": tp["abfluss"],
                       "water_body_lake": False, "hinweis": "Topf ist Teil des Gewaessers: kein WaterBodyLake, die SWR fuellt ihn"})

    if topf_oben is not None:
        topf_punkt(topf_oben, 0.0)
        ende = (topf_oben["mitte_cm"][0], topf_oben["mitte_cm"][1], 0.0)
        topf_a = 0.0
    for i, t in enumerate(kette):
        a, b = cut[i]
        A = ausschnitt(t.linie, a, b)
        tp = links[i - 1].get("topf") if i > 0 and links[i - 1]["art"] == "topf" else None
        if tp is not None:
            topf_a = ende[2]
            s_c = ende[2] + max(math.hypot(tp["mitte_cm"][0] - ende[0], tp["mitte_cm"][1] - ende[1]) / 100.0, 1e-3)
            topf_punkt(tp, s_c)
            ende = (tp["mitte_cm"][0], tp["mitte_cm"][1], s_c)
        if ende is None:
            off = -a
        else:
            gap = max(math.hypot(A["x"][0] - ende[0], A["y"][0] - ende[1]) / 100.0, 1e-3)
            off = ende[2] + gap - a
        if tp is not None or (i == 0 and topf_oben is not None):
            topf_eintrag(tp if tp is not None else topf_oben, topf_a, a + off)
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
    if topf_unten is not None:
        s_c = ende[2] + max(math.hypot(topf_unten["mitte_cm"][0] - ende[0], topf_unten["mitte_cm"][1] - ende[1]) / 100.0, 1e-3)
        topf_eintrag(topf_unten, ende[2], s_c)
        topf_punkt(topf_unten, s_c)
    linie = Linie(S, X, Y, Z, B, T, V, K)
    abst.sort(key=lambda d: (d["s_lippe"], d["id"]))
    extra = {"effekte": eff, "strahl": strahl, "vorhang": vorhang, "kaskadennetze": kns,
             "ufer_rand": ufer if ufer["s_m"] else None, "roh": all(t.roh for t in kette), "toepfe": toepfe}
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
        rollen.append("topf" if "topf" in r_ else "becken" if all(x in ("becken", "uebergang", "fuss") for x in r_) else
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
          "punkt_typen": ptyp, "tangenten_cm": tang, "punkte_s_m": [r1(x, 2) for x in ss], "punkt_rollen": rollen,
          "_v_alt": [r1(x) for x in v]}
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


def rand_steil(P, ss, i0, i1, a_sim, b_sim, ist_quelle, regeln):
    """16g (Diagnose, aendert nichts): Rand und Steilheit eines SWR-Bereichs.
    UE-Rechteck = Box der Splinepunkte OHNE Breite (16g Befund 8: Simulationsflaeche = Rechteck um die Splinepunkte ohne
    Rand, Quelle 0,2 m vom Nordrand). kontakte = zusammenhaengende Punktfolgen, deren halbe Breite ueber das UE-Rechteck
    hinausragt (dort liegt das Bett teils ausserhalb der Simulation). rahmen_cm = Rechteck, das jedes Bett +- (halbe Breite
    + rand_zugabe_m) enthaelt (Soll, falls die Flaeche lokal erweitert werden kann). Steilheit: Spiegelgefaelle I im
    gleitenden Fenster fenster_m (1-m-Schritt, Spline-z linear zwischen den Punkten, Stufen zaehlen mit); Strecken mit
    I >= gefaelle_pruefen bzw. >= gefaelle_kaskade (Vereinigung der Fenster, >= strecke_min_m)."""
    R = regeln["swr"]["rand_steil"]
    Q = np.asarray(P, float)[i0:i1 + 1]
    s_ = np.asarray(ss, float)[i0:i1 + 1]
    h = Q[:, 3] / 2.0
    x0, y0, x1, y1 = float(Q[:, 0].min()), float(Q[:, 1].min()), float(Q[:, 0].max()), float(Q[:, 1].max())
    zug = R["rand_zugabe_m"] * 100.0
    rahmen = [float((Q[:, 0] - h - zug).min()), float((Q[:, 1] - h - zug).min()),
              float((Q[:, 0] + h + zug).max()), float((Q[:, 1] + h + zug).max())]
    # Abstand des ersten Punkts (Quelle bzw. Anfang des Teilstuecks) zum UE-Rechteck
    p0 = Q[0]
    seiten0 = {"W": p0[0] - x0, "O": x1 - p0[0], "S": p0[1] - y0, "N": y1 - p0[1]}
    s0_seite = min(sorted(seiten0), key=lambda k: seiten0[k])
    # Kontakte je Seite
    kont = []
    for seite, d in (("W", Q[:, 0] - x0), ("O", x1 - Q[:, 0]), ("S", Q[:, 1] - y0), ("N", y1 - Q[:, 1])):
        ue = h - d
        an = None
        for j in range(len(Q) + 1):
            drin = j < len(Q) and ue[j] > 0.0
            if drin and an is None:
                an = j
            elif not drin and an is not None:
                seg = ue[an:j]
                lo_, hi_ = float(s_[an]), float(s_[j - 1])
                am_ende = lo_ <= float(s_[0]) + R["quelle_abstand_min_m"] + 1e-9 or hi_ >= float(s_[-1]) - R["quelle_abstand_min_m"] - 1e-9
                kont.append({"seite": seite, "s_m": [r1(lo_, 2), r1(hi_, 2)], "laenge_m": r1(hi_ - lo_, 2),
                             "punkt_index": [i0 + an, i0 + j - 1], "am_ende": bool(am_ende),
                             "ueberstand_max_m": r1(float(seg.max()) / 100.0, 2),
                             "z_m": r1(float(Q[an + int(np.argmax(seg)), 2]) / 100.0, 2)})
                an = None
    kont.sort(key=lambda k: (k["s_m"][0], k["seite"]))
    # Steilheit (Spiegel der Spline)
    fen = R["fenster_m"]
    z_ = Q[:, 2] / 100.0
    a, b = float(a_sim), float(b_sim)
    strecken, i_max, s_imax = [], 0.0, None
    if b - a >= fen - 1e-9:
        n = int(math.floor(b - a - fen + 1e-9)) + 1
        st = a + np.arange(n, dtype=float)
        I = (np.interp(st, s_, z_) - np.interp(st + fen, s_, z_)) / fen
        k = int(np.argmax(I))
        i_max, s_imax = float(I[k]), float(st[k])
        def vereinigung(gr):
            iv = []
            for j in np.nonzero(I >= gr - 1e-12)[0]:
                lo, hi = float(st[j]), float(st[j] + fen)
                if iv and lo <= iv[-1][1] + 1e-9:
                    iv[-1][1] = max(iv[-1][1], hi)
                else:
                    iv.append([lo, hi])
            return [v for v in iv if v[1] - v[0] >= R["strecke_min_m"] - 1e-9]
        iv_k = vereinigung(R["gefaelle_kaskade"])
        iv_p = []
        for lo, hi in vereinigung(R["gefaelle_pruefen"]):      # pruefen = ohne die Kaskaden-Strecken
            teile = [[lo, hi]]
            for a_, b_ in iv_k:
                neu = []
                for c_, d_ in teile:
                    if b_ <= c_ or a_ >= d_:
                        neu.append([c_, d_])
                        continue
                    if a_ > c_:
                        neu.append([c_, a_])
                    if b_ < d_:
                        neu.append([b_, d_])
                teile = neu
            iv_p += [v for v in teile if v[1] - v[0] >= R["strecke_min_m"] - 1e-9]
        for klasse, iv in (("kaskade", iv_k), ("pruefen", iv_p)):
            for lo, hi in iv:
                dz = float(np.interp(lo, s_, z_) - np.interp(hi, s_, z_))
                strecken.append({"klasse": klasse, "s_m": [r1(lo, 2), r1(hi, 2)], "laenge_m": r1(hi - lo, 2),
                                 "dz_m": r1(dz, 2), "gefaelle_mittel": r1(dz / (hi - lo), 3)})
    strecken.sort(key=lambda t: (t["s_m"][0], t["klasse"]))
    lk = sum(t["laenge_m"] for t in strecken if t["klasse"] == "kaskade")
    lp = sum(t["laenge_m"] for t in strecken if t["klasse"] == "pruefen")
    eignung = "kaskade_vorschlag" if lk > 0 else ("pruefen" if lp > 0 else "swr")
    return {
        "status": R["status"],
        "rechteck_ue_cm": [r1(x0) + 0.0, r1(y0) + 0.0, r1(x1) + 0.0, r1(y1) + 0.0],
        "anfang": {"art": "quelle" if ist_quelle else "teilstueck", "seite": s0_seite, "abstand_m": r1(seiten0[s0_seite] / 100.0, 2),
                   "halbe_breite_m": r1(float(h[0]) / 100.0, 2),
                   "zu_nah": bool(seiten0[s0_seite] < R["quelle_abstand_min_m"] * 100.0 - 1e-6)},
        "kontakte": kont,
        "rahmen_cm": [r1(v) for v in rahmen],
        "rahmen_m": [r1((rahmen[2] - rahmen[0]) / 100.0, 2), r1((rahmen[3] - rahmen[1]) / 100.0, 2)],
        "hoehenspanne_m": r1(float(z_.max() - z_.min()), 2),
        "z_m": [r1(float(z_.max()), 2), r1(float(z_.min()), 2)],
        "gefaelle_fenster_max": r1(i_max, 3), "gefaelle_fenster_max_s_m": None if s_imax is None else r1(s_imax, 2),
        "steilstrecken": strecken,
        "laenge_kaskade_m": r1(lk, 2), "laenge_pruefen_m": r1(lp, 2),
        "eignung": eignung}


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


FILTER_KLASSEN = ("lippe", "rand", "bett")


def hindernis_rolle(rolle, F):
    """v11 (16g Nachtrag 2): Bachdekor-Rolle eines Objekts aus der Instanz-Ebene (dateien.<netz>.rolle, mehrere mit '/').
    Rueckgabe 'lippe', 'rand', 'bett' bzw. deren Verbindung ('bett+rand'), wenn ALLE Rollen der Datei zu diesen Klassen
    gehoeren; 'unklar' bei gemischten Dateien, 'andere' ohne solche Rolle, 'akteur' fuer Akteure (rolle None)."""
    if rolle is None:
        return "akteur"
    teile = [x for x in str(rolle).split("/") if x]
    if not teile:
        return "andere"
    kl = set()
    for x in teile:
        k_ = next((n for n in FILTER_KLASSEN if re.search(F["rollen"][n], x)), "andere")
        kl.add(k_)
    if "andere" not in kl:
        return "+".join(sorted(kl))
    return "unklar" if len(kl) > 1 else "andere"


def ref_text_von(ref):
    return "%s#%s#%d" % (ref["quelle"], ref.get("datei", "akteure"), ref["index"])


def hindernis_mass(ecken_cm, cx_m, cy_m, P, ss):
    """v11: Mass eines Teils gegen die Spline. P (N, >=4) in cm (x, y, z, RiverWidth), ss (N) in m. Naechster
    Splineabschnitt zum Mittelpunkt; quer = Ausdehnung der 8 Ecken quer zur Spline, beschnitten auf das Bett (+- halbe
    Breite); laengs = s-Bereich der Ecken entlang der Spline. Rueckgabe (quer_m, breite_m, s_von, s_bis, s_mitte)."""
    A, B = P[:-1, :2], P[1:, :2]
    AB = B - A
    L2 = np.maximum((AB ** 2).sum(1), 1e-9)
    c = np.array([cx_m * 100.0, cy_m * 100.0])
    t = np.clip(((c - A) * AB).sum(1) / L2, 0.0, 1.0)
    Q = A + t[:, None] * AB
    j = int(np.argmin(((Q - c) ** 2).sum(1)))
    tj = float(t[j])
    L = math.sqrt(float(L2[j]))
    tx, ty = float(AB[j, 0]) / L, float(AB[j, 1]) / L
    d = ecken_cm[:, :2] - Q[j][None, :]
    u = d[:, 0] * -ty + d[:, 1] * tx
    a = d[:, 0] * tx + d[:, 1] * ty
    breite = (float(P[j, 3]) + tj * (float(P[j + 1, 3]) - float(P[j, 3]))) / 100.0
    halb = 50.0 * breite
    quer = max(0.0, min(float(u.max()), halb) - max(float(u.min()), -halb)) / 100.0
    s_m = float(ss[j]) + tj * (float(ss[j + 1]) - float(ss[j]))
    return quer, breite, s_m + float(a.min()) / 100.0, s_m + float(a.max()) / 100.0, s_m


def hindernis_filter_entscheiden(teile, ss, breiten, F):
    """v11: Entscheidung je Teil. teile: Liste dicts mit key, rolle, quer, breite, s (von, bis); Werte schon auf mm/cm
    gerundet. ss/breiten: Splinepunkte (m) fuer die Bettbreite je Meter. Rueckgabe {key: 'behalten' | 'filter_rolle' |
    'filter_teil' | 'filter_meter'}. Meter-Regel gierig: schmalste zuerst, dann key."""
    out = {}
    kand = []
    for tl in teile:
        if tl["rolle"] in ("akteur", "andere", "unklar"):
            pass
        else:
            out[tl["key"]] = "filter_rolle"
            continue
        if tl["quer"] > F["teil_max_anteil"] * tl["breite"] + 1e-9:
            out[tl["key"]] = "filter_teil"
            continue
        if tl["quer"] <= 0.0:
            out[tl["key"]] = "behalten"
            continue
        kand.append(tl)
    mm = float(F["meter_m"])
    s0, s1 = float(ss[0]), float(ss[-1])
    summe = {}
    for tl in sorted(kand, key=lambda x: (x["quer"], x["key"])):
        b0 = int(math.floor(max(s0, tl["s"][0]) / mm))
        b1 = int(math.floor(min(s1, tl["s"][1]) / mm))
        bins = list(range(b0, max(b0, b1) + 1))
        ok = True
        for bi in bins:
            sm = min(max((bi + 0.5) * mm, s0), s1)
            w = round(float(np.interp(sm, ss, breiten)), 2)
            if summe.get(bi, 0.0) + tl["quer"] > F["meter_max_anteil"] * w + 1e-9:
                ok = False
                break
        if ok:
            for bi in bins:
                summe[bi] = summe.get(bi, 0.0) + tl["quer"]
            out[tl["key"]] = "behalten"
        else:
            out[tl["key"]] = "filter_meter"
    return out


def source_size_regel(breite_cm, SV):
    """source_size_cm: v8 RiverWidth am ersten Punkt des SWR-Bereichs; v11 mindestens source_size_min_cm (300)."""
    if SV.get("source_size") == "breite_quelle_min":
        return r1(max(float(breite_cm), float(SV["source_size_min_cm"])))
    return r1(breite_cm)


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


def _zweierpotenz(x, lo):
    """kleinste Zweierpotenz >= x (mindestens lo)."""
    r = int(lo)
    while r < x - 1e-9:
        r *= 2
    return r


def water_info_bereich(P, ss, i0, i1, regeln):
    """16g Nachtrag (Regel v10): Wasser-Info der Water Zone. Die Simulation erkennt das Bett nur, wo die Wasser-Info der
    zustaendigen Zone das Bett luecklos rastert (C2: 1,18 m je Pixel -> Luecken, Front steht; 0,29 m -> 99,9 % nass).
    Regel (Ferat): Pixel <= schmalste Bachbreite / breite_teiler (6). Rueckgabe: schmalste Breite (RiverWidth der Punkte
    i0..i1), groesste zulaessige Pixelgroesse, groesste Zone je Aufloesung, noetige Aufloesung in einer Zone von
    zone_bekannt_m (C2: 1208 m)."""
    W = regeln["swr"]["water_info"]
    zug = band_zugabe(regeln)
    Q = np.asarray(P, float)[i0:i1 + 1]
    w = Q[:, 3] / 100.0
    j = int(np.argmin(w))
    bmin = float(w[j])
    band = bmin + zug
    px = band / W["breite_teiler"]
    zb = float(W["zone_bekannt_m"])
    rb = _zweierpotenz(zb / px, W["aufloesung_min"])
    return {
        "status": "Regel v11 (16g Nachtrag 2): Pixel <= schmalstes Band (Bett + %g m) / %g" % (zug, W["breite_teiler"]),
        "breite_min_m": r1(bmin, 2), "breite_min_s_m": r1(float(ss[i0 + j]), 2), "band_min_m": r1(band, 2),
        "breite_median_m": r1(float(np.median(w)), 2),
        "pixel_max_m": r1(px, 4),
        "zone_max_m": {str(r): r1(r * px, 1) for r in W["aufloesungen_zeigen"]},
        "zone_bekannt": {"ausdehnung_m": zb, "aufloesung": rb, "pixel_m": r1(zb / rb, 4),
                         "ueber_max": bool(rb > W["aufloesung_max"]),
                         "pixel_quer": {str(r): r1(band / (zb / r), 2) for r in W["aufloesungen_zeigen"]}}}


def band_zugabe(regeln):
    """v11: Band = Bett + band_zugabe_m (RiverWidth im Editor); 0 ohne Eintrag (v10)."""
    return float(regeln["swr"]["sim_vorgaben"].get("band_zugabe_m", 0.0))


def _zone_mb(box, px, W, art="rgba16f"):
    ex, ey = (box[2] - box[0]) / 100.0, (box[3] - box[1]) / 100.0
    rx = _zweierpotenz(ex / px, W["aufloesung_min"])
    ry = _zweierpotenz(ey / px, W["aufloesung_min"])
    return rx, ry, rx * ry * W["zonen"]["bytes_je_pixel"][art] / 2.0 ** 20


def half_float_stufe_cm(z_abs_max_cm, spanne_cm, mantisse_bits=10):
    """v11 (16g Nachtrag 2): Hoehenstufe einer 16-Bit-Wasser-Info (Half Float, 10 Bit Mantisse). absolut: Z in cm ueber 0
    gespeichert -> Stufe = 2^(floor(log2(|z|)) - 10) (190 m: 16 cm); relativ: Z normiert auf die Spanne (0..1) ->
    Stufe = Spanne x 2^-11 im oberen Halbbereich. Rueckgabe (absolut, relativ) in cm."""
    za = max(float(z_abs_max_cm), 1.0)
    ab = 2.0 ** (math.floor(math.log2(za)) - mantisse_bits)
    rel = max(float(spanne_cm), 0.0) * 2.0 ** -(mantisse_bits + 1)
    return ab, rel


def welt_rechteck_cm():
    from sehens_lib import daten
    return [daten.X_MIN_M * 100.0, daten.Y_MIN_M * 100.0, daten.X_MAX_M * 100.0, daten.Y_MAX_M * 100.0]


def zonen_vorschlag(alle, regeln):
    """16g Nachtrag (Regel v10): Water Zones fuer die ganze Welt, so dass jedes Gewaesser die Regel water_info erfuellt.
    Ein WaterBodyRiver gehoert zu genau einer Zone (WaterZoneOverride bzw. overlap_priority), also muss das ganze Bett
    eines Gewaessers in seiner Zone liegen. Grundzone WZ_WELT (ganze Welt, welt_aufloesung) fuer alle Gewaesser, deren
    geforderte Pixelgroesse sie erfuellt; die uebrigen gierig zu feinen Zonen gruppiert (siehe zone_aufschlag_hinweis).
    Deterministisch. Rueckgabe dict fuer wasserzonen.json."""
    W = regeln["swr"]["water_info"]
    Z = W["zonen"]
    rand = Z["rand_m"] * 100.0
    rmax = W["aufloesung_max"]
    items = []
    for e in alle:
        P = np.asarray(e["water_body"]["spline"]["punkte"], float)
        b = box_punkte(P, 0, len(P) - 1)
        items.append({"id": e["id"], "px": (float(P[:, 3].min()) / 100.0 + band_zugabe(regeln)) / W["breite_teiler"],
                      "z_max": float(P[:, 2].max()), "boden_min": float((P[:, 2] - P[:, 4]).min()),
                      "breite": float(P[:, 3].min()) / 100.0,
                      "box": [b[0] - rand, b[1] - rand, b[2] + rand, b[3] + rand],
                      "swr": [kc["id"] for kc in e["swr_bereiche"]]})
    wb = welt_rechteck_cm()
    wr = Z["welt_aufloesung"]
    px_welt = max((wb[2] - wb[0]) / 100.0 / wr[0], (wb[3] - wb[1]) / 100.0 / wr[1])
    welt = [it for it in items if it["px"] >= px_welt - 1e-9]
    rest = sorted((it for it in items if it["px"] < px_welt - 1e-9), key=lambda it: (it["px"], it["id"]))
    fein = []
    for it in rest:
        rx, ry, alleine = _zone_mb(it["box"], it["px"], W)
        best = None
        for k, z in enumerate(fein):
            if z["ueber_max"]:
                continue
            b = [min(z["box"][0], it["box"][0]), min(z["box"][1], it["box"][1]),
                 max(z["box"][2], it["box"][2]), max(z["box"][3], it["box"][3])]
            px = min(z["px"], it["px"])
            rx_, ry_, mb = _zone_mb(b, px, W)
            if rx_ > rmax or ry_ > rmax:
                continue
            d = mb - z["mb"]
            if d <= alleine + Z["zone_aufschlag_mb"] + 1e-9 and (best is None or d < best[0] - 1e-9):
                best = (d, k, b, px, mb)
        if best is not None:
            z = fein[best[1]]
            z.update(box=best[2], px=best[3], mb=best[4])
            z["items"].append(it)
        else:
            fein.append({"box": list(it["box"]), "px": it["px"], "mb": alleine, "items": [it],
                         "ueber_max": bool(rx > rmax or ry > rmax)})
    fein.sort(key=lambda z: (z["box"][1], z["box"][0], z["items"][0]["id"]))

    def zone_eintrag(zid, art, box, px_soll, mitglieder, res=None, prio=0):
        ex, ey = (box[2] - box[0]) / 100.0, (box[3] - box[1]) / 100.0
        if res is None:
            res = [_zweierpotenz(ex / px_soll, W["aufloesung_min"]), _zweierpotenz(ey / px_soll, W["aufloesung_min"])]
        pix = max(ex / res[0], ey / res[1])
        enger = min(mitglieder, key=lambda it: (it["px"], it["id"])) if mitglieder else None
        H = Z.get("half_precision")
        hp = {}
        if H and mitglieder:
            zmax = max(it["z_max"] for it in mitglieder)
            bmin = min(it["boden_min"] for it in mitglieder)
            ab, rel = half_float_stufe_cm(max(abs(zmax), abs(bmin)), zmax - bmin, H["mantisse_bits"])
            ok = max(ab, rel) <= H["stufe_max_cm"] + 1e-9
            hp = {"hoehe_m": {"spiegel_max": r1(zmax / 100.0, 2), "boden_min": r1(bmin / 100.0, 2),
                              "spanne": r1((zmax - bmin) / 100.0, 2)},
                  "half_float_stufe_cm": {"absolut": r1(ab, 2), "relativ": r1(rel, 2), "massgeblich": r1(max(ab, rel), 2)},
                  "half_precision_ok": bool(ok), "format_empfohlen": "rgba16f" if ok else "rgba32f"}
        return dict({"id": zid, "art": art,
                "rechteck_cm": [r1(v) for v in box], "zentrum_cm": [r1(0.5 * (box[0] + box[2])), r1(0.5 * (box[1] + box[3]))],
                "ausdehnung_m": [r1(ex, 1), r1(ey, 1)], "aufloesung": [int(res[0]), int(res[1])], "pixel_m": r1(pix, 4),
                "pixel_max_m": r1(enger["px"], 4) if enger else None,
                "schmalstes": {"gewaesser": enger["id"], "breite_m": r1(enger["breite"], 2)} if enger else None,
                "ueber_max": bool(max(res) > rmax), "overlap_priority": prio,
                "speicher_mb": {k_: r1(res[0] * res[1] * v / 2.0 ** 20, 1) for k_, v in sorted(Z["bytes_je_pixel"].items())},
                "gewaesser": sorted(it["id"] for it in mitglieder),
                "swr_bereiche": sorted(s_ for it in mitglieder for s_ in it["swr"])}, **hp)
    zonen = [zone_eintrag("WZ_WELT", "welt", wb, None, welt, res=list(wr), prio=Z["prioritaet_welt"])]
    for n, z in enumerate(fein):
        zonen.append(zone_eintrag("WZ_F%02d" % (n + 1), "fein", z["box"], z["px"], z["items"], prio=Z["prioritaet_fein"]))
    zuordnung = {g_: z["id"] for z in zonen for g_ in z["gewaesser"]}
    ra = {}
    for z in zonen:
        k_ = "%dx%d" % tuple(z["aufloesung"])
        ra[k_] = ra.get(k_, 0) + 1
    summe = {"zonen": len(zonen), "fein": len(fein), "gewaesser_welt": len(welt), "gewaesser_fein": len(rest),
             "ueber_max": sum(1 for z in zonen if z["ueber_max"]),
             "aufloesungen": {k_: ra[k_] for k_ in sorted(ra)},
             "speicher_mb": {k_: r1(sum(z["speicher_mb"][k_] for z in zonen), 1) for k_ in sorted(Z["bytes_je_pixel"])},
             "speicher_mb_fein": {k_: r1(sum(z["speicher_mb"][k_] for z in zonen[1:]), 1) for k_ in sorted(Z["bytes_je_pixel"])},
             "pixel_welt_m": r1(px_welt, 4)}
    if Z.get("half_precision"):
        mit = [z for z in zonen if "half_precision_ok" in z]
        summe["half_precision"] = {
            "stufe_max_cm": Z["half_precision"]["stufe_max_cm"],
            "ok": sum(1 for z in mit if z["half_precision_ok"]), "aus": sum(1 for z in mit if not z["half_precision_ok"]),
            "aus_zonen": [z["id"] for z in mit if not z["half_precision_ok"]],
            "speicher_mb_empfohlen": r1(sum(z["speicher_mb"][z["format_empfohlen"]] for z in mit), 1),
            "speicher_mb_empfohlen_fein": r1(sum(z["speicher_mb"][z["format_empfohlen"]] for z in mit if z["art"] == "fein"), 1)}
    return {"format": "fluss_sim_wasserzonen_v1", "regeln_version": regeln["version"], "status": W["status"],
            "regel": "Pixel der Wasser-Info <= schmalstes Band (Bett + %g m) / %g; Aufloesung je Achse Zweierpotenz <= %d"
                     % (band_zugabe(regeln), W["breite_teiler"], rmax),
            "hinweis": "Vorschlag: je Zone ein AWaterZone (zone_extent = ausdehnung_m x 100, render_target_resolution = "
                       "aufloesung, overlap_priority); je Gewaesser WaterZoneOverride = water_body.water_zone_vorschlag. "
                       + Z["format_hinweis"],
            "summe": summe, "zonen": zonen, "gewaesser": {k_: zuordnung[k_] for k_ in sorted(zuordnung)}}


def zonen_bekannt_lesen(pfad):
    """--zonen: bekannte Water Zones (JSON). {"zonen": [{"id", "ausdehnung_m": [x, y] | x, "aufloesung": [x, y] | x,
    ("zentrum_cm": [x, y] | "rechteck_cm": [x0, y0, x1, y1] | "feld": "C2"), "overlap_priority" (0), "gewaesser": [ids]
    (WaterZoneOverride, optional)}]}. Rueckgabe Liste mit rechteck_cm, pixel_m."""
    d = lese_json(pfad)
    out = []
    for z in d.get("zonen") or []:
        ae = z.get("ausdehnung_m")
        au = z["aufloesung"]
        au = [int(au), int(au)] if not isinstance(au, list) else [int(au[0]), int(au[1])]
        if z.get("rechteck_cm"):
            box = [float(v) for v in z["rechteck_cm"]]
            ae = [(box[2] - box[0]) / 100.0, (box[3] - box[1]) / 100.0]
        else:
            ae = [float(ae), float(ae)] if not isinstance(ae, list) else [float(ae[0]), float(ae[1])]
            if z.get("zentrum_cm"):
                cx, cy = float(z["zentrum_cm"][0]), float(z["zentrum_cm"][1])
            else:
                from sehens_lib import daten
                x0, y0, x1, y1 = daten.feld_grenzen_m(z["feld"])
                cx, cy = 50.0 * (x0 + x1), 50.0 * (y0 + y1)
            box = [cx - 50.0 * ae[0], cy - 50.0 * ae[1], cx + 50.0 * ae[0], cy + 50.0 * ae[1]]
        out.append({"id": z["id"], "rechteck_cm": box, "ausdehnung_m": ae, "aufloesung": au,
                    "pixel_m": max(ae[0] / au[0], ae[1] / au[1]), "overlap_priority": z.get("overlap_priority", 0),
                    "gewaesser": list(z.get("gewaesser") or []), "half_precision": z.get("half_precision"),
                    "lage": "rechteck" if z.get("rechteck_cm") else
                    ("zentrum" if z.get("zentrum_cm") else "feld %s (Mitte angenommen)" % z.get("feld"))})
    return out


def zone_bekannt_fuer(gid, box, bekannt):
    """Zustaendige bekannte Zone eines Gewaessers: WaterZoneOverride (gewaesser-Liste), sonst die ueberlappende Zone mit
    der hoechsten overlap_priority (gleich: kleinste Pixelgroesse, dann ID). None, wenn keine bekannt ist."""
    for z in bekannt:
        if gid in z["gewaesser"]:
            return z
    kand = [z for z in bekannt if z["rechteck_cm"][0] < box[2] and z["rechteck_cm"][2] > box[0]
            and z["rechteck_cm"][1] < box[3] and z["rechteck_cm"][3] > box[1]]
    if not kand:
        return None
    return sorted(kand, key=lambda z: (-z["overlap_priority"], z["pixel_m"], z["id"]))[0]


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
    tp_iv = [(tp["s_m"][0], tp["s_m"][1], tp["see"]) for tp in gw.get("toepfe") or []]
    if tp_iv:
        becken = becken_ohne_toepfe(becken, tp_iv)
    sp, stufe_punkt = gewaesser_spline(linie, abst, gw["roh_bei"], R)
    ss = np.asarray(sp["punkte_s_m"], float)
    # 16e: Tempo je Splinepunkt nach dem Gefaelle (Manning-Strickler), ersetzt das Rollen-Tempo des Plans
    T = R["tempo"]
    typ_pkt = [gw["typ_bei"](x) for x in ss]
    kst = [T["kst_bach"] if t_ == "bach" else T["kst_fluss"] for t_ in typ_pkt]
    P0 = np.asarray(sp["punkte"], float)
    tempo, gef = tempo_regel(ss, P0[:, 2], P0[:, 3], P0[:, 4], kst, sp["punkt_rollen"], T)
    for i, p_ in enumerate(sp["punkte"]):
        p_[5] = r1(100.0 * tempo[i])
    v_alt = sp.pop("_v_alt")
    sp["tempo_ms"] = [float(x) for x in tempo]
    sp["tempo_info"] = {"regel": "manning_strickler_16e", "tempo_faktor": T["tempo_faktor"],
                        "gefaelle": [float(x) for x in gef], "kst": kst,
                        "hinweis": "WaterVelocityScalar_cm_s = tempo_ms x 100 (UE-Einheit cm/s); gefaelle = Spiegelgefaelle "
                                   "ueber +-%.1f m; kst = Strickler je Punkt (bach/fluss)" % T["fenster_halb_m"]}
    P = np.asarray(sp["punkte"], float)
    wbr = "WBR_" + gid
    # Bereiche (fruehere Abschnitte) zwischen den Faellen
    segs = segmente_bilden(linie, faelle, R)
    if tp_iv:
        segs = segmente_toepfe(segs, tp_iv)
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
                         "rolle": "topf" if g_.get("topf") else
                         bereich_rolle(a, b, linie, innen, becken, all(gw["roh_bei"](x) for x in (a, 0.5 * (a + b), b))),
                         "oben_fall": g_["oben"], "unten_fall": g_["unten"], "faelle_innen": g_["innen"],
                         "abstuerze_innen": innen, "becken": bec, "laeufe": laeufe_in,
                         "rest_oben": bool(g_.get("rest_oben")), "rest_unten": bool(g_.get("rest_unten"))})
        if g_.get("topf"):
            bereiche[-1]["topf"] = g_["topf"]
    # SWR-Bereiche (Nachtrag 17:45): eine SWR je Gewaesser, Aufloesung bis 2048; nur sehr grosse Rechtecke teilen
    zmax_pkt = np.array([S["zelle_max_bach_m"] if t_ == "bach" else S["zelle_max_fluss_m"] for t_ in typ_pkt], float)
    L_max = S["resolution_max"] * zmax_pkt
    # 16e: Baeche bleiben bis zelle_max_bach_ungeteilt_m ungeteilt; geteilt wird mit zelle_max_bach_m je Stueck
    zun_pkt = np.array([zelle_max_ungeteilt(t_, S) for t_ in typ_pkt], float)
    achse_ges = achse_von(box_punkte(P, 0, len(P) - 1))
    if achse_ges <= S["resolution_max"] * float(zun_pkt.min()) + 1e-9:
        teile_ = [{"a": s0, "b": s1, "naht_oben": {"art": "quelle", "s_m": s0}, "naht_unten": {"art": "muendung", "s_m": s1}}]
    else:
        teile_ = swr_teilen(sp, abst, becken, R, L_max)
    ue = S["teilung"]["ueberlappung_m"] / 2.0
    n_k = len(teile_)
    einzel = n_k == 1
    rand = S["rand_m"] * 100.0
    SV = S["sim_vorgaben"]
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
        zmax = zelle_max_ungeteilt(typ, S) if einzel else (S["zelle_max_bach_m"] if typ == "bach" else S["zelle_max_fluss_m"])
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
                    "match_spline": SV["match_spline"],
                    "match_spline_height_amount": SV["match_spline_height_amount"],
                    "remove_outside_spline_amount": SV["remove_outside_spline_amount"],
                    "band_zugabe_m": SV.get("band_zugabe_m", 0.0),
                    "source_size_cm": source_size_regel(P[i0, 3], SV),
                    "sim_speed": SV["sim_speed"], "num_steps": SV["num_steps"],
                    "begrenzung": ({"art": "rechteck_um_fluss", "hinweis": "SWR-Bereich = achsparalleles Rechteck um den Fluss (16c Nachtrag 17:45)"}
                                   if einzel else
                                   {"art": "rechteck_teil", "rechteck_cm": [r1(box[0]), r1(box[1]), r1(box[2]), r1(box[3])],
                                    "zentrum_cm": [r1(0.5 * (box[0] + box[2])), r1(0.5 * (box[1] + box[3]))],
                                    "hinweis": S["teilung"]["geteilt_hinweis"]}),
                    "render_state": dict(S["render_state"]),
                    "material": {"water_body": S["material_spiel"], "baked_sim_material": S["material_spiel"]}},
            "bereich_cm": [r1(box[0] - rand), r1(box[1] - rand), r1(box[2] + rand), r1(box[3] + rand)],
            "rand_steil": rand_steil(P, ss, i0, i1, a_sim, b_sim, k == 0, R),
            "water_info": water_info_bereich(P, ss, i0, i1, R),
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
             "groesse_m": [r1(gro[0], 2), r1(gro[1], 2), r1(gro[2], 2)], "ausdehnung_m": r1(pool.ausdehnung[k], 3), "lage": lage,
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
    # v11 (16g Nachtrag 2): Hindernis-Filter - Lippen-, Rand-, Bettfelsen und zu breite Teile ohne Wasser-Kollision
    F = S.get("hindernis_filter")
    if F and wk:
        Pm = np.asarray(sp["punkte"], float)
        k_von = {pool.ref_text(k): k for k, *_r in kol}
        teile = []
        for e_ in wk:
            key = ref_text_von(e_["ref"])
            k = k_von[key]
            quer, breite, sa, sb, _sm = hindernis_mass(pool.ecken_cm(k), float(pool.cx[k]), float(pool.cy[k]), Pm, ss)
            e_["filter"] = {"rolle": hindernis_rolle(pool.recs[k]["rolle"], F), "quer_im_bett_m": r1(quer, 3),
                            "bett_breite_m": r1(breite, 2), "s_laengs_m": [r1(sa, 3), r1(sb, 3)]}
            teile.append({"key": key, "rolle": e_["filter"]["rolle"], "quer": e_["filter"]["quer_im_bett_m"],
                          "breite": e_["filter"]["bett_breite_m"], "s": e_["filter"]["s_laengs_m"]})
        ent = hindernis_filter_entscheiden(teile, ss, Pm[:, 3] / 100.0, F)
        behalten = []
        for e_ in wk:
            g_ = ent[ref_text_von(e_["ref"])]
            if g_ == "behalten":
                behalten.append(e_)
            else:
                e_["wasser_kollision"] = False
                e_["grund"] = g_
                ohne.append(e_)
        wk = behalten
        ohne.sort(key=lambda e_: ref_text_von(e_["ref"]))
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
        "abstuerze": abst_out, "bereiche": bereiche, "faelle": fl, "schaum_maske": schaum_maske(fl, sp, linie, R),
        "swr_bereiche": kacheln, "toepfe": gw.get("toepfe") or [],
        "wasser_kollision": wk, "ohne_wasser_kollision": ohne,
        "effekte_ohne_fall": sorted({e["_quelle"] + "[%d]" % e["_index"] for e in extra["effekte"]}
                                    - {x["quelle"] + "[%d]" % x["index"] for f in fl for x in f["effekte"]})}
    for k_ in ("quelle_sehens",):
        if gw.get(k_):
            eintrag[k_] = gw[k_]
    eintrag["_tempo_alt_cm_s"] = v_alt
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
# Vorschlaege fuer offene Enden und Luecken (16d, Entscheidung zu Rueckfrage 5 aus 16c): getrennt, nie in der Spline
# ======================================================================================================================
def _rdp(P, tol):
    """Douglas-Peucker (xy, cm) auf einer Punktliste; Anfang/Ende bleiben."""
    P = np.asarray(P, float)
    if len(P) < 3:
        return list(range(len(P)))
    behalten = np.zeros(len(P), bool)
    behalten[0] = behalten[-1] = True
    stapel = [(0, len(P) - 1)]
    while stapel:
        a, b = stapel.pop()
        if b - a < 2:
            continue
        A, B = P[a, :2], P[b, :2]
        AB = B - A
        L = math.hypot(AB[0], AB[1])
        Q = P[a + 1:b, :2]
        if L < 1e-9:
            d = np.hypot(Q[:, 0] - A[0], Q[:, 1] - A[1])
        else:
            d = np.abs(AB[0] * (Q[:, 1] - A[1]) - AB[1] * (Q[:, 0] - A[0])) / L
        k = int(np.argmax(d))
        if d[k] > tol:
            m = a + 1 + k
            behalten[m] = True
            stapel += [(a, m), (m, b)]
    return [i for i in range(len(P)) if behalten[i]]


def _abtasten(P, schritt_cm):
    """Polyline (xy cm) gleichmaessig mit Abstand <= schritt abtasten; Knickpunkte bleiben."""
    out = [list(P[0])]
    for a, b in zip(P[:-1], P[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(math.ceil(L / schritt_cm - 1e-9)))
        for m in range(1, n + 1):
            t = m / n
            out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    return out


class Zielkarte:
    """Wasser als Ziel fuer die Vorschlaege: Gewaesser-Streifen (Spline +- halbe Breite), Seen (ohne Toepfe), Meer."""

    def __init__(self, alle, karte, welt):
        self.welt = welt
        self.karte = karte
        self.gw = []
        for e in alle:
            P = np.asarray(e["water_body"]["spline"]["punkte"], float)
            if len(P) < 2:
                continue
            h = np.maximum(P[:, 3], 400.0) / 2.0
            self.gw.append({"id": e["id"], "art": "fluss" if e["art"] == "fluss" else "bach", "P": P,
                            "ss": np.asarray(e["water_body"]["spline"]["punkte_s_m"], float),
                            "box": ((P[:, 0] - h).min(), (P[:, 1] - h).min(), (P[:, 0] + h).max(), (P[:, 1] + h).max())})
        self.seen = [s for s in karte.seen if not s.get("topf")]

    def raster(self, x0, y0, g_cm, nx, ny, ohne):
        """Zielraster (ny, nx): Spiegel (cm, inf = kein Wasser) und Ziel-Index in self.ziele."""
        tz = np.full((ny, nx), np.inf)
        ti = np.full((ny, nx), -1, np.int64)
        ziele = []
        x1, y1 = x0 + (nx - 1) * g_cm, y0 + (ny - 1) * g_cm

        def zellen(bx):
            j0 = max(int(math.floor((bx[0] - x0) / g_cm)), 0)
            j1 = min(int(math.ceil((bx[2] - x0) / g_cm)), nx - 1)
            i0 = max(int(math.floor((bx[1] - y0) / g_cm)), 0)
            i1 = min(int(math.ceil((bx[3] - y0) / g_cm)), ny - 1)
            return i0, i1, j0, j1

        # Meer (Spiegel 0)
        from sehens_lib import daten as _d
        I, J = np.meshgrid(np.arange(ny), np.arange(nx), indexing="ij")
        X = (x0 + J * g_cm) / 100.0
        Y = (y0 + I * g_cm) / 100.0
        fi, fj = _d.m_zu_pixel(X, Y, self.welt.zelle_m)
        ii = np.clip(np.floor(fi + 0.5).astype(np.int64), 0, self.welt.ny - 1)
        jj = np.clip(np.floor(fj + 0.5).astype(np.int64), 0, self.welt.nx - 1)
        m = np.asarray(self.welt.meer)[ii, jj]
        if m.any():
            ziele.append({"art": "meer", "id": "meer"})
            tz[m] = 0.0
            ti[m] = len(ziele) - 1
        # Seen
        for s in self.seen:
            b = s["box"]
            if b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1:
                continue
            i0, i1, j0, j1 = zellen(b)
            if i0 > i1 or j0 > j1:
                continue
            Ii, Jj = np.meshgrid(np.arange(i0, i1 + 1), np.arange(j0, j1 + 1), indexing="ij")
            px, py = x0 + Jj * g_cm, y0 + Ii * g_cm
            U = s["umriss"]
            xa, ya = U[:, 0], U[:, 1]
            xb, yb = np.roll(xa, -1), np.roll(ya, -1)
            innen = np.zeros(px.shape, bool)
            for k in range(len(U)):
                c = ((ya[k] > py) != (yb[k] > py))
                with np.errstate(divide="ignore", invalid="ignore"):
                    xs = (xb[k] - xa[k]) * (py - ya[k]) / (yb[k] - ya[k]) + xa[k]
                innen ^= c & (px < xs)
            sel = innen & (s["spiegel_cm"] < tz[i0:i1 + 1, j0:j1 + 1])
            if sel.any():
                ziele.append({"art": "see", "id": s["id"]})
                tz[i0:i1 + 1, j0:j1 + 1][sel] = s["spiegel_cm"]
                ti[i0:i1 + 1, j0:j1 + 1][sel] = len(ziele) - 1
        # Gewaesser-Streifen
        for q in self.gw:
            if q["id"] in ohne:
                continue
            b = q["box"]
            if b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1:
                continue
            P = q["P"]
            k_ = None
            hs = np.maximum(np.maximum(P[:-1, 3], P[1:, 3]), 400.0) / 2.0
            lox, hix = np.minimum(P[:-1, 0], P[1:, 0]) - hs, np.maximum(P[:-1, 0], P[1:, 0]) + hs
            loy, hiy = np.minimum(P[:-1, 1], P[1:, 1]) - hs, np.maximum(P[:-1, 1], P[1:, 1]) + hs
            for k in np.where((hix >= x0) & (lox <= x1) & (hiy >= y0) & (loy <= y1))[0]:
                A, B = P[k], P[k + 1]
                bx = (lox[k], loy[k], hix[k], hiy[k])
                i0, i1, j0, j1 = zellen(bx)
                if i0 > i1 or j0 > j1:
                    continue
                Ii, Jj = np.meshgrid(np.arange(i0, i1 + 1), np.arange(j0, j1 + 1), indexing="ij")
                px, py = x0 + Jj * g_cm, y0 + Ii * g_cm
                ab = B[:2] - A[:2]
                t = np.clip(((px - A[0]) * ab[0] + (py - A[1]) * ab[1]) / max(ab[0] ** 2 + ab[1] ** 2, 1e-9), 0, 1)
                d = np.hypot(px - (A[0] + t * ab[0]), py - (A[1] + t * ab[1]))
                hb = np.maximum(A[3] + t * (B[3] - A[3]), 400.0) / 2.0
                z = A[2] + t * (B[2] - A[2])
                sel = (d <= hb) & (z < tz[i0:i1 + 1, j0:j1 + 1])
                if sel.any():
                    if k_ is None:
                        ziele.append({"art": q["art"], "id": q["id"], "P": P, "ss": q["ss"]})
                        k_ = len(ziele) - 1
                    tz[i0:i1 + 1, j0:j1 + 1][sel] = z[sel]
                    ti[i0:i1 + 1, j0:j1 + 1][sel] = k_
        return tz, ti, ziele


def vorschlag_luecke(e, mu, zk, gel, V):
    """Luecke (Ziel bekannt): gerade Verlaengerung vom Spline-Ende bis ins_wasser_m hinter den Wasserrand des Ziels."""
    P = e["water_body"]["spline"]["punkte"]
    ex, ey = P[-1][0], P[-1][1]
    ins = V["ins_wasser_m"] * 100.0
    if mu["art"] in ("fluss", "bach"):
        q = next((x for x in zk.gw if x["id"] == mu.get("ziel")), None)
        if q is None:
            return None
        Q = q["P"]
        A, B = Q[:-1], Q[1:]
        ab = B[:, :2] - A[:, :2]
        t = np.clip(((ex - A[:, 0]) * ab[:, 0] + (ey - A[:, 1]) * ab[:, 1]) / np.maximum((ab ** 2).sum(1), 1e-9), 0, 1)
        cx, cy = A[:, 0] + t * ab[:, 0], A[:, 1] + t * ab[:, 1]
        d = np.hypot(ex - cx, ey - cy)
        k = int(np.argmin(d))
        halb = float(A[k, 3] + t[k] * (B[k, 3] - A[k, 3])) / 2.0
        zt = float(A[k, 2] + t[k] * (B[k, 2] - A[k, 2]))
        ux, uy = (cx[k] - ex) / max(d[k], 1e-9), (cy[k] - ey) / max(d[k], 1e-9)
        L = min(max(float(d[k]) - halb + ins, 50.0), float(d[k]))
        ziel = {"art": q["art"], "id": q["id"], "spiegel_cm": r1(zt),
                "s_m": r1(float(q["ss"][k] + t[k] * (q["ss"][k + 1] - q["ss"][k])), 2)}
    else:
        s = next((x for x in zk.karte.seen if x["id"] == mu.get("ziel")), None)
        if s is None:
            return None
        U = s["umriss"]
        A, B = U, np.roll(U, -1, axis=0)
        ab = B - A
        t = np.clip(((ex - A[:, 0]) * ab[:, 0] + (ey - A[:, 1]) * ab[:, 1]) / np.maximum((ab ** 2).sum(1), 1e-9), 0, 1)
        cx, cy = A[:, 0] + t * ab[:, 0], A[:, 1] + t * ab[:, 1]
        d = np.hypot(ex - cx, ey - cy)
        k = int(np.argmin(d))
        ux, uy = (cx[k] - ex) / max(d[k], 1e-9), (cy[k] - ey) / max(d[k], 1e-9)
        L = float(d[k]) + ins
        zt = float(s["spiegel_cm"])
        ziel = {"art": "see", "id": s["id"], "spiegel_cm": r1(zt)}
    pts = _abtasten([[ex, ey], [ex + ux * L, ey + uy * L]], V["punkt_abstand_m"] * 100.0)
    return _vorschlag_fertig(e, pts, ziel, zt, gel, V, "luecke",
                             "Luecke %.1f m: gerade Verlaengerung vom Spline-Ende %.1f m bis %.1f m hinter den Wasserrand von %s"
                             % (mu.get("luecke_m") or 0.0, L / 100.0, V["ins_wasser_m"], ziel["id"]), [])


def _vorschlag_fertig(e, pts, ziel, zt, gel, V, art, begruendung, kreuzt, extra=None):
    P = e["water_body"]["spline"]["punkte"]
    ez, br, tf, vel = P[-1][2], P[-1][3], P[-1][4], P[-1][5]
    pts = np.asarray(pts, float)
    h = gel.hoehe_cm(pts[:, 0], pts[:, 1])
    z = [float(ez)]
    for i in range(1, len(pts)):
        z.append(min(z[-1], float(h[i])))
    if zt is not None and len(z) > 1:
        z[-1] = min(z[-2], zt)
    z = np.minimum.accumulate(np.asarray(z))
    if zt is not None:
        # nie unter den Spiegel des Ziels (z. B. Meeresboden unter 0 m vor dem Ziel)
        z = np.maximum(z, min(float(zt), float(ez)))
    ein = float(np.max(h[1:] - z[1:])) / 100.0 if len(z) > 1 else 0.0
    L = float(np.hypot(*np.diff(pts[:, :2], axis=0).T).sum()) / 100.0
    v = {"art": art, "methode": (extra or {}).get("methode", "gerade"), "ziel": ziel,
         "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
         "punkte": [[r1(p[0]), r1(p[1]), r1(zz), br, tf, vel] for p, zz in zip(pts, z)],
         "laenge_m": r1(L, 2), "dz_m": r1((float(ez) - float(z[-1])) / 100.0, 2),
         "einschnitt_max_m": r1(max(ein, 0.0), 2), "gelaende_max_ueber_ende_m": r1((float(h.max()) - float(ez)) / 100.0, 2),
         "kreuzt": kreuzt, "begruendung": begruendung,
         "hinweis": "Vorschlag, nicht in der Spline: lokal pruefen und uebernehmen (Spline verlaengern bzw. Weltdaten nachziehen)"}
    if ziel and zt is not None and zt > float(ez) + 1.0:
        v["ziel_hoeher_cm"] = r1(zt - float(ez))
    if extra:
        v.update({k: w for k, w in extra.items() if k != "methode"})
    return v


def vorschlag_offen(e, zk, gel, V, ohne):
    """Offenes Ende: steilstes Gefaelle (D8 auf dem Suchraster), aus einer Senke weiter mit dem Weg des geringsten
    Anstiegs (Dijkstra, Kosten = Laenge + anstieg_kosten x Anstieg) bis zur ersten Wasserzelle (Gewaesser, See, Meer), deren
    Spiegel hoechstens dz_toleranz_cm ueber dem Ende liegt."""
    import heapq
    P = e["water_body"]["spline"]["punkte"]
    ex, ey, ez = P[-1][0], P[-1][1], P[-1][2]
    g = V["raster_m"] * 100.0
    R = V["radius_m"] * 100.0
    n = int(round(R / g))
    nx = ny = 2 * n + 1
    x0, y0 = ex - n * g, ey - n * g
    I, J = np.meshgrid(np.arange(ny), np.arange(nx), indexing="ij")
    H = gel.hoehe_cm(x0 + J * g, y0 + I * g)
    tz, ti, ziele = zk.raster(x0, y0, g, nx, ny, ohne)
    ok = tz <= ez + V["dz_toleranz_cm"]
    nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    i, j = n, n
    weg = [(i, j)]
    abstieg, abstieg_m = 0, 0.0
    while not ok[i, j] and len(weg) < 4 * n:
        best = None
        for di, dj in nb:
            a, b = i + di, j + dj
            if not (0 <= a < ny and 0 <= b < nx):
                continue
            gef = (H[i, j] - H[a, b]) / math.hypot(di, dj)
            if gef > 1e-6 and (best is None or gef > best[0]):
                best = (gef, a, b)
        if best is None:
            break
        abstieg_m += math.hypot(best[1] - i, best[2] - j) * V["raster_m"]
        i, j = best[1], best[2]
        weg.append((i, j))
        abstieg += 1
    methode = "steilstes_gefaelle"
    if not ok[i, j]:
        methode = "steilstes_gefaelle+geringster_anstieg" if abstieg else "geringster_anstieg"
        K = V["anstieg_kosten"]
        start = i * nx + j
        dist = {start: 0.0}
        vor = {}
        heap = [(0.0, start)]
        ziel_k = None
        fertig = set()
        while heap:
            c, k = heapq.heappop(heap)
            if k in fertig:
                continue
            fertig.add(k)
            a, b = divmod(k, nx)
            if ok[a, b]:
                ziel_k = k
                break
            for di, dj in nb:
                a2, b2 = a + di, b + dj
                if not (0 <= a2 < ny and 0 <= b2 < nx):
                    continue
                k2 = a2 * nx + b2
                if k2 in fertig:
                    continue
                c2 = c + math.hypot(di, dj) * V["raster_m"] + K * max(0.0, float(H[a2, b2] - H[a, b])) / 100.0
                if c2 < dist.get(k2, float("inf")) - 1e-12:
                    dist[k2] = c2
                    vor[k2] = k
                    heapq.heappush(heap, (c2, k2))
        if ziel_k is None:
            pts = [[ex, ey]] + [[x0 + b * g, y0 + a * g] for a, b in weg[1:]]
            if len(pts) < 2:
                return None
            return _vorschlag_fertig(e, pts, None, None, gel, V, "offen",
                                     "kein Wasser mit Spiegel <= Ende + %.1f m im Umkreis %.0f m: nur steilstes Gefaelle bis zur "
                                     "Senke (versickert)" % (V["dz_toleranz_cm"] / 100.0, V["radius_m"]), [],
                                     {"methode": "steilstes_gefaelle", "ziel_gefunden": False})
        teil = []
        k = ziel_k
        while k != start:
            teil.append(divmod(k, nx))
            k = vor[k]
        weg += teil[::-1]
    if len(weg) < 2:
        return None
    a, b = weg[-1]
    zd = ziele[int(ti[a, b])]
    zt = float(tz[a, b])
    ziel = {"art": zd["art"], "id": zd["id"], "spiegel_cm": r1(zt)}
    if "P" in zd:
        Q = zd["P"]
        px, py = x0 + b * g, y0 + a * g
        A_, B_ = Q[:-1], Q[1:]
        ab = B_[:, :2] - A_[:, :2]
        t = np.clip(((px - A_[:, 0]) * ab[:, 0] + (py - A_[:, 1]) * ab[:, 1]) / np.maximum((ab ** 2).sum(1), 1e-9), 0, 1)
        d = np.hypot(px - (A_[:, 0] + t * ab[:, 0]), py - (A_[:, 1] + t * ab[:, 1]))
        kk = int(np.argmin(d))
        ziel["s_m"] = r1(float(zd["ss"][kk] + t[kk] * (zd["ss"][kk + 1] - zd["ss"][kk])), 2)
    # Wasser mit hoeherem Spiegel, durch das der Weg fuehrt
    kreuzt = sorted({ziele[int(ti[a_, b_])]["id"] for a_, b_ in weg[1:-1] if ti[a_, b_] >= 0})
    roh = [[ex, ey]] + [[x0 + b_ * g, y0 + a_ * g] for a_, b_ in weg[1:]]
    keep = _rdp(roh, V["vereinfachen_m"] * 100.0)
    pts = _abtasten([roh[k] for k in keep], V["punkt_abstand_m"] * 100.0)
    txt = "offen: Verlaengerung entlang des steilsten Gefaelles (D8, %.0f-m-Raster)" % V["raster_m"]
    if abstieg:
        txt += " %.0f m" % abstieg_m
    if methode != "steilstes_gefaelle":
        txt += ", aus der Senke weiter auf dem Weg des geringsten Anstiegs" if abstieg else \
            " nicht moeglich (Ende in einer Senke): Weg des geringsten Anstiegs"
    txt += " bis %s (Spiegel %.1f m, Ende %.1f m)" % (ziel["id"] if ziel["id"] == ziel["art"] else "%s %s" % (ziel["art"], ziel["id"]),
                                                    zt / 100.0, ez / 100.0)
    if kreuzt:
        txt += "; kreuzt Wasser mit hoeherem Spiegel: %s" % ", ".join(kreuzt)
    return _vorschlag_fertig(e, pts, ziel, zt, gel, V, "offen", txt, kreuzt,
                             {"methode": methode, "ziel_gefunden": True, "abstieg_m": r1(abstieg_m, 1)})


def vorschlaege_bilden(alle, karte, welt, gel, regeln, log_=log):
    """Je offenem Ende und je Luecke ein Vorschlag (Feld muendung.vorschlag + vorschlaege.json). Die Spline bleibt."""
    V = regeln["gewaesser"]["vorschlag"]
    zk = Zielkarte(alle, karte, welt)
    nach_id = {e["id"]: e for e in alle}
    oben = {}
    for e in alle:
        z = e["muendung"].get("ziel")
        if e["muendung"]["art"] in ("fluss", "bach") and z in nach_id:
            oben.setdefault(z, []).append(e["id"])

    def endet_offen(gid):
        """Muendungskette endet offen (bzw. im Kreis): als Ziel ungeeignet, sonst entstehen Vorschlaege in Sackgassen."""
        seen = set()
        while gid in nach_id and gid not in seen:
            seen.add(gid)
            m = nach_id[gid]["muendung"]
            if m["art"] == "offen":
                return True
            if m["art"] not in ("fluss", "bach"):
                return False
            gid = m.get("ziel")
        return gid in seen
    sackgasse = {e["id"] for e in alle if endet_offen(e["id"])}

    def zufluss_baum(gid):
        out, st = {gid}, [gid]
        while st:
            for u in oben.get(st.pop(), []):
                if u not in out:
                    out.add(u)
                    st.append(u)
        return out
    out = []
    for e in sorted(alle, key=lambda e_: e_["id"]):
        mu = e["muendung"]
        if mu["art"] == "offen":
            v = vorschlag_offen(e, zk, gel, V, zufluss_baum(e["id"]) | sackgasse)
        elif mu.get("luecke_m"):
            v = vorschlag_luecke(e, mu, zk, gel, V)
        else:
            continue
        if v is None:
            continue
        mu["vorschlag"] = v
        out.append({"gewaesser": e["id"], "muendung_art": mu["art"], "luecke_m": mu.get("luecke_m"), "vorschlag": v})
    log_("Vorschlaege: %d (offen %d, Luecke %d)" % (len(out), sum(1 for o in out if o["vorschlag"]["art"] == "offen"),
                                                   sum(1 for o in out if o["vorschlag"]["art"] == "luecke")))
    return out


# ======================================================================================================================
# Hauptlauf
# ======================================================================================================================
def toepfe_max(regeln):
    return float((regeln["gewaesser"].get("topf") or {}).get("max_ausdehnung_m", 0.0))


def toepfe_bilden(sehens_seen, sehens_teile, regeln):
    """Kleine Sehens-Seen (groesste Ausdehnung < topf.max_ausdehnung_m), in die ein Sehens-Bach muendet oder aus denen
    einer abfliesst, werden Toepfe des Gewaessers (16d, Entscheidung zu Rueckfrage 4 aus 16c): kein eigener WaterBodyLake,
    die SWR des Gewaessers fuellt sie. Zulauf -> Topf -> Abfluss wird ein Gewaesser. Rueckgabe (toepfe, nach, vor)."""
    TP = regeln["gewaesser"].get("topf") or {}
    mx = toepfe_max(regeln)
    rand = float(TP.get("rand_m", 1.0)) * 100.0
    for s in sehens_seen:
        U = s["umriss"]
        s["ausdehnung_m"] = r1(float(np.hypot(U[:, None, 0] - U[None, :, 0], U[:, None, 1] - U[None, :, 1]).max()) / 100.0, 2) \
            if len(U) > 1 else 0.0
    zu, ab = {}, {}
    for t in sehens_teile:
        sh = t.sehens
        if sh.get("muendung_art") == "see_eigen" and sh.get("muendung"):
            zu.setdefault("%s/%s" % (sh["ort"], sh["muendung"]), []).append(t)
        if sh.get("abfluss_von"):
            ab.setdefault("%s/%s" % (sh["ort"], sh["abfluss_von"]), []).append(t)
    toepfe, nach, vor = {}, {}, {}
    for s in sorted(sehens_seen, key=lambda s_: s_["id"]):
        sid = s["id"]
        if not (s["ausdehnung_m"] < mx and (sid in zu or sid in ab)):
            continue
        U = s["umriss"]
        bx = [float(U[:, 0].min()), float(U[:, 1].min()), float(U[:, 0].max()), float(U[:, 1].max())]
        z_ = sorted(zu.get(sid, []), key=lambda t: (-(t.s1 - t.s0), t.id))
        a_ = sorted(ab.get(sid, []), key=lambda t: t.id)
        tp = {"see": sid, "ausdehnung_m": s["ausdehnung_m"], "spiegel_cm": float(s["spiegel_cm"]),
              "tiefe_cm": max(float(s.get("tiefe_m") or 0.0) * 100.0, regeln["abschnitt"]["tiefe_min_cm"]),
              "mitte_cm": [0.5 * (bx[0] + bx[2]), 0.5 * (bx[1] + bx[3])],
              "breite_cm": max(bx[2] - bx[0], bx[3] - bx[1]) + 2.0 * rand, "rechteck_cm": bx,
              "zulauf": z_[0].id if z_ else None, "abfluss": a_[0].id if a_ else None,
              "weitere_zulaeufe": [t.id for t in z_[1:]], "weitere_abfluesse": [t.id for t in a_[1:]],
              "art": "durchfluss" if (z_ and a_) else ("quelltopf" if a_ else "endtopf"), "gewaesser": None}
        toepfe[sid] = tp
        s["topf"] = True
        if z_ and a_:
            nach[z_[0].id] = (a_[0].id, {"art": "topf", "topf": tp, "abstand_m": 0.0})
            vor[a_[0].id] = z_[0].id
    return toepfe, nach, vor


def finde_sw(sehens_basis, sw_ordner, biom):
    for c in ([os.path.join(sw_ordner, "sw_" + biom)] if sw_ordner else []) + \
             [os.path.join(sehens_basis, biom, "sw_" + biom), os.path.join(sehens_basis, "..", "sw_" + biom)]:
        if os.path.isdir(c):
            return c
    return None


def gewaesser_bilden(welt, gef, sehens, regeln, log_=log, gef_plaene=None):
    """Alle Laeufe laden, verketten, Muendungen bestimmen. Rueckgabe (gewaesser, teile, karte, info)."""
    import gefaelle_daten as gd
    G = regeln["gewaesser"]
    ww = welt.wasser_welt or {}
    teile_welt = []
    E = ersetzte_laeufe()                     # 16h: lokal ersetzte Laeufe (C2 -> Erlenbach p2) gehoeren in kein Gewaesser
    anschluesse = ersatz_anschluesse()        # 16h Nachtrag 3: Kopf des Ziel-Laufs bis zum Ersatz-Spiegel kuerzen
    ersetzt_linien = []
    for f in sorted(ww.get("fluesse", []) or [], key=lambda f: f["id"]):
        if f["id"] in E:
            ersetzt_linien.append((f["id"], np.asarray(f["punkte"], float)))
            continue
        teile_welt.append(("fluss", f["id"], f.get("fluss"), None, f.get("feld"), None))
    for b in sorted(welt.baeche or [], key=lambda b: b["id"]):
        if b["id"] in E:
            ersetzt_linien.append((b["id"], np.asarray(b["punkte"], float)))
            continue
        teile_welt.append(("bach", b["id"], None, b.get("netz"), b.get("feld"), b.get("anschluss")))
    teile = []
    for art, tid, fam, netz, feld, ans in teile_welt:
        if gef_plaene is None:
            pf = os.path.join(gef, tid, "plan.json") if gef else None
            hat_plan = bool(pf and os.path.exists(pf))
        else:
            hat_plan = tid in gef_plaene
        r = gefaelle_gewaesser(gef, tid, regeln) if hat_plan else None
        if r:
            g, linie, abst, extra = r
            her = "plan"
        else:
            lauf = gd.Lauf.aus_welt(welt, tid)
            g, linie, abst, extra = roh_gewaesser(lauf, regeln, art)
            her = "roh"
        if tid in anschluesse:
            kp = kopf_kuerzen(linie, anschluesse[tid], her)
            if kp:
                extra["kopf"] = kp
        teile.append(Teil(tid, art, her, g, linie, abst, extra, familie=fam, netz=netz, feld=feld, anschluss=ans))
    teil_ort = {t.id: t for t in teile}
    # Sehens-Baeche und -Seen
    sehens_teile, sehens_seen = [], []
    for biom, ort, rel in sehens:
        for w in ort.get("wasser") or []:
            if w.get("typ") == "see" and w.get("umriss_cm"):
                sehens_seen.append({"id": "%s/%s" % (ort["id"], w["id"]), "quelle": "sehens/%s/orte.json" % biom,
                                    "umriss": np.asarray(w["umriss_cm"], float)[:, :2], "spiegel_cm": float(w.get("spiegel_cm") or 0.0),
                                    "tiefe_m": w.get("tiefe_m")})
        for g, linie, abst, extra in sehens_gewaesser(biom, ort, regeln):
            w = next(x for x in ort["wasser"] if x.get("typ") == "bach" and x.get("id") == g["bach"])
            sh = {"ort": ort["id"], "biom": biom, "bach": w.get("id"), "muendung": w.get("muendung"),
                  "muendung_art": w.get("muendung_art"), "abfluss_von": w.get("abfluss_von"), "rel": rel}
            sehens_teile.append(Teil(g["id"], "sehens_bach", "sehens", g, linie, abst, extra, sehens=sh))
    toepfe, s_nach, s_vor = toepfe_bilden(sehens_seen, sehens_teile, regeln)
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
    # Sehens-Baeche: Ketten ueber kleine Toepfe (16d, Rueckfrage 4 aus 16c): Zulauf -> Topf -> Abfluss = ein Gewaesser
    s_ort = {t.id: t for t in sehens_teile}
    for t in sehens_teile:
        if t.id in s_vor:
            continue
        k, links = [t], []
        while k[-1].id in s_nach:
            nid, f = s_nach[k[-1].id]
            if any(x.id == nid for x in k):
                break
            k.append(s_ort[nid])
            links.append(f)
        ketten.append((k, links))
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
        if kat == "welt" and ersetzt_linien:
            ob = ersetzt_nachbar(k[0].linie, 0, ersetzt_linien, G)
            if ob:
                an["ersetzter_oberlauf"] = ersetzt_eintrag(ob, E, "Anfang liegt am ersetzten Lauf; das Wasser kommt "
                                                                  "lokal aus dem Ersatz (Zufluss, nicht in diesem Export)")
            if mu.get("art") == "offen":
                ub = ersetzt_nachbar(k[-1].linie, -1, ersetzt_linien, G)
                if ub:
                    mu["ersetzter_lauf"] = ersetzt_eintrag(ub, E, "muendete in einen ersetzten Lauf; lokal Anschluss an "
                                                                  "den Ersatz pruefen")
        topf_oben = topf_unten = None
        if kat == "sehens":
            sh0, sh1 = k[0].sehens, k[-1].sehens
            sid0 = "%s/%s" % (sh0["ort"], sh0.get("abfluss_von")) if sh0.get("abfluss_von") else None
            if sid0 in toepfe and toepfe[sid0]["zulauf"] is None and toepfe[sid0]["abfluss"] == k[0].id:
                topf_oben = toepfe[sid0]
            sid1 = "%s/%s" % (sh1["ort"], sh1.get("muendung")) if sh1.get("muendung_art") == "see_eigen" else None
            if sid1 in toepfe and toepfe[sid1]["abfluss"] is None and toepfe[sid1]["zulauf"] == k[-1].id:
                topf_unten = toepfe[sid1]
        linie, abst, extra, laeufe = zusammenfuegen(k, links, regeln, topf_oben=topf_oben, topf_unten=topf_unten)
        kp = k[0].extra.get("kopf") if kat == "welt" else None
        if kp:
            an = dict(an, punkt_cm=[r1(linie.x[0]), r1(linie.y[0]), r1(linie.z[0])], kopf_gekuerzt=kp)
        for tp in extra.get("toepfe") or []:
            toepfe[tp["see"]]["gewaesser"] = gid
        if topf_unten is not None:
            mu = {"art": "topf", "ziel": topf_unten["see"], "gewaesser": gid, "spiegel_ziel_cm": r1(topf_unten["spiegel_cm"]),
                  "punkt_cm": [r1(linie.x[-1]), r1(linie.y[-1]), r1(linie.z[-1])], "quelle": "sehens",
                  "hinweis": "endet in seinem Topf (< %.0f m, Teil des Gewaessers, kein WaterBodyLake)" % toepfe_max(regeln)}
        if topf_oben is not None:
            an = {"art": "topf", "ziel": topf_oben["see"], "gewaesser": gid, "quelle": "sehens",
                  "punkt_cm": [r1(linie.x[0]), r1(linie.y[0]), r1(linie.z[0])],
                  "hinweis": "beginnt in seinem Topf (< %.0f m, Teil des Gewaessers, kein WaterBodyLake)" % toepfe_max(regeln)}
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
              "muendung": mu, "anfang": an, "roh_bei": roh_bei, "typ_bei": typ_bei, "teile": k,
              "toepfe": extra.get("toepfe") or []}
        if kat == "sehens":
            sh = k[0].sehens
            gw["quelle_sehens"] = {"biom": sh["biom"], "ort": sh["ort"], "bach": sh["bach"]}
            gw["rel"] = sh["rel"]
        else:
            gw["rel"] = os.path.join("gewaesser", gid, "fluss_sim.json")
        gewaesser.append(gw)
    # Anfang/Muendung an einem Topf, der zu einem (anderen) Gewaesser gehoert: kein See mehr, sondern dessen Topf
    for gw in gewaesser:
        for key in ("anfang", "muendung"):
            m = gw[key]
            if m.get("art") == "see" and m.get("ziel") in toepfe and toepfe[m["ziel"]].get("gewaesser"):
                if toepfe[m["ziel"]]["gewaesser"] == gw["id"]:
                    # nur geometrisch neben dem eigenen Topf (z. B. kurzer Zulauf der Elfentreppe): Quelle
                    gw[key] = {"art": "quelle", "punkt_cm": m["punkt_cm"],
                               "hinweis": "beginnt neben dem eigenen Topf %s" % m["ziel"]}
                    continue
                m["art"] = "topf"
                m["gewaesser"] = toepfe[m["ziel"]]["gewaesser"]
                m["hinweis"] = "Topf gehoert zu %s (kein WaterBodyLake)" % m["gewaesser"]
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
    info = {"toepfe": toepfe, "sehens_seen": sehens_seen,
            "ersetzt": {lid: {"ersetzt_durch": E[lid].get("ersetzt_durch"), "art": E[lid].get("art"),
                              "feld": E[lid].get("feld"), "im_export": False} for lid, _ in ersetzt_linien},
            "teile_welt": len(teile), "teile_plan": sum(1 for t in teile if t.herkunft == "plan"),
            "teile_roh": sum(1 for t in teile if t.herkunft == "roh"), "sehens_baeche": len(sehens_teile),
            "fortsetzungen": {a_: sum(1 for _, (n_, f) in nach.items() if f["art"] == a_) for a_ in ("anschluss", "ueberlappung")}}
    return gewaesser, teile, karte, info


def ersatz_anschluesse():
    """16h Nachtrag 3: {ziel_lauf: eintrag} aus ersetzt.json -> ersatz.<ID>.muendung_anschluss (Ziel-Lauf, p2-Spiegel).
    Der Kopf des Ziel-Laufs oberhalb des Ersatz-Spiegels ist ein Rest des ersetzten Laufs (alte Feld-Ueberlappung)."""
    import gefaelle_daten as gd
    out = {}
    for eid, e in sorted((gd.ersetzt_daten().get("ersatz") or {}).items()):
        m = e.get("muendung_anschluss") or {}
        if m.get("ziel_lauf") and m.get("p2_spiegel_m") is not None and m.get("aktiv", True):
            out[m["ziel_lauf"]] = dict(m, ersatz=eid)
    return out


def kopf_kuerzen(linie, m, herkunft):
    """Erster Punkt der Linie mit Spiegel <= Ersatz-Spiegel + toleranz (linear zwischen Splinepunkten). Rueckgabe dict
    {s_m, spiegel_cm, kopf_spiegel_cm, ersatz, ziel_lauf} oder None (Lauf mit Plan: nicht kuerzen, Stufen gehoeren dem Plan)."""
    if herkunft != "roh":
        return None
    grenze = float(m["p2_spiegel_m"]) * 100.0 + float(m.get("toleranz_cm", 2.0))
    z, s_ = linie.z, linie.s
    if z[0] <= grenze:
        return None
    k = int(np.argmax(z <= grenze)) if (z <= grenze).any() else None
    if k is None or k == 0:
        return None
    t = (z[k - 1] - grenze) / max(z[k - 1] - z[k], 1e-9)
    sc = float(s_[k - 1] + t * (s_[k] - s_[k - 1]))
    return {"s_m": r1(sc, 2), "spiegel_cm": r1(grenze), "kopf_spiegel_cm": r1(z[0]), "ersatz": m["ersatz"],
            "ziel_lauf": m["ziel_lauf"], "regel": "16h Nachtrag 3: Kopf = Rest des ersetzten Laufs, Anschluss bei passendem Spiegel"}


def ersetzt_nachbar(L, i, linien, G):
    """16h: Ersetzte Laeufe, deren Linie <= halbe Breite + fortsetzung_abstand_m am Punkt i (0 = Anfang, -1 = Ende) der
    Linie L liegt. Rueckgabe [(lauf_id, abstand_m)] sortiert."""
    x, y = float(L.x[i]), float(L.y[i])
    r_m = float(L.b[i]) / 200.0 + float(G["fortsetzung_abstand_m"])
    out = []
    for lid, P in linien:
        d = projektion_schnell_cm(P, x, y)
        hb = float(np.max(P[:, 3])) / 200.0 if P.shape[1] > 3 else 0.0
        if d / 100.0 <= r_m + hb:
            out.append((lid, round(d / 100.0, 2)))
    return sorted(out, key=lambda t_: (t_[1], t_[0]))


def projektion_schnell_cm(P, x, y):
    """Kleinster Abstand (cm) eines Punkts zur Polylinie P (N x >= 2, cm)."""
    a, b = P[:-1, :2], P[1:, :2]
    ab = b - a
    t = np.clip(((x - a[:, 0]) * ab[:, 0] + (y - a[:, 1]) * ab[:, 1]) / np.maximum((ab ** 2).sum(1), 1e-9), 0.0, 1.0)
    return float(np.min(np.hypot(x - (a[:, 0] + t * ab[:, 0]), y - (a[:, 1] + t * ab[:, 1]))))


def ersetzt_eintrag(nachbarn, E, hinweis):
    return {"laeufe": [lid for lid, _ in nachbarn], "abstand_m": [d for _, d in nachbarn],
            "ersetzt_durch": sorted({E[lid].get("ersetzt_durch") for lid, _ in nachbarn}), "hinweis": hinweis}


def hindernis_komponenten(komp, grenzen=None):
    """Komponenten eines Hindernis-Akteurs WH_<kachel>: je Netz eine HISM-Komponente (16a d2), sortiert nach Netz. Hat ein
    Netz mehr als grenzen.instanzen_je_komponente_max Instanzen, wird es auf weitere Komponenten desselben Netzes geteilt
    (Felder teil/teile; 16c Nachtrag 4). komp: {netz: [Instanz, ...]} in fester Reihenfolge."""
    nmax = int((grenzen or {}).get("instanzen_je_komponente_max") or 0)
    out = []
    for pf in sorted(komp):
        lst = komp[pf]
        teile = [lst] if nmax <= 0 or len(lst) <= nmax else [lst[i:i + nmax] for i in range(0, len(lst), nmax)]
        for k, t in enumerate(teile):
            c = {"netz": pf, "klasse": "HISM", "nanite": None, "kollision": "wie_quelle", "instanzen": t}
            if len(teile) > 1:
                c["teil"] = k + 1
                c["teile"] = len(teile)
            out.append(c)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Exporter Entscheidung 16 (v3, 16c): fluss_sim.json je Gewaesser + back_liste.json")
    ap.add_argument("--gefaelle", default=None, help="Ordner mit <lauf>/plan.json (gefaelle_plan.py)")
    ap.add_argument("--sehens", default=None, help="Ordner mit <biom>/orte.json (Sehens-Planer)")
    ap.add_argument("--sw-ordner", default=None, help="Ordner mit sw_<biom>/ (Standard: <sehens>/<biom>/sw_<biom>)")
    ap.add_argument("--roh", default=None,
                    help="16c Nachtrag 3: Ordner der Roh-Lauf-Ebene (gefaelle/bachbett_roh.py, <lauf>/instanzen/<Feld>/); "
                         "Standard: bachbett_roh neben --gefaelle")
    ap.add_argument("--aus", required=True)
    ap.add_argument("--regeln", default=REGELN_STANDARD)
    ap.add_argument("--nur", nargs="+", default=None)
    ap.add_argument("--gebaut", nargs="+", default=None, metavar="LAUF",
                    help="schon gebaute Laeufe (Gelaende-Delta lokal bereits eingestempelt): Gefaelle-Lauf-IDs, Sehens-Ort-IDs "
                         "oder SW_<ort>_<bach>; ihre Deltas werden nicht addiert (16d)")
    ap.add_argument("--einbau", default=None,
                    help="Ordner sehens_einbau/ (A15_<lauf>/lauf.json, 'nachgezogen'); Standard: <daten1m>/sehens_einbau bzw. "
                         "neben --gefaelle")
    ap.add_argument("--ohne-erkennung", action="store_true", help="lauf.json nicht auswerten (nur --gebaut)")
    from sehens_lib import daten
    daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    regeln = lese_json(a.regeln)
    welt = daten.lade(a.daten2m or (None if a.daten1m else os.path.join(RECHERCHE, "vorlagen", "daten", "sehens")),
                      a.daten1m, pfade=False)
    masse = Masse()
    pool = Pool(regeln, masse)
    gel = Gelaende(welt)
    gef_ok = os.path.isdir(a.gefaelle) if a.gefaelle else False
    gef_plaene, eingabe_weg = lauf_plaene(a.gefaelle if gef_ok else None)
    eingabe_weg = [dict(w, eingabe="gefaelle") for w in eingabe_weg]
    for lauf in sorted(gef_plaene):
        fp_, weg_ = feld_plaene(os.path.join(a.gefaelle, lauf, "instanzen"))
        eingabe_weg += [dict(w, eingabe="gefaelle/%s/instanzen" % lauf) for w in weg_]
        for feld_plan in fp_:
            feld = os.path.basename(os.path.dirname(feld_plan))
            pool.lade_ebene(feld_plan, "gefaelle/%s/instanzen/%s/plan.json" % (lauf, feld))
    roh_basis = roh_ordner_finden(a.roh, a.gefaelle if gef_ok else None)
    roh_liste, weg_ = roh_ebenen(roh_basis)
    eingabe_weg += [dict(w, eingabe="bachbett_roh") for w in weg_]
    for feld_plan, ref in roh_liste:
        pool.lade_ebene(feld_plan, ref)
    if a.roh and not roh_basis:
        log("WARNUNG: --roh %s nicht gefunden - Roh-Lauf-Ebene (Totholz/Felsen) nicht gelesen" % a.roh)
    sehens = []
    sehens_ok = bool(a.sehens and os.path.isdir(a.sehens))
    if sehens_ok:
        for biom in BIOME:
            po = os.path.join(a.sehens, biom, "orte.json")
            if not os.path.exists(po):
                continue
            od = lese_json(po)
            sw = finde_sw(a.sehens, a.sw_ordner, biom)
            if sw:
                fp_, weg_ = feld_plaene(sw)
                eingabe_weg += [dict(w, eingabe="sw_%s" % biom) for w in weg_]
                for feld_plan in fp_:
                    feld = os.path.basename(os.path.dirname(feld_plan))
                    pool.lade_ebene(feld_plan, "sw_%s/%s/plan.json" % (biom, feld))
            for ort in od.get("orte") or []:
                sehens.append((biom, ort, os.path.join("sehens", biom, ort["id"], "fluss_sim.json")))
    for w in eingabe_weg:
        log("uebersprungen: %s/%s - %s" % (w["eingabe"], w["ordner"], w["grund"]))
    einbau = None if a.ohne_erkennung else einbau_ordner_finden(a.einbau, a.daten1m, a.gefaelle, a.sehens, a.sw_ordner)
    if a.einbau and not einbau and not a.ohne_erkennung:
        log("WARNUNG: --einbau %s nicht gefunden - keine Erkennung gebauter Laeufe" % a.einbau)
    ginfo = gelaende_laden(gel, a.gefaelle, gef_plaene, a.sehens if sehens_ok else None, a.gebaut or (), einbau)
    unbekannt = sorted(set(a.gebaut or ()) - set(gef_plaene) - {g["id"] for g in ginfo["gebaut"]}
                       - {o["id"] for _, o, _ in sehens} - {"SW_%s_%s" % (o["id"], w.get("id")) for _, o, _ in sehens
                                                            for w in o.get("wasser") or []})
    for g in ginfo["gebaut"]:
        log("gebaut: %s (%s) - %d Gelaende-Delta(s) nicht addiert (%s%s)" % (
            g["id"], g["art"], g["deltas_ohne"], g["quelle"], ", nachgezogen: %s" % g["nachgezogen_form"] if g["nachgezogen_form"] else ""))
    for g in ginfo["lauf_json_ungebaut"]:
        log("lauf.json ohne passendes Feld (%s nicht in nachgezogen, Form %s): %s - Delta wird addiert"
            % ("/".join(g["felder"]) or "?", g["nachgezogen_form"], g["lauf_json"]))
    for u in unbekannt:
        log("WARNUNG: --gebaut %s: kein Lauf-Plan bzw. Sehens-Ort mit Gelaende-Delta" % u)
    log("Gelaende-Deltas: %d addiert, %d nicht addiert (gebaut: %s); sehens_einbau %s"
        % (ginfo["addiert"], ginfo["ohne"], ", ".join(g["id"] for g in ginfo["gebaut"]) or "keiner",
           "gefunden" if einbau else ("nicht ausgewertet" if a.ohne_erkennung else "nicht gefunden")))
    pool.fertig()
    gewaesser, teile, karte, info = gewaesser_bilden(welt, a.gefaelle if gef_ok else None, sehens, regeln,
                                                     gef_plaene=gef_plaene)
    toepfe = info.pop("toepfe")
    sehens_seen = info.pop("sehens_seen")
    eingaben = {"lauf_plaene": len(gef_plaene), "uebersprungen": eingabe_weg,
                "bachbett_roh": {"ordner": "bachbett_roh" if roh_basis else None,
                                 "laeufe": len({r_.split("/")[1] for _, r_ in roh_liste}), "ebenen": len(roh_liste)}}
    gdelta = {"addiert": ginfo["addiert"], "nicht_addiert": ginfo["ohne"], "gebaut": ginfo["gebaut"],
                               "lauf_json_ungebaut": ginfo["lauf_json_ungebaut"], "gebaut_unbekannt": unbekannt,
                               "sehens_einbau": "gefunden" if einbau else ("nicht ausgewertet" if a.ohne_erkennung else "nicht gefunden")}
    nur = set(a.nur) if a.nur else None
    if nur:
        gewaesser = [gw for gw in gewaesser if gw["id"] in nur or any(l_["id"] in nur for l_ in gw["laeufe"])
                     or (gw.get("quelle_sehens") or {}).get("ort") in nur]
    log("Laeufe: %d Welt (%d mit Plan, %d roh), %d Sehens-Baeche; Fortsetzungen %s; Gewaesser: %d, Gelaende-Deltas %d"
        % (info["teile_welt"], info["teile_plan"], info["teile_roh"], info["sehens_baeche"], info["fortsetzungen"],
           len(gewaesser), len(gel.deltas)))
    if info.get("ersetzt"):
        log("Ersetzt (16h, ersetzt.json), nicht exportiert: %s" % ", ".join(
            "%s -> %s" % (k_, v_["ersetzt_durch"]) for k_, v_ in info["ersetzt"].items()))
    # je Gewaesser bauen
    dateien = {}
    alle = []
    for gw in gewaesser:
        e = baue_gewaesser_v3(gw, regeln, pool)
        alle.append(e)
        dateien.setdefault(gw["rel"], []).append(e)
    tempo_alt = {e["id"]: e.pop("_tempo_alt_cm_s") for e in alle}
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
    # Vorschlaege fuer offene Enden und Luecken (getrennt von der Spline)
    vorschlaege = vorschlaege_bilden(alle, karte, welt, gel, regeln)
    # v11: ein Teil, das in einem Gewaesser ausgefiltert ist, ist es in allen (Wasser-Kollision ist je Objekt eine)
    gefiltert = {}
    for rel in sorted(dateien):
        for e in dateien[rel]:
            for o in e["ohne_wasser_kollision"]:
                if str(o.get("grund", "")).startswith("filter_"):
                    gefiltert.setdefault(ref_text_von(o["ref"]), []).append(e["id"])
    for rel in sorted(dateien):
        for e in dateien[rel]:
            weg = [o for o in e["wasser_kollision"] if ref_text_von(o["ref"]) in gefiltert]
            if not weg:
                continue
            for o in weg:
                o["wasser_kollision"] = False
                o["grund"] = "filter_anderes_gewaesser"
                o["gefiltert_in"] = sorted(set(gefiltert[ref_text_von(o["ref"])]))
            e["wasser_kollision"] = [o for o in e["wasser_kollision"] if o["wasser_kollision"]]
            e["ohne_wasser_kollision"] = sorted(e["ohne_wasser_kollision"] + weg, key=lambda o: ref_text_von(o["ref"]))
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
        komps = hindernis_komponenten(komp, S.get("hindernis_grenzen"))
        kc["hindernis_akteur"] = {
            "id": "WH_" + kid, "klasse": "Actor", "label": "WH_" + kid, "tags": [S["hindernis_tag"], "SWR_B_" + kid],
            "ursprung_cm": [r1(0.5 * (b_[0] + b_[2])), r1(0.5 * (b_[1] + b_[3])), 0.0],
            "komponenten": komps,
            "akteure_mit_tag": akt,
            "n_instanzen": sum(len(v_) for v_ in komp.values()), "n_komponenten": len(komps), "n_akteure_mit_tag": len(akt),
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
                             "sim_vorgaben": {k_: sw[k_] for k_ in SIM_VORGABEN_FELDER},
                             "fingerabdruck": ges, "teile": teile_, "n_hoehen": nh, "n_objekte": no})
    # 16g Nachtrag (Regel v10): Water Zones fuer die ganze Welt (Wasser-Info fein genug fuer das schmalste Bett)
    wz = zonen_vorschlag(alle, regeln)
    for e in alle:
        e["water_body"]["water_zone_vorschlag"] = wz["gewaesser"][e["id"]]
    # schreiben
    for rel in sorted(dateien):
        d = {"format": FORMAT_VERSION, "regeln_version": regeln["version"], "fall_schwelle_m": regeln["fall_schwelle_m"],
             "daten": "1m" if a.daten1m else "2m (Cloud-Test)", "gewaesser": dateien[rel]}
        schreibe_json(os.path.join(a.aus, rel), d)
    zus = zusammenfassung(alle, regeln, info, kol_global, pool, karte, hoehe_kachel, gewaesser)
    zus["tempo"] = tempo_zusammenfassung(alle, tempo_alt, regeln)
    zus["schaum_maske"] = schaum_maske_zusammenfassung(alle, regeln)
    zus["toepfe"] = toepfe_zusammenfassung(toepfe, sehens_seen, karte, regeln, info, alle)
    zus["vorschlaege"] = vorschlaege_zusammenfassung(vorschlaege)
    zus["water_info"] = water_info_zusammenfassung(alle, wz, regeln)
    zus["eingaben"] = eingaben
    zus["gelaende_deltas"] = gdelta
    zus["daten"] = "1m" if a.daten1m else "2m (Cloud-Test)"
    zus["format"] = FORMAT_VERSION
    zus["dateien"] = len(dateien)
    schreibe_json(os.path.join(a.aus, "zusammenfassung.json"), zus)
    schreibe_json(os.path.join(a.aus, "wasserzonen.json"), wz, max_tiefe=3)
    schreibe_json(os.path.join(a.aus, "vorschlaege.json"),
                  {"format": "fluss_sim_vorschlaege_v1", "regeln": regeln["gewaesser"]["vorschlag"],
                   "hinweis": "Vorschlagspunkte fuer offene Enden und Luecken (16d). NICHT in water_body.spline enthalten; lokal "
                              "pruefen und uebernehmen. Erster Punkt = Spline-Ende, z nie steigend.",
                   "vorschlaege": vorschlaege}, max_tiefe=3)
    schreibe_json(os.path.join(a.aus, "back_liste.json"),
                  {"format": BACK_FORMAT, "fingerabdruck": dict(fpr, formel="siehe README fluss_sim, Abschnitt Fingerabdruck"),
                   "einheit": "SWR-Bereich (eine SWR je Gewaesser; Teilstuecke nur bei sehr grossem Rechteck)",
                   "gelaende": {"hinweis": "Fingerabdruck Gelaende = Welt + Planer-Deltas ohne die schon gebauter Laeufe (16d)",
                                "gebaut": [g["id"] for g in ginfo["gebaut"]], "deltas_ohne": ginfo["ohne_dateien"]},
                   "swr_bereiche": back})
    wi_ = zus["water_info"]
    log("Water-Info (16g Nachtrag): schmalste Breite %.2f m -> Pixel <= %.3f m; Zonenvorschlag %d Zonen (%d fein, %s), "
        "%.0f MB RGBA16F / %.0f MB RGBA32F"
        % (wi_["breite_min_m"]["min"], wi_["pixel_max_m"]["min"], wz["summe"]["zonen"], wz["summe"]["fein"],
           wz["summe"]["aufloesungen"], wz["summe"]["speicher_mb"]["rgba16f"], wz["summe"]["speicher_mb"]["rgba32f"]))
    s_ = zus["summe"]
    log("geschrieben: %d Dateien, %d Gewaesser (%d mit einer SWR), %d SWR-Bereiche, Aufloesung %s, Muendungen %s, %d Faelle "
        "(%d mit Vorhang), %d Kollisionsobjekte (%d eindeutig, %d ueberspannt), %d Hindernis-Akteure"
        % (len(dateien), s_["gewaesser"], s_["gewaesser_eine_swr"], s_["swr_bereiche"], zus["swr"]["aufloesung"], zus["muendungen"],
           s_["faelle"], s_["faelle_vorhang"], s_["kollision"], len(kol_global), s_["ueberspannt"], zus["swr"]["hindernis_akteure"]))
    return 0


def _stat(x):
    x = np.asarray(x, float)
    if not len(x):
        return None
    return {"n": int(len(x)), "mittel": r1(x.mean(), 3), "median": r1(np.median(x), 3),
            "p10": r1(np.percentile(x, 10), 3), "p90": r1(np.percentile(x, 90), 3), "min": r1(x.min(), 3), "max": r1(x.max(), 3)}


def gefaelle_klasse(g, grenzen):
    k = int(np.searchsorted(np.asarray(grenzen, float), g, side="right"))
    namen = ["< %g %%" % (grenzen[0] * 100)] + ["%g-%g %%" % (grenzen[i] * 100, grenzen[i + 1] * 100)
                                                 for i in range(len(grenzen) - 1)] + ["> %g %%" % (grenzen[-1] * 100)]
    return namen[k], namen


C2_LAUF = "F_ERLENBACH_1V_C2"


def tempo_zusammenfassung(alle, tempo_alt, regeln):
    """16e: Tempo vorher (Rolle aus dem Plan bzw. Weltdaten) / nachher (Gefaelle-Regel) in m/s, nach Rolle, Gefaelleklasse,
    Kategorie; dazu C2 (Lauf F_ERLENBACH_1V_C2 im Gewaesser F_ERLENBACH) und je Gewaesser die Rangkorrelation."""
    T = regeln["tempo"]
    gr = T["klassen_gefaelle"]
    alt_r, neu_r, alt_k, neu_k, alt_c, neu_c = {}, {}, {}, {}, {}, {}
    c2_alt, c2_neu, c2_r = {}, {}, {}
    A, N, rho = [], [], []
    for e in alle:
        sp = e["water_body"]["spline"]
        neu = np.asarray(sp["tempo_ms"], float)
        alt = np.asarray(tempo_alt[e["id"]], float) / 100.0
        gef = np.asarray(sp["tempo_info"]["gefaelle"], float)
        A += list(alt)
        N += list(neu)
        kat = e["kategorie"]
        alt_c.setdefault(kat, []).extend(alt)
        neu_c.setdefault(kat, []).extend(neu)
        c2 = next((l_["s_m"] for l_ in e["laeufe"] if l_["id"] == C2_LAUF), None)
        for i, rol in enumerate(sp["punkt_rollen"]):
            kl, _ = gefaelle_klasse(gef[i], gr)
            alt_r.setdefault(rol, []).append(alt[i]); neu_r.setdefault(rol, []).append(neu[i])
            alt_k.setdefault(kl, []).append(alt[i]); neu_k.setdefault(kl, []).append(neu[i])
            if c2 and c2[0] - 1e-6 <= sp["punkte_s_m"][i] <= c2[1] + 1e-6:
                c2_alt.setdefault(rol, []).append(alt[i]); c2_neu.setdefault(rol, []).append(neu[i])
                c2_r.setdefault("alle", []).append((alt[i], neu[i], gef[i]))
        if len(neu) >= 30 and np.ptp(gef) > 0.02:
            rho.append((round(spearman(gef, neu), 3), e["id"]))
    _, namen = gefaelle_klasse(0.0, gr)
    out = {"einheit": "m/s (UE: WaterVelocityScalar = x 100 cm/s)", "regel": T["regel"], "tempo_faktor": T["tempo_faktor"],
           "vorher": _stat(A), "nachher": _stat(N),
           "nach_rolle": {r: {"vorher": _stat(alt_r[r]), "nachher": _stat(neu_r[r])} for r in sorted(neu_r)},
           "nach_gefaelle": {k: {"vorher": _stat(alt_k[k]), "nachher": _stat(neu_k[k])} for k in namen if k in neu_k},
           "nach_kategorie": {k: {"vorher": _stat(alt_c[k]), "nachher": _stat(neu_c[k])} for k in sorted(neu_c)},
           "spearman_gefaelle": {"n_gewaesser": len(rho), "median": r1(np.median([r for r, _ in rho]), 3) if rho else None,
                                 "unter_min": sorted(i for r, i in rho if r < T["spearman_min"])}}
    if c2_r:
        a_, n_, g_ = (np.asarray(x, float) for x in zip(*c2_r["alle"]))
        out["c2"] = {"lauf": C2_LAUF, "punkte": int(len(a_)), "vorher": _stat(a_), "nachher": _stat(n_),
                     "nach_rolle": {r: {"vorher": _stat(c2_alt[r]), "nachher": _stat(c2_neu[r])} for r in sorted(c2_neu)},
                     "nach_gefaelle": {k: {"vorher": _stat([a for a, g in zip(a_, g_) if gefaelle_klasse(g, gr)[0] == k]),
                                           "nachher": _stat([n for n, g in zip(n_, g_) if gefaelle_klasse(g, gr)[0] == k])}
                                       for k in namen if any(gefaelle_klasse(g, gr)[0] == k for g in g_)}}
    elif C2_LAUF in ersetzte_laeufe():
        out["c2"] = {"lauf": C2_LAUF, "ersetzt": ersetzt_grund(C2_LAUF),
                     "hinweis": "C2 ist lokal Ferats Erlenbach p2; kein Teil dieses Exports (16h)"}
    return out


def spearman(x, y):
    def rang(v):
        v = np.asarray(v, float)
        o = np.argsort(v, kind="stable")
        r = np.empty(len(v))
        r[o] = np.arange(len(v), dtype=float)
        # Bindungen: mittlerer Rang
        _, inv, cnt = np.unique(v, return_inverse=True, return_counts=True)
        summe = np.bincount(inv, weights=r)
        return summe[inv] / cnt[inv]
    rx, ry = rang(x), rang(y)
    rx -= rx.mean()
    ry -= ry.mean()
    den = math.sqrt(float((rx * rx).sum() * (ry * ry).sum()))
    return float((rx * ry).sum() / den) if den > 0 else 0.0


def schaum_maske_zusammenfassung(alle, regeln):
    M = regeln["schaum"]["maske"]
    n = [e["schaum_maske"]["n"] for e in alle]
    rad = [k["radius_m"] for e in alle for k in e["schaum_maske"]["kapseln"]]
    return {"kapseln": int(sum(n)), "gewaesser_mit_kapseln": int(sum(1 for x in n if x)),
            "je_gewaesser_max": int(max(n)) if n else 0, "slots_max": M["slots_max"],
            "ueber_slots": sorted(e["id"] for e in alle if e["schaum_maske"]["ueber_slots"]),
            "radius_m": _stat(rad)}


def hindernis_filter_zusammenfassung(alle, regeln):
    """v11 (16g Nachtrag 2): Zahlen zum Hindernis-Filter (vorher = alle Objekte, die nach v10 Wasser-Kollision hatten)."""
    F = regeln["swr"].get("hindernis_filter")
    if not F:
        return None
    vor, nach, grund, rolle_v, rolle_n, art_v, art_n = {}, {}, {}, {}, {}, {}, {}
    je_gw = []
    for e in alle:
        n_v = n_n = 0
        for o in e["wasser_kollision"]:
            k_ = ref_text_von(o["ref"])
            vor[k_] = o
            nach[k_] = o
            n_v += 1
            n_n += 1
        for o in e["ohne_wasser_kollision"]:
            g_ = str(o.get("grund", ""))
            if g_.startswith("filter_"):
                vor[ref_text_von(o["ref"])] = o
                n_v += 1
        if n_v != n_n:
            je_gw.append((n_v - n_n, e["id"], n_v, n_n))
    for k_, o in vor.items():
        r_ = (o.get("filter") or {}).get("rolle", "?")
        rolle_v[r_] = rolle_v.get(r_, 0) + 1
        art_v[o["art"]] = art_v.get(o["art"], 0) + 1
        if k_ in nach:
            rolle_n[r_] = rolle_n.get(r_, 0) + 1
            art_n[o["art"]] = art_n.get(o["art"], 0) + 1
        else:
            g_ = o.get("grund")
            grund[g_] = grund.get(g_, 0) + 1
    srt = lambda d: {k_: d[k_] for k_ in sorted(d)}
    q = np.array([(o.get("filter") or {}).get("quer_im_bett_m", 0.0) / max((o.get("filter") or {}).get("bett_breite_m", 1.0), 1e-6)
                  for o in nach.values()], float)
    return {"status": F["status"], "teil_max_anteil": F["teil_max_anteil"], "meter_max_anteil": F["meter_max_anteil"],
            "objekte_eindeutig": {"vorher": len(vor), "nachher": len(nach), "gefiltert": len(vor) - len(nach)},
            "gefiltert_nach_grund": srt(grund), "rolle_vorher": srt(rolle_v), "rolle_nachher": srt(rolle_n),
            "art_vorher": srt(art_v), "art_nachher": srt(art_n),
            "anteil_quer_nachher": {"median": r1(float(np.median(q)), 3) if len(q) else None,
                                    "max": r1(float(q.max()), 3) if len(q) else None},
            "meiste_gefiltert": [[i, v_, n_] for d_, i, v_, n_ in sorted(je_gw, key=lambda t_: (-t_[0], t_[1]))[:10]]}


def water_info_zusammenfassung(alle, wz, regeln):
    """16g Nachtrag: Zahlen zur Regel water_info und zum Zonenvorschlag."""
    W = regeln["swr"]["water_info"]
    ks = [kc for e in alle for kc in e["swr_bereiche"]]
    wi = [(kc["id"], kc["water_info"]) for kc in ks]
    b = np.array([w["breite_min_m"] for _, w in wi], float)
    px = np.array([w["pixel_max_m"] for _, w in wi], float)
    zm = np.array([w["zone_max_m"][str(W["aufloesung_max"])] for _, w in wi], float)
    zb = W["zone_bekannt_m"]
    rb = {}
    for _, w in wi:
        k_ = str(w["zone_bekannt"]["aufloesung"])
        rb[k_] = rb.get(k_, 0) + 1
    grenzen = [1.0, 2.0, 3.0, 5.0, 10.0, 15.0]
    bv, lo = {}, 0.0
    for g_ in grenzen:
        bv["<= %g" % g_] = int(((b > lo) & (b <= g_ + 1e-9)).sum())
        lo = g_ + 1e-9
    bv["> %g" % grenzen[-1]] = int((b > grenzen[-1] + 1e-9).sum())
    return {
        "status": W["status"], "swr_bereiche": len(wi),
        "breite_min_m": {"min": r1(float(b.min()), 2), "median": r1(float(np.median(b)), 2), "verteilung": bv},
        "pixel_max_m": {"min": r1(float(px.min()), 4), "median": r1(float(np.median(px)), 4)},
        "zone_max_m_bei_%d" % W["aufloesung_max"]: {"min": r1(float(zm.min()), 1), "median": r1(float(np.median(zm)), 1),
                                                     "unter_zone_bekannt": int((zm < zb - 1e-9).sum())},
        "zone_bekannt_%g_m_aufloesung" % zb: {k_: rb[k_] for k_ in sorted(rb, key=int)},
        "zone_bekannt_%g_m_1024_pixel_quer_unter_teiler" % zb: sum(1 for _, w in wi if w["zone_bekannt"]["pixel_quer"]["1024"] < W["breite_teiler"] - 1e-9),
        "schmalste": [[i, w["breite_min_m"], w["pixel_max_m"], w["zone_max_m"][str(W["aufloesung_max"])]]
                      for i, w in sorted(wi, key=lambda t: (t[1]["breite_min_m"], t[0]))[:10]],
        "zonen": wz["summe"]}


def vorschlaege_zusammenfassung(vorschlaege):
    out = {"anzahl": len(vorschlaege), "datei": "vorschlaege.json", "nach_art": {}, "methode": {}, "ziel": {},
           "laenge_m": {}, "einschnitt_ueber_1m": [], "kreuzt_hoeheres_wasser": [], "ohne_ziel": []}
    L = []
    for o in vorschlaege:
        v = o["vorschlag"]
        out["nach_art"][v["art"]] = out["nach_art"].get(v["art"], 0) + 1
        out["methode"][v["methode"]] = out["methode"].get(v["methode"], 0) + 1
        z = (v.get("ziel") or {}).get("art", "keins")
        out["ziel"][z] = out["ziel"].get(z, 0) + 1
        L.append(v["laenge_m"])
        if v["einschnitt_max_m"] > 1.0:
            out["einschnitt_ueber_1m"].append([o["gewaesser"], v["einschnitt_max_m"]])
        if v.get("kreuzt"):
            out["kreuzt_hoeheres_wasser"].append([o["gewaesser"], v["kreuzt"]])
        if not v.get("ziel"):
            out["ohne_ziel"].append(o["gewaesser"])
    for k in ("nach_art", "methode", "ziel"):
        out[k] = {x: out[k][x] for x in sorted(out[k])}
    if L:
        out["laenge_m"] = {"min": r1(min(L), 1), "median": r1(float(np.median(L)), 1), "max": r1(max(L), 1)}
    out["liste"] = [[o["gewaesser"], o["vorschlag"]["art"], (o["vorschlag"].get("ziel") or {}).get("id"), o["vorschlag"]["laenge_m"]]
                    for o in vorschlaege]
    return out


def toepfe_zusammenfassung(toepfe, sehens_seen, karte, regeln, info, alle):
    mx = toepfe_max(regeln)
    art = {}
    for tp in toepfe.values():
        art[tp["art"]] = art.get(tp["art"], 0) + 1
    verbunden = set()
    for s in sehens_seen:
        verbunden.add(s["id"])
    gross = sorted(s["id"] for s in sehens_seen if not s.get("topf") and s["ausdehnung_m"] >= mx
                   and any(e["anfang"].get("ziel") == s["id"] or e["muendung"].get("ziel") == s["id"] for e in alle))
    welt_klein = 0
    for s in karte.seen:
        if s["quelle"] == "wasser_welt.json":
            U = s["umriss"]
            if len(U) > 1 and float(np.hypot(U[:, None, 0] - U[None, :, 0], U[:, None, 1] - U[None, :, 1]).max()) / 100.0 < mx:
                welt_klein += 1
    sg = [e for e in alle if e["kategorie"] == "sehens"]
    return {"max_ausdehnung_m": mx, "anzahl": len(toepfe), "nach_art": {k: art[k] for k in sorted(art)},
            "sehens_baeche": info["sehens_baeche"], "sehens_gewaesser": len(sg),
            "sehens_gewaesser_mit_topf": sum(1 for e in sg if e.get("toepfe")),
            "liste": [{"see": tp["see"], "art": tp["art"], "ausdehnung_m": tp["ausdehnung_m"], "gewaesser": tp["gewaesser"],
                       "zulauf": tp["zulauf"], "abfluss": tp["abfluss"]} for _, tp in sorted(toepfe.items())],
            "seen_bleiben": {"sehens_mit_bach_ab_grenze": gross,
                             "sehens_ohne_bach": sum(1 for s in sehens_seen if not s.get("topf") and s["id"] not in gross),
                             "welt_unter_grenze_unveraendert": welt_klein},
            "hinweis": "Toepfe sind Teil ihres Gewaessers (Bereich rolle 'topf', Feld toepfe[]): lokal KEIN WaterBodyLake bauen"}


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
        su["ueberspannt"] += sum(1 for o in e["ohne_wasser_kollision"] if o.get("grund") == "ueberspannt")
        su["gefiltert"] = su.get("gefiltert", 0) + sum(1 for o in e["ohne_wasser_kollision"]
                                                      if str(o.get("grund", "")).startswith("filter_"))
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
    # 16g: Rand und Steilheit (Diagnose)
    rs = [(kc["id"], kc["rand_steil"]) for kc in ks]
    eig = {}
    for _, r_ in rs:
        eig[r_["eignung"]] = eig.get(r_["eignung"], 0) + 1
    hs = np.array([r_["hoehenspanne_m"] for _, r_ in rs], float)
    zus["swr_rand_steil"] = {
        "status": S["rand_steil"]["status"],
        "quelle_zu_nah": sum(1 for _, r_ in rs if r_["anfang"]["art"] == "quelle" and r_["anfang"]["zu_nah"]),
        "quellen": sum(1 for _, r_ in rs if r_["anfang"]["art"] == "quelle"),
        "quelle_abstand_m": {"median": r1(float(np.median([r_["anfang"]["abstand_m"] for _, r_ in rs if r_["anfang"]["art"] == "quelle"])), 2),
                             "unter_1m": sum(1 for _, r_ in rs if r_["anfang"]["art"] == "quelle" and r_["anfang"]["abstand_m"] < 1.0)},
        "mit_kontakt_im_lauf": sum(1 for _, r_ in rs if any(not k_["am_ende"] for k_ in r_["kontakte"])),
        "kontakte_im_lauf": sum(1 for _, r_ in rs for k_ in r_["kontakte"] if not k_["am_ende"]),
        "kontakte_summe": sum(len(r_["kontakte"]) for _, r_ in rs),
        "hoehenspanne_m": {"median": r1(float(np.median(hs)), 1), "max": r1(float(hs.max()), 1),
                           "ueber_50": int((hs > 50).sum()), "ueber_100": int((hs > 100).sum())},
        "eignung": {k_: eig[k_] for k_ in sorted(eig)},
        "laenge_kaskade_m": r1(sum(r_["laenge_kaskade_m"] for _, r_ in rs), 1),
        "laenge_pruefen_m": r1(sum(r_["laenge_pruefen_m"] for _, r_ in rs), 1),
        "steilste": [[i, r_["gefaelle_fenster_max"], r_["laenge_kaskade_m"], r_["hoehenspanne_m"]]
                     for i, r_ in sorted(rs, key=lambda t: (-t[1]["laenge_kaskade_m"], -t[1]["gefaelle_fenster_max"], t[0]))[:10]]}
    # Varianten der Zielzelle (Zielzelle, hoechste Zelle) fuer Bach / Fluss: wie viele Gewaesser muessten geteilt werden?
    var = {}
    for name, zb, mb, mbu, zf, mf in (
            ("regel 16e: bach 0.25 (ungeteilt bis %.2f, Teilstuecke max %.2f), fluss 0.35"
             % (zelle_max_ungeteilt("bach", S), S["zelle_max_bach_m"]), S["zelle_ziel_bach_m"], S["zelle_max_bach_m"],
             zelle_max_ungeteilt("bach", S), S["zelle_ziel_fluss_m"], S["zelle_max_fluss_m"]),
            ("16d: bach 0.25 (max 0.30), fluss 0.35", 0.25, 0.30, 0.30, 0.35, 0.35),
            ("bach 0.25 (max 0.25), fluss 0.35", 0.25, 0.25, 0.25, 0.35, 0.35),
            ("alle 0.25", 0.25, 0.25, 0.25, 0.25, 0.25),
            ("bach 0.30, fluss 0.35", 0.30, 0.30, 0.30, 0.35, 0.35),
            ("bis 512 (Zwischenregel 16c): bach 0.35, fluss 0.5", 0.35, 0.35, 0.35, 0.5, 0.5)):
        n_t, n_k, rv = 0, 0, {"<= 512": 0, "513-1024": 0, "1025-2048": 0}
        rmax = 512 if "512" in name else S["resolution_max"]
        S2 = dict(S, resolution_max=rmax)
        for e, gw in zip(alle, gewaesser):
            ss_ = e["water_body"]["spline"]["punkte_s_m"]
            typ_ = [gw["typ_bei"](x) for x in ss_]
            Lm = np.array([rmax * (mb if t == "bach" else mf) for t in typ_], float)
            Lu = np.array([rmax * (mbu if t == "bach" else mf) for t in typ_], float)
            P = e["water_body"]["spline"]["punkte"]
            if achse_von(box_punkte(P, 0, len(P) - 1)) <= float(Lu.min()) + 1e-9:
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
    zus["hindernis_filter"] = hindernis_filter_zusammenfassung(alle, regeln)
    zus["objekt_pool"] = {"objekte": len(pool.recs), "fest_und_gross": int(pool.fest.sum()),
                          "fest_und_gross_regel_bis_v7": int(pool.fest_alt.sum()),
                          "mindestgroesse": "groesste Ausdehnung (Netz-Bounds x |Skala|) >= %.2f m und Hoehe >= %.2f m"
                                            % (regeln["kollision"]["min_ausdehnung_m"], regeln["kollision"]["min_hoehe_m"])}
    return zus


if __name__ == "__main__":
    sys.exit(main())
