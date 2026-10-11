# Gletscher – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

> **Nachtrag 13c (Pfade, 11.10.2026):** Ferat will Pfade ausdrücklich („lieber ein Pfad mehr als ein Ort weniger“). Alle 8 Orte stehen jetzt in `standorte.json`; die Steige sind dort unter `pfade` eingetragen (`gletscher_pfad_weststeig`, `gletscher_pfad_oststeig`, `gletscher_pfad_nordhang`), die Orte tragen `pfad_id`. Die früheren Variantendateien `standorte_*.json` gibt es nicht mehr – Erwähnungen unten sind historisch, „nur mit Steig“ heißt jetzt „am Pfad“. Prüfer über alle Biome: 0 FEHLER.
>
> Drei Serpentinen erschließen den Gletscherkessel: der Weststeig (1,5 km) von der Straße am Frostlager zu Moränensee und Wächte, der Oststeig (1,3 km) vom östlichen Straßenende zu Gletschertöpfen und Nunatak, und der Nordhang (730 m) als Abzweig vom Weststeig zum Gletscherschliff. Die Linien steigen bis 34–40°; Kehren und Felsstufen rechnet Ferats Serpentinen-Werkzeug.


Stand 11.10.2026 · Agent B4 · Dateien: `standorte.json` (heute gültige Orte), `standorte_steige.json` (Orte, die einen neuen Steig brauchen, mit Steig-Polylinien), je Ort `<id>.png` (Draufsicht 2 m, Steige orange, Zugangspfad gelb), `asset_bedarf.json`. Alle Zahlen aus den 2-m-Daten mit `antworten/skripte/sehens_lib` (Cache, Sichtlinien Gelände + `baumhoehe_4m`, Wegpunkte 20 m); eigene Scores/Skripte im Scratchpad `a13/b4_eis_fjord/` (`kand_gl.py`, `kand_fr.py`, `kand_fj.py`, `opt_gl*.py`, `steig.py`, `build.py`).

## Das Biom in den Daten

- 2,15 km² im Rechteck X −3662 … 350 m, Y −3900 … −2250 m (Felder B1–F2). Dazu gehören die Westinseln und die NW-Halbinsel (ganz ohne Wege)
  und – wichtig – der **Kargletscher nördlich des Frostlagers**: Eis 0,071 km² (Zunge von 310 m bis 94 m hinab, Séracbruch bei Y −2950 … −2800),
  Karwand und Grate bis 415 m, Stirnmoränenbogen und Sander zwischen Zunge und Frostlager.
- Boden: Fels 27,5 %, Trockengras 16,7 %, Schnee 13,8 %, Heide 12,6 %, Gras 8,2 %; Hang Median 40°, 90 %-Wert 57°; Bäume auf 3,7 %.
- **Wege:** nur die Serpentine zum Frostlager (EXP_003, Radius 90 m) und das kurze Ostende bei X −520. Erlaubte Ortsmitten
  (80–300 m vom Weg, ≥ 150 m vom Stadtrand, ≥ 30 m innen): **0,178 km²**, alle um das Frostlager. Darin passen mit 350 m Abstand
  höchstens 3–4 Orte; seit 11:44 liegen dort außerdem tundra_02 (Der Wanderer, −968/−2158) und tundra_05 – ein vierter heute gültiger
  Ort (Endmoräne mit Findlingen bei −1080/−2330) musste deshalb weichen.
- **Folgerung:** 3 Orte gelten heute (`standorte.json`), 5 brauchen einen neuen Steig (`standorte_steige.json`): **Gletschersteig West**
  (Frostlager → Sander → Westgrat → Karboden, 1573 m, max 30°, 114 m steiler als 25° als Felsstufen), Ast **Nordhang** (768 m, ≤ 25°) und
  **Gletschersteig Ost** (Straßenende Ost → Ostgrat → Nunatak, 1383 m, ≤ 25°). Ferat entscheidet.
- Heute (Bilder `BERG11_E1_rundgang`, `SERP2_E2_SERP_D2_kehren_hoch`): kahle Felsflanken mit Kopfsteinpflaster-Wirkung, Schnee als
  glatte Kappe, an der Serpentine lichte Kiefern ohne Unterwuchs. Ziel `witcher_01` (Schneeberge über grünem Tal, Kies und Wasser im
  Vordergrund) und `witcher_06` (Fels mit Schnee nur auf Simsen, Dunst an der Wand).

## Prüfung

- `sehens_pruefen.py` (alle `standorte.json`, mit Daten): **0 FEHLER**; WARNUNG nur „3 Orte (Soll 8)“, weil die übrigen Orte am Steig hängen.
- `standorte_steige.json` mit demselben Prüfer gegen **Wege + Steige** (Steige als Wegzellen gerastert): **0 FEHLER**, WARNUNG nur „5 Orte (Soll 8)“; globale Abstände über alle Biome inklusive aller bedingten Orte (auch lava/standorte_kratersteig nicht betroffen): **0 FEHLER**.
- Kameras nach §8 in der Fassung 11.10. 13:00: alle vier mit **Hoch = −170** (Augenhöhe) und echtem Ziel; Prüfer-Hinweise nur „_anmarsch x m vom Weg“ (Kamera steht auf dem Zugangspfad, dort wo sich der Ort öffnet).
- Bitte bei der globalen Prüfung `*/standorte_steige.json` mitnehmen (wie `lava/standorte_kratersteig.json`), sonst setzen andere Biome Orte in die Steig-Räume.

## Übersicht

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden z | Radius | Weg (Steig) | gilt | Nachweis (sicht.py) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `gletscher_01_gletschertor` | Das Gletschertor | Leuchtfeuer | E2 | −620 / −2845 | 219 m | 190 m | 257 m | heute | 22 m: 20/97 Punkte, bis 796 m |
| 2 | `gletscher_02_lawinenkegel` | Der Lawinenkegel | Leuchtfeuer | D2 | −920 / −2650 | 165 m | 80 m | 279 m | heute | 10 m: 32/151 Punkte, bis 746 m |
| 3 | `gletscher_03_moraenensee` | Der Moränensee | Fundstück | D2 | −1120 / −2950 | 191 m | 60 m | 595 m (172) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: ab ≤ 455 m |
| 4 | `gletscher_04_toteisloch` | Das Toteisloch | Fundstück | E2 | −270 / −2560 | 141 m | 60 m | 239 m | heute | verdeckt vom Weg: ja (0/50 ≤ 400 m) |
| 5 | `gletscher_05_die_waechte` | Die Wächte | Leuchtfeuer | E1 | −610 / −3196 | 412 m | 110 m | 609 m (123) | Steig | 10 m: 55/195 Punkte, bis 768 m |
| 6 | `gletscher_06_gletschertoepfe` | Die Gletschertöpfe | Fundstück | E1 | −250 / −3060 | 121 m | 60 m | 616 m (107) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: ab ≤ 128 m |
| 7 | `gletscher_07_der_nunatak` | Der Nunatak | Fundstück | E2 | 120 / −2970 | 223 m | 70 m | 800 m (107) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: unsichtbar |
| 8 | `gletscher_08_gletscherschliff` | Der Gletscherschliff | Fundstück | D1 | −960 / −3280 | 115 m | 60 m | 759 m (106) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: ab ≤ 610 m |

---

## 1 · Das Gletschertor (`gletscher_01_gletschertor`) – Leuchtfeuer

**Was man sieht.** Die Zunge des Kargletschers bricht über eine Felsstufe: ein 120 m breiter Séracbruch aus blauen, schiefen Eistürmen (8–15 m), dazwischen Spalten, in denen das Licht türkis wird. An ihrem Fuß, links hinter der Stirnmoräne, öffnet sich das Gletschertor – ein 9 m hohes, gewölbtes Portal aus geschichtetem, schmutzig-blauem Eis, aus dem der milchige Gletscherbach tritt. Wer hineingeht, steht 15 m tief in einer Eishöhle mit gewellter Decke (Ablationsnäpfe) und Steinen, die im Eis stecken.

