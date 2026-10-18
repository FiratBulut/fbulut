# Antwort 16h Nachtrag 6k – Simulationsboden im Band: Deckel statt Glättung, „sichtbar“ als Messgröße, Nachfüllen 0,3, Kolke, B5-Halde

Gelesen: recherche/auftraege/16h-nachtrag6k-t6j-ergebnisse.md @ 1c29f5b8d00bf866f0dd923c37c55bf5fbf11993 (Commit 9d11d5a)

Stand 18.10.2026. Gesamtauftrag 16h (Erlenbach p2, Talkaskade s 389–580). Bearbeiter: Cloud-Recherche. Bereich: Messgrößen und
Bodenbefund der SWR p2, Kolke, B5-Ost Halde. Wasser bleibt lokal unverändert, bis Schritt 1 (§2.6) ausgewertet ist.

**Bezug, ebenfalls gelesen (alle Commit 9d11d5a):**
- `recherche/antworten/16h-nachtrag6i-baked-sim-tests-stand.md` @ b3582ca1c2e105c43cbb346c06418a212d133e4b (ganz)
- `recherche/antworten/16h-nachtrag6j-teilung-ergebnis.md` @ 322982b7a365180b078aac3f5c6bdd66eb92365a (ganz)
- `recherche/antworten/21-detailgrad-landschaft-felsdeckung.md` @ 32f301737f1b63bf4931dc22b4c85c80c25169df (§(a), Prüfziele)
- `recherche/README.md` @ 778d8a7b8ac17fcaceb262ee8b63e46898ff7051 (Abschnitte „Start und nächstes Ergebnis“, „Übergabe nach Version“,
  „Tests und sichtbare Abnahme“, „Quellenzugriff und Aufwand“)
- `recherche/vorlagen/pruefung.md` @ 5daf4a9187ba35288dc4838f9461118e0960d068 („Messwerkzeuge“)
- `recherche/auftraege/16f-rueckfrage-epic-parameter-lokal.md` @ 06dbb319226188babbb55902043be858362d111b und
  `recherche/antworten/16f-rueckfrage-epic-parameter-lokal.md` @ 2df21f03041f4840d29cb206a62cf9a709ea33da (Smoothing laut Epic-Leitfaden)
- `recherche/antworten/16a-swr-einrichtungstest-teil1.md` @ aa728f71135565e070421f96982fc2dd6397661e (Bodenerfassung, §d)
- `recherche/antworten/16g-nachtrag2-feinwerte-und-rueckfragen.md` @ 9ca6b951895690bce4f6140dd77aba2b0b843d1b (Half Float, Band + 2 m)
- `recherche/auftraege/16h-nachtrag6f-bettplan-eingebaut.md` @ 6c745a203000e479f4c0d0e610ce05967b4729b6 („Hindernisse 906 + 5 Beckenblöcke“)
- `recherche/antworten/16h-nachtrag6c-becken-kuenstlich.md` @ 75c44f6cc6b74df6551ae9e4a7c3b8b273fadcc3 (SWR-Hindernisse = 5 Beckenblöcke)
- Rechengrundlage: `recherche/antworten/p2_bett/bettplan_p2.json` @ 0013ef4a1922330462308bc7dbad8729ae6a1ef3,
  `recherche/antworten/skripte/p2_bett/p2_bettplan.py` @ c65918691ffef1214808d17f86ef1bc21cf2a5c2,
  `recherche/antworten/fluss_sim/p2_lokal/querschnitte_p2.json` @ f7d2e2805f9d39c4f99d63f85f6b0b35a3a1b54f
- B5: `recherche/antworten/skripte/felsdeckung/felsdeckung_pruefen.py` @ 9311f990688074bfc94595557fbee789d155c4f9,
  `recherche/antworten/felsdeckung/pruefbericht_B5.txt` @ 02b32c5af6d8197c42e4f48df887d5bcf9e898c2

**Kennzeichnung:** [Ferat] eure Messung · [Rechnung] von mir mit Repo-Daten gerechnet, Skript in „Code“ · [Projekt] Regel oder Befund im
Repo · [Epic lokal] Ferats Zusammenfassung des Epic-Leitfadens (16f) · [Suchauszug] nur Suchauszug, Epic-Seiten und Forum aus der Cloud
nicht abrufbar (DNS-Fehler, 18.10.) · [Ableitung] geschlossen, nicht belegt · [zu prüfen] Name/Wert nicht belegt · **anzulegen** = Asset
gibt es noch nicht.

## Kurzfazit

0. **Gemeldete Ergebnisse – geschlossen, je eine Zeile:**
   - **T-b1:** H1 bestätigt (WCBS zeichnet auf Spline-Höhe, Material-Hebel H2/H3 widerlegt) → Erlenbach p2 bleibt BAKED_SIM, keine Spline-Anhebung ohne eigenen Testgrund (6i §1.2 „Nur H1“).
   - **T-c1:** `RenderState` ist im Spiel ohne eigenes C++ nicht umschaltbar → BAKED_SIM bleibt fest gespeichert, kein Entfernungswechsel, T-c2 entfällt.
   - **T6j-C:** nicht übernommen (sichtbar nur −2 bis −3 pp, Front 788 hielt) → Spline-Breite bleibt Bett + 2 m (`band_zugabe_m` 2).
   - **B0:** Ändern von `match_spline_height_amount` setzt die Simulation zurück → jede SWR-Eigenschaftsänderung wird als neuer Lauf ab Reset geplant (Schema B2), nie als Umschalten im laufenden Zustand.
1. **§6.1 Ursache des tiefen Bodens – wartet auf Beleg Schritt 1** (Auswertung vorhandener Dumps, ohne Editor, §2.6).
   - **Glättung des Bodens: als Hauptursache verworfen** [Rechnung]. Jede geprüfte Glättung (Kasten/Gauß 1,1–4 m, auch mehrfach) lässt den
     Band-Median am Plan-Gelände bei −1 bis +3 cm statt −64,7 cm. Sie hebt aber **alle** 24 Hauptkolke um 63–144 cm (Median je Variante), gemessen sind 15/24.
   - **Bestes Modell: „Deckel“** – Simulationsboden ≈ min(Gelände; Editor-Spline + c). Mit c = 3 cm sagt es den Band-Median **−64,6 cm**
     voraus (gemessen −64,7 cm) und lässt das Bett unverändert („passt“) [Rechnung]. Der Mechanismus ist offen.
   - **Ersatzwert hinter der Spline-Breite: verworfen.** T6j-C (Spline Bett + 0,5 m) brachte denselben Versatz (64,7 gegen 63–65 cm) [Ferat].
   - **Andere Bezugshöhe im Dump: verworfen.** Ein globaler Versatz müsste auch im Bett stehen, dort passt der Boden aber [Ferat].
2. **§6.2 Messgröße – beantwortet.** „Sichtbar“ ist richtig für alle Band- und Kolkziele, G nur noch als Nässe-Kennzeichen (Definition §3.1).
   - Das Ziel aus 6g §3 ist sichtbar gemessen **formal erreicht, ohne Reserve** (30,0 ≤ 30 %, 4,7 ≤ 5 %). Es wird durch das Prüfbandziel (3.) ersetzt.
   - Kantenbewuchs ist der nächste Hebel, gesetzt aber erst nach Schritt 2 (§2.6). Sitzt der Deckel in der Simulation, verschiebt seine
     Behebung die Wasserlinie.
3. **§6.3 Prüfband-Ziel – beantwortet:** **sichtbar > 5 cm ≤ 15 % des Bands 0,25–2 m**, Toleranz ±1 pp.
   - Basis 0,3: **14,0 %** → erreicht, mit 1 pp Reserve.
   - Begründung in §3.3: 5 cm liegen sicher über der 16-Bit-Stufe, und 15 % sind die 6g-§3-Ziele flächengewichtet. Der Wert liegt
     zwischen der Geometrie-Untergrenze und Füllen bis Spline + Überfall.
   - Vorbehalt: Bestätigt Schritt 2 den Deckel als Eingang der Simulation, nach der Behebung neu messen.
4. **§6.4 Nachfüllen – beantwortet: bei 0,3 bleiben.** 0,4 macht sichtbar gemessen den Lippenschatten um 7,2 pp und das übrige Band um
   2,0 pp nasser [Ferat B2]. 0,3 hält Bett 100 % und Front 788 m. Tiefer als 0,3 nicht testen (Front-Schwelle ≈ 0,3, 16g-N2 [Ableitung]).
