# Verteilung Biomgruppe 5: Elfenwald (alter Laubwald mit Lichtungen, Elfenruinen)

**Auftrag 11, Teil B5.** Biom `elfenwald`, Foliage-Präfix `FT_EL_EW_`, Ordner `/Game/Eldarien/Welt/Foliage/Elfenwald`. Stand 2026-10-10
(Fortsetzung nach API-Abbruch; Regeln und Planer-Entwurf des Vorgängers geprüft, korrigiert und rauchgetestet). Lieferung: dieser
Bericht, `skripte/elfenwald_regeln.json` (8 Baumklassen + 26 Streuklassen in 4 Schichten, 247 eindeutige Netzpfade, alle gegen
`netze.csv` geprüft, 0 fehlend), `skripte/elfenwald_plan.py` (1 179 Zeilen, FORMAT §3/§5). **Alles UNGETESTET MIT ECHTDATEN** – in der
Cloud nur mit synthetischen Rastern (G4, §5) rauchgetestet. Web-Quellen waren nur als Suchmaschinen-Auszüge lesbar (6 WebSearch-Läufe,
mode extended); solche Belege sind mit **[Suchauszug]** markiert, Zahlen ohne Beleg mit **Richtwert**.

Felder (laut `biome_je_feld.md`): **G3** (elfenwald 97 %, Land 72 %, Laub 56 %), **H3** (100 %, Land 89 %, 60 % steil, Fels 26 %),
**G4** (76 % + heide 22 %, Land 100 %, Laub 75 %, Moos 6 %, Wasser 5 %), **H4** (82 % + aue/sumpf, Land 100 %, 33 % steil), **I4**
(bergwald 78 / elfenwald 21), **H2** (kueste 78 / elfenwald 20), **G2** (Land 4 %). Der Planer läuft je Zelle mit Biomfaktor (elfenwald
1,0; bergwald 0,6; aue 0,5; sumpf 0,35; kueste 0,3; heide 0,25; alles andere 0) aus `eigner.r8`/`welt.json`; Kennzahl 0 und fehlende
Datei → dominantes Feldbiom aus `feld_biom_fallback` (I4 bergwald, H2 kueste, G2 aue, sonst elfenwald).

---

## 1. Witcher-Analyse: Waldpfad, Laubwälder von Velen/Toussaint, Elfenruinen

**witcher_03 (Waldpfad, Kovir-Techdemo).** Das Bild ist zu etwa 60 % mit Objekten zwischen 0,3 und 3 m Höhe gefüllt, obwohl es ein
„Baumbild“ ist: rechts ein Fichtenast als Vordergrund (1–2 m vor der Kamera), links ein liegender Stamm und ein Wurzelteller, am Hangfuß
drei junge Fichten (1,5–3 m) und ein Felsblock-Trio (0,8–2 m), dazwischen Kopfsteine 10–40 cm, Grasbüschel und Schneereste in den Rinnen.
Die Bäume stehen in zwei Höhenklassen (Hero-Fichten 25–30 m im Mittelgrund, 8–12 m am Hang), der Pfad selbst ist nackter Boden mit
Kieseln, keine Textur ohne Objekt. Auf 10 m um die Kamera stehen geschätzt **4–5 Objekte je 100 m²** in der Mittelschicht (Zählung in
`verteilung-leere-fuellen.md` §1). Das ist die Messlatte: **kein Blick ohne Objekt in 0,5–3 m innerhalb 10 m.**

**Velen/Toussaint (W3 Next-Gen).** Belegbar nur indirekt: Velens Wälder sind Mischbestände verschiedenen Alters mit Kronenlücken, in denen
Jungwuchs und blühende Sträucher stehen, Vorbild Białowieża **[Suchauszug Kotaku]**; Kräuter wurden nach ihren natürlichen Standortansprüchen
gesetzt **[Suchauszug VICE]**; Toussaint-Laubwälder sind SpeedTree-Bestände mit zusätzlichen Arten **[Suchauszug SpeedTree]**; das REDkit-
Vegetation-Edit-Tool platziert per Pinsel je Geländetyp, nennt aber keine Dichten. Es bleibt die Bildauswertung (`bildkritik-witcher-messlatte.md`
Rang 4): 2–3 Arten, Höhenvarianz 0,7–1,3, Clumping mit 15–25 % Lichtungen, Waldkanten-Falloff 30–60 m, Totholz 2–3 %, Farbinseln.

**Elfenruinen (Aen Seidhe).** Elfenarchitektur ist „elegant, organisch, asymmetrisch“, Bauten „verschmelzen mit der Umgebung“, Ornamente mit
Ranken- und Baummotiven **[Suchauszug historicalgames.net]**; Beispiele Termes, Arthach, Ruinen am Wyndamer-See **[Suchauszug Witcher-Wiki]**.
Spielerisch immer Blickziel plus Kleinraum: Säulenreihe oder Bogen auf Kuppe/Hangschulter, halb im Boden, Efeu, Moos am Fuß, Bruchsteine
(ein Modder-Breakdown nennt genau diese Moos-/Rissstein-Schichten als das, was den Spielruinen fehlte **[Suchauszug Patreon BetterRuins]**).
Kein Zaun, kein Karren: der Elfenwald ist unbewohnt, seine Spuren sind Ruine, Schrein, Steinmann, Hügelgrab.

**Witcher-4-Techdemo (Kovir).** Nanite Foliage mit modellierten Blättern und voxelisierten Kronen, 60 fps auf PS5 **[Suchauszug PlayStation
Blog, Game Informer]** – keine Dichtezahlen; Grenze ist bei uns der Setzer (60 000 je Ebene), nicht die GPU.

