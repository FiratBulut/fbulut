# Küste – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1)

Stand 11.10.2026 · Agent B8 · Dateien: `standorte.json` (8 Orte + 2 Pfade unter `"pfade"`, Schema aus 13c; jeder Ort trägt `pfad_id`),
je Ort `<id>.png` (Draufsicht, geplante Elemente, Pfade orange, Zugang gelb, Kameras), `asset_bedarf.json`. Alle Zahlen aus den 2-m-Daten
(`vorlagen/daten/sehens`) mit `antworten/skripte/sehens_lib` (Cache, Sichtlinien Gelände + `baumhoehe_4m`, Wegpunkte 20 m). Eigene Skripte
im Scratchpad `a13/b8_kueste_sumpf/` (`s4_kueste.py` Küstenlinie/Inseln, `pfad.py` + `s15/s16_pfade*.py` Pfadsuche, `pfadwelt.py`
Welt mit Pfaden als Weg, `s17_kueste_eval.py`, `s19/s20_*scan.py`, `build.py`). Kameras nach §8 (11.10. 13:00): `_anmarsch` und `_nah`
mit **Hoch −170** und echtem Ziel, `_held`/`_fern` Hoch 170 mit `zz_augenhoehe`.

## Das Biom in den Daten

- **0,73 km² in zwei Teilen:** West (A5/B5, X −4268 … −3500, Y 0 … 1000; 0,46 km²) – die Westflanke eines **660 m hohen Kammes**, der
  in **25–75 m hohen Kliffen** ins Meer bricht (Kliffhöhe 25 m landeinwärts: Median 49 m, 90 % 66 m); Hang Median 29°, 90 % 58°.
  Davor fünf **Felsinselchen**, die im Höhenfeld schon als Pfeiler stehen (144–624 m², 17–48 m hoch) und eine 2,3-ha-Insel (45 m).
  Zehn Bäche erreichen die Kliffkante 40–67 m über dem Meer und stürzen fast senkrecht hinab. Ost (H2, X 2570 … 3328, Y −2702 … −2250;
  0,27 km²) – die Nordkappe eines **bewaldeten Kaps** (Gipfel 245 m), Ufer meist 20–30° steil, im Nordosten ein schmaler Strand,
  im Osten eine Bucht mit 50 m hohen, 41–63° steilen Flanken.
- Boden (Stichprobe): Fels 30 %, Gras 29 %, Wiese 21 %, Nadeln 14 %, Laub 5 %; Süßwasser 1,4 %, Meer im Rechteck 0,1 % (Grenze = Küste).
- **Wege: keine.** Nächster Weg 543 m (Ost) bzw. 564 m (West) vom Biom; mit der 150-m-Zone 414 m. Fläche 80–300 m vom Weg: **0 m²**
  (auch ≤ 400 m: 0). Die Westflanke ist von der Wegseite (Osten) nur über den Kamm (bis 683 m, Osthang > 38°) oder um den
  **Meeresarm** (X −3100, Y 700–1750, 16–40 m breit, 3–4,7 m tief) herum erreichbar. Deshalb – wie bei Lava und Fjord – **zwei neue Pfade**
  (Ferats Linie aus 13c: „lieber ein Pfad mehr als ein Ort weniger“), siehe unten.
- Heute (Bilder `KLIPPE2_A5_fern`, `KLIPPE2_A5_k2_nah`, `BIOM3_B5_rundgang`): grasige Steilflanke über einem Band aus hellen
  Klippen-Kacheln, ein einzelner Pfeiler im Wasser, weiße Fremdkörper-Brocken im Hang, kein Spülsaum, kein Tang, keine Gischt, keine
  Vögel – das Meer stößt „sauber“ an den Fels. Zielbild `witcher_04` (Klippenblick, Dunst, Staffelung) und `witcher_06` (Wand + Wasser).
- **Leitidee:** Die Küste ist ein Ort, an dem **das Meer arbeitet** – es frisst Pfeiler aus dem Kliff (Die Alten), bohrt Tore (Nadeltor),
  bläst durch Gänge (Blasloch), hobelt Bänke (Gezeitenbank), schlägt Kreide ab (Kreidewand), türmt Sand (Dünenkamm); Vögel kalken die
  Insel, Bäche verlieren sich im freien Fall (Seefall). Jeder Ort hat **Salz, Gischt und eine Spritzzone** als gemeinsame Handschrift.

## Pfade (Vorschlag, Ferat entscheidet) – in `standorte.json` → `pfade`

