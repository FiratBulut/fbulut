# Leere füllen: Mittelschicht 0,3–3 m und Spuren von Leben (Auftrag 11, Teil D)

**Projekt:** Eldarien, UE 5.8.3, 9,6 × 7 km, 62 Landfelder. **Stand:** 2026-10-10. **Lieferung:** dieser Bericht, `skripte/mittelschicht_regeln.json`, `skripte/mittelschicht_plan.py`, `skripte/spuren_regeln.json`, `skripte/spuren_plan.py`. **Status der Skripte:** `py_compile` sauber, Rauchtest mit synthetischer Produktionswurzel (G4, Randfelder A1/J7, leeres Feld G3, Lasttest 18 015 Bäume) bestanden; **UNGETESTET MIT ECHTDATEN**. Alle 290 verwendeten Netzpfade wurden maschinell gegen `daten/netze.csv` geprüft (0 Fehler). `assets-taxonomie.json` lag zur Palettenwahl noch nicht vor; die Rollen wurden selbst aus Name, Paket und Maßen klassifiziert.

## 1. Befund aus den Bildern: was in 0,5–3 m Höhe fehlt

Gezählt wurde je Bild grob, was innerhalb von ~10 m um die Kamera (≈ 300 m²) zwischen Knie- und Kopfhöhe steht; der Witcher-Richtwert ist aus den drei Zielbildern auf dieselbe Weise geschätzt.

| Bild | Was in 0,5–3 m steht (10-m-Umkreis) | Objekte je 100 m² heute | Witcher-Richtwert (gleiche Zone) |
|---|---|---|---|
| KLEIN12_G3_boden (Buchenwald, Augenhöhe) | 1 roter Strauch, 1 Felsplatte (aufliegend), sonst nur 0,1-m-Sprösslinge in einer Größe; kein Farn, kein Stamm, kein Ast, kein Stumpf, kein Jungbaum | **0,5–0,7** | witcher_03 (Nadelwald, Kovir): Fichtenast als Vordergrund, 3 junge Fichten 1–3 m, 2 liegende Stämme, 1 Wurzelteller, 4 Felsblöcke, Sträucher am Hangfuß → **≈ 4–5** |
| W6FIN_G3_rundgang (Kiefern-Bergwald, Luftbild) | Nur Kronen und roter Boden; zwischen Stämmen keine Sträucher, kein Jungwuchs, keine Totholzlagen; Waldkante hart | **< 0,2** (Mittelschicht praktisch nicht vorhanden) | witcher_07-Logik (Bildkritik §3): Waldsaum aus Büschen und Jungbäumen 30–60 m Falloff; Stämme/Äste 2–3 % |
| W6FIN_E5_rundgang (Küstenwiese, Weiden) | Bäume im 15-m-Raster, Wiese einfarbig, 0 Büsche, 0 Hochstauden, 0 Steine | **0,3** (nur Bäume) | witcher_01 (Flussaue): Sträucher 0,8–1,5 m am Ufer, Hochstauden-Inseln (rote Ähren, 3–8 Stück), Schilf, 6–8 Blöcke, Jungkiefern → **≈ 2,5–3,5** |
| TERR3_I5_rundgang (Küstenhügel) | Kiefern und Birken einzeln, dazwischen leere Trockenwiese, Ufer ohne Gebüsch | **0,3–0,5** | witcher_05 (Dorf): jede Fläche hat 2–3 Objektgrößen (Kisten, Fässer, Karren, Zaun, Markt) → Spuren von Leben **5–8 je 100 m² im Ort**, 1–2 im Umland |

Die Lücke ist also ein Faktor **5–10** in der Mittelschicht (offen: 0,3 → 2,5; Wald: 0,5 → 4–5) und ein Faktor **> 10** bei Spuren von Leben (heute außerhalb der Houdini-Orte 0). Das deckt sich mit Ferats „Leere“: Die Bodenebene (Witcher-Ebene, Kleinzeug) und die Baumebene sind da, die Höhe dazwischen ist leer, und nichts verrät, dass Menschen hier leben.

## 2. Mittelschicht-Regeln 0,3–3 m (alle 15 Biome)

Alle Zahlen stehen in `mittelschicht_regeln.json` (Biom → Klasse → Netzliste, Dichten, Gruppen, Maßstab, Eingraben, Kippen, Sichtweite, Kollision). Hier die Logik und die wichtigsten Werte.

**Lichtverhältnis (Kronendach).** Der Planer liest alle Baumpositionen aus `bestand/<Feld>/`, `witcher/<Feld>/` (plus die 8 Nachbarfelder, nur Instanzen im Fenster) und `instanzen/instanzen.json` (Houdini, Klassen mit „baum“). Jede Krone wird mit Gewicht Maßstab² auf das 1-m-Raster gesplattet, mit Gauß σ = 6 m (3 Box-Durchläufe) geglättet und in eine Deckung `π·4,5²·Dichte` umgerechnet; **Beschattung = 1 − exp(−1,6·Deckung)** (0 = offen, 1 = geschlossen). 100 Bäume/ha ergeben so 0,64, 330 Bäume/ha 0,97. Ohne Baum-Ebene (Hinweis im Log) wird aus `lage_Laub/Nadeln/Moos` geschätzt, gedeckelt bei 0,7. Jede Klasse hat eine Dichte `[offen, beschattet]` je m² und wird linear dazwischen interpoliert: Farne, Pilze, Wurzeln und Kletterpflanzen steigen mit Schatten, Sträucher, Jungbäume und Grasbüschel fallen.

