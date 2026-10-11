# Asset-Paket-Recherche für Eldarien (Stand 10.10.2026)

(Hilfsagent „Cloud: Fab-Pakete bewerten“, fertig 10.10. 00:20. Von Claude gesichert. Bilder hat der Agent NICHT gesehen – vor Nutzung Bild-Check.)

**Methode / Grenzen.** Fab-Produktseiten direkt gelesen, Fab-Suche und Verkäuferseiten ausgewertet, Web-Suche für Hintergründe. Anbieter-Zuordnung über die
Ordner im Projekt (`Content\<Paket>`, Asset-Namen) – die Paketordner enthalten nach der Löschaktion vom 07.10. teils nur Reste (z. B. `SoulCave` 2 Dateien,
`PBR_Graveyard_and_Landscape` 0, `Nature_Set` 44). Preise = CHF im Schweizer Fab-Shop am 10.10.2026, „Kostenlos“ = Stand heute. Links: `https://www.fab.com/listings/<ID>`.

Unsicher zugeordnet (Fab-Bibliothek im Launcher nachsehen): `Mountain_Shrine`, `AncientRuins`, `MedievalCastle`, `Town`, `Singapore_Canal`, `SmartAssets`, `MuddyGroundPack`.

## 1) Tabelle je Paket

### A. NatureManufacture (Verkäufer https://www.fab.com/sellers/NatureManufacture; Standardlizenz, Updates Juni 2026 außer Ground Packs/Nature Set)

