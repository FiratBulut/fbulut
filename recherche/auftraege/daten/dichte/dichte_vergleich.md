# Dichte-Vergleich: Demo-Karten gegen Eldarien

Stand 2026-10-13 23:40. Quelle: `scripts/unreal/ue_demo_dichte.py` (Zensus im Editor), Tabelle: `scripts/dichte/dichte_vergleich.py`.
Alle Dichten je 100 m2 der Bezugsflaeche (Demo: Landschaftsumriss, sonst Huelle aller Netze; Eldarien: Fenster). Zaehlungen exakt;
Grundflaeche/Hoehe grosser Komponenten aus Stichproben (Spalte "geschaetzt"). Grundflaechen-Prozente sind OBERGRENZEN (Ueberlappung
ignoriert, Kasten statt Umriss). Landschafts-Gras ist die Dichte-Summe aller Grastypen im Landschaftsmaterial (Unreal-Einheit:
Instanzen je 10 m x 10 m bei Lagengewicht 1) - die wirkliche Grasmenge haengt von den Lagen ab und ist hier NICHT gezaehlt.

## Datensaetze

| Datensatz | Quelle | Karte/Feld | Flaeche m2 | Flaechenart | Akteure | Instanzen | geschaetzt | Dauer s | Stand |
|---|---|---|---:|---|---:|---:|---|---:|---|
| Basalt | demo | Basalt | 0 | huelle | 151 | 142 | nein | 12 | 2026-10-13 23:26 |
| NWFX | demo | Overview | 0 | huelle | 30 | 4 | nein | 0 | 2026-10-13 23:26 |
| RA1 | demo | RuralAustralia_Example_01 | 1 040 400 | landschaft | 357 | 39 328 | ja | 6,3 | 2026-10-13 23:25 |
| RA2 | demo | RuralAustralia_Example_02 | 258 064 | landschaft | 915 | 22 549 | ja | 8,2 | 2026-10-13 23:25 |
| RA3 | demo | RuralAustralia_Example_03 | 1 040 400 | landschaft | 337 | 109 577 | ja | 0,1 | 2026-10-13 23:25 |
| RAC | demo | RuralAustralia_Content | 1 040 400 | landschaft | 127 | 1 947 | ja | 3,8 | 2026-10-13 23:26 |
| C2 (1 008x1 008 m) | eldarien | L_Eldarien C2 | 1 016 064 | fenster | 1 867 | 95 106 | nein | 0,9 | 2026-10-13 23:40 |
| C2_fenster (200x200 m) | eldarien | L_Eldarien C2 | 40 000 | fenster | 1 867 | 9 612 | nein | 1,1 | 2026-10-13 23:40 |

## Kennzahlen

