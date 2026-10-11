# Fjord – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

> **Nachtrag 13c (Pfade, 11.10.2026):** Ferat will Pfade ausdrücklich („lieber ein Pfad mehr als ein Ort weniger“). Alle 8 Orte stehen jetzt in `standorte.json`; die Steige sind dort unter `pfade` eingetragen (`fjord_pfad_kanzel`, `fjord_pfad_fjordsteig`), die Orte tragen `pfad_id`. Die früheren Variantendateien `standorte_*.json` gibt es nicht mehr – Erwähnungen unten sind historisch, „nur mit Steig“ heißt jetzt „am Pfad“. Prüfer über alle Biome: 0 FEHLER.
>
> Der Fjordsteig (2,2 km) läuft vom Weg am Erlenbach über den Grat hinunter an den Fjord und erschließt sieben Orte; Serpentine, weil die Linie bis über 50° steigt. Am Grat zweigt der Kanzelsteig (310 m, Serpentine) zur Kanzel ab.


Stand 11.10.2026 · Agent B4 · Dateien: `standorte.json` (heute gültige Orte), `standorte_steige.json` (Orte, die einen neuen Steig brauchen, mit Steig-Polylinien), je Ort `<id>.png` (Draufsicht 2 m, Steige orange, Zugangspfad gelb), `asset_bedarf.json`. Alle Zahlen aus den 2-m-Daten mit `antworten/skripte/sehens_lib` (Cache, Sichtlinien Gelände + `baumhoehe_4m`, Wegpunkte 20 m); eigene Scores/Skripte im Scratchpad `a13/b4_eis_fjord/` (`kand_gl.py`, `kand_fr.py`, `kand_fj.py`, `opt_gl*.py`, `steig.py`, `build.py`).

## Das Biom in den Daten

- 0,90 km² im Rechteck X −2248 … −1250 m, Y −3628 … −2630 m (C1/C2/D1/D2): ein Felsblock mit **Fjordarm** in der Mitte – U-Tal mit
  flacher Sohle (Y −3420 … −3100, 1–50 m) zwischen zwei Felslappen (bis 250 m), Talschluss als halbrunde Wand unter dem Hauptgrat
  (Y −2930, bis 456 m), Meeresarm ab Y −3420. Südseite: Hängetäler zur Tundra.
- Boden: Fels 51,5 %, Trockengras 24,6 %, Erde 13,1 %; Hang Median 49°, 90 %-Wert 64° – das steilste Biom der Welt; Bäume 4,1 %.
- **Wege:** keiner. Nächster Weg (am Erlenbach, X −1458 / Y −2150) 460 m vor dem Rechteck, 310 m vor der 150-m-Zone. Erlaubte Mitten heute: **0**.
- **Folgerung:** alle 8 Orte hängen am **Fjordsteig** (Erlenbach → Hängetal → Grat → Talschluss → Fjordsohle → Mündung, 2352 m,
  max 35°, 566 m steiler als 25° – Kehren und Felsstufen im Talschluss) und dem **Kanzel-Ast** (320 m, max 27°). `standorte.json` ist leer
  (Prüfer: WARNUNG „0 Orte“); die Orte stehen in `standorte_steige.json`.
- Heute (Bild `BERG11_C2_rundgang`): Fels mit Farbbändern und Kopfsteinpflaster-Felsen, Grat kahl. Ziel `witcher_06` (Wand mit Dunst, Wasser
  im Vordergrund) und `witcher_07` (Schlucht mit Bach).

## Prüfung

- `sehens_pruefen.py` (alle `standorte.json`, mit Daten): **0 FEHLER**; WARNUNG nur „0 Orte (Soll 8)“, weil die übrigen Orte am Steig hängen.
- `standorte_steige.json` mit demselben Prüfer gegen **Wege + Steige** (Steige als Wegzellen gerastert): **0 FEHLER**, 0 WARNUNG; globale Abstände über alle Biome inklusive aller bedingten Orte (auch lava/standorte_kratersteig nicht betroffen): **0 FEHLER**.
- Kameras nach §8 in der Fassung 11.10. 13:00: alle vier mit **Hoch = −170** (Augenhöhe) und echtem Ziel; Prüfer-Hinweise nur „_anmarsch x m vom Weg“ (Kamera steht auf dem Zugangspfad, dort wo sich der Ort öffnet).
- Bitte bei der globalen Prüfung `*/standorte_steige.json` mitnehmen (wie `lava/standorte_kratersteig.json`), sonst setzen andere Biome Orte in die Steig-Räume.

## Übersicht

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden z | Radius | Weg (Steig) | gilt | Nachweis (sicht.py) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `fjord_01_die_kanzel` | Die Kanzel | Leuchtfeuer | D1 | −1555 / −3275 | 225 m | 50 m | 1120 m (102) | Steig | 12 m: 44/125 Punkte, bis 798 m |
| 2 | `fjord_02_schleierwand` | Die Schleierwand | Leuchtfeuer | C2 | −1740 / −3000 | 264 m | 120 m | 894 m (91) | Steig | 40 m: 8/66 Punkte, bis 448 m |
| 3 | `fjord_03_trollzunge` | Die Trollzunge | Leuchtfeuer | D2 | −1500 / −2930 | 385 m | 40 m | 770 m (91) | Steig | 8 m: 56/189 Punkte, bis 761 m |
| 4 | `fjord_04_haengetal` | Das Hängetal | Leuchtfeuer (E46) | D2 | −1680 / −2775 | 195 m | 60 m | 663 m (87) | Steig | 12 m: 6/134 Punkte, bis 465 m (Wege allein: 0) |
| 5 | `fjord_05_fjordkopf` | Der Fjordkopf | Leuchtfeuer (E46) | C1 | −1754 / −3358 | 1 m | 70 m | 1239 m (87) | Steig | 4 m: 19/66 Punkte, bis 433 m (Wege allein: 0) |
| 6 | `fjord_06_bergsturz` | Der Bergsturzkegel | Leuchtfeuer (E46) | C1 | −1850 / −3170 | 118 m | 70 m | 1092 m (87) | Steig | 10 m: 16/69 Punkte, bis 330 m (Wege allein: 0) |
| 7 | `fjord_07_brandungsgrotte` | Die Brandungsgrotte | Fundstück | D1 | −1640 / −3540 | 6 m | 50 m | 1375 m (98) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: unsichtbar |
| 8 | `fjord_08_strandterrassen` | Die alten Ufer | Leuchtfeuer (E46) | C1 | −1950 / −3480 | 93 m | 70 m | 1417 m (271) | Steig | 4 m: 37/76 Punkte, bis 628 m (Wege allein: 0) |

