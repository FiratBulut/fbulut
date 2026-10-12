# Antwort zu Auftrag 15f – C2 gebaut: Bildbefund (Schaum, Stufen zu regelmäßig, Beckenfarbe)

Stand 12.10.2026. **Vorfassung mit dem neuen C2-Plan.** Die Endfassung mit allen Läufen, den Vorbildern und dem
Commit-Hash folgt.

## C2 neu (Kennzahlen, Cloud 2 m + 1-m-Fenster)

| Kennzahl | vorher (aaf330c) | nachher |
|---|---|---|
| Lippen schräg (≥ 10° gegen quer) | 0 % | 81 % (Mittel 16,6°, Streuung 17°) |
| CV Teilstufenhöhen in Kaskaden | 0,01 (gleich hoch) | 0,18 |
| CV Lippenabstände / Fallhöhen | 0,43 / 0,56 | 0,51 / 0,67 |
| Schaum > 0,8 (Mittellinie) | 88 % | 29 % |
| Schaum > 0,8 im Querprofil | – | 10 % |

**Prüfer:** 0 FEHLER. Testbild: `gefaelle/test_F_ERLENBACH_1V_C2_s1.png`. Das neue untere Feld zeigt das Netz
abgewickelt mit Lippen, Kerben, Deckung und Schaum.

**Neu im Kaskadennetz:** Je Punkt gibt es ein Querprofil `quer` mit 11 Stützpunkten und den Feldern `dz_cm`,
`deckung`, `schaum` und `tiefe_cm`. Dazu kommen `mittellinie_s_m` und `material_parameter` (Schaum_Menge 0,15,
Zungen_Schaum 0,25). Das Format steht in der Endfassung.
