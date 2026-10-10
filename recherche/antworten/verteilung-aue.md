# Verteilung Biomgruppe 2: Aue/Flussauen (Velen, Weißgarten, Kovir)

**Auftrag 11, Teil B2.** Biom `aue`, Foliage-Präfix `FT_EL_AU_`, Ordner `/Game/Eldarien/Welt/Foliage/Aue`. Stand 2026-10-10.
Lieferung: dieser Bericht, `skripte/aue_regeln.json` (25 Klassen, 211 Netzpfade, alle gegen `netze.csv` geprüft),
`skripte/aue_plan.py` (Planer, FORMAT §3/§5). **Alles UNGETESTET MIT ECHTDATEN** – in der Cloud nur mit synthetischen
Rastern (E5, siehe §4) rauchgetestet. Web-Quellen konnten nur als Suchmaschinen-Auszüge gelesen werden (80.lv, GDC Vault,
Fab waren per Proxy nicht erreichbar); solche Belege sind mit **[Suchauszug]** markiert, Zahlen ohne Beleg mit **Richtwert**.

Betroffene Felder (aue dominant): F1, I1, F2, G2, F3, J3, C4, C5, D5, E5, J5, A6, F6, J6, A7, B7, D7, F7, J7; Aue-Anteile in
F4, F5, H5, E7 (und kleiner in C3, B6, D6, C7, G7–I7, E4, D4, H4, A5). Der Planer läuft in jedem Feld nur auf Zellen mit Biom
`aue` (`eigner.r8` + `welt.json`, Kennzahl 0 = aue laut FORMAT §2), in den Wüstenfeldern C4, D5, E5 (und C3/D3/D4/E3/E4) zusätzlich
nur außerhalb Sand/Sandstein ≥ 0,5 und mit Faktor 0,6.

## 1. Witcher-Analyse: Was Velen, Weißgarten und die Kovir-Auen zwischen Boden und Krone füllt

**Schichten.** Die Zielbilder (witcher_01: Flussaue mit Ruine; witcher_03: Waldpfad mit Bach; witcher_05: Dorfplatz) und die
Beschreibungen in `ANALYSE_WITCHER_2026-10-08.md` zeigen in der Aue durchgehend vier Höhenbänder, die sich gegenseitig verdecken:
(a) Boden 0–0,3 m: Laub, Zweige, Kiesel, Pilze, Klee, Moos auf Steinen; (b) 0,3–1,5 m: hohes Gras knie- bis hüfthoch in 3–5 Arten,
Blumen in Inseln (witcher_01: rote/orange Ähren in Gruppen von 10–30), Hochstauden an Wasser und Waldrand; (c) 1,5–4 m: Weidengebüsch
und Haselhecken, Jungbäume am Saum, liegende Stämme; (d) Krone: Weiden und Pappeln am Wasser, Eichen/Buchen/Hainbuchen auf der
Terrasse, dazwischen Lichtungen. Die Bildkritik (`bildkritik-witcher-messlatte.md`, W6FIN_E5) nennt als konkreten Mangel in
Eldarien: Bäume im 15-m-Raster ohne Clumps, Wiese „ein Beige ohne hohe Gräser, Büsche oder Felsanker“, und empfiehlt Weiden nur
20–40 m vom Wasser, Clumping-Noise 40–100 m, Büsche in 3–7er-Gruppen – diese Zahlen sind ins Regelwerk übernommen.

**Dichten und Gruppen (Richtwerte, aus den Bildern abgeschätzt).** witcher_01 zeigt in 10 m Bildtiefe ~6 Grasarten/Höhen,
1 Blumeninsel je 15–25 m², 1 Busch je 20–40 m², einen Stein je 3–5 m² am Ufer; witcher_03 im Auwald 1 liegenden Stamm je ~100 m²,
Zweige/Äste 0,05–0,1 je m². CDPR beschreibt das Verfahren hinter diesen Dichten: Die GDC-2014-Session „Landscape Creation and
Rendering in REDengine 3“ (Marcin Gollent) nennt Vegetation, die „procedurally generated, offline and in real time“ gesetzt wird,
und ein Generator simuliert „water accumulation and sunlight distribution“, vergleicht Schattenwurf mit dem Lichtbedarf jeder Art und
setzt die passende **[Suchauszug: gdcvault.com/play/1020197; dualshockers.com GDC-Bericht]**. Die REDkit-Doku beschreibt das
Vegetation Edit Tool mit eigenen Pinseln je Geländetyp („fields, meadows, swamps and forests“) mit einstellbarem Spacing und
Scale-Variation **[Suchauszug: cdprojektred.atlassian.net W3REDkit „Vegetation Edit Tool“; 80.lv „World building of Witcher 3“]**.
Genau das bildet der Planer nach: Wasserabstand + relative Höhe (Feuchte) und Kronendach (Licht) steuern jede Klasse.

