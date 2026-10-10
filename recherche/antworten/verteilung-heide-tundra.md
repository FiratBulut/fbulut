# Verteilung Biomgruppe 3: Heide/Tundra (Skellige-Heide, Velen-Moor, Kovir-Hochland)

**Auftrag 11, Teil B3.** Biome `heide` und `tundra`, Thema `heide_tundra`, Foliage-Präfix `FT_EL_HT_`, Ordner
`/Game/Eldarien/Welt/Foliage/HeideTundra`. Stand 2026-10-10. Lieferung: dieser Bericht, `skripte/heide_tundra_regeln.json`
(19 Klassen in 4 Schichten, 142 Paletteneinträge = 124 verschiedene Netze, plus 29 Netze nur in den Overrides; alle 153 Pfade
gegen `netze.csv` geprüft), `skripte/heide_tundra_plan.py` (Planer nach FORMAT §3/§5, 941 Zeilen, nur NumPy).
**Alles UNGETESTET MIT ECHTDATEN** – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern (D2, G5) rauchgetestet (§4).
Web-Quellen waren nur als Suchmaschinen-Auszüge lesbar (6 WebSearch-Läufe); solche Belege sind mit **[Suchauszug]** markiert,
Zahlen ohne Beleg mit **Richtwert**.

Betroffene Felder laut `biome_je_feld.md`: **Tundra** D2 (47 %, 26–446 m, 57 % steil, Heide 22 / Trockengras 21 / Fels 19 / Schnee 9 %),
C2 (21 %), D3 (73 %), E3 (60 %), C3 (27 %; D3/E3/C3 Wüstenfelder), E2 (11 %); **Heide** G5 (77 %, flach, Trockengras 37 / Heide 16 %),
F5 (74 %, 9,7 % Wasser), F4 (21 %), G4 (22 %, Laub 75 % – Waldsperre). Der Planer arbeitet je Zelle nach Biom (`eigner.r8` + `welt.json`): heide und tundra voll, Nachbarbiome mit Faktor (gletscher 0,35, fjord 0,5,
frost 0,3, bergwald 0,25, aue/kueste 0,4, elfenwald 0,15, sumpf 0,3; Wüste/Canyon/Ödland/Lava/Dschungel 0). Zellen mit Heide-Lage
≥ 40 % gelten unabhängig vom Eigner als Heide (Faktor ≥ 0,8), Trockengras ≥ 50 % über 120 m als Tundra (≥ 0,6). Für `eigner = 0`
(Weltgelände) nimmt der Planer das dominante Feldbiom aus `daten/biome_je_feld.json`, sonst die Tabelle `feld_biom_fallback`, sonst aue.

## 1. Witcher-Analyse: Skellige-Heide/Hochmoor, Velen-Moor, Kovir-Hochland

**Was Skellige über die Baumkrone hinaus füllt.** Die Skellige-Inseln bestehen aus drei Höhenbändern, die in den Zielbildern
(witcher_06: Felswand → hausgroße Blöcke → Kopfsteine → Schnee in Rissen) und in der Bildkritik als Prinzip festgehalten sind:
jede Fläche trägt drei bis vier ineinandergreifende Größenstufen plus Makro-Variation im 100–500-m-Maßstab. Auf der Skellige-Heide
sind das: (a) ein durchgehender Heidekraut-Teppich (Calluna) kniehoch in **Flecken** von 20–60 m, dazwischen Trockengras, Flechtenboden
und nackter Fels; (b) darüber 0,5–2 m: Wacholder, Ginster, Krüppelkiefern, einzelne Birken, Findlinge mit Flechten; (c) Bäume nur als
windschiefe Einzelkiefern auf Kuppen und kleine Gruppen in Mulden, darüber die Baumgrenze mit Blockfeldern und Schnee; (d) Spuren:
Trockensteinmauern, Schafpferche, Steinkreise und Steinmänner als Wegmarken im Nebel. CDPRs eigene Beschreibung des Verfahrens ist
bekannt: Vegetation wird mit **Pinseln je Geländetyp** gesetzt, mit einstellbarem Spacing und Scale-Variation, in der Reihenfolge
große Bäume → kleine Bäume → Farne → Gras **[Suchauszug: 80.lv „World Building of Witcher 3“, M. Janiszewski]**. Die Artstation-Seite
von Mark Foreman (Location-Blockout, Lighting, Polish) nennt Skellige als Schwerpunkt der Final-Polish-Phase, gibt aber keine Zahlen
**[Suchauszug: artstation.com/artwork/L8LlP]**; die UE4-/SpeedTree-Nachbildung „The Fields of Ard Skellige“ (exp-points.com) rät,
Foliage auf große Formen und Silhouette zu bauen, damit die Szene auch in der Distanz liest **[Suchauszug]**. Für die Heide heißt das:
die Lesbarkeit kommt aus den **Flecken** (violett/braun/grau im 20–60-m-Maßstab), nicht aus Einzelpflanzen. Deshalb steuert der
Planer Heidekraut, Gras und Wollgras über Wertrauschen mit Schwellen (§2 „Flecken“), nicht über gleichmäßige Dichte.

