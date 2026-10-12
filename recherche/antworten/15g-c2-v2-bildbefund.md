# Antwort zu Auftrag 15g – C2 Version 2 gebaut: Bildbefund (Schaum eckig, Becken zu grün, Terrassen von unten)

Stand 12.10.2026. Die Planer-Fassung ist Commit **`0e00d17`**. Stufen, Stufenhöhen und Beckenspiegel sind dieselben
wie in Version 2 (`ae09234`): In allen 19 Pilotläufen sind Stufenliste, Lippenpunkte und `spiegel_neu_cm` gleich.

## Kurzfazit

- **Schaum eckig → weich.** Die Rechtecke und die Strichreihe kamen von harten Sprüngen quer **und** längs.
  - **Quer:** Bei C2 lagen die Querpunkte bis 2,96 m auseinander (Breite bis 28,8 m bei 11 Punkten).
  - **Längs:** Schaum 1 stand neben 0,1, im Becken auch auf 1,7-m-Abständen.
  - **Jetzt:**
    - Querpunkte max(21; Breite/1 m), bei C2 also 31, Querabstand ≤ 0,99 m.
    - Kanten weich mit smoothstep und deterministischem Rauschen, quer und längs; Mittellinie über die ganze
      Schaumzone alle 0,25 m.
    - Größter Sprung zwischen Nachbarpunkten: quer 1,00 → **0,45**, längs 1,00 → **0,33**.
- **Becken zu grün und deckend.** Werte für `M_EL_Kaskade_SLW2` stehen im Netz (`material_parameter`, Tabelle in
  Abschnitt 2).
  - **Wahrscheinliche Hauptursache:** Laut UE-Doku regelt **Opacity** bei Single Layer Water das Verhältnis
    Wasservolumen zu Oberfläche. Opacity 1 ergibt eine deckende Fläche in Base Color. Wenn `deckung` (Vertex A) auf
    Opacity liegt, sind die Becken (Deckung 1) deckend grün.
  - **Empfehlung:** Opacity nur aus Schaum. `deckung` geht auf Specular und Normalstärke.
  - Dazu `tiefe_cm` ≥ 0 (vorher an 1 613 Stützpunkten negativ). `deckung` ist 0 über Land und läuft zum Ufer weich aus.
- **Terrassen von unten.**
  - **Beckenränder:** Sie sind jetzt unregelmäßig, mit Vorsprüngen bis 1,2 m je Seite und Buchten dazwischen. Die
    Spiegel bleiben waagrecht.
  - **Randblöcke:** 72 Eckblöcke an den Lippenenden und 22 Blöcke am Beckenrand.
  - **Randlänge:** 68 % haben eine Bucht/einen Vorsprung oder einen Block in ≤ 1,5 m. Vorher waren es 0 %.
- **Prüfungen:**

  | Lauf | Läufe | FEHLER | WARNUNG | Anmerkung |
  |---|---|---|---|---|
  | C2, 2 m | 1 | 0 | 2 | zweimal gelaufen, `diff -r` identisch |
  | C2, 1-m-Fenster (`--hoehe1m-fenster`) | 1 | 0 | 2 | zweimal gelaufen, identisch (auch das Testbild) |
  | 19 Pilotläufe, 1-m-Fenster | 19 | 0 | 12 | dieselben 12 WARNUNGEN wie vorher |
  | 19 Pilotläufe, 2 m | 19 | 0 | 12 | |
  | alle 161 Strecken, 2 m | 98 mit Stufen | 0 | 51 | vorher 48; +2 „Schaumanteil > 25 %“, +1 Ufer-Raster F_HAUPTFLUSS_3_C5 |
  | `sehens_lib/selbsttest.py` | – | durch | – | Lib unverändert |

  Die neuen Prüfregeln finden den alten Stand. Der Plan vor 15g ergibt bei C2 5 FEHLER: Querraster zu grob,
  `tiefe_cm` < 0, harte Schaumkante quer an 1 223 Stellen, längs an 104 Stellen, Schaum auf grobem Raster.

## 1. Eckige Schaumflecken

### 1.1 Ursache

- **Quer:** 11 Stützpunkte auf 12–29 m Netzbreite ergeben 1,2–3 m Abstand. Die Kerbe (0,8–3 m) war damit 1–2
  Stützpunkte breit, mit linearem 0,3-m-Rand. Auf dem 0,5-m-Gitter des Einbaus wird daraus ein weißes Rechteck.
