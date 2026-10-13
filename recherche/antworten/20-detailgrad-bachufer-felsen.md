# Antwort 20 – Detailgrad Bachufer: Felsen, Schutt, Stapel, Ritzen-Bewuchs, Wasserkante (Talkaskade p2)

Stand 13.10.2026. Bezug: `auftraege/20-detailgrad-bachufer-felsen.md` (Ferat 65da488), dazu 16h Nachtrag 6h (Dichte-Zensus,
`auftraege/daten/dichte/dichte_vergleich.md`), 6c/6e/6f (Bettplan), N5 (Hindernisfilter), Antwort 21 (Grenze 10 m, Netzform-Regel).

**Kennzeichnung:**
- [Ferat]: eure Zählung oder Messung (Auftrag 20 §0–§7, 6h)
- [Projekt]: unsere Regeln bzw. Daten
- [Plan]: aus `plan_p2_talkaskade.json` gezählt
- [Ableitung]: geschlossen, nicht belegt
- [Liste]: steht so in Ferats Fab-Bibliothek (nur Titel, keine Anbieter- oder Preisangaben)

**Dateien:**
- Regeln: `skripte/detailgrad/detailgrad_regeln.json`
- Planer: `skripte/detailgrad/detailgrad_plan.py`, Bilder: `skripte/detailgrad/detailgrad_bilder.py`
- Plan: `skripte/detailgrad/plan_p2_talkaskade.json`
- Bilder: `detailgrad/querschnitt_ufer.png`, `detailgrad/draufsicht_10m.png`, `detailgrad/stapel_beispiel.png`
- Welt: `skripte/p2_bett/p2_bett_welt.py --instanzen-plan` (neu)
- Bettplan angepasst: `skripte/p2_bett/p2_bett_regeln.json`, `p2_bettplan.py`, Ausgabe `p2_bett/bettplan_p2.json`

## Kurzfazit

- **Regeln und Plan sind fertig.** Der Prüfer meldet 0 FEHLER und 0 WARNUNGEN, zwei Läufe sind byte-gleich (Hash `402247df44ee`).
  Der Bettplan bleibt bei 0 FEHLER, das Gelände ist unverändert (Hash `f274fd1b66d7`).
- **Der Plan deckt die Talkaskade s 390–578 ab, beide Ufer, je 0–10 m ab der Wasserkante.**
  - Gesamt: 7 661 Instanzen, davon 545 mit Kollision. Dazu kommt der Bettplan mit 645 / 149.
  - Summe: 8 306 Instanzen und 694 Kollisionen. Das sind 18 % bzw. 23 % des Feldbudgets C2 (45 000 / 3 000).
- **Ferats Zensus (6h) ist eingebaut:** Das Problem ist die Komposition, also große Blöcke gestapelt statt mehr Kleinzeug.
  - **Neue Rolle `stapel`:** 2–4 Blöcke von 1,5–5 m, überlappend, je 10 m 2 Stapel am Prallhang und 1 am Gleitufer.
  - **Felsdeckung** (Obergrenze wie im Zensus): 130–139 % im Band 0–10 m. Zum Vergleich: Talkaskaden-Fenster heute 1,2 %, RA2 378 %.
    41–47 % dieser Deckung kommt aus stehenden Blöcken.
  - **Netzvielfalt:** 47 verschiedene Netze. Die Demo-Karten nutzen 35–53, das C2-Fenster 181.
  - **Kleinzeug:** am unteren Ende der Referenz (K2 50–65 je 10 m).
- **Je 10 m und Seite** (Band 0–3 m, Median, Spanne) [Plan]:
  - Bestand: Stein 0,3–1 m 27 (26–34); Block 1–3 m 4 (3–6); Schutt 0,1–0,3 m 60 (52–68); Fuß im Wasser 3 (2–4).
  - Bedeckung: Kante 0,88, Uferband 0,79, Hang 3–10 m 0,34.
  - Lage: Kontakt 97 %, ≥ 1/3 eingegraben 94 %.
  - Bewuchs: Bewuchs in Ritzen 100 %, Grasbüschel 8,5; Farne am Gleitufer 3.
- **C.3 entschieden:** „Gras 60–80 % über die Kante“ fällt weg. Die Referenz zeigt nackten nassen Stein.
  - Überhang-Gras nur in Graslücken, auf 5–10 % der Gleitufer-Kante (Plan: 7,6 % / 5,5 %). Am Prallhang 0.
  - Der Grasfuß liegt ≥ 0,3 m über dem Spiegel.
- **Punkt 6 (Schaum):** Im Bach gibt es keinen weißen Kragen und keinen Schaum, außer an Fällen.
  - Der „Kragen“ wird eine dunkle **Nasslinie im Steinmaterial** (`MF_EL_Nasslinie`).
  - Die Schürze an Fällen kommt aus Nature Water FX (`NS_Impact_Small`, gekauft), kein Niagara je Hindernis.
  - Die Wasseroberfläche (V20a, Normalen nach Tempo) folgt Antwort 6h.
- **Kaufen:** nichts. Alle Kandidaten für §7 Punkte 1–5 stehen schon in Ferats Fab-Bibliothek; sie müssten nur importiert werden.
  Der Plan braucht keinen davon, er läuft vollständig aus dem Inventar.
