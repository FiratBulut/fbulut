# Antwort zu 16g Nachtrag 2 – Feinwerte, Hindernis-Filter, Texturformat, Rückfragen 2–5

Stand 13.10.2026. Grundlage sind Ferats Nachtrag `auftraege/16g-nachtrag2-feinwerte-und-rueckfragen.md` (Befunde N1–N7,
Endstand 10:15, Antworten auf unsere Rückfragen und Abschnitt 4 mit **F1/F2**, 11:12–11:29), unsere Antworten
[`16g-swr-steiler-bergbach.md`](16g-swr-steiler-bergbach.md) und [`16g-nachtrag-ursache-gefunden.md`](16g-nachtrag-ursache-gefunden.md),
[`16f-rueckfrage-epic-parameter-lokal.md`](16f-rueckfrage-epic-parameter-lokal.md) sowie `skripte/fluss_sim/` (jetzt Regeln v11).

**Kennzeichnung:**
- [Befund N…/F…]: Ferats Messung
- [Doku]: Epic-API- bzw. Doku-Seite, **nur als Suchauszug** (`dev.epicgames.com` und `docs.unrealengine.com` sind aus der Cloud
  weiter gesperrt, DNS-Fehler)
- [Forum]: Epic-Forum, Suchauszug
- [16a], [16f], [16g]: frühere Antworten im Repo
- [Ableitung]: aus Belegen und Befunden geschlossen bzw. gerechnet
- [unsicher]: nicht belegt, im Test klären

---

## Kurzfazit

1. **Nachfüllrate 0,3 ist die neue Vorgabe** (Regeln v11). Unsere 0,02 aus 16f lag weit unter der gemessenen Schwelle (0,1
   und 0,2 bleiben bei s 76 stehen). Testreihe jetzt **0,3 / 0,4**.
   - Deutung [Ableitung]: Die Front läuft, solange Nachfüllen plus Zufluss die Verluste an der knappen Lippe s 72–81 decken.
   - Der Antrieb des Nachfüllens ist **Rate × Fehlhöhe** (Spline-Spiegel minus Wasserstand). Deshalb wirkt eine um 10 cm
     gesenkte Spline wie eine um etwa 20 % kleinere Rate (bei 0,5 m Tiefe). Das erklärt N7 (−10 cm → Front s 72) und den
     Endstand (+10 cm oben → läuft).
   - **0,3 liegt genau auf der Schwelle.** Die Rate 0,4 gibt Reserve und macht die Spline-Offsets vermutlich unnötig.
2. **F1 und F2 sind eingearbeitet:**
   - `remove_outside_spline_amount` **0** (F1: 50 nimmt 38 % des Überlaufs, macht das Bett aber 15 % flacher).
   - **Band = Bett + 2 m** (neues Feld `band_zugabe_m` 2): F2 mit Band = Bett blieb bei s 59 stehen.
   - **Regel Wasser-Info neu: Pixel ≤ schmalstes Band / 12** (Ferats Vorschlag). **Teiler 6 auf das Bett reicht nicht.**
   - Für C2 (1,6-m-Rinne): Band 3,6 m / 12 = 0,30 m; die Zone 4096 hat 0,295 m und hält die Regel knapp. F6 (2048) ist
     damit nicht nötig.
3. **Spline-Höhen wirken global (N6).** Eine 16-Bit-Rundung relativ zum tiefsten Punkt kann das **in C2 nicht** erklären,
   weil die C2-Zone auf 32 Bit steht (Rundung dann ~0,001 cm) [Ableitung].
   - Wahrscheinlicher ist: Bei 0,3 liegt der Lauf auf der Kippe, und schon kleine Unterschiede zwischen zwei Läufen
     entscheiden.
   - Prüfen: N3 und N6 je zweimal wiederholen, dazu N6 mit 0,4 (Abschnitt 1.3).
4. **Hindernis-Filter N5 ist Regel** (`swr.hindernis_filter`):
   - ohne Lippen-, Rand- und Bettfelsen;
   - Teil ≤ 40 % der Bettbreite;
   - je Meter zusammen ≤ 50 %;
   - ausgefilterte Teile bleiben Deko ohne Wasser-Kollision.
   - 2-m-Lauf: **40 221 → 20 225** Objekte mit Wasser-Kollision (12 923 nach Rolle, 3 526 zu breit, 3 522 über dem
     Meter-Budget, 25 in einem anderen Gewässer). WH-Instanzen 39 239 → 19 864.
5. **`source_size` 300 cm ist jetzt Bach-Mindestwert:** `source_size_cm` = max(300, Breite an der Quelle). Das ändert 55 von
   197 SWR. Spline-Offsets je Abschnitt kommen **nicht** in den Export (Abschnitt 4.4).
6. **Frage 2 – C2 wieder auf 16 Bit? Nein.**
   - Half Float hat 10 Bit Mantisse. Bei 30–190 m (3 000–19 000 cm) sind das Stufen von **2–16 cm**, ab 163,84 m 16 cm.
   - Speichert die Wasser-Info Z relativ zur Spanne der Zone, sind es in C2 (155 m Spanne) **7,6 cm**.
   - Beides liegt über den 10 cm, die in N7 den Lauf kippen, bzw. nahe daran.
   - **Neue Regel `half_precision_ok`** je Zone: Höhenstufe ≤ 4 cm, also Wasser unter 81,92 m und Spanne unter 81,92 m.
   - Weltvorschlag: **12 von 35 Zonen brauchen 32 Bit.** Das ergibt 1 963 MB statt 1 379 MB (alles 16 Bit) bzw. 2 757 MB
     (alles 32 Bit). Für C2 kostet 32 Bit 256 statt 128 MB.
7. **Frage 3:** Mit `is_spatially_loaded` aus belegen alle Zonen dauernd Speicher. Beim Vorschlag wären das **1,4–2,8 GB**.
   - **Empfehlung:** Feine Zonen räumlich laden. Grundzone und Meer bleiben immer geladen.
8. **Frage 5:** Den genauen CVar-Namen konnte ich **nicht belegen**.
   - Den Namen `r.Water.WaterInfo.RenderTargetResolutionMax` gibt es nur im Text der API-Doku [Doku].
   - Belegt sind andere `r.Water.WaterInfo.*`- und `r.Water.WaterMesh.*`-Namen.
   - Die Abfrage per Python liefert für unbekannte Namen 0. Abschnitt 6 zeigt, wie ihr die Liste im Editor auslest.
