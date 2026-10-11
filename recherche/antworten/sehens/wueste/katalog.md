# Wüste – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1, Biom-Agent B6)

Stand 11.10.2026 · Daten: `vorlagen/daten/sehens` (2 m) · Werkzeuge: `antworten/skripte/sehens_lib` · Dateien: `standorte.json`
(8 Orte, Prüfer **0 FEHLER / 0 WARNUNG**), `asset_bedarf.json`, `<id>.png` je Ort.
Die Wüstenfelder C3/C4/D3/D4/D5/E3/E4/E5 sind gebaut (Namaqualand-Planer, Wüstenbach mit Palmen in E4) – hier wird **nur ergänzt**,
nichts entfernt; die Orte liegen bewusst neben dem Bestehenden und nehmen dessen Pflanzen (Fächerpalmen, Sukkulenten, Searsia) auf.

## Das Gelände in Zahlen

Die Wüste (1,43 km², E4/E3/D4/D3) ist kein Erg, sondern ein **Rippenland**: NW–SO-streichende Sandsteinrücken (bis 133 m) mit
sandgefüllten Gassen dazwischen – die Windrichtung ist in den Fels geschrieben. Im Süden liegt das gebaute Palmental (Wüstenbach),
im Osten ein Trockental mit Bach zur Küste, im Südosten eine flache Küstenebene (0–5 m). Boden: Sand 58 %, Sandstein 19 %, Geröll 10 %.

| Kennzahl | Wert |
|---|---|
| Fläche 80–300 m vom Weg | 0,80 km² (größter Abstand 456 m) |
| Sperrflächen | Städte ROMAN_LOC_003 / _005 / _004 (+ 150 m) nehmen die Mitte |
| Packung bei 350 m (mit den 8 Canyon-Orten) | 8 Orte, kein Pfad nötig |

## Übersicht

| ID | Name | Art | Form | Feld | X / Y (m) | Weg | Sicht |
|---|---|---|---|---|---|---|---|
| wueste_01_yardang_flotte | Die Yardang-Flotte | Leuchtfeuer | windgeschliffene Rücken an der Küste | D3 | −836 / −1336 | 299 m | 110/214 Wegpunkte |
| wueste_02_sternduene | Die Sterndüne | Leuchtfeuer | Sterndüne mit drei Kämmen | E4 | −420 / −310 | 131 m | 11/316 |
| wueste_03_die_waechter | Die Wächter | Leuchtfeuer | Pilzfelsen-Gruppe | E4 | 100 / −720 | 149 m | 14/173 |
| wueste_04_quelloase | Die Quelloase | Fundstück | Quelltopf mit Palmen | E3 | −480 / −1350 | 231 m | verdeckt |
| wueste_05_salzpfanne | Die Salzpfanne | Fundstück | Küsten-Sabkha hinter Dünenriegel | E4 | 0 / −380 | 144 m | verdeckt |
| wueste_06_windkanterfeld | Das Windkanter-Feld | Fundstück | Steinpflaster mit Dreikantern | E4 | −501 / −939 | 108 m | verdeckt |
| wueste_07_trockenes_wadi | Das Trockene Wadi | Fundstück | Flutrinne mit Akazien, Trockenfall | E3 | 169 / −1149 | 96 m | verdeckt |
| wueste_08_wabenwand | Die Wabenwand | Fundstück | Tafoni + Wüstenlack an Küstenwand | E3 | −128 / −1338 | 139 m | verdeckt |

Mischung 3 / 5. Erzählung: **Wind** formt (Yardangs 01, Düne 02, Pilzfelsen 03, Windkanter 06), **Wasser** fehlt oder verdunstet
(Quelle 04, Pfanne 05, Wadi 07), **Salz** aus der Gischt höhlt die Wand (08).
**Abgrenzung:** nur Windformen, Salz und Oase. Nicht hier: Felsbogen, Hoodoos, Slot, Kolke (Canyon – Wassererosion im Sandstein),
Badlands/Ton (Ödland), Dünen an der Küste mit Strandhafer (kueste). Pilzfelsen ≠ Hoodoo (siehe canyon/katalog.md); die Sabkha
(Salz, Küste) ≠ Totenpfanne (Ton, Badland-Endpfanne, oedland_07).
**Sichtmessung, Kameras:** wie im Canyon-Katalog (Wegpunkte 20 m, Wege + `pfade[]`, Stempel nachgerechnet; §8 Stand 13:00).

