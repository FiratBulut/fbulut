# Elfenwald – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

Stand 11.10.2026 · Agent B3 (elfenwald + dschungel) · Dateien: `standorte.json` (Prüfer `sehens_pruefen.py`: **0 FEHLER,
0 WARNUNG** für den Elfenwald; Gesamtprüfung aller vorhandenen Biome 0 FEHLER), je Ort `<id>.png` (Draufsicht 2 m mit geplanten
Elementen, Zugang und Kameras), `asset_bedarf.json`. Alle Zahlen aus den 2-m-Daten (`vorlagen/daten/sehens`) mit
`antworten/skripte/sehens_lib` (Cache, Sichtlinien Gelände + `baumhoehe_4m`, Wegpunkte im 20-m-Raster). Kameras nach §8 in der
Fassung 11.10. 13:00: `_anmarsch`, `_nah` und `_fern` mit **Hoch = −170** (genau Augenhöhe) und echtem Ziel, `_held` mit +170.

## Das Biom in den Daten

- Rechteck G2–I4 (x 1352 … 3590 m, y −2248 … −200 m), 3,66 km². In der Mitte die geplante **Elfenstadt** (2600/−700, r 190 m).
  Westteil (G3/G4/H3) hügelig 0–100 m mit vielen Bächen, einem Plateau (2050/−1000) und einer Wegschleife; im Süden der große Fluss.
  Ostteil (H2/H3/H4 jenseits x ≈ 2900) ist ein wegloses Gebirge bis 489 m (Fels 17 % des Bioms, Hang bis 64°) – dort keine
  Ortsmitte möglich (> 300 m vom Weg), nur der Ostrand in I4 liegt wieder nahe einer Straße.
- Boden: Laub 60 %, Fels 17 %, Gras 7 %, Erde 4 %, Moos 4 %, Kies 3 %; Hang Median 19°; Bäume auf 26 % der Fläche, 90 %-Wert 16 m,
  vereinzelt bis 37 m. Erlaubte Ortsmitten (80–300 m Weg, ≥ 150 m Stadt, nicht im Ort, ≥ 30 m innen): **0,94 km²**.
- Heute (Bilder `NAH2_G4_elfenw_nah0`, `CLOUD3_G4_hain0`, `BIOM3_I4_rundgang`, `WASSER3_H4_WF_K8_weit`): klarer See mit
  Hängebirken, gleichmäßiger Jungwald, Heide-/Trockengrasflächen, kaum Unterwuchs, kein Totholz, keine Riesen – es wirkt wie ein
  normaler Mischwald. Zielbild `witcher_07` (dunkle Kronen, Rostakzente, Dunst, Bach im Grund) und `witcher_03` (Totholz, Kiesel,
  Moos, Licht zwischen Stämmen); Farbe nach Dragon Age (Emerald Graves): sattes Grün, kühle Schatten, wenige warme Akzente.
- **Leitidee:** Der Elfenwald ist ein *Märchenwald, der aus Natur besteht* – alles ist ein wenig größer, älter, feuchter und
  leuchtender als im Bergwald oder in der Aue: Riesenbäume, Riesenpilze, Leuchtpilze, Moos, Farn, Kalktuff, Nebel im Kronendach.
  Keine Bauten, keine Elfenspuren; das „Elfische" entsteht nur durch Maßstab, Licht und Farbe.

## Methode

Eigene Scores je Ortstyp (Skripte im Scratchpad `a13/b3_elfen_dschungel/`: `such_elf.py`, `such_pilz.py`, `baeche.py`,
`kombi_e.py`, `plan.py`):

| Ortstyp | Score aus den Daten |
|---|---|
| Riesenbaum (Leuchtfeuer) | TPI100 5–30 m, TPI50 > 2 m, Hang ≤ 8–25°, Baumdichte; dann Sicht mit 55 m Zielhöhe |
| Nebelhain (Leuchtfeuer) | Kuppe/Oberhang mit TPI100 > 25 m; Sicht mit 28 m Zielhöhe |
| Rotlaubhain (Leuchtfeuer) | Hang 10–26° (Glocke um 18°), TPI100 > 0, dichter Wald; Sicht mit 24 m |
| Kalktuff-Treppe | Bachabschnitte (Vektor `baeche_alle`) mit 6–25 % Gefälle auf 40 m, ≥ 60 m innen |
| Farnschlucht | TPI25 ≤ −3 m, mittlerer Hang 25–45° im 16-m-Umkreis, Einzugsfläche 3 000–40 000 m² |
| Blauer Grund | Hang ≤ 4–14°, Baumdichte (30-m-Fenster) hoch, flache Mulde, ≥ 30 m vom Wasser |
| Schwammgrund | TPI50 negativ, 10–50 m vom Wasser, dichter Wald, Nordexposition |
| Wurzelbrücke | Kerbe am Bach: TPI25 negativ, Einzugsfläche ≥ 10 000 m², steile Flanken |

