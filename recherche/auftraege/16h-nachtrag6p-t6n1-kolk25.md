# Nachtrag 6p – T6N1 (Breite 1): alle Tore bestanden, nur Kolk 25 weicht vom Vorlauf ab → nicht gespeichert

Stand 18.10.2026, 22:45 PC-Uhr. Bezug: Antwort 6o (f2bb485) §2.2, §4.2, §4.3. Ferat hat Cloud-Empfehlungen am 18.10. pauschal freigegeben
(„Was Cloud empfiehlt, kannst übernehmen“); gespeichert wird trotzdem nur, wenn eure Abnahme besteht.

## 1. Ergebnis T6N1_2 (Breite 1, Lauf 22:18–22:40, stabil nach zwei Dumps, 0,0 pp Änderung)

| Abnahme 6o §4.2 | T6N1_2 | T6M3A_2 (Vorlauf Breite 1) | Urteil |
|---|---|---|---|
| G1 Prüfband sichtbar_5 | 10,70 % | 10,70 % | bestanden (± 1 pp) |
| G3 Bett nass_sim | 99,84 % | 99,84 % | bestanden |
| Kernbett sichtbar_1 | 100 % (0 Fehlzellen) | 100 % | bestanden |
| Front | 788,4 m | 788 m | bestanden |
| G2′a sichtbare Kolktiefe 0,8–1,35 m | 22 im Ziel, Nr. 3 Gelände (0,68 m), Nr. 36 Toleranz (0,783 m) | gleich | bestanden |
| G2′b W − G − F | −3,9 … −0,1 cm | gleich | bestanden |
| Kolke je ± 4 cm gegen T6M3A_2 | **23 von 24 exakt 0,0 cm; Nr. 25 +10,0 cm** | – | **verfehlt** |
| BAKED_SIM nach Bake zurückgelesen | ja | – | – |

Kolk 25 (s 492,1): W 70,01 statt 69,91 m, sichtbare Tiefe 1,045 statt 0,945 m (beide im Ziel), Half-Float-Stufe dort 2 cm. W − Plan +16,4 cm.
Die Kette hat nach 6o §4.2 „Kolke je ± 4 cm (Laufstreuung)“ korrekt **nicht gespeichert**. Neustart ohne Speichern folgt; Breite 5 bleibt.

## 2. Bilder (Opus-PM gesichtet, Bildpaare an Ferat geschickt)

`bilder/swr_p2/t6n1_bildpaare.jpg`: links Breite 5 (gespeichert), rechts Breite 1, gebacken, gleiche Kameras. K1 (flaches Ufer s 506,5):
keine Treppe, keine Spalte. K4 (Kolk 36) und K5 (Kolk 3): an der Stufe weniger weiße Flecken, Kanten nass. Mündung: praktisch gleich.
Licht vorher/nachher gleich (Sonne pitch −24°, yaw −20°, 100 000, 5 900 K).

## 3. Fragen

1. Die Toleranz ± 4 cm war als „Laufstreuung“ begründet. Gemessen ist die Streuung zwischen zwei Läufen mit gleichen Einstellungen 0,0 cm an
   23 Kolken und 10 cm an einem. Ist ein einzelner Ausreißer, der im Zielbereich bleibt und tiefer wird, ein Grund, nicht zu speichern? Oder
   soll das Kriterium lauten: „Median |ΔW| ≤ 2 cm, kein Kolk verlässt durch die Abweichung den Zielbereich“?
2. Wenn T6N1 übernommen werden soll: einen neuen Lauf T6N1b mit derselben Kette (≈ 30 min) und dann speichern, sofern Kolk 25 im Ziel bleibt?
3. Kolk 25 sitzt am Fuß einer Stufe (W − Plan +16 cm). Hinweis auf einen Strahl wie bei Kolk 36 (6o §1.3), der je Lauf leicht anders trifft?
