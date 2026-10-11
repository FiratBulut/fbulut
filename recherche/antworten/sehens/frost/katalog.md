# Frost – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

Stand 11.10.2026 · Agent B4 · Dateien: `standorte.json` (heute gültige Orte), `standorte_steige.json` (Orte, die einen neuen Steig brauchen, mit Steig-Polylinien), je Ort `<id>.png` (Draufsicht 2 m, Steige orange, Zugangspfad gelb), `asset_bedarf.json`. Alle Zahlen aus den 2-m-Daten mit `antworten/skripte/sehens_lib` (Cache, Sichtlinien Gelände + `baumhoehe_4m`, Wegpunkte 20 m); eigene Scores/Skripte im Scratchpad `a13/b4_eis_fjord/` (`kand_gl.py`, `kand_fr.py`, `kand_fj.py`, `opt_gl*.py`, `steig.py`, `build.py`).

## Das Biom in den Daten

- 0,71 km² im Rechteck X −148 … 788 m, Y −2898 … −1900 m (E2/F2/E3): die verschneite Halbinsel östlich des Frostlagers. Boden Schnee 86 %,
  Fels 5,5 %, Eis 5,5 % (der zugefrorene **Frostsee**, Spiegel 19 m, ~175 × 200 m, S_K13_FROSTSEE_00 mit eis = true), Geröll 2,4 %;
  Hang Median 21°; Bäume 4,3 % (lichte Kiefern). Nordrand: Felsband bis 340 m, Nordostecke: Blockhang mit gefrorenem Tümpel, Ostküste flach.
- **Wege:** keiner im Biom. Der nächste Weg (Straßenende östlich des Frostlagers, X −520) liegt 322 m vor dem Rechteck; mit der
  150-m-Zone der kleinen Biome bleiben nur 0,045 km² am Westrand – das ist Gletscher-Gelände (Toteisloch), kein Frost.
- **Folgerung:** alle 8 Orte hängen am **Froststeig** (Straßenende Ost → Nordufer Frostsee → Küste, 1290 m, max 25°) und seinem
  **Südast** (Westufer → Südufer, 708 m, max 24°). Das ist der günstigste Steig von B4: flach, kurz, ganz im Schnee. `standorte.json` ist
  deshalb leer (Prüfer: WARNUNG „0 Orte“), die Orte stehen in `standorte_steige.json`.
- Thema des Bioms: **gefrorenes Wasser** (See-, Bach-, Sicker-, Spritz- und Raueis) – im Gegensatz zum Gletscher (Gletschereis, Moränen) und
  zur Tundra (Permafrostboden: Pingo, Aufeis, Steinringe, Wabenmoor – tundra/standorte.json, 11:44). Pingo und Aufeis bleiben bei der Tundra.
- Heute: Schneefläche fast ohne Relief, Kiefern einzeln; am Nordufer stehen noch Houdini-Reste (K13_FROSTSEE) – werden ausgeblendet, nichts
  davon verwenden.

## Prüfung

- `sehens_pruefen.py` (alle `standorte.json`, mit Daten): **0 FEHLER**; WARNUNG nur „0 Orte (Soll 8)“, weil die übrigen Orte am Steig hängen.
- `standorte_steige.json` mit demselben Prüfer gegen **Wege + Steige** (Steige als Wegzellen gerastert): **0 FEHLER**, 0 WARNUNG; globale Abstände über alle Biome inklusive aller bedingten Orte (auch lava/standorte_kratersteig nicht betroffen): **0 FEHLER**.
- Kameras nach §8 in der Fassung 11.10. 13:00: alle vier mit **Hoch = −170** (Augenhöhe) und echtem Ziel; Prüfer-Hinweise nur „_anmarsch x m vom Weg“ (Kamera steht auf dem Zugangspfad, dort wo sich der Ort öffnet).
- Bitte bei der globalen Prüfung `*/standorte_steige.json` mitnehmen (wie `lava/standorte_kratersteig.json`), sonst setzen andere Biome Orte in die Steig-Räume.

## Übersicht

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden z | Radius | Weg (Steig) | gilt | Nachweis (sicht.py) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `frost_01_der_eisfall` | Der Eisfall | Fundstück | E2 | 75 / −2420 | 40 m | 50 m | 544 m (86) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: ab ≤ 561 m |
| 2 | `frost_02_frostsee` | Der Frostsee | Leuchtfeuer | E2 | 200 / −2260 | 20 m | 110 m | 690 m (108) | Steig | 6 m: 51/159 Punkte, bis 762 m |
| 3 | `frost_03_eisvorhang` | Der Eisvorhang | Fundstück | E2 | 300 / −2460 | 30 m | 45 m | 771 m (87) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: ab ≤ 550 m |
| 4 | `frost_04_raureifhain` | Der Raureifhain | Leuchtfeuer | F2 | 330 / −2680 | 139 m | 70 m | 839 m (88) | Steig | 16 m: 55/150 Punkte, bis 777 m |
| 5 | `frost_05_blockgletscher` | Der Blockgletscher | Fundstück | F2 | 520 / −2800 | 69 m | 80 m | 1058 m (250) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: ab ≤ 531 m |
| 6 | `frost_06_eiskueste` | Die Eisküste | Leuchtfeuer | F2 | 630 / −2520 | 9 m | 70 m | 1104 m (94) | Steig | 8 m: 6/91 Punkte, bis 788 m |
| 7 | `frost_07_frostblumen` | Die Frostblumen | Fundstück | F2 | 450 / −2270 | 3 m | 60 m | 933 m (191) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: ab ≤ 790 m |
| 8 | `frost_08_glockenbach` | Der Glockenbach | Fundstück | E2 | 230 / −2060 | 3 m | 50 m | 788 m (90) | Steig | verdeckt vom Weg: ja (0/0 ≤ 400 m); Steig: ab ≤ 795 m |

---

## 1 · Der Eisfall (`frost_01_der_eisfall`) – Fundstück · nur mit Steig `froststeig`

