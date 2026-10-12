# Antwort Auftrag 17 – Woher kommt das Wasser unserer Wasserfälle?

Stand 12.10.2026. Ferat: „Unsere Wasserfälle tauchen aus dem Nichts auf.“ Dieser Bericht erklärt, woher Wasserfälle in der Natur ihr
Wasser bekommen. Er prüft alle Fälle unserer Pläne mit dem Gelände (2-m-Daten) und schlägt je Fall eine Lösung vor. Dazu kommt eine Prüferregel.
**Nichts davon ist in einen Planer eingebaut.** Das ist der Folgeauftrag.

| Ergebnis | Pfad |
|---|---|
| Vorschlagsdaten je Fall (Lage, Bewertung, Einzugsgebiet, Maßnahmen, Oberlauf-Punkte) | [`wasserherkunft/faelle_herkunft.json`](wasserherkunft/faelle_herkunft.json) |
| Übersichtskarte (Fälle farbig nach Bewertung, Landmassen) | [`wasserherkunft/faelle_herkunft.png`](wasserherkunft/faelle_herkunft.png) |
| Analyse (deterministisch), Regeln, Prüfer-Vorschlag | [`skripte/wasserherkunft/`](skripte/wasserherkunft/README.md) |

**Quellenlage:** Aus der Cloud ließ sich keine Webseite direkt abrufen (DNS gesperrt). Die Belege im Fachteil stammen deshalb aus
Suchmaschinen-Auszügen der verlinkten Seiten. Zahlen zu unserer Welt sind eigene Rechnungen (Abschnitt 3). Wo etwas Annahme ist, steht es dabei.

---

## 1. Kurzfazit

- **In der Natur kommt Wasser nie aus dem Nichts.** Jeder Fall hat oben etwas, das das Wasser liefert oder speichert:
  1. ein Einzugsgebiet mit Bach,
  2. einen See oder ein Moor,
  3. Schnee oder einen Gletscher,
  4. eine Quelle in der Wand (Gestein speichert Regen),
  5. auf Inselbergen zusätzlich Wolken und Nebel.

  Man **sieht** das fast immer: als Rinne oder Kerbe in der Kante, als Moos- und Nässestreifen, als Sinter, als Schneefeld oder als Karsee.
- **Unsere 178 Fälle:**

  | Bewertung | Anzahl | Anteil |
  |---|---|---|
  | plausibel | 69 | 39 % |
  | fragwürdig | 78 | 44 % |
  | **taucht aus dem Nichts auf** | **31** | **17 %** |

  Zum Bestand: 2 Welt-Wasserfälle, 16 Sehens-Wasserfälle und 160 Vorhang-Fälle aus dem fluss_sim-Export. 10 weitere Vorhänge
  sind dieselben Kanten wie ein Sehens- oder Welt-Wasserfall und zählen deshalb nicht doppelt.
- **Am schlimmsten trifft es die auffälligen Fälle.**
  - **Beide großen Welt-Wasserfälle sind „aus dem Nichts“.** WF_K1 hat 59 m Fallhöhe und ist 15 m breit (Hauptfluss). WF_K8 hat 54 m und
    ist 17 m breit (Elfenfluss). Über der Kante liegt nur 115 m bzw. 76 m Wasser. Dann endet der Fluss mitten im Tal. Das Einzugsgebiet ist
    2,6 ha bzw. 6,5 ha groß. Für einen 15-m-Vorhang wären mit Spielfaktor etwa 30 ha nötig, real 300 ha.
  - **13 der 16 Sehens-Wasserfälle sind „aus dem Nichts“.** Darunter sind:
    - die fünf Fallbänder der Schleierwand (Fjord, 200–230 m, Einzugsgebiet je ≤ 0,04 ha),
    - die Turmquelle (Dschungel, 60 m),
    - der Seefall (Küste, 54 m),
    - der Schleierfall der Klemmblock-Klamm.
- **Der Hauptgrund ist das zu kleine Einzugsgebiet, nicht die Planer-Geometrie.** Der Median liegt bei 0,7 ha. Bei 103 der 178 Fälle reicht
  der mittlere Abfluss nicht einmal für ein Zehntel des Vorhangs (V < 0,05).
  - Real braucht ein Schleierfall rund 0,1–1 km² Einzugsgebiet, ein mittlerer Fall 1–30 km² (Abschnitt 2.3).
  - Unsere Inseln sind 20,5 km² und 11,1 km² groß. Echte Ströme gehen da nicht, kleine Fälle schon, wenn man die Herkunft **zeigt**.
- **Inseln:** Die ganze Welt besteht aus Inseln. Kein Land berührt den Weltrand.
  - Hauptland: 20,5 km², höchster Punkt 684 m.
  - Ostinsel `INSEL_01`: 11,1 km², 489 m, Elfenwald, Dschungel und Heide.
  - 21 kleine Inseln, darunter eine Gletscherinsel mit 213 m.

  Auf der Ostinsel liegen 38 Fälle (17 plausibel, 15 fragwürdig, 6 aus dem Nichts), darunter WF_K8 und die Turmquelle. Für diese
  Inselberge passt Ferats Erklärung: Steigungsregen und Nebel am Gipfel.
- **Lösungen** (Abschnitt 4), nach Klasse:
  - **Quellaustritt in der Wand** mit Nass-, Moos- und Sinterstreifen, wenn oben kein Tal ist: 13 Fälle.
  - **Oberlauf ergänzen** (Bach-Spline bis in die Mulde, Vorschlagspunkte im JSON): 8 Fälle.
  - **Schneefeld oder Firn oberhalb** in Gletscher, Fjord, Frost und Tundra: 62 Fälle.
  - **Fall verkleinern** (Schleier statt Vorhang): 19 Fälle.
  - **Kar oder Rinne formen**: 6 Fälle.
  - **Karsee oder Moor**: 1 Fall.
  - **Gipfelnebel** als Zusatz: 45 Fälle.
- **Regel für die Zukunft** (Abschnitt 5): Ein Fall braucht eine **nachweisbare Herkunft**. Das heißt: ein Mindest-Einzugsgebiet nach Breite und
  Biom, **und** sichtbares Wasser von mindestens 30 m oberhalb oder ein Quellmerkmal. Ein Prüfer-Vorschlag liegt bei.

---

## 2. Woher Wasserfälle ihr Wasser bekommen

### 2.1 Die Quelltypen – kurz und mit Bildidee