| Kennzahl | Basalt | NWFX | RA1 | RA2 | RA3 | RAC | Demo-Mittel | Demo-Max | C2 (1 008x1 008 m) | C2_fenster (200x200 m) | Eldarien-Mittel | Faktor Demo/Eld. | Hinweis |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Netze je 100 m2 (alle Instanzen) | 14200000000000 | 400 000 000 000 | 3,78 | 8,738 | 10,53 | 0,187 | 2433333333337,2 | 14200000000000 | 9,36 | 24,03 | 16,7 | x145752221224,2 |  |
| Baeume/Totholz je 100 m2 | 0 | 0 | 2,108 | 0,081 | 0,024 | 0,001 | 0,369 | 2,108 | 1,09 | 1,873 | 1,482 | x0,25 |  |
| Felsen/Steine je 100 m2 | 14000000000000 | 0 | 1,223 | 1,82 | 0 | 0,001 | 2333333333333,8 | 14000000000000 | 3,38 | 4,668 | 4,024 | x579854208085,0 |  |
| Pflanzen (Netze) je 100 m2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2,133 | 8,453 | 5,293 | x0,00 |  |
| Sonstiges je 100 m2 | 200 000 000 000 | 400 000 000 000 | 0,45 | 6,836 | 10,51 | 0,184 | 100000000003 | 400 000 000 000 | 2,757 | 9,037 | 5,897 | x16957775140,4 |  |
| Kleinzeug < 0,5 m je 100 m2 | 200 000 000 000 | 0 | 0,119 | 2,991 | 4,403 | 0,04 | 33333333334,6 | 200 000 000 000 | 3,579 | 5,655 | 4,617 | x7219695329,1 |  |
| Mittelgross 0,5-3 m je 100 m2 | 7100000000000 | 100 000 000 000 | 2,601 | 5,315 | 6,1 | 0,144 | 1200000000002,4 | 7100000000000 | 5,324 | 18,34 | 11,83 | x101419878296,3 |  |
| Baeume >= 3 m je ha | 0 | 0 | 72,74 | 3,02 | 1,26 | 0,08 | 12,85 | 72,74 | 17,06 | 1,75 | 9,405 | x1,4 |  |
| Totholz/Stuempfe (< 3 m) je 100 m2 | 0 | 0 | 1,38 | 0,051 | 0,011 | 0,001 | 0,24 | 1,38 | 0,919 | 1,855 | 1,387 | x0,17 |  |
| Felsdeckung % (Obergrenze) | 202353000000000 | 0 | 1,868 | 378,4 | 0 | 0,359 | 33725500000063,4 | 202353000000000 | 78,15 | 1,217 | 39,68 | x849851325472,8 | Ueberlappung ignoriert |
| Pflanzen-Grundflaeche % (Obergrenze) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,073 | 4,713 | 2,893 | x0,00 | Ueberlappung ignoriert |
| Baum-Grundflaeche % (Obergrenze) | 0 | 0 | 93,21 | 7,938 | 4,401 | 0,236 | 17,63 | 93,21 | 22,93 | 7,664 | 15,3 | x1,2 | Kronen-Kasten |
| Verschiedene Netze | 23 | 2 | 35 | 53 | 45 | 80 | 39,67 | 80 | 294 | 181 | 237,5 | x0,17 |  |
| davon Baum-Netze | 0 | 0 | 14 | 14 | 14 | 14 | 9,333 | 14 | 60 | 31 | 45,5 | x0,21 |  |
| davon Fels-Netze | 22 | 0 | 5 | 13 | 0 | 15 | 9,167 | 22 | 84 | 52 | 68 | x0,13 |  |
| davon Pflanzen-Netze | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 65 | 50 | 57,5 | x0,00 |  |
| Dreiecke LOD0 je 100 m2 (gesetzt, vor Culling) | 243 528 599 999 999 968 | 288 200 000 000 000 | 13 760 | 5 879 | 1 708 | 125 | 40 636 133 333 336 904 | 243 528 599 999 999 968 | 16 423 | 27 197 | 21 810 | x1863188139997,1 |  |
| Anteil Nanite-Netze | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0,59 | 0,56 | 0,575 | x0,00 |  |
| Landschafts-Gras je 10 m x 10 m (Dichte-Summe, Lagengewicht 1) | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Eldarien 0 | aus dem Landschaftsmaterial |
| Grastypen im Material | - | - | 6 | 6 | 6 | 6 | 6 | 6 | 10 | 10 | 10 | x0,60 |  |
| Gras-Sorten im Material | - | - | 81 | 81 | 81 | 81 | 81 | 81 | 104 | 104 | 104 | x0,78 |  |
| Gras max. Hoehe m | - | - | 3,72 | 3,72 | 3,72 | 3,72 | 3,72 | 3,72 | 2,49 | 2,49 | 2,49 | x1,5 |  |
| Landschaft Quads je m | - | - | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | x1,0 |  |
| Landschafts-Lagen | - | - | 7 | 6 | 6 | 6 | 6,25 | 7 | 26 | 26 | 26 | x0,24 |  |
| Bezugsflaeche m2 | 0 | 0 | 1 040 400 | 258 064 | 1 040 400 | 1 040 400 | 563210,7 | 1 040 400 | 1 016 064 | 40 000 | 528 032 | x1,1 |  |

Faktor = Demo-Mittel / Eldarien-Mittel (x2 = die Demo-Karten stellen doppelt so viel hin). Fehlende Werte (-) = nicht messbar
(z. B. keine Landschaft in der Karte).

## Netze Basalt (haeufigste je Klasse)

