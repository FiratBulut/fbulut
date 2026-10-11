# Antwort auf Auftrag 13b – Ferats Downloads, neuer Bestand

Stand 11.10.2026, nachmittags · Download-Liste: `antworten/sehens-downloadliste.md` + `antworten/sehens/downloadliste.json`

## Kurzfazit

- **Übernommen.** Das neue Inventar ist die Grundlage für die Planung: `netze.csv` mit 1 692 Netzen, `inventar_extra.json` mit
  73 Niagara-Systemen, 44 Decals, 316 Klängen und 46 Cues.
- **Download-Liste neu.** Sie hat jetzt die Abschnitte „Erledigt / im Projekt“ (8 Pakete mit echtem Pfad und Netzzahl), „Läuft bei Ferat /
  wird geladen / Import ausstehend“ (7), „Erneut versuchen“ (2 Asset-IDs) und die noch fehlenden Pakete: A 1, B 14, C 12.
  A + B sind etwa 20,5 GB, soweit eine Größe bekannt ist. Preise bleiben ungeprüft, weil fab.com aus der Cloud nicht erreichbar ist.
- **Die nächsten 5:** Electric Dreams (kostenlos), Nanite Driftwood Props, Quercus Robur (Stieleiche), Forest Fungi, CryoGen.
- **Kataloge und Asset-Bedarf** der 8 Biome aus der ersten Welle (aue, bergwald, lava, elfenwald, dschungel, gletscher, frost, fjord)
  sind mit dem Inventar abgeglichen. Je Ort stehen dort vorhandene Netze, Niagara-Systeme und Klänge mit echtem Pfad, dazu der Paketstatus.
- **Achtung Lava:** `SM_lava_wall_01–09` fehlen im neuen `netze.csv`. Bitte beim Nachladen von Lava & Volcano mitnehmen. Bis dahin planen
  die Lava-Orte mit Ersatz aus `/Game/Basalt`.
- **Phase 2** (Planer-Skripte) beginnt mit diesem Inventar, sobald alle 15 Biome in Phase 1 stehen.

## Was übernommen wurde

