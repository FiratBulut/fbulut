# Antwort auf Auftrag 13d – Bestand nach Ferats Downloads, komplett

Stand 11.10.2026, abends · Download-Liste: `antworten/sehens-downloadliste.md` + `antworten/sehens/downloadliste.json` · je Biom: `antworten/sehens/<biom>/asset_bedarf.json` → `abgleich_13d`, `katalog.md` → „Abgleich Inventar 13d“

## Kurzfazit

- **Übernommen.** Grundlage ist jetzt das Inventar 13d: `netze.csv` mit 1 965 Netzen (+273 gegenüber 13b, keines entfernt) und `inventar_extra.json` mit 116 Niagara-Systemen (+43) und 85 Decals (+41).
- **Erledigt (5 Pakete mehr, jetzt 13):** Nature Water FX, Lava & Volcano, Coast & Dunes und Mountain sind vollständig im Projekt. Dazu kommen Megascans Desert Western und Sandstein mit 43 Netzen, davon 41 nutzbar.
- **Limestone fehlt weiter.** In `netze.csv` gibt es keine neuen Kalk-Netze, weder von Megascans noch das „Limestone Rock Set“ von Ancraite. Beide stehen deshalb als „noch nicht geladen – Ferat wollte laden“ in der Liste. Die Lücke „Karsttürme“ (dschungel_01, _03, _05, _06; aue_07) ist weiter offen.
- **Zwei Desert-Western-Netze bitte erneut laden:** `uldubik_tier_0` und `uk5ebcp_tier_0`. Sie waren bisher Held von canyon_06 und canyon_08 und Begleiter von wueste_03. Diese drei Orte sind auf vollständige Netze umgeplant.
- **Noch offen sind 28 Pakete: A 1, B 12, C 15.** Davon sind **6 kostenlos bzw. aus der Bibliothek, die lädt Claude auf Wunsch**. **22 sind kostenpflichtig oder im Preis ungeprüft, die nur nach Ferats OK.** Dazu kommen die 2 Limestone-Downloads und die 2 Netze zum Neuladen.
- **Abgleich in allen 15 Biomen:** 85 Wünsche sind jetzt mit echten Assets gedeckt, 49 Ersatzlösungen werden gegen echte Assets getauscht, 60 Punkte fehlen weiter. Jeder Asset-Name ist gegen `netze.csv` bzw. `inventar_extra.json` geprüft (131 verschiedene Namen).
- **Phase 2:** Die Phase-2-Planer werden gerade auf die echten Assets umgestellt; die Planer-Skripte habe ich nicht angefasst. Den Stand trägt der Koordinator im STATUS nach.

## Was übernommen wurde

