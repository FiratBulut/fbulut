# Antwort 16h Nachtrag 6o – G2 war falsch gestellt: Tor auf sichtbare Kolktiefe umgestellt, Breite 1 in den Speicherlauf T6N1

Gelesen: recherche/auftraege/16h-nachtrag6o-t6n2-u3-g2-tor.md @ e3f2f5df927c1b03bd593f0702b09d28dd448e7f (Commit b755027)

Stand 18.10.2026. Gesamtauftrag 16h (Erlenbach p2, Talkaskade s 389–580). Bearbeiter: Cloud-Recherche. Bereich: Prüftor P6N, Glättungsbreite
der SWR p2. Wasser bleibt lokal unverändert; gespeichert ist weiter Breite 5 mit BAKED_SIM.

**Bezug, ebenfalls gelesen (alle Commit b755027):**
- Rohdaten 6o: `p6n_bericht.md` @ bff1a600871b4748985569c23423281092609219, `p6n_ausgabe.txt` @ adf1b953d964d0386ee5e9645f64269e38e6666d,
  `p6n_t6n2_ausgabe.txt` @ 21704edd782ad9587b0c6c51be491751971a02e6, `nachbau_ausgabe.txt` @ d941074b4f95a5f4b77dd9a051202ecc63fab366 (alle ganz)
- `recherche/antworten/16h-nachtrag6n-schritt3a-verschwindet.md` @ 845ead7c7fb325736d5fc3464c5b3e3164baf826 (ganz)
- `recherche/antworten/16h-nachtrag6m-schritt2-band-b.md` @ e077fa0f455bf50993093c76d54e98c10d21bd60 (§1–§4), `recherche/antworten/16h-nachtrag6l-boden-schritt1.md`
  @ 68e2f510532a8edb5b921e981f02359c76a30fea (§4, §5), `recherche/antworten/16h-nachtrag6f-bettplan-eingebaut.md` @ cf8e3b00170587949f39be12ddc3ca4f14d48b29 (Kolkziel)
- `recherche/antworten/p2_bett/bettplan_p2.json` @ 0013ef4a1922330462308bc7dbad8729ae6a1ef3 (`becken[].spiegel_m`, `kolk`), `recherche/README.md`
  @ 778d8a7b8ac17fcaceb262ee8b63e46898ff7051 (Reihenfolge Wasser/Darstellung vor Ufer)
- Bild `recherche/bilder/swr_p2/t6m3a_glaettung5_gegen_1.jpg` @ 283d44a6cfcef7143d132014c1fa4656f4abec6e (selbst angesehen, 6 Paare, links 5, rechts 1)

**Kennzeichnung:** [Ferat] Messung bzw. Rolle-1-Bericht aus 6o · [Rechnung] von mir aus Bericht-Tabelle §2 G2 und Bettplan gerechnet ·
[Bild] selbst gesehen · [Ableitung] geschlossen, nicht belegt · [zu prüfen] offen.

## Kurzfazit

1. **Trägt der Nachbau die Folgerung? – beantwortet: ja, für den Löser; nein, für „G2 misst nur ein Artefakt“.** Die Breite ändert nur die
   Zeichnung, der Löser ist bei 1, 2 und 5 derselbe. Aber die Zeichnung ist das Produkt: BAKED_SIM zeigt das geglättete W. Die tieferen Kolke
   bei 5 sieht der Spieler, die trockenen Lippenkronen bei 5 auch (§1).
2. **G2 aus 6n war falsch gestellt – eigener Fehler, korrigiert.** Wir haben die Rückwirkungsprüfung aus 6m (Löser gegen Löser) mit dem
   Kolkschutz vermischt und dafür die geglättete Breite-5-Ausgabe als Bezug genommen (§2.1).
3. **Neues Tor G2′ – festgelegt:** bindend die sichtbare Kolktiefe W − H auf der gezeichneten Ausgabe gegen 0,8–1,35 m (6l §5), dazu
   W − G − F als Gültigkeitsbedingung und W − Planspiegel als Diagnose (§2.2). **T6M3A_2 (Breite 1) besteht G2′ [Rechnung]; damit gilt nach
   6n §2.3 U1.**