---

## 1 · Die Kanzel (`fjord_01_die_kanzel`) – Leuchtfeuer · nur mit Steig `fjordsteig_kanzel`

**Was man sieht.** Am Rand der Ostwand springt eine flache Felsplatte über den Fjord vor – eben wie ein Tisch, an drei Seiten 220 m senkrecht. Ein Riss trennt sie fast von der Wand, man steigt über ihn hinüber. Unten liegt das Wasser grün und glatt, Möwen kreisen unterhalb.

**Vorbild.** Real: Preikestolen (Lysefjord). Spiel: die Aussichtsfelsen in Witcher 3 (Skellige) und Assassin's Creed Valhalla (Norwegen).

**Standort.** Feld D1, X −1555 / Y −3275, Boden 225,0 m. Kuppe/Gipfel; Boden Trockengras 63 %, Fels 20 %, Wiese 8 %, Moos 4 %; Hang 24° (max 69°), Exposition 327°, TPI25 4,9 m, TPI100 35,8 m, Relief 92 m im Radius. Weg 1120 m (Punkt −1424/−2164), **mit Steig 102 m** (`fjordsteig_kanzel`); Wasser 179 m, Meer 188 m, Stadtrand 1080 m (EXP_003); 187 m innerhalb des Bioms; 124 Baumzellen im Radius (max 32 m); Einzugsfläche max 3548 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 12 m: 44 von 125 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,31, lesbar bis 798 m; bester Punkt −1604/−2956 in 323 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: die vorspringende Platte ist von der Fjordsohle und vom Grat aus als Kante lesbar (11 Punkte bis 798 m). Held-Blick von der Platte fjordaus auf den Mund; zweiter Blick vom Fjordboden hinauf (Kamera _anmarsch). Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 139 m (X −1655 / Y −3371), `_held` 44 m (X −1547 / Y −3232), `_nah` 10 m (X −1553 / Y −3265), `_fern` 323 m (X −1604 / Y −2956). **Zugang (kandidaten.erreichbarkeit, 4 m):** 355 m vom Steig (Luftlinie 131 m), max 40,7°, Mittel 21,8°, 97 m steiler als 25°, 240 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Platte aus `SM_MassiveTundraRockFormation_01` (77 × 29 m, flach, 70 % eingegraben, über die Wandkante geschoben) + Riss als Lücke; Wand darunter `veqnci0db_tier_2`, `vmnmbhv_tier_0` (40 × 29 × 23 m) als Schalen. Begleiter (4): Blöcke am Riss `SM_NordicBoulder_01`. Schutt (40–60): Platten `SM_flat_rock_02/03/04`. Kleinzeug: Flechten, Steine. Bewuchs: Heide in Ritzen `SM_heath_A_01`, Krüppelkiefer `SM_pine_beach_crooked_01` am Plattenrand (Windflüchter). Kontaktzone: Grasnarbe endet am Riss, Moos in der Kluft.

**Wasser, Effekte, Licht.** keins oben; unten der Fjord.

