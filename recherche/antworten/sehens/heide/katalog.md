# Heide – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1, Biom-Agent B5)

Stand 11.10.2026 · Daten: `vorlagen/daten/sehens` (2 m) · Werkzeuge: `antworten/skripte/sehens_lib` · Dateien: `standorte.json`
(8 Orte, keine Pfade nötig, Prüfer **0 FEHLER** für heide), `asset_bedarf.json`, `<id>.png` je Ort (Draufsicht mit geplantem Stempel, Elementen, Kameras).
Inventar: Stand 13b (1 692 Netze).

## Das Biom in Zahlen – und was daraus folgt

Heide = 1,59 km² (Felder F4–G5, Streifen H4/H5), eine **Granit-Felsenheide** auf einer niedrigen Platte (Höhe −7…53 m, Hang-Median 4°):
Trockengras 34 %, Wiese 20 %, Laub 13 % (Birkensaum im Norden/Osten), Moos 8 %, Heide 7 %, Geröll 6 %, Schlamm 5 %, Felsplatte 2 %.
Granitbuckel mit Felsplatten (Tors) bei X 1 230–1 420 / Y 450–480 und auf dem Nord-Süd-Rücken X 1 950–2 120; Bäche fließen nach Westen
zur Küste. Ein westlicher Sand-/Wiesenstreifen (X 360–650) ist ohne Wege.

| Kennzahl | Wert |
|---|---|
| Fläche ≤ 80 m / ≤ 300 m vom Weg | 0,65 / 1,35 km² (größter Abstand 630 m) |
| zulässige Zone (80–300 m, Biom innen ≥ 30 m) | 0,58 km² |
| max. Orte bei 350 m | 11 (Greedy); mit den Nachbarn aue_08 (1 196 / −470), dschungel_01/02 (Y ≈ 960), elfenwald_06 (2 112 / −390) eng |
| Verdeckung heute (Ziel 1,5 m, 20-m-Raster der Zone) | nur 192 von 1 496 Rasterpunkten verdeckt – die Heide ist **offen und dicht bewegt** |

**Folge:** Wege liegen überall 80–150 m entfernt; Fundstücke sind nur über **Hohlformen mit Rahmen** zu verstecken (Kessel, Klamm,
Parabeldüne, Moorkuppe mit Krüppelkiefern). Jeder Fundstück-Stempel wurde mit `sicht.py` auf der gestempelten Höhe nachgerechnet
(Kern + 4 Proben, Ziel 1–1,5 m, alle Wegpunkte ≤ 400 m). **3 Leuchtfeuer + 5 Fundstücke.** Zwei Orte wurden nach der Koordinator-Meldung
verschoben (Totengrund ≥ 350 m zu aue_08, Ginstergold ≥ 350 m zu dschungel_02); alle Abstände ≥ 352 m.

**Abgrenzung:** Alles ist **Granit + Heide + Hochmoor** (Dartmoor/Lüneburger Heide). Gestrichen aus Katalog v1: **Der Rachen**
(Schluckloch braucht Kalk), **Karrenfeld** (Kalk), **Blockstrom** (zu nah an bergwald_04 Felsenmeer). Felsburg ≠ bergwald (dort Mönch/
Säulen aus Klippe), Kolk = Hochmoor-Kolk auf der Platte (nicht Sumpf-Bruchwald; sumpf-Katalog lag nicht vor). Tors/Wollsäcke nur hier,
nicht in der Tundra (dort Findling = fremder Block).

## Übersicht

