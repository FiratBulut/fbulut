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
import os
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
LAUB_MUSTER = re.compile(r"(fallen|log|_plant|fern|bush|shrub|petasites|grass|reed|rush|rohrkolben|vine|ivy|liana|"
                         r"buckthorn|juniper|heath|broom|ginster|leaf|foliage|kelp|cattail|bamboo)", re.I)
KEIN_BAUM_MUSTER = re.compile(r"(log|branch|root|stump|cone|needle|leaf|bark|fallen|trunk|_plant)", re.I)


def ist_baum(name):
    n = str(name or "").rsplit("/", 1)[-1]
    return bool(BAUM_MUSTER.search(n)) and not KEIN_BAUM_MUSTER.search(n)


# ============================================================================================
# Hindernisse
# ============================================================================================
def _q_matrix(q):
    x, y, z, w = [float(v) for v in q]
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


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
    breite = max(float(xs.max() - xs.min()), float(ys.max() - ys.min()))
    if ist_baum(pfad) and H >= BAUM_AB_M and H >= 0.8 * breite:      # stehender Baum (liegende Staemme: Box)
        Q = np.stack([xs - xs.mean(), ys - ys.mean()], 1)
        w, V = np.linalg.eigh(Q.T @ Q)
        pr = Q @ V
        ext = np.abs(pr).max(axis=0)
        h.update(typ="baum", r_krone=float(max(0.5, min(ext))),
                 r_stamm=float(max(0.25, 0.012 * H)), z_krone=float(zs.min() + 0.15 * H))
    else:
        qi = (-q[0], -q[1], -q[2], q[3])
        b0, b1 = np.asarray(bmin, np.float64), np.asarray(bmax, np.float64)
        if ist_baum(pfad) or LAUB_MUSTER.search(str(pfad).rsplit("/", 1)[-1]):
            # Laub/Nadeln fuellen die Box nicht: liegende Baeume, Jungbaeume -> Kern 80 % der Box
            m_, r_ = 0.5 * (b0 + b1), 0.4 * (b1 - b0)
            b0, b1 = m_ - r_, m_ + r_
        elif float(np.max((b1 - b0) * s)) > 1500.0:
            # sehr grosse Fels-/Klippenschalen (> 15 m) sind hohl/konkav: Kern 70 % der Box (Ueberhang, Nische)
            m_, r_ = 0.5 * (b0 + b1), 0.35 * (b1 - b0)
            b0, b1 = m_ - r_, m_ + r_
        h.update(typ="box", M=_q_matrix(qi), s=s, bmin=b0, bmax=b1, pz=z_cm / 100.0)
    return h


_CACHE = {}
MIN_HOEHE_M = 2.0             # Instanzen kleiner als 2 m (Farn, Gras, Kiesel) sperren keinen Blick in Augenhoehe


def _stueck_signatur(e):
    return (e.get("pfad"), e.get("x"), e.get("y"), e.get("z"), tuple(e.get("q") or ()), tuple(e.get("s") or ()),
            bool(e.get("akteur")), e.get("ort"), e.get("gruppe"), e.get("ebene"))


def hindernisse_aus_stuecken(stuecke, inv, min_hoehe_m=MIN_HOEHE_M):
    """Planer: Hindernisse aus Ebene.stuecke (alle Orte des Laufs); Akteure immer, Instanzen ab min_hoehe_m."""
    out = []
    for e in stuecke:
        c = _CACHE.get(id(e))
        # 13i Nachtrag: Treffer nur bei gleichem Stueck UND gleicher Lage/Groesse/Rolle (Stuecke werden nach dem ersten
        # Kamerabau noch versetzt: Seebloecke, Buendeln) - sonst neu rechnen; die Reihenfolge folgt immer 'stuecke'
        sig = _stueck_signatur(e)
        if c is not None and c[0] is e and c[2] == sig:
            if c[1] is not None:
                out.append(c[1])
            continue
        h = None
        try:
            info = inv.netz(e["pfad"])
        except KeyError:
            info = None
        grenze = 1.0 if e.get("akteur") else min_hoehe_m
        if info is not None and max(info["groesse_m"]) * max(e["s"]) >= grenze:
            h = _hindernis(info, e["pfad"], e["x"], e["y"], e["z"], e["q"], e["s"], e["ort"], e["gruppe"], e["ebene"])
            if not (h["H"] >= grenze or h["typ"] == "baum"):
                h = None
            else:
                h["stueck"] = e
        _CACHE[id(e)] = (e, h, sig)
        if h is not None:
            out.append(h)
    return out


def hindernisse_aus_ebene(sw_ordner, inv, min_hoehe_m=MIN_HOEHE_M):
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
            if h["H"] >= 1.0:
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
                orte_d = list((d.get("orte") or {}).keys())
                # 13j: Wandmodule/Heldenstuecke, die als Instanzen kommen (Akteur-Budget), behalten ihre Ebene 'held'
                gr_ = str(d.get("gruppe") or "").split("/")
                eb_ = next((g_ for g_ in ("held", "begleiter", "schutt", "kleinzeug", "bewuchs", "kontakt", "wasser",
                                          "pfad") if g_ in gr_), d.get("ebene"))
                h = _hindernis(info, d.get("pfad", key), float(r[0]), float(r[1]), float(r[2]),
                               (float(r[3]), float(r[4]), float(r[5]), float(r[6])), (float(r[7]), float(r[8]), float(r[9])),
                               ort=orte_d[0] if len(orte_d) == 1 else None, gruppe=key, ebene=eb_)
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
    v = np.stack([X * 100.0 - h["x"] * 100.0, Y * 100.0 - h["y"] * 100.0, Z * 100.0 - h["pz"] * 100.0], -1)
    lok = (v @ h["M"].T) / np.maximum(h["s"], 1e-6)
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
_BB = {}