**Höhenstufen Ufer → Aue → Terrasse.** In Velen liegen drei Stufen über dem Wasser: der Uferstreifen (0–8 m, Schilf, Seggen,
Kies, Weidengebüsch, freigespülte Wurzeln an Prallhängen), die Aue (bis ~4 m über Wasser, Wiese mit Blumeninseln, Pappel-/Weiden-
gruppen, Altarme und Teiche mit dichtem Schilf) und die Terrasse (höher, trockener: Hainbuchen-/Eichenhaine, Kiefern auf
Sandkuppen, Felder und Dörfer). Der Planer berechnet beides aus `hoehe.f32` und `karte_wasser.r8`: Distanz zum nächsten Wasser und
Höhe über dem nächsten Wasserpunkt (Jump-Flooding, §2).

**Farbakzente.** Blumeninseln (Mohn rot, Kornblume blau, Kamille weiß, Wegwarte hellblau, Flockenblume violett) in 10–26er-Gruppen
mit einer Hauptart je Insel (60 %), nicht gleichmäßig gestreut; Goldrute/Topinambur gelb am Ufer; Herbstlaub kommt in Eldarien nur
über Material (PerInstanceRandom-Tint) – die Palette hat keine Herbstbäume, siehe Einkaufsliste.

**Blickziele und Spuren von Leben.** Weißgarten ist „known for its fruit orchards“, der Fluss Ismena durchzieht das Dorf
**[Suchauszug: thewitcher3.wiki.fextralife.com/White_Orchard]**; Velen wird als „barren, dotted with skeletal trees and broken
structures“, mit „dense forests, sprawling swamps, and war-ravaged villages“ beschrieben **[Suchauszug: primoumo.medium.com; xgamerss.com]**.
Für Eldarien heißt das: je Weiler Feldstreifen bis an den Ortsrand, lückige Zäune, ein Obstgarten, Kopfweiden-Reihen an Gräben und
Wegen, eine Wassermühle am Bach mit Gefälle, Solitärbäume als Blickziel auf freier Wiese, Totbäume als Velen-Akzent. Die
Witcher-4-Demo (Kovir, State of Unreal 2025) belegt die Technikseite: Nanite Foliage, „every single leaf and pine needle“, Mass-Crowds,
Fast Geometry Streaming **[Suchauszug: press.cdprojektred.com; gameinformer.com]**; der Digital-Foundry-Befund, dass Gras und Kleinzeug
über Runtime-GPU-PCG kommen, ist in `boden-kleinzeug-gras.md` bereits ausgewertet. Für den Planer folgt daraus nur: Kleinzeug kurz
cullen (3 500–7 000 cm), Bäume ohne Cull.

**Was in E5/G5/I5 heute fehlt (Ist-Bilder).** W6FIN_E5: Weiden und Kiefern gleichmäßig verteilt, kein Uferband, keine Büsche,
keine Stämme; BACH3_G5: Bach ohne Uferraum, Wiese ohne Höhenstaffel, Büsche als gleichmäßige Punkte; TERR3_I5: Ufer als Kiesstreifen
ohne Schilf, keine Stufe Ufer/Aue. Die Aue-Ebene adressiert genau diese drei Lücken (Schichten 1, 2, 5).

## 2. Regelwerk (`aue_regeln.json`) – Erklärung je Schicht

Alle Dichten sind Instanzen je m² je Höhenstufe (`ufer` / `aue` / `terrasse`), multipliziert mit dem Lichtfaktor
`licht[offen, beschattet]`, Lagenfaktoren (`lage_*.r8`), Feuchte (Wassernähe 40 m + Lagen Schlamm/Algen/Moos/Kraut/Lehm), Hang
(voll bis 18°, Klassen-Maximum 12–60°), Höhe (Abnahme ab 80 m, 0 ab 260 m), Sand-Dämpfung (Sand-Lage 100 % → ×0,25, außer Kiefern,
Kiesel, Zweige) und Wüstenfaktor 0,6. Gruppen: die Dichte ist Einzelinstanz-Dichte, Gruppenzentren = Dichte/Gruppenmittel; Mitglieder
liegen in `radius_m` um das Zentrum und werden an Sperrzellen erneut geprüft. Zufall ist ein Hash aus globaler Rasterkoordinate, Seed
1105 und Klassenkanal – deterministisch und nahtlos über Feldgrenzen. Abstände: 2,5 m Kleinzeug / 4 m Bäume, Sträucher, Totholz zu
Wegen; 5 m zu Orten; 0,5 m (Schilf, Kleinzeug) bzw. 1,5 m (Bäume, Sträucher) zu Wasser; 1 m zu Bestandsstämmen, 3 m für neue Bäume;
0,8 m zu Ufer-Ebene-Instanzen; 60 m Radius um `docs/staedte/standorte.json` (optional).

