#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
felsgruppen_plan.py – Planer „Fels organisch“ (Auftrag 11, Teil C) für Eldarien (UE 5.8.3, 1-m-Raster 9577 × 7057).

Stand Korrektur Runde 1 (10.10.2026): Die Vorfassung lief lokal mit Echtdaten ohne Absturz (A5 13 311 Instanzen/65 Akteure,
G4 114, E1 18 482, C6 27 357). Diese Fassung setzt antworten/verteilung-KONVENTIONEN.md um:
  - Biom je Zelle strikt aus eigner.r8 + welt.json (Kennzahl 0 = Weltgelände -> aue, Vulkanregion -> lava); das dominante
    Feldbiom (daten/biome_je_feld.json) gilt nur, wenn eigner.r8 fehlt. Querschnitts-Planer: biome_eigen = alle 15 Biome,
    Palette und Dichte je Zelle nach Biom.
  - plan.json mit biome_fenster, zellen_zustaendig, biome_eigen, kollision_anzahl, hinweise; leerer plan.json (instanzen 0)
    statt Textabbruch (Feld ohne Land, Fehler im Feld). Pflichtdatei fehlt -> Meldung, Exit-Code 2.
  - Budget hart: <= 60 000 Instanzen, <= 3 000 mit Kollision; Ausdünnung deterministisch (Hash-Priorität) mit WARNUNG im Log.
  - print() nur ASCII (Umlaute -> ae/oe/ue/ss), Logs werden unter Windows mit cp1252 weiterverarbeitet.
  - optional felsgruppen_overrides aus den Biom-Regeldateien (Zuordnung in felsgruppen_regeln.json["overrides"]); Overrides
    gewinnen. Neue Override-Option mindestdichte_je_ha (Klasse "einzel": Einzelblöcke/Moosfelsen auch ohne Relief).
In der Cloud nur synthetisch rauchgetestet. Korrekturen bitte als auftraege/verteilung-felsgruppen-korrektur.md.

Was das Skript tut
------------------
Liest je Gitterfeld ein Fenster (Feld + 64 m Rand) aus hoehe.f32 (np.memmap, kein Volllesen), berechnet Hang, Normale,
Krümmung (Hessian einer Gauß-geglätteten Höhe, separierbare Faltung, keine Python-Schleifen über Zellen) und leitet daraus
geologische Lagen ab:
  grat       Grate/Kämme (negative Hauptkrümmung) → Hauptfels + 2–5 Nebenblöcke + Steine + Kiesel, Hauptrichtung = Gratachse
  band       Felsbänder in gleicher Höhenlage mit per-Berg-konstanter Schichtneigung (Strike/Dip aus 512-m-Wertrauschen)
  wand       Felsnasen an Wänden > 50° (plan-konvex) → Schalen/Klippen als Akteure
  fuss       Schuttfächer unter Wänden > 50° (Fächer ≤ 64 m, Größe nimmt hangabwärts ab, 4 Stufen)
  blockstrom Blockströme am Hangfuß (konkav, Wand ≥ 25 m darüber in ≤ 128 m)
  kuppe      Einzelblöcke auf Kuppen (lokale Maxima, 32 m Umkreis)
  prallhang  Felsnasen an Flussprallhängen (Krümmung der Flusspolylinie aus wasser_welt.json)
Nichts in Mulden ohne Wand darüber, nichts auf Wasser/Weg/Ort, Abstand zu Bäumen (bestand/) und Felsschalen (felsschalen/).
Zufall ist deterministisch: 64-bit-Hash aus (Seed, Klasse, Weltraster-Koordinate) → Gleichverteilte je Instanz; Nachbarfelder
erzeugen dieselben Gruppen im Überlappungsrand (kein Nahtsprung).

Aufruf
------
  python -I scripts/felsgruppen/felsgruppen_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
                                                    [--overrides-ordner PFAD] [--ohne-overrides]
  --basis   production-Wurzel (Default "."), darunter export/unreal/welt/, daten/netze.csv, daten/netze_masse.json, docs/
  --regeln  Regeldatei (Default: felsgruppen_regeln.json neben dem Skript, sonst scripts/felsgruppen/felsgruppen_regeln.json)
  --faktor  Dichtefaktor (multipliziert alle Annahme-Wahrscheinlichkeiten und die Kiesel-Dichte)
  --bild    Draufsicht docs/pruefung/felsgruppen/<Feld>.png (1 px = 1 m, Farben je Klasse)
  --overrides-ordner  Ordner mit den Biom-Regeldateien (<thema>_regeln.json). Ohne Angabe gesucht: Ordner der Regeldatei,
            <basis>/scripts/<thema>/, <Skriptordner>/../<thema>/. Fehlende Datei -> Hinweis, Biom ohne Overrides.
  --ohne-overrides    Biom-Overrides nicht lesen (Vergleichslauf).

Biom-Overrides (KONVENTIONEN §4)
--------------------------------
Je Biom-Regeldatei der Block "felsgruppen_overrides" (Zuordnung Datei -> Biome in felsgruppen_regeln.json["overrides"]).
Gilt nur für die Biome dieser Datei; Overrides gewinnen gegen felsgruppen_regeln.json. Tolerant gelesen (Werte global für
die Biome der Datei, als {biom: wert} oder in Biom-Unterblöcken {"heide": {...}}):
  palette / biom_palette        Name einer Palette (str) oder {rolle: [Netzpfade]} (ersetzt die Rolle)
  paletten_neu                  {name: {rolle: [..]}} neue Palette (Basis = bisherige Palette des Bioms)
  paletten_ergaenzung/_zusatz   {palette: {rolle: [..]}} hängt Netze an die Palette an
  fels_hero/fels_block/... , netze_moosblock, platte_ersatz, wand_palette.klippe_schale, kiesel_ring.netze,
  kontaktzone.geroellsaum_netze Rollen-Netze (Aliase: fels_hero->hero, klippe_schale->wand, geroell_platte->platte, ...)
  faktor / faktoren / biom_faktor   Zahl = Biomfaktor (ersetzt), {klasse: f} = Klassenfaktor, {biom: ...}
  biom_faktor_<biom>, gruppen_dichte_faktor (multipliziert), klassen_faktor {klasse: f}
  biom_klassen_aus / klassen_aus (ersetzt Liste), klassen_erlaubt (Komplement)
  klassen.<klasse>.p (-> Faktor p/p_basis), klassen.<klasse>.p_faktor, klassen.findling_frei.je_km2 (-> mindestdichte)
  eingraben / eingraben_anteil [lo, hi] (alle Felsrollen), rollen.<rolle>.{massstab, eingraben, sichtweite_cm},
  massstab {rolle: [..]}, sichtweite {rolle: [..]}, wand_palette.{massstab, eingraben_anteil, kippen_in_hang_grad}
  kiesel_dichte_faktor, gruppe.kiesel_dichte_je_m2, kiesel_ring.kiesel_dichte_je_m2 (-> Kieselfaktor)
  mindestdichte_je_ha           Zahl oder [lo, hi] (Mittel): Mindestzahl Felsgruppen je ha Biomfläche (Klasse einzel)
  felder                        Liste: Overrides nur in diesen Feldern
Alle anderen Schlüssel werden ignoriert und in plan.json["overrides"][datei]["ignoriert"] gelistet.
  zusatzklassen {name: {...}}   eigene Felsklassen der Biom-Planer (KONVENTIONEN §6: palette Pflicht; rolle, dichte_je_ha,
                                hang_grad, hoehe_m, wasser_abstand_m, lagen_min, kruemmung, massstab, eingraben_anteil, gruppe,
                                kollision, sichtweite, akteur). Gesetzt nur in Zellen der liefernden Biome + 30-m-Saum, im gemeinsamen
                                Budget, Klasse "z_<name>". Altstellen (heide_tundra klassen.*.neu, wueste terrassenkanten/felsnadel,
                                dschungel karstfuss/karstplatte, lava hero_akteure + Lava-Plan-Punkte) werden, wo eindeutig, abgebildet.

Ausgabe (FORMAT.md §3)
----------------------
  export/unreal/welt/felsgruppen/<Feld>/<Netzname>.f32   10 float32 LE je Instanz: x,y,z cm; qx,qy,qz,qw; sx,sy,sz
  export/unreal/welt/felsgruppen/<Feld>/plan.json        dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision,
                                                         ebene}, akteure[] (große Stücke, rolle "akteur"), entfernen, ft_ordner,
                                                         ft_praefix, biome_fenster, zellen_zustaendig, biome_eigen,
                                                         kollision_anzahl, paletten_je_biom, overrides, hinweise
  Akteur-Instanzen liegen zusätzlich in akteur_<Netzname>.f32 (gleiches Format), damit ein generischer Setzer sie nicht als
  Foliage setzt: dateien-Eintrag trägt rolle "akteur". Instanzen mit Kollision liegen in <Netzname>_kol.f32 (Kollision ist im
  Setzer je Foliage-Typ/Datei); Netz immer über dateien[...]["pfad"], nicht über den Dateinamen.

