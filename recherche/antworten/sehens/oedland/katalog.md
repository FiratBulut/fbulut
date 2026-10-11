# Ödland – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1, Biom-Agent B6)

Stand 11.10.2026 · Daten: `vorlagen/daten/sehens` (2 m) · Werkzeuge: `antworten/skripte/sehens_lib` · Dateien: `standorte.json`
(8 Orte + 3 Pfade „Ödlandpfad“ in `pfade[]`, Prüfer **0 FEHLER / 0 WARNUNG**), `asset_bedarf.json`, `<id>.png` je Ort.

## Das Wichtigste vorweg: Die Badlands haben keinen Weg

Das Ödland-Rechteck (1,92 km², D6/E6/E7) besteht aus drei Teilen: im Norden ein **grüner Wiesengürtel** auf 50–77 m (Wege, Burg
Aethelburg = ROMAN_LOC_020, Außenposten), darunter eine 40–60 m hohe **Abbruchkante mit Badlands** (Rinnen, Messerrücken, bunte
Bänder) und südlich davon das **Ton-Flachland** (Lehm, 3–7 m) mit Zeugenbergen, einem Kraterring und Bächen, die versickern.
Der einzige Weg endet an der Burg.

| Kennzahl | Wert |
|---|---|
| Fläche ≤ 300 m vom Weg | 0,56 km² (80–300 m: 0,47 km²; nach Stadt-/Ortsabstand 0,18 km²) |
| davon mit Ödland-Boden (Lehm/Geröll/Sandstein/Erde/Fels ≥ 50 %) | **0,064 km²** – der Rest ist Wiese, Moos, Nadelstreu |
| größter Wegabstand | 1 586 m; ≤ 800 m: 1,66 km² |
| Packung 350 m, nur Ödland-Boden, ≤ 300 m | **4 Orte** (bei ≤ 400 m: 6) |

**Lösung (nach 13c „lieber ein Pfad mehr als ein Ort weniger“):** 4 Orte gelten mit dem heutigen Wegenetz, 4 weitere am neuen
**Ödlandpfad** (in `standorte.json` → `pfade[]`, Orte mit `pfad_id`):

| Pfad-ID | Art | Länge | max. / mittl. Steigung | Verlauf |
|---|---|---|---|---|
| oedland_pfad_oedlandpfad_abstieg | serpentine | 521 m | 19,8° / 7,7° | Burgweg Aethelburg (Abzweig X −616 / Y 1074, außerhalb des Burgradius 130 m) → Kehren westlich der Burg die Kante hinab → Fuß bei X −505 / Y 1345 |
| oedland_pfad_oedlandpfad_ost | trampelpfad | 844 m | 7,9° / 1,8° | Fuß → am Kraterring vorbei → Ton-Flachland → X 69 / Y 1457 |
| oedland_pfad_oedlandpfad_west | trampelpfad | 567 m | 7,9° / 0,9° | Fuß → südlich der Kugelsteine → Endpfanne des Badland-Bachs → X −899 / Y 1585 |

Breite 1,5 m, Bodenlage Erde/Kies als Band; im Abstieg Kehren mit Trittstufen (`SM_RockSandstone_021/034`). Der Pfad hält ≥ 94 m
Abstand zu allen 8 Ortsmitten. Gegen Wege + Pfad erfüllen alle Orte 80–300 m, Sicht und Erreichbarkeit.

## Übersicht

