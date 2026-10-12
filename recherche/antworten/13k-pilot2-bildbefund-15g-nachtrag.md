# Antwort zu Auftrag 13k – Pilot 2 (Säulenhain, Karsee): Bildbefund und Nachtrag 15g

Stand 12.10.2026. Code-Stand: Commit **`97e82a3`** (Zwischenstände `526ed55`, `3e00e36`). Diese Antwort steht im Commit danach.
Die Nachträge 11:45 (Seefarbe Variante C, Antworten auf die 15g-Rückfragen) und 12:35 (SLW-Einheit je cm bestätigt)
sind eingearbeitet.

## Kurzfazit

- **Sägeschnitt verboten (alle 15 Biome):**
  - Neue Bibliotheksregel: gesägte Stammstücke sind in der Wildnis FEHLER, im Planer (Palette) und im Prüfer
    (`inventar.saegeschnitt`).
  - Erkannt werden das Schnittflächen-Material `MI_Pine_lods_ends`, alle `*_log` aus
    `Mountain_Environment_Set/Details` und Holzlager-Netze. Im Inventar sind das 10 Netze.
  - Vorher lagen **1 606 gesägte Stücke** in 7 Orten von 3 Biomen (bergwald, gletscher, tundra), jetzt **0**.
- **Säulenhain:** Das Holzlager ist weg (954 gesägte Stücke → 0).
  - Totholz: 3 abgestorbene Riesentannen, darunter Gruppen großer liegender Stämme, hangparallel.
  - Kleinholz: Äste in Nestern, Zapfen nur am Rand, Rinde als Decal.
  - Dichte im Hallenkern (≈ 2 780 m²): **1,3 liegende Stämme und 8,9 Äste je 100 m²**. Ferats Richtwert ist 1–3 bzw. 5–15.
  - Waldboden in 6 Schichten: Moospolster, Farngruppen zu 3–7, Heidelbeer-Inseln, bemooste Steine, Wurzeln und
    Nadelstreu. Die Nadelstreu deckt mit 255, damit wächst unter dem Hain kein Landschaftsgras.
- **Fern-Kameras:** Die Sichtprüfung prüft jetzt Gelände **und** Baumkronen.
  - Grundlage für die Kronen sind das 4-m-Baumraster (Höhe → Kronenradius) und die eigenen Netze.
  - Vorher waren **24 von 52** `_fern`-Kameras verdeckt, darunter der Säulenhain.
  - Alle 24 sind neu gesetzt: 21 auf dem Weg, 1 auf einer Lichtung (29 m neben dem Weg), 1 am Gegenhang (137 m),
    2 an Aussichtspunkten ohne Weg (457 m, 699 m; Rückfrage 3).
  - Danach ist keine `_fern`-Kamera mehr verdeckt.
- **Karsee-Rückwand:** Neue Regel in `steilwand.py`: Flächen > 60° werden bis zur Oberkante verkleidet, am Fuß liegt
  ein Schuttkegel.
  - Am Karsee aktiv: **2 155 von 2 163 m²** > 60° sind jetzt mit Fels bedeckt (vorher 395 von 3 244 m² im Fenster).
    Dafür stehen 116 Wandnetze als Instanzen mit Kollision.
  - Nicht für alle Orte eingeschaltet: Es geht um 71 000 m² in 36 Orten, und dort steht meist schon Bestandsfels, den
    wir nicht kennen (Rückfrage 4).
- **Seefarbe:**
  - `bergsee` = Ferats Variante C (Absorption 8/45/40/8, Scattering 0,06/0,22/0,14/0,08, Albedo 0,35,
    Rauheit 0,015). Gilt für den Karsee. Die anderen Seen sind geprüft und bleiben (Tabelle in Abschnitt 5).
  - Warum der Test 8/40/160 kaum wirkte: Das sind **Absorptionslängen in cm**. Blau kam dabei am weitesten
    (160 cm), Rot war nach 8 cm weg. Die flachen Ränder blieben deshalb cyan.
- **Schaum Treppenbäche** (15g-Logik wiederverwendet):
  - Anteil der `quer`-Einträge mit Schaum > 0,5: **61 % → 20 %** (Median der 40 Bäche), gesamt 61 % → 16 %.
    Zum Vergleich C2: 12 %.
  - Karsee: 70–74 % → 19–22 %.
  - Becken und Gumpen ≤ 0,2 (Prüfer: FEHLER, wenn nicht). Am Fallfuß klingt der Schaum über 2–4 m ab.
    Fallflächen ≤ 0,45, nicht mehr 1,0.
  - Die Deckung läuft zum Ufer weich aus wie in 15g.
- **Vorhänge:** Die Aufprall-Effekte an Stufen ≥ 3 m haben jetzt `cull_m` 60–80 m (33 Effekte). Jede Stufe hat
  `strahl_breite_m`, hergeleitet aus Abfluss und kritischer Tiefe im 13f-Querprofil (Median 32 % der Lippenbreite).
- **Treppen unverändert:** Stufenvergleich gegen die Basis: **gleich 42 von 42 Bächen**. Unverändert sind auch:
  - die Wasserfläche (Lippe, Fuß, Becken, Querprofil),
  - alle 75 Effekte nach Asset, Stufe und Position,
  - alle Vorhang-Stufen.
- **Nachtrag 15g:** Die C2-Bilder liefen noch mit dem alten Plan und dem alten Material. Ferats Erklärung
  1/Absorption passt zur UE-Einheit (Abschnitt 8). An C2/`0e00d17` ist kein Fehler zu beheben.
- **SLW-Einheit bestätigt** (Ferat-Test 12:35): UE 5.8 rechnet je cm.
  - Unsere Werte bleiben je m. In jedem Sehens-Kaskadennetz steht jetzt `material_parameter.einheit: "je_m"` mit
    `skalierung_ue: 0.01`, dazu die je-cm-Werte (`SLW_*_pro_cm`).
  - `bergsee` ist eine andere Konvention: `wasserfarben.json` nennt Absorptionslängen in cm. Beides ist getrennt
    dokumentiert.
- **Akteure:** Ferats Grenze von 50 je Ort ist jetzt ein Prüfer-FEHLER. Betroffen waren 5 Orte (bis 77). Der Planer
  bündelt weitere Wiederholungsnetze, jetzt höchstens 50 (gletscher_05).
- **Prüfung:** 2 m alle 15 Biome **0 FEHLER**, zwei Läufe byteidentisch (alle 15), synthetisch 1 m 0 FEHLER, Selbsttest grün (85 Prüfungen, 0 FEHLER).

## 1. Sägeschnitt-Netze

**Regel** (`sehens_lib/inventar.py`):
- `saegeschnitt(netz)` liefert einen Grund, wenn eine dieser Bedingungen zutrifft:
  - Ein Materialslot heißt `*ends*` (laut `netze_masse.json`, `mats`).
  - Das Netz ist ein `*_log` unter `Mountain_Environment_Set/Details/Meshes`.
  - Der Name ist ein Holzlager oder Brennholz.
- `netz_pruefen(…, wildnis=True)` meldet dann FEHLER. Der Grund nennt Ferats Regel: nur an Lagern, Holzfällerplätzen
  und Wegen. In Sehens-Orten (nur Landschaft) gibt es keine Ausnahme.
- Wildnis-Prüfung im Planer (`rezept.palette`) und im Prüfer (Ebene: Instanzen und Akteure). Das A15-Werkzeug ruft
  ohne `wildnis` auf und ist unverändert.

**Inventar (10 Netze erkannt):**
- Mountain-Details: `SM_Forest_pine_04_log`, `_04_01/02/03_log`, `SM_Forest_pine_08_log`, `SM_Forest_Pine_09_log`.
  Alle tragen `MI_Pine_lods_ends`.
- Holzlager: `SM_Pile_WoodLog_02a` (Village), `SM_FireplaceLogs` (Niagara-Demo), `SM_half_log` (Zaunbausatz),
  `SM_firewoodSetA_a1`.
- Nicht erfasst und nach Pfad und Material unauffällig sind `SM_dead_log_01–05` (Forest Set, `MI_logs_01`) und
  `SM_pine_stump_*`. Ob ihre Enden gesägt aussehen, zeigt nur das Bild (Rückfrage 1).

**Alle 15 Biome geprüft** (Stücke im 2-m-Lauf vor 13k):

| Ort | gesägte Stücke vorher | Gruppe → jetzt |
|---|---|---|
| bergwald_03 Säulenhain | 954 (`_04_01/02_log` 920, `_08_log` 34) | `kleinholz`/`moderholz` → Totholz/Äste (unten) |
| bergwald_07 Windwurf | 400 | `bruchstuecke` (Palette `stammstuecke`) → Äste, Kronenteile, wenige `SM_OldFallenTree_02`; 220 statt 400 |
| bergwald_08 Wurzelstein | 126 | `nadeln_zweige`: `_04_01_log` → `SM_Pine_broken_branch_04` |
| bergwald_02 Brandkiefer | 97 | `stammstuecke` (geklumpt) und `brandholz`; `MI_EL_SW_Verkohlt.fuer` ohne `*_log` |
| gletscher_02 Lawinenkegel | 18 | `astbruch`: → `SM_OldTreeBranch_06` |
| tundra_05 Trunkener Grund | 8 | `treibholz`/`totholz`: → `SM_OldFallenTree_02` |
| bergwald_05 Klamm | 3 | `treibholz`: → `SM_OldFallenTree_02` |
| **Summe** | **1 606** | **0** (Prüfer: 0 FEHLER) |