**Was man sieht.** Wo der Nordbach über eine 12-m-Stufe in den Frostsee fällt, ist er mitten im Sturz erstarrt: ein Bündel aus milchig-blauen Eissäulen, zwischen denen hinter dünnem Eis noch Wasser rinnt – man hört es, aber sieht es nur als Schatten. Am Fuß ein Kegel aus gefrorener Gischt.

**Vorbild.** Real: gefrorene Fälle im Johnston Canyon (Kanada), Eisfälle des Kandertals, Gefrorener Fall von Fang (Ouray). Spiel: Eisfälle in Skyrim (Winterfeste) und The Long Dark.

**Standort.** Feld E2, X 75 / Y −2420, Boden 40,0 m. Offener Hang; Boden Schnee 85 %, Fels 9 %, Eis 6 %; Hang 15° (max 78°), Exposition 199°, TPI25 1,5 m, TPI100 −3,7 m, Relief 42 m im Radius. Weg 544 m (Punkt −470/−2424), **mit Steig 86 m** (`froststeig`); Wasser 0 m, Meer 383 m, Stadtrand 609 m (EXP_003); 224 m innerhalb des Bioms; 32 Baumzellen im Radius (max 28 m); Einzugsfläche max 95064 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 26 von 272 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 561 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Vom Froststeig aus (86 m) nur als heller Streifen in einer Kerbe erkennbar; die Säulen öffnen sich im Einschnitt. Held-Blick vom Seeeis hinauf. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 74 m (X 89 / Y −2492), `_held` 44 m (X 83 / Y −2463), `_nah` 10 m (X 77 / Y −2430). **Zugang (kandidaten.erreichbarkeit, 4 m):** 104 m vom Steig (Luftlinie 94 m), max 24,4°, Mittel 17,7°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Eissäulen aus `SM_EISZAPFEN_4/8/9` (1,5–3×, gebündelt, 20–30 Stück) + Eisschale; Material `M_EL_Eis4` (Eis_Farbe heller, Schnee_Menge 0,3). Begleiter (4): Felsköpfe `SM_big_rock_wall_02`, `rcygn_tier_0` mit Eisglasur. Schutt (60–100): gebrochene Zapfen `SM_EISZAPFEN_1/2/5` am Fuß, Steine `SM_NordicBeachRock_01`. Kleinzeug: Eiskrümel (Lage Eis). Bewuchs: vereiste Zwergkiefern am Rand `SM_dwarf_pine_small_01/02` (Material Raureif, s. Materialwünsche). Kontaktzone: Gischteis überzieht die Felsen bis 6 m seitlich (Lage Eis, Decal nass `MI_Leakage_02`).

**Wasser, Effekte, Licht.** Bach oben als `bach` (farbe `klar`) bis zur Kante, darunter kein fließendes Wasser – nur ein schmaler `wasserfall`-Streifen 0,5 m mit `MI_EL_Wasserfall_Kaskade` hinter den Säulen (Deckkraft niedrig). Kalter Dunst `lokaler_nebel` 0,04.

**Geländeänderung.** Stufe versteilen (+2 m Kante, 70–80 Grad), Kegel +1,5 m. Fenster 80 × 60 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_4`, `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_big_rock_wall_02`, `rcygn_tier_0`, `SM_EISZAPFEN_1`, `SM_EISZAPFEN_2`, `SM_EISZAPFEN_5`, `SM_NordicBeachRock_01`, `SM_dwarf_pine_small_01`, `SM_dwarf_pine_small_02`; Decals: `MI_Leakage_02`; Material: `M_EL_Eis4`, `MI_EL_Wasserfall_Kaskade`. Wunsch: **CryoGen: Native Procedural Ice Architecture** (B) – Eissäulen/Tropfeis auf Fels, Ersatz: SM_EISZAPFEN_4/8/9 bis 3x skaliert; **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (B) – Eiskegel am Fuß (Rocky Snow Pile), Ersatz: Geländekegel + Lage Eis; **Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen)** (C) – Restwasser hinter den Säulen, Ersatz: MI_EL_Wasserfall_Kaskade.

**Aufwand und Risiko.** Mittel. Risiko: Eiszapfen max. 4 m – mit 3× Skala Rauheit prüfen (Wunsch CryoGen/Arctic Cliffs).

## 2 · Der Frostsee (`frost_02_frostsee`) – Leuchtfeuer · nur mit Steig `froststeig_sued`

**Was man sieht.** Der Frostsee ist ganz zugefroren, aber nicht weiß: Wind hat den Schnee abgefegt, und man blickt durch schwarzes, klares Eis. Quer über den See läuft ein Rücken aus hochkant gestellten, blau leuchtenden Schollen – Presseis, 3–5 m hoch, wo die Eisdecke zusammengeschoben wurde. In der Westbucht stehen im Schwarzeis weiße Blasen übereinander wie eingefrorene Perlenschnüre.

**Vorbild.** Real: Presseisrücken des Baikalsees, Methanblasen im Abraham Lake (Alberta). Spiel: die Eisseen in Horizon Zero Dawn (Frozen Wilds) und The Long Dark (Mystery Lake).

**Standort.** Feld E2, X 200 / Y −2260, Boden 19,7 m. Ebene; Boden Eis 56 %, Schnee 41 %, Trockengras 3 %; Hang 0° (max 38°), Exposition 0°, TPI25 −0,1 m, TPI100 1,3 m, Relief 13 m im Radius. Weg 690 m (Punkt −470/−2424), **mit Steig 108 m** (`froststeig_sued`); Wasser 8 m, Meer 184 m, Stadtrand 779 m (EXP_003); 185 m innerhalb des Bioms; 42 Baumzellen im Radius (max 26 m); Einzugsfläche max 133688 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 6 m: 51 von 159 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,32, lesbar bis 762 m; bester Punkt −210/−2402 in 434 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: Der blaue Zackenkamm auf der dunklen Fläche ist vom Froststeig (434–762 m) lesbar. Held-Blick vom Nordufer (Kamera 226 m) über das Schwarzeis: Blasen im Vordergrund, Presseisrücken diagonal als Blickachse, Raureif-Kuppe dahinter. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 44 m (X 181 / Y −2220), `_held` 216 m (X 150 / Y −2470), `_nah` 10 m (X 198 / Y −2270), `_fern` 434 m (X −210 / Y −2402). **Zugang (kandidaten.erreichbarkeit, 4 m):** 117 m vom Steig (Luftlinie 111 m), max 24,0°, Mittel 6,9°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Presseisrücken aus 25–40 Eisplatten (Wunsch Megascans Ice Cliff/Arctic Cliffs Eisplatten; Ersatz flache Eisschalen aus `SM_EISZAPFEN_8/9` nebeneinander, Material `M_EL_Eis4`). Begleiter (6–8): größere Schollen, schief. Schutt (150–200): Eissplitter um den Rücken. Kleinzeug: Blasen als Decal unter der Eisfläche (Material-Wunsch Schwarzeis mit Blasen-Parallax). Bewuchs: Schilfhalme eingefroren am Ufer (`SM_rough_horsetail_*` mit Raureif). Kontaktzone: Ufereis mit Schneewehen, Risse als Decal.

**Wasser, Effekte, Licht.** Vorhandener Frostsee (S_K13_FROSTSEE_00, eis true) bleibt; Eisdecke als Lage Eis + `see` farbe `schwarz_spiegel` mit Eismaterial. Kein Nebel; klare Luft – die Wirkung kommt aus Spiegelung und Blau.

**Geländeänderung.** Keine (See ist da); Ufer 0,5 m angleichen. Alte Houdini-Reste am Nordufer (K13_FROSTSEE) werden ausgeblendet – nichts davon nutzen.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_rough_horsetail_01`, `SM_rough_horsetail_02`, `SM_rough_horsetail_03`; Material: `M_EL_Eis4`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Presseisplatten (Ice Cliff zerschnitten), Ersatz: SM_EISZAPFEN_8/9 flach + Material M_EL_Eis4; **Arctic Cliffs** (B) – Eisplatten, Treibeis-Blueprint, Ersatz: wie oben; **Free City & Nature Sounds** (C) – Eisknacken, Wind, Ersatz: kein Klang.

