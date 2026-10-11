# Antwort zu Auftrag 15 – Regelwerk: steile Bach- und Flussstrecken (Felsstufen, Klippen, Fälle)

Stand 11.10.2026. Teil „Natur + Quellen“ (Regelwerk-Agent). Prioritätenliste und Planer macht der zweite Agent; der Koordinator führt beides in
`15-gefaelle.md` zusammen. Maschinenlesbar: [`skripte/gefaelle/gefaelle_regeln.json`](skripte/gefaelle/gefaelle_regeln.json) (Schema im Block `_schema`).

**Kennzeichnung:** Jede Zahl trägt eine Quelle (Kürzel, Liste am Ende) oder **[Annahme]**. „[Annahme, nach X]“ heißt: Bereich aus Quelle X,
der genaue Wert ist eine Spielentscheidung. **Quellenlage:** WebFetch war in dieser Umgebung gesperrt (DNS-Fehler, auch für Wikipedia und
Hochschulserver). Alle Online-Belege stammen deshalb aus Suchmaschinen-Auszügen der verlinkten Seiten. Standardwerte aus der Lehrbuchliteratur,
die ich nicht online nachprüfen konnte, sind mit „(Lehrbuch)“ markiert.

## Kurzfazit

1. **Nie eine Schräge.** In der Natur fällt steiles Wasser fast ganz an Stufen, dazwischen liegen nahezu waagrechte Becken. Im Grand Canyon
   fällt der Großteil der Höhe in Schnellen, die nur ~10 % der Strecke ausmachen (LEO1969). Regel: Beckenspiegel ≤ 2 % (hart 3 %) [Annahme],
   der ganze Rest des Falls liegt auf Stufen. Eine Stufe ist im Spiegel **zwei Punkte ≤ 1 m auseinander**, und der Spiegel steigt nie.
2. **Gerinnetypen nach Gefälle** (Bach, IP2004 nach MB1997; GRANT1990):
   | Gefälle S | Natur | Spielbild |
   |---|---|---|
   | < 1,5 % | pool-riffle | ruhig |
   | 1,5–3 % | plane-bed | ruhig, kleine Schnellen |
   | 3–6,5 % | step-pool | Blockstufen 0,3–1 m |
   | 6,5–30 % | Kaskade bzw. steiler step-pool („steps“ im Mittel 17 %) | dichte Blockstufen 0,5–2 m, einzelne Fälle am Fels |
   | 30–60 % | Fels-/Hangschuttgerinne | Fallkette 2–6 m mit Gumpen [Grenze: Annahme] |
   | > 60 % | Fall/Klamm | Einzelfälle ≥ 4 m, Klammwände [Annahme] |

   Ferats Vorschlag (8–30 % step-pool) deckt sich gut mit der Literatur. Nur die untere Grenze liegt dort bei 3 % statt 8 %.
3. **Stufenabstand L** = B · clamp(0,4 · S^−0,7; 0,8; 4). Das ergibt 1–4 Bachbreiten (MB1997, Lehrbuch) bzw. 0,43–2,4 Breiten (CHIN1999), mit
   steilerem Gefälle enger [Formel: Annahme]. **Spiegelfall je Stufe** D ≈ S · L. **Betthöhe** H = c · S · L mit c = 1–2, Ziel 1,5 (ABR1995).
   Daraus folgt die **Kolk-Resttiefe** (c − 1) · S · L ≈ 0,5 · D.
   Beispiel 4 m breiter Bach bei 20 %: L ≈ 5 m, D ≈ 1 m. Der gebaute C2-Lauf (11 m, 31 %) hat 12 Stufen à 1,8–5,3 m; die Regel liefert 16 à 3,3 m. Das passt.
4. **Stufenarten nach Spiegelfall D:**
   | Art | D | Ausführung |
   |---|---|---|
   | Schnelle | 0,15–0,8 m | kurze Rampe 1,5–4 m, kein Vorhang (FORMAT: Vorhang erst ab 0,8 m) |
   | Blockstufe | 0,8–2 m | Höhe ≈ Größe der Stufenblöcke (RC2021: H ≈ D100) |
   | Fall | ≥ 2 m | nur an anstehendem Fels |

   **Einzelfall statt Kette**, wenn das lokale Gefälle ≥ 60 % ist und dabei ≥ 4 m Fall auf kurzer Strecke (≤ 3 B, 10–40 m) zusammenkommen.
   An anstehendem Fels reichen ≥ 2 m. Die Zahlen sind [Annahme]; die Form folgt dem Knickpunkt an einer harten Schicht (NIAGARA, YOSEMITE, IGUAZU).
5. **Flüsse (B ≥ 10 m)** bilden keine Blockstufen über die volle Breite (Klemmverhältnis Breite/Block, CZ2007). Sie bilden Pool-Schnellen-Folgen
   und bei ≥ 15 % Felskatarakte bzw. breite Fälle. Vorbild Krka: 17 Kalktuffstufen auf 800 m, 45,7 m Fall, also ~2,7 m je Stufe bei ~5,7 %
   (KRKA). Die Regel liefert dafür ~2 m je Stufe auf ~35 m.
6. **Wände:**
   - **Fälle wandern stromauf und hinterlassen eine Schlucht** (Niagara 0,7–1,16 m/Jahr, NIAGARA). Daher bekommt jeder Fall ≥ 2 m seitliche
     Wände von Fallhöhe + 1 m. Unterhalb eines Falls ≥ 4 m folgt eine Schlucht mit Wänden ≈ Fallhöhe, Länge ≈ 4 × Fallhöhe [Faktoren: Annahme].
   - **Klamm**: ab S ≥ 30 % mit Fall oder ≥ 3 m Eintiefung [Annahme]. Echte Klammen sind 80–200 m tief bei 1–2 m Engstelle (KLAMMEN). Im Spiel
     reicht Tiefe/Breite ≥ 3:1.
7. **Gestein je Biom:**
   | Biom | Gestein | Stufenform |
   |---|---|---|
   | Bergwald, Gletscher, Fjord | Granit/Gneis | Blockstufen, Kluftkanten, Gletschertreppe |
   | Canyon, Wüste | geschichteter Sandstein | harte Bank als Lippe, Alkove darunter |
   | Lava | Basalt | Säulenwand (Svartifoss 20 m) |
   | Dschungel | Kalktuff | bewachsene Sinterbarrieren (Plitvice, Krka) |
   | Elfenwald, Aue, Sumpf | bemooster Fels, Holz | Holz- und Wurzelstufen (CURWOHL2003) |

   Alle **645 Netzeinträge** sind gegen `netze.csv` geprüft: 0 Fehler, keine gesperrten Netze, keine Netze mit Materialfehler laut `netz_check_ergebnis.json`.
