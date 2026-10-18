# Antwort 22 – Wasserpflanzen fern vom Wasser: Regeln für Prüfung und Reparatur

Gelesen: recherche/auftraege/22-wasserpflanzen-fern-vom-wasser.md @ 8bb2f7c076094c7bea3521d2effd69df1492483e (Commit b844a46)

Stand 18.10.2026. Bearbeiter: Cloud-Recherche. Bereich: neue Prüfklasse „Wasserpflanze fern vom Wasser“ in der Platzierungsprüfung v3.
Die Ausführung liegt lokal. Hier ist **nichts im Projekt geprüft oder angewendet**. Der Prüfcode in §7 lief nur synthetisch in der Cloud.

**Kennzeichnung:** [S] = nur Suchauszug. Alle Fachseiten waren aus der Cloud gesperrt (siehe §10), es gibt also keine Vollseite.
[Repo] = Daten oder Regeln im Repository. [Bild] = eigene Ansicht der beiden Bildtafeln. [Ableitung] = aus Belegen geschlossen.
[Annahme] = Gestaltungs- oder Startwert, im Pilot zu bestätigen.

## Kurzfazit

1. **Regel je Art (Frage 1): beantwortet.**
   - **Rohrkolben:** im Wasser bis 0,8 m Tiefe, an Land höchstens 6 m vom gebauten Wasser und höchstens 0,5 m über dem Spiegel.
     Von 6 bis 25 m nur in einer nassen Senke.
   - **Binsen:** bis 15 m und 1,5 m über dem Spiegel. Darüber hinaus nur mit Feuchte-Bedingung (Mulde, TWI oder Nass-Lagen).
   - **Schwimmblatt (`SM_WaterPlant01–04`):** nur im Wasser, 0,2–2,0 m tief.
   - Über 35° Hang wächst keine dieser Arten. Das betrifft die B5-Felsflächen.
   - Grundlage: Typha ist eine Röhrichtpflanze mit 10–60 (–100) cm Wassertiefe, Ellenberg-Feuchtezahl 10, und braucht Marsch mit
     Grundwasser unter 25 cm [S]. Juncus bufonius (Feuchtezahl 8) wächst auf zeitweise nassem, offenem Boden, auch in Fahrspuren [S].
2. **Biome (Frage 2): beantwortet.**
   - **Sumpf-Zone (H5, Sumpfteil I5, 30-m-Saum):** Hier gilt eine Ausnahme, aber nur auf der vorhandenen Nassmaske aus
     `sumpf_regeln.json` oder in einer Senke. Die Grasmatte der Sumpf-Zone allein reicht nicht.
   - **Wüste, Canyon, Ödland:** Rohrkolben nur an gebautem Wasser im Band ≤ 5 m (Oase, Quelle; wie `schilf_rest` des Wüstenplaners),
     Binsen ≤ 8 m. Es gibt dort keine Feuchte-Ausnahme. Wüsten-Rohrkolben gibt es real nur an Quellen und Cienegas [S].
3. **Trockenbetten (Frage 3): beantwortet.**
   - **Empfehlung:** die Pflanzen entfernen und durch Trockenbett-Bewuchs aus dem Bestand ersetzen.
   - **„Trockenbach mit Rohrkolben“** bleibt nur in einer nassen Senke ≤ 25 m vom heutigen Wasser stehen. Grüne Rohrkolben auf
     rissigem Schlamm widersprechen sich.
   - **Wasser zurück** ist Ferats Entscheidung. Kriterien stehen in §4.4. Meine Empfehlung: in Wüste, Canyon und Ödland nie; in der
     Aue höchstens für die 1–3 längsten Betten, die alle Kriterien erfüllen.
4. **`GT_Schilf` (Frage 4): Regel beantwortet, Wirkung wartet auf den Trockenlauf T22-0.**
   - Faktor auf `v_schilf`: voll bis 4 m, linear auf 0 bei 12 m. Höhenfaktor 1 bis 0,3 m über dem Spiegel, 0 ab 1,0 m.
   - Ausnahme: in Sumpf-Zellen auf der Nassmaske höchstens 0,5. In Trockenbetten immer 0.
5. **`SM_lily_01_1/_2` (Frage 5): wartet auf Netzbild.**
   - Nach Netzbelegen (Paket, Nachbarnetze, Maße) wahrscheinlich eine **Landlilie**. Das ist eine Hypothese, kein Beweis.
   - Bis zur lokalen Ein-Schritt-Prüfung (§5) bleibt lily aus der Wasserpflanzen- **und** aus der Landregel ausgenommen.
6. **Reparaturform (Frage 6): beantwortet.**
   - Standard ist Entfernen mit Sicherung je Instanz wie in v3. In Trockenbetten wird zusätzlich ersetzt, als eigene, protokollierte
     Zugabe.
   - Versetzen nur für Gruppen ab 6 Instanzen, mit Schwerpunkt ≤ 25 m vom Wasser und freiem Uferband (§6.3). Es ist als Phase 2
     gedacht, nicht als Pilot.
7. **Prüfcode: geliefert.** Python-Referenz mit synthetischem Selbsttest (§7). `python -I … --selbsttest` lief zweimal mit gleicher
   Signatur. Lokal ist der Code nicht ausgeführt.
8. **Erwartete Wirkung [Ableitung aus dem Zensus]:**
   - Entfernt werden etwa **10 500–15 500 von 67 990** Instanzen (15–23 %).
   - Der Anteil „> 15 m vom Wasser“ fällt von 14,2 % auf etwa 2–4 % (nur Feuchte- und Sumpf-Ausnahmen).
   - Die exakte Zahl liefert T22-0.
9. **Nächste Handlung (lokal):** Trockenlauf **T22-0**. Er zählt nur und ändert nichts. Danach folgt der Pilot **C4** (§8).

---

## 1. Befund aus Zensus, Bildern und Repo

### 1.1 Bilder [Bild]

Ich habe beide Tafeln angesehen, auch vergrößert.

| Bild | Was ich sehe | Fallgruppe nach §3 |
|---|---|---|
| C4_09 Horst_2, 349 m | Dunkelgrüne Bandblatt-Rosette **ohne Kolben** im trockenen Steppengras vor roten Sandsteinwänden. Ohne Kolben liest sich der Horst wie Agave/Yucca. | fern im Trockenen |
| D4_07, D4_10 | Canyonfuß und rötlicher, flacher Canyonboden (Playa-Eindruck) mit kleinen Horsten | fern im Trockenen |
| D4_08 ToadRush_02, 363 m | Wiese unter einer Trauerweide, Rosetten, trockener Boden. Die Weide deutet auf ein früheres Gewässer. | fern; Altwasser prüfen |
| D6_01/02/03 | Trockener Boden mit Steinen, ein Kopfsteinbett an Felsen (02) und eine Blumenwiese mit Jung_3 (03) | fern im Trockenen; D6_02 Bettform |
| E6_04 Horst_2, 507 m | Konkave, mit Geröll gepflasterte Rinne: Bettform ohne Wasser | Trockenbett, falls die Altwasser-Schicht dort liegt, sonst fern |
| B5_05/06 ToadRush, 391–434 m | Binsenbüschel über **steile Felsflächen** gestreut | Hang > 35° |
| D5 (Kontrollen) | Rohrkolben mit Kolben am Ufer neben der Brücke | richtig: Kontrollfall „ok“ |
| C4 typisch, 34 m | Jung_1-Gruppen an einer dunklen Schlammrinne mit Weidensaum | Trockenbett |
| F6 typisch, 41 m | Horst_3 auf **rissigem Schlamm** neben einer trockenen Rinne, Weiden | Trockenbett |
| E5 typisch, 29 m | Rechts eine grüne Wasserfläche | Vorbedingung V0: Wasser-Wahrheit lückenhaft, **nicht reparieren** |
| G5 typisch, 22 m | Dichter Rohrkolbenbestand mit Kolben. Unten links dunkle, spiegelnde Pfützen. | Feuchte-Fall: bleibt, wenn eine Senke da ist |
| H4, D4, D6, F5 typisch | Waldboden, Wiese, Schieferschutt; nichts Nasses sichtbar | fern im Trockenen (20–40 m) |
| H5 typisch, ToadRush_00, 19 m | Hohe, gelbbraune Grasmatte ohne sichtbaren Schlamm | Sumpf: entscheidet die Nassmaske |

**Folgerung [Bild/Ableitung]:** Zwei Merkmale machen die fernen Fälle sichtbar falsch: der fehlende Wasserbezug und die Horste ohne
Kolben, die im Trockenen als Sukkulente gelesen werden. Am Ufer mit Kolben (D5, G5) wirkt dasselbe Netz richtig.

### 1.2 Herkunft im Repo [Repo]

- **Die Planer hatten richtige Bänder.** Sie liegen nur auf veralteten Eingaben:
  - `aue_regeln.json` Schilf: 0,5–6 m.
  - `wueste_ergaenzung_regeln.json` `schilf_rest`: 0,8–5 m, < 25°.
  - `sumpf_regeln.json`: `schilf_land` in den Zonen spiegel/ufer (≤ 3 m, ≤ 0,8 m), Rohrkolben im Wasser 0–0,3 m, Seerosen 0,3–1,5 m.
  - `elfenwald` Binsen: 0,5–2,5 m.

  Dass 40 % der Fälle > 15 m ≤ 5 m an Wasser der alten Karte stehen, passt dazu. Die Instanzen wurden gegen eine alte
  `karte_wasser` bzw. die Houdini-Ebene `FT_EL_WELT_*` gesetzt. **Hypothese:** Die Aufteilung nach Foliage-Typ-Präfix
  (`FT_EL_WELT_`, `FT_Rohrkolben_`, `FT_EL_AUE_`, `FT_EL_WUES_`, `FT_EL_SUMP_`, `FT_EL_HEID_`, `FT_EL_DSCH_`, `FT_EL_ELFE_`) zeigt im
  Trockenlauf, welche Ebene die Ursache ist.
