"""rezept.py - baut einen Ort (SEHENS_FORMAT §2-§9) aus einem Regel-Block ("Rezept") der <biom>_regeln.json.

Ein Biom-Planer liest seine Regeln, ruft fuer jeden Ort  ctx = OrtKontext(...); ctx.baue(hooks)  auf und schreibt
alles mit schreibe_biom(...). Die Regeln beschreiben je Ort (Schema: PLANER_ANLEITUNG.md):
  anker        benannte Punkte (Versatz, Richtung+Abstand, Suche hoechster/tiefster/steilster Punkt, Stufe)
  gelaende     Fenster + Werkzeuge (mulde, kuppe, rinne, terrasse, abbruch, glaetten, buckel) -> gelaende/<id>.f32
  wasser       see (mit Becken-Stempel), bach (Punkte oder automatisch: abfluss_von / zulauf_zu), wasserfall
  gruppen      Instanzen je Detail-Ebene (held, begleiter, schutt, kleinzeug, bewuchs, kontakt, wasser, pfad)
  lagen        Bodenlagen (kreis, ring, band, um_gruppe, ufer, hang) -> lagen/<id>_<Lage>.r8
  pfad         Pfad aus standorte.json ("pfade" mit fuer/pfad_id, sonst pfad_cm des Orts) -> Bodenband + Trittsteine
  effekte      punktlicht, spotlicht, lokaler_nebel, niagara (optional), decal; klaenge (Erweiterung)
  freiraeume   Bestand entfernen (Kreis/Rechteck; Hinweis fuer den Setzer)
  budget, marker, kurz, assets_wunsch
Hooks (Python, optional): {"anker": f(ctx), "nach_gelaende": f(ctx), "gruppen": f(ctx), "ende": f(ctx)} fuer
Formen, die sich nicht als Regel ausdruecken lassen (z. B. Klammwaende entlang des Bachs).

Referenzen auf Punkte ("ref"): "mitte" | "<anker>" | [dx, dy] (m relativ zur Mitte) | {"pos_m": [x, y]} |
{"von": ref, "richtung": rspec, "abstand_m": d} | {"anker": name, "versatz_m": [dx, dy]}
Richtungen ("rspec", Kompassgrad 0 = Nord, 90 = Ost): Zahl | "hangab" | "hangauf" | "zu:<ref>" | "von:<ref>" |
{"basis": rspec, "plus": grad}
"""

import math

import numpy as np

from . import log, ascii_text
from . import daten as _daten
from . import gelaende as _gel
from . import format as _fmt
from . import stempel as _st
from . import instanzen as _ins
from . import inventar as _inv
from . import bach as _bach
from . import steilwand as _sw
from . import kamera_frei as _kf
from . import see_bloecke as _sb

FEHLER, WARNUNG, HINWEIS = "FEHLER", "WARNUNG", "HINWEIS"
BUDGET_9 = {"instanzen": 15000, "kollision": 1500, "akteure": 80, "lichter": 4, "niagara": 3, "nebel": 2,
            "decals": 12}
WITCHER_STUFEN = {"held": (1, 3), "begleiter": (3, 12), "schutt": (20, 400), "kleinzeug": (100, 12000)}


