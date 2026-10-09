# Boden-Kleinzeug und Gras wie in Witcher 3/4 (UE 5.8)

**Projekt:** Eldarien – Dark-Fantasy-Open-World-RPG, Third Person, Landschaft 9,6 × 7 km (Landscape 1-m-Raster, 22 Lagen, Nanite-Landschaft mit Tessellation, Lumen, Virtual Shadow Maps, Runtime Virtual Texture, World Partition in 1-km-Zellen). Umsetzung mit Python-Editor-Skripten + eigenem C++-Plugin. Zielplattform PC (RX 7900 XTX 24 GB, 47 GB RAM).
**Unreal-Engine-Version:** 5.8.3
**Priorität:** hoch
**Gewünschter Detailgrad:** ausführlich mit Zahlen und Quellen (Epic-Doku 5.6–5.8, Talks, Forenberichte mit Messwerten)

## Frage
Messlatte ist The Witcher 3 Next-Gen / die Witcher-4-UE5-Demo. Zwei Fragen:

1. **Boden-Kleinzeug:** Dort liegen auf jedem Quadratmeter Kiesel, Zweige, Laub, Zapfen, Wurzeln, kleine Steine in 3D. Welcher Weg ist in UE 5.8 dafür der beste (Qualität, Performance, Streaming in World Partition)? Optionen, die wir kennen: (a) weitere Landscape-Grass-Types mit kleinen Netzen (billig, aber nur um die Kamera), (b) PCG mit PCG Biome Core / Biome Sample (Runtime- vs. Editor-Generation, Hierarchical Generation), (c) Nanite-Foliage-Instanzen (HISM) per Skript, (d) Material-Tricks (Nanite-Displacement, Parallax, Decals). Gesucht: Empfehlung mit Zahlen (Instanzdichten je m², Cull-Distanzen, GPU-Kosten) und Fallen (PCG + World Partition + Landscape-Gras zusammen, Speicher).

2. **Gras:** Was macht Witcher-Gras aus (Dichte, Höhe, Arten-Mischung, Wind, Farbvariation, Interaktion mit dem Spieler) und wie erreicht man das in UE 5.8 mit Landscape Grass Types bzw. PCG (Grass Density, Cull Distance, Wind über Material/Pivot Painter/WPO, Nanite-Foliage für Gras in 5.8 ja/nein)? Welche kostenlosen oder Fab-Grasassets gelten als die besten (Megascans, Electric Dreams, Megaplants …)?

## Kontext
Heute: Landschafts-Gras mit 19 Grass Types über Dichtetexturen (4096², RGBA, eine Art je Kanal), Dichte 100–200 je Komponente, Cull 70–105 m; Foliage-Instanzen (Bäume, Büsche, Farne, Felsen, ~1,5 Mio.) per EldarienTransfer-Plugin (`add_foliage_from_file`) gesetzt. Electric-Dreams-Assets (Hainbuche, Farne, Totholz, Laub) und Megascans sind im Projekt. Grafikspeicher ist knapp (Texturpool 8 GB, Meer-Wasserdaten). Keine Rips aus Spielen empfehlen.
