# Verteilung Biomgruppe 8: Lava (Vulkanregion C6, C7, C5, D6, B6, D7, B7)

**Auftrag 11, Teil B8.** Biom `lava`, Foliage-Präfix `FT_EL_LV_`, Ordner `/Game/Eldarien/Welt/Foliage/Lava`. Stand 2026-10-10,
**Korrektur Runde 1** (Abschnitt unten, gilt vor §1–§6). Ursprüngliche Lieferung (Runde 0): dieser Bericht, `skripte/lava_regeln.json` (16 Klassen, 78 Netze in 82 Paletteneinträgen,
alle gegen `daten/netze.csv` geprüft, 0 fehlend), `skripte/lava_plan.py` (Planer nach FORMAT §3/§5, Schichten 0/1/2/5 plus Punktliste
und Overrides für 3/4). **Alles UNGETESTET MIT ECHTDATEN** – in der Cloud `py_compile`-sauber und mit synthetischen Rastern (C6 mit
Schlackenkegel, Lavastrom, See, Weg, Ort, Fremdbiom-Kachel; §4) rauchgetestet. Web-Quellen waren nur als Suchmaschinen-Auszüge lesbar
(kein Direktzugriff auf Verlage/80.lv/Fab); solche Belege sind mit **[Suchauszug]** markiert, Zahlen ohne Beleg mit **Richtwert**.

Betroffene Felder laut `biome_je_feld.md`: C6 (lava 99 %, Lavafels 45, Lavasand 27, Moos 17, Gras 8; 38 % steiler als 30°, Höhe bis
381 m), C7 (lava 61 %, 48 % Land, 59 % steil), C5 (lava 31 %, Rest Aue, 5,8 % Wasser), D6 (lava 26 %, Ödland 61 %), B6 (lava 13 %,
Bergwald 63 %), D7 (lava 13 %), B7 (lava 6 %). Der Planer läuft in jedem Feld auf der Lava-Maske aus `eigner.r8` + `welt.json`
(Rezept „Vulkanregion“ → lava) und einem 100-m-Übergangssaum außerhalb; Kennzahl 0 (Weltgelände) wird über die Lagen `Lavafels` +
`Lavasand` ≥ 96/255 als Lava erkannt, sonst gilt das dominante Feldbiom.

## Korrektur Runde 1 (10.10.2026): gilt vor allen folgenden Abschnitten

Grundlage: `auftraege/verteilung-korrektur-runde1.md` (lokaler Echtdaten-Test 10.10. 15:30) und `verteilung-KONVENTIONEN.md` §1–§6.
Geändert wurden nur `skripte/lava_plan.py` (jetzt 1 278 Zeilen), `skripte/lava_regeln.json` und dieser Bericht. Wo §2–§6 unten
etwas anderes sagen (100-m-Übergang, Lage-Erkennung für Kennzahl 0, Klassen `pionier`/`gras`/`verkohlt_liegend`/`verkohlt_stumpf`/
`ufer_block`, Overrides im `plan.json`, Empfehlung „Teil D in lava auf Faktor 0“ in §3 und §6.8), gilt dieser Abschnitt.

**Echtdaten-Befund (Vorfassung, Referenz):** A5 0, G4 0, E1 0 Instanzen – richtig, dort gibt es keine Lava. C6 (lava 99 %) **33 516**:
Das liegt unter dem Deckel von 60 000 und unter dem Zielband 45 000–52 000, ein Budgetproblem gab es also nicht. Das Problem waren
**Doppelungen**: In C6 setzte außerdem `mittelschicht` 7 515 Instanzen (Grasbüschel, Zwergheide, Totholz mit denselben Netzen wie
`gras`, `pionier`, `verkohlt_*`, `asche` hier); `felsgruppen` (27 357) und dieser Planer teilten sich die Lava-Blöcke über 0,8 m
(`ufer_block`, `lava_s_rock_03/04` in `schlacke`). Dazu kam die Biomregel: Kennzahl 0 wurde
über die Lagen Lavafels+Lavasand als Lava gelesen, und der Übergang reichte 100 m in fremde Biome. Die Zahl der Kollisionen meldete
die Vorfassung nur als `instanzen_kollision`.

### Was sich geändert hat

| Punkt | Runde 0 | Korrektur Runde 1 |
|---|---|---|
| Biom je Zelle (§1) | Kennzahl 0 → Lava, wenn Lavafels+Lavasand ≥ 96/255, sonst Feld-Fallback-Tabelle | `eigner.r8` + `welt.json`-Rezept; **Kennzahl 0 und unbekannte Rezepte → `aue`**, Rezept mit „vulkan“/„lava“ → `lava`, sonst exakter Biomname oder Teilwort. Nur wenn `eigner.r8`/`welt.json` fehlen, gilt das dominante Feldbiom aus `daten/biome_je_feld.json` (Hinweis in Log und `plan.json`). Regelblock `biom` → `zustaendigkeit` |
| Zuständigkeit (§1) | Lava-Maske + 100-m-Übergangssaum (Aschestaub in Aue/Bergwald) | `biome_eigen = ["lava"]`; bebaut werden lava-Zellen (Faktor 1) und ein **30-m-Saum**, in dem die Dichte linear auf 0 fällt (Distanz per iterativer Dilatation, NumPy). Die Zone `uebergang` ist jetzt dieser Saum. Alle Klassen werden mit dem Faktor multipliziert, Gruppenmitglieder an ihrer eigenen Zelle geprüft. Alle Punkte (Fumarolen, Spire, Höhle, Dampf, Gipfel, Opferstätte) liegen nur auf lava-Zellen im Feld |
| Leerplan (§1) | Feld ohne Lava: `plan.json` mit 0 Instanzen ohne Biomangaben | Eigenanteil im Fenster (Feld + 64 m) **< 2 %** → `plan.json` mit `instanzen: 0`, `leer: true`, `dateien: {}`, `entfernen: ""`, `punkte: []` und allen Pflichtschlüsseln; alte `.f32` werden gelöscht; eine Logzeile |
| plan.json (§2) | `instanzen_kollision`, Overrides als Kopie im Plan | neu: `biome_fenster` (Anteile, absteigend), `zellen_zustaendig` (Feldzellen mit Faktor > 0 ohne Wasser), `biome_eigen`, `kollision_anzahl`; außerdem `ebene` je Datei, `akteure`, `eigenanteil_fenster`, `lava_anteil`, `biom_quelle`, `saum_m`, `budget` (Deckel, Ziel, Zahl vor der Ausdünnung, Zahl je Klasse) und `overrides` (Verweis auf die Blöcke in `lava_regeln.json`). `punkte` bleibt, weil `felsgruppen_plan.py` daraus die Spire-Standorte liest |
| Budget (§3) | proportionale Hash-Ausdünnung (nicht exakt); die Kollision im Budget anders gezählt als im `plan.json` | **exakte** Kappung nach Instanz-Hash: Klassen-`max` → Akteure ≤ 60 → Kollision ≤ 3 000 (nur kollidierende Instanzen, unwichtigste Klasse zuerst) → Ziel 52 000 (je Klasse höchstens 60 % weg, Reihenfolge `prioritaet_behalten` von hinten: kiesel, schwarzkies, asche, schlacke …) → hart 60 000. Kollision je Netz wird für Budget und `plan.json` mit derselben Funktion bestimmt. Jede Ausdünnung schreibt `WARNUNG Budget: …` in Log und `hinweise`; wird Kleinzeug (kiesel, schwarzkies, asche) gedünnt, steht der Hinweis „Landschafts-Gras GT_Steinchen/GT_Kraut dichter stellen“ im Plan |
| Schicht 1 (§4) | moos, flechtenstein, pionier, kiefer_strauch, verkohlt_liegend/stumpf/schnag, gras | nur **Lava-Sonderformen**: `moos` (Racomitrium-Moospolster), `flechtenstein` (Wulstlava, ≤ 0,55 m), `kiefer_strauch` (Rolle jetzt `krummholz`; laut `verteilung-STATUS.md` entfällt `strauch` in der Mittelschicht für lava, weil der Kiefernstrauch Lava-Sonderform ist). `pionier` → `mittelschicht beere`, `gras` → `grasbueschel`, `verkohlt_liegend` → `totholz_liegend`, `verkohlt_stumpf` → `totholz_stumpf` (Werte unter `_korrektur_runde1_alt_klassen` dokumentiert). Eine Sperrliste im Code (`GENERISCH_MITTELSCHICHT`) überspringt solche Klassen mit Hinweis, falls sie wieder in die Regeldatei geraten |
| Schicht 0 | schlacke (inkl. `lava_s_rock_03/04` 1,1–1,2 m), kiesel, asche | `schlacke` nur noch `lava_s_rock_06/07/08` mit Maßstab 0,5–1,3 (0,24–0,78 m); Schlackenfelder und erkaltete Stromkanten (Hang 24–40° × 1,8, Kegelflanke × 2,2) bleiben. `asche` bleibt als **Brandstreu** (Asche-Bodendecker, Zweige 0,36–0,53 m, Schicht 0 wie die Zweige im Elfenwald); weil `mittelschicht` für lava dieselben Netze als `totholz_ast` führt, steht dort Faktor 0 |
| Schicht 2 | baum_tot, baum_kiefer | + `verkohlt_schnag` (stehende verkohlte Stämme 2–3,8 m; Totbaum-Rest, Kollision an) |
| Felsen > 0,8 m (§4/§6) | `ufer_block` (Schicht 5), `saeule`, Spires nur als Punktvorschlag | `ufer_block` → `felsgruppen_overrides.zusatzklassen.lava_uferblock`; Spires → `zusatzklassen.spire`. Eine Prüfung im Code nimmt Stein-/Block-/Kieselnetze mit Höhe × Maßstab > 0,8 m aus der Palette, außer bei `"fels_ausnahme": true`. Die einzige Ausnahme ist `saeule` (Basaltsäulen-Ersatz, Akteure an steilen Lava-Ufern, Yaw = Uferrichtung), die laut Auftrag als Lava-Sonderform bleibt. Für die Übergabe an Teil C steht `zusatzklassen.basaltsaeule` mit `"aktiv": false` bereit |
| Spuren (§4) | `spuren_overrides` mit freien Schlüsseln | Schema `palette`/`faktor`/`verbote`/`zusatzklassen` wie bei nordkueste (unten) |
| Logs (§5) | Umlaute, „→“, „–“ in `print()` | alle Ausgaben über `ascii_text()` (ä→ae, →→->, ≤→<=, §→Par., Rest „?“); `hinweise` im `plan.json` ebenfalls ASCII. Fehlende `hoehe.f32`, Regeldatei oder `netze.csv` sowie ein unbekanntes Feld → `FEHLER: …` und **Exit-Code 2**. `netze.csv` wird zusätzlich neben dem Skript gesucht. Ein Fehler in einem Feld bricht die anderen Felder nicht ab; Exit-Code dann 1 |
| Determinismus (§5) | `stand` mit Uhrzeit, `plan.json` je Lauf verschieden | `stand` = Regelstand („2026-10-10 Korrektur Runde 1“); zwei Läufe sind byteidentisch (alle f32, `plan.json`, PNG) |

