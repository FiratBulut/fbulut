# Antwort zu Korrektur Runde 5 (Auftrag 11, Felsgruppen an Steilhängen)

Stand: 11.10.2026. Umgesetzt und synthetisch getestet, nicht mit Echtdaten. Details: `verteilung-fels-organisch.md` Abschnitt l,
neue Regelblöcke `steilhang` und `blockstrom_platten` in `felsgruppen_regeln.json`.

## Kurzfazit

- **Ursache:** Die mittlere Dichte lag schon vorher unter der Grenze. Verletzt war sie örtlich in Gruppen, Bändern und Blockstrom-Zungen,
  mit bis zu 1,4–1,6 Blöcken über 2 m je 100 m². Dazu kamen gleichverteilte Größen, würfelige oder stehende Netze als Gruppenkern, kaum
  Eingraben und 4–12° Kippen. Dadurch waren die dunklen Unterseiten sichtbar.
- **Steilhang über 35°:** Blöcke über 2 m höchstens 1 je 150 m², über 4 m höchstens 1 je 600 m², geprüft je Zelle und mit Mindestabstand.
  Größen folgen einem Potenzgesetz. Eingraben 50–70 %, lange Achse entlang der Falllinie ± 20°, Kippung voll an die Geländenormale.
- **Würfelige Netze:** 23 würfelartige und 13 stehende Netze dürfen an Hängen über 30° nur noch als Satelliten unter 1,5 m stehen. Die Liste
  steht im Log und im Bericht.
- **Blockstrom:** Platten mindestens 40 % eingegraben, nur in Rinnen und am Hangfuß, nie auf Flächen ohne Hangknick.
- **Unverändert:** Formgruppen-Heros und Grat-Kronen behalten Netz, Größe und Lage. Meer-Regel, Platten-Lagenregel und Sperrlisten gelten weiter.

## Synthetischer Test (vorher = Planer aus Runde 4)

| An Hängen über 35° | B4-artig | A5-artig |
|---|---|---|
| Blöcke über 2 m | 2 904 → 563 | 2 436 → 452 |
| Blöcke über 4 m | 1 915 → 288 | 1 598 → 240 |
| Dichte über 2 m je 100 m², höchste Zelle (Grenze 0,667) | 1,40 → 0,31 | 1,56 → 0,26 |
| Dichte über 4 m je 100 m², höchste Zelle (Grenze 0,167) | 1,09 → 0,156 | 1,07 → 0,164 |
| Würfelanteil an Hängen über 30°, Blöcke 1,5–4 m | 37–44 % → 0 % | 35–39 % → 0 % |
| Eingraben am Steilhang, Median | 0,25 → 0,60 | 0,25 → 0,61 |
| Abweichung lange Achse zur Falllinie, Median | 44° → 10° | 46° → 10° |
| Blockstrom-Platten: Eingraben min / ohne Hangknick | 0,06 / 1,1 % → 0,415 / 0 | 0,105 / 2,7 % → 0,42 / 0 |
| Instanzen gesamt | −27 % (14 051) | −28 % (11 849) |

Zwei Läufe byteidentisch, Logs ASCII, Budget eingehalten, Meer-Regel ohne Verstoß.

## Bitte lokal prüfen

1. **Neue Prüfkameras:** `steilhang_300m`, `steilhang_120m`, `blockstrom_rinne_60m`. Dazu B4 `formgruppe_300m_2/_3` erneut und als Gegenprobe
   A5 `formgruppe_front_120m` und B4 `grat_120m`.
2. **Satelliten der Formgruppen am Steilhang** sind jetzt meist eingebettet, sichtbar im Median 0,23 m statt 3,8 m, weil die Dichtegrenze sie
   verkleinert. Wirken die Formgruppen dadurch zu nackt, die Formgruppen-Satelliten von der Dichtegrenze ausnehmen.
3. **Feldgrenzen:** Dort können zwei Blöcke über 2 m näher als 9,8 m stehen, weil jedes Feld den Mindestabstand nur gegen eigene Stücke prüft.
4. Die Größenverteilung misst Exponent 0,9–1,0 statt 2,2, weil Wandschalen, Heros und Kronen ihre Größe behalten.
