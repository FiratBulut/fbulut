"""sehens_pruefen.py - Pruefer gegen vorlagen/SEHENS_FORMAT.md und die Standortregeln aus Auftrag 13.

Aufruf (aus dem Repo, mit python -I):
  python -I antworten/skripte/sehens_lib/sehens_pruefen.py                      # alle antworten/sehens/*/standorte.json
  python -I antworten/skripte/sehens_lib/sehens_pruefen.py --datei X/orte.json  # Phase 2 (orte.json)
  Optionen: --sehens <Ordner> (Standard antworten/sehens), --daten2m / --daten1m (Gelaende-Regeln pruefen),
            --ohne-daten (nur Format), --cache <Ordner>
Exit-Code 1 bei FEHLER.

Geprueft:
  Phase 1 standorte.json: Pflichtfelder, ID-Schema <biom>_<nn>_<name>, art, mitte/felder, Kameras §8
    (>= 3: _anmarsch/_held/_nah, Leuchtfeuer + _fern; 8 Felder; Abstaende _nah 5-15 m, _fern 300-800 m),
    mit Daten: Weg 80-300 m, nicht im Ort, >= 150 m vom Stadtrand, im Biom (kleine Biome <= 150 m ausserhalb),
    nicht im Meer, Mitte-z ~ Boden; je Biom 8 Orte, ~3 Leuchtfeuer.
  Global ueber alle Biome: Mindestabstand 350 m (beide in kleinen Biomen: 200 m), doppelte IDs.
  Phase 2 orte.json: Pflichtfelder §2, Gelaende/Lagen §3 (Fenster, max_aenderung, Dateigroessen, Rand = 0),
    Wasser §5 (Umriss gegen Uhrzeigersinn = Flaeche > 0 in X/Y wie wasser_welt.json, Farben, Bachgefaelle),
    Effekte §6, Materialwuensche §7 (<= 6 je Biom), Kameras §8, Budget §9.

API: pruefe_standorte(d, welt=None, gel=None), pruefe_orte(d, basis=None), pruefe_global(liste),
     pruefe_alle(sehens_ordner, welt=None, gel=None), melde(befunde, titel)
Befund = (stufe, ort_id, text) mit stufe in FEHLER / WARNUNG / HINWEIS.
"""

import math
import os
import re
import sys

if __name__ == "__main__" and __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "sehens_lib"
    import sehens_lib  # noqa: F401

from . import log, ascii_text  # noqa: E402
from . import daten as _daten  # noqa: E402

FEHLER, WARNUNG, HINWEIS = "FEHLER", "WARNUNG", "HINWEIS"
ARTEN = ("leuchtfeuer", "fundstueck")
FARBEN = ("klar", "tuerkis", "tiefblau", "smaragd", "moorbraun", "schwarz_spiegel", "gletschermilch",
          "thermal", "rostrot", "salzweiss")
MASTER = ("M_EL_Fels_MS", "M_EL_Fels_Auflage", "M_EL_Fels_Sand", "M_EL_Klippe_RVT", "M_EL_Pflanze",
          "M_EL_Eis4", "M_EL_Wasserfall2", "M_MS_Decal", "M_MS_Base")
BUDGET = {"instanzen": 15000, "kollision": 1500, "akteure": 80, "lichter": 4, "niagara": 3, "decals": 12}
FELD_RE = re.compile(r"^[A-J][1-7]$")


