# 16h Nachtrag 6b – Ferat: „Fällt dir nichts Außergewöhnliches auf?“ (Talkaskade von oben, 13.10.2026, 19:20)

Zu Nachtrag 6 §8 (Bild `bilder/swr_p2/talkaskade_treppe_von_oben.jpg`). Was wir jetzt sehen, mit Messwerten:

1. **Wasser liegt neben dem Bett auf dem Ufer und im Gras.** An jeder Stufe breitet sich eine dünne, graue Wasserschicht über den Rand aus.
   - Messung nach dem letzten Bake (16:40): Im 2-m-Band neben dem Bett ist die Talkaskade zu **94,1 %** nass (Ziel ≤ 5 %), das Kiesbett zu
     91,4 %, insgesamt **1 722 Zellen 1–8 m** neben dem Bett.
   - **Ursache:** SWR-Band = Bett + 2 m (sonst blieb die Front bei s 59 stehen, F2 in Nachtrag 2). Bei Nachfüllrate 0,3 füllt die
     Simulation auch dieses Band.
2. **Becken verkehrt herum:** Jedes Becken ist am **unteren** Ende am tiefsten und hat am Einlauf eine flache Schicht. In der Natur liegt der
   Kolk direkt unter dem Absturz, und das Becken läuft zur nächsten Lippe flach aus.
3. **Keine sichtbaren Abstürze:** Die Stufen fallen 0,7–3,7 m (Spiegelsprünge aus `lauf_p2.json`), zu sehen ist nur ein grauer Schleier.
4. Becken zu gleichmäßig, wie eine Schüssel-Treppe (Nachtrag 6 §8). Einzelne Grasbüschel stehen mitten im Bach.

**Fragen:**
- **(a)** Wie halten wir das Wasser im Bett, ohne dass die Front stehen bleibt? Zur Wahl stehen:
  - Ufer an den Stufen höher bzw. das Bett an den Lippen tiefer;
  - `remove_outside` (F1: Überlauf −38 %, aber Bett 15 % flacher);
  - das Band nur an den Stufen breiter;
  - Hindernis-Wände am Ufer;
  - feineres Raster.
- **(b)** Die Becken-Form richtig herum: Kolk unter dem Absturz, Auslauf flach. Das gehört in den neuen Step-Pool-Plan (Nachtrag 6, Frage 4).
- **(c)** Abstürze 0,7–3,7 m: Ferat hatte „warte mit Wasserfällen“ gesagt. Reicht hier das SWR-Wasser über die Lippe, oder braucht jede Stufe
  ≥ 1 m einen Vorhang?
