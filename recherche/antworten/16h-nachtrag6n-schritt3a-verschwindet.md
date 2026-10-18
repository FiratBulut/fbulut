# Antwort 16h Nachtrag 6n – Deckel geschlossen; Glättungsbreite 1 nach einem Prüftor übernehmen; Schaum nicht über die Glättung steuern

Gelesen: recherche/auftraege/16h-nachtrag6n-schritt3a-verschwindet.md @ f1baf7bbac4e53847fa7b3773f6fd1e5af6f58ca (Commit c029476)

Stand 18.10.2026. Gesamtauftrag 16h (Erlenbach p2, Talkaskade s 389–580). Bearbeiter: Cloud-Recherche. Bereich: Glättungsbreite der
SWR p2, Messdefinition, Schaum. Wasser bleibt lokal unverändert. Die nächste Handlung ist eine Auswertung vorhandener Dumps ohne Editor.

**Bezug, ebenfalls gelesen (alle Commit c029476):**
- `recherche/antworten/16h-nachtrag6m-schritt2-band-b.md` @ e077fa0f455bf50993093c76d54e98c10d21bd60 (ganz)
- `recherche/antworten/16h-nachtrag6l-boden-schritt1.md` @ 68e2f510532a8edb5b921e981f02359c76a30fea (ganz)
- `recherche/antworten/16h-nachtrag6k-t6j-ergebnisse.md` @ bd2ee3191705d425ce7d96a826143f2de3b26667 (ohne Code)
- `recherche/README.md` @ 778d8a7b8ac17fcaceb262ee8b63e46898ff7051, `recherche/vorlagen/pruefung.md` @ 5daf4a9187ba35288dc4838f9461118e0960d068
- Bild `recherche/bilder/swr_p2/t6m3a_glaettung5_gegen_1.jpg` @ 283d44a6cfcef7143d132014c1fa4656f4abec6e (selbst angesehen, 6 Kamerapaare)
- Schaum: `recherche/antworten/16e-ferat-schaum-weg-langsamer.md` @ c3534303f176adc5e8307b47bf339b8ab63a8df9 (Kurzfazit, §1.5),
  `recherche/antworten/16f-rueckfrage-epic-parameter-lokal.md` @ 2df21f03041f4840d29cb206a62cf9a709ea33da (§3, §5),
  `recherche/antworten/16h-nachtrag6i-baked-sim-tests-stand.md` @ b3582ca1c2e105c43cbb346c06418a212d133e4b (§1.2 Schaum-Vorgabe),
  `recherche/auftraege/16h-nachtrag-materialtest.md` @ cb8831e2dfd31cb6fa15450ee66c4208023194bc (Variante F, `Foam Opacity` 0)
- Treppe und Fälle: `recherche/antworten/13f-p2-1m-korrekturen.md` @ f41e2df41be3c9dde288771c3f4c8092ba8f2684 (A8),
  `recherche/antworten/skripte/fluss_sim/fluss_sim_regeln.json` @ 9e232c1fd2bac846d6f2c16f41db3728b251e06f (`fall_schwelle_m`, `schaum`, `vorhang`),
  `recherche/antworten/p2_bett/bettplan_p2.json` @ 0013ef4a1922330462308bc7dbad8729ae6a1ef3 (`lippen`, `effekte_vorschlag`, Zonen)

**Kennzeichnung:** [Ferat] eure Messung bzw. Rolle-1-Lesung aus 6n · [Projekt] Regel oder Befund im Repo · [Bild] von mir am Bild gesehen ·
[Ableitung] geschlossen, nicht belegt · [zu prüfen] nicht belegt.

## Kurzfazit

0. **Deckel – beantwortet und geschlossen.** Ergebnis E1 aus 6m §1.3 für das Band: Er ist ein Ausgabe-Artefakt (Saum-Extrapolation in
   trockene Zellen), und die Simulation ist gesund (§1). Der Kolk-Teil der Hydraulikprüfung fehlt noch; er läuft im Prüftor mit.
