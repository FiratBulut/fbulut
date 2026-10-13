# Antwort zu 16h Nachtrag – Materialtest: das Landschaftsmaterial legt hellen Kies unters Wasser

Stand 13.10.2026. Grundlage: `auftraege/16h-nachtrag-materialtest.md` (11:15), Bilder `bilder/swr_p2/wv_varianten.jpg` und
`altwasser_t500_vorher_nachher.jpg`, unsere Hauptantwort [`16h-erlenbach-p2-talkaskade-ufer-wasser.md`](16h-erlenbach-p2-talkaskade-ufer-wasser.md)
(B.1–B.4, A, C) und `skripte/sehens_lib/bachbett_regeln.json`.

**Kennzeichnung:** [Befund] Ferats Test, [Projekt] eigene Regeln/Daten, [Fach] Literatur, [Ableitung] geschlossen und
gerechnet, [Gestaltung] Gestaltungsentscheidung, [unsicher] im Test klären.

---

## Kurzfazit

1. **Befund bestätigt.** Unsere Rechnung zeigt dasselbe wie Ferats Test A–E: Bei 0,4–0,6 m lässt jede der getesteten
   Absorptionen 80–98 % durch (Hauptantwort B.2).
   - Die Wasserwerte sind dort nicht der Hebel; auch die Streustärke 0,1 → 0,02 (C) ändert kaum etwas.
   - **Variante F ist als Zwischenstand richtig.**
   - Den ELD-Schaum noch einmal einzeln prüfen: Test D hat nur `Foam Opacity` abgeschaltet, `ELD_Schaum_Deckkraft` 1 war
     noch an.
2. **B2.3 – Lagen im Bach nicht übermalen** (Tendenz des Koordinators, geprüft und bestätigt).
   - Unter Bächen zeigt das Material die Bachdekor-Lagen und dunkelt sie nur nass ab: `Ufer_Staerke` Bach **0**,
     `Nass_Abdunkeln` **0,40**, Nässe-Rand 50 cm, Tiefenabdunkelung bis × 0,7 mit leichtem Grünstich.
   - Die Kies-Ersetzung (Zielbild K2) bleibt für Seen und Flüsse, die keine eigenen Bettlagen haben.
3. **B2.2 – eigene Steuerung für Bäche:** ein Kanal **Bachgewicht** = 1 − SmoothStep(6 m; 12 m; Gewässerbreite) in der
   Spiegel-Textur (oder eine eigene R8-Textur); im Material je Parameter `Lerp(Welt, Bach, Bachgewicht)`.
4. **B2.1 – Witcher-Bachbett:** Die Bachdekor-Mischung selbst ist mit Kies 41 % zu hell. Unter dem Spiegel neu:
   - Geroell 40, Kies 25, Fels 10, Felsplatte 5, Schlamm 10, Algen 10;
   - Kies nur vorn an Schnellen, Schlamm und Algen in ruhigen Becken.
5. **Alte Flussfelsen:**
   - `C2_Flussfels_006` und `_002` (im p2-Bett) entfernen.
   - Von den übrigen 14 nur Blöcke ≤ 1,5 m im Band 0–12 m behalten, halb eingegraben; größere nur als Uferfels am Prallhang.
     Der Rest wird entfernt, die Bachsteine kommen aus dem Bachdekor.
6. **Klänge:** die drei Fluss-Klänge durch Bachklänge an den Stufen ersetzen.
   - je Stufe ≥ 0,5 m eine Quelle, sonst alle 25–40 m;
   - Reichweite 15–25 m, an Fällen ≥ 1 m 30–40 m;
   - etwa 10–12 dB leiser als der Fluss.
7. Maschinenlesbar: [`bachbett_ufer_regeln.json`](bachbett_ufer_regeln.json) → `B2_landschaft_bach`; Referenz
   `skripte/ufer_regeln/ufer_regeln.py` (`bachgewicht`, `landschaft_wert`), Selbsttest 0 FEHLER.

---

## 1. Einordnung des Tests

