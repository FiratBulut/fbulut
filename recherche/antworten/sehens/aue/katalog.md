# Aue – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

Stand 11.10.2026 · Agent B1 · Dateien: `standorte.json` (Prüfer **0 FEHLER, 0 WARNUNG**; Gesamtprüfung aller Biome: 0 FEHLER,
für die Aue nur die Hinweise „_anmarsch x m vom Weg“ – diese Kameras stehen bewusst auf dem Zugangspfad), je Ort `<id>.png`
(Draufsicht 2 m mit geplanten Elementen, Zugang und Kameras), `asset_bedarf.json`. Alle Zahlen aus den 2-m-Daten
(`vorlagen/daten/sehens`) und `antworten/skripte/sehens_lib` (Cache, Sichtlinien Gelände + `baumhoehe_4m`, Wegpunkte im 20-m-Raster).
Kameras nach §8 in der Fassung vom 11.10. 13:00: **alle mit Hoch = −170** (genau Augenhöhe) und echtem Ziel – Leuchtfeuer
`_anmarsch`/`_fern` auf die Silhouettenmitte (Boden + halbe Zielhöhe), Fundstücke auf Boden + 1 m, `_nah` auf Boden + 0,5 m,
`_held` auf das Blickziel der Komposition.

## Das Biom in den Daten

- **6,84 km²**, aber nur **0,99 km²** erlaubte Ortsmitten (80–300 m vom Weg, ≥ 150 m vom Stadtrand, nicht in Orten, ≥ 30 m
  innen). Die Wege laufen am Talrand und über die Brücken; das Tal ist voller geplanter Städte (37 im Weltdatensatz, viele in C4–E5).
  Erlaubte Fläche nach Feldern: E5 25 %, F4 21 %, C5 15 %, C4 12 %, D5 8 %, C3 5 % – die Inseln (A6/A7/B7, J6) und der Rahmen um
  den Sumpf (H5) haben keine Wege in Reichweite und fallen heraus.
- Form: das breite Tal des **Hauptflusses** (F_HAUPTFLUSS_3, 38–222 m breit) von C4 bis zur Mündung in F5, mit einem
  **Seitenarm** (F_ALTARM_FLUSSAUE_D5/E5) um eine Kiesinsel, einem **hufeisenförmigen Altwasser** (E5), dem Bachdelta in C4 (neun
  Bäche B_R2_R_M1_M1_*), einer **9–10 m hohen Geländestufe** südlich des Flussbogens in C5 und dem bewaldeten Hügellappen F4 am
  Elfenfluss. Boden (Stichprobe): Wiese 46 %, Trockengras 16 %, Sand 10 %, Nadeln 5 %, Laub 5 %, Gras 5 %, Geröll 4 %; 6 % Süßwasser.
- Heute (Bilder `UFER2_E5_E5_Flussaue_Altarm`, `UFER2_E5_E5_Altarm_hoch`, `BIOM2_B7`, `BIOM2_F6`, `MITT1_F5`, `HEUTE1_E5_hain0`):
  saubere Kiesufer ohne Treibgut, Trauerweiden in Reihe, Kies-„Pflaster“ ohne Saum, Wiesen ohne Blumeninseln, Gehölze gleichmäßig
  gestreut, nirgends Totholz oder Hochwasserspuren. Der Fluss **wirkt nicht, als hätte er je Hochwasser geführt**. Zielbild
  `witcher_01` (Flussufer mit Steinen, Spiegelung, rote Ähren in Gruppen) und `witcher_06` (Bach mit Schaum, Blöcken, Saum).
- **Leitidee:** Jeder Ort erzählt eine Kraft des Flusses – **er nagt** (Schwalbenwand), **er baut** (Treibholzwerder),
  **er verlässt sein Bett** (Mondarm, Lilienrinne), **er speist** (Blautopf), **er düngt und überflutet** (Lianenhalle, Die Alte),
  und **wer ihn staut** (Biberstau). Das unterscheidet die Aue von allen anderen Biomen.
