# Verteilung Biomgruppe 6: Sumpf (Velen / Crookback Bog)

**Auftrag 11, Teil B6.** Biom `sumpf`, Foliage-Präfix `FT_EL_SU_`, Ordner `/Game/Eldarien/Welt/Foliage/Sumpf`. Stand 2026-10-10
(Fortsetzung nach API-Abbruch; Regeln und Planer-Entwurf des Vorgängers geprüft, vervollständigt und rauchgetestet).
Lieferung: dieser Bericht, `skripte/sumpf_regeln.json` (Korrektur Runde 1: 17 Planer-Klassen, 74 Netze, dazu `mittelschicht_overrides`,
`felsgruppen_overrides` und `spuren_overrides` mit 67 Netzen; alle gegen `netze.csv` geprüft, 0 fehlend), `skripte/sumpf_plan.py` (Planer
nach FORMAT §3/§5 und Konventionen §1–§6). **Alles UNGETESTET MIT ECHTDATEN** – in der Cloud nur mit synthetischen Rastern rauchgetestet
(Runde 0: H5, §4; Runde 1: H5, C6, H4, Abschnitt K5). Web-Quellen waren nur als Suchmaschinen-Auszüge lesbar (6 Läufe
WebSearch, Markierung **[Suchauszug]**); Zahlen ohne Beleg sind **Richtwerte** aus den Bildern.

Betroffene Felder: **H5** (sumpf 78 %, dschungel 12 %, aue 8 %; Laub 26, Schlamm 21, Algen 14, Gras 13, Kraut 12 %; Höhe 0–93 m,
nur 3 % steil, **kartiertes Wasser 0,4 %**), **I5** (sumpf 11 % als Zunge am Westrand des Bergwalds), **H4** (sumpf 8 % in der
Senke am Südrand des Elfenwalds). Der Planer läuft nur dort, wo `eigner.r8` + `welt.json` Biom `sumpf` liefern oder die Nassmaske
(Lagen Schlamm/Algen/Moos/Lehm/Kraut, geglättet σ 6 m, Schwelle 0,35) bzw. Wassernähe ≤ 3 m greift; außerhalb des Sumpfbioms wirken
nur die Wasserzonen-Klassen mit halber Stärke, Hinterland-Klassen mit dem Biomfaktor (aue 0,35, dschungel 0,3, elfenwald 0,25,
bergwald 0,15, Rest 0). **Überholt durch Korrektur Runde 1 (nächster Abschnitt):** genau diese biomübergreifende Nassmaske war die
Ursache der Fremdbiom-Instanzen. Jetzt gelten nur Sumpf-Zellen plus 30-m-Saum, Kennzahl 0 ist aue, bei < 2 % Sumpf im Fenster wird ein
leerer plan.json geschrieben, und die generischen Mittelschicht-Klassen liefert Teil D über `mittelschicht_overrides`.

---

## Korrektur Runde 1 (10.10.2026): gilt vor allen folgenden Abschnitten

Grundlage: `auftraege/verteilung-korrektur-runde1.md` (lokaler Echtdaten-Test 10.10. 15:30) und `antworten/verteilung-KONVENTIONEN.md`
(verbindlich, inkl. §6 Zusatzklassen-Schema). Geändert wurden nur `skripte/sumpf_plan.py` (jetzt 1 357 Zeilen), `skripte/sumpf_regeln.json`
(17 Planer-Klassen, 74 Netze; dazu 67 Netze in den drei Override-Blöcken, alle in `netze.csv`) und dieser Bericht. Wo §2–§4 und §6
etwas anderes sagen, gilt dieser Abschnitt.

### K1. Echtdaten-Befund und Ursache der Fremdbiom-Instanzen

**Befund (alte Fassung, lokal, `plan.json["instanzen"]`):** A5 (kueste 75 / bergwald 14 / aue 11 %) **75**, G4 (elfenwald 76 / heide 22 %)
**549**, E1 (gletscher 100 %) **140**, C6 (lava 99 %) **995**. In keinem der vier Felder gibt es Sumpf (`biome_je_feld.json`: Sumpf nur in
H5 78 %, I5 11 %, H4 8 %). Jede dieser Instanzen war also falsch.

**Ursache (im Code der alten Fassung nachvollzogen und synthetisch reproduziert).** Die Ebene war nicht an das Biom gebunden, sondern an
eine biomübergreifende **Nassmaske**:

1. `sumpfig = biom_sumpf | nass`. `nass` entstand **in jedem Biom** aus den Lagen Schlamm ×1, Algen ×1, **Moos ×0,5**, Lehm ×0,4 und
   Kraut ×0,2 (geglättet mit σ 6 m, Schwelle 0,35) oder aus „≤ 3 m vom Wasser“.
2. Die Regel „Nassflächen aus Schlamm/Algen ohne offenes Wasser in 18 m = Bultenzone“ (eingeführt für H5, das nur 0,4 % kartiertes
   Wasser hat) griff überall dort, wo `nass` griff. Moospolster auf Lava (C6: Moos 17 %) oder Moos/Kraut im Elfenwald wurden so zur
   Sumpf-Bultenzone.
3. Wasser- und Bult-Klassen bekamen außerhalb des Sumpfs den Faktor `max(biom_faktor, 0,5)`. Damit wurden **lava/gletscher
   (biom_faktor 0) auf 0,5 angehoben**. Hinterland-Klassen liefen zusätzlich mit aue 0,35, dschungel 0,3, elfenwald 0,25 und bergwald 0,15.
4. Kennzahl 0 (Weltgelände) wurde auf `felder[Feld].biom_fallback` gelegt (H5 → sumpf, sonst aue mit 0,35) statt immer auf `aue`.

Zuordnung zu den Echtdaten-Feldern. Sie ist aus den Lagen- und Wasseranteilen in `biome_je_feld.json` abgeleitet; die Zahlen je Klasse
lagen lokal nicht vor:

| Feld | Auslöser | Was gesetzt wurde |
|---|---|---|
| C6 (lava 99 %, Moos 17 %, Wasser 0 %) | 1 + 2 + 3: Moos-Lage → nass → „Bultenzone ohne Wasser“, Faktor 0,5 statt 0 | Seggenbulten, Moospolster, Schachtelhalm, Weidengebüsch, Pestwurz, Stümpfe |
| G4 (elfenwald, Wasser 5 %, Moos 6 %) | 1 + 3: Wasserrand ≤ 3 m und Moos → Wasser-/Ufer-/Bult-Klassen mit 0,5, Hinterland mit 0,25 | Schilf/Binsen/Seerosen an Elfenwald-Seen, Bulten, Laub/Zweige |
| E1 (gletscher, Wasser 0,9 %, keine Nass-Lagen) | 1 + 3: nur „≤ 3 m vom Wasser“ | Schilf, Binsen und Seerosen an Gletscherseen und -bächen |
| A5 (kueste/bergwald/aue, Wasser 0,6 %) | 1 + 3 + 4: Wasserrand, Kennzahl 0 → aue 0,35 | Uferklassen an Bächen |

**Synthetischer Nachweis.** Die alte Fassung lief auf denselben synthetischen Rastern wie der neue Rauchtest (K5). In **C6** (lava 96,5 %
+ bergwald 3,5 %, Moos-Flecken 16,6 %, zwei Tümpel 1 %) setzte sie **5 063 Instanzen, alle auf Lava**. Davon waren 4 644 Landklassen
(segge_bult 1 898, moos_polster 1 589, schachtelhalm 382, bult_strauch 180, pestwurz 155 …) aus 97 624 m² „Bultenzone ohne Wasser“, die
allein aus der Moos-Lage kam. Die übrigen 419 waren Wasserkante (schilf_wasser 224, seerose 82, binse 61). Im Mischfeld **H4** lagen 2 101 von
12 337 Instanzen in Fremdbiom-Zellen, **537 davon mehr als 30 m** von der Sumpfgrenze entfernt (bis 72 m). Im Hauptfeld H5 waren es 115
jenseits von 30 m. Die neue Fassung setzt in C6 **0** Instanzen (leerer plan.json). In H4 liegen alle 1 319 Fremdzellen-Instanzen im Saum
(höchstens 29,5 m).

### K2. Änderungen im Planer (`sumpf_plan.py`)