**Geländeänderung.** Plattenrand +3 m ebnen, Wandkante unter der Platte −5 m (Überhang über Netz). Fenster 100 × 80 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_MassiveTundraRockFormation_01`, `veqnci0db_tier_2`, `vmnmbhv_tier_0`, `SM_NordicBoulder_01`, `SM_flat_rock_02`, `SM_flat_rock_03`, `SM_flat_rock_04`, `SM_heath_A_01`, `SM_pine_beach_crooked_01`. Wunsch: **Free City & Nature Sounds** (C) – Wind, Möwen, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Nur mit Fjordsteig + Kanzel-Ast (320 m, oben ≤ 27 Grad).

## 2 · Die Schleierwand (`fjord_02_schleierwand`) – Leuchtfeuer · nur mit Steig `fjordsteig`

**Was man sieht.** Am Talschluss des Fjords steht eine 250 m hohe, halbrunde Felswand. Über ihre Kante fallen sechs dünne Schmelzbäche aus den Firnrinnen des Grats – so dünn, dass sie halb im Wind verwehen, bevor sie unten in Schuttkegel und Moos aufschlagen. Die Wand ist schwarz und grün gestreift.

**Vorbild.** Real: Sieben Schwestern (Geirangerfjord), Mardalsfossen, Lauterbrunnen. Spiel: Wasserfallwände in Skyrim (Markarth) und Ghost of Tsushima.

**Standort.** Feld C2, X −1740 / Y −3000, Boden 263,8 m. Offener Hang; Boden Fels 95 %, Heide 2 %, Trockengras 1 %, Erde 1 %; Hang 66° (max 72°), Exposition 4°, TPI25 −2,3 m, TPI100 −9,2 m, Relief 309 m im Radius. Weg 894 m (Punkt −1430/−2162), **mit Steig 91 m** (`fjordsteig`); Wasser 89 m, Meer 362 m, Stadtrand 882 m (ROMAN_LOC_018); 362 m innerhalb des Bioms; 3 Baumzellen im Radius (max 22 m); Einzugsfläche max 17988 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 40 m: 8 von 66 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,12, lesbar bis 448 m; bester Punkt −1678/−3444 in 448 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: Vom Fjordboden und Fjordkopf aus (8 Punkte, bis 448 m) die silbernen Fäden vor dunkler Wand; Held-Blick vom Talboden (176 m) mit Bach im Vordergrund. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 121 m (X −1623 / Y −3031), `_held` 176 m (X −1709 / Y −3173), `_nah` 10 m (X −1738 / Y −3010), `_fern` 448 m (X −1678 / Y −3444). **Zugang (kandidaten.erreichbarkeit, 4 m):** 130 m vom Steig (Luftlinie 121 m), max 44,3°, Mittel 17,0°, 24 m steiler als 25°, 130 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: 4–6 Fallbänder `wasserfall` (je 0,6–1,5 m breit, 150–220 m Fall, Material `M_EL_Wasserfall2` mit Deckkraft 0,5, Straehnen 0,9). Begleiter: Wandnetze `vdssailfa_tier_2`, `vfmjadufa_tier_2` als Rippen. Schutt (150–200): Sturzkegel unter jedem Fall `SM_mountain_rock_big_01_*`, `SM_ground_rock_01/02`. Kleinzeug: `SM_SmallStonesPack_*`. Bewuchs nach Ursache: Moosstreifen und Farn nur in der Sprühzone (Klippe-Material Moos_Menge hoch, `SM_EagleFern_S_01/02`), Birken auf den Kegeln. Kontaktzone: Nassstreifen auf der Wand (`MI_Leakage_04/06`).

**Wasser, Effekte, Licht.** Fallbänder enden je in einem kleinen `see` (Gumpe 4–6 m, farbe `klar`), Abfluss als `bach` zum Fjordbach. Sprühnebel `lokaler_nebel` 0,08 am Wandfuß; Niagara-Gischt optional.

**Geländeänderung.** Wandfuß: Gumpen −1 m, Kegel +2 m. Oben am Grat 6 Firnrinnen −1 m als Quelle (Lage Schnee).

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `vdssailfa_tier_2`, `vfmjadufa_tier_2`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_ground_rock_01`, `SM_ground_rock_02`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_EagleFern_S_01`, `SM_EagleFern_S_02`; Decals: `MI_Leakage_04`, `MI_Leakage_06`; Material: `M_EL_Wasserfall2`. Wunsch: **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (A) – Fluss-/Wasserfall-Material für 6 dünne Fallbänder, Ersatz: MI_EL_Wasserfall (Deckkraft 0,5); **Niagara Examples Pack** (B) – Sprühnebel am Wandfuß, Ersatz: lokaler_nebel; **Realistic Waterfall and Water VFX** (C) – verwehende Fallfäden, Ersatz: Material allein.

**Aufwand und Risiko.** Hoch (6 Fälle). Abgrenzung zu bergwald_05 (ein Schleierfall in einer Klamm) und kueste „Seefall“ (Fall direkt ins Meer).

## 3 · Die Trollzunge (`fjord_03_trollzunge`) – Leuchtfeuer · nur mit Steig `fjordsteig`

**Was man sieht.** Am Grat über dem Talschluss ragt eine schmale Felszunge 15 m frei über den Abgrund nach Norden – darunter 300 m Luft bis zum Fjordboden. Von hier sieht man den ganzen Fjord bis zum Meer.

**Vorbild.** Real: Trolltunga (Skjeggedal). Spiel: Aussichtspunkte in Witcher 3 (Skellige) und Zelda Breath of the Wild (Türme).

**Standort.** Feld D2, X −1500 / Y −2930, Boden 384,9 m. Oberhang/Plateaukante; Boden Fels 79 %, Trockengras 13 %, Heide 8 %, Moos 0 %; Hang 63° (max 71°), Exposition 73°, TPI25 2,2 m, TPI100 34,3 m, Relief 136 m im Radius. Weg 770 m (Punkt −1424/−2164), **mit Steig 91 m** (`fjordsteig`); Wasser 210 m, Meer 395 m, Stadtrand 734 m (ROMAN_LOC_018); 252 m innerhalb des Bioms; 0 Baumzellen im Radius (max 0 m); Einzugsfläche max 1508 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 8 m: 56 von 189 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,30, lesbar bis 761 m; bester Punkt −1018/−3116 in 517 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: die Zunge steht als Zacken in der Gratlinie (21 Punkte, bis 761 m, auch vom Gletscher-Westgrat). Held-Blick seitlich vom Grat: Zunge vor dem Fjord. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 50 m (X −1530 / Y −2971), `_held` 101 m (X −1435 / Y −2853), `_nah` 10 m (X −1494 / Y −2922), `_fern` 517 m (X −1018 / Y −3116). **Zugang (kandidaten.erreichbarkeit, 4 m):** 140 m vom Steig (Luftlinie 97 m), max 36,5°, Mittel 19,9°, 35 m steiler als 25°, 96 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Felszunge aus `uchoab3fa_tier_0` (13,5 × 3,3 × 5,2 m) + `rcygn_tier_0` als Unterbau, 8 m eingegraben am Ansatz. Begleiter (3): Gratfelsen `SM_NordicBoulder_01`. Schutt (40–80): Frostschutt am Grat `SM_TundraRockyGround_01`. Kleinzeug: Steine. Bewuchs: Moospolster, Heide, keine Bäume. Kontaktzone: Flechten (Auflage grau-grün).

**Wasser, Effekte, Licht.** keins.

**Geländeänderung.** Grat am Ansatz −1 m (Sattel), sonst keine.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `uchoab3fa_tier_0`, `rcygn_tier_0`, `SM_NordicBoulder_01`, `SM_TundraRockyGround_01`. Wunsch: **Fantasy Ambiences (Lava, Höhle, Wind …)** (C) – Wind am Grat, Ersatz: kein Klang.

**Aufwand und Risiko.** Niedrig–mittel. Risiko: Zunge muss frei schweben – Netz mit Kollision, Fuß tief im Grat.

## 4 · Das Hängetal (`fjord_04_haengetal`) – Leuchtfeuer (E46) · nur mit Steig `fjordsteig`

> **Entscheidung E46: Fundstück → Leuchtfeuer** (11.10.2026, Koordinator für Ferat). Ein Fjord ist eine Aussichtslandschaft, der Fjordsteig ein Panoramaweg; im offenen U-Tal lässt sich der Ort nicht verstecken (Phase 2: Wälle sperrten 0–3 Steigpunkte). Sicht (sicht.py, Silhouette 12 m, Wege + Steige): 6 von 134 Punkten im Ring 300–800 m, lesbar bis 465 m; von bestehenden Wegen allein 0. Neue Kamera `_fern` 465 m (X −1642 / Y −2312). Die Fundstück-Angaben unten sind der Stand vor E46.

**Was man sieht.** Auf der Südseite des Fjordkamms endet ein kleines, flaches Hochtal plötzlich an einer Stufe: Der Bach, der eben noch zwischen Wollgras mäanderte, stürzt 40 m in eine Schlucht. Oben ist es still und grün, unten donnert es.

**Vorbild.** Real: Hängetäler im Yosemite (Bridalveil) und in Norwegen (Aurland). Spiel: die Hochtäler in Skyrim (Rift).

**Standort.** Feld D2, X −1680 / Y −2775, Boden 194,6 m. Schlucht/Kessel; Boden Trockengras 35 %, Erde 29 %, Fels 27 %, Moos 6 %; Hang 32° (max 67°), Exposition 172°, TPI25 −11,3 m, TPI100 −38,9 m, Relief 103 m im Radius. Weg 663 m (Punkt −1430/−2162), **mit Steig 87 m** (`fjordsteig`); Wasser 0 m, Meer 585 m, Stadtrand 655 m (ROMAN_LOC_018); 148 m innerhalb des Bioms; 229 Baumzellen im Radius (max 33 m); Einzugsfläche max 32452 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 16 von 197 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 465 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: von unten verdeckt (Wald und Stufe), vom Fjordsteig erst auf den letzten 100 m. Held-Blick von der Lippe aus das Tal hinunter. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 42 m (X −1653 / Y −2743), `_held` 82 m (X −1733 / Y −2712), `_nah` 10 m (X −1686 / Y −2767). **Zugang (kandidaten.erreichbarkeit, 4 m):** 170 m vom Steig (Luftlinie 153 m), max 37,6°, Mittel 13,2°, 17 m steiler als 25°, 133 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Lippe aus `SM_big_rock_wall_01/02` + Fall (`wasserfall` 40 m, `M_EL_Wasserfall2`). Begleiter (4–5): Blöcke `SM_NordicBoulder_01` an der Lippe. Schutt (100–150): Bachbett `SM_DryRiverBed_01/02`, `SM_SmallStonesPack_*`. Bewuchs nach Ursache: oben Wollgras/Seggen `SM_wk2oaeyqx_VarA…I` und Moor-Moos (nass, flach), unten Farn in der Gischt `SM_EagleFern_S_04`, Birken. Kontaktzone: Nassband an der Lippe.

**Wasser, Effekte, Licht.** `bach` farbe `klar` 2 m, `wasserfall` 40 m an der Lippe, Gumpe `see` 8 m unten.

**Geländeänderung.** Hochtalboden flach glätten, Lippe +1 m. Fenster 120 × 80 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_big_rock_wall_01`, `SM_big_rock_wall_02`, `SM_NordicBoulder_01`, `SM_DryRiverBed_01`, `SM_DryRiverBed_02`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_wk2oaeyqx_VarA`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarC`, `SM_wk2oaeyqx_VarD`, `SM_wk2oaeyqx_VarE`, `SM_wk2oaeyqx_VarF`, `SM_wk2oaeyqx_VarG`, `SM_wk2oaeyqx_VarH`, `SM_wk2oaeyqx_VarI`, `SM_EagleFern_S_04`; Material: `M_EL_Wasserfall2`. Wunsch: **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (A) – Fall 40 m an der Lippe, Ersatz: MI_EL_Wasserfall + MI_EL_Wasserfall_Aufprall; **Free City & Nature Sounds** (C) – Rauschen, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Nur mit Fjordsteig.