**Botanik als Zahlenquelle (für Lückenanteil und Jungwuchs).** Urwald-Buchenbestände haben Lückenanteile von 3–11 % der Fläche (Slowenien,
Kopa 3,2→4,5 %, Gorjanci 9,1→10,6 %) **[Suchauszug PLOS ONE 2013]**; in Karpaten-Tannen-Buchen-Urwäldern 11,3 % Lücken bzw. 37,9 % erweiterte
Lücken **[Suchauszug Springer]**; Jungwuchs keimt bevorzugt an Lückenrändern und unter halbgeschlossenem Dach, nicht in der Lückenmitte
**[Suchauszug Oxford Forestry]**; Totholz 115 m³/ha im Urwald Sitno **[Suchauszug MDPI Forests]**. Daraus: Lichtungsziel 15–25 % (Spiel
liest besser als Urwald, Bildkritik), Jungbäume ×3–4 am Lichtungsrand, Farn/Moos/Pilze mit Beschattung steigend.

**Was heute in G3/G4 fehlt (Ist-Bilder).** `KLEIN12_G3_boden`: braune Laubtextur, gleich große Sprösslinge, ein roter Strauch, eine
aufliegende Platte ohne Laubkante; keine Zweige, Äste, Wurzelanläufe, Farne, Moospolster, Pilze; Buchenstämme ohne Fuß. `W6FIN_G3_rundgang`:
eine Art, eine Höhe, harte Waldkante, keine Lichtungen, roter Boden zwischen den Kronen. Der Elfenwald-Planer liefert genau die fehlenden
Stufen (Schichten 0 und 1, Bachsaum) und – wo keine Bestand-Ebene liegt – einen Altersmix-Bestand mit Lichtungen.

**Quellen (6 WebSearch-Läufe, nur Suchauszüge):** Kotaku „There's Real History, And Beauty, In The Witcher 3's Forests“ · VICE „Designing the
World of The Witcher 3“ · SpeedTree „The Witcher 3: Blood and Wine“ · REDkit-Wiki „Tools“ (Vegetation Edit Tool) · historicalgames.net
„Echoing the Past: Spoliation, Memory, and Power in the Witcher 3“ · Witcher-Wiki „Elven Sanctuary Ruins“, „Elven ruins near Lake Wyndamer“ ·
Patreon „Elven ruins from The Witcher 3 – Build Breakdown“ · PlayStation Blog / CDPR / Game Informer zur W4-Techdemo (2025) · PLOS ONE
10.1371/journal.pone.0052641 (Gap Dynamics Slovenia) · Springer 10.1007/s10342-009-0322-2 (Carpathian gaps) · Forestry 80(4):431 (Gap
regeneration) · MDPI Forests 11(1):81 (Sitno deadwood). Keine Quelle nennt Instanzen je m²; alle Dichten unten sind Richtwerte aus den
Zielbildern und dem Teil-D-Befund.

---

## 2. Regelwerk (`elfenwald_regeln.json`) – je Schicht mit Zahlen

Dichten sind Instanzen je m² als Paar **[offen, voll beschattet]**, linear über die Beschattung interpoliert. Beschattung = 1 − exp(−1,4 ·
π·5² · Kronendichte), Kronendichte = Baumpositionen (Gewicht Maßstab²) mit Gauß σ = 6 m geglättet (wie Teil D, k 1,4 statt 1,6: Hainbuche/
Buche sind dichter als Kiefer, die Schwelle greift früher). Wald = Beschattung > 0,35; Lichtung = Beschattung < 0,18 innerhalb 40 m der
Waldkante; Saum 15 m nach innen / 10 m nach außen; Lichtungsrand = Lichtungszellen ≤ 8 m zur Kante. Feuchte = 0,8·(1 − d_Wasser/30 m) +
0,7·Moos + 1,0·Schlamm + 1,0·Algen + 0,3·Lehm + 0,15·Erde (0–1). Hang voll bis 22°, dann linear 0 bis `hang_max` je Klasse. Mulde =
Laplace der 4-m-geglätteten Höhe > 0,015 (Senken bekommen Laub ×1,8, Farn ×1,4, Moos ×1,3, Pilze ×1,5). Wegrand 2,5–8 m: Blumen ×2,
Farn ×1,4, Hochstauden ×1,8, Laub ×0,6 (Elfenpfad: Blüten statt Kies). Sperrflächen: Wasser (+0,5 m), Weg 2,5 m Kleinzeug / 4 m Große,
Ort 5 m, vorhandene Nicht-Baum-Instanzen 1,2 m, Baumstämme 1 m; neue Bäume 6 m von Bestand-Bäumen.

### Schicht 2 Baum (Modus `auto`: `ergaenzen` wenn `bestand/<Feld>/plan.json` existiert, sonst `voll`)

| Klasse | Netze | Dichte je m² | Jitter-Raster | Maßstab | Kippen | Eingraben | Besonderes |
|---|---|---|---|---|---|---|---|
| hero | Hornbeam_Field_01/02, beech_tree_06/07 | 0,00003 | 40 m | 1,25–1,55 | 0 | 25 cm | nur Lichtungsrand ×12, Saum ×6, Abstand 10 m, Kollision |
| alt | Hornbeam_Field_03/04, Forest_01/02/04, beech_tree_04/05/08/09 | 0,0062 | 7 m | 0,95–1,25 | 0,05 | 20 cm | Fels ×0,3, Abstand 3 m, Kollision |
| mittel | Hornbeam_Forest_03/05–08, beech_tree_02/03 | 0,0090 | 5 m | 0,85–1,12 | 0,05 | 15 cm | Lichtungsrand ×1,2, Abstand 2,2 m, Kollision |
| jung | Hornbeam_Forest_09/10, beech_tree_00_C/D, 01 | 0,006 / 0,0018 | 3,5 m | 0,7–1,05 | 0,08 | 8 cm | Lichtungsrand ×3, Saum ×2,5, ohne Kollision |
| pappel | Poplar_06/07_Forest, 03_Medium, 04_Small | 0,0012 / 0,0005 | 9 m | 0,85–1,15 | 0,03 | 20 cm | Feuchte 0,5→2,2, Lichtungsrand ×2,5, Fels 0 |
| birke | Big_Tree_birch_01 | 0,0008 / 0,0002 | 9 m | 0,8–1,15 | 0,05 | 12 cm | Saum ×3, Kies ×1,5 (Herbstakzent) |
| weide | Big_Tree_willow_01/02 | nur Bachband 3–14 m: 0,0025 | 10 m | 0,8–1,1 | 0,05 | 15 cm | Hang < 25° |
| tot | EuropeanBeech_Dead_XL/M, DeadTree_01/02, Graveyard Dead_Tree_01/03 | 0,0004 / 0,0005 | 12 m | 0,9–1,3 | 0,10 | 15 cm | Lichtung ×0,4, Kollision |

