# Antwort 21 – Detailgrad Landschaft: Felsdeckung statt Textur

Stand 13./14.10.2026. Grundlage: Auftrag 21 (`ba23bb1`), Ferats Dichte-Zensus 16h-N6h (`0bf16f1`, `auftraege/daten/dichte/`),
Fab-Bibliothek 13.10., Inventar 13d. Vorarbeiten, auf denen das aufbaut: `verteilung-fels-organisch.md` + `skripte/felsgruppen_plan.py`
(Schichtfunktion, Gruppengrammatik, Runde-5-Dichtegrenze, Netzform-Regel), `klippennetze-a5.md` (ISM statt Akteure, Post-Import-Pass),
`boden-kleinzeug-gras.md` (Runtime-GPU-PCG für Kleinzeug), `sehens_lib` (Inventar, Platzierung, Lagen, A15-Stempel).

**Lieferung**

| Was | Wo |
|---|---|
| Regeln (alle Zahlen) | `skripte/felsdeckung/felsdeckung_regeln.json` |
| Pilotplaner (Referenz für fs_plan v9) | `skripte/felsdeckung/felsdeckung_plan.py` (+ `felsdeckung_bilder.py`) |
| Prüfer | `skripte/felsdeckung/felsdeckung_pruefen.py`: **0 FEHLER**, zwei Läufe byte-gleich (78 Dateien) |
| Hochrechnung auf alle Felder | `skripte/felsdeckung/felsdeckung_hochrechnung.py` → `felsdeckung/hochrechnung_felder.json` |
| Pilotplan B5-Ost (FORMAT §3) | `felsdeckung/klippenband_B5/`, `halde_B5/`, `platten_B5/`, `baumgruppen_B5/` (plan.json + f32) |
| Akteure | `felsdeckung/akteure_B5.json` (7: 1 Turmklotz, 6 Hero-Blöcke ≥ 6 m) |
| Lagen, Gras, Ausdünnen, Zonen | `felsdeckung/lagen/`, `felsdeckung/masken/`, `felsdeckung/masken_B5.json` |
| Höhenplan Variante B (A15, optional) | `felsdeckung/gelaende_B5_variante_b/` |
| Bilder | `felsdeckung/bilder/`: `zonen_B5.png`, `draufsicht_B5.png`, `delta_karte_B5.png`, `querschnitte_B5.png`, `skizze_wand_halde_tal.png` |
| Prüfbericht, Statistik | `felsdeckung/pruefbericht_B5.txt`, `felsdeckung/statistik_B5.json` |

Aufruf (Repo-Wurzel, Cloud-Daten 2 m; lokal `--daten1m export/unreal/welt`):

```
python -I recherche/antworten/skripte/felsdeckung/felsdeckung_plan.py --aus recherche/antworten/felsdeckung --bild
python -I recherche/antworten/skripte/felsdeckung/felsdeckung_pruefen.py --plan recherche/antworten/felsdeckung --determinismus
python -I recherche/antworten/skripte/felsdeckung/felsdeckung_hochrechnung.py --plan recherche/antworten/felsdeckung
```

## Kurzfazit

1. **Die Kernthese stimmt, mit einer Präzisierung.** Was bei der Hobbyszene und bei Witcher den Unterschied macht, ist **3D-Deckung**, nicht
   „80 % Fels überall“. In Witcher 06/07 sind die Wände zu 100 % Fels und die Hänge darunter zu 100 % Wald oder Blockhalde. Landschaftstextur ist
   dort nie die sichtbare Oberfläche. Bei uns trägt die Textur 50–100 % der Hangflächen. Ferats Dichte-Zensus (6h) bestätigt das: An Stückzahlen
   liegen wir gleichauf (C2 9,4 gegen RA2 8,7 Netze je 100 m²), aber RA2 hat **378 % Felsfußfläche** (wenige große, gestapelte `SM_Ridge_Rock_01`),
   unsere Talkaskade nur 1,2 %. Es fehlen also **große, überlappende Netze an der richtigen Stelle**. Mehr Kleinzeug hilft nicht.
2. **Der größte Hebel ist ein Neigungsband, das heute niemand bedient: 38–50° („Schrofen“).** Welt nach meiner Zonierung: Wand 292 ha,
   **Schrofen 388 ha**, Halde unter Wänden nur 133 ha, Hangfuß 286 ha. Unsere Berge sind eine glatte Rampe von 40–55°. Das ist zu steil für eine
   Halde (Talus liegt bei 30–37°) und zu flach für eine Wand. Geologisch sind das Felsstufen-Hänge. Die Regel dafür: **Felsbänder entlang der
   Schichtlinien** (Δz 5,5 m, Bandhöhe 3–4,5 m, 80 % durchgehend), dazwischen Tritte mit Latschen und Grasflecken. So entstehen echte 3D-Stufen,
   ohne das Gelände umzubauen.
3. **„Keine Brockenflut“ ist eine Frage von Gleichförmigkeit und Größe, nicht von Anzahl.** Belege: Die abgelehnten Fälle (E4 +1 327 Füller
   1–3 m auf 30–60-m-Wänden; Runde 5 „Kistenhaufen“) hatten alle eine Größe auf zu großer Fläche, gleichmäßige Abstände, würfelige Formen und lagen
   auf statt eingegraben. Dagegen wurden 27 Bachdekor-Teile je m in p2 und 13 039 Felsgruppen-Instanzen in B4 angenommen. Eine Halde liest als
   Halde bei **5,7 Instanzen je 100 m²**: großflächige Scan-Bodenplatten als „Schutt-Teppich“ plus Blöcke nach Potenzgesetz, große Blöcke unten
   (Fall-Sortierung), in Kegeln geklumpt, mit Rasenzungen dazwischen. Anhang A rechnete mit 50 je 100 m²; das ist fast 10× weniger.
   Schutt unter 0,5 m kommt **nicht als gespeicherte Instanz**, sondern als Geröll-Lage plus Grastyp bzw. später Runtime-GPU-PCG, wie bei Witcher 4.
4. **Pilot: B5-Ost (480 × 500 m), ein besserer Vorschlag als die drei Kandidaten aus §3.4.** Er liegt im bergwald (96 %). Eine Blickachse von
   Osten fasst Wand (4,3 ha, Relief bis 450 m), Schrofen (8,3 ha), Halde (2,0 ha), Hangfuß (2,6 ha) und zwei Bäche als Talboden. Er liegt nicht im
   p2-Arbeitsgebiet von Auftrag 20. Plan: **6 471 Instanzen + 7 Akteure**, 46 Netze (Demo-Karten 35–53).
   Grundriss-Netzdeckung je Zone (Mittelwert, 0,5-m-Raster):

   | Zone | Netzdeckung |
   |---|---|
   | Halde | 77 % (oben 83 %) |
   | Wand | 80 % (eigene Reihen, die FS-Schalen kommen dazu) |
   | Schrofen | 57 % |
   | Hangfuß nah | 28 % |
   | Felszone gesamt | 67 % |

   Fels-Lage ≥ 38° ohne Netz liegt bei 24,8 % (heute ~100 %). Fußflächen-Summe nach Ferats Zensus-Definition: Halde 145 %, Wand 128 %.