| Neu im Projekt | Pfad | Netze laut `netze.csv` | Eingeplant für |
|---|---|---|---|
| Basalt Columns and Rocks (gekauft) | `/Game/Basalt/meshes/*` | 22, **kein Nanite** | lava_07 Basaltorgel (Held); Ersatz für `SM_lava_wall_*` in lava_01, _04, _05, _08; Sockel des Mönchs (bergwald_01) |
| Megascans Eis/Schnee | `/Game/Fab/Megascans/3D/Ice_Cliff_*`, `Large_Ice_Cliff_*`, `Snow_Embankment_*`, `Snow_Pile_*`, `Rocky_Snow_Pile_*`, `Snowy_Rocks_Pile_*`, `Huge_Snow_Hill_*` | **31** (13b nennt 32) | gletscher_01, _02, _03, _04, _05, _07; frost_01–_06, _08; fjord_04 |
| Megascans Seerose | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/*` | 7 | aue_06 Mondarm (Held), dschungel_05 (optional), sumpf |
| Sumpfzypresse | `/Game/Downloads/SwampCypress/StaticMeshes/SM_SwampCypress_A` | 1 (nur Wurzelstock) | sumpf; ganze Bäume fehlen → Kandidat in B |
| Megascans Limestone Rocks | `/Game/Fab/Megascans/3D/Limestone_Rocks_ubqwdheda/…/Limestone_Rocks_ubqwdheda_High` | 1 (0,6 × 0,65 × 0,09 m) | Kalkschutt in aue_07, dschungel_01, _03, _05, _06 – kein Karst |
| Niagara Examples Pack | `/Game/NiagaraExamples/*` | 75 Netze, 59 Systeme | `NS_Smoke_Plume`, `NS_Chimney_Smoke` (lava_02, _06), `NS_Spark_Continuous` (lava_08), Gischt-Vorlage (bergwald_05, dschungel_02, fjord_02, _07); Nebel nur als Blueprints `BP_FogBankCard`/`BP_FogBankVolume` |
| Free Niagara Particles | `/Game/FreeParticle_SoftTofu/Niagara/*` | 14 Systeme | `NS_Sparkling_Glow`/`_Noise`/`NS_Sparkling` (elfenwald_01, _06, _07; aue_02; frost_04), `NS_leaf` (elfenwald_03, aue_08, bergwald_07), `NS_feather` (aue_03) |
| Free City & Nature Sounds | `/Game/City_Nature_Sounds/WAV/*`, `/CUE/*` | 46 Cues | `CUE_Water_Stream_I–X`, `CUE_Wind_Autumn_wind_with_leaves_rustling_Cue`, `CUE_Rain_Dropping_on_various_textures_Cue` (Tropfen, prüfen), `CUE_Nature_Birds_…_lovebirds_Cue` (nur Dschungel) |

Weiter sind neu im Inventar, ohne eigenen Download-Wunsch: 15 Spline-Klippen `SM_LS_beach_cliff_*`/`SM_LS_beach_escarpment_*` aus
Coast & Dunes (als Lehmwand für aue_03 und als Terrassenkanten für fjord_08 eingeplant). Aus Mountain kamen kurze Stammstücke
`SM_Forest_pine_04_01/02/03_log` (bergwald_03, _07), Fische `SM_Fish_Trout`/`SM_Fish_Perch` (klare Gewässer, optional) und `SM_Anthill` (bergwald_08).

## Neuer Stand der Download-Liste

**Raus (erledigt):** die 8 Pakete der Tabelle oben.

**Raus (gestrichen):**
- Forest Cretaceous: laut Ferat teuer und sehr schlecht bewertet; Riesenbäume bleiben Bestand plus Skalierung.
- Realistic Waterfall and Water VFX und Waterfall Pro: überflüssig, weil Nature Water FX gekauft ist.
- Realistic Starter VFX Pack Vol 2: Dampf kommt jetzt aus dem Niagara Examples Pack.

**Entfallene Wünsche:**
- gletscher: Der Atem, Gletschertisch, Büßereis, Schmelzsee
- fjord: Diamantstrand, Basalt-Blockufer
- dschungel: Tausendfuß
- lava: Regenbogenhang
- heide: Karrenfeld, Der Rachen, Moorauge
- tundra: Warme Quelle
- aue: Hexenring

**Läuft / wird geladen / Import ausstehend:**

| Paket | Status |
|---|---|
| Lava & Volcano | läuft bei Ferat (Effekte, Glut-Decals, Lava-Material; dazu bitte `SM_lava_wall_01–09`) |
| Coast & Dunes | läuft bei Ferat (Decals, Seetang, Stempel) |
| Mountain | läuft bei Ferat (Fluss-/Wasserfall-Material) |
| Megascans Desert Western Cliff Layered XL 14 + Large 03 | wird geladen |
| weitere Megascans-Limestone-Assets | wird geladen (große Kalkfelsen, Karst) |
| „Limestone Rock Set“ von Ancraite | wird geladen (kostenlos). Nur der Name: Einen Link konnte ich per Suche nicht belegen. |
| Nature Water FX | gekauft, Import ausstehend. Die echten Systemnamen folgen mit dem nächsten Inventar. Zugeordnet: kueste_08 Blasloch, kueste_04 Seefall, bergwald_05 Schleierfall, fjord_02 Schleierwand, frost_01 Eisfall und weitere Fälle. |

Mit den Limestone-Downloads ist die Lücke „Karsttürme“ voraussichtlich geschlossen.

**Erneut versuchen:** `61882812-0d2e-4b2a-a43b-9f2d019973a1` und `6676d940-e165-47b0-9471-50a68115315c`. Beide lassen sich aus unserer
Liste nicht eindeutig einem Paket zuordnen, weil die Liste Listing-IDs führt und keine Asset-IDs.

**Was bleibt, neu priorisiert:**

| Prio | Pakete |
|---|---|
| A (1) | Nanite Driftwood Props (Held von aue_04) |
| B (14) | Electric Dreams (kostenlos); Quercus Robur (neu, 13c); Forest Fungi; CryoGen (C → B); Arctic Cliffs; Cave Ambience; Cave Stalactites & Wall Kit (neu); Nanite Tropical Plant Pack 2 (neu); Travertine Terraces; Ultimate Niagara Environmental VFX; Fantasy Ambiences; Brushify Moorlands (neu, B5); Taxodium Distichum (Bald Cypress) Tree Pack (neu, ganze Sumpfzypressen); Megascans Trees: European Black Alder (bleibt B laut B8, nicht abwarten) |
| C (12) | Icelandic Sand, tote Stieleiche, Tundra Icelandic Rock Cluster, Moss & Lichen (B5), Niagara VFX Pack Snow (B → C, nur noch Schnee), Giant Fantasy Mushrooms, Hollowstone, Wadi Rum, Procedural Rocks Generator, Tropical Vegetation, Rain Forest Pack, Wilderness Nature Loops |

**Top 5 der noch fehlenden Pakete:**

1. **Electric Dreams Environment** – kostenlos; tropische Uferpflanzen und Luftwurzeln für dschungel_04 und _07.
2. **Nanite Driftwood Props** – die Treibholzburg ist der Held des Leuchtfeuers aue_04. Im Bestand gibt es nur ein Treibholz von 3,6 m.
3. **Quercus Robur (Stieleiche)** – für Die Alte (aue_02). Bis dahin steht dort die Schwarzpappel ×1,3.
4. **Forest Fungi – Mushroom Pack** (ca. 18 €, ungeprüft) – Pilze für 7 Orte in aue, bergwald und elfenwald.
5. **CryoGen** – Eissäulen, Zapfenvorhang, Eisglocken und Frostblumen für 4 Frost-Orte.

**Lücken ohne Paket** (Tabelle in der Download-Liste):
- Raureif-Bäume: `MI_EL_SW_Raureif` auf den Bestandskiefern.
- Ganze Sumpfzypressen: Bald Cypress Pack (B) als Kandidat.
- Ginster, Wacholder, Wollgras: Ersatz aus Sanddorn, gestauchten Jungkiefern und Binsen (B5).
- Kein Brandungs- und kein Seevogelklang im Bestand (B8).
- Kein Nebel-, Schnee- oder Tropfen-Niagara im Bestand.
- Lavaröhre, Felsnadel und Riesenbäume entstehen aus Bestand plus Gelände und Skalierung.

## Hinweise zu den neuen Netzen

- **Maßstab:**
  - Basalt-Säulen sind klein: 0,29 m Querschnitt, 0,15–2,6 m hoch.
  - `Basalt_Basalt_Cliff_SM` misst 8,6 × 5,3 × 6,0 m.
  - Das größte Eis ist 6,7 × 1,7 × 6,2 m (`uhprdg2fa_tier_0`), der größte Schnee 15,2 × 7,4 × 1,8 m (`vdspdazqa_tier_0`).
  - Seerosen messen 1,2–1,7 m je Gruppe; Limestone ist nur ein flacher Haufen von 0,6 m.
- **Skalierung:**
  - Basaltorgel und Basaltburgen: Gruppen mit ×3–8. Die Säulen werden damit 0,9–2,3 m dick, `Pillar_D` wird bis 21 m lang.
  - Séracwand: ×2,5–4. Riesenseerosen: ×2,5–4.
  - Basalt ist **nicht Nanite**. Deshalb lieber wenige große Akteure setzen und das Budget (≤ 80 Akteure je Ort) beachten.
- **Material M_MS_Base_Trm:**
  - Die Megascans-Eisnetze bringen ein Material mit Durchscheinen mit.
  - Bitte beim Material-Fix für die Ebenen `sw_*` nicht auf `M_EL_Fels_MS` umstellen, sonst geht das Durchscheinen verloren.
  - Unsere Eis-Instanzen (`MI_EL_SW_Gletschereis_Tief`, `_Spritzeis`, `_Schwarzeis`) auf `M_EL_Eis4` gelten weiter nur für Eiszapfen und Flächen.
- **Basalt-Material:**
  - Falls eine Instanz auf `M_EL_Klippe_RVT` nötig ist (`MI_EL_SW_Basalt_Saeule`, `MI_EL_SW_Granit_Moos` für den Mönch-Sockel), bitte die
    Basalt-Texturen in die Instanz übernehmen. Sonst zeigt sie die Textur der Nordklippe.
- **Niagara:**
  - Alle Effekte sind optional (≤ 3 je Ort).
  - „Kopie“ heißt: das System duplizieren und dann Farbe und Größe ändern, z. B. rotes Laub aus `NS_leaf` oder grünliche Sporen aus
    `NS_Sparkling_Glow`.
  - Kampf- und Spieleffekte nutzen wir nicht: Waffen, Explosionen, Pickups, Teleport, `NS_Sparkling_Heart/_Skull/_Note/_Star/_Moon`.

## Credits

**Free Niagara Particles** steht unter **CC BY 4.0** → Namensnennung **„SoftTofuVFX“** in den Credits des Spiels, z. B. „Partikeleffekte:
Free Niagara Particles von SoftTofuVFX, lizenziert unter CC BY 4.0“. Eingesetzt wird es in elfenwald, aue, bergwald, frost und sumpf.

## Phase 2

Phase 2 (Planer-Skripte `skripte/sehens_<biom>/`) beginnt **mit diesem Inventar, sobald alle 15 Biome in Phase 1 stehen**.
Netze aus den laufenden Nachladungen (Lava & Volcano, Coast & Dunes, Mountain, Limestone, Desert Western Cliff, Nature Water FX) setzen
die Planer mit Ersatz aus dem Bestand ein (SEHENS_FORMAT §4). Nach dem Inventar 13d wird der Ersatz gegen die echten Netze getauscht.

## Geänderte Dateien

- `antworten/sehens-downloadliste.md`, `antworten/sehens/downloadliste.json`
- `antworten/sehens/{aue,bergwald,lava,elfenwald,dschungel,gletscher,frost,fjord}/asset_bedarf.json`: neuer Block `abgleich_13b_13c`
  (vorhanden je Ort mit Pfad und Maßen, Paketstatus, Entscheidungen, was weiter fehlt); `status_13b` an jedem Paketwunsch; Materialwünsche ≤ 6
- `antworten/sehens/<dieselben 8>/katalog.md`: Abschnitt „Abgleich mit Inventar 13b und Entscheidungen 13c“
- `antworten/sehens/aue/decal_brutroehren.png`, `decal_brutroehren_n.png` (siehe 13c-Antwort)
