# Verteilung Biomgruppe 3: Heide/Tundra (Skellige-Heide, Velen-Moor, Kovir-Hochland)

**Auftrag 11, Teil B3.** Biome `heide` und `tundra`, Thema `heide_tundra`, Foliage-Präfix `FT_EL_HT_`, Ordner
`/Game/Eldarien/Welt/Foliage/HeideTundra`. Stand 2026-10-10, **Korrektur Runde 1**. Lieferung: dieser Bericht,
`skripte/heide_tundra_regeln.json` (13 Planer-Klassen in 4 Schichten, 85 Paletteneinträge = 75 Netze; dazu `mittelschicht_overrides`
mit 56 Netzen für Teil D, `felsgruppen_overrides` und `spuren_overrides`; alle 158 Netzpfade gegen `netze.csv` geprüft, 0 fehlend),
`skripte/heide_tundra_plan.py` (Planer nach FORMAT §3/§5 und Konventionen §1–§5, 1 154 Zeilen, nur NumPy).
**Alles UNGETESTET MIT ECHTDATEN** – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern rauchgetestet (Abschnitt
„Korrektur Runde 1“, Runde 0 in §4). Web-Quellen waren nur als Suchmaschinen-Auszüge lesbar (6 WebSearch-Läufe); solche Belege sind
mit **[Suchauszug]** markiert, Zahlen ohne Beleg mit **Richtwert**.

Betroffene Felder laut `biome_je_feld.md`: **Tundra** D2 (47 %, 26–446 m, 57 % steil, Heide 22 / Trockengras 21 / Fels 19 / Schnee 9 %),
C2 (21 %), D3 (73 %), E3 (60 %), C3 (27 %; D3/E3/C3 Wüstenfelder), E2 (11 %); **Heide** G5 (77 %, flach, Trockengras 37 / Heide 16 %),
F5 (74 %, 9,7 % Wasser), F4 (21 %), G4 (22 %, Laub 75 % – Waldsperre). Seit Korrektur Runde 1 bebaut der Planer **nur Zellen mit Biom
heide/tundra** (`eigner.r8` + `welt.json`, Kennzahl 0 = `aue`) plus einen 30-m-Saum mit linear fallender Dichte; bei weniger als 2 %
Heide/Tundra im Fenster schreibt er einen leeren `plan.json`. Die Runde-0-Logik (Nachbarbiome mit Faktor, Profil nach Lage für jede
Zelle, `eigner = 0` → dominantes Feldbiom) ist gestrichen; sie hat die Instanzen in E1, G4, A5 und C6 erzeugt (siehe unten).

## Korrektur Runde 1 (10.10.2026, nach `auftraege/verteilung-korrektur-runde1.md` und `verteilung-KONVENTIONEN.md`)

**Anlass (Echtdaten-Test 10.10. 15:30).** Der Planer lief auf A5, G4, E1, C6 ohne Absturz, setzte aber in jedem Feld Instanzen:
A5 (kueste/bergwald/aue) **941**, G4 (elfenwald 76 %, heide 22 %) **4 020**, E1 (gletscher 100 %) **4 360**, C6 (lava 99 %) **172**.
Die lokale Instanz hatte `heide_tundra` wegen `profil_anteil_feld`/`biome_fenster` als Vorbild genannt. Die Ausgabe war vorbildlich,
die Zuständigkeit aber nicht.

**Ursache E1 (gletscher 100 % → 4 360 Instanzen).** Weder ein Saum noch ein Fehler im Profil-Fallback war schuld. Der Planer tat in
Runde 0, was die Regeln vorsahen, und drei Mechanismen addierten sich:
1. **`profil_je_biom`** bildete jedes Fremdbiom auf ein Profil mit Grundfaktor ab: `gletscher → tundra × 0,35`, `fjord × 0,5`,
   `frost × 0,3`, `bergwald × 0,25`, `aue`/`kueste → heide × 0,4`, `elfenwald × 0,15`, `sumpf × 0,3`. Damit war die gesamte Landfläche von E1
   (35 % Land) mit 35 % der Tundra-Dichte planbar. Das ist der Hauptteil.
2. **`lagen_biom_hinweis`**: Zellen mit Heide-Lage ≥ 40 % wurden **unabhängig vom Biom** zur Heide (Faktor ≥ 0,8), und Zellen mit
   Trockengras ≥ 50 % über 120 m zur Tundra (≥ 0,6). E1 hat Trockengras 7 % und Heide 5 %, das ergibt einzelne Inseln mit fast voller Dichte.
3. **Kennzahl 0** (Weltgelände) wurde als dominantes Feldbiom gelesen (`biome_je_feld.json` → E1 = gletscher, danach Punkt 1),
   nicht als `aue`.

Dieselben Wege erklären die anderen Felder: G4 bekam elfenwald × 0,15 (zusätzlich Laub-Sperre × 0,15) auf 76 % der Fläche, zu den
echten heide-Zellen (22 %) hinzu. A5 bekam kueste/aue × 0,4 und bergwald × 0,25. C6 (lava × 0) bekam seine 172 Instanzen aus
den 3 % bergwald × 0,25.

### Änderungen

| Punkt | Runde 0 | Korrektur Runde 1 |
|---|---|---|
| Biom je Zelle (§1) | Kennzahl 0 → dominantes Feldbiom (`biome_je_feld.json`, sonst `feld_biom_fallback`) | Kennzahl 0 und Kennzahlen ohne erkennbares Rezept → **`aue`**, Rezept mit vulkan/lava → `lava`. Nur wenn `eigner.r8` oder `welt.json` fehlen oder unlesbar sind: dominantes Feldbiom aus `daten/biome_je_feld.json`, mit Hinweis in Log und `hinweise`. `feld_biom_fallback` gestrichen |
| Zuständigkeit (§1) | `profil_je_biom` mit Grundfaktoren für 13 Fremdbiome; Lagen machten jede Zelle zu Heide/Tundra | `zustaendigkeit.biome_eigen = ["heide", "tundra"]`. Nur eigene Zellen plus **30-m-Saum, linear 1 → 0** (Jump-Flooding-Distanz mit Index der nächsten eigenen Zelle; im Saum gilt deren Profil). Gruppenmitglieder werden zusätzlich gegen den Saum geprüft, damit nie eine Instanz jenseits des Saums liegt. `profil_je_biom` und `lagen_biom_hinweis` gestrichen. Neu ist `profil_nach_lage`: Heide-Lage ≥ 40 % schaltet in **tundra-Zellen** nur das Profil auf heide (Heideinseln) und ändert nie die Zuständigkeit |
| Leerplan (§1) | – | Eigenanteil im Fenster (Feld + 64 m) **< 2 %** → `plan.json` mit `instanzen: 0`, `dateien: {}`, `entfernen: ""`. Alte `.f32` werden gelöscht, dazu eine Logzeile |
| Wüstenfelder | C3, D3, E3: × 0,7, nur heide/tundra-Zellen | Liste nach FORMAT §2 auf **C3 C4 D3 D4 D5 E3 E4 E5** erweitert; × 0,7, **kein Saum** in Wüsten-/Fremdzellen, Sand/Sandstein-Sperre wie bisher, `entfernen` wird immer ignoriert |
| plan.json (§2) | `biome_fenster` (unsortiert, auf die Profil-Biome reduziert), `kollision_instanzen`, `feldbiom_fuer_eigner0` | Pflichtschlüssel `biome_fenster` (alle 15 Biome möglich, absteigend, Summe 1), `zellen_zustaendig` (Feldzellen mit Saumfaktor > 0), `biome_eigen`, `kollision_anzahl`; `entfernen` immer vorhanden. Unter `statistik` neu: `anteil_eigen_fenster`, `anteil_eigen_feld`, `biom_quelle`, `saum_m`, `wuestenfeld`, `instanzen_vor_budget` und `ausserhalb_eigener_zellen` (Instanzen im Saum, für die Prüfung „liegen die Instanzen wirklich auf heide/tundra?“) |
| Budget (§3) | Ziel 45 000 weich, danach proportional per Hash. Die harte Grenze und der Kollisionsdeckel waren nicht exakt | 1. Kollisionsdeckel 3 000 **exakt** (Kollisionsklassen von hinten nach `prioritaet`). 2. Ziel **48 000** mit weicher Hash-Ausdünnung, je Klasse höchstens auf 25 %. 3. Deckel 60 000 **exakt** (die höchsten Hashwerte der niedrigsten Priorität fallen zuerst). Jede Stufe steht als `WARNUNG` in Log und `hinweise`. Kiesel/Streumatte (`kleinzeug_an_gras`) bekommen den Hinweis „Landschafts-Gras übernimmt“ |
| Ebenen (§4) | Schicht 1 mit 9 Klassen, davon 6 generisch (grasbueschel, jungwuchs, heideblüte, totholz, stumpf; zweige in Schicht 0) | Schicht 1 nur **Sonderformen**: `heidekraut` (Heidekraut-Flecken), `wacholder` (Wacholder-Gruppen), `kruepelkiefer` (Krüppelkiefern), `wollgras` (Wollgras-Büschel am Moor, aus Schicht 5 hierher). Generische Klassen → `mittelschicht_overrides`. Der Planer verwirft zur Sicherheit jede Klasse mit einem Namen aus der §4-Liste (WARNUNG) |
| Fels-Grenze (§4) | Flechtensteine bis 1,2 m × 1,5 = 1,8 m | `fels_grenze_m` 0,8: Der Planer streicht Steinnetze, deren größte Kante × Maßstab-Max über 0,8 m liegt. Flechtenstein-Maßstab 0,6–0,9, Moorstein 0,9–1,5. `xjijbgx`, `mountain_rock_big_01_2/3` und `stones_01_3` wandern in `felsgruppen_overrides` (tundra `paletten_ergaenzung`, heide `paletten_neu.stein`) |
| Paletten-Doppelungen | Beeren in `heidekraut`, Strandrose in `wacholder`; Kiefern-Kurzformen sowohl in `kruepelkiefer` als auch in Teil-D-`jungbaum` | `heidekraut` nur noch heath_A/B/cross, forest_heather (tundra + rhododendron_01). `wacholder` nur Zwergkiefer/Sanddorn. Die Override-Paletten für Teil D lassen alle B3-Sonderform-Netze weg (keine pine_beach_crooked/short in `jungbaum`, keine Zwergkiefer in `strauch`) |
| Logs (§5) | Umlaute, „→“, „…“ in `print()`; Fehler als `SystemExit`-Text (Exit-Code 1) | alle Logs über `ascii_text()` (ae/oe/ue/ss, `->`, `...`). Fehlende `hoehe.f32`, fehlende oder unlesbare Regeldatei und ein unbekanntes Feld ergeben eine `FEHLER: …`-Zeile mit **Exit-Code 2** |