| Punkt | Vorher | Jetzt (Konventionen) |
|---|---|---|
| Biom je Zelle (§1) | Kennzahl 0 → `felder[].biom_fallback` (H5: sumpf), sonst aue | Kennzahl 0 → **aue**, Rezept mit „vulkan“/„lava“ → lava, unbekannte Kennzahl → aue (mit Hinweis). Nur ohne `eigner.r8`/`welt.json`: dominantes Feldbiom aus `daten/biome_je_feld.json` (danach `felder[].biom_fallback`, sonst aue), mit Hinweis im Log |
| Zuständigkeit (§1) | `biom_faktor` je Biom + Nassmaske in jedem Biom | `biome_eigen = [sumpf]`; Dichtefaktor `zust` = 1 in Sumpf-Zellen, im **30-m-Saum** linear 1 → 0 (Jump-Flooding-Distanztransformation, NumPy), sonst 0 und gesperrt. Gilt für **alle** Klassen, auch Wasserkante und Wasserlinsen-Flecken; Gruppenmitglieder nur auf Zellen mit Dichte > 0. `biom_faktor` ist aus den Regeln entfernt |
| Nassmaske / Bultenzone | in jedem Biom | `nass &= zust > 0`: die Bult-Erweiterung „Schlamm/Algen ohne Wasser in 18 m“ gilt nur in Sumpf-Zellen und im Saum. Gesperrte fremde Nassflächen werden als `zonen_m2.nass_fremdbiom_gesperrt` gezählt (H4 synthetisch 8 374 m²) |
| Fremdes Feld (§1) | Plan mit Instanzen | Eigenanteil im Fenster < 2 % → **leerer plan.json** (`instanzen 0`, `dateien {}`, alle Pflichtschlüssel, alte f32 gelöscht), eine Logzeile, Exit 0 |
| plan.json (§2) | `statistik.biome_anteil` | neu: `biome_fenster`, `zellen_zustaendig` (Feldzellen mit `zust > 0`), `biome_eigen`, `kollision_anzahl`, immer `entfernen` (Standard leer; ein gesetzter Filter wird nur bei Sumpf-Anteil im Feld ≥ 85 % ausgegeben, weil er feldweit wirkt); `statistik.zustaendigkeit` (Quelle, Anteile, Zellen eigen/Saum, Instanzen im Saum), `statistik.budget`, `overrides_geliefert` |
| Budget (§3) | Kollision und Ziel proportional, ohne harte Prüfung | Ziel 48 000, **hart 60 000 / 3 000 Kollision**. Erst Kollisionsklassen proportional per Hash, dann das Ziel von der niedrigsten Priorität aufwärts (Klassen ohne Kollision zuerst, ≤ 60 % je Klasse und Durchgang), danach **exakte Kappung** (Priorität, dann Hash). Jede Ausdünnung als `WARNUNG` im Log und in `hinweise`; bei Kleinzeug zusätzlich der Hinweis „an Landschafts-Gras abgeben“ |
| Ausgabe (§5) | Umlaute, „→“, „×“ in `print()` | `ascii_text()` für jede Konsolenzeile (ae/oe/ue/ss, `->`, `x`, Par.), Rest `?`; `plan.json` bleibt UTF-8 |
| Fehler (§5) | `SystemExit` je Feld abgefangen, Exit 1; `netze.csv` optional | fehlende `hoehe.f32`, Regeldatei oder `daten/netze.csv` (auch nicht neben dem Skript bzw. in `vorlagen/daten/`), ungültiges Feld → `FEHLER: …`, **Exit 2**; optionale Dateien → Hinweis, weiter |
| Overrides-Prüfung | nur fels/spuren | alle `/Game/…`-Pfade in `mittelschicht_`, `felsgruppen_` und `spuren_overrides` gegen `netze.csv` (Warnung) |

### K3. Neue Schicht-Definition (§4)

Der Planer setzt nur noch **Boden, Sumpf-Sonderformen, Bäume und Wasserkante**. Die Sonderformen tragen im Regel-JSON `"sonderform": true`.

| Schicht | Klassen | Inhalt / Regel |
|---|---|---|
| 0 boden | `laub_nass`, `moos_polster`, `schlamm_stein` | Laub auf Schlamm, Moospolster (MossClump/CustomMoss ≤ 0,16 m), Schlammsteine am Spiegel (≤ 0,12 m) |
| 1 mittel (nur Sonderformen) | `schilf_land` | Rohrkolben-Landteil am Spiegel (±0,2 m) und Ufer, Gruppen 4–12 |
| | `segge_bult` | Seggenbulten (ToadRush/KikuyuGrass 0,3–0,55 m Horste, Maßstab 0,9–1,5); grass_bush_01/03 entfernt, weil sie Netze der generischen Klasse `grasbueschel` sind |
| | `schachtelhalm` | Röhricht-Saum (Equisetum) am Ufer 0–3 m, Bulten ×0,3 |
| | `wurzel` | Wurzelteller an Bäumen. Bleibt hier, weil `mittelschicht_regeln.json` (`zusatzklassen_eigen`) Wurzeln im Sumpf ausdrücklich der Sonderform überlässt |
| 2 baum | `totbaum_wasser`, `weide`, `erle_ersatz`, `totbaum_land` | **tote Bäume im Flachwasser** (0–0,5 m, Neigung 2–9°), Weiden, Erlen-Ersatz, Totbäume an Land. `mittelschicht` setzt `totbaum` im Sumpf nicht |
| 5 wasserkante (nur Sonderformen) | `schilf_wasser`, `binse_wasser` | **Schilf-/Rohrkolbengürtel nach Wassertiefe** (Rohrkolben 0–0,3 m, Profil voll bis 0,15 m; Binsen 0–0,15 m) |
| | `seerose`, Wasserlinsen-Flecken | Seerosen 0,3–1,5 m auf dem Spiegel; Wasserlinsen als Punktliste `extras.wasserlinsen_flecken` |
| | `seggen_spiegel`, `moos_ufer`, `treibholz_wasser` | Seggen und Moos am Spiegel, Treibholz **im** Flachwasser 0–0,35 m (die Mittelschicht setzt nichts auf Wasser) |

**Verschoben (nichts geht verloren):**

| Bisherige Klasse (Schicht) | Ziel |
|---|---|
| `bult_strauch` (1) | `mittelschicht_overrides.palette.strauch` (grey_willow 01–04 Gewicht 3, Elderberry 01–04 Gewicht 1) + Zusatzklasse `weidengebuesch_saum` (1–18 m vom Wasser, 30/ha) |
| `jungweide` (2, ohne Kollision) | `palette.jungbaum` (Hornbeam Forest_10/Sapling_01/03, Poplar_plant A/B/C) |
| `farn_bult` (1) | `palette.farn` (EagleFern M_01/S_01/S_02/S_04 + Fern 01/03/05 + SilverLadyFern 01/02), Faktor 1,3 |
| `pestwurz` (1) | `palette.hochstaude` (petasites Gewicht 3, Brennnessel, Shaggy Soldier), Faktor 1,2 + Zusatzklasse `pestwurz_ufer` (0–3 m vom Wasser, 300/ha) |
| `totholz_gross`, `totholz_klein` (1) | `palette.totholz_liegend` (LargeFallenTree 01/02, MossyTree_01, dead_log_02, OldFallenTree_01, FallenTreeAssembly_01, trunk 01/02), Faktor 2,0 |
| `stumpf` (1) | `palette.totholz_stumpf` (5 Netze), Faktor 1,8 |
| `zweig` (0) + OldTreeBranch_02/03 aus `totholz_gross` | `palette.totholz_ast` (12 Netze), Faktor 2,5 |
| `pilz` (0) | `faktor.pilz` 0,8, `parameter.pilz.an_totholz` 4,0 |
| Moosblöcke (`felsgruppen_overrides.netze_moosblock`, `moosblock_je_m2_bult`) | `felsgruppen_overrides.zusatzklassen.moosblock_bult` (§6) |
| Steg/Knüppeldamm/Pfähle/Boot (eigene Strukturen) | `spuren_overrides` mit `palette`/`faktor`/`verbote`/`parameter`/`zusatzklassen` |

Netze der verbleibenden Sumpf-Klassen fehlen in den Mittelschicht-Paletten, damit kein Netz doppelt gesetzt wird. Treibholz-Netze
dead_log_01/03/04, OldFallenTree_02, OldTreeBranch_06 und beach_driftwood stehen nicht in `totholz_liegend`, grey_willow_04 nur noch in
`strauch` (Prüfung: 0 gemeinsame Pfade zwischen Planer-Klassen und Mittelschicht-Overrides). Die Faktoren entsprechen grob der alten
Sumpf-Dichte in ihren Zonen geteilt durch die Mittelschicht-Dichte (Mittel aus offen und beschattet), begrenzt auf 0,6–3. Dazu kommen
`grasbueschel` 0,6 (die Seggenbulten übernehmen die Rolle) sowie `beere`, `totbaum` und `wurzel` = 0. Das sind Richtwerte: nach dem ersten
gemeinsamen Setzen in H5 gegen TEICH1 nachstellen.

### K4. Override-Schema (in `sumpf_regeln.json`)