Klumpen: Wertrauschen (Hash der Weltkoordinate, nahtlos) mit Wellenlängen 48 m (0,65) + 16 m (0,35); Zellen < 0,34 sind Lichtung (Dichte
×0,03), darüber steigt die Dichte linear von 0,7 auf 1,6. Gruppen 8–40 m ergeben sich aus den Wellenlängen. Höhe: ab 350 m linear
abnehmend, 0 ab 600 m. Artenmix bei `voll` (Rauchtest, synthetisches G4): Hainbuche/Buche alt 31 %, mittel 37 %, jung 24 %, Pappel 3 %,
Birke 3 %, tot 1,7 %, Hero 0,5 %, Weide < 0,3 %. Bei `ergaenzen` (G4 mit `FT_EL_BST_*`) werden **nur** Hero-Altbäume (0,35/ha: ×8 am
Lichtungsrand des vorhandenen Kronendachs, ×0,5 in Lichtungen, ×0,15 im Wald) und stehendes Totholz (0,45/ha) ergänzt, 7 m Abstand zum
Bestand; erwartet 30–120 Stück je Feld.

### Schicht 1 Mittelschicht 0,3–3 m (Standard `--mittel zusatz`, siehe §4)

| Klasse | Netze (Auszug) | Dichte je m² | Gruppe / Radius | Maßstab | Steuerung | Sichtweite |
|---|---|---|---|---|---|---|
| farn (Farninsel) | Fern_01–06, SilverLadyFern_01–03, BeechFern_09/10/15 | 0,003 / 0,034 (×0,45 im Zusatz) | 6–18 / 3,5 m | 0,8–1,45 | Lichtung ×0,15, Feuchte 0,5→1,9, Moos ×1,6, Mulde ×1,4 | 300 m |
| adlerfarn | EagleFern_M_01, S_01/02/04 | 0,009 / 0,002 | 8–25 / 5 m | 0,9–1,5 | Saum ×2, Lichtungsrand ×3, Gras ×1,3 | 300 m |
| beere (Heidelbeere) | billberry_01–03 | 0,002 / 0,016 | 8–24 / 3 m | 0,9–1,4 | Lichtung ×0,2, Moos ×1,8 | 150 m |
| grashorst | GrassyEmbankment_01/02 | 0,0025 / 0,0004 | 1–3 / 1,5 m | 0,9–1,4 | Moos ×1,8, Mulde ×1,5, Feuchte 0,7→1,6 | 200 m |
| blume_lichtung | WhiteWindflower ×5, LilyOfTheValley ×3, Periwinkle ×3, YellowArchangel ×2 | 0,010 / 0,001 | 10–30 / 4 m | 0,9–1,4 | Lichtung ×2, Lichtungsrand ×2, Wegrand ×2, Hang < 30° | 120 m |
| efeu | Ivy_09–22, EnglishIvy_01/05/08 | am Stamm: 6 % der alt/hero/tot-Bäume, Ring 0,35–0,6 m | 1 | 0,9–1,4 | Yaw zum Stamm, Kippen 0 | 200 m |
| jungbaum | Hornbeam_Sapling_01–07, Seedling_01/02, beech_plant_01–03 | 0,009 / 0,003 (nur `voll`) | 2–6 / 2,5 m | 0,8–1,3 | Saum ×3, Lichtungsrand ×4, Lichtung ×0,7 | 350 m |
| strauch | Elderberry_05–12, hazel_01/02, black_cherry_02/03, maple_bush_02/03 | 0,008 / 0,002 (nur `voll`) | 1–3 / 2,5 m | 0,8–1,4 | Saum ×3, Lichtungsrand ×2,2 | 350 m |
| stamm_liegend | MossyTree_01, LargeFallenTree_01/02, OldFallenTree_01/02, FallenTreeAssembly, dead_log_01/02/04 … | 0,0008 / 0,0016 (nur `voll`) | 1 | 0,9–1,35 | längs Hang ±20°, Eingraben 12 cm, **Kollision** | 500 m |
| stumpf | TreeStump_01, RottenTreeStump_01/02, BirchTreeStump, BrokenStump, stump_03 | 0,0005 / 0,0010 (nur `voll`) | 1 | 0,85–1,4 | Eingraben 8 cm, **Kollision** | 400 m |
| grasbueschel | grass_01/02/03 (Forest), grass_clover_01 | 0,025 / 0,003 (nur `voll`) | 3–9 / 2 m | 0,8–1,5 | Gras/Wiese ×2, Lichtung ×1,5 | 150 m |
| hochstaude | nettle_01_0/1 | 0,008 / 0,002 (nur `voll`) | 4–12 / 2,5 m | 0,9–1,4 | Saum ×2,5, Feuchte 0,5→2,0, Erde/Lehm ×1,6 | 150 m |

### Schicht 0 Boden