---

## wueste_01_yardang_flotte – Die Yardang-Flotte (Leuchtfeuer)

**Was man sieht:** Vier lange Felsrücken laufen parallel auf die Küste zu wie die Rümpfe gestrandeter Schiffe: scharfer, steiler Bug
nach Nordwesten (Windseite), lang auslaufendes Heck mit Sandfahne. Die Flanken sind waagrecht gerieft, zwischen den Rümpfen
Sandgassen mit Rippelmarken.
**Vorbild:** Yardangs der Wüste Lut (Iran), Qaidam; Spiel: Rippenland der Hissing Wastes (DA:I), Windfelsen in Assassin's Creed Origins.
**Standort:** D3, X −836 / Y −1336 m, Boden 44,8 m. Nordenden der Rippen (Rückengrat, Relief 36 m, Hang bis 73°), Küste 40 m
nördlich. Weg 299 m, Stadtrand 427 m.
**Sicht:** 110 von 214 Wegpunkten sehen ≥ 30 % der 15-m-Rücken, mittlerer Anteil 0,48, bis 799 m; `_fern` X −754 / Y −1928 (über die
Bucht, 597 m).
**Komposition und Anmarsch:** Zugang 403 m, „weich“ (4 m > 25°) → Trampelpfad mit zwei Kehren in einer Sandgasse. `_held` 60 m
südlich in der Gasse, Blick nach N: zwei Rümpfe rahmen, der dritte zeigt den Bug gegen das Meer.
**Detail-Ebenen:** Held – Rumpfflanken `vmnmbhv_tier_0`, `SM_MassiveSandstoneCliff_05` (liegend, 45 % eingegraben, Riefen
waagrecht). Begleiter – `SM_HugeSandstoneCliff_05/07`, `uchoab3fa_tier_0` als Heckausläufer. Schutt – `SM_namaqualand_boulder_03_NN`,
`SM_RockSandstone_034` nur an der Bugseite (Ursache: Windabtrag unterschneidet den Bug). Kleinzeug – Kiesel, Sandschleppen
`SM_sandy_slope_05` im Lee. Bewuchs – fast keiner; Trockengras und `SM_othonna_cerarioides_f_NN` nur im Lee.
**Wasser, Effekte, Licht:** keine; Sandfahne als Wunsch-Niagara (optional).
**Geländeänderung:** Gassen −1…−2 m geglättet, Rücken +2 m geschärft; Fenster 280 × 280 m.
**Assets:** „Wadi Rum Sandstone Rock 01–04“ (B), „Ultimate Niagara Environmental VFX“ (B, Sandfahne); Ersatz Bestand,
`MI_EL_SW_Wueste_Sandauflage`.
**Aufwand und Risiko:** hoch (große Form). Risiko: Schalen aus der Ferne sichtbar gekachelt → Mischen, Sand in den Fugen.
Budget ca. 8 000 Instanzen, 30 Akteure.

## wueste_02_sternduene – Die Sterndüne (Leuchtfeuer)