```
"mittelschicht_overrides": {                      # Leser: mittelschicht_plan.py (Teil D)
  "gilt_fuer": ["sumpf"],
  "palette":   {"strauch": [8], "jungbaum": [6], "farn": [9], "hochstaude": [7],
                "totholz_liegend": [8], "totholz_stumpf": [5], "totholz_ast": [12]},
  "faktor":    {"strauch": 1.0, "jungbaum": 1.0, "farn": 1.3, "hochstaude": 1.2, "totholz_liegend": 2.0, "totholz_stumpf": 1.8,
                "totholz_ast": 2.5, "grasbueschel": 0.6, "pilz": 0.8, "beere": 0.0, "totbaum": 0.0, "wurzel": 0.0},
  "parameter": {"strauch": {"netze_gewicht": {...}, "feuchte": [0.6, 2.0]}, "hochstaude": {"netze_gewicht": {...}},
                "pilz": {"an_totholz": 4.0}},
  "zusatzklassen": {                              # Mindestschema §6, nur Sumpf-Zellen + 30-m-Saum
    "pestwurz_ufer":       {"palette": [3], "rolle": "hochstaude", "dichte_je_ha": 300, "wasser_abstand_m": [0, 3],
                            "hang_grad": [0, 28], "gruppe": {"groesse": [3, 9], "radius_m": 2.0}, "kollision": false, ...},
    "weidengebuesch_saum": {"palette": [3], "rolle": "strauch", "dichte_je_ha": 30, "wasser_abstand_m": [1, 18], ...}},
  "herkunft": {...}}
"felsgruppen_overrides": {                         # Leser: felsgruppen_plan.py (Teil C)
  "palette": {"biom": {"sumpf": "moos"}}, "faktor": {"biom": {"sumpf": 0.25}, "kiesel": {"sumpf": 0.0}},
  "klassen_erlaubt": ["kuppe", "prallhang"], "eingraben_anteil": [0.4, 0.5],
  "zusatzklassen": {"moosblock_bult": {"palette": [MossyForestBoulder_01/03/06, MossyRocks_01, MossyEmbankment_02],
      "rolle": "fels_block", "dichte_je_ha": 4.0, "hang_grad": [0, 18], "wasser_abstand_m": [3, 18], "kruemmung": "konvex",
      "massstab": [0.8, 1.3], "eingraben_anteil": [0.4, 0.5], "gruppe": {"groesse": [1, 3], "radius_m": 5.0},
      "kollision": true, "sichtweite": [0, 0], "akteur": false}}}
"spuren_overrides": {                              # Leser: spuren_plan.py (Teil D)
  "palette": {"zaun_pfahl": [...], "steg_pfosten": [...], "steg_planke": [...]},
  "faktor":  {"sumpf": {"steg": 2.0, "zaun_weg": 0.4, "wegkreuz": 0.6, "graeber": 0.5, "rauch": 0.6, "holzschlag": 0.3,
                        "mauer": 0, "feldstreifen": 0, "obstgarten": 0, "karren": 0, "steinmann": 0, "koehler": 0}},
  "verbote": {"sumpf": ["karren", "mauer", "feldstreifen", "obstgarten", "steinmann"]},
  "parameter": {"steg": {"see_min_m2": 1200, "see_min_breite_m": 10, "deck_ueber_wasser_m": 0.45, "laenge_segmente": [2, 5], ...}},
  "zusatzklassen": {"knueppeldamm": {"palette": [SM_half_log, dead_log_04], "rolle": "spur_weg", "auf_weg": true, "nur_nass": true,
                                     "schritt_m": 0.45, "breite_m": 2.6, "yaw": "quer_zum_weg", ...},
                    "pfaehle": {"palette": [wooden_pales_1/2], "dichte_je_ha": 70, "wasser_abstand_m": [0.3, 3],
                                "gruppe": {"groesse": [2, 5], "radius_m": 3.0}, "neigung_grad": [3, 14], ...},
                    "boot": {"palette": [], "aktiv": false, ...}},     # kein Bootsnetz im Inventar
  "blickziele": {...}}
```

**Gegenprobe mit den aktuellen Lesern** (Module aus `skripte/` importiert, Inventar `vorlagen/daten/netze.csv`):
- `mittelschicht_plan.py` (`lade_overrides` + `effektive_regeln`, Feld H5): Block gelesen (palette, faktor, zusatzklassen, parameter),
  0 unbekannte Schlüssel, 0 verworfene Pfade. Im Sumpf kommen hochstaude, farn, strauch, jungbaum, grasbueschel, totholz_* und pilz mit
  Quelle `sumpf`; `pestwurz_ufer` (0,03/m², Wasserabstand 0–3 m) und `weidengebuesch_saum` (0,003/m², 1–18 m) sind als Zusatzklassen
  aktiv. `kletter` bleibt bei der Mittelschicht.
- `felsgruppen_plan.py` (`lade_overrides`): gelesen `palette.biom`, `faktor.biom`, `faktor.kiesel`, `klassen_erlaubt`, `eingraben_anteil`,
  `zusatzklassen.moosblock_bult` (13 Schlüssel gelesen, 0 ignoriert), Biomfaktor 0,25, Klassen grat/band/wand/fuss/blockstrom aus,
  Kiesel 0.
- `spuren_plan.py` liest noch keine `spuren_overrides` (Teil D, Nachrüstung läuft). Die Schlüssel `auf_weg`, `nur_nass`, `schritt_m`,
  `breite_m`, `yaw`, `je_km_ufer` und `neigung_grad` tragen die Sumpf-Logik über das §6-Mindestschema hinaus. Ein Leser ohne Unterstützung
  dafür meldet sie als unbekannt.

### K5. Rauchtest Runde 1 (synthetisch, Cloud: Python 3.13, NumPy 2.5, Pillow, kein numba)

Raster neu erzeugt (volle Größe 7057 × 9577 als memmap, nur drei Fenster beschrieben, nach dem Test gelöscht). **H5**: Sumpf-Kachel
`sumpf_velen` mit fünf Teichen, Bach, Weg, Ort, Schlamm-Nassfläche ohne Wasser, Dschungel-Osten, Weltgelände-Nordstreifen (Kennzahl 0),
150 Bestandsbäume, 800 Ufer-Kiesel. **C6** (Fremdfeld): `Vulkanregion_Sued` 96,5 % + bergwald-Randstreifen, Moos-Flecken 16,6 %,
Schlamm/Algen um zwei Tümpel. **H4** (Mischfeld): elfenwald mit Sumpfsenke (6,6 % des Feldes) und Teich, Schlamm/Algen reichen ~60 m über
die Sumpfgrenze hinaus, Weltgelände im Osten.

| Prüfung | Ergebnis |
|---|---|
| H5 (eigene Zellen) | **26 512** Instanzen (602 Kollision), 74 Netze, 205 Wasserlinsen-Flecken, 7 s. Schichten: boden 12 036 / mittel 7 159 / baum 602 / wasserkante 6 715. `biome_fenster` sumpf 0,777 / dschungel 0,152 / aue 0,070. `zellen_zustaendig` 922 300 (davon Saum 43 388). 469 Instanzen im Saum. Bultenzone ohne Wasser 60 973 m² (nur Sumpf) |
| C6 (Fremdfeld mit Schlamm-/Moos-Lagen) | **leerer plan.json** (`instanzen 0`, keine f32, `biome_fenster` lava 0,965 / bergwald 0,035), eine Logzeile, Exit 0. Alte Fassung: 5 063 |
| H4 (Mischfeld, Saum) | **8 503** Instanzen (145 Kollision), 70 Netze. `zellen_zustaendig` 111 878 (Saum 44 645). Instanzen auf Fremdzellen: 1 319, Abstand zur Sumpfgrenze 0–10 m: 844, 10–20 m: 338, 20–30 m: 137, **> 30 m: 0** (unabhängig per Brute-Force-Abstand, max 29,5 m). 8 374 m² fremde Nassfläche gesperrt. Prüfbild: oranger Saumring, außerhalb keine Instanzen. Alte Fassung: 12 337, davon 537 jenseits von 30 m |
| 30-m-Saum H5 | 469 Fremdzellen-Instanzen: 262 / 166 / 41 in 0–10 / 10–20 / 20–30 m, **> 30 m: 0** |
| Pflichtschlüssel (§2) | `instanzen`, `dateien` (mit `ebene`), `entfernen`, `ft_ordner`, `ft_praefix`, `biome_fenster`, `zellen_zustaendig`, `biome_eigen`, `kollision_anzahl` in allen drei Plänen; Σ `anzahl` = `instanzen` = f32-Zeilen; `kollision_anzahl` = Summe der Dateien mit `kollision` |
| Format | 10 float32 je Instanz, 0 NaN, Quaternionen normiert (Fehler ≤ 6·10⁻⁸), 0 Instanzen außerhalb des Feldes, auf Weg, auf Ort, 0 Landklassen auf `karte_wasser` |
| Determinismus | zweiter Lauf: alle 144 f32 byte-identisch (MD5), `plan.json` bis auf `stand`/`laufzeit_s` identisch |
| Budget | `--faktor 3` (H5): 79 009 → Ziel 48 000. Runde 1 dünnt Kleinzeug und Bulten ×0,437, dann exakte Kappung 48 104 → **48 000**; Kollision 1 659. `WARNUNG` im Log, Kleinzeug-Hinweis in `hinweise`. Zwangstest mit Deckel 20 000 / Kollision 300: 602 → 288 Kollision, 26 512 → 19 989. Direkter Funktionstest: Kollision 3 043 → exakt 2 999, Instanzen 48 146 → exakt 48 000 |
| ASCII (§5) | 0 Nicht-ASCII-Zeichen in allen Konsolenausgaben (zwei Volläufe, Budget- und Fehlerläufe); die alte Fassung hatte 21 Zeilen mit Umlauten/Sonderzeichen |
| Fehlerpfade (§5) | Feld K9, fehlende `hoehe.f32`, fehlende Regeldatei, fehlende `netze.csv` (Skript isoliert kopiert) → `FEHLER: …`, **Exit 2**. Ohne `eigner.r8`: dominantes Feldbiom aus `daten/biome_je_feld.json` mit Hinweis (H5 → sumpf, 29 180 Instanzen; C6 → lava, H4 → elfenwald: jeweils Leerplan) |
| `py_compile` / pyflakes | sauber (nur „numba imported but unused“, gewollt) |

Die Zahlen sind nicht mit §4 vergleichbar: Kennzahl 0 ist jetzt aue statt sumpf, und die generischen Klassen fehlen. Vorher setzte H5
41 008 Instanzen auf denselben Rastern. Die Differenz von 14 496 besteht vor allem aus Zweigen, Farnen, Pilzen, Stümpfen, Totholz,
Weidengebüsch, Pestwurz und Jungweiden. Diese Klassen setzt jetzt die Mittelschicht.

### K6. Echtdaten-Referenz und Erwartung nach der Korrektur