| Herkunft | Was passiert | Echtes Beispiel | Bildidee für uns |
|---|---|---|---|
| **Regen-Einzugsgebiet** | Regen fällt auf eine Fläche. Alles, was nicht verdunstet, sammelt sich in Rinnen zum Bach. Je größer die Fläche, desto mehr Wasser. | fast jeder Mittelgebirgsfall | V-Kerbe in der Kante, ein Bach mit Ufervegetation führt von hinten heran, Rinnen am Hang darüber |
| **Steigungsregen (Luv)** | Feuchte Luft wird am Berg hochgedrückt, kühlt ab und regnet sich aus. Die Luvseite einer Insel bekommt ein Vielfaches. | Waiʻaleʻale (Kauai): langjährig ~10 m/Jahr (423 inch Mittel seit 1912, 30-Jahres-Mittel 2018 ~366 inch) [W1][W2] | Wolkenkappe am Gipfel, grüne nasse Luvseite mit vielen Fäden, trockene Leeseite |
| **Nebel / Wolkenwald** | Bäume und Heide kämmen Wolkenwasser aus. Es tropft als „Nebelniederschlag“ zu Boden. | Madeira: Lorbeerwald ~8 % zusätzlich zum Regen, Baumheide in Hochlagen deutlich mehr [N1][N2]. Erste Messungen nannten unter der Vegetation sogar das 3,5-Fache des Jahresniederschlags [N3] | Nebel hängt in den Kronen über der Kante, triefende Moose, Bartflechten, Tropfen an Blättern |
| **Schichtquelle** | Wasser sickert durch durchlässiges Gestein (Sandstein, poröse Lava, Kalk), bis es auf eine dichte Schicht trifft (Ton, Tuff, Basalt). Dort tritt es seitlich aus, oft als **Quellenlinie** entlang der ganzen Wand [Q1][Q2] | 25 Fontes, Madeira: ein „schwebender Grundwasserleiter“ (Paul-da-Serra-Hochfläche) schneidet die Talflanke an. Im Sommer fließt nur noch Grundwasser [M1][M2] | Waagrechtes nasses Band in der Wand, darunter viele Fäden, Moos- und Farnleiste genau auf der Linie, darüber trockener Fels |
| **Überlauf-/Überfallquelle** | Der Grundwasserleiter liegt in einer Mulde. Wo der Rand am tiefsten ist, läuft er über [Q2][Q3] | Quellen am Muldenrand im Kalkgebirge | Wasser kommt am tiefsten Punkt einer Felsschüssel heraus |
| **Karstquelle / Karstaufstoß** | Regen versickert auf einer großen Kalkfläche (Dolinen, Schlucklöcher) und fließt unterirdisch. Er tritt gebündelt aus, oft mit großer, stark schwankender Schüttung. Das unterirdische Einzugsgebiet kann viel größer sein als das sichtbare [Q4] | Blautopf, Aachtopf, Dschungelquellen in Kalktürmen | Wasser schießt aus einer Höhle oder einem Spalt mitten in der Wand. Darüber ist kein Bach nötig. Sinter- oder Tuffbart darunter |
| **Kalktuff / Sinter** | Kalkreiches Quellwasser gast CO₂ aus (Druck sinkt, Wasser wird wärmer, Verwirbelung am Fall). Moose und Algen entziehen CO₂. Kalk fällt aus und baut Stufen und Barrieren [K1][K2][K3] | Plitvice: Tuffbarrieren aus Moos und Kalk, die die Seen aufstauen und die Fälle bilden [P1][P2] | Helle, poröse, „tropfsteinartige“ Bärte, Moospolster mit Kalkkruste, terrassierte Becken |
| **Hängetal** | Ein Seitengletscher hat sein Tal weniger tief ausgeschürft als der Hauptgletscher. Das Seitental „hängt“ hoch über dem Trogtal. Sein Bach stürzt über die Trogwand [H1][H2] | Staubbach, Lauterbrunnen: 297 m aus einem Hängetal, gespeist von Schnee am Bietenhorn und Wyssbirg. Im trockenen Sommer bleibt nur ein Schleier [S1][S2] | Flache Talschulter oben mit Bach und Wiese, senkrechte Trogwand, Schleierfall, Schuttkegel unten |
| **Gletschertor / Schneefeld** | Schmelzwasser tritt am Gletscherende aus dem Tor oder läuft vom Schneefeld ab. Die Menge schwankt stark mit Tag und Jahr (Maximum Juni–August, nachmittags) [G1][G2][G3] | Svartifoss: Bach Stórilækur vom Rand des Vatnajökull, 20 m über Basaltsäulen [I1][I2]. Krimml: 110,7 km² Einzugsgebiet, davon 12 % Gletscher, ~5,6 m³/s [KR1][KR2] | Graues, trübes Wasser, Eisrand oder Schneefeld sichtbar über der Kante, Firnflecken in Rinnen |
| **See- oder Moorüberlauf** | Ein Kar- oder Moorsee speichert Wasser. Der Abfluss stürzt über die Karschwelle | Karsee-Abflüsse in den Alpen; Seljalandsfoss fällt von einer alten Küstenklippe. Der Seljalandsá kommt vom Eyjafjallajökull. Eine Quelle nennt auch Quellwasser unter Lava auf der Heide [I3][I4] | Seespiegel bis an die Schwelle, Abfluss durch eine Kerbe, Wollgras und Torfmoos oben |

### 2.2 Für Gestalter: Wie erkennt man im Bild, woher das Wasser kommt?

1. **Rinne oder Schlucht über der Kante.** Ein Bach gräbt sich rückwärts ein. Die Kante hat deshalb eine **Kerbe**, selten eine gerade Linie.
   Gerade, scharfe Kanten mit einem breiten Vorhang wirken künstlich.
2. **Vegetationsstreifen.** Entlang des Bachs oberhalb steht Ufergrün (Erlen, Weiden, Hochstauden). An einer Quelllinie in der Wand
   wachsen Moos, Farn und Lebermoos genau auf **einer** Höhe. Nur die Sprühzone unten ist rundum grün.
3. **Nasse Felsbänder.** Dunkle, glänzende Streifen beginnen an der Austrittslinie, nicht irgendwo. Darunter liegen oft Kalk- oder Eisenspuren
   (helle bzw. rostige Bärte).
4. **Sinter oder Kalktuff** an Quellaustritten im Kalk: helle, poröse Wülste, Moospolster mit Kruste.
5. **Speicher oben sichtbar**: Karsee, Moor, Schneefeld, Gletscherrand, Wolkenkappe.
6. **Größe passt zum Hinterland.** Ein breiter, schwerer Vorhang braucht einen Fluss, der von weit her kommt. Ein Schleierfall braucht nur
   einen Bach mit kleinem Kar.

### 2.3 Faustregeln: Einzugsgebiet und Abfluss

**Abfluss ≈ Niederschlag × Abflussbeiwert × Fläche.** Der Abflussbeiwert ist der Anteil, der nicht verdunstet: Wald 0,4–0,6, Fels und Eis
0,7–0,8. Die **Abflussspende** ist der Abfluss je km².

| Gebiet | Niederschlag | Beiwert (Annahme) | Abflussspende |
|---|---|---|---|
| Mittelgebirge | 1 000 mm/a (Schwarzwald 1 000–2 100 mm [R1]) | 0,5 | **≈ 16 l/(s·km²)** |
| Alpen | 2 000 mm/a | 0,7 | **≈ 44 l/(s·km²)** – Krimml real ≈ 51 (5,6 m³/s / 110,7 km² [KR1]) |
| Luv-Insel | 3 000 mm/a | 0,6 | **≈ 57 l/(s·km²)** |
| Luv-Insel, extrem (Waiʻaleʻale) | 10 000 mm/a | 0,7 | **≈ 222 l/(s·km²)** |

**Wie viel Wasser braucht ein Fall?**

Die Überfallformel nach Poleni lautet: q = ⅔·μ·√(2g)·h^1,5 je Meter Breite, mit μ ≈ 0,6 [U1][U2]. Daraus folgt:

- Schleier oder Fäden (h ≈ 5 mm): ≈ 0,6 l/s je Meter Breite.
- Geschlossener, dünner Vorhang (h ≈ 2 cm): ≈ **5 l/s je Meter Breite**.
- Kräftiger Fall (h ≈ 10 cm): ≈ 56 l/s je Meter Breite.

Ein 3 m breiter dünner Vorhang braucht also rund 15 l/s, ein 15 m breiter rund 75 l/s, kräftig rund 300 l/s.

