# Sehenswürdigkeiten – Gesamtkatalog (Auftrag 13, Phase 1, Teil B)

Stand 11.10.2026. **120 Orte in 15 Biomen** (je 8): 48 Leuchtfeuer, 72 Fundstücke, 19 neue Pfade. Nur Landschaft (Fels, Wasser, Eis, Feuer, Pflanzen) – keine Bauten, Ruinen, Knochen oder Menschenspuren, keine Houdini-`SW_*`-Assets.

Prüfer `skripte/sehens_lib/sehens_pruefen.py` über alle Biome (Wege + Pfade): **0 FEHLER**, 1 WARNUNG (Pfad zum Trunkenen Grund streift den Rand der geplanten Stadt ROMAN_LOC_018).

Details je Ort (Was man sieht, Geologie, Held, Kameras, Sicht- und Wegnachweis, Bedarf) im jeweiligen `sehens/<biom>/katalog.md`; Daten in `sehens/<biom>/standorte.json`; alle Orte als Punktliste in `sehens/marker.json`.

Alle 120 Orte liegen 80–300 m vom nächsten Weg oder neuen Pfad (Spalte „nächster Weg/Pfad“, gerechnet mit `gelaende.abstand_weg` inkl. aller `pfade`).

## Übersicht

| Biom | Orte | Leuchtfeuer | Fundstücke | neue Pfade | Katalog |
|---|---|---|---|---|---|
| aue | 8 | 3 | 5 | 0 | [katalog.md](sehens/aue/katalog.md) |
| bergwald | 8 | 3 | 5 | 0 | [katalog.md](sehens/bergwald/katalog.md) |
| elfenwald | 8 | 3 | 5 | 0 | [katalog.md](sehens/elfenwald/katalog.md) |
| dschungel | 8 | 3 | 5 | 0 | [katalog.md](sehens/dschungel/katalog.md) |
| lava | 8 | 4 | 4 | 3 | [katalog.md](sehens/lava/katalog.md) |
| gletscher | 8 | 3 | 5 | 3 | [katalog.md](sehens/gletscher/katalog.md) |
| frost | 8 | 3 | 5 | 2 | [katalog.md](sehens/frost/katalog.md) |
| fjord | 8 | 3 | 5 | 2 | [katalog.md](sehens/fjord/katalog.md) |
| tundra | 8 | 4 | 4 | 4 | [katalog.md](sehens/tundra/katalog.md) |
| heide | 8 | 3 | 5 | 0 | [katalog.md](sehens/heide/katalog.md) |
| kueste | 8 | 4 | 4 | 2 | [katalog.md](sehens/kueste/katalog.md) |
| sumpf | 8 | 3 | 5 | 0 | [katalog.md](sehens/sumpf/katalog.md) |
| canyon | 8 | 3 | 5 | 0 | [katalog.md](sehens/canyon/katalog.md) |
| wueste | 8 | 3 | 5 | 0 | [katalog.md](sehens/wueste/katalog.md) |
| oedland | 8 | 3 | 5 | 3 | [katalog.md](sehens/oedland/katalog.md) |

Abweichungen von 3 Leuchtfeuern / 5 Fundstücken: lava 4/4, tundra 4/4, kueste 4/4. Tundra und Küste: auf der offenen Küstenebene bzw. vom Klippensteig aus lässt sich kein fünftes Fundstück verdecken. Lava: die Kraterreihe am Kratersteig ist ein natürliches Leuchtfeuer.

## Neue Pfade (13c: „lieber ein Pfad mehr als ein Ort weniger“)

Schema `pfade` in `standorte.json` (siehe `skripte/sehens_lib/README.md`). Kehren und Geländeanschnitt rechnet Ferats Serpentinen-Werkzeug. Länge = Polylinie, max. Steigung = Rohlinie auf 2-m-Daten (vor Kehren).

| Biom | Pfad | Art | Länge | max. Steigung | Orte |
|---|---|---|---|---|---|
| lava | `lava_pfad_kratersteig_west` | trampelpfad | 916 m | 10° | 2 |
| lava | `lava_pfad_kratersteig_ost` | trampelpfad | 600 m | 20° | 1 |
| lava | `lava_pfad_gipfelsteig` | serpentine | 2 432 m | 24° | 0 |
| gletscher | `gletscher_pfad_weststeig` | serpentine | 1 535 m | 40° | 2 |
| gletscher | `gletscher_pfad_oststeig` | serpentine | 1 348 m | 34° | 2 |
| gletscher | `gletscher_pfad_nordhang` | serpentine | 732 m | 34° | 1 |
| frost | `frost_pfad_froststeig` | serpentine | 1 278 m | 28° | 5 |
| frost | `frost_pfad_suedsteig` | trampelpfad | 705 m | 24° | 3 |
| fjord | `fjord_pfad_kanzel` | serpentine | 313 m | 28° | 1 |
| fjord | `fjord_pfad_fjordsteig` | serpentine | 2 243 m | 53° | 7 |
| tundra | `tundra_pfad_der_pingo` | trittsteine | 63 m | 24° | 1 |
| tundra | `tundra_pfad_die_eiswand` | trampelpfad | 110 m | 18° | 1 |
| tundra | `tundra_pfad_der_trunkene_grund` | serpentine | 307 m | 26° | 1 |
| tundra | `tundra_pfad_das_aufeis` | serpentine | 280 m | 25° | 1 |
| kueste | `kueste_pfad_klippensteig` | serpentine | 4 269 m | 33° | 5 |
| kueste | `kueste_pfad_kap` | trampelpfad | 1 893 m | 27° | 3 |
| oedland | `oedland_pfad_oedlandpfad_abstieg` | serpentine | 491 m | 20° | 4 |
| oedland | `oedland_pfad_oedlandpfad_ost` | trampelpfad | 828 m | 8° | 2 |
| oedland | `oedland_pfad_oedlandpfad_west` | trampelpfad | 551 m | 8° | 2 |

