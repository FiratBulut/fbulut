# -*- coding: utf-8 -*-
"""bach_anfaenge_plan.py - Auftrag 19: Wie beginnt ein Bach? Plaene fuer die 83 Anfaenge "aus dem Nichts",
Breitenverjuengung fuer alle Anfaenge, die 8 versickernden Enden und die Kaskade K1.

Liest NUR (aendert keinen Planer, keinen Exporter, kein Gelaende):
  - Befund Ferat 13.10. (auftraege/daten/bach_anfaenge/bach_anfaenge.json): Klasse, Biom, Mulde, See, Ende je Gewaesser
  - Splines der Welt (vorlagen/daten/sehens/wasser_welt.json 'fluesse', baeche_alle.json): Punkte [X, Y, Z, Breite,
    Tiefe, Tempo] in cm, Punkt 0 oben (gleiche Daten wie Ferats Werkzeug, Anfang/Ende geprueft)
  - Gelaende 2 m (sehens_lib.daten.lade) bzw. 1 m lokal (--daten1m)
  - fluss_sim: vorschlaege.json (Wege fuer offene Enden, auch F_HAUPTFLUSS_2 -> K1), wasserzonen.json (Gewaesser-Namen),
    skripte/fluss_sim/ersetzt.json (C2-Laeufe durch Erlenbach p2 ersetzt: nicht anfassen)
  - Bericht 17 (wasserherkunft/faelle_herkunft.json): Oberlauf WF_K1
  - felsgruppen_regeln.json (Fels-Paletten je Biom, Biom-Sperren), Inventar (Netznamen, Masse, Saegeschnitt)
Schreibt nach --aus (Standard antworten/bach_anfaenge/):
  bach_anfaenge_plan.json   Plaene je Fall, Spline-Aenderungen (Kopf ersetzen / anhaengen / Ende ersetzen),
                            neue Seen, Lagen-Wuensche, Instanzen, Verjuengung aller Anfaenge, Neu-Backen-Liste
  instanzen/<Feld>/<Netz>.f32 + plan.json   Instanzen im Format FORMAT.md 3 (10 float32 je Instanz)
  bilder/*.png              Uebersicht, Regel-Profil, Skizze je Loesungstyp (--bild)

Aufruf:
  python -I recherche/antworten/skripte/bach_anfaenge/bach_anfaenge_plan.py [--bild] [--aus DIR] [--daten1m DIR]
Deterministisch: Zufall aus sha256(Seed, Gewaesser, Rolle), sortierte Ausgaben, gerundete Werte.
"""

import argparse
import hashlib
import json
import math
import os
import random
import re
import shutil
import struct
import sys

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
SKRIPTE = os.path.dirname(HIER)
ANTWORTEN = os.path.dirname(SKRIPTE)
RECHERCHE = os.path.dirname(ANTWORTEN)
sys.path.insert(0, SKRIPTE)

from sehens_lib import daten as D            # noqa: E402
from sehens_lib.inventar import Inventar     # noqa: E402

STD = {
    "regeln": os.path.join(HIER, "bach_anfaenge_regeln.json"),
    "befund": os.path.join(RECHERCHE, "auftraege", "daten", "bach_anfaenge", "bach_anfaenge.json"),
    "welt": os.path.join(RECHERCHE, "vorlagen", "daten", "sehens"),
    "vorschlaege": os.path.join(ANTWORTEN, "fluss_sim", "vorschlaege.json"),
    "zonen": os.path.join(ANTWORTEN, "fluss_sim", "wasserzonen.json"),
    "ersetzt": os.path.join(SKRIPTE, "fluss_sim", "ersetzt.json"),
    "herkunft": os.path.join(ANTWORTEN, "wasserherkunft", "faelle_herkunft.json"),
    "fels": os.path.join(SKRIPTE, "felsgruppen_regeln.json"),
    "aus": os.path.join(ANTWORTEN, "bach_anfaenge"),
}
FORMAT = "bach_anfaenge_plan_v1"
PUNKT_FELDER = ["x_cm", "y_cm", "z_cm", "breite_cm", "tiefe_cm", "tempo_cm_s"]