**Moor vs. Heide (Velen-Moor).** Wikipedia trennt „heath“ (Tiefland, trocken, frei dränend, saure Böden, niedriges Zwergstrauchgesicht)
von „moor“ (Hochland, hoher Niederschlag) **[Suchauszug: en.wikipedia.org/wiki/Heath, /Moorland]**; die britischen NVC-Klassen geben
Richtwerte für die Struktur: Trockenheide H10/H12 (Calluna–Erica cinerea bzw. Calluna–Vaccinium) hat Calluna-Dominanz, meist 0,3–0,5 m,
ungebrannt bis 1 m hoch, Beweidung ersetzt Zwergsträucher durch Gras **[Suchauszug: JNCC CSM Upland Habitats 2009; sac.jncc.gov.uk
H4030]**. Velens Moor (Crookback Bog) ist das nasse Gegenstück: Wollgras-Weiß über Torfmoos, Tümpel mit Binsenrand, Totbäume und
gebleichte Stämme im Wasser, Torfstiche. Velen-Artist Kacper Niepokólczycki nennt als Thema „desperation, hunger and hopelessness“
und als Vorbild polnische Dörfer **[Suchauszug: 80.lv]** – das Moor ist bewusst karg, mit wenigen, aber starken Akzenten (Hangman's
Tree). In Eldarien liegt dieser Charakter in den Moortümpeln von F5/G5 (Wasser 9,7 bzw. 3,9 %) und in den Moos-/Schlammflächen; die
Schicht `5 wasserkante` setzt dort Wollgras-Stellvertreter, Binsen, Moorsteine, Treibholz und Totbäume (Wasser-Bonus ×2 im 30-m-Band).

**Kovir-Hochland (Witcher-4-Demo).** Die Tech-Demo (State of Unreal 2025, PS5, 60 fps, Ray Tracing) zeigt Kovir mit Nanite Foliage
(einzelne Blätter und Zweige mit Wind) und FastGeo Streaming ohne Pop-in **[Suchauszug: cdprojektred.com Blog 149; blog.playstation.com
2025/06/03; gamingbolt „9 takeaways“]**; die Landschaft ist ein kaltes, offenes Hochland mit Nadelwald in den Tälern, Fels und
kurzem Gras darüber. Zahlen zu Dichten nennt keine Quelle; abgeleitet werden nur drei Regeln: Bäume brechen an der **Baumgrenze** ab
(Eldarien: D2 Ø 182 m, max 446 m, Schnee ab ~300 m → Einzelbäume bis 300 m, Krüppelholz bis 380 m, Zwergstrauch bis 460 m, Gras bis
520 m, **Richtwert** aus den Lagenanteilen in `biome_je_feld.md`), Bäume auf Kuppen sind **windschief** und klein (Lee-Neigung 4–12°,
Maßstab 0,6–0,85), in Mulden stehen sie in Gruppen und größer (2–5, Maßstab 0,95–1,25).

**Dichten und Gruppen (Richtwerte aus Zielbildern und NVC).** Heidekraut-Deckung in Heideflecken ≈ 35 % (Calluna dominant mit
Gras-/Flechtenlücken); Grasbüschel 0,3–1,6 m dazwischen; 1 Strauch je 300–450 m²; 1 Krüppelkiefer je 1 000–2 500 m²; 1 Einzelbaum je
6 000–8 000 m²; Findlinge 3–8 je km²; Flechtensteine 1 je 100–250 m²; Kiesel 0,014–0,035/m². Farbakzente: Heideblüte rosa-violett nur
in Heideflecken, Wollgras-Weiß am Tümpel, Moorbirke hell am Moorrand, Flechten-Gelbgrün auf Südseiten der Steine (Teil C).

**Was heute fehlt (Ist-Bilder).** BERG8_D2: glatte Doppelkuppeln „wie Dünen“, Felsschalen als Konfetti; BACH3_G5: „Heidefleck
rechts abrupt“, Wiese ein Beige, Büsche als gleichmäßige Punkte (Bildkritik: Heide-Kante mit Noise 10–20 m aufbrechen, Büsche in
Gruppen 3–7). Genau das liefert die Ebene: Heideflecken mit weichem Rand (~3–6 m), Wacholder 1–5, Krüppelkiefern 1–3, Flechtensteine 2–6.

**Quellen (6 WebSearch-Läufe, nur Suchauszüge):** 80.lv „World Building of Witcher 3“ (Janiszewski, Niepokólczycki) · ArtStation
Mark Foreman „The Witcher 3: Wild Hunt“ · exp-points.com „The Fields of Ard Skellige (UE4/SpeedTree)“ · Wikipedia „Heath“, „Moorland“ ·
JNCC „Common Standards Monitoring Guidance for Upland Habitats“ (2009), sac.jncc.gov.uk/habitat/H4030 · cdprojektred.com Blog 149,
blog.playstation.com (Witcher-4-Tech-Demo 2025) · Fab/Quixel „Cotton Grass“ (Megascans, ab 3,99 USD), quixel.com/news „Quixel on Fab:
New Megascans and Megaplants“. Keine Quelle nennt Instanzen je m²; alle Dichten sind Richtwerte.

## 2. Regelwerk (`heide_tundra_regeln.json`) – Erklärung je Schicht

**Gemeinsame Steuergrößen.** Dichte je Klasse in Instanzen je m² je Profil (`heide` / `tundra`), multiplikativ mit: Biomfaktor
(oben), Lagenfaktor (gewichtetes Mittel der `lage_*.r8`-Deckungen mit vier Gewichtstabellen `pflanze_trocken`, `pflanze_feucht`,
`stein`, `streu`; z. B. Heidekraut: Heide 1,6, Trockengras 1,1, Moos 0,7, Fels 0,1, Eis/Lava 0), Hang (voll bis `hang_voll_bis`, null ab
`hang_null_ab`; Steine 32/50°, Pflanzen 25–30/38–42°, Wasserkante 15–20/26–32°), Höhenstufen nur im Tundra-Profil (Bäume 240→300 m,
Sträucher 320→380 m, Zwergstrauch 460 m, Gras 520 m; Heide-Profil ohne Grenze), Schnee-Lage (Pflanzen ×0,15, Steine ×0,6 bei voller
Deckung), Kronendach aus Bestands-/Witcher-/Houdini-Bäumen (Box 9 m, Lichtpflanzen ×0,25 unter Kronen; Steine/Bäume ausgenommen),
Exposition (Höhe minus Gauß 40 m, normiert auf 8 m: +1 Kuppe, −1 Mulde; Flechtenstein +80 %, Krüppelkiefer +60 %, Wacholder +30 %),
Mulde (Gauß 12 m; Jungwuchs ×1,5, Kiefern-Gruppen ×3), Wassernähe (Jungwuchs ×2,5/40 m, Moorbirke ×3/45 m, Totbaum ×2/30 m), Baumnähe
(Zweige ×2,5 in 12 m, Totholz ×2 in 15 m). Sperren: Laub+Nadeln ≥ 0,6 → ×0,15 (G4),
Lavafels/Lavasand ≥ 0,3 und Eis ≥ 0,3 → 0; Wüstenfelder C3/D3/E3 → ×0,7, nur tundra/heide-Zellen, Sand+Sandstein linear 1→0 bis 50 %
Deckung, darüber gesperrt, kein `entfernen`. Abstände: 2,5 m Kleinzeug / 4 m Bäume, Krüppelkiefern, Totholz zu Wegen; 5 m zu Orten;
0,3–2 m zu Wasser je Klasse; 1,5 m zu Bestandsstämmen, 1 m zu sonstigen Bestandsinstanzen (Witcher, Mittelschicht, Felsgruppen, Ufer);
neue Bäume 4–6 m zu Bestandsbäumen und untereinander (grobes Raster 0,7 × Abstand). Gruppen: Zentren = Dichte/Gruppenmittel,
Mitglieder im Radius, erneut gegen Sperrmaske geprüft. Zufall: Hash aus absoluter Rasterkoordinate, Seed 3311 und Klassenkanal →
deterministisch und nahtlos über Feldgrenzen (Fenster Feld + 64 m).

