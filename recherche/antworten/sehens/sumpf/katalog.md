# Sumpf – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

Stand 11.10.2026 · Agent B8 · Dateien: `standorte.json` (Prüfer **0 FEHLER, 0 WARNUNG**, 5 HINWEIS „_anmarsch x m vom Weg“ = Kamera am
Zugang), je Ort `<id>.png` (Draufsicht 2 m mit geplanten Elementen, Zugang gelb, Kameras), `asset_bedarf.json`. Zahlen aus den 2-m-Daten mit
`antworten/skripte/sehens_lib`; eigene Skripte im Scratchpad `a13/b8_kueste_sumpf/` (`sumpfwasser.py` Wasserspiegel des Epic-Sees,
`s11_sumpf_kand.py` Kandidatenraster 20 m mit Nässe/Moor/Baumdichte, `s12_typen.py` Scores je Ortstyp, `s13_sicht_sumpf.py` Sicht für alle
1 855 Kandidaten, `s22_sumpf_eval.py`, `build.py`). Kameras nach §8 (11.10. 13:00): `_anmarsch`/`_nah` Hoch −170 mit echtem Ziel.

## Das Biom in den Daten

- **0,99 km²**, ein Rechteck X 2462 … 3460, Y −118 … 880 (H5 78 %, I5, H4, I4). Eine flache **Senke 0–2 m über dem Meer** (Median 2,0 m),
  im Norden der Anstieg zum Elfenwald-Hügel (bis 190 m, Laub).
- **Das Wasser steht nicht in `wasser_2m`:** der Sumpf ist ein Epic-See `T_2954_391` (28 ha, Spiegel **1,58 m**) plus 20 kleine Teiche
  `T_*` mit demselben Spiegel. Ich habe die Umrisse aus `wasser_welt.json` gerastert (`sumpfwasser.py`): **22 % der Biomfläche stehen unter
  Wasser**, Tiefe Median 0,66 m (90 % 1,22 m); die 77 „Meer“-Zellen (Gelände < 0) liegen zu 78 % unter diesem See und sind Süßwasser.
- Boden: Laub 29 %, Algen 17 %, Moos 15 %, Gras 15 %, Kraut 13 %, Schlamm 12 %. Bäume (4-m-Karte): fast keine in der Senke
  (Baumdichte 40 m meist < 5 %) – der Sumpf ist offen, Röhricht ist nicht in der Baumkarte.
- **Wege:** Stichweg im Westen (Ende X 2400 / Y 250), Wegende im Osten (X 3400 / Y 330), Straße am Südrand (Y 950–1000). 80–300 m vom Weg und
  erlaubt: 0,80 km² (inkl. 150-m-Zone), innen 0,47 km². Die Mitte (X 2750–3150, Y 100–500) ist > 300 m von jedem Weg.
- **Verdeckung ist hier selten:** von 1 855 erlaubten Kandidaten sind nur 501 für einen 3-m-Ort vom Weg verdeckt – fast alle im Südstreifen
  (Y 680–880), wo der Südrand mit Wald und Hügeln die Straße abschirmt. West- und Ostteil sind vom Weg aus offen einsehbar. Deshalb stehen
  vier Fundstücke im Südstreifen (je ~205 m Abstand), das fünfte (Erlenbruch) verdeckt sich selbst mit seinem Erlenring.
- Heute (Bilder `NAH2_H5_sumpf_nah0`, `BIOM1_H5_rundgang`): Rohrkolben in gleichmäßigem Raster auf hellem Wasser, Trauerweiden, wenige
  weiße tote Stämme, alles gleich hell; Wasser ohne Spiegelung, keine Bulten, kein Torf, kein Totholz im Wasser, kein Nebel.
