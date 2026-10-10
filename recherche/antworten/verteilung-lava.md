# Verteilung Biomgruppe 8: Lava (Vulkanregion C6, C7, C5, D6, B6, D7, B7)

**Auftrag 11, Teil B8.** Biom `lava`, Foliage-Präfix `FT_EL_LV_`, Ordner `/Game/Eldarien/Welt/Foliage/Lava`. Stand 2026-10-10
(Fortsetzung nach API-Abbruch). Lieferung: dieser Bericht, `skripte/lava_regeln.json` (16 Klassen, 78 Netze in 82 Paletteneinträgen,
alle gegen `daten/netze.csv` geprüft, 0 fehlend), `skripte/lava_plan.py` (Planer nach FORMAT §3/§5, Schichten 0/1/2/5 plus Punktliste
und Overrides für 3/4). **Alles UNGETESTET MIT ECHTDATEN** – in der Cloud `py_compile`-sauber und mit synthetischen Rastern (C6 mit
Schlackenkegel, Lavastrom, See, Weg, Ort, Fremdbiom-Kachel; §4) rauchgetestet. Web-Quellen waren nur als Suchmaschinen-Auszüge lesbar
(kein Direktzugriff auf Verlage/80.lv/Fab); solche Belege sind mit **[Suchauszug]** markiert, Zahlen ohne Beleg mit **Richtwert**.

Betroffene Felder laut `biome_je_feld.md`: C6 (lava 99 %, Lavafels 45, Lavasand 27, Moos 17, Gras 8; 38 % steiler als 30°, Höhe bis
381 m), C7 (lava 61 %, 48 % Land, 59 % steil), C5 (lava 31 %, Rest Aue, 5,8 % Wasser), D6 (lava 26 %, Ödland 61 %), B6 (lava 13 %,
Bergwald 63 %), D7 (lava 13 %), B7 (lava 6 %). Der Planer läuft in jedem Feld auf der Lava-Maske aus `eigner.r8` + `welt.json`
(Rezept „Vulkanregion“ → lava) und einem 100-m-Übergangssaum außerhalb; Kennzahl 0 (Weltgelände) wird über die Lagen `Lavafels` +
`Lavasand` ≥ 96/255 als Lava erkannt, sonst gilt das dominante Feldbiom.

## 1. Referenzanalyse: was ein Lavafeld zwischen Boden und Horizont füllt

**Die Ordnung kommt vom Alter des Stroms, nicht vom Zufall.** Alle vier Referenzlandschaften zeigen dieselbe Abfolge, nur mit
anderen Zeitachsen. Island (Hekla-Chronosequenz, Vilmundardóttir et al. 2018): Lavas jünger als 70 Jahre tragen nur Erstbesiedlung
durch das Wollige Zackenmützenmoos *Racomitrium lanuginosum* und die Flechte *Stereocaulon*, die zu einer geschlossenen Decke
zusammenwächst; 170–700 Jahre alte Ströme sind moosdominiert, und diese Phase ist durch die dicke Moosmatte „arretiert“ – Gefäßpflanzen
kommen erst nach Jahrhunderten **[Suchauszug: journals.sagepub.com/doi/10.1177/0309133318798754, researchgate 328144291]**.
Für die 2021–2023er Ströme am Fagradalsfjall gibt es bisher nur Mikrobiologie (Nature Comms Bio 2025: Besiedlung innerhalb von Stunden,
Stabilisierung nach dem ersten Winter) – sichtbare Vegetation: keine; die Ströme sind tiefschwarz mit rostroten Oxidationsflecken
**[Suchauszug: nature.com/articles/s42003-025-09044-1]**. Eldhraun (Laki 1783, 565 km²) ist nach 240 Jahren vollständig von
*Racomitrium*-Polstern überzogen; Wachstum 1–2 cm je Jahrzehnt, Trittschäden brauchen 30–70 Jahre **[Suchauszug: iceland.org/eldhraun,
amazingiceland.is; Tourismusquellen, nicht peer-reviewed]**. Das ist die Bildwirkung „Moos-Mondlandschaft“: gelbgrüne Polster
0,3–0,7 m über schwarzen Wülsten, keine Sträucher, keine Bäume, nur am Rand Lupinen und Gras.

**Teneriffa** liefert das trockene Gegenstück: Auf den historischen Strömen (Arafo/Fasnia 1705, Garachico 1706, Chinyero 1909) ist die
Oberfläche nur chemisch (Oxidation) und biologisch durch Flechten verwittert; Pflanzen (*Spartocytisus supranubius*-Ginster,
*Erysimum scoparium*) stehen nur auf undatierten, älteren Strömen und dem unteren Garachico-Strom **[Suchauszug: researchgate 286935977,
Feldspektrometrie Teneriffa; en.wikipedia.org/wiki/Teide]**. Übertragen: frische Ströme bleiben über 300 Jahre pflanzenfrei, wenn es
trocken ist; der gelbweiß blühende Ginster (1–2 m, Farbakzent) steht nur im Randgürtel.

**Hawaii** gibt die Formen: Pāhoehoe (glatt, Wülste, Tumuli) und ʻAʻā (scharfkantige Klinker dm–m groß) liegen nebeneinander, Pāhoehoe
überdeckt ʻAʻā teilweise; **Kīpuka** sind von jüngerer Lava umflossene Inseln mit reifer Vegetation, von denen die Wiederbesiedlung
ausgeht; der Farn ʻAe (*Polypodium pellucidum*) und ʻŌhelo-Beeren sind die ersten Besiedler und wachsen aus Rissen und Hohlräumen,
ʻŌhiʻa-Bäume folgen **[Suchauszug: nps.gov/havo/learn/nature/ferns.htm, nps.gov/havo/learn/nature/kipuka.htm, usgs.gov
„Geology/Ecology of Hawaiʻi Volcanoes NP“, smithsonianmag.com]**. Tumuli-Größen fand die Suche nicht; Richtwert aus Fotos 3–10 m
Durchmesser, 1–3 m hoch.