| ID | Name | Art | Form | Feld | X / Y (m) | Weg | Sicht/Verdeckung (mit Stempel) |
|---|---|---|---|---|---|---|---|
| heide_01_die_graue_burg | Die Graue Burg | Leuchtfeuer | Granit-Tor (Wollsack-Stapel) auf Kuppe | F5 | 1310 / 466 | 84 m | 119 von 183 Wegpunkten, bis 795 m |
| heide_02_ginstergold | Ginstergold | Leuchtfeuer | Ginster-/Erikahang in Blüte | G5 | 2295 / 610 | 155 m | 38 von 252, bis 702 m (Farbfläche) |
| heide_03_die_wacholderprozession | Die Wacholderprozession | Leuchtfeuer | Wacholderzug auf flachem Rücken | G4 | 1890 / −80 | 198 m | 82 von 328, bis 800 m |
| heide_04_der_kolk | Der Kolk | Fundstück | Hochmoor-Kolk in Felsrahmen | G5 | 1790 / 595 | 205 m | **verdeckt** (5/5, max. Anteil 0,13) |
| heide_05_der_wackelstein | Der Wackelstein | Fundstück | Wackelstein im Wollsack-Kessel | G5 | 2095 / 320 | 93 m | Kern verdeckt, 4/5 Proben |
| heide_06_der_wollsackfall | Der Wollsackfall | Fundstück | Bachkaskade über Wollsäcke in Klamm | G5 | 1498 / 165 | 115 m | Klamm-Kern verdeckt, 3/5 Proben |
| heide_07_der_totengrund | Der Totengrund | Fundstück | Heidekessel (Nivationsmulde) | F4 | 1310 / −135 | 85 m | Kern verdeckt, 3/5 Proben |
| heide_08_die_windkante | Die Windkante | Fundstück | Parabeldüne mit Windanriss und Windkiefern | F5 | 985 / 330 | 111 m | **verdeckt** (5/5, max. 0,28 von 1 Punkt) |

---

## heide_01_die_graue_burg – Die Graue Burg (Leuchtfeuer)

**Was man sieht:** Auf der Kuppe über zwei Bächen türmen sich graue Granitplatten zu drei Stapeln, der höchste 11 m: waagerecht
geklüftet, die Kanten zu Wollsäcken gerundet, als hätte ein Riese Kissen gestapelt. Hangab ein Meer aus abgestürzten Blöcken (Clitter),
zwischen dem Heidekraut und Farn wachsen; am Fuß eine vom Wind geduckte Eberesche.
**Vorbild:** Haytor und Hound Tor (Dartmoor), Wollsackverwitterung im Fichtelgebirge (Luisenburg); Spiel: Felskuppen in Toussaint
(The Witcher 3), Fallow Mire/Hinterland-Tore (DA:I).
**Standort:** F5, X 1310 / Y 466 m, Boden 22,3 m. Kuppe TPI100 **+13,9 m**, TPI25 +8,5 m, vorhandene Felsplatten 22 %, Heide 27 %,
Moos 26 %. Weg 84 m, Bach 37 m.
**Sicht:** Ziel 12 m: **119 von 183** Wegpunkten (Mittel 0,63), bis 795 m – der beste Leuchtturm der Heide; `_fern` von X 1598 / Y 56 (501 m).
**Komposition und Anmarsch:** Zugang 108 m (max. 24,6°) über den Clitter. `_held` von Südwest: Blockschutt und Heide im Vordergrund,
Haupttor als Silhouette, Nebenstapel staffeln nach rechts.
**Detail-Ebenen:** Held – Haupt-Tor aus `SM_flat_rock_02/03/04` und `SM_big_rock_wall_01/02/03` horizontal gestapelt (versetzt, Fugen
mit Moos), Kappe `SM_mountain_rock_big_02_6`; alles `MI_EL_SW_Granit_Heide`. Begleiter 2 Stapel (7 m, 5 m) aus
`SM_mountain_rock_big_02_1/_4/_8`, `SM_Big_Rock_01/02/03`. Schutt 80–150 – Clitter hangab (`SM_Middle_Rock_01`, `SM_Rock_01/03/05`,
Granit `pjEr1_tier_0`, `pjtsT_tier_0`, `pkeeM_tier_0`, `xf3odif_tier_0`, `xfplcbf_tier_0`), groß unten, klein oben (Ursache: Abbrechen der
Klüfte). Kleinzeug – `SM_s_rock_01/02`, Grus (Lage Kies). Bewuchs nach Ursache – Clitterfugen: Besenheide `SM_forest_heather_01`,
`SM_forest_heather_simple_01`, Heidelbeere `SM_billberry_01/03`, Adlerfarn `SM_EagleFern_M_01`, `SM_EagleFern_S_02`; Windflüchter:
`SM_pine_beach_crooked_02` und eine Birke `Big_Tree_Birch_01` (×0,6) im Lee; Krüppelkiefer `SM_dwarf_pine_medium_02` in einer Kluft.
Kontaktzone – Platten 30 % eingegraben, Moospolster `SM_MossClump_03` auf den Absätzen.
**Wasser, Effekte, Licht:** kein Wasser. Felsschüsseln auf dem Gipfelstapel mit Regenwasser (Decal). Abendlicht von Westen auf grauem Fels.
**Geländeänderung:** Kuppe +2 m (r 26 m), Fenster 78 × 78 m.
**Assets:** Bestand reicht. Wunsch B „Brushify – Moorlands Pack“ (UK-Granit + Heidekraut, neu, siehe `asset_bedarf.json`).
**Aufwand und Risiko:** mittel. Risiko: Stapel wirkt gemauert → Platten verkippen (2–6°), Fugen ungleich, Kanten gerundet.
Budget: ~6 000 Instanzen (900 Kollision), 45 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