| Klasse | Netz | Groesse | Instanzen | je 100 m2 | Grundflaeche m2 | Hoehe m (Mittel/Max) | Dreiecke LOD0 | Nanite | Quelle |
|---|---|---|---:|---:|---:|---|---:|---|---|
| fels | Basalt_Basalt_Cliff_Rock_B_SM | gross | 19 | 1900000000000 | 976,6 | 2,02 / 3,42 | 7 360 | nein | akteur |
| fels | Basalt_Basalt_Pillar_Variance_B_SM | mittel | 15 | 1500000000000 | 1,52 | 0,88 / 1,44 | 380 | nein | akteur |
| fels | Basalt_Basalt_Rock_D_SM | gross | 15 | 1500000000000 | 241,8 | 1,92 / 3,06 | 768 | nein | akteur |
| fels | Basalt_Basalt_Pillar_Variance_D_SM | mittel | 11 | 1 100 000 000 000 | 1,37 | 2,49 / 4 | 704 | nein | akteur |
| fels | Basalt_Basalt_Cluster_A_SM | gross | 10 | 1000000000000 | 183,2 | 3,85 / 4,81 | 66 475 | nein | akteur |
| sonstiges | Plane | gross | 2 | 200000000000 | 12813,6 | 0 / 0 | 2 | nein | akteur |
Kameras: 1 CineCameraActor2 CameraActor (-3495,5, -308,9, 554,9) pitch -19,6 yaw -24,3; 2 Player Start PlayerStart (90,4, 683,4, 242) pitch -5 yaw 330; 3 Player Start PlayerStart (90,4, 683,4, 242) pitch -5 yaw 90

## Netze NWFX (haeufigste je Klasse)

| Klasse | Netz | Groesse | Instanzen | je 100 m2 | Grundflaeche m2 | Hoehe m (Mittel/Max) | Dreiecke LOD0 | Nanite | Quelle |
|---|---|---|---:|---:|---:|---|---:|---|---|
| sonstiges | Sphere | gross | 3 | 300 000 000 000 | 450,2 | 12,25 / 12,25 | 960 | nein | akteur |
| sonstiges | Plane | mittel | 1 | 100000000000 | 250 000 | 0 / 0 | 2 | nein | akteur |
Kameras: 1 Player Start PlayerStart (0, -1 120, 752) pitch -5 yaw 0; 2 Player Start PlayerStart (0, -1 120, 752) pitch -5 yaw 120; 3 Player Start PlayerStart (0, -1 120, 752) pitch -5 yaw 240

## Netze RA1 (haeufigste je Klasse)

| Klasse | Netz | Groesse | Instanzen | je 100 m2 | Grundflaeche m2 | Hoehe m (Mittel/Max) | Dreiecke LOD0 | Nanite | Quelle |
|---|---|---|---:|---:|---:|---|---:|---|---|
| baum | SM_GrassTree_04 | mittel | 5 127 | 0,493 | 11379,1 | 1,53 / 1,65 | 661 | nein | foliage |
| baum | SM_GrassTree_03 | mittel | 4 137 | 0,398 | 24799,4 | 1,48 / 1,55 | 2 429 | nein | foliage |
| baum | SM_GrassTree_01 | gross | 2 840 | 0,273 | 20379,2 | 4,02 / 4,25 | 3 285 | nein | foliage |
| baum | SM_GrassTree_02 | mittel | 2 704 | 0,26 | 18495,8 | 2,96 / 3,14 | 2 927 | nein | foliage |
| baum | SM_Tree_S_01 | gross | 2 447 | 0,235 | 176469,9 | 8,28 / 9,51 | 11 307 | nein | foliage |
| fels | SM_Rock_S_02 | mittel | 5 799 | 0,557 | 3621,9 | 0,2 / 0,2 | 598 | nein | foliage |
| fels | SM_Rock_S_01 | mittel | 5 217 | 0,501 | 10602 | 0,43 / 0,43 | 599 | nein | foliage |
| fels | SM_Rock_M_03 | mittel | 1 111 | 0,107 | 3114,4 | 0,88 / 0,9 | 1 849 | nein | foliage |
| fels | SM_Rock_M_02 | mittel | 574 | 0,055 | 1977,4 | 0,86 / 0,87 | 1 091 | nein | foliage |
| fels | SM_Rock_M_01 | mittel | 21 | 0,002 | 118,6 | 0,69 / 0,71 | 1 378 | nein | foliage |
| sonstiges | SM_Fence_Wires_01 | gross | 1 045 | 0,1 | 914,2 | 1,08 / 1,08 | 7 182 | nein | akteur |
| sonstiges | SM_Fence_02 | mittel | 1 045 | 0,1 | 68,15 | 1,36 / 1,36 | 4 225 | nein | akteur |
| sonstiges | SM_Scatter_02_A | mittel | 570 | 0,055 | 454,4 | 0,06 / 0,08 | 239 | nein | foliage |
| sonstiges | SM_Scatter_02_J | klein | 294 | 0,028 | 36,72 | 0,07 / 0,09 | 15 | nein | foliage |
| sonstiges | SM_Scatter_02_F | mittel | 293 | 0,028 | 106,2 | 0,18 / 0,22 | 27 | nein | foliage |

