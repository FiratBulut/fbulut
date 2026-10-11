"""verdeckung.py - Sicht/Verdeckung eines geplanten Orts MIT Stempel und geplanten Stuecken (Auftrag 13, Phase 2).

Fundstuecke, die erst durch Stempel (Kessel, Wall, Duene), Gehoelz (Saum, Rahmen) oder Felsen verdeckt sind, muss der
Planer bauen. Dieses Modul prueft das nach dem Bauen eines Orts mit sicht.py (Gelaende + 4-m-Baumzellen):

  wp = sicht.Wegpunkte(welt, 20)                      # einmal je Planerlauf
  r = verdeckung.pruefe_ort(ctx, wp)                  # ctx = rezept.OrtKontext nach baue()
  r -> {"verdeckt": bool, "proben": [[n_sichtbar, max_anteil, n_wegpunkte], ...] (Kern, Ost, West, Sued, Nord),
        "heute": [...] (ohne Plan), "ziel_hoehe_m", "probe_r_m", "text"}

Modell (wie Phase 1, standorte.json -> sicht.mit_pfaden):
- Gelaende = Bestand + Stempel-Delta (ctx.stempel.delta im Fenster).
- Felsen/Steine/Staemme (Rolle fels, stein, stamm, wurzel) mit Oberkante >= fels_min_m ueber dem Boden heben das
  Hindernis-Gelaende auf ihre Oberkante (Kreis mit 70 % der kurzen Fuss-Halbachse) - sie sperren sofort.
- Baeume und Straeucher (Rolle baum, pflanze) mit Hoehe >= gehoelz_min_m werden 4-m-Baumzellen (Anzahl 1, Hoehe =
  Oberkante - Boden); sicht.py sperrt Kronen erst ab 3 Proben unter der Krone (dichter Saum noetig).
- Proben: Kern + 4 Punkte im Abstand probe_r_m (Standard Ortsradius / 3), Ziel ziel_hoehe_m (Standard
  standorte.json ziel_hoehe_m), alle Wegpunkte (Wege + Pfade) bis r_max_m. verdeckt = keine Probe mit Anteil > 0,15.

Nur Pruefung, schreibt nichts. Kopiert die Hoehe der Welt einmal je Aufruf (~70 MB bei 2 m).
"""

import copy

import numpy as np

from . import daten as _daten
from . import sicht as _sicht

FELS_ROLLEN = ("fels", "stein", "stamm", "wurzel")
GEHOELZ_ROLLEN = ("baum", "pflanze")


def welt_mit_plan(welt, stempel=None, stuecke=None, fels_min_m=1.0, gehoelz_min_m=2.0):
    """Flache Kopie der Welt mit gestempelter Hoehe, Felsen als Hindernis-Gelaende und Gehoelz als 4-m-Baumzellen.
    stuecke: Liste dict mit x_m, y_m, boden_z_m, oberkante_z_m, fuss_a_m, fuss_b_m, rolle."""
    w2 = copy.copy(welt)
    h = np.array(welt.hoehe, dtype=np.float32, copy=True)
    if stempel is not None and getattr(stempel, "delta", None) is not None:
        sl = stempel.fe.sl
        h[sl] = (stempel.h0 + stempel.delta).astype(np.float32)
    b4 = bh4 = None
    for s in stuecke or []:
        rolle = s.get("rolle")
        hoch = float(s.get("oberkante_z_m", 0.0)) - float(s.get("boden_z_m", 0.0))
        x, y = float(s["x_m"]), float(s["y_m"])
        if rolle in FELS_ROLLEN and hoch >= fels_min_m:
            r = max(0.7 * min(float(s.get("fuss_a_m", 1.0)), float(s.get("fuss_b_m", 1.0))), 0.6 * welt.zelle_m)
            fe = welt.fenster(x, y, r + welt.zelle_m)
            X, Y = fe.gitter_m()
            m = np.hypot(X - x, Y - y) <= r
            sub = h[fe.sl]
            sub[m] = np.maximum(sub[m], float(s["oberkante_z_m"]))
        elif rolle in GEHOELZ_ROLLEN and hoch >= gehoelz_min_m:
            if b4 is None:
                b4 = np.array(welt.baeume4, copy=True)
                bh4 = np.array(welt.baumhoehe4, copy=True)
            i4, j4 = _daten.m_zu_pixel(x, y, 4.0)
            i4 = int(np.clip(np.rint(i4), 0, b4.shape[0] - 1))
            j4 = int(np.clip(np.rint(j4), 0, b4.shape[1] - 1))
            b4[i4, j4] = max(int(b4[i4, j4]), 1)
            bh4[i4, j4] = max(float(bh4[i4, j4]), hoch)
    w2.hoehe = h
    if b4 is not None:
        w2.baeume4, w2.baumhoehe4 = b4, bh4
        w2._baumhoehe_nativ = None
        w2._baeume_nativ = None
    w2._meer = welt._meer
    return w2