**Aufwand und Risiko.** Hoch (Eisplatten und Blasenmaterial). Risiko: Schwarzeis-Material ist neu (Materialwunsch).

## 3 · Der Eisvorhang (`frost_03_eisvorhang`) – Fundstück · nur mit Steig `froststeig`

**Was man sieht.** Unter dem Nordufer des Frostsees tritt Sickerwasser aus einer überhängenden Felsbank. Es ist zu einem 40 m langen Vorhang gefroren: Hunderte Zapfen nebeneinander, oben fingerdick, unten zu Orgelpfeifen verwachsen, dahinter eine flache, blau dämmernde Nische.

**Vorbild.** Real: Eisvorhänge an der Apostle Islands Sea Caves (Lake Superior), Eiszapfenwände am Ouray Ice Park. Spiel: Eishöhlen in Skyrim und God of War (Midgard im Fimbulwinter).

**Standort.** Feld E2, X 300 / Y −2460, Boden 29,8 m. Offener Hang; Boden Schnee 97 %, Eis 2 %, Fels 1 %; Hang 40° (max 58°), Exposition 190°, TPI25 −2,2 m, TPI100 −2,9 m, Relief 29 m im Radius. Weg 771 m (Punkt −470/−2426), **mit Steig 87 m** (`froststeig`); Wasser 90 m, Meer 248 m, Stadtrand 821 m (EXP_003); 249 m innerhalb des Bioms; 5 Baumzellen im Radius (max 28 m); Einzugsfläche max 4812 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 32 von 201 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 550 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Vom Steig aus 87 m entfernt liegt die Felsbank in einer Hangkerbe; der Vorhang ist erst auf dem Uferweg zu sehen. Held-Blick seitlich entlang des Vorhangs. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 107 m (X 221 / Y −2531), `_held` 44 m (X 256 / Y −2460), `_nah` 10 m (X 290 / Y −2460). **Zugang (kandidaten.erreichbarkeit, 4 m):** 140 m vom Steig (Luftlinie 115 m), max 28,5°, Mittel 15,2°, 3 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: Vorhang aus `SM_EISZAPFEN_1…9` (300–500 Instanzen, dicht, Länge nach Unterkante gestaffelt) an einer Felsbank `SM_big_rock_wall_01/03` + `vfmjadufa_tier_2` als Überhang (Netz, Gelände kann nicht überhängen). Begleiter (3–4): Eissäulen bis zum Boden. Schutt (80–120): abgebrochene Zapfen. Kleinzeug: Eiskrümel, Steine. Bewuchs: Moos unter dem Eis sichtbar (grün durch Eis, Lage Moos am Fuß). Kontaktzone: nasser Fels oberhalb (`MI_Leakage_09`).

**Wasser, Effekte, Licht.** Sickerlinie als dünner `bach` (0,3 m) oberhalb, endet `versickert` am Vorhang.