- **Erst der Steinsatz, dann der Bewuchs:**
  1. Bettplan neu laufen lassen.
  2. Steine und Platten setzen.
  3. Stapel, Wände und Fels setzen.
  4. Nasslinien-MIs bauen.
  5. Schutt setzen.
  6. Bewuchs setzen.
  7. Gehölz setzen.
  - Prüfzahlen je Schritt stehen in §5.

## 1. Regeln „Detailgrad Bachufer“

**Grenze:** Dieser Plan gilt von der Wasserkante bis 10 m. Darüber gilt Antwort 21; sie setzt in 0–10 m nichts.
**Zählweise:** je 10 m Uferlänge und **je Seite**. Klassen K1–K4 werden im Band 0–3 m gezählt (wie Ferats Zähltabelle §0). Abstand d = außen ab der Bettkante.

### 1.1 tundra / Talkaskade C2 (gerechnet)

| Element | Wert | Prüfung (Plan je 10 m und Seite) | gegen Ferats Zielspalte |
|---|---|---|---|
| Bedeckung Kante 0–1 m | 3D-Stein ≥ 75 % (Prallhang ≥ 85 %), Erde ≤ 5 % | 0,77–0,98 (Median 0,88); Prallhang 0,89–0,90, Gleitufer 0,81–0,82 | ≥ 70 % / Prallhang ≥ 85 %: **bestätigt**, Kante etwas strenger |
| Bedeckung Uferband 1–3 m | ≥ 65 % (Prallhang ≥ 75 %), Erde ≤ 10 %, Rest Gras/Farn in Lücken | 0,69–0,98 (0,79) | zusammen 0–3 m ≈ 70 % (Gleitufer) bzw. ≈ 80 % (Prallhang): bestätigt |
| Bedeckung Hang 3–10 m | 3D ≥ 30 % (Stapel, Gruppen, Platten); den Rest decken die Felsschicht im Gelände, Moos und Grasfilz | 0,32–0,45 (0,34) | „≥ 80 % Deckung“: **korrigiert**: 3D nur 30 %, die übrigen 50 % kommen aus Material und Gras (im Prüfbild prüfen) |
| K1 Kies < 0,1 m | 5–10 | 5–10 (8) | Referenz nicht zählbar; Zensus 6h: weniger Kleinzeug |
| K2 Schutt 0,1–0,3 m | 50–65, mindestens 2 × K3, höchstens 85; ohne Schuttband | 52–68 (59,5) | 50–100: **bestätigt, unteres Ende** (6h) |
| K3 Stein 0,3–1 m | 26–36; Aufteilung: Haufen 18–26, Saum in Lücken 4–8, Hang 3–10 m extra 5–8 | 26–34 (27); Hang 5–14 | 25–40: bestätigt |
| K4 Block 1–3 m | 3–5 | 3–6 (4) | 3–6: bestätigt |
| **Stapel** 1,5–5 m (neu, 6h) | Prallhang 2, Gleitufer 1 je 10 m. Je Stapel: 2–4 Blöcke (Basis 3–5 m, Nachbarn 2–3,5 m), Abstand 0,35–0,55 × mittlere Größe (überlappend), 30–50 % eingegraben, am Prallhang 1 Block in 2. Lage | 56 Stapel, 210 Blöcke; Felsdeckung 130–139 %, davon stehende Blöcke 41–47 % | neu, aus dem Zensus |
| Fels > 3 m | 1–2 je 50 m am Prallhang (Felsformation 5–6 m), dazu Wandmodule | 5 Felskörper, 27 Wandmodule | „je 50 m ≥ 1“: bestätigt |
| Verhältnis | K2 ≥ 2 × K3; K3 : K4 = 6–12 | 59,5 : 27 = 2,2; 27 : 4 = 6,8 | „≥ 3×“: **ersetzt** durch ≥ 2× (gezählt sind 1,5–6 : 1) |
| Form | kantig/plattig ≥ 70 %, gerundet ≤ 30 %; 3 Größenstufen 0,35 / 0,55 / 0,8 m | gerundet ≈ 5 % der Steine | bestätigt |
| Netzform | Steine > 1,5 m nur mit max(x, y) / z ≥ 1,4 (nie würfelig oder stehend) | im Prüfer, 0 Verstöße | Projekt (Antwort 21, Runde 5) |
| Kontakt | ≥ 60 % der Steine > 0,3 m berühren einen Nachbarn | 0,90–1,0 (0,97) | bestätigt |
| Einbettung | ≥ 50 % zu ≥ 1/3 der Netzhöhe. Je Klasse: K2 40–60 %, K3 33–50 %, K4 35–50 %, Platten 60–80 % | 0,82–1,0 (0,94) | bestätigt |
| Haufen-Rhythmus | 5–15 Stück je Haufen. Länge: Prallhang 2,5–5 m, Gleitufer 1,5–3,5 m. Lücke: Prallhang 0,8–2 m, Gleitufer 1,5–3 m. Haufen reichen von der Kante bis 3 m | 77 Haufen, 5–15 Stück (Median 11), Ø 3,0 m lang, Ø 1,8 m Lücke | bestätigt |
| Stapelung im Haufen | 2. Lage: Prallhang 35 %, Gleitufer 20 % der Steine ≥ 0,45 m, um 25–45 % versetzt, 35 % der Höhe in der 1. Lage verkeilt. Kippung je Haufen 10–25°, je Stein ± 20°. Ab 2,5 m Länge eine Bodenplatte | 112 Steine in 2. Lage | bestätigt |
| Schutt in Fugen | je Stein eine Fuge zum nächsten Nachbarn mit 1–2 Stück; restliches K2 ≤ 1 m am Stein | Bild `stapel_beispiel.png`: 17 Fugenstücke auf 14 Steine | „≥ 2 Lagen?“ siehe §7 |
| Begleiter | um jeden Block ≥ 1 m: 3–6 Steine im Umkreis 2 m und 6–12 Schutt im Umkreis 1 m; vorhandene zählen mit | im Planer | „≥ 5 Begleitsteine“: siehe §7 |
| Schuttband | ab Wandhöhe 1,5 m; 1–1,5 m breit, 10–15 je m², 2 Lagen nur hier | 0 im Median, bis 156 je 10 m an Wänden | bestätigt (> 200 nur an 6–8-m-Wänden) |
| Wand | Wandmodule ab 1 m Höhe und ≥ 38° mittlerer Neigung; Flächen > 45° zu ≥ 90 % Fels | 27 Module (`SM_ForestRockSlab_01`), ≈ 15 % der Uferlänge | siehe §7 (Erdwände ≤ 38°) |
| Fuß im Wasser | 2–3 je 10 m, 0,5–1,4 m, d −0,45…+0,05 m, Oberkante 0,15–0,4 m über dem Spiegel (z absolut) | 2–4 (3) | „≥ 3“: bestätigt mit 2–3 (dazu kommen Lippen- und Eckblöcke des Bettplans) |
| Kantensaum | Steine 0,3–0,6 m nur in den Haufen-Lücken, alle 0,6–0,85 m, d −0,1…0,6 m; dazu Kantenplatten 1,0–1,5 m; Erdkante ≤ 5 % | Bedeckung Kante (oben) | bestätigt |
| Grasnarbe (C.3) | Überhang nur in Graslücken 0,8–1,5 m, 5–10 % der **Gleitufer**-Kante, Prallhang 0; Grasfuß ≥ 0,3 m über dem Spiegel; sonst Gras ≥ 1 m hinter der Steinkante | links 7,6 %, rechts 5,5 %; 20 Büschel | C.3 „60–80 %“ **ersetzt** |
| Ritzen-Bewuchs | ≥ 80 % der Büschel und Farne im Band 1–3 m ≤ 0,3 m an einem Stein ≥ 0,3 m. Gras 6–10 je 10 m, ≤ 0,6 m hoch, 30–50 % trocken | Ritzenanteil 1,0; Gras 6–11 (8,5) | 5–8: leicht **angehoben** (Referenz 10–15) |
| Farne | Gleitufer 2–3 je 10 m, d 1–3 m, an Steinen ≥ 0,5 m; Nordufer zusätzlich 0–1 (das Weltwerkzeug lässt Südufer-Farne weg) | Gleitufer ≈ 3, Prallhang ≈ 0,6 | bestätigt; siehe §7 |
| Moos/Flechte | 0 % unter 1 m über dem Spiegel, voll ab 1,5 m. Auf Steinen als Material-Auflage (`MI_EL_Auf_*`, 30–50 % der Steine, Flecken 20–60 %); am Boden 3–6 Polster je 10 m | Prüfer: Moos unter 1 m = FEHLER, 0 | bestätigt |
| Busch | 1–2 je 10 m, d 2–6 m, am Stein | 1–3 (2) | 1–3: bestätigt |
| Gehölz | 1 Gruppe je 50 m und Seite, 2–3 Bäume, Fuß 2–6 m, Neigung ≤ 30°, 2–3 Steine am Fuß | 17 Bäume | bestätigt (Erle fehlt, §4) |
| Lesbarkeit aus 30 m | ≥ 10 Einzelformen ≥ 0,5 m je 10 m (1. Lage) | 21–38 (30) | bestätigt |
| Sichtweite (cm) | K1 4 000, K2 9 000, K3 25 000, K4/Stapel 50 000, Platte 30 000, Gras 9 000, Farn 15 000, Moos 6 000, Busch 30 000; Wand, Fels und Gehölz 0 (immer) | in `plan.json` je Datei | – |
| Kollision | ab 0,8 m bei Stein, Block, Stapel, Wand, Fels, Gehölz | 545 | Auftrag |
| SWR-Hindernis | N5-Filter: Steine ≥ 0,4 m im Wasser oder ≤ 1 m daneben, nie Block, Stapel, Wand, Fels, Platte, Pflanzen; Teil ≤ 40 % der Bettbreite, je Meter ≤ 50 % (die Hindernisse des Bettplans zählen mit) | 264 (Stein 215, Fuß-Stein 49) | N5 |
| Vielfalt | je Rolle 2–6 Netze, gesamt ≤ 55 | 47 | 6h |