5. **§6.5 Kolke – wartet auf Beleg (Kreuztabelle in Schritt 1).**
   - **Die 5 Beckenblöcke nicht herausnehmen und nicht verkleinern.** Alle 5 liegen laut Plan außerhalb jeder Kolk-Ellipse (normierter Abstand
     ≥ 4,07) und sind 0,41–0,77 m groß. 15 angehobene Kolke erklären sie nicht [Rechnung].
   - Verdacht sind die **906 übrigen Hindernisse** aus dem Altbestand, gesetzt auf das Gelände vor dem Aushub (−2,90 m) [Ableitung].
   - Prüfung ohne Bild: Fußabdrücke gegen Kolkflächen schneiden, dann ein Speicherlauf ohne diese Hindernisse (§5).
6. **§7 B5 Halde – beantwortet: reicht, keine Nachverdichtung jetzt.**
   - Das Ziel aus 21 §(a) ist ≥ 50 % (oberes Drittel ≥ 60 %). 69,5 % liegen 19,5 pp darüber.
   - Die 79 % des Prüfers sind ein **Planwert**, kein Ziel.
   - Nachverdichten nur, wenn das obere Drittel unter 60 % liegt oder eine 48-m-Zelle unter 50 %. Regel und Stückzahl (≈ 150 Teppichstücke)
     stehen in §6.
7. **Eigene frühere Antworten – korrigiert (§7):** Die 78,8-%-Bandzahl, das 5-%-Ziel in der Tiefe-Lesart, die T01-Bestätigung von H1 und die
   formalen Testurteile aus 6j beruhten auf dem zu tiefen Boden. Der Lippenschatten ist als Zone echt. Ein Teil seines Wassers kann aber ein
   Deckel-Artefakt sein. Der Boden-Trick ist zurückgestellt.

**Nächste Handlung (genau eine, lokal, ohne Editor, ≈ 30–45 min):** Schritt 1 aus §2.6, also `boden_befund.py` auf die vorhandenen Dumps
„Basis 0,3 frisch“ und „T6j-C“ anwenden, mit Kolk- und Hindernismaske.
- **Erfolgskriterium:**
  - `--selbsttest` gibt „bestanden“.
  - Beide Dumps liefern dasselbe Urteil, und es ist nicht „uneindeutig“.
  - Die Kolk-Kreuztabelle ist ausgegeben.
- **Für „DECKEL“ zusätzlich die Vorhersage** (Plan-Gelände, c = 3 cm):
  - Band 0,25–1 m: Median −30 ± 10 cm
  - Band 1–2 m: Median −94 ± 15 cm
  - p10: −149 ± 20 cm, p90: ≈ 0 cm

---

## 1. Abschluss der gemeldeten Ergebnisse

| Test | Befund [Ferat] | Entscheidung | Status |
|---|---|---|---|
| T-b1 | BAKED_SIM ≈ 45,16 m, WCBS ≈ 45,03 m = Spline, Multiplier 2/0 ohne Wirkung, `UseBakedSim` True → Wasser weg | Fall „Nur H1“ aus 6i §1.2: BAKED_SIM bleibt an der Talkaskade. Nebenbefund: Der gebackene Spiegel liegt 13–16 cm über der Spline, also bleibt `Nass_Spiegel_Versatz_cm` +20 (6i §3.2) gegen die Spiegeltextur plausibel | geschlossen |
| T-c1 | `RenderState` EditAnywhere ohne Blueprint, nur `SetPaused` BlueprintCallable | Render-State je Akteur fest; Regel 6i §1.2 ohne Entfernungswechsel | geschlossen |
| T6j-C | Front 788, Bett 100 %; sichtbar > 2 cm: 0,25–1 m 27,9 statt 30,0 %, 1–2 m 4,4 statt 4,7 % | nicht übernehmen; Ausnahme zu `band_zugabe_m` entfällt | verworfen |
| B0 | 30 s nach 0,3 → 0: Bett 0 % nass, Front 72 m | Eigenschaftsänderung = Reset. Gilt als Planungsregel für alle Tests unten | geschlossen |

---

## 2. §6.1 Woher kommt der tiefe Boden im Band?

### 2.1 Was die Messung festlegt [Ferat]

- **Band:** Boden aus dem Dump (R + Akteurhöhe − G) im Median 64,7 cm unter `hoehe.f32`. In anderen Läufen 63–65 cm, also auch bei
  schmaler Spline (T6j-C).
- **Bett:** Der Boden passt.
- **Kolke:** An 15 von 24 Hauptkolken liegt der Boden über +10 cm, bis +84 cm.
- **Band, Tiefe G:** > 1 / 10 cm in 83,2 / 45,7 % der Zellen. Sichtbar ist dort aber nur 15,9 / 11,0 %.
- **Folgerung:** G ist im Band großteils Wasser **unter** dem echten Gelände.

### 2.2 Was Epic zu den Feldern sagt

| Feld | Beleg | Bedeutung für §6.1 |
|---|---|---|
| `SmoothingWidth` (int), `SmoothingCutoff` (float) in `ShallowWaterRiverActor.h` | [Suchauszug] API-Tabelle `UShallowWaterRiverComponent`, ohne Beschreibung | Breite in ganzen Zellen ist damit wahrscheinlich, Einheit des Cutoff unbekannt [zu prüfen] |
| „Smoothing Width / Cutoff: Glättung der Oberflächen-Verschiebung bei harten Kanten“ | [Epic lokal] Leitfaden „Baked River Simulations – Parameter Reference“, 16f | Laut Epic wirkt die Glättung auf die **Oberflächen-Verschiebung** (Darstellung bzw. gebackene Fläche), nicht auf den Boden. „Cutoff 500 als Höhengrenze in cm“ ist nirgends belegt |
| `use_capture`, `bottom_contour_actors`, `bottom_contour_capture_offset` | [Suchauszug] Python-API 5.5; Tiefenaufnahme von oben, ganze Akteure (16a §d) | Hindernisse kommen über die Aufnahme dazu; Bedeutung und Einheit von `bottom_contour_capture_offset` [zu prüfen] |
| Niagara `Grid2D_SW_River` hat eine eigene „Smoothing Width“ | [Epic lokal] 16f | zweite Stelle, nur in einer Kopie ändern |

Einen Quelltext-Spiegel der Engine habe ich nicht benutzt. Wie die SWR den Boden aus Landschaft, Hindernissen und Spline zusammensetzt, ist
damit nicht belegt. Den Mechanismus entscheiden die Tests in §2.6.

### 2.3 Rechnung: Welche Hypothese erzeugt das Muster? [Rechnung]

Grundlage ist das Plan-Gelände nach Einbau (`p2_bettplan.py` → `z_neu`, identisch mit `talkaskade_soll.f32`), Raster 0,5 × 0,25 m.
- Die Editor-Spline ist `spiegel_je_m` + 0,05 m (6k §1).
- Band und Kolke sind wie in 6j definiert; die Kolke werden am tiefsten Planpunkt gelesen.
- Skript: `boden_modelle.py` (Code).
- Ergebnis: Gelände − Editor-Spline im Band = p10 / p50 / p90 **−0,14 / 0,68 / 1,51 m**.

| Hypothese (Modell) | Band Median | 0,25–1 / 1–2 m | Bett | Kolke > 10 cm | Kolk max |
|---|---|---|---|---|---|
| **gemessen** [Ferat] | **−64,7** | – | passt | **15/24** | **+84** |
| Glättung Kasten 1,83 m (5 Zellen) | −0,3 | +0,6 / −1,1 | +1,1 | 24/24 | +120 |
| Glättung Kasten 4,04 m (11 Zellen) | +0,2 | +11,5 / −6,6 | +10,0 | 24/24 | +169 |
| Glättung Kasten 1,10 m × 5 | −0,7 | +4,4 / −3,4 | +2,8 | 24/24 | +130 |
| Glättung Kasten 1,83 m × 3 | −0,3 | +6,1 / −3,7 | +3,2 | 24/24 | +147 |
| **Deckel min(Gelände; Spline + 0,03)** | **−64,6** | −30,4 / −94,3 | **0** | 0/24 | 0 |
| Deckel, c = 0 | −67,6 | −33,4 / −97,3 | 0 | 0/24 | 0 |
| Bezugshöhe −0,65 m | −65,0 | −65 / −65 | **−65** | 0/24 | – |