| ID | Art | Länge | Höhe | max / Mittel | > 22° | Anschluss | für |
|---|---|---|---|---|---|---|---|
| `kueste_pfad_klippensteig` | serpentine, 1,5 m | 4 346 m | 19–156 m | 33,4° / 10,6° | 114 m | Weg am Südrand von Zalas verborgener Stadt (X −2507, Y 541), außerhalb des Stadtkreises ROMAN_LOC_009 | kueste_01–05 |
| `kueste_pfad_kap` | trampelpfad, 1,5 m | 1 925 m | 0–100 m | 27,3° / 8,5° | 50 m | Wegkehre südl. der Bucht (X 2453, Y −1741, H2) | kueste_06–08 |

- **Klippensteig** (Abschnitte, Dijkstra auf 4 m, Kante ≤ 22°, Querhang ≤ 40°, Ortskreise 88 m gesperrt, damit kein Ort < 80 m am Pfad liegt):
  1. Zugang 1 780 m: Weg südlich der Stadt (Stadtkreise beim Suchen gesperrt) → Westen über die Hochfläche nördlich des Meeresarms, **um den Kopf des Meeresarms herum** (Y ≈ 730) und am
     Westufer hinab in die Strandebene (A6, X −3480 / Y 1250); 34 m steiler als 22° (max 31,8°) – zwei kurze Kehrenstücke am Westufer.
     Variante mit Kiesnehrung über den Meeresarm (Stempel +1,5 m auf 18 m × 20 m im Meer) wäre 1 193 m bis zum Westufer – **nicht
     empfohlen** (Geländeänderung im Meer, kaum kürzer).
  2. Ebene + Aufstieg 790 m: am Südrand der Ebene entlang, bei X −3670 auf die Kliffterrasse (Y 1040 → 875, max 21,6°).
  3. Kliffweg 1 776 m: auf der Terrasse 50–150 m über dem Meer nach Norden bis zum **Aussichtsende über dem Nadeltor** (X −3900 / Y 150);
     zwei Steilstücke (Y 640 → 452: 51 m, Y 230 → 150: 29 m; max 33°) als Kehren mit Felsstufen.
  Bodenlage Erde/Kies 1,5 m, Felsstufen `SM_flat_rock_04` / `Basalt_Basalt_Rock_B_SM`; keine Brücke, kein Geländer.
- **Kap-Pfad:** Wegkehre → Südufer der Bucht → Westflanke des Kaps (X 2715, 20–60 m über dem Meer) → über die Nordwestschulter
  (Y −2510, zwei Kehrenstücke 22 + 28 m bis 27°) → Nordseite (Y −2530, ~65 m hoch) → Ende über dem Nordoststrand (X 3120 / Y −2520).
- Punkte in cm (`punkte_cm`, vereinfacht, Toleranz 2 m) plus Höhen (`z_cm`, Zusatzfeld). Der Geländeanschnitt kommt aus Ferats
  Serpentinen-Werkzeug (13c).

## Prüfung

- `sehens_pruefen.py` (Stand 11.10. abends, rastert `pfade` aller Biome als Wege): für die Küste **0 FEHLER, 0 WARNUNG**; HINWEISE:
  „_anmarsch 94/112 m vom Weg“ (Kamera am Zugang), Klippensteig quert Süßwasser auf ~114 m, Kap-Pfad 64 von 91 Segmenten > 15 % und
  quert Süßwasser auf ~74 m → Kehren und Trittsteine wie unten. Ohne Pfade wären es 8 FEHLER „Abstand zum Weg 654–1383 m“.
  Keine Abstandskonflikte mit anderen Biomen (nächster fremder Ort 790 m: `elfenwald_08_wurzelbruecke`). Eigene Gegenprobe mit nur
  diesen zwei Pfaden (`pfadwelt.py`): ebenfalls 0 FEHLER.
- Abstände untereinander ≥ 235 m (Dünenkamm – Blasloch 235 m, Alten – Gezeitenbank 310 m, Vogelinsel – Nadeltor 329 m; Regel kleine
  Biome 200 m); zu Fremdorten ≥ 790 m. Mitten höchstens 43 m außerhalb des Bioms (Gezeitenbank, Regel ≤ 150 m).
- 4 Leuchtfeuer / 4 Fundstücke (Richtwert 3/5): die Westküste hat drei Meeresformen, die man nur aus der Ferne sieht – Fundstücke
  braucht die Regel „vom Weg verdeckt“, und an einem Kliffpfad ist jeder Strandpunkt von oben einsehbar. Gescannt: **kein einziger**
  Uferpunkt 85–290 m vom Pfad ist verdeckt (`s19_scan.py`); verdeckt sind nur Orte unter einer Kliffkante oder hinter einer Schulter
  (Seefall, Gezeitenbank, Dünenkamm, Blasloch). Darum 4/4 statt 3/5.