| Paket (Ordner) | Fab-Listing / Preis / Bewertung | Inhalt laut Fab | UE / Nanite | Qualität | Einsatz in Eldarien (konkrete Assets im Projekt) |
|---|---|---|---|---|---|
| **Coast_Dunes_Environment_Set** (455) | `15697157-fccc-45dc-8e23-2897ece19c99` · 80,89 CHF · 4,8 (11) · 07/2025 | 100 % Scans, 4096²: 42 Büsche (Strandrose, Sanddorn), 36 Gräser/Blumen, 9 Eichen, 17 Strandkiefern, **17 gekachelte Spline-Klippen**, **14 Decals (Nassufer, Lehm, Fels, Kiesel, Sand)**, **9 Treibholz**, Zäune, Seepfähle, Flächen-Netze Fels/Lehm, 10 Wurzeln, Seetang/Muscheln, **85 Bodentexturen in 28 Sets**, 20 Stempel, Meer-/Fluss-Material, 1×1 km Demo | **5.5–5.8**; Nanite-Landschaftsmaterial, RVT-Blend; braucht Water-Plugin + Mesh Distance Fields | hoch | **Fjord/Küste** (Spline-Klippen), **Ufer/Kies aller Flüsse** (Decals Kiesel/Nassufer, Flächen-Netze, Bodensets Kiesel/Lehm/Steine), **Totholz** (`FT_SM_beach_driftwood_01…09`), **Heide** (`FT_SM_sea_buckthorn_03`, `FT_SM_beach_rose_06`, `FT_SM_dry_oak_02_A`, `FT_SM_kidney_vetch_01`, `FT_SM_sea_holly_05`), **Küstenkiefern** (`FT_SM_pine_beach_02_A`, `…medium_03`, `…small_04`), Dünen-Stempel. **Ungenutzt – größter Hebel für „Ufer/Flussbett“.** |
| **Forest_Environment_Set** (291) | `11479aa9-a0bb-4292-80b7-1033c48df94c` · 58,41 CHF · 4,5 (32) · 11/2019 | Buchen (Pflanze bis tot), Schwarzkirsche, **Totholz-Stämme**, **alte Wurzeln**, **3D-Laubdetails**, Pilze, Gräser, Holzbau (Brücken), Fels-/Wurzel-BPs mit Moos-Auflage, Sumpf-Wasser | 4.21–5.8; Nanite-Landschaft + RVT ab 5.6 | hoch | **Elfenwald**: `SM_beech_tree_00_C…08`, `SM_black_cherry_03`; **Totholz**: `SM_dead_log_03`, `SM_beech_old_roots_01`; **Boden-Nahdetail**: `SM_detail_leaves_02`, Pilze; Unterwuchs `SM_grass_01_2`, `MI_plant_02`. **Ungenutzt.** |
| **Environment_Set** (251) | `7861982c-92d2-43df-a75d-c07a7cee8b24` · 58,41 CHF · 4,8 (295) · 12/2017 | 8 Tannen, 7 Pappeln, 12 Felsen, **26 Gräser/Kräuter**, **47 Bodenmaterialien** (Laub, Streu, Kiesel, Wurzeln, Nassboden …), Stämme, Wurzeln | 4.16–5.8 | gut (älter) | **Bergwald** (`MI_Bark_Fir_01…05`, `MI_Imposter_Fir_01…08`), Aue (Pappeln), Unterwuchs `SM_fern_01_1`, `SM_nettle_01_0`, `SM_grass_bush_04`, `SM_ground_foliage_01_flowery`, `SM_crooked_root_01`; 47 Bodentexturen als Lagen/Decals. **Ungenutzt.** |
| **Mountain_Environment_Set** (347) | `9ec7df30-3347-4056-8933-6156d983b0cf` · 80,89 CHF · 4,7 (32) · 01/2022 | **448 Meshes/BPs**: Kiefern, Latschen, Felsen/Felswände, Äste, Pilze, Wurzeln, Zapfen; Fluss-Material mit **Auto-Wasserfällen**; Straßen-/Fluss-Splines; **Hintergrund-Gebirge** | 4.21–5.8; Nanite + RVT ab 5.5 | hoch | **Bergwald**: `SM_Forest_pine_02/08`, `SM_dwarf_pine_big_02` (Baumgrenze/Frost); **Felswände** `SM_big_rock_wall_02`, `SM_flat_rock_03`, `MI_mountain_rocks_big_01`; Kleinzeug `SM_Pine_broken_branch_01`, Zapfen; **Berge-Fernansicht** `Background_Terrains`; `BP_Sviatovid_Stone` (Heiden-Idol). Teilweise genutzt. |
| **Meadow_Environment_Set** (311) | `4f61d2d7-8d6f-4817-890d-17a6ba2287af` · 58,41 CHF · 4,8 (108) · 03/2019 | **31 Gras-/Blumentypen**, 8 Büsche, 11 Bäume, **24 Klippen + 20 Felsen**, Sumpf-Material, 9 Bodensets, **Zaunsystem** | 4.21–5.8 | hoch | **Aue/Wiese** (`SM_flower_common_poppy_01`, `SM_flower_brownray_knapweed_02`, `SM_flower_common_chicory_01`), Heide (`SM_dead_grass_01`), `BP_Tree_Stump_Group`, `SM_Rock_04`, Zäune. Genutzt. |
| **Lava_Volcano_Environment_Set** (95) | `154cf0a8-207c-4c5d-a667-60e80e32cfe1` · 53,92 CHF · 5,0 (2) · 10/2025 | 20 Felsen, 9 Klippen (**Nanite**), Lava-Flüsse/-Seen (Water-Plugin, Flowmaps, RVT-Hitze), **20 Bodensets inkl. Schnee**, 20 Niagara-Effekte, 7 Decals, **5 Hintergrund-Berge**, 9 Stempel | **5.6–5.8**; braucht Water + Water Extras + Water Advanced | hoch | **Lava/Ödland** komplett: `SM_lava_wall_02…09`, `SM_lava_b_rock_01`, `SM_lava_m_rock_04`, `SM_lava_s_rock_03`, `T_lava_sand_04`, `MI_Lava_rocks_set_01`; Hintergrund-Berge auch für andere Biome. Kaum genutzt. |
| **Nature_Set** (44) | `dbc82b39-0bb2-4abb-ab8e-777da1ed457e` · 35,94 CHF · 5,0 (11) · 12/2016 | Birken/Weiden, Felsen, Gras, Bodenmaterialien | 4.14–**5.4** | gut, älter | Aue (`Big_Tree_willow_01/02`), Elfenwald (`Big_Tree_birch_01`). Genutzt. |
| **Graveyard** (62) + **PBR_Graveyard_and_Landscape** (0) | „Graveyard and Nature Set“ `4a5d66cf-c189-43a4-8db9-577135653a4a` · 17,96 CHF · 3,9 (40) · 07/2016 | 762 Assets: Friedhof, Kirche, **tote Bäume**, Büsche, Wurzeln, Felsen | 4.15–5.8 | mittel | Totholz `SM_Dead_Tree_01…03`, Kirche `M_Church_sandstone_01/02`, Moosmauern `M_Mixed_stone_wall_04_moss`, Brombeere/Wildrose. |
| **LandscapeGroundPack** (8) | `3e29a433-fea1-47b9-8b60-f55563b14aa8` · 13,46 CHF · 4,4 (22) | 105 Bodentexturen 2048² | 4.10–**5.4** | mittel (2K) | nur `GroundTexture_18/21` übrig; Tessellation in UE5 tot → nur Texturen. |
| **WinterGroundPack** (8) | `007ee5eb-a8d6-4a87-9098-fe3d5c8a1cc2` · 4,47 CHF · 4,2 (23) | 15 Materialien Schnee/Schlamm/Fels | 4.10–**5.4** | mittel | Gletscher/Frost: `Snow_Ground_Texture_1/3/5/10`. |
| **Ice_World** (8) | `69196d08-bcaf-4be0-a22f-64dbcf1a3544` · 17,96 CHF · 4,2 (13) · 07/2017 | Eis-Shader: Tiefe (Parallax), Blend, Transparenz, Anti-Kachel | 4.14–5.8 | gut (Shader) | **Frostsee/Gletscher**: `T_cracked_ice_deep_G`, `T_cracked_ice_shallow_blue_BC` → offener Punkt „Eis Frostsee“. |