### Override-Schema in `lava_regeln.json`

**`mittelschicht_overrides`** (für `mittelschicht_plan.py`, Format wie `nordkueste_regeln.json`/`dschungel_regeln.json`):

```
"mittelschicht_overrides": {
  "biom": "lava", "gilt_fuer": ["lava"],
  "palette":   {"grasbueschel": [6 Pfade], "beere": [6], "totholz_liegend": [5], "totholz_stumpf": [5]},   # ersetzt die Teil-D-Palette
  "faktor":    {"grasbueschel": 0.4, "beere": 0.4, "totholz_liegend": 0.6, "totholz_stumpf": 0.4, "totholz_ast": 0.0,
                "strauch": 0.0, "jungbaum": 0.0, "farn": 0.0, "hochstaude": 0.0, "pilz": 0.0, "totbaum": 0.0, "wurzel": 0.0, "kletter": 0.0},
  "faktor_begruendung": {...},
  "vorlage_biom": {"totholz_stumpf": "bergwald"},                       # Klasse fehlt in mittelschicht_regeln.json für lava
  "parameter": {klasse: {massstab, gruppe, radius_m, kippen, hang_max, eingraben_cm, laengs_hang, kollision, sichtweite, lagen_faktor}},
  "zusatzklassen": {}                                                    # keine: Moos, Wulstlava, Krummholz, Brandstreu setzt lava_plan.py
}
```

| Klasse | Palette (aus Runde 0) | Faktor | Herleitung / Parameter |
|---|---|---|---|
| grasbueschel | Tundra-Gras `SM_wk2oaeyqx_VarB/C/F/G`, `SM_dead_grass_03/01` (Aschegras) | 0,4 | Runde 0 `gras` ≈ 0,0011/m² in C6 (Lagenmix Lavafels 45 / Lavasand 27 / Moos 17 / Gras 8 %, Zonen frisch 0, alt 0,4, rand 1) gegen Teil D 0,006 × Lagenfaktor ≈ 0,5 = 0,003; `lagen_faktor` Lavafels 0,05, Lavasand 0,4, Moos 1,3, Gras/Trockengras 2,0 (ersetzt die Alterszonen: kein Gras auf frischer Lava) |
| beere | `SM_heath_A/B_01`, `SM_billberry_dry_01`, `SM_forest_heather_01`, `SM_beach_rose_06/07` (Ginster-Ersatz) | 0,4 | Runde 0 `pionier` ≈ 0,0013/m²; Maßstab 1,1–1,8, Gruppen 3–8 in 2,4 m |
| totholz_liegend | `SM_OldFallenTree_01/02`, `SM_Forest_pine_04/08/09_log` (verkohlt) | 0,6 | Runde 0 ≈ 0,00012/m² gegen 0,0002; Kollision, längs Hang, eingraben 25 cm |
| totholz_stumpf | `SM_BrokenStump_01`, `SM_RottenTreeStump_02`, `SM_pine_stump_01…03` | 0,4 | Runde 0 ≈ 0,00011/m² gegen Vorlage bergwald 0,0003; ohne Kollision |
| totholz_ast | – | 0 | dieselben Netze setzt `lava_plan.py` zoniert als `asche` (Brandstreu) |
| strauch, jungbaum, farn, hochstaude, pilz, kletter, wurzel, totbaum | – | 0 | Krummholz und Totbäume sind Lava-Sonderformen bzw. Schicht 2 hier, der Rest kommt auf Lava nicht vor |

**`felsgruppen_overrides`** (für `felsgruppen_plan.py`): `palette: "lava"`, `biom_faktor` 1,6, `klassen_faktor` (Blockstrom 2,0, Fuß 1,6,
Kuppe 1,3, Grat 0,9, Band 0,3, Wand 1,0, Prallhang 0,8), `eingraben` [0,3; 0,45], `platte_ersatz`; dazu die Altstelle `hero_akteure` +
`hero_akteur_punkte` und neu `zusatzklassen` nach §6:

| Zusatzklasse | Palette | Schlüssel (§6 + von felsgruppen gelesene Erweiterungen) |
|---|---|---|
| `spire` | `SM_IcelandicLavaSpire_02/01/03` (5–15 m, Nanite, 4 Kollisionsprimitive) | `rolle: fels_hero`, `akteur: true`, **`punkte: {ebene: "lava", typ: "spire_vorschlag"}`**, `hang_grad` [0, 18], `kuppen_prominenz_m` 6, `lagen_min` {Lavafels: 128}, `je_km2` 6, `max_je_feld` 6, `massstab` 0,85–1,2, `eingraben_anteil` 0,2–0,3, `gruppe` 1, `kollision`, `sichtweite` [0, 0] |
| `lava_uferblock` | `SM_lava_s_rock_01/02/05/03` (1–2,3 m) | `rolle: fels_block`, `dichte_je_ha` 200, `wasser_abstand_m` [0, 6], `hang_grad` [0, 60], `massstab` 0,8–1,3, `eingraben_anteil` 0,35–0,55, `gruppe` 1–3 in 2 m, `max_je_feld` 75, `kollision` (bisher `ufer_block` in Schicht 5) |
| `basaltsaeule` | `SM_lava_wall_05/04` | `"aktiv": false` – nur Schalter; aktiv setzen **und** `klassen.saeule` entfernen, wenn Teil C die Basaltsäulen übernehmen soll |

**`spuren_overrides`** (für `spuren_plan.py`; dort ist das Lesen der Overrides noch nicht eingebaut): `palette.steinmann` =
`SM_lava_s_rock_08/07/06`; `faktor.lava` Steinmann 1,5, Wegkreuz 0,5, Karren 0,3, Rauch 1,0, Feldstreifen/Obstgarten/Zaun/Mauer/Steg/
Holzschlag/Köhler/Gräber 0; `verbote.lava` dieselben plus Schrein; `rauch_punkte` {ebene lava, typ fumarole/dampf}; `zusatzklassen`
(§6-Schema mit `punkte`): `schwefelgrube` (Kiste, Fass, Karren, Sack, 3–6 in 8 m an `schwefelgrube_vorschlag`), `opferstaette_saeule`
(Runde 2: `SM_Column_02` × 0,58–0,66 als Akteur an `opferstaette_vorschlag`), `opferstaette_steinkreis` (8–12 Schlackenbrocken, Ring r 3 m, `anordnung: ring`),
`ruine_verkohlt` (`SM_Wall_02` + `SM_Column_02`, schwarze Material-Instanz, max 1 je Feld, Hang ≤ 12°, 6–40 m vom Weg); `blickziele`
wie bisher.

### Spires: Übergabe an `felsgruppen_plan.py`