**Flecken.** Drei Wertrausch-Felder auf absolutem Gitter (2 Oktaven, Smoothstep-Schwelle): `heidekraut` Skala 26 m, Schwelle 0,55,
weich 0,12 (Deckung ≈ 35 %); `gras` 40 m, Schwelle 0,35, weich 0,25 (breite, weiche Grasflächen zwischen den Heideflecken);
`wollgras` 14 m, Schwelle 0,6 (Wollgras-Horste am Tümpel, nicht als Ring).

**Schicht `0 boden`** (Sichtweite 5 000–15 000 cm, keine Kollision):
- `kiesel` (SmallStonesPack_01–14 ohne 05/10/12, stone_04/05/06/08): tundra 0,035, heide 0,014/m², Gruppen 3–9 in 1,6 m, Maßstab
  0,9–1,6, 40 % eingegraben, voll auf Normale gekippt, Hang bis 50°. Niedrigste Priorität → wird zuerst ausgedünnt.
- `flechtenstein` (< 0,8 m: LichenedForestBoulder_01, mountain_rock_small_01_1/2/4/5, mountain_rock_big_01_2/3, Nordic_Forest_Rock_Small
  xjijbgx; heide: s_rock_01–03, stones_01_3): tundra 0,009, heide 0,004, Gruppen 2–6 in 2,2 m, Kuppen +80 %, 38 % eingegraben,
  Schatten an, Sichtweite 15 000. Flechten über Material-Auflage (Teil C `M_EL_Fels_Auflage`, Flechten-Variante).
- `streumatte` (DeadLeaves_12–14, dead_grass_01–03 als Torf-/Streu-Stellvertreter): 0,008–0,009, Gruppen 1–3, Lagen `streu` (Heide,
  Trockengras, Moos 1,0–1,2), Sichtweite 5 000.
- `zweige` (DryBranches_01/04/05/07, mountain_branch_01_01/02): 0,003–0,004, ×2,5 in 12 m um Bäume.

**Schicht `1 mittel`** (0,3–3 m):
- `heidekraut` (heath_A/B_01, forest_heather_01/simple_01, billberry_01/02; tundra: heath_A/B, lingonberry_01/02, billberry_dry_01,
  billberry_03, rhododendron_01): 0,07 (heide) / 0,055 (tundra) **innerhalb der Flecken** → Feldmittel ≈ 0,02–0,025/m²; Gruppen 4–12 in
  2,5 m, Maßstab 1,1–1,9 (die 0,2–0,5-m-Netze lesen so als Polster; `GT_Heide`-GPU-Gras bleibt der Teppich darunter), Sichtweite 12 000.
- `grasbueschel` (Tundra_Grass VarA/C/D/F/G/H 0,3–0,7 m, grass_03_A/B 1,06 m; heide: grass_bush_01/03/04, grass_meadow_03/06/08 bis
  1,6 m): 0,028–0,03 in `gras`-Flecken, Gruppen 3–8, Maßstab 0,8–1,4 → Höhenstaffel 0,3–1,6 m.
- `wacholder` (Stellvertreter: dwarf_pine_small_01/02, medium_01/03, rhododendron_02; heide: sea_buckthorn_03–06 grau-grün, beach_rose_04/06,
  dwarf_pine_small_01): 0,0022–0,0028, Gruppen 1–5 in 3 m, Kuppen +30 %, Sichtweite 30 000, Schatten an.
- `kruepelkiefer` (pine_beach_crooked_01/02, dwarf_pine_big_01/02, pine_beach_short_01/02): 0,0004–0,0009, Gruppen 1–3 in 4 m, Kuppen +60 %,
  Höhenstufe Strauchgrenze (380 m, Abnahme ab 320 m), **Wind**: lee-Neigung 4–12° bei expo > 0,25, **Kollision** ab 2 m Netzhöhe,
  Sichtweite 35 000.
- `jungwuchs` (Hornbeam_Sapling_01/02, Seedling_01/02, grey_willow_02/03; tundra: Forest_pine_plant_01/02, grey_willow_01/02): 0,0005–0,0008,
  Gruppen 2–5, Wasser ×2,5 (40 m), Mulde ×1,5, Lagen `pflanze_feucht`.
- `heideblüte` (beach_rose_02/03/04_with_pink_flowers, Maßstab 0,6–0,9): nur heide 0,0012 in Heideflecken, Gruppen 2–4 – Farbakzent bis
  ein Calluna-Blütennetz da ist.