| Feld | Echtlauf 10.10. (alt) | Erwartung jetzt | Begründung |
|---|---|---|---|
| A5 (kueste/bergwald/aue) | 75 | **leerer plan.json** | Sumpf-Anteil im Fenster 0 % |
| G4 (elfenwald/heide) | 549 | **leerer plan.json** | 0 % Sumpf. Das Fenster reicht 64 m nach H4/H5 hinein; selbst wenn dort Sumpf-Kacheln liegen, bleibt der Anteil deutlich unter 2 % |
| E1 (gletscher 100 %) | 140 | **leerer plan.json** | 0 % Sumpf |
| C6 (lava 99 %) | 995 | **leerer plan.json** | 0 % Sumpf; Moos-Lage wirkt nicht mehr |
| H5 (sumpf 78 %) | – | 18 000–32 000 (Kollision 400–900) | ohne generische Klassen; Kennzahl-0-Zellen sind jetzt aue und bekommen nur Saum |
| I5 (sumpf 11 %) | – | 2 000–6 000 | nur Sumpfzunge + Saum |
| H4 (sumpf 8 %) | – | 1 500–5 000 | nur Senke + Saum; Elfenwald-Nassflächen bleiben frei |

Beim nächsten Echtlauf bitte `biome_fenster`, `zellen_zustaendig` und `statistik.zustaendigkeit` von H5/I5/H4 zurückmelden. Wichtig:
Liegen die H5-Teiche in `eigner.r8` auf **Kennzahl 0** (Weltgelände), sind sie jetzt aue. Dann bekommen nur Wasserzellen ≤ 30 m vom
Sumpfufer einen Gürtel (Saumfaktor < 1), und Seerosen/Schilf werden zur Teichmitte hin dünner. Abhilfe wäre ein Eintrag für die
Teich-Kennzahl in `welt.json` oder eine Ausnahme „Wasser in Sumpf-Kachel-Nähe“ in Runde 2.

### K7. Offene Punkte nach Runde 1

1. `spuren_plan.py` liest `spuren_overrides` noch nicht. Knüppeldamm, Pfähle und Sumpf-Stege fehlen, bis Teil D sie umsetzt. Die
   Sumpf-Sonderschlüssel stehen in K4.
2. Die Override-Faktoren sind Richtwerte aus Dichteverhältnissen, ohne Licht-/Feuchte-Faktoren der Mittelschicht. Nach dem ersten
   gemeinsamen Setzen (felsgruppen → sumpf → mittelschicht → spuren) in H5 mit den Kameras aus §4 nachstellen.
3. Kennzahl-0-Teiche (siehe K6).
4. `verteilung-STATUS.md` wurde nicht geändert (Koordinator): B6 kann auf „korrigiert (synthetisch H5 26 512, C6 Leerplan, H4 Saum)“
   gesetzt werden. Die Zeile „sumpf, heide_tundra, hochgebirge, lava ohne Block“ in `verteilung-leere-fuellen.md` 8.3 ist für sumpf überholt.

---

## 1. Witcher-Analyse: Velen und Crookback Bog

**Was die Quellen hergeben.** Crookback Bog ist laut Witcher-Wiki „a large peat bog in Velen“ im Süden der Region, zwischen Bald
Mountain und The Descent, am Nordrand an eine Bergflanke grenzend; Drowner und Water Hags sind die Standardgegner, „because the area
is mostly swamp“ **[Suchauszug: witcher-games.fandom.com/wiki/Crookback_Bog; thewitcher3.wiki.fextralife.com/Crookback+Bog]**. Das
Velen-Lore-Blatt sagt, die Region enthalte „forests, wetlands and cultivated woods, though the greatest part of it is covered in
swamps and bogs“ **[Suchauszug: witcher-games.fandom.com/wiki/Velen]**. Ein Spieler-Walkthrough beschreibt die Pfade durch das Moor
als schwer zu folgen, „with small wooden platforms crossing the marsh“ **[Suchauszug: thewitcherwalks.blogspot.com, Downwarren &
Crookback Bog]** – das sind die Knüppeldämme und Stege, die in Eldarien heute fehlen. Environment-Artist Kacper Niepokólczycki
(VICE-Interview) hat vor allem das „swampy and rural“ Velen gebaut und nennt polnische Dörfer und Umland als Vorlage **[Suchauszug:
vice.com „Designing the World of The Witcher 3“]**. Michał Janiszewski (80.lv) beschreibt SpeedTree als Kern der Foliage-Arbeit und
einen Vegetationsspezialisten, der „what kind of foliage grows where“ recherchierte und je Region eigene Asset-Bibliotheken und
Atlanten anlegte **[Suchauszug: 80.lv „World Building of Witcher 3“]**. Marcin Gollents GDC-2014-Talk „Landscape Creation and
Rendering in REDengine 3“ listet „on-the-fly distribution“ plus „offline vegetation generator“ für Vegetation und Debris, Slope-
based Texturing und Terrain-Shadow-Clipmaps **[Suchauszug: gdcvault.com/play/1020197; Folien media.gdcvault.com; Mitschnitt
archive.org/details/GDC2014Gollent]**; dass der Generator Wasseransammlung und Licht simuliert, ist in `verteilung-aue.md` §1 als
Sekundärbericht vermerkt. Zur Next-Gen-Fassung bestätigt GameGPU „higher grass density and more variety“ gegenüber dem Original
**[Suchauszug: en.gamegpu.com, Evolution der Grafik]**. Ein eigener Art-Breakdown des Bogs (GDC, Artstation) tauchte in keinem der
sechs Suchläufe auf; alle Dichten unten sind deshalb aus den Zielbildern und dem Ist-Bild TEICH1_H5 abgeleitet.

**Was den Crookback Bog optisch ausmacht (aus den Bildern und Beschreibungen, als Regel formuliert):**

1. **Offenes Wasser ist flach und verlandet.** Teiche und Rinnen haben keine scharfe Kante, sondern eine 1–3 m breite Zone aus
   Schilf im Wasser (Rohrkolben 10–50 cm tief), Binsen am Spiegel, Seerosen 0,3–1,5 m tief und Wasserlinsen-Decken in Buchten.
   Zonierung also **nach Wassertiefe**, nicht nach Abstand.
2. **Tote Bäume stehen im Wasser.** Der Velen-Akzent schlechthin: abgestorbene, entrindete Stämme 6–20 m, schief (2–9°), in Gruppen
   von 2–5, 8–25 m vom Ufer im Flachwasser; dazu liegende Stämme halb im Wasser, Wurzelteller am Rand. Ökologisch: Bäume sterben
   bei 0,7–1,3 m Dauerüberstau (USDA Forest Service, Lake Ocklawaha), Snag-Dichten überfluteter Wälder bis ~105/ha (ScienceDirect
   2025); wir setzen 25/ha im Flachwasser (Budget, Blickruhe).
3. **Bulten statt Wiese.** Das Land zwischen den Teichen ist kein Rasen, sondern Seggenbulten 0,4–0,8 m in Horsten, Moosteppiche,
   Schachtelhalm, Pestwurz, dazwischen Schlammflächen mit Steinen und Laub. Sichtbare Objekte in 0,3–1,5 m alle 2–4 m (Witcher-
   Richtwert aus Teil D: kein Blick ohne Objekt in 0,5–3 m innerhalb 10 m).
4. **Weidengebüsch und Erlen-Bruchwald als Rahmen.** Grau-/Ohrweiden 1,5–3 m in 1–3er-Gruppen bis 18 m vom Wasser, Weiden 10–20 m
   als Solitäre am Ufer, dahinter lichter Bruchwald (Erle fehlt im Inventar → Hainbuche/kleine Pappel), Totbäume auch an Land.
5. **Spuren von Leben sind hölzern und nass.** Stege auf Pfählen, Knüppeldämme über Nassflächen, verwitterte Pfähle (Reusen,
   Stegreste), Boote, Pfahlbau-Ruinen; keine Karren, keine Steinmauern (falsche Spur im Moor).
6. **Farbakzente:** Gelbgrün der Seggen und Wasserlinsen gegen Braun des Schlamms und Grau der Totbäume; Rot nur über Pilze und
   Beeren (Teil D). Nebel kommt aus `dunst-atmosphaere-hoehennebel.md`, nicht aus dieser Ebene.

**Ist-Zustand TEICH1_H5 (Bild vom 10.10.).** Der Teich hat eine harte Kante, der Schilfgürtel steht als gleichmäßiger Saum **auf dem
Land** (Houdini `FT_EL_WELT_Rohrkolben_*`), im Wasser ist nichts; die Fläche dahinter ist ein einheitliches Gelbgrün ohne Bulten,
Moos, Totholz oder Schlamm; die Weiden stehen einzeln im 15–20-m-Raster, kein Totbaum, kein Steg. Genau diese sechs Lücken
adressiert die Ebene.

## 2. Regelwerk (`sumpf_regeln.json`) – Zonierung und Schichten

> **Stand Runde 0.** Seit Korrektur Runde 1 gilt die Zonierung nur in Sumpf-Zellen + 30-m-Saum (auch die Bult-Erweiterung auf
> Nassflächen). Schicht 0 hat nur noch laub_nass/moos_polster/schlamm_stein, Schicht 1 nur schilf_land/segge_bult/schachtelhalm/wurzel;
> zweig, pilz, pestwurz, farn_bult, bult_strauch, totholz_gross/klein, stumpf und jungweide sind nach `mittelschicht_overrides` gewandert.
> Das Budget ist hart (K2). Siehe K2/K3.