Was felsgruppen künftig liest: `lava_regeln.json["felsgruppen_overrides"]["zusatzklassen"]["spire"]`. Weil Name und Inhalt gleich sind,
ersetzt felsgruppen die Altstelle (`hero_akteure` + `punkte.spire_vorschlag`) und meldet „Altstelle(n) spire durch zusatzklassen
ersetzt“. Die Altstelle bleibt in der Datei, damit ältere felsgruppen-Fassungen weiterlaufen. Standorte: felsgruppen öffnet
`export/unreal/welt/lava/<Feld>/plan.json` und nimmt `punkte[typ == "spire_vorschlag"]` (Weltkoordinaten cm). Dieses Format ist
unverändert: flache Kuppen im frischen/alten Kern, Hang ≤ 18°, Prominenz ≥ 6 m, Abstand ≥ 150 m, max 6 je Feld. Fehlt der Lava-Plan,
oder enthält er keine Spire-Punkte, setzt felsgruppen über die Ersatzmaske (Hang, Kuppenprominenz, Lavafels ≥ 128, 6 je km² lava,
max 6) nur in lava-Zellen + Saum. Zwei Einschränkungen gelten für felsgruppen, nicht für diesen Planer. (1) Ein Lava-Plan mit 0 Spire-Punkten
(Leerplan oder keine Kuppe) löst ebenfalls die Ersatzmaske aus. Wenn das stört, sollte felsgruppen „Datei vorhanden, 0 Punkte“ als
„keine Spires“ behandeln. (2) `netz` und `yaw_grad` aus dem Punkt werden nicht übernommen; felsgruppen wählt Netz und Yaw selbst.
Reihenfolge laut §4: zuerst `lava_plan.py`, dann `felsgruppen_plan.py`, damit die Punkte vorliegen.

### Rauchtest Korrektur Runde 1 (synthetisch, Python 3.13, NumPy 2.5, Pillow 12, ohne numba; Raster neu erzeugt, danach gelöscht)

Synthetische Produktionswurzel im Scratchpad: `hoehe.f32` in voller Größe (memmap). **C6**: Schlackenkegel r 320 m / +230 m mit Krater,
Lavastrom 120 m, See r 55 m, zwei Wege, Ort; `eigner.r8` = Kennzahl 7 „Vulkanregion“, dazu eine bergwald-Kachel (Kennzahl 3) in der Ecke,
**99,0 % lava im Feld**. **C5** (Mischfeld): südliches Drittel lava mit Wellengrenze, Rest Kennzahl 0 (= aue) mit Teich. **G4**
(Fremdfeld): elfenwald (Kennzahl 5) + Kennzahl 0. Lagen Lavafels/Lavasand/Moos/Gras, `bestand/C6` mit 300 Kiefern, `netze.csv`,
`netze_masse.json`, `biome_je_feld.json`.

| Feld | biome_fenster | Instanzen (vor Budget) | Kollision | zuständig (Zellen) | Schichten boden / mittel / baum / wasserkante | Punkte | Laufzeit |
|---|---|---|---|---|---|---|---|
| C6 | lava 0,979, bergwald 0,021 | **40 840** (45 141) | 75 (davon 6 Säulen-Akteure) | 1 001 567 | 31 482 / 9 156 / 69 / 133 | 28: 11 Fumarolen, 9 Dampf, 2 Gipfel, 3 Spire, 1 Höhle, 1 Schwefelgrube, 1 Opferstätte | 3,2–4,0 s |
| C5 | aue 0,645, lava 0,355 | **17 240** (18 477) | 113 | 375 256 | 7 794 / 9 333 / 113 / 0 | 3 | 2,9–3,0 s |
| G4 | elfenwald 0,789, aue 0,211 | **0** – leerer `plan.json`, alle Pflichtschlüssel | 0 | 0 | – | 0 | < 1 s |

Prüfskript (unabhängige Distanz über die Randzellen der lava-Maske):

- Alle Pflichtschlüssel sind vorhanden. f32-Summe = `instanzen`, Kollisionssumme = `kollision_anzahl`, jede Datei hat `ebene`.
- Quaternionen sind normiert, Maßstäbe > 0, alle Instanzen liegen im Feld.
- **0 Instanzen** auf Wasser, Weg oder Ort.
- **0 Instanzen jenseits des Saums:** Der größte Abstand einer Instanz außerhalb der Lava zur nächsten lava-Zelle beträgt in C5 29,1 m und in C6 19,0 m (bergwald-Ecke). Das Prüfbild C5 zeigt einen schmalen Saum und einen leeren aue-Teil, auch der Teich bleibt leer.
- **Zwei Läufe sind byteidentisch:** 100 Dateien, f32 + `plan.json` + PNG.
- **Logs: 0 Nicht-ASCII-Zeichen.**
- **Exit-Code 2** bei fehlender `hoehe.f32`, unbekanntem Feld (K9) und fehlender Regeldatei.
- `py_compile` ist sauber.

Budget:

- `--faktor 3`: C6 43 482, C5 34 225. Hier greifen nur die Klassen-`max`.
- Stresslauf mit Regelkopie (Klassen-`max` aus, Kollisionsdeckel 100, `--faktor 4`): C6 184 392 → **59 995** Instanzen, 34 Kollisionen. Ausgedünnt wurde der Reihe nach nach Kollision, Ziel (60 % je Klasse) und harter Kappung, jeder Schritt als WARNUNG, dazu der Landschafts-Gras-Hinweis.

Querprobe mit den Querschnitts-Planern auf denselben Daten:

- `felsgruppen_plan.py C6` liest `lava_regeln.json` mit 11 gelesenen und 0 ignorierten Schlüsseln. `spire` holt 3 Punkte aus `lava/C6/plan.json` und setzt 3 Akteure, `lava_uferblock` 15 Blöcke; die Altstelle wird gemeldet und ersetzt.
- `mittelschicht_plan.py C6` liest palette, faktor, zusatzklassen, parameter und vorlage_biom ohne unbekannte Schlüssel. Ergebnis: grasbueschel 699, beere 633, totholz_liegend 41, totholz_stumpf 38, gesamt 1 588 einschließlich bergwald-Ecke (Vorfassung Echtdaten: 7 515).

**Erwartung Echtdaten C6:** Die Vorfassung setzte 33 516. Entfallen sind gras, pionier, verkohlt_liegend/stumpf und ufer_block (im
Runde-0-Synthetik rund 13 % der Instanzen), außerdem gilt nur noch der 30-m-Saum. Erwartet werden deshalb **~28 000–31 000**, Kollision unter
500, also weit unter Deckel und Ziel. Die Rand-Zone ist in Feldern mit 99 % Lava sehr schmal (Synthetik 0,3 %), deshalb gibt es kaum
Krummholz oder Totbäume. In Echtdaten mit 17 % Moos `zonen.alter_gewichte.randnaehe` prüfen (§6.1 unten).

## 1. Referenzanalyse: was ein Lavafeld zwischen Boden und Horizont füllt

**Die Ordnung kommt vom Alter des Stroms, nicht vom Zufall.** Alle vier Referenzlandschaften zeigen dieselbe Abfolge, nur mit
anderen Zeitachsen. Island (Hekla-Chronosequenz, Vilmundardóttir et al. 2018): Lavas jünger als 70 Jahre tragen nur Erstbesiedlung
durch das Wollige Zackenmützenmoos *Racomitrium lanuginosum* und die Flechte *Stereocaulon*, die zu einer geschlossenen Decke
zusammenwächst; 170–700 Jahre alte Ströme sind moosdominiert, und diese Phase ist durch die dicke Moosmatte „arretiert“ – Gefäßpflanzen
kommen erst nach Jahrhunderten **[Suchauszug: journals.sagepub.com/doi/10.1177/0309133318798754, researchgate 328144291]**.
Für die 2021–2023er Ströme am Fagradalsfjall gibt es bisher nur Mikrobiologie (Nature Comms Bio 2025: Besiedlung innerhalb von Stunden,
Stabilisierung nach dem ersten Winter) – sichtbare Vegetation: keine; die Ströme sind tiefschwarz mit rostroten Oxidationsflecken
**[Suchauszug: nature.com/articles/s42003-025-09044-1]**. Eldhraun (Laki 1783, 565 km²) ist nach 240 Jahren vollständig von
*Racomitrium*-Polstern überzogen; Wachstum 1–2 cm je Jahrzehnt, Trittschäden brauchen 30–70 Jahre **[Suchauszug: iceland.org/eldhraun,
amazingiceland.is; Tourismusquellen, nicht peer-reviewed]**. Das ist die Bildwirkung „Moos-Mondlandschaft“: gelbgrüne Polster
0,3–0,7 m über schwarzen Wülsten, keine Sträucher, keine Bäume, nur am Rand Lupinen und Gras.