## heide_02_ginstergold – Ginstergold (Leuchtfeuer)

**Was man sieht:** Ein ganzer Osthang am Rand des Birkenwalds glüht gelb: dichte Ginsterbüsche in voller Blüte, dazwischen ein purpurner
Saum aus blühender Besenheide. Ein grauer Granitblock trägt einen Kranz aus Ginster. An einer Stelle verkohlte Stummel – ein alter
Heidebrand, aus dem junger Ginster schießt.
**Vorbild:** Ginsterheiden der Bretagne und von Exmoor im Mai; Lüneburger Heide im August (Erika); Spiel: Blütenfelder in Toussaint
(The Witcher 3), Farbtupfer-Wiesen der Smaragdgräber (DA:I).
**Standort:** G5, X 2295 / Y 610 m, Boden 19,7 m. Lichtung am Waldrand (Laub 49 %, Gras 35 %, Schlamm 16 %), Hang 11°, 58 m im Biom.
Weg 155 m; nach Verschiebung 352 m zu dschungel_02.
**Sicht:** Ziel 4 m (Strauchhöhe + Farbfläche): **38 von 252** Wegpunkten (Mittel 0,15), bis 702 m; `_fern` vom Rückenweg X 2086 /
Y 156 (500 m) – der Hang liegt dem Weg frontal gegenüber. Leuchtfeuer durch **Farbe**, nicht Höhe (ehrlich: schwächstes Leuchtfeuer).
**Komposition und Anmarsch:** Zugang 160 m (max. 11,7°). `_held` von Südwest, Blick hangauf: Ginstermasse, Granitblock, dahinter
dunkler Birkenwald als Kontrast.
**Detail-Ebenen:** Held – Granitblock `SM_mountain_rock_big_02_3` + `pkeeM_tier_0`. Begleiter 30–50 Ginsterbüsche (Lücke →
`SM_sea_buckthorn_01/02/03/05` mit `MI_EL_SW_Ginster`, Blüten aus `SM_flower_goldenrod_01/02`, `SM_flower_common_Saint_John_s_wort_01`,
`SM_YellowArchangel_04/08`, `SM_Crownbeard_03/07` in Clustern). Schutt – Brandfläche: `SM_BirchTreeStump_01`, verkohlte Zweige
`SM_branch_01_1` (Ruß-Decal). Bewuchs nach Ursache – Ginster nur auf dem trockenen Oberhang (Sonne), Erika-Saum unten
(`SM_forest_heather_01`, `SM_heath_A_01/B_01` mit `MI_EL_SW_Erika_Bluete`), trockenes Gras `SM_dead_grass_01/02`, `SM_grass_bush_02`,
Jungginster auf der Brandfläche. Kontaktzone – Lage Trockengras/Heide, Gelb als GPU-Gras (Kraut) dazwischen.
**Wasser, Effekte, Licht:** keines; Insektensummen als Klang (Vögel-CUE prüfen). Gegenlicht macht das Gelb hell.
**Geländeänderung:** keine.
**Assets:** Lücke Ginster/Stechginster (kein Fab-Listing gefunden) → Ersatz wie oben; B „Brushify – Moorlands Pack“ für Erika.
**Aufwand und Risiko:** mittel; Risiko: Sanddorn-Ersatz wirkt nicht wie Ginster → Prüfbild, ggf. CGTrader-Modell (Ferat entscheidet).
Budget: ~12 000 Instanzen (300 Kollision), 4 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