8. **Effekte:** höchstens 3 Systeme je Stufe, höchstens 6 gleichzeitig aktiv, Cull 30/45/60 m, Heldenfälle bis 150 m (A12, A14).
   | Stufenart | System |
   |---|---|
   | Schnelle | Stream |
   | Blockstufe | Impact (abwechselnd Impact, Stream, nichts) |
   | Fall 2–6 m | Waterfall_Small + Impact_Small |
   | Fall 6–20 m | Medium-Trio |
   | Fall > 20 m | Large-Trio |

---

## 1. Was die Natur macht (mit Belegen)

### 1.1 Gerinnetypen und Gefälle

| Typ (MB1997) | Gefälle (IP2004 nach MB1997) | Mittleres Gefälle der Einheit (GRANT1990) | Poolabstand (MB1997, Lehrbuch) | Bild |
|---|---|---|---|---|
| dune-ripple / pool-riffle | < 0,015 | Pool 0,005 · Riffle 0,011 | 5–7 B | Mäander, Kiesbänke |
| plane-bed | 0,015–0,030 | Rapid 0,029 | – (keine Pools) | gleichmäßig rau |
| step-pool | 0,030–0,065 | Cascade-Einheit 0,055 | 1–4 B | Blockstufen quer, Becken |
| cascade | > 0,065 | Step-Einheit 0,173 | < 1 B | Wasser springt von Block zu Block |
| bedrock / colluvial | beliebig / steil | – | – | Felsstufen, Fälle, Hangschutt |

- MB1997 messen Gerinne auf ≥ 10–20 Breiten Länge. Das ist die Fenstergröße für die Klassifizierung: `clamp(10·B, 20, 100)` m [Grenzen: Annahme].
- Achtung bei den Begriffen: GRANT1990 benennt *Einheiten* (Pool, Riffle, Rapid, Cascade, Step), MB1997 *Abschnitte*. Steile Bäche zwischen
  10 und 30 % sind in der Natur genau die „steps“ (Mittel 17,3 %). Das stützt Ferats Wahl „8–30 % = Stufen“.

### 1.2 Step-Pool-Geometrie

- **H/L/S = 1–2** bei maximalem Fließwiderstand. Flume-Versuche und 18 natürliche Bäche bestätigen das (ABR1995). H ist die Stufenhöhe von der
  Krone bis zum Kolkgrund, L der Abstand Krone–Krone, S das mittlere Gefälle.
- **Abstand L:** 1–4 Bachbreiten (MB1997, Lehrbuch). Spektralanalyse bei Chin: 0,43–2,40 Breiten (CHIN1999). Viele Daten liegen um 1 B, mit
  langem Ausläufer nach oben. Der Abstand nimmt mit dem Gefälle ab.
- **Stufenhöhe ≈ Größe der größten Blöcke** (H ≈ D100, RC2021). Der Abstand skaliert mit der Grenztiefe, also mit dem Abfluss (RC2021).
  Stufen halten nur, wenn sich die Blöcke quer verkeilen. Das kleine Verhältnis Breite/Blockgröße heißt „jamming ratio“ (CZ2007; in der neueren
  Literatur umstritten).
- **Holzstufen:** Stufen bestehen aus großem Holz, Fels, Wurzeln oder Blöcken. Holz erhöht die Stufe (CURWOHL2003).

### 1.3 Wasserfälle und Knickpunkte

- **Fälle entstehen an einer harten Schicht über weicherem Gestein.** Niagara: Lockport-Dolomit über Rochester-Schiefer, der Schiefer wird
  unterspült (NIAGARA). Die reale Unterschneidungskehle ist dort nur bis ~10 m tief; der Fall weicht eher durch stetiges Abbröckeln zurück (HM2009).
- **Rückschreiten:** Horseshoe Falls 1,16 m/Jahr (1842–1905), 0,70 m/Jahr (1906–1927). Unterhalb bleibt eine Schlucht (NIAGARA).
- **Granit:** Fälle an Klüften und in Hängetälern. Yosemite Falls hat drei Stufen an horizontalen Klüften, Vernal und Nevada Fall liegen auf
  einer „Gletschertreppe“ mit flachen Tritten (YOSEMITE).
- **Basalt:** Svartifoss fällt 20 m vor einem Säulen-Amphitheater von 15–20 m Höhe und 30 m Breite (SVARTI). Iguazu stuft sich über gestapelte
  Basaltströme, ~80 m (IGUAZU).
- **Kolk (Gumpe):** Er wird tiefer mit Fallhöhe und Abfluss und flacher mit viel Geschiebe; Daten von 75 Fällen (SL2016). Gemessen wurden Kolke
  bis ~10 m Tiefe (EGU2025). Eine einfache Formel Tiefe ~ Fallhöhe gibt die Literatur nicht her. Daher **[Annahme]**: Tiefe = clamp(0,3·D + 0,5; 1; 8) m.
  Den Radius bestimmt die Wurfweite des Strahls, x = v0 · √(2D/g) (PHYS), mit v0 = 0,5–3 m/s [Annahme].

### 1.4 Klammen und Schluchten

- **Aareschlucht** 1,4 km lang, bis 200 m tief im Kalk. **Breitachklamm**: Engstelle „Zwing“ 2 m bei ~100–150 m Tiefe. **Partnachklamm** 702 m,
  ~80 m tief (KLAMMEN). Das Verhältnis Tiefe zu Breite liegt also bei 10–100.
- **Strudellöcher:** Tiefe/Radius meist ~2, also Tiefe ≈ Durchmesser; über 3 ist selten (PEL2015). Tiefe und Durchmesser wachsen linear,
  gemessen an 3 930 Strudellöchern (JI2018). Die Formenlehre dazu: RC2005.
- **Verkeilte Blöcke (Klemmblöcke):** Sie sind in Slot-Canyons belegt (Fotobeleg Cottonwood Wash), Maßzahlen habe ich nicht gefunden. Regel
  **[Annahme]**: 2 je 100 m, Durchmesser 1,0–1,4 × Sohlbreite, 1–6 m über der Sohle.