9. **Export und Prüfer (v11):**
   - Der Prüfer meldet **0 FEHLER, 0 WARNUNG, 74 HINWEIS**; zwei Läufe sind byte-gleich (183 Dateien).
   - Der **Objektteil des Fingerabdrucks** ändert sich bei **194 von 197 SWR**, die `sim_vorgaben` bei allen 197.
   - Gelände und Splines bleiben gleich. **Alle SWR neu backen.**

---

## 1. Deutung N1–N7, F1, F2

### 1.1 Was die Befunde zeigen

| Lauf | Rate | Spline | Band, Entfernen | Front | Lesart [Ableitung] |
|---|---|---|---|---|---|
| N2 / N1 | 0,1 / 0,2 | Plan | Bett + 2 m, 0 | s 76, 10 min unverändert | Antrieb zu klein für die knappe Lippe s 72–81 |
| **N3** | **0,3** | Plan | Bett + 2 m, 0 | Mündung (~4 min bei 36 fps) | Schwelle überschritten |
| N4 | 0,3 | Plan | + alle 1 718 Hindernisse | hinter zwei 1-m-Lippenfelsen | 2 × 1 m in 2 m Bett = 100 % zu: Damm |
| N5 | 0,3 | Plan | Hindernisse gefiltert | durch, 99,8 % nass | Filter hält das Bett offen |
| N6 | 0,3 | Kiesbett −12 cm | Bett + 2 m, 0 | **s 81** | Änderung weit talab wirkt oben (global) |
| N7 | 0,3 | überall −10 cm | Bett + 2 m, 0 | s 72 | 10 cm weniger Fehlhöhe ≈ 20 % weniger Antrieb |
| Endstand | 0,3 | oben +10, Kies −12 cm | Kies = Bett, 0 | 783 von 788 | +10 cm oben ≈ +20 % Antrieb |
| F1 | 0,3 | Endstand | Entfernen **50** | 748 (C3-Rand) | Überlauf −38 %, Bett 15 % flacher |
| **F2** | 0,3 | Endstand | **Band = Bett**, Entfernen 50 | **s 59**, Bett 4 % nass | zu schmales Band (und/oder Verlust am Bandrand) |

### 1.2 Warum es bei 0,3 eine Schwelle gibt [Ableitung, Mechanismus unsicher]

`match_spline_height_amount` ist laut Epic eine **Rate**: Wasser wird dort nachgefüllt, wo die Simulation unter dem
Spline-Spiegel liegt [16f, Epic lokal]. Die genaue Formel und Einheit sind nicht belegt. Die Befunde passen zu folgendem
Bild:

1. **Zufuhr je Zelle ≈ Rate × (Spline-Spiegel − Wasserstand).** Das Nachfüllen wirkt offenbar nur dort, wo schon Wasser ist
   (an der Front und dahinter).
   - Sonst hätte auch 0,02 das ganze Band in 10 min gefüllt: Bei einer Rate je Sekunde wären das 50 s Zeitkonstante.
   - N1/N2 zeigen dagegen 10 min Stillstand.
2. **Verluste in der steilen Rinne:**
   - An der knappen Lippe s 72–81 verteilt sich das Wasser als dünner, schneller Film.
   - Zellen unter der Trocken-Schwelle der Simulation zählen als trocken: Das Wasser dort ist verloren bzw. fließt nicht weiter.
   - Mit `remove_outside` > 0 wird Wasser am Bandrand gelöscht.
   - Reibung bremst nur, sie löscht kein Wasser.
3. **Front steht, wenn Zufuhr < Verlust** an der kritischen Stelle. Die Zufuhr wächst linear mit der Rate, der Verlust hängt an
   der Geometrie. Es gibt also eine Grenzrate **r\*** je Stelle; für die Lippe s 72–81 liegt sie zwischen 0,2 und 0,3.
4. **Die Spline-Höhe wirkt wie die Rate**, weil sie die Fehlhöhe verschiebt. Bei einer Plan-Tiefe von etwa 0,5 m gilt:
   - ±10 cm ≈ ±20 % Antrieb;
   - N7 (−10 cm bei 0,3) ≈ Rate 0,24 → unter der Schwelle (passt);
   - Endstand (+10 cm oben) ≈ Rate 0,36 → darüber (passt).
5. **F1/F2 passen dazu:**
   - Mit Entfernen 50 verliert das Bett Wasser am Bandrand. Es wird 15 % flacher (F1).
   - Ist das Band zusätzlich nur so breit wie das Bett (F2), überwiegt der Verlust schon bei s 59.

**Folge:** Gemessen wird an der Kippe. Kleine Unterschiede (Reset-Zustand, Bildrate, Hindernisse, Offsets) entscheiden, ob
die Front durchläuft. Mit 0,4 liegt man um ~33 % über der gemessenen Schwelle. Das entspricht etwa +15 cm Spline-Offset
[Ableitung].

**Bildrate:** Wenn die Live-Simulation je Bild eine feste Zahl von Schritten rechnet, hängt nur die **Dauer** an der Bildrate,
nicht das Ergebnis [unsicher]. Deshalb nicht nach Minuten, sondern nach Bildern messen (z. B. ≥ 9 000 Bilder ≈ 4 min bei
36 fps) und die Bildrate notieren.

### 1.3 Warum wirken Spline-Höhen global? (N6)

Ferats Hypothese: Höhenrundung relativ zum tiefsten Punkt (16-Bit-Quantisierung).

| Mögliche 16-Bit-Stelle | Wie gerundet | Erklärt N6? |
|---|---|---|
| Wasser-Info der Zone (Z Wasser, W Boden) | Half Precision **aus** in C2 → 32 Bit: Stufe ~0,001 cm | **nein** (C2 hatte 32 Bit) |
| dieselbe mit Half Precision an | absolut 8 cm (82–164 m) bzw. 16 cm (> 164 m); relativ zur Spanne 7,6 cm; ändert sich der tiefste Punkt, verschiebt sich jede Stufe | ja, wenn relativ gespeichert wird – **aber nicht im C2-Lauf** |
| Bodenerfassung der SWR (Niagara Scene Capture, Half Float, „saturated at 65504“) [16a, Forum] | absolut in cm: 8/16 cm, unabhängig von der Spline | nein (hängt nicht an der Spline) |