| Fallklasse | mittlerer Abfluss | Einzugsgebiet Mittelgebirge | Alpen | Luv-Insel 3 000 mm | Luv-Insel 10 000 mm |
|---|---|---|---|---|---|
| **Schleierfall** (Fäden, ≤ 2 m) | 5–20 l/s | 0,3–1,3 km² | 0,1–0,45 km² | 0,09–0,35 km² | 0,02–0,09 km² |
| **mittlerer Fall** (geschlossenes Band 2–8 m) | 50–500 l/s | 3–32 km² | 1,1–11 km² | 0,9–9 km² | 0,2–2,3 km² |
| **Strom** (breiter Vorhang, Krimml, Niagara) | 1–10 m³/s und mehr | 63–630 km² | 23–230 km² | 18–175 km² | 4,5–45 km² |

**Für das Spiel:** Spielwelten sind verdichtet. Wege sind 3–5-mal kürzer als in echt, Flächen also 10–25-mal kleiner. Deshalb rechnen wir mit
**Spielfaktor 10**: Ein Fall wirkt glaubwürdig, wenn sein Einzugsgebiet mindestens ein Zehntel des echten Bedarfs liefert und die Herkunft
**sichtbar** ist. Zum Vergleich: 1 km² = 100 ha. Unsere Fälle haben im Median 0,7 ha.

### 2.4 Beispiele aus Spielen und echten Orten

**Echte Orte** (belegt):
- **Staubbach** (Lauterbrunnen) – Hängetal, Schneeschmelze, im Sommer fast nur Schleier [S1][S2].
- **Svartifoss** – Gletscherbach vom Vatnajökull über Basaltsäulen-Amphitheater [I1][I2].
- **Seljalandsfoss** – alte Meeresklippe, Fluss vom Eyjafjallajökull bzw. von der Heide darüber [I3][I4].
- **25 Fontes** (Madeira) – schwebender Grundwasserleiter tritt an der Talflanke aus, dazu Lorbeer-Nebelwald [M1][M2][N1].
- **Plitvice** – Kalktuff baut Barrieren und Fälle [P1][P2].
- **Krimml** – großer Gletscher-Einzugsbereich mit 110,7 km², 380 m in drei Stufen [KR1][KR2].

**Spiele** (nur Skyrim ist belegt, sonst eigene Beobachtung, bitte im Spiel gegenprüfen):
- **Skyrim**: Der White River hat seine Quelle sichtbar im Ilinalta-See. Das ist ein See als Speicher, die Fälle folgen flussab [GS1][GS2].
  Viele Fälle in den Bergen kommen sichtbar aus Schneefeldern. (Beobachtung)
- **The Witcher 3 (Skellige)**: Fälle auf Inselbergen mit Nebel und Wolken an den Gipfeln, meist mit sichtbarem Bach oberhalb. (Beobachtung,
  nicht belegt)
- **Red Dead Redemption 2**: Fälle in den Grizzlies werden von Schneefeldern und Bergbächen gespeist. Der Bach ist oberhalb verfolgbar.
  (Beobachtung, nicht belegt)
- **Ghost of Tsushima**: Fälle liegen in bewaldeten Kerbtälern. Ein Bach führt immer heran, oft mit Nebel. (Beobachtung, nicht belegt)

Ein Gegen-Rat aus der Teichgestaltung lautet, die Quelle „zu verstecken“ [D1]. Das gilt für künstliche Teiche, bei denen die Pumpe stört.
In einer offenen Welt sieht der Spieler von oben, dass nichts da ist. Deshalb zeigen wir die Quelle.

---

## 3. Befund unserer Fälle

### 3.1 Was gerechnet wurde

**Daten:** 2-m-Weltdaten wie in den bisherigen Läufen. Dazu frische Planer-Ausgaben dieses Stands im Scratchpad:
- Gefälle `--alle`,
- 15 Sehens-Planer,
- `bachbett_roh`,
- `fluss_sim_export` (Regeln v8).

Das ergibt 187 Gewässer und 762 Fälle, davon 170 mit Vorhang. Dazu kommen 16 Sehens-Wasserfälle (`wasser` vom Typ `wasserfall`) und
2 Welt-Wasserfälle (`wasser_welt.json`).

| Messgröße | Wie |
|---|---|
| **Einzugsgebiet** | D8 auf dem 2-m-Raster, Senken gefüllt (`sehens_lib.gelaende`). Die Lippe wird auf die Zelle mit der größten Akkumulation im Umkreis von 6 m geschnappt, nicht tiefer als 1,5 m unter der Lippe. |
| **Abfluss** | Summe über das Einzugsgebiet: Niederschlag × Beiwert je Biom (Tabelle in `wasserherkunft_regeln.json`, z. B. Bergwald 1 600 mm × 0,6, Dschungel 3 500 × 0,5, Fjord/Gletscher 2 500 × 0,8, Wüste 100 × 0,15). Dazu +15 % Nebel in Wald- und Inselbiomen über 120 m. |
| **Bedarf** | Poleni mit h = 2 cm über die Fallbreite (Vorhang- bzw. Strahlbreite aus dem Export, `breite_cm` der Sehens-Fälle, Breite aus `wasser_fx` für WF_K1/K8). **V = Abfluss / Bedarf.** |
| **Wasser oberhalb** | Lauflänge des Gewässers bis zur Lippe (Spline) bzw. Länge der Welt-Wasserfläche entlang der Tiefenlinie aufwärts. Es zählt das Längere. |
| **Gipfel über der Lippe** | höchster Punkt im Einzugsgebiet minus Lippe |
| **Rinne** | Tiefenlinie 10–120 m oberhalb, Median-TPI (Radius 15 m) ≤ −0,4 m |
| **Quellmerkmal** | See, Teich oder Sehens-See im Einzugsgebiet; Schnee oder Eis ≥ 2 000 m²; geplante Quelle (`bach.quelle`); Gewässer beginnt an See oder Topf |
| **Biom, Insel** | Biom an der Lippe; Landmassen auf 8-m-Raster |

**Bewertung:**
- **plausibel**: Herkunft sichtbar (Quellmerkmal **oder** ≥ 30 m Wasser oberhalb) **und** V ≥ 0,1 (Spielfaktor 10).
- **aus dem Nichts**: keine sichtbare Herkunft und V < 0,1. **Oder**: kein Quellmerkmal, V < 0,05 und weniger als 150 m Wasser oberhalb.
  Dann beginnt das Wasser kurz oberhalb ohne Quelle und ohne Einzugsgebiet.
- **fragwürdig**: der Rest. Meist ist die Herkunft sichtbar, aber die Menge viel zu klein.

### 3.2 Zahlen

| | plausibel | fragwürdig | aus dem Nichts | Summe |
|---|---|---|---|---|
| Welt-Wasserfälle (WF_K1, WF_K8) | 0 | 0 | **2** | 2 |
| Sehens-Wasserfälle | 0 | 3 | **13** | 16 |
| Vorhang-Fälle (fluss_sim) | 69 | 75 | **16** | 160 |
| **Summe** | **69** | **78** | **31** | **178** |
| davon Hauptland | 52 | 63 | 25 | 140 |
| davon Ostinsel (`INSEL_01`) | 17 | 15 | 6 | 38 |

