"""inventar.py - Asset-Inventar und Asset-Pruefung fuer Phase 2 (SEHENS_FORMAT §4-§7).

Quellen (vorlagen/daten/, Stand 13b):
  netze.csv               alle Static Meshes (pfad;paket;name;dreiecke;nanite;groesse_x/y/z_m;...)  -> Netze
  netze_masse.json        Bounds min/max in cm fuer 451 Netze (Pivot!)                               -> Pivot/Unterkante
  netz_sperre.json        gesperrte Netze                                                            -> FEHLER
  netz_check_ergebnis.json Materialbefund je Netz (ok / schwarz_mspresets / textur_leer)             -> HINWEIS
  inventar_extra.json     niagara (73), decal_materialien (44), klaenge (Beispiel-Listen), wasser_materialien,
                          blueprints_effekt, eldarien_materialien/-instanzen
  material_parameter.json Parameter der Master (fuer materialwuensche §7)

API:
  inv = Inventar.lade(ordner=None)        # Standard vorlagen/daten
  inv.netz("SM_NordicBoulder_01")         -> dict(pfad, name, paket, nanite, groesse_m (x, y, z), bounds_cm (min, max) | None,
                                                   pivot ("bounds" | "angenommen_unten_mitte"))   (Name oder Pfad; KeyError)
  inv.netz_pruefen(name_oder_pfad, optional=False) -> Liste Befunde (stufe, text)
  inv.niagara_pfad(name_oder_pfad), inv.decal_pfad(...), inv.klang_pfad(...)   -> Pfad oder None
  inv.asset_pruefen(art, name_oder_pfad, optional=False) -> Liste Befunde   (art: netz | niagara | decal | klang)
  inv.material_pruefen(mw)                -> Befunde fuer einen materialwunsch (§7: Master + Parameternamen + fuer)
  houdini(name_oder_pfad)                 -> True fuer Houdini-SW_*-Assets (verboten, Auftrag 13)
Fehlende Assets: FEHLER; mit optional=True nur HINWEIS (SEHENS_FORMAT §6 "optional": true).
"""

import csv
import json
import os
import re

from . import log

FEHLER, WARNUNG, HINWEIS = "FEHLER", "WARNUNG", "HINWEIS"

MASTER_ERLAUBT = ("M_EL_Fels_MS", "M_EL_Fels_Auflage", "M_EL_Fels_Sand", "M_EL_Klippe_RVT", "M_EL_Pflanze",
                  "M_EL_Eis4", "M_EL_Wasserfall2", "M_MS_Decal", "M_MS_Base")


def standard_ordner():
    hier = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(hier, "..", "..", "..", "vorlagen", "daten"))


def houdini(s):
    """Houdini-Sehenswuerdigkeiten (SW_*) sind verboten (Auftrag 13, 'Houdini-Sachen auslassen')."""
    n = str(s).rsplit("/", 1)[-1]
    return bool(re.match(r"^(SM_)?SW_", n)) or "/Houdini" in str(s)


def _letzter(s):
    return str(s).rsplit("/", 1)[-1].split(".")[0]