### 1.5 Stromschnellen und Katarakte in Flüssen

- Pool-Schnellen-Wechsel ist der Gleichgewichtszustand. Der Großteil des Falls liegt in Schnellen auf ~10 % der Länge (LEO1969).
- Kalktuff-Flüsse: Krka mit 17 Stufen auf 800 m, 45,7 m Fall, 200–400 m breit (KRKA). Plitvice mit 16 Seen hinter Barrieren, 636 → 503 m auf
  ~8 km; die Barrieren wachsen ~1 cm/Jahr (PLITVICE).
- Flüsse über 4 % sind in der Natur selten. Die 19 Flussstrecken (4–31 %) werden darum wie Katarakte und Kalktuff- bzw. Felsfälle behandelt,
  nicht wie Bäche.

### 1.6 Gesteinsabhängigkeit

| Gestein | Stufenform | Belege | Biome |
|---|---|---|---|
| Granit/Gneis | gerundete Blockstufen, glatte Platten, Kluftkanten, Gletschertreppe, Hängetal-Fälle | YOSEMITE | bergwald, gletscher, fjord, frost, heide |
| geschichteter Sandstein | eine harte Bank als durchgehende Lippe, darunter Alkove; Wasseraustritt an der Schichtgrenze unterhöhlt die Wand; „hanging gardens“ | LM1985, NPS_NAVAJO | canyon, wueste |
| Basalt | Säulenwand, Amphitheater, Säulenstümpfe als Schutt; Fälle in Etagen je Lavastrom | SVARTI, IGUAZU | lava, (kueste, tundra) |
| Kalk / Kalktuff | Sinterbarrieren mit vielen dünnen Strähnen, türkise Becken, Travertin-Terrassen; Kalk-Klammen | PLITVICE, KRKA, HAVASU, KLAMMEN | dschungel |
| Schiefer/Tonstein mit harten Bänken | brüchige Stufen, viel Schichtschutt | NIAGARA (Prinzip) | oedland |
| Lockergestein + Wald | Holz- und Wurzelstufen, Erdanrisse | CURWOHL2003 | aue, sumpf, elfenwald |

---

## 2. Regelwerk für den Planer

Alle Formeln stehen in `gefaelle_regeln.json`. Variablen: S (Gefälle im Fenster), B (Wasserbreite), L, D, H. Dazu gilt
`clamp(x, lo, hi)` = min(max(x, lo), hi).

### 2.1 Harte Regeln

1. **Wasserspiegel nie steigend:** Für alle Punkte von `spiegel_neu_cm` gilt z[i+1] ≤ z[i], Toleranz 0.
2. **Stufe = zwei Punkte:** Der obere Punkt liegt auf der Lippe (z_oben), der untere 0,3–1,0 m stromab (z_oben − D). Der Abstand ist ≤ 1 m (A12, Auftrag).
3. **Flussstücke an jeder Stufe ≥ 0,8 m trennen:** Das obere Stück endet 0,5–1 m hinter der Kante, das nächste beginnt 1–2 m stromab des Fußes.
   Die Lücke ist ≥ 1,2 m, die Stücke überlappen sich in der Draufsicht nicht (A12).
4. **Anfang und Ende behalten ihre Höhe.** Die Summe aller D plus der Beckenfall muss D_ges ergeben; nach dem Zufall wird normiert.
5. **Becken:** Spiegelgefälle `min(0,02; 0,15·S)`, hart ≤ 0,03 [Annahme, Ferat]. Spiegelfall an der Stufe: D = S·L − S_Becken·(L − Stufenlänge).

### 2.2 Klassen (Schwellen je Art)

| Bach (B < 10 m) | S | Stufenarten |
|---|---|---|
| ruhig | < 0,015 | – |
| riffel | 0,015–0,03 | Schnelle |
| step_pool | 0,03–0,065 | Schnelle, Stufe |
| kaskade_stufen | 0,065–0,30 | Stufe, Kaskade, Fall (an Fels) |
| fallkette | 0,30–0,60 | Kaskade, Fall |
| fall_klamm | > 0,60 | Fall |

| Fluss (B ≥ 10 m) | S | Stufenarten |
|---|---|---|
| ruhig | < 0,005 | – |
| riffel | 0,005–0,02 | Schnelle |
| schnellen | 0,02–0,04 | Schnelle 0,3–1 m |
| pool_rapid | 0,04–0,15 | Schnelle, Stufe, Kaskade (Ziel-Fall 2 m je Stufe) |
| katarakt_fels | 0,15–0,40 | Kaskade, Fall (Ziel 3,5 m, mehrere Arme) |
| fall_schlucht | > 0,40 | breiter Fall + Schlucht |

Die Grenzen bis 0,065 (Bach) bzw. 0,04 (Fluss) sind belegt (IP2004, GRANT1990), alle höheren Grenzen sind **[Annahme]**.

### 2.3 Stufen

- **Bach:** L = B · clamp(0,4·S^−0,7; 0,8; 4). Das ergibt bei S = 0,05 → 3,3 B, 0,10 → 2,0 B, 0,20 → 1,2 B, 0,30 → 0,9 B. Kaskade: L = 0,6 B.
- **Fluss:** L = clamp(D_ziel/S; 1 B; 6 B). Die Schnelle ist clamp(0,1·L; 3 m; 0,3·L) lang (LEO1969).
- D = S · L, H = 1,5 · S · L (ABR1995). Streuung ±25 % auf L und ±30 % auf D [Annahme]. Abstand mindestens max(2,5 m; 0,8 B), höchstens
  20 Stufen je 100 m, mehr wird zur Kaskade zusammengefasst [Annahme].
- **Holzstufen** (D ≤ 1 m, B ≤ 6 m) als Anteil der Stufen [Annahme, nach CURWOHL2003]:
  | Biom | Anteil |
  |---|---|
  | sumpf | 80 % |
  | aue | 40 % |
  | elfenwald | 30 % |
  | bergwald | 15 % |
  | dschungel | 10 % |