- **H5 ist größtenteils Absicht.** `sumpf_regeln.json` setzt `segge_bult` (ToadRush_00/02/010) in der Zone `bult` (3–18 m) **und** auf
  Nassflächen ohne Wasser in 18 m. Das ist die Nassmaske mit den Gewichten Schlamm 1, Algen 1, Moos 0,5, Lehm 0,4, Kraut 0,2,
  geglättet mit σ 6 m und Schwelle 0,35. Begründung dort: H5 hat 0,4 % kartiertes Wasser, aber 35 % Schlamm und Algen. Die neue
  Regel übernimmt diese Maske, statt sie zu verwerfen.
- **Antwort 19** setzt Binsen bewusst an 23 Sickerquellen und an Moorwiesen am Bachanfang, unter anderem in C3, C4, D5, D6, E5, F4,
  F5, G4 und G5. Diese Flächen sind Ausnahmeflächen (`quelle`), solange ihr Bach in der Wasser-Wahrheit noch nicht als gebaut gilt.
- **`SM_WaterPlant01–04`** dient im Nordküstenplaner auch als Tang-Ersatz im Spülsaum (`tang`). Für Schwimmblätter zählt deshalb das
  Meer als Wasser (`wasser_alle` aus den Konventionen §1b), für Rohrkolben und Binsen nur Süßwasser.

---

## 2. Ökologische Grundlagen (Quellen in §10)

| Art | Befund | Folge für die Regel |
|---|---|---|
| **Typha (Rohrkolben)** | Röhricht des Flachwassers. Bestände meist bei 10–60 (–100) cm Wassertiefe; der Standort kann im Sommer austrocknen [S Pladias Typhetum latifoliae]. Bestände mit 30–100 cm Dauerüberstau, maximaler Wuchs bei etwa 50 cm (Grace & Wetzel 1981) [S USGS NVCS]. T. latifolia steht flacher als T. angustifolia und verträgt Pegelschwankungen [S USDA Plant Guide]. Ellenberg-Feuchtezahl 10 [S Pladias/FloraVeg]. Keimung in Flachwasser oder auf feuchtem, offenem Schlamm, kaum im eigenen Bestand [S USU Extension]. Weniger Bodenfeuchte senkt Biomasse und Rhizomlänge; der Grundwasserstand korreliert am stärksten mit der Biomasse [S VT-Studie]. Nach Ökostandort-Klassen (USDA NRCS ESD) dominiert er die „Marsch“: Grundwasser < 10 in (25 cm) am Ende der Wachstumszeit. Nasswiese 10–20 in, Wiese 20–40 in [S]. | Wasser bis 0,8 m; an Land Boden ≤ 0,5 m über Spiegel (25 cm Grundwasser plus Toleranz für 1-m-Raster und Pivot) [Ableitung]. |
| **Juncus bufonius (Krötenbinse)** | Einjährig, FACW („meist nass, gelegentlich trocken“). Wächst an nassen Wegrändern, in Senken, Gräben, Marschen und auf Sandbänken [S USGS WARC]. Toad-rush-Gesellschaften auf zeitweise überflutetem oder feuchtem, offenem Boden, in Tümpeln und Fahrspuren von Waldwegen, auch in der Abtrocknungsphase [S EUNIS 3098/3099]. „Open disturbed sites, from dry to wet“ [S NIWA]. Feuchtezahl 8 [S Pladias]. **Zur Verdichtung** sagt keine Quelle etwas direkt; „Fahrspuren“ ist das Nächste. | Binsen brauchen **nicht** permanentes Wasser, aber zeitweise Nässe: weiterer Abstand plus Feuchte-Bedingung. |
| **Juncus effusus (Flatterbinse, Vergleich Nasswiese)** | Wiesen mit dauerfeuchtem Boden [S EUNIS 3963]. Typisch für saisonal nasse Weiden, nicht für ganzjähriges Wasser [S UF/IFAS AG335]. Weniger Bodenfeuchte senkt den Wuchs um bis zu 74 % [S]. | Stützt die Nasswiesen-Ausnahme über eine Mulde oder den TWI. |
| **Nymphaea (Seerose)** | Nymphaeetum albae in Altwassern und Tümpeln, meist 50–100 cm tief, **nicht in fließendem Wasser** [S Pladias]. Gartenangaben 45–150 cm, ein Händler nennt bis 3 m [S]. | 0,2–2,0 m (Toleranz für Spiegel- und Rasterfehler); Fließgewässer nur Hinweis. |
| **Wüste und Canyon** | Typha domingensis bildet Bestände von der Sonora- und Mojave-Wüste bis zum Great Basin, auf alkalischem, feinkörnigem Alluvium [S NatureServe/USGS]; bis etwa 6 g/l Salz [S Cienega de Santa Clara]. Hanging Gardens und Sickerstellen an Canyonwänden sind Inseln feuchter Vegetation in trockener Umgebung; in einer Sickerquell-Gesellschaft des Arid West ist Juncus arcticus genannt [S]. | Rohrkolben in der Wüste nur an Quelle oder Oase mit gebautem Wasser; Binsen an Sickerstellen nur auf Ausnahmeflächen. |
| **Trockenbetten** | In ephemeren Gerinnen der Sonora wachsen Uferbäume über tiefes Grundwasser (Salix > 4 m Flurabstand) [S]. Zu Typha in Trockenbetten fand ich **keine** Quelle. | Weiden am Trockenbett sind plausibel, grüne Rohrkolben auf rissigem Schlamm nicht [Ableitung]. |
| **TWI** | TWI = ln(SCA / tan β) [S SAGA-Doku]. Einen allgemeingültigen Schwellenwert gibt es nicht, er muss je Gebiet kalibriert werden [S]. | Startwert 9,0 bei 1-m-Zellen, Kalibrierung im Trockenlauf (§4.3). |

---

## 3. Regeltabelle (a): Art × Biom → Grenzen

**Eingaben (lokale Namen):**

- `d_w`: horizontaler Abstand zur nächsten **gebauten** Wasserzelle der abgeglichenen Wasser-Wahrheit. Jump-Flooding wie in den
  Planern, Reichweite 64 m, darüber ∞.
- `dh`: Boden am Instanzort (`hoehe.f32`, 1 m, bilinear) minus Spiegel dieser nächsten Wasserzelle. Der Spiegel kommt aus
  `spiegel_cm` bzw. dem Fluss-Spline. Fehlt er, gilt die Geländehöhe der Wasserrand-Zelle wie im Sumpfplaner.
- `tiefe`: Spiegel minus Boden in Wasserzellen.
- `hang`: aus `hoehe.f32`, σ 1,5 m wie in den Planern.
- `biom`: aus `eigner.r8` + `welt.json`.
- `d_alt`: Abstand zur getrennten Schicht „Wasser der alten Karte“, nur Zellen, die heute kein Wasser sind.
- Lagen: `lage_*.r8`.

**Feuchte-Bedingung `feucht`** (eine von drei genügt):

1. **Mulde:** `mulde = Gauss24m(hoehe) − hoehe ≥ 0,5 m` und `hang ≤ 8°` [Annahme]. Das ist die Senken-Definition des Wüstenplaners
   (24-m-Mittel) mit niedrigerer Schwelle.
2. **TWI:** `TWI = ln(a / max(tan β, 0,001)) ≥ 9,0` und `hang ≤ 12°`. Dabei ist `a` die D8-Einzugsfläche je Konturbreite in m, also
   Zellen × Zellbreite. Gerechnet wird auf `hoehe.f32`, vorher mit σ 1,5 m geglättet, im Feld + 64 m Rand. Der Schwellenwert ist
   [Annahme] und wird in T22-0 kalibriert.
3. **Nass-Lagen:** `nass = Gauss6m(1·Schlamm + 1·Algen + 0,5·Moos + 0,4·Lehm + 0,2·Kraut) ≥ 0,35`. Das ist die Nassmaske aus
   `sumpf_regeln.json`.

| Art | Biomgruppe | Wasserzelle | Land: Uferband ok, wenn | Feuchte-Ausnahme | Hang | sonst |
|---|---|---|---|---|---|---|
| **Rohrkolben** `SM_Rohrkolben_Horst_1–6`, `_Jung_1–3` | **standard** (aue, bergwald, elfenwald, heide, dschungel, kueste, fjord) | Tiefe ≤ 0,8 m | `d_w ≤ 6 m` und `dh ≤ 0,5 m` und `hang ≤ 15°` | `d_w ≤ 25 m` und `feucht` und `dh ≤ 1,0 m` und `hang ≤ 8°` | > 35° immer Verstoß | Verstoß |
| Rohrkolben | **sumpf** (Sumpf-Zellen + 30-m-Saum) | Tiefe ≤ 0,8 m | `d_w ≤ 6 m` und `dh ≤ 0,8 m` und `hang ≤ 15°` | überall, wenn `nass ≥ 0,35` **und** `mulde ≥ 0,3 m` und `hang ≤ 8°` (nasse Senke) | > 35° | Verstoß |
| Rohrkolben | **trocken** (wueste, canyon, oedland, lava) | Tiefe ≤ 0,8 m | `d_w ≤ 5 m` und `dh ≤ 0,5 m` und `hang ≤ 15°` | keine; nur Ausnahmefläche `quelle` | > 35° | Verstoß |
| Rohrkolben | **kalt** (gletscher, frost, tundra) | Tiefe ≤ 0,8 m | `d_w ≤ 5 m` und `dh ≤ 0,5 m` und `hang ≤ 15°` | keine | > 35° | Verstoß |
| **Binse** `SM_ToadRush_*` | standard | Tiefe ≤ 0,3 m | `d_w ≤ 15 m` und `dh ≤ 1,5 m` und `hang ≤ 20°` | überall, wenn `feucht` und `hang ≤ 12°` (Nasswiese, Fahrspur, Senke) | > 35° | Verstoß |
| Binse | sumpf | Tiefe ≤ 0,3 m | `d_w ≤ 18 m` und `dh ≤ 2,5 m` und `hang ≤ 20°` (Bultzone des Sumpfplaners) | überall, wenn `feucht` (inklusive Nassmaske) und `hang ≤ 12°` | > 35° | Verstoß |
| Binse | trocken | Tiefe ≤ 0,3 m | `d_w ≤ 8 m` und `dh ≤ 1,0 m` und `hang ≤ 25°` | keine; Sickerstellen nur als Ausnahmefläche `quelle` (gilt unabhängig vom Hang) | > 35° außer `quelle` | Verstoß |
| Binse | kalt | Tiefe ≤ 0,3 m | wie standard | wie standard (Schmelzwasser, Palsen-Schlenken) | > 35° | Verstoß |
| **Schwimmblatt** `SM_WaterPlant01–04` (und künftig Rembrandt Water Lily) | alle; Wasser inklusive Meer (Tang-Ersatz Nordküste) | Tiefe 0,2–2,0 m, sonst Hinweis; in `fluesse` nur Hinweis | an Land immer Verstoß | – | – | Verstoß |
| **`SM_lily_01_1/_2`** | – | nicht geprüft | nicht geprüft | – | – | bis §5 entschieden |
| **`GT_Schilf`** (`v_schilf`) | standard und kalt | Faktor 1 | `f_d`: 1 bis 4 m, linear 0 bei 12 m; `f_h`: 1 bis `dh` 0,3 m, linear 0 bei 1,0 m; `f = f_d·f_h` | – | – | 0 |
| GT_Schilf | sumpf | 1 | wie standard | `f = max(f; 0,5·clip((nass − 0,35)/0,3)·[hang ≤ 8°])` | – | 0 |
| GT_Schilf | trocken | 1 | `f_d`: 1 bis 3 m, 0 bei 6 m; `f_h` wie standard | – | – | 0 |
| GT_Schilf | Trockenbett (`d_alt ≤ 5 m` und `d_w > 12 m`) | – | 0 | – | – | 0 |

