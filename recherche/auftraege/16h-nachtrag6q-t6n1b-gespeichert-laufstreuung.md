# Nachtrag 16h-6q – T6N1b mit K-Kolk bestanden, gespeichert und nach Neuladen bestätigt; Laufstreuung ist global

Stand 19.10.2026, 06:05 PC-Uhr. Bezug: 16h-Nachtrag 6p (8455b38) §1–§4, 6o §4.2/§4.3.

## 1. Ergebnis T6N1b (Breite 1, Kette mit K-Kolk, unabhängig nachgeprüft: „freigegeben mit Bedingungen“)

| Tor | Wert | Grenze |
|---|---:|---|
| G1 Prüfband `sichtbar_5` | 10,70 % (T6M3A_2 10,70) | ≤ 16,0 |
| G3 Bett `nass_sim` | 99,84 % | ≥ 97 |
| Kernbett `sichtbar_1` | 100,0 %, 0 Fehlzellen | ≥ 99 |
| Front | 788,4 m | ≥ 788 |
| K-Kolk gegen T6M3A_2 | Median \|ΔW\| 0,00 cm; 0 Abweichungen > 4 cm; kein Kolk verlässt 0,8–1,35 m | ≤ 2 cm / ≤ 2 / keiner |

- Stabil nach zwei Messungen (größte Änderung 0,9 pp), Front 788 → 788 m.
- Licht vorher und nachher gleich (Sonne Neigung −24°, Richtung −20°, 100 000 lx, 5 900 K).
- Alle 20 Bilder angesehen:
  - K1: keine Treppe, keine Spalte.
  - Mündung: nicht schlechter. Die kantigen Wasserränder am roten Stein gibt es in beiden Fassungen.
  - Kolk 36 und Kolk 3: Die Stufen sind nass-dunkel statt weiß; das Wasser ist klarer.
- Bildpaare an Ferat: `bilder/swr_p2/t6n1b_bildpaare.jpg`.
- **Gespeichert** mit Speicherbeleg je Paket (SWR_Sim, SWR_Fluss, SWR_Arm). Grundlage: Ferats Pauschalfreigabe vom 18.10. 20:20 und eure Empfehlung 6p §2.
- **Danach harter Neustart ohne Speichern; nach erneutem Laden bestätigt:** Breite 1, BAKED_SIM, 0 ungespeichert, Pakete = Beleg, Bake bitgleich T6N1b_2.
- **Neuer gespeicherter Stand des Bachs C2:** smoothing_width 1, Dump `T6N1b_2`.

## 2. Befund zu 6p §3.3: Die Laufstreuung ist nicht örtlich begrenzt

Zwei Läufe mit denselben Eingaben sind nie bitgleich.

| Vergleich | nasse Texel mit Abweichung | davon > 4 cm | Maximum |
|---|---:|---:|---:|
| T6N1_2 − T6M3A_2 (Oberfläche W) | 17 168 von 70 523 | 610 | 56 cm |
| T6N1_2 − T6M3A_2 (Tiefenkanal G) | 52 934 von 70 523 | – | – |
| T6N2_2 − T6M3A_2 (W) | 13 429 | – | – |

- **Ort:** vor allem an der Mündung (s 700–788: 4 552 Texel über 1 cm) und in der Bergrinne. In der Talkaskade sind es nur 372 Texel über 1 cm
  bzw. 10 über 4 cm.
- An den Kolken wirkt W meist bitgleich. Das liegt an der Half-Float-Rundung (2-cm-Stufen); G weicht an drei Vierteln der nassen Texel ab.
- **Vermutung (ungeprüft):** Die Simulation hängt an der Bildrate bzw. am Zeitschritt des Editors.
- Für K-Kolk hatte das keine Folge.

## 3. Auslegung N2 (bitte bestätigen)

Unsere Kette wertet den „Zielbereich 0,8–1,35 m“ in K-Kolk wie G2′a: Kolke innerhalb einer Half-Float-Stufe Toleranz und die Gelände-Ausnahmen
{3, 30} zählen als im Ziel. 6p nennt die Toleranz nicht ausdrücklich. Bei T6N1b ohne Folge, auch bei strenger Lesart verlässt kein Kolk den Bereich.

## 4. Fragen

1. Reicht für künftige Läufe der Vergleich gegen einen Referenzlauf (K-Kolk), oder sollen wir die Laufstreuung selbst als Toleranz messen
   (z. B. zwei Läufe mit gleichen Eingaben, Streuung je Zone als Rauschband)?
2. Die Streuung sitzt an der Mündung (s 700–788). Spricht das für eine Ursache im Übergang zum C3-Fluss (Senke/Nachfüllen), die man festhalten sollte?
3. Gilt der neue Stand (Breite 1) jetzt als Bezug für die Zonen der Steinplanung (23e/23f: Nachrechnung, Planer neu, wenn sich die Kante im Median
   um mehr als 0,3 m verschiebt)?
