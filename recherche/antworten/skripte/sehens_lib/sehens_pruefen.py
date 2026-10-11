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
  Pfade ("pfade", Auftrag 13c): Schema, >= 2 Punkte, breite_cm 120-200, art trampelpfad/serpentine/trittsteine,
    Anschluss (erster Punkt <= 30 m vom Wegenetz oder einem anderen Pfad, FEHLER), Steigung je Segment > 15 %
    (HINWEIS "Kehren noetig", bei serpentine erlaubt), schneidet Stadt/Meer (WARNUNG), quert Wasser (HINWEIS);
    Orte mit "pfad_id": Pfad muss existieren (alle Biome). Die Pfade ALLER Biome zaehlen als Wege
    (daten.lade rastert sie) - fuer Weg 80-300 m, Sicht und Erreichbarkeit.
  Global ueber alle Biome: Mindestabstand 350 m (beide in kleinen Biomen: 200 m), doppelte IDs (Orte, Pfade).
  --sicht: Leuchtfeuer aus 300-800 m von Weg/Pfad sichtbar (WARNUNG sonst), Fundstueck verdeckt (HINWEIS sonst).
  Phase 2 orte.json: Pflichtfelder §2, Gelaende/Lagen §3 (Fenster, max_aenderung, Dateigroessen, Rand = 0,
    |Delta| > 40 m nur mit 'begruendung' (Ferat 11.10.), mit Daten: keine Aenderung <= 2-3 m an Wegen/Wasser,
    Seeufer rundum ueber dem Spiegel nach dem Stempel), Wasser §5 (Umriss gegen Uhrzeigersinn = Flaeche > 0 in X/Y
    wie wasser_welt.json, Farben, Bachgefaelle), Effekte §6 (Niagara/Decal gegen inventar_extra.json: fehlt -> FEHLER,
    "optional": true -> HINWEIS), Klaenge, Pfad (13c), Materialwuensche §7 (<= 6 je Biom, Parameter der Master),
    Kameras §8, Budget §9, Witcher-Detailebenen (HINWEIS bei leeren Ebenen).
  Phase 2 Instanzen sw_<biom>/<Feld>/ (--ebene, Standard neben orte.json): plan.json-Schluessel, f32 = 10 float32 je
    Instanz, anzahl/instanzen/kollision_anzahl stimmen, Netze in netze.csv (nicht gesperrt, kein Houdini SW_*),
    Quaternion normiert, Massstab, Lage im Feldrechteck, <= 500 Akteure je Feld, Budget je Ort = orte.json-Budget
    und <= §9, mit Daten: Meer, Weg, Schweben/Versinken gegen das Gelaende nach dem Stempel.

API: pruefe_standorte(d, welt=None, gel=None), pruefe_orte(d, basis=None, inv=None, welt=None, sw_ordner=None),
     pruefe_ebene(sw_ordner, biom, inv, orte, welt, basis), pruefe_global(liste),
     pruefe_alle(sehens_ordner, welt=None, gel=None, sicht=False), pruefe_pfad(...), pruefe_pfade_datei(...),
     pruefe_sicht(liste, welt), melde(befunde, titel)