| Klasse | Netze | Dichte je m² | Gruppe / Radius | Steuerung | Sichtweite |
|---|---|---|---|---|---|
| laubhaufen | DeadLeaves_01/05/12/13/14, poplar_leaves_01/02, detail_leaves_01/03 | 0,006 / 0,024 | 3–8 / 2 m | Laub ×1,6, Mulde ×1,8, nah Baum (3 m) ×1,4, Lichtung ×0,4 | 60 m |
| zweige | WoodenSticksAndTwigs_01–09 (7), DryBranches_01/04/05/07 | 0,004 / 0,014 | 2–5 / 1,5 m | Laub ×1,3, nah Baum ×2 | 70 m |
| ast | OldTreeBranch_01/04/05, BrokenTreeBranch_01, OakBranch_01, branch_01_1/2, detail_branches_02 | 0,0012 / 0,0035 (nur `voll`) | 1 | Laub ×1,2, nah Baum ×1,6 | 120 m |
| pilz | mushroom_01/02 | 0,0002 / 0,003 (×0,4 im Zusatz) | 3–9 / 0,9 m | an Totholz ×4, Moos ×1,6, Feuchte 0,5→2,2, Lichtung ×0,1 | 60 m |
| wurzel (Wurzelanlauf) | beech_old_roots_01, MossyForestRoots_01–03, ForestRoots_01/02, crooked_root_01 | 30 % der alt/hero/tot-Bäume, max 2, Ring 0,7–2,2 m | 1 | Yaw radial vom Stamm, Kippen 0,8, Eingraben 6 cm | 150 m |
| moos | CustomMoss_01–05, moss_01/02 | 0,003 / 0,020 | 4–12 / 1,5 m | Moos ×2,5, Fels ×1,4, an Totholz ×3, Feuchte 0,6→1,8, Hang bis 45° | 50 m |
| kraut (Sauerklee/Klee) | Violet_Wood_Sorrel VarA/B/D/F/H, CloverVarieties_01–03 | 0,004 / 0,016 | 6–16 / 2 m | Moos ×1,3, Wegrand ×1,3, Feuchte 0,7→1,6 | 70 m |
| stein_klein | MossyForestRock_01, SmallStonesPack_01/03/05/07, stone_03/04/06 | 0,0015 / 0,003 | 2–6 / 1,2 m | Kies/Fels/Geröll ×2,5–3, Hang bis 45°, Eingraben 4 cm, Kippen 1,0 | 80 m |

### Schicht 5 Wasserkante (Bachsaum; Fluss/See ×0,3, dort bleibt `FT_EL_UF_*` führend)

Bach = Wasserzellen, deren lokale Halbbreite (Distanz zum Nichtwasser, Maximum im Umkreis 8 m) ≤ 4 m ist. Band 0,5–6 m vom Wasser, Dichte
fällt linear vom Innen- zum Außenwert: moosstein_bach (MossyForestRock_01–03, MossyRocks_01/02, MossyForestBoulder_02/05/06/07,
LichenedForestBoulder_01) 0,08→0,015, Gruppen 2–5, Maßstab 0,6–1,4, Eingraben 18 cm, Kippen 1,0; embankment (MossyEmbankment_01/02,
ForestRockShelf_01) 0,012→0,002 nur bei Hang 18–60°, Eingraben 30 cm; farn_ufer 0,06→0,012 (0,8–6 m); schachtelhalm (rough_horsetail_01–03)
0,05→0,004 (0,5–3,5 m, Schlamm ×1,8); binse (ToadRush_00/01/02/012) 0,03→0,002 (0,5–2,5 m, Hang < 20°); moos_ufer 0,08→0,01 (0,5–3,5 m).
Alles ohne Kollision, Sichtweiten 50–300 m.

### Budget und Priorität

Ziel je Schicht: Boden 52 000, Mittel 48 000, Baum 22 000, Wasserkante 15 000 (Obergrenzen 60 000 / 20 000). Bei Überschreitung dünnt der
Planer die Klassen von hinten in der Prioritätsliste (Boden: wurzel > ast > stein > pilz > zweige > kraut > moos > laubhaufen; Mittel:
stamm > stumpf > strauch > jungbaum > farn > adlerfarn > efeu > hochstaude > beere > blume > grashorst > grasbueschel) mit einem
gemeinsamen Hash-Faktor, bis das Ziel erreicht ist. Kollision: Schichten 1/5 (liegende Stämme, Stümpfe) ≤ 3 000 je Feld; die Baumschicht
hat ein eigenes Budget `kollision_baum_je_feld` = 20 000 (wie die Bestand-Ebene mit 17 000 Bäumen in G4 – Bäume ohne Kollision sind kein
Spiel). Setzt man es auf 3 000, bekommen nur hero/tot/alt Kollision (Reihenfolge der Prioritätsliste), die übrigen Klassen `kollision:false`.

---

## 3. Overrides für Teil C und Teil D (nur JSON, keine Instanzen aus diesem Planer)

**Moosfelsen (`felsgruppen_overrides`, für `felsgruppen_plan.py`).** Im Elfenwald sind Felsen bemooste Granit-/Gneisblöcke im Laubwald,
keine Wände und keine Schuttfächer (Ausnahme H3/H4 mit Fels-Lagen > 25 %). Palette: Hero `Mossy_Rock_Formation_plFhY`,
`MossyForestBoulder_04`, `TundraMossyBoulder_01`; Block 11 Netze (`MossyForestBoulder_01/03/05/06/07`, `MossyRockFace_02`,
`Forest_Boulder_wgosajs`, `Forest_Rock_wjxqcct`, `Japanese_Mossy_Boulder_veqhehl`, `Nordic_Forest_Rock_Small_xjijbgx`,
`LichenedForestBoulder_01`); Stein `MossyForestRock_01/02`; Platten `MossyRocks_01/02`, `ForestRockSlab_01`, `ForestRockShelf_01`,
`ForestRockFormation_01/02`, `MossyEmbankment_01/02`; Schale nur `HugeMossyForestCliff_01`. Gruppendichte ×0,7, nur Hang ≥ 12° oder
Kuppe oder Bach-Prallhang, keine Mulden ohne Wand. Gruppe = 1 Hauptfels + 2–5 Nebenblöcke + 4–10 Schutt + 10–30 Kiesel, Hauptrichtung
±15°, Eingraben 35–50 % (tiefer als im Gebirge: der Waldboden ist weich), Kippen voll in den Hang. Kontaktzone: Geröllsaum 0,6/m² im Ring
0,5–2 m (`MossyForestRock_01`, `SmallStonesPack_02/06`), Farnring 2–6 nur auf der Schattseite (`SilverLadyFern_02`, `Fern_04`,
`BeechFern_10`), Moos am Fuß 4–10 (`CustomMoss_02/04`), RVT-Fußblend 30–60 cm, Auflage-Material Moos 0,85 / Flechte 0,2 / Schnee 0.
Abstand zu Bäumen 2,5 m; Budget 120 Akteure + 6 000 Foliage je Feld; Sichtweiten Hero 0, Block 500 m, Stein 200 m, Platte 350 m.

