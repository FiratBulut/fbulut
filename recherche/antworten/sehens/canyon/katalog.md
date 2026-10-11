# Canyon – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1, Biom-Agent B6)

Stand 11.10.2026 · Daten: `vorlagen/daten/sehens` (2 m) · Werkzeuge: `antworten/skripte/sehens_lib` · Dateien: `standorte.json`
(8 Orte, Prüfer **0 FEHLER / 0 WARNUNG**), `asset_bedarf.json`, `<id>.png` je Ort (Draufsicht mit Elementen, Zugang, Kameras).
Inventar Stand 13b (1 692 Netze, 73 Niagara). Felder C4/D4 sind gebaut (Namaqualand-Planer) – alles hier **ergänzt** nur.

## Das Gelände in Zahlen

Das Canyon-Biom (1,01 km², Felder D4/C4/D3) ist ein **Sandsteinplateau auf 80–116 m**, in das ein Fluss einen 38–40 m tiefen,
mäandrierenden Canyon geschnitten hat (Sohle 40–47 m, Wände bis 72°). Nach Süden bricht das Plateau mit einer gebänderten
**Schichtstufe** (82 → 35 m) zur Aue ab, nach Norden mit einer zweiten Stufe zur Küste. Zwei Ringrücken (bis 111 m) sitzen auf dem
Plateau, ein Seitenbach erreicht den Hauptcanyon als Hängetal.

| Kennzahl | Wert |
|---|---|
| Fläche ≤ 300 m vom Weg | 0,53 km² (80–300 m: 0,34 km²) |
| davon mit Canyon-Boden (Sand/Sandstein/Geröll ≥ 70 %) | 0,18 km² |
| größter Wegabstand | 670 m (Nordhälfte, Wege nur jenseits der Bucht → nicht zu Fuß erreichbar, Wasser 120 m) |
| Packung bei 200 m Abstand (Canyon ist klein) | bis 13 Mitten; zusammen mit der Wüste (350 m zueinander) 8 + 8 |

Alle 8 Orte liegen deshalb in der Südhälfte: an der Südstufe, in der Mäanderschleife und an den Schichtrippen des Canyonausgangs.
Kein neuer Pfad nötig; fünf Orte brauchen einen kurzen **Zugangspfad mit Kehren** (Verlauf `pfad_cm` am Ort, nicht als `pfade[]`,
weil Pfade sonst als Weg zählen und der Ort 0 m vom „Weg“ läge).

## Übersicht

| ID | Name | Art | Form | Feld | X / Y (m) | Weg | Sicht |
|---|---|---|---|---|---|---|---|
| canyon_01_sonnenfenster | Das Sonnenfenster | Leuchtfeuer | Felsbogen in einer Randfinne | D4 | −1430 / −460 | 113 m | 174/300 Wegpunkte |
| canyon_02_der_waeger | Der Wäger | Leuchtfeuer | Balancierfels auf Rippenkuppe | D4 | −1049 / −415 | 118 m | 126/345 |
| canyon_03_rote_stufe | Die Rote Stufe | Leuchtfeuer | Tafelberg-Abbruch, Schichtstufen | C4 | −1910 / −460 | 300 m | 106/268 |
| canyon_04_fluesterschlucht | Die Flüsterschlucht | Fundstück | Slot-Canyon des Seitenbachs | D4 | −1235 / −848 | 258 m | verdeckt mit Stempel |
| canyon_05_hoodoo_kessel | Der Hoodoo-Kessel | Fundstück | Erosionskessel mit Hoodoos | D4 | −1380 / −700 | 221 m | verdeckt |
| canyon_06_die_kolke | Die Kolke | Fundstück | Pothole-Becken auf Slickrock | D4 | −1570 / −620 | 299 m | verdeckt |
| canyon_07_smaragdgumpe | Die Smaragdgumpe | Fundstück | Fall + Gumpe im Alkoven, Hängender Garten | C4/D4 | −1672 / −438 | 194 m | verdeckt mit Stempel |
| canyon_08_die_welle | Die Welle | Fundstück | kreuzgeschichteter Sandsteinwirbel | D4 | −876 / −288 | 136 m | verdeckt mit Stempel |

Mischung 3 Leuchtfeuer / 5 Fundstücke. Die Orte erzählen das Wasser des Plateaus: Regen sammelt sich in den **Kolken** (06), läuft
als Bach zur Südstufe und fällt in die **Smaragdgumpe** (07); ein zweiter Bach hat die **Flüsterschlucht** (04) gesägt und stürzt in
den Hauptcanyon, dessen Rand zum **Hoodoo-Kessel** (05) zerfällt. Wind und Frost lösen Finnen (01), Säulen (02) und Stufen (03).

