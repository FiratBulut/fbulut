# Bergwald – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

Stand 11.10.2026 · Agent B2 · Dateien: `standorte.json` (Prüfer: **0 FEHLER, 0 WARNUNG, 0 HINWEIS**), je Ort `<id>.png` (Draufsicht 2 m),
`asset_bedarf.json`. Alle Zahlen stammen aus den 2-m-Daten (`vorlagen/daten/sehens`) und aus `antworten/skripte/sehens_lib`
(Cache, Sichtlinien mit Gelände + `baumhoehe_4m`, Wegpunkte im 20-m-Raster).

## Das Biom in den Daten

- Zwei getrennte Teile: **West** (A3–C6, x −4404 … −2650 m) – ein N-S-Gebirgskamm bis 684 m, dessen Ostflanke in Rippen und
  Kerbtäler zerfällt; **Ost** (I3–J5, x 3352 … 4350 m) – ein schmaler Steilhang zum Meer. 4,38 km², davon nur **0,69 km²**
  erlaubte Ortsmitten (80–300 m vom Weg, ≥ 150 m von Städten, nicht in Orten, ≥ 30 m innen) – die Wege laufen nur am Fuß der
  Flanken, der Westhang des Kamms ist weglos und fällt ganz heraus.
- Boden: Fels 29 %, Nadeln 27 %, Gras 14 %, Wiese 12 %, Laub 4 %; Hang Median 36°, 90 %-Wert 58°; Bäume auf nur 12 % der
  Fläche (Höhe Median 18 m, 90 % 26 m) – der Wald steht in Bändern auf Rippen und Talböden, dazwischen nackter Fels.
- Heute (Bilder `BERG11_B4_rundgang`, `BIOM3_A4/I4`, `WASSER3_B4_WF_K1_weit`): graubraune Felsflanken mit Kopfsteinpflaster-Wirkung,
  Einzelbäume in Reihe auf dem Grat, kaum Unterwuchs, kein Totholz. Zielbild ist `witcher_07` (Nadelwaldschlucht mit
  Rostlärchen, Dunst, Bach im Grund) und `witcher_03` (Pfad zwischen Blöcken, Totholz, Schnee nur auf Simsen).
- **Folgerung (Hinweis Ferat):** Bäume blockieren Sichtlinien. Die drei Leuchtfeuer stehen deshalb dort, wo etwas **über die
  Krone** ragt (Felsnadel auf einer Rippennase, Brandkiefer auf einem Spornkopf, Riesentannen über einem Talboden); die fünf
  Fundstücke liegen in Kerben, Kesseln und Waldinnerem, wo der Wald und die Rippen sie verdecken.
- Ortsfindung: eigene Scores je Ortstyp (Skripte im Scratchpad `a13/b2_bergwald/`: `pool.py`, `waehle.py`, `build.py`) –
  Felskopf (TPI50/100 hoch, Fels, Wald im 60-m-Umfeld), Kuppe (TPI50 ≥ 10, Hang ≤ 20°), Hain (Hang ≤ 15°, Baumdichte, Nadeln,
  25–100 m vom Bach), Blockhalde (27° unter Fels, Hohlform), Klamm (TPI25 ≤ −5, Einzugsfläche, Hang ≥ 35°), Kar (TPI100 ≤ −15,
  flacher Boden), Windwurf (Waldhang 15–30°), Wurzelstein (Waldhang ~30° mit Fels). Danach Auswahl aller 8 zusammen mit
  ≥ 360 m Abstand (Kombinationssuche), Leuchtfeuer mit Sichtnachweis, Fundstücke nur, wenn `verdeckt_vom_weg` = wahr.
- Abstände: kleinster Abstand zwischen zwei Bergwald-Orten 372 m (Karsee–Wurzelstein), zu anderen Biomen 373 m (Klamm –
  `elfenwald_02_nebelhain`). Gesamtprüfung über alle vorhandenen `standorte.json` (aue, dschungel, elfenwald, lava, bergwald):
  **0 FEHLER** für den Bergwald. Verteilung: 6 Orte im West-, 2 im Ostteil (Ostteil 1,0 km², davon wenig Maske).
