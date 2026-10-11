# Antwort zu Auftrag 15e – Rechteckige Abgrabungen abseits des Bachs, Lagen an der Feldgrenze

Stand 11.10.2026. **Vorfassung mit C2.** Die Endfassung mit allen Läufen und dem Commit-Hash folgt.

## Kurzfazit C2

**Ursache:** Die 35°-Uferböschung des Querprofils war eine Obergrenze für das Gelände bis 60 m neben dem Bach. Jeder
Hang, der steiler als 35° ist, wurde deshalb abgeschnitten. Gerade Kanten entstanden am 60-m-Band und an den
Segmentenden.

**Behoben:** Außerhalb der Wasserbreite wird nur noch so viel abgetragen, wie die Eintiefung verlangt:
(alter − neuer Spiegel + 0,5 m) − (Abstand − halbe Breite) · tan 35°.

**C2 jetzt:**

| Abstand zum Bach | Abtrag |
|---|---|
| 0–10 m | 6 583 m³ |
| 10–20 m | 1 978 m³ |
| über 20 m | **0 m³** |

- Vorher lagen 50 % des Abtrags weiter als 30 m vom Bach entfernt.
- Max. Δ jetzt 7,42 m (unter dem Fall), vorher 12,6 m.

**Lagen:** Jede Zelle mit |Δ| > 0,3 m hat eine Lage, auch jenseits der Feldgrenze.

**Unverändert gegenüber 15c:** Stufen, Spiegel, Wasserkörper, Effekte und Kameras. Geändert sind nur das Gelände, die
Lagen und Instanzen am Hang (23 Dateien).

**Prüfer:** 0 FEHLER, auch mit den neuen Regeln (Δ > 0,3 m nur am Bach, Lage für jede Δ-Zelle).