### Neue Schicht-1-Definition (Heide/Tundra-Sonderformen)

| Klasse | Sonderform | Netze | Steuerung |
|---|---|---|---|
| `heidekraut` | Heidekraut-Flecken | heath_A_01, heath_B_01, heath_cross_01, forest_heather_01/simple_01; tundra: heath_A/B/cross, rhododendron_01 | 0,07 / 0,055 je m² **nur in Rausch-Flecken** 20–60 m (Deckung ≈ 35 %), Gruppen 4–12, Maßstab 1,1–1,9, Zwergstrauch-Grenze 460 m (tundra) |
| `wacholder` | Wacholder-Gruppen | tundra: dwarf_pine_small_01/02, medium_01/03; heide: sea_buckthorn_03–06, dwarf_pine_small_01 | 0,0028 / 0,0022, Gruppen 1–5 in 3 m, Kuppen +30 %, Strauchgrenze 380 m |
| `kruepelkiefer` | windschiefe Krüppelkiefern | pine_beach_crooked_01/02, short_01/02, dwarf_pine_big_01/02 | 0,0009 / 0,0004, Gruppen 1–3, Kuppen +60 %, Lee-Neigung 4–12°, Kollision ab 2 m |
| `wollgras` | Wollgras-Büschel am Moor | Tundra_Grass VarB/C/G, grass_meadow_08 (hoch skaliert) | 0,12 im Band 0,5–9 m um Moortümpel und × 0,35 auf Moos/Schlamm ≥ 50 %, in Wollgras-Flecken |

Unverändert bleiben Schicht 0 (`kiesel`, `flechtenstein` < 0,8 m, `streumatte`), Schicht 2 (`einzelkiefer`, `moorbirke`, `totbaum`) und
Schicht 5 (`seggen`, `moorstein`, `treibholz`). Treibholz hat jetzt kein Netz mehr mit dem liegenden Totholz gemeinsam, deshalb gibt es
keinen Kollisions-Konflikt zwischen den Klassen mehr.

### Override-Schema `mittelschicht_overrides` (für `mittelschicht_plan.py`, Teil D)

```
"mittelschicht_overrides": {
  "biom": ["heide", "tundra"],
  "palette":   {klasse: [Unreal-Pfade]},     # gilt für heide UND tundra: totholz_liegend, totholz_stumpf, totholz_ast (B3-Paletten)
  "faktor":    {klasse: float},              # gemeinsamer Grundwert (farn 0, pilz 0), von je_biom überschrieben
  "parameter": {klasse: {schluessel: wert}}, # massstab, eingraben_cm, kippen, sichtweite, kollision, laengs_hang, hang_max, nah_baum, feuchte, mulde
  "zusatzklassen": {"heidebluete": {..., "biome": ["heide"]}},   # vollständige Klasse im mittelschicht-Schema
  "vorlage_biom": {"totholz_stumpf": "heide"},                   # Vorlage, wo Teil D die Klasse im Biom nicht hat
  "je_biom": {"heide":  {"palette": {...}, "faktor": {...}, "vorlage_biom": {"farn": "bergwald"}},
              "tundra": {"palette": {...}, "faktor": {...}}},     # biomspezifisch, gewinnt gegen den flachen Block
  "faktor_doku": {...}, "herkunft_b3": {...}, "_entfernen_vorschlag": {...}   # Doku, von Teil D ignoriert
}
```

Teil D liest zuerst den flachen Block und danach `je_biom[biom]`, so wie `effektive_regeln()` in `mittelschicht_plan.py` es tut.
Geprüft mit `lade_overrides()` und `effektive_regeln()` aus Teil D: Der Block wird gelesen (palette, faktor, zusatzklassen, parameter,
je_biom, vorlage_biom), es gibt 0 unbekannte Schlüssel und 0 verworfene Netze. Wirksame Klassen:

| Klasse | heide: Palette / Faktor | tundra: Palette / Faktor | Herkunft B3 Runde 0 |
|---|---|---|---|
| grasbueschel | Tundra_Grass VarC/F/G, grass_bush_01/03/04, grass_meadow_03/06/08 / **0,85** | VarA/C/D/F/G/H, grass_03_A_1/B_1 / **0,6** | `grasbueschel` 0,028/0,03 in Flecken (≈ 60 %) |
| jungbaum | Hainbuche Sapling 01/02, Seedling 01/02, Forest_pine_plant_01 / **0,3** | Forest_pine_plant_01/02, grey_willow_01 / **0,4** | `jungwuchs` 0,0008/0,0005; Feuchte × 2,5, Mulde × 1,5 als `parameter` |
| strauch | grey_willow_02/03, beach_rose_04/05/06 / **0,5** | rhododendron_02, grey_willow_01/02 / **0,4** | aus `wacholder` ausgelagerte Netze; Laubgebüsch (Hasel, Holunder, Ahorn) der Teil-D-Palette ersetzt |
| beere | billberry_01/02/dry_01, lingonberry_01/02 / **0,5** | lingonberry_01/02, billberry_dry_01, billberry_03 / **0,6** | Beeren-Netze aus `heidekraut` |
| totholz_liegend | beach_driftwood_01, Forest_pine_04/08_log, dead_log_03/04, OldTreeBranch_06 / **0,8** | gleich / **1,2** | `totholz` 0,0004/0,00035, Kollision, längs Hang, × 2 nahe Bäumen |
| totholz_stumpf | pine_stump_01–03, BirchTreeStump_01 / **1,0** | gleich (Vorlage heide) / **0,75** | `stumpf` 0,0002/0,00015 |
| totholz_ast | DryBranches_01/04/05/07, mountain_branch_01_01/02 / **0,65** | gleich / **0,75** | `zweige` 0,004/0,003, × 2,5 nahe Bäumen |
| hochstaude | Teil-D-Palette / **0,3** | Teil-D-Palette / **0,5** | – (Goldrute/Crownbeard wirken auf Heide fremd) |
| farn | EagleFern M_01, S_01/02/04 (Adlerfarn, Vorlage bergwald) / **0,4** | – / **0** | – |
| pilz | Teil-D-Palette / **0,5** | – / **0** | – |
| **Zusatz** `heidebluete` | beach_rose_02/03/04_with_pink_flowers, Dichte [0,0005 licht, 0,0001 Schatten], Gruppen 2–4, Maßstab 0,6–0,9 | – | `heideblüte` 0,0012 in Heideflecken |

`felsgruppen_overrides` (heide: Palette `heide` neu, Faktor 0,7, `band/wand/fuss/blockstrom` aus, `findling_frei`; tundra: Faktor 1,0,
`blockstrom` × 1,3, `blockfeld`, `findling_frei`) und `spuren_overrides` (Steinmauern, Pferch, Torfstich, Steinkreis, Steinmänner) bleiben
erhalten. Nur bei den Felsgruppen kamen die abgegebenen Flechtensteine > 0,8 m hinzu. `lade_overrides()` aus `felsgruppen_plan.py` liest
für heide/tundra 12 Schlüssel, darunter die neue `paletten_ergaenzung.tundra`, sowie die Zusatzklasse `blockfeld`. 32 Feinparameter
ignoriert es: `kuppe.hero_p/umkreis_m/block/stein/kiesel/eingraben`, die Details von `findling_frei` und `auflage`. Die stehen weiter als
Beschreibung für Teil C im JSON. `spuren_plan.py` liest heute noch keine `spuren_overrides` (offen bei Teil D).

### Rauchtest Korrektur Runde 1 (synthetisch, Raster neu erzeugt, danach gelöscht)

Synthetische Produktionswurzel im Scratchpad mit `hoehe.f32` in voller Größe (memmap). Gebirge im Norden (E1/D2 bis 345 m), flach im
Süden, vier Tümpel, ein Weg in G5, ein Ort in D2. `eigner.r8`/`welt.json`: 3 = tundra, 8 = heide, 2 = gletscher, 5 = dschungel,
11 = Vulkanregion, 0 = Weltgelände. Die Belegung:
- D2: tundra, das Westdrittel gletscher (Saum innerhalb des Feldes).
- G5: heide, die östlichen 22 % dschungel.
- F4: Weltgelände (aue), am Ostrand ein 208 m breiter heide-Streifen (Mischfeld).
- E1/E2: gletscher.
- D3: tundra im Westen, Sand nach Osten zunehmend.