| Variante | Ergebnis [Befund] | Deutung [Ableitung] |
|---|---|---|
| A, B, C (Absorption 400–2000 cm, Streuung × 0,02–0,12) | fast gleich | Bei 0,5 m Tiefe ist T = exp(−50/L) für alle L ≥ 220 cm zwischen 0,80 und 0,98. Der Unterschied liegt unter dem, was Licht und Grund ausmachen |
| D (`Foam Opacity` 0) | Flecken bleiben | Es sind helle Steine der Kies-Textur, durch Normalen 40 und Refraction 1,15 zu Fladen verzerrt. Offen bleibt der ELD-Schaum (`ELD_Schaum_Deckkraft` 1 war an) |
| E (Roughness 0,04, Normalen 15) | etwas ruhiger | Die Verzerrung ist ein Nebenhebel |
| **Landschaftsmaterial** | Kies × (0,95; 0,93; 0,88) × 0,85 unter jedem Spiegel, Uferband −30…+60 cm | **Hauptursache:** heller, warmer, einheitlicher Grund. Im Abendlicht wird er goldbraun, aus 5 m Höhe wirkt er wie ein sandiger Graben |

**Schnelltest ELD-Schaum** (2 min): in Variante F zusätzlich `ELD_Schaum_Deckkraft` 0. Verschwinden helle Kappen über den
Steinen, dann `ELD_DF_Schaum` 0,25 und `ELD_Kontakt_Radius` 30 setzen (Hauptantwort B.3). Bleibt alles gleich, liegt es nur
an Grund und Verzerrung.

## 2. Frage B2.3 – Sollen die Bachdekor-Lagen unter Wasser übermalt werden?

**Nein, nicht unter Bächen.** Die Tendenz des Koordinators ist richtig; Prüfung [Ableitung, Projekt]:
- Die Lagen sind die geplante Bettstruktur: Schlamm in ruhigen Becken, Kies an Schnellen, Fels an Lippen, Uferstreifen
  (16c Nachtrag 2). Die Ersetzung löscht genau diese Lesbarkeit und macht jedes Bachbett gleich.
- Unter 0,5 m klarem Wasser sieht man den Grund fast unverändert (T ≥ 0,8). Was dort liegt, prägt das Bild. Deshalb muss es
  die richtige Lage sein, nicht eine weltweite Textur.
- Die Ersetzung ist für **Seen und Flüsse ohne eigene Bettlagen** gedacht (Zielbild K2). Dort bleibt sie unverändert.
- Was bleibt im Bach: nur die **Nässe** (Abdunkeln, Rauheit) und die **Tiefenabdunkelung**.

**Sonderfall:** Ein Bach ohne Bachdekor- bzw. Planer-Lagen hätte dann rohes Gelände unter Wasser.
- Unsere Roh-Ebene (`bachbett_roh.py`) gibt allen Welt-Bächen Kies, Schlamm und Uferstreifen. Lokal sollte also jeder Bach
  Lagen haben.
- Wenn nicht: Dort `Ufer_Staerke` 0,4 mit der grauen Bach-Farbe als Rückfall, geschaltet über einen zweiten Wert im Kanal
  (z. B. Bachgewicht 0,5 = „Bach ohne Lagen“) [Ableitung].

## 3. Frage B2.1 – Werte für Witcher-Bachbetten

**Material** (Bach = Bachgewicht 1; Welt-Werte bleiben für Seen und Flüsse):

| Parameter | heute (weltweit) | **Bach** | Begründung |
|---|---|---|---|
| `Ufer_Staerke` (Kies-Ersetzung unter Wasser) | 0,85 | **0** | Lagen zeigen (Abschnitt 2) |
| `Ufer_Farbe` | 0,95; 0,93; 0,88 | (0,60; 0,62; 0,60), nur für den Rückfall ohne Lagen | neutral-grau statt beige |
| `Nass_Abdunkeln` | 0,55 | **0,40** | nasser Stein ist 2- bis 2,5-mal dunkler und satter als trockener [Fach, Jensen et al. 1999] |
| `Nass_Breite_cm` | 150 | **50** | dunkler Nassrand nur 0,2–0,5 m über dem Spiegel (16b); 1,5 m nasser Hang ist für einen 2-m-Bach zu viel |
| `Nass_Staerke` / `Nass_Spiegel` | 2,5 / 1 | 2,5 / 1 | bleibt |
| Rauheit unter Wasser | 0,35 | 0,35 | bleibt; unter Wasser bestimmt die Wasserfläche den Glanz |
| Uferband (−30…+60 cm, Normal-Z > 0,86) | Stärke 0,85 | **0** | dort liegt der Uferstreifen Moos/Erde/Schlamm aus dem Bachdekor; das Kiesband machte die hellen Stufenflächen |
| **Tiefenabdunkelung** (neu, 3 Knoten) | – | Grund × Lerp(1; 0,7; SmoothStep(0,2; 1,0 m; Tiefe)) × Lerp(1; (0,92; 1,0; 0,95); SmoothStep(0,6; 1,5 m; Tiefe)) | Tiefe ablesbar und leicht grün, wo die Absorption bei 0,5 m noch nichts zeigt |

