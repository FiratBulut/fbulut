"""kamera_frei.py - Auftrag 13h: Kameras (SEHENS_FORMAT §8) gegen die eigenen Akteure/Instanzen und den Baumbestand.

Befund aus dem ersten Editor-Pilot: _nah des Saeulenhains stand in einer neuen Baumkrone (nur Nadeln im Bild), und aus
_fern war der Hain nicht zu erkennen. Regeln (FEHLER im Pruefer, im Planer automatisch behoben):
  1. Kamera nicht im geplanten Wasser (See-Umriss, Bachbett) und nicht in einem Netz (Box + 0,3 m).
  2. Abstand zu jedem neuen Baum (Netzhoehe >= 2,5 m) waagrecht >= Kronenradius + 2 m.
  3. Freier Strahl Auge -> Ziel: kein neues Netz (Baeume als Kronenzylinder + Stamm, sonst gedrehte Box), keine
     Bestandskrone (4-m-Baumraster: Krone von 0,35 h bis h ueber dem Boden, ausser in Freiraeumen) auf >= 3 m Laenge,
     kein Gelaende (nach dem Stempel). Das Ziel selbst (Netze im Umkreis 1,5 m um den Zielpunkt) zaehlt nicht.
  4. Leuchtfeuer _fern: die Silhouette muss lesbar sein - sichtbarer Teil (Oberkante der Held-Netze ueber der
     Mindesthoehe, ab der der Strahl frei ist) >= max(10 m, 30 % der Hoehe). Ist der Held ein Baumhain: Held-Baeume
     >= 1,5 x die Bestandsbaeume im Ring um den Ort (90-%-Wert, ohne Freiraeume).

API:
  hindernisse_aus_stuecken(stuecke, inv)          (Planer: Ebene.stuecke)   -> Liste
  hindernisse_aus_ebene(sw_ordner, inv)           (Pruefer: plan.json + f32) -> Liste
  pruefe_kamera(kam, ort, welt, boden_fn, hind, freiraeume) -> [(stufe, text)]
  pruefe_leuchtfeuer(ort, welt, boden_fn, hind, freiraeume) -> [(stufe, text)]
  kameras_bauen(ctx)        Planer: prueft die Kameras eines Orts und versetzt blockierte (Regel "kameras")
  pruefe_orte_kameras(d, basis, welt, sw_ordner, inv) -> Befunde (Pruefer-Einstieg)
"""

import math
import re

import numpy as np

from . import daten as _daten

AUGE_M = 1.7
BAUM_AB_M = 2.5
KRONE_PLUS_M = 2.0            # Ferat 13h: Abstand >= Kronenradius + 2 m
BESTAND_KRONE_AB = 0.35       # Bestandskrone ab 35 % der Baumhoehe (Nadelbaeume; Stamm nicht modelliert)
BESTAND_BLOCK_M = 3.0         # so viel Strahl in Bestandskronen sperrt die Sicht
ZIEL_FREI_M = 1.5
LEUCHT_MIN_M = 10.0
LEUCHT_ANTEIL = 0.3
LEUCHT_FAKTOR = 1.5           # Ferat 13h: Riesen >= 1,5 x Nachbarhoehe

BAUM_MUSTER = re.compile(r"(tree|pine|fir_|spruce|birch|oak|beech|palm|cedar|larch|willow|maple|acacia|baobab|"
                         r"cypress|sequoia|redwood|mangrove|alder|ash_|elm|poplar)", re.I)
KEIN_BAUM_MUSTER = re.compile(r"(log|branch|root|stump|cone|needle|leaf|bark|fallen|dead_|trunk|_plant)", re.I)


def ist_baum(name):
    n = str(name or "").rsplit("/", 1)[-1]
    return bool(BAUM_MUSTER.search(n)) and not KEIN_BAUM_MUSTER.search(n)


