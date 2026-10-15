# Eldarien – Lieferformat Sehenswürdigkeiten (Auftrag 13, Stand 11.10.2026)

**Korrekturhinweis 15.10.2026:** Formate und aktuelle Projektbefunde unterscheiden.
Grassteuerung und Niagara-Bestand wurden unten berichtigt. Die übrigen Bestandsangaben
sind auf den ursprünglichen Stand datiert und vor Verwendung am
[maßgeblichen Inventar](daten/zusammenfassung.md) prüfen.
Für Übergabe und Abnahme gilt die [README](../README.md).

Ergänzt `FORMAT.md` (Raster, Koordinaten, Instanzformat). Alles hier beschreibt, was ein **Sehenswürdigkeiten-Planer** schreiben soll,
damit ich (Claude lokal) es ohne Rückfragen in Unreal 5.8 umsetzen kann. Die Planer laufen lokal (`python -I`, NumPy/numba/Pillow) auf den
1-m-Daten; zum Testen in der Cloud liegen dieselben Karten in 2 m unter `vorlagen/daten/sehens/` (Kodierung in `legende.json`).

## 1. Aufruf und Daten

```
python -I sehens_<biom>.py [--orte ID …] [--bild] [--daten2m <Ordner>] [--aus <Ordner>]
```
- Ohne `--daten2m`: liest die 1-m-Originale aus `export/unreal/welt/` (FORMAT.md §2: `hoehe.f32`, `lage_*.r8`, `karte_weg.r8`,
  `karte_ort.r8`, `karte_wasser.r8`, `eigner.r8` + `welt.json`, Wasser-JSONs, `docs/staedte/standorte.json`).
- Mit `--daten2m vorlagen/daten/sehens`: dieselbe Logik auf den 2-m-PNGs (Cloud-Test). Gleiche Orte bei gleichem Seed, nur gröber.
- Ausgabe (Standard `export/unreal/welt/sehens/<biom>/`, sonst `--aus`): `orte.json`, `gelaende/`, `lagen/`, Vorschaubilder; Instanzen in
  der Ebene `export/unreal/welt/sw_<biom>/<Feld>/` (Abschnitt 4).
- Deterministisch (Seed je Ort), Laufzeit ≤ 3 min je Biom, keine Unreal-Importe, fehlende Dateien → klare Meldung.

## 2. `orte.json` (eine Datei je Biom, Liste von Orten)

```json
{"stand": "2026-10-1x", "biom": "aue", "orte": [{
  "id": "aue_01_blautopf", "name": "Blautopf", "art": "fundstueck",
  "kurz": "Kreisrunder, tiefblauer Quelltopf am Hangfuß, aus dem ein Bach entspringt.",
  "mitte_cm": [123400, -45600, 8120], "radius_m": 45, "felder": ["E5"],
  "standort_begruendung": "Hangfuß mit Mulde (Krümmung …), 140 m vom Weg K14, Bachanfang …",
  "sicht": {"naechster_weg_m": 140, "sichtbar_ab_m": 0},
  "gelaende": {"datei": "gelaende/aue_01_blautopf.f32", "fenster_ij": [i0, j0, hoehe, breite], "max_aenderung_m": 6.5},
  "lagen": {"datei_praefix": "lagen/aue_01_blautopf_", "fenster_ij": [i0, j0, hoehe, breite], "lagen": ["Kies", "Moos", "Schlamm"]},
  "wasser": [ … Abschnitt 5 … ],
  "effekte": [ … Abschnitt 6 … ],
  "materialwuensche": [ … Abschnitt 7 … ],
  "kameras": [["E5", 125000, -47000, 123400, -45600, 8300, "aue_01_blautopf_anmarsch", 170], …],
  "marker": {"titel": "Der Blautopf", "text": "1–2 Sätze im Ton des Romans (Dark Fantasy, kein Kitsch)", "entdeckung_m": 30},
  "assets_wunsch": [{"paket": "Fab: …", "statt_jetzt": "SM_… (aus Inventar)"}],
  "budget": {"instanzen": 6200, "kollision": 340, "akteure": 34, "lichter": 1, "niagara": 0, "decals": 6}
}]}
```
- `art`: `leuchtfeuer` (von weitem sichtbar, zieht vom Weg) oder `fundstueck` (erst aus der Nähe, belohnt Erkunden).
- `fenster_ij`: Zeile i0, Spalte j0 (1-m-Raster), Höhe, Breite. Der Planer schreibt bei 1-m-Daten immer 1-m-Dateien.

## 3. Gelände (`gelaende/<id>.f32`, optional) und Bodenlagen (`lagen/<id>_<Lage>.r8`, optional)

