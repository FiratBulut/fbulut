# `entfernen`-Filter der Biom-Planer (Auftrag 11, Projekt Eldarien, UE 5.8.3)

## Runde 3b: entfernen-Filter je Feld

Anlass ist `auftraege/verteilung-korrektur-runde3b.md`, letzter Absatz. Der lokale Setzer entfernt nichts ohne Freigabe. nordkueste und
dschungel werden erst ausgerollt, wenn geklärt ist, ob alte Bäume ersetzt werden. Die Begründung und die erwartete Zahl entfernter Bäume
gehören je Feld in den STATUS. Stand 10.10.2026. **Alle Zahlen unten sind Erwartungen ohne Echtdaten.** In der Cloud gibt es keine
`witcher/`- und `bestand/`-Instanzen. Die exakte Zahl liefert der Planer lokal (siehe 4.).

### 1. Wer setzt überhaupt `entfernen`? (grep in `antworten/skripte/*.py` und `*_regeln.json`)

| Planer | `entfernen` im Standardlauf | Inhalt | Bäume? |
|---|---|---|---|
| aue | **leer** (bestätigt) | `entfernen: ""`; Kikuyu-Gras nur als `entfernen_vorschlag`, ist aber ausgeschaltet; in Wüstenfeldern immer leer | nein |
| heide_tundra | **leer** (bestätigt) | `entfernen: {heide: "", tundra: ""}`; nur per `--entfernen` setzbar, in Wüstenfeldern ignoriert; Laubgebüsch steht nur als `_entfernen_vorschlag` | nein |
| wueste_ergaenzung | **leer** (bestätigt) | fest `''`, `kein_entfernen: true` | nein |
| sumpf, spuren, mittelschicht (eigene Regeln), hochgebirge | leer | sumpf hat zusätzlich eine 85-%-Sperre; hochgebirge hat nur `entfernen_vorschlag` | nein |
| **nordkueste** (vor 3b) | im Modus `ersetzen` (heute in jedem Feld ohne `bestand/`), wenn der Eigenanteil im Feld ≥ 85 % ist | `sm_forest_pine_0,fir_0,sm_pine_beach_0` | **ja** (Kiefern, Tannen) |
| **dschungel** (vor 3b) | G6, H6, I6, G7, H7, I7 immer, ohne Anteilsprüfung | `sm_vines_01a`; dazu über `mittelschicht_overrides.entfernen_je_feld` die Farne `sm_fern_01a,sm_fern_02a` | nein (Lianen, Farne) |
| elfenwald | aktiv bei Elfenwald-Anteil ≥ 50 % | Witcher-Kleinzeug; bei `--baum voll` auch Witcher-Haine | nur bei `voll`. In den Nordküstenfeldern H2, I3 und I4 liegt der Elfenwald-Anteil bei 6–21 %, dort wird also nichts gesetzt |
| lava | aktiv | `FT_EL_WIT_lava_s_rock_06/07/08` (kleine Steine) | nein |
| felsgruppen | aktiv | `FT_EL_FS_*`-Blockklassen | nein |

Die Planer hochgebirge, mittelschicht, felsgruppen, elfenwald und lava habe ich nicht geändert (paralleler Agent bzw. nicht Teil des Auftrags).

### 2. Befund und Korrektur

**nordkueste: was entfernt wird und warum.** Entfernt werden alte Kiefern, Tannen und Küstenkiefern der Witcher-Ebene (`FT_EL_WIT_*`, „Haine“)
und der Bestand-Ebene (`FT_EL_BST_*`). Grund ist die Witcher-Messlatte: Skellige hat einen lichten Mischwald aus vielen Nadelarten
(Kotaku, 80.lv; `verteilung-nordkueste.md` §1/§3). Heute stehen dort eine Art, eine Höhe und ein Abstand, also eine Monokultur (Befunde
W6FIN_G3, FELS7_A4). Würde der Planer seine eigene gemischte Baumschicht (8 Klassen, Gruppen 18–60 m, Lichtungen 15–25 %) über den alten
Bestand legen, verdoppelte sich die Dichte, ohne dass sich der Mix ändert.

Vor 3b hatte der Filter drei Probleme:

1. **Zu breit im Netzsinn.** `sm_forest_pine_0` traf auch die liegenden Stämme `SM_Forest_pine_04/08/09_log`, also Witcher-Totholz.
   `fir_0` traf die Jungpflanzen `Fir_01_Plant` und `Fir_02_Small` sowie die Totbäume `Fir_08_Dead_Forest/_NoBillboard`. Keines dieser
   Netze setzt der Planer selbst neu.
2. **Zu breit im Raumsinn.** Die 85-%-Prüfung lief über alle Zellen des Feldes, Meer eingeschlossen (Kennzahl 0 = aue). Echte Küstenfelder
   wie B3 (47 % Land) kamen deshalb nie auf 85 %. Für die Frage, welche Bäume ein feldweiter Filter trifft, ist das aber die falsche Größe.
   Im Synthetiktest B5 lag der Anteil über alle Zellen bei 83 %, über die Landzellen bei 97 %.
3. **Keine Freigabe.** Ohne Freigabe entfernt der Setzer nichts, der Planer plante aber trotzdem den vollen Ersatz-Wald. Dazu kam, dass er
   die zu löschenden alten Bäume beim Abstand und beim Kronendach ignorierte. Ergebnis wäre ein Doppelbestand mit überlappenden Stämmen.

Korrektur in `nordkueste_plan.py` und `nordkueste_regeln.json` (minimal; die übrigen Schichten sind unverändert):

- Schalter `--ersetzen` (Standard aus) oder Regel `entfernen_aktiv` (Standard `false`).
- **Ohne Freigabe:** `plan.json["entfernen"] = ""`. Die Kandidaten stehen mit Zahl in `plan.json["entfernen_vorschlag"]`, und
  `baum_modus auto` fällt auf `ergaenzen` zurück (Dichte × 0,35, ≥ 4,5 m Abstand zu den alten Bäumen, die als vorhanden gelten).
  `baum_modus` erzwungen auf `ersetzen` bleibt `ersetzen`, aber ohne Filter.
- **Mit Freigabe** wird der Filter nur gesetzt, wenn alle vier Bedingungen erfüllt sind:
  - Die **Landzellen** des Feldes sind zu ≥ 85 % fjord/kueste/bergwald (`ersetzen_min_anteil`).
  - Höchstens 5 % der Kandidaten stehen in Saum- oder Fremdzellen (`entfernen_max_fremd_anteil`, gezählt aus den echten Positionen).
  - Es gibt überhaupt Kandidaten.
  - Der Modus ist `ersetzen`.

  Der Setzer löscht feldweit. Diese Prüfung ist die Annäherung an „nur in eigenen Zellen“, die mit dem heutigen Setzer möglich ist.
- **Präfixe** sind jetzt genau die Netze, die der Planer selbst als Baum neu setzt:
  `sm_forest_pine_01,02,03,05,06,07`, `fir_03…fir_07`, `sm_pine_beach_0`. Die Funktion `pruefe_entfernen` prüft jedes Präfix gegen
  `daten/netze.csv` und verwirft es mit WARNUNG, wenn es ein fremdes Netz träfe. **Nicht im Filter** sind
  `SM_Forest_pine_04/08/09`: Das Präfix würde die `_log`-Stämme mittreffen. Diese alten Kiefern bleiben stehen und gelten als vorhandene
  Bäume.
- `plan.json["entfernen_nur_ft"] = ["FT_EL_WIT_", "FT_EL_BST_"]` ist ein Hinweis an den Setzer: Er soll nur auf diese Foliage-Typen
  wirken, nie auf die eigenen `FT_EL_NK_*`, auf `FT_EL_WELT_*` oder auf Houdini-Akteure. `FT_EL_WELT_Forest_pine_*` und `Fir_*` existieren
  im Inventar.

**dschungel.** Der Planer entfernt **keine Bäume**. Witcher- und Bestand-Bäume, AsianTemple-Bäume und `SM_Tree_Palm_01` bleiben stehen,
die eigene Baumschicht ergänzt sie mit 4 m Abstand. Kandidat ist nur `sm_vines_01a`. Begründung: Die Witcher-Ebene streut diese Ranke
(12 Dreiecke, kein Nanite) gleichmäßig, ohne Bezug zu Stamm oder Wand. Der Planer setzt dieselbe Ranke gezielt 0,6–1,6 m um eigene
Laubbäume und in Wandspalten von 40–78°. Das Präfix trifft im Inventar nur `SM_Vines_01a`.

