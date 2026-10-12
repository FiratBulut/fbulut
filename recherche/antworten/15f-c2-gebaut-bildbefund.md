# Antwort zu Auftrag 15f – C2 gebaut: Bildbefund (Schaum, Stufen zu regelmäßig, Beckenfarbe)

Stand 12.10.2026. Die Fassung ist Commit **`ae09234`**. Die C2-Vorfassung `72820d2` ist überholt; das Netz reicht
jetzt bis hinter die schrägen Abstürze.

## Kurzfazit

- **Schaum:** Schaum gibt es nur noch am Lippensaum (≤ 0,5 m), auf der Zunge in der Kerbe und im Aufprallkreis
  (≤ 30 % der Beckenlänge), sonst 0. Bei C2 hat jetzt 8 % der Netzfläche Schaum > 0,8, vorher 70 %.
  `Schaum_Menge` 0,15 / `Zungen_Schaum` 0,25 stehen als Empfehlung im Netz (`material_parameter`).
- **Stufen unregelmäßig (Hauptpunkt):**
  - **Lippen:** schräg (Mittel 20,5°, 89 % ≥ 15° über alle Strecken; C2 16,6°), gekrümmt, mit 1–2 Kerben für den
    Hauptstrahl. Teil-Lippen sind versetzt.
  - **Abstände und Höhen:** streuen ±40 %. Kaskaden sind Blockkaskaden mit ungleichen Teilhöhen (CV in C2 0,18,
    vorher 0,01).
  - **Rampen:** 97 eingestreute Rampen über alle Strecken.
  - **Breite:** Lippen eingeschnürt, Becken breiter.
  - **Blöcke und Holz:** Lippen dicht mit Blöcken besetzt, Kerben frei. Dazu Kies im Kolk und Totholz quer.
  - **Netz:** Das Kaskadennetz hat jetzt ein Querprofil (`quer`) mit Wasserhöhe, Deckung, Schaum und Tiefe je
    Stützpunkt. Die Zunge ist in der Kerbe deckend und an den Seiten dünn, sodass Fels durchscheint.
- **Beckenfarbe:** Der Planer liefert `tiefe_cm` je Stützpunkt (C2: Median 1,1 m, 0,55–1,6 m) und den Vorschlag
  Absorption/Streuung × clamp(Tiefe / 1,5 m; 0,35; 1). Flache Becken wirken damit heller.
- **Prüfungen:** Alle Regeln aus 15b–15e gelten weiter. Neu dazu: Querprofil-Prüfung und der HINWEIS
  „Regelmäßigkeit“.

  | Lauf | Läufe | FEHLER | WARNUNG | HINWEIS „Regelmäßigkeit“ |
  |---|---|---|---|---|
  | 19 Pilotläufe, `--hoehe1m-fenster` | 19 | 0 | 13 | 0; zweiter Lauf byteidentisch |
  | alle 161 Strecken, 2 m | 98 mit Stufen | 0 | 46 | 16, nur kurze Strecken mit wenigen Lippen |

- **Regelwerk:** `gefaelle_regeln.json` ist auf Wunsch des Koordinators ergänzt: neuer Block
  `stufen.unregelmaessig`, `stufen.zufall` 0,4/0,4, Lippenwinkel 60–120°.

## 1. Befunde und Änderungen

### 1.1 Schaum („weiße Betontreppe“)

**Ursache:** Schaum lag auf Lippe, Bogen und Wand immer bei 1. Dazu kam ein Aufprallkreis von 1–3 m mit 3 m
Auslauf. Bei Stufen alle 5–10 m überlappte das fast überall.

**Änderung:** Schaum je Querstützpunkt:

| Bereich | Kerbe (Hauptstrahl) | daneben |
|---|---|---|
| Lippensaum (0,5 m vor der Lippe) | 1 | 0,15 |
| Zunge | 1 | 0,1 |
| Aufprallkreis um den Strahl in der Kerbe | 1 | – |
| sonst | 0 | 0 |

- Der Aufprallkreis hat den Radius min(clamp(0,5 D + 0,5; 1; 3); 0,3 × Beckenlänge), mit 0,5 m Rand.
- Auf Rampen ist der Schaum leicht (0,3–0,7).
- Die Spalte `schaum` der Mittellinie ist der mittlere Querpunkt.

### 1.2 Stufen zu regelmäßig