**Was man sieht:** Eine 22 m hohe Düne mit drei geschwungenen, messerscharfen Kämmen, die sich im Gipfel treffen; eine Flanke im
Licht goldgelb, die andere im Schatten blaugrau. Am Fuß ein toter Köcherbaum, halb begraben.
**Vorbild:** Erg Chebbi, Sossusvlei (Big Daddy); Spiel: Dünen in Assassin's Creed Origins, Hissing Wastes.
**Standort:** E4, X −420 / Y −310 m, Boden 27,9 m. Sandhang (Sand 88 %) zwischen Rippen südlich des Palmentals; Sand sammelt sich hier
im Windschatten der Rippen. Weg 131 m, Stadtrand ROMAN_LOC_004 174 m.
**Sicht:** 11 von 316 Wegpunkten im Ring sehen den Gipfel (22 m Düne, Zielhöhe 25 m), bis 385 m – lesbar vom Palmental und vom
Südweg; `_fern` X −190 / Y −518 (311 m).
**Komposition und Anmarsch:** Zugang 144 m streng (max 19°). `_held` 110 m südlich, Blick N: Kämme führen zum Gipfel, dahinter die
Rippen.
**Detail-Ebenen:** Held – Gelände (Stempel). Begleiter – Sandschleppen `SM_sandy_slope_04/05` an den Kämmen. Schutt –
`SM_namaqualand_boulder_05_NN` im Duenental. Kleinzeug – Kiesel im Ausblasungstal. Bewuchs – toter Köcherbaum
`SM_dead_quiver_trunk_NN` (Natur erzählt: die wandernde Düne hat ihn begraben), Rooibos am Fuß, Trockengras. Kontaktzone – Sand
überdeckt den Fels.
**Wasser, Effekte, Licht:** Sandfahne am Gipfel (optional, Niagara-Wunsch).
**Geländeänderung:** Düne +22 m, drei Kämme (Stempel), Fenster 260 × 260 m; Bodenlage Sand 100 %, Rippel als Decal (Coast & Dunes).
**Assets:** „Coast & Dunes – Environment Set“ (A, läuft) – Dünen-Stempel und Rippel-Decals; „Ultimate Niagara Environmental VFX“ (B).
**Aufwand und Risiko:** mittel. Risiko: Kammlinie muss scharf sein (1-m-Daten, Stempel mit Grat).
Budget ca. 1 500 Instanzen, 3 Akteure.

## wueste_03_die_waechter – Die Wächter (Leuchtfeuer)

**Was man sieht:** Sieben weiße, gedrungene Pilzfelsen stehen auf einer Kiesfläche wie Wachen; der Wind hat ihre Füße zu Hohlkehlen
geschliffen, die dunklen Kappen hängen über. Der größte ist 10 m hoch.
**Vorbild:** Weiße Wüste (Farafra, Ägypten), Pilzfelsen der Sahara; Spiel: Felspilze in Hissing Wastes, Wildlands-Wüsten.
**Standort:** E4, X 100 / Y −720 m, Boden 35,4 m. Hangverflachung über dem östlichen Trockental (Sandstein 51 %, Geröll 41 %).
Weg 149 m, Stadtrand 310 m.
**Sicht:** 14 von 173 Wegpunkten sehen ≥ 30 % der 10-m-Gruppe, bis 740 m; `_fern` X −296 / Y −728 (396 m).
**Komposition und Anmarsch:** Zugang 216 m „weich“ (10 m bis 35°) → kurze Kehren. `_held` 40 m nördlich, Gegenlicht.
**Detail-Ebenen:** Held – Kappe `SM_RockSandstone_040`, Fuß `SM_MassiveSandstoneCliff_03` (schmal) mit `MI_EL_SW_Wueste_Sandauflage`.
Begleiter 6 – `SM_SandstoneBoulder_05`, `SM_namaqualand_boulder_03_NN`. Schutt 40–80 – abgefallene Kappen
(`SM_namaqualand_boulder_04_NN`, `SM_SandstoneBoulder_03`, `uldubik_tier_0`). Kleinzeug – Kies `SM_namaqualand_boulders_01_b_NN`.
Bewuchs – Sukkulentenpolster im Lee (`SM_cheiridopsis_succulent_g_NN`), Didelta.
**Wasser, Effekte, Licht:** keine.
**Geländeänderung:** Fläche +/−1 m geglättet, Bodenlage Kies/Geröll (Deflationspflaster).
**Assets:** „Wadi Rum Sandstone Rock 01–04“ (B), „Hollowstone Canyon“ (C), „Procedural Rocks Generator“ (C); Lücke Pilzfelsen →
Bestandslösung in `asset_bedarf.json`.
**Aufwand und Risiko:** mittel. Risiko: Abgrenzung zum Hoodoo – gedrungen, hell, keine Bänder.
Budget ca. 3 000 Instanzen, 20 Akteure.

## wueste_04_quelloase – Die Quelloase (Fundstück)