def _bb_array(hind):
    c = _BB.get(id(hind))
    if c is not None and c[0] is hind and c[1] == len(hind):
        return c[2]
    a = np.array([h["bb"] for h in hind], np.float64).reshape(-1, 4)
    _BB.clear()
    _BB[id(hind)] = (hind, len(hind), a)
    return a


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
    bb = _bb_array(hind)
    sel_ = np.flatnonzero(~((bb[:, 2] < x0) | (bb[:, 0] > x1) | (bb[:, 3] < y0) | (bb[:, 1] > y1))) if len(hind) else []
    nahe = [hind[k] for k in sel_]
    for h in nahe:
        if h["typ"] == "baum":
            dh = math.hypot(ex - h["x"], ey - h["y"])
            if dh < h["r_krone"] + KRONE_PLUS_M + rand_m and h["z0"] - 1.0 <= ez <= h["z1"] + 1.0:
                b.append(("FEHLER", "Kamera %s %.1f m vom Stamm %s (Kronenradius %.1f m + 2 m noetig, 13h)"
                          % (name, dh, str(h["pfad"]).rsplit("/", 1)[-1], h["r_krone"])))
                break
        elif _in_hindernis(h, np.array([ex]), np.array([ey]), np.array([ez]), max(0.3, rand_m))[0]:
            # 13i Nachtrag: der Planer prueft auch den Standplatz mit seiner Reserve (Augenhoehe aus dem 2-m-Stempel
            # weicht vom 1-m-Boden des Pruefers um Dezimeter ab; gletscher_03 _nah stand 0,18 m tiefer im Netz)
            b.append(("FEHLER", "Kamera %s steht in %s" % (name, str(h["pfad"]).rsplit("/", 1)[-1])))
            break
    # Strahl (neue Netze)
    n = max(int(d3 / 0.5), 2)
    t = np.linspace(0.0, 1.0, n + 1)
    X = ex + (tx - ex) * t
    Y = ey + (ty - ey) * t
    Z = ez + (tz - ez) * t
    s = t * d3
    # Motivradius: was naeher als r_motiv am Ziel steht, ist Teil des Bildes (Szene), nicht Verdeckung
    if art == "nah":
        r_motiv = ZIEL_FREI_M
    else:
        r_motiv = min(0.35 * d3, 0.6 * float(ort.get("radius_m", 30.0)))
    gueltig = (s >= 0.3) & (s <= d3 - max(1.0, r_motiv))
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
    # Gelaende (nach dem Stempel) - bei _fern entscheidet die Silhouetten-Regel (pruefe_leuchtfeuer)
    g = np.asarray(boden_fn(X, Y), np.float64)
    unter = gueltig & (s >= 1.0) & (Z < g - 0.2 + (0.7 if rand_m >= 0.5 else (0.35 if rand_m > 0 else 0.0)))
    if unter.any() and art != "fern":
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
    # Totholz (abgestorbene, kahle Staemme) liest sich ueber Farbe und Form, nicht ueber die Hoehe -> nur lebende Baeume
    baeume = [h for h in held if h["typ"] == "baum" and not re.search(r"dead", str(h["pfad"]), re.I)]
    if len(baeume) >= max(2, 0.5 * len(held)):
        r0 = float(ort.get("radius_m", 40.0))
        ang = np.linspace(0, 2 * np.pi, 72, endpoint=False)
        rr = np.arange(r0 + 3.0, r0 + 35.0, 4.0)           # Nachbarn: Ring bis 35 m um den Ort (ohne Freiraeume)
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
            zm = _mindest_z(welt, boden_fn, ex, ey, ez, h["x"], h["y"], freiraeume)
            sicht = h["z1"] - zm
            best = max(best, sicht / max(h["H"], 1.0) if sicht > 0 else 0.0)
            if sicht >= LEUCHT_ANTEIL * h["H"] and (sicht >= LEUCHT_MIN_M or sicht >= 0.9 * h["H"]):
                info["fern_sichtbar_m"] = round(float(sicht), 1)
                break
        else:
            # Silhouette des Orts (Phase 1: Landform + Held, Zielhoehe = 2 x (ZZ - Boden)): >= 30 % ueber der
            # Mindesthoehe (Gelaende + Bestand ohne Freiraeume) genuegt ebenfalls ("Ziel ueber dem Bestand")
            zx, zy = kam[3] / 100.0, kam[4] / 100.0
            zb = float(boden_fn(zx, zy))
            zh_ = float((ort.get("sicht") or {}).get("ziel_hoehe_m") or 0.0)     # Silhouettenhoehe aus Phase 1
            H = max(2.0 * (kam[5] / 100.0 - zb), max(h_["z1"] for h_ in held) - zb, zh_, 4.0)
            zm = _mindest_z(welt, boden_fn, ex, ey, ez, zx, zy, freiraeume)
            anteil = (zb + H - zm) / H
            info["fern_ort_anteil"] = round(float(anteil), 2)
            if anteil < LEUCHT_ANTEIL:
                b.append(("FEHLER", "Leuchtfeuer: aus %s ist die Silhouette nicht lesbar (bester Held %.0f %% sichtbar, "
                                    "Ort-Silhouette %.0f %% von %.0f m; Soll >= 30 %%; 13h: Freiraum in der Achse, hoeher "
                                    "oder Kamera versetzen)" % (kam[6], 100.0 * best, 100.0 * max(anteil, 0.0), H)))
        info["fern_anteil"] = round(best, 2)
        info["fern_himmel"] = himmel_hinter(welt, ex, ey, ez, held)
    return b, info