Die übrigen 8 Biome hatten keine gesägten Stücke.

- **Außerhalb von Sehens gefunden, nicht geändert:** `gefaelle_regeln.json` → `biome.bergwald.netze.holz` enthält
  `SM_Forest_pine_04_01/02/03_log`. Das A15-Werkzeug setzt damit Holzstufen und Totholz-Querlagen.
- Ich habe das nicht angefasst, weil es C2 und alle A15-Läufe ändern würde (Rückfrage 2).

**Netze nachgeschlagen** (`netze.csv`, `netze_masse.json`):

| Netz | Maße (m) | Bemerkung |
|---|---|---|
| `SM_detail_branches_01/02/03` | 1,8 × 1,3 × 0,1 / 1,7 × 1,4 × 0,3 / 2,9 × 3,6 × 0,3 | Forest Set, `MI_Details` – Äste ✓ |
| `SM_OldTreeBranch_01…06` | 1,0–6,9 m lang | Megascans – `_01/_04` Äste, `_02/_03/_06` dicke Äste/Stammteile ✓ |
| `SM_OldFallenTree_01/02` | 2,3 × 0,7 × 0,4 / 3,6 × 0,3 × 0,2 | Megascans – **klein**: allein keine „großen“ Stämme, darum ×1,3–1,8 und ergänzt |
| `SM_LargeFallenTree_01/02` | 3,6 × 0,7 / 5,1 × 2,3 | große liegende Stämme ✓ |
| `SM_FallenSpruceTree_01` | 7,3 × 1,9 | gestürzte Fichte ✓ |
| `SM_MossyTree_01` | 7,8 × 2,3 | bemooster liegender Stamm (Ammen-/Altholz) ✓ |
| `Fir_08_Dead_Forest` | 7 × 9 × 17,7 | abgestorbene Tanne (Environment Set) ✓ – die Totbäume |

**Fehlt:**
- Ein eigenes Rinden-Netz in Waldgröße. Es gibt nur `S_Pine_Bark_Piece_*` (12 cm, Niagara-Demo) und
  `SM_bark_debris_*_NN` (Köcherbaum, Namaqualand).
- Rinde liegt deshalb als Decal `MI_ScatteredTreeBark_01` (schon im Plan).

## 2. Säulenhain (bergwald_03): Totholz und Waldboden

**Totholz und Kleinholz:**
- **`totbaeume`:** 3 × `Fir_08_Dead_Forest` ×2,0–2,4 (35–42 m), im Ring 10–28 m um die Halle. Zusammen mit den
  Riesen sind das 29 Akteure (Grenze 50).
- **`totholz`:** Je Totbaum 3–4 große Stämme im Umkreis von 2,5–11 m:
  - Netze: `SM_LargeFallenTree_01/02`, `SM_FallenSpruceTree_01`, `SM_OldFallenTree_01/02` ×1,3–1,8.
  - `yaw` = hangab + 90° ± 20°, also **hangparallel**.
  - Instanzen mit Kollision.
- **`stammstuecke`:** Mittleres Totholz in 7–9 Nestern zu 2–4 Stück (`SM_OldFallenTree_*`, `SM_OldTreeBranch_02/03/06`),
  ebenfalls hangparallel.
- Die vorhandenen liegenden Riesen (`riese_liegend`, `altholz`, Ammenstamm) bleiben.
- **`aeste`:** 26–30 Nester zu 6–11 Ästen, dazu 8–12 Äste um jeden Totbaum (`aeste_totbaum`).
  - Netze: `SM_detail_branches_*`, `SM_OldTreeBranch_01/04`, `SM_Pine_broken_branch_*`, `SM_BrokenTreeBranch_01`.
- **Zapfen:** nur in Nestern am Hainrand unter den Kiefern (Ring 26–42 m). Tannenzapfen zerfallen am Baum, unter den
  Riesen lägen keine ganzen Zapfen.
- **Pilze:** jetzt am liegenden Totholz.

**Waldboden** (Schichten, alle `cluster`, nicht gleichmäßig):

| Schicht | Gruppe | vorher | nachher |
|---|---|---|---|
| 1 Moospolster | `moospolster` (14–18 Flecken × 8–14) + `moos_am_holz` | 95 (nur Stammfuß) | 347 |
| 2 Farngruppen 3–7 | `farnhorste` (14–18 Gruppen × 3–7) | 31 | 42 |
| 3 Heidelbeer-Inseln | `heidelbeer_inseln` (7–9 × 6–12) + Saum | 202 (nur Ring) | 195 (Inseln im Kern + Saum) |
| 4 bemooste Steine | `bemooste_steine` (5–7 × 2–4, halb eingesunken) | 0 | 14 |
| 5 Wurzeln | `brettwurzeln` + `wurzeln` (`SM_MossyForestRoots_01/02`, `SM_ForestRoots_01/02`) | 19 | 43 |
| 6 Nadelstreu | Lage `Nadeln` 255 ohne Flecken, Rand 6 m | 235, Flecken 0,2 | 255 deckend |

**Bilanz im Kern** (Ellipse 34 × 26 m ≈ 2 780 m²):

| | vorher | nachher | Richtwert Ferat |
|---|---|---|---|
| gesägte Stücke | 954 | **0** | 0 |
| liegende Stämme (inkl. 5 Akteure) | 32 | 35 → **1,3 je 100 m²** | 1–3 |
| Äste | 909 (gleichmäßig) | 246 → **8,9 je 100 m²**, in Nestern | 5–15 |
| Zapfen | 400 | 82 (Rand) | – |
| Instanzen im Ort | 3 352 | 1 600 | – |

**Landschaftsgras (geht das im Planformat?):** Ja, über die Lage.
- SEHENS_FORMAT §3: „neu = max(alt, Ziel), die übrigen Lagen werden skaliert, damit die Summe 255 bleibt“. Das GPU-Gras
  wächst aus Wiese/Gras/Trockengras/Kraut/Heide/Moos.
- Die Nadelstreu mit 255 setzt im Kern alle übrigen Lagen auf 0, Gras wächst dort nicht mehr. Vorher war es 235 mit
  Flecken, an den Fleckstellen blieben bis zu 20 % Restlage.
- Die Moos-Lage um die Stammfüße ist auf 120 gesenkt. Ob Moos ein GT trägt, weiß ich nicht (Rückfrage 5).
- Ein eigenes Feld „Gras aus“ braucht es nicht.
- Die helle Pflanze im Bild `_nah` ist kein Netz aus unserem Plan (vorher und nachher gleich). Sie kommt sehr
  wahrscheinlich aus dem Landschaftsgras.

## 3. `_fern`-Kameras: freie Sichtachse (Gelände UND Baumkronen)

**Neue Prüfung `kamera_frei.pruefe_fern_achse`** (Planer und Prüfer FEHLER):
- **Strahlen:** von `_fern` auf die oberen 30 % der bis zu 6 höchsten Held-Netze (3 Höhen je Netz). Ohne Held-Netz
  geht der Strahl auf die Ort-Silhouette am Kameraziel.
- **Je Strahl geprüft:**
  - Gelände nach dem Stempel, mit 0,3 m Rand.
  - **Bestandskronen:** jede belegte Zelle des 4-m-Baumrasters (`baeume_4m`/`baumhoehe_4m`) als Kronenzylinder um
    die Zellmitte. Radius 0,15 h (1,2–4 m), in den obersten 15 % halb. Krone von 0,35 h bis h, Freiräume ausgenommen.
    1 m Strahl in Kronen sperrt.
  - Eigene Netze (Bäume als Krone + Stamm).
- **Bedingungen:** ≥ 50 % der Strahlen frei. Dazu muss der Vordergrund frei sein: ein Korridor ± 2 m um den
  Hauptstrahl auf den ersten 60 m.
- „Biomdichte“ steckt im Baumraster (Anzahl und Höhe je 4-m-Zelle, aus den Instanzen gerechnet).
- **Suche in vier Durchgängen**, jeweils mit Leuchtfeuer-Silhouette und Achse:
  1. Weg-/Pfadpunkte 300–800 m.
  2. Lichtung bis 40 m daneben (Hang ≤ 30°, keine Krone in 6 m).
  3. Gegenhang bis 150 m daneben.
  4. Aussichtspunkt im ganzen Ring.
- Wertung: vor dem Himmel > sichtbarer Anteil > Achsenanteil > nah am Weg.

**Ergebnis (2 m):**
- Mit der neuen Prüfung waren **24 von 52** `_fern`-Kameras verdeckt. 22 hatten verdeckte Silhouettenstrahlen, 2 nur
  einen verdeckten Vordergrund.
- Alle 24 sind versetzt. Jetzt ist keine mehr verdeckt (Prüfer, `fernpruef`: 0 von 52).
- Die alten Regeln (Leuchtfeuer-Silhouette, Kamera im Netz) melden weiter 0 FEHLER.

