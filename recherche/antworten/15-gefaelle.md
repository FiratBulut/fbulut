# Antwort zu Auftrag 15 – Steile Fluss- und Bachstrecken natürlich machen (Felsstufen, Klippen, Wasserfälle)

Stand 11.10.2026. Zusammenführung von Regelwerk und Planer. Das Regelwerk mit Belegen steht in
[`15-gefaelle-regelwerk.md`](15-gefaelle-regelwerk.md), die Zahlen in
[`skripte/gefaelle/gefaelle_regeln.json`](skripte/gefaelle/gefaelle_regeln.json). Skripte und Formatbeschreibung:
[`skripte/gefaelle/README.md`](skripte/gefaelle/README.md). Die Prioritätenliste liegt in
[`gefaelle/prioritaet.json`](gefaelle/prioritaet.json), die Testbilder in `gefaelle/test_<strecke>.png`.

## Kurzfazit

- **Es gibt keine Schräge mehr.** Jede der 161 steilen Strecken wird zu ruhigen Becken (≤ 2 % Spiegel) und Stufen.
  Die Stufenarten sind Schnelle, Blockstufe 0,8–2 m, Kaskade aus Teilstufen ≤ 1,5 m und Fall (nur an Fels, bis 25 m).
  Lippen sitzen auf dem alten Spiegel, deshalb liegt der neue Spiegel nie über dem alten, und die Summe der Stufen
  ergibt genau den Fall.
- **Wasser nach 14b Variante A.** Oberhalb und unterhalb jeder Stufenstrecke bleibt ein Epic-River, dazwischen liegt
  ein statisches Kaskadennetz (SLW). Die beiden überlappen genau 0,5 m. Es gibt keine Flussstücke mit Lücken und
  keine Schaumscheiben. Niagara-Effekte sitzen an Stufen ≥ 1 m, ein Vorhang-Netz nur an Stufen ≥ 3 m.
- **Testlauf 2 m, Prüfer 0 FEHLER:**
  - **20 Pilot-Strecken** (19 Läufe, C2 auf Rang 1): 346 Stufen.
  - **Alle 161 Strecken:** 1089 Stufen in 98 Läufen, 128 Kaskadennetze, 16 angepasste Zuflüsse.
  - Zwei Läufe ergeben byteidentische Ausgaben.
- **Die weicheren festen Zonen** (Zuflüsse werden mit umgebaut, an Wegen nur noch eine Furt) senken `kaum_planbar` von
  **76 auf 36**. 30 dieser 36 Strecken sind kürzer als 40 m.
- **Nächster Schritt lokal (1 m):** zuerst C2 bauen und mit den Kameras `_vorher`/`_nachher` vergleichen, dann die
  übrigen Piloten. Die Anleitung steht in Abschnitt 5.

## 1. Regelwerk (Zusammenfassung, Details und Quellen im Regelwerk)

Die Regeln und ihre Belege stehen in [`15-gefaelle-regelwerk.md`](15-gefaelle-regelwerk.md), Kurzfazit und
Abschnitt 2. Der Planer liest **alle** Zahlen aus `gefaelle_regeln.json` (v2). Kurz:

- **Klassen nach Gefälle:** ruhig bis 3 %, step-pool 3–6,5 %, Kaskade 6,5–30 %, Fallkette 30–60 %, Fall/Klamm
  über 60 %.
- **Stufenabstand:** L = B · clamp(0,4 · S^−0,7; 0,8; 4). Bei Flüssen gilt eine eigene Regel ohne Blockstufen über die
  volle Breite.
- **Einzelfall statt Kette:** ab S_lok ≥ 0,6 und D ≥ 4 m, an Fels schon ab 2 m.
- **Wände:** Fälle bekommen Wände, unterhalb großer Fälle eine Schlucht. Klamm ab 30 % mit Fall.
- **Gestein und Netze** je Biom am Stufenort.
- **Effekte:** ≤ 3 je Stufe.

