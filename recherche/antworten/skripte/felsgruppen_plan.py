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
Stand Korrektur Runde 2 (auftraege/verteilung-korrektur-runde2.md, Befund 2/3; Echtdaten A5 Runde 1: 12 785 Instanzen +
53 Akteure, aus 300 m nur verstreute Punkte und flache helle Platten auf Gras):
  - Gruppengrammatik (Regelblock "form"): Hauptfels sichtbar 4,5-8,5 m (Grat) bzw. 4-7,5 m (Kuppe), Maßstab = Zielhöhe /
    Netzhöhe (netze_masse.json, sonst netze.csv), Megascans bis 2,5, sonst bis 1,5; 3-5 Satelliten 1,5-4 m entlang der
    gemeinsamen Hauptrichtung, Mittenabstand <= 1,5 x Hauptfels-Radius; Steine 0,5-1,4 m; ohne gültigen Hauptfels keine Gruppe.
  - Felskrone: grat = Kette von Formgruppen auf der Kammlinie (Querschnitt-Maximum, eine Gruppe je 28-m-Zelle);
    fuss = Blockstrom-Zunge am Fuß von Wänden > 50 Grad (Kopfblock 2,5-4 m, Größe hangabwärts abnehmend, <= 30 m).
  - Platten-Regel (Block "platten"): flache Platten-Netze nur auf Kies/Geröll/Fels/Felsplatte >= 100 (Gras/Wiese nicht
    stärker), >= 50 % eingegraben, an der Normale, strenger Schwebe-Test; zentral auch für Zusatzklassen der Biome.
  - Kleinmaterial (Kiesel, Stücke < 0,5 m) nur im Kontaktsaum <= 2 m um Gruppenstücke (Block "kleinmaterial"), nach Budget geprüft.
  - Sperrliste "gesperrt" (SM_Column_03, SM_Main_Arch_01) für Paletten, Overrides, Zusatzklassen und Punkt-Netze.
  - Budget nach Gruppen-Priorität (ganze Gruppen), Kollision über dem Deckel wird bei den kleinsten Stücken abgeschaltet;
    plan.json: statistik.form (Kennzahlen), pruefkameras (Grat-Blick aus 300 m u. a.), gesperrt.
Stand Korrektur Runde 3 (auftraege/verteilung-korrektur-runde3.md; Echtdaten Runde 2: A5 5 563 Instanzen / 316 Gruppen /
45 Akteure, G4 1 448; aus 300 m weiter nur Punkte, rote Findlinge im Nordwald):
  - netz_nur_biome: rote /Game/AncientContent/.../SM_IcelandicBoulder_01-03 nur in canyon/oedland/wueste/lava; erzwungen je
    Biom-Palette (inkl. Override-Paletten), je Zusatzklassen-Stück (Biom der Zelle) und in einer Schlussprüfung; Ersatz grau,
    gleiche Größe (Regeldatei), Log-Hinweis mit Anzahl. uchoab3fa (Quarry Cliff) steht auf der Sperrliste.
  - Formgruppen (Klasse "formgruppe", Block "formgruppen"): 8-20 je Feld auf den markantesten Graten/Kuppen/Wandnasen,
    Auswahl nach Krümmung, Prominenz und Sichtbarkeit von Tal/Weg/Wasser in 300-1500 m (Strahlen auf einem 8-m-Grobraster
    aus hoehe.f32, Fenster Feld + 1,5 km), Mindestabstand; Hero = große Klippennetze (Massive/Huge Nordic Coastal Cliff,
    Sharp_Cliff rcygn, Fab-Massive vdssailfa/vfmjadufa/veqnci0db, big_rock_wall, Big_Rock) skaliert 1,0-2,0 als Akteur mit
    Kollision, 35-60 % eingegraben, Rückseite hangwärts, Schichtneigung je Massiv; Satelliten 2-6 m eng am Fuß, Blockstrom.
  - Runde-2-Gruppen grat/kuppe (Hauptfels 4,5-8,5 m) nur noch als Begleiter der Formgruppen (formgruppen.begleitung).
  - Hangknick-Pflicht (Block hangknick): keine Gruppe auf Wiese ohne Hangknick.
Stand Korrektur Runde 4 (auftraege/verteilung-korrektur-runde4.md, KONVENTIONEN §1b; Meer fehlt in karte_wasser):
  - karte_wasser.r8 = nur Süßwasser. Meer = hoehe < 0 und karte_wasser == 0; wasser_alle = Süßwasser | Meer ersetzt
    karte_wasser als Sperre (ausschluss.wasser_m), Landzellen-Bezug (biome_fenster), Sichtziele (Tal/Binnenwasser/Meer).
    Süßwasser-spezifisch bleiben wasser_abstand_m der Ufer-Zusatzklassen (Bach-/Uferblöcke) und prallhang (Flusspolylinien).
  - Unter -0,3 m nichts; -0,3..0 m nur Zusatzklassen mit "meer_rolle": true; 0..+0,3 m im Küstensaum (<= 30 m zum Meer)
    nur Strand-Zusatzklassen (Rolle wasserkante/strand, "strand": true, kueste/kueste_nur wie nordkueste felsufer) – keine
    Gruppen, Formgruppen, Blockströme. kueste/kueste_nur messen den Abstand jetzt zum echten Meer.
  - Schlussfilter je Instanz (Geländehöhe bilinear am Instanzort) als Sicherheitsnetz; plan.json meer_zellen, meer_gefiltert,
    statistik.meer; Parameter regeln["meer"] (tief_m, saum_hoehe_m, saum_m).
Stand Korrektur Runde 5 (auftraege/verteilung-korrektur-runde5.md; Bilder FELSR3: B4-Steilhang wie ein Kistenhaufen aus kantigen,
fast würfeligen Blöcken, A5-Blockstrom mit dünnen Platten flach obenauf). Regelblöcke "steilhang" und "blockstrom_platten":
  - Steilhang (Hang am Instanzort > 35 Grad): harte Dichtegrenze für Blöcke (Größe = längste Achse Netz x Maßstab) > 2 m höchstens
    1 je 150 m², > 4 m höchstens 1 je 600 m² (Mindestabstand, Quote je 48-m-Zelle und je Feld, Formgruppen-Heros zählen mit);
    überzählige Stücke werden nach Potenzgesetz verkleinert (< 2 m) oder entfallen. Größen am Steilhang nach Potenzgesetz
    N(>d) ~ d^-exponent statt gleichverteilt; Eingraben 50-70 % senkrecht zum Hang (Schwebe-Test), Z-Achse = Geländenormale,
    lange Netzachse in der Hangebene entlang der Falllinie (+-20 Grad).
  - Würfelartige Netze (Seitenverhältnis aller Achsen < 1,4, aus den Netzmaßen) und stehende Netze (Z längste Achse) an Hängen
    > 30 Grad nur als Satelliten < 1,5 m, nie als Gruppenkern, Hero oder Blockstrom-Kopf; plattige/längliche Netze bevorzugt.
  - Blockstrom: plattige Netze nur mit Hangknick am Ort, >= 40 % eingegraben (senkrecht), an der Normale; Zungen bevorzugt in
    Rinnen (Tiefenlinie: Tangentialkrümmung der sigma-8-Höhe) und am Hangfuß.
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
KLASSEN = ["formgruppe", "grat", "band", "wand", "fuss", "blockstrom", "kuppe", "prallhang", "einzel"]
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


def potenz(h, salz, lo, hi, exponent):
    """Runde 5: Größe nach abgeschnittenem Potenzgesetz N(>d) ~ d^-exponent auf [lo, hi] (viele kleine, wenige große)."""
    lo = np.broadcast_to(np.asarray(lo, dtype=np.float64), np.shape(h)).astype(np.float64)
    hi = np.maximum(np.broadcast_to(np.asarray(hi, dtype=np.float64), np.shape(h)), lo)
    u = uni(h, salz)
    a = float(exponent)
    return lo * (1.0 - u * (1.0 - (lo / hi) ** a)) ** (-1.0 / a)


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


MEER_VORGABE = {"tief_m": -0.3, "saum_hoehe_m": 0.3, "saum_m": 30.0}
STRAND_ROLLEN = ("wasserkante", "strand")


def meer_parameter(R):
    """Runde 4 (KONVENTIONEN §1b): Grenzen aus R["meer"] (tief_m, saum_hoehe_m, saum_m), Vorgabe -0,3 / 0,3 / 30."""
    M = dict(MEER_VORGABE)
    for k, v in (R.get("meer") or {}).items():
        if k in M and _zahl(v):
            M[k] = float(v)
    return M


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
        self.nbs = NetzBiomSperre(R, netze, self.gesperrt)  # Runde 3: biombeschränkte Netze (nur melden; erzwungen im Planer)
        self.biomsperre_treffer = []
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
                if self.nbs.aktiv and any(not self.nbs.darf(q, BIOME.index(bn)) for bn in self.biome):
                    self.biomsperre_treffer.append(q)
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
             "punkte": None, "felder": None, "zonen": None, "fuss_m": 22.0, "dichte_gruppen": False, "z_versatz": None,
             "strand": False, "meer_rolle": False, "gelesen": [], "ignoriert": []}
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
                elif v in STRAND_ROLLEN:  # Runde 4: Strand-/Küstenfelsen (z. B. nordkueste felsufer) dürfen auf den Strand
                    z["strand"], z["rolle"] = True, "block"
                    G(k + " (%s: Strand erlaubt, Stuecke als block)" % v)
                    continue
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
            elif k in ("strand", "meer_rolle") and isinstance(v, bool):
                z[k] = v
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
        if z["meer_nur"] or z["meer_rolle"]:  # Küstenklassen (kueste/kueste_nur) und Meeres-Rollen dürfen auf den Strand
            z["strand"] = True
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


