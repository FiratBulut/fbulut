# Korrektur Runde 3b zu Auftrag 11: Biom-Planer auf Augenhöhe (10.10. 20:20 lokal)

Projekt Eldarien, UE 5.8.3. Priorität mittel. Bilder `bilder/nah1/` (Kamera 1,7 m an den dichtesten Stellen der Pläne).

**Sehr gut:** `sumpf` H5 (Rohrkolben, Binsen, Seggen im Flachwasser – wie Velen), `hochgebirge` E1 Bergwiese (Heidekraut, Schutt,
Latschen, Flechtensteine; `NAH1_E1_hochge_nah0`).

**Fehler `hochgebirge`:** In `NAH1_E1_hochge_nah1` wachsen Alpenrosen-/Grasbüschel mitten aus der Schneedecke. Bitte Pflanzen (bodendecker,
grasbueschel, alpenrose, latsche) nur, wo `lage_Schnee` < 60 von 255 und `lage_Eis` < 30; auf Schnee nur Steine/Flechtensteine
(halb eingeschneit: tiefer eingraben) und Eiszapfen an Felskanten.

Ich rolle die Biom-Planer gerade auf ihre Felder aus (aue 34, heide_tundra 10, hochgebirge 10, elfenwald 7, sumpf 3, lava 7,
wueste_ergaenzung 10 Felder); nordkueste/dschungel erst, wenn das Ersetzen alter Bäume geklärt ist (Setzer entfernt nichts ohne Freigabe →
`entfernen`-Filter bitte im STATUS je Feld begründen und die erwartete Zahl entfernter Bäume nennen).
