# Prüftor P6N (Cloud 16h-N6n §2.3): Ergebnis U2 – Bericht Rolle 1

Stand 18.10.2026, Rolle 1 (Technik Shallow Water), offline, ohne Editor. Werkzeug `scripts/swr/t6n_p6n.py` (Ausgabe `p6n_ausgabe.txt`, Daten
`p6n_ergebnis.json` mit SHA-256 aller Eingaben). Antwort 6n gelesen @ Commit 73b2ac5.

## Kurzfazit

- **Dump vorhanden:** `T6M3A_2` (Breite 1, 18:14, 3a-Lauf ab 17:57) und `T6L2B_2` (Breite 5, 16:50, Schritt 2) liegen als Datei vor. P6N läuft
  deshalb offline; der Abbruch-Weg aus 6n §2.5 entfällt.
- **Ergebnis U2** (vorab festgelegt: nur G2 verfehlt):

  | Tor | Wert (Hindernis-Zellen ausgenommen) | Schwelle | Urteil |
  |---|---|---|---|
  | G1 Prüfband sichtbar_5, Breite 1 | **10,70 %** (n 430); mit Hindernis-Zellen 14,14 % (n 665) | ≤ 16,0 % | bestanden |
  | G2 W an 24 Kolkpunkten, 1 − 5 | Median \|ΔW\| **4,0 cm**, Maximum **50 cm** (Nr. 36), 10 Kolke > 5 cm | ≤ 2 cm, keiner > 5 cm | **verfehlt** |
  | G3 Bett `nass_sim`, Breite 1 | **99,84 %** (n 625) | ≥ 97 % | bestanden |

  Kernbett sichtbar_1 (n 250): Breite 5 97,6 % (6 Fehlzellen), Breite 1 **100 %**.
- **Formal nächster Schritt (6n §2.3 U2):** einziger Ersatztest **T6N2 mit Breite 2**, nur im Speicher. Die Kette ist vorbereitet:
  `live/claude_code/swr/_t6n2_kette.sh`, Trockenlauf 8/8.
- **Aber (Diagnose, abgeleitet, an die Cloud):**
  - G2 misst hier nicht den Löser, sondern die Darstellungsglättung bei Breite 5. Bei Breite 1 passt die Ausgabe an allen 24 Kolkpunkten zum
    Löser (W − G − F = −0,1 … −3,9 cm). Bei Breite 5 liegt W dort bis **+53 cm** über Kontur + Tiefe.
  - Ein Offline-Nachbau der Glättung (Programm aus dem Niagara-Asset) erzeugt aus dem Breite-1-Löserzustand den echten Breite-5-Dump nach
    (|dR| Median 0,25 cm, p90 4 cm = eine Half-Float-Stufe). Die Breite ändert also nur die Zeichnung, messbar wirkt sie nicht in den Löser zurück.
  - **Vorhersage für T6N2 aus dem Nachbau:** G1 und G3 bestanden, Kernbett 100 %, **G2 verfehlt wie bei Breite 1** (9 Kolke > 5 cm, max 48 cm)
    → T6N2 verfehlt → **U3**.
  - Der 45-min-Lauf würde damit voraussichtlich nur U3 bestätigen.
- **Empfehlung:** Vor T6N2 die Diagnose an die Cloud (6o): Ist G2 das richtige Tor, wenn ΔW die Breite-5-Glättung misst? Zu entscheiden:
  Kolktiefe (sichtbar bei 5 durch die Glättung bis 50 cm höher gezeichnet) oder Kernbett/scharfe Kante (Breite 1). 6n §2.3 U3 legt diese
  Abwägung ohnehin zu Ferat.
- **Speicherkette:** nicht vorbereitet, denn der Auftrag sah sie nur für U1 oder einen fehlenden Dump vor. Ich kann sie für jede freigegebene
  Breite vorbereiten.

## 1. Messweg (6m §3, 6n §3)

- **Raster:**
  - Kontur F aus Schritt 2 (`T6L2_RT_DBG1`, Debug-Render-Target, A + mitte_z) und die Dumps liegen im selben nativen Sim-Raster: 319 × 2016,
    Meta identisch (geprüft).
  - Welt-1-m-Raster = Fenster des Prüfbands (174 × 69), Felder aus `befund_T6JB0_2.npz` (eingefroren, SHA in `p6n_ergebnis.json`).
  - Texel → 1 m: **nächstes Texel zur Zellmitte** (wie `t6j_messen.proben`), für W = R + mitte_z, G und F.