class NetzBiomSperre:
    """Runde 3 (Befund 1): Netze, die nur in bestimmten Biomen stehen dürfen (felsgruppen_regeln.json["netz_nur_biome"]).
    netze {pfad: [biome]} (Schlüssel mit '*' am Ende = Präfix), ersatz {pfad: [graue Netze gleicher Größe]}."""

    def __init__(self, R, netze, gesperrt=()):
        B = R.get("netz_nur_biome") or {}
        self.exakt, self.praefix, self.ersatz = {}, [], {}
        for p, bl in (B.get("netze") or {}).items():
            if not isinstance(p, str) or p.startswith("_") or not isinstance(bl, list):
                continue
            s = frozenset(BIOME.index(b) for b in bl if b in BIOME)
            if p.endswith("*"):
                self.praefix.append((p[:-1] if p.startswith("/") else "/Game/" + p[:-1], s))
            else:
                self.exakt[norm_pfad(p)] = s
        self.praefix.sort()
        self._cache = {}
        for p, l in (B.get("ersatz") or {}).items():
            if isinstance(l, list):
                self.ersatz[norm_pfad(p)] = [q for q in (norm_pfad(x) for x in l if isinstance(x, str))
                                             if q in netze and q not in gesperrt and self.erlaubt(q) is None]
        self.aktiv = bool(self.exakt or self.praefix)

    def erlaubt(self, pfad):
        """frozenset der erlaubten Biom-Indizes oder None (Netz unbeschränkt)."""
        if pfad not in self._cache:
            s = self.exakt.get(pfad)
            if s is None:
                for pre, ps in self.praefix:
                    if pfad.startswith(pre):
                        s = ps
                        break
            self._cache[pfad] = s
        return self._cache[pfad]

    def darf(self, pfad, b):
        s = self.erlaubt(pfad)
        return s is None or int(b) in s

    def biome_text(self, pfad):
        s = self.erlaubt(pfad)
        return "alle" if s is None else ",".join(BIOME[i] for i in sorted(s))

    def ersatz_fuer(self, pfad):
        return list(self.ersatz.get(pfad, []))

    def liste_filtern(self, liste, b):
        """Netzliste für Biom b: verbotene Netze raus, Ersatz (falls noch nicht drin) an ihre Stelle. -> (neu, raus, rein)."""
        neu, raus, rein = [], [], []
        for p in liste:
            if self.darf(p, b):
                if p not in neu:
                    neu.append(p)
                continue
            raus.append(p)
            for q in self.ersatz_fuer(p):
                if q not in neu and q not in liste:
                    neu.append(q)
                    rein.append(q)
        return neu, raus, rein


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
        if L.biomsperre_treffer:
            log("  Hinweis: %s: %d Verweise auf biombeschraenkte Netze (%s) - werden nur in erlaubten Biomen gesetzt, sonst "
                "grauer Ersatz (netz_nur_biome)." % (datei, len(L.biomsperre_treffer), ", ".join(
                    "%s nur %s" % (p.rsplit("/", 1)[-1], L.nbs.biome_text(p)) for p in sorted(set(L.biomsperre_treffer)))))
        info[datei] = {"biome": biome, "status": "gelesen", "biome_mit_aenderung": sorted(erg), "gelesen": L.gelesen,
                       "gesperrt_entfernt": sorted(set(L.gesperrt_treffer)),
                       "biombeschraenkt_verweise": sorted(set(L.biomsperre_treffer)),
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
        # Runde 5: Steilhang- und Blockstrom-Platten-Regeln
        self.SH = regeln.get("steilhang") or {}
        self.sh_aktiv = bool(self.SH.get("aktiv", False))
        self.BP = regeln.get("blockstrom_platten") or {}
        self.bp_aktiv = bool(self.BP.get("aktiv", False))
        self._nform = {}
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
        # Runde 3: biombeschränkte Netze (rote Findlinge) und Formgruppen-Hero-Paletten
        self.nbs = NetzBiomSperre(regeln, netze, self.gesperrt)
        if self.nbs.aktiv:
            log("Netz-Biomsperre: %s; Ersatz grau: %s" % (
                "; ".join("%s nur %s" % (p.rsplit("/", 1)[-1], self.nbs.biome_text(p)) for p in sorted(self.nbs.exakt)) or "-",
                "; ".join("%s->%s" % (p.rsplit("/", 1)[-1], ",".join(q.rsplit("/", 1)[-1] for q in l))
                          for p, l in sorted(self.nbs.ersatz.items())) or "-"))
        self.form_paletten = {}
        FG = regeln.get("formgruppen") or {}
        for pn, eintraege in sorted(((FG.get("hero") or {}).get("paletten") or {}).items()):
            ok = []
            for e in eintraege if isinstance(eintraege, list) else []:
                p = norm_pfad(e.get("pfad", "")) if isinstance(e, dict) else ""
                if p not in netze or p in self.gesperrt:
                    log("Hinweis: Formgruppen-Hero %s (%s) nicht im Inventar oder gesperrt - ignoriert." % (p, pn))
                    continue
                ok.append({"pfad": p, "typen": list(e.get("typen", ["grat", "kuppe", "nase"])), "gewicht": float(e.get("gewicht", 1.0)),
                           "rueckseite": e.get("rueckseite")})
            if ok:
                self.form_paletten[pn] = ok

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
        # Runde 3 (Befund 1): biombeschränkte Netze je Biom-Palette erzwingen (Grundpalette und Override-Paletten gleichermaßen)
        self.form_pal_basis = list(namen)  # Palettenname vor der Biomsperre (für die Formgruppen-Hero-Palette)
        self.netzsperre_stat = {"paletten": {}}
        if self.nbs.aktiv:
            varianten, biome_je_var = {}, {}
            for b in range(len(BIOME)):
                name = namen[b]
                neu, raus_, rein_ = {}, [], []
                for r, liste in pal[name].items():
                    neu[r], ra, re_ = self.nbs.liste_filtern(liste, b)
                    raus_ += ra
                    rein_ += re_
                if not raus_:
                    continue
                key = (name, tuple(sorted(set(raus_))))
                if key not in varianten:
                    vn = name + "~grau"
                    if vn in pal and pal[vn] != neu:
                        vn = name + "~grau_" + BIOME[b]
                    pal[vn] = neu
                    varianten[key] = (vn, len(raus_), sorted(set(rein_)))
                biome_je_var.setdefault(key, []).append(BIOME[b])
                namen[b] = varianten[key][0]
                if BIOME[b] in self.ov_aktiv:
                    self.ov_aktiv[BIOME[b]]["palette"] = namen[b]
            for key, (vn, n_raus, rein_) in sorted(varianten.items()):
                bl = biome_je_var[key]
                self.netzsperre_stat["paletten"][vn] = {"biome": bl, "entfernt": [p.rsplit("/", 1)[-1] for p in key[1]],
                                                        "verweise": n_raus, "ersatz": [p.rsplit("/", 1)[-1] for p in rein_]}
                log("Netz-Biomsperre: Palette %s fuer %s: %d Verweise entfernt (%s), Ersatz %s." % (
                    key[0], ",".join(bl), n_raus, ",".join(p.rsplit("/", 1)[-1] for p in key[1]),
                    ",".join(p.rsplit("/", 1)[-1] for p in rein_) or "bereits enthalten"))
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
        self.fg_stat, self.form_stat, self.kameras, self.form_info = {}, {}, [], None
        self.steil_stat, self.dichte_stat = {}, {}
        self.haupt_je_biom = np.zeros(len(BIOME), dtype=np.int64)
        self.sh_stat = {"netzform_verworfen": 0, "netzform_umgestellt": 0, "schwebend_verworfen": 0, "potenz_stuecke": 0}
        self.konfig(feld)
        self.netzform_info = self.netzform_log() if self.sh_aktiv else {}
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
        # Runde 4 (KONVENTIONEN §1b): karte_wasser = nur Süßwasser; Meer = hoehe < 0 und karte_wasser == 0
        MP = self.MP = meer_parameter(R)
        suess = (wasser > 0) if wasser is not None else np.zeros(h.shape, dtype=bool)
        self.m_suess = suess
        self.meer = (h < 0.0) & ~suess
        self.wasser_alle = suess | self.meer
        self.d_meer = self.abstand(self.meer, int(math.ceil(MP["saum_m"])) + 1) if self.meer.any() else np.full(h.shape, 1e9)
        self.kuestensaum = ~self.wasser_alle & (h < MP["saum_hoehe_m"]) & (self.d_meer <= MP["saum_m"])
        self.meer_stat = {"meer_zellen_fenster": int(self.meer.sum()), "kuestensaum_zellen_fenster": int(self.kuestensaum.sum()),
                          "grenzen_m": MP, "kandidaten_gesperrt": 0,
                          "schlussfilter": {"unter_tief": 0, "unter_0_ohne_meer_rolle": 0, "strandsaum_ohne_strand_rolle": 0}}
        self.m_wasser = dilate(self.wasser_alle, A["wasser_m"])
        self.m_wasser_roh = self.wasser_alle
        nah_suess = dilate(suess, A["wasser_m"])
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
        # Runde 3: Hangknick = größter Betrag der Hauptkrümmungen (sigma 25 m); Gefälle sigma 25 (Front der Formgruppen)
        self.knick = np.maximum(np.abs(l1b), np.abs(l2b)) >= float(R.get("hangknick", {}).get("kruemmung_min", 0.004))
        g25y, g25x = np.gradient(hs25)
        self.gef25 = np.stack([-g25x, -g25y], axis=2)  # Gefälle-Vektor (x, y), Betrag = tan(Hang)
        # Runde 5: Rinne/Tiefenlinie = Krümmung der sigma-8-Höhe quer zur Falllinie (Tangentialkrümmung, > 0 = Mulde/Rinne)
        g8y, g8x = np.gradient(hs)
        hxx, hxy, hyy = np.gradient(g8x, axis=1), np.gradient(g8x, axis=0), np.gradient(g8y, axis=0)
        q2 = g8x ** 2 + g8y ** 2
        ktan = (hxx * g8y ** 2 - 2.0 * hxy * g8x * g8y + hyy * g8x ** 2) / np.maximum(q2, 1e-9)
        self.rinne = (ktan >= float(self.BP.get("rinne_kruemmung_min", 0.012))) & \
            (np.degrees(np.arctan(np.sqrt(q2))) >= float(self.BP.get("rinne_hang_min_grad", 8)))
        del g8y, g8x, hxx, hxy, hyy, q2, ktan
        hs12 = gauss(h, G["kuppe_sigma_m"])
        self.hs12 = hs12
        self.land = h > 0.2
        # Biom-Anteile im Fenster (Landzellen ohne Süßwasser und Meer; KONVENTIONEN §1/§1b)
        bl = self.biom[self.land & ~self.wasser_alle]
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
        hang_ok = self.hang <= A["max_hang_grad"]
        # Runde 4: Gruppen/Formgruppen/Blockströme nie im Meer, nie im Strandsaum (0..+0,3 m, <= 30 m zum Meer)
        self.m_frei = self.land & ~self.m_wasser & ~self.kuestensaum & ~self.m_weg & ~self.m_ort & hang_ok
        self.m_frei_klein = self.land & ~self.m_wasser & ~self.kuestensaum & ~self.m_weg_klein & ~self.m_ort & hang_ok
        # nur durch die Meer-Regel gesperrt (für meer_gefiltert)
        self.m_frei_om = self.land & ~nah_suess & ~self.m_weg & ~self.m_ort & hang_ok
        self.m_frei_klein_om = self.land & ~nah_suess & ~self.m_weg_klein & ~self.m_ort & hang_ok
        # Strand-Zusatzklassen (Rolle wasserkante/strand, strand true, kueste): ab 0 m bis an die Wasserlinie; meer_rolle ab tief_m
        self.m_frei_strand = (h >= 0.0) & ~self.meer & ~nah_suess & ~self.m_weg & ~self.m_ort & hang_ok
        self.m_frei_strand_klein = (h >= 0.0) & ~self.meer & ~nah_suess & ~self.m_weg_klein & ~self.m_ort & hang_ok
        self.m_frei_meer = (h >= MP["tief_m"]) & ~nah_suess & ~self.m_weg_klein & ~self.m_ort & hang_ok
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
        self.wiese_stat = {}
        self.begleit_stat = {}
        # Runde 3: Formgruppen 10-30 m zuerst (ihre Lage steuert die Begleitgruppen der Runde 2)
        teile_fg, n_fg = self.formgruppen_erzeugen(welt_dir, feld)
        self.statistik["formgruppe"] = {"gruppen": int(n_fg), "instanzen": int(sum(len(t["x"]) for t in teile_fg))}
        inst.extend(teile_fg)
        gruppen_gesamt += n_fg
        self._kuppen = self.kandidaten_kuppe()  # vor dem Grat: Kuppen haben Vorrang vor Kettengliedern
        for kname in KLASSEN:  # "einzel" zuletzt: füllt nur bis mindestdichte_je_ha auf
            if kname == "formgruppe":
                continue
            if kname == "prallhang":
                g = self.kandidaten_prallhang(welt_dir)
            elif kname == "kuppe":
                g = self._kuppen
            elif kname == "grat":
                g, self._kuppen = self.begleit_filter(self.kandidaten_kamm(), self._kuppen)
            elif kname == "fuss":
                g = self.kandidaten_strom()
            elif kname == "einzel":
                g = self.kandidaten_einzel()
            else:
                g = self.kandidaten_gitter(kname)
            g = self.wiese_filter(kname, g)
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
        alle = self.netz_biom_pruefung(alle)
        alle = self.meer_schlussfilter(alle)
        alle = self.steil_dichte(alle)
        alle = self.budget(alle)
        alle = self.kontaktsaum(alle)
        self.form_statistik(alle)
        self.formgruppen_statistik(alle)
        self.steil_statistik(alle)
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
            if self.bp_aktiv:  # Runde 5: Hangfuß oder Rinne (Tiefenlinie), Rinnen bevorzugt
                ok &= self.wand_ueber_128[ci, cj] & ((self.hohl25[ci, cj] >= K["hohl_min"]) | self.rinne[ci, cj]) & ~self.m_wand[ci, cj]
                p *= np.where(self.rinne[ci, cj], float(self.BP.get("rinne_faktor", 1.5)), 1.0)
            else:
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
        score = uni(hsh, 1)
        if self.bp_aktiv:  # Runde 5: Rinne (Tiefenlinie) oder Hangfuß gewinnt die Zellwahl
            ort = self.rinne[ci, cj] | (self.hohl25[ci, cj] >= float(self.R["klassen"]["blockstrom"]["hohl_min"]))
            score = score + float(self.BP.get("ort_bonus", 1.0)) * ort
        s = self._zellen_wahl(ci, cj, score, int(K["strom_abstand_m"]), float(K["strom_min_abstand_m"]))
        ci, cj, hsh = ci[s], cj[s], hsh[s]
        erl, bf = self._klasse_erlaubt("fuss", ci, cj)
        pf = np.ones(len(ci))
        if self.bp_aktiv:
            ort = self.rinne[ci, cj] | (self.hohl25[ci, cj] >= float(self.R["klassen"]["blockstrom"]["hohl_min"])) | self.knick[ci, cj]
            pf = np.where(ort, 1.0, float(self.BP.get("ohne_ort_faktor", 0.3)))
        ok = erl & (uni(hsh, 5) < K["p"] * self.faktor * self.f_ger[ci, cj] * bf * pf)
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

    # Runde 3: Hangknick-Pflicht und Begleitgruppen -------------------------------------------------------------------
    @staticmethod
    def _g_auswahl(g, keep):
        return {k: (v[keep] if isinstance(v, np.ndarray) else v) for k, v in g.items()}

    def wiese_filter(self, kname, g):
        """Keine Gruppe auf Wiese ohne Hangknick (Block hangknick): Kandidaten der genannten Klassen auf Wiese-Zellen
        (Gras/Wiese >= lagen_min, keine Kies/Geroell/Fels-Lage) ohne Hangknick entfallen."""
        if g is None or len(g["ci"]) == 0 or kname not in self.R.get("hangknick", {}).get("klassen", []):
            return g
        wk = self.m_gras[g["ci"], g["cj"]] & ~self.knick[g["ci"], g["cj"]]
        self.wiese_stat[kname] = int(wk.sum())
        return self._g_auswahl(g, ~wk) if wk.any() else g

    def begleit_filter(self, gr, ku):
        """Runde-2-Gruppen (grat/kuppe) nur noch als Begleiter der Formgruppen: je Formgruppe höchstens max_je_formgruppe im
        Abstand abstand_m (nächste zuerst), dazu je Feld höchstens frei_max_je_feld fern jeder Formgruppe (beste nach Relief,
        untereinander >= frei_abstand_m). Ankerpunkte = alle ausgewählten Formgruppen im Fenster (auch im Rand)."""
        FG = self.R.get("formgruppen") or {}
        B = FG.get("begleitung") or {}
        if not FG.get("aktiv") or not B.get("aktiv", True):
            return gr, ku
        kl = B.get("klassen", ["grat", "kuppe"])
        quellen = [(n, g) for n, g in (("grat", gr), ("kuppe", ku)) if n in kl and g is not None and len(g["ci"])]
        if not quellen:
            return gr, ku
        ci = np.concatenate([g["ci"] for _, g in quellen])
        cj = np.concatenate([g["cj"] for _, g in quellen])
        hh = np.concatenate([g["h"] for _, g in quellen])
        src = np.concatenate([np.full(len(g["ci"]), q) for q, (_, g) in enumerate(quellen)])
        n = len(ci)
        a0, a1 = [float(x) for x in B.get("abstand_m", [35, 220])]
        anker = getattr(self, "form_anker", np.zeros((0, 2)))
        if len(anker):
            d_all = np.hypot(ci[:, None] - anker[None, :, 0], cj[:, None] - anker[None, :, 1])
            na = np.argmin(d_all, axis=1)
            d = d_all[np.arange(n), na]
        else:
            na, d = np.zeros(n, dtype=np.int64), np.full(n, np.inf)
        keep = np.zeros(n, dtype=bool)
        mx = int(B.get("max_je_formgruppe", 3))
        zaehl = np.zeros(max(len(anker), 1), dtype=np.int64)
        for k in np.lexsort((uni(hh, 71), d)):
            if a0 <= d[k] <= a1 and zaehl[na[k]] < mx:
                keep[k] = True
                zaehl[na[k]] += 1
        # fern jeder Formgruppe: wenige, verteilt
        fs_i, fs_j = self.feld_slice
        im = (ci >= fs_i.start) & (ci < fs_i.stop) & (cj >= fs_j.start) & (cj < fs_j.stop)
        score = (self.hs8 - self.hs25)[ci, cj] + 0.5 * uni(hh, 72)
        fmax, fab = int(B.get("frei_max_je_feld", 6)), float(B.get("frei_abstand_m", 150))
        gew, n_feld = [], 0
        for k in np.argsort(-score, kind="stable"):
            if d[k] <= a1:
                continue
            if any(math.hypot(ci[k] - a, cj[k] - b) < fab for a, b in gew):
                continue
            if im[k]:
                if n_feld >= fmax:
                    continue
                n_feld += 1
            gew.append((ci[k], cj[k]))
            keep[k] = True
        st = {"anker_formgruppen": int(len(anker)), "begleitend": int((keep & (d <= a1)).sum()),
              "frei": int((keep & (d > a1)).sum()), "entfernt_zu_nah": int((d < a0).sum()),
              "entfernt_gesamt": int((~keep).sum()), "kandidaten": int(n)}
        for q, (name, _) in enumerate(quellen):
            st["%s_vorher" % name] = int((src == q).sum())
            st["%s_nachher" % name] = int((keep & (src == q)).sum())
        self.begleit_stat = st
        log("Begleitung (Runde-2-Gruppen grat/kuppe): %d Kandidaten -> %d begleitend (je Formgruppe <= %d in %d-%d m) + %d frei "
            "(<= %d je Feld), %d entfernt." % (n, st["begleitend"], mx, int(a0), int(a1), st["frei"], fmax, st["entfernt_gesamt"]))
        out = {}
        for q, (name, g) in enumerate(quellen):
            out[name] = self._g_auswahl(g, keep[src == q])
        return out.get("grat", gr), out.get("kuppe", ku)

    # Runde 3: Formgruppen 10-30 m ----------------------------------------------------------------------------------------
    def sicht_daten(self, welt_dir):
        """Grobraster (raster_m, global ausgerichtet) im Fenster Feld + abstand_m[1]: Höhe (Blockmittel aus hoehe.f32), Ziele
        (Weg, Tal, Binnenwasser, Meer mit Gewicht) und Umgebungsmittel (Box umgebung_m) für Prominenz und Tal."""
        FG = self.R["formgruppen"]
        S = FG["sicht"]
        r = int(S["raster_m"])
        reich = int(S["abstand_m"][1]) + 2 * r
        i0f, i1f, j0f, j1f = self.feld_box
        I0, I1 = max(0, (i0f - reich) // r), min(-(-NY // r), -(-(i1f + reich) // r))
        J0, J1 = max(0, (j0f - reich) // r), min(-(-NX // r), -(-(j1f + reich) // r))
        a_, b_, c_, d_ = I0 * r, min(I1 * r, NY), J0 * r, min(J1 * r, NX)
        nI, nJ = I1 - I0, J1 - J0

        def block(pfad, dtype, art):
            if not os.path.isfile(pfad) or os.path.getsize(pfad) != NX * NY * np.dtype(dtype).itemsize:
                return None
            mm = np.memmap(pfad, dtype=dtype, mode="r", shape=(NY, NX))
            roh = np.array(mm[a_:b_, c_:d_])
            if art == "mittel":
                x = np.full((nI * r, nJ * r), np.nan, dtype=np.float32)
                x[:roh.shape[0], :roh.shape[1]] = roh
                x = x.reshape(nI, r, nJ, r)
                ok = np.isfinite(x)
                s = np.where(ok, x, 0.0).sum(axis=(1, 3), dtype=np.float64)
                c = ok.sum(axis=(1, 3))
                return np.where(c > 0, s / np.maximum(c, 1), np.nan)
            x = np.zeros((nI * r, nJ * r), dtype=bool)
            x[:roh.shape[0], :roh.shape[1]] = roh > 0
            return x.reshape(nI, r, nJ, r).any(axis=(1, 3))

        hc = block(os.path.join(welt_dir, "hoehe.f32"), "<f4", "mittel")
        weg = block(os.path.join(welt_dir, "karte_weg.r8"), np.uint8, "max")
        was = block(os.path.join(welt_dir, "karte_wasser.r8"), np.uint8, "max")
        gueltig = np.isfinite(hc)
        hz = np.where(gueltig, hc, 0.0)
        k = max(1, int(round(float(FG.get("umgebung_m", 200)) / r)))

        def boxsumme(a):
            p = np.pad(a, ((k + 1, k), (k + 1, k)), mode="constant")
            c = p.cumsum(0).cumsum(1)
            return c[2 * k + 1:, 2 * k + 1:] - c[:-2 * k - 1, 2 * k + 1:] - c[2 * k + 1:, :-2 * k - 1] + c[:-2 * k - 1, :-2 * k - 1]

        umg = boxsumme(hz) / np.maximum(boxsumme(gueltig.astype(np.float64)), 1.0)
        gy, gx = np.gradient(hz, float(r))
        hang_c = np.degrees(np.arctan(np.hypot(gx, gy)))
        land = gueltig & (hc > 0.2)
        if was is None:
            was = np.zeros(hc.shape, dtype=bool)
        meer = gueltig & (hc < 0.0) & ~was  # Runde 4: karte_wasser = nur Süßwasser; Meer = Blockmittel < 0 ohne Süßwasser
        was_alle = was | meer
        tal = land & ~was_alle & (hc - umg <= -float(S["tal_tiefe_m"])) & (hang_c <= float(S["tal_hang_max_grad"]))
        Z = S["ziele"]
        T = np.zeros(hc.shape)
        if weg is not None:
            T = np.maximum(T, float(Z.get("weg", 1.0)) * weg)
        T = np.maximum(T, float(Z.get("tal", 1.0)) * tal)
        T = np.maximum(T, float(Z.get("wasser_binnen", 0.6)) * was)
        T = np.maximum(T, float(Z.get("meer", 0.3)) * meer)
        if weg is None:
            self.hinweise.append("Formgruppen-Sichtbarkeit ohne karte_weg.r8 (nur Tal/Wasser als Ziel)")
        self.sd = {"r": r, "I0": I0, "J0": J0, "hc": hc, "T": T, "umg": umg,
                   "ziele_anteil": {"weg": float(weg.mean()) if weg is not None else 0.0, "tal": float(tal.mean()),
                                    "wasser": float(was_alle.mean())}}
        return self.sd

    def _grob(self, feld_arr, fi, fj):
        """Bilinearer Wert eines Grobrasters an Fensterkoordinaten (fi, fj) (Zellmitten global ausgerichtet)."""
        sd = self.sd
        r = sd["r"]
        gi = (fi + self.win[0] + 0.5) / r - 0.5 - sd["I0"]
        gj = (fj + self.win[2] + 0.5) / r - 0.5 - sd["J0"]
        a = np.nan_to_num(feld_arr, nan=0.0)
        return bilinear(a, np.clip(gi, 0, a.shape[0] - 1.001), np.clip(gj, 0, a.shape[1] - 1.001))

    def sichtbarkeit(self, ci, cj):
        """Je Kandidat: gewichtete Zahl sichtbarer Ziel-Zellen (Weg/Tal/Wasser) in abstand_m und die Haupt-Sichtrichtung
        (Einheitsvektor x, y). Strahlen auf dem Grobraster; Sichtlinie Auge (Ziel + augenhoehe_m) -> Felskrone (Gelände +
        zielhoehe_m) frei, wenn der Höhenwinkel nicht unter dem Horizont der näheren Strahlpunkte liegt."""
        S = self.R["formgruppen"]["sicht"]
        sd = self.sd
        r = sd["r"]
        nd = int(S["richtungen"])
        th = 2.0 * np.pi * np.arange(nd) / nd
        dd = np.arange(r, float(S["abstand_m"][1]) + 1e-6, float(r))
        gi = (ci + self.win[0]).astype(np.float64)
        gj = (cj + self.win[2]).astype(np.float64)
        Y = gi[:, None, None] + 0.5 + np.sin(th)[None, :, None] * dd[None, None, :]
        X = gj[:, None, None] + 0.5 + np.cos(th)[None, :, None] * dd[None, None, :]
        I = np.floor(Y / r).astype(np.int64) - sd["I0"]
        J = np.floor(X / r).astype(np.int64) - sd["J0"]
        hc, T = sd["hc"], sd["T"]
        ok = (I >= 0) & (I < hc.shape[0]) & (J >= 0) & (J < hc.shape[1])
        Ic, Jc = np.clip(I, 0, hc.shape[0] - 1), np.clip(J, 0, hc.shape[1] - 1)
        hk = np.where(ok, hc[Ic, Jc], np.nan)
        ok &= np.isfinite(hk)
        auge = self.h[ci, cj] + float(S["zielhoehe_m"])
        ang = np.where(ok, (np.nan_to_num(hk) - auge[:, None, None]) / dd[None, None, :], -np.inf)
        hor = np.maximum.accumulate(ang, axis=2)
        hor_vor = np.concatenate([np.full(hor.shape[:2] + (1,), -np.inf), hor[:, :, :-1]], axis=2)
        blick = (np.nan_to_num(hk) + float(S["augenhoehe_m"]) - auge[:, None, None]) / dd[None, None, :]
        ring = (dd >= float(S["abstand_m"][0]))[None, None, :]
        w = np.where(ok & ring & (blick >= hor_vor), T[Ic, Jc], 0.0) * (dd / 1000.0)[None, None, :]
        je_r = w.sum(axis=2)
        summe = je_r.sum(axis=1)
        v = np.stack([(je_r * np.cos(th)[None, :]).sum(1), (je_r * np.sin(th)[None, :]).sum(1)], axis=1)
        nv = np.linalg.norm(v, axis=1, keepdims=True)
        v = np.where(nv > 1e-9, v / np.maximum(nv, 1e-9), 0.0)
        return summe, v

    def netz_xyz(self, pfad):
        """(Breite x, Breite y, Höhe, min_z) in m; Maße aus netze_masse.json, sonst netze.csv (Pivot laut netz_mass)."""
        n = self.netze[pfad]
        if pfad in self.masse:
            mn, mx = self.masse[pfad]
            return (mx[0] - mn[0]) / 100.0, (mx[1] - mn[1]) / 100.0, (mx[2] - mn[2]) / 100.0, mn[2] / 100.0
        h_cm, _, mz = self.netz_mass(pfad)
        return n["sx"], n["sy"], h_cm / 100.0, mz / 100.0

    # Runde 5: Netzform (würfelartig / stehend / plattig / länglich) aus den Netzmaßen ---------------------------------------
    def netz_form(self, pfad):
        """Kennwerte je Netz (gecacht): dx, dy, dz (m), a = längste Achse, verh = längste/kürzeste Achse, wuerfel (verh <
        wuerfel_verhaeltnis), stehend (Z ist die längste Achse), plattig (Z <= plattig_verhaeltnis x längere waagerechte Achse),
        laenglich (waagerechte Achsen >= laenglich_verhaeltnis), gewicht (Vorzug am Hang)."""
        c = self._nform.get(pfad)
        if c is None:
            NF = self.SH.get("netzform", {})
            dx, dy, dz, mz = self.netz_xyz(pfad)
            dx, dy, dz = max(dx, 0.01), max(dy, 0.01), max(dz, 0.01)
            ach = sorted([dx, dy, dz])
            verh = ach[2] / ach[0]
            wa, wb = max(dx, dy), min(dx, dy)
            wuerfel = verh < float(NF.get("wuerfel_verhaeltnis", 1.4))
            stehend = dz >= wa
            plattig = (not wuerfel) and dz <= float(NF.get("plattig_verhaeltnis", 0.5)) * wa
            laenglich = (not wuerfel) and wa / wb >= float(NF.get("laenglich_verhaeltnis", 1.5))
            G = NF.get("gewicht", {})
            gew = float(G.get("plattig", 3.0)) if plattig else (float(G.get("laenglich", 2.0)) if laenglich else float(G.get("sonst", 1.0)))
            c = self._nform[pfad] = {"dx": dx, "dy": dy, "dz": dz, "a": ach[2], "verh": verh, "wuerfel": wuerfel,
                                     "stehend": stehend, "plattig": plattig, "laenglich": laenglich, "gewicht": gew,
                                     "lang_y": dy > dx}
        return c

    def netzform_arrays(self, pfade):
        """Arrays (a, wuerfel, stehend, plattig, gewicht, lang_y, dx, dy) zu einer Netzliste."""
        f = [self.netz_form(p) for p in pfade]
        return (np.array([x["a"] for x in f]), np.array([x["wuerfel"] for x in f], dtype=bool),
                np.array([x["stehend"] for x in f], dtype=bool), np.array([x["plattig"] for x in f], dtype=bool),
                np.array([x["gewicht"] for x in f]), np.array([x["lang_y"] for x in f], dtype=bool),
                np.array([x["dx"] for x in f]), np.array([x["dy"] for x in f]))

    def blockgroesse(self, a):
        """Blockgröße d je Instanz = längste Achse Netz x Maßstab (m)."""
        if len(a["x"]) == 0:
            return np.zeros(0)
        f = {p: self.netz_form(p) for p in set(a["pfad"].tolist())}
        dx = np.array([f[p]["dx"] for p in a["pfad"]])
        dy = np.array([f[p]["dy"] for p in a["pfad"]])
        dz = np.array([f[p]["dz"] for p in a["pfad"]])
        return np.maximum.reduce([dx * a["sx"], dy * a["sy"], dz * a["sz"]])

    def netzform_log(self):
        """Liste der würfelartigen und stehenden Netze in allen Paletten des Feldes (Grund-, Override-, Hero-, Zusatz-Paletten)."""
        pf = set()
        for rollen in self.paletten.values():
            for r, l in rollen.items():
                if r != "kiesel":
                    pf.update(l)
        for l in self.form_paletten.values():
            pf.update(e["pfad"] for e in l)
        for z in self.zusatz:
            pf.update(p for p in z.get("palette", []) if p in self.netze)
        pf = sorted(p for p in pf if p in self.netze)
        w = [(self.netze[p]["name"], round(self.netz_form(p)["verh"], 2)) for p in pf if self.netz_form(p)["wuerfel"]]
        s = [self.netze[p]["name"] for p in pf if self.netz_form(p)["stehend"] and not self.netz_form(p)["wuerfel"]]
        log("Netzform (Runde 5): %d Felsnetze in den Paletten, wuerfelartig (alle Achsen < %.1f) %d: %s" % (
            len(pf), float(self.SH.get("netzform", {}).get("wuerfel_verhaeltnis", 1.4)), len(w),
            ", ".join("%s %.2f" % x for x in w) or "-"))
        log("Netzform (Runde 5): stehend (Z laengste Achse) %d: %s" % (len(s), ", ".join(s) or "-"))
        return {"netze_geprueft": len(pf), "wuerfelartig": [{"netz": n, "verhaeltnis": v} for n, v in w], "stehend": s}

    def form_hero_palette(self, b):
        """Formgruppen-Hero-Palette des Bioms: Basisname der Biom-Palette (ohne @/~-Zusatz) über hero.palette_je_biom, sonst
        Grundzuordnung biom_palette, Rückfall nordisch. Biombeschränkte Netze werden für dieses Biom ausgefiltert."""
        H = self.R["formgruppen"]["hero"]
        pje = H.get("palette_je_biom", {})
        kand = []
        for nm in (self.form_pal_basis[b], self.R["biom_palette"].get(BIOME[b], "nordisch")):
            nm = nm.split("@")[0].split("~")[0]
            kand += [pje.get(nm, nm), nm]
        kand.append("nordisch")
        for nm in kand:
            if nm in self.form_paletten:
                return nm, [e for e in self.form_paletten[nm] if self.nbs.darf(e["pfad"], b)]
        return None, []

    def formgruppen_erzeugen(self, welt_dir, feld):
        """Formgruppen 10-30 m (Klasse formgruppe): Kandidaten auf markanten Graten/Kuppen/Wandnasen (Krümmung, Hangknick,
        Prominenz), Sichtbarkeit von Tal/Weg, gierige Auswahl mit Mindestabstand, je Feld je_feld; Hero (große Klippe als
        Akteur, 1,0-2,0, 35-60 % eingegraben, Rückseite hangwärts), Satelliten 2-6 m am Fuß, Blockstrom, Kieselsaum."""
        FG = self.R.get("formgruppen") or {}
        self.form_anker = np.zeros((0, 2))
        self.form_info = None
        self.form_stat_vorab = {}
        if not FG.get("aktiv"):
            return [], 0
        i0, i1, j0, j1 = self.win
        H, W = self.h.shape
        fs_i, fs_j = self.feld_slice
        rel = self.hs8 - self.hs25
        b_aus = np.array([(BIOME[b] in FG.get("biome_aus", [])) or bool(self.aus_klasse["formgruppe"][b]) for b in range(len(BIOME))])
        maske = (self.knick & (self.grat >= float(FG["kruemmung_min"])) & (rel >= float(FG["relief_min_m"])) & self.m_frei
                 & ~self.m_sperr & ~self.m_mulde & (self.hang <= float(FG["hang_max_grad"])) & ~b_aus[self.biom])
        rd = 3
        maske[:rd, :] = False; maske[-rd:, :] = False; maske[:, :rd] = False; maske[:, -rd:] = False
        ci, cj = np.nonzero(maske)
        st = {"maskenzellen": int(len(ci))}
        self.form_stat_vorab = st
        if len(ci) == 0:
            log("Formgruppen: keine Kandidaten (Hangknick + Gratstaerke + Relief) im Fenster.")
            return [], 0
        kr_ref, pr_ref = float(FG["kruemmung_ref"]), float(FG["prominenz_ref_m"])
        vor = np.clip(self.grat[ci, cj] / kr_ref, 0, 1) + np.clip(rel[ci, cj] / 10.0, 0, 1)
        S_ = int(FG.get("vorwahl_zelle_m", 40))
        s = self._zellen_wahl(ci, cj, vor + 1e-6 * uni(hash64(self.seed, 90, ci + i0, cj + j0), 1), S_, 0.75 * S_)
        ci, cj = ci[s], cj[s]
        self.sicht_daten(welt_dir)
        prom = self.hs12[ci, cj] - self._grob(self.sd["umg"], ci.astype(float), cj.astype(float))
        ok = prom >= float(FG["prominenz_fuell_min_m"])
        ci, cj, prom = ci[ok], cj[ok], prom[ok]
        st["vorwahl"] = int(len(ci))
        if len(ci) == 0:
            log("Formgruppen: keine Kandidaten mit Prominenz >= %.0f m." % float(FG["prominenz_fuell_min_m"]))
            return [], 0
        hsh = hash64(self.seed, 91, ci + i0, cj + j0)
        vs = np.clip(self.grat[ci, cj] / kr_ref, 0, 1) + np.clip(prom / pr_ref, 0, 1)
        nmax = int(FG.get("vorwahl_max", 400))
        if len(ci) > nmax:
            o = np.lexsort((uni(hsh, 2), -vs))[:nmax]
            o.sort()
            ci, cj, prom, hsh = ci[o], cj[o], prom[o], hsh[o]
        sicht, vdir = self.sichtbarkeit(ci, cj)
        GW = FG["gewichte"]
        sicht_n = 1.0 - np.exp(-sicht / float(FG["sicht"]["ref"]))
        score = (float(GW["prominenz"]) * np.clip(prom / pr_ref, 0, 1) + float(GW["kruemmung"]) * np.clip(self.grat[ci, cj] / kr_ref, 0, 1)
                 + float(GW["sicht"]) * sicht_n)
        # Typ: kuppe (lokales Maximum), nase (Wand >= 50 Grad in der Nähe), sonst grat
        T_ = FG.get("typ", {})
        kup = self.hs12[ci, cj] >= boxmax(self.hs12, int(T_.get("kuppe_umkreis_m", 24)))[ci, cj] - float(T_.get("kuppe_toleranz_m", 1.0))
        # Kamm: höchster Punkt im Querschnitt +-kamm_quer_m quer zur Gratachse und deutlich über beiden Seiten
        qg = float(T_.get("kamm_quer_m", 24.0))
        quer = self.gratachse[ci, cj] + 0.5 * np.pi
        Hh, Wh = self.hs8.shape
        h0 = self.hs8[ci, cj]
        g1 = bilinear(self.hs8, np.clip(ci + np.sin(quer) * qg, 0, Hh - 1.001), np.clip(cj + np.cos(quer) * qg, 0, Wh - 1.001))
        g2 = bilinear(self.hs8, np.clip(ci - np.sin(quer) * qg, 0, Hh - 1.001), np.clip(cj - np.cos(quer) * qg, 0, Wh - 1.001))
        kamm = (h0 >= np.maximum(g1, g2)) & (h0 - 0.5 * (g1 + g2) >= float(T_.get("kamm_quer_relief_m", 2.5)))
        nase = dilate(self.m_wand, int(T_.get("nase_wand_abstand_m", 30)))[ci, cj] & ~kup & ~kamm
        typ = np.where(kup, "kuppe", np.where(nase, "nase", "grat"))
        # Hero je Kandidat (vektorisiert je Hero-Palette): Machbarkeit vor der Auswahl
        hero = self._form_hero(ci, cj, hsh, typ, vdir)
        mach = hero["ok"]
        st.update({"sicht_median": round(float(np.median(sicht)), 1) if len(sicht) else 0.0,
                   "machbar": int(mach.sum()), "verworfen_eingraben": int(hero["grund_eingraben"].sum()),
                   "verworfen_frei": int(hero["grund_frei"].sum()), "verworfen_ueberstand": int(hero["grund_ueberstand"].sum())})
        # gierige Auswahl: Score absteigend, Mindestabstand (auch zu Kandidaten im Rand)
        pmin = float(FG["prominenz_min_m"])
        smin = float(FG["score_min"])
        lo, hi = [int(x) for x in FG["je_feld"]]
        dmin = float(FG["abstand_min_m"])
        im = hero["im_feld"]
        order = np.lexsort((uni(hsh, 3), -score))
        gew = []
        for k in order:
            if not mach[k]:
                continue
            if any(math.hypot(hero["fi"][k] - hero["fi"][q], hero["fj"][k] - hero["fj"][q]) < dmin for q in gew):
                continue
            gew.append(k)
        stark = [k for k in gew if score[k] >= smin and prom[k] >= pmin]
        nim = [k for k in stark if im[k]][:hi]
        if len(nim) < lo:  # auffüllen bis je_feld[0] mit schwächeren, aber gültigen Kandidaten
            rest = [k for k in gew if im[k] and k not in nim]
            nim += rest[:lo - len(nim)]
        nim = sorted(nim, key=lambda k: (-score[k], int(hsh[k] % U64(1 << 62))))
        rand_anker = [k for k in gew if not im[k] and score[k] >= smin]
        self.form_anker = np.array([[hero["fi"][k], hero["fj"][k]] for k in nim + rand_anker]).reshape(-1, 2)
        st.update({"ausgewaehlt_im_feld": len(nim), "auswahl_gesamt_fenster": len(gew), "score_min": smin,
                   "aufgefuellt": int(sum(1 for k in nim if not (score[k] >= smin and prom[k] >= pmin)))})
        if not nim:
            log("Formgruppen: %d Kandidaten, %d machbar, keine im Feld ausgewaehlt." % (len(ci), int(mach.sum())))
            return [], 0
        sel = np.array(nim, dtype=np.int64)
        info = {k: (v[sel] if isinstance(v, np.ndarray) and len(v) == len(ci) else v) for k, v in hero.items()}
        info.update({"score": score[sel], "prom": prom[sel], "sicht": sicht[sel], "kruemmung": self.grat[ci[sel], cj[sel]],
                     "typ": typ[sel], "h": hsh[sel]})
        self.form_info = info
        teile = self._form_gruppen(info)
        log("Formgruppen: %d Kandidaten (Vorwahl %d, machbar %d) -> %d im Feld (Score >= %.2f, Abstand >= %.0f m, je Feld %d-%d), "
            "Typen %s; Hero sichtbar median %.1f m (max %.1f), Breite median %.1f m (max %.1f)." % (
                st["maskenzellen"], st["vorwahl"], int(mach.sum()), len(nim), smin, dmin, lo, hi,
                ",".join("%s %d" % (t, int((info["typ"] == t).sum())) for t in ("grat", "kuppe", "nase")),
                float(np.median(info["sicht_h"])), float(info["sicht_h"].max()), float(np.median(info["breite"])), float(info["breite"].max())))
        return teile, len(nim)

    def _form_hero(self, ci, cj, hsh, typ, vdir):
        """Hero-Klippe je Kandidat: Front (Sichtrichtung + Gefälle, am Grat quer zur Gratachse), Netzwahl (Typ, Biom-Palette,
        gewichtete Reihenfolge per Hash; bis zu hero.alternativen Netze werden probiert, das erste machbare gilt), Geometrie
        und Machbarkeit (_form_geo). Liefert Arrays je Kandidat."""
        FG = self.R["formgruppen"]
        HE = FG["hero"]
        n = len(ci)
        FW = HE.get("front_gewichte", {})
        g25 = self.gef25[ci, cj]
        g25n = np.linalg.norm(g25, axis=1, keepdims=True)
        f = float(FW.get("sicht", 1.0)) * vdir + float(FW.get("gefaelle", 0.7)) * g25 / np.maximum(g25n, 1e-9) * np.minimum(1.0, g25n / 0.1)
        ga = self.gratachse[ci, cj]
        ax_ = np.stack([np.cos(ga), np.sin(ga)], axis=1)
        fp = f - (f * ax_).sum(1, keepdims=True) * ax_
        quer = (typ == "grat") & (np.linalg.norm(fp, axis=1) > 0.2)
        f = np.where(quer[:, None], fp, f)
        nf = np.linalg.norm(f, axis=1, keepdims=True)
        zz = zwischen(hsh, 85, 0, 2 * np.pi)
        f = np.where(nf > 1e-6, f / np.maximum(nf, 1e-9), np.stack([np.cos(zz), np.sin(zz)], axis=1))
        # Netz-Reihenfolge je Kandidat: gewichtete Ziehung ohne Zurücklegen (Schlüssel u^(1/w))
        n_alt = max(1, int(HE.get("alternativen", 4)))
        biom = self.biom[ci, cj]
        pfad_alt = np.full((n, n_alt), "", dtype=object)
        achse_alt = np.full((n, n_alt), "auto", dtype=object)
        pal_name = np.full(n, "", dtype=object)
        for b in np.unique(biom):
            pn, ents = self.form_hero_palette(int(b))
            s = np.nonzero(biom == b)[0]
            pal_name[s] = pn or ""
            for t in ("grat", "kuppe", "nase"):
                st_ = s[typ[s] == t]
                e_t = [e for e in ents if t in e["typen"]] or ents
                if len(st_) == 0 or not e_t:
                    continue
                w = np.array([max(e["gewicht"], 1e-6) for e in e_t])
                u = uni(hash64(hsh[st_][:, None], 80, np.arange(len(e_t))[None, :]), 1)
                key = np.log(np.maximum(u, 1e-300)) / w[None, :]
                order = np.argsort(-key, axis=1, kind="stable")[:, :n_alt]
                for a in range(order.shape[1]):
                    for kk, e in enumerate(e_t):
                        m_ = st_[order[:, a] == kk]
                        pfad_alt[m_, a] = e["pfad"]
                        achse_alt[m_, a] = e.get("rueckseite") or HE.get("rueckseite_standard", "auto")
        if self.sh_aktiv:  # Runde 5: würfelartige Netze an Hängen > wuerfel_hang_grad nie als Hero
            w30 = self.hang[ci, cj] > float(self.SH.get("wuerfel_hang_grad", 30))
            for a in range(n_alt):
                bad = w30 & np.array([bool(p) and self.netz_form(p)["wuerfel"] for p in pfad_alt[:, a]], dtype=bool)
                pfad_alt[bad, a] = ""
                self.sh_stat["hero_wuerfel_gesperrt"] = self.sh_stat.get("hero_wuerfel_gesperrt", 0) + int(bad.sum())
        out = None
        offen = np.ones(n, dtype=bool)
        for a in range(n_alt):
            r = self._form_geo(ci, cj, hsh, f, pfad_alt[:, a], achse_alt[:, a])
            r["alternative"] = np.full(n, a)
            if out is None:
                out = r
            else:
                neu = offen & r["ok"]
                for k_, v in r.items():
                    if isinstance(v, np.ndarray) and len(v) == n:
                        out[k_][neu] = v[neu]
            offen &= ~out["ok"]
            if not offen.any():
                break
        for g_ in ("grund_eingraben", "grund_frei", "grund_ueberstand"):  # Gründe nur für endgültig nicht machbare
            out[g_] = out[g_] & ~out["ok"]
        out.update({"front": f, "biom": biom, "palette": pal_name})
        return out

    def _form_geo(self, ci, cj, hsh, f, pfade, achsen):
        """Geometrie einer Hero-Klippe je Kandidat für das gegebene Netz: Maßstab 1,0-2,0 (Ziel-Breite, Grenzen), Yaw (offene
        Seite = -Front), Versatz zur Front, Neigung (Normale, Kippen in den Hang, Schichtneigung) und Eingraben: die geneigte
        Unterseite muss an 9 Punkten des Fußabdrucks um boden_puffer_m unter dem Gelände liegen; nötiger Anteil > eingraben[1]
        oder Überstand über dem höchsten Fußpunkt < ueberstand_min_m -> nicht machbar."""
        HE = self.R["formgruppen"]["hero"]
        n = len(ci)
        H, W = self.h.shape
        i0, _, j0, _ = self.win
        hat = pfade != ""
        dims = {p: self.netz_xyz(p) for p in sorted(set(pfade[hat].tolist()))}
        wx = np.array([dims[p][0] if p else 1.0 for p in pfade])
        wy = np.array([dims[p][1] if p else 1.0 for p in pfade])
        Hm = np.array([dims[p][2] if p else 1.0 for p in pfade])
        mz = np.array([dims[p][3] if p else 0.0 for p in pfade])
        achse = np.array([("+y" if wx[k] >= wy[k] else "+x") if a == "auto" else a for k, a in enumerate(achsen)], dtype=object)
        auf_y = np.array([a[-1] == "y" for a in achse])
        w_lang = np.where(auf_y, wx, wy)
        w_tief = np.where(auf_y, wy, wx)
        s0, s1 = [float(x) for x in HE["massstab"]]
        eb0, eb1 = [float(x) for x in HE["eingraben"]]
        bury = zwischen(hsh, 83, eb0, eb1)
        ziel_b = zwischen(hsh, 82, float(HE["breite_m"][0]), float(HE["breite_m"][1]))
        sk = np.clip(ziel_b / np.maximum(w_lang, 0.1), s0, s1)
        sk = np.minimum(sk, np.maximum(s0, float(HE["breite_max_m"]) / np.maximum(w_lang, 0.1)))
        sk = np.minimum(sk, np.maximum(s0, float(HE["sicht_hoehe_max_m"]) / np.maximum(Hm * (1.0 - bury), 0.1)))
        nu = float(HE.get("nicht_uniform", 0.1))
        sx = sk * (1 + nu * (2 * uni(hsh, 86) - 1))
        sy = sk * (1 + nu * (2 * uni(hsh, 87) - 1))
        s_lang_max = np.maximum(sk, float(HE["breite_max_m"]) / np.maximum(w_lang, 0.1))  # Breitengrenze auch nach nicht_uniform
        sx = np.where(auf_y, np.minimum(sx, s_lang_max), sx)
        sy = np.where(auf_y, sy, np.minimum(sy, s_lang_max))
        # Yaw: lokale Achse der offenen Seite zeigt hangwärts (= -Front)
        bk = -f
        psi_b = np.arctan2(bk[:, 1], bk[:, 0])
        off = np.array([{"+x": 0.0, "-x": np.pi, "+y": -0.5 * np.pi, "-y": 0.5 * np.pi}.get(a, -0.5 * np.pi) for a in achse])
        yaw = psi_b + off
        ex = np.stack([np.cos(yaw), np.sin(yaw)], axis=1)          # lokale X-Achse in Welt (x, y)
        ey = np.stack([-np.sin(yaw), np.cos(yaw)], axis=1)         # lokale Y-Achse
        # Versatz zur Front: Rückseite steckt im Kamm
        tief_h = 0.5 * w_tief * np.where(auf_y, sy, sx)
        versatz = float(HE.get("versatz_tiefe_anteil", 0.5)) * tief_h
        fi = ci + f[:, 1] * versatz
        fj = cj + f[:, 0] * versatz
        inside = (fi >= 2) & (fi < H - 2) & (fj >= 2) & (fj < W - 2)
        fi_c, fj_c = np.clip(fi, 1, H - 1.001), np.clip(fj, 1, W - 1.001)
        hz = bilinear(self.h, fi_c, fj_c)
        cii, cjj = np.round(fi_c).astype(np.int64), np.round(fj_c).astype(np.int64)
        # Neigung: Anteil Normale, Kippen in den Hang (Oberkante zur Rückseite), Schichtneigung um das Streichen
        a_n = float(HE.get("normale_anteil", 0.3))
        up = (1.0 - a_n) * np.array([0.0, 0.0, 1.0])[None, :] + a_n * self.normal[cii, cjj]
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        kipp = np.radians(zwischen(hsh, 84, float(HE["kippen_grad"][0]), float(HE["kippen_grad"][1])))
        up = up + np.concatenate([bk * np.tan(kipp)[:, None], np.zeros((n, 1))], axis=1)
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        d = self.dip[cii, cjj] * float(HE.get("schichtneigung_anteil", 1.0))
        stv = self.strike[cii, cjj]
        sv = np.stack([np.cos(stv), np.sin(stv), np.zeros(n)], axis=1)
        up = up * np.cos(d)[:, None] + np.cross(sv, up) * np.sin(d)[:, None] + sv * (sv * up).sum(1, keepdims=True) * (1 - np.cos(d))[:, None]
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        # Fußabdruck (gedrehtes Rechteck, 9 Punkte): Gelände gegen die geneigte Unterseite, Freiheit
        fa = float(HE.get("fussabdruck_anteil", 0.8))
        ax_h, ay_h = 0.5 * wx * sx * fa, 0.5 * wy * sy * fa
        frei = self.m_frei[cii, cjj] & ~self.m_sperr[cii, cjj] & self.knick[cii, cjj]  # Hangknick-Pflicht auch an der Hero-Mitte
        verbot = self.m_wasser | self.m_weg | self.m_ort
        rueck_lok = {"+x": (1, 0), "-x": (-1, 0), "+y": (0, 1), "-y": (0, -1)}
        lu = np.array([rueck_lok.get(a, (0, 1))[0] for a in achse])
        lv = np.array([rueck_lok.get(a, (0, 1))[1] for a in achse])
        rel_max = np.full(n, -np.inf)   # max(Gelände-Unterseitenebene) relativ zur Mitte: bestimmt den Überstand
        rel_min = np.full(n, np.inf)    # min(...): bestimmt das nötige Eingraben
        b_r = np.zeros(n); b_f = np.zeros(n)
        for u_ in (-1, 0, 1):
            for v_ in (-1, 0, 1):
                dj = u_ * ax_h * ex[:, 0] + v_ * ay_h * ey[:, 0]
                di = u_ * ax_h * ex[:, 1] + v_ * ay_h * ey[:, 1]
                pi, pj = fi + di, fj + dj
                inside &= (pi >= 1) & (pi < H - 1) & (pj >= 1) & (pj < W - 1)
                pic, pjc = np.clip(pi, 1, H - 1.001), np.clip(pj, 1, W - 1.001)
                gh = bilinear(self.h, pic, pjc)
                dz = -(up[:, 0] * dj + up[:, 1] * di) / up[:, 2]   # Höhe der geneigten Unterseitenebene gegenüber der Mitte
                rel = gh - (hz + dz)
                rel_min = np.minimum(rel_min, rel)
                rel_max = np.maximum(rel_max, rel)
                frei &= ~verbot[np.round(pic).astype(np.int64), np.round(pjc).astype(np.int64)]
                b_r = np.where((lu == u_) & (lv == v_), gh, b_r)    # Mitte der Rückseite
                b_f = np.where((lu == -u_) & (lv == -v_), gh, b_f)  # Mitte der Front
        Hs = Hm * sk
        puffer = float(HE.get("boden_puffer_m", 0.3))
        noetig = (puffer - rel_min) / np.maximum(Hs, 0.1)
        bury = np.maximum(bury, noetig)
        ueber = Hs * (1.0 - bury) - rel_max
        g_eb = bury > eb1 + 1e-9
        g_ue = ueber < float(HE.get("ueberstand_min_m", 3.0))
        # Formgröße: max(Breite, sichtbare Höhe) >= groesse_min_m, sichtbare Höhe >= sicht_hoehe_min_m (sonst kein Hero, sondern Block)
        breite = w_lang * np.where(auf_y, sx, sy)
        g_ue |= (np.maximum(breite, Hs * (1.0 - bury)) < float(HE.get("groesse_min_m", 10.0))) | \
            (Hs * (1.0 - bury) < float(HE.get("sicht_hoehe_min_m", 4.0)))
        ok = hat & inside & frei & ~g_eb & ~g_ue
        i0f, i1f, j0f, j1f = self.feld_box
        return {"ok": ok, "im_feld": (fi + i0 >= i0f) & (fi + i0 < i1f) & (fj + j0 >= j0f) & (fj + j0 < j1f),
                "grund_eingraben": hat & inside & frei & g_eb, "grund_frei": hat & ~(inside & frei),
                "grund_ueberstand": hat & inside & frei & ~g_eb & g_ue, "pfad": pfade.copy(), "achse": achse,
                "q": quat_aus_yaw_up(yaw, up), "fi": fi, "fj": fj, "yaw": yaw, "sx": sx, "sy": sy, "sz": sk, "hz": hz, "bury": bury,
                "H": Hm, "z": hz * 100.0 - mz * 100.0 * sk - bury * Hm * 100.0 * sk, "breite": breite,
                "tiefe": 2.0 * tief_h, "sicht_h": Hs * (1.0 - bury), "hoehe_m": Hs, "ax": 0.5 * wx * sx, "ay": 0.5 * wy * sy,
                "rueck_hoeher": b_r > b_f, "rueck_diff_m": b_r - b_f, "ueberstand_m": ueber,
                "r_m": 0.5 * np.maximum(wx * sx, wy * sy)}

    def _ellipse_r(self, info, s_idx, ang):
        """Abstand Mitte -> Rand des Hero-Fußabdrucks (Ellipse mit Halbachsen ax, ay) in Richtung ang (Welt)."""
        rel_ = ang - info["yaw"][s_idx]
        return 1.0 / np.sqrt((np.cos(rel_) / info["ax"][s_idx]) ** 2 + (np.sin(rel_) / info["ay"][s_idx]) ** 2)

    def _form_gruppen(self, info):
        """Instanzen der ausgewählten Formgruppen: Hero (Akteur), Satelliten 2-6 m eng am Fuß (Front und Flanken, nicht hinten),
        Blockstrom ab dem Frontfuß hangabwärts, Kieselsaum um Satelliten/Blockstrom."""
        FG = self.R["formgruppen"]
        SA, BS = FG["satelliten"], FG["blockstrom"]
        i0, _, j0, _ = self.win
        m = len(info["fi"])
        hv = info["h"]
        gid = hash64(hv, 92, 0)
        gp = np.full(m, -1.0)  # Budget: Formgruppen zuletzt ausdünnen
        ci = np.round(info["fi"]).astype(np.int64)
        cj = np.round(info["fj"]).astype(np.int64)
        RO = self.R["rollen"]["hero"]
        hero = {"x": (info["fj"] + j0 - X0) * 100.0, "y": (info["fi"] + i0 - Y0) * 100.0, "z": info["z"], "q": info["q"],
                "sx": info["sx"], "sy": info["sy"], "sz": info["sz"], "pfad": info["pfad"].astype(object),
                "rolle": np.full(m, "hero"), "klasse": np.full(m, "formgruppe"), "koll": np.ones(m, bool),
                "schatten": np.ones(m, bool), "sicht": np.tile(np.array(FG["hero"].get("sichtweite_cm", RO["sichtweite_cm"]), dtype=float), (m, 1)),
                "akteur": np.ones(m, bool), "hoehe_m": info["hoehe_m"], "prio": uni(hv, 53), "ci": ci, "cj": cj,
                "fi": info["fi"], "fj": info["fj"], "gid": gid.astype(U64), "gprio": gp, "haupt": np.ones(m, bool),
                "sicht_h": info["sicht_h"], "r_m": info["r_m"], "dist_r": np.full(m, np.nan), "haengend": np.zeros(m, bool)}
        teile = [hero]
        for b in info["biom"]:
            self.haupt_je_biom[int(b)] += 1
        f = info["front"]
        ang_f = np.arctan2(f[:, 1], f[:, 0])
        for bi in np.unique(info["biom"]):
            sb = np.nonzero(info["biom"] == bi)[0]
            pal = self.pal_je_biom[int(bi)]
            K = self.klasse_param("formgruppe", bi)
            gross = []
            # Satelliten: abwechselnd links/rechts der Front, Winkel winkel_grad, am Rand der Hero-Ellipse
            cnt = ganz(hv[sb], 93, int(SA["anzahl"][0]), int(SA["anzahl"][1]))
            idx = np.repeat(sb, cnt)
            k = np.arange(len(idx)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
            if len(idx):
                hs_ = hash64(hv[idx], 94, k)
                seite = np.where(k % 2 == 0, 1.0, -1.0)
                w0, w1 = np.radians(SA["winkel_grad"][0]), np.radians(SA["winkel_grad"][1])
                ang = ang_f[idx] + seite * zwischen(hs_, 1, w0, w1)
                re_ = self._ellipse_r(info, idx, ang)
                lo, hi = [float(x) for x in SA["hoehe_m"]]
                u = k / np.maximum(np.repeat(cnt, cnt) - 1, 1)
                ziel = np.minimum(lo + (hi - lo) * zwischen(hs_, 3, 0.35, 1.0) * (1.0 - 0.45 * u), 0.6 * info["sicht_h"][idx])
                ziel = np.maximum(ziel, lo)
                r_sat = 0.45 * ziel  # grobe Fußhalbbreite des Satelliten
                dist = re_ * zwischen(hs_, 2, float(SA["abstand_rand"][0]), float(SA["abstand_rand"][1])) + 0.5 * r_sat
                t, _ = self._platzieren(pal, "formgruppe", bi, SA.get("rolle", "block"), info["fi"][idx] + np.sin(ang) * dist,
                                        info["fj"][idx] + np.cos(ang) * dist, hs_, info["yaw"][idx], ziel, gid[idx], gp[idx],
                                        dist_r=dist / np.maximum(re_, 1e-3), wmax=float(SA.get("breite_max_m", 9.0)))
                if t is not None:
                    teile.append(t)
                    gross.append(t)
            # Blockstrom ab dem Frontfuß
            pb = uni(hv[sb], 95) < float(BS.get("p", 0.8))
            s2 = sb[pb]
            if len(s2):
                d0 = self._ellipse_r(info, s2, ang_f[s2]) + float(BS.get("abstand_front_m", 1.5))
                sfi = info["fi"][s2] + np.sin(ang_f[s2]) * d0
                sfj = info["fj"][s2] + np.cos(ang_f[s2]) * d0
                Hh_ = self.h.shape
                ci2 = np.clip(np.round(sfi), 0, Hh_[0] - 1).astype(np.int64)
                cj2 = np.clip(np.round(sfj), 0, Hh_[1] - 1).astype(np.int64)
                steil = self.hang[ci2, cj2] >= float(BS.get("hang_min_grad", 10))
                s2, sfi, sfj, ci2, cj2 = s2[steil], sfi[steil], sfj[steil], ci2[steil], cj2[steil]
                if len(s2):
                    hz2 = hash64(hv[s2], 96, 0)
                    ab = self.abfall[ci2, cj2]
                    y2 = np.arctan2(ab[:, 1], ab[:, 0])
                    kr = BS.get("kopf_hoehe_m", [2.0, 3.5])
                    kopf, v = self._haupt(pal, "formgruppe", bi, [("block", np.ones(len(s2), bool), zwischen(hz2, 21, kr[0], kr[1]))],
                                          sfi, sfj, hz2, y2, gp[s2], strom=True)
                    if kopf is not None:
                        kopf["haupt"][:] = False
                        kopf["gid"] = gid[s2][v].astype(U64)
                        teile.append(kopf)
                        gross.append(kopf)
                        F = self.R["form"]
                        zt = self._zunge(pal, "formgruppe", bi, F, kopf["r_m"], kopf["sicht_h"], kopf["fi"], kopf["fj"], y2[v], hz2[v],
                                         gp[s2][v], gid[s2][v], BS.get("n", [4, 8]), float(BS.get("laenge_max_m", 40)))
                        teile += zt
                        gross += zt
            teile += self._saum(pal, "formgruppe", bi, K, gross)
        return [t for t in teile if t is not None and len(t["x"])]

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

    def waehle_ziel(self, kand, ziel_m, hh, wmax, regel=None):
        """Je Stück ein Netz, das die Zielhöhe (Netzhöhe × Maßstab) innerhalb [min_skalierung, max. Maßstab] und der Breitengrenze
        erreicht (Wahl per Hash); sonst Rückfall auf das nächstliegende Netz. Liefert (Index, Maßstab, Zahl Rückfälle, kein_netz).
        Runde 5 (regel, je Stück): achse = Ziel ist die längste Achse statt der Netzhöhe (Steilhang); Netzform-Regel: an Hängen >
        wuerfel_hang_grad (w30) würfelartige Netze und am Steilhang (steil) stehende Netze nur als Satellit mit d < satellit_max_m,
        nie als Hauptstück; strom_ohne_knick sperrt plattige Netze (Blockstrom ohne Hangknick); plattige/längliche Netze an Hängen
        > wuerfel_hang_grad bevorzugt (Ziehung u^(1/Gewicht)). kein_netz = kein zulässiges Netz (Stück entfällt)."""
        pf, h_m, _, _, w_m, smax = kand
        smin = float(self.R["form"]["min_skalierung"])
        n = len(ziel_m)
        bez = np.broadcast_to(h_m[None, :], (n, len(pf)))
        verbot = None
        u = uni(hash64(hh[:, None], 61, np.arange(len(pf))[None, :]), 62)
        if regel is not None:
            a_m, wue, steh, platt, gew_k = self.netzform_arrays(pf)[:5]
            bez = np.where(regel["achse"][:, None], a_m[None, :], h_m[None, :])
            s_c = np.minimum(np.clip(ziel_m[:, None] / bez, smin, smax[None, :]), wmax / w_m[None, :])
            d = s_c * a_m[None, :] * (1.0 + float(regel.get("nu", 0.0)))  # nicht_uniform kann die längste Achse vergrößern
            form_bad = wue[None, :] | (steh[None, :] & regel["steil"][:, None] & bool(self.SH.get("netzform", {}).get("stehend_sperren", True)))
            verbot = regel["w30"][:, None] & form_bad & (bool(regel["haupt"]) | (d >= float(self.SH.get("netzform", {}).get("satellit_max_m", 1.5))))
            verbot = verbot | (regel["strom_ohne_knick"][:, None] & platt[None, :])
            g = np.where(regel["w30"][:, None], gew_k[None, :], 1.0)
            u = np.where(g != 1.0, u ** (1.0 / g), u)
        s_need = ziel_m[:, None] / bez
        ok = (s_need >= smin) & (s_need <= smax[None, :]) & (w_m[None, :] * s_need <= wmax)
        if verbot is not None:
            ok &= ~verbot
        sc = np.where(ok, u, -1.0)
        k = np.argmax(sc, axis=1)
        kein = sc[np.arange(len(k)), k] < 0
        kein_netz = np.zeros(n, dtype=bool)
        if kein.any():  # Rückfall: zufällig unter den Netzen, deren erreichbare Höhe höchstens 25 % neben dem Ziel liegt
            s_c = np.minimum(np.clip(s_need[kein], smin, smax[None, :]), wmax / w_m[None, :])
            fehler = np.abs(np.log(np.maximum(bez[kein] * s_c, 1e-3) / ziel_m[kein][:, None]))
            if verbot is not None:
                fehler = np.where(verbot[kein], np.inf, fehler)
            nah = (fehler <= fehler.min(axis=1, keepdims=True) + math.log(1.25)) & np.isfinite(fehler)
            k[kein] = np.argmax(np.where(nah, u[kein], -1.0), axis=1)
            kein_netz[kein] = ~nah.any(axis=1)
        bk = bez[np.arange(n), k]
        s = np.minimum(np.clip(ziel_m / bk, smin, smax[k]), wmax / w_m[k])
        return k, s, int(kein.sum()), kein_netz

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

    def _platzieren(self, pal, kname, bi, rolle, fi, fj, hh, yaw0, ziel=None, gid=None, gprio=None, haupt=False, dist_r=None,
                    wmax=None, strom=False):
        """Netzwahl, Maßstab, Eingraben, Prüfung (Fenster, Feld, frei, schwebend, Platten-Regel) und Ausrichtung für n Stücke einer
        Rolle. ziel = sichtbare Zielhöhe in m (Maßstab = Ziel / (Netzhöhe × (1 - Eingraben))); None = Maßstab aus der Rollenregel.
        Runde 5: am Steilhang (Hang am Ort > steilhang.hang_grad, Rollen eingraben_rollen, nicht Kronen-Hauptstücke) Größe als
        längste Achse nach Potenzgesetz, Eingraben 50-70 % senkrecht zum Hang mit Schwebe-Test, Z = Normale, lange Achse entlang
        der Falllinie; Netzform-Regel an Hängen > wuerfel_hang_grad; strom = Blockstrom-Stück (Platten-Regel blockstrom_platten).
        Liefert (Instanz-Dict, Indizes der gültigen Eingaben) oder (None, leer)."""
        leer = (None, np.zeros(0, dtype=np.int64))
        n = len(fi)
        if n == 0:
            return leer
        K = self.klasse_param(kname, bi)
        RO = self.R["rollen"]
        F = self.R["form"]
        SH = self.SH
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
        H, W = self.h.shape
        fi_c0 = np.clip(fi, 1, H - 1.001); fj_c0 = np.clip(fj, 1, W - 1.001)
        ci0, cj0 = np.round(fi_c0).astype(np.int64), np.round(fj_c0).astype(np.int64)
        # Runde 5: Steilhang- und Netzform-Masken am Ort des Stücks
        hang0 = self.hang[ci0, cj0]
        kronen = (bool(haupt) and kname in SH.get("ausnahme_haupt_klassen", ["grat", "kuppe"])) or kname in SH.get("ausnahme_klassen", [])
        steil = (hang0 > float(SH.get("hang_grad", 35))) & (rolle in SH.get("eingraben_rollen", [])) & (not kronen) & self.sh_aktiv
        w30 = (hang0 > float(SH.get("wuerfel_hang_grad", 30))) & (rolle != "kiesel") & self.sh_aktiv
        strom_r = bool(strom) and self.bp_aktiv
        strom_ok = np.full(n, strom_r) & (~self.knick[ci0, cj0] if bool(self.BP.get("nur_mit_hangknick", True)) else False)
        PZ = SH.get("potenz", {})
        p_exp, p_dmin = float(PZ.get("exponent", 2.2)), float(PZ.get("d_min_m", 0.6))
        p_haupt = float(PZ.get("haupt_d_min_anteil", 0.4))  # Hauptstück: Potenzgesetz auf [anteil x geplante Größe, geplante Größe]
        kein_netz = np.zeros(n, dtype=bool)
        if ziel is not None:
            kand = self.kandidaten_netze(pal, rolle)
            if kand is None:
                return leer
            ziel_netz = np.asarray(ziel, dtype=np.float64) / np.maximum(1.0 - bury, 0.3)
            regel = None
            if w30.any() or strom_ok.any():
                if steil.any():  # geplante Netzhöhe als Zielwert der längsten Achse; Satelliten nach Potenzgesetz
                    lo_ = np.minimum(np.maximum(p_dmin, p_haupt * ziel_netz), ziel_netz) if haupt else np.minimum(p_dmin, ziel_netz)
                    d_ziel = potenz(hh, 47, lo_, ziel_netz, p_exp)
                    ziel_netz = np.where(steil, d_ziel, ziel_netz)
                    self.sh_stat["potenz_stuecke"] += int(steil.sum())
                regel = {"achse": steil, "steil": steil, "w30": w30, "haupt": haupt, "strom_ohne_knick": strom_ok,
                         "nu": float(ro["nicht_uniform"])}
            k, sk, n_rueck, kein_netz = self.waehle_ziel(kand, ziel_netz, hh,
                                                         float(wmax if wmax is not None else F["max_breite_m"].get(rolle, 16.0)), regel)
            self.form_rueckfall[rolle] = self.form_rueckfall.get(rolle, 0) + n_rueck
            pfade_l, H_cm, R_cm, MZ = kand[0], kand[1][k] * 100.0, kand[2][k], kand[3][k]
        else:
            pfade_l, hc, rc, mz = pa
            k = np.minimum((uni(hh, 40) * len(pfade_l)).astype(np.int64), len(pfade_l) - 1)
            sk = zwischen(hh, 41, ro["massstab"][0], ro["massstab"][1])
            if not haupt and rolle in ("band", "wand"):
                sk = sk * zwischen(hh, 43, 0.55, 0.9)  # Nebenstücke kleiner als das Hauptstück
            if w30.any():  # Runde 5: Netzform-Regel und Vorzug plattig/länglich (gewichtete Ziehung unter den zulässigen Netzen)
                a_m, wue, steh, platt, gew_k = self.netzform_arrays(pfade_l)[:5]
                d = sk[:, None] * a_m[None, :] * (1.0 + float(ro["nicht_uniform"]))
                bad = wue[None, :] | (steh[None, :] & steil[:, None] & bool(SH.get("netzform", {}).get("stehend_sperren", True)))
                verbot = w30[:, None] & bad & (bool(haupt) | (d >= float(SH.get("netzform", {}).get("satellit_max_m", 1.5))))
                u = uni(hash64(hh[:, None], 63, np.arange(len(pfade_l))[None, :]), 64) ** (1.0 / gew_k[None, :])
                sc = np.where(verbot, -1.0, u)
                k_neu = np.argmax(sc, axis=1)
                k = np.where(w30, k_neu, k)
                kein_netz = w30 & (sc[np.arange(n), k_neu] < 0)
            if steil.any():  # Potenzgesetz auf die längste Achse, Maßstab >= min_skalierung
                a_k = self.netzform_arrays(pfade_l)[0][k]
                d_alt = a_k * sk
                lo_ = np.minimum(np.maximum(p_dmin, p_haupt * d_alt), d_alt) if haupt else np.minimum(p_dmin, d_alt)
                d_neu = potenz(hh, 47, lo_, d_alt, p_exp)
                sk = np.where(steil, np.maximum(d_neu / a_k, np.minimum(sk, float(F["min_skalierung"]))), sk)
                self.sh_stat["potenz_stuecke"] += int(steil.sum())
            H_cm, R_cm, MZ = hc[k], rc[k], mz[k]
        self.sh_stat["netzform_verworfen"] += int(kein_netz.sum())
        pfade = np.array(pfade_l, dtype=object)[k]
        ist_pl = np.array([self.ist_platte(rolle, p) for p in pfade_l])[k]
        if ist_pl.any():
            pmin = float(self.R["platten"].get("eingraben_min", 0.5))
            bury = np.where(ist_pl, np.maximum(bury, pmin), bury)
        # Runde 5: Eingraben senkrecht zum Hang (Steilhang 50-70 %, Blockstrom-Platten >= eingraben_min)
        nf_pl = np.array([self.netz_form(p)["plattig"] for p in pfade_l], dtype=bool)[k]
        strom_pl = strom_r & nf_pl
        if steil.any():
            e0, e1 = [float(x) for x in SH.get("eingraben", [0.5, 0.7])]
            bury = np.where(steil, np.maximum(zwischen(hh, 46, e0, e1), np.where(ist_pl, bury, 0.0)), bury)
        if strom_pl.any():
            bury = np.where(strom_pl, np.maximum(bury, float(self.BP.get("eingraben_min", 0.4)) + float(self.BP.get("reserve", 0.02))), bury)
        senk = steil | strom_pl
        cosn = np.clip(self.normal[ci0, cj0, 2], 0.1, 1.0)
        cfak = np.where(senk, 1.0 / cosn, 1.0)  # z-Versatz je Eingrabtiefe (senkrecht zum Hang gemessen)
        nu = ro["nicht_uniform"]
        fx, fy = 1 + nu * (2 * uni(hh, 51) - 1), 1 + nu * (2 * uni(hh, 52) - 1)
        yaw_s = None
        if senk.any():  # Ausrichtung am Steilhang: längere waagerechte Achse entlang der Falllinie +- Streuung
            nfa = self.netzform_arrays(pfade_l)
            dxk, dyk = nfa[6][k], nfa[7][k]
            fall = np.arctan2(self.abfall[ci0, cj0, 1], self.abfall[ci0, cj0, 0])
            streu = np.radians(float(SH.get("ausrichtung_streuung_grad", 20)))
            lang_y = dyk * fy > dxk * fx
            phi = zwischen(hh, 56, -streu, streu)  # Abweichung der langen Achse von der Falllinie in der Hangebene
            eps = np.where(lang_y, np.arctan(np.tan(phi) / cosn), np.arctan(np.tan(phi) * cosn))  # waagerechter Yaw-Versatz dazu
            yaw_s = fall - np.where(lang_y, 0.5 * np.pi, 0.0) + eps + np.where(uni(hh, 57) < 0.5, np.pi, 0.0)
            # Schwebe-Test: Unterseite (Ebene an der Normale) an 8 Punkten des Fußabdrucks (Ellipse 0,9 x Halbachsen) gegen das Gelände
            L = 0.45 * np.maximum(dxk * fx, dyk * fy) * sk
            B = 0.45 * np.minimum(dxk * fx, dyk * fy) * sk
            fa = fall + np.arctan(np.tan(phi) * cosn)
            n0 = self.normal[ci0, cj0]
            gx, gy = -n0[:, 0] / n0[:, 2], -n0[:, 1] / n0[:, 2]
            hz0 = bilinear(self.h, fi_c0, fj_c0)
            konv = np.full(n, -np.inf)
            for t in np.radians(np.arange(0, 360, 45)):
                lx, ly = L * np.cos(t), B * np.sin(t)
                dj = lx * np.cos(fa) - ly * np.sin(fa)
                di = lx * np.sin(fa) + ly * np.cos(fa)
                hp = bilinear(self.h, np.clip(fi_c0 + di, 1, H - 1.001), np.clip(fj_c0 + dj, 1, W - 1.001))
                konv = np.maximum(konv, hz0 + gx * dj + gy * di - hp)
            tol = np.where(ist_pl, float(self.R["platten"].get("schwebe_toleranz_m", 0.05)), float(SH.get("schwebe_toleranz_m", 0.1)))
            noetig = (konv - tol) * cosn / np.maximum(H_cm * sk / 100.0, 0.05)
            bury = np.where(senk, np.maximum(bury, noetig), bury)
            zu_tief = senk & (bury > float(SH.get("eingraben_max", 0.85)))
            self.sh_stat["schwebend_verworfen"] += int(zu_tief.sum())
            kein_netz = kein_netz | zu_tief
        r_eigen = R_cm * sk  # cm
        i0, i1, j0, j1 = self.win
        i0f, i1f, j0f, j1f = self.feld_box
        inside = (fi >= 1) & (fi < H - 1) & (fj >= 1) & (fj < W - 1)
        fi_c, fj_c, ci, cj = fi_c0, fj_c0, ci0, cj0
        im_feld = (fi + i0 >= i0f) & (fi + i0 < i1f) & (fj + j0 >= j0f) & (fj + j0 < j1f)
        if rolle in ("stein", "kiesel", "platte"):
            frei = self.m_frei_klein[ci, cj]
            frei_om = self.m_frei_klein_om[ci, cj]
        else:
            frei = self.m_frei[ci, cj] & ~self.m_sperr[ci, cj]
            frei_om = self.m_frei_om[ci, cj] & ~self.m_sperr[ci, cj]
        self.meer_stat["kandidaten_gesperrt"] += int((inside & im_feld & frei_om & ~frei).sum())  # Runde 4: nur Meer-Regel
        hz = bilinear(self.h, fi_c, fj_c)
        rr = np.clip(r_eigen / 100.0, 0.5, 20.0)
        hmin_rand = np.minimum.reduce([bilinear(self.h, np.clip(fi_c + d[0] * rr, 1, H - 1.001), np.clip(fj_c + d[1] * rr, 1, W - 1.001))
                                       for d in ((1, 0), (-1, 0), (0, 1), (0, -1))])
        tiefe = bury * H_cm * sk / 100.0 * cfak
        nicht_schwebend = (hz - hmin_rand) <= tiefe + 0.3 + rr * np.tan(np.radians(60.0))
        ok = inside & im_feld & frei & nicht_schwebend & ~kein_netz
        if ist_pl.any():
            s = np.nonzero(ok & ist_pl)[0]
            if len(s):
                ok[s] = self.platte_pruefen(fi_c[s], fj_c[s], rr[s], hz[s], tiefe[s], ci[s], cj[s])
            self.platten_verworfen += int((inside & im_feld & frei & ist_pl & ~ok & ~kein_netz).sum())
        if not ok.any():
            if haupt:
                log("  %s/%s: alle %d Hauptstuecke (%s) verworfen (im Fenster %d, im Feld %d, frei %d, nicht schwebend %d, Netzform/Schwebe %d)" % (
                    kname, pal, n, rolle, int(inside.sum()), int(im_feld.sum()), int(frei.sum()), int(nicht_schwebend.sum()),
                    int(kein_netz.sum())))
            return leer
        v = np.nonzero(ok)[0]
        hh, fi, fj, ci, cj, hz, yaw0 = hh[v], fi[v], fj[v], ci[v], cj[v], hz[v], yaw0[v]
        pfade, H_cm, R_cm, MZ, sk, bury, ist_pl, r_eigen = pfade[v], H_cm[v], R_cm[v], MZ[v], sk[v], bury[v], ist_pl[v], r_eigen[v]
        senk, steil, cfak, fx, fy = senk[v], steil[v], cfak[v], fx[v], fy[v]
        # Ausrichtung: Z auf Normale, Kippen in den Hang (Z-Achse Richtung bergauf), Yaw = Hauptrichtung ± Streuung.
        # Platten: Z-Achse = Geländenormale, kein Kippen, keine Schichtneigung. Runde 5: Steilhang/Blockstrom-Platten ebenso.
        nrm = self.normal[ci, cj]
        kipp = np.radians(zwischen(hh, 45, ro["kippen_grad"][0], ro["kippen_grad"][1]))
        kipp = np.where(ist_pl | senk, 0.0, kipp)
        up = nrm + np.concatenate([-self.abfall[ci, cj] * np.tan(kipp)[:, None], np.zeros((len(kipp), 1))], axis=1)
        up /= np.linalg.norm(up, axis=1, keepdims=True)
        if rolle == "kiesel":
            yaw = zwischen(hh, 50, 0, 2 * np.pi)
        else:
            streu = np.radians(F.get("yaw_streuung_grad", self.R["gruppe"]["yaw_streuung_grad"]))
            yaw = yaw0 + zwischen(hh, 50, -streu, streu)
        if yaw_s is not None:
            yaw = np.where(senk, yaw_s[v], yaw)
        if kname in ("band", "wand") and rolle != "kiesel":
            d = np.where(ist_pl | senk, 0.0, self.dip[ci, cj])
            sv = np.stack([np.cos(yaw0), np.sin(yaw0), np.zeros_like(yaw0)], axis=1)  # Streichvektor
            up = up * np.cos(d)[:, None] + np.cross(sv, up) * np.sin(d)[:, None] + sv * (sv * up).sum(1, keepdims=True) * (1 - np.cos(d))[:, None]
            up /= np.linalg.norm(up, axis=1, keepdims=True)
        q = quat_aus_yaw_up(yaw, up)
        sx = sk * fx
        sy = sk * fy
        sz = sk
        m = len(v)
        hoehe_m = H_cm * sz / 100.0
        koll = np.full(m, bool(ro["kollision"])) & (hoehe_m >= self.R.get("kollision_ab_hoehe_m", 0.8))
        akteur = np.full(m, rolle == "wand") | ((rolle == "hero") & (hoehe_m >= self.R.get("akteur_ab_hoehe_m", 5.0)))
        return {"x": (fj + j0 - X0) * 100.0, "y": (fi + i0 - Y0) * 100.0, "z": hz * 100.0 - MZ * sz - bury * H_cm * sz * cfak, "q": q,
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

    def _haupt(self, pal, kname, bi, rollen_ziel, gi, gj, gh, gyaw, gprio, strom=False):
        """Hauptstücke je Gruppe; rollen_ziel = Liste (rolle, maske, ziel-array oder None). Liefert (dict, Gruppenindizes)."""
        teile, idx = [], []
        for rolle, maske, ziel in rollen_ziel:
            s = np.nonzero(maske)[0]
            if len(s) == 0:
                continue
            t, ok = self._platzieren(pal, kname, bi, rolle, gi[s], gj[s], hash64(gh[s], 30, 0), gyaw[s],
                                     None if ziel is None else ziel[s], gh[s], gprio[s], haupt=True, strom=strom)
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
        haupt, v = self._haupt(pal, kname, bi, [("block", np.ones(n, bool), ziel)], gi, gj, gh, gyaw, gprio, strom=True)
        if haupt is None:
            return []
        self.haupt_je_biom[int(bi)] += len(haupt["x"])
        teile, gross = [haupt], [haupt]
        zt = self._zunge(pal, kname, bi, F, haupt["r_m"], haupt["sicht_h"], haupt["fi"], haupt["fj"], gyaw[v], gh[v], gprio[v], gh[v],
                         K.get("n", K.get("block", [3, 5])), float(K.get("laenge_max_m", 30)))
        teile += zt
        gross += zt
        teile += self._saum(pal, kname, bi, K, gross)
        return teile

    def _zunge(self, pal, kname, bi, F, Rh, Hh, cfi, cfj, yaw, hv, gp, gid, nr, laenge_max):
        """Schwanz einer Blockstrom-Zunge ab dem Kopfblock (Mitte cfi/cfj, Radius Rh, sichtbare Höhe Hh): n Blöcke/Steine entlang
        der Falllinie yaw, Größe abnehmend (form.strom_groesse), Fächer breiter, Länge <= laenge_max. gid = Gruppen-Id je Kopf."""
        teile = []
        m = len(hv)
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
            lang_ok = s_lang + r_est <= laenge_max
            for rolle, maske in (("block", t >= 0.8), ("stein", t < 0.8)):
                s = np.nonzero(maske & lang_ok)[0]
                if len(s) == 0:
                    continue
                tt, _ = self._platzieren(pal, kname, bi, rolle, pfi[s], pfj[s], hs_[s], y_[s], np.maximum(t[s], 0.5), gid[idx][s],
                                         gp[idx][s], strom=True)
                if tt is not None:
                    teile.append(tt)
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
            # Runde 4: kueste/kueste_nur = Abstand zum Meer; Strandklassen = Abstand zu allem Wasser; sonst Ufer = Süßwasser
            art = "meer" if z["meer_nur"] else ("alle" if z["strand"] else "suess")
            wm = {"meer": self.meer, "alle": self.wasser_alle, "suess": self.m_suess}[art]
            maxd = int(min(64, max(1.0, z["wasser"][3])))
            k = ("wasser", art, maxd)
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
        return w * self.zusatz_frei(z)

    def zusatz_frei(self, z):
        """Freie Zellen einer Zusatzklasse (Runde 4): meer_rolle ab tief_m, Strandklassen ab 0 m, sonst Land ohne Strandsaum."""
        klein = z["rolle"] in ("stein", "kiesel", "platte")
        if z["meer_rolle"]:
            return self.m_frei_meer & (True if klein else ~self.m_sperr)
        if z["strand"]:
            return self.m_frei_strand_klein if klein else (self.m_frei_strand & ~self.m_sperr)
        return self.m_frei_klein if klein else (self.m_frei & ~self.m_sperr)

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
            w = self.zusatz_frei(z).astype(np.float64)
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
        # Runde 3: biombeschränkte Netze (rote Findlinge) je Stück nach Biom der Zelle; Ersatz grau gleicher Größe
        restr = [p for p in pfade if self.nbs.erlaubt(p) is not None] if self.nbs.aktiv else []
        ersatz_neu = []
        for p in restr:
            for q in self.nbs.ersatz_fuer(p):
                if q not in pfade:
                    pfade.append(q)
                    ersatz_neu.append(q)
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
        sperre_weg = np.zeros(len(k), dtype=bool)
        if restr:
            bp = self.biom[pci, pcj]
            braucht = np.array([any(not self.nbs.darf(p, b_) for p in restr) for b_ in range(len(BIOME))])
            A_ = np.array([[self.nbs.darf(p, b_) for b_ in range(len(BIOME))] for p in pfade])
            for q in ersatz_neu:  # Ersatz nur dort, wo ein beschränktes Netz verboten ist
                A_[pfade.index(q)] = braucht
            bad = ~A_[k, bp]
            for b_ in np.unique(bp[bad]):
                okk = np.nonzero(A_[:, b_])[0]
                s_ = np.nonzero(bad & (bp == b_))[0]
                if len(okk) == 0:
                    sperre_weg[s_] = True
                    continue
                k[s_] = okk[np.minimum((uni(hh[s_], 47) * len(okk)).astype(np.int64), len(okk) - 1)]
            self.netzsperre_stat.setdefault("zusatzklassen", {})[name] = {
                "netze": [p.rsplit("/", 1)[-1] for p in restr], "ersatz": [p.rsplit("/", 1)[-1] for p in ersatz_neu],
                "stuecke_umgestellt": int((bad & ~sperre_weg).sum()), "stuecke_ohne_ersatz_entfallen": int(sperre_weg.sum())}
            log("Zusatzklasse %s: biombeschraenkte Netze %s (nur %s): %d Stuecke im Fremdbiom auf grauen Ersatz %s umgestellt%s." % (
                name, ",".join(p.rsplit("/", 1)[-1] for p in restr), self.nbs.biome_text(restr[0]), int((bad & ~sperre_weg).sum()),
                ",".join(p.rsplit("/", 1)[-1] for p in ersatz_neu) or "-",
                (", %d ohne Ersatz entfallen" % int(sperre_weg.sum())) if sperre_weg.any() else ""))
        yaw_alle = zwischen(hh, 50, 0, 2 * np.pi)
        yp = p_yaw[idx]
        yaw_alle = np.where((m == 0) & ~np.isnan(yp), np.nan_to_num(yp), yaw_alle)
        ms = z["massstab"] or ro["massstab"]
        sk = zwischen(hh, 41, ms[0], ms[1])
        eb = z["eingraben"] or ro["eingraben"]
        bury = zwischen(hh, 44, eb[0], eb[1])
        # Runde 5: Steilhang- und Netzform-Regel auch für Zusatzklassen (Felsrollen, nicht hängend, kein Akteur)
        SH = self.SH
        z_fels = self.sh_aktiv and not z["z_versatz"] and not z["akteur"] and z["rolle"] in SH.get("eingraben_rollen", [])
        steil = np.zeros(len(hh), dtype=bool)
        if z_fels:
            hang0 = self.hang[pci, pcj]
            w30 = hang0 > float(SH.get("wuerfel_hang_grad", 30))
            steil = hang0 > float(SH.get("hang_grad", 35))
            if w30.any():
                NF = SH.get("netzform", {})
                a_m, wue, steh, _pl, gew_k = self.netzform_arrays(pfade)[:5]
                bad = wue[None, :] | (steh[None, :] & steil[:, None] & bool(NF.get("stehend_sperren", True)))
                smax_sat = float(NF.get("satellit_max_m", 1.5))
                verbot = w30[:, None] & bad & ((m == 0)[:, None] | (sk[:, None] * a_m[None, :] * (1.0 + float(ro["nicht_uniform"])) >= smax_sat))
                if restr:  # Netz-Biomsperre bleibt gültig
                    verbot |= ~A_[:, self.biom[pci, pcj]].T
                falsch = verbot[np.arange(len(k)), k] & ~sperre_weg
                if falsch.any():
                    s_ = np.nonzero(falsch)[0]
                    u_ = uni(hash64(hh[s_][:, None], 63, np.arange(len(pfade))[None, :]), 64) ** (1.0 / gew_k[None, :])
                    sc_ = np.where(verbot[s_], -1.0, u_)
                    kn = np.argmax(sc_, axis=1)
                    hat = sc_[np.arange(len(s_)), kn] >= 0
                    k[s_[hat]] = kn[hat]
                    rest = s_[~hat]  # kein zulässiges Netz: Satelliten auf < satellit_max_m verkleinern, Hauptstück entfällt
                    sat = rest[m[rest] > 0]
                    sk[sat] = np.minimum(sk[sat], 0.97 * smax_sat / a_m[k[sat]] / (1.0 + float(ro["nicht_uniform"])))
                    sperre_weg[rest[m[rest] == 0]] = True
                    self.sh_stat["netzform_umgestellt"] += int(hat.sum()) + int(len(sat))
                    self.sh_stat["netzform_verworfen"] += int((m[rest] == 0).sum())
        H_cm, R_cm, MZ = hc[k], rc[k], mzc[k]
        # Platten-Regel (Runde 2) zentral auch für Zusatzklassen: Rolle platte oder Platten-Netz laut Namensmuster
        ist_pl = np.array([self.ist_platte(z["rolle"], p) for p in pfade])[k]
        if ist_pl.any():
            bury = np.where(ist_pl, np.maximum(bury, float(self.R["platten"].get("eingraben_min", 0.5))), bury)
        cfak = np.ones(len(hh))
        senk = np.zeros(len(hh), dtype=bool)
        if steil.any():  # Runde 5: Eingraben 50-70 % senkrecht zum Hang, Z = Normale, lange Achse entlang der Falllinie
            e0, e1 = [float(x) for x in SH.get("eingraben", [0.5, 0.7])]
            bury = np.where(steil, np.maximum(zwischen(hh, 46, e0, e1), np.where(ist_pl, bury, 0.0)), bury)
            senk = steil
            cosn = np.clip(self.normal[pci, pcj, 2], 0.1, 1.0)
            cfak = np.where(senk, 1.0 / cosn, 1.0)
            nfa = self.netzform_arrays(pfade)
            dxk, dyk = nfa[6][k], nfa[7][k]
            nu_ = ro["nicht_uniform"]
            fx_, fy_ = 1 + nu_ * (2 * uni(hh, 51) - 1), 1 + nu_ * (2 * uni(hh, 52) - 1)
            fall = np.arctan2(self.abfall[pci, pcj, 1], self.abfall[pci, pcj, 0])
            streu = np.radians(float(SH.get("ausrichtung_streuung_grad", 20)))
            lang_y = dyk * fy_ > dxk * fx_
            phi = zwischen(hh, 56, -streu, streu)
            eps = np.where(lang_y, np.arctan(np.tan(phi) / cosn), np.arctan(np.tan(phi) * cosn))
            yaw_s = fall - np.where(lang_y, 0.5 * np.pi, 0.0) + eps + np.where(uni(hh, 57) < 0.5, np.pi, 0.0)
            yaw_alle = np.where(senk, yaw_s, yaw_alle)
            L = 0.45 * np.maximum(dxk * fx_, dyk * fy_) * sk
            B = 0.45 * np.minimum(dxk * fx_, dyk * fy_) * sk
            fa = fall + np.arctan(np.tan(phi) * cosn)
            n0 = self.normal[pci, pcj]
            gx_, gy_ = -n0[:, 0] / n0[:, 2], -n0[:, 1] / n0[:, 2]
            hz0 = bilinear(self.h, fi_c, fj_c)
            konv = np.full(len(hh), -np.inf)
            for t_ in np.radians(np.arange(0, 360, 45)):
                lx, ly = L * np.cos(t_), B * np.sin(t_)
                dj_ = lx * np.cos(fa) - ly * np.sin(fa)
                di_ = lx * np.sin(fa) + ly * np.cos(fa)
                hp = bilinear(self.h, np.clip(fi_c + di_, 1, H - 1.001), np.clip(fj_c + dj_, 1, W - 1.001))
                konv = np.maximum(konv, hz0 + gx_ * dj_ + gy_ * di_ - hp)
            tol = np.where(ist_pl, float(self.R["platten"].get("schwebe_toleranz_m", 0.05)), float(SH.get("schwebe_toleranz_m", 0.1)))
            bury = np.where(senk, np.maximum(bury, (konv - tol) * cosn / np.maximum(hc[k] * sk / 100.0, 0.05)), bury)
            zu_tief = senk & (bury > float(SH.get("eingraben_max", 0.85)))
            self.sh_stat["schwebend_verworfen"] += int(zu_tief.sum())
            sperre_weg = sperre_weg | zu_tief
        r_eigen = R_cm * sk
        hz = bilinear(self.h, fi_c, fj_c)
        rr = np.clip(r_eigen / 100.0, 0.5, 20.0)
        hmin_rand = np.minimum.reduce([bilinear(self.h, np.clip(fi_c + d_[0] * rr, 1, H - 1.001), np.clip(fj_c + d_[1] * rr, 1, W - 1.001))
                                       for d_ in ((1, 0), (-1, 0), (0, 1), (0, -1))])
        nicht_schwebend = (hz - hmin_rand) <= bury * H_cm * sk / 100.0 * cfak + 0.3 + rr * np.tan(np.radians(60.0))
        if z["z_versatz"]:  # hängende Stücke (Pivot oben, z. B. Eisvorhänge): Floating-Prüfung entfällt bewusst
            nicht_schwebend = np.ones(len(hh), dtype=bool)
        ok = inside & im_feld & (w[pci, pcj] > 0) & nicht_schwebend & ~sperre_weg
        if ist_pl.any():
            s_ = np.nonzero(ok & ist_pl)[0]
            if len(s_):
                ok[s_] = self.platte_pruefen(fi_c[s_], fj_c[s_], rr[s_], hz[s_], (bury * H_cm * sk / 100.0 * cfak)[s_], pci[s_], pcj[s_])
            n_pl = int((inside & im_feld & (w[pci, pcj] > 0) & ist_pl & ~ok).sum())
            self.platten_verworfen += n_pl
            if n_pl:
                log("Zusatzklasse %s: %d Platten verworfen (Platten-Regel: Kies/Geroell/Fels-Lage >= %s, nicht schwebend)" % (
                    name, n_pl, self.R["platten"].get("lagen_min", 100)))
        if not ok.any():
            return None, len(ci)
        hh, pfi, pfj, pci, pcj, hz, k, sk, bury, H_cm, MZ, yaw_alle, ist_pl, r_eigen, m_, cfak, senk = (a[ok] for a in (
            hh, pfi, pfj, pci, pcj, hz, k, sk, bury, H_cm, MZ, yaw_alle, ist_pl, r_eigen, m, cfak, senk))
        gidx = idx[ok]
        k_ok = np.nonzero(ok)[0]
        kipp = np.radians(zwischen(hh, 45, ro["kippen_grad"][0], ro["kippen_grad"][1]))
        kipp = np.where(ist_pl | senk, 0.0, kipp)  # Platten (Runde 5: auch Steilhang): Z-Achse = Geländenormale
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
        t = {"x": (pfj + j0 - X0) * 100.0, "y": (pfi + i0 - Y0) * 100.0, "z": hz * 100.0 - MZ * sz - bury * H_cm * sz * cfak + zv * H_cm * sz, "q": q,
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

    def netz_biom_pruefung(self, a):
        """Schlussprüfung Netz-Biomsperre (Runde 3): Stücke mit biombeschränktem Netz in einer Zelle eines fremden Bioms (z. B.
        Satellit über der Biomgrenze) bekommen ein Ersatznetz gleicher Gesamthöhe (Eingrabanteil bleibt); ohne Ersatz entfallen sie."""
        st = self.netzsperre_stat.setdefault("schlusspruefung", {"umgestellt": 0, "entfallen": 0})
        if not self.nbs.aktiv or len(a["x"]) == 0:
            return a
        b = self.biom[a["ci"], a["cj"]]
        bad = np.array([not self.nbs.darf(p, bb) for p, bb in zip(a["pfad"], b)], dtype=bool)
        if not bad.any():
            return a
        weg = np.zeros(len(bad), dtype=bool)
        H, W = self.h.shape
        for k in np.nonzero(bad)[0]:
            alt = a["pfad"][k]
            ers = [q for q in self.nbs.ersatz_fuer(alt) if self.nbs.darf(q, b[k])]
            if not ers or a["haengend"][k]:
                weg[k] = True
                continue
            neu = ers[int(uni(np.array([a["gid"][k]], dtype=U64), 48)[0] * len(ers)) % len(ers)]
            h_alt, _, mz_alt = self.netz_mass(alt)
            h_neu, r_neu, mz_neu = self.netz_mass(neu)
            s_alt = float(a["sz"][k])
            s_neu = s_alt * h_alt / max(h_neu, 1e-3)
            hz = float(bilinear(self.h, np.clip(np.array([a["fi"][k]]), 1, H - 1.001), np.clip(np.array([a["fj"][k]]), 1, W - 1.001))[0])
            bury = (hz * 100.0 - mz_alt * s_alt - float(a["z"][k])) / max(h_alt * s_alt, 1e-3)
            f = s_neu / s_alt
            a["sx"][k] *= f
            a["sy"][k] *= f
            a["sz"][k] = s_neu
            a["z"][k] = hz * 100.0 - mz_neu * s_neu - bury * h_neu * s_neu
            a["pfad"][k] = neu
            a["r_m"][k] = r_neu * max(a["sx"][k], a["sy"][k]) / 100.0
            a["hoehe_m"][k] = h_neu * s_neu / 100.0
        st["umgestellt"] += int((bad & ~weg).sum())
        st["entfallen"] += int(weg.sum())
        log("Netz-Biomsperre Schlusspruefung: %d Stuecke mit biombeschraenktem Netz im Fremdbiom auf Ersatz umgestellt, %d entfallen." % (
            int((bad & ~weg).sum()), int(weg.sum())))
        return {k: v[~weg] for k, v in a.items()} if weg.any() else a

    def meer_schlussfilter(self, a):
        """Runde 4 (KONVENTIONEN §1b), Sicherheitsnetz: Geländehöhe bilinear am Instanzort; < tief_m nie, < 0 nur meer_rolle,
        0..saum_hoehe_m im Küstensaum (<= saum_m zum Meer) nur Strand-Zusatzklassen."""
        SF = self.meer_stat["schlussfilter"]
        if len(a["x"]) == 0:
            return a
        MP = self.MP
        H, W = self.h.shape
        hz = bilinear(self.h, np.clip(a["fi"], 1, H - 1.001), np.clip(a["fj"], 1, W - 1.001))
        mk = {"z_" + z["name"] for z in self.zusatz if z["meer_rolle"]}
        sk = {"z_" + z["name"] for z in self.zusatz if z["strand"] or z["meer_rolle"]}
        kl = a["klasse"].astype(str)
        meer_ok = np.isin(kl, sorted(mk)) if mk else np.zeros(len(kl), dtype=bool)
        strand_ok = np.isin(kl, sorted(sk)) if sk else np.zeros(len(kl), dtype=bool)
        saum = self.d_meer[a["ci"], a["cj"]] <= MP["saum_m"]
        r1 = hz < MP["tief_m"]
        r2 = ~r1 & (hz < 0.0) & ~meer_ok
        r3 = ~r1 & ~r2 & (hz < MP["saum_hoehe_m"]) & saum & ~strand_ok
        weg = r1 | r2 | r3
        SF["unter_tief"] += int(r1.sum())
        SF["unter_0_ohne_meer_rolle"] += int(r2.sum())
        SF["strandsaum_ohne_strand_rolle"] += int(r3.sum())
        if weg.any():
            log("Meer-Schlussfilter (Runde 4): %d Stuecke verworfen (unter %.1f m: %d, unter 0 ohne meer_rolle: %d, Strandsaum ohne Strand-Klasse: %d)." % (
                int(weg.sum()), MP["tief_m"], int(r1.sum()), int(r2.sum()), int(r3.sum())))
            return {k: v[~weg] for k, v in a.items()}
        return a

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
        if len(s) > B["akteure"]:  # Formgruppen-Heros (Runde 3) bleiben immer Akteure
            kleinste = s[np.lexsort((a["hoehe_m"][s], a["klasse"][s] == "formgruppe"))[: len(s) - B["akteure"]]]
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

    # Runde 5: Dichtegrenze am Steilhang und Kennzahlen ------------------------------------------------------------------
    def steil_maske(self):
        """Steilhangfläche (Hang > steilhang.hang_grad, Land ohne Wasser/Meer)."""
        return (self.hang > float(self.SH.get("hang_grad", 35))) & self.land & ~self.wasser_alle

    def steil_dichte(self, a):
        """Harte Dichtegrenze (steilhang.dichte): Stücke am Steilhang mit Blockgröße d > ab_m je Stufe höchstens 1 je flaeche_m2.
        Gierig in Rangfolge (Formgruppen-Hero, wand, Hauptstück, übrige; plattig/länglich vor übrigen; Gruppen-Priorität): Mindestabstand
        mindestabstand_faktor x sqrt(flaeche_m2) je Stufe, Quote je zelle_m-Zelle und je Feld. Formgruppen-Heros zählen, werden aber nie
        abgewiesen. Abgewiesene Stücke: Verkleinerung nach Potenzgesetz auf verkleinern_m (Eingrabanteil bleibt; Maßstab >=
        form.min_skalierung), sonst entfallen sie."""
        SH = self.SH
        D = SH.get("dichte", {})
        self.dichte_stat = {}
        stufen = sorted((float(s["ab_m"]), float(s["flaeche_m2"])) for s in D.get("stufen", []))
        if not self.sh_aktiv or not stufen or len(a["x"]) == 0:
            return a
        hg = float(SH.get("hang_grad", 35))
        fs_i, fs_j = self.feld_slice
        i0, _, j0, _ = self.win
        Z = int(D.get("zelle_m", 48))
        sm = self.steil_maske()[fs_i, fs_j]
        A_feld = float(sm.sum())
        ii_, jj_ = np.nonzero(sm)
        ck_all = ((ii_ + fs_i.start + i0) // Z) * 100000 + (jj_ + fs_j.start + j0) // Z
        keys, cnts = np.unique(ck_all, return_counts=True)
        flaeche = dict(zip(keys.tolist(), cnts.tolist()))
        d = self.blockgroesse(a)
        hang_i = self.hang[a["ci"], a["cj"]]
        aus = sorted(D.get("rollen_ausgenommen", []))
        zaehlt = (hang_i > hg) & ~a["haengend"].astype(bool)
        if aus:
            zaehlt &= ~np.isin(a["rolle"], aus)
        hero = (a["klasse"] == "formgruppe") & (a["rolle"] == "hero")
        rang = np.where(hero, 0, np.where(a["rolle"] == "wand", 1, np.where(a["haupt"], 2, 3)))
        bevor = np.array([self.netz_form(p)["gewicht"] > 1.0 for p in a["pfad"]], dtype=bool)
        kand = np.nonzero(zaehlt & (d > stufen[0][0]))[0]
        order = kand[np.lexsort((-a["prio"][kand], -a["gprio"][kand], ~bevor[kand], rang[kand]))]
        fak = float(D.get("mindestabstand_faktor", 0.8))
        S_ = len(stufen)
        r_s = [fak * math.sqrt(A) for _, A in stufen]
        q_feld = [int(math.floor(A_feld / A)) for _, A in stufen]
        gitter = [dict() for _ in range(S_)]
        zell = [dict() for _ in range(S_)]
        n_feld = [0] * S_
        annahme = np.zeros(len(a["x"]), dtype=bool)
        X, Y = a["x"] / 100.0, a["y"] / 100.0
        for k in order:
            stz = [s for s in range(S_) if d[k] > stufen[s][0]]
            ck = int((a["ci"][k] + i0) // Z) * 100000 + int((a["cj"][k] + j0) // Z)
            ok = True
            if not hero[k]:
                for s in stz:
                    if n_feld[s] >= q_feld[s] or zell[s].get(ck, 0) >= int(math.floor(flaeche.get(ck, 0) / stufen[s][1])):
                        ok = False
                        break
                    gx, gy = int(math.floor(X[k] / r_s[s])), int(math.floor(Y[k] / r_s[s]))
                    for ddx in (-1, 0, 1):
                        for ddy in (-1, 0, 1):
                            for (px, py) in gitter[s].get((gx + ddx, gy + ddy), ()):
                                if (px - X[k]) ** 2 + (py - Y[k]) ** 2 < r_s[s] ** 2:
                                    ok = False
                                    break
                            if not ok:
                                break
                        if not ok:
                            break
                    if not ok:
                        break
            if ok:
                annahme[k] = True
                for s in stz:
                    gx, gy = int(math.floor(X[k] / r_s[s])), int(math.floor(Y[k] / r_s[s]))
                    gitter[s].setdefault((gx, gy), []).append((X[k], Y[k]))
                    zell[s][ck] = zell[s].get(ck, 0) + 1
                    n_feld[s] += 1
        ab = np.zeros(len(a["x"]), dtype=bool)
        ab[kand] = ~annahme[kand]
        st = {"steilhang_flaeche_m2": int(A_feld), "hang_grad": hg, "zelle_m": Z, "kandidaten": int(len(kand)),
              "formgruppen_heros_am_steilhang": int((hero & zaehlt).sum()), "stufen": []}
        for s, (ab_m, A) in enumerate(stufen):
            vor = int((zaehlt & (d > ab_m)).sum())
            st["stufen"].append({"ab_m": ab_m, "flaeche_m2": A, "mindestabstand_m": round(r_s[s], 2), "quote_feld": q_feld[s],
                                 "vorher": vor, "nachher": int(n_feld[s]),
                                 "dichte_je_100m2_vorher": round(100.0 * vor / A_feld, 4) if A_feld else 0.0,
                                 "dichte_je_100m2_nachher": round(100.0 * n_feld[s] / A_feld, 4) if A_feld else 0.0,
                                 "grenze_je_100m2": round(100.0 / A, 4)})
        # Abgewiesene: verkleinern (Potenzgesetz) oder entfernen
        keep = np.ones(len(a["x"]), dtype=bool)
        n_klein = n_weg = 0
        if ab.any():
            s_ = np.nonzero(ab)[0]
            V = D.get("verkleinern_m", [0.6, 1.9])
            NF = SH.get("netzform", {})
            w30 = hang_i[s_] > float(SH.get("wuerfel_hang_grad", 30))
            fb = np.array([self.netz_form(p)["wuerfel"] or self.netz_form(p)["stehend"] for p in a["pfad"][s_]], dtype=bool)
            hi = np.where(w30 & fb, min(float(V[1]), 0.97 * float(NF.get("satellit_max_m", 1.5))), float(V[1]))
            hk = hash64(a["gid"][s_].astype(np.int64), np.round(a["x"][s_]).astype(np.int64), np.round(a["y"][s_]).astype(np.int64))
            d_neu = potenz(hk, 58, np.minimum(float(V[0]), hi), hi, float(SH.get("potenz", {}).get("exponent", 2.2)))
            f = d_neu / d[s_]
            darf = bool(D.get("verkleinern", True)) & (a["rolle"][s_] != "wand")
            klein = darf & (a["sz"][s_] * f >= float(self.R["form"]["min_skalierung"]))
            sk_ = s_[klein]
            fk = f[klein]
            H, W = self.h.shape
            hz = bilinear(self.h, np.clip(a["fi"][sk_], 1, H - 1.001), np.clip(a["fj"][sk_], 1, W - 1.001)) * 100.0
            a["z"][sk_] = hz - fk * (hz - a["z"][sk_])
            for key in ("sx", "sy", "sz", "hoehe_m", "sicht_h", "r_m"):
                a[key][sk_] = a[key][sk_] * fk
            a["koll"][sk_] &= a["hoehe_m"][sk_] >= float(self.R.get("kollision_ab_hoehe_m", 0.8))
            a["akteur"][sk_] &= a["hoehe_m"][sk_] >= float(self.R.get("akteur_ab_hoehe_m", 5.0))
            # Netz zu groß zum Verkleinern: Ersatz durch einen Stein der Biom-Palette (Rolle stein) gleicher Lage, sonst entfällt
            tausch = darf & ~klein
            n_tausch = 0
            if tausch.any():
                ok_t = self._stein_tausch(a, s_[tausch], d_neu[tausch], hk[tausch], hang_i[s_[tausch]])
                n_tausch = int(ok_t.sum())
                tausch[np.nonzero(tausch)[0][~ok_t]] = False
            keep[s_[~klein & ~tausch]] = False
            n_klein, n_weg = int(klein.sum()), int((~klein & ~tausch).sum())
        else:
            n_tausch = 0
        st.update({"verkleinert": n_klein, "durch_stein_ersetzt": n_tausch, "entfernt": n_weg})
        # Kontrolle (nach Verkleinern): Dichte je Stufe im Feld und je Zelle (Zellen mit >= halber Zellfläche Steilhang)
        d2 = self.blockgroesse(a)
        for s, (ab_m, A) in enumerate(stufen):
            m_ = keep & zaehlt & (d2 > ab_m)
            ck = ((a["ci"][m_] + i0) // Z) * 100000 + (a["cj"][m_] + j0) // Z
            kz, kc = np.unique(ck, return_counts=True)
            dm = [100.0 * c / flaeche.get(int(kk), 1) for kk, c in zip(kz, kc) if flaeche.get(int(kk), 0) >= 0.5 * Z * Z]
            st["stufen"][s].update({"kontrolle_anzahl": int(m_.sum()), "max_zelle_je_100m2": round(max(dm), 4) if dm else 0.0})
        self.dichte_stat = st
        log("Steilhang-Dichte (Runde 5): Flaeche > %.0f Grad %d m2; %s; %d verkleinert, %d durch Stein ersetzt, %d entfernt "
            "(Formgruppen-Heros am Steilhang %d)." % (
            hg, int(A_feld), "; ".join("> %.0f m: %d -> %d (Quote %d, %.3f -> %.3f je 100 m2, Grenze %.3f, max Zelle %.3f)" % (
                x["ab_m"], x["vorher"], x["nachher"], x["quote_feld"], x["dichte_je_100m2_vorher"], x["dichte_je_100m2_nachher"],
                x["grenze_je_100m2"], x["max_zelle_je_100m2"]) for x in st["stufen"]), n_klein, n_tausch, n_weg,
            st["formgruppen_heros_am_steilhang"]))
        return {k: v[keep] for k, v in a.items()} if not keep.all() else a

    def _stein_tausch(self, a, idx, d_neu, hk, hang_i):
        """Ersetzt Stücke idx (in place) durch ein Netz der Rolle stein der Biom-Palette mit längster Achse d_neu: gleiche Lage und
        Drehung (lange Achse bleibt auf derselben lokalen Achse), gleicher Eingrabanteil; Netzform-Regel (würfelartig/stehend nur
        < satellit_max_m) und Vorzug plattig/länglich; Platten-Netze laut Muster ausgeschlossen. Liefert Erfolg je Stück."""
        SH, F = self.SH, self.R["form"]
        NF = SH.get("netzform", {})
        smin = float(F["min_skalierung"])
        ro = self.R["rollen"]["stein"]
        nu = float(ro["nicht_uniform"])
        H, W = self.h.shape
        ok = np.zeros(len(idx), dtype=bool)
        a["rolle"] = a["rolle"].astype("<U12")  # "stein" darf nicht abgeschnitten werden
        for n_, k in enumerate(idx):
            pal = self.pal_je_biom[int(self.biom[a["ci"][k], a["cj"][k]])]
            pf = [p for p in self.paletten[pal].get("stein", []) if not self.ist_platte_pfad(p)]
            if not pf:
                continue
            a_m, wue, steh, _pl, gew = self.netzform_arrays(pf)[:5]
            s_need = d_neu[n_] / a_m
            smax = np.array([self.netz_info(p)[4] for p in pf])
            zul = (s_need >= smin) & (s_need <= smax)
            if hang_i[n_] > float(SH.get("wuerfel_hang_grad", 30)):  # Hauptstück bleibt nie würfelartig/stehend
                zul &= ~((wue | (steh & (hang_i[n_] > float(SH.get("hang_grad", 35)))))
                         & (bool(a["haupt"][k]) or d_neu[n_] * (1 + nu) >= float(NF.get("satellit_max_m", 1.5))))
            if not zul.any():
                continue
            u = uni(hash64(hk[n_], 59, np.arange(len(pf))), 1) ** (1.0 / gew)
            j = int(np.argmax(np.where(zul, u, -1.0)))
            neu = pf[j]
            fa = self.netz_form(a["pfad"][k])
            fn = self.netz_form(neu)
            h_alt, _, mz_alt = self.netz_mass(a["pfad"][k])
            h_neu, r_neu, mz_neu = self.netz_mass(neu)
            rx, ry = a["sx"][k] / a["sz"][k], a["sy"][k] / a["sz"][k]
            s_new = d_neu[n_] / max(fn["dx"] * rx, fn["dy"] * ry, fn["dz"])
            hz = float(bilinear(self.h, np.clip(np.array([a["fi"][k]]), 1, H - 1.001), np.clip(np.array([a["fj"][k]]), 1, W - 1.001))[0]) * 100.0
            bury_cf = (hz - mz_alt * a["sz"][k] - a["z"][k]) / max(h_alt * a["sz"][k], 1e-3)  # Eingrabanteil x z-Faktor
            lang_alt = fa["dy"] * a["sy"][k] > fa["dx"] * a["sx"][k]
            lang_neu = fn["dy"] * ry > fn["dx"] * rx
            if lang_alt != lang_neu:  # lange Achse bleibt in derselben Weltrichtung: 90 Grad um die lokale Z-Achse
                qx, qy, qz, qw = a["q"][k]
                c = math.sqrt(0.5)
                a["q"][k] = [qx * c + qy * c, qy * c - qx * c, qz * c + qw * c, qw * c - qz * c]
            a["pfad"][k] = neu
            a["sx"][k], a["sy"][k], a["sz"][k] = s_new * rx, s_new * ry, s_new
            a["z"][k] = hz - mz_neu * s_new - bury_cf * h_neu * s_new
            a["hoehe_m"][k] = h_neu * s_new / 100.0
            a["sicht_h"][k] = a["hoehe_m"][k] * max(0.0, 1.0 - bury_cf)
            a["r_m"][k] = r_neu * max(a["sx"][k], a["sy"][k]) / 100.0
            a["rolle"][k] = "stein"
            a["koll"][k] = bool(ro["kollision"]) and a["hoehe_m"][k] >= float(self.R.get("kollision_ab_hoehe_m", 0.8))
            a["akteur"][k] = False
            a["schatten"][k] = bool(ro["schatten"])
            a["sicht"][k] = ro["sichtweite_cm"]
            ok[n_] = True
        return ok

    def eingrab_senkrecht(self, a, idx):
        """Eingrabanteil senkrecht zum Hang (Anteil der Netzhöhe) für Instanzen idx: (Boden - Unterseite) x cos(Hang) / Höhe."""
        H, W = self.h.shape
        hz = bilinear(self.h, np.clip(a["fi"][idx], 1, H - 1.001), np.clip(a["fj"][idx], 1, W - 1.001)) * 100.0
        mz = np.array([self.netz_mass(p)[2] for p in a["pfad"][idx]])
        hc = np.array([self.netz_mass(p)[0] for p in a["pfad"][idx]])
        cosn = np.clip(self.normal[a["ci"][idx], a["cj"][idx], 2], 0.1, 1.0)
        tiefe_v = hz - mz * a["sz"][idx] - a["z"][idx]
        return tiefe_v * cosn / np.maximum(hc * a["sz"][idx], 1e-3), tiefe_v * cosn / 100.0

    def steil_statistik(self, a):
        """Kennzahlen Runde 5 (nach Budget und Kontaktsaum): Würfelanteil an Hängen > wuerfel_hang_grad nach Größe, Eingraben und
        Ausrichtung am Steilhang, Blockstrom-Platten. plan.json statistik.steilhang und Log."""
        def q(v, p):
            return round(float(np.percentile(v, p)), 3) if len(v) else None
        st = {"dichte": dict(getattr(self, "dichte_stat", {})), "netzform": dict(getattr(self, "netzform_info", {})),
              "zaehler": dict(self.sh_stat)}
        self.steil_stat = st
        if not self.sh_aktiv or len(a["x"]) == 0:
            return
        SH = self.SH
        hang_i = self.hang[a["ci"], a["cj"]]
        d = self.blockgroesse(a)
        fels = (a["rolle"] != "kiesel") & ~a["haengend"].astype(bool)
        wue = np.array([self.netz_form(p)["wuerfel"] for p in a["pfad"]], dtype=bool)
        m30 = fels & (hang_i > float(SH.get("wuerfel_hang_grad", 30)))
        anteil = {}
        for name, lo, hi in (("unter_1_5m", 0.0, 1.5), ("1_5_bis_2m", 1.5, 2.0), ("2_bis_4m", 2.0, 4.0), ("ueber_4m", 4.0, 1e9)):
            mm = m30 & (d >= lo) & (d < hi)
            anteil[name] = {"stuecke": int(mm.sum()), "wuerfelartig": int((mm & wue).sum()),
                            "anteil": round(float((mm & wue).sum()) / max(int(mm.sum()), 1), 4)}
        st["wuerfel_an_haengen_ueber_%d_grad" % int(float(SH.get("wuerfel_hang_grad", 30)))] = anteil
        kern = m30 & wue & (a["haupt"] | ((a["klasse"] == "formgruppe") & (a["rolle"] == "hero")))
        st["wuerfel_als_kern_oder_hero"] = int(kern.sum())
        # Eingraben/Ausrichtung am Steilhang (Rollen eingraben_rollen, ohne Ausnahmen: Formgruppen-Hero, wand, Kronen-Hauptstücke)
        kronen = (a["haupt"] & np.isin(a["klasse"], SH.get("ausnahme_haupt_klassen", ["grat", "kuppe"]))) | \
            np.isin(a["klasse"], SH.get("ausnahme_klassen", []) or ["-"])
        regel = fels & (hang_i > float(SH.get("hang_grad", 35))) & np.isin(a["rolle"], SH.get("eingraben_rollen", [])) & ~kronen \
            & ~(np.char.startswith(a["klasse"].astype(str), "z_") & a["akteur"]) & ~((a["klasse"] == "formgruppe") & (a["rolle"] == "hero"))
        idx = np.nonzero(regel)[0]
        if len(idx):
            anteil_s, tiefe_s = self.eingrab_senkrecht(a, idx)
            st["eingraben_steilhang"] = {"stuecke": int(len(idx)), "anteil_median": q(anteil_s, 50), "anteil_min": q(anteil_s, 0),
                                         "tiefe_m_median": q(tiefe_s, 50), "tiefe_m_min": q(tiefe_s, 0)}
            qq = a["q"][idx]
            dx = np.array([self.netz_form(p)["dx"] for p in a["pfad"][idx]]) * a["sx"][idx]
            dy = np.array([self.netz_form(p)["dy"] for p in a["pfad"][idx]]) * a["sy"][idx]
            x_, y_, z_, w_ = qq[:, 0], qq[:, 1], qq[:, 2], qq[:, 3]
            ax_x = np.stack([1 - 2 * (y_ * y_ + z_ * z_), 2 * (x_ * y_ + z_ * w_), 2 * (x_ * z_ - y_ * w_)], axis=1)  # lokale X-Achse
            ax_y = np.stack([2 * (x_ * y_ - z_ * w_), 1 - 2 * (x_ * x_ + z_ * z_), 2 * (y_ * z_ + x_ * w_)], axis=1)  # lokale Y-Achse
            ax_z = np.stack([2 * (x_ * z_ + y_ * w_), 2 * (y_ * z_ - x_ * w_), 1 - 2 * (x_ * x_ + y_ * y_)], axis=1)  # lokale Z-Achse
            lang = np.where((dy > dx)[:, None], ax_y, ax_x)
            nrm = self.normal[a["ci"][idx], a["cj"][idx]]
            ab = self.abfall[a["ci"][idx], a["cj"][idx]]
            fall3 = np.concatenate([ab * nrm[:, 2:3], -np.sqrt(np.maximum(1 - nrm[:, 2:3] ** 2, 0))], axis=1)  # Falllinie in der Hangebene
            c = np.abs((lang * fall3).sum(1)) / np.maximum(np.linalg.norm(lang, axis=1) * np.linalg.norm(fall3, axis=1), 1e-9)
            abw = np.degrees(np.arccos(np.clip(c, 0, 1)))
            hp = np.degrees(np.arcsin(np.clip(np.abs((lang * nrm).sum(1)) / np.maximum(np.linalg.norm(lang, axis=1), 1e-9), 0, 1)))
            kz = np.degrees(np.arccos(np.clip((ax_z * nrm).sum(1), -1, 1)))
            st["ausrichtung_steilhang"] = {"abweichung_falllinie_in_hangebene_grad_median": q(abw, 50), "p90": q(abw, 90),
                                           "max": q(abw, 100), "anteil_bis_20_grad": round(float((abw <= 20.01).mean()), 4),
                                           "lange_achse_aus_hangebene_grad_max": q(hp, 100),
                                           "z_achse_gegen_normale_grad_max": q(kz, 100)}
        # Blockstrom-Platten (Klassen fuss/blockstrom und Zungen der Formgruppen)
        zunge_fg = (a["klasse"] == "formgruppe") & ~a["haupt"] & ~np.isfinite(a["dist_r"]) & np.isin(a["rolle"], ["block", "stein"])
        kopf_fg = (a["klasse"] == "formgruppe") & (a["rolle"] == "block") & ~np.isfinite(a["dist_r"])
        strom = np.isin(a["klasse"], ["fuss", "blockstrom"]) | zunge_fg | kopf_fg
        platt = np.array([self.netz_form(p)["plattig"] for p in a["pfad"]], dtype=bool)
        sp = np.nonzero(strom & platt & fels)[0]
        bs = {"platten": int(len(sp)), "stuecke_gesamt": int((strom & fels).sum())}
        if len(sp):
            anteil_s, tiefe_s = self.eingrab_senkrecht(a, sp)
            bs.update({"eingraben_anteil_min": q(anteil_s, 0), "eingraben_anteil_median": q(anteil_s, 50),
                       "ohne_hangknick": int((~self.knick[a["ci"][sp], a["cj"][sp]]).sum()),
                       "anteil_ohne_hangknick": round(float((~self.knick[a["ci"][sp], a["cj"][sp]]).mean()), 4)})
        kp = np.nonzero(a["haupt"] & np.isin(a["klasse"], ["fuss", "blockstrom"]))[0]
        if len(kp):
            bs["koepfe_in_rinne_oder_hangfuss"] = round(float((self.rinne[a["ci"][kp], a["cj"][kp]] | (self.hohl25[a["ci"][kp], a["cj"][kp]] >= float(
                self.R["klassen"]["blockstrom"]["hohl_min"]))).mean()), 4)
        st["blockstrom_platten"] = bs
        dz = st["dichte"].get("stufen", [])
        log("Steilhang-Statistik (Runde 5): %s; Wuerfel an Haengen > %s Grad: %s; Wuerfel als Kern/Hero %d; Eingraben Steilhang median %s "
            "(min %s); Abweichung zur Falllinie median %s Grad; Blockstrom-Platten %d, Eingraben min %s, ohne Hangknick %s." % (
                ", ".join("> %.0f m %s (%.3f je 100 m2)" % (x["ab_m"], x.get("kontrolle_anzahl"), x["dichte_je_100m2_nachher"]) for x in dz) or "-",
                SH.get("wuerfel_hang_grad", 30), ", ".join("%s %d/%d" % (k_, v["wuerfelartig"], v["stuecke"]) for k_, v in anteil.items()),
                st["wuerfel_als_kern_oder_hero"], st.get("eingraben_steilhang", {}).get("anteil_median"),
                st.get("eingraben_steilhang", {}).get("anteil_min"),
                st.get("ausrichtung_steilhang", {}).get("abweichung_falllinie_in_hangebene_grad_median"), bs["platten"],
                bs.get("eingraben_anteil_min"), bs.get("ohne_hangknick", 0)))

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

    def formgruppen_statistik(self, a):
        """Kennzahlen Runde 3 (nach Budget und Kontaktsaum): Formgruppen (Hero-Netz, sichtbare Größe, Eingraben, Satelliten,
        Blockstrom), Begleitgruppen, Hangknick-Prüfung, Netz-Biomsperre. plan.json statistik.formgruppen und Log."""
        def q(v, p):
            return round(float(np.percentile(v, p)), 2) if len(v) else None

        st = {"vorauswahl": dict(getattr(self, "form_stat_vorab", {}))}
        fg = a["klasse"] == "formgruppe"
        hk = np.nonzero(fg & a["haupt"])[0]
        st["anzahl"] = int(len(hk))
        info = getattr(self, "form_info", None)
        if len(hk) and info is not None:
            gid_info = hash64(info["h"], 92, 0)
            pos = {int(g): i for i, g in enumerate(gid_info)}
            ii = np.array([pos.get(int(g), -1) for g in a["gid"][hk]])
            ii = ii[ii >= 0]
            netze = {}
            for p in info["pfad"][ii]:
                nm = self.netze[p]["name"]
                netze[nm] = netze.get(nm, 0) + 1
            hb = info["bury"][ii]
            st["typen"] = {t: int((info["typ"][ii] == t).sum()) for t in ("grat", "kuppe", "nase")}
            st["hero_netze"] = dict(sorted(netze.items()))
            st["hero_breite_m"] = {"min": q(info["breite"][ii], 0), "median": q(info["breite"][ii], 50), "max": q(info["breite"][ii], 100)}
            st["hero_sichtbar_hoch_m"] = {"min": q(info["sicht_h"][ii], 0), "median": q(info["sicht_h"][ii], 50),
                                          "max": q(info["sicht_h"][ii], 100)}
            st["hero_groesse_m"] = {"median": q(np.maximum(info["breite"][ii], info["sicht_h"][ii]), 50),
                                    "max": q(np.maximum(info["breite"][ii], info["sicht_h"][ii]), 100),
                                    "hinweis": "max(Breite, sichtbare Hoehe); Ziel 10-30 m"}
            st["hero_netzhoehe_x_massstab_m"] = {"median": q(info["hoehe_m"][ii], 50), "max": q(info["hoehe_m"][ii], 100)}
            st["massstab"] = {"min": q(info["sz"][ii], 0), "median": q(info["sz"][ii], 50), "max": q(info["sz"][ii], 100)}
            st["eingraben_anteil"] = {"min": q(hb, 0), "median": q(hb, 50), "max": q(hb, 100)}
            st["eingrabtiefe_m"] = {"median": q(hb * info["hoehe_m"][ii], 50), "max": q(hb * info["hoehe_m"][ii], 100)}
            st["rueckseite_hangwaerts_anteil"] = round(float(info["rueck_hoeher"][ii].mean()), 3)
            st["rueckseite_minus_front_boden_m"] = {"median": q(info["rueck_diff_m"][ii], 50), "min": q(info["rueck_diff_m"][ii], 0)}
            st["ueberstand_ueber_hoechstem_fusspunkt_m"] = {"min": q(info["ueberstand_m"][ii], 0), "median": q(info["ueberstand_m"][ii], 50)}
            st["score"] = {"min": q(info["score"][ii], 0), "median": q(info["score"][ii], 50)}
            st["prominenz_m"] = {"min": q(info["prom"][ii], 0), "median": q(info["prom"][ii], 50)}
            st["sicht"] = {"min": q(info["sicht"][ii], 0), "median": q(info["sicht"][ii], 50), "max": q(info["sicht"][ii], 100)}
            xy = np.stack([a["x"][hk], a["y"][hk]], axis=1) / 100.0
            if len(hk) > 1:
                dm = np.hypot(xy[:, None, 0] - xy[None, :, 0], xy[:, None, 1] - xy[None, :, 1])
                np.fill_diagonal(dm, np.inf)
                st["abstand_naechste_m"] = {"min": q(dm.min(1), 0), "median": q(dm.min(1), 50)}
            sat = fg & ~a["haupt"] & np.isfinite(a["dist_r"]) & (a["rolle"] != "kiesel")
            zunge = fg & ~a["haupt"] & ~np.isfinite(a["dist_r"]) & np.isin(a["rolle"], ["block", "stein"])
            ns = np.array([int((sat & (a["gid"] == g)).sum()) for g in a["gid"][hk]])
            nz = np.array([int((zunge & (a["gid"] == g)).sum()) for g in a["gid"][hk]])
            st["satelliten"] = {"gesamt": int(sat.sum()), "je_formgruppe": {"min": int(ns.min()), "median": q(ns, 50), "max": int(ns.max())},
                                "sichtbar_hoch_m": {"min": q(a["sicht_h"][sat], 0), "median": q(a["sicht_h"][sat], 50),
                                                    "max": q(a["sicht_h"][sat], 100)},
                                "abstand_zum_herorand_anteil": {"median": q(a["dist_r"][sat], 50), "max": q(a["dist_r"][sat], 100)}}
            st["blockstrom"] = {"stuecke": int(zunge.sum()), "formgruppen_mit_blockstrom": int((nz > 0).sum())}
            st["kiesel_im_saum"] = int((fg & (a["rolle"] == "kiesel")).sum())
            st["instanzen"] = int(fg.sum())
        st["begleitung"] = dict(getattr(self, "begleit_stat", {}))
        # Hangknick-Pflicht: Hauptstücke der Relief-Klassen auf Wiese ohne Hangknick (soll 0 sein)
        kl = self.R.get("hangknick", {}).get("klassen", []) + ["formgruppe"]
        hm = a["haupt"] & np.isin(a["klasse"], kl)
        wk = hm & self.m_gras[a["ci"], a["cj"]] & ~self.knick[a["ci"], a["cj"]]
        st["hangknick"] = {"kandidaten_verworfen_wiese_ohne_knick": dict(getattr(self, "wiese_stat", {})),
                           "hauptstuecke_auf_wiese_ohne_knick": int(wk.sum()),
                           "einzel_auf_wiese_ohne_knick": int((a["haupt"] & (a["klasse"] == "einzel") & self.m_gras[a["ci"], a["cj"]]
                                                              & ~self.knick[a["ci"], a["cj"]]).sum())}
        b = self.biom[a["ci"], a["cj"]]
        rot = np.array([self.nbs.erlaubt(p) is not None and not self.nbs.darf(p, bb) for p, bb in zip(a["pfad"], b)], dtype=bool)
        rot_ok = np.array([self.nbs.erlaubt(p) is not None for p in a["pfad"]], dtype=bool)
        st["netzsperre"] = dict(self.netzsperre_stat, beschraenkt_gesetzt=int(rot_ok.sum()), beschraenkt_im_fremdbiom=int(rot.sum()),
                                gesperrt_gesetzt=int(np.isin(a["pfad"], sorted(self.gesperrt)).sum()))
        self.fg_stat = st
        if st["anzahl"]:
            log("Formgruppen-Statistik: %d Formgruppen %s; Hero Breite median %s m (max %s), sichtbar hoch median %s m (max %s), "
                "Massstab %s-%s, eingegraben %s-%s (median %s); Satelliten %d (je Gruppe %s-%s, sichtbar median %s m); "
                "Blockstrom %d Stuecke; Rueckseite hangwaerts %.0f %%." % (
                    st["anzahl"], st["typen"], st["hero_breite_m"]["median"], st["hero_breite_m"]["max"],
                    st["hero_sichtbar_hoch_m"]["median"], st["hero_sichtbar_hoch_m"]["max"], st["massstab"]["min"], st["massstab"]["max"],
                    st["eingraben_anteil"]["min"], st["eingraben_anteil"]["max"], st["eingraben_anteil"]["median"],
                    st["satelliten"]["gesamt"], st["satelliten"]["je_formgruppe"]["min"], st["satelliten"]["je_formgruppe"]["max"],
                    st["satelliten"]["sichtbar_hoch_m"]["median"], st["blockstrom"]["stuecke"], 100 * st["rueckseite_hangwaerts_anteil"]))
        log("Pruefung: Hauptstuecke auf Wiese ohne Hangknick %d; biombeschraenkte Netze im Fremdbiom %d; gesperrte Netze %d." % (
            st["hangknick"]["hauptstuecke_auf_wiese_ohne_knick"], st["netzsperre"]["beschraenkt_im_fremdbiom"],
            st["netzsperre"]["gesperrt_gesetzt"]))

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
            cz = max(max(boden, 0.0) + ueber, zz - abstand * math.tan(math.radians(12.0)))  # höchstens 12 Grad Aufblick
            cams.append({"name": name, "x_cm": round(cx * 100), "y_cm": round(cy * 100), "z_cm": round(cz * 100),
                         "yaw_grad": round(math.degrees(math.atan2(zy - cy, zx - cx)), 1),
                         "pitch_grad": round(math.degrees(math.atan2(zz - cz, abstand)), 1),
                         "ziel_cm": [round(zx * 100), round(zy * 100), round(zz * 100)], "zweck": zweck,
                         "boden_aus": "hoehe.f32" if inn else "geschaetzt (ausserhalb Fenster)"})
        # Runde 3: Formgruppen (die drei mit dem höchsten Score) von der Front aus 300 m und die beste aus 120 m
        hf_ = np.nonzero(a["haupt"] & (a["klasse"] == "formgruppe"))[0]
        info = getattr(self, "form_info", None)
        if len(hf_) and info is not None:
            pos = {int(g): i for i, g in enumerate(hash64(info["h"], 92, 0))}
            ii = np.array([pos.get(int(g), -1) for g in a["gid"][hf_]])
            sc = np.where(ii >= 0, info["score"][np.maximum(ii, 0)], -1.0)
            for rang, k_ in enumerate(np.argsort(-sc, kind="stable")[:3]):
                k = hf_[k_]
                fr = info["front"][ii[k_]] if ii[k_] >= 0 else np.array([1.0, 0.0])
                kamera("formgruppe_300m_%d" % (rang + 1), k, 300.0, math.atan2(fr[1], fr[0]), 40.0,
                       "Formgruppe %s (%s) aus Tal-/Wegrichtung: Felskrone 10-30 m mit dem Hang verwachsen, Satelliten am Fuss" % (
                           rang + 1, info["typ"][ii[k_]] if ii[k_] >= 0 else "?"))
                if rang == 0:
                    kamera("formgruppe_front_120m", k, 120.0, math.atan2(fr[1], fr[0]), 20.0,
                           "Front der Hero-Klippe: offene Seite darf nicht sichtbar sein (sonst rueckseite im Regelblock umdrehen)")
                    kamera("formgruppe_flanke_120m", k, 120.0, math.atan2(fr[1], fr[0]) + 0.5 * np.pi, 20.0,
                           "Flanke: Eingraben 35-60 %, Rueckseite im Hang, Blockstrom am Fuss")
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
        # Runde 5: Steilhang (Zelle mit der größten Steilhangfläche, größtes Stück > 2 m dort) und Blockstrom in einer Rinne
        if self.sh_aktiv and len(a["x"]):
            hg_ = self.hang[a["ci"], a["cj"]]
            d_ = self.blockgroesse(a)
            Z = int(self.SH.get("dichte", {}).get("zelle_m", 48))
            sm = self.steil_maske()
            fs_i, fs_j = self.feld_slice
            sub = sm[fs_i, fs_j]
            nz_ = (sub.shape[0] // Z) * Z, (sub.shape[1] // Z) * Z
            if nz_[0] and nz_[1]:
                zf = sub[:nz_[0], :nz_[1]].reshape(nz_[0] // Z, Z, nz_[1] // Z, Z).sum(axis=(1, 3))
                m_ = np.zeros(len(a["x"]), dtype=bool)
                for zz in np.argsort(-zf.ravel(), kind="stable")[:40]:  # Zellen nach Steilhangfläche, erste mit Stück
                    zi, zj = np.unravel_index(int(zz), zf.shape)
                    ii0, jj0 = fs_i.start + zi * Z, fs_j.start + zj * Z
                    m_ = (hg_ > float(self.SH.get("hang_grad", 35))) & (a["rolle"] != "kiesel") & (a["ci"] >= ii0) & (a["ci"] < ii0 + Z) \
                        & (a["cj"] >= jj0) & (a["cj"] < jj0 + Z) & (d_ > 1.0)
                    if m_.any():
                        break
                if m_.any():
                    k = np.nonzero(m_)[0][int(np.argmax(d_[m_]))]
                    ab = self.abfall[a["ci"][k], a["cj"][k]]
                    kamera("steilhang_300m", k, 300.0, math.atan2(ab[1], ab[0]), 40.0,
                           "Steilhang > 35 Grad (Runde 5): wenige grosse, halb eingegrabene Platten entlang der Falllinie, dazwischen kleines "
                           "Geroell; kein Kistenhaufen aus wuerfeligen Bloecken")
                    kamera("steilhang_120m", k, 120.0, math.atan2(ab[1], ab[0]), 25.0,
                           "Steilhang nah: Bloecke > 2 m mit >= 10 m Abstand, Z an der Normale, 50-70 % eingegraben, keine sichtbare Unterseite")
            hr = np.nonzero(a["haupt"] & np.isin(a["klasse"], ["fuss", "blockstrom"]) & self.rinne[a["ci"], a["cj"]])[0]
            if len(hr):
                k = hr[np.argmax(a["hoehe_m"][hr])]
                ab = self.abfall[a["ci"][k], a["cj"][k]]
                kamera("blockstrom_rinne_60m", k, 60.0, math.atan2(ab[1], ab[0]), 12.0,
                       "Blockstrom in einer Rinne (Runde 5): Platten eingebettet (>= 40 %), nur mit Hangknick, nicht flach obenauf")
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
        stat["formgruppen"] = dict(getattr(self, "fg_stat", {}))
        stat["steilhang"] = dict(getattr(self, "steil_stat", {}))
        plan = plan_kopf(self.R, feld, int(n), self.stand)
        ms = getattr(self, "meer_stat", {})
        meer_gef = int(ms.get("kandidaten_gesperrt", 0) + sum(ms.get("schlussfilter", {}).values()))
        stat["meer"] = ms
        if ms.get("meer_zellen_fenster"):
            self.hinweise.append("Meer (Runde 4): %d Zellen im Fenster (hoehe < 0, nicht in karte_wasser), Kuestensaum %d Zellen; "
                                 "%d Stuecke durch Meer/Strandsaum verworfen (davon Schlussfilter %d)" % (
                                     ms["meer_zellen_fenster"], ms.get("kuestensaum_zellen_fenster", 0), meer_gef,
                                     sum(ms.get("schlussfilter", {}).values())))
        plan.update({"biome_fenster": self.biome_fenster, "zellen_zustaendig": int(self.zellen_zustaendig),
                     "biome_fenster_bezug": "land", "meer_zellen": int(ms.get("meer_zellen_fenster", 0)), "meer_gefiltert": meer_gef,
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
            rad = np.clip(np.round(a["r_m"]), 0, 20).astype(np.int64)
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
            "biome_fenster": {}, "biome_fenster_bezug": "land", "zellen_zustaendig": 0, "kollision_anzahl": 0, "dateien": {}, "akteure": [],
            "meer_zellen": 0, "meer_gefiltert": 0,
            "entfernen": AU.get("entfernen", ""), "ft_ordner": AU["ft_ordner"], "ft_praefix": AU["ft_praefix"],
            "quelle": "felsgruppen_plan.py (Korrektur Runde 5: Steilhang-Dichtegrenze, Potenzgesetz, Eingraben 50-70 %, Netzform-Regel, "
                      "Blockstrom-Platten; Runde 4: Meer = hoehe < 0 ohne karte_wasser; Runde 3: Formgruppen 10-30 m, Netz-Biomsperre, Hangknick; Runde 2: Gruppengrammatik, "
                      "Platten-Regel, Kontaktsaum, Sperrliste)",
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
    ap = argparse.ArgumentParser(description="Felsgruppen-Planer Eldarien (Auftrag 11 C, Korrektur Runde 5).")
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