- `totholz` (beach_driftwood_01 gebleicht, Forest_pine_04/08_log, dead_log_03/04, OldTreeBranch_06): 0,00035–0,0004, Yaw hangabwärts ± 25°,
  28 % der Netzhöhe eingegraben, **Kollision** ab 0,3 m, ×2 in 15 m um Bäume, Sichtweite 40 000.
- `stumpf` (pine_stump_01–03, BirchTreeStump_01): 0,00015–0,0002, 10 cm eingegraben.

**Schicht `2 baum`** (Kollision, Sichtweite 0, Kippen ≤ 0,08, Eingraben 15 cm):
- `einzelkiefer` (Forest_pine_01, pine_beach_01_A/B, 02_A, 03_A, 04_A): Feldmittel 0,00012–0,00016; auf Kuppen einzeln, klein (×0,6–0,85)
  und windschief; in Mulden (Krümmung > 0,35) Gruppen 2–5 in 9 m, ×3 Dichte, größer (×0,95–1,25); Baumgrenze 300 m (Abnahme ab 240 m);
  6 m Mindestabstand; Hang ≤ 38°.
- `moorbirke` (einziges Birkennetz Big_Tree_birch_01, 11,5 m, kein Nanite, 28 k Dreiecke, auf 0,6–1,0 → 7–11 m): 0,00005–0,00009,
  Gruppen 2–4 in 7 m, Wasser ×3 (45 m), Mulde ×1,5, in Tundra nur < 250 m, Hang ≤ 32°.
- `totbaum` (DeadTree_01/02, Dead_Tree qlEtl): 0,00003–0,00004, Wasser ×2 (30 m), bis Strauchgrenze.

**Schicht `5 wasserkante`** (Band um `karte_wasser.r8`; Moortümpel, Bäche):
- `wollgras` (Tundra_Grass VarB/C/G, grass_meadow_08 hoch skaliert 0,9–1,4): 0,12/m² im Band 0,5–9 m **und** ×0,35 auf Moos/Schlamm ≥ 50 %
  (nasse Moorflächen ohne offenes Wasser), in `wollgras`-Flecken, Gruppen 4–10, Hang ≤ 30°.
- `seggen` (ToadRush_011–013 kleine Varianten ≤ 1,5 k Dreiecke; heide zusätzlich Rohrkolben_Jung_1/3): 0,05–0,07 im Band 0,3–4 m, Gruppen 3–8.
- `moorstein` (NordicBeachRock_01, SmallStonesPack_05/10/12, mountain_rock_small_01_3): 0,025–0,04 im Band 0,2–3 m, 45 % eingegraben –
  **entfällt**, wenn `ufer/foliage_<Feld>/` existiert (Ufer-Ebene `FT_EL_UF_*` liefert dann die Kiesel).
- `treibholz` (beach_driftwood_01, dead_log_03): 0,0015–0,002 im Band 0,5–5 m, 30 % eingegraben.

**Budget** (`budget`): Ziel 45 000, harte Grenze 60 000 je Feld, ≤ 3 000 mit Kollision. Ausdünnung deterministisch (Hash je Instanz)
von hinten nach `prioritaet`: Kiesel → Streumatte → Zweige → Grasbüschel → Flechtenstein → Heidekraut → Treibholz → Moorstein →
Wollgras → Seggen → Heideblüte → Jungwuchs → Stumpf → Totholz → Wacholder → Krüppelkiefer → Totbaum → Moorbirke → Einzelkiefer; je
Klasse im ersten Durchgang höchstens auf 25 % gekürzt, danach proportional bis zur harten Grenze; Kollisionsklassen separat.

**Overrides für Teil C/D** (gleiche Schlüssel wie `felsgruppen_regeln.json` / `spuren_regeln.json`; nicht vom Heide-Planer gesetzt):
- `felsgruppen_overrides.heide`: Palette `heide` neu (hero: Meadow Rock_05, Big_Rock_01/02, IcelandicBoulder_03, NordicBoulder_01;
  block: Meadow Rock_01–07, IcelandicBoulder_01/02, Granite_Rock pkeeM/pjtsT), Biomfaktor 0,7, Klassen `band`, `wand`, `fuss`, `blockstrom` aus (Flachheide), `kuppe` p 0,9 mit Umkreis 40 m, **neu `findling_frei`**:
  freistehende **Findlinge** 3–6 je km² auf Hang 0–14°, 80 % Hero, 40–55 % eingegraben, nie näher als 120 m zueinander, Flechten-Auflage
  (Weiß-Grau 0,15 + Gelbgrün 0,05 statt Moos).
- `felsgruppen_overrides.tundra`: Palette `tundra`, Faktor 1,0, `blockstrom` ×1,3, **neu `blockfeld`** (Felsenmeer/Frostschutt): Raster
  12 m auf Hochflächen > 280 m mit Hang 6–24°, p 0,35, 2–5 Blöcke + 6–14 Steine + 10–20 Kiesel, gleich groß, kantig, 40–55 % eingegraben;
  `findling_frei` 4–8 je km²; Auflage `flechten_schnee` (Flechten Südseite, Schnee Nordseite/Simse nach Normale).
- `spuren_overrides.heide`: **Steinmauern** statt Holzzäune (25–90 m, 2–4 je km², 4 Lagen 0/0,26/0,5/0,72 m mit 100/90/60/30 %,
  Steinabstand 0,42 m, 12 % Lücken, hang- oder wegparallel, mountain_rock_small_01_*, s_rock_01/02); **neu `pferch`** (Schafpferch 8–14 m Rechteck/Ring aus Trockenmauer, 1 Öffnung 1,8 m, 1–2 je Ort im Ring
  40–220 m, 0–1 frei je Feld ≤ 90 m vom Wasser, Hang ≤ 8°, Beiwerk Trough_01a, Hay_02, wooden_pales_1_01); **neu `torfstich`** (0–3 je Feld
  auf Moos ≥ 35 %/Schlamm ≥ 20 %, ≤ 60 m vom Wasser, Hang ≤ 4°, 6–10 × 12–24 m, Tiefe 60 cm als Punktliste für Höhenpass/Decal, 1–3
  Soden-Stapel Pile_WoodLog_02a × 0,7–0,9); **neu `steinkreis`** als Blickziel (1 je Feld auf Kuppe mit Prominenz ≥ 10 m, Radius 6–11 m,
  5–9 Steine 1,3–2,6 m hochkant, 25 % umgefallen, Akteure mit Kollision); Steinmänner 3 je km²; Schreine 50 % der Wegkreuze
  (Sviatovid_Stone); Wegsaum-Einfriedung als Mauer; keine Obstgärten; Feldstreifen max 4 je Ort; Schäfer-/Torfhütte fehlt (Einkaufsliste).
