# 16h Nachtrag 6n – Schritt 3a (`smoothing_width` 1): Deckel VERSCHWINDET

Stand 18.10.2026, 18:30 PC-Uhr. Bezug: 6l (0595869), 6m (5481238). Nur im Speicher, danach Neustart ohne Speichern (nur die drei SWR-Testobjekte waren
ungespeichert). Ablauf wie T6j-B B2: `smoothing_width` 5 → 1 (zurückgelesen), frisch_reset, LIVE_SIM, stabil bei T6M3A_2 (zwei Dumps < 1 pp), Bake im Speicher.

## Ergebnis (vorab festgelegtes Urteil: VERSCHWINDET, wenn Band-Median Sim-Boden − Gelände > −20 cm)

| Maß | smoothing 5 (Basis T6L2B_2) | smoothing 1 (T6M3A_2) |
|---|---|---|
| gültig (Bett nass, Front) | 100 %, 788 m | 100 %, 788 m |
| **Band-Median Sim-Boden − Gelände** | **−62,3 cm** (0,25–1 m −30,4 / 1–2 m −81,7) | **−3,5 cm** (−4,5 / −2,8) |
| Deckel-Reichweite gegen die echte Kontur (Schritt 2) | 6 Zellen = 2,20 m | 2 Zellen = 0,73 m |
| sichtbar > 2 cm: Band / 0,25–1 m / 1–2 m / Lippenschatten | 15,3 / 30,0 / 4,7 / 55,9 % | 16,1 / 30,0 / **6,0** / 58,6 % |
| Bett sichtbar_1 / **Kernbett** sichtbar_1 (eure Definition 6l §3, n 250) | 88,6 % / **97,6 %** | 95,6 % / **100,0 %** |
| Kolke in 0,8–1,35 m sichtbar | 24/24 (max 1,34 m) | 22/24 (max 1,31 m) |

**Urteil: VERSCHWINDET.** Der Deckel war ein Ausgabe-Artefakt der Höhen-Extrapolation in trockene Zellen (passt zum Niagara-Befund 6m §3); die
Simulation selbst ist gesund. Nach eurer Regel (6k §2.6): `smoothing_width` bleibt 5, „sichtbar“ ist das Maß.

Bilder (Repo `bilder/swr_p2/t6m3a_glaettung5_gegen_1.jpg`, je links 5 / rechts 1, gebacken, gleiche Kameras): Unterschiede klein; mit 1 wirken die
Wasserränder etwas schärfer und der Grund etwas klarer; an der Stufe t430 weniger weißer Schaum.

Zusatzbefund Rolle 1 (abgeleitet aus dem GPU-Programm): Die Glättung wirkt auch auf nasse Zellen (Gewichtung nach Höhenunterschied, nur diagonale
Nachbarn); bei 5 liegt der Sim-Boden auch in 18–33 % der nassen Zellen > 10 cm unter der echten Kontur.

## Fragen

1. **Kernbett-Ziel (≥ 99 %):** wird mit 5 verfehlt (97,6 %), mit 1 erreicht (100 %). Dafür steigt der Uferstreifen 1–2 m auf 6,0 % (Ziel ≤ 5) und 2 Kolke
   fallen aus dem Band. Bleibt es bei 5 (eure Regel), oder ist 1 bzw. ein Zwischenwert (2–3) die bessere Abwägung? Wenn Zwischenwert: wie testen?
2. **Messweg:** Soll der Simulationsboden künftig aus der Debug-Bodenkontur (Render-Target im Zustand DEBUG_RENDER_BOTTOM_CONTOUR) statt aus R − G
   gelesen werden? (Das Umschalten setzt die Simulation zurück; eine Kontur-Lesung braucht also einen eigenen Lauf.)
3. **Schaum:** Ist weniger Schaum an Stufen mit 1 erwünscht oder ein Verlust?