**Teneriffa** liefert das trockene Gegenstück: Auf den historischen Strömen (Arafo/Fasnia 1705, Garachico 1706, Chinyero 1909) ist die
Oberfläche nur chemisch (Oxidation) und biologisch durch Flechten verwittert; Pflanzen (*Spartocytisus supranubius*-Ginster,
*Erysimum scoparium*) stehen nur auf undatierten, älteren Strömen und dem unteren Garachico-Strom **[Suchauszug: researchgate 286935977,
Feldspektrometrie Teneriffa; en.wikipedia.org/wiki/Teide]**. Übertragen: frische Ströme bleiben über 300 Jahre pflanzenfrei, wenn es
trocken ist; der gelbweiß blühende Ginster (1–2 m, Farbakzent) steht nur im Randgürtel.

**Hawaii** gibt die Formen: Pāhoehoe (glatt, Wülste, Tumuli) und ʻAʻā (scharfkantige Klinker dm–m groß) liegen nebeneinander, Pāhoehoe
überdeckt ʻAʻā teilweise; **Kīpuka** sind von jüngerer Lava umflossene Inseln mit reifer Vegetation, von denen die Wiederbesiedlung
ausgeht; der Farn ʻAe (*Polypodium pellucidum*) und ʻŌhelo-Beeren sind die ersten Besiedler und wachsen aus Rissen und Hohlräumen,
ʻŌhiʻa-Bäume folgen **[Suchauszug: nps.gov/havo/learn/nature/ferns.htm, nps.gov/havo/learn/nature/kipuka.htm, usgs.gov
„Geology/Ecology of Hawaiʻi Volcanoes NP“, smithsonianmag.com]**. Tumuli-Größen fand die Suche nicht; Richtwert aus Fotos 3–10 m
Durchmesser, 1–3 m hoch.

**Ätna** ist das Modell für den Rand- und Übergangsgürtel: *Stereocaulon vesuvianum* besiedelt alle Ströme seit 1910, seine Biomasse
steigt im ersten Jahrhundert steil an und fällt dann, wenn Gefäßpflanzen es beschatten; auf dem 1886er Strom standen bereits die
stickstoffbindenden Ginster *Genista aetnensis* und *Spartium junceum*; Artenreichtum hängt nur lose vom Stromalter, eng aber vom
Deckungsgrad ab **[Suchauszug: researchgate 314281270 „Floristic change during early primary succession on lava, Mount Etna“;
uobrep.openrepository.com/handle/10547/610794]**. Informelle Zeitangaben (Flechten nach 5–10 a, Moose nach 20–30 a) stammen von
Tourismusseiten **[Suchauszug: etnaway.com]** und sind nur Richtwerte. Kiefern: keine Quelle gefunden; die Ätna-Kiefer (*Pinus nigra
laricio*) als Krummholz am Stromrand ist Beobachtung aus Fotos, Richtwert.

**Witcher-Staffelung.** CDPR hat kein Lava-Biom; die Prinzipien kommen aus Skellige (Basaltküste, Moos auf Fels, Färöer/Island als
Referenz, siehe `verteilung-fels-organisch.md`) und aus der Methode: Vegetation pro Region als eigene Bibliothek, Reihenfolge große
Bäume → kleine → Farne → Gras, Pinsel je Geländetyp mit Abstand- und Skalenvariation **[Suchauszug: 80.lv/articles/world-building-of-witcher-3]**;
Felsen, Klippen und Wurzeln sitzen im Gelände statt als gestreute Props darauf **[Suchauszug: pcgamer.com „Why I love: The Witcher 3's
topography“]**. Die Bildkritik (`bildkritik-witcher-messlatte.md`) nennt als Kernmangel „jede Fläche trägt genau einen Maßstab“ und
fordert drei bis vier ineinandergreifende Größenstufen plus Makro-Variation im 100–500-m-Maßstab. Für Lava heißt das: **Spire/Hornito
5–15 m → Blöcke 1–3 m (Teil C) → Schlacke 0,25–0,8 m → Kiesel 0,15–0,45 m → Landschaftsmaterial Lavasand**, dazu Makro-Variation durch
die Alterszonen (schwarz / moosgrün / Pioniergelb / Aschegrau im Übergang) und 300-m-Wertrauschen, Farbakzente Schwefelgelb (Fumarolen),
Gelbgrün (Racomitrium), Rost (oxidierte Schlacke per Material), Blickziele Kegelgipfel, Spire, Dampf am Seeufer. Spuren von Leben im
Lavafeld sind dünn: Steinmänner aus Schlacke an Wegen (Island-Vörður), eine verlassene Schwefelgrube, eine Opferstätte am Kegelfuß.

## 2. Regelwerk (`lava_regeln.json`) – Zonierung und Schichten

### 2.1 Lava-Maske, Alter, Zonen, Kegel

`alter = 0,5·Moos + 0,2·Gras + 0,3·(1 − d_Rand/120 m) + 0,2·(Rauschen₃₀₀ − 0,5) − 0,2·Lavafels·(1 − Moos)`, geklemmt 0–1
(Lagen 0–1 aus `lage_*.r8`, Gauß σ 3 m; `d_Rand` = Abstand zum Nicht-Lava per Dilatation auf 2-m-Stufe, gedeckelt 120 m).
Zonen: **frisch** < 0,28, **alt** 0,28–0,52, **rand** ≥ 0,52 (alles innerhalb der Maske), **uebergang** = außerhalb bis 100 m.
Ohne `lage_Moos/Gras` wird nur Randnähe + Rauschen benutzt (Hinweis im Log). Fällt die Rand-Zone in Echtdaten zu dünn aus (C6 hat nur
17 % Moos), `alter_gewichte.randnaehe` auf 0,45 heben. **Schlackenkegel:** Gipfel = lokales Maximum im 60-m-Fenster mit Prominenz ≥ 8 m
gegen das 120-m-Mittel; Flanken = Prominenz > 5 m und Hang 24–36° (Schüttwinkel loser Schlacke 30–35°, Richtwert) tragen Schlacke 2,2×
und Pflanzen 0,3×. Sperrflächen: Wasser + 1,5 m, Weg 2,5 m (Kleinzeug) / 4 m (Blöcke, Bäume, Akteure), Ort 5 m, vorhandene Ebenen
(`bestand/`, `witcher/`, `ufer/`, `instanzen.json`; Bäume 2 m, Sonstiges 1 m), Fumarolen-Radius pflanzenfrei. Hang: Pflanzen ≤ 38°,
Steine ≤ 62° (FORMAT: > 40° nur Felsen). Höhe: Pflanzen ab 220 m linear abnehmend, 0 ab 360 m.

### 2.2 Schichten und Klassen (Dichten Instanzen je m² auf der Lage; Zonenfaktor frisch / alt / rand / übergang)