**Zonen (je Zelle, aus `hoehe.f32`, `karte_wasser.r8`, Umrissen und Spiegeln).** Wasserfläche = `karte_wasser` ∪ Teich-/See-Umrisse.
Spiegel einer Wasserzelle = `spiegel_cm` aus `teiche/teiche.json` bzw. `wasser_welt.json[seen]`; fehlt er, Geländehöhe der nächsten
Wasserrand-Zelle (Jump-Flooding), innerhalb der Fläche mit σ 3 m geglättet. Wasserzellen, deren Grund > 5 cm über dem Spiegel liegt,
zählen für die Zonierung als Land, bleiben aber für Landklassen gesperrt. Wassertiefe = Spiegel − Grund; Höhe über Spiegel (Land) =
Grund − Spiegel des nächsten Ufers (bis 64 m).

| Zone | Bedingung | Inhalt |
|---|---|---|
| `flachwasser` | Wasser, Tiefe 0–0,5 m | Schilf (0–0,3 m, Profil voll bis 0,15, 25 % bei 0,3), Binsen (0–0,15), Totbäume (0–0,5), Treibholz (0–0,35), Seerosen (0,3–1,5), Wasserlinsen (0–0,7, ≤ 6 m vom Ufer) |
| `tiefwasser` | Wasser, > 0,5 m | nur Seerosen bis 1,5 m, sonst nichts |
| `spiegel` | Land, ≤ 2 m vom Wasser, ≤ 0,2 m über Spiegel | Seggen am Spiegel, Rohrkolben-Landteil, Moos, liegendes Totholz, Schlammsteine, Totbäume (½) |
| `ufer` | Land, ≤ 3 m, ≤ 0,8 m über Spiegel | Moosteppich, Seggenbulten, Schachtelhalm, Pestwurz, Weidengebüsch (½), Weiden (0,6) |
| `bult` | Land, 3–18 m, ≤ 2,5 m über Spiegel **oder** Nassfläche (Nassmaske) ohne Wasser in 18 m | Seggenbulten (0,45), Farninseln, Weidengebüsch, Stümpfe, Wurzelteller, Weiden, Totbäume an Land, Moosblöcke (Teil C) |
| `hinterland` | übriges Land ≤ 6 m über Spiegel (oder ohne Wasser in 64 m) | Laub, Zweige, Pilze, Erlen-Ersatz, Totbäume (0,7), Stümpfe (0,6), Farn (0,5) |

Die Bult-Erweiterung auf Nassflächen ohne offenes Wasser ist nötig, weil H5 laut `biome_je_feld.md` nur 0,4 % kartiertes Wasser
hat, aber 35 % Schlamm + Algen: ohne sie blieben die Schlammflächen reines Hinterland mit Laub und Zweigen.

**Faktoren.** Dichte je Klasse = Basis × Zonenfaktor × Lagenfaktor (`lage_*.r8`, Rest-Deckung mit `sonst`) × Hang (voll bis 10°,
0 ab 28°; Bäume ≤ 18–20°, Wasserklassen ≤ 35°) × Höhe über Spiegel (voll bis 1,5 m, 0 ab 6 m) × Biom/Nässe × `--faktor`. Gruppen:
Dichte ist Einzelinstanz-Dichte, Zentren = Dichte/Gruppenmittel, Mitglieder gleichverteilt in `radius_m`, jedes Mitglied erneut gegen
Sperrzellen und lokale Dichte geprüft. Zufall = Hash(absolute Rasterkoordinate, Seed 6106, Klassenkanal): deterministisch, nahtlos.
Abstände: 2,5 m Kleinzeug / 4 m Großes zum Weg, 5 m zum Ort, 0,9 m zu Bestandsstämmen (eigene Bäume 3–6 m), 1,2 m zu Ufer-/Witcher-
Instanzen, Mindestabstände über ein grobes Gitter (Weiden 7 m, Totbäume 4–6 m, große Stämme 6 m).

**Schicht `0 boden`** (Sichtweite 4 000–6 000 cm, kein Schatten, keine Kollision, Eingraben 1–4 cm, voll auf die Normale gekippt):
`laub_nass` DeadLeaves_01/12/13/14 0,035/m² (Laub ×1, Schlamm ×0,4), Gruppen 2–6 in 2,5 m; `zweig` DryBranches_01–05, branch_01_1/2,
WoodenSticksAndTwigs_01/02/04 0,03/m²; `pilz` mushroom_01/02 0,004/m², Gruppen 3–9, ×4 im 3-m-Ring um eigenes Totholz; `moos_polster`
MossClump_01/03/05, CustomMoss_01/02/03/05 0,08/m² Ufer, 0,048 Bult, Maßstab 1,2–2,2; `schlamm_stein` SmallStonesPack_01/03/06/07
0,03/m² nur Spiegel/Ufer, Eingraben 4 cm.

**Schicht `1 mittel`** (0,3–3 m): `schilf_land` Rohrkolben_Horst_1–6/Jung_1–3 0,18/m² am Spiegel (0,063 Ufer), Gruppen 4–12, kaum
gekippt; `segge_bult` ToadRush_00/02/010, KikuyuGrass_01/03/04, grass_bush_01/03 0,12/m² Ufer, 0,054 Bult, Gruppen 3–10 in 2,5 m,
Maßstab 0,9–1,5 (= 0,4–1,6 m Bulten); `schachtelhalm` rough_horsetail_01–03 0,035/m², Gruppen 5–16; `pestwurz` petasites_spurius_01–03
0,03/m² nur Uferband (Teil D streut sie feldweit als Hochstaude 0,012); `farn_bult` EagleFern_M_01/S_01/S_02/S_04 0,015/m² Bult, Gruppen
3–8; `bult_strauch` grey_willow_01–04 0,006/m², 1–3 je Gruppe in 3 m, Sichtweite 30 000; `totholz_gross` LargeFallenTree_01/02,
OldTreeBranch_02/03, MossyTree_01 0,0025/m², **Kollision**, Eingraben 22 cm, Yaw parallel zur Uferlinie ± 20°, Mindestabstand 6 m;
`totholz_klein` dead_log_01–04, OldFallenTree_01/02, FallenTreeAssembly_01 0,012/m², Eingraben 10 cm; `stumpf` RottenTreeStump_01/02,
BrokenStump_01, TreeStump_01, BirchTreeStump_01 0,0025/m², Eingraben 12 cm; `wurzel` MossyForestRoots_01–03 0,0015/m², ×3 im 4-m-Ring
um Bäume.

**Schicht `2 baum`** (Kollision, Sichtweite 0, Kippen ≤ 0,1): `weide` Big_Tree_willow_01/02 (kein Nanite, 30–38 k Dreiecke → Anzahl
klein) 0,0007/m² Bult, 1–3 je Gruppe in 9 m, Maßstab 0,75–1,15, Hang ≤ 18°, Mindestabstand 7 m; `totbaum_wasser` DeadTree_01/02,
EuropeanBeech_Dead_M_01 (Gewicht 3), Dead_Tree_qlEtl (2), Beech_Dead_XL_01, Graveyard Dead_Tree_01/03 (1) 0,0025/m² Flachwasser
0–0,5 m, Gruppen 2–5 in 7 m, Eingraben 40 cm, **Neigung 2–9° in Zufallsrichtung** (Lehnen im Schlamm), Mindestabstand 4 m;
`totbaum_land` 0,0005/m² Bult/Hinterland, Eingraben 30 cm, Neigung 0–5°; `erle_ersatz` Hornbeam_Forest_03/05/06/07 (Nanite),
Poplar_04/05_Small 0,0009/m², lichte Gruppen 2–6 in 8 m, Maßstab 0,7–1,1, 5 m Abstand zu Bestandsbäumen; `jungweide`
Hornbeam_Forest_10, Sapling_01/03, grey_willow_04 0,0015/m², ×2 im 10-m-Ring um Bäume, keine Kollision.

**Schicht `5 wasserkante`** (alles mit `z = Grund − Eingraben·Maßstab`, nur Seerosen `z = Spiegel + 1 cm`): `schilf_wasser`
Rohrkolben_Horst_1–6/Jung_1–2 0,3/m² bei Tiefe 0–0,15 m, 25 % bei 0,3 m, Gruppen 6–20 in 4 m, Eingraben 8 cm; `binse_wasser`
ToadRush_00/01/02/011/012 0,15/m² bei 0–0,15 m, Maßstab 1,0–1,8; `seerose` CityPark SM_WaterPlant01–04 (1,6–3,3 m flache Blattplatten,
21–98 Dreiecke, kein Nanite – Material im Editor prüfen) 0,025/m² bei 0,3–1,5 m, Gruppen 3–10, ≥ 1,5 m vom Ufer, Maßstab 0,6–1,1;
`seggen_spiegel` ToadRush_013–015, dead_grass_01–03 0,08/m² am Spiegel; `moos_ufer` MossPlane, moss_01/02 0,05/m²; `treibholz_wasser`
dead_log_01/03/04, beach_driftwood_01, OldTreeBranch_06, OldFallenTree_02 0,004/m² bei 0–0,35 m, Yaw uferparallel, Eingraben 8 cm,
60 % gekippt. **Wasserlinsen** gibt es nicht als Netz: der Planer schreibt eine Punktliste `plan.json["extras"]["wasserlinsen_flecken"]`
(x, y, z = Spiegel, Radius 2,5–6 m; 6-m-Raster, 45 % der Kandidaten, ≤ 400 je Feld) für Decal, Material-Maske oder Niagara.

