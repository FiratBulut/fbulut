"""format.py - Schreiber fuer standorte.json (Phase 1) und orte.json (Phase 2) nach SEHENS_FORMAT.

Phase 1 - antworten/sehens/<biom>/standorte.json:
  {"stand": "2026-10-11", "biom": "aue", "orte": [{
     "id": "aue_01_blautopf", "name": "Blautopf", "art": "fundstueck" | "leuchtfeuer",
     "mitte_cm": [x, y, z], "radius_m": 45, "felder": ["E5"],
     "kameras": [[Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch], ...],          # SEHENS_FORMAT §8
     "ziel_hoehe_m": 18,                                                # Silhouettenhoehe (Sichtpruefung)
     "standort_begruendung": "...", "sicht": {...}, "erreichbar": {...},
     "pfad_cm": [[x, y, z], ...] (optional, Fussweg Ort -> Weg), "draufsicht": "aue_01_blautopf.png" (optional),
     "pfad_id": "aue_pfad_<name>" (optional: Ort gilt nur ueber diesen Pfad)}],
   "pfade": [{"id": "aue_pfad_<name>", "art": "trampelpfad|serpentine|trittsteine", "breite_cm": 150,
              "punkte_cm": [[x, y], ...], "anschluss": "...", "fuer": ["<ort-id>"], "laenge_m": .., "max_steigung_grad": ..}]}
     (optional, Auftrag 13c; daten.lade() rastert die Pfade ALLER Biome als Wege)

API:
  ort_id(biom, nr, kurz)                      -> "aue_01_blautopf"
  kamera(feld, kx, ky, zx, zy, zz, name, hoch=170)  (cm) -> Liste §8; hoch=-170 = Augenhoehe ohne 3-m-Regel
  standort(id, name, art, x_m, y_m, radius_m, kameras, welt=None, z_m=None, **extra) -> dict
  pfad(id, art, punkte_m, welt=None, breite_cm=150, anschluss="", fuer=None) -> dict ("pfade"-Eintrag)
  schreibe_standorte(pfad, biom, orte, stand=None, pruefen=True, welt=None, pfade=None)
  lade_standorte(pfad), alle_standorte(sehens_ordner) -> Liste (biom, ort, datei), alle_pfade(sehens_ordner)
  belegte_punkte(sehens_ordner, ausser_biom=None) -> Liste dict (x_m, y_m, biom, id) fuer Abstandsregeln
  ort_phase2(standort, **felder) -> Grundgeruest eines orte.json-Eintrags; schreibe_orte(pfad, biom, orte)
  schreibe_f32(pfad, array), schreibe_r8(pfad, array)  (Gelaende-Delta / Bodenlagen, Phase 2)
"""

import datetime
import glob
import json
import os
import re

import numpy as np

from . import log, ascii_text
from . import daten as _daten

ARTEN = ("leuchtfeuer", "fundstueck")


def heute():
    return datetime.date.today().isoformat()


def slug(text):
    t = ascii_text(text).lower()
    t = re.sub(r"[^a-z0-9]+", "_", t).strip("_")
    return t or "ort"


def ort_id(biom, nr, kurz):
    return "%s_%02d_%s" % (biom, int(nr), slug(kurz))


def kamera(feld, kx_cm, ky_cm, zx_cm, zy_cm, zz_cm, name, hoch=170):
    """Kamera nach §8: [Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch] (cm, ganzzahlig)."""
    return [str(feld), int(round(kx_cm)), int(round(ky_cm)), int(round(zx_cm)), int(round(zy_cm)),
            int(round(zz_cm)), str(name), int(round(hoch))]


def kamera_hoehe_cm(welt, kam):
    """Tatsaechliche Kamerahoehe nach §8: Hoch > 0: max(Boden_an_Kamera + Hoch, ZZ + 300);
    Hoch < 0: genau |Hoch| ueber dem Boden (Augenhoehe -170, Stand 11.10. 13:00)."""
    b = welt.hoehe_bei_cm(kam[1], kam[2])
    if kam[7] < 0:
        return b - kam[7]
    return max(b + kam[7], kam[5] + 300)


def _rund(o, nd=1):
    if isinstance(o, float):
        return round(o, nd)
    if isinstance(o, (np.floating,)):
        return round(float(o), nd)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return [_rund(v, nd) for v in o.tolist()]
    if isinstance(o, dict):
        return {k: _rund(v, nd) for k, v in o.items() if not (isinstance(v, np.ndarray) and v.size > 50)}
    if isinstance(o, (list, tuple)):
        return [_rund(v, nd) for v in o]
    return o


def standort(id, name, art, x_m, y_m, radius_m, kameras, welt=None, z_m=None, **extra):
    """Eintrag fuer standorte.json. z_m: Bodenhoehe (aus welt, falls nicht angegeben)."""
    if art not in ARTEN:
        raise ValueError("art muss leuchtfeuer oder fundstueck sein, nicht %r" % art)
    if z_m is None:
        z_m = welt.hoehe_bei_m(x_m, y_m) if welt is not None else 0.0
    e = {"id": id, "name": name, "art": art,
         "mitte_cm": [int(round(x_m * 100)), int(round(y_m * 100)), int(round(z_m * 100))],
         "radius_m": round(float(radius_m), 1),
         "felder": _daten.felder_im_kreis(x_m, y_m, radius_m),
         "kameras": kameras}
    for k, v in extra.items():
        e[k] = _rund(v)
    return e