def _zahl(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _bereich(v, rng, standard=None):
    """Zahl oder [a, b] -> Zufallswert (gleichverteilt)."""
    if v is None:
        v = standard
    if v is None:
        return None
    if _zahl(v):
        return float(v)
    return float(rng.uniform(float(v[0]), float(v[1])))


def _anzahl(v, rng):
    if v is None:
        return 0
    if _zahl(v):
        return int(v)
    return int(rng.integers(int(v[0]), int(v[1]) + 1))


class OrtKontext:
    def __init__(self, welt, gel, inv, ebene, standort, regel, biom, seed=0, stand="", pfade_biom=None,
                 paletten=None, materialien=None, orte_mitten=None):
        self.welt, self.gel, self.inv, self.ebene = welt, gel, inv, ebene
        self.st = standort
        self.r = regel or {}
        self.biom = biom
        self.id = standort["id"]
        self.seed = int(seed)
        self.stand = stand
        self.mx, self.my = standort["mitte_cm"][0] / 100.0, standort["mitte_cm"][1] / 100.0
        self.anker = {"mitte": (self.mx, self.my)}
        self.richtungen = {}
        self.stempel = None
        self.lagen = None
        self.gruppen = {}
        self.wasser = []
        self.see = {}               # id -> {"umriss_m", "spiegel_m"}
        self.linien = {}            # benannte Polylinien (Bachlaeufe, Kanten) in m
        self.effekte = []
        self.klaenge = []
        self.pfad = None
        self.freiraeume = []
        self.meldungen = []
        self.paletten = paletten or {}
        self.materialien = {m["name"]: m for m in (materialien or [])}
        self.mat_benutzt = set()
        self.pfade_biom = pfade_biom or []
        self.orte_mitten = dict(orte_mitten or {})     # ort_id -> (x_m, y_m), fuer pfad.abschnitt (geteilte Pfade)
        self.zugang = None                              # pfad.zugang: Fussweg pfad_cm zusaetzlich zum Pfad aus pfade
        self.pfad_abschnitte = []                       # pfad.abschnitte: weitere Abschnitte aus pfade (eigene Baender)
        self._massiv = _ins.Abstandsgitter(4.0)
        self.eintrag = None
        # Bestandswasser, das NICHT in karte_wasser steht (z. B. Epic-Seen wie T_2954_391 im Sumpf): Liste
        # {"id", "umriss_m", "spiegel_m"}; nass ist es nur, wo das Gelaende unter dem Spiegel liegt (Regel
        # "bestandswasser"). Wird nicht als Wasser geschrieben, zaehlt aber fuer im_wasser, ufer, z_bezug spiegel:<id>.
        self.bestand_seen = []
        # E10/E11: Bestandsbach-Abschnitte, die geplantes Wasser ersetzt (orte.json "bestand_ausblenden")
        self.bestand_ausblenden = []
        # 13f: Bachplanung (A4/A8/A9/A12/A13): id -> Linie, Spiegel-Treppe, Stufen, Ziel, Furten, offene Muendung
        self.bach_plan = {}
        self._ausnahmen = []        # Masken im Stempelfenster: Schutz gilt dort nicht (offene Muendung, ersetztes Houdini)
        self._korridore = []        # weiche Gewichte 0..1 der Muendungskorridore (Begrenzung auf 0,5 m am Bestandswasser)
        self.klein_seen = {}        # A13: Seen < 10 m2 -> Lage/Decal statt Epic-See

    # ------------------------------------------------------------------ Meldungen
    def melde(self, stufe, text):
        self.meldungen.append((stufe, self.id, text))
        if stufe != HINWEIS:
            log("%s %s: %s" % (stufe, self.id, ascii_text(text)))

    # ------------------------------------------------------------------ Punkte / Richtungen
    def boden(self, x, y):
        if self.stempel is not None:
            return self.stempel.hoehe_bei_m(x, y)
        r = self.welt.hoehe_bei_m(x, y)
        return r

    def punkt(self, ref):
        if ref is None or ref == "mitte":
            return self.anker["mitte"]
        if isinstance(ref, str):
            if ref in self.anker:
                return self.anker[ref]
            raise KeyError("%s: Anker %r unbekannt" % (self.id, ref))
        if isinstance(ref, (list, tuple)) and len(ref) == 2 and all(_zahl(v) for v in ref):
            return (self.mx + float(ref[0]), self.my + float(ref[1]))
        if isinstance(ref, dict):
            if "pos_m" in ref:
                return (float(ref["pos_m"][0]), float(ref["pos_m"][1]))
            if "von" in ref:
                x, y = self.punkt(ref["von"])
                g = self.richtung(ref.get("richtung", 0.0), ref["von"])
                dx, dy = _st.kompass_vektor(g)
                d = float(ref.get("abstand_m", 0.0))
                return (x + dx * d, y + dy * d)
            if "anker" in ref:
                x, y = self.punkt(ref["anker"])
                v = ref.get("versatz_m", [0, 0])
                return (x + float(v[0]), y + float(v[1]))
            if "auf_linie" in ref:
                P = np.asarray(self.linien[ref["auf_linie"]], np.float64)
                seg = np.hypot(*np.diff(P, axis=0).T)
                kum = np.concatenate([[0], np.cumsum(seg)])
                sd = float(ref.get("t", 0.5)) * kum[-1] if "t" in ref else float(ref.get("s_m", 0.0))
                k = int(np.clip(np.searchsorted(kum, sd, side="right") - 1, 0, len(seg) - 1))
                f = (sd - kum[k]) / max(seg[k], 1e-9)
                x, y = P[k] + (P[k + 1] - P[k]) * f
                if ref.get("seite_m"):
                    tx, ty = (P[k + 1] - P[k]) / max(seg[k], 1e-9)
                    x, y = x + ty * float(ref["seite_m"]), y - tx * float(ref["seite_m"])   # + = links
                return (float(x), float(y))
        raise ValueError("%s: Punkt-Referenz %r unverstaendlich" % (self.id, ref))

    def richtung(self, spec, bei="mitte"):
        if _zahl(spec):
            return float(spec) % 360.0
        if isinstance(spec, dict):
            return (self.richtung(spec.get("basis", 0.0), spec.get("bei", bei)) + float(spec.get("plus", 0.0))) % 360.0
        if isinstance(spec, str):
            if spec in self.richtungen:
                return self.richtungen[spec]
            x, y = self.punkt(bei)
            if spec in ("hangab", "hangauf"):
                g = self._hangab(x, y, 8.0)
                return g if spec == "hangab" else (g + 180.0) % 360.0
            if spec.startswith("zu:") or spec.startswith("von:"):
                zx, zy = self.punkt(spec.split(":", 1)[1])
                g = _st.vektor_kompass(zx - x, zy - y)
                return g if spec.startswith("zu:") else (g + 180.0) % 360.0
        raise ValueError("%s: Richtung %r unverstaendlich" % (self.id, spec))

    def _hangab_welt(self, x, y, r):
        f = self.welt.hoehe_bei_m
        dzx = f(x + r, y) - f(x - r, y)
        dzy = f(x, y + r) - f(x, y - r)
        return _st.vektor_kompass(-dzx, -dzy)

    def _hangab(self, x, y, r):
        s = float(r)
        f = self.boden
        dzx = f(x + s, y) - f(x - s, y)
        dzy = f(x, y + s) - f(x, y - s)
        return _st.vektor_kompass(-dzx, -dzy)

    # ------------------------------------------------------------------ Anker
    def anker_aufloesen(self):
        for name, spec in (self.r.get("anker") or {}).items():
            if isinstance(spec, dict) and "suche" in spec:
                self.anker[name] = self._suche(spec)
            elif isinstance(spec, dict) and "richtung_von" in spec:
                self.richtungen[name] = self.richtung(spec["richtung_von"], spec.get("bei", "mitte"))
            else:
                self.anker[name] = self.punkt(spec)
        self.linien_aufloesen()
        for name, spec in (self.r.get("anker_danach") or {}).items():
            if isinstance(spec, dict) and "suche" in spec:
                self.anker[name] = self._suche(spec)
            else:
                self.anker[name] = self.punkt(spec)

    def linien_aufloesen(self):
        """Benannte Polylinien: {"punkte": [ref, ...]} | {"abwaerts_von": ref, "laenge_m": L} (steilster Abstieg) |
        {"quer": ref, "richtung": rspec, "laenge_m": L} (Strecke quer, Mitte = ref)."""
        for name, spec in (self.r.get("linien") or {}).items():
            if "punkte" in spec:
                self.linien[name] = self.linie(spec["punkte"])
            elif "abwaerts_von" in spec:
                x, y = self.punkt(spec["abwaerts_von"])
                self.linien[name] = _vereinfachen(self._abwaerts(x, y, float(spec.get("laenge_m", 30.0)),
                                                                 stop_wasser=spec.get("stop_wasser", False)), 0.8)
            elif "quer" in spec:
                x, y = self.punkt(spec["quer"])
                g = self.richtung(spec.get("richtung", 0.0), spec["quer"])
                dx, dy = _st.kompass_vektor(g)
                h = float(spec.get("laenge_m", 8.0)) / 2.0
                self.linien[name] = [[x - dx * h, y - dy * h], [x + dx * h, y + dy * h]]
            else:
                self.melde(FEHLER, "linie %s: punkte, abwaerts_von oder quer fehlt" % name)
                continue
            P = self.linien[name]
            self.anker[name + "_anfang"] = tuple(P[0])
            self.anker[name + "_ende"] = tuple(P[-1])
            if len(P) >= 2:
                self.richtungen[name] = _st.vektor_kompass(P[-1][0] - P[0][0], P[-1][1] - P[0][1])

    def _suche(self, spec):
        x, y = self.punkt(spec.get("bei", "mitte"))
        r = spec.get("r_m", 15.0)
        r = float(r) if _zahl(r) else float(r[1])
        art = spec["suche"]
        if art == "hangauf_bis":
            # vom Punkt hangauf gehen, bis das Gelaende hoehe_m ueber dem Start liegt (oder max_m)
            z0 = float(self.welt.hoehe_bei_m(x, y))
            L = 0.0
            while L < float(spec.get("max_m", 40.0)):
                g = (self._hangab_welt(x, y, 3.0) + 180.0) % 360.0
                dx, dy = _st.kompass_vektor(g)
                x, y = x + dx, y + dy
                L += 1.0
                if self.welt.hoehe_bei_m(x, y) >= z0 + float(spec.get("hoehe_m", 10.0)):
                    break
            return (float(x), float(y))
        if art == "rinne":
            # groesste Einzugsflaeche im Ring r_m [a, b] (optional Sektor [g0, g1] Kompass)
            a, b = (0.0, r) if _zahl(spec.get("r_m", r)) else spec["r_m"]
            fe = self.welt.fenster(x, y, b)
            X, Y = fe.gitter_m()
            d = np.hypot(X - x, Y - y)
            m = (d >= a) & (d <= b)
            if spec.get("sektor"):
                g0, g1 = spec["sektor"]
                gg = (np.degrees(np.arctan2(X - x, -(Y - y))) % 360.0)
                m &= ((gg - g0) % 360.0) <= ((g1 - g0) % 360.0)
            if spec.get("ohne_wasser", True):
                m &= fe.get("wasser") == 0
            acc = np.where(m, fe.get(self.gel.akkumulation), -1.0)
            k = int(np.argmax(acc))
            i, j = np.unravel_index(k, acc.shape)
            return (float(X[i, j]), float(Y[i, j]))
        fe = self.welt.fenster(x, y, r)
        X, Y = fe.gitter_m()
        h = fe.get("hoehe").astype(np.float64)
        innen = np.hypot(X - x, Y - y) <= r
        if art == "hoechster":
            w = np.where(innen, h, -np.inf)
        elif art == "tiefster":
            w = np.where(innen, -h, -np.inf)
        elif art == "steilster":
            w = np.where(innen, _gel.hangneigung(h, self.welt.zelle_m), -np.inf)
        elif art == "flachster":
            w = np.where(innen, -_gel.hangneigung(h, self.welt.zelle_m), -np.inf)
        else:
            raise ValueError("suche %r" % art)
        k = int(np.argmax(w))
        i, j = np.unravel_index(k, w.shape)
        return (float(X[i, j]), float(Y[i, j]))

    # ------------------------------------------------------------------ Gelaende
    def gelaende_bauen(self, hooks=None):
        g = self.r.get("gelaende") or {}
        fm = g.get("fenster_m") or [2 * (self.st["radius_m"] + 25)] * 2
        fx, fy = self.punkt(g.get("bei", "mitte"))
        self.stempel = _st.Stempel(self.welt, fx - fm[1] / 2.0, fy - fm[0] / 2.0, fx + fm[1] / 2.0, fy + fm[0] / 2.0,
                                   rand_m=float(g.get("rand_m", 8.0)), seed=self.seed)
        st = self.stempel
        for op in g.get("ops") or []:
            o = op["op"]
            modus = op.get("modus", "add")
            if o in ("mulde", "kuppe", "terrasse", "glaetten", "buckel"):
                x, y = self.punkt(op.get("bei", "mitte"))
                stg = tuple(op.get("streckung", (1.0, 1.0)))
                rg = self.richtung(op.get("richtung", 0.0), op.get("bei", "mitte"))
                if o == "mulde":
                    st.mulde(x, y, op["radius_m"], op.get("tiefe_m", 1.0), op.get("rand_m", 6.0), op.get("boden", 0.4),
                             stg, rg, modus, ziel_z=self._z_spec(op.get("ziel_z"), x, y))
                elif o == "kuppe":
                    st.kuppe(x, y, op["radius_m"], op["hoehe_m"], op.get("rand_m", 6.0), op.get("plateau", 0.2),
                             stg, rg, modus)
                elif o == "terrasse":
                    st.terrasse(x, y, op["radius_m"], self._z_spec(op.get("ziel_z", "boden"), x, y),
                                op.get("rand_m", 6.0), stg, rg, op.get("modus", "setzen"))
                elif o == "glaetten":
                    st.glaetten(x, y, op["radius_m"], op.get("staerke", 1.0), op.get("sigma_m", 3.0),
                                op.get("rand_m", 4.0))
                else:
                    st.buckel(x, y, op["radius_m"], op["amplitude_m"], op.get("wellenlaenge_m", 8.0),
                              op.get("rand_m", 6.0), stg, rg)
            elif o in ("rinne", "abbruch"):
                pts = self.linie(op["punkte"])
                if o == "rinne":
                    sohle = None
                    if op.get("sohle"):
                        z0 = self._z_spec(op["sohle"][0], *pts[0])
                        z1 = self._z_spec(op["sohle"][1], *pts[-1])
                        sohle = (z0, z1)
                    st.rinne(pts, op["breite_m"], op.get("tiefe_m", 1.0), op.get("rand_m", 3.0), sohle, modus)
                else:
                    st.abbruch(pts, op["hoehe_m"], op.get("breite_m", 4.0), op.get("reichweite_m", 25.0),
                               op.get("seite", "links"), op.get("verteilung", "oben"), modus)
            else:
                self.melde(FEHLER, "gelaende.op %r unbekannt" % o)
        # Seebecken (Wasser mit "becken")
        for w in self.r.get("wasser") or []:
            if w.get("typ") == "see":
                self._see_becken(w)
        if hooks and hooks.get("nach_gelaende"):
            hooks["nach_gelaende"](self)
        # Baeche (Linien, Enden, Spiegel-Treppe, Querprofil) vor dem Abschluss (13f A4/A8/A9/A12/A13)
        self._ist_wasser_maske = None
        if g.get("ist_wasser"):
            self._ist_wasser_maske = np.hypot(st.X - self.mx, st.Y - self.my) <= float(
                g.get("ist_wasser_r_m", self.st["radius_m"]))
        delta_vor_bach = st.delta.copy()
        for w in self.r.get("wasser") or []:
            if w.get("typ") == "bach":
                self._bach_linie(w)
        # 13h: Bachprofil ausserhalb von Netzrand + Uferring hoechstens tiefe + 0,5 m eintiefen (keine Keilwaende)
        n_k = _sw.bach_einschnitt_begrenzen(self, delta_vor_bach)
        if n_k > 0:
            self.melde(HINWEIS, "Bachprofil (13h): Einschnitt ausserhalb Netzrand + Uferring auf %.0f m2 begrenzt" % n_k)
        ausnahme = self._ausnahme_maske(wasser_ausnahmen=True)
        st.fertig(schutz=g.get("schutz", True), weg_m=float(g.get("schutz_weg_m", 3.0)),
                  wasser=not g.get("wasser_frei", False), ausnahme_maske=ausnahme,
                  wasser_maske=self._wasser_maske_fenster(st.fe),
                  senken_fuellen=g.get("senken_fuellen", True))
        if self._korridore and g.get("schutz", True) and not g.get("wasser_frei", False):
            # Muendungskorridor (Koordinator 13f): am Bestandswasser (Wasserschutz-Zone) hoechstens 0,5 m, weich
            fw = st.schutz_faktor(float(g.get("schutz_weg_m", 3.0)), True, 4.0, self._ist_wasser_maske, nur_wasser=True)
            c = np.zeros(st.delta.shape)
            for k_ in self._korridore:
                c = np.maximum(c, k_)
            fweg = st.schutz_faktor(float(g.get("schutz_weg_m", 3.0)), False, 4.0, None)
            st.delta = fweg * (st.delta * fw + (1.0 - fw) * c * np.clip(st.delta, -0.5, 0.5))
            st.delta[np.abs(st.delta) < 0.005] = 0.0
            st.max_aenderung_m = float(np.abs(st.delta).max()) if st.delta.size else 0.0
        # 13h: neue Steilflaechen flacher (Halde) - ausser gewollten, verkleideten Waenden (steil_erlaubt)
        _sw.boeschung_anwenden(self)
        if st.gefuellt_m2 > 0:
            self.melde(HINWEIS, "kleine Senken aufgefuellt (A5): %.0f m2, bis %.2f m angehoben"
                       % (st.gefuellt_m2, st.gefuellt_max_m))
        if g.get("begruendung"):
            st.begruendung = g["begruendung"]
        st.ist_wasser = bool(g.get("ist_wasser"))
        if st.max_aenderung_m > 40.0 and not g.get("begruendung"):
            self.melde(WARNUNG, "Gelaende |Delta| %.1f m > 40 m ohne 'begruendung' (Ferat erlaubt mehr, aber begruenden)"
                       % st.max_aenderung_m)
        sk = st.senken(wasser=self._wasser_maske_fenster(st.fe))
        if sk["flaeche_m2"] > 0:
            # "senke_begruendung" (optional): gewollte Hohlform ohne Wasser (Gaskrater, Schluckloch, Endpfanne) -> HINWEIS
            sb = g.get("senke_begruendung")
            self.melde(HINWEIS if sb else WARNUNG, "geschlossene Senke ohne Wasser/Abfluss: %.0f m2, bis %.1f m tief%s"
                       % (sk["flaeche_m2"], sk["max_tiefe_m"], (" - gewollt: %s" % sb) if sb else ""))

    def _z_spec(self, spec, x, y):
        """Hoehenangabe: Zahl (absolut m) | 'boden' | 'boden+1.5' | 'boden-2' | 'see:<id>' | 'see:<id>+0.5'."""
        if spec is None:
            return None
        if _zahl(spec):
            return float(spec)
        s = str(spec)
        basis, plus = s, 0.0
        for zeichen in ("+", "-"):
            if zeichen in s[1:]:
                k = s.rfind(zeichen)
                basis, plus = s[:k], float(s[k:])
                break
        if basis == "boden":
            return float(self.boden(x, y)) + plus
        if basis.startswith("see:"):
            return self.see[basis[4:]]["spiegel_m"] + plus
        raise ValueError("%s: Hoehenangabe %r" % (self.id, spec))

    def linie(self, refs):
        if isinstance(refs, str):
            return [list(p) for p in self.linien[refs]]
        return [list(self.punkt(r)) for r in refs]

    def _see_einpassen(self, x, y, a_m, b_m, tiefe, freibord, ep):
        """Sucht Mitte (Raster 3 m im Radius r_such_m), Richtung und Spiegel mit dem kleinsten Erdbau:
        Kosten = max(Abtrag ueber dem Spiegel innen, Auftrag fuer das Ufer aussen) + 0,2 x Mittel."""
        rs = float(ep.get("r_such_m", 10.0))
        schritt = float(ep.get("schritt_m", 3.0))
        richtungen = ep.get("richtungen") or list(range(0, 180, 15))
        t = np.linspace(0, 2 * np.pi, 24, endpoint=False)
        rr = np.array([0.0, 0.35, 0.65, 0.9])
        best = None
        for ox in np.arange(-rs, rs + 0.1, schritt):
            for oy in np.arange(-rs, rs + 0.1, schritt):
                if ox * ox + oy * oy > rs * rs:
                    continue
                cx, cy = x + ox, y + oy
                for g in richtungen:
                    ux, uy = _st.kompass_vektor(g)
                    ca, sa = np.cos(t)[None, :], np.sin(t)[None, :]
                    pa, pb = rr[:, None] * a_m * ca, rr[:, None] * b_m * sa
                    zi = np.asarray(self.boden(cx + pa * ux - pb * uy, cy + pa * uy + pb * ux)).ravel()
                    k = 1.0 + 3.0 / max(min(a_m, b_m), 1.0)
                    qa, qb = k * a_m * np.cos(t), k * b_m * np.sin(t)
                    zr = np.asarray(self.boden(cx + qa * ux - qb * uy, cy + qa * uy + qb * ux))
                    for sp in np.unique(np.round(np.quantile(np.concatenate([zi, zr]), np.linspace(0.05, 0.6, 10)), 2)):
                        ab = np.maximum(zi - (sp - 0.3), 0.0)
                        auf = np.maximum(sp + freibord - zr, 0.0)
                        c = max(ab.max(), auf.max()) + 0.2 * (ab.mean() + auf.mean())
                        if best is None or c < best[0]:
                            best = (c, cx, cy, g, float(sp))
        return best

    def _see_becken(self, w):
        x, y = self.punkt(w.get("bei", "mitte"))
        b = w.get("becken") or {}
        a_m = float(b.get("a_m", w.get("r_m", 5.0)))
        b_m = float(b.get("b_m", a_m))
        rg = self.richtung(b.get("richtung", 0.0), w.get("bei", "mitte"))
        spiegel = self._z_spec(w.get("spiegel", "boden"), x, y)
        if math.pi * a_m * b_m < float(w.get("klein_unter_m2", 10.0)):
            self._klein_see(w, x, y, a_m, b_m, rg, spiegel)
            return
        if b.get("einpassen"):
            best = self._see_einpassen(x, y, a_m, b_m, float(w.get("tiefe_m", 2.0)), float(b.get("freibord_m", 0.5)),
                                       b["einpassen"] if isinstance(b["einpassen"], dict) else {})
            if best:
                _, x, y, rg, spiegel = best
                self.melde(HINWEIS, "see %s eingepasst: Mitte (%.0f, %.0f), Richtung %.0f, Spiegel %.2f m, Erdbau max ~%.1f m"
                           % (w["id"], x, y, rg, spiegel, best[0]))
        if w.get("spiegel_rand_min"):
            # Spiegel = tiefster Punkt des Umrisses (vor dem Becken) - nur so hoch wie das Gelaende es hergibt
            t = np.linspace(0, 2 * np.pi, 36, endpoint=False)
            ux, uy = _st.kompass_vektor(rg)
            px = x + a_m * np.cos(t) * ux - b_m * np.sin(t) * uy
            py = y + a_m * np.cos(t) * uy + b_m * np.sin(t) * ux
            spiegel = float(np.min(self.boden(px, py))) + float(w.get("spiegel_rand_min"))
        auslass = b.get("auslass", "auto")
        aus_g = None
        if auslass == "auto":
            # Abfluss = tiefster Punkt 3 m hinter der Uferlinie (vor dem Becken)
            t = np.linspace(0, 2 * np.pi, 72, endpoint=False)
            ux, uy = _st.kompass_vektor(rg)
            pa, pb = (a_m + 3.0) * np.cos(t), (b_m + 3.0) * np.sin(t)
            px, py = x + pa * ux - pb * uy, y + pa * uy + pb * ux
            k = int(np.argmin(np.asarray(self.boden(px, py))))
            aus_g = _st.vektor_kompass(px[k] - x, py[k] - y)
        elif _zahl(auslass):
            aus_g = float(auslass)
        um = self.stempel.see_becken(x, y, a_m, b_m, rg, spiegel, float(w.get("tiefe_m", 2.0)),
                                     ufer_m=float(b.get("ufer_m", 6.0)), freibord_m=float(b.get("freibord_m", 0.5)),
                                     boden=float(b.get("boden", 0.45)), auslass_grad=aus_g,
                                     auslass_sektor_grad=float(b.get("auslass_sektor_grad", 30.0)),
                                     lippe_m=float(b.get("lippe_m", 1.5)))
        self.see[w["id"]] = {"umriss_m": um, "spiegel_m": spiegel, "x": x, "y": y, "a_m": a_m, "b_m": b_m,
                             "richtung": rg, "auslass_grad": aus_g, "lippe_m": float(b.get("lippe_m", 1.5)),
                             "ufer_m": float(b.get("ufer_m", 6.0))}
        self.linien["ufer_" + w["id"]] = um + [um[0]]
        ins = b.get("insel")
        if ins:
            # 13h: Felsinsel als Gelaendekuppe im Becken - Krone >= ueber_m ueber dem Spiegel (nichts unter Wasser)
            ux, uy = _st.kompass_vektor(rg)
            dx, dy = (ins.get("versatz_m") or [0.0, 0.0])
            ix, iy = x + dx, y + dy
            ziel = spiegel + float(ins.get("ueber_m", 0.6))
            hb = float(self.stempel.hoehe_bei_m(ix, iy))
            if ziel > hb:
                self.stempel.kuppe(ix, iy, float(ins.get("r_m", 4.0)), ziel - hb, rand_m=float(ins.get("rand_m", 2.5)),
                                   plateau=float(ins.get("plateau", 0.35)), modus="max")
            self.see[w["id"]]["insel"] = {"x": ix, "y": iy, "r_m": float(ins.get("r_m", 4.0)), "krone_m": ziel}
            self.anker[w["id"] + "_insel"] = (ix, iy)
        # Auto-Anker: <id>_mitte, <id>_auslass (Uferpunkt in Abflussrichtung, 3 m nach aussen)
        self.anker[w["id"] + "_mitte"] = (x, y)
        U = np.asarray(um)
        if aus_g is not None:
            gg = np.array([_st.vektor_kompass(p_[0] - x, p_[1] - y) for p_ in U])
            k = int(np.argmin(np.abs((gg - aus_g + 180.0) % 360.0 - 180.0)))
        else:
            k = int(np.argmin(np.asarray(self.welt.hoehe_bei_m(U[:, 0], U[:, 1]))))
        self.see[w["id"]]["auslass_m"] = [float(U[k, 0]), float(U[k, 1])]
        v = U[k] - [x, y]
        n = max(float(np.hypot(*v)), 1e-6)
        self.anker[w["id"] + "_auslass"] = (float(U[k, 0] + v[0] / n * 3.0), float(U[k, 1] + v[1] / n * 3.0))
        self.richtungen[w["id"] + "_auslass"] = _st.vektor_kompass(v[0], v[1])

    def _klein_see(self, w, x, y, a_m, b_m, rg, spiegel):
        """13f A13: Seen < 10 m2 trianguliert Epic-Wasser schlecht -> Bodenlage (Standard Schlamm) und optional ein
        Decal statt eines Epic-Sees; kein Becken (sonst geschlossene Senke). Regel "klein": {"lage", "wert",
        "decal", "decal_groesse_m"}. Der See bleibt als Anker/Maske bekannt (im_wasser, ufer), wird aber nicht als
        Wasser geschrieben."""
        k = w.get("klein") or {}
        t = np.linspace(0, 2 * np.pi, 16, endpoint=False)
        ux, uy = _st.kompass_vektor(rg)
        pa, pb = a_m * np.cos(t), b_m * np.sin(t)
        um = [[float(x + p * ux - q * uy), float(y + p * uy + q * ux)] for p, q in zip(pa, pb)]
        if _st.flaeche(um) < 0:
            um = um[::-1]
        self.see[w["id"]] = {"umriss_m": um, "spiegel_m": float(spiegel), "x": x, "y": y, "a_m": a_m, "b_m": b_m,
                             "richtung": rg, "auslass_grad": None, "klein": True}
        self.anker[w["id"] + "_mitte"] = (x, y)
        self.anker[w["id"] + "_auslass"] = (x, y)
        self.klein_seen[w["id"]] = {"x": x, "y": y, "r_m": max(a_m, b_m)}
        lage = k.get("lage", "Schlamm")
        if lage:
            self.r.setdefault("lagen", []).append({"lage": lage, "form": "kreis", "bei": {"pos_m": [x, y]},
                                                    "r_m": round(max(a_m, b_m) + 0.5, 2), "wert": k.get("wert", 230),
                                                    "rand_m": 3.0, "flecken": 0.2})
        if k.get("decal"):
            g = float(max(a_m, b_m) * 2.2)
            self.r.setdefault("effekte", []).append(
                {"typ": "decal", "material": k["decal"], "bei": {"pos_m": [x, y]},
                 "groesse_m": k.get("decal_groesse_m", [0.6, round(g, 2), round(g, 2)]),
                 "zweck": "Nassflaeche statt Kleinst-See %s (< 10 m2, A13)" % w["id"],
                 "optional": bool(k.get("optional", False))})
        self.melde(HINWEIS, "see %s: %.1f m2 < 10 m2 -> Lage %s%s statt Epic-See (A13)"
                   % (w["id"], math.pi * a_m * b_m, lage, (" + Decal %s" % k["decal"]) if k.get("decal") else ""))

    def _abwaerts(self, x, y, max_m, schritt_m=2.0, stop_wasser=True, z_start=None, ziel_see=None, vorher=None,
                  richtung0=None, anstieg_m=0.05, abstand_m=1.0):
        """Steilster Abstieg auf dem (gestempelten) Gelaende -> Polylinie [[x, y], ...]. Geplante Seen (mit Puffer)
        werden umgangen - ausser ziel_see: erreicht der Abstieg dessen Puffer, endet er dort."""
        pts = [[x, y]]
        zc = self.boden(x, y) if z_start is None else z_start
        L = 0.0
        winkel = np.radians(np.arange(0, 360, 15))
        letzte = None if richtung0 is None else math.radians(float(richtung0))
        alt = [list(map(float, q[:2])) for q in (vorher or [])]
        while L < max_m:
            kx = x + schritt_m * np.sin(winkel)
            ky = y - schritt_m * np.cos(winkel)
            kz = np.asarray(self.boden(kx, ky))
            if letzte is not None:   # nicht zurueck
                ok = np.cos(winkel - letzte) > -0.2
                kz = np.where(ok, kz, np.inf)
            if len(pts) + len(alt) > 2:
                # 13f: nie neben den eigenen Lauf zurueck (Kehre/Schleife) - Abstand zu allen frueheren Punkten
                Pa = np.asarray(alt + pts[:-1], np.float64)
                dmin = np.min(np.hypot(kx[:, None] - Pa[None, :, 0], ky[:, None] - Pa[None, :, 1]), axis=1)
                kz = np.where(dmin < 0.9 * schritt_m + abstand_m, np.inf, kz)
            if self.see:
                # 13f A4: ein Bach laeuft nicht zurueck in ein geplantes Seebecken und nicht am Ufer entlang (Puffer
                # 2 Zellen + 1 m um den Umriss) - der Abfluss fuehrt vom Auslass weg
                for sid_, sv in self.see.items():
                    if sv.get("klein"):
                        continue
                    drin = self._im_see_puffer(kx, ky, sv)
                    if sid_ == ziel_see and drin.any():
                        # Zielsee erreicht: hinein, solange der Lauf nicht schon unter dessen Spiegel liegt (der
                        # Uferring ist hoeher als das Gelaende - deshalb nicht nach der Hoehe des Nachbarn fragen)
                        kz_z = np.where(drin, kz, np.inf)
                        kk = int(np.argmin(kz_z))
                        if np.isfinite(kz_z[kk]) and (kz_z[kk] <= zc + 0.5 or zc >= float(sv["spiegel_m"]) - 0.1):
                            pts.append([float(kx[kk]), float(ky[kk])])
                            return pts
                    kz = np.where(drin, np.inf, kz)
                    if sid_ != ziel_see:
                        # im Uferring des Sees (Puffer + Ringbreite): nur vom See weg, nicht am Ufer/Damm entlang
                        ring = self._see_puffer_m() + max(float(sv.get("ufer_m", 4.0)), 2.5 * self.welt.zelle_m + 2.5)
                        if bool(self._im_see_puffer(np.array([x]), np.array([y]), sv, ring)[0]):
                            r_jetzt = math.hypot(x - sv["x"], y - sv["y"])
                            r_kand = np.hypot(kx - sv["x"], ky - sv["y"])
                            kz = np.where(r_kand < r_jetzt + 0.5 * schritt_m, np.inf, kz)
            k = int(np.argmin(kz))
            if not np.isfinite(kz[k]):
                break
            if kz[k] > zc + anstieg_m and len(pts) > 2:
                break
            x, y, zc = float(kx[k]), float(ky[k]), min(zc, float(kz[k]))
            letzte = winkel[k]
            pts.append([x, y])
            L += schritt_m
            if stop_wasser and L > 6.0:
                # A9: nur Epic-Gewaesser (baeche_alle, wasser_welt, teiche) beenden den Lauf - Houdini-Raster nicht
                if _bach.epic_ziele(self.welt).bei(x, y, 0.5) is not None:
                    break
        return pts

    def _ausnahme_maske(self, wasser_ausnahmen=True):
        """Maske im Stempelfenster, in der der Wasserschutz (3 m an Bestandswasser) nicht gilt: Ort IST das Wasser
        (gelaende.ist_wasser) und offene Muendungen der Baeche in Bestandswasser (13f A13)."""
        m = None
        if self._ist_wasser_maske is not None:
            m = self._ist_wasser_maske.copy()
        if wasser_ausnahmen:
            for a in self._ausnahmen:
                m = a.copy() if m is None else (m | a)
        return m

    def _see_puffer_m(self):
        return 2.0 * self.welt.zelle_m + 1.0

    def _im_see_puffer(self, x, y, sv, puffer_m=None):
        """True innerhalb des (um puffer_m nach aussen vergroesserten) Seeumrisses."""
        pb = self._see_puffer_m() if puffer_m is None else float(puffer_m)
        U = np.asarray(sv["umriss_m"], np.float64)
        c = np.array([sv["x"], sv["y"]])
        v = U - c
        n = np.maximum(np.hypot(v[:, 0], v[:, 1]), 1e-6)
        return _in_polygon(x, y, U + v / n[:, None] * pb)

    def _bach_linie(self, w):
        """Linie, Enden (A4/A9/A13), Spiegel-Treppe (A8) und Querprofil (A12) eines Bachs -> self.bach_plan[id]."""
        wid = w.get("id", "bach%d" % len(self.bach_plan))
        B = float(w.get("breite_m", 1.5))
        tiefe = float(w.get("tiefe_cm", 30)) / 100.0
        start_see = w.get("abfluss_von")
        mu = w.get("muendung")
        end_see = w.get("bis_see") or (mu if isinstance(mu, str) and mu in self.see else None)
        if end_see and end_see not in self.see:
            self.melde(FEHLER, "bach %s: bis_see %r unbekannt" % (wid, end_see))
            end_see = None
        if start_see and start_see not in self.see:
            self.melde(FEHLER, "bach %s: abfluss_von %r unbekannt" % (wid, start_see))
            return
        if start_see and self.see[start_see].get("klein"):
            start_see = None
        if end_see and self.see[end_see].get("klein"):
            end_see = None
        epic = _bach.epic_ziele(self.welt)
        hinweise = []
        if "punkte" in w:
            pts = self.linie(w["punkte"])
        elif start_see:
            s = self.see[start_see]
            um = np.asarray(s["umriss_m"])
            if s.get("auslass_m"):
                k = int(np.argmin(np.hypot(um[:, 0] - s["auslass_m"][0], um[:, 1] - s["auslass_m"][1])))
            else:
                k = int(np.argmin(np.asarray(self.boden(um[:, 0], um[:, 1]))))
            # A4: Abfluss beginnt am Auslass (auf dem Umriss), dann nach aussen weiter abwaerts
            vx, vy = um[k, 0] - s["x"], um[k, 1] - s["y"]
            n = max(math.hypot(vx, vy), 1e-6)
            aus_m = self._see_puffer_m() + 0.5
            sx, sy = um[k, 0] + vx / n * aus_m, um[k, 1] + vy / n * aus_m
            vor = [[float(um[k, 0] + vx / n * t_), float(um[k, 1] + vy / n * t_)] for t_ in np.arange(0.0, aus_m - 0.4, 1.0)]
            pts = [[float(um[k, 0]), float(um[k, 1])]] + self._abwaerts(
                sx, sy, float(w.get("laenge_m", 60.0)), vorher=vor, richtung0=_st.vektor_kompass(vx, vy),
                ziel_see=end_see)
        elif "von" in w:
            x, y = self.punkt(w["von"])
            pts = self._abwaerts(x, y, float(w.get("laenge_m", 60.0)), ziel_see=end_see)
        else:
            self.melde(FEHLER, "bach %s: punkte, von oder abfluss_von fehlt" % wid)
            return
        if "punkte" not in w and not end_see and _st.polylinie_laenge(pts) < float(w.get("laenge_m", 60.0)) - 2.0:
            # A9: steilster Abstieg stockt an einer Gegensteigung -> weiter entlang der Tiefenlinie (D8, gefuellt)
            pts = self._verlaengern(pts, float(w.get("laenge_m", 60.0)) - _st.polylinie_laenge(pts), epic=epic,
                                    r=0.5 * B + _bach.ZIEL_SUCHE_M)
        pts = [list(map(float, p[:2])) for p in pts]
        if start_see and "punkte" in w:
            # A4: erster Punkt auf den Umriss (Auslass) setzen
            bp, _ = _bach.naechster_umrisspunkt(self.see[start_see]["umriss_m"], *pts[0])
            pts[0] = list(bp)
        # ---- Ende (A4/A9/A13)
        ziel = None
        if end_see:
            um = self.see[end_see]["umriss_m"]
            hit = _bach.schnitt_polygon(pts, um) if len(pts) > 1 else None
            if hit is not None and hit[0] == 0 and bool(_in_polygon(pts[0][0], pts[0][1], um)):
                self.melde(WARNUNG, "bach %s: beginnt im Zielsee %s" % (wid, end_see))
            elif hit is not None:
                # A4: am Seeumriss abschneiden, Endpunkt auf dem Umriss
                k, q = hit
                pts = pts[:k + 1] + [list(q)]
            else:
                bp, d = _bach.naechster_umrisspunkt(um, *pts[-1])
                if d > 0.3:
                    hinweise.append("bis ans Ufer von %s verlaengert (%.1f m)" % (end_see, d))
                    pts.append(list(bp))
                else:
                    pts[-1] = list(bp)
            ziel = {"art": "see_eigen", "id": end_see, "spiegel_m": float(self.see[end_see]["spiegel_m"])}
        else:
            ziel = self._bach_ziel(w, wid, pts, B, epic, hinweise, start_see)
            pts = ziel.pop("_pts")
        n_alt = ziel.pop("_n_alt", None)
        if n_alt and 2 <= n_alt < len(pts):
            # Koordinator 13f / Ferat 13g: zu kurz versickernder Lauf verlaengert - der bisherige Lauf bleibt Punkt fuer
            # Punkt wie in 13f (eigene Vereinfachung), nur die Verlaengerung kommt dazu
            a_ = pts[:n_alt]
            pa = _verdichten(_vereinfachen(a_, 0.5 if len(a_) < 6 else 1.0), float(w.get("max_segment_m", 2.0)))
            pb = _verdichten(_vereinfachen(pts[n_alt - 1:], 1.0), float(w.get("max_segment_m", 2.0)))
            pts = pa + pb[1:]
        else:
            pts = _verdichten(_vereinfachen(pts, 0.5 if len(pts) < 6 else 1.0), float(w.get("max_segment_m", 2.0)))
        if "punkte" not in w:
            # keine Schleife: kommt der Lauf an ein frueheres Stueck (Kehre in flachem Gelaende), endet er dort
            n0 = len(pts)
            pts = _ohne_schleife(pts, 2.0 * _bach.halbe_breite_eff(B, self.welt.zelle_m) + 1.5)
            if len(pts) < n0:
                hinweise.append("Schleife abgeschnitten nach %.0f m" % _st.polylinie_laenge(pts))
                if ziel.get("art") not in ("versickert", "see_eigen", "houdini"):
                    ziel = {"art": "versickert", "id": "versickert"}
                L_ = _st.polylinie_laenge(pts)
                if ziel.get("art") == "versickert" and L_ < _bach.VERSICKERT_MIN_M:
                    # Koordinator 13f: zu kurz versickernd -> ab der Kappung ohne Kehre weiter (>= 25 m)
                    p2 = self._verlaengern_sinnvoll(pts, _bach.VERSICKERT_MIN_M - L_ + 1.0)
                    p2 = pts + _verdichten(_vereinfachen(p2[len(pts) - 1:], 1.0), float(w.get("max_segment_m", 2.0)))[1:]
                    if _st.polylinie_laenge(p2) > L_ + 0.5:
                        pts = p2
                        hinweise.append("versickert: ab der Kappung auf %.0f m verlaengert (A9)" % _st.polylinie_laenge(pts))
        # ---- im Stempelfenster halten (Rand: Delta laeuft auf 0 aus)
        x0, y0, x1, y1 = self.stempel.fe.grenzen_m()
        rr = max(self.stempel.rand_m, 8.0) + 2.0 * self.welt.zelle_m + _bach.halbe_breite_eff(B, self.welt.zelle_m)
        P = np.asarray(pts)
        aus = (P[:, 0] < x0 + rr) | (P[:, 0] > x1 - rr) | (P[:, 1] < y0 + rr) | (P[:, 1] > y1 - rr)
        if aus.any():
            k = int(np.argmax(aus))
            if k < 2:
                self.melde(FEHLER, "bach %s: beginnt am Rand des Gelaendefensters (fenster_m vergroessern)" % wid)
                return
            hinweise.append("am Gelaendefenster gekappt nach %.0f m (Rest ausserhalb)" % _st.polylinie_laenge(pts[:k]))
            pts = pts[:k]
            if ziel.get("art") == "houdini":
                pass                # endet im Houdini-Lauf, der dort weiterlaeuft
            else:
                if ziel.get("art") not in ("versickert",):
                    self.melde(WARNUNG, "bach %s: Muendung %s ausserhalb des Gelaendefensters - endet 'versickert' am "
                                        "Fensterrand (fenster_m vergroessern)" % (wid, ziel.get("id")))
                ziel = {"art": "versickert", "id": "versickert"}
        if ziel.get("art") in ("bach", "fluss", "see", "teich") and ziel.get("id"):
            # Zielspiegel am endgueltigen Endpunkt (die Linie wurde gekappt/verdichtet; Fluesse haben Gefaelle)
            sp_ = epic.spiegel(ziel["id"], *pts[-1])
            if sp_ is not None:
                ziel["spiegel_m"] = float(sp_)
        self.linien["bach_" + wid] = pts
        if w.get("rinne"):
            rn = w["rinne"]
            z0 = float(self.boden(*pts[0])) - float(rn.get("tiefe_m", 0.4))
            z1 = float(self.boden(*pts[-1])) - float(rn.get("tiefe_m", 0.4))
            self.stempel.rinne(pts, float(rn.get("breite_m", w.get("breite_m", 2.0))), 0.0,
                               float(rn.get("rand_m", 2.0)), sohle_z=(z0, min(z0, z1)))
        # ---- Spiegel-Treppe (A8) auf dem bisher gestempelten Gelaende
        ds = 0.5
        sa, xa, ya = _bach.abtasten(pts, ds)
        g = np.asarray(self.boden(xa, ya), np.float64)
        # Ufer beidseits (Pruefstelle): der Uferring hebt hoechstens WULST_MAX_M - liegt eine Seite tiefer (Bach am
        # Hang), muss der Spiegel so tief liegen, dass das Ufer dort noch >= Spiegel + 0,15 m werden kann
        du = _bach.ufer_abstand(B, self.welt.zelle_m)
        tx = np.gradient(xa)
        ty = np.gradient(ya)
        tn = np.maximum(np.hypot(tx, ty), 1e-9)
        nx_, ny_ = ty / tn, -tx / tn
        g_l = np.asarray(self.boden(xa + nx_ * du, ya + ny_ * du), np.float64)
        g_r = np.asarray(self.boden(xa - nx_ * du, ya - ny_ * du), np.float64)
        # Spiegelplanung mit den Werten von 13f (Ferat 13g: Stufen unveraendert); die Reserve wirkt nur im Stempel
        g_eff = np.minimum(g, np.minimum(g_l, g_r) + _bach.PLAN_WULST_MAX_M - _bach.PLAN_RING_UEBER_M - 0.05 +
                           _bach.EINBETTUNG_M)
        g_eff = np.maximum(g_eff, g - 2.0)      # hoechstens 2 m tiefer als die Mitte (Bach am Abbruch: Pruefer meldet)
        if start_see or end_see:
            # am eigenen See (Auslass-Lippe, Muendung) bestimmt der See den Spiegel
            for sid_ in (start_see, end_see):
                if sid_:
                    nahe = self._im_see_puffer(xa, ya, self.see[sid_], self._see_puffer_m() + 1.0)
                    g_eff = np.where(nahe, g, g_eff)
        W0 = float(self.see[start_see]["spiegel_m"]) if start_see else None
        # Furten/Schutz (A13): wo der Weg-/Ortsschutz den Stempel aufhebt, laeuft das Wasser flach ueber den Boden
        fs = self._schutz_faktor_bei(xa, ya)
        furt = fs < 0.98
        boden_arr = np.where(furt, g + 0.03, -np.inf)
        W_boden = None
        if ziel.get("spiegel_m") is not None and ziel["art"] != "see_eigen":
            W_boden = float(ziel["spiegel_m"]) + _bach.MUENDUNG_SEE_M
        boden_arr = np.maximum(boden_arr, W_boden if W_boden is not None else -np.inf)
        boden_arr = np.maximum.accumulate(boden_arr[::-1])[::-1]      # Spiegel davor nie tiefer
        W_ende = float(ziel["spiegel_m"]) + _bach.MUENDUNG_SEE_M if ziel["art"] == "see_eigen" else None
        if W0 is not None and W_boden is not None and W_boden > W0:
            # 13i K4: ein Abfluss beginnt immer auf dem Seespiegel - Ziel ueber W0 wird verworfen (versickert)
            self.melde(WARNUNG, "bach %s: Zielgewaesser %s liegt %.2f m ueber dem Seespiegel - verworfen, versickert"
                       % (wid, ziel["id"], W_boden - W0))
            ziel = {"art": "versickert", "id": "versickert"}
            W_boden = None
            boden_arr = np.where(furt, g + 0.03, -np.inf)
            boden_arr = np.maximum.accumulate(boden_arr[::-1])[::-1]
        # Abfluss: die Seelippe bleibt auf dem Seespiegel (erste Stufe erst hinter der Lippe)
        lippe = max(float(self.see[start_see].get("lippe_m", 1.5)), 2.0 * self.welt.zelle_m + 0.5) + 1.0 \
            if start_see else 0.0
        W, stufen = _bach.treppe(sa, g_eff, B, W0=W0, W_boden=None, W_ende=W_ende, start_fest=start_see is not None,
                                 boden_arr=boden_arr, flach_bis_m=lippe)
        stufen = _bach.stufen_zusammenfassen(stufen)
        fmax = _bach.fall_max()
        for e in stufen:
            if e["fall_m"] > fmax:
                self.melde(WARNUNG, "bach %s: Stufe %.1f m > %.0f m (Regelwerk faelle.hoehe_max_einzeln)" % (wid, e["fall_m"], fmax))
        # ---- offene Muendung in Bestandswasser (A13): Wasserschutz gilt im Muendungskorridor nicht
        offen_s = None
        if ziel["art"] in ("bach", "fluss", "see", "teich"):
            L = float(sa[-1])
            offen_s = max(L - 8.0, 0.0)
            kk = sa >= offen_s
            Pm = np.stack([xa[kk], ya[kk]], 1)
            if len(Pm) >= 2:
                d, _, _ = _st.polylinie_abstand(self.stempel.X, self.stempel.Y, Pm)
                # Koordinator 13f: im Muendungskorridor darf das Gelaende am Bestandswasser hoechstens 0,5 m
                # geaendert werden, weich auslaufend (Kern halbe Breite + 1 m, Auslauf 2 m), nie in Weg-/Ortszonen
                he_ = _bach.halbe_breite_eff(B, self.welt.zelle_m)
                self._ausnahmen.append(d <= he_ + 3.0)
                self._korridore.append(1.0 - _st.glatt01((d - (he_ + 1.0)) / 2.0))
        if w.get("im_bestand_stempeln"):
            # 13f/13g: der Bach IST das unbenannte Bestandsgerinne (Houdini-Raster ohne Epic-Namen) - der Wasserschutz
            # gilt in seinem eigenen Korridor (halbe Breite + 3 m) nicht, das Bett wird dort gestempelt (Spiegel und
            # Stufen unveraendert)
            Pm = np.stack([xa, ya], 1)
            d, _, _ = _st.polylinie_abstand(self.stempel.X, self.stempel.Y, Pm)
            self._ausnahmen.append(d <= _bach.halbe_breite_eff(B, self.welt.zelle_m) + 3.0)
        # ---- Querprofil (A12)
        if w.get("profil", True):
            X_, Y_ = self.stempel.X, self.stempel.Y
            ring_aus = np.zeros(X_.shape, bool)
            tief_aus = np.zeros(X_.shape, bool)
            he = _bach.halbe_breite_eff(B, self.welt.zelle_m)
            for sid, sv in self.see.items():
                if sv.get("klein"):
                    continue
                ring_aus |= _in_polygon(X_, Y_, sv["umriss_m"])
                # Seebecken und Uferring nicht anschneiden: fremde Seen ganz, der eigene Zu-/Abfluss-See ausser im
                # Muendungs-/Auslasskorridor (erste bzw. letzte 6 m des Bachs, halbe Breite + 1 m)
                zone = self._im_see_puffer(X_, Y_, sv, 3.0 + 2.0 * self.welt.zelle_m)
                if sid in (start_see, end_see):
                    L_ = float(sa[-1])
                    stueck = _bach.linien_stueck(np.stack([xa, ya], 1), 0.0, 6.0) if sid == start_see else \
                        _bach.linien_stueck(np.stack([xa, ya], 1), L_ - 6.0, L_)
                    dk, _, _ = _st.polylinie_abstand(X_, Y_, stueck)
                    zone &= dk > he + 1.0
                tief_aus |= zone
            if offen_s is not None:
                ring_aus |= self.stempel.fe.get("wasser") > 0
            self.stempel.bach_profil(np.stack([xa, ya], 1), sa, W, B, tiefe, ring_aus=ring_aus,
                                     tiefe_max_m=float(np.max(g - W)) + tiefe, tief_aus=tief_aus,
                                     name="bach_profil_%s" % wid)
        furten = []
        if furt.any():
            k = 0
            while k < len(furt):
                if furt[k]:
                    j = k
                    while j + 1 < len(furt) and furt[j + 1]:
                        j += 1
                    furten.append((float(sa[k]), float(sa[j])))
                    k = j + 1
                else:
                    k += 1
            hinweise.append("%d Furt(en) im Weg-/Ortsschutz (Wasser flach ueber dem Boden)" % len(furten))
        self.anker["bach_%s_anfang" % wid] = (float(pts[0][0]), float(pts[0][1]))
        self.anker["bach_%s_ende" % wid] = (float(pts[-1][0]), float(pts[-1][1]))
        self.bach_plan[wid] = {"pts": pts, "s": sa, "x": xa, "y": ya, "W": W, "stufen": stufen, "ziel": ziel,
                               "B": B, "tiefe": tiefe, "start_see": start_see, "end_see": end_see, "furten": furten,
                               "offen_s": offen_s, "g_vor": g}
        for h in hinweise:
            self.melde(HINWEIS, "bach %s: %s" % (wid, h))

    def _schutz_faktor_bei(self, x, y):
        """Schutzfaktor (0 = Weg-/Ortsschutz hebt den Stempel auf, 1 = frei) an Weltpunkten."""
        f = self.stempel.schutz_faktor(wasser=False)
        return _st._bilinear_fenster(f, self.stempel.fe, self.welt, x, y, 1.0)

    def _bach_ziel(self, w, wid, pts, B, epic, hinweise, start_see):
        """Muendung eines Bachs ohne eigenen Zielsee (A9/A13): explizite Epic-Kennung, Houdini-Netz (muendung_houdini),
        'versickert' (>= 25 m) oder automatisch: Epic-Gewaesser am Ende, sonst entlang der Tiefenlinie weiter."""
        mu = w.get("muendung")
        r = 0.5 * B + _bach.ZIEL_SUCHE_M
        W0 = float(self.see[start_see]["spiegel_m"]) if start_see else float(self.boden(*pts[0]))

        def laenge(p):
            return _st.polylinie_laenge(p)

        if w.get("muendung_houdini"):
            # explizit: Bach geht in einen sichtbaren Houdini-Wasserlauf ueber (Name, oder true = Name lokal zuordnen);
            # die Linie endet im ersten Houdini-Wasser (karte_wasser) nach 3 m, sonst nach laenge_m
            hid = w["muendung_houdini"] if isinstance(w["muendung_houdini"], str) else "houdini"
            if w.get("houdini_kappen", True) and not isinstance(w["muendung_houdini"], str):
                kum = _bach.bogen(pts)
                for k in range(1, len(pts)):
                    i, j = self.welt.m_zu_ij(pts[k][0], pts[k][1])
                    if kum[k] > 3.0 and self.welt.wasser[i, j] > 0:
                        pts = pts[:k + 1]
                        break
            return {"art": "houdini", "id": hid, "_pts": pts}
        if isinstance(mu, str) and mu not in ("auto", "versickert", "suesswasser_bestand") and mu not in self.see:
            if epic.kennt(mu):
                # Koordinator 13f: erste Stelle am Ziel, an der dessen Spiegel erreichbar ist (nicht ueber dem Gelaende
                # des Laufs bzw. dem Anfang) - dort enden; sonst entlang der Tiefenlinie weiter suchen
                p2 = self._verlaengern(pts, float(w.get("verlaengern_m", 40.0)), epic=None, robust=True)
                for k in range(1, len(p2)):
                    zk = epic.bei(p2[k][0], p2[k][1], r)
                    if zk is None or zk["id"] != mu:
                        continue
                    if zk["spiegel_m"] + _bach.MUENDUNG_SEE_M <= min(W0, float(self.boden(*p2[k])) + 0.3):
                        if k + 1 < len(pts):
                            hinweise.append("an %s angeschlossen nach %.0f m" % (mu, _st.polylinie_laenge(p2[:k + 1])))
                        elif k + 1 > len(pts):
                            hinweise.append("bis %s verlaengert (+%.0f m)" % (mu, _st.polylinie_laenge(p2[:k + 1])
                                                                            - _st.polylinie_laenge(pts)))
                        pts = p2[:k + 1]
                        break
                else:
                    # 13i K4: unerreichbares Ziel verwerfen (Tiefenlinie bzw. versickert >= 25 m), nie den Lauf heben
                    hinweise.append("Muendung %s nicht erreichbar (Spiegel ueber dem Lauf) - Ziel verworfen, "
                                    "automatisch gesucht (13i K4)" % mu)
                    mu = "auto"
                if mu != "auto":
                    sp = epic.spiegel(mu, *pts[-1])
                    return {"art": "bach", "id": mu, "spiegel_m": sp, "_pts": pts}
            self.melde(WARNUNG, "bach %s: Muendung %r ist kein Epic-Gewaesser (A9) - automatisch gesucht" % (wid, mu))
            mu = "auto"
        if mu == "versickert":
            n_alt = None
            if laenge(pts) < _bach.VERSICKERT_MIN_M:
                pts = self._verlaengern(pts, _bach.VERSICKERT_MIN_M - laenge(pts) + 1.0, epic=None)
                if laenge(pts) < _bach.VERSICKERT_MIN_M:
                    # Koordinator 13f: noch zu kurz -> ab dem Ende von 13f ohne Kehre weiter (Lauf davor unveraendert)
                    n_alt = len(pts)
                    pts = self._verlaengern_sinnvoll(pts, _bach.VERSICKERT_MIN_M - laenge(pts) + 1.0)
                hinweise.append("versickert: auf %.0f m verlaengert (>= 25 m, A9)" % laenge(pts))
            return {"art": "versickert", "id": "versickert", "_pts": pts, "_n_alt": n_alt}
        # auto (A9): Epic-Gewaesser am Ende? sonst weiter entlang der Tiefenlinie
        z = epic.bei(pts[-1][0], pts[-1][1], r)
        if z is not None and z["spiegel_m"] + _bach.MUENDUNG_SEE_M > W0:
            hinweise.append("Epic-Gewaesser %s am Ende liegt hoeher (%.2f m > Anfang %.2f m) - keine Muendung"
                            % (z["id"], z["spiegel_m"], W0))
            z = None
        if z is None:
            mehr = float(w.get("verlaengern_m", 40.0))
            p2 = self._verlaengern(pts, mehr, epic=epic, r=r, W0=W0)
            z2 = epic.bei(p2[-1][0], p2[-1][1], r)
            if z2 is not None and z2["spiegel_m"] + _bach.MUENDUNG_SEE_M <= W0:
                hinweise.append("bis %s verlaengert (+%.0f m, A9)" % (z2["id"], laenge(p2) - laenge(pts)))
                pts, z = p2, z2
            else:
                n_alt = None
                if laenge(pts) < _bach.VERSICKERT_MIN_M:
                    if laenge(p2) >= _bach.VERSICKERT_MIN_M:
                        pts = p2
                    else:
                        pts = self._verlaengern(pts, _bach.VERSICKERT_MIN_M - laenge(pts) + 1.0, epic=None)
                        if laenge(pts) < _bach.VERSICKERT_MIN_M:
                            n_alt = len(pts)
                            pts = self._verlaengern_sinnvoll(pts, _bach.VERSICKERT_MIN_M - laenge(pts) + 1.0)
                    hinweise.append("versickert: auf %.0f m verlaengert (>= 25 m, A9)" % laenge(pts))
                if laenge(pts) < _bach.VERSICKERT_MIN_M:
                    self.melde(WARNUNG, "bach %s: versickert nach %.0f m (< 25 m, Gelaende steigt)" % (wid, laenge(pts)))
                return {"art": "versickert", "id": "versickert", "_pts": pts, "_n_alt": n_alt}
        # Linie am Zielgewaesser enden lassen (erster Punkt im Wasser, nicht weit hinein)
        for k in range(1, len(pts)):
            zk = epic.bei(pts[k][0], pts[k][1], 0.0)
            if zk is not None and zk["id"] == z["id"]:
                pts = pts[:k + 1]
                break
        return {"art": z["art"], "id": z["id"], "spiegel_m": float(z["spiegel_m"]), "_pts": pts}

    def _tiefenlinie(self, x, y, max_m):
        """A9: Tiefenlinie ab (x, y) - D8-Abfluss auf dem gefuellten Weltgelaende (Gelaende.empfaenger), d. h. auch
        ueber kleine Gegensteigungen hinweg. Rueckgabe Polylinie [[x, y], ...] (ohne Startpunkt)."""
        rec = self.gel.empfaenger
        i, j = self.welt.m_zu_ij(x, y)
        k = int(i) * self.welt.nx + int(j)
        out, L = [], 0.0
        px, py = x, y
        while L < max_m:
            k = int(rec[k])
            if k < 0:
                break
            qx, qy = self.welt.flat_zu_m(k)
            qx, qy = float(qx), float(qy)
            L += math.hypot(qx - px, qy - py)
            out.append([qx, qy])
            px, py = qx, qy
        return out

    def _verlaengern_sinnvoll(self, pts, mehr_m):
        """Koordinator 13f: zu kurz versickernder Lauf ohne Kehre weiter - nur, wenn die Verlaengerung nicht bergauf in
        Gelaende fuehrt, das der Stempel nicht freilegen darf (Gegenanstieg <= 0,5 m ueber dem bisherigen Ende, ausserhalb
        der Weg-/Ortsschutzzone); sonst bleibt der Lauf wie 13f."""
        p2 = self._verlaengern(pts, mehr_m, epic=None, robust=True)
        if len(p2) <= len(pts):
            return pts
        neu = np.asarray(p2[len(pts):], np.float64)
        z_ende = float(self.boden(*pts[-1]))
        if float(np.max(self.boden(neu[:, 0], neu[:, 1]))) > z_ende + 0.5:
            return pts
        if float(np.min(self._schutz_faktor_bei(neu[:, 0], neu[:, 1]))) < 0.98:
            return pts
        for sv in self.see.values():
            if not sv.get("klein") and self._im_see_puffer(neu[:, 0], neu[:, 1], sv, 3.0 + 2.0 * self.welt.zelle_m).any():
                return pts          # liefe zurueck an einen geplanten See (Uferring/Becken wird nicht angeschnitten)
        g = self.r.get("gelaende") or {}
        if g.get("schutz", True) and not g.get("wasser_frei", False):
            fw = self.stempel.schutz_faktor(float(g.get("schutz_weg_m", 3.0)), True, 4.0,
                                            self._ausnahme_maske(wasser_ausnahmen=True), nur_wasser=True)
            if float(np.min(_st._bilinear_fenster(fw, self.stempel.fe, self.welt, neu[:, 0], neu[:, 1], 1.0))) < 0.98:
                return pts          # liefe in den Wasserschutz des Bestands (dort kein Stempel)
        return p2

    def _verlaengern(self, pts, mehr_m, epic=None, r=3.0, W0=None, robust=False):
        """Linie entlang der Tiefenlinie um bis mehr_m verlaengern (A9): erst steilster Abstieg auf dem gestempelten
        Gelaende, wo der stockt, D8-Tiefenlinie der Welt; stoppt an Epic-Gewaessern."""
        if mehr_m <= 0.5:
            return pts
        x, y = pts[-1]
        if not robust:
            # wie 13f (Stufen der bestehenden Baeche unveraendert, Ferat 13g)
            neu = self._abwaerts(x, y, mehr_m, stop_wasser=False)[1:]
            Ln = _st.polylinie_laenge([[x, y]] + neu) if neu else 0.0
            if Ln < mehr_m - 1.0:
                ax, ay = (neu[-1] if neu else (x, y))
                neu += self._tiefenlinie(ax, ay, mehr_m - Ln)
            return self._verlaengern_anhaengen(pts, neu, mehr_m, epic, r, W0)
        # robust (Koordinator 13f, nur fuer zu kurz versickernde Baeche und explizite Epic-Muendungen): nie neben den
        # eigenen Lauf zurueck (Abstand 3,3 m), aus kleinen Mulden heraus, Tiefenlinie ohne Kehre
        neu = self._abwaerts(x, y, mehr_m, stop_wasser=False, vorher=pts[:-1], abstand_m=1.5)[1:]
        Ln = _st.polylinie_laenge([[x, y]] + neu) if neu else 0.0
        if Ln < mehr_m - 1.0:
            # aus kleinen Mulden heraus: Abstieg mit erlaubtem Gegenanstieg (0,5 m), nie neben den eigenen Lauf;
            # erst danach die D8-Tiefenlinie der Welt
            ax, ay = (neu[-1] if neu else (x, y))
            weiter = self._abwaerts(ax, ay, mehr_m - Ln, stop_wasser=False, vorher=pts + neu[:-1], anstieg_m=0.5,
                                    abstand_m=1.5)[1:]
            neu += weiter
            Ln = _st.polylinie_laenge([[x, y]] + neu) if neu else 0.0
        if Ln < mehr_m - 1.0:
            ax, ay = (neu[-1] if neu else (x, y))
            alle = [list(map(float, q_[:2])) for q_ in pts + neu]
            kum_ = list(_bach.bogen(np.asarray(alle, np.float64)))
            for q in self._tiefenlinie(ax, ay, mehr_m - Ln):
                sq = kum_[-1] + math.hypot(q[0] - alle[-1][0], q[1] - alle[-1][1])
                A_ = np.asarray(alle, np.float64)[np.asarray(kum_) < sq - 6.0]   # fruehere Stuecke, nicht die letzten 6 m
                if len(A_) and np.min(np.hypot(A_[:, 0] - q[0], A_[:, 1] - q[1])) < 3.3:
                    break           # Tiefenlinie laeuft zurueck an den eigenen Lauf (Kehre)
                neu.append(q)
                alle.append([float(q[0]), float(q[1])])
                kum_.append(sq)
        return self._verlaengern_anhaengen(pts, neu, mehr_m, epic, r, W0, robust=True)

    def _verlaengern_anhaengen(self, pts, neu, mehr_m, epic, r, W0, robust=False):
        out = [list(p) for p in pts]
        for p in neu:
            out.append([float(p[0]), float(p[1])])
            if epic is not None:
                z = epic.bei(p[0], p[1], r)
                if z is not None and (W0 is None or z["spiegel_m"] + _bach.MUENDUNG_SEE_M <= W0):
                    break
            if _st.polylinie_laenge(out) - _st.polylinie_laenge(pts) >= mehr_m:
                break
        if robust:
            # bisheriger Lauf Punkt fuer Punkt unveraendert (Ferat 13g), nur die Verlaengerung vereinfacht
            return [list(p) for p in pts] + _vereinfachen(out[len(pts) - 1:], 0.3)[1:]
        return _vereinfachen(out, 0.3)

    # ------------------------------------------------------------------ Wasser (§5)
    def wasser_bauen(self):
        n0 = len(self.wasser)
        self._wasser_bauen()
        regeln = [w for w in (self.r.get("wasser") or []) if w.get("typ") in ("see", "bach", "wasserfall")]
        nach_id = {w.get("id"): w for w in regeln}
        for e in self.wasser[n0:]:
            w = nach_id.get(e.get("id"), {})
            for k in ("material_hinweis", "hinweis_wasser"):     # z. B. Mountain-Fluss-/Wasserfall-Material (13d)
                if w.get(k):
                    e[k] = w[k]
            if w.get("ersetzt_bestandsbach"):
                e["ersetzt_bestandsbach"] = w["ersetzt_bestandsbach"].get("id")
        # E10/E11: "ersetzt_bestandsbach" an einem Wasser-Eintrag oder auf Ortsebene -> bestand_ausblenden
        quellen = [(w.get("id"), w["ersetzt_bestandsbach"]) for w in regeln if w.get("ersetzt_bestandsbach")]
        quellen += [(x.get("ersetzt_durch"), x) for x in _liste(self.r.get("ersetzt_bestandsbach") or [])]
        for wid, eb in quellen:
            self._bestand_ausblenden(wid, eb)
        # 13f B: Houdini-Wassernetze (nicht Epic) im neuen Wasser ausblenden -> bestand_ausblenden art 'houdini'
        for h in _liste(self.r.get("houdini_ausblenden") or []):
            self._houdini_ausblenden(h)

    def _houdini_ausblenden(self, h):
        """{"netz": "<Houdini-Netz>", "see": id | "bach": id | "bei": ref + "r_m", "puffer_m", "breite_m", "grund"}
        -> {"art": "houdini", "netz", "umriss_cm" (gegen den Uhrzeigersinn), "ersetzt_durch", "grund"}."""
        netz = h.get("netz")
        um = None
        if h.get("see") and h["see"] in self.see:
            U = np.asarray(self.see[h["see"]]["umriss_m"], np.float64)
            c = U.mean(axis=0)
            v = U - c
            n = np.maximum(np.hypot(v[:, 0], v[:, 1]), 1e-6)
            um = (U + v / n[:, None] * float(h.get("puffer_m", 2.0))).tolist()
            wer = h["see"]
        elif h.get("bach") and ("bach_" + h["bach"]) in self.linien:
            um = _bach.puffer_polygon(self.linien["bach_" + h["bach"]],
                                      float(h.get("breite_m", 2.0 * float(h.get("puffer_m", 3.0)))))
            wer = h["bach"]
        elif h.get("bei") is not None:
            x, y = self.punkt(h["bei"])
            r = float(h.get("r_m", 10.0))
            t = np.linspace(0, 2 * np.pi, 24, endpoint=False)
            um = [[float(x + r * np.cos(a)), float(y + r * np.sin(a))] for a in t]
            wer = h.get("ersetzt_durch", "")
        if not netz or not um or len(um) < 3:
            self.melde(FEHLER, "houdini_ausblenden: netz und see/bach/bei noetig (%r)" % (h,))
            return
        if _st.flaeche(um) < 0:
            um = um[::-1]
        self.bestand_ausblenden.append({"art": "houdini", "netz": netz, "ersetzt_durch": h.get("ersetzt_durch", wer),
                                        "umriss_cm": [[round(p[0] * 100), round(p[1] * 100)] for p in um],
                                        "flaeche_m2": round(abs(_st.flaeche(um)), 1),
                                        "grund": h.get("grund", "geplantes Wasser ersetzt das Houdini-Wasser hier")})

    def _bestand_ausblenden(self, wid, eb):
        """Ein Abschnitt eines Bestandsbachs (baeche_alle.json), den geplantes Wasser ersetzt: von/bis sind
        Punkt-Referenzen; die Lib projiziert sie auf den Bach (Bogenlaenge s) - der Setzer blendet das Stueck aus."""
        bid = eb.get("id")
        try:
            von, bis = self.punkt(eb["von"]), self.punkt(eb["bis"])
        except (KeyError, ValueError, TypeError) as ex:
            self.melde(FEHLER, "ersetzt_bestandsbach %s: von/bis nicht aufloesbar (%s)" % (bid, ex))
            return
        d = {"art": "bach", "id": bid, "ersetzt_durch": wid,
             "von_cm": [round(von[0] * 100), round(von[1] * 100)], "bis_cm": [round(bis[0] * 100), round(bis[1] * 100)],
             "grund": eb.get("grund", "geplantes Wasser ersetzt diesen Abschnitt des Bestandsbachs")}
        bach = next((b for b in self.welt.baeche if bid in (b.get("id"), b.get("id_r2"))), None)
        if bach is None or len(bach.get("punkte") or []) < 2:
            self.melde(WARNUNG, "ersetzt_bestandsbach: Bach %s nicht in den Bachdaten (Abschnitt nicht projiziert)" % bid)
        else:
            P = np.asarray(bach["punkte"], np.float64)[:, :2] / 100.0
            (s0, d0), (s1, d1) = _projektion(P, *von), _projektion(P, *bis)
            if s1 < s0:
                s0, s1, d0, d1 = s1, s0, d1, d0
            seg = np.hypot(np.diff(P[:, 0]), np.diff(P[:, 1]))
            d.update(von_s_m=round(s0, 1), bis_s_m=round(s1, 1), laenge_m=round(s1 - s0, 1),
                     bach_laenge_m=round(float(seg.sum()), 1), abstand_m=[round(d0, 1), round(d1, 1)])
            if max(d0, d1) > 15.0:
                self.melde(WARNUNG, "ersetzt_bestandsbach %s: von/bis liegt %.0f m neben dem Bach" % (bid, max(d0, d1)))
            if s1 - s0 < 1.0:
                self.melde(WARNUNG, "ersetzt_bestandsbach %s: Abschnitt %.1f m lang" % (bid, s1 - s0))
        if eb.get("hinweis"):
            d["hinweis"] = eb["hinweis"]
        self.bestand_ausblenden.append(d)

    def _wasser_bauen(self):
        for w in self.r.get("wasser") or []:
            t = w.get("typ")
            if t == "see":
                s = self.see.get(w["id"])
                if s is None or s.get("klein"):
                    continue
                e = {"typ": "see", "id": w["id"], "umriss_cm": [[round(p[0] * 100), round(p[1] * 100)] for p in s["umriss_m"]],
                     "spiegel_cm": round(s["spiegel_m"] * 100), "tiefe_m": float(w.get("tiefe_m", 2.0)),
                     "farbe": w.get("farbe", "klar")}
                # 13f/B: tiefe_m passend zum Stempel (groesste Tiefe im Umriss nach dem Stempel)
                tmax = self._see_tiefe(s)
                if tmax is not None and abs(tmax - e["tiefe_m"]) >= 0.3:
                    self.melde(HINWEIS, "see %s: tiefe_m %.1f -> %.1f m (groesste Tiefe nach dem Stempel)"
                               % (w["id"], e["tiefe_m"], tmax))
                    e["tiefe_regel_m"] = e["tiefe_m"]
                    e["tiefe_m"] = round(tmax, 1)
                if s.get("auslass_m"):
                    e["auslass_cm"] = [round(s["auslass_m"][0] * 100), round(s["auslass_m"][1] * 100)]
                frei = self._freibord(s)
                e["freibord_min_m"] = round(frei, 2)
                if frei < -0.02:
                    self.melde(WARNUNG, "see %s: Ufer haelt nicht (bis %.2f m unter dem Spiegel)" % (w["id"], -frei))
                self.wasser.append(e)
            elif t == "bach":
                e = self._bach_eintrag(w)
                if e is not None:
                    self.wasser.append(e)
                    if w.get("furt") and (self.bach_plan.get(w.get("id")) or {}).get("furten"):
                        self._furt_steine(w)
            elif t == "wasserfall":
                kante = self.linie(w["kante"])
                zk = np.asarray(self.boden(np.array([p[0] for p in kante]), np.array([p[1] for p in kante])))
                zk = float(np.max(zk)) + float(w.get("kante_versatz_m", 0.0))
                # 13f: laeuft ein geplanter Bach ueber die Kante, gilt dessen Spiegel (sein Bett ist eingetieft)
                km = np.mean(np.asarray(kante, np.float64), axis=0)
                for pl in self.bach_plan.values():
                    dd_ = np.hypot(pl["x"] - km[0], pl["y"] - km[1])
                    k_ = int(np.argmin(dd_))
                    if dd_[k_] <= max(1.5, 0.5 * pl["B"] + 1.0):
                        zk = max(zk, float(np.max(pl["W"][max(k_ - 2, 0):k_ + 1])))
                if w.get("becken"):
                    fuss = self.see[w["becken"]]["spiegel_m"]
                elif w.get("fuss"):
                    fuss = float(self.boden(*self.punkt(w["fuss"])))
                else:
                    fuss = zk - 5.0
                br = w.get("breite_m") or math.hypot(kante[-1][0] - kante[0][0], kante[-1][1] - kante[0][1])
                e = {"typ": "wasserfall", "id": w.get("id"),
                     "kante_cm": [[round(p[0] * 100), round(p[1] * 100), round(zk * 100)] for p in kante],
                     "fuss_z_cm": round(fuss * 100), "breite_cm": round(float(br) * 100),
                     "farbe": w.get("farbe", "klar"), "fallhoehe_m": round(zk - fuss, 1)}
                if w.get("becken"):
                    e["becken"] = w["becken"]
                if zk - fuss < 1.0:
                    self.melde(WARNUNG, "wasserfall %s: Fallhoehe nur %.1f m" % (w.get("id"), zk - fuss))
                self.wasser.append(e)
            else:
                self.melde(FEHLER, "wasser.typ %r" % t)

    def _furt_steine(self, w):
        """13f A13: Furt (Bach quert Weg/Pfad im Schutzstreifen) mit Trittsteinen quer zum Bach; Regel
        bach.furt = {"palette", "groesse_m", "abstand_m", ...} (Gruppe der Ebene 'pfad')."""
        pl = self.bach_plan[w["id"]]
        fr = dict(w["furt"])
        P = pl["pts"]
        kum = _bach.bogen(P)
        punkte = []
        ab = float(fr.get("abstand_m", 0.9))
        for a_, b_ in pl["furten"]:
            sm = 0.5 * (a_ + b_)
            x, y = _bach.punkt_bei(P, kum, sm)
            x2, y2 = _bach.punkt_bei(P, kum, min(sm + 0.5, kum[-1]))
            x1, y1 = _bach.punkt_bei(P, kum, max(sm - 0.5, 0.0))
            tx, ty = float(x2 - x1), float(y2 - y1)
            n = max(math.hypot(tx, ty), 1e-9)
            nx_, ny_ = ty / n, -tx / n
            h = 0.5 * pl["B"] + 0.6
            k = -h
            while k <= h + 1e-6:
                punkte.append({"pos_m": [float(x + nx_ * k), float(y + ny_ * k)]})
                k += ab
        g = {"name": "furt_" + w["id"], "ebene": "pfad", "rolle": "stein", "warum": fr.get("warum", "Furt mit Trittsteinen"),
             "palette": fr.get("palette", "trittstein"), "verteilung": {"typ": "punkte", "punkte": punkte},
             "groesse_m": fr.get("groesse_m", [0.7, 1.0]), "eingraben": fr.get("eingraben", [0.35, 0.5]),
             "im_wasser": "egal", "weg_abstand_m": 0, "meide": None, "akteur": False}
        try:
            self.gruppe(g)
        except (KeyError, ValueError) as ex:
            self.melde(FEHLER, "Furt %s: %s" % (w["id"], ex))

    def _bach_eintrag(self, w):
        """orte.json-Eintrag eines Bachs aus self.bach_plan (13f): Spiegel = gestempeltes Bett + Tiefe (Treppe),
        Stufen explizit, Muendung nur Epic/eigener See/versickert (A9), Furten, offene Muendung."""
        wid = w.get("id", "")
        pl = self.bach_plan.get(wid)
        if pl is None:
            return None
        s, W = pl["s"], pl["W"]
        P = pl["pts"]
        kum = _bach.bogen(P)
        # Ausgabepunkte: Linienknoten (<= 2 m) + Lippe/Fuss jeder Stufe + Furtgrenzen
        sk = set(np.round(kum, 3).tolist())
        for e in pl["stufen"]:
            sk.add(round(e["s_lippe"], 3))
            sk.add(round(e["s_fuss"], 3))
        for a_, b_ in pl["furten"]:
            sk.add(round(a_, 3))
            sk.add(round(b_, 3))
        sk = np.clip(np.array(sorted(v for v in sk if -1e-3 <= v <= kum[-1] + 1e-3)), 0.0, kum[-1])
        sk = np.unique(np.concatenate([[0.0], sk, [kum[-1]]]))
        sk = sk[np.concatenate([[True], np.diff(sk) > 1e-3])]
        sk[-1] = kum[-1]
        x, y = _bach.punkt_bei(P, kum, sk)
        z = np.interp(sk, s, W)
        # Stufen exakt: Lippe = Oberwasser, Fuss = Unterwasser
        for e in pl["stufen"]:
            z[np.abs(sk - e["s_lippe"]) < 1e-3] = e["oben"]
            z[np.abs(sk - e["s_fuss"]) < 1e-3] = e["unten"]
        z = np.minimum.accumulate(z)
        # Spiegel aus dem gestempelten Bett (A12): Bett + Tiefe stimmt mit dem Plan ueberein (ausser Furt/Muendung)
        bett = np.asarray(self.boden(x, y), np.float64)
        frei = np.ones(len(sk), bool)
        for a_, b_ in pl["furten"]:
            frei &= ~((sk >= a_ - 1.0) & (sk <= b_ + 1.0))
        if pl["offen_s"] is not None:
            frei &= sk < pl["offen_s"]
        for e in pl["stufen"]:
            # Stufenzone wie im Pruefer: Lippe - (0,5 + 0,75 Zellen) ... Fuss + (0,5 + 0,75 Zellen)
            rz_ = 0.5 + 0.75 * float(self.welt.zelle_m)
            frei &= ~((sk >= e["s_lippe"] - rz_) & (sk <= e["s_fuss"] + rz_))
        frei[0] = frei[-1] = False
        # Toleranz wie im Pruefer (A12): 2 cm auf 1 m; auf 2 m verschmiert die bilineare Abfrage Bett und Boeschung
        zz = float(self.welt.zelle_m)
        tol_ = 0.02 if zz <= 1.0 else 0.02 + 0.2 * (zz - 1.0)
        ueber = (bett - z > tol_) & frei
        if ueber.any():
            self.melde(WARNUNG, "bach %s: Bett an %d von %d Punkten ueber dem Spiegel (bis %.2f m) - Stempel geschwaecht?"
                       % (wid, int(ueber.sum()), len(sk), float((bett - z)[ueber].max())))
        B = pl["B"]
        e = {"typ": "bach", "id": wid,
             "punkte_cm": [[round(float(px) * 100), round(float(py) * 100), round(float(pz) * 100), round(B * 100)]
                           for px, py, pz in zip(x, y, z)],
             "tiefe_cm": int(w.get("tiefe_cm", 30)), "farbe": w.get("farbe", "klar"),
             "quelle": bool(w.get("quelle", False)), "laenge_m": round(float(kum[-1]), 1)}
        zi = pl["ziel"]
        e["muendung"] = zi.get("id") or "versickert"
        e["muendung_art"] = zi["art"]
        if zi.get("spiegel_m") is not None:
            e["muendung_spiegel_cm"] = round(float(zi["spiegel_m"]) * 100)
        if pl["start_see"]:
            e["abfluss_von"] = pl["start_see"]
        if pl["stufen"]:
            e["stufen"] = []
            for st_ in pl["stufen"]:
                xl, yl = _bach.punkt_bei(P, kum, st_["s_lippe"])
                xf, yf = _bach.punkt_bei(P, kum, st_["s_fuss"])
                e["stufen"].append({"lippe_cm": [round(float(xl) * 100), round(float(yl) * 100), round(st_["oben"] * 100)],
                                    "fuss_cm": [round(float(xf) * 100), round(float(yf) * 100), round(st_["unten"] * 100)],
                                    "fall_m": round(st_["fall_m"], 2), "art": st_["art"]})
            mx = max(st_["fall_m"] for st_ in pl["stufen"])
            e["hinweis"] = ("%d Stufen explizit in 'stufen' (Lippe/Fuss), dazwischen Becken <= 3 %% und >= 3 m "
                            "(Regelwerk Auftrag 15), groesste %.1f m" % (len(pl["stufen"]), mx))
        if pl["furten"]:
            e["furten"] = []
            for a_, b_ in pl["furten"]:
                xa_, ya_ = _bach.punkt_bei(P, kum, a_)
                xb_, yb_ = _bach.punkt_bei(P, kum, b_)
                e["furten"].append({"von_cm": [round(float(xa_) * 100), round(float(ya_) * 100)],
                                    "bis_cm": [round(float(xb_) * 100), round(float(yb_) * 100)],
                                    "grund": "Weg-/Ortsschutz (3 m): Wasser laeuft flach ueber den Boden (Furt)"})
        if pl["offen_s"] is not None:
            xo, yo = _bach.punkt_bei(P, kum, pl["offen_s"])
            e["muendung_offen_ab_cm"] = [round(float(xo) * 100), round(float(yo) * 100)]
        pa = (getattr(self.stempel, "profil_aussen", None) or {}).get("bach_profil_%s" % wid)
        if pa is not None:
            # 13i K1 / 15e: Absenkung > 0,3 m abseits des Bachs (ausserhalb Netzrand + Uferring + Boeschung + 1 m)
            e["profil_absenkung_aussen"] = {"flaeche_m2": round(pa[0], 1), "max_m": round(pa[1], 2)}
            if pa[0] > 0:
                self.melde(FEHLER, "bach %s: Querprofil senkt %.0f m2 abseits des Bachs > 0,3 m ab (bis %.2f m, 13i K1)"
                           % (wid, pa[0], pa[1]))
        if w.get("im_bestand_stempeln"):
            e["im_bestand_stempeln"] = True
            e["im_bestand_grund"] = w.get("im_bestand_grund") or "Bach IST das unbenannte Bestandsgerinne"
        # 13g: Treppenbach (Stufe >= 0,5 m) zusaetzlich als wasser_koerper (river + kaskadennetz, A15/14b) - nur das
        # Datenformat; Stufen, Becken und Querprofil bleiben wie oben (13f)
        if any(st_["fall_m"] >= _bach.STUFE_NETZ_MIN_M for st_ in pl["stufen"]):
            if not hasattr(self, "_niagara_frei"):
                n_fx = sum(1 for f in (self.r.get("effekte") or []) if f.get("typ") == "niagara")
                self._niagara_frei = max(8 - n_fx, 0)
            lauf_id = "SW_%s_%s" % (self.id, wid)
            wk, fx = _bach.wasser_koerper(lauf_id, pl["s"], pl["x"], pl["y"], pl["W"], pl["stufen"], B,
                                          float(w.get("tiefe_cm", 30)) / 100.0, self.boden,
                                          lambda xx, yy: self.welt.hoehe_bei_m(xx, yy), self.welt.zelle_m,
                                          lambda st, t: self.melde(st if st in (FEHLER, WARNUNG) else HINWEIS,
                                                                   "bach %s: %s" % (wid, t)),
                                          niagara_frei=self._niagara_frei)
            if wk:
                self._niagara_frei -= len(fx)
                e["wasser_koerper_lauf"] = lauf_id
                e["wasser_koerper"] = wk
                n_kn = sum(1 for k_ in wk if k_["typ"] == "kaskadennetz")
                n_rv = sum(1 for k_ in wk if k_["typ"] == "river")
                self.melde(HINWEIS, "bach %s: wasser_koerper %s: %d River, %d Kaskadennetz(e), %d NS_Impact_Small"
                           % (wid, lauf_id, n_rv, n_kn, len(fx)))
        return e

    def _freibord(self, s):
        """Dichtheit des Seeufers: je Umrisspunkt das hoechste Gelaende auf dem Strahl 0,5 ... 3 m (mind. 2 Zellen)
        hinter der Uferlinie minus Spiegel; Rueckgabe das Minimum ueber alle Punkte (>= 0: Ufer haelt rundum).
        Zu- und Abfluesse dieses Sees (offene Muendungen) zaehlen nicht."""
        return ufer_freibord(self.boden, s["umriss_m"], s["spiegel_m"], self.welt.zelle_m,
                             offen=self._see_muendungen(s))

    def _see_muendungen(self, s):
        """Baeche, die an diesem See beginnen oder enden: [(x, y, radius_m)] (Ufer dort offen)."""
        out = []
        sid = next((k for k, v in self.see.items() if v is s), None)
        for pl in self.bach_plan.values():
            r = _bach.halbe_breite_eff(pl["B"], self.welt.zelle_m) + 1.0
            if pl["start_see"] == sid:
                out.append((_bach.linien_stueck(pl["pts"], 0.0, 6.0), r))
            if pl["end_see"] == sid:
                L = float(_bach.bogen(pl["pts"])[-1])
                out.append((_bach.linien_stueck(pl["pts"], L - 6.0, L), r))
        return out

    def _see_tiefe(self, s):
        """Groesste Tiefe (m) eines geplanten Sees nach dem Stempel: Spiegel - tiefstes Gelaende im Umriss."""
        U = np.asarray(s["umriss_m"], np.float64)
        z = max(self.welt.zelle_m * 0.5, 0.5)
        xs = np.arange(U[:, 0].min(), U[:, 0].max() + z, z)
        ys = np.arange(U[:, 1].min(), U[:, 1].max() + z, z)
        X, Y = np.meshgrid(xs, ys)
        m = _in_polygon(X, Y, U)
        if not m.any():
            return None
        return float(s["spiegel_m"] - np.min(np.asarray(self.boden(X[m], Y[m]))))

    def _wasser_maske_fenster(self, fe):
        """Bool-Maske im Fenster: bestehendes Suesswasser + geplante Seen + Bachlaeufe."""
        X, Y = fe.gitter_m()
        m = fe.get("wasser") > 0
        if self.bestand_seen:
            m |= self._bestand_nass(X, Y)
        for s in self.see.values():
            m |= _in_polygon(X, Y, s["umriss_m"])
        for k, pts in self.linien.items():
            if k.startswith("bach_"):
                d, _, _ = _st.polylinie_abstand(X, Y, pts)
                pl = self.bach_plan.get(k[5:])
                m |= d <= (max(1.5, _bach.halbe_breite_eff(pl["B"], self.welt.zelle_m) + 0.5) if pl else 1.5)
        return m

    def bestandswasser_laden(self, spec):
        """Regel "bestandswasser": {"seen": ["T_2954_391", ...] | "auto", "r_m": 200, "spiegel_m": optional} -
        Seen/Teiche aus wasser_welt.json["seen"], die nicht in karte_wasser stehen (Epic-Seen), als Bestand
        registrieren. "auto": alle Seen, deren Umriss naeher als r_m an der Ortsmitte liegt."""
        if not spec:
            return
        ids = spec.get("seen", "auto")
        r = float(spec.get("r_m", 200.0))
        for s in (self.welt.wasser_welt or {}).get("seen", []) or []:
            if not s.get("umriss") or len(s["umriss"]) < 3 or s.get("eis"):
                continue
            if ids != "auto" and s.get("id") not in ids:
                continue
            P = np.asarray(s["umriss"], np.float64)[:, :2] / 100.0
            if ids == "auto" and _gel.abstand_zu_polylinien(self.mx, self.my, [np.vstack([P, P[:1]])]) > r and \
                    not bool(_in_polygon(self.mx, self.my, P)):
                continue
            sp = float(spec.get("spiegel_m", float(s.get("spiegel_cm", 0.0)) / 100.0))
            self.bestand_seen.append({"id": s.get("id"), "umriss_m": P.tolist(), "spiegel_m": sp,
                                      "box": (P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max())})
        if self.bestand_seen:
            self.melde(HINWEIS, "Bestandswasser (nicht in karte_wasser): %s" % ", ".join(
                "%s (Spiegel %.2f m)" % (s["id"], s["spiegel_m"]) for s in self.bestand_seen))

    def _bestand_nass(self, x, y):
        """True, wo ein Bestands-See (bestand_seen) liegt UND das Gelaende (nach Stempel) unter seinem Spiegel."""
        x = np.asarray(x, np.float64)
        y = np.asarray(y, np.float64)
        m = np.zeros(np.broadcast(x, y).shape, bool)
        if not self.bestand_seen or m.size == 0:
            return m
        z = None
        for s in self.bestand_seen:
            x0, y0, x1, y1 = s["box"]
            inb = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
            if not inb.any():
                continue
            if z is None:
                z = np.asarray(self.boden(x, y), np.float64)
            m |= inb & (z < s["spiegel_m"] - 0.03) & _in_polygon(x, y, s["umriss_m"])
        return m

    def spiegel_von(self, sid):
        """Wasserspiegel (m) eines geplanten Sees oder eines Bestands-Sees (bestand_seen)."""
        if sid in self.see:
            return float(self.see[sid]["spiegel_m"])
        for s in self.bestand_seen:
            if s["id"] == sid:
                return float(s["spiegel_m"])
        raise KeyError("%s: See %r unbekannt (weder wasser noch bestandswasser)" % (self.id, sid))

    def im_wasser(self, x, y, rand_m=0.0):
        """True, wo bestehendes Suesswasser/Meer oder geplantes Wasser liegt."""
        x = np.asarray(x, np.float64)
        y = np.asarray(y, np.float64)
        i, j = self.welt.m_zu_ij(x, y)
        m = (self.welt.wasser[i, j] > 0) | self.welt.meer[i, j]
        if self.bestand_seen:
            m |= self._bestand_nass(x, y)
        for s in self.see.values():
            m |= _in_polygon(x, y, s["umriss_m"])
        for k, pts in self.linien.items():
            if k.startswith("bach_"):
                d, _, _ = _st.polylinie_abstand(x, y, pts)
                m |= d <= 1.0 + rand_m
        return m

    def wasser_abstand(self, x, y):
        """Abstand (m) zur naechsten Wasserkante (bestehend + geplant), negativ im Wasser (Naeherung)."""
        x = np.asarray(x, np.float64)
        y = np.asarray(y, np.float64)
        fe = self.stempel.fe
        m = self._wasser_maske_fenster(fe)
        d_aus = _gel.abstand(m, self.welt.zelle_m, 200.0)
        d_in = _gel.abstand(~m, self.welt.zelle_m, 200.0)
        dd = np.where(m, -d_in, d_aus).astype(np.float64)
        return _st._bilinear_fenster(dd, fe, self.welt, x, y, 200.0)

    # ------------------------------------------------------------------ Gruppen (§4)
    def palette(self, g):
        p = g.get("netz") or g.get("palette")
        if isinstance(p, str):
            p = self.paletten.get(p, [p])
        if not p:
            raise ValueError("%s/%s: netz oder palette fehlt" % (self.id, g.get("name")))
        gew = g.get("gewichte")
        namen, ok_gew = [], []
        for k, n in enumerate(p):
            bef = self.inv.netz_pruefen(n)
            for st, t in bef:
                if st == FEHLER:
                    self.melde(FEHLER, "%s: %s" % (g.get("name"), t))
            if any(st == FEHLER for st, _ in bef):
                continue
            namen.append(n)
            ok_gew.append(float(gew[k]) if gew else 1.0)
        return namen, np.asarray(ok_gew) / max(sum(ok_gew), 1e-9)

    def _form(self, v, rng):
        t = v.get("typ", "kreis")
        if t in ("kreis", "ring", "ellipse", "faecher", "rechteck"):
            x, y = self.punkt(v.get("bei", "mitte"))
            f = {"typ": t, "x": x, "y": y}
            if t in ("kreis", "ring"):
                f["r"] = v.get("r_m", 10.0)
            elif t == "ellipse":
                f.update(a=float(v["a_m"]), b=float(v["b_m"]), richtung=self.richtung(v.get("richtung", 0.0), v.get("bei", "mitte")))
            elif t == "faecher":
                f.update(richtung=self.richtung(v.get("richtung", "hangab"), v.get("bei", "mitte")),
                         laenge=float(v["laenge_m"]), oeffnung=float(v.get("oeffnung_grad", 40.0)),
                         t=v.get("t", [0.0, 1.0]), start=float(v.get("start_m", 0.0)))
            else:
                f.update(laenge=float(v["laenge_m"]), breite=float(v["breite_m"]),
                         richtung=self.richtung(v.get("richtung", 0.0), v.get("bei", "mitte")))
            return f
        if t == "band":
            return {"typ": "band", "punkte": self.linie(v["punkte"]), "breite": float(v.get("breite_m", 2.0)),
                    "t": v.get("t", [0.0, 1.0]), "versatz": float(v.get("versatz_m", 0.0))}
        if t == "ufer":
            x, y = self.punkt(v.get("bei", "mitte"))
            return {"typ": "kreis", "x": x, "y": y, "r": v.get("r_m", 30.0), "_ufer": v.get("band_m", [0.0, 2.0])}
        raise ValueError("verteilung.typ %r" % t)

    def gruppe(self, g):
        name = g["name"]
        if not g.get("aktiv", True):
            self.melde(HINWEIS, "Gruppe %s abgeschaltet (%s)" % (name, g.get("grund", "aktiv: false")))
            return []
        if (g.get("verteilung") or {}).get("typ") == "steilwand":
            return _sw.verkleiden(self, g)            # 13h: neue Steilflaechen mit Wand-/Klippennetzen verkleiden
        ebene = g.get("ebene", "schutt")
        rolle = g.get("rolle", "fels")
        rng = _ins.rng_fuer(self.seed, self.id, name)
        namen, gew = self.palette(g)
        if not namen:
            self.melde(FEHLER, "Gruppe %s: keine gueltigen Netze" % name)
            return []
        v = g.get("verteilung") or {"typ": "punkt"}
        t = v.get("typ", "punkt")
        yaws = None
        if t == "punkt":
            x, y = self.punkt(v.get("bei", "mitte"))
            xs, ys, ts = np.array([x]), np.array([y]), np.array([0.0])
        elif t == "punkte":
            P = [self.punkt(p) for p in v["punkte"]]
            xs, ys, ts = np.array([p[0] for p in P]), np.array([p[1] for p in P]), np.linspace(0, 1, len(P))
        elif t == "reihe":
            xs, ys, ts, yaws = self._reihe(v, rng)
        elif t == "anker":
            namen_a = sorted([k for k in self.anker if k.startswith(v["praefix"])],
                             key=lambda k: (len(k), k))
            xs = np.array([self.anker[k][0] for k in namen_a])
            ys = np.array([self.anker[k][1] for k in namen_a])
            ts = np.linspace(0, 1, max(len(namen_a), 1))[:len(namen_a)]
            if all(k in self.richtungen for k in namen_a) and namen_a:
                yaws = np.array([self.richtungen[k] + float(v.get("yaw_plus", 0.0)) for k in namen_a])
        elif t == "cluster":
            # Gruppen: Zentren gleichverteilt in der Grundform (kreis/ring/ellipse/faecher/...), je Zentrum je [a, b]
            # Punkte im radius_m (zur Mitte dichter) - Farnhorste, Blueteninseln, Pilzgruppen
            grund = self._form(dict(v, typ=v.get("form", "kreis")), rng)
            nz = _anzahl(v.get("zentren", [3, 6]), rng)
            cx, cy, _ = _ins.streue(rng, grund, nz, float(v.get("zentren_abstand_m", 2.0 * float(v.get("radius_m", 3.0)))),
                                    filter_fn=lambda a_, b_, c_: ~self.im_wasser(a_, b_))
            xs, ys = _ins.cluster(rng, list(zip(cx, cy)), tuple(v.get("je", [4, 9])), float(v.get("radius_m", 3.0)))
            ts = np.zeros(len(xs))
        elif t == "auf_gruppe":
            xs, ys, ts = self._auf_gruppe(v, rng)
            if len(xs) == 0:
                self.melde(WARNUNG, "Gruppe %s: Bezugsgruppe %s leer" % (name, v["gruppe"]))
                return []
        elif t == "um_gruppe":
            basis = [s for gn in _liste(v["gruppe"]) for s in self.gruppen.get(gn, [])]
            if not basis:
                self.melde(WARNUNG, "Gruppe %s: Bezugsgruppe %s leer" % (name, v["gruppe"]))
                return []
            seite = v.get("seite")
            if isinstance(seite, str) and seite not in ("hangab",):
                seite = {"nord": 0.0, "ost": 90.0, "sued": 180.0, "west": 270.0}.get(seite, None)
            if v.get("ring_m"):
                basis = [dict(s_, fuss_r_m=1.0, _ring_absolut=True, x_m=s_.get("x_m"), y_m=s_.get("y_m"))
                         for s_ in basis]
                ring = tuple(v["ring_m"])
            else:
                ring = tuple(v.get("ring", (0.9, 1.6)))
            xs, ys, ts = _ins.um_stuecke(rng, basis, ring, tuple(v.get("je", (3, 6))),
                                         seite, float(v.get("seite_staerke", 0.6)), self.boden)
        elif t == "halde":
            xs, ys, ts, ziel_n = _sw.halde_punkte(self, g, rng)       # 13h: Bloecke auf der Schutthalde
        else:
            form = self._form(v, rng)
            n = _anzahl(g.get("anzahl"), rng) if "anzahl" in g else int(round(float(g.get("dichte_je_m2", 0.1)) *
                                                                             _ins.form_flaeche(form)))
            xs, ys, ts = _ins.form_punkte(rng, form, max(n * int(g.get("versuche", 6)) + 8, 1))
            if "_ufer" in form:
                d = self.wasser_abstand(xs, ys)
                ok = (d >= form["_ufer"][0]) & (d <= form["_ufer"][1])
                xs, ys, ts = xs[ok], ys[ok], ts[ok]
            ziel_n = n
        if t in ("punkt", "punkte", "reihe", "um_gruppe", "anker", "auf_gruppe", "cluster"):
            ziel_n = len(xs) if "anzahl" not in g or t in ("um_gruppe", "auf_gruppe") else \
                min(len(xs), _anzahl(g["anzahl"], rng))
        # Filter
        ok = self._filter(g, xs, ys, t)
        xs, ys, ts = xs[ok], ys[ok], ts[ok]
        if yaws is not None:
            yaws = yaws[ok]
        abstand = float(g.get("abstand_m", 0.0))
        meide = g.get("meide", "massiv" if ebene in ("held", "begleiter", "schutt", "bewuchs", "wasser", "pfad") else "kern")
        eigen = _ins.Abstandsgitter(max(abstand, 1.0) * 2)
        out = []
        for k in range(len(xs)):
            if len(out) >= ziel_n:
                break
            x, y = float(xs[k]), float(ys[k])
            if abstand > 0 and not eigen.frei_min(x, y, abstand):
                continue
            netz = namen[int(rng.choice(len(namen), p=gew))]
            info = self.inv.netz(netz)
            yaw = float(yaws[k]) if yaws is not None else None
            stk = self._ein_stueck(g, info, x, y, float(ts[k]), rng, yaw)
            if stk is None:
                continue
            if meide == "massiv" and not self._massiv.frei(x, y, stk["kern_r_m"], 1.0):
                continue
            if meide == "kern" and not self._massiv.frei(x, y, 0.0, 0.7):
                continue
            stk["netz"] = info["name"]
            x, y = stk.pop("_x", x), stk.pop("_y", y)
            e = self.ebene.neu(self.id, name, ebene, netz, stk["x"], stk["y"], stk["z"], stk["q"], stk["s"],
                               kollision=stk["kollision"], akteur=stk["akteur"], sichtweite=g.get("sichtweite"),
                               schatten=g.get("schatten"), material=self._material(g), z_frei=stk.get("z_frei", False),
                               rolle=g.get("rolle", "fels"),
                               extra=dict({"hoehe_m": round(stk["hoehe_m"], 2), "boden_z": round(stk["boden_z_m"] * 100, 1),
                                           "unterkante_z": round(stk["unterkante_z_m"] * 100, 1)},
                                          **_pivot_front_extra(info, stk)) if stk["akteur"] else None)
            stk["stueck"] = e
            stk["x_m"], stk["y_m"] = x, y
            out.append(stk)
            eigen.add(x, y, 0.0)
            if stk["massiv"]:
                self._massiv.add(x, y, stk["kern_r_m"])
        self.gruppen[name] = self.gruppen.get(name, []) + out
        if len(out) < ziel_n and g.get("mindestens", 0) > len(out):
            self.melde(WARNUNG, "Gruppe %s: nur %d von %d gesetzt" % (name, len(out), ziel_n))
        elif ziel_n and len(out) < 0.5 * ziel_n and ebene in ("held", "begleiter", "schutt"):
            self.melde(HINWEIS, "Gruppe %s: nur %d von %d gesetzt (Platz/Filter)" % (name, len(out), ziel_n))
        return out

    def _auf_gruppe(self, v, rng):
        """Punkte AUF Stuecken einer Gruppe: entlang ihrer laengsten waagrechten Achse (anteil [a, b]),
        je Stueck je [m, n] Punkte (Jungtannen auf dem Ammenstamm, Kiefer auf dem Findling/der Insel)."""
        xs, ys, ts = [], [], []
        for st in [s_ for gn in _liste(v["gruppe"]) for s_ in self.gruppen.get(gn, [])]:
            info = self.inv.netz(st["stueck"]["pfad"])
            P = _ins.gedrehte_box(info, st["q"], st["s"])
            Q = P[:, :2] - P[:, :2].mean(axis=0)
            w, V = np.linalg.eigh(Q.T @ Q)
            ax = V[:, int(np.argmax(w))]
            proj = Q @ ax
            cx = (st["stueck"]["x"] + P[:, 0].mean()) / 100.0
            cy = (st["stueck"]["y"] + P[:, 1].mean()) / 100.0
            k = _anzahl(v.get("je", [1, 1]), rng)
            a, b = v.get("anteil", [0.5, 0.5])
            tt = np.sort(rng.uniform(a, b, k)) if k > 1 else np.array([(a + b) / 2.0])
            for t_ in tt:
                d = (proj.min() + t_ * (proj.max() - proj.min())) / 100.0
                xs.append(cx + ax[0] * d)
                ys.append(cy + ax[1] * d)
                ts.append(t_)
        return np.asarray(xs), np.asarray(ys), np.asarray(ts)

    def _reihe(self, v, rng):
        """Punkte entlang einer Linie im Abstand abstand_m, seitlich versetzt; yaw = Blick zur/weg von der Linie."""
        pts = self.linie(v["punkte"])
        P = np.asarray(pts, np.float64)
        seg = np.hypot(*np.diff(P, axis=0).T)
        kum = np.concatenate([[0], np.cumsum(seg)])
        L = kum[-1]
        d = float(v.get("abstand_m", 5.0))
        s = np.arange(d / 2.0, L, d) + rng.uniform(-0.25, 0.25, len(np.arange(d / 2.0, L, d))) * d
        s = np.clip(s, 0, L)
        k = np.clip(np.searchsorted(kum, s, side="right") - 1, 0, len(seg) - 1)
        f = (s - kum[k]) / np.maximum(seg[k], 1e-9)
        x = P[k, 0] + (P[k + 1, 0] - P[k, 0]) * f
        y = P[k, 1] + (P[k + 1, 1] - P[k, 1]) * f
        tx = (P[k + 1, 0] - P[k, 0]) / np.maximum(seg[k], 1e-9)
        ty = (P[k + 1, 1] - P[k, 1]) / np.maximum(seg[k], 1e-9)
        lx, ly = ty, -tx                                    # links (Norden oben)
        xs, ys, ys_yaw, ts = [], [], [], []
        for seite in _liste(v.get("seiten", ["links", "rechts"])):
            sg = 1.0 if seite == "links" else -1.0
            off = float(v.get("versatz_m", 4.0)) + rng.uniform(-0.5, 0.5, len(x)) * float(v.get("versatz_streuung_m", 1.0))
            xs.append(x + sg * lx * off)
            ys.append(y + sg * ly * off)
            # Blick zur Linie: Richtung von der Wand zur Linie
            blick = np.array([_st.vektor_kompass(-sg * a, -sg * b) for a, b in zip(lx, ly)])
            if v.get("blick", "zur_linie") == "von_linie":
                blick = (blick + 180.0) % 360.0
            ys_yaw.append(blick)
            ts.append(s / max(L, 1e-9))
        return np.concatenate(xs), np.concatenate(ys), np.concatenate(ts), np.concatenate(ys_yaw)

    def _filter(self, g, xs, ys, typ):
        ok = np.ones(len(xs), bool)
        if len(xs) == 0:
            return ok
        ok &= self.welt.im_raster_m(xs, ys)
        if not ok.any():
            return ok
        i, j = self.welt.m_zu_ij(xs, ys)
        ok &= self.welt.ort[i, j] == 0
        hz = np.asarray(self.boden(xs, ys))
        # boden_min_m: Mindesthoehe ueber dem Meer (Standard -0,3 wie der Pruefer); an Kuesten/Prielen etwas hoeher
        # setzen (z. B. 0,0), damit Rundungen zwischen Stempel- und Prueferboden kein 'im Meer' ausloesen
        ok &= hz > float(g.get("boden_min_m", -0.3))
        iw = g.get("im_wasser", "nein")
        if iw != "egal":
            w = self.im_wasser(xs, ys)
            if iw == "nein":
                ok &= ~w
            elif iw == "nur":
                ok &= w
        wa = g.get("weg_abstand_m")
        if wa is None:
            wa = 4.0 if g.get("ebene") in ("held", "begleiter", "schutt") else 2.5
        if wa > 0 and g.get("ebene") != "pfad":
            ok &= self.gel.abstand_weg[i, j] >= wa
        hg = g.get("hang_grad")
        if hg:
            h = np.asarray(self.stempel.hang_grad_bei_m(xs, ys))
            ok &= (h >= hg[0]) & (h <= hg[1])
        if g.get("hoehe_rel_m"):
            a, b = g["hoehe_rel_m"]
            ref = float(self.boden(*self.punkt(g.get("hoehe_bezug", "mitte"))))
            ok &= (hz - ref >= a) & (hz - ref <= b)
        return ok

    def _material(self, g):
        m = g.get("material")
        if not m:
            return None
        if m not in self.materialien:
            self.melde(FEHLER, "Gruppe %s: material %s nicht in 'materialwuensche' der Regeln" % (g["name"], m))
            return None
        self.mat_benutzt.add(m)
        return m

    def _ein_stueck(self, g, info, x, y, t, rng, yaw_fest=None):
        ebene = g.get("ebene", "schutt")
        rolle = g.get("rolle", "fels")
        # Massstab
        gr = info["groesse_m"]
        if g.get("groesse_m") is not None:
            ziel = _bereich(g["groesse_m"], rng)
            achse = g.get("groesse_achse", "max")
            ref = {"max": max(gr), "z": gr[2], "xy": max(gr[0], gr[1])}[achse]
            s0 = ziel / max(ref, 1e-3)
        else:
            s0 = _bereich(g.get("skala"), rng, 1.0)
        gd = g.get("gradient")
        if gd:
            s0 *= gd.get("von", 1.0) + (gd.get("bis", 1.0) - gd.get("von", 1.0)) * float(np.clip(t, 0, 1))
        sxyz = g.get("skala_xyz", [1.0, 1.0, 1.0])
        if g.get("skala_streuung"):
            a = float(g["skala_streuung"])
            sxyz = [sxyz[0] * rng.uniform(1 - a, 1 + a), sxyz[1] * rng.uniform(1 - a, 1 + a), sxyz[2] * rng.uniform(1 - a, 1 + a)]
        s = (s0 * sxyz[0], s0 * sxyz[1], s0 * sxyz[2])
        # Ausrichtung
        art = g.get("ausrichtung", "normale" if rolle in ("fels", "stein", "stamm", "wurzel", "streu") else "aufrecht")
        yaw_spec = g.get("yaw", "zufall")
        if yaw_fest is not None:
            yaw = yaw_fest + rng.uniform(-1, 1) * float(g.get("yaw_streuung_grad", 8.0))
        elif yaw_spec == "zufall":
            yaw = float(rng.uniform(0, 360))
        else:
            bezug = g.get("yaw_bei")
            if bezug is None:
                self.anker["_hier"] = (x, y)
                bezug = "_hier"
            yaw = self.richtung(yaw_spec, bezug) + rng.uniform(-1, 1) * float(g.get("yaw_streuung_grad", 10.0))
        n = None
        na = float(g.get("normale_anteil", {"normale": 1.0, "aufrecht": 0.0, "liegend": 1.0, "hochkant": 0.0}.get(art, 0.0)
                         if "normale_anteil" not in g else g["normale_anteil"]))
        if art in ("normale", "aufrecht") and rolle in ("pflanze",) and "normale_anteil" not in g:
            na = 0.3
        if rolle == "baum" and "normale_anteil" not in g:
            na = 0.05
        if na > 0:
            n = self.stempel.normale_bei_m(x, y, max(1.0, min(4.0, 0.3 * max(gr[0], gr[1]) * s0)))
        kipp_r = None
        kipp = _bereich(g.get("kipp_grad"), rng, 0.0)
        if kipp:
            kr = g.get("kipp_richtung", "zufall")
            if kr == "zufall":
                kipp_r = float(rng.uniform(0, 360))
            else:
                self.anker["_hier"] = (x, y)
                kipp_r = self.richtung(kr, "_hier") + rng.uniform(-15, 15)
        # E35: front_achse aus netze_masse.json hat Vorrang vor der Regel (sonst Regel, sonst Standard +x)
        if info.get("front_quelle") == "netze_masse" and info.get("front_achse"):
            front, front_q = info["front_achse"], "netze_masse"
        elif g.get("front_achse"):
            front, front_q = g["front_achse"], "regel"
        else:
            front, front_q = "+x", "standard"
        q = _ins.orientierung("aufrecht" if art == "normale" else art, yaw, n, na, kipp_r, kipp,
                              g.get("hochkant_achse", "y"), float(rng.uniform(0, 360)) if art == "liegend" else 0.0,
                              front)
        # Eingraben: Anteil der Dicke senkrecht zum Hang (aufrecht/normale: lokale Z-Hoehe x sz; hochkant/liegend:
        # gedrehte Welt-Hoehe), lotrecht umgerechnet mit der Hangnormalen
        kontakt = "lokal" if art in ("aufrecht", "normale") else "welt"
        if kontakt == "lokal":
            bmin, bmax = info["bounds_cm"]
            H = (bmax[2] - bmin[2]) * s[2] / 100.0
        else:
            P = _ins.gedrehte_box(info, q, s)
            H = (P[:, 2].max() - P[:, 2].min()) / 100.0
        if g.get("eingraben_m") is not None:
            e_m = _bereich(g["eingraben_m"], rng)
        elif g.get("eingraben") is not None:
            e_m = _bereich(g["eingraben"], rng) * H
        else:
            art_e, a, b = _ins.STANDARD_EINGRABEN.get(rolle, ("anteil", 0.25, 0.4))
            e_m = rng.uniform(a, b) * (H if art_e == "anteil" else 1.0)
        if n is not None and kontakt == "lokal":
            e_m = e_m / max(float(np.asarray(n)[2]), 0.5)
        zb = g.get("z_bezug")
        z_unter = None
        if zb:
            if zb.startswith("oberkante:"):
                ziel = self.gruppen.get(zb.split(":", 1)[1]) or []
                if not ziel:
                    self.melde(WARNUNG, "Gruppe %s: z_bezug %s leer" % (g["name"], zb))
                    return None
                z_unter = ziel[0]["oberkante_z_m"] + float(g.get("z_versatz_m", -0.3))
            elif zb.startswith("see:"):
                # aus dem Wasser ragend: Oberkante = Spiegel + oberkante_ueber_m, Unterkante im Seegrund
                # (reicht das Netz nicht bis zum Grund, wird es in Z gestreckt, hoechstens x1,8)
                sid = zb.split(":", 1)[1]
                z_ober = self.see[sid]["spiegel_m"] + float(g.get("oberkante_ueber_m", 1.0))
                grund = float(self.boden(x, y)) - 0.4
                if z_ober - H > grund:
                    f = min(1.8, (z_ober - grund) / max(H, 0.1))
                    s = (s[0], s[1], s[2] * f)
                    P = _ins.gedrehte_box(info, q, s)
                    H = (P[:, 2].max() - P[:, 2].min()) / 100.0
                z_unter = min(z_ober - H, grund)
                e_m = 0.0
            elif zb.startswith("boden+"):
                z_unter = float(self.boden(x, y)) + float(zb.split("+", 1)[1])
                e_m = 0.0
            elif zb.startswith("spiegel:") or zb.startswith("z:"):
                # Unterkante auf einer festen Hoehe: Wasserspiegel eines Sees/Bestands-Sees (Seerosen, Treibgut)
                # oder absolut in m - plus z_versatz_m (Standard 0)
                zz = self.spiegel_von(zb.split(":", 1)[1]) if zb.startswith("spiegel:") else float(zb.split(":", 1)[1])
                z_unter = zz + float(g.get("z_versatz_m", 0.0))
                e_m = 0.0
            elif zb.startswith("oben:"):
                # Unterkante = Oberkante des naechsten Stuecks der Gruppe an dieser Stelle (Kippblock auf Unterlage)
                ziel = self.gruppen.get(zb.split(":", 1)[1]) or []
                if not ziel:
                    return None
                nah = min(ziel, key=lambda s_: (s_["x_m"] - x) ** 2 + (s_["y_m"] - y) ** 2)
                z_unter = nah["oberkante_z_m"] + float(g.get("z_versatz_m", -0.4))
        if yaw_fest is not None and (g.get("verteilung") or {}).get("front_an_linie"):
            # Reihe: die der Linie zugewandte Seite (nicht die Mitte) liegt im Abstand versatz_m von der Linie
            dxb, dyb = _st.kompass_vektor(yaw_fest)
            P = _ins.gedrehte_box(info, q, s)
            pr = (P[:, 0] * dxb + P[:, 1] * dyb) / 100.0
            ext = float(pr.max() - 0.5 * (pr.max() + pr.min()))
            x, y = x - dxb * ext, y - dyb * ext
        if zb and zb.startswith("see:") and kontakt == "lokal":
            P = _ins.gedrehte_box(info, q, s)
            H = (P[:, 2].max() - P[:, 2].min()) / 100.0
        p = _ins.platziere(info, x, y, q, s, self.boden, e_m, g.get("bezug", "mitte" if rolle in ("pflanze", "baum") else "min"),
                           z_unter, kontakt, zentrieren=bool(g.get("zentrieren", True)))
        # z_frei: ruht nicht auf dem Gelaende (auf einem Stueck, verkeilt) - 13f A6: auch Gruppen an Wand/Kante
        # (Efeu, Luftwurzeln, Lianen, Wandmoos) mit "z_frei": true
        p["z_frei"] = (bool(zb) and not zb.startswith("see:")) or bool(g.get("z_frei"))
        p["_x"], p["_y"] = x, y
        groesse = max(gr) * max(s)
        std = _ins.STANDARD_EBENE[ebene]
        if "kollision" in g:
            kol = bool(g["kollision"])
        else:
            kol = std["kollision_ab_m"] is not None and groesse >= std["kollision_ab_m"] and rolle in (
                "fels", "stein", "baum", "stamm", "wurzel")
        akteur = bool(g.get("akteur", ebene == "held" or (ebene == "begleiter" and groesse >= 2.5)))
        massiv = kol or (akteur and rolle != "pflanze")
        # Kernradius fuer Abstaende: Baeume = Stamm (nicht Krone), Felsen = 60 % der KURZEN Fuss-Halbachse
        # (lange Waende/Staemme sperren sonst die ganze Umgebung)
        if rolle == "baum" or (rolle == "stamm" and art == "liegend"):
            kern = max(0.4, 0.035 * max(gr) * max(s))
        elif rolle in ("pflanze", "streu"):
            kern = 0.3 * min(p["fuss_a_m"], p["fuss_b_m"])
        else:
            kern = 0.75 * min(p["fuss_a_m"], p["fuss_b_m"])
        p.update({"q": q, "s": s, "kollision": kol, "akteur": akteur, "massiv": massiv, "kern_r_m": kern, "yaw": yaw,
                  "front_achse": front, "front_quelle": front_q})
        return p

    # ------------------------------------------------------------------ Lagen (§3)
    def lagen_bauen(self):
        regeln = self.r.get("lagen") or []
        pfad_regel = self.r.get("pfad")
        if not regeln and not (pfad_regel and self.pfad):
            return
        x0, y0, x1, y1 = self.stempel.fe.grenzen_m()
        if self.pfad and pfad_regel:
            P = np.asarray(self.pfad["punkte_m"])
            if self.zugang:
                P = np.concatenate([P, np.asarray(self.zugang["punkte_m"])])
            for pa in self.pfad_abschnitte:
                P = np.concatenate([P, np.asarray(pa["punkte_m"])])
            grenze = 600.0 if self.st["art"] == "leuchtfeuer" else 400.0
            if pfad_regel.get("fenster_max_m"):        # optional: Lagenfenster schaerfer begrenzen (z. B. 400 m)
                grenze = min(grenze, float(pfad_regel["fenster_max_m"]))
            x0 = max(min(x0, P[:, 0].min() - 6), self.mx - grenze / 2 + 1)
            x1 = min(max(x1, P[:, 0].max() + 6), self.mx + grenze / 2 - 1)
            y0 = max(min(y0, P[:, 1].min() - 6), self.my - grenze / 2 + 1)
            y1 = min(max(y1, P[:, 1].max() + 6), self.my + grenze / 2 - 1)
        self.lagen = _st.Lagen(self.welt, x0, y0, x1, y1, seed=self.seed)
        lg = self.lagen
        for r in regeln:
            name, wert = r["lage"], float(r.get("wert", 200))
            form = r.get("form", "kreis")
            try:
                if form in ("kreis", "ring"):
                    x, y = self.punkt(r.get("bei", "mitte"))
                    rr = r.get("r_m", 10.0)
                    innen = 0.0
                    if not _zahl(rr):
                        innen, rr = float(rr[0]), float(rr[1])
                    lg.kreis(name, x, y, float(rr), wert, r.get("rand_m", 3.0), r.get("flecken", 0.3),
                             r.get("flecken_m", 6.0), tuple(r.get("streckung", (1, 1))),
                             self.richtung(r.get("richtung", 0.0), r.get("bei", "mitte")), innen)
                elif form == "band":
                    lg.band(name, self.linie(r["punkte"]), float(r.get("breite_m", 2.0)), wert, r.get("rand_m", 3.0),
                            r.get("flecken", 0.2))
                elif form == "um_gruppe":
                    w = np.zeros_like(lg.X)
                    a, b = r.get("ring", [0.8, 1.6])
                    for s in [s for gn in _liste(r["gruppe"]) for s in self.gruppen.get(gn, [])]:
                        # 13f A11: Raender >= 3 m weich (aussen und innen, in Metern)
                        fr = max(s["fuss_r_m"], 0.3)
                        dm = np.hypot(lg.X - s["x_m"], lg.Y - s["y_m"])
                        aussen = _st.abfall(dm, b * fr, b * fr + max(fr, 3.0))
                        innen_w = 1.0 - _st.abfall(dm, max(a * fr - 3.0, 0.0), a * fr) if a > 0 else 1.0
                        w = np.maximum(w, aussen * innen_w)
                    lg.maske(name, w, wert, r.get("flecken", 0.4), r.get("flecken_m", 3.0))
                elif form == "ufer":
                    m = self._wasser_maske_fenster(lg.fe)
                    d = _gel.abstand(m, self.welt.zelle_m, 60.0)
                    a, b = r.get("band_m", [0.0, 3.0])
                    x, y = self.punkt(r.get("bei", "mitte"))
                    nah = np.hypot(lg.X - x, lg.Y - y) <= float(r.get("r_m", 60.0))
                    # 13f A11: auch der innere Rand weich (3 m), nicht hart bei d = a
                    innen_w = _st.glatt01((d - a + 1.5) / 3.0) if a > 0 else 1.0
                    w = np.where(nah, _st.abfall(d, b, b + 3.0) * innen_w, 0.0)
                    lg.maske(name, w, wert, r.get("flecken", 0.3), r.get("flecken_m", 4.0))
                elif form == "halde":
                    # 13h: Schutthalde der Boeschung (Geroell statt glatter Erdflaeche)
                    lg.maske(name, _sw.halde_lage(self, lg), wert, r.get("flecken", 0.3), r.get("flecken_m", 4.0))
                elif form == "hang":
                    x, y = self.punkt(r.get("bei", "mitte"))
                    hg = r.get("hang_grad", [0, 90])
                    h = np.asarray(self.stempel.hang_grad_bei_m(lg.X, lg.Y))
                    nah = _st.abfall(np.hypot(lg.X - x, lg.Y - y), float(r.get("r_m", 30.0)), float(r.get("r_m", 30.0)) + 4)
                    w = nah * _st.glatt01((h - hg[0] + 3) / 6.0) * (1 - _st.glatt01((h - hg[1] + 3) / 6.0))
                    lg.maske(name, w, wert, r.get("flecken", 0.3), r.get("flecken_m", 5.0))
                else:
                    self.melde(FEHLER, "lagen.form %r" % form)
            except ValueError as ex:
                self.melde(FEHLER, "lagen: %s" % ex)
        if self.pfad and pfad_regel:
            # 13f A11: Pfad-Bodenband mit 1 m Uebergang beidseits (0,5 m innen + 1 m aussen), vor dem Lagenfenster
            # auf 10 m ausgeblendet statt hart abgeschnitten
            kw = dict(rand_m=1.0, rand_min=1.0, innen_rand_m=0.5, flecken=0.15, flecken_m=3.0, fenster_aus_m=10.0)
            for name, wert in (pfad_regel.get("lagen") or {"Erde": 220, "Kies": 110}).items():
                br = self.pfad["breite_cm"] / 100.0
                lg.band(name, self.pfad["punkte_m"], br * (1.0 if wert >= 180 else 0.7), float(wert), **kw)
            if self.zugang:
                for name, wert in (self.zugang.get("lagen") or pfad_regel.get("lagen") or {"Erde": 220, "Kies": 110}).items():
                    br = self.zugang["breite_cm"] / 100.0
                    lg.band(name, self.zugang["punkte_m"], br * (1.0 if wert >= 180 else 0.7), float(wert), **kw)
            for pa in self.pfad_abschnitte:
                for name, wert in (pa.get("lagen") or pfad_regel.get("lagen") or {"Erde": 220, "Kies": 110}).items():
                    br = pa["breite_cm"] / 100.0
                    lg.band(name, pa["punkte_m"], br * (1.0 if wert >= 180 else 0.7), float(wert), **kw)
            P = np.asarray(self.pfad["punkte_m"])
            x0, y0, x1, y1 = lg.fe.grenzen_m()
            aus = ~((P[:, 0] >= x0) & (P[:, 0] <= x1) & (P[:, 1] >= y0) & (P[:, 1] <= y1))
            if aus.any():
                self.melde(HINWEIS, "Pfadband: %d von %d Pfadpunkten ausserhalb des Lagenfensters (Fenstergrenze %d m) - "
                                    "dort nur 'pfad' fuer Ferats Pfadwerkzeug" % (int(aus.sum()), len(P),
                                                                                 600 if self.st["art"] == "leuchtfeuer" else 400))

    # ------------------------------------------------------------------ Pfad (13c)
    def pfad_bauen(self):
        """Pfad (13c): zuerst ein Pfad aus standorte.json["pfade"] (fuer/pfad_id), sonst pfad_cm des Orts.
        Erweiterungen (optional, Auftrag 13 Phase 2):
          "abschnitt": "naechster" - bei geteilten Pfaden (mehrere Orte in "fuer") nur der Abschnitt, der diesem Ort
                       entlang der Bogenlaenge am naechsten liegt (Grenze = Mitte zwischen den Projektionen der Orte;
                       braucht orte_mitten). Jeder Pfadmeter gehoert so genau einem Ort (keine doppelten Stufen).
          "zugang": true | {"breite_cm", "lagen", "trittsteine", "vor_wasser_m"} - zusaetzlich der Fussweg pfad_cm des Orts
                       (Pfad -> Ort) als eigenes Bodenband + Trittsteine/Stufen (orte.json "pfad_zugang").
          trittsteine.stufen_bis_grad - Felsstufen nur bis zu dieser Steigung (steiler: Kehren, Ferats Werkzeug).
          "pfad_id": "<id>" - genau diesen Pfad aus pfade nehmen (statt des ersten mit fuer/pfad_id);
          "abschnitt": [von_m, bis_m] - nur diesen Bogenabschnitt (m ab Pfadanfang);
          "abschnitte": [{"pfad_id", "von_m", "bis_m", (breite_cm, lagen, trittsteine)}, ...] - weitere Abschnitte
                       (auch anderer Aeste) als eigene Baender + Stufen (orte.json "pfad_abschnitte"), damit ein
                       verzweigter Pfad ganz in den Lagenfenstern der Orte liegt."""
        pr = self.r.get("pfad")
        if not pr:
            return
        self._pfad_abschnitte_bauen(pr)
        quelle, P = None, None
        pfad_eintrag = None
        wahl = pr.get("pfad_id")
        for p in self.pfade_biom:
            if (p.get("id") == wahl) if wahl else (self.id in (p.get("fuer") or []) or self.st.get("pfad_id") == p.get("id")):
                P = [[q[0] / 100.0, q[1] / 100.0] for q in p["punkte_cm"]]
                quelle = "pfade:%s" % p["id"]
                art = p.get("art", "trampelpfad")
                pfad_eintrag = p
                break
        if P is not None and pr.get("abschnitt") == "naechster":
            P, a_m, b_m = self._pfad_abschnitt(pfad_eintrag, P)
            quelle += " (Abschnitt %.0f-%.0f m)" % (a_m, b_m)
        elif P is not None and isinstance(pr.get("abschnitt"), (list, tuple)):
            P, a_m, b_m = bogen_abschnitt(P, float(pr["abschnitt"][0]), float(pr["abschnitt"][1]))
            quelle += " (Abschnitt %.0f-%.0f m)" % (a_m, b_m)
        if P is None and self.st.get("pfad_cm") and pr.get("quelle", "auto") in ("auto", "pfad_cm"):
            P = [[q[0] / 100.0, q[1] / 100.0] for q in self.st["pfad_cm"]][::-1]    # Weg -> Ort
            quelle = "pfad_cm (Fussweg aus Phase 1, Weg -> Ort)"
            art = None
            if pr.get("vor_wasser_m") is not None:          # Ortsmitte liegt im geplanten See: Fussweg endet am Ufer
                P = self._bis_vor_wasser(P, float(pr["vor_wasser_m"]))
        if P is None:
            self.melde(HINWEIS, "pfad: keine Pfadquelle (pfade/pfad_cm) - kein Pfadband")
            return
        self.pfad = self._pfad_eintrag(P, pr, art, quelle)
        ts = pr.get("trittsteine")
        if ts:
            self._pfad_steine(self.pfad, ts, "pfad")
        zg = pr.get("zugang")
        if zg and pfad_eintrag is not None and self.st.get("pfad_cm"):
            zr = dict(pr, **zg) if isinstance(zg, dict) else dict(pr)
            Pz = [[q[0] / 100.0, q[1] / 100.0] for q in self.st["pfad_cm"]][::-1]      # Pfad -> Ort
            if zr.get("vor_wasser_m") is not None:
                Pz = self._bis_vor_wasser(Pz, float(zr["vor_wasser_m"]))
            self.zugang = self._pfad_eintrag(Pz, zr, None, "pfad_cm (Fussweg vom %s zum Ort)" % pfad_eintrag["id"])
            if zr.get("trittsteine"):
                self._pfad_steine(self.zugang, zr["trittsteine"], "zugang")

    def _pfad_abschnitte_bauen(self, pr):
        """pfad.abschnitte: weitere Bogenabschnitte von Pfaden aus pfade als eigene Baender (+ Stufen/Trittsteine)."""
        for k, a in enumerate(pr.get("abschnitte") or []):
            p = next((q for q in self.pfade_biom if q.get("id") == a.get("pfad_id")), None)
            if p is None:
                self.melde(FEHLER, "pfad.abschnitte: Pfad %r nicht in standorte.json[pfade]" % a.get("pfad_id"))
                continue
            Pa = [[q[0] / 100.0, q[1] / 100.0] for q in p["punkte_cm"]]
            Pa, von, bis = bogen_abschnitt(Pa, float(a.get("von_m", 0.0)), float(a.get("bis_m", 1e12)))
            ar = dict(pr, **{kk: vv for kk, vv in a.items() if kk in ("breite_cm", "lagen", "trittsteine", "vereinfachen_m")})
            e = self._pfad_eintrag(Pa, ar, p.get("art", "trampelpfad"), "pfade:%s (Abschnitt %.0f-%.0f m)" % (p["id"], von, bis))
            e.update(pfad_id=p["id"], von_m=round(von, 1), bis_m=round(bis, 1))
            if ar.get("trittsteine"):
                self._pfad_steine(e, ar["trittsteine"], "abschnitt%d" % (k + 1))
            self.pfad_abschnitte.append(e)

    def _bis_vor_wasser(self, P, vor_m):
        """pfad.zugang.vor_wasser_m: Fussweg endet vor_m vor dem ersten (geplanten oder bestehenden) Wasser, z. B. wenn
        die Ortsmitte jetzt im geplanten See liegt."""
        x, y, s = _gel.polylinie_proben(P, 0.5)
        nass = np.asarray(self.im_wasser(x, y), bool)
        if not nass.any() or nass[0]:
            return P
        k = int(np.argmax(nass))
        s_end = max(float(s[k]) - vor_m, 1.0)
        A = np.asarray(P, np.float64)
        kum = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(A, axis=0).T))])
        j = int(np.clip(np.searchsorted(kum, s_end, side="right") - 1, 0, len(A) - 2))
        f = (s_end - kum[j]) / max(kum[j + 1] - kum[j], 1e-9)
        ende = (A[j] + (A[j + 1] - A[j]) * f).tolist()
        return [list(map(float, q)) for q in A[:j + 1]] + [ende]

    def _pfad_eintrag(self, P, pr, art, quelle):
        P = _vereinfachen(P, float(pr.get("vereinfachen_m", 1.5)))
        prof = _gel.pfad_profil(self.welt, P)
        if art is None:
            art = pr.get("art", "auto")
            if art == "auto":
                art = "serpentine" if prof["max_steigung_prozent"] > 15.0 else "trampelpfad"
        br = int(pr.get("breite_cm", 140))
        br = max(120, min(200, br))
        return {"punkte_m": P, "punkte_cm": [[round(p[0] * 100), round(p[1] * 100)] for p in P],
                "breite_cm": br, "art": art, "quelle": quelle, "laenge_m": prof["laenge_m"],
                "max_steigung_grad": prof["max_steigung_grad"], "lagen": pr.get("lagen")}

    def _pfad_abschnitt(self, p, P):
        """Abschnitt eines geteilten Pfads, der diesem Ort entlang der Bogenlaenge am naechsten liegt."""
        A = np.asarray(P, np.float64)
        seg = np.hypot(*np.diff(A, axis=0).T)
        kum = np.concatenate([[0.0], np.cumsum(seg)])
        L = float(kum[-1])

        def s_von(x, y):
            d = A[1:] - A[:-1]
            t = np.clip(((x - A[:-1, 0]) * d[:, 0] + (y - A[:-1, 1]) * d[:, 1]) / np.maximum(seg ** 2, 1e-9), 0, 1)
            qx, qy = A[:-1, 0] + d[:, 0] * t, A[:-1, 1] + d[:, 1] * t
            k = int(np.argmin(np.hypot(qx - x, qy - y)))
            return float(kum[k] + t[k] * seg[k])

        mitten = dict(self.orte_mitten)
        mitten[self.id] = (self.mx, self.my)
        fuer = sorted({o for o in (p.get("fuer") or []) if o in mitten} | {self.id})
        s = {o: s_von(*mitten[o]) for o in fuer}
        reihe = sorted(fuer, key=lambda o: (s[o], o))
        k = reihe.index(self.id)
        a = 0.0 if k == 0 else 0.5 * (s[reihe[k - 1]] + s[reihe[k]])
        b = L if k == len(reihe) - 1 else 0.5 * (s[reihe[k]] + s[reihe[k + 1]])

        def punkt(sd):
            j = int(np.clip(np.searchsorted(kum, sd, side="right") - 1, 0, len(seg) - 1))
            f = (sd - kum[j]) / max(seg[j], 1e-9)
            return [float(A[j, 0] + (A[j + 1, 0] - A[j, 0]) * f), float(A[j, 1] + (A[j + 1, 1] - A[j, 1]) * f)]

        innen = [[float(q[0]), float(q[1])] for q, sk in zip(A, kum) if a < sk < b]
        return [punkt(a)] + innen + [punkt(b)], a, b

    def _pfad_steine(self, pf, ts, praefix):
        """Trittsteine (Pfad quert Wasser) und Felsstufen (Steigung entlang des Pfads >= stufen_ab_grad) als Gruppen
        <praefix>_trittsteine / <praefix>_stufen (Ebene pfad)."""
        P = pf["punkte_m"]
        x, y, s = _gel.polylinie_proben(P, float(ts.get("abstand_m", 0.9)))
        nass = self.im_wasser(x, y, 0.5)
        steil = np.zeros(len(x), bool)
        if ts.get("stufen_ab_grad") and len(x) > 2:
            # Steigung ENTLANG des Pfads (Fenster 4 m), nicht die Hangneigung quer dazu
            zz = np.asarray(self.boden(x, y), np.float64)
            h = np.degrees(np.arctan(np.abs(np.gradient(zz, s)) if np.all(np.diff(s) > 0) else np.zeros(len(x))))
            steil = h >= float(ts["stufen_ab_grad"])
            if ts.get("stufen_bis_grad") is not None:
                steil &= h <= float(ts["stufen_bis_grad"])
            # Stufen nur alle ~2,5 m
            k = np.round(s / float(ts.get("stufen_abstand_m", 2.5)))
            _, erste = np.unique(np.where(steil, k, -1), return_index=True)
            maske = np.zeros(len(x), bool)
            maske[erste] = True
            steil &= maske
        steil &= ~nass
        for name, sel, pal, gr in ((praefix + "_trittsteine", nass, ts.get("palette", ["SM_flat_rock_04"]),
                                    ts.get("groesse_m", [0.7, 1.1])),
                                   (praefix + "_stufen", steil, ts.get("stufen_palette", ts.get("palette", ["SM_flat_rock_04"])),
                                    ts.get("stufen_groesse_m", ts.get("groesse_m", [0.9, 1.4])))):
            if not sel.any():
                continue
            g = {"name": name, "ebene": "pfad", "rolle": "stein", "palette": pal, "groesse_m": gr,
                 "verteilung": {"typ": "punkte", "punkte": [{"pos_m": [float(a), float(b)]} for a, b in zip(x[sel], y[sel])]},
                 "eingraben": ts.get("eingraben", [0.45, 0.6]), "im_wasser": "egal", "weg_abstand_m": 0,
                 "meide": None, "kollision": True, "akteur": False, "ausrichtung": "normale"}
            self.gruppe(g)
        pf["trittsteine"] = len(self.gruppen.get(praefix + "_trittsteine", []))
        pf["stufen"] = len(self.gruppen.get(praefix + "_stufen", []))

    # ------------------------------------------------------------------ Effekte (§6), Klaenge
    def effekte_bauen(self):
        for e in self.r.get("effekte") or []:
            t = e.get("typ")
            n = int(e.get("anzahl", 1))
            rng = _ins.rng_fuer(self.seed, self.id, "eff", t, e.get("material", e.get("asset", "")))
            orte = [self.punkt(e.get("bei", "mitte"))]
            if n > 1 or e.get("verteilung"):
                form = self._form(e.get("verteilung") or {"typ": "kreis", "bei": e.get("bei", "mitte"), "r_m": 6.0}, rng)
                def _filt(a, b, c, form=form):
                    ok = ~self.im_wasser(a, b) if t == "decal" else np.ones(len(a), bool)
                    if "_ufer" in form:     # Verteilung "ufer": nur im Band band_m an der Wasserkante (Nassband-Decals)
                        dd = self.wasser_abstand(a, b)
                        ok &= (dd >= form["_ufer"][0]) & (dd <= form["_ufer"][1])
                    return ok
                xs, ys, _ = _ins.streue(rng, form, n, float(e.get("abstand_m", 1.5)), filter_fn=_filt, versuche=30)
                orte = list(zip(xs, ys))
            for (x, y) in orte:
                z = float(self.boden(x, y)) + float(e.get("hoehe_m", 0.0))
                pos = [round(x * 100), round(y * 100), round(z * 100)]
                if t in ("punktlicht", "spotlicht"):
                    d = {"typ": t, "pos_cm": pos, "farbe": e.get("farbe", [1.0, 0.95, 0.85]),
                         "intensitaet_cd": float(e.get("intensitaet_cd", 300.0)),
                         "radius_cm": round(float(e.get("radius_m", 10.0)) * 100), "schatten": bool(e.get("schatten", False))}
                    if t == "spotlicht":
                        kompass = self.richtung(e.get("kompass", 0.0), e.get("bei", "mitte"))
                        neig = float(e.get("neigung_grad", -80.0))
                        q = _ins.q_mul(_ins.q_yaw_kompass(kompass), _ins.q_achse((0, 1, 0), -math.radians(neig)))
                        d["richtung_q"] = [round(v, 5) for v in _ins.q_norm(q)]
                        d["kegel_grad"] = float(e.get("kegel_grad", 20.0))
                elif t == "lokaler_nebel":
                    d = {"typ": t, "pos_cm": pos, "radius_cm": round(float(e.get("radius_m", 15.0)) * 100),
                         "dichte": float(e.get("dichte", 0.05)), "farbe": e.get("farbe", [0.8, 0.82, 0.85]),
                         "hoehenabfall": float(e.get("hoehenabfall", 0.5))}
                elif t == "niagara":
                    asset = e.get("asset")
                    kopie = e.get("kopie_von")
                    if kopie:
                        # E45: Kopie NS_EL_SW_<Name> unter /Game/Eldarien/Welt/FX/Sehens, Original bleibt unberuehrt
                        pfad = asset if "/" in str(asset) else "%s/%s" % (_inv.KOPIE_ORDNER, asset)
                    else:
                        pfad = self.inv.niagara_pfad(asset) if asset else None
                    yaw_n = self.richtung(e["yaw"], e.get("bei", "mitte")) if "yaw" in e else float(e.get("yaw_grad", 0.0))
                    d = {"typ": t, "asset": pfad or asset, "pos_cm": pos,
                         "rot_q": [round(v, 5) for v in _ins.q_yaw_kompass(yaw_n)],
                         "skala": float(e.get("skala", 1.0)), "optional": bool(e.get("optional", True))}
                    if kopie:
                        d["kopie_von"] = self.inv.niagara_pfad(kopie) or kopie
                        if e.get("kopie_aenderungen"):
                            d["kopie_aenderungen"] = e["kopie_aenderungen"]
                    for k in ("wunsch_paket", "hinweis", "credits", "bedingung", "cull_m"):
                        if e.get(k):
                            d[k] = e[k]
                    befunde = (self.inv.kopie_pruefen(d["asset"], kopie, d["optional"]) if kopie else
                               self.inv.asset_pruefen("niagara", d["asset"], d["optional"]))
                    for st, txt in befunde:
                        self.melde(st, txt)
                elif t == "decal":
                    mat = self.inv.decal_pfad(e["material"]) or e["material"]
                    gr = e.get("groesse_m", [1.0, 2.0, 2.0])
                    gs = _bereich(e.get("groesse_faktor"), rng, 1.0)
                    if e.get("ausrichtung", "boden") == "boden":
                        q = _ins.q_mul(_ins.q_yaw_kompass(float(rng.uniform(0, 360))),
                                       _ins.q_achse((0, 1, 0), math.pi / 2.0))     # X-Achse (Projektion) nach unten
                    else:
                        kompass = self.richtung(e.get("blick", "hangab"), e.get("bei", "mitte"))
                        q = _ins.q_yaw_kompass((kompass + 180.0) % 360.0)          # projiziert gegen die Wand
                    d = {"typ": t, "material": mat, "pos_cm": pos,
                         "groesse_cm": [round(gr[0] * 100), round(gr[1] * 100 * gs), round(gr[2] * 100 * gs)],
                         "rot_q": [round(v, 5) for v in _ins.q_norm(q)]}
                    if not e.get("optional") and e["material"] in self.materialien and not self.inv.decal_pfad(mat):
                        # E13: fest eingeplantes Decal mit eigener Material-Instanz (materialwuensche), wird angelegt
                        self.melde(HINWEIS, "decal %s: eigene Material-Instanz aus materialwuensche, wird angelegt%s"
                                   % (mat, (" (%s)" % e["bedingung"]) if e.get("bedingung") else ""))
                    else:
                        for st, txt in self.inv.asset_pruefen("decal", mat, bool(e.get("optional", False))):
                            self.melde(st, txt)
                    if e.get("optional"):
                        d["optional"] = True
                    # eigene Decal-Textur (Wunsch, PNG im Repo) und Hinweise durchreichen (optional)
                    for k in ("textur", "textur_normal", "hinweis", "wunsch_paket", "bedingung"):
                        if e.get(k):
                            d[k] = e[k]
                else:
                    self.melde(FEHLER, "effekt.typ %r" % t)
                    continue
                if e.get("zweck"):
                    d["zweck"] = e["zweck"]
                self.effekte.append(d)
        for k in self.r.get("klaenge") or []:
            x, y = self.punkt(k.get("bei", "mitte"))
            pf = self.inv.klang_pfad(k["asset"]) or k["asset"]
            for st, txt in self.inv.asset_pruefen("klang", pf, bool(k.get("optional", False))):
                self.melde(st, txt)
            kl = {"asset": pf, "pos_cm": [round(x * 100), round(y * 100),
                                          round((float(self.boden(x, y)) + float(k.get("hoehe_m", 1.5))) * 100)],
                  "radius_cm": round(float(k.get("radius_m", 30.0)) * 100),
                  "lautstaerke": float(k.get("lautstaerke", 0.7)), "zweck": k.get("zweck", "")}
            for f in ("optional", "bedingung", "hinweis", "ersatz", "wunsch_paket"):     # E18/E29 (nur wenn gesetzt)
                if k.get(f):
                    kl[f] = k[f]
            self.klaenge.append(kl)
        for f in self.r.get("freiraeume") or []:
            x, y = self.punkt(f.get("bei", "mitte"))
            d = {"ort": self.id, "form": f.get("form", "kreis"), "mitte_cm": [round(x * 100), round(y * 100)],
                 "ebenen": f.get("ebenen", ["bestand", "witcher", "mittelschicht"]), "rollen": f.get("rollen", ["baum", "strauch"]),
                 "grund": f.get("grund", "")}
            for k in ("netze", "hinweis"):          # E23: Netznamen-Muster des auszublendenden Bestands
                if f.get(k):
                    d[k] = f[k]
            if d["form"] == "kreis":
                d["radius_cm"] = round(float(f.get("r_m", 10.0)) * 100)
            else:
                d.update(laenge_cm=round(float(f["laenge_m"]) * 100), breite_cm=round(float(f["breite_m"]) * 100),
                         richtung_grad=round(self.richtung(f.get("richtung", 0.0), f.get("bei", "mitte")), 1))
            self.freiraeume.append(d)

    # ------------------------------------------------------------------ Ablauf
    def baue(self, hooks=None):
        hooks = hooks or {}
        self.anker_aufloesen()
        if self.r.get("bestandswasser"):
            self.bestandswasser_laden(self.r["bestandswasser"])
        if hooks.get("anker"):
            hooks["anker"](self)
        self.gelaende_bauen(hooks)
        self.wasser_bauen()
        for g in self.r.get("gruppen") or []:
            try:
                self.gruppe(g)
            except (KeyError, ValueError) as ex:
                self.melde(FEHLER, "Gruppe %s: %s" % (g.get("name"), ex))
        _sw.auto_verkleiden(self)                         # 13h: restliche neue Steilflaechen mit Wandnetzen des Bioms
        if getattr(self, "_halde_gruppe", None):
            self.gruppe(self._halde_gruppe)              # 13h: Bloecke auf der Schutthalde (Boeschung)
        if hooks.get("gruppen"):
            hooks["gruppen"](self)
        self.pfad_bauen()
        self.lagen_bauen()
        self.effekte_bauen()
        if hooks.get("ende"):
            hooks["ende"](self)
        return self

    def budget(self):
        b = self.r.get("budget_grenzen") or {}
        self.ebene.ausduennen(self.id, int(b.get("instanzen", BUDGET_9["instanzen"])),
                              int(b.get("kollision", BUDGET_9["kollision"])), int(b.get("akteure", BUDGET_9["akteure"])))
        z = self.ebene.zaehle(self.id)
        eff = self.effekte
        bud = {"instanzen": z["instanzen"], "kollision": z["kollision"], "akteure": z["akteure"],
               "lichter": sum(1 for e in eff if e["typ"] in ("punktlicht", "spotlicht")),
               "niagara": sum(1 for e in eff if e["typ"] == "niagara"),
               "nebel": sum(1 for e in eff if e["typ"] == "lokaler_nebel"),
               "decals": sum(1 for e in eff if e["typ"] == "decal")}
        for k, mx in BUDGET_9.items():
            if bud[k] > mx:
                self.melde(FEHLER if k in ("lichter", "niagara", "nebel", "decals") else WARNUNG,
                           "Budget %s %d > %d (§9)" % (k, bud[k], mx))
        rw = self.r.get("budget") or {}
        for k, v in rw.items():
            if k in bud and _zahl(v) and bud[k] > 1.25 * v + 2:
                self.melde(HINWEIS, "Budget %s %d ueber Katalog-Richtwert %s" % (k, bud[k], v))
        return bud, z

    def detail_ebenen(self, z):
        de = {}
        for eb in _ins.EBENEN:
            st = [e for e in self.ebene.vom_ort(self.id) if e["ebene"] == eb]
            if not st:
                continue
            netze = {}
            for e in st:
                netze[e["netz"]] = netze.get(e["netz"], 0) + 1
            de[eb] = {"anzahl": len(st), "netze": dict(sorted(netze.items(), key=lambda kv: -kv[1]))}
        for eb, (a, b) in WITCHER_STUFEN.items():
            n = de.get(eb, {}).get("anzahl", 0)
            if n < a:
                self.melde(HINWEIS, "Witcher-Groessenstufe %s: %d (Richtwert %d-%d)" % (eb, n, a, b))
        for eb in ("bewuchs", "kontakt"):
            if eb not in de:
                self.melde(HINWEIS, "Witcher-Ebene %s fehlt" % eb)
        return de

    def eintrag_bauen(self, mat_liste):
        # 13h: Kameras gegen eigene Netze, Bestandskronen und Gelaende pruefen, blockierte versetzen (Regel "kameras");
        # vor dem Budget, weil ein freigeraeumter Standplatz Instanzen entfernt
        kam_neu = _kf.kameras_bauen(self)
        if kam_neu is not None:
            self.st = dict(self.st, kameras=kam_neu)
        e = _fmt.ort_phase2(self.st, kurz=self.r.get("kurz", ""))
        if kam_neu is not None:
            e["kameras_13h"] = "Kameras gegenueber standorte.json geaendert (13h: freie Sicht, Abstand zu Kronen)"
        if self.stempel is not None:
            e["gelaende_max_m"] = round(self.stempel.max_aenderung_m, 2)
        e["wasser"] = self.wasser
        e["effekte"] = self.effekte
        e["materialwuensche"] = mat_liste
        mk = self.r.get("marker") or {}
        e["marker"] = {"titel": mk.get("titel", self.st["name"]), "text": mk.get("text", ""),
                       "entdeckung_m": mk.get("entdeckung_m", 30)}
        e["assets_wunsch"] = self.r.get("assets_wunsch", [])
        e["budget"] = bud
        if self.pfad:
            e["pfad"] = {k: self.pfad[k] for k in ("punkte_cm", "breite_cm", "art", "quelle", "laenge_m", "max_steigung_grad",
                                                   "trittsteine", "stufen") if k in self.pfad}
        if self.zugang:
            e["pfad_zugang"] = {k: self.zugang[k] for k in ("punkte_cm", "breite_cm", "art", "quelle", "laenge_m",
                                                            "max_steigung_grad", "trittsteine", "stufen") if k in self.zugang}
        if self.pfad_abschnitte:
            e["pfad_abschnitte"] = [{k: pa[k] for k in ("pfad_id", "von_m", "bis_m", "punkte_cm", "breite_cm", "art", "quelle",
                                                        "laenge_m", "max_steigung_grad", "trittsteine", "stufen") if k in pa}
                                    for pa in self.pfad_abschnitte]
        if self.klaenge:
            e["klaenge"] = self.klaenge
        if self.freiraeume:
            e["freiraeume"] = self.freiraeume
        if self.bestand_ausblenden:
            e["bestand_ausblenden"] = self.bestand_ausblenden
        _sb.korrigieren(self)                            # 13h Nachtrag: Bloecke im See nie knapp unter dem Spiegel
        e["detail_ebenen"] = self.detail_ebenen(z)
        e["hinweise"] = [ascii_text(t) for s, _, t in self.meldungen if s == HINWEIS][:30]
        self.eintrag = e
        return e