Zusammen 20 893 m. Kurze Zugänge mit Kehren vom Weg zum Ort stehen als `pfad_cm` am Ort und zählen nicht als Weg.

## aue

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Biberstau** | Fundstück | 144 m | – | Im dunklen Nadelwald am Westrand der Aue hört man zuerst Wasser, das nicht rauscht, sondern über eine Kante | [Bild](sehens/aue/aue_01_biberstau.png) |
| 02 | **Die Alte** | Leuchtfeuer | 270 m | – | Mitten in der Bachwiese von C4, zwischen zwei Bacharmen, steht ein einzelner Baum, der die ganze Ebene | [Bild](sehens/aue/aue_02_die_alte.png) |
| 03 | **Schwalbenwand** | Leuchtfeuer | 267 m | – | Südlich des großen Flussbogens bricht die Terrasse in einer 9–10 m hohen, fast senkrechten Wand aus | [Bild](sehens/aue/aue_03_schwalbenwand.png) |
| 04 | **Treibholzwerder** | Leuchtfeuer | 273 m | – | Mitten im Strom liegt eine lange Kiesinsel. | [Bild](sehens/aue/aue_04_treibholzwerder.png) |
| 05 | **Lilienrinne** | Fundstück | 148 m | – | Zwischen den Gehölzinseln der Hartholzaue zieht eine flache, gewundene Mulde durch die Wiese – ein alter | [Bild](sehens/aue/aue_05_lilienrinne.png) |
| 06 | **Mondarm** | Fundstück | 84 m | – | Vom Weg aus nur ein Weidengebüsch. | [Bild](sehens/aue/aue_06_mondarm.png) |
| 07 | **Blautopf** | Fundstück | 87 m | – | In einer Kerbe des Laubwalds, unter einem halbrunden Kalkfelsen, liegt ein kreisrunder Topf voller Wasser | [Bild](sehens/aue/aue_07_blautopf.png) |
| 08 | **Lianenhalle** | Fundstück | 210 m | – | Am Prallufer des Elfenflusses steht ein Stück Urwald der Hartholzaue: alte Pappeln, Hainbuchen und Eichen, | [Bild](sehens/aue/aue_08_lianenhalle.png) |

## bergwald

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Der Mönch** | Leuchtfeuer | 296 m | – | Auf der Nase einer Felsrippe, dort wo die letzten Wetterkiefern des Grats stehen, ragt eine schlanke, | [Bild](sehens/bergwald/bergwald_01_der_moench.png) |
| 02 | **Die Brandkiefer** | Leuchtfeuer | 101 m | – | Auf dem Kopf eines bewaldeten Sporns, hoch über der Talstraße, steht eine riesige tote Kiefer, schwarz | [Bild](sehens/bergwald/bergwald_02_die_brandkiefer.png) |
| 03 | **Säulenhain** | Leuchtfeuer | 104 m | – | Auf einer Bachterrasse zwischen zwei Gerinnen stehen zwölf Tannen in doppelter Größe – 45–55 m, Stämme wie | [Bild](sehens/bergwald/bergwald_03_saeulenhain.png) |
| 04 | **Felsenmeer** | Fundstück | 84 m | – | Hinter einer Waldrippe öffnet sich ein Talschluss: oben eine graue Abbruchkante, darunter ein Meer aus | [Bild](sehens/bergwald/bergwald_04_felsenmeer.png) |
| 05 | **Klemmblock-Klamm** | Fundstück | 203 m | – | Ein Bach beginnt am Fuß einer Felsstufe. | [Bild](sehens/bergwald/bergwald_05_klemmblock_klamm.png) |
| 06 | **Karsee** | Fundstück | 285 m | – | Hinter einer Felsschwelle liegt ein kleiner, tintendunkler See in einem Kessel, dessen Wände 30–50 m | [Bild](sehens/bergwald/bergwald_06_karsee.png) |
| 07 | **Windwurf** | Fundstück | 132 m | – | Mitten im dichten Küstenwald plötzlich Licht: eine 115 m lange Gasse, in der alle Fichten in dieselbe Richtung | [Bild](sehens/bergwald/bergwald_07_windwurf.png) |
| 08 | **Der Wurzelstein** | Fundstück | 275 m | – | Auf einer Waldrippe liegt ein Findling so groß wie ein Haus. | [Bild](sehens/bergwald/bergwald_08_der_wurzelstein.png) |