**Höhenstufen.** `ufer`: Wasserabstand ≤ 8 m oder (Höhe über nächstem Wasser ≤ 1 m und Abstand ≤ 40 m); `aue`: Höhe über Wasser ≤ 4 m
und Abstand ≤ 120 m; sonst `terrasse`. Fenster ohne Wasser: `aue` dort, wo Wiese+Moos+Gras ≥ 0,45, sonst Terrasse. `stillwasser`
(Altarm/Teich): Zelle in einem See-/Teichumriss (`wasser_welt.json` `seen[].umriss`, `teiche/teiche.json`, Polygonrasterung im Planer)
oder Wasseranteil im 61-m-Fenster < 0,12 (schmales, stilles Gewässer); dort Schilf ×2, Seggen ×1,5, Kiesel ×0,3.

**Schicht `0 boden`** (Sichtweite 4 000–7 000 cm, kein Schatten, keine Kollision, Eingraben 1–3 cm, Kippen 0,5–1,0):
- `laub` (DeadLeaves_01/12/13/14, poplar_leaves_01/02, detail_leaves_01/03): 0,004–0,008/m² offen, ×9 unter Kronen, Laub-Lage ×2,
  Wiese ×0,5; Gruppen 2–5 in 1,5 m.
- `zweige` (WoodenSticksAndTwigs_01–10, DryBranches_01/03/04/05, branch_01_1/2): 0,004–0,006, ×6 unter Kronen, Laub ×1,8.
- `kiesel` (SmallStonesPack_01–14): nur Aue/Terrasse 0,004–0,006 auf Kies ×4, Geröll ×3, Erde ×1,5, Wiese ×0,3, am Ufer 0 – Kiesbänke
  kommen aus `FT_EL_UF_*`.
- `pilz` (mushroom_01/02): 0,0005–0,001, ×4 im Schatten, Feuchte 0,5–2,0, Gruppen 3–7.
- `bodendecker` (CloverVarieties_01–04, GroundCover_01/05–08, ground_foliage_02_0/1): 0,006–0,010, Wiese ×1,4, Moos ×1,5, Trockengras ×0,5.

**Schicht `1 mittel`** (0,3–3 m):
- `grasbueschel` (grass_meadow_01/02/03/04/06/08 = 0,6–1,7 m, grass_bush_02–04, dead_grass_01/02): 0,010–0,016, im Wald ×0,25;
  Gruppen 2–6, Maßstab 0,8–1,4 → Witcher-Höhenstaffel knie- bis hüfthoch, ergänzend zum GPU-Gras (0,2–1,2 m).
- `blumeninsel` (Mohn, Kornblume, Kamille, Wegwarte, Flockenblume, Seifenkraut, Johanniskraut, Margerite, Wundklee; 14 Netze):
  0,004–0,009 als 10–26er-Inseln, Radius 4,5 m, Hauptart je Insel 60 %, Wiese ×1,5, Laub ×0,1 → ~1 Insel je 1 600–3 000 m².
- `hochstaude` (Goldrute, Topinambur, Nessel, Crownbeard_07/08; 0,65–1,7 m): Ufer 0,010, Aue 0,005, Terrasse 0,002, Saum ×2, Feuchte 0,6–2,0.
- `strauch` (Elderberry_05–09 Nanite, grey_willow_02–04, hazel_01/02, maple_bush_02–04, sea_buckthorn_01/02 als Weißdorn-Ersatz):
  0,0026–0,0045, Gruppen 1–4 in 2,8 m, Saum ×2,5, Maßstab 0,85–1,5, Sichtweite 30 000.
- `hecke_weg` (hazel_02, Elderberry_08/09, sea_buckthorn_01/02, maple_bush_04): Band 4–7 m neben Wegen, auf 40 % der 48-m-Abschnitte,
  0,12/m² → ~1 Strauch je 2,8 m Wegstrecke, Yaw entlang des Weges ± 15°, nur > 150 m vom Ort (Feldrand-Hecken um Orte: `spuren_overrides`).