## 2. Prioritätenliste und Top 20

Die Bewertung lautet Score = 100 · (0,40 · Sicht + 0,30 · Sehens + 0,30 · Physik):

- **Sicht:** Wegpunkte mit Sichtlinie, nächster Wegpunkt, Anteil der Strecke, der sichtbar ist.
- **Sehens:** Kameras der 120 Sehenswürdigkeiten, deren Bild die Strecke zeigt, und Abstand zum Ortsrand.
- **Physik:** Fall, Gefälle, Länge.

C2 ist auf Vorgabe des Koordinators Rang 1. Strecken, die ein Sehens-Planer umbaut, sind markiert
(`umgebaut_von_sehens` bzw. `teilweise_sehens`).

**Status der 161 Strecken:**

| Status | Anzahl |
|---|---|
| offen | 117 |
| teilweise_sehens | 2 |
| umgebaut_von_sehens | 6 |
| kaum_planbar (< 15 m oder < 30 % frei) | 36 (vorher 76) |

**Pilot = die 20 besten planbaren Strecken.** Ränge, die in der Tabelle fehlen (4, 7, 8, 20), sind umgebaut oder
kaum planbar.

| Rang | Strecke | Biom | Länge m | Fall m | Score | Begründung |
|---|---|---|---|---|---|---|
| 1 | F_ERLENBACH_1V_C2_s1 | tundra | 181 | 57,0 | 50,1 | Vorgabe Koordinator (Ferat schaut dorthin); 14b zurückgestellt, A15 ersetzt A14; 90 % vom Weg sichtbar; Mittel 31 %, max 102 % |
| 2 | B_R_P0_M2_03_s1 | tundra | 395 | 72,3 | 92,4 | 98 % vom Weg sichtbar (20 m); 2 Kameras von tundra_08_das_wabenmoor, grenzt an den Ort |
| 3 | B_R_P0_M2_02_s1 | tundra | 240 | 49,8 | 88,8 | 57 Wegpunkte, 11 m; 3 Kameras (gletscher_02, tundra_02, tundra_03) |
| 5 | F_ERLENBACH_2V_D3_s1 | tundra | 156 | 22,1 | 76,3 | 53 Wegpunkte; Kamera tundra_01_der_pingo, 11 m vom Ort |
| 6 | B_R_P1_M2_01_s1 | tundra | 332 | 41,3 | 76,0 | 88 Wegpunkte; Kamera tundra_03_die_eiswand |
| 9 | B_R_P0_M2_02_s2 | tundra | 57 | 7,6 | 71,9 | 38 Wegpunkte; 2 Kameras tundra_03_die_eiswand |
| 10 | B_R_P0_M2_04_s1 | tundra | 126 | 17,8 | 68,8 | 31 Wegpunkte (15 m); Kamera wueste_01_yardang_flotte |
| 11 | B_R_M3_P1_01_s1 | aue | 230 | 39,9 | 67,0 | 25 Wegpunkte; 60 m von kueste_05; max 37 % |
| 12 | B_R_P0_M2_01_s1 | tundra | 135 | 16,6 | 66,6 | 41 Wegpunkte; Kamera tundra_02_der_wanderer |
| 13 | B_R_M2_P1_02_s1 | bergwald | 192 | 42,7 | 65,6 | 24 Wegpunkte; Mittel 22 %, max 65 % |
| 14 | B_R_P4_M2_04_s1 | elfenwald | 573 | 133,5 | 65,6 | an elfenwald_04_elfentreppe (dort ausgespart); größter Fall der Liste |
| 15 | B_R_P1_M2_03_s1 | tundra | 72 | 8,6 | 63,7 | 68 Wegpunkte; Kamera tundra_03_die_eiswand |
| 16 | B_K8_ELFENFALL_01_s1 | elfenwald | 448 | 114,9 | 62,9 | Kamera elfenwald_03_rotlaubhain, 7 m vom Ort; 115 m Fall |
| 17 | B_R_P5_P1_05_s2 | dschungel | 182 | 37,3 | 61,5 | 24 Wegpunkte; Mittel 21 % |
| 18 | F_ELFENFLUSS_3_H4_s1 | elfenwald | 418 | 45,0 | 61,3 | Fluss, 19 Wegpunkte, 100 % sichtbar |
| 19 | B_R_P4_M1_03_s1 | elfenwald | 251 | 39,5 | 60,8 | Weg 11 m |
| 21 | B_R2_R_P0_M2_01_s1 | tundra | 47 | 7,2 | 60,7 | 48 Wegpunkte; Kamera tundra_02_der_wanderer |
| 22 | B_R_P3_M2_01_s1 | elfenwald | 386 | 46,9 | 60,3 | Weg 16 m, 52 % sichtbar |
| 23 | B_R_P5_P1_03_s1 | dschungel | 156 | 25,3 | 60,2 | Weg 12 m, 100 % sichtbar |
| 24 | B_R2_R_M1_M1_02_s2 | aue | 134 | 19,1 | 60,1 | Weg 10 m, 100 % sichtbar |

