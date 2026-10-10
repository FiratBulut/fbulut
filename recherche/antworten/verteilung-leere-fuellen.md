# Leere füllen: Mittelschicht 0,3–3 m und Spuren von Leben (Auftrag 11, Teil D)

**Projekt:** Eldarien, UE 5.8.3, 9,6 × 7 km, 62 Landfelder. **Stand:** 2026-10-10 (Fortsetzung nach API-Abbruch). **Lieferung:** dieser Bericht, `skripte/mittelschicht_regeln.json` + `mittelschicht_plan.py`, `skripte/spuren_regeln.json` + `spuren_plan.py`. **Status der Skripte:** `py_compile` sauber; Rauchtest mit synthetischer Produktionswurzel bestanden (G4 mit Orten/Weg/See/932 Bäumen, Randfeld A1, baumloses G3, Budget-Zwangstest, Fehlerpfade; Abschnitt 5). Echtdaten-Lauf der Vorfassung lokal ohne Absturz (A5/G4/E1/C6); **Korrektur Runde 1 siehe Abschnitt 8** (Biom-Zuständigkeit, Pflichtschlüssel, Ebenen-Abgrenzung, Override-Schema, Budget, ASCII-Logs). Beide Planer prüfen beim Start alle Netzpfade ihrer Regeldatei gegen `daten/netze.csv` (237 + 85 Pfade, 0 fehlend) und brechen bei unbekannten Netzen mit Liste ab. Paletten nachträglich gegen `assets-taxonomie.json` geprüft: 663 von 830 Netz-Biom-Zuordnungen der Mittelschicht haben Eignung ≥ 1 (80 %); die übrigen sind bewusste Zweitverwertung in Biomen ohne eigene Mittelschicht (gletscher, frost, lava, oedland, canyon, wueste: Trockengras, Dürräste, Totbäume) sowie 54 Dschungel-Zuordnungen (gemäßigte Farne/Holunder als Füller; Abschnitt 7).

## 1. Befund aus den Bildern: was in 0,5–3 m Höhe fehlt

Gezählt je Bild, was innerhalb von ~10 m um die Kamera (≈ 300 m²) zwischen Knie- und Kopfhöhe steht; der Witcher-Richtwert ist aus den Zielbildern gleich geschätzt.

| Bild | Was in 0,5–3 m steht (10-m-Umkreis) | Objekte je 100 m² heute | Witcher-Richtwert (gleiche Zone) |
|---|---|---|---|
| KLEIN12_G3_boden (Buchenwald, Augenhöhe) | 1 roter Strauch, 1 aufliegende Felsplatte, sonst 0,1-m-Sprösslinge einer Größe; kein Farn, Stamm, Ast, Stumpf, Jungbaum | **0,5–0,7** | witcher_03 (Nadelwald Kovir): Fichtenast als Vordergrund, 3 junge Fichten 1–3 m, 2 liegende Stämme, 1 Wurzelteller, 4 Blöcke, Sträucher am Hangfuß → **≈ 4–5** |
| W6FIN_G3_rundgang (Kiefern-Bergwald, Luftbild) | nur Kronen und roter Boden; zwischen Stämmen weder Sträucher noch Jungwuchs noch Totholz; Waldkante hart | **< 0,2** | witcher_07-Logik (Bildkritik §3): Waldsaum aus Büschen und Jungbäumen, 30–60 m Falloff; Stämme/Äste 2–3 % |
| W6FIN_E5_rundgang (Küstenwiese, Weiden) | Bäume im 15-m-Raster, Wiese einfarbig, 0 Büsche, 0 Hochstauden, 0 Steine | **0,3** | witcher_01 (Flussaue): Sträucher 0,8–1,5 m am Ufer, Hochstauden-Inseln (3–8 Stück), Schilf, 6–8 Blöcke, Jungkiefern → **≈ 2,5–3,5** |
| TERR3_I5_rundgang (Küstenhügel) | Kiefern und Birken einzeln, dazwischen leere Trockenwiese, Ufer ohne Gebüsch | **0,3–0,5** | witcher_05 (Dorf): jede Fläche hat 2–3 Objektgrößen (Kisten, Fässer, Karren, Zaun) → Spuren **5–8 je 100 m² im Ort**, 1–2 im Umland |

Die Lücke ist ein Faktor **5–10** in der Mittelschicht (offen 0,3 → 2,5; Wald 0,5 → 4–5) und **> 10** bei Spuren von Leben (außerhalb der Houdini-Orte heute 0). Boden- und Baumebene sind da; die Höhe dazwischen ist leer, und nichts verrät, dass Menschen hier leben.

## 2. Mittelschicht-Regeln 0,3–3 m (alle 15 Biome)

> Stand Runde 0. Seit Korrektur Runde 1 heißen die Totholz-Klassen `totholz_liegend`, `totholz_stumpf`, `totholz_ast`; `schilf` entfällt, `totbaum`/`wurzel`/`kletter` nur noch in einzelnen Biomen, Paletten werden von den Biom-Planern überschrieben – siehe Abschnitt 8.

Alle Zahlen stehen in `mittelschicht_regeln.json` (Biom → Klasse → Netze, Dichte, Gruppe, Maßstab, Eingraben, Kippen, Sichtweite, Kollision; 14 Klassen: farn, strauch, jungbaum, beere, hochstaude, schilf, grasbueschel, totholz, stumpf, ast, wurzel, pilz, kletter, totbaum).

**Lichtverhältnis (Kronendach).** Der Planer liest alle Baumpositionen aus `bestand/<Feld>/`, `witcher/<Feld>/` (plus 8 Nachbarfelder, nur Instanzen im Fenster) und `instanzen/instanzen.json` (Houdini-Klassen mit „baum“). Jede Krone wird mit Gewicht Maßstab² auf das 1-m-Raster gesplattet, Gauß σ = 6 m (3 Box-Durchläufe), Deckung = π·4,5²·Dichte, **Beschattung = 1 − exp(−1,6·Deckung)**. 100 Bäume/ha ergeben 0,64, 330 Bäume/ha 0,97. Ohne Baum-Ebene (Log-Hinweis) wird aus `lage_Laub/Nadeln/Moos` geschätzt, gedeckelt bei 0,7. Jede Klasse hat eine Dichte `[offen, beschattet]` je m², linear interpoliert: Farne, Pilze, Wurzeln, Kletterpflanzen steigen mit Schatten; Sträucher, Jungbäume, Grasbüschel fallen.

**Waldrand-Saum.** Wald = Beschattung > 0,35; Waldkante = Waldzelle mit Nicht-Wald-Nachbar; Kantendistanz per Jump-Flooding. Saumfaktor steigt linear von 1 auf den Klassenwert (Strauch 2,5, Jungbaum 2,0, Beere/Hochstaude 1,5–1,8) innerhalb **15 m nach innen** und **10 m nach außen** (Naturschutzbund: Strauchgürtel 5–10 m, Waldmantel 10–20 m). **Lichtungsränder** (offen, Beschattung < 0,18, < 40 m von der Kante, Kantenabstand ≤ 8 m) erhalten für Jungbäume Faktor 2–3 („Schösslinge an Lichtungsrändern“).

**Feuchte.** `0,8·max(0, 1 − d_Wasser/40 m) + 1,0·Schlamm + 1,0·Algen + 0,6·Moos + 0,3·Kraut + 0,3·Lehm`, geklippt 0–1. Klassen haben `feuchte: [trocken, nass]`-Faktoren: Farn 0,5→1,8 (Elfenwald), Weiden/Holunder in der Aue 0,6→2,5; Schilf nur im Uferband 0–6 m (Zusatzdichte 0,03–0,05/m²).

**Hang, Höhe, Schnee.** Voll bis 22°, linear auf 0 bis zum Klassen-`hang_max` (meist 35°; Kletterpflanzen 90°). Ab 350 m linear abnehmend, 0 ab 650 m; Klassen-Obergrenzen (Zwergkiefer 350 m, Krüppelkiefer 300 m). Lage Schnee reduziert auf 25 %, Eis auf 0.

**Gruppen.** Farninseln 3–12 (Radius 3 m), Beeren/Heide 4–14 (2,5–3 m), Hochstauden 3–10, Sträucher 1–4, Jungbäume 1–5, Pilze 3–8 (1 m), Totholz 1–2. Gruppenzentren mit Dichte/Gruppenmittel gestreut, Mitglieder gleichverteilt in der Scheibe, jedes Mitglied erneut gegen Freiflächenmaske und Dichte > 0 geprüft.

**Dichten (Instanzen je m², offen / beschattet) – Auszug:**

