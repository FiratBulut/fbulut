# Auftrag 22c – karte_wasser nach 22b §5: nicht eingesetzt, Rückfragen

Stand 18.10.2026, 19:00 PC-Uhr. Bezug: Antwort 22b §5. Neue Karte gerechnet (`karte_wasser_22b.r8` neben der alten), **alte Karte nicht überschrieben**.

## 1. Warum nicht eingesetzt

- **Automatischer Weltnutzer:** `scripts/bewuchs_texturen.py` packt die ganze `karte_wasser.r8` in den Alpha-Kanal der Textur `T_Eldarien_Bewuchs_D`;
  das Landschaftsmaterial steuert damit die Nässe (Abdunkeln `Nass_Abdunkeln` 0,6, Rauheit). Die heutige Textur ist Texel für Texel aus der heutigen
  Karte gebaut. Routine-Ketten (`sehens_gelaende_kette.sh`, `gef_gelaende_kette.sh`, `altwasser_kette.sh`, wartende Kette 230) bauen die Textur
  nebenbei neu → die nächste solche Kette würde die Nässe in 50 Feldern ändern (457 603 Zellen weniger, 817 141 mehr), ohne dass ein Planer läuft.
- `t22_0.py` und die Pilotwerkzeuge lesen den Altwasser-Abstand `d_alt` aus `karte_wasser.r8`; nach dem Überschreiben verschwände die Trockenbett-Gruppe.

## 2. Neue Karte (Regeln §5)

Wasser (> 127) = gebautes Süßwasser der Wahrheit status24 ohne Meer; ohne SWR-Überlauf (Band-Regel, 3 770 Zellen); Zellen mit Höhe < 0 byte-gleich
(Meer nach Planerformel gleich); Kodierung wie bisher (255 Wasser, Saum der Vorlage, auf 127 begrenzt); nur Felder mit Wasseränderung.
Zahlen: 373 153 Zellen fallen weg, 775 775 kommen dazu (1 148 928 in 50 Feldern; T22-0 nannte 1 132 777 in 40, Unterschied erklärt: 10 Felder ohne
Wasserpflanzen + Höhe < 0 + SWR-Überlauf).

| Prüffall (22b) | Ergebnis |
|---|---|
| Meer nach Planerformel unverändert | erfüllt (33 879 008 vorher/nachher) |
| 0 neue Zellen mit Höhe < 0 | erfüllt |
| C2: p2-Bett ist Wasser | erfüllt (5 966/5 966) |
| C2: altes Band außerhalb p2 leer | erfüllt |
| C2: ≤ 1 % Abweichung zur bereinigten Karte | **nicht erfüllt: 3,40 %** (davon 972 Zellen durch Saum-Begrenzung 127) |
| D5-Brücke unverändert | **nicht erfüllt: +5 504 / +5 696 Zellen im ±50-m-Fenster** |
| 30 Felder byte-gleich | **nicht erfüllt: nur 20** |
| V1-Abweichung 0 | **nicht erfüllt: Rest 71 917** (68 147 Höhe < 0 + 3 770 SWR-Überlauf) |

## 3. Fragen

1. **Umriss oder sichtbares Wasser?** Der Umriss der Wahrheit enthält 309 082 trockene Zellen (Spiegel ≤ 2 cm über Gelände, z. B. Ufer im Spline-Band).
   Von den 775 775 neuen Wasserzellen sind 255 733 trocken (D5-Brücke 4 013 von 5 504). Mit „sichtbar“ kämen an der D5-Brücke trotzdem ~1 500 Zellen je
   Fenster dazu, weil der gebaute Fluss breiter ist als das alte Band.
2. **Höhe < 0:** „Meer unverändert“ und „V1 = 0“ widersprechen sich (68 147 Zellen, vor allem F4, F5, F6, H5, H7). Was hat Vorrang?
3. **Houdini-Wasserfälle:** Der Typ `houdini_bleibt` fehlt in der Wahrheit; die Becken der 10 bleibenden Fälle fehlen in der neuen Karte (sichtbare
   Houdini-Flächen verlieren 104 417 Wasserzellen). Sollen die Becken nachgetragen werden (Quelle?), bevor die Karte eingesetzt wird?
4. **Nässe im Landschaftsmaterial:** Soll die Nässe-Textur beim Einsetzen bewusst mitgezogen werden (sichtbare Änderung in 50 Feldern), oder soll die
   Textur von der Karte entkoppelt werden (eigene, eingefrorene Nässe-Quelle), damit Routine-Ketten sie nicht nebenbei ändern?