## elfenwald

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Mutterbaum** | Leuchtfeuer | 94 m | – | Auf einer runden Waldkuppe über der Küste steht ein Baum, der nicht in diese Welt passt: 55 m hoch, der | [Bild](sehens/elfenwald/elfenwald_01_mutterbaum.png) |
| 02 | **Nebelhain** | Leuchtfeuer | 295 m | – | Auf dem Ostgrat, 393 m hoch, sitzt eine Wolke fest. | [Bild](sehens/elfenwald/elfenwald_02_nebelhain.png) |
| 03 | **Rotlaubhain** | Leuchtfeuer | 173 m | – | Am Hang über der Elfenstadt brennt mitten im grünen Wald ein Fleck Rot: vierzehn Buchen mit blutrotem Laub, | [Bild](sehens/elfenwald/elfenwald_03_rotlaubhain.png) |
| 04 | **Elfentreppe** | Fundstück | 109 m | – | Man folgt einem Rauschen in eine Senke und steht vor einer Treppe aus Wasser: Der Waldbach fällt über | [Bild](sehens/elfenwald/elfenwald_04_elfentreppe.png) |
| 05 | **Farnschlucht** | Fundstück | 208 m | – | Ein Tobel an der Grenze zum Gebirge: Der Bach stürzt über 80 m Länge 48 m tief in kleinen Kaskaden hinab, | [Bild](sehens/elfenwald/elfenwald_05_farnschlucht.png) |
| 06 | **Blauer Grund** | Fundstück | 153 m | – | Nach 150 m durch braunen Buchenwald wird der Boden blau. | [Bild](sehens/elfenwald/elfenwald_06_blauer_grund.png) |
| 07 | **Schwammgrund** | Fundstück | 100 m | – | Am nordseitigen Bachhang liegt ein gestürzter Riese, 48 m lang, halb zu Erde zerfallen. | [Bild](sehens/elfenwald/elfenwald_07_schwammgrund.png) |
| 08 | **Wurzelbruecke** | Fundstück | 82 m | – | In der Kerbe eines Waldbachs liegt ein einzelner Riesenstamm quer über dem Wasser, 44 m lang, 3 m dick, | [Bild](sehens/elfenwald/elfenwald_08_wurzelbruecke.png) |

## dschungel

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Mondtor** | Leuchtfeuer | 80 m | – | Über dem Wald am Nordrand steht ein 100 m hoher Kalkturm, und oben an seiner Schulter klafft ein rundes | [Bild](sehens/dschungel/dschungel_01_mondtor.png) |
| 02 | **Turmquelle** | Leuchtfeuer | 83 m | – | An der Nordwand eines 160 m hohen Turms tritt auf halber Höhe Wasser aus dem Fels – kein Bach führt hinauf, | [Bild](sehens/dschungel/dschungel_02_turmquelle.png) |
| 03 | **Steinwald** | Leuchtfeuer | 286 m | – | Auf der Schulter eines Turms im Osten steht ein Wald aus Stein: sechzig graue Kalknadeln, 4–18 m hoch, | [Bild](sehens/dschungel/dschungel_03_steinwald.png) |
| 04 | **Blaues Auge** | Fundstück | 239 m | – | Zwischen drei Türmen öffnet sich im Wald plötzlich der Boden: ein fast runder Schacht, 50 × 60 m, mit | [Bild](sehens/dschungel/dschungel_04_blaues_auge.png) |
| 05 | **Verborgene Lagune** | Fundstück | 276 m | – | Im Fuß eines großen Turms klafft eine Spalte. | [Bild](sehens/dschungel/dschungel_05_verborgene_lagune.png) |
| 06 | **Schluckhoehle** | Fundstück | 222 m | – | Am Westrand, wo der Wald in eine offene Kalkplatte übergeht, laufen zwei Bäche von Norden und Süden aufeinander | [Bild](sehens/dschungel/dschungel_06_schluckhoehle.png) |
| 07 | **Garten der Riesen** | Fundstück | 209 m | – | Unter 60 m hohen Urwaldriesen liegt eine Lichtung, in der alles zu groß ist: Blätter wie Segel, 2–4 m hohe | [Bild](sehens/dschungel/dschungel_07_garten_der_riesen.png) |
| 08 | **Sinterhalle** | Fundstück | 128 m | – | Am Fuß der Südwand im Karstmassiv wölbt sich der Fels zu einem 40 m breiten, 12 m hohen Dach. | [Bild](sehens/dschungel/dschungel_08_sinterhalle.png) |

## lava

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Die Schwarze Mauer** | Leuchtfeuer | 96 m | – | Aus dem grünen Moospolster steigt unvermittelt eine schwarze Wand aus Blocklava, 6–9 m hoch, 140 m lang, in | [Bild](sehens/lava/lava_01_schwarze_mauer.png) |
| 02 | **Schwefelgrund** | Leuchtfeuer | 201 m | – | Am Fuß des Vulkans liegt eine flache Mulde, in der der Boden ocker, schwefelgelb und gebleicht ist. | [Bild](sehens/lava/lava_02_schwefelgrund.png) |
| 03 | **Die Kraterkinder** | Leuchtfeuer | 291 m | – | In einer schwarzen Aschensenke am Rand der grünen Aue sitzen fünf kleine, runde Kegel wie Kinder um ein Feuer, | [Bild](sehens/lava/lava_03_kraterkinder.png) |
| 04 | **Das Roehrenfenster** | Fundstück | 286 m | – | Auf dem Moosplateau liegt ein Druckrücken; wer darüber geht, steht plötzlich an einem 26 × 16 m großen, | [Bild](sehens/lava/lava_04_roehrenfenster.png) |
| 05 | **Die Klare Spalte** | Fundstück | 135 m | – | Mitten in der Mooslava klafft eine 110 m lange, 4–9 m breite Spalte. | [Bild](sehens/lava/lava_05_klare_spalte.png) |
| 06 | **Die Kraterreihe** | Leuchtfeuer | 149 m | `lava_pfad_kratersteig_ost` | Am Nordostfuß des Vulkans stehen vier Schlackenkegel auf einer schnurgeraden Spalte, wie Perlen auf einer Schnur. | [Bild](sehens/lava/lava_06_kraterreihe.png) |
| 07 | **Die Basaltorgel** | Fundstück | 104 m | `lava_pfad_kratersteig_west` | Vom Plateau aus nichts. | [Bild](sehens/lava/lava_07_basaltorgel.png) |
| 08 | **Das Glutauge** | Fundstück | 99 m | `lava_pfad_kratersteig_west` | Auf dem jungen, schwarz glänzenden Strom des Westplateaus – Stricklava mit Seilen, Zehen und aufgewölbten | [Bild](sehens/lava/lava_08_glutauge.png) |

