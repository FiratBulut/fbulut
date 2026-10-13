# 16h Nachtrag 2 – Ergebnisse TL, T0, Kasten-Statistik; Antworten auf eure Rückfragen (13.10.2026, 12:00)

Bezug: eure Antwort `antworten/16h-erlenbach-p2-talkaskade-ufer-wasser.md` (b12cc00).

## 1. TL – Bach-Werte im Landschaftsmaterial (global, nur Speicher, wieder zurück)

Gesetzt waren `Ufer_Staerke` 0,25, `Ufer_Farbe` (0,60; 0,62; 0,60), `Nass_Abdunkeln` 0,40 und `Nass_Breite_cm` 50.
Uferband-Höhe und Normal-Z sind im Material fest verdrahtet, keine Parameter. Bild: `bilder/swr_p2/tl_landschaft_bachwerte.jpg`.

**Ergebnis:**
- **Das Bett wird nicht grau.** An zwei von vier Stellen ist es kaum verändert. Bei t500 wird es sogar **oranger**, weil statt der hellen
  Kies-Ersetzung nun die Bachdekor-Lagen durchkommen:
  - Kies = `T_ground_big_pebbles_01` (Environment_Set),
  - Geroell = `T_ground_stones_01` (Mountain_Environment_Set).
- **Hauptgrund: die Tal-Tönung aus Houdini** (Lagen `Toenung_R/G/B`, 64 = neutral, `ToenungStaerke` 0,5).
  - Entlang Talkaskade und Kiesbett: R 66–79, G 43–47, B 30–34, also Faktor etwa (1,1; 0,72; 0,53).
  - Mit Stärke 0,5 bleibt (1,05; 0,86; 0,77): alles wird orange.
  - Das gilt für das ganze Tal, auch 40–80 m vom alten Fluss entfernt (R 64, G 47, B 37). Es ist also kein Rest der alten Flüsse.
  - Zum Vergleich: Bergrinne (43; 49; 36), Weltmittel (61; 59; 54).
- Folgerung: Der Kanal „Bachgewicht“ lohnt nur, wenn er auch die **Tönung unter und am Wasser** zurücknimmt, und/oder graue Bachgrund-Texturen
  nimmt. Nur Ufer-Stärke und -Farbe ändern zu wenig.

**Frage TL:**
1. Soll die Tönung unter dem Spiegel und im Uferband (z. B. bis 0,5 m über dem Spiegel) auf neutral gehen?
2. Welche Texturen für den nassen Bachgrund? Bitte aus dem Inventar wählen: `export/unreal/welt/inventar/` bzw. eure Liste aus Auftrag 13d.

## 2. T0 – Zerlegung Wasser (kumulativ, an t430/t500)

Bild: `bilder/swr_p2/t0_zerlegung.jpg`.

| Stufe | Änderung | Ergebnis |
|---|---|---|
| a | Glas (Absorption 100 000, Streuung A 0, Schaum 0, ELD-Schaum 0) | **schon goldbraun** |
| b | Absorption 222/1000/1250 | gleich |
| c | Streuung A 0,1 | gleich, **nicht milchig** bei 0,5 m |
| d | Foam Opacity 0,5 | gleich |
| e | ELD_Schaum_Deckkraft 1 | gleich |
| f | Refraction 1,0 statt 1,15 | etwas weniger Verzerrung, Farbe gleich |

**Antwort Rückfrage 2:**
- Keine Stufe bringt das Gold. Es liegt im Grund (Lagen-Texturen × Tönung × warmes Licht).
- Streuung A 0,1 macht bei 0,5 m nichts sichtbar milchig. A ist also nicht „je cm“, oder es wirkt sehr schwach.
- Variante F bleibt gesetzt.

## 3. Kasten-Statistik (Rückfrage 4) – Querschnitte alle 2 m

Daten: `antworten/fluss_sim/p2_lokal/querschnitte_p2.json`:
- 788 Querschnitte, je Seite ab der Wasserkante, d/z in 0,5-m-Schritten,
- Wasserkante = erster Punkt mit Gelände ≥ Plan-Spiegel,
- Höhen = `welt/hoehe.f32` vom 13.10.

Dazu `kasten_statistik_p2.json` und das Bild `bilder/swr_p2/kasten_statistik_p2.png`. Gerechnet mit eurer Referenz `kasten_hoehe` (45°) und
`boeschung_zuruecklegen` (32°, Korridor 4 m).

| Abschnitt | Querschnitte | Kästen > 0,6 m | max | Mittel | Abtrag beim Zurücklegen |
|---|---|---|---|---|---|
| Bergrinne | 200 | 93 (46,5 %) | 9,07 m | 1,44 m | 113 m³ |
| Durchbruch | 190 | 34 (17,9 %), nur s 199–270 | 6,50 m | 0,61 m | 23 m³ |
| Talkaskade | 190 | 32 (16,8 %), nur s 500–575 | 2,70 m | 0,27 m | 76 m³ |
| Kiesbett | 148 | 0 | – | – | – |
| Mündung | 60 | 0 | – | – | – |

Die Felsrinne (Bergrinne) und der Anfang des Durchbruchs sind nach eurer Regel Fels- bzw. Durchbruch-Ausnahmen. Echte Kästen in
Lockermaterial gibt es also nur in der **unteren Talkaskade (s 500–575)**.

**Frage C:** Zurücklegen nur dort (76 m³), oder auch Teile von Bergrinne und Durchbruch, wo das Gelände vor dem Graben kein Fels war? Eine
Lagen-Prüfung „Fels/Felsplatte ≥ 50 % vor dem Graben“ kann ich je Querschnitt liefern.

## 4. Erledigt seit eurer Antwort

- **B.6:** `C2_Flussfels_006` und `_002` entfernt. Die Akteur-Pakete sind gesichert in `Sicherung/C2_Flussfels_2026-10-13`. Die übrigen 14 und
  die Klänge sind noch offen.
- **Teil A:**
  - Datensatz `sehens_einbau/altbett_p2` gerechnet: eure Bänder; „Umgebung“ = Füllung aus natürlichen Zellen ≥ 30 m von anderem Wasser,
    Kies ≤ 5 % und Geröll ≤ 10 %, dazu Rest-Schotterflecken; Gras × `gras_dichte_faktor`.
  - Prüfung: 0 Kies-Bänder > 8 × 20 m außerhalb 0–6 m.
  - Die Kette schreibt gerade C2/D2. Bilder folgen.
  - Abweichung von euch: Der Median-Ansatz „30–60 m, ±15 m Höhe, Neigungsklasse“ ist durch die Box-Füllung ersetzt, weil die nahe
    Umgebung im Kiesbett selbst Schotter ist (Ufer der C3-Bäche). Ohne Kappe kamen dort 60 % Kies heraus.
- **Rückfrage 6 (Mündung):** p2 erreicht den C3-Lauf `F_ERLENBACH_2_C3` bei **s ≈ 748 m**. Dort ist der Abstand zur C3-Mitte gleich seiner
  halben Breite (18 m). Ab s 760 liegt p2 in der C3-Mitte. Der C3-Spiegel (wasser_welt.json) liegt 0,9 m über dem p2-Spiegel bei s 740.
  Ein Bild der Mündung folgt.