| Paket | Pfad | Netze / Systeme laut Inventar | wichtig für die Orte |
|---|---|---|---|
| **Nature Water FX** (gekauft) | `/Game/NatureWaterFX/FX/*` | 20 Niagara, 6 Materialien | `NS_Waterfall_Small/Medium/Large` für alle Fälle (der Vorhang bleibt `M_EL_Wasserfall2`); `NS_Impact_*` als Gischt statt `lokaler_nebel`/`NS_Smoke_Plume`; `NS_Geyser_Large` für das Blasloch kueste_08; `NS_Geyser_Small` für die Eisvulkane frost_06 und den Dampfschlot lava_02; `NS_Stream_*` für Kaskaden; `NS_Wake_*` (Kopie) als Schaum um Felsfüße |
| **Lava & Volcano** (vollständig) | `/Game/Lava_Volcano_Environment_Set/*` | 44 Netze (+19), 23 Niagara, 24 Decal-Materialien | **`SM_lava_wall_01–09` sind wieder da.** Damit wird der Basalt-Ersatz in lava_01, _04, _05 und _08 getauscht; die Basaltorgel lava_07 bleibt aus Basalt. Lava-Fläche `SM_lava_disc`/`SM_Lava_HP` und `M_NM_Master_Lava_Material` für das Glutauge. `FX_Lava_Smoke_*`, `FX_Distortion_Small/Big` (Hitzeflimmern), `FX_Lava_Bubble`, `FX_Lava_Particle_01/02`. Dazu Glut-Decals `MI_NM_Decal_Lava_{Normals,NoAlbedo,NoAlbedoNoNormals}_01–07` |
| **Coast & Dunes** (vollständig) | `/Game/Coast_Dunes_Environment_Set/*` | 196 Netze (+65), 17 Decal-Materialien | Nassband `MI_Deca_Wet`/`_Flat` **an allen Wasserorten** statt `MI_Leakage_*`. Weiter: Algen `MI_Decal_Algae`, Lehm `MI_Decal_Clay_01–03`, Rippel `MI_Decal_Sand_Small/Big_Waves`, Kiesel `MI_Decal_Rocks_Small/Big`. Seetang `SM_seaweed_01_A–E`, Muscheln `SM_shells_01_A/B`, Treibholz `SM_beach_driftwood_02–09` (0,8–2,4 m), Wurzelteller `SM_pine_roots_01` (3,2 m) |
| **Mountain** (vollständig) | `/Game/Mountain_Environment_Set/*` | 244 Netze (+141), 2 Decals | 30 Pilze, darunter Baumschwamm `SM_mushroom_red-belted_conk_01–03`; damit ist Forest Fungi nur noch C. Felsen `SM_Big_rock_01/02` (8–10 m) und `SM_flat_rock_01` (9,9 m). Wurzeln `SM_stones_roots_04/05` (6,6 m) und `SM_roots_slope_*` für den Wurzelstein. Latschen `SM_dwarf_pine_*`, Jungkiefern `SM_Forest_pine_tree_00_A–D`, Heide `SM_heath_*_02/03`. Fluss-/Seematerial `M_River_Water_Translucent(_Tess)`, `M_Lake_Water_Translucent_Tess` |
| **Megascans Desert Western + Sandstein** | `/Game/Fab/Megascans/3D/Desert_Western_*` u. a. | 36 + 7 Netze, alle Nanite | Cliff/Formation/Spire Layered XL bis 68,6 × 43,5 × 36,8 m. **Hoodoos canyon_05 aus `Spire_Large_03/05` und `Spire_Layered_XL_03–05`**; die Welle canyon_08 aus `Cliff_Layered_Large_03`. Rote Stufe, Rippenland und Regenbogenhang aus `Cliff_Layered_XL_02/_11` und `Formation_Layered_XL_01/_06`. Pilzkappe wueste_03 aus `Red_Sandstone_Cliff_sfEby`, Dreikanter aus `Sharp_Sandstone_pjcxN`. Fab-Material, kein Material-Fix |
| Megascans Eis/Schnee (Nachtrag) | `/Game/Fab/Megascans/3D/Snow_*` | jetzt 33 (+2) | `Snow_Hill_vdbmabvva` (20,7 × 13,8 × 3,0 m) als Altschnee-Kegel für gletscher_02 |

**Abweichungen zwischen 13d und dem Inventar** (beim Abgleich aufgefallen):

- **Mountain:** 13d nennt „+243 Netze“, `netze.csv` hat **+141**. Der Gesamtstand ist 244, wahrscheinlich ist das gemeint.
- **Desert Western:** 13d nennt 45 Assets, `netze.csv` hat 36 Netze.
  - Die Oberflächen `Cracked_Sandstone_Mud` und `Sandstone_Gravel` sind keine Netze.
  - `Cliff_Layered_XL` gibt es nur als 01/02/03/07/08/11/16. **XL 14 aus dem ursprünglichen Wunsch fehlt.** XL_02 und XL_11 übernehmen die Rolle, ein Nachladen ist nicht nötig.