- **Längs:** Der Saum (0,5 m) und die Zunge waren Masken mit harter Grenze. Neben Schaum 1 lag 0,1, und im Becken
  lagen die Punkte bis 1,7 m auseinander. Das ergab die „Strichreihe“ (`s1`, `s1_weg`, `fern`).

### 1.2 Änderungen (`quer_ergaenzen`, `kerben_weich`, `schaum_weich`, `quer_n`)

1. **Querpunkte:**
   - N = max(21; ⌈(Breite_max + 0,8 m)/1 m⌉ + 1), ungerade (Mittelpunkt = Spalte `schaum` der Mittellinie).
   - Die Zahl gilt je Netz und steht in `quer_punkte`; bei C2 ist sie 31.
   - In `gefaelle_regeln.json`: `quer_punkte` 21, `quer_abstand_max_m` 1,0.
2. **Quer weich:**
   - Der Kerbenrand ist ein smoothstep über ≥ 3 Querabstände (mindestens 0,4 m). Damit liegen 2 Zwischenpunkte
     zwischen Kerbe und Seite.
   - Die Kerbenbreite schwankt entlang s mit Rauschen (±20 % des Rands), die Kante ist also nicht gerade.
3. **Längs weich, unterhalb länger als oberhalb:**
   - **Kern:** am Lippensaum und auf der Zunge (bis Fuß + Bogen + 0,3 m) Schaum 1 in der Kerbe, 0,1–0,15 daneben.
   - **Oberhalb:** Anstieg über 0,8 m. Schaum ≥ 0,5 liegt höchstens etwa 0,5 m vor der Lippe, wie bisher.
   - **Unterhalb:** Abklingen über clamp(0,15 × Beckenlänge; 0,8; 1,5) m.
   - Beide Längen schwanken um ±20 % mit 2-D-Wertrauschen (Gitter 0,9 m). Die Kante ist dadurch ausgefranst und
     keine Linie.
   - **Aufprall:** Der Kern endet dort, wo der Schaum auf 0,5 fällt. Das liegt bei ≤ 30 % der Beckenlänge, wie
     bisher. Neu: Er endet auch vor der Beckenmitte, wenn der Strahl weit trifft.
   - **Rand des Aufpralls:** elliptisch, längs wie das Abklingen, quer ≥ 3,2 Querabstände, und nur unterhalb der
     eigenen Lippe. Vorher lief ein Aufprallrand bei kurzen Kaskadenbecken bis über die nächste Lippe hinauf.
4. **Rauschen deterministisch:** ganzzahliger Hash (splitmix), Seed aus Lauf-ID und Netznummer.
5. **Verdichtung:** Um jede Lippe liegt die Mittellinie alle 0,25 m, über die ganze Schaumzone (vom Anstieg bis zum
   Ende des Abklingens bzw. des Aufpralls).
6. **Sicherheitsnetz:**
   - `schaum_weich` begrenzt den Sprung auf 0,45 je Querabstand bzw. je 0,5 m längs.
   - Es hebt nur die niedrigere Seite an, es entsteht also kein neuer Schaum in der Fläche.
   - An der Fallkante (Punkte mit fast gleichem s) gilt 0,3 × 0,45.

**Regel „Schaum nur an Lippen / Zunge / Aufprall“:** gilt weiter, für Schaum ≥ 0,5. Nur das weiche Ausklingen (< 0,5)
reicht darüber hinaus, oberhalb ~0,8 m, unterhalb ≤ 1,5 m. Text im Netz: `schaum_regel`.

**Prüfer (`pruefe_schaum_15g`, alles FEHLER):**
- ≥ 21 Querpunkte und Querabstand ≤ 1 m.
- Sprung zwischen Nachbarpunkten quer ≤ 0,5 und längs ≤ 0,5 je 0,5 m.
- Wo Schaum > 0,05 liegt, Längsabstand ≤ 0,6 m.
- Schaum ≥ 0,5 nicht in der Beckenmitte: je Längsstreifen, Becken ≥ 6 m, Bereich [Anfang + 0,5 L + 1,5 m; Ende − 1 m].
- `tiefe_cm` ≥ 0.
- Dazu eine WARNUNG, wenn Schaum ≥ 0,5 mehr als 25 % der Netzfläche bedeckt (dichte Fallketten).

### 1.3 Zahlen C2 (1-m-Fenster, KN0)