## 3. Pilot-Ergebnis (2-m-Test)

In der Spalte „gestuft“ steht der Fall auf Stufen neben dem Gesamtfall. Den Rest überbrücken feste Zonen und
Becken. FX = Niagara-Systeme + Zusatz-Aufprall mit Cull 20 m. KN = Kaskadennetz.

| Rang | Strecke | Stufen | Arten | gestuft / ges. m | größte m | Vorhang | Holz | FX | Wasser | Kameras | feste Zonen |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | F_ERLENBACH_1V_C2_s1 | 19 | 5 Fall, 14 Kaskade | 52,1 / 57,0 | 4,7 | 2 | 0 | 12 + 6 | 1 KN, 2 River | 4 | – |
| 2 | B_R_P0_M2_03_s1 | 29 | 1 Fall, 15 Kaskade, 13 Stufe | 54,7 / 72,3 | 8,1 | 1 | 0 | 18 + 7 | 2 KN, 3 River | 2 | Sehens, Furt |
| 3 | B_R_P0_M2_02_s1 | 21 | 2 Fall, 13 Kaskade, 6 Stufe | 38,0 / 49,8 | 5,2 | 2 | 0 | 12 + 5 | 2 KN, 3 River | 4 | Furt |
| 5 | F_ERLENBACH_2V_D3_s1 | 7 | 6 Kaskade, 1 Stufe | 13,5 / 22,1 | 2,3 | 0 | 0 | 6 + 3 | 1 KN, 2 River | 4 | Sehens, Furt |
| 6 | B_R_P1_M2_01_s1 | 31 | 20 Kaskade, 11 Stufe | 35,2 / 41,3 | 2,5 | 0 | 0 | 21 + 3 | 1 KN, 2 River | 4 | – |
| 9 | B_R_P0_M2_02_s2 | 4 | 2 Kaskade, 2 Stufe | 5,2 / 7,6 | 2,1 | 0 | 0 | 6 | 2 KN, 3 River | 4 | – |
| 10 | B_R_P0_M2_04_s1 | 12 | 5 Kaskade, 7 Stufe | 11,7 / 17,8 | 1,9 | 0 | 0 | 8 | 2 KN, 3 River | 4 | Furt |
| 11 | B_R_M3_P1_01_s1 | 22 | 16 Kaskade, 6 Stufe | 34,6 / 39,9 | 4,9 | 0 | 22 | 14 + 5 | 1 KN, 2 River | 4 | – |
| 12 | B_R_P0_M2_01_s1 | 8 | 6 Kaskade, 2 Stufe | 12,4 / 16,6 | 2,4 | 0 | 0 | 10 + 1 | 1 KN, 2 River | 4 | – |
| 13 | B_R_M2_P1_02_s1 | 18 | 4 Fall, 10 Kaskade, 4 Stufe | 35,8 / 42,7 | 8,4 | 3 | 1 | 10 + 2 | 2 KN, 3 River | 4 | Furt |
| 14 | B_R_P4_M2_04_s1 | 45 | 7 Fall, 21 Kaskade, 17 Stufe | 112,3 / 133,5 | 15,4 | 7 | 5 | 22 + 9 | 3 KN, 4 River | 2 | Sehens, Furt, Abschnitt |
| 15 | B_R_P1_M2_03_s1 | 4 | 2 Kaskade, 2 Stufe | 6,3 / 8,6 | 1,9 | 0 | 0 | 6 + 1 | 1 KN, 2 River | 4 | – |
| 16 | B_K8_ELFENFALL_01_s1 | 18 | 4 Fall, 13 Kaskade, 1 Stufe | 79,5 / 114,9 | 18,5 | 4 | 0 | 18 + 5 | 2 KN, 3 River | 2 | Ort, Stadt, Sehens |
| 17 | B_R_P5_P1_05_s2 | 17 | 11 Kaskade, 6 Stufe | 25,3 / 37,3 | 3,6 | 0 | 0 | 15 + 6 | 3 KN, 4 River | 4 | Furt |
| 18 | F_ELFENFLUSS_3_H4_s1 | 3 | 2 Kaskade, 1 Stufe | 7,5 / 45,0 | 3,2 | 0 | 0 | 6 | 1 KN, 2 River | 4 | Ort, Stadt, Furt |
| 19 | B_R_P4_M1_03_s1 | 19 | 13 Kaskade, 6 Stufe | 18,5 / 39,5 | 1,9 | 0 | 3 | 9 + 1 | 1 KN, 2 River | 2 | Ort, Furt |
| 21 | B_R2_R_P0_M2_01_s1 | 3 | 1 Kaskade, 2 Stufe | 4,2 / 7,2 | 2,0 | 0 | 0 | 4 | 1 KN, 2 River | 4 | See |
| 22 | B_R_P3_M2_01_s1 | 40 | 27 Kaskade, 13 Stufe | 35,8 / 46,9 | 2,3 | 0 | 6 | 20 + 1 | 2 KN, 3 River | 2 | Furt |
| 23 | B_R_P5_P1_03_s1 | 14 | 10 Kaskade, 4 Stufe | 18,6 / 25,3 | 2,8 | 0 | 0 | 12 + 2 | 1 KN, 2 River | 4 | Furt |
| 24 | B_R2_R_M1_M1_02_s2 | 12 | 10 Kaskade, 2 Stufe | 12,0 / 19,1 | 2,4 | 0 | 12 | 8 | 1 KN, 2 River | 2 | Furt |