1. **F1 Glättungsbreite – beantwortet: Breite 1 übernehmen, wenn das Prüftor (§2.3) besteht.** Nicht bei 5 bleiben, nur weil die Regel aus
   6k §2.6 es sagt. Deren Annahme „Glättung betrifft nur Wasser, das nicht gezeichnet wird“ hat 6n widerlegt.
   - Bindend sind: Kernbett ≥ 99 % (bei 5 verfehlt), Prüfband sichtbar_5 ≤ 15 % ± 1 pp (für 1 noch nicht gemessen) und die Kolke.
   - Die 6,0 % im Streifen 1–2 m messen das alte Ziel aus 6g §3. 6k §3.3 hat es ersetzt; es wird nur noch gemeldet.
   - Keine Reihe 2/3/4. Ein Zwischenwert kommt nur als einziger Ersatztest in Frage, und dann Breite 2 statt 3 (§2.4).
2. **F2 Messweg – beantwortet, wie in 6m §3.** Der Boden kommt aus der Debug-Kontur und wird nur neu gelesen, wenn sich der Boden
   ändert. Neu kommt hinzu, dass `nass_sim` bei Breite 5 nicht trägt und die Werte für „sichtbar“ an die Breite gebunden sind (§3).
3. **F3 Schaum – beantwortet: kein Verlust.** An einer Stufe ist weniger Schaum ausdrücklich gewollt. An einem Fall darf es Schaum geben,
   aber er gehört dann in den Schaumweg (Niagara-Grenzen, Aufprall-Effekte) und nicht in die Glättungsbreite (§4).
4. **Eigene Fehler korrigiert (§5):** Für die Basis meldete 6m „Kernbett erfüllt“, obwohl es nie gemessen war. Die Vorhersagen „Kernbett
   ± 1 pp“, „Ufer treppig“ und „Schaum bleibt“ sind gescheitert.

**Nächste Handlung (genau eine, lokal, ohne Editor, ≈ 20 min): das Prüftor P6N, also die Dumps T6M3A_2 (Breite 1) und T6L2B_2 (Breite 5)
mit demselben Auswerteweg wie 6n auswerten.** Gemessen werden G1–G3 und die Diagnose D aus §2.3.
- **Erfolgskriterium:** Alle Werte sind gemeldet, mit Dump-ID und Breite, und das Ergebnis fällt in U1, U2 oder U3 (§2.3).
- **Abbruch:** T6M3A_2 liegt nicht als Datei vor (nur im Speicher). Dann entfällt P6N, und dieselben Werte werden im Speicherlauf (§2.5)
  vor dem Speichern berechnet. Gespeichert wird nur bei U1.

---

## 1. Deckel: formaler Abschluss

| Kriterium aus 6m §1.2/§1.3 (vorab) | Erwartung | 6n [Ferat] | Urteil |
|---|---|---|---|
| Band-Median Sim-Boden − Gelände | −20 … 0 cm | −62,3 → **−3,5 cm** | erfüllt |
| Reichweite des Saums | ≤ 2 Zellen | 6 → **2 Zellen** (0,73 m) | erfüllt |
| Front, Bett | 788 m ± 2 m, Bett ≥ 97 % | 788 m, 100 % | erfüllt |
| Kolke: Median \|ΔW\| ≤ 2 cm, kein Kolk > 5 cm | – | nicht gemeldet | **im Prüftor (G2)** |
| Kernbett sichtbar_1 ± 1 pp | ± 1 pp | **+2,4 pp** | verfehlt; neuer Befund, nicht Teil des Deckels (§2.2) |

**Damit geschlossen (beantwortet):**
- **Ursache des Deckels:** Das Programm schreibt in trockene Zellen Nachbarspiegel und gemittelte Tiefe. R − G ist dort kein Boden. Die
  Simulation rechnet auf dem echten Gelände (Kontur = Gelände, Band B).