**Vorbild.** Real: Gletschertor des Morteratsch und des Rhonegletschers, Eishöhlen des Breiðamerkurjökull (Vatnajökull), Séracs des Glacier des Bossons. Spiel: der Gletscher über Kaer Morhen/Skellige (Witcher 3), die blauen Eiswände in Skyrim (Höhlen des Schlangenzahns).

**Standort.** Feld E2, X −620 / Y −2845, Boden 218,8 m. Offener Hang; Boden Eis 89 %, Fels 5 %, Erde 4 %, Schnee 1 %; Hang 31° (max 70°), Exposition 197°, TPI25 0,7 m, TPI100 5,7 m, Relief 100 m im Radius. Weg 257 m (Punkt −646/−2588); Wasser 195 m, Meer 570 m, Stadtrand 156 m (EXP_003); 472 m innerhalb des Bioms; 0 Baumzellen im Radius (max 0 m); Einzugsfläche max 31824 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 22 m: 20 von 97 Wegpunkten im Ring 300–800 m (Wege) sehen ≥ 30 %, Mittel 0,17, lesbar bis 796 m; bester Punkt −658/−2430 in 417 m mit Anteil 1,00.

**Komposition und Anmarsch.** Blickziel ist das dunkle Portal unter der leuchtend blauen Séracwand. Vordergrund: Sanderfläche mit Gletscherbach und Kiesbänken, Mitte: Stirnmoräne mit Toteisbuckeln, Hintergrund: Séracbruch und die Karwand mit der Wächte (gletscher_05) als zweite Silhouette. Der Spieler sieht die Séracs schon von der Serpentine; das Portal zeigt sich erst, wenn er auf der Sanderfläche links um die Moräne geht. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 259 m (X −645 / Y −2587), `_held` 240 m (X −760 / Y −2650), `_nah` 10 m (X −626 / Y −2837), `_fern` 417 m (X −658 / Y −2430). **Zugang (kandidaten.erreichbarkeit, 4 m):** 393 m vom Weg (Luftlinie 259 m), max 31,1°, Mittel 10,8°, 4 m steiler als 25°, 30 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Séracwand aus 6–10 großen Eisnetzen (Wunsch Megascans Ice Cliff, bis dahin `SM_EISZAPFEN_9` gruppiert + Geländestufe mit Lage Eis und Material `M_EL_Eis4`) und das Portal als Gewölbe aus 3–4 Eisschalen. Begleiter (5–7): `SM_NordicBoulder_01` und `SM_TundraMossyBoulder_01` als Gletscherfracht vor dem Tor, halb im Eis/Kies. Schutt (150–200): Moränenschutt `SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_01/02`, `SM_mountain_rock_big_01_1…5`, nach außen feiner (Sortierung). Kleinzeug: `SM_SmallStonesPack_01…14`, `SM_NordicBeachRock_01`, Eisbrocken `SM_EISZAPFEN_1/5` liegend als Kalbungsreste. Bewuchs nach Ursache: fast keiner – erst 80 m vor der Stirn Pioniere (`SM_wk2oaeyqx_VarA…I`, `SM_heath_B_01`), das zeigt das junge Gletschervorfeld. Kontaktzone: Eis endet nie scharf – Schmutzband aus Kies auf dem Eis (Lage Kies/Geroell über Eis gemischt), Schmelzwasserrinnen, nasser dunkler Kies am Fuß (`MI_Leakage_03`).

**Wasser, Effekte, Licht.** Gletscherbach (`bach`, farbe `gletschermilch`, quelle true) aus dem Portal, 2–4 m breit, auf der Sanderfläche verzweigt, mündet in den vorhandenen F_GLETSCHERTAL. Kalter Nebel im Portal (`lokaler_nebel`, Dichte 0,08, bläulich), ein schwaches blaues Punktlicht (0,4/0,7/1,0; 800 cd) im Höhlenende, damit die Tiefe auch bei fester Sonne leuchtet. Niagara optional: Tropfwasser am Portal.