| Kamera | Abstand zum Ort | neben Weg/Pfad | Feld |
|---|---|---|---|
| `aue_02_die_alte_fern` | 631 m | 0 m | C4 |
| `aue_04_treibholzwerder_fern` | 703 m | 3 m | D5 |
| **`bergwald_03_saeulenhain_fern`** | **693 m** | **3 m** | **C4** (−2166 / −246 m, NO des Hains) |
| `dschungel_01_mondtor_fern` | 784 m | 0 m | G5 |
| `dschungel_02_turmquelle_fern` | 748 m | 3 m | G5 |
| `dschungel_03_steinwald_fern` | 612 m | 2 m | H6 |
| `elfenwald_01_mutterbaum_fern` | 669 m | 2 m | G3 |
| `elfenwald_02_nebelhain_fern` | 560 m | 2 m | I4 |
| `fjord_01_die_kanzel_fern` | 410 m | **137 m** (Gegenhang) | C2 |
| `frost_02_frostsee_fern` | 737 m | 0 m | E2 |
| `frost_04_raureifhain_fern` | 559 m | 0 m | E2 |
| `frost_06_eiskueste_fern` | 604 m | **699 m** (Aussichtspunkt) | F2 |
| `gletscher_01_gletschertor_fern` | 760 m | 2 m | D2 |
| `gletscher_02_lawinenkegel_fern` | 761 m | 3 m | E3 |
| `heide_03_die_wacholderprozession_fern` | 345 m | 0 m | G5 |
| `kueste_01_die_alten_fern` | 322 m | 3 m | B5 |
| `kueste_02_die_vogelinsel_fern` | 377 m | 2 m | A5 |
| `kueste_03_das_nadeltor_fern` | 323 m | **457 m** (Aussichtspunkt) | A4 |
| `kueste_06_die_kreidewand_fern` | 595 m | 0 m | H3 |
| `lava_02_schwefelgrund_fern` | 497 m | 3 m | C6 |
| `oedland_03_hoellentor_fern` | 420 m | 2 m | E6 |
| `sumpf_02_der_weidendom_fern` | 314 m | **29 m** (Lichtung) | I5 |
| `sumpf_03_der_reiherhorst_fern` | 385 m | 2 m | G5 |
| `tundra_03_die_eiswand_fern` | 699 m | 2 m | E3 |

**Säulenhain:**
- Die alte `_fern` stand 520 m südlich (−2674 / 616). Dort lag der Strahl nach ~200 m in Bestandskronen (4 von 18
  Strahlen frei).
- Die neue Kamera steht 693 m nordöstlich auf dem Weg. Alle 18 Silhouettenstrahlen sind frei, der Vordergrund ist frei.
  Sichtbar sind 96 % der Silhouette (57 m), allerdings vor Gelände und nicht vor dem Himmel. Auf dem Weg hat keine
  Position den Himmel dahinter und eine freie Achse.
- Ferats Frage `Fir_07` auf 570 m lässt sich damit auf ~690 m prüfen.

## 4. Karsee-Rückwand: Flächen > 60° bis zur Oberkante

**Werkzeug** (`steilwand.verkleiden_60`, Regel `gelaende.verkleiden_60`):
- **Bereich:** alle Gebiete > 60° (≥ 10 m², 1-m-Raster nach dem Stempel), natürliche und neue, die im Umkreis `r_m`
  liegen (Standard Radius + 25 m) und zum Ort schauen (≥ 30 % der Zellen mit Hangab-Richtung ± 75° zur Ortsmitte).
  Verkleidet wird jeweils das **ganze** Gebiet bis zur Oberkante.
- **Verkleidung:** wie 13h – gierig von unten nach oben, Front talwärts, gestapelt. Die Netze sind Instanzen mit
  Kollision, belasten also das Akteur-Budget nicht. Für die Steilflächen-Prüfung zählen sie als Fels.
- **Schuttkegel am Fuß:** Zellen bis 7 m unterhalb des unteren Wanddrittels, flacher als 40°. Dort liegen Blöcke
  (`kegelschutt`, 0,12 je m², 0,5–1,6 m) und die Lage Geröll 205.
- **Prüfer** (`pruefe_ort_steil60`):
  - Mit Regel: offene Gebiete > 20 m² = FEHLER.
  - Ohne Regel: HINWEIS mit der offenen Fläche als Liste. In `orte.json` steht dann `gelaende.steil60`.

**Karsee** (`r_m` 75 um die Seemitte; Palette `rcygn_tier_0`, `SM_HugeNordicCoastalCliff_01/02`,
`SM_big_rock_wall_01` mit 7–12 m Höhe):

| | vorher | nachher |
|---|---|---|
| Fläche > 60° im Kar (zum See gewandt) | 2 163 m², davon 395 m² mit Fels (Fenster gesamt 3 244 m²) | 2 163 m², davon **2 155 m²** mit Fels |
| offen in Gebieten > 20 m² | 2 648 m² (27 Gebiete im Fenster) | **0** |
| Wandnetze 60° | – | 116 (Instanzen mit Kollision) + Schuttkegel |
| Akteure Karsee | 44 | 44 |

**Warum nicht für alle Orte an:**
- In den Ortsfenstern der übrigen Orte liegen auf 2 m **82 800 m²** > 60° (zum Ort gewandt). Davon sind 10 700 m² mit
  unserem Fels bedeckt, 70 900 m² sind offen in 36 Orten.
- Größte Posten: fjord_02 Schleierwand 27 400 m², fjord_06 9 300 m², dschungel_05 5 000 m², gletscher_03 3 900 m²,
  wueste_02 3 700 m².
- Das wären 1 500–2 000 weitere Wandnetze. Die meisten dieser Wände tragen vermutlich Bestandsfels (Houdini, Fab),
  den die Daten nicht kennen.
- Die Liste steht als HINWEIS im Prüfer. Ein Eintrag `verkleiden_60` im Rezept schaltet die Regel je Ort ein
  (Rückfrage 4).

## 5. Seefarbe `bergsee`

**Werte:** Ferats Variante C, im Format von `wasserfarben.json`, Master `M_Eldarien_Wasser_Schaum8`:
- Absorption **8 / 45 / 40 / 8**
- Scattering **0,06 / 0,22 / 0,14 / 0,08**
- Albedo **0,35**
- Rauheit **0,015**

**Umsetzung:**
- In `FARBEN` des Prüfers und in `format.WASSER_FARBEN`.
- In `orte.json` oben als Block `wasser_farben`, nur wenn ein See die Farbe nutzt.
- Am Karsee gesetzt, mit neuer `farbe_begruendung`. Kurzbeschreibung „Dunkel blaugrüner Karsee“.

**Was die Werte bedeuten:**
- Die Absorption ist eine **Absorptionslänge in cm** (Konvention `wasserfarben.json`: das Material gibt 1/Wert als
  SLW-Koeffizient je cm aus). Sie ist kein Koeffizient und bekommt **keine** Skalierung 0,01.
- 8/45/40 cm entspricht 0,125/0,022/0,025 je cm = 12,5/2,2/2,5 je m. Im Block `wasser_farben` stehen beide Angaben
  (`einheit_absorption`, `entspricht_koeffizient`).
- Zum Vergleich die Kaskadennetze: `material_parameter.SLW_Absorption_pro_m` sind Koeffizienten je m, Skalierung
  0,01 (Abschnitt 8).
- Rot ist nach wenigen Zentimetern weg, Grün kommt am weitesten, Blau knapp dahinter: dunkles Blaugrün.
- Die Streuung hat keinen Blau-Überhang mehr.

**See-Zuordnung in allen Biomen geprüft:**

| See | Farbe | Entscheidung |
|---|---|---|
| bergwald_06 `karsee` (Kar, 3,5 m) | tiefblau → **bergsee** | Kar-/Bergsee |
| aue_07 `topf` (Blautopf, 9 m) | tiefblau | bleibt – Quelltopf |
| gletscher_03 `moraenensee` | gletschermilch | bleibt (Gletschertrübe) |
| gletscher_04 `kesselsee` (Toteisloch im Heidehang) | schwarz_spiegel | bleibt (Moorauge) |
| gletscher_06 Töpfe, lava_05 Spalte, wueste_04, dschungel_02, elfenwald_04 | tuerkis | bleiben (Gletschertöpfe, Grundwasserspalte, Quelltopf, Kalktuff) |
| tundra_01 `kratersee` (Pingo, 2 m) | smaragd | bleibt (flacher Tundrasee) |
| übrige (Moor, Sumpf, Gumpen, Thermal, Salz) | moorbraun / schwarz_spiegel / klar / thermal / salzweiss | unverändert |

- Weitere Kar- oder Bergseen gibt es in den 120 Orten nicht.
- Neue Prüferregel: `tiefblau` an einem See, der kein Quelltopf ist (Name ohne quell/topf/cenote), ergibt eine WARNUNG.
  Aktuell sind es 0.

**Warum der lokale Test (8/40/160, Streuung 0,06/0,20/0,45) kaum wirkte:**
1. **Richtung, nicht Skala:**
   - Die Zahlen sind Absorptionslängen, keine Koeffizienten. Eine große Zahl bedeutet wenig Absorption.
   - 8/40/160 cm schluckt Rot sehr schnell und Blau am wenigsten (160 cm).
   - Am 10–30 cm tiefen Rand bleiben danach Grün (e^−0,25…−0,75 = 78–47 %) und Blau (94–83 %) übrig, Rot ist fast
     null. Das ist **Cyan**.
   - In der Tiefe wird es dunkler, weil auch Grün verschwindet. Genau so beschreibt Ferat das Bild.
2. **Streuung:** 0,20/0,45 in Grün/Blau macht das Wasser eher heller blau-cyan als vorher.
3. **Wie Variante C es löst:** Blau und Grün bekommen ähnliche, kurze Längen (40/45 cm), die Blaustreuung sinkt
   (0,14). Das ist dunkles Blaugrün.