# ============================================================================================
# Hindernisse
# ============================================================================================
def _hindernis(info, pfad, x_cm, y_cm, z_cm, q, s, ort=None, gruppe=None, ebene=None):
    from . import instanzen as _ins
    bmin, bmax = info["bounds_cm"]
    s = np.asarray(s, np.float64)
    P = _ins.gedrehte_box(info, q, s)
    xs, ys, zs = (x_cm + P[:, 0]) / 100.0, (y_cm + P[:, 1]) / 100.0, (z_cm + P[:, 2]) / 100.0
    H = float(zs.max() - zs.min())
    h = {"pfad": pfad, "ort": ort, "gruppe": gruppe, "ebene": ebene, "x": x_cm / 100.0, "y": y_cm / 100.0,
         "z0": float(zs.min()), "z1": float(zs.max()), "H": H,
         "bb": (float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max()))}
    if ist_baum(pfad) and H >= BAUM_AB_M:
        Q = np.stack([xs - xs.mean(), ys - ys.mean()], 1)
        w, V = np.linalg.eigh(Q.T @ Q)
        pr = Q @ V
        ext = np.abs(pr).max(axis=0)
        h.update(typ="baum", r_krone=float(max(0.5, min(ext))),
                 r_stamm=float(max(0.25, 0.012 * H)), z_krone=float(zs.min() + 0.15 * H))
    else:
        qi = (-q[0], -q[1], -q[2], q[3])
        h.update(typ="box", qi=qi, s=s, bmin=np.asarray(bmin, np.float64), bmax=np.asarray(bmax, np.float64),
                 pz=z_cm / 100.0)
    return h


def hindernisse_aus_stuecken(stuecke, inv, min_hoehe_m=1.0):
    """Planer: Hindernisse aus Ebene.stuecke (alle Orte des Laufs)."""
    out = []
    for e in stuecke:
        try:
            info = inv.netz(e["pfad"])
        except KeyError:
            continue
        gr = info["groesse_m"]
        if max(gr) * max(e["s"]) < min_hoehe_m:
            continue
        h = _hindernis(info, e["pfad"], e["x"], e["y"], e["z"], e["q"], e["s"], e["ort"], e["gruppe"], e["ebene"])
        if h["H"] >= min_hoehe_m or h["typ"] == "baum":
            out.append(h)
    return out


def hindernisse_aus_ebene(sw_ordner, inv, min_hoehe_m=1.0):
    """Pruefer: Hindernisse aus sw_<biom>/<Feld>/plan.json (Akteure) und den f32-Dateien (Instanzen)."""
    from . import instanzen as _ins
    out = []
    for feld, (plan, arr) in sorted(_ins.lies_ebene(sw_ordner).items()):
        for e in plan.get("akteure") or []:
            try:
                info = inv.netz(e.get("pfad") or e["netz"])
            except KeyError:
                continue
            q = (e["qx"], e["qy"], e["qz"], e["qw"])
            h = _hindernis(info, e.get("pfad"), e["x"], e["y"], e["z"], q, (e["sx"], e["sy"], e["sz"]),
                           ort=None, gruppe=e.get("klasse"), ebene=e.get("ebene"))
            if h["H"] >= min_hoehe_m:
                out.append(h)
        for key, d in (plan.get("dateien") or {}).items():
            a = arr.get(key)
            if a is None or a.ndim != 2 or not len(a):
                continue
            try:
                info = inv.netz(d.get("pfad", key))
            except KeyError:
                continue
            gr = info["groesse_m"]
            if max(gr) * float(np.max(a[:, 7:10])) < min_hoehe_m:
                continue
            for r in a:
                if max(gr) * float(max(r[7:10])) < min_hoehe_m:
                    continue
                h = _hindernis(info, d.get("pfad", key), float(r[0]), float(r[1]), float(r[2]),
                               (float(r[3]), float(r[4]), float(r[5]), float(r[6])), (float(r[7]), float(r[8]), float(r[9])),
                               gruppe=key, ebene=d.get("ebene"))
                if h["H"] >= min_hoehe_m or h["typ"] == "baum":
                    out.append(h)
    return out