class Inventar:
    def __init__(self, ordner):
        self.ordner = ordner
        self.netze = {}            # pfad -> dict
        self._name = {}            # name.lower() -> [pfad, ...]
        self.masse = {}
        self.sperre = set()
        self.check = {}
        self.niagara = set()
        self.decals = set()
        self.klaenge = set()
        self.klaenge_anzahl = {}
        self.blueprints = set()
        self.wasser_mat = set()
        self.material_param = {}
        self.stand = ""

    # ------------------------------------------------------------------ Laden
    @classmethod
    def lade(cls, ordner=None):
        ordner = ordner or standard_ordner()
        inv = cls(ordner)
        p = lambda n: os.path.join(ordner, n)
        if not os.path.exists(p("netze.csv")):
            raise FileNotFoundError("Pflichtdatei fehlt: %s" % p("netze.csv"))
        with open(p("netze.csv"), "r", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter=";"):
                try:
                    g = (float(r["groesse_x_m"]), float(r["groesse_y_m"]), float(r["groesse_z_m"]))
                except (TypeError, ValueError):
                    g = (1.0, 1.0, 1.0)
                e = {"pfad": r["pfad"], "name": r["name"] or _letzter(r["pfad"]), "paket": r.get("paket", ""),
                     "nanite": str(r.get("nanite", "0")).strip() in ("1", "true", "True"), "groesse_m": g,
                     "dreiecke": int(float(r.get("dreiecke") or 0))}
                inv.netze[r["pfad"]] = e
                for k in {e["name"].lower(), _letzter(r["pfad"]).lower()}:
                    inv._name.setdefault(k, []).append(r["pfad"])
        if os.path.exists(p("netze_masse.json")):
            with open(p("netze_masse.json"), "r", encoding="utf-8") as f:
                inv.masse = json.load(f)
        if os.path.exists(p("netz_sperre.json")):
            with open(p("netz_sperre.json"), "r", encoding="utf-8") as f:
                d = json.load(f)
            inv.sperre = set(d if isinstance(d, list) else d.get("gesperrt", d.get("netze", [])))
        if os.path.exists(p("netz_check_ergebnis.json")):
            with open(p("netz_check_ergebnis.json"), "r", encoding="utf-8") as f:
                inv.check = json.load(f)
        if os.path.exists(p("inventar_extra.json")):
            with open(p("inventar_extra.json"), "r", encoding="utf-8") as f:
                ex = json.load(f)
            inv.stand = ex.get("stand", "")
            inv.niagara = {str(x).split(".")[0] for x in ex.get("niagara", [])}
            inv.decals = {(x["pfad"] if isinstance(x, dict) else str(x)).split(".")[0]
                          for x in ex.get("decal_materialien", [])}
            for art, v in (ex.get("klaenge") or {}).items():
                inv.klaenge_anzahl[art] = int(v.get("anzahl", 0)) if isinstance(v, dict) else len(v)
                for x in (v.get("beispiele", []) + v.get("alle", [])) if isinstance(v, dict) else v:
                    inv.klaenge.add(str(x).split(".")[0])
            inv.blueprints = {str(x).split(".")[0] for x in ex.get("blueprints_effekt", [])}
            inv.wasser_mat = {str(x).split(".")[0] for x in ex.get("wasser_materialien", [])}
        else:
            log("Hinweis: inventar_extra.json fehlt -> Niagara/Decals/Klaenge nicht pruefbar")
        if os.path.exists(p("material_parameter.json")):
            with open(p("material_parameter.json"), "r", encoding="utf-8") as f:
                for m in json.load(f):
                    inv.material_param[m["name"]] = m
        return inv

    # ------------------------------------------------------------------ Netze
    def netz_pfad(self, s):
        """Name oder Pfad -> Pfad (oder None). Namen ohne Gross/Klein; mehrdeutige Namen -> None."""
        s = str(s).split(".")[0]
        if s in self.netze:
            return s
        k = self._name.get(s.lower())
        if k and len(set(k)) == 1:
            return k[0]
        return None

    def mehrdeutig(self, s):
        k = self._name.get(_letzter(s).lower()) or []
        return len(set(k)) > 1

    def netz(self, s):
        """Netz-Info (KeyError, wenn nicht im Inventar). bounds_cm aus netze_masse.json, sonst Annahme
        Pivot unten Mitte (UE-Standard fuer Megascans/Foliage)."""
        p = self.netz_pfad(s)
        if p is None:
            raise KeyError("Netz nicht im Inventar (netze.csv): %s" % s)
        e = dict(self.netze[p])
        m = self.masse.get(p)
        if m and "min" in m and "max" in m:
            e["bounds_cm"] = (tuple(m["min"]), tuple(m["max"]))
            e["pivot"] = "bounds"
        else:
            gx, gy, gz = (v * 100.0 for v in e["groesse_m"])
            e["bounds_cm"] = ((-gx / 2, -gy / 2, 0.0), (gx / 2, gy / 2, gz))
            e["pivot"] = "angenommen_unten_mitte"
        return e

    def netz_pruefen(self, s, optional=False):
        b = []
        if houdini(s):
            return [(FEHLER, "Houdini-Asset (SW_*) verboten: %s" % s)]
        p = self.netz_pfad(s)
        if p is None:
            if self.mehrdeutig(s):
                return [(FEHLER, "Netzname mehrdeutig, bitte vollen Pfad angeben: %s" % s)]
            return [(HINWEIS if optional else FEHLER, "Netz nicht in netze.csv: %s" % s)]
        if p in self.sperre:
            b.append((FEHLER, "Netz gesperrt (netz_sperre.json): %s" % p))
        c = self.check.get(p)
        if isinstance(c, dict) and c.get("klasse") not in (None, "ok"):
            b.append((HINWEIS, "Materialbefund %s: %s (Material-Fix sw_* noetig)" % (c.get("klasse"), _letzter(p))))
        return b

    # ------------------------------------------------------------------ Extra
    def _suche(self, menge, s):
        s = str(s).split(".")[0]
        if s in menge:
            return s
        t = [x for x in menge if _letzter(x).lower() == _letzter(s).lower()]
        return t[0] if len(t) == 1 else None

    def niagara_pfad(self, s):
        return self._suche(self.niagara, s)

    def decal_pfad(self, s):
        return self._suche(self.decals, s)

    def klang_pfad(self, s):
        return self._suche(self.klaenge, s)

    def blueprint_pfad(self, s):
        return self._suche(self.blueprints, s)

    def asset_pruefen(self, art, s, optional=False):
        """art: netz | niagara | decal | klang | blueprint. Fehlend -> FEHLER (optional -> HINWEIS)."""
        if art == "netz":
            return self.netz_pruefen(s, optional)
        if s is None or s == "":
            return [(HINWEIS if optional else FEHLER, "%s ohne Asset-Pfad" % art)]
        if houdini(s):
            return [(FEHLER, "Houdini-Asset (SW_*) verboten: %s" % s)]
        fn = {"niagara": self.niagara_pfad, "decal": self.decal_pfad, "klang": self.klang_pfad,
              "blueprint": self.blueprint_pfad}[art]
        if fn(s) is not None:
            if art == "klang" and "/City_Nature_Sounds/" in str(s) and re.search(
                    r"Crowd|City|Elevator|Motorcycle|Fireworks|roof|Mall|parade|Street|Traffic|Car_",
                    _letzter(s)):
                return [(FEHLER, "Stadt-/Menschenklang nicht erlaubt (13b: nur Naturklaenge): %s" % s)]
            return []
        if art == "klang" and self.klaenge_anzahl:
            # inventar_extra.json listet nur Beispiele (40 von 316 Waves, 40 von 46 Cues)
            n = sum(self.klaenge_anzahl.values())
            return [(HINWEIS if optional else WARNUNG,
                     "Klang nicht in den Inventar-Beispielen (%d von %d gelistet): %s" % (len(self.klaenge), n, s))]
        return [(HINWEIS if optional else FEHLER, "%s nicht in inventar_extra.json: %s" % (art, s))]

    def material_pruefen(self, mw, alle_namen=False):
        """materialwunsch §7: name MI_EL_SW_*, basis erlaubter Master, Parameter existieren im Master,
        fuer: Netze aus dem Inventar (sonst HINWEIS - Beschreibungen sind erlaubt)."""
        b = []
        n = str(mw.get("name", ""))
        if not n.startswith("MI_EL_SW_"):
            b.append((FEHLER, "materialwunsch.name muss mit MI_EL_SW_ beginnen: %r" % n))
        basis = mw.get("basis")
        if basis not in MASTER_ERLAUBT:
            b.append((FEHLER, "materialwunsch %s: basis %r ist kein erlaubter Master" % (n, basis)))
        m = self.material_param.get(basis)
        if m:
            erlaubt = set((m.get("skalar") or {}).keys()) | set((m.get("vektor") or {}).keys())
            for k, v in (mw.get("parameter") or {}).items():
                if k not in erlaubt:
                    b.append((FEHLER, "materialwunsch %s: Parameter %r gibt es in %s nicht" % (n, k, basis)))
                elif k in (m.get("vektor") or {}) and not (isinstance(v, list) and len(v) in (3, 4)):
                    b.append((FEHLER, "materialwunsch %s: %s ist ein Vektor [r, g, b, a]" % (n, k)))
                elif k in (m.get("skalar") or {}) and not isinstance(v, (int, float)):
                    b.append((FEHLER, "materialwunsch %s: %s ist ein Skalar" % (n, k)))
        elif basis in MASTER_ERLAUBT:
            b.append((HINWEIS, "materialwunsch %s: Parameter von %s nicht pruefbar (material_parameter.json)" % (n, basis)))
        for f in mw.get("fuer") or []:
            if self.netz_pfad(f) is None:
                b.append((HINWEIS, "materialwunsch %s: 'fuer' %r ist kein Netzname (Beschreibung?)" % (n, f)))
        return b