def _projektion(P, x, y):
    """Projektion eines Punkts auf eine Polylinie P (n x 2, m) -> (Bogenlaenge s_m, Abstand_m)."""
    A, B = P[:-1], P[1:]
    AB = B - A
    L = np.maximum((AB ** 2).sum(1), 1e-12)
    t = np.clip(((x - A[:, 0]) * AB[:, 0] + (y - A[:, 1]) * AB[:, 1]) / L, 0.0, 1.0)
    Q = A + AB * t[:, None]
    dd = np.hypot(Q[:, 0] - x, Q[:, 1] - y)
    k = int(np.argmin(dd))
    seg = np.sqrt(L)
    return float(seg[:k].sum() + t[k] * seg[k]), float(dd[k])


def _pivot_front_extra(info, stk):
    """E35: Pivot-/Front-Angaben je Akteur (netze_masse.json, sonst Arbeitsannahme vermerkt)."""
    d = {"pivot_z_anteil": round(float(info.get("pivot_z_anteil", 0.0)), 2),
         "pivot_xy_versatz_m": [round(float(v), 2) + 0.0 for v in info.get("pivot_xy_versatz_m", (0.0, 0.0))],
         "front_achse": stk.get("front_achse", "+x"), "front_quelle": stk.get("front_quelle", "standard")}
    teile = []
    if info.get("pivot_quelle") == "annahme_e35":
        teile.append("Pivot unten Mitte angenommen")
    if d["front_quelle"] != "netze_masse":
        teile.append("Schauseite nicht gemessen (Annahme +Y), gesetzt mit front_achse %s (%s)"
                     % (d["front_achse"], d["front_quelle"]))
    if teile:
        d["annahme"] = "E35: " + "; ".join(teile) + " - per Skript pruefen"
    return d