**Ätna** ist das Modell für den Rand- und Übergangsgürtel: *Stereocaulon vesuvianum* besiedelt alle Ströme seit 1910, seine Biomasse
steigt im ersten Jahrhundert steil an und fällt dann, wenn Gefäßpflanzen es beschatten; auf dem 1886er Strom standen bereits die
stickstoffbindenden Ginster *Genista aetnensis* und *Spartium junceum*; Artenreichtum hängt nur lose vom Stromalter, eng aber vom
Deckungsgrad ab **[Suchauszug: researchgate 314281270 „Floristic change during early primary succession on lava, Mount Etna“;
uobrep.openrepository.com/handle/10547/610794]**. Informelle Zeitangaben (Flechten nach 5–10 a, Moose nach 20–30 a) stammen von
Tourismusseiten **[Suchauszug: etnaway.com]** und sind nur Richtwerte. Kiefern: keine Quelle gefunden; die Ätna-Kiefer (*Pinus nigra
laricio*) als Krummholz am Stromrand ist Beobachtung aus Fotos, Richtwert.

**Witcher-Staffelung.** CDPR hat kein Lava-Biom; die Prinzipien kommen aus Skellige (Basaltküste, Moos auf Fels, Färöer/Island als
Referenz, siehe `verteilung-fels-organisch.md`) und aus der Methode: Vegetation pro Region als eigene Bibliothek, Reihenfolge große
Bäume → kleine → Farne → Gras, Pinsel je Geländetyp mit Abstand- und Skalenvariation **[Suchauszug: 80.lv/articles/world-building-of-witcher-3]**;
Felsen, Klippen und Wurzeln sitzen im Gelände statt als gestreute Props darauf **[Suchauszug: pcgamer.com „Why I love: The Witcher 3's
topography“]**. Die Bildkritik (`bildkritik-witcher-messlatte.md`) nennt als Kernmangel „jede Fläche trägt genau einen Maßstab“ und
fordert drei bis vier ineinandergreifende Größenstufen plus Makro-Variation im 100–500-m-Maßstab. Für Lava heißt das: **Spire/Hornito
5–15 m → Blöcke 1–3 m (Teil C) → Schlacke 0,25–0,8 m → Kiesel 0,15–0,45 m → Landschaftsmaterial Lavasand**, dazu Makro-Variation durch
die Alterszonen (schwarz / moosgrün / Pioniergelb / Aschegrau im Übergang) und 300-m-Wertrauschen, Farbakzente Schwefelgelb (Fumarolen),
Gelbgrün (Racomitrium), Rost (oxidierte Schlacke per Material), Blickziele Kegelgipfel, Spire, Dampf am Seeufer. Spuren von Leben im
Lavafeld sind dünn: Steinmänner aus Schlacke an Wegen (Island-Vörður), eine verlassene Schwefelgrube, eine Opferstätte am Kegelfuß.

## 2. Regelwerk (`lava_regeln.json`) – Zonierung und Schichten

### 2.1 Lava-Maske, Alter, Zonen, Kegel

`alter = 0,5·Moos + 0,2·Gras + 0,3·(1 − d_Rand/120 m) + 0,2·(Rauschen₃₀₀ − 0,5) − 0,2·Lavafels·(1 − Moos)`, geklemmt 0–1
(Lagen 0–1 aus `lage_*.r8`, Gauß σ 3 m; `d_Rand` = Abstand zum Nicht-Lava per Dilatation auf 2-m-Stufe, gedeckelt 120 m).
Zonen: **frisch** < 0,28, **alt** 0,28–0,52, **rand** ≥ 0,52 (alles innerhalb der Maske), **uebergang** = außerhalb bis 100 m.
Ohne `lage_Moos/Gras` wird nur Randnähe + Rauschen benutzt (Hinweis im Log). Fällt die Rand-Zone in Echtdaten zu dünn aus (C6 hat nur
17 % Moos), `alter_gewichte.randnaehe` auf 0,45 heben. **Schlackenkegel:** Gipfel = lokales Maximum im 60-m-Fenster mit Prominenz ≥ 8 m
gegen das 120-m-Mittel; Flanken = Prominenz > 5 m und Hang 24–36° (Schüttwinkel loser Schlacke 30–35°, Richtwert) tragen Schlacke 2,2×
und Pflanzen 0,3×. Sperrflächen: Wasser + 1,5 m, Weg 2,5 m (Kleinzeug) / 4 m (Blöcke, Bäume, Akteure), Ort 5 m, vorhandene Ebenen
(`bestand/`, `witcher/`, `ufer/`, `instanzen.json`; Bäume 2 m, Sonstiges 1 m), Fumarolen-Radius pflanzenfrei. Hang: Pflanzen ≤ 38°,
Steine ≤ 62° (FORMAT: > 40° nur Felsen). Höhe: Pflanzen ab 220 m linear abnehmend, 0 ab 360 m.

### 2.2 Schichten und Klassen (Dichten Instanzen je m² auf der Lage; Zonenfaktor frisch / alt / rand / übergang)

