# Antwort zur 16f-Rückfrage – Epic „Baked River Simulations – Parameter Reference“ (lokal gelesen)

Stand 12.10.2026. Grundlage sind Ferats lokale Zusammenfassung der Epic-Seite
(`auftraege/16f-rueckfrage-epic-parameter-lokal.md`, gelesen 12.10.2026, 23:40) und unsere bisherigen Empfehlungen:
- 16f Teil A, Abschnitt 4: Befund 7 und Testmatrix;
- 16e: Schaum aus, Option-B-Maske, Tempo nach Gefälle;
- 16b und 16c: C2-Strecke, Zelle und Auflösung;
- `skripte/fluss_sim/`.

Die Epic-Seite ist aus der Cloud weiter gesperrt. **Ferats Zusammenfassung gilt hier als Primärquelle.**

**Kennzeichnung:**
- [Epic lokal]: Ferats Zusammenfassung der Epic-Seite
- [Projekt]: eigene Daten, Messungen und Antworten
- [Ableitung]: aus beidem geschlossen
- [unsicher]: Wert oder Einheit nicht belegt; im Test klären

## Kurzfazit

- **Befund 7 ist erklärt.** `match_spline_height_amount` ist eine **Nachfüllrate**. Die Simulation füllt dort Wasser nach, wo sie
  unter dem Spline-Spiegel liegt [Epic lokal].
  - Mit 2 hat sie das ganze Spline-Band bis zum Spiegel aufgefüllt. Unsere Deutung in 16f 4.2 („zieht zur Spline“) war
    also richtig, nur der Hebel lag im falschen Feld.
  - **Neu:** `match_spline` **an** (bool), `match_spline_height_amount` **0,02** (Test 0 / 0,02 / 0,05),
    `remove_outside_spline_amount` **50**, `source_size` = Bachbreite an der Quelle (Test 300 / 1000 cm).
  - Diese Werte stehen jetzt je SWR im Export (Regeln v8, Commit `7ee1900`).
- **Die Auflösung bleibt nach Zielzelle** (Bach 0,25 m, Fluss 0,35 m, höchstens 2048).
  - Epics „ideal ≥ 1024“ gilt für eine feste Fläche. Bei uns haben 151 von 199 SWR kleine Rechtecke (Achse < 256 m) und
    schon heute 0,25 m Zelle.
  - Ein Mindestwert von 1024 gäbe dort Zellen von im Median 0,10 m und 1,8-mal so viele Zellen (80 → 144 Mio.). Das kostet
    Backzeit ohne sichtbaren Nutzen.
  - C2 liegt im Export in `F_ERLENBACH_T00` mit 1856 Zellen und 0,247 m, also schon über 1024. Der lokale Test-Akteur
    `SWR_C2` sollte 1024 bekommen (0,17 m statt 0,33 m).
- **Schaum nach Ferats Wunsch** (kein Schaum im Bach, nur an Fällen) geht jetzt **mit Epics eigenen Reglern**, ohne Umbau des
  Masters:
  - Material: `FoamAttenMin` / `FoamAttenMax` = **2,5 / 4,5 m/s**, `LowVelocityFoamScale` = **0**.
  - Niagara-Kopie: Weißwasser nur in schnellem, tiefem Wasser (`Restrict Emission Speed Range` ab 3 m/s,
    `Restrict Emission Depth Range` ab 0,15 m).
  - Die Einheit der Regler ist unbekannt (m/s, cm/s oder normiert). Ein Einheitentest mit dem Render State „Debug Foam“
    klärt sie in 10 Minuten (Abschnitt 3.3).
- **Die Option-B-Maske aus 16e wird optional.**
  - `FoamAtten` lässt Schaum an allen Fallfüßen ab etwa 1 m zu. Die Maske deckte nur die 170 Vorhang-Fälle ab.
  - Die Maske bleibt im Export als Rückfall, falls steile Rinnen ohne Fall noch schäumen.
- **Tempo:** Epic bestätigt, dass `Speed` nur das Einschwingen beschleunigt (Substeps ≥ Speed). Test V1 aus 16e entfällt.
  - Gegen „zu schnell“ in der gebackenen Strömung wirken **Friction** und **Velocity Dissipation** in der Niagara-Kopie.
    Start: je Standard × 2 bzw. × 1,5. Danach **neu backen**.
- **Hindernisse:** Der Export filterte schon bei 0,4 m. Er maß aber die gedrehte Welt-Box im Grundriss, und schräg liegende
  0,3-m-Steine kamen so darüber.
  - **Neu:** größte Ausdehnung des Netzes × Skala ≥ 0,4 m (Ferat: „Steine ≥ 0,4 m eintragen“).
  - Eindeutige Objekte: 42 285 → **40 980**. 1 323 kleine Felsen und Steinpackungen fallen weg, 18 lange bzw. hohe Objekte
    kommen dazu.
  - Instanzen in den `WH_`-Akteuren: 41 251 → **39 946**.
- **Fingerabdrücke:** 149 von 199 SWR ändern sich, nur im Objektteil. Gelände und Splines bleiben gleich.
  - Die neuen SWR-Werte stehen **nicht** im Fingerabdruck. Die Back-Liste nennt sie je SWR unter `sim_vorgaben`.
  - Gebacken ist außer den C2-Tests noch nichts. Deshalb einfach mit den neuen Werten bauen.
- **Prüfer:** 0 FEHLER, 0 WARNUNG, 70 HINWEIS. Zwei Läufe sind byte-gleich (183 Dateien). Alle 6 neuen Gegenproben ergeben
  FEHLER.