### B. Hivemind (https://www.fab.com/sellers/Hivemind; gescannte Pflanzen + Nebel-VFX, `M_Basic_PBR`)

| Paket | Fab-Listing | Inhalt | UE / Nanite | Qualität | Einsatz |
|---|---|---|---|---|---|
| **HauntedVillage** (202) | „Modular Haunted Village“ `ef13e86e-83bb-4e7b-988d-8bed08791018` · 53,92 CHF · 5,0 (13) · 11/2024 | modulares Spukdorf, begehbare Häuser, Props, **gescannte Pflanzen + Schutt**, Windmühle, Nebel-VFX, PCG | **5.3–5.8**, Lumen + Nanite | hoch | Dark-Fantasy-Dörfer/Ruinen (Städte), `Scanned_Foliage` + `PCG` als Unterwuchs/Schutt; Nebelkarten für Talnebel. |
| **Hivemind/Medieval_Docks** (37) | „Modular Medieval Town, Docks“ `9bec871e-2d9b-4261-aa26-868d4300f81a` · 71,90 CHF · 4,9 (26) · 05/2024 | **323 Meshes**, Häuser, Hafen, **Nanite-Pflanzen**, VFX; braucht Water, Landmass | 5.3–5.8 | hoch | Fjord-/Küstenhafen, Flussdörfer; `SM_EagleFern_S_04`, `MI_EagleFern_Atlas_01`, `SM_MossClump_04`. |
| **Town** (49) | Hivemind, unklar welches: „Townsmith“ `7cdd67b0-ff96-403b-afbf-54542f562357`, „Modular Medieval Town“ `2b1bca91-ece3-4f33-8f7d-9639ab5d4323`, „Stylized Town“ `4121695a-563b-488b-911d-2a3fbda98634` | Reste: Heuballen, Laterne, Zäune | 5.x | – | Dorf-Kleinzeug `BP_HayBales`, `SM_Hay_Pile`, `SM_Lamp`, `SM_Fence_01/03`. |

### C. Meshingun Studio (https://www.fab.com/sellers/Meshingun%20Studio)

