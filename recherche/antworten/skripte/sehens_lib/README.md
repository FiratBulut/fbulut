# sehens_lib – Baukasten für Auftrag 13 (Sehenswürdigkeiten)

Eigene Implementierung nach `vorlagen/FORMAT.md` §1, `vorlagen/SEHENS_FORMAT.md` und
`vorlagen/daten/sehens/legende.json`. Python 3.11+, nur NumPy + Pillow (SciPy wird genutzt, falls vorhanden).
Deterministisch, ASCII-Logs, keine Unreal-Importe.

## Einbinden (auch mit `python -I`)

`python -I` setzt den Skriptordner **nicht** in `sys.path` – deshalb explizit:

```python
import os, sys
sys.path.insert(0, os.path.join(REPO, "antworten", "skripte"))   # REPO = Wurzel des Repos
from sehens_lib import daten, gelaende, sicht, kandidaten, zeichnen
from sehens_lib import format as sfmt          # 'format' nicht als Name 'format' importieren
```

## Schnellstart

```python
welt = daten.lade()                      # 2 m aus vorlagen/daten/sehens; daten.lade(daten1m="export/unreal/welt") für 1 m
gel  = gelaende.Gelaende(welt)           # Ganze-Welt-Raster lazy + .npy-Cache (siehe unten)
wp   = sicht.Wegpunkte(welt, 20)         # Wegzellen auf 20 m ausgedünnt (für Sichtlinien)

belegt = sfmt.belegte_punkte("antworten/sehens", ausser_biom="aue")   # Orte anderer Biome (Abstände)
def score(welt, gel):                    # eigener Score: Arrays aus gel kombinieren
    return kandidaten.norm(gel.tpi(50), 0, 15) * 0.6 + kandidaten.norm(gel.neigung, 15, 45) * 0.4
liste = kandidaten.kandidaten(welt, gel, "aue", score, n=10, belegt=belegt)
k = liste[0]                             # dict: x_m, y_m, z_m, feld, boden, neigung_grad, tpi100_m, landform,
                                         #       abstand_weg_m, abstand_wasser_m, einzugsflaeche_max_m2, ...
s = sicht.sicht_von_wegen(welt, wp, k["x_m"], k["y_m"], ziel_hoehe_m=18)    # Leuchtfeuer?
v = sicht.verdeckt_vom_weg(welt, wp, k["x_m"], k["y_m"], ziel_hoehe_m=3)    # Fundstück?
e = kandidaten.erreichbarkeit(welt, gel, k["x_m"], k["y_m"])                # Fußweg <= 25 Grad?
oid = sfmt.ort_id("aue", 1, "Blautopf")                                      # "aue_01_blautopf"
kams = sicht.kameras_vorschlagen(welt, wp, oid, k["x_m"], k["y_m"], "fundstueck", 4,
                                 gel=gel, pfad_m=[p[:2] for p in e["pfad_m"]])
ort = sfmt.standort(oid, "Blautopf", "fundstueck", k["x_m"], k["y_m"], 45, kams, welt=welt,
                    ziel_hoehe_m=4, standort_begruendung="...", sicht={...}, erreichbar=e)
sfmt.schreibe_standorte("antworten/sehens/aue/standorte.json", "aue", [ort], welt=welt)   # prüft mit
zeichnen.draufsicht(welt, k["x_m"], k["y_m"], "antworten/sehens/aue/%s.png" % oid, groesse_m=500,
                    elemente=[{"typ": "kreis", "pos_m": [k["x_m"], k["y_m"]], "radius_m": 45, "name": "Becken"}],
                    kameras=kams, titel=oid)
```

## Module und Kernfunktionen

**daten.py** – Laden, Legende, Koordinaten
- `lade(daten2m=None, daten1m=None)` → `Welt`; Raster `hoehe` (m), `biom` (0–14, 255 = Meer), `boden` (0–21, 255),
  `weg`, `ort`, `wasser`, `meer` (Höhe < 0 und kein Süßwasser), `baeume4`/`baumhoehe4` (4 m), `baumhoehe_nativ`;
  Vektoren `baeche`, `teiche`, `wasser_welt`, `staedte` (x_m, y_m, radius_m).