Landschaft: 1 Teile, Quads/m 1, Material `MI_Landscape_Example_01`, Lagen: __LANDSCAPE_VISIBILITY__, LandscapeLayer_Gravel, LandscapeLayer_Dirt, LandscapeLayer_Stones, LandscapeLayer_Grass, LandscapeLayer_Leaves, LandscapeLayer_Roadside
Gras im Material `M_Landscape`: 6 Typen, 81 Sorten, Dichte-Summe 0 je 10 m x 10 m, max. Hoehe 3,72 m: GrassLayer_Dirt 0; GrassLayer_Stones 0; GrassLayer_Grass 0; GrassLayer_Leaves 0; GrassLayer_Roadside 0; GrassLayer_Gravel 0
Ausgeschlossen: SM_Horizon_01 (himmel/hintergrund (Name))
Kameras: 1 Camera2 CameraActor (4 986, 14892,2, 349,9) pitch -20,4 yaw -105,9; 2 Camera3 CameraActor (-6597,1, 14720,9, 395,3) pitch -23,6 yaw -83,7; 3 Camera4 CameraActor (2976,2, 21336,1, 329,6) pitch -18 yaw -129,3

## Netze RA2 (haeufigste je Klasse)

| Klasse | Netz | Groesse | Instanzen | je 100 m2 | Grundflaeche m2 | Hoehe m (Mittel/Max) | Dreiecke LOD0 | Nanite | Quelle |
|---|---|---|---:|---:|---:|---|---:|---|---|
| baum | SM_GrassTree_03 | mittel | 52 | 0,02 | 305,5 | 1,46 / 1,46 | 2 429 | nein | akteur |
| baum | SM_Tree_S_01 | gross | 34 | 0,013 | 5484,3 | 12,4 / 12,51 | 11 307 | nein | akteur |
| baum | SM_GrassTree_02 | mittel | 28 | 0,011 | 178,2 | 2,86 / 2,86 | 2 927 | nein | akteur |
| baum | SM_Log_S_02 | gross | 19 | 0,007 | 371,2 | 1,2 / 1,62 | 15 027 | nein | akteur |
| baum | SM_Log_S_01 | gross | 16 | 0,006 | 197,9 | 1,15 / 1,72 | 6 002 | nein | akteur |
| fels | SM_Rock_S_02 | mittel | 3 573 | 1,385 | 3340,2 | 0,23 / 0,7 | 598 | nein | foliage |
| fels | SM_Rock_S_01 | mittel | 536 | 0,208 | 2480,5 | 0,64 / 0,86 | 599 | nein | foliage |
| fels | SM_Rock_M_01 | gross | 206 | 0,08 | 4998,6 | 1,26 / 4,07 | 1 378 | nein | akteur |
| fels | SM_Ridge_Rock_01 | gross | 79 | 0,031 | 30965,5 | 2,62 / 7,24 | 19 833 | nein | akteur |
| fels | SM_Rock_M_02 | mittel | 68 | 0,026 | 689,6 | 1,33 / 3,47 | 1 091 | nein | akteur |
| sonstiges | SM_Scatter_02_H | klein | 2 431 | 0,942 | 169,8 | 0,08 / 0,11 | 23 | nein | foliage |
| sonstiges | SM_Scatter_02_I | klein | 2 399 | 0,93 | 188 | 0,04 / 0,06 | 10 | nein | foliage |
| sonstiges | SM_Scatter_02_J | klein | 2 389 | 0,926 | 261,6 | 0,06 / 0,09 | 15 | nein | foliage |
| sonstiges | SM_Scatter_04_B | mittel | 1 955 | 0,758 | 1879,6 | 0,05 / 0,07 | 1 192 | nein | foliage |
| sonstiges | SM_Scatter_03_B | mittel | 1 529 | 0,592 | 1383,6 | 0,14 / 0,15 | 181 | nein | foliage |