4. **Physikalischer Rand:** Wo das Wasser nur wenige Zentimeter tief ist, wirkt keine Absorption (Beer-Lambert). Den
   Rand dämpfen nur ein dunklerer Grund (`Color Scale Behind Water` bzw. Albedo, nasser Kies) und weniger Streuung.

## 6. Schaummenge der Treppenbäche

**Ursache:**
- Die Sehens-Stufen hatten eine „Kerbe“ über die ganze Lippenbreite (gerade Lippen, 13j). Damit bekamen Saum, Zunge
  und Aufprall über die ganze Breite Schaum 1.
- Die Becken der Sehens-Treppen sind nur 3–4 m lang, die Schaumzonen überlappten.

**Änderung** (`sehens_lib/bach.py`, 15g-Logik wiederverwendet):
1. **`quer_ergaenzen` aus `gefaelle_plan.py`** (15g) läuft unverändert, mit einer Kopie des Regelwerks mit
   Sehens-Werten:
   - Saum 0,3 m, Seitenschaum 0,05/0,08, Aufprall ≤ 15 % des Beckens, Abklingen 2–4 m.
   - Deckung zum Ufer weich ab 80 % der Rezepttiefe.
   - A15/C2 rechnet weiter mit dem Original.
2. **Kerbe = Strahlbreite** (Abschnitt 7) statt ganzer Lippe. Die Krone bleibt gerade (Kerbentiefe 0), `dz_cm` und
   Querprofil sind wie 13f. Neben dem Strahl ist auf der Zunge die Deckung 0,3.
3. **Längshülle** `schaum_huelle`, danach die 15g-Lipschitz-Hülle `schaum_weich`:
   - Becken/Gumpe ≤ **0,2**.
   - Lippensaum ≤ 0,5.
   - Fallfläche ≤ **0,45** – die Fall-Optik macht das Material.
   - Fallfuß: Spitze 0,65–0,85 für 0,2 m, dann **Abklingen über 2–4 m** (1 + 0,5 · Fallhöhe, höchstens 70 % des
     Beckens).
   - Schnellen ≤ 0,45.
4. **Prüfer** (`pruefe_schaum_sehens`, dazu die 15g-Regeln übernommen):
   - FEHLER: Becken (hinter Fuß + Abklingen, > 0,8 m vor der nächsten Lippe) Schaum > 0,2.
   - FEHLER: Fallflächen pauschal ≥ 0,95.
   - FEHLER (aus 15g): harte Kanten, grobes Raster, Beckenmitte, `tiefe_cm` < 0.
   - WARNUNG: Anteil > 0,5 über 35 %.

**Zahlen je Bach** (2 m; Anteil der `quer`-Einträge mit Schaum > 0,5 und mit Deckung = 1):

| Bach | Schaum > 0,5 vorher | nachher | Deckung = 1 vorher | nachher |
|---|---|---|---|---|
| `aue_01_biberstau ueberlauf` | 59 % | 26 % | 54 % | 54 % |
| `aue_07_blautopf quellbach` | 58 % | 28 % | 39 % | 45 % |
| `bergwald_05_klemmblock_klamm klammbach` | 62 % | 20 % | 50 % | 39 % |
| `bergwald_06_karsee abfluss` | 70 % | 22 % | 51 % | 48 % |
| `bergwald_06_karsee zulauf_sued` | 74 % | 19 % | 60 % | 32 % |
| `bergwald_06_karsee zulauf_west` | 74 % | 22 % | 54 % | 29 % |
| `canyon_04_fluesterschlucht spaltbach` | 39 % | 0 % | 0 % | 23 % |
| `dschungel_02_turmquelle quellbach` | 37 % | 2 % | 7 % | 26 % |
| `dschungel_06_schluckhoehle schwinde` | 33 % | 0 % | 2 % | 21 % |
| `elfenwald_04_elfentreppe abfluss` | 56 % | 23 % | 51 % | 53 % |
| `elfenwald_04_elfentreppe stufe_1` | 52 % | 30 % | 29 % | 37 % |
| `elfenwald_04_elfentreppe stufe_2` | 48 % | 29 % | 32 % | 49 % |
| `elfenwald_04_elfentreppe stufe_3` | 45 % | 12 % | 48 % | 44 % |
| `elfenwald_04_elfentreppe stufe_4` | 48 % | 20 % | 38 % | 47 % |
| `elfenwald_04_elfentreppe zulauf` | 76 % | 23 % | 40 % | 23 % |
| `elfenwald_05_farnschlucht tobelbach` | 69 % | 21 % | 45 % | 35 % |
| `fjord_02_schleierwand abfluss1` | 69 % | 23 % | 50 % | 32 % |
| `fjord_02_schleierwand abfluss3` | 68 % | 26 % | 48 % | 34 % |
| `fjord_02_schleierwand abfluss4` | 70 % | 21 % | 50 % | 31 % |
| `fjord_04_haengetal hochtalbach` | 72 % | 22 % | 48 % | 32 % |
| `frost_03_eisvorhang sickerlinie` | 53 % | 13 % | 21 % | 10 % |
| `gletscher_01_gletschertor gletscherbach` | 63 % | 12 % | 33 % | 39 % |
| `gletscher_02_lawinenkegel schmelz_mitte` | 70 % | 20 % | 35 % | 18 % |
| `gletscher_02_lawinenkegel schmelz_ost` | 69 % | 22 % | 42 % | 21 % |
| `gletscher_02_lawinenkegel schmelz_west` | 60 % | 17 % | 31 % | 17 % |
| `gletscher_03_moraenensee firnrinnsal` | 64 % | 20 % | 48 % | 19 % |
| `gletscher_03_moraenensee seeabfluss` | 72 % | 24 % | 48 % | 23 % |
| `gletscher_05_die_waechte muehlenbach` | 52 % | 10 % | 18 % | 25 % |
| `gletscher_06_gletschertoepfe klammbach_1` | 39 % | 12 % | 22 % | 33 % |
| `gletscher_06_gletschertoepfe klammbach_2` | 69 % | 13 % | 55 % | 37 % |
| `gletscher_06_gletschertoepfe klammbach_oben` | 54 % | 16 % | 35 % | 30 % |
| `gletscher_06_gletschertoepfe klammbach_unten` | 66 % | 20 % | 47 % | 34 % |
| `heide_06_der_wollsackfall klammbach` | 63 % | 22 % | 23 % | 24 % |
| `lava_03_kraterkinder rinnsal` | 45 % | 7 % | 13 % | 22 % |
| `tundra_03_die_eiswand rinnsal` | 61 % | 15 % | 20 % | 29 % |
| `tundra_04_die_fliesstreppe schmelzfaden` | 61 % | 13 % | 25 % | 15 % |
| `tundra_05_der_trunkene_grund abfluss` | 51 % | 15 % | 27 % | 21 % |
| `tundra_06_das_schneetaelchen schmelzwasser` | 32 % | 0 % | 0 % | 17 % |
| `wueste_04_quelloase rinnsal` | 38 % | 8 % | 13 % | 29 % |

- **Gesamt:** Schaum > 0,5 sinkt von 61 % auf **16 %**, im Median der Bäche von 61 % auf **20 %**. Zum Vergleich
  C2 (`0e00d17`, 2 m): 12 %.
- **Becken mit Schaum > 0,2:** 0 (Prüfer).
- **Bäche über 35 %** (WARNUNG):
  - fjord_04 `hochtalbach` KN0 (41 %, 13 Netzpunkte, eine Lippe)
  - heide_06 `klammbach` KN1 (41 %, 13 Punkte)
  - Beides sind kurze Netze, die fast nur aus einer Stufe bestehen.
- **Deckung:** Sie läuft jetzt in allen Netzen zum Ufer auf 0 aus. Ferat sah auf dem 13j-Stand „überall 1,0“. Den
  Wert 1 haben nur noch die Wasserflächen in der Mitte.

## 7. Vorhänge: `cull_m` und `strahl_breite_m`

**`cull_m`:**
- Aufprall-Effekte (`NS_Impact_Small`) an Stufen ≥ 3 m: **60 m bei 3 m Fall, linear bis 80 m ab 10 m Fall**, mit
  `cull_grund`. Das betrifft 33 Effekte. Alle anderen behalten 20 m.
- Die Grenze von 8 Niagara je Ort bleibt (Höchstwert jetzt 8: bergwald_06, elfenwald_04/05, fjord_02/04). Die Orte
  liegen ≥ 350 m auseinander, 80 m Cull überlappen also nicht.

**`strahl_breite_m`** (`bach.lippen_strahl`):
1. **Querschnitt** 0,3 m oberhalb der Lippe. Auf 1 m kommt er aus dem gestempelten Gelände. Auf 2 m ist die Fallkante
   verschmiert; dann gilt das 13f-Querprofil selbst: Bett = Spiegel − Tiefe zwischen den Wasserkanten der
   Rezeptbreite, 35°-Böschung.
2. **Abfluss:** Q = A(Becken) × v. v ist das Beckentempo des A15-Werkzeugs (0,8 m/s, `KN.tempo.becken`).
3. **Strahl:** An der Lippe stellt sich die kritische Tiefe ein (Q² T / (g A³) = 1). Der Strahl ist die
   Wasserspiegelbreite T_c bei kritischer Tiefe, Mitte am tiefsten Punkt.