## Übersicht

| Nr | ID | Name | Art | Feld | X / Y (m) | Boden z | Radius | Pfad | Nachweis (sicht.py, Wege + Pfade) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `kueste_01_die_alten` | Die Alten | Leuchtfeuer | A5 | −4010 / 872 | 47,8 m (Pfeilerkopf) | 150 m | Klippensteig 298 m | 40 m: **97 / 131** Punkte (300–800 m) ≥ 30 %, Mittel 0,73, bis 726 m; bester 501 m, 1,0 |
| 2 | `kueste_02_die_vogelinsel` | Die Vogelinsel | Leuchtfeuer | A5 | −4180 / 419 | 33,6 m | 110 m | Klippensteig 231 m | 30 m: **53 / 76**, Mittel 0,68, bis 769 m; bester 484 m, 1,0 |
| 3 | `kueste_03_das_nadeltor` | Das Nadeltor | Leuchtfeuer | A5 | −4100 / 100 | 45,6 m | 90 m | Klippensteig 165 m | 40 m: **4 / 58**, bis 755 m; bester 460 m, 0,98 (vom Kliffweg Y 450–520) |
| 4 | `kueste_04_der_seefall` | Der Seefall | Fundstück | A5 | −3844 / 578 | 35,6 m (Lippe 57 m) | 50 m | Klippensteig 92 m | verdeckt: 0,00 an 88 Punkten ≤ 400 m, 0 / 150 ≤ 800 m; 3×3 5/9 |
| 5 | `kueste_05_die_gezeitenbank` | Die Gezeitenbank | Fundstück | A6 | −3750 / 1040 | 4,6 m | 45 m | Klippensteig 105 m | verdeckt: 0,00 an 61 Punkten; 0 / 173 ≤ 800 m; 3×3 9/9 |
| 6 | `kueste_06_die_kreidewand` | Die Kreidewand | Leuchtfeuer | H2 | 2590 / −2380 | 5,5 m (Fuß) | 90 m | Kap-Pfad 110 m | 25 m: **29 / 79**, bis 743 m; bester 646 m (Bucht-Südufer); auch vom **heutigen** Weg 8 / 24 |
| 7 | `kueste_07_der_duenenkamm` | Der Dünenkamm | Fundstück | H2 | 3300 / −2590 | 2,9 m | 60 m | Kap-Pfad 191 m | verdeckt: 0,00 an 12 Punkten; 0 / 68 ≤ 800 m; 3×3 9/9 |
| 8 | `kueste_08_das_blasloch` | Das Blasloch | Fundstück | H2 | 3185 / −2385 | 13,2 m | 45 m | Kap-Pfad 148 m | verdeckt: 0,00 an 19 Punkten; 0 / 84 ≤ 800 m; 3×3 9/9 |

Gegenüber Katalog v1 übernommen und verortet: **Die Alten**, **Blasloch**, **Seefall**, **Vogelfelsen** (jetzt als Insel), **Felstor**
(jetzt **Nadeltor** auf einem echten 46-m-Pfeiler). Ersetzt: **Grotte** (der Fjord hat `fjord_07_brandungsgrotte`; Tausch nicht nötig –
die Küste plant keine Grotte), **Kugelstrand** (kein passendes Asset, Konkretionen wirken als Kugeln künstlich), **Windflüchter** (Heide
hat `heide_08_die_windkante`). Neu: **Gezeitenbank**, **Kreidewand**, **Dünenkamm**. Seegraswiese: als Kleinzeug in der Gezeitenbank
(unter Wasser sonst nicht sichtbar).

**Einmaligkeit (geprüft gegen alle `katalog.md`/`standorte*.json` und Katalog v1):** Die Alten/Nadeltor ≠ Mönch (bergwald, Felsnadel im
Wald) ≠ Steinwald/Mondtor (dschungel, Kalknadeln/Bogen im Wald) – hier **Granitpfeiler und ein Tor im Meer, Brandung am Fuß**.
Seefall ≠ Schleierwand (fjord, 250-m-Wand mit Schmelzfäden) ≠ Klemmblock-Klamm (bergwald) – hier **ein Bach, der 57 m frei ins offene
Meer fällt**. Kreidewand ≠ Schwalbenwand (aue, Lehmprallhang am Fluss) ≠ Bemalte Hügel – hier **weißer Kreideabbruch mit gestürzten
Buchen und Feuerstein am Strand**. Gezeitenbank ≠ alte Ufer (fjord, gehobene Strandterrassen) – hier **lebende Tümpel auf Meeresniveau**.
Dünenkamm ≠ Große Sterndüne (wüste) – **Vordüne mit Strandhafer, Sanddorn, Kartoffelrose**. Blasloch ≠ Geysir/„Der Atem“
(gletscher/tundra) – **Meerwasser, von der Welle durch einen Gang gedrückt**, kein Dampf.