## heide_03_die_wacholderprozession – Die Wacholderprozession (Leuchtfeuer)

**Was man sieht:** Über einen flachen Rücken zieht sich eine Reihe dunkler, säulenförmiger Wacholder – 45 Gestalten von 3 bis 7 m, alle
in dieselbe Richtung, wie eine Prozession von Mönchen auf dem Weg nach Nordosten. In der Mitte ein silbergrauer, abgestorbener Wacholder,
am Ende ein einzelner Findling.
**Vorbild:** Wacholderheiden Lüneburger Heide (Totengrund, Wilsede), Haselünner Wacholderhain; Spiel: Silhouettenbäume im Hinterland (DA:I).
**Standort:** G4, X 1890 / Y −80 m, Boden 25,5 m. Flacher Rücken (Hang 2,6°, Ebene), Trockengras 69 %, 16 Baumzellen (lichter Saum).
Weg 198 m; 381 m zu elfenwald_06.
**Sicht:** Ziel 6 m: **82 von 328** Wegpunkten (Mittel 0,19), bis 800 m; mit dem 1,2-m-Rücken (Stempel) 12 Wegpunkte mehr als heute;
`_fern` vom Rückenweg X 1986 / Y 340 (431 m).
**Komposition und Anmarsch:** Zugang 212 m (max. 17,2°). `_held` vom Osten auf Augenhöhe gegen den Himmel: die Säulen als dunkle Figuren.
**Detail-Ebenen:** Held – Totwacholder `SM_DeadTree_02` (×0,8, silbergrau). Begleiter 45 Säulen (Lücke Wacholder → `SM_Forest_pine_plant_01/02/03`,
`Fir_01_Plant`, `Fir_02_Small` nicht-uniform skaliert sx = sy 0,45–0,6, sz 1,1–1,5, `MI_EL_SW_Wacholder`), dazu `SM_dwarf_pine_big_01/02` als
niedrige Wacholderbüsche; `SM_Forest_pine_10_dead` liegend. Findling `SM_NordicBoulder_01` (×0,5), `SM_Rock_02`. Kleinzeug –
`SM_branch_01_1`, `SM_dead_grass_03`. Bewuchs nach Ursache – Lichtung mit Besenheide (`SM_forest_heather_01`, `SM_heath_cross_01`), trockene
Horste `SM_grass_bush_01`, Adlerfarn `SM_EagleFern_S_01` im Halbschatten. Kontaktzone – Nadelstreu (Lage Nadeln) unter jeder Säule.
**Wasser, Effekte, Licht:** keines. Wind (`CUE_Wind_Autumn_wind_with_leaves_rustling_Cue`).
**Geländeänderung:** sanfter Rücken +1,2 m entlang der Prozession (Fenster 170 × 144 m).
**Assets:** Lücke Wacholder (kein Fab-Listing) → Ersatz; B „Brushify – Moorlands“ für Bodendecker.
**Aufwand und Risiko:** mittel; Risiko: Säulenform aus Kiefer-Jungpflanzen → Prüfbild entscheidet.
Budget: ~5 000 Instanzen (100 Kollision), 50 Akteure, 0 Lichter, 0 Niagara, 0 Decals.

## heide_04_der_kolk – Der Kolk (Fundstück)