| Biom | Strauch | Jungbaum | Farn | Beere/Heide | Hochstaude | Grasbüschel | Totholz (Koll.) | Stumpf (Koll.) | Ast | Pilz |
|---|---|---|---|---|---|---|---|---|---|---|
| elfenwald | 0,014 / 0,005 | 0,010 / 0,003 | 0,006 / 0,022 | – | 0,008 / 0,010 | 0,012 / 0,002 | 0,0006 / 0,0022 | 0,0003 / 0,0011 | 0,004 / 0,010 | 0,002 / 0,010 |
| bergwald | 0,012 / 0,004 | 0,010 / 0,003 | 0,002 / 0,009 | 0,015 / 0,030 | 0,004 / 0,002 | 0,012 / 0,003 | 0,0004 / 0,0018 | 0,0003 / 0,0010 | 0,004 / 0,012 | 0,001 / 0,006 |
| aue | 0,0045 / 0,002 | 0,0025 / 0,001 | 0,001 / 0,005 | – | 0,012 / 0,004 | 0,016 / 0,004 | 0,0007 / 0,0012 | 0,0004 / 0,0006 | 0,003 / 0,006 | 0,001 / 0,003 |
| heide | 0,004 / 0,002 | 0,003 / 0,001 | – | 0,045 / 0,020 | 0,008 / 0,003 | 0,020 / 0,006 | 0,0005 / 0,0008 | 0,0002 / 0,0005 | 0,006 / 0,005 | 0,002 / 0,003 |
| tundra | 0,0035 / 0,002 | 0,0012 / 0,0006 | – | 0,040 / 0,025 | 0,002 / 0,001 | 0,030 / 0,010 | 0,0003 / 0,0004 | – | 0,004 / 0,003 | – |
| sumpf | 0,008 / 0,004 | 0,002 / 0,0012 | 0,006 / 0,014 | – | 0,012 / 0,010 (+Schilf 0,05 Ufer) | 0,010 / 0,004 | 0,0015 / 0,0030 | 0,0006 / 0,0015 | 0,004 / 0,006 | 0,003 / 0,008 |
| dschungel | 0,010 / 0,006 | 0,006 / 0,003 | 0,010 / 0,030 | – | 0,012 / 0,015 | 0,010 / 0,004 | 0,0010 / 0,0030 | 0,0003 / 0,0010 | 0,004 / 0,008 | 0,002 / 0,006 |
| kueste / fjord | 0,008 / 0,003 · 0,0065 / 0,003 | 0,004 / 0,0015 | – · 0,002 / 0,006 | 0,010 · 0,020 | 0,006 / 0,003 | 0,016 / 0,005 | 0,0008 / 0,0010 | 0,0002 / 0,0005 | 0,004–0,005 | – |
| gletscher / frost | 0,0012 / 0,0006 | – | – | 0,010 / 0,006 | – | 0,010 / 0,004 | 0,0001 | – | 0,002 | – |
| lava | 0,0010 / 0,0005 | – | – | 0,006 / 0,003 | – | 0,006 / 0,003 (×0,1 auf Lavafels) | 0,0002 | – | 0,003 | – |
| wueste / canyon / oedland | 0,002–0,003 (Rooibos) | – | – | – / – / 0,004 | – | – / 0,006 / 0,008 | 0,0002–0,0004 | – | 0,002–0,004 | – |

Für den Blick-Test: Im Elfenwald (Beschattung 0,7) summieren sich Farn + Strauch + Jungbaum + Hochstaude + Totholz auf **≈ 0,044/m² = 4,4 Objekte je 100 m²** (plus Äste/Pilze), im offenen Elfenwald-Saum 0,06, in der offenen Aue 0,02–0,035 mit Hochstauden-Inseln – die Witcher-Spanne aus Abschnitt 1. Dazu stehende Totbäume 0,5–3 je ha im Wald (Sumpf 3–6), Wurzelteller 0,5–3 je 1 000 m² nur im 1–2-m-Ring um Stämme, Efeu/Lianen an 8 % (Elfenwald) bzw. 25 % (Dschungel) der Stämme.

**Maßstab, Eingraben, Kippen, Sichtweiten, Kollision.** Maßstab je Klasse 0,7–1,4 (Dschungel-Busch `SM_Bush_01a` 0,45–0,8, weil 3,4 m hoch); Eingraben Pflanzen 2–5 cm, Stümpfe 8–12 cm, liegende Stämme 25–30 cm, Totbäume 15–20 cm; Kippen auf die Normale: Sträucher/Farne 30 %, Jungbäume 10 %, Totbäume 5 %, Totholz/Äste/Wurzeln 100 %, Stämme zusätzlich längs zum Gefälle ±20°. Sichtweiten: Pilze 60 m, Kleinzeug/Hochstauden/Beeren/Äste 120 m, Sträucher/Farne/Jungbäume 300 m, Totholz/Stümpfe 450 m, Totbäume 0. **Kollision nur** Totholz liegend, Stümpfe, Totbäume (936–1 666 je Feld im Test, Deckel 3 000 mit Ausdünnung). Abstände: Kleinzeug 2,5 m, Großes 4 m zum Weg, 5 m zum Ort, 1 m zum Wasser, 0,9 m zu Stämmen (Totbäume 3 m), 1,2 m zu vorhandenen Witcher-/Bestand-Instanzen (werden gelesen und als belegt markiert).

**Budget je Feld.** Ziel 52 000, Deckel 60 000; Überschuss wird gemeinsam-proportional aus den niedrigsten Prioritäten (Pilz, Ast, Grasbüschel, …) gedünnt, höchstens 50 % je Klasse und Runde; Protokoll in `plan.json["hinweise"]`. Wüstenfelder C3–E5: Feldfaktor 0,5 (nur ergänzen).

**Witcher-Belege.** CDPR nutzte ~20 Baum-/Straucharten mit je 5–12 Modellen, 40 Grasarten und Biom-Pinsel (80.lv, GameBanshee); SpeedTree zählt ~200 Pflanzentypen; die Witcher-4-Demo streut Kleinzeug per GPU-PCG plus Nanite (boden-kleinzeug-gras.md). Für Dichten nennt keine Quelle Zahlen; die Werte sind aus den Zielbildern abgezählt und mit Ökologie-Spannen plausibilisiert (Jungwuchs 0,7–7,5/m² in Naturwäldern nach Harms et al. 2004 liegt weit über unseren 0,003–0,01, weil nur sichtbare 0,3–3-m-Exemplare gesetzt werden; Strauchgürtel/Waldmantel nach Naturschutzbund und LFI Schweiz).

## 3. Spuren von Leben (spuren_plan.py)

**Orte** werden aus `karte_ort.r8` abgeleitet: Maske auf 4-m-Raster, Zusammenhangskomponenten per Min-Label-Ausbreitung (vektorisiert), je Komponente Mittelpunkt, Fläche, Radius = √(A/π), Biom am Mittelpunkt; ≥ 400 m² gilt als Ort, kleiner als Einzelbauwerk (nur Rauch mit 50 %). **Wege**: Distanzfeld mit Seed-Rückgabe liefert je Zelle Abstand, Normale und Tangente – Zäune, Karren, Kreuze stehen parallel bzw. frontal zum Weg. **Seen**: Wasserkomponenten ≥ 2 500 m² und ≥ 15 m breit, Uferzellen 1–2 m vom Wasser, Hang ≤ 7°, Tiefe 6 m vom Ufer 0,3–1,6 m (bilinear aus `hoehe.f32`) = flaches Ufer.