## 5 · Der Fjordkopf (`fjord_05_fjordkopf`) – Leuchtfeuer (E46) · nur mit Steig `fjordsteig`

> **Entscheidung E46: Fundstück → Leuchtfeuer** (11.10.2026, Koordinator für Ferat). Ein Fjord ist eine Aussichtslandschaft, der Fjordsteig ein Panoramaweg; im offenen U-Tal lässt sich der Ort nicht verstecken (Phase 2: Wälle sperrten 0–3 Steigpunkte). Sicht (sicht.py, Silhouette 4 m, Wege + Steige): 19 von 66 Punkten im Ring 300–800 m, lesbar bis 433 m; von bestehenden Wegen allein 0. Neue Kamera `_fern` 433 m (X −1616 / Y −2948). Die Fundstück-Angaben unten sind der Stand vor E46.

**Was man sieht.** Wo der Fjordbach ins Meer läuft, hat er einen flachen Fächer aus Kies und Sand geschüttet. Bei Ebbe liegt er frei: Rinnen, in denen das Süßwasser milchig ins grüne Salzwasser zieht, Tang auf den Steinen, und überall die Wände, die 300 m hochsteigen.

**Vorbild.** Real: Fjordköpfe in Geiranger, Lærdal, Fjærland. Spiel: Fjordufer in Assassin's Creed Valhalla (Norwegen) und God of War.

**Standort.** Feld C1, X −1754 / Y −3358, Boden 0,6 m. Talboden (U-Tal); Boden Erde 54 %, Sand 25 %, Fels 16 %, Geroell 3 %; Hang 0° (max 71°), Exposition 270°, TPI25 −0,9 m, TPI100 −26,1 m, Relief 84 m im Radius. Weg 1239 m (Punkt −1424/−2164), **mit Steig 87 m** (`fjordsteig`); Wasser 0 m, Meer 4 m, Stadtrand 1217 m (ROMAN_LOC_018); 4 m innerhalb des Bioms; 123 Baumzellen im Radius (max 33 m); Einzugsfläche max 153672 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 45 von 111 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 433 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: der Fächer liegt unter der Talkante; vom Weg nichts. Held-Blick vom Fächer fjordaus zwischen den Wänden. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 95 m (X −1757 / Y −3263), `_held` 82 m (X −1754 / Y −3276), `_nah` 10 m (X −1759 / Y −3349). **Zugang (kandidaten.erreichbarkeit, 4 m):** 102 m vom Steig (Luftlinie 95 m), max 17,6°, Mittel 12,0°, 0 m steiler als 25°, 0 m Querhang > 38°, 3 m Furt → frei begehbar.