**Was man sieht:** Hinter einem Kranz aus Granitplatten und Krüppelkiefern wölbt sich ein Hochmoor, rot-grün gesprenkelt von Torfmoos-
Bulten. In seiner Mitte liegt ein kreisrundes, schwarzes Wasserauge, so glatt, dass sich die Wolken darin spiegeln. Silberne
Birkenskelette stehen am Rand, Wollgras weht.
**Vorbild:** Hochmoor-Kolke im Pietzmoor (Lüneburger Heide) und auf Dartmoor (Fox Tor Mires); Spiel: Moorauge im Wald von Crookback Bog
(The Witcher 3) – hier ohne Ruine.
**Standort:** G5, X 1790 / Y 595 m, Boden 16,7 m. **Vorhandene** ovale Mulde (Schlamm 99 %, flach 1°) mit Felsrahmen im Westen/Süden
(Rand 21–24 m). Weg 205 m.
**Verdeckung:** mit Moorkuppe, Felsrahmen (+1,5 m im Nordosten) und Krüppelkiefernsaum (3,5 m): **alle 5 Proben verdeckt**
(max. Anteil 0,13 bei 115–122 Wegpunkten ≤ 400 m); heute 4 Wegpunkte mit Sicht (282 m).
**Komposition und Anmarsch:** Zugang 221 m (max. 19°) von Süden durch eine Lücke im Felsrahmen – erst dort öffnet sich das Wasserauge.
`_held` auf dem Südrand, Blick nach Norden über die Bulten auf den Kolk.
**Detail-Ebenen:** Held – Kolk (Wasser). Begleiter – Krüppelkiefern `SM_dwarf_pine_small_01/02`, `SM_dwarf_pine_medium_01/03`,
`SM_pine_beach_short_01/02`, Birkenskelette `SM_DeadTree_01`, `SM_BirchTreeStump_01`. Schutt – Felsplatten `SM_flat_rock_03`,
`SM_MossyRocks_01` am Rahmen. Kleinzeug – `SM_branch_01_1`, Torfmoos `SM_MossClump_01/02/05`, `SM_moss_01/02`. Bewuchs nach Ursache –
Bulten trocken: `SM_heath_A_01`, `SM_lingonberry_01`, `SM_billberry_dry_01`; Schlenken nass: Binsen `SM_ToadRush_00/010/014`
(Wollgras-Lücke). Kontaktzone – Kolkrand schwingend (Moos bis an die Wasserlinie, kein Kies), Nassband.
**Wasser, Effekte, Licht:** `see` 22 × 16 m, `schwarz_spiegel`, 2,5 m tief; Bodennebel `lokaler_nebel` (0,05) in der Mulde; Klang
`CUE_Water_Stream_IV_Cue` sehr leise. Spiegelung ist das Bild.
**Geländeänderung:** Moorkuppe +1,2 m (100 × 80 m), Kolk −2,5 m, Felsrahmen NO +1,5 m; Fenster 140 × 134 m.
**Assets:** Bestand; B „Brushify – Moorlands“ (Heide auf Bulten). Seerose bewusst nicht (Hochmoor nährstoffarm).
**Aufwand und Risiko:** gering–mittel.
Budget: ~7 000 Instanzen (300 Kollision), 15 Akteure, 0 Lichter, 0 Niagara, 1 Nebel, 4 Decals.

## heide_05_der_wackelstein – Der Wackelstein (Fundstück)

**Was man sieht:** Zwischen den Granitplatten des Rückens führt ein Durchschlupf in einen runden Felsenkessel, ummauert von
Wollsäcken. In der Mitte ruht ein 4,5 m großer, gerundeter Block auf einer einzigen Kippkante – man meint, ein Stoß würde ihn wiegen.
Auf einem Nachbarstein eine Felsschüssel voller Regenwasser.
**Vorbild:** Logan Rock (Cornwall), Wackelsteine im Fichtelgebirge; Opferkessel (Verwitterungsschüsseln) im Granit; Spiel: Rätselsteine
in Skellige.
**Standort:** G5, X 2095 / Y 320 m, Boden 24,1 m. Südostflanke des Granitrückens (Felsplatte 14 %, Plattenfeld vorhanden), Weg 93 m.
**Verdeckung:** Kessel −3,2 m mit Wollsack-Kranz +2,2 m: **Kern und 3 Proben verdeckt**; Ostprobe am Kesselrand von 14 Wegpunkten im
Tiefland Ost (340–370 m, Anteil ≤ 0,60) sichtbar. Heute 18 Wegpunkte, nächster 85 m.
**Komposition und Anmarsch:** Zugang 98 m (max. 16,8°) über den Durchschlupf Südwest. `_held` aus dem Durchschlupf: Rahmen aus Fels links
und rechts, Wackelstein in der Mitte.
**Detail-Ebenen:** Held – `SM_mountain_rock_big_02_5` (gerundet) auf `SM_flat_rock_04`, Kippkante sichtbar. Begleiter 8–12 Kranzblöcke
`SM_mountain_rock_big_02_2/_7`, `SM_Big_Rock_01/02`, `SM_ground_rock_03_03`, `pjEr1_tier_0`, `pjtsT_tier_0`. Schutt 40–80 – `SM_Rock_04/06/07`,
`SM_s_rock_03`. Bewuchs nach Ursache – Kesselboden geschützt: Heidelbeere `SM_billberry_02`, Besenheide `SM_forest_heather_simple_01`,
Farn `SM_EagleFern_S_04`, Weide `SM_grey_willow_03` am Wasser der Schüssel; Moos `SM_MossClump_04` auf der Nordseite.
Kontaktzone – Grus (Lage Kies) am Fuß jedes Blocks.
**Wasser, Effekte, Licht:** Felsschüssel als Decal + kleine `see` (1,5 m, `klar`). Kessel im Schatten, der Wackelstein im Licht.
**Geländeänderung:** Kessel −3,2 m (r 13 m), Kranz +2,2 m (Ring r 17 m); Fenster 70 × 70 m.
**Assets:** Bestand; B „Brushify – Moorlands“ (UK-Granit).
**Aufwand und Risiko:** gering.
Budget: ~3 000 Instanzen (500 Kollision), 20 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