Zu den Spalten:

- **Stufe** heißt Blockstufe 0,8–2 m, im `plan.json` steht sie als `art: kaskade` mit `art_regel: stufe`.
- **Holz:** In der Aue sind Wurzelstufen und Holz-Verklausungen die Stufen.
- **Fremdes Wasser** (meist nur wenige Meter am Laufende) fehlt in der Spalte „feste Zonen“.

**Prüfer Piloten:** 0 FEHLER, 13 WARNUNG. Davon betreffen 6 Stufen ≥ 1 m ohne Niagara wegen der Grenze für
gleichzeitige Systeme, 3 Bett oder Ufer an einzelnen Punkten im 2-m-Raster und 2 je ein Becken mit 2–3 %.

**C2 im Einzelnen:**

- 19 Stufen. 11 davon übernehmen die Lagen S01–S11 aus `stufen.json` (Feld `vorgabe_stufen_json`).
- Vorhang an den 2 Fällen ≥ 3 m (S05, S06). Kaskaden fallen in Teilstufen ≤ 1,5 m und bekommen Niagara.
- `plan.json` → `a14.ersetzt_a14 = true` mit den ersetzten Gruppen C2_A–C2_E.
- S00 aus `stufen.json` (3,3 m) geht in der Kaskade S01 (4,7 m, Lippe 9 m weiter oben) auf. Die ersten 10 m des Laufs
  bleiben als Anschluss im oberen River (1,6 m Fall).