**Waldrand-Saum.** Wald = Beschattung > 0,35; Waldkante = Waldzellen mit Nicht-Wald-Nachbar; Distanz zur Kante per Jump-Flooding. Saumfaktor steigt linear von 1 auf den Klassenwert (Strauch 2,5, Jungbaum 2,0, Beere/Hochstaude 1,5–1,8) innerhalb **15 m nach innen** und **10 m nach außen** (Naturschutzbund: Strauchgürtel 5–10 m, Waldmantel 10–20 m). **Lichtungsränder** (offen, Beschattung < 0,18, < 40 m von der Kante, Kantenabstand ≤ 8 m) bekommen für Jungbäume Faktor 2–3 („Schösslinge an Lichtungsrändern“).

**Feuchte.** `Feuchte = 0,8·max(0, 1 − d_Wasser/40 m) + 1,0·Schlamm + 1,0·Algen + 0,6·Moos + 0,3·Kraut + 0,3·Lehm` (Lagen 0–1), geklippt auf 0–1. Klassen haben `feuchte: [trocken, nass]`-Faktoren: Farn 0,5→1,8 (Elfenwald), Weiden/Holunder in der Aue 0,6→2,5, Schilf nur im Uferband 0–6 m (Zusatzdichte 0,03–0,05/m²).

**Hang, Höhe, Schnee.** Voll bis 22°, linear auf 0 bis zum Klassen-`hang_max` (meist 35°; Kletterpflanzen 90°). Höhe: ab 350 m linear abnehmend, 0 ab 650 m; Klassen haben eigene Obergrenzen (Zwergkiefer 350 m, Krüppelkiefer 300 m). Lage Schnee reduziert auf 25 %, Eis auf 0 (Gletscher/Frost).

**Gruppen.** Farninseln 3–12 (Radius 3 m), Beeren/Heide 4–14 (Radius 2,5–3 m), Hochstauden 3–10, Sträucher 1–4, Jungbäume 1–5, Pilze 3–8 (Radius 1 m), Totholz 1–2. Gruppenzentren werden mit Dichte/Gruppenmittel gestreut, Mitglieder gleichverteilt in der Scheibe; jedes Mitglied wird an seiner Zelle erneut gegen Freiflächenmaske und Dichte > 0 geprüft.

**Dichten (Instanzen je m², offen / beschattet) – Auszug:**

| Biom | Strauch | Jungbaum | Farn | Beere/Heide | Hochstaude | Grasbüschel | Totholz (Koll.) | Stumpf (Koll.) | Ast | Pilz |
|---|---|---|---|---|---|---|---|---|---|---|
| elfenwald | 0,014 / 0,005 | 0,010 / 0,003 | 0,006 / 0,022 | – | 0,008 / 0,010 | 0,012 / 0,002 | 0,0006 / 0,0022 | 0,0003 / 0,0011 | 0,004 / 0,010 | 0,002 / 0,010 |
| bergwald | 0,012 / 0,004 | 0,010 / 0,003 | 0,002 / 0,009 | 0,015 / 0,030 | 0,004 / 0,002 | 0,012 / 0,003 | 0,0004 / 0,0018 | 0,0003 / 0,0010 | 0,004 / 0,012 | 0,001 / 0,006 |
| aue | 0,0045 / 0,002 | 0,0025 / 0,001 | 0,001 / 0,005 | – | 0,012 / 0,004 | 0,016 / 0,004 | 0,0007 / 0,0012 | 0,0004 / 0,0006 | 0,003 / 0,006 | 0,001 / 0,003 |
| heide | 0,004 / 0,002 | 0,003 / 0,001 | – | 0,045 / 0,020 | 0,008 / 0,003 | 0,020 / 0,006 | 0,0005 / 0,0008 | 0,0002 / 0,0005 | 0,006 / 0,005 | 0,002 / 0,003 |
| tundra | 0,0035 / 0,002 | 0,0012 / 0,0006 | – | 0,040 / 0,025 | 0,002 / 0,001 | 0,030 / 0,010 | 0,0003 / 0,0004 | – | 0,004 / 0,003 | – |
| sumpf | 0,008 / 0,004 | 0,002 / 0,0012 | 0,006 / 0,014 | – | 0,012 / 0,010 (+Schilf 0,05 am Ufer) | 0,010 / 0,004 | 0,0015 / 0,0030 | 0,0006 / 0,0015 | 0,004 / 0,006 | 0,003 / 0,008 |
| dschungel | 0,010 / 0,006 | 0,006 / 0,003 | 0,010 / 0,030 | – | 0,012 / 0,015 | 0,010 / 0,004 | 0,0010 / 0,0030 | 0,0003 / 0,0010 | 0,004 / 0,008 | 0,002 / 0,006 |
| kueste / fjord | 0,008 / 0,003 · 0,0065 / 0,003 | 0,004 / 0,0015 | – · 0,002 / 0,006 | 0,010 · 0,020 | 0,006 / 0,003 | 0,016 / 0,005 | 0,0008 / 0,0010 | 0,0002 / 0,0005 | 0,004–0,005 | – |
| gletscher / frost | 0,0012 / 0,0006 | – | – | 0,010 / 0,006 | – | 0,010 / 0,004 | 0,0001 | – | 0,002 | – |
| lava | 0,0010 / 0,0005 | – | – | 0,006 / 0,003 | – | 0,006 / 0,003 (×0,1 auf Lavafels) | 0,0002 | – | 0,003 | – |
| wueste / canyon / oedland | 0,002–0,003 (Rooibos) | – | – | – / – / 0,004 | – | – / 0,006 / 0,008 | 0,0002–0,0004 | – | 0,002–0,004 | – |