Befund = (stufe, ort_id, text) mit stufe in FEHLER / WARNUNG / HINWEIS.
"""

import math
import os
import re
import sys

import numpy as np

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
BUDGET_OPTIONAL = {"nebel": 2}
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
        if hoch == 0 or abs(hoch) > 5000:
            b.append((WARNUNG, oid, "Kamera %s: Hoch %s cm ungewoehnlich (Augenhoehe -170 oder 170)" % (name, hoch)))
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
            hk = (boden - hoch) if hoch < 0 else max(boden + hoch, zz + 300)
            if hoch > 0 and art_k in ("anmarsch", "fern") and hk - (boden + hoch) > 500:
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


# ============================================================================================
# Pfade (Auftrag 13c: "pfade" in standorte.json)
# ============================================================================================
PFAD_BREITE_CM = (120, 200)
PFAD_ANSCHLUSS_M = 30.0
PFAD_KEHREN_PROZENT = 15.0


def _pfad_linien(pfade, ausser=None):
    return [p["punkte_m"] for p in pfade if p.get("id") != ausser]


def pruefe_pfad(p, biom, welt=None, gel=None, alle_pfade=(), orte_ids=None):
    """Prueft einen Pfad-Eintrag. alle_pfade: normierte Pfade aller Biome (Anschluss an andere Pfade)."""
    b = []
    if not isinstance(p, dict):
        return [(FEHLER, biom, "pfade: Eintrag muss ein Objekt sein")]
    pid = p.get("id")
    if not isinstance(pid, str) or not pid:
        return [(FEHLER, biom, "Pfad ohne id")]
    if not re.match(r"^%s_pfad_[a-z0-9_]+$" % re.escape(biom), pid):
        b.append((FEHLER, pid, "Pfad-id muss '%s_pfad_<name>' sein (klein, ASCII)" % biom))
    art = p.get("art")
    if art not in _daten.PFAD_ARTEN:
        b.append((FEHLER, pid, "art %r (%s)" % (art, "/".join(_daten.PFAD_ARTEN))))
    br = p.get("breite_cm")
    if not _zahl(br):
        b.append((FEHLER, pid, "breite_cm fehlt"))
    elif not (PFAD_BREITE_CM[0] <= br <= PFAD_BREITE_CM[1]):
        b.append((FEHLER, pid, "breite_cm %s (Soll %d-%d cm)" % (br, PFAD_BREITE_CM[0], PFAD_BREITE_CM[1])))
    pts = p.get("punkte_cm")
    if not isinstance(pts, list) or len(pts) < 2 or not all(_pkt(q, 2) for q in pts):
        b.append((FEHLER, pid, "punkte_cm: mindestens 2 Punkte [x, y] in cm"))
        return b
    if not isinstance(p.get("anschluss"), str) or not p.get("anschluss"):
        b.append((WARNUNG, pid, "anschluss fehlt (welcher Weg/Ort, Startpunkt)"))
    fuer = p.get("fuer")
    if not isinstance(fuer, list):
        b.append((WARNUNG, pid, "fuer muss eine Liste von Ort-ids sein"))
    elif not fuer:
        b.append((HINWEIS, pid, "fuer ist leer (Pfad ohne Ort)"))
    elif orte_ids is not None:
        for oid in fuer:
            if oid not in orte_ids:
                b.append((WARNUNG, pid, "fuer: Ort %r gibt es nicht" % oid))
    for f in ("laenge_m", "max_steigung_grad"):
        if not _zahl(p.get(f)):
            b.append((WARNUNG, pid, "%s fehlt" % f))
    pm = [[q[0] / 100.0, q[1] / 100.0] for q in pts]
    if welt is None:
        return b
    from . import gelaende as _gel
    if not all(welt.im_raster_m(x, y) for x, y in pm):
        b.append((FEHLER, pid, "Punkte ausserhalb der Welt"))
        return b
    # Anschluss: erster Punkt <= 30 m vom Wegenetz (ohne Pfade) oder von einem anderen Pfad
    x0, y0 = pm[0]
    d_netz = float("inf")
    if gel is not None:
        i, j = welt.m_zu_ij(x0, y0)
        d_netz = float(gel.abstand_weg_basis[i, j])
    d_pfad = _gel.abstand_zu_polylinien(x0, y0, _pfad_linien(alle_pfade, ausser=pid))
    if gel is None and not alle_pfade:
        b.append((HINWEIS, pid, "Anschluss nicht geprueft (keine Gelaendedaten)"))
    elif min(d_netz, d_pfad) > PFAD_ANSCHLUSS_M:
        b.append((FEHLER, pid, "schliesst nicht an: erster Punkt %.0f m vom Wegenetz, %.0f m vom naechsten Pfad "
                               "(Soll <= %.0f m)" % (d_netz, d_pfad, PFAD_ANSCHLUSS_M)))
    # Steigung je Segment
    pr = _gel.pfad_profil(welt, pm)
    steil = [sg for sg in pr["segmente"] if sg["max_prozent"] > PFAD_KEHREN_PROZENT]
    if steil and art != "serpentine":
        b.append((HINWEIS, pid, "%d von %d Segmenten > %.0f %% (max %.0f %% = %.0f Grad, %.0f m steil): Kehren noetig"
                  % (len(steil), len(pr["segmente"]), PFAD_KEHREN_PROZENT, pr["max_steigung_prozent"],
                     pr["max_steigung_grad"], pr["laenge_ueber_15_prozent_m"])))
    if _zahl(p.get("laenge_m")) and abs(p["laenge_m"] - pr["laenge_m"]) > max(5.0, 0.1 * pr["laenge_m"]):
        b.append((HINWEIS, pid, "laenge_m %.0f, aus punkte_cm %.0f m" % (p["laenge_m"], pr["laenge_m"])))
    # Stadt / Meer / Suesswasser entlang der Linie
    x, y = _daten.polylinie_dichte(pm, welt.zelle_m)
    i, j = welt.m_zu_ij(x, y)
    n_meer = int(welt.meer[i, j].sum())
    if n_meer:
        b.append((WARNUNG, pid, "schneidet das Meer auf ca. %.0f m" % (n_meer * welt.zelle_m)))
    xs, ys, rs = welt.staedte_m()
    if xs.size:
        dd = np.hypot(x[:, None] - xs[None, :], y[:, None] - ys[None, :]) - rs[None, :]
        innen = dd.min(axis=0) < 0
        if innen.any():
            namen = [str(welt.staedte[k].get("id")) for k in np.flatnonzero(innen)]
            b.append((WARNUNG, pid, "schneidet die geplante Stadt %s" % ", ".join(namen)))
    n_w = int((welt.wasser[i, j] > 0).sum())
    if n_w and art != "trittsteine":
        b.append((HINWEIS, pid, "quert Suesswasser auf ca. %.0f m (Trittsteine/Furt)" % (n_w * welt.zelle_m)))
    return b


def _pfade_der_datei(d, biom):
    out = []
    for p in d.get("pfade") or []:
        n = _daten.normiere_pfad(p, biom=biom)
        if n is not None:
            out.append(n)
    return out


def _pfade_vereinigt(eigene, welt):
    """Pfade dieser Datei + uebrige Pfade der Welt (andere Biome), eigene haben Vorrang."""
    ids = {p["id"] for p in eigene}
    return list(eigene) + [p for p in (getattr(welt, "pfade", None) or []) if p["id"] not in ids]


def pruefe_pfade_datei(d, biom, welt=None, gel=None, alle_pfade=None, orte_ids=None):
    """Pfade einer standorte.json + pfad_id der Orte. alle_pfade/orte_ids: global (alle Biome)."""
    b = []
    pfade = d.get("pfade")
    orte = [o for o in (d.get("orte") or []) if isinstance(o, dict)]
    if pfade is not None and not isinstance(pfade, list):
        return [(FEHLER, biom, "'pfade' muss eine Liste sein")]
    pfade = pfade or []
    eigene = _pfade_der_datei(d, biom)
    if alle_pfade is None:
        alle_pfade = _pfade_vereinigt(eigene, welt)
        if welt is not None and eigene and _daten.pfade_kennung(alle_pfade) != getattr(welt, "pfade_kennung", ""):
            b.append((HINWEIS, biom, "Welt ohne den aktuellen Pfadstand geladen - Wegabstaende gegen alten Stand "
                                     "(daten.lade() neu aufrufen)"))
    if orte_ids is None:
        orte_ids = {o.get("id") for o in orte}
    gesehen = set()
    for p in pfade:
        pid = p.get("id") if isinstance(p, dict) else None
        if pid in gesehen:
            b.append((FEHLER, pid, "doppelte Pfad-id"))
        gesehen.add(pid)
        b += pruefe_pfad(p, biom, welt, gel, alle_pfade, orte_ids)
    alle_ids = {p["id"]: p for p in alle_pfade}
    for o in orte:
        pid = o.get("pfad_id")
        if pid is None:
            continue
        if not isinstance(pid, str) or pid not in alle_ids:
            b.append((FEHLER, o.get("id", "?"), "pfad_id %r: diesen Pfad gibt es nicht" % (pid,)))
        elif isinstance(alle_ids[pid].get("fuer"), list) and o.get("id") not in alle_ids[pid]["fuer"]:
            b.append((HINWEIS, o.get("id", "?"), "pfad_id %s: Ort fehlt in dessen 'fuer'" % pid))
    return b


def pruefe_sicht(liste, welt, abstand_m=20.0):
    """Sicht vom Weg/Pfad (welt.weg inkl. Pfade): Leuchtfeuer aus 300-800 m sichtbar (WARNUNG sonst),
    Fundstueck vom Weg/Pfad aus verdeckt (HINWEIS sonst). liste: [(biom, ort, datei), ...]."""
    from . import sicht as _sicht
    b = []
    wp = _sicht.Wegpunkte(welt, abstand_m)
    for _, o, _ in liste:
        m = o.get("mitte_cm")
        if not _pkt(m, 2):
            continue
        x, y = m[0] / 100.0, m[1] / 100.0
        oid = o.get("id", "?")
        H = o.get("ziel_hoehe_m") if _zahl(o.get("ziel_hoehe_m")) else None
        if o.get("art") == "leuchtfeuer":
            s = _sicht.sicht_von_wegen(welt, wp, x, y, H or 15.0)
            if s["n_sichtbar"] == 0:
                b.append((WARNUNG, oid, "Leuchtfeuer: von keinem Weg/Pfad aus 300-800 m sichtbar (Ziel %.0f m)"
                          % (H or 15.0)))
            else:
                b.append((HINWEIS, oid, "Leuchtfeuer: %d Weg-/Pfadpunkte sehen es (300-800 m), ab %.0f m"
                          % (s["n_sichtbar"], s["sichtbar_ab_m"] or 0)))
        elif o.get("art") == "fundstueck":
            v = _sicht.verdeckt_vom_weg(welt, wp, x, y, min(H or 3.0, 3.0))
            if not v["verdeckt"]:
                ns = v.get("naechste_sicht_m")
                b.append((HINWEIS, oid, "Fundstueck: vom Weg/Pfad aus sichtbar (max. Anteil %.2f, naechste Sicht %s m) "
                                        "- Rahmen/Stempel noetig" % (v["max_anteil"], "%.0f" % ns if ns is not None else "?")))
    return b


def pruefe_standorte(d, welt=None, gel=None, biom=None, global_pruefen=True, alle_pfade=None, orte_ids=None):
    """Prueft eine standorte.json (dict). global_pruefen: Abstaende/IDs innerhalb der Datei.
    alle_pfade/orte_ids: Pfade und Ort-ids aller Biome (sonst: diese Datei + welt.pfade)."""
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
    b += pruefe_pfade_datei(d, biom or "?", welt, gel, alle_pfade, orte_ids)
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


def pruefe_alle(sehens_ordner, welt=None, gel=None, sicht=False):
    """Alle <sehens_ordner>/*/standorte.json einzeln + global (Abstaende, ids, Pfade aller Biome).
    sicht=True: zusaetzlich Sicht vom Weg/Pfad (pruefe_sicht, braucht welt). Rueckgabe Befunde."""
    from .format import alle_standorte, lade_standorte
    import glob
    b = []
    dateien = []
    for p in sorted(glob.glob(os.path.join(sehens_ordner, "*", "standorte.json"))):
        try:
            d = lade_standorte(p)
        except Exception as ex:
            b.append((FEHLER, p, "JSON nicht lesbar: %s" % ex))
            continue
        biom = d.get("biom") or os.path.basename(os.path.dirname(p))
        if biom != os.path.basename(os.path.dirname(p)):
            b.append((WARNUNG, biom, "biom %r passt nicht zum Ordner %s" % (biom, p)))
        dateien.append((p, d, biom))
    alle_pfade, pfad_biom = [], {}
    for p, d, biom in dateien:
        for q in _pfade_der_datei(d, biom):
            if q["id"] in pfad_biom:
                b.append((FEHLER, q["id"], "doppelte Pfad-id (auch in %s)" % pfad_biom[q["id"]]))
                continue
            pfad_biom[q["id"]] = biom
            alle_pfade.append(q)
    if welt is not None and alle_pfade and _daten.pfade_kennung(alle_pfade) != getattr(welt, "pfade_kennung", ""):
        b.append((HINWEIS, "-", "Welt ohne den aktuellen Pfadstand geladen (daten.lade(pfade=<sehens>))"))
    liste = alle_standorte(sehens_ordner)
    orte_ids = {o.get("id") for _, o, _ in liste if isinstance(o, dict)}
    for p, d, biom in dateien:
        b += pruefe_standorte(d, welt, gel, biom, global_pruefen=False, alle_pfade=alle_pfade, orte_ids=orte_ids)
    b += pruefe_global(liste)
    if sicht and welt is not None:
        b += pruefe_sicht([(bb, o, q) for bb, o, q in liste if q.endswith("standorte.json")], welt)
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
                    b.append((HINWEIS if g.get("begruendung") else WARNUNG, oid,
                              "%s: |Delta| bis %.1f m > 40 m (Ferat 11.10.: erlaubt, %s)"
                              % (df, mx, "begruendet" if g.get("begruendung") else "bitte 'begruendung' setzen")))
                if not np.isfinite(a).all():
                    b.append((FEHLER, oid, "%s: NaN/Inf im Gelaende-Delta" % df))
                if abs(mx - float(g.get("max_aenderung_m", mx))) > 0.5:
                    b.append((HINWEIS, oid, "%s: max_aenderung_m %.1f, Datei %.1f" % (df, g.get("max_aenderung_m"), mx)))
    return b


def pruefe_ort(o, biom, basis=None, inv=None, welt=None):
    """Ein orte.json-Eintrag (Phase 2). inv: inventar.Inventar (Asset-Pruefung), welt: Kameras/Gelaende-Regeln."""
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
        if _zahl(g.get("max_aenderung_m")) and g["max_aenderung_m"] > 40 and not g.get("begruendung"):
            b.append((WARNUNG, oid, "gelaende.max_aenderung_m %.1f > 40 ohne 'begruendung'" % g["max_aenderung_m"]))
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
            for f in ("asset", "pos_cm"):
                if f not in e:
                    b.append((FEHLER, oid, "niagara.%s fehlt" % f))
            if inv is not None:
                b += [(st, oid, tx) for st, tx in inv.asset_pruefen("niagara", e.get("asset"), bool(e.get("optional")))]
            elif not e.get("optional"):
                b.append((HINWEIS, oid, "niagara %s: ohne Inventar nicht pruefbar" % e.get("asset")))
        elif t == "decal":
            zahl["decal"] += 1
            for f in ("material", "pos_cm", "groesse_cm"):
                if f not in e:
                    b.append((FEHLER, oid, "decal.%s fehlt" % f))
            if inv is not None and e.get("material"):
                b += [(st, oid, tx) for st, tx in inv.asset_pruefen("decal", e["material"], bool(e.get("optional")))]
        else:
            b.append((FEHLER, oid, "effekte.typ %r" % t))
    for n, mx in (("licht", 4), ("nebel", 2), ("niagara", 3), ("decal", 12)):
        if zahl[n] > mx:
            b.append((FEHLER, oid, "%d %s-Effekte > %d" % (zahl[n], n, mx)))
    for mw in o.get("materialwuensche", []) or []:
        if inv is not None:
            b += [(st, oid, tx) for st, tx in inv.material_pruefen(mw)]
            continue
        if not str(mw.get("name", "")).startswith("MI_EL_SW_"):
            b.append((FEHLER, oid, "materialwunsch.name muss mit MI_EL_SW_ beginnen: %r" % mw.get("name")))
        if mw.get("basis") not in MASTER:
            b.append((FEHLER, oid, "materialwunsch.basis %r ist kein erlaubter Master" % mw.get("basis")))
    for k in o.get("klaenge", []) or []:
        if not k.get("asset") or not _pkt(k.get("pos_cm"), 3):
            b.append((FEHLER, oid, "klaenge: asset und pos_cm [x, y, z] noetig"))
        elif inv is not None:
            b += [(st, oid, tx) for st, tx in inv.asset_pruefen("klang", k["asset"], bool(k.get("optional")))]
    for pk, pf in [("pfad", o.get("pfad")), ("pfad_zugang", o.get("pfad_zugang"))] + \
            [("pfad_abschnitte[%d]" % k, q) for k, q in enumerate(o.get("pfad_abschnitte") or [])]:
        if not pf:
            continue
        pts = pf.get("punkte_cm") or []
        if len(pts) < 2 or not all(_pkt(q, 2) for q in pts):
            b.append((FEHLER, oid, "%s.punkte_cm: >= 2 Punkte [x, y] (13c)" % pk))
        if not (_zahl(pf.get("breite_cm")) and 120 <= pf["breite_cm"] <= 200):
            b.append((FEHLER, oid, "%s.breite_cm %r (Soll 120-200, 13c)" % (pk, pf.get("breite_cm"))))
        if pf.get("art") not in _daten.PFAD_ARTEN:
            b.append((FEHLER, oid, "%s.art %r (%s)" % (pk, pf.get("art"), "/".join(_daten.PFAD_ARTEN))))
    de = o.get("detail_ebenen")
    if isinstance(de, dict):
        for eb in ("held", "begleiter", "schutt", "kleinzeug", "bewuchs", "kontakt"):
            if not (de.get(eb) or {}).get("anzahl"):
                b.append((HINWEIS, oid, "Witcher-Detailebene '%s' leer" % eb))
    if welt is not None:
        b += pruefe_ort_gelaende(o, basis, welt)
    b += pruefe_kameras(oid, art, o.get("kameras"), m, welt)
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


def pruefe_orte(d, basis=None, inv=None, welt=None, sw_ordner=None):
    """Prueft eine orte.json (Phase 2). basis: Ordner der Datei (fuer gelaende/lagen-Dateien), inv: Inventar
    (Assets), welt: Gelaende-Regeln, sw_ordner: Instanz-Ebene sw_<biom> (Format, Assets, Budget-Abgleich)."""
    b = []
    biom = d.get("biom")
    if biom not in _daten.BIOME:
        b.append((FEHLER, "-", "biom %r unbekannt" % biom))
    orte = d.get("orte") or []
    for o in orte:
        b += pruefe_ort(o, biom or "?", basis, inv, welt)
    if sw_ordner is not None:
        b += pruefe_ebene(sw_ordner, biom, inv, orte, welt, basis)
    mw = sum(len(o.get("materialwuensche", []) or []) for o in orte)
    if mw > 6:
        b.append((FEHLER, biom, "%d Materialwuensche > 6 je Biom" % mw))
    b += pruefe_global([(biom, o, "") for o in orte])
    return b



# ============================================================================================
# Phase 2: Gelaende gegen Daten, Instanz-Ebene sw_<biom>
# ============================================================================================
class BodenNachStempel:
    """Bodenhoehe NACH den Gelaendestempeln aller Orte einer orte.json (Welt bilinear + 1-m-Deltas)."""

    def __init__(self, welt, orte, basis):
        self.welt = welt
        self.deltas = []
        for o in orte or []:
            g = o.get("gelaende") or {}
            fij = g.get("fenster_ij")
            if not (basis and g.get("datei") and isinstance(fij, list) and len(fij) == 4):
                continue
            pf = os.path.join(basis, g["datei"])
            if os.path.exists(pf) and os.path.getsize(pf) == fij[2] * fij[3] * 4:
                self.deltas.append((fij, np.fromfile(pf, dtype="<f4").reshape(fij[2], fij[3])))

    def delta(self, x_m, y_m):
        x = np.asarray(x_m, np.float64)
        y = np.asarray(y_m, np.float64)
        out = np.zeros(np.broadcast(x, y).shape)
        for (i0, j0, hh, ww), a in self.deltas:
            fi = y + _daten.OFF_I - i0
            fj = x + _daten.OFF_J - j0
            innen = (fi >= 0) & (fi <= hh - 1) & (fj >= 0) & (fj <= ww - 1)
            if not innen.any():
                continue
            i = np.clip(np.floor(fi).astype(np.int64), 0, hh - 2)
            j = np.clip(np.floor(fj).astype(np.int64), 0, ww - 2)
            di = np.clip(fi - i, 0, 1)
            dj = np.clip(fj - j, 0, 1)
            v = (a[i, j] * (1 - di) * (1 - dj) + a[i, j + 1] * (1 - di) * dj + a[i + 1, j] * di * (1 - dj) +
                 a[i + 1, j + 1] * di * dj)
            out = np.where(innen, out + v, out)
        return out

    def hoehe(self, x_m, y_m):
        return self.welt.bilinear(self.welt.hoehe, np.asarray(x_m, np.float64), np.asarray(y_m, np.float64)) + \
            self.delta(x_m, y_m)


def pruefe_ort_gelaende(o, basis, welt):
    """§3 mit Daten: keine Aenderung <= 3 m an Wegen/bestehendem Wasser (ausser 'ist_wasser'), Seeufer rundum
    ueber dem Spiegel (Gelaende nach Stempel), Kamera/Ort nicht im Meer."""
    b = []
    oid = o.get("id", "?")
    g = o.get("gelaende") or {}
    fij = g.get("fenster_ij")
    a = None
    if basis and g.get("datei") and isinstance(fij, list) and len(fij) == 4:
        pf = os.path.join(basis, g["datei"])
        if os.path.exists(pf) and os.path.getsize(pf) == fij[2] * fij[3] * 4:
            a = np.fromfile(pf, dtype="<f4").reshape(fij[2], fij[3])
    if a is not None:
        i0, j0, hh, ww = fij
        z = welt.zelle_m
        ii = np.clip(((np.arange(i0, i0 + hh)) // int(z)).astype(np.int64), 0, welt.ny - 1)
        jj = np.clip(((np.arange(j0, j0 + ww)) // int(z)).astype(np.int64), 0, welt.nx - 1)
        weg = welt.weg[ii][:, jj] > 0
        wasser = welt.wasser[ii][:, jj] > 0
        from . import gelaende as _g
        geaendert = np.abs(a) > 0.05
        for name, m in (("Weg", weg), ("bestehendem Wasser", wasser)):
            if name != "Weg" and g.get("ist_wasser"):
                continue
            if not m.any() or not geaendert.any():
                continue
            d = _g.abstand(m, 1.0, 10.0)
            n = int((geaendert & (d <= 2.0)).sum())
            if n:
                b.append((WARNUNG if name != "Weg" else FEHLER, oid,
                          "Gelaende aendert sich %d m2 naeher als 2 m an %s (Soll: keine Aenderung <= 3 m, §3)" % (n, name)))
    # Seeufer
    boden = BodenNachStempel(welt, [o], basis)
    for w in o.get("wasser", []) or []:
        if w.get("typ") != "see" or not w.get("umriss_cm") or not _zahl(w.get("spiegel_cm")):
            continue
        from .rezept import ufer_freibord
        u = np.asarray(w["umriss_cm"], np.float64) / 100.0
        tief = -ufer_freibord(boden.hoehe, u, float(w["spiegel_cm"]) / 100.0, welt.zelle_m)
        if tief > 0.05:
            b.append((WARNUNG, oid, "see %s: Ufer haelt nicht - auf einem Strahl 0,5-3 m hinter dem Umriss bis %.2f m "
                                    "UNTER dem Spiegel (Gelaende nach Stempel)" % (w.get("id"), tief)))
    m = o.get("mitte_cm")
    if _pkt(m, 2) and welt.im_raster_m(m[0] / 100.0, m[1] / 100.0):
        i, j = welt.cm_zu_ij(m[0], m[1])
        if welt.meer[i, j]:
            b.append((FEHLER, oid, "Mitte liegt im Meer"))
    return b


def pruefe_ebene(sw_ordner, biom, inv=None, orte=None, welt=None, basis=None):
    """Instanz-Ebene sw_<biom>/<Feld>/ (FORMAT.md §3, SEHENS_FORMAT §4, §9): plan.json-Schluessel, f32-Groessen,
    Anzahlen, Assets (netze.csv, Sperre, Houdini), Quaternion/Massstab, Lage im Feld, Akteure (<= 500 je Feld),
    Budget je Ort gegen orte.json, mit Welt: Meer, Weg, Schweben/Versinken gegen das Gelaende NACH dem Stempel."""
    from . import instanzen as _ins
    b = []
    tag = "sw_%s" % biom
    ebene = _ins.lies_ebene(sw_ordner)
    if not ebene:
        b.append((WARNUNG, tag, "keine Felder in %s" % sw_ordner))
        return b
    je_ort = {}
    boden = BodenNachStempel(welt, orte, basis) if welt is not None else None
    # Orte, die bestehendes Wasser SIND (gelaende.ist_wasser): dort sind Instanzen im Bestandswasser gewollt
    wasser_fenster = [(o["gelaende"]["fenster_ij"]) for o in (orte or [])
                      if (o.get("gelaende") or {}).get("ist_wasser") and o["gelaende"].get("fenster_ij")]
    ort_re = re.compile(r"^(%s_\d{2}_[a-z0-9_]+?)_[a-z0-9_]+$" % re.escape(biom))
    orte_ids = {o.get("id") for o in (orte or [])}

    def ort_von_klasse(k):
        for oid in orte_ids:
            if k.startswith(oid + "_"):
                return oid
        mm = ort_re.match(k or "")
        return mm.group(1) if mm else None

    for feld, (plan, arr) in sorted(ebene.items()):
        ft = "%s/%s" % (tag, feld)
        for k in ("stand", "feld", "instanzen", "dateien", "akteure"):
            if k not in plan:
                b.append((FEHLER, ft, "plan.json: Schluessel %s fehlt" % k))
        if plan.get("feld") != feld:
            b.append((FEHLER, ft, "plan.json feld %r passt nicht zum Ordner" % plan.get("feld")))
        try:
            x0, y0, x1, y1 = _daten.feld_grenzen_m(feld)
        except (ValueError, IndexError):
            b.append((FEHLER, ft, "Ordnername ist kein Feld"))
            continue
        summe = kol = 0
        n_schwebt = n_vers = n_weg = n_wasser = n_aussen = 0
        for key, d in (plan.get("dateien") or {}).items():
            a = arr.get(key)
            if a is None:
                b.append((FEHLER, ft, "%s.f32 fehlt" % key))
                continue
            if a.ndim != 2:
                b.append((FEHLER, ft, "%s.f32: Groesse kein Vielfaches von 40 Bytes" % key))
                continue
            if a.shape[0] != d.get("anzahl"):
                b.append((FEHLER, ft, "%s: anzahl %s, Datei %d" % (key, d.get("anzahl"), a.shape[0])))
            summe += a.shape[0]
            if d.get("kollision"):
                kol += a.shape[0]
            for f in ("pfad", "anzahl", "sichtweite", "kollision"):
                if f not in d:
                    b.append((FEHLER, ft, "%s: Schluessel %s fehlt" % (key, f)))
            if inv is not None:
                b += [(st, ft, "%s: %s" % (key, tx)) for st, tx in inv.netz_pruefen(d.get("pfad", key))]
            if not np.isfinite(a).all():
                b.append((FEHLER, ft, "%s: NaN/Inf" % key))
                continue
            qn = np.linalg.norm(a[:, 3:7], axis=1)
            if np.abs(qn - 1).max() > 1e-3:
                b.append((FEHLER, ft, "%s: Quaternion nicht normiert (max |q| %.4f)" % (key, qn.max())))
            if (a[:, 7:10] <= 0).any() or (a[:, 7:10] > 60).any():
                b.append((FEHLER, ft, "%s: Massstab <= 0 oder > 60" % key))
            xm, ym = a[:, 0] / 100.0, a[:, 1] / 100.0
            aus = (xm < x0) | (xm >= x1) | (ym < y0) | (ym >= y1)
            n_aussen += int(aus.sum())
            for oid, n in (d.get("orte") or {}).items():
                z = je_ort.setdefault(oid, {"instanzen": 0, "kollision": 0, "akteure": 0})
                z["instanzen"] += n
                if d.get("kollision"):
                    z["kollision"] += n
            if welt is not None:
                bz = boden.hoehe(xm, ym)
                zz = a[:, 2] / 100.0
                # Unter-/Oberkante aus den Netz-Bounds (Pivot kann oben liegen, z. B. Efeu), Naeherung aufrecht
                if inv is not None and inv.netz_pfad(d.get("pfad", "")):
                    info = inv.netz(d["pfad"])
                    (_, _, bz0), (_, _, bz1) = info["bounds_cm"]
                    unter = zz + bz0 / 100.0 * a[:, 9]
                    ober = zz + bz1 / 100.0 * a[:, 9]
                else:
                    unter, ober = zz, zz + 1.0
                # Toleranz waechst mit der Hangneigung (Interpolation zwischen Zellen an Stempelkanten/Waenden)
                gx = (boden.hoehe(xm + 1.0, ym) - boden.hoehe(xm - 1.0, ym)) / 2.0
                gy = (boden.hoehe(xm, ym + 1.0) - boden.hoehe(xm, ym - 1.0)) / 2.0
                tol = 0.35 + 0.5 * welt.zelle_m + np.hypot(gx, gy) * welt.zelle_m
                n_schwebt += max(0, int((unter - bz > tol).sum()) - int(d.get("z_frei_anzahl", 0)))
                n_vers += int((ober < bz - 0.5 - np.hypot(gx, gy) * welt.zelle_m).sum())
                i, j = welt.m_zu_ij(xm, ym)
                if (bz < -0.3).any():
                    b.append((FEHLER, ft, "%s: %d Instanzen im Meer (Boden < -0,3 m)" % (key, int((bz < -0.3).sum()))))
                n_weg += int((welt.weg_basis[i, j] > 0).sum()) if "pfad" not in str(d.get("gruppe")) else 0
                if not any(t in str(d.get("gruppe", "")) for t in ("wasser", "pfad")):
                    nass = welt.wasser[i, j] > 0
                    for (fi0, fj0, fh, fw) in wasser_fenster:
                        ii1 = ym + _daten.OFF_I
                        jj1 = xm + _daten.OFF_J
                        nass &= ~((ii1 >= fi0) & (ii1 < fi0 + fh) & (jj1 >= fj0) & (jj1 < fj0 + fw))
                    n_wasser += int(nass.sum())
        if summe != plan.get("instanzen"):
            b.append((FEHLER, ft, "instanzen %s, Summe der Dateien %d" % (plan.get("instanzen"), summe)))
        if "kollision_anzahl" in plan and kol != plan["kollision_anzahl"]:
            b.append((FEHLER, ft, "kollision_anzahl %s, Summe %d" % (plan["kollision_anzahl"], kol)))
        if summe > 60000:
            b.append((WARNUNG, ft, "%d Instanzen > 60 000 je Feld (alle Ebenen zusammen!)" % summe))
        ak = plan.get("akteure") or []
        if len(ak) > 500:
            b.append((FEHLER, ft, "%d Akteure > 500 je Feld" % len(ak)))
        for k, e in enumerate(ak):
            fehlt = [f for f in ("netz", "pfad", "x", "y", "z", "qx", "qy", "qz", "qw", "sx", "sy", "sz", "klasse")
                     if f not in e]
            if fehlt:
                b.append((FEHLER, ft, "akteur %d: %s fehlt" % (k, ", ".join(fehlt))))
                continue
            if inv is not None:
                b += [(st, ft, "akteur %s: %s" % (e["netz"], tx)) for st, tx in inv.netz_pruefen(e["pfad"])]
            if not (x0 <= e["x"] / 100.0 < x1 and y0 <= e["y"] / 100.0 < y1):
                n_aussen += 1
            qn = math.sqrt(e["qx"] ** 2 + e["qy"] ** 2 + e["qz"] ** 2 + e["qw"] ** 2)
            if abs(qn - 1) > 1e-3:
                b.append((FEHLER, ft, "akteur %s: Quaternion nicht normiert" % e["netz"]))
            oid = ort_von_klasse(e["klasse"])
            if oid is None:
                b.append((FEHLER, ft, "akteur klasse %r muss '<ort_id>_<rolle>' sein" % e["klasse"]))
            else:
                je_ort.setdefault(oid, {"instanzen": 0, "kollision": 0, "akteure": 0})["akteure"] += 1
            if welt is not None and _zahl(e.get("unterkante_z")) and _zahl(e.get("boden_z")):
                bz = float(boden.hoehe(e["x"] / 100.0, e["y"] / 100.0))
                if e["unterkante_z"] / 100.0 > bz + 0.3 + 0.5 * welt.zelle_m and not e.get("z_frei"):
                    b.append((WARNUNG, ft, "akteur %s (%s): Unterkante %.1f m ueber dem Boden"
                              % (e["netz"], e["klasse"], e["unterkante_z"] / 100.0 - bz)))
        if n_aussen:
            b.append((FEHLER, ft, "%d Instanzen/Akteure ausserhalb des Feldrechtecks (Setzer ueberspringt sie)" % n_aussen))
        if n_schwebt:
            b.append((WARNUNG, ft, "%d Instanzen schweben (Unterkante > Boden nach Stempel + Toleranz)" % n_schwebt))
        if n_vers:
            b.append((HINWEIS, ft, "%d Instanzen ganz im Boden (Oberkante unter dem Boden)" % n_vers))
        if n_weg:
            b.append((WARNUNG, ft, "%d Instanzen auf dem Wegenetz" % n_weg))
        if n_wasser:
            b.append((HINWEIS, ft, "%d Instanzen im bestehenden Suesswasser (nicht Ebene wasser/pfad)" % n_wasser))
    # Budget je Ort gegen orte.json und §9
    for o in orte or []:
        oid = o.get("id")
        z = je_ort.get(oid, {"instanzen": 0, "kollision": 0, "akteure": 0})
        bu = o.get("budget") or {}
        for k in ("instanzen", "kollision", "akteure"):
            if _zahl(bu.get(k)) and int(bu[k]) != z[k]:
                b.append((FEHLER, oid, "budget.%s = %s, Ebene %s enthaelt %d" % (k, bu[k], tag, z[k])))
            if z[k] > BUDGET[k]:
                b.append((WARNUNG, oid, "%s %d > %d (§9)" % (k, z[k], BUDGET[k])))
    for oid in je_ort:
        if orte is not None and oid not in orte_ids:
            b.append((WARNUNG, oid, "Instanzen in %s fuer einen Ort, der nicht in orte.json steht" % tag))
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
    ap.add_argument("--sicht", action="store_true", help="auch Sicht vom Weg/Pfad (Leuchtfeuer/Fundstueck)")
    ap.add_argument("--ebene", default=None, help="Phase 2: Ordner sw_<biom> (Standard: neben orte.json, falls vorhanden)")
    ap.add_argument("--inventar", default=None, help="Ordner mit netze.csv/inventar_extra.json (Standard vorlagen/daten)")
    _daten.argumente_hinzufuegen(ap)
    a = ap.parse_args(argv)
    welt = gel = None
    if not a.ohne_daten:
        try:
            from . import gelaende
            welt = _daten.lade(a.daten2m, a.daten1m, pfade=a.sehens)
            gel = gelaende.Gelaende(welt, cache=a.cache)
        except Exception as ex:
            log("Daten nicht geladen (%s) - nur Formatpruefung" % ex)
    alle = []
    if a.datei:
        for p in a.datei:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            if os.path.basename(p).startswith("orte") or any("budget" in o for o in d.get("orte", [])):
                from . import inventar as _inv
                basis = os.path.dirname(os.path.abspath(p))
                try:
                    inv = _inv.Inventar.lade(a.inventar)
                except Exception as ex:
                    log("Inventar nicht geladen (%s) - keine Asset-Pruefung" % ex)
                    inv = None
                sw = a.ebene or os.path.join(basis, "sw_%s" % d.get("biom"))
                if not os.path.isdir(sw):
                    log("Hinweis: keine Ebene %s - Instanzen nicht geprueft (--ebene angeben)" % sw)
                    sw = None
                bb = pruefe_orte(d, basis=basis, inv=inv, welt=welt, sw_ordner=sw)
            else:
                bb = pruefe_standorte(d, welt, gel)
            melde(bb, os.path.basename(p))
            alle += bb
    else:
        alle = pruefe_alle(a.sehens, welt, gel, sicht=a.sicht)
        melde(alle, a.sehens)
    return 1 if any(s == FEHLER for s, _, _ in alle) else 0


if __name__ == "__main__":
    sys.exit(main())
