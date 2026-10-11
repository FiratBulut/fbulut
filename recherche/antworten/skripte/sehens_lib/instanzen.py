"""instanzen.py - Instanzen der Ebene sw_<biom> (SEHENS_FORMAT §4, Format exakt wie FORMAT.md §3).

Ausgabe je Feld: <welt>/sw_<biom>/<Feld>/plan.json + <Dateischluessel>.f32 (je Instanz 10 float32 LE:
x, y, z [cm], qx, qy, qz, qw, sx, sy, sz). Heldenstuecke als Akteure in plan["akteure"] (keine f32).
Dateischluessel = Netzname (+ "_kol" fuer Instanzen mit Kollision, + "__<Kurz>" bei Materialwunsch), damit der
Setzer je Datei einen Foliage-Typ FT_EL_SW<xx>_<Schluessel> mit EINER Kollisions-Einstellung anlegt.
Eine Instanz gehoert dem Feld, in dem sie liegt (Rechteck-Regel; der Setzer ueberspringt Instanzen ausserhalb).

Bausteine:
  Quaternionen (x, y, z, w): q_mul, q_achse, q_drehe, q_von_bis, q_yaw_kompass(grad), q_kippen(richtung, grad)
  orientierung(art, ...)       aufrecht | hochkant | liegend  (+ Kompass-Yaw, Kippen zur Hangnormalen, Neigen)
  platziere(inv, netz, x, y, q, s, boden_fn, eingraben_m, bezug="min")  -> z so, dass die Unterkante eingegraben ist
                               (Kontaktpunkte der Unterseite einzeln gegen das Gelaende -> nichts schwebt)
  Streuung: streue_flaeche(rng, form, n, abstand_m, filter_fn) mit Formen kreis/ring/ellipse/faecher/band/rechteck,
            cluster(rng, zentren, je, radius_m), um_stuecke(rng, stuecke, ring, je, seite) (Kontaktzonen)
  Ebene(biom, inv): neu(...), zaehle(ort), ausduennen(ort, budget), schreibe(sw_ordner), statistik
Standards je Detail-Ebene (held, begleiter, schutt, kleinzeug, bewuchs, kontakt, wasser): STANDARD_EBENE.
"""

import json
import math
import os
import zlib

import numpy as np

from . import log, ascii_text
from . import daten as _daten

EBENEN = ("held", "begleiter", "schutt", "kleinzeug", "bewuchs", "kontakt", "wasser", "pfad")
# Ausduenn-Reihenfolge (zuerst entfernt) bei Budget-Ueberschreitung
AUSDUENN_ORDNUNG = ("kleinzeug", "kontakt", "bewuchs", "pfad", "schutt", "wasser", "begleiter", "held")

STANDARD_EBENE = {
    # sichtweite [Start, Ende] cm (0 = unbegrenzt), schatten, Kollision ab Groesse m (None = nie)
    "held": {"sichtweite": [0, 0], "schatten": True, "kollision_ab_m": 0.8},
    "begleiter": {"sichtweite": [0, 0], "schatten": True, "kollision_ab_m": 0.8},
    "schutt": {"sichtweite": [0, 45000], "schatten": True, "kollision_ab_m": 0.8},
    "kleinzeug": {"sichtweite": [0, 9000], "schatten": False, "kollision_ab_m": None},
    "bewuchs": {"sichtweite": [0, 30000], "schatten": True, "kollision_ab_m": 2.5},
    "kontakt": {"sichtweite": [0, 12000], "schatten": False, "kollision_ab_m": None},
    "wasser": {"sichtweite": [0, 15000], "schatten": False, "kollision_ab_m": 0.8},
    "pfad": {"sichtweite": [0, 25000], "schatten": True, "kollision_ab_m": 0.5},
}
# Eingraben je Rolle (FORMAT.md §3): Anteil der Netzhoehe oder absolute Meter
STANDARD_EINGRABEN = {"fels": ("anteil", 0.25, 0.45), "stein": ("anteil", 0.30, 0.50),
                      "stamm": ("anteil", 0.20, 0.35), "baum": ("m", 0.15, 0.40), "pflanze": ("m", 0.02, 0.05),
                      "wurzel": ("anteil", 0.25, 0.40), "streu": ("m", 0.0, 0.02)}


# ============================================================================================
# Quaternionen (x, y, z, w) - Hamilton-Produkt wie FQuat
# ============================================================================================
def q_mul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def q_achse(achse, winkel_rad):
    a = np.asarray(achse, np.float64)
    n = float(np.linalg.norm(a))
    if n < 1e-12 or abs(winkel_rad) < 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    a = a / n
    s = math.sin(winkel_rad / 2.0)
    return (float(a[0] * s), float(a[1] * s), float(a[2] * s), math.cos(winkel_rad / 2.0))