- `spuren_overrides.tundra`: verfallene Mauern (15–50 m, 0–2 je km², 3 Lagen, 25 % Lücken, nur < 300 m), Sommerweide-Pferch 0–1,
  Torfstich 0–2 (< 250 m), Steinkreis 5–7 Steine mit 40 % umgefallen, **Steinmänner 8 je km² und alle 70–110 m am Weg** (Wegmarken in
  Nebel/Schnee), Schreine 30 %, keine Obstgärten, Feldstreifen max 1 je Ort / 2 je Feld, Jagdhütte fehlt.

### 2.1 Planer `heide_tundra_plan.py` (FORMAT §3/§5)

- **Aufruf:** `python -I scripts/heide_tundra/heide_tundra_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]
  [--entfernen "p1,p2"]`; Regeln standardmäßig `heide_tundra_regeln.json` neben dem Skript. Keine Unreal-Importe; NumPy, Pillow nur
  für `--bild` (ohne Pillow PPM); numba wird gemeldet, nicht gebraucht.
- **Lesen:** `hoehe.f32` per `np.memmap`, nur Fenster Feld + 64 m (NY = 7057, NX = 9577; J-Spalte bei 9577 geklippt → J-Felder 505 m
  breit); `karte_*.r8`, `lage_*.r8` (22 Namen), `eigner.r8` + `welt.json` optional mit Warnung; Bestand aus `bestand/`, `witcher/`,
  `mittelschicht/`, `felsgruppen/` (Feld + 8 Nachbarn; Bäume vs. Sonstige über `rolle`/`gruppe`/Name), `ufer/foliage_<Feld>/`,
  `instanzen/instanzen.json` (fehlt → Hinweis im Protokoll und in `plan.json["hinweise"]`); `daten/netze.csv` aus production, neben dem
  Skript oder aus der Repo-Vorlage (Pfadprüfung: fehlende Netze werden mit Warnung gestrichen; Netzhöhen für Eingraben/Kollisionsschwelle).
- **Rechnen:** Hang/Normale aus Gauß(2 m)-Gradient, Exposition, Mulde, Wasserdistanz (Jump-Flooding), Dilatation für Abstände,
  Kronendach als Box-Faltung, Flecken als Wertrauschen; je Klasse Dichtekarte → Bernoulli-Zug der Zentren → Mitglieder → Attribute
  (Maßstab, Wind, Netzwahl je Profil, Eingraben, Quaternion aus Normale + Lee-Lehnen + Yaw). Kein Python-Loop über Zellen.
- **Schreiben:** `export/unreal/welt/heide_tundra/<Feld>/<Netz>.f32` (alte f32 vorher gelöscht) und `plan.json` mit `stand, feld,
  ebene, instanzen, dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene, schicht, klasse}, ft_ordner, ft_praefix,
  entfernen (nur wenn gesetzt; in Wüstenfeldern nie), klassen, schichten, kollision_instanzen, profil_anteil_feld, biome_fenster,
  feldbiom_fuer_eigner0, quellen_bestand, hinweise, ungetestet`. Nur Instanzen **im Feld** werden geschrieben (Rand dient der Nahtlosigkeit).
  `--bild` → `docs/pruefung/heide_tundra/<Feld>.png` (1 px = 1 m; Profil heide violett-grau / tundra grün-grau mit Schummerung,
  Wasser blau, Weg gelb, Ort rot, Sand-Sperre beige, nicht planbare Biome dunkel, Klassen nach `farbe`, Bäume/Krüppelkiefern/Totholz 3 × 3 px).

## 3. Abgrenzung zu vorhandenen Ebenen: ergänzen, nicht ersetzen

| Ebene | Verhältnis zur Heide/Tundra-Ebene | `entfernen`? |
|---|---|---|
| Witcher-Bewuchs `FT_EL_WIT_*` | Andere Netze, andere Steuergrößen (Flecken, Höhenstufen, Exposition); WIT-Instanzen als Sperrpunkte (1 m), WIT-Bäume als Kronendach | nein. Nach Sichtung in D2/G5 `FT_EL_WIT_maple_bush_0,FT_EL_WIT_Elderberry_` per `--entfernen` (Laubgebüsch wirkt fremd) |
| Wald-Bestand `FT_EL_BST_*` | Kronendach → Lichtpflanzen ×0,25; neue Bäume 4–6 m Abstand; in G4 (Laub 75 %) sperrt die Waldlage zusätzlich ×0,15 | nein |
| Mittelschicht `mittelschicht/` (Teil D: heide/tundra Beere/Heide 0,045/0,040, Grasbüschel 0,02/0,03) | **Überschneidung** bei Zwergstrauch und Grasbüschel. Vorschlag: in den zehn Feldern nur `heide_tundra`, Mittelschicht-Biomfaktor heide/tundra = 0 (oder hier `--faktor 0.5`); läuft die Mittelschicht zuerst, werden ihre Instanzen Sperrpunkte | nein |
| Felsgruppen `felsgruppen/` (Teil C, `FT_EL_FG_*`) und Felsschalen `FT_EL_FS_*` | Alle Felsen > 0,8 m kommen von dort (Overrides §2: Findlinge, Blockfelder, Kuppen); diese Ebene setzt nur Steine < 0,8 m und meidet Felsgruppen-Instanzen (1 m) | nein |
| Ufer `FT_EL_UF_*` | Moorsteine entfallen, wenn `ufer/foliage_<Feld>/` existiert; Pflanzen der Wasserkante bleiben (Band 0,3–9 m) | nein |
| Spuren `spuren/` (Teil D) | Steinmauern, Pferche, Torfstiche, Steinkreise über `spuren_overrides`; diese Ebene setzt keine Spuren | nein |
| Wüste `FT_EL_WU_*` (C3, D3, E3) | nur ergänzen: ×0,7, nur tundra/heide-Zellen, Sand/Sandstein-Sperre, `entfernen` wird auch per CLI ignoriert | nein |
| Landschafts-Gras `GT_*` (`GT_Heide`, Trockengras) | bleibt Teppich 0,2–1,2 m; Heidekraut-Polster (×1,1–1,9) und Büschel bis 1,6 m sind die Stufe darüber | nein |