## 4. Wasser nach 14b Variante A

Verbindlich nach [`14b-befund-geteilte-baeche.md`](14b-befund-geteilte-baeche.md), Abschnitte 3 und 4.
`plan.json` → `wasser_koerper` enthält zwei Typen:

- **`river`**: ober- und unterhalb, Punkte [x, y, z, breite, tiefe, velocity] und `punkt_typen`,
  `anschluss_oben`/`anschluss_unten` mit `ueberlapp_m` 0,5.
- **`kaskadennetz`**: von 0,5 m vor der ersten Lippe bis hinter den Fuß der letzten Stufe.
  - Felder: `s_m`, `mittellinie` [x, y, z, breite, tempo, fallanteil, schaum, abstand_bett], `knick` je Punkt (becken,
    lippe, bogen, wand, fuss, rampe; Überfallbogen v = 2,4 m/s), `rand_ueberstand_m` 0,4, `material`
    `MI_EL_Kaskade_SLW` (nach 14b neu anzulegen), `vorhang_an_stufen` (einzelner Absturz ≥ 3 m), `muendungen_s_m`, `pruefung`.
  - Prüfungen: Bett ≥ 0,2 m unter dem Spiegel, Ufer am Netzrand über dem Spiegel.
- **Effekte:**
  - Stufen < 1 m bekommen kein Niagara.
  - 1–3 m und Kaskaden (Teilstufen ≤ 1,5 m): `NS_Waterfall_Small` + `NS_Impact_Small`. Ab 3 m Absturz kommt der Vorhang dazu, große Fälle bekommen das
    Medium- oder Large-Trio.
  - Höchstens 6 Systeme gleichzeitig mit Cull ≥ 30 m. Dazu je Stufe ≥ 1 m ohne Aufprall ein `NS_Impact_Small` mit
    Cull 20 m. Hart gelten höchstens 8 gleichzeitig.
- **Variante C** (gestufter Einzelspline + eigene Bach-Zone) gibt es nur mit `--variante C`.

## 5. Aufruf lokal auf 1 m, Schritt für Schritt (für Claude lokal)

```
python -I recherche/antworten/skripte/gefaelle/gefaelle_prioritaet.py --daten1m export/unreal/welt
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis .            # 20 Piloten
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis . --laeufe F_ERLENBACH_1V_C2   # nur C2
python -I recherche/antworten/skripte/gefaelle/gefaelle_pruefen.py export/unreal/welt/gefaelle --daten1m export/unreal/welt
```

Ausgabe nach `export/unreal/welt/gefaelle/<lauf>/`. Auf 1 m gelten Bett- und Uferabweichungen als FEHLER. Zuerst C2,
dann die anderen Piloten in Rangfolge. Je Lauf:

1. **Kameras „vorher“ setzen.** Aus `plan.json` → `kameras` die Einträge `<strecke>_vorher` und `_weg_vorher`
   anlegen (Hoch = −170) und Bilder machen, **bevor** etwas geändert wird.
2. **Gelände-Delta:**
   - `abschnitte[].gelaende.datei` (f32, Meter, Fenster `fenster_ij` im 1-m-Raster) auf die Landschaft addieren.
     Der Rand ist 0.
   - Danach die Lagen `lagen/<abschnitt>_<Lage>.r8` in die Gewichtsebenen schreiben.
   - Wege, Orte und Sehenswürdigkeiten bleiben unverändert, das prüft der Prüfer.
3. **Kaskadennetz bauen.** Je `wasser_koerper` mit `typ: kaskadennetz` ein Static Mesh `SM_KN_<lauf>_<nr>` nach 14b
   Abschnitt 3 A, Schritt 2:
   - Becken als Streifen mit 0,5-m-Zellen, Breite + 2 × 0,4 m.
   - Zunge auf dem Überfallbogen.
   - Vertexfarbe R = Tempo/300, G = Fallanteil, B = Schaum.
   - Material `MI_EL_Kaskade_SLW`. Wenn es fehlt, zuerst nach 14b Schritt 1 anlegen.
   - Keine Kollision.
