# -*- coding: utf-8 -*-
"""p2_bett_bilder.py - Bilder zum p2-Bettplan (16h Nachtrag 6c), nur PIL/NumPy.

  talkaskade_delta.png        Draufsicht abgewickelt (x = s, y = u): Gelaende neu - Ist (blau Abtrag, rot Auftrag)
  talkaskade_tiefe.png        Draufsicht abgewickelt: Wassertiefe neu, Lippen, Kerben, Kolke, Bloecke
  talkaskade_laengsprofil.png Laengsschnitt (Spiegel alt/neu, Narbe, Talweg), Hoehen relativ zur Tal-Trendlinie
  talkaskade_querschnitte.png 8 Querschnitte (Ist, Soll, Wasser)
Ist im alten Bett ist ANGENOMMEN (Ferats Kennzahlen, Kasten-U); die Ufer stammen aus querschnitte_p2.json.
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SK = 2                       # intern doppelt zeichnen, dann verkleinern (glatte Linien)
FLAECHE = (252, 252, 251)
TINTE = (11, 11, 11)
TINTE2 = (82, 81, 78)
GITTER = (226, 225, 221)
NEUTRAL = (240, 239, 236)
BLAU = (42, 120, 214)
BLAU_D = (16, 66, 129)
ROT = (227, 73, 72)
ROT_D = (130, 30, 30)
GRUEN = (0, 131, 0)
GRAU = (138, 137, 134)
FONT_PFADE = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"]


def schrift(g):
    for p in FONT_PFADE:
        if os.path.exists(p):
            return ImageFont.truetype(p, g * SK)
    return ImageFont.load_default()


def lerp_farbe(a, b, t):
    t = np.clip(t, 0.0, 1.0)[..., None]
    return np.asarray(a, float) * (1 - t) + np.asarray(b, float) * t


def divergent(d, grenze=2.0):
    """Abtrag blau, Auftrag rot, |d| < 5 cm neutral grau."""
    t = np.clip(np.abs(d) / grenze, 0, 1) ** 0.7
    neg = np.where(t[..., None] < 0.5, lerp_farbe(NEUTRAL, (110, 160, 228), t * 2), lerp_farbe((110, 160, 228), BLAU_D, t * 2 - 1))
    pos = np.where(t[..., None] < 0.5, lerp_farbe(NEUTRAL, (236, 140, 130), t * 2), lerp_farbe((236, 140, 130), ROT_D, t * 2 - 1))
    out = np.where((d < 0)[..., None], neg, pos)
    out[np.abs(d) < 0.05] = NEUTRAL
    return out


def sequenz(t):
    stufen = [(205, 226, 251), (134, 182, 239), (57, 135, 229), (37, 106, 191), (16, 66, 129), (13, 54, 107)]
    t = np.clip(t, 0, 1) * (len(stufen) - 1)
    i = np.clip(np.floor(t).astype(int), 0, len(stufen) - 2)
    f = (t - i)[..., None]
    a = np.array(stufen, float)
    return a[i] * (1 - f) + a[i + 1] * f


class Leinwand:
    def __init__(self, b, h):
        self.im = Image.new("RGB", (b * SK, h * SK), FLAECHE)
        self.d = ImageDraw.Draw(self.im)

    def text(self, x, y, t, g=13, farbe=TINTE, anker="la"):
        self.d.text((x * SK, y * SK), t, fill=farbe, font=schrift(g), anchor=anker)

    def linie(self, pts, farbe, w=1, strich=None):
        P = [(x * SK, y * SK) for x, y in pts]
        if strich is None:
            self.d.line(P, fill=farbe, width=max(1, int(w * SK)), joint="curve")
            return
        for (x0, y0), (x1, y1) in zip(P, P[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            n = max(1, int(L / (strich * SK * 2)))
            for k in range(n):
                a, b = k / n, (k + 0.5) / n
                self.d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)],
                            fill=farbe, width=max(1, int(w * SK)))

    def kreis(self, x, y, r, farbe, rand=None):
        self.d.ellipse([(x - r) * SK, (y - r) * SK, (x + r) * SK, (y + r) * SK], fill=farbe, outline=rand,
                       width=SK if rand else 0)

    def rechteck(self, x0, y0, x1, y1, farbe=None, rand=None, w=1):
        self.d.rectangle([x0 * SK, y0 * SK, x1 * SK, y1 * SK], fill=farbe, outline=rand, width=w * SK)

    def bild(self, arr, x, y):
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
        im = im.resize((im.width * SK, im.height * SK), Image.NEAREST)
        self.im.paste(im, (x * SK, y * SK))

    def speichern(self, pfad):
        self.im.resize((self.im.width // SK, self.im.height // SK), Image.LANCZOS).save(pfad, optimize=True)


# ----------------------------------------------------------------------------------------------------------------------
def _streifen(X, n=3):
    S = X["G"]["S"]
    a, b = float(S[0]), float(S[-1])
    L = (b - a) / n
    return [(a + i * L, a + (i + 1) * L) for i in range(n)]


def _karte(X, farbe_fn, titel, legende_fn, pfad, unterzeile):
    G = X["G"]
    S, U = G["S"], G["U"]
    pxm = 20
    umax = 9.0
    rand_l, rand_r = 56, 16
    streifen = _streifen(X)
    sl = max(b - a for a, b in streifen)
    breite = int(sl * pxm) + rand_l + rand_r
    hoehe_str = int(2 * umax * pxm)
    kopf = 70
    fuss = 110
    Lw = Leinwand(breite, kopf + len(streifen) * (hoehe_str + 46) + fuss)
    Lw.text(rand_l, 16, titel, 17)
    Lw.text(rand_l, 42, unterzeile, 12, TINTE2)
    rgb_alle = farbe_fn()
    ju = np.nonzero(np.abs(U) <= umax + 1e-9)[0]
    for k, (a, b) in enumerate(streifen):
        y0 = kopf + k * (hoehe_str + 46)
        ii = np.nonzero((S >= a - 1e-9) & (S <= b + 1e-9))[0]
        sub = rgb_alle[np.ix_(ii, ju)]                    # [s, u]
        img = np.transpose(sub, (1, 0, 2))[::-1]          # Zeilen: u von oben (links, +) nach unten
        img = np.repeat(np.repeat(img, int(round(pxm * 0.25)), axis=0), int(round(pxm * 0.5)), axis=1)
        Lw.bild(img, rand_l, y0)

        def px(s, u):
            return rand_l + (s - S[ii[0]]) * pxm, y0 + (umax - u) * pxm + 0.25 * pxm / 2

        # Kanten neu
        for E_ in (G["EL"], G["ER"]):
            Lw.linie([px(S[i], E_[i]) for i in ii], TINTE, 1.2)
        # alte Kante (Planbreite)
        Bo = np.interp(S[ii], X["ist"].s, X["ist"].B)
        for sg in (1, -1):
            Lw.linie([px(S[i], sg * Bo[n] / 2) for n, i in enumerate(ii)], GRAU, 1, strich=4)
        # Lippen
        for j, L in enumerate(X["lippen"]):
            if L.art == "bestand" or not (a - 1 <= L.s <= b + 1):
                continue
            h = L.Bl / 2 + 0.6
            uu = np.linspace(L.uc - h, L.uc + h, 15)
            pts = [px(float(L.linie(u, L.uc)), u) for u in uu]
            pts = [p for p in pts if rand_l <= p[0] <= rand_l + sl * pxm]
            if len(pts) > 1:
                Lw.linie(pts, (40, 40, 40), 2.2)
            for ur, w, _ in L.kerben[:1]:
                x_, y_ = px(float(L.linie(L.uc + ur, L.uc)), L.uc + ur)
                if rand_l <= x_ <= rand_l + sl * pxm:
                    Lw.kreis(x_, y_, 3.5, (255, 255, 255), TINTE)
        # Kolke
        for bk in X["becken"]:
            Kk = bk["kolk"]
            if a <= Kk["s"] <= b:
                x_, y_ = px(Kk["s"], Kk["u"])
                Lw.d.ellipse([(x_ - Kk["a_up"] * pxm) * SK, (y_ - Kk["w"] / 2 * pxm) * SK,
                              (x_ + Kk["a_dn"] * pxm) * SK, (y_ + Kk["w"] / 2 * pxm) * SK], outline=(255, 255, 255),
                             width=SK)
        # Bloecke
        for x in X["liste"]:
            if x["rolle"] == "kies" or not (a <= x["s"] <= b):
                continue
            x_, y_ = px(x["s"], x["u"])
            Lw.kreis(x_, y_, max(1.8, x["g"] * pxm * 0.35), (70, 66, 60), (255, 255, 255))
        # Achsen
        Lw.rechteck(rand_l, y0, rand_l + (S[ii[-1]] - S[ii[0]]) * pxm + pxm * 0.5, y0 + hoehe_str, None, GITTER)
        for s in range(int(math.ceil(a / 10.0) * 10), int(b) + 1, 10):
            x_, _ = px(s, 0)
            Lw.linie([(x_, y0 + hoehe_str), (x_, y0 + hoehe_str + 5)], TINTE2, 1)
            Lw.text(x_, y0 + hoehe_str + 7, "s %d" % s, 11, TINTE2, "ma")
        for u in (-8, -4, 0, 4, 8):
            _, y_ = px(S[ii[0]], u)
            Lw.text(rand_l - 6, y_, ("%+d" % u) if u else "0", 11, TINTE2, "rm")
        Lw.text(6, y0 + 4, "links", 10, TINTE2)
        Lw.text(6, y0 + hoehe_str - 14, "rechts", 10, TINTE2)
    legende_fn(Lw, rand_l, kopf + len(streifen) * (hoehe_str + 46) + 6)
    Lw.speichern(pfad)


def bild_delta(X, pfad):
    G = X["G"]
    d = X["z_neu"] - X["ist_z"]

    def farbe():
        rgb = divergent(d)
        rgb[G["WG"] <= 0.0] = FLAECHE
        return rgb

    def leg(Lw, x, y):
        w = 360
        werte = np.linspace(-2, 2, w)
        bar = divergent(np.tile(werte, (14, 1)))
        Lw.bild(bar, x, y + 18)
        Lw.text(x, y, "Gelaende neu - Ist (m)", 12)
        for v in (-2, -1, 0, 1, 2):
            Lw.text(x + (v + 2) / 4 * w, y + 36, ("%+d" % v) if v else "0", 11, TINTE2, "ma")
        Lw.text(x, y + 54, "blau = Abtrag (Bett, Kolke, zurueckgelegte Boeschung)   rot = Auftrag (Schulter, Lippen-Einschnuerung)",
                11, TINTE2)
        Lw.text(x, y + 72, "Linien: schwarz = neue Bettkante, grau gestrichelt = alte Planbreite, dunkel dick = Lippe, "
                           "weisser Punkt = Hauptkerbe, Ellipse = Kolk, Punkte = Bloecke", 11, TINTE2)
        Lw.text(x + 400, y + 18, "Ist im alten Bett ANGENOMMEN (Kasten-U, 1,0 -> 0,55 m); Ufer aus querschnitte_p2.json",
                11, ROT_D)

    nz = X["kennzahlen"]["neu"]
    _karte(X, farbe, "Erlenbach p2, Talkaskade: Delta-Karte des neuen Bettplans (abgewickelt, x = s, y = u)", leg, pfad,
           "%d Einheiten, %d Lippen, Abtrag ~%d m3, Auftrag ~%d m3 (geschaetzt). 1 m = 20 px." %
           (nz["einheiten"], nz["lippen"], nz["abtrag_m3_geschaetzt"], nz["auftrag_m3_geschaetzt"]))


def bild_tiefe(X, pfad):
    G = X["G"]
    t = G["W"] - X["z_neu"]
    z = X["z_neu"]
    gs, gu = np.gradient(z, 0.5, 0.25)
    hang = np.degrees(np.arctan(np.hypot(gs - 0.29, gu)))     # Hang ohne Talgefaelle (Uferstufe sichtbar)
    schatten = np.clip(1.0 - hang / 110.0, 0.68, 1.0)

    def farbe():
        land = np.array([214, 206, 186], float)[None, None, :] * schatten[..., None]
        rgb = np.where((t > 0.01)[..., None], sequenz(t / 1.2), land)
        rgb[G["WG"] <= 0.0] = FLAECHE
        return rgb

    def leg(Lw, x, y):
        w = 300
        bar = sequenz(np.tile(np.linspace(0, 1, w), (14, 1)))
        Lw.bild(bar, x, y + 18)
        Lw.text(x, y, "Wassertiefe neu (m)", 12)
        for v in (0, 0.4, 0.8, 1.2):
            Lw.text(x + v / 1.2 * w, y + 36, ("%.1f" % v).replace(".", ","), 11, TINTE2, "ma")
        Lw.text(x, y + 54, "Land: hell = flach, dunkel = steil (Uferstufe, Boeschung, Stufenwand).  Becken 0,8-1,2 m, "
                           "Rinne an der Hauptkerbe 0,2-0,4 m, Uferstufe 0,2-0,5 m.", 11, TINTE2)
        Lw.text(x, y + 72, "Kolk (Ellipse) direkt unter der Hauptkerbe der oberen Lippe, laenglich, Talweg wandert zur Kerbe der "
                           "naechsten Lippe.", 11, TINTE2)

    _karte(X, farbe, "Erlenbach p2, Talkaskade: Wassertiefe und Formen (abgewickelt, x = s, y = u)", leg, pfad,
           "Spiegel waagrecht je Becken; die SWR rechnet den echten Spiegel beim Backen.")


def bild_laengs(X, pfad):
    G = X["G"]
    S, U, W = G["S"], G["U"], G["W"]
    ist = X["ist"]
    T = np.interp(S, ist.s, ist.T)
    k = np.polyfit(S, T, 1)
    trend = np.polyval(k, S)
    j0 = int(np.argmin(np.abs(U)))
    sp_neu = W[:, j0]
    sp_alt = np.array([ist.spiegel_alt(s) for s in S])
    zb = np.where(G["innen"], X["z_neu"], np.inf).min(axis=1)
    zb_alt = np.where(np.abs(U)[None, :] <= 0.3, X["ist_z"], np.inf).min(axis=1)
    halb = [(S[0], (S[0] + S[-1]) / 2), ((S[0] + S[-1]) / 2, S[-1])]
    B, Hp = 1500, 330
    rl, top = 70, 70
    Lw = Leinwand(B, top + 2 * (Hp + 50) + 90)
    Lw.text(rl, 16, "Erlenbach p2, Talkaskade: Laengsschnitt, Hoehe relativ zur Tal-Trendlinie (Gefaelle %.0f %%)" %
            (-100 * k[0]), 17)
    Lw.text(rl, 42, "So sind 0,3-m-Stufen auf 56 m Gesamtfall lesbar. Narbe = Gelaende 1,5 m neben der alten Kante "
                    "(Minimum beider Seiten, geglaettet).", 12, TINTE2)
    ylo, yhi = -4.5, 1.5
    for n, (a, b) in enumerate(halb):
        y0 = top + n * (Hp + 50)
        m = (S >= a) & (S <= b)
        xs = lambda s: rl + (s - a) / (b - a) * (B - rl - 20)
        ys = lambda z: y0 + (yhi - z) / (yhi - ylo) * Hp
        for g in range(int(ylo), int(yhi) + 1):
            Lw.linie([(rl, ys(g)), (B - 20, ys(g))], GITTER, 1)
            Lw.text(rl - 8, ys(g), "%+d m" % g if g else "0", 11, TINTE2, "rm")
        for s in range(int(math.ceil(a / 10) * 10), int(b) + 1, 10):
            Lw.text(xs(s), y0 + Hp + 6, "s %d" % s, 11, TINTE2, "ma")
        # Einheiten-Klassen oben
        for e in X["EH"][1:]:
            if a <= e["a"] <= b:
                kurz = {"kurz": "k", "mittel": "m", "lang": "L", "ruhig": "R"}[e["klasse"]]
                Lw.text(xs((e["a"] + min(e["b"], b)) / 2), y0 + 4, kurz, 11, TINTE2 if kurz != "R" else BLAU_D, "ma")
        ss = S[m]
        Lw.linie([(xs(s), ys(z)) for s, z in zip(ss, (T - trend)[m])], GRUEN, 1.6)
        Lw.linie([(xs(s), ys(z)) for s, z in zip(ss, (sp_alt - trend)[m])], GRAU, 1.4, strich=3)
        Lw.linie([(xs(s), ys(z)) for s, z in zip(ss, (zb_alt - trend)[m])], GRAU, 1, strich=2)
        Lw.linie([(xs(s), ys(z)) for s, z in zip(ss, (zb - trend)[m])], TINTE, 1.4)
        Lw.linie([(xs(s), ys(z)) for s, z in zip(ss, (sp_neu - trend)[m])], BLAU, 2.4)
    y = top + 2 * (Hp + 50) - 10
    items = [(BLAU, "Spiegel neu (u = 0, fuer die SWR-Spline)", None), (TINTE, "Talweg neu (tiefster Bettpunkt)", None),
             (GRUEN, "Grasnarbe (Ist)", None), (GRAU, "Spiegel alt (2-m-Schnitte)", 3),
             (GRAU, "Bett alt (angenommen)", 2)]
    x = rl
    for f, t, st in items:
        Lw.linie([(x, y + 8), (x + 26, y + 8)], f, 2.2, strich=st)
        Lw.text(x + 32, y + 1, t, 11, TINTE2)
        x += 50 + len(t) * 6.4
    Lw.text(rl, y + 26, "Buchstaben oben: Einheit k = kurz (1-1,3 B), m = mittel, L = lang, R = ruhige Strecke (3-4 B).",
            11, TINTE2)
    Lw.speichern(pfad)


def bild_quer(X, pfad):
    G = X["G"]
    S, U, W = G["S"], G["U"], G["W"]
    bk = X["becken"]
    wahl = []
    haupt = [b for b in bk if b["typ"] == "haupt"]
    ruhig_k = {e["k"] for e in X["EH"] if e["klasse"] == "ruhig"}
    r_b = [b for b in haupt if X["lippen"][b["oben"]].einheit in ruhig_k]
    for b in (r_b[:1] + haupt[2:3] + haupt[len(haupt) // 2:len(haupt) // 2 + 1]):
        wahl.append((b["kolk"]["s"], "Kolk Becken %d (%s)" % (b["nr"], "ruhig" if b in r_b else "Hauptbecken")))
    for b in haupt[3:4] + r_b[:1]:
        N_ = X["lippen"][b["unten"]]
        wahl.append(((b["kolk"]["s"] + N_.s) / 2, "Auslauf Becken %d" % b["nr"]))
    for L in [L for L in X["lippen"] if L.art == "stufe"][:1] + [L for L in X["lippen"] if L.art == "kaskade_teil"][3:4]:
        wahl.append((L.s - 0.25, "Lippe %d (%s, Fall %.1f m)" % (L.nr, L.art, L.D)))
    tb = [b for b in bk if b["typ"] == "teil"]
    if tb:
        wahl.append((tb[len(tb) // 2]["kolk"]["s"], "Teilbecken %d (Kaskade)" % tb[len(tb) // 2]["nr"]))
    gesehen, w2 = set(), []
    for s, ti in sorted(wahl):
        k = round(s * 2)
        if k not in gesehen:
            gesehen.add(k)
            w2.append((s, ti))
    rest = [b for b in haupt if round(b["kolk"]["s"] * 2) not in gesehen]
    for b in rest[len(rest) // 3::max(len(rest) // 3, 1)]:
        if len(w2) >= 8:
            break
        w2.append((b["kolk"]["s"], "Kolk Becken %d (Hauptbecken)" % b["nr"]))
        gesehen.add(round(b["kolk"]["s"] * 2))
    wahl = sorted(w2)[:8]
    cols, rows = 2, 4
    pw, ph = 700, 250
    Lw = Leinwand(cols * pw + 40, rows * (ph + 40) + 140)
    Lw.text(30, 14, "Erlenbach p2, Talkaskade: Querschnitte (Blick talwaerts, links = u > 0), Hoehe relativ zum neuen Spiegel", 17)
    Lw.text(30, 40, "Ufer Ist aus querschnitte_p2.json; Bett Ist angenommen (gestrichelt). 1 Kaestchen = 1 m quer / 0,5 m hoch.",
            12, TINTE2)
    umax = 8.0
    zlo, zhi = -1.6, 3.0
    for n, (s, titel) in enumerate(wahl):
        cx = 30 + (n % cols) * (pw + 10)
        cy = 70 + (n // cols) * (ph + 40)
        i = int(np.clip(round((s - S[0]) / 0.5), 0, len(S) - 1))
        j0 = int(np.argmin(np.abs(U - G["UC"][i])))
        w0 = W[i, j0]
        m = np.abs(U) <= umax
        xs = lambda u: cx + 40 + (umax - u) / (2 * umax) * (pw - 60)       # Blick talwaerts: links (u>0) links im Bild
        ys = lambda z: cy + 20 + (zhi - z) / (zhi - zlo) * (ph - 40)
        for g in np.arange(zlo, zhi + 1e-9, 0.5):
            Lw.linie([(cx + 40, ys(g)), (cx + pw - 20, ys(g))], GITTER, 1)
        for u in range(-int(umax), int(umax) + 1):
            Lw.linie([(xs(u), cy + 20), (xs(u), cy + ph - 20)], GITTER, 1)
        for g in (-1, 0, 1, 2, 3):
            Lw.text(cx + 34, ys(g), "%+d" % g if g else "0", 10, TINTE2, "rm")
        zn = X["z_neu"][i] - w0
        zi = X["ist_z"][i] - w0
        uu = U[m]
        # Wasser
        wv = W[i][m] - w0
        poly = []
        for u, a_, b_ in zip(uu, zn[m], wv):
            if a_ < b_:
                poly.append((u, a_, b_))
        if poly:
            for (u, a_, b_) in poly:
                Lw.rechteck(xs(u + 0.125), ys(b_), xs(u - 0.125), ys(a_), (180, 210, 245), None)
        innen_alt = np.abs(uu) <= np.interp(S[i], X["ist"].s, X["ist"].B) / 2
        Lw.linie([(xs(u), ys(z)) for u, z, f in zip(uu, zi[m], innen_alt) if not f and u > 0], GRAU, 1.6)
        Lw.linie([(xs(u), ys(z)) for u, z, f in zip(uu, zi[m], innen_alt) if not f and u < 0], GRAU, 1.6)
        Lw.linie([(xs(u), ys(z)) for u, z, f in zip(uu, zi[m], innen_alt) if f], GRAU, 1.2, strich=2)
        Lw.linie([(xs(u), ys(z)) for u, z in zip(uu, zn[m])], TINTE, 2.0)
        Lw.linie([(xs(u), ys(0)) for u in (uu[0], uu[-1])], BLAU, 1.0, strich=3)
        spa = X["ist"].spiegel_alt(S[i]) - w0
        Lw.linie([(xs(uu[0]), ys(spa)), (xs(uu[-1]), ys(spa))], GRAU, 1.0, strich=2)
        Lw.text(cx + 44, cy + 2, "s %.1f: %s" % (S[i], titel), 12)
        tmax = float((W[i] - X["z_neu"][i])[G["innen"][i]].max()) if G["innen"][i].any() else 0
        Lw.text(cx + pw - 24, cy + 2, "Tiefe max %.2f m" % tmax, 11, TINTE2, "ra")
    y = 70 + rows * (ph + 40)
    x = 40
    for f, t, st in [(TINTE, "Gelaende neu", None), (GRAU, "Ufer Ist", None), (GRAU, "Bett Ist (angenommen)", 2),
                     (GRAU, "Spiegel alt", 2), ((180, 210, 245), "Wasser neu", None)]:
        Lw.linie([(x, y + 8), (x + 26, y + 8)], f, 3 if f == (180, 210, 245) else 2, strich=st)
        Lw.text(x + 32, y + 1, t, 11, TINTE2)
        x += 60 + len(t) * 6.4
    Lw.speichern(pfad)


def alle(X, aus):
    import p2_bettplan as pb
    if "kennzahlen" not in X:
        X["kennzahlen"] = pb.kennzahlen(X)
    ab = X["ab"]
    bild_delta(X, os.path.join(aus, "%s_delta.png" % ab))
    bild_tiefe(X, os.path.join(aus, "%s_tiefe.png" % ab))
    bild_laengs(X, os.path.join(aus, "%s_laengsprofil.png" % ab))
    bild_quer(X, os.path.join(aus, "%s_querschnitte.png" % ab))