Dazu acht `lage_*.r8`, `bestand/D2` (300 Kiefern), `witcher/G5` (400 Büsche), `ufer/foliage_D2` sowie `daten/netze.csv` und
`biome_je_feld.json` aus der Vorlage. Aufruf: `python -I -X utf8 heide_tundra_plan.py D2 G5 E1 F4 C6 D3 --bild --basis prod`
(Python 3.13, NumPy 2.5, ohne numba):

| Feld | Rolle | Instanzen | Kollision | Boden / Mittel / Baum / Wasser | biome_fenster | zellen_zustaendig | im Saum (max. Abstand) | Zeit |
|---|---|---|---|---|---|---|---|---|
| D2 | eigene Zellen (tundra) | **16 399** | 131 | 12 543 / 3 797 / 59 / 0 | tundra 0,554, gletscher 0,316, aue 0,131 | 715 511 | 604 (29 m) | 6,6 s |
| G5 | eigene Zellen (heide) | **36 674** | 331 | 17 785 / 18 692 / 180 / 17 | heide 0,614, aue 0,210, dschungel 0,177 | 817 488 | 666 (28 m) | 5,5 s |
| E1 | Gletscherfeld | **0** (Leerplan) | 0 | – | gletscher 0,887, aue 0,109, tundra 0,003 | 0 | – | < 0,1 s |
| F4 | Mischfeld aue/heide (Saum) | **10 595** | 127 | 5 448 / 5 076 / 71 / 0 | aue 0,834, heide 0,166 | 238 896 | 623 (28 m) | 5,9 s |
| C6 | ohne Heide/Tundra | **0** (Leerplan) | 0 | – | aue 1,0 | 0 | – | < 0,1 s |
| D3 | Wüstenfeld (nur ergänzen) | **14 816** | 184 | 8 534 / 6 202 / 80 / 0 | aue 0,497, tundra 0,483, gletscher 0,020 | 580 608 (= 576 × 1 008, ohne Saum) | 0 | 4,5 s |

Geprüft wurde Folgendes:
- **Schlüssel:** Alle Pflichtschlüssel nach FORMAT §3 und Konventionen §2 sind vorhanden, auch im Leerplan. Je Datei sind `pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene` gesetzt. `instanzen` ist gleich der Summe der `.f32` und der `anzahl`, und `kollision_anzahl` ist gleich der Zahl der Instanzen mit `kollision=true`.
- **Zuständigkeit:** Alle Instanzen liegen im Feld. **0 Instanzen liegen jenseits des 30-m-Saums**, der größte Abstand zur nächsten eigenen Zelle ist 29 m. In der Prüfung zählen die Instanzen auf Fremdzellen getrennt (D2 nur gletscher, G5 nur dschungel, F4 nur aue).
- **Saumverlauf:** Über eine einzelne Biomgrenze in 10-m-Bändern, innen drei Bänder | außen vier Bänder:
  - G5: 401 / 458 / 375 | **352 / 182 / 107 / 0**
  - F4: 441 / 476 / 487 | **344 / 215 / 78 / 0**

  Die Dichte fällt also linear auf 0.
- **Sperrflächen:** 0 Instanzen auf Wasser, Weg oder Ort. Die Quaternionen sind normiert (|q| − 1 ≤ 1,2·10⁻⁷).
- **Determinismus:** Bei zwei Läufen sind die MD5 aller 185 `.f32` gleich, und `plan.json` ist bis auf `stand`/`laufzeit_s` identisch.
- **Budget:**
  - G5 mit `--faktor 3`: 108 679 → **47 991** (Ziel 48 000), 1 044 mit Kollision, die WARNUNG steht im Log.
  - Testregeln mit Deckel 20 000, Kollision 100 und Ziel 15 000: exakt **20 000** Instanzen, **97 ≤ 100** mit Kollision. Zuerst gestrichen wurden Kiesel und Streumatte, dazu kam der Kleinzeug-Hinweis.
- **Fallback ohne `eigner.r8`:** Die Felder werden über `biome_je_feld.json` gelesen, mit Hinweis im Log. G5 wird als heide gelesen (46 739 Instanzen). E1 (gletscher), C6 (lava) und F4 (aue) bekommen einen Leerplan.
- **Fehlerfälle:** Fehlende `hoehe.f32`, Feld K9, fehlende Regeldatei und eine unlesbare Regeldatei enden jeweils mit einer `FEHLER`-Zeile und **Exit-Code 2**.
- **Logs:** Alle Läufe haben 0 Nicht-ASCII-Bytes. `py_compile` ist sauber, pyflakes meldet nur den optionalen numba-Import.

Die Werte sind mit Runde 0 nicht direkt vergleichbar (anderes synthetisches Raster: D2 44 905, G5 44 976). Der Rückgang kommt vor allem
aus Schicht 1. In G5 sank sie von 34 925 auf 18 692, weil Grasbüschel, Jungwuchs, Heideblüte, Totholz und Stümpfe jetzt Teil D setzt;
Zweige fehlen außerdem in Schicht 0. G5 liegt ohne Budget-Eingriff unter dem Ziel (Runde 0: 69 711 → 44 976 gekappt).

**Echtdaten Runde 0 und Erwartung nach der Korrektur** (Feldwerte aus `biome_je_feld.json`):

| Feld | Biome | Runde 0 (echt) | Erwartung Runde 1 | Begründung |
|---|---|---|---|---|
| A5 | kueste 75, bergwald 14, aue 11 | 941 | **0** (Leerplan) | keine heide/tundra-Zellen im Fenster |
| G4 | elfenwald 76, heide 22, aue 3 | 4 020 | **500–4 000**, nur auf heide-Zellen plus ≤ 30 m Saum | elfenwald × 0,15 entfällt; Laub ≥ 60 % dämpft weiter × 0,15; Schicht 1 nur Sonderformen. Im `plan.json` prüfen: `biome_fenster.heide` ≈ 0,2, `statistik.ausserhalb_eigener_zellen` = Saum-Instanzen |
| E1 | gletscher 100 | 4 360 | **0** (Leerplan) | gletscher gehört zu `hochgebirge`; tundra-Zellen aus E2/D2 im 64-m-Rand < 2 % |
| C6 | lava 99 | 172 | **0** (Leerplan) | bergwald × 0,25 entfällt |
| D2 / G5 / F5 | tundra 47 / heide 77 / heide 74 | – | 18 000–40 000 / 30 000–52 000 / 12 000–30 000 | `erwartung_je_feld` |

**Offen für Echtdaten:**
- **Kennzahl 0:** Sind Heide/Tundra-Flächen in `eigner.r8` als Kennzahl 0 kodiert, liest der Planer sie nach Konvention als `aue` und bleibt dort leer. Das bitte beim ersten Lauf an `biome_fenster` von G5/D2 prüfen; heide bzw. tundra sollte dort > 0,4 sein.
- **Teil D:** Bis Teil D `mittelschicht_overrides` liest, fehlen in Heide/Tundra Grasbüschel, Jungwuchs, Totholz und Heideblüte der Runde 0.

## 1. Witcher-Analyse: Skellige-Heide/Hochmoor, Velen-Moor, Kovir-Hochland

**Was Skellige über die Baumkrone hinaus füllt.** Die Skellige-Inseln bestehen aus drei Höhenbändern, die in den Zielbildern
(witcher_06: Felswand → hausgroße Blöcke → Kopfsteine → Schnee in Rissen) und in der Bildkritik als Prinzip festgehalten sind:
jede Fläche trägt drei bis vier ineinandergreifende Größenstufen plus Makro-Variation im 100–500-m-Maßstab. Auf der Skellige-Heide
sind das: (a) ein durchgehender Heidekraut-Teppich (Calluna) kniehoch in **Flecken** von 20–60 m, dazwischen Trockengras, Flechtenboden
und nackter Fels; (b) darüber 0,5–2 m: Wacholder, Ginster, Krüppelkiefern, einzelne Birken, Findlinge mit Flechten; (c) Bäume nur als
windschiefe Einzelkiefern auf Kuppen und kleine Gruppen in Mulden, darüber die Baumgrenze mit Blockfeldern und Schnee; (d) Spuren:
Trockensteinmauern, Schafpferche, Steinkreise und Steinmänner als Wegmarken im Nebel. CDPRs eigene Beschreibung des Verfahrens ist
bekannt: Vegetation wird mit **Pinseln je Geländetyp** gesetzt, mit einstellbarem Spacing und Scale-Variation, in der Reihenfolge
große Bäume → kleine Bäume → Farne → Gras **[Suchauszug: 80.lv „World Building of Witcher 3“, M. Janiszewski]**. Die Artstation-Seite
von Mark Foreman (Location-Blockout, Lighting, Polish) nennt Skellige als Schwerpunkt der Final-Polish-Phase, gibt aber keine Zahlen
**[Suchauszug: artstation.com/artwork/L8LlP]**; die UE4-/SpeedTree-Nachbildung „The Fields of Ard Skellige“ (exp-points.com) rät,
Foliage auf große Formen und Silhouette zu bauen, damit die Szene auch in der Distanz liest **[Suchauszug]**. Für die Heide heißt das:
die Lesbarkeit kommt aus den **Flecken** (violett/braun/grau im 20–60-m-Maßstab), nicht aus Einzelpflanzen. Deshalb steuert der
Planer Heidekraut, Gras und Wollgras über Wertrauschen mit Schwellen (§2 „Flecken“), nicht über gleichmäßige Dichte.