| Spur | Regel (Zahlen in `spuren_regeln.json`) | Netze im Inventar | Ausgabe |
|---|---|---|---|
| **Feldstreifen** | Ring 30–150 m um Orte, Raster 36 m, 55 % der Zellen, Rechtecke 20–60 × 20–60 m, Ausrichtung = Wegtangente (Weg < 80 m) sonst Höhenlinie, 2. Versuch um 90° und 0,7/0,5-fach; Hang ≤ 8°, Beschattung ≤ 0,3, Weg > 6 m; max 12 je Ort, 30 je Feld; 35 % mit Feldfrucht-Reihen (1,2 × 0,9 m), sonst Stoppeln 0,08/m²; 0–3 Heuhaufen | Zaun `SM_fenceA/D/E_a1` (3,29 m, 15 % Lücken, ±6° Kippen), Frucht `SM_flower_sunroot_01/02` (0,6–0,9), Stoppel `SM_dead_grass_01/02`, Heu `SM_Hay_Pile`, `SM_StrawPile_01a`, `SM_Hay_02` | Zaun/Pflanzen als Foliage; Rechteck als `flaechen[]` mit `lage_vorschlag` Erde/Lehm |
| **Trockenmauern** | In Stein-Biomen (fjord, kueste, bergwald, heide, tundra, gletscher, frost) statt Holzzaun: Steine alle 0,45 m, 3 Lagen (0 / 0,28 / 0,52 m; 100/85/50 %), Versatz ½ Stein, Jitter ±12 cm, Basis 8 cm eingegraben, Maßstab 0,8–1,2 | `SM_mountain_rock_small_01_1/2/4/5`, `SM_s_rock_01–03`, `SM_stones_01_1/4/5`, `SM_MossyForestRock_01` | Foliage ohne Kollision (Budget) |
| **Obstgarten** | 1 je Ort mit Radius ≥ 35 m, Ring 20–90 m, 30–50 × 24–40 m, Reihen 7 m, Abstand 6 m, Jitter ±0,6 m, Maßstab 0,7–1,0, vor den Feldstreifen gesetzt | Ersatz je Biom: `SM_EuropeanHornbeam_Forest_09/10` (Nanite), `SM_beech_tree_00_B/C/D`, Küste `SM_dry_oak_02_C/D`, Nadelbiome `SM_pine_beach_small_01/02`, Dschungel `SM_Palm_01_06–08_G` | Foliage mit Kollision, `flaechen[]` obstgarten |
| **Zaun am Weg** | 1–3 Läufe je Ort, Wegabstand 3,5 m, Ortsrand 10–70 m, Länge 20–60 m, 20 % Lücken, eine Wegseite (Vorzeichen der Normalen am Ortsmittelpunkt) | Holzzaun + `SM_Fence_01` (Town); Stein-Biome: Mauerstücke | Foliage |
| **Steinmänner** | a) Wegmarken in Stein-Biomen alle 90–140 m (3–6 m neben dem Weg, 80 %); b) Kuppen (lokales Maximum 90 m, Prominenz ≥ 12 m); c) frei 6 je km² (Weg > 20 m, Ort > 60 m, Hang < 25°). 5–9 Steine, Basis 1,5–2,2-fach, Abnahme 0,82, Höhenversatz 0,24 m·Maßstab, Versatz 6 cm·√k | `SM_mountain_rock_small_01_*`, `SM_s_rock_01/02`, `SM_NordicBeachRock_01` | Foliage mit Kollision |
| **Wegkreuze / Schreine** | Wegband 3–5 m, 1 je 220-m-Raster, Score = Zufall + 2 (Kuppe ≤ 10 m) + 2 (Furt: Wasser 2–15 m) + 1 (Ortsrand 40–90 m), Schwelle 0,35; Front zum Weg; in elfenwald/dschungel/aue/sumpf 40 % Schrein | Kreuz `SM_Cross` (0,81 m → ×2,2–2,6, ±5° schief) auf 3 Steinen; Schrein = `SM_Column_03` (×0,6) + `SM_Lamp` + 2 Sträucher | Kreuz/Säule als Akteur |
| **Verlassene Karren** | Wegband 2–5 m, 1,6 je km Weg (Raster 390 m, 65 %), Ort > 120 m, Yaw = Tangente ±15°, Roll 4–14°, 1–3 Beiwerk (Fass, Kiste, Rad, Sack) in 1,4–3 m | `SM_cartB_a1`, `SM_BrokenWoodWagon` (Nanite), 20 % `SM_Carriage_01a` | Karren als Akteur |
| **Fischerstege** | flache Seeufer, Ort ≤ 400 m oder Weg ≤ 80 m, max 3 je Feld, 2–4 Segmente à 4 m, 4 Planken à 0,31 m, Deck 0,6 m über Uferhöhe, 2 Pfosten je Segment (3,8 m eingesenkt), Längsbalken, Geländer am Ende, 1–2 Fässer/Kisten/Trog am Landende | `SM_PlankThin_4m_01a`, `SM_Plank_4m_01a`, `SM_Beam_4m`, `SM_Rail_3m`, `SM_Trough_01a` | Foliage mit Kollision; Achse als `punkte[typ=steg]` |
| **Holzschlag-Lichtungen** | Lichtung ≥ 150 m² im Wald (Waldanteil 60 m > 0,3), Weg 8–180 m, Ort > 60 m, max 3 je Feld, Radius 12–22 m: Stümpfe 0,045/m², Äste 0,03/m², 2–5 Stämme mit gemeinsamer Richtung ±20°, 1–2 Stapel, 30 % Karren, 30 % Lagerfeuer (5 Steine + Rauchpunkt) | Stümpfe nach Biom (Nadel: `SM_pine_stump_01–03`, `SM_TreeStump_01`; Laub: `SM_BirchTreeStump_01`, `SM_BrokenStump_01`, `SM_stump_03`, `SM_Tree_Stump_02`), Stämme `SM_Forest_Pine_09/04/08_log`, `SM_LargeFallenTree_02`, Stapel `SM_Pile_WoodLog_02a`, `SM_firewoodSetA_a1` | Foliage (Stümpfe/Stämme Kollision) |
| **Köhlerplätze** | Beschattung 0,3–0,75, Hang ≤ 6°, Weg 40–220 m, Ort > 80 m, kein Stamm im 7-m-Umkreis, max 2 je Feld: Meiler = 6 Holzstapel im Ring r 3,2 m tangential + 2. Ring 0,55 r um 0,9 m erhöht, 10 Stümpfe 10–18 m, Feuerholz/Fass/Kiste | `SM_Pile_WoodLog_02a`, `SM_firewoodSetA_a1`, `SM_barrelClosedA_a1`, `SM_crateA_a1` | Rauchpunkt `meiler` (0,6), `flaechen[]` Kreis r 7 m Lage Erde |
| **Gräber** | Friedhof je Ort mit Radius ≥ 25 m: 12 × 18 m im Ring 8–30 m, Reihen 1,6–2,2 m, 70 % belegt, Kreuze 0,9–1,3, ±8° schief, Umfriedung Mauer/Zaun, 60 % ein Totbaum; Einzelgräber 0,7 je km Weg (4–8 m vom Weg, Ort > 100 m): Kreuz + 3 Steine + 1 Ast | `SM_Cross`, `SM_DeadTree_01/02`, `SM_EuropeanBeech_Dead_M_01` | Friedhof als `flaechen[]`, Totbaum als Akteur |
| **Rauchsäulen** | je Ort `clip(Fläche/1000·1,2, 1, 10)` Punkte in Ortszellen (30-m-Raster), 2,5 m über Boden, Stärke 0,5–1,0; Meiler 0,6; Lagerfeuer 0,3 | – (Partikel) | `punkte[]` typ herd/meiler/lagerfeuer, x/y/z cm, staerke |

**Ausgabe-Konventionen (plan.json).** Wie `felsgruppen_plan.py`: Großobjekte (Kreuze, Schrein-Säulen, Karren, Grab-Totbäume) liegen in `akteur_<Netz>.f32` mit `rolle: "akteur"` und zusätzlich in der Liste `akteure[]` (x, y, z, Quaternion, Maßstab); alle anderen Dateien sind HISM-Foliage `FT_EL_SP_<Netz>` unter `/Game/Eldarien/Welt/Foliage/Spuren`. Ein Netz, das in mehreren Gruppen vorkommt (z. B. `SM_Cross` als Wegkreuz-Akteur und als Grabkreuz-Foliage), bekommt je Datei genau eine Kollisionseinstellung (Vereinigung). `hinweis_setzer` im plan.json erklärt `akteure`, `punkte` (Niagara-Rauch an x,y,z; Stegachse) und `flaechen` (Rechtecke/Kreise zum Malen der Landschaftslage). **Budget:** Deckel 60 000 Instanzen und 3 000 mit Kollision je Feld werden im Planer durchgesetzt – deterministische Ausdünnung in der Reihenfolge `budget.prioritaet` (feld, mauer, zaun, grab, holzschlag, koehler, steg, wegkreuz, karren, steinmann, obstgarten, schrein; höchstens 60 % je Gruppe und Runde); Akteure werden nie gedünnt (eigener Deckel 400).

**Was im Inventar fehlt (Spuren):** kein Steinmauer-Modul (aus Einzelsteinen gebaut, 2,2 Steine je Meter → 130–280 Instanzen je Mauer), kein Steinmann-Netz, kein Wegkreuz in Mannshöhe (Grabkreuz 2,4-fach skaliert; Texeldichte sinkt), kein Schrein/Bildstock, keine echten Obstbäume, kein Steg-Modul, kein Meiler, kein Brunnen außer dem orientalischen `SM_Well_02a` (nicht verwendet), keine Vogelscheuche, Bienenkörbe, Galgen, Wegweiser. Siehe Einkaufsliste.

## 4. Blickziele je Landfeld

**Koordinatenregel (im Planer umgesetzt, Ausgabe `plan.json["blickziele"]`):**
- **Kuppe** = lokales Maximum im 150-m-Fenster (exakter gleitender Max-Filter) **und** Prominenz (Höhe − 150-m-Mittel) ≥ 15 m **und** Hang ≤ 18°; Score = Prominenz + 20·Sichtbarkeit (Anteil tiefer liegender Umgebung) + 5 (Weg < 150 m); je 200-m-Raster ein Kandidat, die 3 besten je Feld.
- **Typ nach Biom** (`blickziele.typ_je_biom`): Kuppe im Offenland (Beschattung ≤ 0,15) → *Solitärbaum* (alter Baum 1,3–1,5-fach, Felsblock, Stamm als Bank); Kuppe mit Fels/Hang > 18° in Nähe → *Felsturm* (Hero-Fels aus Teil C, 8–15 m); Kuppe am Weg (< 120 m) in Aue/Elfenwald/Heide/Dschungel → *Ruine* (`AncientRuins` Säulen/Mauerrest, 3–6 Teile, 25–40 % eingegraben); *Wasserfall* nur mit Punkt in `wasser_welt.json["wasserfaelle"]` oder Fluss über Höhenstufe ≥ 8 m auf 30 m (Regel für Teil B/Flüsse, nicht im Planer); *Blumenlichtung* = größte Lichtung ≥ 150 m² im Wald, Weg < 200 m (Planer liefert den Punkt, Blumen-Inseln setzt die Witcher-Ebene); *Totbaum-Solitär* (Sumpf/Ödland/Lava) = Kuppe oder Uferpunkt mit `SM_Dead_Tree_01–03` 1,2-fach.
- Blickziele nie näher als 5 m an Ort/Weg, nie auf Wasser; Wege sollen auf sie zuführen („roads as design tools“, 80.lv/GameBanshee).

Tabelle: dominantes Biom (Nebenbiome), Typvorschlag 1–3 (Reihenfolge = Vorrang; Felsturm/Wasserfall nur bei Wandanteil ≥ 10 % bzw. Wasser ≥ 2 % und Höhe ≥ 150 m), erwartete Mittelschicht-Instanzen (Landfläche × Biom-Dichtesumme × Waldanteil aus Lagen, −70 % je Steilanteil, Deckel 52 000) und Spuren-Auslöser (Ort/Weg/See aus `biome_je_feld`).

