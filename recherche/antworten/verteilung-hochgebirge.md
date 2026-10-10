# Verteilung Biomgruppe 4: Gletscher/Frost/Hochgebirge (Kaer Morhen, Blaue Berge, Kovir)

**Projekt:** Eldarien, UE 5.8.3, 1-m-Raster 9577 × 7057, World Partition, Nanite. **Stand:** 2026-10-10 (Auftrag 11, Teil B4).
**Felder:** B1, C1, D1, E1, B2, C2, D2, E2, F2, E3 (Biome `gletscher`, `frost`; Mischanteile fjord/tundra/bergwald/aue).
**Lieferung:** dieses Dokument, `skripte/hochgebirge_regeln.json` (alle Zahlen, ohne Code änderbar), `skripte/hochgebirge_plan.py`
(Planer nach FORMAT.md §3/§5; Thema `hochgebirge`, Foliage-Typen `FT_EL_HG_*` in `/Game/Eldarien/Welt/Foliage/Hochgebirge`).
**Status:** Skript in der Cloud syntaxgeprüft und mit einem **synthetischen** D2-Fenster rauchgetestet (§5). **Kein Lauf mit Echtdaten,
kein Setzen im Editor.** Zahlen ohne Quelle sind Richtwerte und so markiert; Web-Quellen nur als **[Suchauszug]** (kein Direktzugriff
auf 80.lv/Fab/ArtStation aus dieser Umgebung, maximal 6 Suchen).

## 1. Witcher-Analyse: Kaer Morhen, Blaue Berge, Kovir – was den Berg zwischen Boden und Gipfel füllt

**Was CDPR belegt (Suchauszüge).** Zu Kaer Morhen gibt es keinen eigenen Umgebungs-Breakdown; das Vice-Interview zum Weltbau sagt, die
Orte seien keine 1:1-Kopien realer Landschaften, Gameplay und „Flow“ hätten Vorrang, und Kaer Morhen aus dem ersten Spiel sei die Basis für
die größere Festung samt Tal-Hub gewesen **[Suchauszug: vice.com „Designing the World of The Witcher 3“]**. Lukasz Lakomski nennt einen
eigenen „Decoration Pass“ für Kaer Morhen und die Höhlen **[Suchauszug: artstation.com/artwork/Z6Ql0]** – also eine Hand-Schicht über der
prozeduralen Vegetation (GDC 2014 Gollent, siehe `verteilung-aue.md`). Die Witcher-4-Demo (State of Unreal 2025) führt Ciri durch Kovir
„through rugged mountains and dense forests“ zum Hafen Valdrest, mit Nanite Foliage (jedes Blatt, jede Nadel 3D), Fast Geometry Streaming und
Mass-AI, PS5 bei 60 fps **[Suchauszug: press.cdprojektred.com/en/news/1778; cgmagonline.com]**. Für Eldarien folgt daraus nichts Numerisches,
aber zwei Prinzipien: (1) der Berg bekommt eine prozedurale Grundschicht **plus** eine Dekorationsschicht mit wenigen Hand-Akzenten (Totbaum,
Gipfelkreuz, Steinmännchen-Kette); (2) Nadelbäume sind in Kovir Fichte und Lärche, nicht Kiefer.

**Was die Zielbilder zeigen.** `witcher_07` (Nadelwald-Schlucht mit Lärchen): dunkle Fichten und rostrote Lärchen in Mischhöhen, Nebelbänder
zwischen den Stufen, Fels erst **über** dem Wald, die Rinne selbst bewaldet bis weit hinauf (Schluchtwald). `witcher_06` (Tal mit Brücke unter
rot-weißen Wänden): Wand (100 m) → hausgroße Blöcke → Kopfsteine → Schnee **nur in Rissen und auf Simsen**, nie an der Wand; unter jeder Wand
ein Schuttkegel. `witcher_04` (Klippe über dem Tal mit Burg): Vordergrundplatte mit Flechten, Kräutern und Schnee in Rissen; dahinter drei
Tiefenstufen im Dunst. `ANALYSE_WITCHER_2026-10-08.md` Punkt 5 fasst es zusammen: „scharfe Grate und Türme, Fels mit Farbbändern, Schnee nur
auf Simsen und flachen Stellen (Hangneigung!)“. Die Bildkritik (BERG8_C2/D2) hält dagegen: Kuppel-Silhouette, Felsschalen-Konfetti, keine
Höhenstaffel – zwischen Gipfel und Tal gibt es heute **keine** erkennbare Vegetationsstufe.

**Höhenstufen der Alpen → Eldarien.** Die Alpen staffeln (Quellen: Agrarraum-Lexikon, Biber Berti, wirtschaftsgeografie.com, GRIN
**[Suchauszüge]**): Bergwald bis ~1 500–1 800 m, subalpine Krummholzstufe (Latsche, Grünerle) bis zur Baumgrenze 1 900–2 400 m, alpine Matten-
stufe (Zwergsträucher, Gräser, Polster) bis 2 500–3 000 m, subnival/nival darüber (Moose, Flechten, Fels, Firn). Eldariens Berge enden bei
~700 m (B4 684 m; in der Gruppe C2 475, D2 446, E1 419, E2 381 m). Also werden die Stufen auf 0–700 m **gestaucht** und für die Nordlage
der Gletscherfelder abgesenkt. Der Planer rechnet je Zelle:

| Stufe | Inhalt (Witcher-Bild) | gletscher | frost | tundra | fjord | bergwald |
|---|---|---|---|---|---|---|
| 0 bergwald | Kiefern-/Tannenwald, Schluchtwald mit Lärchen (witcher_07) | < 170 m | < 120 m | < 220 m | < 200 m | < 360 m |
| 1 krummholz | Latschen-Inseln, Krüppelkiefern, windschiefe Einzelbäume, Totholz, Totbaum-Silhouetten | 170–270 | 120–220 | 220–320 | 200–300 | 360–460 |
| 2 matte | Alpenrosen-/Heide-Zwergstrauch, Polster, Grasbüschel, Flechtenblöcke, Schuttfächer | 270–370 | 220–280 | 320–420 | 300–400 | 460–540 |
| 3 fels_schnee | Schutt, Schnee-Simse, Eiszapfen, Hero-Felsen (Teil C) | > 370 | > 280 | > 420 | > 400 | > 540 |