- `jungbaum` (Hornbeam_Sapling_01–04 Nanite, Poplar_plant_A/B/C, beech_plant_02/03): 0,0012–0,0016, Saum ×3, Lichtungsrand ×2.
- `farn` (Fern_01–06, SilverLadyFern_01/02): nur beschattet (offen ×0,05, Schatten ×4), Feuchte 0,5–1,8, Gruppen 3–10.
- `totholz_klein` (dead_log_01–04, Tree_Stump_02/03, OldTreeBranch_03): 0,0005–0,0008, Yaw hangabwärts bzw. flussparallel (< 12 m vom Wasser).
- `totholz_gross` (trunk_01/02, LargeFallenTree_02, FallenTreeAssembly_01, MossyTree_01, Tree_Stump_01): 0,0002–0,00035, **Kollision**,
  Eingraben 8 cm + 25 % der Netzhöhe (FORMAT §3: Stämme 20–35 %), Sichtweite 60 000.
- `stumpf` (stump_03, TreeStump_01, BirchTreeStump_01, RottenTreeStump_01): 0,0002–0,0004, ×3 innerhalb 200 m um Orte (Holzschlag).

**Schicht `2 baum`** (Kollision, Sichtweite 0, Eingraben 8–12 cm, Kippen ≤ 0,08, Hang ≤ 28–32°, 3 m Abstand zu Bestandsbäumen):
- `auwald_weide` (Big_Tree_willow_01/02, kein Nanite, 30–38 k Dreiecke mit LOD): nur 3–28 m vom Wasser, Ufer 0,0035, Aue 0,0006,
  Gruppen 2–5 in 9 m, Maßstab 0,55–0,9 (9–19 m hoch).
- `auwald_pappel` (Poplar_01_Standalone, Poplar_03/04/05, SM_Poplar_tree_02/03/04/05_Optimised): 6–45 m vom Wasser, Aue 0,0022,
  Gruppen 2–6 in 11 m, Moos ×1,3, Trockengras ×0,6.
- `hain_terrasse` (Hornbeam_Field_01–04 + Forest_01/02/03/05/07 Nanite, beech_tree_01/02/03/04/06): Terrasse 0,0016, Aue 0,0010,
  Haine 6–18 Bäume in 15 m, Mindestabstand 4 m, Lichtungsfenster: 25 % aller 120-m-Zellen ohne Hain-Zentren, im Bestandswald ×0.
- `kiefer_hain` (pine_beach_01_A/B, 02_A, 03_A): Terrasse 0,0006 auf Trockengras ×2 / Sand ×2, Wiese ×0,3, Gruppen 3–7 (Velen-Mix, E5-Ist).
- `solitaer` (Hornbeam_Field_01/02, Poplar_02_Standalone, beech_tree_06/09, Big_Tree_willow_02 nur < 30 m Wasser): Blickziel, 1 Baum je
  96-m-Raster mit p = 0,45, 40 m frei von Bestandsbäumen, Beschattung ≤ 0,08, Maßstab 1,1–1,4 → 20–45 je Vollfeld.
- `totbaum` (DeadTree_01/02 Nanite, EuropeanBeech_Dead_M_01): 0,00005–0,00012, Feuchte ×1,6 (Velen-Akzent, Ufer).

**Schicht `5 wasserkante`** (Abstimmung mit `FT_EL_UF_*`: Instanzen der Ufer-Ebene werden geladen, 0,8 m Sperrradius; Zellen mit > 3
Ufer-Steinen im 7×7-Fenster gelten als Kiesbank → Schilf ×0,3):
- `schilf` (Rohrkolben_Horst_1–6, Rohrkolben_Jung_1–3 = Eldarien-Netze 0,4–3,2 k Dreiecke, ToadRush_00/02): Band 0,5–6 m, 0,22/m²,
  Gruppen 4–12 in 2,2 m, Hang ≤ 12°, Kippen 0,1 (aufrecht), Stillwasser ×2.
- `seggen` (grass_meadow_02/04/08, grass_bush_02/03, beach_grass_01_1/2, rough_horsetail_01–03): Band 1–12 m, 0,10/m², Stillwasser ×1,5.
- `uferstaude` (petasites_spurius_01–03 = Pestwurz, Goldrute, Topinambur, Nessel, hedge_bedstraw, Periwinkle_01): Band 2–16 m, 0,03/m².
- `uferwurzel` (crooked_root_01/021/04/05, MossyForestRoots_01/02): Steilufer (Hang ≥ 14°) 0,8–4 m vom Wasser, 0,012/m², voll gekippt.

**Budget** (`budget`): 60 000 je Feld (Ziel 52 000), ≤ 3 000 mit Kollision; Schichtziele 22 000 / 22 000 / 2 600 / 12 000; Ausdünnung
deterministisch in der Reihenfolge Kiesel → Zweige → Laub → … → Haine → Weiden → Totbaum → Solitär (Solitäre zuletzt).