Vor 3b galt der Filter auch in G7, H7 und I7 (73–76 % Dschungel, 24–27 % aue). Dort hätte er Ranken in Aue-Zellen gelöscht. Korrektur in
`dschungel_plan.py` und `dschungel_regeln.json`:

- Gleicher Schalter `--ersetzen` bzw. `entfernen_aktiv`, gleiche Ausgabe `entfernen_vorschlag`.
- Mit Freigabe wird der Filter nur gesetzt, wenn die Landzellen zu ≥ 85 % Dschungel sind (`entfernen_min_anteil_land`) und höchstens 5 %
  der Kandidaten in Saum- oder Fremdzellen stehen.
- `entfernen_nur_ft: ["FT_EL_WIT_"]`.
- Die Farn-Entfernung, die Teil D über `mittelschicht_overrides.entfernen_je_feld` ausführt, ist jetzt leer (`{}`). Der bisherige Inhalt
  steht in `_entfernen_je_feld_vorschlag`. Freigabe heißt: Die Einträge für G6/H6/I6 nach `entfernen_je_feld` kopieren.
  `mittelschicht_plan.py` liest den Block weiter ohne Warnung (geprüft). Das H6-Synthetikfeld hat danach `entfernen ""` statt
  `sm_fern_01a,sm_fern_02a`.

### 3. Tabellen je Feld (Erwartung, ohne Echtdaten)

**Herleitung.** Es gibt **keine Zählung vorhandener Bäume je Feld**:

- `inventar.json` und `zusammenfassung.md` zählen nur Netze, Foliage-Typen und Pakete. Die `density`-Werte der Foliage-Typen sind
  Painter-Einstellungen, keine Bestandszahlen.
- Bekannt ist nur die Bestand-Ebene in G4 mit 17 000 Bäumen, also etwa 168 Bäume/ha in geschlossenem Wald (FORMAT §3/§4).

Die Spalten sind deshalb **Schätzungen Dichte × Fläche**. Die Annahmen:

- **Eigene Landfläche** A = 101,6 ha × Land % × Biomanteil % aus `biome_je_feld.json`. Dabei ist angenommen, dass die Biomanteile auf
  Land und Wasser gleich verteilt sind.
- **Baumfähig** = A × (1 − 0,5 × Anteil steil > 30°). Angenommen ist, dass die Hälfte der steilen Fläche über 40° liegt, Fels ist oder
  über der Waldgrenze 420–560 m.
- **Kandidaten** (alte Kiefern 01–03/05–07, Tanne 03–07, Küstenkiefer in `witcher/` und `bestand/`): 10–50 Bäume/ha baumfähig. Witcher-Haine
  sind Gruppen, kein geschlossener Wald; der Wert liegt deutlich unter den 168/ha der G4-Bestand-Ebene.
- **Neue Bäume:** `ersetzen` 15–45/ha baumfähig, `ergaenzen` 5–15/ha. Das ist aus den Synthetikläufen und der Spanne in
  `verteilung-nordkueste.md` §4 abgeleitet (1 200–2 500 im steilen Bergwald).
- Alle Werte sind auf 10 bzw. 50 gerundet.

**Nordküste** (biome_eigen fjord, kueste, bergwald; „Filter möglich“ heißt Landanteil ≥ 85 %):

