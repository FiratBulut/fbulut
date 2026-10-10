# Eldarien – Datenformate und Konventionen für Verteilungs-Skripte (Stand 10.10.2026)

Für Cloud-Agenten, die Verteilungs-/Planer-Skripte schreiben. Die Skripte laufen **nicht in der Cloud**, sondern lokal auf dem
Projekt-PC (Windows 11, Python 3.11, NumPy, numba, Pillow; `python -I`), und zwar in zwei Stufen:

1. **Planer (offline, reines Python):** liest die Weltdaten (unten), schreibt Instanzlisten je Gitterfeld. Kein Unreal nötig.
2. **Setzer (Unreal-Editor-Python):** liest die Instanzlisten und setzt sie als Foliage (HISM) oder Akteure. Dafür gibt es bereits
   generische Setzer; ein neuer Planer soll das **vorhandene Setzer-Format** bedienen, dann ist kein neuer Setzer nötig.

Alle Pfade relativ zu `production/` (= `D:\Das Lied der Asche\ELDARIEN_ENVIRONMENT_SKILLS_V1\production\`).

## 1. Welt und Raster

- Landschaft 9577 × 7057 m im **1-m-Raster**, `NX = 9577`, `NY = 7057`. Rasterzelle `(i, j)` (Zeile i = Nord-Süd, Spalte j = West-Ost)
  ↔ Unreal-Welt `X_cm = (j − 4730,5) · 100`, `Y_cm = (i − 4060,5) · 100`. Meeresspiegel Z = 0.
- 70 Gitterfelder `A1 … J7`, je **1008 m**: Spalte `s` (A = 0 … J = 9), Zeile `r` (1 … 7) → `j ∈ [s·1008, (s+1)·1008)`,
  `i ∈ [(r−1)·1008, r·1008)`. 62 Felder haben Land (Tabelle `daten/biome_je_feld.md`).
- Unreal-Einheit cm; Rotation als **Quaternion** (x, y, z, w); Maßstab als Faktor je Achse.

## 2. Weltdaten (`export/unreal/welt/`, alle Raster NY × NX, zeilenweise, little-endian, ohne Kopf)

| Datei | Typ | Inhalt |
|---|---|---|
| `hoehe.f32` | float32, Meter | Geländehöhe (= Unreal-Höhe ≤ 1,2 cm) |
| `lage_<Name>.r8` | uint8 0–255 | Deckung der Bodenlage (Gewicht des Landschaftsmaterials): Wiese, Gras, Trockengras, Laub, Nadeln, Moos, Heide, Kraut, Erde, Lehm, Schlamm, Sand, Kies, Geroell, Fels, Felsplatte, Sandstein, Schnee, Eis, Lavafels, Lavasand, Algen |
| `karte_wasser.r8` | uint8 | > 0 = Wasserfläche (Flüsse, Seen, Bäche, Teiche, Meer) |
| `karte_weg.r8` | uint8 | > 0 = Weg/Straße (Abstand halten: 2,5 m Kleinzeug, 4 m Bäume/Felsen) |
| `karte_ort.r8` | uint8 | > 0 = Ort/Bauwerk (Abstand 5 m) |
| `eigner.r8` + `welt.json` | uint8 | Houdini-Kachel-Kennzahl je Zelle; `welt.json["kacheln"][k]["rezept"]` = **Biom** (0 = Weltgelände → `aue`, Vulkanregion → `lava`) |
| `wasser_welt.json` | JSON | `fluesse` (je Feld: `punkte` [x_cm, y_cm, z_cm, breite_cm, …]), `seen` (`umriss` [[x, y], …], `spiegel_cm`), `wasserfaelle` |
| `baeche/baeche.json`, `baeche/baeche_r2.json`, `teiche/teiche.json` | JSON | Bäche (Punkte mit Breite), Teiche (Umriss) |
| `instanzen/instanzen.json` | JSON | Houdini-Bestand (Bäume, Sträucher, Felsen, Orte): `verzeichnis[]` mit `name`, `ref` (Unreal-Pfad), `klasse`, `n`, `grenzen_cm` |
| `witcher/<Feld>/`, `bestand/<Feld>/`, `ufer/foliage_<Feld>/`, `felsschalen/plan_<Feld>.json` | f32/JSON | bereits gesetzte Ebenen (Abschnitt 4) – ein neuer Planer muss sie kennen (Abstand, Ersetzen) |
| `docs/staedte/standorte.json` | JSON | geplante Stadt-/Dorfstandorte (frei halten) |

Biome (15): `aue, bergwald, gletscher, tundra, canyon, oedland, heide, elfenwald, dschungel, kueste, wueste, lava, frost, sumpf, fjord`.
Wüstenfelder `C3 C4 D3 D4 D5 E3 E4 E5` haben einen eigenen Planer (Namaqualand) – dort nur ergänzen, nicht ersetzen.

## 3. Instanzformat (das ALLE Setzer lesen)

`<Netzname>.f32`: je Instanz **10 float32 LE**: `x, y, z` (cm, Weltkoordinaten), `qx, qy, qz, qw` (Quaternion), `sx, sy, sz` (Maßstab).
Dazu je Feld ein `plan.json`:

```json
{"stand": "…", "feld": "G4", "instanzen": 17152,
 "dateien": {"SM_beech_tree_01": {"pfad": "/Game/Forest_Environment_Set/Environment/Foliage/Models/SM_beech_tree_01",
                                  "anzahl": 822, "gruppe": "buche", "rolle": "baum", "sichtweite": [0, 0],
                                  "schatten": true, "kollision": true}},
 "entfernen": "sm_beech_tree_0,sm_forest_pine_0",          # optional: Netznamen-Präfixe alter Instanzen, die im Feld gelöscht werden
 "ft_ordner": "/Game/Eldarien/Welt/Foliage/<Thema>", "ft_praefix": "FT_EL_<KUERZEL>_"}
```

- `pfad` = Unreal-Paketpfad des Static Mesh (aus dem Inventar `daten/netze.csv`, Spalte `pfad`), ohne `.Name`.
- `sichtweite` [Start, Ende] in cm (0 = unbegrenzt). Richtwerte: Kiesel/Laub/Zweige 3 500–9 000, Kleinzeug 10 000–15 000, Sträucher
  25 000–40 000, Blöcke/Totholz 35 000–60 000, Bäume/Hero-Felsen 0.
- `kollision`: nur für Bäume, Felsen > 0,8 m, liegende Stämme. Kleinzeug nie.
- Bodenhöhe: `z` = Geländehöhe (bilinear aus `hoehe.f32`) **minus** Eingraben (Felsen 25–45 % der Netzhöhe, Steine 30–50 %, Stämme 20–35 %,
  Pflanzen 2–5 cm). Netzmaße (min/max der Bounds in cm) stehen in `daten/netze_masse.json` (451 Netze) bzw. `daten/netze.csv` (alle).
- Drehung: Z-Achse auf die Geländenormale kippen (Felsen/Steine voll, Sträucher 30 %, Bäume 0–10 %), dann Zufalls-Yaw.
- Felder sind **deterministisch**: Zufall aus (Rasterkoordinate, Seed) ableiten, Planung im Fenster Feld + Rand (48–64 m), damit
  Nachbarfelder ohne Nahtsprung passen. Nichts auf Wasser, Weg, Ort, Standorte; Hang > 40° nur Felsen/Kletterpflanzen.
- Größenordnung je Feld (gesetzt und flüssig): Witcher-Ebene 50 000 Kleinzeug, Wald-Bestand 17 000 Bäume, Ufer 26 000 Steine,
  Felsschalen 500–2 500 Stücke. Richtwert für eine neue Ebene: ≤ 60 000 Instanzen je Feld, davon ≤ 3 000 mit Kollision.

## 4. Bereits vorhandene Ebenen (nicht doppelt planen, sondern einfügen/ersetzen)

| Ebene | Planer (lokal) | Setzer (Editor) | Foliage-Typen | Inhalt |
|---|---|---|---|---|
| Houdini-Bestand | – (Export) | – | Houdini-Akteure/Foliage | Bäume, Sträucher, Felsen, Orte aus Houdini (`instanzen.json`) |
| Wüste | `scripts/wueste_bewuchs/` | eigener | `FT_EL_WU_*` | Namaqualand-Wüste (C3–E5) |
| Witcher-Bewuchs | `scripts/witcher_bewuchs/wit_plan.py` | `witcher/wit_setzen.py` | `FT_EL_WIT_*` | Haine, Waldsaum, Totholz, Unterwuchs, Farne, Laub/Zweige, Blumeninseln, Gebüsch |
| Wald-Bestand | `scripts/bestand/bestand_plan.py` | `witcher/bestand_setzen.py` | `FT_EL_BST_*` | Baum-Ebene neu: Gruppen 8–40 m, Lichtungen 15 %, Höhen 0,7–1,3, Artenmix, Totholz 3 % (G4 gesetzt) |
| Ufer | `scripts/ufer/ufer_plan.py` | `wassertest/ufer_setzen.py` | `FT_EL_UF_*` | Kiesel, Kopfsteine, Blöcke, Platten, Treibholz an allen Ufern (5 Felder gesetzt) |
| Felsschalen | `scripts/felsschalen/fs_plan.py` | `felsschalen/feld_setzen.py` + `fs_foliage_setzen.py` | `FT_EL_FS_*` + Akteure | Offene Klippen-Schalen an Steilwänden (Rück-/Unterseite im Gelände), kleine Stücke als Foliage |
| Klippen (neu) | `scripts/klippen/klippen_plan.py` | `ue_klippen_setzen.py` | Akteure | Fab-Klippennetze als Wandfronten (A5/B5 geplant) |
| Landschafts-Gras | Landschaftsmaterial | – | `GT_*` (19 Grasarten) | GPU-Gras 0,2–1,2 m aus Bodenlagen, nur um die Kamera |

Ein neuer Biom-Planer liefert deshalb **eine oder mehrere neue Ebenen** (z. B. `mittelschicht/<Feld>/`, `felsgruppen/<Feld>/`,
`spuren/<Feld>/`) im Format aus Abschnitt 3, plus optional `entfernen`-Filter für Ebenen, die er ersetzt.

## 5. Was ein Cloud-Skript enthalten soll

```
python -I scripts/<thema>/<thema>_plan.py FELD [FELD …] [--bild] [--faktor 1.0]
```
- Liest nur `export/unreal/welt/*` (+ Inventar), schreibt nur nach `export/unreal/welt/<thema>/<Feld>/` (f32 + plan.json) und
  `docs/pruefung/<thema>/<Feld>.png` (Draufsicht 1 px = 1 m, Farben je Klasse) bei `--bild`.
- Regeln als **eigene JSON-Datei** (`<thema>_regeln.json`: Dichten, Gruppen, Größen, Eingraben, Biomfaktoren), damit sie ohne Code
  änderbar sind. Oben im Skript: Kurzbeschreibung, Aufruf, Quellen.
- Laufzeit ≤ 60 s je Feld (NumPy/numba; keine Python-Schleifen über 1 M Zellen). Fehlende Dateien → klare Meldung, kein Absturz.
- Keine Unreal-Importe im Planer. Setzer-Hinweise (Foliage-Typ-Einstellungen, Kollision, Sichtweiten) in `plan.json["dateien"]`.
- Jeder Netzname muss im Inventar existieren (`daten/netze.csv`); fehlende Wunsch-Assets stattdessen in die Einkaufsliste.