## 1. Befund 7 – Wasser füllt das ganze Spline-Band

### 1.1 Was die Felder laut Epic tun [Epic lokal]

| Feld (Python) | Bedeutung | bei uns bisher | **neu** |
|---|---|---|---|
| `match_spline` (bool) | schaltet den künstlichen Abgleich der Simulation an die Spline ein oder aus; kann unrealistisch wirken | an | **an** (nur als Überlauf-Schutz) |
| `match_spline_height_amount` | **Rate**, mit der Wasser nachgefüllt wird, wo die Simulation unter der Spline-Höhe liegt (Niagara „Add Water To Match Spline Rate“); gedacht für Flüsse, die Volumen verlieren | **2** | **0,02** (Test 0 / 0,02 / 0,05) |
| `remove_outside_spline_amount` | Rate, mit der Wasser außerhalb der Spline entfernt wird (Niagara „Remove Water Outside Spline Rate“) | 50 | **50** |
| `source_size` | Größe des Bereichs, aus dem an der Quelle Wasser austritt; „Standard meist gut“ | 10 m | **Bachbreite an der Quelle**; Test 300 / 1000 cm |
| `resolution_max_axis` | Zellen auf der längsten Achse; „so hoch wie das Budget erlaubt, ideal ≥ 1024“ | nach Zielzelle | **nach Zielzelle** (Abschnitt 2) |
| `sim_speed` / `num_steps` | Tempo-Multiplikator zum schnelleren Einschwingen; Substeps ≥ Speed | 10 / 10 | **10 / 10** |
| Smoothing Width / Cutoff | glättet die Oberflächen-Verschiebung an harten Kanten | Standard | bei Treppen-Artefakten erhöhen |
| Reset / Bake | Reset baut neu auf und startet Live Sim; Bake schreibt in Texturen | – | **Reset nach jeder Gelände- oder Kollisionsänderung** |

**Ursache Befund 7 [Ableitung]:**
- Mit einer Rate von 2 ersetzt die Simulation jedes Defizit unter dem Spline-Spiegel fast sofort.
- Das Wasser steht deshalb überall auf Spline-Höhe, auch über den Rampen und Rändern, wo das Bett schmaler oder flacher ist
  als das Band.
- Dazu kommt die Breite: Die Spline-Breite liegt an C2 in den 2-m-Daten bei 13–28 m (Median 21 m). Die wasserführende Rinne
  ist viel schmaler (Ferat: 3 m) [Projekt].
- Ergebnis: 99,7 % der Fläche nass, Tiefe im Median 1,25 m (Befund 7).

### 1.2 Startwerte (im Export, `swr.sim_vorgaben`, Regeln v8)

| Feld im Export (`swr_bereiche[].swr`) | Wert | Herkunft |
|---|---|---|
| `match_spline` | `true` (auch für die 5 geteilten Gewässer; bis v7 dort „lokal testen“) | Epic: Abgleich an/aus, nicht der Bereich |
| `match_spline_height_amount` | **0,02** | Mitte der Testreihe 0 … 0,05: füllt Verdunstungs- und Randverluste nach, aber kein Band |
| `remove_outside_spline_amount` | **50** | Netz gegen Überlaufen (16f 4.3) |
| `source_size_cm` | `RiverWidth` des ersten Splinepunkts des SWR-Bereichs | Bachbreite an der Quelle; bei Teilstücken die Breite am Anfang des Stücks |
| `sim_speed` / `num_steps` | 10 / 10 | Epic: Substeps ≥ Speed |
| `resolution_max_axis` | wie bisher: ⌈Achse / Zielzelle / 32⌉ × 32, höchstens 2048 | Abschnitt 2 |

- **`source_size_cm` im 2-m-Lauf:**
  - Median 4,0 m, 10.–90. Perzentil 2,8–19,4 m.
  - Verteilung: 104 SWR bei 2–4 m, 47 bei 4–6 m, 20 über 20 m (Flüsse und Teilstücke, bis 78,6 m bei `F_HAUPTFLUSS_3_T03`).
  - `F_ERLENBACH_T00` beginnt im Roh-Stück aus den Weltdaten und bekommt deshalb 33 m. Das ist für C2 nicht aussagekräftig.
    Den Test-Akteur `SWR_C2` testet ihr mit 300 und 1000 cm (Rückfrage 1).
- **Prüfer:** Er meldet FEHLER, wenn ein Feld von der Vorgabe abweicht. Außerdem bei `num_steps` < `sim_speed`, bei
  `source_size_cm` ≠ Breite am ersten Punkt und wenn `sim_vorgaben` in der Back-Liste ≠ SWR.

### 1.3 Testreihe Befund 7 (C2, Test-Akteur `SWR_C2`)

Alle Varianten mit `match_spline` an und `remove_outside_spline_amount` 50, zuerst bei der bisherigen Auflösung (512), damit
sie mit Befund 7 vergleichbar sind.

| Lauf | `match_spline_height_amount` | `source_size` | Erwartung |
|---|---|---|---|
| B7-1 | 2 (Referenz) | 1000 cm | Band voll, wie Befund 7 |
| B7-2 | 0 | 300 cm | Wasser nur aus der Quelle. Kann zum Ende hin dünn werden, wenn das Bett Volumen verliert |
| **B7-3** | **0,02** | **300 cm** | **Start:** Bett gefüllt, Band außerhalb trocken |
| B7-4 | 0,05 | 300 cm | etwas voller; Rückfall, falls B7-3 zum Ende hin austrocknet |
| B7-5 | bester aus B7-2…4 | 1000 cm | zeigt, ob eine breite Quelle am Anfang die Ränder flutet |