**Geländeänderung.** Stempel 220 × 160 m: Felsstufe unter den Séracs um 6–8 m versteilen (Eisbruch), Portalnische 4 m tief, Sander 0,5–1 m eingeebnet mit 2–3 flachen Rinnen. Lagen: Eis (Zunge), Kies/Geroell (Sander, Moräne), Schnee nur in Mulden.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_9`, `SM_NordicBoulder_01`, `SM_TundraMossyBoulder_01`, `SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_01`, `SM_NordicBeachRockyGround_02`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_NordicBeachRock_01`, `SM_EISZAPFEN_1`, `SM_EISZAPFEN_5`, `SM_wk2oaeyqx_VarA`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarC`, `SM_wk2oaeyqx_VarD`, `SM_wk2oaeyqx_VarE`, `SM_wk2oaeyqx_VarF`, `SM_wk2oaeyqx_VarG`, `SM_wk2oaeyqx_VarH`, `SM_wk2oaeyqx_VarI`, `SM_heath_B_01`; Decals: `MI_Leakage_03`; Material: `M_EL_Eis4`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Séracwand und Portal aus echtem Eis (Ice Cliff), Kalbungsbrocken (Rocky Snow Pile), Ersatz: SM_EISZAPFEN_8/9 gebündelt + Geländestufe, Material M_EL_Eis4; **Arctic Cliffs** (B) – große Eisplatten/Eisstücke für die Séracs, Ersatz: wie oben; **Niagara Examples Pack** (B) – kalter Nebel im Portal, Tropfwasser, Ersatz: lokaler_nebel ohne Niagara; **Cave Ambience** (C) – Klang in der Eishöhle, Ersatz: kein Klang; **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (C) – Gletscherbach-Schaum am Portal, Ersatz: MI_EL_Wasserfall_Aufprall.

**Aufwand und Risiko.** Hoch (Eisnetze sind die Lücke des Bestands). Risiko: ohne Megascans-Eis wirkt die Séracwand aus Eiszapfen künstlich – deshalb Paket A. Das Portal muss begehbar sein (Kollision) und darf nicht mit der Stadtzone (150 m) kollidieren: Mitte 156 m vom Rand des Frostlagers.

## 2 · Der Lawinenkegel (`gletscher_02_lawinenkegel`) – Leuchtfeuer

**Was man sieht.** Aus einer engen Rinne in der Westwand des Tals zieht ein schmutzig-weißer Kegel aus Altschnee 90 m weit in den Wald: der Lawinenkegel. Im Sommer ist er grau gebändert, an seinem Fuß tropft er in kleine Schmelzrinnen. Rechts und links liegen Fichtenstämme wie Streichhölzer, alle in Fallrichtung, mit abgerissenen Kronen; oben in der Rinne hängt noch Schnee. Ein Ort, der vom Wetter erzählt.

**Vorbild.** Real: Lawinenkegel im Lauterbrunnental und am Fuß des Eigers, Lawinenstriche in Kanada (Rogers Pass). Spiel: die Schneerinnen von Skellige (Witcher 3), Lawinenhänge in Red Dead Redemption 2 (Grizzlies).

**Standort.** Feld D2, X −920 / Y −2650, Boden 165,4 m. Offener Hang; Boden Heide 39 %, Trockengras 28 %, Schnee 14 %, Fels 13 %; Hang 39° (max 78°), Exposition 184°, TPI25 0,9 m, TPI100 8,2 m, Relief 102 m im Radius. Weg 279 m (Punkt −648/−2588); Wasser 155 m, Meer 608 m, Stadtrand 234 m (EXP_003); 230 m innerhalb des Bioms; 451 Baumzellen im Radius (max 28 m); Einzugsfläche max 53636 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 10 m: 32 von 151 Wegpunkten im Ring 300–800 m (Wege) sehen ≥ 30 %, Mittel 0,20, lesbar bis 746 m; bester Punkt −782/−2112 in 555 m mit Anteil 1,00.

**Komposition und Anmarsch.** Leuchtfeuer: Der weiße Fächer mit der dunklen Rinne darüber steht als helle Zunge im dunklen Waldhang – vom Weg zum Frostlager aus 330–750 m zu lesen. Held-Blick vom Kegelfuß hangauf: Bruchholz im Vordergrund, Kegel in der Mitte, die Rinne als Blickachse nach oben. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 330 m (X −639 / Y −2477), `_held` 25 m (X −920 / Y −2675), `_nah` 10 m (X −920 / Y −2660), `_fern` 555 m (X −782 / Y −2112). **Zugang (kandidaten.erreichbarkeit, 4 m):** 459 m vom Weg (Luftlinie 330 m), max 24,7°, Mittel 11,7°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Kegel als Geländeform (Stempel) mit Lage Schnee + Altschnee-Netze (Wunsch Megascans Snow Embankment/Huge Snow Hill; Ersatz Stempel + Lage Schnee und Schutt). Begleiter (6–8): umgeknickte Fichten `SM_FallenSpruceTree_01`, `SM_BrokenTreeAssembly_01`, `SM_Forest_pine_10_dead` schräg, Wurzelteller `SM_Pine_roots_01/03`. Schutt (80–150): Lawinenschutt im Schnee – `SM_mountain_rock_big_01_*`, `SM_ground_rock_01`, Äste `SM_Pine_broken_branch_01/02`, `SM_mountain_branch_01_01/02`. Kleinzeug: `SM_DryBranches_01…08`, Nadeln über Landschaftsgras. Bewuchs nach Ursache: Bahn frei von Bäumen, am Rand Jungwuchs `Fir_01_Plant`, `SM_Forest_pine_plant_01…03`, Weidengebüsch `SM_grey_willow_01…04` (typisch für Lawinenbahnen). Kontaktzone: Schnee schmutzig-gestreift (Decal `MI_ScatteredSticksAndTwigs_01`), Schmelzrand nass (`MI_Leakage_05`).

**Wasser, Effekte, Licht.** Drei dünne Schmelzrinnen am Kegelfuß (`bach`, farbe `klar`, quelle true, 0,5 m breit), versickern nach 40 m im Schutt.

**Geländeänderung.** Kegel +3…+6 m auf 90 × 60 m (Fächerform, Spitze in der Rinne), Rinne 2 m eingetieft. Lagen: Schnee (Kegel), Geroell (Rinnenboden), Laub/Nadeln am Rand.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_FallenSpruceTree_01`, `SM_BrokenTreeAssembly_01`, `SM_Forest_pine_10_dead`, `SM_Pine_roots_01`, `SM_Pine_roots_03`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_ground_rock_01`, `SM_Pine_broken_branch_01`, `SM_Pine_broken_branch_02`, `SM_mountain_branch_01_01`, `SM_mountain_branch_01_02`, `SM_DryBranches_01`, `SM_DryBranches_02`, `SM_DryBranches_03`, `SM_DryBranches_04`, `SM_DryBranches_05`, `SM_DryBranches_06`, `SM_DryBranches_07`, `SM_DryBranches_08`, `Fir_01_Plant`, `SM_Forest_pine_plant_01`, `SM_Forest_pine_plant_02`, `SM_Forest_pine_plant_03`, `SM_grey_willow_01`, `SM_grey_willow_02`, `SM_grey_willow_03`, `SM_grey_willow_04`; Decals: `MI_ScatteredSticksAndTwigs_01`, `MI_Leakage_05`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Altschnee-Kegel (Snow Embankment, Huge Snow Hill), Ersatz: Geländekegel + Lage Schnee; **Free City & Nature Sounds** (C) – Wind, Tropfen, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Risiko: ein weißer Kegel im Sommerwald kann wie ein Fehler aussehen – deshalb Schmutzbänder, Bruchholz und die sichtbare Rinne als Ursache.

## 3 · Der Moränensee (`gletscher_03_moraenensee`) – Fundstück · nur mit Steig `gletschersteig_west`

**Was man sieht.** In einem kleinen Hängetal unter dem Westgrat liegt ein milchig-türkiser See, nicht größer als ein Hof, hinter einem Riegel aus Moränenschutt. Der Gletscher, der ihn aufgeschüttet hat, ist längst weg; nur Firnflecken an der Rückwand speisen ihn. Am Ufer: Schliffplatten, Wollgras, ein einzelner von Flechten grüner Block.

**Vorbild.** Real: Moränenseen der Hohen Tauern, Lago di Sorapis (Farbe), Moränenstauseen im Himalaya (kleiner Maßstab). Spiel: die Gebirgsseen in Breath of the Wild (Hebra) und Witcher 3 (Skellige, Spikeroog).

**Standort.** Feld D2, X −1120 / Y −2950, Boden 190,6 m. Talboden (U-Tal); Boden Fels 75 %, Erde 13 %, Trockengras 12 %, Moos 1 %; Hang 56° (max 67°), Exposition 327°, TPI25 −2,1 m, TPI100 −20,1 m, Relief 165 m im Radius. Weg 595 m (Punkt −648/−2588), **mit Steig 172 m** (`gletschersteig_west`); Wasser 74 m, Meer 259 m, Stadtrand 537 m (EXP_003); 30 m innerhalb des Bioms; 0 Baumzellen im Radius (max 0 m); Einzugsfläche max 5188 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 12 von 316 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 455 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Man steigt vom Gletschersteig über den Moränenriegel – erst auf seiner Krone liegt der See mit der Felswand dahinter da. Held-Blick über den Riegel auf das Wasser mit gespiegelter Wand. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 73 m (X −1067 / Y −2901), `_held` 82 m (X −1106 / Y −3031), `_nah` 10 m (X −1118 / Y −2960). **Zugang (kandidaten.erreichbarkeit, 4 m):** 356 m vom Steig (Luftlinie 200 m), max 41,6°, Mittel 21,6°, 188 m steiler als 25°, 193 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: der See selbst (Farbe `gletschermilch`), Damm als Geländeform. Begleiter (4–6): `SM_LichenedForestBoulder_01`, `SM_TundraMossyBoulder_01`, `xf3odif_tier_0`, `xisgcic_tier_0` am Ufer, halb im Wasser. Schutt (100–150): Moränenriegel aus `SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_01/02`, `skjsL_tier_0`, `pkeeM_tier_0`. Kleinzeug: `SM_SmallStonesPack_*`, Kies am Ufer. Bewuchs: Moos und Seggen nur auf der wasserseitigen Dammseite (`SM_MossClump_01…05`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarF`), Zwergkiefer `SM_dwarf_pine_small_01` im Windschatten. Kontaktzone: helles Kalkband am Ufer (Wasserstand), Moos `MI_TileableMossPatches_02` an Blockfüßen.

**Wasser, Effekte, Licht.** `see` (Umriss ~45 × 30 m, gegen den Uhrzeigersinn, Spiegel = Damm − 1 m, Tiefe 4 m, farbe `gletschermilch`), Abfluss als dünner `bach` über den Damm Richtung Ostbucht. Morgennebel: `lokaler_nebel` 0,05 über dem Wasser.

