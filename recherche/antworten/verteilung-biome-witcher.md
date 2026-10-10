# Antwort zu Auftrag 11: Asset-Analyse und Verteilungs-Skripte je Biom (Witcher-Qualität)

Stand: 10.10.2026, nach Korrektur Runde 1. Koordination und laufender Stand: `verteilung-STATUS.md`. Verbindliche Regeln für alle
Planer: `verteilung-KONVENTIONEN.md`.

## Kurzfazit

- **Geliefert:** alle Teile A, B1–B9, C und D. Das sind 12 Planer-Skripte mit je einem Regel-JSON und einem deutschen Bericht, dazu die
  Asset-Taxonomie aller 1 435 Netze.
- **Getestet:** jeder Planer nur synthetisch in der Cloud, nie mit Echtdaten. Geprüft sind deterministische Läufe, Budget, ASCII-Logs,
  Leerplan in fremden Biomen und 0 Instanzen jenseits des 30-m-Saums. Echtdaten-Zahlen stehen als Erwartung in den Berichten.
- **Korrektur Runde 1 ist eingearbeitet.** Jeder Planer bebaut nur noch seine Biom-Zellen. Generische Mittelschicht-Klassen kommen nur
  aus `mittelschicht_plan.py`, Felsen über 0,8 m nur aus `felsgruppen_plan.py`, Spuren von Leben nur aus `spuren_plan.py`. Biom-Planer
  liefern dafür Overrides in ihrer Regeldatei. Details: `verteilung-korrektur-runde1.md`.
- **Gegen Ferats Hauptkritik** („Felsen wie hingeklebt“, „Gefühl der Leere“) wirken Teil C und Teil D. Sie zuerst setzen und gegen die
  Zielbilder prüfen.

## Lieferung

| Teil | Bericht | Skripte unter `skripte/` |
|---|---|---|
| A Taxonomie | `assets-taxonomie.md` | `assets-taxonomie.json` (eine Ebene höher), `taxonomie_erzeugen.py` |
| C Fels organisch | `verteilung-fels-organisch.md` | `felsgruppen_plan.py`, `felsgruppen_regeln.json` |
| D Leere füllen | `verteilung-leere-fuellen.md` | `mittelschicht_plan.py`, `mittelschicht_regeln.json`, `spuren_plan.py`, `spuren_regeln.json` |
| B1 Nordküste (fjord, kueste, bergwald) | `verteilung-nordkueste.md` | `nordkueste_plan.py`, `nordkueste_regeln.json` |
| B2 Aue | `verteilung-aue.md` | `aue_plan.py`, `aue_regeln.json` |
| B3 Heide/Tundra | `verteilung-heide-tundra.md` | `heide_tundra_plan.py`, `heide_tundra_regeln.json` |
| B4 Gletscher/Frost | `verteilung-hochgebirge.md` | `hochgebirge_plan.py`, `hochgebirge_regeln.json` |
| B5 Elfenwald | `verteilung-elfenwald.md` | `elfenwald_plan.py`, `elfenwald_regeln.json` |
| B6 Sumpf | `verteilung-sumpf.md` | `sumpf_plan.py`, `sumpf_regeln.json` |
| B7 Dschungel inkl. Karst | `verteilung-dschungel.md` | `dschungel_plan.py`, `dschungel_regeln.json` |
| B8 Lava | `verteilung-lava.md` | `lava_plan.py`, `lava_regeln.json` |
| B9 Wüste/Canyon/Ödland (nur ergänzen) | `verteilung-wueste.md` | `wueste_ergaenzung_plan.py`, `wueste_ergaenzung_regeln.json` |

Jeder Bericht enthält Witcher-Analyse mit Quellen, Regelwerk-Erklärung, Testanleitung mit Prüfkameras, Einkaufsliste und den Abschnitt
„Korrektur Runde 1“.

## Ausführen

Alle Planer haben dieselbe Kommandozeile. Die Regeldateien aller Biome müssen im selben Ordner liegen, weil die drei Querschnitts-Planer
deren Overrides lesen.

```
python -I -X utf8 felsgruppen_plan.py A5 G4 --basis <production-Wurzel> [--bild] [--faktor 1.0]
python -I -X utf8 <biom>_plan.py      A5 G4 --basis <production-Wurzel>
python -I -X utf8 spuren_plan.py      A5 G4 --basis <production-Wurzel>
python -I -X utf8 mittelschicht_plan.py A5 G4 --basis <production-Wurzel>
```

- **Reihenfolge beim Planen (seit Runde 2):** lava, felsgruppen, übrige Biom-Planer, spuren, mittelschicht. mittelschicht liest die Spuren-Ensembles als Blickziele und hält Sichtachsen frei.
- **Reihenfolge beim Setzen:** felsgruppen, dann Biom-Planer, dann mittelschicht, dann spuren.
- **Spires:** `felsgruppen` liest die Spire-Punkte aus `lava/<Feld>/plan.json`. Für Lava-Felder daher `lava_plan.py` vor `felsgruppen`
  laufen lassen. Ohne Lava-Plan greift eine Ersatzmaske mit höchstens 6 Spires je Feld.
- **Exit-Code 2** bedeutet: Pflichtdatei fehlt oder Feld ungültig. In fremden Biomen schreibt jeder Planer einen leeren `plan.json`.
- **Budget:** höchstens 60 000 Instanzen je Feld und Planer, davon höchstens 3 000 mit Kollision. Jede Ausdünnung steht als WARNUNG im Log.

## Erste Prüfung mit Echtdaten

1. `felsgruppen` und `mittelschicht` in A5 und G4 setzen und gegen die Zielbilder halten, wie geplant.
2. In jedem `plan.json` `biome_fenster` und `zellen_zustaendig` lesen. Sind Heide-, Tundra- oder Sumpfgebiete oder Teiche als Kennzahl 0
   kodiert, zählen sie als aue. Dann bleiben die zuständigen Planer dort leer.
3. Für C6 gilt: 3 % bergwald liegt über der 2-%-Schwelle. nordkueste setzt dort einige hundert Instanzen. Für einen Leerplan
   `zustaendigkeit.min_anteil_eigen` in `nordkueste_regeln.json` auf 0.04 setzen.
4. Die Override-Faktoren sind nur synthetisch kalibriert. Nach dem ersten gemeinsamen Lauf je Biom nachstellen.

## Offene Punkte für Runde 2

- **Wüstenfelder:** `mittelschicht` erkennt die vorhandene Namaqualand-Ebene in C3–E5 nicht als belegt. Dort können einzelne Sträucher
  neben vorhandenen stehen.
- **Fehlende Spuren-Netze:** Mühle, Boot, Laternen, Steinbrücke, Gipfelkreuz, Unterstand und Seilbrücke sind geregelt, haben aber kein
  Netz im Inventar. Torfstich hat keine Instanzen-Spur.
- **Einkauf:** Die Einkaufslisten stehen je Bericht im Abschnitt „Einkaufsliste“. Fab war aus der Cloud nicht erreichbar, die Namen sind
  deshalb Fab-Suchbegriffe.
- Korrekturen bitte wie bisher als `auftraege/verteilung-<thema>-korrektur.md` oder als neue Runde.