- **Lippe** (`lippe_cm`, links → rechts mit Blick talwärts, 3–7 Punkte) [Annahme]:
  - quer zur Fließrichtung, 90 ± 15°;
  - Breite B + 2·clamp(0,25 B; 0,5; 2) m, die Lippe bindet also beidseitig ins Ufer ein;
  - flacher Bogen mit Scheitel stromab, Pfeilhöhe 0,1 B;
  - der Hauptüberfall ist clamp(0,5 B; 1 m; B) breit und sitzt aus der Mitte versetzt.

### 2.4 Kolk und Becken

| Größe | Regel | Beleg |
|---|---|---|
| Kolk unter Blockstufe | Tiefe clamp((c−1)·S·L; 0,3; 2) m, tiefster Punkt 0,5–1 D unter der Lippe | ABR1995 / [Annahme] |
| Kolk unter Fall | Tiefe clamp(0,3 D + 0,5; 1; 8) m, Radius max(0,75 B; x_Strahl + 0,5 B; 2 m), oval 1,2–1,5 : 1 | SL2016, EGU2025, PHYS / [Annahme] |
| Beckenlänge | L − Stufenlänge, mindestens max(0,8 B; 2 m), sonst Kaskade | [Annahme] |
| Beckenbreite | 1,2 B | [Annahme] |
| Flussbecken zwischen Schnellen | Tiefe clamp(0,1 B; 1,5; 6) m | [Annahme, nach LEO1969] |

### 2.5 Einzelner großer Fall statt Stufenkette

- Bedingung: lokales Gefälle (Fenster clamp(2 B; 8; 20) m) ≥ 0,6 **und** Fall im Fenster ≥ 4 m, bei anstehendem Fels ≥ 2 m. Steilstücke
  innerhalb clamp(3 B; 10; 40) m werden zu **einem** Fall gebündelt; davor und danach wird das Gefälle flacher [Annahme].
- **Fels gilt als anstehend**, wenn mindestens eins zutrifft [Annahme]:
  - im Umkreis 10 m ist eine der Lagen Fels, Felsplatte, Sandstein oder Lavafels ≥ 128;
  - die Hangneigung quer zum Lauf ist > 45°;
  - Biom bergwald, gletscher, frost, fjord, canyon oder lava und S ≥ 0,30.
- Ein Einzelfall wird höchstens 25 m hoch, darüber zwei Fälle mit Zwischengumpe [Annahme]. Ausnahme sind die Heldenfälle WF_K1/K8.
  In Fallketten sind die Glieder ~8 m hoch (clamp 2–12 m), mit flachen Tritten der Länge max(2·Kolkradius; 1,5 B) dazwischen
  [Annahme, nach YOSEMITE].
- Die Lippe ist eine **durchgehende Kante** aus Riegel-Netzen, kein Steinhaufen:
  - Riegeldicke clamp(0,3 D; 1; 4) m, Überstand 0,2–1,5 m, Fallwand 70–90°;
  - Hohlkehle bis 0,3 D tief, nur als Netz, denn die Landschaft kann keine Überhänge (FORMAT).
- **Breite Fälle (Fluss):** Lippe leicht hufeisenförmig, 2–5 Strähnen mit nassen Felsrippen dazwischen [Annahme, nach IGUAZU/KRKA].

### 2.6 Klamm und Uferklippen

| Regel | Wert | Beleg |
|---|---|---|
| Klamm wann | S ≥ 0,30 und (Fall ≥ 4 m oder Bett ≥ 3 m unter beiden Ufern) | [Annahme] |
| Sohlbreite | clamp(1,2 B; 2 m; 2 B) | [Annahme, nach KLAMMEN] |
| Klammtiefe unter Fall | ≈ Fallhöhe, clamp(D; 3; 40) m | [Annahme, nach NIAGARA] |
| Tiefe : Breite | ≥ 3 : 1 (Natur 10–100) | KLAMMEN / [Annahme] |
| Klammlänge unterhalb | clamp(4 D; 15; 150) m | [Annahme] |
| Strudellöcher | 4 je 100 m, Ø 0,5–3 m, Tiefe ≈ Ø | PEL2015 / [Annahme] |
| Klemmblöcke | 2 je 100 m, 1,0–1,4 × Sohlbreite, 1–6 m über der Sohle | [Annahme] |
| Uferwand wann | S ≥ 0,20 und Gelände bis 2 B Abstand ≥ 2 m über dem Spiegel; außerdem an jedem Fall ≥ 2 m | [Annahme] |
| Wandhöhe am Fall | clamp(D + 1; 2; D + 5) m | [Annahme, nach NIAGARA] |
| Wandlänge unterhalb | clamp(3 D; 6; 60) m | [Annahme] |
| Wand: Abstand zum Wasser, Neigung | 0–1,5 m, 60–90° | [Annahme] |
| Prallhang / Gleithang | Außenbogen höhere Wand, Innenbogen Schutt/Kies | [Annahme] |
| Wandnetze | Gruppen aus 2–5 Netzen, 10–30 % überlappend, eine Schichtneigung (5–15°), 25–40 % eingegraben | A5 |

### 2.7 Schutt und Blöcke

| Ort | Größe | Beleg |
|---|---|---|
| Stufenblöcke | max(1,0 · H; B/6), clamp(Lippenbreite / Blockgröße + 1; 2; 9) je Lippe, Keystone in der Mitte | RC2021, CZ2007 / [Annahme] |
| Becken | Kies/Steine 0,05–0,3 m | [Annahme] |
| unter Fällen | clamp(D; 3; 15) Sturzblöcke, Größe clamp(0,15 D; 0,5; 3) m | [Annahme] |
| Wandfuß | Schuttkegel ~35° (30–37°), Länge 0,6 × Wandhöhe, unten grob, oben fein | SCREE / [Annahme] |

### 2.8 Bodenlagen

Die Namen sind exakt die aus FORMAT §2. Die Gewichte stehen in `lagen.zonen`, die Lagenwahl je Biom in `biome.<biom>.lagen`.

| Zone | Gewicht | Breite | Normalfall |
|---|---|---|---|
| bett_becken | 200 | B | Kies |
| bett_stufe | 220 | B + 2 m | Geroell |
| bett_fels | 230 | B + 2 m | Felsplatte |
| kolk | 150 | Kolkradius | Kies + Geroell |
| ufer_nah | 160 | 2 m | je Biom |
| ufer_gischt | 200 | clamp(1,5 D; 3; 25) m | Moos |
| wandfuss | 220 | 0,6 × Wandhöhe | Geroell + Fels |