**Overrides für Teil C/D** (gleiche Schlüssel wie `felsgruppen_regeln.json` / `spuren_regeln.json`):
- `felsgruppen_overrides`: Palette `moos`, Biomfaktor 0,35, Klassen `band`, `wand`, `grat`, `fuss` aus; `kuppe` nur Terrasse (p 0,5,
  Hang 4–30°), `blockstrom` nur Terrasse p 0,2, `prallhang` mit Krümmung ≥ 0,003, Uferabstand 2–8 m, 2–5 Blöcke + 6–14 Steine +
  15–30 Kiesel; Steine 40–55 % eingegraben; Lagen-Boost Geröll/Kies, Hemmung Wiese/Schlamm.
- `spuren_overrides`: Feldstreifen Ring 20–220 m, 70 % der Zellen, max 18 je Ort / 40 je Feld, Hang ≤ 6°, 45 % mit Frucht, Zaunlücken
  25 %, **Feldrand-Hecke** auf 50 % der Ränder (hazel_02, Elderberry_08, sea_buckthorn_01/02, Abstand 2,5 m, 30 % Lücken); Obstgarten
  max 2 je Ort, Ring 15–140 m, Reihe 6,5 m × 5,5 m, Ersatznetze Hornbeam_Forest_09/10 + beech_tree_00_C/D; Zäune 2–4 je Ort à 30–90 m;
  **neu `kopfweiden_reihe`** entlang Weg/Bach/Graben, Abstand 6–9 m, 30–90 m lang, 1–3 je Ort, ≤ 25 m vom Wasser, Ersatz
  Big_Tree_willow_01 auf 0,45–0,6 (7–10 m) als Akteur; **neu `muehle`** (nur Positionsliste: Bach mit ≥ 2 m Gefälle je 100 m, ≤ 250 m
  vom Ort); Stege nur an Stillwasser; Blickziel-Typen aue = Solitärbaum, Kopfweiden-Reihe, Ruine, Blumenlichtung, Mühle.

## 3. Abgrenzung zu vorhandenen Ebenen: ergänzen, nicht ersetzen

| Ebene | Verhältnis zur Aue-Ebene | `entfernen`? |
|---|---|---|
| Witcher-Bewuchs `FT_EL_WIT_*` (50 000 Kleinzeug: Haine, Waldsaum, Totholz, Farne, Laub, Blumeninseln Crownbeard/Lachenalia/Windflower, Gebüsch) | Aue nutzt **andere Netze** (Meadow-Blumen, Rohrkolben, Weiden, Pappeln, Hainbuchen-Haine) und andere Steuergrößen (Höhenstufe, Wasserabstand); WIT-Instanzen werden als `belegt` (1,2 m) geladen | nein. Vorschlag `entfernen_vorschlag`: `SM_KikuyuGrass_` (warmes Namaqualand-Gras der WIT-Ebene passt nicht in die Aue) – Standard aus, nach Abnahme einschalten |
| Wald-Bestand `FT_EL_BST_*` (17 000 Bäume) | Liefert das Kronendach (Beschattung → Laub/Zweige/Farn/Pilz hoch, Gras/Blumen niedrig) und den Saum; neue Bäume halten 3 m Abstand, Haine nur außerhalb (Beschattung ×0), Solitäre 40 m frei | nein |
| Ufer `FT_EL_UF_*` (26 000 Kiesel/Kopfsteine/Blöcke/Treibholz) | Aue setzt **keine** Uferkiesel und kein Treibholz; Schilf/Seggen/Stauden füllen die Pflanzenlücke 0,5–16 m; Kiesbänke dämpfen Schilf ×0,3; 0,8 m Sperrradius um Ufer-Instanzen | nein |
| Felsschalen `FT_EL_FS_*` | unberührt (Aue hat fast keine Felsen; Felsgruppen-Planer mit Overrides) | nein |
| Landschafts-Gras `GT_*` | bleibt die Basis 0,2–1,2 m; Aue-Grasbüschel (0,6–1,7 m) sind die Hero-Staffel darüber | nein |
| Wüste `FT_EL_WU_*` (C3–E5) | nur ergänzen: Faktor 0,6, Sand/Sandstein ≥ 0,5 gesperrt | nein |

Begründung „kein Ersetzen“: Jede vorhandene Ebene trägt einen anderen Maßstab (Bildkritik §1: „jede Fläche trägt genau einen
Maßstab“); die Aue-Ebene fügt die fehlenden Stufen dazwischen ein. Erst wenn im Editor doppelte Blumenflächen oder zu dichter
Unterwuchs sichtbar werden, sollte man die WIT-Dichte je Feld über deren Planer senken, nicht per `entfernen`.