**Moor vs. Heide (Velen-Moor).** Wikipedia trennt „heath“ (Tiefland, trocken, frei dränend, saure Böden, niedriges Zwergstrauchgesicht)
von „moor“ (Hochland, hoher Niederschlag) **[Suchauszug: en.wikipedia.org/wiki/Heath, /Moorland]**; die britischen NVC-Klassen geben
Richtwerte für die Struktur: Trockenheide H10/H12 (Calluna–Erica cinerea bzw. Calluna–Vaccinium) hat Calluna-Dominanz, meist 0,3–0,5 m,
ungebrannt bis 1 m hoch, Beweidung ersetzt Zwergsträucher durch Gras **[Suchauszug: JNCC CSM Upland Habitats 2009; sac.jncc.gov.uk
H4030]**. Velens Moor (Crookback Bog) ist das nasse Gegenstück: Wollgras-Weiß über Torfmoos, Tümpel mit Binsenrand, Totbäume und
gebleichte Stämme im Wasser, Torfstiche. Velen-Artist Kacper Niepokólczycki nennt als Thema „desperation, hunger and hopelessness“
und als Vorbild polnische Dörfer **[Suchauszug: 80.lv]** – das Moor ist bewusst karg, mit wenigen, aber starken Akzenten (Hangman's
Tree). In Eldarien liegt dieser Charakter in den Moortümpeln von F5/G5 (Wasser 9,7 bzw. 3,9 %) und in den Moos-/Schlammflächen; die
Schicht `5 wasserkante` setzt dort Wollgras-Stellvertreter, Binsen, Moorsteine, Treibholz und Totbäume (Wasser-Bonus ×2 im 30-m-Band).

**Kovir-Hochland (Witcher-4-Demo).** Die Tech-Demo (State of Unreal 2025, PS5, 60 fps, Ray Tracing) zeigt Kovir mit Nanite Foliage
(einzelne Blätter und Zweige mit Wind) und FastGeo Streaming ohne Pop-in **[Suchauszug: cdprojektred.com Blog 149; blog.playstation.com
2025/06/03; gamingbolt „9 takeaways“]**; die Landschaft ist ein kaltes, offenes Hochland mit Nadelwald in den Tälern, Fels und
kurzem Gras darüber. Zahlen zu Dichten nennt keine Quelle; abgeleitet werden nur drei Regeln: Bäume brechen an der **Baumgrenze** ab
(Eldarien: D2 Ø 182 m, max 446 m, Schnee ab ~300 m → Einzelbäume bis 300 m, Krüppelholz bis 380 m, Zwergstrauch bis 460 m, Gras bis
520 m, **Richtwert** aus den Lagenanteilen in `biome_je_feld.md`), Bäume auf Kuppen sind **windschief** und klein (Lee-Neigung 4–12°,
Maßstab 0,6–0,85), in Mulden stehen sie in Gruppen und größer (2–5, Maßstab 0,95–1,25).

**Dichten und Gruppen (Richtwerte aus Zielbildern und NVC).** Heidekraut-Deckung in Heideflecken ≈ 35 % (Calluna dominant mit
Gras-/Flechtenlücken); Grasbüschel 0,3–1,6 m dazwischen; 1 Strauch je 300–450 m²; 1 Krüppelkiefer je 1 000–2 500 m²; 1 Einzelbaum je
6 000–8 000 m²; Findlinge 3–8 je km²; Flechtensteine 1 je 100–250 m²; Kiesel 0,014–0,035/m². Farbakzente: Heideblüte rosa-violett nur
in Heideflecken, Wollgras-Weiß am Tümpel, Moorbirke hell am Moorrand, Flechten-Gelbgrün auf Südseiten der Steine (Teil C).

**Was heute fehlt (Ist-Bilder).** BERG8_D2: glatte Doppelkuppeln „wie Dünen“, Felsschalen als Konfetti; BACH3_G5: „Heidefleck
rechts abrupt“, Wiese ein Beige, Büsche als gleichmäßige Punkte (Bildkritik: Heide-Kante mit Noise 10–20 m aufbrechen, Büsche in
Gruppen 3–7). Genau das liefert die Ebene: Heideflecken mit weichem Rand (~3–6 m), Wacholder 1–5, Krüppelkiefern 1–3, Flechtensteine 2–6.

**Quellen (6 WebSearch-Läufe, nur Suchauszüge):** 80.lv „World Building of Witcher 3“ (Janiszewski, Niepokólczycki) · ArtStation
Mark Foreman „The Witcher 3: Wild Hunt“ · exp-points.com „The Fields of Ard Skellige (UE4/SpeedTree)“ · Wikipedia „Heath“, „Moorland“ ·
JNCC „Common Standards Monitoring Guidance for Upland Habitats“ (2009), sac.jncc.gov.uk/habitat/H4030 · cdprojektred.com Blog 149,
blog.playstation.com (Witcher-4-Tech-Demo 2025) · Fab/Quixel „Cotton Grass“ (Megascans, ab 3,99 USD), quixel.com/news „Quixel on Fab:
New Megascans and Megaplants“. Keine Quelle nennt Instanzen je m²; alle Dichten sind Richtwerte.

## 2. Regelwerk (`heide_tundra_regeln.json`) – Erklärung je Schicht

> **Stand Korrektur Runde 1.** Wo dieser Abschnitt Runde 0 beschreibt, gilt der Abschnitt „Korrektur Runde 1“: Der Biomfaktor ist durch
> Zuständigkeit plus 30-m-Saum ersetzt, die Klassen `grasbueschel`, `jungwuchs`, `heideblüte`, `totholz`, `stumpf` und `zweige` stehen
> jetzt in `mittelschicht_overrides` (Teil D), `wollgras` ist in Schicht 1, das Budget-Ziel ist 48 000 mit exakten Deckeln, und der
> Flechtenstein-Maßstab ist 0,6–0,9 (≤ 0,8 m).

**Gemeinsame Steuergrößen.** Dichte je Klasse in Instanzen je m² je Profil (`heide` / `tundra`), multiplikativ mit: Zuständigkeit (eigene Zelle 1, Saum linear
1 → 0 auf 30 m; Runde 0: Biomfaktor), Lagenfaktor (gewichtetes Mittel der `lage_*.r8`-Deckungen mit vier Gewichtstabellen `pflanze_trocken`, `pflanze_feucht`,
`stein`, `streu`; z. B. Heidekraut: Heide 1,6, Trockengras 1,1, Moos 0,7, Fels 0,1, Eis/Lava 0), Hang (voll bis `hang_voll_bis`, null ab
`hang_null_ab`; Steine 32/50°, Pflanzen 25–30/38–42°, Wasserkante 15–20/26–32°), Höhenstufen nur im Tundra-Profil (Bäume 240→300 m,
Sträucher 320→380 m, Zwergstrauch 460 m, Gras 520 m; Heide-Profil ohne Grenze), Schnee-Lage (Pflanzen ×0,15, Steine ×0,6 bei voller
Deckung), Kronendach aus Bestands-/Witcher-/Houdini-Bäumen (Box 9 m, Lichtpflanzen ×0,25 unter Kronen; Steine/Bäume ausgenommen),
Exposition (Höhe minus Gauß 40 m, normiert auf 8 m: +1 Kuppe, −1 Mulde; Flechtenstein +80 %, Krüppelkiefer +60 %, Wacholder +30 %),
Mulde (Gauß 12 m; Jungwuchs ×1,5, Kiefern-Gruppen ×3), Wassernähe (Jungwuchs ×2,5/40 m, Moorbirke ×3/45 m, Totbaum ×2/30 m), Baumnähe
(Zweige ×2,5 in 12 m, Totholz ×2 in 15 m). Sperren: Laub+Nadeln ≥ 0,6 → ×0,15 (G4),
Lavafels/Lavasand ≥ 0,3 und Eis ≥ 0,3 → 0; Wüstenfelder C3 C4 D3 D4 D5 E3 E4 E5 → ×0,7, nur tundra/heide-Zellen ohne Saum, Sand+Sandstein linear 1→0 bis 50 %
Deckung, darüber gesperrt, kein `entfernen`. Abstände: 2,5 m Kleinzeug / 4 m Bäume, Krüppelkiefern, Totholz zu Wegen; 5 m zu Orten;
0,3–2 m zu Wasser je Klasse; 1,5 m zu Bestandsstämmen, 1 m zu sonstigen Bestandsinstanzen (Witcher, Mittelschicht, Felsgruppen, Ufer);
neue Bäume 4–6 m zu Bestandsbäumen und untereinander (grobes Raster 0,7 × Abstand). Gruppen: Zentren = Dichte/Gruppenmittel,
Mitglieder im Radius, erneut gegen Sperrmaske geprüft. Zufall: Hash aus absoluter Rasterkoordinate, Seed 3311 und Klassenkanal →
deterministisch und nahtlos über Feldgrenzen (Fenster Feld + 64 m).

**Flecken.** Drei Wertrausch-Felder auf absolutem Gitter (2 Oktaven, Smoothstep-Schwelle): `heidekraut` Skala 26 m, Schwelle 0,55,
weich 0,12 (Deckung ≈ 35 %); `gras` 40 m, Schwelle 0,35, weich 0,25 (breite, weiche Grasflächen zwischen den Heideflecken);
`wollgras` 14 m, Schwelle 0,6 (Wollgras-Horste am Tümpel, nicht als Ring).

**Schicht `0 boden`** (Sichtweite 5 000–15 000 cm, keine Kollision):
- `kiesel` (SmallStonesPack_01–14 ohne 05/10/12, stone_04/05/06/08): tundra 0,035, heide 0,014/m², Gruppen 3–9 in 1,6 m, Maßstab
  0,9–1,6, 40 % eingegraben, voll auf Normale gekippt, Hang bis 50°. Niedrigste Priorität → wird zuerst ausgedünnt.