- **Ablauf je Lauf:** Wert setzen, **Reset**, einlaufen lassen (Pegel ändert sich < 1 cm in 10 s), dann Bake und Render State
  `Water Component With Baked Sim`.
- **Messgrößen** (wie 16f 4.3):
  - Anteil nasser Zellen im Bett (Gelände < Planspiegel − 5 cm) ≥ 95 %;
  - nasse Zellen im Band außerhalb des Betts ≤ 5 %;
  - Tiefe im Median gegen Plan: Becken ± 0,2 m, Rinnen ± 0,1 m.
- **Prüfbilder:** Draufsicht C2 (Render State `Baked Sim`, genaueste Ansicht), `kn0_unten`, `kn0_nah_s119`.
- **Python** (Namen laut Ferats Zusammenfassung):

```python
import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
swr = next(a for a in eas.get_all_level_actors() if a.get_actor_label() == 'SWR_C2')
c = swr.get_component_by_class(unreal.ShallowWaterRiverComponent)
for n, v in (('match_spline', True), ('match_spline_height_amount', 0.02),
             ('remove_outside_spline_amount', 50.0), ('source_size', 300.0)):
    c.set_editor_property(n, v)
    print(n, c.get_editor_property(n))
# danach Reset im Details-Panel (bzw. die Reset-Funktion der Komponente), einlaufen lassen, Bake
```

- **Spline-Breite:** In 16f 4.3 stand „RiverWidth = Bett + 2 m“. Das ist jetzt **nachrangig**. Mit kleiner Nachfüllrate
  füllt die Simulation das Band nicht mehr auf, auch wenn es breiter ist als das Bett.
  - Nur wenn `remove_outside_spline_amount` sichtbar Wasser am Bettrand abschneidet, die Breite um 2 m erhöhen.
  - Der Export bleibt dafür unverändert.

## 2. Auflösung: Epic empfiehlt ≥ 1024

**Unsere Regel (16c, 16e):** Die Auflösung folgt der Zielzelle. Für die Darstellung zählt die Zellgröße, nicht die Zahl.

| | heute (Regel v8 = v7) | Mindestens 1024 | Bach-Zielzelle 0,20 m |
|---|---|---|---|
| SWR < 512 / 512–1023 / ≥ 1024 | 87 / 64 / 48 | 0 / 0 / 199 | – |
| SWR mit 2048 | 17 | 17 | 25 |
| Zellen gesamt | **80 Mio.** | 144 Mio. (× 1,8) | 101 Mio. (× 1,26) |
| Zelle der heute < 1024 | 0,25 m (Bach) | Median 0,10 m, bis 0,01 m | 0,20 m |

**Kosten** [Projekt, Test 16c an C2, live im Editor]:

| Auflösung | Kosten je Bild |
|---|---|
| 512 | 0,8 ms |
| 1024 | 6,3 ms |
| 2048 | 9,7 ms |

- Die 2048-Variante war nach 45 s noch nicht eingelaufen.
- Gebacken kostet eine SWR im Spiel ≈ 0,2 ms, unabhängig von der Auflösung.
- **Die Kosten fallen also beim Backen an.** Feinere Zellen brauchen zusätzlich mehr Schritte bis zum Ruhezustand
  [Ableitung]. Zwischen 512 und 1024 ist je SWR mit dem 8- bis 15-fachen der Backzeit zu rechnen.

**Bewertung:**
- Epics „≥ 1024“ ist eine Faustregel für eine Fläche mit fester Größe [Ableitung]. Bei 128-m-Rechtecken und 0,25 m sind 512
  Zellen genau richtig. 1024 gäbe 0,125 m. Das ist feiner als die Hindernisse (≥ 0,4 m) und als das 1-m-Gelände.
- An C2 liegt die Export-SWR schon über 1024 (1856 Zellen, 0,247 m). Euer Bild `c2_aufloesung_512_1024_2048.jpg` zeigte bei
  1024 vor allem **feineren Schaum** (16c). Mit Schaum fast überall aus zählt das weniger.
- **Empfehlung:**
  - Regel lassen.
  - `SWR_C2` im Test auf **1024** stellen, als Vergleich zur Export-SWR (0,247 m). Dabei Backzeit und Einlaufzeit messen
    (Testreihe T3).
  - Sieht 1024 (0,17 m) an Lippen und Fallfüßen deutlich besser aus als 0,25 m, auf die Variante „Bach 0,20 m“ gehen
    (eine Zahl in den Regeln, 101 Mio. Zellen).

## 3. Schaum: kein Schaum im Bach, nur an Fällen

### 3.1 Bezug zum Tempo (16e)

**Spline-Tempo** nach der `tempo_ms`-Regel (16e, mittlere Geschwindigkeit) [Projekt]:

| Strecke | Tempo |
|---|---|
| Becken | ≈ 0,2 m/s (p10–p90 0,13–0,29) |
| Lippen und Füße | ≈ 1,2 m/s |
| steile Rinnen | 1–2,5 m/s (Kappe 2,5) |

**Gebackene Strömung** [Ableitung]:
- Sie ist eine eigene Rechnung. In einer 2D-Simulation ist ein Absturz eine steile Rinne über 1–2 Zellen.
- Am Fallfuß erreicht das Wasser einen Teil der Fallgeschwindigkeit v = √(2 g h):

  | Fallhöhe | v = √(2 g h) |
  |---|---|
  | 1 m | 4,4 m/s |
  | 1,5 m | 5,4 m/s |
  | 2 m | 6,3 m/s |
  | 3 m | 7,7 m/s |