Landschaft: 1 Teile, Quads/m 1, Material `MI_Landscape_Example_02`, Lagen: __LANDSCAPE_VISIBILITY__, LandscapeLayer_Gravel, LandscapeLayer_Dirt, LandscapeLayer_Stones, LandscapeLayer_Grass, LandscapeLayer_Leaves
Gras im Material `M_Landscape`: 6 Typen, 81 Sorten, Dichte-Summe 0 je 10 m x 10 m, max. Hoehe 3,72 m: GrassLayer_Dirt 0; GrassLayer_Stones 0; GrassLayer_Grass 0; GrassLayer_Leaves 0; GrassLayer_Roadside 0; GrassLayer_Gravel 0
Kameras: 1 Camera1 CameraActor (4200,2, -1616,8, 251,2) pitch 8 yaw -115,5; 2 Camera2 CameraActor (5010,1, -4748,8, 349,6) pitch 39,4 yaw -21,7; 3 Camera3 CameraActor (11084,4, -3 342, 339,8) pitch -9,8 yaw 79,3

## Netze RA3 (haeufigste je Klasse)

| Klasse | Netz | Groesse | Instanzen | je 100 m2 | Grundflaeche m2 | Hoehe m (Mittel/Max) | Dreiecke LOD0 | Nanite | Quelle |
|---|---|---|---:|---:|---:|---|---:|---|---|
| baum | SM_GrassTree_03 | mittel | 36 | 0,003 | 209,5 | 1,46 / 1,46 | 2 429 | nein | akteur |
| baum | SM_GrassTree_02 | mittel | 31 | 0,003 | 195 | 2,84 / 2,86 | 2 927 | nein | akteur |
| baum | SM_GrassTree_04 | mittel | 29 | 0,003 | 61,99 | 1,5 / 1,5 | 661 | nein | akteur |
| baum | SM_Tree_S_01 | gross | 27 | 0,003 | 4075,6 | 11,92 / 12,51 | 11 307 | nein | akteur |
| baum | SM_GrassTree_01 | gross | 21 | 0,002 | 139,2 | 3,86 / 3,86 | 3 285 | nein | akteur |
| sonstiges | SM_Scatter_03_B | mittel | 15 317 | 1,472 | 12614,4 | 0,13 / 0,19 | 181 | nein | foliage |
| sonstiges | SM_Scatter_03_A | mittel | 15 281 | 1,469 | 11037,1 | 0,13 / 0,18 | 112 | nein | foliage |
| sonstiges | SM_Scatter_02_I | klein | 9 407 | 0,904 | 838,1 | 0,05 / 0,06 | 10 | nein | foliage |
| sonstiges | SM_Scatter_02_F | mittel | 9 386 | 0,902 | 3496,3 | 0,19 / 0,23 | 27 | nein | foliage |
| sonstiges | SM_Scatter_02_H | klein | 9 354 | 0,899 | 742,5 | 0,09 / 0,11 | 23 | nein | foliage |

Landschaft: 1 Teile, Quads/m 1, Material `MI_Landscape_Example_03`, Lagen: __LANDSCAPE_VISIBILITY__, LandscapeLayer_Gravel, LandscapeLayer_Dirt, LandscapeLayer_Stones, LandscapeLayer_Grass, LandscapeLayer_Leaves
Gras im Material `M_Landscape`: 6 Typen, 81 Sorten, Dichte-Summe 0 je 10 m x 10 m, max. Hoehe 3,72 m: GrassLayer_Dirt 0; GrassLayer_Stones 0; GrassLayer_Grass 0; GrassLayer_Leaves 0; GrassLayer_Roadside 0; GrassLayer_Gravel 0
Ausgeschlossen: SM_Horizon_01 (himmel/hintergrund (Name))
Kameras: 1 Camera1 CameraActor (13766,4, -4474,7, 96,8) pitch 6 yaw -166,2; 2 Camera2 CameraActor (922,3, -3645,5, 146,6) pitch -9,8 yaw -152; 3 Camera3 CameraActor (11383,5, -4820,4, 97,5) pitch 3,8 yaw -148