## heide_06_der_wollsackfall – Der Wollsackfall (Fundstück)

**Was man sieht:** Neben einer 5 m hohen Granitrippe hat sich der Heidebach eine schmale Klamm gegraben. Über drei Stufen aus gerundeten
Wollsäcken fällt er insgesamt 4 m in eine klare Gumpe; Gischt netzt Farne und Moos, eine Eberesche hängt über dem Kopf der Klamm.
**Vorbild:** Becky Falls und Lydford (Dartmoor), Bachkaskaden im Fichtelgebirge (Egerquelle); Spiel: Waldbäche in Velen (The Witcher 3).
**Standort:** G5, X 1498 / Y 165 m (Kern = Fallstufe X 1476 / Y 160), Boden 18,9 m. Vorhandene N-S-Felsrippe (4–5 m) neben dem Bach
(Gefälle 19 → 13 m auf 130 m), Weg 115 m.
**Verdeckung:** Klamm −3,5 m + Wollsack-Ufer West +1,8 m + Ebereschen am Klammkopf, Erlen am Ausgang: **Kern, Süd- und Nordprobe
verdeckt**, Westprobe 1 Wegpunkt (0,28); Ostprobe auf der Rippenkante 40 Wegpunkte (die Rippe selbst ist heute schon sichtbar).
**Komposition und Anmarsch:** Zugang 130 m vom Weg Nord ohne Pfadbau (max. 31,7° nur auf 4 m am Klammrand → 5–6 Steinstufen
`SM_flat_rock_03` als Instanzen, kein Pfad nötig). `_held` von unten auf der Kiesbank, Blick bachauf auf die drei Stufen.
**Detail-Ebenen:** Held – Fallstufen aus `SM_mountain_rock_big_02_1/_6`, `SM_Big_Rock_03` quer im Bett. Begleiter 5–8 – Wollsäcke
`SM_Middle_Rock_01`, `SM_Rock_01/05`, `SM_MossyForestBoulder_04`, `SM_MossyForestRock_02`. Schutt 60–100 – Bachkiesel `SM_stones_01_2/_4`,
`SM_DryRiverBed_01`. Kleinzeug – Laub `SM_detail_leaves_02`, Wurzeln `SM_Pine_roots_02`. Bewuchs nach Ursache – Spritzzone: Farne
`SM_Fern_02`, `SM_SilverLadyFern_01`, Moos `SM_MossClump_01/03`; Klammkopf: Eberesche-Ersatz `Big_Tree_Birch_01`, `SM_beech_tree_00_B`;
Rand: Adlerfarn `SM_EagleFern_M_01`. Kontaktzone – Nassband, Moos auf allen bachseitigen Steinflanken.
**Wasser, Effekte, Licht:** vorhandener Bach (Ort IST dieses Wasser) mit 3 Stufen > 0,8 m → kleine Wasserfälle; `see` Gumpe 12 × 9 m
`klar`; Schaum am Fuß; Klang `CUE_Water_Stream_IX_Cue`/`_X_Cue`. Lichtfleck durch die Ebereschenkrone.
**Geländeänderung:** Klamm −3,5 m (Band 16 m, 100 m lang), Gumpe −1,5 m, Ufer West +1,8 m; Fenster 78 × 136 m; |Δ| an Wasser 4,6 m (erlaubt).
**Assets:** Download A „Mountain – Environment Set“ (Wasserfallmaterial, lädt Ferat gerade); Ersatz `M_EL_Wasserfall2`.
**Aufwand und Risiko:** mittel–hoch (Wasser + Gelände).
Budget: ~6 000 Instanzen (600 Kollision), 25 Akteure, 0 Lichter, 1 Niagara (Gischt, optional), 4 Decals.