- **Damit entfallen:** die Schritte 3b (Capture-Offset) und „Header lesen“ aus 6k/6l, die Kandidaten D1/D2 sowie Phantom-Schulter und
  Kriterium „Deckel-Kern“ (schon in 6m zurückgezogen).
- **Kantenbewuchs** ist vom Deckel nicht mehr blockiert. Er wartet nur noch auf die Breitenentscheidung, weil sie die sichtbare
  Wasserlinie um bis zu eine Zelle verschiebt [Ableitung].
- **Der Boden-Trick** bleibt zurückgestellt (6m); er braucht einen eigenen Testgrund.

**Offen, getrennt vom Deckel:** die Glättungsbreite (§2); die Kolkhebung +10 cm in der Kontur, eine reine Diagnose ohne Bildwirkung
(6m §4, unverändert); woher der Schaum in BAKED_SIM kommt (§4).

---

## 2. F1: Welche Glättungsbreite?

### 2.1 Welche Ziele binden

| Ziel | Quelle | Art | Breite 5 | Breite 1 |
|---|---|---|---|---|
| **Kernbett sichtbar_1 ≥ 99 %** (n 250) | 6l §4 | Bild, bindend | **97,6 % ✗** (6 Zellen) | 100 % ✓ |
| **Prüfband sichtbar_5 ≤ 15 %, Toleranz ± 1 pp** (Band 0,25–2 m, mit Lippenschatten) | 6k §3.3 | Bild, bindend | 14,0 % (6k-Basis) ✓ | **nicht gemessen**, erwartet 14,5–15,0 % (sichtbar_2 +0,8 pp) |
| **Kolktiefe sichtbar 0,8–1,35 m an 24/24** | 6l §5 | Bild, bindend | 24/24 ✓ | **22/24**, Abstand unbekannt |
| Bett nass ≥ 97 %, Front 788 m | 6k §2.6, 6m §3 | Gesundheit | ✓ | ✓ |
| sichtbar_2: 0,25–1 m ≤ 30 %, 1–2 m ≤ 5 % | 6g §3 | **ersetzt** (6k Kurzfazit 2, §3.2) | 30,0 / 4,7 | 30,0 / 6,0 – nur melden |

- **Zu den 6,0 %:** Die Schwelle von 2 cm liegt auf der Half-Float-Stufe von R (16g-N2), deshalb hat 6k das Ziel ersetzt. Selbst nach
  altem Maß lägen +1,0 pp genau an der Toleranzgrenze von 6k §3.3.
- **Lippenschatten** (+2,7 pp) hat kein eigenes Ziel; er geht im Prüfband auf.

### 2.2 Abwägung: Bild zuerst, Hydraulik als Grenze

**Mechanismus** [Ableitung aus 6n]: Bei Breite 5 wirkt die Glättung als Tiefpass auf den gezeichneten Spiegel W, auch in nassen Zellen.
Er senkt W an Kuppen (Lippenkronen, Uferkanten) und hebt ihn in Mulden (Kolke). Dazu passen alle Zahlen:
- Kernbett und Ufer werden mit Breite 1 nasser (+2,4 bzw. +1,3 pp).
- Die Kolke werden mit Breite 1 flacher (Maximum 1,34 → 1,31 m, 2 fallen unter 0,8 m).
- „Sim-Boden > 10 cm unter der Kontur in 18–33 % der nassen Zellen“ heißt dasselbe: W gesenkt, G gleich.

**Folge:** Anders als der Deckel ist das **kein Mess-Artefakt**. Der Bake enthält das geglättete W, und BAKED_SIM zeichnet es.
Deshalb ist das Verfehlen des Kernbetts bei 5 im Bild echt.
- Wie stark es auffällt, zeigt erst die Diagnose D (§2.3).
- sichtbar_1 misst mit 1 cm unterhalb der Half-Float-Stufe von 2 cm. Ein Teil der 6 Zellen kann deshalb auch nur ein Film sein.