**Folgerung für die Schwelle:**
- **Unter 2,5 m/s** (alles, was die Tempo-Regel für Becken und Rinnen vorsieht): **kein Schaum**.
- **Ab etwa 4,5 m/s** (Fallfuß ab ≈ 1 m, unsere `fall_schwelle_m`): **voller Schaum**.
- Dazwischen weicher Übergang: Die steilsten Rinnen und kleine Fälle schäumen leicht.

### 3.2 Material (`MI_EL_SWR_Klar` bzw. Baked Sim Material)

| Parameter | 16e (Schaum aus) | **neu** | Begründung |
|---|---|---|---|
| `FoamAttenMin` | – | **2,5 m/s** | darunter kein Schaum [Epic lokal]; = Kappe der Tempo-Regel |
| `FoamAttenMax` | – | **4,5 m/s** | ab hier voller Schaum; ≈ Fallfuß 1 m |
| `LowVelocityFoamScale` | – | **0** | kein Schaum in langsamem Wasser (Becken, Kehrwasser) |
| `Foam Opacity` | 0 | **0,6** (Wert vor 16e) | Der Schaum ist wieder erlaubt, die Geschwindigkeit begrenzt ihn |
| `Foam Boost` / `Foam powr` | 0 / 0,6 | **0,45 / 1,5** (16b) | dünner, ausgefranster Fallschaum |
| `Sim Foam Normal` | 0 | **0,5** | leichte Beulen nur dort, wo Schaum ist |
| `ELD_Strom_Schaum`, `ELD_Fels_Schaum`, `ELD_DF_Schaum`, `ELD_Ufer_Schaum`, `ELD_Schaum_Deckkraft` | 0 | **0 lassen** | unsere eigenen Schaumquellen hängen nicht an `FoamAtten` |

**Einheiten [unsicher]:** Die Werte oben sind in m/s angegeben. Je nach Einheit des Materials gilt:

| Einheit des Materials | `FoamAttenMin` / `FoamAttenMax` |
|---|---|
| cm/s (UE-Einheit) | **250 / 450** |
| normiert auf `MaxFlowVelocity` 1024 cm/s | **0,244 / 0,44** |

Die Einheit klärt der Test in 3.3.

### 3.3 Einheitentest mit „Debug Foam“ (10 min, C2, kein neues Backen)

1. Render State `Debug Foam` an `SWR_C2`. Das zeigt den gebackenen Schaum der Simulation, ohne Material-Dämpfung
   [vermutlich].
   - Bild 1: Draufsicht C2.
   - Wo die Simulation Schaum erzeugt, bestimmen Niagara (3.4) und das Backen, nicht `FoamAtten`.
2. Zurück auf `Water Component With Baked Sim`. `FoamAttenMin` = **1**, `FoamAttenMax` = **2**, `LowVelocityFoamScale` 0. Dann
   Bild 2.
   - **Becken frei, Rinnen und Fallfüße weiß:** Die Einheit ist **m/s**.
   - **Fast alles wie Bild 1** (kaum gedämpft): Die Einheit ist **cm/s**. Gegenprobe mit 100 / 200, das muss wie „m/s“
     aussehen.
   - **Gar kein Schaum mehr:** Der Wert ist **normiert** (1 = 1024 cm/s). Gegenprobe mit 0,1 / 0,2.
3. Dann die Startwerte aus 3.2 in der gefundenen Einheit setzen. Bild 3: `kn0_unten`, `kn0_nah_s119` und Fallfuß S04.
   - Erwartung: Schaum nur am Fuß von S04/S05 und in den steilsten Rinnen; Becken klar.
4. Mit `Velocity Debug` = 1 in WCBS die gebackene Geschwindigkeit an einer Rinne und an einem Fallfuß ablesen. Liegen die
   Rinnen schon über 2,5 m/s, `FoamAttenMin` auf 3,0 m/s heben.

### 3.4 Niagara-Kopie (`NS_EL_SW_River`, Kopie von `Grid2D_SW_River`; nur die Kopie ändern)

Die Standardwerte der Kopie sind uns unbekannt. Deshalb stehen hier Faktoren auf den Standard bzw. Grenzen in m/s und m.
Bitte den Standard vorher notieren.

| Regler | **Start** | Begründung |
|---|---|---|
| **Restrict Emission Speed Range** | **an**, ab **3,0 m/s** (cm/s: 300) | kein Weißwasser unter der Rinnen-Kappe; Fallfüße liegen bei 4–8 m/s |
| **Restrict Emission Depth Range** | **an**, ab **0,15 m** (cm: 15) | kein Weißwasser in dünnen Rinnen; ersetzt die Idee `Sim Foam Depth Min` 15–25 cm aus 16f 4.3 |
| Depth-Difference Mult | Standard × **1,5** | Höhenunterschied = Absturz; der gewünschte Schaumort |
| Velocity Mult | Standard | wirkt schon über die Speed-Grenze |
| Curvature Mult | Standard × **0,5** | weniger Schaum an Wellenkämmen in Rinnen |
| Vorticity Mult | Standard × **0,25** | weniger Schaum in Kehrwasser und an Steinen |
| Dissipation Rate | Standard × **2** | Schaum zerfällt nach etwa 3–6 m, wie der Aufprallteppich (16e: Kapsel ≤ 6 m) |
| **Sekundär-Emitter (Gischt)** | **aus** (wie 16e); Variante: an mit Speed ab **4,5 m/s** und Depth ab 0,2 m | Gischt an Fällen liefern die Nature-Water-FX (`NS_Impact_*`). Nicht beides, sonst doppelte Gischt |