Die Werte stehen:
- je Stufe in `stufen_strahl` (`strahl_breite_m`, `u_mitte_m`, `abfluss_m3_s`, `krit_tiefe_m`, `wasserbreite_m`,
  `lippe_breite_m`, `querschnitt`),
- je Vorhang in `vorhang`,
- je Effekt in `strahl_breite_m`.

Der Strahl nutzt im Median **32 %** der Lippenbreite (Netz + Rand, 2 m: 3,6 m), Spanne 10–86 %.

| Vorhang-Stufe (Karsee/Klamm, 2 m) | Fall | Strahl | Wasser | Lippe | Q | Cull |
|---|---|---|---|---|---|---|
| bergwald_06 `abfluss` S00 | 12,0 m | 2,25 m | 2,45 m | 3,6 m | 0,50 m³/s | 80 m |
| bergwald_06 `zulauf_sued` S01–S05 | 3,1–12,3 m | 1,15 m | 1,15 m | 3,6 m | 0,12 m³/s | – (Niagara-Grenze) |
| bergwald_06 `zulauf_west` S05 | 10,1 m | 1,15 m | 1,15 m | 3,6 m | 0,12 m³/s | – |
| bergwald_05 `klammbach` S00 / S01 | 8,9 / 3,2 m | 1,65 m | 1,95 m | 3,6 m | 0,42 m³/s | 77 / 61 m |

Auf 1 m ist die Lippe schmaler (Netzbreite folgt der Wasserkante). Die Strahlbreite bleibt dort ähnlich, weil sie aus
Rezeptbreite und Tiefe kommt.

## 8. Nachtrag 15g (C2)

**Welcher Stand lief?**
- Die neuen C2-Bilder (`c2_v2_schaum035.jpg`) liefen noch auf dem **alten Plan** (Version 2, `ae09234`/`2378e0d`) und
  mit dem alten Material `MI_EL_Kaskade_SLW`.
- Das zeigt das Bild: gerade Beckenränder ohne Eckblöcke an den Lippenenden. `0e00d17` setzt 72 Eckblöcke und
  22 Randblöcke sowie Buchten bis 1,2 m.
- Ferat bestätigt es im Nachtrag 11:45. Version 3 wird gerade mit `0e00d17` gebaut.
- Das „deckende Grün“ kommt aus dem alten Material (1/Absorption der Fluss-Instanz), nicht aus dem Plan.

**Einheit (Ferats Erklärung gegen die UE-Doku geprüft, mit dem Test 12:35 bestätigt):**
- Die Epic-Doku zum Single Layer Water nennt für Absorptions- und Streukoeffizienten **keine Einheit** („Range 0 bis
  unendlich“).
- UE rechnet in Zentimetern. Das Forumsbeispiel „clear water“ trägt die Meterwerte des reinen Wassers
  (0,35/0,07/0,03) ausdrücklich **× 0,01** ein. Die Koeffizienten wirken also **je cm**.
- Damit stimmt Ferats Rechnung: 24/48/40 cm → 1/x = 0,042/0,021/0,025 je cm = 4,2/2,1/2,5 je m. Das ist 10- bis
  50-mal mehr als unsere 0,40/0,07/0,05 je m. Bei 1,5 m Tiefe bleiben in Rot e^−6,3 ≈ 0,2 % – deckend grün.
- **Korrektur zu 15g:** Der Satz „In UE 5 liegen die Koeffizienten je Meter“ war falsch. Richtig ist: Der Knoten
  rechnet je cm, unsere Werte sind je m.
- **Bestätigt (Nachtrag 12:35, `pilot2_slw2_einheit.jpg`):**
  - Mit × 1,0 leuchtet schon 20–30 cm tiefes Wasser türkis, mit × 0,01 bleibt es klar. Die Skalierung 0,01 ist
    richtig und bleibt der Wert.
  - Im Bild (Spalte „SLW2 0,01“) sind die Gumpen am Karsee klar mit sichtbarem Grund.
  - Kontrolle mit tiefen Gumpen (C2 Version 3): Bei 1,5 m Tiefe muss Rot auf ~55 % fallen (e^−0,40·1,5).
- **Eindeutig im Plan:** Jedes Sehens-Kaskadennetz trägt in `material_parameter` unverändert `SLW_Absorption_pro_m`
  und `SLW_Streuung_pro_m`. Dazu kommen:
  - `einheit: "je_m"`, `skalierung_ue: 0.01`
  - die umgerechneten Werte `SLW_Absorption_pro_cm` (0,004/0,0007/0,0005) und `SLW_Streuung_pro_cm`
    (0,0002/0,0003/0,0004)
  - `einheit_hinweis` mit der Abgrenzung zu `wasserfarben.json`
  - Keine Zahl ist still geändert.
- Die A15-Netze (C2) tragen diese Felder noch nicht. Ich habe `skripte/gefaelle/` nicht angefasst; die Werte gelten
  dort genauso (Rückfrage 6).
- Für Seen im `wasserfarben.json`-Format (Absorptionslängen in cm) braucht es keine Skalierung, das Material nimmt
  1/Wert je cm.

**Ist in `0e00d17` noch etwas zu tun?**
- Ich habe C2 mit dem unveränderten Werkzeug neu geplant (2 m mit 1-m-Fenster) und geprüft:
  - Planer 0 FEHLER.
  - `gefaelle_pruefen` 0 FEHLER, 2 WARNUNG wie in 15g (1 Beckenabschnitt > 2 %, 6 Stufen ohne Niagara).
  - Schaum > 0,5 auf 12 % der `quer`-Einträge.
- Kein echter Fehler, **C2 ist nicht geändert**. `skripte/gefaelle/` ist unverändert, der Gefälle-Prüfer bleibt
  bei 0 FEHLER.
- Zwei Beobachtungen ohne Änderung:
  - C2 hat 62 Akteure (HINWEIS im A15-Prüfer). Ferats Grenze von 50 gilt in Sehens jetzt als FEHLER (Rückfrage 6).
  - Die `material_parameter` im Netz nennen weiter Schaum_Menge 0,15 und Zungen_Schaum 0,25. Lokal gelten 0,35 und
    0,35. Die MI ist für alle Netze dieselbe, die Abstimmungsdatei gilt.

## 9. Akteure je Ort (Ferat: höchstens 50)

- Der Prüfer meldet > 50 Akteure je Ort jetzt als **FEHLER** (vorher HINWEIS „Richtwert“).
- **Planer** (`rezept._akteure_buendeln`): Nach der 13j-Bündelung (≥ 12 gleiche Netze) werden weitere
  Wiederholungsnetze zu Instanzen mit Kollision. Reihenfolge: zuerst die häufigsten, dann die kleinsten. Nie
  `akteur_fest` und nie die Held-Ebene.
- **Vorher > 50:** gletscher_05 (77), canyon_03 (68), canyon_07 (65), fjord_08 (56), tundra_03 (56).
- **Jetzt:** höchstens 50 (gletscher_05), dann lava_05 mit 49.
- Lage, Größe und Drehung bleiben, nur die Ausgabeform ändert sich.

## Prüfergebnis

| Lauf | Ergebnis |
|---|---|
| 2 m, alle 15 Planer | Planer 0 FEHLER, Prüfer **0 FEHLER** |
| Determinismus 2 m | alle 15 je zweimal nacheinander: byteidentisch (`diff -r`), Eingaben-Prüfsumme vor/zwischen/nach gleich |
| synthetisch 1 m, alle 15 | Planer 0 FEHLER, Prüfer **0 FEHLER**; Schaum > 0,5 im Mittel 22 % (Karsee 20–34 %); Karsee `_nah` per Rückfallring 19 m vom Ziel (WARNUNG Abstand, sonst stünde sie im See) |
| Selbsttest | 85 ok, 0 FEHLER (neu Schritt 13 `selbsttest_13k.py`, 17 Prüfungen) |
| Stufenvergleich gegen Basis (Stand vor 13k) | gleich 42 von 42 |
| Wasserfläche, Effekte, Vorhänge (56 Körper) | Effekte 75 = 75 nach Asset/Stufe/Position; Vorhang-Stufen gleich; Wasserhöhe an Lippe/Fuß/Becken gleich (nur zusätzliche Verdichtungspunkte, Zwischenwerte bis 1,2 cm) |
| Gesägte Stücke | 1 606 → 0 |
| `_fern` verdeckt (neue Achsenprüfung) | 24 → 0 |
| C2 (`0e00d17`, unverändert) | Planer 0 FEHLER, Gefälle-Prüfer 0 FEHLER / 2 WARNUNG |

**Neue WARNUNGEN:** nur die zwei kurzen Netze mit Schaum > 35 % (Abschnitt 6).

**Bekannte WARNUNGEN, unverändert:**
- Stufen ohne Niagara (Grenze 8).
- Karsee-Ufer 4 Proben auf 2 m.
- versickert < 25 m.
- Senken in lava.
- heide_06 `fall3`.
- gletscher_03 26,4 m.
- elfenwald_02 `_nah` 16 m.
- sumpf_02 Rohrkolben-Horst (Planer-Warnung).

**Nur auf synthetischen 1 m, alle WARNUNG:**
- Karsee `_nah` 19 m: Die Wandverkleidung belegt auf 1 m die Ufernischen. Neu ist ein Rückfallring bis
  Regelmaximum + 5 m; auf 2 m bleibt die Kamera unverändert.