**Geländeänderung.** Stempel 120 × 100 m: Becken −3…−5 m im U-Tal-Boden, Damm +3 m (Riegel) – Becken hat Abfluss (keine geschlossene Senke ohne Wasser). Lagen: Kies (Ufer), Moos, Fels.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_LichenedForestBoulder_01`, `SM_TundraMossyBoulder_01`, `xf3odif_tier_0`, `xisgcic_tier_0`, `SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_01`, `SM_NordicBeachRockyGround_02`, `skjsL_tier_0`, `pkeeM_tier_0`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_MossClump_01`, `SM_MossClump_02`, `SM_MossClump_03`, `SM_MossClump_04`, `SM_MossClump_05`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarF`, `SM_dwarf_pine_small_01`; Decals: `MI_TileableMossPatches_02`. Wunsch: **Megascans Icelandic Sand With Pebbles** (C) – Uferkies hell, Ersatz: SM_BeachSandWithPebbles_01/02; **Free City & Nature Sounds** (C) – Wind, Wasser, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Nur mit Gletschersteig West erreichbar (Zugang 356 m, davon 188 m steiler als 25 Grad: Felsstufen). Risiko: Hang 56 Grad am Punkt – Becken muss auf der Talsohle liegen, nicht in der Flanke (Stempel prüfen).

## 4 · Das Toteisloch (`gletscher_04_toteisloch`) – Fundstück

**Was man sieht.** Mitten im Heidehang östlich des Frostlagers ein runder Trichter, 6–7 m tief und 45 m breit, mit steilen, moosigen Wänden. Unten steht schwarzes, stilles Wasser, an seinem Rand ragen Birken schräg nach innen. Der Trichter ist das Abdruckloch eines Eisblocks, den der Gletscher hier liegen ließ und der unter dem Schutt geschmolzen ist.

**Vorbild.** Real: Sölle Mecklenburgs, Kettle Holes in Wisconsin und Island (Skaftafell). Spiel: die verborgenen Waldtümpel in Witcher 3 (Velen) – hier ohne Menschenspur.

**Standort.** Feld E2, X −270 / Y −2560, Boden 141,3 m. Schlucht/Kessel; Boden Heide 54 %, Schnee 19 %, Trockengras 15 %, Erde 7 %; Hang 3° (max 59°), Exposition 122°, TPI25 −9,9 m, TPI100 −23,5 m, Relief 43 m im Radius. Weg 239 m (Punkt −472/−2432); Wasser 238 m, Meer 727 m, Stadtrand 242 m (EXP_003); 122 m innerhalb des Bioms; 190 Baumzellen im Radius (max 24 m); Einzugsfläche max 46460 m². Geschlossene Senke 6,5 m tief. **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (50 Wegpunkte ≤ 400 m, max. Anteil 0,00).

**Komposition und Anmarsch.** Fundstück: Vom Weg aus ist der Trichter nicht zu sehen (Rand und Bäume verdecken ihn); er öffnet sich erst 25–30 m vor dem Rand. Held-Blick vom Südrand hinunter: schräge Birken rahmen den schwarzen Spiegel, im Wasser spiegelt sich der helle Himmel. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 29 m (X −288 / Y −2537), `_held` 25 m (X −286 / Y −2541), `_nah` 10 m (X −276 / Y −2552). **Zugang (kandidaten.erreichbarkeit, 4 m):** 345 m vom Weg (Luftlinie 246 m), max 29,2°, Mittel 9,5°, 6 m steiler als 25°, 6 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: der Kesselsee (Farbe `schwarz_spiegel`). Begleiter (5–8): schräge Birken `Big_Tree_Birch_01` (0,5–0,7×), ein Birkenstumpf `SM_BirchTreeStump_01`, ein ins Wasser gekippter Stamm `SM_Forest_pine_04_log`. Schutt (40–80): Blöcke vom Trichterrand `SM_MossyRocks_02`, `texndcpda_tier_0`, `xjijdiz_tier_0`. Kleinzeug: Laub/Nadeln in der Mulde, `SM_DryBranches_*`. Bewuchs nach Ursache: Feuchtering aus Moos und Schachtelhalm (`SM_MossClump_*`, `SM_rough_horsetail_01…03`) auf den unteren 2 m, oben Heide `SM_heath_A_01`, `SM_lingonberry_01/02`. Kontaktzone: Uferband aus Torfmoos (Lage Moos 255), Laub schwimmt in einer Ecke.

**Wasser, Effekte, Licht.** `see` kreisrund ~20 m, Spiegel 1,5 m unter dem tiefsten Randpunkt, Tiefe 3 m, farbe `schwarz_spiegel`. Nebel in der Senke (`lokaler_nebel` 0,06).

**Geländeänderung.** Senke ist schon da (Senkentiefe 6,5 m); Stempel nur 60 × 60 m: Wände auf 35–40 Grad versteilen, Boden 1 m glätten. Lagen: Moos, Erde, Laub.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `Big_Tree_Birch_01`, `SM_BirchTreeStump_01`, `SM_Forest_pine_04_log`, `SM_MossyRocks_02`, `texndcpda_tier_0`, `xjijdiz_tier_0`, `SM_DryBranches_01`, `SM_DryBranches_02`, `SM_DryBranches_03`, `SM_DryBranches_04`, `SM_DryBranches_05`, `SM_DryBranches_06`, `SM_DryBranches_07`, `SM_DryBranches_08`, `SM_MossClump_01`, `SM_MossClump_02`, `SM_MossClump_03`, `SM_MossClump_04`, `SM_MossClump_05`, `SM_rough_horsetail_01`, `SM_rough_horsetail_02`, `SM_rough_horsetail_03`, `SM_heath_A_01`, `SM_lingonberry_01`, `SM_lingonberry_02`. Wunsch: **Free City & Nature Sounds** (C) – Stille/Wind in der Senke, Ersatz: kein Klang.

**Aufwand und Risiko.** Niedrig – fast nur Bestand. Risiko: gering; Abstand zur Fliesstreppe der Tundra (tundra_04) 407 m.

## 5 · Die Wächte (`gletscher_05_die_waechte`) – Leuchtfeuer · nur mit Steig `gletschersteig_west`

**Was man sieht.** Auf dem Nordgrat des Kars hängt eine Schneewächte wie eine erstarrte Welle 6–8 m über den Abgrund, blau im Schatten, an der Kante von Wind gezahnt. Darunter, am Fuß der Karwand, klafft der Bergschrund zwischen Fels und Gletscher, und im flachen Firnbecken davor gurgelt eine Gletschermühle: ein Loch im Eis, in das ein Schmelzbach stürzt.

**Vorbild.** Real: Wächten am Säntis und an der Jungfrau, Bergschrund an der Eiger-Nordwand, Gletschermühlen auf dem Aletschgletscher. Spiel: Kammlinien von The Long Dark, die Gipfel von Skellige (Witcher 3).

**Standort.** Feld E1, X −610 / Y −3196, Boden 412,5 m. Kuppe/Gipfel; Boden Fels 77 %, Schnee 22 %, Eis 0 %, Erde 0 %; Hang 25° (max 77°), Exposition 333°, TPI25 8,7 m, TPI100 79,9 m, Relief 186 m im Radius. Weg 609 m (Punkt −646/−2588), **mit Steig 123 m** (`gletschersteig_west`); Wasser 166 m, Meer 241 m, Stadtrand 506 m (EXP_003); 241 m innerhalb des Bioms; 0 Baumzellen im Radius (max 0 m); Einzugsfläche max 1188 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 10 m: 55 von 195 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,14, lesbar bis 768 m; bester Punkt −824/−2974 in 308 m mit Anteil 0,74; von bestehenden Wegen allein: 14 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: Die weiße Kante liegt genau auf der Himmelslinie über dem Gletscher – von der Straße am Frostlager (750 m) lesbar. Held-Blick vom flachen Firnbecken (Kamera 140 m südlich auf dem Eis): Gletschermühle vorne, Bergschrund als dunkle Linie in der Mitte, Wächte oben. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 175 m (X −756 / Y −3099), `_held` 151 m (X −650 / Y −3050), `_nah` 10 m (X −613 / Y −3186), `_fern` 308 m (X −824 / Y −2974). **Zugang (kandidaten.erreichbarkeit, 4 m):** 224 m vom Steig (Luftlinie 210 m), max 24,0°, Mittel 8,5°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Wächte aus gestreckten Schneenetzen (Wunsch Megascans Snow Embankment, gekippt; Ersatz Geländegrat + Lage Schnee + `SM_EISZAPFEN_6/9` an der Unterseite). Begleiter (4–5): Felsköpfe am Grat `SM_NordicBoulder_01`, `rcygn_tier_0` mit Schneekappe (`M_EL_Fels_Auflage`, Auflage_Farbe weiß). Schutt (60–100): Wächtenbruch – Schneeblöcke und Eisbrocken im Becken unter der Wand (`SM_EISZAPFEN_1…5` liegend, Megascans Rocky Snow Pile). Kleinzeug: Steinschlag auf dem Firn (`SM_SmallStonesPack_*`, `SM_NordicBeachRock_01`). Bewuchs: keiner – nur Flechten (Lage Fels mit Moos 10 %). Kontaktzone: Bergschrund als 2–3 m breite Rinne mit Eis-Kante, Firn wellig (Lage Schnee über Eis).

**Wasser, Effekte, Licht.** Gletschermühle: kurzer `bach` (supraglazial, farbe `tuerkis`, 1 m) endet `versickert` in einem runden Schacht (Netz-Ring aus Eis); Wasserfall-Material `MI_EL_Wasserfall_Kaskade` 3 m in den Schacht. Effekt optional: Schneefahne an der Wächte (Niagara-Wunsch).

**Geländeänderung.** Grat: Wächtenwulst +2…+4 m auf 140 × 20 m, Bergschrund −3 m; Firnbecken flach. Lagen: Schnee (Grat), Eis (Becken), Fels.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_6`, `SM_EISZAPFEN_9`, `SM_NordicBoulder_01`, `rcygn_tier_0`, `SM_EISZAPFEN_1`, `SM_EISZAPFEN_2`, `SM_EISZAPFEN_3`, `SM_EISZAPFEN_4`, `SM_EISZAPFEN_5`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_NordicBeachRock_01`; Material: `M_EL_Fels_Auflage`, `MI_EL_Wasserfall_Kaskade`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Wächte (Snow Embankment gekippt), Wächtenbruch (Rocky Snow Pile), Ersatz: Geländewulst + Lage Schnee + SM_EISZAPFEN_6/9; **Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam** (B) – Schneefahne an der Wächte, Ersatz: ohne Effekt; **Fantasy Ambiences (Lava, Höhle, Wind …)** (C) – Wind am Grat, Ersatz: kein Klang.

**Aufwand und Risiko.** Hoch (Gratlage, Steig 1,6 km). Risiko: Wächte braucht ein überhängendes Netz (Gelände kann keine Überhänge) – ohne Megascans-Schnee Ersatz nur als Wulst.

## 6 · Die Gletschertöpfe (`gletscher_06_gletschertoepfe`) – Fundstück · nur mit Steig `gletschersteig_ost`

**Was man sieht.** In einer engen Felsklamm nordöstlich des Kars hat das Schmelzwasser des einstigen Gletschers runde Töpfe in den Fels gebohrt – drei glattgeschliffene Kessel, der größte 6 m weit und mannstief, in jedem liegt noch der Mahlstein. Der Klammbach fällt von Topf zu Topf.

**Vorbild.** Real: Gletschergarten Luzern, Gletschertöpfe von Maloja, Strudeltöpfe der Liechtensteinklamm. Spiel: die Felsbecken in Horizon Forbidden West (Kältezonen).

**Standort.** Feld E1, X −250 / Y −3060, Boden 121,4 m. Schlucht/Kessel; Boden Fels 58 %, Erde 22 %, Heide 9 %, Trockengras 7 %; Hang 34° (max 80°), Exposition 98°, TPI25 −11,0 m, TPI100 −51,7 m, Relief 116 m im Radius. Weg 616 m (Punkt −646/−2588), **mit Steig 107 m** (`gletschersteig_ost`); Wasser 150 m, Meer 260 m, Stadtrand 488 m (EXP_003); 191 m innerhalb des Bioms; 24 Baumzellen im Radius (max 19 m); Einzugsfläche max 57352 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 4 von 328 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 128 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Die Klamm ist vom Oststeig aus nicht einsehbar (128 m maximale Sichtweite, 4 Wegpunkte); man steigt in die Kerbe und steht plötzlich über dem ersten Topf. Held-Blick bachauf: drei Töpfe in einer Linie, nasse Wände, Lichtfleck von oben. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 14 m (X −242 / Y −3048), `_held` 25 m (X −228 / Y −3072), `_nah` 10 m (X −241 / Y −3065). **Zugang (kandidaten.erreichbarkeit, 4 m):** 316 m vom Steig (Luftlinie 118 m), max 40,6°, Mittel 19,1°, 74 m steiler als 25°, 216 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: drei Töpfe als Geländeform (Stempel, runde Kessel −2…−4 m) mit Wandnetzen `SM_big_rock_wall_01/02/03` und glatten Schalen `SM_SmoothRockShelf_01` am Rand. Begleiter (3): Mahlsteine `SM_NordicBeachRocks_01` (0,3–0,5×) rund in jedem Topf. Schutt (60–100): runde Bachsteine `SM_NordicBeachRock_01`, `SM_BeachSandWithPebbles_01`. Kleinzeug: `SM_SmallStonesPack_*`. Bewuchs nach Ursache: Moos und Farn nur im Sprühbereich (`SM_MossClump_*`, `SM_BeechFern_04`, `SM_EagleFern_S_01`), oben Zwergkiefern. Kontaktzone: Nassband dunkel (`MI_Leakage_07/08`), Moos kriecht an den Topfrändern hoch (`M_EL_Klippe_RVT`).

**Wasser, Effekte, Licht.** `bach` farbe `klar` (Klammbach, 1,5 m) mit drei Stufen 2–3 m (werden kleine Fälle), jeder Topf als `see` 3–6 m, farbe `tuerkis`, Tiefe 2 m.

**Geländeänderung.** Stempel 90 × 50 m entlang der Klamm: Töpfe ausfräsen, Stufen betonen; Rand Δ 0. Lagen: Fels, Kies, Moos.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_big_rock_wall_01`, `SM_big_rock_wall_02`, `SM_big_rock_wall_03`, `SM_SmoothRockShelf_01`, `SM_NordicBeachRocks_01`, `SM_NordicBeachRock_01`, `SM_BeachSandWithPebbles_01`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_MossClump_01`, `SM_MossClump_02`, `SM_MossClump_03`, `SM_MossClump_04`, `SM_MossClump_05`, `SM_BeechFern_04`, `SM_EagleFern_S_01`; Decals: `MI_Leakage_07`, `MI_Leakage_08`; Material: `M_EL_Klippe_RVT`. Wunsch: **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (B) – Kaskaden zwischen den Töpfen, Ersatz: MI_EL_Wasserfall_Kaskade; **Free City & Nature Sounds** (B) – Rauschen in der Klamm, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Risiko: Klamm (Hang 34–80 Grad) – Zugang 316 m mit 74 m steiler als 25 Grad (Trittstufen).

## 7 · Der Nunatak (`gletscher_07_der_nunatak`) – Fundstück · nur mit Steig `gletschersteig_ost`

**Was man sieht.** Hinter dem Ostgrat versteckt sich ein schwarzer Felszahn, der aus einem Firnfeld ragt wie eine Insel aus dem Eis: der Nunatak. Seine Flanken sind vom Frost in Platten gesprengt, auf seinem Scheitel wächst ein Polster aus Moos und eine einzelne, vom Wind gebeugte Zwergkiefer – das einzige Lebende weit und breit.

**Vorbild.** Real: Nunatakker Grönlands und Islands (Esjufjöll), Felsinseln im Vatnajökull. Spiel: die Felsinseln im Eis von Skyrim (Ödfrost) und The Long Dark.

**Standort.** Feld E2, X 120 / Y −2970, Boden 223,5 m. Kuppe/Gipfel; Boden Fels 70 %, Schnee 24 %, Trockengras 4 %, Geroell 2 %; Hang 54° (max 67°), Exposition 64°, TPI25 5,4 m, TPI100 38,6 m, Relief 157 m im Radius. Weg 800 m (Punkt −472/−2432), **mit Steig 107 m** (`gletschersteig_ost`); Wasser 89 m, Meer 268 m, Stadtrand 720 m (EXP_003); 72 m innerhalb des Bioms; 47 Baumzellen im Radius (max 30 m); Einzugsfläche max 1380 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: nicht sichtbar.

**Komposition und Anmarsch.** Fundstück: Der Felszahn liegt hinter dem Ostgrat und ist von keinem Weg- oder Steigpunkt zu sehen (0 von 174); er erscheint, wenn man über den Sattel tritt. Held-Blick von Südosten (120 m) über das Firnfeld: dunkler Zahn vor dem Meer. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 77 m (X 49 / Y −2941), `_held` 120 m (X 161 / Y −2857), `_nah` 10 m (X 123 / Y −2961). **Zugang (kandidaten.erreichbarkeit, 4 m):** 185 m vom Steig (Luftlinie 107 m), max 34,9°, Mittel 21,3°, 43 m steiler als 25°, 114 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Felsturm 20–24 m aus `veqnci0db_tier_2` (hochkant, 6 m eingegraben) + `ukjhcamga_tier_0` als Flanke, Material mit Schneekappe (`M_EL_Fels_Auflage`, Auflage_Farbe weiß, Menge 0,6). Begleiter (4–6): `SM_MassiveTundraRockFormation_02` als Fußplatte, `SM_NordicBoulder_01`. Schutt (120–180): Frostschutt-Kegel `SM_TundraRockyGround_01`, `xjijdiz_tier_0`, `texndcpda_tier_0`, `SM_mountain_rock_big_02_*`. Kleinzeug: Plattenscherben `SM_ground_rock_03_01`. Bewuchs: Moospolster `SM_MossClump_*` und 1 Zwergkiefer `SM_dwarf_pine_medium_02` auf dem Scheitel (Windflüchter). Kontaktzone: Firn liegt in einem Randkolk 1–2 m tiefer um den Fels (Windkolk), Schutt auf dem Firn.

**Wasser, Effekte, Licht.** keins; Schneefahne am Scheitel (Niagara-Wunsch, optional).

**Geländeänderung.** Stempel 120 × 120 m: Firnfeld ringsum glätten (Lage Schnee 255), Randkolk −1,5 m; der Zahn ist Netz.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `veqnci0db_tier_2`, `ukjhcamga_tier_0`, `SM_MassiveTundraRockFormation_02`, `SM_NordicBoulder_01`, `SM_TundraRockyGround_01`, `xjijdiz_tier_0`, `texndcpda_tier_0`, `SM_mountain_rock_big_02_1`, `SM_mountain_rock_big_02_2`, `SM_mountain_rock_big_02_3`, `SM_mountain_rock_big_02_4`, `SM_mountain_rock_big_02_5`, `SM_mountain_rock_big_02_6`, `SM_mountain_rock_big_02_7`, `SM_mountain_rock_big_02_8`, `SM_ground_rock_03_01`, `SM_MossClump_01`, `SM_MossClump_02`, `SM_MossClump_03`, `SM_MossClump_04`, `SM_MossClump_05`, `SM_dwarf_pine_medium_02`; Material: `M_EL_Fels_Auflage`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (B) – Firnfeld-Ränder, Schnee am Fels (Rocky Snow Pile), Ersatz: Lage Schnee + M_EL_Fels_Auflage; **Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam** (C) – Schneefahne, Ersatz: ohne Effekt.

**Aufwand und Risiko.** Mittel. Risiko: das Firnfeld macht den Ort – ohne Schneelage ist es nur ein Felsen. Abstand zu frost_04 (Raureifhain) 358 m.

## 8 · Der Gletscherschliff (`gletscher_08_gletscherschliff`) – Fundstück · nur mit Steig `gletschersteig_nordhang`

**Was man sieht.** Auf der Nordflanke über dem Meer hat das Eis den Fels poliert: buckelige Rundhöcker, glatt wie Walrücken, mit feinen parallelen Kratzern und sichelförmigen Schlagmarken. Auf dem höchsten Buckel sitzt ein Findling, den der Gletscher hier abgestellt hat – auf drei kleinen Steinen.

**Vorbild.** Real: Rundhöcker am Grimselpass, Gletscherschliffe im Gletschergarten Cavaglia, Findling auf Stelzen (Yorkshire Dales, Norber Erratics). Spiel: die geschliffenen Felsen in Witcher 3 (Skellige, Ard Skellig).

**Standort.** Feld D1, X −960 / Y −3280, Boden 114,8 m. Offener Hang; Boden Trockengras 32 %, Fels 28 %, Erde 28 %, Heide 9 %; Hang 44° (max 60°), Exposition 316°, TPI25 0,7 m, TPI100 11,8 m, Relief 124 m im Radius. Weg 759 m (Punkt −648/−2588), **mit Steig 106 m** (`gletschersteig_nordhang`); Wasser 109 m, Meer 120 m, Stadtrand 679 m (EXP_003); 120 m innerhalb des Bioms; 8 Baumzellen im Radius (max 20 m); Einzugsfläche max 1752 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 13 von 232 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 610 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Vom Nordhang-Steig aus erst auf den letzten 100 m zu sehen (die Buckel liegen hinter einer Hangkante). Held-Blick hangab: Schliffplatten vorne mit Kratzern im Streiflicht, Findling in der Mitte, das Meer dahinter. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 95 m (X −1019 / Y −3206), `_held` 101 m (X −1055 / Y −3245), `_nah` 10 m (X −969 / Y −3277). **Zugang (kandidaten.erreichbarkeit, 4 m):** 184 m vom Steig (Luftlinie 146 m), max 31,6°, Mittel 13,2°, 26 m steiler als 25°, 159 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Findling 5–6 m (`SM_NordicBoulder_01`, 0,7×) auf drei Stütz­steinen `skjsL_tier_0`. Begleiter (5–7): Rundhöcker aus `SM_SmoothRockShelf_01`, `SM_ForestRockSlab_01`, `SM_MassiveTundraRockFormation_02` flach, 40–60 % eingegraben, Schrammen als Decal (`MI_TileableLeakage_02` gestreckt). Schutt (40–80): wenig – Schliff ist sauber; nur in Rinnen `SM_ErodedRockyGround_01…03`. Kleinzeug: Flechtenflecken. Bewuchs nach Ursache: Heide und Krähenbeere nur in den Rinnen zwischen den Buckeln (`SM_heath_A_01`, `SM_heath_cross_01`, `SM_lingonberry_01`), auf den Buckeln nichts. Kontaktzone: Grasnarbe bricht an der Plattenkante ab (Lage Fels → Heide mit 3 m Saum).

**Wasser, Effekte, Licht.** keins.

**Geländeänderung.** Stempel 120 × 90 m: Buckel glätten (Krümmung), Rinnen −0,5 m. Lagen: Felsplatte, Heide.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_NordicBoulder_01`, `skjsL_tier_0`, `SM_SmoothRockShelf_01`, `SM_ForestRockSlab_01`, `SM_MassiveTundraRockFormation_02`, `SM_ErodedRockyGround_01`, `SM_ErodedRockyGround_02`, `SM_ErodedRockyGround_03`, `SM_heath_A_01`, `SM_heath_cross_01`, `SM_lingonberry_01`; Decals: `MI_TileableLeakage_02`. Wunsch: **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (C) – Decals für Schrammen/Flechten, Ersatz: MI_TileableLeakage_02 gestreckt.