**Ruinen/Schreine (`spuren_overrides`, für `spuren_plan.py`).** Aus: Zaun, Feldstreifen, Obstgarten, Karren, Holzschlag, Köhler, Rauch,
Steg, Mauer. Stattdessen: **Ruine** 1–3 Gruppen je Feld à 3–8 Stücke im Radius 6–18 m, Lage Kuppe/Hangschulter < 12°, 20–80 m vom Weg,
nicht im Ort (+30 m), ≥ 10 m vom Wasser, Beschattung 0,3–0,7 (im Wald mit Lichtschneise); Foliage `SM_Column_02/03`, `SM_Wall_02`; Akteur
`SM_Main_Arch_01` (529 640 Dreiecke, je Feld ≤ 1) und `SM_Wall_01` (372 163 Dreiecke, ≤ 2); Eingraben 15–35 %, Kippen 2–8°, gemeinsame
Hauptrichtung ±12°, Säulen in Reihe 3–4 m; Bewuchs: Efeu an 40 % der Wände (`Ivy_11/17/21/25`), Moos 6–12 je Stück, Farn 2–5, Bruchsteine 3–8.
**Schrein** 1–2 je Feld: `SM_Sviatovid_Stone` an Wegkreuzung oder Bachquerung (Weg dilatiert 6 m ∩ Wasser), 2–4 m neben dem Weg, unter
Altbaum oder vor Hero-Fels, Beigaben 6–12 Kiesel + 8–16 Blumen (`LilyOfTheValley_02`, `WhiteWindflower_04`); `SM_Cross` (christlich) nicht
im Elfenwald. **Steinmann** 2–6 je Feld an Wegen auf Kuppen/Lichtungsrändern, 4–7 Steine. **Hügelgrab/Steinkreis** 0–1 je Feld in der
Lichtungsmitte (Hang < 6°, ≥ 40 m vom Weg), 7–12 Moosblöcke im Radius 4–7 m, Blumeninsel innen ×3. Der Elfenwald-Planer liefert die
Standorte als `blickziele` in `plan.json` (größte Lichtung mit Radius, Kuppe nahe Weg, Bachquerung) – im Rauchtest: Lichtung r = 36 m bei
X 1 391 / Y −863 m, Schrein an der Bachquerung X 1 734 / Y −548 m.

---

## 4. Abgrenzung zu vorhandenen Ebenen

**`FT_EL_BST_*` (Bestand, G4 gesetzt, 17 000 Bäume).** Bleibt. Der Planer erkennt `bestand/G4/plan.json`, liest alle Baumpositionen
(Feld + 8 Nachbarn, nur im Fenster) für das Kronendach, hält 6–7 m Abstand und ergänzt nur Hero-Altbäume und stehendes Totholz (§2).
In G3/H3/H4/I4/H2/G2 (keine Bestand-Ebene) liefert er den Bestand selbst (`voll`) und setzt dann `entfernen` auch für Witcher-Haine
(`sm_europeanhornbeam_field_0`, `sm_beech_tree_0`, …) – nur für Präfixe, die laut `witcher/<Feld>/plan.json` dort wirklich vorkommen.
Will man G4 ebenfalls vom Elfenwald-Planer bestücken: `--baum voll` setzt `entfernen` für die Bestand-Netze (Rauchtest: 13 519 Bäume,
Lichtungsanteil 19 %, Beschattung 0,67).

**`FT_EL_WIT_*` (Witcher-Bewuchs).** Die Witcher-Ebene streut im Elfenwald generische Farne, Laub, Zweige, Gebüsch, Totholz, Blumen und
Namaqualand-Netze ohne Beschattungs-, Saum- und Feuchte-Regel. Alle Nicht-Baum-Rollen, die der Elfenwald neu setzt, kommen in den
`entfernen`-Filter (57 Präfixe in der JSON; wirksam nur die im Feld vorhandenen – Rauchtest G4: `sm_fern_0,sm_mossytree_01`). Die
Witcher-Haine bleiben, solange der Planer selbst keine Bäume liefert.

**Teil-D-Mittelschicht (`mittelschicht_plan.py`, `FT_EL_MS_*`).** Teil D liefert im Elfenwald bereits farn 0,006/0,022, strauch 0,014/0,005,
jungbaum 0,010/0,003, hochstaude 0,008/0,010, grasbueschel 0,012/0,002, totholz 0,0006/0,0022, stumpf, ast 0,004/0,010, wurzel, pilz
0,002/0,010, kletter, totbaum. Damit nichts doppelt steht, läuft der Elfenwald-Planer standardmäßig mit **`--mittel zusatz`**: Klassen
strauch, jungbaum, hochstaude, grasbueschel, stamm_liegend, stumpf und ast entfallen (Faktor 0 in `teil_d.zusatz_faktor`), farn ×0,45 und
pilz ×0,4 bleiben als Verdichtung. Der elfenwaldspezifische Zusatz ist: **Farninseln** (6–18 Stück, Radius 3,5 m, nur Schatten/Mulde/
Feuchte – Teil D streut Farn gleichmäßig), **Adlerfarn** am Lichtungsrand, **Heidelbeere** (Teil D: „–“), **Grashorste**, **Lichtungsblumen-
Inseln**, **Efeu und Wurzelanlauf am Stamm** (Teil D streut Efeu/Wurzeln frei), dazu die komplette Bodenschicht (Laub, Zweige, Moos,
Sauerklee, Kleinsteine) und der Bachsaum, die Teil D nicht hat. `--mittel voll` nur, wenn `mittelschicht_plan.py` in den Elfenwald-Feldern
nicht läuft. Rauchtest-Differenz (dichter Synthetik-Bestand): Mittelschicht 24 839 (zusatz) gegen 48 019 nach Budget (voll, 68 388 vor
Ausdünnung).

