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