- Die Zone kennt die Felder `WaterHeightExtents` (FVector2f), `GroundZMin`, `CaptureZ` und `CaptureZOffset`. Letzteres wird
  „nach dem größten Z aller Wasserkörper der Zone“ angewandt [Doku].
  - Das spricht dafür, dass die Wasser-Info die Höhen **relativ** zu einem Bereich der Zone speichert, der vom höchsten bzw.
    tiefsten Wasserkörper abhängt [Ableitung].
  - Belegt ist es nicht.
- **In 32 Bit ist das ohne Wirkung.** N6 hat deshalb vermutlich eine andere Ursache [Ableitung]:
  1. **Lauf an der Kippe:** Bei 0,3 kann ein zweiter, gleicher Lauf anders ausgehen. N3 und N6 sind je ein Lauf.
  2. **Ein globaler Wert hängt an der Spline**, z. B. der Höhenbereich der Zone (`WaterHeightExtents`) oder der Ausgangsstand
     nach Reset [unsicher].
- **Test (je 5 min bzw. 9 000 Bilder, Zone 4096, 32 Bit):**

  | Lauf | Rate | Spline | Erwartung, wenn Kippe | Erwartung, wenn global |
  |---|---|---|---|---|
  | N3-W1, N3-W2 | 0,3 | Plan | Mal durch, mal s 76–81 | immer durch |
  | N6-W1 | 0,3 | Kies −12 cm | wie N3-W | immer s 81 |
  | N6-0,4 | 0,4 | Kies −12 cm | durch | durch (mehr Reserve) |
  | N6-M | 0,3 | nur letzte 20 m (Mündung) −12 cm | wie N3 | s 81 (tiefster Punkt geändert) |

  Bleibt N6-M bei s 81 stehen, ist der **tiefste Punkt** der Hebel; dann hängt die Simulation an einem globalen Höhenbereich.

### 1.4 F1 und F2

- **F1 (Entfernen 50):** Ferats Folgerung trifft zu, also Endstand 0. Überlauf außerhalb des Bands zeichnet das Netz in WCBS
  nicht. Ein flacheres Bett (Tiefe Mitte 0,47 statt 0,55 m, Kies 0,37 statt 0,53 m) sieht man dagegen.
  - Die Front bei 748 ist die Grenze des C3-Flusses und damit richtig.
- **F2 (Band = Bett + Entfernen 50):** Die Front steht bei s 59, das Bett ist zu 4,1 % nass.
  - Ferats Schluss: Teiler 6 (6,8 Pixel quer) reicht nicht; mit Bett + 2 m (12–14 Pixel) läuft es.
  - **Übernommen:** Band = Bett + 2 m, Pixel ≤ Band / 12.
  - Hinweis [Ableitung]: F2 hat zwei Dinge zugleich geändert, das schmale Band **und** Entfernen 50 am Bandrand. Beides senkt
    die Bilanz aus 1.2. Ein Lauf F2b (Band = Bett, Entfernen 0) würde trennen, was davon die Pixel waren.
  - F2b ist **nicht nötig**, weil Bett + 2 m funktioniert. Wir nennen Teiler 6 deshalb nicht mehr als ausreichend.

---

## 2. Neue Werte für F1, F2 und F6

| Punkt | v10 | **v11** | Grund |
|---|---|---|---|
| `match_spline_height_amount` | 0,02 (Test 0/0,02/0,05) | **0,3** (Test **0,3 / 0,4**) | N1–N3 |
| `remove_outside_spline_amount` | 50 | **0** (Test 0/50 erledigt) | F1 |
| Band (`RiverWidth` im Editor) | Plan-Bett (lokal teils + 2 m) | **Bett + 2 m** (`band_zugabe_m` 2) | F2 |
| `source_size_cm` | Breite an der Quelle | **max(300, Breite an der Quelle)** | Endstand 300 cm am 1,6–2,4-m-Bett |
| Regel Wasser-Info | Pixel ≤ Bett / 6 | **Pixel ≤ Band / 12** | F2, Ferats Vorschlag |
| Hindernisse | alle festen ≥ 0,4 m | **Filter N5** (Abschnitt 4) | N4/N5 |
| Messen | 120 s | **≥ 5 min bzw. ≥ 9 000 Bilder**, Bildrate notieren | Ferat |

**Nächste Läufe (C2, Zone 4096, 32 Bit, Hindernisse N5, Quelle 300, Entfernen 0, Band Bett + 2 m):**

| Lauf | Änderung | Erfolg, wenn |
|---|---|---|
| **F2-0,4** | Rate 0,4, **Spline ohne Offsets** (Plan) | Front bis 748 in allen Abschnitten. Dann entfallen die Offsets, und 0,4 wird Vorgabe |
| F2-0,4-K | wie oben, Kiesbett-Band = Bett | Überlauf im Kies wie Endstand (−35 %), Front unverändert |
| N3-W / N6-W / N6-M | Abschnitt 1.3 | klärt Kippe oder globale Wirkung |
| **F6** | **entfällt.** Mit der neuen Regel braucht C2 0,30 m je Pixel, 2048 hätte 0,59 m | nur, falls Speicher gespart werden soll |

Bleibt F2-0,4 an einer Stelle hängen, zuerst dort das Band lokal verbreitern (+1 m). Erst danach die Rate weiter erhöhen.
Eine höhere Rate füllt auch Mulden neben dem Bett.

---

## 3. Frage 2: Texturformat – kann C2 wieder auf 16 Bit?

### 3.1 Half-Float-Auflösung

Half Float hat 1 Vorzeichen-, 5 Exponenten- und 10 Mantissen-Bit. Im Bereich [2ᵉ; 2ᵉ⁺¹) beträgt die Stufe 2ᵉ⁻¹⁰.

