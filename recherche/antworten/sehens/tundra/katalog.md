# Tundra – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1, Biom-Agent B5)

Stand 11.10.2026 · Daten: `vorlagen/daten/sehens` (2 m) · Werkzeuge: `antworten/skripte/sehens_lib` (Cache, `sicht.py`, `kandidaten.py`)
· Dateien: `standorte.json` (8 Orte + 4 Pfade im 13c-Schema, Prüfer **0 FEHLER** für tundra; einzige Warnung: Pfad 05 streift den Rand von Kharad-Vor), `asset_bedarf.json`, `<id>.png` je Ort (Draufsicht 2 m mit
geplantem Geländestempel, Elementen, Zugang, Kameras). Inventar: Stand 13b (1 692 Netze, Megascans Eis/Schnee vorhanden).

## Das Biom in Zahlen – und was daraus folgt

Tundra = 1,71 km² (Felder C2–E3), vorherrschend Heide 34 %, Wiese 20 %, Trockengras 19 %, Schnee 8 %, Kies 6 %; nur 2 % Baumzellen;
Höhe −6…335 m (Hang-Median 17°). Kernraum ist die Küstenebene zwischen Kharad-Vor und dem Frostrand (X −2 100…−100, Y −2 450…−1 550)
mit einem verflochtenen Gletscherfluss (Zopfstrom, X −1 800), runden Hügeln und ovalen, abflusslosen Pfannen im Südwesten, einer
Bergschulter im Norden (bis 222 m) und einer Schluchtrinne (Bach von 112 auf 42 m).

| Kennzahl | Wert |
|---|---|
| Fläche ≤ 80 m / ≤ 300 m / ≤ 400 m vom Weg | 0,48 / 1,18 / 1,41 km² |
| zulässige Zone (80–300 m, ≥ 150 m Stadtrand, nicht in Orten, ≥ 30 m innen) | 0,33 km² |
| größter Abstand zum Weg | 892 m |
| max. Orte bei 350 m (3 000 Greedy-Packungen) | 11 – ohne die Sandstein-Landzunge südlich der Bucht (Y > −1 560) und die Schneefelder am Frostrand nur **9** |
| Städte/Orte im Biom | Kharad-Vor (Festung), Erlenbach, Altes Nordtor, Aufstiegsweg, Haus mit offenen Türen |

**Folge:** 8 Orte passen, aber eng. Natürliche Verdeckung vom Weg gibt es fast nur auf der Nordschulter (Rückseite des Hügels) und in der
Schluchtrinne; die Küstenebene liegt offen unter dem 15–20 m höheren Küstenweg. Ich habe deshalb **4 Leuchtfeuer + 4 Fundstücke**
gewählt (Richtwert 3/5) – jede Form dort, wo das Gelände sie hergibt. Vier Orte brauchen einen Pfad (stehen als `pfade` in
`standorte.json`, Ferats Linie „lieber ein Pfad mehr“).

**Abgrenzung (gelesen: gletscher, frost, fjord `standorte*.json`; deren `katalog.md` gab es noch nicht):** Alles hier ist
**Permafrost/Periglazial** – Bodeneis, Frostmusterung, Fließerde, Torf. Keine Gletscherform (Tor, Schliff, Toteisloch, Moräne, Nunatak →
gletscher), kein gefrorenes Wasserfall-/Seeeis (Eisfall, Eisvorhang, Frostsee, Frostblumen → frost), keine Fjordküste/Strandterrassen
(fjord_08 „Die alten Ufer“). Bewusst gestrichen aus Katalog v1: **Warme Quelle** (Dopplung mit gletscher-Geysir), **Die Erstarrten**
(Granitpfeiler = Heide-Tor), **Os**. Grenzfälle mit Begründung: tundra_05 (Thermokarstsee) ≠ gletscher_04 Toteisloch (dort Gletscher-Toteis,
hier tauender Boden mit Palsen und kippenden Bäumen); tundra_06 Aufeis ≠ frost_01/03 (dort gefrorene Fälle/Vorhänge, hier flächiges
Schichteis aus Grundwasser im Talboden) – **Ferat bitte bestätigen**.