**Budget.** Ziel 48 000, Deckel 60 000 je Feld, ≤ 3 000 mit Kollision (Kollisionsklassen proportional gedünnt); Ausdünnung von
hinten über die Prioritätsliste (Schlammsteine, Laub, Zweige zuerst; Totbäume im Wasser, Weiden, Erlen-Ersatz zuletzt), höchstens
60 % je Klasse und Durchgang, deterministisch per Hash.

### 2.1 Planer `sumpf_plan.py` (FORMAT §3/§5)

- **Aufruf:** `python -I scripts/sumpf/sumpf_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]`; nur
  NumPy (+ Pillow für `--bild`), numba wird erkannt, aber nicht benötigt (Cloud-Test ohne numba).
- **Lesen:** `hoehe.f32` als memmap, nur Fenster Feld + 64 m (J-Spalte bei NX = 9577 geklippt, Zeile 7 bei NY = 7057);
  `karte_wasser/weg/ort.r8`, `lage_*.r8`, `eigner.r8` + `welt.json` (Kennzahl 0 → dominantes Feldbiom aus `felder[].biom_fallback`,
  sonst aue), `teiche/teiche.json` + `wasser_welt.json[seen]` (Umrisse als `umriss|punkte|polygon` in cm Welt, Spiegel als
  `spiegel_cm|z_cm|hoehe_cm|spiegel|z|spiegel_m`), `bestand/`, `witcher/` (Feld + 8 Nachbarn), `ufer/foliage_<Feld>/`,
  `instanzen/instanzen.json` – alles außer `hoehe.f32` optional mit klarer Meldung und Eintrag in `plan.json["hinweise"]`;
  `daten/netze.csv` (sonst `vorlagen/daten/netze.csv` neben dem Repo) für die Pfadprüfung.
- **Rechnen:** Normale/Hang aus dem Gradienten; zwei Jump-Flooding-Läufe (Wasserrand → Spiegel, Ufer → Distanz/nächster Uferpunkt);
  Nassmaske; Zonen; je Klasse Dichtekarte → Bernoulli-Zug → Gruppenzentren → Mitglieder; Mindestabstand über ein grobes Gitter;
  Yaw `ufer` aus dem Gradienten des geglätteten Distanzfelds. Kein Python-Loop über Zellen; 7 s je Feld in der Cloud.
- **Schreiben:** `export/unreal/welt/sumpf/<Feld>/<Netz>.f32` (10 float32 LE; alte f32 vorher gelöscht) und `plan.json` mit
  `stand, feld, instanzen, dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene[, gruppen]}, ft_ordner,
  ft_praefix, ebenen, extras{wasserlinsen_flecken}, statistik{je_klasse, kollision, biome_anteil, zonen_m2, laufzeit_s, …}, hinweise,
  ungetestet`; `entfernen` nur, wenn in den Regeln gesetzt (Standard leer). `gruppen` listet Klassen, die dasselbe Netz mit anderem
  Eingraben nutzen (DeadTree, Rohrkolben, dead_log, ToadRush, grey_willow_04). `--bild` → `docs/pruefung/sumpf/<Feld>.png` (1 px = 1 m).

## 3. Overrides für Teil C/D und Abgrenzung

> **Stand Runde 0.** Override-Blöcke seit Korrektur Runde 1 im Schema {palette, faktor, zusatzklassen} (K4); Moosblöcke als
> `felsgruppen_overrides.zusatzklassen.moosblock_bult`. Neu ist `mittelschicht_overrides`. Die Zeile `FT_EL_MS_` der Tabelle unten ist
> überholt: die Mittelschicht ist jetzt der einzige Planer der generischen Klassen im Sumpf.

**`felsgruppen_overrides`** (an `felsgruppen_plan.py`): Biomfaktor 0,25, nur Klassen `kuppe` und `prallhang`, Palette `moos`,
Eingraben 40–50 %, kein Geröllsaum (Schlamm statt Kies); zusätzlich **Moosblöcke** 0,0004/m² auf Bulten aus MossyForestBoulder_01/03/06,
MossyRocks_01, MossyEmbankment_02 (alle im Inventar).

**`spuren_overrides`** (an `spuren_plan.py`): **Stege** schon ab 1 200 m² See und 10 m Breite (Sumpfteiche sind klein), Uferhang ≤ 6°,
Tiefe in 6 m ≤ 1,2 m, Deck 0,45 m über Spiegel, 2–5 Segmente, 2 Pfosten je Segment, max 4 je Feld, Pfähle wooden_pales_1/2_01, Planken
SM_PlankThin_4m_01a/SM_Plank_4m_01a; **Knüppeldamm** (neu): Wegzellen innerhalb der Nassmaske bekommen Halbstämme SM_half_log/dead_log_04
quer zum Weg alle 0,45 m, Breite 2,6 m, Jitter 8 cm, Eingraben 6 cm, ohne Kollision (Weg bleibt begehbar), ≤ 400 m je Feld;
**Pfähle** (neu): 6 je km Ufer in 2–5er-Gruppen (Radius 3 m) am Spiegel/Flachwasser ≤ 0,4 m, Neigung 3–14°, Eingraben 60 cm
(verwitterte Reusen-/Stegreste); **Boot**: 1–3 je Feld am Spiegel, aber kein Netz im Inventar (SM_BrokenWoodWagon ausdrücklich nicht –
Karren im Sumpf ist falsche Spur); **Blickziele** sumpf: Totbaum-Solitär (Beech_Dead_XL_01 × 1,3–1,6 im Flachwasser 0,2–0,5 m,
8–25 m vom Ufer des größten Teichs, 1 je Feld), Pfahlbau-Ruine (AncientRuins SM_Column_02 + Town SM_Beam_4m als Akteure auf einer
Uferkuppe > 1 m über Spiegel, ≤ 60 m vom Weg), Steg.

**Abgrenzung (ergänzen, nicht ersetzen):**

| Ebene | Verhältnis zur Sumpf-Ebene | `entfernen`? |
|---|---|---|
| `FT_EL_WIT_*` (Laub, Zweige, Farne, Unterwuchs feldweit) | Sumpf legt dieselben Rollen nur in den Nasszonen (≤ 18 m Wasser bzw. Nassmaske) dichter; WIT-Instanzen werden geladen und mit 1,2 m gesperrt | nein |
| `FT_EL_BST_*` (Bäume) | Kronendach wird nicht gebraucht (Sumpf ist offen); eigene Bäume halten 3–6 m Abstand zu Bestandsstämmen, Wurzelteller/Jungweiden suchen deren Nähe | nein |
| `FT_EL_UF_*` (Kiesel, Kopfsteine, Treibholz) | Sumpf setzt eigenes Treibholz nur **im** Flachwasser und Schlammsteine nur am Spiegel; UF-Instanzen 1,2 m gesperrt. Kiesel an Schlammufern sind inhaltlich falsch | **vorerst nein**; nach Sichtprüfung H5 `entfernen: "SM_SmallStonesPack_"` je Feld erwägen (`entfernen_hinweis` in den Regeln) |
| `FT_EL_WELT_Rohrkolben_*` (Houdini-Schilf, TEICH1 zeigt es als Landsaum) | eigener Gürtel steht tiefengestaffelt **im** Wasser (0–0,3 m) und dichter; Doppelung am Spiegel möglich | nein; bei sichtbarer Doppelung `entfernen: "SM_Rohrkolben_"` nur in H5 |
| `FT_EL_MS_*` (Teil D Mittelschicht: Strauch, Farn, Hochstaude, Totholz, Stumpf, Pilz feldweit, Sumpf-Zeile 0,008/0,002/0,006/0,012/0,0015/0,0006/0,003 je m²) | Sumpf-Klassen gleicher Art sind auf Uferband/Bulten begrenzt (Pestwurz nur 0–3 m, Adlerfarn nur Bulten, Weidengebüsch nur ≤ 18 m) und liegen im Hinterland unter 50 % der MS-Dichte; Teil D liefert die biomübergreifende Mittelschicht und die Spuren, diese Ebene den sumpfspezifischen Zusatz | nein |
| `GT_Schilf` (Landschafts-Gras) | bleibt, trägt die Fernwirkung | nein |
| Felsschalen `FT_EL_FS_*` | unberührt (Sumpf ist flach) | nein |

## 4. Testanleitung

> **Stand Runde 0.** Rauchtest und Erwartungswerte nach der Korrektur stehen in K5/K6; die Prüfkameras unten gelten weiter.

**Rauchtest Cloud (gelaufen am 10.10., Python 3.13, NumPy 2.5, ohne numba).** Synthetische Produktionswurzel im Scratchpad:
`hoehe.f32` in voller Größe 7057 × 9577 als memmap, nur das H5-Fenster (1136 × 1136 m) beschrieben – flache Senke 6 m mit Rauschen
0,3 m, Anstieg auf 40 m im Osten, Kuppe 4 m, **5 Teiche** (0,6–2,2 m tief, Paraboloid-Grund, flaches Uferband 0–0,4 m) als
`karte_wasser.r8` plus `teiche/teiche.json` mit 48-Punkt-Umrissen (nur 3 von 5 mit `spiegel_cm`, 2 über den Fallback), ein 4 m
breiter Bach ohne Umriss, Weg (Nord–Süd durch die Nasszone), Ort 60 × 80 m, `eigner.r8` (0 = Fallback sumpf, 3 = aue, 7 = dschungel)
+ `welt.json`, `lage_Schlamm/Algen/Moos/Laub/Gras/Kraut.r8`, `bestand/H5` (150 Hainbuchen), `ufer/foliage_H5` (800 Kiesel),
`daten/netze.csv`. Ergebnis `python -I scripts/sumpf/sumpf_plan.py H5 --bild`:

- **37 789 Instanzen (611 mit Kollision), 115 Netze, 205 Wasserlinsen-Flecken, 7,1 s** (8,2 s Wanduhr mit Bild); Ebenen boden
  20 168 / mittel 10 235 / baum 648 / wasserkante 6 738. Zonen (m²): Flachwasser 36 148, Tiefwasser 68 112, Spiegel 4 732, Ufer 5 145,
  Bult 86 749 (davon 36 877 Nassfläche ohne Wasser), Hinterland 678 026; Wasser 10,3 % des Feldes; Biomanteile sumpf 0,78 / dschungel
  0,15 / aue 0,07 aus `eigner.r8`.
- Größte Klassen: Laub 8 518, Zweige 8 357, Seggenbulten 4 391, Schilf im Wasser 3 521, Moospolster 2 378, Adlerfarn 2 064, Seerosen
  1 376, Binsen 1 183, Pilze 732, Stümpfe 719, Schilf-Landteil 693, Totholz klein 570, Schachtelhalm 544, Pestwurz 433, Weidengebüsch
  408, Wurzelteller 346, Moos am Ufer 350, Seggen am Spiegel 243, Schlammsteine 183; Bäume: Erlen-Ersatz 280, Totbäume Land 132,
  **Totbäume im Wasser 89**, Jungweiden 104, Treibholz 65, große Stämme 67, Weiden 43.
- Prüfskript: alle 115 f32 durch 10 teilbar, Anzahl = `plan.json`, Schema je Datei vollständig (inkl. `ebene`), Quaternionen normiert
  (|q| − 1 ≤ 1,2·10⁻⁷); **0 Instanzen** außerhalb des Feldes, auf Weg, auf Ort; **0 Landklassen-Instanzen auf `karte_wasser`**
  (erst nach der Korrektur: vorher 114 auf Wasserzellen, die der Planer wegen Grund > Spiegel als Land umgedeutet hatte – jetzt hart
  gesperrt, 1 368 solche Zellen als Hinweis protokolliert); 6 232 Wasserklassen-Instanzen auf Wasserzellen mit **z = Grund −
  Eingraben·Maßstab exakt** (Abweichung < 1 mm), Seerosen auf Spiegel + 1 cm bei 0,26–1,5 m Grund darunter; Landklassen z − Gelände
  −0,39 … −0,01 m. **Zwei Läufe byte-identisch** (MD5 aller f32). `--faktor 2.0`: 67 085 → Ziel 48 000, Ausdünnung 0,43 auf
  Schlammsteine/Laub/Zweige, 1 062 Kollision. I5/J7 ohne Daten im Fenster: 0 Instanzen mit Hinweis „kein Wasser im Fenster“, J7 als
  Randspalte 569 m breit in 1,0 s; ungültiges Feld K9, fehlende Basis, fehlende Regeldatei → klare Meldung, Exit.
- Prüfbild (1008 × 1008): Teiche blau mit Tiefenverlauf, Schilf-/Binsengürtel gelb am Rand, Seerosen rosa im Tiefwasser, Spiegel/Ufer/
  Bult grün getönt, Ort rot, Weg braun, Hinterland mit Laub/Zweig-Streu; der Bach bekommt denselben Gürtel (siehe Offene Punkte).
  Große Raster wurden nach dem Test gelöscht (Rest 2,7 MB).

**Erwartete Instanzzahlen je Feld mit Echtdaten (Richtwert, Spanne ± 40 %).** Grundlage: Nassfläche aus den Lagenanteilen (H5
Schlamm + Algen 35 % ≈ 350 000 m²), kartiertes Wasser 0,4 % (H5) bzw. 0,2 % (I5):

| Feld | sumpf % / Nassfläche | gesamt | boden | mittel | baum | wasserkante |
|---|---|---|---|---|---|---|
| H5 | 78 / ~350 000 m² | 35 000–48 000 | 16 000–22 000 | 12 000–20 000 | 400–900 | 1 500–6 000 (hängt am kartierten Wasser) |
| I5 | 11 / ~45 000 m² | 4 000–9 000 | 1 500–3 500 | 1 500–4 000 | 50–150 | 100–800 |
| H4 | 8 / ~30 000 m² | 2 500–7 000 | 1 000–3 000 | 1 000–3 000 | 30–120 | 100–600 |

Kollision je Feld 300–900 (Totbäume, Weiden, Erlen-Ersatz, große Stämme) – weit unter 3 000.

**Prüfkameras:**
1. **H5 Teichufer TEICH1, Augenhöhe 1,7 m**, am Westufer des Teichs mit Blick nach Osten über das Wasser (Vergleich
   TEICH1_H5_teich_T_K5_SUMPF_00). Erfolg: Schilfgürtel steht **im** Wasser und wird mit der Tiefe dünner, Binsen am Spiegel,
   Seerosen-Flecken ab 1,5 m vom Ufer, Wasserlinsen-Decal in den Buchten, 2–5 Totbäume schief im Flachwasser mit Treibholz davor,
   hinter dem Ufer Seggenbulten und Moos statt Rasen, Weidengebüsch in 1–3er-Gruppen bis 18 m, keine Pflanze schwebt (Eingraben 2–8 cm).
2. **H5 Nassfläche ohne Teich, 1,7 m, 60 m vom nächsten Wasser** auf Schlamm/Algen-Lage. Erfolg: Bulten, Moospolster, Schachtelhalm,
   Stümpfe, ein Totbaum je 2 ha, Knüppeldamm am Weg; innerhalb 10 m mindestens ein Objekt in 0,5–3 m Höhe.
3. **H5 Draufsicht 300 m** (Prüfbild und Editor): Totbaum-Gruppen nur an Teichen, Erlen-Ersatz als lichte Gruppen 2–6, kein Raster.
4. **I5 Westrand, 2 m Höhe**, Blick vom Bergwald in die Sumpfzunge: Übergang ohne Kante (Biomfaktor bergwald 0,15, Nassmaske).
5. **Naht H5/G5 und H5/H4** (Draufsicht 100 m): keine Dichtesprünge (Fenster + 64 m).

## 5. Einkaufsliste (frei bevorzugt, High 4K reicht)

| Was | Exakter Name / Suchbegriff (Fab/Megascans) | Wofür | Status |
|---|---|---|---|
| **Rohrkolben / Binsen im Wasser** (Typha, Schoenoplectus) | Megascans führt laut Suchauszug keine Cattail/Bulrush; Fab-Kategorie 3D-Model → Nature → Plants durchsuchen („Cattail“, „Bulrush“, „Typha latifolia“); Drittanbieter-Sets TurboSquid/3dgardenplants sind kostenpflichtig **[Suchauszug]** | `schilf_wasser`, `binse_wasser` (heute Eldarien-Rohrkolben 0,6–3,2 k Dreiecke, kein Nanite; ToadRush 15–29 k ohne Nanite) | **offen**, Ersatz vorhanden |
| **Seerosen** (Nymphaea) | Quixel-Megascans-Kategorie „Submerged“: **Rembrandt Water Lily**, **Carolana Water Lily** **[Suchauszug: quixel.com/megascans/home?category=3D+plant&category=aquatic]**; Preis/Freistellung im Fab-Konto prüfen | `seerose` (heute CityPark SM_WaterPlant01–04, 21–98 Dreiecke, Blattplatten ohne Blüte) | **kaufen/prüfen**, hohe Priorität |
| **Wasserlinsen-Decal** (Lemna) | kein Netz sinnvoll; Fab „Duckweed Decal“ / Megascans Surface „Pond Scum“ oder Material-Maske aus `extras.wasserlinsen_flecken` | Wasserlinsen-Flecken (Punktliste im plan.json) | **prüfen**, sonst Material |
| **Tote Sumpfbäume** entrindet, 8–15 m, mit Wurzelansatz | Megascans Trees „Dead Tree“ (im Inventar nur Dead_Tree_qlEtl 6,2 m), Fab „Nanite Dead Tree Pack swamp“; die Graveyard-Totbäume (23–25 k Dreiecke, kein Nanite) nur mit Gewicht 1 | `totbaum_wasser`, Blickziel-Solitär | offen, Ersatz DeadTree_01/02 + Beech_Dead |
| **Steg / Boot** | Fab „Old Wooden Boat“, „Rowing Boat Wreck“, „Wooden Pier Modular“ (Medieval_Docks-Hivemind im Inventar hat Farne, aber keine Stegmodule mit Pfählen) | `spuren_overrides.steg`, `boot` | **offen**, Steg aus Pales + Plank_4m behelfsmäßig |
| **Hängemoos / Bartflechte** (Usnea, Spanish Moss) | Fab „Hanging Moss“ / „Spanish Moss Nanite“; Megascans hat Moos nur als Boden-Clumps | Vorhang an Totbäumen und Weiden (Velen-Silhouette) | offen |
| **Erle / Bruchwald** (Alnus glutinosa) | Megascans Trees „European Black Alder“ bei Erscheinen; Fab „Alder Tree Nanite“ | `erle_ersatz` (heute Hainbuche + kleine Pappel) | offen |
| **Torf-/Schlammplatten** | Megascans Surface/3D „Mud Ground“, „Peat Bog“, „Cracked Mud“ als Geröllplatte | Taxonomie-Lücke sumpf | offen |
| **Pfähle mit Schädeln / Totems** | Fab „Swamp Totem“, „Witch Hut Props“ | Crones-Akzent für `pfaehle` | optional |