4. **River kürzen bzw. teilen.** Den bisherigen `WaterBodyRiver` des Laufs durch die `river`-Einträge ersetzen (Punkte,
   Breite, Tiefe, Velocity, `zone`). Die Überlappung mit dem Netz beträgt genau 0,5 m, das Netz liegt dort 2 cm
   unter dem River-Spiegel.
   - **Zuflüsse:** Bei Einträgen in `zufluesse` die Endpunkte des Zufluss-Splines auf `punkte_neu_cm` setzen.
   - **C2:** Die A14-Gruppen C2_A–C2_E aus `wasser_fx/plan.json` und die Teilung aus `stufen_fluss_teile.json` nicht
     bauen bzw. wieder entfernen, A15 ersetzt sie (`plan.json` → `a14`).
5. **Netze und Akteure.** Die Ebene `gefaelle` aus `instanzen/<Feld>/plan.json` + `<Netz>.f32` wie bei den
   Sehens-Ebenen laden (FORMAT.md §3, Präfix `FT_EL_GEF_`). Dazu gehören Fallwände, Riegel/Lippen,
   Holz-Verklausungen, Wände, Blöcke, Kies und Moos. Die Akteure stehen in `plan["akteure"]`.
6. **Vorhang und Effekte.**
   - Vorhang-Netze nur an `vorhang_an_stufen` (einzelner Absturz ≥ 3 m, Stufenfeld `vorhang`).
   - Niagara-Systeme aus `effekte`: Pfad `asset`, `pos_cm`, `rot_q`, `skala`, `cull_m`, Cast Shadow aus, Sort 2.
   - Keine Schaumscheiben.
7. **Kameras „nachher“.** Dieselben Kameras als `_nachher` bzw. `_weg_nachher` setzen und die Bilder neben die
   Vorher-Bilder legen.
8. **Prüfen.** `gefaelle_pruefen.py` auf 1 m ausführen, dazu 14b Prüfschritte A 1–5: Becken von Ufer zu Ufer nass,
   keine weißen Rechtecke, Schaumbänder aus 60–100 m, `stat Niagara` und `profilegpu` ≤ 0,5 ms, Übergänge ohne Spalt.

## 6. Prüfer

`gefaelle_pruefen.py` läuft auch eingebaut im Planer. Er prüft:

- **Spiegel:** monoton, Anfang und Ende auf alter Höhe, nie über dem alten, Becken ≤ 3 % (FEHLER) bzw. ≤ 2 %
  (WARNUNG), Rampen.
- **Stufen** gegen die Arten.
- **Wasser:** Mittellinie monoton, Überlappung genau 0,5 m und sonst keine, jede Stufe im Netz, Bett ≥ 0,2 m, Ufer
  über dem Spiegel, Niagara oder Vorhang an Stufen ≥ 1 m.
- **Effekte:** Inventar, ≤ 3 je Stufe, ≤ 6 gleichzeitig mit Cull ≥ 30 m, ≤ 8 gesamt.
- **Kameras.**
- **Gelände:** Rand 0, Abstand zu Weg 2 m und Ort 5 m, nicht in Sehenswürdigkeiten, Anheben > 1 m.
- **Lagen.**
- **Instanzen:** über `sehens_lib.sehens_pruefen` (Format, Inventar, Budget, Schweben, Weg).

**Ergebnis 2 m:**

| Lauf | FEHLER | WARNUNG | Anmerkung |
|---|---|---|---|
| Piloten | 0 | 13 | zweiter Lauf byteidentisch |
| alle 161 | 0 | 32 | |

`sehens_lib/selbsttest.py` und der Bergwald-Planer: 0 FEHLER.

## 7. Grenzen