## 4. Testanleitung

**Rauchtest Cloud (gelaufen).** Mini-Produktionswurzel mit `hoehe.f32` in voller Größe 7057 × 9577 (memmap, nur E5-Fenster
beschrieben: flache Aue 12 m, Mäanderfluss 18 m breit, Bach, Altarm 110 × 36 m mit Umriss in `wasser_welt.json`, Terrassenstufe +18 m,
Kuppe), `karte_wasser/weg/ort.r8`, `lage_Wiese/Trockengras/Moos/Laub/Sand.r8`, `eigner.r8` + `welt.json`, `bestand/E5` (190 Bäume in
3 Hainen), `ufer/foliage_E5` (3 000 Kiesel), `daten/netze.csv`. Ergebnis `python -I scripts/aue/aue_plan.py E5 --bild`:
**32 627 Instanzen (790 mit Kollision), 188 Netze, Laufzeit 8,0 s** (4 Kerne, NumPy 2.5, ohne numba), Schichten boden 11 980 /
mittel 16 254 / baum 702 / wasserkante 3 691 (E5 ist Wüstenfeld → Faktor 0,6); 0 Instanzen auf Wasser/Weg/Ort; alle f32 lesbar
(Zeilen × 10, Quaternionen normiert, Anzahl = `plan.json`); zwei Läufe byte-identisch (MD5); Stillwasser-Umriss erkannt
(28,9 % der Uferzellen still); Kiesbank-Dämpfung aktiv (8,7 % der Uferzone). Zweiter Lauf mit nur `hoehe.f32` (keine Karten, F6/J7):
klare Hinweise je fehlender Datei, J7 (Randspalte, 505 m breit) 22 774 Instanzen in 0,6 s; ungültiges Feld und fehlende Basis
→ klare Meldung. Prüfbild `docs/pruefung/aue/E5.png`: Höhenstufen getönt (Ufer blau, Aue grün, Terrasse beige), Stillwasser hellblau,
Klassen nach `bild_farben`.

**Erwartete Instanzzahlen je Feld (Richtwert, Spanne ±35 %; Grundlage: Land-/Wasseranteil aus `biome_je_feld.md`, 0,05–0,06
Instanzen je m² Aue-Land nach Budget):**

| Feld | Land % / aue % | gesamt | boden | mittel | baum | wasserkante |
|---|---|---|---|---|---|---|
| C5 | 100 / 63 | 30 000–42 000 | 12 000–17 000 | 12 000–17 000 | 900–1 600 | 5 000–9 000 (Wasser 5,8 %) |
| E5, D5, C4 (Wüste ×0,6) | 97–100 / 93–75 | 20 000–34 000 | 8 000–13 000 | 8 000–14 000 | 500–1 100 | 3 000–7 000 |
| F4, F6 | 54 / 79, 51 / 96 | 20 000–30 000 | 8 000–12 000 | 8 000–12 000 | 500–1 000 | 2 500–5 000 |
| J6, D7, B7, F2 | 41–28 / 98–54 | 8 000–20 000 | 3 000–8 000 | 3 000–8 000 | 200–600 | 500–3 000 |
| A7, I1, F1, J5, A6, J3 (Sand 86–92 %) | 13–7 / 98–100 | 1 500–6 000 | 600–2 500 | 500–2 500 | 100–400 | 0–800 |
| G2, J7, F3 | 4–1 | 200–2 000 | – | – | 0–100 | – |

Kollision je Feld: 600–2 200 (Bäume 500–2 000, große Stämme 50–200) – unter 3 000; bei Überschreitung dünnt der Planer alle
Kollisionsklassen proportional.

**Prüfkameras (Feld, Position als Raster-/Weltkoordinate, Blick):**
1. **E5 Flussufer, Augenhöhe 1,7 m**, am Außenbogen des Hauptflusses, Blick flussaufwärts gegen die Sonne (Vergleich W6FIN_E5, witcher_01).
   Erfolg: Schilfgürtel 0,5–6 m mit Lücken an Kiesbänken, dahinter Seggen/Pestwurz, Weiden 3–28 m in 2–5er-Gruppen, keine Pflanze
   schwebt über der Wasserkante (Eingraben 3–4 cm), keine Instanz im Wasser.
2. **C5 Aue, 2 m Höhe, 60 m vom Wasser**, Blick quer zur Aue auf die Terrasse. Erfolg: innerhalb 10 m mindestens ein Objekt in 0,5–3 m
   Höhe (Grasbüschel/Strauch/Jungbaum), Blumeninseln als Flecken (nicht Streu), Pappelgruppe im Mittelgrund, Hainbuchen-Hain mit
   Lichtung am Horizont, Solitärbaum als Blickziel.