5. **Speicher:** Hochgerechnet ergibt das Regelwerk **≈ 389 000 neue Instanzen für die ganze Welt**, höchstens 24 000 je Feld (D2), B5 22 000,
   B4 18 000. Das sind etwa 4–14 MB RAM je Feld und 46 neue Netze, die Nanite-Daten werden nur einmal geladen. Instanzen sind nicht das Risiko. Die
   Risiken sind die Texturen der Raw-8K-Sätze (vorher auf 4K klemmen) und Bäume mit WPO (VSM). Weil die Ausdünn-Maske etwa 60 % des Altbestands
   im Fenster entfernt, sinkt die Baumzahl im Pilot.
6. **Höhenumbau ist im Pilot nicht nötig.** Variante B (3 Schüttkegel, max 5 m, 9 168 m³) ändert auf dem 45–55°-Hang sichtbar wenig
   (Querschnitte), kostet aber einen Feld-Neuaufbau. Empfehlung: nur Netze. Stufen, Plateau und Turm macht das Klippenband.
7. **Eigene Planer statt PCG für Fels und Bäume.** Das entspricht der Witcher-4-Aufteilung: Felsen und Bäume offline, Kleinzeug zur Laufzeit per
   GPU-PCG. Der Grund sind 67 km² mit WMI-Ketten, Feld für Feld, deterministisch und in der Cloud prüfbar. PCG kommt später nur für Kleinzeug unter
   0,5 m.
8. **Ab welchem Schritt ein Prüfbild wie die Referenz liest** (Reihenfolge f): nach den Schritten 1–4 (Messung, Klippenband, Halde,
   Ausdünnen + Baumgruppen). Ziel ist dann ein Netz-Pixelanteil ≥ 75 % im Talblick K1.

## (a) Regeln „Felsdeckung je Hangneigung und Zone“ (bergwald)

Die Zonen werden aus `hoehe` mit geglätteter Neigung berechnet (Kasten ±3 m), damit Halde und Schrofen nicht im 1–2-m-Rauschen flackern.
Alle Dichten gelten je 100 m² Grundriss. Deckung = Grundriss-Fußabdruck (Ellipse der gedrehten Bounds × 0,85), Vereinigung ohne Doppelzählung.

