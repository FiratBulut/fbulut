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

## Pfade (Auftrag 13c)

Pfade stehen in der `standorte.json` ihres Bioms auf oberster Ebene (die alten `standorte_*.json` sind abgelöst):

```json
"pfade": [{"id": "lava_pfad_kratersteig_west", "art": "trampelpfad|serpentine|trittsteine", "breite_cm": 150,
           "punkte_cm": [[x, y], ...], "anschluss": "Archivpfad vor Zalas Archiv ...", "fuer": ["lava_07_basaltorgel"],
           "laenge_m": 916.0, "max_steigung_grad": 10.1}]
```
Orte, die nur über einen Pfad gelten, tragen `"pfad_id": "<id>"`. Ferats Werkzeug rechnet Serpentinen und den Geländeanschnitt.

- `daten.lade()` liest die Pfade **aller** Biome (`antworten/sehens/*/standorte.json`) und rastert sie zusätzlich zum Wegenetz
  als Weg: `welt.weg` = Wege + Pfade, `welt.weg_basis` = Wegenetz allein, `welt.pfade` (normiert, `punkte_m`),
  `welt.pfad_maske`, `welt.setze_pfade(liste)`. `daten.lade(pfade=False)` = altes Verhalten; `pfade="<sehens-Ordner>"` oder
  eine Liste geht auch. Ohne `"pfade"` in den Dateien ist alles wie bisher.
- Damit gelten Pfade überall als Weg: `gel.abstand_weg`/`weg_naechst` (Regel 80–300 m, Kandidatensuche `filter_maske`),
  `sicht.Wegpunkte` (Leuchtfeuer 300–800 m sichtbar, Fundstücke verdeckt), `kandidaten.erreichbarkeit` (Fußweg zum nächsten
  Weg oder Pfad). `gel.abstand_weg_basis` misst nur zum Wegenetz. Der Cache-Ordner bleibt gleich; der Abstand mit Pfaden liegt
  als `abstand_weg_p<Kennung>.npy` daneben (einmal ~12 s je Pfadstand, die 6 neuesten bleiben).
- `format.pfad(id, art, punkte_m, welt=welt, anschluss=..., fuer=[...])` baut einen Eintrag (Länge, max. Steigung aus der Höhe);
  `format.schreibe_standorte(..., pfade=[...])`, `format.alle_pfade(ordner)`; `belegte_punkte` liefert auch `pfad_id`;
  `alle_standorte` zählt Orte aus `standorte_*.json` nicht doppelt, wenn ihre id schon in einer `standorte.json` steht.
- `gelaende.pfad_profil(welt, punkte_m)` → Länge, Steigung je Segment (Fenster 10 m entlang des Pfads), max/mittel,
  Länge > 15 % und > 25°; `gelaende.abstand_zu_polylinien(x, y, linien)`.
- `zeichnen.draufsicht` zeichnet die Pfade aus `welt.pfade` automatisch (Farbe je `art`, Kennung, Legende; `pfade=False` aus).
- Prüfer: Schema (id `<biom>_pfad_<name>`, ≥ 2 Punkte, `breite_cm` 120–200, `art`), Anschluss (erster Punkt ≤ 30 m vom
  Wegenetz oder von einem anderen Pfad, sonst FEHLER), Steigung je Segment > 15 % → HINWEIS „Kehren nötig“ (bei `serpentine`
  erlaubt), schneidet Stadt (Radius aus `standorte.json`) oder Meer → WARNUNG, quert Süßwasser → HINWEIS, `pfad_id` muss
  existieren (FEHLER), doppelte Pfad-ids über alle Biome (FEHLER). `--sicht`: Leuchtfeuer von Weg/Pfad aus 300–800 m sichtbar,
  Fundstücke verdeckt.
- Ein Pfad soll **am Ort vorbei** (80–300 m) oder bis 80–300 m vor den Ort führen; den Rest geht man über den Fußweg
  (`pfad_cm` des Orts, `erreichbarkeit`). Endet ein Pfad direkt am Ort, ist der Wegabstand 0 m → FEHLER.

## Module und Kernfunktionen

**daten.py** – Laden, Legende, Koordinaten
- `lade(daten2m=None, daten1m=None, pfade=True)` → `Welt`; Raster `hoehe` (m), `biom` (0–14, 255 = Meer), `boden` (0–21, 255),
  `weg` (Wege + Pfade), `weg_basis` (nur Wege), `ort`, `wasser`, `meer` (Höhe < 0 und kein Süßwasser), `baeume4`/`baumhoehe4` (4 m), `baumhoehe_nativ`;
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

