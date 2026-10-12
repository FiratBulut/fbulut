# Antwort zu Auftrag 16d – fluss_sim lokal: Archivordner, gebaute Pläne, Töpfe, Vorschläge

Stand 12.10.2026. Grundlage sind Auftrag 16d samt Nachtrag 19:00 (lokale Antworten auf die Rückfragen aus 16c), die
Koordinator-Entscheidungen zu den 16c-Rückfragen 4 und 5, die Antwort 16c und `skripte/fluss_sim/`. Gerechnet wurde wie in
16c mit den 2-m-Daten: Gefälle-Planer `--alle` (98 Lauf-Pläne), Sehens-Planer für alle 15 Biome.

## Kurzfazit

- **Beide Fehler sind behoben** (Commits `8d3d44d` und `10f237f`).
  - **Fehler 1, Archivordner:** Gelesen werden nur noch Lauf-Pläne, also `<lauf>/plan.json` mit dem Schlüssel
    `wasser_koerper`. Ordner mit „.“ im Namen oder mit führendem „_“ und andere Pläne wie der Feld-Instanzplan
    `gefaelle/C2/plan.json` werden übersprungen und im Protokoll genannt. Das gilt auch für Archiv-Feldordner unter
    `instanzen/` und `sw_<biom>/`. Mit drei Archivkopien von C2 las der alte Exporter 20 190 Objekte und 2 248
    Kollisionseinträge zu viel. Der neue Exporter liefert mit Archivordnern dieselben Dateien wie ohne sie.
  - **Fehler 2, Geländedeltas doppelt:** Das Delta eines gebauten Laufs wird nicht mehr addiert. Gebaut ist ein Lauf, wenn
    er unter `--gebaut` steht oder wenn `sehens_einbau/A15_<lauf>/lauf.json` in `nachgezogen` sein Feld nennt.
  - **Befund zu Fehler 2:** Die `lage`-Einstufungen hängen **nicht** vom Gelände ab. Sie waren also auch lokal richtig.
    Falsch war nur der Gelände-Teil des Fingerabdrucks im SWR-Bereich des gebauten Laufs (`F_ERLENBACH_T00`). Er hätte
    bei jedem Lauf „neu backen“ gemeldet. Die synthetische Gegenprobe bestätigt das: Die `lage` aller 23 450 Objekte ist
    gleich, und mit „gebaut“ ist der Fingerabdruck wieder gleich dem ohne doppeltes Delta.
- **16c-Rückfrage 4 (Töpfe):** 21 Sehens-Seen unter 30 m gehören jetzt zu ihrem Gewässer. Davon sind 9 Durchfluss-,
  9 Quell- und 3 Endtöpfe.
  - Die Elfentreppe besteht aus 6 Bächen und 5 Töpfen. Sie ist jetzt **ein** Gewässer mit **einer** SWR (60 × 52 m,
    256, 0,235 m). Die Gletschertöpfe (4 Bäche, 3 Töpfe) und der Wollsackfall (2 Bäche, 1 Gumpe) sind ebenfalls je ein
    Gewässer.
  - Gewässer: 196 → **187**. Sehens: 42 Bäche → 33 Gewässer. SWR: 211 → 202. Mit einer SWR: 188 → 179; alle
    Sehens-Gewässer haben genau eine.
  - Mündung „See“: 23 → 11, dazu 3 × „Topf“. Anfang „See“: 25 → 5, dazu 10 × „Topf“.
- **16c-Rückfrage 5 (Vorschläge):** Es gibt 47 Vorschläge, getrennt von der Spline (`muendung.vorschlag` und
  `vorschlaege.json`).
  - 23 Lücken: gerade Verlängerungen von 4–22 m.
  - 24 offene Enden: Verlängerung entlang des steilsten Gefälles, bei einer Senke weiter auf dem Weg des geringsten
    Anstiegs. Länge 20–591 m. Alle 24 finden ein Ziel: 20 × Bach, 12 × Fluss, 12 × See, 3 × Meer, gezählt über alle 47.
  - 9 Vorschläge brauchen einen Einschnitt von mehr als 1 m. 3 davon führen durch `F_HAUPTFLUSS_3`, das dort einen
    höheren Spiegel hat. Diese Fälle sind eher Fehler in den Weltdaten.