Basis = Baumgrenze (gletscher 230, frost 180, tundra 280, fjord 260, bergwald 420 m) mit Krummholzband −60/+40 m und Schneegrenze = Baumgrenze
+ 100–140 m. Dazu kommen fünf Versätze, die die Witcher-Bilder erklären: **Exposition** ±45 m (Südhang höher; Sonnigkeit aus der Südkomponente
der Normale, voll ab 15° Hang), **Hang** −30 m bei 25→45° (steile Flanken sind früher kahl), **Grat** −40 m (Laplace σ 6 m, konvex; Grate
tragen keinen Wald, Bildkritik „Baumreihe exakt auf der Kammlinie“ ist ein Fehler), **Rauschen** ±35 m auf einem 320-m-Gitter (keine
Höhenlinie als Waldkante) und **Schlucht** +70 m in konkaven Rinnen ≤ 25 m vom Bach (Laplace σ 8 m > 0,006; der Lärchen-Schluchtwald aus
witcher_07 reicht über die Baumgrenze hinaus). Unabhängig von der Höhe gilt `lage_Schnee ≥ 0,55` oder `lage_Eis ≥ 0,4` → Stufe 3: Das ist für
**E2** entscheidend (Schnee 47 %, Eis 9 % bei Ø 139 m) und für F2/E3 (Schnee 34/17 %): Dort liegt der „Frost“ als Lage, nicht als Höhe.

**Dichten, Gruppen, Farbakzente (aus den Bildern geschätzt, Richtwerte).** In witcher_07 stehen auf 100 m Hang 3–5 Baumtrupps zu 4–10 Stück
mit Lücken von 15–30 m; an der Waldgrenze Einzelbäume alle 15–25 m, zwischen ihnen Latschen-Inseln 3–9 Stück je 15–40 m². Farbakzente:
Lärchen-Rost (fehlt im Inventar, §6), Alpenrosen-Rosa (Mountain `SM_rhododendron_01/02`), Flechten-Gelbgrün (`SM_LichenedForestBoulder_01`),
Schnee-Weiß gegen Felsgrau. Blickziele je Feld (Spuren-Overrides §3): Felsturm/Grat-Hero aus Teil C, Wasserfall, Gletscherzunge (E2),
Gipfelkreuz, Totbaum-Solitär. Spuren von Leben über der Baumgrenze: Steinmännchen alle 60–100 m am Pfad, ein Holzkreuz je Pass, eine
Passhütte mit Rauch – sonst nichts (keine Zäune, keine Felder).

**Botanische Stützen (Suchauszüge).** Die Latsche (Pinus mugo) besiedelt die subalpine Krummholzstufe zusammen mit Alpenrosen, „mäßig
trockene, felsige, sehr nasse oder kalte Standorte“ und Lawinenhänge, auf denen alle anderen Baumarten zerstört werden; sie verträgt
Schneelast und wurzelt am breitesten auf Schutthängen **[Suchauszug: flora-kleinwalsertal.at, wildfind.com, de.wikipedia.org/wiki/Bergkiefer]**.
Die Rostblättrige Alpenrose wächst „just above the tree line“ auf kalkarmen Böden **[Suchauszug: en.wikipedia.org/wiki/Rhododendron_ferrugineum,
openflora.ch]**; ihre Bindung an lange Schneedecke (Nordhang) ist Lehrbuchwissen, in den Suchauszügen aber nicht belegt – daher nur
Faktor 1,25 Nord / 0,8 Süd. Hangneigungsgrenzen für beide fand die Suche nicht; die Regel „Pflanzen ≤ 40°“ kommt aus FORMAT §3, die
Latsche erhält deshalb den vollen Faktor bis 34° (Steilhang-Besiedler), nicht bis 30° wie Bäume.

## 2. Regelwerk (`hochgebirge_regeln.json`) – Erklärung je Schicht

Alle Dichten sind Instanzen je m² vor Faktoren; Faktoren: Stufe [bergwald, krummholz, matte, fels_schnee], Biom (gletscher/frost 1,0; tundra
0,55; fjord 0,4; bergwald 0,3; alle anderen 0), Lagen (1 + Σ Deckung·(w−1)), Hang (voll bis a°, null ab b°), Exposition (Nord→Süd linear).
Gruppen: Saat-Wahrscheinlichkeit = Dichte / mittlere Gruppengröße, dann n Mitglieder im Radius; jedes Mitglied muss selbst eine gültige
Zelle treffen. In **Nicht-Kernbiomen** (tundra, fjord, bergwald) setzt der Planer nur Stufe ≥ 1, weil B1/B3 dort den Wald planen.

**Schicht 0 boden (Budget 38 500).**

| Klasse | Netze | Dichte | Stufen | Lagen (Gewicht) | Hang | Gruppe | Maßstab / Eingraben | Sichtweite |
|---|---|---|---|---|---|---|---|---|
| kiesel_schutt | SmallStonesPack_08…14, Mountain SM_stone_04…08 (5–12 cm) | 0,30 | 0,25/0,7/1/1 | Geröll 2,2, Kies 1,8, Fels 1,6, Schnee 0,5, Eis 0,3, Gras 0,2 | ≤ 35° voll, 55° null | 4–14 in 1,8 m | 0,8–1,6, 35 % | 60 m |
| flechtenstein | mountain_rock_small_01_1/2/4/5, s_rock_01…03, NordicBeachRock_01 (16–44 cm) | 0,06 | 0,3/0,8/1/0,7 | Geröll 1,6, Fels 1,5, Felsplatte 1,3 | 35/55° | 2–6 in 2 m | 0,7–1,4, 40 % | 120 m |
| schneefleck | Icelandic_Boulder texndcpda, Nordic_Cluster_Small xjijdiz, NordicBeachRockyGround_02, NordicBeach_02 (25–41 cm flache Platten) | 0,035 | 0/0,2/0,6/1 | Schnee 1,8, Eis 1,4 | **≤ 20° voll, 32° null** | 2–5 in 2,5 m | 0,8–1,3, 50 % | 100 m |
| geroellplatte | TundraRockyGround_01, NordicBeachRockyGround_01, xjijdiz_tier_0 (2–6 m) | 0,004 | 0,1/0,5/1/0,8 | Geröll 2,5, Kies 1,5, Fels 1,4 | 14–36° voll, 46° null | 1–3 in 5 m | 0,8–1,25, 45 %, Längsachse hangab ±25° | 300 m |