- Schaum > 35 % an gletscher_03 (2 Netze) und heide_06 KN1.
- Bekannte Kamerawarnungen in elfenwald_05, fjord_06 und kueste_08.

**Testbilder:** Alle `sehens/<biom>/test_*.png` sind neu erzeugt.

## Lokal zu tun

1. **Neu planen auf 1 m** mit Commit `97e82a3` oder neuer. Alle Biome, mindestens bergwald:
   ```
   python -I recherche/antworten/skripte/sehens_bergwald/sehens_bergwald.py --basis <production>
   ```
2. **Säulenhain:**
   - Vorher zurückbauen: die alten Instanzen `SM_Forest_pine_04_0x_log` und `SM_Forest_pine_08_log`.
   - Einbauen: Ebene `sw_bergwald` B5/C5 und Lage `Nadeln`.
   - Kameras: `bergwald_03_saeulenhain_nah`, `_held`, `_fern` (neu, C4, 693 m NO).
   - Prüfen:
     - Waldboden: Schichten, kein Holzlager, kein Gras unter dem Hain.
     - Aus `_fern` stehen die Kronen frei, ohne Vordergrund-Kiefern.
     - Ferats Frage `Fir_07`-LOD auf ~690 m.
3. **Karsee:**
   - Ebenen neu (116 Wandnetze `wandverkleidung_60` als Instanzen mit Kollision, Schuttkegel).
   - Seefarbe `bergsee`: ist lokal schon gesetzt.
   - Kameras: `bergwald_06_karsee_nah` (Rückwand bis zur Oberkante in Fels, Schuttkegel am Fuß), `_held`,
     `_anmarsch`.
   - Schauseite der Klippen weiter `+y` angenommen (E35).
4. **Treppenbäche** (Karsee, Klamm):
   - `quer` neu einbauen, Material weiter nach 15g.
   - Erwartung: klare Becken, Schaum am Fuß 2–4 m auslaufend, Fallflächen mit Struktur.
   - Vorhänge auf `strahl_breite_m` je Stufe schmaler bauen (`vorhang` im Netz).
   - Aufprall-Effekte an Stufen ≥ 3 m mit `cull_m` 60–80 m.
   - Kameras: `B5_SW_bergwald_06_karsee_abfluss_kn0_unten`, `…_abfluss_kn0_nah_s13`, `…_zulauf_sued_kn0_nah_s27`,
     `…_zulauf_west_kn0_unten`.
5. **SLW2:** Skalierung 0,01 (bestätigt). Test mit tiefen Gumpen an C2 Version 3: Rot bei 1,5 m Tiefe auf ~55 %
   (Abschnitt 8).
6. **Neue `_fern`-Kameras der anderen Biome** (Tabelle Abschnitt 3): Bitte bei Gelegenheit ansehen, vor allem die
   zwei Aussichtspunkte ohne Weg (frost_06, kueste_03).

## Quellen