def _in_hindernis(h, X, Y, Z, rand_m=0.0):
    """Punkte (Arrays) im Hindernis h."""
    if h["typ"] == "baum":
        d = np.hypot(X - h["x"], Y - h["y"])
        krone = (d <= 0.8 * h["r_krone"] + rand_m) & (Z >= h["z_krone"] - rand_m) & (Z <= h["z1"] + rand_m)
        stamm = (d <= h["r_stamm"] + rand_m) & (Z >= h["z0"]) & (Z <= h["z1"])
        return krone | stamm
    from . import instanzen as _ins
    v = np.stack([X * 100.0 - h["x"] * 100.0, Y * 100.0 - h["y"] * 100.0, Z * 100.0 - h["pz"] * 100.0], -1)
    lok = _ins.q_drehe(h["qi"], v) / np.maximum(h["s"], 1e-6)
    r = rand_m * 100.0 / np.maximum(h["s"], 1e-6)
    return np.all((lok >= h["bmin"] - r) & (lok <= h["bmax"] + r), axis=-1)


def _freiraum_maske(freiraeume, X, Y):
    m = np.zeros(np.broadcast(X, Y).shape, bool)
    for f in freiraeume or []:
        if not f.get("mitte_cm"):
            continue
        rollen = f.get("rollen") or ["baum"]
        if "baum" not in rollen:
            continue
        mx, my = f["mitte_cm"][0] / 100.0, f["mitte_cm"][1] / 100.0
        if f.get("form", "kreis") == "kreis":
            m |= np.hypot(X - mx, Y - my) <= float(f.get("radius_cm", 1000)) / 100.0
        else:
            a = math.radians(float(f.get("richtung_grad", 0.0)))
            ux, uy = math.sin(a), -math.cos(a)
            u = (X - mx) * ux + (Y - my) * uy
            v = -(X - mx) * uy + (Y - my) * ux
            m |= (np.abs(u) <= float(f.get("laenge_cm", 0)) / 200.0) & (np.abs(v) <= float(f.get("breite_cm", 0)) / 200.0)
    return m


def _bestand(welt, X, Y, freiraeume):
    """(Baumhoehe m, Baum ja) des 4-m-Bestands an Punkten; in Freiraeumen kein Baum."""
    i4, j4 = _daten.m_zu_pixel(X, Y, 4.0)
    i4 = np.clip(np.rint(i4), 0, welt.baumhoehe4.shape[0] - 1).astype(np.int64)
    j4 = np.clip(np.rint(j4), 0, welt.baumhoehe4.shape[1] - 1).astype(np.int64)
    bh = welt.baumhoehe4[i4, j4].astype(np.float64)
    da = (welt.baeume4[i4, j4] > 0) & (bh > 1.0)
    if freiraeume:
        da &= ~_freiraum_maske(freiraeume, X, Y)
    return bh, da


# ============================================================================================
# Kamera
# ============================================================================================
def kamera_auge(kam, boden_fn):
    kx, ky = kam[1] / 100.0, kam[2] / 100.0
    b = float(boden_fn(kx, ky))
    if kam[7] < 0:
        return kx, ky, b - kam[7] / 100.0
    return kx, ky, max(b + kam[7] / 100.0, kam[5] / 100.0 + 3.0)


def _wasser_bei(ort, x, y):
    from . import steilwand as _sw
    from . import stempel as _stm
    from . import bach as _b
    for w in ort.get("wasser") or []:
        if w.get("typ") == "see" and w.get("umriss_cm"):
            U = np.asarray(w["umriss_cm"], np.float64)[:, :2] / 100.0
            if _sw.in_polygon(np.array([x]), np.array([y]), U)[0]:
                return "See %s" % w.get("id")
        elif w.get("typ") == "bach" and w.get("punkte_cm") and len(w["punkte_cm"]) >= 2:
            P = np.asarray(w["punkte_cm"], np.float64)
            d, _, _ = _stm.polylinie_abstand(np.array([x]), np.array([y]), P[:, :2] / 100.0)
            if d[0] <= _b.halbe_breite_eff(float(P[0][3]) / 100.0 if P.shape[1] > 3 else 1.0, 1.0) + 0.5:
                return "Bach %s" % w.get("id")
    return None