| Höhe (absolut, cm) | Höhe (m) | Stufe |
|---|---|---|
| 2 048–4 096 | 20,5–41,0 | **2 cm** |
| 4 096–8 192 | 41,0–81,9 | **4 cm** |
| 8 192–16 384 | 81,9–163,8 | **8 cm** |
| 16 384–32 768 | 163,8–327,7 | **16 cm** (190 m = 19 000 cm) |
| bis 65 504 | 655 m | 32 cm; darüber Überlauf (16a T2-10) |

**C2 (Erlenbach p2, 35,8–190,1 m):**
- **Absolut in cm gespeichert:**
  - Rinne über 163,84 m in 16-cm-Stufen, Durchbruch und Talkaskade (82–164 m) in 8 cm, Kiesbett und Mündung (36–41 m) in 2 cm.
  - Bei 0,5 m Bachtiefe sind 16 cm ein Drittel der Tiefe. Der Spiegel springt alle ~0,3–0,4 m Lauflänge (39–64 % Gefälle) um
    eine Stufe.
  - **Für steile Bergbäche über 164 m reicht 16 Bit nicht** [Ableitung].
- **Relativ zur Spanne gespeichert** (normiert 0…1): Stufe = Spanne × 2⁻¹¹ im oberen Halbbereich. In C2 (154,3 m Spanne,
  mit Boden ~155 m) sind das **7,6 cm**.
- **Was speichert Epic?** Nicht belegt.
  - Belegt sind nur die Felder `WaterHeightExtents`, `GroundZMin`, `CaptureZ` (in `FWaterInfoTextureRenderingParams`) und
    `bHalfPrecisionTexture` („16 oder 32 Bit je Kanal“) [Doku].
  - Die Höhenfelder sprechen für eine relative Speicherung [Ableitung].
  - Die Bodenerfassung der SWR selbst ist laut Forum absolut in Half Float (Sättigung bei 65 504) [16a, Forum].
- **Messlatte:** N7 zeigt, dass 10 cm Höhenfehler an einer knappen Lippe den Lauf kippen. Auch die relative Lesart
  (7,6 cm) liegt zu nah daran.

**Antwort: C2 bleibt auf 32 Bit (Half Precision aus).** Das kostet bei 4096² **256 MB statt 128 MB** (+128 MB), ohne Slices.

### 3.2 Neue Regel `half_precision_ok` je Zone (Regeln v11, `swr.water_info.zonen.half_precision`)

- **Stufe** = größere von zwei Rechnungen:
  - absolut: 2^(⌊log₂ max |z|⌋ − 10), mit z = höchster Spiegel bzw. tiefster Boden in cm;
  - relativ: Spanne (höchster Spiegel − tiefster Boden) × 2⁻¹¹.
- **`half_precision_ok`, wenn die Stufe ≤ 4 cm ist.** Das gilt für Wasser unter 81,92 m **und** eine Spanne unter 81,92 m.
  - 4 cm ist eine Wahl mit Reserve gegen die 10 cm aus N7 [Ableitung].
  - Bei 8 cm (Wasser über 82 m) also 32 Bit.

**Ergebnis Weltvorschlag (2-m-Daten, neue Regel Band / 12):**

| | Zonen | Speicher, alle geladen |
|---|---|---|
| alles 16 Bit | 35 | 1 378,5 MB |
| alles 32 Bit | 35 | 2 757 MB |
| **nach `half_precision_ok`** | 23 × 16 Bit, **12 × 32 Bit** | **1 962,5 MB** (feine Zonen 1 706,5 MB) |

- Die 32-Bit-Zonen sind `WZ_WELT` (Wasser bis 207 m, Spanne 295 m) sowie `WZ_F01`, `F02`, `F04`, `F05`, `F06`, `F10`,
  `F12`, `F17`, `F19`, `F21`, `F22`: Bergbäche bis 307 m und Gletscher-, Klamm- und Karsee-Abflüsse.
- **Die Grundzone trägt auch Seen und Meer, die der Export nicht kennt.** Lokal mit allen Wasserflächen nachrechnen.
  - Bergseen über 82 m machen die Grundzone ohnehin 32-bittig.
  - Alternative: Bergseen in eigene feine Zonen legen, dann bleibt die Grundzone (Meer, tiefe Flüsse) bei 16 Bit
    (128 statt 256 MB).
- **Eure Zonen:**
  - C3 (Mündung, ~36–40 m): 16 Bit in Ordnung, wenn alles Wasser darin unter 81,9 m liegt.
  - Meer: 16 Bit in Ordnung.
  - **D2 (Felsrinne, Quelle 190 m): 32 Bit**, sobald dort ein Bach oder See über 82 m simuliert bzw. gezeichnet wird.
- Prüfer mit `--zonen`: Eine Zone mit `"half_precision": true` und Stufe über 4 cm ergibt eine **WARNUNG** (Beispiel C2:
  „Höhenstufe 16 cm, Half Precision aus“).

---

## 4. Hindernis-Filter (Regel v11, `swr.hindernis_filter`)

### 4.1 Regel

Gilt für alle Objekte mit Wasser-Kollision (`WH_`-Akteure und Akteure mit Tag), **nach** der bisherigen Auswahl (fest,
≥ 0,4 m, im Wasser oder ≤ 1 m daneben, nicht überspannend):

1. **Rolle:** Lippen-, Rand- und Bettfelsen bekommen keine Wasser-Kollision (`grund: filter_rolle`).
   - Stufe, Ufer und Bett formt das Gelände; diese Felsen sind Deko darauf.
   - Unsere Planer schreiben die Rolle je Netz-Datei (`dateien.<netz>.rolle`, mehrere mit „/“). Zugeordnet wird so:
     - Lippe: `riegel_*`, `lippe_*`;
     - Rand: `randbloecke`, `randecke`, `rahmenbloecke`, `bbf_ufer`;
     - Bett: `beckenbloecke`, `bbf_wasser`.
   - Eine Datei zählt nur, wenn **alle** ihre Rollen in diese Klassen fallen. Gemischte Dateien („unklar“, 1 430 Objekte) und
     Akteure (Held-Felsen, Fallwände, Sehens-Schwellen; 982) prüft nur die Größenregel.
   - Ferats Bachdekor-Werkzeug kennt die Rolle je Teil und braucht diese Zuordnung nicht.