- Die Spritzzone verdient das Moos: Kryptogamen sind dort 4,4-mal vielfältiger, und die kühle Luft wirkt über die Gischt hinaus (SPRAY_BC).
- Biom-Ausnahmen in der Spritzzone: frost → Eis, canyon/wüste → Moos nur im Sprühschatten.
- Ränder weich ≥ 3 m (FORMAT).

### 2.9 Effekte (Nature Water FX, Pfade `/Game/NatureWaterFX/FX/…`)

| Stufenart | D | Systeme (Pflicht + optional) | Ort | Cull |
|---|---|---|---|---|
| schnelle | 0,15–0,8 m | `NS_Stream_Small` (B ≥ 6 m `Medium`, ≥ 15 m `Large`), jede 2. Schnelle | Mitte Rampe, Spiegel + 10 cm | 30 m |
| stufe | 0,8–2 m | `NS_Impact_Small` (+ `NS_Stream_Small`), abwechselnd Impact/Stream/leer | Aufprall 0,2–0,6 m hinter dem unteren Punkt | 30 m |
| kaskade | 0,4–1,5 m je Teilstufe | `NS_Stream_Medium` (+ `NS_Impact_Small`) | Mitte | 45 m |
| fall_klein | 2–6 m | `NS_Waterfall_Small` + `NS_Impact_Small` (+ `NS_Wake_Small`) | Lippe + 0,2 m / Aufprall / Aufprall + 2 m | 45 m |
| fall_mittel | 6–20 m | `NS_Waterfall_Medium` + `NS_Impact_Medium` + `NS_Wake_Medium` | wie oben, Wake + 4 m | 60 m |
| fall_gross | > 20 m | Large-Trio | wie WF_K1/K8 | 150/100/60 m |

- **Grenzen:** höchstens 3 Systeme je Stufe; höchstens 6 gleichzeitig aktiv an jedem Standort am Bach (A14-Prüfung); laut SEHENS_FORMAT
  höchstens 3 je Ort.
- **Pflicht an jeder Stufe ≥ 0,8 m:** Vorhang und Schaumscheibe bleiben, Niagara ergänzt nur (A14).
- **Einstellungen:** Cast Shadow aus, Sort Priority 2, Pivot 3–10 cm über dem Spiegel; die lokale +X-Achse zeigt in Fließrichtung (A14).
- **Klang:** Cues I–III für Schnellen, IV–VI für Stufen, VII–X für Fälle; Radius 25–35 m, Heldenfall 90 m (A14).
- Die Skalen-Referenzen (Small 3×5 m usw.) sind aus A14 übernommen und **ungeprüft**.

---

## 3. Felstyp und Netze je Biom

Die vollständigen Listen stehen in `biome.<biom>.netze`, mit den Gruppen lippe, riegel, bloecke, wand, schutt, kies, holz und extra.
Gewählt wurde nach den Paletten der Sehenswürdigkeiten-Planer (`sehens_<biom>_regeln.json`) und den Maßen aus `netze.csv`:
- Riegel und Blöcke 2–6 m für Stufen bis 2 m (halb eingegraben);
- Wände 5–40 m;
- `SM_ForestRockShelf_01` als voller Megascans-Pfad, weil der Name doppelt vorkommt.