**Detail-Ebenen.** Held: Fächer als Geländeform mit 3–5 Rinnen. Begleiter (5–8): Blöcke `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01` im Watt. Schutt (150–200): `SM_NordicBeachRockyGround_01/02`, `SM_NordicBeach_02`, `SM_BeachSandWithPebbles_01/02`. Kleinzeug: Treibholz `SM_beach_driftwood_01`. Bewuchs nach Ursache: Strandgras und Sanddorn am Rand `SM_beach_grass_01_*`, `SM_sea_buckthorn_01/02`; Tang auf Steinen (Wunsch Coast & Dunes). Kontaktzone: Spülsaum, nasser Sand (Decal).

**Wasser, Effekte, Licht.** Fjordbach-Mündung als `bach` (farbe `gletschermilch`) in den Fjord; Meer vorhanden.

**Geländeänderung.** Fächer +0,5 m, Rinnen −0,5 m. Fenster 140 × 100 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01`, `SM_NordicBeachRockyGround_01`, `SM_NordicBeachRockyGround_02`, `SM_NordicBeach_02`, `SM_BeachSandWithPebbles_01`, `SM_BeachSandWithPebbles_02`, `SM_beach_driftwood_01`, `SM_beach_grass_01_1`, `SM_beach_grass_01_2`, `SM_beach_grass_01_3`, `SM_beach_grass_01_4`, `SM_beach_grass_01_hp_1`, `SM_beach_grass_01_hp_2`, `SM_sea_buckthorn_01`, `SM_sea_buckthorn_02`. Wunsch: **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (A) – Seetang, Spülsaum-Decals, nasser Sand, Ersatz: SM_beach_driftwood_01, MI_Leakage_*; **Megascans Icelandic Sand With Pebbles** (C) – dunkler Kies im Fächer, Ersatz: SM_BeachSandWithPebbles_01/02.

**Aufwand und Risiko.** Niedrig–mittel.

## 6 · Der Bergsturzkegel (`fjord_06_bergsturz`) – Leuchtfeuer (E46) · nur mit Steig `fjordsteig`

> **Entscheidung E46: Fundstück → Leuchtfeuer** (11.10.2026, Koordinator für Ferat). Ein Fjord ist eine Aussichtslandschaft, der Fjordsteig ein Panoramaweg; im offenen U-Tal lässt sich der Ort nicht verstecken (Phase 2: Wälle sperrten 0–3 Steigpunkte). Sicht (sicht.py, Silhouette 10 m, Wege + Steige): 16 von 69 Punkten im Ring 300–800 m, lesbar bis 330 m; von bestehenden Wegen allein 0. Neue Kamera `_fern` 330 m (X −1562 / Y −3008). Die Fundstück-Angaben unten sind der Stand vor E46.

**Was man sieht.** Aus der Westwand ist ein Stück Berg ausgebrochen: oben eine helle, frische Abrissnische, darunter ein Kegel aus hausgroßen Blöcken, der bis an den Talboden reicht. Zwischen den Blöcken wachsen schon junge Birken – der Sturz ist alt genug für Bäume, jung genug für scharfe Kanten.

**Vorbild.** Real: Bergsturz am Tafjord und Loen (Norwegen), Felsstürze im Yosemite. Spiel: Geröllhalden in Witcher 3 (Skellige).

**Standort.** Feld C1, X −1850 / Y −3170, Boden 118,4 m. Schlucht/Kessel; Boden Fels 84 %, Erde 13 %, Wiese 2 %, Trockengras 1 %; Hang 70° (max 73°), Exposition 118°, TPI25 −11,2 m, TPI100 −34,1 m, Relief 219 m im Radius. Weg 1092 m (Punkt −1430/−2162), **mit Steig 87 m** (`fjordsteig`); Wasser 100 m, Meer 207 m, Stadtrand 1083 m (ROMAN_LOC_018); 207 m innerhalb des Bioms; 41 Baumzellen im Radius (max 32 m); Einzugsfläche max 9484 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 53 von 118 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 330 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: liegt in der Westflanke, vom Fjordsteig aus erst nahe sichtbar. Held-Blick vom Kegelfuß hinauf zur Nische. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 99 m (X −1753 / Y −3151), `_held` 82 m (X −1769 / Y −3156), `_nah` 10 m (X −1840 / Y −3168). **Zugang (kandidaten.erreichbarkeit, 4 m):** 164 m vom Steig (Luftlinie 99 m), max 58,8°, Mittel 22,3°, 48 m steiler als 25°, 62 m Querhang > 38°, 6 m Furt → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: 8–12 große Blöcke `SM_NordicBoulder_01`, `SM_MassiveTundraRockFormation_02`, `ukjhcamga_tier_0`. Begleiter: Abrissnische als helles Netz `vdssailfa_tier_2`. Schutt (180–200): `SM_mountain_rock_big_01_*`, `SM_mountain_rock_big_02_*`, sortiert (groß unten). Kleinzeug: `SM_stone_03…08`. Bewuchs nach Ursache: Birken `Big_Tree_Birch_01` (0,4–0,6×) und Moos auf den älteren unteren Blöcken. Kontaktzone: Flechten nur auf alten Blöcken.

**Wasser, Effekte, Licht.** keins.

**Geländeänderung.** Nische −3 m, Kegel +4 m. Fenster 140 × 120 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_NordicBoulder_01`, `SM_MassiveTundraRockFormation_02`, `ukjhcamga_tier_0`, `vdssailfa_tier_2`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_mountain_rock_big_02_1`, `SM_mountain_rock_big_02_2`, `SM_mountain_rock_big_02_3`, `SM_mountain_rock_big_02_4`, `SM_mountain_rock_big_02_5`, `SM_mountain_rock_big_02_6`, `SM_mountain_rock_big_02_7`, `SM_mountain_rock_big_02_8`, `SM_stone_03`, `SM_stone_04`, `SM_stone_05`, `SM_stone_06`, `SM_stone_07`, `SM_stone_08`, `Big_Tree_Birch_01`. Wunsch: **Free City & Nature Sounds** (C) – Steinschlag/Wind, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel.

## 7 · Die Brandungsgrotte (`fjord_07_brandungsgrotte`) – Fundstück · nur mit Steig `fjordsteig`

**Was man sieht.** An der Ostspitze der Fjordmündung, wo die Dünung hereinläuft, hat das Meer einen schmalen Spalt ins Gestein gearbeitet: eine Grotte, hoch und eng, mit grünem Wasser, in dem Tang wogt. Bei jeder Welle atmet sie.

**Vorbild.** Real: Grotten an Norwegens Außenküste (Stetind-Fjord), Kvitholmen. Spiel: Meereshöhlen in God of War.

**Standort.** Feld D1, X −1640 / Y −3540, Boden 6,1 m. Offener Hang; Boden Trockengras 42 %, Sand 32 %, Fels 16 %, Moos 8 %; Hang 56° (max 60°), Exposition 359°, TPI25 −2,1 m, TPI100 −10,3 m, Relief 77 m im Radius. Weg 1375 m (Punkt −648/−2588), **mit Steig 98 m** (`fjordsteig`); Wasser 212 m, Meer 4 m, Stadtrand 1312 m (EXP_003); 4 m innerhalb des Bioms; 100 Baumzellen im Radius (max 33 m); Einzugsfläche max 6940 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: nicht sichtbar.

**Komposition und Anmarsch.** Fundstück: vom Steig aus nicht zu sehen (0 Punkte); man klettert über die Uferblöcke um die Ecke. Held-Blick in den Spalt. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 15 m (X −1647 / Y −3527), `_held` 44 m (X −1602 / Y −3562), `_nah` 10 m (X −1631 / Y −3545). **Zugang (kandidaten.erreichbarkeit, 4 m):** 119 m vom Steig (Luftlinie 97 m), max 30,9°, Mittel 14,9°, 27 m steiler als 25°, 119 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Grottenportal aus 2–3 Wandschalen `SM_HugeNordicCoastalCliff_01/02`, `SM_MassiveNordicCoastalCliff_01`. Begleiter: Uferblöcke `SM_NordicBeachRocks_01`. Schutt: `SM_NordicBeachRockyGround_01/02`. Bewuchs: Tang/Seepocken-Band (Wunsch Coast & Dunes Seetang). Kontaktzone: Nassband (`MI_Leakage_10`).

**Wasser, Effekte, Licht.** Meer; Gischt optional (Niagara).

**Geländeänderung.** Uferkante −1 m. Fenster 80 × 60 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_HugeNordicCoastalCliff_01`, `SM_HugeNordicCoastalCliff_02`, `SM_MassiveNordicCoastalCliff_01`, `SM_NordicBeachRocks_01`, `SM_NordicBeachRockyGround_01`, `SM_NordicBeachRockyGround_02`; Decals: `MI_Leakage_10`. Wunsch: **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (A) – Seetang-Band und Nässe, Ersatz: MI_Leakage_10; **Niagara Examples Pack** (B) – Gischt im Spalt, Ersatz: ohne Effekt; **Cave Ambience** (B) – Grottenklang, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Abgrenzung zu kueste „Grotte“ (Kliffhöhle mit türkisem Wasser): hier enger Spalt im Fjord mit Tang.