**Geländeänderung.** Felsbank +2 m betonen, Fuß −1 m (Nische). Fenster 60 × 40 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_1`, `SM_EISZAPFEN_2`, `SM_EISZAPFEN_3`, `SM_EISZAPFEN_4`, `SM_EISZAPFEN_5`, `SM_EISZAPFEN_6`, `SM_EISZAPFEN_7`, `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_big_rock_wall_01`, `SM_big_rock_wall_03`, `vfmjadufa_tier_2`; Decals: `MI_Leakage_09`. Wunsch: **CryoGen: Native Procedural Ice Architecture** (B) – dichter Zapfenvorhang, Ersatz: SM_EISZAPFEN_1…9 (300–500 Instanzen); **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (C) – Eisglasur am Fels, Ersatz: Material M_EL_Eis4.

**Aufwand und Risiko.** Mittel. Abgrenzung zu tundra_03 „Die Eiswand“: dort (vermutlich) freigelegtes Bodeneis; hier gefrorenes Sickerwasser an Fels.

## 4 · Der Raureifhain (`frost_04_raureifhain`) – Leuchtfeuer · nur mit Steig `froststeig`

**Was man sieht.** Auf einer Hangschulter über dem Frostsee stehen dreißig Kiefern, die keine Bäume mehr zu sein scheinen: dicke Panzer aus Raureif und Schnee haben sie in weiße, gebeugte Gestalten verwandelt – Schneegespenster, die alle nach Osten schauen, weil der Wind von Westen kommt.

**Vorbild.** Real: Juhyo (Schneemonster) am Zao in Japan, Raureifwälder Lapplands (Riisitunturi). Spiel: die verschneiten Wälder in Red Dead Redemption 2 (Colter) und Skyrim (Dämmerstern).

**Standort.** Feld F2, X 330 / Y −2680, Boden 139,4 m. Oberhang/Plateaukante; Boden Schnee 80 %, Geroell 15 %, Fels 3 %, Eis 1 %; Hang 56° (max 58°), Exposition 166°, TPI25 −0,8 m, TPI100 16,4 m, Relief 105 m im Radius. Weg 839 m (Punkt −470/−2426), **mit Steig 88 m** (`froststeig`); Wasser 142 m, Meer 380 m, Stadtrand 843 m (EXP_003); 220 m innerhalb des Bioms; 170 Baumzellen im Radius (max 29 m); Einzugsfläche max 1224 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 16 m: 55 von 150 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,34, lesbar bis 777 m; bester Punkt −120/−2446 in 507 m mit Anteil 1,00; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: die weiße Gruppe hebt sich auf der Felsschulter gegen den dunklen Hang ab, vom Froststeig 434–777 m lesbar. Held-Blick von Osten durch die Gestalten auf den See. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 113 m (X 299 / Y −2571), `_held` 67 m (X 393 / Y −2703), `_nah` 10 m (X 339 / Y −2683), `_fern` 507 m (X −120 / Y −2446). **Zugang (kandidaten.erreichbarkeit, 4 m):** 229 m vom Steig (Luftlinie 113 m), max 26,5°, Mittel 19,0°, 9 m steiler als 25°, 58 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: 25–35 Kiefern `SM_Forest_pine_06/07`, `SM_dwarf_pine_big_01/02` mit Raureif-Material (M_EL_Pflanze, Farbe weiß-bläulich) und Schneekappen-Netzen (Wunsch Megascans Snow Embankment klein; Ersatz Lage Schnee + Material). Begleiter: 3 tote, ganz eingepackte Stämme `SM_Forest_pine_10_dead`. Schutt (60–100): abgebrochene Äste `SM_Pine_broken_branch_01/02` im Schnee. Kleinzeug: Eisnadeln. Bewuchs nach Ursache: Windflüchter – Kronen nach Osten gekämmt (Rotation), Westseite dicker Panzer. Kontaktzone: Schneewehen hinter jedem Baum (Lage Schnee, Geländewelle +0,5 m).

**Wasser, Effekte, Licht.** keins; feines Glitzern optional (Niagara Schneefall leicht, Wunsch).

**Geländeänderung.** Schneewehen-Muster ±0,5 m (Stempel klein). Lagen: Schnee 255.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_Forest_pine_06`, `SM_Forest_pine_07`, `SM_dwarf_pine_big_01`, `SM_dwarf_pine_big_02`, `SM_Forest_pine_10_dead`, `SM_Pine_broken_branch_01`, `SM_Pine_broken_branch_02`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (B) – Schneekappen/Wehen (Snow Embankment klein), Ersatz: Lage Schnee + Raureif-Material; **Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam** (B) – Glitzernder Schneefall, Eisnebel, Ersatz: ohne Effekt.

**Aufwand und Risiko.** Mittel. Risiko: Material entscheidet – ohne Raureif-Material nur verschneite Kiefern.

## 5 · Der Blockgletscher (`frost_05_blockgletscher`) – Fundstück · nur mit Steig `froststeig`

**Was man sieht.** Am Osthang zieht eine graue Zunge aus Blöcken wie ein Lavastrom ins Tal – aber sie ist kalt: ein Blockgletscher, unter dessen Schutt ein Eiskern steckt. Die Stirn ist 6 m hoch und steil, an ihrer Basis tritt eiskaltes Wasser aus und hat einen kleinen, schwarz zugefrorenen Blasensee aufgestaut.

**Vorbild.** Real: Blockgletscher im Engadin (Murtèl), Sulzkar (Steiermark), Alaska Range. Spiel: die Geröllhalden in Witcher 3 (Skellige) – hier mit Eiskern und Wulsten.

**Standort.** Feld F2, X 520 / Y −2800, Boden 69,2 m. Offener Hang; Boden Schnee 47 %, Geroell 34 %, Eis 9 %, Trockengras 8 %; Hang 34° (max 46°), Exposition 351°, TPI25 −0,4 m, TPI100 2,9 m, Relief 94 m im Radius. Weg 1058 m (Punkt −472/−2432), **mit Steig 250 m** (`froststeig`); Wasser 123 m, Meer 200 m, Stadtrand 1048 m (EXP_003); 100 m innerhalb des Bioms; 52 Baumzellen im Radius (max 33 m); Einzugsfläche max 5060 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 4 von 119 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 531 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: Blockzunge liegt hinter einer Hangrippe, vom Steig aus nur aus 4 Punkten zu sehen. Held-Blick an der Stirn: Wulste von oben nach unten, See vorne. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 44 m (X 564 / Y −2798), `_held` 25 m (X 542 / Y −2812), `_nah` 10 m (X 529 / Y −2805). **Zugang (kandidaten.erreichbarkeit, 4 m):** 411 m vom Steig (Luftlinie 262 m), max 24,9°, Mittel 8,2°, 0 m steiler als 25°, 5 m Querhang > 38° → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Stirn als Geländestufe + 20–30 Blöcke `SM_NordicBoulder_01`, `SM_TundraMossyBoulder_01`, `SM_MassiveTundraRockFormation_02`. Begleiter: Fließwulste (3–4 bogenförmige Rücken). Schutt (180–200): Blockfeld `SM_TundraRockyGround_01`, `SM_mountain_rock_big_01_*`, `SM_mountain_rock_big_02_*`, `xf3odif_tier_0`. Kleinzeug: `SM_SmallStonesPack_*` nur an der Stirnbasis (feines Material rieselt). Bewuchs: Flechten auf alten Blöcken (Material Auflage grau-grün), nichts auf der aktiven Stirn. Kontaktzone: Eis in Lücken der Stirn sichtbar (`SM_EISZAPFEN_1/5` liegend, Material Eis4).