- `flechtenstein` (< 0,8 m: LichenedForestBoulder_01, mountain_rock_small_01_1/2/4/5, mountain_rock_big_01_2/3, Nordic_Forest_Rock_Small
  xjijbgx; heide: s_rock_01–03, stones_01_3): tundra 0,009, heide 0,004, Gruppen 2–6 in 2,2 m, Kuppen +80 %, 38 % eingegraben,
  Schatten an, Sichtweite 15 000. Flechten über Material-Auflage (Teil C `M_EL_Fels_Auflage`, Flechten-Variante).
- `streumatte` (DeadLeaves_12–14, dead_grass_01–03 als Torf-/Streu-Stellvertreter): 0,008–0,009, Gruppen 1–3, Lagen `streu` (Heide,
  Trockengras, Moos 1,0–1,2), Sichtweite 5 000.
- ~~`zweige`~~ (DryBranches_01/04/05/07, mountain_branch_01_01/02): 0,003–0,004, ×2,5 in 12 m um Bäume. **Seit Runde 1 → Teil D `totholz_ast`.**

**Schicht `1 mittel`** (0,3–3 m; Runde 1: nur noch heidekraut, wacholder, kruepelkiefer und wollgras, die übrigen → `mittelschicht_overrides`):
- `heidekraut` (heath_A/B_01, forest_heather_01/simple_01, billberry_01/02; tundra: heath_A/B, lingonberry_01/02, billberry_dry_01,
  billberry_03, rhododendron_01): 0,07 (heide) / 0,055 (tundra) **innerhalb der Flecken** → Feldmittel ≈ 0,02–0,025/m²; Gruppen 4–12 in
  2,5 m, Maßstab 1,1–1,9 (die 0,2–0,5-m-Netze lesen so als Polster; `GT_Heide`-GPU-Gras bleibt der Teppich darunter), Sichtweite 12 000.
- `grasbueschel` (Tundra_Grass VarA/C/D/F/G/H 0,3–0,7 m, grass_03_A/B 1,06 m; heide: grass_bush_01/03/04, grass_meadow_03/06/08 bis
  1,6 m): 0,028–0,03 in `gras`-Flecken, Gruppen 3–8, Maßstab 0,8–1,4 → Höhenstaffel 0,3–1,6 m.
- `wacholder` (Stellvertreter: dwarf_pine_small_01/02, medium_01/03, rhododendron_02; heide: sea_buckthorn_03–06 grau-grün, beach_rose_04/06,
  dwarf_pine_small_01): 0,0022–0,0028, Gruppen 1–5 in 3 m, Kuppen +30 %, Sichtweite 30 000, Schatten an.
- `kruepelkiefer` (pine_beach_crooked_01/02, dwarf_pine_big_01/02, pine_beach_short_01/02): 0,0004–0,0009, Gruppen 1–3 in 4 m, Kuppen +60 %,
  Höhenstufe Strauchgrenze (380 m, Abnahme ab 320 m), **Wind**: lee-Neigung 4–12° bei expo > 0,25, **Kollision** ab 2 m Netzhöhe,
  Sichtweite 35 000.
- `jungwuchs` (Hornbeam_Sapling_01/02, Seedling_01/02, grey_willow_02/03; tundra: Forest_pine_plant_01/02, grey_willow_01/02): 0,0005–0,0008,
  Gruppen 2–5, Wasser ×2,5 (40 m), Mulde ×1,5, Lagen `pflanze_feucht`.
- `heideblüte` (beach_rose_02/03/04_with_pink_flowers, Maßstab 0,6–0,9): nur heide 0,0012 in Heideflecken, Gruppen 2–4 – Farbakzent bis
  ein Calluna-Blütennetz da ist.
- `totholz` (beach_driftwood_01 gebleicht, Forest_pine_04/08_log, dead_log_03/04, OldTreeBranch_06): 0,00035–0,0004, Yaw hangabwärts ± 25°,
  28 % der Netzhöhe eingegraben, **Kollision** ab 0,3 m, ×2 in 15 m um Bäume, Sichtweite 40 000.
- `stumpf` (pine_stump_01–03, BirchTreeStump_01): 0,00015–0,0002, 10 cm eingegraben.

**Schicht `2 baum`** (Kollision, Sichtweite 0, Kippen ≤ 0,08, Eingraben 15 cm):
- `einzelkiefer` (Forest_pine_01, pine_beach_01_A/B, 02_A, 03_A, 04_A): Feldmittel 0,00012–0,00016; auf Kuppen einzeln, klein (×0,6–0,85)
  und windschief; in Mulden (Krümmung > 0,35) Gruppen 2–5 in 9 m, ×3 Dichte, größer (×0,95–1,25); Baumgrenze 300 m (Abnahme ab 240 m);
  6 m Mindestabstand; Hang ≤ 38°.
- `moorbirke` (einziges Birkennetz Big_Tree_birch_01, 11,5 m, kein Nanite, 28 k Dreiecke, auf 0,6–1,0 → 7–11 m): 0,00005–0,00009,
  Gruppen 2–4 in 7 m, Wasser ×3 (45 m), Mulde ×1,5, in Tundra nur < 250 m, Hang ≤ 32°.
- `totbaum` (DeadTree_01/02, Dead_Tree qlEtl): 0,00003–0,00004, Wasser ×2 (30 m), bis Strauchgrenze.

**Schicht `5 wasserkante`** (Band um `karte_wasser.r8`; Moortümpel, Bäche):
- `wollgras` (Tundra_Grass VarB/C/G, grass_meadow_08 hoch skaliert 0,9–1,4): 0,12/m² im Band 0,5–9 m **und** ×0,35 auf Moos/Schlamm ≥ 50 %
  (nasse Moorflächen ohne offenes Wasser), in `wollgras`-Flecken, Gruppen 4–10, Hang ≤ 30°.
- `seggen` (ToadRush_011–013 kleine Varianten ≤ 1,5 k Dreiecke; heide zusätzlich Rohrkolben_Jung_1/3): 0,05–0,07 im Band 0,3–4 m, Gruppen 3–8.
- `moorstein` (NordicBeachRock_01, SmallStonesPack_05/10/12, mountain_rock_small_01_3): 0,025–0,04 im Band 0,2–3 m, 45 % eingegraben –
  **entfällt**, wenn `ufer/foliage_<Feld>/` existiert (Ufer-Ebene `FT_EL_UF_*` liefert dann die Kiesel).
- `treibholz` (beach_driftwood_01, dead_log_03): 0,0015–0,002 im Band 0,5–5 m, 30 % eingegraben.

**Budget** (`budget`, Runde 0; Runde 1: Ziel 48 000, Kollision und Deckel exakt, siehe oben): Ziel 45 000, harte Grenze 60 000 je Feld, ≤ 3 000 mit Kollision. Ausdünnung deterministisch (Hash je Instanz)
von hinten nach `prioritaet`: Kiesel → Streumatte → Zweige → Grasbüschel → Flechtenstein → Heidekraut → Treibholz → Moorstein →
Wollgras → Seggen → Heideblüte → Jungwuchs → Stumpf → Totholz → Wacholder → Krüppelkiefer → Totbaum → Moorbirke → Einzelkiefer; je
Klasse im ersten Durchgang höchstens auf 25 % gekürzt, danach proportional bis zur harten Grenze; Kollisionsklassen separat.

**Overrides für Teil C/D** (gleiche Schlüssel wie `felsgruppen_regeln.json` / `spuren_regeln.json`; nicht vom Heide-Planer gesetzt):
- `felsgruppen_overrides.heide`: Palette `heide` neu (hero: Meadow Rock_05, Big_Rock_01/02, IcelandicBoulder_03, NordicBoulder_01;
  block: Meadow Rock_01–07, IcelandicBoulder_01/02, Granite_Rock pkeeM/pjtsT), Biomfaktor 0,7, Klassen `band`, `wand`, `fuss`, `blockstrom` aus (Flachheide), `kuppe` p 0,9 mit Umkreis 40 m, **neu `findling_frei`**:
  freistehende **Findlinge** 3–6 je km² auf Hang 0–14°, 80 % Hero, 40–55 % eingegraben, nie näher als 120 m zueinander, Flechten-Auflage
  (Weiß-Grau 0,15 + Gelbgrün 0,05 statt Moos).
- `felsgruppen_overrides.tundra`: Palette `tundra`, Faktor 1,0, `blockstrom` ×1,3, **neu `blockfeld`** (Felsenmeer/Frostschutt): Raster
  12 m auf Hochflächen > 280 m mit Hang 6–24°, p 0,35, 2–5 Blöcke + 6–14 Steine + 10–20 Kiesel, gleich groß, kantig, 40–55 % eingegraben;
  `findling_frei` 4–8 je km²; Auflage `flechten_schnee` (Flechten Südseite, Schnee Nordseite/Simse nach Normale).
- `spuren_overrides.heide`: **Steinmauern** statt Holzzäune (25–90 m, 2–4 je km², 4 Lagen 0/0,26/0,5/0,72 m mit 100/90/60/30 %,
  Steinabstand 0,42 m, 12 % Lücken, hang- oder wegparallel, mountain_rock_small_01_*, s_rock_01/02); **neu `pferch`** (Schafpferch 8–14 m Rechteck/Ring aus Trockenmauer, 1 Öffnung 1,8 m, 1–2 je Ort im Ring
  40–220 m, 0–1 frei je Feld ≤ 90 m vom Wasser, Hang ≤ 8°, Beiwerk Trough_01a, Hay_02, wooden_pales_1_01); **neu `torfstich`** (0–3 je Feld
  auf Moos ≥ 35 %/Schlamm ≥ 20 %, ≤ 60 m vom Wasser, Hang ≤ 4°, 6–10 × 12–24 m, Tiefe 60 cm als Punktliste für Höhenpass/Decal, 1–3
  Soden-Stapel Pile_WoodLog_02a × 0,7–0,9); **neu `steinkreis`** als Blickziel (1 je Feld auf Kuppe mit Prominenz ≥ 10 m, Radius 6–11 m,
  5–9 Steine 1,3–2,6 m hochkant, 25 % umgefallen, Akteure mit Kollision); Steinmänner 3 je km²; Schreine 50 % der Wegkreuze
  (Sviatovid_Stone); Wegsaum-Einfriedung als Mauer; keine Obstgärten; Feldstreifen max 4 je Ort; Schäfer-/Torfhütte fehlt (Einkaufsliste).