## 8 · Die alten Ufer (`fjord_08_strandterrassen`) – Leuchtfeuer (E46) · nur mit Steig `fjordsteig`

> **Entscheidung E46: Fundstück → Leuchtfeuer** (11.10.2026, Koordinator für Ferat). Ein Fjord ist eine Aussichtslandschaft, der Fjordsteig ein Panoramaweg; im offenen U-Tal lässt sich der Ort nicht verstecken (Phase 2: Wälle sperrten 0–3 Steigpunkte). Sicht (sicht.py, Silhouette 4 m, Wege + Steige): 37 von 76 Punkten im Ring 300–800 m, lesbar bis 628 m; von bestehenden Wegen allein 0. Neue Kamera `_fern` 498 m (X −1664 / Y −3072). Die Fundstück-Angaben unten sind der Stand vor E46.

**Was man sieht.** Am Westhang der Fjordmündung ziehen sich drei grüne Stufen parallel zum Wasser den Berg hinauf – alte Strandlinien, 20, 45 und 70 m über dem heutigen Meer. Auf jeder Stufe liegen gerundete Strandkiesel und Muschelschill, mitten im Gras.

**Vorbild.** Real: gehobene Strandterrassen in Spitzbergen, Hudson Bay, Bohuslän. Spiel: so noch nicht.

**Standort.** Feld C1, X −1950 / Y −3480, Boden 93,2 m. Offener Hang; Boden Trockengras 57 %, Fels 25 %, Wiese 9 %, Moos 5 %; Hang 44° (max 68°), Exposition 75°, TPI25 −0,8 m, TPI100 11,4 m, Relief 135 m im Radius. Weg 1417 m (Punkt −1430/−2162), **mit Steig 271 m** (`fjordsteig`); Wasser 228 m, Meer 89 m, Stadtrand 1405 m (ROMAN_LOC_018); 90 m innerhalb des Bioms; 410 Baumzellen im Radius (max 33 m); Einzugsfläche max 8108 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 45 von 88 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 638 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: liegt auf der Westseite, vom Steig aus nur als grüne Bänder; die Kiesel sieht man erst darauf. Held-Blick quer über die Stufen. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 334 m (X −1653 / Y −3327), `_held` 25 m (X −1954 / Y −3455), `_nah` 10 m (X −1952 / Y −3470). **Zugang (kandidaten.erreichbarkeit, 4 m):** 568 m vom Steig (Luftlinie 334 m), max 46,6°, Mittel 16,6°, 93 m steiler als 25°, 345 m Querhang > 38°, 15 m Furt → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: drei Terrassen (Gelände). Begleiter: 3–4 Blöcke. Schutt: Rundkiesel `SM_BeachSandWithPebbles_01/02`, `SM_NordicBeachRock_01`. Bewuchs: Gras/Heide (`SM_wk2oaeyqx_*`, `SM_heath_A_01`). Kontaktzone: Kiesbänder an den Stufenkanten.