## Netze RAC (haeufigste je Klasse)

| Klasse | Netz | Groesse | Instanzen | je 100 m2 | Grundflaeche m2 | Hoehe m (Mittel/Max) | Dreiecke LOD0 | Nanite | Quelle |
|---|---|---|---:|---:|---:|---|---:|---|---|
| baum | SM_Log_L_01 | gross | 1 | 0 | 143,1 | 6 / 6 | 24 096 | nein | akteur |
| baum | SM_Log_M_01 | gross | 1 | 0 | 39,87 | 2,69 / 2,69 | 20 415 | nein | akteur |
| baum | SM_Log_S_01 | gross | 1 | 0 | 7,33 | 0,91 / 0,91 | 6 002 | nein | akteur |
| baum | SM_Log_S_02 | gross | 1 | 0 | 14,2 | 1,04 / 1,04 | 15 027 | nein | akteur |
| baum | SM_Tree_L_01 | gross | 1 | 0 | 982,3 | 28,46 / 28,46 | 32 110 | nein | akteur |
| fels | SM_Cliff_M_01_B | gross | 1 | 0 | 236,8 | 7,84 / 7,84 | 15 005 | nein | akteur |
| fels | SM_Cliff_M_02_A | gross | 1 | 0 | 310,4 | 11,81 / 11,81 | 19 313 | nein | akteur |
| fels | SM_Cliff_M_02_B | gross | 1 | 0 | 277,5 | 11 / 11 | 17 434 | nein | akteur |
| fels | SM_Cliff_M_03 | gross | 1 | 0 | 266 | 8,96 / 8,96 | 19 444 | nein | akteur |
| fels | SM_Ridge_Rock_01 | gross | 1 | 0 | 125,2 | 1,49 / 1,49 | 19 833 | nein | akteur |
| sonstiges | SM_Scatter_04_D | mittel | 533 | 0,051 | 141,8 | 0,03 / 0,03 | 1 192 | nein | foliage |
| sonstiges | SM_Scatter_03_B | mittel | 152 | 0,015 | 83,77 | 0,11 / 0,15 | 181 | nein | foliage |
| sonstiges | SM_Scatter_03_A | mittel | 151 | 0,015 | 74,03 | 0,1 / 0,15 | 112 | nein | foliage |
| sonstiges | SM_Scatter_02_A | mittel | 105 | 0,01 | 55,25 | 0,05 / 0,1 | 239 | nein | foliage |
| sonstiges | SM_Scatter_02_J | klein | 93 | 0,009 | 7,95 | 0,06 / 0,09 | 15 | nein | foliage |

Landschaft: 1 Teile, Quads/m 1, Material `MI_Landscape_Content_01`, Lagen: __LANDSCAPE_VISIBILITY__, LandscapeLayer_Gravel, LandscapeLayer_Dirt, LandscapeLayer_Stones, LandscapeLayer_Grass, LandscapeLayer_Leaves
Gras im Material `M_Landscape`: 6 Typen, 81 Sorten, Dichte-Summe 0 je 10 m x 10 m, max. Hoehe 3,72 m: GrassLayer_Dirt 0; GrassLayer_Stones 0; GrassLayer_Grass 0; GrassLayer_Leaves 0; GrassLayer_Roadside 0; GrassLayer_Gravel 0
Ausgeschlossen: SM_Horizon_01 (himmel/hintergrund (Name))
Kameras: 1 mitte huelle+boden (0, 0, 170) pitch -5 yaw 0; 2 mitte huelle+boden (0, 0, 170) pitch -5 yaw 120; 3 mitte huelle+boden (0, 0, 170) pitch -5 yaw 240

## Netze C2 (1 008x1 008 m) (haeufigste je Klasse)