**Was man sieht:** Im engen Talgrund nahe der Nordküste quillt aus dem Fuß der Rippen ein türkiser Quelltopf, 12 m breit; fünf
Fächerpalmen, Binsen und Rohrkolben drängen sich um das Wasser, das nach 40 m im Sand versickert.
**Vorbild:** Guelta d'Archei, Ein Gedi; Spiel: Oasen in Assassin's Creed Origins, Zerrikanien-Vorstellung (Witcher).
**Standort:** E3, X −480 / Y −1350 m, Boden 16,8 m. Talgrund (Einzugsfläche 65 000 m²) am Fuß der Rippen – Schichtquelle am Übergang
Sandstein/Sand; 40 m im Biom. Weg 231 m, Stadtrand 473 m.
**Sicht:** verdeckt heute und mit Becken (0,00, 21 Wegpunkte).
**Komposition und Anmarsch:** Zugang 603 m „weich“ (Umweg durch die Rippen, 4 m mit 30°) → Trampelpfad mit Kehre. Man hört Wasser
(City & Nature Sounds) bevor man es sieht. `_held` 100 m nördlich hangauf, Blick ins Tal.
**Detail-Ebenen:** Held – Quelltopf (Wasser) + Palmengruppe `SM_Palm_01_03_G`, `SM_Palm_01_04_G`, `SM_Palm_01_02_G`. Begleiter –
`SM_Palm_01_07_G/09_G` (Jungpalmen), `SM_HugeSandstoneCliff_02` als Quellwand. Schutt – `SM_RockSandstone_021`, `SM_stones_01_3`.
Kleinzeug – Palmwedel `SM_dry_quiver_leaf_a_NN`, Kiesel. Bewuchs nach Ursache – Feuchtring: `SM_Rohrkolben_Horst_2`,
`SM_Rohrkolben_Jung_1`, `SM_ToadRush_010`, Farn `SM_Fern_02a` an der Quellwand; außen Searsia.
**Wasser, Effekte, Licht:** `see` Quelltopf (farbe `tuerkis`, 3 m), `bach` 40 m → `versickert`; Nassband-Decals.
**Geländeänderung:** Becken −3 m (r 18 m), Fenster 80 × 80 m.
**Assets:** Bestand (Palmen sind schon im Palmental verwendet). „Coast & Dunes“ (B) Nass-Decals; „Free City & Nature Sounds“ (vorhanden).
**Aufwand und Risiko:** mittel. Risiko: Dopplung mit dem gebauten Palmental → hier Quelle + Wasser blau, dort Bach.
Budget ca. 4 000 Instanzen, 12 Akteure, 4 Decals.

## wueste_05_salzpfanne – Die Salzpfanne (Fundstück)

**Was man sieht:** Hinter einem niedrigen Dünenriegel liegt eine gleißend weiße Kruste mit Wabenmuster, 120 m breit; in der Mitte eine
milchige Restsole, am Rand Treibholz und salzverkrustete Steine.
**Vorbild:** Sabkha der Arabischen Golfküste, Badwater; Spiel: Salzflächen in Mad-Max-/Wildlands-Wüsten.
**Standort:** E4, X 0 / Y −380 m, Boden 1,9 m. Abflusslose Küstenebene (Hang 2°, TPI −4,3 m, Einzugsfläche 21 000 m²) – Meerwasser
und Abfluss verdunsten. Weg 144 m, Stadtrand ROMAN_LOC_004 322 m.
**Sicht:** verdeckt (0,00, 65 Wegpunkte), auch mit Pfanne −1 m und Riegel +6 m.
**Komposition und Anmarsch:** Zugang 151 m streng (max 12°) über den Riegel – auf dem Kamm öffnet sich das Weiß. `_held` 120 m
westlich auf dem Riegel.
**Detail-Ebenen:** Held – Kruste (Bodenlage + Decal). Begleiter – `SM_namaqualand_boulder_02_NN`, `SM_beach_driftwood_01` mit
`MI_EL_SW_Salzkruste`. Schutt – `SM_namaqualand_rocks_01_b_NN`. Bewuchs nach Ursache – Salzpflanzen nur am Rand
(`SM_crystalline_iceplant_a/c_NN`, Leipoldtia), im Kern nichts.
**Wasser, Effekte, Licht:** `see` Restsole (farbe `salzweiss`, 0,2 m); helles Weiß braucht Belichtungsprüfung.
**Geländeänderung:** Pfanne −1 m geglättet, Dünenriegel +6 m (r 45 m) auf der Wegseite (NW); Fenster 200 × 200 m.
**Assets:** „Coast & Dunes“ (A, läuft); Lücke Wabenmuster → eigene Decal-Textur (prozedural).
**Aufwand und Risiko:** mittel. Risiko: Weiß überstrahlt → `Helligkeit` der Decals 0,8.
Budget ca. 2 000 Instanzen, 4 Akteure, 10 Decals.