# ============================================================================================
# 13k: Fern-Achse (Gelaende UND Baumkronen) - _fern darf nicht selbst im Wald stehen
# ============================================================================================
FERN_ANTEIL_MIN = 0.5         # mindestens die Haelfte der Silhouettenstrahlen frei
FERN_NAH_M = 60.0             # Vordergrund: Korridor +-FERN_KORRIDOR_M um den Hauptstrahl kronenfrei
FERN_KORRIDOR_M = 2.0
FERN_KRONE_BLOCK_M = 1.0      # so viel Strahl in einer Krone sperrt (4-m-Raster: Zellmitte +- Kronenradius)
FERN_GELAENDE_RAND_M = 0.3


def kronen_radius_m(h):
    """Kronenradius eines Bestandsbaums aus der Hoehe (Nadelbaum ~0,15 h, 1,2-4,0 m)."""
    return np.clip(0.15 * np.asarray(h, np.float64), 1.2, 4.0)


def bestand_kronen_treffer(welt, boden_fn, X, Y, Z, freiraeume=None):
    """13k: Punkte (X, Y, Z) in einer Bestandskrone? Jede Zelle des 4-m-Baumrasters (baeume4 > 0) traegt eine Krone
    um die Zellmitte: Radius kronen_radius_m(h) (oberste 15 % halber Radius), von Boden + 0,35 h bis Boden + h; Baeume
    in Freiraeumen (Regel 'freiraeume', Rolle baum) zaehlen nicht. Geprueft werden die 3 x 3 Nachbarzellen."""
    X = np.asarray(X, np.float64)
    Y = np.asarray(Y, np.float64)
    Z = np.asarray(Z, np.float64)
    fi, fj = _daten.m_zu_pixel(X, Y, 4.0)
    i0 = np.rint(fi).astype(np.int64)
    j0 = np.rint(fj).astype(np.int64)
    ny, nx = welt.baumhoehe4.shape
    hit = np.zeros(X.shape, bool)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            i = np.clip(i0 + di, 0, ny - 1)
            j = np.clip(j0 + dj, 0, nx - 1)
            h = welt.baumhoehe4[i, j].astype(np.float64)
            da = (welt.baeume4[i, j] > 0) & (h > 1.0)
            if not da.any():
                continue
            cx, cy = _daten.pixel_zu_m(i, j, 4.0)
            if freiraeume:
                da &= ~_freiraum_maske(freiraeume, cx, cy)
            if not da.any():
                continue
            g = np.asarray(boden_fn(cx, cy), np.float64)
            r = kronen_radius_m(h)
            r = np.where(Z > g + 0.85 * h, 0.5 * r, r)
            hit |= da & (np.hypot(X - cx, Y - cy) <= r) & (Z >= g + BESTAND_KRONE_AB * h) & (Z <= g + h)
    return hit


def _strahl_frei(welt, boden_fn, hind, freiraeume, ex, ey, ez, tx, ty, tz, ende_frei_m, ignor=(), gelaende=True):
    """Strahl Auge -> Punkt: (frei, Grund). Gelaende (nach dem Stempel) mit 0,3 m Rand, Bestandskronen (>= 1 m Strahl
    in Kronen), eigene Netze (Baeume als Krone + Stamm, sonst Box) - die letzten ende_frei_m vor dem Ziel zaehlen nicht."""
    d3 = math.sqrt((tx - ex) ** 2 + (ty - ey) ** 2 + (tz - ez) ** 2)
    dh = math.hypot(tx - ex, ty - ey)
    if d3 < 1.0:
        return True, ""
    s_nah = np.arange(1.0, min(80.0, d3), 0.5)
    s_fern = np.arange(80.0, d3, 2.0) if d3 > 80.0 else np.zeros(0)
    s = np.concatenate([s_nah, s_fern])
    s = s[s <= d3 - ende_frei_m]
    if not len(s):
        return True, ""
    f = s / d3
    X, Y, Z = ex + (tx - ex) * f, ey + (ty - ey) * f, ez + (tz - ez) * f
    g = np.asarray(boden_fn(X, Y), np.float64)
    unter = Z < g + FERN_GELAENDE_RAND_M
    if gelaende and unter.any():
        return False, "Gelaende nach %.0f m" % float(s[unter][0] * dh / d3)
    ds = np.diff(np.concatenate([[0.0], s]))
    kr = bestand_kronen_treffer(welt, boden_fn, X, Y, Z, freiraeume)
    if float((ds * kr).sum()) >= FERN_KRONE_BLOCK_M:
        return False, "Baumkronen (Bestand) nach %.0f m" % float(s[kr][0] * dh / d3)
    for h in hind:
        if id(h) in ignor:
            continue
        sel = (X >= h["bb"][0] - 1) & (X <= h["bb"][2] + 1) & (Y >= h["bb"][1] - 1) & (Y <= h["bb"][3] + 1)
        if not sel.any():
            continue
        if _in_hindernis(h, X[sel], Y[sel], Z[sel], 0.0).any():
            return False, "%s nach %.0f m" % (str(h["pfad"]).rsplit("/", 1)[-1], float(s[sel][0] * dh / d3))
    return True, ""