| Kennzahl | vorher (2378e0d = Fassung ae09234) | nachher (0e00d17) |
|---|---|---|
| Querpunkte / größter Querabstand | 11 / 2,96 m | **31 / 0,99 m** |
| größter Schaumsprung quer (Nachbarpunkte) | 1,00 (99 %-Wert 1,00) | **0,45** (0,45) |
| größter Schaumsprung längs | 1,00 (99 %-Wert 0,73) | **0,33** (0,23) |
| größter Längsabstand mit Schaum > 0,05 | 1,73 m | **0,37 m** |
| Netzpunkte | 776 | 856 |
| Schaum > 0,8 / ≥ 0,5 / > 0,05 (Netzfläche) | 8,4 % / 9,5 % / 42 % | 6,2 % / 10,5 % / 49 % |

- Mehr Fläche mit Schaum > 0,05 heißt: Die Ränder laufen aus. Der Kern (> 0,8) ist kleiner geworden.
- Über alle 19 Pilotläufe (49 Netze):
  - größter Sprung quer 0,45, längs 0,39 (vorher je 1,00)
  - Schaum ≥ 0,5 im Mittel 11,5 % der Netzfläche, vorher 15,0 %
- Bild: [`gefaelle/c2_15g_schaum_vorher_nachher.png`](gefaelle/c2_15g_schaum_vorher_nachher.png) zeigt das Netz
  abgewickelt (s 0–75 m), bilinear wie das Einbau-Gitter. Oben: weiße Rechtecke an den Kerben. Unten: runde,
  ausgefranste Flecken. Das Testbild [`gefaelle/test_F_ERLENBACH_1V_C2_s1.png`](gefaelle/test_F_ERLENBACH_1V_C2_s1.png)
  ist neu erzeugt.

## 2. Becken zu grün und deckend – Werte für `M_EL_Kaskade_SLW2`

### 2.1 Was die UE-Doku zu Single Layer Water sagt

- Der Knoten **Single Layer Water Material** hat vier Eingänge:
  - Scattering Coefficients
  - Absorption Coefficients
  - PhaseG: Richtung der Streuung, 0 = isotrop
  - Color Scale Behind Water: Helligkeit des Grunds, wirkt wie Kaustik oder Schatten, ist aber nur ein Bildeffekt
- Wasser rechnet die Durchlässigkeit über die echte Tiefe hinter der Oberfläche. Die Koeffizienten sind
  Dämpfung je Längeneinheit (Beer-Lambert). Höhere Absorption macht das Wasser weniger durchsichtig.
- **Opacity** im Hauptknoten regelt das Verhältnis Volumen-BSDF zu Oberflächen-BRDF. Hohe Opacity ergibt eine
  deckende Oberfläche, die mit Base Color schattiert wird. So macht man Schaum.
- Blend Mode muss Opaque oder Masked sein.
- Refraktion: Für große flache Wasserflächen empfiehlt Epic **Pixel Normal Offset** statt Index of Refraction. Ohne
  Normal Map gibt es dann keine Refraktion.

**Folgerung:** `deckung` (Vertex A) nicht auf Opacity legen. Sonst ist jedes Becken mit Deckung 1 eine deckende
Fläche in Base Color, und genau so sieht `kn0_nah_s119` aus. Opacity kommt nur aus dem Schaum (Vertex B).

### 2.2 Parameter (stehen in `material_parameter` jedes Kaskadennetzes)