- Ortsfindung (Skripte im Scratchpad `a13/b1_aue/`: `signale.py`, `typen.py`, `feinsuche.py`, `robust.py`, `schirm.py`, `bau_aue.py`):
  eigene Raster Abstand zum Fluss/Altarm (Flusspolylinien gerastert), Baumdichte 40 m, Relief 30 m; Scores je Ortstyp –
  Quelltopf (Bachanfang ≤ 25 m, profilkonkav, TPI50 < 0, steiler Rahmen), Prallhang (Relief 30 m ≥ 4 m, Hang ≥ 25° am Fluss),
  Kiesbank (Kies/Sand/Geröll ≥ 20 %, 10–25 m vom Fluss), Altarm (≤ 25 m vom Seitenarm), Solitär (TPI100 > 0, offen, Wiese),
  Auwald (Baumdichte ≥ 10 %, flach, 30–80 m vom Wasser), Flutrinne (TPI25 < 0, flach, ≤ 400 m vom Fluss). Danach
  Feinsuche je Ort (8-m-Gitter) und für Fundstücke eine **Robustheitsprobe**: Verdeckung an 3 × 3 Punkten im Abstand 8 m.
- Abstände: kleinster Abstand zwischen zwei Aue-Orten 365 m (Blautopf – Lianenhalle), zu anderen Biomen 467 m
  (Biberstau – `bergwald_02_die_brandkiefer`; Stand 29 Orte anderer Biome). Verteilung: West (C4/C5) 3, Mitte (D5/E5) 3, Ost (F4) 2.

## Übersicht

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden z | Radius | Weg | Nachweis (sicht.py) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `aue_01_biberstau` | Biberstau | Fundstück | C4 | −2530 / −840 | 34,3 m | 45 m | 144 m | verdeckt: max. Anteil 0,00 an 77 Wegpunkten ≤ 400 m; 3×3-Probe 9/9 |
| 2 | `aue_02_die_alte` | Die Alte | Leuchtfeuer | C4 | −2282 / −552 | 24,2 m | 40 m | 270 m | 30 m: 83 / 328 Wegpunkte (300–800 m) ≥ 30 %, bis 798 m; bester 499 m, Anteil 0,98 |
| 3 | `aue_03_schwalbenwand` | Schwalbenwand | Leuchtfeuer | C5 | −2160 / 82 | 13,8 m | 80 m | 267 m | 12 m: 70 / 333 Wegpunkte, bis 795 m; aus Süden (Wandseite) 33 / 54 |
| 4 | `aue_04_treibholzwerder` | Treibholzwerder | Leuchtfeuer | D5 | −730 / 494 | 19,7 m | 60 m | 273 m | 12 m: 57 / 343 Wegpunkte, bis 792 m; bester 499 m, Anteil 1,0 |
| 5 | `aue_05_lilienrinne` | Lilienrinne | Fundstück | E5 | −420 / 214 | 12,9 m | 70 m | 148 m | verdeckt: 0,00 an 72 Wegpunkten ≤ 400 m; 3×3 9/9 |
| 6 | `aue_06_mondarm` | Mondarm | Fundstück | E5 | −240 / 740 | 19,2 m | 90 m | 84 m | verdeckt: 0,00 an 48 Wegpunkten; 3×3 heute 3/9, mit geplantem Weidengürtel 9/9 |
| 7 | `aue_07_blautopf` | Blautopf | Fundstück | F4 | 1166 / −834 | 27,1 m | 40 m | 87 m | verdeckt: 0,00 an 77 Wegpunkten; 3×3 9/9 |
| 8 | `aue_08_lianenhalle` | Lianenhalle | Fundstück | F4 | 1196 / −470 | 16,9 m | 60 m | 210 m | verdeckt: 0,00 an 58 Wegpunkten; 3×3 8/9 |

Gegenüber Katalog v1 übernommen: **Blautopf**, **Die Alte**, **Schwalbenwand** (jetzt mit echter Geländestufe). Ersetzt:
„Hexenring“ und „Mohnsenke“ (Wiesenmotive ohne Flussbezug; Mohn ist ein Ackerbegleiter) durch **Lilienrinne** (Flutrinne);
„Erdfall-Weiher“ (Karsttrichter – geologisch eher Heide/Karst, und es gibt schon Moorauge/Blaues Auge) durch **Mondarm**
(echtes Altwasser in den Daten); „Der Gespaltene“ (Findling – Gletscher/Tundra-Motiv) durch **Treibholzwerder**; neu sind
**Biberstau** und **Lianenhalle** (Hartholzaue). „Sieben Brüder“ (Drumlins) entfällt – glazial, nicht fluvial.