- Epic Games: [Single Layer Water Shading Model](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine)
  und [API UMaterialExpressionSingleLayerWaterMaterialOutput (4.27)](https://docs.unrealengine.com/4.27/API/Runtime/Engine/Materials/UMaterialExpressionSingleLayerWa-/index.html)
  – Eingänge Scattering/Absorption Coefficients, Bereich 0 bis unendlich, keine Einheit angegeben. Aus der Cloud nur
  über Suchauszüge erreichbar.
- Epic Developer Community: [Actually realistic water shader](https://forums.unrealengine.com/t/actually-realistic-water-shader/141661)
  – „clear water“: Absorption (0,35/0,07/0,03) × 0,01, Streuung (0,0007/0,0021/0,0025) × 0,01 (Meterwerte auf cm
  umgerechnet).
- World of Level Design: [UE5 Single Layer Water Pool](https://www.worldofleveldesign.com/categories/ue5/single-layer-water-pool-still.php)
  – Farbparameter mit Teiler für handliche Koeffizienten.
- Pope, R. M.; Fry, E. S. (1997): Absorption spectrum (380–700 nm) of pure water. Applied Optics 36(33), 8710–8723,
  [doi:10.1364/AO.36.008710](https://doi.org/10.1364/AO.36.008710) – Beer-Lambert-Werte reinen Wassers (Kontrolle
  e^−0,6 bei 1,5 m).
- Laurion, I. et al. (2000): Attenuation of ultraviolet radiation in mountain lakes. Limnology and Oceanography
  45(6), 1274–1288, [doi:10.4319/lo.2000.45.6.1274](https://doi.org/10.4319/lo.2000.45.6.1274) – gelöste Organik
  (CDOM) dämpft in klaren Hochgebirgsseen Blau und UV. Begründung für Blaugrün statt Tiefblau.
- Rose, K. C. et al.: [Light attenuation characteristics of glacially-fed lakes](https://repository.si.edu/items/112093e1-d628-41c4-88a7-ef64bc6625b1/full)
  – Gletschertrübe dominiert dort; Begründung, dass der Moränensee `gletschermilch` bleibt.
- Chow, V. T. (1959): Open-Channel Hydraulics, Kap. 3 (kritische Strömung, Q² T / (g A³) = 1) – Strahlbreite an der
  Lippe.
- Chin, A. (1999): The morphologic structure of step-pools in mountain streams. Geomorphology 27, 191–204 (im
  Regelwerk `CHIN1999`) – kurze Becken der Treppenbäche.
- Vorlagen im Repo:
  - `vorlagen/SEHENS_FORMAT.md` §3 (Lagen: neu = max(alt, Ziel), GPU-Gras aus den Lagen), §5 (Farben)
  - `vorlagen/daten/netze.csv`, `netze_masse.json` (Maße und Materialslots, `MI_Pine_lods_ends`)
- Auftrag 13k mit Nachträgen 11:45 und 12:35, Bilder `bilder/sehens_p2/*.jpg` (auch `pilot2_seefarben.jpg`,
  `pilot2_slw2_einheit.jpg`), `bilder/gefaelle_c2/c2_v2_schaum035.jpg`.

## Rückfragen

1. **Weitere Sägeschnitt-Kandidaten:** `SM_dead_log_01–05` (Forest Set) und `SM_pine_stump_01–05` (Mountain) haben
   kein `ends`-Material. Sehen ihre Enden im Editor gesägt aus? Dann nehme ich sie in die Regel auf.
   `SM_dead_log_*` nutzen aue (`knueppel`) und canyon (`treibholz`).
2. **A15-Holzstufen:** `gefaelle_regeln.json` → `biome.bergwald.netze.holz` nutzt `SM_Forest_pine_04_0x_log`
   (Holzstufen und Totholz-Querlagen der Gefällestrecken). Soll die Sägeschnitt-Regel auch dort gelten? Dann ersetze
   ich die Palette durch `SM_OldFallenTree_*`/`SM_FallenSpruceTree_01`. Das ändert die Instanzen der A15-Läufe,
   nicht C2s Wasser.
3. **`_fern` ohne Weg:**
   - frost_06 Eisküste (699 m neben dem nächsten Weg) und kueste_03 Nadeltor (457 m) haben nur von Aussichtspunkten
     ohne Weg eine freie Achse. Auf dem Weg verdecken Bestandskronen bzw. die Küstenkante.
   - Reicht das als Bildkamera, oder sollen dort Pfade bzw. Lichtungen (Freiraum) entstehen?
4. **Regel > 60° für alle Orte:** Eingeschaltet ist sie nur am Karsee. In 36 weiteren Orten sind 70 900 m² > 60°
   offen (Liste im Prüfer-HINWEIS). Kannst du die Bestand-Felsinstanzen je Feld exportieren? Dann kann der Prüfer
   sie als Deckung zählen, und die Regel lässt sich überall einschalten.
5. **Gras aus Moos und Nadeln:** Welche GT-Grasarten hängen an `Moos` und `Nadeln`? Wächst aus Nadeln nichts, ist die
   Nadelstreu 255 die vollständige Grassperre. Und wie verrechnet dein Werkzeug zwei Ziel-Lagen in derselben Zelle
   (Nadeln 255 + Moos 120)?
6. **A15 nachziehen?**
   - C2 hat 62 Akteure. Soll die Bündelung auf höchstens 50 aus Abschnitt 9 auch im Gefälle-Werkzeug laufen?
   - Sollen die A15-Netze dieselben Einheitenfelder in `material_parameter` bekommen (`einheit`, `skalierung_ue`,
     `SLW_*_pro_cm`)? Das ändert in C2 nur Metadaten.

## Nachtrag: Rückfragen 2 und 6 entschieden

Stand 12.10.2026, Code-Stand **`024d25f`** (bitte lokal mit diesem Commit oder neuer planen). Entscheidungen des
Koordinators:
- Rückfrage 2: Die Sägeschnitt-Regel gilt auch für A15, weil Gefälle-Bäche Wildnis sind.
- Rückfrage 6: Die Grenze von 50 Akteuren gilt je Sehens-Ort. Für Gefälle-Läufe gilt sie je 200 m Lauflänge bzw. je
  Back-Kachel. Wiederholte gleiche Akteure werden nach der 13j-Regel (≥ 12) Instanzen.

**Holz (`skripte/gefaelle/`):**
- `biome.bergwald.netze.holz`: Statt der drei gesägten `SM_Forest_pine_04_0x_log` stehen jetzt die natürlichen Netze
  aus Abschnitt 1 dort:
  - Stämme `SM_OldFallenTree_01/02`, `SM_LargeFallenTree_01/02`, `SM_FallenSpruceTree_01`, `SM_MossyTree_01`
  - Äste `SM_OldTreeBranch_01/02/03/04/06`, `SM_detail_branches_01/02/03`
- Elfenwald, Aue, Sumpf, Dschungel und Ödland bekommen dazu lange natürliche Stämme bzw. Äste. `SM_dead_log_*`
  bleibt, weil Rückfrage 1 offen ist.
- Das Netz wird nach Länge gewählt. Holzstufe: 0,45–0,7 × Lippenbreite, Totholz: 0,6–0,95 × Bachbreite. Erlaubt ist
  0,6–1,8 × Netzlänge (`stufen.holzstufe.netz_skala`).
- Vorher wurde das Holz bis × 45 skaliert: `SM_OldTreeBranch_01` lag auf 45 m, in breiten Flüssen lag `SM_dead_log_*`
  bis × 38.
- Die Stämme liegen jetzt quer zum Bach und folgen der Hangnormalen (`normale`, wie das 13k-Totholz).
  - Vorher waren sie mit `liegend` gesetzt. Das erwartet einen stehend modellierten Stamm (lange Achse z).
  - Liegend modellierte Netze (lange Achse x/y) standen dadurch schräg bis senkrecht im Bach.
  - Nur stehend modellierte Stücke (`Branch_Goat_Willow_Decaying_*`) bleiben `liegend`.
- Lage, Zahl und Höhe der Stufen sind unverändert.

| Holz (alle 161 Strecken, 2 m) | vor 13k | jetzt |
|---|---|---|
| Holzstücke (Holzstufen + Totholz) | 1 002 | 1 002 |
| davon gesägt (`*_log`) | 56 | **0** |
| Skala > 1,8 | 707 (max × 45,8) | **0** (max × 1,80) |
| Palette bergwald | 3 gesägte + 1 natürliches Netz | 14 natürliche |

Die 1 002 Stücke verteilen sich so:

| Netze | Stücke |
|---|---|
| `SM_OldTreeBranch_04` | 145 |
| `SM_LargeFallenTree_01` | 141 |
| `SM_OldFallenTree_02` | 136 |
| `SM_OldTreeBranch_06` | 131 |
| `SM_OldFallenTree_01` | 123 |
| `SM_LargeFallenTree_02` | 71 |
| `SM_MossyForestRoots_01/02/03` | 70 |
| `SM_MossyTree_01` | 35 |
| `SM_OldTreeBranch_02/03` | 34 |
| `SM_dead_log_01–04` | 100 |
| `SM_detail_branches_01/02/03` | 12 |
| Rest | 4 |

Holzstufen gibt es 327 (Aue 272, Elfenwald 44, Bergwald 7, Dschungel 4).

**Akteure:**
- Je Abschnitt gilt die 13j-Regel: Netze, die dort ≥ 12-mal als Akteur stehen, werden Instanzen mit Kollision.
- Danach gilt je Lauf: höchstens 50 Akteure je 200 m Lauflänge, gemessen in einem gleitenden Fenster.
  - Ist ein Fenster zu voll, greift die 13k-Logik: zuerst die häufigsten Netze, dann die kleinsten, nie die
    Held-Ebene.
  - Gemeinsamer Code in `sehens_lib/instanzen.py`: `akteure_wiederholt_buendeln`, `akteure_auf_grenze`,
    `akteure_je_fenster`.
- Prüfer:
  - `pruefe_ebene(…, kontext="sehens" | "gefaelle")`. Die Grenze „50 je Ort“ gilt nur im Kontext `sehens`, alle
    anderen Regeln gelten in beiden Kontexten (auch der Sägeschnitt).
  - `gefaelle_pruefen` meldet > 50 je 200 m als FEHLER.
  - `fluss_sim_pruefen` meldet > 50 Akteure eines Gefälle-Laufs je Back-Kachel als FEHLER.
- Lage, Größe und Drehung bleiben gleich. Niagara-Effekte und Vorhänge sind unverändert.

| Akteure (2 m) | vorher | jetzt |
|---|---|---|
| alle 98 Läufe mit Plan | 929 | 771 (144 nach 13j in 6 Läufen, 14 nach Fenster in `B_R_P1_M2_02`) |
| C2 (203 m) | 62 | **42** (20 × `rcygn_tier_0` als Instanzen) |
| `B_K8_ELFENFALL_01` | 90 (Abschnitt a1: 77) | 39 |
| `B_R_P4_M2_04` | 71 (a1: 68) | 38 |
| höchstens je 200 m Lauflänge | 76 (`B_K8_ELFENFALL_01`) | 49 (`B_R2_R_P4_M2_01`) |

**Prüfergebnis:**

| Lauf | vor 13k (`1de18bb`) | nach 13k (`8774ca9`) | jetzt (`024d25f`) |
|---|---|---|---|
| Gefälle `--alle` 2 m, Planer | 0 FEHLER | 189 FEHLER | **0 FEHLER**, 2 WARNUNG |
| Gefälle `--alle` 2 m, Prüfer | 0 FEHLER, 51 WARNUNG, 130 HINWEIS | 193 FEHLER, 57 WARNUNG, 126 HINWEIS | **0 FEHLER, 42 WARNUNG**, 129 HINWEIS |
| 19 Piloten, 1-m-Fenster, Prüfer | 0 FEHLER, 12 WARNUNG, 25 HINWEIS | 21 FEHLER, 13 WARNUNG, 22 HINWEIS | **0 FEHLER, 11 WARNUNG**, 23 HINWEIS |
| C2 (1-m-Fenster) | 0 FEHLER, 2 WARNUNG | 1 FEHLER (62 Akteure), 2 WARNUNG | 0 FEHLER, 2 WARNUNG (wie 15g) |

- **Determinismus:** `--alle` und die Piloten liefen je zweimal. Die Ausgaben sind identisch (`diff -r` ohne Bilder).
- **WARNUNG gegenüber dem Stand vor 13k:** 9 Warnungen „Instanzen schweben“ fallen weg (vorher stand Holz schräg im
  Bach). Neue Warnungen gibt es nicht. Die übrigen 42 sind die bekannten (Stufen ohne Niagara wegen der Grenze
  gleichzeitig, Becken > 2 %, 2-m-Raster).
- **Unverändert gegenüber dem Stand vor 13k:**
  - Stufen, Spiegel, Wasserkörper, Effekte, Kameras, Gelände- und Lagen-Dateien.
  - Die Gesamtzahl der Stücke (Instanzen + Akteure).
  - Etwa 1 800 von 65 000 kleinen Steinen und Kieseln rücken leicht, weil die Abstandsregel die neue Holzgröße sieht.
- **15 Sehens-Planer (2 m):** 0 FEHLER. Die Ausgaben sind byte-gleich mit dem Stand `8774ca9`; die Bibliothek ist nur
  umgebaut, das Verhalten ist gleich. Selbsttest grün: 90 Prüfungen, 0 FEHLER, davon 5 neu in Schritt 13 (Akteure
  nach Kontext).
- **fluss_sim neu** (Beispiele in `antworten/fluss_sim/` und Zahlen in Datei 16 aktualisiert):
  - Prüfer 0 FEHLER, 0 WARNUNG. Zwei Läufe byte-gleich (163 Dateien).
  - 1 120 Abschnitte, 765 Fälle und 555 Kacheln wie vorher.
  - Kollisionsobjekte 23 401 (vorher 23 397), eindeutig 22 825 (vorher 22 820).
  - Die Kollisionsobjekte verweisen auf die Instanzen; die ehemaligen Akteure stehen jetzt als Instanzen mit
    Kollision in den `*_kol`-Dateien.
  - C2: 625 Kollisionsobjekte wie vorher; 2 von 3 Kacheln haben einen neuen Fingerabdruck.

**Lokal zu tun:**
1. Gefälle-Läufe mit `024d25f` neu planen (1 m). Vorher die alten Holzinstanzen `SM_Forest_pine_04_0x_log`
   zurückbauen.
2. Danach `fluss_sim_export.py` neu laufen lassen. In C2 sind 2 Kacheln neu zu backen (geänderter Fingerabdruck).
3. Im Bild prüfen: Stämme liegen quer, keine stehenden Stämme, Holzstufen überspannen die Lippe.

**Offen:**
- Rückfrage 6, zweiter Teil: die Einheitenfelder (`einheit`, `skalierung_ue`, `SLW_*_pro_cm`) in den
  `material_parameter` der A15-Netze. Das ist nicht entschieden und nicht umgesetzt.
- Rückfrage 1 (`SM_dead_log_*`, `SM_pine_stump_*`) ist weiter offen. A15 nutzt `SM_dead_log_*` nur noch für kurze
  Stücke (100 Stück, Skala ≤ 1,8).
- Dieselbe `liegend`-Ausrichtung liegend modellierter Stämme steckt auch in Sehens-Regeln, z. B. ödland `staemme`
  (`SM_dead_log_01/03`). Das ist nicht geändert, weil die Sehens-Ausgaben gleich bleiben sollten.

## Nachtrag: Stammausrichtung Sehens, Einheitenfelder A15

Stand 12.10.2026, Code-Stand **`f1ec688`** (bitte lokal mit diesem Commit oder neuer planen). Damit sind die beiden
offenen Punkte aus dem Nachtrag oben erledigt.

**1. Stammausrichtung in den Sehens-Regeln**

- **Suche:** In allen 15 Sehens-Regeln habe ich jede Gruppe mit `ausrichtung: liegend` gegen die Netzmaße geprüft.
  `liegend` dreht die lokale Z-Achse in die Waagrechte. Richtig ist das nur für stehend modellierte Netze (lange
  Achse z).
  - **Richtig (bleiben):** Bäume (`Fir_08_Dead`, `SM_Forest_pine_08/09`, `SM_Forest_pine_10_dead`, `SM_beech_tree_08`,
    `SM_EuropeanBeech_Dead_M_01`), Basaltsäulen, Eiszapfen, `Branch_Goat_Willow_Decaying_*`.
  - **Falsch** (liegend modellierte Stämme mit `liegend`), zwei Gruppen:
    - ödland `oedland_04_dornbusch_senke` → `staemme`: `SM_dead_log_01/03`
    - sumpf `sumpf_02_der_weidendom` → `treibende_aeste`: `SM_dead_log_02`
  - Beide Paletten mischen stehend und liegend modellierte Netze. Eine Änderung der Regel-Datei hätte deshalb nicht
    gereicht.
- **Behebung in der Bibliothek** (`rezept._ein_stueck`, nach dem Vorbild von A15 `holz_form`, `024d25f`):
  - Steht `liegend` an einer Gruppe mit `rolle: stamm` und einem liegend modellierten Netz, wird dieses Netz mit
    `normale` gesetzt. Es folgt damit der Hangnormalen wie das 13k-Totholz.
  - Die lange Achse zeigt in die Yaw-Richtung, also dorthin, wohin vorher der Stammkopf zeigte.
  - Der Zufallswert für den Roll wird weiter gezogen. So bleibt die Zahlenfolge gleich, und alle anderen Stücke
    bleiben, wo sie waren.
- **Skala:** Liegende Stämme als Instanzen sind auf 0,6–1,8 begrenzt, Äste nur nach oben (≤ 1,8).
  - Betroffen waren nur Stücke über 1,8: ödland `staemme` (bis × 2,2) und `oedland_07_totenpfanne` → `liegende`
    (bis × 2,0).
  - Einzeln gesetzte Akteure behalten die Skala aus ihrer Regel. Das sind die Riesen in Held- und Begleiter-Ebene,
    z. B. elfenwald_07 Riesenstamm × 4,6, dschungel_07 Sturzstamm × 4,2, sumpf `liegende` × 2,0–2,6. Der Prüfer
    nennt sie als HINWEIS (40 Akteure in 6 Biomen). Soll auch für sie 1,8 gelten, ist das eine Bildentscheidung, bitte sagen.
- **Neue Prüferregel** `pruefe_liegendes_holz` in `pruefe_ebene`, gilt in den Kontexten Sehens und Gefälle:
  - Geprüft werden liegend modellierte Holznetze (`inventar.liegendes_holz`: Stamm- oder Ast-Name, lange waagrechte
    Achse ≥ 1,5 × Höhe; Wurzeln, Stümpfe und Bäume nicht).
  - **FEHLER**, wenn die Hochachse mehr als **45°** von der Hangnormalen abweicht (Gelände nach dem Stempel), der
    Stamm also steht oder auf der Kante liegt.
  - **FEHLER**, wenn eine Instanz außerhalb der Skala liegt (Stämme 0,6–1,8, Äste ≤ 1,8). Bei Akteuren ist das ein
    HINWEIS.
  - **Warum gegen die Hangnormale:** Gegen die Senkrechte gemessen kommen auch richtig gesetzte Zweige auf
    Steilhängen auf bis zu 75°. Gegen die Hangnormale liegen alle richtig gesetzten Stücke bei höchstens 36°, die
    falschen bei 80–92°.
  - Selbsttest Schritt 13, Teil 9: 5 neue Prüfungen.
- Treppen, Stufen, Effekte, Kameras, Gelände und Lagen sind unverändert. `orte.json` ist in allen 15 Biomen
  byte-gleich.

| Betroffene Stücke (2 m) | Ort | vorher | jetzt |
|---|---|---|---|
| `SM_dead_log_01/03`, `staemme` | oedland_04 Dornbusch-Senke | 8 stehend (80–92° gegen die Hangnormale), 4 davon × 1,87–2,02 | 8 liegend, Skala ≤ 1,8 |
| `SM_dead_log_01/02/04`, `liegende` | oedland_07 Totenpfanne | 9 mit × 1,81–1,97 (Lage richtig) | 9 mit × 1,8 |
| `SM_dead_log_02`, `treibende_aeste` | sumpf_02 Weidendom | 32 stehend oder auf der Kante (bis 90°) | 32 liegend |
| **Summe** | 3 Orte | **40 Stämme falsch ausgerichtet, 13 zu groß skaliert** (4 davon beides) | 0 |

Daneben rücken im Feld D6 (Dornbusch-Senke, Totenpfanne) 54 von 3 670 kleinen Steinen (`SM_SmallStonesPack_*`) um bis
zu 2,8 m, weil die Abstandsregel die liegenden Stämme sieht. Die anderen 13 Biome sind byte-gleich mit dem Stand vor dem Nachtrag.
Testbilder neu: `test_oedland_04_dornbusch_senke.png`, `test_oedland_07_totenpfanne.png`,
`test_sumpf_02_der_weidendom.png`. Alle übrigen Testbilder sind byte-gleich.

**2. Einheitenfelder in den A15-Kaskadennetzen**

- `gefaelle_plan.slw_einheit` schreibt in `material_parameter` jedes Kaskadennetzes dieselben Felder wie in den
  Sehens-Netzen. Schlüssel und Reihenfolge sind gleich:
  - `einheit: "je_m"`, `skalierung_ue: 0.01`
  - `SLW_Absorption_pro_cm` [0,004; 0,0007; 0,0005] und `SLW_Streuung_pro_cm` [0,0002; 0,0003; 0,0004]
  - `einheit_hinweis`
- Die je-m-Werte (`SLW_Absorption_pro_m` 0,40/0,07/0,05, `SLW_Streuung_pro_m` 0,02/0,03/0,04) sind unverändert.
- `--alle` 2 m: 123 Kaskadennetze in 98 Läufen tragen die Felder, C2 eingeschlossen. Sonst sind die Pläne gleich mit
  `024d25f`: Instanzen, Gelände, Lagen, Wasser, Effekte. Die Sehens-Netze sind byte-gleich, weil `bach.py` dieselben
  Werte setzt.

**Prüfergebnis**

| Lauf | Ergebnis |
|---|---|
| 15 Sehens-Planer, 2 m | Planer und Prüfer **0 FEHLER** in allen 15. Vorher fand der neue Prüfer 8 FEHLER (ödland 6, sumpf 2). Zwei Läufe byte-gleich (`diff -r`). |
| 15 Sehens-Planer, synthetisch 1 m | Planer und Prüfer **0 FEHLER** in allen 15 |
| Selbsttest | grün, 95 ok, 0 FEHLER (vorher 90; neu: 5 Prüfungen Stammausrichtung) |
| Gefälle `--alle` 2 m | Planer 0 FEHLER, 2 WARNUNG; Prüfer **0 FEHLER**, 42 WARNUNG, 129 HINWEIS (wie `024d25f`). Zwei Läufe identisch. |
| 19 Piloten, 1-m-Fenster | Planer 0 FEHLER; Prüfer **0 FEHLER**, 11 WARNUNG, 23 HINWEIS (wie `024d25f`). Zwei Läufe identisch. |
| fluss_sim neu | Prüfer **0 FEHLER**, 0 WARNUNG, 10 HINWEIS. Zwei Läufe byte-gleich (163 Dateien). |

- **fluss_sim:**
  - Abschnitte, Fälle, Kollisionsobjekte und Back-Liste sind gleich: **0 Back-Kacheln mit neuem Fingerabdruck**.
  - Keiner der 49 geänderten Stämme liegt in einem Gewässer mit Kachel. ödland_04, ödland_07 und sumpf_02 haben keinen
    Sehens-Bach.
  - Geändert hat sich nur `objekt_pool.fest_und_gross`: 63 898 → 63 887. 11 Stämme sind liegend bzw. mit Skala ≤ 1,8
    kleiner als die Mindestgröße für feste Objekte.
  - Beispiele in `antworten/fluss_sim/`: nur `zusammenfassung.json` geändert. Die Zahlen in Datei 16 bleiben.
- Die Prüferregel greift auch in A15. Die Gefälle-Läufe melden 0 FEHLER, weil das Holz dort seit `024d25f` quer und
  mit Skala 0,6–1,8 liegt.

**Lokal zu tun:**
1. ödland und sumpf mit `f1ec688` neu planen (1 m). Die Ebenen `sw_oedland` und `sw_sumpf` tauschen; betroffen
   sind die Felder D6 bzw. H5/I5.
2. Im Bild prüfen:
   - Dornbusch-Senke: tote Stämme liegen im Gestrüpp.
   - Weidendom: `SM_dead_log_02` treibt flach.
   - Totenpfanne: Stämme ≤ × 1,8.
3. Gefälle-Läufe neu planen ist nicht nötig. Nur wer die Felder `einheit`/`SLW_*_pro_cm` im Werkzeug lesen will, plant
   neu. Kein Neubacken nötig.