| Parameter | Wert | Begründung |
|---|---|---|
| Absorption (R, G, B) je m | **0,40 / 0,07 / 0,05** | Reines Wasser nach Pope & Fry 1997: 650 nm 0,34, 550 nm 0,057, 450 nm 0,009 je m. Dazu wenig gelöstes Organik/Mineral im Gebirgsbach. Blau < Grün, damit es nicht ins Grüne kippt. Gleiche Größenordnung wie das Forumsbeispiel „clear water“ (0,35 / 0,07 / 0,03) je m. |
| Streuung (R, G, B) je m | **0,02 / 0,03 / 0,04** | Reines Wasser 0,001–0,005 je m (Morel 1974). Wenig Schwebstoff gibt den Becken etwas Körper. Höhere Werte machen das Wasser milchig und deckend. |
| PhaseG | **0,5** | Natürliche Partikel streuen stark vorwärts (g ≈ 0,92, Petzold). 0,5 vermeidet einen grellen Hof gegen die Sonne. Vorzeichen nach aktueller Doku (g > 0 = vorwärts); die 4.26-Referenz nennt es umgekehrt. Wird das Wasser gegen die Sonne nicht heller, Vorzeichen tauschen. |
| Color Scale Behind Water | **1,0** | Grund unverändert hell, klares Wasser. Für dunklere Gumpen 0,85–0,9. |
| Base Color | **Schaum (0,80 / 0,83 / 0,83) linear** | Wirkt nur dort, wo Opacity > 0 ist, also im Schaum. |
| Opacity | **Schaum × Kurve aus Schaum_Menge (0,15) bzw. Zungen_Schaum (0,25)** | nicht aus Deckung, siehe 2.1 |
| Specular | **0,25** | F0 von Wasser (n = 1,33) ist 0,02; UE-Specular = F0/0,08 |
| Rauheit | **Becken 0,04, Schaum 0,4** | lerp über Vertex B |
| Refraktion | **Pixel Normal Offset, 1,33**; an Lippen/Zungen 1,15 | Wert für Wasser; zu starke Verzerrung an den Lippen dämpfen |
| Deckung (Vertex A) | **× Specular und × Normalstärke** | Am Ufer läuft der Glanz aus. Quads < 0,3 nur weglassen, wo `tiefe_cm` = 0 ist. |
| Tiefenfaktor | **optional** Absorption/Streuung × clamp(Tiefe/1,5 m; 0,35; 1) | SLW rechnet die Tiefe schon selbst. Zuerst mit Faktor 1 testen, den Faktor nur nehmen, wenn flache Becken noch zu farbig sind. |

**Einheit:** In UE 5 liegen die Koeffizienten je Meter. Frühe Beispiele (UE 4.25) haben dieselben Werte × 0,01 für
je cm genutzt. Lokal prüfen: Bei 1,5 m Tiefe muss Rot auf etwa 55 % gedämpft sein (e^−0,6), der Grund also leicht
türkis.

### 2.3 Tiefe und Deckung im `quer`

- **`tiefe_cm` ≥ 0:** 0, wo das Gelände über dem Wasser liegt (Netz unter dem Ufer). Vorher war `tiefe_cm` an 1 613
  Stützpunkten negativ. C2: Median 1,11 m, höchstens 4,35 m (Kolk).
- **`deckung`:**
  - 0 über Land.
  - Sonst 0,3 + 0,7 × smoothstep(Tiefe / 0,6 m).
  - Quer fällt sie höchstens um 0,5 je Stützpunkt, auch an steilen Böschungen.
  - Die Zunge in der Kerbe bleibt deckend, daneben bleibt `seite_deckung` (Fels scheint durch).
- **Kennzahlen C2:**
  - Beckenstützpunkte mit Tiefe ≤ 0, die trotzdem Deckung > 0,3 hatten: 13,9 % → **0 %**.
  - Größter Deckungssprung quer im Becken: 0,82 → **0,50**.
  - Netzfläche mit Deckung < 0,3: 13 % → 23 %. Der Zuwachs ist Land unter dem Netz; dieses Netz ist jetzt breiter,
    siehe 3.
- **Ferats Regel „Quads mit Deckung < 0,3 weglassen“:** An Ufern trifft sie jetzt nur die Quads unter dem Gelände.
  An Zungen bleibt es wie bisher.

## 3. Terrassen von unten (`kn0_unten`)

### 3.1 Unregelmäßige Beckenränder (`UferRand`)

- **Wasserkante je Seite:** Sie zieht um einen Einzug e(s) = amp(s) × n(s) nach innen.
  - n ist weiches Wertrauschen in zwei Oktaven, Wellenlänge ~6,5 m und ~2,8 m. Der Seed kommt aus Lauf-ID und Seite.
  - Über eine weiche Schwelle (n < 0,3 → 0, n > 0,75 → 1) entstehen Buchten auf voller Breite und Vorsprünge.
- **amp** = clip(0,2 × Breite − 0,3 m; 0; 1,2 m). Je Seite ist amp = 0:
  - am Lippenende dieser Seite (schräge Lippe: s_l + Versatz(±h)), 0,3 m frei, 1 m Übergang
  - an Segmentenden (3 m) und Mündungen
  - in Wand- und Klammzonen (Böschung > 50°)
- **Netzbreite:** Sie wächst um max(amp links; amp rechts) und bleibt so die Hülle. Die Wasserkante liegt nie
  außerhalb des Netzes, der Netzrand nie im Wasser. An den Lippen bleibt die Einschnürung.