- **Prüfer:** 0 FEHLER, 0 WARNUNG, 60 HINWEIS. Zwei Läufe sind byte-gleich (183 Dateien). Die 12 neuen Gegenproben
  ergeben alle FEHLER; ebenso der Fall „gebaut vermerkt, aber Welt ohne Stempel“.

## 1. Fehler 1 – Archivordner und Feld-Plan

**Lösung** (`lauf_plaene()`, `feld_plaene()` in `fluss_sim_export.py`; der Prüfer nutzt dieselben Funktionen):

- Unter `--gefaelle` zählt ein Ordner nur unter drei Bedingungen:
  - Sein Name enthält kein „.“.
  - Sein Name beginnt nicht mit „_“.
  - Seine `plan.json` hat den Schlüssel `wasser_koerper`.
- Unter `<lauf>/instanzen/` und `sw_<biom>/` werden Feldordner mit „.“ oder führendem „_“ übersprungen.
- Die Sehens-Biome werden über ihre festen Namen gelesen (`<biom>/orte.json`). Archivordner neben den Biomen werden also
  nie gelesen.
- Jeder übersprungene Ordner steht im Protokoll und in `zusammenfassung.json` unter `eingaben.uebersprungen`. Dort stehen
  Eingabe, Ordner und Grund.
- Die Archivordner dürfen also wieder in `gefaelle/` liegen. `_alt/` ist nicht mehr nötig, schadet aber nicht.

**Protokoll** (synthetische Gegenprobe, Aufbau wie bei dir lokal):

```
[fluss_sim] uebersprungen: gefaelle/C2 - kein Lauf-Plan (ohne 'wasser_koerper', z. B. Feld-Instanzplan von a15_einbau.py)
[fluss_sim] uebersprungen: gefaelle/F_ERLENBACH_1V_C2.alt_lava_biomfehler - Archivordner ('.' im Namen bzw. fuehrendes '_')
[fluss_sim] uebersprungen: gefaelle/F_ERLENBACH_1V_C2.alt_v1_gebaut - Archivordner ('.' im Namen bzw. fuehrendes '_')
[fluss_sim] uebersprungen: gefaelle/F_ERLENBACH_1V_C2.alt_vor15b - Archivordner ('.' im Namen bzw. fuehrendes '_')
[fluss_sim] uebersprungen: gefaelle/_alt - Archivordner ('.' im Namen bzw. fuehrendes '_')
[fluss_sim] uebersprungen: gefaelle/F_ERLENBACH_1V_C2/instanzen/C2.alt_v1 - Archivordner ('.' im Namen bzw. fuehrendes '_')
[fluss_sim] uebersprungen: sw_elfenwald/G4.alt - Archivordner ('.' im Namen bzw. fuehrendes '_')
[fluss_sim] uebersprungen: sw_elfenwald/_G3 - Archivordner ('.' im Namen bzw. fuehrendes '_')
```

**Gegenprobe:**

- **Aufbau:** alle 98 Pläne, dazu
  - drei Archivkopien von `F_ERLENBACH_1V_C2` (`.alt_v1_gebaut`, `.alt_vor15b`, `.alt_lava_biomfehler`);
  - `_alt/` mit einer `plan.json`;
  - der Feld-Instanzplan `C2/plan.json` (Kopie von `instanzen/C2/plan.json`);
  - `instanzen/C2.alt_v1` sowie `sw_elfenwald/G4.alt` und `_G3`.

| | Objekte im Pool | Kollisionseinträge | Gelände-Deltas |
|---|---|---|---|
| ohne Archivordner | 347 878 | 21 715 | 224 |
| **alter Exporter (16c) mit Archivordnern** | **368 068** (+20 190) | **23 963** (+2 248) | **227** (+3) |
| neuer Exporter mit Archivordnern | 347 878 | wie ohne | 224 |