**Aufwand und Risiko.** Niedrig–mittel. Risiko: Schrammen brauchen gute Decals (Wunsch Coast & Dunes Decals als Ersatzquelle).

---

## Steige (Vorschlag, Ferat entscheidet)

- **`gletschersteig_west`** – Start: Strasse am Frostlager (X -652, Y -2460); 1573 m, Höhe 91–382 m, max 30,0°, Mittel 14,6°, 114 m steiler als 25° (Kehren/Felsstufen). Polylinie in `standorte_steige.json` → `steige`. Bodenlage Kies/Erde als 1,2-m-Band, Trittsteine; keine Bauten.
- **`gletschersteig_nordhang`** – Start: Abzweig vom Gletschersteig West am Westgrat (X -930, Y -3000); 768 m, Höhe 144–367 m, max 24,8°, Mittel 18,7°, 0 m steiler als 25° (Kehren/Felsstufen). Polylinie in `standorte_steige.json` → `steige`. Bodenlage Kies/Erde als 1,2-m-Band, Trittsteine; keine Bauten.
- **`gletschersteig_ost`** – Start: Strassenende oestlich des Frostlagers (X -520, Y -2434); 1383 m, Höhe 127–338 m, max 25,0°, Mittel 16,6°, 0 m steiler als 25° (Kehren/Felsstufen). Polylinie in `standorte_steige.json` → `steige`. Bodenlage Kies/Erde als 1,2-m-Band, Trittsteine; keine Bauten.