def pruefe_fern_achse(kam, ort, welt, boden_fn, hind, freiraeume=None):
    """13k (Ferat Pilot 2): freie Sichtachse aus _fern auf die Silhouette - Gelaende UND Baumkronen (Bestand aus dem
    4-m-Baumraster mit Kronenradius, eigene Baeume/Netze). Strahlen auf die oberen 30 % der hoechsten Held-Netze
    (bis 6 Netze x 3 Hoehen; ohne Held-Netz: Ort-Silhouette am Kameraziel); mindestens 50 % muessen frei sein. Dazu
    muss der Vordergrund frei sein: Korridor +-2 m um den Hauptstrahl auf den ersten 60 m ohne Krone/Netz/Gelaende
    (Kamera auf einer Lichtung oder am Gegenhang, nicht im Wald). Rueckgabe (befunde [(stufe, text)], info)."""
    b = []
    name = str(kam[6])
    ex, ey, ez = kamera_auge(kam, boden_fn)
    held = sorted(_held_hindernisse(ort, hind), key=lambda h_: -h_["z1"])[:6]
    ziele = []
    if held:
        for h in held:
            H = max(h["H"], 1.0)
            for f_ in (0.0, 0.15, 0.3):
                ziele.append((h["x"], h["y"], h["z1"] - f_ * H - 0.1))
    else:
        zx, zy = kam[3] / 100.0, kam[4] / 100.0
        zb = float(boden_fn(zx, zy))
        H = max(2.0 * (kam[5] / 100.0 - zb), float((ort.get("sicht") or {}).get("ziel_hoehe_m") or 0.0), 4.0)
        for f_ in (0.0, 0.15, 0.3):
            ziele.append((zx, zy, zb + (1.0 - f_) * H))
    eigen = {id(h) for h in _held_hindernisse(ort, hind)}
    r_motiv = 0.6 * float(ort.get("radius_m", 30.0))
    frei_n, gruende = 0, []
    for tx, ty, tz in ziele:
        ok, grund = _strahl_frei(welt, boden_fn, hind, freiraeume, ex, ey, ez, tx, ty, tz, r_motiv, eigen)
        frei_n += int(ok)
        if not ok:
            gruende.append(grund)
    anteil = frei_n / max(len(ziele), 1)
    # Vordergrund-Korridor um den Hauptstrahl (Mitte der Ziele)
    mx = float(np.mean([z_[0] for z_ in ziele]))
    my = float(np.mean([z_[1] for z_ in ziele]))
    mz = float(np.mean([z_[2] for z_ in ziele]))
    dh = max(math.hypot(mx - ex, my - ey), 1e-6)
    ux, uy = (mx - ex) / dh, (my - ey) / dh
    nah_ok, nah_grund = True, ""
    L = min(FERN_NAH_M, dh - r_motiv)
    for off in (-FERN_KORRIDOR_M, 0.0, FERN_KORRIDOR_M):
        # Parallelstrahl seitlich versetzt; nur die ersten L Meter (Bildvordergrund)
        px, py = ex - uy * off, ey + ux * off
        tz_ = ez + (mz - ez) * L / dh
        # seitliche Strahlen pruefen nur Kronen und Netze (das Gelaende neben der Kamera prueft der Hauptstrahl)
        ok, grund = _strahl_frei(welt, boden_fn, [h for h in hind if id(h) not in eigen], freiraeume,
                                 px, py, ez, px + ux * L, py + uy * L, tz_, 0.0, gelaende=(off == 0.0))
        if not ok:
            nah_ok, nah_grund = False, "%s (Versatz %+.0f m)" % (grund, off)
            break
    info = {"fern_achse_anteil": round(anteil, 2), "fern_vordergrund_frei": nah_ok}
    if anteil < FERN_ANTEIL_MIN:
        b.append(("FEHLER", "Kamera %s: Fern-Achse verdeckt - nur %d von %d Silhouettenstrahlen frei (%s; 13k: Gelaende "
                            "und Baumkronen, Lichtung oder Gegenhang)" % (name, frei_n, len(ziele),
                                                                        "; ".join(sorted(set(gruende))[:3]))))
    if not nah_ok:
        b.append(("FEHLER", "Kamera %s: Vordergrund verdeckt - %s im Korridor +-%.0f m auf den ersten %.0f m (13k: "
                            "Kamera steht im Wald)" % (name, nah_grund, FERN_KORRIDOR_M, L)))
    return b, info