def pruefe_kamera(kam, ort, welt, boden_fn, hind, freiraeume=None, bestand=True, rand_m=0.0):
    """Befunde [(stufe, text)] fuer eine Kamera [Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch]."""
    b = []
    name = str(kam[6])
    art = name.rsplit("_", 1)[-1]
    ex, ey, ez = kamera_auge(kam, boden_fn)
    tx, ty, tz = kam[3] / 100.0, kam[4] / 100.0, kam[5] / 100.0
    w = _wasser_bei(ort, ex, ey)
    if w:
        b.append(("FEHLER", "Kamera %s steht im geplanten Wasser (%s)" % (name, w)))
    d3 = math.sqrt((tx - ex) ** 2 + (ty - ey) ** 2 + (tz - ez) ** 2)
    if d3 < 0.5:
        return b
    # Kandidaten (Box um den Strahl + 25 m)
    x0, x1 = min(ex, tx) - 25.0, max(ex, tx) + 25.0
    y0, y1 = min(ey, ty) - 25.0, max(ey, ty) + 25.0
    nahe = [h for h in hind if not (h["bb"][2] < x0 or h["bb"][0] > x1 or h["bb"][3] < y0 or h["bb"][1] > y1)]
    for h in nahe:
        if h["typ"] == "baum":
            dh = math.hypot(ex - h["x"], ey - h["y"])
            if dh < h["r_krone"] + KRONE_PLUS_M + rand_m and h["z0"] - 1.0 <= ez <= h["z1"] + 1.0:
                b.append(("FEHLER", "Kamera %s %.1f m vom Stamm %s (Kronenradius %.1f m + 2 m noetig, 13h)"
                          % (name, dh, str(h["pfad"]).rsplit("/", 1)[-1], h["r_krone"])))
                break
        elif _in_hindernis(h, np.array([ex]), np.array([ey]), np.array([ez]), 0.3 + rand_m)[0]:
            b.append(("FEHLER", "Kamera %s steht in %s" % (name, str(h["pfad"]).rsplit("/", 1)[-1])))
            break
    # Strahl (neue Netze)
    n = max(int(d3 / 0.5), 2)
    t = np.linspace(0.0, 1.0, n + 1)
    X = ex + (tx - ex) * t
    Y = ey + (ty - ey) * t
    Z = ez + (tz - ez) * t
    s = t * d3
    gueltig = (s >= 0.3) & (s <= d3 - 1.0)
    eigen_held = {id(h) for h in _held_hindernisse(ort, nahe)} if art != "nah" else set()
    for h in nahe:
        # das Ziel selbst (Netz am Zielpunkt, bei Fern-/Uebersichtskameras die Held-Netze des Orts) sperrt nicht
        if id(h) in eigen_held:
            continue
        if _in_hindernis(h, np.array([tx]), np.array([ty]), np.array([tz]), ZIEL_FREI_M)[0]:
            continue
        sel = gueltig & (X >= h["bb"][0] - 1) & (X <= h["bb"][2] + 1) & (Y >= h["bb"][1] - 1) & (Y <= h["bb"][3] + 1)
        if not sel.any():
            continue
        hit = _in_hindernis(h, X[sel], Y[sel], Z[sel], rand_m)
        if hit.any():
            k = int(np.flatnonzero(hit)[0])
            b.append(("FEHLER", "Kamera %s: Sicht nach %.0f m durch %s verdeckt (13h: freie Sichtlinie)"
                      % (name, float(s[sel][k]), str(h["pfad"]).rsplit("/", 1)[-1])))
            break
    # Gelaende (nach dem Stempel)
    g = np.asarray(boden_fn(X, Y), np.float64)
    unter = gueltig & (s >= 1.0) & (Z < g - 0.2 + rand_m)
    if unter.any():
        b.append(("FEHLER", "Kamera %s: Gelaende verdeckt die Sicht nach %.0f m" % (name, float(s[unter][0]))))
    # Bestandskronen
    if bestand and art != "fern":
        bh, da = _bestand(welt, X, Y, freiraeume)
        im = gueltig & da & (Z >= g + BESTAND_KRONE_AB * bh) & (Z <= g + bh)
        lang = float(im.sum()) * (d3 / n)
        if lang >= BESTAND_BLOCK_M:
            b.append(("FEHLER", "Kamera %s: %.0f m des Strahls in Bestandskronen (4-m-Raster; Freiraum oder Kamera "
                                "versetzen, 13h)" % (name, lang)))
    return b