def _zahl(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _pkt(v, n):
    return isinstance(v, (list, tuple)) and len(v) >= n and all(_zahl(x) for x in v[:n])


# ============================================================================================
# Kameras (§8)
# ============================================================================================
def pruefe_kameras(oid, art, kams, mitte_cm, welt=None, gel=None):
    b = []
    if not isinstance(kams, list) or len(kams) < 3:
        b.append((FEHLER, oid, "kameras: mindestens 3 noetig (_anmarsch, _held, _nah)"))
        return b
    namen = {}
    for k in kams:
        if not isinstance(k, list) or len(k) != 8:
            b.append((FEHLER, oid, "Kamera braucht 8 Felder [Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch]: %r" % (k,)))
            continue
        feld, kx, ky, zx, zy, zz, name, hoch = k
        if not (isinstance(feld, str) and FELD_RE.match(feld)):
            b.append((FEHLER, oid, "Kamera %s: Feld %r ungueltig" % (name, feld)))
        if not all(_zahl(v) for v in (kx, ky, zx, zy, zz, hoch)):
            b.append((FEHLER, oid, "Kamera %s: Koordinaten/Hoch muessen Zahlen sein (cm)" % name))
            continue
        if not isinstance(name, str) or not name.startswith(oid + "_"):
            b.append((FEHLER, oid, "Kamera-Name %r muss mit '%s_' beginnen" % (name, oid)))
            continue
        art_k = name[len(oid) + 1:]
        namen[art_k] = k
        if hoch <= 0 or hoch > 5000:
            b.append((WARNUNG, oid, "Kamera %s: Hoch %s cm ungewoehnlich (Augenhoehe 170)" % (name, hoch)))
        if mitte_cm and _pkt(mitte_cm, 2):
            dz = math.hypot(zx - mitte_cm[0], zy - mitte_cm[1]) / 100.0
            if dz > 120:
                b.append((WARNUNG, oid, "Kamera %s: Ziel %.0f m von der Ortsmitte entfernt" % (name, dz)))
        d = math.hypot(kx - zx, ky - zy) / 100.0
        if art_k == "nah" and not (4.0 <= d <= 16.0):
            b.append((WARNUNG, oid, "Kamera _nah: Abstand %.1f m (Soll 5-15 m)" % d))
        if art_k == "fern" and not (280.0 <= d <= 820.0):
            b.append((WARNUNG, oid, "Kamera _fern: Abstand %.0f m (Soll 300-800 m)" % d))
        if welt is not None:
            if not welt.im_raster_m(kx / 100.0, ky / 100.0):
                b.append((FEHLER, oid, "Kamera %s ausserhalb der Welt" % name))
                continue
            i, j = welt.cm_zu_ij(kx, ky)
            if welt.meer[i, j] or welt.wasser[i, j] > 0:
                b.append((WARNUNG, oid, "Kamera %s steht im Wasser/Meer" % name))
            boden = welt.hoehe_bei_cm(kx, ky)
            hk = max(boden + hoch, zz + 300)
            if art_k in ("anmarsch", "fern") and hk - (boden + hoch) > 500:
                b.append((HINWEIS, oid, "Kamera %s: ZZ + 300 hebt die Kamera %.0f m ueber Augenhoehe "
                                        "(Ziel tiefer legen)" % (name, (hk - boden - hoch) / 100.0)))
            if art_k == "anmarsch" and gel is not None and gel.abstand_weg[i, j] > 30:
                b.append((HINWEIS, oid, "Kamera _anmarsch %.0f m vom Weg (ok, wenn auf dem Zugangspfad)"
                          % gel.abstand_weg[i, j]))
    for pflicht in ("anmarsch", "held", "nah"):
        if pflicht not in namen:
            b.append((FEHLER, oid, "Kamera _%s fehlt" % pflicht))
    if art == "leuchtfeuer" and "fern" not in namen:
        b.append((FEHLER, oid, "Leuchtfeuer braucht Kamera _fern (300-800 m)"))
    return b


# ============================================================================================
# Phase 1
# ============================================================================================
def pruefe_standort(o, biom, welt=None, gel=None):
    b = []
    oid = o.get("id") if isinstance(o, dict) else None
    if not isinstance(o, dict) or not isinstance(oid, str):
        return [(FEHLER, "?", "Ort ohne id")]
    for f in ("id", "name", "art", "mitte_cm", "radius_m", "felder", "kameras"):
        if f not in o:
            b.append((FEHLER, oid, "Pflichtfeld fehlt: %s" % f))
    if not re.match(r"^%s_\d{2}_[a-z0-9_]+$" % re.escape(biom), oid):
        b.append((FEHLER, oid, "id muss '%s_<nn>_<name>' sein (klein, ASCII)" % biom))
    art = o.get("art")
    if art not in ARTEN:
        b.append((FEHLER, oid, "art %r (leuchtfeuer/fundstueck)" % art))
    m = o.get("mitte_cm")
    if not _pkt(m, 3):
        b.append((FEHLER, oid, "mitte_cm muss [x, y, z] in cm sein"))
        m = None
    r = o.get("radius_m")
    if not _zahl(r) or r <= 0:
        b.append((FEHLER, oid, "radius_m fehlt/ungueltig"))
    elif r > 300:
        b.append((WARNUNG, oid, "radius_m %.0f > 300 (Gelaendefenster max. 400-600 m)" % r))
    if m:
        x, y = m[0] / 100.0, m[1] / 100.0
        f = _daten.feld_von_m(x, y)
        if f is None:
            b.append((FEHLER, oid, "mitte ausserhalb der Welt"))
        elif f not in (o.get("felder") or []):
            b.append((FEHLER, oid, "felder %r enthaelt nicht das Feld der Mitte %s" % (o.get("felder"), f)))
        if welt is not None and f is not None:
            i, j = welt.m_zu_ij(x, y)
            bz = welt.hoehe_bei_m(x, y)
            if abs(bz - m[2] / 100.0) > 3.0:
                b.append((WARNUNG, oid, "mitte z %.1f m weicht %.1f m vom Boden ab" % (m[2] / 100.0, m[2] / 100.0 - bz)))
            if welt.meer[i, j]:
                b.append((FEHLER, oid, "Mitte liegt im Meer"))
            if welt.ort[i, j] > 0:
                b.append((FEHLER, oid, "Mitte liegt in einem Ort (ort_2m)"))
            if gel is not None:
                dw = float(gel.abstand_weg[i, j])
                if dw < 60 or dw > 400:
                    b.append((FEHLER, oid, "Abstand zum Weg %.0f m (Soll 80-300 m)" % dw))
                elif dw < 80 or dw > 300:
                    b.append((WARNUNG, oid, "Abstand zum Weg %.0f m (Soll 80-300 m)" % dw))
                if gel.abstand_ort[i, j] < 20:
                    b.append((WARNUNG, oid, "nur %.0f m bis zu einem Ort/Bauwerk" % gel.abstand_ort[i, j]))
                sd, st = gel.stadt_abstand_punkt(x, y)
                if sd < 150:
                    b.append((FEHLER, oid, "nur %.0f m vom Rand der geplanten Stadt %s (Soll >= 150 m)"
                              % (sd, (st or {}).get("id"))))
                if biom in _daten.BIOME:
                    ba = float(gel.biom_abstand(biom)[i, j])
                    if _daten.ist_kleines_biom(biom):
                        if ba < -150:
                            b.append((FEHLER, oid, "%.0f m ausserhalb des Bioms %s (kleine Biome <= 150 m)"
                                      % (-ba, biom)))
                    elif ba < 0:
                        b.append((FEHLER, oid, "Mitte liegt %.0f m ausserhalb des Bioms %s" % (-ba, biom)))
                    elif ba < 20:
                        b.append((HINWEIS, oid, "nur %.0f m innerhalb der Biomgrenze (Rechteck)" % ba))
    b += pruefe_kameras(oid, art, o.get("kameras"), m, welt, gel)
    for k in ("pfad_cm",):
        if k in o and o[k] and not all(_pkt(p, 2) for p in o[k]):
            b.append((FEHLER, oid, "%s: Liste von [x, y(, z)] in cm" % k))
    return b


def pruefe_standorte(d, welt=None, gel=None, biom=None, global_pruefen=True):
    """Prueft eine standorte.json (dict). global_pruefen: Abstaende/IDs innerhalb der Datei."""
    b = []
    biom = biom or d.get("biom")
    if biom not in _daten.BIOME:
        b.append((FEHLER, "-", "biom %r unbekannt" % biom))
    if "stand" not in d:
        b.append((WARNUNG, "-", "Feld 'stand' fehlt"))
    orte = d.get("orte")
    if not isinstance(orte, list):
        return b + [(FEHLER, "-", "'orte' muss eine Liste sein")]
    for o in orte:
        b += pruefe_standort(o, biom or "?", welt, gel)
    if len(orte) != 8:
        b.append((WARNUNG, biom, "%d Orte (Soll 8 je Biom)" % len(orte)))
    nl = sum(1 for o in orte if isinstance(o, dict) and o.get("art") == "leuchtfeuer")
    if orte and not (2 <= nl <= 4):
        b.append((HINWEIS, biom, "%d Leuchtfeuer / %d Fundstuecke (Richtwert 3 / 5)" % (nl, len(orte) - nl)))
    if global_pruefen:
        b += pruefe_global([(biom, o, "") for o in orte if isinstance(o, dict)])
    return b


def pruefe_global(liste):
    """Abstaende und IDs ueber alle Biome. liste: [(biom, ort, pfad), ...]."""
    from .format import mindestabstand_m
    b = []
    ids = {}
    pts = []
    for biom, o, _ in liste:
        oid = o.get("id", "?")
        if oid in ids:
            b.append((FEHLER, oid, "doppelte id (auch in %s)" % ids[oid]))
        ids[oid] = biom
        m = o.get("mitte_cm")
        if _pkt(m, 2):
            pts.append((biom, oid, m[0] / 100.0, m[1] / 100.0))
    for a in range(len(pts)):
        for c in range(a + 1, len(pts)):
            ba, ia, xa, ya = pts[a]
            bc, ic, xc, yc = pts[c]
            d = math.hypot(xa - xc, ya - yc)
            mn = mindestabstand_m(ba, bc)
            if d < mn:
                b.append((FEHLER, ia, "nur %.0f m zu %s (%s), Soll >= %.0f m" % (d, ic, bc, mn)))
    return b


def pruefe_alle(sehens_ordner, welt=None, gel=None):
    """Alle <sehens_ordner>/*/standorte.json einzeln + global. Rueckgabe Befunde."""
    from .format import alle_standorte, lade_standorte
    import glob
    b = []
    for p in sorted(glob.glob(os.path.join(sehens_ordner, "*", "standorte.json"))):
        try:
            d = lade_standorte(p)
        except Exception as ex:
            b.append((FEHLER, p, "JSON nicht lesbar: %s" % ex))
            continue
        biom = d.get("biom") or os.path.basename(os.path.dirname(p))
        if biom != os.path.basename(os.path.dirname(p)):
            b.append((WARNUNG, biom, "biom %r passt nicht zum Ordner %s" % (biom, p)))
        b += pruefe_standorte(d, welt, gel, biom, global_pruefen=False)
    b += pruefe_global(alle_standorte(sehens_ordner))
    return b


# ============================================================================================
# Phase 2
# ============================================================================================
def _flaeche(u):
    n = len(u)
    return 0.5 * sum(u[k][0] * u[(k + 1) % n][1] - u[(k + 1) % n][0] * u[k][1] for k in range(n))


def _pruefe_fenster(oid, name, g, art, basis, suffixe=None, typ="f32"):
    b = []
    fij = g.get("fenster_ij")
    if not (isinstance(fij, list) and len(fij) == 4 and all(isinstance(v, int) for v in fij)):
        return [(FEHLER, oid, "%s.fenster_ij muss [i0, j0, hoehe, breite] (int, 1 m) sein" % name)]
    i0, j0, hh, ww = fij
    if hh <= 0 or ww <= 0 or i0 < 0 or j0 < 0 or i0 + hh > _daten.NY_1M or j0 + ww > _daten.NX_1M:
        b.append((FEHLER, oid, "%s.fenster_ij ausserhalb der Welt: %r" % (name, fij)))
    grenze = 600 if art == "leuchtfeuer" else 400
    if max(hh, ww) > grenze:
        b.append((FEHLER, oid, "%s-Fenster %dx%d m > %d m" % (name, hh, ww, grenze)))
    elif max(hh, ww) > 400:
        b.append((WARNUNG, oid, "%s-Fenster %dx%d m > 400 m (nur grosse Leuchtfeuer, begruenden)" % (name, hh, ww)))
    if basis:
        import numpy as np
        dateien = [g.get("datei")] if typ == "f32" else [(g.get("datei_praefix") or "") + s + ".r8"
                                                        for s in (suffixe or [])]
        for df in dateien:
            if not df:
                continue
            pf = os.path.join(basis, df)
            if not os.path.exists(pf):
                b.append((WARNUNG, oid, "Datei fehlt: %s" % df))
                continue
            soll = hh * ww * (4 if typ == "f32" else 1)
            ist = os.path.getsize(pf)
            if ist != soll:
                b.append((FEHLER, oid, "%s: %d Bytes, Soll %d (Fenster %dx%d)" % (df, ist, soll, hh, ww)))
                continue
            if typ == "f32":
                a = np.fromfile(pf, dtype="<f4").reshape(hh, ww)
                rand = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
                if np.abs(rand).max() > 0.01:
                    b.append((FEHLER, oid, "%s: Rand des Fensters nicht 0 (max %.2f m)" % (df, np.abs(rand).max())))
                mx = float(np.abs(a).max())
                if mx > 40:
                    b.append((WARNUNG, oid, "%s: |Delta| bis %.1f m > 40 m (begruenden)" % (df, mx)))
                if abs(mx - float(g.get("max_aenderung_m", mx))) > 0.5:
                    b.append((HINWEIS, oid, "%s: max_aenderung_m %.1f, Datei %.1f" % (df, g.get("max_aenderung_m"), mx)))
    return b


def pruefe_ort(o, biom, basis=None):
    b = []
    oid = o.get("id", "?")
    for f in ("id", "name", "art", "kurz", "mitte_cm", "radius_m", "felder", "standort_begruendung", "sicht",
              "kameras", "marker", "budget"):
        if f not in o:
            b.append((FEHLER, oid, "Pflichtfeld fehlt: %s" % f))
    if not re.match(r"^%s_\d{2}_[a-z0-9_]+$" % re.escape(biom), oid):
        b.append((FEHLER, oid, "id muss '%s_<nn>_<name>' sein" % biom))
    art = o.get("art")
    if art not in ARTEN:
        b.append((FEHLER, oid, "art %r" % art))
    m = o.get("mitte_cm")
    if not _pkt(m, 3):
        b.append((FEHLER, oid, "mitte_cm [x, y, z] cm"))
        m = None
    s = o.get("sicht") or {}
    for f in ("naechster_weg_m", "sichtbar_ab_m"):
        if f not in s:
            b.append((WARNUNG, oid, "sicht.%s fehlt" % f))
    if "gelaende" in o and o["gelaende"]:
        g = o["gelaende"]
        b += _pruefe_fenster(oid, "gelaende", g, art, basis, typ="f32")
        if _zahl(g.get("max_aenderung_m")) and g["max_aenderung_m"] > 40:
            b.append((WARNUNG, oid, "gelaende.max_aenderung_m %.1f > 40 (begruenden)" % g["max_aenderung_m"]))
    if "lagen" in o and o["lagen"]:
        lg = o["lagen"]
        for n in lg.get("lagen", []):
            if n not in _daten.BODEN:
                b.append((FEHLER, oid, "Bodenlage %r unbekannt (FORMAT.md §2)" % n))
        b += _pruefe_fenster(oid, "lagen", lg, art, basis, suffixe=lg.get("lagen", []), typ="r8")
    seen = set()
    for w in o.get("wasser", []) or []:
        t = w.get("typ")
        if t not in ("see", "bach", "wasserfall"):
            b.append((FEHLER, oid, "wasser.typ %r" % t))
            continue
        if w.get("farbe") not in FARBEN:
            b.append((FEHLER, oid, "wasser.farbe %r (erlaubt: %s)" % (w.get("farbe"), ", ".join(FARBEN))))
        if t == "see":
            u = w.get("umriss_cm") or []
            if len(u) < 3 or not all(_pkt(p, 2) for p in u):
                b.append((FEHLER, oid, "see.umriss_cm: >= 3 Punkte [x, y]"))
            elif _flaeche(u) <= 0:
                b.append((FEHLER, oid, "see.umriss_cm im Uhrzeigersinn - muss gegen den Uhrzeigersinn "
                                       "(Flaeche > 0 in X/Y wie wasser_welt.json)"))
            for f in ("spiegel_cm", "tiefe_m"):
                if not _zahl(w.get(f)):
                    b.append((FEHLER, oid, "see.%s fehlt" % f))
            for k in ("id", "kennung", "name"):
                if w.get(k):
                    seen.add(w[k])
        elif t == "bach":
            p = w.get("punkte_cm") or []
            if len(p) < 2 or not all(_pkt(q, 4) for q in p):
                b.append((FEHLER, oid, "bach.punkte_cm: >= 2 Punkte [x, y, z, breite]"))
            else:
                anst = [p[k + 1][2] - p[k][2] for k in range(len(p) - 1)]
                if max(anst) > 1.0:
                    b.append((FEHLER, oid, "bach: Wasserspiegel steigt um bis %.0f cm (Quelle -> Muendung fallend)"
                              % max(anst)))
            for f in ("tiefe_cm",):
                if not _zahl(w.get(f)):
                    b.append((FEHLER, oid, "bach.%s fehlt" % f))
            if not isinstance(w.get("quelle"), bool):
                b.append((WARNUNG, oid, "bach.quelle true/false fehlt"))
            if not w.get("muendung"):
                b.append((WARNUNG, oid, "bach.muendung fehlt (Kennung oder 'versickert')"))
    for w in o.get("wasser", []) or []:
        if w.get("typ") == "wasserfall":
            k = w.get("kante_cm") or []
            if len(k) < 2 or not all(_pkt(q, 3) for q in k):
                b.append((FEHLER, oid, "wasserfall.kante_cm: >= 2 Punkte [x, y, z]"))
            elif _zahl(w.get("fuss_z_cm")) and w["fuss_z_cm"] >= min(q[2] for q in k):
                b.append((FEHLER, oid, "wasserfall.fuss_z_cm liegt nicht unter der Kante"))
            for f in ("fuss_z_cm", "breite_cm"):
                if not _zahl(w.get(f)):
                    b.append((FEHLER, oid, "wasserfall.%s fehlt" % f))
            if w.get("becken") and w["becken"] not in seen:
                b.append((WARNUNG, oid, "wasserfall.becken %r: kein see mit dieser Kennung (id)" % w["becken"]))
    eff = o.get("effekte", []) or []
    zahl = {"licht": 0, "nebel": 0, "niagara": 0, "decal": 0}
    for e in eff:
        t = e.get("typ")
        if t in ("punktlicht", "spotlicht"):
            zahl["licht"] += 1
            for f in ("pos_cm", "farbe", "intensitaet_cd", "radius_cm"):
                if f not in e:
                    b.append((FEHLER, oid, "%s.%s fehlt" % (t, f)))
            if e.get("schatten"):
                b.append((HINWEIS, oid, "Licht mit Schatten - begruenden"))
        elif t == "lokaler_nebel":
            zahl["nebel"] += 1
            for f in ("pos_cm", "radius_cm", "dichte"):
                if f not in e:
                    b.append((FEHLER, oid, "lokaler_nebel.%s fehlt" % f))
        elif t == "niagara":
            zahl["niagara"] += 1
            if not e.get("optional"):
                b.append((FEHLER, oid, "niagara: im Projekt gibt es keine Niagara-Systeme -> \"optional\": true"))
        elif t == "decal":
            zahl["decal"] += 1
            for f in ("material", "pos_cm", "groesse_cm"):
                if f not in e:
                    b.append((FEHLER, oid, "decal.%s fehlt" % f))
        else:
            b.append((FEHLER, oid, "effekte.typ %r" % t))
    for n, mx in (("licht", 4), ("nebel", 2), ("niagara", 3), ("decal", 12)):
        if zahl[n] > mx:
            b.append((FEHLER, oid, "%d %s-Effekte > %d" % (zahl[n], n, mx)))
    for mw in o.get("materialwuensche", []) or []:
        if not str(mw.get("name", "")).startswith("MI_EL_SW_"):
            b.append((FEHLER, oid, "materialwunsch.name muss mit MI_EL_SW_ beginnen: %r" % mw.get("name")))
        if mw.get("basis") not in MASTER:
            b.append((FEHLER, oid, "materialwunsch.basis %r ist kein erlaubter Master" % mw.get("basis")))
    b += pruefe_kameras(oid, art, o.get("kameras"), m)
    mk = o.get("marker") or {}
    if not mk.get("titel") or not mk.get("text"):
        b.append((WARNUNG, oid, "marker.titel/text leer"))
    bu = o.get("budget") or {}
    for k, mx in BUDGET.items():
        v = bu.get(k)
        if not _zahl(v):
            b.append((WARNUNG, oid, "budget.%s fehlt" % k))
        elif v > mx:
            b.append((WARNUNG, oid, "budget.%s = %d > Richtwert %d" % (k, v, mx)))
    if _zahl(bu.get("lichter")) and bu["lichter"] != zahl["licht"]:
        b.append((HINWEIS, oid, "budget.lichter %d, effekte %d" % (bu["lichter"], zahl["licht"])))
    for a in o.get("assets_wunsch", []) or []:
        if not a.get("paket") or "statt_jetzt" not in a:
            b.append((WARNUNG, oid, "assets_wunsch braucht paket + statt_jetzt (Ersatz aus Inventar)"))
    return b


def pruefe_orte(d, basis=None):
    """Prueft eine orte.json (Phase 2). basis: Ordner der Datei (fuer gelaende/lagen-Dateien)."""
    b = []
    biom = d.get("biom")
    if biom not in _daten.BIOME:
        b.append((FEHLER, "-", "biom %r unbekannt" % biom))
    orte = d.get("orte") or []
    for o in orte:
        b += pruefe_ort(o, biom or "?", basis)
    mw = sum(len(o.get("materialwuensche", []) or []) for o in orte)
    if mw > 6:
        b.append((FEHLER, biom, "%d Materialwuensche > 6 je Biom" % mw))
    b += pruefe_global([(biom, o, "") for o in orte])
    return b


# ============================================================================================
# Ausgabe / CLI
# ============================================================================================
def melde(befunde, titel=""):
    """Gibt Befunde ASCII aus. Rueckgabe dict Zaehler."""
    z = {FEHLER: 0, WARNUNG: 0, HINWEIS: 0}
    for st, oid, txt in befunde:
        z[st] = z.get(st, 0) + 1
    log("Pruefung %s: %d FEHLER, %d WARNUNG, %d HINWEIS" % (titel, z[FEHLER], z[WARNUNG], z[HINWEIS]))
    for st in (FEHLER, WARNUNG, HINWEIS):
        for s, oid, txt in befunde:
            if s == st:
                log("  %-7s %-28s %s" % (s, ascii_text(oid)[:28], ascii_text(txt)))
    return z


def main(argv=None):
    import argparse
    import json
    repo = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    ap = argparse.ArgumentParser(description="Pruefer gegen SEHENS_FORMAT (Auftrag 13)")
    ap.add_argument("--sehens", default=os.path.join(repo, "antworten", "sehens"))
    ap.add_argument("--datei", nargs="*", default=None, help="einzelne standorte.json / orte.json")
    ap.add_argument("--ohne-daten", action="store_true", help="nur Format, keine Gelaende-Regeln")
    _daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    welt = gel = None
    if not a.ohne_daten:
        try:
            from . import gelaende
            welt = _daten.lade(a.daten2m, a.daten1m)
            gel = gelaende.Gelaende(welt, cache=a.cache)
        except Exception as ex:
            log("Daten nicht geladen (%s) - nur Formatpruefung" % ex)
    alle = []
    if a.datei:
        for p in a.datei:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            if os.path.basename(p).startswith("orte") or any("budget" in o for o in d.get("orte", [])):
                bb = pruefe_orte(d, basis=os.path.dirname(os.path.abspath(p)))
            else:
                bb = pruefe_standorte(d, welt, gel)
            melde(bb, os.path.basename(p))
            alle += bb
    else:
        alle = pruefe_alle(a.sehens, welt, gel)
        melde(alle, a.sehens)
    return 1 if any(s == FEHLER for s, _, _ in alle) else 0


if __name__ == "__main__":
    sys.exit(main())
