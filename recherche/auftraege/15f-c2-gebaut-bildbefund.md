# Auftrag 15f – C2 im Editor gebaut: Bildbefund und Wünsche (Stufen zu regelmäßig)

Stand 12.10.2026, 01:45. Der Pilot C2 (`F_ERLENBACH_1V_C2`, Plan aaf330c, 1 m, Biom tundra) ist **vollständig eingebaut**:

- Gelände C2: 4 065 Zellen, −9,33 bis +1,00 m.
- Wasser: River R0 (29 m) und Kaskadennetz KN0 (37 544 Punkte), Material `MI_EL_Kaskade_SLW`. Oberer Erlenbach gekürzt.
- Ebene `gefaelle`: 1 183 Instanzen und 56 Akteure. Effekte: 18 Niagara.

Bilder: [`bilder/gefaelle_c2/c2_vorher_nachher.jpg`](../bilder/gefaelle_c2/c2_vorher_nachher.jpg) (links vorher, rechts nachher) und
[`c2_schaumstufen.jpg`](../bilder/gefaelle_c2/c2_schaumstufen.jpg). Die Nachher-Bilder wurden noch mit Schaum 1,0 aufgenommen.

## Was funktioniert

- Das Kaskadennetz zeichnet jedes Becken von Ufer zu Ufer nass, ohne trockene Becken. Variante A aus 14b ist damit bestätigt.
- Die Übergänge zu River und Zufluss passen, Niagara sitzt an den Stufen. Uferring und Lagen sind sauber, Abtrag gibt es nur im Bachkorridor.

## Befunde

1. **Schaum (bei mir behoben):** Die Vertexfarbe B ist an 77 % der Netzpunkte > 0,8. Bei 16 Stufen auf 174 m überlappen die Aufprall-Radien fast
   überall. Mit `Schaum_Menge` 1 wirkte das Netz deshalb wie eine **weiße Betontreppe**. Lokal steht jetzt `Schaum_Menge` 0,15 / `Zungen_Schaum` 0,25:
   grünlich-klares Wasser auf den Stufen, Schaum an den Fällen. **Bitte im Planer:** Schaum nur am Lippensaum (≤ 0,5 m) und im Aufprallkreis,
   dazwischen 0. Aufpralltrichter ≤ 30 % der Beckenlänge.
2. **Die Stufen sind zu regelmäßig. Das ist jetzt der Hauptmangel.** Aus jeder Kamera sieht man eine **Treppe**: gerade Lippen quer über die ganze
   Breite, gleiche Abstände, gleiche Höhen. Besonders deutlich ist das im oberen Teil (S01–S04, Kaskaden mit 2–4 gleichen Teilstufen) und im Bild
   `kn0_unten` (Terrassenfolge). Wunsch:
   - Lippen unregelmäßig: schräg zur Fließrichtung (±15–30°), gekrümmt, mit Kerbe (Hauptstrahl an 1–2 Stellen statt über die volle Breite).
     Teil-Lippen versetzt, keine durchgehende Kante.
   - Abstände und Höhen stärker streuen (±40 %). Kaskaden nicht als gleich hohe Teilstufen, sondern als Blockkaskade mit unterschiedlichen
     Stufenhöhen. Dazwischen ab und zu Rampe/Schnelle.
   - **Lippen aus Blöcken** (Keystones, Riegel) dicht besetzen, sodass die Geländekante nirgends als gerade Linie sichtbar ist. Dazu Blöcke im Becken,
     Kolk mit Kies, Totholz quer.
   - Bachbreite wechseln: Becken breiter, Lippen schmaler (Einschnürung).
   - Im Kaskadennetz: Zungen entlang der Kerben breiter und deckender, an den Seiten dünn oder fehlend, sodass Fels durchschaut.
3. **Beckenfarbe:** Die Becken wirken dunkel tannengrün, dunkler als der River unterhalb. Lokal prüfe ich `Absorption_Faktor`/`Streuung_Faktor`
   (Umrechnung aus dem Flussmaterial war geschätzt).

## Bitte

- Den Planer (A15) für 2. anpassen: unregelmäßige Lippen und Abstände, Blocklippen. C2 dann neu planen; ich rechne auf 1 m nach und baue neu.
- Die übrigen 19 Piloten baue ich erst, wenn Ferat C2 abgenommen hat.
