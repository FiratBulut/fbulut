# Auftrag 13 – Sehenswürdigkeiten (8 je Biom): Status

Stand: 2026-10-11 11:35 UTC. Koordinator: Cloud-Session. Wird bei jedem Push aktualisiert.

## Phase 1

| Teil | Inhalt | Stand |
|---|---|---|
| A | Download-Liste für Ferat (`sehens-downloadliste.md`, `sehens/downloadliste.json`) | **Vorfassung gepusht**: 34 Pakete (A 9, B 13, C 12), A+B ca. 49,5 GB geschätzt; Top-10 kostenlos bzw. schon gekauft. Preise/Größen/Versionen ungeprüft (fab.com aus der Cloud nicht erreichbar). Wird nach den Biom-Entwürfen nachgeschärft (Ort-IDs, fehlende Formen). |
| Baukasten | `skripte/sehens_lib/` (Laden 2 m, Hang/Krümmung/Abfluss, Sichtbarkeit vom Weg, Kandidatensuche, Draufsicht-PNG, Format-Prüfer `sehens_pruefen.py`) | fertig, gepusht (Selbsttest auf echten 2-m-Daten ohne Fehler; Grenzen: Bäume nur 4-m-Näherung, 1-m-Lader nur synthetisch getestet) |
| B/C | Katalog + `sehens/<biom>/standorte.json` + Draufsichten je Ort | Welle 1: B1 aue · B2 bergwald (fertig) · B3 elfenwald+dschungel · B7 lava. Welle 2: B4 gletscher+frost+fjord (läuft) · B5 tundra+heide · B6 canyon+wueste+oedland · B8 kueste+sumpf |
| D | diese Datei | laufend |

## Biome

| Biom | Stand | Orte |
|---|---|---|
| bergwald | fertig (Prüfer 0 Fehler/0 Warnungen) | Leuchtfeuer: 01 Der Mönch (Felsnadel), 02 Die Brandkiefer (Blitzbaum), 03 Säulenhain (Riesentannen); Fundstücke: 04 Felsenmeer, 05 Klemmblock-Klamm mit Schleierfall, 06 Karsee, 07 Windwurf, 08 Der Wurzelstein |

## bildwuensche

- bergwald: Mönch und Säulenhain `_fern`, Klamm und Karsee `_held` (Kameras in `sehens/bergwald/standorte.json`)

## Offene Fragen

- bergwald: Reicht für den Mönch eine hochkant gestellte Granit-Schale `veqnci0db_tier_2` (kein echtes Felsnadel-Netz)? Dürfen Nicht-Nanite-Nadelbäume liegend (Windwurf) und 2,5-fach skaliert (Säulenhain) gesetzt werden, oder auf Forest Cretaceous warten? Geländestempel ±6 m für den Karsee in B5 in Ordnung?