| Schicht | Klasse (Gruppe) | Netze | Dichte (Lage) | Zone f/a/r/ü | Gruppe n / r | Maßstab | Eingraben | Sichtweite cm | Koll. | max |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 boden | `schlacke` (Aa-Klinker 0,25–0,8 m) | `SM_lava_s_rock_06/07/08` (0,5–0,8 m) + `_03/_04` klein skaliert | Lavafels 0,012, Lavasand 0,010, Geröll 0,012, Moos 0,003 | 1,4/1,0/0,5/0,25; Hang 24–40° ×1,8; Kegelflanke ×2,2 | 3–8 / 2,2 m | 0,45–0,85, ±15 % nicht-uniform | 30–50 % | 0–15 000 | nein | 9 000 |
| 0 boden | `kiesel` (Lavakiesel-Ersatz) | `SM_SmallStonesPack_08…14`, `SM_stone_05/06/07` ×1,2–2,6 → 0,15–0,45 m | Lavasand 0,045, Lavafels 0,028, Geröll 0,04 | 1,2/0,9/0,6/0,5 | 6–18 / 1,6 m | 1,2–2,6 | 30–50 % | 0–6 000 | nein | 22 000 |
| 0 boden | `asche` (verkohlte Zweige) | `SM_DryBranches_01/04/05/07`, `SM_dead_quiver_branch_01/02_NN` | Lavasand 0,004, Nadeln 0,006, Gras 0,004 | 0/0,6/1,2/1,5 | 1–4 / 2,5 m | 0,9–1,5 | 3 cm | 0–9 000 | nein | 2 500 |
| 1 mittel | `moos` (Racomitrium-Polster) | `SM_MossClump_01/03/05` ×2–4 (→ 0,3–0,7 m), `SM_MossPlane`, `SM_moss_01/02` | Moos 0,05, Lavafels 0,012, Gras 0,01 | 0,08/1,0/1,1/0,4; am Fuß von Schlacke ×1,6 | 5–14 / 2 m | 2,0–4,0 | 4 cm | 0–12 000 | nein | 8 000 |
| 1 mittel | `flechtenstein` (Wulstlava-Ersatz) | `SM_LichenedForestBoulder_01`, `SM_MossyRocks_01/02`, `SM_MossyForestRock_01/03`, `texndcpda_tier_0` | Moos 0,006, Lavafels 0,004 | 0,1/1,0/0,8/0,3 | 1–4 / 2,5 m | 0,7–1,2 | 35–55 % | 0–20 000 | nein | 2 500 |
| 1 mittel | `pionier` (Ginster-Ersatz) | `SM_heath_A/B_01` ×1,1–1,8, `SM_billberry_dry_01`, `SM_forest_heather_01`, `SM_beach_rose_06/07` | Gras 0,008, Moos 0,006, Trockengras 0,006 | 0/0,5/1,2/0,9 | 3–8 / 2,4 m | 1,1–1,8 | 3 cm | 0–15 000 | nein | 2 500 |
| 1 mittel | `kiefer_strauch` (Krüppelkiefer 0,8–2 m) | `SM_pine_beach_short_01/02`, `_crooked_02`, `SM_dwarf_pine_small_01/02`, `_medium_01` | Nadeln 0,0015, Gras 0,0012 | 0/0,25/1,0/1,3 | 1–3 / 3 m | 0,7–1,15 | 6 cm | 0–30 000 | nein | 500 |
| 1 mittel | `verkohlt_liegend` | `SM_OldFallenTree_01/02`, `SM_Forest_pine_04/08/09_log` | Nadeln 0,0006, Lavasand 0,0004 | 0,15/0,6/1,0/1,4 | 1–2 / 4 m | 0,9–1,3 | 20–35 %, Yaw hangab ±35° | 0–45 000 | **ja** | 450 |
| 1 mittel | `verkohlt_stumpf` | `SM_BrokenStump_01`, `SM_RottenTreeStump_02`, `SM_pine_stump_01…03` | Nadeln 0,0006 | 0,2/0,6/1,0/1,3 | 1–3 / 5 m | 0,9–1,4 | 8 cm | 0–25 000 | nein | 400 |
| 1 mittel | `verkohlt_schnag` (stehend 2–3,8 m) | `SM_dead_quiver_trunk_NN` (2 m, 88 Dreiecke) ×1–1,9, `SM_RottenTreeStump_01` | Nadeln 0,0005, Lavasand 0,0004 | 0,3/0,8/1,0/1,0 | 1–4 / 6 m | 1,0–1,9 | 15 cm | 0–30 000 | nein | 400 |
| 1 mittel | `gras` (Horstgras) | Tundra-Gras `SM_wk2oaeyqx_VarB/C/F/G`, `SM_dead_grass_01/03` | Gras 0,012, Trockengras 0,012, Wiese 0,008 | 0/0,4/1,0/1,2 | 3–9 / 2 m | 0,9–1,4 | 3 cm | 0–12 000 | nein | 3 000 |
| 2 baum | `baum_tot` | `SM_DeadTree_01/02` (6–7 m), `SM_EuropeanBeech_Dead_XL_01` (21 m), `Fir_08_Dead_NoBillboard` | Nadeln 0,0005, Gras 0,0003 | 0/0,3/1,0/1,4 | 1–3 / 7 m | 0,9–1,3 | 20 cm | 0 | **ja** | 180 |
| 2 baum | `baum_kiefer` (Krummholz 2,5–5 m) | `SM_pine_beach_crooked_01`, `_small_01/04`, `SM_dwarf_pine_big_01/02` | Nadeln 0,0012, Gras 0,0006 | 0/0,15/1,0/1,2 | 1–4 / 6 m | 0,7–1,1 | 10 cm | 0 | **ja** | 250 |
| 5 wasserkante | `ufer_block` (abgeschreckte Blöcke) | `SM_lava_s_rock_01/02/05/03` (1,1–2,3 m) | 0,02 im Band 0–6 m | 1,0/1,0/0,8/0 | 1–3 / 2 m | 0,8–1,3 | 35–55 % | 0–40 000 | **ja** | 150 |
| 5 wasserkante | `schwarzkies` | `SM_NordicBeachRock_01`, `SM_SmallStonesPack_08/12`, `SM_stone_06` | 0,12 im Band 0–8 m | 1/1/1/0,6 | 5–16 / 1,8 m | 0,8–1,6 | 30–50 % | 0–6 000 | nein | 1 500 |
| 5 wasserkante | `saeule` (Basaltsäulen-Ersatz, **Akteure**) | `SM_lava_wall_05` (1,75 × 1,95 × 3,95 m), `_04` hochkant | 0,0025 im Band 1–10 m, Hang 28–75° | 1/0,8/0,3/0 | 2–5 / 4 m, Yaw = Uferrichtung | 0,9–1,5 | 30–45 % | 0 | **ja** | 40 |