Ergebnis für den Blick-Test: Im Elfenwald (Beschattung 0,7) summieren sich Farn + Strauch + Jungbaum + Hochstaude + Totholz auf **≈ 0,044/m² = 4,4 Objekte je 100 m²** in 0,5–3 m (plus Äste/Pilze), im offenen Elfenwald-Saum 0,06, in der Aue offen 0,02–0,035 (mit Hochstauden-Inseln) – also die Witcher-Spanne aus Abschnitt 1. Dazu kommen stehende Totbäume mit 0,5–3 je ha im Wald (Sumpf 3–6 je ha), Wurzelteller 0,5–3 je 1 000 m² nur im 1–2-m-Ring um Stämme, Efeu/Lianen an 8 % (Elfenwald) bzw. 25 % (Dschungel) der Stämme.

**Maßstab, Eingraben, Kippen, Sichtweiten, Kollision.** Maßstab je Klasse 0,7–1,4 (Dschungel-Busch `SM_Bush_01a` 0,45–0,8, weil 3,4 m hoch); Eingraben Pflanzen 2–5 cm, Stümpfe 8–12 cm, liegende Stämme 25–30 cm, Totbäume 15–20 cm; Kippen auf die Normale: Sträucher/Farne 30 %, Jungbäume 10 %, Totbäume 5 %, Totholz/Äste/Wurzeln 100 % (liegen auf dem Hang), Stämme zusätzlich längs zum Gefälle ±20°. Sichtweiten: Pilze 60 m, Kleinzeug/Hochstauden/Beeren/Äste 120 m, Sträucher/Farne/Jungbäume 300 m, Totholz/Stümpfe 450 m, Totbäume 0. **Kollision nur** Totholz liegend, Stümpfe, Totbäume (937–1 666 je Feld im Test, Deckel 3 000 mit automatischer Ausdünnung). Abstände: Kleinzeug 2,5 m, Großes 4 m zum Weg, 5 m zum Ort, 1 m zum Wasser, 0,9 m zu Stämmen (Totbäume 3 m), 1,2 m zu vorhandenen Witcher-/Bestand-Instanzen (werden gelesen und als belegt markiert).

**Budget je Feld.** Ziel 52 000, Deckel 60 000. Überschuss wird gemeinsam-proportional aus den niedrigsten Prioritäten (Pilz, Ast, Grasbüschel, …) gedünnt, höchstens 50 % je Klasse pro Runde; Protokoll im `plan.json["hinweise"]`. Wüstenfelder C3–E5: Feldfaktor 0,5 (nur ergänzen). Rauchtest G4 (synthetisch, 932 Bäume): 56 556 geplant → 52 047 geschrieben, 160 Netze, 3,6–5,5 s; mit 18 015 Bäumen: 44 455 Instanzen, 1 666 mit Kollision, 3,9 s.

**Witcher-Belege (Suchauszüge).** CDPR nutzte ~20 Baum-/Straucharten mit je 5–12 Modellen, 40 Grasarten, Biom-spezifische Pinsel (80.lv „World building of Witcher 3“, GameBanshee-Interview); SpeedTree zählt ~200 Pflanzentypen (SpeedTree-Fallstudie). Die Witcher-4-Demo setzt Kleinzeug und Gras per Runtime-GPU-PCG plus Nanite (boden-kleinzeug-gras.md, DF-Interview Örtegren). Für die Dichte selbst gibt keine Quelle Zahlen; die Werte oben sind aus den Zielbildern abgezählt und mit Ökologie-Spannen plausibilisiert: Jungwuchs 0,7–7,5/m² in Naturwäldern (Harms et al. 2004, Biotropica) liegt weit über unseren 0,003–0,01, weil wir nur sichtbare 0,3–3-m-Exemplare setzen; Strauchgürtel 5–10 m / Waldmantel 10–20 m (Naturschutzbund-Heft „Waldränder“, LFI Schweiz: Waldrand-Dichteklassen 0–25 % bis 76–100 %).

## 3. Spuren von Leben (spuren_plan.py)

**Orte** werden aus `karte_ort.r8` abgeleitet: Maske auf 4-m-Raster, Zusammenhangskomponenten per Min-Label-Ausbreitung (vektorisiert), je Komponente Mittelpunkt, Fläche, Radius = √(A/π), Biom am Mittelpunkt; ≥ 400 m² gilt als Ort, kleiner als Einzelbauwerk (nur Rauch mit 50 %). **Wege**: Distanzfeld mit Seed-Rückgabe liefert je Zelle Abstand, Normale zum Weg und Tangente – damit stehen Zäune, Karren, Kreuze parallel bzw. frontal zum Weg. **Seen**: Wasserkomponenten ≥ 2 500 m² und ≥ 15 m breit (Distanz zum Land), Uferzellen 1–2 m vom Wasser, Hang ≤ 7°, Tiefe 6 m vom Ufer 0,3–1,6 m (bilinear aus `hoehe.f32`) = flaches Ufer.