**`FT_EL_UF_*` (Ufer, 5 Felder)** bleibt an Fluss/See führend (Wasserkante ×0,3); am Bach (Halbbreite ≤ 4 m) setzt der Elfenwald den
Saum voll. **Felsschalen/Klippen** werden nicht berührt (Fels ist Teil C).

---

## 5. Testanleitung

**Rauchtest Cloud (gelaufen).** Synthetische production-Wurzel: `hoehe.f32` in voller Größe 7 057 × 9 577 (memmap, nur das G4-Fenster + 64 m
beschrieben: Relief 15–45 m, Bachtal, Kuppe NW, Gefälle nach Osten), `karte_wasser.r8` (Bach 3–5 m breit, Teich 60 × 90 m), `karte_weg.r8`
(Weg N–S, kreuzt den Bach), `karte_ort.r8`, `eigner.r8` + `welt.json` (Kachel 7 elfenwald, 9 heide in der SO-Ecke, 0 im Norden),
`lage_Laub/Moos/Gras.r8`, `bestand/G4` (1 938 bzw. 11 064 Bäume in Gruppen 12–28 m mit drei Lichtungen 38–60 m), `witcher/G4`
(300 Farne + 50 Moosstämme), `daten/netze.csv`. Python 3.13, NumPy 2.5, ohne numba, 4 Kerne.

| Lauf | Instanzen gesamt | Boden | Mittel | Baum | Wasserkante | Kollision Baum / andere | Netze | Laufzeit |
|---|---|---|---|---|---|---|---|---|
| G4, 1 938 Bäume, Standard (ergaenzen + zusatz) | 40 846 | 16 494 | 23 100 | 34 | 1 218 | 34 / 0 | 123 | 12,6 s |
| G4, 1 938 Bäume, `--mittel voll` | 67 348 | 17 967 | 48 129 (Ziel greift, ×0,52) | 34 | 1 218 | 34 / 1 144 | 186 | 13,1 s |
| G4, 11 064 Bäume, Standard | 60 824 | 34 818 | 24 839 | 43 | 1 124 | 43 / 0 | 122 | 13,5 s |
| G4, 11 064 Bäume, `--mittel voll` | 87 229 | 38 043 | 48 019 (×0,51) | 43 | 1 124 | 43 / 1 519 | 185 | 13,7 s |
| G4, `--baum voll` (eigener Bestand) | 88 092 | 52 014 (Ziel, Laub ×0,91) | 21 496 | 13 519 | 1 063 | 10 324 / 0 | 151 | 10,9 s |
| G3 (Synthetik: nur 64 m Land am Südrand, keine Bestand-Ebene → `voll`) | 5 069 | 2 815 | 1 577 | 677 | 0 (kein Wasser, Hinweis) | 474 / 0 | – | 7,5 s |

Prüfskript (alle Läufe): jede f32 durch 10 teilbar, Anzahl = `plan.json`, Quaternionen normiert (|q| − 1 ≤ 1,1·10⁻⁷), Schema je Datei
(`pfad, anzahl, gruppe, rolle, ebene, sichtweite, schatten, kollision`) vollständig, **0 Instanzen auf Wasser/Weg/Ort, 0 außerhalb des
Feldes** (nach Korrektur: Feldgrenze jetzt auf der Gleitkomma-Koordinate, vorher 40 Instanzen bis 0,5 m außerhalb), z − Gelände −0,31 m
(Moossteine 18 cm, Böschungen 30 cm eingegraben) bis +0,23 m (Bilinear-Vergleichsartefakt am Bachhang), Maßstab 0,53–2,20 (Pilze bis
Moospolster), zwei Läufe byte-identisch (MD5 `44d47005…`). **Farninseln folgen der Beschattung:** Feldmittel 0,41 (dicht) – an
Farn-Instanzen 0,59, Heidelbeere 0,60, Moos 0,60, Laub 0,57; Lichtungsblumen 0,23, Adlerfarn 0,31 (Lichtungsrand). Im dünnen Bestand
(Mittel 0,09): Farn 0,33, Blumen 0,07. Fehlerpfade: Feld `K9`, fehlende Basis, fehlende Regeldatei → klare Meldung, Exit; fehlende
`lage_*`/Karten → Hinweis je Datei, Lauf geht weiter; fehlende Netzpfade würden aus den Paletten gestrichen (Meldung mit Liste).
Prüfbild `docs/pruefung/elfenwald/G4.png` (1 008 × 1 008): Höhe grau, Beschattung grün getönt, Wasser blau, Weg braun, Ort rot, Klassen
nach `bild_farben`, Blickziele als rotes Kreuz. Große Synthetik-Raster nach dem Test gelöscht.

**Behobene Fehler des Entwurfs:** Klassen-Kanäle aus Pythons `hash()` (je Prozess zufällig, nicht deterministisch) → CRC32; `eigner` 0
pauschal `aue` → dominantes Feldbiom; `SM_MossyTree_01` (liegender Stamm) als Baum gezählt; Python-Schleife im Wurzel-/Efeu-Ring
vektorisiert; Feldgrenze auf Zellen statt Koordinaten; Dichten offener Lagen gesenkt (Grasbüschel 0,040→0,025, Lichtungsblumen 0,028→0,010,
Beere 0,026→0,016, Lichtungsschwelle 0,42→0,34, Kerndichte 0,7–1,6), damit `voll`-Läufe nahe am Ziel landen.

**Erwartete Instanzzahlen je Feld mit Echtdaten (Richtwert, Spanne ±35 %; Grundlage: Land-/Laub-/Wasseranteil, Beschattung 0,8–0,9 bei
170 Bäumen/ha, Standardmodus):**