## heide_07_der_totengrund – Der Totengrund (Fundstück)

**Was man sieht:** Hinter einer Hangkante öffnet sich ein runder, 4 m tiefer Kessel, dessen Hänge vollständig mit blühender Besenheide
bedeckt sind – ein purpurner Trichter. Auf dem sandigen Grund silbernes Gras, drei dunkle Wacholder stehen wie Wächter, ein Birkensaum
umrahmt den Rand. Nach Nordwesten läuft ein trockenes Tälchen aus.
**Vorbild:** Totengrund bei Wilsede (Lüneburger Heide) – periglaziale Nivationsmulde; Spiel: versteckte Lichtungen in den Smaragdgräbern (DA:I).
**Standort:** F4, X 1310 / Y −135 m, Boden 21,2 m. Hangfuß unter dem Birkensaum (Heide 37 %, Trockengras 35 %, 39 Baumzellen),
Hang 13°. Weg 85 m; 352 m zu aue_08 (nach Verschiebung).
**Verdeckung:** Kessel −4 m, Westrand +3 m, Auslauf nach NW: **Kern, West- und Südprobe verdeckt**; Ost-/Nordprobe am Kesselhang von 3 bzw. 7
Wegpunkten (Anteil ≤ 0,62/1,0, 138–146 m, Weg West, tiefer) einsehbar. Heute 13 Wegpunkte.
**Komposition und Anmarsch:** Zugang 89 m (max. 21°) über den Rand – der Kessel erscheint plötzlich unter den Füßen. `_held` vom Ostrand
in den Trichter, Wacholder als Maßstab.
**Detail-Ebenen:** Held – Kessel (Gelände) + drei Wacholder (Ersatz `SM_Forest_pine_plant_02/03`, `MI_EL_SW_Wacholder`). Begleiter –
`SM_DeadTree_02` (Totholz), Birken `Big_Tree_Birch_01` am Rand. Schutt – Sandabbrüche am Kesselrand `SM_sandy_slope_01/03`, Steine
`SM_Rock_02`, `SM_s_rock_02`. Kleinzeug – `SM_branch_01_1`, Silbergras `SM_beach_grass_02_1/_3`, `SM_dead_grass_01`. Bewuchs nach Ursache –
Hänge Besenheide (`SM_forest_heather_01`, `SM_forest_heather_simple_01`, `SM_heath_A/B_01`, `SM_heath_cross_01` mit `MI_EL_SW_Erika_Bluete`),
Grund Sand (Lage Sand) mit Silbergras, Heidelbeere `SM_billberry_03` im Schatten der Birken. Kontaktzone – Sandrand mit Wurzeln.
**Wasser, Effekte, Licht:** keines; Stille (Wind gedämpft). Der Kessel fängt Abendlicht, der Rand bleibt dunkel.
**Geländeänderung:** Kessel −4 m (68 × 56 m), Westrand +3 m, Auslauf −1,2 m; Fenster 102 × 122 m.
**Assets:** Lücke Wacholder; B „Brushify – Moorlands“ (blühende Heide).
**Aufwand und Risiko:** gering–mittel.
Budget: ~10 000 Instanzen (100 Kollision), 6 Akteure, 0 Lichter, 0 Niagara, 0 Decals.

## heide_08_die_windkante – Die Windkante (Fundstück)