4. **23/24 mit Nr. 3 bei 0,68 m – entschieden: besteht, aber nicht über eine Zähltoleranz.** Bei Nr. 3 steht das Wasser auf Planspiegel
   (−1,2 cm); es fehlt Gelände, nicht Wasser. Die Ausnahme ist vor jedem Lauf aus Plan und Gelände bestimmbar (Nr. 3 und 30). „≥ 22/24, keiner
   unter 0,6 m“ lehne ich ab (§2.3).
5. **F2 Gegenüberstellung für Ferat – entfällt als Entscheidungsfrage,** weil G2 ersetzt ist. Für seine Speicherfreigabe steht ein kurzer
   Text in §3.
6. **F3 Breite 1 oder 2 – beantwortet: Breite 1.** Die Kolke unterscheiden 1 und 2 nicht, und Breite 2 glättet Uferkanten nach der
   nachgebauten Formel praktisch nicht. Protokoll-Delta zu 6n §2.5 in §4.
7. **Neuer Befund, offen:** Kolk 36 steht im Löser 35 cm unter Planspiegel, bei jeder Breite. Breite 5 malt das zu (§1.3).

**Nächste Handlung (genau eine, im Editor, nur im Speicher bis zur Freigabe, ≈ 60 min): Speicherlauf T6N1 mit Breite 1 nach §4,
ausgewertet mit G2′; gespeichert wird erst nach Ferats Freigabe.**
- **Erfolgskriterium:** Abnahme §4.3 vollständig mit Dump-ID, Werten und Bildern gemeldet; Ferats Entscheidung festgehalten; bei Freigabe
  Speicherbeleg je Paket (Level, SWR, Bake).
- **Abbruch:** nach 25 min nicht stabil; G2′b an einem Kolk verletzt; BAKED_SIM nach dem Bake nicht zurückgelesen; Ferat lehnt ab. Dann
  Level ohne Speichern neu laden und Breite 5 + BAKED_SIM bestätigen.

---

## 1. Der Nachbau: was er belegt und was nicht

### 1.1 Was er belegt

- **Der Löser hängt nicht an der Breite.** Bei Breite 1 passt die Ausgabe an allen 24 Kolken zum Löser (W − G − F −0,1 … −3,9 cm). Der
  Nachbau erzeugt aus diesem Zustand den Breite-5-Dump eines **anderen** Laufs: |dR| Median 0,25 cm, p90 4 cm, dieselben 6 Fehlzellen [Ferat].
- **Die Vorhersage für Breite 2 traf ein,** vor dem Lauf festgelegt: G1, G3, Kernbett bestanden, G2 verfehlt mit max 48 cm (gemessen 48 cm,
  10 statt 9 Kolke) [Ferat]. Das ist der stärkste Beleg, denn es ist eine Vorhersage und keine Anpassung.
- **Nachbau Breite 1 und Breite 2 sind an den Kolken gleich** (beide 23/24, Nr. 3 0,72 m, dieselben 9 Kolke über 5 cm) [Ferat, Nachbau-Ausgabe].
  Unterschiede zwischen den echten Läufen T6M3A_2 und T6N2_2 an den Kolken sind daher Laufstreuung, nicht Breite.

### 1.2 Was daraus nicht folgt

„Gezeichnet, nicht gerechnet“ stimmt. „Also misst G2 ein Artefakt, das nicht zählt“ stimmt nicht.
- Der Bake enthält das geglättete W, BAKED_SIM zeichnet es (6n §2.2). Die Kolktiefe im Bild ist W − H der Ausgabe, nicht G + F − H des Lösers.
- Nach README gilt „Wasserverhalten/Darstellung vor abhängiger Uferanpassung“: Bewertet wird die gezeichnete Oberfläche.
- Dieselbe Regel gilt in beide Richtungen. Bei 5 sind die tieferen Kolke **und** die trockenen Lippenkronen im Bild echt. An 4 der 6
  Kernbett-Fehlzellen sieht man bei 5 trockenen Grund (W − H −3,7 … −13,7 cm), obwohl dort 24–50 cm Wasser fließen [Ferat].

### 1.3 Ein Mechanismus, zwei Wirkungen [Rechnung aus Bericht §2 und Bettplan]