Weitere Zahlen:
- **Einzugsgebiet:** Median 0,7 ha. 96 Fälle haben unter 1 ha, 40 unter 0,1 ha. Das größte sind 23 ha (Elfentreppe).
- **Menge:** Bei 69 Fällen passt sie (V ≥ 0,1). Bei 6 ist sie knapp (0,05–0,1). Bei **103 ist sie viel zu klein** (V < 0,05). Davon haben
  94 eine sichtbare Herkunft, nur die Menge stimmt nicht.
- **Herkunft:** 15 Fälle haben überhaupt keine sichtbare Herkunft (kein Quellmerkmal, < 30 m Wasser oberhalb). 64 Fälle haben weniger als
  30 m Wasser oberhalb.
- **Quelle kurz vor dem Fall:** Von allen 762 Fällen des Exports liegen **173 (in 61 Gewässern) weniger als 30 m unter der Quelle ihres
  Gewässers**, davon 48 mit Vorhang. Am häufigsten betrifft das die Sehens-Bäche:
  - Lawinenkegel (Gletscher),
  - Farnschlucht (Elfenwald),
  - Firnrinnsal (Gletscher),
  - Fließtreppe (Tundra),
  - Karsee-Zuläufe (Bergwald).

  Dazu kommen Welt-Bäche `B_R_P0_P2_06`, `B_R2_R_P0_P2_03`, `B_R_M2_P1_01` und `B_K1_WASSERFALL_WEST_01–03`
  (`faelle_quelle_kurz_oberhalb` im JSON).
- **Mündung „Wasserfall“:** Nur ein Gewässer mündet in einen Wasserfall, `F_HAUPTFLUSS_1` in WF_K1. Es ist ein **30-m-Stück**, 108 bis
  78 m vor der Kante. Drei Gewässer **beginnen** an einem Welt-Wasserfall:
  - `F_HAUPTFLUSS_1` und `F_HAUPTFLUSS_2` an WF_K1,
  - `F_ELFENFLUSS` an WF_K8.

  Unter den Fällen geht es also weiter, über ihnen fast nicht.

### 3.3 Welt- und Sehens-Wasserfälle (einzeln)

Spalten:
- EZG: Einzugsgebiet.
- Abfluss: mittlerer Abfluss.
- Bedarf: Bedarf eines dünnen Vorhangs (h = 2 cm).
- Wasser oben: sichtbares Wasser oberhalb der Lippe.

| Fall | Feld | Biom / Land | Fall × Breite (m) | EZG ha | Abfluss l/s | Bedarf l/s | V | Wasser oben m | Gipfel über Lippe m | Rinne | Quellmerkmal | Bewertung | Maßnahmen |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `WF_K1` | B4 | bergwald / Hauptland | 59 × 14,9 | 2,62 | 0,92 | 74,7 | 0,012 | 115 | 317 | ja | – | **aus dem Nichts** | Oberlauf + verkleinern + Gipfelnebel |
| `WF_K8` | H4 | elfenwald / Ostinsel | 54 × 16,6 | 6,53 | 2,57 | 83,2 | 0,031 | 76 | 361 | ja | – | **aus dem Nichts** | Oberlauf + verkleinern + Gipfelnebel |
| `bergwald_05_klemmblock_klamm/schleierfall` | I4 | bergwald / Ostinsel | 30 × 3,5 | 0,04 | 0,01 | 17,5 | 0,001 | 0 | 113 | nein | – | **aus dem Nichts** | Quellaustritt Wand + verkleinern + Gipfelnebel |
| `gletscher_05_die_waechte/muehlenfall` | E1 | gletscher / Hauptland | 4 × 1,0 | 0,00 | 0,00 | 5,0 | 0,001 | 54 | 7 | nein | Quelle geplant | fragwürdig | Schneefeld + verkleinern |
| `gletscher_06_gletschertoepfe/topffall` | E2 | gletscher / Hauptland | 20 × 1,6 | 0,00 | 0,00 | 8,0 | 0,000 | 49 | 16 | nein | – | **aus dem Nichts** | Schneefeld + verkleinern |
| `canyon_04_fluesterschlucht/spaltfall` | D4 | canyon / Hauptland | 12 × 2,5 | 4,13 | 0,14 | 12,5 | 0,011 | 129 | 60 | ja | – | **aus dem Nichts** | Karsee/Moor + verkleinern |
| `canyon_07_smaragdgumpe/fadenfall` | D4 | canyon / Hauptland | 35 × 5,0 | 5,30 | 0,20 | 25,1 | 0,008 | 95 | 49 | nein | See im EZG | fragwürdig | verkleinern |
| `heide_06_der_wollsackfall/fall3` | G5 | heide / Ostinsel | 1 × 3,0 | 0,85 | 0,14 | 15,0 | 0,009 | 137 | 25 | ja | – | **aus dem Nichts** | Oberlauf + Karsee/Moor + verkleinern |
| `elfenwald_05_farnschlucht/tropfwand` | H3 | elfenwald / Ostinsel | 12 × 2,2 | 0,06 | 0,02 | 11,0 | 0,002 | 0 | 62 | nein | – | **aus dem Nichts** | Quellaustritt Wand + verkleinern + Sinter |
| `dschungel_02_turmquelle/turmquelle` | G6 | dschungel / Ostinsel | 60 × 6,0 | 0,02 | 0,01 | 30,1 | 0,000 | 0 | 64 | nein | – | **aus dem Nichts** | Quellaustritt Wand + verkleinern + Sinter |
| `kueste_04_der_seefall/seefall` | A5 | kueste / Hauptland | 54 × 5,0 | 0,34 | 0,09 | 25,1 | 0,003 | 10 | 373 | nein | – | **aus dem Nichts** | Oberlauf + Kar/Rinne formen + verkleinern + Gipfelnebel |
| `frost_01_der_eisfall/restwasser` | E2 | frost / Hauptland | 17 × 0,6 | 0,00 | 0,00 | 3,0 | 0,000 | 0 | 8 | nein | – | **aus dem Nichts** | Quellaustritt Wand + Schneefeld + verkleinern |
| `fjord_02_schleierwand/fall1` | C2 | fjord / Hauptland | 228 × 1,2 | 0,02 | 0,01 | 6,0 | 0,002 | 0 | 74 | nein | – | **aus dem Nichts** | Quellaustritt Wand + Schneefeld + verkleinern |
| `fjord_02_schleierwand/fall2` | C2 | fjord / Hauptland | 213 × 0,7 | 0,03 | 0,02 | 3,5 | 0,006 | 0 | 76 | nein | – | **aus dem Nichts** | Quellaustritt Wand + Schneefeld + verkleinern |
| `fjord_02_schleierwand/fall3` | C2 | fjord / Hauptland | 227 × 1,5 | 0,02 | 0,01 | 7,5 | 0,001 | 0 | 73 | nein | – | **aus dem Nichts** | Quellaustritt Wand + Schneefeld + verkleinern |
| `fjord_02_schleierwand/fall4` | C2 | fjord / Hauptland | 204 × 1,0 | 0,04 | 0,03 | 5,0 | 0,005 | 0 | 70 | nein | – | **aus dem Nichts** | Quellaustritt Wand + Schneefeld + verkleinern |
| `fjord_02_schleierwand/fall5` | C2 | fjord / Hauptland | 227 × 0,6 | 0,02 | 0,01 | 3,0 | 0,003 | 0 | 65 | nein | – | **aus dem Nichts** | Quellaustritt Wand + Schneefeld + verkleinern |
| `fjord_04_haengetal/lippenfall` | D2 | fjord / Hauptland | 33 × 2,5 | 0,77 | 0,49 | 12,5 | 0,039 | 39 | 227 | ja | Quelle geplant | fragwürdig | Schneefeld + Kar/Rinne formen + verkleinern + Gipfelnebel |