- **2-m-Daten:** Ein 4-m-Bach ist dort nur 2 Zellen breit. Bett und Ufer verschmieren, deshalb gilt auf 2 m ein
  Rasterzuschlag (WARNUNG statt FEHLER). Lokal auf 1 m wird streng geprüft.
- **Gestufter Anteil:** Er liegt bei 50–95 % des Gesamtfalls. Der Rest liegt in Furten, Sehens- und Ortszonen und am
  Laufende, dort bleibt der alte Spiegel.
- **Niagara-Grenze:** An dichten Kaskaden bleiben einzelne Stufen ≥ 1 m ohne Systeme. Dort trägt nur der Schaum im Netz.
- **Pivot und Schauseite** der Wand- und Riegelnetze sind angenommen. Das ist vor dem Serienbau an C2 im Bild zu prüfen.
- **Uferwulst:** Wo das alte Ufer kaum über dem Wasser liegt, wird es bis 1 m angehoben.
- **H4:** Die A14-Schnellen liegen auf `F_ELFENFLUSS_2_H4`. Diese Strecke ist kaum planbar (Ort/Stadt) und bleibt Fluss
  mit `NS_Stream` aus A14. `F_ELFENFLUSS_3_H4` ist ein anderer Lauf. Dort verlangt das Regelwerk Stufen (45 m auf
  418 m), also gibt es ein Kaskadennetz.

## 8. Getroffene Entscheidungen (Koordinator, von Ferat übertragen, 11.10.)

1. **Niagara:**
   - ≤ 6 gleichzeitig mit Cull ≥ 30 m, dazu je Stufe ≥ 1 m ein `NS_Impact_Small` mit Cull 20 m, hart ≤ 8.
   - Stufen < 1 m bekommen kein Niagara.
   - WARNUNG nur bei Stufen ≥ 1 m.
2. **Feste Zonen weicher:**
   - Zuflüsse werden mit umgebaut (Mündung ins Becken, Endstück angepasst).
   - Stufen bis 6 m an Wege heran, an der Querung eine Furt ≥ 4 m (umgesetzt mit ≥ 12 m ruhigem Wasser).
   - Orte und Sehenswürdigkeiten bleiben fest.
3. **Netze:**
   - `uk5ebcp` wird übersprungen.
   - Elfenwald: gestapelte `SM_HugeMossyForestCliff_01` / `SM_ForestRockShelf_*`.
   - Aue: keine Felswände, sondern Erdanrisse, Wurzelstufen und Holz-Verklausungen.
4. **C2** wird vollständig mit Kaskadennetz geplant, Pilot Rang 1, Vorgabe `stufen.json`. A15 ersetzt A14.
   **H4** bleibt Fluss mit A14.
5. **Wasser:** 14b Variante A ist Standard. Kein `custom` als Standard, Variante C nur auf Abruf. Keine Schaumscheiben.

## 9. Rückfragen

1. **Material:** `MI_EL_Kaskade_SLW` gibt es noch nicht. Sollen Absorption und Scattering aus
   `MI_Eldarien_Wasser_Fluss` übernommen werden (14b Rückfrage)?
2. **Niagara:** Bei dichten Kaskaden (z. B. C2 S03/S04/S07/S08/S12/S16) bleiben Stufen ≥ 1 m ohne Systeme.
   Reicht der Netzschaum, oder soll die harte Grenze dort auf 10 steigen?
3. **Kaum planbare Strecken:** 30 der 36 `kaum_planbar`-Strecken sind < 40 m lang. Bleiben sie so, oder sollen sie
   von Hand mit einer Einzelstufe gebaut werden?
4. **Uferwulst:** Ist das Anheben des Ufers um bis zu 1 m für die Prüfung „Ufer über dem Spiegel“ in Ordnung, oder
   soll stattdessen das Bett tiefer gelegt werden?
5. **Reihenfolge lokal:** zuerst C2 allein bauen und abnehmen lassen, danach die anderen 19 Piloten, dann alle?