| Paket | Fab-Listing | Inhalt | UE / Nanite | Qualität | Einsatz |
|---|---|---|---|---|---|
| **Bazaar_Meshingun** (109) | „The Bazaar“ `cff79d2c-4b55-45a2-80fc-960193a6dfd4` · 85,38 CHF · 4,6 (58) | 250+ Assets, 40 Prefabs, Trimsheets, Palmen, Sandsturm | 4.24–5.8; Nanite + Lumen | hoch | **Wüste/Canyon**: Oasenstadt (Städte), Palmen `T_Tree_Palm_Fo_M`. |
| **Village** (168) | „Medieval Village Megapack“ `e49a4e1a-63a4-4472-9026-8c2339164c29` · 161,80 CHF · 4,6 (23) | **550+ Assets**, 100 Prefabs, Wetterwerkzeug; Nanite kompatibel, **aber aus** (Vertex-Paint) | 4.24–5.8 | hoch | Dörfer gemäßigter Biome; `BP_Carriage_01a`, `SM_Wheel_01b`, Regen-Texturen. |
| **AsianTemple** (100) | „Asian Temple Pack“ `db0d10ca-2b9e-4027-bc27-5cd845f12602` · 62,91 CHF · 4,5 (13) · 07/2021 | Bäume, Klippen, Ranken + Architektur | 4.24–5.8 | gut | **Dschungel/Karst**: `SM_Cliff_01a`, `SM_Tree_Big_01a`, Farne `MI_Fren_01a/02a`, `T_Moss_ORM`. Genutzt. |
| **FeudalJapan_Meshingun** (nicht installiert) | `80c4ae6f-b612-4d5b-86b4-d8fec433d469` · 179,78 CHF · 4,6 (33) | 400+ Assets, Bambus, Kirsche | 5.1–5.8 | hoch | Dschungel-Vegetation (Bambus); sonst fremd. |
| **Gothic_Interior** (nicht installiert) | `c856b256-c060-4337-8156-8b604ce0cadd` · 224,72 CHF · 4,9 (27) | Innenräume | 4.24–5.8 | sehr hoch | für die Landschaft wertlos. |

### D. Übrige Pakete