- **Delta-Höhe in Metern**, float32, zeilenweise, Größe = Fenster. Ich schreibe sie mit unserer Höhen-Pipeline (je Feld zwei Phasen),
  verschiebe Pflanzen/Akteure im Fenster mit und baue Gras-Karten neu – das kostet Editorzeit: **nur ändern, wo die Form es braucht.**
- Regeln: Rand des Fensters Δ = 0 mit weichem Übergang ≥ 8 m; |Δ| ≤ 40 m (mehr nur begründet); keine Änderung ≤ 3 m an Wegen
  (`karte_weg > 0`) und an bestehendem Wasser (`karte_wasser > 0`), außer der Ort IST dieses Wasser; keine geschlossenen Senken ohne
  Wasser/Abfluss (es regnet im Spiel nicht, aber es sieht falsch aus); Landschaft kann **keine Überhänge** – Bögen, Tore, Höhlen,
  Pilzfelsen, überhängende Wände sind Netze (Akteure) auf dem Gelände, mit Fuß im Boden.
- **Bodenlagen**: uint8-Zielgewicht 0–255 je genannter Lage (Namen exakt wie FORMAT.md §2: Wiese, Gras, Trockengras, Laub, Nadeln, Moos,
  Heide, Kraut, Erde, Lehm, Schlamm, Sand, Kies, Geroell, Fels, Felsplatte, Sandstein, Schnee, Eis, Lavafels, Lavasand, Algen).
  Ich setze `neu = max(alt, ziel)` und skaliere die übrigen Lagen, damit die Summe 255 bleibt. Weiche Ränder (≥ 3 m), fleckig statt Kreis.
  **Ersetzt durch lokalen Befund 16h/6i §5:** Die Grasdichte hängt dort an separaten
  Bewuchskarten `v_*.r8`, nicht direkt an diesen Lagen. Eine Dichtemaske gezielt auf die
  betroffenen Bewuchskarten anwenden und Texturen/Gras-Karten lokal erneuern. Betroffene
  Karten und Ablauf vor Umsetzung lokal prüfen; nicht aus einer Lagenänderung eine
  Grasänderung ableiten. [Beleg](../auftraege/16h-nachtrag6i-baked-sim-tests-stand.md).

## 4. Instanzen (Ebene `sw_<biom>`, Format exakt wie FORMAT.md §3)

- Ordner `export/unreal/welt/sw_<biom>/<Feld>/` mit `plan.json` + `<Netz>.f32`. Eine Instanz gehört dem Feld, in dem ihr Ort liegt
  (Rechteck-Regel; Instanzen außerhalb werden vom Setzer des Feldes übersprungen).
- Foliage-Typen entstehen automatisch als `FT_EL_SW<xx>_<Netz>` (xx = erste zwei Buchstaben des Bioms: SWAU, SWBE, SWGL, SWTU, SWCA, SWOE,
  SWHE, SWEL, SWDS, SWKU, SWWU, SWLA, SWFR, SWSU, SWFJ). `ft_praefix`/`ft_ordner` im Plan werden ignoriert.
- **Heldenstücke als Akteure**: Liste `plan["akteure"]` mit `{"netz", "pfad", "x", "y", "z", "qx", "qy", "qz", "qw", "sx", "sy", "sz",
  "klasse": "<ort_id>_<rolle>"}` (≤ 500 je Feld). Alles Kleine als Foliage-Datei.
- Netznamen nur aus `daten/netze.csv` (Stand 11.10.) oder aus der Download-Liste (dann im Plan mit Ersatz aus dem Inventar, bis das Paket da
  ist). Gesperrt: `daten/netz_sperre.json`. Megascans/Fab-Netze bekommen nach dem Setzen unsere Material-Überschreibung (Material-Fix
  läuft bei mir für alle Ebenen `sw_*`; sonst wären sie schwarz) – für euch kein eigener Schritt. Ein Plan darf auch nur `akteure` enthalten. Netze mit Fehlern: `daten/netz_check_ergebnis.json`.
- Bodenhöhe immer aus der **nach** dem Geländestempel gültigen Höhe (Planer rechnet `hoehe + delta`). Eingraben wie FORMAT.md §3.

## 5. Wasser (`wasser`, optional; ich baue es als Epic-Wasser)

| `typ` | Felder | Hinweise |
|---|---|---|
| `see` (auch Teich, Quelltopf, Cenote, Gumpe) | `umriss_cm` [[x, y], …] **gegen den Uhrzeigersinn**, `spiegel_cm`, `tiefe_m`, `farbe` | Ufer muss rundum über dem Spiegel liegen (Gelände ggf. per Stempel) |
| `bach` | `punkte_cm` [[x, y, z, breite_cm], …] (Quelle → Mündung), `tiefe_cm`, `farbe`, `quelle`: true/false, `muendung`: Kennung eines vorhandenen Gewässers oder `versickert` | z = Wasserspiegel; Gefälle stetig; Stufen > 0,8 m werden kleine Wasserfälle |
| `wasserfall` | `kante_cm` [[x, y, z], …] (Lippe links → rechts, Blick talwärts), `fuss_z_cm`, `breite_cm`, `becken`: Kennung eines `see` | Vorhang mit `M_EL_Wasserfall2`, Schaum am Fuß |