def _dump(daten_, pfad):
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    txt = json.dumps(daten_, ensure_ascii=False, indent=1)
    # Kameras und Koordinatenlisten kompakt in einer Zeile
    txt = re.sub(r"\[\s+([^\[\]{}]*?)\s+\]", lambda m: "[" + re.sub(r"\s*\n\s*", " ", m.group(1)) + "]", txt)
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(txt + "\n")


def schreibe_standorte(pfad, biom, orte, stand=None, pruefen=True, welt=None, pfade=None, gel=None):
    """Schreibt standorte.json (Phase 1). pfade: Liste aus format.pfad(...) -> Schluessel "pfade"
    (ohne pfade wie bisher). pruefen=True: Pruefer laufen lassen und Befunde loggen."""
    d = {"stand": stand or heute(), "biom": biom, "orte": orte}
    if pfade:
        d["pfade"] = pfade
    _dump(d, pfad)
    log("geschrieben: %s (%d Orte)" % (pfad, len(orte)))
    if pruefen:
        from . import sehens_pruefen as sp
        bef = sp.pruefe_standorte(d, welt=welt, gel=gel)
        sp.melde(bef, titel=os.path.basename(pfad))
    return d


def lade_standorte(pfad):
    with open(pfad, "r", encoding="utf-8") as f:
        return json.load(f)


def alle_standorte(sehens_ordner, mit_varianten=True):
    """Alle Orte aus <sehens_ordner>/*/standorte.json -> Liste (biom, ort, pfad).
    mit_varianten: auch */standorte_*.json (alte Steig-Varianten, z. B. standorte_steige.json) - deren Raeume
    sind reserviert. Keine Doppelzaehlung: Ein Ort, dessen id schon in einer standorte.json steht (z. B. nach
    Uebernahme mit "pfad_id"), wird aus den Varianten nicht noch einmal gezaehlt."""
    out = []
    haupt = sorted(glob.glob(os.path.join(sehens_ordner, "*", "standorte.json")))
    var = sorted(glob.glob(os.path.join(sehens_ordner, "*", "standorte_*.json"))) if mit_varianten else []
    gesehen = set()
    for p in haupt + [q for q in var if q not in haupt]:
        try:
            d = lade_standorte(p)
        except Exception as ex:  # defekte Datei -> melden, weiter
            log("FEHLER beim Lesen %s: %s" % (p, ex))
            continue
        b = d.get("biom") or os.path.basename(os.path.dirname(p))
        ist_var = p not in haupt
        for o in d.get("orte", []):
            oid = o.get("id") if isinstance(o, dict) else None
            if ist_var and oid in gesehen:
                continue
            if oid:
                gesehen.add(oid)
            out.append((b, o, p))
    return out


def alle_pfade(sehens_ordner):
    """Alle Pfade ("pfade" in */standorte.json) -> Liste normierter dicts (id, biom, art, breite_cm,
    punkte_m, fuer, anschluss, quelle). Gleich daten.lade_pfade."""
    return _daten.lade_pfade(sehens_ordner)


def belegte_punkte(sehens_ordner, ausser_biom=None):
    """Bereits geplante Orte anderer Biome (fuer Mindestabstaende): Liste dict(x_m, y_m, biom, id, pfad_id).
    Orte an Pfaden (standorte.json mit "pfad_id") zaehlen wie alle anderen, Varianten ohne Doppelzaehlung."""
    out = []
    for b, o, _ in alle_standorte(sehens_ordner):
        if ausser_biom and b == ausser_biom:
            continue
        m = o.get("mitte_cm")
        if not m:
            continue
        out.append({"x_m": m[0] / 100.0, "y_m": m[1] / 100.0, "biom": b, "id": o.get("id"),
                    "pfad_id": o.get("pfad_id")})
    return out


def pfad(id, art, punkte_m, welt=None, breite_cm=150, anschluss="", fuer=None, **extra):
    """Eintrag fuer standorte.json "pfade" (Auftrag 13c): punkte_cm [[x, y], ...], breite_cm, art,
    anschluss, fuer; mit welt zusaetzlich laenge_m und max_steigung_grad (gelaende.pfad_profil)."""
    if art not in _daten.PFAD_ARTEN:
        raise ValueError("art muss %s sein, nicht %r" % ("/".join(_daten.PFAD_ARTEN), art))
    e = {"id": id, "art": art, "breite_cm": int(round(breite_cm)),
         "punkte_cm": [[int(round(p[0] * 100)), int(round(p[1] * 100))] for p in punkte_m],
         "anschluss": anschluss, "fuer": list(fuer or [])}
    if welt is not None:
        from .gelaende import pfad_profil
        pr = pfad_profil(welt, [[q[0] / 100.0, q[1] / 100.0] for q in e["punkte_cm"]])
        e["laenge_m"] = pr["laenge_m"]
        e["max_steigung_grad"] = pr["max_steigung_grad"]
    for k, v in extra.items():
        e[k] = _rund(v)
    return e