Alle Felsen/Steine werden voll auf die Geländenormale gekippt, Sträucher 35–50 %, Bäume 10–15 %, Yaw zufällig außer `verkohlt_liegend`
(hangab) und `saeule` (Uferrichtung). Pivot: alle `SM_lava_*` haben den Pivot in der Netzmitte (`netze_masse.json`: min_z ≈ −H/2); der
Planer rechnet `z = Boden − min_z·s − Eingraben·H·s`, für Netze ohne Bounds-Eintrag Pivot unten. Budget: Ziel 52 000 je Feld, hart
60 000; Kollision ≤ 3 000 (nur `verkohlt_liegend`, `baum_*`, `ufer_block`, `saeule`); Akteure ≤ 60. Bei Überschreitung werden zuerst
`kiesel`, `schwarzkies`, `asche`, `schlacke` nach Instanz-Hash ausgedünnt, Bäume und Akteure zuletzt. Wichtig für den Setzer: die 29
`Lava_Volcano`-Netze haben **keine Kollisionsprimitive** (Taxonomie); `plan.json` fordert für Blöcke > 0,8 m trotzdem `kollision: true`
und trägt je Netz den Hinweis „Komplex-als-Einfach oder Konvex-Hülle erzeugen“ ein. Material-Hinweise im `plan.json`: `kiesel`,
`schwarzkies`, `asche`, `verkohlt_*`, `baum_tot` brauchen eine dunkle/verkohlte Material-Instanz (Albedo ×0,2–0,35, Rauheit 0,9–0,95),
`moos` eine gelbgrüne statt waldgrüne.

### 2.3 Overrides für Schicht 3 (Teil C, `felsgruppen_plan.py`) und Schicht 4 (Teil D, `spuren_plan.py`)

`plan.json["felsgruppen_overrides"]`: Palette `lava` (Teil C hat sie bereits: `lava_b_rock_01/02`, `lava_m_rock_*`, `lava_s_rock_*`,
`lava_wall_*`, LavaSpire als Hero), Biomfaktor **1,6** statt 1,0 (Blockfelder/ʻAʻā-Klinker), Klassenfaktoren Blockstrom 2,0, Hangfuß 1,6,
Kuppe 1,3, Grat 0,9, Wand 1,0, Prallhang 0,8, **Band 0,3** (Lavaströme haben keine Sedimentbankung; Stromfronten sind Hangfuß/Wand),
Zonenfaktor frisch 1,3 / alt 1,0 / rand 0,7 / übergang 0,4, Eingraben 30–45 %, Kollision ab 0,8 m Höhe (Setzer-Hinweis wie oben).
Platten-Ersatz (Lava hat keine `geroell_platte`): `SM_MossyRocks_01/02`, `SM_TundraRockyGround_01`, `texndcpda_tier_0`. Kiesel-Ersatz:
Teil C streut `SM_stone_03…08` (grau) – bitte dieselbe dunkle Material-Instanz oder Klasse `kiesel` dieses Regelwerks. **Spires als
Akteure:** `SM_IcelandicLavaSpire_01…03` (5,0–5,3 m hoch, `_02` 15 × 7 m, Nanite, 4 Kollisionsprimitive) werden nicht von diesem Planer
gesetzt; er liefert `punkte[typ == spire_vorschlag]` (flache Kuppen im Kern, Hang ≤ 18°, Prominenz ≥ 6 m, Abstand ≥ 150 m, max 6 je Feld,
mit Netz und Yaw) als `hero_akteur_punkte` für Teil C oder für die Hand.

`plan.json["spuren_overrides"]`: aus = Feldstreifen, Obstgarten, Zaun, Mauer, Steg, Holzschlag, Köhler, Friedhof; **Steinmänner** ×1,5
aus `SM_lava_s_rock_06/07/08` entlang der Wege (Abstand 90–140 m); Wegkreuze ×0,5, keine Schreine; Rauchsäulen aus `punkte[typ ==
fumarole]`; Schwefelgrube (Kisten/Fässer/Karren 3–6 im Radius 8 m) an `schwefelgrube_vorschlag`; Opferstätte (Steinkreis 8–12 Schlacken,
r 3 m, `AncientRuins/SM_Column_03`) an `opferstaette_vorschlag`; Blickziele Kegelgipfel, Spire, stärkste Fumarole, Höhleneingang.

### 2.4 Punktliste (`plan.json["punkte"]`, Weltkoordinaten cm)