| Schicht | Klasse (Gruppe) | Netze | Dichte (Lage) | Zone f/a/r/ü | Gruppe n / r | Maßstab | Eingraben | Sichtweite cm | Koll. | max |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 boden | `schlacke` (Aa-Klinker 0,25–0,8 m) | `SM_lava_s_rock_06/07/08` (0,5–0,8 m) + `_03/_04` klein skaliert | Lavafels 0,012, Lavasand 0,010, Geröll 0,012, Moos 0,003 | 1,4/1,0/0,5/0,25; Hang 24–40° ×1,8; Kegelflanke ×2,2 | 3–8 / 2,2 m | 0,45–0,85, ±15 % nicht-uniform | 30–50 % | 0–15 000 | nein | 9 000 |
| 0 boden | `kiesel` (Lavakiesel-Ersatz) | `SM_SmallStonesPack_08…14`, `SM_stone_05/06/07` ×1,2–2,6 → 0,15–0,45 m | Lavasand 0,045, Lavafels 0,028, Geröll 0,04 | 1,2/0,9/0,6/0,5 | 6–18 / 1,6 m | 1,2–2,6 | 30–50 % | 0–6 000 | nein | 22 000 |
| 0 boden | `asche` (verkohlte Zweige) | `SM_DryBranches_01/04/05/07`, `SM_dead_quiver_branch_01/02_NN` | Lavasand 0,004, Nadeln 0,006, Gras 0,004 | 0/0,6/1,2/1,5 | 1–4 / 2,5 m | 0,9–1,5 | 3 cm | 0–9 000 | nein | 2 500 |
| 1 mittel | `moos` (Racomitrium-Polster) | `SM_MossClump_01/03/05` ×2–4 (→ 0,3–0,7 m), `SM_MossPlane`, `SM_moss_01/02` | Moos 0,05, Lavafels 0,012, Gras 0,01 | 0,08/1,0/1,1/0,4; am Fuß von Schlacke ×1,6 | 5–14 / 2 m | 2,0–4,0 | 4 cm | 0–12 000 | nein | 8 000 |
| 1 mittel | `flechtenstein` (Wulstlava-Ersatz) | `SM_LichenedForestBoulder_01`, `SM_MossyRocks_01/02`, `SM_MossyForestRock_01/03`, `texndcpda_tier_0` | Moos 0,006, Lavafels 0,004 | 0,1/1,0/0,8/0,3 | 1–4 / 2,5 m | 0,7–1,2 | 35–55 % | 0–20 000 | nein | 2 500 |
| 1 mittel | `pionier` (Ginster-Ersatz) | `SM_heath_A/B_01` ×1,1–1,8, `SM_billberry_dry_01`, `SM_forest_heather_01`, `SM_beach_rose_06/07` | Gras 0,008, Moos 0,006, Trockengras 0,006 | 0/0,5/1,2/0,9 | 3–8 / 2,4 m | 1,1–1,8 | 3 cm | 0–15 000 | nein | 2 500 |
| 1 mittel | `kiefer_strauch` (Krüppelkiefer 0,8–2 m) | `SM_pine_beach_short_01/02`, `_crooked_02`, `SM_dwarf_pine_small_01/02`, `_medium_01` | Nadeln 0,0015, Gras 0,0012 | 0/0,25/1,0/1,3 | 1–3 / 3 m | 0,7–1,15 | 6 cm | 0–30 000 | nein | 500 |
| 1 mittel | `verkohlt_liegend` | `SM_OldFallenTree_01/02`, `SM_Forest_pine_04/08/09_log` | Nadeln 0,0006, Lavasand 0,0004 | 0,15/0,6/1,0/1,4 | 1–2 / 4 m | 0,9–1,3 | 20–35 %, Yaw hangab ±35° | 0–45 000 | **ja** | 450 |
| 1 mittel | `verkohlt_stumpf` | `SM_BrokenStump_01`, `SM_RottenTreeStump_02`, `SM_pine_stump_01…03` | Nadeln 0,0006 | 0,2/0,6/1,0/1,3 | 1–3 / 5 m | 0,9–1,4 | 8 cm | 0–25 000 | nein | 400 |
| 1 mittel | `verkohlt_schnag` (stehend 2–3,8 m) | `SM_dead_quiver_trunk_NN` (2 m, 88 Dreiecke) ×1–1,9, `SM_RottenTreeStump_01` | Nadeln 0,0005, Lavasand 0,0004 | 0,3/0,8/1,0/1,0 | 1–4 / 6 m | 1,0–1,9 | 15 cm | 0–30 000 | nein | 400 |
| 1 mittel | `gras` (Horstgras) | Tundra-Gras `SM_wk2oaeyqx_VarB/C/F/G`, `SM_dead_grass_01/03` | Gras 0,012, Trockengras 0,012, Wiese 0,008 | 0/0,4/1,0/1,2 | 3–9 / 2 m | 0,9–1,4 | 3 cm | 0–12 000 | nein | 3 000 |
| 2 baum | `baum_tot` | `SM_DeadTree_01/02` (6–7 m), `SM_EuropeanBeech_Dead_XL_01` (21 m), `Fir_08_Dead_NoBillboard` | Nadeln 0,0005, Gras 0,0003 | 0/0,3/1,0/1,4 | 1–3 / 7 m | 0,9–1,3 | 20 cm | 0 | **ja** | 180 |
| 2 baum | `baum_kiefer` (Krummholz 2,5–5 m) | `SM_pine_beach_crooked_01`, `_small_01/04`, `SM_dwarf_pine_big_01/02` | Nadeln 0,0012, Gras 0,0006 | 0/0,15/1,0/1,2 | 1–4 / 6 m | 0,7–1,1 | 10 cm | 0 | **ja** | 250 |
| 5 wasserkante | `ufer_block` (abgeschreckte Blöcke) | `SM_lava_s_rock_01/02/05/03` (1,1–2,3 m) | 0,02 im Band 0–6 m | 1,0/1,0/0,8/0 | 1–3 / 2 m | 0,8–1,3 | 35–55 % | 0–40 000 | **ja** | 150 |
| 5 wasserkante | `schwarzkies` | `SM_NordicBeachRock_01`, `SM_SmallStonesPack_08/12`, `SM_stone_06` | 0,12 im Band 0–8 m | 1/1/1/0,6 | 5–16 / 1,8 m | 0,8–1,6 | 30–50 % | 0–6 000 | nein | 1 500 |
| 5 wasserkante | `saeule` (Basaltsäulen-Ersatz, **Akteure**) | `SM_lava_wall_05` (1,75 × 1,95 × 3,95 m), `_04` hochkant | 0,0025 im Band 1–10 m, Hang 28–75° | 1/0,8/0,3/0 | 2–5 / 4 m, Yaw = Uferrichtung | 0,9–1,5 | 30–45 % | 0 | **ja** | 40 |

Alle Felsen/Steine werden voll auf die Geländenormale gekippt, Sträucher 35–50 %, Bäume 10–15 %, Yaw zufällig außer `verkohlt_liegend`
(hangab) und `saeule` (Uferrichtung). Pivot: alle `SM_lava_*` haben den Pivot in der Netzmitte (`netze_masse.json`: min_z ≈ −H/2); der
Planer rechnet `z = Boden − min_z·s − Eingraben·H·s`, für Netze ohne Bounds-Eintrag Pivot unten. Budget: Ziel 52 000 je Feld, hart
60 000; Kollision ≤ 3 000 (nur `verkohlt_liegend`, `baum_*`, `ufer_block`, `saeule`); Akteure ≤ 60. Bei Überschreitung werden zuerst
`kiesel`, `schwarzkies`, `asche`, `schlacke` nach Instanz-Hash ausgedünnt, Bäume und Akteure zuletzt. Wichtig für den Setzer: die 29
`Lava_Volcano`-Netze haben **keine Kollisionsprimitive** (Taxonomie); `plan.json` fordert für Blöcke > 0,8 m trotzdem `kollision: true`
und trägt je Netz den Hinweis „Komplex-als-Einfach oder Konvex-Hülle erzeugen“ ein. Material-Hinweise im `plan.json`: `kiesel`,
`schwarzkies`, `asche`, `verkohlt_*`, `baum_tot` brauchen eine dunkle/verkohlte Material-Instanz (Albedo ×0,2–0,35, Rauheit 0,9–0,95),
`moos` eine gelbgrüne statt waldgrüne.

### 2.3 Overrides für Schicht 3 (Teil C, `felsgruppen_plan.py`) und Schicht 4 (Teil D, `spuren_plan.py`)

`plan.json["felsgruppen_overrides"]`: Palette `lava` (Teil C hat sie bereits: `lava_b_rock_01/02`, `lava_m_rock_*`, `lava_s_rock_*`,
`lava_wall_*`, LavaSpire als Hero), Biomfaktor **1,6** statt 1,0 (Blockfelder/ʻAʻā-Klinker), Klassenfaktoren Blockstrom 2,0, Hangfuß 1,6,
Kuppe 1,3, Grat 0,9, Wand 1,0, Prallhang 0,8, **Band 0,3** (Lavaströme haben keine Sedimentbankung; Stromfronten sind Hangfuß/Wand),
Zonenfaktor frisch 1,3 / alt 1,0 / rand 0,7 / übergang 0,4, Eingraben 30–45 %, Kollision ab 0,8 m Höhe (Setzer-Hinweis wie oben).
Platten-Ersatz (Lava hat keine `geroell_platte`): `SM_MossyRocks_01/02`, `SM_TundraRockyGround_01`, `texndcpda_tier_0`. Kiesel-Ersatz:
Teil C streut `SM_stone_03…08` (grau) – bitte dieselbe dunkle Material-Instanz oder Klasse `kiesel` dieses Regelwerks. **Spires als
Akteure:** `SM_IcelandicLavaSpire_01…03` (5,0–5,3 m hoch, `_02` 15 × 7 m, Nanite, 4 Kollisionsprimitive) werden nicht von diesem Planer
gesetzt; er liefert `punkte[typ == spire_vorschlag]` (flache Kuppen im Kern, Hang ≤ 18°, Prominenz ≥ 6 m, Abstand ≥ 150 m, max 6 je Feld,
mit Netz und Yaw) als `hero_akteur_punkte` für Teil C oder für die Hand.

`plan.json["spuren_overrides"]`: aus = Feldstreifen, Obstgarten, Zaun, Mauer, Steg, Holzschlag, Köhler, Friedhof; **Steinmänner** ×1,5
aus `SM_lava_s_rock_06/07/08` entlang der Wege (Abstand 90–140 m); Wegkreuze ×0,5, keine Schreine; Rauchsäulen aus `punkte[typ ==
fumarole]`; Schwefelgrube (Kisten/Fässer/Karren 3–6 im Radius 8 m) an `schwefelgrube_vorschlag`; Opferstätte (Steinkreis 8–12 Schlacken,
r 3 m, `AncientRuins/SM_Column_02`, Runde 2) an `opferstaette_vorschlag`; Blickziele Kegelgipfel, Spire, stärkste Fumarole, Höhleneingang.

### 2.4 Punktliste (`plan.json["punkte"]`, Weltkoordinaten cm)