- **Neu backen: ja.** Die Emission läuft beim Backen. Danach Bild mit `Debug Foam`; erwartet sind Flecken nur an den
  Fallfüßen.
- Die Einheit der Niagara-Grenzen ist ebenfalls [unsicher]. Niagara Fluids rechnet in UE-Einheiten (cm, cm/s). Wenn die
  Speed-Grenze in m/s gedacht ist, entsteht gar kein Schaum mehr; dann 3,0 statt 300 eintragen.

### 3.5 Option-B-Maske (16e) – noch nötig?

| | `FoamAtten` + Niagara-Grenzen | Option-B-Maske |
|---|---|---|
| wo Schaum | jedes Wasser über ≈ 2,5–4,5 m/s: Fallfüße ab ≈ 1 m (762 Fälle) und die steilsten Rinnen | nur in Kapseln an den 170 Vorhang-Fällen |
| Aufwand | Werte im MI und in der Niagara-Kopie | Master-Umbau, 16 Slots, Kind-MI je Gewässer |
| Risiko | steile Rinnen ohne Fall schäumen leicht | 592 Fälle von 1–3 m ganz ohne Schaum |

**Empfehlung:**
1. Zuerst **nur `FoamAtten` + Niagara-Grenzen**. Das trifft „Schaum nur an Fällen“ genauer als die Maske, weil auch kleine
   Fälle einen Fuß haben, und es braucht keinen Master-Umbau.
2. Die **Maske nur, wenn** die Bilder aus 3.3/3.4 in Rinnen ohne Fall noch Schaum zeigen. Dann **beides**:
   Schaum = Simulationsschaum × `FoamAtten` × Maske.
   - Die Maske müsste dann auch die Fälle von 1–3 m abdecken (mehr Slots oder eine Maskentextur je Gewässer). Bitte erst nach
     den Bildern entscheiden.
3. Der Export behält `schaum_maske` unverändert (170 Kapseln).

## 4. Wellen und Trübung (klares Bachwasser)

| Parameter | **Start** | Begründung |
|---|---|---|
| Scattering Min Velocity / Max Velocity (Velocity Scattering) | **1,5 / 4,0 m/s** | Becken und normale Rinnen bleiben klar; nur Fallfüße werden milchig (Luftbläschen) |
| Low Velocity Wave Scale | **0,2** | Becken fast glatt: Der Grund bleibt sichtbar |
| Wave Atten Min / Max | **0,3 / 1,5 m/s** | Riffel wachsen von Becken zu Rinne; ab 1,5 m/s volle Wellen |
| WPO-Wellen | Amplitude **halbieren**, bei Bächen ≤ 2 cm | Displacement ist in WCBS gröber [Epic lokal]; große WPO-Wellen zeigen auf 0,25-m-Zellen Treppen |
| Absorption / Scattering (globale Vektorparameter) | (0,45; 0,10; 0,08) / (0,002; 0,004; 0,004) je m (16f 5.2) | einmal global; Moor und Wolfsschlucht dunkler über Kind-MI |

- Die Einheiten sind wie bei `FoamAtten` [unsicher]. Es gilt dieselbe Einheit, die der Test 3.3 ergibt.
- Neu backen ist nicht nötig, das sind reine Material-Werte.

## 5. Tempo: Niagara Friction und Velocity Dissipation

| Regler (Niagara-Kopie) | **Start** | Testreihe | neu backen |
|---|---|---|---|
| Friction | Standard × **2** | × 1,5 / × 2 / × 3 | **ja** (Reset + Bake) |
| Velocity Dissipation | Standard × **1,5** | × 1 / × 1,5 / × 2 | **ja** |
| Smoothing Width (Niagara und SWR) | Standard | nur bei Treppen-Artefakten erhöhen | ja |
| `sim_speed` / `num_steps` | 10 / 10 | – | – |

- **Zuerst die Material-Werte aus 16e** (`Simulation Flowmap Speed` 0,5, `SIm Flowmap Speed` 1,0). Sie brauchen kein neues
  Backen.
- **Erst wenn die gebackene Strömung selbst zu schnell ist**, kommt Friction dazu. Prüfen mit `Velocity Debug` in WCBS;
  zu schnell heißt Becken > 0,3 m/s oder Rinnen > 2,5 m/s.
- **Friction bremst vor allem flaches Wasser** [Epic lokal]. Langsameres Wasser steht tiefer (Kontinuität) [Ableitung].
  Nach einer Friction-Änderung deshalb die Messgrößen aus 1.3 noch einmal prüfen.
- **`sim_speed`:** Epic bestätigt die Vermutung aus 16e: `Speed` lässt die Simulation nur schneller einschwingen. LIVE_SIM
  wirkt deshalb zu schnell. Tempo nur in WCBS bzw. PIE beurteilen. Test V1 aus 16e entfällt.

## 6. Hindernisse: Use Capture, Bottom Contour, Dilation

**Epic** [Epic lokal]:
- `Use Capture` erfasst Hindernisse per Szenen-Capture als Tiefenkarte. Dazu kommen Bottom Contour Actors/Tags und
  Capture Offset.
- Dilated Bottom Contour Actors/Tags + Collision Dilation vergrößern Hindernisse, wenn Wasser durch Geometrie läuft.
- Nach jeder Gelände- oder Kollisionsänderung: Reset.