def bogen_abschnitt(P, a_m, b_m):
    """Teil einer Polylinie zwischen den Bogenlaengen a_m und b_m (m ab Anfang, geklemmt) -> (punkte, a, b)."""
    A = np.asarray(P, np.float64)[:, :2]
    seg = np.hypot(*np.diff(A, axis=0).T)
    kum = np.concatenate([[0.0], np.cumsum(seg)])
    a = float(np.clip(a_m, 0.0, kum[-1]))
    b = float(np.clip(b_m, a, kum[-1]))

    def punkt(sd):
        j = int(np.clip(np.searchsorted(kum, sd, side="right") - 1, 0, len(seg) - 1))
        f = (sd - kum[j]) / max(seg[j], 1e-9)
        return [float(A[j, 0] + (A[j + 1, 0] - A[j, 0]) * f), float(A[j, 1] + (A[j + 1, 1] - A[j, 1]) * f)]

    innen = [[float(q[0]), float(q[1])] for q, sk in zip(A, kum) if a < sk < b]
    return [punkt(a)] + innen + [punkt(b)], a, b


def ufer_freibord(boden_fn, umriss_m, spiegel_m, zelle_m=1.0, offen=None):
    """Je Umrisspunkt: max. Gelaende auf dem Strahl 0,5 ... max(3, 2 x Zelle) m nach aussen (von der Umrissmitte)
    minus Spiegel; Rueckgabe Minimum (m). Eine Lippe irgendwo auf dem Strahl genuegt - das Wasser bleibt drin.
    offen: [(x, y, r)] Zu-/Abfluesse - Umrisspunkte naeher als r zaehlen nicht (dort fliesst das Wasser weiter)."""
    um = np.asarray(umriss_m, np.float64)
    if offen:
        from .stempel import polylinie_abstand
        frei = np.ones(len(um), bool)
        for o_ in offen:
            if len(o_) == 3:
                ox, oy, orr = o_
                frei &= np.hypot(um[:, 0] - ox, um[:, 1] - oy) > orr
            else:
                Pz, orr = o_
                dd, _, _ = polylinie_abstand(um[:, 0], um[:, 1], Pz)
                frei &= dd > orr
        if not frei.any():
            return 0.0            # ganzer Umriss liegt an Zu-/Abfluessen (kleiner Topf zwischen zwei Baechen)
        if True:
            um_alle = um
            um = um[frei]
            v = um - um_alle.mean(axis=0)
            n = np.maximum(np.hypot(v[:, 0], v[:, 1]), 1e-6)
            ds = np.arange(0.5, max(3.0, 2.0 * zelle_m) + 0.01, 0.5)
            best = np.full(len(um), -1e9)
            for dd in ds:
                a = um + v / n[:, None] * dd
                best = np.maximum(best, np.asarray(boden_fn(a[:, 0], a[:, 1]), np.float64))
            return float((best - spiegel_m).min())
    v = um - um.mean(axis=0)
    n = np.maximum(np.hypot(v[:, 0], v[:, 1]), 1e-6)
    ds = np.arange(0.5, max(3.0, 2.0 * zelle_m) + 0.01, 0.5)
    best = np.full(len(um), -1e9)
    for dd in ds:
        a = um + v / n[:, None] * dd
        best = np.maximum(best, np.asarray(boden_fn(a[:, 0], a[:, 1]), np.float64))
    return float((best - spiegel_m).min())


