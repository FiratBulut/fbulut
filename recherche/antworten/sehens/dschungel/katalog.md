# Dschungel und Turmkarst – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

Stand 11.10.2026 · Agent B3 (elfenwald + dschungel) · Dateien: `standorte.json` (Prüfer `sehens_pruefen.py`: **0 FEHLER,
0 WARNUNG** für den Dschungel; Hinweis: Blaues Auge liegt 20 m „innerhalb" – die Grenze ist hier der Kraterrand des
Meer-Schachts, nicht der Biomrand), je Ort `<id>.png` (Draufsicht 2 m), `asset_bedarf.json`. Zahlen aus den 2-m-Daten
(`vorlagen/daten/sehens`) mit `antworten/skripte/sehens_lib`. Kameras nach §8 (Stand 11.10. 13:00): `_anmarsch`, `_nah`,
`_fern` mit **Hoch = −170** und echtem Ziel, `_held` mit +170.

## Das Biom in den Daten

- Rechteck G5–I7 (x 1352 … 4350 m, y 752 … 2674 m), 3,31 km², mit Nordkerbe in H5 (dort Sumpf/Heide nördlich). Flache
  Tieflandebene (Höhe Median 21 m), aus der **Kalktürme** 60–165 m steil aufragen (TPI100 bis +74 m, Hang bis 82°) – im Westen
  (G6/H6) einzeln, im Osten (I6/I7) zu einem Massiv mit geschlossenen Spalten und Kesseln verwachsen. Ein großer Fluss mäandriert
  von H5 nach Süden zum Meer.
- Boden: Laub 51 %, Fels 13 %, Wiese 7 %, Schlamm 7 %, Kraut 6 %, Trockengras 5 %; Hang Median 11°, 90 %-Wert 50°; Bäume nur auf
  15 % der Fläche, dafür bis 61 m hoch (Riesenbäume `SM_Tree_Big_01b`). Wege nur im Nordband und am Ostrand – der ganze Süden
  liegt > 300 m vom Weg und fällt heraus. Erlaubte Ortsmitten: **0,94 km²**.
- Heute (Bilder `BIOM3_G6_rundgang`, `BIOM3_H6_rundgang`, `BIOM2_I5_rundgang`, `MITT1_G5`, `NAH2_H5_sumpf`): Kalktürme aus
  `SM_Cliff_01*` mit Bonsai-Kronen oben, darunter ein gleichförmiger, heller Kronenteppich; am Boden kaum Unterwuchs, kein
  Wasser zwischen den Türmen, keine Lianen. Zielbild: Guilin/Ha-Long-Karst mit Dunst; Witcher-Qualität heißt hier: Fuß der Türme
  mit Schuttkegeln, Feuchte, Lianen, Wasser in Kalkformen, Riesenblätter im Unterholz.
- **Leitidee (Abgrenzung zum Elfenwald):** Der Dschungel ist **Kalk und Wasser**: Türme, Fenster, Karstquelle, Cenote,
  Schwinde, Turmspalte, Steinwald, Sinter – dazu tropische Riesenblätter. Riesenbäume, Pilze, Leuchtpflanzen, Farnschluchten und
  Nebelwald bleiben im Elfenwald.

## Methode

Eigene Scores je Ortstyp (Scratchpad `a13/b3_elfen_dschungel/`: `such_ds.py`, `such_ds2.py`–`such_ds4.py`, `such_abri.py`,
`becken.py`, `kombi.py`, `plan.py`):