Die Ausgabe des neuen Exporters mit Archivordnern ist bis auf `zusammenfassung.json` (Liste `eingaben.uebersprungen`)
byte-gleich mit der Ausgabe ohne Archivordner.

## 2. Fehler 2 – Geländedeltas doppelt

### 2.1 Lösung

- **Wann ein Delta nicht addiert wird** (`gelaende_laden()`):
  - wenn der Lauf unter **`--gebaut`** steht. Erlaubt sind die Gefälle-Lauf-ID, die Sehens-Ort-ID oder `SW_<ort>_<bach>`.
  - **automatisch**, wenn `sehens_einbau/A15_<lauf>/lauf.json` existiert und `nachgezogen` das Feld nennt.
    - Bei Plänen über mehrere Felder wird je Abschnitt geprüft. Alle Felder in `felder` des Abschnitts müssen genannt
      sein. Beispiel: `B_K1_WASSERFALL_WEST_01` liegt in B4 und C4.
    - Bei Sehens-Orten gilt `A15_<ort>/lauf.json` oder `A15_SW_<ort>_<bach>/lauf.json` gegen die `felder` des Orts.
- **Fehlende oder unklare `lauf.json`:**
  - Fehlt die Datei, gilt der Lauf als ungebaut.
  - Ist die Datei unlesbar oder fehlt das Feld in `nachgezogen`, wird das Delta addiert. Das Protokoll nennt die Datei
    dann unter `lauf.json ohne passendes Feld …`.
- **Wo der Exporter `sehens_einbau/` sucht** (dieselbe Regel gilt für die Pfade relativ zum Welt-Export):
  1. `--einbau DIR`;
  2. `<daten1m>/sehens_einbau`, lokal also `export/unreal/welt/sehens_einbau`;
  3. neben `--gefaelle`, also `export/unreal/welt/gefaelle` → `export/unreal/welt/sehens_einbau`;
  4. neben `--sw-ordner` bzw. `--sehens`.

  `--ohne-erkennung` schaltet die automatische Erkennung ab.
- **Annahme zum Format von `lauf.json`** (Funktion `nachgezogen_felder()`, mit 15 Formen getestet):

  | Form von `nachgezogen` | gilt als nachgezogen |
  |---|---|
  | `["C2", "C3"]` (auch klein geschrieben) | die genannten Felder |
  | `[{"feld": "C2", "ok": true, …}]` (auch `id`/`name`) | Felder ohne `ok`/`nachgezogen`/`fertig`/`erledigt` = falsch |
  | `{"C2": true \| {…}, "C3": false}` | Felder mit wahrem Wert |
  | `{"felder": ["C2"]}` | die Liste |
  | `"C2"` oder `"C2,C3"` | die genannten Felder |
  | `true` | alle Felder des Laufs |
  | `false`, `[]`, nicht vorhanden | keins |

  Steht `nachgezogen` nicht oben, wird in Unterobjekten bis Tiefe 3 gesucht, z. B. `{"gelaende": {"nachgezogen": […]}}`.
- **Ausgabe:**
  - Protokoll: `gebaut: F_ERLENBACH_1V_C2 (gefaelle) - 1 Gelaende-Delta(s) nicht addiert (sehens_einbau/A15_F_ERLENBACH_1V_C2/lauf.json, nachgezogen: liste)`.
  - `zusammenfassung.json`: `gelaende_deltas`. Dort stehen `addiert` und `nicht_addiert` sowie `gebaut[]` mit ID, Art,
    Quelle, Form und Feldern, dazu `lauf_json_ungebaut[]` und `gebaut_unbekannt[]` (unbekannte IDs aus `--gebaut`).
  - `back_liste.json`: `gelaende.gebaut` und `gelaende.deltas_ohne` (die weggelassenen Delta-Dateien).
- **Prüfer:**
  - Er rechnet das Gelände genau ohne `deltas_ohne`.
  - Er erkennt die gebauten Läufe außerdem selbst neu. Weicht das Ergebnis vom Export ab, meldet er eine WARNUNG
    (`lauf.json seit dem Export geändert?`).

