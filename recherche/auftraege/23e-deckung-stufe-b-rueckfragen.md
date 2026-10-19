# Auftrag 23e – T23d-D gerechnet, Stufe B, T23-0 Fassung 2, Rückfragen

Stand 19.10.2026, 02:20 PC-Uhr. Bezug: Antwort 23d (8dce6ec), Regeln 23.4 (eingefroren als `regeln_23d_1efa9f8e`). Rolle 1, offline.
Selbsttests mit 23.4: 23 `64a654746495eca8`, 23b `dabb50741db8b9ac`, 23c `b4ebdb213b2f71ba`.

## 1. T23d-D Deckung C2 als Vereinigung

Kontrollfall bestanden: alle 12 Planwerte höchstens 0,004 vom Soll (Kante 0,882/0,849, ohne Platten 0,232/0,226).

| Zustand | Kante links | Kante rechts |
|---|---:|---:|
| A alt | 0,89 | 0,87 |
| B Neuplanung | 0,17 | 0,14 |
| C + Hindernis offen | 0,32 | 0,31 |
| D + Lage (sichtbar) | 0,47 | – |

- Die Kantenzone ist zu 66 % sichtbar nass (Wasser-Wahrheit v3: 93–95 %), 33 % der Fläche sind steiler als 38°; dort darf keine Lage hin.
- Ufer mit Lage 0,76/0,71 (Ziel 0,75).
- **Der lokale Vorschlag mit 1 155 Lagen wird abgelehnt:** Zonenziele nicht erreicht; zu viele K1-Netze (18–20 je 10 m statt ≤ 10); Anteil Stücke
  ≥ 1 m an der neuen Netzfläche 0.
- **Fehlbetrag für den Planer-Neulauf** (Stücke ≥ 1 m je 10 m und Seite): Kante 6,9/6,8 (≈ 260 gesamt), Ufer 0/1,5 (≈ 30), Hang 13,4/12,1 (≈ 480).

## 2. Stufe B (Punktwolken aus dem Editor, 142 Netze in C2)

FEHLER in C2: Stufe A 23.1 21 496 → Stufe A 23.4 21 476 → **Stufe B 23.4 21 628**. 116 Felsen kippen in Stufe B von ok nach FEHLER, fast alle mit
„Lücke/Deckung“, obwohl sie in Stufe A eingegraben sind (Beispiel C2:1989: A −31,6 cm, B +39,3 cm). Ursache: Die untere Hülle runder Netze steigt im Kern
stark an – bei 40 von 91 Netzen liegen mehr als 50 % der Zellen über 5 cm über dem tiefsten Punkt.

## 3. T23-0 Fassung 2

K31 als eigene Testlandschaft mit Sattel-Quad (8 × 8 Stützpunkte, Skala 100/100/128, zwei gegenüberliegende Ecken +80 cm, Collision Mip 0;
Erwartung an drei Proben: unsere Diagonale 80/40/40 cm, andere Diagonale 0/0/0, bilinear 40/30/30). K32 Stein auf Blockecke außerhalb der
Kern-Ellipse → FEHLER Lücke 170,4 cm. K10 jetzt FEHLER Lücke statt Schwerpunkt (Referenz prüft den Schwerpunkt nur bei aufliegenden Stücken).

## 4. Rückfragen

1. **Lücke in Stufe B:** Wie messen bei runden Unterseiten – Perzentil der Unterseiten-Zellen (welches?) oder nur bodennahe Zellen (Abstand zum
   tiefsten Punkt ≤ x cm)? Sonst werden eingegrabene Felsen zu FEHLER.
2. **Kante fast ganz nass:** Wie die Kantendeckung 0,75 erreichen, wenn 66–95 % der Kante sichtbar nass sind und ein Drittel steiler als 38° ist?
   Gilt das Kantenziel nur für trockene Zellen, oder sollen große Steine ins Wasser (Dachziegel, Keystones)?
3. **K1-Grenze (≤ 10 je 10 m):** Schon die Ersatz-Kiesel reißen sie. Gilt sie je Zone oder je Seite, und zählen Kiesel unter Wasser mit?
4. **0,55 m² Fußabdruck je Stück ≥ 1 m:** Woher stammt der Wert, soll der Planer damit die Stückzahl aus dem Fehlbetrag rechnen?
5. **Planausgaben für Misch-Kürzel fehlen** (Herkunft nur 55,5 % eindeutig, 252 594 Instanzen ohne Treffer): Sollen diese Fenster ohne Herkunft
   nach Fenster-Regeln behandelt werden, oder erst die alten Planer erneut laufen lassen, um ihre Ausgaben zu rekonstruieren?
