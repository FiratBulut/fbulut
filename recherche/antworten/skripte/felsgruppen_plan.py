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
             "punkte": None, "felder": None, "zonen": None, "fuss_m": 22.0, "dichte_gruppen": False, "gelesen": [], "ignoriert": []}
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
        info[datei] = {"biome": biome, "status": "gelesen", "biome_mit_aenderung": sorted(erg), "gelesen": L.gelesen,
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

        # Lagen (optional) → Faktor
        lagen = R.get("lagen", {})
        fels = np.zeros_like(h)
        for ln in lagen.get("fels_boost", []):
            a = lade_raster(os.path.join(welt_dir, "lage_%s.r8" % ln), np.uint8, win, name="lage_%s.r8" % ln)
            if a is not None:
                fels = np.maximum(fels, a / 255.0)
        ger = np.zeros_like(h)
        for ln in lagen.get("geroell_boost", []):
            a = lade_raster(os.path.join(welt_dir, "lage_%s.r8" % ln), np.uint8, win, name="lage_%s.r8" % ln)
            if a is not None:
                ger = np.maximum(ger, a / 255.0)
        schnee = lade_raster(os.path.join(welt_dir, "lage_%s.r8" % lagen.get("schnee_hemmung", "Schnee")), np.uint8, win, name="lage_Schnee.r8")
        schnee = schnee / 255.0 if schnee is not None else np.zeros_like(h)
        fmin, fmax = lagen.get("faktor_min", 0.5), lagen.get("faktor_max", 1.5)
        self.f_fels = np.clip(0.6 + 0.9 * fels - 0.3 * schnee, fmin, fmax)
        self.f_ger = np.clip(0.7 + 0.8 * ger, fmin, fmax)

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
        hs25 = gauss(h, G["massiv_sigma_m"])
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
        for kname in KLASSEN:  # "einzel" zuletzt: füllt nur bis mindestdichte_je_ha auf
            if kname == "prallhang":
                g = self.kandidaten_prallhang(welt_dir)
            elif kname == "kuppe":
                g = self.kandidaten_kuppe()
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
        self._abst_cache = {}
        self._lage_cache = {}
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
        K = self.R["klassen"][kname]
        salz = {"grat": 11, "band": 12, "wand": 13, "fuss": 14, "blockstrom": 15}[kname]
        fi, fj, hsh = self._gitterpunkte(K["raster_m"], salz)
        ci, cj = np.round(fi).astype(np.int64), np.round(fj).astype(np.int64)
        hang = self.hang[ci, cj]
        ok = self.m_frei[ci, cj] & (hang >= K["hang_grad"][0]) & (hang <= K["hang_grad"][1])
        p = np.full(len(ci), K["p"] * self.faktor)
        if kname == "grat":
            ok &= (self.grat[ci, cj] >= K["grat_staerke_min"]) & ~self.m_mulde[ci, cj]
            p *= self.f_fels[ci, cj] * np.clip(self.grat[ci, cj] / (3 * K["grat_staerke_min"]), 0.5, 1.5)
            yaw = self.gratachse[ci, cj]
        elif kname == "band":
            ok &= self.m_band[ci, cj] & ~self.m_mulde[ci, cj] & (self.grat[ci, cj] > -0.01)
            p *= self.f_fels[ci, cj]
            yaw = self.strike[ci, cj]
        elif kname == "wand":
            ok &= (self.grat[ci, cj] >= K["nase_min"])
            p *= self.f_fels[ci, cj]
            yaw = self.strike[ci, cj]
        elif kname == "fuss":
            ok &= (self.fuss_stufe[ci, cj] >= 0) & ~self.m_wand[ci, cj] & ~self.m_mulde[ci, cj]
            p *= self.f_ger[ci, cj]
            yaw = np.arctan2(self.abfall[ci, cj, 1], self.abfall[ci, cj, 0])
        else:  # blockstrom
            ok &= self.wand_ueber_128[ci, cj] & (self.hohl25[ci, cj] >= K["hohl_min"]) & ~self.m_wand[ci, cj]
            p *= self.f_ger[ci, cj]
            yaw = np.arctan2(self.abfall[ci, cj, 1], self.abfall[ci, cj, 0])
        erl, bf = self._klasse_erlaubt(kname, ci, cj)
        ok &= erl & (uni(hsh, 5) < p * bf)
        return {"ci": ci[ok], "cj": cj[ok], "fi": fi[ok], "fj": fj[ok], "h": hsh[ok], "yaw": yaw[ok],
                "stufe": self.fuss_stufe[ci[ok], cj[ok]] if kname == "fuss" else None}

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

    # Gruppen → Instanzen -------------------------------------------------------------------------------------------
    def gruppe_erzeugen(self, kname, g):
        K = self.R["klassen"][kname]
        GR = self.R["gruppe"]
        biom_g = self.biom[g["ci"], g["cj"]]
        teile = []
        for bi in np.unique(biom_g):  # je Biom: Palette, Rollen-Parameter und Kieselfaktor des Bioms (inkl. Overrides)
            sel = biom_g == bi
            pal = self.pal_je_biom[int(bi)]
            K = self.klasse_param(kname, bi)
            gi, gj, gh, gyaw = g["fi"][sel], g["fj"][sel], g["h"][sel], g["yaw"][sel]
            stufe = g["stufe"][sel] if g.get("stufe") is not None else None
            n = len(gi)
            # Hauptstück: hero (mit Wahrscheinlichkeit) sonst block / band / wand / stufenrolle
            haupt_rolle = np.full(n, "block", dtype=object)
            erl_einzel = self.einzel_rollen.get(int(bi)) if kname == "einzel" else None
            if kname in ("grat", "kuppe", "prallhang", "einzel") and (erl_einzel is None or "hero" in erl_einzel):
                haupt_rolle[uni(gh, 20) < K["hero_p"]] = "hero"
            elif kname == "band":
                haupt_rolle[:] = "band"
            elif kname == "wand":
                haupt_rolle[:] = "wand"
            elif kname == "fuss":
                st = np.array(K["stufen"], dtype=object)
                haupt_rolle = np.array([st[s][2] for s in stufe], dtype=object)
            # Anzahl Nebenstücke je Rolle
            def anzahl(rolle, salz):
                if rolle not in K:
                    return np.zeros(n, dtype=np.int64)
                lo, hi = K[rolle]
                return ganz(gh, salz, lo, hi)
            plan = []  # (rolle, anzahl-array, ist_haupt, radius-faktor-bereich, salz)
            plan.append(("__haupt__", np.ones(n, dtype=np.int64), True, (0, 0), 30))
            if kname == "band":
                plan.append(("band", np.maximum(anzahl("band", 31) - 1, 0), False, (0.7, 0.9), 31))
            elif kname == "wand":
                plan.append(("wand", np.maximum(anzahl("wand", 31) - 1, 0), False, (0.7, 0.9), 31))
                plan.append(("block", anzahl("block", 32), False, GR["neben_abstand_hero_r"], 32))
            elif kname == "fuss":
                plan.append(("__stufe__", np.maximum(anzahl("n", 31) - 1, 0), False, (0.8, 1.6), 31))
            else:
                plan.append(("block", anzahl("block", 32), False, GR["neben_abstand_hero_r"], 32))
            plan.append(("stein", anzahl("stein", 33), False, GR["stein_abstand_hero_r"], 33))
            if erl_einzel is not None:  # mindestdichte_klassen: nur diese Rollen als Nebenstücke (Kieselsaum bleibt)
                plan = [e for e in plan if e[0] == "__haupt__" or e[0] in erl_einzel]
            if self.paletten[pal].get("platte") and kname in ("blockstrom", "fuss", "kuppe"):
                plan.append(("platte", (uni(gh, 34) < 0.5).astype(np.int64), False, (1.0, 1.6), 34))
            # Hauptstück zuerst, um den Radius zu kennen
            haupt = self._stuecke(pal, kname, haupt_rolle, gi, gj, gh, gyaw, np.ones(n, dtype=np.int64), True, (0, 0), 30,
                                  None, stufe, bi=bi)
            if haupt is None:
                r_haupt = np.full(n, 150.0)
            else:
                r_haupt = haupt["r_haupt"]  # je Gruppe, cm
                teile.append(haupt)
                if kname != "einzel":
                    self.haupt_je_biom[int(bi)] += len(haupt["x"])  # Hauptstücke liegen alle im Feld (im_feld-Prüfung)
            for rolle, cnt, _, rb, salz in plan[1:]:
                if cnt.sum() == 0:
                    continue
                if rolle == "__stufe__":
                    rl = haupt_rolle
                else:
                    rl = np.full(n, rolle, dtype=object)
                t = self._stuecke(pal, kname, rl, gi, gj, gh, gyaw, cnt, False, rb, salz, r_haupt, stufe, bi=bi)
                if t is not None:
                    teile.append(t)
            # Kiesel-Saum (Kieselfaktor des Bioms aus Overrides skaliert Dichte und Spanne)
            kf = float(self.kiesel_f[int(bi)])
            if "kiesel" in K and self.paletten[pal].get("kiesel") and kf > 0:
                lo, hi = K["kiesel"]
                lo, hi = int(round(lo * kf)), max(int(round(lo * kf)), int(round(hi * kf)))
                ring0, ring1 = GR["kiesel_ring_m"]
                d0, d1 = GR["kiesel_dichte_je_m2"]
                rh = r_haupt / 100.0
                flaeche = np.pi * ((rh + ring1) ** 2 - (rh + ring0) ** 2)
                dichte = zwischen(gh, 35, d0, d1) * self.faktor * kf
                cnt = np.clip(np.round(flaeche * dichte), lo, hi).astype(np.int64)
                t = self._stuecke(pal, kname, np.full(n, "kiesel", dtype=object), gi, gj, gh, gyaw, cnt, False,
                                  (ring0, ring1), 36, r_haupt, stufe, ring=True, bi=bi)
                if t is not None:
                    teile.append(t)
        return [t for t in teile if t is not None and len(t["x"])]

    def _stuecke(self, pal, kname, rollen, gi, gj, gh, gyaw, cnt, ist_haupt, rb, salz, r_haupt, stufe, ring=False, bi=0):
        """Erzeugt cnt[k] Stücke je Gruppe k mit Rolle rollen[k]. Liefert Instanz-Arrays (oder None)."""
        K = self.klasse_param(kname, bi)
        GR = self.R["gruppe"]
        RO = self.R["rollen"]
        idx = np.repeat(np.arange(len(gi)), cnt)
        if len(idx) == 0:
            return None
        m = np.arange(len(idx)) - np.repeat(np.cumsum(cnt) - cnt, cnt)  # Mitgliedsindex in der Gruppe
        hh = hash64(gh[idx], salz, m)
        rollen_i = rollen[idx]
        x = np.zeros(len(idx)); y = np.zeros(len(idx)); z = np.zeros(len(idx))
        pf_idx = np.zeros(len(idx), dtype=np.int64)
        pfade_alle = np.empty(len(idx), dtype=object)
        H_cm = np.zeros(len(idx)); R_cm = np.zeros(len(idx)); MZ = np.zeros(len(idx))
        sk = np.zeros(len(idx)); bury = np.zeros(len(idx)); kipp = np.zeros(len(idx)); nu = np.zeros(len(idx))
        koll = np.zeros(len(idx), dtype=bool); schatten = np.zeros(len(idx), dtype=bool)
        sicht = np.zeros((len(idx), 2))
        rolle_arr = np.empty(len(idx), dtype=object)
        for rolle in np.unique(rollen_i):
            s = rollen_i == rolle
            pa = self.palette_arrays(pal, rolle)
            if pa is None:
                # Rolle ohne Netze in dieser Palette → nächstkleinere Rolle
                for ersatz in ("block", "stein", "kiesel"):
                    pa = self.palette_arrays(pal, ersatz)
                    if pa is not None:
                        rolle = ersatz
                        break
                if pa is None:
                    continue
            pfade, hc, rc, mz = pa
            k = np.minimum((uni(hh[s], 40) * len(pfade)).astype(np.int64), len(pfade) - 1)
            ro = self.rolle_param(bi, rolle)  # Grundregel + Biom-Override (massstab, eingraben, sichtweite_cm, kippen_grad)
            ov_eb = self.rollen_ov.get((int(bi), rolle), {}).get("eingraben")
            sk_s = zwischen(hh[s], 41, ro["massstab"][0], ro["massstab"][1])
            if kname == "fuss":
                st = K["stufen"]
                f0 = np.array([st[v][3] for v in stufe[idx[s]]]); f1 = np.array([st[v][4] for v in stufe[idx[s]]])
                sk_s = sk_s * zwischen(hh[s], 42, f0, f1)
            if not ist_haupt and rolle in ("block", "band", "wand"):
                sk_s *= zwischen(hh[s], 43, 0.55, 0.9)  # Größenstaffelung: Nebenstücke kleiner als das Hauptstück
            pfade_alle[s] = np.array(pfade, dtype=object)[k]
            H_cm[s] = hc[k]; R_cm[s] = rc[k]; MZ[s] = mz[k]; sk[s] = sk_s
            eb = ov_eb if ov_eb is not None else K.get("eingraben", RO[rolle]["eingraben"])  # Override > Klasse > Rolle
            bury[s] = zwischen(hh[s], 44, eb[0], eb[1])
            kipp[s] = np.radians(zwischen(hh[s], 45, ro["kippen_grad"][0], ro["kippen_grad"][1]))
            nu[s] = ro["nicht_uniform"]
            koll[s] = bool(ro["kollision"]); schatten[s] = bool(ro["schatten"]); sicht[s] = ro["sichtweite_cm"]
            rolle_arr[s] = rolle
        ok = np.array([p is not None for p in pfade_alle])
        if not ok.all():
            idx, m, hh, x, y = idx[ok], m[ok], hh[ok], x[ok], y[ok]
            pfade_alle, H_cm, R_cm, MZ, sk, bury, kipp, nu = (a[ok] for a in (pfade_alle, H_cm, R_cm, MZ, sk, bury, kipp, nu))
            koll, schatten, sicht, rolle_arr = koll[ok], schatten[ok], sicht[ok], rolle_arr[ok]
            if len(idx) == 0:
                return None
        r_eigen = R_cm * sk  # cm
        # Lage relativ zur Gruppenmitte
        gy = gyaw[idx]
        if ist_haupt:
            dist = np.zeros(len(idx)); ang = gy
        elif ring:
            dist = r_haupt[idx] + zwischen(hh, 46, rb[0], rb[1]) * 100.0
            ang = zwischen(hh, 47, 0, 2 * np.pi)
        elif rolle_arr[0] in ("band", "wand"):
            # entlang des Streichens aufgereiht, abwechselnd beide Seiten
            seite = np.where(m % 2 == 0, 1.0, -1.0)
            dist = (r_haupt[idx] + r_eigen) * zwischen(hh, 46, rb[0], rb[1]) * (1 + m // 2)
            ang = gy + np.where(seite > 0, 0.0, np.pi) + np.radians(zwischen(hh, 48, -8, 8))
        else:
            # Nebenblöcke/Steine: um die Hauptrichtung gestreut, Überlappung 10–30 % (nah) bzw. außen (Steine)
            streu = np.radians(GR["neben_yaw_streuung_grad"]) if rolle_arr[0] == "block" else np.pi
            seite = np.where(uni(hh, 49) < 0.5, 0.0, np.pi)
            ang = gy + seite + zwischen(hh, 48, -streu, streu)
            dist = (r_haupt[idx] + r_eigen) * zwischen(hh, 46, rb[0], rb[1])
            if kname in ("fuss", "blockstrom"):  # Falllinie: Stücke hangabwärts versetzt
                ang = gy + zwischen(hh, 48, -0.6, 0.6)
                dist = r_haupt[idx] * 0.5 + zwischen(hh, 46, rb[0], rb[1]) * 300.0
        fj = gj[idx] + np.cos(ang) * dist / 100.0
        fi = gi[idx] + np.sin(ang) * dist / 100.0
        # Gültigkeit: im Feld, frei
        i0, i1, j0, j1 = self.win
        i0f, i1f, j0f, j1f = self.feld_box
        H, W = self.h.shape
        inside = (fi >= 1) & (fi < H - 1) & (fj >= 1) & (fj < W - 1)
        fi_c = np.clip(fi, 1, H - 1.001); fj_c = np.clip(fj, 1, W - 1.001)
        ci, cj = np.round(fi_c).astype(np.int64), np.round(fj_c).astype(np.int64)
        im_feld = (fi + i0 >= i0f) & (fi + i0 < i1f) & (fj + j0 >= j0f) & (fj + j0 < j1f)
        klein = np.isin(rolle_arr.astype(str), ["stein", "kiesel", "platte"])
        frei = np.where(klein, self.m_frei_klein[ci, cj], self.m_frei[ci, cj] & ~self.m_sperr[ci, cj])
        # Floating-Check: Bodenhöhe unter dem Rand des Stücks darf nicht viel tiefer liegen als in der Mitte
        hz = bilinear(self.h, fi_c, fj_c)
        rr = np.clip(r_eigen / 100.0, 0.5, 20.0)
        hmin_rand = np.minimum.reduce([bilinear(self.h, np.clip(fi_c + d[0] * rr, 1, H - 1.001), np.clip(fj_c + d[1] * rr, 1, W - 1.001))
                                       for d in ((1, 0), (-1, 0), (0, 1), (0, -1))])
        # schwebend, wenn der Boden innerhalb des Stückradius tiefer abfällt als Eingrabtiefe + 60°-Hang erlauben
        nicht_schwebend = (hz - hmin_rand) <= bury * H_cm * sk / 100.0 + 0.3 + rr * np.tan(np.radians(60.0))
        ok = inside & im_feld & frei & nicht_schwebend
        if not ok.any():
            if ist_haupt:
                log("  %s/%s: alle %d Hauptstücke verworfen (im Fenster %d, im Feld %d, frei %d, nicht schwebend %d)" % (
                    kname, pal, len(ok), int(inside.sum()), int(im_feld.sum()), int(frei.sum()), int(nicht_schwebend.sum())))
            return None
        sel = ok
        idx, hh, fi, fj, ci, cj, hz = idx[sel], hh[sel], fi[sel], fj[sel], ci[sel], cj[sel], hz[sel]
        pfade_alle, H_cm, R_cm, MZ, sk, bury, kipp, nu = (a[sel] for a in (pfade_alle, H_cm, R_cm, MZ, sk, bury, kipp, nu))
        koll, schatten, sicht, rolle_arr, ang = koll[sel], schatten[sel], sicht[sel], rolle_arr[sel], ang[sel]
        gy = gyaw[idx]
        # Ausrichtung: Z auf Normale, Kippen in den Hang (Z-Achse Richtung bergauf), Yaw = Hauptrichtung ± Streuung
        n = self.normal[ci, cj]
        bergauf = -self.abfall[ci, cj]
        t = np.tan(kipp)[:, None]
        up = n + np.concatenate([bergauf * t, np.zeros((len(t), 1))], axis=1)
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        if rolle_arr[0] == "kiesel":
            yaw = zwischen(hh, 50, 0, 2 * np.pi)
        else:
            streu = np.radians(self.R["gruppe"]["yaw_streuung_grad"])
            yaw = gy + zwischen(hh, 50, -streu, streu)
        if kname == "band" or (kname == "wand"):
            # Schichtneigung: Z-Achse zusätzlich um die Streichrichtung um dip kippen
            d = self.dip[ci, cj]
            sv = np.stack([np.cos(gy), np.sin(gy), np.zeros_like(gy)], axis=1)  # Streichvektor
            # Rotation von up um sv um Winkel d (Rodrigues)
            up = up * np.cos(d)[:, None] + np.cross(sv, up) * np.sin(d)[:, None] + sv * (sv * up).sum(1, keepdims=True) * (1 - np.cos(d))[:, None]
            up /= np.linalg.norm(up, axis=1, keepdims=True)
        q = quat_aus_yaw_up(yaw, up)
        sx = sk * (1 + nu * (2 * uni(hh, 51) - 1))
        sy = sk * (1 + nu * (2 * uni(hh, 52) - 1))
        sz = sk
        x_cm = (fj + j0 - X0) * 100.0
        y_cm = (fi + i0 - Y0) * 100.0
        z_cm = hz * 100.0 - MZ * sz - bury * H_cm * sz
        hoehe_m = H_cm * sz / 100.0
        kol_ab = self.R.get("kollision_ab_hoehe_m", 0.8)
        koll = koll & (hoehe_m >= kol_ab)
        akteur_ab = self.R.get("akteur_ab_hoehe_m", 5.0)
        akteur = (rolle_arr.astype(str) == "wand") | ((rolle_arr.astype(str) == "hero") & (hoehe_m >= akteur_ab))
        if ist_haupt:
            r_haupt = np.zeros(len(gi))
            r_haupt[idx] = r_eigen[sel]
            fehl = r_haupt == 0
            r_haupt[fehl] = 150.0  # Hauptstück verworfen → Standardradius für Nebenstücke
        return {"x": x_cm, "y": y_cm, "z": z_cm, "q": q, "sx": sx, "sy": sy, "sz": sz, "pfad": pfade_alle,
                "rolle": rolle_arr.astype(str), "klasse": np.full(len(x_cm), kname), "koll": koll, "schatten": schatten,
                "sicht": sicht, "akteur": akteur, "hoehe_m": hoehe_m, "prio": uni(hh, 53),
                "r_haupt": r_haupt if ist_haupt else None, "ci": ci, "cj": cj}

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
            pq = z["punkte"]
            pp = os.path.join(welt_dir, pq.get("ebene", ""), feld, "plan.json")
            try:
                with open(pp, encoding="utf-8") as f:
                    pl = json.load(f)
                pts = [p for p in pl.get("punkte", []) if p.get("typ") == pq.get("typ")]
                punkte = np.array([[p["y_cm"] / 100.0 + Y0 - self.win[0], p["x_cm"] / 100.0 + X0 - self.win[2]] for p in pts]).reshape(-1, 2)
                log("Zusatzklasse %s: %d Punkte (%s) aus %s" % (name, len(punkte), pq.get("typ"), pp))
            except Exception:
                log("Hinweis: Zusatzklasse %s: %s/%s/plan.json fehlt/unlesbar - Ersatz ueber Maske (Hang, Prominenz, Lagen)." % (
                    name, pq.get("ebene"), feld))
        if punkte is not None and len(punkte):
            fi, fj = punkte[:, 0], punkte[:, 1]
            ok = (fi >= 1) & (fi < self.h.shape[0] - 1) & (fj >= 1) & (fj < self.h.shape[1] - 1)
            fi, fj = fi[ok], fj[ok]
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
        fi, fj, ci, cj, hsh = fi[ok], fj[ok], ci[ok], cj[ok], hsh[ok]
        im = (ci >= fs_i.start) & (ci < fs_i.stop) & (cj >= fs_j.start) & (cj < fs_j.stop)
        fi, fj, ci, cj, hsh = fi[im], fj[im], ci[im], cj[im], hsh[im]
        if z["max_je_feld"] is not None and len(ci) > z["max_je_feld"]:
            o = np.argsort(uni(hsh, 7), kind="stable")[: z["max_je_feld"]]
            fi, fj, ci, cj, hsh = fi[o], fj[o], ci[o], cj[o], hsh[o]
        if len(ci) == 0:
            return None, 0
        # Palette: eigene Netzliste, sonst Rollen der Biom-Palette (Altstellen ohne Netze)
        pfade = list(z["palette"])
        if not pfade:
            b0 = BIOME.index(next(iter(z["biome"])))
            for r_ in z["palette_rollen"]:
                pfade += [p for p in self.paletten[self.pal_je_biom[b0]].get(r_, []) if p not in pfade]
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
        ms = z["massstab"] or ro["massstab"]
        sk = zwischen(hh, 41, ms[0], ms[1])
        eb = z["eingraben"] or ro["eingraben"]
        bury = zwischen(hh, 44, eb[0], eb[1])
        H_cm, R_cm, MZ = hc[k], rc[k], mzc[k]
        r_eigen = R_cm * sk
        hz = bilinear(self.h, fi_c, fj_c)
        rr = np.clip(r_eigen / 100.0, 0.5, 20.0)
        hmin_rand = np.minimum.reduce([bilinear(self.h, np.clip(fi_c + d_[0] * rr, 1, H - 1.001), np.clip(fj_c + d_[1] * rr, 1, W - 1.001))
                                       for d_ in ((1, 0), (-1, 0), (0, 1), (0, -1))])
        nicht_schwebend = (hz - hmin_rand) <= bury * H_cm * sk / 100.0 + 0.3 + rr * np.tan(np.radians(60.0))
        ok = inside & im_feld & (w[pci, pcj] > 0) & nicht_schwebend
        if not ok.any():
            return None, len(ci)
        hh, pfi, pfj, pci, pcj, hz, k, sk, bury, H_cm, MZ = (a[ok] for a in (hh, pfi, pfj, pci, pcj, hz, k, sk, bury, H_cm, MZ))
        kipp = np.radians(zwischen(hh, 45, ro["kippen_grad"][0], ro["kippen_grad"][1]))
        up = self.normal[pci, pcj] + np.concatenate([-self.abfall[pci, pcj] * np.tan(kipp)[:, None], np.zeros((len(kipp), 1))], axis=1)
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        q = quat_aus_yaw_up(zwischen(hh, 50, 0, 2 * np.pi), up)
        nu = ro["nicht_uniform"]
        sx = sk * (1 + nu * (2 * uni(hh, 51) - 1)); sy = sk * (1 + nu * (2 * uni(hh, 52) - 1)); sz = sk
        hoehe_m = H_cm * sz / 100.0
        n = len(hh)
        koll_basis = ro["kollision"] if z["kollision"] is None else z["kollision"]
        koll = np.full(n, bool(koll_basis)) & (hoehe_m >= self.R.get("kollision_ab_hoehe_m", 0.8))
        sicht = np.tile(np.array(z["sichtweite"] or ro["sichtweite_cm"], dtype=float), (n, 1))
        t = {"x": (pfj + j0 - X0) * 100.0, "y": (pfi + i0 - Y0) * 100.0, "z": hz * 100.0 - MZ * sz - bury * H_cm * sz, "q": q,
             "sx": sx, "sy": sy, "sz": sz, "pfad": np.array(pfade, dtype=object)[k], "rolle": np.full(n, z["rolle"]),
             "klasse": np.full(n, "z_" + z["name"]), "koll": koll,
             "schatten": np.full(n, bool(ro["schatten"] if z["schatten"] is None else z["schatten"])), "sicht": sicht,
             "akteur": np.full(n, bool(z["akteur"])), "hoehe_m": hoehe_m, "prio": uni(hh, 53), "ci": pci, "cj": pcj}
        log("Zusatzklasse %s: %d Gruppen, %d Instanzen (%d mit Kollision%s)" % (
            name, len(ci), n, int(koll.sum()), ", Akteure" if z["akteur"] else ""))
        return t, len(ci)

    # Zusammenführen, Budget ------------------------------------------------------------------------------------------
    def zusammenfuehren(self, teile):
        keys = ["x", "y", "z", "q", "sx", "sy", "sz", "pfad", "rolle", "klasse", "koll", "schatten", "sicht", "akteur", "hoehe_m", "prio", "ci", "cj"]
        if not teile:
            return {k: np.zeros((0, 4) if k == "q" else (0, 2) if k == "sicht" else 0) for k in keys}
        return {k: np.concatenate([t[k] for t in teile]) for k in keys}

    def budget(self, a):
        """Harte Deckel (KONVENTIONEN §3): je Rolle, Kollision, Akteure, gesamt. Ausdünnung deterministisch nach Hash-Priorität
        (prio aus Instanz-Hash), Kleinzeug zuerst, hero/wand zuletzt; jede Ausdünnung mit WARNUNG im Log und in hinweise."""
        B = self.R["budget"]
        n = len(a["x"])
        if n == 0:
            return a
        keep = np.ones(n, dtype=bool)
        rolle = a["rolle"]
        grund = {}

        def weg(idx, g):
            if len(idx):
                keep[idx] = False
                grund[g] = grund.get(g, 0) + int(len(idx))
        # je Rolle
        for ro, cap in B.get("je_rolle", {}).items():
            s = np.nonzero(keep & (rolle == ro))[0]
            if len(s) > cap:
                weg(s[np.argsort(-a["prio"][s], kind="stable")[: len(s) - cap]], "%s>%d" % (ro, cap))
        # Gesamt (Kleinzeug zuerst)
        for ro in ["kiesel", "stein", "platte", "block", "band"]:
            ng = int(keep.sum())
            if ng <= B["gesamt"]:
                break
            s = np.nonzero(keep & (rolle == ro))[0]
            weg(s[np.argsort(-a["prio"][s], kind="stable")[: min(len(s), ng - B["gesamt"])]], "gesamt>%d" % B["gesamt"])
        # Kollision (kleine Rollen zuerst)
        for ro in ["block", "band", "wand", "hero"]:
            nk = int((keep & a["koll"]).sum())
            if nk <= B["kollision"]:
                break
            s = np.nonzero(keep & a["koll"] & (rolle == ro))[0]
            weg(s[np.argsort(-a["prio"][s], kind="stable")[: min(len(s), nk - B["kollision"])]], "kollision>%d" % B["kollision"])
        # Akteure: kleinste bleiben als Foliage
        s = np.nonzero(keep & a["akteur"])[0]
        if len(s) > B["akteure"]:
            kleinste = s[np.argsort(a["hoehe_m"][s], kind="stable")[: len(s) - B["akteure"]]]
            a["akteur"][kleinste] = False
            log("Hinweis Budget: %d kleinste Akteure als Foliage gesetzt (Akteure <= %d)." % (len(kleinste), B["akteure"]))
        if grund:
            txt = "%d von %d Instanzen deterministisch ausgeduennt (%s)" % (int((~keep).sum()), n, ", ".join(
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
        plan = plan_kopf(self.R, feld, int(n), self.stand)
        plan.update({"biome_fenster": self.biome_fenster, "zellen_zustaendig": int(self.zellen_zustaendig),
                     "kollision_anzahl": int(a["koll"].sum()), "biom_quelle": self.biom_quelle,
                     "dateien": dateien, "akteure": akteure, "seed": self.seed, "faktor": self.faktor,
                     "paletten_je_biom": {bn: self.pal_je_biom[BIOME.index(bn)] for bn in self.biome_fenster},
                     "overrides": {"aktiv_je_biom": {bn: o for bn, o in self.ov_aktiv.items() if bn in self.biome_fenster},
                                   "dateien": self.ov_info},
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
            gross = {"hero": 2, "wand": 2, "band": 1, "block": 1, "platte": 0, "stein": 0, "kiesel": 0}
            for rolle in ["kiesel", "stein", "platte", "block", "band", "wand", "hero"]:
                s = ok & (a["rolle"] == rolle)
                if not s.any():
                    continue
                r = gross[rolle]
                for kl in np.unique(a["klasse"][s]):
                    ss = s & (a["klasse"] == kl)
                    col = farben.get(kl, np.array(self.R.get("zusatz", {}).get("farbe", [255, 255, 255]), dtype=np.uint8))
                    if rolle == "kiesel":
                        col = (col.astype(int) * 0.5 + 100).astype(np.uint8)
                    for di in range(-r, r + 1):
                        for dj in range(-r, r + 1):
                            ii = np.clip(ci[ss] + di, 0, H - 1); jj = np.clip(cj[ss] + dj, 0, W - 1)
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
            "quelle": "felsgruppen_plan.py (Korrektur Runde 1; Vorfassung lief mit Echtdaten A5/G4/E1/C6)",
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
    ap = argparse.ArgumentParser(description="Felsgruppen-Planer Eldarien (Auftrag 11 C, Korrektur Runde 1).")
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