### 2.2 Was das doppelte Delta wirklich verfälschte

- `lage` (`im_wasser`/`ufer`) und die Wasser-Kollision rechnen nur mit den Objekt-Bounds aus dem Plan und mit der Spline,
  also mit Wasserstand und Breite aus dem Plan. Das Gelände geht dort **nicht** ein. Deine C2-Einstufungen waren daher
  richtig.
- Das Gelände steckt nur im **Fingerabdruck** (`teile.gelaende`) und in `gelaende_max_cm`.
  - Doppelt gezählt wurde das Delta von C2 im SWR-Bereich `F_ERLENBACH_T00`: Becken und Fälle bis zu 7,2 m tief laut
    Plan-Abschnitt, bei dir bis −9,95 m.
  - Folge: Der Vergleich zwischen Planer und Editor hätte dort immer „geändert“ gemeldet.
  - `gelaende_max_cm` blieb gleich, weil die Deltas nur abgraben.

### 2.3 Gegenprobe (synthetisch)

**Aufbau:** Das Delta von `F_ERLENBACH_1V_C2` wird vor dem Export in die 2-m-Welt gestempelt (Skript im Scratchpad: es
ersetzt `daten.lade`). So sieht es lokal nach dem Bauen aus.

| Variante | `lage` aller 23 450 Objekte (903 an F_ERLENBACH) | Gelände-Fingerabdruck ≠ ungebaut | Prüfer |
|---|---|---|---|
| Welt gestempelt, **ohne** gebaut (doppelt) | gleich | `F_ERLENBACH_T00` | 0 FEHLER, 1 WARNUNG, sobald `lauf.json` existiert |
| Welt gestempelt, `--gebaut F_ERLENBACH_1V_C2` | gleich | **keiner** | 0 FEHLER |
| Welt gestempelt, `lauf.json` mit `"nachgezogen": ["C2"]` | gleich | **keiner** (Ausgabe = `--gebaut`) | 0 FEHLER, HINWEIS „gebaut“ |
| Export „gebaut“, aber Welt **ohne** Stempel geprüft | – | – | **FEHLER** `F_ERLENBACH_T00` |
| Sehens: `A15_SW_elfenwald_04_elfentreppe_zulauf/lauf.json` mit `{"H3": {…}}` | gleich | nur die 3 SWR-Bereiche, die das Fenster der Elfentreppe berühren | – |
| `--gebaut GIBT_ES_NICHT` | – | – | WARNUNG im Protokoll, steht in `gebaut_unbekannt` |

### 2.4 Aufrufe

Lokal mit automatischer Erkennung, wie bisher; `sehens_einbau/` liegt neben `gefaelle/`:

```
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle \
       --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt --aus export/unreal/welt/fluss_sim
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_pruefen.py export/unreal/welt/fluss_sim \
       --gefaelle export/unreal/welt/gefaelle --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt
```

Ausdrücklich gebaut, ohne `lauf.json`, bzw. ein anderer Einbau-Ordner:

```
python -I …/fluss_sim_export.py … --gebaut F_ERLENBACH_1V_C2
python -I …/fluss_sim_export.py … --einbau D:/…/export/unreal/welt/sehens_einbau
python -I …/fluss_sim_export.py … --ohne-erkennung --gebaut F_ERLENBACH_1V_C2 elfenwald_04_elfentreppe
```

## 3. Entscheidung zu 16c-Rückfrage 4: Töpfe gehören zum Gewässer

**Regel** (`regeln.gewaesser.topf`, Regeln Version 4):

- **Was ein Topf ist:** ein Sehens-See mit größter Ausdehnung unter 30 m (größter Abstand zweier Umrisspunkte), in den ein
  Sehens-Bach mündet oder aus dem einer abfließt.
- **Folgen:** Der Topf ist kein eigener `WaterBodyLake`. Die eine SWR des Gewässers füllt ihn.
- **Durchfluss:** Zulauf → Topf → Abfluss wird ein Gewässer, das nach dem obersten Bach heißt. Bei mehreren Zuläufen geht
  der längste weiter; in den Daten kommt das nicht vor.