| Paket | Anbieter / Fab-Listing | Inhalt | UE / Nanite | Qualität | Einsatz |
|---|---|---|---|---|---|
| **Megascans** (956) | Quixel: 57 3D-Assets, 41 Pflanzen, 12 Surfaces, 15 Decals | u. a. `WoodenSticksAndTwigs`, `DryBranches`, `SmallStonesPack`, `DeadLeaves`, `ForestRoots`, `MossyForestBoulder`, `HugeNordicCoastalCliff`, `MassiveTundraRockFormation`, `CanyonSandstoneRidge`, `DryRiverBed`, `NordicBeachRocks`, `BeachSandWithPebbles`; Surfaces `NordicMoss`, `MossyRockyGround`, `SwampWater`, `BeachCliff`; Decals `ScatteredSticksAndTwigs`, `TileableMossPatches`, `ScatteredBark` | Nanite | sehr hoch | Grundstock. **Boden-Kleinzeug (3D-Zweige/Steine/Laub) liegt schon im Projekt** – Lücke ist die Verteilung (PCG/Foliage). Pflanzen überwiegend tropisch → Dschungel. |
| **Megaplant_Library** (117; 13 Arten: Bilberry, Bulrush, Stinging Nettle, Wood Anemone, Heather, Elder, English Oak, European Aspen, European Beech, Goat Willow, Japanese Medlar, Rowan, Silver Birch) | Quixel Megaplants, **kostenlos**, https://www.fab.com/sellers/Quixel%20Megaplants (37 Produkte) | PVE-Preset, `SKM_Branch_*`, `SKM_Twig_*_Dead_*`; **Nanite-Foliage + Dynamic Wind** | **5.7–5.8**; Plugin „Procedural Vegetation Editor“ + „Nanite Foliage (Experimental)“ | sehr hoch | alle gemäßigten Biome; tote Zweige als Totholz. **Experimental – Epic rät vom Ausliefern ab.** |
| **Namaqualand** (326) | Poly Haven `295ed897-fe78-4711-a583-d9b80fde554a` · kostenlos, **CC BY 4.0** · 5,0 (40) | 14 Pflanzen, 18 Felsen, HDRIs; Nanite, Impostors | 5.4 (läuft in 5.8) | sehr hoch | Wüste/Canyon (genutzt). **Credits: „Poly Haven“.** |
| **AncientContent** = Valley of the Ancient (97) | Epic `0c19880e-21bd-42ba-8287-1caccc3951b1` · kostenlos | 2×2 km Megascans; **205 GB**; UE-only | 5.0–5.7 | sehr hoch | `SM_IcelandicBoulder_02`, `T_IcelandicLavaSpire_A_02`, `SM_RockSandstone_021`, `SM_ToadRush_012`, `MI_LimestoneRocks3`. |
| **Electric Dreams Sample** | Epic `d79688f5-29be-4fb2-a650-2d4a813f5306` · kostenlos | 7 PCG-Beispiellevel | 5.2–5.8; UE-only | sehr hoch | PCG-Vorlagen für H3; Hainbuche/Farne/Totholz übernommen. |
| **SoulCave** (2) | Epic „Soul: Cave“ `75f42402-40bb-4a1b-b557-18e2c9604273` · kostenlos | Mobile-Qualität 2014 | – | niedrig | eher nicht. |
| **CityPark** (26) | SilverTm `11cc2abb-126c-4452-9fe4-6f2381d96544` · kostenlos · 4,5 (244) | 500+ Meshes | 4.24–5.7 | mittel | Wasserpflanzen `SM_WaterPlant01…04` (Teiche/Sumpf), Brunnen. |
| **Palms_Pack_01** (173) | Open World Development `9f81069d-877c-4d4e-aa28-30f5d1a8d8c9` · 17,96 CHF · 5,0 (3) | 12 Hanfpalmen `SM_Palm_01_01…12_G`, Impostors | 4.24–5.8 | gut | Dschungel/Karst. Ungenutzt. |
| **MedievalFantasyVillage** (57) | LAYA DESIGN `b8d49812-57f8-4e6e-bf95-aa5696efc25f` · 44,03 CHF · 5,0 (4) · 02/2026 | 52 Meshes, Procedural Foliage, RVT, Rotbuchen | 5.1–5.8 | gut | Totholz `SM_EuropeanBeech_Dead_M_01`, `…_XL_01`; Zäune, Karren. |
| **Mountain_Shrine** (19) | unsicher: YOS3D `7fdd9389-5d8b-483b-a9bd-424c221a3922` oder Hivemind „Mountain“ `05571320-3950-409f-a77f-e3ee4b36b5b5` | Laterne, Moos-Blend, Triplanar | – | – | `MI_Lantern_01`, `M_LayeredMaterial`/`ML_Base_Triplanar` (Moos/Erde-Auflage). |
| **AncientRuins** (36) | unsicher; Kandidat Sidearm „Ancient Ruins“ `27ab1216-d3d0-4b1b-b423-b589903ab857` · 17,96 CHF · 4,8 (14) | `SM_Column_02/03`, `SM_Main_Arch_01`, `SM_Wall_01/02`, Sand-Blend | – | mittel | Ruinen Elfenwald/Wüste. |
| **MedievalCastle** (33) | unsicher (Dexsoft `94b2c6c1-93a7-4291-9af9-ecc84884e751`?) | `SM_BrokenWoodWagon`, `SM_Cross` | – | – | Deko. |
| **RiverShader** (13) | SHADERSOURCE „River Buoyancy Tool“ `682b8592-3159-443a-87b3-9c843a910095` | UE4-only, Legacy | 4.16–4.27 | veraltet | **Nicht verwenden.** |
| **MuddyGroundPack** (4) | unklar; `T_MuddyGround_4K_*` | 1 Schlamm-Set 4K | – | – | Sumpf-Bodenlage. |
| **RothenburgBridge** (nicht installiert) | Pierogi3 „Medieval Stone Bridge – Nanite“ `4c64ce34-195b-4b45-8e14-70273cc984b5` · **kostenlos** · 06/2026 | 1 Steinbrücke, Nanite, Kollision | 5.7 | gut | **Brücken** (spätere Straßenphase). |
| **Realistic_Mossy_Rocky_Grass_PBR_Material** (nicht installiert) | AL-HADIDI `eb3390a8-0f58-4d74-844a-a47a2c16bd29` · kostenlos (Personal) · 08/2026 | Materialsatz bis 8K | 5.8 | gut | Bergwald/Heide-Bodenlage; gleicher Anbieter „Muddy Ground with Pebbles and Grass“ `93d594e8-99f2-4ec6-8980-6135929338d8` → Sumpf/Ufer. |
| **Singapore_Canal, SmartAssets** | nicht auffindbar | – | – | – | irrelevant. |

## 2) Rangliste: die 10 wertvollsten ungenutzten Pakete/Assets für die Witcher-Messlatte