**Bild** [Bild, links 5 / rechts 1, gebacken, gleiche Kameras]:
- `C2_bett_ufer`: Rechts ist der Grund unter Wasser deutlich gegliedert und die Wasserkante am Fels schärfer; links liegt eine
  gleichmäßig grünliche Fläche darüber.
- `C2_t430_auge`: links mehrere weiße Schaumflecken auf der nahen Stufe, rechts nur wenige kleine. Die übrigen vier Paare sind
  praktisch gleich.
- **Keine treppige Uferlinie und keine Spalte** in dieser Auflösung. Ein Nahbild eines flachen Ufers (6m K1) fehlt; es gehört in den
  Speicherlauf. Standbilder sagen nichts über die Strömung (`pruefung.md`).

**Hydraulik:** Front und Bett sind unverändert. Die Glättung sitzt damit in der Darstellung, nicht im Löser, soweit diese groben Maße
reichen. Den feinen Nachweis liefert G2.

**Urteil:** Breite 1 ist im Bild gleich oder besser. Sie erfüllt das bindende Kernbettziel und zeigt den Spiegel des Lösers ohne
Weichzeichner. Ihr einziges mögliches Minus sind die zwei Kolke. Die entscheidende Frage ist deshalb, um wie viel sie flacher werden.

### 2.3 Prüftor P6N (vorab festgelegt, nur Schwellen aus 6k/6l/6m)

| Nr | Größe (Welt-1-m-Raster, Hindernis-Zellen ausgenommen) | Schwelle | Quelle |
|---|---|---|---|
| G1 | Prüfband sichtbar_5, T6M3A_2 | ≤ 16,0 % (15 % + 1 pp) | 6k §3.3 |
| G2 | W an den 24 tiefsten Kolkpunkten, T6M3A_2 − T6L2B_2 | Median \|ΔW\| ≤ 2 cm **und** kein Kolk \|ΔW\| > 5 cm; die zwei Kolke unter 0,8 m mit Nr. und Wert | 6m §1.2 |
| G3 | Bett `nass_sim` bei Breite 1 (Kontur aus Schritt 2) | ≥ 97 % | 6m §3 |
| D | die 6 Kernbett-Fehlzellen bei 5: W − H, Zone, Neigung, Abstand zur nächsten Lippe, Wert bei 1 | nur melden | 6l §4 |

**Erwartung** [Ableitung]: G1 bei 14,5–15,0 %. G2 mit ΔW von −1 bis −4 cm, die zwei Kolke bei 0,76–0,80 m. D: mindestens 4 der
6 Zellen auf Lippenkronen (Zone 3) mit W − H zwischen −2 und +1 cm. Liegt eine Zelle bei W − H < −2 cm, zeigt Breite 5 dort sichtbar
trockenen Grund im Kernbett; das stärkt die Wahl von Breite 1.

| Ergebnis | Entscheidung |
|---|---|
| **U1:** G1–G3 bestanden | **Breite 1 übernehmen.** Das ist der in 6m E1 vorgesehene „eigene Lauf mit Vergleichsstellen“. Ihn gibt Ferat frei; dann folgt der Speicherlauf T6N1 (§2.5). Das Kolkziel gilt als erfüllt, innerhalb der 5-cm-Toleranz aus 6m; das wird im Vorgang vermerkt |
| **U2:** nur G2 verfehlt (ein Kolk verliert > 5 cm) | **einziger Ersatztest T6N2 mit Breite 2,** Ablauf wie T6M3A, nur im Speicher. Bestanden, wenn Kernbett ≥ 99 % und G1–G3 (G2 gegen Breite 5) gelten; dann wird Breite 2 gespeichert wie in §2.5. Verfehlt → U3 |
| **U3:** G1 oder G3 verfehlt, oder T6N2 verfehlt | **bei 5 bleiben** (gespeichert, kein Eingriff). Das Kernbett gilt als verfehlt, 6 Zellen, mit Lage aus D. Ob Kolktiefe oder Kernbett wichtiger ist, entscheidet Ferat. Keine weiteren Breiten |