**Wasser, Effekte, Licht.** keins.

**Geländeänderung.** Drei Stufen +1…2 m Kanten. Fenster 140 × 120 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_BeachSandWithPebbles_01`, `SM_BeachSandWithPebbles_02`, `SM_NordicBeachRock_01`, `SM_wk2oaeyqx_VarA`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarC`, `SM_wk2oaeyqx_VarD`, `SM_wk2oaeyqx_VarE`, `SM_wk2oaeyqx_VarF`, `SM_wk2oaeyqx_VarG`, `SM_wk2oaeyqx_VarH`, `SM_wk2oaeyqx_VarI`, `SM_heath_A_01`. Wunsch: **Megascans Icelandic Sand With Pebbles** (C) – gerundete Strandkiesel, Ersatz: SM_BeachSandWithPebbles_01/02, SM_NordicBeachRock_01.

**Aufwand und Risiko.** Niedrig.

---

## Steige (Vorschlag, Ferat entscheidet)

- **`fjordsteig`** – Start: Weg am Erlenbach (X -1458, Y -2150); 2352 m, Höhe 23–398 m, max 34,9°, Mittel 18,8°, 566 m steiler als 25° (Kehren/Felsstufen). Polylinie in `standorte_steige.json` → `steige`. Bodenlage Kies/Erde als 1,2-m-Band, Trittsteine; keine Bauten.
- **`fjordsteig_kanzel`** – Start: Abzweig vom Fjordsteig am Grat (X -1610, Y -2950); 320 m, Höhe 287–398 m, max 27,4°, Mittel 18,8°, 8 m steiler als 25° (Kehren/Felsstufen). Polylinie in `standorte_steige.json` → `steige`. Bodenlage Kies/Erde als 1,2-m-Band, Trittsteine; keine Bauten.

Gerechnet mit eigener Dijkstra-Suche (4-m-Raster, 16 Nachbarn, Kante ≤ 25°, nur wo nicht möglich 30/35°), Ortskreise 88 m gesperrt, damit kein Ort näher als 80 m am Steig liegt.

## Einmaligkeit (Abgrenzung)

- Kanzel, Trollzunge, Schleierwand, Hängetal, Fjordkopf, Bergsturzkegel, alte Ufer sind fjordtypisch. Abgrenzung: Klemmblock-Klamm mit Schleierfall (bergwald_05: ein Fall in einer Klamm), Seefall/Grotte der Küste (Fall direkt ins offene Meer, Kliffhöhle mit türkisem Wasser) – hier Brandungsgrotte als enger Spalt mit Tang an der Fjordmündung. Falls die Küste schon eine Grotte setzt, ist fjord_07 der Ort, den ich als erstes tausche.
- Diamantstrand und Basalt-Blockufer aus der Download-Liste nicht verwendet (kein Gletscher am Fjord, kein Basalt).

## Bildwünsche (leere Standorte, Kamera aus der jeweiligen standorte*.json)

- `fjord_02_schleierwand_held` – Talschluss vom Fjordboden
- `fjord_01_die_kanzel_anmarsch` – Ostwand von der Sohle: wo genau die Kante ist

## Offene Fragen an Ferat

- Baust du den **Fjordsteig** (2,35 km, 566 m davon als Kehren/Stufen) und den Kanzel-Ast? Alternativ: ein richtiger Weg vom Erlenbach in den Fjord.
- Sollen Wasserfälle über 150 m Fallhöhe mit dem Mountain-Set-Material gebaut werden oder lieber kürzer?

<!-- abgleich-13b13c -->

## Abgleich mit Inventar 13b und Entscheidungen 13c (Stand 11.10.2026)

Neues Inventar: `netze.csv` mit 1 692 Netzen, `inventar_extra.json` mit 73 Niagara-Systemen, 15 Effekt-Blueprints und 46 Klang-Cues. Maschinenlesbar steht alles in `asset_bedarf.json` → `abgleich_13b_13c`. Der Abschnitt ergänzt die Ortsbeschreibungen oben; wo er abweicht, gilt er.

### Entscheidungen aus 13c

- **Nature Water FX gekauft** (fjord_02_schleierwand, fjord_04_haengetal): Ferat hat Nature Water FX gekauft; der Import steht aus. Die echten Systemnamen folgen mit dem nächsten Inventar, bis dahin gilt der Ersatz (lokaler_nebel bzw. NS_Smoke_Plume als Gischt-Vorlage). Realistic Waterfall VFX und Waterfall Pro sind damit gestrichen.
- **Steige** (alle 8 Orte): Fjordsteig und Kanzel-Ast überführt ein anderer Agent als `pfade` nach `standorte.json` (Schema in `skripte/sehens_lib/README.md`). Den Stand trägt der Koordinator nach.
- **Entfallen** (–): Diamantstrand und Basalt-Blockufer sind aus der Download-Liste gestrichen (merge B4).

### Neu im Bestand – je Ort