### 1.2 Andere Biome (Ableitung, nicht gerechnet; Prüfung wie tundra)

| Biom | Abweichung von tundra |
|---|---|
| heide | Bedeckung 0,55 / 0,35 / 0,10; K3 20–28; Farne 1–2; Stapel 1 / 0,5 |
| bergwald | Bedeckung 0,60 / 0,40 / 0,15; Farne 3–5 an beiden Ufern; Moos ab 0,7 m; Gehölz 2–3 Gruppen je 50 m; Totholz 1–2 je 20 m; Stapel 1,5 / 0,5 |
| aue | Bedeckung 0,30 / 0,15 / 0,05; K3 8–14; K4 0–1; Kiesbank 40–70 % am Gleitufer; Gras-Überhang 20–40 %; Stapel 0,5 / 0 |
| elfenwald | wie bergwald; Moos ab 0,3 m, 60–90 % der Steine mit Flecken |
| dschungel | wie bergwald; Bedeckung 0,40 / 0,20 / 0,05; Wurzeln 2–4 je 10 m |
| wueste | kein Moos, keine Farne, Gras 1–3; Bedeckung 0,60 / 0,50 / 0,30; Stapel 2 / 1 |

## 2. Plan p2-Talkaskade

### 2.1 Bilder

- `detailgrad/querschnitt_ufer.png`: Querschnitt am Prallhang s 545 mit den Zonen Kante, Uferband und Hang sowie der Grenze zu Auftrag 21. Dazu die Tabelle der Stückzahlen je Klasse und Zone im Abschnitt s 540–550.
- `detailgrad/draufsicht_10m.png`: s 540–550 links. Leiste mit dem Haufen/Lücken-Rhythmus und den Graslücken; Steine nach Klasse, 2. Lage blau, Platten, Stapel, Ritzen-Bewuchs.
- `detailgrad/stapel_beispiel.png`: Haufen 8 links, s 433–436, von der Seite und von oben.
  - 10 Steine in der 1. Lage, 4 in der 2. Lage, 17 Stück Fugenschutt, 1 Bodenplatte.
  - Kippung 8–20°, 1. Lage zu 35–49 % eingegraben.