2. **Teil ≤ 40 % der lokalen Bettbreite** (`filter_teil`).
   - Quer = Ausdehnung der 8 gedrehten Ecken (Netz-Bounds × Skala) quer zur Spline am nächsten Splinepunkt, **nur der Teil im
     Bett** (± halbe Breite).
   - Bettbreite = `RiverWidth` an dieser Stelle (Plan-Bett, ohne Band-Zugabe).
3. **Je Meter Lauflänge zusammen ≤ 50 % der Bettbreite** (`filter_meter`).
   - Raster s = 0, 1, 2 … m ab der Quelle; ein Teil zählt in jedem Meter, den sein s-Bereich (Länge entlang der Spline)
     berührt.
   - Die Teile werden gierig verteilt, die schmalsten zuerst (dann Verweis). So bleiben möglichst viele Teile, und große
     Teile fallen zuerst weg.
4. Teile **ganz neben dem Bett** (quer 0) bleiben.
5. Ein Teil, das in einem Gewässer ausgefiltert ist, ist es überall (`filter_anderes_gewaesser`, 25 Teile). Kollision gibt es
   je Objekt nur einmal.
6. **Ausgefilterte Teile bleiben als Deko.** Sie stehen in `ohne_wasser_kollision` mit `grund` und `filter` (`rolle`,
   `quer_im_bett_m`, `bett_breite_m`, `s_laengs_m`) und in keinem `WH_`-Akteur.

**Unsere Präzisierung:** Wir messen quer **im Bett**. Ein großer Uferblock, der 0,3 m ins Bett ragt, zählt also mit 0,3 m.
Misst Ferats Werkzeug die ganze Teilbreite, ist es strenger; beides hält das Bett offen (Rückfrage 2).

### 4.2 Zahlen (2-m-Lauf, alle 186 Gewässer)

| | vorher (v10) | nachher (v11) |
|---|---|---|
| eindeutige Objekte mit Wasser-Kollision | 40 221 | **20 225** |
| Einträge `wasser_kollision` (je Gewässer) | 40 476 | 20 371 |
| Instanzen in `WH_`-Akteuren | 39 239 | 19 864 |
| Akteure mit Tag | 982 | 361 |
| Objekte in den Fingerabdrücken (Summe über 197 SWR) | 52 691 | 26 712 |
| davon Fels / Holz / sonstiges | 22 703 / 17 383 / 135 | 7 324 / 12 821 / 80 |

- **Ausgefiltert (19 996):**
  - Rolle 12 923 (Bett + Rand 3 710, Bett + Lippe + Rand 3 872, Lippe + Rand 2 081, Rand 1 459, Lippe 1 197, Bett 428,
    Bett + Lippe 176);
  - zu breit 3 526, Meter-Budget 3 522, in einem anderen Gewässer ausgefiltert 25 (`zusammenfassung.json`; der Prüfer
    zählt je Teil den eigenen Grund: 3 537 / 3 536).
- Behaltene Teile belegen im Median **7,3 %** der Bettbreite, höchstens 40 %.
- Die meisten Teile verlieren `F_ELFENFLUSS` (2 905 → 2 067), `B_R_P4_M2_04` (1 442 → 712) und `B_R2_R_P4_M2_01`
  (1 147 → 505).
- **Gegenüber Ferats N5** (1 718 → 1 336, 78 % bleiben) bleiben bei uns nur 50 %.
  - Unsere Planer setzen viel mehr Riegel-, Rand- und Beckenblöcke als Ferats Bachdekor.
  - Die 2-m-Plan-Breiten sind oft breiter als das lokale Bett; lokal auf 1 m fallen deshalb eher **mehr** Teile weg.

### 4.3 `source_size` 300 cm als Bach-Standard

- Gemessen: Quelle 300 cm am 1,6–2,4-m-Bett → Front 783 von 788 m, Bett 99,8 % nass (Endstand).
- **v11:** `source_size_cm` = max(300, `RiverWidth` am ersten Punkt des SWR-Bereichs).
  - Breitere Quellen (Flüsse, Teilstücke) behalten ihre Breite: `F_ERLENBACH` ab C3 3 600 cm.
  - 55 von 197 SWR ändern sich, vorher ab 70 cm. Der Median ist jetzt 400 cm.
- Ob `source_size` Durchmesser oder Kantenlänge ist, ist nicht belegt [unsicher]; für das Ergebnis zählt der gemessene Wert.

### 4.4 Spline-Höhen-Offsets je Abschnitt: kein Feld

Kein Export-Feld, weil:
1. die Wirkung **global** und nicht verstanden ist (N6);
2. die Offsets nach 1.2 nur die Rate ersetzen (+10 cm ≈ +20 %), und 0,4 das ohne Eingriff in die Spline leisten sollte;
3. ein Offset den Splineteil des Fingerabdrucks ändern und alle Spline-Prüfungen (Lippe/Fuß ± 2 cm, Becken auf dem Spiegel)
   brechen würde.

Ferats Endstand (+10 cm oben, −12 cm im Kies) bleibt eine lokale Einstellung an p2, bis F2-0,4 zeigt, ob er nötig ist.

---

## 5. Frage 3: World Partition – alle 37 Zonen immer geladen

- **Speicher** [Ableitung]: Mit `is_spatially_loaded` = False belegt jede Zone ihre Wasser-Info dauernd, im Spiel und im
  Editor.
  - Beim Weltvorschlag (35 Zonen) sind das **1,38 GB (16 Bit) bis 2,76 GB (32 Bit)**, mit gemischtem Format 1,96 GB.
  - Eure 37 Zonen kennen wir nicht. Eine 4096²-Zone kostet 128/256 MB, eine 2048²-Zone 32/64 MB.
  - Bitte `stat RHI` bzw. `memreport -full` einmal mit allen Zonen messen.
- **Empfehlung:**
  - **Feine Zonen räumlich laden** (`is_spatially_loaded` = True).
  - **Grundzone, Meer und große Seezonen immer geladen** (False). Sie tragen das ferne Wasser.
  - Im Spiel liegen dann typisch die Grundzone und 2–4 feine Zonen im Ladebereich, also **~200–600 MB** [Ableitung].