Was die Tabelle zeigt:
- **WF_K1 und WF_K8** liegen in Houdini-Kacheln. Der Fluss oberhalb ist nur ein Stück im Kachelrand. Das Gelände hat eine Rinne (Tal), aber
  kein Wasser darin. Darüber steigt ein steiler Berg 317 m bzw. 361 m an.
- Der **Oberlauf-Vorschlag** folgt der Tiefenlinie bis zur Quellmulde:
  - WF_K1: 135 m weiter, +138 m Höhe.
  - WF_K8: 228 m weiter, +203 m Höhe.

  Das Einzugsgebiet bleibt trotzdem klein. Deshalb gehören **Gipfelnebel** und ein **schmalerer Fall** dazu. Zur Größenordnung:
  - WF_K1 liefert 0,9 l/s, das reicht real für 0,2 m Vorhangbreite.
  - Mit Spielfaktor 10 sind es rund 2 m Breite.
  - Zusätzlich kann ein **Karsee oder ein Schneefeld in der Mulde** als Speicher dienen.
- **Schleierwand (Fjord):** Die Lippen liegen auf einer Wandkrone. Darüber steigt das Gelände noch 65–76 m an, aber ohne Tal.
  Das passt zum Bild „Quelllinie in der Wand“: ein Schmelzwasser- oder Schichtquellband unter einem Firnfeld auf der Hochfläche.
  Der Katalog nennt als Vorbild die Sieben Schwestern und den Mardalsfossen.
- **Turmquelle (Dschungel)** und **Tropfwand (Farnschlucht):** Ein Bach oben ist hier falsch. Richtig ist eine **Karstquelle** mit Höhle
  oder Spalt in der Wand und **Sinterbart**. Ihr Wasser kommt unterirdisch aus der Fläche (Abschnitt 2.1). Die Fallbreite muss dann aber
  zum Quelltopf passen: 1–2 m statt 6 m.
- **Seefall (Küste):** Der Bach kommt erst 10 m vor der Kante aus dem Nichts. Die Tiefenlinie führt 168 m bergauf zu einer Mulde
  (Vorschlagspunkte im JSON).
- **Spaltfall (Canyon):** Der Spaltbach ist 129 m lang, hat aber keine Quelle. Canyon-Biom heißt: wenig Regen. Ein Karsee oder ein Moor in der
  Hochfläche, besser noch eine **Karstquelle** am Bachanfang, macht ihn glaubhaft.

### 3.4 Vorhang-Fälle aus dem fluss_sim-Export (je Gewässer)

| Gewässer | Vorhang-Fälle | plausibel / fragwürdig / Nichts | Biom / Land | EZG ha (min–max) | V (min–max) | Wasser oben m (min) | Anfang | Hauptmaßnahme |
|---|---|---|---|---|---|---|---|---|
| `B_K8_ELFENFALL_01` | 4 | 4 / 0 / 0 | elfenwald / Ostinsel | 2,99–6,09 | 0,174–0,283 | 59 | quelle | – |
| `B_R2_R_P4_M2_01` | 2 | 1 / 1 / 0 | elfenwald / Ostinsel | 1,24–5,63 | 0,080–0,429 | 98 | quelle | Oberlauf |
| `B_R_M2_P1_01` | 2 | 2 / 0 / 0 | bergwald / Hauptland | 3,83–3,83 | 0,251–0,289 | 151 | quelle | – |
| `B_R_M2_P1_02` | 4 | 0 / 0 / 4 | bergwald / Hauptland | 0,34–0,50 | 0,020–0,030 | 23 | quelle | verkleinern |
| `B_R_M3_M2_01` | 5 | 5 / 0 / 0 | bergwald / Hauptland | 6,64–7,40 | 0,349–0,572 | 266 | quelle | – |
| `B_R_P0_M2_02` | 2 | 0 / 0 / 2 | tundra / Hauptland | 0,11–0,22 | 0,003–0,004 | 16 | quelle | Quellaustritt Wand |
| `B_R_P0_M2_03` | 2 | 0 / 0 / 2 | tundra / Hauptland | 1,35–1,67 | 0,039–0,044 | 50 | quelle | Oberlauf |
| `B_R_P4_M2_01` | 1 | 0 / 0 / 1 | elfenwald / Ostinsel | 0,82–0,82 | 0,070–0,070 | 15 | quelle | Oberlauf |
| `B_R_P4_M2_04` | 7 | 7 / 0 / 0 | elfenwald / Ostinsel | 2,50–4,22 | 0,177–0,341 | 89 | quelle | – |
| `B_R_P5_P1_04` | 1 | 1 / 0 / 0 | dschungel / Ostinsel | 1,44–1,44 | 0,145–0,145 | 56 | quelle | – |
| `F_ERLENBACH` | 4 | 0 / 2 / 2 | tundra / Hauptland | 1,42–2,40 | 0,013–0,030 | 110 | quelle | Schneefeld |
| `SW_aue_07_blautopf_quellbach` | 1 | 0 / 1 / 0 | aue / Ostinsel | 1,12–1,12 | 0,015–0,015 | 18 | topf | verkleinern |
| `SW_bergwald_05_klemmblock_klamm_klammbach` | 3 | 0 / 3 / 0 | bergwald / Ostinsel | 0,66–0,68 | 0,028–0,029 | 12 | topf | verkleinern |
| `SW_bergwald_06_karsee_abfluss` | 8 | 8 / 0 / 0 | bergwald / Hauptland | 4,14–6,41 | 0,128–0,199 | 139 | see | – |
| `SW_bergwald_06_karsee_zulauf_sued` | 6 | 0 / 6 / 0 | bergwald / Hauptland | 0,68–0,70 | 0,041–0,042 | 0 | quelle | Kar/Rinne formen |
| `SW_bergwald_06_karsee_zulauf_west` | 6 | 6 / 0 / 0 | bergwald / Hauptland | 3,30–4,02 | 0,200–0,244 | 90 | quelle | – |
| `SW_elfenwald_04_elfentreppe_zulauf` | 4 | 4 / 0 / 0 | elfenwald / Ostinsel | 20,65–23,04 | 1,234–1,364 | 600 | quelle | – |
| `SW_elfenwald_05_farnschlucht_tobelbach` | 10 | 0 / 10 / 0 | elfenwald / Ostinsel | 0,37–0,69 | 0,020–0,036 | 10 | quelle | verkleinern |
| `SW_fjord_02_schleierwand_abfluss1` | 13 | 13 / 0 / 0 | fjord / Hauptland | 1,49–1,99 | 0,198–0,265 | 9 | topf | – |
| `SW_fjord_02_schleierwand_abfluss3` | 13 | 0 / 13 / 0 | fjord / Hauptland | 0,41–0,51 | 0,024–0,052 | 10 | topf | Schneefeld |
| `SW_fjord_02_schleierwand_abfluss4` | 15 | 10 / 5 / 0 | fjord / Hauptland | 0,00–2,90 | 0,001–0,387 | 8 | topf | Schneefeld |
| `SW_fjord_04_haengetal_hochtalbach` | 2 | 2 / 0 / 0 | fjord / Hauptland | 2,72–2,80 | 0,153–0,228 | 49 | quelle | – |
| `SW_frost_03_eisvorhang_sickerlinie` | 1 | 0 / 1 / 0 | frost / Hauptland | 0,01–0,01 | 0,001–0,001 | 10 | quelle | Schneefeld |
| `SW_gletscher_01_gletschertor_gletscherbach` | 1 | 0 / 1 / 0 | gletscher / Hauptland | 0,03–0,03 | 0,001–0,001 | 43 | quelle | Schneefeld |
| `SW_gletscher_02_lawinenkegel_schmelz_mitte` | 3 | 0 / 3 / 0 | gletscher / Hauptland | 0,02–0,02 | 0,006–0,006 | 0 | quelle | Schneefeld |
| `SW_gletscher_02_lawinenkegel_schmelz_ost` | 6 | 0 / 6 / 0 | gletscher / Hauptland | 0,04–0,08 | 0,009–0,018 | 0 | quelle | Schneefeld |
| `SW_gletscher_03_moraenensee_firnrinnsal` | 6 | 0 / 6 / 0 | gletscher / Hauptland | 0,03–0,05 | 0,009–0,013 | 0 | quelle | Schneefeld |
| `SW_gletscher_03_moraenensee_seeabfluss` | 9 | 0 / 9 / 0 | gletscher / Hauptland | 0,06–0,26 | 0,010–0,043 | 34 | see | Schneefeld |
| `SW_gletscher_06_gletschertoepfe_klammbach_oben` | 14 | 6 / 3 / 5 | gletscher / Hauptland | 0,00–5,97 | 0,000–0,590 | 8 | quelle | Schneefeld |
| `SW_tundra_04_die_fliesstreppe_schmelzfaden` | 3 | 0 / 3 / 0 | tundra / Hauptland | 0,01–0,04 | 0,001–0,004 | 42 | quelle | Schneefeld |
| `SW_tundra_05_der_trunkene_grund_abfluss` | 1 | 0 / 1 / 0 | tundra / Hauptland | 2,15–2,15 | 0,056–0,056 | 6 | see | Schneefeld |
| `SW_wueste_04_quelloase_rinnsal` | 1 | 0 / 1 / 0 | wueste / Hauptland | 0,43–0,43 | 0,000–0,000 | 12 | topf | verkleinern |