- **Mountain-Wasserfall-Material:** Ein eigenes Wasserfall-Material ist unter den im Inventar gelisteten Namen nicht sichtbar (gelistet sind 12 von 21 Materialien). Die Fallvorhänge bleiben deshalb bei `M_EL_Wasserfall2`/`MI_EL_Wasserfall`; Bewegung und Gischt kommen aus Nature Water FX.
- **Coast-&-Dunes-„Stempel“:** Sie stehen nicht als Netz im Inventar, die Geländestempel bleiben deshalb eigene.
- **Neue Doppelnamen** (in Plänen immer den vollen Pfad nehmen):
  - `SM_Forest_pine_06` gibt es zweimal: als Baum (Foliage, 25 m), den frost_04 nutzt, und als Wurzelstück (Roots, 2,5 m).
  - `SM_Big_rock_01/02` (Mountain) ist nicht dasselbe wie `SM_Big_Rock_01/02` (Environment_Set).
  - `SM_pine_roots_01` (Coast) ist nicht dasselbe wie `SM_Pine_roots_01` (Mountain).
  - `SM_grass_01_3/_4` gibt es in Forest und in Mountain.
  - Hilfsnetze ohne Nutzen: `SM_Overview_cube`, `SM_Clean_Water`, `SM_River`.

## Neuer Stand der Download-Liste

**Erledigt / im Projekt (13):** die 8 Pakete aus 13b und neu Nature Water FX, Lava & Volcano, Coast & Dunes, Mountain sowie Desert Western + Sandstein, jeweils mit echtem Pfad und Netz- bzw. Systemzahl.

**Läuft / noch nicht geladen / erneut laden (4):**

| Paket | Stand | Beschaffung |
|---|---|---|
| Weitere Megascans-Limestone-Assets (große Kalkfelsen, Karst) | noch nicht geladen – Ferat wollte laden | kostenlos → Claude lädt auf Wunsch |
| Limestone Rock Set (Ancraite) | noch nicht geladen – Ferat wollte laden (Link weiter nicht belegt) | kostenlos → Claude lädt auf Wunsch |
| `Desert_Western_Cluster_Rock_Medium_05_uldubik` | erneut laden (1 von 5 Dateien) | kostenlos → Claude lädt auf Wunsch |
| `Desert_Western_Ledge_Rock_Small_07_uk5ebcp` | erneut laden (1 von 5 Dateien) | kostenlos → Claude lädt auf Wunsch |

Die zwei fehlgeschlagenen IDs aus 13b (`61882812-…`, `6676d940-…`) bleiben unter „Erneut versuchen“. Es ist möglich, dass es genau diese zwei unvollständigen Netze sind.

**Noch fehlend – kostenlos/aus Bibliothek → Claude lädt auf Wunsch (6):**

- Electric Dreams Environment (B)
- Megascans Trees: European Black Alder (B)
- Megascans Icelandic Sand With Pebbles (C)
- Tundra Icelandic Rock Cluster (C)
- Megascans Desert Pack (C, Vault)
- Megascans Sandstone (C, Vault; durch Desert Western weitgehend gedeckt)

**Noch fehlend – kostenpflichtig bzw. Preis ungeprüft → nur nach Ferats OK (22):**

| Prio | Pakete |
|---|---|
| A (1) | **Nanite Driftwood Props**: Held der Treibholzburg aue_04. Das neue Coast-Treibholz misst nur 0,8–2,4 m und reicht für den Spülsaum (aue_05 erledigt), nicht für die Burg. |
| B (10) | Quercus Robur; CryoGen; Arctic Cliffs; Cave Ambience (ca. 9 €); Cave Stalactites & Wall Kit; Nanite Tropical Plant Pack 2; Travertine Terraces; Fantasy Ambiences (ca. 65 €); Bald Cypress Tree Pack; Hollowstone Canyon (nur noch für die Wabenwand wueste_08) |
| C (11) | Forest Fungi (B → C); Ultimate Niagara Environmental VFX (B → C, offen nur noch Sandfahnen und Schnee); Wadi Rum Sandstone (B → C); Imposing Dead Quercus; Moss & Lichen; Niagara VFX Pack Snow; Giant Fantasy Mushrooms; Procedural Rocks Generator (kaum noch nötig); Tropical Vegetation; Rain Forest Pack; Wilderness Nature Loops |

**Top 5 jetzt:**

1. Limestone + Ancraite (kostenlos)
2. Electric Dreams (kostenlos)
3. European Black Alder (kostenlos)
4. Nanite Driftwood Props (OK nötig)
5. Quercus Robur (OK nötig)