| typ | Regel | Felder je Punkt |
|---|---|---|
| `fumarole` | 12 je km² frisch, 4 alt, 0,5 rand; Kegelflanke/Prominenz > 8 m ×3; Hang ≤ 40°; Abstand ≥ 45 m; max 24 je Feld; Radius pflanzenfrei | `staerke` 0,4–1,0 (Niagara-Rate), `radius_m` 1,5–5 (Schwefelkruste/Decal), `schwefel` (60 % gelb, Námafjall-Optik), `zone`, `kegelflanke`, z = Boden + 0,3 m |
| `dampf` | Lava (frisch/alt) berührt Wasser: Band 0–3 m, Abstand ≥ 25 m, max 20 | `staerke` 0,3–0,7 (Laze-Dampf) |
| `kegel_gipfel` | lokale Maxima mit Prominenz ≥ 8 m, max 6 | `prominenz_m` (Blickziel) |
| `spire_vorschlag` | s. 2.3 | `netz`, `yaw_grad` |
| `hoehle_vorschlag` | Lavawand 48–75°, ≥ 40 m vom Rand, Abstand ≥ 300 m, max 2 | Hinweis: kein Höhlen-Netz im Inventar |
| `schwefelgrube_vorschlag` | stärkste Fumarole mit Weg ≤ 150 m, max 1 | – |
| `opferstaette_vorschlag` | 25 m hangab vom ersten Spire/Gipfel, max 1 | `anker` |

### 2.5 Planer `lava_plan.py`

Aufruf `python -I scripts/lava/lava_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]`. Fenster Feld + 64 m
per `np.memmap` (NY 7057 × NX 9577, J-Spalte auf 9577 geklippt: 505 m breit), Hang/Normale aus Gauß-geglätteter Höhe (σ 1,5 m),
Prominenz aus Box-Mittel 120 m, Abstände per Dilatation (2-m-Stufe), Gruppen als Zentren + Mitglieder in Scheiben, jede Instanz wird
gegen Dichte, Sperre, Hang und Feldgrenze geprüft. Zufall: 64-bit-Hash aus (Seed 806, Klasse, Weltrasterkoordinate) → Nachbarfelder
erzeugen im Randstreifen dieselben Gruppen, zwei Läufe sind byte-identisch. Nur NumPy (numba wird erkannt, nicht gebraucht). Ausgabe
`export/unreal/welt/lava/<Feld>/<Netz>.f32` (10 float32 LE), `akteur_<Netz>.f32` für `saeule`, `plan.json` mit `stand, feld, ebene,
instanzen, instanzen_kollision, dateien{pfad, anzahl, gruppe, rolle, schicht, sichtweite, schatten, kollision, hinweis}, entfernen,
ft_ordner, ft_praefix, punkte, zonen, lava_anteil, felsgruppen_overrides, spuren_overrides, hinweise`; `--bild` →
`docs/pruefung/lava/<Feld>.png` (Hintergrund = Zone: frisch schwarz, alt oliv, rand grün, übergang beige; Wasser blau, Weg braun, Ort
rot; Instanzen in Klassenfarbe; Kreuze = Punkte). Fehlende optionale Dateien (Lagen, Karten, eigner/welt.json, Ebenen, netze_masse)
erzeugen je einen Hinweis in Log und `plan.json["hinweise"]`; fehlende `hoehe.f32`/`netze.csv`/Regeldatei → klare Meldung, Exit.

## 3. Abgrenzung zu vorhandenen Ebenen und zu Teil C/D

- **`FT_EL_WIT_*` (Witcher-Bewuchs):** `entfernen = FT_EL_WIT_lava_s_rock_06,…_07,…_08` – nur die drei kleinen, gleichmäßig
  gestreuten Lava-Steine werden durch die geclusterte Klasse `schlacke` ersetzt (gleiche Netze, Gruppen 3–8, Flanken-Bonus).
  `FT_EL_WIT_lava_s_rock_01–05` und `lava_m_rock_01/04` bleiben, bis Teil C in den Lava-Feldern abgenommen ist; dann dort `entfernen`
  erweitern. Witcher-Kleinzeug (Laub, Zweige) läuft in Lava ohnehin nicht (Biom-Eignung 0).
- **`FT_EL_BST_*` (Wald-Bestand):** kein Baum-Bestand in Lava; im Übergangssaum (B6 Bergwald, C5 Aue) hält der Planer 2 m Abstand zu
  Bestand-Bäumen und setzt nur Totbäume/Krüppelkiefern zusätzlich (Lava hat den Waldrand getötet).
- **`FT_EL_FS_lava_wall_01/02/09` (Felsschalen):** bleiben als Wandsilhouette; die `saeule`-Akteure nutzen `lava_wall_04/05` nur in
  Uferbändern (1–10 m vom Wasser, Hang ≥ 28°), keine Doppelung mit Steilwänden > 55°.
- **`FT_EL_UF_*` (Ufer):** die Ufer-Ebene läuft an allen Ufern; die Wasserkanten-Klassen hier gelten nur **innerhalb** der Lava-Maske
  (Zonenfaktor übergang 0) und ergänzen schwarze Blöcke/Kies; `ufer/foliage_<Feld>` wird als belegt gelesen (1 m Abstand).
- **Teil C (`felsgruppen_plan.py`):** setzt Schicht 3 (Hero, Blöcke, Blockströme, Hangfuß) mit den Overrides aus 2.3. Dieser Planer
  streut nichts über 0,8 m außer `ufer_block`/`saeule`; die Klasse `flechtenstein` (0,35–1,2 m, tief eingegraben) liegt bewusst in
  Schicht 1 als Wulstlava-Optik, nicht als Felsgruppe.
- **Teil D (`mittelschicht_plan.py`):** hat für lava nur Trockengras/Totholz (0,001–0,006/m²). Empfehlung: in den Lava-Feldern
  `mittelschicht` für Biom lava auf Faktor 0 stellen, da `gras`, `pionier`, `verkohlt_*` hier dichter und zoniert gesetzt werden;
  im Übergang (Aue/Bergwald-Zellen) bleibt Teil D zuständig. `spuren_plan.py` nutzt die Overrides aus 2.3.
- **Wüste (C3–E5):** keine Überschneidung (D5/E5 haben keine Lava).

## 4. Testanleitung

**Rauchtest Cloud (gelaufen, Python 3.13, NumPy 2.5, Pillow 12, ohne numba).** Mini-Produktionswurzel mit `hoehe.f32` in voller Größe
(memmap; nur C6-Fenster beschrieben: Grundfläche 30 m + 3 %-Gefälle, Schlackenkegel r 320 m / +230 m mit 60-m-Krater, Lavastrom 120 m breit
/ 12 m hoch nach Südost, See r 55 m am Kegelfuß 3 m eingetieft, Weg schräg durch den Kegel, Ort 40 × 50 m), `karte_wasser/weg/ort.r8`,
`eigner.r8` (Vulkanregion Kennzahl 7 unregelmäßig r 360–480 m; Nordhälfte außen Kennzahl 3 = aue, Südhälfte 0 = Weltgelände) +
`welt.json`, `lage_Lavafels/Lavasand/Moos/Gras.r8` (Summe 255, Moosrampe 200–400 m vom Kegel), `bestand/C6` (300 Kiefern),
`daten/netze.csv` + `netze_masse.json`. Ergebnis `lava_plan.py C6 --bild`: **42 169 Instanzen (587 mit Kollision), 76 Netzdateien,
23 Punkte, 3,8–4,7 s** je Feld (inkl. Bild). Zonen im Feld: frisch 37,1 %, alt 16,5 %, rand 3,5 %, übergang 27,7 %, sonst 15,2 %
(Lava-Anteil 57 %); Schichten boden 26 265 / mittel 15 447 / baum 355 / wasserkante 102. Klassen: kiesel 15 268, schlacke 9 059 → 8 996
(max), moos 8 034 → 7 998, gras 4 307 → 2 984 (max 3 000), pionier 2 290, asche 1 918, flechtenstein 1 195, kiefer_strauch 517 → 497,
baum_kiefer 233, verkohlt_liegend 209, verkohlt_stumpf 187, verkohlt_schnag 149, baum_tot 122, schwarzkies 158, ufer_block 29,
saeule 0 (bei `--faktor 3`: 8 Akteure in `akteur_SM_lava_wall_04/05.f32`, Kollision/Hinweis gesetzt). Punkte: 6 Fumarolen (2 mit
Schwefel), 9 Dampf am Seeufer, 2 Kegelgipfel (Kraterrand 17,7 m, Stromende 9,1 m), 3 Spire-Vorschläge, 1 Höhle, 1 Schwefelgrube
(Fumarole am Weg), 1 Opferstätte. Prüfskript: alle f32 durch 10 teilbar, Anzahl = `plan.json`, Quaternionen normiert, Maßstäbe > 0,
alle Instanzen im Feld, **0 Instanzen** auf Wasser/Weg/Ort, z − Gelände zwischen −0,22 m (Flechtensteine 35–55 % eingegraben) und
−0,03 m, maximaler geglätteter Hang je Rolle: Pflanzen ≤ 38°, Steine ≤ 56°, Blöcke ≤ 59°; zwei Läufe byte-identisch (MD5 aller f32);
`--faktor 0.5` → 21 750 Instanzen. Randfeld J7 (505 m breit, keine Lava): 0 Instanzen, 0,7 s, kein Fehler; C7 ohne Lava im Synthetik:
927 Instanzen aus dem Übergangssaum des C6-Kegels (Nahtfenster wirkt). Fehlende `hoehe.f32` → „Pflichtdatei fehlt“, Exit. Prüfbild
`docs/pruefung/lava/C6.png`: schwarzer Kern mit Kiesel-/Schlacke-Clustern, oliver Moosring, grüner Randsaum, beiger Übergang mit
Totholz/Gras, See mit Dampfkreuzen, Weg und Ort frei. Die Rand-Zone ist im Synthetik dünn (3,5 %), weil die Moosrampe nur bis 0,73
reicht – in Echtdaten prüfen (§6).

