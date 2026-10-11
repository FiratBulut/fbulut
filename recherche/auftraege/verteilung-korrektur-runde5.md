# Korrektur Runde 5 (Auftrag 11) – Felsgruppen: zu viele kantige Blöcke an Steilhängen

Stand 11.10.2026 06:00 lokal. Runde 3/4 von `felsgruppen_plan.py` lokal mit Echtdaten gesetzt (A5: 4 450 Instanzen + 30 Hero-Klippen, B4: 19 207 + 150),
Bilder aus den Prüfkameras des Planers (Kamera max. 25 m über Grund): `recherche/bilder/felsr3/`.

## Was gut ist (bitte so lassen)
- Küste A5: Felsnasen mit Klippenwand ins Meer, Brandungspfeiler, oben Gras/Kiefern (`FELSR3_A5_R3_formgruppe_front_120m.jpg`).
- Grate B4: Felskronen mit dem Hang verwachsen, Kiefern auf dem Kamm (`FELSR3_B4_R3_grat_120m.jpg`).

## Was nicht passt
1. **B4-Steilhang (`FELSR3_B4_R3_formgruppe_300m_3.jpg`, auch `_300m_2.jpg`):** sehr viele große, kantige, fast würfelige Blöcke dicht an dicht – wirkt
   wie ein Schutthaufen aus Kisten, nicht wie ein gewachsener Hang. Ziel (Witcher 3): an Steilhängen wenige große, halb eingegrabene Platten
   entlang der Schichtung, dazwischen viel kleineres Geröll und Fels der Landschaft.
2. **Blockstrom A5 (`FELSR3_A5_R3_blockstrom_120m.jpg`):** dünne Platten liegen flach obenauf statt eingebettet.

## Bitte ändern (felsgruppen_regeln.json / felsgruppen_plan.py)
- Steilhang > 35°: Blöcke > 2 m höchstens 1 je 150 m², > 4 m höchstens 1 je 600 m²; Größenstaffelung nach Potenzgesetz (viele kleine, wenige große).
- Eingraben an Steilhängen 50–70 % (statt 35–60 %), lange Achse hangparallel bzw. entlang der Schichtung (Fallrichtung ± 20°), Kippung voll an die Normale.
- Würfelartige Netze (Seitenverhältnis aller Achsen < 1,4) an Hängen > 30° nur als Satelliten < 1,5 m, nie als Gruppenkern.
- Blockstrom: Platten mindestens 40 % eingegraben, nie flach auf einer Fläche ohne Hangknick; lieber Rinnen/Hangfuß.
- Bericht: je Feld Zahl der Blöcke > 2 m und deren Dichte je 100 m² an Hängen > 35° (vorher/nachher, synthetischer Test reicht).