- `spuren_overrides.tundra`: verfallene Mauern (15–50 m, 0–2 je km², 3 Lagen, 25 % Lücken, nur < 300 m), Sommerweide-Pferch 0–1,
  Torfstich 0–2 (< 250 m), Steinkreis 5–7 Steine mit 40 % umgefallen, **Steinmänner 8 je km² und alle 70–110 m am Weg** (Wegmarken in
  Nebel/Schnee), Schreine 30 %, keine Obstgärten, Feldstreifen max 1 je Ort / 2 je Feld, Jagdhütte fehlt.

### 2.1 Planer `heide_tundra_plan.py` (FORMAT §3/§5)

- **Aufruf:** `python -I scripts/heide_tundra/heide_tundra_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
  [--entfernen "p1,p2"]`; Regeln standardmäßig `heide_tundra_regeln.json` neben dem Skript. Keine Unreal-Importe; NumPy, Pillow nur
  für `--bild` (ohne Pillow PPM); numba wird gemeldet, nicht gebraucht.
- **Lesen:** `hoehe.f32` per `np.memmap`, nur Fenster Feld + 64 m (NY = 7057, NX = 9577; J-Spalte bei 9577 geklippt → J-Felder 505 m
  breit); `karte_*.r8`, `lage_*.r8` (22 Namen), `eigner.r8` + `welt.json` optional mit Warnung; Bestand aus `bestand/`, `witcher/`,
  `mittelschicht/`, `felsgruppen/` (Feld + 8 Nachbarn; Bäume vs. Sonstige über `rolle`/`gruppe`/Name), `ufer/foliage_<Feld>/`,
  `instanzen/instanzen.json` (fehlt → Hinweis im Protokoll und in `plan.json["hinweise"]`); `daten/netze.csv` aus production, neben dem
  Skript oder aus der Repo-Vorlage (Pfadprüfung: fehlende Netze werden mit Warnung gestrichen; Netzhöhen für Eingraben/Kollisionsschwelle).
- **Rechnen:** Hang/Normale aus Gauß(2 m)-Gradient, Exposition, Mulde, Wasserdistanz (Jump-Flooding), Dilatation für Abstände,
  Kronendach als Box-Faltung, Flecken als Wertrauschen; je Klasse Dichtekarte → Bernoulli-Zug der Zentren → Mitglieder → Attribute
  (Maßstab, Wind, Netzwahl je Profil, Eingraben, Quaternion aus Normale + Lee-Lehnen + Yaw). Kein Python-Loop über Zellen.
- **Schreiben:** `export/unreal/welt/heide_tundra/<Feld>/<Netz>.f32` (alte f32 vorher gelöscht) und `plan.json` mit `stand, feld,
  ebene, instanzen, dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene, schicht, klasse}, ft_ordner, ft_praefix,
  entfernen (Runde 1: immer, leer in Wüstenfeldern), biome_fenster, zellen_zustaendig, biome_eigen, kollision_anzahl, klassen, schichten, profil_anteil_feld,
  statistik{anteil_eigen_fenster, biom_quelle, saum_m, ausserhalb_eigener_zellen, quellen_bestand, …}, hinweise, ungetestet`. Nur Instanzen **im Feld** werden geschrieben (Rand dient der Nahtlosigkeit).
  `--bild` → `docs/pruefung/heide_tundra/<Feld>.png` (1 px = 1 m; Profil heide violett-grau / tundra grün-grau mit Schummerung,
  Wasser blau, Weg gelb, Ort rot, Sand-Sperre beige, nicht planbare Biome dunkel, Klassen nach `farbe`, Bäume/Krüppelkiefern/Totholz 3 × 3 px).

## 3. Abgrenzung zu vorhandenen Ebenen: ergänzen, nicht ersetzen

| Ebene | Verhältnis zur Heide/Tundra-Ebene | `entfernen`? |
|---|---|---|
| Witcher-Bewuchs `FT_EL_WIT_*` | Andere Netze, andere Steuergrößen (Flecken, Höhenstufen, Exposition); WIT-Instanzen als Sperrpunkte (1 m), WIT-Bäume als Kronendach | nein. Nach Sichtung in D2/G5 `FT_EL_WIT_maple_bush_0,FT_EL_WIT_Elderberry_` per `--entfernen` (Laubgebüsch wirkt fremd) |
| Wald-Bestand `FT_EL_BST_*` | Kronendach → Lichtpflanzen ×0,25; neue Bäume 4–6 m Abstand; in G4 (Laub 75 %) sperrt die Waldlage zusätzlich ×0,15 | nein |
| Mittelschicht `mittelschicht/` (Teil D) | **Runde 1 geklärt (Konventionen §4):** Teil D setzt alle generischen Klassen (Grasbüschel, Jungbaum, Strauch, Beere, Totholz, Farn, Hochstaude, Pilz) mit Palette/Faktoren aus `mittelschicht_overrides`. B3 setzt nur Heidekraut-Flecken, Wacholder, Krüppelkiefern und Wollgras. Reihenfolge: felsgruppen → heide_tundra → mittelschicht → spuren | nein (Witcher-Laubgebüsch: `_entfernen_vorschlag`) |
| Felsgruppen `felsgruppen/` (Teil C, `FT_EL_FG_*`) und Felsschalen `FT_EL_FS_*` | Alle Felsen > 0,8 m kommen von dort (Overrides §2: Findlinge, Blockfelder, Kuppen); diese Ebene setzt nur Steine < 0,8 m und meidet Felsgruppen-Instanzen (1 m) | nein |
| Ufer `FT_EL_UF_*` | Moorsteine entfallen, wenn `ufer/foliage_<Feld>/` existiert; Pflanzen der Wasserkante bleiben (Band 0,3–9 m) | nein |
| Spuren `spuren/` (Teil D) | Steinmauern, Pferche, Torfstiche, Steinkreise über `spuren_overrides`; diese Ebene setzt keine Spuren | nein |
| Wüste `FT_EL_WU_*` (C3, D3, E3) | nur ergänzen: ×0,7, nur tundra/heide-Zellen, Sand/Sandstein-Sperre, `entfernen` wird auch per CLI ignoriert | nein |
| Landschafts-Gras `GT_*` (`GT_Heide`, Trockengras) | bleibt Teppich 0,2–1,2 m; Heidekraut-Polster (×1,1–1,9) und Büschel bis 1,6 m sind die Stufe darüber | nein |

Begründung: Hauptfehler laut Bildkritik ist „jede Fläche trägt genau einen Maßstab“; die Ebene fügt die fehlenden Stufen (Flecken
20–60 m, Polster 0,3–0,8 m, Sträucher 1–3 m, Einzelbäume) hinzu. Entfernen erst, wenn im Editor doppelte Gebüsche sichtbar sind.

## 4. Testanleitung

**Rauchtest Cloud Runde 0 (gelaufen am 10.10., wiederholt nach dem Sitzungsabbruch; Rauchtest Runde 1 siehe Abschnitt „Korrektur Runde 1“).** Mini-Produktionswurzel mit `hoehe.f32` in voller
Größe 7057 × 9577 (memmap; D2-Fenster: welliges Hochland 159–355 m, 25 % über 300 m, 62 % > 30° Hang; G5-Fenster: flache Heide 8–38 m),
`karte_wasser.r8` (zwei Moortümpel 32 + 20 m Radius in eingeebneten Moorbecken), `karte_weg.r8` (Diagonale 4 m), `karte_ort.r8`
(60 × 60 m), `eigner.r8` (D2 = 7 tundra, G5 = 12 heide) + `welt.json`, `lage_Heide/Trockengras/Moos/Geroell/Schnee/Fels/Wiese/Sand.r8`,
`bestand/D2` (300 Kiefern), `witcher/G5` (400 maple_bush als Sonstige), `ufer/foliage_D2` (150 Kiesel), `daten/netze.csv`.
Ergebnis `python -I scripts/heide_tundra/heide_tundra_plan.py D2 G5 --bild --basis .` (Python 3.13, NumPy 2.5, 4 Kerne, ohne numba):

| Feld | Instanzen (vor Budget → nach) | Kollision | Netze | boden | mittel | baum | wasserkante | Laufzeit |
|---|---|---|---|---|---|---|---|---|
| D2 | 51 373 → 44 905 | 409 | 119 | 26 384 | 18 335 | 107 | 79 | 4,8 s |
| G5 | 69 711 → 44 976 | 738 | 102 | 9 465 | 34 925 | 298 | 288 | 4,7 s |