Quellen (Regeln, Zahlen): antworten/verteilung-fels-organisch.md, antworten/klippennetze-a5.md (Eingraben 25–45 %,
Schichtneigung je Front, Gruppen 2–5), antworten/bildkritik-witcher-messlatte.md (Cluster statt Stufenkanten, Floating-Check),
vorlagen/FORMAT.md (Raster, Instanzformat, Budgets). Geologie: Schutthalden 30–38° (Richtwert), Sturzsortierung optional.
"""
import argparse
import csv
import json
import math
import os
import sys
import time
import zlib

import numpy as np
np.seterr(over="ignore")  # uint64-Hash-Multiplikation darf überlaufen

try:  # numba ist optional; alles läuft auch rein mit NumPy
    import numba  # noqa: F401
    HAVE_NUMBA = True
except Exception:  # pragma: no cover
    HAVE_NUMBA = False

NX, NY, FELD = 9577, 7057, 1008
X0, Y0 = 4730.5, 4060.5  # X_m = j - X0, Y_m = i - Y0
BIOME = ["aue", "bergwald", "gletscher", "tundra", "canyon", "oedland", "heide", "elfenwald", "dschungel", "kueste", "wueste",
         "lava", "frost", "sumpf", "fjord"]
ROLLEN_ORDNUNG = ["hero", "wand", "band", "block", "platte", "stein", "kiesel"]
KLASSEN = ["grat", "band", "wand", "fuss", "blockstrom", "kuppe", "prallhang", "einzel"]
U64 = np.uint64

_ASCII = {"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss", "–": "-", "—": "-", "→": "->",
          "←": "<-", "≤": "<=", "≥": ">=", "×": "x", "°": " Grad", "…": "...", "„": '"', "“": '"', "”": '"', "‚": "'",
          "‘": "'", "’": "'", "²": "2", "§": "Par. ", "±": "+/-", "≈": "~", "·": "*", "µ": "u", "é": "e"}


def ascii_text(t):
    """Nur ASCII für print(): Logs werden unter Windows mit cp1252 weiterverarbeitet (KONVENTIONEN §5)."""
    t = str(t)
    for k, v in _ASCII.items():
        if k in t:
            t = t.replace(k, v)
    return t.encode("ascii", "replace").decode("ascii")


def log(*a):
    print(ascii_text("[felsgruppen] " + " ".join(str(x) for x in a)), flush=True)


def abbruch(msg):
    """Pflichtdatei fehlt/fehlerhaft: klare Meldung, Exit-Code 2 (KONVENTIONEN §5)."""
    log("FEHLER: " + msg)
    sys.exit(2)


# ----------------------------------------------------------------------------------------------------------------------
# Hash-Zufall (deterministisch aus Weltkoordinaten)
# ----------------------------------------------------------------------------------------------------------------------
def _mix(h):
    h = np.atleast_1d(h).astype(U64, copy=True)
    h ^= h >> U64(30)
    h *= U64(0xBF58476D1CE4E5B9)
    h ^= h >> U64(27)
    h *= U64(0x94D049BB133111EB)
    h ^= h >> U64(31)
    return h


def hash64(*teile):
    """teile: int-Arrays/Skalare (broadcastbar). Liefert uint64-Hash."""
    h = None
    for t in teile:
        a = np.atleast_1d(np.asarray(t)).astype(np.int64).astype(U64)
        h = a * U64(0x9E3779B97F4A7C15) if h is None else _mix(h ^ (a + U64(0x9E3779B97F4A7C15)))
    return _mix(h)


def uni(h, salz):
    """Gleichverteilte in [0,1) aus Hash h und Salz (int)."""
    return (_mix(h ^ U64(salz * 0x9E3779B97F4A7C15 & 0xFFFFFFFFFFFFFFFF)) >> U64(11)).astype(np.float64) * (1.0 / 9007199254740992.0)


def zwischen(h, salz, lo, hi):
    return lo + (hi - lo) * uni(h, salz)


def ganz(h, salz, lo, hi):
    """Ganzzahl in [lo, hi] (inklusiv)."""
    return lo + np.minimum((uni(h, salz) * (hi - lo + 1)).astype(np.int64), hi - lo)


# ----------------------------------------------------------------------------------------------------------------------
# Raster-Operatoren (rein NumPy, separierbar)
# ----------------------------------------------------------------------------------------------------------------------
def gauss1d(a, sigma, axis):
    r = max(1, int(3.0 * sigma + 0.5))
    x = np.arange(-r, r + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sigma) ** 2)
    k /= k.sum()
    pad = [(0, 0), (0, 0)]
    pad[axis] = (r, r)
    ap = np.pad(a, pad, mode="edge")
    out = np.zeros(a.shape, dtype=np.float64)
    n = a.shape[axis]
    for t in range(len(k)):
        sl = [slice(None), slice(None)]
        sl[axis] = slice(t, t + n)
        out += k[t] * ap[tuple(sl)]
    return out


def gauss(a, sigma):
    return gauss1d(gauss1d(a.astype(np.float64), sigma, 0), sigma, 1)


def _shift(a, d, axis, fill):
    out = np.full_like(a, fill)
    n = a.shape[axis]
    if abs(d) >= n:
        return out
    src = [slice(None), slice(None)]
    dst = [slice(None), slice(None)]
    if d > 0:
        src[axis] = slice(0, n - d)
        dst[axis] = slice(d, n)
    else:
        src[axis] = slice(-d, n)
        dst[axis] = slice(0, n + d)
    out[tuple(dst)] = a[tuple(src)]
    return out


def boxmax(a, r, fill=-np.inf):
    """Max-Filter mit Chebyshev-Radius ≥ r (Verdopplungsschritte; effektiver Radius = nächste 2^k-1 ≥ r)."""
    m = a
    for axis in (0, 1):
        step = 1
        while step <= r:
            m = np.maximum(m, np.maximum(_shift(m, step, axis, fill), _shift(m, -step, axis, fill)))
            step *= 2
    return m


def boxmin(a, r):
    return -boxmax(-a, r, fill=-np.inf)


def dilate(mask, r):
    if r <= 0:
        return mask.copy()
    return boxmax(mask.astype(np.uint8), r, fill=0) > 0


def hessian(hs):
    gy, gx = np.gradient(hs)
    hxx = np.gradient(gx, axis=1)
    hyy = np.gradient(gy, axis=0)
    hxy = np.gradient(gx, axis=0)
    tr = 0.5 * (hxx + hyy)
    dd = np.sqrt((0.5 * (hxx - hyy)) ** 2 + hxy ** 2)
    lam1 = tr + dd  # größte Krümmung (positiv = konkav/Mulde)
    lam2 = tr - dd  # kleinste (negativ = konvex/Grat)
    theta1 = 0.5 * np.arctan2(2.0 * hxy, hxx - hyy)  # Richtung des Eigenvektors zu lam1 (= Gratachse, Winkel in (x,y))
    return lam1, lam2, theta1


def wertrauschen(x, y, gitter, seed, salz):
    """Bilinear interpoliertes Gitterrauschen in [0,1) (x, y in m, Weltkoordinaten), deterministisch."""
    gx = np.floor(x / gitter)
    gy = np.floor(y / gitter)
    fx = x / gitter - gx
    fy = y / gitter - gy
    fx = fx * fx * (3 - 2 * fx)
    fy = fy * fy * (3 - 2 * fy)
    gx = gx.astype(np.int64)
    gy = gy.astype(np.int64)

    def v(dx, dy):
        return uni(hash64(seed, 7001 + salz, gx + dx, gy + dy), 3)

    return (v(0, 0) * (1 - fx) + v(1, 0) * fx) * (1 - fy) + (v(0, 1) * (1 - fx) + v(1, 1) * fx) * fy


# ----------------------------------------------------------------------------------------------------------------------
# Daten laden
# ----------------------------------------------------------------------------------------------------------------------
def feld_bereich(name):
    name = name.strip().upper()
    if len(name) < 2 or not name[0].isalpha() or not name[1:].isdigit():
        raise ValueError("Feldname wie 'B4' erwartet, nicht %r" % name)
    s = ord(name[0]) - 65
    r = int(name[1:])
    if not (0 <= s <= 9 and 1 <= r <= 7):
        raise ValueError("Feld %s außerhalb A1…J7" % name)
    j0, i0 = s * FELD, (r - 1) * FELD
    return i0, min(i0 + FELD, NY), j0, min(j0 + FELD, NX)


def lade_raster(pfad, dtype, win, pflicht=False, name=""):
    """Fenster (i0,i1,j0,j1) aus NY×NX-Raster per memmap; None wenn fehlt (oder Abbruch bei pflicht)."""
    if not os.path.isfile(pfad):
        if pflicht:
            abbruch("Pflichtdatei fehlt: %s" % pfad)
        log("Hinweis: %s fehlt (%s) - wird ohne fortgesetzt." % (name or os.path.basename(pfad), pfad))
        return None
    itemsize = np.dtype(dtype).itemsize
    groesse = os.path.getsize(pfad)
    if groesse != NX * NY * itemsize:
        msg = "%s hat %d Byte, erwartet %d (NY=%d × NX=%d × %d)" % (pfad, groesse, NX * NY * itemsize, NY, NX, itemsize)
        if pflicht:
            abbruch(msg)
        log("Hinweis: " + msg + " - ignoriert.")
        return None
    mm = np.memmap(pfad, dtype=dtype, mode="r", shape=(NY, NX))
    i0, i1, j0, j1 = win
    return np.array(mm[i0:i1, j0:j1])


def lade_netze(basis, skriptdir):
    kandidaten = [os.path.join(basis, "daten", "netze.csv"), os.path.join(skriptdir, "netze.csv"),
                  os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "netze.csv")]
    for p in kandidaten:
        if os.path.isfile(p):
            netze = {}
            with open(p, encoding="utf-8") as f:
                for r in csv.DictReader(f, delimiter=";"):
                    netze[r["pfad"]] = {"name": r["name"], "paket": r["paket"], "nanite": r["nanite"] == "1",
                                        "sx": float(r["groesse_x_m"] or 0), "sy": float(r["groesse_y_m"] or 0),
                                        "sz": float(r["groesse_z_m"] or 0),
                                        "kollision": int(r["kollision_primitive"] or 0)}
            log("Inventar: %d Netze aus %s" % (len(netze), p))
            return netze
    abbruch("Pflichtdatei fehlt: daten/netze.csv (gesucht: %s)" % ", ".join(kandidaten))


def lade_masse(basis, skriptdir):
    for p in [os.path.join(basis, "daten", "netze_masse.json"), os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "netze_masse.json")]:
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            return {k: (v["min"], v["max"]) for k, v in d.items() if "min" in v and "max" in v}
    log("Hinweis: daten/netze_masse.json fehlt – Pivot-Lage aus Regeln (netz_pivot_mitte) bzw. Annahme Pivot unten.")
    return {}


def dominantes_biom(basis, skriptdir, feld):
    """Dominantes Biom des Feldes aus daten/biome_je_feld.json; None wenn unbekannt. Nur Fallback, wenn eigner.r8 fehlt."""
    for p in [os.path.join(basis, "daten", "biome_je_feld.json"), os.path.join(skriptdir, "..", "..", "vorlagen", "daten", "biome_je_feld.json")]:
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                bp = d["felder"][feld]["biome_prozent"]
                bn = sorted(bp, key=lambda t: -t[1])[0][0]
                return bn if bn in BIOME else None
            except Exception as e:
                log("Hinweis: biome_je_feld.json unlesbar (%s)" % e)
                return None
    return None


def biom_aus_rezept(rez):
    """welt.json-Rezept -> Biomname (None = unbekannt). Weltgelände -> aue, Vulkanregion -> lava (KONVENTIONEN §1)."""
    r = str(rez).strip().lower()
    if r in BIOME:
        return r
    if r in ("", "0", "welt", "weltgelaende", "weltgelände"):
        return "aue"
    if "vulkan" in r or "lava" in r:
        return "lava"
    for bn in sorted(BIOME, key=len, reverse=True):
        if bn in r:
            return bn
    for teil, bn in (("glet", "gletscher"), ("elfen", "elfenwald"), ("dschung", "dschungel"), ("jungle", "dschungel"),
                     ("kuest", "kueste"), ("küst", "kueste"), ("wuest", "wueste"), ("wüst", "wueste"), ("moor", "sumpf"),
                     ("frost", "frost"), ("eis", "gletscher"), ("wald", "bergwald")):
        if teil in r:
            return bn
    return None


def lade_biome(welt_dir, win, basis, skriptdir, feld, regeln):
    """Biom-Index je Zelle (Index in BIOME) strikt nach KONVENTIONEN §1.

    eigner.r8 + welt.json["kacheln"][k]["rezept"]; Kennzahl 0 = Weltgelände -> aue; Vulkanregion -> lava.
    Nur wenn eigner.r8 fehlt: dominantes Feldbiom aus daten/biome_je_feld.json (Hinweis), sonst biom_zuordnung.fallback_biom.
    Liefert (biom_index_raster, quelle)."""
    shape = (win[1] - win[0], win[3] - win[2])
    fb = regeln.get("biom_zuordnung", {}).get("fallback_biom", "aue")
    fb = fb if fb in BIOME else "aue"
    eig = lade_raster(os.path.join(welt_dir, "eigner.r8"), np.uint8, win, name="eigner.r8")
    if eig is None:
        dom = dominantes_biom(basis, skriptdir, feld)
        bn = dom or fb
        log("Hinweis: eigner.r8 fehlt - Fallback: Biom im ganzen Fenster '%s' (%s)." % (
            bn, "dominantes Feldbiom aus daten/biome_je_feld.json" if dom else "biome_je_feld.json fehlt -> fallback_biom"))
        return np.full(shape, BIOME.index(bn), dtype=np.int16), ("fallback_feldbiom" if dom else "fallback_biom")
    aue = BIOME.index("aue")
    tab = np.full(256, aue, dtype=np.int16)
    wj = os.path.join(welt_dir, "welt.json")
    if not os.path.isfile(wj):
        dom = dominantes_biom(basis, skriptdir, feld) or fb
        tab[1:] = BIOME.index(dom)
        log("Hinweis: welt.json fehlt - Kennzahl 0 = aue, alle anderen Kennzahlen = '%s' (dominantes Feldbiom)." % dom)
        return tab[eig], "eigner_ohne_welt_json"
    try:
        with open(wj, encoding="utf-8") as f:
            welt = json.load(f)
    except Exception as e:
        dom = dominantes_biom(basis, skriptdir, feld) or fb
        tab[1:] = BIOME.index(dom)
        log("Hinweis: welt.json unlesbar (%s) - Kennzahl 0 = aue, alle anderen = '%s' (dominantes Feldbiom)." % (e, dom))
        return tab[eig], "eigner_ohne_welt_json"
    kacheln = welt.get("kacheln", welt) if isinstance(welt, dict) else welt
    eintraege = []
    if isinstance(kacheln, dict):
        for k, v in kacheln.items():
            try:
                eintraege.append((int(k), v))
            except ValueError:
                if isinstance(v, dict) and "id" in v:
                    eintraege.append((int(v["id"]), v))
    elif isinstance(kacheln, list):
        for idx, v in enumerate(kacheln):
            k = v.get("id", v.get("kennzahl", idx)) if isinstance(v, dict) else idx
            eintraege.append((int(k), v))
    unbekannt = set()
    bekannt = np.zeros(256, dtype=bool)
    bekannt[0] = True
    for k, v in eintraege:
        if not (0 < k < 256):
            continue  # 0 bleibt Weltgelände = aue
        rez = v.get("rezept", v.get("biom", "")) if isinstance(v, dict) else str(v)
        bn = biom_aus_rezept(rez)
        if bn is None:
            unbekannt.add(str(rez))
            bn = "aue"
        tab[k] = BIOME.index(bn)
        bekannt[k] = True
    if unbekannt:
        log("Hinweis: unbekannte Rezepte in welt.json -> aue: %s" % ", ".join(sorted(unbekannt))[:300])
    out = tab[eig]
    fehl = np.unique(eig[~bekannt[eig]])
    if len(fehl):
        log("Hinweis: Kennzahlen ohne Eintrag in welt.json -> aue: %s" % ", ".join(str(int(x)) for x in fehl[:20]))
    return out, "eigner_welt_json"


def finde_polylinien(obj, out, tiefe=0):
    """Sucht rekursiv dicts mit 'punkte' (Liste von [x_cm, y_cm, (z), (breite_cm), …])."""
    if tiefe > 6:
        return
    if isinstance(obj, dict):
        p = obj.get("punkte")
        if isinstance(p, list) and len(p) >= 3 and isinstance(p[0], (list, tuple)) and len(p[0]) >= 2:
            out.append(p)
        for v in obj.values():
            finde_polylinien(v, out, tiefe + 1)
    elif isinstance(obj, list):
        for v in obj:
            finde_polylinien(v, out, tiefe + 1)


def lade_fluesse(welt_dir):
    p = os.path.join(welt_dir, "wasser_welt.json")
    if not os.path.isfile(p):
        log("Hinweis: wasser_welt.json fehlt – Klasse prallhang entfällt.")
        return []
    try:
        with open(p, encoding="utf-8") as f:
            w = json.load(f)
    except Exception as e:
        log("Hinweis: wasser_welt.json unlesbar (%s) - Klasse prallhang entfaellt." % e)
        return []
    out = []
    finde_polylinien(w.get("fluesse", w) if isinstance(w, dict) else w, out)
    log("Flüsse: %d Polylinien aus wasser_welt.json" % len(out))
    return out


def lade_positionen_f32(ordner):
    """Alle *.f32 in ordner → (x_cm, y_cm) Arrays."""
    xs, ys = [], []
    if not os.path.isdir(ordner):
        return None
    for fn in sorted(os.listdir(ordner)):
        if fn.lower().endswith(".f32"):
            a = np.fromfile(os.path.join(ordner, fn), dtype="<f4")
            if a.size % 10 == 0 and a.size:
                a = a.reshape(-1, 10)
                xs.append(a[:, 0])
                ys.append(a[:, 1])
    if not xs:
        return None
    return np.concatenate(xs), np.concatenate(ys)


def positionen_aus_json(obj, out, tiefe=0):
    if tiefe > 6:
        return
    if isinstance(obj, dict):
        if "x" in obj and "y" in obj and isinstance(obj["x"], (int, float)) and isinstance(obj["y"], (int, float)):
            out.append((float(obj["x"]), float(obj["y"])))
        for v in obj.values():
            positionen_aus_json(v, out, tiefe + 1)
    elif isinstance(obj, list):
        if len(obj) in (7, 10) and all(isinstance(v, (int, float)) for v in obj[:2]):
            out.append((float(obj[0]), float(obj[1])))
        else:
            for v in obj:
                positionen_aus_json(v, out, tiefe + 1)


def sperrmaske(win, pos, radius):
    """Boolesche Maske im Fenster: True in radius um Positionen (cm-Weltkoordinaten)."""
    i0, i1, j0, j1 = win
    m = np.zeros((i1 - i0, j1 - j0), dtype=bool)
    if pos is None:
        return m
    x, y = pos
    j = np.round(x / 100.0 + X0).astype(np.int64) - j0
    i = np.round(y / 100.0 + Y0).astype(np.int64) - i0
    ok = (i >= 0) & (i < m.shape[0]) & (j >= 0) & (j < m.shape[1])
    m[i[ok], j[ok]] = True
    return dilate(m, int(round(radius)))


# ----------------------------------------------------------------------------------------------------------------------
# Geometrie
# ----------------------------------------------------------------------------------------------------------------------
def bilinear(h, fi, fj):
    i = np.clip(np.floor(fi).astype(np.int64), 0, h.shape[0] - 2)
    j = np.clip(np.floor(fj).astype(np.int64), 0, h.shape[1] - 2)
    di = np.clip(fi - i, 0, 1)
    dj = np.clip(fj - j, 0, 1)
    return ((h[i, j] * (1 - dj) + h[i, j + 1] * dj) * (1 - di) + (h[i + 1, j] * (1 - dj) + h[i + 1, j + 1] * dj) * di)


def quat_aus_yaw_up(yaw_rad, up):
    """Rotation mit Z-Achse = up (N×3) und X-Achse ≈ (cos yaw, sin yaw); Quaternion (x,y,z,w). Basis X×Y=Z wie in UE."""
    f0 = np.stack([np.cos(yaw_rad), np.sin(yaw_rad), np.zeros_like(yaw_rad)], axis=1)
    right = np.cross(up, f0)
    nr = np.linalg.norm(right, axis=1, keepdims=True)
    nr[nr < 1e-6] = 1.0
    right /= nr
    fwd = np.cross(right, up)
    m = np.stack([fwd, right, up], axis=2)  # Spalten = Achsen: m[:, :, 0] = X
    m00, m11, m22 = m[:, 0, 0], m[:, 1, 1], m[:, 2, 2]
    tr = m00 + m11 + m22
    q = np.zeros((len(tr), 4))
    # Shepperd: vier Fälle, vektorisiert
    c0 = tr > 0
    s = np.sqrt(np.maximum(tr, 0) + 1.0) * 2
    s[~c0] = 1.0
    q[c0, 3] = 0.25 * s[c0]
    q[c0, 0] = (m[c0, 2, 1] - m[c0, 1, 2]) / s[c0]
    q[c0, 1] = (m[c0, 0, 2] - m[c0, 2, 0]) / s[c0]
    q[c0, 2] = (m[c0, 1, 0] - m[c0, 0, 1]) / s[c0]
    c1 = (~c0) & (m00 > m11) & (m00 > m22)
    s = np.sqrt(np.maximum(1.0 + m00 - m11 - m22, 1e-12)) * 2
    q[c1, 3] = (m[c1, 2, 1] - m[c1, 1, 2]) / s[c1]
    q[c1, 0] = 0.25 * s[c1]
    q[c1, 1] = (m[c1, 0, 1] + m[c1, 1, 0]) / s[c1]
    q[c1, 2] = (m[c1, 0, 2] + m[c1, 2, 0]) / s[c1]
    c2 = (~c0) & (~c1) & (m11 > m22)
    s = np.sqrt(np.maximum(1.0 + m11 - m00 - m22, 1e-12)) * 2
    q[c2, 3] = (m[c2, 0, 2] - m[c2, 2, 0]) / s[c2]
    q[c2, 0] = (m[c2, 0, 1] + m[c2, 1, 0]) / s[c2]
    q[c2, 1] = 0.25 * s[c2]
    q[c2, 2] = (m[c2, 1, 2] + m[c2, 2, 1]) / s[c2]
    c3 = (~c0) & (~c1) & (~c2)
    s = np.sqrt(np.maximum(1.0 + m22 - m00 - m11, 1e-12)) * 2
    q[c3, 3] = (m[c3, 1, 0] - m[c3, 0, 1]) / s[c3]
    q[c3, 0] = (m[c3, 0, 2] + m[c3, 2, 0]) / s[c3]
    q[c3, 1] = (m[c3, 1, 2] + m[c3, 2, 1]) / s[c3]
    q[c3, 2] = 0.25 * s[c3]
    q /= np.linalg.norm(q, axis=1, keepdims=True)
    return q


# ----------------------------------------------------------------------------------------------------------------------
# Biom-Overrides (felsgruppen_overrides aus den Biom-Regeldateien, KONVENTIONEN §4)
# ----------------------------------------------------------------------------------------------------------------------
ROLLEN_ALIAS = {r: r for r in ROLLEN_ORDNUNG}
ROLLEN_ALIAS.update({"fels_hero": "hero", "fels_wand": "wand", "klippe_schale": "wand", "fels_band": "band", "fels_block": "block",
                     "fels_stein": "stein", "fels_platte": "platte", "geroell_platte": "platte", "geroellsaum": "kiesel",
                     "geroellsaum_netze": "kiesel", "fels_kiesel": "kiesel", "netze_moosblock": "block",
                     "platte_ersatz": "platte"})
DOKU_SCHLUESSEL = ("hinweis", "doku", "quelle", "stand", "biom", "bedingung")


def _ist_doku(k):
    return k in DOKU_SCHLUESSEL or k.startswith("_") or k.endswith("_hinweis") or k.endswith("_doku")


def _zahl(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _spanne(v):
    return isinstance(v, (list, tuple)) and len(v) == 2 and all(_zahl(x) for x in v)


def _ist_biom_dict(v):
    return isinstance(v, dict) and len(v) > 0 and all(k in BIOME for k in v)


def norm_pfad(p):
    """Netzpfad tolerant: ohne '/Game/' -> ergänzt; '.Name'-Suffix entfernt."""
    p = str(p).strip()
    if not p.startswith("/"):
        p = "/Game/" + p
    letzt = p.rsplit("/", 1)[-1]
    if "." in letzt:
        p = p.rsplit(".", 1)[0]
    return p


ZK_ROLLEN = {"fels_block": "block", "block": "block", "fels_hero": "hero", "hero": "hero", "fels_stein": "stein", "stein": "stein",
             "geroell_platte": "platte", "fels_platte": "platte", "platte": "platte", "kiesel": "kiesel", "ufer_stein": "kiesel",
             "klippe_schale": "wand", "wand": "wand", "band": "band", "fels_band": "band", "eis": "stein"}


def _mittel(v):
    if _zahl(v):
        return float(v)
    if _spanne(v):
        return 0.5 * (v[0] + v[1])
    return None


def _trapez_spec(v):
    """[lo, hi] (hart) oder [a, b, c, d] (Rampe a->b, voll b..c, Rampe c->d)."""
    if _spanne(v):
        return (float(v[0]), float(v[0]), float(v[1]), float(v[1]))
    if isinstance(v, (list, tuple)) and len(v) == 4 and all(_zahl(x) for x in v):
        return tuple(float(x) for x in v)
    return None


def trapez(x, t):
    a, b, c, d = t
    w = np.ones(np.shape(x))
    w = np.where(x < a, 0.0, w)
    w = np.where(x > d, 0.0, w)
    if b > a:
        w = np.where((x >= a) & (x < b), (x - a) / (b - a), w)
    if d > c:
        w = np.where((x > c) & (x <= d), (d - x) / (d - c), w)
    return w


def _leer_rec():
    return {"palette_name": None, "palette_rollen": {}, "palette_zusatz": {}, "paletten_neu": {}, "faktor": None,
            "faktor_mult": 1.0, "klassen_faktor": {}, "klassen_aus": None, "eingraben": None, "rollen": {},
            "kiesel_faktor": None, "mindestdichte_je_ha": None, "mindest_findling": None, "einzel_rollen": None,
            "klassen_param": {}, "felder": None}


class OverrideLeser:
    """Normalisiert einen felsgruppen_overrides-Block (beliebiges der vorkommenden Schemata) zu je-Biom-Datensätzen."""

    def __init__(self, R, datei, biome, netze):
        self.R = R
        self.datei = datei
        self.biome = [b for b in biome if b in BIOME]
        self.netze = netze
        self.rec = {bn: _leer_rec() for bn in self.biome}
        self.gelesen, self.ignoriert, self.fehlpfade, self.fremd = [], [], [], []
        self.zusatz = []          # normalisierte Zusatzklassen (KONVENTIONEN §6)
        self.datei_json = {}      # ganze Biom-Regeldatei (für eindeutige Altwerte, z. B. lava punkte.spire_vorschlag)
        self.gesperrt = gesperrte_netze(R)  # Runde 2: Sperrliste (felsgruppen_regeln.json "gesperrt")
        self.gesperrt_treffer = []
        k = R["gruppe"]["kiesel_dichte_je_m2"]
        self.kiesel_basis = 0.5 * (k[0] + k[1])

    def _g(self, t):
        if t not in self.gelesen:
            self.gelesen.append(t)

    def _i(self, t):
        if t not in self.ignoriert:
            self.ignoriert.append(t)

    def je_biom(self, v, scope, pfad):
        if _ist_biom_dict(v):
            for bn, x in v.items():
                if bn in scope:
                    yield bn, x
                else:
                    self.fremd.append("%s.%s" % (pfad, bn))
        else:
            for bn in scope:
                yield bn, v

    def pfade(self, liste):
        if isinstance(liste, str):
            liste = [liste]
        out = []
        if not isinstance(liste, (list, tuple)):
            return out
        for p in liste:
            if not isinstance(p, str):
                continue
            q = norm_pfad(p)
            if q in self.gesperrt:
                self.gesperrt_treffer.append(q)
                continue
            if q in self.netze:
                if q not in out:
                    out.append(q)
            elif q not in self.fehlpfade:
                self.fehlpfade.append(q)
        return out

    def rollen_palette(self, d, scope, pfad):
        for k, v in d.items():
            r = ROLLEN_ALIAS.get(k)
            p = "%s.%s" % (pfad, k) if pfad else k
            if r is None:
                if not _ist_doku(k):
                    self._i(p)
                continue
            liste = self.pfade(v)
            if not liste:
                self._i(p + " (keine gueltigen Netzpfade)")
                continue
            for bn in scope:
                self.rec[bn]["palette_rollen"][r] = liste
            self._g(p)

    def paletten_tabelle(self, d, scope, pfad, ziel):
        if not isinstance(d, dict):
            self._i(pfad)
            return
        for name, rollen in d.items():
            if not isinstance(rollen, dict):
                if not _ist_doku(name):
                    self._i("%s.%s" % (pfad, name))
                continue
            tab = {}
            for k, v in rollen.items():
                r = ROLLEN_ALIAS.get(k)
                if r is None and k == "eis":  # Altstelle hochgebirge: Eiszapfen, Werte aus klassen.grat.hinweis
                    self.zusatz_lesen("eis", {"palette": v, "rolle": "eis", "hang_grad": [55, 90], "exposition": "nord",
                                              "dichte_je_m2": 0.04, "lagen_min": {"Schnee": 140}, "eingraben_anteil": [0.0, 0.05],
                                              "kollision": False, "kruemmung": "konvex"}, scope, "%s.%s.%s" % (pfad, name, k), alt=True)
                    continue
                if r is None:
                    if not _ist_doku(k):
                        self._i("%s.%s.%s" % (pfad, name, k))
                    continue
                liste = self.pfade(v)
                if liste:
                    tab[r] = liste
            if tab:
                for bn in scope:
                    self.rec[bn][ziel].setdefault(name, {}).update(tab)
                self._g("%s.%s" % (pfad, name))

    def palette(self, v, scope, pfad):
        # Schema wie mittelschicht_overrides: {"biom": {biom: name}, "ergaenzung": {palette: {rolle: [..]}}, "neu": {...},
        # "<rolle>": [..], "bevorzugt": ... (ignoriert)}
        if isinstance(v, dict) and not _ist_biom_dict(v) and any(k in ("biom", "ergaenzung", "zusatz", "neu", "rollen") for k in v):
            rest = {}
            for k, x in v.items():
                p = "%s.%s" % (pfad, k)
                if k == "biom":
                    self.palette(x, scope, p)
                elif k in ("ergaenzung", "zusatz"):
                    self.paletten_tabelle(x, scope, p, "palette_zusatz")
                elif k == "neu":
                    self.paletten_tabelle(x, scope, p, "paletten_neu")
                elif k == "rollen" and isinstance(x, dict):
                    self.rollen_palette(x, scope, p)
                else:
                    rest[k] = x
            if rest:
                self.rollen_palette(rest, scope, pfad)
            return
        for bn, x in self.je_biom(v, scope, pfad):
            if isinstance(x, str):
                self.rec[bn]["palette_name"] = x
                self._g(pfad)
            elif isinstance(x, dict):
                self.rollen_palette(x, [bn], pfad)
            elif isinstance(x, list):
                self.palette_liste(x, [bn], pfad)
            else:
                self._i(pfad)

    def palette_liste(self, lst, scope, pfad):
        """palette als Liste: Netzpfade (Rolle aus der Netzgröße laut _doku.rollen: hero > 3 m, block 0,8-3 m, stein < 0,8 m,
        kiesel < 0,4 m, platte = flach) oder {"pfad"/"netz": ..., "rolle": ...}. Ersetzt die genannten Rollen der Biom-Palette;
        nicht belegte Rollen (z. B. wand, band) bleiben aus der Standardpalette."""
        tab = {}
        for e in lst:
            if isinstance(e, dict):
                p_ = e.get("pfad", e.get("netz"))
                r = ROLLEN_ALIAS.get(e.get("rolle", ""), ZK_ROLLEN.get(e.get("rolle", "")))
            else:
                p_, r = e, None
            if not isinstance(p_, str):
                continue
            q = self.pfade([p_])
            if not q:
                continue
            if r is None:
                n = self.netze[q[0]]
                hoch, breit = n["sz"], max(n["sx"], n["sy"])
                r = ("platte" if breit >= 1.0 and hoch < 0.3 * breit else "hero" if hoch > 3.0 else "block" if hoch >= 0.8
                     else "stein" if hoch >= 0.4 else "kiesel")
            tab.setdefault(r, []).append(q[0])
        if not tab:
            self._i(pfad + " (Liste ohne gueltige Netzpfade)")
            return
        for bn in scope:
            self.rec[bn]["palette_rollen"].update(tab)
        self._g(pfad + " (Liste -> %s)" % ", ".join("%s %d" % (r, len(l)) for r, l in sorted(tab.items())))

    def _kf(self, bn, kname, f):
        kf = self.rec[bn]["klassen_faktor"]
        kf[kname] = kf.get(kname, 1.0) * float(f)

    def faktor(self, v, scope, pfad):
        if _zahl(v):
            for bn in scope:
                self.rec[bn]["faktor"] = float(v)
            self._g(pfad)
            return
        if not isinstance(v, dict):
            self._i(pfad)
            return
        if _ist_biom_dict(v):
            for bn, x in self.je_biom(v, scope, pfad):
                self.faktor(x, [bn], pfad)
            return
        for k, x in v.items():
            p = "%s.%s" % (pfad, k)
            if k in KLASSEN and _zahl(x):
                for bn in scope:
                    self._kf(bn, k, x)
            elif k in ("gesamt", "dichte") and _zahl(x):
                for bn in scope:
                    self.rec[bn]["faktor"] = float(x)
            elif k == "biom":  # Zahl oder {biom: zahl}
                self.faktor(x, scope, p)
                continue
            elif k == "klassen":  # {klasse: f} oder {biom: {klasse: f}}
                self.klassen_faktor(x, scope, p)
                continue
            elif k == "kiesel":  # Zahl oder {biom: zahl}
                for bn, y in self.je_biom(x, scope, p):
                    if _zahl(y):
                        self.rec[bn]["kiesel_faktor"] = float(y)
            elif k == "eingraben":
                self.eingraben(x, scope, p)
                continue
            else:
                if not _ist_doku(k):
                    self._i(p)
                continue
            self._g(p)

    def klassen_faktor(self, v, scope, pfad):
        for bn, x in self.je_biom(v, scope, pfad):
            if not isinstance(x, dict):
                self._i(pfad)
                continue
            for k, f in x.items():
                if k in KLASSEN and _zahl(f):
                    self._kf(bn, k, f)
                    self._g(pfad)
                elif not _ist_doku(k):
                    self._i("%s.%s" % (pfad, k))

    def klassen_aus(self, v, scope, pfad, erlaubt=False):
        for bn, x in self.je_biom(v, scope, pfad):
            if not isinstance(x, list):
                self._i(pfad)
                continue
            liste = [k for k in x if k in KLASSEN]
            if erlaubt:  # Komplement der Relief-Klassen; "einzel" (mindestdichte) bleibt erlaubt
                liste = [k for k in KLASSEN if k != "einzel" and k not in liste]
            self.rec[bn]["klassen_aus"] = liste
            self._g(pfad)

    def klassen(self, v, scope, pfad):
        if not isinstance(v, dict):
            self._i(pfad)
            return
        for kname, d in v.items():
            pk = "%s.%s" % (pfad, kname)
            if not isinstance(d, dict):
                if not _ist_doku(kname):
                    self._i(pk)
                continue
            for bn, par in self.je_biom(d, scope, pk):
                if not isinstance(par, dict):
                    continue
                if kname in KLASSEN:
                    basis_p = float(self.R["klassen"].get(kname, {}).get("p", 1.0)) or 1.0
                    for k, x in par.items():
                        if k == "p" and _zahl(x):
                            self._kf(bn, kname, float(x) / basis_p)
                            self._g(pk + ".p")
                        elif k == "p_faktor" and _zahl(x):
                            self._kf(bn, kname, x)
                            self._g(pk + ".p_faktor")
                        elif (k == "hero_p" and _zahl(x)) or (k in ("block", "stein", "kiesel", "band", "wand", "n", "eingraben")
                                                              and _spanne(x)):
                            # Gruppen-Feinparameter: werden beim Gruppenaufbau je Biom angewandt
                            self.rec[bn]["klassen_param"].setdefault(kname, {})[k] = (float(x) if _zahl(x) else
                                                                                       [x[0], x[1]])
                            self._g("%s.%s" % (pk, k))
                        elif k in ("umkreis_m", "hang_grad", "raster_m", "kruemmung_min", "ufer_abstand_m", "abstand_m",
                                   "stufen", "faecher_max_m", "grat_staerke_min", "nase_min", "hohl_min", "wand_umkreis_m"):
                            self._i("%s.%s (%s)" % (pk, k, "Kandidatensuche gilt fuer alle Biome gemeinsam"))
                        elif not _ist_doku(k):
                            self._i("%s.%s" % (pk, k))
                elif kname in ("findling_frei", "findlinge", "einzelbloecke") and ("je_km2" in par or "je_ha" in par) \
                        and not par.get("neu"):
                    w = par.get("je_ha")
                    if w is None:
                        jk = par["je_km2"]
                        w = (0.5 * (jk[0] + jk[1]) if _spanne(jk) else jk) / 100.0 if (_spanne(jk) or _zahl(jk)) else None
                    elif _spanne(w):
                        w = 0.5 * (w[0] + w[1])
                    if _zahl(w):
                        self.rec[bn]["mindest_findling"] = float(w)
                        self._g(pk + ".je_km2 (-> mindestdichte_je_ha)")
                    for k in par:
                        if k not in ("je_km2", "je_ha") and not _ist_doku(k):
                            self._i("%s.%s" % (pk, k))
                elif isinstance(par, dict) and par.get("neu"):  # Altstelle heide_tundra (blockfeld, findling_frei): Netze aus Biom-Palette
                    pz = {k: x for k, x in par.items() if k not in ("neu", "flechten")}
                    ex = {}
                    if "palette" not in par and "netze" not in par:
                        hp = par.get("hero_p")
                        ex["palette_rollen"] = ["hero", "block"] if (_zahl(hp) and hp >= 0.5) else ["block"]
                        ex["rolle"] = "fels_hero" if (_zahl(hp) and hp >= 0.5) else "fels_block"
                    if _zahl(par.get("hero_p")) and _spanne(par.get("block")):  # Hauptstück + Nebenblöcke
                        pz["block"] = [1 + par["block"][0], 1 + par["block"][1]]
                    nm = kname if len(self.biome) == 1 else "%s_%s" % (kname, bn)  # eindeutig je Biom (Statistik, Hash)
                    self.zusatz_lesen(nm, pz, [bn], pk, alt=True, extra=ex)
                    if "flechten" in par:
                        self._i(pk + ".flechten (Materialauflage, nicht Planer)")
                else:
                    self._i(pk)

    def eingraben(self, v, scope, pfad):
        for bn, x in self.je_biom(v, scope, pfad):
            if _spanne(x):
                self.rec[bn]["eingraben"] = [float(x[0]), float(x[1])]
                self._g(pfad)
            else:
                self._i(pfad)

    def rolle_param(self, bn, r, par, pfad):
        for k, x in par.items():
            kk = {"eingraben_anteil": "eingraben", "sichtweite": "sichtweite_cm", "kippen_in_hang_grad": "kippen_grad"}.get(k, k)
            if kk in ("massstab", "eingraben", "sichtweite_cm", "kippen_grad") and _spanne(x):
                self.rec[bn]["rollen"].setdefault(r, {})[kk] = [float(x[0]), float(x[1])]
                self._g("%s.%s" % (pfad, k))
            elif ROLLEN_ALIAS.get(k) is not None or _ist_doku(k):
                continue  # Netzlisten werden separat gelesen
            else:
                self._i("%s.%s" % (pfad, k))

    def rollen(self, v, scope, pfad):
        if not isinstance(v, dict):
            self._i(pfad)
            return
        for k, d in v.items():
            r = ROLLEN_ALIAS.get(k)
            pk = "%s.%s" % (pfad, k)
            if r is None or not isinstance(d, dict):
                if not _ist_doku(k):
                    self._i(pk)
                continue
            for bn, par in self.je_biom(d, scope, pk):
                if isinstance(par, dict):
                    self.rolle_param(bn, r, par, pk)

    def je_rolle_spanne(self, v, scope, pfad, kk):
        for bn, d in self.je_biom(v, scope, pfad):
            if not isinstance(d, dict):
                self._i(pfad)
                continue
            for k, x in d.items():
                r = ROLLEN_ALIAS.get(k)
                if r is None or not _spanne(x):
                    if not _ist_doku(k):
                        self._i("%s.%s" % (pfad, k))
                    continue
                self.rec[bn]["rollen"].setdefault(r, {})[kk] = [float(x[0]), float(x[1])]
                self._g("%s.%s" % (pfad, k))

    def kiesel_dichte(self, x, scope, pfad):
        f = None
        if _spanne(x):
            f = 0.5 * (x[0] + x[1]) / self.kiesel_basis
        elif _zahl(x):
            f = float(x) / self.kiesel_basis
        if f is None:
            self._i(pfad)
            return
        for bn in scope:
            self.rec[bn]["kiesel_faktor"] = f
        self._g(pfad + " (-> Kieselfaktor %.2f)" % f)

    def mindest(self, v, scope, pfad):
        for bn, x in self.je_biom(v, scope, pfad):
            w = float(x) if _zahl(x) else (0.5 * (x[0] + x[1]) if _spanne(x) else None)
            if w is None:
                self._i(pfad)
                continue
            self.rec[bn]["mindestdichte_je_ha"] = max(0.0, w)
            self._g(pfad)

    def zusatz_lesen(self, name, d, scope, pfad, alt=False, extra=None):
        """Zusatzklasse (KONVENTIONEN §6) tolerant normalisieren; abweichende Schlüssel, wo eindeutig, auf das Schema abbilden.
        alt=True: aus einer Altstelle (nicht unter 'zusatzklassen') abgeleitet."""
        if not isinstance(d, dict):
            self._i(pfad)
            return
        if extra:
            d = dict(d, **{k: v for k, v in extra.items() if k not in d})
        if d.get("aktiv") is False:
            self._g(pfad + " (aktiv=false, nicht gesetzt)")
            return
        z = {"name": name, "datei": self.datei, "pfad": pfad, "alt": alt, "biome": {bn: 1.0 for bn in scope},
             "palette": [], "palette_rollen": None, "rolle": "block", "dichte_je_ha": None, "dichte_bezug": "maske",
             "hang": None, "hoehe": None, "wasser": None, "meer_nur": False, "lagen_min": {}, "lagen_gewicht": {},
             "kruemmung": "egal", "massstab": None, "eingraben": None, "gruppe_n": (1, 1), "gruppe_r": None,
             "kollision": None, "sichtweite": None, "schatten": None, "akteur": False, "raster_m": None, "klumpung": None,
             "wand_abstand": None, "relief": None, "kuppe_prominenz_m": None, "exposition": None, "max_je_feld": None,
             "punkte": None, "felder": None, "zonen": None, "fuss_m": 22.0, "dichte_gruppen": False, "z_versatz": None, "gelesen": [], "ignoriert": []}
        G, I = z["gelesen"].append, z["ignoriert"].append
        hang_lo = hang_hi = p_alt = abstand = umkreis = abbruch = None
        for k, v in d.items():
            if _ist_doku(k) or k == "aktiv":
                continue
            if k in ("palette", "netze"):
                lst = [p for l in v.values() if isinstance(l, list) for p in l] if isinstance(v, dict) else v
                z["palette"] = self.pfade(lst)
                G(k)
            elif k == "palette_rollen" and isinstance(v, list):
                z["palette_rollen"] = [ROLLEN_ALIAS[r] for r in v if r in ROLLEN_ALIAS]
                G(k)
            elif k == "rolle" and isinstance(v, str):
                if v == "akteur":
                    z["akteur"], z["rolle"] = True, "hero"
                elif v in ZK_ROLLEN:
                    z["rolle"] = ZK_ROLLEN[v]
                else:
                    I("rolle=%s (-> block)" % v)
                    continue
                G(k)
            elif k == "dichte_je_ha" and _mittel(v) is not None:
                z["dichte_je_ha"] = _mittel(v)
                G(k)
            elif k in ("dichte", "dichte_je_m2", "dichte_block_je_m2") and _mittel(v) is not None:
                z["dichte_je_ha"] = _mittel(v) * 1e4
                G(k + " (je m2 -> je ha)")
            elif k == "je_km2" and _mittel(v) is not None:
                z["dichte_je_ha"], z["dichte_bezug"], z["dichte_gruppen"] = _mittel(v) / 100.0, "biom", True
                G(k + " (Gruppen je km2 Biomflaeche)")
            elif k in ("hang_grad", "hang") and _trapez_spec(v):
                z["hang"] = _trapez_spec(v)
                G(k)
            elif k == "hang_min" and (_spanne(v) or _zahl(v)):
                hang_lo = (v[0], v[1]) if _spanne(v) else (v, v)
                G(k)
            elif k in ("hang_max", "hang_max_grad") and _zahl(v):
                hang_hi = float(v)
                G(k)
            elif k == "hoehe_m" and _trapez_spec(v):
                z["hoehe"] = _trapez_spec(v)
                G(k)
            elif k == "hoehe" and _spanne(v):
                z["hoehe"] = (-1e5, -1e5, float(v[0]), float(v[1]))
                G(k + " (voll bis a, 0 bei b)")
            elif k == "ab_hoehe_m" and _zahl(v):
                z["hoehe"] = (float(v), float(v), 1e5, 1e5)
                G(k)
            elif k == "wasser_abstand_m" and _trapez_spec(v):
                z["wasser"] = _trapez_spec(v)
                G(k)
            elif k == "kueste" and _trapez_spec(v):
                z["wasser"], z["meer_nur"] = _trapez_spec(v), True
                G(k + " (-> wasser_abstand_m zum Meer)")
            elif k == "kueste_nur":
                z["meer_nur"] = bool(v)
                G(k)
            elif k == "lagen_min" and isinstance(v, dict):
                z["lagen_min"] = {l: float(x) for l, x in v.items() if _zahl(x)}
                G(k)
            elif k == "lagen" and isinstance(v, dict) and d.get("lagen_modus", "gewicht") == "gewicht":
                z["lagen_gewicht"] = {l: float(x) for l, x in v.items() if _zahl(x)}
                G(k + " (gewicht)")
            elif k == "lagen_modus":
                continue
            elif k == "kruemmung" and v in ("konvex", "konkav", "egal"):
                z["kruemmung"] = v
                G(k)
            elif k == "massstab" and _spanne(v):
                z["massstab"] = [float(v[0]), float(v[1])]
                G(k)
            elif k in ("eingraben_anteil", "eingraben"):
                x = v.get("anteil") if isinstance(v, dict) else v
                if _spanne(x):
                    z["eingraben"] = [float(x[0]), float(x[1])]
                elif _zahl(x):
                    z["eingraben"] = [float(x), float(x)]
                else:
                    I(k)
                    continue
                G(k)
            elif k == "gruppe" and isinstance(v, dict):
                for kk, x in v.items():
                    if kk == "groesse" and (_spanne(x) or _zahl(x)):
                        z["gruppe_n"] = (int(x[0]), int(x[1])) if _spanne(x) else (int(x), int(x))
                        G("gruppe.groesse")
                    elif kk == "radius_m" and _zahl(x):
                        z["gruppe_r"] = float(x)
                        G("gruppe.radius_m")
                    elif not _ist_doku(kk):
                        I("gruppe." + kk)
            elif k == "block" and _spanne(v) and alt:
                z["gruppe_n"] = (int(v[0]), int(v[1]))
                G(k + " (-> gruppe.groesse)")
            elif k == "hero_p" and alt and _zahl(v):
                G(k + " (-> Netze hero+block der Biom-Palette)" if v >= 0.5 else k + " (< 0,5: nur block)")
            elif k in ("stein", "kiesel") and alt and _spanne(v):
                I("%s (Kleinzeug-Saum je Gruppe: nicht im Schema §6)" % k)
            elif k in ("kollision", "schatten", "akteur") and isinstance(v, bool):
                z[k] = v
                G(k)
            elif k == "sichtweite" and _spanne(v):
                z["sichtweite"] = [float(v[0]), float(v[1])]
                G(k)
            elif k == "raster_m" and _zahl(v):
                z["raster_m"] = float(v)
                G(k)
            elif k == "p" and _zahl(v):
                p_alt = float(v)
                G(k + " (mit raster_m -> dichte)")
            elif k == "klumpung" and isinstance(v, dict) and _zahl(v.get("skala_m")):
                z["klumpung"] = (float(v["skala_m"]), float(v.get("staerke", 0.6)), float(v.get("schwelle", 0.3)))
                G(k)
            elif k in ("zonen_faktor", "karst_faktor") and isinstance(v, dict):
                z["zonen"] = {zk: float(x) for zk, x in v.items() if zk in ("wand", "fuss", "gipfel", "spalte", "sonst") and _zahl(x)}
                for zk in v:
                    if zk not in ("wand", "fuss", "gipfel", "spalte", "sonst"):
                        I("%s.%s" % (k, zk))
                G(k + " (-> zonen_faktor)")
            elif k == "z_versatz_anteil" and (_zahl(v) or _spanne(v)):
                z["z_versatz"] = [float(v), float(v)] if _zahl(v) else [float(v[0]), float(v[1])]
                G(k)
            elif k == "fuss_breite_m" and _zahl(v):
                z["fuss_m"] = float(v)
                G(k)
            elif k in ("wand_abstand_m", "zone_m") and _trapez_spec(v):
                z["wand_abstand"] = _trapez_spec(v)
                G(k + " (-> Abstand zur Wand)")
            elif k == "abstand_m" and _mittel(v) is not None:
                abstand = _mittel(v)
                G(k)
            elif k == "umkreis_m" and _zahl(v):
                umkreis = float(v)
                G(k)
            elif k == "abbruch_min_m" and _zahl(v):
                abbruch = float(v)
                G(k)
            elif k in ("kuppen_prominenz_min_m", "kuppen_prominenz_m") and _zahl(v):
                z["kuppe_prominenz_m"] = float(v)
                G(k)
            elif k == "exposition" and v in ("nord", "sued", "ost", "west"):
                z["exposition"] = v
                G(k)
            elif k == "max_je_feld" and _zahl(v):
                z["max_je_feld"] = int(v)
                G(k)
            elif k == "punkte" and isinstance(v, dict):
                z["punkte"] = v
                G(k)
            elif k == "felder" and isinstance(v, list):
                z["felder"] = [str(f).strip().upper() for f in v]
                G(k)
            elif k == "biome" and isinstance(v, dict):
                z["biome"] = {bn: float(x) for bn, x in v.items() if bn in scope and _zahl(x)}
                G(k)
            else:
                I(k)
        if hang_lo or hang_hi is not None:
            t = z["hang"] or (0.0, 0.0, 90.0, 90.0)
            if hang_lo:
                t = (float(hang_lo[0]), float(hang_lo[1]), t[2], t[3])
            if hang_hi is not None:
                t = (t[0], t[1], min(t[2], hang_hi), min(t[3], hang_hi))
            z["hang"] = t
        if abbruch is not None:
            z["relief"] = (umkreis or 6.0, abbruch)
        if abstand and z["dichte_je_ha"] is None:  # Kantenstücke: ein Stück je abstand_m auf einem Streifen 2 * umkreis
            z["dichte_je_ha"] = 1e4 / (abstand * 2.0 * (umkreis or 6.0))
            G("abstand_m (-> dichte_je_ha %.0f im Kantenstreifen)" % z["dichte_je_ha"])
        if p_alt is not None and z["raster_m"] and z["dichte_je_ha"] is None:
            z["dichte_je_ha"] = p_alt * 1e4 / z["raster_m"] ** 2 * 0.5 * sum(z["gruppe_n"])
        if z["gruppe_r"] is None:
            z["gruppe_r"] = 0.5 * z["raster_m"] if (z["raster_m"] and z["gruppe_n"][1] > 1) else 4.0
        if not z["palette"] and not z["palette_rollen"]:
            I("palette fehlt (Pflicht) -> Klasse verworfen")
            self._i(pfad + " (Zusatzklasse ohne palette)")
            self.zusatz.append(dict(z, verworfen=True))
            return
        if z["dichte_je_ha"] is None and not z["punkte"]:
            z["dichte_je_ha"] = 1.0
            I("dichte fehlt -> 1 je ha")
        if not any(x > 0 for x in z["biome"].values()):
            I("keine Biome mit Gewicht > 0 -> nicht gesetzt")
        self._g(pfad + " (Zusatzklasse)")
        self.zusatz.append(z)

    def lies(self, block, scope=None, pfad=""):
        scope = list(scope or self.biome)
        if not isinstance(block, dict):
            self._i(pfad or "(kein JSON-Objekt)")
            return
        bio = block.get("biom")
        if isinstance(bio, str):
            if bio in scope:
                scope = [bio]
                self._g((pfad + "." if pfad else "") + "biom")
            else:
                self.fremd.append((pfad + "." if pfad else "") + "biom=" + bio)
                return
        bed = block.get("bedingung")
        if isinstance(bed, dict):
            pb = (pfad + "." if pfad else "") + "bedingung"
            if isinstance(bed.get("biom"), str) and bed["biom"] in scope:
                scope = [bed["biom"]]
                self._g(pb + ".biom")
            for k in bed:
                if k != "biom":
                    self._i("%s.%s" % (pb, k))
        for k, v in block.items():
            p = (pfad + "." if pfad else "") + k
            if k in BIOME and isinstance(v, dict):
                if k in scope:
                    self.lies(v, [k], p)
                else:
                    self.fremd.append(p)
                continue
            if _ist_doku(k):
                continue
            if k == "zusatzklassen" and isinstance(v, dict):
                for name, zd in v.items():
                    if not _ist_doku(name):
                        self.zusatz_lesen(name, zd, scope, "%s.%s" % (p, name))
                continue
            if k == "karstfuss" and isinstance(v, dict):  # Altstelle dschungel: Moosblöcke am Karstfuß, Netze = fels_block des Blocks
                self.zusatz_lesen(k, v, scope, p, alt=True, extra={
                    "palette": block.get("fels_block", []), "rolle": "fels_block", "kruemmung": "egal",
                    "gruppe": {"groesse": [1, 3], "radius_m": 3}})
                continue
            if k == "hero_akteure" and isinstance(v, list):  # Altstelle lava: Spires als Akteure an Punkten des Lava-Planers
                sp = (self.datei_json.get("punkte") or {}).get("spire_vorschlag") or {}
                ex = {"palette": v, "rolle": "akteur", "punkte": {"ebene": "lava", "typ": "spire_vorschlag"},
                      "hang_max_grad": sp.get("hang_max_grad", 18), "kuppen_prominenz_m": sp.get("kuppen_prominenz_m", 6),
                      "max_je_feld": sp.get("max_je_feld", 6), "je_km2": sp.get("max_je_feld", 6), "lagen_min": {"Lavafels": 128},
                      "eingraben_anteil": block.get("eingraben", [0.3, 0.45]), "kollision": True}
                self.zusatz_lesen("spire", ex, scope, p, alt=True)
                continue
            if k == "hero_akteur_punkte":
                self._g(p + " (-> spire.punkte)")
                continue
            if k in ("palette", "biom_palette"):
                self.palette(v, scope, p)
            elif k in ("paletten_neu", "paletten"):
                self.paletten_tabelle(v, scope, p, "paletten_neu")
            elif k in ("paletten_ergaenzung", "paletten_zusatz", "palette_zusatz"):
                self.paletten_tabelle(v, scope, p, "palette_zusatz")
            elif k in ROLLEN_ALIAS and isinstance(v, list):
                self.rollen_palette({k: v}, scope, pfad)
            elif k == "wand_palette" and isinstance(v, dict):
                self.rollen_palette({kk: x for kk, x in v.items() if kk in ROLLEN_ALIAS}, scope, p)
                for bn in scope:
                    self.rolle_param(bn, "wand", {kk: x for kk, x in v.items() if kk not in ROLLEN_ALIAS}, p)
            elif k == "kiesel_ring" and isinstance(v, dict):
                for kk, x in v.items():
                    if kk == "netze":
                        self.rollen_palette({"kiesel": x}, scope, p + ".netze->")
                    elif kk == "kiesel_dichte_je_m2":
                        self.kiesel_dichte(x, scope, p + "." + kk)
                    elif not _ist_doku(kk):
                        self._i("%s.%s" % (p, kk))
            elif k == "kontaktzone" and isinstance(v, dict):
                for kk, x in v.items():
                    if kk == "geroellsaum_netze":
                        self.rollen_palette({kk: x}, scope, p)
                    elif not _ist_doku(kk):
                        self._i("%s.%s" % (p, kk))
            elif k in ("faktor", "faktoren", "biom_faktor"):
                self.faktor(v, scope, p)
            elif k.startswith("biom_faktor_") and _zahl(v):
                bn = k[len("biom_faktor_"):]
                if bn in scope:
                    self.rec[bn]["faktor"] = float(v)
                    self._g(p)
                else:
                    self._i(p)
            elif k in ("gruppen_dichte_faktor", "dichte_faktor") and _zahl(v):
                for bn in scope:
                    self.rec[bn]["faktor_mult"] *= float(v)
                self._g(p)
            elif k == "klassen_faktor":
                self.klassen_faktor(v, scope, p)
            elif k in ("biom_klassen_aus", "klassen_aus"):
                self.klassen_aus(v, scope, p)
            elif k == "klassen_erlaubt":
                self.klassen_aus(v, scope, p, erlaubt=True)
            elif k == "klassen":
                self.klassen(v, scope, p)
            elif k in ("eingraben", "eingraben_anteil"):
                self.eingraben(v, scope, p)
            elif k == "rollen":
                self.rollen(v, scope, p)
            elif k == "massstab" and isinstance(v, dict):
                self.je_rolle_spanne(v, scope, p, "massstab")
            elif k == "sichtweite" and isinstance(v, dict):
                self.je_rolle_spanne(v, scope, p, "sichtweite_cm")
            elif k == "kiesel_dichte_faktor":
                for bn, x in self.je_biom(v, scope, p):
                    if _zahl(x):
                        self.rec[bn]["kiesel_faktor"] = float(x)
                        self._g(p)
            elif k == "gruppe" and isinstance(v, dict):
                for kk, x in v.items():
                    if kk == "kiesel_dichte_je_m2":
                        self.kiesel_dichte(x, scope, p + "." + kk)
                    elif not _ist_doku(kk):
                        self._i("%s.%s" % (p, kk))
            elif k == "mindestdichte_je_ha":
                self.mindest(v, scope, p)
            elif k == "mindestdichte_klassen" and isinstance(v, list):
                rl = [ROLLEN_ALIAS[x] for x in v if x in ROLLEN_ALIAS]
                for bn in scope:
                    self.rec[bn]["einzel_rollen"] = rl
                self._g(p)
            elif k == "felder" and isinstance(v, list):
                for bn in scope:
                    self.rec[bn]["felder"] = [str(f).strip().upper() for f in v]
                self._g(p)
            elif isinstance(v, dict) and (isinstance(v.get("netze"), list) or isinstance(v.get("palette"), list)):
                # Altstelle mit eigener Netzliste; Rolle nur, wo die Quelle sie eindeutig nennt
                ex = {}
                if isinstance(v.get("karst_faktor"), dict):  # dschungel karstplatte: Zonen laut karst_faktor, Fussbreite = karstfuss.zone_m
                    zm = (block.get("karstfuss") or {}).get("zone_m")
                    if _spanne(zm):
                        ex["fuss_breite_m"] = float(zm[1])
                    if "sonst" not in v["karst_faktor"] and "Karstfu" in str(v.get("_doku", "")):
                        ex["zonen_faktor"] = dict(v["karst_faktor"], sonst=0.0)  # nach karst_faktor gelesen  # _doku: "Platten am Karstfuss" -> uebrige Flaeche 0
                if "rolle" not in v:
                    if "platte" in k or "geroell_platte" in str(v.get("_doku", "")):
                        ex["rolle"] = "geroell_platte"          # dschungel karstplatte: "Jetzt Teil C (geroell_platte)"
                    elif "akteur" in str(v.get("hinweis", "")).lower():
                        ex["rolle"] = "akteur"                  # wueste felsnadel: "Blickziel ... als Akteur"
                self.zusatz_lesen(k, v, scope, p, alt=True, extra=ex)
            elif k == "auflage":
                self._i(p + " (Materialauflage, nicht Planer)")
            else:
                self._i(p)

    def ergebnis(self):
        """Nur Biome mit tatsächlichen Abweichungen; mindest_findling greift, wenn mindestdichte_je_ha nicht gesetzt ist."""
        out = {}
        for bn, r in self.rec.items():
            if r["mindestdichte_je_ha"] is None and r["mindest_findling"] is not None:
                r["mindestdichte_je_ha"] = r["mindest_findling"]
            if any(r[k] not in (None, {}, 1.0) for k in r if k != "mindest_findling"):
                out[bn] = r
        return out


def gesperrte_netze(R):
    """Sperrliste aus felsgruppen_regeln.json["gesperrt"]["netze"] (Korrektur Runde 2): normierte Paketpfade."""
    g = R.get("gesperrt", {})
    liste = g.get("netze", []) if isinstance(g, dict) else g
    return set(norm_pfad(p) for p in liste if isinstance(p, str))


def lade_overrides(R, regeln_pfad, basis, skriptdir, ordner, netze):
    """Liest felsgruppen_overrides aller Biom-Regeldateien (Zuordnung R["overrides"]["dateien"]). Fehlende Datei -> Hinweis."""
    O = R.get("overrides", {})
    if not O.get("aktiv", True):
        log("Overrides: in felsgruppen_regeln.json abgeschaltet (overrides.aktiv = false).")
        return {}, {}, []
    schl = O.get("schluessel", "felsgruppen_overrides")
    alle, info, zusatz = {}, {}, []
    for datei, biome in O.get("dateien", {}).items():
        if datei.startswith("_"):
            continue
        thema = datei[:-len("_regeln.json")] if datei.endswith("_regeln.json") else os.path.splitext(datei)[0]
        kand = []
        if ordner:
            kand.append(os.path.join(ordner, datei))
        if regeln_pfad:
            kand.append(os.path.join(os.path.dirname(os.path.abspath(regeln_pfad)), datei))
        kand += [os.path.join(basis, "scripts", thema, datei), os.path.join(skriptdir, "..", thema, datei)]
        pfad = next((p for p in kand if os.path.isfile(p)), None)
        if pfad is None:
            log("Hinweis: %s fehlt (gesucht in %d Ordnern) - Biome %s ohne Overrides." % (datei, len(kand), ",".join(biome)))
            info[datei] = {"biome": biome, "status": "Datei fehlt"}
            continue
        try:
            with open(pfad, encoding="utf-8") as f:
                ganz_json = json.load(f)
            block = ganz_json.get(schl)
        except Exception as e:
            log("Hinweis: %s unlesbar (%s) - Biome %s ohne Overrides." % (pfad, e, ",".join(biome)))
            info[datei] = {"biome": biome, "status": "unlesbar"}
            continue
        if not block:
            log("Hinweis: %s ohne Block '%s' - Biome %s ohne Overrides." % (datei, schl, ",".join(biome)))
            info[datei] = {"biome": biome, "status": "kein Block %s" % schl}
            continue
        L = OverrideLeser(R, datei, biome, netze)
        L.datei_json = ganz_json
        L.lies(block)
        erg = L.ergebnis()
        alle.update(erg)
        felder_block = block.get("felder") if isinstance(block.get("felder"), list) else None
        echt = {z["name"] for z in L.zusatz if not z["alt"]}
        doppelt = [z for z in L.zusatz if z["alt"] and z["name"] in echt]
        if doppelt:  # gleiche Klasse unter zusatzklassen und an einer Altstelle: zusatzklassen gewinnt
            log("  Hinweis: %s: Altstelle(n) %s durch zusatzklassen ersetzt." % (datei, ",".join(z["name"] for z in doppelt)))
            L.zusatz = [z for z in L.zusatz if z not in doppelt]
        for z in L.zusatz:
            if felder_block and not z.get("felder"):
                z["felder"] = [str(f).strip().upper() for f in felder_block]
            zusatz.append(z)
            log("  Zusatzklasse %s/%s%s: %s; Biome %s; gelesen %d, ignoriert %d%s" % (
                datei, z["name"], " (Altstelle)" if z["alt"] else "", "VERWORFEN" if z.get("verworfen") else "ok",
                ",".join("%s %.1f" % kv for kv in z["biome"].items()), len(z["gelesen"]), len(z["ignoriert"]),
                (" [" + ", ".join(z["ignoriert"])[:200] + "]") if z["ignoriert"] else ""))
        if L.gesperrt_treffer:
            log("  Hinweis: %s: %d Verweise auf gesperrte Netze entfernt (%s)." % (
                datei, len(L.gesperrt_treffer), ", ".join(sorted(set(p.rsplit("/", 1)[-1] for p in L.gesperrt_treffer)))))
        info[datei] = {"biome": biome, "status": "gelesen", "biome_mit_aenderung": sorted(erg), "gelesen": L.gelesen,
                       "gesperrt_entfernt": sorted(set(L.gesperrt_treffer)),
                       "ignoriert": L.ignoriert, "fremde_biome_ignoriert": L.fremd, "fehlende_netzpfade": L.fehlpfade,
                       "zusatzklassen": {z["name"]: {"altstelle": z["alt"], "verworfen": bool(z.get("verworfen")),
                                                     "gelesen": z["gelesen"], "ignoriert": z["ignoriert"]} for z in L.zusatz}}
        log("Overrides %s -> %s: gelesen %d Schluessel, ignoriert %d%s%s" % (
            datei, ",".join(sorted(erg)) or "(keine Aenderung)", len(L.gelesen), len(L.ignoriert),
            (", %d Netzpfade nicht im Inventar (verworfen)" % len(L.fehlpfade)) if L.fehlpfade else "",
            (", fremde Biome ignoriert: %s" % ",".join(L.fremd)[:120]) if L.fremd else ""))
        if L.ignoriert:
            log("  ignoriert: %s" % ", ".join(L.ignoriert)[:400])
    return alle, info, zusatz


# ----------------------------------------------------------------------------------------------------------------------
# Planer
# ----------------------------------------------------------------------------------------------------------------------
class Planer:
    def __init__(self, regeln, netze, masse, basis, faktor, skriptdir=".", overrides=None, ov_info=None, zusatz=None):
        self.R = regeln
        self.skriptdir = skriptdir
        self.netze = netze
        self.masse = masse
        self.basis = basis
        self.faktor = faktor
        self.seed = int(regeln.get("seed", 1))
        self.pivot_mitte = set(regeln.get("netz_pivot_mitte", []))
        self.pal_info = {}
        self.ov = overrides or {}
        self.ov_info = ov_info or {}
        self.zusatz = [z for z in (zusatz or []) if not z.get("verworfen")]
        self.stand = "regeln %s" % regeln.get("_doku", {}).get("stand", "?")  # deterministisch (kein Zeitstempel)
        # Sperrliste (Runde 2, Befund 3): gesperrte Netze aus allen Paletten der Grundregeln entfernen (Overrides: OverrideLeser.pfade)
        self.gesperrt = gesperrte_netze(regeln)
        raus = []
        for pal, rollen in regeln["paletten"].items():
            for rolle in list(rollen):
                vor = rollen[rolle]
                rollen[rolle] = [p for p in vor if p not in self.gesperrt]
                raus += [p for p in vor if p in self.gesperrt]
        if self.gesperrt:
            log("Sperrliste: %d Netze gesperrt (%s); aus Grundpaletten entfernt: %d Verweise." % (
                len(self.gesperrt), ", ".join(sorted(p.rsplit("/", 1)[-1] for p in self.gesperrt)), len(raus)))
        fehlend = []
        for pal, rollen in regeln["paletten"].items():
            for rolle, pfade in rollen.items():
                for p in pfade:
                    if p not in netze:
                        fehlend.append(p)
        if fehlend:
            abbruch("%d Paletten-Pfade aus felsgruppen_regeln.json nicht in netze.csv, z. B. %s" % (len(fehlend), fehlend[:3]))

    # Biom-Konfiguration je Feld (Grundregeln + Overrides) --------------------------------------------------------------
    def konfig(self, feld):
        R = self.R
        pal = {k: {r: list(v) for r, v in rollen.items()} for k, rollen in R["paletten"].items()}
        namen = [R["biom_palette"].get(bn, "nordisch") for bn in BIOME]
        bf = np.array([float(R["biom_faktor"].get(bn, 1.0)) for bn in BIOME])
        aus = {bn: set(R.get("biom_klassen_aus", {}).get(bn, [])) for bn in BIOME}
        kf = {bn: {} for bn in BIOME}
        kiesel = np.ones(len(BIOME))
        mind = np.zeros(len(BIOME))
        for bn, v in R.get("mindestdichte_je_ha", {}).items():
            if bn in BIOME and _zahl(v):
                mind[BIOME.index(bn)] = float(v)
        self.rollen_ov = {}
        self.ov_aktiv = {}
        self.einzel_rollen = {}
        self.klassen_ov = {}
        for bn, rec in sorted(self.ov.items()):
            b = BIOME.index(bn)
            if rec["felder"] and feld not in rec["felder"]:
                log("Overrides %s: nur fuer Felder %s - in %s nicht aktiv." % (bn, ",".join(rec["felder"]), feld))
                continue
            for name, rollen in rec["paletten_neu"].items():
                if name not in pal:
                    pal[name] = {r: list(v) for r, v in pal[namen[b]].items()}  # Basis: bisherige Palette des Bioms
                pal[name].update({r: list(v) for r, v in rollen.items()})
            basis = rec["palette_name"] or namen[b]
            if basis not in pal:
                log("Hinweis: Overrides %s: Palette '%s' unbekannt - bleibt '%s'." % (bn, basis, namen[b]))
                basis = namen[b]
            zus = rec["palette_zusatz"].get(basis, {})
            if rec["palette_rollen"] or zus:
                neu = {r: list(v) for r, v in pal[basis].items()}
                for r, v in rec["palette_rollen"].items():
                    neu[r] = list(v)
                for r, v in zus.items():
                    neu[r] = neu.get(r, []) + [p for p in v if p not in neu.get(r, [])]
                namen[b] = basis + "@" + bn
                pal[namen[b]] = neu
            else:
                namen[b] = basis
            if rec["faktor"] is not None:
                bf[b] = rec["faktor"]
            bf[b] *= rec["faktor_mult"]
            kf[bn].update(rec["klassen_faktor"])
            if rec["klassen_aus"] is not None:
                aus[bn] = set(rec["klassen_aus"])
            if rec["kiesel_faktor"] is not None:
                kiesel[b] = rec["kiesel_faktor"]
            if rec["mindestdichte_je_ha"] is not None:
                mind[b] = rec["mindestdichte_je_ha"]
            if rec["einzel_rollen"]:
                self.einzel_rollen[b] = set(rec["einzel_rollen"])
            for kn, par in rec["klassen_param"].items():
                self.klassen_ov[(b, kn)] = dict(par)
            for r, d in rec["rollen"].items():
                self.rollen_ov[(b, r)] = dict(d)
            if rec["eingraben"] is not None:
                for r in ("hero", "wand", "band", "block", "platte", "stein"):
                    self.rollen_ov.setdefault((b, r), {}).setdefault("eingraben", list(rec["eingraben"]))
            self.ov_aktiv[bn] = {"palette": namen[b], "biom_faktor": round(float(bf[b]), 3),
                                 "klassen_faktor": {k: round(v, 3) for k, v in sorted(kf[bn].items())},
                                 "klassen_aus": sorted(aus[bn]), "kiesel_faktor": round(float(kiesel[b]), 3),
                                 "mindestdichte_je_ha": float(mind[b]), "rollen": {"%s" % r: d for (bb, r), d in self.rollen_ov.items() if bb == b},
                                 "klassen_param": {kn: d for (bb, kn), d in self.klassen_ov.items() if bb == b}}
        self.paletten = pal
        self.pal_je_biom = namen
        self.pal_info = {}
        self.bf_klasse = {k: np.array([bf[b] * float(kf[BIOME[b]].get(k, 1.0)) for b in range(len(BIOME))]) for k in KLASSEN}
        self.aus_klasse = {k: np.array([k in aus[bn] for bn in BIOME]) for k in KLASSEN}
        self.kiesel_f = kiesel
        self.mindest = mind

    def klasse_param(self, kname, b):
        """Klassenregel + Biom-Feinparameter aus Overrides (hero_p, block/stein/kiesel/band/wand/n, eingraben)."""
        K = self.R["klassen"][kname]
        o = self.klassen_ov.get((int(b), kname))
        if not o:
            return K
        d = dict(K)
        d.update(o)
        return d

    def rolle_param(self, b, rolle):
        ro = self.R["rollen"][rolle]
        o = self.rollen_ov.get((int(b), rolle))
        if not o:
            return ro
        d = dict(ro)
        d.update(o)
        return d

    # Netz-Kennwerte -------------------------------------------------------------------------------------------------
    def netz_mass(self, pfad):
        n = self.netze[pfad]
        h_cm = n["sz"] * 100.0
        r_cm = 0.5 * max(n["sx"], n["sy"]) * 100.0
        if pfad in self.masse:
            mn, mx = self.masse[pfad]
            minz = mn[2]
            h_cm = mx[2] - mn[2]
            r_cm = 0.5 * max(mx[0] - mn[0], mx[1] - mn[1])
        elif pfad in self.pivot_mitte:
            minz = -0.5 * h_cm
        else:
            minz = 0.0
        return h_cm, r_cm, minz

    def palette_arrays(self, pal, rolle):
        pfade = self.paletten[pal].get(rolle, [])
        if not pfade:
            return None
        key = (pal, rolle)
        if key not in self.pal_info:
            h, r, mz = zip(*[self.netz_mass(p) for p in pfade])
            self.pal_info[key] = (pfade, np.array(h), np.array(r), np.array(mz))
        return self.pal_info[key]

    # Hauptlauf ------------------------------------------------------------------------------------------------------
    def plane_feld(self, feld, welt_dir, bild):
        t0 = time.time()
        R = self.R
        rand = int(R.get("rand_m", 64))
        i0f, i1f, j0f, j1f = feld_bereich(feld)
        win = (max(0, i0f - rand), min(NY, i1f + rand), max(0, j0f - rand), min(NX, j1f + rand))
        i0, i1, j0, j1 = win
        self.win = win
        self.feld_box = (i0f, i1f, j0f, j1f)
        h = lade_raster(os.path.join(welt_dir, "hoehe.f32"), "<f4", win, pflicht=True, name="hoehe.f32").astype(np.float64)
        H, W = h.shape
        self.h = h
        self.hinweise = []
        self.haupt_je_biom = np.zeros(len(BIOME), dtype=np.int64)
        self.konfig(feld)
        self.biom, self.biom_quelle = lade_biome(welt_dir, win, self.basis, self.skriptdir, feld, R)
        ii, jj = np.mgrid[0:H, 0:W]
        self.ii, self.jj = ii, jj
        xg = (jj + j0) - X0  # Welt-m
        yg = (ii + i0) - Y0

        # Masken ---------------------------------------------------------------------------------------------------
        def r8(name):
            a = lade_raster(os.path.join(welt_dir, name), np.uint8, win, name=name)
            return a

        wasser = r8("karte_wasser.r8")
        weg = r8("karte_weg.r8")
        ort = r8("karte_ort.r8")
        A = R["ausschluss"]
        self.m_wasser = dilate(wasser > 0, A["wasser_m"]) if wasser is not None else (h <= 0.05)
        self.m_wasser_roh = (wasser > 0) if wasser is not None else (h <= 0.05)
        self.m_weg = dilate(weg > 0, A["weg_m"]) if weg is not None else np.zeros_like(self.m_wasser)
        self.m_weg_klein = dilate(weg > 0, int(math.ceil(2.5))) if weg is not None else np.zeros_like(self.m_wasser)
        self.m_ort = dilate(ort > 0, A["ort_m"]) if ort is not None else np.zeros_like(self.m_wasser)

        # Lagen (optional) → Faktor (Rasterfenster je Lage nur einmal lesen, Cache auch für Zusatzklassen/Platten)
        self._lage_cache = {}
        self._abst_cache = {}
        lagen = R.get("lagen", {})
        fels = np.zeros_like(h)
        for ln in lagen.get("fels_boost", []):
            a = self.lage(welt_dir, ln)
            if a is not None:
                fels = np.maximum(fels, a / 255.0)
        ger = np.zeros_like(h)
        for ln in lagen.get("geroell_boost", []):
            a = self.lage(welt_dir, ln)
            if a is not None:
                ger = np.maximum(ger, a / 255.0)
        schnee = self.lage(welt_dir, lagen.get("schnee_hemmung", "Schnee"))
        schnee = schnee / 255.0 if schnee is not None else np.zeros_like(h)
        fmin, fmax = lagen.get("faktor_min", 0.5), lagen.get("faktor_max", 1.5)
        self.f_fels = np.clip(0.6 + 0.9 * fels - 0.3 * schnee, fmin, fmax)
        self.f_ger = np.clip(0.7 + 0.8 * ger, fmin, fmax)
        # Platten-Regel (Runde 2): flache Platten nur auf Kies/Geroell/Fels/Felsplatte >= lagen_min, Gras/Wiese nicht ueberwiegend
        P = R.get("platten", {})
        self.platten_rollen = set(P.get("rollen", ["platte"]))
        self.platten_verworfen = 0
        self.form_rueckfall = {}
        self._ninfo, self._kand, self._platte_pfad = {}, {}, {}
        stein = None
        for ln in P.get("lagen", ["Kies", "Geroell", "Fels", "Felsplatte"]):
            a = self.lage(welt_dir, ln)
            if a is not None:
                stein = a if stein is None else np.maximum(stein, a)
        gras = None
        for ln in P.get("vorrang_gegen", ["Gras", "Wiese"]):
            a = self.lage(welt_dir, ln)
            if a is not None:
                gras = a if gras is None else np.maximum(gras, a)
        lmin = float(P.get("lagen_min", 100))
        if stein is None:
            self.m_platte = np.zeros(h.shape, dtype=bool)
            log("Hinweis: keine der Lagen %s vorhanden - keine Platten (Platten-Regel)." % ",".join(P.get("lagen", [])))
            self.hinweise.append("Platten-Regel: keine Kies/Geroell/Fels-Lage vorhanden -> keine Platten")
        else:
            self.m_platte = (stein >= lmin) & ((gras is None) | (stein >= (gras if gras is not None else 0)))
        self.m_gras = ((gras >= lmin) if gras is not None else np.zeros(h.shape, dtype=bool)) & ~(
            (stein >= lmin) if stein is not None else np.zeros(h.shape, dtype=bool))

        # Vorhandene Ebenen (Abstand) --------------------------------------------------------------------------------
        sperr = np.zeros_like(self.m_wasser)
        bst = lade_positionen_f32(os.path.join(welt_dir, "bestand", feld))
        if bst is None:
            log("Hinweis: bestand/%s/ fehlt – kein Baumabstand geprüft." % feld)
        else:
            sperr |= sperrmaske(win, bst, A["baum_m"])
            log("Bestand: %d Baum-Instanzen als Sperre (%.1f m)" % (len(bst[0]), A["baum_m"]))
        fs = os.path.join(welt_dir, "felsschalen", "plan_%s.json" % feld)
        if os.path.isfile(fs):
            pos = []
            try:
                with open(fs, encoding="utf-8") as f:
                    positionen_aus_json(json.load(f), pos)
            except Exception as e:
                log("Hinweis: felsschalen/plan_%s.json unlesbar (%s)." % (feld, e))
            if pos:
                p = np.array(pos)
                sperr |= sperrmaske(win, (p[:, 0], p[:, 1]), A["felsschale_m"])
                log("Felsschalen: %d Positionen aus plan_%s.json als Sperre (%.0f m)" % (len(pos), feld, A["felsschale_m"]))
            else:
                log("Hinweis: felsschalen/plan_%s.json ohne erkennbare Positionen (x/y) – keine Sperre." % feld)
        else:
            log("Hinweis: felsschalen/plan_%s.json fehlt – kein Abstand zu Felsschalen geprüft." % feld)
        self.m_sperr = sperr

        # Gelände-Ableitungen -----------------------------------------------------------------------------------------
        G = R["glaettung"]
        h1 = gauss(h, G["hang_sigma_m"])
        gy, gx = np.gradient(h1)
        gmag = np.hypot(gx, gy)
        self.hang = np.degrees(np.arctan(gmag))
        nz = 1.0 / np.sqrt(1.0 + gmag ** 2)
        self.normal = np.stack([-gx * nz, -gy * nz, nz], axis=2)
        gm = np.where(gmag > 1e-6, gmag, 1.0)
        self.abfall = np.stack([-gx / gm, -gy / gm], axis=2)  # Einheitsvektor hangabwärts (x,y)
        hs = gauss(h, G["kruemmung_sigma_m"])
        lam1, lam2, theta1 = hessian(hs)
        self.grat = -lam2  # > 0 konvex (Grat/Nase)
        self.mulde = lam1  # > 0 konkav (Rinne/Mulde)
        self.gratachse = theta1
        self.hs8 = hs
        hs25 = gauss(h, G["massiv_sigma_m"])
        self.hs25 = hs25
        l1b, l2b, _ = hessian(hs25)
        self.hohl25 = l1b + l2b  # Laplace grob: > 0 Hangfuß/Mulde
        hs12 = gauss(h, G["kuppe_sigma_m"])
        self.hs12 = hs12
        self.land = h > 0.2
        # Biom-Anteile im Fenster (Landzellen; KONVENTIONEN §2)
        bl = self.biom[self.land]
        if bl.size:
            cnt = np.bincount(bl.astype(np.int64), minlength=len(BIOME)) / float(bl.size)
            self.biome_fenster = {BIOME[i]: round(float(cnt[i]), 4) for i in np.argsort(-cnt) if cnt[i] > 0}
        else:
            self.biome_fenster = {}
        log("Biome im Fenster (Land, Quelle %s): %s" % (self.biom_quelle, ", ".join(
            "%s %.1f%%" % (k, 100 * v) for k, v in self.biome_fenster.items()) or "kein Land"))
        for bn in self.biome_fenster:
            if bn in self.ov_aktiv:
                o = self.ov_aktiv[bn]
                log("  %s: Palette %s, Biomfaktor %.2f, Klassen aus %s, Mindestdichte %.2f/ha (Overrides)" % (
                    bn, o["palette"], o["biom_faktor"], ",".join(o["klassen_aus"]) or "-", o["mindestdichte_je_ha"]))

        # Wände und Schuttfächer
        K = R["klassen"]
        wand = self.hang >= K["fuss"]["wand_ab_grad"]
        relief = boxmax(hs, 12) - boxmin(hs, 12)
        grosse_wand = wand & (relief >= K["fuss"]["wand_hoehe_min_m"])
        wand_h = np.where(grosse_wand, h, -np.inf)
        self.fuss_stufe = np.full(h.shape, -1, dtype=np.int8)
        for si, st in reversed(list(enumerate(K["fuss"]["stufen"]))):
            d = int(st[1])
            oben = boxmax(wand_h, d) > h + 2.0
            self.fuss_stufe[oben] = si
        self.wand_ueber_128 = boxmax(wand_h, K["blockstrom"]["wand_umkreis_m"]) > h + K["blockstrom"]["wand_hoehe_min_m"]
        wand_nah = boxmax(wand_h, A["mulde_wand_umkreis_m"]) > h + A["mulde_wand_hoehe_min_m"]
        self.m_mulde = (self.mulde > A["mulde_staerke_min"]) & (~wand_nah)
        self.m_wand = wand
        self.xg, self.yg = xg, yg

        # Schichtung je Bergmassiv (Strike/Dip)
        S = R["schichtung"]
        st = wertrauschen(xg, yg, S["gitter_m"], self.seed, 1) * 2 * np.pi
        dip = np.radians(S["dip_grad"][0] + (S["dip_grad"][1] - S["dip_grad"][0]) * wertrauschen(xg, yg, S["gitter_m"], self.seed, 2))
        abst = S["band_abstand_m"][0] + (S["band_abstand_m"][1] - S["band_abstand_m"][0]) * wertrauschen(xg, yg, S["gitter_m"], self.seed, 3)
        self.strike, self.dip = st, dip
        phase = (hs - np.tan(dip) * (xg * np.cos(st) + yg * np.sin(st))) / abst
        self.m_band = (phase - np.floor(phase)) < S["band_breite_anteil"]

        # Allgemeine Ausschlüsse
        self.m_frei = self.land & ~self.m_wasser & ~self.m_weg & ~self.m_ort & (self.hang <= A["max_hang_grad"])
        self.m_frei_klein = self.land & ~self.m_wasser & ~self.m_weg_klein & ~self.m_ort & (self.hang <= A["max_hang_grad"])
        fs_i, fs_j = slice(i0f - i0, i1f - i0), slice(j0f - j0, j1f - j0)
        self.feld_slice = (fs_i, fs_j)
        self.zellen_zustaendig = int(self.m_frei[fs_i, fs_j].sum())
        if not self.land[fs_i, fs_j].any():
            log("%s: kein Land im Feld - leerer plan.json." % feld)
            self.hinweise.append("kein Land im Feld")
            leer = self.zusammenfuehren([])
            self.statistik = {}
            self.schreiben(feld, leer, welt_dir)
            return leer

        # Gruppen je Klasse -------------------------------------------------------------------------------------------
        inst = []  # Liste von dicts mit Arrays
        self.statistik = {}
        gruppen_gesamt = 0
        self._kuppen = self.kandidaten_kuppe()  # vor dem Grat: Kuppen haben Vorrang vor Kettengliedern
        for kname in KLASSEN:  # "einzel" zuletzt: füllt nur bis mindestdichte_je_ha auf
            if kname == "prallhang":
                g = self.kandidaten_prallhang(welt_dir)
            elif kname == "kuppe":
                g = self._kuppen
            elif kname == "grat":
                g = self.kandidaten_kamm()
            elif kname == "fuss":
                g = self.kandidaten_strom()
            elif kname == "einzel":
                g = self.kandidaten_einzel()
            else:
                g = self.kandidaten_gitter(kname)
            if g is None or len(g["ci"]) == 0:
                self.statistik[kname] = {"gruppen": 0}
                continue
            n_vor = len(g["ci"])
            teile = self.gruppe_erzeugen(kname, g)
            n_inst = int(sum(len(t["x"]) for t in teile))
            self.statistik[kname] = {"gruppen": n_vor, "instanzen": n_inst}
            gruppen_gesamt += n_vor
            inst.extend(teile)
        # Zusatzklassen der Biom-Planer (KONVENTIONEN §6): nur Zellen des liefernden Bioms + 30-m-Saum, gemeinsames Budget
        self.zusatz_stat = {}
        for z in self.zusatz:
            if z["felder"] and feld not in z["felder"]:
                continue
            t, n_g = self.zusatz_erzeugen(z, feld, welt_dir)
            self.zusatz_stat["%s/%s" % (z["datei"].replace("_regeln.json", ""), z["name"])] = {
                "gruppen": int(n_g), "instanzen": int(len(t["x"])) if t is not None else 0}
            if t is not None and len(t["x"]):
                inst.append(t)
                gruppen_gesamt += n_g
        alle = self.zusammenfuehren(inst)
        alle = self.budget(alle)
        alle = self.kontaktsaum(alle)
        self.form_statistik(alle)
        self.pruefkameras(alle)
        t1 = time.time()
        self.schreiben(feld, alle, welt_dir)
        if bild:
            self.bild(feld, alle)
        log("%s: %d Gruppen, %d Instanzen (%d mit Kollision, %d Akteure) in %.1f s (Planung %.1f s)" % (
            feld, gruppen_gesamt, len(alle["x"]), int(alle["koll"].sum()), int(alle["akteur"].sum()), time.time() - t0, t1 - t0))
        return alle

    # Kandidaten ----------------------------------------------------------------------------------------------------
    def _gitterpunkte(self, raster_m, salz):
        """Gejitterte Gitterpunkte (global deterministisch) im Fenster: Rasterkoordinaten (fi, fj) + Hash."""
        i0, i1, j0, j1 = self.win
        gi = np.arange(i0 // raster_m, (i1 - 1) // raster_m + 1)
        gj = np.arange(j0 // raster_m, (j1 - 1) // raster_m + 1)
        GI, GJ = np.meshgrid(gi, gj, indexing="ij")
        hsh = hash64(self.seed, salz, GI.ravel(), GJ.ravel())
        fi = (GI.ravel() + uni(hsh, 1)) * raster_m - i0
        fj = (GJ.ravel() + uni(hsh, 2)) * raster_m - j0
        ok = (fi >= 1) & (fi < self.h.shape[0] - 1) & (fj >= 1) & (fj < self.h.shape[1] - 1)
        return fi[ok], fj[ok], hsh[ok]

    def _klasse_erlaubt(self, kname, ci, cj):
        """Je Kandidat: Klasse im Biom der Zelle erlaubt? und Faktor = Biomfaktor * Klassenfaktor (Grundregeln + Overrides)."""
        b = self.biom[ci, cj]
        return ~self.aus_klasse[kname][b], self.bf_klasse[kname][b]

    def kandidaten_gitter(self, kname):
        """Gitter-Kandidaten für band, wand, blockstrom (grat -> kandidaten_kamm, fuss -> kandidaten_strom seit Runde 2)."""
        K = self.R["klassen"][kname]
        salz = {"band": 12, "wand": 13, "blockstrom": 15}[kname]
        fi, fj, hsh = self._gitterpunkte(K["raster_m"], salz)
        ci, cj = np.round(fi).astype(np.int64), np.round(fj).astype(np.int64)
        hang = self.hang[ci, cj]
        ok = self.m_frei[ci, cj] & (hang >= K["hang_grad"][0]) & (hang <= K["hang_grad"][1])
        p = np.full(len(ci), K["p"] * self.faktor)
        if kname == "band":
            ok &= self.m_band[ci, cj] & ~self.m_mulde[ci, cj] & (self.grat[ci, cj] > -0.01)
            p *= self.f_fels[ci, cj]
            yaw = self.strike[ci, cj]
        elif kname == "wand":
            ok &= (self.grat[ci, cj] >= K["nase_min"])
            p *= self.f_fels[ci, cj]
            yaw = self.strike[ci, cj]
        else:  # blockstrom
            ok &= self.wand_ueber_128[ci, cj] & (self.hohl25[ci, cj] >= K["hohl_min"]) & ~self.m_wand[ci, cj]
            p *= self.f_ger[ci, cj]
            yaw = np.arctan2(self.abfall[ci, cj, 1], self.abfall[ci, cj, 0])
        erl, bf = self._klasse_erlaubt(kname, ci, cj)
        ok &= erl & (uni(hsh, 5) < p * bf)
        return {"ci": ci[ok], "cj": cj[ok], "fi": fi[ok], "fj": fj[ok], "h": hsh[ok], "yaw": yaw[ok], "stufe": None}

    def kandidaten_kuppe(self):
        K = self.R["klassen"]["kuppe"]
        hs = self.hs12
        peak = (hs >= boxmax(hs, K["umkreis_m"]) - 1e-6) & self.land & (self.hang <= K["hang_grad"][1]) & self.m_frei & ~self.m_wand
        peak[:2, :] = False; peak[-2:, :] = False; peak[:, :2] = False; peak[:, -2:] = False  # Fensterrand ist kein Gipfel
        ci, cj = np.nonzero(peak)
        if len(ci) == 0:
            return None
        i0, i1, j0, j1 = self.win
        # eine Kuppe je Umkreis-Zelle (Plateaus mit gleichen Werten)
        key = (ci + i0) // K["umkreis_m"] * 100000 + (cj + j0) // K["umkreis_m"]
        _, idx = np.unique(key, return_index=True)
        ci, cj = ci[idx], cj[idx]
        hsh = hash64(self.seed, 16, ci + i0, cj + j0)
        erl, bf = self._klasse_erlaubt("kuppe", ci, cj)
        ok = erl & (uni(hsh, 5) < K["p"] * self.faktor * bf)
        return {"ci": ci[ok], "cj": cj[ok], "fi": ci[ok].astype(float), "fj": cj[ok].astype(float), "h": hsh[ok],
                "yaw": zwischen(hsh[ok], 6, 0, 2 * np.pi), "stufe": None}

    def kandidaten_einzel(self):
        """Mindestdichte (mindestdichte_je_ha je Biom): Einzelblöcke/Moosfelsen auch ohne Relief.

        Ist-Dichte = Hauptstücke der Relief-Klassen je ha freier Biomfläche im Feld. Fehlt etwas, werden gejitterte
        Gitterpunkte (raster_m, globaler Hash -> nahtlos) mit p = Fehlmenge / Zahl freier Gitterpunkte angenommen."""
        K = self.R["klassen"].get("einzel")
        if K is None or not (self.mindest > 0).any():
            return None
        fs_i, fs_j = self.feld_slice
        hang_ok = (self.hang >= K["hang_grad"][0]) & (self.hang <= K["hang_grad"][1])
        basis = self.m_frei & hang_ok & ~self.m_mulde & ~self.m_wand & ~self.m_sperr
        rm = float(K["raster_m"])
        p_b = np.zeros(len(BIOME))
        for b in np.nonzero(self.mindest > 0)[0]:
            bfeld = self.biom[fs_i, fs_j] == b
            flaeche_ha = float((bfeld & self.m_frei[fs_i, fs_j]).sum()) / 1e4
            if flaeche_ha < 0.05 or self.aus_klasse["einzel"][b]:
                continue
            frei_ha = float((bfeld & basis[fs_i, fs_j]).sum()) / 1e4
            ist = self.haupt_je_biom[b] / flaeche_ha
            fehl = max(0.0, float(self.mindest[b]) - ist)
            if fehl <= 0 or frei_ha <= 0:
                log("Mindestdichte %s: Ist %.2f/ha, Soll %.2f/ha - keine Einzelbloecke noetig." % (BIOME[b], ist, self.mindest[b]))
                continue
            punkte = frei_ha * 1e4 / (rm * rm)
            p_b[b] = min(1.0, fehl * flaeche_ha / max(punkte, 1e-9))
            log("Mindestdichte %s: Soll %.2f/ha, Ist %.2f/ha auf %.1f ha -> ca. %d Einzelgruppen (p=%.3f je %d-m-Punkt)" % (
                BIOME[b], self.mindest[b], ist, flaeche_ha, int(round(min(fehl * flaeche_ha, punkte))), p_b[b], int(rm)))
        if not (p_b > 0).any():
            return None
        fi, fj, hsh = self._gitterpunkte(int(rm), 18)
        ci, cj = np.round(fi).astype(np.int64), np.round(fj).astype(np.int64)
        b = self.biom[ci, cj]
        ok = basis[ci, cj] & (uni(hsh, 5) < p_b[b] * self.faktor)
        return {"ci": ci[ok], "cj": cj[ok], "fi": fi[ok], "fj": fj[ok], "h": hsh[ok],
                "yaw": zwischen(hsh[ok], 6, 0, 2 * np.pi), "stufe": None}

    def _zellen_wahl(self, ci, cj, score, S, dmin):
        """Je globaler S-m-Zelle (Weltraster, nahtlos) der Kandidat mit höchstem score; Kandidaten der 8 Nachbarzellen, die näher als
        dmin liegen und einen höheren score haben, unterdrücken den schwächeren. Liefert Indizes in ci/cj."""
        if len(ci) == 0:
            return np.zeros(0, dtype=np.int64)
        i0, _, j0, _ = self.win
        gi, gj = ci + i0, cj + j0
        bi_, bj_ = gi // S, gj // S
        key = bi_ * 100000 + bj_
        order = np.lexsort((-score, key))
        ks = key[order]
        sel = order[np.concatenate([[True], ks[1:] != ks[:-1]])]  # nach key sortiert
        k, sc = key[sel], score[sel]
        pi, pj = gi[sel].astype(np.float64), gj[sel].astype(np.float64)
        weg = np.zeros(len(sel), dtype=bool)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                nk = (bi_[sel] + di) * 100000 + (bj_[sel] + dj)
                pos = np.minimum(np.searchsorted(k, nk), len(k) - 1)
                da = k[pos] == nk
                d = np.hypot(pi - pi[pos], pj - pj[pos])
                staerker = (sc[pos] > sc) | ((sc[pos] == sc) & (nk < k))
                weg |= da & (d < dmin) & staerker
        return sel[~weg]

    def kandidaten_kamm(self):
        """Felskrone (Klasse grat, Runde 2): Kammlinie = Gratstärke >= kamm_staerke_min, Querschnitt-Maximum der σ-8-Höhe
        (höher als ±kamm_quer_m quer zur Gratachse), Relief gegen σ 25 >= kamm_relief_min_m; eine Gruppe je kette_abstand_m-Zelle
        (höchster Kammpunkt + Zufall), Nachbarn < kette_min_abstand_m und Kuppen (< kuppe_abstand_m) unterdrückt -> Kette
        entlang des Kamms. Hauptrichtung = Gratachse."""
        K = self.R["klassen"]["grat"]
        hs = self.hs8
        rel = hs - self.hs25
        ok = (self.grat >= K["kamm_staerke_min"]) & (rel >= K["kamm_relief_min_m"]) & self.m_frei & ~self.m_mulde \
            & (self.hang >= K["hang_grad"][0]) & (self.hang <= K["hang_grad"][1])
        ok[:2, :] = False; ok[-2:, :] = False; ok[:, :2] = False; ok[:, -2:] = False
        ci, cj = np.nonzero(ok)
        if len(ci) == 0:
            return None
        quer = self.gratachse[ci, cj] + 0.5 * np.pi
        q = float(K["kamm_quer_m"])
        H, W = hs.shape
        di, dj = np.sin(quer) * q, np.cos(quer) * q
        h0 = hs[ci, cj]
        tol = float(K.get("kamm_toleranz_m", 0.03))
        h1 = bilinear(hs, np.clip(ci + di, 0, H - 1.001), np.clip(cj + dj, 0, W - 1.001))
        h2 = bilinear(hs, np.clip(ci - di, 0, H - 1.001), np.clip(cj - dj, 0, W - 1.001))
        kamm = (h0 >= h1 - tol) & (h0 >= h2 - tol)
        qg = float(K.get("kamm_quer_gross_m", 0.0))
        if qg > 0:  # großräumig: höchster Punkt im Querschnitt und deutlich über beiden Seiten (kein Buckel am Hang)
            dig, djg = np.sin(quer) * qg, np.cos(quer) * qg
            g1 = bilinear(hs, np.clip(ci + dig, 0, H - 1.001), np.clip(cj + djg, 0, W - 1.001))
            g2 = bilinear(hs, np.clip(ci - dig, 0, H - 1.001), np.clip(cj - djg, 0, W - 1.001))
            kamm &= (h0 >= np.maximum(g1, g2)) & (h0 - 0.5 * (g1 + g2) >= float(K.get("kamm_quer_relief_m", 2.5)))
        ci, cj = ci[kamm], cj[kamm]
        self.kamm_zellen = int(len(ci))
        if len(ci) == 0:
            return None
        i0, _, j0, _ = self.win
        hsh = hash64(self.seed, 11, ci + i0, cj + j0)
        score = rel[ci, cj] + float(K.get("kette_zufall_m", 3.0)) * uni(hsh, 1)
        s = self._zellen_wahl(ci, cj, score, int(K["kette_abstand_m"]), float(K["kette_min_abstand_m"]))
        ci, cj, hsh = ci[s], cj[s], hsh[s]
        ku = self._kuppen
        if ku is not None and len(ku["ci"]) and len(ci):  # Kuppe hat Vorrang (eigene Formgruppe)
            d = np.hypot(ci[:, None] - ku["ci"][None, :], cj[:, None] - ku["cj"][None, :]).min(axis=1)
            nah = d < float(K.get("kuppe_abstand_m", 24))
            ci, cj, hsh = ci[~nah], cj[~nah], hsh[~nah]
        p = K["p"] * self.faktor * self.f_fels[ci, cj]
        erl, bf = self._klasse_erlaubt("grat", ci, cj)
        ok = erl & (uni(hsh, 5) < p * bf)
        ci, cj, hsh = ci[ok], cj[ok], hsh[ok]
        return {"ci": ci, "cj": cj, "fi": ci.astype(float), "fj": cj.astype(float), "h": hsh, "yaw": self.gratachse[ci, cj],
                "stufe": None}

    def kandidaten_strom(self):
        """Blockstrom am Wandfuß (Klasse fuss, Runde 2): Zellen 0–8 m unter einer großen Wand >= wand_ab_grad (Stufe 0), keine
        Wand/Mulde, Hang laut Klasse; eine Zunge je strom_abstand_m-Zelle, Nachbarn < strom_min_abstand_m unterdrückt.
        Hauptrichtung = Falllinie."""
        K = self.R["klassen"]["fuss"]
        ok = (self.fuss_stufe == 0) & ~self.m_wand & ~self.m_mulde & self.m_frei & ~self.m_sperr \
            & (self.hang >= K["hang_grad"][0]) & (self.hang <= K["hang_grad"][1])
        ci, cj = np.nonzero(ok)
        if len(ci) == 0:
            return None
        i0, _, j0, _ = self.win
        hsh = hash64(self.seed, 14, ci + i0, cj + j0)
        s = self._zellen_wahl(ci, cj, uni(hsh, 1), int(K["strom_abstand_m"]), float(K["strom_min_abstand_m"]))
        ci, cj, hsh = ci[s], cj[s], hsh[s]
        erl, bf = self._klasse_erlaubt("fuss", ci, cj)
        ok = erl & (uni(hsh, 5) < K["p"] * self.faktor * self.f_ger[ci, cj] * bf)
        ci, cj, hsh = ci[ok], cj[ok], hsh[ok]
        return {"ci": ci, "cj": cj, "fi": ci.astype(float), "fj": cj.astype(float), "h": hsh,
                "yaw": np.arctan2(self.abfall[ci, cj, 1], self.abfall[ci, cj, 0]), "stufe": None}

    def kandidaten_prallhang(self, welt_dir):
        K = self.R["klassen"]["prallhang"]
        linien = lade_fluesse(welt_dir)
        if not linien:
            return None
        i0, i1, j0, j1 = self.win
        H, W = self.h.shape
        out = {"ci": [], "cj": [], "fi": [], "fj": [], "h": [], "yaw": []}
        for pts in linien:
            P = np.array([[p[0], p[1], (p[3] if len(p) > 3 else 400.0)] for p in pts], dtype=np.float64)
            fj = P[:, 0] / 100.0 + X0 - j0
            fi = P[:, 1] / 100.0 + Y0 - i0
            if not ((fi > -200) & (fi < H + 200) & (fj > -200) & (fj < W + 200)).any():
                continue
            if len(P) < 3:
                continue
            d1 = np.stack([fj[1:-1] - fj[:-2], fi[1:-1] - fi[:-2]], axis=1)
            d2 = np.stack([fj[2:] - fj[1:-1], fi[2:] - fi[1:-1]], axis=1)
            l1 = np.linalg.norm(d1, axis=1) + 1e-6
            l2 = np.linalg.norm(d2, axis=1) + 1e-6
            t1, t2 = d1 / l1[:, None], d2 / l2[:, None]
            kreuz = t1[:, 0] * t2[:, 1] - t1[:, 1] * t2[:, 0]
            punkt = np.clip((t1 * t2).sum(1), -1, 1)
            winkel = np.arctan2(kreuz, punkt)  # >0 Linkskurve (in (x,y)-Ebene)
            kappa = winkel / (0.5 * (l1 + l2))
            tang = t1 + t2
            tn = np.linalg.norm(tang, axis=1) + 1e-6
            tang /= tn[:, None]
            links = np.stack([-tang[:, 1], tang[:, 0]], axis=1)
            aussen = -np.sign(kappa)[:, None] * links  # Außenufer = gegen die Kurvenmitte
            s = np.concatenate([[0.0], np.cumsum(l1)])  # Bogenlänge an den Mittelpunkten
            stark = np.abs(kappa) >= K["kruemmung_min"]
            if not stark.any():
                continue
            idx = np.nonzero(stark)[0]
            # ein Kandidat je abstand_m Bogenlänge: stärkste Krümmung
            bucket = (s[idx] // K["abstand_m"]).astype(np.int64)
            order = np.lexsort((-np.abs(kappa[idx]), bucket))
            idx = idx[order]
            bucket = bucket[order]
            keep = np.concatenate([[True], bucket[1:] != bucket[:-1]])
            idx = idx[keep]
            hsh = hash64(self.seed, 17, np.round(P[idx + 1, 0]).astype(np.int64), np.round(P[idx + 1, 1]).astype(np.int64))
            ab = zwischen(hsh, 4, K["ufer_abstand_m"][0], K["ufer_abstand_m"][1]) + P[idx + 1, 2] / 200.0
            cj_f = fj[idx + 1] + aussen[idx, 0] * ab
            ci_f = fi[idx + 1] + aussen[idx, 1] * ab
            ok = (ci_f >= 1) & (ci_f < H - 1) & (cj_f >= 1) & (cj_f < W - 1)
            ci, cj = np.round(ci_f[ok]).astype(np.int64), np.round(cj_f[ok]).astype(np.int64)
            hsh, ci_f, cj_f = hsh[ok], ci_f[ok], cj_f[ok]
            yaw = np.arctan2(tang[idx[ok], 1], tang[idx[ok], 0])
            hang = self.hang[ci, cj]
            ok2 = self.m_frei[ci, cj] & (hang >= K["hang_grad"][0]) & (hang <= K["hang_grad"][1])
            erl, bf = self._klasse_erlaubt("prallhang", ci, cj)
            ok2 &= erl & (uni(hsh, 5) < self.faktor * bf)
            out["ci"].append(ci[ok2]); out["cj"].append(cj[ok2]); out["fi"].append(ci_f[ok2]); out["fj"].append(cj_f[ok2])
            out["h"].append(hsh[ok2]); out["yaw"].append(yaw[ok2])
        if not out["ci"]:
            return None
        g = {k: np.concatenate(v) for k, v in out.items()}
        g["stufe"] = None
        return g

    # Gruppen → Instanzen (Korrektur Runde 2: Gruppengrammatik „Form auf 300 m“) ----------------------------------------
    def ist_platte_pfad(self, pfad):
        """Flaches Platten-Netz laut Namensmuster (platten.muster), unabhängig von der Rolle."""
        v = self._platte_pfad.get(pfad)
        if v is None:
            name = self.netze[pfad]["name"] if pfad in self.netze else pfad.rsplit("/", 1)[-1]
            v = self._platte_pfad[pfad] = any(m in name for m in self.R.get("platten", {}).get("muster", []))
        return v

    def ist_platte(self, rolle, pfad):
        """Platten-Regel greift für Netze laut Namensmuster und für flache Netze (Höhe < flach_verhaeltnis × Breite) mit Rolle
        platte/geroell_platte; nicht flache Blöcke einer Platten-Rolle (z. B. hochgebirge moraene) bleiben bei den Lagen des Bioms."""
        return self.ist_platte_pfad(pfad) or (rolle in self.platten_rollen and bool(self.netz_info(pfad)[5]))

    def netz_info(self, pfad):
        """(Höhe cm, Radius cm, min_z cm, Breite m, max. Maßstab, flach) – Maßstab-Obergrenze 2,5 für Megascans, sonst 1,5."""
        v = self._ninfo.get(pfad)
        if v is None:
            F = self.R["form"]
            h_cm, r_cm, mz = self.netz_mass(pfad)
            mega = any(m in pfad for m in F.get("megascans_muster", ["/Megascans/"]))
            smax = float(F["max_skalierung_megascans"] if mega else F["max_skalierung_sonst"])
            w_m = 2.0 * r_cm / 100.0
            flach = (h_cm / 100.0) < float(F["flach_verhaeltnis"]) * w_m or self.ist_platte_pfad(pfad)
            v = self._ninfo[pfad] = (h_cm, r_cm, mz, w_m, smax, flach)
        return v

    def kandidaten_netze(self, pal, rolle):
        """Nicht flache Netze für eine Zielhöhen-Rolle (hero/block/stein) aus den Rollen laut form.kandidaten_rollen."""
        key = (pal, rolle)
        if key not in self._kand:
            F = self.R["form"]
            pf = []
            for r in F["kandidaten_rollen"].get(rolle, [rolle]) + ["block", "hero", "stein"]:
                if pf and r not in F["kandidaten_rollen"].get(rolle, [rolle]):
                    break  # Rückfall-Rollen nur, wenn die eigentlichen Rollen nichts liefern
                for p in self.paletten[pal].get(r, []):
                    if p not in pf and not self.netz_info(p)[5]:
                        pf.append(p)
            if not pf:
                self._kand[key] = None
            else:
                info = [self.netz_info(p) for p in pf]
                self._kand[key] = (pf, np.array([x[0] for x in info]) / 100.0, np.array([x[1] for x in info]),
                                   np.array([x[2] for x in info]), np.array([x[3] for x in info]), np.array([x[4] for x in info]))
        return self._kand[key]

    def waehle_ziel(self, kand, ziel_m, hh, wmax):
        """Je Stück ein Netz, das die Zielhöhe (Netzhöhe × Maßstab) innerhalb [min_skalierung, max. Maßstab] und der Breitengrenze
        erreicht (Wahl per Hash); sonst Rückfall auf das nächstliegende Netz. Liefert (Index, Maßstab, Zahl Rückfälle)."""
        pf, h_m, _, _, w_m, smax = kand
        smin = float(self.R["form"]["min_skalierung"])
        s_need = ziel_m[:, None] / h_m[None, :]
        ok = (s_need >= smin) & (s_need <= smax[None, :]) & (w_m[None, :] * s_need <= wmax)
        u = uni(hash64(hh[:, None], 61, np.arange(len(pf))[None, :]), 62)
        sc = np.where(ok, u, -1.0)
        k = np.argmax(sc, axis=1)
        kein = sc[np.arange(len(k)), k] < 0
        if kein.any():  # Rückfall: zufällig unter den Netzen, deren erreichbare Höhe höchstens 25 % neben dem Ziel liegt
            s_c = np.minimum(np.clip(s_need[kein], smin, smax[None, :]), wmax / w_m[None, :])
            fehler = np.abs(np.log(np.maximum(h_m[None, :] * s_c, 1e-3) / ziel_m[kein][:, None]))
            nah = fehler <= fehler.min(axis=1, keepdims=True) + math.log(1.25)
            k[kein] = np.argmax(np.where(nah, u[kein], -1.0), axis=1)
        s = np.minimum(np.clip(ziel_m / h_m[k], smin, smax[k]), wmax / w_m[k])
        return k, s, int(kein.sum())

    def platte_pruefen(self, fi, fj, rr, hz, tiefe_m, ci, cj):
        """Platten-Regel (platten.*): Lagen-Maske an Mitte + 4 Randpunkten (0,6 r) und strenger Schwebe-Test gegen die Ebene
        durch die Mitte (8 Richtungen am Rand): Gelände darf höchstens Eingrabtiefe + Toleranz unter der Plattenebene liegen."""
        H, W = self.h.shape
        ok = self.m_platte[ci, cj].copy()
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            pi = np.clip(np.round(fi + d[0] * 0.6 * rr), 0, H - 1).astype(np.int64)
            pj = np.clip(np.round(fj + d[1] * 0.6 * rr), 0, W - 1).astype(np.int64)
            ok &= self.m_platte[pi, pj]
        n = self.normal[ci, cj]
        gx, gy = -n[:, 0] / n[:, 2], -n[:, 1] / n[:, 2]  # Gradient der Ebene (dh/dx, dh/dy)
        tol = float(self.R["platten"].get("schwebe_toleranz_m", 0.05))
        for a in np.radians(np.arange(0, 360, 45)):
            dj, di = np.cos(a) * rr, np.sin(a) * rr
            hp = bilinear(self.h, np.clip(fi + di, 1, H - 1.001), np.clip(fj + dj, 1, W - 1.001))
            ok &= (hz + gx * dj + gy * di - hp) <= tiefe_m + tol
        return ok

    def _platzieren(self, pal, kname, bi, rolle, fi, fj, hh, yaw0, ziel=None, gid=None, gprio=None, haupt=False, dist_r=None):
        """Netzwahl, Maßstab, Eingraben, Prüfung (Fenster, Feld, frei, schwebend, Platten-Regel) und Ausrichtung für n Stücke einer
        Rolle. ziel = sichtbare Zielhöhe in m (Maßstab = Ziel / (Netzhöhe × (1 - Eingraben))); None = Maßstab aus der Rollenregel.
        Liefert (Instanz-Dict, Indizes der gültigen Eingaben) oder (None, leer)."""
        leer = (None, np.zeros(0, dtype=np.int64))
        n = len(fi)
        if n == 0:
            return leer
        K = self.klasse_param(kname, bi)
        RO = self.R["rollen"]
        F = self.R["form"]
        if ziel is None:
            pa = self.palette_arrays(pal, rolle)
            if pa is None:  # Rolle ohne Netze in dieser Palette -> nächstkleinere Rolle (wie Runde 1)
                for ersatz in ("block", "stein", "kiesel"):
                    pa = self.palette_arrays(pal, ersatz)
                    if pa is not None:
                        rolle = ersatz
                        break
            if pa is None:
                return leer
        ro = self.rolle_param(bi, rolle)
        ov_eb = self.rollen_ov.get((int(bi), rolle), {}).get("eingraben")
        eb = ov_eb if ov_eb is not None else K.get("eingraben", RO[rolle]["eingraben"])  # Override > Klasse > Rolle
        bury = zwischen(hh, 44, eb[0], eb[1])
        if ziel is not None:
            kand = self.kandidaten_netze(pal, rolle)
            if kand is None:
                return leer
            ziel_netz = np.asarray(ziel, dtype=np.float64) / np.maximum(1.0 - bury, 0.3)
            k, sk, n_rueck = self.waehle_ziel(kand, ziel_netz, hh, float(F["max_breite_m"].get(rolle, 16.0)))
            self.form_rueckfall[rolle] = self.form_rueckfall.get(rolle, 0) + n_rueck
            pfade_l, H_cm, R_cm, MZ = kand[0], kand[1][k] * 100.0, kand[2][k], kand[3][k]
        else:
            pfade_l, hc, rc, mz = pa
            k = np.minimum((uni(hh, 40) * len(pfade_l)).astype(np.int64), len(pfade_l) - 1)
            sk = zwischen(hh, 41, ro["massstab"][0], ro["massstab"][1])
            if not haupt and rolle in ("band", "wand"):
                sk = sk * zwischen(hh, 43, 0.55, 0.9)  # Nebenstücke kleiner als das Hauptstück
            H_cm, R_cm, MZ = hc[k], rc[k], mz[k]
        pfade = np.array(pfade_l, dtype=object)[k]
        ist_pl = np.array([self.ist_platte(rolle, p) for p in pfade_l])[k]
        if ist_pl.any():
            pmin = float(self.R["platten"].get("eingraben_min", 0.5))
            bury = np.where(ist_pl, np.maximum(bury, pmin), bury)
        r_eigen = R_cm * sk  # cm
        H, W = self.h.shape
        i0, i1, j0, j1 = self.win
        i0f, i1f, j0f, j1f = self.feld_box
        inside = (fi >= 1) & (fi < H - 1) & (fj >= 1) & (fj < W - 1)
        fi_c = np.clip(fi, 1, H - 1.001); fj_c = np.clip(fj, 1, W - 1.001)
        ci, cj = np.round(fi_c).astype(np.int64), np.round(fj_c).astype(np.int64)
        im_feld = (fi + i0 >= i0f) & (fi + i0 < i1f) & (fj + j0 >= j0f) & (fj + j0 < j1f)
        if rolle in ("stein", "kiesel", "platte"):
            frei = self.m_frei_klein[ci, cj]
        else:
            frei = self.m_frei[ci, cj] & ~self.m_sperr[ci, cj]
        hz = bilinear(self.h, fi_c, fj_c)
        rr = np.clip(r_eigen / 100.0, 0.5, 20.0)
        hmin_rand = np.minimum.reduce([bilinear(self.h, np.clip(fi_c + d[0] * rr, 1, H - 1.001), np.clip(fj_c + d[1] * rr, 1, W - 1.001))
                                       for d in ((1, 0), (-1, 0), (0, 1), (0, -1))])
        tiefe = bury * H_cm * sk / 100.0
        nicht_schwebend = (hz - hmin_rand) <= tiefe + 0.3 + rr * np.tan(np.radians(60.0))
        ok = inside & im_feld & frei & nicht_schwebend
        if ist_pl.any():
            s = np.nonzero(ok & ist_pl)[0]
            if len(s):
                ok[s] = self.platte_pruefen(fi_c[s], fj_c[s], rr[s], hz[s], tiefe[s], ci[s], cj[s])
            self.platten_verworfen += int((inside & im_feld & frei & ist_pl & ~ok).sum())
        if not ok.any():
            if haupt:
                log("  %s/%s: alle %d Hauptstuecke (%s) verworfen (im Fenster %d, im Feld %d, frei %d, nicht schwebend %d)" % (
                    kname, pal, n, rolle, int(inside.sum()), int(im_feld.sum()), int(frei.sum()), int(nicht_schwebend.sum())))
            return leer
        v = np.nonzero(ok)[0]
        hh, fi, fj, ci, cj, hz, yaw0 = hh[v], fi[v], fj[v], ci[v], cj[v], hz[v], yaw0[v]
        pfade, H_cm, R_cm, MZ, sk, bury, ist_pl, r_eigen = pfade[v], H_cm[v], R_cm[v], MZ[v], sk[v], bury[v], ist_pl[v], r_eigen[v]
        # Ausrichtung: Z auf Normale, Kippen in den Hang (Z-Achse Richtung bergauf), Yaw = Hauptrichtung ± Streuung.
        # Platten: Z-Achse = Geländenormale, kein Kippen, keine Schichtneigung.
        nrm = self.normal[ci, cj]
        kipp = np.radians(zwischen(hh, 45, ro["kippen_grad"][0], ro["kippen_grad"][1]))
        kipp = np.where(ist_pl, 0.0, kipp)
        up = nrm + np.concatenate([-self.abfall[ci, cj] * np.tan(kipp)[:, None], np.zeros((len(kipp), 1))], axis=1)
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        if rolle == "kiesel":
            yaw = zwischen(hh, 50, 0, 2 * np.pi)
        else:
            streu = np.radians(F.get("yaw_streuung_grad", self.R["gruppe"]["yaw_streuung_grad"]))
            yaw = yaw0 + zwischen(hh, 50, -streu, streu)
        if kname in ("band", "wand") and rolle != "kiesel":
            d = np.where(ist_pl, 0.0, self.dip[ci, cj])
            sv = np.stack([np.cos(yaw0), np.sin(yaw0), np.zeros_like(yaw0)], axis=1)  # Streichvektor
            up = up * np.cos(d)[:, None] + np.cross(sv, up) * np.sin(d)[:, None] + sv * (sv * up).sum(1, keepdims=True) * (1 - np.cos(d))[:, None]
            up /= np.linalg.norm(up, axis=1, keepdims=True)
        q = quat_aus_yaw_up(yaw, up)
        nu = ro["nicht_uniform"]
        sx = sk * (1 + nu * (2 * uni(hh, 51) - 1))
        sy = sk * (1 + nu * (2 * uni(hh, 52) - 1))
        sz = sk
        m = len(v)
        hoehe_m = H_cm * sz / 100.0
        koll = np.full(m, bool(ro["kollision"])) & (hoehe_m >= self.R.get("kollision_ab_hoehe_m", 0.8))
        akteur = np.full(m, rolle == "wand") | ((rolle == "hero") & (hoehe_m >= self.R.get("akteur_ab_hoehe_m", 5.0)))
        return {"x": (fj + j0 - X0) * 100.0, "y": (fi + i0 - Y0) * 100.0, "z": hz * 100.0 - MZ * sz - bury * H_cm * sz, "q": q,
                "sx": sx, "sy": sy, "sz": sz, "pfad": pfade, "rolle": np.full(m, rolle), "klasse": np.full(m, kname), "koll": koll,
                "schatten": np.full(m, bool(ro["schatten"])), "sicht": np.tile(np.array(ro["sichtweite_cm"], dtype=float), (m, 1)),
                "akteur": akteur, "hoehe_m": hoehe_m, "prio": uni(hh, 53), "ci": ci, "cj": cj, "fi": fi, "fj": fj,
                "gid": (gid[v] if gid is not None else hh).astype(U64), "gprio": gprio[v] if gprio is not None else uni(hh, 60),
                "haupt": np.full(m, bool(haupt)), "sicht_h": hoehe_m * (1.0 - bury), "r_m": R_cm * np.maximum(sx, sy) / 100.0,
                "dist_r": dist_r[v] if dist_r is not None else np.full(m, np.nan), "haengend": np.zeros(m, dtype=bool)}, v

    def gruppe_erzeugen(self, kname, g):
        """Je Biom (Palette, Rollen-Parameter, Kieselfaktor inkl. Overrides): Formgruppe (grat, kuppe, prallhang, einzel, band, wand)
        oder Blockstrom-Zunge (fuss, blockstrom)."""
        biom_g = self.biom[g["ci"], g["cj"]]
        teile = []
        for bi in np.unique(biom_g):
            sel = biom_g == bi
            pal = self.pal_je_biom[int(bi)]
            K = self.klasse_param(kname, bi)
            arg = (g["fi"][sel], g["fj"][sel], g["h"][sel], g["yaw"][sel])
            if kname in ("fuss", "blockstrom"):
                teile += self._gruppe_strom(kname, pal, bi, K, *arg)
            else:
                teile += self._gruppe_form(kname, pal, bi, K, *arg)
        return [t for t in teile if t is not None and len(t["x"])]

    def _haupt(self, pal, kname, bi, rollen_ziel, gi, gj, gh, gyaw, gprio):
        """Hauptstücke je Gruppe; rollen_ziel = Liste (rolle, maske, ziel-array oder None). Liefert (dict, Gruppenindizes)."""
        teile, idx = [], []
        for rolle, maske, ziel in rollen_ziel:
            s = np.nonzero(maske)[0]
            if len(s) == 0:
                continue
            t, ok = self._platzieren(pal, kname, bi, rolle, gi[s], gj[s], hash64(gh[s], 30, 0), gyaw[s],
                                     None if ziel is None else ziel[s], gh[s], gprio[s], haupt=True)
            if t is not None:
                teile.append(t)
                idx.append(s[ok])
        if not teile:
            return None, np.zeros(0, dtype=np.int64)
        return self.zusammenfuehren(teile), np.concatenate(idx)

    def _gruppe_form(self, kname, pal, bi, K, gi, gj, gh, gyaw):
        """Formgruppe: Hauptfels (sichtbar 4–10 m an Graten/Kuppen, Maßstab aus Netzhöhe), 3–5 Satelliten 1,5–4 m eng gestaffelt
        entlang der gemeinsamen Hauptrichtung (Mittenabstand <= 1,5 × Hauptfels-Radius), Steine 0,5–1,4 m, optional eine Platte am
        Fuß (nur auf Kies/Geröll/Fels), Kieselsaum 0,5–2 m um jedes große Stück. Ohne gültigen Hauptfels entfällt die Gruppe."""
        F = self.R["form"]
        n = len(gi)
        gprio = uni(gh, 60)
        erl = self.einzel_rollen.get(int(bi)) if kname == "einzel" else None
        if kname in ("band", "wand"):
            haupt, v = self._haupt(pal, kname, bi, [(kname, np.ones(n, bool), None)], gi, gj, gh, gyaw, gprio)
        else:
            hero = uni(gh, 20) < float(K.get("hero_p", 0.0))
            if erl is not None and "hero" not in erl:
                hero[:] = False
            hr = F["hero_hoehe_m"].get(kname, [4.0, 8.0])
            br = F["haupt_block_hoehe_einzel_m"] if kname == "einzel" else F["haupt_block_hoehe_m"]
            ziel = np.where(hero, zwischen(gh, 21, hr[0], hr[1]), zwischen(gh, 22, br[0], br[1]))
            haupt, v = self._haupt(pal, kname, bi, [("hero", hero, ziel), ("block", ~hero, ziel)], gi, gj, gh, gyaw, gprio)
        if haupt is None:
            return []
        if kname != "einzel":
            self.haupt_je_biom[int(bi)] += len(haupt["x"])  # Hauptstücke liegen alle im Feld (im_feld-Prüfung)
        teile = [haupt]
        Rh, Hh, cfi, cfj = haupt["r_m"], haupt["sicht_h"], haupt["fi"], haupt["fj"]
        yaw, hv, gp, gid = gyaw[v], gh[v], gprio[v], gh[v]
        ab = self.abfall[haupt["ci"], haupt["cj"]]
        ang_ab = np.arctan2(ab[:, 1], ab[:, 0])
        m = len(v)

        def anzahl(key, salz, lo=0, hi=0):
            r = K.get(key, [lo, hi])
            return ganz(hv, salz, int(r[0]), int(r[1])) if _spanne(r) else np.zeros(m, dtype=np.int64)

        def rang(cnt):
            idx = np.repeat(np.arange(m), cnt)
            return idx, np.arange(len(idx)) - np.repeat(np.cumsum(cnt) - cnt, cnt)

        darf = (lambda r: True) if erl is None else (lambda r: r in erl)
        a0, a1 = F["satellit_abstand_r"]
        streu = np.radians(F["satellit_streuung_grad"])
        gross = [haupt]
        # Satelliten entlang der Hauptrichtung (abwechselnd beide Seiten), Abstand wächst mit dem Rang, Größe nimmt ab
        sat_plan = []
        if kname == "band":
            sat_plan.append(("band", np.maximum(anzahl("band", 31) - 1, 0), False))
        elif kname == "wand":
            sat_plan.append(("wand", np.maximum(anzahl("wand", 31) - 1, 0), False))
            sat_plan.append(("block", anzahl("block", 32), True))
        else:
            sat_plan.append(("block", anzahl("block", 32), True))
        for rolle, cnt, mit_ziel in sat_plan:
            if not darf(rolle) or cnt.sum() == 0:
                continue
            idx, k = rang(cnt)
            hs_ = hash64(hv[idx], 32 if rolle == "block" else 31, k)
            u = (k + uni(hs_, 1)) / np.maximum(cnt[idx], 1)
            if rolle in ("band", "wand"):  # entlang des Streichens
                dist = Rh[idx] * np.minimum(0.9 + 0.5 * (k // 2), a1)
                ang = yaw[idx] + np.where(k % 2 == 0, 0.0, np.pi) + np.radians(zwischen(hs_, 2, -8, 8))
                ziel = None
            else:
                dist = Rh[idx] * (a0 + (a1 - a0) * u)
                ang = yaw[idx] + np.where(k % 2 == 0, 0.0, np.pi) + zwischen(hs_, 2, -streu, streu)
                lo, hi = F["satellit_hoehe_m"]
                f0, f1 = F["satellit_anteil_haupt"]
                ziel = Hh[idx] * zwischen(hs_, 3, f0, f1) * (1.0 - 0.3 * u)
                ziel = np.clip(ziel, np.minimum(lo, 0.7 * Hh[idx]), np.minimum(hi, 0.85 * Hh[idx]))
            t, _ = self._platzieren(pal, kname, bi, rolle, cfi[idx] + np.sin(ang) * dist, cfj[idx] + np.cos(ang) * dist, hs_,
                                    yaw[idx], ziel, gid[idx], gp[idx], dist_r=dist / np.maximum(Rh[idx], 1e-3))
            if t is not None:
                teile.append(t)
                gross.append(t)
        # Steine 0,5–1,4 m dicht am Hauptfels, bevorzugt hangabwärts
        cnt = anzahl("stein", 33)
        if darf("stein") and cnt.sum():
            idx, k = rang(cnt)
            hs_ = hash64(hv[idx], 33, k)
            s0, s1 = F["stein_abstand_r"]
            dist = Rh[idx] * zwischen(hs_, 1, s0, s1)
            ang = np.where(uni(hs_, 2) < 0.6, ang_ab[idx] + zwischen(hs_, 3, -1.2, 1.2), zwischen(hs_, 4, 0, 2 * np.pi))
            lo, hi = F["stein_hoehe_m"]
            t, _ = self._platzieren(pal, kname, bi, "stein", cfi[idx] + np.sin(ang) * dist, cfj[idx] + np.cos(ang) * dist, hs_,
                                    yaw[idx], zwischen(hs_, 5, lo, hi), gid[idx], gp[idx], dist_r=dist / np.maximum(Rh[idx], 1e-3))
            if t is not None:
                teile.append(t)
                gross.append(t)
        # Platte am Fuß des Hauptfelsens (Platten-Regel: nur auf Kies/Geröll/Fels-Lagen)
        pp = float(K.get("platte_p", 0.0))
        if pp > 0 and self.paletten[pal].get("platte") and darf("platte"):
            s = np.nonzero(uni(hv, 34) < pp)[0]
            if len(s):
                hs_ = hash64(hv[s], 34, 0)
                p0, p1 = F["platte_abstand_r"]
                dist = Rh[s] * zwischen(hs_, 1, p0, p1)
                ang = ang_ab[s] + zwischen(hs_, 2, -1.0, 1.0)
                t, _ = self._platzieren(pal, kname, bi, "platte", cfi[s] + np.sin(ang) * dist, cfj[s] + np.cos(ang) * dist, hs_,
                                        yaw[s], None, gid[s], gp[s])
                if t is not None:
                    teile.append(t)
        teile += self._saum(pal, kname, bi, K, gross)
        return teile

    def _gruppe_strom(self, kname, pal, bi, K, gi, gj, gh, gyaw):
        """Blockstrom-Zunge: Kopfblock (sichtbar kopf_hoehe_m) am Wandfuß bzw. Hangfuß, dann n Blöcke/Steine entlang der Falllinie,
        Größe hangabwärts abnehmend (form.strom_groesse), Fächer wird nach unten breiter, Länge <= laenge_max_m; Kieselsaum um
        jedes Stück (ergibt den Schuttfächer)."""
        F = self.R["form"]
        n = len(gi)
        gprio = uni(gh, 60)
        kr = K.get("kopf_hoehe_m", [2.0, 3.5])
        ziel = zwischen(gh, 21, kr[0], kr[1])
        haupt, v = self._haupt(pal, kname, bi, [("block", np.ones(n, bool), ziel)], gi, gj, gh, gyaw, gprio)
        if haupt is None:
            return []
        self.haupt_je_biom[int(bi)] += len(haupt["x"])
        teile, gross = [haupt], [haupt]
        Rh, Hh, cfi, cfj = haupt["r_m"], haupt["sicht_h"], haupt["fi"], haupt["fj"]
        yaw, hv, gp = gyaw[v], gh[v], gprio[v]
        m = len(v)
        nr = K.get("n", K.get("block", [3, 5]))
        cnt = ganz(hv, 31, int(nr[0]), int(nr[1]))
        idx = np.repeat(np.arange(m), cnt)
        k = np.arange(len(idx)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        if len(idx):
            hs_ = hash64(hv[idx], 31, k)
            u = (k + 1.0) / cnt[idx]
            g0, g1 = F["strom_groesse"]
            t = Hh[idx] * (g0 + (g1 - g0) * u) * zwischen(hs_, 3, 0.85, 1.1)
            r_est = 0.85 * t  # Fußradius typischer Blöcke ~ 0,85 × sichtbare Höhe
            r_vor = np.where(k == 0, Rh[idx], np.concatenate([[0.0], r_est[:-1]]))
            f0, f1 = F["strom_abstand_faktor"]
            schritt = (r_vor + r_est) * zwischen(hs_, 4, f0, f1)
            cs = np.cumsum(schritt)
            s_lang = cs - np.repeat(cs[np.cumsum(cnt) - cnt] - schritt[np.cumsum(cnt) - cnt], cnt)
            lat = zwischen(hs_, 5, -1.0, 1.0) * (0.4 * r_est + 0.18 * s_lang)
            y_ = yaw[idx]
            pfi = cfi[idx] + np.sin(y_) * s_lang + np.cos(y_) * lat
            pfj = cfj[idx] + np.cos(y_) * s_lang - np.sin(y_) * lat
            lang_ok = s_lang + r_est <= float(K.get("laenge_max_m", 30))
            for rolle, maske in (("block", t >= 0.8), ("stein", t < 0.8)):
                s = np.nonzero(maske & lang_ok)[0]
                if len(s) == 0:
                    continue
                tt, _ = self._platzieren(pal, kname, bi, rolle, pfi[s], pfj[s], hs_[s], y_[s], np.maximum(t[s], 0.5), hv[idx][s],
                                         gp[idx][s])
                if tt is not None:
                    teile.append(tt)
                    gross.append(tt)
        teile += self._saum(pal, kname, bi, K, gross)
        return teile

    def _saum(self, pal, kname, bi, K, gross):
        """Kieselsaum (Kleinmaterial) 0,5–2 m um jedes große Stück, bevorzugt hangabwärts; Anzahl je Stück aus Ringfläche ×
        Dichte, begrenzt auf klassen.<k>.kiesel (Hauptstück) bzw. form.kiesel_je_stueck (übrige), × Kieselfaktor des Bioms."""
        F = self.R["form"]
        kf = float(self.kiesel_f[int(bi)])
        if kf <= 0 or not self.paletten[pal].get("kiesel") or not gross:
            return []
        g = self.zusammenfuehren(gross)
        n = len(g["x"])
        if n == 0:
            return []
        lo = np.zeros(n); hi = np.zeros(n)
        for rolle, (a, b) in F["kiesel_je_stueck"].items():
            s = (g["rolle"] == rolle) & ~g["haupt"]
            lo[s], hi[s] = a, b
        kk = K.get("kiesel", [0, 0])
        lo[g["haupt"]], hi[g["haupt"]] = kk[0], kk[1]
        lo, hi = np.round(lo * kf), np.maximum(np.round(lo * kf), np.round(hi * kf))
        ph = hash64(g["gid"].astype(np.int64), np.round(g["x"]).astype(np.int64), np.round(g["y"]).astype(np.int64))
        r0, r1 = F["kiesel_ring_m"]
        d0, d1 = F["kiesel_dichte_je_m2"]
        flaeche = np.pi * ((g["r_m"] + r1) ** 2 - (g["r_m"] + r0) ** 2)
        cnt = np.clip(np.round(flaeche * zwischen(ph, 35, d0, d1) * self.faktor * kf), lo, hi).astype(np.int64)
        if cnt.sum() == 0:
            return []
        idx = np.repeat(np.arange(n), cnt)
        k = np.arange(len(idx)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        hk = hash64(ph[idx], 36, k)
        ab = self.abfall[g["ci"][idx], g["cj"][idx]]
        hangab = np.arctan2(ab[:, 1], ab[:, 0])
        ang = np.where(uni(hk, 1) < float(F["kiesel_hangab_anteil"]), hangab + zwischen(hk, 2, -1.4, 1.4), zwischen(hk, 3, 0, 2 * np.pi))
        dist = g["r_m"][idx] + zwischen(hk, 4, r0, r1)
        t, _ = self._platzieren(pal, kname, bi, "kiesel", g["fi"][idx] + np.sin(ang) * dist, g["fj"][idx] + np.cos(ang) * dist, hk,
                                np.zeros(len(idx)), None, g["gid"][idx], g["gprio"][idx])
        return [t] if t is not None else []

    # Zusatzklassen ---------------------------------------------------------------------------------------------------
    def abstand(self, maske, maxd):
        """Chebyshev-Abstand (m) zu maske, bis maxd (darüber maxd + 1); iterative 3x3-Dilatation, keine Zellschleifen."""
        d = np.full(maske.shape, float(maxd + 1))
        d[maske] = 0.0
        cur = maske.copy()
        for k in range(1, int(maxd) + 1):
            nxt = cur.copy()
            for ax in (0, 1):
                nxt |= _shift(cur, 1, ax, False) | _shift(cur, -1, ax, False)
            nxt |= _shift(_shift(cur, 1, 0, False), 1, 1, False) | _shift(_shift(cur, 1, 0, False), -1, 1, False)
            nxt |= _shift(_shift(cur, -1, 0, False), 1, 1, False) | _shift(_shift(cur, -1, 0, False), -1, 1, False)
            d[nxt & ~cur] = float(k)
            cur = nxt
            if cur.all():
                break
        return d

    def lage(self, welt_dir, name):
        if name not in self._lage_cache:
            a = lade_raster(os.path.join(welt_dir, "lage_%s.r8" % name), np.uint8, self.win, name="lage_%s.r8" % name)
            self._lage_cache[name] = None if a is None else a.astype(np.float64)
        return self._lage_cache[name]

    def zusatz_gewicht(self, z, welt_dir):
        """Gewicht 0..1.5 je Zelle im Fenster: Biom (+30-m-Saum) x Hang x Höhe x Wasserabstand x Lagen x Krümmung x ..."""
        saum = float(self.R.get("zusatz", {}).get("saum_m", 30))
        bw = np.zeros(len(BIOME))
        for bn, x in z["biome"].items():
            bw[BIOME.index(bn)] = x
        if not (bw > 0).any():
            return None
        key = ("biom",) + tuple(np.nonzero(bw > 0)[0])
        if key not in self._abst_cache:
            self._abst_cache[key] = self.abstand(bw[self.biom] > 0, int(saum))
        d = self._abst_cache[key]
        w = np.where(bw[self.biom] > 0, bw[self.biom], np.clip(1.0 - d / saum, 0.0, 1.0) * bw.max())
        if z["hang"]:
            w = w * trapez(self.hang, z["hang"])
        if z["hoehe"]:
            w = w * trapez(self.h, z["hoehe"])
        if z["wasser"]:
            wm = self.m_wasser_roh & (self.h <= 0.5) if z["meer_nur"] else self.m_wasser_roh
            maxd = int(min(64, max(1.0, z["wasser"][3])))
            k = ("wasser", z["meer_nur"], maxd)
            if k not in self._abst_cache:
                self._abst_cache[k] = self.abstand(wm, maxd)
            w = w * trapez(self._abst_cache[k], z["wasser"])
        for ln, mn in z["lagen_min"].items():
            a = self.lage(welt_dir, ln)
            if a is not None:
                w = w * (a >= mn)
        if z["lagen_gewicht"]:
            summe, da = np.zeros_like(w), False
            for ln, g in z["lagen_gewicht"].items():
                a = self.lage(welt_dir, ln)
                if a is not None:
                    summe += g * a / 255.0
                    da = True
            if da:
                w = w * np.clip(summe, 0.0, 1.5)
        if z["kruemmung"] == "konvex":
            w = w * (self.grat > 0.005)
        elif z["kruemmung"] == "konkav":
            w = w * (self.mulde > 0.005)
        if z["exposition"]:
            ax, sg = {"nord": (1, -1), "sued": (1, 1), "ost": (0, 1), "west": (0, -1)}[z["exposition"]]
            w = w * (sg * self.abfall[:, :, ax] > 0.5)
        if z["relief"]:
            u, mn = z["relief"]
            w = w * ((boxmax(self.h, int(u)) - boxmin(self.h, int(u))) >= mn)
        if z["kuppe_prominenz_m"]:
            hs = self.hs12
            w = w * ((hs >= boxmax(hs, 16) - 0.5) & (hs - boxmin(hs, 64) >= z["kuppe_prominenz_m"]))
        if z["wand_abstand"]:
            maxd = int(min(64, max(1.0, z["wand_abstand"][3])))
            k = ("wand", maxd)
            if k not in self._abst_cache:
                self._abst_cache[k] = self.abstand(self.m_wand, maxd)
            w = w * trapez(self._abst_cache[k], z["wand_abstand"])
        if z["zonen"]:  # Geländezonen (Vorrang wand > fuss > gipfel > spalte > sonst); nicht genannte Zonen Faktor 1
            Zf = z["zonen"]
            maxd = int(min(64, max(1.0, z["fuss_m"])))
            k = ("wand", maxd)
            if k not in self._abst_cache:
                self._abst_cache[k] = self.abstand(self.m_wand, maxd)
            fuss = (self._abst_cache[k] <= z["fuss_m"]) & ~self.m_wand
            gipfel = ~self.m_wand & ~fuss & (self.grat > 0.005)
            spalte = ~self.m_wand & ~fuss & ~gipfel & (self.mulde > 0.005)
            zf = np.full(w.shape, Zf.get("sonst", 1.0))
            zf[spalte] = Zf.get("spalte", 1.0)
            zf[gipfel] = Zf.get("gipfel", 1.0)
            zf[fuss] = Zf.get("fuss", 1.0)
            zf[self.m_wand] = Zf.get("wand", 1.0)
            w = w * zf
        if z["klumpung"]:
            sk, st, sw = z["klumpung"]
            n = wertrauschen(self.xg, self.yg, sk, self.seed, 50 + zlib.crc32(z["name"].encode()) % 1000)
            w = w * ((1.0 - st) + st * np.clip((n - sw) / max(1e-6, 1.0 - sw), 0.0, 1.0))
        klein = z["rolle"] in ("stein", "kiesel", "platte")
        frei = self.m_frei_klein if klein else (self.m_frei & ~self.m_sperr)
        return w * frei

    def zusatz_erzeugen(self, z, feld, welt_dir):
        """Kandidaten (Gitter oder Punkte) -> Gruppen -> Instanzen (Format wie _stuecke)."""
        salz = 2000 + zlib.crc32(("%s/%s" % (z["datei"], z["name"])).encode()) % 100000
        w = self.zusatz_gewicht(z, welt_dir)
        if w is None or not (w > 0).any():
            return None, 0
        fs_i, fs_j = self.feld_slice
        n_lo, n_hi = z["gruppe_n"]
        n_mittel = max(0.5 * (n_lo + n_hi), 1.0)
        dichte = (z["dichte_je_ha"] or 0.0) / (1.0 if z["dichte_gruppen"] else n_mittel)  # Gruppen je ha
        name = "%s/%s" % (z["datei"].replace("_regeln.json", ""), z["name"])
        punkte = None
        if z["punkte"]:
            # Plan des Biom-Planers vorhanden -> genau dessen Punkte (auch 0); Ersatzmaske nur, wenn der Plan fehlt/unlesbar ist
            pq = z["punkte"]
            pp = os.path.join(welt_dir, pq.get("ebene", ""), feld, "plan.json")
            if os.path.isfile(pp):
                try:
                    with open(pp, encoding="utf-8") as f:
                        pl = json.load(f)
                    punkte = [p for p in pl.get("punkte", []) if isinstance(p, dict) and p.get("typ") == pq.get("typ")
                              and _zahl(p.get("x_cm")) and _zahl(p.get("y_cm"))]
                    log("Zusatzklasse %s: %d Punkte (%s) aus %s" % (name, len(punkte), pq.get("typ"), pp))
                except Exception as e:
                    log("Hinweis: Zusatzklasse %s: %s unlesbar (%s) - Ersatz ueber Maske." % (name, pp, e))
            else:
                log("Hinweis: Zusatzklasse %s: %s/%s/plan.json fehlt - Ersatz ueber Maske (Hang, Prominenz, Lagen)." % (
                    name, pq.get("ebene"), feld))
            if punkte is not None and not punkte:
                return None, 0
        p_netz = p_yaw = None
        if punkte:
            fi = np.array([p["y_cm"] / 100.0 + Y0 - self.win[0] for p in punkte])
            fj = np.array([p["x_cm"] / 100.0 + X0 - self.win[2] for p in punkte])
            p_netz = np.array([norm_pfad(p["netz"]) if isinstance(p.get("netz"), str) else "" for p in punkte], dtype=object)
            p_yaw = np.array([math.radians(p["yaw_grad"]) if _zahl(p.get("yaw_grad")) else np.nan for p in punkte])
            ok = (fi >= 1) & (fi < self.h.shape[0] - 1) & (fj >= 1) & (fj < self.h.shape[1] - 1)
            fi, fj, p_netz, p_yaw = fi[ok], fj[ok], p_netz[ok], p_yaw[ok]
            ci, cj = np.round(fi).astype(np.int64), np.round(fj).astype(np.int64)
            hsh = hash64(self.seed, salz, ci + self.win[0], cj + self.win[2])
            # Punkte des Biom-Planers tragen dessen Bedingungen schon: gültig, wo frei (nicht über die Ersatzmaske)
            w = (self.m_frei & ~self.m_sperr).astype(np.float64)
            ok = w[ci, cj] > 0
        else:
            if dichte <= 0:
                return None, 0
            fein = bool(z["relief"] or z["kuppe_prominenz_m"] or z["exposition"])
            r = z["raster_m"] or np.clip(math.sqrt(1e4 / max(dichte, 1e-6)) / 2.0, 2.0, 32.0)
            r = int(max(2, min(r, 3 if fein else r)))
            fi, fj, hsh = self._gitterpunkte(r, salz)
            ci, cj = np.round(fi).astype(np.int64), np.round(fj).astype(np.int64)
            wp = w[ci, cj]
            if z["dichte_bezug"] == "biom":  # Dichte je ha Biomfläche (je_km2): auf die Kandidaten im Feld verteilen
                bw = np.array([z["biome"].get(bn, 0.0) for bn in BIOME])
                flaeche_ha = float(((bw[self.biom[fs_i, fs_j]] > 0) & self.land[fs_i, fs_j]).sum()) / 1e4
                im = ((ci >= fs_i.start) & (ci < fs_i.stop) & (cj >= fs_j.start) & (cj < fs_j.stop))
                summe = float(wp[im].sum())
                p = (dichte * flaeche_ha / summe) if summe > 0 else 0.0
            else:
                p = dichte * r * r / 1e4
            ok = uni(hsh, 5) < np.minimum(1.0, p * wp * self.faktor)
        if p_netz is None:
            p_netz = np.full(len(fi), "", dtype=object)
            p_yaw = np.full(len(fi), np.nan)
        fi, fj, ci, cj, hsh, p_netz, p_yaw = fi[ok], fj[ok], ci[ok], cj[ok], hsh[ok], p_netz[ok], p_yaw[ok]
        im = (ci >= fs_i.start) & (ci < fs_i.stop) & (cj >= fs_j.start) & (cj < fs_j.stop)
        fi, fj, ci, cj, hsh, p_netz, p_yaw = fi[im], fj[im], ci[im], cj[im], hsh[im], p_netz[im], p_yaw[im]
        if z["max_je_feld"] is not None and len(ci) > z["max_je_feld"]:
            o = np.argsort(uni(hsh, 7), kind="stable")[: z["max_je_feld"]]
            fi, fj, ci, cj, hsh, p_netz, p_yaw = fi[o], fj[o], ci[o], cj[o], hsh[o], p_netz[o], p_yaw[o]
        if len(ci) == 0:
            return None, 0
        # Palette: eigene Netzliste, sonst Rollen der Biom-Palette (Altstellen ohne Netze)
        pfade = list(z["palette"])
        if not pfade:
            b0 = BIOME.index(next(iter(z["biome"])))
            for r_ in z["palette_rollen"]:
                pfade += [p for p in self.paletten[self.pal_je_biom[b0]].get(r_, []) if p not in pfade]
        for pn in p_netz:  # Netz aus dem Punkt (im Inventar) zusätzlich erlauben
            if pn and pn in self.netze and pn not in pfade and pn not in self.gesperrt:
                pfade.append(pn)
        if not pfade:
            return None, 0
        mass = [self.netz_mass(p) for p in pfade]
        hc = np.array([m[0] for m in mass]); rc = np.array([m[1] for m in mass]); mzc = np.array([m[2] for m in mass])
        ro = self.R["rollen"][z["rolle"]]
        # Gruppen -> Stücke
        cnt = ganz(hsh, 21, n_lo, n_hi)
        idx = np.repeat(np.arange(len(ci)), cnt)
        m = np.arange(len(idx)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        hh = hash64(hsh[idx], salz, m)
        dist = np.where(m == 0, 0.0, z["gruppe_r"] * np.sqrt(uni(hh, 22)))
        ang = zwischen(hh, 23, 0, 2 * np.pi)
        pfi = fi[idx] + np.sin(ang) * dist
        pfj = fj[idx] + np.cos(ang) * dist
        H, W = self.h.shape
        i0, i1, j0, j1 = self.win
        i0f, i1f, j0f, j1f = self.feld_box
        inside = (pfi >= 1) & (pfi < H - 1) & (pfj >= 1) & (pfj < W - 1)
        fi_c = np.clip(pfi, 1, H - 1.001); fj_c = np.clip(pfj, 1, W - 1.001)
        pci, pcj = np.round(fi_c).astype(np.int64), np.round(fj_c).astype(np.int64)
        im_feld = (pfi + i0 >= i0f) & (pfi + i0 < i1f) & (pfj + j0 >= j0f) & (pfj + j0 < j1f)
        k = np.minimum((uni(hh, 40) * len(pfade)).astype(np.int64), len(pfade) - 1)
        # Hauptstück (m == 0) übernimmt Netz und Drehung aus dem Punkt, falls angegeben
        pidx = {p: n_ for n_, p in enumerate(pfade)}
        k_punkt = np.array([pidx.get(pn, -1) for pn in p_netz[idx]], dtype=np.int64)
        k = np.where((m == 0) & (k_punkt >= 0), k_punkt, k)
        yaw_alle = zwischen(hh, 50, 0, 2 * np.pi)
        yp = p_yaw[idx]
        yaw_alle = np.where((m == 0) & ~np.isnan(yp), np.nan_to_num(yp), yaw_alle)
        ms = z["massstab"] or ro["massstab"]
        sk = zwischen(hh, 41, ms[0], ms[1])
        eb = z["eingraben"] or ro["eingraben"]
        bury = zwischen(hh, 44, eb[0], eb[1])
        H_cm, R_cm, MZ = hc[k], rc[k], mzc[k]
        # Platten-Regel (Runde 2) zentral auch für Zusatzklassen: Rolle platte oder Platten-Netz laut Namensmuster
        ist_pl = np.array([self.ist_platte(z["rolle"], p) for p in pfade])[k]
        if ist_pl.any():
            bury = np.where(ist_pl, np.maximum(bury, float(self.R["platten"].get("eingraben_min", 0.5))), bury)
        r_eigen = R_cm * sk
        hz = bilinear(self.h, fi_c, fj_c)
        rr = np.clip(r_eigen / 100.0, 0.5, 20.0)
        hmin_rand = np.minimum.reduce([bilinear(self.h, np.clip(fi_c + d_[0] * rr, 1, H - 1.001), np.clip(fj_c + d_[1] * rr, 1, W - 1.001))
                                       for d_ in ((1, 0), (-1, 0), (0, 1), (0, -1))])
        nicht_schwebend = (hz - hmin_rand) <= bury * H_cm * sk / 100.0 + 0.3 + rr * np.tan(np.radians(60.0))
        if z["z_versatz"]:  # hängende Stücke (Pivot oben, z. B. Eisvorhänge): Floating-Prüfung entfällt bewusst
            nicht_schwebend = np.ones(len(hh), dtype=bool)
        ok = inside & im_feld & (w[pci, pcj] > 0) & nicht_schwebend
        if ist_pl.any():
            s_ = np.nonzero(ok & ist_pl)[0]
            if len(s_):
                ok[s_] = self.platte_pruefen(fi_c[s_], fj_c[s_], rr[s_], hz[s_], (bury * H_cm * sk / 100.0)[s_], pci[s_], pcj[s_])
            n_pl = int((inside & im_feld & (w[pci, pcj] > 0) & ist_pl & ~ok).sum())
            self.platten_verworfen += n_pl
            if n_pl:
                log("Zusatzklasse %s: %d Platten verworfen (Platten-Regel: Kies/Geroell/Fels-Lage >= %s, nicht schwebend)" % (
                    name, n_pl, self.R["platten"].get("lagen_min", 100)))
        if not ok.any():
            return None, len(ci)
        hh, pfi, pfj, pci, pcj, hz, k, sk, bury, H_cm, MZ, yaw_alle, ist_pl, r_eigen, m_ = (a[ok] for a in (
            hh, pfi, pfj, pci, pcj, hz, k, sk, bury, H_cm, MZ, yaw_alle, ist_pl, r_eigen, m))
        gidx = idx[ok]
        k_ok = np.nonzero(ok)[0]
        kipp = np.radians(zwischen(hh, 45, ro["kippen_grad"][0], ro["kippen_grad"][1]))
        kipp = np.where(ist_pl, 0.0, kipp)  # Platten: Z-Achse = Geländenormale
        up = self.normal[pci, pcj] + np.concatenate([-self.abfall[pci, pcj] * np.tan(kipp)[:, None], np.zeros((len(kipp), 1))], axis=1)
        if z["z_versatz"]:  # hängend: Z-Achse = Welt-Z (nicht auf die Wandnormale gekippt)
            up = np.tile(np.array([0.0, 0.0, 1.0]), (len(kipp), 1))
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        q = quat_aus_yaw_up(yaw_alle, up)
        nu = ro["nicht_uniform"]
        sx = sk * (1 + nu * (2 * uni(hh, 51) - 1)); sy = sk * (1 + nu * (2 * uni(hh, 52) - 1)); sz = sk
        hoehe_m = H_cm * sz / 100.0
        n = len(hh)
        koll_basis = ro["kollision"] if z["kollision"] is None else z["kollision"]
        koll = np.full(n, bool(koll_basis)) & (hoehe_m >= self.R.get("kollision_ab_hoehe_m", 0.8))
        sicht = np.tile(np.array(z["sichtweite"] or ro["sichtweite_cm"], dtype=float), (n, 1))
        zv = zwischen(hh, 54, z["z_versatz"][0], z["z_versatz"][1]) if z["z_versatz"] else 0.0
        # z_versatz_anteil: Stück um Anteil x Netzhöhe x Maßstab nach oben (Welt-Z) versetzt (hochgebirge: "Pivot oben")
        t = {"x": (pfj + j0 - X0) * 100.0, "y": (pfi + i0 - Y0) * 100.0, "z": hz * 100.0 - MZ * sz - bury * H_cm * sz + zv * H_cm * sz, "q": q,
             "sx": sx, "sy": sy, "sz": sz, "pfad": np.array(pfade, dtype=object)[k], "rolle": np.full(n, z["rolle"]),
             "klasse": np.full(n, "z_" + z["name"]), "koll": koll,
             "schatten": np.full(n, bool(ro["schatten"] if z["schatten"] is None else z["schatten"])), "sicht": sicht,
             "akteur": np.full(n, bool(z["akteur"])), "hoehe_m": hoehe_m, "prio": uni(hh, 53), "ci": pci, "cj": pcj,
             "fi": pfi, "fj": pfj, "gid": hsh[gidx].astype(U64), "gprio": uni(hsh[gidx], 60), "haupt": np.zeros(n, dtype=bool),
             "sicht_h": hoehe_m * (1.0 - bury) + (zv * hoehe_m if z["z_versatz"] else 0.0), "r_m": R_cm[k_ok] * np.maximum(sx, sy) / 100.0,
             "dist_r": np.full(n, np.nan), "haengend": np.full(n, bool(z["z_versatz"]))}
        log("Zusatzklasse %s: %d Gruppen, %d Instanzen (%d mit Kollision%s)" % (
            name, len(ci), n, int(koll.sum()), ", Akteure" if z["akteur"] else ""))
        return t, len(ci)

    # Zusammenführen, Budget, Kontaktsaum, Statistik ---------------------------------------------------------------------
    SCHLUESSEL = ["x", "y", "z", "q", "sx", "sy", "sz", "pfad", "rolle", "klasse", "koll", "schatten", "sicht", "akteur", "hoehe_m",
                  "prio", "ci", "cj", "fi", "fj", "gid", "gprio", "haupt", "sicht_h", "r_m", "dist_r", "haengend"]

    def zusammenfuehren(self, teile):
        if not teile:
            leer = {k: np.zeros(0) for k in self.SCHLUESSEL}
            leer["q"], leer["sicht"] = np.zeros((0, 4)), np.zeros((0, 2))
            for k in ("koll", "schatten", "akteur", "haupt", "haengend"):
                leer[k] = np.zeros(0, dtype=bool)
            for k in ("ci", "cj"):
                leer[k] = np.zeros(0, dtype=np.int64)
            leer["gid"] = np.zeros(0, dtype=U64)
            leer["pfad"], leer["rolle"], leer["klasse"] = (np.zeros(0, dtype=object), np.zeros(0, dtype="<U12"), np.zeros(0, dtype="<U12"))
            return leer
        return {k: np.concatenate([t[k] for t in teile]) for k in self.SCHLUESSEL}

    def budget(self, a):
        """Harte Deckel (KONVENTIONEN §3): je Rolle, gesamt, Kollision, Akteure. Runde 2: Ausdünnung nach Gruppen-Priorität
        (ganze Gruppen zuerst statt einzelner Stücke vieler Gruppen; Kiesel nach Instanz-Hash); Kollision über dem Deckel wird bei
        den kleinsten Stücken abgeschaltet (Stück bleibt sichtbar). Jede Änderung mit WARNUNG im Log und in hinweise."""
        B = self.R["budget"]
        n = len(a["x"])
        if n == 0:
            return a
        keep = np.ones(n, dtype=bool)
        rolle = a["rolle"]
        grund = {}

        def ordnung(s, gruppe):
            if gruppe:
                return s[np.lexsort((-a["prio"][s], -a["gprio"][s]))]
            return s[np.argsort(-a["prio"][s], kind="stable")]

        def weg(idx, g):
            if len(idx):
                keep[idx] = False
                grund[g] = grund.get(g, 0) + int(len(idx))
        for ro, cap in B.get("je_rolle", {}).items():
            s = np.nonzero(keep & (rolle == ro))[0]
            if len(s) > cap:
                weg(ordnung(s, ro != "kiesel")[: len(s) - cap], "%s>%d" % (ro, cap))
        for ro in ["kiesel", "stein", "platte", "block", "band"]:
            ng = int(keep.sum())
            if ng <= B["gesamt"]:
                break
            s = np.nonzero(keep & (rolle == ro))[0]
            weg(ordnung(s, ro != "kiesel")[: min(len(s), ng - B["gesamt"])], "gesamt>%d" % B["gesamt"])
        nk = int((keep & a["koll"]).sum())
        if nk > B["kollision"]:
            s = np.nonzero(keep & a["koll"])[0]
            s = s[np.lexsort((a["prio"][s], a["hoehe_m"][s]))][: nk - B["kollision"]]  # kleinste zuerst
            a["koll"][s] = False
            grund["kollision>%d (abgeschaltet, Stueck bleibt)" % B["kollision"]] = int(len(s))
        s = np.nonzero(keep & a["akteur"])[0]
        if len(s) > B["akteure"]:
            kleinste = s[np.argsort(a["hoehe_m"][s], kind="stable")[: len(s) - B["akteure"]]]
            a["akteur"][kleinste] = False
            log("Hinweis Budget: %d kleinste Akteure als Foliage gesetzt (Akteure <= %d)." % (len(kleinste), B["akteure"]))
        if grund:
            txt = "%d von %d Instanzen deterministisch ausgeduennt bzw. Kollision abgeschaltet (%s)" % (int((~keep).sum()), n, ", ".join(
                "%s: %d" % (g, k) for g, k in grund.items()))
            log("WARNUNG Budget: " + txt)
            self.hinweise.append("Budget: " + txt)
            if any(g.startswith(("kiesel", "stein", "gesamt")) for g in grund):
                self.hinweise.append("Kleinzeug (kiesel/stein) ausgeduennt: Geroellsaum bevorzugt ueber Landschafts-Gras bzw. "
                                     "Bodenlagen Kies/Geroell darstellen (KONVENTIONEN §3).")
        ziel = int(B.get("ziel", 52000))
        if int(keep.sum()) > ziel:
            log("Hinweis Budget: %d Instanzen ueber Zielwert %d (Deckel %d)." % (int(keep.sum()), ziel, B["gesamt"]))
            self.hinweise.append("Instanzen ueber Zielwert %d (Deckel %d)" % (ziel, B["gesamt"]))
        return {k: v[keep] for k, v in a.items()}

    @staticmethod
    def min_randabstand(px, py, bx, by, br):
        """Kleinster Abstand (m) von Punkten zum Rand großer Stücke (Kreis um Mitte mit Radius br); exakt, in Blöcken nach x sortiert."""
        out = np.full(len(px), np.inf)
        if len(px) == 0 or len(bx) == 0:
            return out
        o = np.argsort(bx, kind="stable")
        bx, by, br = bx[o], by[o], br[o]
        reich = float(br.max()) + 3.0
        op = np.argsort(px, kind="stable")
        for s0 in range(0, len(op), 2048):
            s = op[s0:s0 + 2048]
            lo = np.searchsorted(bx, px[s].min() - reich)
            hi = np.searchsorted(bx, px[s].max() + reich, side="right")
            if hi > lo:
                d = np.hypot(px[s][:, None] - bx[None, lo:hi], py[s][:, None] - by[None, lo:hi]) - br[None, lo:hi]
                out[s] = d.min(axis=1)
        return out

    def kleinmaterial_maske(self, a):
        KM = self.R.get("kleinmaterial", {})
        pl = np.array([self.ist_platte(r, p) for r, p in zip(a["rolle"], a["pfad"])], dtype=bool) if len(a["x"]) else np.zeros(0, bool)
        klein = ((a["rolle"] == "kiesel") | (a["hoehe_m"] < float(KM.get("hoehe_max_m", 0.5)))) & ~a["haengend"] & ~pl
        gross = (np.isin(a["rolle"], KM.get("gross_rollen", ["hero", "wand", "band", "block", "stein"])) |
                 (a["hoehe_m"] >= float(KM.get("gross_ab_m", 0.5)))) & ~klein & ~pl
        return klein, gross

    def kontaktsaum(self, a):
        """Kleinmaterial (Kiesel, Steine < hoehe_max_m) nur im Kontaktsaum: Abstand zum Rand eines großen Stücks <= saum_m.
        Nach dem Budget: verwaiste Säume (großes Stück ausgedünnt/verworfen) fallen weg."""
        KM = self.R.get("kleinmaterial")
        if not KM or len(a["x"]) == 0:
            self.km_stat = {"kleinmaterial": 0, "entfernt_ausserhalb_saum": 0}
            return a
        klein, gross = self.kleinmaterial_maske(a)
        d = self.min_randabstand(a["x"][klein] / 100.0, a["y"][klein] / 100.0, a["x"][gross] / 100.0, a["y"][gross] / 100.0,
                                 a["r_m"][gross])
        raus = np.zeros(len(a["x"]), dtype=bool)
        raus[np.nonzero(klein)[0][d > float(KM["saum_m"])]] = True
        self.km_stat = {"kleinmaterial": int(klein.sum() - raus.sum()), "entfernt_ausserhalb_saum": int(raus.sum())}
        if raus.any():
            log("Kontaktsaum: %d von %d Kleinmaterial-Stuecken ohne grosses Stueck in <= %.1f m entfernt (verwaist nach Budget/Pruefung)." % (
                int(raus.sum()), int(klein.sum()), float(KM["saum_m"])))
        return {k: v[~raus] for k, v in a.items()}

    def form_statistik(self, a):
        """Kennzahlen der Gruppengrammatik (nach Budget und Kontaktsaum): Gruppen je Klasse, Hauptfels-Höhen, Gruppenbreite,
        Satellitenabstand, Platten auf Gras, Kleinmaterial außerhalb des Saums. Steht in plan.json statistik.form und im Log."""
        def q(v, p):
            return round(float(np.percentile(v, p)), 2) if len(v) else None
        st = {}
        if len(a["x"]) == 0:
            self.form_stat = st
            return
        haupt = a["haupt"]
        form_kl = ["grat", "kuppe", "prallhang", "einzel", "band", "wand"]
        st["gruppen_je_klasse"] = {k: int((haupt & (a["klasse"] == k)).sum()) for k in KLASSEN if (haupt & (a["klasse"] == k)).any()}
        st["gruppen"] = int(sum(st["gruppen_je_klasse"].values()))
        hero = haupt & np.isin(a["klasse"], ["grat", "kuppe", "prallhang"])
        st["hauptfels_grat_kuppe"] = {"anzahl": int(hero.sum()), "davon_rolle_hero": int((hero & (a["rolle"] == "hero")).sum()),
                                      "sichtbar_m": {"min": q(a["sicht_h"][hero], 0), "median": q(a["sicht_h"][hero], 50),
                                                     "max": q(a["sicht_h"][hero], 100)},
                                      "netzhoehe_x_massstab_m": {"median": q(a["hoehe_m"][hero], 50), "max": q(a["hoehe_m"][hero], 100)},
                                      "massstab": {"median": q(a["sz"][hero], 50), "max": q(a["sz"][hero], 100)}}
        # Gruppenbreite: Durchmesser des Kreises um den Hauptfels, der alle Stücke >= 0,5 m der Gruppe enthält
        big = a["rolle"] != "kiesel"
        hidx = np.nonzero(haupt)[0]
        breite = {}
        if len(hidx):
            og = np.argsort(a["gid"][hidx], kind="stable")
            hg = a["gid"][hidx][og]
            s = np.nonzero(big)[0]
            pos = np.searchsorted(hg, a["gid"][s])
            pos_c = np.minimum(pos, len(hg) - 1)
            da = hg[pos_c] == a["gid"][s]
            s, pos_c = s[da], pos_c[da]
            h = hidx[og][pos_c]
            ext = np.hypot(a["x"][s] - a["x"][h], a["y"][s] - a["y"][h]) / 100.0 + a["r_m"][s]
            emax = np.zeros(len(hg))
            np.maximum.at(emax, pos_c, ext)
            b = 2.0 * emax
            kl = a["klasse"][hidx][og]
            for name, kls in (("form", ["grat", "kuppe", "prallhang"]), ("band", ["band"]), ("wand", ["wand"]), ("einzel", ["einzel"]),
                              ("blockstrom_laenge", ["fuss", "blockstrom"])):
                m = np.isin(kl, kls)
                w_ = emax[m] if name == "blockstrom_laenge" else b[m]  # Blockstrom: Länge ab Kopfblock-Mitte
                if m.any():
                    breite[name] = {"p10": q(w_, 10), "median": q(w_, 50), "p90": q(w_, 90), "max": q(w_, 100)}
        st["gruppenbreite_m"] = breite
        dr = a["dist_r"][np.isfinite(a["dist_r"]) & np.isin(a["klasse"], form_kl)]
        st["satellitenabstand_r"] = {"anzahl": int(len(dr)), "median": q(dr, 50), "p95": q(dr, 95), "max": q(dr, 100)}
        # Platten: auf Gras = Lagen-Maske verletzt (Gras/Wiese >= 100 und keine Kies/Geroell/Fels-Lage >= 100)
        pl = np.array([self.ist_platte(r, p) for r, p in zip(a["rolle"], a["pfad"])], dtype=bool)
        st["platten"] = {"anzahl": int(pl.sum()), "auf_gras": int((pl & self.m_gras[a["ci"], a["cj"]]).sum()),
                         "ohne_kies_fels_lage": int((pl & ~self.m_platte[a["ci"], a["cj"]]).sum()),
                         "verworfen_platten_regel": int(self.platten_verworfen)}
        klein, gross = self.kleinmaterial_maske(a)
        d = self.min_randabstand(a["x"][klein] / 100.0, a["y"][klein] / 100.0, a["x"][gross] / 100.0, a["y"][gross] / 100.0,
                                 a["r_m"][gross])
        saum = float(self.R.get("kleinmaterial", {}).get("saum_m", 2.0))
        st["kleinmaterial"] = {"anzahl": int(klein.sum()), "anteil_an_instanzen": round(float(klein.mean()), 3),
                               "ausserhalb_saum": int((d > saum).sum()), "randabstand_m": {"median": q(d, 50), "max": q(d, 100)},
                               "entfernt_ausserhalb_saum": int(getattr(self, "km_stat", {}).get("entfernt_ausserhalb_saum", 0))}
        st["netzwahl_rueckfall"] = {k: int(v) for k, v in sorted(self.form_rueckfall.items())}
        st["kammzellen"] = int(getattr(self, "kamm_zellen", 0))
        self.form_stat = st
        hf = st["hauptfels_grat_kuppe"]["sichtbar_m"]
        log("Form: %d Gruppen %s; Hauptfels Grat/Kuppe sichtbar median %s m, max %s m; Breite Formgruppen median %s m (p10 %s, p90 %s); "
            "Satellitenabstand max %s x R; Platten %d (auf Gras %d); Kleinmaterial %d, ausserhalb Saum %d" % (
                st["gruppen"], st["gruppen_je_klasse"], hf["median"], hf["max"], breite.get("form", {}).get("median"),
                breite.get("form", {}).get("p10"), breite.get("form", {}).get("p90"), st["satellitenabstand_r"]["max"],
                st["platten"]["anzahl"], st["platten"]["auf_gras"], st["kleinmaterial"]["anzahl"], st["kleinmaterial"]["ausserhalb_saum"]))

    def pruefkameras(self, a):
        """Kamera-Vorschläge (Weltkoordinaten cm, UE-Yaw/Pitch in Grad): Grat-Blick aus ~300 m quer zur Gratachse auf die höchste
        Felskrone, Blockstrom-Blick 120 m hangabwärts, Kuppe aus 200 m. Höhe: Gelände am Kamerapunkt (im Fenster) + Angabe."""
        cams = []
        H, W = self.h.shape
        i0, _, j0, _ = self.win

        def kamera(name, k, abstand, richtung, ueber, zweck):
            zx, zy = a["x"][k] / 100.0, a["y"][k] / 100.0
            zz = a["z"][k] / 100.0 + a["hoehe_m"][k] * 0.5
            cx, cy = zx + np.cos(richtung) * abstand, zy + np.sin(richtung) * abstand
            fi, fj = cy + Y0 - i0, cx + X0 - j0
            inn = (1 <= fi < H - 1) and (1 <= fj < W - 1)
            boden = float(bilinear(self.h, np.array([fi]), np.array([fj]))[0]) if inn else zz - 0.5 * abstand * 0.3
            cz = max(boden, 0.0) + ueber
            cams.append({"name": name, "x_cm": round(cx * 100), "y_cm": round(cy * 100), "z_cm": round(cz * 100),
                         "yaw_grad": round(math.degrees(math.atan2(zy - cy, zx - cx)), 1),
                         "pitch_grad": round(math.degrees(math.atan2(zz - cz, abstand)), 1),
                         "ziel_cm": [round(zx * 100), round(zy * 100), round(zz * 100)], "zweck": zweck,
                         "boden_aus": "hoehe.f32" if inn else "geschaetzt (ausserhalb Fenster)"})
        hk = np.nonzero(a["haupt"] & (a["klasse"] == "grat"))[0]
        if len(hk):
            k = hk[np.argmax(a["z"][hk])]
            achse = self.gratachse[a["ci"][k], a["cj"][k]]
            # Seite mit dem tieferen Gelände (freie Sicht auf den Kamm)
            best = None
            for s in (1.0, -1.0):
                r = achse + s * 0.5 * np.pi
                fi = a["fi"][k] + np.sin(r) * 150.0
                fj = a["fj"][k] + np.cos(r) * 150.0
                hz = float(bilinear(self.h, np.clip(np.array([fi]), 1, H - 1.001), np.clip(np.array([fj]), 1, W - 1.001))[0])
                if best is None or hz < best[0]:
                    best = (hz, r)
            kamera("grat_300m", k, 300.0, best[1], 60.0, "Felskrone als Kette auf dem Kamm, Hauptfelsen 4-10 m als Form lesbar")
            kamera("grat_120m", k, 120.0, best[1], 25.0, "Gruppe nah: Satelliten eng am Hauptfels, Kieselsaum nur am Fuss")
        hf = np.nonzero(a["haupt"] & (a["klasse"] == "fuss"))[0]
        if len(hf):
            k = hf[np.argmax(a["hoehe_m"][hf])]
            ab = self.abfall[a["ci"][k], a["cj"][k]]
            kamera("blockstrom_120m", k, 120.0, math.atan2(ab[1], ab[0]), 15.0,
                   "Blockstrom am Wandfuss: Kopfblock an der Wand, Groesse hangabwaerts abnehmend")
        hq = np.nonzero(a["haupt"] & (a["klasse"] == "kuppe"))[0]
        if len(hq):
            k = hq[np.argmax(a["z"][hq])]
            kamera("kuppe_200m", k, 200.0, -0.75 * np.pi, 40.0, "Kuppe mit Hauptfels und Satelliten")
        self.kameras = cams

    # Ausgabe --------------------------------------------------------------------------------------------------------
    def schreiben(self, feld, a, welt_dir):
        AU = self.R["ausgabe"]
        out = os.path.join(self.basis, AU["ordner"], feld)
        os.makedirs(out, exist_ok=True)
        for fn in os.listdir(out):
            if fn.endswith(".f32"):
                os.remove(os.path.join(out, fn))
        dateien = {}
        akteure = []
        n = len(a["x"])
        if n:
            rec = np.column_stack([a["x"], a["y"], a["z"], a["q"], a["sx"], a["sy"], a["sz"]]).astype("<f4")
            # Kollision ist im Setzer eine Eigenschaft des Foliage-Typs (je Datei): Instanzen mit Kollision stehen deshalb in
            # eigener Datei <Netz>_kol.f32, damit kollision_anzahl genau dem entspricht, was der Setzer mit Kollision setzt.
            schluessel = np.char.add(np.char.add(np.where(a["akteur"], "akteur_", "").astype(str),
                                                 np.array([self.netze[p]["name"] for p in a["pfad"]]).astype(str)),
                                     np.where(a["koll"].astype(bool), "_kol", "").astype(str))
            for key in np.unique(schluessel):
                s = np.nonzero(schluessel == key)[0]
                rec[s].tofile(os.path.join(out, key + ".f32"))
                pf = a["pfad"][s[0]]
                ist_akteur = bool(a["akteur"][s[0]])
                sicht = a["sicht"][s]
                sw = [0, 0] if (sicht[:, 1] == 0).any() else [int(sicht[:, 0].min()), int(sicht[:, 1].max())]
                rollen = sorted(set(a["rolle"][s].tolist()))
                dateien[key] = {"pfad": pf, "anzahl": int(len(s)), "gruppe": "/".join(rollen), "ebene": "felsgruppen",
                                "rolle": "akteur" if ist_akteur else "fels", "sichtweite": sw,
                                "schatten": bool(a["schatten"][s].any()), "kollision": bool(a["koll"][s].any()),
                                "nanite": bool(self.netze[pf]["nanite"]),
                                "klassen": sorted(set(a["klasse"][s].tolist()))}
                if ist_akteur:
                    for k in s:
                        akteure.append({"netz": self.netze[pf]["name"], "pfad": pf, "rolle": "akteur", "klasse": str(a["klasse"][k]),
                                        "x": float(a["x"][k]), "y": float(a["y"][k]), "z": float(a["z"][k]),
                                        "qx": float(a["q"][k, 0]), "qy": float(a["q"][k, 1]), "qz": float(a["q"][k, 2]), "qw": float(a["q"][k, 3]),
                                        "sx": float(a["sx"][k]), "sy": float(a["sy"][k]), "sz": float(a["sz"][k]),
                                        "hoehe_m": round(float(a["hoehe_m"][k]), 2)})
        stat = dict(self.statistik)
        stat["je_rolle"] = {ro: int((a["rolle"] == ro).sum()) for ro in ROLLEN_ORDNUNG}
        stat["kollision"] = int(a["koll"].sum())
        stat["akteure"] = len(akteure)
        stat["zusatzklassen"] = dict(getattr(self, "zusatz_stat", {}))
        stat["mindestdichte"] = {BIOME[b]: {"soll_je_ha": float(self.mindest[b]), "hauptstuecke_relief": int(self.haupt_je_biom[b])}
                                 for b in np.nonzero(self.mindest > 0)[0] if BIOME[b] in self.biome_fenster}
        stat["form"] = dict(getattr(self, "form_stat", {}))
        plan = plan_kopf(self.R, feld, int(n), self.stand)
        plan.update({"biome_fenster": self.biome_fenster, "zellen_zustaendig": int(self.zellen_zustaendig),
                     "kollision_anzahl": int(a["koll"].sum()), "biom_quelle": self.biom_quelle,
                     "dateien": dateien, "akteure": akteure, "seed": self.seed, "faktor": self.faktor,
                     "paletten_je_biom": {bn: self.pal_je_biom[BIOME.index(bn)] for bn in self.biome_fenster},
                     "overrides": {"aktiv_je_biom": {bn: o for bn, o in self.ov_aktiv.items() if bn in self.biome_fenster},
                                   "dateien": self.ov_info},
                     "pruefkameras": list(getattr(self, "kameras", [])), "gesperrt": sorted(self.gesperrt),
                     "hinweise": list(self.hinweise), "statistik": stat})
        with open(os.path.join(out, "plan.json"), "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=1)
        log("geschrieben: %s (%d Dateien, %d Akteure)" % (out, len(dateien), len(akteure)))

    def bild(self, feld, a):
        try:
            from PIL import Image
        except Exception:
            log("Hinweis: Pillow fehlt – kein Bild.")
            return
        AU = self.R["ausgabe"]
        i0, i1, j0, j1 = self.win
        i0f, i1f, j0f, j1f = self.feld_box
        si, sj = i0f - i0, j0f - j0
        H, W = i1f - i0f, j1f - j0f
        n = self.normal[si:si + H, sj:sj + W]
        licht = np.array([-0.5, -0.5, 0.707]); licht /= np.linalg.norm(licht)
        shade = np.clip((n * licht).sum(2), 0, 1) * 0.7 + 0.2
        img = np.stack([shade] * 3, axis=2) * 255
        wz = self.m_wasser_roh[si:si + H, sj:sj + W]
        img[wz] = [40, 80, 180]
        img[~self.land[si:si + H, sj:sj + W]] = [20, 40, 120]
        w = self.m_wand[si:si + H, sj:sj + W]
        img[w] = img[w] * 0.6 + np.array([80, 60, 40]) * 0.4
        img = img.astype(np.uint8)
        if len(a["x"]):
            ci = a["ci"] - si; cj = a["cj"] - sj
            ok = (ci >= 0) & (ci < H) & (cj >= 0) & (cj < W)
            farben = {k: np.array(v["farbe"], dtype=np.uint8) for k, v in self.R["klassen"].items()}
            # Runde 2: Stücke als Scheibe mit ihrem Fußradius (1 px = 1 m), damit die Gruppenform in der Draufsicht lesbar ist
            rad = np.clip(np.round(a["r_m"]), 0, 9).astype(np.int64)
            rad[a["rolle"] == "kiesel"] = 0
            for rolle in ["kiesel", "stein", "platte", "block", "band", "wand", "hero"]:
                s = ok & (a["rolle"] == rolle)
                if not s.any():
                    continue
                for kl in np.unique(a["klasse"][s]):
                    ss = s & (a["klasse"] == kl)
                    col = farben.get(kl, np.array(self.R.get("zusatz", {}).get("farbe", [255, 255, 255]), dtype=np.uint8))
                    if rolle == "kiesel":
                        col = (col.astype(int) * 0.5 + 100).astype(np.uint8)
                    elif rolle == "platte":
                        col = np.array([240, 240, 240], dtype=np.uint8)
                    elif rolle in ("block", "stein"):
                        col = (col.astype(int) * 0.75).astype(np.uint8)
                    for r in np.unique(rad[ss]):
                        sr = ss & (rad == r)
                        for di in range(-r, r + 1):
                            for dj in range(-r, r + 1):
                                if di * di + dj * dj > r * r + r:
                                    continue
                                ii = np.clip(ci[sr] + di, 0, H - 1); jj = np.clip(cj[sr] + dj, 0, W - 1)
                                img[ii, jj] = col
        pfad = os.path.join(self.basis, AU["bild"])
        os.makedirs(pfad, exist_ok=True)
        Image.fromarray(img, "RGB").save(os.path.join(pfad, feld + ".png"))
        log("Bild: %s" % os.path.join(pfad, feld + ".png"))


# ----------------------------------------------------------------------------------------------------------------------
def plan_kopf(R, feld, n, stand):
    """Gemeinsame Pflichtschlüssel (FORMAT §3, KONVENTIONEN §2) für vollen und leeren plan.json."""
    AU = R["ausgabe"]
    return {"stand": stand, "feld": feld, "instanzen": int(n), "ebene": "felsgruppen", "biome_eigen": list(BIOME),
            "biome_fenster": {}, "zellen_zustaendig": 0, "kollision_anzahl": 0, "dateien": {}, "akteure": [],
            "entfernen": AU.get("entfernen", ""), "ft_ordner": AU["ft_ordner"], "ft_praefix": AU["ft_praefix"],
            "quelle": "felsgruppen_plan.py (Korrektur Runde 2: Gruppengrammatik, Platten-Regel, Kontaktsaum, Sperrliste)",
            "hinweis_setzer": "Eintraege mit rolle 'akteur' (Dateien akteur_*.f32, Liste 'akteure') als StaticMeshActor setzen, "
                              "nicht als Foliage; Kollision nur wo kollision=true; Z enthaelt bereits das Eingraben.",
            "hinweise": []}


def schreibe_leeren_plan(basis, R, feld, grund):
    """Leerer plan.json (instanzen 0, keine f32) statt Textabbruch, z. B. nach einem Fehler im Feld."""
    out = os.path.join(basis, R["ausgabe"]["ordner"], feld)
    os.makedirs(out, exist_ok=True)
    for fn in os.listdir(out):
        if fn.endswith(".f32"):
            os.remove(os.path.join(out, fn))
    plan = plan_kopf(R, feld, 0, "regeln %s" % R.get("_doku", {}).get("stand", "?"))
    plan["hinweise"] = [ascii_text(grund)]
    plan["fehler"] = ascii_text(grund)
    with open(os.path.join(out, "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    log("leerer plan.json geschrieben: %s (%s)" % (out, grund))


# ----------------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Felsgruppen-Planer Eldarien (Auftrag 11 C, Korrektur Runde 2).")
    ap.add_argument("felder", nargs="+", help="Gitterfelder, z. B. B4 C2")
    ap.add_argument("--bild", action="store_true", help="Draufsicht docs/pruefung/felsgruppen/<Feld>.png")
    ap.add_argument("--faktor", type=float, default=1.0, help="Dichtefaktor (Standard 1.0)")
    ap.add_argument("--basis", default=".", help="production-Wurzel")
    ap.add_argument("--regeln", default=None, help="felsgruppen_regeln.json")
    ap.add_argument("--overrides-ordner", default=None, help="Ordner mit den Biom-Regeldateien (<thema>_regeln.json)")
    ap.add_argument("--ohne-overrides", action="store_true", help="felsgruppen_overrides der Biom-Planer nicht lesen")
    args = ap.parse_args()
    skriptdir = os.path.dirname(os.path.abspath(__file__))
    regeln = args.regeln
    if regeln is None:
        for p in [os.path.join(skriptdir, "felsgruppen_regeln.json"), os.path.join(args.basis, "scripts", "felsgruppen", "felsgruppen_regeln.json")]:
            if os.path.isfile(p):
                regeln = p
                break
    if regeln is None or not os.path.isfile(regeln):
        abbruch("Pflichtdatei fehlt: felsgruppen_regeln.json (--regeln PFAD)")
    try:
        with open(regeln, encoding="utf-8") as f:
            R = json.load(f)
    except Exception as e:
        abbruch("felsgruppen_regeln.json unlesbar: %s" % e)
    log("Regeln: %s (Seed %s), numba: %s" % (regeln, R.get("seed"), "ja" if HAVE_NUMBA else "nein (NumPy-Fallback)"))
    welt_dir = os.path.join(args.basis, "export", "unreal", "welt")
    if not os.path.isdir(welt_dir):
        abbruch("Ordner fehlt: %s (production-Wurzel mit --basis angeben)" % welt_dir)
    netze = lade_netze(args.basis, skriptdir)
    masse = lade_masse(args.basis, skriptdir)
    if args.ohne_overrides:
        ov, ov_info, zusatz = {}, {}, []
        log("Overrides: abgeschaltet (--ohne-overrides).")
    else:
        ov, ov_info, zusatz = lade_overrides(R, regeln, args.basis, skriptdir, args.overrides_ordner, netze)
    pl = Planer(R, netze, masse, args.basis, args.faktor, skriptdir, ov, ov_info, zusatz)
    for feld in args.felder:
        try:
            feld_bereich(feld)
        except ValueError as e:
            log("FEHLER: %s - Feld uebersprungen." % e)
            continue
        try:
            pl.plane_feld(feld.upper(), welt_dir, args.bild)
        except SystemExit:
            raise
        except Exception as e:  # klare Meldung, leerer plan.json, weiter mit nächstem Feld
            import traceback
            for zeile in traceback.format_exc().rstrip().splitlines():
                log("  " + zeile)
            log("FEHLER in Feld %s: %s" % (feld, e))
            schreibe_leeren_plan(args.basis, R, feld.upper(), "Fehler im Planer: %s" % e)


if __name__ == "__main__":
    main()