### 2.4 Warum kein Reihentest, und warum 2 statt 3

- **Kosten:** Jede Breite kostet Reset, ≈ 25 min bis stabil, Bake, BAKED_SIM neu setzen und Bilder, zusammen ≈ 45 min. Für 1 liegen
  die Zahlen schon vor; es fehlen nur drei Auswertungen.
- **Warum 2:** Das Kernbett erlaubt höchstens 2 Fehlzellen von 250. Linear zwischen Breite 1 (0 Zellen) und 5 (6 Zellen) ergibt das:

  | Breite | Fehlzellen | Kernbett | Ziel |
  |---|---|---|---|
  | 2 | ≈ 1,5 | ≈ 99,4 % | erfüllt |
  | 3 | ≈ 3 | ≈ 98,8 % | **verfehlt** |

  Breite 3 verfehlte also schon nach dieser Schätzung das Ziel, für das ein Zwischenwert überhaupt gebraucht würde [Ableitung, linear;
  die Gewichtung nach Höhenunterschied kann davon abweichen].
- **`smoothing_cutoff`** (500) wird nicht getestet. Was er bedeutet (vielleicht eine Grenze für den Höhenunterschied), ist nicht belegt
  [zu prüfen]. Aufnehmen nur, wenn Rolle 1 diese Bedeutung im Programm findet und U3 eintritt.

### 2.5 Speicherlauf T6N1 (nur nach U1 und Freigabe)

1. **Ausgangsstand-ID** notieren (Breite 5, BAKED_SIM, gespeicherter Bake); den Bake vor dem Überschreiben als Kopie sichern.
2. **Vorher-Bilder:** K1 (flaches Ufer s 506,5 aus 3–4 m, 6m) und die Mündung p2 → C3 als Vergleichsstelle in derselben SWR.
3. **Lauf:** `smoothing_width` 1 setzen und zurücklesen, LIVE_SIM, frisch_reset, bis stabil (zwei Dumps im Abstand von 3 min < 1 pp).
   Dann Bake, `render_state` = BAKED_SIM (Regel 6i), Dump T6N1_2, Bilder der sechs 6n-Kameras plus K1 und Mündung.
4. **Abnahme:** Kernbett ≥ 99 %, G1–G3 erfüllt, Werte je ± 1 pp wie T6M3A_2, Front 788 m. An K1 keine Treppenkante und keine Spalte
   (sonst gilt die Epic-Regel „bei Treppen-Artefakten erhöhen“, 16f → U2). Die Mündung zeigt keine Verschlechterung.
5. **Speichern:** Level, SWR und Bake, mit Speicherbeleg je Paket. **Abbruch:** nach 25 min nicht stabil oder Abnahme gescheitert →
   ohne Speichern neu laden und prüfen, dass Breite 5 und BAKED_SIM wieder stehen.

**Geltungsbereich:** Der Wert gilt nur für die SWR p2. Andere SWR, auch an den Treppen der Sehens-Bäche, erhalten ihn erst mit einem
eigenen Lauf. Er ist keine Exportregel; in `fluss_sim_regeln.json` steht ohnehin keine Glättungsbreite.

---

## 3. F2: Messweg (bestätigt, siehe 6m §3)

- **Ja,** der Boden F kommt aus `DEBUG_RENDER_BOTTOM_CONTOUR`, im nativen Raster, mit eigenem Durchgang und Rückweg ohne Speichern.
- **Keine neue Konturlesung** für die Breitenwahl: 6n bestätigt, dass der Boden nicht an `smoothing_width` hängt. Bei Breite 1 liegt
  R − G im Band bei −3,5 cm. Die Kontur aus Schritt 2 gilt für 5, 2 und 1.

**Neu, weil der Deckel erklärt ist:**
- **`nass_sim` hängt an der Breite.** Die 6m-Definition (|W − G − F| ≤ 5 cm) setzt W − G = F in nassen Zellen voraus; bei 5 stimmt
  das in 18–33 % der nassen Zellen nicht [Ferat]. **Breite 1:** 6m-Definition gilt, G3 prüft sie. **Breite 5:** Bett-Gesundheit wieder
  über G > 1 mm (6l); Saum und `nass_sim` nur im Band auswerten.