| Ort | Asset | Pfad | Maße (m) | Einsatz |
|---|---|---|---|---|
| fjord_02_schleierwand | `NS_Smoke_Plume` (Niagara) | `/Game/NiagaraExamples/FX_Smoke/NS_Smoke_Plume` | – | Vorlage für Sprühnebel am Wandfuß – Kopie, weiß (optional; sonst lokaler_nebel) |
| fjord_02_schleierwand | `CUE_Water_Stream_X_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_X_Cue` | – | Fallbänder |
| fjord_04_haengetal | `xemmbh2qx_tier_0` | `/Game/Fab/Megascans/3D/Snow_Pile_xemmbh2qx/Raw/xemmbh2qx_tier_0/StaticMeshes/xemmbh2qx_tier_0` | 1,3 × 0,88 × 0,49 | Altschneerest im Hängetal (optional) |
| fjord_04_haengetal | `CUE_Water_Stream_IX_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_IX_Cue` | – | Fall an der Lippe |
| fjord_07_brandungsgrotte | `NS_Smoke_Plume` (Niagara) | `/Game/NiagaraExamples/FX_Smoke/NS_Smoke_Plume` | – | Vorlage für Gischt im Spalt (optional) |
| fjord_08_strandterrassen | `SM_LS_beach_escarpment_02_A` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Cliffs/Landscape_Spline_Meshes/SM_LS_beach_escarpment_02_A` | 9 × 2,89 × 1,86 | Terrassenkante (9 × 1,9 m, neu aus Coast & Dunes) |
| fjord_08_strandterrassen | `SM_LS_beach_escarpment_02_B` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Cliffs/Landscape_Spline_Meshes/SM_LS_beach_escarpment_02_B` | 11,16 × 2,71 × 1,83 | Terrassenkante (11,2 m) |
| fjord_08_strandterrassen | `SM_LS_beach_escarpment_01_C` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Cliffs/Landscape_Spline_Meshes/SM_LS_beach_escarpment_01_C` | 8,63 × 1,57 × 1,03 | niedrige Kante (1 m) |

### Paketstatus der Wünsche dieses Bioms

| Paket | Status | Orte |
|---|---|---|
| Cave Ambience | fehlt (Download-Liste) | 07 |
| Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen) | läuft bei Ferat | 05, 07 |
| Fantasy Ambiences (Lava, Höhle, Wind …) | fehlt (Download-Liste) | 03 |
| Free City & Nature Sounds | im Projekt (/Game/City_Nature_Sounds, nur Naturklänge nutzen) | 01, 04, 06 |
| Megascans Icelandic Sand With Pebbles | fehlt (Download-Liste) | 05, 08 |
| Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen) | läuft bei Ferat | 02, 04 |
| Niagara Examples Pack | im Projekt (/Game/NiagaraExamples) | 02, 07 |
| Realistic Waterfall and Water VFX | gestrichen (Nature Water FX gekauft) | 02 |

### Fehlt weiterhin

- Seetang/Seepocken-Band: Coast & Dunes läuft bei Ferat (Decals, Seetang); bis dahin MI_Leakage_10.

### Material-Instanzen (2 von höchstens 6)

| Name | Basis | Parameter | für |
|---|---|---|---|
| `MI_EL_SW_Klippe_Fjordnass` | `M_EL_Klippe_RVT` | `Moos_Farbe` [0,55, 0,75, 0,45, 1], `Moos_Menge` 0,85, `Blend_Hoehe` 600, `Toenung` [0,7, 0,72, 0,75, 1] | `vdssailfa_tier_2`, `vfmjadufa_tier_2`, `SM_HugeNordicCoastalCliff_01` |
| `MI_EL_SW_Schleierfall` | `M_EL_Wasserfall2` | `Deckkraft` 0,55, `Straehnen_Staerke` 0,9, `Schaum_Menge` 1,6, `V_Skala` 0,4 | Fallbänder Schleierwand |

## Abgleich Inventar 13d (Stand 11.10.2026, abends)

Neues Inventar: 1 965 Netze, 116 Niagara, 85 Decals. Pfade, Maße und Paketstatus stehen in `asset_bedarf.json` → `abgleich_13d`. Orte und Kameras bleiben unverändert; die Phase-2-Planer werden gerade auf die echten Assets umgestellt.

**Jetzt erfüllt:**

- `fjord_02_schleierwand` – Mountain/Nature Water FX: 6 dünne Fallbänder + Sprühnebel (A/B): `NS_Waterfall_Small`, `NS_Impact_Small`
- `fjord_04_haengetal` – Mountain: Fall 40 m an der Lippe (A): `NS_Waterfall_Medium`, `NS_Impact_Medium`, `M_River_Water_Translucent`
- `fjord_05_fjordkopf` – Coast & Dunes: Seetang, Spülsaum-Decals, nasser Sand (A): `SM_seaweed_01_A`, `SM_seaweed_01_C`, `MI_Decal_Algae`, `MI_Decal_Sand_Wet`, `MI_Deca_Wet_Flat`, `SM_beach_driftwood_02`
- `fjord_07_brandungsgrotte` – Coast & Dunes: Seetang-Band und Nässe (A): `MI_Decal_Algae`, `MI_Deca_Wet`, `SM_seaweed_01_D`
- `fjord_07_brandungsgrotte` – Niagara: Gischt im Spalt (B): `NS_Impact_Small`, `NS_Wake_Small`

**Ersatz → echtes Asset:**

- `fjord_05_fjordkopf, fjord_07_brandungsgrotte`: statt MI_Leakage_10 als Tang-/Nassband → `MI_Decal_Algae`, `MI_Deca_Wet`
- `fjord_02_schleierwand`: statt lokaler_nebel als Sprühnebel am Wandfuß → `NS_Impact_Small`
- `fjord_08_strandterrassen`: statt nur SM_BeachSandWithPebbles_01/02 → `MI_Decal_Rocks_Small` – Kiesel-Decal als Ergänzung; Icelandic Sand bleibt C.

**Fehlt weiter:**

- Dunkler Kies/gerundete Strandkiesel (fjord_05_fjordkopf, fjord_08_strandterrassen) – Megascans Icelandic Sand With Pebbles (C) · *kostenlos → Claude lädt auf Wunsch*
- Grottenklang (fjord_07_brandungsgrotte) – Cave Ambience (B) · *nur nach Ferats OK*
- Wind am Grat (fjord_03_trollzunge) – Fantasy Ambiences (B) · *nur nach Ferats OK*
- Brandungs-/Möwenklang (fjord_01_die_kanzel, fjord_05_fjordkopf, fjord_07_brandungsgrotte) – kein Paket gefunden (Wilderness Nature Loops C, Inhalt ungeprüft) · *nur nach Ferats OK*