- **Leitidee:** Jeder Ort zeigt, **wie der Sumpf lebt und stirbt** – er ertränkt den Wald (Ertrunkener Wald), er baut Torf und schwimmende
  Matten (Schwingrasen), er wächst in Bulten (Bultenfeld), er nährt Riesenblätter (Tellerweiher), Vögel nisten über ihm (Reiherhorst),
  Bäume stellen sich auf Stelzen (Erlenbruch, Weidendom), und er atmet Gas und Nebel aus (Irrlichtsenke). Farbe: schwarzes Wasser, rostrotes
  Torfmoos, silbernes Totholz, giftgrüne Wasserlinsen – Dragon-Age-Palette, nie grau-braun.

## Prüfung

- `sehens_pruefen.py` (alle Biome, mit Daten): für den Sumpf **0 FEHLER, 0 WARNUNG**; globale Abstände inkl. `standorte_steige.json` und
  `standorte_kratersteig.json`: kein Konflikt (nächster Fremdort 405 m: `heide_02_ginstergold`).
- Abstände untereinander ≥ 202 m (Schwingrasen – Tellerweiher 202 m, Bultenfeld – Irrlichtsenke 206 m; Regel kleine Biome 200 m).
- Alle Orte im Biom (20–102 m innen), 154–286 m vom Weg, Stadtrand ≥ 401 m. Fußweg vom Weg überall **streng ≤ 25°** (max 24,4°);
  nasse Strecken auf dem Zugang (Epic-See) 0–94 m → Bultenpfad/Trittsteine (unten je Ort).

## Übersicht

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden z | Radius | Weg | Nachweis (sicht.py) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `sumpf_01_der_ertrunkene_wald` | Der Ertrunkene Wald | Leuchtfeuer | H5 | 2610 / 160 | 1,0 m (Wasser 0,6 m) | 70 m | 154 m | 18 m: **50 / 154** Punkte (300–800 m), bis 731 m; bester 502 m, 1,0 |
| 2 | `sumpf_02_der_weidendom` | Der Weidendom | Leuchtfeuer | H5/I5 | 3350 / 580 | 0,5 m (Wasser 1,1 m) | 55 m | 198 m | 22 m: **9 / 120**, bis 635 m; bester 564 m, 0,97 |
| 3 | `sumpf_03_der_reiherhorst` | Der Reiherhorst | Leuchtfeuer | H5 | 2650 / 380 | 2,0 m | 50 m | 272 m | 20 m: **65 / 204**, bis 746 m; bester 495 m, 1,0 |
| 4 | `sumpf_04_der_schwingrasen` | Der Schwingrasen | Fundstück | H5 | 2690 / 700 | 2,2 m | 50 m | 286 m | verdeckt: 0,00 an 30 Punkten ≤ 400 m; 3×3 9/9 |
| 5 | `sumpf_05_der_erlenbruch` | Der Erlenbruch | Fundstück | H4 | 2560 / −110 | 13,1 m | 50 m | 286 m | verdeckt mit Erlenring: 0,00 an 39 Punkten; 3×3 9/9 (ohne Ring 6/9) |
| 6 | `sumpf_06_das_bultenfeld` | Das Bultenfeld | Fundstück | H5/I5 | 3290 / 780 | 2,5 m | 45 m | 273 m | verdeckt: 0,00 an 36 Punkten; 3×3 9/9 |
| 7 | `sumpf_07_der_tellerweiher` | Der Tellerweiher | Fundstück | H5 | 2890 / 725 | 0,5 m (Wasser 1,0 m) | 50 m | 259 m | verdeckt: 0,00 an 42 Punkten; 3×3 9/9 |
| 8 | `sumpf_08_die_irrlichtsenke` | Die Irrlichtsenke | Fundstück | H5 | 3085 / 795 | 2,3 m | 50 m | 178 m | verdeckt: 0,00 an 46 Punkten; 3×3 9/9 |