| Stelle | Lippe (Art, Fall) | Krone darüber, W − H bei 5 / 1 | Kolk darunter, W − G − F bei 5 | Kolk W − H bei 5 / 1 |
|---|---|---|---|---|
| s 481,9 / Kolk 22 | 22 (Stufe, 1,55 m) | −13,7 / +24,3 cm | +42,1 cm | 1,23 / 0,91 m |
| s 529,7 / Kolk 36 | 36 (Stufe, 1,53 m) | −0,4 / +17,6 cm | +53,1 cm | 1,28 / 0,78 m |

- Die zwei größten Kolkhebungen liegen genau unter zwei der Kernbett-Fehlzellen. Die Glättung zieht an der Stufe den oberen Spiegel nach
  unten über die Krone und hebt den Spiegel im Kolk darunter. Bei 5 wird die Stufe also als Rampe gezeichnet. An Kolk 36 erscheint der Fall
  rund 0,5 m niedriger (Oberbecken-Plan 56,99 m, Kolk bei 1 55,11 m, bei 5 55,61 m) [Ableitung].
- Das trifft die Treppe der Sehens-Bäche (13f A8), nicht nur die Kolke. Ein Nahbild davon fehlt (§1.4).
- **Planspiegel gegen Ausgabe** (`becken[].spiegel_m`, 24 Kolke): Median W − Plan bei 1 **+5,4 cm**, bei 5 **+13,9 cm**. Der „Überstand
  13–16 cm“ aus T-b1, auf den 6l §5 die Obergrenze 1,35 m stützt, war bei Breite 5 gemessen und enthält also Glättung.
- **Kolk 36 ist ein echter Wasserbefund:** Der Löser hält ihn bei 1 und bei 5 auf ≈ 55,1 m, 35 cm unter Plan (55,46 m). Breite 5 zeigt
  1,28 m nur, weil sie das überdeckt. Ursache offen [zu prüfen]: Lippe 37 im Gelände tiefer als geplant, oder der Kolkpunkt liegt im
  schnellen Strahl direkt am Fuß der Stufe.

### 1.4 Noch nicht geprüft

- **Die sichtbare Kolktiefe, wie der Spieler sie sieht.** Keine der 6 Kameras aus 6n zeigt einen Kolk an einer Stufe aus der Nähe. [Bild] In
  `C2_m_talkaskade`, `C2_t430_schraeg` und `C2_t500_auge` sind die Becken links und rechts praktisch gleich. Ob Kolk 36 bei 1 sichtbar flacher
  oder die Stufe sichtbar höher wirkt, ist offen. Die T6N2-Bilder liegen nicht im Repo; ich habe sie nicht gesehen.
- Ob die gerenderte Fläche am Texel W des Bakes trifft (Netzauflösung, Interpolation im Material). Die Dumps lesen den Bake, nicht den
  Bildschirm [zu prüfen].
- Kollider fehlen im Nachbau; der Breite-5-Vergleich stammt aus einem anderen Lauf (Laufstreuung an Kolken bis 4 cm, Nr. 3: 0,68 gegen 0,72 m).
- Strömung und zeitliche Treppenartefakte sind aus Standbildern nicht ableitbar (`pruefung.md`).

---

## 2. Das Tor G2′

### 2.1 Was an G2 falsch war (Korrektur 6n §2.3)

- In 6m §1.2 sollte ΔW an den Kolken nur eine Frage beantworten: Wirkt die Glättung in den Löser zurück? Dafür ist ein Vergleich Löser gegen
  Löser richtig.
- 6n hat daraus zusätzlich einen Kolkschutz gemacht („höchstens 5 cm verlieren“) und dabei angenommen, die Breite-5-Ausgabe sei an Kolken
  gleich dem Löser. Das war falsch: An 13 der 24 Kolke liegt W − G − F bei 5 über 5 cm [Rechnung].
- G2 hat deshalb die Löserebene bei 1 gegen die gemalte Ebene bei 5 verglichen. Die Rückwirkungsfrage beantwortet nun der Nachbau (§1.1);
  den Kolkschutz muss ein Bildmaß tragen.
