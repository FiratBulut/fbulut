"""vorschau.py - Testbild sehens/<biom>/test_<id>.png fuer Phase 2 (Draufsicht eines gebauten Orts).

vorschau(ctx, pfad, groesse_m=None, breite_px=900)
  Grund: Boden-Farbe (vorherrschende Lage, geplante Bodenlagen daruebergeblendet) x Schummerung des Gelaendes
  NACH dem Stempel, Hoehenlinien; Stempel: rot = angehoben, blau = abgesenkt (Deckkraft ~ |Delta|), Umriss |Delta| > 0,25 m.
  Wasser: Bestand blau, geplante Seen tuerkis mit Umriss, Baeche als Linie, Wasserfall-Kante weiss mit Pfeil.
  Instanzen: Fussabdruck je Detail-Ebene (Farbe), Akteure als gedrehte Grundrisse mit Umriss.
  Effekte: Nebel (Kreis gestrichelt), Licht (Stern), Niagara (Dreieck, hohl = optional), Decal (Rechteck), Klang (K).
  Kameras §8 als Pfeile, Pfad (Bodenband), Freiraeume (rot gestrichelt). Legende: Zahlen je Ebene, Budget, Stempel.
ctx: rezept.OrtKontext nach baue() und eintrag_bauen().
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw

from . import ascii_text
from . import daten as _daten
from . import instanzen as _ins
from . import zeichnen as _z

FARBE_EBENE = {"held": (235, 40, 40), "begleiter": (255, 140, 30), "schutt": (150, 150, 160),
               "kleinzeug": (240, 225, 140), "bewuchs": (60, 200, 70), "kontakt": (150, 190, 60),
               "wasser": (80, 220, 255), "pfad": (255, 255, 255)}
LAGE_FARBE = dict(_z.BODEN_FARBEN)


def _gestrichelt(dr, mx, my, r, farbe, breite=2, n=28):
    for k in range(n):
        if k % 2:
            continue
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        dr.line([(mx + r * math.cos(a0), my + r * math.sin(a0)), (mx + r * math.cos(a1), my + r * math.sin(a1))],
                fill=farbe, width=breite)


def vorschau(ctx, pfad, groesse_m=None, breite_px=900):
    welt = ctx.welt
    st = ctx.stempel
    x0s, y0s, x1s, y1s = st.fe.grenzen_m()
    if groesse_m is None:
        groesse_m = max(x1s - x0s, y1s - y0s, 2.6 * ctx.st["radius_m"], 120.0) + 20.0
        groesse_m = min(groesse_m, 320.0)
    fe = welt.fenster(ctx.mx, ctx.my, groesse_m / 2.0)
    X, Y = fe.gitter_m()
    h = np.asarray(st.hoehe_bei_m(X, Y), np.float64)
    d = np.asarray(_ins_delta(st, X, Y))
    z = welt.zelle_m
    # Grundfarbe aus Boden + geplanten Lagen
    bo = fe.get("boden")
    lut = np.zeros((256, 3))
    lut[:] = (150, 150, 140)
    for k, n in enumerate(_daten.BODEN):
        lut[k] = _z.BODEN_FARBEN.get(n, (150, 150, 140))
    rgb = lut[bo].astype(np.float64)
    if ctx.lagen is not None:
        for n in ctx.lagen.namen():
            a = np.asarray(_lagen_bei(ctx.lagen, X, Y, n)) / 255.0
            rgb = rgb * (1 - 0.8 * a[..., None]) + np.array(LAGE_FARBE.get(n, (200, 200, 200))) * 0.8 * a[..., None]
    sh = _z.schummerung(h, z)
    rgb = rgb * (0.35 + 0.85 * sh[..., None])
    relief = float(h.max() - h.min())
    fein = 1.0 if relief < 40 else (2.0 if relief < 120 else 5.0)
    lf = _z._hoehenlinien(h, fein)
    lg = _z._hoehenlinien(h, fein * 5)
    rgb[lf] *= 0.8
    rgb[lg] *= 0.55
    # Stempel einfaerben
    dm = max(float(np.abs(d).max()), 0.5)
    a = np.clip(np.abs(d) / dm, 0, 1)[..., None] * 0.55
    farbe = np.where(d[..., None] > 0, np.array([230, 60, 40]), np.array([40, 90, 230]))
    rgb = rgb * (1 - a) + farbe * a
    wa = fe.get("wasser") > 0
    rgb[wa] = rgb[wa] * 0.3 + np.array(_z.FARBEN["wasser"]) * 0.7
    me = fe.get("meer")
    rgb[me] = np.array(_z.FARBEN["meer"])
    wg = fe.get("weg") > 0
    rgb[wg] = _z.FARBEN["weg"]
    skala = max(1, int(round(breite_px / max(rgb.shape[1], 1))))
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize(
        (rgb.shape[1] * skala, rgb.shape[0] * skala), Image.BILINEAR)
    W, H = img.size
    dr = ImageDraw.Draw(img, "RGBA")
    px_m = skala / z

    def P(x, y):
        i, j = fe.lokal(x, y)
        return (float(j) + 0.5) * skala, (float(i) + 0.5) * skala

    f_k = _z._font(12)
    # Freiraeume
    for f in ctx.freiraeume:
        mx, my = P(f["mitte_cm"][0] / 100.0, f["mitte_cm"][1] / 100.0)
        if f["form"] == "kreis":
            _gestrichelt(dr, mx, my, f["radius_cm"] / 100.0 * px_m, (255, 0, 200, 230), 2)
        else:
            ga = math.radians(f["richtung_grad"])
            ux, uy = math.sin(ga), -math.cos(ga)
            L, B = f["laenge_cm"] / 200.0, f["breite_cm"] / 200.0
            ecken = [(L * sx * ux - B * sy * uy, L * sx * uy + B * sy * ux) for sx, sy in ((1, 1), (1, -1), (-1, -1), (-1, 1))]
            q = [P(f["mitte_cm"][0] / 100.0 + a, f["mitte_cm"][1] / 100.0 + b) for a, b in ecken]
            dr.line(q + [q[0]], fill=(255, 0, 200, 230), width=2)
    # Pfad
    if ctx.pfad:
        q = [P(p[0], p[1]) for p in ctx.pfad["punkte_m"]]
        dr.line(q, fill=(0, 0, 0, 200), width=max(3, int(ctx.pfad["breite_cm"] / 100.0 * px_m) + 2), joint="curve")
        dr.line(q, fill=(250, 235, 200, 255), width=max(1, int(ctx.pfad["breite_cm"] / 100.0 * px_m)), joint="curve")
    # Wasser (geplant)
    for w in ctx.wasser:
        if w["typ"] == "see":
            q = [P(p[0] / 100.0, p[1] / 100.0) for p in w["umriss_cm"]]
            dr.polygon(q, fill=(40, 200, 210, 150), outline=(220, 255, 255, 255))
        elif w["typ"] == "bach":
            q = [P(p[0] / 100.0, p[1] / 100.0) for p in w["punkte_cm"]]
            br = max(2, int(w["punkte_cm"][0][3] / 100.0 * px_m))
            dr.line(q, fill=(60, 150, 255, 230), width=br, joint="curve")
        elif w["typ"] == "wasserfall":
            q = [P(p[0] / 100.0, p[1] / 100.0) for p in w["kante_cm"]]
            dr.line(q, fill=(255, 255, 255, 255), width=5)
            c = q[len(q) // 2]
            dr.text((c[0] + 6, c[1] - 14), "Fall %.0f m" % w.get("fallhoehe_m", 0), fill=(255, 255, 255),
                    font=f_k, stroke_width=2, stroke_fill=(0, 0, 0))
    # Instanzen (kleine zuerst)
    stuecke = ctx.ebene.vom_ort(ctx.id)
    reihen = ["kleinzeug", "kontakt", "bewuchs", "pfad", "wasser", "schutt", "begleiter", "held"]
    for eb in reihen:
        c = FARBE_EBENE[eb]
        for e in stuecke:
            if e["ebene"] != eb:
                continue
            info = ctx.inv.netz(e["pfad"])
            pts = _ins.gedrehte_box(info, e["q"], e["s"])
            xs = (e["x"] + pts[:, 0]) / 100.0
            ys = (e["y"] + pts[:, 1]) / 100.0
            cx, cy = P(float(xs.mean()), float(ys.mean()))
            if e.get("rolle") == "baum":
                # stehender Baum: Krone als Kreis (halbe Box-Breite), Stamm als Punkt am Pivot
                kr = 0.25 * (xs.max() - xs.min() + ys.max() - ys.min()) * 0.5 * px_m
                dr.ellipse([cx - kr, cy - kr, cx + kr, cy + kr], fill=c + (60,), outline=c + (230,), width=2 if e["akteur"] else 1)
                sx_, sy_ = P(e["x"] / 100.0, e["y"] / 100.0)
                dr.ellipse([sx_ - 3, sy_ - 3, sx_ + 3, sy_ + 3], fill=(60, 30, 10, 255), outline=(0, 0, 0, 255))
                continue
            if e["akteur"]:
                # gedrehter Grundriss: konvexe Huelle der Boxpunkte
                hull = _huelle(np.stack([xs, ys], axis=1))
                q = [P(a, b) for a, b in hull]
                dr.polygon(q, fill=c + (120,), outline=(0, 0, 0, 255))
                dr.line(q + [q[0]], fill=c + (255,), width=2)
            else:
                r = max(0.9, 0.5 * max(xs.max() - xs.min(), ys.max() - ys.min()) * px_m * (0.5 if eb in ("bewuchs",) else 0.8))
                if eb == "kleinzeug":
                    r = max(0.8, min(r, 2.0))
                dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c + (200 if eb != "bewuchs" else 110,),
                           outline=(0, 0, 0, 160) if r > 2.5 else None)
    # Effekte
    for e in ctx.effekte:
        x, y = e["pos_cm"][0] / 100.0, e["pos_cm"][1] / 100.0
        mx, my = P(x, y)
        t = e["typ"]
        if t == "lokaler_nebel":
            _gestrichelt(dr, mx, my, e["radius_cm"] / 100.0 * px_m, (235, 235, 245, 230), 2)
        elif t in ("punktlicht", "spotlicht"):
            for k in range(8):
                a = math.pi * k / 4
                dr.line([(mx, my), (mx + 9 * math.cos(a), my + 9 * math.sin(a))], fill=(255, 240, 80, 255), width=2)
        elif t == "niagara":
            tri = [(mx, my - 9), (mx - 8, my + 6), (mx + 8, my + 6)]
            if e.get("optional"):
                dr.polygon(tri, outline=(220, 120, 255, 255))
            else:
                dr.polygon(tri, fill=(220, 120, 255, 255), outline=(0, 0, 0, 255))
        elif t == "decal":
            g = e["groesse_cm"]
            ww, hh = g[1] / 200.0 * px_m, g[2] / 200.0 * px_m
            dr.rectangle([mx - ww, my - hh, mx + ww, my + hh], outline=(170, 110, 60, 255), width=2)
    for k in ctx.klaenge:
        mx, my = P(k["pos_cm"][0] / 100.0, k["pos_cm"][1] / 100.0)
        dr.text((mx - 4, my - 7), "K", fill=(255, 255, 255), font=f_k, stroke_width=2, stroke_fill=(60, 0, 90))
    # Kameras
    for kam in ctx.st.get("kameras") or []:
        art = str(kam[6]).rsplit("_", 1)[-1]
        c = _z.FARBEN["kamera"].get(art, (255, 255, 255))
        p0, p1 = P(kam[1] / 100.0, kam[2] / 100.0), P(kam[3] / 100.0, kam[4] / 100.0)
        if not (0 <= p0[0] < W and 0 <= p0[1] < H):
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            for tt in np.linspace(0, 1, 300):
                qx, qy = p0[0] + dx * tt, p0[1] + dy * tt
                if 4 <= qx < W - 4 and 4 <= qy < H - 4:
                    p0 = (qx, qy)
                    break
            dr.text((p0[0] + 4, p0[1] + 4), art, fill=c + (255,), font=f_k, stroke_width=2, stroke_fill=(0, 0, 0))
        _z._pfeil(dr, p0, p1, (0, 0, 0, 255), breite=5, spitze=12)
        _z._pfeil(dr, p0, p1, c + (255,), breite=3, spitze=10)
    # Massstab + Nord
    sm = 20.0 if groesse_m < 200 else 50.0
    L = sm * px_m
    dr.rectangle([8, H - 34, 20 + L + 40, H - 6], fill=(255, 255, 255, 200))
    dr.rectangle([14, H - 16, 14 + L, H - 10], fill=(0, 0, 0, 255))
    dr.text((14, H - 32), "%d m" % sm, fill=(0, 0, 0), font=f_k)
    dr.polygon([(W - 24, 10), (W - 32, 32), (W - 16, 32)], fill=(255, 255, 255, 230), outline=(0, 0, 0, 255))
    # Legende
    LB = 300
    out = Image.new("RGB", (W + LB, max(H, 640)), (22, 22, 26))
    out.paste(img, (0, 0))
    d2 = ImageDraw.Draw(out)
    ft = _z._font(15)
    y = 8
    e = ctx.eintrag or {}
    for zeile in (ctx.id, "%s - %s" % (ascii_text(ctx.st["name"]), ctx.st["art"])):
        d2.text((W + 10, y), ascii_text(zeile)[:38], fill=(255, 255, 255), font=ft)
        y += 20
    zeilen = ["Feld %s  X %.0f  Y %.0f m" % (_daten.feld_von_m(ctx.mx, ctx.my), ctx.mx, ctx.my),
              "Ausschnitt %.0f x %.0f m" % (groesse_m, groesse_m),
              "Stempel max %.1f m (rot hoch, blau tief)" % st.max_aenderung_m]
    if ctx.lagen is not None:
        zeilen.append("Lagen: " + ", ".join(ctx.lagen.namen())[:40])
    for zl in zeilen:
        d2.text((W + 10, y), ascii_text(zl), fill=(200, 200, 200), font=f_k)
        y += 16
    y += 6
    de = e.get("detail_ebenen") or {}
    for eb in ("held", "begleiter", "schutt", "kleinzeug", "bewuchs", "kontakt", "wasser", "pfad"):
        n = de.get(eb, {}).get("anzahl", 0)
        if not n:
            continue
        d2.ellipse([W + 12, y + 3, W + 22, y + 13], fill=FARBE_EBENE[eb], outline=(0, 0, 0))
        top = list(de[eb]["netze"].items())[:1]
        d2.text((W + 30, y), ascii_text("%-9s %5d  %s" % (eb, n, top[0][0][:16] if top else "")), fill=(230, 230, 230), font=f_k)
        y += 17
    y += 6
    b = e.get("budget") or {}
    for k in ("instanzen", "kollision", "akteure", "lichter", "niagara", "nebel", "decals"):
        if k in b:
            d2.text((W + 12, y), "%-10s %6d" % (k, b[k]), fill=(200, 220, 255), font=f_k)
            y += 15
    y += 6
    leg = [("see/bach", (40, 200, 210)), ("Wasserfall", (255, 255, 255)), ("Pfad", (250, 235, 200)),
           ("Nebel / Licht", (235, 235, 245)), ("Niagara (hohl=optional)", (220, 120, 255)),
           ("Decal", (170, 110, 60)), ("Freiraum (Bestand weg)", (255, 0, 200))]
    for t, c in leg:
        d2.rectangle([W + 12, y + 3, W + 22, y + 13], fill=c)
        d2.text((W + 30, y), t, fill=(220, 220, 220), font=f_k)
        y += 15
    for art in ("anmarsch", "held", "nah", "fern"):
        _z._pfeil(d2, (W + 10, y + 8), (W + 26, y + 8), _z.FARBEN["kamera"][art], breite=3, spitze=6)
        d2.text((W + 32, y), "Kamera _" + art, fill=(220, 220, 220), font=f_k)
        y += 15
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    out.save(pfad, optimize=True)
    return pfad


def _ins_delta(st, X, Y):
    from .stempel import _bilinear_fenster
    return _bilinear_fenster(st.delta, st.fe, st.welt, X, Y, 0.0)


def _lagen_bei(lg, X, Y, name):
    from .stempel import _bilinear_fenster
    return _bilinear_fenster(lg.ziel[name], lg.fe, lg.welt, X, Y, 0.0)


def _huelle(P):
    """Konvexe Huelle (Monotone Chain) von Punkten (N, 2)."""
    P = sorted(set(map(tuple, np.round(P, 3))))
    if len(P) < 3:
        return P

    def kreuz(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    unten, oben = [], []
    for p in P:
        while len(unten) >= 2 and kreuz(unten[-2], unten[-1], p) <= 0:
            unten.pop()
        unten.append(p)
    for p in reversed(P):
        while len(oben) >= 2 and kreuz(oben[-2], oben[-1], p) <= 0:
            oben.pop()
        oben.append(p)
    return unten[:-1] + oben[:-1]