Begründung: Hauptfehler laut Bildkritik ist „jede Fläche trägt genau einen Maßstab“; die Ebene fügt die fehlenden Stufen (Flecken
20–60 m, Polster 0,3–0,8 m, Sträucher 1–3 m, Einzelbäume) hinzu. Entfernen erst, wenn im Editor doppelte Gebüsche sichtbar sind.

## 4. Testanleitung

**Rauchtest Cloud (gelaufen am 10.10., wiederholt nach dem Sitzungsabbruch).** Mini-Produktionswurzel mit `hoehe.f32` in voller
Größe 7057 × 9577 (memmap; D2-Fenster: welliges Hochland 159–355 m, 25 % über 300 m, 62 % > 30° Hang; G5-Fenster: flache Heide 8–38 m),
`karte_wasser.r8` (zwei Moortümpel 32 + 20 m Radius in eingeebneten Moorbecken), `karte_weg.r8` (Diagonale 4 m), `karte_ort.r8`
(60 × 60 m), `eigner.r8` (D2 = 7 tundra, G5 = 12 heide) + `welt.json`, `lage_Heide/Trockengras/Moos/Geroell/Schnee/Fels/Wiese/Sand.r8`,
`bestand/D2` (300 Kiefern), `witcher/G5` (400 maple_bush als Sonstige), `ufer/foliage_D2` (150 Kiesel), `daten/netze.csv`.
Ergebnis `python -I scripts/heide_tundra/heide_tundra_plan.py D2 G5 --bild --basis .` (Python 3.13, NumPy 2.5, 4 Kerne, ohne numba):

| Feld | Instanzen (vor Budget → nach) | Kollision | Netze | boden | mittel | baum | wasserkante | Laufzeit |
|---|---|---|---|---|---|---|---|---|
| D2 | 51 373 → 44 905 | 409 | 119 | 26 384 | 18 335 | 107 | 79 | 4,8 s |
| G5 | 69 711 → 44 976 | 738 | 102 | 9 465 | 34 925 | 298 | 288 | 4,7 s |

Größte Klassen D2: Kiesel 13 002, Heidekraut 8 266 (31 % der Zellen per Heide-Lage ≥ 40 % als Heide-Profil), Grasbüschel 7 671,
Flechtenstein 7 662, Wacholder 1 476, Krüppelkiefer 413, Einzelkiefer 83 (nur unter 300 m), Wollgras 22; Moorstein übersprungen (Ufer-Ebene
vorhanden). G5: Heidekraut 20 922, Grasbüschel 9 664, Flechtenstein 3 473, Kiesel 2 827 (auf 25 % gekürzt), Wacholder 2 307, Jungwuchs 616,
Krüppelkiefer 454, Heideblüte 388, Wollgras 196, Einzelkiefer 183, Moorbirke 83, Seggen 65, Totbaum 32, Moorstein 21. Prüfskript: alle 221 f32 durch 10 teilbar, Anzahl = `plan.json`,
Schema vollständig (je Datei `pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene`; Kopf mit `ebene`, `ft_ordner`,
`ft_praefix`), Quaternionen normiert (|q|−1 ≤ 1,2·10⁻⁷), **0 Instanzen auf Wasser/Weg/Ort, 0 außerhalb des Feldes**, z − Gelände
−1,17 m (Flechtensteine 38 % eingegraben, ×1,5 skaliert) bis +0,86 m (Bilinear-Artefakt an 40°-Hängen der Synthetik; auf G5 −0,38 …
+0,25 m). Zwei Läufe byte-identisch (MD5 über 218 Dateien); `--faktor 0.5` → G5 34 593. Fehlerfälle (Feld K9, fehlende Basis, fehlende
Regeldatei) → klare Meldung und Exit; D3 (Wüstenfeld, nur 100-m-Landstreifen aus dem D2-Rand) 3 420 Instanzen mit Faktor 0,7; J7
(Randspalte, Fenster 569 × 1073) 0 Instanzen in 1,1 s; E2 mit `biome_je_feld.json` → eigner 0 als gletscher (×0,35), 1 583 Instanzen.
Prüfbilder `docs/pruefung/heide_tundra/D2.png`, `G5.png` (1008 × 1008): Heideflecken violett mit weichen Rändern, Kiesel/Flechtensteine
als gelbe Streu an Hängen, Bäume nur in Mulden, Wollgras weiß und Binsen am Tümpel, Ort rot, Weg gelb.

**Erwartete Instanzzahlen je Feld (Richtwert, Spanne ±35 %; Grundlage Biom-/Lagenanteile in `biome_je_feld.md`):**