**Lagen unter dem Spiegel** (Bachdekor, Prozent):

| Lage | heute | **Vorschlag** | Bedingung |
|---|---|---|---|
| Geroell | 33 | **40** | überall; trägt die gemischte Körnung |
| Kies | 41 | **25** | vorn an Schnellen und Rinnen (Ruhe < 0,6) |
| Fels / Felsplatte | 7 / – | **10 / 5** | an Lippen und Stufen |
| Schlamm | 8 | **10** | ruhige, tiefe Becken (Ruhe ≥ 0,6, Tiefe ≥ 0,25 m) |
| Algen | – | **10** | ruhige Becken ≥ 0,4 m, nicht an Schnellen |
| übrige | 11 | 0 | – |

- Wenn die Kies-Textur selbst beige ist, im Bach eine **graue, gemischte Bachkiesel-Textur** für die Lage Kies verwenden
  (oder `Kies` dort × (0,8; 0,82; 0,8)) [Gestaltung].
- Nach diesem Schritt erst die Wasserwerte fein abstimmen (Hauptantwort B.3, V1 für Becken ≥ 1 m).

## 4. Frage B2.2 – weltweit oder eigene Bach-Steuerung?

**Eigene Steuerung** [Ableitung]:
- **Kanal Bachgewicht** = 1 − SmoothStep(6 m; 12 m; Gewässerbreite), um eine 2-m-Zelle weichgezeichnet.
  - Als zweiter Kanal von `T_Eldarien_Wasserspiegel_2m`, wenn das Format es erlaubt; sonst eine eigene R8-Textur
    `T_Eldarien_Bachgewicht_2m` mit gleicher Lage und Größe.
  - Die Breite kommt aus eurer Wasserkarte bzw. der Spline (p2: 1,6–2,4 m → 1; C3-Fluss → 0).
- **Material:** je Parameter aus Abschnitt 3 `Lerp(Welt, Bach, Bachgewicht)`, dazu die Tiefenabdunkelung × Bachgewicht.
  - Das sind 6–8 Lerp-Knoten und ein Textur-Abruf mehr (oder keiner, wenn es ein Kanal der vorhandenen Textur ist).
- **Warum nicht weltweit:**
  - Seen und Flüsse ohne Bettlagen brauchen die Kies-Ersetzung (K2, helle Kiesufer).
  - Bäche brauchen das Gegenteil.
  - Mit einem Satz Werte für beide verliert immer eine Seite.
- **Testreihenfolge:**
  1. Die Bach-Werte vorübergehend global setzen (Test TL der Hauptantwort), Bilder wie `wv_varianten.jpg`, zurückstellen.
  2. Trägt das Bild, den Kanal bauen.

## 5. Nebenbefund: alte Flussfelsen `C2_Flussfels_*`

| Fall | Regel | Begründung |
|---|---|---|
| `_006` (1,9 m von der Mitte), `_002` (2,4 m) im p2-Bett | **entfernen** | Ein Block des 30-m-Flusses dämmt den 2-m-Bach. Ohne Wasser-Kollision läuft das Wasser durch ihn hindurch, mit Kollision staut er (16g N4: zwei 1-m-Lippenfelsen dämmten das Bett) |
| übrige im Band 0–12 m vom p2-Bett, ≤ 1,5 m | **behalten**, 40–60 % eingraben (Hauptantwort C.4), Moos oben ab 0,3 m über dem Spiegel; ≤ 1 m neben dem Wasser als SWR-Hindernis (Reset + Bake) | passt als alte Ufersteine ins Hochwasserbett (A.2) |
| größer als 1,5 m | nur als **Uferfels an einem Prallhang** (Außenkurve), ≥ 50 % eingegraben; sonst entfernen | Ein Blockfeld ohne den Fluss, der es abgelegt hat, liest sich wie der alte Schotterstreifen |
| außerhalb 12 m | **entfernen** oder als einzelner Findling mit Moos und Gras am Fuß (höchstens 1 je 50 m) | gleiche Logik wie Teil A |

