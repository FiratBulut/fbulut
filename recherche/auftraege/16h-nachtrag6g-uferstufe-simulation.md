# 16h Nachtrag 6g – Uferstufe hält in der Simulation nicht: dichte Spline (1 m) bringt nur 85 → 78,5 %, remove_outside 50 stoppt die Front

Stand 13.10. 22:50. Bezug: 6f (Band 85 % nass), 6b (Prüfkriterium ≤ 5 %), 6c-Bettplan (eingebaut).

## Messungen (frischer Dump nach je 5 min Live-Sim, Prüfband `p2bett_pruefband.py`)

| Variante | Bett nass | Band 0,25–2 m nass | Tiefe Bett Median / p90 | Front |
|---|---|---|---|---|
| 54 Spline-Punkte (direkt = Plan-Spiegel), remove 0 | 100 % | **85,0 %** | 0,40 / 0,72 m | 788/788 |
| **388 Punkte je 1 m aus spline_z.json + 5 cm (Ferat „ein Tick höher, minim“), remove 0 – gebacken + gespeichert** | 100 % | **78,5 %** | 0,34 / 0,59 m | 788/788 |
| dito + `remove_outside_spline_amount` 50 (F1) | 0 % | 0 % | – | **63/788** (Front bleibt in der Bergrinne stehen, wie F2 am 13.10. vormittags) |

- Spline-Verschmierung war also NICHT die Hauptursache (Abweichung Spline–Plan je Meter vorher mittel 23,8 cm, max +96 cm; jetzt 0).
- Das Gelände stimmt: 0,5 m hinter der Bettkante Median +0,21 m über dem Plan-Spiegel, 0,8 % darunter (`p2_bett_bericht.md`).
- Die SWR hat **36,7-cm-Zellen** (319 × 2016 = Maximum 2048 über den ganzen 788-m-Bach). Die Uferstufe ist 0,25–0,9 m breit = 1–2 Zellen; eure
  6b-Vermutung („feineres Raster erst prüfen, wenn die Uferstufe im Bake nicht hält“) ist jetzt der Hauptverdacht: Die Sim tastet das Gelände
  zu grob ab, die Stufe wird weggeglättet, und das Nachfüllen (0,3) bis zur Spline-Höhe setzt die Nachbarzellen unter Wasser.
- Tiefe im Bett sinkt mit dichter Spline (0,40 → 0,34 m Median): Die Kolke (Plan 0,84–1,20 m) werden im 37-cm-Raster nur 0,6–0,7 m tief (p90 0,59).

## Fragen (bitte mit Zahlen)

1. **Eigene SWR nur für die Talkaskade** (s 389–580, ~200 × 30 m → 2048 Zellen ≈ 10 cm): Darf eine zweite `ShallowWaterRiver` denselben
   WaterBodyRiver als Quelle nutzen (zwei SWR auf EINEM Wasserkörper, Ferat erlaubt die Teilung der Simulationsbereiche bei > 600 m)? Welche SWR
   schreibt dann die gebackenen Texturen ins Material des Wasserkörpers – gibt es einen Weg (eigener Water Body für s 389–580 mit Übergang, oder
   `WaterBodyMeshComponent`/zweites Material), ohne den Fluss zu teilen? Wenn nein: Alternative?
2. Nachfüllen 0,3 ist die Schwelle, unter der die Front hängen bleibt (13.10. 09:50). Gibt es in 5.8 eine Möglichkeit, das Nachfüllen **nur im
   Bett** wirken zu lassen (Maske/„Bottom Contour“-Trick: Uferstufe als Hindernis-Akteur `WH_*` entlang der Bettkante, 0,3 m hoch)?
3. Ist das 5-%-Ziel bei 37-cm-Zellen überhaupt erreichbar, oder soll das Ziel für diese Auflösung z. B. ≤ 30 % im Band 0,25–1 m lauten und die
   Landschaft den Rest tragen (Uferkante als Steine/Gras verdecken)?
4. Kolktiefe: Lohnt ein tieferer Plan (Kolke 1,3–1,5 m), damit im 37-cm-Raster 0,8–1,0 m ankommen?

Bilder: `bilder/swr_p2/bettplan_p2d_dicht.jpg` (P2C 54 Punkte vs. P2D 388 Punkte – praktisch gleich). Ferats Fab-Bibliothek (348 Einträge) liegt
in `auftraege/daten/fab_bibliothek_2026-10-13.md|json` für die Bedarfslisten 20/21.