### 2.2 Format und Weg in die Welt

- **`plan_p2_talkaskade.json`** ist nach Netz gegliedert wie FORMAT §3 `dateien`.
  - Je Netz: Pfad, Ebene, Rollen, Kollision, Sichtweite, Nanite, `material_vorschlag`.
  - Spalten je Eintrag: `s_m, u_m, skala, yaw_rel_grad, kipp_grad, einbettung, groesse_m, z_plan_m, swr_hindernis, nr, z_absolut, z_rel_m, rolle, seite, d_m, haufen, lage`.
  - Die Koordinaten s/u sind dieselben wie im Bettplan.
- **Höhe z:**
  - Bei `z_absolut` gilt der Wert absolut (Fuß-Steine).
  - Bei `z_rel_m` gilt Gelände + z_rel (2. Lage, Überhang-Gras).
  - Sonst gilt Gelände − Einbettung × Netzhöhe.
- **Weg in die Welt:**
  ```
  python -I p2_bett_welt.py --lauf lauf_p2.json --welt export/unreal/welt \
                            --instanzen-plan recherche/antworten/skripte/detailgrad/plan_p2_talkaskade.json
  ```
  - Es schreibt `<welt>/detailgrad/ERLENBACH_P2/instanzen/<Feld>/plan.json` und `<Netz>.f32` (FORMAT §3, Ebene `detailgrad`, FT-Präfix `FT_EL_DG_`).
  - Das Gelände ist Ist + Delta aus `bettplan_p2.json`.
  - Der Selbsttest prüft z für alle drei Fälle (`instanzen_plan_z_ok: true`).
- **Drehung:** Platten liegen in der Böschung. `yaw_rel` ist ±90° zum Wasser, `kipp` entspricht der Neigung (kipp > 0 heißt Nase nach unten wie in `quat_yaw_pitch`).
- **Reihenfolge-Falle Feldhöhen:**
  - Erst `p2_bettplan.py`, dann `detailgrad_plan.py`.
  - Danach `p2_bett_welt.py` zweimal: einmal Gelände, einmal `--instanzen-plan`.
  - Beide Läufe brauchen dieselbe `hoehe.f32`.
  - Nach jeder Bett- oder Feldhöhenänderung alle vier neu laufen lassen. Der Plan rechnet aus dem Gelände nach 6f; die Welt setzt auf die aktuelle Höhe plus Delta.
- **Durchbruch und Bergrinne:** nicht gerechnet (6d: später). Der Planer nimmt sie auf, sobald der Bettplan dort Abschnitte hat.

### 2.3 Budget und Dichte

| Kennzahl | Plan Talkaskade (Band 0–10 m, je Seite) | C2-Fenster heute [Ferat 6h] | RA2 [Ferat 6h] |
|---|---|---|---|
| Netze je 100 m² | 201 / 206 | 24,0 | 8,7 |
| davon < 0,5 m | 123 / 130 | – | – |
| Felsdeckung % (Obergrenze, Überlappung mitgezählt) | 139 / 130 | 1,2 | 378 |
| Anteil Deckung aus Netzen ≥ 1 m | 0,91 / 0,90 | – | – |
| Anteil Deckung aus stehenden Blöcken (ohne Platten) | 0,47 / 0,41 | – | – |
| verschiedene Netze | 47 | 181 | 53 |

- **Feld C2:**
  - Detailgrad 7 661 Instanzen und 545 Kollisionen, Bettplan 645 / 149, zusammen 8 306 / 694.
  - Das ist 18 % bzw. 23 % von 45 000 / 3 000.
  - Nicht enthalten: bachdekor (Bett) und Landschaftsgras.