**Sichtmessung:** `sicht.py`, Wegpunkte alle 20 m, Gelände + `baumhoehe_4m`, **mit dem geplanten Stempel** (Kopie der Höhe; geplante
Gebüsch-Säume als 4-m-Baumzellen). Leuchtfeuer: Wegpunkte im Ring 300–800 m, die ≥ 30 % der Silhouette sehen. Fundstück: Kern +
4 Proben im Abstand r/3, Ziel 0,6–1,5 m, alle Wegpunkte ≤ 400 m, verdeckt = Anteil ≤ 0,15. Kameras nach §8 (13:00): `_anmarsch`/`_nah`
Hoch −170, echtes Ziel; Kameras im Wasser automatisch ans Ufer verschoben. Zweiter Durchgang **mit allen Pfaden als Wege** (wie der Prüfer): Leuchtfeuer sehen dann mehr Wegpunkte (Pingo 143/189, Wanderer 172/359, Eiswand 113/246, Fließtreppe 74/267); Werte in `standorte.json → sicht.mit_pfaden`.

## Übersicht

| ID | Name | Art | Form | Feld | X / Y (m) | Weg | Sicht/Verdeckung (mit Stempel) | Pfad |
|---|---|---|---|---|---|---|---|---|
| tundra_01_der_pingo | Der Eisbuckel | Leuchtfeuer | Pingo mit Gipfelkrater und Eislinse | C3 | −1736 / −1842 | 153 m | 110 von 129 Wegpunkten, bis 798 m | Trittsteine 63 m |
| tundra_02_der_wanderer | Der Wanderer | Leuchtfeuer | Findling (Erratiker) auf Rundhöcker im Flechtenteppich | D2 | −968 / −2158 | 129 m | 95 von 175, bis 796 m | – |
| tundra_03_die_eiswand | Die Eiswand | Leuchtfeuer | Auftaurutschung mit Grundeis-Kopfwand | E3 | −530 / −1845 | 195 m | 87 von 159, bis 699 m | Trampelpfad 110 m |
| tundra_04_die_fliesstreppe | Die Fließtreppe | Leuchtfeuer | Solifluktionsloben + Schneeflecken | E2 | −450 / −2195 | 145 m | 62 von 100, bis 625 m | – |
| tundra_05_der_trunkene_grund | Der Trunkene Grund | Fundstück | Thermokarstsee, Palsen, kippender Wald | D2 | −1355 / −2450 | 280 m | verdeckt (5/5 Proben, 0 von 15–17; mit Pfad 0 von 78–81) | Serpentine 307 m |
| tundra_06_das_aufeis | Das Aufeis | Fundstück | geschichtetes Aufeis im Schluchtboden | C2 | −1760 / −2235 | 296 m | verdeckt (5/5 Proben, 0 von 22–32; mit Pfad 0 von 82–101) | Serpentine 281 m |
| tundra_07_die_steinringe | Die Steinringe | Fundstück | sortierte Steinringe im Flechtenteppich, Eisschubwall | D3 | −1412 / −1630 | 93 m | teilweise (s. u.) | – |
| tundra_08_das_wabenmoor | Das Wabenmoor | Fundstück | Eiskeil-Polygonmoor an der Flussmündung | D3 | −924 / −1738 | 104 m | Kern 3 von 80 (Anteil 0,25), 2/5 Proben verdeckt | – |

Erzählbogen: Der Boden ist gefroren und arbeitet – er hebt (Pingo, Palsen), sortiert (Steinringe, Polygone), fließt (Fließtreppe), taut und
bricht (Eiswand, Trunkener Grund) und schichtet Eis aus Quellwasser (Aufeis); dazwischen liegt, was das Eis einst brachte (Wanderer).

---

## tundra_01_der_pingo – Der Eisbuckel (Leuchtfeuer)

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

## tundra_02_der_wanderer – Der Wanderer (Leuchtfeuer)

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

## tundra_03_die_eiswand – Die Eiswand (Leuchtfeuer)

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

## tundra_04_die_fliesstreppe – Die Fließtreppe (Leuchtfeuer)

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

## tundra_05_der_trunkene_grund – Der Trunkene Grund (Fundstück)

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

## tundra_06_das_aufeis – Das Aufeis (Fundstück)

