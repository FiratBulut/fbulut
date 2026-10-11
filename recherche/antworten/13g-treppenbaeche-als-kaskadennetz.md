# Antwort zu Auftrag 13g – Treppenbäche der Sehenswürdigkeiten als `wasser_koerper` (river + kaskadennetz)

Stand 11.10.2026. Code: Commit **`8175f8f`** (mit den Zwischenständen `88a66ec` und `0d40e67`). Diese Antwort steht
im Commit danach.

## Kurzfazit

- Jeder Bach mit einer Stufe ≥ 0,5 m hat in `orte.json` zusätzlich `wasser_koerper` im A15/14b-Format:
  - `river` für Strecken ≥ 15 m außerhalb der Stufenstrecken,
  - `kaskadennetz` je zusammenhängender Stufenstrecke,
  - Lauf-ID `SW_<ortid>_<bachid>`.
- Das betrifft **39 von 42 Bächen** mit **44 Kaskadennetzen** und **13 River-Stücken**.
- Die Netze werden mit `gefaelle_plan.bauen_wasser_A` gebaut. Die Funktion ist nur importiert, nichts in
  `skripte/gefaelle/` ist geändert. Grundlage sind die vorhandenen 13f-`stufen` und der 13f-Spiegel. Es gibt keine
  neue Planung.
- **Stufen unverändert gegenüber 13f:** Das Prüfskript `sehens_lib/stufen_vergleich.py` vergleicht die 2-m-Ausgabe
  dieses Stands mit `c945f93`. Ergebnis: **alle 42 Bäche „gleich“** (Lippe/Fuß x, y, z in cm, `fall_m`, `art`).
- Die in 13f vorgeschlagene Bündelung zu Fallketten (Frage 4) ist zurückgebaut.
- Prüfer mit den Netzregeln aus `gefaelle_pruefen.py`:
  - 2 m, alle 15: **0 FEHLER**, zwei Läufe byteidentisch;
  - synthetisch 1 m: **0 FEHLER**;
  - Selbsttest: **0 FEHLER**, mit drei neuen 13g-Fällen.
- Zwei Abweichungen, weil das Querprofil wie 13f bleibt (Rückfrage 1):
  - Bett-Regel: gemessen wird am tiefsten Bettpunkt, Mindestwert ≥ min(0,2 m; halbe Rezepttiefe).
  - Netzbreite = Wasserbreite im Gelände.

## Format

Neu im Bach-Eintrag (`orte.json` → `orte[].wasser[]`, typ `bach`). Alle bisherigen Felder bleiben: `punkte_cm`,
`stufen`, `furten` usw.

```json
"wasser_koerper_lauf": "SW_heide_06_der_wollsackfall_klammbach",
"wasser_koerper": [
  {"id": "…_KN0", "typ": "kaskadennetz", "s_m": [0.0, 16.42],
   "mittellinie": [[x_cm, y_cm, z_cm, breite_cm, tempo_cm_s, fallanteil, schaum, abstand_bett_cm], …],
   "mittellinie_felder": ["x_cm", "y_cm", "z_cm", "breite_cm", "tempo_cm_s", "fallanteil", "schaum", "abstand_bett_cm"],
   "knick": ["rampe", "becken", "lippe", "bogen", "wand", "fuss", …],
   "rand_ueberstand_m": 0.4, "zelle_m": 0.5, "anfang_unter_river_cm": 2, "ende_unter_river_cm": 2,
   "fuss_unter_spiegel_m": 0.3, "material": "/Game/Eldarien/Welt/Wasser/Stufenfall/MI_EL_Kaskade_SLW",
   "nanite": false, "schatten": false, "kollision": "keine",
   "stufen": ["…_S00"], "vorhang_an_stufen": [], "rampen_s_m": [[0.0, 13.93]],
   "effekte": [{"typ": "niagara", "asset": "/Game/NatureWaterFX/FX/NS_Impact_Small", "stufe": "…_S00",
                "pos_cm": [x, y, z], "cull_m": 20.0, "zweck": "Aufprall am Fuss (A15 2.9)"}],
   "anschluss_unten": …, "pruefung": {…}, "breite_bach_m": 2.6},
  {"id": "…_R0", "typ": "river", "s_m": [15.92, 34.33],
   "punkte": [[x_cm, y_cm, z_cm, breite_cm, tiefe_cm, tempo_cm_s], …],
   "punkt_typen": ["CURVE", "CURVE_CLAMPED", …, "CURVE"], "zone": "<Feld>_Wasserzone",
   "overlap_material_priority": 0,
   "anschluss_oben": {"an": "…_KN0", "ueberlapp_m": 0.5}, "anschluss_unten": {"an": "…_KN1", "ueberlapp_m": 0.5},
   "breite_bach_m": 2.6},
  …
]
```

So entstehen die Werte (Adapter `sehens_lib/bach.py: wasser_koerper()`, Aufruf in `rezept._bach_eintrag`):