- **Jede Zahl für „sichtbar“ gehört zu einer Breite.** Der Vergleich mit 6k/6l-Werten gilt nur bei gleicher Breite; mit jeder Meldung
  wird die Breite angegeben.
- **R − G ist in keinem Ziel mehr enthalten.** Es bleibt nur als Diagnose, und zwar Saumreichweite bzw. Glättung.
- **Unverändert offen** und ohne Einfluss auf F1–F3: wie die Textur auf das 1-m-Raster abgebildet wird (6m Rückfrage), und die
  Kolkhebung an den Texelmitten (6m §4).

---

## 4. F3: Schaum an t430 – erwünscht, kein Verlust

**Feste Entscheidung:** Kein Schaum im Bach außer an Fällen (Ferat 12.10.; 16e, 16f §3) [Projekt].
- **Fall:** Einzelabsturz bzw. Kaskaden-Teilstufe ab `fall_schwelle_m` 1,0 m, keine Rampe und keine Schnelle.
- **Schaumobjekte** gibt es nur an Vorhang-Fällen: `nur_an_vorhang`, Vorhang ab 3 m bzw. bei einer senkrechten Felslippe ab 2 m
  (`fluss_sim_regeln.json`).
- **Die Treppe** der Sehens-Bäche (13f A8: Becken ≤ 3 % und ≥ 3 m; Arten Schnelle, Stufe, Fall) bleibt; daran ändert die Schaumfrage
  nichts (6k §3.3).

**Ist t430 eine Stufe oder ein Fall?** Die Kamera gehört zur Reihe „Talkaskade TK1 t430/t500/t550“, liegt also bei etwa s 430
[Ableitung aus dem Namen]. Ihre genaue Lage und Blickrichtung stehen nicht im Repo. Im Plan liegen dort:

| Lippe | s | Art | Fall | Einstufung nach Regel |
|---|---|---|---|---|
| 7 | 425,73 | stufe | 0,96 m | **Stufe** (< 1,0 m): kein Schaum |
| 8 | 430,42 | kaskade_teil | 1,60 m | **Fall**: Schaum am Fuß erlaubt; `NS_Impact_Small` bei s 431,31 vorgeschlagen, noch nicht gesetzt |
| 9 | 432,81 | schnelle | 0,57 m | **nie Fall**: kein Schaum |

Welche Lippe im Bild schäumt, kann ich aus dem Repo nicht zuordnen.

**Antwort:**
- **An Lippe 7 oder 9** ist weniger Schaum genau das Gewollte.
- **An Lippe 8** darf Schaum am Fuß sein. Er soll aber dort entstehen, wo der Schaumweg ihn erzeugt, und nicht als Nebenwirkung der
  Glättung.
- In keinem Fall ist das ein Grund, bei Breite 5 zu bleiben.

**Steuerung über Material und Schaumweg, nicht über `smoothing_width`:**
- **Material:** `MI_EL_SWR_Klar` hat `Foam Opacity` 0 (Variante F). Das wirkt aber nur im WCBS-Weg. BAKED_SIM zeichnet über Epics
  `SW_Water_Material_River_Niagara` (6i Test 5). Der dort sichtbare Schaum stammt also vom Simulationsschaum dieses Wegs oder vom
  Gischt-Emitter.
- **Hebel:** die Grenzen der Niagara-Kopie (16f §3.4: Speed ab 3,0 m/s, Depth ab 0,15 m, Sekundär-Emitter aus) und die
  Aufprall-Effekte an Fällen ab 1 m (`effekte_vorschlag`).
- **Wie die Glättung den Schaum mindert,** ist offen [zu prüfen]. Für die Entscheidung spielt es keine Rolle.
- **Kein eigener Schritt jetzt.** Das bleibt der offene Punkt aus 6i „Was fehlt“ 4 und wird nach der Breitenentscheidung bearbeitet.

