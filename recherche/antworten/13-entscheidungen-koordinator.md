# Auftrag 13 – Entscheidungen zu allen offenen Fragen (Koordinator)

Stand 11.10.2026, abends. Grundlage: `sehens-STATUS.md` („Noch offen“ 1–13, „Neu aus Phase 2 …“, „Neu aus 13d“), `13-sehenswuerdigkeiten-8-je-biom.md`, Rückfragen in `14-wasser-fx.md`, die Biom-Kataloge, die Planer-Regeln und das Inventar (`vorlagen/daten/netze.csv`, `inventar_extra.json`, `material_parameter.json`).
Maschinenlesbar: [`sehens/entscheidungen.json`](sehens/entscheidungen.json) (45 Einträge, je `id, biom, ort, gruppe, frage, entscheidung, planer_aenderung {datei, was}, prioritaet, pruefschritt`).

Gruppen: **(a)** Geschmack/Gestaltung → entschieden. **(b)** Editor-Faktenfrage → Arbeitsannahme + Prüfschritt für Claude lokal. **(c)** Geldfrage → ohne Kauf gebaut, ggf. Empfehlung.
Priorität: **1** vor dem nächsten Planerlauf · **2** vor dem Setzen im Editor · **3** Feinschliff/Doku.
Markierungen: **[ungeprüft]** = nicht belegt. Vorbilder aus Spielen ohne belastbare Quelle sind als solche gekennzeichnet.

## Kurzfazit – die 10 wichtigsten Entscheidungen

1. **Kein Kauf nötig.** Alles wird mit Bestand und kostenlosen Megascans gebaut. Die sechs kostenlosen Pakete und Limestone Quarry werden geladen, das Ancraite-Set wird gestrichen (E31, E32).
2. **Pivot und Schauseite werden per Skript geprüft, nicht per Auge.** Bis dahin gilt „Pivot unten Mitte, Schauseite +Y“. Das Ergebnis kommt nach `netze_masse.json`, danach laufen alle Planer neu (E35).
3. **Der Material-Fix lässt die 33 Eis- und Schnee-Netze aus.** Sie behalten `M_MS_Base_Trm` (E34).
4. **Elfentreppe ersetzt den Bestandsbach** auf 72 m. Der Wollsackfall bekommt dasselbe neue Feld `ersetzt_bestandsbach` (E10, E11).
5. **Pilzfelsen sind kreidehell mit dunklen Kappen**, nach dem Vorbild der Weißen Wüste. Dafür gibt es ein MI auf `M_MS_Base`; die Füße kommen nur noch aus `ulbwebv_tier_0` (E01).
6. **Nebel gibt es nur als `lokaler_nebel`**, ohne FogBank-Blueprints. Bewegte Fetzen kommen als Niagara-Kopie (E06, E07).
7. **Irrlichter bleiben mit Licht, aber sichtbar:** 40 bzw. 30 cd statt 2 bzw. 1,5 cd (E08).
8. **Tiere:** keine Tier-Modelle. Erlaubt sind die ferne Vogelwolke als Partikelpunkte und Ameisen am Ameisenhaufen. Die Fischgräten fliegen aus dem Katalog (E03, E04, E05).
9. **Niagara-Kopien statt Originale:** Dampfsäule, Fumarole, Gasflammen und Schlammblasen werden als `NS_EL_SW_*` mit Feld `kopie_von` angelegt (E14, E15, E45).
10. **Wasser-FX:** Der Cull der Heldenfälle (150/100/60 m) ist freigegeben, mit einer Messschranke bei 0,5 ms. S02 bekommt nur dann einen Impact, wenn das Budget von 6 hält (E27, E28).

Weitere Punkte im Einzelnen:
- Die Wabenwand wird ohne Hollowstone gebaut: Decals plus eine Probe mit Lavawand-Modulen in Sandsteintönung (E30).
- Der Gletschersteig darf über flaches Eis führen (E22).
- Der Canyonsteig bleibt Reserve (E25).
- Die Wüste erreicht damit genau 6/6 Material-Instanzen.

## Entscheidungen