def _mindest_z(welt, boden_fn, ex, ey, ez, tx, ty, freiraeume):
    """Mindesthoehe am Ziel fuer freie Sicht: Gelaende (nach dem Stempel) + Bestandskronen 0,85 h ohne Freiraeume;
    einzelne Kronen lassen Luecken (drittgroesster Kronenwert, wie sicht.baum_block = 3)."""
    from . import sicht as _si
    z_min, _ = _si.mindesthoehe(welt, ex, ey, ez, tx, ty, baum=False, ziel_rand_m=4.0)
    d = math.hypot(tx - ex, ty - ey)
    t = np.arange(6.0, max(d - 4.0, 6.5), 4.0)
    Xs = ex + (tx - ex) * t / max(d, 1e-6)
    Ys = ey + (ty - ey) * t / max(d, 1e-6)
    g = np.asarray(boden_fn(Xs, Ys), np.float64)
    bh, da = _bestand(welt, Xs, Ys, freiraeume)
    ob = np.where(da, g + 0.85 * bh, g)
    zreq = ez + (ob - ez) * d / t
    zk = np.sort(np.where(da, zreq, -np.inf))[::-1]
    zb = zk[2] if len(zk) >= 3 and np.isfinite(zk[2]) else -np.inf
    zg = float(np.max(np.where(~da, zreq, -np.inf))) if (~da).any() else -np.inf
    return max(float(z_min[0]), zb, zg)


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
PLANER_RAND_M = 0.6         # Planer prueft mit Reserve (2-m-Stempel gegen 1-m-Boden des Pruefers)
ABSTAND = {"nah": (5.0, 15.0), "held": (20.0, 70.0), "anmarsch": (25.0, 160.0), "fern": (300.0, 800.0)}
ABSTAND_WEIT = {"nah": (4.0, 16.0), "held": (12.0, 100.0), "anmarsch": (20.0, 220.0)}


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
    ux, uy = _stm.kompass_vektor(float(ctx.richtung(r.get("ziel_richtung", 0.0))))
    best = max(st, key=lambda s_: (s_["stueck"]["x"] / 100.0 - ctx.mx) * ux + (s_["stueck"]["y"] / 100.0 - ctx.my) * uy)
    return best["stueck"]["x"] / 100.0, best["stueck"]["y"] / 100.0


FERN_ABSEITS_M = 40.0         # 13k: Lichtung hoechstens so weit neben dem Weg/Pfad (zweiter Durchgang)
FERN_GEGENHANG_M = 150.0      # 13k: dritter Durchgang - Gegenhang/Aussichtspunkt bis 150 m neben Weg/Pfad (Raster 20 m)
FERN_FREI_M = 1.0e9           # 13k: vierter Durchgang - Aussichtspunkt im ganzen Ring (nur wenn sonst nichts frei ist)


def _fern_kandidaten(ctx, wp, weit=False):
    """13k: Kandidaten fuer _fern - Weg-/Pfadpunkte im Ring 300-800 m und Punkte bis 40 m daneben (Lichtung, Gegenhang):
    Raster 10 m, kein Wasser/Meer, Hang <= 30 Grad, keine Bestandskrone im Umkreis 6 m."""
    idx, d = wp.im_ring(ctx.mx, ctx.my, 300.0, 800.0)
    out = [(float(wp.x_m[k]), float(wp.y_m[k]), 0.0) for k in idx]
    if not len(idx):
        return out
    gesehen = set()
    if weit:
        # Gegenhang: Raster 20 m im ganzen Ring, bis FERN_GEGENHANG_M neben Weg/Pfad
        out = []
        for x0 in np.arange(math.floor((ctx.mx - 800.0) / 20.0) * 20.0, ctx.mx + 800.0, 20.0):
            for y0 in np.arange(math.floor((ctx.my - 800.0) / 20.0) * 20.0, ctx.my + 800.0, 20.0):
                x, y = float(x0), float(y0)
                r = math.hypot(x - ctx.mx, y - ctx.my)
                if not (300.0 <= r <= 800.0) or not bool(ctx.welt.im_raster_m(x, y)):
                    continue
                ab = float(np.min(np.hypot(wp.x_m[idx] - x, wp.y_m[idx] - y)))
                if FERN_ABSEITS_M < ab:
                    out.append((x, y, ab))
    for k in ([] if weit else idx):
        for dx in (-40.0, -30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0, 40.0):
            for dy in (-40.0, -30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0, 40.0):
                if dx == 0.0 and dy == 0.0:
                    continue
                x = round((float(wp.x_m[k]) + dx) / 10.0) * 10.0
                y = round((float(wp.y_m[k]) + dy) / 10.0) * 10.0
                if (x, y) in gesehen:
                    continue
                gesehen.add((x, y))
                r = math.hypot(x - ctx.mx, y - ctx.my)
                if not (300.0 <= r <= 800.0) or not bool(ctx.welt.im_raster_m(x, y)):
                    continue
                ab = float(np.min(np.hypot(wp.x_m[idx] - x, wp.y_m[idx] - y)))
                if ab > FERN_ABSEITS_M:
                    continue
                out.append((x, y, ab))
    ok = []
    for x, y, ab in out:
        if ab == 0.0:
            ok.append((x, y, ab))
            continue
        i, j = ctx.welt.m_zu_ij(x, y)
        if ctx.welt.meer[i, j] or ctx.welt.wasser[i, j] > 0 or ctx.welt.ort[i, j] > 0:
            continue
        gx = np.array([x - 2.0, x + 2.0, x, x])
        gy = np.array([y, y, y - 2.0, y + 2.0])
        hz = np.asarray(ctx.boden(gx, gy), np.float64)
        if math.degrees(math.atan(math.hypot(hz[1] - hz[0], hz[3] - hz[2]) / 4.0)) > 30.0:
            continue
        ang = np.linspace(0, 2 * np.pi, 12, endpoint=False)
        rx, ry = x + 6.0 * np.sin(ang), y - 6.0 * np.cos(ang)
        rz = np.asarray(ctx.boden(rx, ry), np.float64) + 6.0
        if bestand_kronen_treffer(ctx.welt, ctx.boden, rx, ry, rz, ctx.freiraeume).any():
            continue
        ok.append((x, y, ab))
    return ok