**Was man sieht:** Am Grund einer engen Schlucht liegt mitten im Sommer eine 70 m lange, gestufte Eisdecke, 1–2,5 m dick, blau an den
Kanten und weiß oben. Der Bach hat sich eine schmale Rinne hindurchgeschnitten; an der Quelle oberhalb tritt Grundwasser aus und
gefriert Schicht um Schicht. Unterhalb ein Kiesfächer, auf dem das Eis in Schollen zerfällt.
**Vorbild:** Aufeis (Naledi) im Brooks Range und an der Indigirka; Spiel: Eisstufen im Frostgipfel-Tal (DA:I), aber ohne Wasserfall.
**Standort:** C2, X −1760 / Y −2235 m (Ostflanke; Talboden 20 m westlich bei 42–44 m, dort 25 m breit). Schlucht/Kessel, TPI100 −20 m,
Relief 52 m, Geröll 25 %. Weg 296 m (Weg Ost), Stadtrand 359 m.
**Verdeckung:** 5/5 Proben verdeckt, 0 von 22–32 Wegpunkten (Schluchtwände).
**Komposition und Anmarsch:** Zugang 379 m (max. 24,7°) → **Pfad `tundra_pfad_das_aufeis` (Serpentine 281 m bis zur Schluchtkante, dann 92 m Trampelspur mit Kehren hinab)**.
`_anmarsch` an der Schluchtkante: Blick hinunter auf das weiße Band. `_held` vom Westhang talab, `_nah` an der Eisstufe.
**Detail-Ebenen:** Held – Eisdecke aus `vd5leh0ga_tier_0`, `uhpocesfa_tier_0`, `vdsrdd0fa_tier_0` (Ice Cliff, vorhanden) flach gelegt,
Stufenkanten `SM_SmoothRockShelf_01`/`SM_ForestRockSlab_01`/`SM_ForestRockShelf_01` mit `MI_EL_SW_Aufeis`. Begleiter 4–6 – Eisschollen
am Fächer, Schneewächten an der Schattenwand (`xelnbaeqx_tier_0`, `vcyiedgfa_tier_0`, `xfwhcfnqx_tier_0`). Schutt 60–100 – Kies und
Gerölle im Bett (`SM_DryRiverBed_01/02`, `SM_NordicBeachRockyGround_01/02`, `SM_stones_01_2/_5`). Kleinzeug – Eiszapfen
`SM_EISZAPFEN_1/2/5/8` an den Stufen, `SM_SmallStonesPack_05`. Bewuchs nach Ursache – Talboden kahl (Eis, Hochwasser), Hangfuß:
Polarweide `SM_grey_willow_01/04`, Tundragras `SM_wk2oaeyqx_VarB`, Moos an der Quelle. Kontaktzone – Eisrand taut: Nassband, Schlamm.
**Wasser, Effekte, Licht:** `bach` mit `quelle: true` am Kopf, `klar`, schneidet die Eisrinne, mündet in den vorhandenen Bach. Klang
`CUE_Water_Stream_VII_Cue`. Die Schlucht liegt im Schatten, das Eis leuchtet kühl – keine Lichter nötig.
**Geländeänderung:** keine.
**Assets:** Eis/Schnee jetzt vorhanden; Download B „Arctic Cliffs“ nur für größere Platten.
**Aufwand und Risiko:** mittel. Risiko: Dopplung mit frost (Eis) – Unterschied: Schichteis auf Kies, kein Fall, kein See. Ferat entscheidet.
Budget: ~4 000 Instanzen (400 Kollision), 30 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

## tundra_07_die_steinringe – Die Steinringe (Fundstück)

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

## tundra_08_das_wabenmoor – Das Wabenmoor (Fundstück)

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

## Pfade (`standorte.json → pfade`, Schema 13c)

| ID | Art | Länge (gebaut) | Rest als Trampelspur | max. Steigung (ganze Route) | Anschluss | Hinweis |
|---|---|---|---|---|---|---|
| tundra_pfad_der_pingo | Trittsteine | 63 m | 92 m | 24,3° | Weg westlich des Zopfstroms (X −1583 / Y −1859) | Furt 10 m → Trittsteine; am Hügelfuß Kehren |
| tundra_pfad_die_eiswand | Trampelpfad | 110 m | 92 m | 18,3° | Küstenweg Ost (X −697 / Y −1941) | 8 m Bach → Trittsteine |
| tundra_pfad_der_trunkene_grund | Serpentine | 307 m | 185 m | 26,3° | Weg westlich Kharad-Vor (X −1419 / Y −2165, außerhalb des Stadtrands) | streift den Stadtkreis (Prüfer-WARNUNG); Kehren |
| tundra_pfad_das_aufeis | Serpentine | 281 m | 92 m | 24,7° | Weg Ost (X −1547 / Y −1967) | Kehren hinab in die Schlucht |