| Nr | Frage | Entscheidung | Vorbild (real/Spiel, Link) | Umsetzung (Biom/Ort, Asset/Wert, Planer) | Prüfschritt Claude lokal (nur b) |
|---|---|---|---|---|---|
| E01 | (a) Pilzfelsen wueste_03: weiß oder gebändert? | **Kreidehell, Bänder nur gedämpft, dunkle Kappen bleiben.** Grenzt die „Wächter“ klar von den gebänderten Hoodoos (canyon_05) ab, die dieselben Spire-Netze nutzen. | **Weiße Wüste, Farafra (Ägypten):** Kreidefelsen, vom Wind zu Pilzformen geschliffen, teils zweigeschossig hoch ([Wikipedia](https://en.wikipedia.org/wiki/White_Desert_National_Park)). Das trägt „weiß + gedrungen + Hohlkehle“. | wueste_03. Neues MI `MI_EL_SW_Waechter_Kreide`, basis `M_MS_Base` (hat `Saturation`, `Brightness`, `BaseColor Tint` laut `material_parameter.json`): Saturation 0,25, Brightness 1,35, Contrast 0,9, Tint (0,97/0,95/0,90). Füße nur `ulbwebv_tier_0` (Spire_Large_05, 8,4 × 8,5 × 11,8 m, gedrungen), `vepoda2_tier_0` entfällt. Kappen `SM_RockSandstone_040` mit `MI_EL_SW_Wuestenlack` bleiben. Wüste danach 5/6 MI. **Planer wueste.** Textur-Namen des Fab-MI von ulbwebv liest Claude lokal ab. | – |
| E02 | (a) Guano-Wand der Vogelinsel im Osten? | **Ja, Ostflanke.** Guano folgt den Brutsimsen, nicht dem Kompass, und alle Kameras stehen im Osten. | **Bass Rock (Schottland):** 120 m Steilwände, weiß durch Basstölpel und Kot; die Seabird-Centre-Leitung sagt, das Weiß komme vor allem von den Vögeln selbst ([Atlas Obscura](https://www.atlasobscura.com/places/bass-rock)). Weiß gehört also dorthin, wo die Brutsimse sind. | kueste_02 bleibt wie gebaut. Nur `sehens/kueste/katalog.md`: „West“ → „Ost“. | – |
| E03 | (a) Vogelwolke `NS_feather` behalten? | **Ja, nur als ferne Punkte** 35–60 m über der Brutwand, nie in Spielernähe. | Bass Rock (wie E02): Die Kolonie ist von weitem als wirbelnde weiße Punkte lesbar. Skellige (Witcher 3) zeigt Meerestiere als ferne Umgebungsanimation [Forenaussage, [Steam](https://steamcommunity.com/app/292030/discussions/0/1353742967813411950)]. | kueste_02: `NS_feather` optional → false, hoehe_m 35 → 45, Hinweis „offene Frage 8“ ersetzen. **Planer kueste.** | – |
| E04 | (a) Tiere (Fische, Ameisen, Vögel) mit „nur Landschaft“? | **Keine Tier-Modelle, die sich durch den Raum bewegen.** Im Inventar gibt es kein Vogel- oder Fischnetz. Erlaubt sind Ameisen auf dem Haufen (`SM_anthill_ants_anim_random`, Teil des Bodens) und E03. | Wie E03: Ferne Andeutung statt Kreatur. | bergwald_08: Gruppe `ameisen` aktiv → true. Den Satz „Tiere bleiben aus (offene Frage 8)“ in den `_doku` von aue/sumpf aktualisieren. **Planer bergwald, aue, sumpf (Doku).** | – |
| E05 | (a) Reiherhorst: „Federn und Fischgräten“ im Katalog | **Fischgräten streichen** (Knochen-Regel). Federn (sehr spärlich) und gekalkter Boden bleiben. | – (Ferats Linie) | `sehens/sumpf/katalog.md`. Der Planer enthält keine Gräten. | – |
| E06 | (a) Nebel: FogBank-Akteure oder nur `lokaler_nebel`? | **Nur `lokaler_nebel`** (≤ 2 je Ort). `BP_FogBankCard/Volume` stammen aus einem Effekt-Demo-Paket, und SEHENS_FORMAT kennt keinen Blueprint-Akteur. Ein neuer Typ wäre ein Umbau am Setzer. | Epic: Local Fog Volume = kugelförmiger, radial auslaufender Nebel, ergänzt den Höhennebel und skaliert auf allen Plattformen ([Epic-Doku](https://dev.epicgames.com/documentation/en-us/unreal-engine/local-fog-volumes-in-unreal-engine)). | Alle Biome unverändert. elfenwald_02: Hinweis „falls Ferat Blueprints setzt“ entfernen. **Planer elfenwald.** | – |
| E07 | (a) Nebelhain: FogBankCard oder 2 lokale Nebel? | **2 lokale Nebel bleiben** (Kronenwolke, Gratkrone). Dazu optional 1 Niagara-Kopie `NS_EL_SW_Nebelfetzen`. | **Fanal (Madeira):** Lorbeer-Altbäume, die regelmäßig in Wolke stehen ([My Modern Met](https://mymodernmet.com/fanal-forest-albert-dros/)); Wistman's Wood, Dartmoor ([Bitesized Britain](https://www.bitesizedbritain.co.uk/this-mystical-stunted-oak-wood-in-dartmoor-in-devon/)). Der Nebel steht in den Kronen, nicht am Boden. | elfenwald_02: `effekte +=` Niagara `NS_EL_SW_Nebelfetzen` (kopie_von `/Game/NiagaraExamples/FX_Smoke/NS_Smoke_Plume`): Auftrieb 0, Drift 0,3 m/s, Sprites 6–10 m, Alpha 0,15, Farbe (0,90/0,92/0,93), Lebensdauer 20 s, Cull 120 m, hoehe_m 12, optional. **Planer elfenwald.** | – |
| E08 | (a) Irrlichter mit Lichtern oder nur Nebel? | **Mit Lichtern, aber sichtbar:** 40 cd und 30 cd, Radius 5 m, kein Schatten, gelbgrün. 2 cd wären bei fester Tagsonne unsichtbar. Bleibt unter den Leuchtpilzen des Elfenwalds (180–300 cd). | Irrlicht-Folklore: Lichter über Mooren, die erscheinen und verlöschen ([Phipps](https://www.phipps.conservatory.org/blog/detail/biopgh-blog-will-o-the-wisps-the-haunt-of-the-swamp)). Velens Sümpfe (Witcher 3) leben von Nebel und Unheimlichkeit ([Consolepulse](https://consolepulse.com/multiplatform/the-witcher/guides/the-witcher-3-velen-explained)); Bayou Nwa/Lagras (RDR2) als stehendes Dunkelwasser ([Fandom](https://reddead.fandom.com/wiki/Bayou_Nwa)). | sumpf_08: punktlicht glimm_a 2 → 40 cd, glimm_b 1,5 → 30 cd, radius 4 → 5 m. `NS_Sparkling_Glow` ×2 und die Nebelbank bleiben (3 Effekte vom Typ Licht/Niagara sind im Rahmen). **Planer sumpf.** | – |
| E09 | (a) Sumpf-See stellenweise `schwarz_spiegel`? | **Nein.** Der Epic-See `T_2954_391` bleibt einheitlich: ein Wasserkörper hat ein Material, und Teilfärbung bräuchte überlappende Körper. Schwarzspiegel gibt es an eigenen Körpern: sumpf_04 (3 Augen), heide_04 (Kolk), dschungel_06 (Strudeltopf). | **Okefenokee:** Gerbstoffe machen das Wasser teefarben; dunkle, stille Flächen spiegeln ([Science News Explores](https://www.snexplores.org/article/okefenokee-swamp-ecology-climate)). Das wirkt in kleinen, ruhigen Augen stärker als auf dem großen See. | Keine Planeränderung; Satz im `skripte/sehens_sumpf/README.md`. | – |
| E10 | (a) Elfentreppe: Bestandsbach ersetzen? | **Ja.** `B_R_P4_M1_01` wird auf der Linie `treppe` von s 0 bis 72 m ausgeblendet. Die 5 Tuffbecken mit ihren Stufenbächen ersetzen ihn, oben und unten schließt der Bestand an. | **Plitvice:** Kalktuff-Barrieren (Moos, Algen fällen Kalk), die Seen zu Kaskaden stauen ([Nationalpark](https://np-plitvicka-jezera.hr/en/natural-and-cultural-heritage/natural-heritage/tufa/)). **Krka, Skradinski buk:** 17 Kaskaden ([Amusing Planet](https://www.amusingplanet.com/2014/05/skradinski-buk-in-croatia.html)). Ein durchlaufender Bach durch die Becken würde die Stufen zerstören. | elfenwald_04: neues Feld `ersetzt_bestandsbach = {id, von, bis}`. `sehens_lib/rezept.py` schreibt daraus `bestand_ausblenden` in `orte.json`; das Feld wird einmal für E10/E11/E39 definiert. **Planer elfenwald + Lib.** | – |
| E11 | (a) Wollsackfall: Fundstück oder Leuchtfeuer? | **Fundstück bleibt.** Die 15 von 124 Wegpunkten sehen nur Glanz zwischen Bäumen; das ist der Lockruf (der Marker-Text arbeitet mit dem Rauschen). | **Becky Falls, Dartmoor:** ~20 m über Granitblöcke in altem Wald, von der Straße nicht zu sehen ([Wikipedia](https://en.wikipedia.org/wiki/Becky_Falls)). | heide_06: Feld `ersetzt_bestandsbach = {id: B_R2_R_P3_P0_01, von: p0, bis: p3}` statt nur Hinweis. **Planer heide.** | – |
| E12 | (a) Gelb getönter Sanddorn als Ginster? | **Ja.** Silhouette (dorniger, dichter Busch) und Farbe (`MI_EL_SW_Ginstergold`) tragen. | **Dartmoor:** Im August/September färben Westlicher Ginster und Heide die Granit-Tors gelb und lila ([Ordnance Survey](https://getoutside.ordnancesurvey.co.uk/guides/explore-dartmoor-national-park)). | heide_02 unverändert; die Frage im README streichen. | – |
| E13 | (a) `MI_EL_SW_Russ_Decal` anlegen? | **Ja**, wie Brutröhren (aue) und Salzkruste (wueste). Ein natürlicher Heidebrand, aus dem Ginster austreibt. | – (projektinterne Linie: eigene prozedurale Decals) | heide_02: Decal optional → false, sobald das MI angelegt ist (Heide 6/6). **Planer heide.** | – |
| E14 | (a) Dampfsäule als weiße Kopie von `FX_Smoke_Volcano_01`? | **Ja:** `NS_EL_SW_Dampfsaeule`, Farbe (0,95/0,94/0,90), Deckkraft ×0,5, Spawn ×0,5. Die Fumarolenfahne als `NS_EL_SW_Fumarole` (aus `FX_Lava_Smoke_03`). | **Hverir/Námafjall (Island):** Fumarolen und Schlammtöpfe stoßen fast reinen Dampf aus, weiß statt aschgrau ([Campervan Iceland](https://www.campervaniceland.com/blog/things-to-do/hverir)); Dampf über heißen Quellen in Yellowstone ([SummitPost](https://summitpost.org/grand-prismatic-spring/516255/c-516255)). | lava_02: asset → `NS_EL_SW_Dampfsaeule` (kopie_von). lava_02 und lava_06: `FX_Lava_Smoke_03` → `NS_EL_SW_Fumarole`. **Planer lava.** | – |
| E15 | (a) Kopien `NS_Fire`/`NS_Bubble_Burst` mit kleinen, langsamen Partikeln? | **Ja:** `NS_EL_SW_Gasflammen` (Flammen 0,3–0,8 m, viele Quellen auf r 12 m, ohne Funken) und `NS_EL_SW_Schlammblasen` (schlammgrau 0,35/0,32/0,28, Größe ×0,5, Spawn ×0,4). | **Yanartaş (Türkei):** Erdgas brennt seit Jahrtausenden in vielen kleinen Flammen aus Felsritzen ([CNN](https://edition.cnn.com/travel/yanartas-turkey-burning-rocks-chimaera)). Darvaza nur als Bildvorbild für den Krater, weil dort ein Bohrunfall der Ursprung ist ([Smithsonian](https://www.smithsonianmag.com/travel/giant-hole-ground-has-been-fire-more-40-years-180951247/)). Schlammtöpfe Hverir (s. E14). | oedland_03: `NS_Fire` → `NS_EL_SW_Gasflammen`. oedland_06: `NS_Bubble_Burst` ×2 → `NS_EL_SW_Schlammblasen`. **Planer oedland.** | – |
| E16 | (a) `MI_EL_SW_Basalt_Saeule` mit Basalt-Texturen? | **Ja.** Das Paket ist gekauft; die Nordklippen-Textur wäre granitisch und verwischt die Säulenkanten. | **Svartifoss (Skaftafell):** schwarze Säulen wie Orgelpfeifen, Bruchstücke am Fuß ([Iceland Travel Guide](https://icelandtravelguide.is/locations/svartifoss-waterfall)). | lava (MI): texturen = Albedo/Normal/ORM aus `/Game/Basalt`. Bei verschiedenen Textursätzen gilt das MI nur für die Pillars-Netze. **Planer lava.** | Material-Slots von `Basalt_Basalt_Pillars_Wall_SM` und `Basalt_Basalt_Cliff_SM` auslesen. Ein Satz → MI für alle 5; zwei → nur Pillars. |
| E17 | (a) Gipfelsteig mit dem Serpentinen-Werkzeug neu? | **Ja.** Das Bodenband aus Phase 1 ist nur ein Platzhalter. | **Bright Angel Trail:** Kehren folgen einer Bruchlinie, steile Abschnitte (Jacob's Ladder) bis ~15 % ([Sunset](https://sunset.com/travel/national-parks/bright-angel-trail)). | `lava_pfad_gipfelsteig` → neue Punktliste in `sehens/lava/standorte.json`. **Planer lava** (liest die neuen Punkte). | – |
| E18 | (c) Lava: Klangpaket Wind/Laub oder stumm? | **Ohne Kauf.** Der Wind-Cue bleibt an lava_01/06/07 (0,3–0,4), aber nur, wenn das Laub kaum hörbar ist; sonst dort stumm. | – | **Planer lava:** Bedingung am Klang-Eintrag. | Cue `CUE_Wind_Autumn_wind_with_leaves_rustling_Cue` anhören; Laub deutlich → an den drei Orten streichen. |
| E19 | (a) Tundra-Pfad streift ROMAN_LOC_018? | **Erlaubt.** Die 150-m-Regel gilt für Orte, nicht für Pfade; die Stadtfläche selbst wird nicht berührt. | – | `sehens/tundra/standorte.json`: `warnung_akzeptiert` am Pfad. | Nach dem Bau der Stadt: Pfadanfang schneidet kein Gebäude, sonst Start 30–40 m nach Westen. |
| E20 | (a) Aufeis/Thermokarst neben Frost/Gletscher (dazu A14-Rückfrage 1) | **Aufeis entfällt** (C2-Kaskade hat Vorrang; das Schneetälchen ist in Arbeit). **Thermokarstsee bleibt**, weil sich tauender Boden mit kippenden Bäumen klar vom Toteisloch und vom Frostsee abhebt. | – (Katalog-Vorbild unverändert) | Tundra-Katalog: Frage 1 streichen. | – |
| E21 | (a) Steinringe Fundstück oder Leuchtfeuer? 4/4 ok? | **Fundstück bleibt, 4/4 bleibt.** Ringe sind flach und lesen sich nur von oben. Der Teilblick vom höheren Weg ist ein Hinweis. | **Kvadehuksletta (Svalbard):** sortierte Ringe 0,5–5 m, Steinränder bis 0,5 m hoch ([Polar Research](https://polarresearch.net/index.php/polar/article/download/2361/5611)). | Tundra-Katalog: Fragen 2/3 streichen. | – |
| E22 | (a) Steig über Gletschereis? | **Ja, nur über flaches Eis** (≤ 12°), als Spur ohne Bauwerk: Bodenband Schnee/Kies (Schmutzband, Mittelmoräne), keine Stufen, keine Seile, mindestens 15 m vom Bergschrund. | **Falljökull (Skaftafell):** Geführte Gletscherwanderungen für Anfänger führen über die flache Zunge ([Manawa](https://manawa.com/en/book/28694)). | gletscher: `gletscher_pfad_nordhang` in `standorte.json` + **Planer gletscher** (Bodenband, Abstand). | – |
| E23 | (b) Houdini-Reste K7, K13, K9 ausblenden? | **Ja.** K7/K13 sind schon als `freiraeume` geplant. K9 wird nur unter den neuen Pfeilern ausgeblendet (kueste_01, kueste_03). | – | **Planer kueste:** `freiraeume` mit Rolle houdini, Netznamen nach Befund. | Im Outliner nach „K9“/„K13“ filtern, Namen und Lage notieren. Bilder `kueste_01_die_alten_fern`, `frost_02_frostsee_held` mit/ohne. |
| E24 | (a) Wasserfälle > 150 m Fallhöhe? | **Ja**, steht so schon im Fjord-Planer. Der Vorhang trägt die Höhe, Niagara sitzt nur an Lippe und Fuß. | **Sju Søstre, Geirangerfjord:** ~410 m gesamt, längster Freifall ~250 m ([World of Waterfalls](https://www.world-of-waterfalls.com/norway-seven-sisters.html)). | Keine Änderung; STATUS-Frage 5 erledigt. | – |
| E25 | (a) Canyonsteig? | **Nicht jetzt, als Reserve.** Der Canyon hat 8 Orte bei 0 Fehlern. Fällt ein Ort im Editorbild durch, ersetzt ihn ein Ort am Mündungsfall (X −1610 / Y −1090) über einen Randsteig vom Burgweg ROMAN_LOC_003. | Bright Angel Trail (s. E17); Steig am Fels entlang statt durch das Wasser. | `sehens/canyon/katalog.md`: Vermerk „Reserve (E25)“. | – |
| E26 | (a) Brandungsgrotte fjord_07 tauschen? | **Bleibt im Fjord.** Die Küste hat keine Grotte, also gibt es keine Doppelung. | – | `sehens/fjord/katalog.md`: „Tauschkandidat“ streichen. | – |
| E27 | (b) Cull der Heldenfälle 150/100 m? | **Freigegeben mit Messschranke:** Fall 150, Impact 100, Wake 60 m. Über 0,5 ms GPU für Wasser-FX gilt die Rückfallstufe 100/60/40 m. Dieselbe Klasse gilt für kueste_04 und dschungel_02. | Epic: Effect Type mit `cull_by_distance`/`max_distance`; Instanz-Cull ohne Significance-Handler nur beim Spawnen ([Python-API](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/NiagaraSystemScalabilitySettings)). | `wasser_fx/plan.json`: `rueckfall_cull_m`. | `stat Niagara` + `profilegpu` bei `WASSER3_H4_WF_K8_weit` und `kueste_04_der_seefall_held`; Wert in `plan.json → messung`. |
| E28 | (b) S02 ohne Niagara – 7. Impact? | **Budget bleibt 6.** S02 bekommt `NS_Impact_Small` mit Cull 20 m nur, wenn `plan_pruefen.py` ≤ 6 gleichzeitig meldet; sonst bleiben Vorhang und Schaumscheibe. | – | `wasser_fx/plan_erzeugen.py`: C2_B += S02 (optional). | `plan_pruefen.py` laufen lassen, Ergebnis in Antwort 14 nachtragen. |
| E29 | (c) Klangpakete (Tosen, Brandung, Seevögel, Höhle) | **Ohne Kauf:** Tosen aus zwei geschichteten Cues (IX + IV, Pitch 0,6–0,7, versetzt). Brandung zuerst mit dem kostenlosen MetaSound „Procedural Sea Waves“ testen (prozedural, ohne Audiodateien; „free“ laut Fab-Kategorieauszug [ungeprüft]). Höhlen mit `CUE_Rain_Dropping…` leise. Seevögel bleiben eine Lücke. | [Fab-Listing Procedural Sea Waves](https://www.fab.com/listings/2b11f781-970a-4c37-9ab2-90d16137555f), [Fab-Kategorie Ocean](https://www.fab.com/category/audio/ambient-sounds--ocean). | `sehens-downloadliste.md` (C, kostenlos). **Planer kueste:** zweite Klangquelle optional. | – |
| E30 | (c) Hollowstone für die Wabenwand kaufen? | **Jetzt nicht.** Decals wie geplant plus Probe: `SM_lava_wall_04` (3,1 × 3,3 × 4,4 m) und `SM_lava_wall_09` in Sandsteintönung als Wabennischen im Schattenteil. Kauf erst, wenn die Probe im Bild nicht trägt. | **Tafoni/Wabenverwitterung:** Salz in trockenen Küsten- und Wüstenlagen höhlt Sandstein, Nischen vertiefen sich selbst ([Wikipedia](https://en.wikipedia.org/wiki/Honeycomb_weathering)). Die Blasenhohlräume der Lavawand ahmen das im Maßstab nach [Annahme, Bild entscheidet]. | wueste_08: MI `MI_EL_SW_Wabenfels` (`M_EL_Fels_MS`, Toenung 0,78/0,60/0,45, Helligkeit 0,9) → Wüste 6/6. Gruppe `wabennischen` (4 Akteure, 3–5 m, optional). **Planer wueste.** | – |
| E31 | (c) Limestone laden? Ancraite-Link? | **Megascans Limestone Quarry laden** (5 Quarry Cliffs + Rocks/Rubble/Slab, kostenlos, Ferat lädt). **Ancraite streichen** (kein Treffer). | – | `sehens-downloadliste.md`. **Planer dschungel** (+aue_07): Quarry-Paletten optional, Ersatz `SM_Cliff_01*`. | – |
| E32 | (c) 6 kostenlose Pakete mitladen? | **Ja, alle sechs.** Electric Dreams lädt Claude lokal; die Megascans lädt Ferat (vorher Besitz prüfen). | – | Downloadliste-Status; danach Inventar neu, `asset_bedarf.json` abgleichen. | – |
| E33 | (b) uldubik/uk5ebcp neu laden, fehlgeschlagene IDs? | **Neu laden.** Bis dahin bleiben die Ersatznetze. | – | Downloadliste „Erneut versuchen“; Sperre aufheben bei 5/5 Dateien. | Beide Netze im Fab-Fenster neu laden, Dateien zählen, Log nach `61882812-…`/`6676d940-…` durchsuchen. |
| E34 | (b) Eis-Netze behalten `M_MS_Base_Trm`? | **Ja (Arbeitsannahme).** Der Material-Fix für `sw_*` lässt die 33 Eis/Schnee-Megascans aus. | – | `sehens_lib/inventar.py`: `material_fix_ausnahmen` in `orte.json`. | Im Material-Fix-Skript prüfen, ob `M_MS_Base_Trm`-Netze übersprungen werden; ein Eisnetz in gletscher_01 mit dem Original vergleichen. |
| E35 | (b) Pivot/Schauseite (Klippenschalen, Basalt, Mountain, lava_wall, Desert Western, Eisklippen, Cliff_01*, HugeMossyForestCliff, stones_roots, Lehm/Kalkwand) | **Arbeitsannahme: Pivot unten Mitte, Schauseite +Y.** Geprüft wird per Skript; das Ergebnis geht nach `netze_masse.json`, danach alle Planer neu. | – | `sehens_lib/inventar.py`: Felder `pivot_z_anteil`, `pivot_xy_versatz_m`, `front_achse`; Planer lesen `front_achse` vorrangig von dort. **Alle Planer** (nur neu laufen). | Unreal-Python `StaticMesh.get_bounding_box()`: min.z ≈ 0 und Mitte xy ≈ 0 → „unten Mitte“, sonst Versatz. Schauseite: 4-Seiten-Bild je Netz in einer Testkarte. Reihenfolge: Mondtor `_fern`, Sonnenfenster, Schwarze Mauer, Eiswand. |
| E36 | (b) Nadeltor-Sturz Unterseite, Klippenschalen | **Arbeitsannahme: geschlossene Unterseite.** Bei Loch: Sturz 180° um die Längsachse drehen oder eine zweite Schale (Skala 0,9) darunter. | – | **Planer kueste** (nur bei Befund). | Kamera im Torgang, Augenhöhe, Blick nach oben. |
| E37 | (b) Mondarm-Spiegel 14,2 m? | **Arbeitsannahme 14,2 m.** Bei Abweichung > 0,3 m wird der Wert im Planer ersetzt. | – | **Planer aue** (nur bei Befund). | Z der Wasseroberfläche des Mondarm-WaterBody ablesen. |
| E38 | (b) Reiherhorste, Blattkarten der Graveyard-Totbäume | **Arbeitsannahme: ohne Blattkarten.** Grüne Karten → `MI_EL_SW_Silberholz` ohne Blattslot oder `SM_EuropeanBeech_Dead_XL_01`. | – | **Planer sumpf** (nur bei Befund). | Bild `sumpf_03_der_reiherhorst_nah`, Material-Slots auflisten. |
| E39 | (b) Schluckhöhle: Wasser läuft nach Süden weiter? | **Arbeitsannahme: nein.** Falls doch: `ersetzt_bestandsbach` wie E10. | – | **Planer dschungel** (nur bei Befund). | Bild `dschungel_06_schluckhoehle_nah` + Kamera 30 m südlich des Portals. |
| E40 | (b) `SM_lava_disc` mit Glut-Material? Pivot `SM_lava_wall_*`? | **Arbeitsannahme: eine Instanz von `M_NM_Master_Lava_Material`.** Sonst setzt der Planer das Lava-MI des Sets. Pivot über E35. | – | **Planer lava** (nur bei Befund). | `SM_lava_disc` öffnen, Slot 0 ablesen; leuchtet es im Schachtschatten? |
| E41 | (b) Wollsackfall-Stufen im 1-m-Lauf | **Arbeitsannahme: 2 × ~1,1 m + Fall3.** Jede Stufe muss > 0,8 m bleiben, sonst vertieft der Stempel. | – | **Planer heide** (nur bei Befund). | 1-m-Lauf, Stufenhöhen aus `orte.json`. |
| E42 | (b) Karsee ±9 m im 1-m-Lauf | **Arbeitsannahme ±9 m.** Ufer rundum über dem Spiegel. | – | **Planer bergwald** (nur bei Befund). | 1-m-Lauf; Prüfer „Ufer unter Spiegel“ = 0. |
| E43 | (b) Pfad `M_River_Water_Translucent`; Coast-&-Dunes-„Stempel“ | **Arbeitsannahme:** Vorhänge immer `M_EL_Wasserfall2`, Bäche `M_River_Water_Translucent` (Mountain-Set). Dünen entstehen aus unseren Geländestempeln. | – | `sehens_lib/inventar.py`: vollen Pfad eintragen; `material_hinweis` in elfenwald/heide/kueste. | Content Browser: `M_River_Water_Translucent`, im Coast_Dunes-Ordner nach „Stamp“/„Brush“ suchen. |
| E44 | (b) `SM_lava_wall_01–09` zurück? | **Erledigt** (Inventar 13d, 1,7–6,8 m). | – | STATUS Punkt 2 als erledigt markieren. | Pivot über E35. |
| E45 | (a) Niagara-Kopien: Namen, Ablage | **`/Game/Eldarien/Welt/FX/Sehens/NS_EL_SW_<Name>`**, Originale bleiben unberührt. Planer schreiben `kopie_von`. | – | `sehens_lib/rezept.py`: `kopie_von` durchreichen; Prüfer: Präfix `NS_EL_SW_` verlangt `kopie_von`. **Lib.** | – |

### Was die Planer ändern müssen (nach Biom)

- **Lib (`sehens_lib`)** (vor allen Biomen, Prio 1):
  - Feld `ersetzt_bestandsbach` → `bestand_ausblenden` (E10)
  - `material_fix_ausnahmen` (E34)
  - Pivot- und Front-Felder aus `netze_masse.json` (E35)
  - `kopie_von` (E45)
  - Pfad von `M_River_Water_Translucent` (E43)
- **elfenwald:** Elfentreppe ersetzt den Bestandsbach (E10); FogBank-Hinweis raus (E06); optional Nebelfetzen (E07).
- **heide:** Feld `ersetzt_bestandsbach` am Wollsackfall (E11); Ruß-Decal fest einplanen, sobald das MI da ist (E13).
- **wueste:**
  - `MI_EL_SW_Waechter_Kreide` + Füße nur `ulbwebv_tier_0` (E01)
  - `MI_EL_SW_Wabenfels` + Gruppe `wabennischen` (E30) → 6/6 MI
- **kueste:** NS_feather fest, Höhe 45 m (E03); K9-Freiräume (E23); zweite Brandungs-Klangquelle optional (E29); Katalog „Ost“ (E02).
- **sumpf:** Irrlicht-Lichter 40/30 cd, Radius 5 m (E08); README-Satz Seefarbe (E09); Katalog ohne Fischgräten (E05).
- **lava:**
  - Dampfsäule und Fumarole als Kopien (E14)
  - Basalt-Texturen im MI (E16)
  - Gipfelsteig-Punkte neu (E17)
  - Wind-Cue mit Bedingung (E18)
- **oedland:** Gasflammen- und Schlammblasen-Kopien (E15).
- **bergwald:** Ameisen aktiv (E04).
- **gletscher:** Nordhang-Spur über Eis mit Schnee/Kies-Band, ≤ 12°, ≥ 15 m vom Bergschrund (E22).
- **tundra:** `warnung_akzeptiert` am Pfad (E19); Katalogfragen 1–3 streichen (E20, E21).
- **canyon, fjord, dschungel, aue, frost:** nur Katalog-Vermerke (E25, E26) bzw. Änderungen nur bei Befund (E36–E42).
- **wasser_fx (Auftrag 14):** Rückfall-Cull (E27); S02 optional (E28).
- **Downloadliste:** Limestone laden, Ancraite streichen (E31); 6 kostenlose Pakete laden (E32); Procedural Sea Waves (E29); Neuladen uldubik/uk5ebcp (E33).

## Empfehlungen zum Kauf (Ferats Geld, nicht entschieden)

Alles oben funktioniert ohne Kauf. Diese Käufe würden eine echte Lücke schließen, die Megascans und der Bestand nicht füllen. Sie stehen nach Nutzen je Euro sortiert.

1. **Cave Ambience** (Gravity Sound): 27 Höhlenloops à ~1 min.
   - **9,99 USD auf itch.io** ([itch.io](https://gravity-sound.itch.io/cave-ambience)); Fab-Preis [ungeprüft] ([Fab](https://www.fab.com/listings/0cdc50ee-2c20-45d1-b35d-c158fb9fa013)).
   - Grund: 6 Höhlen- und Schlundorte haben heute nur den Tropfen-Cue (dschungel_06/08, fjord_07, gletscher_01, lava_04, oedland_08). Megascans hat keine Klänge.
   - Kleinster Betrag mit spürbarer Wirkung.
2. **Hollowstone Canyon:** 23 Nanite-Felsen mit 4K-Texturen, poröse Wüstenfelsen ([Fab](https://www.fab.com/listings/67f820de-2119-4948-8acb-5f36ec31d1d5)). **Preis [ungeprüft].**
   - Nur kaufen, wenn die Lavawand-Probe (E30) im Editorbild nicht als Wabenwand trägt.
   - Megascans hat keine Tafoni-Wand (nur „Icelandic Porous Rock“, 0,24 m).
3. **Fantasy Ambiences** (Lava, Höhle, Wind): **ca. 74,99 USD** laut Downloadliste (Gumroad/itch), Fab-Preis [ungeprüft].
   - Erst nach Hörproben, und nur, wenn nach E18/E29 die Lava- und Windorte zu still wirken.
   - Ersetzt Punkt 1 teilweise; nicht beide kaufen, ohne gehört zu haben.
4. **CryoGen** (prozedurales Eis, C++-Plugin) ([Fab](https://www.fab.com/listings/1758130d-aa4e-4b26-ae97-fb5f43a2c22b)): **Preis [ungeprüft].**
   - Erst prüfen, wenn Eisfall, Eisvorhang, Frostblumen und Glockenbach aus `SM_EISZAPFEN_*` + `MI_EL_SW_Spritzeis` im Bild nicht tragen.

**Nicht empfohlen** (Bestand oder Megascans gleichwertig):
- Arctic Cliffs, Wadi Rum, Procedural Rocks Generator
- Ultimate Niagara Environmental VFX, Niagara VFX Pack Snow
- Giant Fantasy Mushrooms (Stilrisiko), Travertine Terraces (die Elfentreppe trägt mit Tuff-Stempel + MI)
- Tropen-Pakete (erst Electric Dreams), Bald Cypress
- Imposing Dead Quercus Robur, Moss & Lichen

## Bleibt bei Ferat

- **Jeder Kauf** aus dem Abschnitt oben. Das ist eine Geldentscheidung, keine Gestaltungsfrage.
- **Megascans-Downloads aus seinem Fab-Konto** (Limestone Quarry, European Black Alder, Icelandic Sand, Tundra Icelandic Rock Cluster, Desert Pack, Sandstone, Driftwood, English Oak). Entschieden ist hier nichts mehr offen; es ist nur eine Handlung, die nur Ferat ausführen kann.

## Quellen

Alle Links stehen in der Tabelle bei der jeweiligen Entscheidung. Projektintern:
- `vorlagen/SEHENS_FORMAT.md` §5–§9 (Wasserfarben, Effekttypen, Budgets)
- `vorlagen/daten/material_parameter.json` (Parameter von `M_MS_Base`, `M_EL_Fels_MS`)
- `vorlagen/daten/netze.csv` (Maße `ulbwebv_tier_0`, `SM_lava_wall_*`)
- `vorlagen/daten/inventar_extra.json` (Niagara-Pfade, keine Tier-Netze, kein Wasserfall-Cue)
- `14-wasser-fx.md` §3, §4, §7
- `sehens-downloadliste.md` (Preise Fantasy Ambiences, Megascans-Prüfung)

Seiten von fab.com waren nur über Suchauszüge erreichbar. Fab-Preise sind deshalb [ungeprüft].