Danach Auswahl der 8 zusammen per Kombinationssuche (≥ 350 m untereinander und zu allen belegten Punkten anderer Biome,
Abzug für Orte < 80 m an der Rechteckgrenze), Leuchtfeuer nur mit Sichtnachweis 300–800 m, Fundstücke nur mit
`verdeckt_vom_weg` = wahr. Kleinster Abstand im Elfenwald: 369 m (Schwammgrund – Blauer Grund); zu anderen Biomen: 373 m (Nebelhain – `bergwald_05_klemmblock_klamm`).

## Abgrenzung (keine Dopplung)

| Elfenwald | nicht zu verwechseln mit | Unterschied |
|---|---|---|
| Mutterbaum (Riesenbaum über dem Kronendach) | aue „Die Alte" (Buche auf offener Wiese), bergwald „Säulenhain" (12 Riesentannen), bergwald „Wurzelstein" (Fichte umklammert Findling) | ein einzelner Laub-Riese **im** dichten Wald, ragt 30 m über die Wipfel; Brettwurzeln **ohne** Fels, Wurzelhalle mit Leuchtpilzen |
| Nebelhain (Nebelwald auf dem Gipfel) | sumpf „Geisterwald" (tote Stämme im Wasser) | lebende, knorrige, moosbehangene Altbäume auf trockenem Fels, Wolke im Kronendach |
| Rotlaubhain | bergwald Rostlärchen-Akzent | Laubbaum-Hain mit rotem Laub, als einziges Farbfeld im Grün |
| Elfentreppe (Kalktuff-Stufen im Waldbach) | gletscher „Der Atem", tundra „Warme Quelle", canyon „Hängender Garten" | kaltes, klares Bachwasser, grüne Moostuff-Stufen – kein Dampf, keine Sinterwand |
| Farnschlucht (Tobel mit Farnwänden) | bergwald „Klemmblock-Klamm" | Wände bestehen aus Farn statt Fels, kein Klemmblock, kein Wasserfall – Kaskadenbach |
| Blauer Grund (blau blühender Waldboden) | aue „Lilienrinne", aue „Hexenring" | Blüten **unter** geschlossenem Buchendach, ganze Fläche blau-violett, kein Ring |
| Schwammgrund (Riesenpilze auf Moderholz) | aue „Hexenring" (Pilzring) | 2–4 m hohe Pilze und Baumschwämme auf einem gestürzten Riesen – Zersetzung, kein Ring |
| Wurzelbrücke (ein gestürzter Riese als Brücke) | bergwald „Windwurf" (viele Stämme), bergwald Säulenhain-Ammenstamm | **ein** 44-m-Stamm quer über eine Bachkerbe, Wurzelteller steht 8 m hoch |

Gegenüber dem eigenen Dschungel (B3): Riesenbäume, Pilze, Leuchtpflanzen, Nebel und Farn gibt es **nur** im Elfenwald; der
Dschungel bekommt Kalkfels, Karstwasser und Riesenblätter. Aus Katalog v1 entfallen „Silberhain" (zu nah an aue „Hexenring":
Birken + weiße Blüten), „Steinernes Tor" (Felsbögen haben Wüste, Canyon und Dschungel-Mondtor) und „Glühwürmchen-Lichtung"
(Licht trägt bei fester Sonne nicht, sumpf hat Irrlichter). Neu: Nebelhain, Blauer Grund, Schwammgrund.