- Einmaligkeit: geprüft gegen den Katalog v1 aller Biome und die Ortsnamen der schon vorhandenen `standorte.json` (aue, dschungel, elfenwald, lava; deren `katalog.md` gab es noch nicht). Abgrenzung: Mönch ≠ „Die
  Erstarrten“ (Tundra, Pfeilergruppe auf kahler Kuppe) ≠ „Die Alten“ (Küste, Brandungspfeiler); Felsenmeer ≠ „Blockstrom“ (Heide,
  offene Blockzunge) – hier bemooste Blöcke **unter Wald** unter einer Abbruchkante; Brandkiefer ≠ „Die Alte“/„Mutterbaum“
  (lebende Laubbäume); Karsee ≠ „Schmelzsee“ (auf Gletschereis) und ≠ Moorauge/Erdfall-Weiher (Flachland); Klamm ≠ Farnschlucht
  (Elfenwald, Farnwände, kein Fall) und ≠ Flüsterschlucht (Sandstein, trocken).

## Übersicht

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden z | Radius | Weg | Nachweis (sicht.py) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `bergwald_01_der_moench` | Der Mönch | Leuchtfeuer | B3 | −3408 / −1102 | 348 m | 40 m | 296 m | 32-m-Silhouette von 66 / 175 Wegpunkten (300–800 m) ≥ 30 % lesbar, bis 800 m |
| 2 | `bergwald_02_die_brandkiefer` | Die Brandkiefer | Leuchtfeuer | B4 | −2990 / −920 | 164 m | 35 m | 101 m | 32 m: 56 / 233 Wegpunkte, bis 800 m; bester Punkt 706 m mit Anteil 1,0 |
| 3 | `bergwald_03_saeulenhain` | Säulenhain | Leuchtfeuer | B5 | −2764 / 104 | 81 m | 45 m | 104 m | 50 m: 59 / 179 Wegpunkte, bis 800 m; Fuß (3 m) von 0 / 264 Wegpunkten ≤ 800 m |
| 4 | `bergwald_04_felsenmeer` | Felsenmeer | Fundstück | B4 | −2938 / −510 | 130 m | 50 m | 84 m | verdeckt: 0 / 94 Wegpunkten ≤ 400 m, 0 / 342 ≤ 800 m (4 m) |
| 5 | `bergwald_05_klemmblock_klamm` | Klemmblock-Klamm | Fundstück | I4 | 3730 / −966 | 99 m | 40 m | 203 m | verdeckt: 0 / 26 ≤ 400 m, 0 / 62 ≤ 800 m (6 m) |
| 6 | `bergwald_06_karsee` | Karsee | Fundstück | B5 | −3210 / 72 | 259 m | 50 m | 285 m | verdeckt: 0 / 33 ≤ 400 m, 0 / 177 ≤ 800 m (4 m) |
| 7 | `bergwald_07_windwurf` | Windwurf | Fundstück | I4 | 3985 / −650 | 21 m | 55 m | 132 m | verdeckt: 0 / 53 ≤ 400 m, 0 / 81 ≤ 800 m (4 m) |
| 8 | `bergwald_08_der_wurzelstein` | Der Wurzelstein | Fundstück | B4 | −3262 / −296 | 357 m | 30 m | 275 m | verdeckt: 0 / 47 ≤ 400 m (6 m); aus 749–761 m sehen 3 Wegpunkte bis 72 % (im Wald nicht lesbar) |

Umbenennungen gegenüber Katalog v1/Download-Liste: „Blitzbaum“ → **Die Brandkiefer**; „Schleierfall“ ist jetzt Teil der
**Klemmblock-Klamm** (der Fall schließt die Klamm ab – im Gelände liegen beide an derselben Stufe); „Karsee“ übernommen,
**Der Wurzelstein** ist neu (ersetzt die Reserve „Schleierfall“ als eigenen Ort).

Gemeinsame Kameras: alle nach §8 auf Augenhöhe (Prüfer ohne Hinweis). Weil eine Kamera nach §8 nicht nach oben schauen kann,
sind `_anmarsch`, `_held`, `_fern` so gewählt, dass die **Oberkante** des Ziels höchstens 27° über dem Horizont liegt
(halber Bildwinkel ~29,5°).