- **Spiegelpunkte:**
  - Lippe und Fuß jeder 13f-Stufe genau aus `stufen` (oben/unten); bei einer Schnelle ist der Fuß eine `rampe`.
  - Dazwischen der geplante 13f-Spiegel alle 2 m (`becken`).
  - Die Mittellinie fällt monoton.
- **Netz-Strecken:**
  - Je Stufe ≥ 0,5 m ein Segment.
  - `kn_bereiche` (A15) fasst Segmente zusammen, wenn der River dazwischen kürzer als 15 m + 2 × 0,5 m wäre. Das
    Stück dazwischen kommt als Rampe ins Netz (15c).
  - Am Laufanfang und -ende gehen kurze Reste ebenfalls ins Netz.
- **Überlappung und Höhe:** Netz und River überlappen 0,5 m, das Netz liegt dort 2 cm unter dem River. Den Überfall
  an jeder Stufe (`bogen`, `wand`, `fuss`), Tempo, Schaum und `abstand_bett_cm` rechnet `bauen_wasser_A` wie in A15.
- **Netzbreite** = max(Bachbreite; 2 × (Uferprüfstelle − 0,4 m)): Der Netzrand (halbe Breite + 0,4 m) liegt genau an
  der Uferprüfstelle des 13f-Querprofils. Bei schmalen Bächen ist die Wasserfläche im Gelände breiter als
  `breite_m`, weil die Wasserkante mindestens 0,75 Zellen von der Mitte liegt. `breite_bach_m` nennt die
  Rezeptbreite.
- **Effekte (A15 2.9):**
  - `NS_Impact_Small` am Fuß jeder Stufe ≥ 1 m, Cull 20 m, die größten Stufen zuerst.
  - Höchstens 8 Niagara je Ort, die Rezept-Niagara mitgezählt.
  - Ein Vorhang (`vorhang_an_stufen`) nur an einem Einzelabsturz ≥ 3 m.
  - Die Effekte der Rezepte (13f) bleiben unverändert.
- Seen, Teiche und große Wasserfälle bleiben wie bisher.

## Je Biom

| Biom | Bäche | mit Stufe ≥ 0,5 m | Kaskadennetze | River ≥ 15 m | NS_Impact_Small |
|---|---|---|---|---|---|
| aue | 2 | 2 | 2 | 0 | 2 |
| bergwald | 4 | 4 | 4 | 0 | 10 |
| canyon | 2 | 1 | 1 | 1 | 0 |
| dschungel | 2 | 2 | 2 | 1 | 1 |
| elfenwald | 7 | 7 | 7 | 0 | 10 |
| fjord | 4 | 4 | 5 | 1 | 10 |
| frost | 1 | 1 | 1 | 0 | 3 |
| gletscher | 11 | 11 | 11 | 4 | 27 |
| heide | 2 | 1 | 3 | 2 | 0 |
| kueste | 0 | 0 | 0 | 0 | 0 |
| lava | 1 | 1 | 1 | 0 | 1 |
| oedland | 0 | 0 | 0 | 0 | 0 |
| sumpf | 1 | 0 | 0 | 0 | 0 |
| tundra | 4 | 4 | 6 | 4 | 10 |
| wueste | 1 | 1 | 1 | 0 | 1 |
| **Summe** | **42** | **39** | **44** | **13** | **75** |

Die meisten Bäche sind kurz und gestuft. Deshalb ist meist der ganze Bach ein Netz mit Rampen. Getrennte River gibt es
nur bei langen ruhigen Strecken, zum Beispiel heide_06 `klammbach` oder tundra_04 `schmelzfaden`.

## Stufen unverändert gegenüber 13f

Prüfskript `recherche/antworten/skripte/sehens_lib/stufen_vergleich.py`. Es vergleicht je Bach die Stufen zweier
`orte.json`: Lippe und Fuß in cm, `fall_m`, `art`.

```
python -I sehens_lib/stufen_vergleich.py --ordner <aus> <aus> _neu _basis
  (<aus>/<biom>_basis = Planer im Stand c945f93, <aus>/<biom>_neu = dieser Stand, je 2 m)
Summe: gleich 42
```

Was ich dafür gegenüber dem ersten Nachtrag zu 13f zurückgenommen oder weggelassen habe (Details im Abschnitt
„Entscheidungen Koordinator“ in `13f-p2-1m-korrekturen.md`):

- **Fallketten (Frage 4):** ganz zurückgebaut.
- **Spiegelplanung:** rechnet mit den 13f-Werten (Ring + 0,15 m, hebt ≤ 1 m). Die Reserve für das Ufer (+ 0,2 m,
  hebt ≤ 2 m, Wasserkante aufgefüllt) wirkt nur im Stempel.
- **Linienführung:** Schleifenkappung, Abstiegsabstände und die A9-Verlängerung sind wie 13f. Die neue Verlängerung
  zu kurz versickernder Läufe hängt nur hinten an. Sie lässt den 13f-Lauf Punkt für Punkt gleich und greift nur,
  wenn sie sinnvoll ist.