**format.py** – `ort_id`, `kamera`, `standort`, `pfad`, `schreibe_standorte`, `lade_standorte`, `alle_standorte`,
`alle_pfade`, `belegte_punkte`, `mindestabstand_m`, Phase 2: `ort_phase2`, `schreibe_orte`, `schreibe_f32` (Gelände-Δ), `schreibe_r8` (Lagen).

**Phase 2** (Auftrag 13, Lieferformat `vorlagen/SEHENS_FORMAT.md`) – siehe Abschnitt „Phase 2“ unten und
[`PLANER_ANLEITUNG.md`](PLANER_ANLEITUNG.md): `inventar.py`, `stempel.py`, `instanzen.py`, `rezept.py`, `vorschau.py`.

**sehens_pruefen.py** – `python -I antworten/skripte/sehens_lib/sehens_pruefen.py [--sicht]` prüft alle
`antworten/sehens/*/standorte.json` (Format, Kameras, Pfade, Geländeregeln mit Daten gegen Wege + Pfade aller Biome, globale
Abstände über alle Biome – noch vorhandene Varianten `*/standorte_*.json` zählen ohne Doppelzählung mit);
`--datei X/orte.json` prüft Phase 2: orte.json (§2–§9), Gelände/Lagen-Dateien, mit Daten Weg-/Wasserschutz und
Seeufer, Assets gegen das Inventar und – falls `X/sw_<biom>/` existiert oder `--ebene` angegeben ist – die
Instanz-Ebene (Format, Anzahlen, Assets, Feldrechteck, Akteure, Budget je Ort, Schweben/Versinken). Exit 1 bei FEHLER.

## Phase 2 – Planer-Bausteine (Auftrag 13)

Lieferformat: `vorlagen/SEHENS_FORMAT.md` (+ `FORMAT.md` §3). Muster-Planer: `skripte/sehens_bergwald/`.
Anleitung für neue Biom-Planer (Aufbau, Regel-Schema, Bausteine, fehlende Assets, Prüfschritte):
**[`PLANER_ANLEITUNG.md`](PLANER_ANLEITUNG.md)**.

| Modul | Inhalt |
|---|---|
| `inventar.py` | `Inventar.lade()` – `netze.csv`, `netze_masse.json` (Bounds/Pivot), `netz_sperre.json`, `netz_check_ergebnis.json`, `inventar_extra.json` (Niagara, Decals, Klänge), `material_parameter.json`. `netz(name\|pfad)`, `netz_pruefen`, `asset_pruefen(art, pfad, optional)` (fehlend → FEHLER, `optional` → HINWEIS; Houdini `SW_*` → FEHLER; Stadt-/Menschenklänge → FEHLER), `material_pruefen` (Master + Parameternamen). |
| `stempel.py` | `Stempel` (Gelände-Δ in m, gerechnet im nativen Raster, geschrieben IMMER 1 m): `mulde`, `kuppe`, `rinne` (auch absolute fallende Sohle), `terrasse`, `abbruch`, `glaetten`, `buckel`, `see_becken` (Becken + Uferring über dem Spiegel + Auslass-Lippe). `modus` add/min/max/setzen = Blending mit dem Bestand. `fertig()`: Rand Δ = 0 (≥ 8 m weich), Schutz ≤ 3 m an Wegen/Wasser (außer `ist_wasser`). `hoehe_bei_m`/`normale_bei_m` = Boden NACH dem Stempel. `senken()` findet geschlossene Senken. `Lagen`: `kreis`/Ring, `band`, `maske`, max-Kombination, fleckig (`flecken`). |
| `instanzen.py` | Quaternionen (`q_mul`, `q_yaw_kompass`, `q_kippen`, …), `orientierung(aufrecht\|hochkant\|liegend, yaw, normale, anteil, kippen)`, `platziere(...)` (Kontaktpunkte der Unterseite gegen das Gelände, Pivot aus Bounds, Eingraben), Streuung (`form_punkte`, `streue` mit Mindestabstand, `cluster`, `um_stuecke` = Kontaktzone um Fuß-Ellipsen), `Ebene` (sammelt, `ausduennen` nach §9, schreibt `sw_<biom>/<Feld>/plan.json` + f32 mit 10 float32 je Instanz, Akteure in `plan["akteure"]`), `lies_ebene`. |
| `rezept.py` | `OrtKontext(...).baue(hooks)` – baut einen Ort aus dem Regel-Block: Anker/Linien, Gelände, Wasser (§5), Gruppen je Detail-Ebene, Pfad (13c), Lagen, Effekte (§6), Klänge, Freiräume, Budget (§9), orte.json-Eintrag. `schreibe_biom(...)` schreibt orte.json, gelaende/, lagen/ und die Ebene. |
| `vorschau.py` | `vorschau(ctx, pfad)` → `test_<id>.png`: Gelände nach dem Stempel (rot/blau = Δ), geplante Lagen, Wasser, Instanzen je Detail-Ebene, Akteur-Grundrisse, Effekte, Pfad, Freiräume, Kameras, Legende mit Zahlen und Budget. |