| typ | Regel | Felder je Punkt |
|---|---|---|
| `fumarole` | 12 je km² frisch, 4 alt, 0,5 rand; Kegelflanke/Prominenz > 8 m ×3; Hang ≤ 40°; Abstand ≥ 45 m; max 24 je Feld; Radius pflanzenfrei | `staerke` 0,4–1,0 (Niagara-Rate), `radius_m` 1,5–5 (Schwefelkruste/Decal), `schwefel` (60 % gelb, Námafjall-Optik), `zone`, `kegelflanke`, z = Boden + 0,3 m |
| `dampf` | Lava (frisch/alt) berührt Wasser: Band 0–3 m, Abstand ≥ 25 m, max 20 | `staerke` 0,3–0,7 (Laze-Dampf) |
| `kegel_gipfel` | lokale Maxima mit Prominenz ≥ 8 m, max 6 | `prominenz_m` (Blickziel) |
| `spire_vorschlag` | s. 2.3 | `netz`, `yaw_grad` |
| `hoehle_vorschlag` | Lavawand 48–75°, ≥ 40 m vom Rand, Abstand ≥ 300 m, max 2 | Hinweis: kein Höhlen-Netz im Inventar |
| `schwefelgrube_vorschlag` | stärkste Fumarole mit Weg ≤ 150 m, max 1 | – |
| `opferstaette_vorschlag` | 25 m hangab vom ersten Spire/Gipfel, max 1 | `anker` |

### 2.5 Planer `lava_plan.py`

Aufruf `python -I scripts/lava/lava_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]`. Fenster Feld + 64 m
per `np.memmap` (NY 7057 × NX 9577, J-Spalte auf 9577 geklippt: 505 m breit), Hang/Normale aus Gauß-geglätteter Höhe (σ 1,5 m),
Prominenz aus Box-Mittel 120 m, Abstände per Dilatation (2-m-Stufe), Gruppen als Zentren + Mitglieder in Scheiben, jede Instanz wird
gegen Dichte, Sperre, Hang und Feldgrenze geprüft. Zufall: 64-bit-Hash aus (Seed 806, Klasse, Weltrasterkoordinate) → Nachbarfelder
erzeugen im Randstreifen dieselben Gruppen, zwei Läufe sind byte-identisch. Nur NumPy (numba wird erkannt, nicht gebraucht). Ausgabe
`export/unreal/welt/lava/<Feld>/<Netz>.f32` (10 float32 LE), `akteur_<Netz>.f32` für `saeule`, `plan.json` mit `stand, feld, ebene,
instanzen, instanzen_kollision, dateien{pfad, anzahl, gruppe, rolle, schicht, sichtweite, schatten, kollision, hinweis}, entfernen,
ft_ordner, ft_praefix, punkte, zonen, lava_anteil, felsgruppen_overrides, spuren_overrides, hinweise`; `--bild` →
`docs/pruefung/lava/<Feld>.png` (Hintergrund = Zone: frisch schwarz, alt oliv, rand grün, übergang beige; Wasser blau, Weg braun, Ort
rot; Instanzen in Klassenfarbe; Kreuze = Punkte). Fehlende optionale Dateien (Lagen, Karten, eigner/welt.json, Ebenen, netze_masse)
erzeugen je einen Hinweis in Log und `plan.json["hinweise"]`; fehlende `hoehe.f32`/`netze.csv`/Regeldatei → klare Meldung, Exit.

## 3. Abgrenzung zu vorhandenen Ebenen und zu Teil C/D

- **`FT_EL_WIT_*` (Witcher-Bewuchs):** `entfernen = FT_EL_WIT_lava_s_rock_06,…_07,…_08` – nur die drei kleinen, gleichmäßig
  gestreuten Lava-Steine werden durch die geclusterte Klasse `schlacke` ersetzt (gleiche Netze, Gruppen 3–8, Flanken-Bonus).
  `FT_EL_WIT_lava_s_rock_01–05` und `lava_m_rock_01/04` bleiben, bis Teil C in den Lava-Feldern abgenommen ist; dann dort `entfernen`
  erweitern. Witcher-Kleinzeug (Laub, Zweige) läuft in Lava ohnehin nicht (Biom-Eignung 0).
- **`FT_EL_BST_*` (Wald-Bestand):** kein Baum-Bestand in Lava; im Übergangssaum (B6 Bergwald, C5 Aue) hält der Planer 2 m Abstand zu
  Bestand-Bäumen und setzt nur Totbäume/Krüppelkiefern zusätzlich (Lava hat den Waldrand getötet).
- **`FT_EL_FS_lava_wall_01/02/09` (Felsschalen):** bleiben als Wandsilhouette; die `saeule`-Akteure nutzen `lava_wall_04/05` nur in
  Uferbändern (1–10 m vom Wasser, Hang ≥ 28°), keine Doppelung mit Steilwänden > 55°.
- **`FT_EL_UF_*` (Ufer):** die Ufer-Ebene läuft an allen Ufern; die Wasserkanten-Klassen hier gelten nur **innerhalb** der Lava-Maske
  (Zonenfaktor übergang 0) und ergänzen schwarze Blöcke/Kies; `ufer/foliage_<Feld>` wird als belegt gelesen (1 m Abstand).
- **Teil C (`felsgruppen_plan.py`):** setzt Schicht 3 (Hero, Blöcke, Blockströme, Hangfuß) mit den Overrides aus 2.3. Dieser Planer
  streut nichts über 0,8 m außer `ufer_block`/`saeule`; die Klasse `flechtenstein` (0,35–1,2 m, tief eingegraben) liegt bewusst in
  Schicht 1 als Wulstlava-Optik, nicht als Felsgruppe.