## wueste_06_windkanterfeld – Das Windkanter-Feld (Fundstück)

**Was man sieht:** Auf einer windoffenen Verflachung des Rippenkamms liegt ein dunkles Steinpflaster; jeder Stein ist vom Sand
dreikantig geschliffen und glänzt vom Wüstenlack. In der Mitte ein mannshoher Dreikanter.
**Vorbild:** Serir/Reg der Sahara, Dreikanter (Ventifakte) der Antarktis-Trockentäler; Spiel: Kiesebenen in AC Origins.
**Standort:** E4, X −501 / Y −939 m, Boden 107,4 m. Kammverflachung (Hang 8°, Relief 61 m) nördlich ROMAN_LOC_005 – volle
Windexposition. Weg 108 m, Stadtrand 154 m.
**Sicht:** verdeckt (0,00, 89 Wegpunkte) – liegt über allen Wegen.
**Komposition und Anmarsch:** Zugang 380 m „weich“ (6 m mit 27°) → Kehren am Kamm. `_held` 43 m östlich, Blick über das Pflaster ins
Rippenland.
**Detail-Ebenen:** Held – Dreikanter `SM_SandstoneBoulder_05` mit `MI_EL_SW_Wuestenlack`. Begleiter – `SM_namaqualand_boulder_03/04_NN`,
`SM_SandstoneBoulder_04`. Schutt 200 – `SM_namaqualand_boulder_05/06_NN`, `SM_RockSandstone_021`. Kleinzeug Tausende – Pflaster
`SM_namaqualand_rocks_01_a/c_NN`, `…stones_01_d_NN` dicht, eingeregelt (lange Achse NW–SO). Bewuchs – vereinzelte Leipoldtia-Polster.
**Wasser, Effekte, Licht:** keine.
**Geländeänderung:** keine; Bodenlage Kies/Geröll 90 %.
**Assets:** Bestand; „Wadi Rum…“ (C).
**Aufwand und Risiko:** gering. Risiko: Instanzzahl des Pflasters → 8 000 Kleinsteine als Foliage ohne Kollision.
Budget ca. 9 000 Instanzen (200 Kollision), 4 Akteure.

## wueste_07_trockenes_wadi – Das Trockene Wadi (Fundstück)

**Was man sieht:** Eine enge Flutrinne, Sohle aus rundgeschliffenem Geröll, an den Prallhängen Treibholz in Verhauen 2 m über der
Sohle – Spur der letzten Flut. Zwei Schirm-Akazien und Dornbusch, ein 4 m hoher Trockenfall mit poliertem Fels.
**Vorbild:** Wadis im Sinai / Wadi Rum; Spiel: Trockenflussbetten in RDR2, AC Origins.
**Standort:** E3, X 169 / Y −1149 m, Boden 20,5 m. Kerbtal (TPI −15 m, Relief 45 m, Geröll 39 %) kurz vor der Mündung in den
Ostbach (13 m). Weg 96 m, Stadtrand 472 m.
**Sicht:** verdeckt (0,00, 19 Wegpunkte).
**Komposition und Anmarsch:** Zugang 201 m „weich“ (Querhänge) → Trampelpfad in der Sohle. `_held` 25 m talauf, Blick zum Trockenfall.
**Detail-Ebenen:** Held – Akazien `SM_searsia_burchellii_large_NN` ×1,4, `SM_dry_oak_01_D` (flache Krone). Begleiter –
`SM_searsia_burchellii_medium_NN`, Prallhang `SM_HugeSandstoneCliff_07`, Treibholz `SM_beach_driftwood_01`. Schutt –
`SM_DryRiverBed_01/02`, `SM_stones_01_6`, `SM_namaqualand_boulder_04_NN` sortiert (grob oben, fein unten). Kleinzeug – Rinde und
Äste `SM_bark_debris_01_a_NN`, `SM_dead_quiver_branch_01_NN`, Kiesel. Bewuchs nach Ursache – Bäume nur in der Sohle (Grundwasser),
Dornbusch Didelta/Othonna an den Rändern.
**Wasser, Effekte, Licht:** kein Wasser; Spülsaum-Decals `MI_TileableLeakage_*`.
**Geländeänderung:** Trockenfall +4 m Stufe, Sohle geglättet; Fenster 120 × 100 m.
**Assets:** Bestand; „Coast & Dunes“ (B); Lücke Akazie → Searsia/Eiche.
**Aufwand und Risiko:** gering–mittel.
Budget ca. 4 000 Instanzen, 10 Akteure, 6 Decals.