## gletscher

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Das Gletschertor** | Leuchtfeuer | 192 m | – | Die Zunge des Kargletschers bricht über eine Felsstufe: ein 120 m breiter Séracbruch aus blauen, schiefen Eistürmen (8–15 m), dazwischen Spalten, in denen das Licht … | [Bild](sehens/gletscher/gletscher_01_gletschertor.png) |
| 02 | **Der Lawinenkegel** | Leuchtfeuer | 87 m | – | Aus einer engen Rinne in der Westwand des Tals zieht ein schmutzig-weißer Kegel aus Altschnee 90 m weit in den Wald: der Lawinenkegel. | [Bild](sehens/gletscher/gletscher_02_lawinenkegel.png) |
| 03 | **Der Moränensee** | Fundstück | 173 m | `gletscher_pfad_weststeig` | In einem kleinen Hängetal unter dem Westgrat liegt ein milchig-türkiser See, nicht größer als ein Hof, hinter einem Riegel aus Moränenschutt. | [Bild](sehens/gletscher/gletscher_03_moraenensee.png) |
| 04 | **Das Toteisloch** | Fundstück | 141 m | – | Mitten im Heidehang östlich des Frostlagers ein runder Trichter, 6–7 m tief und 45 m breit, mit steilen, moosigen Wänden. | [Bild](sehens/gletscher/gletscher_04_toteisloch.png) |
| 05 | **Die Wächte** | Leuchtfeuer | 125 m | `gletscher_pfad_weststeig` | Auf dem Nordgrat des Kars hängt eine Schneewächte wie eine erstarrte Welle 6–8 m über den Abgrund, blau im Schatten, an der Kante von Wind gezahnt. | [Bild](sehens/gletscher/gletscher_05_die_waechte.png) |
| 06 | **Die Gletschertöpfe** | Fundstück | 109 m | `gletscher_pfad_oststeig` | In einer engen Felsklamm nordöstlich des Kars hat das Schmelzwasser des einstigen Gletschers runde Töpfe in den Fels gebohrt – drei glattgeschliffene Kessel, der größte … | [Bild](sehens/gletscher/gletscher_06_gletschertoepfe.png) |
| 07 | **Der Nunatak** | Fundstück | 108 m | `gletscher_pfad_oststeig` | Hinter dem Ostgrat versteckt sich ein schwarzer Felszahn, der aus einem Firnfeld ragt wie eine Insel aus dem Eis: der Nunatak. | [Bild](sehens/gletscher/gletscher_07_der_nunatak.png) |
| 08 | **Der Gletscherschliff** | Fundstück | 106 m | `gletscher_pfad_nordhang` | Auf der Nordflanke über dem Meer hat das Eis den Fels poliert: buckelige Rundhöcker, glatt wie Walrücken, mit feinen parallelen Kratzern und sichelförmigen Schlagmarken. | [Bild](sehens/gletscher/gletscher_08_gletscherschliff.png) |

## frost

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Der Eisfall** | Fundstück | 87 m | `frost_pfad_froststeig` | Wo der Nordbach über eine 12-m-Stufe in den Frostsee fällt, ist er mitten im Sturz erstarrt: ein Bündel aus milchig-blauen Eissäulen, zwischen denen hinter dünnem Eis … | [Bild](sehens/frost/frost_01_der_eisfall.png) |
| 02 | **Der Frostsee** | Leuchtfeuer | 108 m | `frost_pfad_suedsteig` | Der Frostsee ist ganz zugefroren, aber nicht weiß: Wind hat den Schnee abgefegt, und man blickt durch schwarzes, klares Eis. | [Bild](sehens/frost/frost_02_frostsee.png) |
| 03 | **Der Eisvorhang** | Fundstück | 88 m | `frost_pfad_froststeig` | Unter dem Nordufer des Frostsees tritt Sickerwasser aus einer überhängenden Felsbank. | [Bild](sehens/frost/frost_03_eisvorhang.png) |
| 04 | **Der Raureifhain** | Leuchtfeuer | 88 m | `frost_pfad_froststeig` | Auf einer Hangschulter über dem Frostsee stehen dreißig Kiefern, die keine Bäume mehr zu sein scheinen: dicke Panzer aus Raureif und Schnee haben sie in weiße, gebeugte … | [Bild](sehens/frost/frost_04_raureifhain.png) |
| 05 | **Der Blockgletscher** | Fundstück | 250 m | `frost_pfad_froststeig` | Am Osthang zieht eine graue Zunge aus Blöcken wie ein Lavastrom ins Tal – aber sie ist kalt: ein Blockgletscher, unter dessen Schutt ein Eiskern steckt. | [Bild](sehens/frost/frost_05_blockgletscher.png) |
| 06 | **Die Eisküste** | Leuchtfeuer | 95 m | `frost_pfad_froststeig` | An der Ostküste friert die Brandung an: ein Eisfuß aus geschichtetem Spritzeis säumt den Strand, und darauf stehen Eisvulkane – Kegel bis 4 m, aus deren Spitze bei jeder … | [Bild](sehens/frost/frost_06_eiskueste.png) |
| 07 | **Die Frostblumen** | Fundstück | 192 m | `frost_pfad_suedsteig` | Wo der Abfluss des Frostsees ins Meer mündet, liegt eine flache Lagune mit hauchdünnem, jungem Eis. | [Bild](sehens/frost/frost_07_frostblumen.png) |
| 08 | **Der Glockenbach** | Fundstück | 92 m | `frost_pfad_suedsteig` | Ein flacher Bach rauscht über Steine zum Meer – und jeder Stein, den die Spritzer treffen, trägt eine Glocke aus Eis: runde, durchsichtige Hauben, unten offen, in denen … | [Bild](sehens/frost/frost_08_glockenbach.png) |