- **Bedingungen und Risiken** [unsicher, im Test klären]:
  1. Ein Gewässer mit `WaterZoneOverride` darf nicht sichtbar sein, während seine Zone noch nicht geladen ist. Sonst fällt
     es auf die Grundzone zurück (grob) oder fehlt kurz.
     - Die Zone umfasst alle ihre Betten + 10 m und wird deshalb über ihre Bounds mindestens so früh geladen wie ihre Flüsse.
     - Testen: im PIE an eine Zonengrenze fahren und auf Flackern oder fehlendes Wasser achten (`r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames`
       erzwingt ein Neuzeichnen).
  2. **Backen nur mit geladener Zone.** Im Editor die Region laden (oder vorübergehend nicht räumlich laden).
  3. Forum: In 5.3/5.4 wurden nicht räumlich geladene Akteure im Standalone-Spiel trotzdem räumlich geladen (UE-219132)
     [Forum]. Das Gegenteil ist nicht gemeldet; trotzdem einmal im Standalone prüfen.
  4. Ein Forenfall zeigt eine zu früh erzeugte (zu grobe) Wasser-Info nach dem Nachladen eines Levels. Abhilfe war ein
     verzögertes `MarkForRebuild()` an der Zone [Forum]. Erscheint das Wasser nach dem Nachladen blockig, ist das der
     Kandidat.

---

## 6. Frage 5: Name der CVar für die Höchstauflösung

**Stand der Belege:**

| Name | Beleg | Status |
|---|---|---|
| `r.Water.WaterInfo.RenderTargetResolutionMax` | nur im Doku-Text zu `AWaterZone::RenderTargetResolution` („CVar … may clamp the resolution“) [Doku, 16g] | **nicht bestätigt**; Ferats Python-Abfrage liefert 0 |
| `r.Water.WaterInfo.RenderTargetResolution`, `r.Water.WaterInfo.MaxRenderTargetResolution` | kein Beleg | **nicht belegt** |
| `r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames` | Doku „Water Debugging and Scalability Options“ (5.2) [Doku] | belegt |
| `r.Water.WaterInfo.RenderMethod` | Forum (Movie Render Queue, 5.4) [Forum] | belegt |
| `r.Water.WaterMesh.ShowWireframe`, `…ShowWireframeAtBaseHeight`, `…ShowTileBounds` | Doku (5.2) [Doku] | belegt |
| `r.Water.MaxFlowVelocity` | Projekt A12 | belegt |

**Warum die Python-Abfrage 0 liefert:** `unreal.SystemLibrary.get_console_variable_int_value(name)` gibt für einen
**unbekannten Namen 0** zurück, nicht einen Fehler [Ableitung]. 0 heißt also nur: unter diesem Namen nicht gefunden (oder
Wert 0). Ob es eine solche Kappung in 5.8 überhaupt als CVar gibt, ist offen. Sie kann auch ein Editor-Setting sein (ältere
Doku: `UWaterEditorSettings` … `MaxWaterVelocityAndHeightTextureSize`) [Doku, Version unklar].

**So listet ihr alle Namen im Editor:**
1. **Konsole (sicher):** `r.Water.WaterInfo.` eintippen (mit Punkt). Die Autovervollständigung zeigt alle CVars mit diesem
   Präfix samt Hilfetext. Ebenso `r.Water.WaterMesh.` und `r.Water.`.
2. **Ausgabe ins Log:**
   - `DumpConsoleCommands r.Water` schreibt alle Befehle und Variablen mit diesem Präfix ins Output Log [unsicher: Präfixfilter].
   - `DumpCVars r.Water` gibt es nach eurem Vorschlag ebenfalls [unsicher, nicht belegt]. Eine Fehlermeldung „Command not
     recognized“ zeigt sofort, ob es ihn gibt.
   - `help` erzeugt die Hilfeseite aller Konsolenvariablen (HTML im `Saved`-Ordner) [unsicher].
3. **Python** (liest das Log nach dem Befehl, weil es keine Python-Liste der CVars gibt [unsicher]):

```python
import unreal, os, glob
unreal.SystemLibrary.execute_console_command(None, "DumpConsoleCommands r.Water")
for n in ("r.Water.WaterInfo.RenderTargetResolutionMax", "r.Water.WaterInfo.RenderTargetResolution",
          "r.Water.WaterInfo.MaxRenderTargetResolution"):
    unreal.SystemLibrary.execute_console_command(None, n)      # Name ohne Wert: druckt "n = ..." oder "not recognized"
log = sorted(glob.glob(os.path.join(unreal.Paths.project_log_dir(), "*.log")), key=os.path.getmtime)[-1]
zeilen = open(log, encoding="utf-8", errors="ignore").read().splitlines()
for z in zeilen[-400:]:
    if "r.Water" in z or "not recognized" in z:
        print(z)
```

4. **Ob gekappt wird, direkt prüfen:**
   - Größe der tatsächlich erzeugten Textur: `obj list class=TextureRenderTarget2DArray` bzw. `stat RHI` / `memreport -full`
     nach dem Umstellen der Zone.
   - Steht dort bei Einstellung 4096 auch 4096 × 4096, kappt nichts.
   - Für 8192 genauso testen. Wir schlagen 8192 weiter **nicht** vor; die Regel bleibt bei höchstens 4096 je Achse.

---

## 7. Export und Prüfer (Regeln v11)

**Geändert** (`skripte/fluss_sim/`, README „Ergänzungen 16g Nachtrag 2“):

| Teil | Änderung |
|---|---|
| `fluss_sim_regeln.json` | Version 11. `sim_vorgaben`: Rate 0,3 (Test 0,3/0,4), Entfernen 0 (Test 0/50), `band_zugabe_m` 2, `source_size` „breite_quelle_min“ mit 300 cm. `water_info`: Teiler 12 auf das Band. Neu: `hindernis_filter` (Rollen, 40 %, 50 %, 1 m) und `water_info.zonen.half_precision` (Stufe ≤ 4 cm) |
| Export | Filter je Gewässer und global, `filter`-Feld je Eintrag, `zusammenfassung.json` → `hindernis_filter`; `swr.band_zugabe_m` (auch in `back_liste.sim_vorgaben`); `water_info.band_min_m`; `wasserzonen.json` je Zone `hoehe_m`, `half_float_stufe_cm`, `half_precision_ok`, `format_empfohlen`, Summe mit Speicher bei empfohlenem Format |
| Prüfer | Filter unabhängig nachgerechnet (eigene Drehung der Bounds, eigene gierige Meter-Rechnung); SWR-Vorgaben v11 und `source_size_cm`; global: ausgefiltertes Teil nirgends mit Kollision; `--zonen` mit `half_precision` → WARNUNG über 4 cm |
| `zonen_beispiel_c2.json` | Ferats C2-Werte: Zentrum (−221 050; −254 850) cm, 1208 m, 4096, Half Precision aus |