A + B sind etwa 19 GB, soweit eine Größe bekannt ist.

**Gelöste Lücken:**

- Gischt, Fontänen und Wasserfall-Effekte
- Hoodoos im canyon_05
- Senkrechter Wurzelteller (bergwald_07)
- Nassband an allen Wasserorten
- Lavaröhre und Stricklava (wieder mit `SM_lava_wall_*`)

**Weiter offen:**

- Karsttürme (Limestone)
- Schnee- und Tropfen-Niagara
- Raureif-Bäume
- Ganze Sumpfzypressen
- Brandungsklang
- Tafoni (Wabenwand)

## Was je Biom getauscht wird (Auszug, Details in `abgleich_13d`)

- **Lava:**
  - `SM_lava_wall_01–09` statt Basalt (lava_01, _04, _05, _08).
  - Fumarolen `FX_Lava_Smoke_*` + `FX_Distortion_Small`.
  - Glutauge mit `SM_lava_disc`, Lava-Material und Glut-Decals.
- **Canyon:**
  - Desert Western statt `SM_MassiveSandstoneCliff_*` + Rotband-Tönung für canyon_01, _03, _04 und _05.
  - canyon_06 und _08 nehmen statt der unvollständigen Netze `vbvqbbofa_tier_0` (Ledge_Rock_Large_03) bzw. `vbzmdd1ga_tier_0` (Cliff_Layered_Large_03). `MI_EL_SW_Welle` auf `vbzmdd1ga_tier_0` umhängen.
- **Ödland:**
  - Rippenland und Regenbogenhang aus Desert Western (die Bänder sind in der Textur, die Tönungen nur noch für Akzente).
  - Höllentor mit Glut-Decal + `FX_Distortion_Big`.
  - Schlammvulkänchen mit `FX_Lava_Bubble` (Kopie braun) + `Mound_Mud_Rough_01`.
  - Totenpfanne mit `MI_Decal_Clay_*`.
- **Wüste:**
  - Yardang-Flanken aus `Ledge_Rock_Large_03`/`Cliff_Layered_XL_03`.
  - Wächter ohne `uldubik` (dafür `uk4pehu_tier_0`, Schaft `Spire_Large_05`, Kappe `Red_Sandstone_Cliff_sfEby`).
  - Rippel- und Kiesel-Decals.
- **Küste und Fjord:**
  - Seetang, Muscheln und `MI_Decal_Algae` statt `MI_Leakage_10`.
  - Gischt `NS_Impact_*`, Blasloch `NS_Geyser_Large`.
  - Fälle `NS_Waterfall_*` (Seefall, Schleierwand, Hängetal).
- **Bergwald, Elfenwald, Aue:**
  - Mountain-Pilze statt `SM_mushroom_01/02`.
  - Wurzelteller `SM_pine_roots_01` (Windwurf).
  - Wurzelstein mit `SM_stones_roots_04/05`.
  - Schwalbenwand mit `MI_Decal_Clay_*`.
  - Klamm, Karsee, Elfentreppe und Farnschlucht mit `NS_Waterfall_*`/`NS_Stream_*`.
- **Gletscher, Frost, Tundra, Heide, Sumpf:**
  - Lawinenkegel mit `Snow_Hill_vdbmabvva`.
  - Eisvulkane `NS_Geyser_Small`.
  - Gletscherschliff mit `SM_flat_rock_01`.
  - Windkante mit Rippel-Decals.
  - Wollsackfall mit `NS_Waterfall_Small`.
  - Nassband `MI_Deca_Wet(_Flat)` an allen Wasserorten.

## Alte Ortsnamen aus Katalog v1 → endgültige Orte