- **Quelltopf:** Das Gewässer beginnt in der Topfmitte (`anfang.art = "topf"`).
- **Endtopf:** Das Gewässer endet dort (`muendung.art = "topf"`).
- **Spline:** Je Topf gibt es einen Punkt in der Mitte des Topf-Rechtecks auf dem Spiegel, mit Rolle `topf`.
  - Breite = größte Rechteckseite + 2 × 1 m. Damit schließt das SWR-Rechteck den Topf sicher ein; der Prüfer prüft das.
  - Tiefe aus `tiefe_m`, Tempo 10 cm/s.
- **Export:** Liste `toepfe[]` mit See, Art, `s_m`, Spiegel, Rechteck und `water_body_lake: false`, dazu ein Bereich mit
  `rolle: "topf"`.
- **Größere Seen** bleiben Seen und Mündungsziele: Biberstau 36 m, Karsee 34 m, Moränensee 32 m, Trunkensee 50 m.
- **Welt-Seen** bleiben unverändert, auch die 12 unter 30 m, denn sie sind keine Sehens-Treppen.

**Zahlen vorher/nachher** (2 m, alle Gewässer):

| | 16c (vorher) | 16d (nachher) |
|---|---|---|
| Gewässer | 196 | **187** |
| Sehens-Bäche → Gewässer | 42 → 42 | 42 → **33** (15 mit Topf) |
| SWR-Bereiche / Gewässer mit einer SWR | 211 / 188 | **202 / 179** (Welt unverändert 169 / 146) |
| Auflösung ≤ 512 / 513–1024 / 1025–2048 | 106 / 56 / 49 | 95 / 58 / 49 |
| Mündung See / Topf | 23 / – | 11 / 3 |
| Anfang See / Topf / Quelle | 25 / – / 168 | 5 / 10 / 169 |
| Kollisionseinträge (im Wasser) | 21 715 (20 806) | 22 025 (21 143): Objekte in den Töpfen |
| Hindernis-Akteure | 141 | 132 |
| Prüfer-HINWEIS „Fuß am Gewässerende“ | 7 | 5 |

| Topf-Gewässer | Bäche | Töpfe | Länge | SWR (Rechteck, Auflösung, Zelle) | Anfang → Mündung |
|---|---|---|---|---|---|
| `SW_elfenwald_04_elfentreppe_zulauf` | 6 | 5 (8,4–11 m) | 78,8 m | 60 × 52 m, 256, 0,235 m | Quelle → Bach |
| `SW_gletscher_06_gletschertoepfe_klammbach_oben` | 4 | 3 (4–6,4 m) | 138,5 m | 38 × 131 m, 544, 0,240 m | Quelle → versickert |
| `SW_heide_06_der_wollsackfall_klammbach` | 2 | 1 (11 m) | 113,1 m | 29 × 107 m, 448, 0,239 m | Quelle → versickert |
| 9 Quelltöpfe (Blautopf 20 m, Tosbecken 22 m, Gumpen, Schmelztümpel, Quelltopf …) | je 1 | 1 | | | Topf → … |
| 3 Endtöpfe (Strudeltopf, Hängetal-Gumpe, Schlenke) | je 1 | 1 | | | … → Topf |

`B_R_P2_M1_01` (Welt) beginnt am Blautopf. Sein Anfang heißt jetzt `topf` mit `gewaesser: SW_aue_07_blautopf_quellbach`.
Die Liste aller 21 Töpfe steht in `zusammenfassung.json` unter `toepfe.liste`. Beispiel im Repo:
`fluss_sim/sehens/elfenwald/elfenwald_04_elfentreppe/fluss_sim.json`.

## 4. Entscheidung zu 16c-Rückfrage 5: Vorschlagspunkte für offene Enden und Lücken

**Verfahren** (`regeln.gewaesser.vorschlag`). Die Spline bleibt unverändert; die Vorschläge stehen nur in
`muendung.vorschlag` und gesammelt in `fluss_sim/vorschlaege.json`.