**Unser Export** (bisher und weiter):
- `use_capture` true, Tag `SWR_Hindernis`, `bottom_contour_actors` = die `WH_`-Akteure im Bereich.
- `wasser_kollision` nur für feste Objekte (Fels, Holz, Kollision im Plan; nie Pflanzen) im Wasser oder ≤ 1 m daneben.
- Überspannende Objekte bleiben ohne Kollision.

### 6.1 Mindestgröße 0,4 m (Regeln v8)

**Befund:** Der Export filterte schon (`min_ausdehnung_m` 0,4, `min_hoehe_m` 0,2). Gemessen wurde aber die größte Seite der
**gedrehten Welt-Box im Grundriss**. Ein schräg liegender 0,3-m-Stein hat eine Welt-Box von bis zu 0,42 m und kam so über
die Grenze.

**Neue Regel:**
- **Größte Ausdehnung** = max über x, y, z von (Netz-Bounds max − min) × |Skala|, ohne Drehung. Sie muss ≥ **0,4 m** sein.
  - Bounds aus `netze_masse.json`, sonst `netze.csv`.
  - Die Höhe der Welt-Box muss wie bisher ≥ 0,2 m sein (Kies, Steinpackungen, flache Platten bleiben ohne).
- Kleinere Objekte bekommen **keine** `wasser_kollision` und stehen in **keinem** `WH_`-Akteur.
- Neues Feld `ausdehnung_m` je Kollisionseintrag.

| 2-m-Lauf | vorher (v7) | **nachher (v8)** |
|---|---|---|
| Pool fest und groß genug | 102 338 | **99 581** |
| Kollisionseinträge | 42 542 | **41 235** |
| eindeutige Objekte (= in `WH_`) | 42 285 | **40 980** (−1 323 Fels, +11 Fels, +7 Holz) |
| davon im Wasser | 37 081 | **35 959** |
| überspannt (ohne Kollision) | 7 103 | **6 863** |
| Instanzen in `WH_` (HISM) / Akteure mit Tag | 41 251 / 1 034 | **39 946** / 1 034 |
| `WH_`-Akteure | 197 | 197 |
| Kehrwasser-Schaumobjekte (Lee von Randblöcken) | 317 | 316 |

- **Weggefallen:** `SM_mountain_rock_small_01_*` (707), `SM_NordicBeachRock_01` (104), `SM_SmallStonesPack_*` (≈ 370) und
  weitere kleine Felsen. Ihre alte Welt-Box im Grundriss war 0,40–0,62 m (Median 0,46 m), ihre echte Größe < 0,4 m.
- **Neu dazu (18):** lange Äste und hohe Felsen (`SM_Big_Rock_03`, `SM_ForestRockShelf_*`, `SM_mountain_branch_01_02`).
  Ihre Welt-Box war im Grundriss < 0,4 m, sie selbst sind länger oder höher.
- **Größte Abnahmen je `WH_`:**

  | `WH_` | vorher | nachher |
  |---|---|---|
  | `B_R_M2_P1_01` | 1 035 | 888 |
  | `B_K1_WASSERFALL_WEST_01` | 875 | 759 |
  | `B_K1_WASSERFALL_WEST_03` | 984 | 893 |

- **F_ERLENBACH:** 1 026 → 1 015 Einträge. C2-Ebene 609 → 605. `WH_F_ERLENBACH_T00`: 708 → 701 Instanzen.
- **Lokal:** Das Bau-Werkzeug setzt die Regel auf alle Ebenen im SWR-Bereich an, auch Bestand und Felsgruppen. Maßgeblich ist
  dieselbe Formel: Bounds × Skala, ohne Drehung.

### 6.2 Dilation und Capture

- **Start ohne Dilation.** Bei 0,25 m Zelle ist ein 0,4-m-Stein etwa 1,6 Zellen groß. Das reicht für die Tiefenkarte.
- **Prüfbild:** Render State `Debug Bottom Contour`. Alle Steine ≥ 0,4 m und Stämme müssen als Erhebung sichtbar sein.
- **Läuft Wasser durch dünne Stämme oder Äste** (Ø < 0,3 m, quer zur Strömung): diese Holz-Komponenten des `WH_`-Akteurs als
  **Dilated Bottom Contour Actors** eintragen und `Collision Dilation` = 1 Zelle (25 cm). Felsen nicht dilatieren, sonst
  werden Rinnen zu eng.
  - Wenn das hilft, gibt der Export die Holz-Komponenten als eigenes Feld aus (Rückfrage 3).
- **`Capture Offset`:** Standard lassen. Nur wenn die gebackene Fläche gegen die Spline versetzt liegt (5.6-Fehler mit
  `use_capture`, 16f 4.3), hier zuerst ansehen.

## 7. Alte Empfehlung → neue Empfehlung