| Spur | Regel (Zahlen in `spuren_regeln.json`) | Netze im Inventar | Ausgabe |
|---|---|---|---|
| **Feldstreifen** | Ring 30–150 m um Orte, Raster 36 m, 55 % der Zellen, Rechtecke 20–60 × 20–60 m, Ausrichtung = Wegtangente (Weg < 80 m) sonst Höhenlinie, 2. Versuch um 90° und 0,7/0,5-fach; Hang ≤ 8°, Beschattung ≤ 0,3, Weg > 6 m; max 12 je Ort, 30 je Feld; 35 % mit Feldfrucht-Reihen (1,2 m × 0,9 m), sonst Stoppel-Flecken 0,08/m²; 0–3 Heuhaufen | Zaun `SM_fenceA/D/E_a1` (3,29 m, 15 % Lücken, ±6° Kippen), Frucht `SM_flower_sunroot_01/02` (Topinambur-Optik, 0,6–0,9 skaliert), Stoppel `SM_dead_grass_01/02`, Heu `SM_Hay_Pile`, `SM_StrawPile_01a`, `SM_Hay_02` | Zaun/Pflanzen als Foliage; Rechteck als `flaechen[]` mit `lage_vorschlag` Erde/Lehm zum Malen der Landschaftslage |
| **Trockenmauern** | In Stein-Biomen (fjord, kueste, bergwald, heide, tundra, gletscher, frost) statt Holzzaun: Steine alle 0,45 m, 3 Lagen (0 / 0,28 / 0,52 m, Anteil 100/85/50 %), Versatz ½ Stein je Lage, Jitter ±12 cm, Basis 8 cm eingegraben, Maßstab 0,8–1,2 | `SM_mountain_rock_small_01_1/2/4/5`, `SM_s_rock_01–03`, `SM_stones_01_1/4/5`, Moosstein `SM_MossyForestRock_01` | Foliage ohne Kollision (Budget) |
| **Obstgarten** | 1 je Ort mit Radius ≥ 35 m, Ring 20–90 m, 30–50 × 24–40 m, Reihen 7 m, Abstand 6 m, Jitter ±0,6 m, Maßstab 0,7–1,0, wird **vor** den Feldstreifen gesetzt | Ersatz-Obstbäume je Biom: `SM_EuropeanHornbeam_Forest_09/10` (5–6,7 m, Nanite), `SM_beech_tree_00_B/C/D`, Küste `SM_dry_oak_02_C/D`, Nadelbiome `SM_pine_beach_small_01/02`, Dschungel `SM_Palm_01_06–08_G` | Foliage mit Kollision, `flaechen[]` Typ obstgarten |
| **Zaun am Weg** | 1–3 Läufe je Ort, Wegabstand 3,5 m, Ortsrand 10–70 m, Länge 20–60 m, 20 % Lücken, nur eine Wegseite (Vorzeichen der Normalen am Ortsmittelpunkt) | Holzzaun + `SM_Fence_01` (Town); Stein-Biome: Mauerstücke | Foliage |
| **Steinmänner** | a) Wegmarken in Stein-Biomen alle 90–140 m (3–6 m neben dem Weg, 80 %); b) Kuppen (lokales Maximum 90 m, Prominenz ≥ 12 m); c) frei 6 je km² (Weg > 20 m, Ort > 60 m, Hang < 25°). 5–9 Steine, Basis 1,5–2,2-fach, Abnahme 0,82 je Stein, Höhenversatz 0,24 m·Maßstab, Versatz 6 cm·√k | `SM_mountain_rock_small_01_*`, `SM_s_rock_01/02`, `SM_NordicBeachRock_01` | Foliage mit Kollision (21 Steine im Test) |
| **Wegkreuze / Schreine** | Wegband 3–5 m, 1 je 220-m-Raster, Score = Zufall + 2 (Kuppe ≤ 10 m) + 2 (Furt: Wasser 2–15 m) + 1 (Ortsrand 40–90 m), Schwelle 0,35; Front zum Weg; in elfenwald/dschungel/aue/sumpf 40 % Schrein | Kreuz `SM_Cross` (0,81 m → Maßstab 2,2–2,6 = 1,8–2,1 m, ±5° schief) auf 3 Steinen; Schrein = `SM_Column_03` (×0,6 = 1,9 m) + `SM_Lamp` + 2 Sträucher (`SM_Elderberry_06/07`, `SM_hazel_02`) | Kreuz/Säule als `akteure` (rolle akteur) + f32 |
| **Verlassene Karren** | Wegband 2–5 m, 1,6 je km Weg (Raster 390 m, 65 %), Ort > 120 m, Yaw = Tangente ±15°, Roll 4–14°, 1–3 Beiwerk (Fass, Kiste, Rad, Sack) in 1,4–3 m | `SM_cartB_a1`, `SM_BrokenWoodWagon` (Nanite), 20 % `SM_Carriage_01a` (schwer, 25 Kollisionsprimitive) | Karren als `akteure` |
| **Fischerstege** | flache Seeufer wie oben, See-Ortsnähe (Ort ≤ 400 m oder Weg ≤ 80 m), max 3 je Feld, 2–4 Segmente à 4 m, 4 Planken à 0,31 m, Deck 0,6 m über Wasserspiegel (= Uferhöhe), 2 Pfosten je Segment (3,8 m eingesenkt), Längsbalken, 1 Geländer am Ende, 1–2 Fässer/Kisten/Trog am Landende | `SM_PlankThin_4m_01a`, `SM_Plank_4m_01a`, `SM_Beam_4m` (vertikal), `SM_Rail_3m`, `SM_Trough_01a` | Foliage mit Kollision; Steg-Achse als `punkte[typ=steg]` (x, y, z, yaw, Länge) |
| **Holzschlag-Lichtungen** | Lichtung ≥ 150 m² im Wald (Waldanteil im 60-m-Fenster > 0,3), Weg 8–180 m, Ort > 60 m, max 3 je Feld, Radius 12–22 m: Stümpfe 0,045/m², Äste 0,03/m², 2–5 liegende Stämme mit gemeinsamer Richtung ±20°, 1–2 Stapel, 30 % Karren, 30 % Lagerfeuer (5 Steine + Rauchpunkt) | Stümpfe nach Biom (Nadel: `SM_pine_stump_01–03`, `SM_TreeStump_01`; Laub: `SM_BirchTreeStump_01`, `SM_BrokenStump_01`, `SM_stump_03`, `SM_Tree_Stump_02`), Stämme `SM_Forest_Pine_09/04/08_log` (4,5–5,6 m), `SM_LargeFallenTree_02`, Stapel `SM_Pile_WoodLog_02a`, `SM_firewoodSetA_a1` | Foliage (Stümpfe/Stämme Kollision) |
| **Köhlerplätze** | Beschattung 0,3–0,75, Hang ≤ 6°, Weg 40–220 m, Ort > 80 m, kein Stamm im 7-m-Umkreis, max 2 je Feld: Meiler = 6 Holzstapel im Ring r 3,2 m tangential + 2. Ring 0,55 r um 0,9 m erhöht, 10 Stümpfe 10–18 m, Feuerholz/Fass/Kiste | `SM_Pile_WoodLog_02a`, `SM_firewoodSetA_a1`, `SM_barrelClosedA_a1`, `SM_crateA_a1` | Rauchpunkt `meiler` (Stärke 0,6), `flaechen[]` Kreis r 7 m Lage Erde |
| **Gräber** | Friedhof je Ort mit Radius ≥ 25 m: 12 × 18 m im Ring 8–30 m, Reihen 1,6–2,2 m, 70 % belegt, Kreuze 0,9–1,3, ±8° schief, Umfriedung Mauer/Zaun, 60 % ein Totbaum; Einzelgräber 0,7 je km Weg (4–8 m vom Weg, Ort > 100 m): Kreuz + 3 Steine + 1 Ast | `SM_Cross`, `SM_DeadTree_01/02`, `SM_EuropeanBeech_Dead_M_01` | Friedhof als `flaechen[]`, Totbaum als Akteur |
| **Rauchsäulen** | je Ort `clip(Fläche/1000·1,2, 1, 10)` Punkte in Ortszellen (30-m-Raster), 2,5 m über Boden, Stärke 0,5–1,0; Meiler 0,6; Lagerfeuer 0,3 | – (Partikel) | `punkte[]` mit typ herd/meiler/lagerfeuer, x/y/z cm, staerke |