def _liste(v):
    return v if isinstance(v, (list, tuple)) else [v]


def _in_polygon(x, y, poly):
    P = np.asarray(poly, np.float64)
    x = np.asarray(x, np.float64)
    y = np.asarray(y, np.float64)
    innen = np.zeros(np.broadcast(x, y).shape, bool)
    n = len(P)
    for k in range(n):
        x1, y1 = P[k]
        x2, y2 = P[(k + 1) % n]
        c = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / np.where(y2 - y1 == 0, 1e-12, y2 - y1) + x1)
        innen ^= c
    return innen


def _ohne_schleife(pts, abstand_m, mindest_bogen_m=None):
    """Kuerzt eine Polylinie an der ersten Stelle, die naeher als abstand_m an ein frueheres Stueck kommt, das entlang
    der Linie mehr als mindest_bogen_m (Standard 3 x abstand_m) zurueckliegt."""
    P = np.asarray(pts, np.float64)[:, :2]
    if len(P) < 4:
        return pts
    kum = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))])
    mb = float(mindest_bogen_m if mindest_bogen_m is not None else 3.0 * abstand_m)
    for k in range(2, len(P)):
        alt = kum < kum[k] - mb
        if alt.any():
            d = np.hypot(P[alt, 0] - P[k, 0], P[alt, 1] - P[k, 1])
            if d.min() < abstand_m:
                return [list(map(float, q)) for q in P[:k]]
    return pts