**Abgrenzung:** Sandstein-Formen aus Wasser-Erosion. Nicht hier: Felsbogen im Karst (dschungel_01 Mondtor, Kalk), Pilzfelsen aus
Windschliff (wueste_03), Yardangs (wueste_01), Bunte Ton-Hänge und Badland-Rinnen (oedland_01/02), Basaltsäulen (lava). Hoodoo
(schlank, gebändert, im Kessel, Deckstein) ≠ Pilzfelsen (gedrungen, Wind-Hohlkehle am Fuß, frei auf der Fläche).
**Sichtmessung:** `sicht.py`, Wegpunkte alle 20 m, Gelände + `baumhoehe_4m`, Wege inklusive aller Pfade aus `pfade[]` (Stand 13c).
Leuchtfeuer: Wegpunkte im Ring 300–800 m mit ≥ 30 % Silhouette. Fundstück: kein Wegpunkt ≤ 400 m sieht > 15 % eines 3-m-Ziels –
heute und mit dem geplanten Stempel (Delta auf die Höhe gerechnet, dann neu gemessen). Kameras §8 (Stand 13:00): `_anmarsch`/`_nah`
Hoch −170 mit echtem Ziel, `_held`/`_fern` +170.

---

## canyon_01_sonnenfenster – Das Sonnenfenster (Leuchtfeuer)

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

## canyon_02_der_waeger – Der Wäger (Leuchtfeuer)

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

## canyon_03_rote_stufe – Die Rote Stufe (Leuchtfeuer)

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

## canyon_04_fluesterschlucht – Die Flüsterschlucht (Fundstück)

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

## canyon_05_hoodoo_kessel – Der Hoodoo-Kessel (Fundstück)

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

## canyon_06_die_kolke – Die Kolke (Fundstück)

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

## canyon_07_smaragdgumpe – Die Smaragdgumpe (Fundstück)

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

## canyon_08_die_welle – Die Welle (Fundstück)

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

## Offene Fragen an Ferat (Canyon)

- Die Nordhälfte des Canyons (Mäander-Oberlauf, Nordstufe, Ringrücken, Mündungsfall bei X −1610 / Y −1090) ist 400–670 m vom Weg und
  nur über Wasser erreichbar – ein späterer „Canyonsteig“ vom Burgweg ROMAN_LOC_003 am Rand entlang würde 2–3 weitere Orte öffnen.
- Darf die Welle eine eigene prozedurale Decal-Textur (Linienmuster) bekommen?

## Abgleich Inventar 13d (Stand 11.10.2026, abends)

Neues Inventar: 1 965 Netze, 116 Niagara, 85 Decals. Pfade, Maße und Paketstatus stehen in `asset_bedarf.json` → `abgleich_13d`. Orte und Kameras bleiben unverändert; die Phase-2-Planer werden gerade auf die echten Assets umgestellt.

**Jetzt erfüllt:**

- `canyon_03_rote_stufe` – Desert Western Cliff Layered XL 14 als Stufenwand mit Bändern (A): `venuafk_tier_0 (Desert_Western_Cliff_Layered_XL_11)`, `uk5oded_tier_0 (Desert_Western_Cliff_Layered_XL_02)`, `vjqhcapga_tier_0 (Desert_Western_Cliff_Layered_XL_07)`
- `canyon_01_sonnenfenster` – Desert Western: geschichtete Bogenfinne mit Farbbändern (B): `vepnfcr_tier_0 (Desert_Western_Formation_Layered_XL_03)`, `vjqiaa2qx_tier_0 (Desert_Western_Formation_Layered_XL_05)`, `vb1mbdega_tier_0 (Desert_Western_Cliff_Layered_Large_02)`
- `canyon_04_fluesterschlucht` – Desert Western: glatt gewaschene, geschwungene Schluchtwände (B): `vjqhcapga_tier_0 (Desert_Western_Cliff_Layered_XL_07)`, `vceoferfa_tier_0 (Desert_Western_Cliff_Layered_XL_03)`, `veoneio_tier_0 (Desert_Western_Cliff_Layered_XL_01)`
- `canyon_04_fluesterschlucht` – Mountain/Nature Water FX: Austritt des Falls in den Canyon (A): `NS_Waterfall_Small`, `NS_Impact_Small`, `M_River_Water_Translucent`
- `canyon_05_hoodoo_kessel` – Hoodoo-Schäfte (Hollowstone B / Procedural Rocks C): `vepoda2_tier_0 (Desert_Western_Spire_Large_03)`, `ulbwebv_tier_0 (Desert_Western_Spire_Large_05)`, `vh3oagiga_tier_0 (Desert_Western_Spire_Layered_XL_03)`, `vennei3_tier_0 (Desert_Western_Spire_Layered_XL_04)`, `vijmaacqx_tier_0 (Desert_Western_Spire_Layered_XL_05)`
- `canyon_05_hoodoo_kessel` – Desert Western: Kesselwand mit Bändern (B): `umsocbyfa_tier_0 (Desert_Western_Cliff_Layered_XL_08)`, `vceldhvfa_tier_0 (Desert_Western_Cliff_Layered_XL_16)`
- `canyon_02_der_waeger` – Procedural Rocks Generator (C): Sockelsäule mit Taille: `ulbwebv_tier_0 (Desert_Western_Spire_Large_05)`
- `canyon_06_die_kolke` – Coast & Dunes: Nass-/Kiesel-Decals am Kolkrand (B): `MI_Deca_Wet`, `MI_Decal_Rocks_Small`
- `canyon_07_smaragdgumpe` – Mountain/Nature Water FX: 38-m-Fall mit Gischt (A/C): `NS_Waterfall_Medium`, `NS_Impact_Medium`, `M_River_Water_Translucent`
- `canyon_07_smaragdgumpe` – Coast & Dunes: Nassband an der Gumpe (B): `MI_Deca_Wet`
- `canyon_08_die_welle` – Desert Western Cliff Layered Large 03 als Wellenplatte (A): `vbzmdd1ga_tier_0 (Desert_Western_Cliff_Layered_Large_03)`, `venodhb_tier_0 (Desert_Western_Patch_Ground_Slate_Small_01)`