Rauchtest G4 (synthetisch, 2 Orte, 1 Weg, 1 See, 1 Fluss): 24 Feldstreifen, 1 Obstgarten, 125 Zaunsegmente am Weg, 4 Steinmänner, 8 Wegkreuze/Schreine, 1 Karren, 2 Stege, 3 Holzschläge, 2 Köhler, 1 Friedhof, 2 Einzelgräber, 16 Rauch-/Stegpunkte, 10 Akteure; 6 257 Instanzen, 1 330 mit Kollision, 9,0 s.

**Was im Inventar fehlt (Spuren):** kein Steinmauer-Modul (wird aus Einzelsteinen gebaut, 2,2 Steine je Meter → 130–280 Instanzen je Mauer), kein Steinmann-Netz, kein Wegkreuz in Mannshöhe (Grabkreuz wird 2,4-fach skaliert; Texel-Dichte sinkt), kein Schrein/Bildstock, keine echten Obstbäume, kein Steg-Modul, kein Meiler, kein Brunnen außer dem orientalischen `SM_Well_02a` (Bazaar – nicht verwendet), keine Vogelscheuche, keine Bienenkörbe, kein Galgen/Wegweiser. Siehe Einkaufsliste.

## 4. Blickziele je Landfeld

**Koordinatenregel (im Planer umgesetzt, Ausgabe `plan.json["blickziele"]`):**
- **Kuppe** = Zelle ist lokales Maximum im 150-m-Fenster (exakter gleitender Max-Filter) **und** Prominenz (Höhe − 150-m-Mittel) ≥ 15 m **und** Hang ≤ 18°; Score = Prominenz + 20·Sichtbarkeit (Anteil tiefer liegender Umgebung) + 5 (Weg < 150 m); je 200-m-Raster ein Kandidat, die 3 besten je Feld.
- **Typ nach Biom** (Tabelle `blickziele.typ_je_biom`): Kuppe im Offenland mit Beschattung ≤ 0,15 → *Solitärbaum* (ein alter Baum 1,3–1,5-fach, Felsblock, Bank aus Stamm); Kuppe mit Fels/Hang > 18° in Nähe → *Felsturm* (Hero-Fels aus Teil C, 8–15 m); Kuppe am Weg (< 120 m) in Aue/Elfenwald/Heide/Dschungel → *Ruine* (`AncientRuins` Säulen/Mauerrest, 3–6 Teile, 25–40 % eingegraben); *Wasserfall* nur, wenn `wasser_welt.json["wasserfaelle"]` einen Punkt im Feld hat oder Fluss über Höhenstufe ≥ 8 m auf 30 m läuft (nicht im Planer, Regel für Teil B/Flüsse); *Blumenlichtung* = größte Lichtung ≥ 150 m² im Wald, Weg < 200 m (Planer liefert den Punkt; Blumen-Inseln setzt die Witcher-Ebene); *Totbaum-Solitär* (Sumpf/Ödland/Lava) = Kuppe oder Uferpunkt mit `SM_Dead_Tree_01–03` 1,2-fach.
- Blickziele stehen nie näher als 5 m an Ort/Weg, nie auf Wasser; Wege sollten laut Witcher-Praxis auf sie zuführen („roads as design tools“, GameBanshee/80.lv).

