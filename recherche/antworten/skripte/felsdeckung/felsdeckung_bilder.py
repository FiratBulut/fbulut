"""felsdeckung_bilder.py - Bilder zum Pilotplan Auftrag 21 (nur Pillow/NumPy, deterministisch).

  zonen_<Feld>.png          Zonenkarte (Wand, Schrofen, Halde, Hangfuss, Hangwald, Tal, Sperre) + Pruefkameras
  draufsicht_<Feld>.png     Fussabdruecke je Thema auf Schummerung (1 px = 0,5 m)
  delta_karte_<Feld>.png    Variante B: Schuettkegel-Delta (m) auf Schummerung, Wasser + Uferband A20
  querschnitte_<Feld>.png   3 Schnitte entlang der Kegel-Falllinien: Gelaende vorher/nachher, Zonenband, Stuecke
  skizze_wand_halde_tal.png Schema Wand -> Schrofen -> Halde -> Hangfuss -> Bach mit Zahlen der Regeln
Aufruf ueber felsdeckung_plan.py --bild.
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import felsdeckung_plan as FP

FLAECHE = (252, 252, 251)
TINTE = (11, 11, 11)
TINTE2 = (82, 81, 78)
GEDAEMPFT = (137, 135, 129)
GITTER = (225, 224, 217)
# feste kategoriale Reihenfolge (Referenzpalette): Slot 1..7
SLOT = [(42, 120, 214), (235, 104, 52), (27, 175, 122), (237, 161, 0), (232, 123, 164), (0, 131, 0), (98, 80, 214)]
THEMA_FARBE = {"klippenband": SLOT[0], "halde": SLOT[1], "platten": SLOT[2], "baumgruppen": SLOT[5]}
ZONE_FARBE = {"wand": SLOT[6], "schrofen": SLOT[0], "halde": SLOT[1], "fuss": SLOT[2], "hangwald": SLOT[5],
              "tal": (205, 226, 251), "sperre": (195, 194, 183)}
BLAU = [(205, 226, 251), (158, 197, 244), (109, 167, 236), (57, 135, 229), (37, 106, 191), (24, 79, 149), (13, 54, 107)]


def schrift(gr):
    try:
        return ImageFont.load_default(gr)
    except TypeError:
        return ImageFont.load_default()


def schummerung(K, zr):
    """Schummerung (0..1) des Fensters auf zr-m-Raster."""
    x0, y0, x1, y1 = K.fenster_m
    xs = np.arange(x0 + zr / 2, x1, zr)
    ys = np.arange(y0 + zr / 2, y1, zr)
    X, Y = np.meshgrid(xs, ys)
    gx = K.bilinear(K.gx, X, Y)
    gy = K.bilinear(K.gy, X, Y)
    hs = (1.0 + (-gx * -0.6 + -gy * -0.6) + 0.0) / np.sqrt(1 + gx * gx + gy * gy)
    hs = np.clip(0.55 + 0.45 * (hs - 0.5), 0.25, 1.0)
    return X, Y, hs


def massstab(d, x, y, px_je_m, f, laenge_m=100):
    L = laenge_m * px_je_m
    d.rectangle([x, y, x + L, y + 5], fill=TINTE)
    d.rectangle([x + L / 2, y, x + L, y + 5], fill=FLAECHE, outline=TINTE)
    d.text((x, y + 8), "0", fill=TINTE, font=f)
    d.text((x + L - 24, y + 8), "%d m" % laenge_m, fill=TINTE, font=f)


def nordpfeil(d, x, y, f):
    d.polygon([(x, y), (x - 7, y + 18), (x + 7, y + 18)], fill=TINTE)
    d.text((x - 4, y + 20), "N", fill=TINTE, font=f)


def legende(d, x, y, eintraege, f, kasten=14):
    for i, (farbe, text) in enumerate(eintraege):
        yy = y + i * (kasten + 6)
        d.rounded_rectangle([x, yy, x + kasten, yy + kasten], radius=3, fill=farbe)
        d.text((x + kasten + 6, yy - 1), text, fill=TINTE, font=f)


def kameras(R):
    k = R["pilot"].get("kameras", [])
    return k


def zonen_bild(pl, aus):
    K, R = pl.K, pl.R
    zr = 1.0
    X, Y, hs = schummerung(K, zr)
    zone = K.naechst(K.zone, X, Y)
    rgb = np.zeros(X.shape + (3,))
    for name, code in FP.ZONEN.items():
        rgb[zone == code] = ZONE_FARBE[name]
    rgb = rgb * (0.55 + 0.45 * hs[..., None])
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    H, W = X.shape
    rand_r = 400
    im = Image.new("RGB", (W + rand_r, H + 80), FLAECHE)
    im.paste(Image.fromarray(rgb), (0, 40))
    d = ImageDraw.Draw(im)
    f, fg = schrift(14), schrift(18)
    d.text((8, 10), "B5-Ost: Zonen im Pilotfenster (480 x 500 m, 1 px = 1 m)", fill=TINTE, font=fg)
    fl = {}
    for name, code in FP.ZONEN.items():
        fl[name] = float(((K.zone == code) & K.innen).sum() * K.z * K.z) / 1e4
    eint = [(ZONE_FARBE[n], "%s  %.1f ha" % (t, fl[n])) for n, t in
            (("wand", "Wand >= 50 Grad"), ("schrofen", "Schrofen 38-50 Grad"), ("halde", "Halde 26-40 Grad unter Wand"),
             ("fuss", "Hangfuss 12-26 Grad"), ("hangwald", "Hangwald 26-38 Grad"), ("tal", "Tal < 12 Grad"),
             ("sperre", "Sperre (Uferband 0-10 m A20, Weg, Ort)"))]
    legende(d, W + 14, 50, eint, f)
    x0, y0, _, _ = K.fenster_m
    for k in kameras(R):
        cx, cy = (k["x_m"] - x0) / zr, (k["y_m"] - y0) / zr + 40
        if 0 <= cx < W and 40 <= cy < H + 40:
            a = math.radians(k["blick_kompass_grad"])
            d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=TINTE)
            d.line([cx, cy, cx + 40 * math.sin(a), cy - 40 * math.cos(a)], fill=TINTE, width=3)
            d.text((cx + 8, cy + 6), k["name"], fill=TINTE, font=f)
    d.text((W + 14, 50 + 7 * 20 + 10), "Kameras: siehe Antwort (g);", fill=TINTE2, font=f)
    d.text((W + 14, 50 + 8 * 20 + 10), "K1 steht im Tal (C5), ausserhalb.", fill=TINTE2, font=f)
    massstab(d, 20, H + 46, 1.0 / zr, f)
    nordpfeil(d, W - 20, 50, f)
    im.save(os.path.join(aus, "zonen_%s.png" % K.feld), optimize=False)


def draufsicht(pl, aus):
    K = pl.K
    zr = 0.5
    X, Y, hs = schummerung(K, zr)
    g = (245 * hs).astype(np.uint8)
    H, W = X.shape
    rand_r = 330
    im = Image.new("RGB", (W + rand_r, H + 90), FLAECHE)
    im.paste(Image.fromarray(np.stack([g, g, g], -1)), (0, 50))
    d = ImageDraw.Draw(im)
    f, fg = schrift(16), schrift(22)
    x0, y0, _, _ = K.fenster_m
    reihen = ["halde", "platten", "klippenband", "baumgruppen"]
    for th in reihen:
        for e in pl.stuecke:
            if e["thema"] != th:
                continue
            mx, my, a, b, w = e["fuss"]
            farbe = THEMA_FARBE[th]
            if e["rolle"].startswith("baum") or e["rolle"] == "latsche":
                r = 1.5 if e["rolle"] == "latsche" else max(1.5, 0.22 * e["d_m"])
                cx, cy = (mx - x0) / zr, (my - y0) / zr + 50
                d.ellipse([cx - r / zr, cy - r / zr, cx + r / zr, cy + r / zr], outline=farbe, width=2)
                continue
            if e["rolle"] == "fuge":
                cx, cy = (mx - x0) / zr, (my - y0) / zr + 50
                d.point((cx, cy), fill=SLOT[5])
                continue
            pts = []
            for t in range(16):
                ph = 2 * math.pi * t / 16
                lx, ly = 0.85 * a * math.cos(ph), 0.85 * b * math.sin(ph)
                px = mx + lx * math.cos(w) - ly * math.sin(w)
                py = my + lx * math.sin(w) + ly * math.cos(w)
                pts.append(((px - x0) / zr, (py - y0) / zr + 50))
            d.polygon(pts, fill=farbe, outline=FLAECHE)
    d.text((8, 12), "B5-Ost: Fussabdruecke je Thema (Variante %s, 1 px = 0,5 m)" % pl.variante, fill=TINTE, font=fg)
    n = {}
    for e in pl.stuecke:
        n[e["thema"]] = n.get(e["thema"], 0) + 1
    legende(d, W + 16, 60, [(THEMA_FARBE[t], "%s  %d Stuecke" % (t, n.get(t, 0))) for t in
                           ("klippenband", "halde", "platten", "baumgruppen")], f, 16)
    d.text((W + 16, 60 + 4 * 24 + 8), "Baeume/Latschen: Ringe", fill=TINTE2, font=f)
    d.text((W + 16, 60 + 5 * 24 + 8), "Fugenbewuchs: Punkte", fill=TINTE2, font=f)
    massstab(d, 20, H + 56, 1.0 / zr, f)
    nordpfeil(d, W - 24, 60, f)
    im.save(os.path.join(aus, "draufsicht_%s.png" % K.feld), optimize=False)


def delta_karte(pl, welt, R, aus, delta, kegel):
    K0 = FP.Kontext(welt, R)
    zr = 1.0
    X, Y, hs = schummerung(K0, zr)
    dd = K0.bilinear(delta, X, Y)
    g = 235 * hs
    rgb = np.stack([g, g, g], -1)
    stufen = [0.05, 0.5, 1.0, 2.0, 3.0, 4.0, 4.75]
    for k, s in enumerate(stufen):
        rgb[dd >= s] = np.array(BLAU[k]) * (0.75 + 0.25 * hs[dd >= s, None])
    dw = K0.bilinear(K0.d_wasser, X, Y)
    rgb[dw < 1.0] = (24, 79, 149)
    rgb[(dw >= 9.5) & (dw < 10.5)] = (208, 59, 59)
    rgb[(dw >= 11.6) & (dw < 12.4)] = (250, 178, 25)
    H, W = X.shape
    im = Image.new("RGB", (W + 360, H + 90), FLAECHE)
    im.paste(Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), (0, 50))
    d = ImageDraw.Draw(im)
    f, fg = schrift(14), schrift(18)
    x0, y0, _, _ = K0.fenster_m
    d.text((8, 12), "Variante B: Schuettkegel (nur Auftrag, A15-Delta in m)", fill=TINTE, font=fg)
    for i, c in enumerate(kegel):
        cx, cy = (c["x_m"] - x0) / zr, (c["y_m"] - y0) / zr + 50
        a = math.radians(c["fallrichtung_kompass"])
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=TINTE)
        d.line([cx, cy, cx + 60 * math.sin(a), cy - 60 * math.cos(a)], fill=TINTE, width=2)
        d.text((cx + 8, cy - 18), "K%d  %.1f m / %.0f m3" % (i + 1, c["max_auftrag_m"], c["volumen_m3"]), fill=TINTE, font=f)
    eint = [(BLAU[k], ">= %.2g m" % s) for k, s in enumerate(stufen)]
    legende(d, W + 14, 60, eint, f)
    yy = 60 + len(eint) * 20 + 10
    legende(d, W + 14, yy, [((24, 79, 149), "Wasser (Bestand)"), ((208, 59, 59), "10 m: Grenze Uferband A20"),
                            ((250, 178, 25), "12 m: Kegel-Schutzabstand")], f)
    d.text((W + 14, yy + 70), "Linie = Fallrichtung = Schnitt", fill=TINTE2, font=f)
    massstab(d, 20, H + 56, 1.0 / zr, f)
    nordpfeil(d, W - 20, 60, f)
    im.save(os.path.join(aus, "delta_karte_%s.png" % K0.feld), optimize=False)


def querschnitte(pl, welt, R, aus, delta, kegel):
    K0 = FP.Kontext(welt, R)
    K = pl.K
    pw, ph, rl, ob = 1300, 280, 70, 40
    n = max(1, len(kegel))
    im = Image.new("RGB", (pw, n * (ph + 50) + 60), FLAECHE)
    d = ImageDraw.Draw(im)
    f, fg = schrift(14), schrift(18)
    d.text((8, 10), "Querschnitte entlang der Kegel-Falllinien (Ueberhoehung 1:1, Stuecke +-4 m vom Schnitt)",
           fill=TINTE, font=fg)
    for i, c in enumerate(kegel):
        a = math.radians(c["fallrichtung_kompass"])
        ux, uy = math.sin(a), -math.cos(a)
        s = np.arange(-25.0, 95.0, 0.5)
        xs, ys = c["x_m"] + s * ux, c["y_m"] + s * uy
        h0 = K0.bilinear(K0.h, xs, ys)
        h1 = h0 + K0.bilinear(delta, xs, ys)
        zmin, zmax = float(h0.min()) - 5, float(max(h0.max(), h1.max())) + 10
        top = 50 + i * (ph + 50)
        breite = pw - rl - 20
        mz = min(breite / (s[-1] - s[0]), (ph - ob) / (zmax - zmin))

        def P(sv, zv):
            return rl + (sv - s[0]) * mz, top + ob + (zmax - zv) * mz
        for gz in range(int(zmin // 20 * 20), int(zmax) + 1, 20):
            y_ = P(s[0], gz)[1]
            if top + ob <= y_ <= top + ph:
                d.line([rl, y_, pw - 20, y_], fill=GITTER)
                d.text((8, y_ - 8), "%d m" % gz, fill=GEDAEMPFT, font=f)
        zone = K0.naechst(K0.zone, xs, ys)
        inv = {v: k for k, v in FP.ZONEN.items()}
        for k in range(len(s) - 1):
            x_, _ = P(s[k], 0)
            x2, _ = P(s[k + 1], 0)
            d.rectangle([x_, top + ph + 4, x2, top + ph + 14], fill=ZONE_FARBE[inv[int(zone[k])]])
        for sv, za, zb_ in zip(s, h0, h1):
            if zb_ - za > 0.02:
                d.line([P(sv, za), P(sv, zb_)], fill=BLAU[2], width=2)
        d.line([P(sv, zv) for sv, zv in zip(s, h0)], fill=GEDAEMPFT, width=2)
        d.line([P(sv, zv) for sv, zv in zip(s, h1)], fill=SLOT[0], width=2)
        for e in pl.stuecke:
            mx, my, aa, bb, w = e["fuss"]
            vx, vy = mx - c["x_m"], my - c["y_m"]
            sv = vx * ux + vy * uy
            qv = -vx * uy + vy * ux
            if abs(qv) > 4.0 or not (s[0] <= sv <= s[-1]):
                continue
            zb = float(K.boden(mx, my))
            farbe = THEMA_FARBE[e["thema"]]
            px, py = P(sv, zb)
            hh = max(2.0, e["hoehe_m"] * mz * (0.5 if not e["rolle"].startswith("baum") else 1.0))
            ww = max(2.0, min(e["d_m"], 12.0) * mz * 0.5)
            if e["rolle"].startswith("baum") or e["rolle"] == "latsche":
                d.line([px, py, px, py - hh], fill=farbe, width=2)
            else:
                d.rectangle([px - ww, py - hh, px + ww, py], outline=farbe, width=2)
        d.text((rl, top + 4), "K%d  Fallrichtung %.0f Grad, max %.1f m, %.0f m3  (grau vorher, blau Variante B, Flaeche = Auftrag)"
               % (i + 1, c["fallrichtung_kompass"], c["max_auftrag_m"], c["volumen_m3"]), fill=TINTE, font=f)
        d.text((rl, top + ph + 16), "Zonenband (Farben wie zonen_B5.png); 0 m = Kegelspitze am Wandfuss", fill=TINTE2, font=f)
    im.save(os.path.join(aus, "querschnitte_%s.png" % K.feld), optimize=False)


def skizze(R, aus):
    W, H = 1500, 760
    im = Image.new("RGB", (W, H), FLAECHE)
    d = ImageDraw.Draw(im)
    f, fs, fg = schrift(15), schrift(13), schrift(20)
    d.text((14, 10), "Skizze Wand -> Schrofen -> Halde -> Hangfuss -> Bach (Regeln Auftrag 21, bergwald; schematisch, nicht massstaeblich)",
           fill=TINTE, font=fg)
    # Profil
    prof = [(60, 120), (260, 150), (300, 470), (420, 560), (640, 640), (900, 690), (1120, 712), (1180, 718), (1450, 724)]
    poly = prof + [(1450, H), (60, H)]
    d.polygon(poly, fill=(225, 224, 217))
    d.line(prof, fill=GEDAEMPFT, width=3)
    # Wand: Reihen
    for k in range(6):
        y = 175 + k * 50
        x = 262 + (y - 150) * (40 / 320.0)
        d.rectangle([x - 34 - (k % 2) * 12, y, x + 6, y + 44], fill=SLOT[6], outline=FLAECHE, width=2)
    d.polygon([(205, 95), (240, 95), (250, 160), (200, 160)], fill=SLOT[6])
    d.text((150, 70), "Turmklotz (1 je Front, <= 25 m ueber Grat)", fill=TINTE, font=fs)
    d.text((14, 330), "WAND >= 50 Grad", fill=TINTE, font=f)
    d.text((14, 350), "Reihen dz = 0,75 x Modulhoehe", fill=TINTE2, font=fs)
    d.text((14, 367), "35 % Ueberlappung, Kipp 4-10 Grad", fill=TINTE2, font=fs)
    d.text((14, 384), "Ziel >= 85 % mit FS-Schalen", fill=TINTE2, font=fs)
    # Schrofen-Baender
    for k in range(4):
        x = 310 + k * 30
        y = 470 + k * 22
        d.rectangle([x, y - 22, x + 26, y], fill=SLOT[0], outline=FLAECHE, width=2)
        d.ellipse([x + 26, y - 8, x + 36, y + 2], fill=SLOT[5])
    d.text((300, 400), "SCHROFEN 38-50 Grad", fill=TINTE, font=f)  # Texte rechts der Wand
    S_ = R["schrofen"]
    d.text((300, 420), ("Baender dz %g m (+-%g), Hoehe %g-%g m" % (S_["band_dz_m"], S_["band_dz_streuung_m"], S_["band_hoehe_m"][0],
                                                               S_["band_hoehe_m"][1])).replace(".", ","), fill=TINTE2, font=fs)
    d.text((300, 437), "%d %% durchgehend, Latschen auf Tritten" % (100 * S_["band_kontinuitaet"]), fill=TINTE2, font=fs)
    # Halde
    for k in range(18):
        x = 440 + k * 11
        y = 563 + (x - 420) * (77 / 220.0)
        d.rectangle([x, y - 4, x + 9, y], fill=SLOT[1])
    for k, (x, r) in enumerate([(470, 4), (520, 6), (565, 8), (600, 10), (630, 13)]):
        y = 563 + (x - 420) * (77 / 220.0)
        d.ellipse([x - r, y - r * 1.2, x + r, y + r * 0.3], fill=(196, 84, 40), outline=FLAECHE)
    d.text((440, 470), "HALDE 26-40 Grad (unter Wand, <= 60 m)", fill=TINTE, font=f)
    H_ = R["halde"]
    d.text((440, 490), "Teppich-Scans %d -> %d %% Deckung" % (100 * H_["deckung_oben"], 100 * H_["deckung_unten"]), fill=TINTE2, font=fs)
    d.text((440, 507), "Bloecke 2,7 -> 2,1 je 100 m2, gross unten", fill=TINTE2, font=fs)
    d.text((440, 524), "Schutt < 0,5 m nur Lage + Grastyp", fill=TINTE2, font=fs)
    # Hangfuss Platten + Baeume
    for k, x in enumerate([700, 760, 840, 930]):
        y = 640 + (x - 640) * (50 / 260.0)
        d.polygon([(x - 22, y + 2), (x + 22, y - 3), (x + 26, y + 3), (x - 20, y + 6)], fill=SLOT[2])
        d.ellipse([x + 24, y - 6, x + 30, y], fill=SLOT[5])
    for x, hgt in ((780, 70), (800, 95), (818, 55), (990, 85), (1010, 60)):
        y = 640 + (x - 640) * (50 / 260.0)
        d.polygon([(x, y - hgt), (x - 12, y - 8), (x + 12, y - 8)], fill=SLOT[5])
        d.line([x, y - 8, x, y], fill=(90, 60, 30), width=3)
        d.ellipse([x + 6, y - 7, x + 16, y + 1], fill=SLOT[1])
    P_ = R["platten"]
    d.text((690, 500), "HANGFUSS 12-26 Grad", fill=TINTE, font=f)
    d.text((690, 520), "Platten %g-%g m, %d-%d %% eingegraben" % (P_["laenge_m"][0], P_["laenge_m"][1],
                                                               100 * P_["eingraben"][0], 100 * P_["eingraben"][1]), fill=TINTE2, font=fs)
    d.text((690, 537), ("Deckung nah %d %%, fern %d %%; Fugen %.1f je m Rand" % (100 * P_["deckung_nah"], 100 * P_["deckung_fern"],
                                                                          P_["fugen_je_m_rand"])).replace(".", ","), fill=TINTE2, font=fs)
    d.text((690, 554), "Baumgruppen 3-8 (4,5-15 m), Block je Baum <= 3 m", fill=TINTE2, font=fs)
    # Bach + A20
    d.rectangle([1120, 712, 1180, 724], fill=(57, 135, 229))
    d.line([1080, 640, 1080, 745], fill=(208, 59, 59), width=2)
    d.line([1220, 640, 1220, 745], fill=(208, 59, 59), width=2)
    d.text((1060, 650), "Uferband 0-10 m = Auftrag 20", fill=(208, 59, 59), font=fs)
    d.text((1060, 666), "(hier setzt dieser Plan nichts)", fill=(208, 59, 59), font=fs)
    d.text((1240, 620), "10-15 m: Uebergang", fill=TINTE2, font=fs)
    d.text((1240, 636), "Teppich x 0,5, keine Baender/Baeume", fill=TINTE2, font=fs)
    legende(d, 1180, 80, [(SLOT[6], "Wandreihen / Turm (klippenband)"), (SLOT[0], "Schrofen-Baender (klippenband)"),
                          (SLOT[1], "Halde: Teppich + Bloecke"), (SLOT[2], "Platten + Fugen"), (SLOT[5], "Baeume, Latschen, Gras")], fs)
    im.save(os.path.join(aus, "skizze_wand_halde_tal.png"), optimize=False)


def alle(pl, welt, R, aus, delta, kegel):
    o = os.path.join(aus, "bilder")
    os.makedirs(o, exist_ok=True)
    zonen_bild(pl, o)
    draufsicht(pl, o)
    delta_karte(pl, welt, R, o, delta, kegel)
    querschnitte(pl, welt, R, o, delta, kegel)
    skizze(R, o)