`farbe` ∈ `klar`, `tuerkis`, `tiefblau`, `smaragd`, `moorbraun`, `schwarz_spiegel`, `gletschermilch`, `thermal`, `rostrot`, `salzweiss` –
ich lege dafür je eine Wasser-Instanz an. Heiße Quellen: `thermal` + Effekt Dampf (Abschnitt 6).

## 6. Effekte (`effekte`, optional)

| `typ` | Felder | Grenzen |
|---|---|---|
| `punktlicht` / `spotlicht` | `pos_cm`, `farbe` [r, g, b] 0–1, `intensitaet_cd`, `radius_cm`, (`richtung_q`, `kegel_grad`), `schatten`: false | ≤ 4 je Ort, Schatten nur begründet |
| `lokaler_nebel` | `pos_cm`, `radius_cm`, `dichte` (0–1, Richtwert 0,02–0,2), `farbe`, `hoehenabfall` | ≤ 2 je Ort (Local Fog Volume) |
| `niagara` | `asset` (Pfad), `pos_cm`, `rot_q`, `skala` | Bestand anhand Inventar und lokalem Assetpfad prüfen. Fehlende Assets als Wunsch und `"optional": true` kennzeichnen; keine pauschale Annahme „keine Systeme vorhanden“. |
| `decal` | `material` (Pfad aus `inventar_extra.json`), `pos_cm`, `groesse_cm` [x, y, z], `rot_q` | ≤ 12 je Ort |

Die frühere Aussage „KEINE Niagara-Systeme“ ist überholt: der spätere
[Sehens-Status, Phase 2](../antworten/sehens-STATUS.md) benennt Systeme und Niagara-Kopien.
Ein genannter Plan allein beweist aber nicht den heutigen lokalen Assetbestand; exakten
Pfad vor Anwendung prüfen.

Licht: feste Sonne (~24°, 5 900 K), kein Tag-Nacht-Wechsel, Höhennebel W7. Leuchten (Glut, Pilze, Irrlichter) deshalb dezent und nur in
Schatten/Senken wirksam planen; die Wirkung muss auch tagsüber tragen.

## 7. Materialwünsche (`materialwuensche`, optional, ≤ 6 je Biom)

`{"name": "MI_EL_SW_<Kurzname>", "basis": "<Master aus daten/material_parameter.json>", "parameter": {"<Name>": Wert oder [r, g, b, a]},
"fuer": ["SM_…"]}` – nur vorhandene Parameter der Master (`M_EL_Fels_MS`, `M_EL_Fels_Auflage` (Moos/Schnee/Sand obenauf),
`M_EL_Fels_Sand`, `M_EL_Klippe_RVT` (Fußblend + Moos), `M_EL_Pflanze`, `M_EL_Eis4`, `M_EL_Wasserfall2`, `M_MS_Decal`, `M_MS_Base`).
Neue Master-Materialien oder Texturen nur mit Begründung als eigener Punkt (ich baue sie selten und vorsichtig).

## 8. Kameras (für meine Prüfbilder)

`[Feld, KX, KY, ZX, ZY, ZZ, Name, Hoch]` in cm: Kamera (KX, KY), Ziel (ZX, ZY, ZZ absolut). Hoch positiv: Kamerahöhe =
`max(Boden_an_Kamera + Hoch, ZZ + 300)` (Blick von oben). **Hoch negativ = genau |Hoch| über dem Boden** (Augenhöhe: `-170`), ohne die
3-m-Regel (Stand 11.10. 13:00). Ist die Sicht verdeckt, steigt die Kamera in 4-m-Schritten.
Mindestens 3 je Ort: `_anmarsch` (vom nächsten Weg, Augenhöhe, so wie der Spieler den Ort zuerst sieht), `_held` (beste Komposition),
`_nah` (Detail 5–15 m). Leuchtfeuer zusätzlich `_fern` (300–800 m).

## 9. Budgets je Ort (Richtwerte; der Editor muss flüssig bleiben)

≤ 15 000 Instanzen (davon ≤ 1 500 mit Kollision), ≤ 80 Akteure, ≤ 4 Lichter, ≤ 3 Niagara, ≤ 2 Nebel, ≤ 12 Decals, Geländefenster
≤ 400 × 400 m (große Leuchtfeuer bis 600 m, begründet). Je Feld zusammen mit allen Ebenen ≤ 60 000 neue Instanzen.