- **Gelände:**
  - `profil_T`, `aussen_begrenzen` und der Uferring rechnen mit der Wasserkante je Seite.
  - Die Vorsprünge bildet der Uferring (Spiegel + 0,2 m, höchstens 1 m anheben). Sein Plateau endet weiter am
    Netzrand + 1,5 m.
  - In den Buchten schneidet das Gelände neben dem Wasser höchstens Eintiefung + 0,5 m (Regel aus 15e).
  - Größtes Δ bei C2 unverändert 7,26 m (Fälle).
- **Ausgabe:** `plan.json` → `ufer_rand` mit Einzug links/rechts je 1 m und den Kennzahlen.

### 3.2 Randblöcke

- **`randecke_<n>`:**
  - An jedem Lippenende, auch an Teil-Lippen, steht mit 85 % ein Eckblock von 0,9–1,8 m.
  - Er sitzt 0,1–0,6 m außerhalb der Wasserkante und 0,2–0,8 m stromab.
  - Von unten gesehen bricht er genau die Ecke, an der die Terrassenkante sichtbar wird.
- **`randbloecke_<n>`:** am Beckenrand alle 2,5–5 m je Seite, auf Vorsprüngen immer, sonst mit 33 %, Größe 0,6–1,4 m.
- **Netze:** nur aus der Biom-Palette `bloecke` (sonst `riegel`), die gegen das Inventar (`netze.csv` /
  `inventar_extra.json`) geprüft wird. Es gibt keine neuen Namen. Ebene `schutt`, keine Akteure, eingegraben
  0,3–0,45, Wegabstand 4 m wie die Stufenblöcke. Moos (Kontakt) wächst auch an diesen Blöcken.
- **Kerben:** Kerben für die Hauptsträhne gibt es seit 15f (1–2 je Lippe, Krone 0,15–0,4 m tiefer). Sie bleiben
  unverändert.

### 3.3 Zahlen

| Kennzahl | C2 vorher | C2 nachher | 19 Piloten nachher |
|---|---|---|---|
| größter Einzug je Seite | 0 | 1,2 m | 0,7–1,2 m |
| Randlänge mit Bucht/Vorsprung (Einzug > 0,3 m) | 0 % | 17 % | Mittel 25 % |
| Randlänge mit Randblock ≤ 1,5 m | 0 % | 61 % | – |
| Randlänge mit einem von beiden | 0 % | **68 %** | Mittel 63 %, min. 31 % |
| Eckblöcke / Randblöcke | 0 / 0 | **72 / 22** | 793 / 789 |
| Instanzen / Akteure | 1 631 / 62 | 1 803 / 62 | |
| mittlere Netzbreite | 20,2 m | 20,5 m | |
| Stufen, Stufenhöhen, Spiegel | 18 Stufen | gleich | in allen 19 Läufen gleich |

- **Wenige Buchten bei C2 (17 %):** C2 hat 42 Lippen auf 170 m. Die Kaskadenbecken sind oft nur 2–4 m lang, und an
  jedem Lippenende bleibt der Rand fest. Dort tragen die Eckblöcke die Unregelmäßigkeit.
- **Wenige Blöcke bei B_R2_R_M1_M1_02 (31 %):** Der Lauf hat Holzstufen, an denen es keine Eckblöcke gibt.

## 4. Lokal zu tun

1. **Neu planen auf 1 m** (Commit `0e00d17` oder neuer):
   ```
   python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis . --laeufe F_ERLENBACH_1V_C2
   ```
   Erwartet: 0 FEHLER. Schaum, Deckung und Tiefe kommen aus `quer` (`quer_punkte` je Netz, bei C2 31).
2. **Einbau:**
   - Gelände-Delta, Lagen und Instanzen von C2 tauschen. Das Delta ändert sich am Ufer (Buchten/Vorsprünge), dazu
     kommen die Ebenen `randecke_*` und `randbloecke_*`.
   - Kaskadennetz neu erzeugen, Vertexhöhe = `z_cm + dz_cm`.
   - Das Netz ist jetzt um bis zu 1,2 m breiter. Über Land ist die Deckung 0, dort darf das Netz fehlen.
3. **Material `M_EL_Kaskade_SLW2`:**
   - Werte aus Abschnitt 2.2.
   - Opacity = Schaum (Vertex B), nicht Deckung.
   - Deckung (Vertex A) → Specular/Normalstärke.
   - Tiefenfaktor zuerst aus (= 1).