def _held_hindernisse(ort, hind):
    """Held-Netze des Orts (Planer: Feld 'ort'; Pruefer: Akteur-Klasse '<ort_id>_<gruppe>')."""
    oid = ort.get("id", "")
    return [h for h in hind if h.get("ebene") == "held" and
            (h.get("ort") == oid or str(h.get("gruppe") or "").startswith(oid + "_"))]


def pruefe_leuchtfeuer(ort, welt, boden_fn, hind, freiraeume=None):
    """Leuchtfeuer: _fern zeigt die Silhouette (Ziel ueber dem Bestand oder freie Achse); Baumhain >= 1,5 x Bestand."""
    from . import sicht as _si
    b = []
    if ort.get("art") != "leuchtfeuer":
        return b, None
    kams = [k for k in ort.get("kameras") or [] if str(k[6]).endswith("_fern")]
    held = _held_hindernisse(ort, hind)
    if not held:
        return b, None
    mx, my = ort["mitte_cm"][0] / 100.0, ort["mitte_cm"][1] / 100.0
    info = {}
    # Riesen-Regel (nur wenn der Held ein Baumhain ist)
    baeume = [h for h in held if h["typ"] == "baum"]
    if len(baeume) >= max(2, 0.5 * len(held)):
        r0 = float(ort.get("radius_m", 40.0))
        ang = np.linspace(0, 2 * np.pi, 72, endpoint=False)
        rr = np.arange(r0 + 5.0, r0 + 65.0, 4.0)
        A, RR = np.meshgrid(ang, rr)
        X = mx + RR * np.sin(A)
        Y = my - RR * np.cos(A)
        bh, da = _bestand(welt, X, Y, freiraeume)
        nachbar = float(np.percentile(bh[da], 90)) if da.sum() >= 10 else 0.0
        hoehen = np.array([h["H"] for h in baeume])
        info["held_hoehe_m"] = round(float(np.median(hoehen)), 1)
        info["nachbar_p90_m"] = round(nachbar, 1)
        if nachbar > 0 and float(np.median(hoehen)) < LEUCHT_FAKTOR * nachbar:
            b.append(("FEHLER", "Leuchtfeuer: Held-Baeume im Median %.1f m < %.1f x Bestand (90 %%: %.1f m) - nicht als "
                                "Silhouette lesbar (13h)" % (float(np.median(hoehen)), LEUCHT_FAKTOR, nachbar)))
    for kam in kams:
        ex, ey, ez = kamera_auge(kam, boden_fn)
        best = 0.0
        for h in sorted(held, key=lambda h_: -h_["z1"])[:12]:
            z_min, _ = _si.mindesthoehe(welt, ex, ey, ez, h["x"], h["y"], baum=False, ziel_rand_m=4.0)
            # Bestand ohne Freiraeume als Hindernis (Kronen 0,85 h wie sicht.py)
            d = math.hypot(h["x"] - ex, h["y"] - ey)
            t = np.arange(6.0, max(d - 4.0, 6.5), 4.0)
            Xs = ex + (h["x"] - ex) * t / d
            Ys = ey + (h["y"] - ey) * t / d
            g = np.asarray(boden_fn(Xs, Ys), np.float64)
            bh, da = _bestand(welt, Xs, Ys, freiraeume)
            ob = np.where(da, g + 0.85 * bh, g)
            zreq = ez + (ob - ez) * d / t
            # einzelne Kronen lassen Luecken (wie sicht.baum_block = 3): drittgroesster Wert der Kronen
            zk = np.sort(np.where(da, zreq, -np.inf))[::-1]
            zb = zk[2] if len(zk) >= 3 and np.isfinite(zk[2]) else -np.inf
            zg = float(np.max(np.where(~da, zreq, -np.inf))) if (~da).any() else -np.inf
            zm = max(float(z_min[0]), zb, zg)
            sicht = h["z1"] - zm
            best = max(best, sicht / max(h["H"], 1.0) if sicht > 0 else 0.0)
            if sicht >= max(LEUCHT_MIN_M, LEUCHT_ANTEIL * h["H"]):
                info["fern_sichtbar_m"] = round(float(sicht), 1)
                break
        else:
            b.append(("FEHLER", "Leuchtfeuer: aus %s ist die Silhouette nicht lesbar (bester Held %.0f %% sichtbar, "
                                "Soll >= max(10 m, 30 %%); 13h: Freiraum in der Achse, hoeher oder Kamera versetzen)"
                      % (kam[6], 100.0 * best)))
        info["fern_anteil"] = round(best, 2)
        info["fern_himmel"] = himmel_hinter(welt, ex, ey, ez, held)
    return b, info