- Auch 6l §5 „Kolkziel erfüllt 24/24“ ist zu relativieren: Nr. 3 lag bei 5 genau auf 0,80 m, davon +16,7 cm gemalt.

### 2.2 Festlegung (gilt für alle Breiten, vor T6N1)

| Nr | Größe (24 Kolkpunkte wie P6N, Hindernis-Zellen ausgenommen) | Schwelle | Art |
|---|---|---|---|
| **G2′a** | sichtbare Kolktiefe W − H auf dem Dump des Bakes, den BAKED_SIM zeichnet | je Kolk 0,8 m − s bis 1,35 m + s; s = Half-Float-Stufe an der Stelle (1/2/4 cm, Bericht §1). Ausnahme siehe §2.3 | **bindend** |
| **G2′b** | W − G − F, also Ausgabe gegen Löser | \|·\| ≤ 5 cm an allen 24 | Gültigkeit: verletzt bei Breite 1 oder 2 → Nachbau-Annahme falsch, Abbruch |
| **G2′c** | W − `spiegel_m` je Kolk | nur melden; Werte unter −20 cm einzeln nennen | Diagnose (Kolk 36) |

Bei Breite 5 verfehlt G2′b per Bauart und wird nur gemeldet. Die Toleranz s stammt aus der Auflösung, die 6n schon für ΔW anerkannt hat;
sie ist kein neuer Spielraum.

### 2.3 Nr. 3 bei 0,68 m und die Ausnahme

- **Die Lage:** Planspiegel 97,762 m, Plantiefe 0,84 m (unterster Planwert). H an der tiefsten Zelle liegt 14,8 cm über dem Planboden. Damit
  ist Planspiegel − H = **0,69 m**. Breite 1 zeigt W = 97,75 m, also 1,2 cm unter Plan [Rechnung]. Das Wasser tut, was der Plan verlangt; die
  Tiefe fehlt im Gelände bzw. im 1-m-Raster, das den tiefsten Planpunkt eines 1,7 × 2,2 m kleinen Kolks verfehlt (6l §5).
- **Regel, aus 6l §5 abgeleitet:** 6l setzt die sichtbare Tiefe als Plantiefe plus Überstand. Liegt schon der Planspiegel weniger als 0,8 m
  über H, kann kein richtiges Wasser 0,8 m erreichen. Dort gilt W ≥ `spiegel_m` − s, und der Kolk wird als **Geländebefund** geführt.
  - Die Liste hängt nur an Plan und Gelände und steht vor jedem Lauf fest: **Nr. 3 (0,69 m) und Nr. 30 (0,75 m)** [Rechnung]. Nr. 30 erreicht
    bei 1 ohnehin 0,90 m.
- **Warum nicht „≥ 22/24, keiner unter 0,6 m“:** Dafür gibt es in 6k/6l keine Quelle; 6l verlangt alle 24. Die Zählregel würde zudem einen
  Kolk durchlassen, dessen Wasser 35 cm unter Plan steht, ohne dass es auffällt. Bei Nr. 36 ist das bei Breite 1 der Fall (0,78 m).
- **Ergebnis T6M3A_2 (Breite 1):** 22 Kolke im Ziel; Nr. 36 mit 0,783 m innerhalb s = 2 cm, **knapp**; Nr. 3 Geländebefund. G2′a bestanden,
  G2′b bestanden (−0,1 … −3,9 cm). **Mit G1 10,70 %, G3 99,84 % und Kernbett 100 % gilt U1.**
- **T6N2_2 (Breite 2):** 23/24, Nr. 3 wie oben. Nr. 36 ≈ 0,80 m, falls das Maximum von 48 cm dort liegt [Ableitung]. Ebenfalls bestanden.

---

## 3. Für Ferat: Was ändert die Breite? (Grundlage: die sechs Bildpaare aus 6n §2.2)

Die Simulation rechnet das Wasser bei jeder Einstellung gleich. Die Einstellung entscheidet nur, wie weich die Oberfläche gezeichnet wird.
- **Was du siehst:** In vier der sechs Ansichten keinen Unterschied. Am nahen Ufer (`C2_bett_ufer`) sieht man mit Breite 1 den Grund unter
  Wasser deutlicher, und die Kante am Fels ist schärfer. An der nahen Stufe (`C2_t430_auge`) gibt es weniger weiße Flecken.