**Ausnahmeflächen `quelle`** (Urteil `ok_ausnahme`, keine Reparatur):

- Quell- und Nassflächen aus `antworten/bach_anfaenge/bach_anfaenge_plan.json` (Sickerquelle, Moorwiese, Felsquelle) und die
  Karst-Quelltopf- und Oasen-Orte der Sehenswürdigkeiten (`sehens/*/asset_bedarf.json`), jeweils als Polygon + 5 m.
- Liegt der zugehörige Bach schon gebaut in der Wasser-Wahrheit, greift ohnehin das Uferband.

**Begründung der Zahlen [Ableitung]:**

- 6 m (Rohrkolben) und 5 m (trocken) übernehmen die vorhandenen Planer-Bänder.
- `dh` 0,5 m entspricht der Marsch-Klasse (< 25 cm Grundwasser) plus 1-m-Raster-Toleranz.
- Binsen 15 m und 1,5 m decken die Nasswiese (25–50 cm) und die Wiese (50–100 cm) der ESD-Klassen ab, plus Böschungsfehler.
- Für den Sumpf übernehme ich die Bultzone (18 m, 2,5 m) des bestehenden Sumpfplaners.
- Die Hanggrenze 35° liegt oberhalb aller Planer-Grenzen (Wasserklassen ≤ 35° im Sumpfplaner).

---

## 4. Entscheidungsfolge (b) für die drei Fallgruppen

### 4.0 Vorbedingungen je Feld (vor jeder Reparatur)

- **V0 – Wasser-Wahrheit vollständig?** Für jedes Gewässer der alten Karte im Feld prüfen, ob noch ein Wasserakteur
  (`WaterBodyRiver`, See oder Teich) oder eine sichtbare Wasserfläche im Level liegt (E5-Fall).
  - Wenn ja: Die Wasser-Wahrheit ist lückenhaft. Erst dort nachtragen. Instanzen ≤ 25 m davon sind gesperrt und werden nicht
    repariert.
- **V1 – Kehren sie wieder?** Gilt `karte_wasser.r8` des Exports (`export/unreal/welt`) gleich der Wasser-Wahrheit? Gezählt werden
  abweichende Zellen je Feld.
  - Wenn nein: Der nächste Lauf von aue, wueste oder sumpf setzt die Pflanzen erneut. Die Karte muss vor dem nächsten Planerlauf
    erneuert werden. Diese Prüfung blockiert die Reparatur nicht, gehört aber in den Bericht.
- **V2 – lily:** `SM_lily_01_*` bleibt ausgenommen, bis §5 entschieden ist.

### 4.1 Ablauf je Instanz (Klassen Rohrkolben, Binse, Schwimmblatt)

```
1  Ausnahmefläche quelle?                         ja → ok_ausnahme (behalten)
2  in gebauter Wasserzelle?
     Schwimmblatt: Tiefe 0,2–2,0 → ok, sonst Hinweis
     Rohrkolben ≤ 0,8 m / Binse ≤ 0,3 m → ok, sonst Verstoß „zu_tief“ → entfernen
3  Schwimmblatt an Land                           → Verstoß → entfernen
4  hang > 35°                                     → Verstoß „hang“ (bzw. „trockenbett“) → entfernen
5  Uferband (Tabelle §3) erfüllt                  → ok
6  Feuchte-Ausnahme (Tabelle §3) erfüllt          → ok_feucht (behalten)
7  d_alt ≤ 5 m                                    → Fallgruppe TROCKENBETT  → 4.3
8  Biomgruppe sumpf                               → Fallgruppe SUMPF        → 4.4
9  sonst                                          → Fallgruppe FERN IM TROCKENEN → 4.2
```

### 4.2 Fern im Trockenen (C4, D4, D6, E6, B5 sowie die meisten Fälle 15–50 m)

1. V0 bestanden? Sonst sperren.
2. Entfernen mit Sicherung (§6.1). **Kein Ersatz.** Der Boden trägt dort schon Steppengras und Geröll; ein Ersatz würde nur Instanzen
   hinzufügen.
3. Wenn die Gruppe ≥ 6 Instanzen hat und ihr Schwerpunkt ≤ 25 m vom Wasser liegt: Kandidat für Versetzen in Phase 2 (§6.3).
4. Wüste, Canyon, Ödland: kein Versetzen in Rinnen ohne Wasser. Die Oase bekommt ihren Saum vom Planer (`schilf_rest`), nicht aus
   Altinstanzen.

### 4.3 Am Trockenbett (C4 typisch, F6, Teile von D6/E6; etwa 40 % der Fälle > 15 m)

1. V0: Ist das Bett wirklich trocken, oder fehlt nur der Eintrag in der Wasser-Wahrheit?
2. Wer schon in Schritt 6 als `ok_feucht` gilt, bleibt stehen. Das ist das Rest-Röhricht in einer nassen Senke ≤ 25 m vom heutigen
   Wasser (Standardbiome).
3. Alle übrigen werden entfernt und **ersetzt** (§6.2). Der Ersatz ist eine eigene protokollierte Zugabe, Dichte 1 Gruppe je 2
   entfernte Instanzen.
4. Ferat entscheidet je Bett über „Wasser zurück“ (§4.5). Bis dahin gilt 3. Die Zugabe ist rücknehmbar.
5. Das Trockenbett geht als Bett-Liste in den Bericht: Gewässer-ID der alten Karte, Länge, Pflanzen davor/danach, Anschluss an
   heutiges Wasser ja/nein, Einzugsfläche aus D8.

### 4.4 Sumpf-Zone (H5, Sumpfteil I5, 30-m-Saum)

1. Binsen: Bei `feucht` (Nassmaske, Mulde oder TWI) und `hang ≤ 12°` bleiben sie stehen. Das ist die Bult- und Nasswiesen-Logik des
   Sumpfplaners.
2. Rohrkolben: Sie bleiben nur in einer **nassen Senke** (`nass ≥ 0,35` und `mulde ≥ 0,3 m`, `hang ≤ 8°`). Auf trockener
   Gras- oder Laubmatte werden sie entfernt.
3. Kein Ersatz. Die Mittelschicht des Sumpfes setzt ohnehin Bulten, Moos und Schachtelhalm.
4. **H5-Grund [Hypothese aus dem Auftrag]:** Die Biom-Zone wurde statt der Wasserzelle gesetzt. Der Trockenlauf zeigt je Ebene, wie
   viele der 2 147 Fälle auf der Nassmaske liegen. Bei H5 mit 21 % Schlamm und 14 % Algen erwarte ich, dass 35–60 % bleiben
   [Annahme].

### 4.5 Kriterium „Soll eher Wasser zurück?“ (Frage 3)

Wasser zurück ist eine **Gestaltungsentscheidung für Ferat**. Ich empfehle es nur, wenn **alle** Punkte erfüllt sind:

1. **Biom:** standard (aue, bergwald, elfenwald, heide). In Wüste, Canyon und Ödland ist das trockene Gerinne der richtige Look:
   Ephemere Gerinne sind dort der Normalfall [S Pima County]. Diese bleiben trocken.
2. **Herkunft und Abfluss:** Das Bett hat einen plausiblen Anfang nach Antwort 19 (Quelltyp) und ist bergab an heutiges Wasser
   angeschlossen. Kein Gegengefälle, kein Ende „aus dem Nichts“ (Antworten 17/19).
3. **Einzugsfläche:** D8-Einzugsfläche an der Mündung ≥ 0,2 km² [Annahme; Vergleichswert für Dauerabfluss im humiden Biom, im Pilot
   gegen die gebauten Bäche prüfen: gebaute Bäche mit kleinerer Fläche senken die Schwelle].
4. **Lohnt der Aufwand:** Länge ≥ 150 m **und** sichtbar von Weg oder Sehenswürdigkeit **oder** ≥ 300 Wasserpflanzen-Instanzen am
   Bett. Grund: Jedes neue Gewässer bedeutet einen eigenen `WaterBodyRiver`, eine eigene SWR und einen eigenen Bake (Regel „ein Fluss
   je Gewässer“). Schaum gibt es nur an Fällen.
5. **Keine Spuren:** reine Landschaft, keine Mühle, kein Wehr.

Erfüllt ein Bett alle fünf Punkte, steht es mit Empfehlung auf der Bett-Liste. Ferat wählt. Alle anderen Betten bleiben trocken und
werden nach §4.3 bewachsen. **Meine Empfehlung:** C4 und F6 trocken lassen, solange 2 und 4 nicht belegt sind. Die
Trockenbett-Bepflanzung ist rücknehmbar, sie verbaut also nichts.

---

## 5. Frage 5: `SM_lily_01_1/_2`

**Belege [Repo]:**