| Zone | Bedingung | Netzklassen (Thema) | Dichte / Geometrie | Deckung Ziel (Pilot gemessen) | Begründung |
|---|---|---|---|---|---|
| **Wand** | ≥ 50° und Relief ≥ 6 m in 12 m; Reihen nur bei Relief ≥ 20 m in 40 m | Großmodule in **Reihen** (`klippenband:wandreihe`): MassiveNordicCoastalCliff_01, HugeNordicCoastalCliff_01/02, ukjhcamga (geschichtet) | Reihen auf Schichtlinien, Δz = 0,75 × Modulhöhe (7,5 m), 35 % Überlappung, Kipp 4–10° in den Hang, Skala 0,8–1,15, Rückseite im Gelände (¼ Modultiefe), **Foliage/ISM mit Kollision**, keine Akteure | eigene Reihen ≥ 60 % (**80 %**), mit FS-Schalen ≥ 85 % | Reihenlogik aus klippen_plan 2.1; ISM statt Akteur (Epic: Primitive ≈ 10× Instanz; WP-Hänger ab 200+ Akteuren je Zelle) |
| **Turmklotz** | 1 je Wandfront (markanteste Nase, TPI 40 m, ≥ 30 m vom Wasser) | veqnci0db (Akteur) | aufrecht, 25 % eingegraben, Krone ≤ 25 m über dem Grat erlaubt | Pilot 1 (Krone 5,5 m unter dem Grat) | Blickziel der Referenz; fs_plan-„turm“ ohne „nicht über Wand“ |
| **Gratkrone** | Grat (TPI 20 m ≥ 3 m) und ≥ 25° | HugeNordicCoastalCliff_02, big_rock_wall_01 | Abstand ≥ 36 m, Höhe 4–7 m, Front hangab | Pilot 42 | gebrochener statt runder Grat; Plateau nur als Netz |
| **Schrofen** | 38–50°, nicht Halde | Felsbänder (`klippenband:band`): big_rock_wall_01/02, ForestRockSlab_01, mountain_rock_big_02_3 | Bänder auf Schichtlinien f = h − tan(8°)·(x cos 20° + y sin 20°), **Δz 5,5 m ± 1,2 m**, Bandhöhe 3–4,5 m, 25 % Überlappung, **80 % durchgehend** (Lücken 5–20 m), Rücksprung 0,5–2 m je Band, Rückneigung 14°; dazu Latschen 2–5 je Gruppe (~18 Gruppen/ha), Grasflecken ≤ 18 % | ≥ 50 % (**57 %**) | größte Fläche der Welt ohne Netz (388 ha); Stufen 2–6 m der Referenz; gemeinsames Streichen (felsgruppen „schichtung“) |
| **Halde** | 26–40°, ≤ 60 m unter einer Wand und tiefer als die mittlere Wandhöhe im Umkreis 40 m | **Schutt-Teppich** (flache Scans): TundraRockyGround_01, NordicBeachRockyGround_01/02, ForestRockFormation_05/06; **Blöcke**: MossyForestBoulder, xf3odif/xfplcbf/xjijbgx, mountain_rock_big_02_*, Hero NordicBoulder_01/TundraMossyBoulder_01 | Teppich: Zieldeckung 72 % am Wandfuß → 42 % am unteren Rand, × (1 ± 0,55 Kegelrauschen 36 m), Rasenzungen (Rauschen < −0,55 → × 0,25), Skala 1,3–1,8, Yaw Falllinie ± 25°, 30–50 % eingegraben. Blöcke je Klasse (oben → unten): 0,8–1,5 m **2,0 → 1,0**; 1,5–3 m **0,6 → 0,8**; 3–6 m **0,10 → 0,30**; 6–9 m **0 → 0,04**; Potenzgesetz N(>d) ∝ d^−2,2 in der Klasse; lange Achse ± 20° zur Falllinie; 40–60 % senkrecht eingegraben; Mindestabstand 0,62·(rᵢ+rⱼ) (berühren sich); harte Quote je 48-m-Zelle: > 2 m ≤ 1,2, > 4 m ≤ 0,35 | ≥ 50 %, oben ≥ 60 % (**77 % / 83 %**) | Talus 30–37°, konkav ([Scottish Geology Trust](https://geoguide.scottishgeologytrust.org/page/2138), [Wikipedia Scree](https://en.wikipedia.org/wiki/Scree)); Fall-Sortierung grob unten ([JNCC GCR](https://data.jncc.gov.uk/data/c9bdfe0b-ca6f-4a90-87a6-d03f64e8124c/gcr-v33-mass-movements-c4.pdf)), nicht überall ([NHESS 2021](https://nhess.copernicus.org/articles/21/1159/2021/)) |
| **Schutt < 0,5 m** | Halde, Wandfuß | Lage Geröll 235 (Halde), 225 unter jedem Stück + 1 m Saum; Grastyp/PCG mit SM_mountain_rock_small_01_*, SM_stones_01_*, SM_SmallStonesPack_* | **0 gespeicherte Instanzen**; Grastyp 0,6–1,2/m², End-Cull 30–40 m | – | Witcher 4: „runtime GPU-based PCG … for the small debris“ (DF-Interview, siehe `boden-kleinzeug-gras.md`) |
| **Hangfuß / Plattenfelder** | 12–26°, ≤ 150 m unter Wand oder ≤ 40 m unter Halde; „nah“ = ≤ 60 m | Platten (`platten:platte`): flat_rock_02/04, ForestRockSlab_01, TundraRockyGround_01, ForestRockFormation_06 | Länge 4–10 m (Potenz 0,8), nur in Plattenfeldern (Kegelrauschen ≥ −0,2), Zieldeckung nah 28 %, fern 8 %, 40–60 % senkrecht eingegraben, Yaw = Streichen + 90° ± 25° | nah ≥ 22 % (**28 %**) | Witcher 04 (Platte mit Flechten); keine „3 Platten je 100 m²“ (Anhang A) – das wird Konfetti |
| **Fugenbewuchs** | Ring 0–0,4 m außerhalb jeder Platte | Gras (grass_bush_01/04, wk2oaeyqx_VarA) 60 %, Farn (fern_01_0/1) 25 %, Moos (moss_01) 15 % | 0,3 je m Plattenrand (± 30 %) | Pilot 2 131 | „Grasbüschel in den Fugen“ |
| **Baumgruppen** | Hangfuß, Hangwald, Halde (t > 0,6), Schrofen; ≥ 10 m vom Wasser; Hang ≤ 46°; nie Wand | Nadel: jung SM_Forest_pine_tree_00_A/B (4,5–6,5 m) 30 %, mittel tree_00_C/D (8,5–12 m) 40 %, hoch pine_10_special/SM_Forest_pine_01 (12,5–15 m) 30 %; tot pine_10_dead jeder 18.; Latschen dwarf_pine_* | Zentrumsabstand 30 m (Fuß/Hangwald), 40 m (Halde), 45 m (Schrofen); Wahrscheinlichkeit 0,55 / 0,6 / 0,35 / 0,25; Lückenrauschen 60 m (< −0,15 → keine Gruppe); 3–8 Bäume, Radius 5–11 m, Mindestabstand 3,5 m; **jeder Baum mit Block ≥ 1 m im Radius 3 m** (sonst Fußblock 1–2,5 m hangab); liegendes Totholz 0,5 je Gruppe | baumfreie Felszone ≥ 35 %; Grat-Kette ≤ 3; Höhe hoch : jung ≥ 1,8 (Pilot 3,3) | Witcher 04/06/07: Gruppen und Lichtungen; Maßstab Baum 8–15 m gegen Block 1–8 m |
| **Grat-Regel** | ≤ 8 m vom Grat | wie oben | Gruppe ≤ 3 Bäume, andere Grat-Gruppe ≥ 40 m entfernt | größte Kette 3 | B4-„Hecke“ vermeiden |
| **Baumart** | alle Felszonen | nur Nadel | Birke nur ≤ 25 m vom Wasser oder in Aue (wit_plan, c) | – | Referenz „nur Fichten/Kiefern“ |
| **Gras** | Halde/Schrofen/Wand | Grasdichte-Maske | unter Stücken 0, Fugenring 0,3–1,5 m 255, sonst Flecken ≤ 18 % (Rauschen 5 m); Hangfuß 60 % voll, Rest 60/255 | – | Referenz „Gras nur Flecken“ |
| **Uferband** | 0–10 m ab Wasserkante | – | **nichts von diesem Planer** (Auftrag 20) | – | Abgrenzung |
| **Übergang** | 10–15 m | Blöcke, Platten, Teppich | Teppich-Zieldeckung × 0,5; keine Bänder, keine Bäume | – | Wandfuß-Schuttband am Wasser gehört zu A20 (Zeile „1 Schuttband am Fuß jeder Wand“) |

### Abweichungen je Biom (Faktoren in `regeln.biome`, bezogen auf bergwald)

| Biom | Deckung | Bäume | Abweichung |
|---|---|---|---|
| bergwald | 1,0 | 1,0 | Referenz (Nordic-Paletten wie oben) |
| fjord | 1,1 | 0,7 | Bänder Δz 4,5 m, mehr Wandreihen; Klippe bis ans Meer gestuft (klippen_plan, c) |
| gletscher | 1,0 | 0,35 | Teppich mit Schnee (Rocky_Snow_Pile vcyiccyga/xfwgbg0qx), Schnee-Auflage MI_EL_Auf_* auf Oberseiten; Latschen statt Bäume über 300 m |
| kueste | 0,9 | 0,5 | NordicBeachRocks/RockyGround bevorzugt; Platten bis 15 m ans Meer; Küstenkiefern pine_beach_* |
| tundra | 0,8 | 0,5 | Teppich mit TundraRockyGround/MossyRocks; Bänder flacher (Höhe 2–3 m); Birke nur am Wasser |
| wueste / canyon | 0,7 / 0,9 | 0 / 0,1 | Sandstein-Paletten (Desert_Western_Layered für Bänder, rot), eigener Planer C3–E5 nur ergänzen, keine Grasflecken |
| elfenwald | 0,55 | 1,3 | Moos-Paletten (MossyForestBoulder, Mossy_Rock_Formation plFhY), Wald trägt die Hänge, Halde nur unter echten Wänden |
| dschungel | 0,5 | 1,5 | Karst (AsianTemple SM_Cliff_01a–e) nur als Wand/Turm; Bewuchs deckt Schrofen |
| lava / oedland | 0,8 / 0,7 | 0 / 0,2 | Lava-Paletten (Pivot Mitte!), Basalt erst nach Nanite-Umstellung; Teppich aus Lavafels-Netzen fehlt (e) |

### „Keine Brockenflut“ – was das Problem ist und welche Dichte als Halde liest

| Fall | Anzahl | Größe | Gleichförmigkeit | Form/Lage | Urteil |
|---|---|---|---|---|---|
| E4 +1 327 Füller (abgelehnt) | +1 327 auf ~3 ha Wand | 1–3 m auf 30–60-m-Wand → Konfetti | ein Größenband, Rasterabstand | aufgelegt | Größe + Gleichförmigkeit |
| Runde 5 „Kistenhaufen“ (abgelehnt) | 0,4/100 m² > 2 m (unter der Grenze!) | 2–4 m gleichverteilt | örtlich dicht, isotrop | würfelig, 25 % eingegraben, Unterseiten sichtbar | Form + Lage + Gleichförmigkeit |
| p2 Bachdekor (angenommen) | 27 je m | 0,1–1 m | Bachlauf-Struktur | eingebettet | Anzahl kein Problem |
| Zensus 6h | C2 9,4 vs RA2 8,7 je 100 m² | RA2: wenige riesige Ridge_Rock, 378 % Fußfläche | gestapelt, überlappend | – | Komposition ist das Problem |

**Vorschlag:** Halde mit **Teppich 3,6 + Blöcke 2,1 = 5,7 Instanzen je 100 m²** (Pilot), Fußflächen-Summe 145 %, Deckung 77 %. Gleichförmigkeit wird
viermal gebrochen:

- Kegelrauschen ± 55 %,
- Rasenzungen,
- Potenzgesetz plus Fall-Sortierung,
- 4 Größenklassen.

Würfelige oder stehende Netze über 1,5 m sind verboten (wie Runde 5). Prüfung im Editor: Prüfbild K2 Ferat zeigen und fragen: „Halde oder
Brockenflut?“

### Prüfung von Anhang A (Ferats Ableitungen)

| Anhang A | Übernommen? | Meine Regel |
|---|---|---|
| ≥ 80 % Netz überall | teilweise | je Zone: Wand ≥ 85 % mit Schalen, Halde ≥ 70 %, Schrofen ≥ 55 %, Hangfuß ~30 %; Rest Wald/Latschen/Gras = 3D-Deckung |
| Haldenband 0,3–0,5 × Wandhöhe, 30–38° | ja (≤ 60 m) | Hang 26–40°, weil unser Gelände kaum echte Talus-Winkel hat |
| ≥ 10 Blöcke + ≥ 40 Schutt je 100 m² | **nein** | 2,1 Blöcke + 3,6 Teppich-Scans; Schutt als Lage/Grastyp (10× weniger Instanzen) |
| Größe nimmt hangab ab | **umgekehrt** | Blöcke grob unten (Fall-Sortierung), Deckung nimmt hangab ab |
| Eingraben 30–50 % | ja, mehr | 40–60 % senkrecht zum Hang |
| Bänder 2–6 m, Rücksprung 0,5–2 m | ja | Δz 5,5 m, Band 3–4,5 m, Rücksprung 0,5–2 m |
| Turm ≥ 20 m über dem Grat | gelockert | ≤ 25 m erlaubt, nicht verlangt |
| Platten ≥ 3 je 100 m² | **nein** | Deckung 28 % mit Platten 4–10 m in Feldern (≈ 1 je 100 m²) |
| Block : Baum ≥ 1 : 1 | ja | jeder Baum mit Block ≥ 1 m in 3 m (Pilot 97,6 %, Block:Baum 4,2) |
| Grat ≤ 3 in Reihe | ja | Kette ≤ 3, 40 m Abstand |
| Totholz Poisson 5 je Gruppe | nein | 0,5 liegend je Gruppe + 1 stehend je 18 Bäume (Referenz ohne Totholz) |

## (b) Pilot B5-Ost

**Warum nicht D2, B5-Bach oder B4-K1?**

- D2 p2-Quelle ist das Arbeitsgebiet von Auftrag 20. Dort würden zwei Pläne in dieselben Zellen schreiben. Außerdem ist es tundra/gletscher mit
  Birken.
- Das B5-Fenster am Bach R3 hat nur 0,3 ha Wand.
- B4-K1 ist das schwerste Feld; dazu kommen Wasserfall und Hauptfluss.

**B5-Ost** (`fenster_m` −3200…−2720 / 0…500, ganz in B5) ist die Ostflanke desselben Massivs. Die Suche über 500-m-Fenster (Score aus Wand + Halde + Talboden; bergwald, fjord, gletscher, tundra, kueste ≥ 70 %) setzte es auf Platz 4 der Welt: Wand 3,4 ha, Halde 5,9 ha,
Talboden 2,6 ha. Davor liegen zwei D2-Fenster (p2-Gebiet, tundra) und ein A3-Fenster (bergwald, Nordende des Massivs, gleichwertig, aber
1,4 ha Wasser und Weg im Fenster). Für den Plan ist das Fenster um 70 m nach Westen verschoben, damit es ganz in B5 liegt. Von Osten aus K1 (Tal in C5,
450–600 m Abstand) stehen Wand, Schrofen und Halde im oberen Bilddrittel, die zwei Bäche bilden die Mitte. Das ist die Komposition der Referenz.

Zonen im Fenster (24 ha):

| Zone | Fläche |
|---|---|
| Wand | 4,35 ha |
| Schrofen | 8,27 ha |
| Halde | 2,01 ha |
| Hangfuß | 2,61 ha |
| Hangwald | 2,72 ha |
| Tal | 0,03 ha |
| Sperre (Uferband, Wege) | 4,01 ha |

| Thema (Kürzel, FT-Präfix) | Instanzen | davon | Akteure | Kollision |
|---|---|---|---|---|
| `klippenband_B5` (KBAND, `FT_EL_KBAND_`) | 2 031 | 1 364 Bänder, 625 Wandreihen, 42 Gratkronen | 1 Turm | 2 031 |
| `halde_B5` (HALDE, `FT_EL_HALDE_`) | 1 149 | 733 Teppich, 416 Blöcke (246 / 143 / 29 je Klasse) | 6 Hero | im Budget |
| `platten_B5` (PLATTE, `FT_EL_PLATTE_`) | 2 560 | 429 Platten, 2 131 Fugenpflanzen | 0 | Platten |
| `baumgruppen_B5` (BGRP, `FT_EL_BGRP_`) | 731 | 49 Gruppen, 209 Bäume (8 tot), 152 Fußblöcke, 18 Totholz, 352 Latschen | 0 | Bäume/Blöcke |
| **Summe** | **6 471** | 46 verschiedene Netze, Quellnetze 0,44 M Dreiecke | **7** | 3 000 (Deckel; 255 kleinste Steine ohne) |

**Prüfer `pruefbericht_B5.txt`: 0 FEHLER.**

| Geprüft | Ergebnis |
|---|---|
| Sperren | 0 Stücke im Uferband 0–10 m, auf Wegen, im Meer |
| Lage | 0 schwebend, 0 außerhalb von Feld oder Fenster |
| Form | 0 würfelige Blöcke > 1,5 m |
| Halde, Dichte je 48-m-Zelle | max 1,02 (> 2 m) / 0,25 (> 4 m) je 100 m² |
| Bäume | 97,6 % mit Block, größte Grat-Kette 3 |
| A15 | 0 Zellen mit Auftrag < 12 m vom Wasser |
| Determinismus | zwei Läufe (PYTHONHASHSEED 1/4711) byte-gleich |

**Reihenfolge lokal:**

1. Ausdünn-Maske anwenden:
   - Datei `masken/ausduennen_B5.u8`, 255 = entfernen, 59,8 % des Fensters.
   - Nur Altbestand-Bäume: Houdini-Bäume, `FT_EL_WIT_*` Hangwald/Haine, `FT_EL_BST_*`.
2. Lagen schreiben: `lagen/felsdeckung_B5_{Geroell,Fels,Felsplatte}.r8`, `fenster_ij` 4060/1530/502/482, `neu = max(alt, ziel)`.
3. Grasdichte: `masken/grasdichte_B5.u8` in die GT-Dichtekarten multiplizieren, dann rebuild_grass_maps.
4. Themen setzen: klippenband → halde → platten → baumgruppen (generischer FORMAT-§3-Setzer), dann Akteure aus `akteure_B5.json`.
5. Prüfbilder K1–K3 aufnehmen (Koordinaten in `regeln.pilot.kameras`).
6. Pixelmessung mit Ferats Werkzeug.

Rückbau: nach Präfix `FT_EL_{KBAND,HALDE,PLATTE,BGRP}_`. Das ist unabhängig vom `entfernen`-Filter der Felsgruppen und von fs_plan.

**Netze und Material vor dem Setzen:**

- `xf3odif`, `xfplcbf`, `xjijbgx`, `ukjhcamga` sind Raw-8K-Sätze: Texturen auf 4K klemmen (Post-Import-Pass aus `klippennetze-a5.md`).
- `SM_ErodedRockyGround_01–03` wären die besten Teppiche, haben aber den Materialbefund `textur_leer`. Sie sind deshalb nicht im Pilot; nach dem
  Material-Fix in die Palette `teppich` aufnehmen.
- `SM_IcelandicBoulder_*` sind gesperrt und werden nicht benutzt.

**Variante B (optional, nicht empfohlen):**

- 3 Schüttkegel an Rinnenausgängen am Wandfuß.
- Nur Auftrag, konkav 34° → 29°, Sektor ± 55°, max 5 m.
- Volumen: K1 2 389 m³, K2 2 015 m³, K3 4 764 m³.
- Format A15: `plan.json` mit `abschnitte[].gelaende` {`datei`, `fenster_ij`, `max_aenderung_m`}.
- Delta-Karte und Querschnitte unter `bilder/`.
- Auf dem 45–55°-Hang ist die Wirkung ein Keil von wenigen Metern. Den Feld-Neuaufbau (Höhen → Lagen → Gras → Nanite → Foliage verschieben)
  lohnt das nicht.
- Wenn doch gewünscht: Planer mit `--gelaende` neu laufen lassen. Der Prüfer meldet auch dafür 0 FEHLER.

## (c) Planer-Änderungen (Patch-Beschreibung, die Skripte liegen lokal)

### fs_plan.py v8 → v9 (Referenzumsetzung `felsdeckung_plan.py`)

| Parameter | v8 | v9 | Hinweis |
|---|---|---|---|
| Zonen | nur Wandzellen ≥ Biom-Schwelle 40–55°, Wandhöhe ≥ 6 m | **6 Zonen**: Wand ≥ 50° (Relief ≥ 6 m), Schrofen 38–50°, Halde 26–40° unter Wand (≤ 60 m, tiefer als mittlere Wandhöhe 40 m), Hangfuß 12–26°, Hangwald, Tal; Neigung für Zonen mit Kasten ± 3 m geglättet | `Kontext` im Referenzplaner |
| `luecke_roh` / WELT_FUELLER | aus (Probe E4 abgelehnt) | **bleibt aus**; ersetzt durch Schrofen-Bänder und Halde | kein Füller auf Wänden |
| Fußzone (`fuss_abstand_m` 5, `fuss_k` 3,0) | Brocken weit auseinander | ersetzt durch Halde-Modul (Teppich + Blöcke, Fall-Sortierung, Quote je 48-m-Zelle) | `plane_halde` |
| Neu: `schichtung` | – | Streichen/Fallen je Massiv aus dem felsgruppen-512-m-Rauschen (statt Pilot-Konstante 20°/8°) | ein Code für felsgruppen und fs_plan |
| Neu: Schrofen-Bänder | – | `band_dz_m` 5,5 ± 1,2, `band_hoehe_m` 3–4,5, Überlappung 0,25, Kontinuität 0,8, Rückneigung 14°, Versatz 0,5–2 m | `plane_klippenband` Teil 1 |
| Wand-Reihen | Zufallsnetze, Wiederholung 20 m | **Reihenlogik aus klippen_plan 2.1** für Binnenwände ab 20 m Relief: Δz = 0,75 × Modulhöhe, 35 % Überlappung, Kipp 4–10°, Front hangab; als Foliage mit Kollision | Schalen bleiben, Reihen kommen dazu; Ziel ≥ 85 % |
| Turm-Modus | „nicht über Wand“ | 1 je Front, Krone ≤ 25 m über dem Grat, Akteur | Blickziel |
| Eingraben | Klassenwerte | Teppich 30–50 %, Blöcke/Platten 40–60 % **senkrecht zum Hang** (z = e·H/cos α), Schwebe-Test wie Runde 5 | |
| Netzform | – | würfelig/stehend > 1,5 m verboten (Verhältnis < 1,4 / Z längste Achse) | aus felsgruppen Runde 5 |
| Platten-Rolle | Sims-Füller ForestRockShelf ≤ 40° | Plattenfelder 12–26°, 4–10 m, Deckung 28/8 %, Fugenring | `plane_platten` |
| Palette | 64 FT_EL_FS_* | ≤ 50 Netze je Biom, große Scans zuerst | Zensus 6h |
| Prüfung | fs_deckung_c ≥ 50° | Deckungsraster je Zone 25–90°, Fels-Lage ≥ 38° ohne Netz, Dichtequoten | `felsdeckung_pruefen.py` |

Laufzeit Referenzplaner: 11 s für 24 ha (2 m, ohne numba). Hochgerechnet auf ein 1-km-Feld mit 1 m sind es etwa 2–4 min; mit numba sollte es
unter 60 s bleiben (nicht gemessen).

### wit_plan.py

| Parameter | heute | neu |
|---|---|---|
| fels_lage-Grenze Gruppenmitte / Baum | ≤ 0,6 / ≤ 0,7 | ≤ 0,9 / ≤ 0,95 (Bäume dürfen in den Fels) |
| Block je Baum | 0,3 Großfelsen je Gruppe | **jeder Baum mit Block ≥ 1 m in 3 m**, sonst Fußblock 1–2,5 m hangab (MossyForestBoulder_03/04, mountain_rock_big_02_5) |
| Höhenklassen | keine | jung 30 % (4,5–6,5 m), mittel 40 % (8,5–12 m), hoch 30 % (12,5–15 m); Hauptbäume SM_Forest_pine_01–09 nur mit Skala 0,6–0,9 |
| Grat-Regel | keine | ≤ 8 m vom Grat: Gruppe ≤ 3, nächste Grat-Gruppe ≥ 40 m |
| Ausdünnen | nie | Maske wie `ausduennen_B5.u8`: Wand, Halde t < 0,6 und Gratband 8 m immer; Schrofen außer Bestandsinseln (Rauschen ≥ 0,25); Hangfuß/Hangwald in Lücken (Rauschen < −0,05) |
| Birke | Artgewicht tundra 0,65 / bergwald 0,2 | in Felszonen 0; nur ≤ 25 m vom Wasser oder in Aue |
| Totholz | Poisson 1,6 je Gruppe | 0,5 liegend je Gruppe + jeder 18. Baum stehend tot |

### klippen_plan.py 2.1

- **Binnenwand-Modus:** Die Bedingung „Meer < 60 m“ wird optional. Fronten kommen aus Wandzellen-Ketten mit Relief ≥ 20 m. Die Reihenhöhen
  liegen auf der Schichtfunktion statt auf festen Höhen (gleiche Bänder in Wand und Schrofen).
- **Küste A5/B5:** Reihen bis 2 m über den Meeresspiegel fortsetzen. Das ergibt den gestuften Abgang zum Meer, die fehlende Zeile aus §1.
- `deckung_bis_30m` je 120-m-Abschnitt bleibt Prüfmaß, Ziel ≥ 0,85.

### bachdekor (nur Abgrenzung, Inhalt bei Auftrag 20)

Blöcke ≥ 1 m im Wasser und „Stamm quer“ brauchen die SWR-Umfluss-Prüfung aus 16h. Das plant Auftrag 20. Dieser Plan setzt **0 Stücke in 0–10 m**.
Die Halde endet an der 10-m-Linie, damit ihr Schuttband und das Uferband von A20 nicht doppelt belegt werden.

### PCG gegen eigene Planer

| Kriterium | eigene Planer (FORMAT §3) | PCG (UE 5.7/5.8) |
|---|---|---|
| Reife | erprobt (felsgruppen, wit_plan, sehens, A15) | Framework seit 5.7 production-ready ([Epic 5.7](https://www.unrealengine.com/news/unreal-engine-5-7-is-now-available), Suchauszug); Nanite Foliage und Procedural Vegetation Editor experimentell ([Digital Production](https://digitalproduction.com/2025/11/12/unreal-engine-5-7-foliage-pcg-and-in-editor-ai/)) |
| 67 km², Feld für Feld, WMI-Ketten | Planer offline in Sekunden je Feld, Setzer seriell | Partitionierte Generierung im Editor, schwer per WMI zu takten; Python ohne PCGMeshSampler |
| Prüfung in der Cloud | ja (dieser Prüfer, 0 FEHLER, byte-gleich) | nein, nur im Editor |
| Determinismus und Nahtstellen | Hash-Zufall aus Koordinaten, Feldrand 64 m | Seeds je Partition; Nahtverhalten zu WP-Zellen ungeklärt (`boden-kleinzeug-gras.md`) |
| Kleinzeug < 0,5 m | sinnlos als gespeicherte Instanzen | **richtig dafür**: Runtime-GPU-PCG (Witcher 4) |
| Speicher | gespeicherte Instanzen (≈ 0,4 M Welt, s. d) | Runtime-Instanzen nur um die Kamera |

**Entscheidung:** Fels, Bänder, Platten und Bäume mit eigenen Planern (v9). Schutt und Kleinzeug zuerst als Grastyp, später als GPU-PCG. Die
Electric-Dreams-Graphen dienen nur als Ideenquelle (laut Teammitglied kam der PCG-Inhalt nicht in die Demo, [ArtStation](https://jackm.artstation.com/projects/DvmwAO), Suchauszug).

## (d) Speicher- und Leistungsschätzung

Hochrechnung mit `felsdeckung_hochrechnung.py`: Zonen je Feld × Raten des Pilots je ha Zielzone × Biomfaktor.

| Thema | Rate je ha | Zielzonen |
|---|---|---|
| Halde | 571 | Halde |
| Klippenband | 161 | Schrofen + Wand |
| Platten | 982 | Hangfuß (davon 80 % Fugenpflanzen) |
| Baumgruppen | 47 | Felszonen |

| Feld | Biom | Wand / Schrofen / Halde / Fuß ha | neue Instanzen | Akteure | heute (07.10.) | danach | RAM neu |
|---|---|---|---|---|---|---|---|
| B5 | bergwald | 30,7 / 30,6 / 4,8 / 7,0 | 22 062 | 19 | 97 223 + 1 454 Akt. | ≈ 119 000 (minus Ausdünnung) | 4–13 MB |
| B4 | bergwald | 40,1 / 25,1 / 2,7 / 4,4 | 18 337 | 13 | 106 925 + 3 819 Akt. + 13 039 FG | ≈ 138 000 | 4–11 MB |
| D2 | tundra | 16,7 / 21,9 / 8,2 / 17,5 | 24 030 (Max. der Welt) | 22 | 122 674 | ≈ 147 000 | 5–14 MB |
| C2 | gletscher | 22,5 / 17,5 / 1,9 / 6,7 | 14 683 | 9 | 65 255 + 24 402 p2 | ≈ 104 000 | 3–9 MB |
| E2 | gletscher | 11,1 / 19,2 / 5,5 / 14,8 | 23 477 | 19 | – | – | 5–14 MB |
| A5 | kueste | 2,2 / 10,2 / 2,1 / 1,7 | 4 797 | 6 | + FG 3 245 + KP 357 | – | 1–3 MB |
| **Welt** | – | 292 / 388 / 133 / 286 | **≈ 389 000** | ≈ 355 | 2,92 M | ≈ 3,3 M (+13 %) | ≈ 80–230 MB |

| Ressource | Schätzung | Grundlage / Maßnahme |
|---|---|---|
| RAM (50,6 GB) | +80–230 MB Welt, +4–14 MB je Feld | 200–600 B je Instanz (64 B GPU-Instanzdaten laut Epic-ISM-Doku + Foliage/HISM/Undo im Editor); unkritisch |
| Akteure je Zelle | ≤ 22 neue je Feld | Wand/Bänder als ISM; WP-Hänger erst ab 200–300 Akteuren je Zelle (Forum, `klippennetze-a5.md`) |
| Nanite-Daten | 46 Quellnetze, 0,44 M Dreiecke einmalig | Instanzzahl kostet Nanite kaum (Cluster-Culling); Nanite-Streaming-Pool prüfen (`r.Nanite.Streaming.StreamingPoolSize`, laut Forum Standard 512 MB, unbestätigt, [Guru3D](https://forums.guru3d.com/posts/6015659/)) → 1024 MB setzen, wenn `stat NaniteStreaming` Überlauf zeigt |
| Texturen (Pool 8 000 MB) | ~30 neue Materialsätze × 25–45 MB (4K) ≈ 0,8–1,4 GB voll aufgelöst, gestreamt deutlich weniger | **Raw-8K vorher auf 4K klemmen** (xf3odif, xfplcbf, xjijbgx, ukjhcamga = je ×4 Speicher) |
| VSM (Absturz bei 14,4/23,7 GB) | Felsnetze statisch, Nanite, ohne WPO → Seiten bleiben gecacht ([Epic Fortnite-VSM](https://www.unrealengine.com/en-US/tech-blog/virtual-shadow-maps-in-fortnite-battle-royale-chapter-4)) | Risiko sind Nicht-Nanite-Bäume mit WPO; im Pilot +209 neue Bäume, ~60 % des Altbestands im Fenster entfernt → netto weniger WPO-Bäume; Schutz-CVars beibehalten; Messziel VRAM ≤ 16 GB im K1-Blick |
| Ladezeit je Feld | +2–5 s beim ersten Laden (neue Netze/Texturen), danach ~0 | Schätzung ohne Messung; 7–22 Akteure je Feld |
| Nanite vorher umstellen | Pilot: keine Pflicht (alle Felsnetze Nanite) | für Biome später: SM_flat_rock_01, Mountain SM_Big_rock_01/02, Basalt 22, Rural Australia, Escarpments 02 (A20), Klasse A gruppenweise ≤ 20 000 Objekte; **Bäume erst nach VSM-Messung** (Nadelbäume sind Nicht-Nanite und haben WPO) |

## (e) Ladeliste und Einkaufsliste (nur Vorschlag, Ferat entscheidet)

Alle Posten außer dem letzten stehen in Ferats Fab-Bibliothek (kostenlos oder besessen) bzw. in seiner Ladeliste 6h §3. Netznamen nach dem Laden
aus dem neuen Inventar nehmen, nicht von hier.

| Posten (Fab-Bibliothek) | Größe / Art | Nanite | wofür | Priorität |
|---|---|---|---|---|
| Megaplants: Norway Spruce, Baltic Pine, Dead Pine | Nadelbäume 8–25 m mit Altersstufen | ja (Nanite Foliage, experimentell, UE 5.7+) | Baumklassen mittel/hoch statt skalierter SM_Forest_pine_0x; Lärchen-/Totbaum-Akzent | 1 – erst im Pilot-Fenster testen (VSM) |
| Megaplants: Black Alder | Laubbaum am Wasser | ja | Birke am Felshang ersetzen (nur ≤ 25 m vom Wasser) | 3 |
| Valley of the Ancient | große Nanite-Fels- und Klippenmodule | ja | Wandreihen und Turm (größere Module, weniger Wiederholung); Farbe vorher prüfen (dunkel) | 2 |
| Landscape Mountains / Free Mountain Terrain, Rock and Tree / Free Hill Rock Mountain Terrain | Bergkulissen | unbekannt | Fernebene (≥ 2 Silhouetten im Dunst) | 3 |
| Open World Demo Collection | Kite-Demo (Felsen, Kiefern, Heide) | unbekannt (UE4-Inhalt) | Kiefern 8–15 m, Felsflächen; vor Nutzung Nanite-Pass | 2 |
| Megascans laut 6h: scree, slate, layered cliff, boulder, rock assembly; Bibliothek: „Slate stone pile“, „Dirty stones pile“, „Rocks Pack“, „rocks pack“, „Forest pine boulder“, „Beach cliff rock face“ | Schutt-/Steinhaufen 2–4 m, Schichtkliff 6–12 m | Megascans ja | **Teppich** (Haufen statt 30 Steine), **Schrofen-Bänder in Nordic-Farbe** (fehlende Bandmodule 2–6 m), Hero-Blöcke 4–8 m | 1 |
| Realistic Mossy Rocky Grass PBR Material / Forest pine tree needles ground soil | Bodenmaterial | – | Geröll-/Nadel-Lage unter Halde und Bäumen | 3 |
| Nordic Coastal Cliff (f53f0b71, frühere Empfehlung) | geschichtete Nordic-Klippe | ja | Wandreihen bergwald/fjord | 2 |
| **kostenpflichtig, nur falls 1–3 nicht reichen:** Moos-/Flechten-Decal-Satz für Fels (Megascans/Fab) | Decals | – | Flechten auf Oberseiten (Witcher 04) | 4 |

## (f) Reihenfolge nach Wirkung

Gemessen wird immer im festen Standpunkt K1 (Talblick, 450–600 m zur Wand) und in K2 (Hangfuß).

| Schritt | Inhalt | Aufwand | Wirkung im Prüfbild |
|---|---|---|---|
| 1 | Messung einrichten: Ferats Pixelmessung (Netz/Landschaft) für K1–K3; Prüfer v9 (Deckungsraster 25–90°, Fels-Lage ≥ 38° ohne Netz) | 0,5 Tag | Ausgangswert (erwartet K1 ~15–25 % Netz) |
| 2 | **Klippenband**: Schrofen-Bänder + Wandreihen + Turm (größte sichtbare Fläche; Rampe → Stufen) | Pilot sofort; v9 2–3 Tage | **bricht zuerst**: aus 500 m ist die 40–55°-Rampe die halbe Bildfläche; K1 +30–40 Punkte |
| 3 | **Halde** (Teppich + Blöcke) + Lagen + Grasdichte | Pilot sofort | Wandfuß liest als Zone; Maßstabsanker 3–8 m |
| 4 | **Ausdünnen + Baumgruppen** (Altbestand weg, Gruppen 3–8 mit Block) | Maske vorhanden; wit_plan 1 Tag | Wald als Gruppen; **ab hier liest K1 wie die Referenz** (Ziel ≥ 75 % Netz) |
| 5 | Platten + Fugen am Hangfuß | Pilot sofort | K2-Vordergrund (Witcher 04) |
| 6 | Material: M_EL_Klippe_RVT (Fußblend, Moos-Krone), Flechten für bergwald, Farbbänder nach Welthöhe | 1–2 Tage | Kontaktzone, Farbe; Kachelung verschwindet |
| 7 | Bach im Blockwerk (Auftrag 20) | A20 | Mitte des K1-Bilds |
| 8 | Welt-Rollout Feld für Feld (Top-12 aus Hochrechnung), Fernebene, Megaplants-Bäume | je Feld 1 Lauf | – |
| 9 | Optional Variante B (Schüttkegel), Plateaus als Gelände, 1-m-Facetten | groß | gering |

## (g) Messkriterien (Schwelle für „bestanden“)

| Maß | Werkzeug | Schwelle Pilot | Pilot (Plan) |
|---|---|---|---|
| Netz-Pixelanteil K1 (Landschaft ausgeblendet) | **Ferats Pixelmessung** / SceneCapture `hide_actor_components` | ≥ 75 % (Wand+Halde-Bild), K2 ≥ 60 %, K3 ≥ 65 % | im Editor messen |
| größte zusammenhängende Texturfläche ohne Netz/Busch | Pixelmessung (Zusammenhangskomponente) | ≤ 10 × 10 m in K2 | im Editor |
| Grundriss-Netzdeckung Halde / oben | Prüfer | ≥ 50 % / ≥ 60 % | 77 / 83 % |
| … Schrofen / Wand (eigene) / Hangfuß nah | Prüfer | ≥ 50 / ≥ 60 / ≥ 22 % | 57 / 80 / 28 % |
| Fels-Lage ≥ 38° ohne Netz | Prüfer (Cloud: vorherrschende Lage; lokal `lage_Fels.r8` > 127) | ≤ 45 % (Welt-Ziel ≤ 30 % nach Schritt 6) | 24,8 % |
| Fußflächen-Summe Halde (Zensus-Definition) | Prüfer / Ferats Zensus | ≥ 120 % | 145 % |
| Instanzen je 100 m² Halde | Statistik | ≤ 8 | 5,7 |
| Blöcke > 2 m / > 4 m je 100 m² (Halde, 48-m-Zelle) | Prüfer | ≤ 1,2 / ≤ 0,35 | 1,02 / 0,25 |
| Blöcke > 2 m außerhalb Halde an Hängen > 35° | Prüfer (Runde 5) | ≤ 0,67 | 0,37 |
| würfelige/stehende Blöcke > 1,5 m; schwebende Stücke; Stücke im Uferband 0–10 m | Prüfer | 0 | 0 / 0 / 0 |
| baumfreie Felszone (kein Baum in 7,5 m) | Prüfer | ≥ 35 % | 90 % (nur neue Bäume; mit Altbestand im Editor zählen) |
| Baum mit Block ≥ 1 m in 3 m | Prüfer | ≥ 90 % | 97,6 % |
| Grat-Kette (Bäume ≤ 7 m Abstand im Gratband) | Prüfer | ≤ 3 | 3 |
| Höhe höchster/niedrigster Baum | Prüfer | ≥ 1,8 | 3,3 |
| verschiedene Netze im Fenster | Statistik | ≤ 60 | 46 |
| Determinismus | Prüfer `--determinismus` | byte-gleich | ja |
| VRAM im K1-Blick / `stat streaming` | Editor | ≤ 16 GB, kein Pool-Überlauf | im Editor |

Zum Rollout gehört eine Halde-Fußflächen-Karte je Feld nach Ferats Zensus (`ue_demo_dichte.py` mit Fenster = Feld): Vergleich gegen RA2 (378 %) und
gegen den Pilot (145 %).

## Was fehlt bis Witcher 4

- **Echte Großformen:** Kovir hat Türme und Pfeiler aus 5–20-m-Felsflächen mit Farbbändern (06/07). Uns fehlen große, geschichtete
  Nordic-Module in Nordic-Farbe, Plateaus und eine Gelände-Erosion, die schon im Höhenmodell Rinnen und Stufen anlegt (Witcher: Terrain außerhalb
  der Engine gebaut). Netze überdecken das. Ein neues Höhenmodell ist ein eigenes Projekt.
- **Material:** Fels mit RVT-Fußblend, Moos/Schnee nach Normale und Flechten (M_EL_Klippe_RVT); Farbbänder entlang der Bänder; Variation je
  Instanz über CPD.
- **Vegetation:** Nadelbäume 8–15 m mit Altersstufen und Nanite (Megaplants); Farbakzente (Lärchen-Rost); dichter Unterwuchs zwischen Blöcken
  (06: Büsche und Moos).
- **Kleinzeug zur Laufzeit:** GPU-PCG für Schutt, Zweige und Gras statt gespeicherter Instanzen. Bei CDPR sind „95 % of our screen often
  foliage“ (PC Gamer, siehe `boden-kleinzeug-gras.md`).
- **Licht und Atmosphäre:** Dunst an Wänden, Talnebel, Fernebene mit Bergsilhouetten.
- **Wasser:** Blockbach, Gischt, klares Live-Wasser (Auftrag 20, 16h-N6h).
- **Fernsicht:** HLOD-Instancing für Felsnetze (`hlod-fernansicht-world-partition.md`), sonst bricht die Felsdeckung ab 1 km ab.

## Quellen

Die Seiten wurden über die Websuche gelesen. Einträge mit „Suchauszug“ wurden nicht als Vollseite geöffnet.

- Talus-Winkel 35–37° oben, 31–34° unten, konkav: [Scottish Geology Trust, GeoGuide](https://geoguide.scottishgeologytrust.org/page/2138) (Suchauszug); [Wikipedia: Scree](https://en.wikipedia.org/wiki/Scree); Profilknick 33–34° unter Felswänden: [Francou & Manté 1990, Permafrost and Periglacial Processes](https://ideas.repec.org/a/wly/perpro/v1y1990i1p53-60.html) (Suchauszug); Bruchwinkel 33–37°: [IRD](https://horizon.documentation.ird.fr/exl-doc/pleins_textes/divers19-08/010048761.pdf) (Suchauszug, schon in `verteilung-fels-organisch.md`).
- Fall-Sortierung (große Blöcke unten), nicht auf allen Kegeln: [JNCC GCR Vol. 33 Mass Movements](https://data.jncc.gov.uk/data/c9bdfe0b-ca6f-4a90-87a6-d03f64e8124c/gcr-v33-mass-movements-c4.pdf) (zitiert Ballantyne & Harris 1994, Suchauszug); [Wegner et al., NHESS 21, 1159 (2021)](https://nhess.copernicus.org/articles/21/1159/2021/).
- Potenzgesetz der Sturzvolumina N = a·V^−b: [Hantz et al. 2017](https://www.isterre.fr/IMG/pdf/hantz_et_al_rocexs2017.pdf), [NPG 16, 179 (2009)](https://npg.copernicus.org/articles/16/179/2009/npg-16-179-2009.pdf) (Suchauszüge). Exponent 2,2 auf die Blocklänge ist meine Spielübersetzung (aus felsgruppen Runde 5), kein Messwert.
- UE 5.7: [Epic, Unreal Engine 5.7 is now available](https://www.unrealengine.com/news/unreal-engine-5-7-is-now-available), [Digital Production](https://digitalproduction.com/2025/11/12/unreal-engine-5-7-foliage-pcg-and-in-editor-ai/), [80.lv](https://80.lv/articles/unreal-engine-5-7-preview-released) (Suchauszüge).
- VSM-Caching und Nanite: [Epic Tech Blog, VSM in Fortnite](https://www.unrealengine.com/en-US/tech-blog/virtual-shadow-maps-in-fortnite-battle-royale-chapter-4) (Suchauszug); Nanite-Streaming-Pool 512 MB: [Guru3D-Forum](https://forums.guru3d.com/posts/6015659/) (Einzelaussage, unbestätigt).
- Witcher-4-Demo (Runtime-GPU-PCG für Kleinzeug, Nanite Foliage): Belege in `antworten/boden-kleinzeug-gras.md` (DF-Interview, PC Gamer, CDPR Press); [CG Magazine](https://www.cgmagonline.com/news/the-witcher-4-tech-demo-state-of-unreal) (Suchauszug).
- ISM/Primitive-Kosten, WP-Hänger: Epic ISM-Doku und Forum, zitiert in `antworten/klippennetze-a5.md`.
- Electric Dreams PCG: [ArtStation Jack M.](https://jackm.artstation.com/projects/DvmwAO) (Suchauszug).
- Projektdaten: Auftrag 21, 16h-N6h + `auftraege/daten/dichte/dichte_vergleich.md`, `vorlagen/daten/sehens/*_2m.png` (Höhe 2 m, 1/64 m), `netze.csv`, `netze_masse.json`, `netz_sperre.json`, `netz_check_ergebnis.json`, `fab_bibliothek_2026-10-13.*`.

## Rückfragen

1. **Front-Achse der Band- und Klippennetze:** `netze_masse.json` kennt keine. Annahme: Schauseite = lokale −Y (`regeln.front_achse_annahme`).
   Bitte in K3 an drei Bändern prüfen. Ist es falsch, `+y`/`+x` eintragen und neu rechnen (1 Zeile).
2. **`remove_foliage_by_mask`:** Stimmt die Semantik „255 = entfernen“? Lassen sich die Typen auf Altbestand-Bäume einschränken (Houdini,
   `FT_EL_WIT_*`, `FT_EL_BST_*`)? Wie viele Bäume entfernt die Maske in B5-Ost? Das brauche ich für die VSM-Bilanz.
3. **Grasdichte:** Gibt es ein Werkzeug, das eine Faktor-Maske in die GT-Dichtekarten multipliziert? Oder sollen wir Geröll-/Fels-Lage höher
   schreiben, damit das Gras über die Gewichtsnormierung zurückgeht?
4. **FS-Schalen im Fenster:** Behalten (Wanddeckung mit Reihen dann über 85 %) oder für den Vorher/Nachher-Vergleich ausblenden?
5. **Kollisionsdeckel 3 000 im Fenster:** Ist es in Ordnung, dass die 255 kleinsten Steine (0,8–1,2 m) keine Kollision haben? Oder wollt ihr einen höheren
   Deckel?
6. **Brockenflut:** Bitte Ferat nach dem Setzen K2 zeigen. Liest das als Halde? Falls nicht: Ist es die Größe (dann Teppich-Skala hoch) oder
   die Anzahl (dann Blockklasse 0,8–1,5 m halbieren)?
7. **Pixelmessung:** Kann Ferats Werkzeug Landschafts-Gras und Akteure getrennt zählen (Netz = Fels + Pflanze, Textur = Landschaft ohne Gras)?
   Und darf die K1-Kamera in C5 stehen (Feld muss geladen sein)?
8. **Variante B** (Schüttkegel): Sollen wir sie verwerfen? Mein Rat: ja.
9. **Megaplants Norway Spruce/Baltic Pine:** Nach dem Laden die Netznamen ins Inventar. Dann tauschen wir die Paletten `baum_mittel`/`baum_hoch`
   aus und messen VSM.