Der Schneefleck ist die Umsetzung von „Schnee nur auf Simsen“: flache Platten ragen nur aus Flächen < 32° aus dem Schnee; an Wänden gibt es
keine Schnee-Instanzen. Schuttfächer-Platten liegen auf 14–46° (Halden 30–38°, Wikipedia Scree; Fächer selbst plant Teil C).

**Schicht 1 mittel (Budget 51 800, Ziel-Gesamtbudget 52 000 greift vorher).**

| Klasse | Netze | Dichte | Stufen | Hang | Exposition N/S | Gruppe | Besonderes |
|---|---|---|---|---|---|---|---|
| latsche | dwarf_pine_small/medium/big (0,9–2,6 m; kein Nanite) | 0,03 | 0,2/1/0,3/0 | 34/40° | 0,6/1,3 | 3–9 in 3,5 m | Längsachse in Windrichtung, 30 % auf Normale gekippt, Sichtweite 350 m, Budget 7 000 |
| krueppelkiefer | pine_beach_crooked_01/02, short_01/02 (0,8–3,4 m) | 0,005 | 0,1/1/0,15/0 | 32/40° | 0,5/1,4 | 1–3 in 4 m | 6–18° in den Wind gekippt; Kollision nur crooked_01 (3,4 m) |
| alpenrose | rhododendron_01/02 (3), heath_A/B (2), lingonberry_01, billberry_03 | 0,05 | 0,3/1/1/0,1 | 34/40° | **1,25/0,8** | 6–16 in 3 m | Heide-Lage 1,7; Budget 10 000 |
| polster | heath_cross_01, forest_heather_01, billberry_dry_01, lingonberry_02 | 0,03 | 0,1/0,6/1/0,3 | 36/40° | 0,9/1,1 | 3–8 in 1,5 m | Fels 1,2 / Geröll 1,3 / Kies 1,2 bevorzugt (Felsritzen) |
| grasbueschel_alpin | Tundra_Grass VarA–H (Nanite), grass_03_A_1, dead_grass_03 | 0,06 | 0,5/1/1/0,1 | 34/40° | 0,8/1,2 | 4–12 in 2,5 m | Trockengras 1,6, Wiese 1,3; Budget 12 000 |
| totholz_wind | dead_log_01…04, Pine_broken_branch_01/02, mountain_branch_01_01/02, pine_stump_01/02 | 0,004 | 0,6/1/0,3/0,05 | 32/40° | – | 1–3 in 2 m | Längsachse hangab ±60°, Eingraben 25 % |
| wurzelteller | Pine_roots_01…03, stones_roots_01 (0,6–1,6 m) | 0,0008 | 0,5/1/0,2/0 | 32/40° | – | einzeln | Kollision, Sichtweite 400 m, Budget 300 |
| flechtenblock | LichenedForestBoulder_01, stones_01_2/5/6, Nordic_Rock_Small xjijbgx, Icelandic_Rock skjsL, Granite pjtsT (0,46–0,91 m) | 0,012 | 0,4/0,8/1/0,8 | 38/55° | – | 2–5 in 2,5 m | Mittelschicht-Ersatz über der Baumgrenze (Taxonomie-Lücke); Kollision nur ≥ 0,8 m |

**Schicht 2 baum (Budget 6 300, Kollision).**

| Klasse | Netze | Dichte | Stufen | Hang | Gruppe | Besonderes |
|---|---|---|---|---|---|---|
| bergwald_kiefer | Forest_pine_01/02/03, Fir_06_Forest, Fir_03_Medium (12–22 m) | 0,006 | 1/0,15/0/0 | 30/40° | 3–8 in 9 m | nur Kernbiome (dort liegt keine Bestand-Ebene); 4 m Abstand zu BST/WIT/Houdini-Bäumen; Maßstab 0,75–1,15 |
| krummholz_baum | Forest_pine_plant_03, pine_beach_03_A/04_A, Fir_01_Plant, Fir_02_Small (4–7,5 m) | 0,006 | 0,3/1/0,12/0 | 32/40° | 1–4 in 5 m | z-gestaucht 0,7–1,0, 35 % gekippt, in Windrichtung |
| schluchtwald | Fir_03_Medium, Fir_02_Small, Forest_pine_01/02, Fir_07_Forest | 0,012 | 1/1/0,6/0 | 34/44° | 4–10 in 7 m | **nur Schlucht-Maske** (konkav, ≤ 25 m vom Bach), Nordhang 1,1; Lärchen-Ersatz bis zum Kauf |
| totbaum_grenze | DeadTree_01/02, Dead_Tree qlEtl (Nanite, 6,2–6,8 m), Fir_08_Dead_Forest | 0,0009 | 0,3/1/0,3/0,02 | 34/40° | 1–2 in 6 m | Silhouetten gegen den Himmel, Maßstab 0,6–1,0, Budget 300 |

**Schicht 5 wasserkante (Budget 17 800).** Wasserzellen mit Hang ≥ 18° gelten als Wasserfall/Kaskade; Fuß = Zellen ≤ 10 m darunter mit Hang
< 25°; Gletscherbach = Wasser in Stufe ≥ 2 mit 6-m-Saum.