| Feld | Biom | Blickziel-Typen | Mittelschicht (Spanne) | Spuren-Auslöser |
|---|---|---|---|---|
| B1 | gletscher (aue) | felsturm, wasserfall | 500–1300 | – |
| C1 | gletscher (fjord) | felsturm, wasserfall | 3200–7500 | – |
| D1 | gletscher (fjord) | felsturm, wasserfall | 2900–6900 | – |
| E1 | gletscher | felsturm, wasserfall | 2700–6300 | – |
| F1 | aue (gletscher) | solitaerbaum, ruine, blumenlichtung | 2400–5600 | – |
| I1 | aue | solitaerbaum, ruine, blumenlichtung | 2700–6400 | – |
| B2 | gletscher (bergwald) | felsturm, wasserfall | 1800–4200 | – |
| C2 | gletscher (fjord, tundra) | felsturm, wasserfall | 7800–18200 | See/Fluss |
| D2 | tundra (gletscher, fjord) | felsturm, steinkreis_ruine, solitaerbaum | 20800–48600 | Ort 2%, Weg |
| E2 | gletscher (frost, tundra) | felsturm, wasserfall | 12700–29600 | Ort 3%, Weg, See/Fluss |
| F2 | aue (frost) | solitaerbaum, ruine, blumenlichtung | 6000–14000 | – |
| G2 | aue (elfenwald) | solitaerbaum, ruine, blumenlichtung | 600–1600 | – |
| H2 | kueste (elfenwald) | felsturm, ruine, solitaerbaum | 5500–13000 | – |
| A3 | bergwald (aue) | wasserfall, ruine | 5000–11700 | – |
| B3 | bergwald | felsturm, wasserfall, ruine | 9000–21100 | Ort 8%, Weg, See/Fluss |
| C3 | aue (tundra, bergwald) | solitaerbaum, ruine, blumenlichtung | 8500–20000 | Ort 6%, Weg, See/Fluss |
| D3 | tundra (canyon, wueste) | steinkreis_ruine, wasserfall, solitaerbaum | 11700–27400 | Ort 5%, Weg, See/Fluss |
| E3 | tundra (wueste, frost) | felsturm, steinkreis_ruine, solitaerbaum | 6700–15800 | Weg, See/Fluss |
| F3 | aue (frost, tundra) | solitaerbaum, ruine, blumenlichtung | 200–500 | – |
| G3 | elfenwald (aue) | blumenlichtung, ruine, solitaerbaum | 26800–52000 | Weg, See/Fluss |
| H3 | elfenwald | felsturm, wasserfall, blumenlichtung | 19800–46300 | Weg, See/Fluss |
| I3 | bergwald (elfenwald) | felsturm, wasserfall, ruine | 6200–14500 | See/Fluss |
| J3 | aue | solitaerbaum, ruine, blumenlichtung | 1700–4000 | – |
| A4 | bergwald (aue) | felsturm, wasserfall, ruine | 7200–16900 | See/Fluss |
| B4 | bergwald | felsturm, wasserfall, ruine | 17400–40700 | Ort 6%, Weg, See/Fluss |
| C4 | aue (canyon, bergwald) | solitaerbaum, ruine, blumenlichtung | 9700–22800 | Ort 13%, Weg, See/Fluss |
| D4 | canyon (wueste, aue) | felsturm, wasserfall, ruine | 3800–8800 | Ort 20%, Weg, See/Fluss |
| E4 | wueste (aue) | felsturm, ruine | 2300–5500 | Ort 10%, Weg, See/Fluss |
| F4 | aue (heide) | solitaerbaum, ruine, blumenlichtung | 15100–35200 | Weg, See/Fluss |
| G4 | elfenwald (heide, aue) | blumenlichtung, ruine, solitaerbaum | 31200–52000 | Weg, See/Fluss |
| H4 | elfenwald (aue, sumpf) | felsturm, wasserfall, blumenlichtung | 28600–52000 | Ort 15%, Weg, See/Fluss |
| I4 | bergwald (elfenwald) | felsturm, wasserfall, ruine | 12200–28400 | Weg, See/Fluss |
| A5 | kueste (bergwald, aue) | felsturm, ruine, solitaerbaum | 3200–7600 | – |
| B5 | bergwald (kueste) | felsturm, wasserfall, ruine | 15100–35300 | Weg, See/Fluss |
| C5 | aue (lava, bergwald) | solitaerbaum, ruine, blumenlichtung | 20800–48600 | Ort 15%, Weg, See/Fluss |
| D5 | aue (oedland) | solitaerbaum, ruine, blumenlichtung | 10900–25600 | Ort 33%, Weg, See/Fluss |
| E5 | aue (oedland) | solitaerbaum, ruine, blumenlichtung | 11600–27000 | Ort 3%, Weg, See/Fluss |
| F5 | heide (aue) | solitaerbaum, steinkreis_ruine, blumenlichtung | 26600–52000 | Weg, See/Fluss |
| G5 | heide (dschungel) | solitaerbaum, steinkreis_ruine, blumenlichtung | 31200–52000 | Weg, See/Fluss |
| H5 | sumpf (dschungel, aue) | totbaum_solitaer, ruine | 29900–52000 | Weg |
| I5 | bergwald (dschungel, sumpf) | ruine | 18000–42100 | Weg |
| J5 | aue | solitaerbaum, ruine, blumenlichtung | 2200–5100 | – |
| A6 | aue | solitaerbaum, ruine, blumenlichtung | 2100–5000 | – |
| B6 | bergwald (aue, lava) | wasserfall, ruine | 16600–38700 | See/Fluss |
| C6 | lava | felsturm, totbaum_solitaer | 7200–16900 | – |
| D6 | oedland (lava, aue) | ruine, wasserfall, totbaum_solitaer | 10700–24900 | See/Fluss |
| E6 | oedland (aue) | ruine, totbaum_solitaer | 9200–21500 | Ort 4%, Weg |
| F6 | aue (oedland) | solitaerbaum, ruine, blumenlichtung | 12100–28300 | See/Fluss |
| G6 | dschungel (aue) | ruine, wasserfall, felsturm | 27200–52000 | Weg, See/Fluss |
| H6 | dschungel | ruine, wasserfall, felsturm | 31200–52000 | Weg, See/Fluss |
| I6 | dschungel | ruine, wasserfall, felsturm | 19600–45800 | Weg, See/Fluss |
| J6 | aue | solitaerbaum, ruine, blumenlichtung | 10000–23500 | – |
| A7 | aue | solitaerbaum, ruine, blumenlichtung | 3200–7600 | – |
| B7 | aue (lava) | solitaerbaum, ruine, blumenlichtung | 6700–15600 | – |
| C7 | lava (aue) | felsturm, totbaum_solitaer | 4400–10400 | – |
| D7 | aue (lava) | solitaerbaum, ruine, blumenlichtung | 6700–15700 | – |
| E7 | oedland (aue) | ruine, totbaum_solitaer | 1900–4500 | Ort 1% |
| F7 | aue (oedland) | solitaerbaum, ruine, blumenlichtung | 5100–12000 | Ort 4% |
| G7 | dschungel (aue) | ruine, felsturm | 2700–6300 | – |
| H7 | dschungel (aue) | ruine | 7200–16800 | See/Fluss |
| I7 | dschungel (aue) | ruine, wasserfall, felsturm | 3500–8300 | – |
| J7 | aue | solitaerbaum, ruine, blumenlichtung | 400–1100 | – |

Die Spannen sind Erwartungswerte aus den Lagenanteilen, nicht aus den Rastern; bei Feldern mit viel Sand (Meeresboden zählt als Land mit Höhe 0) fallen die realen Zahlen niedriger aus, weil `karte_wasser` das Meer ausschließt.

## 5. Testanleitung mit Rauchtest-Ergebnis

**Aufruf lokal** (Windows, production-Wurzel): `python -I scripts\mittelschicht\mittelschicht_plan.py G4 --bild` und `python -I scripts\spuren\spuren_plan.py G4 --bild`; Regeldateien neben die Skripte legen (`scripts/mittelschicht/mittelschicht_regeln.json`, `scripts/spuren/spuren_regeln.json`); `--basis PFAD` für eine andere Wurzel, `--regeln PFAD` für Regelvarianten, `--faktor 0.5` beim ersten Lauf auf Feldern mit voller Witcher-Ebene. Beim Start meldet jeder Planer, wie viele Netzpfade gegen `daten/netze.csv` geprüft wurden; fehlt das Inventar, läuft er mit Hinweis ungeprüft weiter; unbekannte Netze brechen mit Liste ab. Fehlt `hoehe.f32`, Abbruch mit Pfadangabe; fehlende `karte_*.r8`, `lage_*.r8`, `eigner.r8`/`welt.json` oder Baum-Ebenen werden als Hinweis protokolliert (Annahme: keine Fläche / Biom-Fallback je Feld / Beschattung aus Lagen).

**Rauchtest (Cloud, synthetische Produktionswurzel, Raster in voller Größe 7057 × 9577 als memmap, Python 3.13, NumPy 2.5, ohne numba):**