- **Paket:** `Forest_Environment_Set` (NatureManufacture, 11/2019). Laut Paketbewertung Buchen (Pflanze bis tot), Schwarzkirsche,
  Totholz, Wurzeln, Laubdetails, Pilze, Gräser, Holzbau **und „Sumpf-Wasser“** (`vorlagen/doku/fab_pakete_bewertung_2026-10-10.md`).
  Das Paket hat also ein Wassermaterial. Eine Seerose ist darum nicht ausgeschlossen.
- **Nachbarnetze im Ordner** `Environment/Foliage/Models`: `SM_grass_01_*`, `SM_foliage_fern_01_*`, `SM_plant_01–03_*`,
  `SM_ivy_01_*`, `SM_shaggy_soldier_01_*` (Franzosenkraut), `SM_black_cherry_*`, `SM_beech_*`. Das ist Waldboden- und
  Ruderalflora mit gleichem Namensschema und gleicher Dreieckszahl (lily 139/160, Gräser 31–127, Farn 77–227).
- **Maße:** 0,53 × 0,50 × **0,30 m** bzw. 0,71 × 0,65 × 0,26 m. Die reinen Schwimmblatt-Netze sind flach: `SM_WaterPlant01–04`
  0,02 m, Rembrandt Water Lily VarB 0,01 m. Rembrandt-Varianten mit Blüte sind aber ebenfalls 0,29–0,85 m hoch. **Die Höhe allein
  entscheidet also nicht.**
- **Projektnutzung** (Deutung, kein unabhängiger Beleg): Foliage-Typen `FT_EL_MITT_lily_01_*` der Mittelschicht (Land) und
  `FT_Forest_Environment_Set__SM_lily_01_*` mit `align_to_normal` (Bodenausrichtung). Die Taxonomie führt die Netze als „blume“ mit
  dem Hinweis „laubwald“. Die Nordküste nutzt sie als Waldblume neben Windröschen und Maiglöckchen.
- **Botanik:** Die typische Lilie im Buchenwald ist Lilium martagon, Kennart der Fagetalia [S].

**Urteil:** **wahrscheinlich Landlilie (Hypothese)**. Ich setze sie nicht auf Seerose um, solange kein Netzbild vorliegt.

**Lokale Ein-Schritt-Prüfung:** `SM_lily_01_1` im Static-Mesh-Editor öffnen. Ein Screenshot in orthografischer Seitenansicht und einer
schräg von oben, dazu der Name der Basisfarbe-Textur ihres Materials.

- **Seerose**, wenn runde oder herzförmige Blätter mit Einschnitt flach in einer Ebene (≤ 3 cm) auf Pivot-Höhe liegen.
- **Landlilie**, wenn ein Stängel aufsteigt, mit Blättern entlang oder in Quirlen, oder mit Turban- oder Trichterblüte.

**Folgen der Entscheidung:**

- **Landlilie:** lily aus der Wasserpflanzen-Ausnahme von v3 streichen. Damit erfasst v3 „Pflanzen im Wasser“ die lily-Instanzen in
  Wasserzellen. In `sehens-katalog.md`/`sehens/aue` ist `SM_lily_01_1` als Seerosen-Ersatz eingetragen; diesen Eintrag ersetzt dann
  die Rembrandt Water Lily oder `SM_WaterPlant01–04`. Das ist ein Hinweis für den Katalog, ich ändere ihn hier nicht.
- **Seerose:** Klasse `schwimmblatt`. Instanzen an Land sind Verstoß.
- In beiden Fällen gilt laut Auftrag: Die 54,9 % ändern sich nicht.

---

## 6. Reparaturform (c)

### 6.1 Standard: Entfernen mit Sicherung je Instanz (wie v3)

- Je Instanz eine Sicherungszeile im v3-Format, ergänzt um:
  - `regel_version` „22.1“, `test_id`, `fall` (fern_trocken / trockenbett / sumpf / hang / zu_tief / land);
  - Messwerte `d_w`, `dh`, `hang`, `feucht`, `nass`, `mulde`, `twi`, `biom`;
  - Foliage-Typ und Ebene (Präfix), Netz, vollständige Transformation, Instanz-Hash.
- **Rücknahme** = die Zeilen wieder setzen. Im Pilot wird eine 1-%-Stichprobe zurückgesetzt und auf identische Transformation
  geprüft.
- Je verändertem Paket bzw. jeder World-Partition-Zelle ein Speicherbeleg.

### 6.2 Ersatz in Trockenbetten (nur Fallgruppe „trockenbett“)

Nur Bestandsnetze mit vorhandenen Foliage-Typen, keine neuen Assets. Je **2 entfernte** Instanzen setze ich 1 Ersatzgruppe am Ort
der ersten (Hash der Instanz-ID, deterministisch). Versatz ± 0,5 m, Yaw frei, Maßstab 0,8–1,2, 2–3 cm eingegraben. Jede Zugabe wird
mit Test-ID protokolliert; Rücknahme = protokollierte Zugaben löschen.

| Lage | Gruppe | Netze (Foliage-Typ) |
|---|---|---|
| standard, Bettrand (`d_alt` 1–5 m) | 2–3 Trockengras + 0–1 Ast + 0–2 Kiesel | `SM_dead_grass_01–03` (`FT_EL_MITT_dead_grass_*`), `SM_DryBranches_01` (`FT_EL_MITT_DryBranches_01`), `SM_SmallStonesPack_01/03` (`FT_EL_AUE_SmallStonesPack_01/03`) |
| standard, Bettrand mit `mulde ≥ 0,5 m` | zusätzlich 1 Schachtelhalm (Restfeuchte am Rand) | `SM_rough_horsetail_01–03` (`FT_EL_AUE_rough_horsetail_01` usw.) |
| trocken, Bettrand | 2–3 niedrige Trockenbüschel + 0–2 Kiesel | `SM_wk2oaeyqx_VarD/E/H/I` (0,22–0,25 m; `FT_EL_MITT_wk2oaeyqx_*`), `SM_SmallStonesPack_01/03` (`FT_EL_WUES_SmallStonesPack_*`) |
| trocken, Bettsohle (`d_alt = 0`, `hang < 10°`) | 1 Trockenbett-Platte | `SM_DryRiverBed_01/02` (`FT_EL_WUES_DryRiverBed_01/02`) |

- **Wunsch, anzulegen und optional:** „Rohrkolben vertrocknet“. Das ist ein brauner Horst mit geknickten Kolben, als Referenzbild aus einem Bildauftrag
  plus Blender-Ableitung von `SM_Rohrkolben_Horst_*`. Er würde ein Rest-Röhricht am Trockenbett glaubwürdig machen. Ohne ihn gilt:
  keine grünen Rohrkolben auf Riss-Schlamm.
- **Sperren für Ersatz:** nicht in Wasserzellen, nicht auf `karte_weg`, nicht > 25° Hang.

### 6.3 Versetzen nur für Gruppen (Phase 2, nach dem Pilotbild)

**Begründung:** Echte Röhrichte sind Gürtel entlang des Ufers. Eine geschlossene Gruppe ist schon ein Bestand; sie zu versetzen erhält
die gesetzte Form. Einzelne Streuinstanzen ans Ufer zu ziehen, würde dagegen Haufen an Stellen erzeugen, die die Planer und Antwort
20 (Uferdetail) schon füllen.

**Bedingungen:**

1. **Gruppe:**
   - ≥ 6 Verstöße derselben Art;
   - Single-Linkage ≤ 3 m (Gruppenradius der Planer 1,8–4 m);
   - Schwerpunkt `d_w ≤ 25 m`;
   - nicht Fallgruppe trocken.
2. **Ziel:** die nächste Wasserrand-Zelle (Quelle des Jump-Flooding).
   - Zielband Land 0–3 m mit `dh ≤ 0,3 m` oder Wasser 0–0,3 m (Rohrkolben) bzw. 0–0,15 m (Binse);
   - `hang ≤ 15°`, nicht `karte_weg`, nicht v3-Sperrfläche.
3. **Platz:** Im Umkreis 5 m um den Zielpunkt stehen < 3 Rohrkolben bzw. Binsen. Nach dem Versetzen bleibt die Dichte im Zielband
   ≤ 0,3/m² (`schilf_wasser` im Sumpfplaner).
4. **Abstände:**
   - Horst-Mittelpunkte ≥ 0,9 m untereinander;
   - ≥ 1,2 m zu vorhandenen Ufer- und Witcher-Instanzen (Regel des Sumpfplaners);
   - ≥ 4 m zu Stämmen von Ufergehölzen.
5. **Form:** Relative Lage erhalten. Schwerpunkt auf den Zielpunkt verschieben, Hauptachse (PCA) parallel zur Uferlinie drehen;
   z = Boden − 8 cm.
6. Sicherung wie §6.1 mit Alt- **und** Neu-Transformation. Scheitert eine Bedingung, wird entfernt.

---

## 7. Prüfcode (Referenz, Python 3 + NumPy)

Der Code ist eine Referenz für die lokale Prüfklasse. Er rechnet die Felder je Feld (`d_w` mit Spiegel der nächsten Wasserzelle,
`d_alt`, Hang, Mulde, TWI, Nassmaske), urteilt je Instanz, sucht Versetz-Kandidaten und rechnet den `GT_Schilf`-Faktor.

**Selbsttest** (synthetische Welt 240 × 160 m: Fluss mit Böschung, Aue-Mulde, altes Bett im Tal, Sumpfsenke mit Schlamm-Lage,
Steilwand, Wüstenstreifen):

- Jump-Flooding-Abstand gegen Brute-Force an 200 Zufallspunkten (unabhängiger Sollwert);
- 14 Fälle mit vorab festgelegtem Urteil;
- TWI-Rangfolge Bettsohle > Hang;
- Gruppensuche (8er-Gruppe wird Kandidat, 3 Einzelne nicht);
- Schilf-Faktor an 5 Punkten;
- Determinismus über zwei Läufe.

**Cloud-Ergebnis:** zweimal `SELBSTTEST OK  Regeln 22.1  Faelle 14  Cluster 1  Signatur 521ccd76eaca5822`.