**Ersatz → echtes Asset:**

- `canyon_06_die_kolke`: statt Held uk5ebcp_tier_0 + uldubik_tier_0 (UNVOLLSTÄNDIG angekommen – nicht verwenden) → `vbvqbbofa_tier_0 (Desert_Western_Ledge_Rock_Large_03)`, `uk5pbhv_tier_0 (Desert_Western_Ledge_Rock_Medium_07)`, `ulerccg_tier_0 (Desert_Western_Ledge_Rock_Small_05)`, `uk5ocf2_tier_0 (Canyon_Sandstone_Rocky_Ground)` – Ledge_Rock_Large_03 (20,7 m) als Felsbank mit Kolken, Ledge_Rock_Medium_07/Small_05 und Canyon_Sandstone_Rocky_Ground als Ränder.
- `canyon_08_die_welle`: statt Held uk5ebcp_tier_0, Begleiter uldubik_tier_0 (UNVOLLSTÄNDIG – nicht verwenden) → `vbzmdd1ga_tier_0 (Desert_Western_Cliff_Layered_Large_03)`, `uk4pehu_tier_0 (Desert_Western_Cluster_Rock_Medium_06)` – MI_EL_SW_Welle auf vbzmdd1ga_tier_0 umhängen (statt uk5ebcp_tier_0).
- `canyon_01, _03, _04, _05`: statt SM_MassiveSandstoneCliff_01–05, SM_HugeSandstoneCliff_*, vmnmbhv/ukjhcamga_tier_0 + MI_EL_SW_Canyon_Rotband → `venuafk_tier_0 (Desert_Western_Cliff_Layered_XL_11)`, `uk5oded_tier_0 (Desert_Western_Cliff_Layered_XL_02)`, `vepnfcr_tier_0 (Desert_Western_Formation_Layered_XL_03)`, `vjqhcapga_tier_0 (Desert_Western_Cliff_Layered_XL_07)` – Desert Western hat die Farbbänder schon in der Textur (Fab-Material M_MS_Base, Nanite, kein Material-Fix) → Rotband-Tönung nur noch für Begleiter aus dem alten Bestand.
- `canyon_07_smaragdgumpe`: statt lokaler_nebel + NS_SmokePuffLight weiß als Gischt → `NS_Impact_Medium`

**Nicht verwenden (unvollständig angekommen, Ferat lädt neu):** `uk5ebcp_tier_0 (Desert_Western_Ledge_Rock_Small_07_uk5ebcp)`, `uldubik_tier_0 (Desert_Western_Cluster_Rock_Medium_05_uldubik)`

**Fehlt weiter:**

- Wäger-Kopf mit geschlossener Rückseite (canyon_02_der_waeger) – Wadi Rum Sandstone Rock 01–04 (jetzt C) · *nur nach Ferats OK*
- Wind-Flüstern in der Kerbe (Klang) (canyon_04_fluesterschlucht) – Fantasy Ambiences (B) · *nur nach Ferats OK*
- Desert Western Cliff Layered XL 14 (ursprünglicher Wunsch) (canyon_03_rote_stufe) – nicht nötig – XL_02/XL_11 decken es · *ohne Paket*