| Name in 13d (Katalog v1) | endgültig |
|---|---|
| Der Atem (Geysir, gletscher) | **Ort gestrichen** (Gletscher jetzt gletscher_01–08). Die Geysir-Systeme gehen an kueste_08 Das Blasloch, frost_06 Die Eisküste (Eisvulkane) und lava_02 Schwefelgrund (Dampfschlot). |
| Diamantstrand (fjord) | **Ort gestrichen** (kein Gletscher am Fjord). Das Küstenmaterial geht an kueste_05 Die Gezeitenbank, kueste_07 Der Dünenkamm und fjord_05 Der Fjordkopf. |
| Sonnentor (wüste) | **canyon_01 Das Sonnenfenster** |
| Naturbrücke (canyon), auch „Felsfenster“ | **canyon_01 Das Sonnenfenster** (ein Bogen im Canyon) |
| Bemalte Hügel (ödland), auch „Regenbogenhang“ (lava) | **oedland_02 Der Regenbogenhang** (der Lava-Regenbogenhang ist als Dopplung gestrichen) |
| Feenkamine (ödland) | **Ort gestrichen.** Die Felstürme stehen jetzt im canyon_05 Der Hoodoo-Kessel (Desert-Western-Spires). |
| Hoodoo-Kessel / Die Welle / Flüsterschlucht | canyon_05 / canyon_08 / canyon_04 |
| Die Wächter | wueste_03 Die Wächter |
| Schleierfall, Klamm | bergwald_05 Klemmblock-Klamm (Schleierfall); die Schleierwand im Fjord ist fjord_02 |
| Hängender Garten (canyon) | Teil von canyon_07 Die Smaragdgumpe |
| Wurzelstein | bergwald_08 Der Wurzelstein |
| Brandungspfeiler / Grotte (Küste) | kueste_01 Die Alten / fjord_07 Die Brandungsgrotte (die Küste hat keine Grotte) |
| Glutauge, Schwefelgrund, Kraterreihe | lava_08, lava_02, lava_06 |
| Lavafälle, Rauchfahnen | **kein eigener Ort.** `FX_Lava_Waterfall*` ist nicht eingeplant; `FX_Smoke_Volcano_01` ist höchstens dezent über der Kraterreihe lava_06 möglich (Bild-Check). |
| Blasloch, Quellen, Stufenfälle | kueste_08; Quellen aue_07 Blautopf, dschungel_02 Turmquelle, wueste_04 Quelloase; Stufenfälle heide_06 Wollsackfall, elfenwald_04 Elfentreppe |

## Geänderte Dateien

- `antworten/sehens-downloadliste.md`, `antworten/sehens/downloadliste.json`:
  - neu: „Erledigt“ mit 13 Paketen, „Läuft / noch nicht geladen / erneut laden“ mit 4 Einträgen
  - Feld `beschaffung` an jedem Paket
  - Summen mit `kostenlos_claude_laedt` und `nur_nach_ferats_ok`
  - neue Top 5, Lücken und Hinweise zu Doppelnamen
- `antworten/sehens/<alle 15 Biome>/asset_bedarf.json`: neuer Block `abgleich_13d` mit:
  - `erfuellt` (mit Pfad, Maßen, Nanite)
  - `ersatz_tauschen`
  - `fehlt_weiter` (mit Beschaffung)
  - `pakete_status_13d`
  - bei Canyon und Wüste `nicht_verwenden`, bei Frost `warnung`
  - Orte, Kameras und die Felder aus 13b sind unverändert.
- `antworten/sehens/<alle 15 Biome>/katalog.md`: Abschnitt „Abgleich Inventar 13d“ am Ende.

## Rückfragen

1. **Limestone:** Soll Claude die kostenlosen Limestone-Assets jetzt aus der Bibliothek laden? Wenn ja: welche Megascans-Limestone-Assets? Oder Freigabe „große Kalkfelsen/Felswände, Claude wählt“? Und gibt es einen Link zum Ancraite-„Limestone Rock Set“?
2. **Neu laden:** Darf Claude `uldubik` und `uk5ebcp` neu laden und dabei die zwei fehlgeschlagenen IDs aus 13b prüfen?
3. **Kostenlose Pakete:** Darf Claude diese gleich mitladen?
   - Electric Dreams
   - European Black Alder
   - Icelandic Sand
   - Tundra Icelandic Rock Cluster
   - aus dem Vault, falls vorhanden: Megascans Desert Pack und Megascans Sandstone