- **Was sich ändert:** Heute werden die Stufen weich gezeichnet. Einige Steinkanten oben an der Stufe sehen dadurch trocken aus, und das
  Becken darunter wirkt bis zu einem halben Meter voller. Mit Breite 1 sind die Kanten nass und die Stufen voll hoch. Ein Becken (Nr. 36)
  wirkt dann flacher, weil dort tatsächlich weniger Wasser steht. Das wird separat geprüft.
- **Was es kostet:** Kein neues Asset, ein Lauf von etwa einer Stunde. Gespeichert wird erst, wenn du die Vorher-/Nachher-Bilder gesehen
  und zugestimmt hast, auch die neuen Nahbilder von zwei Becken.

---

## 4. F3: Breite 1, und das Protokoll T6N1

### 4.1 Warum 1 und nicht 2

| Merkmal | Breite 1 (T6M3A_2) | Breite 2 (T6N2_2) | Urteil |
|---|---|---|---|
| G1 Band sichtbar_5 | 10,70 % | 10,70 % | gleich |
| Kernbett sichtbar_1 | 100 % | 100 % | gleich |
| G3 Bett `nass_sim` | 99,84 % | 99,36 % | 1 besser, beide im Ziel |
| Band-Median Sim-Boden − Gelände | −3,5 cm | −14,1 cm | 1 näher am Gelände (weniger Saum) |
| Kolke G2′a | 22 + Nr. 36 knapp + Nr. 3 Gelände | 23 + Nr. 3 Gelände | gleich innerhalb Laufstreuung (Nachbau 1 = 2, §1.1) |
| Nachbau gegen echten Dump | \|dR\| 0 / 4 cm, \|dG\| 0 / 0 | nicht separat geprüft | 1 ist belegt „Ausgabe = Löser“ |

- **Uferkanten:** Nach der von Rolle 1 nachgebauten Formel wirken bei 2 nur die 4 Diagonalen mit Gewicht 0,207 · smoothstep(0, 500 cm, |ΔH|).
  Bei einer Uferstufe von einer Zelle (|ΔH| ≈ 37 cm) sind das ≈ 0,3 %, erst an Fällen um 1,5 m ≈ 4,5 % [Rechnung nach Bericht §3]. Breite 2
  schützt also nicht gegen treppige Ufer. Zeigt K1 Treppen, hilft 2 nicht; dann ist ein anderer Hebel nötig (§4.3).
- **Nr. 3 bei 0,68 m** ist bei 1 und 2 gleich (Geländebefund). Bei Nr. 36 liegen 0,78 und ≈ 0,80 m eine Half-Float-Stufe auseinander, in
  zwei verschiedenen Läufen.
- **Folge:** Nach 6n §2.3 führt U1 direkt zu Breite 1. Breite 2 bringt keinen messbaren Vorteil und hat das schlechtere Bett.

### 4.2 Delta zu 6n §2.5

| Punkt 6n §2.5 | Neu |
|---|---|
| 1 Ausgangsstand-ID, Bake-Kopie | unverändert |
| 2 Vorher-Bilder K1, Mündung | **plus K4:** Kolk 36 mit Lippe 36 (s 529–532), schräg von unten, 4–6 m; **plus K5:** Kolk 3 (s 402,8), gleiche Art. Kamera und Licht festhalten |
| 3 Lauf, Bake | unverändert; danach `render_state` = BAKED_SIM setzen **und zurücklesen**, erst dann Dump T6N1_2 und Bilder (sechs 6n-Kameras, K1, K4, K5, Mündung) |
| 4 Abnahme „G1–G3“ | **G1, G2′a/b (+c melden), G3**, Kernbett ≥ 99 %, Front 788 m; je ± 1 pp wie T6M3A_2, Kolke je ± 4 cm (Laufstreuung) |
| 4 K1 „sonst → U2“ | Treppe oder Spalte an K1 → **nicht speichern**, Bild melden. Kein automatischer Wechsel auf 2 (§4.1) |
| 5 Speichern | **erst nach Ferats Freigabe** anhand der Bildpaare und der Werte; bis dahin bleibt alles nur im Speicher |
| Auswertung | `t6n_p6n.py` um G2′ ergänzen. **Kontrolle vor dem Lauf** auf T6M3A_2: Nr. 3 W − Plan −1,2 cm, Nr. 36 0,783 m und −35,2 cm, Ausnahmeliste {3, 30} |