- Koordinaten: `welt.m_zu_ij(x_m, y_m)`, `welt.ij_zu_m(i, j)`, `welt.cm_zu_ij`, `welt.ij_zu_cm`, Modul:
  `pixel_zu_m(i, j, zelle_m)`, `m_zu_pixel(x, y, zelle_m)`. Formel: `X_cm = (z·j + (z−1)/2 − 4730,5)·100`,
  `Y_cm = (z·i + (z−1)/2 − 4060,5)·100` (z = 1/2/4 m). Norden = −Y = Bildoben.
- `feld_von_m(x, y)` → "E5", `feld_grenzen_m("E5")`, `felder_im_kreis(x, y, r)`.
- `welt.hoehe_bei_m(x, y)` (bilinear), `welt.hoehe_bei_cm`, `welt.baumhoehe_bei_m`, `welt.biom_bei_m`, `welt.boden_bei_m`.
- `welt.fenster(x_m, y_m, radius_m)` / `welt.fenster_box(x0, y0, x1, y1)` → `Fenster` mit `.sl`, `.get("hoehe")`,
  `.get(array)`, `.x_m`, `.y_m`, `.gitter_m()`, `.lokal(x, y)`, `.fenster_ij_1m()` (für orte.json).
- `biom_name(code)`, `boden_name(code)`, `KLEINE_BIOME`, `argumente_hinzufuegen(argparse)` (`--daten2m/--daten1m/--cache`).

**gelaende.py** – Analyse (Array-Funktionen + `Gelaende` mit Cache)
- `hangneigung(h, z)` [Grad], `exposition(h, z)` [0 = N, 90 = O, hangab], `kruemmung(h, z, sigma_m)` → (profil, plan) [1/m]
  (> 0 konvex: Kante/Rücken, < 0 konkav: Hangfuß/Rinne), `tpi(h, z, r_m)`, `glaetten`, `box_mittel`, `max_filter`, `min_filter`.
- `abfluss(h, z, auslass)` → gefuellt, empfaenger (D8, flach), akkumulation_m2 – Senken vollständig gefüllt (Becken-Graph).
- `abstand(maske, z, max_m, indizes=False)` – exakte euklidische Distanz (+ nächster Index).
- `landformen(...)` – 10 Klassen nach Weiss (`LANDFORMEN`).
- `Gelaende(welt, cache=None)`: `neigung`, `exposition`, `tpi(r)`, `kruemmung(sigma)`, `landformen()`, `gefuellt`,
  `senkentiefe`, `empfaenger`, `akkumulation` (m²), `haupt_zufluss`, `tiefenlinien(min_m2)`, `gerinne_anfaenge(min_m2)`
  (Quellen), `stufen(...)` (Gefällsprünge entlang Tiefenlinien → Wasserfälle), `kuppen(...)`, `kessel(...)`,
  `grate(...)`, `kanten(...)`, `abstand_weg` + `weg_naechst`, `abstand_ort`, `abstand_wasser`, `abstand_meer`,
  `abstand_stadt` (zum Stadtrand), `biom_abstand(name)` (> 0 innen, < 0 außen), `stadt_abstand_punkt(x, y)`.
- Vektoren: `stufen_entlang_linie(welt, punkte_m)`, `bach_enden(welt)` (Quelle/Ende jedes Bachs), `polylinie_proben`.

**sicht.py** – Sichtlinien (Gelände + Baumhöhe, 4-m-Schritt)
- `Wegpunkte(welt, 20)`, `sicht_von_wegen(welt, wp, x, y, ziel_hoehe_m, r_min_m=300, r_max_m=800)` → n_sichtbar,
  anteil_wegpunkte, bester (Wegpunkt für `_fern`), sichtbar_ab_m.
- `verdeckt_vom_weg(welt, wp, x, y, ziel_hoehe_m=3, r_max_m=400)` → verdeckt, max_anteil, naechste_sicht_m.
- `beste_blickposition(welt, x, y, ziel_hoehe_m, r_min_m=30, r_max_m=150, gel=gel, bevorzugt_grad=None)` → `_held`.
- `sichtanteil(welt, ex, ey, tx, ty, H)` / `mindesthoehe(...)` für eigene Strahlen; Parameter `baum`, `baum_faktor`
  (0,85), `baum_block` (3 Proben unter Krone sperren), `schritt_m` (4).
- `kameras_vorschlagen(...)` → §8-Kameras `_anmarsch`, `_held`, `_nah` (+ `_fern` bei Leuchtfeuer);
  `zz_augenhoehe(...)` hält die Kamera trotz `max(Boden + Hoch, ZZ + 300)` auf Augenhöhe.