| Klasse | Netze | Band | Dichte | Gruppe | Besonderes |
|---|---|---|---|---|---|
| bach_block | IcelandicBoulder_01, Nordic_Cluster xisgcic/xf3odif/xfplcbf, Granite pkeeM (0,9–1,2 m) | 1–4 m | 0,05 | 1–3 in 2,5 m | Kollision, Eingraben 35 %, Hang ≤ 55° |
| bach_moosstein | MossyForestRock_01, MossyForestBoulder_02, stones_01_1/3/4 | 1–6 m | 0,08 | 2–5 in 2 m | Stufe 3 nur 0,2 (Moos nicht über der Schneegrenze) |
| bach_kiesel | NordicBeachRock_01, SmallStonesPack_08/11/13, stone_06 | 1–3 m | 0,5 | 4–12 in 1,5 m | Sichtweite 60 m, Budget 8 000 |
| wasserfall_block | NordicBoulder_01, IcelandicBoulder_03, NordicBeachRocks_01, xisgcic (1,1–4,1 m) | Wasserfallfuß | 0,03 | 1–3 in 4 m | Kollision, Hero-Sturzblöcke, Budget 300 |
| eiszapfen | Eldarien SM_EISZAPFEN_1/2/3/5/6/7 (0,8–2,6 m) | Wand ≥ 55° in Stufe ≥ 2 oder ≤ 3 m an Kaskaden | 0,04 | 2–6 in 1,5 m | Nordwand 1,4 / Süd 0,6; z = Gelände + 0,85·Netzhöhe (Pivot oben angenommen); Budget 1 500 |

**Ausschlüsse und Budget.** Nichts auf Wasser, Meer (Höhe ≤ 0,2 m), Weg (2,5 m Kleinzeug, 4 m Bäume/Blöcke), Ort (5 m); Abstand zu Bäumen
der Ebenen `bestand/`, `witcher/`, `instanzen/` (Feld + 8 Nachbarn): Bäume 4 m, Mittelschicht 1,5 m, Wasserkante 1 m; zu Felsschalen
(`felsschalen/plan_<Feld>.json`): Bäume 3 m, Mittelschicht 1 m. Pflanzen nie über 40°, Steine bis 55°, Eiszapfen 55–90°. Erst Klassenbudgets,
dann Gesamtziel 52 000 (Deckel 60 000) und Kollision 3 000, ausgedünnt von der niedrigsten Priorität (Kiesel) aufwärts per Instanz-Hash –
deterministisch. Zufall: 64-bit-Hash aus (Seed 4411 + Klassenindex, Weltraster i, j, Mitglied); Fenster Feld + 64 m, also nahtlos.

## 3. Overrides für die Querschnitts-Planer (nicht von diesem Skript angewendet)

**Felsgruppen (Teil C, `felsgruppen_overrides`).** Biomfaktor gletscher 1,3 / frost 1,1 mit Palette `tundra` plus Zusatz-Hero
(MassiveTundraRockFormation_02, NordicBoulder_01, IcelandicBoulder_03), Blöcke (IcelandicBoulder_01, skjsL, pkeeM, pjEr1), Platten
(TundraRockyGround_01, texndcpda) und Rolle `eis` (SM_EISZAPFEN_4/8/9 für Grat-Nordwände). **Schneegrenze:** oberhalb (Höhenregel oder
`lage_Schnee ≥ 0,55`) Moos-Netze ausschließen (TundraMossyBoulder, MossyForest*), Kiesel ×0,5, Hero ×1,2 (freigewitterte Felsen); Schnee hemmt
Felsen nur bis Faktor 0,6 (Schnee liegt **auf** Felsen, sie verschwinden nicht). **Schuttdichten:** Fächer p 0,7 (statt 0,45) und bis 90 m
lang (Frostsprengung), Stufen 0–10 m Blöcke ×0,85–1,2, 10–22 m ×0,55–0,85, 22–45 m Steine ×0,7–1,1, 45–90 m ×0,4–0,7; Blockstrom-Faktor 1,4
als Moränen-Ersatz an Karböden (konkav, 5–18°) mit Hauptrichtung quer zum Tal; Grat p 0,65 / Hero 0,7 mit Eiszapfen an der Nordseite;
Felsband-Faktor 0,8 (Schnee-Simse liegen auf dem Band). Kieselsaum 2–5/m². `entfernen_zusatz` listet die gletscher/frost-Suffixe der
Block-Felsschalen (`FT_EL_FS_mountain_rock_big_02_8_*`, `FT_EL_FS_IcelandicBoulder_02/03_*`), die mit Teil C entfallen.

**Spuren (Teil D, `spuren_overrides`).** Steinmännchen alle 60–100 m am Weg (2–5 m seitlich), auf Kuppen/Pässen (Prominenz ≥ 8 m) und frei
12/km², nur ab Stufe 1, 5–11 Steine, Basis-Maßstab 1,6–2,4; Holzkreuz alle 400 m an Pässen, keine Schreine; keine Zäune, keine Feldstreifen;
Einzelgräber 0,6 je km Weg; Rauch nur an Pass-Hütten (Faktor 0,5). Fehlende Netze (Gipfelkreuz, Unterstand, Seilbrücke/Steg) sind mit
Regel hinterlegt und stehen in der Einkaufsliste; Zwischenlösung Holzkreuz ×2,5 aus `spuren_regeln.netze.kreuz`. Blickziel-Regel
**Gletscherzunge:** größte zusammenhängende `lage_Eis`-Fläche ≥ 2 000 m² mit Hang 8–25°; ihr tiefster Punkt ist Zungenende und Bachquelle.

## 4. Abgrenzung zu `FT_EL_WIT_*`, `FT_EL_BST_*`, `FT_EL_FS_*`