## fjord

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Die Kanzel** | Leuchtfeuer | 103 m | `fjord_pfad_kanzel` | Am Rand der Ostwand springt eine flache Felsplatte über den Fjord vor – eben wie ein Tisch, an drei Seiten 220 m senkrecht. | [Bild](sehens/fjord/fjord_01_die_kanzel.png) |
| 02 | **Die Schleierwand** | Leuchtfeuer | 91 m | `fjord_pfad_fjordsteig` | Am Talschluss des Fjords steht eine 250 m hohe, halbrunde Felswand. | [Bild](sehens/fjord/fjord_02_schleierwand.png) |
| 03 | **Die Trollzunge** | Leuchtfeuer | 91 m | `fjord_pfad_fjordsteig` | Am Grat über dem Talschluss ragt eine schmale Felszunge 15 m frei über den Abgrund nach Norden – darunter 300 m Luft bis zum Fjordboden. | [Bild](sehens/fjord/fjord_03_trollzunge.png) |
| 04 | **Das Hängetal** | Fundstück | 88 m | `fjord_pfad_fjordsteig` | Auf der Südseite des Fjordkamms endet ein kleines, flaches Hochtal plötzlich an einer Stufe: Der Bach, der eben noch zwischen Wollgras mäanderte, stürzt 40 m in eine … | [Bild](sehens/fjord/fjord_04_haengetal.png) |
| 05 | **Der Fjordkopf** | Fundstück | 87 m | `fjord_pfad_fjordsteig` | Wo der Fjordbach ins Meer läuft, hat er einen flachen Fächer aus Kies und Sand geschüttet. | [Bild](sehens/fjord/fjord_05_fjordkopf.png) |
| 06 | **Der Bergsturzkegel** | Fundstück | 87 m | `fjord_pfad_fjordsteig` | Aus der Westwand ist ein Stück Berg ausgebrochen: oben eine helle, frische Abrissnische, darunter ein Kegel aus hausgroßen Blöcken, der bis an den Talboden reicht. | [Bild](sehens/fjord/fjord_06_bergsturz.png) |
| 07 | **Die Brandungsgrotte** | Fundstück | 101 m | `fjord_pfad_fjordsteig` | An der Ostspitze der Fjordmündung, wo die Dünung hereinläuft, hat das Meer einen schmalen Spalt ins Gestein gearbeitet: eine Grotte, hoch und eng, mit grünem Wasser, in … | [Bild](sehens/fjord/fjord_07_brandungsgrotte.png) |
| 08 | **Die alten Ufer** | Fundstück | 271 m | `fjord_pfad_fjordsteig` | Am Westhang der Fjordmündung ziehen sich drei grüne Stufen parallel zum Wasser den Berg hinauf – alte Strandlinien, 20, 45 und 70 m über dem heutigen Meer. | [Bild](sehens/fjord/fjord_08_strandterrassen.png) |