| Feld | Biomanteil (Land %) | Begründung | Kandidaten (Schätzung) | erwartet entfernt: ohne Freigabe / mit `--ersetzen` | neue Bäume: ohne Freigabe (ergänzen) / mit `--ersetzen` |
|---|---|---|---|---|---|
| A3 | bergwald 92, aue 8 (16) | Filter möglich: Kiefern-Monokultur am Hang → Artenmix | 150–650 | 0 / 150–650 | 70–200 / 200–600 |
| B3 | bergwald 100 (47) | Filter möglich: reiner Bergwald, Monokultur → Mix mit Tanne, Birke, Hainbuche, Totbaum | 300–1 550 | 0 / 300–1 550 | 150–450 / 450–1 400 |
| I3 | bergwald 94, elfenwald 6 (31) | Filter möglich; der Elfenwald-Planer entfernt hier nichts (6 % < 50 %) | 200–1 000 | 0 / 200–1 000 | 100–300 / 300–900 |
| A4 | bergwald 92, aue 8 (36) | Filter möglich: FELS7_A4 zeigt die Kiefern-Monokultur am Fjordhang | 250–1 150 | 0 / 250–1 150 | 100–350 / 350–1 000 |
| B4 | bergwald 100 (100) | Filter möglich: steiler Bergwald, Waldgrenze 420–560 m, darüber nur Krüppelkiefer | 600–3 050 | 0 / 600–3 050 | 300–900 / 900–2 750 |
| A5 | kueste 75, bergwald 14, aue 11 (24) | Filter möglich: Klippenküste, Küstenkiefer/-eiche statt Forstkiefer. Entfällt, wenn > 5 % der alten Kiefern in den Aue-Zellen stehen | 150–650 | 0 / 0–650 | 70–200 / 200–600 |
| B5 | bergwald 79, kueste 21 (98) | Filter möglich: Küste → Hangwald → Grat; Synthetiktest mit Filter aktiv | 600–2 950 | 0 / 600–2 950 | 300–900 / 900–2 650 |
| H2 | kueste 78, elfenwald 20 (39) | kein Filter: Landanteil 78 % < 85 %, sonst würden Elfenwald-Bäume gelöscht | 200–1 000 | 0 / 0 | 100–300 / 100–300 (ergänzen) |
| I4 | bergwald 78, elfenwald 21 (63) | kein Filter: 78 % < 85 % | 300–1 600 | 0 / 0 | 150–500 / 150–500 |
| I5 | bergwald 68, dschungel 21, sumpf 11 (50) | kein Filter: 68 % < 85 % | 350–1 700 | 0 / 0 | 150–500 / 150–500 |
| B6 | bergwald 63, aue 24, lava 13 (63) | kein Filter: 63 % < 85 % | 350–1 800 | 0 / 0 | 200–550 / 200–550 |
| C1 | fjord 31, gletscher 69 (38) | kein Filter: nur Fjordzellen bis zur Gletschergrenze | 70–350 | 0 / 0 | 30–100 / 30–100 |
| D1 | fjord 26, gletscher 72 (40) | kein Filter | 60–300 | 0 / 0 | 30–90 / 30–90 |
| C2 | fjord 23, gletscher 46, tundra 21 (65) | kein Filter | 100–500 | 0 / 0 | 50–150 / 50–150 |
| D2 | fjord 19, tundra 47, gletscher 34 (100) | kein Filter | 150–700 | 0 / 0 | 70–200 / 70–200 |
| B2 | bergwald 20, gletscher 80 (25) | kein Filter | 30–150 | 0 / 0 | 10–40 / 10–40 |
| C3 | bergwald 6 (62) | kein Filter: nur Saumfeld | 40–200 | 0 / 0 | 20–50 / 20–50 |
| C4 | bergwald 6 (100) | kein Filter: nur Saumfeld | 60–300 | 0 / 0 | 30–90 / 30–90 |
| C5 | bergwald 6 (100) | kein Filter: nur Saumfeld | 60–300 | 0 / 0 | 30–90 / 30–90 |
| H1, A2, I2 | kueste 19 / bergwald 19 / bergwald 20 (Land 0) | kein Land, also keine Bäume | 0 | 0 / 0 | 0 / 0 |
| **Summe** | | **Filter möglich nur in A3, B3, I3, A4, B4, A5, B5** | | **0 / ≈ 2 100–11 000** | |

Vor 3b hätte der Filter mit Freigabe im Nordküsten-Synthetiktest B5 zusätzlich getroffen: Kiefer 08 (600), `_log` (300), `Fir_02_Small`
(200) und `Fir_08_Dead` (100). Mit 3 100 statt 1 900 Treffern waren das 63 % mehr.

**Dschungel** (biome_eigen dschungel). **Entfernte Bäume: 0 in allen Feldern.** Kandidaten sind nur Witcher-Lianen. Deren Dichte ist
unbekannt; die Schätzung von 5–25 je ha Dschungel-Land ist schwach belegt.