Tabelle: dominantes Biom (Nebenbiome), Typvorschlag 1–3 (Reihenfolge = Vorrang; Felsturm/Wasserfall nur bei Wandanteil ≥ 10 % bzw. Wasser ≥ 2 % und Höhe ≥ 150 m), erwartete Mittelschicht-Instanzen (Spanne aus Landfläche × Biom-Dichtesumme × Waldanteil aus Lagen, −70 % je Steilanteil, Deckel 52 000) und ob Spuren zu erwarten sind (Ort/Weg/See aus `biome_je_feld`).

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

Die Spannen sind Erwartungswerte aus den Lagenanteilen der Tabelle, nicht aus den Rastern; bei Feldern mit viel Sand (Meeresboden zählt als Land mit Höhe 0) fallen die realen Zahlen niedriger aus, weil `karte_wasser` das Meer ausschließt.

## 5. Testanleitung

**Aufruf lokal** (Windows, production-Wurzel): `python -I scripts\mittelschicht\mittelschicht_plan.py G4 --bild` und `python -I scripts\spuren\spuren_plan.py G4 --bild`; die Regeldateien neben die Skripte legen (`scripts/mittelschicht/mittelschicht_regeln.json`, `scripts/spuren/spuren_regeln.json`). Erster Lauf mit `--faktor 0.5`, wenn das Feld schon eine volle Witcher-Ebene trägt.

**Erwartete Zahlen je Feld (Spanne):**
- Mittelschicht: Tabelle §4; Wald-Felder (G3, G4, H3, H4, B4, G6, H6, F5, G5, H5) laufen in den Deckel 52 000 und zeigen im Log eine Ausdünnung von Pilz/Ast/Grasbüschel um 10–40 %; Kollision 900–2 500. Mehr als 60 000 oder mehr als 3 000 Kollision darf nie vorkommen (dann Korrektur melden).
- Spuren: Felder mit Orten (B3, C3–E5, B4, C4, D4, E4, H4, C5, D5, D2, E2, E6, E7, F7): 2 000–12 000 Instanzen (davon 60–80 % Feldfrucht/Stoppeln), 600–2 500 mit Kollision, 5–40 Akteure, 5–40 Rauchpunkte, 5–30 Flächen; Felder ohne Ort, mit Weg (G3, H3, F4, G4, I4, B5, F5, G5, H5, I5, G6, H6, I6, E3): 50–600 Instanzen (Steinmänner, Kreuze, Karren, Einzelgräber, Holzschlag, Köhler); Felder ohne Ort und Weg: 0–50. Stege nur in Feldern mit See ≥ 2 500 m² und flachem Ufer (0–3).
- Laufzeit: Mittelschicht 4–8 s, Spuren 9–20 s je Feld (Cloud-Messung 3,6–5,5 s / 8,3–9,3 s auf 1136² Fenster; Windows-PC ähnlich). Über 60 s → Korrektur.