| Feld | Biom-/Landanteil | gesamt | boden | mittel | baum | wasserkante | Kollision |
|---|---|---|---|---|---|---|---|
| D2 | tundra 47, gletscher 34 (×0,35), fjord 19 (×0,5); 57 % steil | 28 000–52 000 | 14 000–26 000 | 12 000–22 000 | 60–250 | 100–800 | 150–500 |
| G5 | heide 77, dschungel 22 (×0); flach, Wasser 3,9 % | 38 000–58 000 (Budget greift) | 8 000–14 000 | 28 000–38 000 | 200–450 | 600–2 500 | 500–1 100 |
| F5 | heide 74, aue 25; Land 58 %, Wasser 9,7 % | 15 000–35 000 | 4 000–9 000 | 10 000–22 000 | 100–300 | 1 500–5 000 | 200–600 |
| D3 (Wüste ×0,7) | tundra 73, Sand 32 % | 10 000–28 000 | 4 000–12 000 | 5 000–14 000 | 30–150 | 300–1 500 | 50–250 |
| E3 (Wüste ×0,7) | tundra 60, Sand 52, Schnee 17 % | 5 000–16 000 | 2 000–7 000 | 2 500–8 000 | 10–80 | 100–600 | 20–150 |
| C3 (Wüste ×0,7) | tundra 27 (aue ×0 im Wüstenfeld) | 3 000–10 000 | 1 000–4 000 | 1 500–5 000 | 10–60 | 50–400 | 10–100 |
| C2, E2 | tundra 21 / 11, gletscher ×0,35, Schnee 47 % (E2) | 3 000–14 000 | 1 500–7 000 | 1 500–6 000 | 10–60 | 50–500 | 20–120 |
| F4 | heide 21, aue 79 (×0,4), Land 54 % | 6 000–16 000 | 2 000–5 000 | 4 000–10 000 | 30–120 | 200–1 200 | 50–200 |
| G4 | heide 22, elfenwald 76 (×0,15), Laub 75 % (×0,15) | 1 500–6 000 | 500–2 000 | 1 000–4 000 | 10–40 | 50–300 | 10–60 |

**Prüfkameras (Feld, Position, Blick):**
1. **G5 Heidefleck, Augenhöhe 1,7 m**, Kuppe 200 m nordöstlich des Moortümpels, Blick nach Südwesten in tiefem Seitenlicht (Vergleich
   BACH3_G5). Erfolg: Heidekraut-Polster lesen als violett-braune Flecken 20–60 m mit weichem Rand (kein harter „Heidefleck“), dazwischen
   Grasbüschel in 2–3 Höhen, alle 10–20 m ein Wacholder/Sanddorn, Findling mit Flechten im Mittelgrund; innerhalb 10 m mindestens ein
   Objekt in 0,5–3 m Höhe.
2. **G5/F5 Moortümpel, 2 m Höhe am Ufer**, Blick über das Wasser gegen die Sonne. Erfolg: Binsen 0,3–4 m, Wollgras-Horste 0,5–9 m in
   Flecken (nicht als Ring), Treibholz und 1–2 Moorbirken am Rand, Totbaum als Silhouette, nichts im Wasser, keine Pflanze schwebt.
3. **D2 Kuppe 280 m, 1,7 m**, Blick nach Nordwesten (gegen den Wind). Erfolg: Einzelkiefern klein und leewärts (SO) geneigt, Krüppel-
   kiefern in 1–3er-Gruppen, Flechtensteine auf der Kuppe dichter, Heide/Trockengras-Flecken, Schnee ab ~330 m ohne Pflanzen.
4. **D2 Mulde 220 m, 3 m Höhe.** Erfolg: Kiefern-Gruppe 2–5, größer als auf der Kuppe, Jungwuchs/Grauweide, Zweige und Totholz um die Stämme.
5. **D2 Hochfläche > 300 m, Draufsicht 150 m.** Erfolg: keine Bäume über 300 m, Blockfelder (Teil C) mit Kiesel-/Flechtenstein-Saum.
6. **Nahtprüfung** G5/F5 und D2/C2 (Draufsicht 100 m): Flecken und Gruppen laufen über die Feldgrenze, keine Dichtesprünge.

**Erfolgskriterien in Zahlen:** Instanzen je Schicht in der Tabelle; Kollision < 3 000 (D2/G5 Rauchtest 409/738); Setzer-Zeit je Feld
< 5 min (≤ 124 Foliage-Typen `FT_EL_HT_*`, davon 15 Baum-/Stamm-/Krüppelkiefer-Typen mit Kollision); Nicht-Nanite-Netze
(Big_Tree_birch_01, pine_beach_*, Mountain-Gräser) auf LOD-Übergänge geprüft; PNG und `plan.json` je Feld vorhanden.

## 5. Einkaufsliste fehlender Assets (frei bevorzugt, Stufe High 4K)