def q_drehe(q, v):
    """Vektor(en) v (..., 3) mit q drehen."""
    x, y, z, w = q
    v = np.asarray(v, np.float64)
    u = np.array([x, y, z])
    t = 2.0 * np.cross(u, v)
    return v + w * t + np.cross(u, t)


def q_von_bis(u, v):
    """Kuerzeste Drehung, die Einheitsvektor u auf v bringt."""
    u = np.asarray(u, np.float64) / np.linalg.norm(u)
    v = np.asarray(v, np.float64) / np.linalg.norm(v)
    c = float(np.dot(u, v))
    if c > 1 - 1e-9:
        return (0.0, 0.0, 0.0, 1.0)
    if c < -1 + 1e-9:
        a = np.cross(u, [1, 0, 0])
        if np.linalg.norm(a) < 1e-6:
            a = np.cross(u, [0, 1, 0])
        return q_achse(a, math.pi)
    return q_achse(np.cross(u, v), math.acos(c))


def q_yaw_kompass(grad):
    """Drehung um Z, die die lokale +X-Achse auf die Kompassrichtung grad legt (0 = Nord = -Y, 90 = Ost)."""
    a = math.radians(grad)
    dx, dy = math.sin(a), -math.cos(a)
    return q_achse((0, 0, 1), math.atan2(dy, dx))


def q_kippen(richtung_grad, winkel_grad):
    """Kippt die Z-Achse um winkel_grad in Kompassrichtung richtung_grad."""
    a = math.radians(richtung_grad)
    dx, dy = math.sin(a), -math.cos(a)
    return q_achse((-dy, dx, 0.0), math.radians(winkel_grad))


def q_norm(q):
    q = np.asarray(q, np.float64)
    q = q / max(np.linalg.norm(q), 1e-12)
    if q[3] < 0:
        q = -q
    return tuple(float(v) for v in q)


def orientierung(art="aufrecht", yaw_grad=0.0, normale=None, normale_anteil=0.0, kipp_richtung_grad=None,
                 kipp_grad=0.0, hochkant_achse="y", roll_grad=0.0, front_achse="+x"):
    """Quaternion fuer eine Instanz.
    art: 'aufrecht' (Z bleibt oben) | 'hochkant' (lokale Y- bzw. X-Achse nach oben, fuer Schalen/Platten als Nadel) |
         'liegend' (lokale Z-Achse - Stamm - waagrecht in Richtung yaw_grad, roll_grad um die Stammachse).
    yaw_grad: Kompassrichtung, in die front_achse (aufrecht/hochkant) bzw. der Stammkopf (liegend) zeigt.
    normale/normale_anteil: Kippen zur Hangnormalen (0..1). kipp_*: zusaetzliches Neigen (Baum im Nachbarn haengend)."""
    if art == "liegend":
        q = q_mul(q_achse((0, 1, 0), math.pi / 2.0), q_achse((0, 0, 1), math.radians(roll_grad)))  # Z -> +X
        q = q_mul(q_yaw_kompass(yaw_grad), q)
    else:
        if art == "hochkant":
            q0 = q_achse((1, 0, 0), math.pi / 2.0) if hochkant_achse == "y" else q_achse((0, 1, 0), -math.pi / 2.0)
        else:
            q0 = (0.0, 0.0, 0.0, 1.0)
        f = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0), "+z": (0, 0, 1),
             "-z": (0, 0, -1)}[front_achse]
        f = q_drehe(q0, f)
        basis = math.atan2(f[1], f[0])
        q = q_mul(q_achse((0, 0, 1), -basis), q0)          # Front -> +X
        q = q_mul(q_yaw_kompass(yaw_grad), q)
    if normale is not None and normale_anteil > 0:
        n = np.asarray(normale, np.float64)
        qt = q_von_bis((0, 0, 1), n)
        ax = np.array(qt[:3])
        s = np.linalg.norm(ax)
        if s > 1e-9:
            win = 2 * math.atan2(s, qt[3]) * float(normale_anteil)
            q = q_mul(q_achse(ax, win), q)
    if kipp_grad and kipp_richtung_grad is not None:
        q = q_mul(q_kippen(kipp_richtung_grad, kipp_grad), q)
    return q_norm(q)


# ============================================================================================
# Platzierung
# ============================================================================================
def _ecken(bmin, bmax, n=4):
    xs = np.linspace(bmin[0], bmax[0], n)
    ys = np.linspace(bmin[1], bmax[1], n)
    zs = np.linspace(bmin[2], bmax[2], n)
    g = np.stack(np.meshgrid(xs, ys, zs, indexing="ij"), axis=-1).reshape(-1, 3)
    rand = ((g[:, 0] == xs[0]) | (g[:, 0] == xs[-1]) | (g[:, 1] == ys[0]) | (g[:, 1] == ys[-1]) |
            (g[:, 2] == zs[0]) | (g[:, 2] == zs[-1]))
    return g[rand]