| Ebene | Verhältnis | `entfernen` |
|---|---|---|
| Witcher-Bewuchs `FT_EL_WIT_*` (Haine, Farn, Ahornbusch, Weide, Krautpflanzen, Laub/Zweige) | Ergänzen. Hochgebirge nutzt andere Netze (Latsche, Alpenrose, Tundra-Gras, Nordic-Steine) und andere Steuergrößen (Höhenstufe, Exposition, Schnee-Lage). Über der Baumgrenze stören Farn/Ahorn/Weide aber die Stufe. | Standard leer. Vorschlag `FT_EL_WIT_foliage_fern,FT_EL_WIT_maple_bush,FT_EL_WIT_grey_willow,FT_EL_WIT_plant_0` **nur** in reinen gletscher/frost-Feldern (E1, F2), weil `entfernen` feldweit wirkt; C2/D2/E2 (fjord/tundra-Anteile) nicht. Eintrag in `ausgabe.entfernen`. |
| Wald-Bestand `FT_EL_BST_*` (B1/B3 planen Wald in fjord/tundra/bergwald) | Abstand 4 m zu allen BST-Bäumen; `bergwald_kiefer` nur in Kernbiomen (dort gibt es keine BST-Ebene); in tundra/fjord/bergwald setzt der Planer nur Stufe ≥ 1. Kamm-Ausschluss (Grat −40 m) ergänzt die BST-Kammregel. | keine |
| Felsschalen `FT_EL_FS_*` | Abstand 3 m (Bäume) / 1 m (Mittel); Block-Klassen entfallen mit Teil C (`felsgruppen_overrides.entfernen_zusatz`), Wand-Schalen bleiben bis zur Abnahme der Klasse `wand`. | nur über Teil C |
| Ufer `FT_EL_UF_*` | An Gletscherbächen über der Baumgrenze setzt die Ufer-Ebene bereits Kiesel/Blöcke; `bach_kiesel` ist deshalb auf 1–3 m und 8 000 begrenzt. Wenn Ufer dort schon liegt: `bach_kiesel.dichte_je_m2` auf 0. | keine |
| Houdini-Bestand (`instanzen.json`) | Abstand wie BST; fehlt die Datei → Hinweis, Lauf geht weiter. | keine |

Die Hochgebirge-Ebene ersetzt also **nichts** automatisch; sie fügt die Höhenstufen-Schicht ein, die heute fehlt. Mischfelder bekommen in
den Nicht-Kernanteilen nur die Stufen ≥ 1 (Krummholz, Matte, Fels/Schnee), die B1/B3 nicht planen.

## 5. Testanleitung

**Aufruf (lokal):** `python -I scripts/hochgebirge/hochgebirge_plan.py C2 D2 E1 E2 --bild` (Regeldatei neben dem Skript; `--faktor 0.7`
für dichte Bergfelder; `--basis` = production-Wurzel). Ausgabe `export/unreal/welt/hochgebirge/<Feld>/<Netz>.f32` + `plan.json` (FORMAT §3
plus `ebene` je Netz und `statistik` mit Klassen, Ebenen, Stufenflächen, Baum-/Schneegrenze, Laufzeit), Prüfbild
`docs/pruefung/hochgebirge/<Feld>.png` (Stufen dunkelgrün/oliv/ocker/weiß, Meer dunkelblau, Wasser blau, Wasserfallfuß cyan, Schlucht
grünlich, Klassen nach `bild_farben`). Setzer: generisch (FORMAT §3), Foliage-Typen `FT_EL_HG_<Netz>` – Sichtweiten/Kollision/Schatten aus
`plan.json["dateien"]`; die Mountain-/Coast-Dunes-Pflanzen sind kein Nanite und brauchen Cull 350–400 m.

**Rauchtest (synthetisch, Cloud, Python 3.13, NumPy 2.5, Pillow 12, kein numba).** Mini-Produktionswurzel mit `hoehe.f32` in voller Größe
(memmap 270 MB, nur D2-Fenster + 96 m beschrieben): Bergmassiv 0–668 m mit scharfem Grat NW–SO, Hauptgipfel, Nebengipfel, Kar mit flachem
Karsee und Gletscherbach nach NO, Wandstufe am SW-Hang, Passweg (3 678 Zellen), Passhütte (313), Meer-Ecke (0 m), 72 % Hang > 30°, 18 % > 55°;
`karte_wasser/weg/ort.r8`, `lage_Fels/Geroell/Schnee/Eis/Trockengras/Heide.r8`, `eigner.r8` (Kacheln 5 gletscher_nord, 6 tundra_hang, Streifen 0)
+ `welt.json`, `bestand/D2` (300 Kiefern), `felsschalen/plan_D2.json` (40 Stücke), `daten/netze.csv`, `daten/biome_je_feld.json`;
kein `instanzen.json`, kein `netze_masse.json` (beides → Hinweis). Ergebnis D2: **44 107 Instanzen, 112 Netze, 1 207 mit Kollision, 4,1 s**
(Gesamtlauf 4,8 s); Ebenen boden 31 690 / mittel 9 815 / baum 317 / wasserkante 2 285; Klassen kiesel 22 000 (Budget), flechtenstein 9 000
(Budget), schneefleck 370, geroellplatte 320, latsche 649, krüppelkiefer 108, alpenrose 2 263, polster 1 488, grasbüschel 2 715, totholz 168,
wurzelteller 27, flechtenblock 2 397, bergwald_kiefer 43, krummholz_baum 130, schluchtwald 96, totbaum 48, bach_block 58, moosstein 190,
bach_kiesel 511, wasserfall_block 26, eiszapfen 1 500 (Budget). Stufenflächen im Feld 37,5 / 23,2 / 14,1 / 23,6 %, Baumgrenze 89–387 m
(Mittel 226), Schneegrenze 229–477 m. Geprüft: alle f32 mit 10 float32 je Instanz, Anzahl = `plan.json`, Quaternionen normiert (Fehler 0),
x/y im Feld, Maßstab 0,52–1,91, Eiszapfen hängen (z = Gelände + 0,85 H); zwei Läufe byteidentisch; `--faktor 0.5` → 35 397; Höhenstufen im
PNG als vier Bänder um den Grat sichtbar, Schluchtwald in der Bachrinne, Wasserfallfuß am Karsee-Abfluss. Randfälle: J7 (Randspalte 505 m,
kein Land) und E1 (im Synthetik Meer) → leerer Plan mit Hinweis, 1,3–3,4 s; fehlende `hoehe.f32`/`netze.csv` → „FEHLT (Pflicht)“; Feld Z9
→ Fehlermeldung, Lauf geht weiter. Im ersten Lauf fielen zwei Fehler auf und wurden behoben: keine Land-/Meerprüfung (Instanzen auf 0 m
möglich) und Matte zu schmal (Schneegrenze +40 m). Die synthetischen Raster wurden danach gelöscht.