**Laufzeit in der Cloud:** TWI auf 568² Zellen (2 m, Feld + 64 m Rand) 1,8 s; Jump-Flooding auf 1 136² Zellen (1 m) 7,9 s. Für 70
Felder ist der TWI auf 2-m-Raster ausreichend; die TWI-Schwelle gilt dann für 2-m-Zellen und wird dort kalibriert (ln 2 ≈ 0,7
Versatz zu 1 m).

**Lokale Anbindung:**

- Zellindex aus Weltkoordinaten wie in den Planern (Feldursprung + Rand).
- Der Aufrufer übergibt `biom` je Instanz und gibt im 30-m-Saum um Sumpf-Zellen „sumpf“.
- Lagen kommen als `lage_<Name>.r8 / 255`.
- `quellpoly` wird aus `bach_anfaenge_plan.json` und den Sehens-Orten gerastert.
- Für `v_schilf` wird `schilf_faktor` bilinear am Texelmittelpunkt (~2,3 m) abgetastet, `v' = round(v · f)`. Das Original
  `v_schilf.r8` bleibt als Sicherung; danach wird das Landschaftsgras lokal erneuert, wie bei der Grasmaske in 6i.

```python
# wasserpflanzen_regel.py - Referenz fuer die Pruefklasse "Wasserpflanze fern vom Wasser" (Antwort 22).
# Nur NumPy, keine Unreal-Importe. Aufruf: python -I wasserpflanzen_regel.py --selbsttest
# Raster: Zeile i = y, Spalte j = x, Zellgroesse ZELLE_M (lokal hoehe.f32: 1 m). Positionen in m ab Rasterursprung.
import hashlib
import sys

import numpy as np

ZELLE_M = 1.0
REGEL_VERSION = "22.1"

# ---------- Klassen (Netzname -> Art) ----------
# Feste Praefixe der 24 Netze aus dem Zensus (kein freies "rush", sonst trifft es z. B. "Brush").
_PRAEFIX = [
    ("rohrkolben", ("SM_Rohrkolben_",)),
    ("binse", ("SM_ToadRush_",)),
    ("schwimmblatt", ("SM_WaterPlant0", "Rembrandt_Water_Lily_")),
    ("lily_pruefen", ("SM_lily_01_",)),       # bis zur Netzpruefung (Frage 5) weder Wasser- noch Landregel
]


def art(netz):
    n = netz.split("/")[-1].split(".")[0]
    for a, praefixe in _PRAEFIX:
        if n.startswith(praefixe):
            return a
    return None


# Biom je Zelle aus eigner.r8 + welt.json (Konventionen par. 1). Aufrufer gibt "sumpf" auch fuer den 30-m-Saum um Sumpf-Zellen.
GRUPPE = {"sumpf": "sumpf", "wueste": "trocken", "canyon": "trocken", "oedland": "trocken", "lava": "trocken",
          "gletscher": "kalt", "frost": "kalt", "tundra": "kalt"}  # aue, bergwald, elfenwald, heide, dschungel, kueste, fjord: standard


def biomgruppe(biom):
    return GRUPPE.get(biom, "standard")


# ---------- Grenzwerte (Tabelle a der Antwort) ----------
# d_max: horizontaler Abstand zur gebauten Wasserzelle; dh_max: Boden minus Spiegel; hang_max in Grad.
# feucht_band: bis zu diesem Abstand darf die Feuchte-Bedingung den Abstand ersetzen (None = nie, inf = ueberall).
R = {
    ("rohrkolben", "standard"): dict(d_max=6.0, dh_max=0.5, hang_max=15.0, feucht_band=25.0, feucht_dh=1.0, feucht_hang=8.0),
    ("rohrkolben", "sumpf"):    dict(d_max=6.0, dh_max=0.8, hang_max=15.0, feucht_band=np.inf, feucht_dh=None, feucht_hang=8.0),
    ("rohrkolben", "trocken"):  dict(d_max=5.0, dh_max=0.5, hang_max=15.0, feucht_band=None),
    ("rohrkolben", "kalt"):     dict(d_max=5.0, dh_max=0.5, hang_max=15.0, feucht_band=None),
    ("binse", "standard"):      dict(d_max=15.0, dh_max=1.5, hang_max=20.0, feucht_band=np.inf, feucht_dh=None, feucht_hang=12.0),
    ("binse", "sumpf"):         dict(d_max=18.0, dh_max=2.5, hang_max=20.0, feucht_band=np.inf, feucht_dh=None, feucht_hang=12.0),
    ("binse", "trocken"):       dict(d_max=8.0, dh_max=1.0, hang_max=25.0, feucht_band=None),
    ("binse", "kalt"):          dict(d_max=15.0, dh_max=1.5, hang_max=20.0, feucht_band=np.inf, feucht_dh=None, feucht_hang=12.0),
}
TIEFE_MAX = {"rohrkolben": 0.8, "binse": 0.3}       # in einer Wasserzelle: Wassertiefe am Fuss
SCHWIMM_TIEFE = (0.2, 2.0)                          # Schwimmblatt nur in Wasser dieser Tiefe
HANG_HART = 35.0                                    # darueber nie (B5-Felsflaechen), ausser Quellpolygon
ALT_M = 5.0                                         # Abstand zur Altwasser-Schicht fuer Fallgruppe "trockenbett"
MULDE_SIGMA_M, MULDE_MIN_M = 24.0, 0.5
TWI_MIN = 9.0                                       # vorlaeufig, im Pilot kalibrieren (Abschnitt 4.3)
NASS_LAGEN = {"Schlamm": 1.0, "Algen": 1.0, "Moos": 0.5, "Lehm": 0.4, "Kraut": 0.2}   # = sumpf_regeln.json nass_maske
NASS_SIGMA_M, NASS_MIN = 6.0, 0.35


# ---------- Rasterhilfen ----------
def blur(a, sigma_m, zelle=ZELLE_M):
    """Gauss-Naeherung: drei Boxfilter je Achse (Kantenwerte fortgesetzt)."""
    s = sigma_m / zelle
    r = max(1, int(round((np.sqrt(4.0 * s * s + 1.0) - 1.0) / 2.0)))  # Boxradius fuer 3 Durchlaeufe
    out = a.astype(np.float64)
    for ax in (0, 1):
        for _ in range(3):
            p = np.pad(out, [(r + 1, r) if k == ax else (0, 0) for k in (0, 1)], mode="edge")
            c = np.cumsum(p, axis=ax)
            hi = np.take(c, np.arange(2 * r + 1, c.shape[ax]), axis=ax)
            lo = np.take(c, np.arange(0, c.shape[ax] - 2 * r - 1), axis=ax)
            out = (hi - lo) / (2 * r + 1)
    return out.astype(np.float32)


def hang_grad(h, zelle=ZELLE_M, sigma_m=1.5):
    gy, gx = np.gradient(blur(h, sigma_m, zelle), zelle)
    return np.degrees(np.arctan(np.hypot(gx, gy))).astype(np.float32)


def jfa(mask, max_m=64.0, zelle=ZELLE_M):
    """Abstand (m) zur naechsten True-Zelle + deren Index (Jump-Flooding wie in den Planern). Ausser Reichweite: inf, -1."""
    H, W = mask.shape
    ii, jj = np.indices((H, W))
    si = np.where(mask, ii, -1)
    sj = np.where(mask, jj, -1)
    s = 1
    while s * 2 <= max(H, W):
        s *= 2
    schritte = []
    while s >= 1:
        schritte.append(s)
        s //= 2
    schritte += [2, 1]
    for s in schritte:
        for di in (-s, 0, s):
            for dj in (-s, 0, s):
                if di == 0 and dj == 0:
                    continue
                ni = np.clip(ii + di, 0, H - 1)
                nj = np.clip(jj + dj, 0, W - 1)
                ci, cj = si[ni, nj], sj[ni, nj]
                ok = ci >= 0
                d_neu = np.where(ok, (ii - ci) ** 2 + (jj - cj) ** 2, np.iinfo(np.int64).max)
                d_alt = np.where(si >= 0, (ii - si) ** 2 + (jj - sj) ** 2, np.iinfo(np.int64).max)
                besser = d_neu < d_alt
                si = np.where(besser, ci, si)
                sj = np.where(besser, cj, sj)
    d = np.where(si >= 0, np.sqrt((ii - si) ** 2 + (jj - sj) ** 2) * zelle, np.inf)
    zu_weit = d > max_m
    d[zu_weit] = np.inf
    si[zu_weit] = -1
    sj[zu_weit] = -1
    return d.astype(np.float32), si, sj


def twi(h, zelle=ZELLE_M):
    """TWI = ln(a / tan b), a = Einzugsflaeche je Konturbreite (m), D8, tan b >= 0.001."""
    H, W = h.shape
    hs = blur(h, 1.5, zelle).astype(np.float64)
    acc = np.ones(H * W)
    flat = hs.ravel()
    order = np.argsort(-flat, kind="stable")
    nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for k in order:
        i, j = divmod(int(k), W)
        best, bk = 0.0, -1
        for di, dj in nb:
            a, b = i + di, j + dj
            if 0 <= a < H and 0 <= b < W:
                g = (flat[k] - hs[a, b]) / (zelle * (1.4142135 if di and dj else 1.0))
                if g > best:
                    best, bk = g, a * W + b
        if bk >= 0:
            acc[bk] += acc[k]
    gy, gx = np.gradient(hs, zelle)
    tanb = np.maximum(np.hypot(gx, gy), 0.001)
    return np.log(acc.reshape(H, W) * zelle / tanb).astype(np.float32)


# ---------- Felder je Feld (einmal rechnen) ----------
def felder(hoehe, wasser, spiegel, altwasser, lagen=None, quellpoly=None, zelle=ZELLE_M):
    """hoehe: hoehe.f32; wasser: bool gebaute Wasserzellen (Wasser-Wahrheit); spiegel: Spiegel je Wasserzelle (m, sonst nan);
    altwasser: bool Wasser der alten Karte; lagen: {Name: 0..1}; quellpoly: bool Quell-/Sehens-Ausnahmeflaechen."""
    d_w, si, sj = jfa(wasser, 64.0, zelle)
    sp_naechst = np.where(si >= 0, spiegel[np.maximum(si, 0), np.maximum(sj, 0)], np.nan)
    d_alt, _, _ = jfa(altwasser & ~wasser, 64.0, zelle)
    hang = hang_grad(hoehe, zelle)
    mulde = blur(hoehe, MULDE_SIGMA_M, zelle) - hoehe
    t = twi(hoehe, zelle)
    nass = np.zeros_like(hoehe, dtype=np.float32)
    for n, w in NASS_LAGEN.items():
        if lagen and n in lagen:
            nass += w * lagen[n]
    nass = blur(nass, NASS_SIGMA_M, zelle)
    feucht = ((mulde >= MULDE_MIN_M) & (hang <= 8.0)) | ((t >= TWI_MIN) & (hang <= 12.0)) | (nass >= NASS_MIN)
    q = quellpoly if quellpoly is not None else np.zeros(hoehe.shape, bool)
    return dict(hoehe=hoehe, wasser=wasser, spiegel=spiegel, d_w=d_w, sp=sp_naechst, d_alt=d_alt, hang=hang,
                mulde=mulde, twi=t, nass=nass, feucht=feucht, quelle=q, zelle=zelle)


def _bilinear(a, x, y, z):
    j, i = x / z - 0.5, y / z - 0.5
    j0, i0 = int(np.clip(np.floor(j), 0, a.shape[1] - 2)), int(np.clip(np.floor(i), 0, a.shape[0] - 2))
    fj, fi = np.clip(j - j0, 0, 1), np.clip(i - i0, 0, 1)
    return float((a[i0, j0] * (1 - fj) + a[i0, j0 + 1] * fj) * (1 - fi) + (a[i0 + 1, j0] * (1 - fj) + a[i0 + 1, j0 + 1] * fj) * fi)


# ---------- Urteil je Instanz ----------
def pruefe(netz, x, y, biom, F):
    a = art(netz)
    if a is None or a == "lily_pruefen":
        return dict(art=a, urteil="nicht_geprueft", fall="-", grund="keine Wasserpflanzenregel", aktion="behalten")
    z = F["zelle"]
    i = int(np.clip(y // z, 0, F["hoehe"].shape[0] - 1))
    j = int(np.clip(x // z, 0, F["hoehe"].shape[1] - 1))
    boden = _bilinear(F["hoehe"], x, y, z)
    hang, d_w, d_alt = float(F["hang"][i, j]), float(F["d_w"][i, j]), float(F["d_alt"][i, j])
    g = biomgruppe(biom)
    m = dict(art=a, gruppe=g, d_w=round(d_w, 2), hang=round(hang, 1), feucht=bool(F["feucht"][i, j]),
             nass=round(float(F["nass"][i, j]), 2), mulde=round(float(F["mulde"][i, j]), 2), twi=round(float(F["twi"][i, j]), 1))
    if F["wasser"][i, j]:
        tiefe = float(F["spiegel"][i, j]) - boden
        m["tiefe"] = round(tiefe, 2)
        if a == "schwimmblatt":
            ok = SCHWIMM_TIEFE[0] <= tiefe <= SCHWIMM_TIEFE[1]
            return dict(m, urteil="ok" if ok else "hinweis", fall="wasser", grund="Tiefe %.2f m" % tiefe, aktion="behalten")
        if tiefe > TIEFE_MAX[a]:
            return dict(m, urteil="verstoss", fall="zu_tief", grund="Tiefe %.2f > %.2f m" % (tiefe, TIEFE_MAX[a]), aktion="entfernen")
        return dict(m, urteil="ok", fall="wasser", grund="Flachwasser", aktion="behalten")
    if a == "schwimmblatt":
        return dict(m, urteil="verstoss", fall="land", grund="Schwimmblatt an Land", aktion="entfernen")
    dh = boden - float(F["sp"][i, j]) if np.isfinite(d_w) else np.inf
    m["dh"] = round(dh, 2) if np.isfinite(dh) else None
    if F["quelle"][i, j]:
        return dict(m, urteil="ok_ausnahme", fall="quelle", grund="Quell-/Sehens-Ausnahmeflaeche", aktion="behalten")
    if hang > HANG_HART:
        fall = "trockenbett" if d_alt <= ALT_M else "hang"
        return dict(m, urteil="verstoss", fall=fall, grund="Hang %.0f > %.0f Grad" % (hang, HANG_HART), aktion="entfernen")
    r = R[(a, g)]
    if d_w <= r["d_max"] and dh <= r["dh_max"] and hang <= r["hang_max"]:
        return dict(m, urteil="ok", fall="ufer", grund="Uferband", aktion="behalten")
    fb = r.get("feucht_band")
    if fb is not None and d_w <= fb and F["feucht"][i, j] and hang <= r["feucht_hang"]:
        if r.get("feucht_dh") is None or dh <= r["feucht_dh"]:
            if not (a == "rohrkolben" and g == "sumpf") or (F["nass"][i, j] >= NASS_MIN and F["mulde"][i, j] >= 0.3):
                return dict(m, urteil="ok_feucht", fall="sumpf" if g == "sumpf" else "feucht", grund="Feuchte-Bedingung", aktion="behalten")
    if d_alt <= ALT_M:
        fall, aktion = "trockenbett", "ersetzen_trockenbett"
    elif g == "sumpf":
        fall, aktion = "sumpf", "entfernen"
    else:
        fall, aktion = "fern_trocken", "entfernen"
    grund = "d_w %.1f m, dh %s m, Hang %.0f" % (d_w, m["dh"], hang)
    return dict(m, urteil="verstoss", fall=fall, grund=grund, aktion=aktion)


def cluster_versetzen(punkte, urteile, F, link_m=3.0, min_n=6, max_d_w=25.0):
    """Verstoesse in Gruppen (Single-Linkage <= link_m). Gruppen >= min_n mit Schwerpunkt <= max_d_w m vom Wasser -> Kandidat."""
    idx = [k for k, u in enumerate(urteile) if u["urteil"] == "verstoss" and u["fall"] != "zu_tief"]
    eltern = {k: k for k in idx}

    def wurzel(k):
        while eltern[k] != k:
            eltern[k] = eltern[eltern[k]]
            k = eltern[k]
        return k
    zellen = {}
    for k in idx:
        zellen.setdefault((int(punkte[k][0] // link_m), int(punkte[k][1] // link_m)), []).append(k)
    for (cx, cy), ks in zellen.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for k in ks:
                    for l in zellen.get((cx + dx, cy + dy), []):
                        if l > k and np.hypot(punkte[k][0] - punkte[l][0], punkte[k][1] - punkte[l][1]) <= link_m:
                            eltern[wurzel(k)] = wurzel(l)
    gruppen = {}
    for k in idx:
        gruppen.setdefault(wurzel(k), []).append(k)
    kandidaten = []
    for ks in gruppen.values():
        if len(ks) < min_n:
            continue
        cx = float(np.mean([punkte[k][0] for k in ks]))
        cy = float(np.mean([punkte[k][1] for k in ks]))
        i, j = int(cy // F["zelle"]), int(cx // F["zelle"])
        if F["d_w"][i, j] <= max_d_w:
            kandidaten.append(sorted(ks))
    return kandidaten


def schilf_faktor(F, biomgruppe_raster):
    """Faktor 0..1 fuer v_schilf. biomgruppe_raster: 0 standard/kalt, 1 sumpf (inkl. Saum), 2 trocken.
    Auf dem 1-m-Raster rechnen, fuer v_schilf (~2,3 m/Texel) bilinear am Texelmittelpunkt abtasten."""
    d = F["d_w"]
    dh = np.where(F["wasser"], 0.0, F["hoehe"] - np.nan_to_num(F["sp"], nan=1e9))
    trocken = biomgruppe_raster == 2
    d0, d1 = np.where(trocken, 3.0, 4.0), np.where(trocken, 6.0, 12.0)
    f_d = np.clip((d1 - d) / (d1 - d0), 0, 1)
    f_h = np.clip((1.0 - dh) / 0.7, 0, 1)
    f = np.where(F["wasser"], 1.0, f_d * f_h)
    sumpf = biomgruppe_raster == 1
    f_s = 0.5 * np.clip((F["nass"] - NASS_MIN) / 0.3, 0, 1) * (F["hang"] <= 8.0)
    f = np.where(sumpf, np.maximum(f, f_s), f)
    bett = (F["d_alt"] <= ALT_M) & (d > 12.0)
    return np.where(bett, 0.0, f).astype(np.float32)


# ---------- synthetischer Selbsttest ----------
def _welt():
    H, W = 160, 240
    y, x = np.indices((H, W)).astype(np.float32) + 0.5
    h = 20.0 + 0.02 * x                                   # sanft nach Osten steigend
    fluss = np.abs(y - 40) <= 4                           # gebauter Fluss y 36..44, Spiegel 19.5 + 0.02 x
    h = np.where(np.abs(y - 40) <= 8, h - 2.0 + 0.25 * np.abs(y - 40), h)   # Bett + Boeschung, Mitte 1,5 m tief
    spiegel = np.where(fluss, 19.5 + 0.02 * x, np.nan).astype(np.float32)
    h = h - 1.0 * np.exp(-(((x - 70) / 5.0) ** 2 + ((y - 58) / 5.0) ** 2))   # Nassmulde in der Aue, 14 m vom Ufer
    bett = (np.abs(y - 110) <= 3) & (x < 120)            # altes Bett, trocken (nur alte Karte)
    h = np.where((np.abs(y - 110) <= 30) & (x < 125), h + 0.05 * np.abs(y - 110), h)   # Talform zum Bett
    h = np.where(bett, h - 1.2, h)
    h = np.where((x > 200) & (y > 100), h + (x - 200) * 1.2, h)   # Steilwand Osten (~50 Grad)
    sumpf = (x > 130) & (x < 195) & (y > 70) & (y < 150)
    mulde = np.exp(-(((x - 160) / 14.0) ** 2 + ((y - 120) / 14.0) ** 2))
    h = np.where(sumpf, h - 1.5 * mulde, h)
    lagen = {"Schlamm": np.where(sumpf & (mulde > 0.25), 1.0, 0.0).astype(np.float32)}
    return h.astype(np.float32), fluss, spiegel, bett, lagen, sumpf


def _biom(x, y, sumpf):
    if sumpf[int(y), int(x)]:
        return "sumpf"
    return "wueste" if x < 60 else "aue"


def selbsttest():
    h, fluss, spiegel, bett, lagen, sumpf = _welt()
    F = felder(h, fluss, spiegel, bett, lagen)
    # 1) Abstand gegen Brute-Force (unabhaengiger Sollwert)
    wi, wj = np.nonzero(fluss)
    rng = np.random.default_rng(22)
    for _ in range(200):
        i, j = int(rng.integers(0, 160)), int(rng.integers(0, 240))
        soll = np.sqrt(((wi - i) ** 2 + (wj - j) ** 2).min())
        soll = soll if soll <= 64 else np.inf
        assert (np.isinf(soll) and np.isinf(F["d_w"][i, j])) or abs(F["d_w"][i, j] - soll) < 1e-3, (i, j, soll, F["d_w"][i, j])
    # 2) Faelle mit erwartetem Urteil
    faelle = [
        ("SM_Rohrkolben_Horst_2", 100.5, 47.5, "ok"),              # 3 m vom Ufer, flach
        ("SM_Rohrkolben_Jung_1", 100.5, 43.5, "ok"),               # im Flachwasser (0,6 m)
        ("SM_Rohrkolben_Horst_2", 100.5, 80.5, "verstoss"),        # 36 m vom Wasser, aue, trocken
        ("SM_Rohrkolben_Horst_6", 30.5, 80.5, "verstoss"),         # Wueste fern
        ("SM_Rohrkolben_Horst_3", 30.5, 110.5, "verstoss"),        # im alten Bett
        ("SM_ToadRush_02", 100.5, 52.5, "ok"),                     # Binse 8 m vom Ufer
        ("SM_Rohrkolben_Jung_2", 70.5, 58.5, "ok_feucht"),         # Rohrkolben in Aue-Mulde 14 m vom Ufer
        ("SM_ToadRush_02", 160.5, 120.5, "ok_feucht"),             # Binse in Sumpf-Mulde mit Schlamm
        ("SM_Rohrkolben_Horst_1", 160.5, 120.5, "ok_feucht"),      # Rohrkolben in nasser Sumpfsenke
        ("SM_ToadRush_010", 225.5, 130.5, "verstoss"),             # Felswand
        ("SM_WaterPlant02", 100.5, 40.5, "ok"),                    # Schwimmblatt Flussmitte (Tiefe 1,5 m)
        ("SM_WaterPlant02", 100.5, 60.5, "verstoss"),              # Schwimmblatt an Land
        ("SM_lily_01_1", 100.5, 80.5, "nicht_geprueft"),
        ("SM_LilyOfTheValley_02", 100.5, 80.5, "nicht_geprueft"),
    ]
    urteile = []
    for netz, x, y, soll in faelle:
        u = pruefe(netz, x, y, _biom(x, y, sumpf), F)
        urteile.append(u)
        assert u["urteil"] == soll, (netz, x, y, soll, u)
    assert urteile[4]["fall"] == "trockenbett" and urteile[4]["aktion"] == "ersetzen_trockenbett", urteile[4]
    assert urteile[3]["fall"] == "fern_trocken" and urteile[9]["fall"] == "hang"
    # 3) TWI: Bettsohle feuchter als Hang daneben
    assert F["twi"][110, 60] > F["twi"][95, 60] + 1.0, (F["twi"][110, 60], F["twi"][95, 60])
    # 4) Cluster: 8 Horste dicht bei 15-20 m vom Ufer -> Kandidat; 3 einzelne fern -> kein Kandidat
    pk = [(100.5 + dx, 62.5 + dy) for dx in (0, 1.5, 3) for dy in (0, 1.5, 3)][:8] + [(20.5, 80.5), (25.5, 85.5), (40.5, 90.5)]
    uk = [pruefe("SM_Rohrkolben_Horst_4", px, py, _biom(px, py, sumpf), F) for px, py in pk]
    kand = cluster_versetzen(pk, uk, F)
    assert len(kand) == 1 and len(kand[0]) == 8, kand
    # 5) GT_Schilf-Faktor
    bg = np.where(sumpf, 1, np.where(np.indices(h.shape)[1] < 60, 2, 0))
    f = schilf_faktor(F, bg)
    assert f[46, 100] == 1.0 and 0.8 < f[47, 100] < 1.0 and f[80, 100] == 0.0 and f[110, 30] == 0.0 and f[120, 160] > 0.0
    # 6) Determinismus
    sig = hashlib.sha256(repr(urteile).encode() + f.tobytes() + F["twi"].tobytes()).hexdigest()[:16]
    F2 = felder(h, fluss, spiegel, bett, lagen)
    f2 = schilf_faktor(F2, bg)
    u2 = [pruefe(n, x, y, _biom(x, y, sumpf), F2) for n, x, y, _ in faelle]
    assert hashlib.sha256(repr(u2).encode() + f2.tobytes() + F2["twi"].tobytes()).hexdigest()[:16] == sig
    print("SELBSTTEST OK  Regeln %s  Faelle %d  Cluster %d  Signatur %s" % (REGEL_VERSION, len(faelle), len(kand), sig))


if __name__ == "__main__":
    if "--selbsttest" in sys.argv:
        selbsttest()
    else:
        print("Aufruf: python -I wasserpflanzen_regel.py --selbsttest")
```