4. **Kamera-Prüfpunkte:**
   - **`s1`, `s1_weg`, `fern`:** keine weißen Rechtecke, keine Strichreihe. Schaum als ausgefranste Flecken an den
     Kerben, nach unten 1–1,5 m auslaufend.
   - **`kn0_unten`:** Die Terrassenkanten sind unterbrochen: Eckblöcke an den Lippenenden, Vorsprünge und Buchten in
     den längeren Becken. Die Spiegel bleiben waagrecht.
   - **`kn0_nah_s119` (und `kn0_nah_s63`):** Die Gumpe ist klar, man sieht den Grund. Leicht türkis erst ab ~1,5 m
     Tiefe, kein deckendes Grün.

## 5. Aufruf (Cloud-Test)

```
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --daten2m recherche/vorlagen/daten/sehens \
    --hoehe1m-fenster recherche/vorlagen/daten/gefaelle/hoehe_1m_fenster --laeufe F_ERLENBACH_1V_C2 --aus <scratchpad>/a15g --bild
python -I recherche/antworten/skripte/gefaelle/gefaelle_pruefen.py <scratchpad>/a15g --daten2m recherche/vorlagen/daten/sehens \
    --hoehe1m-fenster recherche/vorlagen/daten/gefaelle/hoehe_1m_fenster
```

## 6. Quellen

- Epic Games: [Single Layer Water Shading Model in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine)
  – Eingänge Scattering/Absorption/PhaseG/Color Scale Behind Water, Opacity als Verhältnis Volumen-BSDF/Oberflächen-BRDF,
  Blend Mode Opaque/Masked
- Epic Games: [Single Layer Water Shading Model (UE 4.27)](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model?application_version=4.27)
- Epic Games: [Refraction Using Pixel Normal Offset](https://dev.epicgames.com/documentation/en-us/unreal-engine/refraction-using-pixel-normal-offset-in-unreal-engine)
- Epic Games: [Shading Models in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/shading-models-in-unreal-engine)
- Pope, R. M.; Fry, E. S. (1997): Absorption spectrum (380–700 nm) of pure water. II. Integrating cavity measurements.
  Applied Optics 36(33), 8710–8723, [doi:10.1364/AO.36.008710](https://doi.org/10.1364/AO.36.008710)
- Morel, A. (1974): Optical properties of pure water and pure sea water. In: Jerlov, Steemann Nielsen (Hrsg.), Optical
  Aspects of Oceanography, 1–24 (Streuung reinen Wassers)
- Mobley, C. D.: [Ocean Optics Web Book – Petzold’s Measurements](https://oceanopticsbook.info/view/scattering/petzolds-measurements) (mittlerer Kosinus der Partikel-Phasenfunktion 0,924)
- Epic Developer Community: [Actually realistic water shader](https://forums.unrealengine.com/t/actually-realistic-water-shader/141661)
  – Beispielwerte „clear water“ (Absorption 0,35/0,07/0,03, Streuung ~0,0007–0,0025, je × 0,01 in UE 4.25)
- World of Level Design: [UE5 Single Layer Water Pool](https://www.worldofleveldesign.com/categories/ue5/single-layer-water-pool-still.php)
  – Pixel Normal Offset in der Praxis

Hinweis: Die Epic-Seiten sind aus der Cloud nur über Suchauszüge erreichbar (Proxy). Die Aussagen oben stammen aus
diesen Auszügen der offiziellen Seiten.

## 7. Rückfragen

1. **Opacity:** Liegt `deckung` im lokalen `M_EL_Kaskade_SLW2` auf Opacity? Wenn ja, ist das sehr wahrscheinlich das
   „deckende Grün“. Bitte einmal mit Opacity = 0 im Becken gegenprüfen.
2. **Einheit der Koeffizienten:** Bitte kurz bestätigen, dass dein UE die SLW-Koeffizienten je Meter rechnet (Test in
   Abschnitt 2.2). Sonst alle Werte × 0,01.
3. **Buchten bei C2:**
   - Sie sind kurz, weil die Becken kurz sind. Ist von unten mehr Unruhe gewünscht? Dann ginge
     `ufer_rauschen.lippe_frei_m` 0,3 → 0 (Vorsprünge bis an die Lippe) oder `amp_max_m` 1,2 → 1,6.
   - Beides ändert die Stufen nicht.