**Erwartete Instanzzahlen je Feld** (Spanne; Grundlage: Rauchtest skaliert mit Land-% und Kernbiom-Anteil; Echtdaten ±50 %; auch in
`erwartung_je_feld`):

| Feld | Land % / Kernbiom % | gesamt | boden | mittel | baum | wasserkante | Kollision |
|---|---|---|---|---|---|---|---|
| D2 | 100 / gletscher 34 (+ tundra 47) | 30 000–50 000 | 22 000–32 000 | 6 000–12 000 | 150–500 | 800–3 000 | 800–1 800 |
| E2 | 100 / gletscher 50 + frost 39 | 35 000–58 000 | 25 000–35 000 | 5 000–12 000 | 300–900 | 2 000–6 000 (Eis 9 %, Eiszapfen am Budget) | 900–2 200 |
| C2 | 65 / gletscher 46 | 20 000–40 000 | 15 000–26 000 | 4 000–9 000 | 150–500 | 800–3 000 | 600–1 500 |
| C1, D1, E1 | 35–40 / gletscher 69–100 | 10 000–25 000 | 8 000–17 000 | 2 000–6 000 | 100–400 | 300–1 500 | 300–1 000 |
| B2 | 25 / gletscher 80 | 8 000–16 000 | 6 000–11 000 | 1 500–4 000 | 50–250 | 200–800 | 250–700 |
| F2 | 34 / frost 46 | 6 000–14 000 | 4 000–9 000 | 1 000–3 500 | 50–200 | 200–1 000 | 150–500 |
| E3 | 56 / frost 7 (+ tundra 60) | 2 000–8 000 | 1 500–5 000 | 400–2 000 | 0–60 | 50–500 | 50–300 |
| B1 | 9 / gletscher 94 | 1 500–5 000 | 1 000–3 500 | 300–1 200 | 0–50 | 0–300 | 30–200 |

Liegt ein Feld über 52 000, greift der Deckel (Kiesel zuerst). Liegt es unter der Spanne, zuerst `statistik.je_stufe_flaeche_prozent` prüfen:
Sind > 70 % Stufe 0 in einem tundra-Feld, ist die Baumgrenze für dieses Massiv zu hoch (`baumgrenze_m.tundra` senken).

**Prüfkameras** (Welt-cm; X = (j − 4730,5)·100, Y = (i − 4060,5)·100; Feldmitte angegeben, Kamera relativ dazu setzen):

| Feld / Lage | Position | Blick | Erfolg erkennbar an |
|---|---|---|---|
| **C2 Grat** (Mitte X −221 050, Y −254 850; max 475 m) | höchster Punkt des Hauptkamms, 200 m seitlich quer zum Grat, 40 m über Grund | entlang des Grats, 10° abwärts | vier Bänder von unten nach oben: Kiefern (nur im gletscher-Teil) → Latschen-Inseln und windschiefe Einzelbäume mit 1–2 Totbäumen als Silhouette → Alpenrosen-/Heide-Flecken mit Flechtenblöcken und Schuttplatten → Schutt mit Schnee-Simsen; der Grat selbst ohne Bäume (Versatz −40 m); Waldkante keine Höhenlinie (Rauschen ±35 m), auf der Südflanke 60–90 m höher als auf der Nordflanke |
| **D2 Doppelkuppel** (X −120 250, Y −254 850; max 446 m) | Sattel zwischen den Kuppeln, 30 m über Grund (Nachstellung BERG8_D2) | auf die höhere Kuppe, 15° aufwärts | Dünenprofil durch Stufenwechsel gegliedert: Krummholz-Band mit Latschen quer zum Hang, darüber ocker-graue Matte, Schneeflecken nur auf Flächen < 32°, keine Schnee-Platten an der Flanke; Bach-Rinnen mit Schluchtwald (Fir) bis über die Baumgrenze |
| **E1 Gletscherkamm** (X −19 450, Y −355 650; max 419 m) | höchster Punkt, 150 m entlang des Kamms zurück, 30 m über Grund | entlang des Kamms, Nordwand im Bild | Eiszapfen (SM_EISZAPFEN) hängen an Nordwänden ≥ 55° über der Schneegrenze, nicht an Südwänden und nicht auf Flächen; Schutt-Kiesel 4–14 in Gruppen auf Geröll-Lage; `entfernen`-Vorschlag aktiv → keine Farne/Ahornbüsche über 230 m |
| **E2 Gletscherzunge** (X −19 450, Y −254 850; max 381 m) | tiefster Punkt der größten `lage_Eis`-Fläche (Zungenende), 60 m talwärts, 15 m über Grund | zungenaufwärts, 10° aufwärts | Stufe 3 trotz Ø 139 m (Lage Schnee/Eis > 0,55/0,4): Schneefleck-Platten auf dem Firn, Schutt, Eiszapfen an Eis-/Felskanten; am Bach ab der Quelle Bachblöcke 0,9–1,2 m und Moossteine erst unterhalb der Schneegrenze; keine Alpenrosen auf Eis (Lage 0,0) |
| **F2 Frost-Terrasse** (X 81 350, Y −254 850; max 174 m) | Übergang aue→frost, 20 m über Grund | hangauf | im aue-Anteil nichts (Biomfaktor 0), im frost-Anteil Krummholz ab 120 m mit Krüppelkiefern in Windrichtung (Yaw 90° ± 18°, 6–18° gekippt) |