1. **Coast & Dunes – Environment Set** (installiert, ungenutzt): Lücke „Ufer/Flussbett (Steine, Kies)“ + Fjord-Steilküste: 14 Ufer-Decals, Fels-/Lehm-Flächennetze, 17 Spline-Klippen, 9 Treibholzstämme, 85 Bodentexturen; 5.5–5.8, RVT-Blend.
2. **Forest – Environment Set**: Buchenwald mit Jung-/Alt-/Totbäumen, `SM_dead_log_*`, `SM_beech_old_roots_*`, 3D-Laub `SM_detail_leaves_*`, Pilze → Elfenwald, Totholz, Boden-Nahdetail.
3. **Environment Set**: 47 gescannte Bodenmaterialien + 26 Gräser/Kräuter + Tannen → Bodenschichten, Bergwald.
4. **Mountain – Environment Set, Restteile**: `Background_Terrains`, `SM_big_rock_wall_*`, Latschen, Äste/Zapfen, Fluss-Splines mit Auto-Wasserfällen.
5. **Quixel Megaplants** (13 Arten da, >20 weitere kostenlos: Norway Spruce, Baltic Pine, Dead Pine, Dry Common Reed, Lingonberry, Black Poplar …); Experimental.
6. **Lava & Volcano – Environment Set**: Nanite-Felsen/Klippen, Lavaflüsse über Epic-Wasser, 5 Hintergrund-Berge, 20 Bodensets inkl. Schnee → Lava-Wände.
7. **Hivemind Docks + Haunted Village**: beste Gebäude-Kits (Städte-Phase); gescannte Pflanzen und Nebel-VFX jetzt nutzbar.
8. **Asian Temple + Palms Pack 01**: einzige Dschungel-/Karst-Bausteine.
9. **Ice World + Winter Ground Pack** (+ kostenlose Megascans-Schnee-Meshes) → Gletscher/Frost, „Eis Frostsee“.
10. **Graveyard and Nature Set + Medieval Fantasy Village** → Totholz, Moosmauern, Brombeere/Wildrose, Zäune/Karren.

## 3) Lücken, die kein Paket deckt – kostenlose Empfehlungen (Fab, 10.10.2026)

**Lücken:** (a) Gletscher/Eis in 3D; (b) Sumpf (Schilf, Sumpfzypressen); (c) Karsttürme; (d) Berge mit Farbbändern; (e) Nadelwald-Bäume in Nanite; (f) Wiesenblumen-Vielfalt.

1. **Megascans Eis/Schnee:** „Ice Cliff“ `198d6561-73ca-4d4e-adc5-efe457f5c793` (auch `3697046b-9768-4bb6-a117-4dbc8a67eb61`, `339fd6af-6ca3-4f12-84e2-73e010f26360`), „Snow Pile“ `8e55612b-1f02-4262-aad4-f1a00dfa7c62`, „Snow Embankment“ `7b805548-e3d7-4cd5-a4ab-17f3ce2ec315`, „Snow Clump“ `7671b700-ce1a-4b49-9d1b-3add4a6a33c3`, „Rocky Snow Pile“ `0c6bddcc-8949-4e2d-bb42-0fb27c00121d`, „Huge Snow Hill“ `b77dce3d-44e8-4d32-9fc5-fe712db2f18c`.
2. **Megaplants Nadelbäume:** „Norway Spruce“ `f87364c9-10a2-4834-8566-a0291c717758`, „Baltic Pine“ `a2b04e81-5075-479f-a9d2-4940022f330a` (+ Saplings `ae732b47-14db-422e-b11d-c93537cb5165`), „Dead Pine“ `bc9e4e89-fcf4-4be6-b0f0-8b37395a72de` (5.7+, PVE, Experimental).
3. **Sumpf:** Megaplants „Dry Common Reed“ `00299cb6-8602-4736-8565-4b19b41f5686`; Project Nature „giant Reed“ `b4c4cc88-d228-4961-9c18-9aa9c0d1292c`; EntropyArchives „Swamp Cypress Roots – Nanite Ready (Free)“ `770f0ddb-2e52-4bd7-9fa8-deaf33466765`; Megascans „Rembrandt Water Lily“ `96391dd8-2556-47cf-a3ff-de5634adf19d`.
4. **Küste/Kies:** Poly Haven „Smuggler's Cove Asset Pack“ `a0935013-5959-47c2-97d9-75478ded0e6b` (CC BY 4.0): Küstenklippen `coastal_cliff_01…06_b`, `coast_rocks_01…04`, Sandmaterialien; ScanForge „stones field pebbles FREE“ `206322b8-5d13-4e5a-9151-8a876406019f`, „stone pebbles big“ `71158c92-e5c9-4892-8ad0-ec478b93e82a`; Megascans „Small Pebbles Ground“ `a0e6a70f-8d24-4481-af19-327f5e7e5bef`, „Icelandic Sand With Pebbles“ `43dee764-0072-448f-8c4d-9aff7d899445`.
5. **Boden-Kleinzeug & Farbbänder:** „Forest Floor Compost“ `176c6df3-f06b-47c8-b216-0416be280a0a`, „Forest Floor“ `dae56d09-862c-4f77-9e72-a41281c49633`, „Mossy Forest Floor“ `31b154e8-dea5-49c8-9b29-6362fe1a4a8d`, „Fallen Log“ `8c058dd2-d70a-4f3d-b797-bf4e80730ad5`, „Common Spruce Branch“ `10a2c302-4015-47d8-88f3-f457c3bc72c2`, „Birch Branch“ `9cc51395-bdd0-43d0-b4a8-3f491461dd79`, „Oak Tree Branch“ `c1994f5b-4d83-4909-846f-65d60c7c8f1e`; **Farbbänder**: „Desert Western Cliff Layered XL 14“ `23639c4c-ca70-49f1-b462-afaa454252b2`, „Desert Western Cliff Layered Large 03“ `b4a34fb2-7b1f-411b-be85-26b8735306c2`, „Nordic Coastal Cliff“ `f53f0b71-fd1e-4c8b-9e65-bda485469f86`; **Wiesenblumen**: Project Nature „Meadow Flowers“ `e648b1bd-11f6-4895-bd43-15e399c80297`, Megascans „Field Poppy“ `66cb2706-bc30-4f26-92ec-cad48723bd4a`; Nadelwald ohne Experimental: Project Nature „Spruce Forest“ `f8044501-17a2-498f-b198-5f1bc71ee87a` (bis 5.4 gelistet).