- **Lücke (23):** gerade vom Spline-Ende bis 1 m hinter den Wasserrand des bekannten Ziels.
- **Offen (24):**
  1. Auf einem 4-m-Suchraster (Umkreis 1 500 m, Gelände = Welt + Deltas) geht es entlang des **steilsten Gefälles** (D8).
  2. Endet das in einer Senke, geht es weiter auf dem Weg des **geringsten Anstiegs** (Dijkstra, Kosten = Länge + 20 ×
     Anstieg).
  3. Ziel ist die erste Wasserzelle mit Spiegel ≤ Ende + 1 m: Gewässer-Streifen, See (ohne Töpfe) oder Meer.
  4. Nicht als Ziel zählen das eigene Gewässer, seine Zuflüsse und Gewässer, deren Mündungskette selbst offen endet.
     Sonst zeigten zwei offene Bäche aufeinander; das kam im ersten Lauf bei `B_R_M1_P0_01` ↔ `B_R3_R_M1_P0_01` vor.
- **Felder:**
  - `punkte`: x, y, z, Breite, Tiefe, Tempo. Der erste Punkt ist das Spline-Ende, die Punkte liegen höchstens 5 m
    auseinander. z = min(vorheriges z, Gelände), nie steigend und nie unter dem Spiegel des Ziels.
  - `ziel` (Art, ID, Spiegel, bei Gewässern `s_m`), `laenge_m`, `dz_m`.
  - `einschnitt_max_m`: wie weit das Gelände entlang des Wegs über dem Wasser liegt.
  - `kreuzt`: Wasser mit höherem Spiegel auf dem Weg.
  - `methode` und `begruendung`.

**Zahlen:**

| | Anzahl | Länge | Methode | Ziel |
|---|---|---|---|---|
| Lücke | 23 | 4,2–22,0 m (Median 9,4) | gerade | 14 Bach, 6 Fluss, 3 See |
| offen | 24 | 20,0–591,1 m (Median 136,6) | 7 steilstes Gefälle, 13 Gefälle + geringster Anstieg, 4 nur geringster Anstieg | 6 Bach, 6 Fluss, 9 See, 3 Meer |

**Ansehen vor dem Übernehmen** (`zusammenfassung.json` unter `vorschlaege`):

- **Durch höheres Wasser** (3): `B_R_M1_P0_01`, `B_R_M1_P0_02` und `B_R3_R_M1_P0_01` enden 4–6 m **unter** dem Spiegel von
  `F_HAUPTFLUSS_3` direkt daneben.
  - Der Vorschlag führt sie durch den Fluss zum See `S_R_M1_P0_00`, mit Einschnitt 5,7–7,5 m.
  - Besser: das Bachende in den Weltdaten auf den Flussspiegel heben und als Zusammenfluss anschließen.
- **Großer Einschnitt:**
  - `F_HAUPTFLUSS_2`: 591 m bis `F_HAUPTFLUSS_3`, Einschnitt 12,4 m. Das Ende in B4 hat keinen Anschluss.
  - Dazu `B_R3_K12_WUESTE_01` (3,9 m, 521 m bis zur Salzpfanne) und `B_K1_WASSERFALL_WEST_03` (3,0 m).
- **Gut** sind 38 von 47 mit Einschnitt ≤ 1 m. Beispiel: `B_R_M2_M2_01` erreicht über 75 m nur bergab das Meer.

```json
{"art": "offen", "methode": "steilstes_gefaelle", "ziel": {"art": "meer", "id": "meer", "spiegel_cm": 0.0},
 "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
 "punkte": [[-339650.0, -156850.0, 2873.8, 482.8, 38.6, 300.0], [-339650.0, -157250.0, 2512.5, 482.8, 38.6, 300.0], "… 20 Punkte",
            [-343250.0, -162850.0, 0.0, 482.8, 38.6, 300.0]],
 "laenge_m": 74.91, "dz_m": 28.74, "einschnitt_max_m": 0.0, "kreuzt": [],
 "begruendung": "offen: Verlaengerung entlang des steilsten Gefaelles (D8, 4-m-Raster) 75 m bis meer (Spiegel 0.0 m, Ende 28.7 m)"}
```

