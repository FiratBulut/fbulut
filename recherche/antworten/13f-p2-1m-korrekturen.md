# Antwort zu Auftrag 13f – Korrekturen an den Sehenswürdigkeiten-Planern nach dem 1-m-Lauf

Stand 11.10.2026. **Vorfassung nach dem Bergwald-Teil** – die Punkte für die übrigen Biome folgen in der
Endfassung dieser Datei.

## Kurzfazit (Vorfassung)

- **Bergwald-Pilot (bergwald_03 Säulenhain + bergwald_06 Karsee)** ist an der Quelle korrigiert:
  A3 (Bäume am Stammfuß), A4 (Mündung/Abfluss am Seeumriss), A7 (`materialwuensche_biom`), A8 (Stufen mit
  Becken, explizit ausgegeben), A9 (Mündung nur Epic), A10 (Feldgrenze), A11 (weiche Lagenränder), A12
  (Querprofil je Bach) und B bergwald_06 (Zulauf West im alten Lauf, `tiefe_m` nach dem Stempel,
  Houdini-Netz `R_M2_P0__WASSER` ausgeblendet, Zu- und Abfluss im alten Lauf).
- Bergwald auf 2 m: Planer 0 FEHLER, 0 WARNUNG; Prüfer 0 FEHLER, 0 WARNUNG; zwei Läufe byteidentisch.
- Zusätzlich auf einer synthetischen 1-m-Welt (2-m-Daten hochgerechnet) geprüft: Prüfer 0 FEHLER.
- Die lokalen Übergangslösungen für A1, A2, A3, A4, A7, A10 können für den Pilot entfallen, sobald dieser
  Stand lokal läuft.

Der Bergwald-Pilot steht im Commit, der diese Vorfassung enthält (siehe Git-Log „Auftrag 13f: Bergwald-Pilot“).