def mindestabstand_m(biom_a, biom_b):
    """350 m; 200 m wenn beide Orte in kleinen Biomen liegen (canyon, sumpf, fjord, kueste, frost)."""
    return 200.0 if (_daten.ist_kleines_biom(biom_a) and _daten.ist_kleines_biom(biom_b)) else 350.0


# --- Phase 2 ----------------------------------------------------------------------------------
def ort_phase2(st, kurz="", standort_begruendung=None, **felder):
    """Grundgeruest eines orte.json-Eintrags (SEHENS_FORMAT §2) aus einem standorte.json-Eintrag."""
    e = {"id": st["id"], "name": st["name"], "art": st["art"], "kurz": kurz,
         "mitte_cm": st["mitte_cm"], "radius_m": st["radius_m"], "felder": st.get("felder", []),
         "standort_begruendung": standort_begruendung or st.get("standort_begruendung", ""),
         "sicht": {"naechster_weg_m": (st.get("sicht") or {}).get("naechster_weg_m"),
                   "sichtbar_ab_m": (st.get("sicht") or {}).get("sichtbar_ab_m", 0)},
         "wasser": [], "effekte": [], "materialwuensche": [], "kameras": st.get("kameras", []),
         "marker": {"titel": st["name"], "text": "", "entdeckung_m": 30},
         "assets_wunsch": [],
         "budget": {"instanzen": 0, "kollision": 0, "akteure": 0, "lichter": 0, "niagara": 0, "decals": 0}}
    e.update({k: _rund(v) for k, v in felder.items()})
    return e


def schreibe_orte(pfad, biom, orte, stand=None, pruefen=True, zusatz=None):
    """zusatz: weitere Schluessel auf oberster Ebene (z. B. material_fix_ausnahmen, E34)."""
    d = {"stand": stand or heute(), "biom": biom, "orte": orte}
    d.update(zusatz or {})
    _dump(d, pfad)
    log("geschrieben: %s (%d Orte)" % (pfad, len(orte)))
    if pruefen:
        from . import sehens_pruefen as sp
        sp.melde(sp.pruefe_orte(d, basis=os.path.dirname(os.path.abspath(pfad))), titel=os.path.basename(pfad))
    return d


def schreibe_f32(pfad, a):
    """Gelaende-Delta (m) als float32 LE zeilenweise (SEHENS_FORMAT §3)."""
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    np.ascontiguousarray(a, dtype="<f4").tofile(pfad)


def schreibe_r8(pfad, a):
    """Bodenlage-Zielgewicht uint8 0..255 zeilenweise (SEHENS_FORMAT §3)."""
    os.makedirs(os.path.dirname(os.path.abspath(pfad)), exist_ok=True)
    np.ascontiguousarray(np.clip(a, 0, 255), dtype=np.uint8).tofile(pfad)


# ============================================================================================
# 13k: Wasserfarben (SEHENS_FORMAT §5 'farbe') - neue Voreinstellung 'bergsee' (Ferat, Nachtrag 11:45, Variante C)
# ============================================================================================
# Format wie Ferats wasserfarben.json (Master M_Eldarien_Wasser_Schaum8): 'absorption' ist je Kanal eine
# ABSORPTIONSLAENGE in cm (das Material gibt 1/Wert je cm als SLW-Koeffizient aus), 'scattering' der Streuwert,
# dazu albedo und rauheit. 8/45/40 cm entspricht 0,125/0,022/0,025 je cm = 12,5/2,2/2,5 je m: Rot ist nach wenigen
# Zentimetern weg, Gruen kommt am weitesten -> dunkles Blaugruen; Streuung 0,06/0,22/0,14 ohne Blau-Ueberhang.
# tiefblau bleibt Ferats bestehende Instanz (nur noch fuer Quelltoepfe).
WASSER_FARBEN = {
    "bergsee": {"master": "M_Eldarien_Wasser_Schaum8", "absorption": [8, 45, 40, 8],
                "scattering": [0.06, 0.22, 0.14, 0.08], "albedo": 0.35, "rauheit": 0.015,
                "einheit_absorption": "cm (Absorptionslaenge je Kanal; Koeffizient = 1/Wert je cm)",
                "je_m": {"absorption_koeff_pro_m": [12.5, 2.22, 2.5]},
                "fuer": "Kar- und Bergseen (13k, Ferat Variante C 'dunkles Blaugruen'); tiefblau nur Quelltoepfe",
                "quelle": "Ferat, Auftrag 13k Nachtrag 11:45, bilder/sehens_p2/pilot2_seefarben.jpg (C)"},
}


def wasser_farben_block(farben):
    """orte.json oben: Werte der im Biom benutzten neuen Voreinstellungen (Format wasserfarben.json)."""
    out = {f: dict(WASSER_FARBEN[f]) for f in sorted(set(farben)) if f in WASSER_FARBEN}
    return out or None