Erweiterungen von `orte.json` (zusätzlich zu §2, von Ferats Werkzeugen ignorierbar): `pfad` (13c), `pfad_zugang` (Fußweg
`pfad_cm` zusätzlich zu einem Pfad aus `pfade`, Regel `pfad.zugang`), `klaenge`,
`freiraeume` (Bestand entfernen), `detail_ebenen` (Witcher-Größenstufen), `hinweise`, `gelaende.begruendung`,
`gelaende.ist_wasser`, `see.auslass_cm`, `see.freibord_min_m`. In `plan.json`: `orte_budget`, `dateien[*].orte`,
`dateien[*].material_wunsch`, `dateien[*].z_frei_anzahl`, Akteure mit `hoehe_m`, `boden_z`, `unterkante_z`, `pivot`.

## Cache und Laufzeiten (2 m, 4789 × 3529, ohne SciPy)

- Ordner: `$SEHENS_CACHE` oder `--cache`, Standard
  `/tmp/claude-0/-home-user-fbulut/a2c581ba-c24a-5bce-9c65-c37d036a756e/scratchpad/a13/cache/welt_2m_<Fingerabdruck>/`
  (Fingerabdruck aus Daten + Version; neue Daten → neuer Unterordner). Arrays werden per Memory-Map geladen.
- Füllen: `python -I antworten/skripte/sehens_lib/gelaende.py --biome --kruemmung` (einmalig ~3,5 min).
- Erstberechnung: Abfluss ~23 s, je Distanz ~7–14 s, TPI ~4 s, Krümmung ~11 s je σ, Biomabstand 1–18 s.
  Aus dem Cache: ~0,3–0,6 s je Raster. Selbsttest mit Cache ~20 s (davon ~12 s Wegabstand mit Testpfad).
- Speicher: ~70 MB je float32-Raster; die 1-m-Welt ist 4× größer.

## Selbsttest

`python -I antworten/skripte/sehens_lib/selbsttest.py [--biom bergwald] [--aus <Ordner>]` – schreibt nur nach
`--aus` (Standard Scratchpad `a13/`, nie ins Repo). Schritt 9 prüft die Pfade (Testpfad rastern, Abstände, Prüfer, Rücksetzen).
Schritt 10 prüft Phase 2: Inventar-/Asset-Prüfung, Quaternionen, Stempel mit allen Werkzeugen (Rand 0, 1-m-Datei),
einen Ort aus einem Rezept zweimal (byteidentisch), orte.json + Ebene, Vorschau, Prüfer 0 FEHLER und absichtlich kaputte
Fälle (Uhrzeigersinn, fehlendes Niagara, Budget ≠ Ebene, falsche Anzahl, unbekanntes Netz). Laufzeit ~30 s mit Cache.

## Bekannte Grenzen

- Biomgrenzen sind Rechtecke; `biom_abstand` misst zum Rechteckrand – Boden/Form selbst prüfen.
- Bäume nur als 4-m-Näherung (`baeume_4m`, `baumhoehe_4m`); Kronen ohne Stammraum (unter Kronen keine Durchsicht).
- Abfluss auf dem Höhenraster (Wasserflächen sind Gelände = Seegrund, gefüllt); Bäche als Vektoren separat (`bach_enden`).
- `erreichbarkeit` rechnet auf 4 m gemittelten Höhen (kleine Stufen < 4 m verschwinden).
- §8: Die Kamera schaut immer leicht abwärts (`ZZ + 300` ≤ Kamerahöhe); sehr hoch liegende Ziele hebt die Regel an
  (Prüfer-HINWEIS).
- Phase 2: Pivot und Front-Achse sind nur für die 451 Netze in `netze_masse.json` bekannt; sonst gilt „Pivot unten Mitte“
  (`pivot: angenommen_unten_mitte` im Akteur). Welche Seite einer Klippenschale die Schauseite ist, weiß nur das Editorbild
  (`front_achse` in den Regeln). Auf 2-m-Daten sind Kanten (Stempel, Lippen) 2 Zellen breit; der 1-m-Lauf lokal schärft sie.