def himmel_hinter(welt, ex, ey, ez, held, weit_m=4000.0):
    """Steht die Oberkante der Held-Netze vor dem Himmel (True) oder vor Gelaende dahinter (False)?"""
    h = max(held, key=lambda h_: h_["z1"])
    d = math.hypot(h["x"] - ex, h["y"] - ey)
    if d < 1.0:
        return True
    ux, uy = (h["x"] - ex) / d, (h["y"] - ey) / d
    t = np.arange(d + 20.0, d + weit_m, 20.0)
    X, Y = ex + ux * t, ey + uy * t
    ok = welt.im_raster_m(X, Y)
    if not ok.any():
        return True
    g = welt.bilinear(welt.hoehe, X[ok], Y[ok])
    winkel_gel = float(np.max((g - ez) / t[ok]))
    return bool((h["z1"] - ez) / d > winkel_gel)


# ============================================================================================
# Planer
# ============================================================================================
PLANER_RAND_M = 0.4         # Planer prueft mit Reserve (2-m-Stempel gegen 1-m-Boden des Pruefers)
ABSTAND = {"nah": (5.0, 15.0), "held": (20.0, 70.0), "anmarsch": (25.0, 160.0), "fern": (300.0, 800.0)}


def _kandidaten(kam, art, rng_n=48, abstand_m=None, richtung=None):
    """Ersatzpositionen fuer eine Kamera: Ringe um das Ziel, zuerst nahe der alten Position (oder der Richtung)."""
    tx, ty = kam[3] / 100.0, kam[4] / 100.0
    kx, ky = kam[1] / 100.0, kam[2] / 100.0
    d0 = math.hypot(kx - tx, ky - ty)
    a0 = math.atan2(kx - tx, -(ky - ty)) if richtung is None else math.radians(float(richtung))
    lo, hi = abstand_m if abstand_m else ABSTAND.get(art, (5.0, 80.0))
    d0 = min(max(d0, lo), hi)
    ds = sorted(set([round(max(lo, min(hi, d0 * f)), 1) for f in (1.0, 0.85, 1.15, 0.7, 1.3, 0.55, 1.5)] +
                    [round(lo + (hi - lo) * f, 1) for f in (0.0, 0.5, 1.0)]))
    out = []
    for d in ds:
        for k in range(rng_n):
            da = (k + 1) // 2 * (2 * math.pi / rng_n) * (1 if k % 2 else -1)
            a = a0 + da
            x, y = tx + d * math.sin(a), ty - d * math.cos(a)
            kosten = abs(da) * 10.0 + abs(d - d0) / max(d0, 1.0) * 6.0
            out.append((kosten, x, y))
    out.sort(key=lambda t: t[0])
    return out


def _ziel_aus_gruppe(ctx, r):
    """Zielpunkt = Stueck der Gruppe r["ziel_gruppe"], das am weitesten in r["ziel_richtung"] liegt (Hallenrand)."""
    from . import stempel as _stm
    st = ctx.gruppen.get(r["ziel_gruppe"]) or []
    if not st:
        return None
    ux, uy = _stm.kompass_vektor(float(r.get("ziel_richtung", 0.0)))
    best = max(st, key=lambda s_: (s_["stueck"]["x"] / 100.0 - ctx.mx) * ux + (s_["stueck"]["y"] / 100.0 - ctx.my) * uy)
    return best["stueck"]["x"] / 100.0, best["stueck"]["y"] / 100.0