| Ortstyp | Score aus den Daten |
|---|---|
| Turm mit Fenster (Leuchtfeuer) | TPI100 20–60 m + Höhe 60–160 m; Sicht mit 25 m Bogenhöhe |
| Karstquelle am Turm (Leuchtfeuer) | Abstand zu Wandzellen (Hang > 60°) 4–16 m, Hang am Punkt ≤ 12–30°, Wandhöhe (Max 60 m − h) 30–90 m; Sicht mit 0,8 × Wandhöhe |
| Steinwald (Leuchtfeuer) | Kuppe/Turmschulter TPI50 5–30 m, Hang ≤ 20–45°; Sicht mit 15 m Nadelhöhe |
| Cenote | Senkentiefe (gefüllte Senken) + Meer-Zellen unter Gelände (Schacht bis Meerniveau) |
| Lagune | geschlossene Becken ≥ 20 m tief an Turmfüßen (`becken.py`: Überlaufhöhe, Boden, Fläche) |
| Schwinde | Bachenden ohne Abfluss (`bach_enden`, `im_wasser` = falsch) an Kalkbank |
| Garten der Riesen | Hang ≤ 3–12°, 15–65 m vom Wasser, Lichtung (Baumdichte < 0,05–0,3), ≥ 30–100 m von Wänden |
| Sinterhalle (Abri) | Wandfuß (Wand 6–14 m entfernt, Wandhöhe > 30 m), Hang ≤ 15–30° |

Kombinationssuche über alle Kandidaten mit ≥ 350 m Abstand und Biomgrenzen-Abzug, Leuchtfeuer nur mit Sichtnachweis,
Fundstücke nur verdeckt. Kleinster Abstand im Dschungel 351 m (Mondtor – Schluckhöhle), zu anderen Biomen > 1 km.

## Abgrenzung (keine Dopplung)

| Dschungel | nicht zu verwechseln mit | Unterschied |
|---|---|---|
| Mondtor (Fenster im Kalkturm) | wüste „Sonnentor", canyon „Naturbrücke"/„Felsfenster" | Loch hoch oben in einem bewaldeten Karstturm, Sandsteinbögen sind frei stehend und rot |
| Turmquelle (Quelle tritt aus der Turmwand) | bergwald „Klemmblock-Klamm" (Wasserfall in Klamm), küste „Seefall" | Karstquelle mitten in einer senkrechten Kalkwand, kein Bach von oben |
| Steinwald (Kalknadeln) | heide „Karrenfeld" (flaches Pflaster), canyon „Hoodoo-Kessel", lava „Dunkle Burgen" | graue Kalknadeln 4–18 m auf einer Turmschulter, Pflanzen in den Gassen |
| Blaues Auge (Cenote) | aue „Erdfall-Weiher" (flacher Trichter in Wiese) | senkrechte Schachtwände, Wasser 6–20 m unter dem Rand, Luftwurzeln |
| Verborgene Lagune (Wasser in der Turmspalte) | fjord, küste | Süßwasser in einem geschlossenen Kalkspalt, Zugang nur durch eine Gasse |
| Schluckhöhle (Bach verschwindet) | heide „Der Rachen" (Bach stürzt in Schacht) | zwei Bäche laufen flach in ein Portal unter einer Kalkbank, kein Fall |
| Garten der Riesen (Riesenblätter) | elfenwald (Riesenpilze, Riesenbaum) | tropische Blattpflanzen 2–4 m, keine Bäume, keine Pilze |
| Sinterhalle (Felsdach mit Sinterfahnen) | elfenwald „Elfentreppe" (Kalktuff im fließenden Bach), lava „Röhrenfenster" | trockene Halle unter Überhang, Tropfvorhang und ein Sinterbecken |

Aus Katalog v1 entfallen: **Tausendfuß** (Riesen-Banyan) – doppelt mit dem Mutterbaum des Elfenwalds (Ferats Vorgabe: Riesenbäume
nur im Elfenwald), außerdem fand sich kein verdeckter Standort; ersetzt durch **Sinterhalle** (Karst, I7). Steinwald wird
Leuchtfeuer (Turmschulter, von der Straße lesbar); Turmquelle und Schluckhöhle rücken in die erste Welle.