def _verdichten(pts, max_m):
    """Segmente laenger als max_m unterteilen (Baeche: Stufen bleiben klein, Gefaelle folgt dem Gelaende)."""
    out = [list(pts[0])]
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(math.ceil(L / max_m)))
        for k in range(1, n + 1):
            out.append([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n])
    return out


def _vereinfachen(pts, tol):
    """Douglas-Peucker (m)."""
    P = np.asarray(pts, np.float64)[:, :2]
    if len(P) < 3:
        return [list(map(float, p)) for p in P]
    keep = np.zeros(len(P), bool)
    keep[0] = keep[-1] = True
    stapel = [(0, len(P) - 1)]
    while stapel:
        a, b = stapel.pop()
        if b <= a + 1:
            continue
        ab = P[b] - P[a]
        L = max(np.hypot(*ab), 1e-9)
        d = np.abs((P[a + 1:b, 0] - P[a, 0]) * ab[1] - (P[a + 1:b, 1] - P[a, 1]) * ab[0]) / L
        k = int(np.argmax(d))
        if d[k] > tol:
            m = a + 1 + k
            keep[m] = True
            stapel += [(a, m), (m, b)]
    return [[float(p[0]), float(p[1])] for p in P[keep]]


# ============================================================================================
# Biom schreiben
# ============================================================================================
def materialien_verteilen(kontexte, materialwuensche, inv):
    """Jeder Materialwunsch (<= 6 je Biom) erscheint genau einmal: beim ersten Ort, der ihn benutzt
    (sonst beim ersten Ort). Rueckgabe dict ort_id -> Liste."""
    out = {c.id: [] for c in kontexte}
    if not kontexte:
        return out
    for mw in materialwuensche:
        for st, txt in inv.material_pruefen(mw):
            kontexte[0].melde(st, txt)
        ziel = next((c for c in kontexte if mw["name"] in c.mat_benutzt), kontexte[0])
        out[ziel.id].append({k: mw[k] for k in ("name", "basis", "parameter", "fuer", "texturen", "hinweis") if k in mw})
    if len(materialwuensche) > 6:
        kontexte[0].melde(FEHLER, "%d Materialwuensche > 6 je Biom (§7)" % len(materialwuensche))
    return out