**Lauf** (2-m-Daten, Scratchpad, Code-Stand dieses Commits):
- Vorlauf: Gefälle-Planer `--alle` (120 Läufe, 1 050 Stufen, 0 FEHLER), Roh-Ebene (95 Roh-Läufe, Prüfer 0 FEHLER),
  Sehens-Ausgaben unverändert.
- Export zweimal; zum Vergleich der v10-Code auf denselben Eingaben. Er reproduziert die bisherigen Beispiele byte-gleich.

| Prüfung | Ergebnis |
|---|---|
| Prüfer (mit Daten, `--vergleich`) | **0 FEHLER, 0 WARNUNG, 74 HINWEIS** (neu: Hindernis-Filter; Rest wie bisher) |
| Determinismus | **183 Dateien byte-gleich** |
| Gewässer, SWR, Fälle | 186 / 197 / 737 (166 Vorhang), unverändert |
| Fingerabdrücke gegen v10 | **194 von 197 geändert, nur Objektteil**; Gelände 0, Splines 0. Gleich bleiben `B_R_M2_M1_02`, `B_R_M2_M2_01` (keine Objekte) und `SW_lava_03_kraterkinder_rinnsal` (3 Objekte, alle behalten) |
| `sim_vorgaben` gegen v10 | alle 197 geändert (Rate, Entfernen, `band_zugabe_m`; 55 auch `source_size_cm`) |
| Beispiele | `F_ERLENBACH` 363 → 139 Objekte im Fingerabdruck (`d48d07dd22ff…`), Karsee-Abfluss 39 → 30, Elfentreppe 140 → 101, `B_R2_K10_TUNDRA_01` 94 → 53 |
| Water Zones | 35 Zonen (vorher 28), 1 378,5 / 2 757 MB; 12 Zonen 32 Bit; `F_ERLENBACH` → `WZ_F08` |
| `--zonen zonen_beispiel_c2.json` | 0 FEHLER (7 SWR-Bereiche geprüft), 2 WARNUNG (Betten der 2-m-Daten ragen aus C2), HINWEIS „Stufe 16 cm, Half Precision aus“ |
| dieselbe mit `half_precision: true` | + 1 WARNUNG (Stufe 16 cm > 4 cm) |

**Gegenproben** (alle mit Exit 1):

| Gegenprobe | Ergebnis |
|---|---|
| gefilterter Randfels zurück in `wasser_kollision` | 4 FEHLER |
| `quer_im_bett_m` auf 90 % der Breite | 5 FEHLER |
| `filter_teil` als `filter_meter` | 1 FEHLER |
| Rate 0,02 | 2 FEHLER |
| `source_size_cm` 200 statt 300 | 2 FEHLER |

**Beispiele neu** unter `antworten/fluss_sim/`:
- neu geschrieben: `F_ERLENBACH`, Karsee, Elfentreppe, `zusammenfassung.json`, `wasserzonen.json`,
  `back_liste_auszug.json`;
- gleich geblieben: `vorschlaege.json`.

---

## 8. Mündung (Abschnitt 4 Punkt 3)

- `F_ERLENBACH_2_C3` steht bei 37,78 m, p2 bei s 740 bei 36,86 m. **Der Bach endet 0,9 m unter dem Fluss** [Befund].
- Das Wasser des Flusses würde in den Bach zurückstehen, und die Flächen schneiden sich [Ableitung].
- **Vorschlag** [Ableitung]: Der Spiegel von p2 muss an der Flussgrenze (s ≈ 748) **auf dem Flussspiegel** enden.
  - Entweder p2 von s ≈ 700 bis 748 anheben (flacher Auslauf auf 37,8 m).
  - Oder den Flussspiegel dort aus dem lokalen 1-m-Gelände neu setzen; die 37,78 m stammen aus den 2-m-Weltdaten.
  - Unterhalb von s 748 gehört das Wasser dem Fluss. Die p2-Spline darf dort enden.
- Wir warten auf das Bild der Mündung.

> **Nachtrag (nach 16h Nachtrag 2):** Diese Empfehlung ist überholt, solange Ferats Prüfung aussteht.
> In [`16h-nachtrag2-tl-t0-kasten.md`](16h-nachtrag2-tl-t0-kasten.md) zeigt sich: Die 37,78 m am Kopf von `F_ERLENBACH_2_C3` sind eine Kopie des Endes des ersetzten `F_ERLENBACH_2_C2`. Sie sind also der Rest der alten Überlappung und kein Flussspiegel.
> Deshalb gilt dort der p2-Spiegel, ohne Anheben, und `F_ERLENBACH` wird am Kopf gekürzt.
> Nur wenn das C3-Wasser im Level tatsächlich bei ≈ 37,8 m steht (Rückfrage 3 in 16h Nachtrag 2), gilt der Vorschlag oben.
>
> **Stand 16h Nachtrag 3:** Ferats Mündungsbild zeigt C3 dort als Tümpel im Schotterbett, ohne Glaswand. Die Kürzung ist im Export
> umgesetzt (`ersetzt.json` → `muendung_anschluss`, `kopf_kuerzen`), siehe [`16h-nachtrag3-teile-a-c1-t3-schaum.md`](16h-nachtrag3-teile-a-c1-t3-schaum.md) §6.
> Der Vorschlag oben (p2 anheben) entfällt.

---

## Was lokal zu tun ist

Code- und Regelstand: Commit `c5d3cbb` (fluss_sim v11).

1. **F2-0,4** (Abschnitt 2): Rate 0,4, Spline ohne Offsets, Band = Bett + 2 m, Entfernen 0, Quelle 300, Hindernisse N5.
   - ≥ 9 000 Bilder bzw. 5 min, Bildrate notieren.
   - Messen wie F1: Bett nass, 1–8 m außerhalb, Tiefe Mitte, Front.