Was die Tabelle zeigt:
- **Plausibel** sind die Gewässer mit echtem Hinterland:
  - Karsee-Abfluss und westlicher Zulauf (Bergwald),
  - Elfentreppe (23 ha, Welt-Bach 600 m oberhalb),
  - die Elfenfall-Bäche der Ostinsel,
  - `B_R_M3_M2_01` (7 ha),
  - der Hängetal-Hochtalbach.
- **Gletscher, Fjord, Frost und Tundra:** Viele kleine Kaskaden mit Vorhang haben Einzugsgebiete unter 0,1 ha (Lawinenkegel, Firnrinnsal,
  Fließtreppe). Bei Schmelzwasser ist das erlaubt, **wenn das Schneefeld oder der Firn darüber sichtbar ist**. Darum heißt die Hauptmaßnahme
  dort „Schneefeld“. Sonst lieber Fäden statt Vorhang.
- **`F_ERLENBACH` (gebaute C2-Kaskade):** Das Wasser reicht schon bis in die Quellmulde (`wasser_reicht_bis_mulde`). Ein Oberlauf hilft hier
  nicht. Die Tundra (600 mm) liefert zu wenig Wasser. Abhilfe ist ein Schneetälchen oder ein Firnrest in der Mulde, oder kleinere Vorhänge.
  Die Kaskade ist schon gebaut. Das ist ein Hinweis, kein Umbau-Zwang.
- **Wüsten-Oase:** Eine Oasenquelle wird in der Natur von fernem Grundwasser gespeist, nicht vom Regen vor Ort. Der Quelltopf ist als Merkmal
  richtig. Nur der 1-m-Vorhang ist zu groß: Rinnsal statt Vorhang.

---

## 4. Lösungen je Klasse

Die Kennungen stehen in `faelle_herkunft.json` unter `massnahmen`. Die erste ist die Hauptmaßnahme, die übrigen sind Zusätze. Die Zahlen nennen,
wie oft eine Maßnahme Hauptmaßnahme ist.

| Kennung | Wann | Umsetzung (konkret) | Hauptmaßnahme bei |
|---|---|---|---|
| `quellaustritt_felswand` | Kein Tal über der Kante. Der Fall hängt an einer Wand oder einem Turm. | Ein **waagrechtes Quellband** 2–10 m unter der Kante: Decal-Streifen „nass“ (`MI_Leakage_*`), darüber trocken. Moos- und Farnleiste auf genau dieser Höhe (Lage Moos, `SM_MossClump_*`, `SM_EagleFern_*`). Der Vorhang beginnt **am Band**, nicht an der Kante. Im Kalk (Dschungel, Canyon, Elfenwald, Heide) ein **Spalt oder Höhlenmund** und ein heller **Sinterbart** darunter (Decal oder Lage, Vorbild Plitvice). Breite ≤ 2 m. | 13 (Schleierwand ×5, Turmquelle, Klemmblock-Schleier, Farnschlucht-Tropfwand, Eisfall, `B_R_P0_M2_02` …) |
| `oberlauf_ergaenzen` | Tiefenlinie oberhalb vorhanden, aber trocken | **Bach-Spline** entlang `oberlauf.punkte_cm` (ab dem Ende des vorhandenen Wassers, alle 10 m, bis zur Quellmulde mit Einzugsfläche < 1 500 m²). Der Oberlauf ist schmal (0,5–1,5 m), mit Stufen. Am Ende eine **Quellmulde**: Moospolster, Quelltopf, Sumpfgras. | 8 (WF_K1, WF_K8, Seefall, Wollsackfall, `B_R2_R_P4_M2_01`, `B_R_P0_M2_03` ×2, `B_R_P4_M2_01`) |
| `schneefeld_oberhalb` | Gletscher, Fjord, Frost, Tundra, oder Schnee im Einzugsgebiet | **Schneefeld oder Firnrest** in der Mulde bzw. auf der Hochfläche über der Kante (Lage Schnee/Eis, Megascans Snow Embankment). Ein Schmelzrinnsal läuft sichtbar zur Kante. Wasser leicht trüb. | 62 |
| `fall_verkleinern` | Herkunft sichtbar, Menge viel zu klein | Vorhang durch **Schleier oder Fäden** ersetzen. Breite = `breite_passend_m` × 10 (Spielfaktor). Oder den Fall flussab verlegen, wo mehr Einzugsgebiet ist. | 19 |
| `einzugsgebiet_formen` | Es fehlt höchstens das 3-Fache (mit Spielfaktor) | **Kar oder Rinne** über der Kante ins Gelände formen (Gelände-Stempel), damit die Tiefenlinie mehr Fläche sammelt. Zugleich die Kerbe in der Kante zeigen. | 6 (Karsee-Zulauf Süd …) |
| `karsee_moor_oberhalb` | Flaches Relief oberhalb | **Karsee oder Moor** als Speicher. Der Abfluss geht durch eine Kerbe an der Schwelle. Wollgras und Torfmoos. | 1 (Spaltfall) |
| `nebel_am_gipfel` | Nicht plausibel, Gipfel ≥ 80 m über der Lippe, Insel oder Wald-/Küstenbiom | **Lokaler Nebel** oder eine **Volumetric-Cloud-Kappe** am Gipfel bzw. Kamm über dem Einzugsgebiet. Nebel in den Kronen am Hang, wie im Nebelhain (`elfenwald_02_nebelhain`, Ostgrat der Ostinsel), der dieses Bild schon zeigt. Das erklärt das Wasser der Inselberge (Madeira-Prinzip). | Zusatz bei 45 |
| `sinter_kalktuff` | Quellaustritt im Kalk-Biom | Sinter- oder Tuffbart, Moos mit heller Kruste, kleine Tuffstufen im Becken | Zusatz |
| `nassstreifen_moos` | alle nicht plausiblen | Nass- und Moosstreifen entlang der Quelllinie und der Fallbahn | Zusatz |