## Die 8 Orte

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden | Weg | Radius | Sicht / Verdeckung (sicht.py) | Zugang |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `dschungel_01_mondtor` | Mondtor | Leuchtfeuer | G5 | 1786 / 958 | 101,0 m | 80 m | 55 m | 25 m: **196 / 241** Wegpunkte (300–800 m), Mittel 0,79, bis 800 m; bester 496 m, 1,00 | **Pfad** 274 m (31 m steil) |
| 2 | `dschungel_02_turmquelle` | Turmquelle | Leuchtfeuer | G5 | 2250 / 962 | 34,7 m | 83 m | 50 m | 60 m: 60 / 166, Mittel 0,23, bis 798 m; bester 326 m, 0,90 | Fußweg 83 m, max 6° |
| 3 | `dschungel_03_steinwald` | Steinwald | Leuchtfeuer | H6 | 3330 / 1442 | 132,6 m | 286 m | 50 m | 15 m: 24 / 157, bis 792 m; bester 501 m, 1,00 | **Pfad** 531 m (19 m steil) |
| 4 | `dschungel_04_blaues_auge` | Blaues Auge | Fundstück | H6 | 2436 / 1278 | 16,4 m | 239 m | 50 m | verdeckt: 0 / 48 Wegpunkte ≤ 400 m (4 m) | Fußweg 287 m, max 23° |
| 5 | `dschungel_05_verborgene_lagune` | Verborgene Lagune | Fundstück | G6 | 1897 / 1377 | 23,0 m | 276 m | 50 m | verdeckt: 0 / 41 | **Pfad** 531 m + Gasse (Stempel) |
| 6 | `dschungel_06_schluckhoehle` | Schluckhöhle | Fundstück | G6 | 1468 / 1106 | 17,2 m | 222 m | 45 m | Portal (1476/1099) verdeckt: 0 / 44 | Fußweg 235 m, max 16° |
| 7 | `dschungel_07_garten_der_riesen` | Garten der Riesen | Fundstück | H6 | 2892 / 1264 | 17,4 m | 209 m | 45 m | verdeckt: 0 / 50 (3 m) | **Pfad** 232 m (11 m Bach → Trittsteine) |
| 8 | `dschungel_08_sinterhalle` | Sinterhalle | Fundstück | I7 | 3780 / 2120 | 20,5 m | 128 m | 50 m | verdeckt: 0 / 46 | Fußweg 131 m, max 15° |

---

## 1 · Mondtor (`dschungel_01_mondtor`) – Leuchtfeuer

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

## 2 · Turmquelle (`dschungel_02_turmquelle`) – Leuchtfeuer

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

## 3 · Steinwald (`dschungel_03_steinwald`) – Leuchtfeuer

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

## 4 · Blaues Auge (`dschungel_04_blaues_auge`) – Fundstück

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

## 5 · Verborgene Lagune (`dschungel_05_verborgene_lagune`) – Fundstück

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

## 6 · Schluckhöhle (`dschungel_06_schluckhoehle`) – Fundstück

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

## 7 · Garten der Riesen (`dschungel_07_garten_der_riesen`) – Fundstück

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

## 8 · Sinterhalle (`dschungel_08_sinterhalle`) – Fundstück

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

## Budgets (Richtwerte §9)

| Ort | Instanzen | Kollision | Akteure | Lichter | Niagara | Nebel | Decals | Geländefenster |
|---|---|---|---|---|---|---|---|---|
| 01 Mondtor | 3 000 | 200 | 20 | 0 | 0 | 0 | 2 | 120 × 120 m |
| 02 Turmquelle | 5 000 | 300 | 15 | 0 | 1 (opt.) | 1 | 4 | 140 × 120 m |
| 03 Steinwald | 4 000 | 600 | 70 | 0 | 0 | 0 | 6 | 110 × 110 m |
| 04 Blaues Auge | 3 000 | 200 | 30 | 1 | 0 | 1 | 4 | 120 × 120 m |
| 05 Verborgene Lagune | 4 000 | 300 | 25 | 0 | 0 | 1 | 4 | 150 × 120 m |
| 06 Schluckhöhle | 2 500 | 200 | 12 | 0 | 0 | 1 | 3 | 80 × 60 m |
| 07 Garten der Riesen | 3 000 | 100 | 10 | 0 | 0 | 1 | 2 | 100 × 100 m (Lagen) |
| 08 Sinterhalle | 3 000 | 300 | 25 | 1 | 1 (opt.) | 1 | 12 | 90 × 70 m |