---

## 1 · Die Alten (`kueste_01_die_alten`) – Leuchtfeuer · Klippensteig

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

## 2 · Die Vogelinsel (`kueste_02_die_vogelinsel`) – Leuchtfeuer · Klippensteig

**Was man sieht.** Eine Insel wie ein Schiffsrumpf, 45 m hoch, die Ostwand **weiß gekalkt** von tausenden Brutplätzen (Entscheidung E02: Ostflanke – Guano folgt den Brutsimsen, alle Kameras stehen im Osten), auf jedem Sims ein
weißer Punkt, in der Luft ein langsamer Wirbel aus Vögeln. Oben kurzes, vom Kot überdüngtes Grün, die Ostseite grasig mit krummen
Kiefern. Bei Westwind zieht ein Geruch nach Fisch und Salz bis aufs Kliff.

**Leuchtfeuer.** 30-m-Silhouette: 53 von 76 Punkten (300–800 m) lesbar, bis 769 m; die weiße Wand leuchtet gegen das dunkle Meer.

**Vorbild.** Real: Bass Rock (Schottland), Vogelinsel Runde (Norwegen), Látrabjarg. Spiel: Vogelfelsen von Ard Skellig (Witcher 3).

**Standort.** Feld A5, X −4180 / Y 419, Boden 33,6 m: die 2,3-ha-Insel (hmax 45 m), 260 m vor der Küste, Wiese 87 %, 124 Baumzellen auf der
Ostseite (bis 25 m), Flanken bis 77°. 70 m im Biom. Klippensteig 231 m (Aussichtsende X −3900 / Y 452).

**Komposition und Anmarsch.** Man kommt von Süden über den Kliffweg; die Insel steht genau in der Blickachse nach Nordwest, das Licht fällt
von links auf die weiße Wand. Kameras: `_anmarsch` (X −3952 / Y 386, 230 m), `_held` (X −4064 / Y 281, 180 m – vom Klippenvorsprung),
`_nah` auf der Insel (10 m), `_fern` vom Kliffweg (X −3744 / Y 630, 484 m). **Zugang:** keiner (Insel); Aussicht am Pfadende.

**Detail-Ebenen.** Held: Ostwand (E02) aus `vfmjadufa_tier_2` + `vdssailfa_tier_2` (je 2, ×1,4) vor die Inselflanke gesetzt, mit
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

## 3 · Das Nadeltor (`kueste_03_das_nadeltor`) – Leuchtfeuer · Klippensteig (Ende)

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

## 4 · Der Seefall (`kueste_04_der_seefall`) – Fundstück · Klippensteig

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

## 5 · Die Gezeitenbank (`kueste_05_die_gezeitenbank`) – Fundstück · Klippensteig

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

## 6 · Die Kreidewand (`kueste_06_die_kreidewand`) – Leuchtfeuer · Kap-Pfad

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

## 7 · Der Dünenkamm (`kueste_07_der_duenenkamm`) – Fundstück · Kap-Pfad

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

## 8 · Das Blasloch (`kueste_08_das_blasloch`) – Fundstück · Kap-Pfad

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

## Bildwünsche (Kameras in `standorte.json`)

- `kueste_04_der_seefall_held` – Kliffkante am Bach heute (gibt es den Wasserstreifen am Kliff schon, wie hoch ist die Wand?)
- `kueste_01_die_alten_fern` – die Inselchen heute (Höhenfeld-Pfeiler, Reste der Houdini-Kachel K9?)
- `kueste_06_die_kreidewand_fern` – Westflanke des Kaps von der Bucht aus

## Offene Fragen an Ferat

1. **Klippensteig (4,35 km) und Kap-Pfad (1,9 km) bauen?** Ohne sie hat die Küste keinen einzigen gültigen Ort (alles 543–1 383 m vom Weg).
   Kürzere Variante: Klippensteig nur bis zum Seefall (2,9 km) – dann fallen Vogelinsel und Nadeltor weg.
