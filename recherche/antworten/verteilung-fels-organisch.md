# Fels organisch – Felsen, die zum Berg gehören (Auftrag 11, Teil C)

**Projekt:** Eldarien, UE 5.8.3, 1-m-Raster 9577 × 7057, World Partition, Nanite. **Stand:** 2026-10-10.
**Lieferung:** dieses Dokument, `skripte/felsgruppen_regeln.json` (alle Zahlen), `skripte/felsgruppen_plan.py` (Planer, FORMAT.md §3/§5).
**Status:** Vorfassung lief lokal mit Echtdaten (A5, G4, E1, C6) ohne Absturz; **Korrektur Runde 1** (Abschnitt h) setzt
`verteilung-KONVENTIONEN.md` um und ist in der Cloud nur synthetisch rauchgetestet (B4 + G4). Kein Setzen im Editor. Zahlen ohne Quelle sind
Richtwerte und so markiert. Web-Quellen nur als Suchauszüge (kein
Direktzugriff auf Epic-Doku/Fab/80.lv aus dieser Umgebung).

## a) Kurzbefund aus den Bildern: warum die Felsen „aufgeklebt“ wirken

Die vier Ist-Bilder (BERG8_A5, BERG8_C2, FELS7_A4, FELS7_B5) zeigen dasselbe Muster, die drei Zielbilder (witcher_04/06/07) das Gegenteil:

| Befund im Ist-Bild | Beleg | Im Zielbild |
|---|---|---|
| **Einzelsteine ohne Gruppe.** Jede Schale ist ein Solitär; kein Hauptfels mit Satelliten, kein Schutt, kein Kieselsaum. | C2: ~200 dunkle Shards als gleichmäßiges „Konfetti“ auf der Kuppel; A4: Perlenketten aus Einzelstücken. | witcher_06: links ein hausgroßer Block mit 3–4 kleineren davor, Schnee nur auf den Oberseiten; dazwischen Kopfsteine. |
| **Keine gemeinsame Schichtneigung.** Jede Schale hat eigenen Yaw/Pitch; die V16-Kachel darunter zeigt horizontale Linien, die Schalen ignorieren sie. | C2 links: Platten kippen in alle Richtungen; B5 rechte Flanke: helle Platten quer zur Kachelschichtung. | witcher_06/07: rote Felswände mit einer durchgehenden, leicht geneigten Bankung; Türme stehen alle in derselben Streichrichtung. |
| **Keine Kontaktzone.** Schale endet mit harter Kante auf der Kacheltextur; kein Geröll, kein Moos, kein Bodenblend; links in A5 schweben 8–10 Schalen frei über dem Meer. | A5 linker Bildrand; A4 alle Reihen (gleiche Farbe wie Kachel, keine Tiefe). | witcher_07: unter jeder Wand ein Schuttkegel, Fels geht über Kies/Moos in Wald über; witcher_04: Vordergrundplatte mit Flechten, Kräutern und Schnee in Rissen. |
| **Auf Terrassenstufen statt an Graten.** Die Felsreihen folgen den Reststufen der alten Terrassen (horizontale Reihen im gleichen Abstand), nicht Graten, Rinnen oder Wandfüßen. | A4: 8–10 waagrechte Reihen; C2: Shards auch mitten in der glatten Kuppel. | witcher_04/07: Fels dort, wo die Form bricht – Gratlinien, Türme, Wandfüße; die glatten Flanken tragen Wald oder Schnee. |
| **Gleiche Größe.** Alle Shards ~5–10 m, keine Staffelung über drei Größenstufen. | A4, C2. | witcher_06: Wand (100 m) → Blöcke (5–10 m) → Kopfsteine (0,5 m) → Schnee/Kies. |

Zusammengefasst: Die heutige Ebene streut **eine** Größenstufe **statistisch** auf **einer** Oberflächeneigenschaft (Steilheit). Es fehlen die
geologischen Lagen (Grat, Band, Wand, Fuß), die Gruppengrammatik und die Kontaktzone. Das löst kein Material allein; die Platzierung muss aus
der Geländeform kommen.