An jeder Kamera zusätzlich 3 m Nahsicht: Latschen und Alpenrosen 3–6 cm eingegraben (keine schwebenden Wurzelhälse), Steine 35–50 % im
Boden, Eiszapfen mit Spitze nach unten (sonst `z_versatz_anteil` oder Pivot-Annahme korrigieren), keine Pflanze über 40° Hang.

## 6. Einkaufsliste (Fab/Megascans, frei bevorzugt, Stufe High 4K; Namen sind Fab-Suchbegriffe – Fab war aus der Cloud nicht erreichbar)

| Asset (Suchbegriff) | Stufe | Wofür | Lücke heute |
|---|---|---|---|
| **Europäische Lärche** (Fab „European Larch“ / „Larix decidua“; MAWI/„Conifer Forest“-Packs enthalten Lärchen, Herbstvariante rostrot) | High, Nanite-fähig, 2–3 Alter + Herbst | `schluchtwald`, `bergwald_kiefer` 20–35 % Beimischung, Krummholz-Einzelbaum (witcher_07-Rostton) | Megascans führt keine Lärche **[Suchauszug: Megascans-Baumpacks sind Erle/Buche]**; Inventar nur Kiefer/Tanne; Zwischenlösung PerInstanceRandom-Tint auf Fir |
| **Latsche / Legföhre** (Fab „Mountain Pine“, „Pinus mugo“, „Dwarf Pine Nanite“) | High, Nanite | `latsche` – heute Mountain `SM_dwarf_pine_*` ohne Nanite (Cull 350 m, VSM-Kosten) | kein Nanite-Zwergkiefer-Netz |
| **Alpenrose** (Fab „Rhododendron ferrugineum“, „Alpine Rose“; sonst Megascans „Heather“/„Blueberry“ als Ersatz) | High | `alpenrose` – rosa Farbakzent der Matte | `SM_rhododendron_01/02` sind Mountain-Gartenformen 0,4 m ohne Nanite |
| **Schnee-Felsen / Snowy Rocks** (Megascans „Snowy Rock“, „Snow Covered Boulder“, „Icelandic Snow Rock“) | High 4K | Stufe 3 Blöcke/Hero statt Material-Schneekrone; `schneefleck`-Platten mit echtem Schnee | heute Schnee nur über `M_EL_Klippe_RVT`/Material; keine Schnee-Netze |
| **Eisblöcke / Firnreste** (Fab „Ice Block“, „Glacier Ice Chunk“, „Frozen Rock“) | High, Nanite | Gletscherzunge E2, Karsee-Rand, Moränen-Ersatz (Taxonomie-Lücke „keine Eisblöcke/Firnreste“) | nur SM_EISZAPFEN (hängend) |
| **Gipfelkreuz** (Fab „Summit Cross“, „Wooden Cross Mountain“; Metall oder Holz, 2–3 m) | Medium reicht | 1 Akteur je Berg (Spuren-Override `gipfelkreuz`) | kein Netz; Zwischenlösung Holzkreuz ×2,5 |
| **Steinmännchen** (Fab „Cairn“, „Stone Pile Marker“ 0,6–1,2 m, 2–3 Varianten) | High | Spuren `steinmann` als ein Netz statt 5–11 Instanzen (Kollision, HLOD) | Zwischenlösung aus mountain_rock_small/s_rock |
| Unterstand/Pass-Hütte, Seilbrücke/Steg (Fab „Alpine Hut“, „Rope Bridge“) | Medium | Spuren-Overrides `unterstand`, `seilbruecke_steg` | keine Netze |
| Moränenschutt-Platte (Megascans „Rocky Ground Moraine“/„Gravel Debris Slope“ 3–5 m) | High 4K | `geroellplatte` 2–6 m (heute 3 Netze) | zu wenig Platten-Varianten |

Vor jedem Kauf: Megascans ggf. schon vor 31.12.2024 beansprucht (dann frei); nach Import der Post-Import-Pass aus `klippennetze-a5.md`
(Nanite, Kollision Convex, Texturen auf 4K klemmen). Die Suche nach Fab-Listings für Gipfelkreuz/Eisblock/Steinmännchen lieferte nur
Fab-Allgemeines **[Suchauszug: fab.com-Launch-Meldungen]** – Namen sind Suchbegriffe, keine bestätigten Listings.

## 7. Offene Punkte und Annahmen

1. **Ungetestet mit Echtdaten.** Schwellen (Grat-Laplace 0,015, Schlucht-Krümmung 0,006, Baum-/Schneegrenzen je Biom) sind am synthetischen
   Massiv abgestimmt. Erster Echtlauf D2/E2 mit `--bild`, dann `statistik.je_stufe_flaeche_prozent` gegen `biome_je_feld.md` (Höhe Ø/max)
   prüfen; typische Korrektur: `baumgrenze_m.gletscher` ±30 m, `rauschen_amplitude_m` 35 → 25, wenn die Waldkante zu zerrissen ist.
2. **Rasterrichtung.** Annahme: Zeile i wächst nach Süden (A1 = links oben, `biome_je_feld.json` „raster“); Exposition und Windrichtung
   (`wind_richtung_grad` 90 = +Y) hängen daran. Zeigt der Südhang im Editor nach Norden, `exposition`-Paare je Klasse tauschen (oder
   `exposition_versatz_m` negieren) und `wind_richtung_grad` auf 270.
3. **Pivot der Eiszapfen** (`SM_EISZAPFEN_*`): Pivot oben angenommen, z = Gelände + 0,85·H·s. Hängt der Zapfen falsch, `z_versatz_anteil` auf
   0 (Pivot unten) oder 0,5 stellen. Mountain-/Coast-Dunes-Netze fehlen in `netze_masse.json` → Pivot Bodenmitte angenommen.
