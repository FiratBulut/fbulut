# -*- coding: utf-8 -*-
"""detailgrad_bilder.py - Bilder zu Auftrag 20 aus dem Detailgrad-Plan (aufgerufen von detailgrad_plan.py --bild).

  querschnitt_ufer.png  Querschnitt 0-10 m ab der Wasserkante (Prallhang), Zonen Kante/Ufer/Hang, Anzahl je Klasse und Zone (10 m)
  draufsicht_10m.png    Draufsicht 10 m Ufer: Haufen/Luecken-Rhythmus, Steine nach Klasse, Platten, Bewuchs in Ritzen
  stapel_beispiel.png   ein Haufen von der Seite und von oben: 1./2. Lage, gemeinsame Kippung, Eingraben, Schutt in den Fugen
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

FONT_PFADE = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"]
FONT_FETT = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"]


def schrift(g, fett=False):
    for p in (FONT_FETT if fett else FONT_PFADE):
        if os.path.exists(p):
            return ImageFont.truetype(p, g)
    return ImageFont.load_default()


HG = (246, 244, 238)
WASSER = (120, 160, 190)
WASSER_H = (196, 216, 230)
GELAENDE = (150, 128, 96)
FARBE = {"kies": (205, 200, 190), "schutt": (165, 160, 152), "stein": (120, 118, 114), "fussstein": (95, 93, 90),
         "block": (70, 68, 66), "stapel": (88, 84, 80), "platte": (200, 192, 176), "wand": (110, 96, 84), "fels": (80, 72, 66),
         "gras_ritze": (110, 160, 60), "gras_kante": (60, 140, 50), "farn_ritze": (30, 110, 50), "farn": (30, 110, 50),
         "moos_boden": (120, 140, 60), "busch": (70, 120, 60), "gehoelz": (30, 80, 40)}
LAGE2 = (60, 90, 150)
ZONEN = (("Kante", 0.0, 1.0), ("Ufer", 1.0, 3.0), ("Hang", 3.0, 10.0))
KLASSEN = (("K1 Kies < 0,1", lambda e: e["rolle"] == "kies"),
           ("K2 Schutt 0,1-0,3", lambda e: e["rolle"] == "schutt"),
           ("K3 Stein 0,3-1", lambda e: e["rolle"] in ("stein", "fussstein", "block") and 0.3 <= e["g"] < 1.0),
           ("K4 Block 1-3", lambda e: e["rolle"] in ("stein", "fussstein", "block") and e["g"] >= 1.0),
           ("Stapel-Block 1,5-5", lambda e: e["rolle"] == "stapel"),
           ("Platte (Boden)", lambda e: e["rolle"] == "platte"),
           ("Wand / Fels > 3", lambda e: e["rolle"] in ("wand", "fels")),
           ("Gras (Ritze/Kante)", lambda e: e["rolle"] in ("gras_ritze", "gras_kante")),
           ("Farn", lambda e: e["rolle"] in ("farn_ritze", "farn")),
           ("Moos-Polster", lambda e: e["rolle"] == "moos_boden"),
           ("Busch", lambda e: e["rolle"] == "busch"),
           ("Gehoelz", lambda e: e["rolle"] == "gehoelz"))


class Zeichner:
    """ImageDraw mit sortierten Rechteck-/Ellipsen-Ecken (PIL verlangt x0 <= x1, y0 <= y1)."""

    def __init__(self, im):
        self.d = ImageDraw.Draw(im)

    @staticmethod
    def _b(xy):
        if len(xy) == 2:
            (x0, y0), (x1, y1) = xy
        else:
            x0, y0, x1, y1 = xy
        return [min(x0, x1), min(y0, y1), max(x0, x1) + 0.01, max(y0, y1) + 0.01]

    def rectangle(self, xy, **kw):
        self.d.rectangle(self._b(xy), **kw)

    def ellipse(self, xy, **kw):
        self.d.ellipse(self._b(xy), **kw)

    def __getattr__(self, k):
        return getattr(self.d, k)


def fussradius(P, e):
    gx, gy, gz = P.N.gr(e["netz"])
    return 0.5 * math.sqrt(gx * gy) * e["skala"]


def waehle_abschnitt(P, kz):
    """Prallhang-Abschnitt mit einem Haufen mit 2. Lage, moeglichst in der Mitte der Kaskade."""
    best = None
    for k in kz:
        if k["faktor_laenge"] < 0.99:
            continue
        sd = k["seite"]
        a, b = k["s"]
        if P.G.prallseite((a + b) / 2.0) != sd:
            continue
        hauf = {}
        for e in P.inst:
            if e["seite"] == sd and a + 1 <= e["s"] < b - 1 and 0 <= e["haufen"] < 1000:
                hauf.setdefault(e["haufen"], []).append(e)
        for h, L in hauf.items():
            n2 = sum(1 for e in L if e["lage"] == 2)
            sc = (n2 >= 1, len(L), -abs((a + b) / 2.0 - 480.0))
            if best is None or sc > best[0]:
                best = (sc, sd, a, b, h)
    return best[1:]


# ======================================================================================================================
def querschnitt(P, sd, a, b, h, aus):
    G = P.G
    sg = 1.0 if sd == "links" else -1.0
    L = [e for e in P.inst if e["seite"] == sd and e["haufen"] == h]
    s0 = sum(e["s"] for e in L) / len(L)
    W = G.spiegel(s0, sg)
    m = 120
    x0, y0 = 90, 120
    dmin, dmax = -1.5, 10.8
    zs = [G.z(s0, G.u_von(s0, sg, d * 0.1)) - W for d in range(int(dmin * 10), int(dmax * 10) + 1)]
    zmax = max(zs) + 1.2
    zmin = -1.0
    Wd = int((dmax - dmin) * m) + x0 + 40
    Ht = int((zmax - zmin) * m) + y0 + 60
    tab_h = 90 + 28 * len(KLASSEN)
    im = Image.new("RGB", (Wd, Ht + tab_h), HG)
    dr = Zeichner(im)

    def px(d, z):
        return x0 + (d - dmin) * m, y0 + (zmax - z) * m
    # Zonen
    for (nm, d0, d1), c in zip(ZONEN, ((236, 232, 222), (228, 224, 212), (238, 236, 230))):
        dr.rectangle([px(d0, zmax)[0], y0, px(d1, zmax)[0], Ht], fill=c)
        dr.text((px(d0, zmax)[0] + 4, y0 + 6 + (22 if nm == "Kante" else 0)), "%s %g-%g m" % (nm, d0, d1), fill=(60, 60, 60), font=schrift(18, True))
    dr.line([px(10, zmin), px(10, zmax)], fill=(200, 60, 60), width=3)
    dr.text((px(10, zmax)[0] - 210, y0 + 34), "Grenze Auftrag 21 (10 m)", fill=(180, 40, 40), font=schrift(15))
    # Wasser
    poly = [px(dmin, 0.0)]
    d_end = dmin
    for i, z in enumerate(zs):
        d_end = dmin + i * 0.1
        poly.append(px(d_end, min(z, 0.0)))
        if z > 0:
            break
    poly.append(px(d_end, 0.0))
    dr.polygon(poly, fill=WASSER_H)
    dr.line([px(dmin, 0), px(d_end, 0)], fill=WASSER, width=3)
    # Gelaende
    pts = [px(dmin + i * 0.1, z) for i, z in enumerate(zs)]
    dr.polygon(pts + [px(dmax, zmin), px(dmin, zmin)], fill=(214, 200, 176))
    dr.line(pts, fill=GELAENDE, width=3)
    # Instanzen im Streifen +-0,8 m
    sel = [e for e in P.inst if e["seite"] == sd and abs(e["s"] - s0) <= 0.8 and dmin <= e["d"] <= dmax]
    sel.sort(key=lambda e: -abs(e["s"] - s0))
    for e in sel:
        zt = e["zt"] - W
        z = e["z"] - W
        r = e["rolle"]
        if r in ("platte",):
            rr = fussradius(P, e) * 0.85
            dick = max(0.03, e["top"] - e["zt"])
            sg = 1.0 if sd == "links" else -1.0
            pts = []
            for k in range(11):
                d = e["d"] - rr + 2 * rr * k / 10.0
                pts.append(px(d, G.z(s0, G.u_von(s0, sg, d)) - W + dick / 2.0))
            dr.line(pts, fill=(170, 160, 140), width=max(3, int(dick * m)))
            continue
        if r in ("gras_ritze", "gras_kante", "farn_ritze", "farn", "busch", "moos_boden"):
            hh = e["h"] if r != "moos_boden" else 0.08
            bx, by = px(e["d"], zt)
            dr.polygon([(bx - 0.18 * m, by), (bx + 0.18 * m, by), (bx, by - hh * m)], fill=FARBE[r])
            continue
        if r == "gehoelz":
            bx, by = px(e["d"], zt)
            dr.line([(bx, by), (bx, by - 2.2 * m)], fill=(90, 60, 40), width=8)
            dr.ellipse([bx - 0.9 * m, by - 4.0 * m, bx + 0.9 * m, by - 1.6 * m], fill=FARBE[r])
            continue
        rr = 0.5 * e["g"] if r not in ("wand", "fels") else fussradius(P, e)
        c = LAGE2 if e["lage"] == 2 else FARBE[r]
        dr.ellipse([px(e["d"] - rr, 0)[0], px(0, z + e["h"])[1], px(e["d"] + rr, 0)[0], px(0, z)[1]], fill=c,
                   outline=(40, 40, 40))
        if e["einb"] > 0.05 and e["lage"] == 1:
            yy = px(0, zt)[1]
            dr.line([(px(e["d"] - rr, 0)[0], yy), (px(e["d"] + rr, 0)[0], yy)], fill=(230, 230, 230), width=2)
    # Achsen
    for d in range(-1, 11):
        x, y = px(d, zmin)
        dr.line([(x, y), (x, y - 8)], fill=(0, 0, 0), width=2)
        dr.text((x - 8, y + 4), "%d" % d, fill=(0, 0, 0), font=schrift(15))
    for z in range(0, int(zmax) + 1):
        x, y = px(dmin, z)
        dr.line([(x, y), (x + 8, y)], fill=(0, 0, 0), width=2)
        dr.text((x - 50, y - 9), "%+d m" % z, fill=(0, 0, 0), font=schrift(15))
    dr.text((x0, 20), "Querschnitt Ufer 0-10 m, %s (Prallhang), s = %.1f m (Talkaskade p2), Streifen +-0,8 m" % (sd, s0),
            fill=(0, 0, 0), font=schrift(24, True))
    dr.text((x0, 56), "z relativ zum Spiegel; d = Abstand ab Wasserkante. Ellipse = Netz (Hoehe = Netzhoehe x Skala), "
            "weisser Strich = Gelaende (eingegraben darunter), blau = 2. Lage", fill=(40, 40, 40), font=schrift(16))
    # Tabelle: Anzahl je Klasse und Zone im Abschnitt (10 m)
    ty = Ht + 20
    dr.text((x0, ty), "Anzahl je Klasse und Zone, Abschnitt s %.0f-%.0f m, %s (Plan; Soll je 10 m im Band 0-3 m: K3 26-36, K2 50-65 bis 2 x K3, "
            "K4 3-5)" % (a, b, sd), fill=(0, 0, 0), font=schrift(17, True))
    cols = [x0, x0 + 260, x0 + 420, x0 + 580, x0 + 740, x0 + 900]
    ty += 34
    for c, t in zip(cols, ("Klasse", "Kante 0-1", "Ufer 1-3", "Hang 3-10", "0-3 m", "0-10 m")):
        dr.text((c, ty), t, fill=(0, 0, 0), font=schrift(16, True))
    for nm, f in KLASSEN:
        ty += 28
        vals = []
        for d0, d1 in ((-0.6, 1.0), (1.0, 3.0), (3.0, 10.0), (-0.6, 3.0), (-0.6, 10.0)):
            vals.append(sum(1 for e in P.inst if e["seite"] == sd and a <= e["s"] < b and d0 < e["d"] <= d1 and f(e)
                            and e["haufen"] != -11))
        dr.text((cols[0], ty), nm, fill=(0, 0, 0), font=schrift(16))
        for c, v in zip(cols[1:], vals):
            dr.text((c, ty), "%d" % v, fill=(0, 0, 0), font=schrift(16))
    im.save(os.path.join(aus, "querschnitt_ufer.png"), optimize=True)


# ======================================================================================================================
def draufsicht(P, sd, a, b, aus):
    m = 120
    x0, y0 = 80, 190
    dmin, dmax = -1.5, 10.5
    Wd = int((b - a) * m) + x0 + 40
    Ht = int((dmax - dmin) * m) + y0 + 150
    im = Image.new("RGB", (Wd, Ht), HG)
    dr = Zeichner(im)

    def px(s, d):
        return x0 + (s - a) * m, y0 + (dmax - d) * m
    dr.rectangle([px(a, 0), px(b, dmin)], fill=WASSER_H)
    for d in (1.0, 3.0, 10.0):
        dr.line([px(a, d), px(b, d)], fill=(200, 60, 60) if d == 10 else (150, 150, 150), width=2)
    for nm, d0, d1 in ZONEN:
        dr.text((x0 + 6, px(a, (d0 + d1) / 2)[1] - 10), nm, fill=(90, 90, 90), font=schrift(18, True))
    sel = [e for e in P.inst if e["seite"] == sd and a - 1.5 <= e["s"] < b + 1.5 and dmin <= e["d"] <= dmax]
    reihen = ("platte", "wand", "fels", "moos_boden", "stapel", "stein", "fussstein", "block", "kies", "schutt", "gras_ritze", "gras_kante",
              "farn_ritze", "farn", "busch", "gehoelz")
    for r in reihen:
        for e in sel:
            if e["rolle"] != r:
                continue
            x, y = px(e["s"], e["d"])
            if r in ("platte", "wand", "fels"):
                gx, gy, gz = P.N.gr(e["netz"])
                hx, hy = 0.5 * gx * e["skala"] * 0.85 * m, 0.5 * gy * e["skala"] * 0.85 * m
                w = math.radians(e["yaw"])
                pts = []
                for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                    pts.append((x + sx * hx * math.cos(w) - sy * hy * math.sin(w), y - (sx * hx * math.sin(w) + sy * hy * math.cos(w))))
                dr.polygon(pts, fill=FARBE[r], outline=(170, 160, 140))
            elif r in ("gras_ritze", "gras_kante", "farn_ritze", "farn", "busch", "moos_boden", "gehoelz"):
                rr = {"gras_ritze": 0.14, "gras_kante": 0.25, "farn_ritze": 0.3, "farn": 0.3, "busch": 0.5, "moos_boden": 0.35,
                      "gehoelz": 0.8}[r] * m
                c = (180, 150, 70) if e.get("trocken") else FARBE[r]
                if r in ("farn_ritze", "farn"):
                    for k in range(6):
                        w = k * math.pi / 3
                        dr.line([(x, y), (x + rr * math.cos(w), y + rr * math.sin(w))], fill=c, width=5)
                else:
                    dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=c, outline=(30, 60, 30))
            else:
                rr = fussradius(P, e) * m * max(0.15, 1.0 - e["einb"]) ** 0.3
                c = LAGE2 if e["lage"] == 2 else FARBE[r]
                dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=c, outline=(30, 30, 30), width=2 if r != "kies" else 1)
    dr.rectangle([0, 0, Wd, y0 - 6], fill=HG)
    dr.rectangle([0, 0, x0 - 2, Ht], fill=HG)
    dr.rectangle([px(b, 0)[0] + 2, 0, Wd, Ht], fill=HG)
    # Rhythmus-Leiste
    for (x0_, x1_, art, prall) in P.rhythmus[sd]:
        if x1_ < a or x0_ > b:
            continue
        c = (120, 118, 114) if art == "haufen" else (150, 190, 110)
        dr.rectangle([px(max(x0_, a), 0)[0], y0 - 60, px(min(x1_, b), 0)[0], y0 - 30], fill=c, outline=(40, 40, 40))
        if min(x1_, b) - max(x0_, a) > 0.8:
            dr.text((px(max(x0_, a), 0)[0] + 4, y0 - 58), "Haufen" if art == "haufen" else "Luecke", fill=(255, 255, 255)
                    if art == "haufen" else (20, 60, 20), font=schrift(15))
    for (x0_, x1_) in P.grasluecken[sd]:
        if x0_ < b and x1_ > a:
            dr.rectangle([px(max(x0_, a), 0)[0], y0 - 26, px(min(x1_, b), 0)[0], y0 - 14], fill=(60, 140, 50))
    for s in range(int(math.ceil(a)), int(b) + 1):
        x, y = px(s, dmin)
        dr.line([(x, y), (x, y + 8)], fill=(0, 0, 0), width=2)
        dr.text((x - 16, y + 10), "%d" % s, fill=(0, 0, 0), font=schrift(15))
    for d in range(-1, 11):
        x, y = px(a, d)
        dr.text((x0 - 50, y - 9), "%d m" % d, fill=(0, 0, 0), font=schrift(15))
    dr.text((x0, 16), "Draufsicht 10 m Ufer: %s, s %.0f-%.0f m (Talkaskade p2) - Haufen/Luecken-Rhythmus" % (sd, a, b),
            fill=(0, 0, 0), font=schrift(24, True))
    for i, t in enumerate(("Leiste: grau = Haufen (5-15 Stueck), gruen = Luecke (Farn/Gras), dunkelgruen = Grasluecke mit Ueberhang.",
                           "Kreise: hell Kies, grau Schutt, mittel Stein 0,3-1 m, dunkel Block/Stapel/Fuss im Wasser, blau 2. Lage;"
                           " Rechtecke = Bodenplatten/Wand.",
                           "Gruen: Gras in Ritzen (ocker = trocken), Stern = Farn, gross = Busch/Gehoelz, oliv = Moos (>= 1 m ueber"
                           " Spiegel). Rote Linie = Grenze Auftrag 21.")):
        dr.text((x0, 50 + 22 * i), t, fill=(40, 40, 40), font=schrift(15))
    im.save(os.path.join(aus, "draufsicht_10m.png"), optimize=True)


# ======================================================================================================================
def stapel(P, sd, h, aus):
    L = [e for e in P.inst if e["seite"] == sd and e["haufen"] == h]
    st = [e for e in L if e["rolle"] in ("stein", "fussstein", "block")]
    sch = [e for e in L if e["rolle"] == "schutt"]
    pl = [e for e in L if e["rolle"] == "platte"]
    sa, sb = min(e["s"] for e in L) - 0.8, max(e["s"] for e in L) + 0.8
    zmin = min(e["z"] for e in L) - 0.3
    zmax = max(e["top"] for e in L) + 0.3
    m = 220
    x0, y0 = 80, 130
    Wd = max(int((sb - sa) * m) + x0 + 60, 1500)
    H1 = int((zmax - zmin) * m)
    dmin = min(e["d"] for e in L) - 0.8
    dmax = max(e["d"] for e in L) + 0.8
    H2 = int((dmax - dmin) * m)
    Ht = y0 + H1 + 90 + H2 + 160
    im = Image.new("RGB", (Wd, Ht), HG)
    dr = Zeichner(im)

    def ps(s, z):
        return x0 + (s - sa) * m, y0 + (zmax - z) * m
    # Seitenansicht (Blick quer zum Bach, s nach rechts): Gelaende-Mittel + Steine
    srt = sorted(st, key=lambda e: -e["d"])
    for e in srt:
        rr = 0.5 * e["g"]
        c = LAGE2 if e["lage"] == 2 else FARBE[e["rolle"]]
        dr.ellipse([ps(e["s"] - rr, 0)[0], ps(0, e["top"])[1], ps(e["s"] + rr, 0)[0], ps(0, e["z"])[1]], fill=c, outline=(30, 30, 30),
                   width=2)
        if e["lage"] == 1:
            y = ps(0, e["zt"])[1]
            dr.line([(ps(e["s"] - rr, 0)[0], y), (ps(e["s"] + rr, 0)[0], y)], fill=(150, 110, 70), width=3)
    for e in sch:
        rr = 0.5 * e["g"]
        dr.ellipse([ps(e["s"] - rr, 0)[0], ps(0, e["top"])[1], ps(e["s"] + rr, 0)[0], ps(0, e["z"])[1]], fill=FARBE["schutt"],
                   outline=(60, 60, 60))
    dr.text((x0, y0 - 40), "Seitenansicht (quer zum Bach): braune Striche = Gelaende am Stein (Teil darunter eingegraben), blau = "
            "2. Lage verkeilt (35 % der Hoehe in der 1. Lage)", fill=(40, 40, 40), font=schrift(16))
    # Draufsicht
    yb = y0 + H1 + 90

    def pd(s, d):
        return x0 + (s - sa) * m, yb + (dmax - d) * m
    for e in pl:
        gx, gy, gz = P.N.gr(e["netz"])
        hx, hy = 0.5 * gx * e["skala"] * 0.85 * m, 0.5 * gy * e["skala"] * 0.85 * m
        x, y = pd(e["s"], e["d"])
        w = math.radians(e["yaw"])
        pts = [(x + sx * hx * math.cos(w) - sy * hy * math.sin(w), y - (sx * hx * math.sin(w) + sy * hy * math.cos(w)))
               for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        dr.polygon(pts, fill=FARBE["platte"], outline=(170, 160, 140))
    for e in sorted(st, key=lambda e: e["lage"]) + sch:
        x, y = pd(e["s"], e["d"])
        rr = fussradius(P, e) * m * (max(0.15, 1.0 - e["einb"]) ** 0.3)
        c = LAGE2 if e["lage"] == 2 else FARBE[e["rolle"]]
        dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=c, outline=(30, 30, 30), width=2)
        if e["rolle"] != "schutt":
            w = math.radians(e["yaw"])
            dr.line([(x, y), (x + 0.8 * rr * math.cos(w), y - 0.8 * rr * math.sin(w))], fill=(255, 255, 255), width=3)
    dr.line([pd(sa, 0.0), pd(sb, 0.0)], fill=WASSER, width=4)
    dr.text((x0, yb - 40), "Draufsicht: helle Flaeche = Bodenplatte unter dem Haufen, weisser Strich = Drehung (gemeinsame "
            "Fallrichtung +- 20 Grad), blaue Linie = Wasserkante", fill=(40, 40, 40), font=schrift(16))
    n1 = sum(1 for e in st if e["lage"] == 1)
    n2 = sum(1 for e in st if e["lage"] == 2)
    kipp = [e["kipp"] for e in st]
    einb = [e["einb"] for e in st if e["lage"] == 1]
    dr.text((x0, 20), "Stapel-Beispiel: Haufen %d, %s (Prallhang), s %.1f-%.1f m" % (h, sd, sa + 0.8, sb - 0.8), fill=(0, 0, 0),
            font=schrift(24, True))
    dr.text((x0, 56), "%d Steine 1. Lage + %d in 2. Lage, %d Schutt in den Fugen, %d Bodenplatte; Kippung %.0f-%.0f Grad; "
            "eingegraben 1. Lage %.0f-%.0f %% der Netzhoehe" % (n1, n2, len(sch), len(pl), min(kipp), max(kipp), 100 * min(einb),
                                                                100 * max(einb)), fill=(0, 0, 0), font=schrift(17))
    dr.text((x0, Ht - 60), "Massstab: 1 m = %d px. Werte aus plan_p2_talkaskade.json (Spalten haufen, lage, kipp_grad, einbettung)." % m,
            fill=(60, 60, 60), font=schrift(15))
    im.save(os.path.join(aus, "stapel_beispiel.png"), optimize=True)


def alle(P, abschnitte, kz, out, aus):
    sd, a, b, h = waehle_abschnitt(P, kz)
    querschnitt(P, sd, a, b, h, aus)
    draufsicht(P, sd, a, b, aus)
    stapel(P, sd, h, aus)
    return sd, a, b, h
