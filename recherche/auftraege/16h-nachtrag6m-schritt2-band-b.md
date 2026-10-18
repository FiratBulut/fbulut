# 16h Nachtrag 6m – Schritt 2 (6l §3) ausgeführt: Band B, Umschalten setzt zurück, Zusatzbefund aus dem Niagara-Programm

Stand 18.10.2026, 17:10 PC-Uhr. Bezug: Antwort 6l (0595869). Alles nur im Speicher, danach Neustart ohne Speichern (geprüft: nur die drei
SWR-Testobjekte waren ungespeichert).

## 1. Ort (Abweichung von §3.2, lokal freigegeben)

Kein Kandidat erfüllte §3.2 wörtlich (R5 „kein Hindernis 2 m“: 0 von 21; R1: 3; R2: 8). Gewählt: Uferlatte **s 506,51, u −4,05, Kante 1,43 m**
(Gelände 64,951 m, Spline 63,773 m, Sim-Boden in beiden Dumps Spline + 5,7 cm). Spline von s 504–509 völlig flach (Neigung innerhalb ±1 m: 0),
kein Hindernis auf der Lattenzelle und ihren 4 Nachbarn (nächster Stein diagonal 1,41 m). Bettlatte s 505,99, u −0,93 (Bettgelände 63,348 m,
Wasser 48 cm, kein Kolk, kein Hindernis). Latten 5 × 5 cm, 5-cm-Striche, nicht in `bottom_contour_actors`, ohne Kollision.

## 2. Ergebnis

| Messung | Wert |
|---|---|
| Basis (frisch, Nachfüllen 0,3, stabil) | Bett 100 %, Front 788 m, sichtbar wie bisher (0,25–1 m 30,0 %, 1–2 m 4,7 %), Sim-Boden − Gelände Band −62,3 cm |
| `render_state` → DEBUG_RENDER_BOTTOM_CONTOUR | Enum in 5.8.3 belegt; gesetzt über die Property |
| **Uferlatte** | Kontur **65,030 m = Gelände + 7,9 cm = Spline + 125,7 cm** (Segment 31,1; 3×3-Median Band B) → **Band B** |
| Bettlatte (Kontrollfall) | Kontur − Bettgelände im Median −1,0 cm (71,7 % der Bettzellen in ±10 cm) → bestanden |
| Fläche (numerisch aus dem Render-Target, Leseweg gegen den Bake-Dump geprüft) | Band: Median Kontur − Gelände −0,7 cm, unter Gelände − 10 cm 21,7 %; Kolke (67 Zellen) Median +10,0 cm, 50,7 % > +10 cm → „gemischt“ |
| Umschalten zurück auf LIVE_SIM | **setzt die Simulation zurück** (10 s danach Bett 0 %, Front 325 m); Nachlauf ab Reset gültig (Bett 100 %, Front 788 m) |
| Bilder | `T6L2_*` (live, Debug, Debug ohne Landschaft, Debug ohne Instanzen): die orangefarbene Kontur folgt Bett und Uferböschung |

**Lesart:** Die Bodenkontur der Simulation liegt auf dem Gelände (am Ufer +7,9 cm), nicht auf Spline-Höhe. Der „Deckel“ (Sim-Boden im Dump 63 cm
unter dem Gelände) sitzt also nicht im Eingang der Simulation.

## 3. Zusatzbefund (Rolle 1, offline, abgeleitet): das GPU-Programm in `Grid2D_SW_River.uasset`

- Das Niagara-System (Plugin WaterAdvanced, UE 5.8.3) trägt sein GPU-Programm lesbar im Asset.
- Nach jedem Simulationsschritt schreibt es in **trockene Zellen** als Wasserhöhe das Mittel der nassen Nachbarn und eine gemittelte Tiefe – bis
  5 Zellen weit (über `SmoothingWidth` 5).
- Der Simulationsboden selbst ist das Maximum aus Akteur- und Landschafts-Aufnahme; mit der Wasserhöhe der Wasser-Info wird er nicht verrechnet.
- An drei Dumps (14.10., T6JB0_2, T6JC_2) bestätigt: Auf Hangpixeln steht der gespeicherte Spiegel 3–6 Zellen hinter der nassen Kante auf Höhe des
  Nachbar-Wasserspiegels (+1…+4 cm), obwohl das Gelände 0,6–1,2 m höher liegt; die Tiefe fällt nach außen auf 0; ab 7 Zellen springt der Wert aufs
  Gelände. Unser „Boden = R + Akteurhöhe − G“ ergibt dort genau den Deckel.
- Das passt zu Deckelhöhe (Spline/Nachbar-Spiegel), weichem Rand, Reichweite unabhängig von der Spline-Breite (≈ 5 Zellen × 0,367 m ≈ 1,8 m + Rand)
  und zu Band B.
- Nebenbefund: euer Kriterium „Deckel-Kern“ ergibt auf den eingefrorenen Befund-Rastern 57,1 / 56,2 % (Vorhersage ≥ 75 %).

## 4. Nächster Schritt laut eurer Tabelle: 3a (`smoothing_width` 1), Lauf ab Reset wie B2

Erwartung nach dem Zusatzbefund: Das Deckel-Muster im Dump schrumpft auf etwa 1 Zelle (Band-Median über −20 cm). Wenn ja → reines
Ausgabe-Artefakt, `smoothing_width` bleibt 5, „sichtbar“ bleibt das Maß.

## Fragen

1. Einverstanden mit 3a wie oben? Gibt es eine Erwartung für die Wirkung von `smoothing_width` 1 auf das **sichtbare** Wasser (Zeichnung, Schaum)?
2. Wenn der Deckel ein reines Ausgabe-Artefakt ist: Soll der Simulationsboden für unsere Messungen künftig aus der Debug-Kontur (Render-Target im
   Debug-Zustand) statt aus R − G gelesen werden?
3. Kolke: Kontur im Kolk im Median +10 cm über dem Gelände (50,7 % > +10 cm) – passt das zu eurer O2-Diagnose (Anhebung des Sim-Bodens in Kolken)?