**kandidaten.py** – Suche und Erreichbarkeit
- `filter_maske(welt, gel, biom, weg_min_m=80, weg_max_m=300, stadt_min_m=150, ort_min_m=30, innen_min_m=None,
  wasser_ok=False, max_neigung=None, zusatz=None)` (kleine Biome: Mitte bis 150 m außerhalb erlaubt).
- `kandidaten(welt, gel, biom, score, n=10, abstand_m=None, maske=None, belegt=None, raster_m=10)` – greedy mit
  350 m (kleine Biome 200 m) untereinander und zu `belegt` (alle Biome).
- `merkmale(welt, gel, x, y, radius_m=40, biom=None)` – Kennzahlen für Begründung.
- `erreichbarkeit(welt, gel, x, y, max_grad=25)` – Dijkstra (4 m) vom Ort zum nächsten Weg; `erreichbar`, `modus`
  (streng/weich), `pfad_noetig`, `pfad_m`/`pfad_cm` (Polylinie Ort → Weg), `max_steigung_grad`, `steil_laenge_m`.
- Score-Hilfen `norm`, `glocke`, `score_praegnanz`, `score_mulde`, `score_kante` (Signatur `(welt, gel)`).

**zeichnen.py** – `draufsicht(welt, x, y, pfad, groesse_m=500, skala=2, elemente=[...], kameras=[...], titel=...)`
(Elemente: `punkt`, `kreis`, `linie`, `polygon`, `text`, Koordinaten `*_m` oder `*_cm`), `uebersicht(welt, pfad, biom, punkte)`.

**format.py** – `ort_id`, `kamera`, `standort`, `schreibe_standorte`, `lade_standorte`, `alle_standorte`,
`belegte_punkte`, `mindestabstand_m`, Phase 2: `ort_phase2`, `schreibe_orte`, `schreibe_f32` (Gelände-Δ), `schreibe_r8` (Lagen).

**sehens_pruefen.py** – `python -I antworten/skripte/sehens_lib/sehens_pruefen.py` prüft alle
`antworten/sehens/*/standorte.json` (Format, Kameras, Geländeregeln mit Daten, globale Abstände über alle Biome);
`--datei X/orte.json` prüft Phase 2 (Felder §2–§9, Budget, Dateigrößen, Rand Δ = 0, Umriss gegen Uhrzeigersinn =
Fläche > 0 in X/Y wie `wasser_welt.json`). Exit 1 bei FEHLER.

## Cache und Laufzeiten (2 m, 4789 × 3529, ohne SciPy)

- Ordner: `$SEHENS_CACHE` oder `--cache`, Standard
  `/tmp/claude-0/-home-user-fbulut/a2c581ba-c24a-5bce-9c65-c37d036a756e/scratchpad/a13/cache/welt_2m_<Fingerabdruck>/`
  (Fingerabdruck aus Daten + Version; neue Daten → neuer Unterordner). Arrays werden per Memory-Map geladen.
- Füllen: `python -I antworten/skripte/sehens_lib/gelaende.py --biome --kruemmung` (einmalig ~3,5 min).
- Erstberechnung: Abfluss ~23 s, je Distanz ~7–14 s, TPI ~4 s, Krümmung ~11 s je σ, Biomabstand 1–18 s.
  Aus dem Cache: ~0,3–0,6 s je Raster. Selbsttest mit Cache ~17 s.
- Speicher: ~70 MB je float32-Raster; die 1-m-Welt ist 4× größer.

## Selbsttest

`python -I antworten/skripte/sehens_lib/selbsttest.py [--biom bergwald] [--aus <Ordner>]` – schreibt nur nach
`--aus` (Standard Scratchpad `a13/`, nie ins Repo).

## Bekannte Grenzen

- Biomgrenzen sind Rechtecke; `biom_abstand` misst zum Rechteckrand – Boden/Form selbst prüfen.
- Bäume nur als 4-m-Näherung (`baeume_4m`, `baumhoehe_4m`); Kronen ohne Stammraum (unter Kronen keine Durchsicht).
- Abfluss auf dem Höhenraster (Wasserflächen sind Gelände = Seegrund, gefüllt); Bäche als Vektoren separat (`bach_enden`).
- `erreichbarkeit` rechnet auf 4 m gemittelten Höhen (kleine Stufen < 4 m verschwinden).
- §8: Die Kamera schaut immer leicht abwärts (`ZZ + 300` ≤ Kamerahöhe); sehr hoch liegende Ziele hebt die Regel an
  (Prüfer-HINWEIS).
