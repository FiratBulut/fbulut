# Auftrag 13 – Sehenswürdigkeiten (8 je Biom): Status

Stand: 2026-10-11 12:05 UTC. Koordinator: Cloud-Session. Wird bei jedem Push aktualisiert.

## Phase 1

| Teil | Inhalt | Stand |
|---|---|---|
| A | Download-Liste für Ferat (`sehens-downloadliste.md`, `sehens/downloadliste.json`) | **Vorfassung gepusht**: 34 Pakete (A 9, B 13, C 12), A+B ca. 49,5 GB geschätzt; Top-10 kostenlos bzw. schon gekauft. Preise/Größen/Versionen ungeprüft (fab.com aus der Cloud nicht erreichbar). Wird nach den Biom-Entwürfen nachgeschärft (Ort-IDs, fehlende Formen). |
| Baukasten | `skripte/sehens_lib/` (Laden 2 m, Hang/Krümmung/Abfluss, Sichtbarkeit vom Weg, Kandidatensuche, Draufsicht-PNG, Format-Prüfer `sehens_pruefen.py`) | fertig, gepusht (Selbsttest auf echten 2-m-Daten ohne Fehler; Grenzen: Bäume nur 4-m-Näherung, 1-m-Lader nur synthetisch getestet) |
| B/C | Katalog + `sehens/<biom>/standorte.json` + Draufsichten je Ort | Welle 1: B1 aue (fertig) · B2 bergwald (fertig) · B3 elfenwald+dschungel · B7 lava (fertig). Welle 2: B4 gletscher+frost+fjord (läuft) · B5 tundra+heide (läuft) · B6 canyon+wueste+oedland (läuft) · B8 kueste+sumpf |
| D | diese Datei | laufend |

## Biome

| Biom | Stand | Orte |
|---|---|---|
| aue | fertig (Prüfer 0 Fehler/0 Warnungen; Mondarm nur mit neuem Ufergehölz-Gürtel voll verdeckt) | Leuchtfeuer: 02 Die Alte (Riesen-Stieleiche), 03 Schwalbenwand (Prallhang-Lehmwand), 04 Treibholzwerder (Kiesinsel mit Treibholz); Fundstücke: 01 Biberstau, 05 Lilienrinne, 06 Mondarm (Altwasser), 07 Blautopf (Quelltopf), 08 Lianenhalle (Auwald) |
| lava | fertig mit Abweichung: 5 regelkonforme Orte in `standorte.json` (Prüfer 0 Fehler; 2 Warnungen Wegabstand 324/393 m), 3 weitere in `standorte_kratersteig.json` nur mit neuem Pfad „Kratersteig“ (Ost 624 m, West 898 m, max. 22°) – auf dem Vulkan liegt kein Weg | Leuchtfeuer: 01 Die Schwarze Mauer (Stromkante mit Schlotturm), 02 Schwefelgrund (Fumarolenfeld), 03 Die Kraterkinder (Pseudokrater); Fundstücke: 04 Das Röhrenfenster (eingestürzte Lavaröhre mit Farnoase), 05 Die Klare Spalte (Grundwasserspalte); mit Kratersteig: 06 Die Kraterreihe (Leuchtfeuer), 07 Die Basaltorgel, 08 Das Glutauge |
| bergwald | fertig (Prüfer 0 Fehler/0 Warnungen) | Leuchtfeuer: 01 Der Mönch (Felsnadel), 02 Die Brandkiefer (Blitzbaum), 03 Säulenhain (Riesentannen); Fundstücke: 04 Felsenmeer, 05 Klemmblock-Klamm mit Schleierfall, 06 Karsee, 07 Windwurf, 08 Der Wurzelstein |

## bildwuensche

- aue: fünf Bildwünsche mit Kameras in `sehens/aue/asset_bedarf.json`
- lava: Kraterreihe (heutige Kachel), Westschlucht, Stromfront, Kraterkinder-Senke (Kameras in `sehens/lava/asset_bedarf.json`)
- bergwald: Mönch und Säulenhain `_fern`, Klamm und Karsee `_held` (Kameras in `sehens/bergwald/standorte.json`)

## Offene Fragen

- aue: Für Die Alte auf das Eichenpaket (Quercus Robur) warten oder Schwarzpappel aus dem Bestand (×1,3)? Megascans-Erlen (European Black Alder) schon in der Bibliothek? Einverstanden mit 220 m neuem Ufergehölz am Mondarm (sonst kein echtes Fundstück)? Darf für die Brutröhren der Schwalbenwand eine eigene kleine Decal-Textur erzeugt werden?
- **lava: Soll der Kratersteig gebaut werden (dann 8 Orte), oder wird für das Lava-Biom die Regel 80–300 m vom Weg gelockert?** Der Gipfelkrater ginge nur mit Serpentinen (Kegel 30–40°). Basalt Columns AssetKit (ca. 11 €) für die Basaltorgel kaufen?
- bergwald: Reicht für den Mönch eine hochkant gestellte Granit-Schale `veqnci0db_tier_2` (kein echtes Felsnadel-Netz)? Dürfen Nicht-Nanite-Nadelbäume liegend (Windwurf) und 2,5-fach skaliert (Säulenhain) gesetzt werden, oder auf Forest Cretaceous warten? Geländestempel ±6 m für den Karsee in B5 in Ordnung?