def _fern_suchen(ctx, kam, ort, hind):
    """Leuchtfeuer _fern: Weg-/Pfadpunkt 300-800 m, von dem die Silhouette lesbar ist - zuerst vor dem Himmel,
    dann der groesste sichtbare Anteil; bei Gleichstand nahe der alten Kamera."""
    from . import sicht as _si
    wp = getattr(ctx, "_wegpunkte", None)
    if wp is None:
        wp = _si.Wegpunkte(ctx.welt, 20.0)
        ctx._wegpunkte = wp
    idx, d = wp.im_ring(ctx.mx, ctx.my, 300.0, 800.0)
    kx, ky = kam[1] / 100.0, kam[2] / 100.0
    best = None
    for k in idx:
        x, y = float(wp.x_m[k]), float(wp.y_m[k])
        k2 = list(kam)
        k2[0], k2[1], k2[2] = _daten.feld_von_m(x, y), int(round(x * 100)), int(round(y * 100))
        o2 = dict(ort, kameras=[k2])
        bef, info = pruefe_leuchtfeuer(o2, ctx.welt, ctx.boden, hind, ctx.freiraeume)
        if bef or not info:
            continue
        if pruefe_kamera(k2, ort, ctx.welt, ctx.boden, hind, ctx.freiraeume, bestand=False):
            continue
        sc = (1 if info.get("fern_himmel") else 0, round(info.get("fern_anteil", 0.0), 1),
              -math.hypot(x - kx, y - ky))
        if best is None or sc > best[0]:
            best = (sc, k2, info)
    return best