- **Hochgerechnet auf den ganzen Lauf p2** (788 m, gleiche Dichte): ≈ 32 000 Instanzen [Ableitung]. Das geht nicht ins Budget.
  - Volle Dichte daher nur in der Talkaskade und an Sehens-Stellen.
  - Im übrigen Lauf: K2 halbieren, keine Hangplatten, Stapel nur am Prallhang. Das ergibt ≈ 40 % [Ableitung].
- **Die Dichte von ≈ 200 je 100 m²** liegt am schmalen Nahband. Gut 60 % davon ist Kleinzeug unter 0,5 m, und zwar die Referenzzahl K2.
  Wird das Budget knapp, zuerst K2 auf 40 senken (Rückfrage 2).

## 3. Palette, Dichten, geänderte Regeln

### 3.1 Netze je Rolle (Anzahl im Plan) und Material

| Rolle | Netze (Anzahl) | MI-Vorschlag (erst setzen, wenn die MI existiert) |
|---|---|---|
| stein (K3) | `SM_namaqualand_boulders_01_b_NN` 227, `SM_stones_01_2` 189, `_01_a_NN` 168, `SM_stones_01_3` 161, `xjijbgx` 144, `pjcxN` 111, `skjsL` 106, `pkeeM` 91, `texndcpda` 86, `SM_mountain_rock_small_01_1/_2` 63 | Fab: `MI_EL_<id>` auf `M_EL_Fels_MS2`; Namaqualand: `MI_EL_NL_namaqualand_*` grau; Forest: `MI_EL_NL_SM_stones_01_*` als MS2-Kopie |
| fussstein | `namaqualand_boulders_01_b` 17, `xjijbgx` 14, `SM_stones_01_2` 10, `pkeeM` 8, `skjsL` 8 | wie stein, Nasslinie Pflicht |
| block (K4) | `skjsL` 56, `SM_mountain_rock_big_01_5` 39, `_01_1` 36, `pkeeM` 35 | Mountain: `MI_EL_NL_mountain_rocks_big_01` (wie 6f) |
| **stapel** | `SM_mountain_rock_big_02_8` 42, `_02_1` 40, `_02_5` 35, `SM_ground_rock_03_03` 35, `SM_flat_rock_02` 31, `_02_3` 27 | `MI_EL_NL_mountain_rocks_atlas_01/_02`, `MI_EL_NL_rocks_atlas_01_Needless`, `MI_EL_NL_Flat_rock_01` (auf `M_EL_Mountain_NL`) |
| platte | `SM_NordicBeachRockyGround_02`, `SM_TundraRockyGround_01`, `SM_ErodedRockyGround_01` (1 172) | vorhandene `MI_EL_*` (MS2) |
| wand / fels | `SM_ForestRockSlab_01` 27; `SM_ForestRockFormation_05/_06` 5 | vorhandene `MI_EL_*`, dazu Auflage `_tundra` |
| schutt / kies | `SM_stone_04/06/09`, `SM_namaqualand_rocks_01_a_NN` (je ≈ 930); `SM_stone_01/02/07` (282) | `MI_EL_NL_*` (Mountain); Namaqualand grau |
| gras_ritze / gras_kante | `SM_grass_bush_01` 93, `SM_wk2oaeyqx_VarA` 90, `_VarE` 72, `_VarI` 63; Kante: `SM_GrassyEmbankment_01`, `SM_grass_bush_01` | 30–50 % als `MI_EL_<Netz>_trocken` (Kopie mit braunem Tint) |
| farn | `SM_EagleFern_S_02`, `SM_SilverLadyFern_01/_03` (66) | – |
| moos_boden / busch / gehoelz | `SM_moss_01/02`; `SM_grey_willow_01`, `SM_dwarf_pine_small_01`; `SM_Forest_pine_tree_00_B/_C`, `Big_Tree_Birch_01` | – |

- **Neu in der Bachpalette:**
  - die Stapel-Netze (Mountain `big_02`, `flat_rock_02`, `ground_rock_03_03`);
  - `SM_ForestRockSlab_01` als Wandmodul;
  - Namaqualand grau als kantiger Schutt und Kleinstein;
  - die Fab-Platten `texndcpda`, `pjcxN`.
- **Aus der Palette genommen** wegen Vielfalt (6h): die übrigen Fab- und Megascans-Steine. Sie stehen unter `netze_reserve` in den Regeln.

### 3.2 Welche Regeln sich ändern (Werte in `detailgrad_regeln.json` → `aenderungen_andere_regeln`)

**Bettplan (`p2_bett_regeln.json`), schon gerechnet:**
- `ausstattung_6e.aktiv_20`: In der Talkaskade sind Kantengras, Ufermoos und Farne aus, das übernimmt dieser Plan. Totholz bleibt (5).
- `bloecke.randblock.anteil` 0,4 → 0, das übernehmen Haufen und Stapel.
- Der Bettplan behält Lippen 158, Keystones 88, Eckblöcke 58, Beckenblöcke 5, Kies 331 und Totholz 5. Gelände unverändert.

**bachdekor (`bachdekor_swr_regeln.json`, bei euch lokal):**
- In der Talkaskade setzt bachdekor nur noch das Bett. Diese Uferklassen sind dort aus: `kiesel` ufer/saum, `randstein`, `randfels`, `moos_ufer_m2`, `insel_m2`, `farn`, `strauch`.
- Außerhalb der Talkaskade:

| Schlüssel | alt → neu |
|---|---|
| `kiesel_ufer_m2` | 0,3 → 2,0, nur in Fugen bzw. am Stein |
| `kiesbank` | 0,06 → 0,25 |
| `becken_minus` | 0,55 → 0,25 |
| Becken-Schlamm % | 80 → 30 |
| Abstand stein/stein | 0,85 → 0,5 |
| Abstand kiesel/kiesel | 0,8 → 0,5 |
| Abstand kiesel/stein | 0,85 → 0,4 |
| Abstand fels/fels | 0,75 → 0,4 (überlappend) |
| Abstand pflanze/stein | 0,9 → 0,1 |
| Abstand moos/stein | 0,7 → 0,2 |
| Graben min | 0,25 → 0,33 |
| `randfels_gross_anteil` | 0,75–0,9 → 0,4–0,6 |
| Glieder | 4–7 → 4–8 |
| `moos_ufer_m2` | 0 unter 1 m über dem Spiegel |
| `strauch_gruppe` | 0,06 → 0,12 |
| `zweig_gruppe` | 0,12 → 0,06 |
| Sichtweite kiesel | 6 000 → 8 000 |
| Sichtweite bachstein | 18 000 → 25 000 |
| Sichtweite geroell | 15 000 → 25 000 |

- **Neu:**
  - Klasse `felsstapel` mit 0,2 je m am Prallhang und 0,1 je m am Gleitufer, Werte wie Stapel;
  - je Klasse 2–5 Netze;
  - Reihenfolge: Steine vor Pflanzen.

**kantenufer_p2 (C.4):**
- Talkaskade aus; dort gilt `plan_p2_talkaskade.json`.
- Sonst:

| Schlüssel | alt → neu |
|---|---|
| `ueberhaengendes_gras.anteil` | 0,6–0,8 → 0,05–0,1, nur Gleitufer, Grasfuß ≥ 0,3 m |
| `moospolster.ab_h_m` | 0,25 → 1,0 |
| „gerade“ (Steine je 10 m) | 3–6 → 26–36 |
| Farne | Gleitufer 2–3 je 10 m, in Steinlücken |

- **Widerspruchsfrei:** Uferplan, 6e-Ausstattung und die 6f-Größenregel überschneiden sich nicht mehr.
  - Der Planer belegt die Bettplan-Blöcke (Lippen-, Eck-, Keystone- und Beckenblöcke) vorab als besetzt.
  - Die 6f-Größen gelten weiter für das Bett.
  - Das Ufer folgt den Klassen K1–K4 und Stapel.

## 4. Was gekauft oder geladen werden müsste (Ferat entscheidet)

- **Ergebnis:** Für §7 Punkte 1–5 ist **nichts zu kaufen**. Alle Kandidaten stehen schon in Ferats Fab-Bibliothek (13.10., 348 Einträge) und müssten nur importiert werden.
- **Was die Liste nicht enthält:** Anbieter, Preis, Größe und Lizenz. Diese Spalten sind deshalb offen und beim Import abzulesen. Ich erfinde keine Werte.
- **Der Plan braucht keinen dieser Titel.** Für jeden Punkt steht der Ersatz aus dem Bestand dabei.

| §7 | Titel in Ferats Bibliothek [Liste] | Anbieter | Preis | Größe / Lizenz | Reicht ein vorhandenes Netz mit MI-Override? |
|---|---|---|---|---|---|
| 1 Scree/Schutthaufen grau | „Slate stone pile“, „Dirty stones pile“, „Military Trenches Debris Patch Rock Corner“ | nicht in der Liste („Military Trenches“ vermutlich Megascans-Reihe, da „Military Trench Megascans Sample“ daneben steht [Ableitung]) | in der Bibliothek, 0 € zusätzlich | offen | **ja für den Plan:** Schuttband aus Einzelstücken (10–15 je m²). Desert_Western-Piles grau nur, wenn ein Haufen-Netz gewünscht ist |
| 2 Schieferstapel | „Slate stone pile“ | nicht in der Liste | 0 € zusätzlich | offen | **ja:** Stapel-Logik mit `texndcpda`, `pjcxN` und `flat_rock_02` (Planer). Ein Fertig-Stapel wäre nur für die Ferne günstiger |
| 3 kantiger Kleinschutt | „Rocks Pack“ und „rocks pack“ (zwei Einträge), „Military Trenches Ground Patch Rock S 03/S 04“ | nicht in der Liste | 0 € zusätzlich | offen | **ja:** `SM_namaqualand_rocks_01_a_NN` grau (kantiger Granit) |
| 4 Uferwand-Module | „Beach cliff rock face“, „Forest pine boulder“, „Rocky Stone Path Scan“ (Kantenplatten); „Project Titan“, „Electric Dreams Env“ (Epic-Beispiele [Ableitung]) | nicht in der Liste | 0 € zusätzlich | offen | **ja:** `SM_ForestRockSlab_01`, `SM_big_rock_wall_02/03`, `mountain_rock_big_02`; Coast-Escarpments grau mit Flechte nur für > 1,5 m hohe Wände |
| 5 Erle | „Megaplants: Black Alder“ | Megaplants-Reihe [Liste] | 0 € zusätzlich | offen | nein, kein Ersatz. Bis zum Import Birke (`Big_Tree_Birch_01`) |