- **Definitionen:**
  - `sichtbar_x` (Bild) = G > 0,1 cm ∧ W − H > x, mit H = `hoehe.f32`.
  - `nass_sim` = G > 0,1 cm ∧ |W − G − F| ≤ 5 cm.
  - Kontrollfall KB1–KB6 aus 6m §3 bestanden: nass_sim 3, Saum 2, trocken 1; sichtbar_5 Bild 4, Sim 3; Kolk 1,10 m.
- **Masken:**
  - Band = Maske 2/3 (`talkaskade_C2_lippenschatten.u8`, Band 0,25–2 m mit Lippenschatten), Bett = Maske 1.
  - Hindernis-Zellen = Grundriss des WH-Akteurs (befund, Stand 14.10.).
  - Mit Hindernis-Zellen gibt G1 bei Breite 5 **13,98 %**; das reproduziert die 6k-Basis von 14,0 %.
- **Kolkpunkt:** die Zelle mit dem kleinsten H je Kolk (24 Hauptbecken, befund `kolk`). Mit und ohne Hindernis-Zellen sind es dieselben Zellen
  und dieselben Werte.
- **Projektprobe F (6m §3):** Flaches Kernbett (Neigung < 0,2, n 133): Median |F − H| 1,73 cm, 94,0 % in ± 10 cm → **bestanden**. Ein
  Halbzellen-Versatz F/H liegt nicht vor (bestes RMS bei 0/0). F ist damit für G3 verwendbar.
- **Auflösung:** R ist Half-Float relativ zu mitte_z (34,03 m). Je nach Höhe ist die Stufe unterschiedlich groß:

  | Lage | relative Höhe | Stufe |
  |---|---|---|
  | Kolke oberhalb ≈ 75 m Weltlage | über 41 m | 4 cm |
  | Kolke zwischen ≈ 54,5 und 75 m | 20,5–41 m | 2 cm |
  | Kolke darunter | unter 20,5 m | 1 cm |

  Die ΔW sind deshalb Vielfache von 1, 2 oder 4 cm. Die Schwelle „Median ≤ 2 cm“ liegt für die oberen Kolke unter der Auflösung.

## 2. Ergebnisse

### G1 Prüfband sichtbar_5

| Dump (Breite) | ohne Hindernis-Zellen (n 430) | mit (n 665) | Sim-Definition (nass_sim ∧ W − H > 5 cm), ohne |
|---|---|---|---|
| T6M3A_2 (1) | **10,70 %** | 14,14 % | 10,23 % |
| T6L2B_2 (5) | 10,47 % | 13,98 % | 6,51 % |

### G2 Kolke (Wasserspiegel W an der tiefsten Zelle; Tiefe = W − H; „W − G − F“ = 0 heißt, die Ausgabe passt zum Löser)