**Erwartete Instanzzahlen je Feld (Rechnung aus Flächenanteilen und Dichten, Spanne ±35 %, nach Budget):**

| Feld | Lava-Fläche km² | gesamt | boden | mittel | baum | wasserkante | Kollision | Fumarolen |
|---|---|---|---|---|---|---|---|---|
| C6 (lava 99 %, 38 % steil) | 1,0 | 32 000–48 000 | 20 000–30 000 | 8 000–16 000 | 80–300 | 0 (kein Wasser) | 300–800 | 8–24 |
| C7 (lava 61 %, 48 % Land, 59 % steil) | 0,3 | 12 000–26 000 | 8 000–18 000 | 3 000–7 000 | 50–200 | 0 | 150–500 | 3–12 |
| C5 (lava 31 % + Saum, Wasser 5,8 %) | 0,31 | 8 000–18 000 | 4 000–10 000 | 3 000–7 000 | 100–300 | 200–1 200 | 300–900 | 1–6 |
| D6 (lava 26 %, Wasser 3,7 %) | 0,25 | 6 000–14 000 | 3 000–8 000 | 2 000–5 000 | 60–200 | 100–800 | 200–600 | 1–5 |
| B6, D7 (lava 13 %) | 0,08–0,13 | 3 000–8 000 | 1 500–4 500 | 1 000–3 000 | 40–150 | 0–300 | 100–400 | 0–3 |
| B7 (lava 6 %, 28 % Land) | 0,02 | 800–3 000 | 400–1 500 | 300–1 200 | 10–60 | 0 | 20–120 | 0–1 |

**Prüfkameras (Weltkoordinaten cm; Feldmitte = Spalte·1008 + 504, Zeile analog):**
1. **C6 Lavafeld, Augenhöhe 1,7 m** bei X −221 050, Y 148 350 (Feldmitte, Lavafels-Fläche; wenn dort Kegelflanke, 150 m hangab), Blick
   quer zur Hangrichtung ins tiefe Seitenlicht. Erfolg: innerhalb 10 m drei Größenstufen (Kiesel 0,15–0,45 m in Nestern von 6–18,
   Schlackenbrocken 0,25–0,8 m in Gruppen 3–8 mit sichtbar eingegrabener Unterkante, dahinter Teil-C-Blöcke 1–3 m); kein Stein schwebt,
   keine Pflanze im frischen Kern außer vereinzelten verkohlten Stümpfen; mindestens eine Fumarole in Sichtweite (gelbe Kruste, Rauch);
   Kleinzeug cullt bei 60 m (Kiesel) bzw. 150 m (Schlacke) ohne sichtbares Aufploppen gegen den dunklen Boden.
2. **C7 Hang, 10 m über Grund** bei X −221 050, Y 249 150 (Mitte der 59-%-Steilzone), Blick hangauf 20° nach oben. Erfolg: Schlacke
   verdichtet sich auf den 24–40°-Flanken (×1,8), Pflanzen enden bei 38°, oberhalb nur Felsen (Teil C) und Schlacke; Flechtensteine und
   Moospolster sitzen in Mulden und am Fuß von Blöcken (×1,6), nicht gleichmäßig; Hangfuß zeigt Übergang Schlacke → Lavasand mit
   Horstgras.
3. **C5 Übergang Lava → Aue, 2 m Höhe** bei X −221 050, Y 47 550 ± 300 m auf der Lava-Grenze (Prüfbild: Grenze oliv/beige), Blick
   entlang der Grenze. Erfolg: innerhalb 100 m außerhalb der Lava ein Aschestaub-Saum mit verkohlten Stämmen hangab, Stümpfen, 1–3
   Totbäumen und Krüppelkiefern in 1–4er-Gruppen, Horstgras in Rissen; innerhalb der Lava ein grüner Randgürtel (Heide/Strandrose als
   Pionier, Moos) – kein harter Materialwechsel ohne Objekte; Aue-Ebene (`FT_EL_AU_*`) und Lava-Ebene überlappen nur im Saum.
4. **D6/C5 Seeufer in der Lava, 3 m Höhe**, Blick über das Wasser. Erfolg: schwarzer Kiessaum 0–8 m, abgeschreckte Blöcke halb im Wasser,
   an steilen Ufern 2–5 hochkant stehende `lava_wall_05` in Uferrichtung, Dampfpunkte an der Wasserlinie (Niagara); nichts im Wasser.
5. **Draufsicht 400 m über C6** (Prüfbild und Editor). Erfolg: drei Farbzonen als Makro-Variation (schwarz, moosgrün, Pioniergelb),
   Zonengrenzen unregelmäßig (300-m-Rauschen), Kegelgipfel mit Fumarolen-Kranz, Spire als Blickziel auf einer Kuppe, Weg und Ort frei.
6. **Nahtprüfung C6/C7 und C6/B6** (Draufsicht 100 m): Gruppen laufen über die Feldgrenze, keine Dichtesprünge.

Erfolgskriterien in Zahlen: Instanzen und Kollision je Feld innerhalb der Tabelle; Setzer legt ≤ 78 Foliage-Typen `FT_EL_LV_*` an
(davon 6 Baum-/Stamm-/Blocktypen mit Kollision) plus ≤ 60 Akteure; Laufzeit Planer ≤ 10 s je Feld; PNG und `plan.json` je Feld.

## 5. Einkaufsliste (Fab/Megascans, frei bevorzugt; Namen sind Fab-Suchbegriffe, da Fab nicht direkt lesbar war)

| Asset (Fab-/Megascans-Name) | Stufe | Wofür | Heutiger Ersatz |
|---|---|---|---|
| Megascans „Pahoehoe Lava“ / „Ropy Lava Rock“ / „Lava Flow Surface“ (Platten 1–3 m, flach, Wulststruktur) | High 4K, Nanite | Klasse `flechtenstein` → echte Wulstlava in alt/frisch; Teil-C-`platte_ersatz` | bemooste Waldsteine tief eingegraben |
| Megascans „Volcanic Rock“ / „Scoria“ / „Lava Rock Small“ (Schlackenbrocken 0,2–0,6 m, 4–6 Varianten, rot-schwarz) | High 2K | `schlacke` (heute 3 Netze, 3 Skalierungen) – mehr Varianz, rostrote Oxidationsvarianten | `SM_lava_s_rock_06–08` skaliert |
| Megascans „Lava Pebbles“ / „Volcanic Gravel“ / „Black Beach Pebbles“ (Kleinsteine 5–30 cm als Pack) | High 2K | `kiesel`, `schwarzkies`, Teil-C-Kieselsaum | graue SmallStonesPack + dunkle Material-Instanz |
| Megascans „Moss Clump“ / „Icelandic Moss“ / „Mossy Ground Patch“ (Racomitrium-Polster 0,3–0,8 m, gelbgrün) | High 2K, Nanite | `moos` (heute 0,1–0,18-m-Docks-Moos ×2–4 skaliert → Texturdichte zu grob) | MossClump/MossPlane |
| Megascans „Burnt Tree Trunk“ / „Charred Log“ / „Burnt Stump“ (verkohlte Stämme 3–8 m, Stümpfe) | High 4K | `verkohlt_liegend/stumpf/schnag`, Teil-D-Totbaum-Solitär | Mossy-Totholz + schwarze Material-Instanz |
| Megascans „Basalt Columns“ / „Columnar Basalt“ / „Hexagonal Basalt Cliff“ (Säulenreihen 3–8 m) | High 4K, Nanite | `saeule` an Lava-Ufern und Stromfronten (Reynisfjara-Optik); Teil-C-Klasse wand in lava | `lava_wall_05` hochkant |
| Decals „Sulfur Crust“ / „Yellow Mineral Deposit“ / „Fumarole Ground“ (2–5 m) + Niagara-Rauch | 2K | Fumarolen-Punkte (`radius_m`, `schwefel`), Schwefelgrube | – (nur Punktliste) |
| Megascans „Broom Shrub“ / „Genista“ / „Retama“ (Ginster 1–2 m, gelb blühend) | High 2K | `pionier` Farbakzent am Rand (Ätna/Teide) | Heide ×1,1–1,8, Strandrose |
| Megascans „Lava Tube Entrance“ / „Cave Entrance Rock“ (8–15 m) | High 4K | `hoehle_vorschlag` | kein Netz |

