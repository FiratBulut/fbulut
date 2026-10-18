# 16h Nachtrag 6l – Schritt 1 (6k §2.6) ausgeführt: formal „uneindeutig“, Profil s 439, Editor-Landschaft geprüft

Stand 18.10.2026, 13:30 PC-Uhr. Bezug: Antwort 6k (9f18c4f). Kein Editor-Test nach eurer Regel „uneindeutig → Profil, kein Editor-Test“.
Einzige Editor-Handlung: ein reiner Lesetest der Landschaftshöhen (§4), nichts gespeichert.

## 1. Ergebnis Schritt 1

- `boden_befund.py --selbsttest`: 7/7, „bestanden“, Ausgabe zeichengleich mit eurer Antwort. `boden_modelle.py` ebenfalls zeichengleich.
  Beide wörtlich aus dem Code-Abschnitt übernommen.
- Welt-1-m-Raster des Prüfbands (Fenster i0 1666, j0 2943, 174 × 69), `--zelle 1.0`:

  | Dump | Urteil |
  |---|---|
  | Basis 0,3 frisch (T6JB0_2) | ERSATZWERT hinter der Spline-Breite |
  | T6j-C (T6JC_2) | GLÄTTUNG des Bodens |

  → verschieden, keines DECKEL, Erfolgskriterium nicht erfüllt.
- **DECKEL scheitert nur an „eng“:** Boden − Spline an Bandzellen mit Gelände > Spline + 0,15 m: p10/p50/p90 = −28,7/+4,2/+41,7 cm bzw.
  −30,4/+2,0/+40,9 cm. Spanne 70/71 cm, verlangt ≤ 15 cm. Alle anderen DECKEL-Zeichen erfüllt: r(Versatz; Gelände − Spline) −0,823/−0,825,
  Band-Median −63,0/−64,7 cm, Bett −1,2 cm, Median Boden − Spline +2 bis +4 cm.
- **GLÄTTUNG** knapp: r_Laplace 0,504 (T6JB0_2: 0,499), Schwelle 0,5. Im nativen Sim-Raster (0,367 m) 0,35. Kontrollfall: Schon das Umtasten auf 1 m
  ergibt 0,48 ohne jeden Versatz.
- **ERSATZWERT** ist nur der Rückfall über den Sprung innen/außen (−50 cm). Die Reichweite des Deckels ist bei Spline Bett + 0,5 m und Bett + 2 m gleich.
- Die 70 cm Streuung sind echt: Ein injizierter DECKEL wird im 1-m-Raster mit der Abtastung des Dumps erkannt (Spanne ≤ 8 cm, 9/9 Kontrollfälle);
  im nativen Raster ist die Spanne ebenfalls 69–71 cm.

**DECKEL-Vorhersage gegen Messung** (Boden − Gelände im Band, cm):

| Größe | Vorhersage (Plan, c = 3 cm) | gemessen B0 / C | Deckel-Modell auf echtem hoehe.f32 |
|---|---|---|---|
| 0,25–1 m Median | −30 ± 10 | −29,8 / −32,4 | −27,9 |
| 1–2 m Median | −94 ± 15 | −81,7 / −82,3 | −83,3 |
| p10 | −149 ± 20 | −120,6 / −121,7 | −129,4 |
| p90 | ≈ 0 | +0,4 / +0,1 | 0 |

Zusatzbefunde (offline):
- Der Deckel reicht etwa 3 m hinter die Plan-Bettkante, in beiden Dumps gleich: gedeckelt 72 % der Zellen bei Kante 0,5–1 m, 48–55 % bei
  2–2,5 m, unter 15 % ab 3 m.
- Streuung Boden − Spline: in flachen Becken 33–36 cm, an Stufen und Rampen 78–82 cm. 21 flache Zellen liegen in beiden Dumps genau auf Spline + 2 bis 6 cm.
- Ausgeschlossen: ältere Geländestände (vor Auftrag 230 und vier weitere; höchstens 12,5 % der Zellen innerhalb 10 cm), andere Bezugsflächen
  (alte Spline, eigene Splinelinie, Plan-Spiegel, Bettspiegel), Glättung allein.
- Das Deckel-Modell senkt den Bandfehler von 64,5 auf 14,8 cm (Median); es bleiben 25–30 cm RMS, die kein geprüftes Modell erklärt.

## 2. Profil quer an s 439 (verlangt bei „uneindeutig“)

s 439 liegt auf einer Rampe (Lippe 10 bei s 437,6); die Editor-Spline fällt dort 0,34–0,35 m je Meter. u > 0 = links. B0 / C = T6JB0_2 / T6JC_2.