## 5. Reihenfolge nach Wirkung (lokale Aufträge)

**Prüfkameras:** C2_t430_auge, C2_t500_auge, C2_t550_auge, C2_t500_schraeg, C2_tk_becken_auge.
**Zählung:** im Plan je 10 m und Seite (`kennzahlen_je_10m`) und im Prüfbild als Sichtschätzung je 10 m.
**Teilimport:** Die Dateien in `instanzen/<Feld>/plan.json` tragen `rolle` und `gruppe`; so lässt sich jeder Schritt einzeln setzen.

| # | Schritt | Prüfung Plan | Prüfung Bild |
|---|---|---|---|
| 1 | `p2_bettplan.py` neu laufen lassen (6e-Ufer und Randblöcke aus), Gelände mit `p2_bett_welt.py` | 645 Instanzen, 0 FEHLER | Kantengras, Moos und Farne aus 6e sind weg |
| 2 | **Steinsatz:** Rollen platte, stein, fussstein, block (Haufen, Saum, Fuß im Wasser) | K3 26–36, K4 3–5, Fuß 2–3, Kante ≥ 0,75, Uferband ≥ 0,65 | t430/t500: Steine 0,3–1 m sichtbar ≥ 20 je 10 m (heute 8–14), Fuß im Wasser ≥ 2, nackte Erde 0–3 m ≤ 10 % |
| 3 | **Komposition:** stapel, wand, fels | 1 bzw. 2 Stapel je 10 m; Felsdeckung ≥ 100 % | Zensus-Skript im Talkaskaden-Fenster: Felsdeckung ≥ 100 % (heute 1,2 %); t550 und t500_schraeg: ≥ 1 Stapel je 10 m am Prallhang lesbar. Frage an Ferat: „Kistenhaufen?“ (Antwort 21) |
| 4 | **Material:** `M_EL_Mountain_NL` mit `MI_EL_NL_*`, Fab-`MI_EL_*`, Namaqualand grau | alle `material_vorschlag` vorhanden | t430: dunkler Streifen 10–20 cm an ≥ 80 % der Steine im Wasser |
| 5 | **Schutt:** schutt, kies (Fugen, Begleiter, Schuttband) | K2 50–65 bzw. ≥ 2 × K3, K1 5–10 | Uferband 0–3 m: Anteil V < 0,18 ≥ 15 % (Ferats Pillow-Box) |
| 6 | **Bewuchs:** gras_ritze, gras_kante, farn_ritze, farn, moos_boden | Ritzen ≥ 0,8; 0 Gras im Wasser; Moos 0 unter 1 m | t500: Gras ≥ 1 m hinter der Steinkante außer in Graslücken; Farne 2–3 je 10 m am Gleitufer |
| 7 | **Rahmen:** busch, gehoelz | 1–2 Büsche je 10 m, 1 Gruppe je 50 m | tk_becken_auge: Bäume ≤ 20 m vom Ufer sichtbar |
| parallel | **Wasser:** Antwort 6h (EpicKlar/P2M, Near Normal 0, V20a nur bei Bedarf); Fälle mit `NS_Impact_Small` | – | wie 6h |

## 6. Wasserkante und Schaum an Steinen in der SWR

- **Vorgabe:** im Bach kein Schaum außer an Fällen; Nasslinie und Kragen sind etwas anderes als Schaum.
- **Kragen an der Anströmseite:**
  - kein weißer Kragen und kein `ELD_DF_Schaum` (ungetestet, nicht bauen).
  - Bei 2–4 m Bachbreite und dieser Wassermenge wäre er falsch; die Referenz ist ein 6–10 m breiter Fluss [Ableitung].
  - Stattdessen ein **dunkler Nass-Kragen im Steinmaterial**: `MF_EL_Nasslinie` mit `MF_EL_Spiegelhoehe` (16h N6 §4.2).
    - Talkaskade (Spritzzone): `Nass_Voll_cm` 12 / `Nass_Rand_cm` 30.
    - Sonst 8 / 20 (N6).
  - Das braucht die Nasslinie auch in `M_Master_material` (`M_EL_Mountain_NL`, 6d/6f). Darum ist das Material Schritt 4 in §5.
- **Schürze je Lippe:**
  - Nur an Fällen ≥ 1 m: `NS_Impact_Small` (Nature Water FX, gekauft), 24 Stellen; ab 1,8 m `NS_Waterfall_Small`, 3 Stellen (Bettplan `effekte_vorschlag`, 6e).
  - Nicht aus dem SimFoam-Kanal: `M_Eldarien_Wasser_Schaum8` hat weder FoamAtten noch Velocity-Scattering, und Schaum ist ausdrücklich nicht gewünscht.
- **Niagara je Hindernis:** nein. Das wären 264 Ufer- plus 5 Bett-Hindernisse und damit zu teuer, und es würde den Schaum wieder einführen.
- **Kräuselung 5–15 cm und Normalen nach Tempo:**
  - Reihenfolge wie Antwort 6h: erst EpicKlar/P2M, Near Normal 0 im MI, V20a (`ELD_Normal_Nah` 0,35) nur bei Bedarf.
  - Danach „Normalen nach Tempo“ (18 §3.1): die Normalstärke über `Sim Velocity` lerpen, nah flach, in Rinnen gerichtet.
  - Die Diagnose-Reihe D/W nicht weiterführen (siehe §7).