| Nr | s | H | W bei 5 | W bei 1 | ΔW cm | Tiefe 5 | Tiefe 1 | W−G−F bei 5 | W−G−F bei 1 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 396,9 | 97,83 | 98,83 | 98,83 | 0 | 1,00 | 1,00 | −1,6 | −1,5 |
| **3** | 402,8 | 97,07 | 97,87 | 97,75 | −12 | 0,80 | **0,68** | +16,7 | −2,9 |
| 5 | 410,9 | 93,95 | 94,99 | 94,99 | 0 | 1,04 | 1,04 | −2,9 | −3,0 |
| 6 | 420,7 | 92,31 | 93,47 | 93,27 | −20 | 1,15 | 0,95 | +24,8 | −3,9 |
| 7 | 427,0 | 91,40 | 92,43 | 92,43 | 0 | 1,03 | 1,03 | +0,1 | −0,1 |
| 12 | 443,2 | 86,23 | 87,55 | 87,35 | −20 | 1,31 | 1,11 | +30,8 | −2,2 |
| 15 | 452,5 | 81,89 | 83,07 | 82,95 | −12 | 1,18 | 1,06 | +17,6 | −1,9 |
| 17 | 459,6 | 78,51 | 79,71 | 79,71 | 0 | 1,20 | 1,20 | −3,0 | −3,2 |
| 18 | 467,4 | 77,60 | 78,59 | 78,59 | 0 | 0,99 | 0,99 | −1,5 | −2,1 |
| 21 | 477,8 | 74,07 | 75,07 | 74,99 | −8 | 1,00 | 0,92 | +11,4 | −2,7 |
| 22 | 483,7 | 72,44 | 73,67 | 73,35 | −32 | 1,23 | 0,91 | +42,1 | −1,6 |
| 25 | 492,1 | 68,96 | 70,07 | 69,91 | −16 | 1,10 | 0,94 | +6,1 | −0,1 |
| 27 | 498,4 | 66,64 | 67,63 | 67,59 | −4 | 0,99 | 0,95 | +4,0 | −1,2 |
| 29 | 505,1 | 62,79 | 63,83 | 63,83 | 0 | 1,04 | 1,04 | −0,1 | −1,8 |
| 30 | 512,0 | 61,53 | 62,43 | 62,43 | 0 | 0,90 | 0,90 | −0,2 | −0,3 |
| 33 | 519,5 | 58,73 | 59,59 | 59,55 | −4 | 0,86 | 0,82 | +4,4 | −1,4 |
| 35 | 526,4 | 55,98 | 57,11 | 57,03 | −8 | 1,13 | 1,05 | +13,6 | −1,7 |
| **36** | 531,4 | 54,33 | 55,61 | 55,11 | **−50** | 1,28 | **0,78** | **+53,1** | −1,4 |
| 38 | 538,4 | 52,18 | 53,26 | 53,23 | −3 | 1,08 | 1,05 | +7,1 | −0,5 |
| 40 | 545,5 | 49,85 | 51,06 | 50,96 | −10 | 1,20 | 1,10 | +14,1 | −0,9 |
| 41 | 549,8 | 48,71 | 50,05 | 50,02 | −3 | 1,34 | 1,31 | +8,5 | −0,3 |
| 42 | 555,8 | 47,73 | 48,71 | 48,72 | +1 | 0,98 | 0,99 | +0,1 | −0,1 |
| 44 | 562,9 | 45,27 | 46,34 | 46,30 | −4 | 1,07 | 1,03 | +6,5 | −0,6 |
| 45 | 573,1 | 43,96 | 45,19 | 45,19 | 0 | 1,23 | 1,23 | −0,8 | −0,8 |

- **Zusammenfassung:** Median |ΔW| 4,0 cm, Median ΔW −4,0 cm; |ΔW| > 5 cm bei Nr. 3, 6, 12, 15, 21, 22, 25, 35, 36, 40. Kolktiefe 0,8–1,35 m:
  Breite 5 24/24, Breite 1 **22/24**.
- **Die zwei Kolke unter 0,8 m bei Breite 1 (6n Rückfrage):**
  - **Nr. 3** (s 402,8): 0,68 m bei 1, 0,80 m bei 5.
  - **Nr. 36** (s 531,4): 0,78 m bei 1, 1,28 m bei 5.
- **Lesart:** ΔW ist nur dort ≠ 0, wo die Breite-5-Ausgabe nicht zum Löser passt (W − G − F +4 … +53 cm); bei Breite 1 passt sie überall
  (−0,1 … −3,9 cm). Bei Breite 1 ist zugleich die gezeichnete Tiefe G an 9 dieser 10 Punkte 4,5–13 cm größer (Nr. 25: −9,8 cm). Breite 5 hebt also den gezeichneten
  Spiegel in Mulden an und senkt die gezeichnete Tiefe, genau wie 6n §2.2 vermutet. Ein tieferer Wasserstand im Löser bei Breite 1 ist es nicht.

### G3 Bett nass_sim

| Dump (Breite) | ohne Hindernis-Zellen (n 625) | mit (n 722) | G > 0,1 cm | Saum im Bett |
|---|---|---|---|---|
| T6M3A_2 (1) | **99,84 %** | 99,86 % | 100 % | 0,16 % |
| T6L2B_2 (5) | 54,24 % | 56,37 % | 100 % | 45,76 % |

Wie 6n §3 sagt, trägt `nass_sim` bei Breite 5 nicht: In 46 % der Bettzellen passt die geglättete Ausgabe nicht zu Kontur + Tiefe.

### D Kernbett-Fehlzellen bei Breite 5

Kernbett nach 6l §4: Bett, Innenabstand ≥ 2 Zellen, Neigung < 0,5; n 250, ohne Hindernis-Zellen n 244 mit denselben 6 Fehlzellen.