| u (m) | Kante (m) | Maske | Gelände (m) | Spline (m) | Boden − Gelände (cm) | Boden − Spline (cm) | G (cm) | W − H (cm) |
|---|---|---|---|---|---|---|---|---|
| −7,27 | 5,71 | 0 | 91,17 | 89,21 | +2 / +2 | +198 | 0 | +2 |
| −5,37 | 3,67 | 0 | 91,24 | 89,31 | −13 / −13 | +180 | 0 | −13 |
| −4,43 | 2,81 | 0 | 90,64 | 89,38 | −133 / −137 | −6 / −10 | 0 | −133 |
| −4,11 | 2,54 | 0 | 90,45 | 89,21 | −166 / −162 | −42 / −38 | 0 | −166 |
| −3,16 | 1,46 | 3 | 89,69 | 89,26 | −49 / −48 | −6 / −4 | 11 / 9 | −38 |
| −2,21 | 0,52 | 3 | 89,09 | 89,32 | +14 / +14 | −9 | 12 | +26 |
| −0,95 | 0 | 1 | 88,69 | 89,22 | +1 / +1 | −52 | 49 | +50 |
| 0,00 | 0 | 1 | 89,02 | 89,27 | −8 / −11 | −32 / −35 | 32 | +25 / +21 |
| +0,95 | 0 | 1 | 89,01 | 89,33 | +24 / +24 | −8 | 14 | +38 |
| +2,22 | 0,50 | 2 | 89,70 | 89,22 | −50 / −50 | −2 | 7 | −43 |
| +3,17 | 1,36 | 2 | 90,56 | 89,27 | −103 / −103 | +26 | 2 | −101 |
| +4,11 | 2,39 | 0 | 91,19 | 89,34 | −108 / −108 | +77 | 0 | −108 |
| +5,38 | 3,66 | 0 | 91,34 | 89,22 | +1 / +1 | +213 | 0 | +1 |

Lesart: Rechts sitzt der Boden bis Kante 2,8 m etwa auf Spline-Höhe, auch außerhalb des Prüfbands; ab 3,7 m wieder auf dem Gelände. Links bei
0,5 m auf Spline-Höhe, bei 1,36 m 26 cm darüber, bei 2,39 m 77 cm über der Spline (aber 1,08 m unter dem Gelände), ab 3,66 m auf dem Gelände.
Übergang über 1–2 m, keine scharfe Kante. Beide Dumps praktisch gleich (≤ 4 cm). Sichtbares Wasser nur im Bett und in der ersten Zelle rechts.

## 3. Kolke und neues Bettziel

| Lesart | hoch | mit Hindernis | ohne | flach mit Hindernis |
|---|---|---|---|---|
| `boden_befund` (Median der 1-m-Zellen) | 20 (C: 19) | 1 | 19 (18) | 2 von 4 (2 von 5) |
| am Kolkmittelpunkt (frühere 15/24-Zählung) | 15 | 1 | 14 | 2 von 9 |

- O1 widerlegt (1 statt ≥ 13 von 15). Nur 3 Kolke berühren einen Grundriss, alle drei Ufersteine aus „detailgrad“. Der heutige Hindernis-Akteur hat
  1 145 Teile (901 Altbestand, 239 detailgrad, 5 Beckenblöcke); in s 385–585 liegen nur 13 Altbestand-Teile (vom Filter am 14.10. schon geräumt).
  Der Verdacht „906 Alt-Hindernisse im Korridor“ ist damit überholt.
- O2 nicht erreicht: r(Anhebung; Kolkbreite) −0,52 / −0,47 / −0,13 (verlangt ≤ −0,6).
- Kolktiefe sichtbar (W − H an der tiefsten Zelle): Median 107 cm, 80–134 cm; 18–20 von 24 im Ziel 0,8–1,2 m, keiner darunter.
- **Neues Bettziel (6k §3.3) nicht erfüllt:** sichtbar_1 im Bett 88,6 % (verlangt ≥ 99 %), nur im 1-m-Raster gemessen. Band erfüllt sein Ziel:
  sichtbar_5 = 14,0 / 12,6 % (≤ 15 %), mit Hindernis-Ausschluss 10,5 / 9,1 %.

## 4. Editor-Lesetest: Landschaft = hoehe.f32 (neu)

Frage aus Schritt 1: Weicht die Editor-Landschaft im Band vom Weltstand ab, z. B. durch eine noch aktive Water-Brush-Ebene?
Gemessen mit `sample_landscape_heights` an allen 2 118 Zellen von Bett, Band, Lippenschatten und bis 3,5 m dahinter (C2 geladen, nur lesen):

| Bereich | Zellen | Editor − hoehe.f32 Median | p10 / p90 | größte |Abweichung| | > 5 cm |
|---|---|---|---|---|---|
| alle | 2 118 | −0,03 cm | −0,66 / +0,58 cm | 0,89 cm | 0 |
| Bett | 722 | −0,08 cm | −0,67 / +0,60 cm | 0,85 cm | 0 |
| Band | 554 | −0,03 cm | −0,67 / +0,56 cm | 0,88 cm | 0 |
| Lippenschatten | 111 | −0,04 cm | −0,68 / +0,47 cm | 0,82 cm | 0 |

→ Die Landschaft im Editor ist exakt der Weltstand. Der tiefe Simulationsboden kommt nicht aus einer abweichenden Landschaft.

## Fragen

1. Gilt ein Deckel mit 33 cm (flach) bis 80 cm (Rampen) Rest-Streuung als DECKEL? Passt „eng ≤ 15 cm“ zur Bettform mit Rampen von 0,35 m/m?
2. Wenn ja: Schritt 2 (DEBUG_RENDER_BOTTOM_CONTOUR + Latten) an einer flachen Stelle statt s 439? 21 flache Kandidaten mit Boden = Spline + 2–6 cm
   liegen vor (Liste auf Wunsch).
3. Bettziel sichtbar_1 ≥ 99 % gegen gemessene 88,6 %: Liegt das am Deckel (Bettzellen nahe der Kante) oder ist das Ziel im 1-m-Raster zu streng?
4. Kolke: Gilt das Kolkziel über „Kolktiefe sichtbar“ (18–20/24 im Ziel) als erfüllt?