Gerechnet mit eigener Dijkstra-Suche (4-m-Raster, 16 Nachbarn, Kante ≤ 25°, nur wo nicht möglich 30/35°), Ortskreise 88 m gesperrt, damit kein Ort näher als 80 m am Steig liegt.

## Einmaligkeit (Abgrenzung)

- Gletschertor/Séracs, Wächte, Bergschrund, Gletschermühle, Gletschertöpfe, Toteisloch, Moränensee, Gletscherschliff, Nunatak, Lawinenkegel gibt es in keinem anderen Biom. Der Findling „Der Wanderer“ gehört der Tundra (tundra_02) – deshalb keine eigene Findlingsstätte; nur ein Findling als Begleiter auf dem Gletscherschliff. Karsee ist Bergwald (bergwald_06) – der Moränensee hier ist durch einen Moränenriegel gestaut und milchig.
- Aus Katalog v1 übernommen: Gletschertor; ersetzt: „Der Atem“ (Geysir, kein Gletscherphänomen – Download-Liste bitte anpassen), Gletschertisch, Büßereis und Schmelzsee (zu klein für die 0,07 km² Eis; Gletschermühle steckt jetzt in der Wächte). Blasenbucht/Diamantstrand aus v1 sind nicht im Gletscher.

## Bildwünsche (leere Standorte, Kamera aus der jeweiligen standorte*.json)