**Wasser, Effekte, Licht.** Blasensee `see` ~18 m, farbe `schwarz_spiegel`, mit Eismaterial (Blasen wie Frostsee).

**Geländeänderung.** Stempel 160 × 110 m: Wulste +1…+2 m, Stirn +4 m steil (Netze tragen die Steilheit).

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_NordicBoulder_01`, `SM_TundraMossyBoulder_01`, `SM_MassiveTundraRockFormation_02`, `SM_TundraRockyGround_01`, `SM_mountain_rock_big_01_1`, `SM_mountain_rock_big_01_2`, `SM_mountain_rock_big_01_3`, `SM_mountain_rock_big_01_4`, `SM_mountain_rock_big_01_5`, `SM_mountain_rock_big_02_1`, `SM_mountain_rock_big_02_2`, `SM_mountain_rock_big_02_3`, `SM_mountain_rock_big_02_4`, `SM_mountain_rock_big_02_5`, `SM_mountain_rock_big_02_6`, `SM_mountain_rock_big_02_7`, `SM_mountain_rock_big_02_8`, `xf3odif_tier_0`, `SM_SmallStonesPack_01`, `SM_SmallStonesPack_02`, `SM_SmallStonesPack_03`, `SM_SmallStonesPack_04`, `SM_SmallStonesPack_05`, `SM_SmallStonesPack_06`, `SM_SmallStonesPack_07`, `SM_SmallStonesPack_08`, `SM_SmallStonesPack_09`, `SM_SmallStonesPack_10`, `SM_SmallStonesPack_11`, `SM_SmallStonesPack_12`, `SM_SmallStonesPack_13`, `SM_SmallStonesPack_14`, `SM_EISZAPFEN_1`, `SM_EISZAPFEN_5`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (C) – Eis in den Stirnlücken, Ersatz: SM_EISZAPFEN_1/5 liegend.

**Aufwand und Risiko.** Mittel. Abgrenzung zu heide „Blockstrom“ (Steinstrom ohne Eis, flach) und bergwald „Felsenmeer“ (bemoost unter Wald).

## 6 · Die Eisküste (`frost_06_eiskueste`) – Leuchtfeuer · nur mit Steig `froststeig`

**Was man sieht.** An der Ostküste friert die Brandung an: ein Eisfuß aus geschichtetem Spritzeis säumt den Strand, und darauf stehen Eisvulkane – Kegel bis 4 m, aus deren Spitze bei jeder Welle eine Fontäne aus Wasser und Eisbrei schießt. Felsen im Wasser tragen Eiskappen wie Zuckerhüte.

**Vorbild.** Real: Eisvulkane am Michigansee (Grand Haven), Eisfuß an der Küste Spitzbergens. Spiel: die vereisten Küsten in God of War (2018) und Skyrim (Meer der Geister).

**Standort.** Feld F2, X 630 / Y −2520, Boden 9,2 m. Offener Hang; Boden Schnee 100 %; Hang 9° (max 29°), Exposition 117°, TPI25 0,7 m, TPI100 1,2 m, Relief 23 m im Radius. Weg 1104 m (Punkt −470/−2426), **mit Steig 94 m** (`froststeig`); Wasser 290 m, Meer 43 m, Stadtrand 1143 m (EXP_003); 43 m innerhalb des Bioms; 252 Baumzellen im Radius (max 33 m); Einzugsfläche max 19452 m². **Sicht (Leuchtfeuer, sicht.py):** Silhouette 8 m: 6 von 91 Wegpunkten im Ring 300–800 m (Wege + Steige) sehen ≥ 30 %, Mittel 0,05, lesbar bis 788 m; bester Punkt −152/−2424 in 788 m mit Anteil 0,99; von bestehenden Wegen allein: 0 Punkte.

**Komposition und Anmarsch.** Leuchtfeuer: die weißen Kegel mit Fontäne über dem dunklen Meer – vom Froststeig 6 Punkte bis 788 m; ein kleines, aber klares Signal am Ende des Steigs. Held-Blick vom Hang (100 m) über Eisfuß und Kegel aufs Meer. Kameras (alle Hoch −170, Ziel ZZ = Boden + halbe Silhouette): `_anmarsch` 74 m (X 569 / Y −2479), `_held` 101 m (X 531 / Y −2538), `_nah` 10 m (X 620 / Y −2522), `_fern` 788 m (X −152 / Y −2424). **Zugang (kandidaten.erreichbarkeit, 4 m):** 100 m vom Steig (Luftlinie 93 m), max 10,9°, Mittel 3,0°, 0 m steiler als 25°, 0 m Querhang > 38° → frei begehbar.

**Detail-Ebenen.** Held: 3–4 Eiskegel (Geländekegel + Eisnetze, Wunsch Megascans Rocky Snow Pile/Ice Cliff; Ersatz Lage Eis + `SM_EISZAPFEN_8/9` als Kraterrand). Begleiter (5–8): eisgekappte Felsen `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01` (Material Auflage weiß). Schutt (100–200): Eisschollen am Strand. Kleinzeug: Eiskrümel, Kies `SM_BeachSandWithPebbles_01/02`. Bewuchs: keiner. Kontaktzone: Eisfuß mit Schichtkante, Nassband (`MI_Leakage_11`).

**Wasser, Effekte, Licht.** Meer vorhanden; Fontänen als Niagara (Wunsch, optional), sonst nur Gischt-Decal. Nebel: Seerauch über dem Wasser (`lokaler_nebel` 0,05).

**Geländeänderung.** Eisfuß +1 m Band, Kegel +2…+4 m. Fenster 120 × 80 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_8`, `SM_EISZAPFEN_9`, `SM_NordicBeachRocks_01`, `SM_NordicBoulder_01`, `SM_BeachSandWithPebbles_01`, `SM_BeachSandWithPebbles_02`; Decals: `MI_Leakage_11`. Wunsch: **Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile** (A) – Eiskegel und Eiskappen (Rocky Snow Pile, Ice Cliff), Ersatz: Lage Eis + SM_EISZAPFEN_8/9; **Niagara Examples Pack** (B) – Fontänen der Eisvulkane, Gischt, Ersatz: Decal statt Bewegung; **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (B) – Nassband-Decals, Spülsaum, Ersatz: MI_Leakage_11; **Free City & Nature Sounds** (C) – Brandung, Ersatz: kein Klang.