Alle Werte in cm. Eine Gauß-Glättung mit σ = 0,9 bzw. 1,8 m liegt im selben Muster (Band −0,7 bzw. +3,3 cm, Kolke 24/24).

**Lesart** [Ableitung]:
- **Warum die Glättung die Zeichen nicht trifft:** Glätten verschiebt den Boden um etwa σ²/2 · Krümmung.
  - Das Band besteht aus Schulter (Kante konvex: tiefer) und Böschungsfuß (konkav: höher). Beides gleicht sich im Median aus.
  - Eine Glättung erzeugt deshalb keinen systematischen Versatz von −65 cm.
  - Die Kolke (1,4–2,5 m breit, ≈ 1 m tief) sind starke Mulden und würden **alle** gefüllt.
- **Warum der Deckel trifft:**
  - Das Band liegt im Median 0,68 m über der Editor-Spline. Ein Boden, der nicht über Spline-Höhe steigt, liegt dort im Median
    0,65–0,68 m zu tief.
  - Das Bett liegt unter der Spline und bleibt unverändert.
  - Dazu passt die Tiefe G: Der gebackene Spiegel steht 13–16 cm über der Spline (T-b1). Über einem Boden auf Spline-Höhe ergibt das
    G ≈ 0,1–0,2 m im ganzen Band, obwohl das Wasser unter dem echten Gelände liegt.
  - Das Modell sagt 82 % Bandzellen mit Versatz < −10 cm voraus. Gemessen ist Tiefe > 1 cm in 83,2 %.
- **Die Kolke erklärt der Deckel nicht.** Sie brauchen eine eigene Ursache (§5).
- **Vorbehalt:** Das Plan-Gelände ist nicht `hoehe.f32`. Das alte Bett ist im Planer angenommen, die Landschaft liegt im 1-m-Raster. Die
  Rechnung entscheidet zwischen den Modellen, sie belegt den Mechanismus nicht. Den Beleg liefert Schritt 1 am echten Dump.

### 2.4 Hypothesen, unterscheidende Tests, Entscheidung

| Hypothese | Vorhersage im Dump | Stand | Unterscheidender Test | Entscheidung danach |
|---|---|---|---|---|
| **D: Deckel** – Boden ≈ min(Gelände; Spline + c) | Bandzellen mit Gelände > Spline + 0,15: Boden − Spline eng (p90 − p10 ≤ 15 cm); r(Versatz; Gelände − Spline) ≤ −0,8; 0,25–1 m ≈ −30, 1–2 m ≈ −94 cm | bestes Modell [Rechnung] | Schritt 1 (offline), dann Schritt 2 (Debug-Bodenkontur) | D bestätigt → Schritt 2 klärt, ob er im Eingang (D1/D2) oder in der gebackenen Ausgabe (D3) sitzt |
| D1: Boden aus der Wasser-Info bzw. Wassertiefe ≥ 0 gegen den Spline-Spiegel | wie D; Deckel folgt der Spline-Höhe, nicht einer festen Höhe | [Ableitung] | Schritt 2 | im Eingang → §2.5 |
| D2: Aufnahme mit Nah-/Fernebene an Spiegelhöhe + `bottom_contour_capture_offset` | wie D, c = Offset | [Ableitung], Feldbedeutung [zu prüfen] | Schritt 3b (Offset + 200 cm, Reset) | Versatz ändert sich mit dem Offset → D2; sonst D2 verworfen |
| D3: gebackene Ausgabe verschoben (z. B. Glättung der Oberflächen-Verschiebung, laut Epic) | wie D im Dump, aber Debug-Bodenkontur zeigt das echte Ufer | möglich [Epic lokal + Ableitung] | Schritt 2, dann 3a (`smoothing_width` 1, Reset) | Muster verschwindet mit 1 → nur Mess-Artefakt; Simulation gesund; „sichtbar“ genügt |
| S: Glättung des **Bodens** | Versatz folgt der Krümmung (r(Versatz; Laplace) ≥ 0,5), Band-Median ≈ 0, alle Kolke gehoben | **verworfen** als Ursache des Bandversatzes [Rechnung] | Schritt 1 prüft es mit | nur mit neuer Evidenz wieder aufnehmen |
| F: Aufnahme endet an der Spline-Breite, dahinter Ersatzwert | Sprung beim Kantenabstand der Spline-Grenze; Versatz hängt an der Spline-Breite | **verworfen**: T6j-C hat denselben Versatz [Ferat] | – | – |
| R: andere Bezugshöhe | gleicher Versatz in Bett und Band | **verworfen**: Bett passt [Ferat] | – | – |
| O: Hindernisse in der Aufnahme | nur Anhebungen, an Fußabdrücken | erklärt das Band nicht; Kandidat für die Kolke | §5 | §5 |

Das Skript `boden_befund.py` (Code) klassifiziert genau nach den Spalten „Vorhersage“. Sein Selbsttest erzeugt jeden Fall aus dem
Plan-Gelände mit bekannter Ursache und muss ihn wiederfinden: DECKEL (mit und ohne 3 cm Rauschen), GLÄTTUNG 1,8/4 m, ERSATZWERT, BEZUGSHÖHE,
kein Versatz. Heute: 7/7 richtig, „Selbsttest bestanden“. Das ist der Kontrollfall nach `pruefung.md` „Messwerkzeuge“: Der Sollwert ist
injiziert und stammt nicht vom Klassifikator.

### 2.5 Folgen, falls der Deckel im Eingang der Simulation sitzt (D1/D2) [Ableitung]

- **Phantom-Schulter:** Die Simulation sieht neben dem Bett eine waagrechte Fläche auf Spline-Höhe. Wasser kann darauf **hinter dem echten
  Ufer** fließen und an tiefen Stellen wieder austreten.
  - Ein Teil des sichtbaren Lippenschattens kann so entstehen.
  - Dazu passt, dass T6j-C (kein Nachfüllen im Band) den Lippenschatten kaum änderte.
- **Boden-Trick (6g §2, 6j) wirkungslos:** Ein unsichtbarer Streifen über Spline-Höhe würde gedeckelt. Er ist deshalb bis Schritt 2
  **zurückgestellt**.
- **Hydraulik:** Die Phantom-Fläche verbreitert den Abflussquerschnitt. Behebt man den Deckel, können Beckenspiegel und sichtbares Band sich
  ändern. Deshalb kommt der Kantenbewuchs erst danach.
- **Sitzt der Deckel nur in der Ausgabe (D3):** Keine dieser Folgen tritt ein. Dann genügt die Messgröße „sichtbar“, und die Simulation
  bleibt, wie sie ist.

### 2.6 Testfolge mit Erwartung und Abbruch

Alles im Speicher, nichts speichern. Rückweg: Level ohne Speichern neu laden. Nach B0 ist jede Eigenschaftsänderung ein neuer Lauf ab Reset,
`render_state` vorher LIVE_SIM, bis stabil (zwei Dumps im Abstand von 3 min < 1 pp), dann Dump.

| Schritt | Was | Aufwand | Erwartung je Hypothese | Entscheidung |
|---|---|---|---|---|
| **1 (nächste Handlung)** | `boden_befund.py --selbsttest`, dann `--dump` für Basis 0,3 und T6j-C, Welt-1-m-Raster. Felder s. Skriptkopf; `spline` = Z der Editor-Spline am s der Zelle (gleiche s-Zuordnung wie die Lippenschatten-Maske). Dazu `kolk` (Kolkellipsen aus `bettplan_p2.json` über `p2_bett_welt.py`) und `hindernis` (Fußabdrücke aller Instanzen in `bottom_contour_actors` bzw. mit Tag) | 30–45 min, ohne Editor | D: Urteil DECKEL mit den Vorhersagen oben. S: GLÄTTUNG. Sonst „uneindeutig“ | DECKEL → Schritt 2. GLÄTTUNG → Schritt 3a direkt. Uneindeutig → Profil quer an s 439 (beide Ufer) als Tabelle zurückmelden, kein Editor-Test |
| 2 | `render_state` = `DEBUG_RENDER_BOTTOM_CONTOUR` (16a). Messlatte (5 × 5 × 150 cm, Striche 5 cm) auf das linke Ufer bei s ≈ 439, Kantenabstand 1,5 m (Plan: Gelände 89,9 m, Spline ≈ 88,8 m); zweite Latte im Bett | 15 min; ob der Debug-Zustand ohne Reset umschaltet, zuerst mit Bett-Latte prüfen | D1/D2: Bodenkontur am Ufer flach auf Spline-Höhe, ≈ 1 m unter der Uferlatte. D3: Kontur folgt dem Ufer | flach → Schritt 3b und §2.5 gilt. Folgt dem Ufer → Schritt 3a |
| 3a | `smoothing_width` 1 statt 5, sonst Basis, Lauf wie B2 | ≈ 15–20 min | D3 über die Glättung: Deckel-Muster im Dump verschwindet oder schrumpft deutlich (Band-Median über −20 cm). Sonst unverändert ±3 cm | verschwindet → nur Ausgabe-Artefakt, Wert bleibt 5, „sichtbar“ ist das Maß. Unverändert → Glättung endgültig verworfen |
| 3b | `bottom_contour_capture_offset` lesen; Lauf mit Wert + 200 cm (Einheit zu prüfen) | ≈ 15–20 min | D2: Band-Versatz ändert sich mit dem Offset. D1: unverändert | ändert sich → Offset als Hebel, Wert an C2 gegenprüfen (geteilte Regel). Unverändert → D1: Recherche Wasser-Info-Boden mit lokalem Header-Auszug |