**Prüfkameras** (Position in Unreal-cm, Höhe 170 cm über Boden, Brennweite 35 mm, Sonne 18–24°):
1. **G4 Waldinneres** – Mitte des Feldes (X ≈ 182 000, Y ≈ −53 000), Blick nach Norden: innerhalb 10 m müssen ≥ 4 Objekte 0,5–3 m stehen (Farninsel, Holunder, Hainbuchen-Schössling, ein liegender Stamm), kein Objekt im Stamm eines Baumes, Farne und Pilze nur im Schatten.
2. **G4 Waldrand/Lichtung** – ein Punkt aus `plan.json["blickziele"]` (Typ blumenlichtung), Blick in den Wald: Saum mit 2–3-facher Strauch-/Jungbaumdichte 10–15 m breit, Schösslinge 1–2 m am Lichtungsrand, dahinter dunkler, farnreicher Bestand.
3. **C5 oder D5 Ortsrand** – 80 m vom Ortsmittelpunkt (aus `plan.json["orte"]`) auf dem Weg stehend, Blick zum Ort: Zaunlauf 20–60 m auf einer Seite, Feldstreifen mit Reihen/Stoppeln, Heuhaufen, Obstgarten-Reihen, Rauch über den Dächern (Partikel an `punkte`), ein Wegkreuz am Ortsrand.
4. **D2 Tundra-Weg** – auf dem Weg, Blick zur nächsten Kuppe: Steinmann alle 90–140 m neben dem Weg und einer auf der Kuppe, Trockenmauer statt Holzzaun, Zwergkiefern-Gruppen unter 350 m, keine Sträucher über 350 m.
5. **H5 Sumpf-See** – flaches Seeufer: Fischersteg 8–16 m ins Wasser, Deck 0,6 m über Spiegel, Pfosten im Wasser, Fass/Kiste am Landende; Schilf-/Rohrkolben-Band 0–6 m, Totbäume 3–6 je ha.

**Erfolgskriterien:** (1) An keiner der 5 Kameras ein 10-m-Umkreis ohne Objekt 0,5–3 m (Witcher-Regel). (2) Nichts auf Wasser, Weg (≤ 2,5/4 m), Ort (≤ 5 m), nichts in Stämmen, keine schwebenden oder versunkenen Instanzen (Z = bilinear − Eingraben; bei Steilhang Stämme längs). (3) Prüfbilder `docs/pruefung/<thema>/<Feld>.png` zeigen Instanzen gehäuft an Saum, Ufer, Lichtungsrand, nicht gleichmäßig. (4) Nachbarfelder ohne Nahtsprung (Hash aus globaler Rasterkoordinate; Cloud-Test: zwei Läufe byte-identisch). (5) Frame-Budget: Mittelschicht-Netze sind zu 60 % Nanite; nicht-Nanite-Pflanzen (Forest/Meadow/Mountain-Sets, Masked) mit Sichtweite ≤ 120–300 m; Schatten für Pilze/Äste/Beeren/Grasbüschel aus (`schatten: false` im plan.json).

## 6. Einkaufsliste fehlender Assets

| Wunsch | Fab-/Megascans-Name (frei bevorzugt) | Stufe | Wofür |
|---|---|---|---|
| Trockenmauer-Module (gerade, Ecke, Ende, verfallen) | Megascans „Dry Stone Wall“ (Quixel, 3D-Asset-Sammlung, ab 0,99 USD je Asset) oder Fab „Medieval Stone Walls Modular“ | High 4K | ersetzt die 130–280 Einzelsteine je Mauer durch 10–20 Module |
| Steinmann/Cairn | Megascans „Stacked Stones / Cairn“ (3 Varianten) | High | Wegmarken Tundra/Fjord/Bergwald |
| Bildstock, Wegkreuz 2 m, Holzschrein | Fab „Medieval Wayside Shrine“ / „Roadside Cross“ (Polish-rural-Pakete) | High | Wegkreuze in Augenhöhe mit passender Texeldichte statt 2,4-fach skaliertem Grabkreuz |
| Obstbäume (Apfel, Birne, Kirsche) 4–7 m, Nanite | Megaplant Library „Apple Tree“, „Cherry Tree“ (frei, PVE-Bäume), oder Fab „Fruit Trees Pack“ | High | Obstgärten (heute Hainbuche/Buche/Küsteneiche als Ersatz) |
| Steg-Modul (Deck 4 m, Pfosten, Leiter, Anlegepfahl) | Hivemind „Medieval Docks“ (bereits teilweise im Projekt – nur Farn/Moos importiert): Docks-Module nachimportieren | – | Fischerstege, Bootsanleger |
| Meiler/Köhlerhütte, Köhlerhaufen mit Erde | Fab „Charcoal Kiln“ / „Medieval Charcoal Burner“ | Medium | Köhlerplätze (heute Holzstapel-Ring) |
| Vogelscheuche, Bienenkörbe, Heureuter, Wegweiser | Fab „Medieval Farm Props“ (Meshingun Village-Pakete) | Medium | Feldstreifen, Ortsrand |
| Wacholder, Schlehe, Weißdorn, Brombeere (Heckensträucher 1–3 m) | Megascans „Juniper“, Megaplant „Hawthorn/Blackthorn“, Fab „European Shrubs Nanite“ | High | Heide/Tundra/Aue-Saum: heute nur Hasel, Holunder, Ahornbusch, Strandrose |
| Hochstauden Mitteleuropa (Mädesüß, Weidenröschen, Brennnessel groß, Beinwell) | Megascans „Fireweed“, „Meadowsweet“, „Nettle“ (3D-Plants) | High | Aue/Sumpf-Hochstaudenfluren (heute Goldrute/Topinambur/Crownbeard) |
| Jungfichte/Jungkiefer 1–3 m Nanite | Megascans „Norway Spruce Sapling“, Megaplant „Scots Pine young“ | High | Bergwald/Fjord-Schösslinge (heute `SM_Forest_pine_plant` ohne Nanite) |
| Pilzgruppen (Hallimasch, Fliegenpilz, Baumpilz) | Megascans „Mushrooms“ 3D-Plants | Medium | Elfenwald/Sumpf (heute 2 Meadow-Pilze) |