3. **F6 Altarm/Teich (Stillwasser)**, 3 m Höhe, Blick über das Wasser. Erfolg: Schilf doppelt so dicht wie am Fluss, Totbaum am Ufer,
   keine Kiesel am Stillufer.
4. **D5 Weg mit Hecke, 1,7 m, Blick entlang des Weges** (außerhalb 150 m vom Ort). Erfolg: Heckenabschnitte 4–7 m neben dem Weg, 40 %
   der Strecke, Sträucher längs ausgerichtet, nichts näher als 4 m am Weg.
5. **Draufsicht 300 m über C5** (Prüfbild und Editor). Erfolg: Haine als Clumps 20–40 m mit 25 % Lichtungsfenstern, kein 15-m-Raster,
   Weiden nur am Wasserband, Terrasse mit Kiefern-Gruppen auf Trockengras.
6. **Nahtprüfung** an der Grenze C5/D5 und E5/F5 (Draufsicht 100 m): keine Dichtesprünge, Gruppen laufen über die Grenze (Fenster + 64 m).

**Erfolgskriterien in Zahlen:** Instanzen je Schicht innerhalb der Tabelle; Kollision < 3 000; Setzer-Zeit je Feld < 5 min
(188 Netze → 188 Foliage-Typen `FT_EL_AU_*`, davon 25 Baum-/Stammtypen mit Kollision); kein Netz mit Nicht-Nanite-Bäumen
(Poplar, Big_Tree_willow) ohne LOD-Prüfung; PNG und `plan.json` je Feld vorhanden.

## 5. Einkaufsliste fehlender Assets (frei bevorzugt, Stufe High 4K)

| Was | Exakter Name (Fab/Megascans) | Stufe | Wofür | Status |
|---|---|---|---|---|
| **Kopfweide** (Salix alba, pollard) | nicht gefunden; Megascans führt keine Kopfweide. Kandidaten: Fab-Suche „Pollard Willow“ (Drittanbieter) oder eigene Variante aus `Big_Tree_willow_01` (Stamm kürzen) | High | `kopfweiden_reihe` (Spuren-Override), Gräben, Weg- und Bachränder | **offen**, Ersatz Big_Tree_willow_01 × 0,45–0,6 |
| **Weide/Erle Nanite** (Salix, Alnus) | Fab „Stylized Willow Tree“ (c6bfbdf6-…) ist stilisiert, 2 947 Dreiecke, Nanite „not recommended with wind“ **[Suchauszug]** – ungeeignet; Megascans Trees „European Black Alder“ / „White Willow“ bei Erscheinen prüfen | High | Ersatz der Nicht-Nanite Big_Tree_willow (30–38 k Dreiecke) | offen |
| **Obstbäume** (Apfel, Birne, Pflaume) | Fab-Suche „apple tree Nanite“ lieferte keinen Treffer **[Suchauszug]**; Megascans „Apple Tree“ (Trees-Kollektion) prüfen | High | Obstgarten je Weiler (Weißgarten) | offen, Ersatz Hornbeam_Forest_09/10 |
| **Hecken** (Weißdorn, Schlehe, Haselhecke als Segment 2–4 m) | keine Treffer; Megascans „Hawthorn“ / „Blackthorn“ prüfen | High | Feldrand- und Wegsaum-Hecken | offen, Ersatz sea_buckthorn + hazel |
| **Schilf-Varianten** (Phragmites) | Quixel Megaplants „Dry Common Reed“ (Fab, Experimental, Procedural Vegetation Editor) – im Projekt als Megaplant_Library vorhanden, aber nur Blatt-/Blütenkarten, kein Streunetz; Drittanbieter „Common Reed mid poly, 3 Netze, auto LODs“ **[Suchauszug]** | High | Schilfgürtel am Fluss (Rohrkolben = Teich-Optik) | **kaufen/prüfen**: 3-Netz-Set |
| **Seggen/Binsen** (Carex, Juncus) | Megascans „Soft Rush“ / „Sedge“ prüfen; ToadRush vorhanden (15–29 k Dreiecke ohne Nanite, nur 2 Netze eingesetzt) | High | Band 1–12 m | offen |
| **Feldfrüchte** | Fab „Nanite Foliage – Wheat Field“ (dbcbdc42-…), Vollgeometrie ohne Alpha, Wind + Interaktion, UE 5.1+, Update 08/2025 **[Suchauszug]** | – | Feldstreifen (Spuren) | **kaufen** (Preis nicht ermittelt) |
| **Wassermühle** | kein Mühlen-Netz im Inventar; Fab-Suche „medieval watermill“ (Hivemind/Meshingun-Kits enthalten keine) | High | Blickziel am Bach | offen |
| **Herbstlaub-Varianten** | Megascans Hornbeam hat nur Sommerlaub; Alternative: Material-Instanz `MI_EuropeanHornbeam_*` mit Tint (kein Kauf) | – | Farbakzent Herbst (witcher_07) | Material statt Kauf |
| **Uferstauden** (Mädesüß, Blutweiderich, Iris) | Megascans „Purple Loosestrife“, „Meadowsweet“, „Yellow Iris“ prüfen | High | `uferstaude` | offen, Ersatz Pestwurz/Goldrute |