## tundra

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Der Eisbuckel** | Leuchtfeuer | 92 m | `tundra_pfad_der_pingo` | Aus der flachen Schwemmebene neben dem Zopfstrom wölbt sich ein vollkommen runder, 22 m hoher Hügel mit braun-grüner | [Bild](sehens/tundra/tundra_01_der_pingo.png) |
| 02 | **Der Wanderer** | Leuchtfeuer | 129 m | – | Auf dem höchsten Punkt einer kahlen, glattgeschliffenen Felskuppe liegt ein hausgroßer, fremdartig heller Block – | [Bild](sehens/tundra/tundra_02_der_wanderer.png) |
| 03 | **Die Eiswand** | Leuchtfeuer | 93 m | `tundra_pfad_die_eiswand` | An der Küste ist die Tundra aufgerissen: ein Halbrund von 100 m Breite, dessen Rückwand 8–10 m hoch aus gestreiftem | [Bild](sehens/tundra/tundra_03_die_eiswand.png) |
| 04 | **Die Fliesstreppe** | Leuchtfeuer | 145 m | – | Ein sonniger Südwesthang ist zu einer Riesentreppe geworden: fünf grüne, zungenförmige Wülste aus Fließerde, jeder | [Bild](sehens/tundra/tundra_04_die_fliesstreppe.png) |
| 05 | **Der Trunkene Grund** | Fundstück | 185 m | `tundra_pfad_der_trunkene_grund` | Hinter dem Hügelrücken, im lichten Fichten-Lärchen-Saum, liegt ein brauner See ohne festes Ufer. | [Bild](sehens/tundra/tundra_05_der_trunkene_grund.png) |
| 06 | **Das Aufeis** | Fundstück | 89 m | `tundra_pfad_das_aufeis` | Am Grund einer engen Schlucht liegt mitten im Sommer eine 70 m lange, gestufte Eisdecke, 1–2,5 m dick, blau an den | [Bild](sehens/tundra/tundra_06_das_aufeis.png) |
| 07 | **Die Steinringe** | Fundstück | 93 m | – | Auf einer Kiesterrasse über dem Strand liegen zwanzig Ringe aus Steinen, 2–4 m im Durchmesser, so regelmäßig, als | [Bild](sehens/tundra/tundra_07_die_steinringe.png) |
| 08 | **Das Wabenmoor** | Fundstück | 104 m | – | Unten an der Flussmündung, im Schutz des Steilufers, ist der Boden in Waben zerlegt: sechseckige Felder von 9–12 m, | [Bild](sehens/tundra/tundra_08_das_wabenmoor.png) |

## heide

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Die Graue Burg** | Leuchtfeuer | 84 m | – | Auf der Kuppe über zwei Bächen türmen sich graue Granitplatten zu drei Stapeln, der höchste 11 m: waagerecht | [Bild](sehens/heide/heide_01_die_graue_burg.png) |
| 02 | **Ginstergold** | Leuchtfeuer | 155 m | – | Ein ganzer Osthang am Rand des Birkenwalds glüht gelb: dichte Ginsterbüsche in voller Blüte, dazwischen ein purpurner | [Bild](sehens/heide/heide_02_ginstergold.png) |
| 03 | **Die Wacholderprozession** | Leuchtfeuer | 198 m | – | Über einen flachen Rücken zieht sich eine Reihe dunkler, säulenförmiger Wacholder – 45 Gestalten von 3 bis 7 m, alle | [Bild](sehens/heide/heide_03_die_wacholderprozession.png) |
| 04 | **Der Kolk** | Fundstück | 205 m | – | Hinter einem Kranz aus Granitplatten und Krüppelkiefern wölbt sich ein Hochmoor, rot-grün gesprenkelt von Torfmoos- | [Bild](sehens/heide/heide_04_der_kolk.png) |
| 05 | **Der Wackelstein** | Fundstück | 93 m | – | Zwischen den Granitplatten des Rückens führt ein Durchschlupf in einen runden Felsenkessel, ummauert von | [Bild](sehens/heide/heide_05_der_wackelstein.png) |
| 06 | **Der Wollsackfall** | Fundstück | 115 m | – | Neben einer 5 m hohen Granitrippe hat sich der Heidebach eine schmale Klamm gegraben. | [Bild](sehens/heide/heide_06_der_wollsackfall.png) |
| 07 | **Der Totengrund** | Fundstück | 85 m | – | Hinter einer Hangkante öffnet sich ein runder, 4 m tiefer Kessel, dessen Hänge vollständig mit blühender Besenheide | [Bild](sehens/heide/heide_07_der_totengrund.png) |
| 08 | **Die Windkante** | Fundstück | 111 m | – | Am Westrand der Heide, wo der Seewind auf das Land trifft, hat der Sand eine hufeisenförmige Düne aufgeworfen, 4 m hoch, | [Bild](sehens/heide/heide_08_die_windkante.png) |

## kueste

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Die Alten** | Leuchtfeuer | 300 m | `kueste_pfad_klippensteig` | Vor dem Kliff stehen zwei Granitpfeiler im Meer, der größere 45 m hoch, schmal, oben mit einem Schopf aus Grasnelken | [Bild](sehens/kueste/kueste_01_die_alten.png) |
| 02 | **Die Vogelinsel** | Leuchtfeuer | 232 m | `kueste_pfad_klippensteig` | Eine Insel wie ein Schiffsrumpf, 45 m hoch, die Westwand weiß gekalkt von tausenden Brutplätzen, auf jedem Sims ein | [Bild](sehens/kueste/kueste_02_die_vogelinsel.png) |
| 03 | **Das Nadeltor** | Leuchtfeuer | 167 m | `kueste_pfad_klippensteig` | Am Ende des Kliffwegs, 130 m vor der Küste: ein 46-m-Pfeiler, durch den das Meer ein Tor geschlagen hat – unten eine | [Bild](sehens/kueste/kueste_03_das_nadeltor.png) |
| 04 | **Der Seefall** | Fundstück | 93 m | `kueste_pfad_klippensteig` | Man hört ihn, bevor man ihn sieht: ein Bach läuft durch Farn und Grasnelken auf die Kliffkante zu – und ist weg. | [Bild](sehens/kueste/kueste_04_der_seefall.png) |
| 05 | **Die Gezeitenbank** | Fundstück | 106 m | `kueste_pfad_klippensteig` | Am Fuß der Kliffecke, wo die Strandebene ans Gebirge stößt, liegt eine flache, dunkle Felsbank knapp über dem Wasser, | [Bild](sehens/kueste/kueste_05_die_gezeitenbank.png) |
| 06 | **Die Kreidewand** | Leuchtfeuer | 112 m | `kueste_pfad_kap` | Mitten in der grünen Buchenflanke des Kaps ist ein Stück Berg abgerutscht: eine leuchtend weiße Kreidewand, 25–30 m | [Bild](sehens/kueste/kueste_06_die_kreidewand.png) |
| 07 | **Der Dünenkamm** | Fundstück | 191 m | `kueste_pfad_kap` | Hinter der Nordostnase des Kaps, unsichtbar vom Pfad, liegt ein Strand, den der Wind zu einem Dünenkamm aufgeworfen | [Bild](sehens/kueste/kueste_07_der_duenenkamm.png) |
| 08 | **Das Blasloch** | Fundstück | 150 m | `kueste_pfad_kap` | In der steilen Ostbucht, auf einer dunklen Felsplatte über dem Wasser: ein Loch, kaum zwei Meter breit. | [Bild](sehens/kueste/kueste_08_das_blasloch.png) |