Karsttürme: kein kostenloser Treffer – nur eigene Kompositionen aus Megascans-Kalkstein (`Limestone Rocks` `796fb016-84b1-4920-82b1-ebde6dd40910`) oder Kaufpaket.

## 4) Lizenz und Nutzung in UE 5.8

- **Fab-Standardlizenz** (fab.com/eula): nicht-exklusiv; Inhalte dürfen verändert, in Projekte eingebaut und kommerziell vertrieben werden. Verboten: Inhalte einzeln weitergeben; Endnutzer am Herausziehen hindern; Projekte müssen Mehrwert bieten. Weitergabe nur an Mitarbeitende am selben Projekt. Keine Kombination mit GPL/LGPL/CC-BY-SA. Erworbene Inhalte bleiben unter den Kaufbedingungen.
- **Personal vs. Professional:** gleiche Rechte; Personal bis 100 000 USD Bruttoumsatz/12 Monate; kein Upgrade nötig bei späterem Überschreiten.
- **Epic-Inhalte mit UE-Bindung:** Valley of the Ancient, Electric Dreams („Use Only with Unreal Engine-based Products“) – für Eldarien unproblematisch, nichts in andere Engines exportieren.
- **CC BY 4.0:** Namaqualand und Smuggler's Cove → **Namensnennung „Poly Haven“ in den Credits**.
- **Megascans:** 2024 über Fab geholte Assets = Fab-Standardlizenz; über Bridge/Quixel.com = alte Epic-Content-Lizenz (nur UE). Megaplants kostenlos, aber Experimental.
- **Technik 5.8:** Pakete nur bis 5.4 gelistet (Nature Set, Ground Packs, Project Nature) über ältere Engine installieren und migrieren; deren Tessellation-Materialien funktionieren in UE5 nicht (nur Texturen übernehmen). River Buoyancy Tool nicht benutzen. Pflicht-Plugins: Coast & Dunes (Water, Mesh Distance Fields), Lava (Water, Water Extras, Water Advanced), Hivemind Docks (Water, Landmass), Hivemind Village (PCG, PCG External Data Interop, PCG Geometry Script Interop, Volumetrics, Virtual Textures). Valley of the Ancient braucht 205 GB.

**Nächster Schritt (Vorschlag des Agenten):** Coast & Dunes-Decals/Flächennetze und Forest-Set-Totholz/3D-Laub in kleinen Gruppen laden (Nanite-Bau im Hintergrund → Speicher), Bilder gegen die Witcher-Zielbilder prüfen; parallel die kostenlosen Megaplants-Nadelbäume und Megascans-Schnee/Eis-Meshes in die Fab-Bibliothek legen (Ferat muss sie im Launcher „Zur Bibliothek hinzufügen“).