| ID | Name | Art | Form | Feld | X / Y (m) | Weg (heute) | Status |
|---|---|---|---|---|---|---|---|
| oedland_01_rippenland | Das Rippenland | Leuchtfeuer | Badlands mit Rinnenerosion | E6 | 20 / 1210 | 251 m (272) | regelkonform |
| oedland_02_regenbogenhang | Der Regenbogenhang | Leuchtfeuer | bunt gebänderte Tonflanke | D6 | −880 / 1160 | 224 m (234) | regelkonform |
| oedland_03_hoellentor | Das Höllentor | Leuchtfeuer | brennender Gaskrater | E6 | 180 / 1530 | 133 m (625) | am Ödlandpfad |
| oedland_04_dornbusch_senke | Die Dornbusch-Senke | Fundstück | Dornbusch-Hohlform am Bach | D6 | −1210 / 1040 | 290 m | regelkonform |
| oedland_05_kugelsteine | Die Kugelsteine | Fundstück | Konkretionen im Kolk eines Geröllfächers | E6 | −600 / 1400 | 94 m (294) | regelkonform |
| oedland_06_schlammvulkaene | Die Schlammvulkänchen | Fundstück | Salsenfeld am Kraterring | E6 | −284 / 1636 | 112 m (589) | am Ödlandpfad |
| oedland_07_totenpfanne | Die Totenpfanne | Fundstück | Ton-Endpfanne mit toten Bäumen | D6 | −820 / 1720 | 124 m (665) | am Ödlandpfad |
| oedland_08_erdroehren | Die Erdröhren | Fundstück | Piping: Schlucklöcher und Tunnel im Ton | D6 | −1080 / 1460 | 220 m (581) | am Ödlandpfad |

Mischung 3 / 5. Erzählung: Der Ton zerfällt an der Kante zu **Rippen** (01) und **Farbbändern** (02); Flutwasser trägt das Material
hinab, kolkt die **Kugelsteine** frei (05), frisst **Röhren** in den Ton (08) und verdunstet in der **Totenpfanne** (07). Im Untergrund
gärt Gas: es blubbert in den **Schlammvulkänchen** (06) und brennt im **Höllentor** (03). Oben am Wiesenrand die **Dornbusch-Senke** (04).
**Geröllfächer** ist kein eigener Ort mehr (auf offener Fläche vom neuen Pfad aus nicht verdeckbar) – er ist die Bühne der Kugelsteine.
**Abgrenzung:** Ton/Badland, Gas, Schlamm. Nicht hier: Sandstein-Hoodoos/Bögen (Canyon), Salzpfanne (Wüste – Salz, Küste),
Fumarolen/Schwefel (lava_02), Lavaröhren (lava_04), Lehm-Prallhang (aue_03). Der Regenbogenhang wurde vom Lava-Biom abgegeben.
**Sichtmessung, Kameras:** wie im Canyon-Katalog; Wege inklusive `pfade[]` aller Biome (13c).

---

## oedland_01_rippenland – Das Rippenland (Leuchtfeuer)

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

## oedland_02_regenbogenhang – Der Regenbogenhang (Leuchtfeuer)

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

## oedland_03_hoellentor – Das Höllentor (Leuchtfeuer, am Ödlandpfad)

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

## oedland_04_dornbusch_senke – Die Dornbusch-Senke (Fundstück)

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

## oedland_05_kugelsteine – Die Kugelsteine (Fundstück)

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

## oedland_06_schlammvulkaene – Die Schlammvulkänchen (Fundstück, am Ödlandpfad)

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

## oedland_07_totenpfanne – Die Totenpfanne (Fundstück, am Ödlandpfad)

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

## oedland_08_erdroehren – Die Erdröhren (Fundstück, am Ödlandpfad)

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

## Offene Fragen an Ferat (Ödland)

- **Ödlandpfad bauen?** (3 Äste, 1,93 km, Serpentine 19,8° im Abstieg). Ohne Pfad hat das Ödland 4 Orte.
- Darf das Höllentor 2 Punktlichter + 3 Niagara nutzen (Budget-Grenze)?

## Abgleich Inventar 13d (Stand 11.10.2026, abends)

Neues Inventar: 1 965 Netze, 116 Niagara, 85 Decals. Pfade, Maße und Paketstatus stehen in `asset_bedarf.json` → `abgleich_13d`. Orte und Kameras bleiben unverändert; die Phase-2-Planer werden gerade auf die echten Assets umgestellt.