**Versetzen** lohnt nur für die großen Blöcke, die an einen Prallhang der Talkaskade passen (Hauptantwort C.4: Prallhang-Fuß
0,6–1,4 m, größere als Uferfels). Die Bachsteine selbst liefert das Bachdekor.

## 6. Nebenbefund: Klänge `C2_Ton_Fluss_01/02/05`

[Gestaltung, unsicher: Werte sind Erfahrungswerte, keine Messung; im Spiel abhören]

| Quelle | Ort | Reichweite (Abklingen bis 0) | Lautstärke gegen den Flussklang | Klang |
|---|---|---|---|---|
| Stufe 0,5–1 m | an der Lippe, 0,5 m über dem Spiegel | 15–20 m | −12 dB | Plätschern, kurze Loops |
| Fall ≥ 1 m | am Fuß | 30–40 m (innerer Radius 3–5 m) | −6 bis −8 dB | Rauschen mit Aufprall |
| ruhige Strecke | alle 25–40 m, nur wo 20 m keine Stufe ist | 10–15 m | −16 bis −18 dB | leises Gluckern |
| Mündung in den C3-Fluss | – | – | – | der Flussklang des C3-Laufs bleibt |

- Die drei alten Flussklänge entfernen oder auf die Fall-Werte oben umstellen. Ein 30-m-Flussklang auf einem 2-m-Bach ist
  rund doppelt so laut empfunden wie passend (10 dB ≈ doppelte Lautheit).
- Höchstens 3–4 Bachquellen gleichzeitig hörbar, sonst entsteht ein Rauschteppich.
- Die Stufen der Talkaskade (s 390–579) zuerst setzen; dort hört der Spieler den Bach.

## 7. Was lokal zu tun ist

Regeln und Referenz: Commit **`97a8e12`** holen (enthält auch den Code der Hauptantwort).

1. Variante F lassen. Schnelltest `ELD_Schaum_Deckkraft` 0 (Abschnitt 1).
2. Test TL: Bach-Werte aus Abschnitt 3 global; Bilder an `C2_t430_auge`, `C2_t500_auge`, `C2_t500_schraeg`, `C2_t550_auge`.
3. Bachdekor unter dem Spiegel auf die neue Mischung; Kies-Textur prüfen.
4. Kanal Bachgewicht und Lerp im Landschaftsmaterial; Seen und Flüsse gegen ein Vorher-Bild prüfen (müssen gleich bleiben).
5. `C2_Flussfels_006` und `_002` entfernen, die übrigen nach Abschnitt 5; SWR Reset + Bake.
6. Klänge nach Abschnitt 6.

## Quellen

- Ferats Nachtrag `auftraege/16h-nachtrag-materialtest.md`, Bilder `wv_varianten.jpg`, `altwasser_t500_vorher_nachher.jpg`.
- Hauptantwort [`16h-erlenbach-p2-talkaskade-ufer-wasser.md`](16h-erlenbach-p2-talkaskade-ufer-wasser.md): Absorptionstabelle
  (B.2), Wasserwerte (B.3), FoamAtten (B.4), Bänder A.2, Steine C.4.
- [Jensen, Legakis, Dorsey 1999: Rendering of Wet Materials](http://graphics.ucsd.edu/~henrik/papers/rendering_wet_materials/rendering_wet_materials_egwr99.pdf)
  – nasse Oberflächen dunkler und satter (Wasserfilm und Poren).
- `skripte/sehens_lib/bachbett_regeln.json` (Uferstreifen, Schlamm, Ruhe), 16b (Nassrand 0,2–0,5 m, Grund × 0,6), 16g
  Nachtrag 2 (N4: Lippenfelsen dämmen das Bett).

## Rückfragen

1. Erlaubt `T_Eldarien_Wasserspiegel_2m` einen zweiten Kanal, oder lieber eine eigene R8-Textur?
2. Haben alle lokalen Bäche Bettlagen (Bachdekor oder unsere Roh-Ebene)? Sonst brauchen wir den Rückfall
   „Bach ohne Lagen“ (Abschnitt 2).
3. Ist die Kies-Textur der Lage `Kies` dieselbe wie die der Ersetzung? Dann im Bach eine graue Bachkiesel-Variante.
