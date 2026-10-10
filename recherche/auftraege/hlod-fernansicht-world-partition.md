# Auftrag 10: Fernansicht ohne Löcher – HLOD für Landschaft, Foliage und Felsen in World Partition (UE 5.8.3)

Kontext: Eldarien, UE 5.8.3, World Partition mit 1-km-Zellen (70 Gitterfelder A1…J7, 9,6 × 7 km), Nanite-Landschaft (266 Streaming-Proxys, je 8 × 8
Komponenten à 126 m, 1-m-Raster), Runtime Virtual Texture für den Boden, Foliage als HISM (Felsschalen `FT_EL_FS_*`, Bäume, Gras per Landscape Grass),
große Felsen als Static-Mesh-Akteure (Nanite), Epic-Water-Flüsse je Zelle. Streaming-Quelle = Spieler/Editor-Kamera. Problem in den Bildern: entferntes
Gelände fehlt oder erscheint spät (z. B. ein Grat 1–1,5 km entfernt ist nicht geladen, während die Felsen-Foliage darauf schon sichtbar ist →
„schwebende Felsen“; Küstenlinien in 3–5 km fehlen; bei 24 × 24 km Ozean sieht man den Horizont, aber keine Inseln). Es wurden noch nie HLODs gebaut.

**Frage 1 – Landschaft in der Ferne:** Wie bleibt eine Nanite-Landschaft in World Partition 5.8 in 2–10 km Entfernung sichtbar? Optionen: (a) Landscape-
HLOD (Landscape-Proxys in HLOD-Layer, `WorldPartitionHLODsBuilder`, Einstellungen „HLOD Layer“ an den Proxys, Texturgrößen, Build-Dauer für 266 Proxys),
(b) größere Streaming-Reichweite der Landschafts-Zellen („Runtime Grid“ mit eigener Loading Range für Landschaft vs. 1-km-Zellen für Details),
(c) „Landscape Streaming Proxies außerhalb des Grids“ / Data Layers / „Is Spatially Loaded = false“ für die Landschaft (Speicherkosten bei 266 Nanite-Proxys),
(d) Fern-Mesh (gebackenes Low-Poly der ganzen Insel als Static Mesh mit RVT-Fernfarbe) – wie machen es Epic-Beispiele (Project Titan 8 × 8 km, City Sample)?
Bekannte 5.8-Fallen (Forum: Landscape-HLOD backt Normale falsch, RVT-Fernfarbe schwarz, Nanite-Landscape + HLOD) mit Quellen.

**Frage 2 – Foliage/Felsen/Bäume in der Ferne:** HLOD-Layer-Typen (Instancing, Merged Mesh, Simplified Mesh, Approximated) für HISM-Foliage und Nanite-
Static-Meshes; was in 5.8 mit Nanite praktisch funktioniert, Build-Zeit/Speicher je 1-km-Zelle (Erfahrungswerte), wie man HLOD-Layer per Python/Editor-
Skript zuweist (`WorldPartitionHLODUtilities`, `HLODLayer`-Assets, `set_editor_property('hlod_layer')` an Akteuren/Foliage-Typen), wie man den Builder aus
der Kommandozeile fährt (`-run=WorldPartitionBuilderCommandlet -Builder=WorldPartitionHLODsBuilder`), inkrementell nur für geänderte Zellen.

**Frage 3 – Reihenfolge und Risiken:** Welche Reihenfolge ist für eine Welt, an der noch täglich Gelände/Foliage geändert wird, sinnvoll (HLOD erst spät?
oder jetzt mit kleinem Layer-Satz, Builds nachts)? Speicher (Festplatte ≥ 60 GB frei halten, RAM 47 GB), Risiko für den Editor (Builder im eigenen
Prozess, Editor muss zu sein?), was ein Spieler ohne HLOD sieht (Streaming-Range vergrößern als Notlösung: Kosten).

Antwort als kompakter deutscher Bericht mit Quellen (Epic-Doku 5.6–5.8, Foren, Talks) und einer Schritt-Liste mit Befehlen/Python-Snippets (ungetestet
markiert). Ergebnis als Datei `recherche/antworten/hlod-fernansicht-world-partition.md`.