## wueste_08_wabenwand – Die Wabenwand (Fundstück)

**Was man sieht:** Die Nordwand einer Küstenrippe ist von Waben durchlöchert – Hunderte Höhlungen, von Faustgröße bis zu einer
6-m-Nische, dazwischen dunkle, blauschwarz glänzende Streifen von Wüstenlack. In der größten Nische steht ein Köcherbaum im Schatten.
**Vorbild:** Tafoni der Wüstenküsten (Namib, Sinai), Wüstenlack (Utah); Spiel: Felswände in Elden Ring (Caelid-Ränder).
**Standort:** E3, X −128 / Y −1338 m, Boden 44,3 m. Nordwand einer Rippe 240 m von der Küste (Wände bis 71°) – Salzgischt + Tau
sind die Ursache der Waben. Weg 139 m, Stadtrand 451 m.
**Sicht:** verdeckt (0,00, 21 Wegpunkte).
**Komposition und Anmarsch:** Zugang 235 m „weich“ (Querhänge) → Trampelpfad. `_held` 44 m westlich, Wand im Streiflicht.
**Detail-Ebenen:** Held – `SM_MassiveSandstoneCliff_02`, `SM_HugeSandstoneCliff_05` mit Waben-Decals; Lack als dunkle
`MI_TileableLeakage`-Streifen. Begleiter – `SM_RockSandstone_040`, `SM_SandstoneBoulder_05`. Schutt – `SM_SandstoneBoulder_03`.
Bewuchs – `SM_quiver_tree_01_NN` in der Nische, Stonecrop/Eispflanze in Höhlungen.
**Wasser, Effekte, Licht:** Schatten der Nische wirkt kühl; kein Licht.
**Geländeänderung:** keine.
**Assets:** „Hollowstone Canyon (Porous Rocks Desert)“ (A für diesen Ort – nur damit echte Waben); Ersatz Decals.
**Aufwand und Risiko:** mittel; ohne Hollowstone schwach.
Budget ca. 2 000 Instanzen, 8 Akteure, 12 Decals.

## Offene Fragen an Ferat (Wüste)

- Hollowstone Canyon (Preis ungeprüft) für Wabenwand und Hoodoos – kaufen? Sonst Decal-Lösung.
- Sterndüne +22 m Geländestempel neben dem gebauten Palmental in Ordnung?

## Abgleich Inventar 13d (Stand 11.10.2026, abends)

Neues Inventar: 1 965 Netze, 116 Niagara, 85 Decals. Pfade, Maße und Paketstatus stehen in `asset_bedarf.json` → `abgleich_13d`. Orte und Kameras bleiben unverändert; die Phase-2-Planer werden gerade auf die echten Assets umgestellt.

**Jetzt erfüllt:**