## sumpf

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Der Ertrunkene Wald** | Leuchtfeuer | 154 m | – | Vom Westweg aus ragen über dem Röhricht graue Spitzen in den Himmel – tote Fichten, Dutzende, silbern gebleicht, die | [Bild](sehens/sumpf/sumpf_01_der_ertrunkene_wald.png) |
| 02 | **Der Weidendom** | Leuchtfeuer | 198 m | – | Im Osten des Sumpfes steht ein runder Hügel aus Grün über dem Röhricht – erst beim Näherkommen erkennt man, dass es | [Bild](sehens/sumpf/sumpf_02_der_weidendom.png) |
| 03 | **Der Reiherhorst** | Leuchtfeuer | 272 m | – | Auf einer flachen Moosinsel mitten im offenen Sumpf stehen drei abgestorbene Baumriesen, weiß und kahl – und in ihren | [Bild](sehens/sumpf/sumpf_03_der_reiherhorst.png) |
| 04 | **Der Schwingrasen** | Fundstück | 286 m | – | Hinter einem Saum aus Moorbirken öffnet sich eine Fläche aus rostrotem und grünem Torfmoos, die schwankt, wenn man | [Bild](sehens/sumpf/sumpf_04_der_schwingrasen.png) |
| 05 | **Der Erlenbruch** | Fundstück | 286 m | – | Am Fuß des Nordhangs, wo Quellwasser austritt, steht ein dichter Ring aus Bäumen auf Stelzwurzeln – jeder Stamm auf | [Bild](sehens/sumpf/sumpf_05_der_erlenbruch.png) |
| 06 | **Das Bultenfeld** | Fundstück | 273 m | – | Eine Wiese, die keine ist: hunderte kniehohe Seggenbulten, jeder ein Schopf aus Halmen auf einem Sockel aus alten | [Bild](sehens/sumpf/sumpf_06_das_bultenfeld.png) |
| 07 | **Der Tellerweiher** | Fundstück | 259 m | – | Ein kleiner, stiller Weiher hinter Rohrkolben, und darauf liegen Seerosenblätter so groß wie Wagenräder – 3 bis 5 m, | [Bild](sehens/sumpf/sumpf_07_der_tellerweiher.png) |
| 08 | **Die Irrlichtsenke** | Fundstück | 178 m | – | Eine Senke voller Totholz, in der der Nebel auch mittags nicht weicht. | [Bild](sehens/sumpf/sumpf_08_die_irrlichtsenke.png) |

## canyon

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Das Sonnenfenster** | Leuchtfeuer | 113 m | – | Auf der Oberkante der Südstufe steht eine freie, 25 m lange Sandsteinfinne, rostrot mit hellen Bändern. | [Bild](sehens/canyon/canyon_01_sonnenfenster.png) |
| 02 | **Der Wäger** | Leuchtfeuer | 118 m | – | Auf der Kuppe einer schmalen Schichtrippe am Canyonausgang balanciert ein 6 m großer, rundgeschliffener Block auf | [Bild](sehens/canyon/canyon_02_der_waeger.png) |
| 03 | **Die Rote Stufe** | Leuchtfeuer | 300 m | – | Über dem Aue-Vorland erhebt sich die westliche Schichtstufe in vier Etagen: rote Wände, helle Gesimse, auf jedem | [Bild](sehens/canyon/canyon_03_rote_stufe.png) |
| 04 | **Die Flüsterschlucht** | Fundstück | 258 m | – | Ein Bach auf dem Plateau verschwindet in einem Spalt, 2–6 m breit, 18 m tief, mit geschwungenen, glattgewaschenen | [Bild](sehens/canyon/canyon_04_fluesterschlucht.png) |
| 05 | **Der Hoodoo-Kessel** | Fundstück | 221 m | – | Der Canyonrand ist hier zu einem halbrunden Kessel zerfallen. | [Bild](sehens/canyon/canyon_05_hoodoo_kessel.png) |
| 06 | **Die Kolke** | Fundstück | 299 m | – | Eine Bank aus hellem Slickrock, darin ein halbes Dutzend runder, wassergefüllter Kolke (1–4 m), verbunden durch | [Bild](sehens/canyon/canyon_06_die_kolke.png) |
| 07 | **Die Smaragdgumpe** | Fundstück | 194 m | – | In einem halbrunden Alkoven der Südstufe fällt der Plateaubach in Fäden 38 m über die Bänder in eine smaragdgrüne | [Bild](sehens/canyon/canyon_07_smaragdgumpe.png) |
| 08 | **Die Welle** | Fundstück | 136 m | – | In einer Mulde zwischen Schichtrippen liegt eine Platte aus versteinerter Düne: Hunderte feiner Linien in Rot, | [Bild](sehens/canyon/canyon_08_die_welle.png) |