Größte Klassen D2: Kiesel 13 002, Heidekraut 8 266 (31 % der Zellen per Heide-Lage ≥ 40 % als Heide-Profil), Grasbüschel 7 671,
Flechtenstein 7 662, Wacholder 1 476, Krüppelkiefer 413, Einzelkiefer 83 (nur unter 300 m), Wollgras 22; Moorstein übersprungen (Ufer-Ebene
vorhanden). G5: Heidekraut 20 922, Grasbüschel 9 664, Flechtenstein 3 473, Kiesel 2 827 (auf 25 % gekürzt), Wacholder 2 307, Jungwuchs 616,
Krüppelkiefer 454, Heideblüte 388, Wollgras 196, Einzelkiefer 183, Moorbirke 83, Seggen 65, Totbaum 32, Moorstein 21. Prüfskript: alle 221 f32 durch 10 teilbar, Anzahl = `plan.json`,
Schema vollständig (je Datei `pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene`; Kopf mit `ebene`, `ft_ordner`,
`ft_praefix`), Quaternionen normiert (|q|−1 ≤ 1,2·10⁻⁷), **0 Instanzen auf Wasser/Weg/Ort, 0 außerhalb des Feldes**, z − Gelände
−1,17 m (Flechtensteine 38 % eingegraben, ×1,5 skaliert) bis +0,86 m (Bilinear-Artefakt an 40°-Hängen der Synthetik; auf G5 −0,38 …
+0,25 m). Zwei Läufe byte-identisch (MD5 über 218 Dateien); `--faktor 0.5` → G5 34 593. Fehlerfälle (Feld K9, fehlende Basis, fehlende
Regeldatei) → klare Meldung und Exit; D3 (Wüstenfeld, nur 100-m-Landstreifen aus dem D2-Rand) 3 420 Instanzen mit Faktor 0,7; J7
(Randspalte, Fenster 569 × 1073) 0 Instanzen in 1,1 s; E2 mit `biome_je_feld.json` → eigner 0 als gletscher (×0,35), 1 583 Instanzen.
Prüfbilder `docs/pruefung/heide_tundra/D2.png`, `G5.png` (1008 × 1008): Heideflecken violett mit weichen Rändern, Kiesel/Flechtensteine
als gelbe Streu an Hängen, Bäume nur in Mulden, Wollgras weiß und Binsen am Tümpel, Ort rot, Weg gelb.

**Erwartete Instanzzahlen je Feld – Stand Runde 0** (Richtwert, Spanne ±35 %; Grundlage Biom-/Lagenanteile in `biome_je_feld.md`). Seit
Runde 1 gelten kleinere Werte ohne Fremdbiom-Anteile und ohne generische Mittelschicht, siehe `erwartung_je_feld` und den Abschnitt
„Korrektur Runde 1“; G4 liegt bei 500–4 000, A5/E1/C6 bei 0:

| Feld | Biom-/Landanteil | gesamt | boden | mittel | baum | wasserkante | Kollision |
|---|---|---|---|---|---|---|---|
| D2 | tundra 47, gletscher 34 (×0,35), fjord 19 (×0,5); 57 % steil | 28 000–52 000 | 14 000–26 000 | 12 000–22 000 | 60–250 | 100–800 | 150–500 |
| G5 | heide 77, dschungel 22 (×0); flach, Wasser 3,9 % | 38 000–58 000 (Budget greift) | 8 000–14 000 | 28 000–38 000 | 200–450 | 600–2 500 | 500–1 100 |
| F5 | heide 74, aue 25; Land 58 %, Wasser 9,7 % | 15 000–35 000 | 4 000–9 000 | 10 000–22 000 | 100–300 | 1 500–5 000 | 200–600 |
| D3 (Wüste ×0,7) | tundra 73, Sand 32 % | 10 000–28 000 | 4 000–12 000 | 5 000–14 000 | 30–150 | 300–1 500 | 50–250 |
| E3 (Wüste ×0,7) | tundra 60, Sand 52, Schnee 17 % | 5 000–16 000 | 2 000–7 000 | 2 500–8 000 | 10–80 | 100–600 | 20–150 |
| C3 (Wüste ×0,7) | tundra 27 (aue ×0 im Wüstenfeld) | 3 000–10 000 | 1 000–4 000 | 1 500–5 000 | 10–60 | 50–400 | 10–100 |
| C2, E2 | tundra 21 / 11, gletscher ×0,35, Schnee 47 % (E2) | 3 000–14 000 | 1 500–7 000 | 1 500–6 000 | 10–60 | 50–500 | 20–120 |
| F4 | heide 21, aue 79 (×0,4), Land 54 % | 6 000–16 000 | 2 000–5 000 | 4 000–10 000 | 30–120 | 200–1 200 | 50–200 |
| G4 | heide 22, elfenwald 76 (×0,15), Laub 75 % (×0,15) | 1 500–6 000 | 500–2 000 | 1 000–4 000 | 10–40 | 50–300 | 10–60 |

**Prüfkameras (Feld, Position, Blick):**
1. **G5 Heidefleck, Augenhöhe 1,7 m**, Kuppe 200 m nordöstlich des Moortümpels, Blick nach Südwesten in tiefem Seitenlicht (Vergleich
   BACH3_G5). Erfolg: Heidekraut-Polster lesen als violett-braune Flecken 20–60 m mit weichem Rand (kein harter „Heidefleck“), dazwischen
   Grasbüschel in 2–3 Höhen, alle 10–20 m ein Wacholder/Sanddorn, Findling mit Flechten im Mittelgrund; innerhalb 10 m mindestens ein
   Objekt in 0,5–3 m Höhe.
2. **G5/F5 Moortümpel, 2 m Höhe am Ufer**, Blick über das Wasser gegen die Sonne. Erfolg: Binsen 0,3–4 m, Wollgras-Horste 0,5–9 m in
   Flecken (nicht als Ring), Treibholz und 1–2 Moorbirken am Rand, Totbaum als Silhouette, nichts im Wasser, keine Pflanze schwebt.
3. **D2 Kuppe 280 m, 1,7 m**, Blick nach Nordwesten (gegen den Wind). Erfolg: Einzelkiefern klein und leewärts (SO) geneigt, Krüppel-
   kiefern in 1–3er-Gruppen, Flechtensteine auf der Kuppe dichter, Heide/Trockengras-Flecken, Schnee ab ~330 m ohne Pflanzen.
4. **D2 Mulde 220 m, 3 m Höhe.** Erfolg: Kiefern-Gruppe 2–5, größer als auf der Kuppe, Jungwuchs/Grauweide, Zweige und Totholz um die Stämme.
5. **D2 Hochfläche > 300 m, Draufsicht 150 m.** Erfolg: keine Bäume über 300 m, Blockfelder (Teil C) mit Kiesel-/Flechtenstein-Saum.
6. **Nahtprüfung** G5/F5 und D2/C2 (Draufsicht 100 m): Flecken und Gruppen laufen über die Feldgrenze, keine Dichtesprünge.

**Erfolgskriterien in Zahlen:** Instanzen je Schicht in der Tabelle; Kollision < 3 000 (D2/G5 Rauchtest 409/738); Setzer-Zeit je Feld
< 5 min (≤ 124 Foliage-Typen `FT_EL_HT_*`, davon 15 Baum-/Stamm-/Krüppelkiefer-Typen mit Kollision); Nicht-Nanite-Netze
(Big_Tree_birch_01, pine_beach_*, Mountain-Gräser) auf LOD-Übergänge geprüft; PNG und `plan.json` je Feld vorhanden.

## 5. Einkaufsliste fehlender Assets (frei bevorzugt, Stufe High 4K)

| Was | Exakter Name (Fab/Megascans), Befund | Stufe | Wofür | Status |
|---|---|---|---|---|
| **Heidekraut in Blüte** (Calluna vulgaris, Erica cinerea) | Fab-Suche „heather calluna“ beim Verkäufer Quixel Megascans ohne Treffer **[Suchauszug]**; Drittanbieter „Heather Plant Pack“ direkt auf Fab prüfen | High, Nanite | `heidekraut` (Ersatz heath_A/B, billberry), `heideblüte` (Ersatz beach_rose_pink) – der violette Skellige-Akzent | **offen**, wichtigste Lücke |
| **Wacholder** (Juniperus communis, Säule + Kriechform 0,5–2 m) | nur Megascans-Zweig-Atlanten „Desert Western Tree Branch Juniper“ gefunden, keine Pflanze **[Suchauszug]**; Fab „Juniper bush Nanite“ prüfen | High | `wacholder` (Ersatz dwarf_pine, sea_buckthorn) | offen |
| **Ginster** (Ulex europaeus/Cytisus, gelb blühend 1–2 m) | kein Treffer; Megascans „Gorse“ bei Erscheinen prüfen | High | `wacholder`-Palette heide, Farbakzent gelb (Skellige-Frühling) | offen |
| **Wollgras** (Eriophorum) | Quixel Megascans **„Cotton Grass“** auf Fab, ab 3,99 USD **[Suchauszug: fab.com Seller Quixel Megascans]** | High | `wollgras` (Ersatz Tundra_Grass hoch skaliert) – weißer Moor-Akzent | **kaufen** (Lizenz im Fab-Konto prüfen) |
| **Moorbirke** (Betula pubescens, 6–12 m, mehrstämmig, Nanite) | Fab „Birch tree Nanite“ Drittanbieter; Megascans Trees „Silver Birch“ bei Erscheinen | High | `moorbirke` (Ersatz Big_Tree_birch_01 ohne Nanite, 28 k Dreiecke) | offen |
| **Flechtensteine** (Granit 0,3–1,5 m, ohne Moos) | nur LichenedForestBoulder_01 vorhanden; Fab „lichen rock“ prüfen | High | `flechtenstein`, `findling_frei`; bis dahin Flechten über `M_EL_Fels_Auflage` | offen (Material reicht vorerst) |
| **Trockensteinmauer-Segmente** (2–4 m, Ecke, Ende, verfallen) | Fab-Suche „dry stone wall sheepfold“ ohne Treffer; gefunden nur Ziegel-/Fachwerk-Kits (Massive Realities) und dekogon „Fences VOL.3“ (Nanite-Zäune) **[Suchauszug]** | High, Nanite | `mauer`, `pferch`; heute Einzelsteine (7 je 3 m, teuer) | **offen**, zweitwichtigste Lücke |
| **Schäfer-/Torfhütte, Jagdunterstand** | kein Netz im Inventar (Village/Town-Kits haben nur Dorfhäuser); Fab „shepherd hut medieval“ prüfen | High | `huette` (Spuren-Override) | offen, Ersatz Holzstapel + Pfähle + Karren |
| **Zwergbirke / Weidengebüsch 0,3–1 m** (Taxonomie-Lücke tundra) | Megascans „Dwarf Willow“/„Arctic Willow“ prüfen | High | `jungwuchs`-Palette tundra (Ersatz grey_willow, Forest_pine_plant) | offen |
| **Torfsoden-Stapel, Torfstich-Decal** | kein Treffer; eigenes Netz (Quader 0,3 × 0,15 × 0,1 m, Stapel) + Decal | – | `torfstich` | eigenbau |