- **Teil D (`mittelschicht_plan.py`):** hat für lava nur Trockengras/Totholz (0,001–0,006/m²). Empfehlung: in den Lava-Feldern
  `mittelschicht` für Biom lava auf Faktor 0 stellen, da `gras`, `pionier`, `verkohlt_*` hier dichter und zoniert gesetzt werden;
  im Übergang (Aue/Bergwald-Zellen) bleibt Teil D zuständig. `spuren_plan.py` nutzt die Overrides aus 2.3.
- **Wüste (C3–E5):** keine Überschneidung (D5/E5 haben keine Lava).

## 4. Testanleitung

**Rauchtest Cloud (gelaufen, Python 3.13, NumPy 2.5, Pillow 12, ohne numba).** Mini-Produktionswurzel mit `hoehe.f32` in voller Größe
(memmap; nur C6-Fenster beschrieben: Grundfläche 30 m + 3 %-Gefälle, Schlackenkegel r 320 m / +230 m mit 60-m-Krater, Lavastrom 120 m breit
/ 12 m hoch nach Südost, See r 55 m am Kegelfuß 3 m eingetieft, Weg schräg durch den Kegel, Ort 40 × 50 m), `karte_wasser/weg/ort.r8`,
`eigner.r8` (Vulkanregion Kennzahl 7 unregelmäßig r 360–480 m; Nordhälfte außen Kennzahl 3 = aue, Südhälfte 0 = Weltgelände) +
`welt.json`, `lage_Lavafels/Lavasand/Moos/Gras.r8` (Summe 255, Moosrampe 200–400 m vom Kegel), `bestand/C6` (300 Kiefern),
`daten/netze.csv` + `netze_masse.json`. Ergebnis `lava_plan.py C6 --bild`: **42 169 Instanzen (587 mit Kollision), 76 Netzdateien,
23 Punkte, 3,8–4,7 s** je Feld (inkl. Bild). Zonen im Feld: frisch 37,1 %, alt 16,5 %, rand 3,5 %, übergang 27,7 %, sonst 15,2 %
(Lava-Anteil 57 %); Schichten boden 26 265 / mittel 15 447 / baum 355 / wasserkante 102. Klassen: kiesel 15 268, schlacke 9 059 → 8 996
(max), moos 8 034 → 7 998, gras 4 307 → 2 984 (max 3 000), pionier 2 290, asche 1 918, flechtenstein 1 195, kiefer_strauch 517 → 497,
baum_kiefer 233, verkohlt_liegend 209, verkohlt_stumpf 187, verkohlt_schnag 149, baum_tot 122, schwarzkies 158, ufer_block 29,
saeule 0 (bei `--faktor 3`: 8 Akteure in `akteur_SM_lava_wall_04/05.f32`, Kollision/Hinweis gesetzt). Punkte: 6 Fumarolen (2 mit
Schwefel), 9 Dampf am Seeufer, 2 Kegelgipfel (Kraterrand 17,7 m, Stromende 9,1 m), 3 Spire-Vorschläge, 1 Höhle, 1 Schwefelgrube
(Fumarole am Weg), 1 Opferstätte. Prüfskript: alle f32 durch 10 teilbar, Anzahl = `plan.json`, Quaternionen normiert, Maßstäbe > 0,
alle Instanzen im Feld, **0 Instanzen** auf Wasser/Weg/Ort, z − Gelände zwischen −0,22 m (Flechtensteine 35–55 % eingegraben) und
−0,03 m, maximaler geglätteter Hang je Rolle: Pflanzen ≤ 38°, Steine ≤ 56°, Blöcke ≤ 59°; zwei Läufe byte-identisch (MD5 aller f32);
`--faktor 0.5` → 21 750 Instanzen. Randfeld J7 (505 m breit, keine Lava): 0 Instanzen, 0,7 s, kein Fehler; C7 ohne Lava im Synthetik:
927 Instanzen aus dem Übergangssaum des C6-Kegels (Nahtfenster wirkt). Fehlende `hoehe.f32` → „Pflichtdatei fehlt“, Exit. Prüfbild
`docs/pruefung/lava/C6.png`: schwarzer Kern mit Kiesel-/Schlacke-Clustern, oliver Moosring, grüner Randsaum, beiger Übergang mit
Totholz/Gras, See mit Dampfkreuzen, Weg und Ort frei. Die Rand-Zone ist im Synthetik dünn (3,5 %), weil die Moosrampe nur bis 0,73
reicht – in Echtdaten prüfen (§6).

**Erwartete Instanzzahlen je Feld (Rechnung aus Flächenanteilen und Dichten, Spanne ±35 %, nach Budget):**

| Feld | Lava-Fläche km² | gesamt | boden | mittel | baum | wasserkante | Kollision | Fumarolen |
|---|---|---|---|---|---|---|---|---|
| C6 (lava 99 %, 38 % steil) | 1,0 | 32 000–48 000 | 20 000–30 000 | 8 000–16 000 | 80–300 | 0 (kein Wasser) | 300–800 | 8–24 |
| C7 (lava 61 %, 48 % Land, 59 % steil) | 0,3 | 12 000–26 000 | 8 000–18 000 | 3 000–7 000 | 50–200 | 0 | 150–500 | 3–12 |
| C5 (lava 31 % + Saum, Wasser 5,8 %) | 0,31 | 8 000–18 000 | 4 000–10 000 | 3 000–7 000 | 100–300 | 200–1 200 | 300–900 | 1–6 |
| D6 (lava 26 %, Wasser 3,7 %) | 0,25 | 6 000–14 000 | 3 000–8 000 | 2 000–5 000 | 60–200 | 100–800 | 200–600 | 1–5 |
| B6, D7 (lava 13 %) | 0,08–0,13 | 3 000–8 000 | 1 500–4 500 | 1 000–3 000 | 40–150 | 0–300 | 100–400 | 0–3 |
| B7 (lava 6 %, 28 % Land) | 0,02 | 800–3 000 | 400–1 500 | 300–1 200 | 10–60 | 0 | 20–120 | 0–1 |