**Je Fall** stehen im JSON:
- `bewertung`, `menge`, `herkunft_sichtbar`,
- `einzugsgebiet_m2`, `abfluss_mittel_l_s`, `bedarf_vorhang_l_s`, `verhaeltnis`, `breite_passend_m`,
- `wasser_oberhalb_m` (Plan bzw. Welt), `gipfel_ueber_lippe_m`, `rinne`, `quellmerkmale`, `biom`, `landmasse`,
- `massnahmen`, `empfehlung`.

Wo sinnvoll, steht dort auch `oberlauf` mit diesen Feldern:
- `punkte_cm` [x, y, z];
- `ende`: `mulde`, `kamm`, `anstieg_max`, `anschluss_wasser` oder `wasser_reicht_bis_mulde`;
- `ab_lippe_m`, `laenge_m`, `hoehe_gewinn_m`.

Nach `ende` aufgeteilt gibt es 34 Vorschläge: 12 bis zur Mulde, 13 bis zum Kamm, 3 brechen am Steilhang ab, 1 erreicht vorhandenes Wasser, und
bei 5 reicht das Wasser schon bis zur Mulde.

---

## 5. Regel für künftige Planung (Vorschlag)

**Prüferregel „nachweisbare Herkunft“.** Jeder Fall mit Vorhang, Sehens-Wasserfall oder Welt-Wasserfall muss diese Prüfungen bestehen:

| Code | Stufe | Bedingung |
|---|---|---|
| **H1** | FEHLER | **Herkunft sichtbar**: ≥ 30 m Wasser oberhalb der Lippe **oder** ein Quellmerkmal. Quellmerkmale sind: See, Teich oder Topf; Schnee oder Eis im Einzugsgebiet; geplante Quelle mit Quellmulde, Quellband oder Karstmund. Eine trockene Rinne reicht nicht. |
| **H2** | FEHLER | **Mindest-Einzugsgebiet** (ohne Quellmerkmal). Es gilt: Fläche ≥ Breite × 5 l/s je m × 0,1 ÷ Abflussspende des Bioms. Die Werte stehen in der Tabelle unten. |
| **H3** | WARNUNG | sonst V < 0,1: Der Prüfer nennt `breite_passend_m`. |
| **H4** | HINWEIS | Das Gewässer beginnt weniger als 30 m oberhalb der Lippe. |
| **H5** | HINWEIS | Nicht plausibel, Gipfel ≥ 80 m über der Lippe, Insel oder Wald-/Küstenbiom: Gipfelnebel vorschlagen. |

**Mindest-Einzugsgebiet in ha** (mit Spielfaktor 10, dünner Vorhang):

| Biom | 1 m breit | 3 m | 8 m | 15 m |
|---|---|---|---|---|
| Gletscher, Fjord | 0,8 | 2,4 | 6,3 | 12 |
| Dschungel | 0,9 | 2,7 | 7,2 | 14 |
| Elfenwald | 1,5 | 4,4 | 12 | 22 |
| Bergwald, Lava | 1,6 | 4,8 | 13 | 24 |
| Küste | 2,3 | 6,8 | 18 | 34 |
| Frost | 2,8 | 8,5 | 23 | 42 |
| Heide, Sumpf | 3,2–3,6 | 9,5–11 | 25–29 | 47–54 |
| Aue, Tundra | 4,4 | 13 | 35 | 66 |
| Canyon, Ödland, Wüste | 13–105 | 40–316 | – | – (nur mit Quelle) |

**Im Planer** (Folgeauftrag) heißt das:
- Ein Fall wird nur gesetzt, wenn H1 und H2 erfüllt sind.
- Sonst setzt der Planer automatisch eine der Maßnahmen aus Abschnitt 4: zuerst Quellmerkmal oder Oberlauf, dann Verkleinern.

Der Vorschlag liegt als
[`skripte/wasserherkunft/wasserherkunft_pruefen.py`](skripte/wasserherkunft/wasserherkunft_pruefen.py) bei. Er liest
`faelle_herkunft.json` und ist in keinen Planer eingebaut. Ergebnis auf dem heutigen Stand:
- FEHLER H1: 15
- FEHLER H2: 34
- WARNUNG H3: 75
- HINWEIS H4: 40
- HINWEIS H5: 45
- Exit-Code 1

---

## 6. Was lokal zu tun ist

1. **Nichts bauen.** Das hier sind Vorschlagsdaten.
2. **Optional mit 1 m prüfen.** Der Lauf ist auf 1 m nicht getestet. Vorher die Planer- und fluss_sim-Ausgaben auf 1 m erzeugen (siehe
   [fluss_sim-README](skripte/fluss_sim/README.md)). Dann:
   ```
   python -I recherche/antworten/skripte/wasserherkunft/wasserherkunft.py --daten1m export/unreal/welt \
          --fs export/unreal/welt/fluss_sim --sehens export/unreal/welt/sehens --aus export/unreal/welt/wasserherkunft --bild
   python -I recherche/antworten/skripte/wasserherkunft/wasserherkunft_pruefen.py export/unreal/welt/wasserherkunft/faelle_herkunft.json
   ```
3. **Im Editor ansehen** (Kameras der Sehens-Orte; Lage `lage.lippe_cm` im JSON):
   - WF_K1 (B4) und WF_K8 (H4): Sieht man von oben, dass der Fluss im Tal endet?
   - die Schleierwand (C2),
   - die Turmquelle (G6),
   - den Seefall (A5).
4. **Entscheiden** (Rückfragen unten): Spielfaktor, Niederschlag je Biom, bevorzugte Maßnahme je Klasse. Danach folgt der Planer-Einbau.

---

## 7. Quellen

Alle Belege stammen aus Suchmaschinen-Auszügen. Die Seiten selbst waren aus der Cloud nicht abrufbar.

**Niederschlag, Nebel, Abfluss**
- [W1] Wikipedia: Mount Waiʻaleʻale – https://en.wikipedia.org/wiki/Mount_Wai%CA%BBale%CA%BBale
- [W2] The Garden Island: Mittelwerte des USGS-Pegels Waiʻaleʻale – https://thegardenisland.com/?p=97394
- [N1] Figueira et al. 2013 (Lorbeerwald Madeira, Wolkenwasser ≈ 8 % des Regens) und Prada et al. 2009, Repositorium Univ. Madeira – https://digituma.uma.pt/entities/publication/c7541a8d-1e28-43b8-b6d3-fcd014506c6a
- [N2] Prada et al.: Fog precipitation and rainfall interception in the natural forests of Madeira – https://uon.sdsu.edu/prada_fog_precipitation.pdf
- [N3] Prada & da Silva 2001: Fog precipitation on the island of Madeira – https://www.fogquest.org/wp-content/uploads/2024/02/n-Prada-and-da-Silva-2001-Fog-precipitation.pdf
- [R1] LGRB Baden-Württemberg: Niederschlag Schwarzwald (1 100 bis 2 100 mm) – https://lgrbwissen.lgrb-bw.de/printpdf/14961
- [A1] Hydrologischer Atlas der Schweiz, Tafel 5.4 (mittlere Abflussspenden) – https://hydrologicalatlas.ch/products/printed-issue/rivers-and-lakes/plate-5-4 ; Tafel 6.4 („Wasserschloss Europas“) – https://hydrologischeratlas.ch/downloads/01/content/Text_Tafel64.de.pdf
- [U1] Poleni-Überfallformel (Lehrmaterial Sachsen) – https://bildungsportal.sachsen.de/opal/oer/8RCwGTxWabDo
- [U2] IAHR: Geschichte der Poleni-Formel – https://www.iahr.org/library/info?pid=17532