Kostenhinweis aus `boden-kleinzeug-gras.md`: Megascans-Assets sind seit 2025 je Asset kostenpflichtig, sofern nicht vor dem
31.12.2024 beansprucht; Fab-Konto zuerst prüfen.

## 6. Offene Punkte und Annahmen

1. **Baumgrenze 300 m** ist aus D2-Lagenanteilen (Schnee 9 %) abgeleitet, nicht aus einem Klimamodell; wenn Ferat auf E2/C2 Bäume bis
   350 m will, `hoehe.tundra.baumgrenze_m` und `strauchgrenze_m` anheben. Heide-Profil hat keine Höhenstufe (Felder < 110 m).
2. ~~**Profil-Zuordnung über Lagen**~~ (Runde 1 gestrichen; heute schaltet Heide ≥ 40 % nur in tundra-Zellen das Profil, `profil_nach_lage`). Runde 0: Heide ≥ 40 % → heide, Trockengras ≥ 50 % über 120 m → tundra, konnte in C2/D1/E1 (Heide 4–10 %)
   kleine Heideinseln erzeugen; wenn unerwünscht, `lagen_biom_hinweis` leeren.
3. ~~**Überschneidung mit der Mittelschicht (Teil D)**~~ (Runde 1 entschieden: Konventionen §4, `mittelschicht_overrides`). Runde 0: beide Planer setzen Zwergstrauch und Grasbüschel in heide/tundra. Entscheidung
   nötig (Vorschlag §3: in den zehn Feldern nur `heide_tundra`, Mittelschicht-Biomfaktor heide/tundra = 0).
4. **Witcher-Ebene / `instanzen.json`**: Bäume werden nur am Namen bzw. an `rolle`/`klasse` erkannt (pine, beech, birch …);
   für `instanzen.json` ist der Dateiname `datei` oder `<name>.f32` angenommen.
5. ~~**Netze in zwei Klassen**~~ (Runde 1: kein Netz mehr in zwei Planer-Klassen). Runde 0: (driftwood/dead_log in `totholz` mit und `treibholz` ohne Kollision; Tundra_Grass VarC/G und
   grass_meadow_08 in `grasbueschel` und `wollgras`): Setzer übernimmt die Einstellungen der ersten Klasse – also Kollision für alles
   Treibholz (6 Instanzen, unerheblich) und Sichtweite 10 000 für Wollgras. Bei Bedarf eigene Wollgras-Netze nach dem Kauf.
6. **Eingraben nach Netzhöhe** (Flechtensteine 38 %, Kiesel 40 %, Totholz 28 %) setzt Pivot in Netzmitte voraus; `netze_masse.json`
   hat für die Mountain-/Meadow-Steine Bounds – nach dem ersten Setzen prüfen, ob Steine schweben oder versinken, dann
   `eingraben_anteil` anpassen.
7. **Wüstenfelder** (Runde 1: C3 C4 D3 D4 D5 E3 E4 E5, ohne Saum): nur tundra/heide-Zellen; die aue-Anteile in C3 bleiben dem Aue-Planer (dort ×0,6). Der eigene Wüsten-
   Planer bleibt unberührt (kein `entfernen`, auch nicht per `--entfernen`).
8. **Dichten sind Richtwerte** (keine Quelle nennt Instanzen je m²). Erster Kalibrierschritt: G5 und D2 setzen, Kameras 1 und 3,
   `--faktor 0.7 … 1.3` vergleichen. In Runde 0 lief G5 ins Budget (69 700 → 45 000). Seit Runde 1 (Schicht 1 nur Sonderformen,
   Ziel 48 000) bleibt das synthetische G5 mit 36 674 darunter; wenn mehr Heidekraut gewünscht ist, `budget.ziel_instanzen_je_feld`
   bis 52 000 anheben (Deckel 60 000 bleibt hart).
9. **Rauchtest-Grenzen**: synthetisches Rauschen ohne echte Grate/Blockfelder, keine `witcher/`-Rollen, keine `instanzen.json`,
    Sand-Sperre nur ohne Sandlage durchlaufen. Erstes Echtdaten-Feld daher G5 (flach, Heide) neben D2 (Höhenstufen, Wind).
10. **Status-Datei** `verteilung-STATUS.md` wurde nicht verändert (Koordinator); B3 kann auf „fertig (ungetestet mit Echtdaten)“ gesetzt werden.

## Korrektur Runde 2 (10.10.2026)

- Keine gesperrten Netze und keine Platten im Planer. `kiesel` hat `teppich_sperre` (nur auf/bis 6 m um Kies-/Geroell-/Fels-Lagen >= 80/255, bis 3 m am Weg, bis 5 m am Wasser); `flechtenstein`/`moorstein` unveraendert.
- Rauchtest synthetisch D2: Kiesel 14 302 -> 7 302, Hangteppich-Kiesel 6 311 -> 0; Feld 38 842 Instanzen, zwei Laeufe byteidentisch, Log ASCII, 6 s.

## Korrektur Runde 3 (10.10.2026)

- Rote `/Game/AncientContent/…/SM_IcelandicBoulder_01/02/03` entfernt (nur noch canyon/oedland/wueste/lava): `felsgruppen_overrides.heide.paletten_neu.heide` hero `_03` -> `/Game/Megascans/…/SM_MossyForestBoulder_04` (3,3 m), block `_01`+`_02` -> `SM_MossyForestBoulder_03` (2,0 m); `spuren_overrides.heide.steinkreis` ohne `_03` (bleiben 3 graue Netze 4,1–5,3 m, Hoehe wird ohnehin skaliert). Planer-Code unveraendert.

## Korrektur Runde 4 (10.10.2026): Meer fehlt in `karte_wasser`

- Ausgangslage: Der Planer setzte schon nur auf `hoehe > 0,05` und hatte deshalb keine Instanzen unter 0 m. Er zählte aber das Meer (eigner 0 = aue) im Biom-Anteil mit, ließ Kleinzeug, Wacholder und Heidekraut bis an die Wasserlinie und nutzte `karte_wasser` allein für Sperre und Abstand.
- Umgesetzt nach Konventionen §1b: `meer = hoehe < 0 & karte_wasser == 0`, `wasser_alle = karte_wasser > 0 | meer`. Landzellen-Bezug für `biome_fenster` (`biome_fenster_bezug`), Eigenanteil/Leerplan-Schwelle, Saum und `zellen_zustaendig`. Sperre und Abstand (`wasser_min`) sowie die Ufer-Kieselmaske laufen über den Abstand zu `wasser_alle`. Am Süßwasser bleiben das Wasserkante-Band (Seggen, Moorsteine, Treibholz, Wollgras an Moortümpeln) und `wasser_bonus` (Moorbirke, Totbaum).
- Neuer Block `meer` in `heide_tundra_regeln.json` (`tief_m` −0,3, `saum_hoehe_m` 0,3, `saum_m` 30). Unter −0,3 m nichts. −0,3…0 m nur `meer_rolle`, hier keine. 0…+0,3 m im Küstensaum (≤ 30 m zum Meer) nur Schicht 5 wasserkante oder `strand: true`.
- Schlussfilter: Er prüft die Geländehöhe bilinear am Instanzort und an der Küste z ≥ −0,3 m. `plan.json` meldet `meer_zellen` und `meer_gefiltert` (auch im Leerplan), `statistik` meldet `kuestensaum_zellen_feld` und `meer_gefiltert_je_klasse`.
- Rauchtest synthetisch (A5: Heide bis an einen Strand 0–0,3 m, Meer West nicht in `karte_wasser`, Fluss und Süßwassersee unter 0 m in `karte_wasser`; B5: Tundra an der Nordküste; J6 nur aue; Raster danach gelöscht):

| Feld | Gesamt vorher → nachher | Gelände < 0 m | 0…0,3 m Küstensaum vorher → nachher |
|---|---|---|---|
| A5 | 6 174 → 5 898 | 0 → 0 | 273 (Heidekraut 127, Kiesel/Flechtensteine 119, Streumatten 24, Wacholder 3) → 0 |
| B5 | 2 391 → 2 238 | 0 → 0 | 147 (Steine 85, Streumatten 40, Wacholder 16, Heidekraut 5, Baum 1) → 0 |
| J6 | 0 → 0 (leer) | – | – |

`meer_gefiltert` 0, weil die Maske schon greift. Instanz-z < 0: vorher 6, nachher 0. Zwei Läufe byteidentisch, Log ASCII, `py_compile` ok, 6 s je Feld.