| Feld | Land % / elfenwald % | Baum (Modus) | Boden | Mittel (zusatz) | Wasserkante | Kollision |
|---|---|---|---|---|---|---|
| G4 | 100 / 76 (Bestand da) | 40–120 (ergaenzen) | 45 000–52 000 (Ziel greift) | 18 000–28 000 | 2 000–5 000 (Wasser 5 %) | 50–150 |
| G3 | 72 / 97 | 9 000–15 000 (voll) | 30 000–45 000 | 12 000–20 000 | 400–1 500 | 7 000–12 000 (Bäume) |
| H3 | 89 / 100, 60 % steil, Fels 26 % | 7 000–12 000 | 25 000–40 000 | 10 000–18 000 | 1 500–4 000 | 6 000–10 000 |
| H4 | 100 / 82 | 9 000–15 000 | 35 000–52 000 | 14 000–24 000 | 1 500–4 000 | 7 000–12 000 |
| I4 | 63 / 21 (bergwald ×0,6) | 2 000–5 000 | 6 000–14 000 | 3 000–7 000 | 300–1 200 | 1 500–4 000 |
| H2 | 39 / 20 (kueste ×0,3) | 800–2 500 | 2 500–7 000 | 1 200–3 500 | 100–500 | 600–2 000 |
| G2 | 4 / 20 | 0–100 | 100–600 | 50–300 | 0 | 0–80 |

Bleibt eine Schicht in G4 unter 50 % der Spanne, stimmt wahrscheinlich die Beschattung nicht (zu wenige Bäume erkannt: Hinweis
„Kronendach aus N Bäumen“ prüfen – N sollte ≈ 17 000 + Nachbarn sein); liegt sie darüber, greift das Ziel (Hinweis „Ausdünnung“).

**Prüfkameras (Augenhöhe 1,7 m, FoV 50°, Sonne 18–24° seitlich):**
1. **G4 Bachquerung** – auf dem Weg 10 m vor der Kreuzung Weg × Bach (Blickziel `schrein_an_bachquerung` in `plan.json`), Blick bachaufwärts.
   Erfolg: Moossteine 0,5–6 m vom Wasser in 2–5er-Gruppen, Farn/Schachtelhalm dazwischen, nichts im Wasser, nichts näher als 2,5 m am Weg;
   innerhalb 10 m ≥ 3 Objekte in 0,5–3 m Höhe (Farninsel, Moosstein, Weide/Pappel am Band 3–14 m).
2. **G4 Lichtung** – Mitte der größten Lichtung (Blickziel `lichtung_mit_blumen`), Blick nach Nordost gegen das Licht. Erfolg:
   Blumeninseln als Flecken 4–8 m (nicht Streu), Adlerfarn und Jungbäume (Teil D) am Rand dichter als innen, ein Hero-Altbaum am Rand
   (Maßstab 1,25–1,55), kein Baum in der Mitte.
3. **G4 Altwald** – 80 m in den Wald (Beschattung > 0,8), Blick quer zum Hang. Erfolg: Laub- und Zweighaufen um die Stämme, Wurzelanläufe
   an 30 % der alten Stämme, Moospolster und Heidelbeere in Senken, Farninseln im Schatten; in 10 m ≥ 4 Objekte in 0,5–3 m (Witcher-
   Richtwert 4–5 je 100 m² zusammen mit Teil D). Vergleich: `KLEIN12_G3_boden` (heute 0,5–0,7).
4. **G3 Waldkante** – an der Grenze Laub (56 %) → Sand (23 %), Blick entlang der Kante. Erfolg: Dichte-Falloff über 15 m innen / 10 m außen,
   Birken und Jungwuchs im Saum, keine harte Linie wie in `W6FIN_G3_rundgang`; Lichtungen 15–25 % (`statistik.lichtung_anteil`).
5. **H3 Hang** – Hangfuß unter einer Fels-Lage (Fels 26 %), Blick hangaufwärts. Erfolg: Bäume dünnen über 30° aus (Fels ×0,3), Moos und
   Kleinsteine ziehen auf den Fels, Farn nur auf der Schattseite; keine Instanz an Hängen > 40° außer Moos/Steinen (bis 45°).
6. **Draufsicht 300 m über G4** (Prüfbild und Editor): Farninseln als Flecken im dunklen Kronendach, Blumen nur in Lichtungen, Heide-Ecke
   (22 %) deutlich dünner (×0,25); **Naht G3/G4 und G4/H4** ohne Dichtesprung (Fenster + 64 m, nahtloses Wertrauschen).

**Erfolgskriterium in Zahlen:** an Kamera 1–3 kein 10-m-Umkreis ohne Objekt in 0,5–3 m Höhe (Mittelschicht Teil D + Elfenwald-Zusatz
zusammen ≥ 3–5 je 100 m²); Instanzen je Schicht in der Tabelle; Kollision Schichten 1/5 < 3 000; Setzer-Zeit je Feld < 5 min (≈ 120–190
Foliage-Typen `FT_EL_EW_*`); keine Instanz schwebt (Eingraben 1–30 cm) und keine steht im Wasser/auf dem Weg.

---

## 6. Einkaufsliste (frei bevorzugt, Stufe High 4K; Raw 8K nur für Hero-Stücke)