Hinweis aus `boden-kleinzeug-gras.md`: Megascans ist seit 2025 pro Asset kostenpflichtig, sofern nicht vor dem 31.12.2024
beansprucht; Megaplants (z. B. „Dry Common Reed“) sind laut Quixel frei und Nanite-fähig, brauchen aber den Procedural Vegetation
Editor **[Suchauszug: quixel.com/news; fab.com/listings/00299cb6-…]**.

## 6. Offene Punkte und Annahmen

1. **Spiegel-Bestimmung ist die größte Unsicherheit.** Der Fallback (Geländehöhe am Wasserrand, σ 3 m) ist für flache Teiche
   richtig, für Bäche/Flüsse falsch: dort steht das Wasser-Mesh über dem Bett, der Rand ist Böschung → Tiefe zu klein, Gürtel zu breit.
   Deshalb Spiegel bevorzugt aus `teiche.json`/`wasser_welt.json` (`spiegel_cm`); fehlt der Schlüssel, am besten in H5 die vier
   Teichspiegel von Hand eintragen. Fließgewässer sollten über `wasser_welt.json[fluesse]` (Punkte mit z) ausgeschlossen werden – im
   Planer noch nicht umgesetzt (Erweiterung: Flussband dilatieren und aus `wasser` nehmen).
2. **Nur 0,4 % kartiertes Wasser in H5** trotz sichtbarem Teich (TEICH1): entweder sind Teiche nur in `teiche.json`, nicht in
   `karte_wasser.r8` – dann liest der Planer sie über die Umrisse –, oder die Senke ist Schlamm ohne offenes Wasser. Die Bult-Erweiterung
   auf Nassflächen (§2) fängt den zweiten Fall ab; die Wasserkanten-Zahlen bleiben bis zum Echtlauf unsicher.
3. **Format der Umrisse** (`umriss` als `[[x_cm, y_cm], …]`, Spiegel `spiegel_cm`) ist aus FORMAT §2 abgeleitet; andere Schlüssel
   werden mit Hinweis ignoriert, der Planer läuft dann ohne Umrisse weiter.
4. **Seerosen-Netze** (CityPark) sind Platzhalter; Material (Masked, Two-Sided, kein WPO-Wind) im Editor prüfen, sonst Klasse
   deaktivieren (`dichte: 0`).
5. **Doppelung mit Houdini-Rohrkolben und Ufer-Kieseln**: erst nach Sichtprüfung in H5 je Feld `entfernen` setzen (Text in
   `ausgabe.entfernen_hinweis`).
6. **Hang ist im Rauchtest kaum geprüft** (Synthetik flach, Anstieg nur im Osten): Regeln Bäume ≤ 18–20°, Wasserklassen ≤ 35° greifen
   erst mit Echtdaten (H4 bis 489 m Höhe, 33 % steil – dort entscheidet `hoehe_ueber_spiegel_abnahme` 1,5 → 6 m, ob der Sumpf wirklich
   nur in der Senke bleibt).
7. **Bäume des Bestands** werden an Rolle/Gruppe/Namen erkannt (`baum, tree, hornbeam, willow, …` ohne `dead, stump, log, …`);
   `witcher/<Feld>/` und `instanzen.json` fehlten im Test (Code nur syntaktisch geprüft).
8. **Nicht-Nanite-Netze** in der Palette: Big_Tree_willow (30–38 k), Graveyard Dead_Tree (23–25 k), ToadRush (15–29 k), Rohrkolben,
   grey_willow, Poplar_Small – Sichtweiten gesetzt, LOD-Übergänge im Editor prüfen; Anzahl der Weiden ist bewusst klein (43 im Test).
9. **Zahlen** sind Richtwerte aus Bildern; erster Kalibrierschritt: H5 setzen, Kamera 1 und 2 aufnehmen, `--faktor 0,7 … 1,4` vergleichen.
10. `verteilung-STATUS.md` wurde nicht geändert (Koordinator); B6 kann auf „fertig (ungetestet mit Echtdaten)“ gesetzt werden.

## Korrektur Runde 4 (10.10.2026): Meer fehlt in karte_wasser

- `karte_wasser.r8` enthält nur Süßwasser. Neu nach Konventionen §1b: `meer = (hoehe < 0) & (karte_wasser == 0)`.
  - Teich-/See-Umrisse aus `teiche.json`/`wasser_welt.json` gelten als Süßwasser und nie als Meer.
  - `wasser_alle` = Süßwasser | Meer.
- Spiegel, Wassertiefe und die Zonen flachwasser/tiefwasser/spiegel/ufer/bult bleiben **nur am Süßwasser**. Die Gürtel aus Schilf, Binsen, Seerosen und toten Bäumen nach Wassertiefe entstehen also nie im Meer.
  - Meerzellen sind kein Land und haben Zone 0 (keine Klasse). Sie sind in der Grundsperre und nie Nass- oder Bultenfläche.
  - `zellen_zustaendig` zählt das Meer nicht mehr mit.
- Küstensaum (Nicht-Wasser unter +0,3 m bis 30 m zum Meer): nur Rolle `wasserkante`, `strand: true` oder `meer_rolle: true`.
  - Zusätzlich gibt es einen Schlussfilter am Instanzort (bilineare Geländehöhe, vor dem Budget).
  - Neuer Block `meer` in `sumpf_regeln.json`. Neu in `plan.json`: `meer_zellen`, `meer_gefiltert`, `statistik.meer`.
- Rauchtest synthetisch H5: flache Marschküste (0–0,3 m auf 75 m), Meer bis −6 m ohne `karte_wasser`, Polder −0,4 m hinter der Küste, vier Teiche über 0 m in `karte_wasser`. Höhe = Gelände am Instanzort:

  | | vorher | nachher |
  |---|---|---|
  | Instanzen gesamt | 47 930 | 47 823 (Budget-Ziel 48 000 greift in beiden Läufen) |
  | Gelände < −0,3 m (Meer) | **840** | 0 |
  | −0,3 … 0 m (Meer) | 28 | 0 |
  | auf Meerzellen | 863 | 0 |
  | 0–0,3 m ≤ 30 m zum Meer | 1 763 (baum 61, boden 773, mittel 670, wasserkante 259) | 0 |
  | Instanz-z < −0,3 m | 846 | 0 |
  | `zellen_zustaendig` | 1 016 064 | 807 814 |

  - `meer_zellen` 304 315, `meer_gefiltert` 3. Mit `--faktor 0.5` (ohne Budget) 43 167 → 40 798.
  - 41 Instanzen liegen 29,5–31 m vom Meer (Zellraster): Rundung an der Saumgrenze.
- Süßwasser unverändert:
  - Mit `--faktor 0.5` sind alle 972 Instanzen auf `karte_wasser`-Zellen byteidentisch. Die Klassen schilf_wasser 629, binse_wasser 207, seerose 118, totbaum_wasser 9, treibholz_wasser 9, seggen_spiegel 48, schilf_land 98, moos_ufer 26 und schlamm_stein 13 sind gleich geblieben.
  - Mit Faktor 1 sind die Wassertiefe-Klassen gleich (totbaum_wasser 19, schilf_wasser 1 213, binse_wasser 470, seerose 237, treibholz_wasser 15, schilf_land 152).
  - Nur seggen_spiegel 36 → 38, moos_ufer 27 → 30 und schlamm_stein 12 → 14 ändern sich. Grund: Das Budget dünnt weniger aus (Runde-1-Faktor 0,532 → 0,566), weil die Meer-Instanzen fehlen.
- Zwei Läufe byteidentisch (f32 und plan.json, Faktor 1 und 0,5), Log ASCII, py_compile ok, 5–6 s. Leerplan (C2) meldet `meer_zellen`.
- Offen:
  1. (erledigt, Nachtrag) Netze mehrerer Klassen in verschiedenen Ebenen: **Entscheidung eigene Datei je Ebene** (`<Netz>_e<Ebene>`, z. B. `SM_ToadRush_00_e1` für segge_bult, `SM_Rohrkolben_Horst_*_e1` für schilf_land), statt Mehrheits-Rolle – so stimmt `rolle`/`ebene` jeder Datei exakt (Test C4: 10 Dateien mit fremder Ebene → 0), Klassen derselben Ebene teilen sich weiter eine Datei (`gruppen`).
  2. (erledigt, Nachtrag) Landzellen-Bezug (§1): `biome_fenster` und Eigenanteil (2-%-Schwelle) nur über Landzellen ohne `wasser_alle`; Saum nur auf Land, Süßwasser des eigenen Bioms bleibt eigen (Teich-Gürtel unverändert), kein Saum in fremde Teich-/See-Umrisse; `biome_fenster_bezug: "land"`. Synthetisch: Inselfeld E4 Leerplan → Plan (1,37 % → 77,2 %, 2 517 Instanzen, 268 im eigenen Inselteich), Binnen E6: 2 135 Instanzen im Kennzahl-0-See (Saum) → 0, `zellen_zustaendig` 791 219 → 765 959. Risiko aus K6 bleibt: liegen Sumpfteiche in `eigner.r8` auf Kennzahl 0, bekommen sie jetzt gar keinen Gürtel mehr (vorher Saum-Gürtel bis 30 m) – beim Echtlauf H5 prüfen. Byteidentisch, ASCII.
  3. Keine Meeres-Klassen im Sumpf. `meer_rolle` lässt der Schlussfilter zu, eine Meer-Zone gibt es aber nicht (Tang und Muscheln gehören zu nordkueste).