| Biom | Felstyp | Lippe (Auswahl) | Riegel / Blöcke | Wand | Schutt | Lagen Becken / Stufe / Ufer / Gischt |
|---|---|---|---|---|---|---|
| bergwald | Granit/Gneis | `SM_flat_rock_01…04`, `SM_ground_rock_03_03` | `SM_mountain_rock_big_02_1…8` | `SM_big_rock_wall_01…03`, `rcygn_tier_0`, `SM_HugeNordicCoastalCliff_01/02` | `SM_mountain_rock_big_01_*`, `SM_ground_rock_01/02` | Kies / Geroell / Geroell, Nadeln, Moos / Moos |
| elfenwald | bemooster Fels + Wurzeln | `SM_ForestRockShelf_01…03`, `SM_ForestRockSlab_01`, `SM_MossyRocks_01/02` | `SM_MossyForestBoulder_*` | `SM_HugeMossyForestCliff_01`, `SM_MossyRockFace_02`, `plFhY_tier_0` | `SM_MossyForestRock_01/03`, `SM_stones_01_*` | Kies, Moos / Geroell / Moos, Laub / Moos |
| aue | Kies, Holz | `SM_flat_rock_02/03` | `SM_stones_01_2/6`, `SM_Rock_04/07` / `SM_Rock_01/03/06` | `SM_MossyEmbankment_*`, `SM_GrassyEmbankment_*` (Erdanriss) | `SM_stones_01_1/4/5` | Kies / Geroell / Kies, Gras, Schlamm / Moos |
| dschungel | Kalk, Kalktuff | `SM_LimestoneRocks2/3`, `SM_ForestRockShelf_02`, `SM_flat_rock_*` | `SM_LimestoneRocks2/3` / `SM_Big_Rock_01…03` | `ukjhcamga_tier_0`, `uchoab3fa_tier_0` | `SM_ground_rock_*`, `Limestone_Rocks_ubqwdheda_High` | Kies, Algen / Geroell / Moos, Schlamm / Moos |
| lava | Basalt | `Basalt_Basalt_Pillars_Cluster_Low_SM`, `…Pillar_A/Variance_A` | Säulenstümpfe / `Basalt_Basalt_Rock_A…D_SM`, `SM_lava_b_rock_*` | `Basalt_Basalt_Pillars_Wall/WallOverhang/WallSlope_SM`, `Basalt_Basalt_Cliff_SM`, `SM_lava_wall_*` | Säulenstücke B/C, `SM_lava_s_rock_*` | Lavasand, Kies / Lavafels / Lavafels, Moos / Moos |
| gletscher | Granit/Gneis, geschliffen | `SM_flat_rock_01/04`, `SM_SmoothRockShelf_01` | `SM_mountain_rock_big_02_*`, `SM_NordicBoulder_01` | `SM_big_rock_wall_*`, `rcygn_tier_0`, Eiswand `uhprdg2fa_tier_0` | Moränenschutt, `pkeeM_tier_0` | Kies, Geroell / Geroell / Geroell, Fels / Moos |
| frost | Granit + Eis | `SM_flat_rock_01…04` | `SM_mountain_rock_big_02_*` | Granitwände + `Ice_Cliff`-Netze | dazu Eissplitter | Kies / Geroell / Schnee, Eis / **Eis** |
| fjord | Gneis | `SM_flat_rock_02…04` | `SM_mountain_rock_big_02_*`, `SM_NordicBoulder_01` | `SM_MassiveNordicCoastalCliff_01`, `vdssailfa/vfmjadufa/veqnci0db_tier_2` | `SM_mountain_rock_big_01_*` | Kies, Geroell / Geroell / Fels, Moos, Heide / Moos |
| tundra | Frostschutt auf Gneis/Basalt | `SM_flat_rock_03`, `SM_SmoothRockShelf_01`, `SM_ForestRockFormation_05` | `SM_TundraMossyBoulder_01`, `skjsL_tier_0` | `SM_MassiveTundraRockFormation_02`, `rcygn_tier_0` | `SM_TundraRockyGround_01` | Kies / Geroell / Moos, Trockengras / Moos |
| heide | Granit (Wollsack) | `SM_flat_rock_03`, `SM_SmoothRockShelf_01` | `SM_Rock_01…07` / Granite_Rock `pjEr1/pjtsT/pkeeM` | `SM_big_rock_wall_*` | `SM_s_rock_*` | Kies / Geroell / Heide, Moos / Moos |
| kueste | Gneis/Basalt | `SM_flat_rock_04`, `Basalt_Basalt_Rock_B_SM` | `SM_NordicBeachRocks_01` / `SM_NordicBoulder_01` | `SM_HugeNordicCoastalCliff_*`, `SM_MassiveNordicCoastalCliff_01`, `Basalt_Basalt_Cliff_SM` | `SM_NordicBeachRockyGround_*` | Kies / Geroell / Fels, Gras / Moos |
| sumpf | kein Fels | `SM_MossyForestRoots_01/02` | `SM_dead_log_01…04` | `SM_MossyEmbankment_*` | Äste | Schlamm / Schlamm / Moos, Schlamm / Moos |
| canyon | geschichteter Sandstein | Ledges `vbvqbbofa`, `uk5pbhv`, `ulerccg`, `uk5ebcp_tier_0` | Ledges / `SM_SandstoneBoulder_*`, `SM_RockSandstone_*` | `Desert_Western_Cliff_Layered`-Netze (`vb1mbdega` …), `SM_MassiveSandstoneCliff_*` | Schichtgeröll `ul4lehiga/ulnfeaw/ulcceh3_tier_0` | Sand, Kies / Sandstein / Sandstein, Sand / Moos |
| wueste | Sandstein + Granitblöcke | wie canyon | Ledges / `SM_namaqualand_boulder_*` | `Desert_Western_Cliff_Layered`-Netze | Schichtgeröll | Sand, Kies / Sandstein / Sand, Sandstein / Moos |
| oedland | Schiefer mit harten Bänken | `SM_Rock_02/04`, `ulerccg_tier_0` | `SM_Rock_01/03/05/06` | `uchoab3fa_tier_0` (Quarry), `ukjhcamga_tier_0` (Layered Rock) | Schichtgeröll, `SM_s_rock_*` | Kies, Schlamm / Geroell / Erde, Geroell / Moos |

Hinweise je Biom (stehen auch in `besonderheiten`):
- **dschungel:** Kalktuff-Barrieren 0,5–3 m, Wasser `tuerkis`, Vorhang in vielen Strähnen über die ganze Lippe.
- **lava:** Säulen senkrecht in der Wand, Säulenstümpfe als Lippe und als Schutt im Becken.
- **gletscher:** Wasser `gletschermilch`; Fälle aus Hängetälern.
- **frost:** Eiszapfen (`SM_EISZAPFEN_*`) an Lippe und Wand.
- **canyon/wüste:** Alkove unter der Lippe, Grün nur im Sprühschatten.
- **kueste:** kein Kolk im Meer.
- **aue/sumpf:** Stufen meist aus Holz, Uferanrisse aus Erde statt Felswand.

Zur Verteilung: Die 161 Strecken liegen nach dem Hauptbiom ihres Feldes vor allem in elfenwald (49), aue (41), bergwald (24), dschungel (16),
gletscher (11) und tundra (12). Für aue zeigt das Hauptbiom oft nur die Talsohle; der Planer sollte das Biom am Ort nehmen.

---

## 4. Vorbilder für die Optik

