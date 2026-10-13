# 16h Nachtrag 3 – Teil A und C1 eingebaut, T3 (Tempo), FoamAtten: Parameter liegen in Epic-Funktionen (13.10.2026, 12:35)

## 1. Eingebaut und gespeichert

| Teil | Was | Ergebnis |
|---|---|---|
| **A** Altbett | `sehens_einbau/altbett_p2`, C2 und D2, Lagen und Gras × `gras_dichte_faktor` | Gras-Karten 0 falsch; Bild `bilder/swr_p2/teila_vorher_nachher.jpg`. Sichtbar: am Ufer mehr Moos und Gras; das Kiesfeld im Kiesbett liegt zu großen Teilen im Schutzabstand (15 m) der C3-Bäche und blieb |
| **C1** Kästen | `sehens_einbau/teilc_p2` über `brush_uebernahme.py` (Kern 109 Zellen, 61 m³ Abtrag, max 1,61 m), nur untere Talkaskade | **Prallhänge ausgenommen** (Außenkurve mit Radius < 5 B, eure Regel `prallhang`): s 534–540 links, s 550–556 rechts (R 6,8–16,8 m, Kasten 1,1–2,7 m) bleiben steil. 179 Pflanzen und Steine mit abgesenkt. SWR neu gebacken: Bett 99,9 % nass, Front 783/788. Bild `bilder/swr_p2/teilc1_vorher_nachher.jpg`: kleine Wirkung |
| B.6 | `C2_Flussfels_006/_002` entfernt | Die übrigen 14 und die Klänge sind offen (Fragen in §4) |

**Offen aus C:**
- Die Prallhänge sollen nach eurer Regel ab 1,5 m felsig werden (Erdanriss oben, Blockfuß).
- Dazu C.2 (Lagen nach Neigung), C.3 (Kante) und C.4 (Steine).
- **Frage:** C.2 bis C.4 als Lagen- und Instanz-Plan je Querschnitt? Die Querschnitte habt ihr (`p2_lokal/querschnitte_p2.json`).

## 2. T3 – Tempo der gebackenen Simulation (Dump `sim_tempo`, cm/s)

| Abschnitt | Becken (Plan-Tiefe ≥ 0,6) P10 / Median / P90 | Rinnen (< 0,45) | Stufenfuß (1–3 m unter einer Stufe > 0,3 m) |
|---|---|---|---|
| Bergrinne | – | 47 | 104 / **188** / 664 |
| Durchbruch | 2 / 4 / 40 | 4 / 45 / 116 | 58 / 134 / 200 |
| Talkaskade | – | 153 / **209** / 250 | 63 / 125 / 285 |
| Kiesbett | 13 / 20 / 55 | 60 / 95 / 166 | 40 / 75 / 177 |

Alle nassen Zellen: P50 39, P90 147, P99 609 cm/s.
- Die Becken liegen unter 50 cm/s, wie in 16f erwartet.
- Die Stufenfüße liegen bei 125–188 cm/s (Median). Nur die steilen Stufen der Bergrinne erreichen > 300 cm/s.
- Folge für die Schwelle: Mit 250/450 cm/s gäbe es Schaum fast nur in der Bergrinne und an den schnellsten Stellen der Talkaskade. Die Rinnen
  der Talkaskade (209) sind schneller als ihre Stufenfüße (125).

## 3. FoamAtten (B.4): Die Parameter liegen nicht in unserem Master

Graph von `M_Eldarien_Wasser_Schaum8` gelesen (`antworten/fluss_sim/p2_lokal/master_graph_schaum8.json`: 328 Knoten, 22 Funktionsaufrufe,
45 Parameter):
- **Nicht im Master-Graphen:** `Velocity Debug`, `SimFoam Contrast`, `Foam Opacity`, `Sim Foam Normal`, `Foam Boost`, `MaxFlowVelocity`.
  Sie stecken in Epic-Funktionen, vermutlich:
  - `/Water/Materials/Functions/SampleFluidSimulation` (Ausgänge gehen im Master nur an `WaterOpacityMaskFromDepth`),
  - `/Water/Materials/Layers/WaterAttributes`,
  - `WaterRiverFlowmaps`, `BeachFoam`, `WaveVelocityMask`.
- **Im Master:** `Scattering` (→ Multiply → Add) und unser ELD-Schaum (`ELD_Schaum_Deckkraft` → Lerp → MakeMaterialAttributes), dazu die
  übrigen `ELD_*`-Parameter. `ELD_Strom_*` liest die alte Strömungstextur `T_Eldarien_Wasserfluss`, nicht die SWR.
- Ein Einbau nach B.4 bräuchte also **Kopien von Epic-Funktionen** (Plugin-Inhalt nie ändern) und einen Master `…Schaum9`, der sie aufruft.

**Frage:** Bitte einen konkreten Plan:
1. Welche Funktion wird kopiert, und an welchem Knoten liegt in ihr die dekodierte Geschwindigkeit bzw. der Simulationsschaum?
2. Oder die Steilheits-Alternative: Gibt es im Master eine Normale der gebackenen Fläche? Sonst bräuchte auch sie eine Funktionskopie.
- Ferat wollte am 12.10. keinen Schaum in Bächen („nur an Fällen etwas“), die Fall-FX warten noch. Deshalb hat das keine Eile.

## 4. Kleinkram B.6

- **Übrige 14 Flussfelsen:** Sie sind 1,9–12 m vom p2-Bett entfernt. Größe und Eingrabung messe ich noch.
  - Frage: Bei > 1,5 m entfernen oder versenken (Mittelpunkt −30 % der Höhe)?
- **Klänge:** `C2_Ton_Fluss_01/02/05` liegen 0,3–2,3 m vom Bach.
  - Welche Bach-Klänge aus dem Inventar? (`City_Nature_Sounds` und NatureWaterFX sind da, Liste unter `export/unreal/welt/inventar/`.)
  - Bis dahin würde ich die Lautstärke auf 40 % senken.

## 5. Mündung

Bild `bilder/swr_p2/muendung.jpg`. p2 läuft durch das Kiesfeld in einen kleinen Wasserspiegel des C3-Laufs. Eine „Glaswand“ ist nicht zu sehen.
Der C3-Lauf ist dort aber nur ein Tümpel in einem breiten Schotterbett. Das passt zu eurem Plan, `F_ERLENBACH` ab C3 neu zu backen.