Gegenüber Katalog v1 übernommen: **Geisterwald** (jetzt **Ertrunkener Wald**, tote Fichten), **Irrlichtweiher** (jetzt **Irrlichtsenke**, natürlich:
Nebel + schwaches Faulgasglimmen), **Mooraugen** (jetzt **Schwingrasen** mit drei Augen), **Tellerweiher**, **Weidendom**. Ersetzt:
**Schlammtöpfe** (Ödland hat Schlammvulkane; im Sumpf ohne Wärmequelle unglaubwürdig), **Blüteninsel** (ohne Begründung im Gelände),
**Ewige Flamme** (würde Glut/Feuer in ein Wasserbiom bringen; als dezentes Glimmen in der Irrlichtsenke aufgegangen). Neu: **Reiherhorst**,
**Bultenfeld**, **Erlenbruch**.

**Einmaligkeit:** Ertrunkener Wald ≠ Biberstau (aue: Damm als Held, 3 ertrunkene Fichten) – hier **50 silberne Fichtenleichen** in schwarzem
Wasser, kein Damm. Weidendom ≠ Mondarm (aue, Altwasser mit Weidensaum) ≠ Lianenhalle – hier **ein geschlossener Ring aus Riesenweiden im
Wasser**, Dach geschlossen, Schwarzspiegel innen. Schwingrasen ≠ `heide_04_der_kolk` (Heideweiher) ≠ `tundra_08_das_wabenmoor` (Strangmoor) –
hier **schwimmende Torfmoosdecke**, die beim Betreten schwankt, mit drei tintenschwarzen Augen. Tellerweiher ≠ Mondarm (normale Seerosen) –
**Riesenseerosen 3–5 m**. Erlenbruch ≠ Lianenhalle/Blauer Grund – **Stelzwurzel-Bäume in Schwarzwasser am Quellhang**. Reiherhorst ≠ Brandkiefer
(bergwald, Blitzbaum) ≠ Vogelinsel (küste, Seevögel) – **Kolonie von Graureihern in toten Baumriesen** über dem offenen Sumpf.
Irrlichtsenke ≠ Nebelhain (elfenwald, Nebelwald am Grat) – **Bodennebel über Faulschlamm in einer Senke** mit schwachem Glimmen.

---

## 1 · Der Ertrunkene Wald (`sumpf_01_der_ertrunkene_wald`) – Leuchtfeuer

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

## 2 · Der Weidendom (`sumpf_02_der_weidendom`) – Leuchtfeuer

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

## 3 · Der Reiherhorst (`sumpf_03_der_reiherhorst`) – Leuchtfeuer

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

## 4 · Der Schwingrasen (`sumpf_04_der_schwingrasen`) – Fundstück

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

## 5 · Der Erlenbruch (`sumpf_05_der_erlenbruch`) – Fundstück

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

## 6 · Das Bultenfeld (`sumpf_06_das_bultenfeld`) – Fundstück

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

## 7 · Der Tellerweiher (`sumpf_07_der_tellerweiher`) – Fundstück

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

## 8 · Die Irrlichtsenke (`sumpf_08_die_irrlichtsenke`) – Fundstück

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

## Bildwünsche (Kameras in `standorte.json`)

- `sumpf_01_der_ertrunkene_wald_fern` – offenes Wasser heute (Epic-See 1,58 m) vom Westweg
- `sumpf_07_der_tellerweiher_held` – Teich `T_2884_725` heute: Ufer, Röhricht

## Offene Fragen an Ferat

1. Darf der Epic-See `T_2954_391` stellenweise eine eigene Wasserfarbe bekommen (schwarz_spiegel im Ertrunkenen Wald/Weidendom), oder bleibt
   der Sumpf einheitlich?
2. Erlenbruch mit Birken/Pappeln jetzt bauen (13c) und das Erlenpaket später nachziehen – einverstanden?
3. Irrlichter als `NS_Sparkling_Glow` mit 2 schwachen Punktlichtern – oder ganz ohne Licht, nur Nebel?