**Befund:** `B_R_P3_P0_01` und `B_R3_R_P3_P0_02` münden in den Weltdaten mit Lücke **ineinander**. Das ist ein Kreis, den
es schon in 16c gab: Beide enden 0,7 bzw. 1,1 m hoch nahe der Küste. Die Lücken-Vorschläge zeigen deshalb auch
aufeinander (siehe Rückfrage 3).

## 5. Lauf und Prüfung

- **Export** (2 m): 187 Gewässer in 180 Dateien, 47 Vorschläge. Laufzeit ~36 s; die Vorschläge brauchen davon ~15 s.
  Damit es so schnell geht, rechnet `Gelaende.delta()` nur noch die Punkte im Fenster jedes Deltas. Das Ergebnis ist
  bitgleich: alle 202 Fingerabdrücke wie vorher.
- **Prüfer:** 0 FEHLER, 0 WARNUNG, 60 HINWEIS. Die HINWEISE verteilen sich so: 24 × offen, 20 × Lücke in Fluss/Bach
  (+ 3 in See ohne HINWEIS), 8 × geteilt, 5 × Fuß am Ende, je 1 × Läufe, Vorschläge, Determinismus. 183 Dateien sind
  byte-gleich (`--vergleich`).
- **Neu geprüft:**
  - Pool und Gelände nur aus Lauf-Plänen.
  - Gelände ohne `deltas_ohne`.
  - Töpfe: Bereich `topf`; Punkte auf dem Spiegel (± 3 cm); SWR-Rechteck schließt den Topf ein; Größe < 30 m; nur in
    einem Gewässer; nicht mehr als See-Ziel; kein `WaterBodyLake`.
  - Läufe und Töpfe lückenlos.
  - Vorschläge: Beginn am Spline-Ende, nie steigend, Abstand ≤ 5 m, `laenge_m`, Ziel erreicht (Streifen, See oder Meer),
    gleich `vorschlaege.json`.
- **Gegenproben**, alle FEHLER mit Exit 1:
  - Töpfe: Topf nicht auf dem Spiegel, Topf ≥ 30 m, Rechteck ohne Topf, Topf ohne Bereich, Topf als `WaterBodyLake`,
    Mündung in einen Topf als See.
  - Vorschläge: steigt, beginnt nicht am Ende, Abstand 8 m, Ziel verfehlt, fehlt; `vorschlaege.json` weicht ab.
  - Gelände: „gebaut“ vermerkt, aber Welt ohne Stempel.
  - Die 10 Gegenproben aus 16c gelten weiter.
- **Beispiele im Repo** (`antworten/fluss_sim/`): `F_ERLENBACH`, Karsee, neu `elfenwald_04_elfentreppe`,
  `zusammenfassung.json`, `vorschlaege.json` (alle 47) und `back_liste_auszug.json` mit dem Kopf `gelaende`.

## 6. Was lokal zu tun ist

Commits: **`8d3d44d`** (Exporter, Prüfer, Regeln v4, README, Beispiele) und **`10f237f`** (Vorschläge: Wasserstand nie
unter dem Ziel), dazu der Commit dieser Antwort.

1. `git pull`. Die Archivordner dürfen in `gefaelle/` bleiben.
2. **Exporter und Prüfer auf 1 m** mit denselben Befehlen wie bisher (Abschnitt 2.4). Im Protokoll prüfen:
   - `uebersprungen: gefaelle/C2 - kein Lauf-Plan …` und je Archivordner eine Zeile;
   - `gebaut: F_ERLENBACH_1V_C2 (gefaelle) - 1 Gelaende-Delta(s) nicht addiert (sehens_einbau/A15_F_ERLENBACH_1V_C2/lauf.json, …)`;
   - erwartet: Pool und Kollision nur aus `F_ERLENBACH_1V_C2` und den übrigen echten Läufen (deine 532 Objekte an C2).
   - Steht stattdessen `lauf.json ohne passendes Feld …`, erkennt der Exporter dein Format nicht. Dann bis zur Anpassung
     `--gebaut F_ERLENBACH_1V_C2` nehmen und mir eine `lauf.json` schicken (Rückfrage 1).