# ======================================================================================================================
# Kleinkram
# ======================================================================================================================
def lese(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def r(x, n=1):
    return round(float(x), n)


def rng(*k):
    h = hashlib.sha256("|".join(str(x) for x in k).encode("utf-8")).hexdigest()
    return random.Random(int(h[:16], 16))


def bogen(pk):
    """Bogenlaenge in m je Punkt (Punkte in cm)."""
    s = [0.0]
    for a, b in zip(pk[:-1], pk[1:]):
        s.append(s[-1] + math.hypot(b[0] - a[0], b[1] - a[1]) / 100.0)
    return s


def einheit(dx, dy):
    n = math.hypot(dx, dy)
    return (dx / n, dy / n) if n > 1e-9 else (1.0, 0.0)


def drehe(v, grad):
    a = math.radians(grad)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def interp_punkt(pk, s, sw):
    """Punkt (alle 6 Werte) bei Bogenlaenge sw (m) auf pk mit Bogen s."""
    if sw <= s[0]:
        return list(pk[0])
    for i in range(1, len(s)):
        if sw <= s[i] + 1e-9:
            t = (sw - s[i - 1]) / max(s[i] - s[i - 1], 1e-9)
            return [pk[i - 1][k] + t * (pk[i][k] - pk[i - 1][k]) for k in range(len(pk[i]))]
    return list(pk[-1])


def median(v):
    v = sorted(v)
    n = len(v)
    if not n:
        return None
    return v[n // 2] if n % 2 else 0.5 * (v[n // 2 - 1] + v[n // 2])


def ellipse(cx, cy, ux, uy, a_m, b_m, n=32):
    """Ellipse um (cx, cy) in cm, Halbachse a_m entlang (ux, uy), b_m quer; Umriss in cm (gegen den Uhrzeiger)."""
    out = []
    for k in range(n):
        t = 2 * math.pi * k / n
        la, lc = a_m * math.cos(t), b_m * math.sin(t)
        out.append([r(cx + (la * ux - lc * uy) * 100.0), r(cy + (la * uy + lc * ux) * 100.0)])
    return out


def punkt_in_polygon(x, y, poly):
    inn = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xs = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xs:
                inn = not inn
    return inn


def huelle(p):
    """Konvexe Huelle (monotone chain), p Liste (x, y)."""
    p = sorted(set(p))
    if len(p) < 3:
        return p

    def kreuz(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in p:
        while len(lo) >= 2 and kreuz(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(hi) >= 2 and kreuz(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]


def flaeche(poly):
    a = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2.0


# ---------------------------------------------------------------- Drehung
def mat_quat(m):
    t = m[0][0] + m[1][1] + m[2][2]
    if t > 0:
        s = math.sqrt(t + 1.0) * 2
        w, x, y, z = 0.25 * s, (m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s
    elif m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        s = math.sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) * 2
        w, x, y, z = (m[2][1] - m[1][2]) / s, 0.25 * s, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s
    elif m[1][1] > m[2][2]:
        s = math.sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2
        w, x, y, z = (m[0][2] - m[2][0]) / s, (m[0][1] + m[1][0]) / s, 0.25 * s, (m[1][2] + m[2][1]) / s
    else:
        s = math.sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2
        w, x, y, z = (m[1][0] - m[0][1]) / s, (m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, 0.25 * s
    n = math.sqrt(w * w + x * x + y * y + z * z)
    q = [x / n, y / n, z / n, w / n]
    # kanonisch wie fluss_sim: erstes Element != 0 in der Reihenfolge w, z, y, x positiv
    for k in (3, 2, 1, 0):
        if abs(q[k]) > 1e-12:
            if q[k] < 0:
                q = [-v for v in q]
            break
    return q


def mat_achse(ax, grad):
    a = math.radians(grad)
    x, y, z = ax
    n = math.sqrt(x * x + y * y + z * z)
    if n < 1e-12:
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    x, y, z = x / n, y / n, z / n
    c, s, C = math.cos(a), math.sin(a), 1 - math.cos(a)
    return [[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C]]


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


# ======================================================================================================================
# Daten
# ======================================================================================================================
class Welt:
    def __init__(self, args):
        self.R = lese(args.regeln)
        self.befund = lese(args.befund)
        ww = lese(os.path.join(args.welt, "wasser_welt.json"))
        ba = lese(os.path.join(args.welt, "baeche_alle.json"))
        self.splines = {}
        for f in ww["fluesse"]:
            self.splines[f["id"]] = [list(map(float, p)) for p in f["punkte"]]
        for b in ba["baeche"]:
            self.splines[b["id"]] = [list(map(float, p)) for p in b["punkte"]]
        self.seen = {s["id"]: s for s in ww["seen"]}
        self.wasserfaelle = ww.get("wasserfaelle", [])
        self.vorschlaege = {v["gewaesser"]: v for v in lese(args.vorschlaege)["vorschlaege"]}
        self.zonen_gew = set(lese(args.zonen)["gewaesser"].keys())
        er = lese(args.ersetzt)
        self.ersetzt = sorted(k for k, v in er.get("laeufe", {}).items() if v.get("aktiv", True) is not False)
        self.herkunft = {f["id"]: f for f in lese(args.herkunft)["faelle"]}
        self.fels = lese(args.fels)
        self.inv = Inventar.lade()
        if args.daten1m:
            self.w = D.lade(daten1m=args.daten1m)
        else:
            self.w = D.lade(daten2m=args.welt)
        self.gew = {g["id"]: g for g in self.befund["gewaesser"]}
        self._gew_map()

    # --- Hoehe
    def h(self, x_m, y_m):
        return float(self.w.hoehe_bei_m(x_m, y_m))

    def h_cm(self, x_cm, y_cm):
        return self.h(x_cm / 100.0, y_cm / 100.0) * 100.0

    def normale(self, x_m, y_m):
        d = 1.0
        hx = (self.h(x_m + d, y_m) - self.h(x_m - d, y_m)) / (2 * d)
        hy = (self.h(x_m, y_m + d) - self.h(x_m, y_m - d)) / (2 * d)
        n = math.sqrt(hx * hx + hy * hy + 1.0)
        return (-hx / n, -hy / n, 1.0 / n)

    def biom(self, x_m, y_m):
        return self.w.biom_bei_m(x_m, y_m)

    # --- Gewaesser-Namen wie fluss_sim (wasserzonen.json 'gewaesser')
    def _gew_map(self):
        nach = {}
        for g in self.befund["gewaesser"]:
            m = re.match(r"Fortsetzung: (\S+)", g["ende"].get("text", ""))
            if m and m.group(1) in self.gew:
                nach.setdefault(m.group(1), []).append(g["id"])
        self.vorgaenger = {k: sorted(v) for k, v in nach.items()}
        self.gewaesser_von = {}
        for gid in sorted(self.gew):
            self.gewaesser_von[gid] = self._gew_name(gid, set())

    def _gew_name(self, gid, gesehen):
        if gid in self.zonen_gew:
            return gid
        g = self.gew[gid]
        for k in (g.get("gruppe"), g.get("familie")):
            if g["art"] == "fluss" and k in self.zonen_gew:
                return k
        if g["art"] == "swr" or gid in gesehen:
            return None
        gesehen.add(gid)
        for v in self.vorgaenger.get(gid, []):
            n = self._gew_name(v, gesehen)
            if n:
                return n
        return None


# ======================================================================================================================
# Profil am Anfang
# ======================================================================================================================
def biom_norm(W, b):
    return W.R["klassifizierung"]["biom_alias"].get(b, b)


def laenge_L(W, B, biom, gefaelle, ist_fluss, typ):
    A = W.R["anfang"]
    L = A["L_m"]
    if typ in ("seeabfluss", "nebenarm", "abzweig"):
        return L[typ]
    if ist_fluss:
        return max(L["fluss_min"], min(L["fluss_max"], L["fluss_je_m_breite"] * B))
    f = A["L_biom_faktor"].get(biom, 1.0)
    if gefaelle >= A["steil_ab"]:
        f *= A["steil_faktor"]
    return max(L["min"], min(L["max"], f * (L["basis"] + L["je_m_breite"] * B)))


def b0_von(W, typ, B):
    A = W.R["anfang"]
    if typ in A["b0_m"]:
        return min(A["b0_m"][typ], B)
    return A["b0_anteil"][typ] * B


def profil(W, s, L, b0, B):
    if s >= L:
        return B
    e = W.R["anfang"]["exponent_breite"]
    return b0 + (B - b0) * (max(s, 0.0) / L) ** e


def tiefe_von(W, breite_m, t_orig_m, ist_fluss):
    T = W.R["anfang"]["tiefe"]
    soll = t_orig_m if ist_fluss else max(t_orig_m, T["klemme_ferat_m"])
    return max(T["min_m"], min(soll, breite_m / T["breite_teiler"]))


def tempo_von(W, s, L, v_orig):
    v0 = min(W.R["anfang"]["tempo_quelle_cm_s"], v_orig)
    if s >= L:
        return v_orig
    return v0 + (v_orig - v0) * (max(s, 0.0) / L) ** 0.5


def sollbreite(pk):
    s = bogen(pk)
    w = [p[3] / 100.0 for p, ss in zip(pk, s) if 20.0 <= ss <= 120.0]
    if not w:
        w = [p[3] / 100.0 for p in pk]
    return median(w)


def kopf_bauen(W, alt, neu_xyz, b0, L, B, ist_fluss):
    """Neuer Kopf: neue Punkte (oben -> unten, ohne alten Punkt 0) + alte Punkte bis s < L (auf <= 5 m verdichtet).
    Rueckgabe (kopf_punkte, alt_bis_index_exkl). Danach folgt alt[k:] unveraendert."""
    ds = W.R["anfang"]["punktabstand_m"]
    s_alt = bogen(alt)
    # Laenge der Verlaengerung
    kette = [list(p) for p in neu_xyz] + [alt[0][:3]]
    ext = bogen(kette)[-1] if neu_xyz else 0.0
    k = 0
    while k < len(alt) and s_alt[k] + ext < L:
        k += 1
    if k == 0:
        k = 1
    k = min(k, len(alt))
    kopf = []
    # neue Punkte (Werte des alten Punkts 0 als Vorlage fuer Tiefe/Tempo)
    t0, v0 = alt[0][4] / 100.0, alt[0][5]
    s_kette = bogen(kette)
    for p, s in zip(neu_xyz, s_kette[:-1]):
        b = min(profil(W, s, L, b0, B), B)
        kopf.append([p[0], p[1], p[2], b * 100.0, tiefe_von(W, b, t0, ist_fluss) * 100.0, tempo_von(W, s, L, v0)])
    # alte Punkte 0 .. k-1 verdichtet
    for i in range(k):
        seg = [alt[i]]
        if i + 1 < len(alt) and i + 1 <= k:
            d = s_alt[i + 1] - s_alt[i]
            n = int(math.ceil(d / ds - 1e-9))
            for j in range(1, n):
                seg.append(interp_punkt(alt, s_alt, s_alt[i] + d * j / n))
        for p in seg:
            s_ab = _s_auf(alt, s_alt, p) + ext
            b = min(profil(W, s_ab, L, b0, B), p[3] / 100.0) if s_ab < L else p[3] / 100.0
            b = max(b, min(b0, p[3] / 100.0))
            t = tiefe_von(W, b, p[4] / 100.0, ist_fluss) if s_ab < L else p[4] / 100.0
            v = tempo_von(W, s_ab, L, p[5])
            kopf.append([p[0], p[1], p[2], b * 100.0, t * 100.0, v])
    return kopf, k


def _s_auf(pk, s, p):
    best, bs = 1e18, 0.0
    for i in range(len(pk) - 1):
        ax, ay, bx, by = pk[i][0], pk[i][1], pk[i + 1][0], pk[i + 1][1]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 < 1e-9 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
        qx, qy = ax + t * dx, ay + t * dy
        d = math.hypot(p[0] - qx, p[1] - qy)
        if d < best - 1e-9:
            best, bs = d, s[i] + t * (s[i + 1] - s[i])
    return bs


def runde_punkte(pk):
    return [[r(p[0]), r(p[1]), r(p[2]), r(p[3]), r(p[4]), r(p[5])] for p in pk]


# ======================================================================================================================
# Wege hangauf
# ======================================================================================================================
def spur_hoch(W, x_m, y_m, u, max_len, wand_stop=True, kegel=None):
    """Talweg aufwaerts: je Schritt im Kegel um u die niedrigste Stelle, die hoeher liegt (Tiefenlinie hangauf).
    Rueckgabe (punkte [(x, y, h)], grund)."""
    K = W.R["klassifizierung"]
    st = K["spur_schritt_m"]
    kegel = K["spur_kegel_grad"] if kegel is None else kegel
    hcur = W.h(x_m, y_m)
    cur = (x_m, y_m)
    d = u
    out = []
    grund = "laenge"
    for _ in range(int(max_len / st + 1e-9)):
        kand = []
        a = -kegel
        while a <= kegel + 1e-9:
            v = drehe(d, a)
            px, py = cur[0] + st * v[0], cur[1] + st * v[1]
            hh = W.h(px, py)
            if hh >= hcur + K["spur_anstieg_min_m"]:
                kand.append((round(hh, 3), abs(a), a, px, py))
            a += K["spur_kegel_schritt_grad"]
        if not kand:
            grund = "flach"
            break
        kand.sort()
        hh, _, a, px, py = kand[0]
        if wand_stop and (hh - hcur) / st > K["spur_wand_steigung"]:
            grund = "wand"
            break
        out.append((px, py, hh))
        nd = einheit(px - cur[0], py - cur[1])
        d = einheit(0.5 * d[0] + 0.5 * nd[0], 0.5 * d[1] + 0.5 * nd[1])
        cur, hcur = (px, py), hh
    return out, grund


def neue_punkte_z(W, weg_oben_nach_unten_m, z_unten_cm):
    """weg: [(x_m, y_m, h_m)] von oben nach unten (ohne alten Punkt 0). Spiegel = Gelaende - 0,10 m, nie fallend
    hangauf (von unten aus gerechnet: z >= z des Punktes darunter)."""
    dz = W.R["anfang"]["spiegel_unter_gelaende_m"] * 100.0
    out = []
    z_vor = z_unten_cm
    for x, y, h in reversed(weg_oben_nach_unten_m):
        z = max(h * 100.0 - dz, z_vor)
        out.append([x * 100.0, y * 100.0, z])
        z_vor = z
    return list(reversed(out))


def glaette(W, start, sp, runden=2):
    """Talweg-Spur (2-m-Raster, zickzack) glaetten: 3er-Mittel der xy, Start fest; Hoehe neu abgefragt."""
    xy = [start] + [(p[0], p[1]) for p in sp]
    for _ in range(runden):
        neu = [xy[0]]
        for i in range(1, len(xy) - 1):
            neu.append((0.25 * xy[i - 1][0] + 0.5 * xy[i][0] + 0.25 * xy[i + 1][0],
                        0.25 * xy[i - 1][1] + 0.5 * xy[i][1] + 0.25 * xy[i + 1][1]))
        neu.append(xy[-1])
        xy = neu
    return [(x, y, W.h(x, y)) for x, y in xy[1:]]


def verdichte_m(pts_m, ds):
    """Polylinie (x, y) in m auf <= ds verdichten (inkl. Endpunkte)."""
    out = [pts_m[0]]
    for a, b in zip(pts_m[:-1], pts_m[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(math.ceil(d / ds - 1e-9)))
        for j in range(1, n + 1):
            t = j / n
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    return out


# ======================================================================================================================
# Instanzen
# ======================================================================================================================
class Instanzen:
    def __init__(self, W):
        self.W = W
        self.liste = []          # dict je Instanz
        self.fels = W.fels
        self.nur = {k: v for k, v in W.fels["netz_nur_biome"]["netze"].items()}
        self.gesperrt = set(W.fels["gesperrt"]["netze"])
        self._ok_cache = {}

    def netz_ok(self, n, biom):
        key = (n, biom)
        if key in self._ok_cache:
            return self._ok_cache[key]
        ok = True
        try:
            p = self.W.inv.netz(n)["pfad"]
        except Exception:
            ok = False
            p = n
        if ok:
            bef = self.W.inv.netz_pruefen(p, wildnis=True)
            if bef or p in self.gesperrt:
                ok = False
            if p in self.nur and biom not in self.nur[p]:
                ok = False
        self._ok_cache[key] = ok
        return ok

    def palette(self, biom, rolle):
        pal = self.fels["biom_palette"].get(biom, "nordisch")
        liste = self.fels["paletten"][pal].get(rolle, [])
        return [n for n in liste if self.netz_ok(n, biom)]

    def setze(self, fall, netz, x_m, y_m, rolle, ziel_m=None, skala=None, eingraben=0.0, kipp=1.0, yaw=0.0,
              plus_cm=0.0, extra_achse=None, extra_grad=0.0, kollision_auto=True):
        W = self.W
        n = W.inv.netz(netz)
        pfad = n["pfad"]
        gx, gy, gz = n["groesse_m"]
        if skala is None:
            skala = ziel_m / max(gx, gy, gz)
        bmin = n.get("bounds_cm")[0][2] if n.get("bounds_cm") else 0.0
        nx, ny, nz = W.normale(x_m, y_m)
        # Kippen auf die Normale (Anteil kipp)
        ax = (-ny, nx, 0.0)
        winkel = math.degrees(math.acos(max(-1.0, min(1.0, nz)))) * kipp
        m = mat_achse(ax, winkel)
        if extra_achse is not None:
            m = mat_mul(m, mat_achse(extra_achse, extra_grad))
        m = mat_mul(m, mat_achse((0.0, 0.0, 1.0), yaw))
        q = mat_quat(m)
        z = W.h(x_m, y_m) * 100.0 - bmin * skala - eingraben * gz * 100.0 * skala + plus_cm
        hoehe_m = gz * skala
        groesste = max(gx, gy, gz) * skala
        kol = kollision_auto and rolle in ("fels", "platte") and hoehe_m >= W.R["quellfassung"]["kollision_ab_m"]
        self.liste.append({"fall": fall, "netz": n["name"], "pfad": pfad, "rolle": rolle,
                           "x": x_m * 100.0, "y": y_m * 100.0, "z": z, "q": q, "s": skala,
                           "hoehe_m": hoehe_m, "groesse_m": groesste, "kollision": bool(kol)})

    def waehle(self, liste, ziel_m, g, lo=0.4, hi=2.5):
        """Netz aus der Liste, dessen Skala fuer die Zielgroesse (groesste Kante) in [lo, hi] liegt; sonst das naechste."""
        passt, alle = [], []
        for n in liste:
            gx, gy, gz = self.W.inv.netz(n)["groesse_m"]
            sk = ziel_m / max(gx, gy, gz)
            alle.append((abs(math.log(sk)), n))
            if lo <= sk <= hi:
                passt.append(n)
        if passt:
            return passt[g.randrange(len(passt))]
        return sorted(alle)[0][1]

    def von_fall(self, fall):
        return [i for i in self.liste if i["fall"] == fall]


def abstand_spline_m(x_m, y_m, pk):
    """kleinster Abstand (m) zur Mittellinie minus halbe Breite."""
    best = 1e18
    for i in range(len(pk) - 1):
        ax, ay, bx, by = pk[i][0] / 100, pk[i][1] / 100, pk[i + 1][0] / 100, pk[i + 1][1] / 100
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((x_m - ax) * dx + (y_m - ay) * dy) / L2))
        b = (pk[i][3] + t * (pk[i + 1][3] - pk[i][3])) / 200.0
        d = math.hypot(x_m - (ax + t * dx), y_m - (ay + t * dy)) - b
        best = min(best, d)
    if len(pk) == 1:
        best = math.hypot(x_m - pk[0][0] / 100, y_m - pk[0][1] / 100) - pk[0][3] / 200.0
    return best


def frei_vom_wasser(x, y, rad, pk, rand=0.3):
    return abstand_spline_m(x, y, pk) >= rand + rad


def quellfassung(W, I, fall, typ, Q, u, b0, biom, pk_neu, extra=None):
    """Instanzen um den Quellpunkt Q (m) mit Richtung u (hangauf). pk_neu = neuer Kopf (fuer den Wasserabstand).
    Rueckgabe: dict (lagen, brush, decals)."""
    QF = W.R["quellfassung"]
    N = W.R["netze"]
    g = rng(W.R["seed"], fall, typ)
    c = (-u[1], u[0])
    wald = biom in QF["wald_biome"]
    info = {"lagen_wunsch": [], "brush": None, "decals": []}

    def ort(a, cc):
        return Q[0] + a * u[0] + cc * c[0], Q[1] + a * u[1] + cc * c[1]

    def fels(rolle_pal, ziel, x, y, eing=None):
        pal = I.palette(biom, rolle_pal) or I.palette(biom, "stein")
        n = I.waehle(pal, ziel, g)
        e = eing if eing is not None else g.uniform(*QF["eingraben"]["fels"])
        rad = 0.5 * ziel
        for _ in range(6):
            if frei_vom_wasser(x, y, 0.5 * rad, pk_neu):
                break
            x, y = x + 0.5 * u[0], y + 0.5 * u[1]
        I.setze(fall, n, x, y, "fels", ziel_m=ziel, eingraben=e, kipp=1.0, yaw=g.uniform(0, 360))

    def pflanzen(liste, anzahl, rmin, rmax, winkel, rolle, kipp=0.3, ska=(0.8, 1.2), mitte=None, ellip=None):
        for _ in range(anzahl):
            n = liste[g.randrange(len(liste))]
            if ellip is not None:
                (ea, eb, ca) = ellip
                t, rr = g.uniform(0, 2 * math.pi), math.sqrt(g.uniform(0, 1))
                x, y = ort(ca + ea * rr * math.cos(t), eb * rr * math.sin(t))
            else:
                a = math.radians(g.uniform(-winkel, winkel))
                rr = g.uniform(rmin, rmax)
                v = drehe(u, math.degrees(a))
                x, y = Q[0] + rr * v[0], Q[1] + rr * v[1]
            if abstand_spline_m(x, y, pk_neu) < 0.05 and rolle != "binse":
                continue
            if rolle == "binse" and abstand_spline_m(x, y, pk_neu) < 0.0:
                continue
            I.setze(fall, n, x, y, rolle, skala=g.uniform(*ska), eingraben=0.0, kipp=kipp, yaw=g.uniform(0, 360),
                    plus_cm=-QF["eingraben"]["pflanze_cm"], kollision_auto=False)

    if typ in ("hangquelle", "quellmulde", "rheokrene"):
        P = QF["rheokrene"]
        nf = g.randint(*P["felsen"])
        for k in range(nf):
            ziel = g.uniform(*P["haupt_m"]) if k == 0 else g.uniform(*P["neben_m"])
            a = (k / max(nf - 1, 1) - 0.5) * 2 * P["winkel_grad"] if nf > 1 else 0.0
            a += g.uniform(-12, 12)
            rr = g.uniform(*P["radius_m"]) + b0 / 2 + 0.3 * ziel
            v = drehe(u, a)
            fels("block" if k == 0 else "stein", ziel, Q[0] + rr * v[0], Q[1] + rr * v[1])
        pflanzen(N["moos"], g.randint(*P["moos"]), P["moos_radius_m"][0], P["moos_radius_m"][1], 150, "moos")
        if wald:
            pflanzen(N["farn"], g.randint(*P["farn"]), P["farn_radius_m"][0], P["farn_radius_m"][1], 120, "farn")
        lg = dict(P["lagen"])
        info["lagen_wunsch"].append({"form": "kreis", "mitte_cm": [r(Q[0] * 100), r(Q[1] * 100)],
                                     "radius_m": lg.pop("radius_m"), "lagen": lg})
        br = dict(P["brush"])
        info["brush"] = dict(br, mitte_cm=[r((Q[0] + 0.4 * br["laenge_m"] * u[0]) * 100),
                                          r((Q[1] + 0.4 * br["laenge_m"] * u[1]) * 100)],
                             richtung=[r(u[0], 3), r(u[1], 3)])
    elif typ == "felsquelle":
        P = QF["felsquelle"]
        pal = I.palette(biom, "platte") or I.palette(biom, "band")
        ziel = g.uniform(*P["platte_m"])
        x, y = ort(0.45 * ziel + b0 / 2 + 0.2, 0.0)
        n = I.waehle(pal, ziel, g)
        gx, gy, _ = W.inv.netz(n)["groesse_m"]
        yaw = math.degrees(math.atan2(c[1], c[0])) + (0.0 if gx >= gy else 90.0)
        I.setze(fall, n, x, y, "platte", ziel_m=ziel, eingraben=g.uniform(*QF["eingraben"]["platte"]), kipp=1.0,
                yaw=yaw, extra_achse=(c[0], c[1], 0.0), extra_grad=g.uniform(*P["platte_kipp_grad"]))
        for k in range(g.randint(*P["felsen"])):
            seite = 1 if k % 2 == 0 else -1
            zz = g.uniform(*P["neben_m"])
            x, y = ort(g.uniform(0.0, 1.2), seite * (b0 / 2 + 0.6 + 0.5 * zz + g.uniform(0.2, 0.8)))
            fels("stein" if k else "block", zz, x, y)
        pflanzen(N["moos"], g.randint(*P["moos"]), 0.6, 3.0, 140, "moos")
        if wald:
            pflanzen(N["farn"], g.randint(*P["farn"]), 2.0, 4.0, 120, "farn")
        lg = dict(P["lagen"])
        info["lagen_wunsch"].append({"form": "kreis", "mitte_cm": [r(Q[0] * 100), r(Q[1] * 100)],
                                     "radius_m": lg.pop("radius_m"), "lagen": lg})
        x, y = ort(0.2 + b0 / 2, 0.0)
        info["decals"].append({"pfad": P["decal"], "pos_cm": [r(x * 100), r(y * 100), r(W.h(x, y) * 100 + 40)],
                               "groesse_m": [2.0, 1.2], "blick": [r(-u[0], 3), r(-u[1], 3)],
                               "zweck": "Nassstreifen unter der Felsplatte (Bericht 17 nassstreifen_moos)"})
        info["topf_durchmesser_m"] = P["topf_durchmesser_m"]
        if biom in P["sinter_biome"]:
            info["sinter"] = "Sinterbart/Kalktuff als Material-Wunsch (helle, poroese Kruste unter der Platte, Bericht 17 sinter_kalktuff); kein Netz im Inventar"
    elif typ == "sickerquelle":
        P = QF["helokrene"]
        la, lb = g.uniform(*P["flaeche_laenge_m"]), g.uniform(*P["flaeche_breite_m"])
        el = (la / 2, lb / 2, la / 2 - 1.0)
        pflanzen(N["binse"], g.randint(*P["binsen"]), 0, 0, 0, "binse", kipp=0.3, ellip=el)
        pflanzen(N["moos"], g.randint(*P["moos"]), 0, 0, 0, "moos", ellip=el)
        pal = I.palette(biom, "platte") or I.palette(biom, "stein")
        for k in range(g.randint(*P["platten"])):
            x, y = ort(g.uniform(1.0, la - 2.0), g.choice([-1, 1]) * g.uniform(1.0, lb / 2))
            zz = g.uniform(*P["platte_m"])
            n = I.waehle(pal, zz, g)
            I.setze(fall, n, x, y, "platte", ziel_m=zz,
                    eingraben=g.uniform(*QF["eingraben"]["platte"]), kipp=1.0, yaw=g.uniform(0, 360))
        cx, cy = ort(la / 2 - 1.0, 0.0)
        info["lagen_wunsch"].append({"form": "ellipse", "mitte_cm": [r(cx * 100), r(cy * 100)],
                                     "achsen_m": [r(la / 2), r(lb / 2)], "richtung": [r(u[0], 3), r(u[1], 3)],
                                     "lagen": P["lagen"], "zweck": "Quellmoor/Nassflaeche: Wasser sickert flaechig aus"})
    elif typ == "schneetaelchen":
        P = QF["schneetaelchen"]
        a = g.uniform(*P["schnee_abstand_m"])
        x, y = ort(a, 0.0)
        I.setze(fall, N["schnee"][0], x, y, "schnee", skala=g.uniform(*P["schnee_skala"]),
                eingraben=g.uniform(*QF["eingraben"]["schnee"]), kipp=1.0,
                yaw=math.degrees(math.atan2(c[1], c[0])) + g.uniform(-15, 15), kollision_auto=False)
        for k in range(g.randint(*P["steine"])):
            zz = g.uniform(*P["stein_m"])
            v = drehe(u, g.uniform(-100, 100))
            rr = g.uniform(1.0, 2.5) + b0 / 2
            fels("stein", zz, Q[0] + rr * v[0], Q[1] + rr * v[1])
        pflanzen(N["moos"], g.randint(*P["moos"]), 0.5, 3.0, 140, "moos")
        lg = dict(P["lagen"])
        info["lagen_wunsch"].append({"form": "ellipse", "mitte_cm": [r(x * 100), r(y * 100)],
                                     "achsen_m": [lg.pop("laenge_m") / 2, lg.pop("breite_m") / 2],
                                     "richtung": [r(u[0], 3), r(u[1], 3)], "lagen": lg,
                                     "zweck": "Schneerest im Taelchen (Lage Schnee) + Geroell am Austritt"})
    elif typ in ("seeabfluss", "nebenarm"):
        P = QF[typ]
        for k in range(P["bloecke"]):
            seite = 1 if k % 2 == 0 else -1
            zz = g.uniform(*P["block_m"])
            x, y = ort(g.uniform(-0.5, 0.8), seite * (b0 / 2 + 0.5 + 0.5 * zz))
            fels("block", zz, x, y)
        if typ == "seeabfluss":
            pal = I.palette(biom, "platte") or I.palette(biom, "stein")
            for k in range(P["platten"]):
                seite = -1 if k % 2 == 0 else 1
                x, y = ort(g.uniform(-0.3, 0.6), seite * (b0 / 2 + 0.4 + g.uniform(0.3, 0.8)))
                zz = g.uniform(*P["platte_m"])
                I.setze(fall, I.waehle(pal, zz, g), x, y, "platte", ziel_m=zz,
                        eingraben=g.uniform(*QF["eingraben"]["platte"]), kipp=1.0, yaw=g.uniform(0, 360))
            pflanzen(N["moos"], g.randint(*P["moos"]), 0.8, 2.5, 160, "moos")
        lg = dict(P["lagen"])
        info["lagen_wunsch"].append({"form": "kreis", "mitte_cm": [r(Q[0] * 100), r(Q[1] * 100)],
                                     "radius_m": lg.pop("radius_m"), "lagen": lg})
    if extra:
        extra(g, ort, fels, pflanzen, info)
    return info


# ======================================================================================================================
# Faelle
# ======================================================================================================================
def see_kante(W, see, x_m, y_m):
    """naechster Punkt auf dem Seeumriss (m)."""
    um = [(p[0] / 100.0, p[1] / 100.0) for p in see["umriss"]]
    best = (1e18, None)
    for i in range(len(um)):
        a, b = um[i], um[(i + 1) % len(um)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((x_m - a[0]) * dx + (y_m - a[1]) * dy) / L2))
        q = (a[0] + t * dx, a[1] + t * dy)
        d = math.hypot(x_m - q[0], y_m - q[1])
        if d < best[0]:
            best = (d, q)
    return best


def naechstes_fliess(W, gid, x_m, y_m):
    """(abstand_rand_m, id, punkt_cm) des naechsten anderen Fliessgewaessers (Mittellinie - halbe Breite)."""
    best = (1e18, None, None)
    for oid in sorted(W.splines):
        if oid == gid or oid in W.ersetzt:
            continue
        pk = W.splines[oid]
        a = np.array(pk)
        d = np.hypot(a[:, 0] / 100 - x_m, a[:, 1] / 100 - y_m) - a[:, 3] / 200
        i = int(np.argmin(d))
        if d[i] < best[0]:
            best = (float(d[i]), oid, pk[i])
    return best


def plane_e(W, I, g):
    gid = g["id"]
    A = g["anfang"]
    K = W.R["klassifizierung"]
    biom = biom_norm(W, A["biom"])
    ein = W.R["einzelfaelle"].get(gid)
    fall = {"id": gid, "gewaesser": W.gewaesser_von.get(gid), "art": g["art"], "feld": A["feld"], "biom": biom,
            "breite_alt_m": A["breite_m"], "spiegel_alt_m": A["spiegel_m"],
            "anfang_alt_cm": [r(A["x_cm"]), r(A["y_cm"]), r(A["z_cm"])]}
    if ein and ein["loesung"] in ("karstquelle_trockental", "quellsumpf_see", "karsee", "kaskade_k1"):
        return plane_einzel(W, I, g, fall, ein)
    alt = W.splines.get(gid)
    lokal = None
    if alt is None:
        # SWR_ARM_OST: lokale Ferat-Spline, nicht im Repo -> nur Ort, Typ und Profilvorgabe
        lokal = ein["hinweis"] if ein else "Spline nicht im Repo"
        alt = [[A["x_cm"], A["y_cm"], A["z_cm"], A["breite_m"] * 100, 40.0, 100.0]]
    ist_fluss = g["art"] == "fluss"
    x0, y0 = alt[0][0] / 100, alt[0][1] / 100
    if len(alt) > 1:
        u = einheit(alt[0][0] - alt[1][0], alt[0][1] - alt[1][1])
    else:
        mv = g["mulde_vorschlag"]
        u = einheit(mv["x_cm"] / 100 - x0, mv["y_cm"] / 100 - y0)
    B = sollbreite(alt) if len(alt) > 1 else A["breite_20m_m"]
    gef = abs(A["gefaelle_20m_spline_prozent"]) / 100.0
    neu = []
    typ = None
    grund = ""
    zusatz = {}
    # 1 Seeabfluss
    sn = A.get("see_naechster") or {}
    if sn and sn["abstand_m"] <= K["see_max_m"] and sn["spiegel_m"] >= A["spiegel_m"] + K["see_hoeher_min_m"] \
            and sn["id"] in W.seen:
        d, q = see_kante(W, W.seen[sn["id"]], x0, y0)
        vin = einheit(q[0] - x0, q[1] - y0)
        qin = (q[0] + vin[0] * 1.0, q[1] + vin[1] * 1.0)
        weg = verdichte_m([qin, (x0, y0)], W.R["anfang"]["punktabstand_m"])[:-1]
        zs, z0 = W.seen[sn["id"]]["spiegel_cm"], alt[0][2]
        Ltot = math.hypot(qin[0] - x0, qin[1] - y0)
        ein_max = 0.0
        pts = []
        for (x, y) in weg:
            t = math.hypot(x - x0, y - y0) / max(Ltot, 1e-6)
            z = z0 + t * (zs - z0)
            ein_max = max(ein_max, W.h(x, y) - z / 100.0)
            pts.append([x * 100, y * 100, z])
        if ein_max <= K["see_einschnitt_max_m"]:
            typ, neu = "seeabfluss", pts
            u = einheit(qin[0] - x0, qin[1] - y0)
            grund = "See %s %.0f m entfernt, Spiegel %.2f m ueber dem Anfang; Einschnitt bis %.1f m" % (
                sn["id"], sn["abstand_m"], sn["spiegel_m"] - A["spiegel_m"], ein_max)
            zusatz = {"see": sn["id"], "see_spiegel_cm": r(zs), "einschnitt_max_m": r(ein_max, 2)}
    if typ is None and sn and sn["abstand_m"] <= K["see_max_m"]:
        if sn["spiegel_m"] < A["spiegel_m"] + K["see_hoeher_min_m"]:
            zusatz["see_verworfen"] = "%s %.0f m entfernt liegt %.2f m tiefer als der Anfang: kein Seeabfluss" % (
                sn["id"], sn["abstand_m"], A["spiegel_m"] - sn["spiegel_m"])
        elif sn["id"] in W.seen:
            zusatz["see_verworfen"] = "%s %.0f m entfernt, %.2f m hoeher, aber Einschnitt bis %.1f m (> %.1f m)" % (
                sn["id"], sn["abstand_m"], sn["spiegel_m"] - A["spiegel_m"], ein_max, K["see_einschnitt_max_m"])
    # 2 Nebenarm (Aue)
    if typ is None and biom in K["nebenarm_biome"]:
        d, oid, p = naechstes_fliess(W, gid, x0, y0)
        if oid and d <= K["nebenarm_max_m"] and p[2] >= alt[0][2] + K["nebenarm_hoeher_min_m"] * 100 \
                and p[3] >= alt[0][3] * 0.9:
            weg = verdichte_m([(p[0] / 100, p[1] / 100), (x0, y0)], W.R["anfang"]["punktabstand_m"])[:-1]
            Lt = math.hypot(p[0] / 100 - x0, p[1] / 100 - y0)
            pts = []
            for (x, y) in weg:
                t = math.hypot(x - x0, y - y0) / max(Lt, 1e-6)
                pts.append([x * 100, y * 100, alt[0][2] + t * (p[2] - alt[0][2])])
            typ, neu = "nebenarm", pts
            u = einheit(p[0] / 100 - x0, p[1] / 100 - y0)
            grund = "%s fliesst %.1f m daneben, %.2f m hoeher: Nebenarm/Flutrinne zweigt dort ab" % (
                oid, d, (p[2] - alt[0][2]) / 100)
            zusatz = {"abzweig_von": oid, "abzweig_gewaesser": W.gewaesser_von.get(oid)}
    # 3 Quellmulde
    mv = g.get("mulde_vorschlag")
    if typ is None and mv and mv["richtungen"] >= K["mulde_richtungen_min"] and mv["abstand_m"] <= K["mulde_abstand_max_m"]:
        steig = (mv["boden_m"] - A["spiegel_m"]) / max(mv["abstand_m"], 1e-6)
        if 0 < steig <= K["mulde_steigung_max"]:
            mx, my = mv["x_cm"] / 100, mv["y_cm"] / 100
            weg = verdichte_m([(mx, my), (x0, y0)], W.R["anfang"]["punktabstand_m"])[:-1]
            neu = neue_punkte_z(W, [(x, y, W.h(x, y)) for x, y in weg], alt[0][2])
            typ = "quellmulde"
            u = einheit(mx - x0, my - y0)
            grund = "Quellmulde %d m hangauf (%d/4 Seiten steigen, Steigung %.0f %%): Anfang dorthin verlaengern" % (
                mv["abstand_m"], mv["richtungen"], 100 * steig)
    spur, sgrund = (None, None)
    if typ is None:
        spur, sgrund = spur_hoch(W, x0, y0, u, max(K["hang_laenge_m"], K["schnee_laenge_m"]))
        def anstieg(bis_m):
            pp = [p for k, p in enumerate(spur) if (k + 1) * K["spur_schritt_m"] <= bis_m + 1e-9]
            return (pp[-1][2] - W.h(x0, y0)) if pp else 0.0, pp
        a25, sp25 = anstieg(K["hang_laenge_m"])
        a30, sp30 = anstieg(K["schnee_laenge_m"])
        fels_hang = A.get("fels_hangauf_anteil", 0.0) >= K["fels_hangauf_min"]
        if biom in K["schnee_biome"] and a30 >= K["hang_anstieg_min_m"]:
            typ, sp = "schneetaelchen", sp30
            grund = "Kaltes Biom (%s), Taelchen steigt %.1f m auf %d m: Schneerest als Speicher" % (biom, a30, len(sp30) * 5)
        elif (biom in K["karst_biome"] and a25 >= K["fels_anstieg_min_m"]) or fels_hang or \
                (sgrund == "wand" and len(spur) < int(K["hang_laenge_m"] / K["spur_schritt_m"])):
            typ, sp = "felsquelle", sp25
            grund = "Wasser tritt am Hangfuss unter Fels aus (%s, Anstieg %.1f m, %s)" % (
                biom, a25, "Wand" if sgrund == "wand" else ("Fels hangauf %.0f %%" % (100 * A["fels_hangauf_anteil"]) if fels_hang else "Kalk-Biom"))
        elif a25 >= K["hang_anstieg_min_m"]:
            typ, sp = "hangquelle", sp25
            grund = "Hang steigt %.1f m auf %d m: Rheokrene, Anfang den Talweg hinauf verlaengern" % (a25, len(sp25) * 5)
        else:
            typ, sp = "sickerquelle", []
            grund = "Gelaende flach (Anstieg %.1f m auf 25 m): Helokrene, Wasser sickert flaechig aus (Quellmoor)" % a25
        if sp:
            if typ == "felsquelle" and len(sp) > 3:
                sp = sp[:3]
            sp = glaette(W, (x0, y0), sp)
            neu = neue_punkte_z(W, list(reversed(sp)), alt[0][2])
            if neu:
                u = einheit(neu[0][0] / 100 - (neu[1][0] / 100 if len(neu) > 1 else x0),
                            neu[0][1] / 100 - (neu[1][1] / 100 if len(neu) > 1 else y0))
    b0 = b0_von(W, "rheokrene" if typ in ("hangquelle", "quellmulde") else
                ("helokrene" if typ == "sickerquelle" else typ), B)
    L = laenge_L(W, B, biom, gef, ist_fluss, typ)
    kopf, k = kopf_bauen(W, alt, neu, b0, L, B, ist_fluss)
    Q = (kopf[0][0] / 100, kopf[0][1] / 100)
    if typ in ("seeabfluss", "nebenarm") and len(neu) > 1:
        # Fassung an der Austrittsstelle (Ufer bzw. Abzweig), nicht im See/Fluss
        Q = (neu[1][0] / 100, neu[1][1] / 100)
    qinfo = quellfassung(W, I, gid, typ, Q, u, b0, biom, kopf)
    ext = (bogen([p[:3] for p in neu] + [alt[0][:3]])[-1]) if neu else 0.0
    fall.update({
        "loesung": typ, "begruendung": grund, "massnahme_17": MASSNAHME_17[typ], "quelltyp": QUELLTYP[typ],
        "B_soll_m": r(B, 2), "b0_m": r(b0, 2), "L_m": r(L, 1), "verlaengerung_m": r(ext, 1),
        "anfang_neu_cm": [r(kopf[0][0]), r(kopf[0][1]), r(kopf[0][2])],
        "spline": None if lokal else {"modus": "kopf_ersetzen", "alt_bis_index_exkl": k, "alt_punkte": len(alt),
                                      "punkte": runde_punkte(kopf)},
        "quellfassung": dict(qinfo, mitte_cm=[r(Q[0] * 100), r(Q[1] * 100)], richtung_hangauf=[r(u[0], 3), r(u[1], 3)]),
    })
    if spur is not None:
        fall["spur_hangauf"] = {"grund": sgrund, "punkte": len(spur)}
    fall.update(zusatz)
    if lokal:
        for i in I.von_fall(gid):
            i["lokal"] = True
        fall["lokal"] = lokal + "; Instanzen nur hier im Plan, nicht unter instanzen/ (C2 ist Ferats p2-Gebiet)"
        fall["profil_vorgabe"] = {"b0_m": r(b0, 2), "L_m": r(L, 1), "B_m": r(B, 2),
                                  "regel": "Breite = b0 + (B - b0) * (s/L)^0,8; Tiefe = max(0,10; min(Soll; Breite/4))"}
    return fall


MASSNAHME_17 = {"hangquelle": "oberlauf_ergaenzen", "quellmulde": "oberlauf_ergaenzen", "felsquelle": "quellaustritt_felswand",
                "sickerquelle": "karsee_moor_oberhalb", "schneetaelchen": "schneefeld_oberhalb", "seeabfluss": "see_speicher",
                "nebenarm": "zufluss_aus_fluss", "karstquelle_trockental": "quellaustritt_felswand",
                "quellsumpf_see": "karsee_moor_oberhalb", "karsee": "karsee_moor_oberhalb", "kaskade_k1": "oberlauf_ergaenzen"}
QUELLTYP = {"hangquelle": "Rheokrene (Sturz-/Fliessquelle)", "quellmulde": "Rheokrene in Quellmulde",
            "felsquelle": "Schicht-/Karstquelle unter Felsplatte", "sickerquelle": "Helokrene (Sicker-/Sumpfquelle, Quellmoor)",
            "schneetaelchen": "Schmelzwasser aus Schneerest", "seeabfluss": "Seeabfluss (Lippe)",
            "nebenarm": "Nebenarm/Flutrinne aus dem Fluss", "karstquelle_trockental": "Limnokrene (Karst-Quelltopf) unter Trockental",
            "quellsumpf_see": "Quellsumpf (Helokrene gross) mit Sumpfsee", "karsee": "Karsee unter der Karwand",
            "kaskade_k1": "Fortsetzung ueber Kaskade (Schlucht)"}


# ---------------------------------------------------------------- Einzelfaelle
def see_statistik(W, umriss_cm, spiegel_cm):
    xs = [p[0] / 100 for p in umriss_cm]
    ys = [p[1] / 100 for p in umriss_cm]
    zell = W.w.zelle_m
    poly = [(p[0] / 100, p[1] / 100) for p in umriss_cm]
    ab, unter, n = [], 0, 0
    x = math.floor(min(xs))
    while x <= max(xs):
        y = math.floor(min(ys))
        while y <= max(ys):
            if punkt_in_polygon(x, y, poly):
                h = W.h(x, y)
                n += 1
                ab.append(h - spiegel_cm / 100)
                unter += h < spiegel_cm / 100
            y += zell
        x += zell
    ab.sort()
    return {"flaeche_m2": r(flaeche(poly), 0), "abtrag_max_m": r(max(ab), 2) if ab else 0.0,
            "abtrag_p90_m": r(ab[int(0.9 * (len(ab) - 1))], 2) if ab else 0.0,
            "tiefe_max_m": r(-min(ab), 2) if ab else 0.0,
            "anteil_gelaende_unter_spiegel": r(unter / max(n, 1), 2)}


def becken_flaeche(W, x0, y0, u, spiegel_m, graben_max_m, radius_m, flaeche_max_m2, hinten_m=-5.0):
    """Zellen (2 m bzw. 1 m) verbunden mit dem Anfang, Gelaende <= Spiegel + graben_max, im Radius, nicht flussab
    (Abstand entlang u >= hinten_m); die naechsten bis flaeche_max. Rueckgabe (huelle [(x, y)], flaeche_zellen_m2)."""
    zell = W.w.zelle_m
    start = (round(x0 / zell) * zell, round(y0 / zell) * zell)
    offen, gesehen, zellen = [start], {start}, []
    while offen:
        p = offen.pop()
        if math.hypot(p[0] - x0, p[1] - y0) > radius_m:
            continue
        if (p[0] - x0) * u[0] + (p[1] - y0) * u[1] < hinten_m:
            continue
        if W.h(p[0], p[1]) > spiegel_m + graben_max_m:
            continue
        zellen.append(p)
        for dx, dy in ((zell, 0), (-zell, 0), (0, zell), (0, -zell)):
            q = (round(p[0] + dx, 3), round(p[1] + dy, 3))
            if q not in gesehen:
                gesehen.add(q)
                offen.append(q)
    zellen.sort(key=lambda p: (math.hypot(p[0] - x0, p[1] - y0), p))
    zellen = zellen[:int(flaeche_max_m2 / (zell * zell))]
    return huelle([(round(x, 2), round(y, 2)) for x, y in zellen]), len(zellen) * zell * zell


def plane_einzel(W, I, g, fall, ein):
    gid = g["id"]
    A = g["anfang"]
    alt = W.splines[gid]
    biom = fall["biom"]
    x0, y0 = alt[0][0] / 100, alt[0][1] / 100
    u = einheit(alt[0][0] - alt[1][0], alt[0][1] - alt[1][1])
    c = (-u[1], u[0])
    B = sollbreite(alt)
    typ = ein["loesung"]
    fall["loesung"] = typ
    fall["massnahme_17"] = MASSNAHME_17[typ]
    fall["quelltyp"] = QUELLTYP[typ]
    gg = rng(W.R["seed"], gid, typ)
    if typ == "kaskade_k1":
        fall["begruendung"] = ("Beginnt 570 m unter dem Ende von F_HAUPTFLUSS_2 (198,4 m) und 156 m tiefer: Kaskade K1 "
                               "schliesst die Strecke; der Anfang ist dann eine Fortsetzung (Plan unter 'kaskade_k1').")
        fall["spline"] = None
        fall["siehe"] = "kaskade_k1"
        return fall
    zs = alt[0][2] + 5.0
    if typ in ("karstquelle_trockental", "quellsumpf_see"):
        a_m, b_m = ein["see_durchmesser_m"]
        cx, cy = x0 + ein["see_versatz_m"] * u[0], y0 + ein["see_versatz_m"] * u[1]
        # Halbachse entlang u = b_m/2 (laengs), quer a_m/2
        um = ellipse(cx * 100, cy * 100, u[0], u[1], b_m / 2, a_m / 2)
        if ein.get("graben_max_m") is not None:
            poly, _ = becken_flaeche(W, x0, y0, u, zs / 100, ein["graben_max_m"], ein["radius_m"], ein["flaeche_max_m2"])
            um = [[r(x * 100), r(y * 100)] for x, y in poly]
        see = {"id": "S_NEU_" + gid, "zweck": QUELLTYP[typ], "spiegel_cm": r(zs), "umriss": um,
               "water_body": "WaterBodyLake", "brush": "Water-Brush Blend Min (Becken graben, Rand natuerlich)"}
        see.update(see_statistik(W, um, zs))
        fall["see_neu"] = see
        b0 = ein["b0_anteil"] * B
        L = ein["L_m"]
        kopf, k = kopf_bauen(W, alt, [], b0, L, B, True)
        fall.update({"B_soll_m": r(B, 2), "b0_m": r(b0, 2), "L_m": L, "verlaengerung_m": 0.0,
                     "anfang_neu_cm": [r(kopf[0][0]), r(kopf[0][1]), r(kopf[0][2])],
                     "spline": {"modus": "kopf_ersetzen", "alt_bis_index_exkl": k, "alt_punkte": len(alt),
                                "punkte": runde_punkte(kopf)}})
        rand = b_m / 2  # Abstand Mitte -> oberer Rand entlang u
        if typ == "karstquelle_trockental":
            fall["begruendung"] = ("51 m breiter Fluss im Canyonkopf, Gelaende flach, oberhalb ein trockenes Tal: wie "
                                   "Fontaine de Vaucluse/Loue-Quelle tritt der Fluss in einem Karst-Quelltopf am Fuss der "
                                   "Wand aus; das Tal darueber bleibt trocken (Trockental, Hochwasserbett).")
            sp, sg = spur_hoch(W, cx + rand * u[0], cy + rand * u[1], u, ein["trockental_m"], wand_stop=False, kegel=45)
            fall["trockental"] = {"punkte_cm": [[r(x * 100), r(y * 100), r(h * 100)] for x, y, h in sp],
                                  "breite_m": ein["trockental_breite_m"], "grund": sg,
                                  "lagen": {"Geroell": 45, "Kies": 35, "Trockengras": 20},
                                  "zweck": "trockenes Hochwasserbett oberhalb des Quelltopfs (Lagenband, keine Spline)"}
            # Felsen am oberen Topfrand (Austritt) + Platten
            for kk in range(ein["felsen"]):
                a = (kk / max(ein["felsen"] - 1, 1) - 0.5) * 140.0 + gg.uniform(-8, 8)
                v = drehe(u, a)
                rr = (rand if abs(a) < 30 else 0.8 * rand) + gg.uniform(1.5, 4.0)
                pal = I.palette(biom, "block")
                zz = gg.uniform(1.8, 3.5)
                I.setze(gid, I.waehle(pal, zz, gg), cx + rr * v[0], cy + rr * v[1], "fels",
                        ziel_m=zz, eingraben=gg.uniform(0.35, 0.5), kipp=1.0, yaw=gg.uniform(0, 360))
            pal = I.palette(biom, "platte") or I.palette(biom, "band")
            for kk in range(ein["platten"]):
                x, y = cx + (rand + 1.0) * u[0] + (kk - 0.5) * 6 * c[0], cy + (rand + 1.0) * u[1] + (kk - 0.5) * 6 * c[1]
                zz = gg.uniform(3.0, 4.0)
                I.setze(gid, I.waehle(pal, zz, gg), x, y, "platte", ziel_m=zz,
                        eingraben=0.4, kipp=1.0, yaw=gg.uniform(0, 360))
            for kk in range(ein["moos"]):
                v = drehe(u, gg.uniform(-80, 80))
                rr = rand + gg.uniform(0.5, 5.0)
                I.setze(gid, W.R["netze"]["moos"][gg.randrange(5)], cx + rr * v[0], cy + rr * v[1], "moos",
                        skala=gg.uniform(0.8, 1.2), kipp=0.3, yaw=gg.uniform(0, 360), plus_cm=-3, kollision_auto=False)
            fall["decals"] = [{"pfad": W.R["quellfassung"]["felsquelle"]["decal"],
                               "pos_cm": [r((cx + (rand + 1.5) * u[0]) * 100), r((cy + (rand + 1.5) * u[1]) * 100),
                                          r(W.h(cx + (rand + 1.5) * u[0], cy + (rand + 1.5) * u[1]) * 100 + 80)],
                               "groesse_m": [6.0, 3.0], "blick": [r(-u[0], 3), r(-u[1], 3)],
                               "zweck": "Nassstreifen an der Wand ueber dem Quelltopf"}]
            fall["sinter"] = "Topf tiefblau (tiefe Mitte), heller Kalk-/Sinterrand am Austritt (Material-Wunsch)"
        else:
            fall["begruendung"] = ("49 m breiter Fluss beginnt flach im Sumpf; noerdlich faellt das Land auf 2 m ab, ein "
                                   "Oberlauf ist dort nicht moeglich. Glaubwuerdig ist ein Quellsumpf: flaechig "
                                   "austretendes Wasser sammelt sich in einem flachen Sumpfsee, aus dem der Fluss abfliesst. "
                                   "Der Teich T_3313_789 liegt 5 m tiefer und taugt nicht als Quelle.")
            poly = [(p[0] / 100, p[1] / 100) for p in um]
            mx = sum(p[0] for p in poly) / len(poly)
            my = sum(p[1] for p in poly) / len(poly)

            def randpunkt(aussen):
                k = gg.randrange(len(poly))
                a, b = poly[k], poly[(k + 1) % len(poly)]
                t = gg.uniform(0, 1)
                x, y = a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
                v = einheit(x - mx, y - my)
                d = gg.uniform(*aussen)
                return x + v[0] * d, y + v[1] * d
            for kk in range(ein["binsen"]):
                x, y = randpunkt((0.5, 5.0))
                I.setze(gid, W.R["netze"]["binse"][gg.randrange(3)], x, y, "binse", skala=gg.uniform(0.9, 1.3),
                        kipp=0.3, yaw=gg.uniform(0, 360), plus_cm=-3, kollision_auto=False)
            for kk in range(ein["moos"]):
                x, y = randpunkt((0.5, 2.5))
                I.setze(gid, W.R["netze"]["moos"][gg.randrange(5)], x, y, "moos", skala=gg.uniform(0.8, 1.2),
                        kipp=0.3, yaw=gg.uniform(0, 360), plus_cm=-3, kollision_auto=False)
            saum = [[r((mx + 1.3 * (x - mx)) * 100), r((my + 1.3 * (y - my)) * 100)] for x, y in poly]
            fall["lagen_wunsch"] = [{"form": "polygon", "umriss_cm": saum,
                                     "lagen": {"Schlamm": 45, "Moos": 30, "Gras": 25},
                                     "zweck": "Sumpfsaum um den See (Umriss x 1,3)"}]
            fall["hinweis_bewuchs"] = "Sumpfzypresse/Seerose aus den Downloads vom 11.10. nur, wenn im Inventar (heute nicht gelistet)"
        return fall
    if typ == "karsee":
        # Flaeche: verbundene Zellen <= Spiegel + graben_max, hangauf-Seite, Radius
        poly, _ = becken_flaeche(W, x0, y0, u, zs / 100, ein["graben_max_m"], ein["radius_m"], ein["flaeche_max_m2"])
        um = [[r(x * 100), r(y * 100)] for x, y in poly]
        varianten = []
        for gm in ein.get("graben_varianten_m", []):
            pv, fz = becken_flaeche(W, x0, y0, u, zs / 100, gm, ein["radius_m"], 1e9)
            varianten.append({"graben_max_m": gm, "flaeche_m2": r(fz, 0), "huelle_m2": r(flaeche(pv), 0)})
        fall["karsee_varianten"] = varianten
        see = {"id": "S_NEU_KARSEE_K1", "zweck": "Karsee am Fuss der Karwand (Speicher fuer WF_K1, Bericht 17 Rueckfrage 3)",
               "spiegel_cm": r(zs), "umriss": um, "water_body": "WaterBodyLake",
               "brush": "Water-Brush Blend Min bis %.1f m tief graben; Schwelle zum Stummel natuerlich lassen" % ein["graben_max_m"]}
        see.update(see_statistik(W, um, zs))
        fall["see_neu"] = see
        Bn = min(B, ein["b_soll_m"])
        b0 = ein["b0_anteil"] * Bn
        # ganzer Stummel auf Bn; Kopf = Seeabfluss
        neu_alt = [[p[0], p[1], p[2], min(p[3], Bn * 100), p[4], p[5]] for p in alt]
        kopf, k = kopf_bauen(W, neu_alt, [], b0, W.R["anfang"]["L_m"]["seeabfluss"], Bn, True)
        rest = runde_punkte(neu_alt[k:])
        fall.update({"B_soll_m": r(Bn, 2), "b0_m": r(b0, 2), "L_m": W.R["anfang"]["L_m"]["seeabfluss"], "verlaengerung_m": 0.0,
                     "anfang_neu_cm": [r(kopf[0][0]), r(kopf[0][1]), r(kopf[0][2])],
                     "spline": {"modus": "kopf_ersetzen", "alt_bis_index_exkl": len(alt), "alt_punkte": len(alt),
                                "punkte": runde_punkte(kopf) + rest,
                                "hinweis": "ganzer 30-m-Stummel ersetzt: Breite <= %.1f m (Fallbreite WF_K1)" % ein["b_soll_m"]}})
        fall["begruendung"] = ("21 m breiter 30-m-Stummel am Fuss einer steilen Rinne (Wand 138 m hoch, Bericht 17): kein Tal "
                               "fuer einen Fluss, aber Platz fuer einen kleinen Karsee am Wandfuss. Der See speichert, der "
                               "Stummel wird sein Abfluss (Breite auf die Fallbreite 14,9 m), die Rinne darueber fuehrt "
                               "Faeden/Nassstreifen (Oberlauf aus 17) und Gipfelnebel.")
        o = W.herkunft.get("WF_K1", {}).get("oberlauf")
        if o:
            fall["oberlauf_17"] = {"punkte_cm": o["punkte_cm"], "laenge_m": o["laenge_m"], "hoehe_gewinn_m": o["hoehe_gewinn_m"],
                                   "vorschlag": "kein SWR-Bach (Steigung ~100 %): Faeden/Nassstreifen (MI_Leakage) in der Rinne, "
                                                "optional Bach 0,4-1,5 m nur im unteren flacheren Teil"}
        for kk in range(ein["felsen"]):
            p = poly[gg.randrange(len(poly))]
            v = einheit(p[0] - x0, p[1] - y0)
            x, y = p[0] + v[0] * gg.uniform(1.0, 3.0), p[1] + v[1] * gg.uniform(1.0, 3.0)
            pal = I.palette(biom, "block")
            zz = gg.uniform(1.2, 2.5)
            I.setze(gid, I.waehle(pal, zz, gg), x, y, "fels", ziel_m=zz,
                    eingraben=gg.uniform(0.35, 0.5), kipp=1.0, yaw=gg.uniform(0, 360))
        for kk in range(ein["moos"]):
            p = poly[gg.randrange(len(poly))]
            v = einheit(p[0] - x0, p[1] - y0)
            I.setze(gid, W.R["netze"]["moos"][gg.randrange(5)], p[0] + v[0] * gg.uniform(0.3, 2.0),
                    p[1] + v[1] * gg.uniform(0.3, 2.0), "moos", skala=gg.uniform(0.8, 1.2), kipp=0.3,
                    yaw=gg.uniform(0, 360), plus_cm=-3, kollision_auto=False)
        return fall
    raise ValueError(typ)


# ---------------------------------------------------------------- Kaskade K1
def plane_k1(W, I):
    K = W.R["kaskade_k1"]
    v = W.vorschlaege["F_HAUPTFLUSS_2"]["vorschlag"]
    pk = v["punkte"]
    s = bogen(pk)
    S = s[-1]
    hf2 = W.splines["F_HAUPTFLUSS_2_B4"]
    hf3 = W.splines["F_HAUPTFLUSS_3_C4"]
    b_an, b_ab = hf2[-1][3] / 100, hf3[0][3] / 100
    bs = K["schlucht_breite_m"]

    def breite(sw):
        if sw < K["einlauf_m"]:
            t = sw / K["einlauf_m"]
            return b_an + (bs - b_an) * (0.5 - 0.5 * math.cos(math.pi * t))
        if sw > S - K["auslauf_m"]:
            t = (sw - (S - K["auslauf_m"])) / K["auslauf_m"]
            return bs + (b_ab - bs) * (0.5 - 0.5 * math.cos(math.pi * t))
        return bs

    def z_bei(sw):
        return interp_punkt(pk, s, sw)[2]

    grenzen = [0.0]
    while grenzen[-1] < S - 1e-6:
        nxt = grenzen[-1] + max(10.0, K["becken_laenge_breiten"] * bs)
        if nxt > S - 10.0:
            nxt = S
        grenzen.append(nxt)
    z_start = pk[0][2]
    niveaus = []
    for a, b in zip(grenzen[:-1], grenzen[1:]):
        niveaus.append(z_bei(b))
    niveaus[0] = z_start
    niveaus[-1] = hf3[0][2]
    # Stufen kleiner stufe_min zusammenlegen (Schnelle)
    punkte, stufen = [], []
    z_vor = z_start
    for kb, (a, b) in enumerate(zip(grenzen[:-1], grenzen[1:])):
        zb = niveaus[kb]
        fall_h = (z_vor - zb) / 100.0
        if fall_h >= K["stufe_min_m"]:
            stufen.append({"s_m": r(a, 1), "fall_m": r(fall_h, 2), "oben_cm": r(z_vor), "unten_cm": r(zb)})
            if a > 0:
                p = interp_punkt(pk, s, max(a - 0.5, 0))
                punkte.append([p[0], p[1], z_vor, breite(a) * 100, 0, K["tempo_stufe_cm_s"], "lippe"])
            p = interp_punkt(pk, s, a + 0.5)
            punkte.append([p[0], p[1], zb, breite(a) * 100, 0, K["tempo_becken_cm_s"], "fuss"])
        else:
            zb = z_vor if fall_h < 0 else zb
            p = interp_punkt(pk, s, a)
            punkte.append([p[0], p[1], zb, breite(a) * 100, 0, K["tempo_becken_cm_s"], "becken"])
        n = max(1, int(math.ceil((b - a) / 10.0)))
        for j in range(1, n):
            p = interp_punkt(pk, s, a + (b - a) * j / n)
            punkte.append([p[0], p[1], zb, breite(a + (b - a) * j / n) * 100, 0, K["tempo_becken_cm_s"], "becken"])
        z_vor = zb
    # Ende = Anfang HF3
    punkte.append([hf3[0][0], hf3[0][1], hf3[0][2], hf3[0][3], hf3[0][4], hf3[0][5], "anschluss_hf3"])
    # Luecken > 10 m schliessen (linear)
    dicht = [punkte[0]]
    for q in punkte[1:]:
        p = dicht[-1]
        d = math.hypot(q[0] - p[0], q[1] - p[1]) / 100
        n = int(math.ceil(d / 10.0 - 1e-9))
        for j in range(1, n):
            t = j / n
            dicht.append([p[k] + t * (q[k] - p[k]) for k in range(6)] + ["becken"])
        dicht.append(q)
    punkte = dicht
    # nie steigend
    for i in range(1, len(punkte)):
        punkte[i][2] = min(punkte[i][2], punkte[i - 1][2])
    for p in punkte[:-1]:
        p[4] = min(K["tiefe_becken_m"], p[3] / 100 / 4) * 100
    # Einschnitt
    ein = []
    for p in punkte:
        e = W.h_cm(p[0], p[1]) / 100 - p[2] / 100
        ein.append(e)
    strecken = []
    sp = bogen(punkte)
    cur = None
    for i, e in enumerate(ein):
        if e >= K["einschnitt_markieren_ab_m"]:
            if cur is None:
                cur = [sp[i], sp[i], e]
            cur[1], cur[2] = sp[i], max(cur[2], e)
        elif cur is not None:
            strecken.append(cur)
            cur = None
    if cur:
        strecken.append(cur)
    stufen_sort = sorted(stufen, key=lambda x: (-x["fall_m"], x["s_m"]))
    effekte = []
    for st in stufen_sort[:K["effekte_max_faelle"]]:
        if st["fall_m"] < K["fall_ab_m"]:
            continue
        p0 = interp_punkt(pk, s, max(st["s_m"] - 0.5, 0))
        p1 = interp_punkt(pk, s, st["s_m"] + 2.0)
        effekte.append({"typ": "niagara", "asset": K["niagara_fall"], "pos_cm": [r(p0[0]), r(p0[1]), st["oben_cm"]],
                        "cull_m": K["cull_m"], "zweck": "Fall %.1f m (Lippe)" % st["fall_m"]})
        effekte.append({"typ": "niagara", "asset": K["niagara_fuss"], "pos_cm": [r(p1[0]), r(p1[1]), st["unten_cm"]],
                        "cull_m": K["cull_m"], "zweck": "Aufprall am Fuss"})
    rollen = [p[6] for p in punkte]
    return {
        "id": "K1", "von": "F_HAUPTFLUSS_2_B4 (Ende, 198,4 m)", "nach": "F_HAUPTFLUSS_3_C4 (Anfang, 42,8 m)",
        "weg_quelle": "fluss_sim vorschlaege.json F_HAUPTFLUSS_2 (%s, %.0f m)" % (v["methode"], v["laenge_m"]),
        "laenge_m": r(sp[-1], 1), "hoehe_m": r((punkte[0][2] - punkte[-1][2]) / 100, 2),
        "schlucht_breite_m": bs, "stufen": stufen, "stufen_anzahl": len(stufen),
        "fall_max_m": max([x["fall_m"] for x in stufen] or [0]),
        "einschnitt": {"max_m": r(max(ein), 2), "strecken_ueber_m": K["einschnitt_markieren_ab_m"],
                       "strecken": [[r(a, 1), r(b, 1), r(e, 2)] for a, b, e in strecken],
                       "hinweis": "Gelaende ueber dem Spiegel: dort Schlucht graben (Stempel/Water-Brush), Waende Fels (Felsschalen)"},
        "effekte": effekte,
        "spline": {"gewaesser_lauf": "F_HAUPTFLUSS_2_B4", "modus": "anhaengen",
                   "punkte": runde_punkte([p[:6] for p in punkte]), "rollen": rollen},
        "folge": "F_HAUPTFLUSS_3_C4 beginnt dann als Fortsetzung (kein Quellbau, Breite 47 m bleibt). Im Export werden "
                 "F_HAUPTFLUSS_2 und F_HAUPTFLUSS_3 ein Gewaesser (Name nach Praefix-Regel, voraussichtlich F_HAUPTFLUSS).",
        "swr": "Steilstrecke (156 m auf 590 m): 16g-Eignung 'kaskade_vorschlag' zu erwarten; erst im Bild pruefen, Plan B "
               "Kaskadennetz (13g) nur, wenn die SWR die Becken nicht haelt.",
    }


# ---------------------------------------------------------------- Enden
def plane_ende(W, I, g):
    gid = g["id"]
    E = W.R["enden"]
    alt = W.splines[gid]
    gew = W.gewaesser_von.get(gid)
    s = bogen(alt)
    S = s[-1]
    xe, ye = alt[-1][0] / 100, alt[-1][1] / 100
    biom = W.biom(xe, ye)
    # Gefaelle letzte 30 m (Gelaende)
    p30 = interp_punkt(alt, s, max(S - 30, 0))
    gef = (W.h(p30[0] / 100, p30[1] / 100) - W.h(xe, ye)) / max(min(30, S), 1)
    v = W.vorschlaege.get(gew) or {}
    vv = v.get("vorschlag")
    if vv and math.hypot(vv["punkte"][0][0] - alt[-1][0], vv["punkte"][0][1] - alt[-1][1]) > 100:
        vv = None
    out = {"id": gid, "gewaesser": gew, "feld": g["ende"]["feld"], "biom": biom, "breite_m": r(alt[-1][3] / 100, 2),
           "ende_cm": [r(alt[-1][0]), r(alt[-1][1]), r(alt[-1][2])], "gefaelle_30m": r(gef, 3), "befund": g["ende"]["text"]}
    if gid == "F_HAUPTFLUSS_2_B4":
        out.update({"loesung": "kaskade_k1", "begruendung": "Ende ist der Kopf der Kaskade K1 (Plan 'kaskade_k1')", "spline": None})
        return out
    ok = False
    if vv:
        lang, ein = vv["laenge_m"], vv["einschnitt_max_m"]
        ziel_hoeher = vv.get("ziel_hoeher_cm", 0) > 0
        feucht = biom in E["feucht_biome"]
        ok = (not ziel_hoeher) and ein <= E["einschnitt_max_m"] and (
            lang <= E["anschluss_max_m"] or (feucht and lang <= E["anschluss_feucht_max_m"]))
        out["vorschlag_fluss_sim"] = {"ziel": vv["ziel"], "laenge_m": lang, "einschnitt_max_m": ein,
                                      "ziel_hoeher_cm": vv.get("ziel_hoeher_cm"), "methode": vv["methode"]}
    if ok:
        out.update({"loesung": "anschluss",
                    "begruendung": "fluss_sim-Vorschlag %.0f m bis %s %s, Einschnitt %.2f m: anschliessen (in %s versickert ein Bach nicht)" % (
                        vv["laenge_m"], vv["ziel"]["art"], vv["ziel"]["id"], vv["einschnitt_max_m"], biom),
                    "spline": {"modus": "anhaengen", "punkte": runde_punkte(vv["punkte"][1:])}})
        return out
    # versickern
    B = alt[-1][3] / 100
    Lv = max(E["versickern_laenge_m"][0], min(E["versickern_laenge_m"][1], E["versickern_laenge_breiten"] * B))
    j = len(alt) - 1
    while j > 0 and s[j] > S - Lv:
        j -= 1
    neu = []
    ds = W.R["anfang"]["punktabstand_m"]
    n = max(1, int(math.ceil((S - s[j]) / ds)))
    for k in range(n + 1):
        sw = s[j] + (S - s[j]) * k / n
        p = interp_punkt(alt, s, sw)
        t = (sw - (S - Lv)) / Lv if sw > S - Lv else 0.0
        t = max(0.0, min(1.0, t))
        b = p[3] * (1 - (1 - E["rest_breite_anteil"]) * t)
        tf = p[4] + (E["rest_tiefe_m"] * 100 - p[4]) * t
        vt = p[5] + (W.R["anfang"]["tempo_quelle_cm_s"] - p[5]) * t
        neu.append([p[0], p[1], p[2], b, tf, vt])
    for i in range(1, len(neu)):
        neu[i][2] = min(neu[i][2], neu[i - 1][2])
    u = einheit(alt[-1][0] - alt[-2][0], alt[-1][1] - alt[-2][1])
    c = (-u[1], u[0])
    gg = rng(W.R["seed"], gid, "ende")
    trocken = biom in E["trocken_biome"]
    if trocken:
        art = "endpfanne" if gef < 0 else "trockenbett"
    else:
        art = "schotterfaecher" if gef >= E["faecher_gefaelle_min"] else "moorwiese"
    flaechen = []
    if art == "endpfanne":
        a_m, b_m = 1.5 * B + 6, B + 4
        flaechen.append({"form": "ellipse", "mitte_cm": [r((xe + u[0] * a_m * 0.5) * 100), r((ye + u[1] * a_m * 0.5) * 100)],
                         "achsen_m": [r(a_m), r(b_m)], "richtung": [r(u[0], 3), r(u[1], 3)],
                         "lagen": {"Lehm": 50, "Sand": 30, "Schlamm": 20},
                         "zweck": "Endpfanne (Playa): das Bett endet in einer abflusslosen Senke, Wasser versickert/verdunstet; "
                                  "heller Lehm mit Trockenrissen bzw. Salzkruste (Material-Wunsch)"})
        pal = I.palette(biom, "stein")
        for kk in range(6):
            t = gg.uniform(0, 2 * math.pi)
            x = xe + u[0] * a_m * 0.5 + (a_m * math.cos(t) * u[0] - b_m * math.sin(t) * u[1]) * gg.uniform(0.9, 1.1)
            y = ye + u[1] * a_m * 0.5 + (a_m * math.cos(t) * u[1] + b_m * math.sin(t) * u[0]) * gg.uniform(0.9, 1.1)
            zz = gg.uniform(0.5, 1.0)
            I.setze("ENDE_" + gid, I.waehle(pal, zz, gg), x, y, "fels", ziel_m=zz, eingraben=gg.uniform(0.3, 0.45),
                    kipp=1.0, yaw=gg.uniform(0, 360))
    elif art in ("schotterfaecher", "trockenbett"):
        lf = gg.uniform(*E["faecher_laenge_m"])
        w0, w1 = B, B * gg.uniform(*E["faecher_breite_breiten"])
        poly = [(xe - c[0] * w0 / 2, ye - c[1] * w0 / 2), (xe + c[0] * w0 / 2, ye + c[1] * w0 / 2),
                (xe + u[0] * lf + c[0] * w1 / 2, ye + u[1] * lf + c[1] * w1 / 2),
                (xe + u[0] * lf - c[0] * w1 / 2, ye + u[1] * lf - c[1] * w1 / 2)]
        flaechen.append({"form": "polygon", "umriss_cm": [[r(x * 100), r(y * 100)] for x, y in poly],
                         "lagen": {"Kies": 45, "Geroell": 35, "Sand": 20} if not trocken else {"Geroell": 40, "Sand": 40, "Kies": 20},
                         "zweck": ("Trockenbett (Wadi): Wasser versickert in Sand und Kies, das trockene Bett laeuft weiter"
                                   if trocken else
                                   "Schotterfaecher: Wasser versickert im groben Schotter, trockene Rinnen verzweigen sich")})
        pal = I.palette(biom, "stein")
        pk_k = I.palette(biom, "kiesel")
        for kk in range(gg.randint(*E["faecher_steine"])):
            a = gg.uniform(0.1, 1.0)
            wq = w0 + (w1 - w0) * a
            x = xe + u[0] * lf * a + c[0] * gg.uniform(-wq / 2, wq / 2)
            y = ye + u[1] * lf * a + c[1] * gg.uniform(-wq / 2, wq / 2)
            if kk % 3 == 0 or not pk_k:
                zz = gg.uniform(0.6, 1.2)
                I.setze("ENDE_" + gid, I.waehle(pal, zz, gg), x, y, "fels", ziel_m=zz,
                        eingraben=gg.uniform(0.3, 0.45), kipp=1.0, yaw=gg.uniform(0, 360))
            else:
                I.setze("ENDE_" + gid, pk_k[gg.randrange(len(pk_k))], x, y, "fels", skala=gg.uniform(0.8, 1.5),
                        eingraben=0.3, kipp=1.0, yaw=gg.uniform(0, 360))
    else:
        lm = E["moor_laenge_m"]
        bm = E["moor_breite_breiten"] * B
        cx, cy = xe + u[0] * lm / 2 * 0.8, ye + u[1] * lm / 2 * 0.8
        flaechen.append({"form": "ellipse", "mitte_cm": [r(cx * 100), r(cy * 100)], "achsen_m": [r(lm / 2), r(bm / 2)],
                         "richtung": [r(u[0], 3), r(u[1], 3)], "lagen": {"Moos": 40, "Schlamm": 35, "Gras": 25},
                         "zweck": "Moorwiese: Wasser verteilt sich flaechig und versickert"})
        for kk in range(gg.randint(*E["moor_binsen"])):
            t, rr = gg.uniform(0, 2 * math.pi), math.sqrt(gg.uniform(0, 1))
            x = cx + (lm / 2) * rr * math.cos(t) * u[0] + (bm / 2) * rr * math.sin(t) * c[0]
            y = cy + (lm / 2) * rr * math.cos(t) * u[1] + (bm / 2) * rr * math.sin(t) * c[1]
            if abstand_spline_m(x, y, neu) < 0:
                continue
            I.setze("ENDE_" + gid, W.R["netze"]["binse"][gg.randrange(3)], x, y, "binse", skala=gg.uniform(0.9, 1.3),
                    kipp=0.3, yaw=gg.uniform(0, 360), plus_cm=-3, kollision_auto=False)
        for kk in range(gg.randint(*E["moor_moos"])):
            t, rr = gg.uniform(0, 2 * math.pi), math.sqrt(gg.uniform(0, 1))
            x = cx + (lm / 2) * rr * math.cos(t) * u[0] + (bm / 2) * rr * math.sin(t) * c[0]
            y = cy + (lm / 2) * rr * math.cos(t) * u[1] + (bm / 2) * rr * math.sin(t) * c[1]
            I.setze("ENDE_" + gid, W.R["netze"]["moos"][gg.randrange(5)], x, y, "moos", skala=gg.uniform(0.8, 1.2),
                    kipp=0.3, yaw=gg.uniform(0, 360), plus_cm=-3, kollision_auto=False)
    grund = []
    if vv:
        grund.append("fluss_sim-Vorschlag %.0f m, Einschnitt %.2f m%s" % (
            vv["laenge_m"], vv["einschnitt_max_m"], ", Ziel hoeher" if vv.get("ziel_hoeher_cm", 0) > 0 else ""))
    grund.append("Biom %s, Gefaelle %.1f %%" % (biom, 100 * gef))
    out.update({"loesung": "versickern_" + art, "begruendung": "; ".join(grund),
                "spline": {"modus": "ende_ersetzen", "alt_ab_index": j, "alt_punkte": len(alt),
                           "punkte": runde_punkte(neu)},
                "flaechen": flaechen, "versickern_laenge_m": r(Lv, 1)})
    return out


# ---------------------------------------------------------------- Verjuengung aller Anfaenge (Teil 3)
def verjuengung_alle(W, e_ids):
    out = []
    for gid in sorted(W.gew):
        g = W.gew[gid]
        if gid in e_ids:
            continue
        kl, ua = g["klasse"], g["unterart"]
        alt = W.splines.get(gid)
        ist_fluss = g["art"] == "fluss"
        if kl == "a":
            typ = "seeabfluss"
        elif kl == "c":
            typ = "gletschertor" if ist_fluss else "schneetaelchen"
        elif kl == "d":
            typ = "rheokrene"
        elif kl == "b" and ua == "abzweig":
            typ = "abzweig"
        else:
            continue
        if alt is None:
            out.append({"id": gid, "klasse": kl, "typ": typ, "hinweis": "lokale Spline (p2/Arm), nicht im Repo: Regel gilt, "
                        "Ferats Werkzeug zieht nach", "gewaesser": W.gewaesser_von.get(gid)})
            continue
        biom = biom_norm(W, g["anfang"]["biom"])
        B = sollbreite(alt)
        b0 = b0_von(W, typ, B)
        gef = abs(g["anfang"]["gefaelle_20m_spline_prozent"]) / 100
        L = laenge_L(W, B, biom, gef, ist_fluss, typ)
        s = bogen(alt)
        pts = []
        for i, p in enumerate(alt):
            if s[i] >= L:
                break
            b = max(min(profil(W, s[i], L, b0, B), p[3] / 100), min(b0, p[3] / 100))
            t = tiefe_von(W, b, p[4] / 100, ist_fluss)
            v = tempo_von(W, s[i], L, p[5])
            pts.append([i, r(b * 100), r(t * 100), r(v)])
        out.append({"id": gid, "gewaesser": W.gewaesser_von.get(gid), "klasse": kl, "unterart": ua, "typ": typ,
                    "biom": biom, "B_soll_m": r(B, 2), "b0_m": r(b0, 2), "L_m": r(L, 1),
                    "breite_alt_m": r(alt[0][3] / 100, 2), "punkte": pts})
    return out


# ======================================================================================================================
# Neu backen
# ======================================================================================================================
def neu_backen(W, faelle, k1, enden, verj, I, seen):
    # Bereiche je Gewaesser (Rechteck der Laeufe + halbe Breite + 8 m)
    ber = {}
    for gid, pk in W.splines.items():
        gw = W.gewaesser_von.get(gid)
        if not gw or gid in W.ersetzt:
            continue
        a = np.array(pk)
        hb = a[:, 3].max() / 200 + 8
        x0, x1 = a[:, 0].min() / 100 - hb, a[:, 0].max() / 100 + hb
        y0, y1 = a[:, 1].min() / 100 - hb, a[:, 1].max() / 100 + hb
        if gw in ber:
            b = ber[gw]
            ber[gw] = [min(b[0], x0), min(b[1], y0), max(b[2], x1), max(b[3], y1)]
        else:
            ber[gw] = [x0, y0, x1, y1]
    direkt = {}

    def add(gw, grund):
        if gw:
            direkt.setdefault(gw, set()).add(grund)
    for f in faelle:
        if f.get("spline"):
            add(f["gewaesser"], "Anfang neu (%s)" % f["loesung"])
        if f.get("see_neu"):
            add(f["gewaesser"], "neuer See am Anfang")
    add("F_HAUPTFLUSS_2", "Kaskade K1 angehaengt")
    add("F_HAUPTFLUSS_3", "Kaskade K1 (Anfang wird Fortsetzung)")
    for e in enden:
        if e.get("spline"):
            add(e["gewaesser"], "Ende neu (%s)" % e["loesung"])
    for v in verj:
        if v.get("punkte"):
            add(v["gewaesser"], "Breite/Tiefe am Anfang (%s)" % v["typ"])
    # Nachbarn: neue Punkte, Seen, Instanzen mit Kollision in fremdem Bereich
    orte = []
    for f in faelle:
        if f.get("spline"):
            for p in f["spline"]["punkte"]:
                orte.append((p[0] / 100, p[1] / 100, f["gewaesser"], "neue Splinepunkte von %s" % f["id"]))
    for p in k1["spline"]["punkte"]:
        orte.append((p[0] / 100, p[1] / 100, "F_HAUPTFLUSS_2", "Kaskade K1"))
    for e in enden:
        if e.get("spline"):
            for p in e["spline"]["punkte"]:
                orte.append((p[0] / 100, p[1] / 100, e["gewaesser"], "Ende %s" % e["id"]))
    for s in seen:
        for p in s["umriss"]:
            orte.append((p[0] / 100, p[1] / 100, s.get("gewaesser"), "neuer See %s" % s["id"]))
    for i in I.liste:
        if i["kollision"]:
            orte.append((i["x"] / 100, i["y"] / 100, None, "Fels mit Kollision (%s)" % i["fall"]))
    nachbar = {}
    for gw in sorted(ber):
        b = ber[gw]
        for x, y, eigen, grund in orte:
            if eigen == gw:
                continue
            if b[0] <= x <= b[2] and b[1] <= y <= b[3]:
                nachbar.setdefault(gw, set()).add(grund.split(" (")[0] if "Fels" in grund else grund)
    liste = []
    for gw in sorted(set(direkt) | set(nachbar)):
        liste.append({"gewaesser": gw, "direkt": sorted(direkt.get(gw, [])),
                      "nachbar": sorted(nachbar.get(gw, []))[:6] if gw not in direkt else []})
    return {"anzahl": len(liste), "direkt": len(direkt), "nur_nachbar": len([x for x in liste if not x["direkt"]]),
            "liste": liste,
            "hinweis": "Nachbarn: neue Punkte, neue Seen oder Felsen mit Kollision liegen im Rechteck (Laeufe + halbe Breite "
                       "+ 8 m) eines anderen Gewaessers; dessen Gelaende- bzw. Objektteil des Fingerabdrucks aendert sich, "
                       "sobald gegraben bzw. gesetzt ist. Massgeblich bleibt die Back-Liste des Exports (bereich_cm). "
                       "source_size_cm = Breite am ersten Punkt aendert sich bei jedem neuen Anfang (sim_vorgaben), "
                       "also auch ohne Fingerabdruck-Aenderung neu backen. Sehens-Gewaesser (SW_*) nicht geprueft."}


# ======================================================================================================================
# Ausgabe FORMAT 3
# ======================================================================================================================
def schreibe_format3(W, I, aus, stand):
    R = W.R
    QF = R["quellfassung"]
    je_feld = {}
    for i in I.liste:
        if i.get("lokal"):
            continue
        f = D.feld_von_cm(i["x"], i["y"])
        key = i["netz"] + ("_kol" if i["kollision"] else "")
        je_feld.setdefault(f, {}).setdefault(key, []).append(i)
    basis = os.path.join(aus, "instanzen")
    if os.path.isdir(basis):
        shutil.rmtree(basis)  # nur die eigene Ausgabe: alte Netz-Dateien eines frueheren Laufs entfernen
    dateien_alle = []
    for feld in sorted(je_feld):
        d = os.path.join(basis, feld)
        os.makedirs(d, exist_ok=True)
        plan = {"stand": stand, "feld": feld, "instanzen": 0, "dateien": {},
                "ft_ordner": R["ausgabe"]["ft_ordner"], "ft_praefix": R["ausgabe"]["ft_praefix"],
                "quelle": "Auftrag 19 bach_anfaenge_plan.py (Quellfassungen, Schotterfaecher, Moorwiesen)"}
        for key in sorted(je_feld[feld]):
            liste = je_feld[feld][key]
            buf = bytearray()
            for i in liste:
                buf += struct.pack("<10f", i["x"], i["y"], i["z"], *i["q"], i["s"], i["s"], i["s"])
            with open(os.path.join(d, key + ".f32"), "wb") as fh:
                fh.write(bytes(buf))
            rolle = liste[0]["rolle"]
            sw = QF["sichtweite_cm"].get(rolle, 25000)
            plan["dateien"][key] = {"pfad": liste[0]["pfad"], "anzahl": len(liste), "gruppe": "bach_anfang_" + rolle,
                                    "rolle": rolle, "sichtweite": [0, sw], "schatten": rolle in ("fels", "platte", "schnee", "farn"),
                                    "kollision": bool(liste[0]["kollision"])}
            plan["instanzen"] += len(liste)
            dateien_alle.append(os.path.join("instanzen", feld, key + ".f32"))
        with open(os.path.join(d, "plan.json"), "w", encoding="utf-8") as fh:
            json.dump(plan, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    return sorted(je_feld), dateien_alle


# ======================================================================================================================
# Bilder
# ======================================================================================================================
TYP_FARBE = {  # Referenzpalette (dataviz, hell), feste Reihenfolge
    "hangquelle": (42, 120, 214), "felsquelle": (235, 104, 52), "sickerquelle": (27, 175, 122), "quellmulde": (237, 161, 0),
    "schneetaelchen": (232, 123, 164), "seeabfluss": (0, 131, 0), "nebenarm": (98, 80, 214), "einzelfall": (227, 73, 72)}
TYP_FORM = {"hangquelle": "kreis", "felsquelle": "dreieck", "sickerquelle": "raute", "quellmulde": "quadrat",
            "schneetaelchen": "stern", "seeabfluss": "kreuz", "nebenarm": "dreieck_u", "einzelfall": "kreis_gross"}


def _font(n):
    from PIL import ImageFont
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, n)
    return ImageFont.load_default()


def _marke(dr, x, y, form, farbe, gr=6):
    o = (20, 20, 20)
    if form == "kreis":
        dr.ellipse([x - gr, y - gr, x + gr, y + gr], fill=farbe, outline=o)
    elif form == "kreis_gross":
        dr.ellipse([x - gr - 3, y - gr - 3, x + gr + 3, y + gr + 3], fill=farbe, outline=o, width=2)
    elif form == "quadrat":
        dr.rectangle([x - gr, y - gr, x + gr, y + gr], fill=farbe, outline=o)
    elif form == "dreieck":
        dr.polygon([(x, y - gr - 1), (x - gr, y + gr), (x + gr, y + gr)], fill=farbe, outline=o)
    elif form == "dreieck_u":
        dr.polygon([(x, y + gr + 1), (x - gr, y - gr), (x + gr, y - gr)], fill=farbe, outline=o)
    elif form == "raute":
        dr.polygon([(x, y - gr - 1), (x + gr + 1, y), (x, y + gr + 1), (x - gr - 1, y)], fill=farbe, outline=o)
    elif form == "stern":
        pts = []
        for k in range(10):
            a = math.pi / 2 + k * math.pi / 5
            rr = gr + 2 if k % 2 == 0 else gr / 2
            pts.append((x + rr * math.cos(a), y - rr * math.sin(a)))
        dr.polygon(pts, fill=farbe, outline=o)
    elif form == "kreuz":
        dr.rectangle([x - gr, y - 2, x + gr, y + 2], fill=farbe, outline=o)
        dr.rectangle([x - 2, y - gr, x + 2, y + gr], fill=farbe, outline=o)


def schummer(h, zelle):
    gy, gx = np.gradient(h.astype(np.float64), zelle)
    az, al = math.radians(315), math.radians(45)
    sl = np.arctan(np.hypot(gx, gy) * 1.5)
    asp = np.arctan2(-gx, gy)
    s = np.sin(al) * np.cos(sl) + np.cos(al) * np.sin(sl) * np.cos(az - asp)
    return np.clip(s, 0, 1)


def bild_uebersicht(W, faelle, enden, pfad):
    from PIL import Image, ImageDraw
    h = W.w.hoehe
    st = max(1, int(round(8 / W.w.zelle_m)))
    hs = h[::st, ::st]
    sh = schummer(hs, W.w.zelle_m * st)
    meer = hs < 0
    g = (110 + 120 * sh).astype(np.uint8)
    rgb = np.stack([g, g, g], -1)
    rgb[meer] = (196, 214, 230)
    img = Image.fromarray(rgb, "RGB")
    leg_w = 300
    can = Image.new("RGB", (img.width + leg_w, img.height), (252, 252, 251))
    can.paste(img, (0, 0))
    dr = ImageDraw.Draw(can)
    f, fk = _font(16), _font(13)

    def px(x_cm, y_cm):
        i, j = D.m_zu_pixel(x_cm / 100, y_cm / 100, W.w.zelle_m * st)
        return float(j), float(i)
    zaehl = {}
    for fa in faelle:
        typ = fa["loesung"] if fa["loesung"] in TYP_FARBE else "einzelfall"
        zaehl[typ] = zaehl.get(typ, 0) + 1
        x, y = px(*fa["anfang_alt_cm"][:2])
        _marke(dr, x, y, TYP_FORM[typ], TYP_FARBE[typ])
    for e in enden:
        x, y = px(*e["ende_cm"][:2])
        dr.rectangle([x - 7, y - 7, x + 7, y + 7], outline=(20, 20, 20), width=3)
    x0 = img.width + 16
    dr.text((x0, 14), "Bach-Anfaenge: 83 Faelle", fill=(11, 11, 11), font=f)
    dr.text((x0, 36), "Loesung (Form + Farbe)", fill=(82, 81, 78), font=fk)
    y = 62
    namen = {"hangquelle": "Hangquelle (Rheokrene)", "felsquelle": "Felsquelle", "sickerquelle": "Sickerquelle (Quellmoor)",
             "quellmulde": "Quellmulde", "schneetaelchen": "Schneetaelchen", "seeabfluss": "Seeabfluss",
             "nebenarm": "Nebenarm", "einzelfall": "Einzelfall (grosse Fluesse)"}
    for typ in TYP_FARBE:
        if typ not in zaehl:
            continue
        _marke(dr, x0 + 8, y + 8, TYP_FORM[typ], TYP_FARBE[typ])
        dr.text((x0 + 24, y), "%s: %d" % (namen[typ], zaehl[typ]), fill=(11, 11, 11), font=fk)
        y += 24
    dr.rectangle([x0 + 1, y + 2, x0 + 15, y + 16], outline=(20, 20, 20), width=3)
    dr.text((x0 + 24, y), "versickerndes Ende: %d" % len(enden), fill=(11, 11, 11), font=fk)
    dr.text((x0, can.height - 40), "Schummerung 8 m, Norden oben", fill=(82, 81, 78), font=fk)
    can.save(pfad, optimize=True)


def bild_regel(W, pfad):
    from PIL import Image, ImageDraw
    Wd, Hd = 900, 620
    img = Image.new("RGB", (Wd, Hd), (252, 252, 251))
    dr = ImageDraw.Draw(img)
    f, fk = _font(16), _font(13)
    B = 4.0
    kurven = [("Hang-/Sickerquelle, Aue", "rheokrene", "aue", 0), ("Hangquelle, Tundra", "rheokrene", "tundra", 1),
              ("Felsquelle, Dschungel", "felsquelle", "dschungel", 2), ("Seeabfluss", "seeabfluss", "aue", 6)]
    farben = [(42, 120, 214), (235, 104, 52), (27, 175, 122), (0, 131, 0)]
    pan = [(70, 60, 860, 290, "Breite (m)", 0, 4.5), (70, 350, 860, 560, "Tiefe (m)", 0, 0.5)]
    for (x0, y0, x1, y1, tit, lo, hi) in pan:
        dr.line([(x0, y1), (x1, y1)], fill=(120, 120, 120))
        dr.line([(x0, y0), (x0, y1)], fill=(120, 120, 120))
        dr.text((x0, y0 - 24), tit, fill=(11, 11, 11), font=f)
        for k in range(5):
            v = lo + (hi - lo) * k / 4
            yy = y1 - (y1 - y0) * k / 4
            dr.line([(x0, yy), (x1, yy)], fill=(232, 232, 230))
            dr.text((x0 - 44, yy - 8), "%.2f" % v if hi < 1 else "%.1f" % v, fill=(82, 81, 78), font=fk)
        for k in range(0, 81, 10):
            xx = x0 + (x1 - x0) * k / 80
            dr.text((xx - 8, y1 + 4), "%d" % k, fill=(82, 81, 78), font=fk)
    dr.text((440, 590), "Abstand vom Anfang s (m)", fill=(82, 81, 78), font=fk)
    for (name, typ, biom, _), col in zip(kurven, farben):
        b0 = b0_von(W, typ, B)
        L = laenge_L(W, B, biom, 0.05, False, typ)
        for pi, (x0, y0, x1, y1, tit, lo, hi) in enumerate(pan):
            pts = []
            for k in range(0, 801):
                s = k / 10
                b = profil(W, s, L, b0, B)
                v = b if pi == 0 else tiefe_von(W, b, 0.32, False)
                pts.append((x0 + (x1 - x0) * s / 80, y1 - (y1 - y0) * (v - lo) / (hi - lo)))
            dr.line(pts, fill=col, width=2)
    # Legende unten rechts im Breiten-Panel (dort laufen keine Kurven)
    lx, ly = 560, 175
    for k, ((name, typ, biom, _), col) in enumerate(zip(kurven, farben)):
        L = laenge_L(W, B, biom, 0.05, False, typ)
        dr.line([(lx, ly + 9 + 20 * k), (lx + 26, ly + 9 + 20 * k)], fill=col, width=3)
        dr.text((lx + 32, ly + 20 * k), "%s: b0 %.1f m, L %.0f m" % (name, b0_von(W, typ, B), L), fill=(11, 11, 11), font=fk)
    dr.text((70, 4), "Breiten- und Tiefenprofil am Anfang (Sollbreite 4 m; Tiefe = max(0,10; min(0,40; Breite/4)))",
            fill=(11, 11, 11), font=f)
    img.save(pfad, optimize=True)


def bild_skizze(W, I, titel, mitte_m, fenster_m, alt_pk, neu_pk, seen, flaechen, fall_ids, pfad, profil_daten=None):
    from PIL import Image, ImageDraw
    pxm = W.R["ausgabe"]["bild_px_je_m"] if fenster_m <= 120 else max(1, int(540 / fenster_m))
    N = int(fenster_m * pxm)
    cx, cy = mitte_m
    xs = cx - fenster_m / 2 + (np.arange(N) + 0.5) / pxm
    ys = cy - fenster_m / 2 + (np.arange(N) + 0.5) / pxm
    XX, YY = np.meshgrid(xs, ys)
    H = W.w.bilinear(W.w.hoehe, XX, YY)
    sh = schummer(H, 1.0 / pxm)
    g = (95 + 135 * sh).astype(np.uint8)
    rgb = np.stack([(g * 0.95).astype(np.uint8), g, (g * 0.9).astype(np.uint8)], -1)
    img = Image.fromarray(rgb, "RGB")
    seite = 380
    can = Image.new("RGB", (N + seite, max(N, 560)), (252, 252, 251))
    dr = ImageDraw.Draw(img, "RGBA")
    f, fk = _font(15), _font(12)

    def P(x_m, y_m):
        return ((x_m - (cx - fenster_m / 2)) * pxm, (y_m - (cy - fenster_m / 2)) * pxm)

    def band(pk, fuell, rand):
        if len(pk) < 2:
            return
        li, re_ = [], []
        for i, p in enumerate(pk):
            a = pk[max(i - 1, 0)]
            b = pk[min(i + 1, len(pk) - 1)]
            t = einheit(b[0] - a[0], b[1] - a[1])
            n = (-t[1], t[0])
            hb = p[3] / 200
            li.append(P(p[0] / 100 + n[0] * hb, p[1] / 100 + n[1] * hb))
            re_.append(P(p[0] / 100 - n[0] * hb, p[1] / 100 - n[1] * hb))
        poly = li + list(reversed(re_))
        dr.polygon(poly, fill=fuell, outline=rand)
    for s in seen:
        dr.polygon([P(p[0] / 100, p[1] / 100) for p in s["umriss"]], fill=(58, 120, 200, 150), outline=(20, 60, 120, 255))
    for fl in flaechen:
        if fl["form"] == "polygon":
            pts = [P(p[0] / 100, p[1] / 100) for p in fl["umriss_cm"]]
        elif fl["form"] == "kreis":
            mx, my = fl["mitte_cm"][0] / 100, fl["mitte_cm"][1] / 100
            pts = [P(mx + fl["radius_m"] * math.cos(t), my + fl["radius_m"] * math.sin(t))
                   for t in np.linspace(0, 2 * math.pi, 40)]
        elif fl["form"] == "ellipse":
            mx, my = fl["mitte_cm"][0] / 100, fl["mitte_cm"][1] / 100
            a, b = fl["achsen_m"]
            ux, uy = fl["richtung"]
            pts = [P(mx + a * math.cos(t) * ux - b * math.sin(t) * uy, my + a * math.cos(t) * uy + b * math.sin(t) * ux)
                   for t in np.linspace(0, 2 * math.pi, 48)]
        elif fl["form"] == "linie":
            pts = [P(p[0] / 100, p[1] / 100) for p in fl["punkte_cm"]]
            if len(pts) > 1:
                dr.line(pts, fill=(150, 110, 60, 255), width=max(2, int(fl.get("breite_m", 4) * pxm)))
            continue
        dr.polygon(pts, fill=(140, 110, 60, 60), outline=(120, 90, 40, 255))
    band(alt_pk, (255, 255, 255, 40), (40, 40, 40, 255))
    band(neu_pk, (42, 120, 214, 170), (20, 60, 120, 255))
    farbe = {"fels": (70, 70, 70, 255), "platte": (120, 110, 100, 255), "moos": (60, 130, 50, 255),
             "farn": (30, 100, 40, 255), "binse": (150, 160, 60, 255), "schnee": (250, 250, 255, 255)}
    for i in I.liste:
        if i["fall"] not in fall_ids:
            continue
        x, y = P(i["x"] / 100, i["y"] / 100)
        rr = max(2.0, 0.5 * i["groesse_m"] * pxm) if i["rolle"] in ("fels", "platte", "schnee") else 2.0
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=farbe[i["rolle"]], outline=(0, 0, 0, 255))
    # Massstab
    mst = 10 if fenster_m <= 150 else 50
    dr.line([(10, N - 14), (10 + mst * pxm, N - 14)], fill=(0, 0, 0, 255), width=3)
    dr.text((12, N - 32), "%d m" % mst, fill=(0, 0, 0, 255), font=fk)
    can.paste(img, (0, 0))
    dr = ImageDraw.Draw(can, "RGBA")
    x0 = N + 14
    zeilen = titel.split("\n")
    dr.text((x0, 10), zeilen[0], fill=(11, 11, 11, 255), font=f)
    yy = 32
    for z in zeilen[1:]:
        dr.text((x0, yy), z, fill=(82, 81, 78, 255), font=fk)
        yy += 16
    yy += 6
    leg = [((255, 255, 255), "alte Spline (Band)"), ((42, 120, 214), "neue Spline (Band = Breite)"),
           ((58, 120, 200), "neuer See"), ((140, 110, 60), "Lagen-Wunsch / Flaeche"), ((70, 70, 70), "Fels"),
           ((120, 110, 100), "Felsplatte"), ((60, 130, 50), "Moos"), ((30, 100, 40), "Farn"), ((150, 160, 60), "Binse"),
           ((250, 250, 255), "Schnee")]
    for col, txt in leg:
        dr.rectangle([x0, yy + 2, x0 + 12, yy + 14], fill=col + (255,), outline=(0, 0, 0, 255))
        dr.text((x0 + 18, yy), txt, fill=(11, 11, 11, 255), font=fk)
        yy += 18
    if profil_daten:
        # Breitenprofil (eine Achse: Breite in m) alt gestrichelt-grau, neu blau
        px0, py0, px1, py1 = x0 + 34, yy + 34, x0 + seite - 30, yy + 34 + 150
        alt_s, alt_b, neu_s, neu_b = profil_daten
        smax = max(max(neu_s), max(alt_s), 1.0)
        bmax = max(max(alt_b), max(neu_b), 0.5) * 1.1
        dr.text((x0, yy + 8), "Breite (m) ueber s (m)", fill=(11, 11, 11, 255), font=fk)
        dr.line([(px0, py1), (px1, py1)], fill=(120, 120, 120, 255))
        dr.line([(px0, py0), (px0, py1)], fill=(120, 120, 120, 255))
        for k in range(3):
            v = bmax * k / 2
            yv = py1 - (py1 - py0) * k / 2
            dr.text((px0 - 30, yv - 7), "%.1f" % v, fill=(82, 81, 78, 255), font=fk)
        dr.text((px0, py1 + 4), "0", fill=(82, 81, 78, 255), font=fk)
        dr.text((px1 - 24, py1 + 4), "%.0f" % smax, fill=(82, 81, 78, 255), font=fk)

        def lin(ss, bb, col):
            pts = [(px0 + (px1 - px0) * s / smax, py1 - (py1 - py0) * b / bmax) for s, b in zip(ss, bb)]
            if len(pts) > 1:
                dr.line(pts, fill=col, width=2)
        lin(alt_s, alt_b, (150, 150, 150, 255))
        lin(neu_s, neu_b, (42, 120, 214, 255))
        dr.text((px0 + 6, py1 + 20), "grau alt, blau neu", fill=(82, 81, 78, 255), font=fk)
    can.save(pfad, optimize=True)


# ======================================================================================================================
# Hauptlauf
# ======================================================================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for k in ("regeln", "befund", "welt", "vorschlaege", "zonen", "ersetzt", "herkunft", "fels", "aus"):
        ap.add_argument("--" + k, default=STD[k])
    ap.add_argument("--daten1m", default=None)
    ap.add_argument("--bild", action="store_true")
    args = ap.parse_args()
    W = Welt(args)
    I = Instanzen(W)
    stand = W.R["stand"]
    e_faelle = [g for g in W.befund["gewaesser"] if g["klasse"] == "e"]
    e_faelle.sort(key=lambda g: (-g["anfang"]["breite_m"], g["id"]))
    for gid in W.ersetzt:
        if any(g["id"] == gid for g in e_faelle):
            raise SystemExit("ersetzter Lauf unter den e-Faellen: %s" % gid)
    faelle = [plane_e(W, I, g) for g in e_faelle]
    k1 = plane_k1(W, I)
    enden_g = sorted([g for g in W.befund["gewaesser"] if g["ende"]["klasse"] == "nichts"],
                     key=lambda g: (-g["ende"]["breite_m"], g["id"]))
    enden = [plane_ende(W, I, g) for g in enden_g]
    verj = verjuengung_alle(W, set(g["id"] for g in e_faelle))
    seen = []
    for f in faelle:
        if f.get("see_neu"):
            s = dict(f["see_neu"])
            s["gewaesser"] = f["gewaesser"]
            seen.append(s)
    # Instanzen je Fall in die Faelle schreiben
    for f in faelle + enden:
        fid = f["id"] if f in faelle else "ENDE_" + f["id"]
        li = I.von_fall(fid)
        f["instanzen"] = [[i["netz"] + ("_kol" if i["kollision"] else ""), r(i["x"]), r(i["y"]), r(i["z"]),
                           r(i["q"][0], 5), r(i["q"][1], 5), r(i["q"][2], 5), r(i["q"][3], 5), r(i["s"], 4)]
                          for i in li]
        f["instanzen_anzahl"] = len(li)
        f["akteure"] = 0
    backen = neu_backen(W, faelle, k1, enden, verj, I, seen)
    os.makedirs(args.aus, exist_ok=True)
    felder, dateien = schreibe_format3(W, I, args.aus, stand)
    zl = {}
    for f in faelle:
        zl[f["loesung"]] = zl.get(f["loesung"], 0) + 1
    ze = {}
    for e in enden:
        ze[e["loesung"]] = ze.get(e["loesung"], 0) + 1
    netze = {}
    for i in I.liste:  # auch lokale (fuer den Pruefer)
        k = i["netz"] + ("_kol" if i["kollision"] else "")
        if k not in netze:
            netze[k] = {"pfad": i["pfad"], "rolle": i["rolle"], "kollision": i["kollision"], "anzahl": 0}
        netze[k]["anzahl"] += 1
    plan = {
        "format": FORMAT, "stand": stand, "auftrag": "recherche/auftraege/19-bach-anfaenge-quellen.md (Fassung 652af24)",
        "regeln": "skripte/bach_anfaenge/bach_anfaenge_regeln.json (Version %d)" % W.R["version"],
        "eingaben": {"befund": "auftraege/daten/bach_anfaenge/bach_anfaenge.json (83 e, 8 Enden versickert)",
                     "splines": "vorlagen/daten/sehens/wasser_welt.json + baeche_alle.json (Anfang/Ende = Befund, geprueft)",
                     "gelaende": "1 m lokal" if args.daten1m else "2 m (Cloud)",
                     "fluss_sim": "vorschlaege.json, wasserzonen.json, ersetzt.json", "bericht_17": "wasserherkunft/faelle_herkunft.json"},
        "einheiten": "cm (Koordinaten, Breite, Tiefe), cm/s (Tempo), m (Laengen in Feldern *_m)",
        "punkt_felder": PUNKT_FELDER,
        "anwendung": {
            "kopf_ersetzen": "neue Spline = punkte + alt[alt_bis_index_exkl:] (alt = Lauf in wasser_welt.json bzw. baeche_alle.json, Punkt 0 oben)",
            "anhaengen": "neue Spline = alt + punkte",
            "ende_ersetzen": "neue Spline = alt[:alt_ab_index] + punkte",
            "verjuengung_alle": "nur Breite/Tiefe/Tempo der genannten Punkt-Indizes setzen (x, y, z bleiben)",
            "instanzen": "Format FORMAT.md 3 unter instanzen/<Feld>/ (10 float32 je Instanz); hier je Fall lesbar: [Netz, x, y, z, qx, qy, qz, qw, Skala]",
            "baeche_bauen": "Tiefen-Klemme im Anfangsbereich: max(0,10 m; min(0,40 m; Breite/4)) statt >= 0,40 m"},
        "zusammenfassung": {"faelle_e": len(faelle), "loesungen": dict(sorted(zl.items())), "enden": len(enden),
                            "enden_loesungen": dict(sorted(ze.items())),
                            "verjuengung_alle": len([v for v in verj if v.get("punkte")]),
                            "verjuengung_ohne_spline": len([v for v in verj if not v.get("punkte")]),
                            "instanzen": len([i for i in I.liste if not i.get("lokal")]),
                            "instanzen_nur_im_plan_lokal": len([i for i in I.liste if i.get("lokal")]),
                            "akteure": 0, "felder": felder,
                            "neue_seen": len(seen), "neu_backen": backen["anzahl"], "netze": len(netze)},
        "faelle": faelle,
        "kaskade_k1": k1,
        "enden": enden,
        "verjuengung_alle": verj,
        "seen_neu": seen,
        "netze": dict(sorted(netze.items())),
        "neu_backen": backen,
        "dateien": sorted(dateien),
    }
    with open(os.path.join(args.aus, "bach_anfaenge_plan.json"), "w", encoding="utf-8") as fh:
        json.dump(plan, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    if args.bild:
        bilder(W, I, plan, os.path.join(args.aus, "bilder"))
    print("Faelle %d %s | Enden %s | Verjuengung %d | Instanzen %d in %d Feldern | Neu backen %d" % (
        len(faelle), dict(sorted(zl.items())), dict(sorted(ze.items())), plan["zusammenfassung"]["verjuengung_alle"],
        plan["zusammenfassung"]["instanzen"], len(felder), backen["anzahl"]))


def bilder(W, I, plan, ordner):
    if os.path.isdir(ordner):
        shutil.rmtree(ordner)
    os.makedirs(ordner, exist_ok=True)
    bild_uebersicht(W, plan["faelle"], plan["enden"], os.path.join(ordner, "uebersicht.png"))
    bild_regel(W, os.path.join(ordner, "profil_regel.png"))
    gesehen = set()
    for f in plan["faelle"]:
        typ = f["loesung"]
        if typ in gesehen or typ == "kaskade_k1" or not f.get("spline") or f.get("lokal"):
            continue
        gesehen.add(typ)
        alt = W.splines[f["id"]]
        neu = f["spline"]["punkte"] + alt[f["spline"]["alt_bis_index_exkl"]:]
        q = f["spline"]["punkte"][0]
        fen = W.R["ausgabe"]["bild_fenster_m"]
        if typ in ("karstquelle_trockental", "quellsumpf_see", "karsee"):
            fen = 200.0
        mitte = (q[0] / 100, q[1] / 100)
        fl = list(f.get("quellfassung", {}).get("lagen_wunsch", [])) + list(f.get("lagen_wunsch", []))
        if f.get("trockental"):
            fl.append({"form": "linie", "punkte_cm": f["trockental"]["punkte_cm"], "breite_m": 4})
        seen = [f["see_neu"]] if f.get("see_neu") else []
        if f.get("see") in W.seen:
            seen.append(W.seen[f["see"]])  # bestehender See (Seeabfluss)
        sa = bogen(alt)
        sn = bogen(neu)
        lim = f["L_m"] + 20
        prof = ([s for s in sa if s <= lim] or [0], [p[3] / 100 for p, s in zip(alt, sa) if s <= lim] or [alt[0][3] / 100],
                [s for s in sn if s <= lim + f["verlaengerung_m"]], [p[3] / 100 for p, s in zip(neu, sn) if s <= lim + f["verlaengerung_m"]])
        titel = "%s: %s\n%s\nBiom %s, Feld %s\nBreite alt %.1f m -> b0 %.2f m, L %.0f m\nVerlaengerung %.0f m, Instanzen %d" % (
            typ, f["id"], f["quelltyp"][:46], f["biom"], f["feld"], f["breite_alt_m"], f["b0_m"], f["L_m"],
            f["verlaengerung_m"], f["instanzen_anzahl"])
        bild_skizze(W, I, titel, mitte, fen, alt, neu, seen, fl, {f["id"]}, os.path.join(ordner, "skizze_%s.png" % typ), prof)
    # K1
    k1 = plan["kaskade_k1"]
    hf2 = W.splines["F_HAUPTFLUSS_2_B4"]
    pk = k1["spline"]["punkte"]
    xs = [p[0] / 100 for p in pk]
    ys = [p[1] / 100 for p in pk]
    mitte = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    fen = max(max(xs) - min(xs), max(ys) - min(ys)) + 80
    titel = "kaskade_k1: F_HAUPTFLUSS_2 -> 3\n%.0f m lang, %.0f m Hoehe, %d Stufen\nSchlucht %.0f m breit, Fall max %.1f m\nEinschnitt bis %.1f m (graben)" % (
        k1["laenge_m"], k1["hoehe_m"], k1["stufen_anzahl"], k1["schlucht_breite_m"], k1["fall_max_m"], k1["einschnitt"]["max_m"])
    sk = bogen(pk)
    bild_skizze(W, I, titel, mitte, fen, hf2 + [W.splines["F_HAUPTFLUSS_3_C4"][0]], [hf2[-1]] + pk, [], [], set(),
                os.path.join(ordner, "skizze_kaskade_k1.png"), (sk, [p[3] / 100 for p in pk], sk, [p[3] / 100 for p in pk]))
    # Enden je Art
    ges = set()
    for e in plan["enden"]:
        if e["loesung"] in ges or not e.get("spline"):
            continue
        ges.add(e["loesung"])
        alt = W.splines[e["id"]]
        sp = e["spline"]
        neu = alt[:sp["alt_ab_index"]] + sp["punkte"] if sp["modus"] == "ende_ersetzen" else alt + sp["punkte"]
        pe = alt[-1]
        if sp["modus"] == "anhaengen":
            xs = [p[0] / 100 for p in sp["punkte"]] + [pe[0] / 100]
            ys = [p[1] / 100 for p in sp["punkte"]] + [pe[1] / 100]
            mitte = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
            fen = max(max(xs) - min(xs), max(ys) - min(ys)) + 60
        else:
            mitte, fen = (pe[0] / 100, pe[1] / 100), 120.0
        bg = e["begruendung"]
        titel = "Ende %s: %s\n%s, Feld %s, Breite %.1f m\n%s\n%s" % (e["loesung"], e["id"], e["biom"], e["feld"], e["breite_m"],
                                                                    bg[:46], bg[46:92])
        sa, sn = bogen(alt), bogen(neu)
        a0 = max(0.0, sa[-1] - 120.0)
        prof = ([x - a0 for x in sa if x >= a0], [p[3] / 100 for p, x in zip(alt, sa) if x >= a0],
                [x - a0 for x in sn if x >= a0], [p[3] / 100 for p, x in zip(neu, sn) if x >= a0])
        bild_skizze(W, I, titel, mitte, fen, alt, neu, [], e.get("flaechen", []), {"ENDE_" + e["id"]},
                    os.path.join(ordner, "skizze_ende_%s.png" % e["loesung"]), prof)


if __name__ == "__main__":
    main()