## wueste

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Die Yardang-Flotte** | Leuchtfeuer | 299 m | – | Vier lange Felsrücken laufen parallel auf die Küste zu wie die Rümpfe gestrandeter Schiffe: scharfer, steiler Bug | [Bild](sehens/wueste/wueste_01_yardang_flotte.png) |
| 02 | **Die Sterndüne** | Leuchtfeuer | 131 m | – | Eine 22 m hohe Düne mit drei geschwungenen, messerscharfen Kämmen, die sich im Gipfel treffen; eine Flanke im | [Bild](sehens/wueste/wueste_02_sternduene.png) |
| 03 | **Die Wächter** | Leuchtfeuer | 149 m | – | Sieben weiße, gedrungene Pilzfelsen stehen auf einer Kiesfläche wie Wachen; der Wind hat ihre Füße zu Hohlkehlen | [Bild](sehens/wueste/wueste_03_die_waechter.png) |
| 04 | **Die Quelloase** | Fundstück | 231 m | – | Im engen Talgrund nahe der Nordküste quillt aus dem Fuß der Rippen ein türkiser Quelltopf, 12 m breit; fünf | [Bild](sehens/wueste/wueste_04_quelloase.png) |
| 05 | **Die Salzpfanne** | Fundstück | 144 m | – | Hinter einem niedrigen Dünenriegel liegt eine gleißend weiße Kruste mit Wabenmuster, 120 m breit; in der Mitte eine | [Bild](sehens/wueste/wueste_05_salzpfanne.png) |
| 06 | **Das Windkanter-Feld** | Fundstück | 108 m | – | Auf einer windoffenen Verflachung des Rippenkamms liegt ein dunkles Steinpflaster; jeder Stein ist vom Sand | [Bild](sehens/wueste/wueste_06_windkanterfeld.png) |
| 07 | **Das Trockene Wadi** | Fundstück | 97 m | – | Eine enge Flutrinne, Sohle aus rundgeschliffenem Geröll, an den Prallhängen Treibholz in Verhauen 2 m über der | [Bild](sehens/wueste/wueste_07_trockenes_wadi.png) |
| 08 | **Die Wabenwand** | Fundstück | 139 m | – | Die Nordwand einer Küstenrippe ist von Waben durchlöchert – Hunderte Höhlungen, von Faustgröße bis zu einer | [Bild](sehens/wueste/wueste_08_wabenwand.png) |

## oedland

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Das Rippenland** | Leuchtfeuer | 251 m | – | Über dem Wiesenrand steigt eine graue Badland-Kuppe auf, zerschnitten von Dutzenden paralleler Rinnen; dazwischen | [Bild](sehens/oedland/oedland_01_rippenland.png) |
| 02 | **Der Regenbogenhang** | Leuchtfeuer | 219 m | – | Eine 60 m hohe, steile Tonflanke in Bändern: Ziegelrot, Ocker, Violettgrau, Kreideweiß, wieder Rot – wie | [Bild](sehens/oedland/oedland_02_regenbogenhang.png) |
| 03 | **Das Höllentor** | Leuchtfeuer | 133 m | `oedland_pfad_oedlandpfad_ost` | Mitten im grauen Ton-Flachland klafft ein kreisrunder Krater, 40 m breit, 9 m tief. | [Bild](sehens/oedland/oedland_03_hoellentor.png) |
| 04 | **Die Dornbusch-Senke** | Fundstück | 290 m | – | Am Westrand der Kante, wo ein Bach unter die Wiese taucht, liegt eine Senke voller grauer Dornbüsche, dazwischen | [Bild](sehens/oedland/oedland_04_dornbusch_senke.png) |
| 05 | **Die Kugelsteine** | Fundstück | 94 m | – | Wo eine Badland-Rinne auf das Flachland mündet, hat die Flut einen Geröllfächer geschüttet und in seiner Mitte einen | [Bild](sehens/oedland/oedland_05_kugelsteine.png) |
| 06 | **Die Schlammvulkänchen** | Fundstück | 106 m | `oedland_pfad_oedlandpfad_ost` | Neben dem alten Kraterring liegt in einer flachen Mulde ein Feld grauer Kegel, 1–3 m hoch, jeder mit nassem Krater, | [Bild](sehens/oedland/oedland_06_schlammvulkaene.png) |
| 07 | **Die Totenpfanne** | Fundstück | 124 m | `oedland_pfad_oedlandpfad_west` | Der Badland-Bach endet in einer weißen, gerissenen Tonpfanne. | [Bild](sehens/oedland/oedland_07_totenpfanne.png) |
| 08 | **Die Erdröhren** | Fundstück | 220 m | `oedland_pfad_oedlandpfad_west` | Am Lehmhang über dem Westbach ist der Boden durchlöchert: drei Schlucklöcher bis 7 m tief, verbunden durch Tunnel, | [Bild](sehens/oedland/oedland_08_erdroehren.png) |