## 7. Offene Punkte und Annahmen

1. **Format der Baum-Ebenen:** angenommen `plan.json["dateien"]` mit `rolle: "baum"` (bestand) bzw. Gruppennamen mit Baumart (witcher) und `<Name>.f32` daneben; Houdini `instanzen.json["verzeichnis"][]` mit `klasse` und optional `datei`, sonst `<name>.f32`. Trifft das nicht zu, meldet das Log „keine Baum-Ebene“ und schätzt aus Lagen – dann sind Lichtungen/Holzschlag/Köhler unsicher.
2. **welt.json-Struktur:** `kacheln` als Liste oder Dict mit `kennzahl`/`id` und `rezept`; Rezepttext wird auf Biomnamen oder „vulkan/lava“ abgebildet, sonst Feld-Fallback (dominantes Biom aus `biome_je_feld`, in den Regeln hinterlegt).
3. **Quaternionen/Yaw-Vorzeichen** in Unreals linkshändigem System: Zufalls-Yaw ist unkritisch, aber Zäune, Stege, Stämme und Karren verlassen sich auf `yaw = atan2(dY, dX)` und Längsachse = X des Netzes. Beim ersten Setzen prüfen; falls gespiegelt, im Setzer `yaw → −yaw`.
4. **Pivot der Netze:** Steg-Pfosten `SM_Beam_4m` und Planken werden mit Pivot am Fuß/Mitte angenommen; Mauersteine/Steinmann-Steine mit Pivot an der Unterkante. Bei Mittelpivots `z_offset`/`eingraben_cm` in den Regeln anpassen.
5. **Wasserspiegel von Seen** = Uferhöhe aus `hoehe.f32` (Steg-Deck +0,6 m); exakter wäre `wasser_welt.json["seen"][].spiegel_cm` – nicht eingebaut, weil die Zuordnung See↔Komponente ohne Echtdaten nicht testbar war.
6. **Landschaftslagen für Felder** schreibt der Planer nicht (nur `flaechen[]` mit `lage_vorschlag`); ein kleiner Editor-Schritt (Landscape-Layer malen in den Rechtecken) fehlt noch.
7. **Doppelung mit Witcher-Ebene** (Gebüsch, Farne, Totholz): vorhandene Instanzen werden als belegt (1,2 m) gelesen, nicht entfernt; `entfernen`-Filter bewusst nicht gesetzt. Bei zu dichtem Ergebnis `--faktor 0.6`.
8. **Wüstenfelder** erhalten nur Rooibos/Totholz mit Faktor 0,5; Abstimmung mit B9 nötig.
9. **Kollision der Mauersteine** ist aus (Budget); begehbare Mauern brauchen im Setzer eine einfache Box-Kollision je Mauerlauf.
10. Numba wird nicht genutzt (reiner NumPy-Pfad reicht: 4–9 s je Feld).

## Quellen

- FORMAT.md, bildkritik-witcher-messlatte.md, boden-kleinzeug-gras.md, strassen-splines-bruecken.md (Frage 4), ANALYSE_WITCHER_2026-10-08.md.
- [80.lv – World building of Witcher 3](https://80.lv/articles/world-building-of-witcher-3/) (Biom-Pinsel, Artenzahl, Wege als Führung).
- [GameBanshee – Witcher 3 Environment Design Interview](https://www.gamebanshee.com/kwaax), [The World Building of The Witcher 3](https://www.gamebanshee.com/kw3cr) (Orte nach Einwohnerzahl, keine Rasterplatzierung, Points of Interest).
- [SpeedTree – Witcher 3 Fallstudie](https://store.speedtree.com/?p=2530) (~200 Pflanzentypen).
- [GDC Europe 2016 – The Living World of The Witcher](https://gdconf.com/news/at-gdc-europe-youll-see-how-the-witchers-living-world-was-built) (Ankündigung).
- [TechRadar – Witcher-4-Techdemo](https://www.techradar.com/gaming/five-things-we-learned-from-the-witcher-4s-technical-demo), [Seasoned Gaming – State of Unreal 2025](https://seasonedgaming.com/2025/06/03/cd-projekt-red-shows-off-the-witcher-4-at-state-of-unreal/) (Nanite Foliage, PS5 60 fps).
- [Naturschutzbund – Waldränder: Gestaltung und Pflege](https://naturschutzbund.at/files/NATUR%20VERBINDET/Waldraender-Gestaltung-Pflege_NL4_17.pdf) (Strauchgürtel 5–10 m, Waldmantel 10–20 m), [LFI Schweiz – Waldrand-Dichteklassen](https://www.lfi.ch/api/data-catalog/pdf/37), [waldwissen.net – Waldrand](https://www.waldwissen.net/de/lebensraum-wald/naturschutz/artenschutz/waldrand-lebensraum-voller-ueberraschungen).
- [Harms et al. 2004, Biotropica – Sapling density](https://bioone.org/journals/BIOTROPICA/volume-36/issue-1/03200/Variation-in-Small-Sapling-Density-Understory-Cover-and-Resource-Availability/10.1646/03200.full) (0,7–7,5 Jungpflanzen/m²).