**Abbruch:**
- Bett der Talkaskade < 97 % oder Front < 788 m → Lauf ungültig, letzten gültigen Dump verwenden.
- Schritt 2 setzt die Simulation zurück → dann erst nach Schritt 1 und nur mit einem Lauf ab Reset im Debug-Zustand.

---

## 3. §6.2/§6.3 Messgröße „sichtbar“ und Prüfband-Ziel

### 3.1 Definition (gilt ab jetzt für Band, Bett und Kolke)

Je Zelle im Welt-1-m-Raster des Prüfbands, mit Spiegel W = R + Akteurhöhe, Gelände H = `hoehe.f32` und Tiefe G:

| Größe | Formel | Zweck |
|---|---|---|
| **nass** | G > 0,001 m | nur Kennzeichen, kein Zielmaß |
| **sichtbar_x** | nass ∧ W − H > x | Zielmaß Band und Bett |
| **verdeckt** | nass ∧ W − H ≤ 0 | Diagnose (Phantomwasser unter dem Gelände), kein Ziel; unter dem Deckel ≈ Band-Tiefe minus sichtbar |
| **Kolktiefe sichtbar** | W − H am tiefsten Landschaftspunkt des Kolks | ersetzt G im Kolk, weil der Boden dort zu hoch liegen kann (§5); Ziel 0,8–1,2 m (6f) |
| Hindernis-Zellen | Zellen unter einem Fußabdruck aus `bottom_contour_actors` | aus Zähler **und** Nenner des Bands nehmen, Anzahl mitmelden |

Begründung der Fälle:
- **Boden unter dem Gelände (Deckel):** Wasser unter H wird nicht gezeichnet. Es zählt nur, wo W über H durchstößt, und genau das ist
  `sichtbar`.
- **Boden über dem Gelände (Kolk, Hindernis):**
  - G unterschätzt die Wassersäule. Deshalb gilt im Kolk W − H.
  - Im Band verdeckt ein Hindernis das Wasser ganz oder teilweise. Deshalb nimmt man diese Zellen heraus und zählt sie nicht als trocken.
- **Trockene Zellen:** R ist dort kein Spiegel. Trockene Zellen gehen nie in `sichtbar` ein.

**Kontrollfall vor der nächsten Projektzahl** (`pruefung.md` „Wassertiefe/Uferband“). Synthetisches Raster mit sechs Bandzellen; Sollwerte
von Hand, nicht vom Werkzeug:

| Zelle | H | W | G | Erwartung |
|---|---|---|---|---|
| KS1 Bett | 10,00 | 10,30 | 0,30 | sichtbar_5 ja (Bett) |
| KS2 Deckel | 10,80 | 10,20 | 0,15 | nass, sichtbar nein, verdeckt ja |
| KS3 Lippenschatten | 10,10 | 10,22 | 0,12 | sichtbar_5 und sichtbar_10 ja |
| KS4 Film | 10,00 | 10,03 | 0,03 | sichtbar_2 ja, sichtbar_5 nein |
| KS5 trocken | 10,00 | 10,50 | 0 | nicht nass, nicht sichtbar |
| KS6 Hindernis | 10,00 | 10,20 | 0,20 | ausgeschlossen |

- Soll im Band (KS2–KS5): sichtbar_5 = 1/4 = 25 %, „Tiefe > 10 cm“ = 2/4 = 50 %, ausgeschlossen = 1.
- Toleranz: 0 Zellen Abweichung.

### 3.2 §6.2: richtig, und was daraus folgt

- **Ja, „sichtbar“ ist die richtige Größe.** Das Bild zeigt W über H, nicht G.
  - Belegt durch eure Beobachtung: kein sichtbares Wasser, wo G > 10 cm.
  - Gestützt durch die Rechnung: Füllen bis Editor-Spline + Überfall trifft die sichtbaren Zahlen, nicht die Tiefe-Zahlen.

  | Bereich | Rechnung, e = 0 m: > 1 / 2 / 5 / 10 cm | Rechnung, e = 0,15 m | gemessen sichtbar, Basis 0,3 |
  |---|---|---|---|
  | Band gesamt | 12,7 / 12,5 / 11,8 / 10,8 | 18,5 / 18,1 / 16,7 / 15,0 | 15,9 / 15,3 / 14,0 / 11,0 |
  | 0,25–1 m | 19,4 / 18,9 / 18,0 / 16,6 | 28,6 / 28,0 / 25,4 / 22,7 | 30,7 / 30,0 / 27,1 / 22,5 |
  | 1–2 m | 7,8 / 7,7 / 7,2 / 6,4 | 11,0 / 10,7 / 10,2 / 9,2 | 5,2 / 4,7 / 4,4 / 2,6 |

  - Nah an der Kante passt Füllen bis Spline + 0,15 m. Das ist genau der Überstand des gebackenen Spiegels aus T-b1.
  - Weiter außen bleibt das Wasser unter der Vorhersage, weil das Nachfüllen nur innerhalb der Spline-Breite (Bett + 1 m je Seite) wirkt
    [Ableitung wie 6j].
- **6g §3** (> 2 cm: 0,25–1 m ≤ 30 %, 1–2 m ≤ 5 %) ist mit 30,0 / 4,7 % **formal erreicht, ohne Reserve**. Die 2-cm-Schwelle liegt auf der
  16-Bit-Stufe von R. Deshalb ersetzt das Ziel aus §3.3 dieses Kriterium.
- **Nächster Hebel:** ja, der Kantenbewuchs (6j „Was fehlt“ Punkt 2). Gesetzt wird er nach Schritt 2. Er verdeckt die Filme 1–5 cm
  (Band: 15,9 − 14,0 = 1,9 pp, im inneren Band 3,6 pp) und die Ränder des Lippenschattens.

### 3.3 §6.3: neues Prüfband-Ziel

**Prüfband 0,25–2 m hinter der Plan-Bettkante: sichtbar_5 ≤ 15 % der Bandzellen. Toleranz ±1 pp. Bett: sichtbar_1 ≥ 99 %.**
Basis 0,3: 14,0 % → **erreicht**.

Begründung:
1. **Schwelle 5 cm:** R ist 16-Bit-Gleitkomma. Bei |R| 20–41 m beträgt die Stufe 2 cm, also ±1 cm (16g-N2 §3.1). 5 cm sind mehr als das
   Doppelte des Stufenfehlers. Filme bis 5 cm übernimmt der Kantenbewuchs, nicht die Simulation.
2. **15 %:** Das ist 6g §3 flächengewichtet auf 5 cm übertragen. Das innere Band umfasst 43 %, das äußere 57 % der Bandzellen:
   0,43 · 30 + 0,57 · 5 ≈ 15,7 % [Rechnung]. Ein strengeres Ziel bräuchte Gründe, die wir nicht haben.
3. **Die Geometrie setzt die Untergrenze:**
   - Füllen genau bis zur Editor-Spline ergibt 11,8 %.
   - Mit dem gemessenen Überstand von 0,15 m sind es 16,7 %.
   - Unter etwa 12 % kommt man nur mit einer anderen Spline-Form. Die Treppe der Sehens-Bäche bleibt aber.
4. **Toleranz ±1 pp:** Zwei Messungen derselben Basis (Dump 14.10. gegen frisch) unterschieden sich um ≤ 0,4 pp [Ferat].