**Aufwand und Risiko.** Mittel–hoch (ohne Niagara fehlt die Bewegung). Abgrenzung zu kueste (Felstor, Pfeiler, Blasloch aus Fels).

## 7 · Die Frostblumen (`frost_07_frostblumen`) – Fundstück · nur mit Steig `froststeig_sued`

**Was man sieht.** Wo der Abfluss des Frostsees ins Meer mündet, liegt eine flache Lagune mit hauchdünnem, jungem Eis. Darauf wachsen Frostblumen: Tausende fingergroße Eiskristalle, wie Federn oder Farne, die in der Sonne glitzern – ein Feld, das bei jedem Schritt knistert.

**Vorbild.** Real: Frostblumen auf jungem Meereis (Arktis), auf Seen in Schweden. Spiel: kaum gesehen – genau deshalb ein Fundstück.

**Standort.** Feld F2, X 450 / Y −2270, Boden 2,6 m. Ebene; Boden Schnee 100 %, Trockengras 0 %; Hang 3° (max 22°), Exposition 99°, TPI25 0,2 m, TPI100 0,3 m, Relief 7 m im Radius. Weg 933 m (Punkt −470/−2424), **mit Steig 191 m** (`froststeig_sued`); Wasser 6 m, Meer 40 m, Stadtrand 1011 m (EXP_003); 40 m innerhalb des Bioms; 65 Baumzellen im Radius (max 31 m); Einzugsfläche max 450400 m². **Verdeckung (Fundstück, sicht.py, 3 m):** vom Wegenetz verdeckt = ja (0 Wegpunkte ≤ 400 m, max. Anteil 0,00); vom künftigen Steig aus: 43 von 118 Steig-/Wegpunkten ≤ 800 m sehen mehr als 15 % (weiteste 790 m) – Rahmen (Fels, Wall, Bäume) in Phase 2 setzen.

**Komposition und Anmarsch.** Fundstück: liegt tief hinter einem Uferwall; vom Weg nicht zu sehen. Vom Südsteig aus ist die Fläche als heller Fleck erkennbar, die Kristalle aber erst aus 5–10 m. Held-Blick flach über die Kristalle gegen die Sonne. Kameras (alle Hoch −170, Ziel ZZ = Boden + 1–1,5 m): `_anmarsch` 189 m (X 301 / Y −2153), `_held` 120 m (X 332 / Y −2249), `_nah` 10 m (X 440 / Y −2268). **Zugang (kandidaten.erreichbarkeit, 4 m):** 200 m vom Steig (Luftlinie 189 m), max 6,0°, Mittel 1,4°, 0 m steiler als 25°, 0 m Querhang > 38°, 6 m Furt → **Pfad nötig** (in `pfad_cm`): Erde/Kies-Band 1,2 m, Trittsteine `SM_flat_rock_04`, steile Stücke als Felsstufen `SM_ground_rock_03_03`.

**Detail-Ebenen.** Held: Kristallfeld als Instanzen (Wunsch CryoGen oder eigene kleine Kristallnetze; Ersatz `SM_EISZAPFEN_1/5` sehr klein, 0,05–0,1×, Tausende). Begleiter: 3–4 flache Felsen `SM_NordicBeachRockyGround_02`. Schutt: Treibholz `SM_beach_driftwood_01` eingefroren. Kleinzeug: Eiskrümel. Bewuchs: Strandgras am Wall `SM_beach_grass_01_1/2` mit Raureif. Kontaktzone: Rand der Lagune mit Spülsaum aus Eis.

**Wasser, Effekte, Licht.** Lagune `see` ~40 × 30 m, farbe `schwarz_spiegel`, Tiefe 0,5 m, mit Eismaterial (dünn).

**Geländeänderung.** Uferwall +1 m, Lagune −0,5 m. Fenster 100 × 80 m.

**Assets.** Bestand (alle in `netze.csv`, keins gesperrt): `SM_EISZAPFEN_1`, `SM_EISZAPFEN_5`, `SM_NordicBeachRockyGround_02`, `SM_beach_driftwood_01`, `SM_beach_grass_01_1`, `SM_beach_grass_01_2`. Wunsch: **CryoGen: Native Procedural Ice Architecture** (B) – kleine Eiskristalle (Frostblumen), Ersatz: SM_EISZAPFEN_1/5 0,05–0,1x; **Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen)** (C) – Treibholz/Spülsaum, Ersatz: SM_beach_driftwood_01.

**Aufwand und Risiko.** Mittel. Risiko: Instanzenzahl (Kristalle) – Budget 8 000 kleine Instanzen. Ersetzt die frühere Idee „Aufeis“, das jetzt die Tundra hat (tundra_06).

## 8 · Der Glockenbach (`frost_08_glockenbach`) – Fundstück · nur mit Steig `froststeig_sued`

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

## Steige (Vorschlag, Ferat entscheidet)

- **`froststeig`** – Start: Strassenende oestlich des Frostlagers (X -520, Y -2434); 1290 m, Höhe 11–134 m, max 25,0°, Mittel 10,3°, 0 m steiler als 25° (Kehren/Felsstufen). Polylinie in `standorte_steige.json` → `steige`. Bodenlage Kies/Erde als 1,2-m-Band, Trittsteine; keine Bauten.
- **`froststeig_sued`** – Start: Abzweig vom Froststeig bei X 0, Y -2530; 708 m, Höhe 4–71 m, max 24,2°, Mittel 8,1°, 0 m steiler als 25° (Kehren/Felsstufen). Polylinie in `standorte_steige.json` → `steige`. Bodenlage Kies/Erde als 1,2-m-Band, Trittsteine; keine Bauten.