Vor dem Kauf: Megascans-Assets, die vor 31.12.2024 beansprucht wurden, sind frei (`boden-kleinzeug-gras.md`); nach Import Post-Import-Pass
nach `klippennetze-a5.md` (Nanite, Convex-Kollision 4–16 Hulls, Texturen auf 4K/2K klemmen). Wird eingekauft, nur die Pfade in
`lava_regeln.json` tauschen, der Planer bleibt gleich.

## 6. Offene Punkte und Annahmen

1. **Ungetestet mit Echtdaten.** Zonenschwellen (0,28 / 0,52) und Alter-Gewichte sind auf synthetische Lagen abgestimmt; in C6 (Moos 17 %)
   kann die Rand-Zone zu dünn werden → `randnaehe` 0,45 oder `alt_bis` 0,45. Kegelerkennung (Prominenz ≥ 8 m gegen 120-m-Mittel) kann
   in C6 (381 m Höhe, 38 % steil) Felsgrate als Kegel lesen; dann `prominenz_min_m` 12 und Flanken-Hangfenster prüfen.
2. **`welt.json`-Schema** nur aus FORMAT bekannt: `kacheln` als Dict oder Liste mit `kennzahl`/`id` + `rezept`; Zuordnung über die
   Wörter „lava“/„vulkan“ im Rezepttext, alles andere = anderes Biom, Kennzahl 0 = Lage-Erkennung (Schwelle 96/255, Glättung 6 m).
3. **Lagen `Lavafels`/`Lavasand`** werden als dominante Lagen in der Lava angenommen; sind sie in Echtdaten mit `Fels`/`Geroell` gemischt,
   `lagen`-Liste und Dichten je Lage erweitern (Geröll ist bereits mit Schlacke/Kiesel-Dichte belegt).
4. **Material-Instanzen** (dunkle Kiesel/Zweige, verkohltes Holz, gelbgrünes Moos) sind Setzer-Arbeit; ohne sie stehen graue Steine
   und braunes Totholz auf schwarzem Grund. Hinweise stehen je Netz in `plan.json["dateien"][…]["hinweis"]`.
5. **Kollision der Lava-Netze**: keine Primitive im Inventar; `kollision: true` für `ufer_block`, `saeule` und Teil-C-Blöcke erfordert
   Komplex-als-Einfach oder Konvex-Hüllen (bei ≤ 200 Stück je Feld vertretbar; `klippennetze-a5.md`).
6. **Nicht-Nanite-Netze** in der Palette: Coast_Dunes-/Mountain-Kiefern (`kiefer_strauch`, `baum_kiefer`), `Fir_08_Dead`, Meadow
   `dead_grass` – Sichtweiten gesetzt (300 m bzw. 0 für Bäume), LOD im Editor prüfen; Hinweis im `plan.json`.
7. **Spires** werden nur vorgeschlagen (Punkte), nicht gesetzt; Teil C muss `hero_akteur_punkte` lesen oder der Setzer setzt sie von Hand.
   `SM_IcelandicLavaSpire_02` ist 15 × 7 × 5 m (liegende Formation) – Yaw aus dem Punkt, Eingraben 25 % Richtwert.
8. **Doppelungen mit Teil D** (`mittelschicht` lava-Dichten) und mit `FT_EL_WIT_lava_s_rock_01–05`: bewusst belassen bis zur Abnahme;
   danach `entfernen` erweitern bzw. Teil-D-Faktor in lava auf 0.
9. **Fumarolen-Dichte** (12/km² frisch) ist Richtwert aus Námafjall/Sólfatara-Fotos; Niagara-Kosten bei 24 Säulen je Feld prüfen
   (Sichtweite 2–3 km, Rauch träge 3–8 m hoch, Dampf am Wasser kürzer).
10. **Zeitplan Setzer:** 76–78 Foliage-Typen je Feld sind viele; wenn der generische Setzer je Typ > 3 s braucht, Palette per
    `netz_gewichte` 0 auf ~50 Netze kürzen (Kiesel 10 → 6, Moos 6 → 4).

## Korrektur Runde 2 (10.10.2026)

- Gesperrte Saeule Nr. 03 aus `spuren_overrides.zusatzklassen.opferstaette_saeule` ersetzt durch SM_Column_02 (5 m x 0,58-0,66 = ca. 3 m, gleiche Wirkung); Hinweistext in `punkte.opferstaette_vorschlag` angepasst.
- Basaltsaeulen-Ersatz (lava_wall_04/05, 3,9-4,5 m, Felsen > 0,8 m) an Teil C uebergeben: Klasse `saeule` entfernt (Werte in `_korrektur_runde2_alt_klassen`), `felsgruppen_overrides.zusatzklassen.basaltsaeule.aktiv = true`. `platte_ersatz` (TundraRockyGround) bleibt Teil C. Keine Platten im Planer.
- Rauchtest synthetisch C6: 33 279 Instanzen, zwei Laeufe byteidentisch, gesperrte Netze 0, Log ASCII, 3 s.

## Korrektur Runde 4 (10.10.2026): Meer fehlt in `karte_wasser`

Anlass: `auftraege/verteilung-korrektur-runde4.md`. `karte_wasser.r8` enthält nur Süßwasser, und die Lava-Planung lief bis auf den
Meeresboden. Umgesetzt nach `verteilung-KONVENTIONEN.md` §1b in `skripte/lava_plan.py` und `skripte/lava_regeln.json` (neuer Block `meer`):

- `meer = (hoehe < 0) & (karte_wasser == 0)`. Im Code steht `wasser` jetzt für `wasser_alle = karte_wasser > 0 | meer`, `suess` nur
  für `karte_wasser`. Das gilt für Sperren, `wasser_nah` (`ausschluss.wasser_m`), das Wasserband von `schwarzkies`, Dampf-Punkte (Lava trifft
  Wasser, auch Meer), Höhlen-Vorschläge, `zellen_zustaendig` und das Prüfbild. Der Lavastrom ist kein Wasser.
- `schwarzkies` (schwarzer Lavasand-Strand) bekommt `strand: true`. Es ist die einzige Klasse im Küstensaum 0…+0,3 m (≤ 30 m zu `meer`).
  Unter −0,3 m wird nichts gesetzt, −0,3…0 m nur `meer_rolle` (keine Klasse).
- Die Prüfung läuft zellweise in der Dichtekarte und als Schlussfilter an der Bodenhöhe am Instanzort (bilinear), vor dem Budget.
  `plan.json` meldet `meer_zellen`, `meer_gefiltert`, `meer_gefiltert_je_klasse` und `kuestensaum_zellen_feld`, der leere Plan `meer_zellen`.

Rauchtest synthetisch (Scratchpad, danach gelöscht): je Feld eine Küste quer durchs Feld – Meer bis −14 m **nicht** in `karte_wasser`, flache Zone −0,3…0 m (≈ 25 m breit), Strand 0…0,3 m (15 m), Insel, See + Fluss in `karte_wasser` bis 45 m ins Meer, Binnensenke 0,15 m (> 100 m vom Meer), Weg. Gezählt an der Bodenhöhe am Instanzort (bilinear) und am Feld z (mit Eingraben). Feld C7 (lava 100 %, Meer 41 % des Fensters):

| C7 | vorher | nachher |
|---|---|---|
| Instanzen gesamt | 32 892 | 32 651 |
| Bodenhöhe < 0 m / < −0,3 m | **14 245 (43 %)** / 13 192 | **0 / 0** |
| −0,3…0 m nach Rolle | 1 053 (Kiesel 725, Schlacke 251, Moos 61, Flechtenstein 11, Schnag 5) | 0 |
| 0…0,3 m im Küstensaum | 711, darunter Schlacke 186, Moos 19, Flechtenstein 12, Schnag 5 | 1 042, nur `schwarzkies` (Netzdateien geprüft) |
| Feld z < 0 (mit Eingraben) | 14 230 | 257 – Strand-Kiesel auf Boden 0…0,3 m (Eingraben 30–50 %) |
| `meer_gefiltert` | – | 41 |

Die Gesamtzahl bleibt fast gleich, weil `kiesel` (22 000) und `schwarzkies` (1 500) am Klassen-`max` hängen. Was nicht mehr auf den
Meeresboden fällt, füllt das Land auf. Zwei Läufe sind byteidentisch, das Log ist ASCII-only, `py_compile` ist sauber, `--bild` und
fehlende `karte_wasser.r8` laufen. UNGETESTET MIT ECHTDATEN.