2. **Kippe oder global** (Abschnitt 1.3): N3 zweimal, N6 einmal, N6 mit 0,4, N6-M (nur Mündung −12 cm).
3. **C2 auf 32 Bit lassen.** Zonen mit Wasser über 82 m bzw. mehr als 82 m Spanne (z. B. D2) auf 32 Bit stellen.
4. **Speicher messen:** `stat RHI` / `memreport -full` mit allen 37 Zonen, danach feine Zonen räumlich laden und im PIE erneut
   messen; an einer Zonengrenze auf Flackern achten.
5. **CVar-Namen auslesen** (Abschnitt 6): Autovervollständigung `r.Water.WaterInfo.` bzw. `DumpConsoleCommands r.Water`;
   Ausgabe oder Bild schicken.
6. **Bau-Werkzeug auf v11:**
   - `RiverWidth` = `punkte[3]` + 100 × `band_zugabe_m`;
   - SWR-Werte aus `sim_vorgaben`;
   - `WH_`-Akteure nur mit `wasser_kollision`; die Teile aus `ohne_wasser_kollision` (Grund `filter_*`) bleiben als Deko
     ohne Tag stehen;
   - Zonen-Format aus `wasserzonen.json` (`format_empfohlen`).
7. **Lokaler Lauf auf 1 m:**
   - `fluss_sim_export.py` und `fluss_sim_pruefen.py` mit `--zonen` (eure 37 Zonen inkl. `half_precision`);
   - erst danach gelten Zonenliste und Filterzahlen für die Welt.
8. **Neu backen:** alle SWR (Objektteil und `sim_vorgaben` geändert).

## Quellen

Epic-Seiten waren aus der Cloud nicht lesbar (DNS-Fehler); Inhalte nur aus Suchmaschinen-Auszügen.

**Epic (Doku, API):**
- [AWaterZone (API)](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/AWaterZone): `RenderTargetResolution`
  (Hinweis auf eine kappende CVar), `GroundZMin`, `CaptureZOffset`, `bHalfPrecisionTexture` [Doku]
- [FWaterInfoTextureRenderingParams](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/FSceneView/FWaterInfoTextureRenderingParams):
  `WaterHeightExtents` (FVector2f), `GroundZMin`, `CaptureZ`, `WaterZoneExtents` [Doku]
- [Water Debugging and Scalability Options (5.2)](https://docs.unrealengine.com/5.2/en-US/water-debugging-and-scalability-options-in-unreal-engine/),
  [aktuelle Fassung](https://dev.epicgames.com/documentation/unreal-engine/water-debugging-and-scalability-options-in-unreal-engine):
  `r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames`, `r.Water.WaterMesh.ShowWireframe`, `…ShowWireframeAtBaseHeight`,
  `…ShowTileBounds` [Doku]
- [Water Meshing System and Surface Rendering](https://dev.epicgames.com/documentation/unreal-engine/water-meshing-system-and-surface-rendering-in-unreal-engine) [Doku]
- [UE Public Roadmap: Water Scalability](https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/1453-water-scalability):
  5.4 lokale Tessellation und lokale Verarbeitung der Water-Info

**Epic-Forum (Auszüge):**
- [Water not rendering in movie export](https://forums.unrealengine.com/t/water-not-rendering-in-movie-export/1826466):
  `r.Water.WaterInfo.RenderMethod`
- [Water Body Not Rendering Properly When Loading a Level Mid Session – delayed MarkForRebuild() on WaterZone](https://forums.unrealengine.com/t/water-body-not-rendering-properly-when-loading-a-level-mid-session-requires-delayed-markforrebuild-on-waterzone/2568982)
- [Non-spatially loaded World Partition actor becomes spatially loaded in Standalone](https://forums.unrealengine.com/t/1409411) (UE-219132)
- Niagara Scene Capture „saturated at 65504“ (Forum 5.8, zitiert in [16a](16a-swr-einrichtungstest-teil1.md))

**Projekt:**
- `auftraege/16g-nachtrag2-feinwerte-und-rueckfragen.md` (N1–N7, Endstand, F1/F2, Rückfragen)
- [`16g-nachtrag-ursache-gefunden.md`](16g-nachtrag-ursache-gefunden.md), [`16g-swr-steiler-bergbach.md`](16g-swr-steiler-bergbach.md)
  (16 Bit „harmlos“ – **hiermit korrigiert**: 8–16 cm sind nach N7 nicht harmlos),
  [`16f-rueckfrage-epic-parameter-lokal.md`](16f-rueckfrage-epic-parameter-lokal.md) (Rate, Startwerte),
  [`16a-swr-einrichtungstest-teil1.md`](16a-swr-einrichtungstest-teil1.md) (Bodenerfassung Half Float)
- `skripte/fluss_sim/` (Regeln v11, Export, Prüfer, README, `zonen_beispiel_c2.json`); Beispiele `fluss_sim/`

## Rückfragen

1. **F2-0,4 ohne Offsets:** Läuft p2 mit 0,4 und Plan-Spline durch? Dann wird 0,4 Vorgabe, und die Offsets entfallen.
2. **Filter-Maß:** Misst euer Bachdekor-Werkzeug „Teil ≤ 40 %“ über die ganze Teilbreite oder nur über den Teil im Bett?
   Wir rechnen im Bett. Soll der Export die ganze Breite nehmen (strenger)?
3. **Rollen:** Passt unsere Zuordnung (Lippe = `riegel`/`lippe`, Rand = `randbloecke`/`randecke`/`rahmenbloecke`/`bbf_ufer`,
   Bett = `beckenbloecke`/`bbf_wasser`) zu euren Lippen-, Rand- und Bettfelsen? Sollen Held-Akteure (Fallwände, Schwellen)
   wie Bachdekor gefiltert werden oder, wie jetzt, nur nach Größe?
4. **Zonenliste:** Bitte die 37 Zonen mit Lage, Ausdehnung, Auflösung, Half Precision und Override-Gewässern schicken (Format
   `zonen_beispiel_c2.json`). Dann prüft `--zonen` auch Format und Speicher.
5. **CVar:** Was zeigt die Autovervollständigung für `r.Water.WaterInfo.`?