## Offene Fragen an Ferat

1. Blaues Auge: Der Schacht (2392/1286) liegt unter Meerniveau – siehst du dort heute Meerwasser? (Bildwunsch in `asset_bedarf.json`.)
2. Mondtor: Es gibt keinen Kalk-Felsbogen – ist ein aus `SM_Cliff_01b/01c` zusammengesetzter Bogen für dich in Ordnung?
3. Garten der Riesen braucht ein Tropenpflanzen-Paket (Nanite Tropical Plant Pack 2 oder Electric Dreams) – welches hast du schon?
4. Tausendfuß (Banyan) aus Katalog v1 ist gestrichen (Riesenbäume nur im Elfenwald) – einverstanden?

<!-- abgleich-13b13c -->

## Abgleich mit Inventar 13b und Entscheidungen 13c (Stand 11.10.2026)

Neues Inventar: `netze.csv` mit 1 692 Netzen, `inventar_extra.json` mit 73 Niagara-Systemen, 15 Effekt-Blueprints und 46 Klang-Cues. Maschinenlesbar steht alles in `asset_bedarf.json` → `abgleich_13b_13c`. Der Abschnitt ergänzt die Ortsbeschreibungen oben; wo er abweicht, gilt er.

### Entscheidungen aus 13c

- **Nature Water FX gekauft** (dschungel_02_turmquelle): Ferat hat Nature Water FX gekauft; der Import steht aus. Die echten Systemnamen folgen mit dem nächsten Inventar, bis dahin gilt der Ersatz (lokaler_nebel bzw. NS_Smoke_Plume als Gischt-Vorlage). Realistic Waterfall VFX und Waterfall Pro sind damit gestrichen.
- **Mondtor-Bogen aus SM_Cliff_01*** (dschungel_01_mondtor): Ja: Sturz `SM_Cliff_01b`, Pfeiler `SM_Cliff_01c`. Die Fugen werden mit Geröll, Moos und Decal geschlossen, der Sockel per Geländestempel. Das Prüfbild entscheidet. Neu: Kalkschutt `Limestone_Rocks_ubqwdheda_High` (0,6 m) unter dem Tor.
- **Cenote als eigener `see`** (dschungel_04_blaues_auge): Ja: eigener `see` mit **`farbe: tuerkis`**, Spiegel unabhängig vom Meer. Das Meerwasser im Schacht nimmt Ferat als Bildwunsch auf.
- **Tausendfuß gestrichen** (–): Ja (13c): ersetzt durch `dschungel_08_sinterhalle`. Riesenbäume gibt es nur im Elfenwald.
- **Tropenpflanzen im Bestand** (dschungel_04, _05, _07): AsianTemple (`SM_Fern_01a/02a`, `SM_Vines_01a`, `SM_Tree_Big_01a/b`), `SM_Tree_Palm_01`, Palms_Pack, Electric-Dreams-Reste und Megaplants (122 Netze) – mehr ist nicht da. Electric Dreams bleibt in der Download-Liste (B, kostenlos).

### Neu im Bestand – je Ort

