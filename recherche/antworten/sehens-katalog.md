# Sehenswürdigkeiten – Gesamtkatalog (Auftrag 13, Phase 1, Teil B)

Stand 11.10.2026. **120 Orte in 15 Biomen** (je 8): 48 Leuchtfeuer, 72 Fundstücke, 18 neue Pfade. Nur Landschaft (Fels, Wasser, Eis, Feuer, Pflanzen) – keine Bauten, Ruinen, Knochen oder Menschenspuren, keine Houdini-`SW_*`-Assets.

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
| tundra | 8 | 4 | 4 | 3 | [katalog.md](sehens/tundra/katalog.md) |
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
| kueste | `kueste_pfad_klippensteig` | serpentine | 4 269 m | 33° | 5 |
| kueste | `kueste_pfad_kap` | trampelpfad | 1 893 m | 27° | 3 |
| oedland | `oedland_pfad_oedlandpfad_abstieg` | serpentine | 491 m | 20° | 4 |
| oedland | `oedland_pfad_oedlandpfad_ost` | trampelpfad | 828 m | 8° | 2 |
| oedland | `oedland_pfad_oedlandpfad_west` | trampelpfad | 551 m | 8° | 2 |

Zusammen 20 612 m. Kurze Zugänge mit Kehren vom Weg zum Ort stehen als `pfad_cm` am Ort und zählen nicht als Weg.

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/aue/katalog.md](sehens/aue/katalog.md)

### 1 · Biberstau (`aue_01_biberstau`) – Fundstück

**Was man sieht.** Im dunklen Nadelwald am Westrand der Aue hört man zuerst Wasser, das nicht rauscht, sondern über eine Kante
rieselt. Dann öffnet sich zwischen den Stämmen ein stiller, teebrauner Teich – und quer durch den Bach liegt, sauber gebogen wie
von Hand, ein 24 m langer Damm aus Ästen, Knüppeln und Schlamm. Am Nordufer ein mannshoher Hügel aus Zweigen: die Burg. Drei
Fichten stehen ertrunken und grau im Wasser, an den Ufern zugespitzte Stümpfe, eine gefällte Espe liegt mit der Krone im Teich,
und überall weiße Späne.

**Vorbild.** Biberdämme im Bayerischen Wald und in Kanada (Algonquin); Spiel: die stillen Waldweiher in Velen (Witcher 3),
Biberteiche in Red Dead Redemption 2.

**Standort.** Feld C4, X −2530 / Y −840, Boden 34,3 m. Bach B_R2_R_M1_M1_04 (4 m breit) fließt hier mit 5–6 % Gefälle nach
Osten (34,8 m bei −2534 → 33,1 m bei −2520); Einzugsfläche 0,076 km². Boden Nadeln 87 % / Kies 11 %, Hang 4° (max 32° an
der Bachkerbe), TPI25 −0,9 m, TPI100 −1,5 m – eine flache Rinne im Wald. 144 m vom Weg, 321 m vom Rand der Stadt ROMAN_LOC_007,
120 m innerhalb des Biom-Rechtecks (Westgrenze zum Bergwald), 457 Baumzellen im Radius, Bäume bis 29 m. **Sicht:** vom Weg
völlig verdeckt (max. Anteil 0,00 an 77 Wegpunkten ≤ 400 m, alle 9 Probepunkte verdeckt).

**Komposition und Anmarsch.** Zugang 146 m vom Weg (−2673/−835) von Westen, streng erreichbar (max 14,8°, Mittel 7,3°, 18 m
Furt über den Bach → 4 Trittsteine `SM_flat_rock_02`). `_anmarsch` 38 m westlich am Teichende: man sieht über den Spiegel auf
die Burg. `_held` von unterhalb (Osten, 30 m, −2502/−824) auf den Damm: Vordergrund Rinnsal über Kies, Mitte die Dammkrone mit
dem Überlauf, Hintergrund der Teich mit den grauen Fichten und Lichtflecken. `_nah` 13 m: Dammkrone, Schlamm, Späne.

**Detail-Ebenen.** Held: der Damm – 24 m Bogen flussab gewölbt, 1,6 m hoch, aus `SM_OldTreeBranch_01…05`, `SM_trunk_01/02`,
`SM_dead_log_01/03` quer und `SM_detail_branches_01…03` eingeflochten; Schlamm-Lage auf der Wasserseite. Begleiter (5): Burg
(Haufen aus denselben Ästen + `SM_BrokenTreeAssembly_01`, 4,5 m Ø), 3 ertrunkene Fichten (`Fir_08_Dead_NoBillboard`,
`SM_Forest_pine_10_dead` ×0,7), gefällte Espe (`SM_LargeFallenTree_02`). Schutt (40–60): Nagestümpfe (`SM_BirchTreeStump_01`,
`SM_TreeStump_01`, `SM_RottenTreeStump_02`, schräg eingegraben), Knüppel im Wasser, Schwemmäste an der Dammfront. Kleinzeug:
Späne-Decal `MI_ScatteredBark_01`, `MI_Sticks_01`, `SM_SmallStonesPack_03` im Überlauf. Bewuchs nach Ursache: Licht fällt, wo
die Biber gefällt haben → Stockausschläge der Espe (`SM_Poplar_plant_A_00/C_00`), Rohrkolben und Binsen nur im Flachwasser am
Einlauf (`SM_Rohrkolben_Horst_1/3`, `SM_ToadRush_00/010`), Farn am feuchten Hangfuß (`SM_SilverLadyFern_03`). Kontakt: Damm 30 %
im Bachbett, Wurzeln `SM_MossyForestRoots_02` an der Uferkante, Nassband `MI_TileableLeakage_01` an den Stämmen auf Spiegelhöhe.

**Wasser, Effekte, Licht.** `see` Stauteich ~42 × 22 m, Spiegel ≈ 34,6 m, 1,2–1,8 m tief, Farbe `moorbraun`; der bestehende
Bach beginnt unter dem Damm neu (Überlaufrinne, Stufe 1,2 m → kleiner Schleier, Schaum nur dort). Ein lokaler Nebel über dem
Teich (Dichte 0,04). Lichtschacht durch die Lücke, die die Biber geschlagen haben – reines Sonnenlicht, kein Zusatzlicht.

**Geländeänderung.** Teichbecken −0,5…−1,4 m (oberhalb des Damms, flach zu den Ufern), Dammfuß +0,4 m; Fenster 90 × 70 m,
|Δ| ≤ 1,5 m, das Becken ist Wasser (keine trockene Senke). Lagen: Schlamm am Ufer, Kies im Überlauf, Moos am Hangfuß.

**Assets.** Bestand wie oben (alle in `netze.csv`, keiner gesperrt). Wunsch: Erlen-Paket „Megascans Trees: European Black Alder“
(neu, C) für die Ufer; Klang Free City & Nature Sounds (B). Lücke: angenagter Sanduhr-Stumpf und Biberburg → aus Bestand gebaut.

**Aufwand und Risiko.** Mittel (≈ 60 Akteure, ~3 500 Instanzen). Risiko: Damm aus Einzelästen wirkt leicht „gestapelt“ –
Schlamm-Lage und Gras zwischen den Ästen sind Pflicht; `Fir_08_*` ist kein Nanite (nur 3 Stück).

---

### 2 · Die Alte (`aue_02_die_alte`) – Leuchtfeuer

**Was man sieht.** Mitten in der Bachwiese von C4, zwischen zwei Bacharmen, steht ein einzelner Baum, der die ganze Ebene
beherrscht: eine uralte Stieleiche, 34 m hoch und ebenso breit, der Stamm hohl und 3,5 m dick, die unteren Äste so schwer, dass
sie fast den Boden berühren. Ein Blitz hat vor Jahren einen Starkast abgerissen; er liegt noch da, bemoost, voller Pilze. Unter der
Traufe ein dunkler Ring aus Brennnessel und Holunder, außerhalb leuchten Inseln aus Margeriten und Flockenblumen. Drei junge
Eichen stehen verstreut in der Wiese – die Häher haben die Eicheln der Alten vergraben.

**Vorbild.** Major Oak (Sherwood), die Ivenacker Eichen; Spiel: die Einzelbäume in Velen und Toussaint (Witcher 3).

**Standort.** Feld C4, X −2282 / Y −552, Boden 24,2 m. Offene Wiese (Wiese 87 %, Trockengras 13 %), Relief nur 2,3 m im 40-m-Kreis,
4 Baumzellen im Radius (Baumdichte 1 %), Bach 0–8 m entfernt (Wurzeln greifen ins Ufer; Einzugsfläche dort 0,5 km²). 270 m vom Weg,
179 m vom Rand der Stadt ROMAN_LOC_010, 334 m innerhalb des Bioms. Ausgewählt als Punkt mit der größten Fernwirkung im Umkreis von
90 m (Feinsuche, 8-m-Gitter). **Sicht:** Mit 30 m Zielhöhe sehen 83 von 328 Wegpunkten im Ring 300–800 m mindestens 30 % der
Silhouette (Mittel 0,21), lesbar bis 798 m; bester Punkt (−1986/−150) in 499 m mit Anteil 0,98.

**Komposition und Anmarsch.** Blickziel ist die Krone gegen den Himmel über der flachen Wiese – die Ebene macht den Baum groß.
`_fern` von der Straße im Nordosten (499 m, Anteil 0,98), `_anmarsch` 213 m vor dem Baum am Zugangspfad (Anteil 0,51, die
Bacherlen rahmen links), `_held` 87 m von Südosten (−2214/−606), Ziel 12 m über dem Boden: Vordergrund Blumeninsel, Mitte der
Traufschatten, Hintergrund das Bergwald-Gebirge im Dunst. `_nah` 10 m: Stammfuß, Höhlung, Wurzelanläufe. Zugang 330 m vom Weg
(−2451/−299), streng erreichbar (max 11°, 6 m Furt über einen Bacharm → Trittsteine).

**Detail-Ebenen.** Held: Stieleiche aus „Quercus Robur – Nanite & Impostor“ (neu, B), Ersatz `SM_Poplar_tree_06_Optimised` ×1,3
(34,5 m) – dann eine **Schwarzpappel**, ebenso auentypisch; Stammfuß 30 % eingegraben, Wurzelanläufe `SM_beech_old_roots_01`,
`SM_crooked_root_01/04`, `SM_MossyForestRoots_01/03`. Begleiter (4): abgebrochener Starkast (`SM_LargeFallenTree_02` +
`SM_OldTreeBranch_05/06`), 3 Jungeichen `SM_dry_oak_01_B`, `SM_dry_oak_01_D`, `SM_dry_oak_02_A`. Schutt (30–50): Totäste unter
der Krone, Rindenstücke (`MI_ScatteredBark_01`). Kleinzeug: Laub `SM_DeadLeaves_03`, `SM_detail_leaves_01` nur im Traufkreis.
Bewuchs nach Ursache: Schatten und Vogelkot unter der Krone → Brennnessel (`SM_nettle_01_0/1_*`) und Holunder (`SM_Elderberry_03/07`);
offene Wiese → Blumeninseln (`SM_flower_chamomile_01`, `SM_flower_brownray_knapweed_01`, `SM_meadow_daisy_01`,
`SM_flower_common_Saint_John_s_wort_01`) in 3 Klumpen auf der Sonnenseite, hohes Gras `SM_grass_meadow_02/04`. Kontakt:
Moos-Decal `MI_TileableMossPatches_02` am Stammfuß Nordseite, Erde-Lage im Traufring (zertreten vom Wild).

**Wasser, Effekte, Licht.** Bestehender Bach am Fuß. Optional Pollen-/Samenflug im Gegenlicht („Free Niagara Particles“, C).
Kein Licht, kein Nebel – die Alte lebt vom Tageslicht und ihrem Schatten.

**Geländeänderung.** Flacher Wurzelhügel +0,4…+0,8 m (Ø 30 m), Fenster 60 × 60 m. Lagen: Erde/Laub im Traufkreis, Kraut am Rand.

**Assets.** Bestand wie oben. Wunsch: Stieleiche (B, neu), Pilze (Forest Fungi, C), Klang (B). Lücke: hohler Stamm – kommt mit
dem Eichenpaket; mit dem Pappel-Ersatz entfällt die Höhlung.

**Aufwand und Risiko.** Gering bis mittel (≈ 25 Akteure, ~4 000 Instanzen). Risiko: ohne Eichenpaket wirkt die Pappel schlanker;
Skalierung > 1,3 macht Blätter zu groß.

---

### 3 · Schwalbenwand (`aue_03_schwalbenwand`) – Leuchtfeuer

**Was man sieht.** Südlich des großen Flussbogens bricht die Terrasse in einer 9–10 m hohen, fast senkrechten Wand aus
ockerfarbenem Lehm und Sand ab – der alte Prallhang, an dem der Fluss nagte, bevor er nach Norden wanderte. Im oberen Drittel
durchlöchern Hunderte Brutröhren der Uferschwalben die Wand in lockeren Bändern; darunter Rinnspuren, herausgebrochene Schollen
und ein Schuttkegel. Oben auf der Kante stehen drei Schwarzpappeln, eine hängt mit freigespülten Wurzeln schon halb über dem
Abgrund. Am Fuß liegt die alte Flussrinne – feucht, mit Pestwurz, Schachtelhalm und Pfützen.

**Vorbild.** Steilufer der Elbe und Oder (Uferschwalben-Kolonien), Loess-Abbrüche am Kaiserstuhl; Spiel: die Lehmabbrüche am
Pontar (Witcher 3), Flussufer in Kingdom Come: Deliverance.

**Standort.** Feld C5, X −2160 / Y 82, Boden 13,8 m (Fuß). Die Stufe fällt in den Daten von 22,7 m (Terrasse) auf 13,9 m auf nur
10 m Breite, bis 63–69° (Boden Fels an der Steilstelle −2120/60), Relief 10,9 m im Radius; sie zieht sich 130 m von −2250 bis
−2122. Nördlich der Terrasse fließt der Hauptfluss (38 m), südlich liegt die tiefere Rinne (12,6 m). Boden Wiese 56 %, Geröll
26 %, Gras 12 %. 267 m vom Weg, 215 m vom Stadtrand ROMAN_LOC_019, 402 m innerhalb des Bioms. **Sicht:** Mit 12 m Zielhöhe
(Wand + Pappelfuß) sehen 70 / 333 Wegpunkte im Ring 300–800 m ≥ 30 % (Mittel 0,16), bis 795 m; aus dem Südsektor (Blick nach N
± 60°, also auf die Wandfläche) **33 von 54** Wegpunkten. Die Pappeln auf der Kante (25 m) wirken weiter.

**Komposition und Anmarsch.** `_fern` von der Straße im Südwesten (−2482/468, 503 m, Anteil 0,67): die helle Wand als
waagrechter Streifen unter der dunklen Pappelreihe. `_anmarsch` vom Wegpunkt (−2487/275), 380 m, Anteil 0,78. `_held` 85 m
aus der Altrinne (−2188/158), Ziel Wandmitte (5 m über Fuß): Vordergrund Pestwurz und Pfütze mit Spiegelung der Wand, Mitte
Schuttkegel, oben die überhängende Pappel gegen den Himmel. `_nah` 10 m: Brutröhren, Wurzelvorhang, Schollen. **Pfad nötig:**
411 m vom Weg (−2487/275) durch die Rinne, max 12,8°, aber 4 m Bach + 15 m Furt → Trittsteine (`SM_flat_rock_02/03`) und
Erde/Kies-Band 1,2 m. (Der nächste Weg in 267 m liegt jenseits des Flusses – deshalb Zugang von Süden.)

**Detail-Ebenen.** Held: Wand aus Klippenschalen `SM_beach_cliff_02_A/B/C` (6,6–6,8 m) gestaffelt und `SM_beach_cliff_01_A/B`
darüber, Abbruchkante oben `SM_beach_escarpment_01_A`, alle mit Materialwunsch `MI_EL_SW_Lehmwand`; Brutröhren als Decal
(Lücke, s. u.). Begleiter (5): 3 Schwarzpappeln auf der Kante (`SM_Poplar_tree_05/07_Optimised`, `Poplar_02_Standalone`), die
kippende Pappel (`SM_Poplar_tree_04` 25° geneigt) mit freigelegtem Wurzelteller (`SM_Pine_roots_01`, `SM_crooked_root_021`),
eine abgestürzte Scholle (`SM_sandy_slope_05`). Schutt (60–120): Schuttkegel unter den Rinnen aus `SM_sandy_slope_01/02/03`,
`SM_scarp_01/02`, `SM_Rock_02`, `SM_ForestRockFormation_02`, unten gröber. Kleinzeug: `SM_s_rock_01`, `SM_SmallStonesPack_05`,
Wurzelvorhang aus `SM_crooked_roots_small`, `SM_ForestRoots_01/02` an der Oberkante. Bewuchs nach Ursache: Wand kahl (sie
bricht nach), nur Grasbüschel auf Simsen (`SM_grass_bush_02`); feuchte Rinne → Pestwurz (`SM_petasites_spurius_01`),
Schachtelhalm (`SM_rough_horsetail_01`), Rohrkolben in der Pfütze (`SM_Rohrkolben_Horst_2`, `SM_ToadRush_02`); trockene Kante →
Seifenkraut (`SM_flower_bouncing_bet_01`). Kontakt: Schalen 30–40 % eingegraben, Sickerstreifen `MI_Leakage_04` unter den
Rinnen, Nassband `MI_TileableLeakage_03` am Fuß.

**Wasser, Effekte, Licht.** 2 kleine `see` in der Rinne (Pfützen 6–10 m, `klar`, 0,4 m). Kein Effekt nötig; die Südwand steht
voll in der festen Sonne (warmer Ocker gegen kühlen Schatten der Rinne – das Witcher-Kontrastpaar).

**Geländeänderung.** Wand versteilen: Fuß −1…−2 m zurücknehmen, Kante +0,5 m, Schuttkegel +0,5…+1,5 m modellieren, Rinne
−0,5…−1 m mit Pfützen (Abfluss nach Osten erhalten). Fenster 200 × 90 m, |Δ| ≤ 3 m; Fluss liegt ≥ 30 m nördlich (keine
Änderung am Wasser). Lagen: Lehm/Sand an Wand und Kegel, Schlamm/Moos in der Rinne.

**Assets.** Bestand wie oben. Paket: Coast & Dunes (A, Lehm-/Nassufer-Decals), Klang (C). Lücke: Brutröhren – kleine eigene
Maskentextur für ein Decal aus `M_MS_Decal` (Begründung: kein Asset zeigt Erdlöcher; ohne sie ist es nur „eine Wand“).

**Aufwand und Risiko.** Mittel bis hoch (≈ 50 Akteure, ~5 000 Instanzen). Risiko: Klippenschalen aus dem Küstenpaket dürfen
nicht nach Meer aussehen → Materialwunsch ist Pflicht; neue Decal-Textur braucht Ferats Zustimmung.

---

### 4 · Treibholzwerder (`aue_04_treibholzwerder`) – Leuchtfeuer

**Was man sieht.** Mitten im Strom liegt eine lange Kiesinsel. Ihr flussaufwärts gerichteter Kopf ist unter einem Berg aus
silbergrau gebleichtem Treibholz begraben – 6 m hoch verkeilte Stämme, Wurzelteller, Äste, darüber eine ganze Pappel, die das
letzte Hochwasser mit dem Wurzelteller voran hier abgesetzt hat. Hinter dem Verhau haben sich Silberweiden angesiedelt, zum
Inselende hin läuft eine weiße Kiesfahne aus, auf der junge Weiden und Pappeln keimen. Das Wasser rauscht am Holz.

**Vorbild.** Verklausungen am Tagliamento und an der Isar (Pupplinger Au), Treibholzinseln der Loire; Spiel: die Flussinseln am
Pontar (Witcher 3), Treibholz in „The Last of Us Part II“-Flussauen.

**Standort.** Feld D5 (Rand E5), X −730 / Y 494, Boden 19,7 m. Kiesinsel ~100 × 30 m (Sand 47 %, Geröll 29 %, Schlamm 12 %),
1–2 m über dem Wasser, zwischen Hauptstrom (Süden) und Seitenarm F_ALTARM_FLUSSAUE_D5 (Norden, 8–17 m breit). Strom von West
nach Ost → der Inselkopf (−760…−742) fängt das Treibgut. Keine Bäume heute, Einzugsfläche 5,3 km². 273 m vom Weg, 257 m vom
Stadtrand RES_CH41_LOC_006, 275 m innerhalb des Bioms. **Sicht:** Mit 12 m (Verklausung + Weiden) sehen 57 / 343 Wegpunkte ≥ 30 %
(Mittel 0,14), bis 792 m; bester Punkt (−662/988) südlich in 499 m mit vollem Anteil – über die offene Wasserfläche frei.

**Komposition und Anmarsch.** `_fern` vom Südufer-Weg (499 m): die helle Holzburg vor dunklen Weiden auf dem Wasser.
`_anmarsch` 213 m am Zugang von Nordwesten, `_held` 120 m von der Furt am Seitenarm (−807/402): Vordergrund Kies und
Trittsteine im strömenden Arm, Mitte der Verhau mit der Pappel, Hintergrund der breite Strom und das Südufer. `_nah` 10 m:
verkeilte Stämme, Wurzelteller, Spülsaum. **Pfad nötig:** 313 m vom Weg (−917/265), flach (max 9°), aber der Seitenarm muss
gequert werden (10 m Wasser, 36 m Furtbereich) → **Furt** aus Trittsteinen `SM_flat_rock_02/03`, `SM_SmoothRockShelf_01` auf
einer Kiesschwelle (nur Netze, das Wasser bleibt unverändert).

**Detail-Ebenen.** Held: Treibholzburg aus „Nanite Driftwood Props“ (neu, A: Haufen + Stämme), Ersatz `SM_LargeFallenTree_01/02`,
`SM_OldFallenTree_01/02`, `SM_FallenSpruceTree_01`, `SM_BrokenTreeAssembly_01`, `SM_trunk_01/02` mit Materialwunsch
`MI_EL_SW_Treibholz` (gebleicht). Begleiter (6): gestrandeter Baum (`Fir_08_Dead_NoBillboard` liegend) mit Wurzelteller
(`SM_Pine_roots_01/02`, `SM_stones_roots_01/02` hochkant), 3 Weiden (`Big_Tree_Willow_01/02`) hinter dem Verhau (Strömungsschatten).
Schutt (80–150): Äste `SM_OldTreeBranch_01/03/05`, `SM_beach_driftwood_01`, Kiesrücken `SM_NordicBeachRockyGround_01/02`,
`SM_BeachSandWithPebbles_01`, `SM_DryRiverBed_01`. Kleinzeug: `SM_SmallStonesPack_01/07/12` (Hunderte, nach Größe sortiert:
grob am Kopf, fein an der Fahne), Spülsaum-Decals `MI_SticksAndTwigs_01`, `MI_ScatteredSticksAndTwigs_01`. Bewuchs nach Ursache:
Pioniere nur auf der Kiesfahne im Strömungsschatten (`SM_grey_willow_02/04`, `SM_Poplar_plant_A_00/B_00`), Pestwurz am
Feuchtrand (`SM_petasites_spurius_02`), Strandgras-artige Büschel (`SM_beach_grass_02_1`) auf Sand. Kontakt: Stämme halb im
Kies und im Wasser, Nassband `MI_TileableLeakage_02` 0,3 m über Spiegel an allem Holz.

**Wasser, Effekte, Licht.** Bestehendes Wasser; Schaum nur an der Holzfront (Material-Schaum, kein Niagara). Optional
Pappelsamen-Flocken (C). Kein Licht.

**Geländeänderung.** Inselkopf +0,5…+1,0 m Kiesrücken unter dem Verhau, Fahne flach ausziehen; Fenster 140 × 60 m, |Δ| ≤ 1,2 m,
mindestens 3 m Abstand zum Wasser. Lagen: Kies/Geröll am Kopf, Sand an der Fahne, Schlamm in Mulden.

**Assets.** Bestand wie oben. Pakete: Nanite Driftwood Props (neu, A), Coast & Dunes (A, Nassband/Kiesel), Erle (C), Klang (B).

**Aufwand und Risiko.** Mittel (≈ 70 Akteure, ~6 000 Instanzen, 1 200 mit Kollision). Risiko: ohne Treibholzpaket sehen
Waldstämme mit Moos/Rinde falsch aus – Bleich-Material nötig; Ufer-Instanzen dürfen nicht im Wasser schweben (Spiegel 18–20 m).

---

### 5 · Lilienrinne (`aue_05_lilienrinne`) – Fundstück

**Was man sieht.** Zwischen den Gehölzinseln der Hartholzaue zieht eine flache, gewundene Mulde durch die Wiese – ein alter
Flutarm, den der Fluss nur bei Hochwasser noch füllt. Vom Weg ist sie unsichtbar. Tritt man zwischen den Weidenbüschen
hindurch, liegt plötzlich ein goldenes Band vor einem: Sumpf-Schwertlilien, dazwischen purpurner Blutweiderich und weißes
Mädesüß, in der tiefsten Stelle ein klarer Tümpel mit Kaulquappen. Ein Saum aus angeschwemmtem Reisig in den Weiden zeigt, wie
hoch das Wasser zuletzt stand.

**Vorbild.** Flutrinnen der Elbtalaue und am Oberrhein (Taubergießen); Spiel: Wildblumensenken in Toussaint (Witcher 3),
Feuchtwiesen in Kingdom Come.

**Standort.** Feld E5, X −420 / Y 214, Boden 12,9 m. Die Daten zeigen eine natürliche Tiefenlinie parallel zum Fluss: von
(−600/246, 17,3 m) über (−460/242, 14,2 m) und (−420/214, 12,9 m) nach (−340/196, 11,2 m), 2,3 % Gefälle, TPI25 −0,8 m, TPI100
−1,7 m, Einzugsfläche 0,084 km². Boden Wiese 88 %, Hang 3° (max 12°). Gehölzinseln ringsum (1 100 Baumzellen im 70-m-Radius,
bis 29 m). 148 m vom Weg, 214 m vom Stadtrand ROMAN_LOC_004, 301 m innerhalb des Bioms, Fluss 220 m südlich. **Sicht:** verdeckt
(0,00 an 72 Wegpunkten ≤ 400 m), 9/9 Probepunkte – entlang der Rinne nur bei −540/286 und −420/214 robust (deshalb hier).

**Komposition und Anmarsch.** Zugang 152 m vom Weg (−529/109) von Nordwesten durch die Gehölze, streng (max 7°). `_anmarsch`
19 m vor der Mitte – erst dort öffnet sich die Rinne (Anteil springt auf 1,0). `_held` 82 m westlich in der Rinne (−497/242),
Blick nach Osten **längs** der Rinne: Vordergrund Lilien, Mitte Tümpel mit Spiegelung, Hintergrund die dunkle Gehölzwand –
die Rinne führt das Auge. `_nah` 10 m: Lilienblüten, Schlammrisse, Spülsaum.

**Detail-Ebenen.** Held: das goldene Band (Lücke Schwertlilie → `SM_Crownbeard_01/03/08` gelb zwischen schwertförmigen Blättern
von `SM_Rohrkolben_Jung_1/2`), 40 m lang, 4–8 m breit, nur im Rinnenboden. Begleiter: 2 purpurne Inseln
(`SM_flower_brownray_knapweed_01/02` mit `MI_EL_SW_Weiderich`), Mädesüß/Windröschen (`SM_WhiteWindflower_02`,
`SM_flower_chamomile_02`), Seifenkraut am trockenen Rand (`SM_flower_bouncing_bet_01`), Weidenbüsche als Rahmen (`SM_grey_willow_03/04`,
1 `Big_Tree_Willow_01`). Schutt (30–50): Spülsaum in einer Linie quer zur Rinne (`SM_detail_branches_02/03`, `SM_OldTreeBranch_04`,
`SM_dead_log_02`, Decal `MI_SticksAndTwigs_01`) – alle in Fließrichtung ausgerichtet. Kleinzeug: `SM_SmallStonesPack_09` im
Tümpel, Schlammrisse (Lage Schlamm + `MI_TileableLeakage_04`). Bewuchs nach Ursache (Feuchtegradient quer zur Rinne): Tümpel →
Binsen/Schachtelhalm (`SM_ToadRush_011`, `SM_rough_horsetail_02`) → Lilien/Weiderich → Pestwurz (`SM_petasites_spurius_01`) →
Wiese `SM_grass_meadow_01/03`. Kontakt: Pflanzen in Klumpen, nichts gleichmäßig; Nassband am Tümpelrand.

**Wasser, Effekte, Licht.** `see` Restwassertümpel ~10 m Ø, `klar`, 0,6 m tief (Ufer per Stempel rundum höher, Abfluss über
die Rinne nach Osten). Lokaler Bodennebel in der Rinne (Dichte 0,05, starker Höhenabfall). Optional Mückenschwarm (C).

**Geländeänderung.** Rinne entlang der Tiefenlinie −0,8…−1,5 m (8–14 m breit, 180 m lang), Tümpel −2,2 m, weiche Ränder ≥ 8 m;
Fenster 220 × 120 m, |Δ| ≤ 2,2 m; Gefälle bleibt stetig nach Osten (keine geschlossene Senke außer dem Tümpel mit Wasser).

**Assets.** Bestand wie oben. Pakete: Niagara Examples (C), Driftwood (C), Klang (B). Lücke: Schwertlilie/Blutweiderich (s. o.).

**Aufwand und Risiko.** Gering bis mittel (≈ 10 Akteure, ~9 000 Instanzen, kaum Kollision). Risiko: die Ersatzblumen sind
keine Iris – aus der Nähe erkennbar; Farbwirkung aus 10–30 m trägt.

---

### 6 · Mondarm (`aue_06_mondarm`) – Fundstück

**Was man sieht.** Vom Weg aus nur ein Weidengebüsch. Geht man durch eine Lücke im Weidenvorhang, steht man am Ufer eines
hufeisenförmigen, spiegelglatten Altwassers – eine abgeschnittene Flussschlinge, die wie eine Mondsichel um eine Halbinsel aus
Wiese und alten Weiden liegt. Teich- und Seerosen bedecken die Buchten, Rohrkolben säumen den Einlauf, eine umgestürzte
Silberweide liegt quer im Wasser und treibt trotzdem grün aus. Im Wasser spiegeln sich die Weiden und der Himmel.

**Vorbild.** Altwasser der Donau (Donauauen bei Wien), Elbaltarme; Spiel: die Teiche bei Crookback Bog (Witcher 3, ohne
Sumpfgrusel), Weiher in Red Dead Redemption 2.

**Standort.** Feld E5, X −240 / Y 740, Boden 19,2 m (Südufer). Das Altwasser (Teich T_K2_FLUSSAUE_00 und die anschließende
Wasserfläche, Spiegel 13,2 m) liegt 5–6 m unter der Uferkante, das Ufer ist bis 62° steil (Uferabbruch), Zulauf eines Baches
von Süden bei −265/750. Boden Wiese 50 %, Schlamm 20 %, Trockengras 18 %; 651 Baumzellen im Radius. 84 m vom Weg, 249 m vom
Stadtrand RES_CHEP_LOC_005, 242 m innerhalb des Bioms. **Sicht:** Mitte verdeckt (0,00 an 48 Wegpunkten ≤ 400 m), aber nur 3/9
Probepunkte – der Weg liegt 50–150 m südlich am Hang. Deshalb plane ich einen **Weiden-/Erlengürtel** (9–12 m hoch, 12 m
breit, 220 m lang) zwischen Weg und Ufer; mit ihm im Baumraster gerechnet (`schirm.py`): **9/9 verdeckt**. Der Gürtel ist der
natürliche Weichholzsaum eines Altwassers und gehört ohnehin zur Szene.

**Komposition und Anmarsch.** Zugang 99 m vom Weg (−265/829), streng (max 10,6°), 18 m Furt über den Zulaufbach (Trittsteine).
`_anmarsch` 42 m vor der Mitte in der Weidenlücke (Anteil 1,0 – hier öffnet sich der Blick). `_held` vom Südufer (−235/739)
nach Westnordwest über die Bucht auf das Seerosenfeld (Ziel Spiegel + 0,5 m): Vordergrund Röhricht, Mitte Seerosen und die
liegende Weide, Hintergrund die Halbinsel mit Weidenkronen. `_nah` 10 m: Ufer, Wurzeln, Rosenblätter.

**Detail-Ebenen.** Held: Seerosen-/Teichrosenfelder (2 Buchten) aus „Megascans Rembrandt Water Lily“ (A), Ersatz
`SM_WaterPlant01…04`, `SM_lily_01_1`. Begleiter (6): liegende Weide (`Big_Tree_Willow_01` 70° gekippt + `SM_LargeFallenTree_02`
als Stamm), 4 Uferweiden (`Big_Tree_Willow_01/02`, `SM_Poplar_tree_03_Optimised`), Eisvogel-Ast (`SM_OldTreeBranch_05` übers Wasser).
Schutt (30–60): Schwemmholz `SM_OldFallenTree_02` am Einlauf, freigespülte Wurzeln am Abbruch (`SM_crooked_root_031/05`,
`SM_MossyForestRoots_01`). Kleinzeug: Laub im Flachwasser, Röhricht-Halme. Bewuchs nach Ursache: Röhricht nur am flachen
Einlauf und in den Buchten (`SM_Rohrkolben_Horst_1/4/6`, `SM_Rohrkolben_Jung_3`, `SM_ToadRush_012`), Pestwurz und Schachtelhalm
auf dem Schlammsaum (`SM_petasites_spurius_03`, `SM_rough_horsetail_03`), Holunder am trockenen Oberhang (`SM_Elderberry_05`),
Weidengürtel (`SM_grey_willow_01…04` + Weiden/Erlen). Kontakt: Nassband `MI_TileableLeakage_01`, Moos `MI_TileableMossPatches_01`
an den Wurzeln, Schlamm-Lage am Ufer.

**Wasser, Effekte, Licht.** Bestehendes Wasser (Farbe bleibt; Wunsch: `smaragd` statt Flussgrün, falls der Teich eine eigene
Instanz bekommt). Ein lokaler Nebel über dem Spiegel (Dichte 0,03, sehr flach). Optional Mücken (C). Kein Licht.

**Geländeänderung.** Keine Form; nur Bodenlagen (Schlamm, Moos, Kraut) und ein 3-m-Pfad (Erde) durch den Gürtel. Fenster 120 × 80 m.

**Assets.** Bestand wie oben. Pakete: Water Lily (A), Erle (neu, B, für den Gürtel), Niagara Examples (C), Klang (A).

**Aufwand und Risiko.** Mittel (≈ 30 Akteure, ~7 000 Instanzen). Risiko: der Fundstück-Charakter hängt am Weidengürtel – er
muss vor dem Ort gebaut werden; die Wasserfläche ist ein bestehendes Houdini-/Epic-Wasser (Uferhöhe prüfen).

---

### 7 · Blautopf (`aue_07_blautopf`) – Fundstück

**Was man sieht.** In einer Kerbe des Laubwalds, unter einem halbrunden Kalkfelsen, liegt ein kreisrunder Topf voller Wasser
von unwirklichem Blau – so klar, dass man die Felsen und einen versunkenen Stamm in 9 m Tiefe sieht, und doch so tief, dass die
Mitte fast schwarz wird. Am Rand Moos, Hirschzungenfarn, Efeu an der Wand; aus dem Topf fließt still der Bach, der unten nach
Norden zur Küste rinnt. Vom Weg hört man ihn, sieht ihn aber nicht.

**Vorbild.** Blautopf (Blaubeuren), Aachtopf, Fontaine de Vaucluse; Spiel: die Quellen in Toussaint (Witcher 3), Plitvice-Quellen
in „Kingdom Come“.

**Standort.** Feld F4, X 1166 / Y −834, Boden 27,1 m. **Anfang des Bachs B_R_P2_M1_01** (Quelle z 27,9 m bei 1166/−828; er
fällt auf 195 m bis 0,6 m) – der Topf sitzt genau am Bachanfang, am Talschluss einer Kerbe: TPI25 −2,8 m, TPI100 −9,6 m, Relief
20,6 m im 40-m-Kreis, Hang 19° (max 42°) – der halbrunde Hang hinter der Quelle ist die Felswand. Boden Laub 86 %, Moos 8 %,
Kies 6 %; 302 Baumzellen, bis 24 m. 87 m vom Weg (der oben hinter der Kante verläuft), 1 250 m vom nächsten Stadtrand, 186 m
innerhalb des Bioms. **Sicht:** verdeckt (0,00 an 77 Wegpunkten ≤ 400 m), 9/9 Probepunkte.

**Komposition und Anmarsch.** Zugang 90 m vom Weg (1179/−749), streng (max 20,8°, Mittel 13°) – ein Steig an der Ostseite der
Wand hinab (Erde/Laub-Band, 3 Trittstufen `SM_flat_rock_02`). `_anmarsch` 55 m oberhalb auf der Kante (1175/−780): der erste
Blick **von oben** in das Blau. `_held` 35 m bachab von Norden (1158/−858): Vordergrund der Bach über Kies, Mitte der Topf,
Hintergrund die Kalkwand mit der überhängenden Buche. `_nah` 12 m vom Ostrand (1178/−823): Uferplatten, Farn, Blick ins Wasser.

**Detail-Ebenen.** Held: der Topf (Wasser + Stempel), Rand aus Kalkplatten (`SM_ForestRockShelf_01`, `SM_ForestRockSlab_01`,
`SM_SmoothRockShelf_01`, `SM_LimestoneRocks2/3`; besser „Megascans Limestone Rocks“, B). Begleiter (5): Kalkwand 6–8 m im Halbrund
aus `SM_big_rock_wall_01/02/03`, `SM_HugeMossyForestCliff_01`, `SM_MossyRockFace_02` mit `MI_EL_SW_Kalk_Moos`; überhängende Buche
(`SM_beech_tree_06`), versunkener Stamm (`SM_LargeFallenTree_01`, 7 m tief, durchs Wasser sichtbar). Schutt (20–40): bemooste Blöcke
am Wandfuß (`SM_MossyForestBoulder_02/05`, `SM_MossyForestRock_02`). Kleinzeug: `SM_SmallStonesPack_06`, `SM_NordicBeachRock_01`
im Abfluss, Laub. Bewuchs nach Ursache: Dauerfeuchte und Kühle → Farne (`SM_Fern_02/04`, `SM_SilverLadyFern_05`, `SM_BeechFern_04`
als Hirschzungen-Ersatz), Moos (`SM_MossClump_01`) auf allen Kanten, Efeu an der Wand (`SM_EnglishIvy_03`), Pestwurz am Abfluss
(`SM_petasites_spurius_02`). Kontakt: Sickerstreifen `MI_Leakage_07` an der Wand, Moos-Decal `MI_TileableMossPatches_03`.

**Wasser, Effekte, Licht.** `see` Quelltopf ~20 m Ø (Umriss leicht oval), Spiegel ≈ 28,0 m, 9 m tief, Farbe `tiefblau`;
der bestehende Bach ist sein Abfluss (keine neue Bachgeometrie nötig, nur der Anfang 3 m verlegt). Lokaler Nebel in der Kerbe
(Dichte 0,04, kalte Luft). Optional Quellaufwallung in der Mitte („Nature Water FX“, C, kostenpflichtig). Kein Licht.

**Geländeänderung.** Topf als Trichter bis −9 m (Ø 20 m, Wände 35–60°), Wandfuß −1 m, Kalkwand-Sockel +1…+3 m im Halbrund;
Fenster 80 × 80 m, |Δ| ≤ 9 m (begründet: der Topf **ist** das Wasser), Rand Δ = 0, Weg bleibt unberührt (≥ 60 m). Lagen: Moos,
Kies am Abfluss, Fels am Rand.

**Assets.** Bestand wie oben. Pakete: Limestone Rocks (B), Nature Water FX (C), Klang (A). Keine Lücke.

**Aufwand und Risiko.** Mittel (≈ 35 Akteure, ~3 000 Instanzen). Risiko: das Blau steht und fällt mit dem Wassermaterial
(`tiefblau` + dunkler Grund); Uferhöhe muss rundum über 28,0 m liegen (Stempel prüfen).

---

### 8 · Lianenhalle (`aue_08_lianenhalle`) – Fundstück

**Was man sieht.** Am Prallufer des Elfenflusses steht ein Stück Urwald der Hartholzaue: alte Pappeln, Hainbuchen und Eichen,
deren Kronen sich zu einem Dach schließen. Von den Ästen hängen Vorhänge aus Waldrebe und Efeu bis zum Boden, wie Taue in einer
Halle. Darunter ein heller Teppich aus Buschwindröschen und Maiglöckchen, ein liegender Riesenstamm voller Pilze – und an allen
Stämmen, in 1,8 m Höhe, eine gerade graue Schlammlinie und Bündel aus Reisig in den Astgabeln: so hoch stand das letzte
Hochwasser. Ein einzelner Lichtschacht fällt durch eine Kronenlücke.

**Vorbild.** Hartholzauen an der Donau (Nationalpark Donau-Auen), am Rhein (Taubergießen) und der Elbe; Spiel: die Wälder um
Novigrad/Oxenfurt (Witcher 3), „Ghost of Tsushima“-Lichtschächte.

**Standort.** Feld F4, X 1196 / Y −470, Boden 16,9 m. Laubwald (Laub 97 %, Moos 3 %), 693 Baumzellen im 60-m-Radius (Baumdichte
24 %, bis 23 m), Hang 7,5° (max 16°), 58 m vom Elfenfluss (Prallufer seiner Rechtskurve). 210 m vom Weg, 1 233 m vom nächsten
Stadtrand, 156 m innerhalb des Bioms (Ostgrenze zum Elfenwald bei x ≈ 1350). **Sicht:** verdeckt (0,00 an 58 Wegpunkten),
8/9 Probepunkte (Feinsuche hat den robustesten Punkt gewählt).

**Komposition und Anmarsch.** Zugang 226 m vom Weg (1095/−653) von Nordwesten durch den Wald, streng (max 16,9°). `_anmarsch`
52 m vor der Mitte, wo der erste Vorhang sichtbar wird. `_held` 35 m von Südwesten (1174/−492), Ziel 5 m hoch: zwei Stämme als
Torpfosten, dazwischen der Lianenvorhang, dahinter der Lichtschacht auf dem Blütenteppich. `_nah` 10 m: Schlammlinie und Genist
am Stamm.

**Detail-Ebenen.** Held: der Lianenvorhang zwischen 4 Altbäumen (`SM_Poplar_tree_06/07_Optimised`, `Poplar_06_Forest`,
`SM_EuropeanHornbeam_Forest_02/04`; Stieleiche als Wunsch, C) – Lianen `SM_Vines_01a` (5,7 m) gereiht, `SM_Ivy_10/12/17`,
`SM_EnglishIvy_05` an den Stämmen. Begleiter (4): liegender Altstamm (`SM_LargeFallenTree_01`, `SM_MossyTree_01`), toter Biotopbaum
(`SM_EuropeanBeech_Dead_XL_01`), Wurzelstock (`SM_RottenTreeStump_01`). Schutt (40–80): Genistbündel in Astgabeln
(`SM_detail_branches_01/03`, `SM_OldTreeBranch_02`) alle auf 1,6–2,0 m Höhe, Totäste am Boden. Kleinzeug: `SM_DeadLeaves_05`,
`SM_ForestRoots_02`, Decal `MI_ScatteredSticksAndTwigs_01`. Bewuchs nach Ursache: nährstoffreicher Auenlehm + Frühlingslicht
→ Teppich aus `SM_WhiteWindflower_01/04`, `SM_LilyOfTheValley_02`, `SM_YellowArchangel_05`, `SM_Periwinkle_02`; Holunder in der
Lichtlücke (`SM_Elderberry_09`); im Kronenschatten nichts als Laub. Kontakt: **Schlammlinie** `MI_TileableLeakage_02` als waagrechtes
Band 1,6–1,9 m an allen Stämmen (alle gleich hoch!), Moos `MI_TileableMossPatches_02` darunter.

**Wasser, Effekte, Licht.** Kein Wasser im Ort (der Fluss blitzt durch die Stämme im Süden). Ein `spotlicht` als Lichtschacht
(warm, 6° Kegel, ohne Schatten, nur in der Halle wirksam) + ein lokaler Nebel (Dichte 0,06) macht den Strahl sichtbar.
Optional fallende Blätter im Schacht (C).

**Geländeänderung.** Keine Form. Lagen: Laub/Moos, Schlamm-Flecken in Mulden (Hochwasserablagerung). Fenster 100 × 100 m nur für Lagen.

**Assets.** Bestand wie oben (Hainbuchen = Megascans, laut `netz_check_ergebnis.json` „schwarz_mspresets“ → die automatische
Überschreibung ist nötig). Pakete: Stieleiche/tote Eiche (C), Pilze (C), Niagara VFX Laub (C), Klang (B). Lücke: Bärlauch →
Windröschen/Maiglöckchen.

**Aufwand und Risiko.** Mittel (≈ 40 Akteure, ~8 000 Instanzen). Risiko: Lianen aus Einzelstücken müssen geordnet hängen
(gerade nach unten, gebündelt), sonst „Lametta“; nahe der Elfenwald-Grenze – Pappeln/Hainbuchen statt Buchen halten das Bild
eindeutig „Aue“.

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/bergwald/katalog.md](sehens/bergwald/katalog.md)

### 1 · Der Mönch (`bergwald_01_der_moench`) – Leuchtfeuer

**Was man sieht.** Auf der Nase einer Felsrippe, dort wo die letzten Wetterkiefern des Grats stehen, ragt eine schlanke,
leicht geneigte Granitnadel 28 m über ihren Sockel – ein dunkler Finger über den Wipfeln, oben flechtengrau, unten moosig und
nass vom Sickerwasser. Darunter rieselt ein Schuttkegel in die Kerbe nach Nordnordost. Vom Talweg sieht man die Nadel als
Kerbe in der Gratlinie; erst am Grat merkt man, wie frei sie steht.

**Vorbild.** Barbarine und Mönch (Sächsische Schweiz), Old Man of Storr (Skye); Spiel: die Felsnadeln über Kaer Morhen (Witcher 3),
Skellige-Grate.

**Standort.** Feld B3, X −3408 / Y −1102, Boden 347,8 m. Nase einer N-fallenden Rippe: TPI100 +35,6 m, Landform Kuppe/Gipfel,
Relief 106 m im 40-m-Kreis; nach N −54 m und nach O −37 m auf 40 m, nach S steigt die Rippe +38 m – die Nadel steht also frei
vor dem Kamm. Boden Fels 67 % / Nadeln 26 %, Hang 52° (max 65°), Exposition 25° (NNO). 296 m vom nächsten Weg (−3114/−1132),
74 m vom Bach, 355 m vom Rand der Stadt ROMAN_LOC_021, 489 m innerhalb des Bioms. **Sicht:** Mit 32 m Zielhöhe sehen 66 von
175 Wegpunkten im Ring 300–800 m mindestens 30 % der Silhouette (Mittel 0,35), lesbar bis 800 m; bester Punkt (−3038/−1434) in
497 m mit vollem Anteil. Die Bäume des Grats (189 Baumzellen im Radius, max 24 m) verdecken nur den Sockel – genau das gewünschte
„über die Wipfel“.

**Komposition und Anmarsch.** Blickziel ist die Nadel vor dem Himmel bzw. vor dem Dunst über dem Meer (N). Vordergrund: Grat
mit Wetterkiefern, Mitte: Sockelblöcke, Hintergrund: die Kerbtäler und die Küste. `_fern` von der Straße im Osten (B3,
630 m, Anteil 1,0), `_anmarsch` 137 m vor dem Ort am Steig (Anteil 0,81), `_held` 117 m von SO am Rippenhang (Kamera 363 m, auf
Höhe der Nadelmitte; Anteil 0,58 – die Grat-Kiefern rahmen links), `_nah` 10 m (Sockel, Moos, Sickerstreifen). **Pfad nötig:**
662 m Steig vom Weg (−3063/−1085), Luftlinie 345 m, max 37°, Mittel 18°, 105 m steiler als 25° und 291 m durch Querhang > 38° →
Kehren mit Erde/Kies-Band 1,2 m und Trittstufen aus `SM_flat_rock_04`, im Steilstück Felsstufen (`SM_ground_rock_03_03`).

**Detail-Ebenen.** Held: Nadel aus `veqnci0db_tier_2` (22,9 × 37,7 × 33,8 m, Granit-Schale) hochkant, 6–8 m eingegraben →
~28 m sichtbar; Kappe/Grat aus `rcygn_tier_0`. Begleiter (5): Sockelblöcke `ukjhcamga_tier_0`, `SM_NordicBoulder_01`,
`SM_mountain_rock_big_02_7/_8`. Schutt (120–180): Schuttkegel hangab aus `SM_mountain_rock_big_01_1…5`, `SM_ground_rock_01`,
nach unten gröber (Sortierung des Kegels). Kleinzeug: `SM_mountain_rock_small_01_*`, `SM_stone_03…08`, Nadeln/Zapfen über
Landschaftsgras. Bewuchs nach Ursache: 3–5 Wetterkiefern am Grat (`SM_Forest_pine_06` 0,6× gestaucht, `SM_dwarf_pine_big_01`)
auf der windabgewandten Seite, Krähenbeere/Heide in Spalten (`SM_heath_A_01`, `SM_lingonberry_01`), Flechte als Auflage. Kontakt:
Nadel 25–35 % eingegraben, Moos über `M_EL_Fels_Auflage` nur auf der Nordseite, Kiessaum 2–4 m um den Sockel.

**Wasser, Effekte, Licht.** Kein Wasser; ein dunkler Sickerstreifen (`MI_TileableLeakage_02`, Decal 2 × 12 m) an der Nadel.
Ein lokaler Nebel in der Kerbe unterhalb (Dichte 0,05) trennt die Nadel vom Hintergrund. Kein Licht.

**Geländeänderung.** Klein: Sockelplateau 12 × 10 m um 0–2 m ausgleichen, Schuttkegel −1…+2 m modellieren; Steig als
Bodenlage Erde/Kies. Fenster 120 × 120 m, |Δ| ≤ 3 m.

**Assets.** Bestand: s. o. (alle in `netze.csv`, keine gesperrt). Wunsch: keiner zwingend. Lücke: **eine echte Felsnadel**
(Turm mit Kopf) gibt es nicht – Lösung ohne Paket: Granit-Schale hochkant + Kappe; sieht es im Editor zu flach aus, eine zweite
Schale (`vdssailfa_tier_2`) gespiegelt dahinter. Klang: Wind (Free City & Nature Sounds, A).

**Aufwand und Risiko.** Mittel (≈ 40 Akteure, ~4 000 Instanzen). Risiko: Rückseite der Schale (offen) – nur von N/O zeigen, oder
zweite Schale; Steig ist lang.

---

### 2 · Die Brandkiefer (`bergwald_02_die_brandkiefer`) – Leuchtfeuer

**Was man sieht.** Auf dem Kopf eines bewaldeten Sporns, hoch über der Talstraße, steht eine riesige tote Kiefer, schwarz
verkohlt bis in die Astquirle, vom Blitz längs gespalten; ein abgeworfener Kronenteil liegt hangab. Ringsum eine runde Lichtung
aus Asche, Erde und verkohlten Stümpfen, dahinter ein Ring aus jungem Kiefern- und Birkenaufwuchs, hüfthoch und leuchtend grün,
erst dann wieder dunkler Hochwald – die Geschichte eines Gewitters in drei Ringen, und von unten eine schwarze Gabel über den
Wipfeln.

**Vorbild.** Blitzbäume auf Kuppen (Schwarzwald, Tatra), Brandflächen mit Birkenvorwald; Spiel: die toten Einzelbäume von Velen
(Witcher 3) – hier ohne Menschenspur.

**Standort.** Feld B4, X −2990 / Y −920, Boden 164,3 m. Spornkopf über dem Tal: TPI25 +3,8 m, TPI50 +11,4 m, TPI100 +20,4 m,
Landform Kuppe/Gipfel, Hang 26° (max 58°), Exposition 62° (ONO, zur Straße). Boden Nadeln 88 % / Fels 9 %, dichter Wald ringsum
(374 Baumzellen im 35-m-Kreis, bis 31 m) – die Lichtung ist also die Folge des Brandes. 101 m vom Weg (−3016/−1018), 70 m vom Bach,
120 m vom nächsten Ort, 151 m vom Rand ROMAN_LOC_001 (knapp über der 150-m-Grenze), 342 m innerhalb des Bioms. Erste Wahl war
der Spornkopf I4 (3620/−590); er lag 203 m neben `elfenwald_02_nebelhain` und wurde deshalb hierher verlegt (Prüfer global
0 FEHLER). **Sicht:** 32 m Zielhöhe → 56 von 233 Wegpunkten im Ring 300–800 m sehen ≥ 30 % (mittlerer Anteil 0,13 – der Wald
schluckt den Stamm, die Krone ragt heraus), lesbar bis 800 m; bester Punkt (−2508/−404) in 706 m mit vollem Anteil. Der Fuß
(3 m) ist vom Weg nur an 1 von 117 Wegpunkten ≤ 400 m zu 28 % sichtbar.

**Komposition und Anmarsch.** Die schwarze Gabel gegen den Himmel über dem dunklen Wald, dahinter die Felsflanke des Kamms.
`_fern` von der Straße im NO (C4, 706 m, Anteil 1,0), `_anmarsch` 147 m vom Talweg im N (Anteil 0,66), `_held` 60 m von WSW
vom Hang oberhalb (Kamera 194 m) über Lichtung und Baum hinweg ins Tal, `_nah` 10 m (Rinde, Spaltriss, Asche). **Pfad nötig:**
286 m vom Weg (−2947/−1065), Luftlinie 151 m, max 29°, nur 7 m steiler als 25°, 14 m Querhang, 4 m Bach (Trittsteine) →
Steig mit zwei Kehren, Erde/Nadel-Band.

**Detail-Ebenen.** Held: `SM_Forest_pine_10_dead` ×1,3 (≈ 32 m), Materialwunsch verkohlt (s. u.). Begleiter (5): 2 verkohlte
Stümpfe (`SM_RottenTreeStump_01`, `SM_BrokenStump_01`), abgeworfener Kronenteil (`SM_BrokenTreeAssembly_01` ×1,5),
2 stehende tote Nachbarn (`qlEtl_tier_0`, `SM_DeadTree_02`). Schutt (40–80): verkohlte Äste/Rinde (`SM_Pine_broken_branch_01`,
`SM_mountain_branch_01_01`), `SM_Forest_pine_04_log`. Kleinzeug: Zapfen/Nadeln, Ascheflecken. Bewuchs nach Ursache: innen nichts
(Asche), Ring 16–30 m Jungwuchs `SM_Forest_pine_plant_01…03`, `Fir_01_Plant`, Birken `Big_Tree_Birch_01` 0,3–0,5× (Pionier),
Weidenröschen-Ersatz `SM_Crownbeard_03` (Blüteninseln), außen normaler Wald. Kontakt: Stamm 0,5 m eingegraben, Wurzelanläufe
`SM_Pine_roots_01`, Bodenlage Erde im Brandkreis, Moos fehlt bewusst.

**Wasser, Effekte, Licht.** Kein Wasser. Decals: `MI_ScatteredBark_01`, `MI_ScatteredSticksAndTwigs_01` (verkohlt getönt) im
Brandkreis; Ruß-Decal fehlt (Lücke). Optional Niagara (Niagara Examples Pack): sehr dünner Staub/Asche-Wirbel, `optional: true`.
Kein Licht.

**Geländeänderung.** Keine Form, nur Lagen: Erde 200 im Kreis 16 m (fleckig), Kraut/Gras im Ring. Fenster 80 × 80 m.

**Assets.** Bestand s. o. Wünsche: Niagara Examples Pack (A, Asche optional), Forest Cretaceous (B – nur falls dort ein toter
Riesenstamm dabei ist; Ersatz `SM_Forest_pine_10_dead` ×1,3). Materialwunsch `MI_EL_SW_Verkohlt` (Basis `M_EL_Fels_MS`,
`Toenung` [0,16, 0,14, 0,13, 1], `Helligkeit` 0,6) für Stümpfe/Äste; für die Kiefer selbst bitte prüfen, ob die
Material-Überschreibung (`M_EL_Pflanze`, `Farbe` [0,2, 0,18, 0,17, 1]) greift.

**Aufwand und Risiko.** Klein (≈ 15 Akteure, ~3 000 Instanzen; bestehende Bäume im 16-m-Kreis entfernen). Risiko: `SM_Forest_pine_10_dead` ist nicht Nanite (Billboard-LOD
aus der Ferne prüfen – die Silhouette ist der Ort).

---

### 3 · Säulenhain (`bergwald_03_saeulenhain`) – Leuchtfeuer

**Was man sieht.** Auf einer Bachterrasse zwischen zwei Gerinnen stehen zwölf Tannen in doppelter Größe – 45–55 m, Stämme wie
Säulen, astfrei bis 20 m. Darunter Halbdunkel, Nadelteppich, Sauerklee, Farnhorste und ein gestürzter Riese, auf dem eine Reihe
junger Tannen wächst (Ammenstamm). Von außen sieht man eine dunkle Kronenburg, die doppelt so hoch ist wie der Wald ringsum.

**Vorbild.** Cathedral Grove (Vancouver Island), Muir Woods; Spiel: der Wald von Brokilon/Crookback Bog-Altbäume (Witcher 3),
Hinterlands (Dragon Age: Inquisition).

**Standort.** Feld B5, X −2764 / Y 104, Boden 80,9 m. Talboden-Terrasse: Hang 15°, TPI100 +0,4 m, Exposition 50°; 26 m vom
Bach, Einzugsfläche 163 024 m² (feucht, tiefgründig), Boden Nadeln 85 % / Kies 10 %. Dichter Wald (498 Baumzellen im 45-m-Kreis,
max 32 m). 104 m vom Weg, 159 m vom nächsten Ort, 179 m vom Rand RES_CH27_LOC_003, 116 m innerhalb des Bioms. **Sicht:** Mit 50 m
Zielhöhe sehen 59 von 179 Wegpunkten (33 %) die oberen ≥ 15 m, lesbar bis 800 m; bester Punkt (−2166/−246) in 693 m (0,83).
Der Fuß (3 m) ist von **keinem** der 264 Wegpunkte bis 800 m sichtbar – man sieht nur die Kronen über dem Wald.

**Komposition und Anmarsch.** Außen: Kronenburg über dem Wald (`_fern` 693 m von SW-Straße in C4, Anteil 0,83; `_anmarsch`
114 m von der Serpentine im NW, 0,61). Innen: `_held` 45 m von N über den Bach in die Halle (Stämme als Säulenreihe, Lichtschacht
über dem Ammenstamm), `_nah` 10 m (Stammfuß mit Brettwurzeln, Moos). **Pfad nötig nur wegen 4 m Bach:** 156 m vom Weg
(−2643/31), max 24,5°, Trittsteine (`SM_SmallStonesPack_03`, `SM_flat_rock_02`) über den Bach.

**Detail-Ebenen.** Held (12): `Fir_07_Forest`/`Fir_04_Standalone` ×2,2–2,5 (≈ 48–55 m), Wunsch Forest Cretaceous. Begleiter:
gestürzter Riese `SM_MossyTree_01` ×3 + `SM_LargeFallenTree_02` ×2 mit Wurzelteller `SM_Pine_roots_01` ×2; 6–8 normale Tannen
(`Fir_06_Forest`) als Maßstab am Rand. Schutt (60–120): Äste, Rindenstücke, Moderholz (`SM_OldFallenTree_02`, `SM_Forest_pine_08_log`,
`SM_detail_branches_03`). Kleinzeug: Zapfen, Nadeln, Pilze (Wunsch Forest Fungi). Bewuchs nach Ursache: lichtarm → kein Gras,
Farn in Inseln (`SM_EagleFern_M_01`, `SM_SilverLadyFern_04`), Moos am Stammfuß/Nordseite (`SM_MossClump_02`), Heidelbeere
(`SM_billberry_01`) nur in Lichtflecken, Jungtannen-Reihe auf dem Ammenstamm (`Fir_01_Plant` 0,3×). Kontakt: Stammfüße
40 % eingegraben, Wurzelanläufe `SM_MossyForestRoots_03`, Nadelstreu-Lage.

**Wasser, Effekte, Licht.** Bach bleibt; Ufer mit Kies und Moos. Lokaler Nebel in der Halle (Dichte 0,03, warm-grau) für
sichtbare Lichtschächte; 1 Spotlicht (schwach, kein Schatten) als Lichtfleck auf dem Ammenstamm. Klang: Waldhalle (Free City &
Nature Sounds, A).

**Geländeänderung.** Keine Form; Lagen Nadeln 220, Moos 150 fleckig um Stammfüße. Fenster 110 × 110 m.

**Assets.** Bestand s. o. Wünsche: **Forest Cretaceous** (B, echte Mammut-/Riesenstämme – sonst gestreckte Tannen mit
verzerrter Rinde), **Forest Fungi – Mushroom Pack** (B), Free City & Nature Sounds (A).

**Aufwand und Risiko.** Mittel (≈ 30 Akteure, ~6 000 Instanzen). Risiko: skalierte Nicht-Nanite-Tannen (Rindenkachel, LOD/Billboard
der Kronen auf 700 m) – im Editor zuerst `_fern` prüfen.

---

### 4 · Felsenmeer (`bergwald_04_felsenmeer`) – Fundstück

**Was man sieht.** Hinter einer Waldrippe öffnet sich ein Talschluss: oben eine graue Abbruchkante, darunter ein Meer aus
hausgroßen bis kopfgroßen Blöcken, kreuz und quer, dick bemoost, mit Fichten, die zwischen den Blöcken wurzeln. Ein Kippblock
liegt schräg auf zwei anderen; darunter eine kühle, dunkle Spalte, aus der man den Bach rauschen hört.

**Vorbild.** Felsenmeer im Lautertal (Odenwald), Blockhalden im Harz; Spiel: Blockhalden unter Kaer Morhen, die bemoosten Hänge
der Emerald Graves (DA:I).

**Standort.** Feld B4, X −2938 / Y −510, Boden 130 m. Talschluss/Kessel: TPI25 −11,6 m, TPI100 −41,2 m, Wände nach W/N/S
+46…+52 m auf 40 m (max Hang 69° = Abbruchkante als Ursache), Halde 27° nach O (Exposition 84°). Boden Geröll/Fels 72 %,
Moos 8 %. Einzugsfläche 12 004 m². 84 m vom Weg – aber jenseits des großen Flusses, 188 m vom Rand ROMAN_LOC_001, 290 m innen.
**Verdeckung:** 4 m Zielhöhe von 0 der 94 Wegpunkte bis 400 m und 0 von 342 bis 800 m sichtbar.

**Komposition und Anmarsch.** Man kommt von unten (O) aus dem Wald: `_anmarsch` 62 m, der Blick geht die Halde hinauf zur
Kante. `_held` 27 m: Kippblock im Vordergrund, Blockfeld steigt zur hellen Kante, Fichten als Säulen dazwischen. `_nah` 10 m:
Spalte unter dem Kippblock, Moospolster. **Pfad nötig:** 644 m vom Weg (−2961/−253) – die direkte Linie (84 m) quert den Fluss;
max 24,7°, 0 m steil, 36 m Querhang, 16 m Wasser → Trittsteine an einem Seitenbach. Pfad als Erde/Nadel-Band, am Ende über
Blöcke (Trittsteine aus `SM_flat_rock_04`).

**Detail-Ebenen.** Held: Kippblock `SM_NordicBoulder_01` ×1,5 auf `SM_MossyForestBoulder_04` ×2. Begleiter (6–8): `SM_Big_Rock_01/02`
×1,5, `SM_mountain_rock_big_02_1/_3`. Schutt (150–200): Blockfeld `SM_MossyForestBoulder_01/03`, `SM_MossyRocks_02`,
`SM_ForestRockFormation_05`, oben grob/kantig (frisch, `M_EL_Fels_MS`), unten rund/bemoost (alt) – Alter erzählt die Halde.
Kleinzeug: `SM_SmallStonesPack_*`, Laub/Nadeln in den Fugen. Bewuchs nach Ursache: Fichten (`Fir_06_Forest`, `SM_Forest_pine_09`)
mit Wurzeln über Blöcke (`SM_MossyForestRoots_03`), Farn in feuchten Fugen (`SM_Fern_02`), Moosdecken (`M_EL_Fels_Auflage`
Moos oben/Nord), am Fuß der Wand Tropfnässe. Kontakt: Blöcke 25–45 % eingegraben, untereinander verkeilt, Kiessaum.

**Wasser, Effekte, Licht.** Unter dem Blockfeld rauscht ein unsichtbarer Bach (nur Klang + 2 Nassflecken-Decals
`MI_Leakage_04`). Lokaler Nebel am Wandfuß (0,04). Kein Licht.

**Geländeänderung.** Halde leicht buckelig (−1…+2 m), Lagen Geroell 200, Moos 160 fleckig. Fenster 160 × 160 m.

**Assets.** Bestand s. o. Wunsch: Free City & Nature Sounds (A, verborgener Bach). Ersatzfrei machbar.

**Aufwand und Risiko.** Mittel-hoch wegen Blockzahl (≈ 60 Akteure, ~5 000 Instanzen, ~1 200 mit Kollision – im Budget). Risiko:
Bachquerung des Pfades; Spieler im Blockfeld → Kollision nur für große Blöcke.

---

### 5 · Klemmblock-Klamm (`bergwald_05_klemmblock_klamm`) – Fundstück

**Was man sieht.** Ein Bach beginnt am Fuß einer Felsstufe. Folgt man ihm 30 m hinein, stehen die Wände links und rechts
nur noch 6–10 m auseinander, triefend und moosgrün; über dem Spalt hängt ein eingeklemmter Block wie ein Riegel. Dahinter fällt
ein Schleierfall 30 m die Stufe hinab in eine smaragdgrüne Gumpe mit sichtbarem Kiesgrund.

**Vorbild.** Kjeragbolten (Klemmblock), Partnachklamm / Liechtensteinklamm, Schleierfälle der Ammergauer Alpen; Spiel: die
Schluchten unter Kaer Morhen, Klamm-Wasserfälle in Skellige.

**Standort.** Feld I4, X 3730 / Y −966, Boden 98,9 m. Kerbtal: TPI25 −17,7 m, TPI100 −22,7 m, Hang 62° (max 74,5°); Wände nach N
+15 m und S +16 m auf 10 m (Klammbreite ~20 m), nach W steigt die Stufe +22 m auf 10 m. `gel.stufen` findet bei (3716/−966) einen
Gefällsprung von **31,2 m auf 16 m** (Gefälle 1,95 gegen 1,17 oberhalb, Einzugsfläche 2 876 m²) – der Fall; der Bach im
Wasserraster beginnt bei ~3745/−958 (Gumpenablauf). Boden Fels 60 % / Laub 33 %. 203 m vom Weg, 191 m vom Meer, 140 m innen.
**Verdeckung:** 6 m Zielhöhe von 0 / 26 Wegpunkten ≤ 400 m und 0 / 62 ≤ 800 m sichtbar.

**Komposition und Anmarsch.** Kurze Inszenierung in drei Schritten: Bach im Wald (`_anmarsch` 30 m, Klammeingang), Klemmblock
als Rahmen, durch den man den Fall sieht (`_held` 23 m bachab, Blick W: Block oben im Bild, Fall in der Mitte, Gumpe unten),
`_nah` 10 m an der Gumpe. **Pfad nötig:** 419 m vom Weg (3787/−769), max 39°, 19 m steil, 61 m Querhang, 8 m Wasser → Steig
bis zum Klammeingang, in der Klamm Trittsteine im Bach (`SM_flat_rock_02/_04`), kein Steg (keine Bauten).

**Detail-Ebenen.** Held: Klemmblock `SM_NordicBoulder_01` ×1,2 zwischen den Wänden, 6 m über dem Bach. Begleiter: Klammwände aus
`SM_big_rock_wall_01…03` ×3–4 und `rcygn_tier_0`/`vfmjadufa_tier_2` als Wandschalen (Fuß im Boden), Fallkante `ukjhcamga_tier_0`.
Schutt (60–100): Bachblöcke `SM_mountain_rock_big_02_*`, Gerölle in der Gumpe `SM_DryRiverBed_01`. Kleinzeug: Kies, Treibholz
(`SM_OldTreeBranch_06`, `SM_Forest_pine_04_log` verkeilt = Hochwasser erzählt). Bewuchs nach Ursache: Spritzzone Moos und Farn
(`SM_SilverLadyFern_04`, `SM_BeechFern_04`), Efeu-Ersatz `SM_Ivy_11` an der Nordwand, oben an der Kante Kiefern mit freigespülten
Wurzeln (`SM_Pine_roots_03`). Kontakt: Nassband 1 m über Wasser (`M_EL_Klippe_RVT` Moos, `M_EL_Fels_MS` `Nass_Dunkel`).

**Wasser, Effekte, Licht.** `wasserfall` Kante (3716/−962 … 3716/−972, z ≈ 127 m) → Fuß ≈ 96 m, Breite 3–4 m, `becken` = Gumpe;
`see` Gumpe r ≈ 6 m, `smaragd`, Tiefe 2,5 m; `bach` Gumpe → bestehendes Gerinne (fallend, ~2 m breit, `klar`). Gischt-Nebel
(lokaler Nebel 0,08) am Fallfuß, Niagara-Gischt optional. 1 Punktlicht kühl am Gumpenrand (schwach) gegen die Schwärze der Klamm.

**Geländeänderung.** Gumpe −2,5 m, Klammboden glätten (−1…+1 m), Fallkante als Netz. Fenster 90 × 90 m; keine Änderung am
Bestandswasser außer der Ort selbst.

**Assets.** Bestand s. o., Wasserfall-Material `MI_EL_Wasserfall`/`MI_EL_Wasserfall_Aufprall`. Wünsche: **Mountain – Environment Set
(Fluss-/Wasserfall-Material)** (A), Niagara Examples Pack (A, Gischt optional), Nature Water FX (B), Realistic Waterfall and Water
VFX / Waterfall Pro (C, nur falls der eigene Vorhang zu glatt wirkt), Free City & Nature Sounds (A, Fallrauschen).

**Aufwand und Risiko.** Hoch (Wasser + Wände; ≈ 45 Akteure, ~4 000 Instanzen). Risiko: Klammbreite aus 2-m-Daten (~20 m) –
im 1-m-Test enger stellen; Fallhöhe hängt an der Stufe, Planer muss Kante/Fuß aus 1 m nehmen.

---

### 6 · Karsee (`bergwald_06_karsee`) – Fundstück

**Was man sieht.** Hinter einer Felsschwelle liegt ein kleiner, tintendunkler See in einem Kessel, dessen Wände 30–50 m
aufragen. Drei Bäche fallen aus den Rinnen der Karwand hinein, auf der Westseite ein grauer Schuttkegel bis ins Wasser, mitten im
See eine Felsinsel mit einer einzelnen verkrüppelten Kiefer. Der Abfluss stürzt über die Schwelle als Kaskade ins Tal.

**Vorbild.** Karseen der Tatra und der Alpen (Seebensee, Gaisalpsee); Spiel: die Bergseen in Skellige/Kaer Morhen, Frostback-Seen
(DA:I).

**Standort.** Feld B5, X −3210 / Y 72, Boden 258,7 m. Kessel im Talschluss: TPI25 −10,0 m, TPI100 −39,3 m, Boden 18° (flacher
Karboden), Wände S/SW/W +25…+50 m auf 20–40 m (max 73°), offen nach NO/O (−2,5 m auf 10 m, −11…−16 m auf 40 m = natürliche
Schwelle). Einzugsfläche 64 124 m² – mehrere Rinnen laufen hier zusammen (Wasser 8 m). Boden Fels 70 % / Geröll 22 %. 285 m vom
Weg, 305 m vom Rand ROMAN_LOC_017, 290 m innen. **Verdeckung:** 4 m Zielhöhe von 0 / 33 ≤ 400 m und 0 / 177 ≤ 800 m sichtbar.

**Komposition und Anmarsch.** Man steigt am Abfluss hinauf (`_anmarsch` 26 m, Anteil 0,93: über die Schwelle hinweg öffnet sich
der See), `_held` 35 m auf der Karschwelle mit Blick SW: dunkler Spiegel, Insel, Schuttkegel, Karwand mit Fallstreifen; `_nah`
12 m am SO-Ufer (Zulauf, Kiesbank). **Pfad nötig:** 470 m vom Weg (−2937/−7), entlang des Abflusses, max 41,5° (Schwelle),
38 m steil, 104 m Querhang, 119 m im Bachbett (Furt/Trittsteine) → Steig neben dem Bach, an der Schwelle Felsstufen.

**Detail-Ebenen.** Held: der See + Insel (`SM_NordicBoulder_01` + `SM_MossyForestBoulder_04`, Kiefer `SM_dwarf_pine_big_01`).
Begleiter: Karschwelle aus `SM_MassiveTundraRockFormation_02` (Rundbuckel, glazial geschliffen) + `ukjhcamga_tier_0`; 2–3 große
Uferblöcke. Schutt (100–200): Schuttkegel `SM_mountain_rock_big_01_*`, `SM_ground_rock_01`, unter Wasser weiterlaufend. Kleinzeug:
Kies am Ufer, Treibholz an der Schwelle. Bewuchs nach Ursache: Ufer Binsen (`SM_ToadRush_010`), Moos- und Seggensaum an den Zuläufen,
Latschen/Zwergkiefern auf den Rundbuckeln (`SM_dwarf_pine_medium_02`), Heidelbeere/Preiselbeere zwischen Blöcken, kaum Bäume
(Kaltluftsee). Kontakt: Nassband am Ufer, Felsen 35 % eingegraben, Moos auf Nordseiten.

**Wasser, Effekte, Licht.** `see` ~56 × 34 m (`schwarz_spiegel`, Tiefe 4 m, Umriss gegen Uhrzeigersinn um −3214/64),
3 Zuläufe als `bach` (Quelle in den Rinnen → See), Abfluss `bach` über die Schwelle → bestehender Bach (Stufen > 0,8 m werden
kleine Fälle). Lokaler Nebel über dem See (0,06, kühl). Kein Licht.

**Geländeänderung.** Becken −2…−4 m, Karschwelle +3…+5 m am NO-Rand (Ufer muss rundum über dem Spiegel liegen); |Δ| ≤ 6 m,
Fenster 140 × 140 m. Bestandswasser wird Teil des Ortes (der Ort IST dieses Gewässer).

**Assets.** Bestand s. o., Wasser-Material `MI_Eldarien_Wasser_See`. Wünsche: Mountain – Environment Set (A, Kaskade über die
Schwelle), Free City & Nature Sounds (A). Optional Seerosen **nicht** (zu hoch/kalt).

**Aufwand und Risiko.** Mittel-hoch (Seenbau + Stempel; ≈ 25 Akteure, ~4 000 Instanzen). Risiko: Seespiegel gegen 1-m-Gelände
abstimmen; kein geschlossener Kessel ohne Abfluss – Abfluss über die Schwelle ist Pflicht.

---

### 7 · Windwurf (`bergwald_07_windwurf`) – Fundstück

**Was man sieht.** Mitten im dichten Küstenwald plötzlich Licht: eine 115 m lange Gasse, in der alle Fichten in dieselbe Richtung
liegen – Kronen landeinwärts nach Westen, die Wurzelteller zum Meer hin hochgestellt wie Wände, mit Erde und Steinen darin. In
den Wurzellöchern stehen Pfützen, zwischen den Stämmen schießen Himbeeren, Weidenröschen und junge Fichten auf.

**Vorbild.** Sturmflächen nach Kyrill/Lothar (Schwarzwald, Harz), Windwurf-Gassen an der norwegischen Küste; Spiel:
Sturmschneisen in Velen (Witcher 3), die umgestürzten Wälder der Emerald Graves.

**Standort.** Feld I4, X 3985 / Y −650, Boden 21 m. Offener Waldhang 16° (max 31°), Exposition 81° (O) **direkt zum Meer (66 m)**:
der Sturm kommt von See, der Hang ist die erste Waldkante. Boden Nadeln 89 %, dichter Wald (725 Baumzellen im 55-m-Kreis, bis 30 m).
132 m vom Weg, 67 m innen. **Verdeckung:** 4 m Zielhöhe von 0 / 53 ≤ 400 m und 0 / 81 ≤ 800 m sichtbar – vom Küstenweg sieht man
nur Wald.

**Komposition und Anmarsch.** Fußweg ohne Pfad (streng erreichbar: 149 m, max 21°). `_anmarsch` 38 m am Waldrand der Gasse
(Blick nach O über die liegenden Stämme aufs Meer), `_held` 20 m von SSW quer zur Gasse (Wurzelteller als Wand im Vordergrund,
Stämme führen den Blick bergauf), `_nah` 10 m (Wurzelteller mit Steinen, Pfütze).

**Detail-Ebenen.** Held: 9–14 liegende Fichten (`SM_Forest_pine_08/_09` liegend, Wind aus; Ersatz `SM_FallenSpruceTree_01` ×2,5,
`SM_LargeFallenTree_02` ×2) mit Wurzeltellern `SM_Pine_roots_01` ×2 + `SM_stones_roots_01/02` (Steine im Wurzelballen). Begleiter:
3 gebrochene Stümpfe (`SM_BrokenStump_01`), 2 schräg hängende Bäume, die im Nachbarbaum hängen geblieben sind. Schutt (100–200):
Äste, Kronenteile, Rinde (`SM_Pine_broken_branch_01/02`, `SM_detail_branches_03`). Kleinzeug: Nadeln, Zapfen, Erde. Bewuchs nach
Ursache: Licht → Jungfichten `Fir_01_Plant`/`SM_Forest_pine_plant_*`, Holunder `SM_Elderberry_08`, Hasel `SM_hazel_02`, Kraut/Gras
in der Gasse; Waldrand mit Saum. Kontakt: Wurzellöcher als Mulden mit Pfützen, Erde-Lage um die Teller.

**Wasser, Effekte, Licht.** 3–4 kleine Pfützen in Wurzellöchern (`see` r 1–2 m, `moorbraun`, Tiefe 0,3 m). Optional Niagara
fliegende Nadeln/Blätter (Niagara VFX Pack …Autumn Leaves, B / Ultimate Niagara Environmental VFX, B). Kein Licht – die
Sonne fällt durch die Gasse (Kontrast zum dunklen Wald).

**Geländeänderung.** Wurzellöcher −0,5…−1 m (6–9 Stück), Fenster 140 × 60 m (gedreht). Bestehende Bäume in der Gasse entfernen
(Planer-Liste für den Setzer).

**Assets.** Bestand s. o. Wünsche: Forest Fungi (B, Pilze auf Totholz), Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves &
Steam (B), Ultimate Niagara Environmental VFX (B), Free City & Nature Sounds (A, Brandung + Wind). Lücke: **großer Wurzelteller**
(3–5 m, senkrecht) – Lösung ohne Paket: `SM_Pine_roots_01` ×2 + `SM_stones_roots_02` gekippt + Erde-Decal.

**Aufwand und Risiko.** Mittel (≈ 40 Akteure, ~5 000 Instanzen). Risiko: liegende Foliage-Bäume mit Wind-Animation (Wind 0 nötig,
sonst wackeln Stämme) und Billboards im Liegen – Ersatz sind die Megascans-Stämme.

---

### 8 · Der Wurzelstein (`bergwald_08_der_wurzelstein`) – Fundstück

**Was man sieht.** Auf einer Waldrippe liegt ein Findling so groß wie ein Haus. Auf seinem Scheitel wächst eine alte Fichte;
ihre Wurzeln haben den Block umklammert und greifen in dicken, bemoosten Strängen 6 m tiefer in den Boden. Neben dem Block liegen
kleinere Brocken desselben Felssturzes, dazwischen Heidelbeere und Farn.

**Vorbild.** „Baum auf dem Stein“ (Sächsische Schweiz, Bastei; Ta Prohm ohne Ruine), Wurzelfelsen im Bayerischen Wald; Spiel:
Felsen mit Wurzelkronen in Kaer Morhen, Emerald Graves.

**Standort.** Feld B4, X −3262 / Y −296, Boden 357 m. Rippenrücken (TPI100 +13,6 m) mit 33°-Flanke nach O (Exposition 95°), Fels
39 % / Nadeln 38 % / Gras 20 % – Block-und-Wald-Mischung, die einen Findling erklärt (Felssturz von der Wand oberhalb, W +36 m auf
40 m). 275 m vom Weg, 62 m vom Bach, 269 m vom Rand ROMAN_LOC_017, 381 m innen. **Verdeckung:** 6 m Zielhöhe von 0 / 47 Wegpunkten
≤ 400 m sichtbar; bis 800 m sehen 3 von 207 Wegpunkten (749–761 m entfernt) bis zu 72 % – ein 6-m-Block in 750 m Wald ist nicht
als Ort lesbar (Fundstück bleibt verdeckt).

**Komposition und Anmarsch.** `_anmarsch` 111 m vom Steig (Block erscheint zwischen Stämmen), `_held` 83 m von NNO talseitig
(Block mit Baumkrone, dahinter der Hang), `_nah` 10 m (Wurzelstränge über Moos). **Pfad nötig:** 641 m vom Weg (−2937/−195),
max 36°, 33 m steil, 199 m Querhang → Steig mit Kehren, im oberen Teil über Felsstufen.

**Detail-Ebenen.** Held: Findling `SM_NordicBoulder_01` ×1,4 (≈ 9 × 12 × 6 m) + Fichte `SM_Forest_pine_08` 0,8× auf dem Scheitel.
Begleiter (4–6): `SM_Big_Rock_01/02`, `SM_MossyForestBoulder_04`. Wurzeln: `SM_Pine_roots_01/03` + `SM_stones_roots_03` über die
Blockflanken bis in den Boden (Ursache sichtbar). Schutt (30–60): Blöcke `SM_MossyForestBoulder_01/03`, `SM_ground_rock_01`.
Kleinzeug: Nadeln, Zapfen, Rindenstücke. Bewuchs nach Ursache: Moos auf der Blocknordseite und auf den Wurzeln
(`M_EL_Fels_Auflage`), Heidelbeere/Preiselbeere am Fuß (`SM_billberry_01`, `SM_lingonberry_01`), Farn im Wurzelschatten
(`SM_BeechFern_04`). Kontakt: Block 30 % eingegraben, Wurzeln ins Gelände gesenkt, Nadelstreu.

**Wasser, Effekte, Licht.** Kein Wasser. Lichtschacht durch eine Kronenlücke (1 Spotlicht schwach, kein Schatten) auf den Block.

**Geländeänderung.** Kleine Terrasse 10 × 8 m (−1…+1 m) für den Blockfuß. Fenster 60 × 60 m.

**Assets.** Bestand s. o. Wünsche: keine zwingend. Klang: Wald (Free City & Nature Sounds, A).

**Aufwand und Risiko.** Klein-mittel (≈ 20 Akteure, ~2 000 Instanzen). Risiko: Wurzelnetze an den Block anpassen (Handarbeit im
Editor, 1-m-Test).

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/elfenwald/katalog.md](sehens/elfenwald/katalog.md)

### 1 · Mutterbaum (`elfenwald_01_mutterbaum`) – Leuchtfeuer

**Was man sieht.** Auf einer runden Waldkuppe über der Küste steht ein Baum, der nicht in diese Welt passt: 55 m hoch, der
Stamm 6 m dick, silbergraue glatte Rinde, die Krone 60 m breit und 30 m über allen anderen Wipfeln. Von der Küstenstraße sieht
man einen dunklen Kronenberg über dem Wald. Steht man darunter, öffnet sich eine Lichtung, die der Riese selbst geschaffen hat
(sein Schatten lässt nichts aufkommen): ein Ring aus Brettwurzeln, mannshoch, zwischen ihnen Nischen, in denen bleiche Pilze
im Halbdunkel schwach leuchten. Am Lichtungsrand stürmt Jungwuchs ins Licht; auf der Lee-Seite liegt der umgestürzte Rivale.

**Vorbild.** Real: Riesenbuchen im Urwald Uholka-Schyrokyj Luh (Karpaten), Tāne Mahuta (Kauri, Neuseeland) für den Maßstab;
Spiel: Brokilon und der „Heilige Hain" (Witcher 3), Baumriesen der Emerald Graves (Dragon Age: Inquisition).

**Standort.** Feld G3, X 1736 / Y −1302, Boden 40,6 m. Oberhang/Plateaukante einer Waldkuppe: Hang 6° (max 41° an der
Flanke), TPI100 +13,6 m, Exposition 238° (SW zur Küste), Boden Laub 97 %. Dichter Wald (421 Baumzellen im 45-m-Kreis,
max 23 m) – der Riese überragt ihn um 32 m. Bach 53 m östlich (Wasserversorgung = Ursache für die Größe). 94 m vom
Küstenweg, 863 m vom Rand der Elfenstadt, 107 m innen. **Sicht:** 55 m Zielhöhe → 82 von 339 Wegpunkten im Ring 300–800 m
sehen ≥ 30 % (Mittel 0,15), lesbar bis 758 m; bester Punkt (1680/−1612) auf der Südstraße in 315 m, Anteil 0,90.

**Komposition und Anmarsch.** `_fern` 315 m von Süden (Straße am Bach, Anteil 0,92): Kronenberg über dem Wald, davor die
Bucht. `_anmarsch` 89 m vom Küstenweg im Westen (Augenhöhe, Anteil 0,76): durch Stämme sieht man zuerst den Stammfuß,
erst beim Hochschauen die Krone. `_held` 286 m aus SW von der Küste (Blick 60°): Meer und Kies im Vordergrund, Waldsaum,
darüber der Riese – klassisches Witcher-Bild mit Luftperspektive. `_nah` 10 m: Brettwurzel-Nische mit Leuchtpilzen. Zugang
ohne Pfad: 98 m, max 24,4° vom Weg (1645/−1319); nur ein Trampelpfad (Erde/Laub-Band 1,5 m) mit Wurzelstufen.

**Detail-Ebenen.** Held (1): Riese, Akteur `SM_beech_tree_05` ×2,5 (≈ 55 m) bis das Wunschpaket da ist; Stammfuß verstärkt
durch 6 radiale Brettwurzeln `SM_beech_old_roots_01` ×5–6 und `SM_MossyForestRoots_03` ×3 (bilden die Nischen). Begleiter (6):
2 normale Altbuchen `SM_beech_tree_09` als Maßstab am Lichtungsrand, der tote Rivale `SM_EuropeanBeech_Dead_XL_01` (stehend,
blitzgespalten) und sein liegender Partner `SM_LargeFallenTree_02` mit Wurzelteller in einer Senke, 2 Wurzelstöcke
`SM_RottenTreeStump_01`. Schutt (80–150): herabgefallene Äste `SM_OldTreeBranch_05`, `SM_BrokenTreeBranch_01`,
`SM_detail_branches_03`, Rindenstücke (Decal `MI_ScatteredBark_01`). Kleinzeug: Bucheckern/Laub `SM_detail_leaves_01`,
`SM_DeadLeaves_01`, Pilzgruppen `SM_mushroom_01/02` (Wunsch Forest Fungi). Bewuchs nach Ursache: im Kronenschatten nur
Moos (`SM_MossClump_01`, `SM_CustomMoss_01`) und Laub; Jungwuchs-Ring im Licht am Lichtungsrand (`SM_beech_tree_00_C`,
`SM_beech_plant_02`), Farn im feuchten Osten zum Bach (`SM_SilverLadyFern_01`), Efeu am Stamm (`SM_Ivy_17`, `SM_Ivy_25` bis 5 m).
Kontakt: Wurzeln 35–45 % eingegraben, Moosband am Stammfuß (Lage Moos), Laub sammelt sich in den Nischen.

**Wasser, Effekte, Licht.** Kein Wasser. 2 Punktlichter (kalt-grün 0,55/0,9/0,6, 300 cd, Radius 6 m, ohne Schatten) in zwei
Wurzelnischen = Leuchtpilze; Niagara „Leuchtsporen" (optional, Free Niagara Particles) im Kronenschatten. Lichtschacht durch die
Lücke des toten Rivalen (lokaler Nebel 0,03, damit der Strahl sichtbar wird).

**Geländeänderung.** Kuppe bleibt; Lichtung leicht gewölbt +0,5 m um den Stamm (Wurzelanlauf), Wurzelteller-Senke −1,2 m
(6 × 14 m) neben dem liegenden Rivalen. Lagen: Laub 230, Moos 160 fleckig im Kronenkreis, Erde 120 am Trampelpfad. Fenster
140 × 140 m.

**Assets.** Bestand s. o. (exakte Netznamen). Wunsch: **Forest Cretaceous** (B, Riesenstamm mit echter Rinde – Ersatz:
gestreckte `SM_beech_tree_05`, Risiko verzerrte Rinde), **Forest Fungi – Mushroom Pack** (B, Pilze in den Nischen – Ersatz
`SM_mushroom_01/02`), **Free Niagara Particles** (B, Leuchtsporen – Ersatz nur Punktlicht), **Free City & Nature Sounds** (C,
Wind in der Krone).

**Aufwand und Risiko.** Mittel (≈ 25 Akteure, ~5 000 Instanzen). Risiko: skalierter Nicht-Nanite-Baum (Blattgröße ×2,5,
Billboard auf 300 m) – `_fern` zuerst prüfen; Notlösung Krone aus 3 überlagerten `SM_beech_tree_05` (×1,8) um einen ×2,5-Stamm.

---

### 2 · Nebelhain (`elfenwald_02_nebelhain`) – Leuchtfeuer

**Was man sieht.** Auf dem Ostgrat, 393 m hoch, sitzt eine Wolke fest. Von der Küstenstraße unten sieht man eine dunkle,
zerzauste Kronengruppe, um die ein weißer Schleier hängt – der einzige Nebel am klaren Tag. Oben stehen neun uralte, krumme
Bäume, die Äste waagrecht und dick wie Stämme, alles in grünen Moospolstern und hängenden Bartflechten; der Boden ist ein
federndes Moosbett zwischen Felsrippen. Man hört Tropfen fallen, obwohl es nicht regnet: der Wald kämmt das Wasser aus der Wolke.

**Vorbild.** Real: Fanal-Lorbeerwald (Madeira), Wistman's Wood (Dartmoor); Spiel: Crookback Bog und Ard Skellig-Hochwald
(Witcher 3), Nebelwälder der Hinterlands (DA:I).

**Standort.** Feld I4, X 3460 / Y −708, Boden 392,7 m. Oberhang am Grat: Hang 44° (Felsrippen bis 63°), TPI100 +34,5 m, 82 m
Relief im 45-m-Kreis, Exposition 111° (O, zur Straße), Boden Laub 55 % / Fels 25 % / Erde 19 %. 368 Baumzellen (max 23 m).
295 m vom Weg (Straße in I4 östlich, 3829/−639), 132 m innen, 373 m von `bergwald_05_klemmblock_klamm`. **Sicht:** 28 m
Zielhöhe → 47 von 80 Wegpunkten (300–800 m) sehen ≥ 30 % (Mittel 0,43), lesbar bis 710 m; bester (3830/−732) in 371 m, 1,00.

**Komposition und Anmarsch.** `_fern` 371 m von der Straße im Osten (Augenhöhe, Blick 266°): Grat mit Nebelkrone über dem
Wald. `_anmarsch` 376 m (gleiche Straße, Anteil 0,75). `_held` 56 m von Süden auf dem Grat (Blick 350°): Moosboden im
Vordergrund, die knorrigen Stämme als Gitter, Nebel dahinter mit Gegenlicht. `_nah` 10 m: Ast mit Moos und Flechten.
**Pfad nötig:** 921 m Fußweg (Luftlinie 375 m) mit max 44°, 134 m steiler als 25°, 325 m Querhang → Serpentinenpfad
(Erde/Kies-Band 1,2 m, 6–8 Kehren am Osthang, natürliche Felsstufen `SM_flat_rock_02` als Tritte). Das ist der teuerste
Zugang im Biom, aber der Grat ist die einzige Stelle im Osten mit Sicht.

**Detail-Ebenen.** Held (9): knorrige Altbäume = `Big_Tree_Willow_02` ×0,8 und `SM_beech_tree_09` ×1,1 schräg (bis 12°
geneigt, windgebeugt nach W), Stämme mit `M_EL_Fels_Auflage`-Moos (Materialwunsch unten). Begleiter (5): Felsrippen
`SM_MossyRockFace_02`, `SM_HugeMossyForestCliff_01` ×1,5, Block `SM_MossyForestBoulder_04`. Schutt (40–80): bemooste Äste
`SM_OldTreeBranch_05`, `SM_MossyTree_01` (liegender Ast), Steine `SM_MossyRocks_02`. Kleinzeug: `SM_MossClump_01–05`,
`SM_CustomMoss_01–05` dicht, Flechten-Decals (`MI_TileableMossPatches_02`). Bewuchs nach Ursache: Nebelfeuchte → Moos überall,
Hängeflechten = `SM_Ivy_11`/`SM_Ivy_21` (hängend, grau-grün getönt) an den Ästen, Farn nur in Felsspalten (`SM_SilverLadyFern_02`),
kein Gras (zu dunkel, zu sauer). Windflüchter am Grat nach W. Kontakt: Wurzeln über Fels (`SM_Pine_roots_01`), Moos kriecht
40 cm am Fels hoch (`M_EL_Klippe_RVT` Moos_Band).

**Wasser, Effekte, Licht.** 2 lokale Nebel (Radius 40 m, Dichte 0,12, kühlweiß, Höhenabfall gering) – liegen *in* den Kronen,
nicht am Boden; optional Niagara-Nebelfetzen (Niagara Examples Pack) für Bewegung. 6 Decals `MI_Leakage_02` als Tropfnässe
unter Ästen. Kein Licht (Sonne gegen Nebel reicht).

**Geländeänderung.** Keine Form. Lagen Moos 230, Fels 140 (Rippen), Erde 120 am Pfad. Fenster 120 × 120 m (+ Pfadband).

**Assets.** Bestand s. o. Wunsch: **Niagara Examples Pack** (B für diesen Ort, Nebelbewegung – Ersatz: zwei statische lokale
Nebel), **Free City & Nature Sounds** (C, Tropfen/Wind). Materialwunsch `MI_EL_SW_Bartflechte` (M_EL_Pflanze, `Farbe`
[0,72, 0,78, 0,62, 1], `Wind_Staerke` 0,5) für `SM_Ivy_11`, `SM_Ivy_21`.

**Aufwand und Risiko.** Mittel (≈ 30 Akteure, ~6 000 Instanzen, langer Pfad). Risiko: Nebel bei fester Sonne aus 370 m nur
schwach lesbar → Dichte im Editor auf `_fern` einstellen; Pfad 921 m kostet Lagen-Arbeit am Steilhang.

---

### 3 · Rotlaubhain (`elfenwald_03_rotlaubhain`) – Leuchtfeuer

**Was man sieht.** Am Hang über der Elfenstadt brennt mitten im grünen Wald ein Fleck Rot: vierzehn Buchen mit blutrotem Laub,
in der Mitte ein alter Baum, um den sich die jüngeren drängen. Darunter liegt das gefallene Laub als rot-kupferner Teppich, der
hangab wie ein Fluss zwischen den grünen Stämmen ausläuft. Bei Wind wirbeln einzelne rote Blätter ins Grün.

**Vorbild.** Real: Blutbuchen-Haine (Fagus sylvatica f. purpurea), Herbstwälder Hokkaidōs; Spiel: die rostroten Lärchen aus
`witcher_07`, Herbstfarben im Toussaint-Wald (Blood and Wine).

**Standort.** Feld H4 (Ränder H3), X 2744 / Y −1030, Boden 103,1 m. Offener Hang 18,7° (max 42°), Exposition 243° (SW – zur Stadt
und zum Tal hin, also *dem Betrachter zugewandt*), TPI100 +6,8 m, Boden Laub 96 %, 636 Baumzellen (max 26 m). Bach 52 m.
173 m vom Weg, 170 m vom Rand der Elfenstadt (≥ 150), 631 m innen. **Sicht:** 24 m Zielhöhe → 62 von 254 Wegpunkten sehen ≥ 30 %,
lesbar bis 799 m; bester (2442/−688) an der Stadtstraße in 456 m, Anteil 0,90.

**Komposition und Anmarsch.** `_fern` 456 m aus SW von der Stadtstraße (Augenhöhe): Talmulde, darüber der rote Fleck am Hang –
der Farbakzent, den `witcher_07` vormacht. `_anmarsch` 79 m (Anteil 0,60): rote Kronen schimmern durch grüne Stämme.
`_held` 48 m von SO quer zum Hang (Blick 120°): der rote Laubstrom hangab im Vordergrund, der alte Baum als Blickziel. `_nah`
10 m: rote Blätter auf Moos und Wurzeln. Zugang ohne Pfad: 185 m, max 18,4° vom Weg (2579/−981).

**Detail-Ebenen.** Held (1): Altbuche `SM_beech_tree_05` ×1,3 mit rotem Laub. Begleiter (13): `SM_beech_tree_03/07/09` in Gruppe,
gleiche rote Tönung, 2 junge `SM_beech_tree_00_C` am Rand in Übergangsfarbe (orange). Schutt (60): Äste
`SM_detail_branches_03`, `SM_OldTreeBranch_05`. Kleinzeug (Tausende): rotes Laub = `SM_DeadLeaves_01–08` + `SM_detail_leaves_01`
mit rotem Material, dichter hangab (Fließrichtung = Ursache), Bucheckern. Bewuchs nach Ursache: Unterwuchs spärlich (Buchenschatten),
nur Sauerklee/Efeu (`SM_ivy_01_1`, `SM_CloverVarieties_01`), Farn am bachseitigen Rand. Kontakt: Wurzelanläufe
`SM_beech_old_roots_01`, Laub liegt in Mulden dicker.

**Wasser, Effekte, Licht.** Kein Wasser. Niagara fallende rote Blätter (optional, „Niagara VFX Pack — Snow, Sakura Petals,
Autumn Leaves & Steam" oder Free Niagara Particles). Kein Licht.

**Geländeänderung.** Keine Form. Lage Laub 255 im Hain und als Zunge 90 m hangab. Fenster 120 × 120 m.

**Assets.** Bestand s. o. Materialwünsche: `MI_EL_SW_Rotlaub` (M_EL_Pflanze, `Farbe` [0,78, 0,16, 0,10, 1], `Variation` 0,4) für die
Blatt-Slots der Buchen `SM_beech_tree_03/05/07/09` und `MI_EL_SW_Rotlaub_Boden` (gleiche Basis, `Farbe` [0,55, 0,18, 0,09, 1]) für
`SM_DeadLeaves_01–08`, `SM_detail_leaves_01`. (Die Buchen haben eigene Blattmaterialien → lokal als Instanz-Überschreibung, Ferat
entscheidet.) Wunsch: **Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam** (C, fallendes Laub), Ersatz ohne Effekt.

**Aufwand und Risiko.** Gering (≈ 15 Akteure, ~4 000 Instanzen). Risiko: nur die Tönung macht den Ort – wenn die Blattmaterialien
keine Farbüberschreibung erlauben, muss ein eigenes MI der Buchenblätter her (eigener Punkt für Ferat).

---

### 4 · Elfentreppe (`elfenwald_04_elfentreppe`) – Fundstück

**Was man sieht.** Man folgt einem Rauschen in eine Senke und steht vor einer Treppe aus Wasser: Der Waldbach fällt über
sieben flache, gerundete Stufen aus hellem, moosgrünem Kalktuff, jede mit einem klaren, türkisgrünen Becken davor. Die Kanten
sind mit Moos gepolstert, aus ihnen hängen Wasserfäden; im Becken liegen helle Kiesel und versinterte Äste. Rundum Farn,
Pestwurz und Moos – ein Feuchtering, ringsum wieder brauner Buchenwald.

**Vorbild.** Real: Plitvicer Seen (Kroatien, Kalktuff in Buchenwald), Krka; Spiel: Bachläufe im Velen-Wald und die
„Fairy Pools"-artigen Stufen in Skellige (Witcher 3), Emerald Graves (DA:I).

**Standort.** Feld H3, X 2390 / Y −1230, Boden 31,6 m. Am Bach `B_R_P4_M1_01` knapp vor dem Zusammenfluss mit drei Nachbarbächen:
Gefälle 17–21 % auf 40 m (2405/−1235 → 2371/−1214), Einzugsfläche 231 744 m² (genug Wasser für Sinter), Hang 7° im Mittel,
Flanken bis 45°, TPI100 −7,8 m (Senke). Boden Laub 76 % / Kies 15 % / Moos 9 %; hoher Wald (bis 37 m). 109 m vom Weg, 380 m von
der Elfenstadt, 522 m innen. **Verdeckung:** 4 m Zielhöhe von 0 der 159 Wegpunkte bis 400 m sichtbar.

**Komposition und Anmarsch.** `_anmarsch` 36 m (Anteil 0,61): von oben über die Böschung sieht man zuerst Glanz zwischen
Farn. `_held` 44 m quer von Osten (Blick 260°): die Treppe als Diagonale durchs Bild, Becken im Vordergrund, Lichtflecken auf
dem Wasser. `_nah` 10 m: Stufenkante mit Wasserfäden und Moospolster. Zugang ohne Pfad: 157 m, max 24,4° vom Weg (2501/−1329).

**Detail-Ebenen.** Held: 7 Tuff-Stufen (Gelände-Stempel + Akteure `SM_ForestRockShelf_01` / `SM_SmoothRockShelf_01` ×1,5 als
Stufenkanten, Material hell + Moos, bis Paket da ist). Begleiter (6): 2 große bemooste Blöcke `SM_MossyForestBoulder_04`, ein
versinterter liegender Stamm `SM_OldFallenTree_01` quer im Becken, 3 Altbuchen am Rand. Schutt (60–100): Kiesel/Steine im Bach
`SM_SmallStonesPack_01–08`, `SM_DryRiverBed_01` im Becken, Äste. Kleinzeug: Laub in den Becken-Ecken, Moosklumpen. Bewuchs nach
Ursache (Feuchtering 6–10 m): Pestwurz `SM_petasites_spurius_01–03`, Schachtelhalm `SM_rough_horsetail_01`, Farn `SM_Fern_01`,
`SM_SilverLadyFern_01`, Moos auf jeder Stufe (`SM_MossClump_*`), Sumpfdotter-Akzent `SM_YellowArchangel_01`. Kontakt: Stufen 40 %
im Gelände, Nassband (Decal `MI_TileableLeakage_02`) an jeder Kante.

**Wasser, Effekte, Licht.** Wasser: `bach` über die Stufen (Spiegelhöhen je Stufe, Stufen 0,6–1,2 m → die > 0,8 m werden kleine
Fälle), dazu 4 kleine `see`-Becken (Farbe `tuerkis`, Tiefe 0,8–1,5 m), Mündung in den vorhandenen Bach. Schaum nur an den Kanten.
Kein Licht; ein lokaler Nebel (0,02) in der Senke für Lichtschächte.

**Geländeänderung.** Stempel 80 × 50 m: Bachbett in 7 Stufen umformen (−1,5 … +1,0 m), Becken −1,2 m hinter jeder Stufe,
Rand 8 m weich. Ausnahme Wasserregel: der Ort IST dieser Bach. Lagen Kies 200 im Bett, Moos 220 an Kanten, Laub außen.

**Assets.** Bestand s. o. Wunsch: **Travertine Hot Spring Terraces – Modular Environment Pack** (B, echte Sinterkanten – Ersatz:
Felsplatten mit hellem MI), **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (B, Kaskadenwasser),
**Free City & Nature Sounds** (C, Bachrauschen). Materialwunsch `MI_EL_SW_Kalktuff` (M_EL_Fels_Auflage, `Toenung`
[1,0, 0,97, 0,88, 1], `Auflage_Menge` 0,7, `Auflage_Farbe` [0,55, 0,7, 0,35, 1]) für `SM_ForestRockShelf_01`, `SM_SmoothRockShelf_01`.

**Aufwand und Risiko.** Mittel-hoch (Wasser je Stufe, ≈ 20 Akteure, ~5 000 Instanzen). Risiko: Epic-Wasser über viele kleine
Stufen (Spiegel müssen exakt sitzen) – Fallback: ein durchgehender `bach` mit Stufen, Becken nur als Gelände.

---

### 5 · Farnschlucht (`elfenwald_05_farnschlucht`) – Fundstück

**Was man sieht.** Ein Tobel an der Grenze zum Gebirge: Der Bach stürzt über 80 m Länge 48 m tief in kleinen Kaskaden hinab,
und die Wände links und rechts (14–30 m) sind nicht Fels, sondern Farn – Wurmfarn, Hirschzunge, Frauenfarn, Schicht über
Schicht wie ein grüner Vorhang. Oben am Schluchtkopf tropft eine Quellwand; das Licht kommt nur als grüner Schimmer durch.

**Vorbild.** Real: Fern Canyon (Prairie Creek, Kalifornien), Tobel im Allgäu; Spiel: die Farnhohlwege von Skellige,
Hinterlands-Schluchten (DA:I).

**Standort.** Feld H3, X 2762 / Y −1588, Boden 87,2 m. Schlucht/Kessel: TPI25 −12,0 m, TPI100 −15 m, Hang 55° (max 68°),
84 m Relief im Kreis, Exposition 357° (N, schattig = Ursache für Farn). Nordwand +30 m, Südwand +14 m. Boden Laub 35 % /
Erde 31 % / Fels 26 %. Das Gerinne steht nur im Wasserraster (nicht in `baeche_alle`): 81 m bei x 2750 → 33 m bei x 2680.
208 m vom Weg, 246 m innen. **Verdeckung:** 0 von 67 Wegpunkten bis 400 m.

**Komposition und Anmarsch.** `_anmarsch` 28 m (Anteil 0,51) vom Pfad am Schluchtrand. `_held` 24 m vom südlichen Hangfuß
(2745/−1605) quer in die Schlucht: Kaskaden in der Mitte, Farnwand rechts füllt das Bild, Tropfwand als helles Ziel. `_nah`
10 m: Hirschzunge an nassem Fels. **Pfad nötig:** 229 m vom Weg (2563/−1531), max 27°, 11 m steil, 30 m Querhang → Pfad als
Erde-Band mit 3 Wurzelstufen am Einstieg.

**Detail-Ebenen.** Held: die Farnwände – Hunderte `SM_Fern_01–06`, `SM_SilverLadyFern_01–03`, `SM_EagleFern_M_01`,
`SM_BeechFern_04/05`, gestaffelt an den Hängen (dicht, alle Größen). Begleiter (5): eingestürzte bemooste Platten
`SM_ForestRockSlab_01`, `SM_MossyEmbankment_01/02` als Wandstücke, 2 liegende Stämme quer im Tobel `SM_FallenTreeAssembly_01`.
Schutt (100–150): Steine im Bachbett `SM_SmallStonesPack_*`, `SM_MossyRocks_01/02`. Kleinzeug: Moos, nasses Laub. Bewuchs nach
Ursache: N-Exposition + Tropfwasser → Farn und Moos statt Gras; oben am Rand Buchen, deren Wurzeln in die Schlucht hängen
(`SM_MossyForestRoots_02`). Kontakt: Farn wächst aus Moospolstern, kein nackter Boden sichtbar.

**Wasser, Effekte, Licht.** `bach` mit 6 Kaskaden (je 1–3 m) entlang der Rasterlinie, Farbe `klar`; Tropfwand am Kopf als
6 Decals `MI_Leakage_05–10` + feiner Schleier-`wasserfall` (2 m breit, 3 m). Lokaler Nebel 0,04 im Tobel. Kein Licht.

**Geländeänderung.** Stempel 90 × 40 m: Bachbett-Stufen (−1 … −2 m), Wände leicht nachschärfen (+2 m oben an der Südkante).

**Assets.** Bestand s. o. Wunsch: **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (B, Kaskaden –
Ersatz `M_EL_Wasserfall2`), **Free City & Nature Sounds** (C, Rauschen).

**Aufwand und Risiko.** Mittel (≈ 12 Akteure, ~9 000 Instanzen – viel Farn). Risiko: Bach fehlt in den Vektoren → Wasser neu
anlegen; Farn auf 55°-Hängen braucht Ausrichtung zur Hangnormale.

---

### 6 · Blauer Grund (`elfenwald_06_blauer_grund`) – Fundstück

**Was man sieht.** Nach 150 m durch braunen Buchenwald wird der Boden blau. Eine flache Senke, so groß wie ein Marktplatz,
ganz bedeckt mit blau-violetten Blüten, darüber glatte graue Buchenstämme wie Säulen, ein geschlossenes Dach – und genau in der
Mitte eine Kronenlücke, durch die ein Lichtschacht auf das Blau fällt. Kein Gras, kein Busch; nur Blüten, Stämme und Licht.

**Vorbild.** Real: Hallerbos (Belgien), Hasenglöckchenwälder Englands; Spiel: die Blumenwiesen im Wald von Toussaint
(Witcher 3: Blood and Wine), Emerald Graves (DA:I).

**Standort.** Feld G4, X 2112 / Y −390, Boden 24,4 m. Ebene: Hang 3° (max 25° an der Böschung), TPI100 −6,8 m (flache Senke),
Boden Laub 92 % / Moos 8 %, **dichtester Wald im Biom** (1 182 Baumzellen im 45-m-Kreis, max 23 m) = Ursache für
geschlossenes Dach. Bach 70 m (Frühjahrsfeuchte). 153 m vom Weg, 388 m von der Elfenstadt, 142 m innen. **Verdeckung:** 3 m
Zielhöhe von 0 der 99 Wegpunkte bis 400 m.

**Komposition und Anmarsch.** `_anmarsch` 19 m (Anteil 1,0): plötzlicher Farbwechsel zwischen den Stämmen. `_held` 25 m
(Blick 300°): Stämme als Rahmen, Blau als Fläche, Lichtschacht als Blickziel. `_nah` 10 m: Blüten mit einem moosigen Wurzelanlauf.
Zugang ohne Pfad: 158 m, max 16,4° vom Weg (2225/−281).

**Detail-Ebenen.** Held: der Blütenteppich (≈ 8 000 Instanzen `SM_Periwinkle_01–04` ×0,4–0,5, dazwischen weiße Inseln
`SM_WhiteWindflower_01–03` und `SM_LilyOfTheValley_01–03`). Begleiter (8): Hallenbuchen `SM_beech_tree_06/07` (hohe, astfreie
Formen) im lockeren Ring, ein umgestürzter Stamm `SM_LargeFallenTree_02` am Rand, auf dem das Blau endet. Schutt (40): Äste,
Rinde (`MI_ScatteredBark_01`). Kleinzeug: Altlaub zwischen den Blüten (`SM_DeadLeaves_*`), Bucheckern. Bewuchs nach Ursache:
Frühblüher nur unter Laubdach (vor dem Austrieb) – deshalb **kein** Gras; im Lichtschacht etwas dichter und höher; am
Übergang zum normalen Wald dünnt das Blau fleckig aus. Kontakt: Wurzelanläufe `SM_beech_old_roots_01`, Moos am Stammfuß.

**Wasser, Effekte, Licht.** Kein Wasser. Lokaler Nebel 0,05 (leicht blau-grau) für sichtbaren Lichtschacht; 1 Spotlicht (warm,
schwach, ohne Schatten) als Verstärkung des Schachts. Optional Niagara Pollen/Staub im Licht.

**Geländeänderung.** Keine Form. Lagen Laub 200, Moos 120 fleckig, Kraut 0 (kein GPU-Gras). Fenster 120 × 120 m.

**Assets.** Bestand s. o. (Immergrün `SM_Periwinkle_*` ist vorhanden). Wunsch: **Free Niagara Particles** (C, Pollen im Licht).

**Aufwand und Risiko.** Gering (≈ 10 Akteure, ~9 000 Instanzen). Risiko: `SM_Periwinkle` ist 1,4 m hoch modelliert →
skaliert prüfen; Farbe muss blau-violett lesen (Materialwunsch `MI_EL_SW_Blaugrund`, M_EL_Pflanze `Farbe` [0,55, 0,6, 1,0, 1],
nur falls das Original zu rosa ist).

---

### 7 · Schwammgrund (`elfenwald_07_schwammgrund`) – Fundstück

**Was man sieht.** Am nordseitigen Bachhang liegt ein gestürzter Riese, 48 m lang, halb zu Erde zerfallen. Aus ihm wachsen
Pilze, die nicht sein dürften: Schirmlinge so hoch wie ein Mensch, Konsolen von Baumschwämmen wie Treppenstufen, Trauben kleiner
Hallimasch, die im Schatten unter dem Stamm schwach grünlich glimmen. Der Boden federt, es riecht nach Moder.

**Vorbild.** Real: Totholz-Urwald Białowieża, Riesenporlinge und Zunderschwamm; Spiel: Pilzgründe in Velen und der
„Wald der Toten" (Witcher 3), Pilzhöhlen-Ästhetik der Emerald Graves.

**Standort.** Feld G4, X 1808 / Y −600, Boden 17,2 m. Unterhang 7° (max 17°), Exposition 23° (N = schattig, feucht – Ursache),
Bach 33 m (Einzugsfläche 5 420 m²), Boden Laub 99 %, 756 Baumzellen (max 24 m). 100 m vom Weg, 608 m von der Stadt, 352 m innen.
**Verdeckung:** 4 m Zielhöhe von 0 der 81 Wegpunkte bis 400 m.

**Komposition und Anmarsch.** `_anmarsch` 27 m (Anteil 1,0) von N über den Hang. `_held` 101 m entlang der Stammachse aus W
(Blick 90°): der Stamm als Diagonale, Pilze werden nach vorn größer. `_nah` 10 m: Pilzgruppe mit Glimmen im Stammschatten.
Zugang ohne Pfad: 103 m, max 7°.

**Detail-Ebenen.** Held: liegender Riese = `SM_LargeFallenTree_02` ×2 + `SM_MossyTree_01` ×2 hintereinander, Wurzelteller
`SM_Pine_roots_01` ×2 hochkant. Begleiter (6–8): 3 Riesenschirmlinge (2–4 m), 4 Konsolen-Gruppen (Wunsch Giant Fantasy Nanite
Mushrooms / Forest Fungi; Ersatz `SM_mushroom_01/02` ×6–12). Schutt (80–120): abgefallene Rinde (`MI_ScatteredBark_01`,
`MI_ScatteredTreeBark_01`), Morschholz `SM_OldFallenTree_02`, `SM_BrokenStump_01`. Kleinzeug: Hunderte kleiner Pilze
`SM_mushroom_01/02` ×0,5–1, Laub, Moos. Bewuchs nach Ursache: Zersetzung → Moos und Farn auf dem Stamm (`SM_SilverLadyFern_01`,
`SM_MossClump_*`), Jungbuchen in der Lichtlücke, die der Sturz gerissen hat (`SM_beech_plant_01/02`), Brennnessel am nährstoffreichen
Wurzelteller (`SM_nettle_01_0_SM_nettle_01_0`). Kontakt: Stamm 30 % eingesunken, Laub angeweht auf der Hangseite.

**Wasser, Effekte, Licht.** Kein Wasser. 2 Punktlichter (grün-weiß, 200 cd, 4 m, ohne Schatten) unter dem Stamm; Niagara
Sporenstaub (optional, Free Niagara Particles). Lokaler Nebel 0,03 hangab zum Bach.

**Geländeänderung.** Stamm-Mulde −0,6 m (50 × 6 m), Wurzelteller-Grube −1,0 m. Lagen Erde 160 + Moos 180 um den Stamm.

**Assets.** Bestand s. o. Wunsch: **Giant Fantasy Nanite Mushrooms** (B für diesen Ort, die Riesenpilze – ohne sie bleibt nur
skaliertes `SM_mushroom_01/02` mit sichtbar grober Geometrie), **Forest Fungi – Mushroom Pack** (B, Konsolen/Baumschwämme),
**Free Niagara Particles** (C).

**Aufwand und Risiko.** Gering-mittel (≈ 15 Akteure, ~4 000 Instanzen). Risiko: ohne Pilzpaket kein Held; „Fantasy"-Pilze dürfen
nicht bonbonfarben sein (Farbe erdig, Glimmen nur im Schatten).

---

### 8 · Wurzelbrücke (`elfenwald_08_wurzelbruecke`) – Fundstück

**Was man sieht.** In der Kerbe eines Waldbachs liegt ein einzelner Riesenstamm quer über dem Wasser, 44 m lang, 3 m dick,
ganz in Moos. Sein Wurzelteller steht am Ufer senkrecht wie eine 8 m hohe Wand aus Erde, Steinen und Wurzelsträngen; im Loch
darunter hat sich ein Tümpel gebildet. Auf dem Stamm wächst eine Reihe junger Bäume. Man kann darüber gehen.

**Vorbild.** Real: Wurzelbrücken-Motiv der Regenwälder Tasmaniens/Olympic NP (gestürzte Riesen als Brücken); Spiel: Baumstamm-
Brücken in Velen (Witcher 3), Emerald Graves (DA:I).

**Standort.** Feld H3, X 2361 / Y −1624, Boden 9,2 m. Am Bach `B_R_P4_M2_02` (Einzugsfläche 148 924 m²), Schlucht/Kessel:
TPI25 −3,7 m, TPI100 −14,5 m, Flanken bis 50°, Boden Laub 71 % / Kies 16 %. 83 m vom Weg (Straße 80 m westlich oberhalb, durch
die Kerbe verdeckt), 130 m innen. **Verdeckung:** 0 von 106 Wegpunkten bis 400 m.

**Komposition und Anmarsch.** `_anmarsch` 53 m (Anteil 0,70) vom Kerbenrand. `_held` 63 m aus NW den Bach entlang (Blick 140°):
Bach als Linie, der Stamm quer als Rahmen, Wurzelteller rechts als dunkle Masse. `_nah` 10 m: Moos und Jungbäume
auf dem Stamm. Zugang ohne Pfad: 97 m, max 19,5°.

**Detail-Ebenen.** Held: `SM_LargeFallenTree_02` ×3 (Länge ≈ 44 m) quer zum Bach, Wurzelteller `SM_stones_roots_01` ×1,2 +
`SM_Pine_roots_01` ×1,5 hochkant (Wunsch Forest Cretaceous Riesenstamm). Begleiter (4): Stumpf des Riesen am Gegenufer
`SM_RottenTreeStump_01` ×2, 2 Blöcke aus dem Wurzelteller `SM_MossyForestBoulder_03`. Schutt (60–100): Steine und Erde unter dem
Teller (`SM_ground_rock_01`, `SM_SmallStonesPack_*`), abgebrochene Äste im Bach (Treibholzstau an der Stammunterseite).
Kleinzeug: Moos, Laub, Kiesel. Bewuchs nach Ursache: Ammenstamm-Reihe junger Buchen auf dem Stamm (`SM_beech_plant_00–02`), Farn
in der feuchten Kerbe, Pestwurz am Ufer (`SM_petasites_spurius_01`). Kontakt: Stamm liegt auf beiden Ufern auf (je 10 %
eingegraben), Tümpel unter dem Wurzelteller.

**Wasser, Effekte, Licht.** Bach bleibt; ein `see`-Tümpel (5 × 4 m, `klar`, 0,6 m) im Wurzelloch; Schaum am Treibholzstau.
Kein Licht.

**Geländeänderung.** Kerbe nachschärfen: Ufer −1,5 m auf 30 m Länge (Kerbe wirkt 5–6 m tief), Wurzelloch −1,2 m. Lagen Kies im
Bett, Moos 200 an den Ufern.

**Assets.** Bestand s. o. Wunsch: **Forest Cretaceous** (B, Riesenstamm – Ersatz skalierte `SM_LargeFallenTree_02`),
**Forest Fungi – Mushroom Pack** (C, Pilze am Stamm).

**Aufwand und Risiko.** Gering (≈ 10 Akteure, ~3 000 Instanzen). Risiko: begehbarer Stamm braucht saubere Kollision (Akteur mit
Kollision, Kapsel).

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/dschungel/katalog.md](sehens/dschungel/katalog.md)

### 1 · Mondtor (`dschungel_01_mondtor`) – Leuchtfeuer

**Was man sieht.** Über dem Wald am Nordrand steht ein 100 m hoher Kalkturm, und oben an seiner Schulter klafft ein rundes
Loch, durch das der Himmel scheint – ein steinerner Mond. Von der Straße unten liest man ihn aus jeder Richtung: dunkler Turm,
heller Kreis. Wer den Pfad über die Westrampe hinaufsteigt, steht im Tor: ein 26 m weiter Bogen, innen glatt gewaschen, mit
Farnen und Lianen, die von der Kante hängen, und dem Blick über die Karstebene bis zum Meer.

**Vorbild.** Real: Moon Hill (Yueliang Shan, Yangshuo), Tianmen-Höhle (Zhangjiajie); Spiel: Felsfenster der Hinterlands und
der Exalted Plains (DA:I), Skellige-Felstore (Witcher 3).

**Standort.** Feld G5 (Ränder G6), X 1786 / Y 958, Boden 101 m – Kuppe des Turms: TPI100 +53 m, TPI25 +28 m, Wände bis 86°,
83 m Relief im 45-m-Kreis, Boden Fels 66 % / Laub 19 %. Westseite eine Rampe (43 → 101 m auf 86 m, ≈ 34°), Ostseite fällt
senkrecht auf 31 m; nach Süden ein Spalt bis 26 m zwischen zwei Turmteilen (Ursache des Fensters: Verkarstung entlang der Kluft).
80 m vom Weg (am Fuß), 208 m innen. **Sicht:** 25 m Bogenhöhe → **196 von 241** Wegpunkten (300–800 m) sehen ≥ 30 % (Mittel
0,79), lesbar bis 800 m; bester (1356/710) in 496 m, Anteil 1,00 – das stärkste Leuchtfeuer des Bioms.

**Komposition und Anmarsch.** `_fern` 496 m aus WNW von der Straße (Augenhöhe, Blick 120°): Turm mit Lichtkreis über dem
Wald. `_anmarsch` 156 m (Anteil 0,94) am Rampenfuß. `_held` 50 m vom Turmrücken im Süden (Blick 350°): durch das Tor hindurch
auf Ebene und Meer, Lianen als Rahmen. `_nah` 10 m: Torlaibung mit Sinterspuren. **Pfad nötig:** 274 m vom Weg (1667/857),
max 34°, 31 m steiler als 25°, 75 m Querhang → Pfad über die Westrampe, im Steilstück natürliche Kalkstufen
(`SM_ForestRockShelf_01–03`, `SM_flat_rock_02`) und Wurzeltritte.

**Detail-Ebenen.** Held: der Bogen – zwei Pfeiler `SM_Cliff_01c` ×0,35 und ein liegender Sturz `SM_Cliff_01b` ×0,45 (Akteure,
Material `M_EL_Klippe_RVT` mit Moosband oben), am Gipfelgrat eingebunden in die bestehenden Turmwände. Begleiter (5):
abgebrochene Bogenstücke als Blöcke am Rampenfuß (`SM_Big_Rock_03`, `SM_mountain_rock_big_02_1`), zwei Bonsai-Kiefern-artige
Kronen `SM_Tree_Small_01a` ×0,4 auf dem Sturz. Schutt (60–120): Kalkschutt unter dem Tor `SM_LimestoneRocks2/3`,
`SM_ground_rock_01`, Schuttkegel an der Ostwand (Ursache: Frostsprengung/Lösung). Kleinzeug: Kalkgrus, Laub, Samen. Bewuchs nach
Ursache: Lianen von der Torkante (`SM_Vines_01a`, `SM_Ivy_11`, `SM_Ivy_25` hängend), Farn in der feuchten Laibung
(`SM_Fern_01a`, `SM_Fern_02a`), Büsche nur auf Simsen (`SM_Bush_01a`), Moos-/Flechten-Decals auf der Wetterseite. Kontakt: Pfeiler
40 % im Gelände, Schuttsaum, Moosband.

**Wasser, Effekte, Licht.** Kein Wasser. Kein Licht (Gegenlicht durch das Tor genügt). 2 Decals `MI_Leakage_03` als Sinterstreifen.

**Geländeänderung.** Gipfel: Kerbe −6 m (20 × 8 m) für die Torsohle, Rampe geglättet als Pfad (±1 m). Fenster 120 × 120 m.

**Assets.** Bestand s. o. **Lücke:** Es gibt keinen Kalk-Felsbogen im Bestand oder in der Download-Liste – Lösung ohne Asset:
Bogen aus `SM_Cliff_01b/01c` (wie oben), Fuge mit Lianen/Moos kaschieren. Wunsch: **Megascans Limestone Rocks** (B, Kalkschutt –
Ersatz `SM_LimestoneRocks2/3`).

**Aufwand und Risiko.** Mittel (≈ 20 Akteure, ~3 000 Instanzen). Risiko: zusammengesetzter Bogen kann aus 500 m künstlich
wirken (Fugen) → im Editor zuerst `_fern`; Plan B: Fenster als Loch zwischen zwei Turmköpfen (Kerbe statt Sturz).

---

### 2 · Turmquelle (`dschungel_02_turmquelle`) – Leuchtfeuer

**Was man sieht.** An der Nordwand eines 160 m hohen Turms tritt auf halber Höhe Wasser aus dem Fels – kein Bach führt hinauf,
der Berg selbst blutet. Ein weißer Strahl fällt 45 m frei, zerstäubt an einem Absatz, und landet in einem türkisgrünen
Tosbecken am Wandfuß. Von der Straße sieht man den hellen Streifen auf der dunklen Wand und den Dunst darüber.

**Vorbild.** Real: Karstquellen in Guizhou (Huangguoshu-Umfeld), Fontaine de Vaucluse, Kaieteur-Wandquellen; Spiel: Wasserfälle
an Skellige-Klippen (Witcher 3), Crestwood (DA:I).

**Standort.** Feld G5 (Ränder G6), X 2250 / Y 962, Boden 34,7 m. Talboden vor dem Turm (2294/1048, Gipfel 159,5 m): Hang 13°,
Wand 4–16 m entfernt mit bis 82°, Wandhöhe 119 m, 97 m Relief im Kreis, Boden Laub 81 % / Fels 19 %. 83 m vom Weg, 212 m innen,
Gewässer 131 m nordwestlich (Mündung des neuen Bachs). **Sicht:** 60 m Zielhöhe (Wandstreifen) → 60 von 166 Wegpunkten sehen
≥ 30 % (Mittel 0,23), lesbar bis 798 m; bester (2128/660) in 326 m, 0,90.

**Komposition und Anmarsch.** `_fern` 326 m von NNW (Augenhöhe, Blick 158°): Turm, weißer Faden, Dunst. `_anmarsch` 83 m
(Anteil 0,92) direkt vom Weg. `_held` 120 m aus NO (Blick 230°): Becken im Vordergrund, Fall als Vertikale, Turmkopf mit
Bonsai-Kronen. `_nah` 10 m: Tosbecken mit Gischt und Kalkblöcken. Zugang ohne Pfad: 83 m, max 6,4°.

**Detail-Ebenen.** Held: Wasserfall (Mesh/Material) aus einer Felsnische (`SM_Cliff_01e` ×0,25 als Quellmund-Lippe). Begleiter
(6): Absatz mit Kolk auf halber Höhe (`SM_ForestRockShelf_02` ×3), Sturzblöcke im Becken `SM_Big_Rock_01/03`, `SM_LimestoneRocks3`
×3. Schutt (100–150): Kalkgeröll am Wandfuß `SM_ground_rock_01/02`, Kies im Abfluss `SM_SmallStonesPack_*`. Kleinzeug: Kiesel,
nasses Laub. Bewuchs nach Ursache: Sprühzone (Radius 20 m) dicht grün – Moos auf allem (`M_EL_Klippe_RVT` Moos), Farne
`SM_Fern_01a`, Lianen `SM_Vines_01a` neben dem Fall, Riesenblätter-Ersatz `SM_petasites_spurius_01–03` ×2,5, Palmen
`SM_Palm_01_06_G`, `SM_Palm_01_10_G` am Beckenrand; außerhalb normaler Laubwald. Kontakt: Nassband (Decal `MI_TileableLeakage_03`)
in der Wand unter dem Quellmund, Kalkkrusten am Beckenrand.

**Wasser, Effekte, Licht.** `wasserfall` (Kante 6 m breit bei +45 m, Fuß 35 m, `M_EL_Wasserfall2`), `see` Tosbecken (D 22 m,
`tuerkis`, 2,5 m), `bach` 95 m vom Becken nach NW in das vorhandene Gerinne (Quelle = Becken). Gischt: Niagara (optional).
Lokaler Nebel 0,06 am Fuß. Kein Licht.

**Geländeänderung.** Becken −3 m (D 22 m) mit Rand, Bachrinne −0,8 m auf 95 m. Fenster 140 × 120 m.

**Assets.** Bestand s. o. Wunsch: **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (A, Fall und Bach),
**Nature Water FX (Fontänen, Geysire, Bäche, Wasserfälle)** (B, Gischt am Fuß – Ersatz lokaler Nebel), **Niagara Examples
Pack** (B), **Free City & Nature Sounds** (B, Rauschen).

**Aufwand und Risiko.** Mittel (≈ 15 Akteure, ~5 000 Instanzen). Risiko: Fall aus der Wandmitte braucht eine sichtbare Ursache
(dunkle Quellnische, Sinterfahne darunter) – sonst wirkt es wie ein Rohr.

---

### 3 · Steinwald (`dschungel_03_steinwald`) – Leuchtfeuer

**Was man sieht.** Auf der Schulter eines Turms im Osten steht ein Wald aus Stein: sechzig graue Kalknadeln, 4–18 m hoch,
messerscharf gerillt, dicht wie Bäume. Von der Straße sieht man eine gezackte Krone über dem Grün. Oben geht man durch enge
Gassen zwischen den Nadeln; in den Fugen wachsen Farne, kleine Palmen und Lianen, die von Nadel zu Nadel hängen.

**Vorbild.** Real: Shilin (Steinwald, Yunnan), Tsingy de Bemaraha (Madagaskar); Spiel: Felsnadelfelder der Exalted Plains
(DA:I), Skellige-Zacken (Witcher 3).

**Standort.** Feld H6 (Ränder I6), X 3330 / Y 1442, Boden 132,6 m. Turmschulter: TPI100 +32,5 m, TPI25 +16,5 m, Hang 12° auf der
Schulter, Wände bis 77°, Boden Fels 57 % / Laub 28 %. 286 m vom Weg, 428 m innen. **Sicht:** 15 m Nadelhöhe → 24 von 157
Wegpunkten sehen ≥ 30 %, lesbar bis 792 m; bester (3114/990) in 501 m, Anteil 1,00.

**Komposition und Anmarsch.** `_fern` 501 m aus NNW (Augenhöhe, Blick 154°): gezackte Silhouette über dem Wald.
`_anmarsch` 154 m vom Pfad (Anteil 1,0). `_held` 48 m von OSO (Blick 300°): Gasse zwischen den Nadeln als Tiefenachse, am Ende
Ausblick. `_nah` 10 m: Karrenrillen an einer Nadel. **Pfad nötig:** 531 m vom Weg (3555/1229), max 38°, 19 m steil, 36 m
Querhang → Pfad mit natürlichen Kalkstufen.

**Detail-Ebenen.** Held: 60 Nadeln – `SM_Cliff_01b`, `SM_Cliff_01c`, `SM_Cliff_01e` aufrecht ×0,08–0,25 (4–18 m), gleiche Felsfarbe
wie die Türme. Begleiter (6): 3 umgestürzte Nadeln als Blöcke (`SM_Big_Rock_03`), 3 Bonsai-Bäume `SM_Tree_Small_01a` ×0,4. Schutt
(150–200): Kalkplatten und Scherben `SM_LimestoneRocks2/3`, `SM_flat_rock_03/04`, `SM_ground_rock_03_01`. Kleinzeug: Grus, Laub in
den Gassen. Bewuchs nach Ursache: Humus nur in Spalten → Farn `SM_Fern_01a`/`SM_Fern_02a`, Büsche `SM_Bush_01a`, Jungpalmen
`SM_Palm_01_11_G`/`_12_G`, Lianen `SM_Vines_01a`; auf den Nadeln nur Flechten (Decal `MI_TileableMossPatches_03`). Kontakt:
Nadeln 30 % eingegraben, Schuttsaum, Laub in den Gassen.

**Wasser, Effekte, Licht.** Kein Wasser, keine Effekte. Licht: Schattenlinien der Nadeln bei fester Sonne (24°) = Bildwirkung.

**Geländeänderung.** Schulter leicht verebnen (±1,5 m) für Gassen; Lagen Fels 200, Kies 120 in Gassen. Fenster 110 × 110 m.

**Assets.** Bestand s. o. **Lücke:** keine Kalknadel-Netze – Lösung ohne Asset: skalierte `SM_Cliff_01*`. Wunsch: **Megascans
Limestone Rocks** (B, Platten/Karren), **Procedural Rocks Generator** (C, falls gewünscht eigene Nadeln).

**Aufwand und Risiko.** Mittel (≈ 70 Akteure – an der 80er-Grenze, ~4 000 Instanzen). Risiko: Wiederholung der Cliff-Formen
→ jede Nadel anders gedreht/skaliert, Deckungs-Prüfung mit `_held`.

---

### 4 · Blaues Auge (`dschungel_04_blaues_auge`) – Fundstück

**Was man sieht.** Zwischen drei Türmen öffnet sich im Wald plötzlich der Boden: ein fast runder Schacht, 50 × 60 m, mit
senkrechten, moosgrünen Wänden. 6–20 m tiefer liegt Wasser von einem Blau, das man nicht für möglich hält. Von der Kante hängen
Luftwurzeln und Lianen bis ins Wasser; Licht fällt als Kegel hinein und zeichnet den hellen Grund nach.

**Vorbild.** Real: Ik Kil und Cenote Suytun (Yucatán); Spiel: Cenote-artige Wasserlöcher in Shadow of the Tomb Raider,
Emprise du Lion-Höhlenseen (DA:I).

**Standort.** Feld H6, Mitte am Ostrand X 2436 / Y 1278 (Boden 16,4 m). Der Schacht selbst (2368–2416 / 1254–1316, 2 344 m²)
reicht unter Meerniveau (Gelände −2 m, heute als „Meer" kodiert) – er ist schon im Gelände, ohne Stempel. Rand im Osten 5–20 m,
im Westen steigt er zum Turm (125 m). Wald bis 61 m hoch. 239 m vom Weg, Mitte bewusst auf dem Rand (die Mitte darf nicht im
Meer liegen). **Verdeckung:** 4 m Zielhöhe von 0 der 48 Wegpunkte bis 400 m.

**Komposition und Anmarsch.** `_anmarsch` 77 m (Anteil 1,0) von NW durch den Wald – der Schacht erscheint erst 20 m vor der Kante.
`_held` 82 m aus NW (Blick 150°) über die Kante hinab: Wurzelvorhang links, Lichtkegel auf dem Wasser. `_nah` 10 m: Kante mit
Luftwurzeln. Zugang ohne Pfad: 287 m vom Weg (2213/1195), max 23°.

**Detail-Ebenen.** Held: Schachtwände – Ring aus `SM_Cliff_01d` ×0,25 und `SM_HugeMossyForestCliff_01` ×2 (Akteure, 40 % unter
Wasser), damit die Wand wirklich senkrecht ist. Begleiter (6): Riesenbaum `SM_Tree_Big_01a` am Westrand, dessen Luftwurzeln
herabhängen (`SM_Vines_01a` ×2, `SM_Ivy_11/17/25`), 2 Sturzblöcke im Wasser `SM_MossyForestBoulder_04`, `SM_LimestoneRocks3`.
Schutt (40–60): Kalkplatten an einem schmalen Uferband `SM_flat_rock_02`, Äste im Wasser. Kleinzeug: Laub auf dem Wasser
(Decal), Kiesel am Grund. Bewuchs nach Ursache: feuchte Wand → Moos + Farn in Bändern (`SM_Fern_01a`), Rand mit Riesenblättern
(`SM_petasites_spurius_*` ×2,5) und Palmen `SM_Palm_01_04_G`; im Wasser nichts (tief, klar). Kontakt: Moos-Nassband 1 m über
dem Spiegel (`MI_TileableLeakage_01`).

**Wasser, Effekte, Licht.** `see` mit eigenem Spiegel +0,3 m (Umriss aus den Meer-Zellen, **`tuerkis`** – 13c: eigener See, unabhängig vom Meer, Tiefe 18 m), damit der
Ozean nicht durchscheint. Lichtkegel: 1 Spotlicht von oben (weiß, schwach, ohne Schatten) + lokaler Nebel 0,03 im Schacht.

**Geländeänderung.** Keine (Schacht vorhanden); Rand im Osten +2 m angehoben, damit das Ufer rundum über dem Spiegel liegt
(§5). Fenster 120 × 120 m.

**Assets.** Bestand s. o. Wunsch: **Electric Dreams Environment** (B, tropische Uferpflanzen, Wurzeln), **Tropical Vegetation
Assets** (C).

**Aufwand und Risiko.** Mittel (≈ 30 Akteure, ~3 000 Instanzen). Risiko: Ozean-Ebene im Schacht (Meer-Kodierung) → eigener
`see` muss sie abdecken; Ferat bitte prüfen, ob dort heute Meerwasser sichtbar ist (Bildwunsch).

---

### 5 · Verborgene Lagune (`dschungel_05_verborgene_lagune`) – Fundstück

**Was man sieht.** Im Fuß eines großen Turms klafft eine Spalte. Man zwängt sich 40 m durch eine Gasse, kaum breiter als
ein Karren, die Wände 30 m hoch – und steht am Ufer eines smaragdgrünen Sees, ringsum Wände bis 125 m, oben ein schmaler
Himmel. Lianen hängen bis aufs Wasser, Seerosen-artige Blätter treiben, es ist still bis auf Tropfen.

**Vorbild.** Real: Hongs von Phang Nga (Thailand), Tham Lod-Lagunen; Spiel: verborgene Buchten in Skellige (Witcher 3),
Kraterseen der Emerald Graves (DA:I).

**Standort.** Feld G6, X 1897 / Y 1377, Boden 23 m. Geschlossenes Becken in der Turmspalte (`becken.py`): Boden 9,5 m,
Überlauf 38 m, Tiefe 29 m, Ausdehnung 142 × 98 m; TPI25 −49,7 m, Nordostwand bis 125 m, Südwestwand 50–56 m, außen 20 m. Boden Fels
66 %. 276 m vom Weg, 286 m innen. **Verdeckung:** 0 von 41 Wegpunkten bis 400 m.

**Komposition und Anmarsch.** `_anmarsch` 44 m (Anteil 1,0) am Ausgang der Gasse. `_held` 82 m aus OSO (Blick 300°) die Spalte
entlang: Wasser als glatte Fläche, Lianen-Vorhänge gestaffelt. `_nah` 10 m: Ufer mit Wurzeln. **Pfad nötig:** Gasse
(1944/1442 → 1922/1402, 43 m, Stempel) + Fußweg 488 m vom Weg (2123/1157), max 33,5°, 4 m steil, 26 m Querhang; gesamt 531 m.

**Detail-Ebenen.** Held: Lagune + Gasse. Begleiter (6): Sturzblöcke im Wasser (`SM_Big_Rock_01`, `SM_LimestoneRocks3`), ein in
die Spalte gestürzter Baum `SM_MossyTree_01`. Schutt (60–100): Kalkschutt in der Gasse `SM_ground_rock_01`, Kiesbank am Ufer
`SM_DryRiverBed_01`, `SM_SmallStonesPack_*`. Kleinzeug: Laub, Treibgut. Bewuchs nach Ursache: Schatten + Feuchte → Lianen von den
Kanten (`SM_Vines_01a`, `SM_Ivy_11/17/21/25`), Farn in Wandritzen `SM_Fern_02a`, Uferpflanzen `SM_ToadRush_010`, Schwimmblätter
`SM_WaterPlant01–04`; oben am Kamm Bonsai-Kronen. Kontakt: Nassband und Kalksinter am Spiegel (`MI_TileableLeakage_04`).

**Wasser, Effekte, Licht.** `see` (Umriss = Becken unter 19 m, Spiegel 19 m, `smaragd`, 6–9 m tief); Überlauf durch die Gasse als
kurzer `bach` (versickert nach 30 m). Lokaler Nebel 0,05. Kein Licht.

**Geländeänderung.** Gasse durch die Südwestwand: 43 × 6 m, bis −30 m (Wand 50 m → Sohle 20 m), Ränder 8 m weich; Becken nicht
ändern. Fenster 150 × 120 m. Überhänge der Gasse als Akteure (`SM_Cliff_01b` ×0,2).

**Assets.** Bestand s. o. Wunsch: **Rain Forest Pack** (C, Lianen/Schwimmpflanzen), **Megascans Limestone Rocks** (C),
**Megascans Rembrandt Water Lily** (C, falls Seerosen erwünscht – sonst `SM_WaterPlant01–04`).

**Aufwand und Risiko.** Mittel-hoch (Stempel 30 m tief, ≈ 25 Akteure, ~4 000 Instanzen). Risiko: die Spalte ist im Gelände sehr
geradlinig (Rechteckform) – Wandakteure müssen sie brechen.

---

### 6 · Schluckhöhle (`dschungel_06_schluckhoehle`) – Fundstück

**Was man sieht.** Am Westrand, wo der Wald in eine offene Kalkplatte übergeht, laufen zwei Bäche von Norden und Süden aufeinander
zu – und verschwinden. Unter einer 7 m hohen Kalkbank öffnet sich ein dunkles Portal in einem Trichter; das Wasser gurgelt über
Kiesel hinein, Treibholz hat sich vor dem Loch verkeilt, kühle Luft kommt heraus.

**Vorbild.** Real: Ponore der Karstpoljen (Planinsko polje, Slowenien), Xe Bang Fai (Laos); Spiel: Höhleneingänge in Velen
(Witcher 3), Emprise du Lion (DA:I).

**Standort.** Feld G6, Mitte X 1468 / Y 1106 (Boden 17,2 m) auf der Kalkbank, Portal (1476/1099) am Fuß. Die Bäche
`B_R2_R_P3_P1_03` (Quelle 1550/1006) und `B_R_P3_P1_03` (Quelle 1500/1180) enden beide bei 1490–1496 / 1092–1094, ohne Abfluss
(`im_wasser` = falsch) – die Schwinde ist die Ursache. Stufe 17 → 10 m, Boden Felsplatte 44 % / Trockengras 29 % / Moos 17 %
(offenes Karstpflaster), Einzugsfläche 57 972 m². 222 m vom Weg, 118 m innen. **Verdeckung:** Portal mit 4 m Zielhöhe von 0 der
44 Wegpunkte bis 400 m sichtbar (mit dem geplanten Trichter −6 m erst recht); die Mitte auf der Bank sehen 2 Wegpunkte in
220–350 m (max 0,83) – dort sieht man nur eine niedrige Kalkbank in der Ebene, nicht das Portal.

**Komposition und Anmarsch.** `_anmarsch` 221 m vom Weg im Norden (Anteil 0,83 auf die Bank). `_held` 25 m (Blick 190°): beide
Bäche als Linien ins dunkle Tor, Treibholz im Mittelgrund. `_nah` 10 m: Wasser fällt über Kiesel ins Dunkel. Zugang ohne Pfad:
235 m, max 16°.

**Detail-Ebenen.** Held: Portal – Überhang `SM_Cliff_01e` ×0,12 als Höhlendach, Laibung `SM_ForestRockShelf_01–03`. Begleiter (5):
Kalkbank aus `SM_LimestoneRocks3` ×3–4, `SM_SmoothRockShelf_01`; Treibholzstau `SM_OldTreeBranch_05`, `SM_BrokenTreeAssembly_01`.
Schutt (80–120): Kies und Kalkscherben im Trichter `SM_SmallStonesPack_*`, `SM_ground_rock_03_01`. Kleinzeug: Schwemmlaub,
Zweige an der Hochwassermarke. Bewuchs nach Ursache: Feuchte im Trichter → Moos/Farn (`SM_Fern_02a`), Schachtelhalm
`SM_rough_horsetail_01`; auf der trockenen Platte Trockengras/`SM_KikuyuGrass_*`, Kraut in den Karren. Kontakt: Hochwasserlinie als
Decal `MI_Leakage_08`, Schlamm/Kies-Saum.

**Wasser, Effekte, Licht.** Beide Bäche verlängern bis ins Portal (`muendung`: `versickert`), letzte 6 m mit Gefälle 1:3 (Strudel,
Schaum). Lokaler Nebel 0,05 im Portal (kalte Luft), Portalinneres schwarz (Decal + Geometrie). Kein Licht.

**Geländeänderung.** Schwinde-Trichter 30 × 20 m, −6 m, Ränder weich; Bachenden an den Trichter anschließen. Fenster 80 × 60 m.

**Assets.** Bestand s. o. Wunsch: **Cave Ambience** (B, Klang aus dem Portal – sonst stumm), **Cave Stalactites & Wall Kit –
Midpoly Nanite-Ready Asset Pack** (neu, C, Laibung/Tropfsteine im Portal), **Megascans Limestone Rocks** (C).

**Aufwand und Risiko.** Gering-mittel (≈ 12 Akteure, ~2 500 Instanzen). Risiko: zwei Bäche in ein Loch – Epic-Wasser endet sauber
nur, wenn das Bachende im Dunkel liegt.

---

### 7 · Garten der Riesen (`dschungel_07_garten_der_riesen`) – Fundstück

**Was man sieht.** Unter 60 m hohen Urwaldriesen liegt eine Lichtung, in der alles zu groß ist: Blätter wie Segel, 2–4 m hohe
Elefantenohren und Bananenstauden, darüber rote und pinke Blütenkolben. Man geht zwischen Blättern hindurch, die über dem Kopf
zusammenschlagen; Licht fällt grün durch sie hindurch.

**Vorbild.** Real: Unterwuchs-Lichtungen im Daintree und auf Borneo (Alocasia, Colocasia, Heliconia); Spiel: der Dschungel aus
Shadow of the Tomb Raider, Uncharted 4; Farbregie nach DA:I.

**Standort.** Feld H6, X 2892 / Y 1264, Boden 17,4 m. Ebene 2,9°, Boden Laub 67 % / Gras 33 % (Lichtung = Ursache: Licht für
Großblattpflanzen), umgeben von Bäumen bis 61 m (271 Baumzellen im Kreis, aber Mitte frei). Fluss/Bach 49 m (feucht). 209 m vom
Weg, 384 m innen. **Verdeckung:** 3 m Zielhöhe von 0 der 50 Wegpunkte bis 400 m.

**Komposition und Anmarsch.** `_anmarsch` 151 m (Anteil 1,0) von SSW über die Bachquerung. `_held` 82 m von SSO (Blick 330°):
Blattmassen im Vordergrund, Riesenstämme als Säulen dahinter, Blütenakzent. `_nah` 10 m: Blattunterseite im Gegenlicht.
**Pfad nötig:** 232 m vom Weg (2949/1063), max 17°, 11 m über einen Bach → Trittsteine `SM_flat_rock_02`, `SM_SmallStonesPack_*`.

**Detail-Ebenen.** Held: Blattpflanzen (Wunsch Nanite Tropical Plant Pack 2 / Tropical Vegetation; Ersatz `SM_petasites_spurius_01–03`
×3–4 und `SM_Fern_01a` ×2). Begleiter (6–8): 2 Riesenbäume `SM_Tree_Big_01b` am Rand, ein gestürzter Stamm `SM_LargeFallenTree_02`
(Ursache der Lichtung), Palmen `SM_Palm_01_02_G/_03_G`. Schutt (40): Äste, Fruchtschalen-artige Zweige `SM_detail_branches_03`.
Kleinzeug: Laub, große gefallene Blätter (Decal `MI_PlantsPerennials_01`). Bewuchs nach Ursache: Lichtung → Großblatt + Blüten
(`SM_Crownbeard_03–10` gelb als Ersatz, Blüten rot/pink nur aus Paket), Waldrand mit `SM_Bush_01a`; im Schatten nur Farn. Kontakt:
Blätter dicht, Boden kaum sichtbar.

**Wasser, Effekte, Licht.** Bach bleibt (Trittsteine). Lokaler Nebel 0,04 (feuchte Luft, Lichtstrahlen). Kein Licht.

**Geländeänderung.** Keine Form. Lagen Kraut 220, Gras 160, Laub außen. Fenster 100 × 100 m.

**Assets.** Bestand s. o. Wunsch: **Nanite Tropical Plant Pack 2** (neu, B – Seborn3D, Taro/Colocasia u. a.,
https://www.fab.com/listings/70db06c9-ad22-4ae0-bfe4-dd77976cfa78, Preis ungeprüft), **Electric Dreams Environment** (B),
**Tropical Vegetation Assets** (C), **Rain Forest Pack** (C).

**Aufwand und Risiko.** Gering (≈ 10 Akteure, ~3 000 Instanzen). Risiko: **ohne Paket kein Held** – Pestwurz-Ersatz bleibt
„groß, aber europäisch". Erst nach Download bauen.

---

### 8 · Sinterhalle (`dschungel_08_sinterhalle`) – Fundstück

**Was man sieht.** Am Fuß der Südwand im Karstmassiv wölbt sich der Fels zu einem 40 m breiten, 12 m hohen Dach. Darunter ist es
trocken und kühl; von der Dachkante hängen Sinterfahnen wie erstarrte Vorhänge, ein Tropfvorhang klickt in ein Becken mit
weißem Sinterrand. Der Boden ist glatter Kalk mit Tierpfaden – draußen gleißender Dschungel, drinnen Dämmerung.

**Vorbild.** Real: Westeingang der Niah-Höhle (Borneo), Abris im Karst von Phong Nha; Spiel: Höhlenvorhallen in
Shadow of the Tomb Raider, Felsnischen in Skellige (Witcher 3).

**Standort.** Feld I7, Mitte X 3780 / Y 2120 (Boden 20,5 m) auf dem Schuttkegel vor der Wand, Abri bei 3736/2120 am Wandfuß
(Wand 125 → 85 m auf 20 m, darunter Talus 23°). Exposition 91° (O, Morgensonne in die Halle), Boden Gras 57 % / Fels 26 %, Meer
68 m. 128 m vom Weg, 68 m innen (Ostrand des Rechtecks; das Massiv selbst liegt innen). **Verdeckung:** 0 von 46 Wegpunkten.

**Komposition und Anmarsch.** `_anmarsch` 53 m (Anteil 0,91) von Norden durch den Wald. `_held` 44 m von NNW (Blick 170°): Dach als
dunkler Bogen, Sinterfahnen im Gegenlicht, Becken als helle Fläche. `_nah` 10 m: Tropfbecken mit Sinterrand. Zugang ohne Pfad:
131 m, max 15°.

**Detail-Ebenen.** Held: Felsdach `SM_Cliff_01b` ×0,35 gedreht als Überhang auf der Wand (Akteur). Begleiter (6): Sinterfahnen
(Wunsch Cave Stalactites & Wall Kit; Ersatz Decals), Versturzblöcke vom Dach `SM_Big_Rock_03`, `SM_mountain_rock_big_02_1`, ein
Tropfstein-Stummel (`SM_LimestoneRocks2` hochkant). Schutt (100–150): Talus aus `SM_ground_rock_01/02`, `SM_LimestoneRocks3`, unter
dem Dach feiner. Kleinzeug: Kalkgrus, trockenes Laub angeweht. Bewuchs nach Ursache: unter dem Dach nichts (kein Licht, kein Regen);
an der Traufe ein grüner Streifen (Moos, `SM_Fern_02a`, `SM_Vines_01a` hängend); draußen Busch `SM_Bush_01a`, Palmen
`SM_Palm_01_07_G`. Kontakt: Sinterfahnen-Decals `MI_Leakage_01–13`, `MI_TileableLeakage_01–04` an der Wand, Tropfnässe-Flecken.

**Wasser, Effekte, Licht.** `see` Tropfbecken (D 12 m, `klar`, 0,4 m) mit Sinterrand; Tropfen als Niagara (optional). 1 Punktlicht
(warm, schwach) als Reflexlicht unter dem Dach. Lokaler Nebel 0,02.

**Geländeänderung.** Hallenboden verebnen (−1,5 m, 30 × 12 m), Becken −0,5 m. Fenster 90 × 70 m.

**Assets.** Bestand s. o. Wunsch: **Cave Stalactites & Wall Kit – Midpoly Nanite-Ready Asset Pack** (neu, B,
https://www.fab.com/listings/6d72a075-8a87-4add-b1df-a6e5664bd4c8, Preis ungeprüft – Stalaktiten, Wandmodule, Nanite, UE 5.0+),
**Travertine Hot Spring Terraces – Modular Environment Pack** (C, Sinterbecken), **Cave Ambience** (C).

**Aufwand und Risiko.** Mittel (≈ 25 Akteure, ~3 000 Instanzen). Risiko: Überhang aus gedrehtem Cliff-Netz – Kontaktlinie zur Wand
mit Moos/Decals verstecken.

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/lava/katalog.md](sehens/lava/katalog.md)

### lava_01_schwarze_mauer – Die Schwarze Mauer (Leuchtfeuer)

**Was man sieht:** Aus dem grünen Moospolster steigt unvermittelt eine schwarze Wand aus Blocklava, 6–9 m hoch, 140 m lang, in
Wellen vor- und zurückspringend – die erstarrte Stirn eines alten Stroms, der hier stehen blieb. Auf einem Vorsprung der Front ragt
ein 10 m hoher, zerfranster **Schlotturm** (Hornito) wie ein Finger auf; daneben ein kleinerer Zwilling. Vor der Wand ein Saum aus
abgebrochenen Blöcken, in den Fugen kriecht graugrünes Zackenmützenmoos hoch. Am Fuß steht ein toter, silbergrauer Baum, den der
Strom einst umflossen hat.
**Vorbild:** Stromfronten von Eldhraun und Holuhraun (Island), Hornitos am Kīlauea; Spiel: Mt. Gelmir (Elden Ring) als dunkle
Lavaküste, Hellblade II (Island-Fotogrammetrie) für Moos auf Lava.
**Standort:** C6, X −2084 / Y 1045 m, Boden 47,3 m. Westfront des alten Blockstroms (Lavafels 47 %, Moos 41 %): Profil y = 1010:
41,0 → 49,7 m (Stufe 8,7 m), y = 1040: 6,1 m, y = 1050: 5,3 m; Hang an der Front bis 45°. Weg 324 m (Archivpfad), Zalas Archiv
258 m, Biominneres 394 m. Näher an den Weg geht nicht: lava_03 (359 m) und lava_02 (387 m) begrenzen.
**Sicht:** 37 von 52 Wegpunkten im Ring 300–800 m sehen ≥ 30 % (Zielhöhe 16 m = Front + Schlotturm), mittlerer Anteil 0,57,
lesbar bis 785 m; bester Fernblick vom Pfad unterhalb Zalas Stadt (X −2506 / Y 624, 596 m, Anteil 1,0).
**Komposition und Anmarsch:** Vom Archivpfad sieht man die Wand als dunklen Strich über dem Moos, der Schlotturm bricht die Linie.
Zugang 351 m ohne Pfadbau (max. 20,2°, Mittel 4,9°). `_held` 33 m westlich im Moos, Blick nach Osten: Vordergrund Moospolster und
Blockschutt, Mitte Wand, Schlotturm als Blickziel gegen den Himmel, rechts dahinter die Vulkanflanke.
**Detail-Ebenen:** Held 1 – Schlotturm `SM_IcelandicLavaSpire_01` × 1,8 (≈ 9,6 m) + `SM_IcelandicLavaSpire_03` × 1,3 als Zwilling,
30 % eingegraben. Begleiter 6–8 – Wandschollen `SM_lava_wall_01/02/03/09` (6–7 m) schräg in der Front, `SM_lava_b_rock_01/02`
(4–5 m) als abgesackte Blöcke. Schutt 120–180 – `SM_lava_m_rock_01…08`, `SM_lava_s_rock_01…05` als Schuttsaum 8–15 m vor der
Front (Ursache: Abbrechen der Stirn), grobe Blöcke unten, feine oben. Kleinzeug Hunderte – `SM_lava_s_rock_06/07/08`,
`SM_SmallStonesPack_08…14`. Bewuchs nach Ursache – Moospolster (`SM_moss_01/02`, `SM_MossClump_01/03/05`, Lage Moos) vor der Front
und auf schattigen Blockoberseiten (`MI_EL_SW_Lava_Moos`), Pioniere in Spalten der Krone (`SM_dwarf_pine_small_01/02`,
`SM_wk2oaeyqx_VarB/C`), toter Baum `Fir_08_Dead_NoBillboard` am Fuß (Natur erzählt: vom Strom eingeschlossen), trockene Zweige
`SM_DryBranches_04/07`. Kontaktzone – Blöcke 30–45 % eingegraben, Moos kriecht an der Wand bis 1,5 m hoch, Kiesrand im Schuttsaum.
**Wasser, Effekte, Licht:** kein Wasser, keine Glut (kalter, alter Strom). Westseitige Wand im Licht, Schlagschatten der Blöcke.
**Geländeänderung:** Rücken +3 m entlang der Front (Band 10 m, Rand 7 m) → Wand 8–12 m; Fenster ca. 200 × 220 m.
**Assets:** Bestand wie oben (alle in `netze.csv`). Wunsch: „Tundra Icelandic Rock Cluster“ (neu, C) für bemooste Kontaktblöcke;
Ersatz `SM_lava_m_rock_*` + `MI_EL_SW_Lava_Moos`.
**Aufwand und Risiko:** mittel. Risiko: Texel-Dichte des 1,8-fach skalierten Lava-Spire; Gefahr „Mauer wie Bauwerk“ → Front in
Lappen und Rinnen brechen, nie gerade.
Budget (Richtwert): ~7 000 Instanzen (900 Kollision), 30 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

### lava_02_schwefelgrund – Schwefelgrund (Leuchtfeuer)

**Was man sieht:** Am Fuß des Vulkans liegt eine flache Mulde, in der der Boden ocker, schwefelgelb und gebleicht ist. Aus zwei
Rissen (NO–SW, parallel zur Kraterreihe) zischen 6–9 Fumarolen; ein 3 m hoher, gelb verkrusteter **Dampfschlot** schickt eine
weiße Säule 20–30 m hoch. Zwei milchig-türkise **Schwefelquellen** dampfen in kleinen Becken mit gelbem Rand. Um die Mulde ein
toter Saum: gebleichte Halme, kein Moos.
**Vorbild:** Hverir/Námaskarð am Fuß des Námafjall (Island), Solfatara (Pozzuoli); Spiel: Fumarolen und Schwefelquellen in
Eastmarch (Skyrim), Farbigkeit wie DA:I.
**Standort:** C6, X −2394 / Y 1276 m, Boden 49,7 m. Nordfuß des Vulkans, flache Hangmulde (TPI100 −2,55 m, Hang 15°), Moos 51 %,
Wiese 24 %, Lavafels-Rippen 24 %. Weg 393 m (WARNUNG, Zone ≤ 400 m; weiter nach Norden ginge nur auf Kosten von lava_01/05),
Archiv 334 m, Wasser 573 m (Quellen bekommen eigenes Becken).
**Sicht:** 22 von 22 Wegpunkten im Ring sehen ≥ 30 % der 25-m-Dampfsäule, mittlerer Anteil 0,64, bis 798 m; `_fern` vom Weg
unter Zalas Stadt (X −2496 / Y 490, 793 m).
**Komposition und Anmarsch:** Vom Archivpfad steht die Dampfsäule vor der dunklen Vulkanflanke – das zieht. Zugang 405 m ohne
Pfadbau (max. 19,8°). `_held` 70 m südlich hangauf, Blick nach Norden über das gelbe Feld, Dampf vor der grünen Mooslava-Ebene.
**Detail-Ebenen:** Held – Dampfschlot (Hügel +2,8 m mit Krater, Krone aus `SM_lava_b_rock_04` + `SM_lava_m_rock_05` mit
`MI_EL_SW_Schwefelkruste`). Begleiter 6–9 – Fumarolen-Mündungen aus `SM_lava_m_rock_01/02/07` als Steinringe, zwei Quellbecken.
Schutt 60–100 – gebleichte, verkrustete `SM_lava_s_rock_01…05` an den Rissen. Kleinzeug – `SM_SmallStonesPack_*`,
`SM_dead_grass_01…03`. Bewuchs nach Ursache – im Kern nichts (Hitze, Säure), Ring tote Halme, außen Moos/Wiese wie heute.
Kontaktzone – Decals Schwefel gelb (`MI_EL_SW_Schwefel_Decal`), Ocker/Weiß, Nassränder `MI_Leakage_*` an den Quellen.
**Wasser:** 2 `see` (Quelltöpfe), `farbe` thermal, Ø 7 m und 10 m, 0,6 m tief, Ufer mit Kiesring und gelbem Rand.
**Effekte, Licht:** Niagara Dampfsäule + 6–9 kleine Fahnen (optional, Lava & Volcano Set / Niagara Examples), `lokaler_nebel` 2× in
der Mulde (Dichte 0,08, weiß-gelblich). Keine Glut. Dampf trägt auch bei fester Sonne.
**Geländeänderung:** Mulde −1,6 m (42 × 30 m, Rand weich), Schlothügel +2,8 m; Lagen Lehm, Erde, Kies. Fenster 150 × 150 m.
Keine abflusslose Senke: die tiefste Stelle füllt das Quellbecken.
**Assets:** Bestand wie oben; Pakete Lava & Volcano (A, schon gekauft – Dampf/Rauch-Niagara), Niagara Examples (A),
Fantasy Ambiences (B, Zischen). Ersatz ohne Download: 2 Nebelvolumen + Decals.
**Aufwand und Risiko:** mittel. Risiko: ohne Niagara fehlt die Fernwirkung (dann kein echtes Leuchtfeuer) → Download A nötig.
Budget: ~4 000 Instanzen (300 Kollision), 20 Akteure, 0 Lichter, 3 Niagara, 2 Nebel, 10 Decals.

### lava_03_kraterkinder – Die Kraterkinder (Leuchtfeuer)

**Was man sieht:** In einer schwarzen Aschensenke am Rand der grünen Aue sitzen fünf kleine, runde Kegel wie Kinder um ein Feuer,
3,5–7,5 m hoch, jeder mit einem Krater oben; in den zwei größten steht schwarzes, spiegelndes Wasser. Ihre Flanken sind von Moos
und Gras überwachsen, die Kraterränder schwarz-rot. Aus dem großen Kraterteich sickert ein Rinnsal nach Norden zum Bach.
**Vorbild:** Pseudokrater von Skútustaðir am Mývatn (Lava floss über nassen Grund, Dampfexplosionen); Spiel: Hellblade II
(isländische Kraterlandschaften).
**Standort:** C5, X −2140 / Y 690 m, Boden 18,2 m. Geschlossene Lavasand-Senke (Lavasand 97 %, Senkentiefe 3,9 m, Einzugsfläche
0,36 km²), Ränder 22–26 m, Boden 16–18 m; Bach der Aue 130 m nördlich – genau die Lage, in der Pseudokrater entstehen (Lava auf
nassem Grund). Weg 291 m (Weg bei „Labor drei“), Zalas Stadt 210 m, Biominneres 40 m.
**Sicht:** 26 von 130 Wegpunkten im Ring sehen ≥ 30 % der Kegelgruppe (Zielhöhe 8 m), bis 772 m; bester Blick vom Pfad unter Zalas
Stadt (375 m, Anteil 0,8). Ein bescheidenes Leuchtfeuer: Hügelgruppe mit Dellen am Horizont, nicht hoch.
**Komposition und Anmarsch:** Zugang 293 m ohne Pfadbau (max. 14,6°). `_held` vom Südrand der Senke (Augenhöhe), Blick nach Norden:
Kegel im Mittelgrund, Kraterteich spiegelt, dahinter das Grün der Aue und der Bach.
**Detail-Ebenen:** Held – größter Kegel mit Teich (Ø 34 m). Begleiter 4 – weitere Kegel (Stempel). Schutt 80–150 – Schlacke am
Kraterrand `SM_lava_m_rock_02/07`, `SM_lava_s_rock_03…08`, Schweißschlacken `SM_lava_wall_06/07/08`. Kleinzeug –
`SM_SmallStonesPack_*`, `SM_stone_05…07`. Bewuchs nach Ursache – Flanken grün (älter, feucht): `SM_wk2oaeyqx_VarA…I`,
`SM_grey_willow_01…04` (Kriechweiden) an den Teichen, `SM_Rohrkolben_Horst_1…6` sparsam am Teichrand, Moos `SM_MossClump_*`;
Kraterränder kahl (Wind). Kontaktzone – Nassband am Teich (`MI_Leakage_*`), Kiesring.
**Wasser:** 2 `see` in den Kratern (`schwarz_spiegel`, Ø 12 m, 1,5 m tief), 1 `bach` als Überlauf (Breite 0,6 m, `muendung` =
Aue-Bach nördlich, Gefälle stetig).
**Effekte, Licht:** `lokaler_nebel` 1× dünn über den Teichen (Dichte 0,03). Keine Glut.
**Geländeänderung:** 5 Kegelstempel (+3,5 … +7,5 m, Krater −2 … −5 m), Fenster ca. 200 × 180 m, Δ max 7,5 m; Krater mit Wasser
gefüllt (keine trockenen geschlossenen Senken: die drei kleinen Krater flach, 2 m, mit Moosboden und Rinne).
**Assets:** Bestand wie oben; Coast & Dunes Decals (B, Nassband), Icelandic Sand With Pebbles (C), Tundra Icelandic Rock Cluster (C).
**Aufwand und Risiko:** mittel. Risiko: Nähe zu Zalas Stadt (210 m) – Silhouetten der Ruinen dürfen nicht ins `_held`-Bild.
Budget: ~6 000 Instanzen (400 Kollision), 10 Akteure, 0 Lichter, 0 Niagara, 1 Nebel, 4 Decals.

### lava_04_roehrenfenster – Das Röhrenfenster (Fundstück)

**Was man sieht:** Auf dem Moosplateau liegt ein Druckrücken; wer darüber geht, steht plötzlich an einem 26 × 16 m großen,
8 m tiefen Loch. Die Decke einer Lavaröhre ist eingestürzt: an beiden Enden öffnen sich schwarze Röhrenmäuler unter überhängenden
Lavaplatten, am Grund liegt Bruchschutt, über dem eine kleine **Farnoase** wächst – kühl, feucht, grün im schwarzen Stein. Ein
Lichtschacht fällt schräg hinein. Zwei kleine Einsenkungen im Moos zeigen, wohin die Röhre läuft.
**Vorbild:** Einbruchsfenster von Raufarhólshellir und Lofthellir (Island), Thurston Lava Tube (Hawaii); Spiel: Höhleneingänge
Skelliges (Witcher 3) im Licht-/Farnspiel.
**Standort:** C5, X −1792 / Y 780 m, Boden 36,8 m. Rand des Moos-Lavaplateaus über der Wiese (Stromrand 35–37 m, Hang 10–22°,
TPI100 +3,2 m) – Röhren laufen hangab zum Stromrand (nach NO). Wiese 45 %, Moos 37 %. Weg 286 m, Wasser 175 m.
**Verdeckung:** heute (flach, Silhouette 1 m) sieht man den Ort von 6 der 20 Wegpunkte ≤ 400 m – deshalb Druckrücken +3,5 m
zwischen Weg und Fenster. Mit Stempel: **Einblick in die Grube 0 %**, auch ein 1-m-Objekt am wegseitigen Rand 0 % (0 von 20
Wegpunkten). Man findet das Fenster erst auf dem Rücken.
**Komposition und Anmarsch:** Zugang 335 m vom Weg bei „Labor drei“ (max. 13,8°). `_anmarsch` auf dem Zugang, Augenhöhe.
`_held` auf dem Druckrücken (24 m), Blick nach Süden hinab: Farnoase im Lichtschacht, Röhrenmaul als dunkles Blickziel.
**Detail-Ebenen:** Held – Grube + Deckenlippen `SM_lava_wall_01/02/09` kopfüber als Akteure (Überhang ist Netz, kein Gelände).
Begleiter 4–6 – große Deckenbrocken `SM_lava_b_rock_01…04` am Grund. Schutt 60–120 – `SM_lava_m_rock_*` als Bruchkegel unter den
Rändern. Kleinzeug – `SM_lava_s_rock_06…08`, `SM_SmallStonesPack_*`. Bewuchs nach Ursache – Farne nur im kühlen Schacht
(`SM_EagleFern_M_01`, `SM_EagleFern_S_01/02/04`, `SM_foliage_fern_01_1…4`, `SM_Fern_01a/02a`), Moospolster an der schattigen
Nordwand (`SM_moss_01/02`, `SM_MossClump_*`), oben Moos und Wiese wie heute. Kontaktzone – Tropfspuren `MI_Leakage_01…13` an den
Wänden, Moos kriecht über die Kante.
**Wasser, Effekte, Licht:** kein offenes Wasser (Abfluss in die Röhre). `lokaler_nebel` 1× im Schacht (Kaltluft, 0,05).
Keine Lichter – das Dunkel der Röhrenmäuler ist gewollt.
**Geländeänderung:** Grube −8 m (Ellipse 26 × 16 m), Druckrücken +3,5 m, 2 Einsenkungen −1,5/−2 m. Fenster ca. 90 × 90 m.
Die Grube ist eine geschlossene Senke ohne Wasser – begründet: sie entwässert sichtbar in die beiden Röhrenmäuler.
**Assets:** Bestand wie oben; Cave Ambience (B, Tropfen/Hall), Niagara Examples (A, Mist Card); Lücke Lavaröhre ohne Asset.
**Aufwand und Risiko:** mittel–hoch. Risiko: Fugen zwischen Gelände und Deckenlippen → Lippen tief einbinden, Moos-Decal über die
Naht.
Budget: ~3 500 Instanzen (500 Kollision), 25 Akteure, 0 Lichter, 1 Niagara (optional), 1 Nebel, 8 Decals.

### lava_05_klare_spalte – Die Klare Spalte (Fundstück)

**Was man sieht:** Mitten in der Mooslava klafft eine 110 m lange, 4–9 m breite Spalte. 5 m unter der Kante steht Wasser so klar,
dass man 6 m tiefer jeden Block am Grund sieht – türkis in der Mitte, fast schwarz in den Klüften. Die Wände sind senkrecht
geklüfteter Basalt, mit Moos auf jeder Leiste. Über der Engstelle klemmt ein Felsblock; an der Kante steht eine windschiefe Birke.
**Vorbild:** Silfra und Almannagjá (Þingvellir), Grjótagjá; Spiel: Hellblade II.
**Standort:** C6, X −2604 / Y 982 m, Boden 29,6 m. Moos-Lavaebene im Westen (Moos 55 %, Wiese 23 %, Lavafels 17 %, Hang 12°),
Spalte NO–SW (Azimut 40°) parallel zur Eruptionsspalte der Kraterreihe – dieselbe Dehnungsrichtung. Weg 242 m, Zalas Stadt 151 m
(Mitte; die Spalte endet nach SW), Biominneres 46 m.
**Verdeckung:** heute (Silhouette 1 m) max. Anteil 0,36 von 4 der 15 Wegpunkte ≤ 400 m. Die Spalte liegt unter Flur: **Einblick
0,4 %** (max. Anteil 0,004). Die Kante selbst ist offene Moosfläche – auf der Wegseite (NO) deshalb nichts über 0,5 m setzen;
Moos-Tumulus +2,4 m am NO-Ende als Rahmen.
**Komposition und Anmarsch:** Zugang 252 m ohne Pfadbau (max. 14,6°). `_held` am NO-Ende auf dem Tumulus, Blick nach SW die Spalte
entlang (Fluchtpunkt, Wasser leuchtet, Birke als Rahmen). Abstieg über eine Schuttrampe an der Engstelle zum Wasser.
**Detail-Ebenen:** Held – Spalte (Stempel) mit Wänden aus `SM_lava_wall_04/05` senkrecht gereiht (`MI_EL_SW_Basalt_Saeule` nur
als Klufttönung). Begleiter 3–5 – Klemmblock `SM_lava_b_rock_02`, Bruchblöcke `SM_lava_b_rock_01/03` im Wasser (sichtbarer Grund).
Schutt 80–150 – `SM_lava_m_rock_*` an den Wandfüßen und als Rampe. Kleinzeug – `SM_lava_s_rock_06…08` am Ufer. Bewuchs nach
Ursache – Moos auf Leisten (Feuchte), Farne in schattigen Klüften (`SM_foliage_fern_01_*`), eine Windbirke `Big_Tree_Birch_01`
× 0,45 an der Kante (Windflüchter), Kriechweiden `SM_grey_willow_01…04`. Kontaktzone – Nassband an der Wasserlinie (Coast & Dunes
Decals / `MI_Leakage_*`), Moos kriecht über die Kante.
**Wasser:** `see` in der Spalte (`tuerkis`, Spiegel 5 m unter Flur, 6 m tief, Umriss gegen den Uhrzeigersinn), Grundwasser ohne
Zufluss – klar, kein Schaum.
**Effekte, Licht:** keine. Lichtspiel über das Wasser (Kaustik im Wassermaterial, falls vorhanden).
**Geländeänderung:** Rinne −11 m (Breite 6 m, Rand 2,5 m) über 110 m, Tumulus +2,4 m. Fenster ca. 160 × 120 m.
**Assets:** Bestand wie oben; Coast & Dunes Decals (B); Wunsch Tundra Icelandic Rock Cluster (C). Basalt Columns (A) optional für
die Wände.
**Aufwand und Risiko:** hoch. Risiko: Gelände kann keine senkrechten Wände – Wände sind Netze, Fugen zum Gelände sorgfältig decken;
Wasser in schmaler Rinne braucht saubere Ufer-Netze.
Budget: ~5 000 Instanzen (900 Kollision), 45 Akteure, 0 Lichter, 0 Niagara, 0 Nebel, 8 Decals.

### lava_06_kraterreihe – Die Kraterreihe (Leuchtfeuer, nur mit Kratersteig)

**Was man sieht:** Am Nordostfuß des Vulkans stehen vier Schlackenkegel auf einer schnurgeraden Spalte, wie Perlen auf einer Schnur.
Der größte, ein nach Südwesten offener Hufeisenkegel, ragt 27 m auf; sein Krater ist 16 m tief, innen rostrot, außen schwarz.
Aus dem Kraterboden steigt ein Hauch Restdampf. Zwischen den Kegeln Schweißschlacke und ein Fächer roter Schlacke.
**Vorbild:** Lakagígar (Laki-Spalte), Eldgjá; Spiel: Mt. Gelmir (Elden Ring).
**Standort:** C6, X −1790 / Y 1345 m, Boden 58,6 m. Vorhandene Kegelkette (alte Kachel, im Gelände enthalten): Kraterböden bei
(−1698/1240) 36 m, (−1762/1322) 52 m, (−1804/1340) 56 m, (−1844/1430) 66 m; Hauptkegel-Rand 82 m. Richtung NO–SW (37°).
Heute 737 m vom Weg; zum Kratersteig (Ast Ost) 148 m.
**Sicht (mit Steig):** 27 von 69 Wegpunkten im Ring sehen ≥ 30 % (Zielhöhe 18 m), bis 593 m; `_fern` vom Steig (412 m).
**Komposition und Anmarsch:** Zugang 160 m vom Steigende (max. 14,2°). `_held` am Steigende, Augenhöhe, Blick nach Südosten:
rechts der Hauptkegel (170 m), nach links staffeln sich die kleineren Kegel bis 240 m. `_nah` am Kraterrand des Hauptkegels.
**Detail-Ebenen:** Held – Hauptkegel (Gelände, Rand schärfen). Begleiter 3 – kleinere Kegel. Schutt 150–250 – Schlacke
`SM_lava_m_rock_*`, `SM_lava_s_rock_*`, rote Schlacke mit `MI_EL_SW_Schlacke_Rot`, Spatterfladen `SM_lava_wall_06/07/08`.
Kleinzeug – Lapilli als Lage Lavasand + `SM_SmallStonesPack_*`. Bewuchs nach Ursache – auf dem jungen Kegel fast nichts; Moos nur
an der Nordseite des ältesten (NO-)Kegels, einzelne `SM_wk2oaeyqx_*` in Windschatten. Kontaktzone – Schlacke 40 % eingegraben.
**Wasser, Effekte, Licht:** Restdampf (Lava & Volcano Niagara, optional) + `lokaler_nebel` klein im Krater. Keine Glut.
**Geländeänderung:** Kraterrand +2 m / Krater −2 m schärfen, Lage Lavasand rotbraun über Material. Fenster ca. 300 × 300 m
(Kette 300 m lang).
**Assets:** Bestand; Lava & Volcano (A), Fantasy Ambiences (B).
**Aufwand und Risiko:** niedrig–mittel (Form ist schon da). Risiko: alte Kachel-Optik („Houdini-Kegel“) muss durch Material/Schlacke
natürlich werden – Bildwunsch.
Budget: ~8 000 Instanzen (600 Kollision), 15 Akteure, 0 Lichter, 1 Niagara, 1 Nebel, 4 Decals.

### lava_07_basaltorgel – Die Basaltorgel (Fundstück, nur mit Kratersteig)

**Was man sieht:** Vom Plateau aus nichts. Wer am Rand hinabsteigt, steht in einer kleinen Schlucht vor einer 16–20 m hohen,
leicht gebogenen Wand aus **sechseckigen Basaltsäulen** – oben gefächert wie Orgelpfeifen, unten senkrecht. Am Fuß liegen
abgebrochene Säulenstücke wie gestapelte Stämme; Moos besetzt die Stufen, Sickerwasser zeichnet dunkle Streifen.
**Vorbild:** Gerðuberg und Svartifoss (Island), Stuðlagil; Spiel: Säulenbasalt in Skellige (Witcher 3).
**Standort:** B6, X −2795 / Y 1390 m, Boden 42,3 m. Schlucht zwischen Aschenplateau (55–58 m) und Westhügel (80–95 m): Talboden
40–44 m, Plateaukante 10–14 m bei 30–35°, TPI100 −10,5 m. Biominneres 59 m. Heute 661 m vom Weg; zum Kratersteig (Ast West) 107 m.
**Verdeckung (mit Steig):** heute und mit Stempel **verdeckt**: 0 von 38 Wegpunkten ≤ 400 m sehen die Wand (max. Anteil 0,0) –
sie liegt unter der Plateaukante.
**Komposition und Anmarsch:** Zugang 116 m (max. 24,5°) – über die Kante als kleiner Pfad mit Trittstufen im Schutt (Rampe von
Norden). `_held` auf dem Schluchtboden, Augenhöhe, Blick nach Osten auf die Wand; `_nah` 10 m vor den Säulenfüßen.
**Detail-Ebenen:** Held – Säulenwand (Basalt Columns, 21 Typen) auf 90 m Länge. Begleiter 6–10 – Säulengruppen, gekippte Säulen.
Schutt 100–200 – Säulenstücke in der Halde (Ursache: Frostsprengung). Kleinzeug – `SM_lava_s_rock_06…08`, `SM_stone_05…07`.
Bewuchs – Moospolster auf Stufen und Halde (Nordwand schattig), Farne in Fugen, Gras am Schluchtboden. Kontaktzone –
Sickerstreifen `MI_Leakage_*`, Moos am Wandfuß (`M_EL_Klippe_RVT` Fußblend, `MI_EL_SW_Basalt_Saeule`).
**Wasser, Effekte, Licht:** nur Sickerwasser (Decals). Schlucht im Halbschatten – Säulenkanten fangen Streiflicht.
**Geländeänderung:** Kante +4 m (Band 8 m) → Wand 16–20 m; Fenster ca. 150 × 150 m.
**Assets:** Basalt Columns and Rocks 21 Types – AssetKit PBR (A, ca. 11 €, Ferat entscheidet). Ersatz `SM_lava_wall_04/05`
senkrecht + `SM_IcelandicLavaSpire_01/03` – ohne echte Sechsecke deutlich schwächer.
**Aufwand und Risiko:** mittel mit Paket, hoch ohne. Risiko: Säulen-Paket ohne belegtes Nanite.
Budget: ~4 000 Instanzen (800 Kollision), 70 Akteure, 0 Lichter, 0 Niagara, 0 Nebel, 6 Decals.

### lava_08_glutauge – Das Glutauge (Fundstück, nur mit Kratersteig)

**Was man sieht:** Auf dem jungen, schwarz glänzenden Strom des Westplateaus – Stricklava mit Seilen, Zehen und aufgewölbten
Schollen – liegt zwischen zwei Buckeln ein 8 × 6 m großes Loch. 6 m tief darunter fließt dumpf orange **Glut** vorbei, die Luft
darüber flimmert, ein dünner Dampf zieht. In Haarrissen ringsum glimmt es kaum sichtbar. Kein Halm wächst hier.
**Vorbild:** Skylights am Kīlauea (Puʻu ʻŌʻō-Röhren), Fagradalsfjall 2021; Spiel: Muspelheim (God of War) – aber dezent.
**Standort:** B6, X −2745 / Y 1740 m, Boden 64,8 m. Junger Lavastrom (Lavafels 73 %) auf dem flachen Abschnitt des Westplateaus
(Hang 9°, Relief 10,5 m), der Strom reicht weiter bis zur Westküste. Heute 936 m vom Weg; zum Kratersteig 118 m.
**Verdeckung (mit Steig):** **Einblick 0 %** (0 von 18 Wegpunkten ≤ 400 m sehen in den Schacht); die Kante ist offene Lava – dort
nichts über 0,5 m. Die Glut sieht man nur vom Rand.
**Komposition und Anmarsch:** Zugang 126 m (max. 6,8°). `_held` auf dem nordöstlichen Buckel (+1,8 m), Blick schräg in den Schacht;
`_nah` 7 m.
**Detail-Ebenen:** Held – Schacht mit Glut (Lava-Material, Lava & Volcano). Begleiter 2 – Tumuli (Buckel) mit Rissen.
Schutt 40–80 – Krustenplatten `SM_lava_wall_06/07/08` liegend mit `MI_EL_SW_Lava_Glasur`. Kleinzeug – `SM_lava_s_rock_06…08`.
Bewuchs – keiner (zu jung, zu heiß); Kontrast zu 04. Kontaktzone – Glut-Decals (Lava-Set, 3–4 Stück) in Rissen, Rußdecal am Rand.
**Wasser, Effekte, Licht:** 1 `punktlicht` orange [1,0; 0,45; 0,15], 800 cd, Radius 600 cm, kein Schatten, im Schacht; Niagara
Hitzeflimmern + Funken (optional, Lava-Set / Ultimate Niagara). Wirkung im Schatten des Schachts auch bei fester Sonne.
**Geländeänderung:** Schacht −6 m (8 × 6 m), 2 Tumuli +1,4/+1,8 m. Fenster ca. 90 × 90 m.
**Assets:** Lava & Volcano (A, Material + Decals), Ultimate Niagara Environmental VFX (B), Fantasy Ambiences (B).
**Aufwand und Risiko:** mittel. Risiko: Glut zu stark → Kitsch; Intensität klein halten, Bild mit fester Sonne prüfen.
Budget: ~2 500 Instanzen (300 Kollision), 20 Akteure, 1 Licht, 2 Niagara, 0 Nebel, 6 Decals.

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/gletscher/katalog.md](sehens/gletscher/katalog.md)

### 1 · Das Gletschertor (`gletscher_01_gletschertor`) – Leuchtfeuer

**Was man sieht.** Die Zunge des Kargletschers bricht über eine Felsstufe: ein 120 m breiter Séracbruch aus blauen, schiefen Eistürmen (8–15 m), dazwischen Spalten, in denen das Licht türkis wird. An ihrem Fuß, links hinter der Stirnmoräne, öffnet sich das Gletschertor – ein 9 m hohes, gewölbtes Portal aus geschichtetem, schmutzig-blauem Eis, aus dem der milchige Gletscherbach tritt. Wer hineingeht, steht 15 m tief in einer Eishöhle mit gewellter Decke (Ablationsnäpfe) und Steinen, die im Eis stecken.

**Vorbild.** Real: Gletschertor des Morteratsch und des Rhonegletschers, Eishöhlen des Breiðamerkurjökull (Vatnajökull), Séracs des Glacier des Bossons. Spiel: der Gletscher über Kaer Morhen/Skellige (Witcher 3), die blauen Eiswände in Skyrim (Höhlen des Schlangenzahns).

**Standort.** Feld E2, X −620 / Y −2845, Boden 218,8 m. Offener Hang; Boden Eis 89 %, Fels 5 %, Erde 4 %, Schnee 1 %; Hang 31° (max 70°), Exposition 197°, TPI25 0,7 m, TPI100 5,7 m, Relief 100 m im Radius. Weg 257 m (Punkt −646/−2588); Wasser 195 m, Meer 570 m, Stadtrand 156 m (EXP_003); 472 m innerhalb des Bioms; 0 Baumzellen im Radius (max 0 m); Einzugsfläche max 31824 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 22 m: 20 von 97 Wegpunkten im Ring 300–800 m (Wege) sehen ≥ 30 %, Mittel 0,17, lesbar bis 796 m; bester Punkt −658/−2430 in 417 m mit Anteil 1,00.

**Komposition und Anmarsch.** Blickziel ist das dunkle Portal unter der leuchtend blauen Séracwand. Vordergrund: Sanderfläche mit Gletscherbach und Kiesbänken, Mitte: Stirnmoräne mit Toteisbuckeln, Hintergrund: Séracbruch und die Karwand mit der Wächte (gletscher_05) als zweite Silhouette. Der Spieler sieht die Séracs schon von der Serpentine; das Portal zeigt sich erst, wenn er auf der Sanderfläche links um die Moräne geht. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 259 m (X −645 / Y −2587), `_held` 240 m (X −760 / Y −2650), `_nah` 10 m (X −626 / Y −2837), `_fern` 417 m (X −658 / Y −2430). **Zugang (kandidaten.erreichbarkeit, 4 m):** 393 m vom Weg (Luftlinie 259 m), max 31,1°, Mittel 10,8°, 4 m steiler als 25°, 30 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Séracwand aus 6–10 großen Eisnetzen (Wunsch Megascans Ice Cliff, bis dahin `SM_EISZAPFEN_9` gruppiert + Geländestufe mit Lage Eis und Material `M_EL_Eis4`) und das Portal als Gewölbe aus 3–4 Eisschalen. Begleiter (5–7): `SM_NordicBoulder_01` und `SM_TundraMossyBoulder_01` als Gletscherfracht vor dem Tor, halb im Eis/Kies. Schutt (150–200): Moränenschutt `SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_01/02`, `SM_mountain_rock_big_01_1…5`, nach außen feiner (Sortierung). Kleinzeug: `SM_SmallStonesPack_01…14`, `SM_NordicBeachRock_01`, Eisbrocken `SM_EISZAPFEN_1/5` liegend als Kalbungsreste. Bewuchs nach Ursache: fast keiner – erst 80 m vor der Stirn Pioniere (`SM_wk2oaeyqx_VarA…I`, `SM_heath_B_01`), das zeigt das junge Gletschervorfeld. Kontaktzone: Eis endet nie scharf – Schmutzband aus Kies auf dem Eis (Lage Kies/Geroell über Eis gemischt), Schmelzwasserrinnen, nasser dunkler Kies am Fuß (`MI_Leakage_03`).

**Wasser, Effekte, Licht.** Gletscherbach (`bach`, farbe `gletschermilch`, quelle true) aus dem Portal, 2–4 m breit, auf der Sanderfläche verzweigt, mündet in den vorhandenen F_GLETSCHERTAL. Kalter Nebel im Portal (`lokaler_nebel`, Dichte 0,08, bläulich), ein schwaches blaues Punktlicht (0,4/0,7/1,0; 800 cd) im Höhlenende, damit die Tiefe auch bei fester Sonne leuchtet. Niagara optional: Tropfwasser am Portal.

**Geländeänderung.** Stempel 220 × 160 m: Felsstufe unter den Séracs um 6–8 m versteilen (Eisbruch), Portalnische 4 m tief, Sander 0,5–1 m eingeebnet mit 2–3 flachen Rinnen. Lagen: Eis (Zunge), Kies/Geroell (Sander, Moräne), Schnee nur in Mulden.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_9`, `SM_NordicBoulder_01`, `SM_TundraMossyBoulder_01`, `SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_01`, `SM_NordicBeachRockyGround_02`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_NordicBeachRock_01`, `SM_EISZAPFEN_1`, `SM_EISZAPFEN_5`, `SM_wk2oaeyqx_VarA`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarC`, `SM_wk2oaeyqx_VarD`, `SM_wk2oaeyqx_VarE`, `SM_wk2oaeyqx_VarF`, `SM_wk2oaeyqx_VarG`, `SM_wk2oaeyqx_VarH`, `SM_wk2oaeyqx_VarI`, `SM_heath_B_01`; Decals: `MI_Leakage_03`; Material: `M_EL_Eis4`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Séracwand und Portal aus echtem Eis (Ice Cliff), Kalbungsbrocken (Rocky Snow Pile), Ersatz: SM_EISZAPFEN_8/9 gebündelt + Geländestufe, Material M_EL_Eis4; **Arctic Cliffs** (B) – große Eisplatten/Eisstücke für die Séracs, Ersatz: wie oben; **Niagara Examples Pack** (B) – kalter Nebel im Portal, Tropfwasser, Ersatz: lokaler_nebel ohne Niagara; **Cave Ambience** (C) – Klang in der Eishöhle, Ersatz: kein Klang; **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (C) – Gletscherbach-Schaum am Portal, Ersatz: MI_EL_Wasserfall_Aufprall.

**Aufwand und Risiko.** Hoch (Eisnetze sind die Lücke des Bestands). Risiko: ohne Megascans-Eis wirkt die Séracwand aus Eiszapfen künstlich – deshalb Paket A. Das Portal muss begehbar sein (Kollision) und darf nicht mit der Stadtzone (150 m) kollidieren: Mitte 156 m vom Rand des Frostlagers.

### 2 · Der Lawinenkegel (`gletscher_02_lawinenkegel`) – Leuchtfeuer

**Was man sieht.** Aus einer engen Rinne in der Westwand des Tals zieht ein schmutzig-weißer Kegel aus Altschnee 90 m weit in den Wald: der Lawinenkegel. Im Sommer ist er grau gebändert, an seinem Fuß tropft er in kleine Schmelzrinnen. Rechts und links liegen Fichtenstämme wie Streichhölzer, alle in Fallrichtung, mit abgerissenen Kronen; oben in der Rinne hängt noch Schnee. Ein Ort, der vom Wetter erzählt.

**Vorbild.** Real: Lawinenkegel im Lauterbrunnental und am Fuß des Eigers, Lawinenstriche in Kanada (Rogers Pass). Spiel: die Schneerinnen von Skellige (Witcher 3), Lawinenhänge in Red Dead Redemption 2 (Grizzlies).

**Standort.** Feld D2, X −920 / Y −2650, Boden 165,4 m. Offener Hang; Boden Heide 39 %, Trockengras 28 %, Schnee 14 %, Fels 13 %; Hang 39° (max 78°), Exposition 184°, TPI25 0,9 m, TPI100 8,2 m, Relief 102 m im Radius. Weg 279 m (Punkt −648/−2588); Wasser 155 m, Meer 608 m, Stadtrand 234 m (EXP_003); 230 m innerhalb des Bioms; 451 Baumzellen im Radius (max 28 m); Einzugsfläche max 53636 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 10 m: 32 von 151 Wegpunkten im Ring 300–800 m (Wege) sehen ≥ 30 %, Mittel 0,20, lesbar bis 746 m; bester Punkt −782/−2112 in 555 m mit Anteil 1,00.

**Komposition und Anmarsch.** Leuchtfeuer: Der weiße Fächer mit der dunklen Rinne darüber steht als helle Zunge im dunklen Waldhang – vom Weg zum Frostlager aus 330–750 m zu lesen. Held-Blick vom Kegelfuß hangauf: Bruchholz im Vordergrund, Kegel in der Mitte, die Rinne als Blickachse nach oben. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 330 m (X −639 / Y −2477), `_held` 25 m (X −920 / Y −2675), `_nah` 10 m (X −920 / Y −2660), `_fern` 555 m (X −782 / Y −2112). **Zugang (kandidaten.erreichbarkeit, 4 m):** 459 m vom Weg (Luftlinie 330 m), max 24,7°, Mittel 11,7°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Kegel als Geländeform (Stempel) mit Lage Schnee + Altschnee-Netze (Wunsch Megascans Snow Embankment/Huge Snow Hill; Ersatz Stempel + Lage Schnee und Schutt). Begleiter (6–8): umgeknickte Fichten `SM_FallenSpruceTree_01`, `SM_BrokenTreeAssembly_01`, `SM_Forest_pine_10_dead` schräg, Wurzelteller `SM_Pine_roots_01/03`. Schutt (80–150): Lawinenschutt im Schnee – `SM_mountain_rock_big_01_*`, `SM_ground_rock_01`, Äste `SM_Pine_broken_branch_01/02`, `SM_mountain_branch_01_01/02`. Kleinzeug: `SM_DryBranches_01…08`, Nadeln über Landschaftsgras. Bewuchs nach Ursache: Bahn frei von Bäumen, am Rand Jungwuchs `Fir_01_Plant`, `SM_Forest_pine_plant_01…03`, Weidengebüsch `SM_grey_willow_01…04` (typisch für Lawinenbahnen). Kontaktzone: Schnee schmutzig-gestreift (Decal `MI_ScatteredSticksAndTwigs_01`), Schmelzrand nass (`MI_Leakage_05`).

**Wasser, Effekte, Licht.** Drei dünne Schmelzrinnen am Kegelfuß (`bach`, farbe `klar`, quelle true, 0,5 m breit), versickern nach 40 m im Schutt.

**Geländeänderung.** Kegel +3…+6 m auf 90 × 60 m (Fächerform, Spitze in der Rinne), Rinne 2 m eingetieft. Lagen: Schnee (Kegel), Geroell (Rinnenboden), Laub/Nadeln am Rand.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_FallenSpruceTree_01`, `SM_BrokenTreeAssembly_01`, `SM_Forest_pine_10_dead`, `SM_Pine_roots_01`, `SM_Pine_roots_03`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_ground_rock_01`, `SM_Pine_broken_branch_01`, `SM_Pine_broken_branch_02`, `SM_mountain_branch_01_01`, `SM_mountain_branch_01_02`, `SM_DryBranches_01`, `SM_DryBranches_02`, `SM_DryBranches_03`, `SM_DryBranches_04`, `SM_DryBranches_05`, `SM_DryBranches_06`, `SM_DryBranches_07`, `SM_DryBranches_08`, `Fir_01_Plant`, `SM_Forest_pine_plant_01`, `SM_Forest_pine_plant_02`, `SM_Forest_pine_plant_03`, `SM_grey_willow_01`, `SM_grey_willow_02`, `SM_grey_willow_03`, `SM_grey_willow_04`; Decals: `MI_ScatteredSticksAndTwigs_01`, `MI_Leakage_05`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Altschnee-Kegel (Snow Embankment, Huge Snow Hill), Ersatz: Geländekegel + Lage Schnee; **Free City & Nature Sounds** (C) – Wind, Tropfen, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Risiko: ein weißer Kegel im Sommerwald kann wie ein Fehler aussehen – deshalb Schmutzbänder, Bruchholz und die sichtbare Rinne als Ursache.

### 3 · Der Moränensee (`gletscher_03_moraenensee`) – Fundstück · nur mit Steig `gletschersteig_west`

**Was man sieht.** In einem kleinen Hängetal unter dem Westgrat liegt ein milchig-türkiser See, nicht größer als ein Hof, hinter einem Riegel aus Moränenschutt. Der Gletscher, der ihn aufgeschüttet hat, ist längst weg; nur Firnflecken an der Rückwand speisen ihn. Am Ufer: Schliffplatten, Wollgras, ein einzelner von Flechten grüner Block.

**Vorbild.** Real: Moränenseen der Hohen Tauern, Lago di Sorapis (Farbe), Moränenstauseen im Himalaya (kleiner Maßstab). Spiel: die Gebirgsseen in Breath of the Wild (Hebra) und Witcher 3 (Skellige, Spikeroog).

**Standort.** Feld D2, X −1120 / Y −2950, Boden 190,6 m. Talboden (U-Tal); Boden Fels 75 %, Erde 13 %, Trockengras 12 %, Moos 1 %; Hang 56° (max 67°), Exposition 327°, TPI25 −2,1 m, TPI100 −20,1 m, Relief 165 m im Radius. Weg 595 m (Punkt −648/−2588), **mit Steig 172 m** (`gletschersteig_west`); Wasser 74 m, Meer 259 m, Stadtrand 537 m (EXP_003); 30 m innerhalb des Bioms; 0 Baumzellen im Radius (max 0 m); Einzugsfläche max 5188 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 12 von 316 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 455 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Man steigt vom Gletschersteig über den Moränenriegel – erst auf seiner Krone liegt der See mit der Felswand dahinter da. Held-Blick über den Riegel auf das Wasser mit gespiegelter Wand. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 73 m (X −1067 / Y −2901), `_held` 82 m (X −1106 / Y −3031), `_nah` 10 m (X −1118 / Y −2960). **Zugang (kandidaten.erreichbarkeit, 4 m):** 356 m vom Steig (Luftlinie 200 m), max 41,6°, Mittel 21,6°, 188 m steiler als 25°, 193 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: der See selbst (Farbe `gletschermilch`), Damm als Geländeform. Begleiter (4–6): `SM_LichenedForestBoulder_01`, `SM_TundraMossyBoulder_01`, `xf3odif_tier_0`, `xisgcic_tier_0` am Ufer, halb im Wasser. Schutt (100–150): Moränenriegel aus `SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_01/02`, `skjsL_tier_0`, `pkeeM_tier_0`. Kleinzeug: `SM_SmallStonesPack_*`, Kies am Ufer. Bewuchs: Moos und Seggen nur auf der wasserseitigen Dammseite (`SM_MossClump_01…05`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarF`), Zwergkiefer `SM_dwarf_pine_small_01` im Windschatten. Kontaktzone: helles Kalkband am Ufer (Wasserstand), Moos `MI_TileableMossPatches_02` an Blockfüßen.

**Wasser, Effekte, Licht.** `see` (Umriss ~45 × 30 m, gegen den Uhrzeigersinn, Spiegel = Damm − 1 m, Tiefe 4 m, farbe `gletschermilch`), Abfluss als dünner `bach` über den Damm Richtung Ostbucht. Morgennebel: `lokaler_nebel` 0,05 über dem Wasser.

**Geländeänderung.** Stempel 120 × 100 m: Becken −3…−5 m im U-Tal-Boden, Damm +3 m (Riegel) – Becken hat Abfluss (keine geschlossene Senke ohne Wasser). Lagen: Kies (Ufer), Moos, Fels.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_LichenedForestBoulder_01`, `SM_TundraMossyBoulder_01`, `xf3odif_tier_0`, `xisgcic_tier_0`, `SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_01`, `SM_NordicBeachRockyGround_02`, `skjsL_tier_0`, `pkeeM_tier_0`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_MossClump_01`, `SM_MossClump_02`, `SM_MossClump_03`, `SM_MossClump_04`, `SM_MossClump_05`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarF`, `SM_dwarf_pine_small_01`; Decals: `MI_TileableMossPatches_02`. Wunsch: **Megascans Icelandic Sand With Pebbles** (C) – Uferkies hell, Ersatz: SM_BeachSandWithPebbles_01/02; **Free City & Nature Sounds** (C) – Wind, Wasser, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Nur mit Gletschersteig West erreichbar (Zugang 356 m, davon 188 m steiler als 25 Grad: Felsstufen). Risiko: Hang 56 Grad am Punkt – Becken muss auf der Talsohle liegen, nicht in der Flanke (Stempel prüfen).

### 4 · Das Toteisloch (`gletscher_04_toteisloch`) – Fundstück

**Was man sieht.** Mitten im Heidehang östlich des Frostlagers ein runder Trichter, 6–7 m tief und 45 m breit, mit steilen, moosigen Wänden. Unten steht schwarzes, stilles Wasser, an seinem Rand ragen Birken schräg nach innen. Der Trichter ist das Abdruckloch eines Eisblocks, den der Gletscher hier liegen ließ und der unter dem Schutt geschmolzen ist.

**Vorbild.** Real: Sölle Mecklenburgs, Kettle Holes in Wisconsin und Island (Skaftafell). Spiel: die verborgenen Waldtümpel in Witcher 3 (Velen) – hier ohne Menschenspur.

**Standort.** Feld E2, X −270 / Y −2560, Boden 141,3 m. Schlucht/Kessel; Boden Heide 54 %, Schnee 19 %, Trockengras 15 %, Erde 7 %; Hang 3° (max 59°), Exposition 122°, TPI25 −9,9 m, TPI100 −23,5 m, Relief 43 m im Radius. Weg 239 m (Punkt −472/−2432); Wasser 238 m, Meer 727 m, Stadtrand 242 m (EXP_003); 122 m innerhalb des Bioms; 190 Baumzellen im Radius (max 24 m); Einzugsfläche max 46460 m². Geschlossene Senke 6,5 m tief. **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (50 Wegpunkte ≤ 400 m, max. Anteil 0,00).

**Komposition und Anmarsch.** Fundstück: Vom Weg aus ist der Trichter nicht zu sehen (Rand und Bäume verdecken ihn); er öffnet sich erst 25–30 m vor dem Rand. Held-Blick vom Südrand hinunter: schräge Birken rahmen den schwarzen Spiegel, im Wasser spiegelt sich der helle Himmel. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 29 m (X −288 / Y −2537), `_held` 25 m (X −286 / Y −2541), `_nah` 10 m (X −276 / Y −2552). **Zugang (kandidaten.erreichbarkeit, 4 m):** 345 m vom Weg (Luftlinie 246 m), max 29,2°, Mittel 9,5°, 6 m steiler als 25°, 6 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: der Kesselsee (Farbe `schwarz_spiegel`). Begleiter (5–8): schräge Birken `Big_Tree_Birch_01` (0,5–0,7×), ein Birkenstumpf `SM_BirchTreeStump_01`, ein ins Wasser gekippter Stamm `SM_Forest_pine_04_log`. Schutt (40–80): Blöcke vom Trichterrand `SM_MossyRocks_02`, `texndcpda_tier_0`, `xjijdiz_tier_0`. Kleinzeug: Laub/Nadeln in der Mulde, `SM_DryBranches_*`. Bewuchs nach Ursache: Feuchtering aus Moos und Schachtelhalm (`SM_MossClump_*`, `SM_rough_horsetail_01…03`) auf den unteren 2 m, oben Heide `SM_heath_A_01`, `SM_lingonberry_01/02`. Kontaktzone: Uferband aus Torfmoos (Lage Moos 255), Laub schwimmt in einer Ecke.

**Wasser, Effekte, Licht.** `see` kreisrund ~20 m, Spiegel 1,5 m unter dem tiefsten Randpunkt, Tiefe 3 m, farbe `schwarz_spiegel`. Nebel in der Senke (`lokaler_nebel` 0,06).

**Geländeänderung.** Senke ist schon da (Senkentiefe 6,5 m); Stempel nur 60 × 60 m: Wände auf 35–40 Grad versteilen, Boden 1 m glätten. Lagen: Moos, Erde, Laub.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `Big_Tree_Birch_01`, `SM_BirchTreeStump_01`, `SM_Forest_pine_04_log`, `SM_MossyRocks_02`, `texndcpda_tier_0`, `xjijdiz_tier_0`, `SM_DryBranches_01`, `SM_DryBranches_02`, `SM_DryBranches_03`, `SM_DryBranches_04`, `SM_DryBranches_05`, `SM_DryBranches_06`, `SM_DryBranches_07`, `SM_DryBranches_08`, `SM_MossClump_01`, `SM_MossClump_02`, `SM_MossClump_03`, `SM_MossClump_04`, `SM_MossClump_05`, `SM_rough_horsetail_01`, `SM_rough_horsetail_02`, `SM_rough_horsetail_03`, `SM_heath_A_01`, `SM_lingonberry_01`, `SM_lingonberry_02`. Wunsch: **Free City & Nature Sounds** (C) – Stille/Wind in der Senke, Ersatz: kein Klang.

**Aufwand und Risiko.** Niedrig – fast nur Bestand. Risiko: gering; Abstand zur Fliesstreppe der Tundra (tundra_04) 407 m.

### 5 · Die Wächte (`gletscher_05_die_waechte`) – Leuchtfeuer · nur mit Steig `gletschersteig_west`

**Was man sieht.** Auf dem Nordgrat des Kars hängt eine Schneewächte wie eine erstarrte Welle 6–8 m über den Abgrund, blau im Schatten, an der Kante von Wind gezahnt. Darunter, am Fuß der Karwand, klafft der Bergschrund zwischen Fels und Gletscher, und im flachen Firnbecken davor gurgelt eine Gletschermühle: ein Loch im Eis, in das ein Schmelzbach stürzt.

**Vorbild.** Real: Wächten am Säntis und an der Jungfrau, Bergschrund an der Eiger-Nordwand, Gletschermühlen auf dem Aletschgletscher. Spiel: Kammlinien von The Long Dark, die Gipfel von Skellige (Witcher 3).

**Standort.** Feld E1, X −610 / Y −3196, Boden 412,5 m. Kuppe/Gipfel; Boden Fels 77 %, Schnee 22 %, Eis 0 %, Erde 0 %; Hang 25° (max 77°), Exposition 333°, TPI25 8,7 m, TPI100 79,9 m, Relief 186 m im Radius. Weg 609 m (Punkt −646/−2588), **mit Steig 123 m** (`gletschersteig_west`); Wasser 166 m, Meer 241 m, Stadtrand 506 m (EXP_003); 241 m innerhalb des Bioms; 0 Baumzellen im Radius (max 0 m); Einzugsfläche max 1188 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 10 m: 55 von 195 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,14, lesbar bis 768 m; bester Punkt −824/−2974 in 308 m mit Anteil 0,74; von bestehenden Wegen allein: 14 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: Die weiße Kante liegt genau auf der Himmelslinie über dem Gletscher – von der Straße am Frostlager (750 m) lesbar. Held-Blick vom flachen Firnbecken (Kamera 140 m südlich auf dem Eis): Gletschermühle vorne, Bergschrund als dunkle Linie in der Mitte, Wächte oben. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 175 m (X −756 / Y −3099), `_held` 151 m (X −650 / Y −3050), `_nah` 10 m (X −613 / Y −3186), `_fern` 308 m (X −824 / Y −2974). **Zugang (kandidaten.erreichbarkeit, 4 m):** 224 m vom Steig (Luftlinie 210 m), max 24,0°, Mittel 8,5°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Wächte aus gestreckten Schneenetzen (Wunsch Megascans Snow Embankment, gekippt; Ersatz Geländegrat + Lage Schnee + `SM_EISZAPFEN_6/9` an der Unterseite). Begleiter (4–5): Felsköpfe am Grat `SM_NordicBoulder_01`, `rcygn_tier_0` mit Schneekappe (`M_EL_Fels_Auflage`, Auflage_Farbe weiß). Schutt (60–100): Wächtenbruch – Schneeblöcke und Eisbrocken im Becken unter der Wand (`SM_EISZAPFEN_1…5` liegend, Megascans Rocky Snow Pile). Kleinzeug: Steinschlag auf dem Firn (`SM_SmallStonesPack_*`, `SM_NordicBeachRock_01`). Bewuchs: keiner – nur Flechten (Lage Fels mit Moos 10 %). Kontaktzone: Bergschrund als 2–3 m breite Rinne mit Eis-Kante, Firn wellig (Lage Schnee über Eis).

**Wasser, Effekte, Licht.** Gletschermühle: kurzer `bach` (supraglazial, farbe `tuerkis`, 1 m) endet `versickert` in einem runden Schacht (Netz-Ring aus Eis); Wasserfall-Material `MI_EL_Wasserfall_Kaskade` 3 m in den Schacht. Effekt optional: Schneefahne an der Wächte (Niagara-Wunsch).

**Geländeänderung.** Grat: Wächtenwulst +2…+4 m auf 140 × 20 m, Bergschrund −3 m; Firnbecken flach. Lagen: Schnee (Grat), Eis (Becken), Fels.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_6`, `SM_EISZAPFEN_9`, `SM_NordicBoulder_01`, `rcygn_tier_0`, `SM_EISZAPFEN_1`, `SM_EISZAPFEN_2`, `SM_EISZAPFEN_3`, `SM_EISZAPFEN_4`, `SM_EISZAPFEN_5`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_NordicBeachRock_01`; Material: `M_EL_Fels_Auflage`, `MI_EL_Wasserfall_Kaskade`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Wächte (Snow Embankment gekippt), Wächtenbruch (Rocky Snow Pile), Ersatz: Geländewulst + Lage Schnee + SM_EISZAPFEN_6/9; **Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam** (B) – Schneefahne an der Wächte, Ersatz: ohne Effekt; **Fantasy Ambiences (Lava, Höhle, Wind …)** (C) – Wind am Grat, Ersatz: kein Klang.

**Aufwand und Risiko.** Hoch (Gratlage, Steig 1,6 km). Risiko: Wächte braucht ein überhängendes Netz (Gelände kann keine Überhänge) – ohne Megascans-Schnee Ersatz nur als Wulst.

### 6 · Die Gletschertöpfe (`gletscher_06_gletschertoepfe`) – Fundstück · nur mit Steig `gletschersteig_ost`

**Was man sieht.** In einer engen Felsklamm nordöstlich des Kars hat das Schmelzwasser des einstigen Gletschers runde Töpfe in den Fels gebohrt – drei glattgeschliffene Kessel, der größte 6 m weit und mannstief, in jedem liegt noch der Mahlstein. Der Klammbach fällt von Topf zu Topf.

**Vorbild.** Real: Gletschergarten Luzern, Gletschertöpfe von Maloja, Strudeltöpfe der Liechtensteinklamm. Spiel: die Felsbecken in Horizon Forbidden West (Kältezonen).

**Standort.** Feld E1, X −250 / Y −3060, Boden 121,4 m. Schlucht/Kessel; Boden Fels 58 %, Erde 22 %, Heide 9 %, Trockengras 7 %; Hang 34° (max 80°), Exposition 98°, TPI25 −11,0 m, TPI100 −51,7 m, Relief 116 m im Radius. Weg 616 m (Punkt −646/−2588), **mit Steig 107 m** (`gletschersteig_ost`); Wasser 150 m, Meer 260 m, Stadtrand 488 m (EXP_003); 191 m innerhalb des Bioms; 24 Baumzellen im Radius (max 19 m); Einzugsfläche max 57352 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 4 von 328 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 128 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Die Klamm ist vom Oststeig aus nicht einsehbar (128 m maximale Sichtweite, 4 Wegpunkte); man steigt in die Kerbe und steht plötzlich über dem ersten Topf. Held-Blick bachauf: drei Töpfe in einer Linie, nasse Wände, Lichtfleck von oben. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 14 m (X −242 / Y −3048), `_held` 25 m (X −228 / Y −3072), `_nah` 10 m (X −241 / Y −3065). **Zugang (kandidaten.erreichbarkeit, 4 m):** 316 m vom Steig (Luftlinie 118 m), max 40,6°, Mittel 19,1°, 74 m steiler als 25°, 216 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: drei Töpfe als Geländeform (Stempel, runde Kessel −2…−4 m) mit Wandnetzen `SM_big_rock_wall_01/02/03` und glatten Schalen `SM_SmoothRockShelf_01` am Rand. Begleiter (3): Mahlsteine `SM_NordicBeachRocks_01` (0,3–0,5×) rund in jedem Topf. Schutt (60–100): runde Bachsteine `SM_NordicBeachRock_01`, `SM_BeachSandWithPebbles_01`. Kleinzeug: `SM_SmallStonesPack_*`. Bewuchs nach Ursache: Moos und Farn nur im Sprühbereich (`SM_MossClump_*`, `SM_BeechFern_04`, `SM_EagleFern_S_01`), oben Zwergkiefern. Kontaktzone: Nassband dunkel (`MI_Leakage_07/08`), Moos kriecht an den Topfrändern hoch (`M_EL_Klippe_RVT`).

**Wasser, Effekte, Licht.** `bach` farbe `klar` (Klammbach, 1,5 m) mit drei Stufen 2–3 m (werden kleine Fälle), jeder Topf als `see` 3–6 m, farbe `tuerkis`, Tiefe 2 m.

**Geländeänderung.** Stempel 90 × 50 m entlang der Klamm: Töpfe ausfräsen, Stufen betonen; Rand Δ 0. Lagen: Fels, Kies, Moos.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_big_rock_wall_01`, `SM_big_rock_wall_02`, `SM_big_rock_wall_03`, `SM_SmoothRockShelf_01`, `SM_NordicBeachRocks_01`, `SM_NordicBeachRock_01`, `SM_BeachSandWithPebbles_01`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_MossClump_01`, `SM_MossClump_02`, `SM_MossClump_03`, `SM_MossClump_04`, `SM_MossClump_05`, `SM_BeechFern_04`, `SM_EagleFern_S_01`; Decals: `MI_Leakage_07`, `MI_Leakage_08`; Material: `M_EL_Klippe_RVT`. Wunsch: **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (B) – Kaskaden zwischen den Töpfen, Ersatz: MI_EL_Wasserfall_Kaskade; **Free City & Nature Sounds** (B) – Rauschen in der Klamm, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Risiko: Klamm (Hang 34–80 Grad) – Zugang 316 m mit 74 m steiler als 25 Grad (Trittstufen).

### 7 · Der Nunatak (`gletscher_07_der_nunatak`) – Fundstück · nur mit Steig `gletschersteig_ost`

**Was man sieht.** Hinter dem Ostgrat versteckt sich ein schwarzer Felszahn, der aus einem Firnfeld ragt wie eine Insel aus dem Eis: der Nunatak. Seine Flanken sind vom Frost in Platten gesprengt, auf seinem Scheitel wächst ein Polster aus Moos und eine einzelne, vom Wind gebeugte Zwergkiefer – das einzige Lebende weit und breit.

**Vorbild.** Real: Nunatakker Grönlands und Islands (Esjufjöll), Felsinseln im Vatnajökull. Spiel: die Felsinseln im Eis von Skyrim (Ödfrost) und The Long Dark.

**Standort.** Feld E2, X 120 / Y −2970, Boden 223,5 m. Kuppe/Gipfel; Boden Fels 70 %, Schnee 24 %, Trockengras 4 %, Geroell 2 %; Hang 54° (max 67°), Exposition 64°, TPI25 5,4 m, TPI100 38,6 m, Relief 157 m im Radius. Weg 800 m (Punkt −472/−2432), **mit Steig 107 m** (`gletschersteig_ost`); Wasser 89 m, Meer 268 m, Stadtrand 720 m (EXP_003); 72 m innerhalb des Bioms; 47 Baumzellen im Radius (max 30 m); Einzugsfläche max 1380 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: nicht sichtbar.

**Komposition und Anmarsch.** Fundstück: Der Felszahn liegt hinter dem Ostgrat und ist von keinem Weg- oder Steigpunkt zu sehen (0 von 174); er erscheint, wenn man über den Sattel tritt. Held-Blick von Südosten (120 m) über das Firnfeld: dunkler Zahn vor dem Meer. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 77 m (X 49 / Y −2941), `_held` 120 m (X 161 / Y −2857), `_nah` 10 m (X 123 / Y −2961). **Zugang (kandidaten.erreichbarkeit, 4 m):** 185 m vom Steig (Luftlinie 107 m), max 34,9°, Mittel 21,3°, 43 m steiler als 25°, 114 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Felsturm 20–24 m aus `veqnci0db_tier_2` (hochkant, 6 m eingegraben) + `ukjhcamga_tier_0` als Flanke, Material mit Schneekappe (`M_EL_Fels_Auflage`, Auflage_Farbe weiß, Menge 0,6). Begleiter (4–6): `SM_MassiveTundraRockFormation_02` als Fußplatte, `SM_NordicBoulder_01`. Schutt (120–180): Frostschutt-Kegel `SM_TundraRockyGround_01`, `xjijdiz_tier_0`, `texndcpda_tier_0`, `SM_mountain_rock_big_02_*`. Kleinzeug: Plattenscherben `SM_ground_rock_03_01`. Bewuchs: Moospolster `SM_MossClump_*` und 1 Zwergkiefer `SM_dwarf_pine_medium_02` auf dem Scheitel (Windflüchter). Kontaktzone: Firn liegt in einem Randkolk 1–2 m tiefer um den Fels (Windkolk), Schutt auf dem Firn.

**Wasser, Effekte, Licht.** keins; Schneefahne am Scheitel (Niagara-Wunsch, optional).

**Geländeänderung.** Stempel 120 × 120 m: Firnfeld ringsum glätten (Lage Schnee 255), Randkolk −1,5 m; der Zahn ist Netz.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `veqnci0db_tier_2`, `ukjhcamga_tier_0`, `SM_MassiveTundraRockFormation_02`, `SM_NordicBoulder_01`, `SM_TundraRockyGround_01`, `xjijdiz_tier_0`, `texndcpda_tier_0`, `SM_mountain_rock_big_02_1`, `SM_mountain_rock_big_02_2`, `SM_mountain_rock_big_02_3`, `SM_mountain_rock_big_02_4`, `SM_mountain_rock_big_02_5`, `SM_mountain_rock_big_02_6`, `SM_mountain_rock_big_02_7`, `SM_mountain_rock_big_02_8`, `SM_ground_rock_03_01`, `SM_MossClump_01`, `SM_MossClump_02`, `SM_MossClump_03`, `SM_MossClump_04`, `SM_MossClump_05`, `SM_dwarf_pine_medium_02`; Material: `M_EL_Fels_Auflage`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (B) – Firnfeld-Ränder, Schnee am Fels (Rocky Snow Pile), Ersatz: Lage Schnee + M_EL_Fels_Auflage; **Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam** (C) – Schneefahne, Ersatz: ohne Effekt.

**Aufwand und Risiko.** Mittel. Risiko: das Firnfeld macht den Ort – ohne Schneelage ist es nur ein Felsen. Abstand zu frost_04 (Raureifhain) 358 m.

### 8 · Der Gletscherschliff (`gletscher_08_gletscherschliff`) – Fundstück · nur mit Steig `gletschersteig_nordhang`

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/frost/katalog.md](sehens/frost/katalog.md)

### 1 · Der Eisfall (`frost_01_der_eisfall`) – Fundstück · nur mit Steig `froststeig`

**Was man sieht.** Wo der Nordbach über eine 12-m-Stufe in den Frostsee fällt, ist er mitten im Sturz erstarrt: ein Bündel aus milchig-blauen Eissäulen, zwischen denen hinter dünnem Eis noch Wasser rinnt – man hört es, aber sieht es nur als Schatten. Am Fuß ein Kegel aus gefrorener Gischt.

**Vorbild.** Real: gefrorene Fälle im Johnston Canyon (Kanada), Eisfälle des Kandertals, Gefrorener Fall von Fang (Ouray). Spiel: Eisfälle in Skyrim (Winterfeste) und The Long Dark.

**Standort.** Feld E2, X 75 / Y −2420, Boden 40,0 m. Offener Hang; Boden Schnee 85 %, Fels 9 %, Eis 6 %; Hang 15° (max 78°), Exposition 199°, TPI25 1,5 m, TPI100 −3,7 m, Relief 42 m im Radius. Weg 544 m (Punkt −470/−2424), **mit Steig 86 m** (`froststeig`); Wasser 0 m, Meer 383 m, Stadtrand 609 m (EXP_003); 224 m innerhalb des Bioms; 32 Baumzellen im Radius (max 28 m); Einzugsfläche max 95064 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 26 von 272 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 561 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Vom Froststeig aus (86 m) nur als heller Streifen in einer Kerbe erkennbar; die Säulen öffnen sich im Einschnitt. Held-Blick vom Seeeis hinauf. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 74 m (X 89 / Y −2492), `_held` 44 m (X 83 / Y −2463), `_nah` 10 m (X 77 / Y −2430). **Zugang (kandidaten.erreichbarkeit, 4 m):** 104 m vom Steig (Luftlinie 94 m), max 24,4°, Mittel 17,7°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Eissäulen aus `SM_EISZAPFEN_4/8/9` (1,5–3×, gebündelt, 20–30 Stück) + Eisschale; Material `M_EL_Eis4` (Eis_Farbe heller, Schnee_Menge 0,3). Begleiter (4): Felsköpfe `SM_big_rock_wall_02`, `rcygn_tier_0` mit Eisglasur. Schutt (60–100): gebrochene Zapfen `SM_EISZAPFEN_1/2/5` am Fuß, Steine `SM_NordicBeachRock_01`. Kleinzeug: Eiskrümel (Lage Eis). Bewuchs: vereiste Zwergkiefern am Rand `SM_dwarf_pine_small_01/02` (Material Raureif, s. Materialwünsche). Kontaktzone: Gischteis überzieht die Felsen bis 6 m seitlich (Lage Eis, Decal nass `MI_Leakage_02`).

**Wasser, Effekte, Licht.** Bach oben als `bach` (farbe `klar`) bis zur Kante, darunter kein fließendes Wasser – nur ein schmaler `wasserfall`-Streifen 0,5 m mit `MI_EL_Wasserfall_Kaskade` hinter den Säulen (Deckkraft niedrig). Kalter Dunst `lokaler_nebel` 0,04.

**Geländeänderung.** Stufe versteilen (+2 m Kante, 70–80 Grad), Kegel +1,5 m. Fenster 80 × 60 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_4`, `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_big_rock_wall_02`, `rcygn_tier_0`, `SM_EISZAPFEN_1`, `SM_EISZAPFEN_2`, `SM_EISZAPFEN_5`, `SM_NordicBeachRock_01`, `SM_dwarf_pine_small_01`, `SM_dwarf_pine_small_02`; Decals: `MI_Leakage_02`; Material: `M_EL_Eis4`, `MI_EL_Wasserfall_Kaskade`. Wunsch: **CryoGen: Native Procedural Ice Architecture** (B) – Eissäulen/Tropfeis auf Fels, Ersatz: SM_EISZAPFEN_4/8/9 bis 3x skaliert; **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (B) – Eiskegel am Fuß (Rocky Snow Pile), Ersatz: Geländekegel + Lage Eis; **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (C) – Restwasser hinter den Säulen, Ersatz: MI_EL_Wasserfall_Kaskade.

**Aufwand und Risiko.** Mittel. Risiko: Eiszapfen max. 4 m – mit 3× Skala Rauheit prüfen (Wunsch CryoGen/Arctic Cliffs).

### 2 · Der Frostsee (`frost_02_frostsee`) – Leuchtfeuer · nur mit Steig `froststeig_sued`

**Was man sieht.** Der Frostsee ist ganz zugefroren, aber nicht weiß: Wind hat den Schnee abgefegt, und man blickt durch schwarzes, klares Eis. Quer über den See läuft ein Rücken aus hochkant gestellten, blau leuchtenden Schollen – Presseis, 3–5 m hoch, wo die Eisdecke zusammengeschoben wurde. In der Westbucht stehen im Schwarzeis weiße Blasen übereinander wie eingefrorene Perlenschnüre.

**Vorbild.** Real: Presseisrücken des Baikalsees, Methanblasen im Abraham Lake (Alberta). Spiel: die Eisseen in Horizon Zero Dawn (Frozen Wilds) und The Long Dark (Mystery Lake).

**Standort.** Feld E2, X 200 / Y −2260, Boden 19,7 m. Ebene; Boden Eis 56 %, Schnee 41 %, Trockengras 3 %; Hang 0° (max 38°), Exposition 0°, TPI25 −0,1 m, TPI100 1,3 m, Relief 13 m im Radius. Weg 690 m (Punkt −470/−2424), **mit Steig 108 m** (`froststeig_sued`); Wasser 8 m, Meer 184 m, Stadtrand 779 m (EXP_003); 185 m innerhalb des Bioms; 42 Baumzellen im Radius (max 26 m); Einzugsfläche max 133688 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 6 m: 51 von 159 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,32, lesbar bis 762 m; bester Punkt −210/−2402 in 434 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: Der blaue Zackenkamm auf der dunklen Fläche ist vom Froststeig (434–762 m) lesbar. Held-Blick vom Nordufer (Kamera 226 m) über das Schwarzeis: Blasen im Vordergrund, Presseisrücken diagonal als Blickachse, Raureif-Kuppe dahinter. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 44 m (X 181 / Y −2220), `_held` 216 m (X 150 / Y −2470), `_nah` 10 m (X 198 / Y −2270), `_fern` 434 m (X −210 / Y −2402). **Zugang (kandidaten.erreichbarkeit, 4 m):** 117 m vom Steig (Luftlinie 111 m), max 24,0°, Mittel 6,9°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Presseisrücken aus 25–40 Eisplatten (Wunsch Megascans Ice Cliff/Arctic Cliffs Eisplatten; Ersatz flache Eisschalen aus `SM_EISZAPFEN_8/9` nebeneinander, Material `M_EL_Eis4`). Begleiter (6–8): größere Schollen, schief. Schutt (150–200): Eissplitter um den Rücken. Kleinzeug: Blasen als Decal unter der Eisfläche (Material-Wunsch Schwarzeis mit Blasen-Parallax). Bewuchs: Schilfhalme eingefroren am Ufer (`SM_rough_horsetail_*` mit Raureif). Kontaktzone: Ufereis mit Schneewehen, Risse als Decal.

**Wasser, Effekte, Licht.** Vorhandener Frostsee (S_K13_FROSTSEE_00, eis true) bleibt; Eisdecke als Lage Eis + `see` farbe `schwarz_spiegel` mit Eismaterial. Kein Nebel; klare Luft – die Wirkung kommt aus Spiegelung und Blau.

**Geländeänderung.** Keine (See ist da); Ufer 0,5 m angleichen. Alte Houdini-Reste am Nordufer (K13_FROSTSEE) werden ausgeblendet – nichts davon nutzen.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_rough_horsetail_01`, `SM_rough_horsetail_02`, `SM_rough_horsetail_03`; Material: `M_EL_Eis4`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Presseisplatten (Ice Cliff zerschnitten), Ersatz: SM_EISZAPFEN_8/9 flach + Material M_EL_Eis4; **Arctic Cliffs** (B) – Eisplatten, Treibeis-Blueprint, Ersatz: wie oben; **Free City & Nature Sounds** (C) – Eisknacken, Wind, Ersatz: kein Klang.

**Aufwand und Risiko.** Hoch (Eisplatten und Blasenmaterial). Risiko: Schwarzeis-Material ist neu (Materialwunsch).

### 3 · Der Eisvorhang (`frost_03_eisvorhang`) – Fundstück · nur mit Steig `froststeig`

**Was man sieht.** Unter dem Nordufer des Frostsees tritt Sickerwasser aus einer überhängenden Felsbank. Es ist zu einem 40 m langen Vorhang gefroren: Hunderte Zapfen nebeneinander, oben fingerdick, unten zu Orgelpfeifen verwachsen, dahinter eine flache, blau dämmernde Nische.

**Vorbild.** Real: Eisvorhänge an der Apostle Islands Sea Caves (Lake Superior), Eiszapfenwände am Ouray Ice Park. Spiel: Eishöhlen in Skyrim und God of War (Midgard im Fimbulwinter).

**Standort.** Feld E2, X 300 / Y −2460, Boden 29,8 m. Offener Hang; Boden Schnee 97 %, Eis 2 %, Fels 1 %; Hang 40° (max 58°), Exposition 190°, TPI25 −2,2 m, TPI100 −2,9 m, Relief 29 m im Radius. Weg 771 m (Punkt −470/−2426), **mit Steig 87 m** (`froststeig`); Wasser 90 m, Meer 248 m, Stadtrand 821 m (EXP_003); 249 m innerhalb des Bioms; 5 Baumzellen im Radius (max 28 m); Einzugsfläche max 4812 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 32 von 201 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 550 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Vom Steig aus 87 m entfernt liegt die Felsbank in einer Hangkerbe; der Vorhang ist erst auf dem Uferweg zu sehen. Held-Blick seitlich entlang des Vorhangs. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 107 m (X 221 / Y −2531), `_held` 44 m (X 256 / Y −2460), `_nah` 10 m (X 290 / Y −2460). **Zugang (kandidaten.erreichbarkeit, 4 m):** 140 m vom Steig (Luftlinie 115 m), max 28,5°, Mittel 15,2°, 3 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Vorhang aus `SM_EISZAPFEN_1…9` (300–500 Instanzen, dicht, Länge nach Unterkante gestaffelt) an einer Felsbank `SM_big_rock_wall_01/03` + `vfmjadufa_tier_2` als Überhang (Netz, Gelände kann nicht überhängen). Begleiter (3–4): Eissäulen bis zum Boden. Schutt (80–120): abgebrochene Zapfen. Kleinzeug: Eiskrümel, Steine. Bewuchs: Moos unter dem Eis sichtbar (grün durch Eis, Lage Moos am Fuß). Kontaktzone: nasser Fels oberhalb (`MI_Leakage_09`).

**Wasser, Effekte, Licht.** Sickerlinie als dünner `bach` (0,3 m) oberhalb, endet `versickert` am Vorhang.

**Geländeänderung.** Felsbank +2 m betonen, Fuß −1 m (Nische). Fenster 60 × 40 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_1`, `SM_EISZAPFEN_2`, `SM_EISZAPFEN_3`, `SM_EISZAPFEN_4`, `SM_EISZAPFEN_5`, `SM_EISZAPFEN_6`, `SM_EISZAPFEN_7`, `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_big_rock_wall_01`, `SM_big_rock_wall_03`, `vfmjadufa_tier_2`; Decals: `MI_Leakage_09`. Wunsch: **CryoGen: Native Procedural Ice Architecture** (B) – dichter Zapfenvorhang, Ersatz: SM_EISZAPFEN_1…9 (300–500 Instanzen); **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (C) – Eisglasur am Fels, Ersatz: Material M_EL_Eis4.

**Aufwand und Risiko.** Mittel. Abgrenzung zu tundra_03 „Die Eiswand“: dort (vermutlich) freigelegtes Bodeneis; hier gefrorenes Sickerwasser an Fels.

### 4 · Der Raureifhain (`frost_04_raureifhain`) – Leuchtfeuer · nur mit Steig `froststeig`

**Was man sieht.** Auf einer Hangschulter über dem Frostsee stehen dreißig Kiefern, die keine Bäume mehr zu sein scheinen: dicke Panzer aus Raureif und Schnee haben sie in weiße, gebeugte Gestalten verwandelt – Schneegespenster, die alle nach Osten schauen, weil der Wind von Westen kommt.

**Vorbild.** Real: Juhyo (Schneemonster) am Zao in Japan, Raureifwälder Lapplands (Riisitunturi). Spiel: die verschneiten Wälder in Red Dead Redemption 2 (Colter) und Skyrim (Dämmerstern).

**Standort.** Feld F2, X 330 / Y −2680, Boden 139,4 m. Oberhang/Plateaukante; Boden Schnee 80 %, Geroell 15 %, Fels 3 %, Eis 1 %; Hang 56° (max 58°), Exposition 166°, TPI25 −0,8 m, TPI100 16,4 m, Relief 105 m im Radius. Weg 839 m (Punkt −470/−2426), **mit Steig 88 m** (`froststeig`); Wasser 142 m, Meer 380 m, Stadtrand 843 m (EXP_003); 220 m innerhalb des Bioms; 170 Baumzellen im Radius (max 29 m); Einzugsfläche max 1224 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 16 m: 55 von 150 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,34, lesbar bis 777 m; bester Punkt −120/−2446 in 507 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: die weiße Gruppe hebt sich auf der Felsschulter gegen den dunklen Hang ab, vom Froststeig 434–777 m lesbar. Held-Blick von Osten durch die Gestalten auf den See. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 113 m (X 299 / Y −2571), `_held` 67 m (X 393 / Y −2703), `_nah` 10 m (X 339 / Y −2683), `_fern` 507 m (X −120 / Y −2446). **Zugang (kandidaten.erreichbarkeit, 4 m):** 229 m vom Steig (Luftlinie 113 m), max 26,5°, Mittel 19,0°, 9 m steiler als 25°, 58 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: 25–35 Kiefern `SM_Forest_pine_06/07`, `SM_dwarf_pine_big_01/02` mit Raureif-Material (M_EL_Pflanze, Farbe weiß-bläulich) und Schneekappen-Netzen (Wunsch Megascans Snow Embankment klein; Ersatz Lage Schnee + Material). Begleiter: 3 tote, ganz eingepackte Stämme `SM_Forest_pine_10_dead`. Schutt (60–100): abgebrochene Äste `SM_Pine_broken_branch_01/02` im Schnee. Kleinzeug: Eisnadeln. Bewuchs nach Ursache: Windflüchter – Kronen nach Osten gekämmt (Rotation), Westseite dicker Panzer. Kontaktzone: Schneewehen hinter jedem Baum (Lage Schnee, Geländewelle +0,5 m).

**Wasser, Effekte, Licht.** keins; feines Glitzern optional (Niagara Schneefall leicht, Wunsch).

**Geländeänderung.** Schneewehen-Muster ±0,5 m (Stempel klein). Lagen: Schnee 255.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_Forest_pine_06`, `SM_Forest_pine_07`, `SM_dwarf_pine_big_01`, `SM_dwarf_pine_big_02`, `SM_Forest_pine_10_dead`, `SM_Pine_broken_branch_01`, `SM_Pine_broken_branch_02`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (B) – Schneekappen/Wehen (Snow Embankment klein), Ersatz: Lage Schnee + Raureif-Material; **Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam** (B) – Glitzernder Schneefall, Eisnebel, Ersatz: ohne Effekt.

**Aufwand und Risiko.** Mittel. Risiko: Material entscheidet – ohne Raureif-Material nur verschneite Kiefern.

### 5 · Der Blockgletscher (`frost_05_blockgletscher`) – Fundstück · nur mit Steig `froststeig`

**Was man sieht.** Am Osthang zieht eine graue Zunge aus Blöcken wie ein Lavastrom ins Tal – aber sie ist kalt: ein Blockgletscher, unter dessen Schutt ein Eiskern steckt. Die Stirn ist 6 m hoch und steil, an ihrer Basis tritt eiskaltes Wasser aus und hat einen kleinen, schwarz zugefrorenen Blasensee aufgestaut.

**Vorbild.** Real: Blockgletscher im Engadin (Murtèl), Sulzkar (Steiermark), Alaska Range. Spiel: die Geröllhalden in Witcher 3 (Skellige) – hier mit Eiskern und Wulsten.

**Standort.** Feld F2, X 520 / Y −2800, Boden 69,2 m. Offener Hang; Boden Schnee 47 %, Geroell 34 %, Eis 9 %, Trockengras 8 %; Hang 34° (max 46°), Exposition 351°, TPI25 −0,4 m, TPI100 2,9 m, Relief 94 m im Radius. Weg 1058 m (Punkt −472/−2432), **mit Steig 250 m** (`froststeig`); Wasser 123 m, Meer 200 m, Stadtrand 1048 m (EXP_003); 100 m innerhalb des Bioms; 52 Baumzellen im Radius (max 33 m); Einzugsfläche max 5060 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 4 von 119 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 531 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Blockzunge liegt hinter einer Hangrippe, vom Steig aus nur aus 4 Punkten zu sehen. Held-Blick an der Stirn: Wulste von oben nach unten, See vorne. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 44 m (X 564 / Y −2798), `_held` 25 m (X 542 / Y −2812), `_nah` 10 m (X 529 / Y −2805). **Zugang (kandidaten.erreichbarkeit, 4 m):** 411 m vom Steig (Luftlinie 262 m), max 24,9°, Mittel 8,2°, 0 m steiler als 25°, 5 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Stirn als Geländestufe + 20–30 Blöcke `SM_NordicBoulder_01`, `SM_TundraMossyBoulder_01`, `SM_MassiveTundraRockFormation_02`. Begleiter: Fließwulste (3–4 bogenförmige Rücken). Schutt (180–200): Blockfeld `SM_TundraRockyGround_01`, `SM_mountain_rock_big_01_*`, `SM_mountain_rock_big_02_*`, `xf3odif_tier_0`. Kleinzeug: `SM_SmallStonesPack_*` nur an der Stirnbasis (feines Material rieselt). Bewuchs: Flechten auf alten Blöcken (Material Auflage grau-grün), nichts auf der aktiven Stirn. Kontaktzone: Eis in Lücken der Stirn sichtbar (`SM_EISZAPFEN_1/5` liegend, Material Eis4).

**Wasser, Effekte, Licht.** Blasensee `see` ~18 m, farbe `schwarz_spiegel`, mit Eismaterial (Blasen wie Frostsee).

**Geländeänderung.** Stempel 160 × 110 m: Wulste +1…+2 m, Stirn +4 m steil (Netze tragen die Steilheit).

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_NordicBoulder_01`, `SM_TundraMossyBoulder_01`, `SM_MassiveTundraRockFormation_02`, `SM_TundraRockyGround_01`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_mountain_rock_big_02_1`, `SM_mountain_rock_big_02_2`, `SM_mountain_rock_big_02_3`, `SM_mountain_rock_big_02_4`, `SM_mountain_rock_big_02_5`, `SM_mountain_rock_big_02_6`, `SM_mountain_rock_big_02_7`, `SM_mountain_rock_big_02_8`, `xf3odif_tier_0`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_EISZAPFEN_1`, `SM_EISZAPFEN_5`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (C) – Eis in den Stirnlücken, Ersatz: SM_EISZAPFEN_1/5 liegend.

**Aufwand und Risiko.** Mittel. Abgrenzung zu heide „Blockstrom“ (Steinstrom ohne Eis, flach) und bergwald „Felsenmeer“ (bemoost unter Wald).

### 6 · Die Eisküste (`frost_06_eiskueste`) – Leuchtfeuer · nur mit Steig `froststeig`

**Was man sieht.** An der Ostküste friert die Brandung an: ein Eisfuß aus geschichtetem Spritzeis säumt den Strand, und darauf stehen Eisvulkane – Kegel bis 4 m, aus deren Spitze bei jeder Welle eine Fontäne aus Wasser und Eisbrei schießt. Felsen im Wasser tragen Eiskappen wie Zuckerhüte.

**Vorbild.** Real: Eisvulkane am Michigansee (Grand Haven), Eisfuß an der Küste Spitzbergens. Spiel: die vereisten Küsten in God of War (2018) und Skyrim (Meer der Geister).

**Standort.** Feld F2, X 630 / Y −2520, Boden 9,2 m. Offener Hang; Boden Schnee 100 %; Hang 9° (max 29°), Exposition 117°, TPI25 0,7 m, TPI100 1,2 m, Relief 23 m im Radius. Weg 1104 m (Punkt −470/−2426), **mit Steig 94 m** (`froststeig`); Wasser 290 m, Meer 43 m, Stadtrand 1143 m (EXP_003); 43 m innerhalb des Bioms; 252 Baumzellen im Radius (max 33 m); Einzugsfläche max 19452 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 8 m: 6 von 91 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,05, lesbar bis 788 m; bester Punkt −152/−2424 in 788 m mit Anteil 0,99; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: die weißen Kegel mit Fontäne über dem dunklen Meer – vom Froststeig 6 Punkte bis 788 m; ein kleines, aber klares Signal am Ende des Steigs. Held-Blick vom Hang (100 m) über Eisfuß und Kegel aufs Meer. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 74 m (X 569 / Y −2479), `_held` 101 m (X 531 / Y −2538), `_nah` 10 m (X 620 / Y −2522), `_fern` 788 m (X −152 / Y −2424). **Zugang (kandidaten.erreichbarkeit, 4 m):** 100 m vom Steig (Luftlinie 93 m), max 10,9°, Mittel 3,0°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: 3–4 Eiskegel (Geländekegel + Eisnetze, Wunsch Megascans Rocky Snow Pile/Ice Cliff; Ersatz Lage Eis + `SM_EISZAPFEN_8/9` als Kraterrand). Begleiter (5–8): eisgekappte Felsen `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01` (Material Auflage weiß). Schutt (100–200): Eisschollen am Strand. Kleinzeug: Eiskrümel, Kies `SM_BeachSandWithPebbles_01/02`. Bewuchs: keiner. Kontaktzone: Eisfuß mit Schichtkante, Nassband (`MI_Leakage_11`).

**Wasser, Effekte, Licht.** Meer vorhanden; Fontänen als Niagara (Wunsch, optional), sonst nur Gischt-Decal. Nebel: Seerauch über dem Wasser (`lokaler_nebel` 0,05).

**Geländeänderung.** Eisfuß +1 m Band, Kegel +2…+4 m. Fenster 120 × 80 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01`, `SM_BeachSandWithPebbles_01`, `SM_BeachSandWithPebbles_02`; Decals: `MI_Leakage_11`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Eiskegel und Eiskappen (Rocky Snow Pile, Ice Cliff), Ersatz: Lage Eis + SM_EISZAPFEN_8/9; **Niagara Examples Pack** (B) – Fontänen der Eisvulkane, Gischt, Ersatz: Decal statt Bewegung; **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (B) – Nassband-Decals, Spülsaum, Ersatz: MI_Leakage_11; **Free City & Nature Sounds** (C) – Brandung, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel–hoch (ohne Niagara fehlt die Bewegung). Abgrenzung zu kueste (Felstor, Pfeiler, Blasloch aus Fels).

### 7 · Die Frostblumen (`frost_07_frostblumen`) – Fundstück · nur mit Steig `froststeig_sued`

**Was man sieht.** Wo der Abfluss des Frostsees ins Meer mündet, liegt eine flache Lagune mit hauchdünnem, jungem Eis. Darauf wachsen Frostblumen: Tausende fingergroße Eiskristalle, wie Federn oder Farne, die in der Sonne glitzern – ein Feld, das bei jedem Schritt knistert.

**Vorbild.** Real: Frostblumen auf jungem Meereis (Arktis), auf Seen in Schweden. Spiel: kaum gesehen – genau deshalb ein Fundstück.

**Standort.** Feld F2, X 450 / Y −2270, Boden 2,6 m. Ebene; Boden Schnee 100 %, Trockengras 0 %; Hang 3° (max 22°), Exposition 99°, TPI25 0,2 m, TPI100 0,3 m, Relief 7 m im Radius. Weg 933 m (Punkt −470/−2424), **mit Steig 191 m** (`froststeig_sued`); Wasser 6 m, Meer 40 m, Stadtrand 1011 m (EXP_003); 40 m innerhalb des Bioms; 65 Baumzellen im Radius (max 31 m); Einzugsfläche max 450400 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 43 von 118 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 790 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: liegt tief hinter einem Uferwall; vom Weg nicht zu sehen. Vom Südsteig aus ist die Fläche als heller Fleck erkennbar, die Kristalle aber erst aus 5–10 m. Held-Blick flach über die Kristalle gegen die Sonne. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 189 m (X 301 / Y −2153), `_held` 120 m (X 332 / Y −2249), `_nah` 10 m (X 440 / Y −2268). **Zugang (kandidaten.erreichbarkeit, 4 m):** 200 m vom Steig (Luftlinie 189 m), max 6,0°, Mittel 1,4°, 0 m steiler als 25°, 0 m Querhang > 38°, 6 m Furt → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Kristallfeld als Instanzen (Wunsch CryoGen oder eigene kleine Kristallnetze; Ersatz `SM_EISZAPFEN_1/5` sehr klein, 0,05–0,1×, Tausende). Begleiter: 3–4 flache Felsen `SM_NordicBeachRockyGround_02`. Schutt: Treibholz `SM_beach_driftwood_01` eingefroren. Kleinzeug: Eiskrümel. Bewuchs: Strandgras am Wall `SM_beach_grass_01_1/2` mit Raureif. Kontaktzone: Rand der Lagune mit Spülsaum aus Eis.

**Wasser, Effekte, Licht.** Lagune `see` ~40 × 30 m, farbe `schwarz_spiegel`, Tiefe 0,5 m, mit Eismaterial (dünn).

**Geländeänderung.** Uferwall +1 m, Lagune −0,5 m. Fenster 100 × 80 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_1`, `SM_EISZAPFEN_5`, `SM_NordicBeachRockyGround_02`, `SM_beach_driftwood_01`, `SM_beach_grass_01_1`, `SM_beach_grass_01_2`. Wunsch: **CryoGen: Native Procedural Ice Architecture** (B) – kleine Eiskristalle (Frostblumen), Ersatz: SM_EISZAPFEN_1/5 0,05–0,1x; **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (C) – Treibholz/Spülsaum, Ersatz: SM_beach_driftwood_01.

**Aufwand und Risiko.** Mittel. Risiko: Instanzenzahl (Kristalle) – Budget 8 000 kleine Instanzen. Ersetzt die frühere Idee „Aufeis“, das jetzt die Tundra hat (tundra_06).

### 8 · Der Glockenbach (`frost_08_glockenbach`) – Fundstück · nur mit Steig `froststeig_sued`

**Was man sieht.** Ein flacher Bach rauscht über Steine zum Meer – und jeder Stein, den die Spritzer treffen, trägt eine Glocke aus Eis: runde, durchsichtige Hauben, unten offen, in denen das Wasser klingelt. An den Ufern hängen Eiskragen über dem Wasser.

**Vorbild.** Real: Eisglocken im Zillertal und am Lake Superior, Eiskragen an Bächen Finnlands. Spiel: so noch nicht gesehen.

**Standort.** Feld E2, X 230 / Y −2060, Boden 3,1 m. Offener Hang; Boden Schnee 100 %; Hang 8° (max 22°), Exposition 212°, TPI25 −0,8 m, TPI100 −0,9 m, Relief 7 m im Radius. Weg 788 m (Punkt −472/−2418), **mit Steig 90 m** (`froststeig_sued`); Wasser 0 m, Meer 76 m, Stadtrand 900 m (EXP_003); 71 m innerhalb des Bioms; 57 Baumzellen im Radius (max 24 m); Einzugsfläche max 14444 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 47 von 132 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 795 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Der Bach liegt in einer flachen Rinne; die Glocken sind erst aus 10–20 m als Glanz zu erkennen. Held-Blick bachab auf einer Steinreihe. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 89 m (X 231 / Y −2149), `_held` 120 m (X 138 / Y −2137), `_nah` 10 m (X 221 / Y −2064). **Zugang (kandidaten.erreichbarkeit, 4 m):** 89 m vom Steig (Luftlinie 89 m), max 7,9°, Mittel 3,6°, 0 m steiler als 25°, 0 m Querhang > 38°, 9 m Furt → frei begehbar.

**Detail-Ebenen.** Held: 30–60 Eisglocken auf Steinen (Wunsch CryoGen; Ersatz halbierte Eisschalen aus `SM_EISZAPFEN_*` + Material Eis4) auf `SM_NordicBeachRock_01`, `SM_NordicBeachRocks_01`. Begleiter: Eiskragen am Ufer. Schutt (100–150): Bachsteine `SM_SmallStonesPack_*`, `SM_BeachSandWithPebbles_02`. Bewuchs: Seggen mit Raureif (`SM_wk2oaeyqx_VarB`). Kontaktzone: nasse, glänzende Steine (`MI_Leakage_01`).

**Wasser, Effekte, Licht.** Bach als `bach` (farbe `klar`, 2 m) mit Steinen im Wasser; kleine Stufen 0,3 m (Gischt).

**Geländeänderung.** Rinne −0,5 m schärfen. Fenster 80 × 40 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_1`, `SM_EISZAPFEN_2`, `SM_EISZAPFEN_3`, `SM_EISZAPFEN_4`, `SM_EISZAPFEN_5`, `SM_EISZAPFEN_6`, `SM_EISZAPFEN_7`, `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_NordicBeachRock_01`, `SM_NordicBeachRocks_01`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_BeachSandWithPebbles_02`, `SM_wk2oaeyqx_VarB`; Decals: `MI_Leakage_01`. Wunsch: **CryoGen: Native Procedural Ice Architecture** (B) – Eisglocken auf Steinen, Ersatz: halbe Eisschalen aus SM_EISZAPFEN_* + Material Eis4; **Free City & Nature Sounds** (C) – Bachklang, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Risiko: ohne Glocken-Netz nur Eis auf Steinen.

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/fjord/katalog.md](sehens/fjord/katalog.md)

### 1 · Die Kanzel (`fjord_01_die_kanzel`) – Leuchtfeuer · nur mit Steig `fjordsteig_kanzel`

**Was man sieht.** Am Rand der Ostwand springt eine flache Felsplatte über den Fjord vor – eben wie ein Tisch, an drei Seiten 220 m senkrecht. Ein Riss trennt sie fast von der Wand, man steigt über ihn hinüber. Unten liegt das Wasser grün und glatt, Möwen kreisen unterhalb.

**Vorbild.** Real: Preikestolen (Lysefjord). Spiel: die Aussichtsfelsen in Witcher 3 (Skellige) und Assassin's Creed Valhalla (Norwegen).

**Standort.** Feld D1, X −1555 / Y −3275, Boden 225,0 m. Kuppe/Gipfel; Boden Trockengras 63 %, Fels 20 %, Wiese 8 %, Moos 4 %; Hang 24° (max 69°), Exposition 327°, TPI25 4,9 m, TPI100 35,8 m, Relief 92 m im Radius. Weg 1120 m (Punkt −1424/−2164), **mit Steig 102 m** (`fjordsteig_kanzel`); Wasser 179 m, Meer 188 m, Stadtrand 1080 m (EXP_003); 187 m innerhalb des Bioms; 124 Baumzellen im Radius (max 32 m); Einzugsfläche max 3548 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 12 m: 44 von 125 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,31, lesbar bis 798 m; bester Punkt −1604/−2956 in 323 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: die vorspringende Platte ist von der Fjordsohle und vom Grat aus als Kante lesbar (11 Punkte bis 798 m). Held-Blick von der Platte fjordaus auf den Mund; zweiter Blick vom Fjordboden hinauf (Kamera _anmarsch). Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 139 m (X −1655 / Y −3371), `_held` 44 m (X −1547 / Y −3232), `_nah` 10 m (X −1553 / Y −3265), `_fern` 323 m (X −1604 / Y −2956). **Zugang (kandidaten.erreichbarkeit, 4 m):** 355 m vom Steig (Luftlinie 131 m), max 40,7°, Mittel 21,8°, 97 m steiler als 25°, 240 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Platte aus `SM_MassiveTundraRockFormation_01` (77 × 29 m, flach, 70 % eingegraben, über die Wandkante geschoben) + Riss als Lücke; Wand darunter `veqnci0db_tier_2`, `vmnmbhv_tier_0` (40 × 29 × 23 m) als Schalen. Begleiter (4): Blöcke am Riss `SM_NordicBoulder_01`. Schutt (40–60): Platten `SM_flat_rock_02/03/04`. Kleinzeug: Flechten, Steine. Bewuchs: Heide in Ritzen `SM_heath_A_01`, Krüppelkiefer `SM_pine_beach_crooked_01` am Plattenrand (Windflüchter). Kontaktzone: Grasnarbe endet am Riss, Moos in der Kluft.

**Wasser, Effekte, Licht.** keins oben; unten der Fjord.

**Geländeänderung.** Plattenrand +3 m ebnen, Wandkante unter der Platte −5 m (Überhang über Netz). Fenster 100 × 80 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_MassiveTundraRockFormation_01`, `veqnci0db_tier_2`, `vmnmbhv_tier_0`, `SM_NordicBoulder_01`, `SM_flat_rock_02`, `SM_flat_rock_03`, `SM_flat_rock_04`, `SM_heath_A_01`, `SM_pine_beach_crooked_01`. Wunsch: **Free City & Nature Sounds** (C) – Wind, Möwen, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Nur mit Fjordsteig + Kanzel-Ast (320 m, oben ≤ 27 Grad).

### 2 · Die Schleierwand (`fjord_02_schleierwand`) – Leuchtfeuer · nur mit Steig `fjordsteig`

**Was man sieht.** Am Talschluss des Fjords steht eine 250 m hohe, halbrunde Felswand. Über ihre Kante fallen sechs dünne Schmelzbäche aus den Firnrinnen des Grats – so dünn, dass sie halb im Wind verwehen, bevor sie unten in Schuttkegel und Moos aufschlagen. Die Wand ist schwarz und grün gestreift.

**Vorbild.** Real: Sieben Schwestern (Geirangerfjord), Mardalsfossen, Lauterbrunnen. Spiel: Wasserfallwände in Skyrim (Markarth) und Ghost of Tsushima.

**Standort.** Feld C2, X −1740 / Y −3000, Boden 263,8 m. Offener Hang; Boden Fels 95 %, Heide 2 %, Trockengras 1 %, Erde 1 %; Hang 66° (max 72°), Exposition 4°, TPI25 −2,3 m, TPI100 −9,2 m, Relief 309 m im Radius. Weg 894 m (Punkt −1430/−2162), **mit Steig 91 m** (`fjordsteig`); Wasser 89 m, Meer 362 m, Stadtrand 882 m (ROMAN_LOC_018); 362 m innerhalb des Bioms; 3 Baumzellen im Radius (max 22 m); Einzugsfläche max 17988 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 40 m: 8 von 66 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,12, lesbar bis 448 m; bester Punkt −1678/−3444 in 448 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: Vom Fjordboden und Fjordkopf aus (8 Punkte, bis 448 m) die silbernen Fäden vor dunkler Wand; Held-Blick vom Talboden (176 m) mit Bach im Vordergrund. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 121 m (X −1623 / Y −3031), `_held` 176 m (X −1709 / Y −3173), `_nah` 10 m (X −1738 / Y −3010), `_fern` 448 m (X −1678 / Y −3444). **Zugang (kandidaten.erreichbarkeit, 4 m):** 130 m vom Steig (Luftlinie 121 m), max 44,3°, Mittel 17,0°, 24 m steiler als 25°, 130 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: 4–6 Fallbänder `wasserfall` (je 0,6–1,5 m breit, 150–220 m Fall, Material `M_EL_Wasserfall2` mit Deckkraft 0,5, Straehnen 0,9). Begleiter: Wandnetze `vdssailfa_tier_2`, `vfmjadufa_tier_2` als Rippen. Schutt (150–200): Sturzkegel unter jedem Fall `SM_mountain_rock_big_01_*`, `SM_ground_rock_01/02`. Kleinzeug: `SM_SmallStonesPack_*`. Bewuchs nach Ursache: Moosstreifen und Farn nur in der Sprühzone (Klippe-Material Moos_Menge hoch, `SM_EagleFern_S_01/02`), Birken auf den Kegeln. Kontaktzone: Nassstreifen auf der Wand (`MI_Leakage_04/06`).

**Wasser, Effekte, Licht.** Fallbänder enden je in einem kleinen `see` (Gumpe 4–6 m, farbe `klar`), Abfluss als `bach` zum Fjordbach. Sprühnebel `lokaler_nebel` 0,08 am Wandfuß; Niagara-Gischt optional.

**Geländeänderung.** Wandfuß: Gumpen −1 m, Kegel +2 m. Oben am Grat 6 Firnrinnen −1 m als Quelle (Lage Schnee).

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `vdssailfa_tier_2`, `vfmjadufa_tier_2`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_ground_rock_01`, `SM_ground_rock_02`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_EagleFern_S_01`, `SM_EagleFern_S_02`; Decals: `MI_Leakage_04`, `MI_Leakage_06`; Material: `M_EL_Wasserfall2`. Wunsch: **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (A) – Fluss-/Wasserfall-Material für 6 dünne Fallbänder, Ersatz: MI_EL_Wasserfall (Deckkraft 0,5); **Niagara Examples Pack** (B) – Sprühnebel am Wandfuß, Ersatz: lokaler_nebel; **Realistic Waterfall and Water VFX** (C) – verwehende Fallfäden, Ersatz: Material allein.

**Aufwand und Risiko.** Hoch (6 Fälle). Abgrenzung zu bergwald_05 (ein Schleierfall in einer Klamm) und kueste „Seefall“ (Fall direkt ins Meer).

### 3 · Die Trollzunge (`fjord_03_trollzunge`) – Leuchtfeuer · nur mit Steig `fjordsteig`

**Was man sieht.** Am Grat über dem Talschluss ragt eine schmale Felszunge 15 m frei über den Abgrund nach Norden – darunter 300 m Luft bis zum Fjordboden. Von hier sieht man den ganzen Fjord bis zum Meer.

**Vorbild.** Real: Trolltunga (Skjeggedal). Spiel: Aussichtspunkte in Witcher 3 (Skellige) und Zelda Breath of the Wild (Türme).

**Standort.** Feld D2, X −1500 / Y −2930, Boden 384,9 m. Oberhang/Plateaukante; Boden Fels 79 %, Trockengras 13 %, Heide 8 %, Moos 0 %; Hang 63° (max 71°), Exposition 73°, TPI25 2,2 m, TPI100 34,3 m, Relief 136 m im Radius. Weg 770 m (Punkt −1424/−2164), **mit Steig 91 m** (`fjordsteig`); Wasser 210 m, Meer 395 m, Stadtrand 734 m (ROMAN_LOC_018); 252 m innerhalb des Bioms; 0 Baumzellen im Radius (max 0 m); Einzugsfläche max 1508 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 8 m: 56 von 189 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,30, lesbar bis 761 m; bester Punkt −1018/−3116 in 517 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: die Zunge steht als Zacken in der Gratlinie (21 Punkte, bis 761 m, auch vom Gletscher-Westgrat). Held-Blick seitlich vom Grat: Zunge vor dem Fjord. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 50 m (X −1530 / Y −2971), `_held` 101 m (X −1435 / Y −2853), `_nah` 10 m (X −1494 / Y −2922), `_fern` 517 m (X −1018 / Y −3116). **Zugang (kandidaten.erreichbarkeit, 4 m):** 140 m vom Steig (Luftlinie 97 m), max 36,5°, Mittel 19,9°, 35 m steiler als 25°, 96 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Felszunge aus `uchoab3fa_tier_0` (13,5 × 3,3 × 5,2 m) + `rcygn_tier_0` als Unterbau, 8 m eingegraben am Ansatz. Begleiter (3): Gratfelsen `SM_NordicBoulder_01`. Schutt (40–80): Frostschutt am Grat `SM_TundraRockyGround_01`. Kleinzeug: Steine. Bewuchs: Moospolster, Heide, keine Bäume. Kontaktzone: Flechten (Auflage grau-grün).

**Wasser, Effekte, Licht.** keins.

**Geländeänderung.** Grat am Ansatz −1 m (Sattel), sonst keine.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `uchoab3fa_tier_0`, `rcygn_tier_0`, `SM_NordicBoulder_01`, `SM_TundraRockyGround_01`. Wunsch: **Fantasy Ambiences (Lava, Höhle, Wind …)** (C) – Wind am Grat, Ersatz: kein Klang.

**Aufwand und Risiko.** Niedrig–mittel. Risiko: Zunge muss frei schweben – Netz mit Kollision, Fuß tief im Grat.

### 4 · Das Hängetal (`fjord_04_haengetal`) – Fundstück · nur mit Steig `fjordsteig`

**Was man sieht.** Auf der Südseite des Fjordkamms endet ein kleines, flaches Hochtal plötzlich an einer Stufe: Der Bach, der eben noch zwischen Wollgras mäanderte, stürzt 40 m in eine Schlucht. Oben ist es still und grün, unten donnert es.

**Vorbild.** Real: Hängetäler im Yosemite (Bridalveil) und in Norwegen (Aurland). Spiel: die Hochtäler in Skyrim (Rift).

**Standort.** Feld D2, X −1680 / Y −2775, Boden 194,6 m. Schlucht/Kessel; Boden Trockengras 35 %, Erde 29 %, Fels 27 %, Moos 6 %; Hang 32° (max 67°), Exposition 172°, TPI25 −11,3 m, TPI100 −38,9 m, Relief 103 m im Radius. Weg 663 m (Punkt −1430/−2162), **mit Steig 87 m** (`fjordsteig`); Wasser 0 m, Meer 585 m, Stadtrand 655 m (ROMAN_LOC_018); 148 m innerhalb des Bioms; 229 Baumzellen im Radius (max 33 m); Einzugsfläche max 32452 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 16 von 197 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 465 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: von unten verdeckt (Wald und Stufe), vom Fjordsteig erst auf den letzten 100 m. Held-Blick von der Lippe aus das Tal hinunter. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 42 m (X −1653 / Y −2743), `_held` 82 m (X −1733 / Y −2712), `_nah` 10 m (X −1686 / Y −2767). **Zugang (kandidaten.erreichbarkeit, 4 m):** 170 m vom Steig (Luftlinie 153 m), max 37,6°, Mittel 13,2°, 17 m steiler als 25°, 133 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Lippe aus `SM_big_rock_wall_01/02` + Fall (`wasserfall` 40 m, `M_EL_Wasserfall2`). Begleiter (4–5): Blöcke `SM_NordicBoulder_01` an der Lippe. Schutt (100–150): Bachbett `SM_DryRiverBed_01/02`, `SM_SmallStonesPack_*`. Bewuchs nach Ursache: oben Wollgras/Seggen `SM_wk2oaeyqx_VarA…I` und Moor-Moos (nass, flach), unten Farn in der Gischt `SM_EagleFern_S_04`, Birken. Kontaktzone: Nassband an der Lippe.

**Wasser, Effekte, Licht.** `bach` farbe `klar` 2 m, `wasserfall` 40 m an der Lippe, Gumpe `see` 8 m unten.

**Geländeänderung.** Hochtalboden flach glätten, Lippe +1 m. Fenster 120 × 80 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_big_rock_wall_01`, `SM_big_rock_wall_02`, `SM_NordicBoulder_01`, `SM_DryRiverBed_01`, `SM_DryRiverBed_02`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_wk2oaeyqx_VarA`, `SM_wk2oaeyqx_VarB`, `SM_wk2oaeyqx_VarC`, `SM_wk2oaeyqx_VarD`, `SM_wk2oaeyqx_VarE`, `SM_wk2oaeyqx_VarF`, `SM_wk2oaeyqx_VarG`, `SM_wk2oaeyqx_VarH`, `SM_wk2oaeyqx_VarI`, `SM_EagleFern_S_04`; Material: `M_EL_Wasserfall2`. Wunsch: **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (A) – Fall 40 m an der Lippe, Ersatz: MI_EL_Wasserfall + MI_EL_Wasserfall_Aufprall; **Free City & Nature Sounds** (C) – Rauschen, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Nur mit Fjordsteig.

### 5 · Der Fjordkopf (`fjord_05_fjordkopf`) – Fundstück · nur mit Steig `fjordsteig`

**Was man sieht.** Wo der Fjordbach ins Meer läuft, hat er einen flachen Fächer aus Kies und Sand geschüttet. Bei Ebbe liegt er frei: Rinnen, in denen das Süßwasser milchig ins grüne Salzwasser zieht, Tang auf den Steinen, und überall die Wände, die 300 m hochsteigen.

**Vorbild.** Real: Fjordköpfe in Geiranger, Lærdal, Fjærland. Spiel: Fjordufer in Assassin's Creed Valhalla (Norwegen) und God of War.

**Standort.** Feld C1, X −1754 / Y −3358, Boden 0,6 m. Talboden (U-Tal); Boden Erde 54 %, Sand 25 %, Fels 16 %, Geroell 3 %; Hang 0° (max 71°), Exposition 270°, TPI25 −0,9 m, TPI100 −26,1 m, Relief 84 m im Radius. Weg 1239 m (Punkt −1424/−2164), **mit Steig 87 m** (`fjordsteig`); Wasser 0 m, Meer 4 m, Stadtrand 1217 m (ROMAN_LOC_018); 4 m innerhalb des Bioms; 123 Baumzellen im Radius (max 33 m); Einzugsfläche max 153672 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 45 von 111 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 433 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: der Fächer liegt unter der Talkante; vom Weg nichts. Held-Blick vom Fächer fjordaus zwischen den Wänden. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 95 m (X −1757 / Y −3263), `_held` 82 m (X −1754 / Y −3276), `_nah` 10 m (X −1759 / Y −3349). **Zugang (kandidaten.erreichbarkeit, 4 m):** 102 m vom Steig (Luftlinie 95 m), max 17,6°, Mittel 12,0°, 0 m steiler als 25°, 0 m Querhang > 38°, 3 m Furt → frei begehbar.

**Detail-Ebenen.** Held: Fächer als Geländeform mit 3–5 Rinnen. Begleiter (5–8): Blöcke `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01` im Watt. Schutt (150–200): `SM_NordicBeachRockyGround_01/02`, `SM_NordicBeach_02`, `SM_BeachSandWithPebbles_01/02`. Kleinzeug: Treibholz `SM_beach_driftwood_01`. Bewuchs nach Ursache: Strandgras und Sanddorn am Rand `SM_beach_grass_01_*`, `SM_sea_buckthorn_01/02`; Tang auf Steinen (Wunsch Coast & Dunes). Kontaktzone: Spülsaum, nasser Sand (Decal).

**Wasser, Effekte, Licht.** Fjordbach-Mündung als `bach` (farbe `gletschermilch`) in den Fjord; Meer vorhanden.

**Geländeänderung.** Fächer +0,5 m, Rinnen −0,5 m. Fenster 140 × 100 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01`, `SM_NordicBeachRockyGround_01`, `SM_NordicBeachRockyGround_02`, `SM_NordicBeach_02`, `SM_BeachSandWithPebbles_01`, `SM_BeachSandWithPebbles_02`, `SM_beach_driftwood_01`, `SM_beach_grass_01_1`, `SM_beach_grass_01_2`, `SM_beach_grass_01_3`, `SM_beach_grass_01_4`, `SM_beach_grass_01_hp_1`, `SM_beach_grass_01_hp_2`, `SM_sea_buckthorn_01`, `SM_sea_buckthorn_02`. Wunsch: **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (A) – Seetang, Spülsaum-Decals, nasser Sand, Ersatz: SM_beach_driftwood_01, MI_Leakage_*; **Megascans Icelandic Sand With Pebbles** (C) – dunkler Kies im Fächer, Ersatz: SM_BeachSandWithPebbles_01/02.

**Aufwand und Risiko.** Niedrig–mittel.

### 6 · Der Bergsturzkegel (`fjord_06_bergsturz`) – Fundstück · nur mit Steig `fjordsteig`

**Was man sieht.** Aus der Westwand ist ein Stück Berg ausgebrochen: oben eine helle, frische Abrissnische, darunter ein Kegel aus hausgroßen Blöcken, der bis an den Talboden reicht. Zwischen den Blöcken wachsen schon junge Birken – der Sturz ist alt genug für Bäume, jung genug für scharfe Kanten.

**Vorbild.** Real: Bergsturz am Tafjord und Loen (Norwegen), Felsstürze im Yosemite. Spiel: Geröllhalden in Witcher 3 (Skellige).

**Standort.** Feld C1, X −1850 / Y −3170, Boden 118,4 m. Schlucht/Kessel; Boden Fels 84 %, Erde 13 %, Wiese 2 %, Trockengras 1 %; Hang 70° (max 73°), Exposition 118°, TPI25 −11,2 m, TPI100 −34,1 m, Relief 219 m im Radius. Weg 1092 m (Punkt −1430/−2162), **mit Steig 87 m** (`fjordsteig`); Wasser 100 m, Meer 207 m, Stadtrand 1083 m (ROMAN_LOC_018); 207 m innerhalb des Bioms; 41 Baumzellen im Radius (max 32 m); Einzugsfläche max 9484 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 53 von 118 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 330 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: liegt in der Westflanke, vom Fjordsteig aus erst nahe sichtbar. Held-Blick vom Kegelfuß hinauf zur Nische. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 99 m (X −1753 / Y −3151), `_held` 82 m (X −1769 / Y −3156), `_nah` 10 m (X −1840 / Y −3168). **Zugang (kandidaten.erreichbarkeit, 4 m):** 164 m vom Steig (Luftlinie 99 m), max 58,8°, Mittel 22,3°, 48 m steiler als 25°, 62 m Querhang > 38°, 6 m Furt → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: 8–12 große Blöcke `SM_NordicBoulder_01`, `SM_MassiveTundraRockFormation_02`, `ukjhcamga_tier_0`. Begleiter: Abrissnische als helles Netz `vdssailfa_tier_2`. Schutt (180–200): `SM_mountain_rock_big_01_*`, `SM_mountain_rock_big_02_*`, sortiert (groß unten). Kleinzeug: `SM_stone_03…08`. Bewuchs nach Ursache: Birken `Big_Tree_Birch_01` (0,4–0,6×) und Moos auf den älteren unteren Blöcken. Kontaktzone: Flechten nur auf alten Blöcken.

**Wasser, Effekte, Licht.** keins.

**Geländeänderung.** Nische −3 m, Kegel +4 m. Fenster 140 × 120 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_NordicBoulder_01`, `SM_MassiveTundraRockFormation_02`, `ukjhcamga_tier_0`, `vdssailfa_tier_2`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_mountain_rock_big_02_1`, `SM_mountain_rock_big_02_2`, `SM_mountain_rock_big_02_3`, `SM_mountain_rock_big_02_4`, `SM_mountain_rock_big_02_5`, `SM_mountain_rock_big_02_6`, `SM_mountain_rock_big_02_7`, `SM_mountain_rock_big_02_8`, `SM_stone_03`, `SM_stone_04`, `SM_stone_05`, `SM_stone_06`, `SM_stone_07`, `SM_stone_08`, `Big_Tree_Birch_01`. Wunsch: **Free City & Nature Sounds** (C) – Steinschlag/Wind, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel.

### 7 · Die Brandungsgrotte (`fjord_07_brandungsgrotte`) – Fundstück · nur mit Steig `fjordsteig`

**Was man sieht.** An der Ostspitze der Fjordmündung, wo die Dünung hereinläuft, hat das Meer einen schmalen Spalt ins Gestein gearbeitet: eine Grotte, hoch und eng, mit grünem Wasser, in dem Tang wogt. Bei jeder Welle atmet sie.

**Vorbild.** Real: Grotten an Norwegens Außenküste (Stetind-Fjord), Kvitholmen. Spiel: Meereshöhlen in God of War.

**Standort.** Feld D1, X −1640 / Y −3540, Boden 6,1 m. Offener Hang; Boden Trockengras 42 %, Sand 32 %, Fels 16 %, Moos 8 %; Hang 56° (max 60°), Exposition 359°, TPI25 −2,1 m, TPI100 −10,3 m, Relief 77 m im Radius. Weg 1375 m (Punkt −648/−2588), **mit Steig 98 m** (`fjordsteig`); Wasser 212 m, Meer 4 m, Stadtrand 1312 m (EXP_003); 4 m innerhalb des Bioms; 100 Baumzellen im Radius (max 33 m); Einzugsfläche max 6940 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: nicht sichtbar.

**Komposition und Anmarsch.** Fundstück: vom Steig aus nicht zu sehen (0 Punkte); man klettert über die Uferblöcke um die Ecke. Held-Blick in den Spalt. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 15 m (X −1647 / Y −3527), `_held` 44 m (X −1602 / Y −3562), `_nah` 10 m (X −1631 / Y −3545). **Zugang (kandidaten.erreichbarkeit, 4 m):** 119 m vom Steig (Luftlinie 97 m), max 30,9°, Mittel 14,9°, 27 m steiler als 25°, 119 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Grottenportal aus 2–3 Wandschalen `SM_HugeNordicCoastalCliff_01/02`, `SM_MassiveNordicCoastalCliff_01`. Begleiter: Uferblöcke `SM_NordicBeachRocks_01`. Schutt: `SM_NordicBeachRockyGround_01/02`. Bewuchs: Tang/Seepocken-Band (Wunsch Coast & Dunes Seetang). Kontaktzone: Nassband (`MI_Leakage_10`).

**Wasser, Effekte, Licht.** Meer; Gischt optional (Niagara).

**Geländeänderung.** Uferkante −1 m. Fenster 80 × 60 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_HugeNordicCoastalCliff_01`, `SM_HugeNordicCoastalCliff_02`, `SM_MassiveNordicCoastalCliff_01`, `SM_NordicBeachRocks_01`, `SM_NordicBeachRockyGround_01`, `SM_NordicBeachRockyGround_02`; Decals: `MI_Leakage_10`. Wunsch: **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (A) – Seetang-Band und Nässe, Ersatz: MI_Leakage_10; **Niagara Examples Pack** (B) – Gischt im Spalt, Ersatz: ohne Effekt; **Cave Ambience** (B) – Grottenklang, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel. Abgrenzung zu kueste „Grotte“ (Kliffhöhle mit türkisem Wasser): hier enger Spalt im Fjord mit Tang.

### 8 · Die alten Ufer (`fjord_08_strandterrassen`) – Fundstück · nur mit Steig `fjordsteig`

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

## tundra

| Nr | Name | Art | nächster Weg/Pfad | Pfad | Was man sieht | Draufsicht |
|---|---|---|---|---|---|---|
| 01 | **Der Eisbuckel** | Leuchtfeuer | 92 m | `tundra_pfad_der_pingo` | Aus der flachen Schwemmebene neben dem Zopfstrom wölbt sich ein vollkommen runder, 22 m hoher Hügel mit braun-grüner | [Bild](sehens/tundra/tundra_01_der_pingo.png) |
| 02 | **Der Wanderer** | Leuchtfeuer | 129 m | – | Auf dem höchsten Punkt einer kahlen, glattgeschliffenen Felskuppe liegt ein hausgroßer, fremdartig heller Block – | [Bild](sehens/tundra/tundra_02_der_wanderer.png) |
| 03 | **Die Eiswand** | Leuchtfeuer | 93 m | `tundra_pfad_die_eiswand` | An der Küste ist die Tundra aufgerissen: ein Halbrund von 100 m Breite, dessen Rückwand 8–10 m hoch aus gestreiftem | [Bild](sehens/tundra/tundra_03_die_eiswand.png) |
| 04 | **Die Fliesstreppe** | Leuchtfeuer | 145 m | – | Ein sonniger Südwesthang ist zu einer Riesentreppe geworden: fünf grüne, zungenförmige Wülste aus Fließerde, jeder | [Bild](sehens/tundra/tundra_04_die_fliesstreppe.png) |
| 05 | **Der Trunkene Grund** | Fundstück | 185 m | `tundra_pfad_der_trunkene_grund` | Hinter dem Hügelrücken, im lichten Fichten-Lärchen-Saum, liegt ein brauner See ohne festes Ufer. | [Bild](sehens/tundra/tundra_05_der_trunkene_grund.png) |
| 06 | **Das Schneetaelchen** | Fundstück | 283 m | – | In einer Hangmulde am Rand des Schneefelds liegt mitten im Sommer ein schmutzig-weißer Altschneerest, rosa | [Bild](sehens/tundra/tundra_06_das_schneetaelchen.png) |
| 07 | **Die Steinringe** | Fundstück | 93 m | – | Auf einer Kiesterrasse über dem Strand liegen zwanzig Ringe aus Steinen, 2–4 m im Durchmesser, so regelmäßig, als | [Bild](sehens/tundra/tundra_07_die_steinringe.png) |
| 08 | **Das Wabenmoor** | Fundstück | 104 m | – | Unten an der Flussmündung, im Schutz des Steilufers, ist der Boden in Waben zerlegt: sechseckige Felder von 9–12 m, | [Bild](sehens/tundra/tundra_08_das_wabenmoor.png) |

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/tundra/katalog.md](sehens/tundra/katalog.md)

### tundra_01_der_pingo – Der Eisbuckel (Leuchtfeuer)

**Was man sieht:** Aus der flachen Schwemmebene neben dem Zopfstrom wölbt sich ein vollkommen runder, 22 m hoher Hügel mit braun-grüner
Torfhaut. Seine Kuppe ist aufgeplatzt: drei Dehnungsrisse laufen sternförmig hangab, im Nordriss glänzt blau-weißes Eis – der Eiskern.
Oben ein Krater mit einem kleinen, smaragdgrünen See; am Kraterrand hängen abgekippte Torfsoden mit Krähenbeeren.
**Vorbild:** Ibyuk-Pingo bei Tuktoyaktuk (Kanada), Pingos im Mackenzie-Delta; Spiel: Skellige-Hochland (The Witcher 3) für die braun-grüne
Torfpalette, Hinterlande (DA:I) für offene Ebenen mit Einzelform.
**Standort:** C3, X −1736 / Y −1842 m, Boden 47,9 m. **Vorhandener** Rundhügel: TPI100 +20,5 m, TPI25 +7,1 m, Kuppe flach (1,9°),
Heide 73 % / Schlamm 20 % – die Form ist schon ein Pingo, nur ohne Krater. Weg 153 m (Aufstiegsweg-Abzweig), Wasser (Zopfstrom) 59 m,
Stadtrand Aufstiegsweg 205 m, 278 m im Biom.
**Sicht:** Silhouette 22 m: **110 von 129** Wegpunkten im Ring 300–800 m sehen ≥ 30 % (Mittel 0,79), lesbar bis 798 m; heute schon 110.
`_fern` vom Küstenweg bei X −1242 / Y −1796 (496 m).
**Komposition und Anmarsch:** Vom Weg östlich des Zopfstroms steht der Buckel als glatte Halbkugel vor dem Meer. Zugang 173 m, quert die
Flussrinnen (10 m Wasser) → **Pfad `tundra_pfad_der_pingo` (Trittsteine, 63 m inkl. Furt; letzte 92 m Trampelspur)**, max. 24,3° am Hügelfuß → kurze Kehren. `_held` vom
Ostufer: Vordergrund Kiesbank und Flussarme, Mitte der Buckel, Blickziel der Eisriss gegen den Himmel.
**Detail-Ebenen:** Held 1 – der Hügel selbst (Gelände) + Eislinse im Nordriss (`vd4hbizcb_tier_0`, `vd5leh0ga_tier_0` aus Megascans
Eis/Schnee, 40 % eingegraben, quer liegend). Begleiter 3–5 – abgerutschte Torfschollen am Kraterrand (`SM_MossyEmbankment_01/02`,
`SM_GrassyEmbankment_01`), ein Altschneerest in der Nordflanke (`uhuldcyfa_tier_0`). Schutt 40–80 – `SM_TundraRockyGround_01`,
`SM_ForestRockFormation_05`, `SM_NordicBeachRockyGround_02` in den Rissen (Ursache: Aufreißen), `SM_TundraMossyBoulder_01` am Fuß.
Kleinzeug – `SM_SmallStonesPack_08`, `xftjadtab_tier_0` (Schneehäufchen im Riss), Eiszapfen `SM_EISZAPFEN_6/8/9` an der Eislinse.
Bewuchs nach Ursache – Flanken trocken: Krähen-/Preiselbeere (`SM_lingonberry_01/02`, `SM_billberry_dry_01`, `SM_heath_A_01`),
Tundragras `SM_wk2oaeyqx_VarB/C/G`; Fuß nass (Schmelzwasser): Binsen `SM_ToadRush_010`, Polarweiden `SM_grey_willow_01/03`, Moos
(`SM_MossClump_01/03`); auf der Kuppe eine einzelne Zwergkiefer `SM_dwarf_pine_small_01` (Windflüchter). Kontaktzone – Risswände mit
Torfüberhang, Eis 40 % eingegraben, Nassband am Kratersee.
**Wasser, Effekte, Licht:** `see` im Krater (Ø ~14 m, `smaragd`, 2 m tief, Ufer überall über dem Spiegel). Eislinse feucht glänzend
(`MI_EL_SW_Grundeis`). Kein Nebel nötig; Licht von Süden modelliert die Kugelform.
**Geländeänderung:** Kuppe +3 m (r 34 m), Krater −7 m (r 13 m), drei Risse −1,4…−2,2 m; Fenster 108 × 108 m, |Δ| ≤ 4,6 m, an
Wegen/Wasser 0 m.
**Assets:** Bestand siehe oben (alle in `netze.csv`, geprüft gegen Sperre/Check). Eis jetzt vorhanden (13b). Wunsch: nur Klang
(vorhanden: `CUE_Wind_Autumn_wind_with_leaves_rustling_Cue`); optional „Fantasy Ambiences“ (C).
**Aufwand und Risiko:** mittel. Risiko: Eisnetze wirken „aufgelegt“ → tief einsetzen, Torfkante drüber.
Budget: ~5 000 Instanzen (400 Kollision), 20 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

### tundra_02_der_wanderer – Der Wanderer (Leuchtfeuer)

**Was man sieht:** Auf dem höchsten Punkt einer kahlen, glattgeschliffenen Felskuppe liegt ein hausgroßer, fremdartig heller Block –
11 × 14 m, 6,5 m hoch –, der auf drei kopfgroßen Steinen balanciert. Sein Fels passt zu nichts ringsum. Der Block ist gelb-grün von
Landkartenflechten gefleckt; um ihn breitet sich ein silbrig-weißer Teppich aus Rentierflechte, aus dem zwei kleinere Findlinge ragen.
**Vorbild:** Findlinge auf Rundhöckern in Lappland und Kanada (Perched Boulders, Big Rock Okotoks); Spiel: Felsen-Einzelgänger auf
Skellige-Kuppen (The Witcher 3), Silhouetten in den Sturmküsten (DA:I).
**Standort:** D2, X −968 / Y −2158 m, Boden 162,9 m. Gipfel der Mittelschulter: TPI100 **+39,7 m**, TPI25 +5,7 m, Gipfel flach (4,3°),
Heide 72 %, Trockengras 24 %. Weg 129 m (Serpentine Gletscherweg), Stadtrand Kharad-Vor 217 m.
**Sicht:** Ziel 8 m: **95 von 175** Wegpunkten (Mittel 0,48), bis 796 m; `_fern` vom Gletscherweg X −522 / Y −2386 (501 m) – der Block
steht dort gegen den Himmel.
**Komposition und Anmarsch:** Zugang 265 m ohne Pfadbau (max. 24,9°, mittel 19,6° – steil, aber im Limit; Trampelspur als Bodenlage).
`_held` 25 m östlich, Blick nach Westen: Flechtenteppich vorn, Block mittig, dahinter die Weite bis Kharad-Vor.
**Detail-Ebenen:** Held – `SM_NordicBoulder_01` × 1,6 (≈ 11 × 14 × 6,5 m) mit `MI_EL_SW_Landkartenflechte`, auf 3 Steinen
`SM_mountain_rock_small_01_1/_4` (sichtbare Fuge = „balanciert“, Fußsteine 30 % eingegraben). Rundhöcker-Platten
`SM_MassiveTundraRockFormation_02` (glatte Luvseite) + `SM_SmoothRockShelf_01`, `SM_ForestRockSlab_01` flach im Boden. Begleiter 2 –
`xisgcic_tier_0`, `skjsL_tier_0` (Erratiker), 3–4 – `texndcpda_tier_0`, `SM_TundraMossyBoulder_01`. Schutt 30–60 – Frostschutt an der
Leeseite (`SM_LichenedForestBoulder_01`). Kleinzeug – `SM_SmallStonesPack_10`. Bewuchs nach Ursache – windgefegter Gipfel:
Flechten (Lage Moos + Decal `MI_EL_SW_Flechte_Decal`), Polster aus `SM_heath_B_01`, `SM_heath_cross_01`, `SM_billberry_01`,
Tundragras `SM_wk2oaeyqx_VarA/E` in Rinnen, eine flach am Boden kriechende Zwergkiefer im Leeschatten des Blocks
(`SM_dwarf_pine_small_02`), Moos `SM_MossClump_02/05` nur an der Nordseite. Kontaktzone – Flechte kriecht 0,5 m am Block hoch.
**Wasser, Effekte, Licht:** keines. Der helle Block gegen den dunklen Hang ist das Licht.
**Geländeänderung:** Sockel +0,8 m (r 14 m), Fenster 54 × 54 m.
**Assets:** Bestand wie oben. Wunsch C: „Moss & Lichen Forest Ground Rock Materials“ (Rentierflechten-Matte), „Tundra Icelandic Rock
Cluster“ (Begleitblöcke). Abgrenzung: gletscher_08 „Gletscherschliff“ zeigt die geschliffene Wand – hier ist der **Block** der Held,
Schrammen nur angedeutet.
**Aufwand und Risiko:** gering–mittel. Risiko: Texeldichte bei ×1,6 → Prüfbild aus 10 m.
Budget: ~3 500 Instanzen (200 Kollision), 12 Akteure, 0 Lichter, 0 Niagara, 4 Decals.

### tundra_03_die_eiswand – Die Eiswand (Leuchtfeuer)

**Was man sieht:** An der Küste ist die Tundra aufgerissen: ein Halbrund von 100 m Breite, dessen Rückwand 8–10 m hoch aus gestreiftem
Eis und schwarzem Torf besteht. Oben hängt die Grasnarbe über wie ein Vordach, Soden sind abgekippt, aus dem Eis tropft es. Im Kessel
fließt grauer Schlamm in Zungen zum Strand; ein Rinnsal zieht vom Fuß der Wand durch die Mitte.
**Vorbild:** Rückschreitende Auftaurutschungen auf Herschel Island (Yukon) und Batagaika (Sibirien), Eiskeile von Duvanny Yar; Spiel:
Abbruchkanten der Sturmküste (DA:I), Velen-Lehmufer (The Witcher 3).
**Standort:** E3, X −530 / Y −1845 m, Boden 9,3 m. **Vorhandene** Hufeisen-Mulde (Boden 3–5 m) hinter einem 11 m hohen Küstenwall,
Hang bis 72° an der Seeseite; Wiese 48 %, Heide 27 %; Meer 34 m, Weg 195 m (Küstenweg Ost), 34 m innerhalb der Biomgrenze (Rechteck).
**Sicht:** Ziel 10 m: **87 von 159** Wegpunkten (Mittel 0,55), bis 699 m; `_fern` vom Gletscherweg X −578 / Y −2340 (497 m) – man blickt
von oben in die helle Wand.
**Komposition und Anmarsch:** Zugang 209 m über die Wiese, quert 8 m Rinnsal → **Pfad `tundra_pfad_die_eiswand` (Trampelpfad 110 m,
Trittsteine am Bach; letzte 92 m Trampelspur)**. `_held` 40 m südwestlich im Kessel, Blick nach Nordosten auf die Wand, Schlammzungen im Vordergrund.
**Detail-Ebenen:** Held – Kopfwand aus `uhprdg2fa_tier_0`, `veipbcmcb_tier_0`, `vdsrdd0fa_tier_0` (Ice Cliff, vorhanden) in Bändern,
dazwischen Torflagen `SM_beach_escarpment_01_A/B/C` mit `MI_EL_SW_Grundeis` im unteren Drittel. Begleiter 6–8 – Eiskeile als senkrechte
Keile (`uhpocesfa_tier_0`, `vd4hbizcb_tier_0`), abgekippte Sodenblöcke (`SM_MossyEmbankment_01/02`, `SM_GrassyEmbankment_01/02`).
Schutt 60–120 – Torfbrocken und Kiesel im Schlammfächer (`SM_ForestRockFormation_06`, `SM_TundraRockyGround_01`,
`SM_SmallStonesPack_03`), ein mitgerissener Fichtenstamm (`SM_FallenSpruceTree_01`, `SM_OldTreeBranch_02`). Kleinzeug –
Schmelzrinnen `SM_DryRiverBed_01/02`, Eiszapfen `SM_EISZAPFEN_3/4/7/9` unter dem Überhang, `xemmbh2qx_tier_0` Schneerest.
Bewuchs nach Ursache – oben intakte Tundra (`SM_wk2oaeyqx_VarD/H`), im Kessel nichts (frischer Schlamm), am Fächerrand erste
Polarweiden `SM_grey_willow_02` (Neubesiedlung). Kontaktzone – Lage Schlamm im Kessel, Nassband am Wandfuß (Decal, Coast & Dunes).
**Wasser, Effekte, Licht:** `bach` vom Wandfuß zum Strand (`versickert` im Fächer, `klar` → schlammig), Tropfen als Klang
(`CUE_Water_Stream_I_Cue`, `CUE_Rain_Dropping_on_various_textures_Cue`); Kaltdunst am Wandfuß `lokaler_nebel` (Dichte 0,04).
**Geländeänderung:** Kesselboden −2,5 m, Kopfwand-Fuß −3,5 m (Bogen), Durchbruch zum Strand −5 m; Fenster 138 × 128 m, nur Senkungen,
|Δ| ≤ 5,2 m, Wege/Wasser 0 m. Kesselboden bleibt > 0 m (kein Meer).
**Assets:** Bestand wie oben; Download B: „Arctic Cliffs“ (größere Eisplatten), „Coast & Dunes“ (Nass-/Lehmdecals, lädt Ferat gerade).
**Aufwand und Risiko:** hoch – die Wand muss geschichtet wirken (Eis/Torf/Gras), nicht wie Gletscher. Risiko Dopplung mit frost/gletscher
gering (dort kein Torf/Boden).
Budget: ~6 000 Instanzen (500 Kollision), 45 Akteure, 0 Lichter, 0 Niagara, 1 Nebel, 8 Decals.

### tundra_04_die_fliesstreppe – Die Fließtreppe (Leuchtfeuer)

**Was man sieht:** Ein sonniger Südwesthang ist zu einer Riesentreppe geworden: fünf grüne, zungenförmige Wülste aus Fließerde, jeder
15–30 m breit, schieben sich übereinander hangab; ihre Stirnen sind 1–1,5 m hohe Stufen, gesäumt von grauen Steinen. Oben im Hang liegt
ein Schneefleck in einer Mulde, von dem ein dünnes Rinnsal über die Stufen rieselt.
**Vorbild:** Solifluktionsloben in Ostgrönland, Abisko und auf Spitzbergen; Spiel: gestufte Grashänge der Frostgipfel (DA:I).
**Standort:** E2, X −450 / Y −2195 m, Boden 55,8 m. Hang 13,6° (Fenster 25 m: 13–16°), Exposition 213° (SSW), TPI100 −3,1 m,
Trockengras 73 %, Bach 52 m östlich. Weg 145 m (Gletscherweg Süd), 54 m im Biom.
**Sicht:** Ziel 12 m (Hangbild): **62 von 100** Wegpunkten (Mittel 0,60), bis 625 m; `_fern` vom Küstenweg X −842 / Y −1892 (495 m) – der
Hang liegt dem Weg frontal gegenüber.
**Komposition und Anmarsch:** Zugang 154 m ohne Pfadbau (max. 22,4°). `_held` unten links, Blick schräg hangauf: die Stufen staffeln sich
wie Terrassen, oben der Schneefleck als heller Punkt.
**Detail-Ebenen:** Held – die Lobenfolge (Gelände) + Stirnsäume aus `SM_GrassyEmbankment_01/02`, `SM_MossyEmbankment_01`. Begleiter 5 –
Stirnblöcke `SM_mountain_rock_big_01_1/_5`, `SM_ground_rock_02`. Schutt 80–150 – sortierte Steine an den Stirnen
(`SM_mountain_rock_small_01_2/_3`, `SM_TundraRockyGround_01`), Steinstreifen hangab zwischen den Loben. Kleinzeug – `SM_SmallStonesPack_12`.
Bewuchs nach Ursache – Loben-Oberseite trocken: `SM_heath_A_01`, `SM_lingonberry_01`, `SM_billberry_02`, Tundragras `SM_wk2oaeyqx_VarC/F`;
nasse Stirnfüße (Sickerwasser): Polarweide `SM_grey_willow_04`, Moos; eine Krüppelkiefer `SM_dwarf_pine_medium_01` am obersten Lobus.
Schneefleck: `vdspdazqa_tier_0` (Huge Snow Hill, flach) + `uhqffeyfa_tier_0`, `vctldcnfa_tier_0`, `xgxhcjxqx_tier_0`, `vcytca0fa_tier_0`
(alle vorhanden). Kontaktzone – Lage Erde an den Stirnen, Schnee mit Schmelzrand (Lage Schlamm).
**Wasser, Effekte, Licht:** `bach` vom Schneefleck über die Stufen (`klar`, 0,3 m breit, kleine Fälle an den Stirnen), Klang
`CUE_Water_Stream_III_Cue`. Optional Schneefahne (C, Niagara VFX Pack). Streiflicht von Westen betont die Stufen.
**Geländeänderung:** 5 Loben +1,3 m (Ellipsen 30 × 22 m), Nivationsmulde −1,5 m; Fenster 134 × 158 m, |Δ| ≤ 1,5 m, Wasser 0 m.
**Assets:** Bestand + Eis/Schnee (vorhanden). Kein Download nötig.
**Aufwand und Risiko:** mittel. Risiko: Loben zu flach im 2-m-Raster → in Phase 2 auf 1 m mit steiler Stirn (Profil ¼-Kosinus).
Budget: ~8 000 Instanzen (300 Kollision), 10 Akteure, 0 Lichter, 0 Niagara, 2 Decals.

### tundra_05_der_trunkene_grund – Der Trunkene Grund (Fundstück)

**Was man sieht:** Hinter dem Hügelrücken, im lichten Fichten-Lärchen-Saum, liegt ein brauner See ohne festes Ufer. Die Bäume rundum
stehen schief, als wären sie betrunken – manche lehnen 30° zur Seite, einige liegen tot im Wasser. Am Rand drei runde Torfbuckel
(Palsen), einer davon aufgebrochen: unter dem Moos glitzert Eis. Ein Abfluss sickert nach Osten.
**Vorbild:** „Drunken Forest“ an Thermokarstseen in Alaska und Jakutien; Palsenmoore in Lappland (Abisko); Spiel: Moorwälder in Velen
(The Witcher 3) – nur kälter.
**Standort:** D2, X −1355 / Y −2450 m, Boden 161,9 m. Nordschulter, flache Dellung (TPI100 −6,5 m, Relief 14 m), Wiese/Trockengras/Heide
je ~ ⅓, **193 Baumzellen** im 40-m-Radius (vorhandener Saum). Weg 280 m (Weg um Kharad-Vor, südlich über den Rücken), Stadtrand 234 m.
**Verdeckung:** Kern + 4 Proben (r 18 m), Ziel 1,5 m: **alle verdeckt**, 0 von 15–17 Wegpunkten ≤ 400 m sehen etwas (Rücken dazwischen).
**Komposition und Anmarsch:** **Pfad `tundra_pfad_der_trunkene_grund` (Serpentine 307 m, max. 26° → Kehren)** vom Weg westlich Kharad-Vor über
den Rücken; er endet 185 m vor dem See hinter der Kuppe (mit Pfad weiter 0 Sichtpunkte), die letzte Strecke ist Trampelspur –
der See öffnet sich erst an der Kante (Kamera `_anmarsch`). `_held` vom Westufer, Blick nach Osten durch zwei schiefe Stämme.
**Detail-Ebenen:** Held – See + Baumgruppe: `Fir_02_Small`, `Fir_03_Medium`, `SM_Forest_pine_01` mit Neigung 10–35° (Akteure, Richtung
zum See), tot im Wasser `Fir_08_Dead_NoBillboard`, `SM_Forest_pine_10_dead`, `SM_DeadTree_01`. Begleiter 3 – Palsen (Gelände) mit
Torfrändern `SM_MossyEmbankment_01/02`, Eiskern `vd4hbizcb_tier_0` (vorhanden). Schutt 30–60 – Treibholz und Wurzelteller
(`SM_FallenSpruceTree_01`, `SM_Forest_pine_04_log`, `SM_Pine_roots_01/03`, `SM_MossyForestRoots_01`, `SM_BirchTreeStump_01`).
Kleinzeug – `SM_OldTreeBranch_03`, `SM_branch_01_1`, Moos `SM_MossClump_01/04`, `SM_moss_01`. Bewuchs nach Ursache – Ufer nass:
Binsen `SM_ToadRush_00/010/014`, Polarweide `SM_grey_willow_02`; Palsen trocken (gehoben): `SM_billberry_01`, `SM_lingonberry_02`,
Jungfichten `Fir_01_Plant` (Jungwuchs auf dem Buckel). Kontaktzone – Torfkante unterspült, Nassband.
**Wasser, Effekte, Licht:** `see` 52 × 32 m, `moorbraun`, 2,5 m tief; Abfluss als `bach` nach Osten (`versickert`). Morgendunst
`lokaler_nebel` (Dichte 0,08, nur über dem Wasser). Klang `CUE_Water_Stream_V_Cue` leise. Lichtflecken durch die Kronen.
**Geländeänderung:** Seebecken −3 m (72 × 52 m), 3 Palsen +2,0…2,6 m, Abflussrinne −1,2 m; Fenster 146 × 98 m.
**Assets:** Bestand wie oben. Kein Download nötig.
**Aufwand und Risiko:** mittel. Risiko: Abgrenzung zu gletscher_04 Toteisloch (dort ohne Wald/Palsen) – bitte bestätigen.
Budget: ~9 000 Instanzen (700 Kollision), 40 Akteure, 0 Lichter, 0 Niagara, 1 Nebel, 4 Decals.

### tundra_06_das_schneetaelchen – Das Schneetälchen (Fundstück)

> **Verlegt wegen C2-Kaskade (Auftrag 14).** Das frühere *Aufeis* (C2, X −1760 / Y −2235) lag auf der unteren Erlenbach-Kaskade
> `F_ERLENBACH_1V_C2`, die Ferat schon gebaut hat (12 Stufen, Gischt). Koordinator: Die Kaskade bleibt. Flussab öffnet sich die
> Schlucht zur Ebene (Weg 59–70 m, 25–44 Wegpunkte mit Sicht), flussauf liegt der Bach offen neben dem Weg (5–13 Wegpunkte); eine
> andere Tundra-Schlucht mit Wasser, 80–300 m vom Weg und verdeckt, gibt es nicht. → **Aufeis gestrichen**, ersetzt durch ein
> Schneetälchen am Schneefeldrand; Pfad `tundra_pfad_das_aufeis` entfällt (Zugang 313 m, max. 14°, kein Pfad nötig).

**Was man sieht:** In einer Hangmulde am Rand des Schneefelds liegt mitten im Sommer ein schmutzig-weißer Altschneerest, rosa
geädert von Schneealgen. Wo er gestern noch lag, ist der Boden schwarz und nass; darum ein Ring aus daumenhohem Zwergweiden-Teppich
mit weißen Blütchen, außen Heide. Unter dem Schnee ein Wall aus Frostschutt, hinter dem sich ein Schmelzwassertümpel staut.
**Vorbild:** Schneetälchen (Salicetum herbaceae) in Lappland und Spitzbergen, Protalus-Wälle, Blutschnee (Chlamydomonas nivalis);
Spiel: späte Schneeflecken im Frostgipfel-Hochland (DA:I).
**Standort:** E3, X −182 / Y −1962 m, Boden 23,6 m. Hangmulde (TPI50 −2,6 m), Hang 8–15° nach SSW, Boden Schnee (Rand des
Frostgebiets, 34 m innerhalb der Biomgrenze); Weg 283 m (Weg Ost), ≥ 352 m zu Eiswand und Fließtreppe.
**Verdeckung:** 5/5 Proben verdeckt (0 von 20–22 Wegpunkten ≤ 400 m), heute wie mit Plan.
**Detail-Ebenen:** Held – Altschneerest `xgxhcjxqx_tier_0` ×1,5 mit `MI_EL_SW_Blutschnee`. Begleiter – Schneewehen `uhuldcyfa_tier_0`,
`Snow_Embankment_uhvifcgfa_High`, `xelnbaeqx_tier_0`, rosa Restschnee `vcytca0fa_tier_0`. Schutt – Protalus-Wall (`SM_TundraRockyGround_01`,
`SM_ground_rock_02`, `SM_mountain_rock_big_01_*`), Blöcke mit `MI_EL_SW_Altschnee`, Frostschutt. Kleinzeug – Schneehäufchen, dunkles
Schneetälchen-Moos, Grus. Bewuchs nach Ursache (Ausaperungszeit) – innen nackt/Moos, dann Zwergweide (`SM_grey_willow_01/02` flach),
Seggen (`SM_wk2oaeyqx_VarD/H/I`), weiße Blütchen (`SM_WhiteWindflower_*` ×0,3), außen Heide/Krähenbeere. Kontaktzone – Kiessaum,
Moos am Tümpel.
**Wasser, Effekte, Licht:** `see` Schmelzwassertümpel (klar, 0,6 m) hinter dem Wall, Abfluss versickert; Decals `MI_Deca_Wet`,
`MI_Decal_Clay_03`; Klang Rinnsal + Wind.
**Geländeänderung:** Nivationsmulde −1,5 m, Protalus-Wall +1 m (Lücke in der Mitte = Abfluss); max. 1,9 m.
**Aufwand und Risiko:** gering. Risiko: Abgrenzung zum Schneefleck der Fließtreppe (dort Nebenrolle, hier Thema: Ausaperung und
Pflanzenzonen).

### tundra_07_die_steinringe – Die Steinringe (Fundstück)

**Was man sieht:** Auf einer Kiesterrasse über dem Strand liegen zwanzig Ringe aus Steinen, 2–4 m im Durchmesser, so regelmäßig, als
hätte sie jemand gelegt – doch es ist der Frost, der die groben Steine nach außen schiebt. In den Ringmitten feiner grauer Grus, an den
Rändern Rentierflechte und Moos. Dahinter ein Wall aus groben Blöcken, vom Meereis aufgeschoben.
**Vorbild:** Sortierte Steinkreise von Kvadehuken (Spitzbergen); Eisschubwälle an arktischen Stränden; Spiel: keines – das ist neu.
**Standort:** D3, X −1412 / Y −1630 m, Boden 4,5 m. Kiesterrasse (Kies 38 %, flach 5°), Meer 34 m, Weg 93 m (Weg West),
Stadtrand Aufstiegsweg 156 m, 34 m im Biom.
**Verdeckung (ehrlich):** Die Terrasse ist der höchste Punkt zwischen Lagune und Strand; ein Rahmen wirkt deshalb nur teilweise.
Mit Eisschubwall (+2,6 m): Kern von **18 von 81** Wegpunkten ≤ 400 m einsehbar (nächster 115 m, Weg West 10 m höher), Ostprobe 28,
Westprobe 6, Nordprobe 1 (Anteil 0,56). Die meisten Sichtlinien kommen vom 15–20 m höheren Küstenweg in 250–400 m – dort ist die Fläche
ein grauer Fleck, die 0,3 m hohen Ringe sind erst unter ~60 m lesbar. Ziel 0,3 m: 15 von 81. **Als Fundstück vertretbar, aber kein
perfektes Versteck** – Alternative wäre Art „leuchtfeuer“ (Ferat).
**Komposition und Anmarsch:** Zugang 98 m (max. 13,7°) über den Kiesrücken. `_held` von Süden auf der Terrasse: Ringe im Vordergrund,
Wall dahinter, darüber der Hang.
**Detail-Ebenen:** Held – Ringfeld (Phase 2 per Skript: Voronoi, Steine nach Größe sortiert) aus `SM_mountain_rock_small_01_1/_2/_5`,
`SM_stones_01_1/_3/_6`, `SM_NordicBeachRock_01`. Begleiter 6 – Wallblöcke `SM_NordicBoulder_01` (×0,5), `SM_TundraMossyBoulder_01`,
`SM_NordicBeachRocks_01`, `pjEr1_tier_0`, `pkeeM_tier_0`. Schutt 150–200 – Ringsteine. Kleinzeug – Grus und Kiesel
(`SM_BeachSandWithPebbles_01/02`, `SM_NordicBeachRockyGround_01`, `SM_SmallStonesPack_01/07/14`). Bewuchs nach Ursache – Ringmitten
kahl (Frosthub), Ringränder: Flechte (`MI_EL_SW_Flechte_Decal`), `SM_MossClump_02/05`, `SM_heath_cross_01`, Tundragras
`SM_wk2oaeyqx_VarA/I` nur in den Fugen. Kontaktzone – Blöcke 35 % eingegraben, Flechten auf den Oberseiten (`MI_EL_SW_Landkartenflechte`).
**Wasser, Effekte, Licht:** keines; Brandung als Klang. Tiefe Sonne wirft lange Schatten der Ringsteine.
**Geländeänderung:** Terrasse eingeebnet auf 3,8 m (r 16 m), Eisschubwall +2,6 m (Hufeisen, offen zum Meer); Fenster 78 × 76 m.
**Assets:** Bestand; Wunsch C „Megascans Icelandic Sand With Pebbles“, „Moss & Lichen …“. Abgrenzung fjord_08 „Die alten Ufer“
(Strandterrassen als Form) – hier ist die **Frostmusterung** das Thema.
**Aufwand und Risiko:** mittel (Skript für Ringe). Risiko siehe Verdeckung.
Budget: ~7 000 Instanzen (600 Kollision), 8 Akteure, 0 Lichter, 0 Niagara, 6 Decals.

### tundra_08_das_wabenmoor – Das Wabenmoor (Fundstück)

**Was man sieht:** Unten an der Flussmündung, im Schutz des Steilufers, ist der Boden in Waben zerlegt: sechseckige Felder von 9–12 m,
jedes mit einem erhöhten Rand aus Moos und Seggen und einem dunklen Tümpel in der Mitte; dazwischen nasse Gräben. Von oben sähe es aus wie
ein Bienenwabenmuster – vom Rand aus sieht man Spiegel neben Spiegel.
**Vorbild:** Eiskeil-Polygone im Lena-Delta und bei Barrow (Alaska); Spiel: keines.
**Standort:** D3, X −924 / Y −1738 m, Boden 5,0 m. Uferterrasse an der Flussmündung (Wasser 30 m, Meer 35 m), Wiese 41 %, Heide 24 %,
Kies 17 %. Weg 104 m (Küstenweg), 36 m im Biom.
**Verdeckung:** ohne Pfade Kern **3 von 80** Wegpunkten (max. Anteil 0,25), West- und Nordprobe verdeckt, Ost/Süd-Proben vom höheren
Küstenweg sichtbar (9 bzw. 20, nächster 127 m); mit Pfaden Kern 5 von 86 (0,82), Ost 15, Süd 26. Rahmen: Uferweiden-Saum 2,5 m auf der Böschungskante (geplant, als 4-m-Baumzellen gerechnet).
**Komposition und Anmarsch:** Zugang 108 m ohne Pfadbau (max. 23°) durch die Böschung; die Waben zeigen sich erst von der Kante.
`_held` auf der Böschung Nordost, Blick schräg über die Waben zur Mündung.
**Detail-Ebenen:** Held – Wabenfeld (Phase 2: Voronoi auf 1 m, Rand +0,4 m, Mitte −0,3 m). Begleiter – 9 Tümpel. Schutt –
Torfstücke an den Grabenrändern (`SM_MossyEmbankment_01/02`, `SM_GrassyEmbankment_01`). Kleinzeug – `SM_branch_01_1`, Moos
`SM_MossClump_01/04`, `SM_moss_02`. Bewuchs nach Ursache – Ränder trocken: Tundragras `SM_wk2oaeyqx_VarD/H/I`; Gräben/Tümpel nass:
Binsen `SM_ToadRush_00/01/010/013/015`, Wollgras-Ersatz (Lücke, s. `asset_bedarf.json`); Böschung: Polarweiden
`SM_grey_willow_01…04` (= Rahmen). Kontaktzone – Nassband an jedem Tümpel.
**Wasser, Effekte, Licht:** 6–9 kleine `see` (je 2–4 m, `schwarz_spiegel`, 0,5 m tief) – die Spiegel sind der Effekt; Klang
`CUE_Water_Stream_II_Cue`. Optional Mückenschwarm (eigenes Niagara, C).
**Geländeänderung:** Terrasse auf 4,8 m eingeebnet (r 16 m), Fenster 98 × 92 m, |Δ| ≤ 4,6 m (Böschungsanschnitt), Fluss 0 m.
**Assets:** Bestand; Download B „Coast & Dunes“ (Nassband-Decals, lädt Ferat gerade).
**Aufwand und Risiko:** mittel; Risiko: viele kleine Wasserflächen (Epic-Water-Kosten) → evtl. Wasser-Decal statt `see`.
Budget: ~6 000 Instanzen (200 Kollision), 0 Akteure, 0 Lichter, 0 Niagara, 9 Wasser, 8 Decals.

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/heide/katalog.md](sehens/heide/katalog.md)

### heide_01_die_graue_burg – Die Graue Burg (Leuchtfeuer)

**Was man sieht:** Auf der Kuppe über zwei Bächen türmen sich graue Granitplatten zu drei Stapeln, der höchste 11 m: waagerecht
geklüftet, die Kanten zu Wollsäcken gerundet, als hätte ein Riese Kissen gestapelt. Hangab ein Meer aus abgestürzten Blöcken (Clitter),
zwischen dem Heidekraut und Farn wachsen; am Fuß eine vom Wind geduckte Eberesche.
**Vorbild:** Haytor und Hound Tor (Dartmoor), Wollsackverwitterung im Fichtelgebirge (Luisenburg); Spiel: Felskuppen in Toussaint
(The Witcher 3), Fallow Mire/Hinterland-Tore (DA:I).
**Standort:** F5, X 1310 / Y 466 m, Boden 22,3 m. Kuppe TPI100 **+13,9 m**, TPI25 +8,5 m, vorhandene Felsplatten 22 %, Heide 27 %,
Moos 26 %. Weg 84 m, Bach 37 m.
**Sicht:** Ziel 12 m: **119 von 183** Wegpunkten (Mittel 0,63), bis 795 m – der beste Leuchtturm der Heide; `_fern` von X 1598 / Y 56 (501 m).
**Komposition und Anmarsch:** Zugang 108 m (max. 24,6°) über den Clitter. `_held` von Südwest: Blockschutt und Heide im Vordergrund,
Haupttor als Silhouette, Nebenstapel staffeln nach rechts.
**Detail-Ebenen:** Held – Haupt-Tor aus `SM_flat_rock_02/03/04` und `SM_big_rock_wall_01/02/03` horizontal gestapelt (versetzt, Fugen
mit Moos), Kappe `SM_mountain_rock_big_02_6`; alles `MI_EL_SW_Granit_Heide`. Begleiter 2 Stapel (7 m, 5 m) aus
`SM_mountain_rock_big_02_1/_4/_8`, `SM_Big_Rock_01/02/03`. Schutt 80–150 – Clitter hangab (`SM_Middle_Rock_01`, `SM_Rock_01/03/05`,
Granit `pjEr1_tier_0`, `pjtsT_tier_0`, `pkeeM_tier_0`, `xf3odif_tier_0`, `xfplcbf_tier_0`), groß unten, klein oben (Ursache: Abbrechen der
Klüfte). Kleinzeug – `SM_s_rock_01/02`, Grus (Lage Kies). Bewuchs nach Ursache – Clitterfugen: Besenheide `SM_forest_heather_01`,
`SM_forest_heather_simple_01`, Heidelbeere `SM_billberry_01/03`, Adlerfarn `SM_EagleFern_M_01`, `SM_EagleFern_S_02`; Windflüchter:
`SM_pine_beach_crooked_02` und eine Birke `Big_Tree_Birch_01` (×0,6) im Lee; Krüppelkiefer `SM_dwarf_pine_medium_02` in einer Kluft.
Kontaktzone – Platten 30 % eingegraben, Moospolster `SM_MossClump_03` auf den Absätzen.
**Wasser, Effekte, Licht:** kein Wasser. Felsschüsseln auf dem Gipfelstapel mit Regenwasser (Decal). Abendlicht von Westen auf grauem Fels.
**Geländeänderung:** Kuppe +2 m (r 26 m), Fenster 78 × 78 m.
**Assets:** Bestand reicht. Wunsch B „Brushify – Moorlands Pack“ (UK-Granit + Heidekraut, neu, siehe `asset_bedarf.json`).
**Aufwand und Risiko:** mittel. Risiko: Stapel wirkt gemauert → Platten verkippen (2–6°), Fugen ungleich, Kanten gerundet.
Budget: ~6 000 Instanzen (900 Kollision), 45 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

### heide_02_ginstergold – Ginstergold (Leuchtfeuer)

**Was man sieht:** Ein ganzer Osthang am Rand des Birkenwalds glüht gelb: dichte Ginsterbüsche in voller Blüte, dazwischen ein purpurner
Saum aus blühender Besenheide. Ein grauer Granitblock trägt einen Kranz aus Ginster. An einer Stelle verkohlte Stummel – ein alter
Heidebrand, aus dem junger Ginster schießt.
**Vorbild:** Ginsterheiden der Bretagne und von Exmoor im Mai; Lüneburger Heide im August (Erika); Spiel: Blütenfelder in Toussaint
(The Witcher 3), Farbtupfer-Wiesen der Smaragdgräber (DA:I).
**Standort:** G5, X 2295 / Y 610 m, Boden 19,7 m. Lichtung am Waldrand (Laub 49 %, Gras 35 %, Schlamm 16 %), Hang 11°, 58 m im Biom.
Weg 155 m; nach Verschiebung 352 m zu dschungel_02.
**Sicht:** Ziel 4 m (Strauchhöhe + Farbfläche): **38 von 252** Wegpunkten (Mittel 0,15), bis 702 m; `_fern` vom Rückenweg X 2086 /
Y 156 (500 m) – der Hang liegt dem Weg frontal gegenüber. Leuchtfeuer durch **Farbe**, nicht Höhe (ehrlich: schwächstes Leuchtfeuer).
**Komposition und Anmarsch:** Zugang 160 m (max. 11,7°). `_held` von Südwest, Blick hangauf: Ginstermasse, Granitblock, dahinter
dunkler Birkenwald als Kontrast.
**Detail-Ebenen:** Held – Granitblock `SM_mountain_rock_big_02_3` + `pkeeM_tier_0`. Begleiter 30–50 Ginsterbüsche (Lücke →
`SM_sea_buckthorn_01/02/03/05` mit `MI_EL_SW_Ginster`, Blüten aus `SM_flower_goldenrod_01/02`, `SM_flower_common_Saint_John_s_wort_01`,
`SM_YellowArchangel_04/08`, `SM_Crownbeard_03/07` in Clustern). Schutt – Brandfläche: `SM_BirchTreeStump_01`, verkohlte Zweige
`SM_branch_01_1` (Ruß-Decal). Bewuchs nach Ursache – Ginster nur auf dem trockenen Oberhang (Sonne), Erika-Saum unten
(`SM_forest_heather_01`, `SM_heath_A_01/B_01` mit `MI_EL_SW_Erika_Bluete`), trockenes Gras `SM_dead_grass_01/02`, `SM_grass_bush_02`,
Jungginster auf der Brandfläche. Kontaktzone – Lage Trockengras/Heide, Gelb als GPU-Gras (Kraut) dazwischen.
**Wasser, Effekte, Licht:** keines; Insektensummen als Klang (Vögel-CUE prüfen). Gegenlicht macht das Gelb hell.
**Geländeänderung:** keine.
**Assets:** Lücke Ginster/Stechginster (kein Fab-Listing gefunden) → Ersatz wie oben; B „Brushify – Moorlands Pack“ für Erika.
**Aufwand und Risiko:** mittel; Risiko: Sanddorn-Ersatz wirkt nicht wie Ginster → Prüfbild, ggf. CGTrader-Modell (Ferat entscheidet).
Budget: ~12 000 Instanzen (300 Kollision), 4 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

### heide_03_die_wacholderprozession – Die Wacholderprozession (Leuchtfeuer)

**Was man sieht:** Über einen flachen Rücken zieht sich eine Reihe dunkler, säulenförmiger Wacholder – 45 Gestalten von 3 bis 7 m, alle
in dieselbe Richtung, wie eine Prozession von Mönchen auf dem Weg nach Nordosten. In der Mitte ein silbergrauer, abgestorbener Wacholder,
am Ende ein einzelner Findling.
**Vorbild:** Wacholderheiden Lüneburger Heide (Totengrund, Wilsede), Haselünner Wacholderhain; Spiel: Silhouettenbäume im Hinterland (DA:I).
**Standort:** G4, X 1890 / Y −80 m, Boden 25,5 m. Flacher Rücken (Hang 2,6°, Ebene), Trockengras 69 %, 16 Baumzellen (lichter Saum).
Weg 198 m; 381 m zu elfenwald_06.
**Sicht:** Ziel 6 m: **82 von 328** Wegpunkten (Mittel 0,19), bis 800 m; mit dem 1,2-m-Rücken (Stempel) 12 Wegpunkte mehr als heute;
`_fern` vom Rückenweg X 1986 / Y 340 (431 m).
**Komposition und Anmarsch:** Zugang 212 m (max. 17,2°). `_held` vom Osten auf Augenhöhe gegen den Himmel: die Säulen als dunkle Figuren.
**Detail-Ebenen:** Held – Totwacholder `SM_DeadTree_02` (×0,8, silbergrau). Begleiter 45 Säulen (Lücke Wacholder → `SM_Forest_pine_plant_01/02/03`,
`Fir_01_Plant`, `Fir_02_Small` nicht-uniform skaliert sx = sy 0,45–0,6, sz 1,1–1,5, `MI_EL_SW_Wacholder`), dazu `SM_dwarf_pine_big_01/02` als
niedrige Wacholderbüsche; `SM_Forest_pine_10_dead` liegend. Findling `SM_NordicBoulder_01` (×0,5), `SM_Rock_02`. Kleinzeug –
`SM_branch_01_1`, `SM_dead_grass_03`. Bewuchs nach Ursache – Lichtung mit Besenheide (`SM_forest_heather_01`, `SM_heath_cross_01`), trockene
Horste `SM_grass_bush_01`, Adlerfarn `SM_EagleFern_S_01` im Halbschatten. Kontaktzone – Nadelstreu (Lage Nadeln) unter jeder Säule.
**Wasser, Effekte, Licht:** keines. Wind (`CUE_Wind_Autumn_wind_with_leaves_rustling_Cue`).
**Geländeänderung:** sanfter Rücken +1,2 m entlang der Prozession (Fenster 170 × 144 m).
**Assets:** Lücke Wacholder (kein Fab-Listing) → Ersatz; B „Brushify – Moorlands“ für Bodendecker.
**Aufwand und Risiko:** mittel; Risiko: Säulenform aus Kiefer-Jungpflanzen → Prüfbild entscheidet.
Budget: ~5 000 Instanzen (100 Kollision), 50 Akteure, 0 Lichter, 0 Niagara, 0 Decals.

### heide_04_der_kolk – Der Kolk (Fundstück)

**Was man sieht:** Hinter einem Kranz aus Granitplatten und Krüppelkiefern wölbt sich ein Hochmoor, rot-grün gesprenkelt von Torfmoos-
Bulten. In seiner Mitte liegt ein kreisrundes, schwarzes Wasserauge, so glatt, dass sich die Wolken darin spiegeln. Silberne
Birkenskelette stehen am Rand, Wollgras weht.
**Vorbild:** Hochmoor-Kolke im Pietzmoor (Lüneburger Heide) und auf Dartmoor (Fox Tor Mires); Spiel: Moorauge im Wald von Crookback Bog
(The Witcher 3) – hier ohne Ruine.
**Standort:** G5, X 1790 / Y 595 m, Boden 16,7 m. **Vorhandene** ovale Mulde (Schlamm 99 %, flach 1°) mit Felsrahmen im Westen/Süden
(Rand 21–24 m). Weg 205 m.
**Verdeckung:** mit Moorkuppe, Felsrahmen (+1,5 m im Nordosten) und Krüppelkiefernsaum (3,5 m): **alle 5 Proben verdeckt**
(max. Anteil 0,13 bei 115–122 Wegpunkten ≤ 400 m); heute 4 Wegpunkte mit Sicht (282 m).
**Komposition und Anmarsch:** Zugang 221 m (max. 19°) von Süden durch eine Lücke im Felsrahmen – erst dort öffnet sich das Wasserauge.
`_held` auf dem Südrand, Blick nach Norden über die Bulten auf den Kolk.
**Detail-Ebenen:** Held – Kolk (Wasser). Begleiter – Krüppelkiefern `SM_dwarf_pine_small_01/02`, `SM_dwarf_pine_medium_01/03`,
`SM_pine_beach_short_01/02`, Birkenskelette `SM_DeadTree_01`, `SM_BirchTreeStump_01`. Schutt – Felsplatten `SM_flat_rock_03`,
`SM_MossyRocks_01` am Rahmen. Kleinzeug – `SM_branch_01_1`, Torfmoos `SM_MossClump_01/02/05`, `SM_moss_01/02`. Bewuchs nach Ursache –
Bulten trocken: `SM_heath_A_01`, `SM_lingonberry_01`, `SM_billberry_dry_01`; Schlenken nass: Binsen `SM_ToadRush_00/010/014`
(Wollgras-Lücke). Kontaktzone – Kolkrand schwingend (Moos bis an die Wasserlinie, kein Kies), Nassband.
**Wasser, Effekte, Licht:** `see` 22 × 16 m, `schwarz_spiegel`, 2,5 m tief; Bodennebel `lokaler_nebel` (0,05) in der Mulde; Klang
`CUE_Water_Stream_IV_Cue` sehr leise. Spiegelung ist das Bild.
**Geländeänderung:** Moorkuppe +1,2 m (100 × 80 m), Kolk −2,5 m, Felsrahmen NO +1,5 m; Fenster 140 × 134 m.
**Assets:** Bestand; B „Brushify – Moorlands“ (Heide auf Bulten). Seerose bewusst nicht (Hochmoor nährstoffarm).
**Aufwand und Risiko:** gering–mittel.
Budget: ~7 000 Instanzen (300 Kollision), 15 Akteure, 0 Lichter, 0 Niagara, 1 Nebel, 4 Decals.

### heide_05_der_wackelstein – Der Wackelstein (Fundstück)

**Was man sieht:** Zwischen den Granitplatten des Rückens führt ein Durchschlupf in einen runden Felsenkessel, ummauert von
Wollsäcken. In der Mitte ruht ein 4,5 m großer, gerundeter Block auf einer einzigen Kippkante – man meint, ein Stoß würde ihn wiegen.
Auf einem Nachbarstein eine Felsschüssel voller Regenwasser.
**Vorbild:** Logan Rock (Cornwall), Wackelsteine im Fichtelgebirge; Opferkessel (Verwitterungsschüsseln) im Granit; Spiel: Rätselsteine
in Skellige.
**Standort:** G5, X 2095 / Y 320 m, Boden 24,1 m. Südostflanke des Granitrückens (Felsplatte 14 %, Plattenfeld vorhanden), Weg 93 m.
**Verdeckung:** Kessel −3,2 m mit Wollsack-Kranz +2,2 m: **Kern und 3 Proben verdeckt**; Ostprobe am Kesselrand von 14 Wegpunkten im
Tiefland Ost (340–370 m, Anteil ≤ 0,60) sichtbar. Heute 18 Wegpunkte, nächster 85 m.
**Komposition und Anmarsch:** Zugang 98 m (max. 16,8°) über den Durchschlupf Südwest. `_held` aus dem Durchschlupf: Rahmen aus Fels links
und rechts, Wackelstein in der Mitte.
**Detail-Ebenen:** Held – `SM_mountain_rock_big_02_5` (gerundet) auf `SM_flat_rock_04`, Kippkante sichtbar. Begleiter 8–12 Kranzblöcke
`SM_mountain_rock_big_02_2/_7`, `SM_Big_Rock_01/02`, `SM_ground_rock_03_03`, `pjEr1_tier_0`, `pjtsT_tier_0`. Schutt 40–80 – `SM_Rock_04/06/07`,
`SM_s_rock_03`. Bewuchs nach Ursache – Kesselboden geschützt: Heidelbeere `SM_billberry_02`, Besenheide `SM_forest_heather_simple_01`,
Farn `SM_EagleFern_S_04`, Weide `SM_grey_willow_03` am Wasser der Schüssel; Moos `SM_MossClump_04` auf der Nordseite.
Kontaktzone – Grus (Lage Kies) am Fuß jedes Blocks.
**Wasser, Effekte, Licht:** Felsschüssel als Decal + kleine `see` (1,5 m, `klar`). Kessel im Schatten, der Wackelstein im Licht.
**Geländeänderung:** Kessel −3,2 m (r 13 m), Kranz +2,2 m (Ring r 17 m); Fenster 70 × 70 m.
**Assets:** Bestand; B „Brushify – Moorlands“ (UK-Granit).
**Aufwand und Risiko:** gering.
Budget: ~3 000 Instanzen (500 Kollision), 20 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

### heide_06_der_wollsackfall – Der Wollsackfall (Fundstück)

**Was man sieht:** Neben einer 5 m hohen Granitrippe hat sich der Heidebach eine schmale Klamm gegraben. Über drei Stufen aus gerundeten
Wollsäcken fällt er insgesamt 4 m in eine klare Gumpe; Gischt netzt Farne und Moos, eine Eberesche hängt über dem Kopf der Klamm.
**Vorbild:** Becky Falls und Lydford (Dartmoor), Bachkaskaden im Fichtelgebirge (Egerquelle); Spiel: Waldbäche in Velen (The Witcher 3).
**Standort:** G5, X 1498 / Y 165 m (Kern = Fallstufe X 1476 / Y 160), Boden 18,9 m. Vorhandene N-S-Felsrippe (4–5 m) neben dem Bach
(Gefälle 19 → 13 m auf 130 m), Weg 115 m.
**Verdeckung:** Klamm −3,5 m + Wollsack-Ufer West +1,8 m + Ebereschen am Klammkopf, Erlen am Ausgang: **Kern, Süd- und Nordprobe
verdeckt**, Westprobe 1 Wegpunkt (0,28); Ostprobe auf der Rippenkante 40 Wegpunkte (die Rippe selbst ist heute schon sichtbar).
**Komposition und Anmarsch:** Zugang 130 m vom Weg Nord ohne Pfadbau (max. 31,7° nur auf 4 m am Klammrand → 5–6 Steinstufen
`SM_flat_rock_03` als Instanzen, kein Pfad nötig). `_held` von unten auf der Kiesbank, Blick bachauf auf die drei Stufen.
**Detail-Ebenen:** Held – Fallstufen aus `SM_mountain_rock_big_02_1/_6`, `SM_Big_Rock_03` quer im Bett. Begleiter 5–8 – Wollsäcke
`SM_Middle_Rock_01`, `SM_Rock_01/05`, `SM_MossyForestBoulder_04`, `SM_MossyForestRock_02`. Schutt 60–100 – Bachkiesel `SM_stones_01_2/_4`,
`SM_DryRiverBed_01`. Kleinzeug – Laub `SM_detail_leaves_02`, Wurzeln `SM_Pine_roots_02`. Bewuchs nach Ursache – Spritzzone: Farne
`SM_Fern_02`, `SM_SilverLadyFern_01`, Moos `SM_MossClump_01/03`; Klammkopf: Eberesche-Ersatz `Big_Tree_Birch_01`, `SM_beech_tree_00_B`;
Rand: Adlerfarn `SM_EagleFern_M_01`. Kontaktzone – Nassband, Moos auf allen bachseitigen Steinflanken.
**Wasser, Effekte, Licht:** vorhandener Bach (Ort IST dieses Wasser) mit 3 Stufen > 0,8 m → kleine Wasserfälle; `see` Gumpe 12 × 9 m
`klar`; Schaum am Fuß; Klang `CUE_Water_Stream_IX_Cue`/`_X_Cue`. Lichtfleck durch die Ebereschenkrone.
**Geländeänderung:** Klamm −3,5 m (Band 16 m, 100 m lang), Gumpe −1,5 m, Ufer West +1,8 m; Fenster 78 × 136 m; |Δ| an Wasser 4,6 m (erlaubt).
**Assets:** Download A „Mountain – Environment Set“ (Wasserfallmaterial, lädt Ferat gerade); Ersatz `M_EL_Wasserfall2`.
**Aufwand und Risiko:** mittel–hoch (Wasser + Gelände).
Budget: ~6 000 Instanzen (600 Kollision), 25 Akteure, 0 Lichter, 1 Niagara (Gischt, optional), 4 Decals.

### heide_07_der_totengrund – Der Totengrund (Fundstück)

**Was man sieht:** Hinter einer Hangkante öffnet sich ein runder, 4 m tiefer Kessel, dessen Hänge vollständig mit blühender Besenheide
bedeckt sind – ein purpurner Trichter. Auf dem sandigen Grund silbernes Gras, drei dunkle Wacholder stehen wie Wächter, ein Birkensaum
umrahmt den Rand. Nach Nordwesten läuft ein trockenes Tälchen aus.
**Vorbild:** Totengrund bei Wilsede (Lüneburger Heide) – periglaziale Nivationsmulde; Spiel: versteckte Lichtungen in den Smaragdgräbern (DA:I).
**Standort:** F4, X 1310 / Y −135 m, Boden 21,2 m. Hangfuß unter dem Birkensaum (Heide 37 %, Trockengras 35 %, 39 Baumzellen),
Hang 13°. Weg 85 m; 352 m zu aue_08 (nach Verschiebung).
**Verdeckung:** Kessel −4 m, Westrand +3 m, Auslauf nach NW: **Kern, West- und Südprobe verdeckt**; Ost-/Nordprobe am Kesselhang von 3 bzw. 7
Wegpunkten (Anteil ≤ 0,62/1,0, 138–146 m, Weg West, tiefer) einsehbar. Heute 13 Wegpunkte.
**Komposition und Anmarsch:** Zugang 89 m (max. 21°) über den Rand – der Kessel erscheint plötzlich unter den Füßen. `_held` vom Ostrand
in den Trichter, Wacholder als Maßstab.
**Detail-Ebenen:** Held – Kessel (Gelände) + drei Wacholder (Ersatz `SM_Forest_pine_plant_02/03`, `MI_EL_SW_Wacholder`). Begleiter –
`SM_DeadTree_02` (Totholz), Birken `Big_Tree_Birch_01` am Rand. Schutt – Sandabbrüche am Kesselrand `SM_sandy_slope_01/03`, Steine
`SM_Rock_02`, `SM_s_rock_02`. Kleinzeug – `SM_branch_01_1`, Silbergras `SM_beach_grass_02_1/_3`, `SM_dead_grass_01`. Bewuchs nach Ursache –
Hänge Besenheide (`SM_forest_heather_01`, `SM_forest_heather_simple_01`, `SM_heath_A/B_01`, `SM_heath_cross_01` mit `MI_EL_SW_Erika_Bluete`),
Grund Sand (Lage Sand) mit Silbergras, Heidelbeere `SM_billberry_03` im Schatten der Birken. Kontaktzone – Sandrand mit Wurzeln.
**Wasser, Effekte, Licht:** keines; Stille (Wind gedämpft). Der Kessel fängt Abendlicht, der Rand bleibt dunkel.
**Geländeänderung:** Kessel −4 m (68 × 56 m), Westrand +3 m, Auslauf −1,2 m; Fenster 102 × 122 m.
**Assets:** Lücke Wacholder; B „Brushify – Moorlands“ (blühende Heide).
**Aufwand und Risiko:** gering–mittel.
Budget: ~10 000 Instanzen (100 Kollision), 6 Akteure, 0 Lichter, 0 Niagara, 0 Decals.

### heide_08_die_windkante – Die Windkante (Fundstück)

**Was man sieht:** Am Westrand der Heide, wo der Seewind auf das Land trifft, hat der Sand eine hufeisenförmige Düne aufgeworfen, 4 m hoch,
die Arme zum Meer gestreckt. In ihrem Innern ein ausgeblasener Kessel aus hellem Sand mit Rippelmarken; an der Kante stehen
windgekrümmte Kiefern, deren Wurzeln frei in der Luft hängen. Auf dem Sandboden blankgeschliffene Windkanter.
**Vorbild:** Parabeldünen und Windanrisse im Hohen Venn/Lieberoser Heide, Kiefern-Windflüchter auf Sylt; Spiel: Sturmküste (DA:I).
**Standort:** F5, X 985 / Y 330 m, Boden 1,6 m. Küsten-Geröllflur (Geröll 61 %, Wiese 31 %) 82 m vom Meer, flach. Weg 111 m.
**Verdeckung:** Parabeldüne (+4 m, offen nach Westen): **alle 5 Proben verdeckt**, max. Anteil 0,28 von 1 Wegpunkt (Westprobe, 120 m);
heute 40 Wegpunkte.
**Komposition und Anmarsch:** Zugang 122 m (max. 11,6°) über den Dünenarm; `_held` auf dem Kamm Ost, Blick in den Kessel und durch die
offene Westseite aufs Meer.
**Detail-Ebenen:** Held – Windkiefern `SM_pine_beach_crooked_01/02` an der Abbruchkante mit freigelegten Wurzeln (`SM_stones_roots_01/03`,
`SM_Pine_roots_01`, `SM_crooked_root_01`). Begleiter – `SM_pine_beach_medium_01/03`, `SM_pine_beach_small_04`. Schutt – Sandabbrüche
`SM_sandy_slope_02/04/05`, `SM_scarp_01`; Windkanter `SM_namaqualand_rocks_01_a_NN`, Kiesel `SM_BeachSandWithPebbles_01`. Kleinzeug –
`SM_branch_01_1`. Bewuchs nach Ursache – Kessel kahl (Wind), Dünenkamm Strandhafer `SM_beach_grass_01_1`, `SM_beach_grass_01_hp_1`,
`SM_beach_grass_03_2`, Leeseite Heide `SM_forest_heather_simple_01`, Stranddistel `SM_sea_holly_01`. Kontaktzone – Lage Sand, Rippel-Decal.
**Wasser, Effekte, Licht:** keines; Sandfahnen optional (C). Wind-Klang. Grelles Licht auf hellem Sand.
**Geländeänderung:** Parabeldüne +4 m (Kamm 9 m breit), Fenster 114 × 126 m; nichts unter 0 m.
**Assets:** Download A „Coast & Dunes“ (Dünenstempel, Sand-Decals – lädt Ferat gerade); sonst Bestand. Abgrenzung kueste: dort Brandung/
Fels; hier Sandheide mit Kiefern.
**Aufwand und Risiko:** gering–mittel.
Budget: ~6 000 Instanzen (200 Kollision), 15 Akteure, 0 Lichter, 0 Niagara, 4 Decals.

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/kueste/katalog.md](sehens/kueste/katalog.md)

### 1 · Die Alten (`kueste_01_die_alten`) – Leuchtfeuer · Klippensteig

**Was man sieht.** Vor dem Kliff stehen zwei Granitpfeiler im Meer, der größere 45 m hoch, schmal, oben mit einem Schopf aus Grasnelken
und Strandmelde, der kleinere 26 m, schief, als hätte er sich zum Großen gebeugt. Dazwischen drei Stümpfe – Pfeiler, die schon gefallen
sind –, um die das Wasser milchig schäumt. Das untere Drittel jeder Säule ist schwarz von Tang und Seepocken, darüber weiße Kotstreifen
der Möwen. Bei jeder Welle zieht ein Schaumring um die Füße.

**Leuchtfeuer.** Silhouette 40 m: vom Klippensteig aus 97 von 131 Punkten im Ring 300–800 m lesbar (Mittel 0,73), weiteste 726 m; der
Spieler sieht die Pfeiler schon aus der Strandebene und dann bei jeder Kehre des Kliffwegs wieder.

**Vorbild.** Real: Old Man of Hoy (Orkney), Zwölf Apostel (Victoria), Reynisdrangar. Spiel: die Seestacks vor Skellige (Witcher 3),
Kliffküste in Ghost of Tsushima (Iki).

**Standort.** Feld A5, X −4010 / Y 872, Boden 47,8 m: Kopf des 624-m²-Inselchens, das im Höhenfeld bereits als 48-m-Säule steht
(TPI25 +49,5 m, TPI100 +62 m, Flanke bis 85°); Begleitpfeiler 140 m südöstlich (−3937/753, 17,6 m). 160 m vor dem Kliff, Meer rundum,
12 m im Biom. Klippensteig 298 m (heute 1 383 m vom Weg); Stadtrand 1 370 m (ROMAN_LOC_009).

**Komposition und Anmarsch.** Blickachse vom Kliff nach Westen ins Gegenlicht (Sonne 24°): Vordergrund Grasnelkenkante, Mitte Pfeiler mit
Schaumring, Hintergrund die Vogelinsel im Dunst. Kameras: `_anmarsch` am Kliffweg (X −3712 / Y 868, 298 m, −170), `_held` auf der
Terrasse (X −3774 / Y 830, 240 m), `_nah` auf dem Pfeilerkopf (10 m), `_fern` vom Kliffweg Nord (X −3882 / Y 388, 501 m).
**Zugang:** keiner – Meeresform, nicht betretbar; Aussichtskanzel am Kliff (−3900/820) als kurzer Abzweig.

**Detail-Ebenen.** Held: Hauptpfeiler aus `veqnci0db_tier_2` hochkant (×1,3, Fuß 3 m im Höhenfeld-Pfeiler versenkt) auf dem vorhandenen
Pfeiler; Begleiter (3): `vdssailfa_tier_2` als schiefer 26-m-Pfeiler, `vfmjadufa_tier_2` + `SM_MassiveNordicCoastalCliff_01` als Stümpfe
(4–9 m über Wasser). Schutt (40–80): `SM_NordicBoulder_01`, `SM_NordicBeachRocks_01` halb unter Wasser im Ring um jeden Fuß (Brandungsblöcke,
Ursache: Abbruch). Kleinzeug: `SM_NordicBeachRockyGround_01/02` auf den Absätzen. Bewuchs nach Ursache: nur oben, wo kein Salzwasser hinkommt –
Grasnelken-/Strandmelde-Ersatz `SM_stonecrop_01/02`, `SM_sea_pea_01`; Möwenkot als weiße Streifen unter Simsen. Kontaktzone: Tang-/Seepockenband
bis 3 m über Spiegel (Materialwunsch `MI_EL_SW_Brandungsfels`), Nässe `MI_Leakage_04/10`.

**Wasser, Effekte, Licht.** Meer (Spiegel 0). Schaum/Gischt: Coast & Dunes-Decals (folgt 13d), sonst `NS_Smoke_Plume` weiß, flach, langsam
(optional, ≤ 3). Kein Licht. Dunst: Höhennebel reicht.

**Geländeänderung.** Keine (Pfeiler stehen schon); höchstens Sockel der Stümpfe −0,5 m, damit sie im Wasser stehen. Fenster 0.

**Assets.** Bestand: `veqnci0db_tier_2`, `vdssailfa_tier_2`, `vfmjadufa_tier_2`, `SM_MassiveNordicCoastalCliff_01`, `SM_HugeNordicCoastalCliff_01/02`,
`SM_NordicBoulder_01`, `SM_NordicBeachRocks_01`, `SM_NordicBeachRockyGround_01/02`, `SM_stonecrop_01/02`, `SM_sea_pea_01`; Decals
`MI_Leakage_04`, `MI_Leakage_10`, `MI_TileableLeakage_02`. Wunsch: **Coast & Dunes** (A, Tang/Schaum-Decals; Ersatz MI_Leakage),
**Ultimate Niagara Environmental VFX** (C, Gischt; Ersatz `NS_Smoke_Plume`).

**Aufwand und Risiko.** Mittel (≈ 12 Akteure, 600 Instanzen). Risiko: Klippen-Schalen hochkant zeigen offene Rückseiten → je Pfeiler zwei
Schalen Rücken an Rücken. Prüfen, ob unter den Inselchen Reste der Houdini-Kachel K9 stehen (Bildwunsch).

### 2 · Die Vogelinsel (`kueste_02_die_vogelinsel`) – Leuchtfeuer · Klippensteig

**Was man sieht.** Eine Insel wie ein Schiffsrumpf, 45 m hoch, die Westwand **weiß gekalkt** von tausenden Brutplätzen, auf jedem Sims ein
weißer Punkt, in der Luft ein langsamer Wirbel aus Vögeln. Oben kurzes, vom Kot überdüngtes Grün, die Ostseite grasig mit krummen
Kiefern. Bei Westwind zieht ein Geruch nach Fisch und Salz bis aufs Kliff.

**Leuchtfeuer.** 30-m-Silhouette: 53 von 76 Punkten (300–800 m) lesbar, bis 769 m; die weiße Wand leuchtet gegen das dunkle Meer.

**Vorbild.** Real: Bass Rock (Schottland), Vogelinsel Runde (Norwegen), Látrabjarg. Spiel: Vogelfelsen von Ard Skellig (Witcher 3).

**Standort.** Feld A5, X −4180 / Y 419, Boden 33,6 m: die 2,3-ha-Insel (hmax 45 m), 260 m vor der Küste, Wiese 87 %, 124 Baumzellen auf der
Ostseite (bis 25 m), Flanken bis 77°. 70 m im Biom. Klippensteig 231 m (Aussichtsende X −3900 / Y 452).

**Komposition und Anmarsch.** Man kommt von Süden über den Kliffweg; die Insel steht genau in der Blickachse nach Nordwest, das Licht fällt
von links auf die weiße Wand. Kameras: `_anmarsch` (X −3952 / Y 386, 230 m), `_held` (X −4064 / Y 281, 180 m – vom Klippenvorsprung),
`_nah` auf der Insel (10 m), `_fern` vom Kliffweg (X −3744 / Y 630, 484 m). **Zugang:** keiner (Insel); Aussicht am Pfadende.

**Detail-Ebenen.** Held: Westwand aus `vfmjadufa_tier_2` + `vdssailfa_tier_2` (je 2, ×1,4) vor die Inselflanke gesetzt, mit
Materialwunsch `MI_EL_SW_Guano` (Auflage weiß, Kante 5 → Kot auf Simsen). Begleiter (4): vorgelagerte Klippe `SM_HugeNordicCoastalCliff_01`,
2 Brandungsblöcke `SM_NordicBoulder_01`. Schutt (80): `SM_NordicBeachRocks_01` am Fuß. Kleinzeug: Federn (`NS_feather`, optional).
Bewuchs: oben überdüngt – `SM_beach_grass_02_1/2`, `SM_sea_wormwood_01`, `SM_kidney_vetch_01` dicht; Ostseite vorhandene Kiefern.
Kontaktzone: Kotbahnen `MI_Leakage_02/07` (Instanzfarbe weiß) unter jedem Sims, Tangband am Fuß.

**Wasser, Effekte, Licht.** Meer. Vogelwirbel als ferne Partikel (`NS_feather` umgebaut, optional). Kein Licht.

**Geländeänderung.** Keine.

**Assets.** Bestand: `vfmjadufa_tier_2`, `vdssailfa_tier_2`, `SM_HugeNordicCoastalCliff_01`, `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01`,
`SM_beach_grass_02_1/2`, `SM_sea_wormwood_01`, `SM_stonecrop_01`, `SM_kidney_vetch_01`; Decals `MI_Leakage_02`, `MI_Leakage_07`;
Effekt `NS_feather` (vorhanden, 13b). Wunsch: **Coast & Dunes** (A), **Free Niagara Particles** (vorhanden).

**Aufwand und Risiko.** Niedrig–mittel. Risiko: Guano-Weiß zu grell → Auflage-Farbe gebrochenes Weiß (0,95/0,94/0,88).

### 3 · Das Nadeltor (`kueste_03_das_nadeltor`) – Leuchtfeuer · Klippensteig (Ende)

**Was man sieht.** Am Ende des Kliffwegs, 130 m vor der Küste: ein 46-m-Pfeiler, durch den das Meer ein **Tor** geschlagen hat – unten eine
Öffnung, 8 m hoch, durch die bei jeder Welle Licht und Schaum fahren. Daneben eine dünne 27-m-Nadel. Vom Pfadende sieht man durch das
Tor auf den Horizont.

**Leuchtfeuer.** 40 m: 4 von 58 Punkten (300–800 m) sehen ≥ 30 % – vom Kliffweg Y 450–520, bis 755 m; danach verschwindet es hinter der
Kliffnase und taucht erst am Pfadende wieder auf (Lockruf zum Weitergehen).

**Vorbild.** Real: Porte d’Aval und Aiguille (Étretat), Durdle Door. Spiel: Felstore an der Küste von Skellige.

**Standort.** Feld A5, X −4100 / Y 100, Boden 45,6 m: 624-m²-Inselchen, 46,5 m hoch (TPI100 +46 m), Nadel 63 m nördlich (−4081/158, 27 m).
8 m im Biom; Klippensteig 165 m.

**Komposition und Anmarsch.** Pfadende als Kanzel (X −3900 / Y 150) mit Blick genau durch die Toröffnung nach WSW. Kameras: `_anmarsch`
(X −3960 / Y 188, 165 m), `_held` (X −4007 / Y 210, 144 m), `_nah` auf dem Pfeilerkopf (6 m, an Land gesetzt), `_fern` (X −3816 / Y 462, 460 m).
**Zugang:** keiner (Insel).

**Detail-Ebenen.** Held: Torfelsen aus zwei `veqnci0db_tier_2` (Beine, ×1,1) + `SM_MassiveNordicCoastalCliff_01` als Sturz (Überhang = Netz);
Begleiter: Nadel `vdssailfa_tier_2` hochkant, 2 Stümpfe `SM_HugeNordicCoastalCliff_02`. Schutt (50): Blöcke im Torgang (`SM_NordicBoulder_01`,
`SM_NordicBeachRocks_01`), weil dort das Dach nachbricht. Kleinzeug: `SM_NordicBeachRockyGround_01`. Bewuchs: Grasschopf oben. Kontaktzone:
Tangband, Schaumspur im Durchgang (`MI_Leakage_10`, `MI_TileableLeakage_01`).

**Wasser, Effekte, Licht.** Meer; Gischt im Tor optional (`NS_Smoke_Plume`).

**Geländeänderung.** Höhenfeld-Pfeiler unter dem Torbogen auf −2 m senken (8 × 12 m, |Δ| ≤ 48 m begründet: sonst stünde der Bogen auf
massivem Gelände). Fenster 40 × 40 m.

**Assets.** Bestand: `veqnci0db_tier_2`, `vdssailfa_tier_2`, `SM_MassiveNordicCoastalCliff_01`, `SM_HugeNordicCoastalCliff_02`, `SM_NordicBoulder_01`,
`SM_NordicBeachRocks_01`, `SM_NordicBeachRockyGround_01`; Decals `MI_Leakage_10`, `MI_TileableLeakage_01`. Wunsch: **Coast & Dunes** (A),
**Ultimate Niagara Environmental VFX** (C).

**Aufwand und Risiko.** Mittel–hoch: Bogen aus Schalen braucht Prüfbild; Δ bis −48 m im Fenster ist ungewöhnlich (Prüfer: WARNUNG > 40 m) –
Alternative: Bogen an die Westseite des Pfeilers setzen, Höhenfeld unverändert.

### 4 · Der Seefall (`kueste_04_der_seefall`) – Fundstück · Klippensteig

**Was man sieht.** Man hört ihn, bevor man ihn sieht: ein Bach läuft durch Farn und Grasnelken auf die Kliffkante zu – und ist weg. Erst an
der Kante sieht man ihn **57 m frei ins Meer fallen**, ein weißes Band, das sich halb im Wind verweht und unten in einen Schaumkessel
schlägt. Die Wand dahinter ist schwarz und nass, Moos nur dort, wo der Sprühnebel hinkommt.

**Fundstück.** Vom Pfad verdeckt: 0,00 an 88 Punkten ≤ 400 m, 0 von 150 ≤ 800 m; die Kliffkante verdeckt alles darunter. Robustprobe 3×3
(8 m): 5/9 – die Lippe selbst ist von der Terrasse in 90–130 m einsehbar, der **Fall** nicht.

**Vorbild.** Real: Múlafossur (Färöer), McWay Falls, Kirkjufellsfoss im Kleinen. Spiel: Wasserfälle an Skelliges Steilküste.

**Standort.** Feld A5, X −3844 / Y 578, Lippe 57 m, Boden am Mittelpunkt 35,6 m: der vorhandene Bach erreicht bei X −3844 die Kante
(Wasser 0 m), nach 8 m Meer bei −2 m – Hang 85°, TPI100 −32 m, Relief 105 m. 6 m im Biom; Klippensteig 92 m; Meer 6 m.

**Komposition und Anmarsch.** Zugang 160 m vom Steig (`pfad_cm`, max 66° in einem 13-m-Stück → Felsstufen) auf eine Kanzel südlich der Lippe;
Blick nach Norden auf das fallende Band mit dem Meer darunter. Kameras: `_anmarsch` (X −3762 / Y 528, 96 m), `_held` (X −3852 / Y 621, 44 m,
auf der Kante), `_nah` (10 m).

**Detail-Ebenen.** Held: `wasserfall` (Lippe 4–6 m breit, Fuß −0,5 m) mit `M_EL_Wasserfall2` (Deckkraft 0,6). Begleiter: Kliffschalen
`vdssailfa_tier_2`, `SM_HugeNordicCoastalCliff_01` beidseits der Lippe (Wand glätten). Schutt (100): `SM_mountain_rock_big_02_1/5`,
`SM_ground_rock_01` im Kessel. Kleinzeug: `SM_SmallStonesPack_03` im Bachbett. Bewuchs: Sprühzone – `SM_EagleFern_S_01`, `SM_SilverLadyFern_01`,
`SM_MossyRocks_01`; oben trockenes Gras. Kontaktzone: Nassstreifen `MI_Leakage_04/06`, Moos `MI_TileableMossPatches_01`.

**Wasser, Effekte, Licht.** Bach (vorhanden) bis zur Lippe, `wasserfall` 57 m, Fuß im Meer. Sprühnebel `BP_FogBankCard` (vorhanden, 13b).
Klang `CUE_Water_Stream_IV_Cue` (vorhanden).

**Geländeänderung.** Kanzel abflachen (±1 m, 10 × 8 m), Bachbett an der Lippe −0,5 m (Kerbe). Fenster 40 × 40 m.

**Assets.** Bestand: `vdssailfa_tier_2`, `SM_HugeNordicCoastalCliff_01`, `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01`, `SM_mountain_rock_big_02_1`,
`SM_mountain_rock_big_02_5`, `SM_ground_rock_01`, `SM_SmallStonesPack_03`, `SM_EagleFern_S_01`, `SM_SilverLadyFern_01`, `SM_MossyRocks_01`,
`SM_flat_rock_04`; Decals `MI_Leakage_04/06`, `MI_TileableMossPatches_01`. Wunsch: **Mountain – Environment Set** (A, Fall-/Schaummaterial;
Ersatz `M_EL_Wasserfall2`), **Nature Water FX** (B, Gischt; Ersatz `NS_Smoke_Plume`), **Free City & Nature Sounds** (vorhanden).

**Aufwand und Risiko.** Mittel. Risiko: 57-m-Vorhang mit eigenem Material wirkt aus 40 m schnell als Fläche → zerrissene Ränder (2 schmale
Zusatzbänder) und Sprühnebel.

### 5 · Die Gezeitenbank (`kueste_05_die_gezeitenbank`) – Fundstück · Klippensteig

**Was man sieht.** Am Fuß der Kliffecke, wo die Strandebene ans Gebirge stößt, liegt eine flache, dunkle Felsbank knapp über dem Wasser,
von Rinnen zerschnitten. In ihren Mulden stehen ein Dutzend Tümpel – glasklar, mit rotem und grünem Tang, Muscheln, Seegras, in einem ein
umgekippter Brocken mit Seesternen. Bei jeder größeren Welle läuft ein Schwall über die Kante und füllt sie nach.

**Fundstück.** Verdeckt: 0,00 an 61 Punkten ≤ 400 m, 0 von 173 ≤ 800 m, 3×3 9/9 – die Kliffecke steht zwischen Pfad und Bank.

**Vorbild.** Real: Rockpools in Cornwall (Polzeath), Gezeitenbänke von Moher. Spiel: Strandsuche an den Inseln von Skellige; Gezeitenbecken in
Sea of Thieves.

**Standort.** Feld A6 (Mitte 43 m außerhalb, Regel ≤ 150 m), X −3750 / Y 1040, Boden 4,6 m: Kliffecke (Hang 39°, Relief 58 m, TPI100 −19 m),
davor Strand/Sand 29 %, Fels 16 %; Meer 6 m. Klippensteig 105 m; Zugang 211 m (max 24,5°, 11 m Querhang > 38° → Stufen).

**Komposition und Anmarsch.** Man steigt vom Ebenenrand hinunter und biegt um die Felsecke: die Bank liegt im Gegenlicht, das Kliff als
dunkler Rahmen rechts. Kameras: `_anmarsch` (X −3678 / Y 964, 105 m), `_held` (X −3728 / Y 1052, 25 m), `_nah` (10 m).

**Detail-Ebenen.** Held: Felsbank aus `SM_SmoothRockShelf_01` + `SM_ForestRockSlab_01` (×2–3), 25–45 % eingegraben. Begleiter (6): Brocken
`SM_NordicBeachRock_01`, Kliff-Schale `SM_HugeNordicCoastalCliff_02` als Ecke. Schutt (150): `SM_NordicBeachRockyGround_01/02`, Kiesel
`SM_SmallStonesPack_01/07`, Sand mit Kies `SM_BeachSandWithPebbles_01`. Kleinzeug: Muscheln/Seegras (Coast & Dunes, folgt), sonst
`SM_WaterPlant03` grün getönt unter Wasser. Bewuchs: oberhalb der Gischt `SM_sea_pea_01`, `SM_stonecrop_02`. Kontaktzone: Tangband,
nasse Kanten `MI_Leakage_10/12`, `MI_TileableLeakage_03`.

**Wasser, Effekte, Licht.** 8–12 kleine `see` (Tümpel, 1–4 m, Spiegel +0,35 m, `farbe: klar`, Tiefe 0,3–0,8 m) auf der Bank. Kein Effekt.

**Geländeänderung.** Bank +0,3…0,6 m (30 × 14 m) mit Mulden −0,4 m für die Tümpel (Ufer rundum über dem Spiegel). Fenster 50 × 40 m.

**Assets.** Bestand: `SM_SmoothRockShelf_01`, `SM_ForestRockSlab_01`, `SM_NordicBeachRockyGround_01/02`, `SM_NordicBeachRock_01`, `SM_SmallStonesPack_01/07`,
`SM_BeachSandWithPebbles_01`, `SM_HugeNordicCoastalCliff_02`, `SM_sea_pea_01`, `SM_stonecrop_02`; Decals `MI_Leakage_10/12`, `MI_TileableLeakage_03`.
Wunsch: **Coast & Dunes** (A, Seetang, Muscheln; Ersatz `SM_WaterPlant03`).

**Aufwand und Risiko.** Niedrig–mittel. Risiko: kleine Seen < 1 m² flackern → mindestens 1,5 m Durchmesser.

### 6 · Die Kreidewand (`kueste_06_die_kreidewand`) – Leuchtfeuer · Kap-Pfad

**Was man sieht.** Mitten in der grünen Buchenflanke des Kaps ist ein Stück Berg abgerutscht: eine **leuchtend weiße Kreidewand**, 25–30 m
hoch, oben die Wurzeln der Buchen, die noch an der Kante hängen. Darunter ein frischer Sturzkegel aus weißem Brei und schwarzen
Feuersteinknollen, zwei Buchen liegen mit der Krone im Wasser. Das Meer davor ist milchig-türkis vom Kalk.

**Leuchtfeuer.** 25 m: 29 von 79 Punkten (300–800 m), bis 743 m; bester Punkt am Südufer der Bucht (646 m). Schon vom **heutigen** Weg
an der Bucht sehen 8 von 24 Punkten die Wand – sie zieht den Spieler auf den Kap-Pfad.

**Vorbild.** Real: Königsstuhl/Jasmund (Rügen), Møns Klint, Étretat-Kreide. Spiel: Kreidefelsen in Kingdom Come Deliverance (Wälder) und
die hellen Küstenabbrüche in The Witcher 3 (Toussaint-Küste).

**Standort.** Feld H2, X 2590 / Y −2380, Fuß 5,5 m: Westflanke des Kaps (Laub 54 %, 156 Baumzellen bis 25 m), Hang bis 38°, 20–30° von 0 auf
90 m; Meer 21 m. Kap-Pfad 110 m (Zugang 146 m, max 23,5°, streng). 22 m im Biom.

**Komposition und Anmarsch.** Von der Bucht im Süden sieht man den weißen Riss im Grün; auf dem Kap-Pfad verschwindet er hinter dem Wald und
öffnet sich erst, wenn man an den Abbruch tritt. Kameras: `_anmarsch` (X 2699 / Y −2291, 141 m), `_held` vom Strand (X 2633 / Y −2355, 50 m),
`_nah` (10 m), `_fern` vom Bucht-Südufer (X 2518 / Y −1738, 646 m).

**Detail-Ebenen.** Held: Wand aus `vmnmbhv_tier_0` + `uchoab3fa_tier_0` + `SM_MassiveSandstoneCliff_05` mit `MI_EL_SW_Kreide` (Tönung weiß).
Begleiter (5): Buchen an der Kante `SM_beech_tree_05/08` (Wurzeln frei), tote Buche `SM_EuropeanBeech_Dead_XL_01`, liegende Bäume
`SM_FallenSpruceTree_01`, `SM_BrokenTreeAssembly_01` mit der Krone im Wasser (Ursache: Abbruch). Schutt (180): Sturzkegel `SM_beach_cliff_02_B`,
`SM_beach_escarpment_01_A` weiß, Feuerstein `SM_SmallStonesPack_05` dunkel, Kiesel `SM_BeachSandWithPebbles_02`. Kleinzeug: Wurzelstrünke
`SM_RottenTreeStump_01`, Efeu `SM_Ivy_11` an der Kante. Bewuchs: Pestwurz `SM_petasites_spurius_01` am Hangfuß (Sickerwasser). Kontaktzone:
Kreidebrei-Fächer ins Wasser, Nassband `MI_Leakage_01/09`.

**Wasser, Effekte, Licht.** Meer; milchiges Wasser lässt sich nicht lokal färben – Kalkfahne als flaches Decal am Grund (Coast & Dunes, B).

**Geländeänderung.** Abbruch: Hang auf 12–15 m Breite um −4…−8 m zurücksetzen (Anriss), Kegel +2 m davor. Fenster 80 × 60 m.

**Assets.** Bestand: `vmnmbhv_tier_0`, `uchoab3fa_tier_0`, `SM_MassiveSandstoneCliff_05`, `SM_beach_cliff_02_B`, `SM_beach_escarpment_01_A`,
`SM_beech_tree_05`, `SM_beech_tree_08`, `SM_EuropeanBeech_Dead_XL_01`, `SM_FallenSpruceTree_01`, `SM_BrokenTreeAssembly_01`, `SM_RottenTreeStump_01`,
`SM_BeachSandWithPebbles_02`, `SM_NordicBeachRock_01`, `SM_SmallStonesPack_05`, `SM_Ivy_11`, `SM_petasites_spurius_01`; Decals `MI_Leakage_01/09`;
Klang `CUE_Wind_Autumn_wind_with_leaves_rustling_Cue`. Wunsch: **Coast & Dunes** (B).

**Aufwand und Risiko.** Mittel. Risiko: Weiß überstrahlt in der festen Sonne → Helligkeit 1,25, Sättigung 0,25, Moosgrün im oberen Rand.

### 7 · Der Dünenkamm (`kueste_07_der_duenenkamm`) – Fundstück · Kap-Pfad

**Was man sieht.** Hinter der Nordostnase des Kaps, unsichtbar vom Pfad, liegt ein Strand, den der Wind zu einem **Dünenkamm** aufgeworfen
hat: 4 m hoch, die Luvseite glatt und gerippelt, oben Strandhafer, der sich in eine Richtung kämmt, dahinter graue Düne mit Sanddorn
(orange Beeren), Kartoffelrosen und Stranddisteln. Im Spülsaum gebleichtes Treibholz und Tang.

**Fundstück.** Verdeckt: 0,00 an 12 Punkten ≤ 400 m, 0 von 68 ≤ 800 m, 3×3 9/9 (die Nordostschulter steht davor).

**Vorbild.** Real: Weißdüne/Graudüne auf Sylt, Hiddensee, Holkham. Spiel: Strände in Red Dead Redemption 2 (Guarma ohne Palmen), Küsten in
Dragon Age: Inquisition (Storm Coast, Farbe).

**Standort.** Feld H2, X 3300 / Y −2590, Boden 2,9 m: Strand an der Ostseite (Sand 40 %, Nadeln 28 %), Hang 11°, Meer 25 m; 258 Baumzellen
dahinter. Kap-Pfad 191 m (Zugang 215 m, max 24,9°).

**Komposition und Anmarsch.** Zugang durch den Kiefernwald hinab; der Kamm sperrt die Sicht aufs Meer, bis man oben steht – dann Weite.
Kameras: `_anmarsch` (X 3220 / Y −2574, 82 m), `_held` (X 3238 / Y −2579, 63 m, über den Kamm aufs Meer), `_nah` (10 m).

**Detail-Ebenen.** Held: Dünenkamm (Gelände). Begleiter (6): krumme Strandkiefern `SM_pine_beach_crooked_01/02`, `SM_pine_beach_medium_02`
(Windflucht landeinwärts). Schutt/Mittel (200): Strandhafer `SM_beach_grass_01_1/2/3`, `SM_beach_grass_01_hp_1`, `SM_beach_grass_03_1/2` in
Horsten auf dem Kamm; Sanddorn `SM_sea_buckthorn_01_fruits`, `SM_sea_buckthorn_03`, Rosen `SM_beach_rose_02_with_pink_flowers`,
`SM_beach_rose_04_white_flowers` in der Graudüne. Kleinzeug: Stranddistel `SM_sea_holly_01/03`, `SM_sea_pea_01`, Treibholz `SM_beach_driftwood_01`,
Kiesel `SM_BeachSandWithPebbles_01`. Bewuchs nach Ursache: Hafer nur auf frischem Sand (Kamm), Sanddorn/Rose dahinter, Kiefern ganz hinten.
Kontaktzone: Spülsaum aus Tang/Zweigen (`MI_Sticks_01`), Sandfahnen.

**Wasser, Effekte, Licht.** Meer; Sandfahnen am Kamm (`NS_leaf` umgefärbt, optional).

**Geländeänderung.** Kamm +3…4,5 m (60 × 18 m, Luv 12°, Lee 28°), Lagen Sand 255 auf Kamm/Strand, Trockengras dahinter. Fenster 90 × 50 m.

**Assets.** Bestand: alle oben genannten (Coast & Dunes, Nicht-Nanite-Pflanzen). Wunsch: **Coast & Dunes** (A, Spülsaum-Decals, Tang),
**Nanite Driftwood Props** (B, Wunsch aus der Aue; Ersatz `SM_beach_driftwood_01`).

**Aufwand und Risiko.** Niedrig. Risiko: Nicht-Nanite-Gräser in großer Dichte → Strandhafer als Landschafts-Gras ergänzen.

### 8 · Das Blasloch (`kueste_08_das_blasloch`) – Fundstück · Kap-Pfad

**Was man sieht.** In der steilen Ostbucht, auf einer dunklen Felsplatte über dem Wasser: ein Loch, kaum zwei Meter breit. Erst ist da nur
ein Grollen unter den Füßen, dann **schießt eine Säule aus Wasser und Gischt 8–14 m hoch**, fällt als Sprühregen zurück, und das Loch
saugt pfeifend Luft. Im Hang darüber stürzt ein Bach in Kaskaden herab.

**Fundstück.** Verdeckt: 0,00 an 19 Punkten ≤ 400 m, 0 von 84 ≤ 800 m, 3×3 9/9 – die Bucht ist von der Nordseite her nicht einsehbar.

**Vorbild.** Real: Kiama Blowhole (Australien), Spouting Horn (Kauai), Gloup (Orkney). Spiel: ähnliche Spritzlöcher in Sea of Thieves.

**Standort.** Feld H2, X 3185 / Y −2385, Boden 13,2 m: Bucht mit 41–63° steilen Flanken (Relief 55 m, TPI100 −16 m), Meer 16 m; vorhandener
Bach endet 50 m nördlich in Kaskaden (X 3060–3150, 85 → 9 m). Kap-Pfad 148 m (Zugang 251 m, max 24,9°).

**Komposition und Anmarsch.** Abstieg in Kehren durch Kiefern; das Grollen ist zuerst da. Held-Blick von der Flanke über die Platte aufs
Meer, die Fontäne vor dem Horizont. Kameras: `_anmarsch` (X 3199 / Y −2465, 81 m), `_held` (X 3196 / Y −2447, 63 m), `_nah` (10 m).

**Detail-Ebenen.** Held: Felsplatte `SM_SmoothRockShelf_01` + `Basalt_Basalt_Cliff_Rock_A_SM` (dunkel, flach) mit Loch (Lücke zwischen zwei
Platten). Begleiter (4): Kliffschalen `SM_HugeNordicCoastalCliff_01`, `SM_MassiveNordicCoastalCliff_01` als Höhlendach zur See (Überhang =
Netz). Schutt (120): `SM_NordicBeachRocks_01`, `SM_NordicBeachRockyGround_02`, `SM_SmallStonesPack_11`. Bewuchs: oben Strandkiefer
`SM_pine_beach_crooked_01`, Sanddorn `SM_sea_buckthorn_04`, Mauerpfeffer `SM_stonecrop_01`; auf der Platte nichts (Salz). Kontaktzone:
Nassfächer um das Loch `MI_Leakage_10/11`.

**Wasser, Effekte, Licht.** Meer; Fontäne: Niagara (Nature Water FX, Geysir-System, alle 9–14 s) – Ersatz `NS_Smoke_Plume` weiß
(schwach). Klang: Grollen/Pfeifen fehlt (Lücke).

**Geländeänderung.** Platte +1 m (18 × 10 m), Gang zur See −2 m unter dem Netzdach. Fenster 40 × 30 m.

**Assets.** Bestand: `SM_HugeNordicCoastalCliff_01`, `SM_MassiveNordicCoastalCliff_01`, `Basalt_Basalt_Cliff_Rock_A_SM` (13b), `SM_SmoothRockShelf_01`,
`SM_NordicBeachRocks_01`, `SM_NordicBeachRockyGround_02`, `SM_SmallStonesPack_11`, `SM_pine_beach_crooked_01`, `SM_sea_buckthorn_04`,
`SM_stonecrop_01`; Decals `MI_Leakage_10/11`. Wunsch: **Nature Water FX** (A für diesen Ort; Ersatz `NS_Smoke_Plume`), **Ultimate Niagara
Environmental VFX** (B), **Coast & Dunes** (A).

**Aufwand und Risiko.** Mittel; ohne Fontänen-Effekt ist der Ort nur halb so stark → Effektpaket entscheidet.

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/sumpf/katalog.md](sehens/sumpf/katalog.md)

### 1 · Der Ertrunkene Wald (`sumpf_01_der_ertrunkene_wald`) – Leuchtfeuer

**Was man sieht.** Vom Westweg aus ragen über dem Röhricht graue Spitzen in den Himmel – tote Fichten, Dutzende, silbern gebleicht, die
Äste nur noch Stummel. Kommt man näher, stehen sie in schwarzem, spiegelglattem Wasser, als wäre ein ganzer Wald ertrunken: Stamm neben
Stamm, manche gekippt, manche zu Stümpfen gebrochen, an jedem ein Bart aus grauer Flechte. Über dem Wasser liegt ein dünner Nebel, in dem
die Stämme sich doppelt spiegeln.

**Leuchtfeuer.** 18-m-Silhouette: 50 von 154 Punkten (300–800 m) lesbar, bis 731 m (bester 502 m im Westen).

**Vorbild.** Real: Lake Kaindy (Kasachstan), Caddo Lake, Totholzwälder hinter Biberdämmen in Kanada. Spiel: Crookback Bog / Velen-Sümpfe
(Witcher 3), die ertrunkenen Wälder in Dragon Age: Inquisition (Fallow Mire).

**Standort.** Feld H5, X 2610 / Y 160, Gelände 0,97 m unter dem Spiegel 1,58 m (Wasser 0,6 m tief): größte offene Wasserfläche im Westteil
(Nässe im 40-m-Radius 82 %, im 80-m-Radius 52 %), Algen 73 %, Hang 2°, Relief 2,5 m. 25 m im Biom; Weg 154 m (Stichweg West), Stadtrand 670 m.
**Ursache in der Erzählung:** das Wasser ist gestiegen (der Spiegel 1,58 m liegt über dem alten Waldboden 0,5–1,2 m) und hat den Fichtenhain
ertränkt.

**Komposition und Anmarsch.** Vom Stichweg nach Osten: Vordergrund Röhricht, Mitte die Stammreihen schräg hintereinander, Hintergrund der
Hügel mit Wald. Kameras: `_anmarsch` am Stichweg (X 2459 / Y 185, 153 m), `_held` (X 2525 / Y 175, 86 m, am Ufer), `_nah` (10 m),
`_fern` (X 2108 / Y 182, 502 m). Zugang 162 m streng (max 4°), davon **94 m nass** → Bultenpfad aus Seggenbulten und liegenden Stämmen.

**Detail-Ebenen.** Held: 40–60 tote Fichten `Fir_08_Dead_NoBillboard`, `Fir_08_Dead_Forest`, `SM_Forest_pine_10_dead` (×0,8–1,2, schräg 0–12°,
Fuß 0,6–1 m unter Wasser), ein „weißer Riese“ ×1,4. Begleiter (6–8): gebrochene Stämme `qlEtl_tier_0`, `SM_DeadTree_01/02`, liegend
`SM_LargeFallenTree_01` halb im Wasser. Schutt (150): Äste `SM_OldTreeBranch_01`, `SM_dead_log_01/03` treibend. Kleinzeug: Moospolster
`SM_MossClump_01` auf Stümpfen. Bewuchs nach Ursache: Rohrkolben-/Seggensaum nur am flachen Rand (`SM_Rohrkolben_Horst_1/4`,
`SM_Rohrkolben_Jung_2`, `SM_ToadRush_013/014`, `SM_dead_grass_02`), im tiefen Teil nichts – keine lebenden Bäume. Kontaktzone: Rindenreste
`MI_ScatteredBark_01`, Nasslinie am Stamm 0,3 m über Spiegel `MI_Leakage_05`.

**Wasser, Effekte, Licht.** Vorhandener Epic-See (Spiegel 1,58 m), Farbe `schwarz_spiegel` als eigener `see`-Ausschnitt (Umriss im Phase-2-Plan).
Bodennebel `BP_FogBankVolume` (vorhanden, 13b) oder `lokaler_nebel` (Dichte 0,06, Höhenabfall stark). Kein Licht.

**Geländeänderung.** Keine (Wasser ist da); Bultenpfad als Instanzen.

**Assets.** Bestand siehe oben (alle in `netze.csv`); Effekte `BP_FogBankVolume`, `BP_FogBankCard` (13b). Wunsch: **Swamp Cypress Roots**
(vorhanden: `SM_SwampCypress_A` als Wurzelfuß einzelner Stämme), Materialwunsch `MI_EL_SW_Silberholz` (nur falls Totholz über die
Megascans-Überschreibung läuft).

**Aufwand und Risiko.** Mittel (≈ 60 Akteure). Risiko: Nicht-Nanite-Fichten mit Billboard → `NoBillboard`-Variante bevorzugen.

### 2 · Der Weidendom (`sumpf_02_der_weidendom`) – Leuchtfeuer

**Was man sieht.** Im Osten des Sumpfes steht ein runder Hügel aus Grün über dem Röhricht – erst beim Näherkommen erkennt man, dass es
**neun Riesenweiden** sind, die im Kreis im Wasser stehen und ihre Kronen zu einem geschlossenen Dach verflochten haben. Darunter ist es
dämmrig, das Wasser schwarz und still, Wurzeln stehen wie Knie heraus, von oben hängen Zweigvorhänge bis aufs Wasser. Man watet hinein wie
in eine Halle.

**Leuchtfeuer.** 22 m: 9 von 120 Punkten (300–800 m), bis 635 m; bester Punkt 564 m nordöstlich (X 3658 / Y 108). Die Kuppel ist die
einzige dunkle Großform in der hellen Osthälfte.

**Vorbild.** Real: Zypressendome der Everglades, Weidenringe an der Mittelelbe. Spiel: der Baum der Muhmen im Krummen Sumpf (Witcher 3) als
Stimmung, ohne Bauwerk.

**Standort.** Feld H5/I5, X 3350 / Y 580, Gelände 0,45 m (Wasser 1,1 m): flache Wanne mit Nässe 58 % im 40-m-Radius, Kraut/Algen/Moos/Gras je
~25 %. 72 m im Biom; Weg 198 m (Wegende Ost). Zugang 202 m streng (max 8°), 40 m nass.

**Komposition und Anmarsch.** Vom Wegende Ost über Bulten hinab; die Kuppel steht vor dem Hügel im Hintergrund; Held-Blick von außen in den
Spalt zwischen zwei Stämmen, dahinter der Schwarzspiegel. Kameras: `_anmarsch` (X 3479 / Y 431, 197 m), `_held` (X 3378 / Y 546, 44 m),
`_nah` (10 m), `_fern` (X 3658 / Y 108, 564 m).

**Detail-Ebenen.** Held: 9 × `Big_Tree_Willow_02`/`_01` (×1,3–1,5) auf einem Ring r = 24 m, Fuß je auf `SM_SwampCypress_A` (13b, Stelz-/Knie-
wurzeln) 0,5 m hochgesetzt. Begleiter (6): Jungweiden `SM_grey_willow_03/04`, gestürzte Weide `SM_MossyTree_01` als Tor. Schutt (100): treibende
Äste `Branch_Goat_Willow_Decaying_02`, `SM_dead_log_02`. Kleinzeug: Moos `SM_MossClump_03`, `SM_CustomMoss_02` auf Wurzeln. Bewuchs: Röhricht-
gürtel außen (`SM_Rohrkolben_Horst_2/5`, `SM_ToadRush_010`), innen im Schatten **nichts außer Wasserlinsen** und einzelnen Seerosen
(Rembrandt Water Lily, 13b). Kontaktzone: Moospelz `MI_TileableMossPatches_02` an den Stammfüßen.

**Wasser, Effekte, Licht.** Innerer Spiegel `schwarz_spiegel` (see, r = 12 m). Dunst `BP_FogBankCard` innen. Ein Lichtschacht durch eine
Kronenlücke ergibt sich aus der festen Sonne – kein Licht nötig.

**Geländeänderung.** Innenmulde −0,4 m (r 14 m) für tieferes, schwärzeres Wasser. Fenster 60 × 60 m.

**Assets.** Bestand: `Big_Tree_Willow_01/02`, `SM_SwampCypress_A`, `SM_grey_willow_03/04`, `Branch_Goat_Willow_Decaying_02`, `SM_Rohrkolben_Horst_2/5`,
`SM_ToadRush_010`, `SM_dead_log_02`, `SM_MossyTree_01`, `SM_MossClump_03`, `SM_CustomMoss_02`, Rembrandt Water Lily (13b). Wunsch: keiner zwingend.

**Aufwand und Risiko.** Niedrig–mittel. Risiko: Trauerweiden wirken „Park“ → Kronen leicht grau-grün tönen, Zweigvorhänge kürzen.

### 3 · Der Reiherhorst (`sumpf_03_der_reiherhorst`) – Leuchtfeuer

**Was man sieht.** Auf einer flachen Moosinsel mitten im offenen Sumpf stehen drei abgestorbene Baumriesen, weiß und kahl – und in ihren
Kronen sitzen **große Reisighorste**, ein Dutzend, manche bewohnt: Graureiher stehen darin wie Statuen. Der Boden darunter ist weiß
gekalkt, Federn und Fischgräten liegen herum, das Gras ist überdüngt und hoch.

**Leuchtfeuer.** 20 m: 65 von 204 Punkten (300–800 m), bis 746 m; vom Westweg und vom Südweg sichtbar.

**Vorbild.** Real: Reiherkolonien im Spreewald und an der Peene, Graureiher-Horste in toten Eichen. Spiel: Vogelbäume in Red Dead Redemption 2
(Bluewater Marsh).

**Standort.** Feld H5, X 2650 / Y 380, Boden 2,0 m (0,4 m über Spiegel): kleine Moosinsel (Algen 43 %, Moos 37 %), Hang 0°, offenes Wasser
ringsum (Nässe 40 m: 47 %). 50 m im Biom; Weg 272 m. Zugang 270 m streng, 60 m nass.

**Komposition und Anmarsch.** Die weißen Kronen stehen gegen den dunklen Elfenwald-Hügel im Norden. Kameras: `_anmarsch` (X 2459 / Y 189, 270 m),
`_held` (X 2619 / Y 354, 40 m), `_nah` (10 m), `_fern` (X 2180 / Y 226, 495 m).

**Detail-Ebenen.** Held: 3 tote Riesen `SM_Dead_Tree_01/02` (×1,4) und `SM_EuropeanBeech_Dead_XL_01`. Begleiter: 12–15 Horste aus
`SM_detail_branches_01/02`, `SM_OldTreeBranch_03/05`, `Branch_Goat_Willow_Decaying_01` in Astgabeln. Schutt (80): heruntergefallene Äste.
Kleinzeug: Federn (`NS_feather`, 13b), Gräten (nicht im Bestand – weggelassen). Bewuchs nach Ursache: überdüngtes Hochgras
(`SM_KikuyuGrass_01`), Rohrkolben `SM_Rohrkolben_Horst_3`, `SM_ToadRush_010`, `SM_dead_grass_01`. Kontaktzone: Kotflecken `MI_Leakage_08`
weiß getönt, `MI_ScatteredSticksAndTwigs_01`.

**Wasser, Effekte, Licht.** Vorhandener See. Reiher als Figuren sind nicht Teil des Auftrags (nur Horste und Spuren).

**Geländeänderung.** Insel +0,3 m (r 18 m), damit sie trocken bleibt. Fenster 50 × 50 m.

**Assets.** Bestand: alle oben genannten; Effekt `NS_feather` (13b). Wunsch: keiner.

**Aufwand und Risiko.** Niedrig. Risiko: Graveyard-Totbäume haben Blattkarten (`M_Dead_Tree_Leaves`) → Blätter-Slot ausblenden.

### 4 · Der Schwingrasen (`sumpf_04_der_schwingrasen`) – Fundstück

**Was man sieht.** Hinter einem Saum aus Moorbirken öffnet sich eine Fläche aus rostrotem und grünem Torfmoos, die **schwankt**, wenn man
sie betritt – ein Teppich, der auf Wasser schwimmt. Mitten darin drei kreisrunde **Mooraugen**, tintenschwarz, ohne Grund, der Rand aus
Moos hängt über. Wollige Seggen, Sonnentau-Rot, ein umgestürzter Birkenstamm, der halb im größten Auge versinkt.

**Fundstück.** Verdeckt: 0,00 an 30 Punkten ≤ 400 m, 3×3 9/9; der Birkensaum und der Südrand schirmen ihn ab (von 800 m sehen 19 von 199
Punkten über den Saum, ab 570 m – aus dieser Entfernung nicht lesbar).

**Vorbild.** Real: Kesselmoore der Uckermark, Schwingrasen im Wurzacher Ried, Moorkolke im Hochmoor. Spiel: Moorflächen in Kingdom Come
Deliverance (Sümpfe bei Sasau), Witcher-3-Sumpf als Gegenbild (dort fehlt genau das).

**Standort.** Feld H5, X 2690 / Y 700, Boden 2,2 m (0,6 m über Spiegel): Moos 40 % (Moorboden 15 m: 79 %), Hang 2°, Nässe 40 m 22 % – Moor,
nicht offenes Wasser. 53 m im Biom; Weg 286 m (Südstraße); Zugang 288 m streng (max 13,5°), trocken.

**Komposition und Anmarsch.** Vom Südrand durch Birken bergab; das größte Auge liegt in der Blickachse mit dem gestürzten Stamm als Linie.
Kameras: `_anmarsch` (X 2699 / Y 845, 145 m), `_held` (X 2690 / Y 820, 120 m), `_nah` (10 m).

**Detail-Ebenen.** Held: drei Augen (Gelände-Kolke). Begleiter (5): Moorbirken `Big_Tree_Birch_01` (×0,6–0,8, krumm), Stumpf
`SM_BirchTreeStump_01`, Stamm im Auge. Schutt (200): Moospolster `SM_MossClump_01/04`, `SM_CustomMoss_01/04`, `SM_moss_01` dicht als Teppich mit
Materialwunsch `MI_EL_SW_Torfmoos` (rötlich). Kleinzeug: Seggen `SM_ToadRush_013/015`, `SM_dead_grass_03`, Schachtelhalm `SM_rough_horsetail_02`,
Heide `SM_forest_heather_01` auf trockeneren Bulten. Kontaktzone: überhängende Moosränder an den Augen, Lagen Moos 255.

**Wasser, Effekte, Licht.** 3 × `see` (r 5 / 3,5 / 2,5 m), Spiegel 1,70 m, Tiefe 2–3 m, `farbe: schwarz_spiegel`; Ufer rundum über Spiegel
(Stempel). Hauch Dunst `BP_FogBankCard`.

**Geländeänderung.** Kolke −2,5…−3 m (steile Wand), Ring +0,2 m. Fenster 70 × 60 m.

**Assets.** Bestand siehe oben; Wunsch: **Megascans Rembrandt Water Lily** (vorhanden, C: zwei Blätter am Rand).

**Aufwand und Risiko.** Niedrig. Risiko: „Schwanken“ ist Gameplay – optisch nur über weichen Moosrand und Wasserlinsen.

### 5 · Der Erlenbruch (`sumpf_05_der_erlenbruch`) – Fundstück

**Was man sieht.** Am Fuß des Nordhangs, wo Quellwasser austritt, steht ein dichter Ring aus Bäumen auf **Stelzwurzeln** – jeder Stamm auf
einem Sockel aus Wurzeln, unter dem das schwarze Wasser durchfließt. Drinnen ist es still und grün: Farne auf jedem Wurzelsockel,
Sumpfdotterblumen-Gelb, ein Rinnsal, das zwischen den Bulten glitzert und im Schlamm versickert. Ein Baum ist umgestürzt und hat seinen
Wurzelteller mit Schlamm hochgerissen.

**Fundstück.** Ohne den Ort heute nur teilweise verdeckt (3×3 6/9); der **Erlenring ist der Ort selbst** (Bruchwald) und macht ihn vom Weg
unsichtbar: mit geplantem Ring (r 38 m, 16 m breit, 14 m hoch) 0,00 an 39 Punkten ≤ 400 m, 0 / 167 ≤ 800 m, 3×3 9/9.

**Vorbild.** Real: Erlenbrüche im Spreewald und am Steinhuder Meer. Spiel: Wälder um Velen (Witcher 3), Moorwald in Kingdom Come.

**Standort.** Feld H4, X 2560 / Y −110, Boden 13,1 m: Hangfuß (Hang 10°, Relief 11 m, TPI100 −2,6 m), Laub 70 %, Schlamm 30 %; ein Gerinne
kommt vom Hang (Wasser 79 m). 10 m im Biom; Weg 286 m. Zugang 311 m streng (max 11°). Stadtrand 401 m.

**Komposition und Anmarsch.** Vom Weg im Westen durch den Hangwald, dann eine Lücke im Erlenring; die gestürzte Erle als Tor.
Kameras: `_anmarsch` (X 2556 / Y −48, 62 m), `_held` (X 2442 / Y −131, 120 m), `_nah` (10 m).

**Detail-Ebenen.** Held: 18–25 Bäume auf Wurzelsockeln – Erlen-Ersatz `Big_Tree_Birch_01`, `SM_Poplar_tree_02/03` (13c: Erlen nicht im
Bestand) auf `SM_beech_old_roots_01`, `SM_MossyForestRoots_02`, `SM_crooked_root_01`, 0,6–0,9 m hochgesetzt. Begleiter: gestürzter Baum
`SM_MossyTree_01` mit Wurzelteller. Schutt (150): `SM_dead_log_04`, Zweige. Kleinzeug/Bewuchs nach Ursache: auf jedem Sockel Farn
(`SM_EagleFern_M_01`, `SM_SilverLadyFern_01/03`), am Rinnsal Pestwurz `SM_petasites_spurius_02`, Gelb `SM_YellowArchangel_01`,
`SM_Crownbeard_01` (Sumpfdotterblume-Ersatz). Kontaktzone: Moos `MI_TileableMossPatches_01`, nasser Schlamm `MI_Leakage_03`, Lagen Schlamm.

**Wasser, Effekte, Licht.** Rinnsal `bach` (Quelle am Hang, 0,4–0,8 m breit, `versickert`), Schwarzwasser-Schlenke `see` r 9 m, Spiegel +0,15 m,
`farbe: moorbraun`. Klang `CUE_Water_Stream_I_Cue` (13b).

**Geländeänderung.** Schlenke −0,6 m, Rinnsal-Kerbe −0,3 m. Fenster 90 × 90 m.

**Assets.** Bestand siehe oben; Wunsch: **Megascans Trees: European Black Alder** (B, Wunsch aus der Aue; Ersatz Birke/Pappel).

**Aufwand und Risiko.** Mittel. Risiko: Birken statt Erlen lesen sich hell – Rinde über Instanzfarbe dunkler.

### 6 · Das Bultenfeld (`sumpf_06_das_bultenfeld`) – Fundstück

**Was man sieht.** Eine Wiese, die keine ist: hunderte **kniehohe Seggenbulten**, jeder ein Schopf aus Halmen auf einem Sockel aus alten
Blattresten, dazwischen schmale Rinnen mit schwarzem Wasser. Man kommt nur von Bult zu Bult springend voran. Weidenbüsche, ein paar
Schachtelhalme, und im Spätsommerlicht leuchten die trockenen Spitzen der Seggen goldgelb.

**Fundstück.** Verdeckt: 0,00 an 36 Punkten ≤ 400 m, 3×3 9/9 (Südrand).

**Vorbild.** Real: Bultenwiesen im Biebrza-Tal (Polen), Seggenriede am Federsee. Spiel: Sumpfwiesen in The Witcher 3 (Velen Süd).

**Standort.** Feld H5/I5, X 3290 / Y 780, Boden 2,5 m (0,9 m über Spiegel): Gras 67 %, Kraut 20 %, Moos 8 %; Hang 3° – die typische Lage
knapp über dem Wasserspiegel, die im Frühjahr überflutet. 102 m im Biom; Weg 273 m; Zugang 282 m streng.

**Komposition und Anmarsch.** Vom Südrand hinab; die Bultenreihe führt als Linie zum Weidendom im Hintergrund (290 m nördlich).
Kameras: `_anmarsch` (X 3159 / Y 939, 206 m), `_held` (X 3255 / Y 875, 101 m), `_nah` (9 m).

**Detail-Ebenen.** Held: 120–180 Bulten aus `SM_KikuyuGrass_01/04` (×1,1–1,5) auf Erdhügeln (Gelände-Höcker +0,4 m). Begleiter: Grauweiden
`SM_grey_willow_01/02` (8), Rohrkolben-Jungpflanzen in den Rinnen `SM_Rohrkolben_Jung_1`. Kleinzeug: `SM_ToadRush_00/010/02`, `SM_grass_bush_02`,
`SM_dead_grass_01`, `SM_rough_horsetail_01`, Moos `SM_MossClump_02`. Kontaktzone: Rinnen mit Wasser, Lagen Schlamm/Algen in den Rinnen.

**Wasser, Effekte, Licht.** Rinnen als flache `see`-Bänder (Spiegel 2,1 m, `moorbraun`). Samenflug `NS_leaf` (optional).

**Geländeänderung.** Höcker-Rauschen +0,2…0,5 m / Rinnen −0,3 m. Fenster 80 × 60 m.

**Assets.** Bestand siehe oben; Wunsch: **Free Niagara Particles** (vorhanden, C).

**Aufwand und Risiko.** Niedrig. Risiko: Bulten als Raster → Abstand nach Rauschen, Rinnen zuerst legen.

### 7 · Der Tellerweiher (`sumpf_07_der_tellerweiher`) – Fundstück

**Was man sieht.** Ein kleiner, stiller Weiher hinter Rohrkolben, und darauf liegen **Seerosenblätter so groß wie Wagenräder** – 3 bis 5 m,
mit hochgebogenem Rand wie Tabletts, dazwischen weiße und rosa Blüten. Auf einem der Teller sitzt ein Frosch, in einem anderen steht
Regenwasser. Libellen, Wasserläufer, das Wasser dunkel-klar.

**Fundstück.** Verdeckt: 0,00 an 42 Punkten ≤ 400 m, 3×3 9/9.

**Vorbild.** Real: Victoria amazonica (Pantanal), Riesenseerosen der Botanischen Gärten. Spiel: Seerosenteiche in Ori, Dragon Age: Inquisition
(Emprise du Lion, Teiche).

**Standort.** Feld H5, X 2890 / Y 725, Grund 0,5 m, Wasser 1,0 m: vorhandener Teich `T_2884_725` (4 805 m², Spiegel 1,58 m), Algen 37 %, Moos 27 %.
102 m im Biom; Weg 259 m; Zugang 292 m streng (max 17,7°), 34 m nass (Trittsteine aus `SM_dead_log_03`).

**Komposition und Anmarsch.** Durch das Röhricht an einer Lücke; die Teller staffeln sich von groß (vorn) nach klein (hinten).
Kameras: `_anmarsch` (X 2921 / Y 892, 170 m), `_held` (X 2890 / Y 845, 120 m), `_nah` (10 m).

**Detail-Ebenen.** Held: 15–25 Riesenblätter Rembrandt Water Lily `VarB` (flaches Blatt) ×2,5–4 (13c: „Riesenseerose durch Skalierung“),
Blüten `VarC/VarF` ×1,5. Begleiter: normale Seerosen `VarA/D/E/G` ×1 im Hintergrund, Trauerweide `Big_Tree_Willow_01` am Ufer. Schutt: treibende
Äste `SM_dead_log_03`. Bewuchs: Rohrkolbengürtel (`SM_Rohrkolben_Horst_6`, `SM_Rohrkolben_Jung_3`), Seggen `SM_ToadRush_014`, Grauweide
`SM_grey_willow_04`. Kontaktzone: Moos `SM_MossClump_05` am Ufer, `MI_Leakage_05`.

**Wasser, Effekte, Licht.** Vorhandener Teich; Farbe `smaragd` statt Standard (klar, dunkel). Kein Effekt.

**Geländeänderung.** Keine.

**Assets.** Bestand: Rembrandt Water Lily (7 Varianten, 13b), `SM_Rohrkolben_Horst_6`, `SM_Rohrkolben_Jung_3`, `SM_ToadRush_014`, `SM_grey_willow_04`,
`Big_Tree_Willow_01`, `SM_dead_log_03`, `SM_MossClump_05`. Wunsch: keiner mehr (Paket ist da).

**Aufwand und Risiko.** Niedrig. Risiko: skalierte Blätter ohne Randwulst → Materialwunsch nicht nötig, `VarB` hat einen flachen Rand;
im Prüfbild beurteilen.

### 8 · Die Irrlichtsenke (`sumpf_08_die_irrlichtsenke`) – Fundstück

**Was man sieht.** Eine Senke voller Totholz, in der der Nebel auch mittags nicht weicht. Der Boden ist schwarzer Faulschlamm, aus dem
Blasen steigen; es riecht nach faulen Eiern. Und dicht über dem Schlamm, im Schatten der umgestürzten Stämme, **glimmen schwache
gelbgrüne Lichter** auf und verlöschen wieder – Sumpfgas, sagen die Leute, Irrlichter sagen die anderen.

**Fundstück.** Verdeckt: 0,00 an 46 Punkten ≤ 400 m, 3×3 9/9.

**Vorbild.** Real: Faulgassenken in Mooren (Methan-Austritt), Nebelsenken des Dachauer Mooses. Spiel: Crookback Bog Nebelhexen-Atmosphäre
(Witcher 3), Fallow Mire (Dragon Age: Inquisition).

**Standort.** Feld H5, X 3085 / Y 795, Boden 2,3 m: Muldenlage (TPI100 −2,5 m), Laub/Algen/Moos/Kraut gemischt, Hang 2,5°; östlich des
Teichs `T_3042_746`. 86 m im Biom; Weg 178 m; Zugang 185 m streng (max 24,4°).

**Komposition und Anmarsch.** Vom Südrand hinab in die Mulde, die Stämme bilden einen dunklen Rahmen; die Lichter sitzen in der Tiefe der
Blickachse. Kameras: `_anmarsch` (X 3091 / Y 886, 91 m), `_held` (X 3085 / Y 877, 82 m), `_nah` (10 m).

**Detail-Ebenen.** Held: Nebelbank + 3–5 Glimmpunkte. Begleiter (6): tote Bäume `SM_Dead_Tree_03`, `SM_DeadTree_02`, liegend
`SM_LargeFallenTree_02`. Schutt (150): Stümpfe `SM_RottenTreeStump_01/02`, `SM_TreeStump_01`, `SM_dead_log_01`. Kleinzeug: Pilze
`SM_mushroom_01/02` an Totholz, Moos `SM_MossClump_01`. Bewuchs: kaum – Faulschlamm (Lage Schlamm 255), Binsen `SM_ToadRush_012` und
Rohrkolben-Jungpflanzen `SM_Rohrkolben_Jung_2` nur am Rand. Kontaktzone: Rinde `MI_ScatteredBark_01`, Moos `MI_TileableMossPatches_02`.

**Wasser, Effekte, Licht.** Schlammtümpel `see` (r 6 m, Spiegel +0,1 m, `moorbraun`). Nebel `BP_FogBankVolume` (13b) bzw. `lokaler_nebel`
(Dichte 0,12, Höhenabfall stark, Radius 30 m). Glimmen: `NS_Sparkling_Glow` (13b, Free Niagara Particles, CC BY 4.0 → Credits), gelbgrün, sehr
langsam; dazu 2 `punktlicht` (Intensität ≤ 2 cd, Radius 4 m, ohne Schatten) – wirkt nur im Schatten der Stämme.

**Geländeänderung.** Mulde −0,4 m. Fenster 70 × 60 m.

**Assets.** Bestand siehe oben; Effekte `BP_FogBankVolume`, `NS_Sparkling_Glow` (13b).

**Aufwand und Risiko.** Niedrig–mittel. Risiko: Glimmen wird bunt-magisch → gelbgrün, 1–3 s an, unregelmäßig, nie mehr als 3 gleichzeitig.

---

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/canyon/katalog.md](sehens/canyon/katalog.md)

### canyon_01_sonnenfenster – Das Sonnenfenster (Leuchtfeuer)

**Was man sieht:** Auf der Oberkante der Südstufe steht eine freie, 25 m lange Sandsteinfinne, rostrot mit hellen Bändern. In ihr
klafft ein Bogen von etwa 9 × 6 m – abends steht die Sonne genau darin. Unter der Finne ein Schuttkegel aus abgebrochenen Platten,
dahinter fällt die Stufe 40 m in die grüne Aue.
**Vorbild:** Delicate Arch / North Window (Arches NP); Spiel: Felsbögen im Toussaint-Hinterland (Witcher 3 B&W), Hissing Wastes (DA:I).
**Standort:** D4, X −1430 / Y −460 m, Boden 82,5 m. Plateaukante: Plateau 82 m, Stufenfuß 35–40 m (Profil x −1450: 82 → 41 m auf
75 m). Weg 113 m (Aue-Weg unter der Stufe), Stadtrand RES_CH49 202 m, 202 m im Biom.
**Sicht:** 174 von 300 Wegpunkten im Ring 300–800 m sehen ≥ 30 % der 14-m-Silhouette, mittlerer Anteil 0,41, bis 797 m; `_fern` vom
Weg bei X −962 / Y −632 (500 m) – der Bogen steht gegen den Himmel.
**Komposition und Anmarsch:** Vom Aue-Weg sieht man das Loch im Grat schon von weitem. Zugang 309 m, heute nur „weich“ (11 m mit
28°): **Zugangspfad mit drei Kehren** durch die Stufe (`pfad_cm`). `_held` 27 m westlich auf dem Plateau, Blick nach Osten: vorn
Slickrock mit Sukkulenten, Mitte Finne mit Bogen, hinten der Canyonausgang.
**Detail-Ebenen:** Held – Bogen aus zwei Pfeilern `SM_MassiveSandstoneCliff_03` + Sturz `SM_MassiveSandstoneCliff_02` (Akteure,
35 % eingegraben). Begleiter 4–6 – `SM_HugeSandstoneCliff_07` als Finnenfortsetzung, `SM_RockSandstone_040`, `SM_SandstoneBoulder_05`.
Schutt 60–120 – `SM_RockSandstone_034/021`, `SM_SandstoneBoulder_04`, `uldubik_tier_0` im Kegel unter dem Bogen (Ursache: Abplatzen
der Bogenunterseite). Kleinzeug – `SM_namaqualand_rocks_01_a_NN`, `SM_namaqualand_stones_01_c_NN`, `SM_SmallStonesPack_09`. Bewuchs –
Pioniere in Fugen (`SM_searsia_lucida_c_NN`, `SM_didelta_spinosa_small_NN`), Sukkulentenpolster (`SM_cheiridopsis_succulent_e_NN`) im
Windschatten, `SM_dead_grass_02`. Kontaktzone – Sandsaum am Fuß (`M_EL_Fels_Sand`), Fugen mit Kies.
**Wasser, Effekte, Licht:** keins. Bogen nach Süden offen – Schlagschatten auf die Stufe; kein Licht nötig.
**Geländeänderung:** keine (Netze auf der Kante); Bodenlage Felsplatte/Sandstein 25 m um die Finne.
**Assets:** Bestand wie oben. Wunsch: „Megascans Desert Western Cliff Layered XL 14 + Large 03“ (B, wird geladen) für eine echte
gebänderte Finne; Ersatz Bestand + `MI_EL_SW_Canyon_Rotband`. „Wadi Rum Sandstone Rock 01–04“ (C).
**Aufwand und Risiko:** mittel. Risiko: Bogen aus Klippenschalen wirkt zusammengesetzt → Fugen mit Schutt/Decal, Prüfbild `_held`.
Budget ca. 4 000 Instanzen (500 Kollision), 18 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

### canyon_02_der_waeger – Der Wäger (Leuchtfeuer)

**Was man sieht:** Auf der Kuppe einer schmalen Schichtrippe am Canyonausgang balanciert ein 6 m großer, rundgeschliffener Block auf
einem 9 m hohen Sockel mit Taille. Zwei kleinere Nadeln stehen daneben; hangab liegt ein Block, der schon gefallen ist.
**Vorbild:** Balanced Rock (Arches NP), Mushroom Rock (Kansas); Spiel: Felsnadeln in Skellige/Velen-Rand, Western Approach (DA:I).
**Standort:** D4, X −1049 / Y −415 m, Boden 68,7 m. Höchster Punkt einer NO-streichenden Rippe (Relief 33 m, Flanken bis 66°).
Weg 118 m (Weg im Canyonausgang), Stadtrand ROMAN_LOC_003 156 m, 42 m im Canyon-Rechteck.
**Sicht:** 126 von 345 Wegpunkten sehen ≥ 30 % des 15-m-Wägers, mittlerer Anteil 0,32, bis 789 m; `_fern` vom Aue-Weg bei X −1000 /
Y 108 (526 m).
**Komposition und Anmarsch:** Der Wäger steht als Fragezeichen über dem Weg. Zugang 128 m, streng (max 24,5°) – Trampelpfad als
Führung. `_held` 30 m südwestlich auf dem Rippenrücken, Blick NO: Rippe führt das Auge zum Wäger, dahinter die Wände der Wüste.
**Detail-Ebenen:** Held – Sockel `SM_MassiveSandstoneCliff_01` hochkant (40 % eingegraben), Kopf `SM_RockSandstone_040` ×1,6.
Begleiter – zwei Nadeln aus `SM_SandstoneBoulder_05` / `SM_HugeSandstoneCliff_02`. Schutt 40–80 – `SM_SandstoneBoulder_04`,
`SM_RockSandstone_034`, `uk5ebcp_tier_0` (Platten); gefallener Block 25 m hangab mit Schleifspur aus Kies. Kleinzeug –
`SM_namaqualand_rocks_01_b_NN`, `…stones_01_a_NN`. Bewuchs – ein Köcherbaum `SM_quiver_tree_02_NN` im Windschatten,
`SM_othonna_cerarioides_c_NN`, Trockengras. Kontaktzone – Sandkehle am Sockelfuß.
**Wasser, Effekte, Licht:** keins.
**Geländeänderung:** keine.
**Assets:** Bestand. Wunsch „Wadi Rum Sandstone Rock 01–04“ (C) – Block 01 als runder Kopf; „Procedural Rocks Generator“ (C) für den
Sockel mit Taille. Ersatz wie oben.
**Aufwand und Risiko:** gering. Risiko: Kopf darf nicht schweben – Auflage sichtbar schmal, 20 cm eingesunken.
Budget ca. 2 500 Instanzen, 8 Akteure.

### canyon_03_rote_stufe – Die Rote Stufe (Leuchtfeuer)

**Was man sieht:** Über dem Aue-Vorland erhebt sich die westliche Schichtstufe in vier Etagen: rote Wände, helle Gesimse, auf jedem
Sims Schuttkegel, oben der Ringrücken als Tafelberg-Sporn. Wo eine Bank fehlt, hängt ein Überhang mit Trockenrinne.
**Vorbild:** Vermilion Cliffs / Grand Staircase (Utah), Tafelberge des Monument Valley; Spiel: rote Felswände in Witcher-Zielbild 6,
Western Approach (DA:I).
**Standort:** C4, X −1910 / Y −460 m, Boden 28,3 m (Stufenfuß). Stufe von 28 auf 106–111 m (Ringrücken), Vorland Trockengras 95 %.
Weg 300 m (Grenzwert, Aue-Weg im Westen), Stadtrand ROMAN_LOC_010 254 m, 40 m im Biom; aue_02 ist 373 m entfernt.
**Sicht:** 106 von 268 Wegpunkten sehen ≥ 30 % der 25-m-Silhouette, bis 798 m; `_fern` X −2334 / Y −208 (493 m).
**Komposition und Anmarsch:** Vom Weg im Westen sieht man die Treppe frontal im Abendlicht. Zugang 368 m, flach (max 7°), quert einen
4 m breiten Bach (Trittsteine). `_held` 150 m östlich am Stufenfuß, Blick nach Westen über den Schuttkegel die Etagen hinauf.
**Detail-Ebenen:** Held – Stufenwand aus `vmnmbhv_tier_0` (40 × 29 × 23 m) und `ukjhcamga_tier_0` (geschichtet, 30 × 9 × 11 m) mit
`MI_EL_SW_Canyon_Rotband`. Begleiter 6–8 – `SM_MassiveSandstoneCliff_05/02`, `SM_HugeSandstoneCliff_05` als Etagenkanten. Schutt
100–180 – Kegel unter jeder Kante (`SM_SandstoneBoulder_04`, `SM_RockSandstone_034/021`, `SM_namaqualand_boulder_04_NN`), grob unten.
Kleinzeug – `SM_namaqualand_boulders_01_a_NN`, `…rocks_01_c_NN`, `SM_SmallStonesPack_11`. Bewuchs – Searsia-Gebüsch am Fuß
(`SM_searsia_burchellii_medium_NN`), eine Trockeneiche `SM_dry_oak_02_B`, Trockengras, Rooibos. Kontaktzone – Kegel 35 % im Boden.
**Wasser, Effekte, Licht:** Trockenrinne mit Nassband-Decal (`MI_Leakage_*`) unter dem Überhang.
**Geländeänderung:** Simse als flache Bänder (+1…−2 m) in der Stufe, Fenster ca. 220 × 180 m.
**Assets:** „Megascans Desert Western Cliff Layered XL 14 + Large 03“ (A, wird geladen) – die eigentliche Bänderwand; Ersatz
Bestand + Tönung.
**Aufwand und Risiko:** hoch (größte Form). Risiko: Kachelmuster der großen Schalen aus 300 m – Schalen drehen/mischen.
Budget ca. 9 000 Instanzen (900 Kollision), 30 Akteure.

### canyon_04_fluesterschlucht – Die Flüsterschlucht (Fundstück)

**Was man sieht:** Ein Bach auf dem Plateau verschwindet in einem Spalt, 2–6 m breit, 18 m tief, mit geschwungenen, glattgewaschenen
Wänden. Licht fällt als Streifen herab, ein verkeilter Klemmblock hängt über dem Wasser. Am Ende öffnet sich der Spalt: der Bach
fällt 25 m in den Hauptcanyon.
**Vorbild:** Antelope Canyon, Buckskin Gulch; Spiel: Felsspalten in Kaer-Morhen-Tälern, Shadow of the Tomb Raider (Slots).
**Standort:** D4, X −1235 / Y −848 m, Boden 81,5 m. Seitenbach (Einzugsfläche 41 000 m²) liegt heute flach auf dem Plateau und fällt
bei X −1300 von 70 auf 46 m (Hängetal). Weg 258 m, Stadtrand ROMAN_LOC_003 180 m.
**Sicht:** heute einsehbar (max. Anteil 0,59 aus 343 m); **mit Kerbe** (−18 m, 2–6 m breit, entlang der Wasserzellen) verdeckt
(0,00, 42 Wegpunkte ≤ 400 m geprüft).
**Komposition und Anmarsch:** Zugang 394 m streng (max 22°) über das Plateau. `_held` 130 m NO am Bach: man sieht nur eine dunkle
Fuge im Sand. `_nah` im Spalt (Kamera auf trockenen Fels verschoben).
**Detail-Ebenen:** Held – Spaltwände `SM_MassiveSandstoneCliff_01/02`, `SM_HugeSandstoneCliff_05` paarweise gespiegelt, oben
überkragend (Akteure). Begleiter – Klemmblock `SM_RockSandstone_040`, `SM_SandstoneBoulder_05`. Schutt – Bachgeröll
`SM_DryRiverBed_01/02`, `SM_stones_01_2`, `SM_RockSandstone_021`. Kleinzeug – Kiesel, Treibholz (`SM_bark_debris_01_c_NN`). Bewuchs
nach Ursache – Feuchte im Schatten: Farn `SM_fern_01_1`, Moos `SM_MossClump_03`, `SM_Vines_01a` an der Spaltwand, Binsen
`SM_ToadRush_02` am Eintritt. Kontaktzone – Nassband 0,5 m, Sandbänke in Kehren.
**Wasser, Effekte, Licht:** Bach (klar, 30 cm) durch den Spalt, Stufen > 0,8 m als kleine Fälle, Austritt als `wasserfall` 25 m in
den Canyon; ein `lokaler_nebel` (Dichte 0,05) im Spaltgrund; Lichtstreifen entstehen von selbst (Sonne 24°).
**Geländeänderung:** Kerbe −12…−18 m auf 120 m Länge, Fenster ca. 160 × 80 m (Ort IST das Wasser → Änderung am Bach erlaubt).
**Assets:** „Mountain – Environment Set“ (A, läuft) für das Fall-Material; „Megascans Desert Western Cliff…“ (B); „Fantasy
Ambiences“ (C, Wind). Ersatz `M_EL_Wasserfall2`.
**Aufwand und Risiko:** hoch. Risiko: Überhänge nur als Netze; Spalt muss begehbar bleiben (Sohle ≥ 2 m).
Budget ca. 5 000 Instanzen, 40 Akteure, 0 Lichter, 1 Nebel, 4 Decals.

### canyon_05_hoodoo_kessel – Der Hoodoo-Kessel (Fundstück)

**Was man sieht:** Der Canyonrand ist hier zu einem halbrunden Kessel zerfallen. In ihm stehen 14–18 schlanke, gebänderte Säulen mit
dunklen Decksteinen, Orange gegen Weiß; zum Fluss hin öffnet sich der Kessel.
**Vorbild:** Bryce Amphitheater (Utah), Goblin Valley; Spiel: Felsnadeln in Hissing Wastes (DA:I).
**Standort:** D4, X −1380 / Y −700 m, Boden 78,2 m. Rand der Mäanderschleife: Wand bis 72° zum Fluss (40 m), Einzugsfläche 178 000 m²
am Kesselrand. Weg 221 m, Stadtrand RES_CH49 189 m.
**Sicht:** verdeckt heute und mit Kessel-Stempel (−14 m, r 45 m): 0,00 aus 55 Wegpunkten.
**Komposition und Anmarsch:** Man kommt über das flache Plateau und steht plötzlich an der Kante. Zugang 315 m, „weich“ wegen steiler
Querhänge → Kehren am Kesselrand. `_held` an der Kante, Blick über die Hoodoos zum Fluss.
**Detail-Ebenen:** Held – Hoodoo-Schäfte aus `SM_MassiveSandstoneCliff_03` (schmal ×0,35, hoch ×1,2) und `SM_HugeSandstoneCliff_02`,
Decksteine `SM_RockSandstone_040`; `uchoab3fa_tier_0` als Kesselwand. Begleiter – `SM_SandstoneBoulder_05`. Schutt 80–150 –
`SM_SandstoneBoulder_04`, `SM_RockSandstone_034`, Sandschleppen `SM_sandy_slope_04` zwischen den Schäften. Kleinzeug –
`SM_namaqualand_rocks_01_d_NN`. Bewuchs – Köcherbaum `SM_quiver_tree_01_NN` auf einem Absatz, `SM_searsia_lucida_e_NN`,
Leipoldtia-Polster. Kontaktzone – Schäfte 30 % eingegraben, Schuttsaum.
**Wasser, Effekte, Licht:** Fluss unten (bestehend). Abends Gegenlicht durch die Säulen.
**Geländeänderung:** Kessel −14 m (r 45 m), offen zum Canyon (keine geschlossene Senke). Fenster 140 × 140 m.
**Assets:** „Hollowstone Canyon“ (B), „Procedural Rocks Generator“ (C), „Megascans Desert Western Cliff…“ (B); Lücke „Hoodoo-Netz“
in `asset_bedarf.json` mit Bestandslösung.
**Aufwand und Risiko:** hoch. Risiko: Säulen wirken geklont → je Säule andere Skalierung/Drehung/Tönung.
Budget ca. 6 000 Instanzen, 45 Akteure.

### canyon_06_die_kolke – Die Kolke (Fundstück)

**Was man sieht:** Eine Bank aus hellem Slickrock, darin ein halbes Dutzend runder, wassergefüllter Kolke (1–4 m), verbunden durch
Rinnen; im größten spiegelt sich der Himmel, Kaulquappen-grün am Rand. Der Überlauf rinnt Richtung Südstufe.
**Vorbild:** Potholes/Tinajas (Canyonlands), Kolkwannen im Elbsandstein; Spiel: Wasserlöcher in RDR2 (New Austin).
**Standort:** D4, X −1570 / Y −620 m, Boden 82,3 m. Ebenes Plateau (Hang 0–5°), 90 m oberhalb des Bachanfangs (Einzugsfläche
6 500 m²). Weg 299 m (Grenze), Stadtrand 332 m.
**Sicht:** verdeckt (0,00) – der Weg liegt 45 m tiefer unter der Stufe.
**Komposition und Anmarsch:** Zugang 392 m „weich“ (4 m mit 34° an der Stufe) → **Kehrenpfad über die Stufe** neben dem Bach.
`_held` 43 m nördlich, Blick über die Kolke zur Stufenkante und zur Aue.
**Detail-Ebenen:** Held – Slickrock-Platten `uk5ebcp_tier_0`, `uldubik_tier_0` (flach, 70 % eingegraben). Begleiter –
`SM_DryRiverBed_01/02` in den Rinnen, `SM_SandstoneBoulder_04`. Schutt – `SM_RockSandstone_021`. Kleinzeug – Kiesel im Kolkgrund.
Bewuchs – Binsenkränze `SM_ToadRush_013` nur an den Kolken, Eispflanzen-Polster in Fugen.
**Wasser, Effekte, Licht:** 6 `see` (Teich, farbe `klar`, 0,3–1,0 m, Umriss rund), Grund sichtbar.
**Geländeänderung:** Kolke je −0,8…−1,2 m (Stempel klein, mit Überlauf-Rinne), Fenster 80 × 80 m.
**Assets:** Bestand; „Coast & Dunes“ (B, läuft) Nass-Decals; Ersatz `MI_TileableLeakage_*`.
**Aufwand und Risiko:** gering–mittel. Risiko: Wasserflächen klein → Epic-Water-Mindestgröße prüfen.
Budget ca. 2 500 Instanzen, 10 Akteure, 6 Decals.

### canyon_07_smaragdgumpe – Die Smaragdgumpe (Fundstück)

**Was man sieht:** In einem halbrunden Alkoven der Südstufe fällt der Plateaubach in Fäden 38 m über die Bänder in eine smaragdgrüne
Gumpe. Die Rückwand ist schwarz-grün gestreift von Sickerwasser, aus den Fugen hängen Farne und Moos – ein hängender Garten. Ein
Felsriegel vorn verdeckt den Blick vom Weg.
**Vorbild:** Lower Calf Creek Falls, Weeping Rock (Zion); Spiel: versteckte Wasserfälle in Toussaint (Witcher 3 B&W).
**Standort:** C4/D4, X −1672 / Y −438 m, Boden 37,4 m. Bach läuft von 81 m (y −540) über 75 m (Kante, y −500) auf 37 m (y −430),
Einzugsfläche 65 000 m². Weg 194 m, Stadtrand ROMAN_LOC_019 339 m.
**Sicht:** heute knapp verdeckt (0,13); mit Alkoven (−6 m) + Felsriegel (+8 m, r 18 m südlich) 0,00.
**Komposition und Anmarsch:** Zugang 198 m streng (max 12°) aus der Aue; man geht hinter den Riegel und steht im Sprühnebel.
`_held` 24 m östlich im Alkoven, Blick auf Fall und Gumpe.
**Detail-Ebenen:** Held – Alkovenwand `SM_MassiveSandstoneCliff_05/02` mit `MI_EL_SW_Canyon_Gumpenmoos` (M_EL_Klippe_RVT, Moos im Band).
Begleiter – Riegel aus `SM_HugeSandstoneCliff_07`, `SM_SandstoneBoulder_05`, `SM_RockSandstone_040`. Schutt – Blöcke im Gumpenrand
(`SM_SandstoneBoulder_04`, `SM_stones_01_6`). Kleinzeug – Kiesel. Bewuchs nach Ursache – Sickerlinie: Farne `SM_fern_01_0`,
`SM_foliage_fern_01_2`, Moos `SM_MossClump_01`, `SM_moss_01`, Ranken `SM_Vines_01a`; Rohrkolben `SM_Rohrkolben_Jung_2` am Abfluss.
Kontaktzone – Nassband und Moos bis 2 m.
**Wasser, Effekte, Licht:** `wasserfall` 38 m (Kante bei y −480), `see` Gumpe r 9 m, farbe `smaragd`, 2,5 m tief, `bach` als Abfluss
in den bestehenden Aue-Bach; `lokaler_nebel` (Gischt) am Fuß, NS_SmokePuffLight weiß (optional). Schatten im Alkoven → kühles Grün.
**Geländeänderung:** Alkoven −6 m (r 22 m), Riegel +8 m (r 18 m), Gumpe −2,5 m; Fenster 100 × 100 m; Bach ist der Ort.
**Assets:** „Mountain – Environment Set“ (A, läuft) Fallmaterial; „Nature Water FX“ (läuft) Gischt; Ersatz `M_EL_Wasserfall2`.
**Aufwand und Risiko:** mittel–hoch. Risiko: Fall auf Stufen statt freier Fall – Kante mit Netz überkragen.
Budget ca. 6 000 Instanzen, 25 Akteure, 0 Lichter, 1 Niagara (optional), 1 Nebel, 5 Decals.

### canyon_08_die_welle – Die Welle (Fundstück)

**Was man sieht:** In einer Mulde zwischen Schichtrippen liegt eine Platte aus versteinerter Düne: Hunderte feiner Linien in Rot,
Ocker und Weiß schwingen wie gefrorene Wellen über den Fels, an einer Kante steigt die Kreuzschichtung als Wand auf.
**Vorbild:** The Wave (Coyote Buttes, Arizona); Spiel: farbige Felsen in Journey/Sea of Thieves (Stil), Hissing Wastes.
**Standort:** D4, X −876 / Y −288 m, Boden 55,1 m. Muldenhang (Hang 19°, Relief 43 m) zwischen den Rippen am Canyon-Ostrand,
131 m außerhalb des Canyon-Rechtecks (Schichtrippen gehören zur Canyonform; kleine Biome ≤ 150 m). Weg 136 m, Stadtrand 243 m.
**Sicht:** heute einsehbar (0,45 aus 300 m) → mit Mulde −5 m verdeckt (0,00, 177 Wegpunkte geprüft).
**Komposition und Anmarsch:** Zugang 157 m streng (max 19°). `_held` 44 m östlich auf der Rippe, Blick in die Mulde.
**Detail-Ebenen:** Held – Wellenplatte `uk5ebcp_tier_0` (Ledge Rock, flach) + `SM_HugeSandstoneCliff_07`, Tönung `MI_EL_SW_Welle`.
Begleiter – `uldubik_tier_0`, `SM_HugeSandstoneCliff_02`. Schutt – `SM_RockSandstone_021`, Sandschleppen `SM_sandy_slope_02`.
Bewuchs – fast keiner (blanker Fels), Eispflanze in Rissen.
**Wasser, Effekte, Licht:** keine; Wirkung im Streiflicht (Sonne 24°).
**Geländeänderung:** Mulde −5 m (r 32 m, mit Abfluss nach SW), Fenster 100 × 100 m; Bodenlage Sandstein/Felsplatte.
**Assets:** „Megascans Desert Western Cliff Layered XL 14 + Large 03“ (A, wird geladen) – nur damit wird die Welle glaubhaft; Ersatz
Tönung + Decal-Streifen (eigene Decal-Textur, prozedural – Wunsch an Claude lokal).
**Aufwand und Risiko:** mittel. Risiko: ohne Large 03 nur „rotes Plateau“ → Priorität A.
Budget ca. 1 500 Instanzen, 6 Akteure, 6 Decals.

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/wueste/katalog.md](sehens/wueste/katalog.md)

### wueste_01_yardang_flotte – Die Yardang-Flotte (Leuchtfeuer)

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

### wueste_02_sternduene – Die Sterndüne (Leuchtfeuer)

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

### wueste_03_die_waechter – Die Wächter (Leuchtfeuer)

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

### wueste_04_quelloase – Die Quelloase (Fundstück)

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

### wueste_05_salzpfanne – Die Salzpfanne (Fundstück)

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

### wueste_06_windkanterfeld – Das Windkanter-Feld (Fundstück)

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

### wueste_07_trockenes_wadi – Das Trockene Wadi (Fundstück)

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

### wueste_08_wabenwand – Die Wabenwand (Fundstück)

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

Biom-Katalog mit Herleitung aus den Daten, Materialwünschen und Abgleich 13b/13c: [sehens/oedland/katalog.md](sehens/oedland/katalog.md)

### oedland_01_rippenland – Das Rippenland (Leuchtfeuer)

**Was man sieht:** Über dem Wiesenrand steigt eine graue Badland-Kuppe auf, zerschnitten von Dutzenden paralleler Rinnen; dazwischen
Messerrücken, kaum handbreit, die Hänge bis 78° steil und nackt. Auf dem höchsten Grat ein abgestorbener Baum.
**Vorbild:** Badlands NP (South Dakota), Bardenas Reales; Spiel: Velen-Ödnis (Witcher 3), Western Approach (DA:I).
**Standort:** E6, X 20 / Y 1210 m, Boden 68,4 m. Kuppe (TPI100 +24,6 m, Relief 57 m, Sandstein 54 %, Trockengras 34 %) über dem
Ton-Flachland; die Rippen ragen über den Wiesengürtel (22–45 m) und sind vom Nordweg zu sehen. Weg 251 m (heute 272 m), Stadtrand
RES_CHEP_LOC_005 191 m.
**Sicht:** 27 von 155 Weg-/Pfadpunkten sehen ≥ 30 % der 15-m-Silhouette, bis 571 m; `_fern` X −122 / Y 1520 (vom Ödlandpfad, 336 m).
**Komposition und Anmarsch:** Zugang heute „weich“ (551 m, 17 m mit bis 35°) → **Kehrenpfad** vom Steinbruch-Weg. `_held` 120 m
westlich auf einem Nebengrat: die Rinnen laufen wie Rippen auf das Auge zu.
**Detail-Ebenen:** Held – Messerrücken aus `ukjhcamga_tier_0` (geschichtet) + `SM_HugeSandstoneCliff_05` mit `MI_EL_SW_Oedland_Ton`.
Begleiter – `SM_HugeSandstoneCliff_07`, `SM_big_rock_wall_02`. Schutt 80–150 – in jeder Rinne ein Schwemmkegel (`SM_Rock_02/05`,
`SM_s_rock_01`, `SM_sandy_slope_03`). Kleinzeug – `SM_SmallStonesPack_03`, `SM_s_rock_02`. Bewuchs – nur auf den Rückenkronen:
Trockengras, Sanddorn `SM_sea_buckthorn_05`; toter Baum `SM_DeadTree_02` (Blitz/Trockenheit). Kontaktzone – Popcorn-Ton als
Bodenlage Lehm, Rinnen mit Kies.
**Wasser, Effekte, Licht:** keine; Streiflicht.
**Geländeänderung:** Rinnen −1…−3 m (Kerbenmuster, je 6–10 m Abstand) auf der Südflanke; Fenster 260 × 200 m.
**Assets:** „Megascans Desert Western Cliff Layered XL 14 + Large 03“ (A, wird geladen); Ersatz Bestand + Tönung.
**Aufwand und Risiko:** mittel–hoch (Rinnenstempel). Risiko: Rinnen auf 2-m-Daten zu weich → 1-m-Lauf prüfen.
Budget ca. 6 000 Instanzen, 20 Akteure.

### oedland_02_regenbogenhang – Der Regenbogenhang (Leuchtfeuer)

**Was man sieht:** Eine 60 m hohe, steile Tonflanke in Bändern: Ziegelrot, Ocker, Violettgrau, Kreideweiß, wieder Rot – wie
gestrichen. Nach Regen leuchten die Farben, im Wind rieselt Popcorn-Ton in die Rinnen.
**Vorbild:** Painted Hills (Oregon), Zhangye Danxia; Spiel: bunte Felswände in Witcher-Zielbild 6, Exalted Plains (DA:I).
**Standort:** D6, X −880 / Y 1160 m, Boden 55,1 m. Westsporn der Abbruchkante (Hang 61°, Relief 64 m, Trockengras/Sandstein/
Geröll/Fels). Weg 224 m, Stadtrand RES_CH45 261 m.
**Sicht:** 29 von 212 Wegpunkten sehen ≥ 30 % der 15-m-Silhouette, bis 786 m; `_fern` X −768 / Y 1600 (vom Ödlandpfad, 454 m) –
vom Flachland aus steht der ganze Hang im Bild.
**Komposition und Anmarsch:** Vom Burgweg sieht man die bunte Oberkante über der Wiese. Zugang 285 m „weich“ → Kehren. `_held`
30 m östlich am Sporn; besser zusätzlich vom Ödlandpfad (`_fern`).
**Detail-Ebenen:** Held – Bänder aus `ukjhcamga_tier_0` ×4 mit `MI_EL_SW_Oedland_Rot/_Ocker/_Violett` + `MI_EL_SW_Oedland_Ton`,
`SM_HugeSandstoneCliff_07`. Begleiter – `SM_HugeSandstoneCliff_02`, `SM_big_rock_wall_01`. Schutt – Schwemmkegel farbig sortiert
(`SM_Rock_02/06`, `SM_s_rock_03`, `SM_sandy_slope_01`). Bewuchs – nichts im Hang (Ursache: Ton quillt), Trockengras/Sanddorn oben,
toter Baum `qlEtl_tier_0` am Fuß. Kontaktzone – Bänder laufen in die Bodenlagen Lehm/Erde aus.
**Wasser, Effekte, Licht:** keine.
**Geländeänderung:** Flanke +/−2 m geglättet für Bandfolge; Fenster 220 × 180 m.
**Assets:** „Megascans Desert Western Cliff Layered XL 14 + Large 03“ (A, wird geladen); Materialwünsche Rot/Ocker/Violett (≤ 6).
**Aufwand und Risiko:** mittel. Risiko: Bänder müssen durchlaufen (Nachbarschalen gleich ausrichten).
Budget ca. 4 000 Instanzen, 24 Akteure.

### oedland_03_hoellentor – Das Höllentor (Leuchtfeuer, am Ödlandpfad)

**Was man sieht:** Mitten im grauen Ton-Flachland klafft ein kreisrunder Krater, 40 m breit, 9 m tief. Sein Grund brennt: Hunderte
kleine Flammen in Rissen, die Wände rußig, darüber eine 30 m hohe Hitzesäule mit Rauch, die man vom Pfad aus von Weitem sieht.
Ringsum ein Saum verbrannter Erde, kein Halm.
**Vorbild:** Darvaza („Tor zur Hölle“, Turkmenistan); Spiel: Feuergruben in Mt. Gelmir (Elden Ring), Emprise du Lion (DA:I).
**Standort:** E6, X 180 / Y 1530 m, Boden 3,8 m. Ebene (Lehm 98 %, Hang 2°). Heute 625 m vom Weg → Ödlandpfad (Ast Ost) 133 m.
Stadtrand 537 m, 62 m im Biom.
**Sicht:** 7 von 63 Weg-/Pfadpunkten im Ring 300–800 m sehen ≥ 30 % der 30-m-Säule (eigene Messung; Prüfer `--sicht`: 10 Punkte, bis 788 m); `_fern` X −202 / Y 1548 (382 m).
**Komposition und Anmarsch:** Erst Rauch über dem Flachland, dann Wärme, dann der Rand. Zugang 139 m eben. `_held` 150 m nördlich
am Pfad, Rauch vor der Badland-Kante.
**Detail-Ebenen:** Held – Kraterwand aus `SM_big_rock_wall_03`, `SM_Big_Rock_01` mit `MI_EL_SW_Russ`. Begleiter – `SM_Big_Rock_02`,
`SM_Rock_01`. Schutt – Abbruchschollen `SM_Rock_04/07`, `SM_s_rock_01` am Kratergrund. Bewuchs – nichts im Saum (Hitze), außen tote
Halme, ein toter Baum `SM_DeadTree_01` (verbrannt).
**Wasser, Effekte, Licht:** `niagara` `/Game/NiagaraExamples/FX_Misc/NS_Fire` (×4 im Grund), `…/FX_Smoke/NS_Smoke_Plume` (Säule),
`…/FX_Sparks/NS_Spark_Continuous` (alle vorhanden seit 13b; im Plan vorerst `optional: true`, wie der Prüfer verlangt); 2 Punktlichter orange (12 000 cd, r 25 m,
ohne Schatten) im Grund; Decal Ruß. Glut nur in der Tiefe → wirkt auch am Tag.
**Geländeänderung:** Krater −9 m (r 22 m), steile Wand; Fenster 100 × 100 m. Keine geschlossene Senke ohne Inhalt: das Feuer ist der
Inhalt (Abfluss nicht nötig, es regnet nicht).
**Assets:** Niagara vorhanden; „Lava & Volcano – Environment Set“ (A, läuft) Glut-Decals/Hitzeflimmern; „Ultimate Niagara
Environmental VFX“ (B); „Fantasy Ambiences“ (B, Fauchen).
**Aufwand und Risiko:** mittel. Risiko: Kampf-Optik der Example-Effekte → Flammen klein und viele.
Budget ca. 1 500 Instanzen, 12 Akteure, 2 Lichter, 3 Niagara, 4 Decals.

### oedland_04_dornbusch_senke – Die Dornbusch-Senke (Fundstück)

**Was man sieht:** Am Westrand der Kante, wo ein Bach unter die Wiese taucht, liegt eine Senke voller grauer Dornbüsche, dazwischen
umgestürzte Stämme und ein toter Baum, dessen Äste wie Finger aus dem Gestrüpp ragen. Wildwechsel führt zum Bach.
**Vorbild:** Dornbuschsavanne/Mallee, Velen-Gestrüpp; Spiel: Crookback Bog-Ränder (Witcher 3).
**Standort:** D6, X −1210 / Y 1040 m, Boden 47,3 m. Verebnung (Hang 3°) über dem Westbach (44 m entfernt), Trockengras 53 %, Wiese 28 %.
Weg 290 m, Stadtrand ROMAN_LOC_016 287 m.
**Sicht:** verdeckt (0,00, 41 Wegpunkte).
**Komposition und Anmarsch:** Zugang 343 m streng (max 22°). `_held` 45 m nordwestlich.
**Detail-Ebenen:** Held – toter Baum `SM_Dead_Tree_02`. Begleiter – Dornbüsche `SM_didelta_spinosa_large_NN`,
`SM_searsia_burchellii_large_NN`, Sanddorn `SM_sea_buckthorn_02`. Schutt – Stämme `SM_dead_log_01/03`, `SM_Rock_03`. Kleinzeug –
`SM_bark_debris_01_b_NN`, Zweige `SM_dead_quiver_branch_02_NN`. Bewuchs – dichter Dornriegel am Rand (Ursache: Grundwasser des Bachs),
innen Trockengras.
**Wasser, Effekte, Licht:** ein `lokaler_nebel` in der Senke (Dichte 0,04).
**Geländeänderung:** Senke −1,5 m mit Abfluss zum Bach; Fenster 100 × 100 m.
**Assets:** Bestand; „Free City & Nature Sounds“ (vorhanden, Grillen/Wind).
**Aufwand und Risiko:** gering.
Budget ca. 5 000 Instanzen, 6 Akteure, 1 Nebel.

### oedland_05_kugelsteine – Die Kugelsteine (Fundstück)

**Was man sieht:** Wo eine Badland-Rinne auf das Flachland mündet, hat die Flut einen Geröllfächer geschüttet und in seiner Mitte einen
9 m tiefen Kolk gerissen. In dessen Ton-Wänden stecken dunkle, fast perfekte Steinkugeln – manche halb frei, eine liegt am Grund.
**Vorbild:** Bisti/De-Na-Zin (New Mexico), Moeraki Boulders; Spiel: Felskugeln in Breath of the Wild (Gerudo), Velen.
**Standort:** E6, X −600 / Y 1400 m, Boden 6,7 m. Rinnenmündung (Einzugsfläche 71 000 m²) am Fuß der Kante. Weg 294 m (Burgweg),
Ödlandpfad 94 m; Stadtrand ROMAN_LOC_020 164 m.
**Sicht:** heute offen (1,00 – vom Pfad aus); mit Kolk −9 m (r 22 m) verdeckt (0,00, 98 Punkte).
**Komposition und Anmarsch:** Vom Pfad sieht man nur den grauen Fächer; am Kolkrand öffnet sich der Blick. Zugang 95 m eben.
`_held` 120 m nördlich hangauf.
**Detail-Ebenen:** Held – Kugeln `SM_SandstoneBoulder_04`, `SM_namaqualand_boulder_04_NN` (×0,6–1,6) mit `MI_EL_SW_Konkretion`.
Begleiter – `SM_Big_Rock_02`, `SM_Middle_Rock_01`. Schutt – Fächer aus `SM_Rock_07`, `SM_s_rock_02`, `SM_stones_01_1` (grob am
Scheitel, fein am Rand). Bewuchs – Trockengras nur am Fächerrand.
**Wasser, Effekte, Licht:** keine.
**Geländeänderung:** Fächer +1,5 m, Kolk −9 m mit Auslauf; Fenster 120 × 120 m.
**Assets:** Bestand; „Wadi Rum…“ (C).
**Aufwand und Risiko:** gering–mittel.
Budget ca. 3 000 Instanzen, 14 Akteure.

### oedland_06_schlammvulkaene – Die Schlammvulkänchen (Fundstück, am Ödlandpfad)

**Was man sieht:** Neben dem alten Kraterring liegt in einer flachen Mulde ein Feld grauer Kegel, 1–3 m hoch, jeder mit nassem Krater,
in dem Schlamm blubbert und über den Rand quillt; Schlammzungen laufen wie Lava aus. Es riecht nach Erdöl.
**Vorbild:** Gobustan (Aserbaidschan), Salsen von Berca; Spiel: Schlammtöpfe in Skyrim (Eastmarch), Hinterlands (DA:I).
**Standort:** E6, X −284 / Y 1636 m, Boden 4,5 m. Geröll-/Tonfläche 86 m südöstlich des Kraterrings (Ring = Mutterkegel). Heute
589 m vom Weg → Ödlandpfad (Ast Ost) 112 m.
**Sicht:** verdeckt mit Mulde −3,5 m (0,00; heute 0,09).
**Komposition und Anmarsch:** Zugang 116 m streng. `_held` 25 m nordöstlich, Ring im Hintergrund.
**Detail-Ebenen:** Held – Kegel als Geländestempel (Bodenlage Schlamm). Begleiter – `SM_Rock_02`, `SM_s_rock_03` im Schlamm.
Kleinzeug – `SM_stones_01_4`, `SM_SmallStonesPack_01`. Bewuchs – nichts im Feld, Trockengras am Rand.
**Wasser, Effekte, Licht:** je Krater `see` (farbe `moorbraun`, 0,3 m); `niagara` `NS_Bubble_Burst` + `NS_SmokePuffLight` (vorhanden).
**Geländeänderung:** Mulde −3,5 m, 6–8 Kegel +1…+3 m mit Kratern; Fenster 140 × 140 m.
**Assets:** Niagara vorhanden; „Lava & Volcano – Environment Set“ (A, läuft) Blasen/Bodensets.
**Aufwand und Risiko:** mittel. Risiko: Abgrenzung zu Schlammtöpfen im Sumpf – hier Kegel auf trockenem Ton.
Budget ca. 1 500 Instanzen, 6 Akteure, 2 Niagara.

### oedland_07_totenpfanne – Die Totenpfanne (Fundstück, am Ödlandpfad)

**Was man sieht:** Der Badland-Bach endet in einer weißen, gerissenen Tonpfanne. Darin stehen schwarze, tote Bäume – vor Jahrhunderten
ertrunken, dann verdorrt, nie verrottet. Kein Laut außer Wind.
**Vorbild:** Deadvlei (Namibia); Spiel: tote Wälder in Velen, Fallow Mire (DA:I).
**Standort:** D6, X −820 / Y 1720 m, Boden 4,0 m. Endpfanne (Einzugsfläche 1,25 km², Lehm 50 %, Erde 33 %, Hang 2°). Heute 665 m vom
Weg → Ödlandpfad (Ast West) 124 m.
**Sicht:** mit Pfanne −3,5 m verdeckt (0,00; heute offen 1,00).
**Komposition und Anmarsch:** Zugang 127 m eben. `_held` 80 m westlich, Gegenlicht: schwarze Silhouetten auf Weiß.
**Detail-Ebenen:** Held – `SM_Dead_Tree_01/03`, `qlEtl_tier_0` (schwarz getönt). Begleiter – `SM_DeadTree_01/02`,
`SM_EuropeanBeech_Dead_M_01`. Schutt – `SM_dead_log_02/04`. Bewuchs – keiner in der Pfanne, Trockengras am Rand.
**Wasser, Effekte, Licht:** keins (trocken); Riss-Decals hell.
**Geländeänderung:** Pfanne −3,5 m (r 50 m) mit Überlauf zum Meer; Fenster 140 × 140 m.
**Assets:** Bestand; „Coast & Dunes“ (B) Riss-/Ton-Decals.
**Aufwand und Risiko:** gering.
Budget ca. 1 000 Instanzen, 12 Akteure, 8 Decals.

### oedland_08_erdroehren – Die Erdröhren (Fundstück, am Ödlandpfad)

**Was man sieht:** Am Lehmhang über dem Westbach ist der Boden durchlöchert: drei Schlucklöcher bis 7 m tief, verbunden durch Tunnel,
eine schmale Erdbrücke spannt über den größten Schacht. Unten hört man Wasser tropfen.
**Vorbild:** Piping/Tunnel-Erosion in Badlands (Dinosaur Provincial Park, Loess-Plateau); Spiel: Erdhöhlen in Velen.
**Standort:** D6, X −1080 / Y 1460 m, Boden 13,8 m. Hang (11°) über dem Westbach (94 m). Heute 581 m vom Weg → Ödlandpfad 220 m.
**Sicht:** mit Löchern −4…−7 m verdeckt (0,00).
**Komposition und Anmarsch:** Zugang 233 m eben. `_held` 120 m südlich.
**Detail-Ebenen:** Held – Erdbrücke aus `SM_big_rock_wall_01` (Ton-Tönung). Begleiter – `SM_Rock_05/03`. Schutt – `SM_s_rock_01`,
`SM_stones_01_5` am Grund. Bewuchs – Sanddorn `SM_sea_buckthorn_04`, Farn `SM_Fern_01a` im feuchten Schacht.
**Wasser, Effekte, Licht:** ein `lokaler_nebel` im Hauptschacht.
**Geländeänderung:** drei Schächte (−7/−5/−4 m), mit Abfluss zum Bach; Fenster 100 × 100 m.
**Assets:** Bestand; „Cave Ambience“ (B).
**Aufwand und Risiko:** mittel (Tunnel als Netze).
Budget ca. 1 500 Instanzen, 10 Akteure, 1 Nebel.

