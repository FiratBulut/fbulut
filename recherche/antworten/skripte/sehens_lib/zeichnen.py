"""zeichnen.py - Draufsicht-PNG je Ort (Phase 1, antworten/sehens/<biom>/<id>.png) und Biom-Uebersicht.

draufsicht(welt, x_m, y_m, pfad, groesse_m=500, skala=2, elemente=None, kameras=None, titel="", gel=None)
  Grund: Bodenlage-Farben x Schummerung (Licht NW), Hoehenlinien (fein/grob, automatisch), Suesswasser, Meer,
  Wege, Orte, Baeume (4 m), Biomgrenze, Massstab, Nordpfeil, Legende rechts.
  elemente: Liste dict, je Element eins von
     {"typ": "punkt",   "pos_m": [x, y],             "farbe": "#d33", "name": "Quelltopf", "groesse": 6}
     {"typ": "kreis",   "pos_m": [x, y], "radius_m": 45, "farbe": ..., "name": ..., "fuellen": False}
     {"typ": "linie",   "punkte_m": [[x, y], ...],   "farbe": ..., "breite": 3, "name": "Pfad"}
     {"typ": "polygon", "punkte_m": [[x, y], ...],   "farbe": ..., "name": "Becken", "fuellen": True}
     {"typ": "text",    "pos_m": [x, y], "text": "Kante"}
     (statt *_m geht auch *_cm)
  kameras: Liste §8 [Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch] in cm -> Pfeile Kamera -> Ziel.
uebersicht(welt, pfad, biom=None, punkte=None, gel=None, verkleinerung=4) - Biom-Karte mit nummerierten Punkten.
"""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import ascii_text, log
from . import daten as _daten

BODEN_FARBEN = {
    "Wiese": (118, 150, 72), "Gras": (100, 140, 64), "Trockengras": (160, 156, 92), "Laub": (150, 112, 62),
    "Nadeln": (110, 88, 60), "Moos": (70, 112, 56), "Heide": (128, 92, 118), "Kraut": (92, 132, 70),
    "Erde": (124, 98, 72), "Lehm": (160, 124, 82), "Schlamm": (92, 80, 62), "Sand": (214, 196, 150),
    "Kies": (170, 164, 150), "Geroell": (146, 142, 136), "Fels": (128, 126, 124), "Felsplatte": (162, 160, 156),
    "Sandstein": (196, 140, 96), "Schnee": (240, 242, 246), "Eis": (196, 226, 240), "Lavafels": (52, 48, 48),
    "Lavasand": (84, 76, 74), "Algen": (64, 116, 104)}
FARBEN = {"weg": (226, 196, 120), "wasser": (58, 120, 200), "meer": (30, 58, 102), "ort": (190, 60, 60),
          "baum": (28, 70, 34), "biomgrenze": (230, 40, 200), "linie_fein": (40, 34, 30),
          "kamera": {"anmarsch": (255, 140, 0), "held": (255, 40, 40), "nah": (250, 230, 40),
                     "fern": (40, 220, 255)}}
_FONT_PFADE = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf",
               "/Library/Fonts/Arial.ttf"]


def _font(groesse):
    for p in _FONT_PFADE:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, groesse)
            except Exception:
                pass
    try:
        return ImageFont.load_default(groesse)
    except TypeError:
        return ImageFont.load_default()


def _farbe(f, standard=(255, 60, 60)):
    if f is None:
        return standard
    if isinstance(f, str):
        f = f.lstrip("#")
        if len(f) == 3:
            f = "".join(c * 2 for c in f)
        return tuple(int(f[k:k + 2], 16) for k in (0, 2, 4))
    return tuple(int(v) for v in f[:3])