---

## 8. Erwartete Wirkung, Pilot, nächste Handlung

### 8.1 Erwartete Zahlen [Ableitung aus dem Zensus 18.10. 08:28; exakt erst nach T22-0]

| Gruppe (Zensus) | Anzahl | erwartet Verstoß | Begründung |
|---|---:|---:|---|
| > 50 m ohne H5 | ≈ 3 950 | ≈ 3 900 | keine Feuchte-Ausnahme so weit außer Nasswiesen-Binsen |
| H5 (Sumpf, 2 147) | 2 147 | ≈ 850–1 400 | 35–60 % bleiben auf der Nassmaske [Annahme] |
| 15–50 m | 3 585 | ≈ 2 500–3 200 | 10–30 % Feuchte-Ausnahmen (G5-Typ) |
| 5–15 m | 9 159 | ≈ 2 700–5 500 | Rohrkolben > 6 m ohne Senke; Binsen ≤ 15 m bleiben meist |
| ≤ 5 m mit `dh`/Hang-Verstoß | unbekannt | ≈ 500–1 500 | Anteil der 3 460 Fälle „> 3 m über Spiegel“ in Wassernähe, B5-Hänge |
| **Summe** | 67 990 | **≈ 10 500–15 500 (15–23 %)** | |

- **Nach der Reparatur:** > 15 m etwa 2–4 % statt 14,2 %; > 50 m ≤ 2 % statt 9,0 % (nur Sumpf-Nassmaske und Nasswiesen).
  „In einer Wasserzelle“ bleibt bei 37 327, abzüglich „zu_tief“.