| Lauf | Ergebnis |
|---|---|
| Mittelschicht G4 (932 Buchen in `bestand/G4`, 2 Orte, Weg, See, Fluss, Lagen Laub/Moos, Biome elfenwald/heide/aue) | 56 450 geplant → **52 047 geschrieben**, 936 mit Kollision, 160 Netze/f32-Dateien, **4,3 s**; Ausdünnung Pilz/Ast/Grasbüschel ×0,77 protokolliert; Klassen: Beere 12 154, Grasbüschel 10 526, Strauch 9 076, Jungbaum 6 908, Hochstaude 5 947, Ast 3 230, Farn 2 209, Pilz 1 012, Totholz 581, Stumpf 298, Totbaum 57 |
| Spuren G4 (gleiche Daten) | **6 257 Instanzen**, 1 289 mit Kollision, 10 Akteure (5 Kreuze, 2 Säulen, 2 Karren, 1 Totbaum), 16 Punkte (11 Herd, 2 Meiler, 1 Lagerfeuer, 2 Steg), 28 Flächen (24 Feldstreifen, 1 Obstgarten, 1 Friedhof, 2 Köhlerplätze), 2 Blickziele (Solitärbaum-Kuppe Prominenz 18 m, Blumenlichtung), 53 f32-Dateien, **9,2 s**; Statistik: 125 Zaunsegmente am Weg, 4 Steinmänner, 8 Wegkreuze/Schreine, 1 Karren, 2 Stege, 3 Holzschläge, 2 Köhler, 1 Friedhof, 2 Einzelgräber |
| Determinismus | je Planer zwei Läufe: alle f32-Dateien byte-identisch (MD5) |
| Formatprüfung | alle f32 Vielfache von 40 Byte, Anzahl = `dateien[].anzahl`, Quaternionen normiert, Maßstab > 0; plan.json mit `stand, feld, instanzen, dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision}, ft_ordner, ft_praefix` (+ `akteure, punkte, flaechen, blickziele, orte, hinweis_setzer` bei Spuren); PNG 1008 × 1008 RGB je Planer |
| Budget-Zwangstest Spuren (Regelvariante Deckel 3 000 / 800) | 6 247 → 2 999 Instanzen, 927 → 800 Kollision, Akteure unverändert 10, 8–10 s |
| Baumloses Feld G3, Randfeld A1 (Fenster am Rasterrand geklippt) | Mittelschicht 35 891 / 35 525 Instanzen (Hinweis „keine Baum-Ebene“, Beschattung aus Lagen), Spuren 4 / 0 Instanzen, kein Absturz; Lasttest mit 18 015 Bäumen (Vorlauf): 44 455 Instanzen, 1 666 Kollision, 3,9 s |
| Fehlerpfade | fehlende `hoehe.f32` → „Pflichtdatei fehlt: …“; unbekannter Netzpfad in den Regeln → Abbruch mit Liste |

**Erwartete Zahlen je Feld mit Echtdaten:** Mittelschicht nach Tabelle §4; Wald-Felder (G3, G4, H3, H4, B4, G6, H6, F5, G5, H5) laufen in den Deckel 52 000 und zeigen 10–40 % Ausdünnung von Pilz/Ast/Grasbüschel; Kollision 900–2 500. Spuren: Felder mit Orten (B3, C3–E5, B4, C4, D4, E4, H4, C5, D5, D2, E2, E6, E7, F7) 2 000–12 000 Instanzen (60–80 % Feldfrucht/Stoppeln), 600–2 500 mit Kollision, 5–40 Akteure, 5–40 Rauchpunkte, 5–30 Flächen; Felder mit Weg ohne Ort (G3, H3, F4, G4, I4, B5, F5, G5, H5, I5, G6, H6, I6, E3) 50–600 Instanzen; Felder ohne Ort und Weg 0–50; Stege nur bei See ≥ 2 500 m² mit flachem Ufer (0–3). Laufzeit: Mittelschicht 4–8 s, Spuren 9–20 s je Feld (Cloud 4,3 / 9,2 s auf 1136²-Fenster). Mehr als 60 000 Instanzen, 3 000 Kollision oder 60 s darf nie vorkommen – dann Korrektur melden.

**Prüfkameras** (Unreal-cm, Höhe 170 cm über Boden, 35 mm, Sonne 18–24°):
1. **G4 Waldinneres** – Feldmitte (X ≈ 182 000, Y ≈ −53 000), Blick nach Norden: innerhalb 10 m ≥ 4 Objekte 0,5–3 m (Farninsel, Holunder, Hainbuchen-Schössling, liegender Stamm), nichts im Stamm eines Baumes, Farne/Pilze nur im Schatten.
2. **G4 Waldrand/Lichtung** – Punkt aus `plan.json["blickziele"]` (blumenlichtung), Blick in den Wald: Saum mit 2–3-facher Strauch-/Jungbaumdichte 10–15 m breit, Schösslinge 1–2 m am Lichtungsrand, dahinter dunkler, farnreicher Bestand.
3. **C5 oder D5 Ortsrand** – 80 m vom Ortsmittelpunkt (`plan.json["orte"]`) auf dem Weg, Blick zum Ort: Zaunlauf 20–60 m auf einer Seite, Feldstreifen mit Reihen/Stoppeln, Heuhaufen, Obstgarten-Reihen, Rauch über den Dächern (`punkte`), ein Wegkreuz am Ortsrand.
4. **D2 Tundra-Weg** – auf dem Weg, Blick zur nächsten Kuppe: Steinmann alle 90–140 m neben dem Weg und einer auf der Kuppe, Trockenmauer statt Holzzaun, Zwergkiefern unter 350 m, keine Sträucher darüber.
5. **H5 Sumpf-See** – flaches Seeufer: Fischersteg 8–16 m ins Wasser, Deck 0,6 m über Spiegel, Pfosten im Wasser, Fass/Kiste am Landende; Schilfband 0–6 m, Totbäume 3–6 je ha.

**Erfolgskriterien:** (1) An keiner Kamera ein 10-m-Umkreis ohne Objekt 0,5–3 m. (2) Nichts auf Wasser, Weg (≤ 2,5/4 m), Ort (≤ 5 m), nichts in Stämmen, nichts schwebend oder versunken (Z = bilinear − Eingraben; am Steilhang Stämme längs). (3) Prüfbilder `docs/pruefung/<thema>/<Feld>.png` zeigen Häufung an Saum, Ufer, Lichtungsrand, nicht gleichmäßig (Cloud-Bild G4: Farn-/Totholz-Cluster unter den Kronen, Beerenband in der Heide, Felder und Zäune nur im Ring um die Orte, Stege am See). (4) Nachbarfelder ohne Nahtsprung (Hash aus globaler Rasterkoordinate). (5) Frame-Budget: Mittelschicht-Netze zu 60 % Nanite; Nicht-Nanite-Pflanzen mit Sichtweite ≤ 120–300 m; Schatten für Pilze/Äste/Beeren/Grasbüschel aus (`schatten: false`).

## 6. Einkaufsliste fehlender Assets

| Wunsch | Fab-/Megascans-Name (frei bevorzugt) | Stufe | Wofür |
|---|---|---|---|
| Trockenmauer-Module (gerade, Ecke, Ende, verfallen) | Megascans „Dry Stone Wall“ (Quixel 3D-Asset-Sammlung) oder Fab „Medieval Stone Walls Modular“ | High 4K | ersetzt 130–280 Einzelsteine je Mauer durch 10–20 Module |
| Steinmann/Cairn | Megascans „Stacked Stones / Cairn“ (3 Varianten) | High | Wegmarken Tundra/Fjord/Bergwald |
| Bildstock, Wegkreuz 2 m, Holzschrein | Fab „Medieval Wayside Shrine“ / „Roadside Cross“ (Polish-rural-Pakete) | High | Wegkreuze in Augenhöhe statt 2,4-fach skaliertem Grabkreuz |
| Obstbäume (Apfel, Birne, Kirsche) 4–7 m, Nanite | Megaplant Library „Apple Tree“, „Cherry Tree“ (frei) oder Fab „Fruit Trees Pack“ | High | Obstgärten (heute Hainbuche/Buche/Küsteneiche) |
| Steg-Modul (Deck 4 m, Pfosten, Leiter, Anlegepfahl) | Hivemind „Medieval Docks“ (im Projekt nur Farn/Moos importiert – Docks-Module nachimportieren) | – | Fischerstege, Bootsanleger |
| Meiler/Köhlerhütte | Fab „Charcoal Kiln“ / „Medieval Charcoal Burner“ | Medium | Köhlerplätze (heute Holzstapel-Ring) |
| Vogelscheuche, Bienenkörbe, Heureuter, Wegweiser | Fab „Medieval Farm Props“ (Meshingun Village-Pakete) | Medium | Feldstreifen, Ortsrand |
| Wacholder, Schlehe, Weißdorn, Brombeere (Hecken 1–3 m) | Megascans „Juniper“, Megaplant „Hawthorn/Blackthorn“, Fab „European Shrubs Nanite“ | High | Heide/Tundra/Aue-Saum: heute nur Hasel, Holunder, Ahornbusch, Strandrose |
| Hochstauden (Mädesüß, Weidenröschen, Brennnessel, Beinwell) | Megascans „Fireweed“, „Meadowsweet“, „Nettle“ | High | Aue/Sumpf-Hochstaudenfluren (heute Goldrute/Topinambur/Crownbeard) |
| Jungfichte/Jungkiefer 1–3 m Nanite | Megascans „Norway Spruce Sapling“, Megaplant „Scots Pine young“ | High | Bergwald/Fjord-Schösslinge (heute `SM_Forest_pine_plant` ohne Nanite) |
| Pilzgruppen (Hallimasch, Fliegenpilz, Baumpilz) | Megascans „Mushrooms“ 3D-Plants | Medium | Elfenwald/Sumpf (heute 2 Meadow-Pilze) |
| Tropische Farne/Großblatt-Stauden 1–3 m, Lianen | Megascans „Tropical Fern“, „Banana Plant“, „Liana“ | High | Dschungel-Mittelschicht (heute gemäßigte Farne/Holunder mit Taxonomie-Eignung 0, s. §7) |