---

## 1 · Der Mönch (`bergwald_01_der_moench`) – Leuchtfeuer

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

## 2 · Die Brandkiefer (`bergwald_02_die_brandkiefer`) – Leuchtfeuer

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

## 3 · Säulenhain (`bergwald_03_saeulenhain`) – Leuchtfeuer

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

## 4 · Felsenmeer (`bergwald_04_felsenmeer`) – Fundstück

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

## 5 · Klemmblock-Klamm (`bergwald_05_klemmblock_klamm`) – Fundstück

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

## 6 · Karsee (`bergwald_06_karsee`) – Fundstück

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

## 7 · Windwurf (`bergwald_07_windwurf`) – Fundstück

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

## 8 · Der Wurzelstein (`bergwald_08_der_wurzelstein`) – Fundstück

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

## Budgets (Richtwerte je Ort, Phase 2 verbindlich)

| Ort | Instanzen | Kollision | Akteure | Lichter | Niagara | Nebel | Decals | Fenster |
|---|---|---|---|---|---|---|---|---|
| 01 Mönch | 4 000 | 500 | 40 | 0 | 0 | 1 | 4 | 120 × 120 m |
| 02 Brandkiefer | 3 000 | 200 | 15 | 0 | 1 (opt.) | 0 | 8 | 80 × 80 m |
| 03 Säulenhain | 6 000 | 300 | 30 | 1 | 0 | 1 | 4 | 110 × 110 m |
| 04 Felsenmeer | 5 000 | 1 200 | 60 | 0 | 0 | 1 | 4 | 160 × 160 m |
| 05 Klamm | 4 000 | 600 | 45 | 1 | 1 (opt.) | 1 | 6 | 90 × 90 m |
| 06 Karsee | 4 000 | 500 | 25 | 0 | 0 | 1 | 4 | 140 × 140 m |
| 07 Windwurf | 5 000 | 400 | 40 | 0 | 1 (opt.) | 0 | 6 | 140 × 60 m |
| 08 Wurzelstein | 2 000 | 200 | 20 | 1 | 0 | 0 | 3 | 60 × 60 m |

Materialwünsche (≤ 6): `MI_EL_SW_Verkohlt` (`M_EL_Fels_MS`, `Toenung` [0,16, 0,14, 0,13, 1], `Helligkeit` 0,6 – Brandkiefer);
`MI_EL_SW_Klammfels_Nass` (`M_EL_Fels_MS`, `Nass_Dunkel` 0,75 – Klamm, Karsee-Ufer); `MI_EL_SW_Granit_Moos` (`M_EL_Klippe_RVT`,
`Moos_Menge_Akteur` 1,0, `Moos_Farbe` [0,75, 0,9, 0,55, 1] – Mönch, Klammwände); `MI_EL_SW_Block_Moos` (`M_EL_Fels_Auflage`,
`Auflage_Menge` 0,8, `Auflage_Farbe` [0,45, 0,6, 0,3, 1] – Felsenmeer, Wurzelstein).

## Offene Fragen an Ferat

1. **Nadel aus Klippenschale:** Für den Mönch gibt es kein Felsnadel-Netz; ich plane eine hochkant gestellte Granit-Schale
   (`veqnci0db_tier_2`). Reicht das, oder sollen wir ein Turm-/Spire-Paket suchen (fab.com war für mich nicht erreichbar)?
2. **Tote/liegende Bäume:** Die Kiefern/Tannen aus Mountain/Environment Set sind keine Nanite-Netze. Dürfen wir sie liegend
   (Windwurf) und auf 2,5× skaliert (Säulenhain) setzen, oder lieber auf „Forest Cretaceous“ warten?
3. **Karsee-Stempel:** Seespiegel und Schwelle brauchen bis ±6 m Gelände – ist das am Kamm in B5 in Ordnung (Feld-Neubau)?
4. **Bildwünsche** (leere Standorte, Kameras in `asset_bedarf.json`): Mönch `_fern`, Säulenhain `_fern`, Klamm `_held`,
   Karsee `_held` – damit wir die Silhouetten vor dem Bau prüfen können.