| s | u | Zone | Neigung | nächste Lippe (Art, Fall, \|ds\|) | W − H bei 5 | W − H bei 1 | F − H |
|---|---|---|---|---|---|---|---|
| 455,75 | −0,33 | Bett | 0,36 | 16 (Kaskadenteil, 0,72 m, 1,12 m) | −3,7 cm | +52,3 cm | −3,7 |
| 481,86 | +0,56 | Lippenkrone | 0,48 | 22 (Stufe, 1,55 m, 0,40 m) | **−13,7 cm** | +24,3 cm | −9,7 |
| 515,81 | +0,68 | Lippenkrone | 0,24 | 32 (Kaskadenteil, 1,12 m, 0,48 m) | −7,2 cm | +10,8 cm | −19,2 |
| 523,87 | −0,54 | Lippenkrone | 0,43 | 35 (Kaskadenteil, 0,96 m, 0,65 m) | −7,0 cm | +1,0 cm | −29,0 |
| 529,67 | +0,22 | Bett | 0,48 | 36 (Stufe, 1,53 m, 0,38 m) | −0,4 cm | +17,6 cm | −6,4 |
| 578,96 | +0,59 | Lippenkrone | 0,49 | 46 (Ende, 0,75 m, 0,04 m) | −2,2 cm | +20,8 cm | −2,2 |

- **Verteilung:** 4 von 6 auf Lippenkronen, wie 6n erwartet hat.
- **W − H bei 5:** liegt bei 4 Zellen unter −2 cm (−3,7 / −13,7 / −7,2 / −7,0). Breite 5 zeigt dort sichtbar trockenen Grund im Kernbett, obwohl
  der Löser 24–50 cm Wasser führt (G bei 5: 23–50 cm). Laut 6n §2.3 stärkt das die Wahl von Breite 1.
- **Bei Breite 1:** alle 6 Zellen sichtbar (+1,0 … +52,3 cm).

## 3. Zusatz: Nachbau der Glättung und Vorhersage für T6N2 (abgeleitet)

**Werkzeug** `scripts/swr/t6n_glaettung_nachbilden.py` (Ausgabe `nachbau_ausgabe.txt`, `nachbau_pruefung.json`, `p6n_nachbau_b1/2/5.json`;
nachgebaute Dumps in `export/unreal/welt/fluss_sim/swr_wasser/dump/T6N_NACHBAU/`). Es bildet Stufe 13 „PostSim“ aus dem Niagara-Asset nach:

- Methode 2, Cutoff 500 cm, Randbreite 2.
- Nur Nachbarn mit xx ≠ 0 und yy ≠ 0.
- Tiefenfenster max(hw − 2, 1).
- Eingangszustand: Löser = Breite-1-Dump, nasse Zellen = `nass_sim`, Höhe = F + G; Kollider unbekannt.

| Prüfung | Ergebnis |
|---|---|
| Nachbau Breite 1 gegen T6M3A_2 | \|dR\| Median 0,00 / p90 4,00 cm, \|dG\| 0 / 0 cm |
| **Nachbau Breite 5 gegen echten T6L2B_2** (anderer Lauf) | \|dR\| Median **0,25** / p90 4,00 cm, \|dG\| 0,08 / 2,09 cm, Jaccard nass 0,979; Kernbett 97,6 % mit **denselben 6** Fehlzellen; nass_sim 55,0 % (echt 54,2 %); Kolke: nur Nr. 25 weicht > 5 cm ab (−10 cm) |
| **Nachbau Breite 2 = Vorhersage T6N2** | G1 11,6 % ✓ (Nachbau liegt bei Breite 1 um +1,2 pp über dem echten Wert), G3 99,84 % ✓, Kernbett 100 % ✓, **G2 verfehlt**: Median \|ΔW\| 4 cm, max 48 cm, 9 Kolke > 5 cm (3, 6, 12, 15, 22, 25, 35, 36, 40), Nr. 3 0,72 m → **T6N2 verfehlt → U3** |

**Warum Breite 2 bei den Kolken wie Breite 1 wirkt:**
- Bei hw 1 hat eine nasse Zelle keine Glättung: der diagonale Abstand 1,41 ist ≥ hw, damit ist das Gewicht 0.
- Bei hw 2 tragen nur die 4 diagonalen Nachbarn bei. Ihr Gewicht ist 0,207 × smoothstep(0, 500 cm, |ΔH|), in Kolken also nahe 0.
- Erst bei hw 5 wirken Nachbarn bis 5 Zellen. Ihr Gewicht steigt mit dem Höhenunterschied, deshalb wird der obere Beckenspiegel in die Mulde
  gezogen.