2. Darf das Höhenfeld unter dem **Nadeltor** um bis zu 48 m abgesenkt werden (Torgang), oder Bogen außen an den Pfeiler setzen?
3. Bleiben die Klippen-Kacheln der alten Houdini-Steilküste (K9) stehen? Die Planung setzt die neuen Felsen auf das heutige Höhenfeld.
4. Fontäne des Blaslochs: Nature Water FX (ca. 40 €) kaufen oder mit `NS_Smoke_Plume` beginnen?

## Abgleich Inventar 13d (Stand 11.10.2026, abends)

Neues Inventar: 1 965 Netze, 116 Niagara, 85 Decals. Pfade, Maße und Paketstatus stehen in `asset_bedarf.json` → `abgleich_13d`. Orte und Kameras bleiben unverändert; die Phase-2-Planer werden gerade auf die echten Assets umgestellt.

**Jetzt erfüllt:**

- `kueste_01_die_alten` – Coast & Dunes: Seetang-/Seepockenband, Nass-Decals (A): `MI_Decal_Algae`, `MI_Deca_Wet`, `SM_seaweed_01_A`, `SM_seaweed_01_B`
- `kueste_01_die_alten` – Gischt an den Pfeilerfüßen (Ultimate Niagara C): `NS_Impact_Small`, `NS_Wake_Medium`
- `kueste_02_die_vogelinsel` – Coast & Dunes: Nass-/Tangband, Spritzzone (A): `MI_Decal_Algae`, `MI_Deca_Wet`
- `kueste_03_das_nadeltor` – Coast & Dunes: Tangband, Schaum im Durchbruch (A): `MI_Decal_Algae`, `SM_seaweed_01_C`, `NS_Wake_Small`
- `kueste_03_das_nadeltor` – Gischt im Tor (Ultimate Niagara C): `NS_Impact_Medium`
- `kueste_04_der_seefall` – Nature Water FX: Gischt am Aufschlag, Sprühnebel (B): `NS_Waterfall_Large`, `NS_Impact_Large`
- `kueste_04_der_seefall` – Mountain: Fall-/Schaummaterial (A): `M_River_Water_Translucent`
- `kueste_05_die_gezeitenbank` – Coast & Dunes: Seetang, Muscheln, Algen-Decals in den Tümpeln (A): `SM_seaweed_01_A`, `SM_seaweed_01_D`, `SM_seaweed_01_E`, `SM_shells_01_A`, `SM_shells_01_B`, `MI_Decal_Algae`, `MI_Decal_Sand_Wet`
- `kueste_06_die_kreidewand` – Coast & Dunes: Kiesel-Decals, Spülsaum (B): `MI_Decal_Rocks_Small`, `MI_Decal_Rocks_Big`, `MI_Deca_Wet_Flat`
- `kueste_07_der_duenenkamm` – Coast & Dunes: Sand-/Spülsaum-Decals, Seetang im Spülsaum (A): `MI_Decal_Sand_Small_Waves`, `MI_Decal_Sand_Big_Waves`, `MI_Decal_Sand_Dry_2`, `SM_seaweed_01_B`, `SM_shells_01_A`
- `kueste_08_das_blasloch` – Nature Water FX: Fontäne aus dem Loch (A, Geysir-System): `NS_Geyser_Large`, `NS_Impact_Medium`
- `kueste_08_das_blasloch` – Coast & Dunes: Nassband, Tang (A): `MI_Deca_Wet`, `MI_Decal_Algae`

**Ersatz → echtes Asset:**

- `kueste_01, _03, _04, _08`: statt NS_Smoke_Plume weiß/flach als Gischt → `NS_Impact_Small`, `NS_Impact_Medium`, `NS_Impact_Large`
- `kueste_08_das_blasloch`: statt NS_Smoke_Plume weiß + Bewegung als Fontäne → `NS_Geyser_Large`
- `kueste_01–_08`: statt MI_Leakage_10/_* als Tang- und Nassband → `MI_Decal_Algae`, `MI_Deca_Wet`
- `kueste_05_die_gezeitenbank`: statt SM_WaterPlant03 grün getönt unter Wasser → `SM_seaweed_01_A`, `SM_seaweed_01_D`
- `kueste_07_der_duenenkamm`: statt SM_dead_grass_01 als Spülsaum, SM_beach_driftwood_01 → `SM_seaweed_01_B`, `SM_beach_driftwood_02`, `SM_beach_driftwood_04`, `SM_beach_driftwood_08`

**Fehlt weiter:**

- Gebleichte große Treibholzstämme (kueste_07_der_duenenkamm) – Nanite Driftwood Props (A, Held von aue_04) · *nur nach Ferats OK*
- Brandungs-/Seevogelklang (kueste_01–_08) – kein Paket belegt (Wilderness Nature Loops C prüfen) · *nur nach Ferats OK*