1. **Lippen schräg, gekrümmt, mit Kerbe** (`lippen_geo`, `lippen_formen`).
   - Winkel 15–30° gegen quer, Vorzeichen zufällig. Pfeil 0,05–0,15 B mit Scheitel stromab.
   - Kerben: 1, ab B ≥ 6 m in 50 % der Fälle 2. Breite 0,2–0,35 B (0,8–3 m), Lage ±0,35 B, Krone in der Kerbe
     0,15–0,4 m tiefer.
   - Die Krone neben der Kerbe liegt 5 cm unter Wasser. Dort sieht man Fels durch dünnes Wasser.
   - Ein Lippenfeld `s_eff(s, u)` verschiebt den Spiegel quer zum Lauf. Gelände, Bett, Kolk, Uferring und
     Netzquerprofil rechnen alle damit.
   - Der Versatz zwischen Nachbarlippen ist auf 0,6 × Becken begrenzt. So bleibt der Spiegel je Längsstreifen
     monoton und jedes Becken erhalten.
   - Teil-Lippen einer Kaskade: gleiche Schrägrichtung, anderer Winkel, Kerbe auf der Gegenseite.
2. **Abstände und Höhen ±40 %.**
   - `stufen.zufall` steht auf 0,4/0,4, das Suchfenster für die nächste Lippe auf 0,6–1,4 L.
   - Kaskaden-Teilhöhen streuen ±45 %. Die Teil-Lippen liegen weiter dort, wo der alte Spiegel um die Summe gefallen
     ist; der Spiegel liegt also nie über dem alten.
   - 30 % der Teilstufen bis 0,8 m werden, wo Platz ist, zu einer Rampe (Schnelle, ≤ 35 %). Der Beckenfall wird auf
     die Rampe umgelegt, damit die nächste Lippe gleich hoch bleibt.
   - Gesamtfall, Becken ≤ 3 % und „Spiegel steigt nie“ bleiben geprüft.
3. **Lippen aus Blöcken** (`lippen_blockpunkte`).
   - Blöcke entlang der schrägen, gekrümmten Lippe im Abstand 0,75 × Blockgröße, Kerben frei.
   - Keystones an beiden Kerbenrändern; die Yaw-Ausrichtung folgt der Lippe.
   - Bei Fällen bilden die Riegel-Netze die Lippe auf dieselbe Weise.
4. **Blöcke im Becken, Kolk mit Kies, Totholz quer.**
   - Beckenblöcke: (b − a)/max(1,5 B; 4 m) statt /max(3 B; 6 m), Größe 0,4–1,3 m.
   - Kies im Kolk: Fächer, 6–30 Stück.
   - Totholz quer im Becken: 30 %, wo das Biom Holz hat und die Stufe keine Holzstufe ist.
   - Wasser-Gruppen halten 1 m Abstand zum Meer.
5. **Breite wechselt.** An den Lippen 0,8 B auf ±1,5 m, in den Becken 1,2 B. Die Breite ändert sich höchstens um
   0,4 m je m.
6. **Kaskadennetz-Querprofil.**
   - Zungen sind in der Kerbe deckend; daneben liegt `deckung` bei 0,15–0,35 (zufällig je Lippe).
   - Querschnitte alle 0,25 m um jede Lippe (`knick` = `uebergang`).
   - Das Netz reicht bis hinter den seitlich am weitesten verschobenen Absturz.

### 1.3 Beckenfarbe

`quer[..][3]` = `tiefe_cm` (Wasser über dem Bett). Vorschlag für das Material: Absorption_Faktor und
Streuung_Faktor × clamp(tiefe / 150 cm; 0,35; 1), dann sind flache Becken heller. Der Hinweis steht auch als
`farbe_hinweis` im Netz. Die Umrechnung aus dem Flussmaterial prüft Claude lokal.

## 2. Format für das Einbau-Werkzeug (Kaskadennetz)

| Feld | Inhalt |
|---|---|
| `mittellinie`, `knick` | wie bisher, `knick` zusätzlich `uebergang` |
| `mittellinie_s_m` | Laufkoordinate je Punkt |
| `quer` | je Punkt `quer_punkte` (11) Einträge `[dz_cm, deckung, schaum, tiefe_cm]` |
| `quer_lage` | Stützpunkt j bei u = (−1 + 2 j/(N − 1)) × (breite/2 + rand_ueberstand_m), u > 0 links in Fließrichtung, j = 0 rechts |
| `material_parameter` | {Schaum_Menge 0,15, Zungen_Schaum 0,25} |
| `farbe_hinweis`, `schaum_regel` | Text |

