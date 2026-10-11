# -*- coding: utf-8 -*-
"""gefaelle_regelwerk.py - liest gefaelle_regeln.json (Regelwerk-Agent, Auftrag 15) und rechnet seine Formeln.

Der Planer nimmt ALLE Zahlen aus der Regeln-JSON (Schema: gefaelle_regeln.json["_schema"]). Formeln sind Python-
Ausdruecke mit + - * / **, min, max, sqrt, clamp(x, lo, hi), abs und Vergleichen/'a if b else c'; sie werden hier
ueber einen AST-Pruefer ausgewertet (keine Attribute, keine Indizes, nur erlaubte Namen).

  rw = Regelwerk.lade(pfad)
  rw.zahl(obj, **variablen)            # {'wert'} | {'formel'} | Zahl
  rw.klasse(art, S)                    # Klasse aus klassen.<art> (bach | fluss)
  rw.art_bereich(stufenart)            # (D_min, D_max) aus stufen.arten
  rw.biom(name)                        # biome.<name> (Netze, Lagen, Felstyp) oder Ersatzbiom
"""

import ast
import json
import math
import os

HIER = os.path.dirname(os.path.abspath(__file__))
REGELN_STANDARD = os.path.join(HIER, "gefaelle_regeln.json")

_FUNKTIONEN = {"min": min, "max": max, "sqrt": math.sqrt, "abs": abs, "round": round,
               "clamp": lambda x, lo, hi: min(max(x, lo), hi)}
_ERLAUBT = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name, ast.Load, ast.Call, ast.IfExp,
            ast.Compare, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Gt, ast.GtE,
            ast.Lt, ast.LtE, ast.Eq, ast.NotEq, ast.BoolOp, ast.And, ast.Or)


class RegelFehler(ValueError):
    pass


def formel(text, **var):
    """Wertet eine Regelformel aus (nur erlaubte Knoten und Namen)."""
    t = str(text).strip()
    if "=" in t.split("(")[0] and "==" not in t and not any(o in t.split("(")[0] for o in ("<=", ">=", "!=")):
        t = t.split("=", 1)[1].strip()          # "L_buendel = clamp(...)" -> nur die rechte Seite
    try:
        baum = ast.parse(t, mode="eval")
    except SyntaxError as ex:
        raise RegelFehler("Formel %r: %s" % (text, ex))
    for k in ast.walk(baum):
        if not isinstance(k, _ERLAUBT):
            raise RegelFehler("Formel %r: Ausdruck %s nicht erlaubt" % (text, type(k).__name__))
        if isinstance(k, ast.Name) and k.id not in var and k.id not in _FUNKTIONEN:
            raise RegelFehler("Formel %r: Variable %r fehlt" % (text, k.id))
        if isinstance(k, ast.Call) and not (isinstance(k.func, ast.Name) and k.func.id in _FUNKTIONEN):
            raise RegelFehler("Formel %r: Funktion nicht erlaubt" % text)
    umgebung = dict(_FUNKTIONEN)
    umgebung.update(var)
    return eval(compile(baum, "<regel>", "eval"), {"__builtins__": {}}, umgebung)   # noqa: S307 (AST geprueft)