### 4.3 Entscheidung je Ergebnis (vorab)

| Ergebnis | Entscheidung |
|---|---|
| Abnahme bestanden, Ferat stimmt zu | speichern mit Speicherbeleg; Breite 1 gilt für die SWR p2; Kantenbewuchs ist frei |
| Nur Nr. 36 unter 0,78 m | nicht speichern; Kolk 36 (Lippe 37, Strahl) zuerst klären. Breite 5 malt den Mangel nur zu |
| K1 treppig oder Spalte | nicht speichern; Rolle 1 prüft `smoothing_cutoff` im Nachbau, bevor ein Lauf startet |
| G2′b verletzt | Abbruch; die Nachbau-Folgerung gilt nicht, und Rolle 1 meldet den Befund |
| Ferat lehnt ab | ohne Speichern neu laden; Breite 5 bleibt mit vermerktem Kernbett-Mangel |

---

## 5. Korrekturen an eigenen Antworten

| Antwort | Aussage | Korrektur |
|---|---|---|
| 6n §2.3 G2 | ΔW gegen Breite 5 schützt die Kolke | misst die Glättung; ersetzt durch G2′ (§2.2) |
| 6n §2.2 | „Ihr einziges mögliches Minus sind die zwei Kolke“ | Nr. 3 ist ein Geländebefund, Nr. 36 ein Löserbefund; beides bei jeder Breite |
| 6l §5 | Kolkziel 24/24 erfüllt, Überstand 13–16 cm | bei Breite 5 gemessen, teils gemalt (Nr. 3 +16,7 cm, Median W − Plan +13,9 statt +5,4 cm) |

## Was fehlt bis Witcher 4

Messlatte ist die UE5-Techdemo, belegt nur über Presse und Suchauszüge (wie 6e/6k–6n). Nach Wirkung sortiert:

1. **Klare, scharfe Wasserkante, nasse Lippenkronen, volle Stufenhöhe:** T6N1 mit Breite 1 (§4). Der größte Gewinn ohne neues Asset.
2. **Kolke halten ihren Planspiegel:** Kolk 36 steht 35 cm zu tief; in sieben Kolken liegt H 17–45 cm über dem Planboden (Nr. 6, 25, 27, 29,
   30, 38, 42) [Rechnung]. Erst Wasser, dann Bettform prüfen.
3. **Kantenbewuchs bis an die Wasserlinie:** frei, sobald Breite 1 gespeichert ist.
4. **Weißwasser nur an Fällen, auch in BAKED_SIM:** Niagara-Grenzen, Aufprall-Effekte an Fällen ab 1 m (6n §4, unverändert).
5. **Nasse Steine an der sichtbaren Linie:** `M_EL_Mountain_NL` (**anzulegen**) und die MS2-MIs.
6. **BAKED_SIM spielfest:** gepackter Build (T-a3), Kosten an p2 (T-a1/T-a2).
7. **Verlässliche Messwege:** gerenderte Fläche gegen Bake-W am Bildschirm, Pixelmessung KF1–KF7 (6j §2).

## Quellen

Keine Websuche. Zahlen aus den 6o-Rohdaten [Ferat]. Eigene Rechnung: Bericht-Tabelle §2 G2 (H, W bei 5/1, W − G − F) gegen
`bettplan_p2.json` `becken[].spiegel_m` und `kolk.tiefe_m`; Gewichte aus der Formel in Bericht §3.

**Nicht belegt:** Nr. 36 bei Breite 2 (nur Summenwerte gemeldet); wie der Kolk 36 im Bild wirkt; warum Kolk 36 tief steht; ob die
Darstellung zwischen den Texeln weiter glättet.

## Rückfragen

Keine, die T6N1 ändert. Mit T6N1 bitte die Spalte W − `spiegel_m` für alle 24 Kolke mitliefern.