def gedrehte_box(info, q, s):
    """Punkte der Oberflaeche der Netz-Box (cm, relativ zum Pivot) nach Skalierung und Drehung."""
    bmin, bmax = info["bounds_cm"]
    p = _ecken(bmin, bmax, 5) * np.asarray(s, np.float64)[None, :]
    return q_drehe(q, p)


def platziere(info, x_m, y_m, q, s, boden_fn, eingraben_m=0.0, bezug="min", z_unterkante_m=None, kontakt="welt",
              zentrieren=True):
    """Pivot-Position (cm) so, dass die Unterseite eingraben_m im Gelaende steckt.
    kontakt: 'lokal' = Unterseite der Netz-Box (lokal z = min; fuer aufrecht/zur Normalen gekippt - die Flaeche liegt
    im Hang), 'welt' = tiefste 12 % der gedrehten Box (hochkant/liegend).
    bezug: 'min' = kein Kontaktpunkt schwebt (Felsen, Staemme, Akteure), 'mitte' = Median der Kontaktpunkte
    (Pflanzen). z_unterkante_m: feste Unterkante (z. B. Oberkante eines anderen Stuecks oder Wasser).
    Rueckgabe dict(x, y, z [cm], hoehe_m (gedreht), fuss_r_m, boden_z_m, unterkante_z_m, oberkante_z_m)."""
    P = gedrehte_box(info, q, s)
    zmin, zmax = float(P[:, 2].min()), float(P[:, 2].max())
    H = max(zmax - zmin, 1.0)
    if kontakt == "lokal":
        bmin, bmax = info["bounds_cm"]
        g = np.stack(np.meshgrid(np.linspace(bmin[0], bmax[0], 5), np.linspace(bmin[1], bmax[1], 5),
                                 [bmin[2]], indexing="ij"), axis=-1).reshape(-1, 3)
        unten = q_drehe(q, g * np.asarray(s, np.float64)[None, :])
    else:
        unten = P[P[:, 2] <= zmin + 0.12 * H]
    cx = x_m * 100.0
    cy = y_m * 100.0
    # Pivot so verschieben, dass die Box-Mitte (XY) auf dem Zielpunkt liegt (zentrieren=False: Pivot = Zielpunkt,
    # z. B. Stammfuss eines liegenden Baums)
    mx = 0.5 * (P[:, 0].min() + P[:, 0].max()) if zentrieren else 0.0
    my = 0.5 * (P[:, 1].min() + P[:, 1].max()) if zentrieren else 0.0
    px, py = cx - mx, cy - my
    fuss_r = 0.5 * math.hypot(P[:, 0].max() - P[:, 0].min(), P[:, 1].max() - P[:, 1].min()) / 100.0
    # Fussabdruck als Ellipse (Hauptachsen der gedrehten Box im Grundriss): Kontaktzonen und Abstaende
    Q = P[:, :2] - P[:, :2].mean(axis=0)
    w_, V = np.linalg.eigh(Q.T @ Q)
    ach = V[:, ::-1]
    pr = Q @ ach
    fa, fb = float(np.abs(pr[:, 0]).max()) / 100.0, float(np.abs(pr[:, 1]).max()) / 100.0
    fw = math.atan2(ach[1, 0], ach[0, 0])
    if z_unterkante_m is not None:
        z = z_unterkante_m * 100.0 - eingraben_m * 100.0 - zmin
        b = float(boden_fn(x_m, y_m))
    else:
        bx = (px + unten[:, 0]) / 100.0
        by = (py + unten[:, 1]) / 100.0
        bz = np.asarray(boden_fn(bx, by), np.float64) * 100.0
        kand = bz - eingraben_m * 100.0 - unten[:, 2]
        z = float(kand.min()) if bezug == "min" else float(np.median(kand))
        b = float(boden_fn(x_m, y_m))
    return {"x": px, "y": py, "z": z, "hoehe_m": H / 100.0, "fuss_r_m": fuss_r, "boden_z_m": b,
            "unterkante_z_m": (z + zmin) / 100.0, "oberkante_z_m": (z + zmax) / 100.0,
            "mx_m": (px + P[:, 0].mean()) / 100.0, "my_m": (py + P[:, 1].mean()) / 100.0,
            "fuss_a_m": max(fa, 0.05), "fuss_b_m": max(fb, 0.05), "fuss_winkel": fw}


# ============================================================================================
# Streuung
# ============================================================================================
def rng_fuer(*teile):
    """Deterministischer Zufallsgenerator aus beliebigen Teilen (Seed, Ort, Gruppe)."""
    h = zlib.crc32("|".join(str(t) for t in teile).encode("utf-8"))
    return np.random.default_rng(h)