3. **Bauwerkzeug (v3):**
   - Je Gewässer **einen** `WaterBodyRiver` aus `water_body.spline` und je `swr_bereiche[]` eine SWR. Der 16d-Text nennt
     noch „je SWR-Einheit aus den Abschnittspunkten“; das war v2.
   - Neu: Für die 21 Seen in `zusammenfassung.json` unter `toepfe.liste` **keinen** `WaterBodyLake` bauen (bzw. den
     vorhandenen entfernen).
   - `anfang.art` bzw. `muendung.art = "topf"` und Bereiche mit `rolle: "topf"` brauchen sonst nichts. Der breite
     Splinepunkt in der Topfmitte gehört dazu.
4. **Vorschläge** aus `vorschlaege.json` ansehen und übernehmen: Spline bzw. Weltdaten (`baeche_alle.json`) nachziehen.
   Die 9 mit Einschnitt > 1 m zuerst, vor allem die 3 durch `F_HAUPTFLUSS_3` und `F_HAUPTFLUSS_2`. Nach dem Nachziehen
   neu exportieren: Die Mündungen werden dann `fluss`/`bach`/`see`/`meer` statt `offen` bzw. „mit Lücke“.
5. Die Tests T1–T5 aus 16c bleiben wie geplant (lokal 205/206).

## Rückfragen

1. **Format von `lauf.json`:** Bitte eine echte Datei aus `sehens_einbau/A15_F_ERLENBACH_1V_C2/` schicken, oder kurz das
   Format von `nachgezogen`. Gelesen werden die Formen aus Abschnitt 2.1.
   - Bei Sehens-Orten nehme ich an: Ein `A15_SW_<ort>_<bach>/lauf.json`, das die Felder des Orts in `nachgezogen` nennt,
     heißt, dass das **Orts**-Delta eingestempelt ist.
   - Stempelt A15 bei Sehens-Bächen nur einen Teil des Orts, müssen wir die Regel verfeinern.
2. **Quell- und Endtöpfe:** Eingeschlossen sind auch 9 Quelltöpfe (z. B. Blautopf, Turmquelle-Tosbecken) und 3 Endtöpfe
   (Strudeltopf, Hängetal-Gumpe, Erlenbruch-Schlenke). Das Gewässer beginnt bzw. endet dort in der Topfmitte. Passt das,
   oder sollen nur Töpfe **zwischen** zwei Bächen (Treppen) zum Gewässer gehören? Dann wären es 9 statt 21 Töpfe, mit
   denselben Gewässerzahlen.
3. **Weltdaten statt Vorschlag?** Für die drei Bäche unter dem Spiegel von `F_HAUPTFLUSS_3` und für `F_HAUPTFLUSS_2` ist
   der Vorschlag nur eine Notlösung (Einschnitt 5,7–12,4 m). Sollen wir lieber die Bachenden in den Weltdaten anheben
   bzw. `F_HAUPTFLUSS_2` an `F_HAUPTFLUSS_3` anschließen? Das wäre Planer- bzw. Weltdaten-Arbeit. Dasselbe gilt für den
   Kreis `B_R_P3_P0_01` ↔ `B_R3_R_P3_P0_02`: zum Meer führen oder zu einem Bach verketten?
4. **16d-Nachtrag Punkt 2 (drei lange Bäche ungeteilt, Zelle 0,31–0,40 m)** ist noch nicht umgesetzt. Ihr wartet laut
   Nachtrag noch auf die Vergleichsbilder. Höchstzelle Bach global 0,40 m hieße: `B_R_P4_M2_04`,
   `B_K1_WASSERFALL_WEST_03` und `B_R_P3_P0_04` ungeteilt; `B_R_P3_P0_02` (0,48 m) bliebe geteilt. Genauso ginge eine
   Ausnahmeliste nur für diese drei. Sollen wir das nach euren Bildern umstellen?