Das alte Ziel „≤ 5 % nass“ (6b) galt der Tiefe G und entfällt. Bestätigt Schritt 2 den Deckel im Eingang, gilt das Ziel nach der Behebung für
den neuen Lauf. Bis dahin ist die 14,0-%-Zahl „vorläufig erreicht“.

---

## 4. §6.4 Nachfüllen: 0,3 bleibt – beantwortet

| Messgröße > 10 cm (0,4 gegen 0,3) [Ferat B2] | Maske 3 (Lippenschatten) | Maske 2 |
|---|---|---|
| Tiefe | +12,6 pp | +5,1 pp |
| **sichtbar** | **+7,2 pp** | **+2,0 pp** |

- 0,4 bringt keinen Vorteil. Bett 100 % und Front 788 m hält schon 0,3. 0,4 macht nur mehr sichtbares Wasser im Band.
- 0,3 bleibt in `fluss_sim_regeln.json` (v11).
- **Nicht unter 0,3 gehen:** 16g-N2 schätzt die Front-Schwelle bei ≈ 0,3 [Ableitung]. Ein Versuch mit 0,2 kostet einen Lauf und riskiert die
  Front. Es gibt keinen Testgrund, solange das Prüfband-Ziel erreicht ist.
- **Nachtrag zur Lesart von B2:** Sichtbar gemessen wirkt das Nachfüllen vor allem im Lippenschatten. H1 (Füllen bis Spline-Höhe) bleibt
  damit als Mechanismus gestützt, jetzt mit der richtigen Messgröße (§7).

---

## 5. §6.5 Kolke bis 84 cm zu flach – wartet auf Beleg (Kreuztabelle in Schritt 1)

**Befund aus dem Plan** [Rechnung, `bettplan_p2.json`]:
- Als SWR-Hindernis (`swr_hindernis` = true) stehen genau die 5 Beckenblöcke im Plan:
  - `SM_LichenedForestBoulder_01` bei s 505,9
  - `SM_MossyForestBoulder_02` bei s 460,4 und s 481,1
  - `SM_MossyForestBoulder_07` bei s 573,0
  - `SM_mountain_rock_big_01_1` bei s 528,4
- Sie sind 0,41–0,77 m groß.
- Ihr normierter Abstand zur nächsten Kolk-Ellipse beträgt 4,07–6,87, also mehr als das Doppelte der Halbachse. So hat sie der Planer auch
  gesetzt („nicht im Strahl und nicht im Kolkkern“, 6c).
- **Sie können 15 Kolke nicht anheben.** Herausnehmen oder Verkleinern würde nichts ändern.

**Kandidaten für die Anhebung:**

| Kandidat | Vorhersage | Unterscheidung |
|---|---|---|
| O1: **906 Alt-Hindernisse** (6f: „Hindernisse 906 + 5“), gesetzt auf das Gelände **vor** dem Aushub von bis zu 2,90 m | Angehobene Kolke ⇔ Alt-Hindernis im Kolk. Die Anhebung reicht bis zur Oberkante des Hindernisses | Kreuztabelle in Schritt 1 (`kolke_hoch_mit_hindernis` usw.) |
| O2: Landschaft in der Aufnahme gröber als `hoehe.f32` (LOD) | Anhebung wächst, je schmaler der Kolk ist (1,43–2,53 m). Kein Bezug zu Hindernissen | Anhebung gegen `breite_m` der 24 Kolke auftragen |
| S: Glättung | alle 24 Kolke um 63–144 cm (Median je Variante) angehoben | widerspricht 15/24 [Rechnung] → verworfen |

**Entscheidungsregel nach Schritt 1:**
- **O1, wenn** mindestens 13 der 15 angehobenen Kolke ein Hindernis enthalten und höchstens 2 der 9 flachen Kolke eines haben.
- **Dann ein Lauf ab Reset**, im Speicher, mit einer Kopie der Hindernisliste ohne Alt-Hindernisse im Bereich s 389–580, Kantenabstand ≤ 2 m.
  - Weg: `bottom_contour_actors` bzw. das Tag `SWR_Hindernis` am betroffenen `WH_`-Akteur entfernen.
  - Erwartung O1: Die angehobenen Kolke fallen auf ≤ +10 cm. Bett ≥ 99 %, Front 788 m.
- **Gilt O1, dann als Regel** (Exporter/Prüfer, Vorschlag):
  - Ein Aufnahme-Hindernis gilt nur, wenn seine Unterkante ≤ neues Gelände + 5 cm liegt, analog zur Schwebeprüfung des Felsplaners.
  - Und nur, wenn es nicht in Zone 2 (Kolk) steht.
  - Nach jedem Gelände-Einbau die Hindernisliste aus dem neuen Gelände neu bilden.
- **O2, wenn** kein Bezug zu Hindernissen besteht, aber eine Korrelation zur Kolkbreite (r ≤ −0,6). Dann ist es keine Frage der Blöcke.
  Kolk-Ziel als „Kolktiefe sichtbar“ (§3.1) prüfen und die Bettform nicht ändern.

---

## 6. §7 B5-Ost Halde: Deckung reicht – beantwortet

**Gegen die Ziele aus 21 §(a)** (`felsdeckung_regeln.json`: `deckung_halde_min` 0,5, `deckung_halde_oben_min` 0,6):

| Zone | Ziel | eure Vereinigung Fels | Plan (Prüfer) | Urteil |
|---|---|---|---|---|
| Halde | ≥ 50 % | 69,5 % | 77,4 % (6k: 79 %) | **erfüllt**, +19,5 pp |
| Halde oberes Drittel (t < 0,33) | ≥ 60 % | nicht gemeldet | 82,6 % | offen, nur dieser Wert fehlt |
| Schrofen | ≥ 50 % | 61,6 % | 57,1 % | erfüllt |
| Wand | ≥ 60 % | 95,0 % | 80,3 % | erfüllt |
| Fuß nah | ≥ 22 % | (Fuß gesamt 26,3 %) | 28,3 % | für „nah“ nicht getrennt gemeldet |

**Warum 9,5 pp unter dem Plan noch kein Mangel sind:**
- 79 % ist der Planwert, kein Ziel.
- Euer Verfahren misst anders als der Prüfer:
  - Ihr zentriert den Fußabdruck am Pivot, der Prüfer an der Mitte der gedrehten Bounds.
  - Der Prüfer nimmt eine Ellipse aus den Halbachsen × 0,85.
  - Ihr ignoriert die Neigung, und die Plan-Fußflächen liegen auf 26–40° Hang.
- Ein Teil der Lücke kann deshalb Messweg sein [Ableitung].
- Für den Bildeindruck zählt ohnehin die Pixelmessung (6j §2, KF1–KF7), nicht der Grundriss.

**Nachverdichten nur, wenn** das obere Drittel unter 60 % liegt oder eine 48-m-Zelle der Halde unter 50 %. Dann gilt diese Regel:
- **Nur Teppich**, keine neuen Blöcke: `TundraRockyGround_01`, `NordicBeachRockyGround_01/02`, `ForestRockFormation_05/06`. Skala 1,3–1,8,
  Yaw Falllinie ± 25°, 30–50 % eingegraben, alles wie 21 §(a).
- **Platzierung:**
  - Nur auf ungedeckte 0,5-m-Zellen der Halde, in denen die Vereinigung im Umkreis von 6 m unter dem Zielverlauf liegt (72 % am Wandfuß →
    42 % am unteren Rand).
  - Mittelpunkt in der größten Lücke.
  - Höchstens 30 % Überlappung mit Bestand.
  - Rasenzungen (Rauschen < −0,55) bleiben frei.
- **Ende:** Abbruch, sobald die Zelle ihren Zielwert erreicht. Es gilt die Quote je 48-m-Zelle aus 21 (> 2 m ≤ 1,2 je 100 m²).

**Stückzahl** [Rechnung, Schätzung]:
- Die Halde hat 2,04 ha = 20 400 m². Das Ziel „wie Plan“ (79 %) braucht 9,5 pp · 20 400 m² ≈ **1 940 m²** zusätzliche Vereinigung.
- Je Plan-Stück kommen im Mittel ≈ 25 m² Fußfläche nach Prüfer-Definition (145 % · 2,01 ha / 1 149 Stück).
- Gezielt in Lücken gesetzt (≤ 30 % Überlappung): 1 940 / (25 · 0,7) ≈ **110 Stück**.
- Zufällig gesetzt (Poisson, −ln(0,21) + ln(0,305) = 0,37 · 20 400 m²) wären es ≈ 300.
- **Richtwert: 150 Teppichstücke**, genug, falls nur das obere Drittel nachgezogen werden muss.