- **Trockenbett-Ersatz:** etwa 4 000–5 000 entfernte Instanzen → 2 000–2 500 Gruppen ≈ 5 000–8 000 kleine Instanzen ohne Kollision.
- **`GT_Schilf`:** Von 514 129 Zellen ≥ 10 % fallen die > 15 m (27 %) außerhalb der Sumpf-Nassmaske auf 0, die 4–12 m werden
  ausgedünnt. 127 000 der Zellen > 15 m liegen in H5, I5 und F5; F5 (heide/aue) fällt ganz weg. Die wirksame Schilfdichte sinkt
  feldweit um etwa 35–55 % [Ableitung], je nach H5/I5-Nassanteil.

### 8.2 Pilot

**Feld C4.** Es hat 724 Fälle > 15 m, beide Trocken-Fallgruppen (C4_09 fern, C4 typisch Trockenbett), Sickerquellen aus Antwort 19,
und D5 als Kontrollnachbar. H5 läuft im Pilot nur als Zählung mit, ohne Reparatur.

Test-IDs: **T22-0** (Trockenlauf 70 Felder), **T22-C4-1** (Reparatur C4). Ausgangsstand-ID lokal vergeben.
Stand `vorbereitet → angewendet → geprüft`.

**Erfolg, wenn alle Punkte gelten:**

1. **Messweg (T22-0):**
   - Die Abstandsklassen reproduzieren den Zensus vom 18.10. 08:28 auf ±1 % (> 5 m 18 839, > 15 m 9 680, > 50 m 6 095, in Wasserzelle
     37 327).
   - Die D5-Kontrollen (Brücke) sind `ok`.
   - Der Selbsttest aus §7 läuft lokal mit derselben Signatur.
2. **Formal (T22-C4-1):**
   - In C4 0 Verstöße der Klassen Rohrkolben und Binse außer gesperrten V0-Fällen.
   - Sicherungszeilen = entfernte Instanzen; Zugaben = protokollierte Zeilen.
   - Die 1-%-Rücknahme-Stichprobe ist transformgleich.
   - Speicherbeleg je verändertem Paket.
3. **Fehlalarm-Kontrolle:**
   - 20 entfernte und 20 behaltene Instanzen in C4/D5 per Draufsicht oder Screenshot gegen die Rasterwerte geprüft.
   - 0 Entfernungen in Wasserzellen oder im 6-m-Uferband mit `dh ≤ 0,5 m`.
4. **Bild** (gleiche Kamera, gleiches Licht):
   - C4_09 zeigt keinen Horst mehr im Steppengras.
   - C4 typisch zeigt das Bett mit Trockengras und Kies, ohne grüne Rohrkolben.
   - Die D5-Brückenansicht ist unverändert.
   - Vergleichsstelle nach `pruefung.md`: der D5-Rand zu C4.

**Abbruch:** Weicht der Messweg in T22-0 um mehr als 1 % ab, oder liegen > 2 % der C4-Verstöße in V0-Sperrflächen, dann wird nicht
repariert. Erst die Wasser-Wahrheit klären.

### 8.3 Nächste Handlung (eine, lokal)

**T22-0 ausführen.** Die Prüfklasse läuft mit Regeln 22.1 über alle 70 Felder, nur lesend.

**Ausgabe je Feld:**