4. **Nicht-Kernbiome.** In tundra/fjord/bergwald plant das Skript nur Stufe ≥ 1; wenn B1/B3 dort selbst Krummholz setzen, `biom_faktor.tundra/
   fjord` auf 0 oder `nicht_kern_nur_ab_stufe` auf 2. Umgekehrt setzt `bergwald_kiefer` in Kernbiomen Wald unter 170–230 m – falls Houdini-
   Bestand dort schon Bäume hat, hält der 4-m-Abstand sie auseinander, die Dichte 0,006 kann aber zu viel sein (`stufen[0]` auf 0,5).
5. **Schema-Toleranz.** `welt.json["kacheln"]` als Dict oder Liste, Rezepte über Schlüsselwörter (gletscher/eis/schnee → gletscher, wald →
   bergwald, vulkan → lava, unbekannt → Feldbiom mit Hinweis); `felsschalen/plan_<Feld>.json` tolerant nach `x/y`-Dicts und 7/10-Tupeln;
   `instanzen.json` nur über `<name>.f32` neben der JSON auswertbar – sonst Hinweis.
6. **`entfernen` wirkt feldweit.** Der Witcher-Vorschlag (Farn/Ahorn/Weide/Kraut) ist deshalb nur für E1/F2 sinnvoll; in C2/D2/E2 bleibt die
   Witcher-Ebene vollständig und über der Baumgrenze können Farne stehen – dort hilft nur ein höhenabhängiger Filter im Setzer (offen).
7. **Kein Nanite bei Latsche/Alpenrose/Krüppelkiefer/Gras_03** (Mountain/Coast_Dunes): 7 000 + 10 000 + 1 500 Instanzen ohne Nanite je Feld
   kosten VSM; Cull 350 m ist gesetzt, WPO begrenzen (`boden-kleinzeug-gras.md`). Einkaufsliste priorisiert deshalb Latsche/Lärche.
8. **Eiszapfen am Budget (1 500)** im Synthetik, weil 18 % Wand > 55°; mit Echtdaten (E1 65 % steil > 30°) ähnlich. Zu viele → `eiszapfen.
   dichte_je_m2` 0,04 → 0,02 oder `hang_min_grad` 60.
9. **Schneegrenze als Höhe ist in Eldarien nachrangig**: E2/F2/E3 tragen Schnee als Lage bei 40–140 m. Der Planer behandelt beide Fälle
   gleich (Stufe 3), aber Stufe 2 (Matte) fehlt dann dazwischen – für E2 ggf. `lage_schnee_als_stufe3_ab` auf 0,7 heben, damit ein
   Alpenrosen-Saum um die Schneefelder entsteht.
10. **Nicht geprüft:** Setzer-Verhalten mit 112 Netzen je Feld (Foliage-Typ-Anzahl `FT_EL_HG_*` ≈ 110), HLOD der Nicht-Nanite-Pflanzen,
   Abstimmung mit Teil C (Overrides müssen in `felsgruppen_regeln.json` übernommen werden; nicht automatisch).

## Quellen

- Repo: `vorlagen/FORMAT.md`; `vorlagen/daten/biome_je_feld.md`; `vorlagen/doku/ANALYSE_WITCHER_2026-10-08.md`; `antworten/bildkritik-witcher-messlatte.md`;
  `antworten/assets-taxonomie.md` (Paletten/Lücken gletscher, frost, tundra); `antworten/verteilung-fels-organisch.md` (Hash-Zufall, Raster-Operatoren, Kameras);
  `antworten/verteilung-leere-fuellen.md` (Spuren-Regeln); `antworten/klippennetze-a5.md`; `antworten/boden-kleinzeug-gras.md`.
- Witcher (Suchauszüge): [Vice – Designing the World of The Witcher 3](https://www.vice.com/en/article/designing-the-world-of-the-witcher-3-wild-hunt/);
  [ArtStation Lukasz Lakomski – The Witcher 3](https://www.artstation.com/artwork/Z6Ql0); [CDPR Press – Witcher 4 UE5 Tech Demo, State of Unreal 2025](https://press.cdprojektred.com/en/news/1778/cd-projekt-red-and-epic-games-present-the-witcher-4-unreal-engine-5-tech-demo-at-the-state-of-unreal-2025);
  [CGMagazine – Witcher 4 UE 5.6 Tech Demo](https://www.cgmagonline.com/news/the-witcher-4-tech-demo-state-of-unreal/).
- Höhenstufen (Suchauszüge): [Lexikon des Agrarraums – Höhenstufen](https://www.agrarraum.info/lexikon/hoehenstufen); [Biber Berti – Flora & Höhenstufen](https://biberberti.com/fur-teens/themen/alpen/menschen/flora-hohenstufen/);
  [wirtschaftsgeografie.com – Alpen](http://www.wirtschaftsgeografie.com/Physische_Geografie/Alpen/body_alpen.html); [GRIN – Höhenstufen des Waldes in den Alpen](https://www.grin.com/document/96126);
  [Wikipedia – Höhenstufe (Ökologie)](https://de.wikipedia.org/wiki/H%C3%B6henstufe_(%C3%96kologie)).
- Botanik (Suchauszüge): [Flora Kleinwalsertal – Latsche](https://flora-kleinwalsertal.at/latsche_pinus-mugo/); [Wikipedia – Bergkiefer](https://de.wikipedia.org/wiki/Bergkiefer);
  [Wikipedia – Rhododendron ferrugineum](https://en.wikipedia.org/wiki/Rhododendron_ferrugineum); [Open Flora – Rostblättrige Alpenrose](https://www.openflora.ch/de/wiki/rostblaettrige-alpenrose-rhododendron-ferrugineum-402.html).
- Assets (Suchauszüge): [Fab – Transition FAQs](https://support.fab.com/s/article/Fab-Transition-FAQs?language=en_US); [CG Channel – 22 free Megascans trees](https://www.cgchannel.com/2021/12/download-22-free-megascans-3d-trees-for-unreal-engine/);
  [Wikipedia – Larix decidua](https://en.wikipedia.org/wiki/Larix_decidua); [Epic – Fab launch](https://www.epicgames.com/site/news/fab-epics-new-unified-content-marketplace-launches-today).