| Klasse | Netz | Groesse | Instanzen | je 100 m2 | Grundflaeche m2 | Hoehe m (Mittel/Max) | Dreiecke LOD0 | Nanite | Quelle |
|---|---|---|---:|---:|---:|---|---:|---|---|
| baum | SM_dwarf_pine_small_01 | mittel | 1 521 | 0,15 | 3164,4 | 1,28 / 1,65 | 550 | nein | foliage |
| baum | SM_dwarf_pine_small_02 | mittel | 1 459 | 0,144 | 2818,6 | 1,09 / 1,4 | 659 | nein | foliage |
| baum | SM_dwarf_pine_medium_01 | mittel | 1 271 | 0,125 | 6427,2 | 2,08 / 2,69 | 2 684 | nein | foliage |
| baum | SM_dwarf_pine_medium_02 | mittel | 1 231 | 0,121 | 7872,8 | 2,12 / 2,69 | 2 950 | nein | foliage |
| baum | SM_dwarf_pine_medium_03 | mittel | 1 038 | 0,102 | 5115 | 1,96 / 2,41 | 2 783 | nein | foliage |
| fels | SM_SmallStonesPack_13 | klein | 2 438 | 0,24 | 64,78 | 0,08 / 0,25 | 706 | ja | foliage |
| fels | SM_SmallStonesPack_14 | klein | 1 981 | 0,195 | 55,39 | 0,14 / 0,41 | 614 | ja | foliage |
| fels | SM_SmallStonesPack_11 | klein | 1 969 | 0,194 | 21,2 | 0,1 / 0,19 | 568 | ja | foliage |
| fels | SM_SmallStonesPack_08 | klein | 1 967 | 0,194 | 31,67 | 0,09 / 0,17 | 698 | ja | foliage |
| fels | SM_SmallStonesPack_12 | klein | 1 594 | 0,157 | 17,97 | 0,08 / 0,25 | 714 | ja | foliage |
| pflanze | SM_grass_03_A_1 | mittel | 2 437 | 0,24 | 1083,9 | 0,87 / 1,18 | 64 | nein | foliage |
| pflanze | SM_grass_03_B_1 | mittel | 2 209 | 0,217 | 907,2 | 0,95 / 1,48 | 96 | nein | foliage |
| pflanze | SM_grass_02_A_1 | klein | 2 096 | 0,206 | 348,9 | 0,35 / 0,44 | 24 | nein | foliage |
| pflanze | SM_grass_02_B_1 | mittel | 1 926 | 0,19 | 649,3 | 0,39 / 0,49 | 26 | nein | foliage |
| pflanze | SM_grass_01_1 | mittel | 1 566 | 0,154 | 1112,3 | 0,39 / 0,48 | 21 | nein | foliage |
| sonstiges | SM_heath_B_01 | mittel | 3 568 | 0,351 | 1852,9 | 0,33 / 0,57 | 193 | nein | foliage |
| sonstiges | SM_heath_A_01 | mittel | 3 293 | 0,324 | 954,4 | 0,4 / 0,67 | 59 | nein | foliage |
| sonstiges | SM_heath_cross_01 | mittel | 2 918 | 0,287 | 1833,3 | 0,3 / 0,5 | 12 | nein | foliage |
| sonstiges | SM_forest_heather_01 | mittel | 2 906 | 0,286 | 1149,4 | 0,52 / 0,82 | 16 | nein | foliage |
| sonstiges | SM_billberry_02 | mittel | 2 814 | 0,277 | 1677,3 | 0,36 / 0,6 | 45 | nein | foliage |

Landschaft: 4 Teile, Quads/m 1, Material `MI_Eldarien_Landschaft_V9b`, Lagen: Wiese, Gras, Trockengras, Laub, Nadeln, Moos, Heide, Kraut, Erde, Schlamm, Lehm, Sand, Kies, Geroell, Fels, Felsplatte, Sandstein, Schnee, Eis, Lavafels, Lavasand, Algen, Toenung_R, Toenung_G, Toenung_B, __LANDSCAPE_VISIBILITY__
Gras im Material `M_Eldarien_Landschaft_V9b`: 10 Typen, 104 Sorten, Dichte-Summe 0 je 10 m x 10 m, max. Hoehe 2,49 m: GT_Wiese_Hoch 0; GT_Wiese_Kurz 0; GT_Blumen_Warm 0; GT_Blumen_Kalt 0; GT_Blumen_Bunt 0; GT_Kraut 0; GT_Farn 0; GT_Nessel 0; GT_Schilf 0; GT_Steinchen 0
Ausgeschlossen: SM_flower_sunroot_01 (himmel/hintergrund (Name))
Kameras: 1 Spielstart_E5 PlayerStart (-20 548, 49 548, 1759,5) pitch -5 yaw 118,8; 2 Spielstart_E5 PlayerStart (-20 548, 49 548, 1759,5) pitch -5 yaw 238,8; 3 Spielstart_E5 PlayerStart (-20 548, 49 548, 1759,5) pitch -5 yaw 358,8