def kameras_bauen(ctx):
    """Planer (rezept.eintrag_bauen): Kameras aus standorte.json, ueberschrieben durch die Regel "kameras"
    ({"<art>": {"pos": ref, "ziel": ref | "ziel_gruppe": name + "ziel_richtung": grad, "ziel_hoehe_m": h,
    "abstand_m": [a, b], "richtung": grad (Kamera vom Ziel aus), "hoch": -170, "grund": text},
    "fern": {"suche": "wegpunkte"}, "versetzen": true}), dann geprueft; blockierte Kameras werden versetzt (Ring um
    das Ziel, nahe der alten Position). Rueckgabe: neue Kameraliste (oder None = unveraendert)."""
    regel = ctx.r.get("kameras") or {}
    alt = [list(k) for k in ctx.st.get("kameras") or []]
    if not alt:
        return None
    hind = hindernisse_aus_stuecken(ctx.ebene.stuecke, ctx.inv)
    ort = {"id": ctx.id, "wasser": ctx.wasser, "art": ctx.st["art"], "mitte_cm": ctx.st["mitte_cm"],
           "radius_m": ctx.st["radius_m"]}
    frei = ctx.freiraeume
    neu = []
    geaendert = False
    for kam in alt:
        name = str(kam[6])
        art = name.rsplit("_", 1)[-1]
        r = regel.get(art) or {}
        if r:
            ziel = None
            if r.get("ziel_gruppe"):
                ziel = _ziel_aus_gruppe(ctx, r)
            elif r.get("ziel") is not None:
                ziel = ctx.punkt(r["ziel"])
            if ziel is not None:
                zx, zy = ziel
                zz = float(ctx.boden(zx, zy)) + float(r.get("ziel_hoehe_m", 1.0))
                kam[3], kam[4], kam[5] = int(round(zx * 100)), int(round(zy * 100)), int(round(zz * 100))
            if r.get("pos") is not None:
                px, py = ctx.punkt(r["pos"])
                kam[1], kam[2] = int(round(px * 100)), int(round(py * 100))
                kam[0] = _daten.feld_von_m(px, py)
            if r.get("hoch") is not None:
                kam[7] = int(r["hoch"])
            geaendert = True
            if art == "fern" and r.get("suche") == "wegpunkte":
                b_ = _fern_suchen(ctx, kam, ort, hind)
                if b_ is not None:
                    kam = b_[1]
                    ctx.melde("HINWEIS", "Kamera %s gesucht (13h): Wegpunkt (%.0f, %.0f) m, %.0f m vom Ort, Silhouette %s, "
                                         "Anteil %.2f" % (name, kam[1] / 100.0, kam[2] / 100.0,
                                                         math.hypot(kam[1] / 100.0 - ctx.mx, kam[2] / 100.0 - ctx.my),
                                                         "vor dem Himmel" if b_[2].get("fern_himmel") else "vor Gelaende",
                                                         b_[2].get("fern_anteil", 0.0)))
        bef = pruefe_kamera(kam, ort, ctx.welt, ctx.boden, hind, frei, rand_m=PLANER_RAND_M)
        if bef and regel.get("versetzen", True) and art != "fern":
            from . import steilwand as _sw
            ausgeblendet = [e["umriss_cm"] for e in ctx.bestand_ausblenden if e.get("art") == "houdini" and e.get("umriss_cm")]
            kand = []
            for kosten, x, y in _kandidaten(kam, art, abstand_m=r.get("abstand_m"), richtung=r.get("richtung")):
                if not ctx.welt.im_raster_m(x, y):
                    continue
                i, j = ctx.welt.m_zu_ij(x, y)
                if ctx.welt.meer[i, j]:
                    continue
                if ctx.welt.wasser[i, j] > 0 and not any(
                        _sw.in_polygon(np.array([x]), np.array([y]), np.asarray(u, np.float64) / 100.0)[0]
                        for u in ausgeblendet):
                    continue                    # Bestandswasser, ausser es wird ausgeblendet (houdini, 13f B)
                hg = float(ctx.stempel.hang_grad_bei_m(x, y)) if ctx.stempel is not None else 0.0
                if hg > 50.0:
                    continue                    # Standplatz: Augenhoehe auf Fels/Halde, nicht in der Wand
                kand.append((kosten + max(0.0, hg - 30.0) * 0.3, x, y))
            kand.sort(key=lambda t: t[0])
            for kosten, x, y in kand:
                k2 = list(kam)
                k2[0], k2[1], k2[2] = _daten.feld_von_m(x, y), int(round(x * 100)), int(round(y * 100))
                if not pruefe_kamera(k2, ort, ctx.welt, ctx.boden, hind, frei, rand_m=PLANER_RAND_M):
                    ctx.melde("HINWEIS", "Kamera %s versetzt (13h): (%.0f, %.0f) -> (%.0f, %.0f) m, %.0f m vom Ziel - "
                                         "vorher: %s" % (name, kam[1] / 100.0, kam[2] / 100.0, x, y,
                                                         math.hypot(x - kam[3] / 100.0, y - kam[4] / 100.0), bef[0][1]))
                    kam = k2
                    bef = []
                    geaendert = True
                    break
        for st_, t in bef:
            ctx.melde("WARNUNG" if st_ == "FEHLER" else st_, t)
        neu.append([kam[0], int(kam[1]), int(kam[2]), int(kam[3]), int(kam[4]), int(kam[5]), kam[6], int(kam[7])])
    return neu if geaendert else None


# ============================================================================================
# Pruefer
# ============================================================================================
def pruefe_orte_kameras(d, basis, welt, sw_ordner, inv):
    """Pruefer-Einstieg: Regeln 1-4 fuer alle Orte einer orte.json (Boden nach allen Stempeln)."""
    from . import sehens_pruefen as _sp
    if welt is None or inv is None:
        return []
    hind = hindernisse_aus_ebene(sw_ordner, inv) if sw_ordner else []
    boden = _sp.BodenNachStempel(welt, d.get("orte") or [], basis)
    b = []
    for o in d.get("orte") or []:
        oid = o.get("id", "?")
        for kam in o.get("kameras") or []:
            if not (isinstance(kam, list) and len(kam) == 8):
                continue
            for st_, t in pruefe_kamera(kam, o, welt, boden.hoehe, hind, o.get("freiraeume")):
                b.append((st_, oid, t))
        bef, info = pruefe_leuchtfeuer(o, welt, boden.hoehe, hind, o.get("freiraeume"))
        b += [(st_, oid, t) for st_, t in bef]
        if info:
            b.append(("HINWEIS", oid, "Leuchtfeuer (13h): %s" % ", ".join("%s %s" % kv for kv in sorted(info.items()))))
    return b