| Feld | Biomanteil (Land %) | Begründung | Bäume entfernt | Lianen `sm_vines_01a`: ohne Freigabe / mit `--ersetzen` (Schätzung) | Farne (Teil D, Vorschlag) | neue Bäume (Ergänzung, beide Fälle) |
|---|---|---|---|---|---|---|
| G6 | dschungel 97, aue 3 (80) | Filter möglich: Lianen an Stämmen und Wänden statt Streuung | 0 | 0 / 400–1 950 | nach Freigabe | 3 950–7 100 |
| H6 | dschungel 100 (94) | Filter möglich (Synthetiktest aktiv) | 0 | 0 / 500–2 400 | nach Freigabe | 4 800–8 600 |
| I6 | dschungel 100 (63) | Filter möglich | 0 | 0 / 300–1 600 | nach Freigabe | 3 200–5 750 |
| G7 | dschungel 73, aue 27 (10) | kein Filter: 73 % < 85 %; im Synthetiktest standen 29 % der Kandidaten in Aue- oder Saumzellen | 0 | 0 / 0 | nein | 350–650 |
| H7 | dschungel 76, aue 24 (22) | kein Filter: 76 % < 85 % | 0 | 0 / 0 | nein | 850–1 550 |
| I7 | dschungel 76, aue 24 (15) | kein Filter: 76 % < 85 % | 0 | 0 / 0 | nein | 600–1 050 |
| G5 | dschungel 22, heide 77 (100) | kein Filter (keine Kandidaten in den Regeln) | 0 | 0 / 0 | nein | 1 100–2 000 |
| H5 | dschungel 12, sumpf 78 (99) | kein Filter | 0 | 0 / 0 | nein | 600–1 100 |
| I5 | dschungel 21, bergwald 68 (50) | kein Filter | 0 | 0 / 0 | nein | 550–950 |

Die neuen Dschungel-Bäume sind mit 50–90 Bäumen/ha Dschungel-Land geschätzt, gedeckelt bei 9 000 je Feld (Synthetik H6: 8 300–8 900).
Diese Ebene ergänzt immer, mit oder ohne Freigabe.

### 4. Wie der Setzer lokal die exakte Zahl bekommt

Der Planer läuft ohne `--ersetzen`. Danach steht in `export/unreal/welt/<thema>/<Feld>/plan.json` unter `entfernen_vorschlag`:

- `anzahl`, getrennt in `anzahl_eigene_zellen`, `anzahl_saum`, `anzahl_fremde_zellen` und `anzahl_auf_wasser`;
- `je_netz` und `je_ebene` (witcher/bestand);
- `houdini_netzgleich`: Instanzen aus `instanzen.json`, die ein reiner Netznamen-Filter ebenfalls träfe;
- `anteil_eigen_land_feld`, `anteil_saum_fremd` und `grund` (warum der Filter nicht gesetzt ist).

Gezählt wird aus `witcher/` und `bestand/` des Feldes und der 8 Nachbarn, nur Positionen im Feld. Die Konsole meldet je Feld:
„entfernen nicht gesetzt: …; Vorschlag N Instanzen (eigene Zellen M)“. Nach der Freigabe lautet der Lauf
`python -I …/nordkueste_plan.py A3 B3 I3 A4 B4 A5 B5 --ersetzen` (dschungel: `G6 H6 I6 --ersetzen`). Dann ist `entfernen` gesetzt, die
Zahl steht in `entfernen_zaehlung`, und nordkueste plant den vollen Ersatz-Wald. **Zahl je Feld bitte an den Koordinator zurückmelden.**
Damit ersetzt sie die Schätzspalten oben.

### 5. Rauchtest (synthetisch, Python 3, NumPy, kein numba; Scratchpad danach gelöscht)

Mini-Produktionswurzel mit Rastern in voller Größe:

- **B5:** Meer im Westen, 210 m kueste, bergwald, 30-m-Aue-Band.
- **witcher/B5:** Kiefer 02 (1 500), Kiefer 08 (600), Kiefer 04_log (300), Fir_06 (400), Fir_02_Small (200), Fir_08_Dead (100),
  Farn 01a (2 000).