**Einmaligkeit (geprüft gegen Katalog v1 aller Biome und alle vorhandenen `standorte.json`/`katalog.md`):** Blautopf ≠ Elfentreppe
(Sinterterrassen) ≠ Silberhain (Birkenquelle) ≠ Turmquelle/Blaues Auge (Dschungel-Karst) – hier ein **einzelner, tiefblauer
Karst-Quelltopf am Talschluss**, ohne Sinter, ohne Birkenring. Mondarm ≠ Tellerweiher (Riesenseerosen) ≠ Geisterwald (tote
Stämme im schwarzen Wasser) – hier ein **Hufeisen-Altwasser mit normalen Teich-/Seerosen, Röhricht und lebenden Weiden**.
Biberstau ≠ Geisterwald: der Held ist der **Damm** (Bauwerk eines Tiers, keine Menschenspur); nur 3 ertrunkene Fichten.
Die Alte ≠ Mutterbaum (Buche im Wald) ≠ Brandkiefer (tot, verkohlt) – hier eine **lebende Solitär-Stieleiche auf offener Wiese**.
Lianenhalle ≠ Säulenhain (Riesentannen) ≠ Weidendom (Weidenring im Wasser) ≠ `elfenwald_06_blauer_grund` (blauer Blütenteppich
mit Lichtschacht unter Buchen) – hier sind **Lianenvorhänge und Hochwassermarken** der Held, Pappeln/Hainbuchen statt Buchen,
der Blütenteppich ist nur weißer Saum. Schwalbenwand ≠ Bemalte Hügel/Canyonwände – **Lehm-/Sandabbruch** mit Brutröhren. Treibholzwerder ≠
Diamantstrand (Eisblöcke) ≠ Windwurf (Sturm) – hier vom **Hochwasser** aufgetürmtes Holz. Lilienrinne ≠ Ginstergold/Wollgrasmeer –
eine **Flutrinne** mit Feuchtstauden.

---

## 1 · Biberstau (`aue_01_biberstau`) – Fundstück

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

## 2 · Die Alte (`aue_02_die_alte`) – Leuchtfeuer

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

## 3 · Schwalbenwand (`aue_03_schwalbenwand`) – Leuchtfeuer

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

## 4 · Treibholzwerder (`aue_04_treibholzwerder`) – Leuchtfeuer

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

## 5 · Lilienrinne (`aue_05_lilienrinne`) – Fundstück

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

## 6 · Mondarm (`aue_06_mondarm`) – Fundstück

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

## 7 · Blautopf (`aue_07_blautopf`) – Fundstück

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

## 8 · Lianenhalle (`aue_08_lianenhalle`) – Fundstück

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

## Budgets (Richtwerte je Ort, Phase 2 verbindlich)

| Ort | Instanzen | Kollision | Akteure | Lichter | Niagara | Nebel | Decals | Fenster |
|---|---|---|---|---|---|---|---|---|
| 01 Biberstau | 3 500 | 400 | 60 | 0 | 0 | 1 | 6 | 90 × 70 m |
| 02 Die Alte | 4 000 | 200 | 25 | 0 | 1 (opt.) | 0 | 4 | 60 × 60 m |
| 03 Schwalbenwand | 5 000 | 600 | 50 | 0 | 0 | 0 | 10 | 200 × 90 m |
| 04 Treibholzwerder | 6 000 | 1 200 | 70 | 0 | 1 (opt.) | 0 | 8 | 140 × 60 m |
| 05 Lilienrinne | 9 000 | 100 | 10 | 0 | 1 (opt.) | 1 | 6 | 220 × 120 m |
| 06 Mondarm | 7 000 | 300 | 30 | 0 | 1 (opt.) | 1 | 6 | 120 × 80 m |
| 07 Blautopf | 3 000 | 400 | 35 | 0 | 1 (opt.) | 1 | 4 | 80 × 80 m |
| 08 Lianenhalle | 8 000 | 300 | 40 | 1 | 1 (opt.) | 1 | 10 | 100 × 100 m |