| Thema | alt (16b/16c/16e/16f) | **neu** | neu backen |
|---|---|---|---|
| `match_spline` | 16f: „1 bzw. nur Lage“, Test 0/1/2; 16c: bei Teilstücken „lokal testen“ (vermutet: Bereich) | **an** (bool), überall; regelt nur den Spline-Abgleich | ja |
| `match_spline_height_amount` | 16f: 0,05 (Test 0/0,05/0,15/0,3); lokal 2 | **0,02** (Test 0/0,02/0,05); Nachfüllrate | ja |
| `remove_outside_spline(_amount)` | 50, Test 20/50/200 | **50**, keine Testreihe nötig | – |
| `source_size` | Bachbreite, Test 2/4/10 m | **= Bachbreite an der Quelle** (Export `source_size_cm`); Test 300/1000 cm | ja |
| Spline `RiverWidth` | Bett + 2 m | **Plan lassen**; + 2 m nur, wenn der Rand abgeschnitten wird | ja |
| `resolution_max_axis` | nach Zielzelle 0,25/0,35 m, ≤ 2048 | **bleibt**; kein Mindestwert 1024; `SWR_C2`-Test mit 1024 | ja |
| `sim_speed` / `num_steps` | 10/10, „Zeitraffer [vermutlich]“, Test V1 | **10/10 bestätigt**, V1 entfällt | – |
| Schaum im Material | `Foam Opacity` 0, `Foam Boost` 0, `Sim Foam Normal` 0, `ELD_*` 0 | **`FoamAttenMin`/`Max` 2,5/4,5 m/s, `LowVelocityFoamScale` 0**, `Foam Opacity` 0,6, `Foam Boost` 0,45, `ELD_*` 0 | nein |
| `Sim Foam Depth Min` | 16f: 8 → 15–25 cm | ersetzt durch **Restrict Emission Depth Range** ab 0,15 m in Niagara | ja |
| Weißwasser in Niagara | Name unbelegt | **Restrict Emission Speed Range** ab 3 m/s; Depth-Difference × 1,5, Curvature × 0,5, Vorticity × 0,25, Dissipation × 2 | ja |
| Sekundär-Emitter | aus (16e) | **aus**; Variante mit Speed ab 4,5 m/s | wahrscheinlich nein |
| Option-B-Maske | Empfehlung (16e) | **optional**, nur wenn Rinnen ohne Fall schäumen; dann Maske × `FoamAtten` | nein |
| Tempo | Flowmap 0,5/1,0; Niagara-Reibung „Name unbelegt“ | Flowmap zuerst; dann **Friction × 2, Velocity Dissipation × 1,5** | ja |
| Trübung | Scattering × 5 in Schnellen über die Geschwindigkeit (16f 5.2) | **Velocity Scattering 1,5/4,0 m/s** | nein |
| Wellen | `Sim Velocity Normal Strength` 15 (16e) | dazu **Low Velocity Wave Scale 0,2, Wave Atten 0,3/1,5 m/s**, WPO halbiert | nein |
| Hindernisse | Grundriss der Welt-Box ≥ 0,4 m, Höhe ≥ 0,2 m | **größte Ausdehnung inkl. Skala ≥ 0,4 m**, Höhe ≥ 0,2 m; Dilation nur bei Durchlaufen | ja (149 SWR) |
| Prüfansichten | WCBS, `Velocity Debug` | dazu **`Debug Foam`, `Debug Bottom Contour`, `Baked Sim`** | – |

## 8. Testreihe lokal (in dieser Reihenfolge)

| Schritt | Was | Prüfbild / Messung | neu backen |
|---|---|---|---|
| T0 | `git pull`; Export und Prüfer auf 1 m (Befehle in `skripte/fluss_sim/README.md`); Feldnamen am `SWR_C2` lesen (`get_editor_property` für die Felder aus 1.2) | Prüfer 0 FEHLER; Liste der Feldnamen | – |
| T1 | Befund 7: B7-1 … B7-4 (Abschnitt 1.3), 512 | Draufsicht `Baked Sim`, `kn0_unten`; nasse Zellen im Bett / im Band, Tiefe | je Lauf |
| T2 | `source_size` 300 vs. 1000 cm mit dem besten Wert aus T1 (B7-5) | Draufsicht Quelle; Rand am Anfang nass? | je Lauf |
| T3 | Auflösung 512 → 1024 mit T1/T2-Werten | `kn0_nah_s119`, Fallfuß S04; Einlaufzeit, Backzeit, Texturgröße | ja |
| T4 | Hindernisse: `Debug Bottom Contour`; bei Durchlaufen Dilation für Holz | Bild Draufsicht; Steine ≥ 0,4 m sichtbar, Stämme dicht | ja, wenn geändert |
| T5 | Material-Einheitentest (3.3), dann `FoamAtten` 2,5/4,5 m/s, `LowVelocityFoamScale` 0, `Foam Opacity` 0,6 | Bilder 1–3 aus 3.3; `Velocity Debug` an Rinne und Fallfuß | nein |
| T6 | Niagara-Kopie `NS_EL_SW_River`: Restrict Speed/Depth, Mults, Dissipation, Sekundär aus (3.4); Kopie in den Projekteinstellungen eintragen | `Debug Foam` Draufsicht; WCBS `kn0_unten` | ja |
| T7 | Tempo: `Velocity Debug`; nur bei Becken > 0,3 / Rinnen > 2,5 m/s Friction × 2, Dissipation × 1,5 | Werte an 3 Becken und 3 Rinnen; Messgrößen aus T1 wiederholen | ja |
| T8 | Wellen und Trübung (Abschnitt 4) | Becken 1,5 m tief: Grund bei 1 m deutlich, bei 2,5 m Umrisse; Rinne mit Riffeln | nein |
| T9 | Entscheidung Option-B-Maske (3.5) | Rinnen ohne Fall: Schaum ja/nein | nein |

Bitte nach T1, T3, T5 und T6 die Bilder schicken. Nach T1 lohnt sich ein kurzer Bescheid, welcher Wert gewinnt; die Zahl in
`swr.sim_vorgaben` ändere ich dann im Export.

## 9. Export, Prüfer und Lauf (Regeln v8, Commit `7ee1900`)