**Was man sieht:** Am Westrand der Heide, wo der Seewind auf das Land trifft, hat der Sand eine hufeisenförmige Düne aufgeworfen, 4 m hoch,
die Arme zum Meer gestreckt. In ihrem Innern ein ausgeblasener Kessel aus hellem Sand mit Rippelmarken; an der Kante stehen
windgekrümmte Kiefern, deren Wurzeln frei in der Luft hängen. Auf dem Sandboden blankgeschliffene Windkanter.
**Vorbild:** Parabeldünen und Windanrisse im Hohen Venn/Lieberoser Heide, Kiefern-Windflüchter auf Sylt; Spiel: Sturmküste (DA:I).
**Standort:** F5, X 985 / Y 330 m, Boden 1,6 m. Küsten-Geröllflur (Geröll 61 %, Wiese 31 %) 82 m vom Meer, flach. Weg 111 m.
**Verdeckung:** Parabeldüne (+4 m, offen nach Westen): **alle 5 Proben verdeckt**, max. Anteil 0,28 von 1 Wegpunkt (Westprobe, 120 m);
heute 40 Wegpunkte.
**Komposition und Anmarsch:** Zugang 122 m (max. 11,6°) über den Dünenarm; `_held` auf dem Kamm Ost, Blick in den Kessel und durch die
offene Westseite aufs Meer.
**Detail-Ebenen:** Held – Windkiefern `SM_pine_beach_crooked_01/02` an der Abbruchkante mit freigelegten Wurzeln (`SM_stones_roots_01/03`,
`SM_Pine_roots_01`, `SM_crooked_root_01`). Begleiter – `SM_pine_beach_medium_01/03`, `SM_pine_beach_small_04`. Schutt – Sandabbrüche
`SM_sandy_slope_02/04/05`, `SM_scarp_01`; Windkanter `SM_namaqualand_rocks_01_a_NN`, Kiesel `SM_BeachSandWithPebbles_01`. Kleinzeug –
`SM_branch_01_1`. Bewuchs nach Ursache – Kessel kahl (Wind), Dünenkamm Strandhafer `SM_beach_grass_01_1`, `SM_beach_grass_01_hp_1`,
`SM_beach_grass_03_2`, Leeseite Heide `SM_forest_heather_simple_01`, Stranddistel `SM_sea_holly_01`. Kontaktzone – Lage Sand, Rippel-Decal.
**Wasser, Effekte, Licht:** keines; Sandfahnen optional (C). Wind-Klang. Grelles Licht auf hellem Sand.
**Geländeänderung:** Parabeldüne +4 m (Kamm 9 m breit), Fenster 114 × 126 m; nichts unter 0 m.
**Assets:** Download A „Coast & Dunes“ (Dünenstempel, Sand-Decals – lädt Ferat gerade); sonst Bestand. Abgrenzung kueste: dort Brandung/
Fels; hier Sandheide mit Kiefern.
**Aufwand und Risiko:** gering–mittel.
Budget: ~6 000 Instanzen (200 Kollision), 15 Akteure, 0 Lichter, 0 Niagara, 4 Decals.

---

## Pfade

Keine. Alle Heide-Orte liegen 84–205 m von bestehenden Wegen und sind ohne Pfadbau erreichbar (`erreichbar.modus = streng`, max. 11–25°;
Wollsackfall nur 4 m mit 31,7° → Steinstufen als Instanzen). `standorte.json` enthält `"pfade": []`.

## Offene Fragen an Ferat

1. **Ginster und Wacholder** gibt es auf Fab nicht (Websuche 11.10.) – Ersatz aus Sanddorn/Jungkiefern ok, oder soll ich Modelle außerhalb
   Fab (CGTrader „Ulex europaeus“, Gumroad „Juniper“) prüfen lassen?
2. „Brushify – Moorlands Pack“ (Heidekraut + UK-Granit) – evtl. schon in deiner Bibliothek? Preis ungeprüft.
3. heide_02 Ginstergold liegt nach der Verschiebung an einer Waldrand-Lichtung (Laub 49 %) – Leuchtfeuer nur über die Farbe (38 Wegpunkte).
4. Bildwünsche (leer): Graue Burg (Kuppe), Kolk-Mulde (Kameras in `asset_bedarf.json`).