def schreibe_biom(aus_ordner, sw_ordner, biom, kontexte, ebene, materialwuensche, inv, stand=None, pruefen=True,
                  alte_orte=None):
    """orte.json + gelaende/ + lagen/ nach aus_ordner, Instanzen nach sw_ordner/<Feld>/. alte_orte: Eintraege
    anderer Orte (bei --ort), die in orte.json erhalten bleiben. Rueckgabe (orte_dict, felder_info)."""
    import os
    os.makedirs(aus_ordner, exist_ok=True)
    mats = materialien_verteilen(kontexte, materialwuensche, inv)
    orte = []
    for c in kontexte:
        e = c.eintrag_bauen(mats[c.id])
        if c.stempel is not None:
            blk = c.stempel.schreibe(aus_ordner, c.id)
            if blk:
                e["gelaende"] = blk
        if c.lagen is not None:
            blk = c.lagen.schreibe(aus_ordner, c.id)
            if blk:
                # E49: Regel warnung_akzeptiert.lagen_fenster -> Pruefer meldet das Fenster > 400 m nur als HINWEIS
                wa = (c.r.get("warnung_akzeptiert") or {}).get("lagen_fenster")
                if wa:
                    blk["warnung_akzeptiert"] = str(wa)
                e["lagen"] = blk
        orte.append(e)
    if alte_orte:
        ids = {o["id"] for o in orte}
        orte = [o for o in alte_orte if o["id"] not in ids] + orte
        orte.sort(key=lambda o: o["id"])
    # E34: im Biom benutzte Eis-/Schnee-Megascans, die der Material-Fix fuer sw_* auslaesst
    fix_aus = sorted({e["pfad"] for e in ebene.stuecke if inv.material_fix_ausnahme(e["pfad"])})
    zusatz = {"material_fix_ausnahmen": {"grund": _inv.MATERIAL_FIX_GRUND, "netze": fix_aus}} if fix_aus else {}
    if materialwuensche:
        # 13f A7: alle Materialwuensche des Bioms zusaetzlich oben in orte.json - wer nur einen Teil der Orte einbaut,
        # verliert keine Definition (beim Ort steht jeder Wunsch weiter genau einmal, beim ersten Nutzer)
        zusatz["materialwuensche_biom"] = [{k: mw[k] for k in ("name", "basis", "parameter", "fuer", "texturen", "hinweis")
                                            if k in mw} for mw in materialwuensche]
    zusatz = zusatz or None
    d = _fmt.schreibe_orte(os.path.join(aus_ordner, "orte.json"), biom, orte, stand=stand, pruefen=False, zusatz=zusatz)
    info = ebene.schreibe(sw_ordner, orte_info={o["id"]: o for o in orte})
    return d, info
