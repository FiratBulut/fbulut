# Auftrag 16c – Ferat: EIN Fluss je Gewässer, keine Abschnitte zwischen den Fällen

Stand 12.10.2026, 17:10. **Entscheidung Ferat:** „Das mit mehreren Flussabschnitten kann man weglassen, wir simulieren ja. Es wird einen Fluss geben
von Anfang bis zum Schluss, wo der Fluss mündet.“

## Folgen für `fluss_sim`

1. **Je Gewässer genau ein `WaterBodyRiver`** von der Quelle bis zur Mündung (in See, Fluss oder Meer), über alle Fälle hinweg. Die Simulation füllt
   Becken und überströmt Lippen selbst – so wie im gespeicherten C2-Test (`SWR_C2_Fluss`, s 0–179 m, 19 Fälle in einer Spline, Bild
   `bilder/swr/c2_wcbs_klar.jpg`). Die Punkte (x, y, z, Breite, Tiefe, Tempo) bitte als **eine** Punktliste je Gewässer ausgeben; z an Stufen so,
   dass die Spline den Wasserspiegel oberhalb und unterhalb trifft (Lippe/Fuß wie bisher als Punktrollen).
2. **Abschnitte `A00…` entfallen** als Water Bodies. Falls ihr sie intern für Fälle/Effekte braucht, nur noch als Bereiche (`s_m`) mit Rollen, nicht
   als eigene Flüsse.
3. **Simulationsbereiche (Kacheln) bleiben eine offene Frage:** Bei langen Gewässern wird ein einzelner `AShallowWaterRiver` zu grob (Auflösung
   höchstens 512 Zellen; C2 179 m → ≈ 0,35 m). Bitte recherchieren: Kann man den Bereich einer SWR auf einen Teil eines langen Flusses begrenzen
   (z. B. Bounds/„Source Size“/eigene Begrenzung), oder legt man mehrere SWR an, die alle denselben Fluss als Quelle nennen? Lokal teste ich das
   (Modus „ein SWR je Kachel mit demselben Fluss“). Bis dahin: ein SWR je Gewässer, wenn die Länge ≤ ~180 m bei 0,35 m Zelle bzw. ≤ ~130 m bei 0,25 m ist.
4. Fälle (Vorhang/Niagara/Schaumobjekte) und `wasser_kollision` (Hindernis-Akteur `WH_…`) bleiben wie in 16/16a. Ferat: Wasserfälle/Vorhänge
   **warten** vorerst.

## Nachtrag 17:45 – Simulationsbereich und Auflösung gemessen (Plugin 0.18, `swr_info`)

- **Der Bereich einer SWR ist das achsparallele Rechteck um ihre Quell-Flüsse:** C2 (`SWR_C2_Fluss`, 179 m) → `sim_res` 255 × 512, `sim_dx` 33,1 cm
  (≈ 84 × 170 m).
- **`resolution_max_axis` über 512 geht** (an C2, live im Editor, ProfileGPU-Summe `Grid2D_SW_River`):

  | Wert | `sim_res` | GPU live (Editor) |
  |---|---|---|
  | 512 | 255 × 512 | 0,8 ms |
  | 1024 | 510 × 1024 | 6,3 ms |
  | 2048 | 1019 × 2048 | 9,7 ms (nach 45 s noch nicht eingelaufen) |

  Bild: [`bilder/swr/c2_aufloesung_512_1024_2048.jpg`](../bilder/swr/c2_aufloesung_512_1024_2048.jpg). (`sim_dx` meldete direkt nach dem Reset noch 33,1 cm –
  vermutlich erst nach dem Neustart der Simulation aktualisiert; das Bild bei 1024 ist sichtbar feiner.)
- **Folgerung (Vorschlag an euch):** Je Gewässer EIN Fluss (Ferat) und EINE SWR, `resolution_max_axis` = längste Rechteckseite / Zielzelle (0,25–0,35 m),
  bis 2048. Die hohen Kosten fallen nur beim Backen im Editor an; im Spiel läuft gebacken (WCBS ≈ 0,2 ms an C2). Nur wo das Rechteck > ~600–700 m
  wird (lange oder diagonal/gewunden verlaufende Flüsse wie `F_HAUPTFLUSS` 2 km), muss der Fluss für die Simulation in wenige lange Stücke geteilt
  werden – nach Länge/Rechteckfläche, nicht an den Fällen. Unsere Daten: Bäche (170 Stück in `baeche_alle.json`, je Feld gestückelt) Median 151 m,
  max 1 000 m; Flüsse (27) Median 204 m, max 1 996 m. Bitte im Export: je Gewässer Rechteckmaße, empfohlene Auflösung und ggf. Teilungspunkte.