Feld C4 bekommt zwei Orte (01, 02: zusammen ~7 500 Instanzen), E5 zwei (05, 06: ~16 000), F4 zwei (07, 08: ~11 000) – alle weit
unter 60 000 je Feld.

**Materialwünsche (5 von 6):** `MI_EL_SW_Lehmwand` (`M_EL_Fels_Sand`: `Toenung` [0,80, 0,64, 0,47, 1], `Sand_Farbe`
[0,86, 0,74, 0,56, 1], `Sand_Menge` 0,8 – Schwalbenwand); `MI_EL_SW_Kalk_Moos` (`M_EL_Klippe_RVT`: `Toenung` [0,96, 0,94, 0,87, 1],
`Moos_Menge_Akteur` 0,9 – Blautopf); `MI_EL_SW_Ufer_Nass` (`M_EL_Fels_MS`: `Nass_Dunkel` 0,75 – Ufersteine, Trittsteine);
`MI_EL_SW_Weiderich` (`M_EL_Pflanze`: `Farbe` [0,95, 0,45, 0,85, 1] – Lilienrinne); `MI_EL_SW_Treibholz` (`M_EL_Fels_MS`:
`Toenung` [1,3, 1,25, 1,18, 1], `Helligkeit` 1,25 – nur falls die Megascans-Überschreibung Holz über `M_EL_Fels_MS` führt).
Neue Textur (eigener Punkt): Brutröhren-Maske für ein Decal aus `M_MS_Decal` (512 px, Claude erzeugt sie).

## Pakete (Zusammenfassung, Details in `asset_bedarf.json`)

- **A:** Free City & Nature Sounds (alle 8 Orte), Coast & Dunes (Decals; Schwalbenwand, Werder), Megascans Rembrandt Water Lily
  (Mondarm), **neu: „Nanite Driftwood Props“** (Treibholzwerder; https://www.fab.com/listings/0e9cba47-33ee-4a64-a1e1-88611efbee3b,
  Preis ungeprüft – „prüfen: evtl. schon in Bibliothek“).