## 7. Offene Punkte und Annahmen

1. **Format der Baum-Ebenen:** angenommen `plan.json["dateien"]` mit `rolle: "baum"` (bestand) bzw. Gruppennamen mit Baumart (witcher) und `<Name>.f32` daneben; Houdini `instanzen.json["verzeichnis"][]` mit `klasse` und optional `datei`. Trifft das nicht zu, meldet das Log „keine Baum-Ebene“ und schätzt aus Lagen – dann sind Lichtungen/Holzschlag/Köhler unsicher.
2. **welt.json:** `kacheln` als Liste oder Dict mit `kennzahl`/`id` und `rezept`; Rezepttext wird auf Biomnamen oder „vulkan/lava“ abgebildet, sonst Feld-Fallback (dominantes Biom aus `biome_je_feld`, in beiden Regeldateien hinterlegt).
3. **Yaw-Vorzeichen** in Unreals linkshändigem System: Zufalls-Yaw ist unkritisch, Zäune, Stege, Stämme, Karren verlassen sich auf `yaw = atan2(dY, dX)` und Längsachse = X des Netzes. Beim ersten Setzen prüfen; falls gespiegelt, im Setzer `yaw → −yaw`.
4. **Pivots:** Steg-Pfosten `SM_Beam_4m` und Planken mit Pivot am Fuß/Mitte angenommen; Mauer-/Steinmann-Steine mit Pivot an der Unterkante. Bei Mittelpivots `z_offset`/`eingraben_cm` in den Regeln anpassen.
5. **Seespiegel** = Uferhöhe aus `hoehe.f32` (Steg-Deck +0,6 m); exakter wäre `wasser_welt.json["seen"][].spiegel_cm` – nicht eingebaut, weil die Zuordnung See↔Komponente ohne Echtdaten nicht testbar war.
6. **Landschaftslagen für Felder** schreibt der Planer nicht (nur `flaechen[]` mit `lage_vorschlag`); ein Editor-Schritt zum Malen der Lage in den Rechtecken fehlt.
7. **Doppelung mit Witcher-Ebene** (Gebüsch, Farne, Totholz): vorhandene Instanzen werden als belegt (1,2 m) gelesen, nicht entfernt; kein `entfernen`-Filter. Bei zu dichtem Ergebnis `--faktor 0.6`.
8. **Taxonomie-Abgleich:** 167 von 830 Netz-Biom-Zuordnungen haben Eignung 0 – 113 davon in gletscher/frost/lava/oedland/canyon/wueste/kueste als bewusste Zweitverwertung (Trockengras, Dürräste, Totbäume, Heide), weil die Taxonomie dort keine Mittelschicht kennt; 54 im Dschungel (Megascans-Farne, Holunder, Meadow-Pilze als Füller). Letztere mit B7 abstimmen und nach Einkauf tropischer Stauden ersetzen (Einkaufsliste); bis dahin `dschungel`-Dichten für `farn`/`strauch` ggf. halbieren.
9. **Wüstenfelder** C3–E5 erhalten nur Rooibos/Totholz mit Feldfaktor 0,5; Abstimmung mit B9 nötig.
10. **Kollision der Mauersteine** ist aus (Budget); begehbare Mauern brauchen im Setzer eine Box-Kollision je Mauerlauf. Wird ein Netz in mehreren Gruppen mit unterschiedlicher Kollision genutzt, gilt je Datei die Vereinigung (Kollision an).
11. **Akteur-Dateien** `akteur_<Netz>.f32` folgen der Felsgruppen-Konvention; ein generischer Setzer, der alle `.f32` als Foliage liest, muss `rolle == "akteur"` auslassen.
12. Numba wird nicht genutzt (reiner NumPy-Pfad: 4–10 s je Feld).

## 8. Korrektur Runde 1 (10.10.2026)

Grundlage: `auftraege/verteilung-korrektur-runde1.md` (lokaler Echtdaten-Test 10.10. 15:30) und `antworten/verteilung-KONVENTIONEN.md`.
Gleiche Dateinamen: `skripte/mittelschicht_plan.py`, `mittelschicht_regeln.json`, `spuren_plan.py`, `spuren_regeln.json`.

**Echtdaten-Referenz der Vorfassung** (lokal, Windows, Python 3.11, `plan.json["instanzen"]`):

| Planer | A5 (bergwald/fjord) | G4 (elfenwald) | E1 (gletscher 100 %) | C6 (lava 99 %) |
|---|---|---|---|---|
| mittelschicht | 36 259 | 26 746 | 15 586 | 7 515 |
| spuren | 51 | 591 | 55 | 393 |

Alle unter dem Deckel 60 000; die Zahlen sind die Vergleichsbasis für den nächsten lokalen Lauf (erwartete Verschiebungen unten).

### 8.1 Was geändert wurde (beide Planer)

- **Biom je Zelle strikt nach KONVENTIONEN §1:** `eigner.r8` + `welt.json["kacheln"][k]["rezept"]`; Kennzahl **0 → `aue`**, Rezept mit „vulkan“/„lava“ → `lava`, sonst exakter Biomname oder Teilwort. Nur wenn `eigner.r8` fehlt, gilt das dominante Feldbiom aus `daten/biome_je_feld.json` (Hinweiszeile). Unbekannte Rezepte → dominantes Feldbiom mit `WARNUNG` und Kennzahlenliste (früher stillschweigend Feld-Fallback).
- **Querschnitts-Planer:** `biome_eigen` = alle 15 Biome; Palette und Dichten je Zelle nach Biom (Spuren: Mauer-/Steinmann-/Schrein-Biome, Obstbaum je Biom, Nadel-/Laubstümpfe).
- **Pflichtschlüssel §2 in jedem plan.json:** `biome_fenster` (Anteile aller Biome im Fenster Feld + 64 m, Summe 1), `zellen_zustaendig` (Feldzellen ohne Wasser/Weg/Ort), `biome_eigen`, `kollision_anzahl` (alle Instanzen mit `kollision: true`, bei Spuren einschließlich Akteure), dazu `ebene` (Mittelschicht 1, Spuren 4) auf Plan- und Dateiebene und `entfernen` (leer bzw. aus Overrides).
- **Leerplan:** Landanteil im Fenster < 2 % (oder keine bebaubare Zelle) → `plan.json` mit `instanzen: 0`, `dateien: {}`, alle Pflichtschlüssel, alte f32 gelöscht, eine Logzeile. Kein Textabbruch mehr.
- **Budget §3:** Deckel 60 000 / 3 000 Kollision hart, Ziel Mittelschicht 52 000. Ausdünnung deterministisch per Hash der globalen Rasterzelle in Prioritätsreihenfolge (Mittelschicht: Pilz, Ast, Grasbüschel, Kletter, Beere, Zusatzklassen, Hochstaude … zuletzt Totbaum), bis zu 6 Runden, jede Ausdünnung als `WARNUNG …` im Log und in `hinweise`, bei gedünntem Grasbüschel/Pilz zusätzlich „Landschafts-Gras GT_* dichter stellen“. Spuren zählen Akteure in den Deckel (werden nie gedünnt; Deckel für Foliage = 60 000 − Akteure bzw. 3 000 − Akteure mit Kollision).
- **Kollision je Netz ohne Vereinigung:** Wird ein Netz in Klassen mit und ohne Kollision genutzt (Spuren: Mauerstein = Steinmann-Stein; Mittelschicht: Ast-Netz auch als liegendes Totholz), schreibt der Planer die Nicht-Kollisions-Instanzen in `<Netz>_ohne_koll.f32` (eigener Foliage-Typ). Vorher machte die Vereinigung im Test G4 aus 937 echten 5 210 Kollisions-Instanzen und zwang die Ausdünnung, Trockenmauern lückig zu machen.
- **Spuren: nichts auf Wasser/Weg/Ort** – zentrale Sperre im Instanz-Sammler (Beiwerk um Karren, Stege, Gräber eingeschlossen); einzige Ausnahme sind Steg-Planken/-Pfosten/-Balken/-Geländer über dem Wasser. Verworfene Instanzen werden gezählt (`hinweise`).
- **Kronendach** (beide) zusätzlich aus den Baum-Dateien der Biom-Planer-Ebenen `nordkueste/ aue/ heide_tundra/ hochgebirge/ elfenwald/ sumpf/ dschungel/ lava/ wueste_ergaenzung/` je `<Feld>/` + 8 Nachbarn: Datei zählt als Baum, wenn `dateien[].ebene` bzw. `schicht` mit „2“ beginnt oder „baum“ enthält (ohne `ebene`: Rolle/Gruppe/Name), Totbäume/Stämme/Stümpfe nicht. Mittelschicht markiert außerdem alle Nicht-Boden-Instanzen dieser Ebenen und von `felsgruppen/<Feld>/` im eigenen Feld als belegt (1,2 m); Schicht 0 (Laub, Kiesel) wird ignoriert.
- **Logs nur ASCII:** jede `print`-Ausgabe läuft durch eine Abbildung (ä→ae, ö→oe, ü→ue, ß→ss, →→->, ≤→<=, §→Par., Rest → `?`); `plan.json` bleibt UTF-8. Fehlende Pflichtdatei (`hoehe.f32`, Regeldatei), unbekanntes Feld oder Netzpfade außerhalb des Inventars → `FEHLER: …` und **Exit-Code 2**.