def stuecke_aus_ctx(ctx):
    """Alle gesetzten Stuecke eines OrtKontexts als Liste fuer welt_mit_plan."""
    out = []
    for name, liste in ctx.gruppen.items():
        for s in liste:
            e = s.get("stueck") or {}
            if "x_m" not in s or "oberkante_z_m" not in s:
                continue
            out.append({"x_m": s.get("mx_m", s["x_m"]), "y_m": s.get("my_m", s["y_m"]), "boden_z_m": s["boden_z_m"],
                        "oberkante_z_m": s["oberkante_z_m"], "fuss_a_m": s.get("fuss_a_m", 1.0),
                        "fuss_b_m": s.get("fuss_b_m", 1.0), "rolle": e.get("rolle")})
    return out


def proben(x, y, r):
    return [(x, y), (x + r, y), (x - r, y), (x, y + r), (x, y - r)]


def pruefe(welt, wp, x, y, ziel_hoehe_m, probe_r_m, r_max_m=400.0, max_anteil=0.15):
    """Kern + 4 Proben -> Liste [n_sichtbar, max_anteil, n_wegpunkte] und verdeckt (bool)."""
    out = []
    for px, py in proben(x, y, probe_r_m):
        v = _sicht.verdeckt_vom_weg(welt, wp, px, py, ziel_hoehe_m=ziel_hoehe_m, r_max_m=r_max_m, max_anteil=max_anteil)
        out.append([int(v["n_sichtbar"]), round(float(v["max_anteil"]), 2), int(v["n_wegpunkte"])])
    return out, all(p[0] == 0 for p in out)


def pruefe_ort(ctx, wp, ziel_hoehe_m=None, probe_r_m=None, kern_m=None, r_max_m=400.0, mit_heute=True,
               fels_min_m=1.0, gehoelz_min_m=2.0):
    """Verdeckung eines gebauten Orts (ctx nach baue()) mit Stempel + geplanten Stuecken; mit_heute: zum Vergleich
    auch ohne Plan. kern_m: [x, y] statt der Ortsmitte (z. B. Fallstufe)."""
    st = ctx.st
    H = float(ziel_hoehe_m if ziel_hoehe_m is not None else st.get("ziel_hoehe_m", 1.5))
    r = float(probe_r_m if probe_r_m is not None else st.get("radius_m", 30.0) / 3.0)
    x, y = (float(kern_m[0]), float(kern_m[1])) if kern_m else (ctx.mx, ctx.my)
    w2 = welt_mit_plan(ctx.welt, ctx.stempel, stuecke_aus_ctx(ctx), fels_min_m, gehoelz_min_m)
    plan, verdeckt = pruefe(w2, wp, x, y, H, r, r_max_m)
    res = {"verdeckt": verdeckt, "proben": plan, "ziel_hoehe_m": H, "probe_r_m": round(r, 1),
           "kern_m": [round(x, 1), round(y, 1)]}
    if mit_heute:
        heute, v0 = pruefe(ctx.welt, wp, x, y, H, r, r_max_m)
        res["heute"] = heute
        res["heute_verdeckt"] = v0
    namen = ("Kern", "Ost", "West", "Sued", "Nord")
    res["text"] = "Verdeckung mit Plan (Ziel %.1f m, Proben %.0f m): %s; %s" % (
        H, r, "VERDECKT" if verdeckt else "teilweise sichtbar",
        ", ".join("%s %d/%d (%.2f)" % (n, p[0], p[2], p[1]) for n, p in zip(namen, plan)))
    if mit_heute:
        res["text"] += " | heute: " + ", ".join("%s %d" % (n, p[0]) for n, p in zip(namen, res["heute"]))
    return res