def _fern_suchen(ctx, kam, ort, hind, achse=True):
    """Leuchtfeuer _fern: Weg-/Pfadpunkt 300-800 m (13k: auch bis 40 m daneben auf einer Lichtung oder am Gegenhang),
    von dem die Silhouette lesbar ist UND die Achse frei ist (Gelaende und Baumkronen, pruefe_fern_achse) - zuerst vor
    dem Himmel, dann der groesste sichtbare Anteil, dann nahe am Weg; bei Gleichstand nahe der alten Kamera."""
    from . import sicht as _si
    wp = getattr(ctx, "_wegpunkte", None)
    if wp is None:
        wp = _si.Wegpunkte(ctx.welt, 20.0)
        ctx._wegpunkte = wp
    kx, ky = kam[1] / 100.0, kam[2] / 100.0
    best = None
    kand = _fern_kandidaten(ctx, wp)
    # zuerst die Weg-/Pfadpunkte selbst, nur wenn keiner taugt die Punkte daneben (Lichtung, Gegenhang)
    weit = None
    for lo, hi in ((0.0, 0.0), (0.1, FERN_ABSEITS_M), (FERN_ABSEITS_M + 0.1, FERN_GEGENHANG_M),
                   (FERN_GEGENHANG_M + 0.1, FERN_FREI_M)):
        if lo > FERN_ABSEITS_M:
            if weit is None:
                weit = _fern_kandidaten(ctx, wp, weit=True)  # nur wenn Weg und Lichtungen nichts liefern
            kand = weit
        ref = [None]
        _fern_durchgang(ctx, kam, ort, hind, achse, [k_ for k_ in kand if lo <= k_[2] <= hi], kx, ky, ref)
        best = ref[0]
        if best is not None:
            break
    return best


