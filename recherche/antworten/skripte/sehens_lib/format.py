"""format.py - Schreiber fuer standorte.json (Phase 1) und orte.json (Phase 2) nach SEHENS_FORMAT.

Phase 1 - antworten/sehens/<biom>/standorte.json:
  {"stand": "2026-10-11", "biom": "aue", "orte": [{
     "id": "aue_01_blautopf", "name": "Blautopf", "art": "fundstueck" | "leuchtfeuer",
     "mitte_cm": [x, y, z], "radius_m": 45, "felder": ["E5"],
     "kameras": [[Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch], ...],          # SEHENS_FORMAT §8
     "ziel_hoehe_m": 18,                                                # Silhouettenhoehe (Sichtpruefung)
     "standort_begruendung": "...", "sicht": {...}, "erreichbar": {...},
     "pfad_cm": [[x, y, z], ...] (optional), "draufsicht": "aue_01_blautopf.png" (optional)}]}

API:
  ort_id(biom, nr, kurz)                      -> "aue_01_blautopf"
  kamera(feld, kx, ky, zx, zy, zz, name, hoch=170)  (cm) -> Liste §8
  standort(id, name, art, x_m, y_m, radius_m, kameras, welt=None, z_m=None, **extra) -> dict
  schreibe_standorte(pfad, biom, orte, stand=None, pruefen=True)
  lade_standorte(pfad), alle_standorte(sehens_ordner) -> Liste (biom, ort)
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
    """Tatsaechliche Kamerahoehe nach §8: max(Boden_an_Kamera + Hoch, ZZ + 300)."""
    b = welt.hoehe_bei_cm(kam[1], kam[2])
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


def schreibe_standorte(pfad, biom, orte, stand=None, pruefen=True, welt=None):
    """Schreibt standorte.json (Phase 1). pruefen=True: Pruefer laufen lassen und Befunde loggen."""
    d = {"stand": stand or heute(), "biom": biom, "orte": orte}
    _dump(d, pfad)
    log("geschrieben: %s (%d Orte)" % (pfad, len(orte)))
    if pruefen:
        from . import sehens_pruefen as sp
        bef = sp.pruefe_standorte(d, welt=welt)
        sp.melde(bef, titel=os.path.basename(pfad))
    return d


def lade_standorte(pfad):
    with open(pfad, "r", encoding="utf-8") as f:
        return json.load(f)


def alle_standorte(sehens_ordner):
    """Alle Orte aus <sehens_ordner>/*/standorte.json -> Liste (biom, ort, pfad)."""
    out = []
    for p in sorted(glob.glob(os.path.join(sehens_ordner, "*", "standorte.json"))):
        try:
            d = lade_standorte(p)
        except Exception as ex:  # defekte Datei -> melden, weiter
            log("FEHLER beim Lesen %s: %s" % (p, ex))
            continue
        b = d.get("biom") or os.path.basename(os.path.dirname(p))
        for o in d.get("orte", []):
            out.append((b, o, p))
    return out


def belegte_punkte(sehens_ordner, ausser_biom=None):
    """Bereits geplante Orte anderer Biome (fuer Mindestabstaende): Liste dict(x_m, y_m, biom, id)."""
    out = []
    for b, o, _ in alle_standorte(sehens_ordner):
        if ausser_biom and b == ausser_biom:
            continue
        m = o.get("mitte_cm")
        if not m:
            continue
        out.append({"x_m": m[0] / 100.0, "y_m": m[1] / 100.0, "biom": b, "id": o.get("id")})
    return out


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


def schreibe_orte(pfad, biom, orte, stand=None, pruefen=True):
    d = {"stand": stand or heute(), "biom": biom, "orte": orte}
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