Kostenhinweis aus `boden-kleinzeug-gras.md`: Megascans ist seit 2025 pro Asset kostenpflichtig (ab 0,99 USD), sofern nicht vor dem
31.12.2024 beansprucht – zuerst im Fab-Konto prüfen, welche der oben genannten Namen schon lizenziert sind.

## 6. Offene Punkte und Annahmen

1. **Formate der optionalen Dateien** (`wasser_welt.json` `seen[].umriss` als `[[x_cm, y_cm], …]`, `teiche/teiche.json`,
   `docs/staedte/standorte.json` mit `x_cm/y_cm` oder `x/y` + `radius_m`) sind aus FORMAT §2 abgeleitet; abweichende Strukturen werden
   mit Hinweis ignoriert, der Planer läuft dann ohne Stillwasser bzw. ohne Standortsperre.
2. **Höhe des nächsten Wassers** wird aus `hoehe.f32` an der nächsten Wasserzelle gelesen (Jump-Flooding). Liegt das Wasserspiegel-
   Mesh höher als die Landschaft unter dem Fluss, ist `hrel` zu groß → Aue-Stufe zu schmal; dann `aue_hrel_max_m` auf 6–8 setzen.
3. **Ufer-Ebene**: Der Planer liest `ufer/foliage_<Feld>/plan.json` + f32 und erkennt Kiesbänke an der Steindichte (> 3 im 7×7-Fenster).
   Falls die Ufer-Ebene ihre Instanzen unter anderem Pfad ablegt, greift nur noch die Wasserabstands-Regel.
4. **Witcher-Ebene `witcher/<Feld>/`**: Als Nicht-Baum-Instanzen „belegt“ gelesen; der Planer erkennt Bäume dort nur am Namen
   (Hornbeam, beech, pine, willow, poplar, birch); Rollenfeld `rolle` in deren `plan.json` wäre zuverlässiger.
5. **Nicht-Nanite-Bäume** (Poplar_*, Big_Tree_willow, beech_tree, pine_beach): Sichtweite 0, aber LOD-Übergänge im Editor prüfen; bei
   Nanite-Umstellung Masken-Material/WPO beachten (Taxonomie, Qualitätshinweise). ToadRush ohne Nanite (15–18 k Dreiecke) steht nur mit
   2 von 11 Schilf-Netzen in der Palette.
6. **Hecken-Richtung** kommt aus dem Gradienten des geglätteten Weg-Distanzfelds; an Kreuzungen ist der Yaw unbestimmt (±90°) –
   dort stehen Sträucher schief zur Straße; akzeptabel, sonst Kreuzungszellen (zwei Wege < 10 m) ausnehmen.
7. **Eingraben nach Netzhöhe** gilt nur für `totholz_gross` (25 % der Höhe aus `netze.csv`); Pivot-Lage der Stämme (Mitte oder unten)
   ist unbekannt – `netze_masse.json` hat für `SM_trunk_01/02` keine Bounds; nach dem ersten Setzen prüfen, ob Stämme schweben.
8. **Zahlen** aller Dichten sind aus Bildern geschätzte Richtwerte; die Witcher-Quellen nennen keine Instanzen je m². Erster
   Kalibrierschritt: C5 und E5 setzen, Kamera 1 und 2 aufnehmen, `--faktor 0,7 … 1,4` vergleichen.
9. **Felder mit Sand-Strand** (F1, I1, J3, J5, A6, A7, J7: Sand 86–98 %) bekommen über die Sand-Dämpfung nur ~25 % der Aue-Dichte; ob
   dort überhaupt Aue-Bewuchs gewünscht ist (Küstenwiese?) entscheidet Ferat – sonst diese Felder nicht planen.
10. **Status-Datei** `verteilung-STATUS.md` wurde nicht verändert (Koordinator); B2 kann auf „fertig (ungetestet)“ gesetzt werden.