**Quelltypen, Karst, Sinter**
- [Q1] Spektrum Lexikon der Geowissenschaften: Schichtquelle – https://www.spektrum.de/lexikon/geowissenschaften/schichtquelle/14206
- [Q2] Spektrum: Quellentypen – https://www.spektrum.de/lexikon/geowissenschaften/quellentypen/13020
- [Q3] wissen.de: Quelle (Überfallquelle) – https://www.wissen.de/lexikon/quelle-geographie
- [Q4] Spektrum: Karstquelle – https://www.spektrum.de/lexikon/geowissenschaften/karstquelle/8112
- [Q5] BAFU: Typisierung von Grundwasserregimen an Quellen – https://www.Bafu.admin.ch/dam/bafu/de/dokumente/grundwasser/fachinfo-daten/grundwasserregime-quellen-2016.pdf.download.pdf/Typisierung_von_Grundwasserregimen_an_Quellen.pdf
- [K1] Bayerisches LfU, Geotope (Kalktuff) – https://www.lfu.bayern.de/geologie/bayerns_schoenste_geotope/19
- [K2] Geyer 2005: Karstquellen (ABU-Info) – https://www.abu-naturschutz.de/fileadmin/user_upload/Veroeffentlichungen/ABU_Info/2005/Geyer_2005_Karstquellen.pdf
- [K3] Land Niederösterreich: Kalktuffquellen – https://noe.gv.at/noe/Naturschutz/Kalktuffquellen.html?print=true
- [P1] NP Plitvicer Seen: How tufa is formed – https://np-plitvicka-jezera.hr/en/natural-and-cultural-heritage/natural-heritage/tufa/how-tufa-is-formed/
- [P2] UNESCO: Plitvice Lakes National Park – https://whc.unesco.org/en/list/98

**Hängetal, Gletscher, Orte**
- [H1] Spektrum: Hängetal – https://www.spektrum.de/lexikon/geowissenschaften/haengetal/6678
- [H2] Spektrum: Trogtal – https://www.spektrum.de/lexikon/geowissenschaften/trogtal/17001
- [S1] Wikipedia: Staubbach Falls – https://en.wikipedia.org/wiki/Staubbach_Falls
- [S2] Britannica: Staubbach Falls – https://www.Britannica.Com/place/Staubbach-Falls
- [G1] chemie.de: Gletscherbach (Tages- und Jahresgang) – https://www.chemie.de/lexikon/Gletscherbach.html
- [G2] Spektrum: Gletscherschmelzwasser – https://www.spektrum.de/lexikon/geowissenschaften/gletscherschmelzwasser/6066
- [G3] wissen.de: Gletschertor – https://www.wissen.de/rechtschreibung/gletschertor
- [I1] Wikipedia: Svartifoss – https://en.wikipedia.org/wiki/Svartifoss
- [I2] Iceland Travel Guide: Svartifoss (Stórilækur, Vatnajökull) – https://icelandtravelguide.is/locations/svartifoss-waterfall
- [I3] Katla Geopark: Seljalandsfoss und Gljúfrabúi (alte Meeresklippe) – https://katlageopark.com/geosites/mainly-geology/seljalandsfoss-and-gljufrabui
- [I4] WorldAtlas: Seljalandsfoss (Gletscher- oder Quellwasser) – https://www.worldatlas.com/falls/seljalandfoss.html
- [M1] Madeira Geodiversität: Geosite 25 Fontes – https://geodiversidade.madeira.gov.pt/en/geosites/madeira/calheta/c01-25-fontes
- [M2] Madeira Geodiversität: As 25 Fontes (PDF, schwebender Grundwasserleiter) – https://geodiversidade.madeira.gov.pt/images/122-As_25_Fontes.pdf
- [KR1] Krimmler Wasserfälle (offizielle Seite) – https://wasserfaelle-krimml.at/en/index.php?Itemid=124
- [KR2] EEA EUNIS: Krimml Falls natural site – https://eunis.eea.europa.eu/sites/AT940001

**Spiele, Gestaltung**
- [GS1] UESP: Lake Ilinalta (Quelle des White River) – https://content2.uesp.net/wiki/Skyrim:Lake_Ilinalta
- [GS2] UESP: Lore White River – https://content2.uesp.net/wiki/Lore:White_River
- [D1] WaterShapes 2002: Hidden sources (Bachquellen verstecken, Teichbau) – https://watershapes.com/images/archives/indexed/WaterShapes200204-dews-hidden-sources-hiding=stream-headwaters-naturalistic-pond-design.pdf

---

## 8. Rückfragen

1. **Spielfaktor 10:** Reicht dir „ein Zehntel des echten Wasserbedarfs“ als Glaubwürdigkeitsgrenze? Mit Faktor 3 wären nur noch 27
   statt 69 Fälle plausibel. Mit Faktor 30 kämen 26 dazu.
2. **Niederschlag je Biom** (`wasserherkunft_regeln.json`): Soll die **Ostinsel eine Luv-Insel** sein? Dann hätte sie z. B. 3 000–5 000 mm
   auf der Luvseite und Nebel. Das würde dort viele Fälle plausibel machen. WF_K8 käme bei 4 000 mm auf etwa V ≈ 0,07 statt 0,03. Wenn ja: Von welcher Seite kommt der Wind?
3. **WF_K1 und WF_K8:** Lieber den **Fluss nach oben verlängern** (135 m bzw. 228 m Oberlauf bis zur Mulde, mit Karsee oder Schneefeld als
   Speicher und Gipfelnebel)? Oder die **Fälle auf 2–5 m Breite** zurücknehmen (Schleier statt Vorhang)?
4. **Schleierwand (Fjord), fünf Bänder:** Passt ein **Firnfeld auf der Hochfläche** mit einer Quelllinie in der Wand? Oder lieber weniger
   Bänder (2 statt 5)?
5. **Turmquelle und Farnschlucht-Tropfwand:** Als **Karstquelle** aus Spalt oder Höhle mit Sinterbart umdeuten und schmaler machen (1–2 m)?
6. **Gletscher-, Tundra- und Frost-Kaskaden** (Lawinenkegel, Firnrinnsal, Fließtreppe): Soll dort ein **sichtbares Schneefeld** Pflicht
   werden? Oder sollen die Vorhänge an diesen sehr kleinen Rinnsalen wegfallen? Die Simulation zeichnet die Rinne ohnehin.
7. **Prüferregel:** Gehört H1/H2 als FEHLER in die Planer (Gefälle, Sehens) oder nur als WARNUNG in den fluss_sim-Prüfer? Die Vorhänge
   warten ja noch (16c).