**Witcher-Belege (Suchauszüge, keine Vollansicht).** CDPR beschreibt für Witcher 3, dass Felsen als Klippen und Höhlendecken
wiederverwendet wurden („Imagine taking a rock and using it as a cliff“, [80.lv World Building of Witcher 3](https://80.lv/articles/world-building-of-witcher-3/));
Skellige wurde nach Faröer, Island und Grönland referenziert ([Consolepulse](https://consolepulse.com/multiplatform/the-witcher/guides/the-witcher-3-skellige-explained),
[PCGamesN](https://www.pcgamesn.com/the-witcher-3-wild-hunt/the-witcher-3-wild-hunt-books-to-games)) – also geschichtete Basalt-/Sedimentküsten mit
Bankung, Schutthalden und moosigen Kronen. Die Level-Designer waren laut Mapcore-Interview (Mark Foreman, Kacper Niepokólczycki, zitiert bei
[Gamebanshee](https://gamebanshee.com/kwaax)) zugleich Komposition-Treiber des Blockouts; Kaer Morhen liegt laut Peter Gelencser
„huddled against the stone precipices“ ([PCGamesN](https://www.pcgamesn.com/the-witcher/story-games)). Für die Witcher-4-Demo (Kovir, Unreal Fest 2025)
liegen Felsen und Bäume in einer **Offline-PCG-Schicht**, nur Kleinzeug/Gras läuft als Runtime-GPU-PCG (Stockholm-Talk „Runtime PCG in The Witcher 4“,
DF-Interview; Nachweise in `boden-kleinzeug-gras.md`). Eine CDPR-Quelle zu konkreten Felsregeln gibt es nicht; die Regeln unten sind aus den
Zielbildern und den Praktiker-Regeln in `klippennetze-a5.md` (Polycount, Brushify, Kodeco) abgeleitet.

## b) Geologische Platzierungsregeln aus den Rasterdaten

Alle Zahlen stehen in `felsgruppen_regeln.json`; hier die Begründung. Grundlage ist `hoehe.f32` im Fenster Feld + 64 m.

**Ableitungen.** Hang und Normale aus einer leicht geglätteten Höhe (Gauß σ = 1,5 m). Krümmung aus dem Hessian einer Gauß-geglätteten Höhe
mit σ = 8 m (FWHM ≈ 19 m, entspricht der geforderten Glättung 15–30 m): Eigenwerte λ₁ ≥ λ₂; **Gratstärke** G = −λ₂ (konvex), **Muldenstärke**
M = λ₁ (konkav), Gratachse = Richtung des Eigenvektors zu λ₁ (die Richtung geringster Krümmung). Zweite Skala σ = 25 m (Laplace) für Hangfüße,
σ = 12 m für Kuppen. Alles separierbare NumPy-Faltung (keine Zellschleifen); Max-/Min-Filter per Verdopplungsschritten (van-Herk-Näherung).

| Lage | Bedingung (Zelle) | Gitter / Annahme | Gruppe |
|---|---|---|---|
| **Grat/Kamm** | G ≥ 0,02 1/m, Hang 10–72°, nicht Mulde | Gitter 14 m, p = 0,55 × Lagenfaktor × clip(G/0,06; 0,5–1,5) | Hauptfels (hero mit p 0,6, sonst Block) + 2–5 Blöcke + 5–12 Steine + 12–28 Kiesel; Hauptrichtung = **Gratachse** |
| **Felsband** | Hang 32–70°, Bandphase: frac((h − tan(dip)·(x·cos s + y·sin s)) / A) < 0,22, G > −0,01 | Gitter 9 m, p = 0,35 × Fels-Lagenfaktor | 1–3 geschichtete Leisten entlang des Streichens + 2–6 Steine + 6–16 Kiesel; Yaw = Streichen s, Z-Achse zusätzlich um s um **dip** gekippt |
| **Wand/Felsnase** | Hang 50–84°, G ≥ 0,012 (plan-konvexe Nase) | Gitter 36 m, p = 0,5 | 2–4 Schalen/Klippen (Akteure) + 1–3 Blöcke + 3–8 Steine; alle mit Streichen/Dip der Wand |
| **Schuttfächer** | Hang 18–42°, keine Wand, oberhalb in ≤ 8/16/32/64 m eine **große Wand** (Hang ≥ 50°, Relief ≥ 8 m in 12 m) | Gitter 10 m, p = 0,45 × Geröll-Lagenfaktor | 2–4 Stücke + 6–14 Kiesel; **Größe nach Stufe**: 0–8 m Blöcke ×0,8–1,15, 8–16 m Blöcke ×0,55–0,85, 16–32 m Steine ×0,75–1,1, 32–64 m Steine ×0,45–0,75; Stücke hangabwärts versetzt (Falllinie) |
| **Blockstrom** | Hang 5–24°, Laplace(σ 25) ≥ 0,002 (Hangfuß), Wand ≥ 25 m höher innerhalb 128 m | Gitter 16 m, p = 0,5 | 3–7 Blöcke + 6–14 Steine + 15–30 Kiesel + 50 % eine Platte; Hauptrichtung = Falllinie |
| **Kuppe** | lokales Maximum (σ 12, Umkreis 32 m), Hang ≤ 38°, nicht Wand | eine Gruppe je Kuppe, p = 0,8 | Hero (p 0,5) oder 1–3 Blöcke + 3–8 Steine + 8–20 Kiesel, Eingraben 35–45 % (sitzt im Gipfel, nicht darauf) |
| **Prallhang** | Flusspolylinie aus `wasser_welt.json`: Krümmung κ = Winkeländerung / Segmentlänge ≥ 0,004 1/m; Punkt auf **Außenufer** (gegen die Kurvenmitte) in Breite/2 + 3–10 m; dort Hang 18–75° | ein Kandidat je 25 m Bogenlänge (stärkste Krümmung) | Hero (p 0,7) + 2–4 Blöcke + 4–10 Steine + 10–20 Kiesel, Yaw = Flusstangente |
| **Mulde** (Ausschluss) | M > 0,012 1/m **und** keine Wand ≥ 10 m höher innerhalb 64 m | – | nichts (außer Prallhang) |

**Schichtneigung je Bergmassiv.** Strike s ∈ [0, 360°), Dip d ∈ [6°, 18°] und Bandabstand A ∈ [24, 40] m kommen aus einem bilinear
interpolierten Wert-Rauschen auf einem 512-m-Gitter (Seed 110): innerhalb eines Massivs (~300 m) praktisch konstant, zwischen Feldern stetig
(kein Nahtsprung), ohne Segmentierung der Berge (die bräuchte Schleifen oder scipy). Felsbänder liegen damit in gleicher Höhenlage, leicht
geneigt, und alle Band-/Wandstücke eines Berges teilen Streichen und Dip – die Spielübersetzung von „thickness, spacing and dip of rock
layers consistent“ (Draw Paint Academy, zitiert in `klippennetze-a5.md`).

**Schutthalden (Geologie).** Natürliche Talus-Hänge liegen bei 30–37° (Schwelle trockener Lockermassen 33–37°, „angle approaching 35°“ in
einer IRD-Studie; Suchauszüge: [IRD](https://horizon.documentation.ird.fr/exl-doc/pleins_textes/divers19-08/010048761.pdf),
[NHESS 2021](https://nhess.copernicus.org/articles/21/1159/2021/)). Daher Fächerklasse auf 18–42° und Fächerlänge ≤ 64 m. **Achtung:**
reale Halden zeigen häufig Sturzsortierung mit den größten Blöcken am Fuß (NHESS: „larger blocks … distal part“; nicht auf allen Kegeln). Der
Auftrag verlangt „Größe nimmt hangabwärts ab“; so ist es umgesetzt, der Parameter `groessenverlauf` in den Regeln dokumentiert die
Alternative (Stufen vertauschen).

**Gruppengrammatik** (`gruppe` in den Regeln): Hauptfels + 2–5 Nebenblöcke, 10–30 % in den Hauptfels geschoben (Abstand = (r_haupt + r_eigen) ×
0,7–0,9), Nebenblöcke um die Hauptrichtung ±35° gestreut, Steine außen (0,9–1,8 r), Kieselring 0,5–2 m mit 1,5–4 Stück/m²; Größenstaffelung
Hauptstück 1,0 → Nebenblock 0,55–0,9 → Stein → Kiesel; Yaw aller Stücke = Hauptrichtung ± 20°. **Eingraben** nach Rolle: Hero 30–45 %,
Block 25–40 %, Band/Platte 35–50 %, Stein/Kiesel 30–50 % der Netzhöhe (FORMAT §3, `klippennetze-a5.md`). **Kippen in den Hang:** Z-Achse auf
die Geländenormale, dann 4–12° (Hero/Block) zurück bergauf gedreht, so dass das Stück sich an den Hang lehnt statt hangab zu kippen; Band und
Wand bekommen statt dessen den Dip um das Streichen. **Lehnen an die Wand:** Fächerstücke der Stufe 0–8 m stehen direkt unter der Wand und
werden mit 0,8–1,15 × Maßstab und 25–40 % Eingraben in die Wandkante geschoben. **Floating-Check** (Maßnahme aus der Bildkritik): fällt der
Boden innerhalb des Stückradius tiefer ab als Eingrabtiefe + 60°-Hang erlauben, wird das Stück verworfen.

**Pivot.** `netze_masse.json` zeigt: Megascans/Namaqualand haben den Pivot unten (min_z ≈ 0 … −18 cm), die Lava-Felsen den Pivot in der
Mitte (min_z ≈ −H/2). Der Planer rechnet z = Boden − min_z·s − Eingraben·H·s; für Netze ohne Bounds-Eintrag gilt Pivot unten, für
`netz_pivot_mitte` (alle Lava-Netze) −H/2. Mountain_Environment_Set-Felsen fehlen in `netze_masse.json` – offener Punkt (g).

**Biome und Paletten.** Das Biom je Zelle kommt aus `eigner.r8` + `welt.json`; Kennzahl 0 (Weltgelände) wird **nicht** als Aue behandelt,
sondern als dominantes Biom des Feldes aus `daten/biome_je_feld.json` (B4 → bergwald), weil die großen Bergflächen im Weltgelände liegen.
Sechs Paletten (203 Netze, alle Nanite, alle Pfade gegen `netze.csv` geprüft): `nordisch` (bergwald, fjord, kueste), `tundra` (gletscher,
tundra, frost), `moos` (elfenwald, aue, heide, sumpf), `sandstein` (canyon, wueste, oedland), `lava`, `karst` (dschungel, AsianTemple-Türme).
Biomfaktoren: fjord 1,1, gletscher 1,1, bergwald/kueste/canyon/lava 1,0, tundra/frost/dschungel 0,9, elfenwald/oedland 0,8, heide 0,6, aue 0,5,
wueste 0,4 (eigener Planer, nur ergänzen, Klasse band aus), sumpf 0,25 (nur kuppe/prallhang). Lagenfaktoren: 0,6 + 0,9·max(Fels,
Felsplatte, Sandstein, Lavafels) − 0,3·Schnee für Grat/Band/Wand, 0,7 + 0,8·max(Geroell, Kies) für Fächer/Blockstrom, beide auf 0,5–1,5 geklemmt.

## c) Kontaktzone

**Geröllsaum.** Jede Gruppe erhält den Kieselring (Rolle `kiesel`, 5–40 cm: SM_SmallStonesPack_01…14, SM_stone_03…08,
SM_mountain_rock_small_01_1…5, Namaqualand rocks/stones für Sandstein; Lava hat keine eigenen Kiesel – Einkaufsliste) im Umkreis 0,5–2 m um
das Hauptstück mit 1,5–4 Stück/m², Yaw frei, Eingraben 30–50 %, Sichtweite 0–60 m, keine Kollision, kein Schatten. Zusätzlich die Steine
(0,4–0,8 m) außen um den Hauptfels. Das ersetzt nicht die PCG-Scree-Idee aus `boden-kleinzeug-gras.md`, sondern liefert den dichten Nahbereich,
den ein Runtime-PCG später übernehmen kann (dann Rolle kiesel im Planer über `budget.je_rolle.kiesel = 0` abschalten).

**Moos/Gras hochkriechend.** Zwei Wege, beide ohne neue Felsnetze: (1) im Felsmaterial über die Weltnormale (unten), (2) Pflanzen aus der
vorhandenen Palette am Fuß und auf Simsen: Moosplatten SM_moss_01/02 (Forest_Environment_Set, 0,5 m, flach), Farne SM_foliage_fern_01_1…4,
SM_fern_01_0…2, Klee SM_clover_01, Grasbüschel SM_grass_bush_01…04, Tundra-Gras SM_wk2oaeyqx_VarA…I (Fab Megascans, 0,2–0,7 m), Sauerklee
SM_uchkajuia_VarA…H; am Küstenfels SM_stonecrop_01/02 und SM_beach_grass_03_1…3. Diese Schicht gehört in die Mittelschicht (Teil D) mit Regel
„Abstand 0,3–1,5 m zu Fels-Instanzen der Ebene felsgruppen, Dichte 0,5–1/m², nur Hang < 45°, nur Rollen hero/block“; der Planer schreibt
dafür die Positionen aller Hauptstücke in `plan.json["akteure"]` bzw. die f32-Dateien, die ein Mittelschicht-Planer als Attraktor lesen kann.

**RVT-Boden-Blend des Felsmaterials (verdichtet aus `klippennetze-a5.md`, dort mit Quellen).** Der Standardgraph in UE 5.8:

1. `Runtime Virtual Texture Sample` auf `RVT_Eldarien_Boden` (BaseColor, Normal, Roughness, Specular) **und** ein zweiter Sample auf einem
   **World-Height-RVT** (eigener Asset-Typ, 16 bit, normiert auf den Z-Bereich des RVT-Volumes; muss im Material-Node übereinstimmen –
   Epic RVT-Doku). Offene Rückfrage aus A5 bleibt: ist `RVT_Eldarien_Boden` ein oder zwei Assets? Ein Asset trägt nur einen Material-Typ.
2. Maske: `Mask = saturate((BlendHeight − (AbsoluteWorldPosition.z − LandscapeZ)) / BlendFalloff)`, optional `Power(Mask, Contrast)`,
   multipliziert mit `saturate(dot(VertexNormalWS, up))` (Überhänge bekommen keine Bodenfarbe) und einer world-aligned Noise-Probe (XY,
   20–60 cm Tiling) gegen gerade Kanten. **Startwerte (Richtwert):** BlendHeight 20–60 cm für Blöcke/Steine, 100–200 cm für Hero/Wand/Band;
   Falloff 0,5 × BlendHeight; Contrast 1,5. BlendHeight mit `ObjectScale.z` multiplizieren, damit skalierte Instanzen stimmen.
3. `BaseColor = Lerp(Fels, RVT_BaseColor, Mask)`, Roughness ebenso; Normale: Fels-Tangentnormale per `TransformVector(Tangent→World)` mit
   `RVT_Normal` lerpen (Faktor 0,7 × Mask), dann **Tangent Space Normal = false**. Die Felsnormale aus `VertexNormalWS` bauen, nicht aus
   `PixelNormalWS` (Rückkopplung der Normal-Map, Polycount).
4. **Moos/Schnee-Krone** im selben Material: `UpMask = saturate((dot(VertexNormalWS, up) − Bias) × Sharpness)` (Bias 0,35, Sharpness 4,
   Richtwert) × XY-Noise × (1 − Mask), plus Welthöhenband (nur oberhalb Boden + 0,5 m), damit Moos nicht mit dem Fußblend konkurriert.
   In gletscher/frost/tundra dieselbe Maske mit Schnee statt Moos (Variation per `Per-Instance Custom Data`, da Vertexpaint auf Nanite fehlt).
5. **Dither/Pixel-Depth-Offset:** Für den Fußkontakt reicht die Höhenmaske; ein zusätzlicher PDO (Stärke 2–5 cm am Fuß, Richtwert) weicht die
   Schnittlinie zum Landscape auf, kostet aber Early-Z und ist in Nanite-Materialien nur mit `Pixel Programmable` erlaubt – nicht als
   Default, sondern als A/B-Test. Gedithertes Ausblenden (DitherTemporalAA) wird durch TSR bereinigt (anekdotisch „virtually no cost“, keine
   Messung), erzeugt aber Masked-Shading und bricht den opaken Nanite-Fastpath – nicht empfohlen.
6. **Kosten (Ableitung, nicht gemessen):** drei RVT-Fetches + ein Height-Fetch je Pixel, kein Triplanar auf dem Boden-Layer; Felsalbedo
   UV-gemappt, Moos eine XY-Projektion (volles Triplanar verdreifacht die Samples). Das Felsmaterial schreibt **nicht** ins RVT. Auf Nanite-
   Landscape wird das RVT aus den Nicht-Nanite-Daten gerendert („twice the amount of data is streamed“, Epic), `Virtual Texture Num LODs = 0`.
   Versionsfallen (alle 5.6–5.8, Forum): RVT-Sample im Landscape-Material braucht einen VT-Feature-Switch; RVT bricht mit Nanite-Displacement
   am Landscape; 5.8: Landscape mit `Landscape Layer Blend` + Nanite wird schwarz – vor dem Umbau prüfen.

**Für den Master `M_EL_Klippe_RVT` soll gelten:** Parameter `BlendHeight` (Default 40 cm), `BlendFalloffFaktor` (0,5), `BlendContrast` (1,5),
`NormalBlend` (0,7), `MoosBias`/`MoosSharpness`/`MoosTiling` (0,35 / 4 / 40 cm), `KroneHoeheBand` (50 cm), `SchneeStattMoos` (Static Switch),
`Per-Instance Custom Data 0` = BlendHeight-Skalar je Instanz (Setzer: Hero/Wand/Band 3,0, Block 1,0, Stein 0,6), Custom Data 1 = Moos-Menge.
Als Default-Master für alle Felsnetze der Paletten eintragen (Fab-MSPresets werden bei Plugin-Updates überschrieben – `klippennetze-a5.md`).

## d) Testanleitung

**Lauf.** `python -I scripts/felsgruppen/felsgruppen_plan.py B4 C2 D2 E1 A5 C6 C7 --bild` (Laufzeit im Rauchtest 7–8 s je Feld bei 1136² Fenster
ohne numba). Danach `docs/pruefung/felsgruppen/<Feld>.png` prüfen: rot = Grat, orange = Band, magenta = Wand, hellblau = Fächer, blau =
Blockstrom, gelb = Kuppe, grün = Prallhang, braun = Wände > 50°. Erwartung: rote Gruppen nur auf Kammlinien, orange in Linien gleicher Höhe
mit sichtbarer Neigung, hellblau als Säume unter braunen Flächen, nichts in Talmulden ohne Wand, nichts in Wasser/Weg/Ort.
Seit Korrektur Runde 1 (Abschnitt h): rosa = Klasse `einzel` (Mindestdichte); Log-Zeilen `Overrides <datei> -> …`, `Biome im Fenster …`,
`Mindestdichte …` und `WARNUNG Budget` prüfen; Vergleich ohne Biom-Overrides mit `--ohne-overrides`, eigener Override-Ordner mit
`--overrides-ordner PFAD`.

**Setzen.** Generischer Setzer auf `export/unreal/welt/felsgruppen/<Feld>/`; Einträge mit `rolle: "akteur"` (Dateien `akteur_<Netz>.f32`,
Liste `akteure`) als StaticMeshActor (Ordner `Felsgruppen/<Feld>`, Tag `EL_Felsgruppe`), alle anderen als HISM-Foliage `FT_EL_FG_<Netz>` unter
`/Game/Eldarien/Welt/Foliage/Felsgruppen`; `entfernen`-Filter anwenden (Abschnitt e). Kollision nur wo `kollision: true` (Rollen hero/wand/band/
block mit Höhe × Maßstab ≥ 0,8 m); Sichtweiten aus `sichtweite`.

**Kameras** (Weltkoordinaten cm nach FORMAT §1: X = (j − 4730,5)·100, Y = (i − 4060,5)·100; Feldmitte angegeben, Z = Bodenhöhe + Angabe;
„höchster Punkt“ = Akteur mit größtem z in `plan.json["akteure"]`, oder argmax von `hoehe.f32` im Feld):

| Feld / Lage | Position | Blick | Erfolg erkennbar an |
|---|---|---|---|
| **B4 Grat** (Feldmitte X −321 850, Y −53 250; max 684 m) | höchster Punkt, 180 m seitlich quer zur Gratachse (Richtung = Gratachse + 90°), 40 m über Grund | entlang der Gratachse, 10° nach unten | Kammlinie trägt eine Kette von Gruppen: je ein großer Hauptfels (5–15 m) mit Satelliten, Steine und Kiesel am Fuß; Flanken darunter frei bis zum nächsten Band; keine Reihe auf Terrassenstufen |
| **C2 Kuppel** (X −221 050, Y −254 850; max 475 m) | Fuß der Hauptwand, 250 m vor der Wand, 20 m über Grund (Nachstellung von BERG8_C2) | zur Wand, 15° nach oben | statt ~200 gleich großer Shards 40–80 Gruppen in Bändern gleicher Höhe, gleiche Neigung; Wandnasen (magenta) als große Schalen; unter der Wand ein Schuttsaum mit abnehmender Blockgröße |
| **D2 Doppelkuppel** (X −120 250, Y −254 850; max 446 m) | Sattel zwischen den Kuppeln, 30 m über Grund | auf die höhere Kuppe | Gipfel mit 1–3 eingegrabenen Blöcken (gelb), Grate darunter mit Gruppen, Dünenprofil durch Felskanten gebrochen |
| **E1 Gletscherkamm** (X −19 450, Y −355 650; max 419 m) | höchster Punkt, 150 m entlang des Grats zurück, 30 m über Grund | entlang des Grats | Felsgruppen tragen Schnee nur auf den Oberseiten (Materialmaske), Bänder zeigen Dip in eine Richtung über den ganzen Kamm |
| **A5 Küste** (X −422 650, Y 47 550; max 365 m) | 300 m vor der Steilküste über dem Wasser, 60 m über Meer | zur Wand (Nachstellung von BERG8_A5) | keine schwebenden Stücke; Wandnasen als Nordic-Klippen (Akteure) mit gleichem Streichen; Fächer am Fuß bis zur Wasserkante, 2 m Abstand zum Wasser |
| **C6 Lava-Fuß** (X −221 050, Y 148 350; max 381 m) | Fuß des Vulkanhangs auf dem Lavasand, 10 m über Grund | hangauf, 20° nach oben | Blockströme (blau) aus lava_m_rock mit Steinen, oberhalb Fächer aus lava_s_rock; keine Felsen auf dem flachen Sand ohne Wand darüber |
| **C7 Lava-Kante** (X −221 050, Y 249 150; max 378 m) | Kante der 59 %-Steilzone, 20 m über Grund | entlang der Kante | lava_wall-Nasen als Akteure an konvexen Kanten, dazwischen frei |

An jeder Kamera zusätzlich 2 m und 50 m Nahsicht auf eine Gruppe: keine sichtbare Unterkante (Eingraben), Kiesel bis an den Fels, Bodenfarbe
kriecht 20–60 cm hoch (RVT), Moos nur oben.

**Erwartete Instanzzahlen je Feld** (Spanne; Rauchtest synthetisch siehe unten; Echtdaten können abweichen):

| Feldtyp | Gruppen | hero | wand | band | block | platte | stein | kiesel | Summe | Kollision | Akteure |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Berg 80 % steil (B4, B5) | 2 500–4 000 | 150–300 | 150–300 | 800–1 500 | 1 200–2 000 | 400–900 | 8 000–12 000 | 25 000–40 000 | 40 000–60 000 (gedeckelt) | 2 500–3 000 (gedeckelt) | 150 (gedeckelt) |
| Berg 60–75 % steil (C2, D2, E1, H3, I4) | 1 500–3 000 | 100–250 | 80–200 | 500–1 200 | 800–1 800 | 300–700 | 5 000–10 000 | 15 000–35 000 | 25 000–50 000 | 1 500–3 000 | 80–150 |
| Küste 24 % Land (A5) | 400–900 | 30–80 | 30–80 | 150–400 | 250–600 | 80–200 | 1 500–3 000 | 4 000–10 000 | 6 000–15 000 | 500–1 200 | 40–120 |
| Lava (C6, C7) | 800–2 000 | 50–150 | 40–120 | 100–400 | 500–1 200 | 0 | 2 500–6 000 | 8 000–20 000 | 12 000–30 000 | 700–1 900 | 60–150 |
| Aue/Heide flach (F4, G4, D5) | 20–150 | 0–10 | 0 | 0 | 50–400 | 20–100 | 150–1 000 | 300–2 500 | 500–4 000 | 50–400 | 0–10 |

Für B4/B5 wird das Budget erreicht; dort `--faktor 0.7` fahren (Rauchtest: Faktor 0,5 halbiert die Gruppen, Instanzen 56 k → 33 k).

**Rauchtest (synthetisch, Cloud, Python 3.13, NumPy 2.5, Pillow 12, kein numba).** Mini-Produktionswurzel mit `hoehe.f32` in voller Größe
(memmap 270 MB) und einem synthetischen Grat NE–SW (420 m, scharfer Kamm, zwei Wandstufen, Nebengipfel, Fluss mit Mäander, See, Weg, Ort,
`lage_Fels/Geroell/Schnee`, `eigner.r8` mit zwei Kacheln, `welt.json`, `wasser_welt.json`, 400 Bäume in `bestand/B4`, 30 Felsschalen in
`felsschalen/plan_B4.json`; 31 % der Zellen > 50°). Ergebnis B4: **3 425 Gruppen, 55 856 Instanzen (vor Budget 67 011), 3 000 mit Kollision,
150 Akteure, 111 f32-Dateien, 7,9 s** (Planung 7,3 s). Klassen: grat 575 Gruppen/20 366 Inst., band 813/16 235, wand 142/1 185, fuss 1 585/20 400,
blockstrom 302/8 613, kuppe 1/28, prallhang 7/184; Rollen nach Budget: hero 230, wand 292, band 1 395, block 1 797, platte 676, stein 11 466,
kiesel 40 000. Geprüft: alle f32 mit 10 float32 je Instanz, Quaternionen normiert (Fehler < 1e-7), x/y innerhalb des Feldes, z = −0,3 … 591 m,
Maßstab 0,23–1,89; plan.json mit `dateien`, `akteure`, `entfernen`, `ft_ordner`, `ft_praefix`, `statistik`; PNG 1008 × 1008 erzeugt;
zweiter Lauf byteidentisch (deterministisch); Nachbarfeld B3 bekommt im 64-m-Überlapp dieselben Gruppen (4 208 Instanzen nur im eigenen Feld);
fehlende `hoehe.f32` → klare Meldung, fehlende optionale Raster → Hinweis und Weiterlauf, ungültiges Feld → übersprungen. Die synthetischen
Raster wurden danach gelöscht.

## e) Welche Felsschalen-Klassen entfallen (`entfernen`-Filter)

Die Felsgruppen übernehmen alle **Block-Klassen** der Felsschalen-Foliage, weil deren Netze jetzt in Gruppen mit Eingraben, Richtung und Saum
gesetzt werden und ein Doppelbestand genau die Konfetti-Wirkung verlängert. `plan.json["entfernen"]`:

```
FT_EL_FS_IcelandicBoulder_0,FT_EL_FS_MossyForestBoulder_0,FT_EL_FS_TundraMossyBoulder_01,FT_EL_FS_SandstoneBoulder_0,
FT_EL_FS_RockSandstone_040,FT_EL_FS_namaqualand_boulder_0,FT_EL_FS_mountain_rock_big_02_
```

(Präfixe decken alle Biom-Suffixe `_fjord/_tundra/_gletscher/_frost/…` ab; 23 der 64 `FT_EL_FS_*`-Typen.) **Bleiben vorerst:** die Wand-Schalen
`FT_EL_FS_big_rock_wall_01…03`, `FT_EL_FS_MassiveNordicCoastalCliff_01`, `FT_EL_FS_HugeSandstoneCliff_02/05/07`, `FT_EL_FS_Cliff_01a…e`,
`FT_EL_FS_lava_wall_01/02/09` und die FS-Akteure an Wänden > 55°, bis die Klasse `wand` (Felsnasen als Akteure) und die Klippen-Ebene (A5/B5)
abgenommen sind; dann in einem zweiten Schritt auf **ein Drittel** ausdünnen (Bildkritik Rang 3) und zuletzt entfernen. Begründung: Die
Felsschalen-Schalen tragen an senkrechten Wänden heute die einzige Silhouette; der Felsgruppen-Planer setzt dort nur an konvexen Nasen (Gitter
36 m). Wüste C3–E5: kein `entfernen` (eigener Planer), Faktor 0,4.

## f) Einkaufsliste fehlender Felsassets (Fab/Megascans, Stufe High 4K; Namen sind Fab-Suchbegriffe, da Fab nicht geöffnet werden konnte)

| Asset (Fab-/Megascans-Name) | Stufe | Wofür | Lücke |
|---|---|---|---|
| Megascans „Nordic Rock Cliff“ / „Icelandic Cliff“ (geschichtet, 6–12 m, 2–3 Varianten) | High 4K, Nanite | Klasse band/grat nordisch & tundra: mittelgroße Leisten 4–8 m | heute nur big_rock_wall (3,4 m) und die 7–15-m-Nordic-Klippen; Lücke 4–8 m |
| Megascans „Rock Debris“ / „Rubble Pile“ / „Scree Pile“ (2–4 m Haufen) | High 4K | Fächerstufe 0–16 m, Blockstrom: Schutt als ein Netz statt 5 Instanzen | kein Haufen-Netz im Inventar |
| Megascans „Volcanic Rock Small“ / „Lava Pebbles“ (3–5 Kleinsteine 5–30 cm) | High 2K | Kieselsaum Lava (heute Mountain-SM_stone_0x, Farbe passt nicht) | Lava-Palette ohne Kiesel |
| Megascans „Mossy Rock Cliff“ / „Mossy Boulder Large“ (3–6 m) | High 4K | Hero elfenwald/moos (heute größter Moosblock 2,0 m, HugeMossyForestCliff ist flach) | Hero-Lücke moos |
| Megascans „Snowy Rock“ oder Schnee-Variante über Material | – | gletscher/frost: Schnee-Krone | per `M_EL_Klippe_RVT` (SchneeStattMoos) lösbar, kein Kauf nötig |
| Megascans „Limestone Rock Formation“ (Karst, 5–15 m, mittlere Türme) | High 4K | karst: zwischen Cliff_01 (30–75 m) und Moosblöcken fehlt die Mittelstufe | Lücke 5–15 m dschungel |
| Megascans „Sandstone Ledge Medium“ (3–6 m) | High 4K | band sandstein (heute uk5ebcp/uldubik 0,6–0,8 m hoch) | Bandstufe canyon |

Vor jedem Kauf: Megascans-Asset ggf. schon vor 31.12.2024 beansprucht (dann frei, `boden-kleinzeug-gras.md`); nach Import Post-Import-Pass
aus `klippennetze-a5.md` (Nanite, Kollision Convex, Texturen auf 4K klemmen, `used_with_nanite`).

## g) Offene Punkte / Annahmen

1. **Ungetestet mit Echtdaten.** Schwellen (G ≥ 0,02, M > 0,012, Nase ≥ 0,012, Hangfuß ≥ 0,002 1/m) sind auf synthetischem Gelände abgestimmt;
   bei echten Terrassenresten (A4) kann die Gratstärke Stufenkanten erkennen – dann `kruemmung_sigma_m` auf 12 m und `grat_staerke_min` auf
   0,03 heben, oder die Reststufen vorher glätten (Bildkritik).
2. **Pivot der Mountain_Environment_Set- und Coast_Dunes-Netze** unbekannt (nicht in `netze_masse.json`); Annahme Pivot unten. Lava-Wände
   (`lava_wall_*`) als Mitte angenommen wie die Lava-Felsen. Bei Sichtkontrolle: schwebt ein Block um H/2, Pivot in `netz_pivot_mitte` eintragen.
3. **Schema `wasser_welt.json`/`felsschalen/plan_<Feld>.json`** nur aus FORMAT.md bekannt; der Leser sucht tolerant nach `punkte`-Listen und
   `x/y`-Dicts bzw. 7/10-Tupeln und meldet, wenn nichts gefunden wird. `welt.json["kacheln"]` wird als Liste oder Dict akzeptiert, Rezepte werden
   über Biom-Schlüsselwörter zugeordnet (unbekannte → Feldbiom), mit Hinweis im Log.
4. **Schichtneigung** ist Rauschen auf 512-m-Gitter, keine echte Massiv-Segmentierung; an Massivgrenzen kann das Streichen innerhalb von ~200 m
   drehen. Reicht für die Bildwirkung, ist aber kein geologisches Modell.
5. **Sturzsortierung** (große Blöcke am Haldenfuß) ist umgekehrt zur Auftragsvorgabe; Parameter dokumentiert, Standard = Vorgabe.
6. **Budget-Deckel** greift in Bergfeldern (Kollision 3 000, Akteure 150); gedeckelt wird nach Instanz-Hash, nicht nach Sichtbarkeit. Wenn der
   Setzer Akteure in Packed Level Actors bündelt (A5-Empfehlung), kann `budget.akteure` auf 300 steigen.
7. **Kollisions-Primitive**: `SM_Cliff_01a…e` haben 282–728 Kollisionsprimitive, `SM_MossyForestBoulder_04` 32, `SM_NordicBoulder_01` 20 –
   Post-Import-Pass auf 4–16 Convex-Hulls, sonst Physik-Kosten bei 150 Akteuren je Feld.
8. **Kiesel 40 000 je Feld** sind nahe der Grenze; sobald Runtime-PCG für Kleinzeug steht (Teil B/D), `je_rolle.kiesel` auf 0 und Saum dort.
9. **Abgleich mit `assets-taxonomie.json`** (Teil A, erschien nach Festlegung der Palette): die Taxonomie stuft nach größter Kante
   (z. B. `SM_mountain_rock_big_02_1`, 2,6 m hoch, 4,7 m lang → `fels_hero`), die Palette hier nach **Höhe** laut Auftrag (hero > 3 m,
   block 0,8–3 m, stein < 0,8 m); Kiesel entsprechen dort `ufer_stein`, die Nordic-/Sandstein-Klippen `klippe_schale`. Beides ist konsistent,
   nur anders benannt; aus der Taxonomie übernommen wurden `SM_IcelandicLavaSpire_01…03` (5,0–5,3 m) als Hero für lava und tundra. Nicht
   aufgenommen (bewusst): Bodenplatten-Netze `SM_ForestTerrain_*`, `SM_DryRiverBed_*`, `SM_MossyEmbankment_*`, `SM_sandy_slope_*` (Ufer/Boden,
   keine Felsgruppen).
10. **Nicht geprüft:** Verhalten des `entfernen`-Filters im vorhandenen Setzer (löscht Präfixe nur im Feld?), HLOD-Einbindung der Akteure
   (siehe `hlod-fernansicht-world-partition.md`), Shader-Kosten von `M_EL_Klippe_RVT` (nur Ableitung).

## h) Korrektur Runde 1 (10.10.2026)

Grundlage: `auftraege/verteilung-korrektur-runde1.md`, `antworten/verteilung-KONVENTIONEN.md` (verbindlich), `vorlagen/FORMAT.md`.
Geändert: nur `skripte/felsgruppen_plan.py`, `skripte/felsgruppen_regeln.json` und dieses Dokument (gleiche Dateinamen).

**Echtdaten-Referenz (lokaler Lauf der Vorfassung, Windows, Python 3.11, `python -I -X utf8`):**

| Feld | Biome (biome_je_feld) | Instanzen | Bemerkung |
|---|---|---|---|
| A5 | kueste 75, bergwald 14, aue 11 | 13 311 (65 Akteure) | Erwartung „Küste 24 % Land" 6 000–15 000 – im Rahmen |
| G4 | elfenwald 76, heide 22, aue 3 | 114 | flach (Ø 23 m, 1 % > 30°): wenig Fels richtig, aber keine Moosfelsen im Wald → Mindestdichte (unten) |
| E1 | gletscher 100 | 18 482 | im Rahmen „Berg 60–75 % steil" |
| C6 | lava 99 | 27 357 | im Rahmen „Lava" 12 000–30 000 |

### Änderungen

1. **Biom je Zelle strikt (§1).** `eigner.r8` + `welt.json["kacheln"][k]["rezept"]`; Kennzahl 0 = Weltgelände → `aue` (nicht mehr das
   dominante Feldbiom), Rezept mit „vulkan"/„lava" → `lava`, sonst Biomname im Rezept (z. B. `K6_FJORD` → fjord); unbekanntes Rezept oder
   Kennzahl ohne `welt.json`-Eintrag → `aue` mit Hinweiszeile. Nur wenn `eigner.r8` fehlt: dominantes Feldbiom aus `daten/biome_je_feld.json`
   (Hinweis), fehlt auch das → `biom_zuordnung.fallback_biom` (aue). `welt.json` fehlt/unlesbar → 0 = aue, alle anderen Kennzahlen = Feldbiom
   (Hinweis). Regelblock `eigner0` (Hang-Fallback) entfällt, ersetzt durch `biom_zuordnung`. Als Querschnitts-Planer ist felsgruppen für alle
   15 Biome zuständig (`biome_eigen` = alle 15, kein 2-%-Abbruch, kein Saum nötig); Palette, Biomfaktor, Klassenfaktoren, Klassen-Ausschlüsse,
   Eingraben, Maßstab, Sichtweite und Kieselfaktor werden **je Zelle nach Biom** gewählt (Gruppen werden je Biom statt je Palette erzeugt).
2. **plan.json-Pflichtschlüssel (§2):** `biome_fenster` (Anteile der Landzellen im Fenster Feld + 64 m, Summe 1), `zellen_zustaendig`
   (freie Landzellen im Feld: kein Wasser/Weg/Ort, Hang ≤ 84°), `biome_eigen` (15), `kollision_anzahl`; dazu `biom_quelle`,
   `paletten_je_biom`, `overrides` (aktive Werte je Biom + je Datei gelesene/ignorierte Schlüssel), `hinweise`; `ebene` auch je `dateien`-Eintrag.
   `stand` ist jetzt der Regelstand statt der Uhrzeit → zwei Läufe sind **byteidentisch inklusive plan.json**.
3. **Kollision je Datei.** Kollision ist im Setzer eine Eigenschaft des Foliage-Typs; bisher lagen kollidierende und nicht kollidierende
   Instanzen desselben Netzes in einer Datei (`kollision: true`, wenn eine kollidiert) – im synthetischen B4 hätte der Setzer 4 040 statt
   3 000 Instanzen mit Kollision gesetzt. Jetzt stehen Instanzen mit Kollision in **`<Netz>_kol.f32`** (bzw. `akteur_<Netz>_kol.f32`);
   `kollision_anzahl` = Summe der Dateien mit `kollision: true` ≤ 3 000. **Setzer:** Netz immer über `dateien[...]["pfad"]`, nicht über den Dateinamen.
4. **Budget (§3).** Deckel unverändert hart: 60 000 gesamt, 3 000 Kollision, 150 Akteure, je Rolle (kiesel 40 000, stein 15 000, block 2 600 …).
   Reihenfolge: je Rolle → gesamt (Kleinzeug zuerst) → Kollision (block, band, wand, hero); deterministisch nach Instanz-Hash. Jede Ausdünnung
   → `WARNUNG Budget: … (block>2600: n, kiesel>40000: n, …)` im Log und in `hinweise`, bei Kleinzeug zusätzlich der Hinweis, den Geröllsaum über
   Landschafts-Gras/Bodenlagen Kies/Geröll zu tragen. Neu `budget.ziel` = 52 000: darüber nur Hinweis.
5. **Ausgabe/Robustheit (§5).** Alle `print()` laufen durch `ascii_text()` (ä→ae, ß→ss, →/≤/≥/°/– ersetzt, Rest `?`); auch Tracebacks.
   Pflichtdatei fehlt (hoehe.f32, Regeln, netze.csv, Paletten-Pfade der Grundregeln) → `FEHLER: …`, **Exit-Code 2**. Feld ohne Land → leerer
   plan.json (`instanzen: 0`, keine f32, `hinweise: ["kein Land im Feld"]`); Ausnahme im Feld → Traceback als Log, **leerer plan.json** mit
   `fehler`, weiter mit dem nächsten Feld. Unlesbare optionale JSON (wasser_welt, welt, felsschalen) → Hinweis, weiter.
6. **Biom-Overrides (§4)** und **Mindestdichte** – siehe unten.

### Override-Schema (felsgruppen_overrides)

Zuordnung in `felsgruppen_regeln.json["overrides"]["dateien"]`: nordkueste → fjord/kueste/bergwald, aue → aue, heide_tundra → heide/tundra,
hochgebirge → gletscher/frost, elfenwald, sumpf, dschungel, lava, wueste_ergaenzung → wueste/canyon/oedland. Suche: `--overrides-ordner`, Ordner
der Regeldatei, `<basis>/scripts/<thema>/`, `<Skriptordner>/../<thema>/`; fehlende Datei oder fehlender Block → eine Hinweiszeile, Biom ohne
Overrides. `--ohne-overrides` für Vergleichsläufe. Ein Block wirkt **nur auf die Biome seiner Datei** (fremde Biome werden gemeldet und
ignoriert); **Overrides gewinnen** gegen `felsgruppen_regeln.json`. Netzpfade tolerant (`/Game/` ergänzt, `.Name` entfernt), Pfade nicht im
Inventar → verworfen (gezählt im Log). Gelesen wird (Wert global für die Biome der Datei, als `{biom: wert}` oder in Biom-Unterblöcken):

| Schlüssel (Varianten) | Wirkung |
|---|---|
| `palette` / `biom_palette`: Name, `{rolle: [..]}`, `{biom: …}`, oder `{biom, ergaenzung, neu, <rolle>}` (Schema wie mittelschicht) | Palettenname bzw. Rollen-Netze ersetzen; `ergaenzung`/`paletten_ergaenzung`/`paletten_zusatz` hängen an; `paletten_neu`/`neu` definieren eine Palette (Basis = bisherige Palette des Bioms). Ergebnis heißt `<palette>@<biom>` |
| Rollen-Aliase | `fels_hero`→hero, `fels_block`→block, `fels_stein`→stein, `geroell_platte`/`platte_ersatz`→platte, `klippe_schale`/`wand_palette`→wand, `netze_moosblock`→block, `kontaktzone.geroellsaum_netze`/`kiesel_ring.netze`→kiesel |
| `faktor`/`faktoren`/`biom_faktor` (Zahl, `{biom: zahl}`, `{biom, klassen, kiesel, eingraben, <klasse>}`), `biom_faktor_<biom>` | Biomfaktor (ersetzt); `gruppen_dichte_faktor` multipliziert |
| `klassen_faktor`, `faktor.klassen`, `klassen.<k>.p` (→ p/p_basis), `klassen.<k>.p_faktor` | Klassenfaktor je Biom (multiplikativ) |
| `biom_klassen_aus`/`klassen_aus` (ersetzt), `klassen_erlaubt` (Komplement der 7 Relief-Klassen) | Klassen-Ausschluss je Biom |
| `eingraben`/`eingraben_anteil` [lo, hi]; `rollen.<rolle>.{massstab, eingraben, sichtweite_cm}`; `massstab {rolle: […]}`; `sichtweite {rolle: […]}`; `wand_palette.{massstab, eingraben_anteil, kippen_in_hang_grad}` | Rollen-Parameter je Biom (Rolle > Biom-Eingraben > Klasse > Grundregel) |
| `kiesel_dichte_faktor`, `faktor.kiesel`, `gruppe.kiesel_dichte_je_m2`, `kiesel_ring.kiesel_dichte_je_m2` (→ Verhältnis zu 2,75 /m²) | Kieselfaktor (Dichte und Spanne des Saums) |
| `mindestdichte_je_ha` (Zahl oder [lo, hi] → Mittel), `mindestdichte_klassen`, `klassen.findling_frei.je_km2` (→ /100 je ha, nur wenn keine Mindestdichte gesetzt) | Mindestdichte (Klasse `einzel`) |
| `felder` | Block nur in diesen Feldern aktiv (dschungel: G6, H6, I6, I7 – gilt für den ganzen Block) |

**Stand der echten Blöcke (Lauf 10.10., 13:45; die Biom-Agenten passen ihre Dateien parallel an):**

| Datei | gelesen | ignoriert (geloggt, in plan.json) |
|---|---|---|
| nordkueste | palette.biom, palette.ergaenzung.nordisch, faktor.biom, faktor.klassen, faktor.kiesel, eingraben | palette.bevorzugt, **zusatzklassen (felsufer)**, auflage, kuesten_regel |
| aue | biom_palette, biom_faktor 0,35, biom_klassen_aus, klassen.kuppe.p, klassen.blockstrom.p, rollen.kiesel.sichtweite_cm, rollen.stein.eingraben | übrige klassen-Parameter (hang_grad, hero_p, nur_hoehenstufe, prallhang-Zahlen), lagen |
| heide_tundra | heide/tundra: biom_palette, biom_faktor, biom_klassen_aus, paletten_neu.heide, klassen.kuppe.p, tundra klassen.blockstrom.p_faktor, findling_frei.je_km2 (→ 0,045 bzw. 0,06 /ha) | übrige Kuppen-Parameter, findling_frei-Details, neue Klasse blockfeld, auflage |
| hochgebirge | biom_faktor, biom_palette, paletten_zusatz.tundra (hero/block/platte), klassen fuss/grat p, band/blockstrom p_faktor, gruppe.kiesel_dichte_je_m2 (→ 1,27) | Rolle eis, schneegrenze, lagen, fuss.stufen/faecher_max_m, grat.hero_p, entfernen_zusatz (durch Präfix `FT_EL_FS_mountain_rock_big_02_` schon abgedeckt) |
| elfenwald | biom, palette (5 Rollen), gruppen_dichte_faktor 0,7, mindestdichte_je_ha 1,0, mindestdichte_klassen, eingraben_anteil, massstab, sichtweite, kontaktzone.geroellsaum_netze | nur_wo, gruppe-Zahlen, kippen_in_hang, übrige kontaktzone (Farnring, Moos → Mittelschicht), abstand_zu_baum_m, budget_je_feld, entfernen_witcher_vorschlag |
| sumpf | biom_faktor_sumpf 0,25, klassen_erlaubt (kuppe, prallhang), palette moos, eingraben_anteil, netze_moosblock | moosblock_je_m2_bult |
| dschungel | bedingung.biom, felder, wand_palette (klippe_schale + massstab 0,35–0,8 + eingraben + kippen), fels_hero/block/stein, geroell_platte, sichtweite.block/stein | bedingung.hang_min_grad/wand_min_hoehe_m, schichtneigung_grad, karstfuss, karstplatte, bild_farbe |
| lava | biom, palette lava, biom_faktor 1,6, klassen_faktor, eingraben, platte_ersatz | zone_faktor, kollision_ab_hoehe_m (= global 0,8), kiesel_ersatz (Text), hero_akteure/-punkte |
| wueste_ergaenzung | biom_palette, klassen_faktor, eingraben_anteil, kiesel_ring (Netze, Dichte → 0,44) | schichtung, terrassenkanten, felsnadel, kippen_in_hang, wueste_felder_faktor |

### Mindestdichte (`mindestdichte_je_ha`, neue Klasse `einzel`)

G4 lieferte 114 Instanzen: wenig Fels bei wenig Relief ist richtig, aber im flachen Elfenwald fehlen Einzelblöcke/Moosfelsen. Neu: optional
je Biom `mindestdichte_je_ha` (Gruppen je ha freier Biomfläche im Feld; Richtwert Elfenwald 0,5–2). Nach den sieben Relief-Klassen zählt der
Planer die Hauptstücke je Biom im Feld; fehlt etwas, füllt Klasse `einzel` auf: gejittertes 20-m-Gitter (globaler Hash → nahtlos), Annahme
p = Fehlmenge / freie Gitterpunkte (frei = kein Wasser/Weg/Ort, keine Mulde ohne Wand, keine Wand, Baumsperre 2,5 m, Hang 0–35°), Gruppe =
Block (Hero mit p 0,12) + 0–2 Nebenblöcke + 2–6 Steine + 4–12 Kiesel, Eingraben 35–50 %. `mindestdichte_klassen` (z. B. `["fels_block",
"fels_stein"]`) beschränkt die Rollen (kein Hero; Kieselsaum bleibt). Gesetzt wird der Wert **im Override der Biom-Regeldatei**
(`felsgruppen_overrides.mindestdichte_je_ha`, gewinnt) oder in der Tabelle `mindestdichte_je_ha` von `felsgruppen_regeln.json` (bewusst leer).
In `elfenwald_regeln.json` hat der Elfenwald-Agent inzwischen selbst **1,0 /ha** mit `mindestdichte_klassen: [fels_block, fels_stein]`
eingetragen (nicht von Teil C gesetzt). plan.json: `statistik.mindestdichte` (Soll je ha, Hauptstücke aus Relief-Klassen).

### Rauchtest Korrektur Runde 1 (synthetisch, Cloud, Python 3.13, NumPy, kein numba)

Raster in voller Größe neu erzeugt (memmap), danach gelöscht. **B4** Gebirge wie Abschnitt d, Kacheln jetzt gemischt: bergwald (59 %), fjord
(29 %), Tal mit Kennzahl 0 → aue (9 %), Ecke „Vulkanregion" → lava (3 %). **G4** flacher Wald (Ø 23 m) mit elfenwald (64 %), heide (28 %),
Bachaue mit Kennzahl 0 → aue (8 %), eine Kennzahl ohne `welt.json`-Eintrag, Bach, Weg, **12 000 Bäume** in `bestand/G4`. Overrides aus den
**echten** Biom-Regeldateien in `antworten/skripte/` (alle neun gelesen).

| Lauf | Gruppen | Instanzen | Kollision | Akteure | Zeit |
|---|---|---|---|---|---|
| B4 (Overrides) | 3 259 | 55 196 (vor Budget 66 052; WARNUNG: block > 2 600: 2 440, kiesel > 40 000: 7 754, kollision > 3 000: 662; Hinweis > Ziel 52 000) | 3 000 | 150 (314 kleinste als Foliage) | 7–9 s |
| G4 (Overrides, Elfenwald 1,0 /ha) | 72 (davon 71 einzel) | 1 125 | 51 | 0 | 5–6 s |
| G4 `--ohne-overrides` | 1 | 31 | 3 | 0 | 8 s |
| G4 mit Kopie elfenwald 2,0 /ha (`--overrides-ordner`) | 147 | 2 167 | 104 | 0 | 7 s |

Geprüft: alle Pflichtschlüssel vorhanden; `instanzen` = Summe `dateien.anzahl` = Zeilen der f32; `kollision_anzahl` = Instanzen in Dateien mit
`kollision: true`; `biome_fenster` Summe 1,000 (B4 bergwald 0,592, fjord 0,293, aue 0,088, lava 0,028); `paletten_je_biom` B4 nordisch@bergwald,
nordisch@fjord, moos, lava@lava – G4 moos@elfenwald (MossyForestBoulder/Lichened/Forest_Boulder, Saum SmallStonesPack_02/06), heide (neue
Palette aus heide_tundra), moos; Quaternionen normiert (Fehler ≤ 1,2e-7), alle x/y im Feld; zwei Läufe **byteidentisch (196 Dateien inkl.
plan.json)**; Log und `--help` **reines ASCII**. Randfälle: A1 (kein Land) → leerer plan.json; Z9 → Zeile „Feld uebersprungen"; `eigner.r8`
entfernt → Fallback dominantes Feldbiom (elfenwald 100 %, Hinweis); `welt.json` bzw. `wasser_welt.json` kaputt → Hinweis, weiter;
`hoehe.f32` fehlt → `FEHLER`, Exit 2; dschungel-Block in B4/G4 inaktiv (nur G6/H6/I6/I7).

**Erwartung Echtdaten nach der Korrektur** (nicht gemessen): A5 – die 11 % aue (Weltgelände) bekommen nur noch kuppe/prallhang/blockstrom mit
Faktor 0,35, Rest wie bisher → leicht weniger als 13 311. G4 – plus ca. 70 Einzelgruppen (≈ 0,76 km² Elfenwald × 1 /ha) ≈ 1 000–1 500
Instanzen. E1 – gletscher-Overrides (Faktor 1,3, fuss ×1,56, blockstrom ×1,4, Kiesel ×1,27) → spürbar mehr als 18 482, Kollisionsdeckel
wahrscheinlich. C6 – lava-Overrides (Faktor 1,6, blockstrom ×2, fuss ×1,6) → deutlich mehr als 27 357, Deckel (Kollision 3 000, ggf. block
2 600) greift mit WARNUNG; falls zu dicht, im lava-Override `biom_faktor` senken statt hier.

### Offene Punkte aus Runde 1

1. **`nordkueste … zusatzklassen.felsufer`** (bisher Schicht 5 des Nordküsten-Planers: Fjord-Felsufer-Blöcke > 0,8 m mit Kollision, 0–14 m
   hinter der Wasserlinie, Hang 14–60°, Dichte 0,008 /m², Klumpung) wird **nicht** gelesen (Auftrag: nur Palette/Faktoren). Da felsgruppen laut
   §4 der einzige Planer für Felsen > 0,8 m ist, fehlen diese Blöcke, bis entschieden ist: (a) Klasse `ufer` hier nachrüsten (Küstenabstand aus
   `karte_wasser`/Meer, Rest wie `einzel`) oder (b) felsufer bleibt im Nordküsten-Planer als Ausnahme. Entscheidung Koordination.
2. Neue Klassen anderer Biome werden ignoriert: heide_tundra `blockfeld` (Felsenmeer), wueste `terrassenkanten`/`felsnadel`, dschungel
   `karstfuss`/`karstplatte`, lava `hero_akteure` (Spires), hochgebirge Rolle `eis`. Kandidaten für eine Runde 2 (je eine Klasse nach dem Muster
   von `einzel`).
3. Strikte Zuordnung 0 → aue: steile Weltgelände-Zellen verlieren grat/band/wand/fuss (aue-Override schaltet sie ab). Laut `biome_je_feld`
   sind die Bergfelder fast vollständig mit Kacheln belegt (B4 bergwald 100 %), das Risiko ist klein; bei Sichtkontrolle in A5 (aue 11 %) prüfen.
4. Dateinamen `<Netz>_kol.f32` neu: Setzer muss das Netz aus `pfad` lesen (tut er laut FORMAT §3 ohnehin) und je Datei einen Foliage-Typ
   anlegen (`FT_EL_FG_<Datei>`).
5. Abschnitt g Punkt 1 und 3 sind überholt: die Vorfassung lief mit Echtdaten; unbekannte Rezepte gehen jetzt auf aue (nicht Feldbiom).