class Regelwerk:
    # Ersatzbiom, falls ein Biom im Regelwerk fehlt (Felstyp am naechsten)
    ERSATZ = {"sumpf": "aue", "oedland": "bergwald", "wueste": "canyon", "fjord": "bergwald", "frost": "gletscher"}

    def __init__(self, daten, pfad=""):
        self.r = daten
        self.pfad = pfad
        for k in ("klassen", "stufen", "becken", "kolk", "faelle", "klamm", "ufer_klippen", "schutt", "lagen",
                  "effekte", "biome"):
            if k not in daten:
                raise RegelFehler("%s: Abschnitt %r fehlt" % (pfad, k))
        self.version = (daten.get("_schema") or {}).get("version")
        self.stand = (daten.get("_doku") or {}).get("stand")

    @classmethod
    def lade(cls, pfad=None):
        pfad = pfad or REGELN_STANDARD
        if not os.path.exists(pfad):
            raise FileNotFoundError("Regelwerk fehlt: %s" % pfad)
        with open(pfad, "r", encoding="utf-8") as f:
            return cls(json.load(f), pfad)

    # ------------------------------------------------------------------ Zahlen
    def zahl(self, obj, abschnitt=None, **var):
        """obj: Zahl | Formel-Text | {'wert'} | {'formel'}. Fehlende Formel-Variablen werden aus Konstanten
        {'wert': ...} im Objekt selbst oder im Abschnitt daneben ergaenzt (z. B. kolk.v0 fuer kolk.x_strahl)."""
        if isinstance(obj, (int, float)) and not isinstance(obj, bool):
            return float(obj)
        v = dict(var)
        for quelle in (obj if isinstance(obj, dict) else {}, abschnitt or {}):
            for k, w in quelle.items():
                if isinstance(w, dict) and "wert" in w and k not in v and isinstance(w["wert"], (int, float)):
                    v[k] = float(w["wert"])
        if isinstance(obj, str):
            return float(formel(obj, **v))
        if isinstance(obj, dict):
            if "formel" in obj:
                return float(formel(obj["formel"], **v))
            if "wert" in obj:
                return float(obj["wert"])
        raise RegelFehler("keine Zahl: %r" % (obj,))

    def bereich(self, obj):
        return float(obj["min"]), float(obj["max"])

    # ------------------------------------------------------------------ Klassen / Stufen
    def fenster(self, B):
        return self.zahl(self.r["klassen"]["fenster"], B=B)

    def fenster_lokal(self, B):
        return self.zahl(self.r["klassen"]["fenster_lokal"], B=B)

    def art_lauf(self, art_daten, B):
        """'bach' | 'fluss' aus art_regel (B >= 10 m wie Fluss)."""
        try:
            a = formel(self.r["klassen"]["art_regel"]["formel"], B=B)
        except (RegelFehler, KeyError):
            a = art_daten
        return "fluss" if (art_daten == "fluss" or a == "fluss") else "bach"

    def klasse(self, art, S):
        liste = self.r["klassen"][art]
        for k in liste:
            if float(k["von"]) <= S < float(k["bis"]):
                return k
        return liste[-1] if S >= float(liste[-1]["von"]) else liste[0]

    def art_bereich(self, stufenart):
        a = self.r["stufen"]["arten"][stufenart]
        lo = float(a.get("D_min") or 0.0)
        hi = a.get("D_max")
        return lo, (float(hi) if hi is not None else float("inf"))

    def abstand_L(self, S, B):
        return self.zahl(self.r["stufen"]["abstand_L"], S=max(S, 1e-3), B=B)

    def abstand_L_kaskade(self, B):
        return self.zahl(self.r["stufen"]["abstand_L_kaskade"], B=B)

    def becken_gefaelle(self, S):
        b = self.r["becken"]
        g = self.zahl(b["gefaelle_formel"], S=S) if "gefaelle_formel" in b else float(b["gefaelle"]["wert"])
        return min(g, float(b["gefaelle"].get("max", g)))

    def becken_gefaelle_hart(self):
        return float(self.r["becken"]["gefaelle"].get("absolut_max", 0.03))

    def becken_laenge_min(self, B):
        return self.zahl(self.r["becken"]["laenge_min"], B=B)

    def zwei_punkte(self):
        z = self.r["stufen"]["zwei_punkte"]
        return float(z["abstand_ziel"]), float(z["abstand_max"])

    def rampe(self, D):
        a = self.r["stufen"]["arten"]["schnelle"]
        return self.zahl(a["rampe_laenge"], D=D), float(a.get("rampe_gefaelle_max", 0.35))

    def zufall(self):
        z = self.r["stufen"]["zufall"]
        return float(z["L_streuung"]), float(z["D_streuung"])

    def max_stufen_je_100m(self):
        return float(self.r["stufen"]["max_stufen_je_100m"]["wert"])

    def c(self):
        return float(self.r["stufen"]["c"]["wert"])

    # ------------------------------------------------------------------ Lippe
    def lippe_breite(self, B):
        return self.zahl(self.r["stufen"]["lippe"]["breite"], B=B)

    def lippe_pfeil(self):
        return float(self.r["stufen"]["lippe"]["form"]["pfeil"])

    def ueberfall_breite(self, B):
        return self.zahl(self.r["stufen"]["lippe"]["ueberfall_breite"], B=B)

    # ------------------------------------------------------------------ Kolk
    def kolk(self, art, D, S, L, B):
        k = self.r["kolk"]
        c = self.c()
        if art == "fall":
            xs = self.zahl(k["x_strahl"], k, D=D)
            tiefe = self.zahl(k["fall_tiefe"], k, D=D)
            radius = self.zahl(k["fall_radius"], k, B=B, x_strahl=xs, D=D)
            return {"tiefe": tiefe, "laenge": 2.0 * radius, "radius": radius, "x_strahl": xs}
        tiefe = self.zahl(k["stufe_tiefe"], k, c=c, S=S, L=L)
        laenge = self.zahl(k["stufe_laenge"], k, D=D, L=max(L, 3.0))
        return {"tiefe": tiefe, "laenge": laenge, "radius": max(0.6 * B, laenge / 2.0), "x_strahl": 0.0}

    # ------------------------------------------------------------------ Faelle, Klamm, Ufer
    def einzelfall(self):
        e = self.r["faelle"]["einzelfall_statt_kette"]
        return float(e["S_lok_min"]["wert"]), float(e["D_min"]["wert"]), float(e["D_min_bei_fels"]["wert"])

    def _erstes(self, abschnitt, *namen):
        a = self.r[abschnitt]
        for n in namen:
            if n in a:
                return a[n]
        raise RegelFehler("%s: keiner von %s" % (abschnitt, ", ".join(namen)))

    def hoehe_max_einzeln(self):
        return self.zahl(self._erstes("faelle", "hoehe_max_einzeln", "hoehe_max_bach"))

    def kette_glied(self, D_ges, B=4.0):
        return self.zahl(self._erstes("faelle", "kette_glied", "kette_teilung"), self.r["faelle"], D_ges=D_ges, B=B)

    def buendel_L(self, B):
        e = self.r["faelle"]["einzelfall_statt_kette"]
        return self.zahl(e["buendeln"], e, B=B) if "buendeln" in e else max(10.0, 3.0 * B)

    def tritt_laenge(self, B, kolk_radius):
        f = self.r["faelle"]
        return self.zahl(f["tritt_laenge"], f, B=B, kolk_radius=kolk_radius) if "tritt_laenge" in f else 1.5 * B

    def klamm(self):
        return self.r["klamm"]

    def ufer(self):
        return self.r["ufer_klippen"]

    def fels_regel(self):
        """ablauf.fels_anstehend (radius, lage_min, hang_grad, S_fels, Biome) - Standard wie Regelwerk v2."""
        f = (self.r.get("ablauf") or {}).get("fels_anstehend") or {}
        return {"radius": float(f.get("radius", 10)), "lage_min": float(f.get("lage_min", 128)),
                "hang_grad": float(f.get("hang_grad", 45)), "S_fels": float(f.get("S_fels", 0.3)),
                "biome": f.get("biome") or ["bergwald", "gletscher", "frost", "fjord", "canyon", "lava"]}

    # ------------------------------------------------------------------ Biome
    def biom(self, name):
        b = self.r["biome"]
        if name in b:
            return name, b[name]
        e = self.ERSATZ.get(name, "bergwald")
        return e, b[e]