- Art × Fallgruppe × Ebene (Foliage-Typ-Präfix);
- V0-Liste (Altwasser mit Wasserakteur im Level) und V1-Zellabweichung `karte_wasser` ↔ Wasser-Wahrheit;
- lily-Instanzen Wasser/Land;
- Bett-Liste (§4.3);
- TWI-Kalibrierung.

**TWI-Kalibrierung:** Die Schwelle trennt ≥ 80 % der Landzellen 0–3 m vom gebauten Wasser in C4/D5 (nass) von ≥ 90 % der Zellen
> 100 m vom Wasser in D4/E6 (trocken). Sie wird übernommen, wenn sie zwischen 7 und 12 liegt. Sonst wird der TWI-Zweig abgeschaltet;
dann gelten nur Mulde und Nassmaske.

**Erfolgskriterium:** 8.2 Punkt 1. Danach folgt T22-C4-1.

**Rückfrage an Ferat (blockiert T22-0 nicht):** Sollen Betten in der Aue, die alle Kriterien aus §4.5 erfüllen, wieder Wasser
bekommen, oder bleiben alle Betten trocken? Ohne Antwort gilt „trocken mit Trockenbett-Bewuchs“, rücknehmbar.

---

## 9. Was fehlt bis Witcher 4

Messlatte: Witcher-4-Techdemo (UE5, State of Unreal 2025). Belege in `boden-kleinzeug-gras.md`. Sortiert nach Wirkung:

1. **Eine Quelle der Wahrheit statt Nachreparatur.** In der Demo wird Vegetation zur Laufzeit per GPU-PCG aus Gelände- und Biomdaten
   erzeugt (Unreal Fest Stockholm 2025, „Runtime PCG in The Witcher 4“). Bei uns stehen gespeicherte Instanzen aus mehreren Ebenen
   gegen veraltete Wasserkarten. Solange `karte_wasser`, Houdini-Ebene und Wasser-Wahrheit auseinanderlaufen (V1), entstehen solche
   Fehler neu. Ziel: Planer und PCG lesen nur die Wasser-Wahrheit plus ein Feuchtefeld (Mulde/TWI/Nassmaske aus §3).
2. **Uferzonierung nach Wassertiefe statt nach Abstand.** Witcher-Ufer haben Röhricht im Wasser, Schwimmblätter, Seggen und einen
   nassen Schlammsaum. Bei uns fehlen Gürtel im Wasser; der Sumpfplaner kann es, angewendet ist es nicht überall.
3. **Röhricht-Assets:**
   - Die Horste ohne Kolben lesen sich im Trockenen als Agave [Bild].
   - ToadRush hat 15–29 k Dreiecke ohne Nanite.
   - Es fehlen Nanite-Röhricht mit Kolben und Wind (Demo: Nanite Foliage mit Skelett-Wind) und eine vertrocknete Variante (anzulegen).
4. **Feuchte im Bodenmaterial:** dunkles Nassband an Ufer und Mulden; Riss-Schlamm nur dort, wo das Bett wirklich trocken ist, mit
   RVT-Übergang. Heute widersprechen sich Textur (Riss) und Bewuchs (Röhricht).
5. **Fernwirkung `GT_Schilf`:** 2,3 m/Texel ist zu grob für schmale Ufergürtel. In der Demo trägt Nanite-Geometrie aus Runtime-PCG
   auch die Ferne; bei uns trägt nur die Dichtekarte.

---

## 10. Quellen (abgerufen 18.10.2026)

**Zugriff:**

- WebFetch scheiterte bei `fs.usda.gov`, `plants.usda.gov`, `www1.usgs.gov`, `en.wikipedia.org` und `courses.washington.edu`
  (DNS-Fehler).
- Der direkte Abruf über den Proxy wurde für `plants.usda.gov`, `en.wikipedia.org`, `fs.usda.gov` (FEIS), `fab.com`,
  `plantsoftheworldonline.org`, `gbif.org` und `cabidigitallibrary.org` abgewiesen (403).
- Alle Aussagen unten stammen deshalb aus **Suchauszügen [S]**. Keine Vollseite wurde gelesen.

**Typha:**

- [Pladias: Typhetum latifoliae](https://pladias.cz/en/vegetation/description/Typhetum%20latifoliae) [S] – 10–60 (–100) cm, kann im
  Sommer austrocknen.
- [USGS NVCS, Cattail-Einheit 871240](https://www1.usgs.gov/csas/nvcs/unitDetails/871240) [S] – 30–100 cm Überstau, maximaler Wuchs
  bei etwa 50 cm (Grace & Wetzel 1981).
- [USDA NRCS Plant Guide Typha latifolia](https://plants.usda.gov/DocumentLibrary/plantguide/pdf/pg_tyla.pdf) [S] – flacher als
  T. angustifolia, verträgt Pegelschwankungen.
- [USU Extension: Broadleaf Cattail](https://extension.usu.edu/rangeplants/grasses-and-grasslikes/broadleaf-cattail) [S] – Keimung
  in Flachwasser und auf feuchtem Schlamm.
- [Virginia Tech, Item 10919/72993](https://vtechworks.lib.vt.edu/handle/10919/72993) [S] – Bodenfeuchte senkt Biomasse und
  Rhizomlänge; Grundwasserstand korreliert mit der Biomasse.
- [USDA NRCS Ecological Site Description R010XY030ID (edit.jornada.nmsu.edu)](https://edit.jornada.nmsu.edu/catalogs/esd/010X/R010XY030ID) [S]
  – Marsch < 10 in, Nasswiese 10–20 in, Wiese 20–40 in, trockene Wiese > 40 in; Marsch von Breitblättrigem Rohrkolben dominiert.
  Welche der gefundenen ESD-Seiten die Klassen enthält, war im Auszug nicht eindeutig.
- [Pladias/FloraVeg Faktenblätter](https://pladias.cz/en/factsheet/default/4984) [S] – Ellenberg F: Typha latifolia 10, Juncus
  bufonius 8. Die genaue Zuordnung der Faktenblatt-ID zur Art war im Auszug nicht sicher.
- [NatureServe/USGS NVCS 688694, Typha domingensis](https://www1.usgs.gov/csas/nvcs/unitDetails/688694) [S] – Sonora, Mojave, Great
  Basin; alkalisches Alluvium.
- [Univ. of Arizona: Salinity limits, Cienega de Santa Clara](https://experts.arizona.edu/en/publications/salinity-limits-of-vegetation-in-cienega-de-santa-clara-an-oligot/) [S]
  – etwa 6 g/l TDS.

**Juncus:**

- [EUNIS 3099 Toad-rush swards](https://eunis.eea.europa.eu/habitats/3099) [S] und [EUNIS 3098](https://eunis.eea.europa.eu/habitats/3098) [S]
  – temporäre Tümpel, Fahrspuren, Abtrocknungsphase.
- [USGS WARC PlantID 706, Juncus bufonius](https://warcapps.usgs.gov/PlantID/Species/Details/706) [S] – nasse Wegränder, Senken,
  Gräben; einjährig; FACW.
- [NIWA factsheet Juncus bufonius](https://niwa.co.nz/sites/default/files/juncus_bufonius_factsheet.pdf) [S] – offene, gestörte
  Standorte, trocken bis nass.
- [EUNIS 3963 Soft rush meadows](https://eunis.eea.europa.eu/habitats/3963) [S] und
  [UF/IFAS AG335](https://edis.ifas.ufl.edu/publication/AG335/pdf) [S] – J. effusus in saisonal nassen Weiden.
- [USGS NVCS 899220](https://www1.usgs.gov/csas/nvcs/unitDetails/899220) bzw. [849120](https://www1.usgs.gov/csas/nvcs/unitDetails/849120) [S]
  – Sickerquell-Gesellschaft Arid West mit Juncus arcticus; welcher der beiden Treffer, war im Auszug nicht eindeutig.
  [Hanging garden (Wikipedia)](https://en.wikipedia.org/wiki/Hanging_garden_(habitat)) [S].

**Nymphaea:**

- [Pladias: Nymphaeetum albae](https://pladias.cz/en/vegetation/description/Nymphaeetum%20albae) [S] – 50–100 cm, nicht in
  fließendem Wasser.
- [RHS Nymphaea alba](https://www.rhs.org.uk/plants/11623/nymphaea-alba-h/details) [S] – Gartenangabe.

**Trockenbetten:**

- [Mountain Scholar: riparian vegetation in ephemeral streams of the Sonoran Desert](https://mountainscholar.org/items/69e7a28e-9a07-4c78-b9fc-12a3bd24730d/full) [S]
- [USFS Treesearch 44422](https://research.fs.usda.gov/download/treesearch/44422.pdf) [S] – Pima County, Salix gooddingii mit
  Grundwasser > 4 m.

**TWI:**

- [SAGA Tool-Doku Topographic Wetness Index](https://saga-gis.sourceforge.io/saga_tool_doc/9.3.1/ta_hydrology_20.html) [S]
- [Ali et al. 2013 (ESPL), Vergleich von Nässe-Indizes](https://water.usask.ca/hillslope/documents/pdfs/2013/13-16%20Ali%20et%20al%202013%20A%20comparison%20of%20wetness....pdf) [S]
  – kein allgemeingültiger Schwellenwert, gebietsweise Kalibrierung.

**Lilie:**

- [IPR-Datenbank Lilium martagon](https://iprdatabase.eu/db/recent/plants/lilium-martagon) [S] und
  [EUNIS 21178 Sainte-Baume Fagus forest](https://eunis.eea.europa.eu/habitats/21178) [S] – Buchenwald-Art (Fagetalia).
- Die Fab-Seite des Forest Environment Set war nicht abrufbar (403). Paketinhalt nur aus `vorlagen/doku/fab_pakete_bewertung_2026-10-10.md`.

**Repo** (Stand Commit b844a46 bzw. 0595869):

- `vorlagen/daten/netze.csv`, `inventar.json`, `biome_je_feld.md`; `antworten/assets-taxonomie.json`;
- `antworten/skripte/{aue,sumpf,wueste_ergaenzung,elfenwald,dschungel,heide_tundra,nordkueste}_regeln.json`;
- `antworten/verteilung-KONVENTIONEN.md`, `verteilung-sumpf.md`, `19-bach-anfaenge-quellen.md`, `boden-kleinzeug-gras.md`.