4. **Kostenpflichtig – welche willst du?** Empfehlung nach Wirkung:
   - Nanite Driftwood Props (einziges A)
   - Quercus Robur
   - CryoGen
   - Hollowstone (nur Wabenwand)
   - Arctic Cliffs

   Forest Fungi, Ultimate Niagara und Wadi Rum sind jetzt verzichtbar (C).
5. **Mountain-Wasserfall-Material:** Gibt es im Mountain-Set ein eigenes Wasserfall-Material (Name)? Im Inventar sind nur 12 der 21 Materialnamen gelistet.
6. **Coast-&-Dunes-„Stempel“:** Wo liegen sie im Projekt? Sie stehen nicht in `netze.csv`; wenn es Heightmap-Texturen sind, könnten Claudes Geländestempel sie als Vorlage nutzen.
7. **Für den Koordinator (Hinweise, keine Rückfrage an Ferat):**
   - `uldubik_tier_0`/`uk5ebcp_tier_0` stehen auch außerhalb der Sehenswürdigkeiten: `skripte/felsgruppen_regeln.json`, `skripte/wueste_ergaenzung_regeln.json`, `assets-taxonomie.*`, `verteilung-*.md`. Die habe ich nicht angefasst.
   - Die Lib sollte bei `SM_Forest_pine_06` den vollen Pfad verlangen: Der Name ist exakt doppelt, nicht nur in der Groß-/Kleinschreibung.

## Nachtrag: Ferats Grundsatz: Megascans vor Kauf

Ferat hat einen neuen Grundsatz: „Kein Geld ausgeben, solange man Besseres von Megascans holen kann.“ Die Megascans hat er 2024 beansprucht, für ihn sind sie also kostenlos. Er lädt sie selbst.

Daraufhin habe ich am 11.10. abends jedes kostenpflichtige oder preislich ungeprüfte Paket und jede Lücke gegen Megascans und Megaplants geprüft. Geprüft wurde nur per Websuche, denn fab.com, quixel.com und die UE-Foren sind aus der Cloud nicht abrufbar. Nicht Belegtes ist in der Liste als [ungeprüft] markiert.

- **Drei Käufe entfallen:**
  - Nanite Driftwood Props → Megascans-Driftwood: Driftwood Trunk, Driftwood, Driftwood Piece, Driftwood Plank, Small Driftwood Piece, dazu „Dead Tree“ als Burgkern.
  - Quercus Robur → „Megaplants: English Oak“. Das Asset ist kostenlos, aber experimentell: Es braucht den Procedural Vegetation Editor und Nanite Foliage.
  - Forest Fungi → Mountain-Pilze und Megascans Forest Undergrowth aus dem Vault.
- **Limestone ist konkret:** Die Sammlung „Limestone Quarry“ bringt Quarry Cliff (5 Fab-Listings, bis 8,8 m) sowie Limestone Rocks, Rubble und Slab. Damit lässt sich die Karst-Lücke schließen, sobald Ferat lädt. Das Ancraite-Set hat die Websuche nicht gefunden.
- **Nur teilweise ersetzt:** Arctic Cliffs (neu: Frozen Lake + Frost), Wadi Rum, die tote Stieleiche, Procedural Rocks und die Tropen-Pakete. Beide Einträge bleiben.
- **Nicht ersetzbar:** Klänge, Niagara-Effekte, CryoGen, Sumpfzypressen, Tropfsteine, Sinterterrassen und Tafoni (Hollowstone).
- **Neuer Stand:** A 1, B 12, C 16, zusammen 29 Pakete. Davon sind **10 kostenlos**: 9 lädt Ferat aus Megascans, 1 lädt Claude. **19 sind kostenpflichtig oder ungeprüft**, vorher waren es 22.

Ferats Ladeliste steht in `antworten/sehens-downloadliste.md` unter „Megascans zum Laden (kostenlos)“. Sie ist nach Wirkung sortiert und nennt je Asset die Ort-IDs. Maschinenlesbar steht sie in `antworten/sehens/downloadliste.json` → `megascans_ladeliste`. Damit sind die Rückfragen 1, 3 und 4 oben überholt, soweit es um Megascans geht.