## Die 8 Orte

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden | Weg | Radius | Sicht / Verdeckung (sicht.py) | Zugang |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `elfenwald_01_mutterbaum` | Mutterbaum | Leuchtfeuer | G3 | 1736 / −1302 | 40,6 m | 94 m | 55 m | 55 m: 82 / 339 Wegpunkte (300–800 m) ≥ 30 %, bis 758 m; bester 315 m, Anteil 0,90 | Fußweg 98 m, max 24° |
| 2 | `elfenwald_02_nebelhain` | Nebelhain | Leuchtfeuer | I4 | 3460 / −708 | 392,7 m | 295 m | 55 m | 28 m: 47 / 80 Wegpunkte, Mittel 0,43, bis 710 m; bester 371 m, Anteil 1,00 | **Pfad**: 921 m Serpentinen |
| 3 | `elfenwald_03_rotlaubhain` | Rotlaubhain | Leuchtfeuer | H4 | 2744 / −1030 | 103,1 m | 173 m | 50 m | 24 m: 62 / 254 Wegpunkte, bis 799 m; bester 456 m, Anteil 0,90 | Fußweg 185 m, max 18° |
| 4 | `elfenwald_04_elfentreppe` | Elfentreppe | Fundstück | H3 | 2390 / −1230 | 31,6 m | 109 m | 45 m | verdeckt: 0 / 159 Wegpunkte ≤ 400 m (4 m) | Fußweg 157 m, max 24° |
| 5 | `elfenwald_05_farnschlucht` | Farnschlucht | Fundstück | H3 | 2762 / −1588 | 87,2 m | 208 m | 45 m | verdeckt: 0 / 67 (4 m) | **Pfad** 229 m (11 m steil) |
| 6 | `elfenwald_06_blauer_grund` | Blauer Grund | Fundstück | G4 | 2112 / −390 | 24,4 m | 153 m | 45 m | verdeckt: 0 / 99 (3 m) | Fußweg 158 m, max 16° |
| 7 | `elfenwald_07_schwammgrund` | Schwammgrund | Fundstück | G4 | 1808 / −600 | 17,2 m | 100 m | 40 m | verdeckt: 0 / 81 (4 m) | Fußweg 103 m, max 7° |
| 8 | `elfenwald_08_wurzelbruecke` | Wurzelbrücke | Fundstück | H3 | 2361 / −1624 | 9,2 m | 83 m | 40 m | verdeckt: 0 / 106 (4 m) | Fußweg 97 m, max 20° |

„Sicht" = Silhouette der angegebenen Zielhöhe über dem Boden der Ortsmitte; ein Wegpunkt zählt, wenn ≥ 30 % davon über
Gelände und Kronen (`baumhoehe_4m` × 0,85) frei sind. „Verdeckt" = kein Wegpunkt bis 400 m sieht mehr als 15 % der
Fundstück-Silhouette.

---

## 1 · Mutterbaum (`elfenwald_01_mutterbaum`) – Leuchtfeuer

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

## 2 · Nebelhain (`elfenwald_02_nebelhain`) – Leuchtfeuer

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

## 3 · Rotlaubhain (`elfenwald_03_rotlaubhain`) – Leuchtfeuer

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

## 4 · Elfentreppe (`elfenwald_04_elfentreppe`) – Fundstück

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

## 5 · Farnschlucht (`elfenwald_05_farnschlucht`) – Fundstück

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

## 6 · Blauer Grund (`elfenwald_06_blauer_grund`) – Fundstück

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

## 7 · Schwammgrund (`elfenwald_07_schwammgrund`) – Fundstück

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

## 8 · Wurzelbrücke (`elfenwald_08_wurzelbruecke`) – Fundstück

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

## Budgets (Richtwerte §9)

| Ort | Instanzen | Kollision | Akteure | Lichter | Niagara | Nebel | Decals | Geländefenster |
|---|---|---|---|---|---|---|---|---|
| 01 Mutterbaum | 5 000 | 200 | 25 | 2 | 1 (opt.) | 1 | 4 | 140 × 140 m |
| 02 Nebelhain | 6 000 | 300 | 30 | 0 | 1 (opt.) | 2 | 8 | 120 × 120 m + Pfad |
| 03 Rotlaubhain | 4 000 | 100 | 15 | 0 | 1 (opt.) | 0 | 0 | 120 × 120 m |
| 04 Elfentreppe | 5 000 | 300 | 20 | 0 | 0 | 1 | 7 | 80 × 50 m |
| 05 Farnschlucht | 9 000 | 300 | 12 | 0 | 0 | 1 | 6 | 90 × 40 m |
| 06 Blauer Grund | 9 000 | 50 | 10 | 1 | 1 (opt.) | 1 | 2 | 120 × 120 m (nur Lagen) |
| 07 Schwammgrund | 4 000 | 150 | 15 | 2 | 1 (opt.) | 1 | 4 | 60 × 30 m |
| 08 Wurzelbrücke | 3 000 | 200 | 10 | 0 | 0 | 0 | 2 | 60 × 40 m |

Alle Felder bleiben weit unter 60 000 neuen Instanzen (G3: 3 Orte ≈ 13 000, H3: 4 Orte ≈ 23 000).

## Offene Fragen an Ferat

1. Rotlaubhain lebt von roter Blatt-Tönung der Buchen (`Forest_Environment_Set`) – darf ich dafür eine Material-Instanz der
   Buchenblätter anlegen lassen (statt M_EL_Pflanze)?
2. Nebelhain braucht einen 0,9-km-Serpentinenpfad am Osthang – ist ein Pfad dieser Länge für dich in Ordnung, oder soll ich den
   Ort auf eine niedrigere, schlechter sichtbare Kuppe legen?
3. Mutterbaum/Wurzelbrücke: Forest Cretaceous (Riesenstämme) ist auch für den Bergwald gewünscht – lohnt der Download (8 GB)?