def form_punkte(rng, form, n):
    """n Zufallspunkte gleichverteilt in einer Form (dict, Weltkoordinaten m) -> (x, y, t) mit t in 0..1
    (Lage entlang Faecher/Band/Rechteck, sonst relativer Radius).
    Formen: {"typ": "kreis", "x", "y", "r"} | {"typ": "ring", "x", "y", "r": [a, b]} |
    {"typ": "ellipse", "x", "y", "a", "b", "richtung"} | {"typ": "faecher", "x", "y", "richtung", "laenge",
    "oeffnung", "t": [a, b]} | {"typ": "band", "punkte": [[x, y], ...], "breite", "t": [a, b]} |
    {"typ": "rechteck", "x", "y", "laenge", "breite", "richtung"}"""
    t = form["typ"]
    if n <= 0:
        return np.zeros(0), np.zeros(0), np.zeros(0)
    if t in ("kreis", "ring"):
        r = form["r"]
        r0, r1 = (0.0, float(r)) if np.isscalar(r) else (float(r[0]), float(r[1]))
        rr = np.sqrt(rng.uniform(r0 * r0, r1 * r1, n))
        a = rng.uniform(0, 2 * np.pi, n)
        return form["x"] + rr * np.cos(a), form["y"] + rr * np.sin(a), rr / max(r1, 1e-9)
    if t == "ellipse":
        rr = np.sqrt(rng.uniform(0, 1, n))
        a = rng.uniform(0, 2 * np.pi, n)
        u, v = rr * np.cos(a) * form["a"], rr * np.sin(a) * form["b"]
        ga = math.radians(form.get("richtung", 0.0))
        ux, uy = math.sin(ga), -math.cos(ga)
        return form["x"] + u * ux - v * uy, form["y"] + u * uy + v * ux, rr
    if t == "faecher":
        t0, t1 = form.get("t", [0.0, 1.0])
        tt = np.sqrt(rng.uniform(t0 * t0, t1 * t1, n))       # flaechentreu (Faecher wird breiter)
        oe = math.radians(form.get("oeffnung", 40.0)) / 2.0
        a = math.radians(form["richtung"]) + rng.uniform(-oe, oe, n)
        d = tt * form["laenge"] + form.get("start", 0.0)
        return form["x"] + d * np.sin(a), form["y"] - d * np.cos(a), tt
    if t == "band":
        P = np.asarray(form["punkte"], np.float64)[:, :2]
        seg = np.hypot(*np.diff(P, axis=0).T)
        kum = np.concatenate([[0], np.cumsum(seg)])
        L = kum[-1]
        t0, t1 = form.get("t", [0.0, 1.0])
        s = rng.uniform(t0 * L, t1 * L, n)
        k = np.clip(np.searchsorted(kum, s, side="right") - 1, 0, len(seg) - 1)
        f = (s - kum[k]) / np.maximum(seg[k], 1e-9)
        x = P[k, 0] + (P[k + 1, 0] - P[k, 0]) * f
        y = P[k, 1] + (P[k + 1, 1] - P[k, 1]) * f
        nx = -(P[k + 1, 1] - P[k, 1]) / np.maximum(seg[k], 1e-9)
        ny = (P[k + 1, 0] - P[k, 0]) / np.maximum(seg[k], 1e-9)
        b = form.get("breite", 2.0)
        off = rng.uniform(-b / 2.0, b / 2.0, n) + form.get("versatz", 0.0)
        return x + nx * off, y + ny * off, s / max(L, 1e-9)
    if t == "rechteck":
        ga = math.radians(form.get("richtung", 0.0))
        ux, uy = math.sin(ga), -math.cos(ga)
        u = rng.uniform(-form["laenge"] / 2.0, form["laenge"] / 2.0, n)
        v = rng.uniform(-form["breite"] / 2.0, form["breite"] / 2.0, n)
        return form["x"] + u * ux - v * uy, form["y"] + u * uy + v * ux, u / form["laenge"] + 0.5
    raise ValueError("Form %r unbekannt" % t)


def form_flaeche(form):
    t = form["typ"]
    if t in ("kreis", "ring"):
        r = form["r"]
        r0, r1 = (0.0, float(r)) if np.isscalar(r) else (float(r[0]), float(r[1]))
        return math.pi * (r1 * r1 - r0 * r0)
    if t == "ellipse":
        return math.pi * form["a"] * form["b"]
    if t == "faecher":
        t0, t1 = form.get("t", [0.0, 1.0])
        return math.radians(form.get("oeffnung", 40.0)) / 2.0 * (form["laenge"] ** 2) * (t1 * t1 - t0 * t0)
    if t == "band":
        P = np.asarray(form["punkte"], np.float64)[:, :2]
        t0, t1 = form.get("t", [0.0, 1.0])
        return float(np.hypot(*np.diff(P, axis=0).T).sum()) * (t1 - t0) * form.get("breite", 2.0)
    if t == "rechteck":
        return form["laenge"] * form["breite"]
    return 0.0