---

## 5. Korrekturen an eigenen Antworten

| Antwort | Aussage | Korrektur |
|---|---|---|
| 6m §1.2, Tabelle | Basis „Kernbett sichtbar_1: Ziel erfüllt“ | **Falsch:** Es war nie gemessen (6l: „wartet auf Beleg“). Gemessen sind 97,6 % bei Breite 5 |
| 6m §1.2 | Kernbett ± 1 pp, Band sichtbar_5 ± 1 pp, Saum nur in trockenen Zellen | Die Glättung wirkt auch auf nasse Zellen [Ferat]; das Kernbett stieg um 2,4 pp |
| 6m §1.2 | Breite 1 macht das Ufer treppig, Spalten möglich | im Bild nicht gesehen; die Ränder sind schärfer. K1 fehlt noch (§2.5) |
| 6m §1.2 | Schaum an den Lippen bleibt | weniger Schaum an t430 |
| 6k §2.6 3a | „verschwindet → Wert bleibt 5, sichtbar ist das Maß“ | Das gilt für den Deckel, nicht für das sichtbare Wasser. Ersetzt durch das Prüftor §2.3 |

---

## Was fehlt bis Witcher 4

Messlatte ist die UE5-Techdemo, belegt nur über Presse und Suchauszüge (wie 6e/6k–6m). Nach Wirkung sortiert:

1. **Klare, scharfe Wasserkante mit sichtbarem Grund:** die Breitenentscheidung (§2). Laut Bild ist das der größte Gewinn, der
   jetzt ohne neues Asset erreichbar ist.
2. **Kantenbewuchs bis an die Wasserlinie** (Kantengras, Moos, Farne): Er ist nicht mehr blockiert und wird gesetzt, sobald die Breite
   gespeichert ist. Er verdeckt Filme von 1–5 cm und die Ränder des Lippenschattens.
3. **Weißwasser nur an Fällen, auch in BAKED_SIM:** Niagara-Grenzen bzw. Gischt-Emitter (16f §3.4, 6i) und Aufprall-Effekte an den
   Fällen ab 1 m (Vorschlag im Bettplan, noch nicht gesetzt).
4. **Nasse Steine an der sichtbaren Linie:** `M_EL_Mountain_NL` (**anzulegen**) und die MS2-MIs; Versatz +20 cm passt zu T-b1.
5. **BAKED_SIM spielfest:** gepackter Build (T-a3), Kosten an p2 (T-a1/T-a2).
6. **Tiefe, dunkle Kolke:** Im Bild sind sie erfüllt. Nach §2.3 dürfen sie höchstens 5 cm verlieren. Die +10 cm in der Kontur bleiben
   Diagnose.
7. **Verlässliche Messwege:** Kolkvergleich an den Texelmitten, Pixelmessung KF1–KF7 (6j §2). Rinnenköpfe und Licht im Einschnitt
   (6e/6f/6j §3).

## Quellen

Keine Websuche in dieser Antwort. Epic-Angaben aus früheren Antworten: 16f („Smoothing Width/Cutoff glättet die Oberflächen-Verschiebung
an harten Kanten; bei Treppen-Artefakten erhöhen“ [Epic lokal]), 6k §2.2 (`SmoothingWidth` int, `SmoothingCutoff` float [Suchauszug]),
6i (Materialpfad in BAKED_SIM [Ferat]). Im Repo: 6n sowie die oben genannten Dateien mit Revision.

**Nicht belegt:** ob die Glättung in den Zustand des nächsten Schritts schreibt (G2 prüft es grob), was `smoothing_cutoff` bedeutet,
woher der Schaum in BAKED_SIM kommt, wo genau die Kamera t430 steht.

## Rückfragen

Keine, die den nächsten Schritt ändert. Mit P6N bitte die Nummern der beiden Kolke unter 0,8 m und ihre Werte bei 5 und 1 melden.