- **Weggelassen, weil sich die Stufen ändern würden:**
  - heide_06 `auslauf` → `B_R2_R_P3_P0_01`: die 0,34-m-Schnelle fiele weg;
  - bergwald_05 Klammbach → `auto`: drei Stufen verschoben sich um bis zu 3 cm;
  - eine neue Linie für canyon_07 `abfluss`: 2 neue Schnellen;
  - eine neue Linie für lava_03 `rinnsal`: 1 cm bzw. 0,01 m Fall.
- Die übrigen Punkte (Mündungskorridor ± 0,5 m, gletscher_06-Ufer, `im_bestand_stempeln` für fjord_02) ändern nur
  das Gelände, nicht Spiegel und Stufen.

Den Vergleich gibt es nur auf 2 m. Für den alten Stand fehlt ein synthetischer 1-m-Lauf. Die Logik ist für beide
Raster dieselbe; lokal auf 1 m kann der Vergleich mit zwei 1-m-Läufen wiederholt werden.

## Prüfer

`sehens_pruefen.pruefe_wasser_koerper` läuft für jeden Bach in `pruefe_baeche`:

- **Pflicht:** Ein Bach mit Stufe ≥ 0,5 m hat `wasser_koerper` (FEHLER), die Lauf-ID ist `SW_<ortid>_<bachid>`.
- **Strukturregeln:** `gefaelle_pruefen.pruefe_wasser` (importiert, ohne Welt):
  - Mittellinie bzw. Spiegel monoton;
  - `knick` so lang wie `mittellinie`;
  - Nachbarn überlappen genau 0,5 m, sonst nichts;
  - kein River < 15 m;
  - River ohne Überlappung in der Draufsicht;
  - jede Stufe ≥ 0,5 m in einem Netz;
  - Stufe ≥ 1 m ohne Niagara oder Vorhang: WARNUNG.
- **Bett und Ufer** auf dem Gelände nach dem Stempel, an den Beckenpunkten außerhalb der Stufen (`nahe_stufe`):
  - Ufer am Netzrand ≥ Spiegel + 0,1 m, wie in `gefaelle_pruefen` (`ufer_proben`, 2-m-Zuschlag 1 m);
  - Bett: tiefster Bettpunkt quer ≥ min(0,2 m; halbe `tiefe_cm`), siehe Rückfrage 1;
  - ausgenommen sind wie bei A12 Furten ± 1,5 m, die offene Mündung, die Stufenzonen ± (0,5 + 0,75 Zellen) und
    1,5 m um eigene Seen.
- **Selbsttest Schritt 11:** Format und Lauf-ID, jede Stufe im Netz bei 0 FEHLER. Kaputte Fälle (Mittellinie steigt,
  River < 15 m) ergeben FEHLER.

Ergebnis:
- 2 m: 0 FEHLER in allen 15 Biomen, zwei Läufe byteidentisch (`diff -r`).
- Synthetisch 1 m: 0 FEHLER.
- Neue WARNUNGEN „n Stufen ≥ 1 m ohne Niagara und ohne Vorhang“: Die Grenze von 8 Niagara je Ort reicht an langen
  Treppen nicht für jede Stufe (zum Beispiel fjord_02, gletscher_02, tundra_04). Dort gibt es nur Schaum im Netz.
- Testbilder erneuert.

## Rückfragen

1. **Bett-Regel und Netzbreite:**
   - Mit dem 13f-Querprofil (Wasserkante innen, 35°-Böschung, Bett = Spiegel − `tiefe_cm` mit 8–30 cm) misst der
     A15-Mittelwert über ± 30 % der Breite die Böschung mit.
   - Bei Bächen mit `tiefe_cm` < 20 ist 0,2 m außerdem gar nicht möglich, ohne das Querprofil zu ändern.
   - Ich prüfe deshalb am tiefsten Bettpunkt gegen min(0,2 m; halbe Tiefe). Die Netzbreite folgt der Wasserbreite im
     Gelände.
   - Passt das für `a15_einbau.py`, oder sollen die Netze `breite_m` des Rezepts behalten und ich das Bett vertiefen?
     Das wäre eine Änderung am Querprofil.
2. **Niagara-Grenze:**
   - Bei langen Treppen reicht „höchstens 8 je Ort“ nicht. Beispiel tundra_04 `schmelzfaden`: 16 Stufen ≥ 1 m
     ohne Impact.
   - Die übrigen Stufen haben nur Schaum im Netz (WARNUNG).
   - Ich zähle je Ort; A15 rechnet „gleichzeitig“ mit dem Cull-Radius. Soll ich das genauso rechnen? Dann bekämen mehr
     Stufen einen Impact.
3. **Weggelassene 13f-Nachträge** (heide_06-Anschluss, bergwald_05 `auto`): Dürfen sie die Stufen dieser zwei Bäche
   ändern? Der Code ist vorhanden; es ist je eine Rezeptzeile.