## 7. Offene Punkte – Entscheidungen

| Frage (Ferat §1–§5) | Entscheidung |
|---|---|
| Kleinschutt ≥ 2 Lagen? | **nein**, außer im Schuttband am Wandfuß (2 Lagen, 35 %). Sonst 1 Lage in den Fugen; Tiefe kommt aus Einbettung und 2. Steinlage |
| Farne an beiden Ufern, Schattenseite bevorzugt? | Gleitufer 2–3 je 10 m (Referenz). Nordufer (Schatten) zusätzlich 0–1; das Weltwerkzeug filtert die Südseite. Beide Ufer voll nur im Biom bergwald |
| Nachbarfelder 5 m ≥ Faktor 3? | **ja** für Heide-Inseln (≤ 30 % des Hangs, 2–5 m, Abstand 3–10 m). Am Ufer ersetzt der Haufen/Lücken-Rhythmus die Regel |
| Totholz-Werte aus der Witcher-Analyse? | **nein** für tundra (Referenz 0 Stämme); Bettplan-Totholz 5 bleibt. Wald-Biome 1–2 je 20 m [Ableitung] |
| Diagnose-Reihe D/W für Schlieren? | **nein**, nicht weiter. Antwort 6h hat die Ursache in den Zeichenweg gelegt; erst P2M |
| Grasfuß ≥ 0,3 m über dem Spiegel? | **ja** (im Prüfer) |
| Beckenabstand 3–12 m, jede 3. Stufe ohne Becken, Breite ± 30 %? | **nicht übernehmen**; der Bettplan 6c löst das mit Einheiten und Rinnen |
| Keine Landschaftstextur > 45°, Erdwände ≤ 45°? | > 45°: ≥ 90 % Fels bzw. Stein. Erdwände **≤ 38°** (strenger); darüber Wandmodule ab 1 m Höhe |
| ≥ 5 Begleitsteine im Umkreis 2 m? | **ja**, als 3–6 Steine im Umkreis 2 m plus 6–12 Schutt im Umkreis 1 m; vorhandene Nachbarn zählen |
| Prüfregeln Kamera (kein Gras < 0,5 m an der Kamera; Blickachse in ≥ 2 von 3 Prüfkameras) | erste Regel **ja**; Blickachse nur als Hinweis, nicht als FEHLER |
| Potenzgesetz ≥ 3× | **≥ 2×** je Klasse abwärts (K2 ≥ 2 × K3); K3 : K4 = 6–12 |
| Parameter-Vermutungen §5 | Werte in §3.2. Die Lagen Erde/Geröll/Kies kommen aus Antwort 21 bzw. 6f §3 (nicht hier) |

## Was fehlt bis Witcher 4 (Ufer Talkaskade, Stand 20)

Messlatte wie 6e: dichte, verzahnte Ufer bis an die Kante, Wind, weiches Licht, klare Wasserformen. Die Techdemo ist nur über Suchauszüge belegt.

Nach Wirkung:
1. **Steinsatz und Komposition bauen** (§5 Schritte 2–3). Heute 1,2 % Felsdeckung im Fenster, mit dem Plan 130–139 %.
   Das ist der größte Abstand zur Demo und zur Referenz.
2. **Wasser im Bett und klar:** feinere SWR (6g) und der EpicKlar-Befund (6h). Ohne das liegt ein Film über den neuen Kantensteinen.
3. **Nasslinie in allen Steinmaterialien** (`M_EL_Mountain_NL`, Fab-MIs). Erst damit lesen sich Fuß-Steine und Kante nass.
4. **Moos und Flechte als Material-Auflage** (`MI_EL_Auf_*_tundra`), Höhenregel 0 % unter 1 m. Der Plan setzt nur Bodenpolster.
5. **Bewuchs mit Wind und Alt-Halmen** (trockene MI-Kopien), Farne und Erle (Import).
6. **Fall-Effekte** (`NS_Impact_Small`) und Licht im Einschnitt.
7. **Durchbruch und Bergrinne** mit demselben Planer, sobald der Bettplan dort rechnet.

## Rückfragen

1. **Platten:** `yaw_rel` ±90° und `kipp` = Neigung (kipp > 0 heißt Nase nach unten) legt die Netz-X-Achse zum Wasser.
   Stimmt das bei euch für `SM_ForestRockSlab_01` und die Rocky-Ground-Netze? Sonst drehe ich um 180°.
2. **Budget:** Soll K2 im Plan auf 40 je 10 m sinken?
   - Das sind ≈ −10 % Instanzen, liegt aber unter der Referenzzahl.
   - Oder gilt die volle Dichte nur für die Talkaskade, wie in §2.3 vorgeschlagen?
3. **MI-Namen:** `material_vorschlag` nutzt `MI_EL_NL_<Paket-MI>` (Mountain), wie in 6f, und `MI_EL_<id>` (Fab). Gibt es die Mountain-Kinder schon unter diesen Namen?
4. **Teilimport:** Soll ich je Schritt in §5 einen eigenen Unterordner schreiben (`detailgrad/<Schritt>/`) statt alles in einen?