**Prüfkameras (Weltkoordinaten cm; Feldmitte = Spalte·1008 + 504, Zeile analog):**
1. **C6 Lavafeld, Augenhöhe 1,7 m** bei X −221 050, Y 148 350 (Feldmitte, Lavafels-Fläche; wenn dort Kegelflanke, 150 m hangab), Blick
   quer zur Hangrichtung ins tiefe Seitenlicht. Erfolg: innerhalb 10 m drei Größenstufen (Kiesel 0,15–0,45 m in Nestern von 6–18,
   Schlackenbrocken 0,25–0,8 m in Gruppen 3–8 mit sichtbar eingegrabener Unterkante, dahinter Teil-C-Blöcke 1–3 m); kein Stein schwebt,
   keine Pflanze im frischen Kern außer vereinzelten verkohlten Stümpfen; mindestens eine Fumarole in Sichtweite (gelbe Kruste, Rauch);
   Kleinzeug cullt bei 60 m (Kiesel) bzw. 150 m (Schlacke) ohne sichtbares Aufploppen gegen den dunklen Boden.
2. **C7 Hang, 10 m über Grund** bei X −221 050, Y 249 150 (Mitte der 59-%-Steilzone), Blick hangauf 20° nach oben. Erfolg: Schlacke
   verdichtet sich auf den 24–40°-Flanken (×1,8), Pflanzen enden bei 38°, oberhalb nur Felsen (Teil C) und Schlacke; Flechtensteine und
   Moospolster sitzen in Mulden und am Fuß von Blöcken (×1,6), nicht gleichmäßig; Hangfuß zeigt Übergang Schlacke → Lavasand mit
   Horstgras.
3. **C5 Übergang Lava → Aue, 2 m Höhe** bei X −221 050, Y 47 550 ± 300 m auf der Lava-Grenze (Prüfbild: Grenze oliv/beige), Blick
   entlang der Grenze. Erfolg: innerhalb 100 m außerhalb der Lava ein Aschestaub-Saum mit verkohlten Stämmen hangab, Stümpfen, 1–3
   Totbäumen und Krüppelkiefern in 1–4er-Gruppen, Horstgras in Rissen; innerhalb der Lava ein grüner Randgürtel (Heide/Strandrose als
   Pionier, Moos) – kein harter Materialwechsel ohne Objekte; Aue-Ebene (`FT_EL_AU_*`) und Lava-Ebene überlappen nur im Saum.
4. **D6/C5 Seeufer in der Lava, 3 m Höhe**, Blick über das Wasser. Erfolg: schwarzer Kiessaum 0–8 m, abgeschreckte Blöcke halb im Wasser,
   an steilen Ufern 2–5 hochkant stehende `lava_wall_05` in Uferrichtung, Dampfpunkte an der Wasserlinie (Niagara); nichts im Wasser.
5. **Draufsicht 400 m über C6** (Prüfbild und Editor). Erfolg: drei Farbzonen als Makro-Variation (schwarz, moosgrün, Pioniergelb),
   Zonengrenzen unregelmäßig (300-m-Rauschen), Kegelgipfel mit Fumarolen-Kranz, Spire als Blickziel auf einer Kuppe, Weg und Ort frei.
6. **Nahtprüfung C6/C7 und C6/B6** (Draufsicht 100 m): Gruppen laufen über die Feldgrenze, keine Dichtesprünge.

Erfolgskriterien in Zahlen: Instanzen und Kollision je Feld innerhalb der Tabelle; Setzer legt ≤ 78 Foliage-Typen `FT_EL_LV_*` an
(davon 6 Baum-/Stamm-/Blocktypen mit Kollision) plus ≤ 60 Akteure; Laufzeit Planer ≤ 10 s je Feld; PNG und `plan.json` je Feld.

## 5. Einkaufsliste (Fab/Megascans, frei bevorzugt; Namen sind Fab-Suchbegriffe, da Fab nicht direkt lesbar war)