- **`fluss_sim_regeln.json`:** Version 8.
  - `swr.sim_vorgaben`: `match_spline` true, `match_spline_height_amount` 0,02, `remove_outside_spline_amount` 50,
    `source_size` „breite_quelle“, `sim_speed` 10, `num_steps` 10, `testreihe`.
  - `kollision.min_ausdehnung_hinweis` beschreibt die neue Mindestgröße.
- **`fluss_sim_export.py`:**
  - je SWR die Felder aus 1.2;
  - `back_liste.json` je SWR mit `sim_vorgaben` (Auflösung, die Felder oben, `use_capture`);
  - Mindestgröße nach größter Ausdehnung inklusive Skala; Feld `ausdehnung_m`;
  - `zusammenfassung.json`: `objekt_pool` mit der Zahl nach alter und neuer Regel.
- **`fluss_sim_pruefen.py`:** neue FEHLER-Prüfungen für:
  - SWR-Felder ≠ Vorgabe;
  - `num_steps` < `sim_speed`;
  - `source_size_cm` ≠ Breite am ersten Punkt;
  - `sim_vorgaben` der Back-Liste ≠ SWR;
  - `ausdehnung_m` ≠ eigene Rechnung (Bounds × |Skala|, ± 1 mm) oder < 0,4 m.
- **Lauf (2-m-Daten, Scratchpad):**
  - Gefälle-Planer `--alle`: 123 Läufe, 0 FEHLER.
  - Sehens-Planer für alle 15 Biome; `bachbett_roh`: 0 FEHLER.
  - Export: 187 Gewässer, 199 SWR, 762 Fälle.
  - **Prüfer 0 FEHLER, 0 WARNUNG, 70 HINWEIS**; zwei Exportläufe byte-gleich (183 Dateien). `selbsttest_16c` ohne Fehler.
- **Gegenproben** (alle FEHLER, Exit 1):

  | Gegenprobe | Ergebnis |
  |---|---|
  | `match_spline_height_amount` 2 | 2 FEHLER |
  | `source_size_cm` 1000 | 2 FEHLER |
  | `ausdehnung_m` 0,3 | 1 FEHLER |
  | Back-Liste `remove_outside_spline_amount` 200 | 1 FEHLER |
  | `num_steps` 5 | 3 FEHLER |
  | Regel 0,5 m statt 0,4 m | 167 FEHLER (Objekte zwischen 0,4 und 0,5 m) |

- **Fingerabdrücke:**
  - 149 von 199 SWR-Bereichen haben einen neuen Fingerabdruck, **nur im Objektteil**: Die Objekte im Fingerabdruck sinken von
    55 157 auf 53 518.
  - 50 SWR bleiben gleich. Gelände und Splines sind überall gleich.
  - Die `sim_vorgaben` gehören nicht zur Formel (`FLUSS_SIM_FP1` unverändert). Das lokale Werkzeug soll neu backen, wenn
    Fingerabdruck **oder** `sim_vorgaben` vom letzten Backen abweichen. Bisher sind nur C2-Tests gebacken, also gilt das für
    alle.
- **Beispiele** unter `antworten/fluss_sim/` neu: `F_ERLENBACH`, Karsee, Elfentreppe, `zusammenfassung.json`,
  `back_liste_auszug.json` (mit `sim_vorgaben`); `vorschlaege.json` unverändert. README um „Ergänzungen 16f Rückfrage“
  ergänzt.

## Rückfragen

1. **Bachbreite an der Quelle:** Der Export nimmt die Spline-Breite am ersten Punkt (2-m-Lauf: Median 4,0 m). An C2 ist die
   Spline in den 2-m-Daten 13–28 m breit; ihr nennt 3 m Bach.
   - Ist die lokale 1-m-Spline an C2 so schmal? Oder meint ihr die Rinne im breiteren Bett?
   - Im zweiten Fall bräuchte der Export eine eigene Quellbreite, z. B. aus der Wasserbreite des Plans statt der Bettbreite.
2. **Einheit von `FoamAtten`, Wave Atten und Scattering Velocity:** Bitte das Ergebnis aus 3.3 melden. Dann trage ich die
   Material-Startwerte als Vorgabe in die Regeln ein, wenn ihr sie vom Bau-Werkzeug setzen lassen wollt.
3. **Dilation:** Läuft in T4 Wasser durch Stämme, gibt der Export die Holz-Komponenten je `WH_` getrennt aus
   (Feld `dilatiert`). Bitte Bescheid geben.
4. **Standardwerte der Niagara-Kopie:** Ein Bildschirmfoto der Benutzerparameter (Friction, Velocity Dissipation,
   Whitewater-Mults, Restrict-Ranges) macht aus den Faktoren in 3.4 und 5 feste Zahlen.

## Quellen

- Ferats Zusammenfassung (lokal gelesen 12.10.2026, 23:40): `recherche/auftraege/16f-rueckfrage-epic-parameter-lokal.md`.
- Epic Developer Community, Devon Penney: „Baked River Simulations – Parameter Reference“ (15.05.2025, aktualisiert
  17.06.2025):
  https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference
  (aus der Cloud gesperrt; Inhalt nur über Ferats Zusammenfassung).
- Projekt:
  - `antworten/16f-water-plugin-bachbett-recherche.md` (Teil A 4 und 5.2);
  - `antworten/16e-ferat-schaum-weg-langsamer.md` (Tempo-Regel, Schaum-Tabellen, Option B);
  - `antworten/16b-swr-c2-ganze-strecke.md`, `antworten/16c-ferat-ein-fluss-je-gewaesser.md` (Kosten 512/1024/2048,
    C2-Rechteck, Auflösungsbild);
  - `skripte/fluss_sim/` (Regeln v8, Export, Prüfer, README).