- `wueste_01_yardang_flotte` – Wadi Rum (B): lange Abbrüche als Rumpfflanken: `vbvqbbofa_tier_0 (Desert_Western_Ledge_Rock_Large_03)`, `vceoferfa_tier_0 (Desert_Western_Cliff_Layered_XL_03)`, `veoneio_tier_0 (Desert_Western_Cliff_Layered_XL_01)`
- `wueste_02_sternduene` – Coast & Dunes: Rippel-Decals (A): `MI_Decal_Sand_Small_Waves`, `MI_Decal_Sand_Big_Waves`, `MI_Decal_Sand_Dry`
- `wueste_03_die_waechter` – Wadi Rum (B): Pilzkappe: `sfEby_tier_0 (Red_Sandstone_Cliff)`, `venpeg2_tier_0 (Desert_Western_Rock_Medium_12)`
- `wueste_04_quelloase` – Coast & Dunes: Nassband-Decals am Quelltopf (B): `MI_Deca_Wet`
- `wueste_05_salzpfanne` – Coast & Dunes: Strand-/Kiesel-Decals (A): `MI_Decal_Sand_Dirt`, `MI_Decal_Rocks_Small`, `MI_Decal_Sand_Dry_2`
- `wueste_06_windkanterfeld` – Wadi Rum (C): kleine Blöcke mit Schliff als Dreikanter: `pjcxN_tier_0 (Sharp_Sandstone)`, `vmjjfhh_tier_0 (Sandstone_Boulder)`, `ulqteed_tier_0 (Desert_Western_Patch_Ground_Rocky_Medium_01)`
- `wueste_07_trockenes_wadi` – Coast & Dunes: Treibholz/Spülsaum-Decals (B): `SM_beach_driftwood_02`, `SM_beach_driftwood_04`, `MI_Decal_Rocks_Small`, `MI_Decal_Rocks_Big`, `ulcceh3_tier_0 (Desert_Western_Pile_Rock_Rough_01)`, `ul4lehiga_tier_0 (Desert_Western_Pile_Rock_Small_01)`

**Ersatz → echtes Asset:**

- `wueste_03_die_waechter`: statt uldubik_tier_0 (UNVOLLSTÄNDIG angekommen – nicht verwenden) → `uk4pehu_tier_0 (Desert_Western_Cluster_Rock_Medium_06)`, `ulbwebv_tier_0 (Desert_Western_Spire_Large_05)` – Cluster_Rock_Medium_06 als Begleiter, Spire_Large_05 als gedrungener Schaft.
- `wueste_01_yardang_flotte`: statt vmnmbhv_tier_0, SM_HugeSandstoneCliff_05 als Flanken → `vbvqbbofa_tier_0 (Desert_Western_Ledge_Rock_Large_03)`, `vceoferfa_tier_0 (Desert_Western_Cliff_Layered_XL_03)`
- `wueste_04_quelloase, wueste_07_trockenes_wadi`: statt MI_Leakage_*/MI_TileableLeakage_* → `MI_Deca_Wet`, `MI_Decal_Rocks_Small`
- `wueste_07_trockenes_wadi`: statt nur SM_beach_driftwood_01 → `SM_beach_driftwood_02`, `SM_beach_driftwood_04`, `SM_beach_driftwood_08`

**Nicht verwenden (unvollständig angekommen, Ferat lädt neu):** `uldubik_tier_0 (Desert_Western_Cluster_Rock_Medium_05_uldubik)`, `uk5ebcp_tier_0 (Desert_Western_Ledge_Rock_Small_07_uk5ebcp)`

**Fehlt weiter:**

- Poröser Wüstenfels = Tafoni-Waben (Held) (wueste_08_wabenwand, wueste_03_die_waechter) – Hollowstone Canyon (B) · *nur nach Ferats OK*
- Sandfahnen am Heck/Kamm (wueste_01_yardang_flotte, wueste_02_sternduene) – Ultimate Niagara Environmental VFX (jetzt C) · *nur nach Ferats OK*
- Breite Wand (04) (wueste_08_wabenwand) – Wadi Rum Sandstone Rock 01–04 (C) – sonst Desert_Western_Cliff_Layered_XL_02 · *nur nach Ferats OK*
- Wüstenpflaster/Wadi-Schutt (wueste_03, wueste_06, wueste_07) – Megascans Desert Pack (C, Vault) – teils durch Desert Western gedeckt · *kostenlos → Claude lädt auf Wunsch*