| Asset (Fab-/Megascans-Name) | Stufe | Wofür | Heutiger Ersatz |
|---|---|---|---|
| Megascans „Pahoehoe Lava“ / „Ropy Lava Rock“ / „Lava Flow Surface“ (Platten 1–3 m, flach, Wulststruktur) | High 4K, Nanite | Klasse `flechtenstein` → echte Wulstlava in alt/frisch; Teil-C-`platte_ersatz` | bemooste Waldsteine tief eingegraben |
| Megascans „Volcanic Rock“ / „Scoria“ / „Lava Rock Small“ (Schlackenbrocken 0,2–0,6 m, 4–6 Varianten, rot-schwarz) | High 2K | `schlacke` (heute 3 Netze, 3 Skalierungen) – mehr Varianz, rostrote Oxidationsvarianten | `SM_lava_s_rock_06–08` skaliert |
| Megascans „Lava Pebbles“ / „Volcanic Gravel“ / „Black Beach Pebbles“ (Kleinsteine 5–30 cm als Pack) | High 2K | `kiesel`, `schwarzkies`, Teil-C-Kieselsaum | graue SmallStonesPack + dunkle Material-Instanz |
| Megascans „Moss Clump“ / „Icelandic Moss“ / „Mossy Ground Patch“ (Racomitrium-Polster 0,3–0,8 m, gelbgrün) | High 2K, Nanite | `moos` (heute 0,1–0,18-m-Docks-Moos ×2–4 skaliert → Texturdichte zu grob) | MossClump/MossPlane |
| Megascans „Burnt Tree Trunk“ / „Charred Log“ / „Burnt Stump“ (verkohlte Stämme 3–8 m, Stümpfe) | High 4K | `verkohlt_liegend/stumpf/schnag`, Teil-D-Totbaum-Solitär | Mossy-Totholz + schwarze Material-Instanz |
| Megascans „Basalt Columns“ / „Columnar Basalt“ / „Hexagonal Basalt Cliff“ (Säulenreihen 3–8 m) | High 4K, Nanite | `saeule` an Lava-Ufern und Stromfronten (Reynisfjara-Optik); Teil-C-Klasse wand in lava | `lava_wall_05` hochkant |
| Decals „Sulfur Crust“ / „Yellow Mineral Deposit“ / „Fumarole Ground“ (2–5 m) + Niagara-Rauch | 2K | Fumarolen-Punkte (`radius_m`, `schwefel`), Schwefelgrube | – (nur Punktliste) |
| Megascans „Broom Shrub“ / „Genista“ / „Retama“ (Ginster 1–2 m, gelb blühend) | High 2K | `pionier` Farbakzent am Rand (Ätna/Teide) | Heide ×1,1–1,8, Strandrose |
| Megascans „Lava Tube Entrance“ / „Cave Entrance Rock“ (8–15 m) | High 4K | `hoehle_vorschlag` | kein Netz |

Vor dem Kauf: Megascans-Assets, die vor 31.12.2024 beansprucht wurden, sind frei (`boden-kleinzeug-gras.md`); nach Import Post-Import-Pass
nach `klippennetze-a5.md` (Nanite, Convex-Kollision 4–16 Hulls, Texturen auf 4K/2K klemmen). Wird eingekauft, nur die Pfade in
`lava_regeln.json` tauschen, der Planer bleibt gleich.

## 6. Offene Punkte und Annahmen

1. **Ungetestet mit Echtdaten.** Zonenschwellen (0,28 / 0,52) und Alter-Gewichte sind auf synthetische Lagen abgestimmt; in C6 (Moos 17 %)
   kann die Rand-Zone zu dünn werden → `randnaehe` 0,45 oder `alt_bis` 0,45. Kegelerkennung (Prominenz ≥ 8 m gegen 120-m-Mittel) kann
   in C6 (381 m Höhe, 38 % steil) Felsgrate als Kegel lesen; dann `prominenz_min_m` 12 und Flanken-Hangfenster prüfen.
2. **`welt.json`-Schema** nur aus FORMAT bekannt: `kacheln` als Dict oder Liste mit `kennzahl`/`id` + `rezept`; Zuordnung über die
   Wörter „lava“/„vulkan“ im Rezepttext, alles andere = anderes Biom, Kennzahl 0 = Lage-Erkennung (Schwelle 96/255, Glättung 6 m).
3. **Lagen `Lavafels`/`Lavasand`** werden als dominante Lagen in der Lava angenommen; sind sie in Echtdaten mit `Fels`/`Geroell` gemischt,
   `lagen`-Liste und Dichten je Lage erweitern (Geröll ist bereits mit Schlacke/Kiesel-Dichte belegt).
4. **Material-Instanzen** (dunkle Kiesel/Zweige, verkohltes Holz, gelbgrünes Moos) sind Setzer-Arbeit; ohne sie stehen graue Steine
   und braunes Totholz auf schwarzem Grund. Hinweise stehen je Netz in `plan.json["dateien"][…]["hinweis"]`.
5. **Kollision der Lava-Netze**: keine Primitive im Inventar; `kollision: true` für `ufer_block`, `saeule` und Teil-C-Blöcke erfordert
   Komplex-als-Einfach oder Konvex-Hüllen (bei ≤ 200 Stück je Feld vertretbar; `klippennetze-a5.md`).
6. **Nicht-Nanite-Netze** in der Palette: Coast_Dunes-/Mountain-Kiefern (`kiefer_strauch`, `baum_kiefer`), `Fir_08_Dead`, Meadow
   `dead_grass` – Sichtweiten gesetzt (300 m bzw. 0 für Bäume), LOD im Editor prüfen; Hinweis im `plan.json`.
7. **Spires** werden nur vorgeschlagen (Punkte), nicht gesetzt; Teil C muss `hero_akteur_punkte` lesen oder der Setzer setzt sie von Hand.
   `SM_IcelandicLavaSpire_02` ist 15 × 7 × 5 m (liegende Formation) – Yaw aus dem Punkt, Eingraben 25 % Richtwert.
8. **Doppelungen mit Teil D** (`mittelschicht` lava-Dichten) und mit `FT_EL_WIT_lava_s_rock_01–05`: bewusst belassen bis zur Abnahme;
   danach `entfernen` erweitern bzw. Teil-D-Faktor in lava auf 0.
9. **Fumarolen-Dichte** (12/km² frisch) ist Richtwert aus Námafjall/Sólfatara-Fotos; Niagara-Kosten bei 24 Säulen je Feld prüfen
   (Sichtweite 2–3 km, Rauch träge 3–8 m hoch, Dampf am Wasser kürzer).
10. **Zeitplan Setzer:** 76–78 Foliage-Typen je Feld sind viele; wenn der generische Setzer je Typ > 3 s braucht, Palette per
    `netz_gewichte` 0 auf ~50 Netze kürzen (Kiesel 10 → 6, Moos 6 → 4).