### 8.2 Ebenen-Abgrenzung (KONVENTIONEN §4) in der Mittelschicht

`mittelschicht_plan.py` ist der einzige Planer der generischen Klassen **strauch, jungbaum, farn, totholz_liegend, totholz_stumpf, totholz_ast, hochstaude, grasbueschel, beere, pilz** (Umbenennung totholz/stumpf/ast → totholz_*; alte Namen in Overrides werden weiter verstanden). Eigene Zusatzklassen nur dort, wo kein Biom-Planer dieselbe Form setzt:

| Klasse | bleibt in | entfällt in (Grund) |
|---|---|---|
| schilf | – | aue, sumpf (Schilfgürtel = Sonderform/Schicht 5 der Biom-Planer) |
| totbaum | elfenwald, dschungel | alle übrigen (Biom-Planer setzen Totbäume in Schicht 2) |
| wurzel | elfenwald, dschungel | sumpf, bergwald, fjord (Sonderform sumpf/nordkueste) |
| kletter | elfenwald, sumpf, dschungel | – (Lianen an Stamm/Wand bleiben Sonderform B7) |
| strauch | – | gletscher, frost, lava (Latschen/Krummholz/Kiefernstrauch = Sonderform hochgebirge/lava) |
| beere (heath/heather) | Preisel-/Heidelbeere | heide, tundra (Heidekraut-Flecken = Sonderform heide_tundra), Dichte 0,02/0,012 bzw. 0,02/0,014 |

**Dschungel:** Palette nach `verteilung-dschungel.md` §3 übernommen (Farne Megascans/EagleFern/SilverLady/BeechFern/`SM_Fern_01a/02a`; Strauch nur `SM_Bush_01a` 0,45–0,8 plus Holunder 05/07/08/09 als Bananen-Ersatz 1,5–2,4 über `netze_massstab`, Gewicht Busch 4 : je Holunder 1; Hochstaude Crownbeard 03/04/07/08 + Pestwurz; Jungbaum Palmen 07–12; Totholz/Stumpf/Wurzel Megascans; Kletter Vines + Ivy; Kikuyu-Gras). Die §3-Tabelle (in G6, H6, I6, I7, G7, H7 Farn/Kletter/Totholz/Stumpf/Wurzel/Pilz = 0, Strauch/Jungbaum/Hochstaude × 0,5) steht als `feld_klassen_faktor.dschungel` mit `nur_ohne_override: true` in den Regeln: Sie gilt nur, solange `dschungel_plan.py` diese Klassen selbst setzt. Seit B7 in Runde 1 einen `mittelschicht_overrides`-Block liefert (und nur noch Lianen, Moospolster, Bäume, Boden, Wasserkante setzt), ist sie inaktiv – sonst blieben die Karstfelder ohne Farn und Totholz. B7 kann Karstfelder über `faktor_je_feld` steuern; `entfernen_je_feld` (G6–I7: `sm_fern_01a,sm_fern_02a`) landet im Mittelschicht-`plan.json["entfernen"]`.

**Heide/Tundra:** Zwergstrauch (Preisel-/Heidelbeere) und Grasbüschel kommen nur noch aus der Mittelschicht; `heide_tundra` setzt künftig nur Heidekraut-Flecken und Sonderformen. Bis `heide_tundra_regeln.json` einen Override-Block hat und `grasbueschel`/`wacholder`/`kruepelkiefer`/`jungwuchs`/`totholz`/`stumpf` nicht mehr selbst setzt, doppeln sich diese Klassen in den zehn Heide/Tundra-Feldern.

### 8.3 Override-Schema für die Biom-Planer (`mittelschicht_overrides`)

Der Block steht in `<thema>_regeln.json` des zuständigen Biom-Planers, gesucht im Ordner der Mittelschicht-Regeldatei, sonst in `../<thema>/`. Zuordnung (`mittelschicht_regeln.json["biom_planer"]`): fjord/kueste/bergwald → nordkueste, aue → aue, heide/tundra → heide_tundra, gletscher/frost → hochgebirge, elfenwald → elfenwald, sumpf → sumpf, dschungel → dschungel, lava → lava, wueste/canyon/oedland → wueste_ergaenzung. Fehlende Datei oder fehlender Block → eine Hinweiszeile, Mittelschicht nimmt eigene Werte. **Overrides gewinnen.**

```json
"mittelschicht_overrides": {
  "palette":       {"strauch": ["/Game/…/SM_hazel_01", "…"]},          // ersetzt die Netzliste (Pfade außerhalb netze.csv werden verworfen)
  "faktor":        {"farn": 1.5, "totholz_ast": 0.35, "kletter": 0.0},  // Dichtefaktor, 0 = Klasse aus
  "zusatzklassen": {"adlerfarn": {"netze": ["…"], "dichte": [0.009, 0.002], "gruppe": [8, 25], "radius_m": 5.0}},
  "parameter":     {"farn": {"gruppe": [6, 18], "lichtung": 0.15, "mulde": 1.4}},   // optional: einzelne Klassenschlüssel
  "je_biom":       {"fjord": {"palette": {…}, "faktor": {…}, "vorlage_biom": {"pilz": "bergwald"}}},
  "faktor_je_feld":   {"G6": {"farn": 0.0}},                       // optional, ersetzt den Feldfaktor
  "entfernen_je_feld": {"G6": "sm_fern_01a,sm_fern_02a"}            // optional, → plan.json entfernen
}
```

**Zusatzklassen nach KONVENTIONEN §6** (Nachtrag 14:15 UTC): gelesen wird tolerant sowohl das Mindestschema (`palette` Pflicht; `rolle`, `dichte_je_ha`, `hang_grad`, `hoehe_m`, `wasser_abstand_m`, `lagen_min` 0–255, `kruemmung` konvex/konkav/egal (±0,2 m gegen das 10-m-Mittel), `massstab`, `eingraben_anteil` × Netzhöhe aus `netze.csv`, `gruppe` {groesse, radius_m}, `kollision`, `sichtweite`, `akteur`) als auch das mittelschicht-Klassenformat (dschungel `riesenfarn_insel`/`staudenflur`/`bananen_ersatz`, elfenwald, nordkueste). Rollen mit fels/stein/block/stamm/baum bekommen ohne Angabe Kollision, Eingraben 25–45 % und Kippen 0,8; `akteur: true` → Datei `akteur_<Netz>.f32` mit `rolle: "akteur"`. Zusatzklassen werden **nur in Zellen des liefernden Bioms plus 30-m-Saum** gesetzt (`zusatz_saum_m`, Dichte linear von 1 an der Biomgrenze auf 0); generische Klassen bleiben streng je Zellbiom. Unbekannte Schlüssel (außer Doku-Schlüsseln wie `_doku`, `*hinweis`, `*begruendung`, `herkunft*`) stehen als Logzeile und in `plan.json["overrides"][thema]["unbekannte_schluessel"]`; `plan.json["overrides"]` nennt je Biom-Planer Datei, Biome, gelesene Schlüssel und Zusatzklassen.

Regeln: Reihenfolge je Teil (flacher Block, danach `je_biom[biom]`) zusatzklassen → palette → parameter → faktor → faktor_je_feld. Gesamtfaktor = Feldfaktor × `faktor` × `biom_faktor`. Zusatzklassen brauchen nur die abweichenden Schlüssel (Rest aus `klasse_vorgabe`), optional `biome` (Liste), `biom_faktor` {biom: f}, `lagen` (= `lagen_faktor`), `schatten`, `farbe`. Klassenparameter, die als Dichtefaktoren wirken: `lichtung` (Lichtung), `wegrand` (≤ 8 m vom Weg), `nah_baum` (0,9–3 m um Stämme), `mulde` (≥ 0,4 m unter dem 10-m-Mittel), `an_totholz` (≤ 2 m um gesetztes Totholz, Klasse wird danach geplant). Palette für eine Klasse, die im Biom fehlt: Vorlage aus `vorlage_biom` bzw. dem ersten Biom mit dieser Klasse. Altform `biom_faktor` {biom: f} (wueste_ergaenzung) multipliziert alle Klassen des Bioms. Zusatzklassen ohne Prioritätseintrag stehen im Budget hinter `hochstaude`.