Je Stützpunkt bedeuten die Werte:

- Wasserhöhe = `z_cm` + `dz_cm`.
- Vertexfarbe B = `schaum`.
- `deckung` geht als Alpha bzw. Opacity in die Zunge. Bei Deckung < 0,3 darf das Netz dort auch fehlen.

Die Stufen haben im Plan neu:

- `lippe_form` mit `winkel_grad`, `pfeil_m`, `kerben` [{u_m, breite_m, tiefe_m}] und `seite_deckung`.
- Teilstufen bekommen `lippe_form`, `rampe` und `rampe_m`.
- `lippe_cm` folgt jetzt der schrägen, gekrümmten Lippe, `ueberfall_cm` liegt in der Hauptkerbe.

## 3. Vorbilder

| Vorbild | Was wir übernehmen |
|---|---|
| [Partnachklamm](https://de.wikipedia.org/wiki/Partnachklamm) (Garmisch) | enge Kalkklamm, das Wasser fällt in schmalen Strahlen über schräge Felskanten, dazwischen dunkle, ruhige Gumpen; Schaum nur am Strahl |
| [Johnston Canyon](https://en.wikipedia.org/wiki/Johnston_Canyon) (Banff) | Fallstufen mit Hauptstrahl an einer Seite der Kante, der Rest der Kante trocken oder nur benetzt; türkise Becken, flach heller |
| [Plitvicer Seen](https://de.wikipedia.org/wiki/Nationalpark_Plitvicer_Seen) (Kaskaden, Kalktuff) | viele Teilstufen unterschiedlicher Höhe, gekrümmte, bewachsene Barrieren, Wasser in vielen Einzelsträhnen; Becken klar und hell |
| Skellige-Bäche ([The Witcher 3](https://witcher.fandom.com/wiki/Skellige)) | Step-Pool-Bäche aus groben Blöcken: die Lippe ist eine Blockreihe mit Lücken, kein Beton; Totholz und Kies im Becken |
| Step-Pool-Literatur (MB1997, CHIN1999, CURWOHL2003; Belege in [`15-gefaelle-regelwerk.md`](15-gefaelle-regelwerk.md)) | Stufen = Blockriegel (Keystones), Abstände streuen, Holzstufen in Waldbächen |

## 4. C2-Kennzahlen (Cloud 2 m + 1-m-Fenster)

| Kennzahl | vorher (aaf330c) | nachher (ae09234) |
|---|---|---|
| Stufen / Lippen (inkl. Teil-Lippen) | 19 / 36 | 18 / 42 |
| Lippen schräg ≥ 10° | 0 % | 81 % (Mittel 16,6°, Streuung 17°) |
| CV Lippenabstände | 0,43 | 0,51 |
| CV Fallhöhen (alle Lippen) | 0,56 | 0,67 |
| CV Teilhöhen in Kaskaden (Mittel) | 0,01 | 0,18 |
| Rampen in Kaskaden | 0 | 1 |
| Schaum > 0,8, Netzfläche | 70 % (Mittellinie) | **8 %** (Querprofil) |
| Schaum > 0, Netzfläche | 100 % | 42 % (davon das meiste 0,1–0,15 an Lippensaum und Zunge) |
| Netzfläche mit Deckung < 0,5 (Fels scheint durch) | 0 % | 22 % |
| Netzpunkte KN0 | 286 | 776 (Querschnitte um die Lippen) |
| Instanzen / Akteure | 1 113 / 46 | 1 631 / 62 |

Die Lippen in C2 sind im Mittel weniger schräg als im Durchschnitt aller Strecken (16,6° gegen 20,5°). Grund: Die
Kaskaden-Teilbecken sind kurz, und der Versatz ist auf 0,6 × Becken begrenzt. Die ersten Lippen eines Segments
bleiben gerade, weil der Spiegel an der Segmentgrenze fest ist.

**Testbild:** `gefaelle/test_F_ERLENBACH_1V_C2_s1.png` zeigt die Draufsicht und das Längsprofil. Neu ist ein drittes
Feld: das Netz abgewickelt (x = s, y = quer) mit Wasser nach Deckung, Schaum weiß, Fels grau und den gelben,
schrägen, gekrümmten Lippen. Die grauen Querstreifen sind Zungen mit geringer Deckung, also Fels unter dünnem Wasser.

## 5. Grenzen und Hinweise

- **Uferproben an schrägen Lippen:** Eine Probe direkt neben einem schrägen Absturz (≤ 1,5 m stromab, ≤ 1 m stromauf
  auf dieser Seite) zählt wie ein Lippen- oder Fußpunkt (`pruefung.ufer_an_lippe`). Dort ist das Ufer die
  Seitenwand des Absturzes. Alle anderen Beckenpunkte werden auf 1 m streng geprüft.
- **Die Krone neben der Kerbe** wird nur abgegraben, nie aufgeschüttet. Wo das alte Gelände tiefer liegt, bilden die
  Lippenblöcke die sichtbare Kante.
- **Kurze Strecken mit 3–5 Lippen** können trotz Zufall gleichmäßig wirken (16 HINWEISE bei allen 161).
- **Regelwerk:** `gefaelle_regeln.json` wurde auf Wunsch des Koordinators geändert (sonst Regelwerk-Agent):
  - `stufen.zufall` 0,25/0,30 → 0,4/0,4
  - `stufen.lippe.winkel_zur_fliessrichtung` 75–105° → 60–120°
  - neuer Block `stufen.unregelmaessig`

## 6. Aufruf

```
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis . --laeufe F_ERLENBACH_1V_C2    # lokal 1 m
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --daten2m recherche/vorlagen/daten/sehens \
    --hoehe1m-fenster recherche/vorlagen/daten/gefaelle/hoehe_1m_fenster --aus <scratchpad>/a15f/plan --bild
```

## Nachtrag: dz-Sprünge im Querprofil (Befund Sehens-Agent)

**Kein Fehler im Plan, aber bitte `dz_cm` nicht auf 0 setzen.** Der Planer bleibt unverändert, C2 und die Piloten
bleiben wie in ae09234.

**Warum `dz_cm` springt:**
- `dz_cm` ist relativ zu `z_cm` des **eigenen** Netzpunkts.
- An einer Stufe liegen Lippe, Bogen, Wand und Fuß auf (fast) gleichem s, aber mit verschiedenem `z_cm`. Das ist die
  Fallkante der Mittellinie, bis zu 18 m an B_K8_ELFENFALL.
- Derselbe Querstützpunkt hat an diesen Punkten dieselbe **absolute** Wasserhöhe `z_cm + dz_cm`. Der relative Wert
  `dz_cm` unterscheidet sich deshalb genau um den Höhenunterschied der Mittellinie.
- Bei schrägen Lippen kreuzt ein Querschnitt die Lippe. Ein Teil liegt dann im Ober-, ein Teil im Unterwasser, und
  `dz_cm` springt innerhalb des Querschnitts um höchstens die Lippenhöhe. Das ist der schräge Vorhang, kein Riss.

**Nachgemessen (19 Pilotläufe, alle Netze):**

| Messung | Ergebnis |
|---|---|
| absolute Wasserhöhe zwischen Punkten mit gleichem s | Unterschied 0 cm |
| absolute Sprünge längs | nie größer als die größte Lippenhöhe des Netzes |
| größter relativer Sprung von `dz_cm` | 18,4 m an einem 18,5-m-Fall |

**Was `dz_cm = 0` bewirken würde:**
- Die Lippen wären wieder gerade quer zum Lauf.
- Das Netz passte nicht mehr zum schräg gestempelten Gelände. Der Prüfer meldet dann bei C2 „Wasserhöhe an Punkten mit
  gleichem s verschieden“ und einen Uferfehler.

**Für das Einbau-Werkzeug:**
- Vertexhöhe = `z_cm + dz_cm`.
- Querschnitte mit gleichem s ergeben Nullflächen; man kann sie zusammenlegen.

**Neue Prüferregel** (`gefaelle_pruefen.py`, Commit siehe unten):
- Die absolute Wasserhöhe `z + dz` muss an Punkten mit gleichem s gleich sein (≤ 1 cm).
- Sprünge längs und quer dürfen höchstens die größte Lippenhöhe des Netzes + 5 cm betragen.
- Ergebnis: Piloten auf 1 m und alle 161 auf 2 m 0 FEHLER. Ein Testplan mit `dz = 0` wird als FEHLER erkannt.