- `gletscher_01_gletschertor_held` – Sander und Zunge heute – wie leer ist das Vorfeld?
- `gletscher_05_die_waechte_fern` – Grat vom Frostlager aus: liest sich die Kante?

## Offene Fragen an Ferat

- Baust du **Gletschersteig West/Nordhang/Ost** (zusammen 3,7 km)? Ohne sie bleiben im Gletscher 3 Orte.
- Darf ein Steig über Gletschereis (Karboden unter der Wächte) führen?
- Alte Netze `SM_K7_GLETSCHER__EIS` (Houdini-Gletscher) bleiben aus – richtig?

<!-- abgleich-13b13c -->

## Abgleich mit Inventar 13b und Entscheidungen 13c (Stand 11.10.2026)

Neues Inventar: `netze.csv` mit 1 692 Netzen, `inventar_extra.json` mit 73 Niagara-Systemen, 15 Effekt-Blueprints und 46 Klang-Cues. Maschinenlesbar steht alles in `asset_bedarf.json` → `abgleich_13b_13c`. Der Abschnitt ergänzt die Ortsbeschreibungen oben; wo er abweicht, gilt er.

### Entscheidungen aus 13c

- **Nature Water FX gekauft** (gletscher_06_gletschertoepfe): Ferat hat Nature Water FX gekauft; der Import steht aus. Die echten Systemnamen folgen mit dem nächsten Inventar, bis dahin gilt der Ersatz (lokaler_nebel bzw. NS_Smoke_Plume als Gischt-Vorlage). Realistic Waterfall VFX und Waterfall Pro sind damit gestrichen.
- **Steige** (gletscher_03, _05–_08): Die Steige (West, Nordhang, Ost) überführt ein anderer Agent als `pfade` nach `standorte.json` (Schema in `skripte/sehens_lib/README.md`). Den Stand trägt der Koordinator in `sehens-STATUS.md` nach.
- **Eis/Schnee im Bestand** (alle): 31 Megascans-Netze stehen in netze.csv (13b nennt 32; Nanite, Material `M_MS_Base_Trm` mit Durchscheinen). Größtes Eis: `uhprdg2fa_tier_0` 6,7 × 1,7 × 6,2 m; Séracwand 15–30 m also mit ×2,5–4 und Gruppen. Größter Schnee: `vdspdazqa_tier_0` (Huge Snow Hill) 15,2 × 7,4 × 1,8 m.

### Neu im Bestand – je Ort

