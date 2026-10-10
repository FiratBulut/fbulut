# Antwort zu Korrektur Runde 4 (Auftrag 11, Meer fehlt in karte_wasser)

Stand: 10.10.2026. Alle 12 Planer sind korrigiert und synthetisch getestet, nicht mit Echtdaten. Regel: `verteilung-KONVENTIONEN.md` §1b.
Zahlen je Planer: `verteilung-STATUS.md` Abschnitt „Runde 4“, Details je Bericht unter „Korrektur Runde 4“.

## Kurzfazit

- Jeder Planer bildet `meer = (hoehe < 0) & (karte_wasser == 0)` und `wasser_alle = karte_wasser > 0 | meer`.
- `wasser_alle` ersetzt `karte_wasser` überall, wo es als Sperre, Abstand, Nicht-Landzelle, Biom-Anteil oder Saum diente. Süßwasser-Regeln
  wie Ufer, Schilf, Wassertiefe-Klassen, Oasen und Stege bleiben bei `karte_wasser`.
- Unter −0,3 m steht nichts. Zwischen −0,3 und 0 m stehen nur Meeres-Rollen. Zwischen 0 und +0,3 m im Küstensaum stehen nur Wasserkante- und
  Strand-Rollen.
- Ein Schlussfilter prüft die Geländehöhe am Instanzort. `plan.json` meldet `meer_zellen`, `meer_gefiltert` und `biome_fenster_bezug: "land"`.

## Synthetischer Test

| Planer | unzulässig unter 0 m: vorher → nachher | Gesamt vorher → nachher |
|---|---|---|
| mittelschicht | 8 608 → 0 | 37 139 → 27 724 |
| spuren | 428 → 0 | 11 191 → 9 202 |
| felsgruppen | 0 → 0 | 1 342 → 1 363 |
| nordkueste | 783 → 0 | 28 504 → 42 913 |
| aue | 20 342 → 0 | 39 244 → 16 286 |
| heide_tundra | 0 → 0, Küstensaum 420 → 0 | 8 565 → 8 136 |
| hochgebirge | 0 → 0, Küstensaum 905 → 15 | 35 440 → 34 570 |
| elfenwald | 0 → 0, Küstensaum 13 → 5 | 41 886 → 42 145 |
| sumpf | 868 → 0 | 47 930 → 47 823 |
| dschungel | 2 → 0 | 15 588 → 15 171 |
| lava | 14 245 → 0 | 32 892 → 32 651 |
| wueste_ergaenzung | 7 969 → 0 | 18 783 → 10 428 |

Zwei Läufe je Planer waren byteidentisch, Logs reines ASCII. Binnenfelder ohne Meer bleiben bei den Querschnittsplanern byteidentisch.

## Was beim Neurechnen auffällt

1. **nordkueste wächst.** Tang, Treibholz und Strandkiesel sind jetzt Meeres-Rollen, Strandplatten Strand-Rollen. Sie finden erst jetzt das
   echte Meer. Im Test lagen 5 206 erlaubte Meeres-Instanzen zwischen −0,3 und 0 m, höchstens 8 m seewärts der Wasserlinie. Ist das zu dicht,
   in `nordkueste_regeln.json` `meer.meer_band_m` oder die Faktoren der Strandklassen senken.
2. **aue in Küstenfeldern:** Das Meer zählte über Kennzahl 0 als aue. Jetzt zählen nur Landzellen; das Küstenfeld B5 wird zum Leerplan.
3. **Inselfelder** wie A2, I4 und E4 können vom Leerplan zum Plan werden, weil ihr Eigenanteil jetzt nur über Land gerechnet wird.
4. **z knapp unter 0 m** durch Eingraben ist auf Strandboden ab 0 m möglich, zum Beispiel Strandkies. Das ist kein Meer.

## Zusätzlich behoben

- **Sumpf und Elfenwald:** Dateien mit Netzen mehrerer Klassen trugen Rolle und Ebene der ersten Klasse. Jetzt gibt es eine Datei je Ebene,
  benannt `<Netz>_e<Ebene>`, zum Beispiel `SM_ToadRush_00_e1`.
- **felsgruppen:** `felsufer` misst den Abstand zum echten Meer. Die Sichtbarkeit der Formgruppen berücksichtigt das Meer.
- **spuren:** Stege nur an Seen, nicht am Meer.

## Bitte lokal prüfen

1. Mit den neuen Plänen das vorläufige `meer_filter.py` gegenrechnen. Es sollte nichts mehr finden, außer Meeres-Rollen zwischen −0,3 und 0 m
   und eingegrabenen Strandstücken.
2. **H5:** Liegen echte Sumpfteiche in `eigner.r8` auf Kennzahl 0, bekommen sie keinen Schilfgürtel mehr. Dann die Teiche dem Sumpf-Rezept zuordnen.
3. Keine der aktuellen Regeldateien außer nordkueste hat Meeres-Rollen. Tang oder Muscheln an anderen Küsten müssten ausdrücklich ergänzt werden.