| Was | Exakter Name (Fab/Megascans), Befund | Stufe | Wofür | Status |
|---|---|---|---|---|
| **Heidekraut in Blüte** (Calluna vulgaris, Erica cinerea) | Fab-Suche „heather calluna“ beim Verkäufer Quixel Megascans ohne Treffer **[Suchauszug]**; Drittanbieter „Heather Plant Pack“ direkt auf Fab prüfen | High, Nanite | `heidekraut` (Ersatz heath_A/B, billberry), `heideblüte` (Ersatz beach_rose_pink) – der violette Skellige-Akzent | **offen**, wichtigste Lücke |
| **Wacholder** (Juniperus communis, Säule + Kriechform 0,5–2 m) | nur Megascans-Zweig-Atlanten „Desert Western Tree Branch Juniper“ gefunden, keine Pflanze **[Suchauszug]**; Fab „Juniper bush Nanite“ prüfen | High | `wacholder` (Ersatz dwarf_pine, sea_buckthorn) | offen |
| **Ginster** (Ulex europaeus/Cytisus, gelb blühend 1–2 m) | kein Treffer; Megascans „Gorse“ bei Erscheinen prüfen | High | `wacholder`-Palette heide, Farbakzent gelb (Skellige-Frühling) | offen |
| **Wollgras** (Eriophorum) | Quixel Megascans **„Cotton Grass“** auf Fab, ab 3,99 USD **[Suchauszug: fab.com Seller Quixel Megascans]** | High | `wollgras` (Ersatz Tundra_Grass hoch skaliert) – weißer Moor-Akzent | **kaufen** (Lizenz im Fab-Konto prüfen) |
| **Moorbirke** (Betula pubescens, 6–12 m, mehrstämmig, Nanite) | Fab „Birch tree Nanite“ Drittanbieter; Megascans Trees „Silver Birch“ bei Erscheinen | High | `moorbirke` (Ersatz Big_Tree_birch_01 ohne Nanite, 28 k Dreiecke) | offen |
| **Flechtensteine** (Granit 0,3–1,5 m, ohne Moos) | nur LichenedForestBoulder_01 vorhanden; Fab „lichen rock“ prüfen | High | `flechtenstein`, `findling_frei`; bis dahin Flechten über `M_EL_Fels_Auflage` | offen (Material reicht vorerst) |
| **Trockensteinmauer-Segmente** (2–4 m, Ecke, Ende, verfallen) | Fab-Suche „dry stone wall sheepfold“ ohne Treffer; gefunden nur Ziegel-/Fachwerk-Kits (Massive Realities) und dekogon „Fences VOL.3“ (Nanite-Zäune) **[Suchauszug]** | High, Nanite | `mauer`, `pferch`; heute Einzelsteine (7 je 3 m, teuer) | **offen**, zweitwichtigste Lücke |
| **Schäfer-/Torfhütte, Jagdunterstand** | kein Netz im Inventar (Village/Town-Kits haben nur Dorfhäuser); Fab „shepherd hut medieval“ prüfen | High | `huette` (Spuren-Override) | offen, Ersatz Holzstapel + Pfähle + Karren |
| **Zwergbirke / Weidengebüsch 0,3–1 m** (Taxonomie-Lücke tundra) | Megascans „Dwarf Willow“/„Arctic Willow“ prüfen | High | `jungwuchs`-Palette tundra (Ersatz grey_willow, Forest_pine_plant) | offen |
| **Torfsoden-Stapel, Torfstich-Decal** | kein Treffer; eigenes Netz (Quader 0,3 × 0,15 × 0,1 m, Stapel) + Decal | – | `torfstich` | eigenbau |

Kostenhinweis aus `boden-kleinzeug-gras.md`: Megascans-Assets sind seit 2025 je Asset kostenpflichtig, sofern nicht vor dem
31.12.2024 beansprucht; Fab-Konto zuerst prüfen.

## 6. Offene Punkte und Annahmen

1. **Baumgrenze 300 m** ist aus D2-Lagenanteilen (Schnee 9 %) abgeleitet, nicht aus einem Klimamodell; wenn Ferat auf E2/C2 Bäume bis
   350 m will, `hoehe.tundra.baumgrenze_m` und `strauchgrenze_m` anheben. Heide-Profil hat keine Höhenstufe (Felder < 110 m).
2. **Profil-Zuordnung über Lagen** (Heide ≥ 40 % → heide, Trockengras ≥ 50 % über 120 m → tundra) kann in C2/D1/E1 (Heide 4–10 %)
   kleine Heideinseln erzeugen; wenn unerwünscht, `lagen_biom_hinweis` leeren.
3. **Überschneidung mit der Mittelschicht (Teil D)**: beide Planer setzen Zwergstrauch und Grasbüschel in heide/tundra. Entscheidung
   nötig (Vorschlag §3: in den zehn Feldern nur `heide_tundra`, Mittelschicht-Biomfaktor heide/tundra = 0).
4. **Witcher-Ebene / `instanzen.json`**: Bäume werden nur am Namen bzw. an `rolle`/`klasse` erkannt (pine, beech, birch …);
   für `instanzen.json` ist der Dateiname `datei` oder `<name>.f32` angenommen.
5. **Netze in zwei Klassen** (driftwood/dead_log in `totholz` mit und `treibholz` ohne Kollision; Tundra_Grass VarC/G und
   grass_meadow_08 in `grasbueschel` und `wollgras`): Setzer übernimmt die Einstellungen der ersten Klasse – also Kollision für alles
   Treibholz (6 Instanzen, unerheblich) und Sichtweite 10 000 für Wollgras. Bei Bedarf eigene Wollgras-Netze nach dem Kauf.
6. **Eingraben nach Netzhöhe** (Flechtensteine 38 %, Kiesel 40 %, Totholz 28 %) setzt Pivot in Netzmitte voraus; `netze_masse.json`
   hat für die Mountain-/Meadow-Steine Bounds – nach dem ersten Setzen prüfen, ob Steine schweben oder versinken, dann
   `eingraben_anteil` anpassen.
7. **Wüstenfelder C3/D3/E3**: nur tundra/heide-Zellen; die aue-Anteile in C3 bleiben dem Aue-Planer (dort ×0,6). Der eigene Wüsten-
   Planer bleibt unberührt (kein `entfernen`, auch nicht per `--entfernen`).
8. **Dichten sind Richtwerte** (keine Quelle nennt Instanzen je m²). Erster Kalibrierschritt: G5 und D2 setzen, Kameras 1 und 3,
   `--faktor 0.7 … 1.3` vergleichen; G5 läuft heute ins Budget (69 700 → 45 000), d. h. Kiesel werden auf 25 % gekürzt – wenn mehr
   Heidekraut gewünscht ist, `budget.ziel_instanzen_je_feld` auf 55 000 setzen.
9. **Rauchtest-Grenzen**: synthetisches Rauschen ohne echte Grate/Blockfelder, keine `witcher/`-Rollen, keine `instanzen.json`,
    Sand-Sperre nur ohne Sandlage durchlaufen. Erstes Echtdaten-Feld daher G5 (flach, Heide) neben D2 (Höhenstufen, Wind).
10. **Status-Datei** `verteilung-STATUS.md` wurde nicht verändert (Koordinator); B3 kann auf „fertig (ungetestet mit Echtdaten)“ gesetzt werden.