| Ort | Asset | Pfad | Maße (m) | Einsatz |
|---|---|---|---|---|
| gletscher_01_gletschertor | `uhprdg2fa_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_uhprdg2fa/Raw/uhprdg2fa_tier_0/StaticMeshes/uhprdg2fa_tier_0` | 6,71 × 1,66 × 6,15 | Séracwand (Ice Cliff, 6,2 m hoch, ×2,5–4) |
| gletscher_01_gletschertor | `veipbcmcb_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_veipbcmcb/Raw/veipbcmcb_tier_0/StaticMeshes/veipbcmcb_tier_0` | 6,82 × 2,7 × 5,25 | Séracwand |
| gletscher_01_gletschertor | `uhpocesfa_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_uhpocesfa/Raw/uhpocesfa_tier_0/StaticMeshes/uhpocesfa_tier_0` | 6,89 × 1,79 × 4,46 | Séracwand, Portal-Laibung |
| gletscher_01_gletschertor | `vdsrdd0fa_tier_0` | `/Game/Fab/Megascans/3D/Large_Ice_Cliff_vdsrdd0fa/Raw/vdsrdd0fa_tier_0/StaticMeshes/vdsrdd0fa_tier_0` | 5,02 × 2,51 × 4,15 | Large Ice Cliff, Portalgewölbe |
| gletscher_01_gletschertor | `vctiegmfa_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_vctiegmfa/Raw/vctiegmfa_tier_0/StaticMeshes/vctiegmfa_tier_0` | 2,51 × 1,95 × 6,42 | Eispfeiler am Portal (6,4 m hoch) |
| gletscher_01_gletschertor | `xfroec0qx_tier_0` | `/Game/Fab/Megascans/3D/Rocky_Snow_Pile_xfroec0qx/Raw/xfroec0qx_tier_0/StaticMeshes/xfroec0qx_tier_0` | 4,7 × 3,83 × 2,17 | Kalbungsbrocken (Rocky Snow Pile) |
| gletscher_01_gletschertor | `vcytca0fa_tier_0` | `/Game/Fab/Megascans/3D/Rocky_Snow_Pile_vcytca0fa/Raw/vcytca0fa_tier_0/StaticMeshes/vcytca0fa_tier_0` | 4,07 × 2,51 × 0,85 | Kalbungsbrocken |
| gletscher_01_gletschertor | `BP_FogBankVolume` (Blueprint) | `/Game/NiagaraExamples/FX_Fog/BP_FogBankVolume` | – | kalter Nebel im Portal (Blueprint, optional) |
| gletscher_02_lawinenkegel | `vdspdazqa_tier_0` | `/Game/Fab/Megascans/3D/Huge_Snow_Hill_vdspdazqa/Raw/vdspdazqa_tier_0/StaticMeshes/vdspdazqa_tier_0` | 15,24 × 7,35 × 1,76 | Altschnee-Kegel (Huge Snow Hill 15 m) |
| gletscher_02_lawinenkegel | `uhvjae0fa_tier_0` | `/Game/Fab/Megascans/3D/Snow_Embankment_uhvjae0fa/Raw/uhvjae0fa_tier_0/StaticMeshes/uhvjae0fa_tier_0` | 6,61 × 4,52 × 0,65 | Schneezunge (Snow Embankment) |
| gletscher_02_lawinenkegel | `uhuldf3fa_tier_0` | `/Game/Fab/Megascans/3D/Snow_Embankment_uhuldf3fa/Raw/uhuldf3fa_tier_0/StaticMeshes/uhuldf3fa_tier_0` | 6,72 × 2,21 × 1,05 | Schneezunge |
| gletscher_02_lawinenkegel | `vcykbjsva_tier_0` | `/Game/Fab/Megascans/3D/Snowy_Rocks_Pile_vcykbjsva/Raw/vcykbjsva_tier_0/StaticMeshes/vcykbjsva_tier_0` | 6,49 × 3,15 × 1,5 | Schnee mit Steinen (Snowy Rocks Pile) |
| gletscher_02_lawinenkegel | `xgxhcjxqx_tier_0` | `/Game/Fab/Megascans/3D/Snow_Pile_xgxhcjxqx/Raw/xgxhcjxqx_tier_0/StaticMeshes/xgxhcjxqx_tier_0` | 7,17 × 6,5 × 2,13 | Schneehaufen (Snow Pile 7 m) |
| gletscher_03_moraenensee | `xemmbh2qx_tier_0` | `/Game/Fab/Megascans/3D/Snow_Pile_xemmbh2qx/Raw/xemmbh2qx_tier_0/StaticMeshes/xemmbh2qx_tier_0` | 1,3 × 0,88 × 0,49 | Altschneerest am Ufer (optional) |
| gletscher_03_moraenensee | `CUE_Water_Stream_II_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_II_Cue` | – | Zufluss, leise |
| gletscher_04_toteisloch | `vd4hbizcb_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_vd4hbizcb/Raw/vd4hbizcb_tier_0/StaticMeshes/vd4hbizcb_tier_0` | 3,83 × 0,55 × 1,59 | freigelegte Toteiskante (Ice Cliff klein, optional) |
| gletscher_05_die_waechte | `xelnbaeqx_tier_0` | `/Game/Fab/Megascans/3D/Snow_Embankment_xelnbaeqx/Raw/xelnbaeqx_tier_0/StaticMeshes/xelnbaeqx_tier_0` | 9,05 × 0,32 × 1,23 | Wächtenlippe (Snow Embankment 9,1 × 0,3 m, gekippt) |
| gletscher_05_die_waechte | `uhqffeyfa_tier_0` | `/Game/Fab/Megascans/3D/Snow_Embankment_uhqffeyfa/Raw/uhqffeyfa_tier_0/StaticMeshes/uhqffeyfa_tier_0` | 4,66 × 2,13 × 0,98 | Wächte |
| gletscher_05_die_waechte | `vctldcnfa_tier_0` | `/Game/Fab/Megascans/3D/Snow_Embankment_vctldcnfa/Raw/vctldcnfa_tier_0/StaticMeshes/vctldcnfa_tier_0` | 6,28 × 2,21 × 0,88 | Wächte |
| gletscher_05_die_waechte | `xemjafmqx_tier_0` | `/Game/Fab/Megascans/3D/Rocky_Snow_Pile_xemjafmqx/Raw/xemjafmqx_tier_0/StaticMeshes/xemjafmqx_tier_0` | 8,66 × 7,96 × 2,56 | Wächtenbruch (Rocky Snow Pile 8,7 m) |
| gletscher_05_die_waechte | `xfwgbg0qx_tier_0` | `/Game/Fab/Megascans/3D/Rocky_Snow_Pile_xfwgbg0qx/Raw/xfwgbg0qx_tier_0/StaticMeshes/xfwgbg0qx_tier_0` | 7,32 × 4,25 × 1,04 | Wächtenbruch |
| gletscher_06_gletschertoepfe | `CUE_Water_Stream_X_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_X_Cue` | – | Rauschen in der Klamm |
| gletscher_07_der_nunatak | `vcykbjsva_tier_0` | `/Game/Fab/Megascans/3D/Snowy_Rocks_Pile_vcykbjsva/Raw/vcykbjsva_tier_0/StaticMeshes/vcykbjsva_tier_0` | 6,49 × 3,15 × 1,5 | Schnee am Fels (Snowy Rocks Pile) |
| gletscher_07_der_nunatak | `vcyiccyga_tier_0` | `/Game/Fab/Megascans/3D/Rocky_Snow_Pile_vcyiccyga/Raw/vcyiccyga_tier_0/StaticMeshes/vcyiccyga_tier_0` | 3,01 × 2,45 × 0,82 | Firnrand (Rocky Snow Pile) |
| gletscher_07_der_nunatak | `xe2obbqqx_tier_0` | `/Game/Fab/Megascans/3D/Snow_Pile_xe2obbqqx/Raw/xe2obbqqx_tier_0/StaticMeshes/xe2obbqqx_tier_0` | 2,08 × 2,07 × 0,52 | Schneerest |

### Paketstatus der Wünsche dieses Bioms

| Paket | Status | Orte |
|---|---|---|
| Arctic Cliffs | fehlt (Download-Liste) | 01 |
| Cave Ambience | fehlt (Download-Liste) | 01 |
| Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen) | läuft bei Ferat | 08 |
| Fantasy Ambiences (Lava, Höhle, Wind …) | fehlt (Download-Liste) | 05 |
| Free City & Nature Sounds | im Projekt (/Game/City_Nature_Sounds, nur Naturklänge nutzen) | 02, 03, 04, 06 |
| Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile | im Projekt (31 Netze in netze.csv, /Game/Fab/Megascans/3D) | 01, 02, 05, 07 |
| Megascans Icelandic Sand With Pebbles | fehlt (Download-Liste) | 03 |
| Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen) | läuft bei Ferat | 01, 06 |
| Niagara Examples Pack | im Projekt (/Game/NiagaraExamples) | 01 |
| Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam | fehlt (Download-Liste) | 05, 07 |

### Fehlt weiterhin

- Schneefahne (Wächte, Nunatak): kein Schnee-Niagara im Bestand → Wunsch bleibt (Ultimate Niagara Environmental VFX B, Niagara VFX Pack Snow C).
- Tropfwasser im Portal: kein System im Bestand.

### Material-Instanzen (3 von höchstens 6)

| Name | Basis | Parameter | für |
|---|---|---|---|
| `MI_EL_SW_Gletschereis_Tief` | `M_EL_Eis4` | `Eis_Farbe` [0,25, 0,55, 0,92, 1], `Eis_Tief_Farbe` [0,02, 0,12, 0,35, 1], `Schnee_Menge` 0,25, `Eis_Rau_Max` 0,22 | Séracs, Gletschertor, Bergschrund, `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9` |
| `MI_EL_SW_Fels_Schneekappe` | `M_EL_Fels_Auflage` | `Auflage_Farbe` [0,95, 0,97, 1, 1], `Auflage_Menge` 0,65, `Auflage_Schwelle` 0,6, `Toenung` [0,75, 0,76, 0,8, 1] | `veqnci0db_tier_2`, `SM_NordicBoulder_01`, `rcygn_tier_0` |
| `MI_EL_SW_Klippe_Gletscherschliff` | `M_EL_Klippe_RVT` | `Moos_Menge` 0,15, `Fels_Saettigung` 0,5, `Helligkeit` 1,1 | `SM_SmoothRockShelf_01`, `SM_MassiveTundraRockFormation_02` |