def _fern_durchgang(ctx, kam, ort, hind, achse, kand, kx, ky, best_ref):
    best = best_ref[0]
    for x, y, ab in kand:
        k2 = list(kam)
        k2[0], k2[1], k2[2] = _daten.feld_von_m(x, y), int(round(x * 100)), int(round(y * 100))
        o2 = dict(ort, kameras=[k2])
        bef, info = pruefe_leuchtfeuer(o2, ctx.welt, ctx.boden, hind, ctx.freiraeume)
        if bef or not info:
            continue
        if pruefe_kamera(k2, ort, ctx.welt, ctx.boden, hind, ctx.freiraeume, bestand=False):
            continue
        ach = None
        if achse:
            fb, ach = pruefe_fern_achse(k2, ort, ctx.welt, ctx.boden, hind, ctx.freiraeume)
            if fb:
                continue
        sc = (1 if info.get("fern_himmel") else 0, round(info.get("fern_anteil", 0.0), 1),
              round((ach or {}).get("fern_achse_anteil", 0.0), 1), -round(ab / 10.0), -math.hypot(x - kx, y - ky))
        if best is None or sc > best[0]:
            best = (sc, k2, dict(info, **(ach or {}), abseits_m=round(ab, 0)))
    best_ref[0] = best


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
           "radius_m": ctx.st["radius_m"],
           "sicht": {"ziel_hoehe_m": ctx.st.get("ziel_hoehe_m") or (ctx.st.get("sicht") or {}).get("ziel_hoehe_m")}}
    frei = ctx.freiraeume
    neu = []
    geaendert = False
    for kam in alt:
        kand = []
        name = str(kam[6])
        art = name.rsplit("_", 1)[-1]
        r = regel.get(art) or {}
        # Ziel folgt dem Gelaende nach dem Stempel (gleiche Hoehe ueber Grund wie in standorte.json)
        if ctx.stempel is not None and ctx.stempel.enthaelt(kam[3] / 100.0, kam[4] / 100.0):
            zb0 = float(ctx.welt.hoehe_bei_m(kam[3] / 100.0, kam[4] / 100.0))
            zb1 = float(ctx.boden(kam[3] / 100.0, kam[4] / 100.0))
            if zb1 - zb0 > 0.3:
                # aufgeschuettet: Ziel hebt sich mit (gleiche Hoehe ueber Grund); abgegraben: Ziel bleibt
                kam[5] = int(round((zb1 + max(kam[5] / 100.0 - zb0, 0.5)) * 100))
                geaendert = True
        zb_t = float(ctx.boden(kam[3] / 100.0, kam[4] / 100.0))
        if kam[5] / 100.0 < zb_t + 0.3:
            kam[5] = int(round((zb_t + (1.0 if art == "nah" else 2.0)) * 100))
            geaendert = True
            ctx.melde("HINWEIS", "Kamera %s: Ziel lag unter dem Boden - auf Boden + %.0f m gehoben (13h)"
                      % (name, 1.0 if art == "nah" else 2.0))
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
                                         "Anteil %.2f, %.0f m neben Weg/Pfad (13k)" % (name, kam[1] / 100.0, kam[2] / 100.0,
                                                         math.hypot(kam[1] / 100.0 - ctx.mx, kam[2] / 100.0 - ctx.my),
                                                         "vor dem Himmel" if b_[2].get("fern_himmel") else "vor Gelaende",
                                                         b_[2].get("fern_anteil", 0.0), b_[2].get("abseits_m", 0.0)))
        bef = pruefe_kamera(kam, ort, ctx.welt, ctx.boden, hind, frei, rand_m=PLANER_RAND_M)
        if os.environ.get("SEHENS_DBG_KAM") and os.environ["SEHENS_DBG_KAM"] in name:
            print("DBG", name, kam, bef)
        if art == "fern":
            # 13k: Fern-Achse (Gelaende und Baumkronen) gehoert zu den Kamera-Befunden
            fb_, _ = pruefe_fern_achse(kam, ort, ctx.welt, ctx.boden, hind, frei)
            bef = bef + fb_
        if art == "fern" and ctx.st["art"] == "leuchtfeuer" and regel.get("versetzen", True) and \
                (r.get("suche") != "wegpunkte" or [x for x in bef if "13k" in x[1]]):
            lb, _ = pruefe_leuchtfeuer(dict(ort, kameras=[kam]), ctx.welt, ctx.boden, hind, frei)
            if bef or [x for x in lb if "_fern" in x[1]]:
                b_ = _fern_suchen(ctx, kam, ort, hind)
                if b_ is not None:
                    ctx.melde("HINWEIS", "Kamera %s versetzt (13h): Wegpunkt (%.0f, %.0f) m, %.0f m vom Ort, Silhouette %s, "
                                         "Anteil %.2f, %.0f m neben Weg/Pfad (13k) - vorher: %s" % (name, b_[1][1] / 100.0, b_[1][2] / 100.0,
                                                                      math.hypot(b_[1][1] / 100.0 - ctx.mx, b_[1][2] / 100.0 - ctx.my),
                                                                      "vor dem Himmel" if b_[2].get("fern_himmel") else "vor Gelaende",
                                                                      b_[2].get("fern_anteil", 0.0), b_[2].get("abseits_m", 0.0),
                                                                      (bef or lb)[0][1]))
                    kam = b_[1]
                    geaendert = True
                    bef = pruefe_kamera(kam, ort, ctx.welt, ctx.boden, hind, frei, rand_m=PLANER_RAND_M)
                    bef = bef + pruefe_fern_achse(kam, ort, ctx.welt, ctx.boden, hind, frei)[0]
        if r.get("abstand_m") and not bef and art != "fern":
            d_ = math.hypot(kam[1] / 100.0 - kam[3] / 100.0, kam[2] / 100.0 - kam[4] / 100.0)
            if not (float(r["abstand_m"][0]) - 0.5 <= d_ <= float(r["abstand_m"][1]) + 0.5):
                bef = [("HINWEIS", "Kamera %s %.0f m vom Ziel, Regel %s m" % (name, d_, r["abstand_m"]))]
        if bef and regel.get("versetzen", True) and art != "fern":
            from . import steilwand as _sw
            ausgeblendet = [e["umriss_cm"] for e in ctx.bestand_ausblenden if e.get("art") == "houdini" and e.get("umriss_cm")]
            kand = []
            rr_ = ctx.richtung(r["richtung"]) if r.get("richtung") is not None else None
            roh = _kandidaten(kam, art, abstand_m=r.get("abstand_m"), richtung=rr_)
            if art in ABSTAND_WEIT:
                # zweiter Ring weiter gefasst (72 Richtungen), teurer -> hinten angestellt; 13k: auch bei einer
                # Ring-Regel als Rueckfall (Karsee 1 m: die Wandverkleidung > 60 Grad belegt Ufernischen)
                ring = ABSTAND_WEIT[art] if not r.get("abstand_m") else \
                    (float(r["abstand_m"][0]), float(r["abstand_m"][1]) + 5.0)
                roh += [(k_ + (50.0 if not r.get("abstand_m") else 200.0), x_, y_)
                        for k_, x_, y_ in _kandidaten(kam, art, 72, ring, rr_)]
            for kosten, x, y in roh:
                if not ctx.welt.im_raster_m(x, y):
                    continue
                i, j = ctx.welt.m_zu_ij(x, y)
                if ctx.welt.meer[i, j]:
                    continue
                if ctx.welt.wasser[i, j] > 0 and not any(
                        _sw.in_polygon(np.array([x]), np.array([y]), np.asarray(u, np.float64) / 100.0, 1.5)[0]
                        for u in ausgeblendet):
                    # Bestandswasser, ausser es wird ausgeblendet (houdini, 13f B); 13k: Rand 1,5 m, weil das
                    # Wasserraster am Umriss der ausgeblendeten Flaeche eine Zelle ueberlappt (1 m)
                    continue
                hg = float(ctx.stempel.hang_grad_bei_m(x, y)) if ctx.stempel is not None else 0.0
                if hg > 50.0:
                    continue                    # Standplatz: Augenhoehe auf Fels/Halde, nicht in der Wand
                kand.append((kosten + max(0.0, hg - 30.0) * 0.3, x, y))
            kand.sort(key=lambda t: t[0])
            # zuerst mit voller Planer-Reserve, dann (enge Schluchten, Nischen) mit kleiner Reserve
            for kosten, x, y, rand_ in [(c[0], c[1], c[2], PLANER_RAND_M) for c in kand] + \
                    [(c[0], c[1], c[2], 0.25) for c in kand]:      # 13i Nachtrag: alle, auch der weite Ring
                k2 = list(kam)
                k2[0], k2[1], k2[2] = _daten.feld_von_m(x, y), int(round(x * 100)), int(round(y * 100))
                _bk = pruefe_kamera(k2, ort, ctx.welt, ctx.boden, hind, frei, rand_m=rand_)
                if os.environ.get("SEHENS_DBG_KAM") and os.environ["SEHENS_DBG_KAM"] in name:
                    print("DBGK", round(x), round(y), rand_, (_bk or [("", "ok")])[0][1][:90])
                if not _bk:
                    ctx.melde("HINWEIS", "Kamera %s versetzt (13h): (%.0f, %.0f) -> (%.0f, %.0f) m, %.0f m vom Ziel - "
                                         "vorher: %s" % (name, kam[1] / 100.0, kam[2] / 100.0, x, y,
                                                         math.hypot(x - kam[3] / 100.0, y - kam[4] / 100.0), bef[0][1]))
                    kam = k2
                    bef = []
                    geaendert = True
                    break
        if bef and [x for x in bef if x[0] == "FEHLER"] and regel.get("standplatz_freiraeumen", True) and art != "fern":
            # Standplatz freiraeumen: eigene Pflanzen-Instanzen (Farn, Strauch, Jungwuchs; keine Akteure) am Standplatz
            # und auf dem Strahl entfernen, wenn die Kamera dann frei ist (alte Position zuerst, dann die Kandidaten)
            weich = [h for h in hind if h.get("stueck") is not None and not h["stueck"].get("akteur")
                     and h["stueck"].get("ort") == ctx.id and h["stueck"].get("ebene") in ("bewuchs", "kleinzeug", "kontakt")]
            hart = [h for h in hind if all(h is not w_ for w_ in weich)]
            for x, y in [(kam[1] / 100.0, kam[2] / 100.0)] + [(c[1], c[2]) for c in kand[:80]]:
                k2 = list(kam)
                k2[0], k2[1], k2[2] = _daten.feld_von_m(x, y), int(round(x * 100)), int(round(y * 100))
                if pruefe_kamera(k2, ort, ctx.welt, ctx.boden, hart, frei, rand_m=PLANER_RAND_M):
                    continue
                weg = [w_ for w_ in weich if pruefe_kamera(k2, ort, ctx.welt, ctx.boden, [w_], frei, bestand=False)]
                ids = {id(w_["stueck"]) for w_ in weg}
                ctx.ebene.stuecke = [e for e in ctx.ebene.stuecke if id(e) not in ids]
                for gn in list(ctx.gruppen):
                    ctx.gruppen[gn] = [s_ for s_ in ctx.gruppen[gn] if id(s_.get("stueck")) not in ids]
                ctx.melde("HINWEIS", "Kamera %s: Standplatz freigeraeumt (13h) - %d Pflanzen entfernt, Kamera bei (%.0f, %.0f) m"
                          % (name, len(weg), x, y))
                kam, bef, geaendert = k2, [], True
                hind = hart + [w_ for w_ in weich if id(w_["stueck"]) not in ids]
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
            if str(kam[6]).endswith("_fern"):
                fb_, fi_ = pruefe_fern_achse(kam, o, welt, boden.hoehe, hind, o.get("freiraeume"))
                b += [(st_, oid, t) for st_, t in fb_]
                b.append(("HINWEIS", oid, "Fern-Achse (13k) %s: %d %% der Silhouettenstrahlen frei, Vordergrund %s"
                          % (kam[6], round(100 * fi_["fern_achse_anteil"]), "frei" if fi_["fern_vordergrund_frei"] else "verdeckt")))
        bef, info = pruefe_leuchtfeuer(o, welt, boden.hoehe, hind, o.get("freiraeume"))
        b += [(st_, oid, t) for st_, t in bef]
        if info:
            b.append(("HINWEIS", oid, "Leuchtfeuer (13h): %s" % ", ".join("%s %s" % kv for kv in sorted(info.items()))))
    return b