- **H6/G7 Dschungel:** G7 mit Aue-Streifen und Meer; je 1 200 Witcher-Lianen und 900 Farne.

| Prüfung | Ergebnis |
|---|---|
| nordkueste B5, Schalter aus | `entfernen ""`, `entfernen_vorschlag.anzahl` 1 900 (eigene Zellen 1 845, Saum 55, fremd 0; je Netz: Kiefer 02 1 500, Fir_06 400), Modus `ergaenzen`, 26 351 Instanzen, Ebene 2: 2 271 |
| nordkueste B5, `--ersetzen` | `entfernen` gesetzt (12 Präfixe), `entfernen_zaehlung` 1 900, `entfernen_nur_ft` gesetzt, Modus `ersetzen`, 32 691 Instanzen. Mit dem Planer vor 3b (gleiche Präfixliste, Schwelle 0,8, weil er über alle Zellen nur 83 % misst) sind alle 152 f32 **byteidentisch**, `dateien` und `entfernen` sind gleich |
| nordkueste, Schalter an, aber Fremdanteil-Grenze 1 % | Filter nicht gesetzt (Grund: 2,9 % > 1 %), Fallback ergänzen, f32 byteidentisch mit „aus“ |
| nordkueste G4 (fremd) | leerer `plan.json` mit `entfernen ""` |
| dschungel H6/G7, Schalter aus | `entfernen ""`. Vorschlag H6: 1 200 Lianen, alle in eigenen Zellen. Vorschlag G7: 1 200, davon 857 eigen, 46 Saum, 297 fremd |
| dschungel, `--ersetzen` | H6 `sm_vines_01a` gesetzt; G7 nicht gesetzt (Landanteil 73 % < 85 %). Alle f32 byteidentisch mit dem Schalter aus und mit dem Planer vor 3b. Die Platzierung hängt nicht am Filter |
| mittelschicht H6 (liest `dschungel_regeln.json`) | `entfernen ""` statt `sm_fern_01a,sm_fern_02a`, keine Warnung |
| Determinismus | zweiter Lauf: alle f32 byteidentisch (nordkueste 153/153, dschungel 54/54 je Feld), `plan.json` bis auf `stand`/`laufzeit_s` gleich |
| ASCII, py_compile | 0 Nicht-ASCII-Zeichen in allen Logs, beide Skripte kompilieren |

### 6. Offen für den Setzer / Koordinator

1. **Wie der Setzer Präfixe abgleicht, ist nicht dokumentiert.** FORMAT §3 nennt Netznamen-Präfixe. lava, felsgruppen und hochgebirge
   verwenden dagegen FT-Präfixe (`FT_EL_WIT_…`). Wenn der Setzer nur Netznamen vergleicht, trifft `sm_forest_pine_02` auch
   `FT_EL_WELT_Forest_pine_02`, Houdini-Kiefern und, bei einem späteren erneuten Setzen, die eigenen `FT_EL_NK_*`. Deshalb gibt es den
   Hinweis `entfernen_nur_ft` und die Zahl `houdini_netzgleich`. Bitte den Setzer so bauen, dass er die Präfixe nur auf
   `entfernen_nur_ft` anwendet und vor dem Setzen der eigenen Ebene löscht.
2. **Echte Zellgenauigkeit** („nur eigene Zellen“ auch in Mischfeldern wie H2, I4, I5, B6, G7–I7) bräuchte einen Setzer, der eine
   Positionsliste oder Biom-Maske je Feld liest. Heute ersetzen diese Felder nichts, sie ergänzen nur.
3. **Kiefer 04/08/09** bleiben auch mit Freigabe stehen, weil das Präfix die `_log`-Stämme mittreffen würde. Bei gleichverteilten
   Kiefernvarianten sind das etwa ⅓ der alten Kiefern. Der Planer behandelt sie als vorhandene Bäume. Bietet der Setzer exakte Namen,
   kann man sie ergänzen.
4. **Die Schätzspalten** (10–50 alte Kandidaten/ha) beruhen auf keiner Zählung. Die Zahlen aus `entfernen_vorschlag` ersetzen sie.