---

## 7. Korrekturen an eigenen Antworten

| Antwort | Aussage | Korrektur |
|---|---|---|
| 6i Kurzfazit 7 und §5 | „65 % > 5 cm und 46 % > 10 cm sind echtes Wasser neben dem Bett, kein dünner Film; unsere Annahme 20–30 % war falsch“ | **Falsch.** Das war die Tiefe G über einem zu tiefen Boden. Sichtbar sind es 14,0 / 11,0 %. Unsere 6g-Erwartung (20–30 % bei > 5 cm) war nicht widerlegt, sie lag eher zu hoch |
| 6i „Was fehlt“ 2 | „Band bei > 10 cm zu 46 % nass“ | sichtbar 11,0 % |
| 6j Kurzfazit 1 | H1 sagt 12,8 % voraus, „T01 misst 13,1 %“ | Der T01-Wert ist Tiefe. Die Übereinstimmung ist **kein Beleg**. Neu gestützt ist H1 durch sichtbar: Basis 11,0 % gegen 10,8 % (Editor-Spline) bei > 10 cm, nah an der Kante mit Überstand 0,15 m (§3.2) |
| 6j §1.1 | „nasse Zellen zu 100 % im Lippenschatten“, Band „78,6 %“ als Argument gegen Variante A | Das 100 % war eine Planrechnung, die 78,6 % sind Tiefe. **Variante A bleibt verworfen**, aus den Gründen der Bauweise, die davon unabhängig sind |
| 6j Tabelle T6j-A/B/C | formale Urteile über Tiefe > 10 cm | **ungültig als Maß.** Mit sichtbar neu gelesen: T6j-B stützt H1 (Maske 3 +7,2 pp, Maske 2 +2,0 pp). T6j-C bleibt ohne nennenswerte Wirkung |
| 6j „Lippenschatten“ | Wasser dort folgt dem Nachfüllen auf Spline-Höhe | Die Zone ist geometrisch echt. Ein Teil ihres sichtbaren Wassers kann aber über die Phantom-Schulter des Deckels kommen (§2.5). Belegt erst nach Schritt 2 |
| 6b / 6f | Prüfband-Ziel ≤ 5 % nass (Tiefe) | ersetzt durch §3.3 |
| 6g §2, 6j | Boden-Trick als nächster Hebel | **zurückgestellt**, bis Schritt 2 einen Deckel im Eingang ausschließt |

---

## Code

Beide Skripte laufen mit `python -I` im Repo, nur mit NumPy, deterministisch. Ausgaben vom 18.10.2026 stehen jeweils darunter.

**`boden_modelle.py`** – Modelle gegen das Plan-Gelände (§2.3, §3.2):

```python
# boden_modelle.py - python -I boden_modelle.py <repo>
# 16h-6k §6.1 offline: Welche Boden-Hypothese erzeugt das gemessene Muster? Grundlage: Plan-Gelaende p2 (deterministisch
# aus p2_bettplan.py, gleich talkaskade_soll.f32), Editor-Spline = spiegel_je_m + 0,05 m (6k §1).
# Soll [Ferat 6k]: Band 0,25-2 m Boden - Gelaende Median -64,7 cm; Bett passt; Hauptkolke 15/24 > +10 cm, max +84 cm.
import importlib.util, json, sys, numpy as np
R = sys.argv[1].rstrip('/') + '/recherche/antworten/'
sp = importlib.util.spec_from_file_location('p2b', R + 'skripte/p2_bett/p2_bettplan.py')
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
X = m.rechne(); Z = X['z_neu']; S = np.asarray(X['G']['S']); U = np.asarray(X['G']['U'])   # Raster 0,5 x 0,25 m
a = np.fromfile(R + 'p2_bett/talkaskade_soll.f32', '<f4').reshape(6, 384, 101); kante, spg = a[5], a[3]
zon = np.fromfile(R + 'p2_bett/talkaskade_zonen.u8', np.uint8).reshape(384, 101)
d = json.load(open(R + 'p2_bett/bettplan_p2.json'))
J = np.array(d['spiegel_je_m']['punkte']); spl = np.repeat((np.interp(S, J[:, 0], J[:, 1]) + 0.05)[:, None], 101, 1)
band = (kante >= 0.25) & (kante <= 2.0) & np.isin(zon, [5, 6, 7]); b1, b2 = band & (kante < 1), band & (kante >= 1)
bett = np.isin(zon, [1, 3, 4])                                       # Bett ohne Kolk
ss, uu = np.meshgrid(S, U, indexing='ij'); KZ = []
for b in (b for b in d['becken'] if b['typ'] == 'haupt'):            # 24 Hauptbecken
    k = b['kolk']; e = ((ss - k['s_m']) / (k['laenge_m'] / 2)) ** 2 + ((uu - k['u_m']) / (k['breite_m'] / 2)) ** 2 <= 1
    KZ.append(e & (zon == 2) if (e & (zon == 2)).any() else e)
DX = 0.367                                                            # SWR-Zelle

def box(z, w, it=1):
    for _ in range(it):
        for ax, hh in ((0, 0.5), (1, 0.25)):
            n = max(1, int(round(w / hh))); n += (n + 1) % 2; k = np.ones(n) / n
            p = np.pad(z, [(n // 2, n // 2) if q == ax else (0, 0) for q in (0, 1)], mode='edge')
            z = np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), ax, p)
    return z

def zeile(name, boden):
    o = (boden - Z) * 100; km = np.array([o[k][np.argmin(Z[k])] for k in KZ])   # Kolk: am tiefsten Planpunkt
    print(f'{name:30s} Band Median {np.median(o[band]):+6.1f} (0,25-1: {np.median(o[b1]):+6.1f} | 1-2: {np.median(o[b2]):+6.1f}) '
          f'| Bett {np.median(o[bett]):+5.1f} | Kolke >10 cm {int((km > 10).sum()):2d}/24, max {km.max():+6.1f}, Median {np.median(km):+6.1f}')

print('Gelaende - Editor-Spline im Band: p10/p50/p90 %.2f / %.2f / %.2f m' % tuple(np.percentile((Z - spl)[band], [10, 50, 90])))
for w, it in ((5 * DX, 1), (11 * DX, 1), (3 * DX, 5), (5 * DX, 3)):
    zeile(f'Glaettung Kasten {w:.2f} m x{it}', box(Z, w, it))
for c in (0.0, 0.03):
    zeile(f'Deckel min(Gelaende, Spline+{c:.2f})', np.minimum(Z, spl + c))
zeile('Bezugshoehe -0,65 m', Z - 0.65)
f = lambda t, mk: ' / '.join(f'{100 * np.mean(t[mk] > x):.1f}' for x in (0.01, 0.02, 0.05, 0.10))
print('"sichtbar" vorhergesagt = Spiegel - Gelaende > 1/2/5/10 cm, Spiegel = Editor-Spline + e (Fuellen bis zur Spline, H1):')
for e in (0.0, 0.10, 0.15):
    print(f'  e {e:.2f} m: Band {f(spl + e - Z, band)} | 0,25-1 m {f(spl + e - Z, b1)} | 1-2 m {f(spl + e - Z, b2)}')
print('  gemessen Basis 0,3 [Ferat 6k]: Band 15,9 / 15,3 / 14,0 / 11,0 | 0,25-1 m 30,7 / 30,0 / 27,1 / 22,5 | 1-2 m 5,2 / 4,7 / 4,4 / 2,6')
```