Gerechnet mit eigener Dijkstra-Suche (4-m-Raster, 16 Nachbarn, Kante ≤ 25°, nur wo nicht möglich 30/35°), Ortskreise 88 m gesperrt, damit kein Ort näher als 80 m am Steig liegt.

## Einmaligkeit (Abgrenzung)

- Pingo, Aufeis, Steinringe, Wabenmoor: Tundra. Eisvorhang ≠ „Die Eiswand“ (tundra_03); Blockgletscher ≠ Blockstrom (Heide) ≠ Felsenmeer (Bergwald). Eisfall/Glockenbach sind gefrorenes Fließwasser, das die anderen Biome nicht haben; Frostsee/Frostblumen gefrorenes Stillwasser; Eisküste gefrorene Brandung (Küste hat Felstor/Pfeiler/Blasloch aus Fels).
- Aus Katalog v1: Eisvorhang und Blasenbucht (jetzt Teil des Frostsees) übernommen.

## Bildwünsche (leere Standorte, Kamera aus der jeweiligen standorte*.json)

- `frost_02_frostsee_held` – Frostsee mit Houdini-Resten am Nordufer – was muss weg?
- `frost_04_raureifhain_fern` – Hangschulter vom Steig aus

## Offene Fragen an Ferat

- Baust du den **Froststeig** (1,3 km + 0,7 km, flach)? Er ist der Schlüssel für alle 8 Frost-Orte.
- Die Houdini-Reste am Frostsee-Nordufer (`SM_K13_FROSTSEE__*`) werden ausgeblendet?

<!-- abgleich-13b13c -->

## Abgleich mit Inventar 13b und Entscheidungen 13c (Stand 11.10.2026)

Neues Inventar: `netze.csv` mit 1 692 Netzen, `inventar_extra.json` mit 73 Niagara-Systemen, 15 Effekt-Blueprints und 46 Klang-Cues. Maschinenlesbar steht alles in `asset_bedarf.json` → `abgleich_13b_13c`. Der Abschnitt ergänzt die Ortsbeschreibungen oben; wo er abweicht, gilt er.

### Entscheidungen aus 13c

- **Nature Water FX gekauft** (frost_01_der_eisfall): Ferat hat Nature Water FX gekauft; der Import steht aus. Die echten Systemnamen folgen mit dem nächsten Inventar, bis dahin gilt der Ersatz (lokaler_nebel bzw. NS_Smoke_Plume als Gischt-Vorlage). Realistic Waterfall VFX und Waterfall Pro sind damit gestrichen.
- **Steige** (alle 8 Orte): Froststeig und Südast überführt ein anderer Agent als `pfade` nach `standorte.json` (Schema in `skripte/sehens_lib/README.md`). Den Stand trägt der Koordinator nach.
- **Eis/Schnee im Bestand** (frost_01–_06): Presseis, Eiskegel und Schneekappen jetzt mit Megascans Ice Cliff/Rocky Snow Pile/Snow Embankment statt Eiszapfen-Bündeln. Eiszapfen `SM_EISZAPFEN_*` bleiben für Vorhang und Glocken.

### Neu im Bestand – je Ort

| Ort | Asset | Pfad | Maße (m) | Einsatz |
|---|---|---|---|---|
| frost_01_der_eisfall | `vctiegmfa_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_vctiegmfa/Raw/vctiegmfa_tier_0/StaticMeshes/vctiegmfa_tier_0` | 2,51 × 1,95 × 6,42 | Eissäule (Ice Cliff, 6,4 m hoch, ×1,5–3) |
| frost_01_der_eisfall | `uhprdg2fa_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_uhprdg2fa/Raw/uhprdg2fa_tier_0/StaticMeshes/uhprdg2fa_tier_0` | 6,71 × 1,66 × 6,15 | Eisfall-Fläche |
| frost_01_der_eisfall | `xfroec0qx_tier_0` | `/Game/Fab/Megascans/3D/Rocky_Snow_Pile_xfroec0qx/Raw/xfroec0qx_tier_0/StaticMeshes/xfroec0qx_tier_0` | 4,7 × 3,83 × 2,17 | Eiskegel am Fuß (Rocky Snow Pile) |
| frost_02_frostsee | `uhpocesfa_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_uhpocesfa/Raw/uhpocesfa_tier_0/StaticMeshes/uhpocesfa_tier_0` | 6,89 × 1,79 × 4,46 | Presseisplatten, schräg, 60–80 % versenkt |
| frost_02_frostsee | `vd5leh0ga_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_vd5leh0ga/Raw/vd5leh0ga_tier_0/StaticMeshes/vd5leh0ga_tier_0` | 8,02 × 2,06 × 2,09 | Presseisrücken (8 m lang) |
| frost_02_frostsee | `veipbcmcb_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_veipbcmcb/Raw/veipbcmcb_tier_0/StaticMeshes/veipbcmcb_tier_0` | 6,82 × 2,7 × 5,25 | Presseisplatte |
| frost_02_frostsee | `vd4hbizcb_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_vd4hbizcb/Raw/vd4hbizcb_tier_0/StaticMeshes/vd4hbizcb_tier_0` | 3,83 × 0,55 × 1,59 | kleine Scholle |
| frost_02_frostsee | `CUE_Ice_Walking_on_ice_I_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Ice_Walking_on_ice_I_Cue` | – | Eisknacken – nur falls ohne Schrittgeräusch (prüfen) |
| frost_03_eisvorhang | `uhprdg2fa_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_uhprdg2fa/Raw/uhprdg2fa_tier_0/StaticMeshes/uhprdg2fa_tier_0` | 6,71 × 1,66 × 6,15 | Eisglasur hinter den Zapfen |
| frost_04_raureifhain | `vcwjeh2fa_tier_0` | `/Game/Fab/Megascans/3D/Snow_Embankment_vcwjeh2fa/Raw/vcwjeh2fa_tier_0/StaticMeshes/vcwjeh2fa_tier_0` | 1,68 × 1,04 × 0,28 | kleine Schneewehe (1,7 m) |
| frost_04_raureifhain | `xemmbh2qx_tier_0` | `/Game/Fab/Megascans/3D/Snow_Pile_xemmbh2qx/Raw/xemmbh2qx_tier_0/StaticMeshes/xemmbh2qx_tier_0` | 1,3 × 0,88 × 0,49 | Schneehaufen |
| frost_04_raureifhain | `xftjadtab_tier_0` | `/Game/Fab/Megascans/3D/Snow_Pile_xftjadtab/Raw/xftjadtab_tier_0/StaticMeshes/xftjadtab_tier_0` | 1,78 × 1,52 × 0,47 | Schneehaufen |
| frost_04_raureifhain | `uhwifglfa_tier_0` | `/Game/Fab/Megascans/3D/Snow_Embankment_uhwifglfa/Raw/uhwifglfa_tier_0/StaticMeshes/uhwifglfa_tier_0` | 6,01 × 1,77 × 0,92 | Schneewehe lang |
| frost_04_raureifhain | `NS_Sparkling` (Niagara) | `/Game/FreeParticle_SoftTofu/Niagara/NS_Sparkling` | – | feines Glitzern – Kopie, weiß, sehr klein (optional) |
| frost_05_blockgletscher | `vcykbjsva_tier_0` | `/Game/Fab/Megascans/3D/Snowy_Rocks_Pile_vcykbjsva/Raw/vcykbjsva_tier_0/StaticMeshes/vcykbjsva_tier_0` | 6,49 × 3,15 × 1,5 | Schnee zwischen Blöcken |
| frost_05_blockgletscher | `xe2obbqqx_tier_0` | `/Game/Fab/Megascans/3D/Snow_Pile_xe2obbqqx/Raw/xe2obbqqx_tier_0/StaticMeshes/xe2obbqqx_tier_0` | 2,08 × 2,07 × 0,52 | Eis/Schnee in Stirnlücken |
| frost_06_eiskueste | `xemjafmqx_tier_0` | `/Game/Fab/Megascans/3D/Rocky_Snow_Pile_xemjafmqx/Raw/xemjafmqx_tier_0/StaticMeshes/xemjafmqx_tier_0` | 8,66 × 7,96 × 2,56 | Eiskegel (Rocky Snow Pile 8,7 m) |
| frost_06_eiskueste | `xfwgbg0qx_tier_0` | `/Game/Fab/Megascans/3D/Rocky_Snow_Pile_xfwgbg0qx/Raw/xfwgbg0qx_tier_0/StaticMeshes/xfwgbg0qx_tier_0` | 7,32 × 4,25 × 1,04 | Eiskappe |
| frost_06_eiskueste | `veipbcmcb_tier_0` | `/Game/Fab/Megascans/3D/Ice_Cliff_veipbcmcb/Raw/veipbcmcb_tier_0/StaticMeshes/veipbcmcb_tier_0` | 6,82 × 2,7 × 5,25 | Eiskante am Ufer |
| frost_08_glockenbach | `vcsibaiga_tier_0` | `/Game/Fab/Megascans/3D/Snow_Embankment_vcsibaiga/Raw/vcsibaiga_tier_0/StaticMeshes/vcsibaiga_tier_0` | 4,62 × 2,79 × 0,54 | Schneekragen am Ufer |
| frost_08_glockenbach | `CUE_Water_Stream_I_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_I_Cue` | – | Bachklang unter dem Eis |