**Folgerungen:**
- Der Nachbau reproduziert die Breite-5-Ausgabe aus dem Breite-1-Löser. Eine messbare Rückwirkung der Glättung in den Löser gibt es damit
  nicht; das war die Absicht von G2 (6m §1.2, 6n „Nicht belegt“).
- Ein Zwischenwert, der das Kolktor erfüllt und das Kernbett hält, ist nach dem Nachbau nicht zu erwarten. Bei 2 sind die Kolke wie bei 1;
  wie es bei 3 und 4 aussieht, ist nicht nachgebaut (das Werkzeug kann es mit `--breiten 3 4`).

## 4. Vorbereitete Kette T6N2 (falls die Cloud bei der 6n-Regel bleibt)

- **Aufbau:**
  - `live/claude_code/swr/_t6n2_kette.sh` startet die bestehende Kette `_t6m3a_kette.sh` (unverändert, Stand Opus-PM 17:52) mit `SWNEU=2`,
    `PRAEFIX=T6N2`, Log `swr/_t6n2_kette.log`.
  - Erst wenn sie mit `T6M3A_FERTIG` endet, wertet `t6n_p6n.py --breite 2` den T6N2-Dump aus.
  - Bestanden nur bei U1 und Kernbett ≥ 99 %, sonst U3. Gespeichert wird nichts.
- **Abbruch und Prüfung:**
  - `UE_PY_UNKLAR` in der inneren Kette führt zu `T6N2_ABBRUCH` ohne weitere Befehle und ohne Auswertung.
  - SHA-256 der Zusatz-Eingaben: `swr/_t6n2_eingaben.sha256` (12 Dateien, darunter die Repo-Dateien des Bettplans und die innere SHA-Liste).
- **Start:** `cd live/claude_code && bash kette_start.sh swr/_t6n2_kette.sh` (≈ 30 min). Voraussetzungen wie 3a: harter Neustart ohne Speichern,
  BAKED_SIM, `smoothing_width` 5, `schmutzig_liste` = 0.
- **Trockenlauf 8/8** (`t6n2_trockenlauf_ausgabe.txt`):
  - Stub-Dump mit G3 verfehlt → „verfehlt“;
  - künstlicher Dump mit allen Toren bestanden → „bestanden“;
  - UE_PY_UNKLAR innen → Abbruch ohne P6N;
  - falsche SHA → Abbruch vor der inneren Kette.

## 5. Offene Punkte

- **G2 als Tor:** ΔW vergleicht gezeichnete Spiegel. Bei Breite 5 enthält W die Glättung, darum misst G2 hier die Darstellung, nicht den Löser.
  Frage an die Cloud (6o):
  - G2 auf Löser-konsistente Werte (W − G − F) umstellen?
  - oder die Kolktiefe als reine Bild-Abwägung behandeln (6n U3: Ferat)?
- **Grenzen des Nachbaus:** Kollider (WH-Hindernisse) sind nicht bekannt und fehlen im Nachbau. Saumzellen mit zufällig |W − G − F| ≤ 5 cm
  zählen als nass. Der Breite-5-Vergleich stammt aus einem anderen Lauf (Schritt 2).
- **Auflösung:** Die Half-Float-Stufe beträgt bei oberen Kolken 4 cm; die Schwelle „Median ≤ 2 cm“ ist dort nicht auflösbar.
- **Speicherkette:** nicht vorbereitet (siehe Kurzfazit).

## 6. Dateien

**Daten und Ausgaben** (`docs/pruefung/wasser/t6n/`):
- `p6n_bericht.md` (dieser Bericht), `p6n_ergebnis.json`, `p6n_ausgabe.txt`
- `nachbau_ausgabe.txt`, `nachbau_pruefung.json`, `p6n_nachbau_b1.json` / `b2` / `b5`
- `t6n2_trockenlauf_ausgabe.txt`

**Skripte** (`scripts/swr/`): `t6n_p6n.py`, `t6n_glaettung_nachbilden.py`, `t6n2_trockenlauf.py`

**Kette** (`live/claude_code/swr/`): `_t6n2_kette.sh`, `_t6n2_eingaben.sha256`