class Abstandsgitter:
    """Mindestabstand (Poisson-Scheiben) ueber Gitter-Hash; Eintraege mit eigenem Radius."""

    def __init__(self, zelle_m=2.0):
        self.z = float(zelle_m)
        self.g = {}

    def _k(self, x, y):
        return int(math.floor(x / self.z)), int(math.floor(y / self.z))

    def frei(self, x, y, r, faktor=1.0, such_r=None):
        such_r = such_r if such_r is not None else r + 12.0
        k0 = self._k(x - such_r, y - such_r)
        k1 = self._k(x + such_r, y + such_r)
        for i in range(k0[0], k1[0] + 1):
            for j in range(k0[1], k1[1] + 1):
                for (px, py, pr) in self.g.get((i, j), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < (faktor * (pr + r)) ** 2:
                        return False
        return True

    def frei_min(self, x, y, d):
        k0 = self._k(x - d, y - d)
        k1 = self._k(x + d, y + d)
        for i in range(k0[0], k1[0] + 1):
            for j in range(k0[1], k1[1] + 1):
                for (px, py, _) in self.g.get((i, j), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < d * d:
                        return False
        return True

    def add(self, x, y, r):
        self.g.setdefault(self._k(x, y), []).append((x, y, r))


def streue(rng, form, n, abstand_m=0.0, filter_fn=None, versuche=8, gitter=None):
    """Bis zu n Punkte in der Form mit Mindestabstand (untereinander und zu 'gitter'), Filter (x, y, t) -> bool-Array.
    Rueckgabe (x, y, t). Deterministisch (rng)."""
    if n <= 0:
        return np.zeros(0), np.zeros(0), np.zeros(0)
    x, y, t = form_punkte(rng, form, int(n * versuche) + 8)
    if filter_fn is not None:
        ok = np.asarray(filter_fn(x, y, t), bool)
        x, y, t = x[ok], y[ok], t[ok]
    eigen = Abstandsgitter(max(abstand_m, 0.5) * 2)
    out = []
    for k in range(len(x)):
        if len(out) >= n:
            break
        if abstand_m > 0 and not eigen.frei_min(x[k], y[k], abstand_m):
            continue
        if gitter is not None and not gitter(x[k], y[k]):
            continue
        eigen.add(x[k], y[k], 0.0)
        out.append(k)
    out = np.asarray(out, np.int64)
    return x[out], y[out], t[out]


def cluster(rng, zentren, je, radius_m):
    """Gruppen um Zentren [(x, y), ...]: je = (min, max) Punkte im Radius (zur Mitte dichter)."""
    xs, ys = [], []
    for cx, cy in zentren:
        k = int(rng.integers(je[0], je[1] + 1))
        r = radius_m * np.sqrt(rng.uniform(0, 1, k)) ** 1.3
        a = rng.uniform(0, 2 * np.pi, k)
        xs.extend(cx + r * np.cos(a))
        ys.extend(cy + r * np.sin(a))
    return np.asarray(xs), np.asarray(ys)


def um_stuecke(rng, stuecke, ring=(0.9, 1.6), je=(4, 8), seite=None, seite_staerke=0.7, boden_fn=None):
    """Kontaktzone: Punkte um platzierte Stuecke (dicts mit x_m, y_m, fuss_r_m) im Ring ring * Fussradius.
    seite: Kompassgrad (z. B. 0 = Nordseite fuer Moos) oder 'hangab' (braucht boden_fn) - bevorzugte Seite."""
    xs, ys, ts = [], [], []
    for st in stuecke:
        k = int(rng.integers(je[0], je[1] + 1))
        if k <= 0:
            continue
        ell = st.get("fuss_a_m") is not None and not st.get("_ring_absolut")
        if ell:
            # Ring um die Fuss-Ellipse (lange Stuecke wie Klammwaende, Staemme): Faktor auf beide Halbachsen
            f = rng.uniform(ring[0], ring[1], k)
            a = rng.uniform(0, 2 * np.pi, k)
            ca, sa = math.cos(st["fuss_winkel"]), math.sin(st["fuss_winkel"])
            u = f * st["fuss_a_m"] * np.cos(a) + 0.3 * np.sign(np.cos(a)) * (f > 1)
            v = f * st["fuss_b_m"] * np.sin(a) + 0.3 * np.sign(np.sin(a)) * (f > 1)
            dx, dy = u * ca - v * sa, u * sa + v * ca
            cx, cy = st.get("mx_m", st["x_m"]), st.get("my_m", st["y_m"])
            if seite is not None:
                # Seitenwahl: Punkte auf der falschen Seite mit Wahrscheinlichkeit seite_staerke verwerfen
                if seite == "hangab" and boden_fn is not None:
                    s_ = max(st["fuss_r_m"], 1.0)
                    gx = boden_fn(cx + s_, cy) - boden_fn(cx - s_, cy)
                    gy = boden_fn(cx, cy + s_) - boden_fn(cx, cy - s_)
                    zx, zy = -gx, -gy
                else:
                    g = math.radians(float(seite))
                    zx, zy = math.sin(g), -math.cos(g)
                gut = (dx * zx + dy * zy) >= 0
                behalten = gut | (rng.uniform(0, 1, k) > seite_staerke)
                dx, dy, f = dx[behalten], dy[behalten], f[behalten]
            xs.extend(cx + dx)
            ys.extend(cy + dy)
            ts.extend(f / max(ring[1], 1e-6))
            continue
        r0, r1 = ring[0] * st["fuss_r_m"], ring[1] * st["fuss_r_m"] + 0.3
        rr = rng.uniform(r0, r1, k)
        a = rng.uniform(0, 2 * np.pi, k)
        ziel = None
        if seite == "hangab" and boden_fn is not None:
            s = max(st["fuss_r_m"], 1.0)
            dzx = boden_fn(st["x_m"] + s, st["y_m"]) - boden_fn(st["x_m"] - s, st["y_m"])
            dzy = boden_fn(st["x_m"], st["y_m"] + s) - boden_fn(st["x_m"], st["y_m"] - s)
            ziel = math.atan2(-dzy, -dzx)
        elif isinstance(seite, (int, float)):
            g = math.radians(seite)
            ziel = math.atan2(-math.cos(g), math.sin(g))
        if ziel is not None:
            # Winkel zur Zielseite ziehen (von-Mises-artig)
            a = ziel + (a - np.pi) * (1.0 - seite_staerke)
        xs.extend(st["x_m"] + rr * np.cos(a))
        ys.extend(st["y_m"] + rr * np.sin(a))
        ts.extend(rr / max(r1, 1e-6))
    return np.asarray(xs), np.asarray(ys), np.asarray(ts)


# ============================================================================================
# Ebene sw_<biom>
# ============================================================================================
def ft_kuerzel(biom):
    return "SW" + biom[:2].upper()


class Ebene:
    """Sammelt Instanzen und Akteure aller Orte eines Bioms und schreibt sw_<biom>/<Feld>/."""

    def __init__(self, biom, inv, stand=""):
        self.biom = biom
        self.inv = inv
        self.stand = stand
        self.stuecke = []          # dicts
        self.hinweise = []

    def neu(self, ort, gruppe, ebene, netz, x_cm, y_cm, z_cm, q, s, kollision=False, akteur=False,
            sichtweite=None, schatten=None, material=None, extra=None, prioritaet=None, z_frei=False, rolle=None):
        """z_frei: Stueck ruht absichtlich NICHT auf dem Gelaende (auf einem anderen Stueck, verkeilt, im Wasser)."""
        info = self.inv.netz(netz)
        if ebene not in EBENEN:
            raise ValueError("Ebene %r (erlaubt: %s)" % (ebene, ", ".join(EBENEN)))
        std = STANDARD_EBENE[ebene]
        e = {"ort": ort, "gruppe": gruppe, "ebene": ebene, "netz": info["name"], "pfad": info["pfad"],
             "x": float(x_cm), "y": float(y_cm), "z": float(z_cm), "q": tuple(float(v) for v in q),
             "s": tuple(float(v) for v in s), "kollision": bool(kollision), "akteur": bool(akteur),
             "sichtweite": list(sichtweite if sichtweite is not None else std["sichtweite"]),
             "schatten": bool(std["schatten"] if schatten is None else schatten), "material": material,
             "nanite": info["nanite"], "pivot": info["pivot"], "extra": dict(extra or {}), "z_frei": bool(z_frei),
             "rolle": rolle,
             "prio": float(prioritaet if prioritaet is not None else zlib.crc32(
                 ("%s|%s|%d" % (ort, gruppe, len(self.stuecke))).encode()) / 4294967296.0)}
        # Feld aus der geschriebenen Genauigkeit (float32 bzw. 0,1 cm), sonst kann ein Stueck genau auf der Feldgrenze
        # nach dem Runden im Nachbarfeld liegen (Pruefer: "ausserhalb des Feldrechtecks")
        e["feld"] = _daten.feld_von_cm(round(float(np.float32(e["x"])), 1), round(float(np.float32(e["y"])), 1))
        self.stuecke.append(e)
        return e

    def vom_ort(self, ort):
        return [e for e in self.stuecke if e["ort"] == ort]

    def entferne_ort(self, ort):
        self.stuecke = [e for e in self.stuecke if e["ort"] != ort]

    def zaehle(self, ort=None):
        st = [e for e in self.stuecke if ort is None or e["ort"] == ort]
        je = {eb: sum(1 for e in st if e["ebene"] == eb) for eb in EBENEN}
        return {"instanzen": sum(1 for e in st if not e["akteur"]),
                "kollision": sum(1 for e in st if e["kollision"] and not e["akteur"]),
                "akteure": sum(1 for e in st if e["akteur"]),
                "akteure_kollision": sum(1 for e in st if e["akteur"] and e["kollision"]),
                "je_ebene": {k: v for k, v in je.items() if v}}

    def ausduennen(self, ort, max_instanzen=15000, max_kollision=1500, max_akteure=80):
        """Deterministisch nach Ebenen-Ordnung (Kleinzeug zuerst) und Hash-Prioritaet. Rueckgabe Anzahl entfernt."""
        weg = 0
        for art, grenze in (("instanzen", max_instanzen), ("kollision", max_kollision), ("akteure", max_akteure)):
            z = self.zaehle(ort)[art]
            if z <= grenze:
                continue
            zuviel = z - grenze
            if art == "instanzen":
                kand = [e for e in self.stuecke if e["ort"] == ort and not e["akteur"]]
            elif art == "kollision":
                kand = [e for e in self.stuecke if e["ort"] == ort and e["kollision"] and not e["akteur"]]
            else:
                kand = [e for e in self.stuecke if e["ort"] == ort and e["akteur"]]
            kand.sort(key=lambda e: (AUSDUENN_ORDNUNG.index(e["ebene"]), e["prio"]))
            if art == "kollision":
                for e in kand[:zuviel]:
                    e["kollision"] = False       # Kollision bei den kleinsten/unwichtigsten abschalten
            else:
                raus = set(id(e) for e in kand[:zuviel])
                self.stuecke = [e for e in self.stuecke if id(e) not in raus]
                weg += zuviel
            self.hinweise.append("%s: %s %d > %d - %d ausgeduennt (%s)" % (ort, art, z, grenze, zuviel,
                                                                          "Kollision aus" if art == "kollision" else "entfernt"))
            log("WARNUNG %s: Budget %s %d > %d, %d ausgeduennt" % (ort, art, z, grenze, zuviel))
        return weg

    @staticmethod
    def schluessel(e):
        k = e["netz"] + ("_kol" if e["kollision"] else "")
        if e.get("material"):
            k += "__" + e["material"].replace("MI_EL_SW_", "")
        return k

    def schreibe(self, sw_ordner, felder=None, orte_info=None):
        """Schreibt <sw_ordner>/<Feld>/plan.json + f32. felder: nur diese Felder (sonst alle mit Stuecken).
        Alte f32 im Feldordner werden entfernt. Rueckgabe dict Feld -> Zusammenfassung."""
        je_feld = {}
        for e in self.stuecke:
            if e["feld"] is None:
                self.hinweise.append("Stueck ausserhalb der Welt verworfen: %s %s" % (e["ort"], e["netz"]))
                continue
            je_feld.setdefault(e["feld"], []).append(e)
        out = {}
        for feld in sorted(set(je_feld) | set(felder or [])):
            if felder is not None and feld not in felder:
                continue
            st = je_feld.get(feld, [])
            ordner = os.path.join(sw_ordner, feld)
            os.makedirs(ordner, exist_ok=True)
            for fn in os.listdir(ordner):
                if fn.endswith(".f32"):
                    os.remove(os.path.join(ordner, fn))
            dateien, akteure = {}, []
            gruppen = {}
            for e in st:
                if e["akteur"]:
                    q = e["q"]
                    a = {"netz": e["netz"], "pfad": e["pfad"], "x": round(e["x"], 1), "y": round(e["y"], 1),
                         "z": round(e["z"], 1), "qx": round(q[0], 6), "qy": round(q[1], 6), "qz": round(q[2], 6),
                         "qw": round(q[3], 6), "sx": round(e["s"][0], 4), "sy": round(e["s"][1], 4),
                         "sz": round(e["s"][2], 4), "klasse": "%s_%s" % (e["ort"], e["gruppe"]),
                         "ebene": e["ebene"], "kollision": e["kollision"], "schatten": e["schatten"],
                         "nanite": e["nanite"], "pivot": e["pivot"]}
                    if e.get("material"):
                        a["material_wunsch"] = e["material"]
                    if e.get("z_frei"):
                        a["z_frei"] = True
                    for k, v in e["extra"].items():
                        a[k] = round(v, 2) if isinstance(v, float) else v
                    akteure.append(a)
                else:
                    gruppen.setdefault(self.schluessel(e), []).append(e)
            for key in sorted(gruppen):
                g = gruppen[key]
                rec = np.array([[e["x"], e["y"], e["z"], e["q"][0], e["q"][1], e["q"][2], e["q"][3],
                                 e["s"][0], e["s"][1], e["s"][2]] for e in g], dtype="<f4")
                rec.tofile(os.path.join(ordner, key + ".f32"))
                sw = [0, 0] if any(e["sichtweite"][1] == 0 for e in g) else \
                    [int(min(e["sichtweite"][0] for e in g)), int(max(e["sichtweite"][1] for e in g))]
                orte = {}
                for e in g:
                    orte[e["ort"]] = orte.get(e["ort"], 0) + 1
                dateien[key] = {"pfad": g[0]["pfad"], "anzahl": len(g),
                                "gruppe": "/".join(sorted({e["ebene"] for e in g})),
                                "rolle": "/".join(sorted({e["gruppe"] for e in g})),
                                "sichtweite": sw, "schatten": any(e["schatten"] for e in g),
                                "kollision": bool(g[0]["kollision"]), "nanite": bool(g[0]["nanite"]),
                                "ebene": "sw_" + self.biom, "orte": orte}
                if g[0].get("material"):
                    dateien[key]["material_wunsch"] = g[0]["material"]
                nz = sum(1 for e in g if e.get("z_frei"))
                if nz:
                    dateien[key]["z_frei_anzahl"] = nz
            n = sum(d["anzahl"] for d in dateien.values())
            kol = sum(d["anzahl"] for d in dateien.values() if d["kollision"])
            orte_feld = sorted({e["ort"] for e in st})
            plan = {"stand": self.stand, "feld": feld, "ebene": "sw_" + self.biom, "biom": self.biom,
                    "instanzen": n, "kollision_anzahl": kol, "akteure_anzahl": len(akteure),
                    "biome_eigen": [self.biom], "orte": orte_feld,
                    "orte_budget": {o: self._feld_budget(st, o) for o in orte_feld},
                    "ft_praefix": "FT_EL_%s_" % ft_kuerzel(self.biom),
                    "hinweis_setzer": ("Foliage-Typen FT_EL_%s_<Dateischluessel> (SEHENS_FORMAT §4); akteure als "
                                       "StaticMeshActor; z enthaelt das Eingraben; 'material_wunsch' = MI_EL_SW_* aus "
                                       "orte.json materialwuensche; pivot 'angenommen_unten_mitte' = Netz ohne Bounds in "
                                       "netze_masse.json (bitte im Editor pruefen)." % ft_kuerzel(self.biom)),
                    "dateien": dateien, "akteure": akteure}
            if orte_info:
                fr = [f for o in orte_feld for f in (orte_info.get(o, {}).get("freiraeume") or [])]
                if fr:
                    plan["freiraeume"] = fr
            if len(akteure) > 500:
                self.hinweise.append("Feld %s: %d Akteure > 500" % (feld, len(akteure)))
            with open(os.path.join(ordner, "plan.json"), "w", encoding="utf-8") as f:
                json.dump(plan, f, ensure_ascii=False, indent=1)
            out[feld] = {"instanzen": n, "kollision": kol, "akteure": len(akteure), "dateien": len(dateien),
                         "orte": orte_feld}
            log("geschrieben: %s (%d Instanzen in %d Dateien, %d Akteure)" % (ordner, n, len(dateien), len(akteure)))
        return out

    @staticmethod
    def _feld_budget(st, ort):
        s = [e for e in st if e["ort"] == ort]
        return {"instanzen": sum(1 for e in s if not e["akteur"]),
                "kollision": sum(1 for e in s if e["kollision"] and not e["akteur"]),
                "akteure": sum(1 for e in s if e["akteur"])}


def lies_ebene(sw_ordner):
    """Liest alle <Feld>/plan.json + f32 einer Ebene -> dict Feld -> (plan, {schluessel: array N x 10})."""
    out = {}
    if not os.path.isdir(sw_ordner):
        return out
    for feld in sorted(os.listdir(sw_ordner)):
        pj = os.path.join(sw_ordner, feld, "plan.json")
        if not os.path.exists(pj):
            continue
        with open(pj, "r", encoding="utf-8") as f:
            plan = json.load(f)
        arr = {}
        for key in plan.get("dateien", {}):
            pf = os.path.join(sw_ordner, feld, key + ".f32")
            if os.path.exists(pf):
                a = np.fromfile(pf, dtype="<f4")
                arr[key] = a.reshape(-1, 10) if a.size % 10 == 0 else a
        out[feld] = (plan, arr)
    return out


def text(s):
    return ascii_text(s)