**Jetzt erfüllt:**

- `oedland_01_rippenland` – Desert Western: gebänderte Wandstücke für Messerrücken (A): `uk5oded_tier_0 (Desert_Western_Cliff_Layered_XL_02)`, `veonegs_tier_0 (Desert_Western_Formation_Layered_XL_01)`, `vceoferfa_tier_0 (Desert_Western_Cliff_Layered_XL_03)`
- `oedland_02_regenbogenhang` – Desert Western: Farbbänder für den bunten Hang (A): `uk4paip_tier_0 (Desert_Western_Formation_Layered_XL_06)`, `vepnfcr_tier_0 (Desert_Western_Formation_Layered_XL_03)`, `venuafk_tier_0 (Desert_Western_Cliff_Layered_XL_11)`
- `oedland_03_hoellentor` – Lava & Volcano: Glut-Decals mit Emission, Hitzeflimmern (A): `MI_NM_Decal_Lava_NoAlbedo_03`, `FX_Distortion_Big`, `FX_Lava_Smoke_1`
- `oedland_03_hoellentor` – Ultimate Niagara (B): Flame Dust/Smoke Spark: `FX_Lava_Particle_02`, `FX_Lava_Smoke_03`
- `oedland_06_schlammvulkaene` – Lava & Volcano: Blasen/Spritzer + Schlamm (A): `FX_Lava_Bubble`, `ulnfeaq_tier_0 (Desert_Western_Mound_Mud_Rough_01)`, `vepoadh_tier_0 (Desert_Western_Slope_Mud_Erosion_01)`
- `oedland_07_totenpfanne` – Coast & Dunes: Ton-/Riss-Decals (B): `MI_Decal_Clay_01`, `MI_Decal_Clay_02`, `MI_Decal_Clay_03`
- `oedland_08_erdroehren` – Lava & Volcano (C): Bodensets Ton, Kies: `vepoadh_tier_0 (Desert_Western_Slope_Mud_Erosion_01)`, `ulcceh3_tier_0 (Desert_Western_Pile_Rock_Rough_01)`, `MI_Decal_Clay_03`

**Ersatz → echtes Asset:**

- `oedland_01_rippenland, oedland_02_regenbogenhang`: statt ukjhcamga_tier_0 ×4 Tönungen, SM_HugeSandstoneCliff_05/07 → `uk5oded_tier_0 (Desert_Western_Cliff_Layered_XL_02)`, `uk4paip_tier_0 (Desert_Western_Formation_Layered_XL_06)`, `veonegs_tier_0 (Desert_Western_Formation_Layered_XL_01)` – Desert Western hat die Bänder in der Textur (Nanite, Fab-Material) – kein Material-Fix.
- `oedland_03_hoellentor`: statt M_Eldarien_Glut auf SM_Rock_* + Punktlicht → `MI_NM_Decal_Lava_NoAlbedo_03`, `FX_Distortion_Big` – M_Eldarien_Glut auf Splittern darf bleiben; Decal + Flimmern ergänzen.
- `oedland_06_schlammvulkaene`: statt NS_Bubble_Burst + Bodenlage Schlamm → `FX_Lava_Bubble`, `ulnfeaq_tier_0 (Desert_Western_Mound_Mud_Rough_01)`
- `oedland_07_totenpfanne`: statt Bodenlage Lehm + MI_TileableLeakage hell → `MI_Decal_Clay_01`, `MI_Decal_Clay_02`

**Fehlt weiter:**

- Brausen/Fauchen des Gaskraters (oedland_03_hoellentor) – Fantasy Ambiences (B) · *nur nach Ferats OK*
- Hall/Tropfen in den Röhren (oedland_08_erdroehren) – Cave Ambience (B) · *nur nach Ferats OK*
- Runde Konkretionen (oedland_05_kugelsteine) – Wadi Rum Sandstone Rock 01–04 (C) · *nur nach Ferats OK*