Ausgabe:
```
Gelaende - Editor-Spline im Band: p10/p50/p90 -0.14 / 0.68 / 1.51 m
Glaettung Kasten 1.83 m x1     Band Median   -0.3 (0,25-1:   +0.6 | 1-2:   -1.1) | Bett  +1.1 | Kolke >10 cm 24/24, max +119.8, Median  +63.1
Glaettung Kasten 4.04 m x1     Band Median   +0.2 (0,25-1:  +11.5 | 1-2:   -6.6) | Bett +10.0 | Kolke >10 cm 24/24, max +169.2, Median +113.9
Glaettung Kasten 1.10 m x5     Band Median   -0.7 (0,25-1:   +4.4 | 1-2:   -3.4) | Bett  +2.8 | Kolke >10 cm 24/24, max +130.3, Median  +78.4
Glaettung Kasten 1.83 m x3     Band Median   -0.3 (0,25-1:   +6.1 | 1-2:   -3.7) | Bett  +3.2 | Kolke >10 cm 24/24, max +147.1, Median  +91.5
Deckel min(Gelaende, Spline+0.00) Band Median  -67.6 (0,25-1:  -33.4 | 1-2:  -97.3) | Bett  +0.0 | Kolke >10 cm  0/24, max   +0.0, Median   +0.0
Deckel min(Gelaende, Spline+0.03) Band Median  -64.6 (0,25-1:  -30.4 | 1-2:  -94.3) | Bett  +0.0 | Kolke >10 cm  0/24, max   +0.0, Median   +0.0
Bezugshoehe -0,65 m            Band Median  -65.0 (0,25-1:  -65.0 | 1-2:  -65.0) | Bett -65.0 | Kolke >10 cm  0/24, max  -65.0, Median  -65.0
"sichtbar" vorhergesagt = Spiegel - Gelaende > 1/2/5/10 cm, Spiegel = Editor-Spline + e (Fuellen bis zur Spline, H1):
  e 0.00 m: Band 12.7 / 12.5 / 11.8 / 10.8 | 0,25-1 m 19.4 / 18.9 / 18.0 / 16.6 | 1-2 m 7.8 / 7.7 / 7.2 / 6.4
  e 0.10 m: Band 16.3 / 16.0 / 15.0 / 13.0 | 0,25-1 m 24.8 / 24.3 / 22.7 / 19.7 | 1-2 m 9.9 / 9.8 / 9.2 / 7.9
  e 0.15 m: Band 18.5 / 18.1 / 16.7 / 15.0 | 0,25-1 m 28.6 / 28.0 / 25.4 / 22.7 | 1-2 m 11.0 / 10.7 / 10.2 / 9.2
  gemessen Basis 0,3 [Ferat 6k]: Band 15,9 / 15,3 / 14,0 / 11,0 | 0,25-1 m 30,7 / 30,0 / 27,1 / 22,5 | 1-2 m 5,2 / 4,7 / 4,4 / 2,6
```

**`boden_befund.py`** – Klassifikator für den echten Dump (Schritt 1) mit Selbsttest:

```python
# boden_befund.py - 16h-6k §6.1: Woher kommt der tiefe Simulationsboden im Band?
#   python -I boden_befund.py --dump befund.npz [--zelle 1.0]   Auswertung eines vorhandenen Dumps (ohne Editor)
#   python -I boden_befund.py --selbsttest <repo>              Kontrollfaelle mit bekannter Ursache (Plan-Gelaende p2)
# befund.npz (gleiches Raster, z. B. Welt-1-m wie das Pruefband), alle Hoehen in m absolut:
#   boden    = R + Akteurhoehe - G (Simulationsboden aus dem Dump)     gelaende = hoehe.f32
#   spline   = Z der Editor-Spline am s der Zelle                       tiefe    = G
#   kante    = Abstand zur Plan-Bettkante (m, 0 im Bett)                maske    = 0 frei, 1 Bett, 2 Band, 3 Lippenschatten
#   optional kolk = Kolk-Nummer je Zelle (-1 sonst), hindernis = 1 unter einem Fussabdruck aus bottom_contour_actors
import argparse, json, sys, numpy as np

def lap(z, h):
    p = np.pad(z, 1, mode='edge')
    return (p[:-2, 1:-1] + p[2:, 1:-1] - 2 * z) / h[0] ** 2 + (p[1:-1, :-2] + p[1:-1, 2:] - 2 * z) / h[1] ** 2

def corr(a, b):
    a, b = a - a.mean(), b - b.mean()
    return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum() + 1e-12))

def befund(D, h):
    o = D['boden'] - D['gelaende']                                    # Versatz Boden - Gelaende (m)
    band = np.isin(D['maske'], [2, 3]) & (D['kante'] >= 0.25) & (D['kante'] <= 2.0)
    hoch = band & (D['gelaende'] - D['spline'] > 0.15)                 # Gelaende klar ueber der Spline
    dsp = (D['boden'] - D['spline'])[hoch]
    innen, aussen = band & (D['kante'] < 1.0), band & (D['kante'] >= 1.0)
    L = lap(D['gelaende'], h)
    r = {'band_versatz_median_cm': 100 * float(np.median(o[band])),
         'band_versatz_p10_p90_cm': [100 * float(np.percentile(o[band], q)) for q in (10, 90)],
         'boden_minus_spline_bei_hoch_p10_p50_p90_cm': [100 * float(np.percentile(dsp, q)) for q in (10, 50, 90)],
         'r_versatz_gegen_gelaende_minus_spline': corr(o[band], (D['gelaende'] - D['spline'])[band]),
         'r_versatz_gegen_laplace': corr(o[band], L[band]),
         'sprung_innen_aussen_cm': 100 * float(np.median(o[aussen]) - np.median(o[innen])),
         'bett_versatz_median_cm': 100 * float(np.median(o[D['maske'] == 1]))}
    breite = r['boden_minus_spline_bei_hoch_p10_p50_p90_cm'][2] - r['boden_minus_spline_bei_hoch_p10_p50_p90_cm'][0]
    if breite <= 15 and r['r_versatz_gegen_gelaende_minus_spline'] <= -0.8 and r['band_versatz_median_cm'] <= -10:
        r['urteil'] = 'DECKEL: Boden ~ min(Gelaende, Spline + c)'
    elif r['r_versatz_gegen_laplace'] >= 0.5:                        # Glaettung: Versatz ~ +sigma^2/2 * Laplace (Mulde hoch, Kante tief)
        r['urteil'] = 'GLAETTUNG des Bodens'
    elif abs(r['band_versatz_median_cm']) < 10:
        r['urteil'] = 'kein Bandversatz'
    elif abs(r['sprung_innen_aussen_cm']) >= 30:
        r['urteil'] = 'ERSATZWERT hinter der Spline-Breite'
    elif abs(r['band_versatz_median_cm'] - r['bett_versatz_median_cm']) <= 5:
        r['urteil'] = 'BEZUGSHOEHE (gleicher Versatz in Bett und Band)'
    else:
        r['urteil'] = 'uneindeutig'
    if 'kolk' in D:
        k = D['kolk']; ids = [int(i) for i in np.unique(k) if i >= 0]
        kv = {i: 100 * float(np.median(o[k == i])) for i in ids}
        r['kolke_ueber_10cm'] = sum(v > 10 for v in kv.values()); r['kolke_n'] = len(ids)
        if 'hindernis' in D:
            mit = {i for i in ids if (D['hindernis'][k == i] > 0).any()}
            r['kolke_hoch_mit_hindernis'] = sum(kv[i] > 10 for i in mit)
            r['kolke_hoch_ohne_hindernis'] = sum(kv[i] > 10 for i in ids if i not in mit)
            r['kolke_flach_mit_hindernis'] = sum(kv[i] <= 10 for i in mit)
    return r

def box(z, n, h):
    out = z
    for ax, hh in ((0, h[0]), (1, h[1])):
        m = max(1, int(round(n / hh))); m += (m + 1) % 2; k = np.ones(m) / m
        p = np.pad(out, [(m // 2, m // 2) if a == ax else (0, 0) for a in (0, 1)], mode='edge')
        out = np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), ax, p)
    return out

def selbsttest(repo):
    import importlib.util
    sp = importlib.util.spec_from_file_location('p2b', repo.rstrip('/') + '/recherche/antworten/skripte/p2_bett/p2_bettplan.py')
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    X = m.rechne(); Z = X['z_neu']; S = np.asarray(X['G']['S']); h = (0.5, 0.25)
    a = np.fromfile(repo.rstrip('/') + '/recherche/antworten/p2_bett/talkaskade_soll.f32', '<f4').reshape(6, 384, 101)
    zon = np.fromfile(repo.rstrip('/') + '/recherche/antworten/p2_bett/talkaskade_zonen.u8', np.uint8).reshape(384, 101)
    d = json.load(open(repo.rstrip('/') + '/recherche/antworten/p2_bett/bettplan_p2.json'))
    J = np.array(d['spiegel_je_m']['punkte']); spl = np.repeat((np.interp(S, J[:, 0], J[:, 1]) + 0.05)[:, None], 101, 1)
    maske = np.where(np.isin(zon, [1, 2, 3, 4]), 1, np.where(np.isin(zon, [5, 6, 7]), 2, 0)).astype(np.uint8)
    basis = dict(gelaende=Z, spline=spl, kante=a[5], maske=maske, tiefe=np.zeros_like(Z))
    rausch = np.random.default_rng(6).normal(0.0, 0.03, Z.shape)    # 3 cm: 16-Bit-Rundung + Abtastung
    faelle = {'DECKEL': np.minimum(Z, spl + 0.02),
              'DECKEL mit 3 cm Rauschen': np.minimum(Z, spl + 0.02) + rausch,
              'GLAETTUNG 1,8 m': box(Z, 1.84, h),
              'GLAETTUNG 4 m': box(Z, 4.04, h),
              'ERSATZWERT': np.where((a[5] >= 1.0) & (maske != 1), Z - 1.5, Z),
              'BEZUGSHOEHE': Z - 0.65,
              'kein': Z}
    ok = True
    for soll, boden in faelle.items():
        r = befund(dict(basis, boden=boden), h)
        hit = r['urteil'].upper().startswith(soll.split()[0].upper())
        ok &= hit
        print(f"{soll:12s} -> {r['urteil']:45s} Band {r['band_versatz_median_cm']:+6.1f} cm  r_Spline {r['r_versatz_gegen_gelaende_minus_spline']:+.2f}  "
              f"r_Laplace {r['r_versatz_gegen_laplace']:+.2f}  Sprung {r['sprung_innen_aussen_cm']:+6.1f}  {'OK' if hit else 'FALSCH'}")
    print('Selbsttest', 'bestanden' if ok else 'NICHT bestanden'); return ok

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--dump'); ap.add_argument('--zelle', type=float, default=1.0)
    ap.add_argument('--selbsttest'); A = ap.parse_args()
    if A.selbsttest:
        sys.exit(0 if selbsttest(A.selbsttest) else 1)
    D = dict(np.load(A.dump)); print(json.dumps(befund(D, (A.zelle, A.zelle)), indent=1, ensure_ascii=False))
```