Natur (Links im JSON unter `vorbilder.natur`):
- **Svartifoss** (Basalt, lava): [Wikipedia](https://en.wikipedia.org/wiki/Svartifoss).
- **Hraunfossar/Aldeyjarfoss** (lava/tundra): Wasser tritt seitlich aus der Wand.
- **Iguazu** (breite Front, zwei Etagen): [IUGS](https://iugs-geoheritage.org/geoheritage_sites/iguazu-iguacu-waterfalls/).
- **Plitvice**: [Poster Uni Zagreb](https://www.pmf.unizg.hr/images/50025872/2019_7.%20PLITVICE%20LAKES%20poster.pdf).
- **Krka, Skradinski buk**: [NP Krka](https://npkrka.hr/en_us/en_US/posjeti/sadrzaji/skradinski-buk/).
- **Havasu/Mooney Falls** (Travertin im roten Canyon): [Earth Magazine](https://www.earthmagazine.org/article/travels-geology-havasu-canyon-land-blue-green-water/).
- **Zion/Navajo-Alkoven**: [NPS](https://www.nps.gov/articles/nps-geodiversity-atlas-navajo-national-monument-arizona.htm).
- **Yosemite** (Gletschertreppe): [USGS PP 160](https://www.nps.gov/parkhistory/online_books/geology/publications/pp/160/contents.htm).
- **Niagara**: [Wikipedia](https://en.wikipedia.org/wiki/Niagara_Falls).
- **Aareschlucht / Breitachklamm / Partnachklamm**: [Übersicht](https://www.indenbergen.de/weblog/ueberblick-uber-die-schoensten-klammen-in-den-alpen/).
- **Geirangerfjord / Sieben Schwestern** (fjord).
- **Lydford Gorge** (Strudellöcher, heide).

Spiele (Ferat: kreativ, an realen Orten und diesen Spielen orientieren):

| Spiel / Ort | Was wir übernehmen | Link |
|---|---|---|
| **Witcher 3 – Skellige** | Geschichtete, halb vergrabene Felsen mit Moos obenauf. CDPR hat einzelne Felsen auch als Klippen verwendet. Eine Schichtneigung je Wand. Vorbild für fjord, kueste, bergwald, frost. | [80.lv World Building of Witcher 3](https://80.lv/articles/world-building-of-witcher-3), [Wiki Skellige](https://witcher.fandom.com/wiki/Skellige) |
| **Witcher 3 – Velen** | Flache Waldbäche mit Holzstufen, Wurzeln und Schlamm, Steilheit nur kurz (aue, sumpf, elfenwald). | [Wiki Velen](https://witcher.fandom.com/wiki/Velen) |
| **DA:I – Emerald Graves** | Riesenbäume und Elfenruinen, Fall an einer Ruine: Fall und Bauwerk kombinieren (elfenwald). | [Game Informer 2014](https://gameinformer.com/games/dragon_age_inquisition/b/playstation4/archive/2014/05/13/history-of-the-elves-explored-in-new-screens.aspx), [Wiki](https://dragonage.fandom.com/wiki/Emerald_Graves) |
| **DA:I – Hinterlands** | Hügelwald mit Felsriegeln und kleinen Fällen (bergwald, aue). | [Wiki](https://dragonage.fandom.com/wiki/The_Hinterlands) |
| **RDR2 – Brandywine Drop** | Fall unter einer Brücke, begehbarer Raum hinter dem Vorhang. | [Spielführer](https://gameskeys.net/brandywine-drop-treasure-location-guide-red-dead-online/) |
| **RDR2 – Elysian Pool** | Fall mit Höhle dahinter. | [Spielführer](https://rankedboost.com/red-dead-redemption-2/elysian-pool/) |
| **RDR2 – Donner Falls, Strawberry** | Fall an der Brücke, Fall mitten im Ort: Wasser als Ortsmotiv. | [Übersicht](https://www.sideshow.com/blog/best-views-destinations-red-dead-redemption-2) |

Die Fandom-Links folgen dem Wiki-Schema, ich konnte sie nicht öffnen (DNS). Bewusst **nicht** verlinkt ist ein PDF „The Art of Dragon Age
Inquisition“, das auf fremden Domains liegt (wahrscheinlich unerlaubte Kopie).

---

## 5. Probe an den Daten (grob, ohne Knickpunkt-Bündelung)

Ich habe die Regeln aus 2.3 grob durchgerechnet: ganze Strecke mit mittlerem S, ohne Fälle zu bündeln.

| Lauf | Art | B | S | L | Stufen | D je Stufe | Art |
|---|---|---|---|---|---|---|---|
| B_R_P4_M2_04 (H3) | Bach | 4,2 m | 23 % | 4,7 m | 123 | 1,0 m | stufe |
| B_K8_ELFENFALL_01 (H3) | Bach | 5,5 m | 26 % | 5,7 m | 79 | 1,4 m | stufe |
| B_K1_WASSERFALL_WEST_01 (B4) | Bach | 5,8 m | 17 % | 8,0 m | 35 | 1,2 m | stufe |
| F_ERLENBACH_1V_C2 | Fluss | 11,2 m | 31 % | 11,2 m | 16 | 3,3 m | fall |
| F_ELFENFLUSS_3_H4 | Fluss | 33,9 m | 11 % | 33,9 m | 12 | 3,1 m | fall |

- Über alle 161 Strecken ergeben sich ~2 300 Stufen: 87 Strecken mit Blockstufen, 58 mit Schnellen, 16 mit Fällen.
- Das ist viel. Der Planer muss Fälle bündeln (2.5) und Holz-, Kaskaden- und Schnellenstrecken zusammenfassen. Effekte nur an jeder 2.–3. Stufe.
- Abgleich: Der handgebaute C2-Lauf (12 Stufen, 1,8–5,3 m, 7–8 m Abstand) liegt nahe an der Regel (16 Stufen à 3,3 m auf 11 m Abstand).

---

## 6. Was nur Annahme ist (vor dem Pilot im Bild prüfen)

- **Formelform des Stufenabstands:** Faktor 0,4 und Exponent −0,7. Der Bereich 1–4 B ist belegt, die Form nicht.
- **Alle Grenzen über 6,5 % (Bach) bzw. 4 % (Fluss):** 30 % und 60 % sind Ferats Vorschlag. Die Literatur sagt nur „Fels- und
  Hangschuttgerinne überwiegen“.
- **Einzelfall-Kriterium:** S_lok ≥ 0,6, D ≥ 4 m (Fels 2 m), Bündelung 3 B, höchstens 25 m je Fall, Kettenglied ~8 m.
- **Kolktiefe unter Fällen** (0,3 D + 0,5): Die Literatur nennt nur die Richtung und Maxima um 10 m. Die Strahlgeschwindigkeit v0 ebenso.
- **Klamm und Ufer:** S ≥ 0,30 bzw. 0,20, Eintiefung 3 bzw. 2 m, Wandlänge 3–4 D, Klemmblöcke (2 je 100 m), Strudelloch-Dichte (4 je 100 m).
  Belegt sind nur Formen und die Verhältnisse Tiefe/Breite bzw. Tiefe ≈ Ø.
- **Größen:** Blockfaktor B/6 (Klemmverhältnis), Sturzblöcke, Beckenkorn.
- **Lagen:** Gewichte und Radien, z. B. die Spritzzone 1,5 D.
- **Effekte:** Skalen-Referenzen und die Zuordnung der Klang-Cues (aus A14, ungeprüft).
- **Biome:** Netzwahl und Holzstufen-Anteile. Die Felstypen sind belegt, die Netze passen nach Maß und Ansicht in den Katalogen; im Editor
  sind sie nicht gesehen.

## Quellen

Kürzel wie in `gefaelle_regeln.json → quellen`. „Auszug“ = nur Suchmaschinen-Auszug gelesen.

- **MB1997** Montgomery & Buffington (1997): Channel-reach morphology in mountain drainage basins. GSA Bulletin 109(5): 596–611.
  [PDF USFS](https://www.fs.usda.gov/rm/boise/publications/watershed/rmrs_1997_montomeryr001.pdf) – Auszug + Lehrbuch (Poolabstände).
- **IP2004** Interpraevent 2004 (Tabelle nach MB1997: < 0,015 / 0,015–0,030 / 0,030–0,065 / > 0,065).
  [PDF](https://www.interpraevent.at/reference/media/1636/download/2004_1_III-343.pdf?v=1) – Auszug.
- **GRANT1990** Grant, Swanson & Wolman (1990): Pattern and origin of stepped-bed morphology in high-gradient streams, Western Cascades.
  GSA Bulletin 102: 340–352. [OSU](https://wpg.forestry.oregonstate.edu/node/729) – Auszug.
- **ABR1995** Abrahams, Li & Atkinson (1995): Step-pool streams: Adjustment to maximum flow resistance. WRR 31(10): 2593–2602.
  [doi](https://doi.org/10.1029/95WR01957) – Auszug.
- **CHIN1999** Chin (1999): Step-pool-Perioden 0,43–2,40 Breiten; The morphologic structure of step-pools in mountain streams,
  Geomorphology 27. [AJS-PDF](https://ajsonline.org/article/61660.pdf) – Auszug.
- **CW2005** Chin & Wohl (2005): Toward a theory for step pools in stream channels. Prog. Phys. Geogr. 29(3).
  [doi](https://doi.org/10.1191/0309133305pp449ra) – Lehrbuch.
- **CZ2007** Church & Zimmermann (2007): Form and stability of step-pool channels. WRR 43, W03415.
  [doi](https://doi.org/10.1029/2006WR005037) – Auszug.
- **RC2021** Richardson & Carling (2021): Step-pool-Experimente, H ≈ D100. [Southampton ePrints](https://eprints.soton.ac.uk/452478) – Auszug.
- **CURWOHL2003** Curran & Wohl (2003): Large woody debris and flow resistance in step-pool channels, Cascade Range. Geomorphology 51.
  [USGS](https://pubs.usgs.gov/publication/70182597) – Auszug.
- **LEO1969** Leopold (1969): The rapids and the pools – Grand Canyon. USGS PP 669-D. [USGS](https://pubs.usgs.gov/publication/pp669D) – Auszug.
- **SL2016** Scheingross & Lamb (2016): Sediment transport through self-adjusting, bedrock-walled waterfall plunge pools. JGR-ES 121.
  [PDF Caltech](https://lamb.caltech.edu/documents/19661/Scheingross_and_Lamb_2016_with_supp.pdf) – Auszug.
- **EGU2025** EGU Geomorphology Blog: Highlighting waterfalls. [Blog](https://blogs.egu.eu/divisions/gm/2025/09/29/highlighting-waterfalls/) – Auszug.
- **DAS2022** Das (2022): Plunge-pool-Daten von 7 Fällen in Ostindien. [Mendeley](https://data.mendeley.com/datasets/ws933yrxtw/1) –
  Zahlen nicht gelesen, gute Quelle zum Nachrechnen.
- **NIAGARA** Wikipedia „Niagara Falls“ (Deckschicht, Rückschreiten). [Link](https://en.wikipedia.org/wiki/Niagara_Falls) – Auszug.
- **HM2009** Hayakawa & Matsukura: Stabilität der Niagara-Wand. [PDF Tsukuba](https://tsukuba.repo.nii.ac.jp/record/21252/files/EG_116-1.pdf) – Auszug.
- **PEL2015** Pelletier u. a.: Controls on the geometry of potholes in bedrock channels.
  [U Arizona](https://experts.arizona.edu/en/publications/controls-on-the-geometry-of-potholes-in-bedrock-channels/) – Auszug.
- **JI2018** Ji u. a. (2018): Diameter–depth of potholes. [PDF](https://publications.polymtl.ca/4957/1/2018_Ji_Relationship_between_diameter_depth_potholes.pdf) – Auszug.
- **RC2005** Richardson & Carling (2005): A typology of sculpted forms in open bedrock channels. GSA Special Paper 392 – Titel.
- **SCREE** Wikipedia „Scree“ / Francou & Manté (Schutthalden ~35°). [Link](https://en.wikipedia.org/wiki/Scree) – Auszug.
- **KLAMMEN** Übersichten Aareschlucht, Breitachklamm, Partnachklamm.
  [indenbergen.de](https://www.indenbergen.de/weblog/ueberblick-uber-die-schoensten-klammen-in-den-alpen/) – Auszug, Angaben schwanken je Seite.
- **SVARTI** [Wikipedia Svartifoss](https://en.wikipedia.org/wiki/Svartifoss) · **IGUAZU** [IUGS](https://iugs-geoheritage.org/geoheritage_sites/iguazu-iguacu-waterfalls/) ·
  **PLITVICE** [Poster](https://www.pmf.unizg.hr/images/50025872/2019_7.%20PLITVICE%20LAKES%20poster.pdf) ·
  **KRKA** [NP Krka](https://npkrka.hr/en_us/en_US/posjeti/sadrzaji/skradinski-buk/) ·
  **HAVASU** [Earth Magazine](https://www.earthmagazine.org/article/travels-geology-havasu-canyon-land-blue-green-water/) – alle Auszug.
- **LM1985** Laity & Malin (1985): Sapping processes and the development of theater-headed valley networks on the Colorado Plateau.
  GSA Bulletin 96(2) – Auszug (die Bandangabe schwankt in den Auszügen).
- **NPS_NAVAJO** [NPS Geodiversity Atlas Navajo NM](https://www.nps.gov/articles/nps-geodiversity-atlas-navajo-national-monument-arizona.htm) – Auszug.
- **YOSEMITE** Matthes (1930), USGS PP 160. [NPS-Onlinebuch](https://www.nps.gov/parkhistory/online_books/geology/publications/pp/160/contents.htm) – Auszug.
- **SPRAY_BC** Waterfalls and Biodiversity in BC / Wells-Gray-Bericht (Coxson; Goward & Björk).
  [UBC](https://www.geog.ubc.ca/biodiversity/WaterfallsandBiodiversityinBC.html) – Auszug.
- **PHYS** Wurfparabel/freier Fall – Lehrbuch.
- Repo: **A12** `12-recherche-wasser-gpu-schatten.md` Teil A · **A14** `14-wasser-fx.md` · **A5** `klippennetze-a5.md` ·
  **FORMAT** `vorlagen/SEHENS_FORMAT.md`, `FORMAT.md`.