## Netze C2_fenster (200x200 m) (haeufigste je Klasse)

| Klasse | Netz | Groesse | Instanzen | je 100 m2 | Grundflaeche m2 | Hoehe m (Mittel/Max) | Dreiecke LOD0 | Nanite | Quelle |
|---|---|---|---:|---:|---:|---|---:|---|---|
| baum | SM_dwarf_pine_small_01 | mittel | 175 | 0,438 | 368,9 | 1,29 / 1,64 | 550 | nein | foliage |
| baum | SM_dwarf_pine_small_02 | mittel | 155 | 0,388 | 321,1 | 1,13 / 1,4 | 659 | nein | foliage |
| baum | SM_dwarf_pine_medium_01 | mittel | 129 | 0,323 | 713,1 | 2,18 / 2,69 | 2 684 | nein | foliage |
| baum | SM_dwarf_pine_medium_02 | mittel | 104 | 0,26 | 697,4 | 2,18 / 2,69 | 2 950 | nein | foliage |
| baum | SM_dwarf_pine_medium_03 | mittel | 95 | 0,237 | 465,7 | 1,96 / 2,39 | 2 783 | nein | foliage |
| fels | SM_stonecrop_01 | mittel | 173 | 0,432 | 128,7 | 0,29 / 0,35 | 58 | nein | foliage |
| fels | SM_SmallStonesPack_14 | klein | 147 | 0,367 | 4,83 | 0,16 / 0,29 | 614 | ja | foliage |
| fels | SM_SmallStonesPack_07 | klein | 123 | 0,307 | 4,4 | 0,16 / 0,33 | 7 506 | ja | foliage |
| fels | SM_SmallStonesPack_13 | klein | 107 | 0,268 | 3,91 | 0,09 / 0,22 | 706 | ja | foliage |
| fels | SM_SmallStonesPack_06 | klein | 101 | 0,253 | 3,68 | 0,09 / 0,14 | 8 236 | ja | foliage |
| pflanze | SM_grass_03_A_1 | mittel | 391 | 0,978 | 181,1 | 0,89 / 1,1 | 64 | nein | foliage |
| pflanze | SM_grass_03_B_1 | mittel | 356 | 0,89 | 143,2 | 0,95 / 1,16 | 96 | nein | foliage |
| pflanze | SM_grass_02_A_1 | klein | 329 | 0,823 | 57,23 | 0,35 / 0,44 | 24 | nein | foliage |
| pflanze | SM_grass_02_B_1 | mittel | 298 | 0,745 | 107,3 | 0,41 / 0,49 | 26 | nein | foliage |
| pflanze | SM_grass_01_1 | mittel | 206 | 0,515 | 150 | 0,39 / 0,48 | 21 | nein | foliage |
| sonstiges | SM_heath_B_01 | mittel | 429 | 1,073 | 234,4 | 0,34 / 0,45 | 193 | nein | foliage |
| sonstiges | SM_heath_cross_01 | mittel | 404 | 1,01 | 273,5 | 0,32 / 0,41 | 12 | nein | foliage |
| sonstiges | SM_forest_heather_01 | mittel | 390 | 0,975 | 160,7 | 0,53 / 0,81 | 16 | nein | foliage |
| sonstiges | SM_billberry_dry_01 | mittel | 345 | 0,863 | 137,9 | 0,27 / 0,33 | 33 | nein | foliage |
| sonstiges | SM_billberry_02 | mittel | 342 | 0,855 | 197,4 | 0,36 / 0,45 | 45 | nein | foliage |
Ausgeschlossen: SM_flower_sunroot_01 (himmel/hintergrund (Name))
Kameras: 1 Spielstart_E5 PlayerStart (-20 548, 49 548, 1759,5) pitch -5 yaw 118,8; 2 Spielstart_E5 PlayerStart (-20 548, 49 548, 1759,5) pitch -5 yaw 238,8; 3 Spielstart_E5 PlayerStart (-20 548, 49 548, 1759,5) pitch -5 yaw 358,8