Ausgabe `python -I boden_befund.py --selbsttest <repo>` (Exit 0):
```
DECKEL       -> DECKEL: Boden ~ min(Gelaende, Spline + c)     Band  -65.6 cm  r_Spline -0.96  r_Laplace +0.27  Sprung  -63.8  OK
DECKEL mit 3 cm Rauschen -> DECKEL: Boden ~ min(Gelaende, Spline + c)     Band  -65.4 cm  r_Spline -0.95  r_Laplace +0.27  Sprung  -62.8  OK
GLAETTUNG 1,8 m -> GLAETTUNG des Bodens                          Band   -0.3 cm  r_Spline -0.48  r_Laplace +0.75  Sprung   -1.7  OK
GLAETTUNG 4 m -> GLAETTUNG des Bodens                          Band   +0.2 cm  r_Spline -0.66  r_Laplace +0.59  Sprung  -18.1  OK
ERSATZWERT   -> ERSATZWERT hinter der Spline-Breite           Band -150.0 cm  r_Spline -0.44  r_Laplace -0.03  Sprung -150.0  OK
BEZUGSHOEHE  -> BEZUGSHOEHE (gleicher Versatz in Bett und Band) Band  -65.0 cm  r_Spline +0.00  r_Laplace +0.00  Sprung   +0.0  OK
kein         -> kein Bandversatz                              Band   +0.0 cm  r_Spline +0.00  r_Laplace +0.00  Sprung   +0.0  OK
Selbsttest bestanden
```

**Hinweise zu Schritt 1:**
- Der Selbsttest läuft im Plan-Raster 0,5 × 0,25 m, der Dump im Welt-1-m-Raster (`--zelle 1.0`). Die Laplace-Korrelation ist im gröberen
  Raster schwächer.
- Gibt der echte Dump `r_Laplace` zwischen 0,3 und 0,5 und kein anderes Urteil, gilt er als „uneindeutig“. Dann folgt die Profiltabelle, kein
  Editor-Test.
- `np.load` lädt ohne Pickle.

---

## Was fehlt bis Witcher 4

Messlatte ist die UE5-Techdemo, belegt nur über Presse und Suchauszüge (wie 6e): Wasser mit Körper im Bett, dunkle klare Kolke, nasse Steine an
der Linie, Bewuchs bis ans Wasser, Halden als Fläche aus Fels. Nach Wirkung sortiert:

1. **Wasser sitzt richtig im Bett, physikalisch und im Bild.**
   - Schritt 1–2 klären, ob die Simulation auf einer Phantom-Schulter rechnet.
   - Erst dann sind Beckenspiegel, Lippenschatten und Front belastbar. Das Prüfband ist sichtbar gemessen schon im Ziel.
2. **Tiefe, dunkle Kolke.** 15 von 24 Kolken sind bis 84 cm zu flach. Damit fehlt das klare, dunkle Becken, das die Techdemo trägt
   (6f Problem B). Hebel ist die Hindernisliste (§5), nicht die Bettform.
3. **Kantenbewuchs bis an die Wasserlinie** (6e/6j): Kantengras, Moos, Farne. Er verdeckt die Filme 1–5 cm und die Lippenschatten-Ränder.
   Setzen nach Schritt 2.
4. **BAKED_SIM spielfest:** Gepackter Build (T-a3) und Kosten an p2 (T-a1/T-a2) sind offen. T-c1 hat den festen Render-State bestätigt.
5. **Verlässliche Dichtezahlen:** Pixelmessung KF1–KF7 (6j §2), dann Halde und Talkaskade im Bild statt im Grundriss bewerten. B5-Halde
   erfüllt das Grundrissziel schon.
6. **Nasse Steine an der sichtbaren Linie:** `M_EL_Mountain_NL` (**anzulegen**) und die MS2-MIs. Der Versatz +20 cm passt zu T-b1
   (Spiegel 13–16 cm über der Spline).
7. Rinnenköpfe an den Bachanfängen, Fall-Effekte nur an Fällen, Licht im Einschnitt (6e/6f/6j §3).

## Quellen

Abruf 18.10.2026.
- **Nicht erreichbar:**
  - `dev.epicgames.com` (WebFetch: DNS-Fehler ENOTFOUND)
  - `forums.unrealengine.com` (WebFetch: DNS-Fehler ENOTFOUND)
  - Je ein Versuch, kein weiterer Zugang.
- **Darum:** Alle Epic-Angaben unten sind **Suchauszüge** bzw. Ferats lokale Zusammenfassung (16f).

- [API: UShallowWaterRiverComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent?lang=en-US)
  – `SmoothingWidth` (int) und `SmoothingCutoff` (float) in `ShallowWaterRiverActor.h`, ohne Beschreibung; Bottom-Contour-Felder und
  Collision Dilation gelistet [Suchauszug]. Versionsbezug der Seite nicht erkennbar.
- [Python 5.5: unreal.ShallowWaterRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent?application_version=5.5)
  – `use_capture`, `bottom_contour_capture_offset`, `baked_water_surface_texture` gelistet, keine Glättungsbeschreibung im Auszug [Suchauszug].
- [Tutorial: Baked River Simulations – Parameter Reference](https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference)
  bzw. [Forum 2512112](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112) – „Smoothing
  Width/Cutoff: Glättung der Oberflächen-Verschiebung bei harten Kanten“, Use Capture als Tiefenaufnahme [Epic lokal, 16f; aus der Cloud
  nur Einleitung im Suchauszug].
- Im Repo: 6i (T-b1/T-c1-Entscheidungsregeln), 6j (H1, Lippenschatten, T6j-A/B/C), 16a §d (Bodenerfassung ganzer Akteure),
  16g-N2 §3.1 (Half-Float-Stufen) und Band + 2 m, 6c (5 SWR-Hindernisse), 6f (906 + 5 Hindernisse, Aushub −2,90 m), 21 §(a) und
  `felsdeckung_regeln.json` (Deckungsziele), `felsdeckung_pruefen.py` (Fußabdruck-Ellipse × 0,85, Bounds-Mitte), `pruefbericht_B5.txt`.

**Nicht belegt bzw. nicht erreichbar:**
- Wie die SWR Landschaft, Hindernisse und Spline zum Boden verrechnet.
- Was `SmoothingCutoff` und `bottom_contour_capture_offset` genau tun, mit Einheit.
- Ob `DEBUG_RENDER_BOTTOM_CONTOUR` ohne Reset umschaltet.
- Schritte 1–3 schließen diese Lücken lokal; ein Header-Auszug aus 5.8.3 (Kommentare zu den drei Feldern) wäre die sichere Ergänzung,
  falls Schritt 3b nötig wird.

## Rückfragen

Keine, die den nächsten Schritt ändert.