Pfade zählen beim Prüfer als Wege. Deshalb **endet jeder Pfad vor dem Ort** (92 m bzw. beim Trunkenen Grund 185 m hinter der Kuppe, damit
der See verdeckt bleibt); die Reststrecke ist eine Trampelspur (Bodenlage Erde, kein Weg). Band 1,5 m Erde/Kies; Punktliste = Rohlinie aus
`kandidaten.erreichbarkeit` (4-m-Raster, Wege in Städten ausgeblendet) – Kehren und ≤ 15 % rechnet euer Serpentinen-Werkzeug.

## Offene Fragen an Ferat

1. tundra_06 **Aufeis** (Eis im Talboden) und tundra_05 **Thermokarstsee** neben frost/gletscher – so in Ordnung?
2. tundra_07 **Steinringe**: vom höheren Küstenweg teilweise einsehbar – als Fundstück lassen oder zum Leuchtfeuer machen?
3. Mischung **4 Leuchtfeuer / 4 Fundstücke** statt 3/5 (die offene Küstenebene gibt kaum Verstecke her).
4. Bildwünsche (leer): Pingo-Hügel, Hufeisen-Mulde der Eiswand, Aufeis-Schlucht (Kameras in `asset_bedarf.json`).

## Abgleich Inventar 13d (Stand 11.10.2026, abends)

Neues Inventar: 1 965 Netze, 116 Niagara, 85 Decals. Pfade, Maße und Paketstatus stehen in `asset_bedarf.json` → `abgleich_13d`. Orte und Kameras bleiben unverändert; die Phase-2-Planer werden gerade auf die echten Assets umgestellt.

**Jetzt erfüllt:**

- `tundra_03_die_eiswand` – Coast & Dunes: Nass-/Lehm-Decals für Schlammstrom und Tropfspuren (B): `MI_Decal_Clay_01`, `MI_Decal_Clay_02`, `MI_Deca_Wet`
- `tundra_08_das_wabenmoor` – Coast & Dunes: Nassband-Decals an den Tümpelrändern (B): `MI_Deca_Wet_Flat`
- `tundra_05_der_trunkene_grund, tundra_06_das_aufeis` – Nassband an allen Wasserorten (13d): `MI_Deca_Wet_Flat`

**Ersatz → echtes Asset:**

- `tundra_03, _05, _06, _08`: statt MI_Leakage_01…13 als Nässe/Schlamm → `MI_Deca_Wet`, `MI_Deca_Wet_Flat`, `MI_Decal_Clay_01` – Nassband an der Wasserlinie jetzt mit dem echten Coast-&-Dunes-Decal MI_Deca_Wet (flache Ufer MI_Deca_Wet_Flat) statt MI_Leakage_*/MI_TileableLeakage_*.
- `tundra_01_der_pingo`: statt Schneekappe aus Snow_Embankment_uhuldcyfa/Snow_Pile_xftjadtab → `Snow_Embankment_uhvifcgfa_High` – optional zusätzliche Schneewehe (neu seit 13b).

**Fehlt weiter:**

- Größere Eisplatten (8–10-m-Wand, Aufeis-Schollen) (tundra_03_die_eiswand, tundra_06_das_aufeis) – Arctic Cliffs (B) · *nur nach Ferats OK*
- Rentierflechte (tundra_02_der_wanderer, tundra_07_die_steinringe) – Moss & Lichen Forest Ground Rock Materials (C) · *nur nach Ferats OK*
- Bemooste Islandblöcke (tundra_02_der_wanderer) – Tundra Icelandic Rock Cluster (C) · *kostenlos → Claude lädt auf Wunsch*
- Kiesmatrix (tundra_07_die_steinringe) – Megascans Icelandic Sand With Pebbles (C) · *kostenlos → Claude lädt auf Wunsch*
- Schneefahnen (optional) (tundra_04_die_fliesstreppe) – Niagara VFX Pack — Snow … (C) · *nur nach Ferats OK*
- Wind-Klang (tundra_01_der_pingo) – Fantasy Ambiences (B) · *nur nach Ferats OK*