def schummerung(h, z, azimut=315.0, hoehe_grad=45.0, ueberhoehung=1.5):
    """Hillshade 0..1 (Licht aus azimut, 0 = Nord, im Uhrzeigersinn)."""
    gy, gx = np.gradient(h.astype(np.float64) * ueberhoehung, float(z))
    a = np.radians(azimut)
    e = np.radians(hoehe_grad)
    lx, ly = np.sin(a), -np.cos(a)  # +x = Ost, +y = Sued
    L = np.array([np.cos(e) * lx, np.cos(e) * ly, np.sin(e)])
    n = np.stack([-gx, -gy, np.ones_like(gx)])
    n /= np.linalg.norm(n, axis=0)
    return np.clip(L[0] * n[0] + L[1] * n[1] + L[2] * n[2], 0, 1)


def _grenzen(a):
    g = np.zeros(a.shape, bool)
    g[:, 1:] |= a[:, 1:] != a[:, :-1]
    g[1:, :] |= a[1:, :] != a[:-1, :]
    return g


def _hoehenlinien(h, intervall):
    k = np.floor(h / intervall)
    return _grenzen(k)


def _blockmax(a, s):
    """Maximum je s x s Block (Form wie a[::s, ::s]) - duenne Linien (Wege, Baeche) bleiben sichtbar."""
    if s <= 1:
        return a
    ny, nx = a.shape
    py, px = (-ny) % s, (-nx) % s
    b = np.pad(a, ((0, py), (0, px)), mode="edge")
    return b.reshape(b.shape[0] // s, s, b.shape[1] // s, s).max(axis=(1, 3))


def _grundbild(welt, fe, skala, schritt=1):
    """Grundbild eines Fensters; schritt > 1 duennt die Raster aus (Uebersichten)."""
    q = (slice(None, None, schritt), slice(None, None, schritt))
    zelle = welt.zelle_m * schritt
    h = fe.get("hoehe")[q].astype(np.float64)
    bo = fe.get("boden")[q]
    lut = np.zeros((256, 3), np.float64)
    lut[:] = (150, 150, 140)
    for k, n in enumerate(_daten.BODEN):
        lut[k] = BODEN_FARBEN.get(n, (150, 150, 140))
    rgb = lut[bo]
    sh = schummerung(h, zelle)
    rgb = rgb * (0.35 + 0.85 * sh[..., None])
    relief = float(h.max() - h.min())
    fein, grob = (2.0, 10.0) if relief < 120 else ((5.0, 25.0) if relief < 400 else (10.0, 50.0))
    lf = _hoehenlinien(h, fein)
    lg = _hoehenlinien(h, grob)
    rgb[lf] = rgb[lf] * 0.82
    rgb[lg] = rgb[lg] * 0.55
    wa = _blockmax(fe.get("wasser"), schritt) > 0
    me = fe.get("meer")[q]
    for m, c, a in ((wa, FARBEN["wasser"], 0.8), (me, FARBEN["meer"], 0.9)):
        rgb[m] = rgb[m] * (1 - a) + np.array(c) * a
    og = _blockmax(fe.get("ort"), schritt) > 0
    rgb[og] = rgb[og] * 0.5 + np.array(FARBEN["ort"]) * 0.5
    wg = _blockmax(fe.get("weg"), schritt) > 0
    rgb[wg] = FARBEN["weg"]
    bg = _grenzen(fe.get("biom")[q])
    rgb[bg] = FARBEN["biomgrenze"]
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    if skala != 1:
        img = img.resize((img.width * skala, img.height * skala), Image.NEAREST)
    return img, (fein, grob)


class _Abb:
    """Weltkoordinaten (m) -> Bildpixel."""

    def __init__(self, welt, fe, skala):
        self.welt, self.fe, self.s = welt, fe, skala

    def __call__(self, x_m, y_m):
        i, j = self.fe.lokal(x_m, y_m)
        return (float(j) + 0.5) * self.s, (float(i) + 0.5) * self.s


def _pos(e, schluessel):
    if schluessel + "_m" in e:
        return e[schluessel + "_m"]
    if schluessel + "_cm" in e:
        v = e[schluessel + "_cm"]
        if schluessel == "punkte":
            return [[p[0] / 100.0, p[1] / 100.0] for p in v]
        return [v[0] / 100.0, v[1] / 100.0]
    return None


def _pfeil(dr, p0, p1, farbe, breite=3, spitze=12):
    dr.line([p0, p1], fill=farbe, width=breite)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = max(np.hypot(dx, dy), 1e-6)
    ux, uy = dx / L, dy / L
    a = (p1[0] - ux * spitze - uy * spitze * 0.5, p1[1] - uy * spitze + ux * spitze * 0.5)
    b = (p1[0] - ux * spitze + uy * spitze * 0.5, p1[1] - uy * spitze - ux * spitze * 0.5)
    dr.polygon([p1, a, b], fill=farbe)


def draufsicht(welt, x_m, y_m, pfad, groesse_m=500.0, skala=2, elemente=None, kameras=None, titel="",
               gel=None, baeume=True, untertitel=None):
    """Schreibt eine Draufsicht (PNG) um (x_m, y_m). Rueckgabe: Pfad."""
    fe = welt.fenster(x_m, y_m, groesse_m / 2.0)
    img, (fein, grob) = _grundbild(welt, fe, skala)
    W, H = img.size
    abb = _Abb(welt, fe, skala)
    dr = ImageDraw.Draw(img, "RGBA")
    # Baeume (4 m)
    if baeume:
        x0, y0, x1, y1 = fe.grenzen_m()
        i40, j40 = _daten.m_zu_pixel(x0, y0, 4.0)
        i41, j41 = _daten.m_zu_pixel(x1, y1, 4.0)
        i40, j40 = max(0, int(np.floor(i40))), max(0, int(np.floor(j40)))
        i41 = min(welt.baeume4.shape[0] - 1, int(np.ceil(i41)))
        j41 = min(welt.baeume4.shape[1] - 1, int(np.ceil(j41)))
        sub = welt.baeume4[i40:i41 + 1, j40:j41 + 1]
        bh = welt.baumhoehe4[i40:i41 + 1, j40:j41 + 1]
        ii, jj = np.nonzero(sub > 0)
        bx, by = _daten.pixel_zu_m(ii + i40, jj + j40, 4.0)
        for xx, yy, hh in zip(bx, by, bh[ii, jj]):
            px, py = abb(xx, yy)
            r = max(1.5, min(4.0, 1.0 + hh / 10.0)) * skala / 2.0
            dr.ellipse([px - r, py - r, px + r, py + r], fill=FARBEN["baum"] + (200,))
    leg = []
    f_klein = _font(11 + 2 * (skala > 1))
    # Elemente
    for e in elemente or []:
        typ = e.get("typ", "punkt")
        c = _farbe(e.get("farbe"))
        if typ in ("punkt", "kreis", "text"):
            p = _pos(e, "pos")
            if p is None:
                continue
            px, py = abb(p[0], p[1])
            if typ == "punkt":
                r = e.get("groesse", 5) * skala / 2.0 + 2
                dr.ellipse([px - r, py - r, px + r, py + r], fill=c + (255,), outline=(0, 0, 0, 255))
            elif typ == "kreis":
                r = e.get("radius_m", 10) / welt.zelle_m * skala
                if e.get("fuellen"):
                    dr.ellipse([px - r, py - r, px + r, py + r], fill=c + (70,), outline=c + (255,), width=2)
                else:
                    dr.ellipse([px - r, py - r, px + r, py + r], outline=c + (255,), width=max(2, skala))
            else:
                dr.text((px, py), ascii_text(e.get("text", "")), fill=c + (255,), font=f_klein,
                        stroke_width=2, stroke_fill=(0, 0, 0))
        elif typ in ("linie", "polygon"):
            pts = _pos(e, "punkte")
            if not pts or len(pts) < 2:
                continue
            q = [abb(p[0], p[1]) for p in pts]
            if typ == "linie":
                dr.line(q, fill=c + (255,), width=int(e.get("breite", 3)) * max(1, skala // 2), joint="curve")
            else:
                dr.polygon(q, fill=(c + (90,)) if e.get("fuellen", True) else None, outline=c + (255,))
        if e.get("name") and e.get("text") is None:
            leg.append((typ, c, e["name"]))
    # Kameras
    kam_leg = set()
    for k in kameras or []:
        name = str(k[6])
        art = name.rsplit("_", 1)[-1]
        c = FARBEN["kamera"].get(art, (255, 255, 255))
        kx, ky, zx, zy = k[1] / 100.0, k[2] / 100.0, k[3] / 100.0, k[4] / 100.0
        p0, p1 = abb(kx, ky), abb(zx, zy)
        innen = 0 <= p0[0] < W and 0 <= p0[1] < H
        if not innen:
            # Pfeil vom Bildrand in Blickrichtung, Abstand beschriften
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            L = max(np.hypot(dx, dy), 1e-6)
            t = 0.0
            for tt in np.linspace(0, 1, 400):
                qx, qy = p0[0] + dx * tt, p0[1] + dy * tt
                if 4 <= qx < W - 4 and 4 <= qy < H - 4:
                    t = tt
                    break
            p0 = (p0[0] + dx * t, p0[1] + dy * t)
            d_m = np.hypot(kx - zx, ky - zy)
            dr.text((p0[0] + 4, p0[1] + 4), "%s %.0f m" % (art, d_m), fill=c + (255,), font=f_klein,
                    stroke_width=2, stroke_fill=(0, 0, 0))
        _pfeil(dr, p0, p1, (0, 0, 0, 255), breite=5 + skala, spitze=12 + 2 * skala)
        _pfeil(dr, p0, p1, c + (255,), breite=2 + skala, spitze=10 + 2 * skala)
        if innen:
            r = 4 + skala
            dr.ellipse([p0[0] - r, p0[1] - r, p0[0] + r, p0[1] + r], fill=c + (255,), outline=(0, 0, 0, 255))
        kam_leg.add(art)
    # Massstab + Nordpfeil
    f = _font(13 + 2 * (skala > 1))
    sm = 100.0 if groesse_m >= 300 else 50.0
    L = sm / welt.zelle_m * skala
    x0, y0 = 14, H - 22
    dr.rectangle([x0 - 6, y0 - 22, x0 + L + 50, y0 + 12], fill=(255, 255, 255, 190))
    dr.rectangle([x0, y0, x0 + L / 2, y0 + 6], fill=(0, 0, 0, 255))
    dr.rectangle([x0 + L / 2, y0, x0 + L, y0 + 6], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    dr.text((x0, y0 - 19), "%d m" % sm, fill=(0, 0, 0), font=f)
    nx0, ny0 = W - 30, 16
    dr.polygon([(nx0, ny0), (nx0 - 9, ny0 + 24), (nx0 + 9, ny0 + 24)], fill=(255, 255, 255, 230),
               outline=(0, 0, 0, 255))
    dr.text((nx0 - 5, ny0 + 25), "N", fill=(255, 255, 255), font=f, stroke_width=2, stroke_fill=(0, 0, 0))
    # Legende rechts
    LB = 250
    out = Image.new("RGB", (W + LB, max(H, 520)), (24, 24, 28))
    out.paste(img, (0, 0))
    d2 = ImageDraw.Draw(out)
    ft = _font(15)
    y = 10
    for zeile in [ascii_text(titel or "Draufsicht")] + ([ascii_text(untertitel)] if untertitel else []):
        d2.text((W + 10, y), zeile[:34], fill=(255, 255, 255), font=ft)
        y += 20
    fe_txt = "X %.0f  Y %.0f m  Feld %s" % (x_m, y_m, _daten.feld_von_m(x_m, y_m))
    d2.text((W + 10, y), fe_txt, fill=(200, 200, 200), font=f_klein)
    y += 16
    d2.text((W + 10, y), "Boden %.0f m, %.0f x %.0f m" % (welt.hoehe_bei_m(x_m, y_m), groesse_m, groesse_m),
            fill=(200, 200, 200), font=f_klein)
    y += 24
    eintraege = [("feld", FARBEN["weg"], "Weg"), ("feld", FARBEN["wasser"], "Suesswasser"),
                 ("feld", FARBEN["meer"], "Meer"), ("feld", FARBEN["ort"], "Ort/Bauwerk"),
                 ("punkt", FARBEN["baum"], "Baum (4 m)"), ("feld", FARBEN["biomgrenze"], "Biomgrenze"),
                 ("feld", (70, 60, 50), "Hoehenlinien %g / %g m" % (fein, grob))]
    eintraege += leg
    eintraege += [("pfeil", FARBEN["kamera"][a], "Kamera _" + a) for a in ("anmarsch", "held", "nah", "fern")
                  if a in kam_leg]
    for typ, c, name in eintraege:
        if typ in ("punkt",):
            d2.ellipse([W + 12, y + 3, W + 22, y + 13], fill=c, outline=(0, 0, 0))
        elif typ == "kreis":
            d2.ellipse([W + 11, y + 2, W + 23, y + 14], outline=c, width=2)
        elif typ == "linie":
            d2.line([(W + 10, y + 8), (W + 26, y + 8)], fill=c, width=3)
        elif typ == "pfeil":
            _pfeil(d2, (W + 10, y + 8), (W + 28, y + 8), c, breite=3, spitze=7)
        else:
            d2.rectangle([W + 10, y + 2, W + 24, y + 14], fill=c)
        d2.text((W + 34, y), ascii_text(name)[:28], fill=(230, 230, 230), font=f_klein)
        y += 18
    d2.text((W + 10, out.height - 34), "Boden: Farbe der vorherrschenden", fill=(150, 150, 150), font=f_klein)
    d2.text((W + 10, out.height - 18), "Bodenlage x Schummerung (NW)", fill=(150, 150, 150), font=f_klein)
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    out.save(pfad, optimize=True)
    return pfad


def uebersicht(welt, pfad, biom=None, punkte=None, verkleinerung=4, rand_m=300.0):
    """Biom-Uebersicht (Schummerung + Boden, Wege, Wasser) mit nummerierten Punkten [{x_m, y_m, (name)}]."""
    if biom:
        ii, jj = np.nonzero(welt.biom_maske(biom))
        x0, y0 = welt.ij_zu_m(ii.min(), jj.min())
        x1, y1 = welt.ij_zu_m(ii.max(), jj.max())
        x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
        fe = welt.fenster_box(x0 - rand_m, y0 - rand_m, x1 + rand_m, y1 + rand_m)
    else:
        fe = welt.fenster_box(_daten.X_MIN_M, _daten.Y_MIN_M, _daten.X_MAX_M, _daten.Y_MAX_M)
    v = int(verkleinerung)
    img, _ = _grundbild(welt, fe, 1, schritt=v)
    if biom:
        m = (fe.get("biom") == _daten.biom_code(biom))[::v, ::v][:img.height, :img.width]
        a = np.asarray(img).astype(np.float64)
        a[~m] *= 0.55
        img = Image.fromarray(a.astype(np.uint8))
    dr = ImageDraw.Draw(img)
    f = _font(12)
    for n, p in enumerate(punkte or [], 1):
        i, j = fe.lokal(p["x_m"], p["y_m"])
        px, py = (j + 0.5) / v, (i + 0.5) / v
        dr.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 40, 40), outline=(0, 0, 0))
        dr.text((px + 5, py - 6), str(p.get("name", n)), fill=(255, 255, 255), font=f, stroke_width=2,
                stroke_fill=(0, 0, 0))
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    img.save(pfad, optimize=True)
    return pfad