### Paketstatus der Wünsche dieses Bioms

| Paket | Status | Orte |
|---|---|---|
| Arctic Cliffs | fehlt (Download-Liste) | 02 |
| Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen) | läuft bei Ferat | 06, 07 |
| CryoGen: Native Procedural Ice Architecture | fehlt (Download-Liste) | 01, 03, 07, 08 |
| Free City & Nature Sounds | im Projekt (/Game/City_Nature_Sounds, nur Naturklänge nutzen) | 02, 06, 08 |
| Megascans Eis/Schnee: Ice Cliff, Snow Embankment, Huge Snow Hill, Rocky Snow Pile | im Projekt (31 Netze in netze.csv, /Game/Fab/Megascans/3D) | 01, 02, 03, 04, 05, 06 |
| Mountain – Environment Set (Fluss-/Wasserfall-Material neu hinzufügen) | läuft bei Ferat | 01 |
| Niagara Examples Pack | im Projekt (/Game/NiagaraExamples) | 06 |
| Niagara VFX Pack — Snow, Sakura Petals, Autumn Leaves & Steam | fehlt (Download-Liste) | 04 |

### Fehlt weiterhin

- Raureif-/Schneebäume: kein Paket gefunden (Websuche 11.10.: nur die Szene „Windy Winter Forest“, nicht empfohlen) → `MI_EL_SW_Raureif` auf `SM_Forest_pine_06/07` bleibt.
- Fontänen der Eisvulkane (frost_06), Schneefall (frost_04): kein System im Bestand.
- Eisglocken/Frostblumen: CryoGen (B) oder Eiszapfen verkleinert.

### Material-Instanzen (3 von höchstens 6)

| Name | Basis | Parameter | für |
|---|---|---|---|
| `MI_EL_SW_Raureif` | `M_EL_Pflanze` | `Farbe` [0,86, 0,91, 0,97, 1], `Helligkeit` 1,45, `Wind_Staerke` 0,05 | `SM_Forest_pine_06`, `SM_Forest_pine_07`, `SM_dwarf_pine_big_01`, `SM_dwarf_pine_small_01`, `SM_rough_horsetail_01`, `SM_wk2oaeyqx_VarB` |
| `MI_EL_SW_Schwarzeis` | `M_EL_Eis4` | `Eis_Farbe` [0,06, 0,12, 0,2, 1], `Eis_Tief_Farbe` [0,01, 0,02, 0,05, 1], `Schnee_Menge` 0,05, `Eis_Spekular` 0,8 | Frostsee-Blasenbucht, Blasensee am Blockgletscher, Frostblumen-Lagune |
| `MI_EL_SW_Spritzeis` | `M_EL_Eis4` | `Eis_Farbe` [0,7, 0,85, 0,97, 1], `Schnee_Menge` 0,45, `Eis_Rau_Max` 0,3 | `SM_EISZAPFEN_1`, `SM_EISZAPFEN_4`, `SM_EISZAPFEN_9`, Eisvorhang, Eisglocken, Eisvulkane |