| Was | Wofür | Fab-/Megascans-Name (Vorschlag) | Stufe |
|---|---|---|---|
| **Hero-Laubbaum > 25 m** (alte Buche/Eiche, Wurzelanlauf, breite Krone) | Blickziel am Lichtungsrand, Hero-Klasse (heute nur Hornbeam_Field 1,25–1,55 skaliert; AsianTemple-Bäume 31–49 m stilistisch fremd) | Fab: „European Beech – Old / Hero“ (Megascans Trees: European Beech Forest Hero), „English Oak Hero“; ersatzweise Quixel „Common Oak“ | High, Nanite |
| **Eiche** als zweite Hauptart (Elfenwald hat Eiche 0 im Inventar) | Artenmix 20–30 %, Herbstakzent, Hero | Megascans Trees „English Oak“ Set (Forest/Field, Sapling) | High |
| **Ruinenstücke elfisch** (gebogene Bögen, Säulenstümpfe, Reliefplatten, Treppenreste, Bodenplatten) | `spuren_overrides.ruine` – heute nur 5 AncientRuins-Netze, zwei davon > 370 k Dreiecke | Fab „Ancient Ruins Modular“ / „Overgrown Ruins Kit“, Megascans „Ruined Wall Section“, „Stone Column Fragment“, „Carved Stone Slab“ | High, Nanite |
| **Pilze** (Steinpilz, Fliegenpilz, Baumpilz/Zunderschwamm, Pilzgruppen) | Boden-Klasse pilz hat nur 2 Meadow-Netze; Baumpilze an Totholz fehlen ganz | Megascans 3D Plants „Mushroom“ (Fly Agaric, Bolete, Shelf Fungus), Fab „Forest Mushrooms Pack“ | High |
| **Efeu/Ranken** als Stammhüllen und Wandbewuchs (gebogene Karten, Ranken 2–4 m) | Efeu am Stamm (heute flache Ivy-Karten), Ruinenbewuchs 40 % | Megascans „English Ivy Climbing“ (Trunk/Wall-Varianten), „Wild Grape Vine“, Fab „Vines & Creepers“ | High |
| Waldbodenblumen in 0,5–1,5 m Höhe (Fingerhut, Waldgeißbart, Bärlauch-Flächen) | Lücke aus Taxonomie: Lichtpflanzen 0,5–1,5 m | Megascans „Foxglove“, „Wild Garlic“, „Goatsbeard“ | High |
| Liegender Hero-Stamm > 8 m mit Wurzelteller, bemoost | Blickziel/Querung im Altwald (LargeFallenTree ist 5–6 m) | Megascans „Fallen Beech Tree Large“, „Uprooted Tree“ | High/Raw |
| Opfergaben/Kerzen/Stoffbänder für Schreine | `spuren_overrides.schrein.beigaben` (fehlt im Inventar) | Fab „Shrine Offerings“, „Medieval Candles“ | Medium |

---

## 7. Offene Punkte und Annahmen

1. **Ungetestet mit Echtdaten.** Beschattungs-Kalibrierung (k = 1,4, σ = 6 m) ist aus Teil D übernommen und an einem Synthetik-Bestand
   geprüft; mit 17 000 Bäumen in G4 wird die Beschattung ≈ 0,9 und die Bodenschicht läuft ins Ziel (52 000). Dann die Boden-Dichten um 20 %
   senken statt ausdünnen zu lassen (Laub 0,024 → 0,019).
2. **Baumschicht-Kollision** 10–13 000 bei `voll` überschreitet den Rahmen „≤ 3 000 Kollision“ bewusst (Bestand-Ebene hat 17 000); wenn
   Ferat das nicht will: `kollision_baum_je_feld` auf 3 000, dann nur hero/tot/alt mit Kollision.
3. **Teil-D-Kopplung.** `--mittel zusatz` setzt voraus, dass `mittelschicht_plan.py` in G3/H3/G4/H4/I4/H2/G2 läuft, und zwar **nach** dem
   Elfenwald-Planer, damit Teil D das Elfenwald-Kronendach (Schicht 2 bei `voll`) sieht; Teil D liest `bestand/` und `witcher/`, nicht
   `elfenwald/` – dort die Ebene `elfenwald` in die Baumquellen aufnehmen (eine Zeile in `lade_baeume`). Umgekehrt liest der Elfenwald-Planer
   keine `mittelschicht/`-Instanzen für den 1,2-m-Abstand; Doppelbelegung derselben Zelle ist bei den entfallenen Klassen ausgeschlossen,
   bei Farn (×0,45) möglich und gewollt (Insel-Verdichtung).
4. **Witcher-Haine bei `voll`.** `entfernen` löscht Witcher-Bäume nur mit den gelisteten Präfixen; Netznamen, die in `witcher/<Feld>/plan.json`
   anders heißen, bleiben stehen → nach dem ersten Echtlauf den Hinweis „entfernen-Filter“ gegen die Witcher-Dateinamen prüfen.
5. **Hang > 40°** bekommt nur Moos und Kleinsteine (bis 45°) und Böschungsstücke am Bach (bis 60°); Kletterpflanzen an Wänden sind Teil C/D.
6. **Nicht-Nanite-Netze** in den Paletten (Poplar_*, Big_Tree_birch/willow, hazel, black_cherry, maple_bush, nettle, Forest-grass, Forest-fern)
   brauchen LOD-Prüfung im Setzer; Sichtweiten sind entsprechend kurz gesetzt (150–350 m).
7. **I4/H2/G2** sind Randfelder mit 20 % Elfenwald-Anteil; dort läuft der Planer nur auf den elfenwald-Zellen voll und auf bergwald/kueste/
   aue-Zellen mit 0,6/0,3/0,5 – die Biomgruppen 1 (Nordküste) und 2 (Aue) bleiben dort führend; Dopplungen im Übergang über `eigner.r8`
   ausgeschlossen, solange beide Planer denselben Biomfaktor-Schnitt verwenden (Elfenwald 1,0 nur auf `rezept = elfenwald`).
8. **Blickziele** sind Vorschläge in `plan.json` (3 Arten, Koordinaten in cm); Instanzen dafür setzt `spuren_plan.py` nach den Overrides,
   der Elfenwald-Planer setzt nur die Blumeninsel-Verdichtung (Lichtung ×2) und den Hero-Altbaum (Lichtungsrand ×12).
9. **Laufzeit** 11–14 s je Feld in der Cloud (4 Kerne); die Jump-Flooding-Distanzfelder (9 Aufrufe) sind der größte Posten (≈ 6 s). Auf dem
   Projekt-PC mit numba ändert sich nichts (numba wird nur gemeldet, nicht genutzt).