- **B:** Megascans Limestone Rocks (Blautopf), **neu: „Megascans Trees: European Black Alder“** (kostenlos laut UE-Marketplace;
  Mondarm-Gürtel, Biberstau, Lilienrinne), **neu: Stieleiche „Quercus Robur – Nanite & Impostor“**
  (https://www.fab.com/listings/453443d0-2015-4d94-9997-81de633b1941, Preis ungeprüft; Die Alte).
- **C:** Forest Fungi, Free Niagara Particles, Niagara Examples, Niagara VFX (Laub), Nature Water FX (kostenpflichtig), neu: tote
  Stieleiche (https://www.fab.com/listings/de7a1a4a-8a51-48cd-b57e-abcb12aafdb2).
- Aus der Vorfassung entfallen für die Aue: „Hexenring“ (Forest Fungi nur noch C), „Erdfall-Weiher“ (→ Mondarm/Blautopf).

## Offene Fragen an Ferat

1. **Die Alte:** Soll ich auf das Stieleichen-Paket warten (B, Preis ungeprüft), oder ist eine Schwarzpappel (`SM_Poplar_tree_06_Optimised`
   ×1,3, sofort) als Solitär genauso recht?
2. **Weiden:** Im Bestand gibt es nur zwei Trauerweiden (`Big_Tree_Willow_01/02`). Hast du das Megascans-Erlenpaket schon (es ist das
   Schwesterpaket der vorhandenen Hainbuchen)? Sonst bitte laden (kostenlos).
3. **Mondarm:** Der Ort ist nur mit einem neuen Weiden-/Erlengürtel zwischen Weg und Ufer ein echtes Fundstück (3/9 → 9/9). Einverstanden,
   dass dort 220 m Ufergehölz gepflanzt werden?
4. **Schwalbenwand:** Darf ich eine kleine eigene Decal-Maske (Brutröhren) erzeugen, oder lieber ohne Löcher?
5. **Bildwünsche** (leere Standorte, Kameras in `asset_bedarf.json`): Die Alte `_fern`, Schwalbenwand `_held`, Treibholzwerder `_fern`,
   Mondarm `_held`, Blautopf `_held` – vor allem Uferhöhen und Wandhöhe vor dem Bau.

<!-- abgleich-13b13c -->

## Abgleich mit Inventar 13b und Entscheidungen 13c (Stand 11.10.2026)

Neues Inventar: `netze.csv` mit 1 692 Netzen, `inventar_extra.json` mit 73 Niagara-Systemen, 15 Effekt-Blueprints und 46 Klang-Cues. Maschinenlesbar steht alles in `asset_bedarf.json` → `abgleich_13b_13c`. Der Abschnitt ergänzt die Ortsbeschreibungen oben; wo er abweicht, gilt er.

### Entscheidungen aus 13c

- **Die Alte mit Bestand** (aue_02_die_alte): Held jetzt `SM_Poplar_tree_06_Optimised` ×1,3 (≈ 34,5 m) als Schwarzpappel. `SM_dry_oak_0*` (Coast & Dunes) sind im Inventar, aber nur 3,9–9,0 m hoch und windgeformt; für den Held bräuchten sie ×3 und mehr (Texel-Dichte, keine Nanite-Netze). Sie bleiben Begleiter/Jungeichen. Stieleichen-Paket steht in der Download-Liste unter B; Austausch später ohne neue Standortsuche.
- **Erlen-Ersatz** (aue_01_biberstau, aue_04_treibholzwerder, aue_06_mondarm): Megascans-Erlen sind nicht im Bestand. Ersatz: Pappeln `SM_Poplar_tree_02/03_Optimised/04_Optimised`, Birke `Big_Tree_Birch_01`, Weiden `Big_Tree_Willow_01/02` und Strauchweiden `SM_grey_willow_01–04`. Erlen bleiben ein optionaler Wunsch (C).
- **Mondarm-Ufergehölz** (aue_06_mondarm): Ja: 220 m neuer Gehölzgürtel am Südufer. Er besteht aus `Big_Tree_Willow_01/02`, `SM_Poplar_tree_03_Optimised`, `Big_Tree_Birch_01` und dem Strauchsaum `SM_grey_willow_01–04`. Er verdeckt den Spiegel vom Weg aus und macht den Ort zum echten Fundstück.
- **Seerosen im Bestand** (aue_06_mondarm): `Rembrandt_Water_Lily_uc2kajgia_*_VarA–G_LOD0` (7 Varianten, 1,2–1,7 m Blattgruppen) ersetzen `SM_WaterPlant01–04` als Held des Seerosenfelds.
- **Decal Brutröhren** (aue_03_schwalbenwand): Ja: eigene Textur `sehens/aue/decal_brutroehren.png` + `_n.png` (Beschreibung unten). Das Decal-Material legt Ferat an.

### Neu im Bestand – je Ort

| Ort | Asset | Pfad | Maße (m) | Einsatz |
|---|---|---|---|---|
| aue_01_biberstau | `SM_Poplar_tree_02` (kein Nanite) | `/Game/Meadow_Environment_Set/Environment/Foliage/Meshes/SM_Poplar_tree_02` | 6,59 × 7,13 × 13,2 | Erlen-Ersatz am Teichrand (13,2 m, 2–3×) |
| aue_01_biberstau | `Big_Tree_Birch_01` (kein Nanite) | `/Game/Nature_Set/Meshes/Big_Tree_birch_01` | 8,08 × 7,88 × 11,51 | Erlen-Ersatz, 1× |
| aue_01_biberstau | `CUE_Water_Stream_I_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_I_Cue` | – | Plätschern am Überlauf, leise |
| aue_02_die_alte | `SM_Poplar_tree_06_Optimised` (kein Nanite) | `/Game/Meadow_Environment_Set/Environment/Foliage/Meshes/SM_Poplar_tree_06_optimised` | 13,85 × 15,52 × 26,56 | Held ×1,3 (Schwarzpappel, 13c) |
| aue_02_die_alte | `SM_dry_oak_01_D` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Foliage/Meshes/SM_dry_oak_01_D` | 5,3 × 3,97 × 8,99 | Jungeiche/Begleiter (9 m) |
| aue_02_die_alte | `SM_dry_oak_02_A` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Foliage/Meshes/SM_dry_oak_02_A` | 3,56 × 2,67 × 7,6 | Jungeiche/Begleiter (7,6 m) |
| aue_02_die_alte | `NS_Sparkling_Noise` (Niagara) | `/Game/FreeParticle_SoftTofu/Niagara/NS_Sparkling_Noise` | – | Pollen im Gegenlicht – Kopie, warmweiß, sehr klein (optional) |
| aue_02_die_alte | `CUE_Wind_Autumn_wind_with_leaves_rustling_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Wind_Autumn_wind_with_leaves_rustling_Cue` | – | Wind in der Krone |
| aue_03_schwalbenwand | `SM_LS_beach_cliff_02_A` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Cliffs/Landscape_Spline_Meshes/SM_LS_beach_cliff_02_A` | 16,42 × 6,17 × 6,59 | Lehmwand-Segment 16,4 × 6,6 m (neu aus Coast & Dunes), mit MI_EL_SW_Lehmwand |
| aue_03_schwalbenwand | `SM_LS_beach_cliff_02_B` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Cliffs/Landscape_Spline_Meshes/SM_LS_beach_cliff_02_B` | 23,04 × 8,31 × 6,62 | Lehmwand-Segment 23,0 × 6,6 m |
| aue_03_schwalbenwand | `SM_LS_beach_cliff_02_C` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Cliffs/Landscape_Spline_Meshes/SM_LS_beach_cliff_02_C` | 15,63 × 6,19 × 6,82 | Lehmwand-Segment 15,6 × 6,8 m |
| aue_03_schwalbenwand | `SM_LS_beach_escarpment_02_B` (kein Nanite) | `/Game/Coast_Dunes_Environment_Set/Cliffs/Landscape_Spline_Meshes/SM_LS_beach_escarpment_02_B` | 11,16 × 2,71 × 1,83 | Abbruchkante oben (11,2 m) |
| aue_03_schwalbenwand | `NS_feather` (Niagara) | `/Game/FreeParticle_SoftTofu/Niagara/NS_feather` | – | einzelne Federn am Wandfuß (optional, sehr spärlich) |
| aue_03_schwalbenwand | `CUE_Wind_Autumn_wind_with_leaves_rustling_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Wind_Autumn_wind_with_leaves_rustling_Cue` | – | Wind über der Kante (Vogelstimmen fehlen) |
| aue_04_treibholzwerder | `SM_Poplar_plant_A_00` (kein Nanite) | `/Game/Meadow_Environment_Set/Environment/Foliage/Meshes/SM_Poplar_plant_A_00` | 2,16 × 1,76 × 3,18 | Weichholz-Jungwuchs (Erlen-Ersatz) |
| aue_04_treibholzwerder | `SM_Poplar_plant_C_00` (kein Nanite) | `/Game/Meadow_Environment_Set/Environment/Foliage/Meshes/SM_Poplar_plant_C_00` | 3,24 × 3,1 × 4,18 | Weichholz-Jungwuchs |
| aue_04_treibholzwerder | `CUE_Water_Stream_VI_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_VI_Cue` | – | Rauschen an der Verklausung |
| aue_05_lilienrinne | `BP_FogBankVolume` (Blueprint) | `/Game/NiagaraExamples/FX_Fog/BP_FogBankVolume` | – | Bodendunst über dem Tümpel (Blueprint aus NiagaraExamples/FX_Fog, kein Niagara-System; optional) |
| aue_06_mondarm | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarA_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarA_LOD0` | 1,19 × 1,26 × 0,29 | Seerosenfeld (Held) |
| aue_06_mondarm | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarB_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarB_LOD0` | 1,28 × 1,34 × 0,01 | flaches Blatt |
| aue_06_mondarm | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarC_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarC_LOD0` | 1,39 × 1,32 × 0,72 | mit Blüte |
| aue_06_mondarm | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarD_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarD_LOD0` | 1,28 × 1,59 × 0,44 | Seerose |
| aue_06_mondarm | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarE_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarE_LOD0` | 1,7 × 1,33 × 0,45 | Seerose |
| aue_06_mondarm | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarF_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarF_LOD0` | 1,48 × 1,48 × 0,85 | Seerose, dicht |
| aue_06_mondarm | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarG_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarG_LOD0` | 1,26 × 1,11 × 0,68 | Seerose |
| aue_06_mondarm | `Big_Tree_Willow_02` (kein Nanite) | `/Game/Nature_Set/Meshes/Big_Tree_willow_02` | 21,4 × 21,12 × 21,25 | Ufergehölz-Gürtel 220 m (13c) |
| aue_06_mondarm | `SM_Poplar_tree_03_Optimised` (kein Nanite) | `/Game/Meadow_Environment_Set/Environment/Foliage/Meshes/SM_Poplar_tree_03_Optimised` | 11,04 × 12,04 × 18,34 | Ufergehölz-Gürtel |
| aue_06_mondarm | `Big_Tree_Birch_01` (kein Nanite) | `/Game/Nature_Set/Meshes/Big_Tree_birch_01` | 8,08 × 7,88 × 11,51 | Ufergehölz-Gürtel, Erlen-Ersatz |
| aue_06_mondarm | `BP_FogBankVolume` (Blueprint) | `/Game/NiagaraExamples/FX_Fog/BP_FogBankVolume` | – | Dunst über dem Spiegel (Blueprint, optional) |
| aue_07_blautopf | `Limestone_Rocks_ubqwdheda_High` | `/Game/Fab/Megascans/3D/Limestone_Rocks_ubqwdheda/StaticMeshes/Limestone_Rocks_ubqwdheda_High` | 0,6 × 0,65 × 0,09 | Kalkschutt am Ufer (nur 0,6 m – Kleinzeug, keine Wand) |
| aue_07_blautopf | `SM_Fish_Trout` (kein Nanite) | `/Game/Mountain_Environment_Set/Details/Meshes/SM_Fish_Trout` | 0,06 × 0,38 × 0,13 | 2–4 Forellen im klaren Wasser (optional, statisch) |
| aue_07_blautopf | `CUE_Water_Stream_III_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_III_Cue` | – | Quellrauschen |
| aue_08_lianenhalle | `NS_leaf` (Niagara) | `/Game/FreeParticle_SoftTofu/Niagara/NS_leaf` | – | fallende Blätter im Lichtschacht (optional) |
| aue_08_lianenhalle | `CUE_Wind_Autumn_wind_with_leaves_rustling_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Wind_Autumn_wind_with_leaves_rustling_Cue` | – | Wind im Kronendach |

### Paketstatus der Wünsche dieses Bioms

| Paket | Status | Orte |
|---|---|---|
| Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen) | läuft bei Ferat | 03, 04 |
| Forest Fungi – Mushroom Pack | fehlt (Download-Liste) | 02, 08 |
| Free City & Nature Sounds | im Projekt (/Game/City_Nature_Sounds, nur Naturklänge nutzen) | 01, 02, 03, 04, 05, 06, 07, 08 |
| Free Niagara Particles | im Projekt (/Game/FreeParticle_SoftTofu, CC BY 4.0 → Credits SoftTofuVFX) | 02 |
| Imposing Dead Quercus Robur (tote Stieleiche) – Nanite & Impostor | fehlt (Download-Liste) | 08 |
| Megascans Limestone Rocks | im Projekt nur 0,6-m-Haufen; weitere Megascans-Limestone-Assets + Ancraite „Limestone Rock Set“ werden geladen | 07 |
| Megascans Rembrandt Water Lily | im Projekt (7 Varianten) | 06 |
| Megascans Trees: European Black Alder | nicht im Bestand – optionaler Wunsch (C); Ersatz Weiden/Pappeln/Birken | 01, 04, 06 |
| Nanite Driftwood Props | fehlt (Download-Liste) | 04, 05 |
| Nature Water FX (Fontänen, Geysire, Bäche, Wasserfälle) | fehlt (Download-Liste) | 07 |
| Niagara Examples Pack | im Projekt (/Game/NiagaraExamples) | 05, 06 |
| Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam | fehlt (Download-Liste) | 08 |
| Quercus Robur (Stieleiche) – Nanite & Impostor | fehlt (Download-Liste) | 02, 08 |

### Material-Instanzen (6 von höchstens 6)

| Name | Basis | Parameter | für |
|---|---|---|---|
| `MI_EL_SW_Lehmwand` | `M_EL_Fels_Sand` | `Toenung` [0,8, 0,64, 0,47, 1], `Sand_Farbe` [0,86, 0,74, 0,56, 1], `Sand_Menge` 0,8, `Sand_Fuss_Weich` 120 | `SM_beach_cliff_02_A`, `SM_beach_cliff_02_B`, `SM_beach_cliff_02_C`, `SM_sandy_slope_01`, `SM_scarp_01`, `SM_LS_beach_cliff_02_A`, `SM_LS_beach_cliff_02_B`, `SM_LS_beach_cliff_02_C` |
| `MI_EL_SW_Kalk_Moos` | `M_EL_Klippe_RVT` | `Toenung` [0,96, 0,94, 0,87, 1], `Moos_Menge_Akteur` 0,9, `Moos_Farbe` [0,7, 0,88, 0,5, 1] | `SM_big_rock_wall_01`, `SM_big_rock_wall_02`, `SM_big_rock_wall_03`, `SM_HugeMossyForestCliff_01` |
| `MI_EL_SW_Ufer_Nass` | `M_EL_Fels_MS` | `Nass_Dunkel` 0,75, `Nass_Weich` 25 | SM_SmallStonesPack_*, `SM_flat_rock_02`, `SM_NordicBeachRock_01`, `SM_MossyForestRock_02` |
| `MI_EL_SW_Weiderich` | `M_EL_Pflanze` | `Farbe` [0,95, 0,45, 0,85, 1], `Variation` 0,4 | `SM_flower_brownray_knapweed_01`, `SM_flower_brownray_knapweed_02` |
| `MI_EL_SW_Treibholz` | `M_EL_Fels_MS` | `Toenung` [1,3, 1,25, 1,18, 1], `Helligkeit` 1,25 | `SM_LargeFallenTree_01`, `SM_LargeFallenTree_02`, `SM_OldFallenTree_02`, `SM_trunk_01` – nur falls die automatische Megascans-Überschreibung auch Holz über M_EL_Fels_MS führt; sonst entfällt er (Driftwood-Paket ist schon hell) |
| `MI_EL_SW_Brutroehren` | `M_MS_Decal` | `Opacity Intensity` 1, `Normal Intensity` 1, `Min Roughness` 0,75, `Brightness` 1 | Decal Brutröhren aue_03_schwalbenwand – Texturen: BaseColorTexture = sehens/aue/decal_brutroehren.png (RGBA, Alpha = Deckkraft), NormalTexture = decal_brutroehren_n.png (DirectX/UE). Material legt Ferat an (13c). |

### Decal-Textur Brutröhren (aue_03_schwalbenwand)

- Dateien: `sehens/aue/decal_brutroehren.png` (RGBA 1024², Farbe + Deckkraft im Alpha) und `decal_brutroehren_n.png` (Normal-Map, DirectX-/UE-Konvention, Grün = −dH/dy). Beide sind prozedural erzeugt und nahtlos in X.
- Inhalt: 52 dunkle, leicht ovale Röhren mit 6–9 cm Breite (Höhe 72–90 % der Breite) in sechs unregelmäßigen, gewellten Reihen. Dazu ausgetretene, hellere Lehmlippen (unten stärker abgenutzt), ein verschmutzter Halo und bei 18 Röhren leichte weiß-graue Kotspuren mit Spritzern nach unten. Außerhalb ist das Decal transparent; die Lehmwand kommt vom Netz.
- Maßstab: **1 Kachel = 200 × 200 cm** (5,12 px/cm). Decal-Größe `groesse_cm` [30, 200, 200] (Tiefe × Breite × Höhe), für längere Wandstücke mehrere Decals nebeneinander (nahtlos in X) oder Kachelung über `Tiling`.
- Projektion: senkrecht auf die Wand (Decal-X = Wandnormale), nur im oberen Wanddrittel unter der Abbruchkante; 6–8 Decals je Wand, Abstände unregelmäßig. Projektionstiefe 30 cm, damit die Unebenheiten der Wand mitgenommen werden, aber der Wandfuß darunter frei bleibt.
- Material: `MI_EL_SW_Brutroehren` auf `M_MS_Decal` (Tabelle oben; Ferat legt es an).