**Stand der Blöcke beim Rauchtest:** aue, dschungel, elfenwald, nordkueste liefern Blöcke im neuen Schema (wurden ohne Änderung gelesen: Dschungel-Zusatzklassen riesenfarn_insel/staudenflur/bananen_ersatz, Elfenwald adlerfarn/grashorst/beere mit wurzel/kletter/totbaum = 0, Nordküste blaubeer_teppich/blume_wald je Biom); sumpf, heide_tundra, hochgebirge, lava ohne Block (eigene Werte, Doppelungsrisiko bis zu deren Korrektur); elfenwald meldet den unbekannten Schlüssel `entfernen_witcher_vorschlag` (wird nicht ausgewertet – bei Bedarf als `entfernen_je_feld` liefern); **wueste_ergaenzung** hat noch die Altform `biom_faktor` wueste/canyon/oedland = 0 – damit setzt die Mittelschicht dort nichts, was §4 widerspricht (B9 sollte auf palette/faktor umstellen oder die Null bewusst bestätigen).

### 8.4 Rauchtest (Cloud, synthetisch, Python 3.13, NumPy, ohne numba)

Synthetische Produktionswurzel (Raster 7057 × 9577 als memmap, nach dem Test gelöscht): **G4** elfenwald 64 % / heide 30 % / Weltgelände 6 % (→ aue), 2 Orte, 2 Wege, See + Fluss, 932 Buchen in `bestand/G4`, Biom-Ebene `elfenwald/G4` mit 600 Bäumen (`ebene "2_baum"`), 900 Adlerfarnen (`1_mittel`), 5 000 Laubhaufen (`0_boden`); **C6** Kachel-Rezept „Vulkanregion_Sued“ 95 %, bergwald 4 % (Randstreifen + Insel im Feld), Weltgelände 1 %, Weg; **A1** nur Meer. Override-Dateien: die aktuellen Regeldateien der neun Biom-Planer aus dem Repository; zusätzlich ein Testblock in `../elfenwald/` (Ordner-Fallback, Fremdpfad im Inventar verworfen, Alias `stumpf`, `faktor_je_feld`).

| Prüfung | Ergebnis |
|---|---|
| Mittelschicht G4 | 54 659 geplant → **51 943** (WARNUNG Instanzbudget, Pilz/Ast/Grasbüschel × 0,84), **1 061 Kollision**, 146 Netze, 5,9 s; Kronendach 1 532 Bäume (bestand + elfenwald), 900 belegt, Laubhaufen ignoriert; Elfenwald-Overrides wirksam (Farn × 1,5, Adlerfarn 4 357, Grashorst 1 185, keine Wurzel/Kletter/Totbaum; Adlerfarn/Grashorst nur im Elfenwald + Saum: 61/50 in Heide-, 34/23 in Aue-Zellen) |
| Mittelschicht C6 (ohne Test-Zusatzklassen) | **8 147**, 191 Kollision, 2,9 s; Lava-Zellen nur Lava-Palette (Beere/Gras/Ast/Totholz) plus 13 blaubeer_teppich aus dem Bergwald-Saum, Bergwald-Zellen Nordküsten-Palette inkl. Zusatzklasse blaubeer_teppich, Weltgelände-Zellen Aue-Palette |
| Spuren G4 / C6 | **23 913** (937 Kollision inkl. Akteure, 14 Akteure, 12 Punkte, 29 Flächen) / **158** (146 Kollision, Steinmänner/Wegkreuze in Lava), 8,6 / 1,9 s |
| A1 (Landanteil 0 %) | beide: leerer `plan.json` mit allen Pflichtschlüsseln, `instanzen 0`, eine Logzeile |
| Pflichtschlüssel | `biome_fenster`, `zellen_zustaendig`, `biome_eigen` (15), `kollision_anzahl`, `ebene`, `entfernen` in allen sechs plan.json; Σ `anzahl` = `instanzen`, Kollisionssumme = `kollision_anzahl`, Quaternionen normiert |
| Wasser/Weg/Ort | **0 Instanzen** auf `karte_wasser/weg/ort > 0` (Mittelschicht alle, Spuren alle außer Steg-Teilen über Wasser) |
| Determinismus | zwei Läufe je Planer (G4, C6, A1): alle f32 byte-identisch (MD5 über alle Dateien) |
| Budget-Zwangstest | Mittelschicht Deckel 10 000 / Ziel 8 000 / Kollision 300: 54 332 → 8 065, Kollision 1 081 → 52; Spuren Deckel 3 000 / 800: 23 899 → 2 978 (154 Kollision, 14 Akteure unverändert); jeweils `WARNUNG` im Log |
| ASCII | 0 Nicht-ASCII-Zeichen in beiden Logs (inkl. Hinweisen mit „§“, „→“, „≥“, Umlauten) |
| Fehlerpfade | fehlende `hoehe.f32`, fehlende Regeldatei, Feld `Z9` → `FEHLER: …`, Exit-Code 2; fehlende `eigner.r8` → dominantes Feldbiom aus `biome_je_feld.json` (G4 → elfenwald) mit Hinweis |
| Zusatzklassen §6 | Test-Override in `lava_regeln.json`: `moospolster_test` (dichte_je_ha 300, hang_grad, hoehe_m, lagen_min Lavafels 60, gruppe {groesse, radius_m}, eingraben_anteil, unbekannter Schlüssel `foo_unbekannt`) → 24 511 Instanzen in Lava-Zellen, 147/27 im 30-m-Saum in Aue/Bergwald, sonst 0; `felsnadel_test` (rolle fels_block, 2/ha, konvex, akteur) → 42 in `akteur_SM_IcelandicBoulder_01.f32`, Kollision an; unbekannter Schlüssel in Log und `plan.json["overrides"]`; Pfad außerhalb des Inventars verworfen mit Hinweis |
| Dschungel-Feldtabelle | G6 ohne B7-Block: Farn/Kletter/Totholz/Stumpf/Wurzel/Pilz 0, Strauch/Jungbaum/Hochstaude 0,5; mit B7-Block: inaktiv (Hinweis), Faktoren aus B7 |
| `py_compile` | beide Skripte sauber |

**Erwartung beim nächsten lokalen Lauf** (gegen die Referenz oben): A5 steigt (Nordküsten-Faktoren Farn × 2,2–2,9, Ast × 1,2–2,1, zwei Zusatzklassen), bleibt aber unter dem Ziel 52 000; G4 steigt wegen Elfenwald-Farninseln/Adlerfarn/Grashorst bis an das Ziel (Ausdünnung mit WARNUNG möglich); E1 sinkt (gletscher ohne Latschen-Strauch und Totbaum); C6 bleibt bei ~7 500. Spuren: Zahlen wie bisher, `kollision_anzahl` jetzt inkl. Akteure; Mauern bleiben vollständig, weil Mauersteine nicht mehr die Steinmann-Kollision erben.

### 8.5 Offen nach Runde 1

1. `spuren_overrides` der Biom-Planer (z. B. Dschungel-Tempelruinen, Wüsten-Karren/Brunnen/Galgen-Ersatz, Hochgebirge-Gipfelkreuz) werden von `spuren_plan.py` noch nicht gelesen. Beim Rauchtest enthielt kein `spuren_overrides`-Block `zusatzklassen` nach §6; die übrigen Blöcke sind themenspezifische Strukturen (je Spurtyp), die einen eigenen Abgleich in Runde 2 brauchen.
2. Biom-Planer ohne Override-Block (aue, sumpf, heide_tundra, hochgebirge, lava) und die Altform von wueste_ergaenzung: Doppelungen bzw. fehlende Mittelschicht, bis sie umgestellt sind (siehe 8.3).
3. Nordküsten-Zusatzklassen nutzen `lagen` – als `lagen_faktor` gelesen (Faktor bei voller Deckung); falls dort anders gemeint, bitte melden.
4. Abgrenzungsliste 8.2 sollte in `verteilung-STATUS.md` übernommen werden (Koordinator).

## Quellen

- FORMAT.md, bildkritik-witcher-messlatte.md, boden-kleinzeug-gras.md, strassen-splines-bruecken.md (Frage 4), assets-taxonomie.md, verteilung-fels-organisch.md (Akteur-Konvention).
- [80.lv – World building of Witcher 3](https://80.lv/articles/world-building-of-witcher-3/); [GameBanshee – Witcher 3 Environment Design Interview](https://www.gamebanshee.com/kwaax), [The World Building of The Witcher 3](https://www.gamebanshee.com/kw3cr); [SpeedTree – Witcher 3 Fallstudie](https://store.speedtree.com/?p=2530); [GDC Europe 2016 – The Living World of The Witcher](https://gdconf.com/news/at-gdc-europe-youll-see-how-the-witchers-living-world-was-built).
- [TechRadar – Witcher-4-Techdemo](https://www.techradar.com/gaming/five-things-we-learned-from-the-witcher-4s-technical-demo), [Seasoned Gaming – State of Unreal 2025](https://seasonedgaming.com/2025/06/03/cd-projekt-red-shows-off-the-witcher-4-at-state-of-unreal/).
- [Naturschutzbund – Waldränder](https://naturschutzbund.at/files/NATUR%20VERBINDET/Waldraender-Gestaltung-Pflege_NL4_17.pdf), [LFI Schweiz – Waldrand-Dichteklassen](https://www.lfi.ch/api/data-catalog/pdf/37), [waldwissen.net – Waldrand](https://www.waldwissen.net/de/lebensraum-wald/naturschutz/artenschutz/waldrand-lebensraum-voller-ueberraschungen).
- [Harms et al. 2004, Biotropica – Sapling density](https://bioone.org/journals/BIOTROPICA/volume-36/issue-1/03200/Variation-in-Small-Sapling-Density-Understory-Cover-and-Resource-Availability/10.1646/03200.full).