| Ort | Asset | Pfad | Maße (m) | Einsatz |
|---|---|---|---|---|
| dschungel_01_mondtor | `Limestone_Rocks_ubqwdheda_High` | `/Game/Fab/Megascans/3D/Limestone_Rocks_ubqwdheda/StaticMeshes/Limestone_Rocks_ubqwdheda_High` | 0,6 × 0,65 × 0,09 | Kalkschutt unter dem Tor (0,6 m, Kleinzeug) |
| dschungel_02_turmquelle | `NS_Smoke_Plume` (Niagara) | `/Game/NiagaraExamples/FX_Smoke/NS_Smoke_Plume` | – | Vorlage für Sprühnebel am Fuß – Kopie, weiß, langsam (optional; sonst lokaler_nebel) |
| dschungel_02_turmquelle | `CUE_Water_Stream_IX_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_IX_Cue` | – | Rauschen des Falls |
| dschungel_03_steinwald | `Limestone_Rocks_ubqwdheda_High` | `/Game/Fab/Megascans/3D/Limestone_Rocks_ubqwdheda/StaticMeshes/Limestone_Rocks_ubqwdheda_High` | 0,6 × 0,65 × 0,09 | Karrenschutt zwischen den Nadeln |
| dschungel_04_blaues_auge | `CUE_Nature_Birds_Singing_and_talking_lovebirds_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Nature_Birds_Singing_and_talking_lovebirds_Cue` | – | Papageien am Schachtrand (leise; passt nur hier) |
| dschungel_05_verborgene_lagune | `Limestone_Rocks_ubqwdheda_High` | `/Game/Fab/Megascans/3D/Limestone_Rocks_ubqwdheda/StaticMeshes/Limestone_Rocks_ubqwdheda_High` | 0,6 × 0,65 × 0,09 | Kalkschutt in der Gasse |
| dschungel_05_verborgene_lagune | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarC_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarC_LOD0` | 1,39 × 1,32 × 0,72 | Seerosen am Rand (optional) |
| dschungel_05_verborgene_lagune | `Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarF_LOD0` | `/Game/Fab/Megascans/Plants/Rembrandt_Water_Lily_uc2kajgia/StaticMeshes/Rembrandt_Water_Lily_uc2kajgia_Raw_uc2kajgia_VarF_LOD0` | 1,48 × 1,48 × 0,85 | Seerosen (optional) |
| dschungel_06_schluckhoehle | `Limestone_Rocks_ubqwdheda_High` | `/Game/Fab/Megascans/3D/Limestone_Rocks_ubqwdheda/StaticMeshes/Limestone_Rocks_ubqwdheda_High` | 0,6 × 0,65 × 0,09 | Kalkbank |
| dschungel_07_garten_der_riesen | `CUE_Nature_Birds_Singing_and_talking_lovebirds_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Nature_Birds_Singing_and_talking_lovebirds_Cue` | – | Vögel im Garten (leise) |

### Paketstatus der Wünsche dieses Bioms

| Paket | Status | Orte |
|---|---|---|
| Cave Ambience | fehlt (Download-Liste) | 06, 08 |
| Cave Stalactites & Wall Kit – Midpoly Nanite-Ready Asset Pack | fehlt (Download-Liste) | 06, 08 |
| Electric Dreams Environment (Dschungel-Pflanzen, Felsen, Soundscape-Klänge) | fehlt (Download-Liste) | 04, 07 |
| Free City & Nature Sounds | im Projekt (/Game/City_Nature_Sounds, nur Naturklänge nutzen) | 02 |
| Megascans Limestone Rocks | im Projekt nur 0,6-m-Haufen; weitere Megascans-Limestone-Assets + Ancraite „Limestone Rock Set“ werden geladen | 01, 03, 05, 06 |
| Megascans Rembrandt Water Lily | im Projekt (7 Varianten) | 05 |
| Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen) | läuft bei Ferat | 02 |
| Nanite Tropical Plant Pack 2 | fehlt (Download-Liste) | 07 |
| Nature Water FX (Fontänen, Geysire, Bäche, Wasserfälle) | gekauft, Import ausstehend – Inventar folgt (Systemnamen danach) | 02 |
| Niagara Examples Pack | im Projekt (/Game/NiagaraExamples) | 02 |
| Procedural Rocks Generator | fehlt (Download-Liste) | 03 |
| Rain Forest Pack | fehlt (Download-Liste) | 05, 07 |
| Travertine Hot Spring Terraces – Modular Environment Pack | fehlt (Download-Liste) | 08 |
| Tropical Vegetation Assets | fehlt (Download-Liste) | 04, 07 |

### Fehlt weiterhin

- Große Kalkfelsen/Karsttürme: Das vorhandene Limestone Rocks ist nur ein 0,6-m-Haufen. Ferat lädt gerade weitere Megascans-Limestone-Assets und das kostenlose „Limestone Rock Set“ von Ancraite („wird geladen“). Damit ist die Lücke voraussichtlich geschlossen; Netznamen folgen mit dem neuen Inventar. Bis dahin gelten `SM_Cliff_01a–e` (bis 75 m, skaliert) und `SM_LimestoneRocks2/3`.

### Material-Instanzen (0 von höchstens 6)

| Name | Basis | Parameter | für |
|---|---|---|---|

## Abgleich Inventar 13d (Stand 11.10.2026, abends)

Neues Inventar: 1 965 Netze, 116 Niagara, 85 Decals. Pfade, Maße und Paketstatus stehen in `asset_bedarf.json` → `abgleich_13d`. Orte und Kameras bleiben unverändert; die Phase-2-Planer werden gerade auf die echten Assets umgestellt.

**Jetzt erfüllt:**

- `dschungel_02_turmquelle` – Nature Water FX: Gischt am Fuß (B) / Sprühnebel: `NS_Waterfall_Medium`, `NS_Impact_Medium`
- `dschungel_02_turmquelle` – Mountain: Wasserfall aus der Wand + Abflussbach (A): `M_River_Water_Translucent`, `NS_Stream_Small`

**Ersatz → echtes Asset:**

- `dschungel_02_turmquelle`: statt lokaler Nebel als Gischt/Sprühnebel → `NS_Impact_Medium`
- `dschungel_02_turmquelle, dschungel_04_blaues_auge, dschungel_05_verborgene_lagune`: statt MI_Leakage_* als Nässe am Ufer → `MI_Deca_Wet` – Nassband an der Wasserlinie jetzt mit dem echten Coast-&-Dunes-Decal MI_Deca_Wet (flache Ufer MI_Deca_Wet_Flat) statt MI_Leakage_*/MI_TileableLeakage_*.

**Fehlt weiter:**

- Große Kalkfelsen/Karsttürme, Kalkplatten, Kalkschutt (dschungel_01_mondtor, dschungel_03_steinwald, dschungel_05_verborgene_lagune, dschungel_06_schluckhoehle) – weitere Megascans-Limestone-Assets / Ancraite „Limestone Rock Set“ – in netze.csv 13d NICHT enthalten; bis dahin SM_Cliff_01a–e skaliert + SM_LimestoneRocks2/3 · *noch nicht geladen, kostenlos → Claude lädt auf Wunsch*
- Tropische Uferpflanzen, Luftwurzeln (dschungel_04_blaues_auge, dschungel_07_garten_der_riesen) – Electric Dreams Environment (B) · *kostenlos → Claude lädt auf Wunsch*
- Riesenblätter (Held) (dschungel_07_garten_der_riesen) – Nanite Tropical Plant Pack 2 (B) · *nur nach Ferats OK*
- Sinterfahnen/Stalaktiten (dschungel_06_schluckhoehle, dschungel_08_sinterhalle) – Cave Stalactites & Wall Kit (B) · *nur nach Ferats OK*
- Höhlenklang (dschungel_06_schluckhoehle, dschungel_08_sinterhalle) – Cave Ambience (B) · *nur nach Ferats OK*
- Sinterbecken (dschungel_08_sinterhalle) – Travertine Hot Spring Terraces (B) · *nur nach Ferats OK*
