# Auftrag 16f – Recherche: Bachbett mit dem UE-5.8-Water-Plugin (Brush) in großer World-Partition-Welt, Witcher-Qualität

Stand 12.10.2026, 22:45. **Ferat:** „Gib der Cloud-Sitzung Recherche, sie soll in UE-Foren nachschauen – es gibt bestimmt viele Berichte, wie man
es am besten macht – und dir einen Bericht geben.“ Seine Richtung (12.10. abends): Bachbetten **inkl. Becken mit dem Water-Plugin von UE 5.8**
formen (nicht mehr mit gestempelten Plänen), danach die Plugin-Einstellungen anpassen, bis Witcher-Qualität erreicht ist; direkt in der echten Welt.

## Unsere Lage (Zahlen)
- Landschaft 9577 × 7057 m (1 m/Punkt), World Partition, 266 Landschaftsteile, Bearbeitungsebenen „Houdini“ (Basis) + „Water“.
- Erlenbach C2: EIN WaterBodyRiver (75 Punkte, 405 m, U-Schleife: Hin- und Rückweg ~40 m auseinander) + Shallow Water River (SWR, 1536, gebacken,
  WCBS, match_spline 2, remove_outside_spline 50, source_size 10 m) + ein Arm als zweite Quelle.
- WaterBrushManager per Editor-Fabrik angelegt und per C++ (`ALandscape::AddBrushToLayer`) an die Ebene „Water“ gehängt (sonst kannte er 0 Körper).
- **Befunde:**
  1. Log: „Landscape edit layers merge requires a minimum batch size of resolution 7057x4537, which is higher than the current desired maximum
     batch resolution 1024x1024 (landscape.BatchedMerge.MaxResolutionPerRenderBatch)“ – läuft trotzdem; Editor-Zusage +20 GB.
  2. Flüsse graben nach der **Tiefe je Spline-Punkt**; `ChannelDepth` 256 → 80 ändert die Mitte praktisch nicht. Becken/Schnellen damit steuerbar,
     Mitte trifft das Soll auf 10–15 cm.
  3. **Curl Noise** (0,4/0,2 und sogar 0,05/0,02) erzeugt bis **22 m** Fehler – die U-Schleife: Höhen der beiden Schleifenhälften vermischen sich.
  4. **Fremde Ellipsen/Balken 40–65 m neben dem Bach** (bis 21 m tief), obwohl der Brush Manager nur unseren Fluss meldet (`GetWaterBodies` = 1) und alle
     geladenen anderen Körper „Affects Landscape“ aus haben – vermutlich zwischengespeicherte Formen von Seen/Bächen ungeladener Zellen
     (WaterBodyBrushCacheContainer?). Auch mit frischem Brush Manager da.
  5. Zwei Läufe mit gleichen Einstellungen unterscheiden sich in 4 438 Zellen (bis 21 m) – nicht deterministisch.
  6. Falloff „Width“ 6 m + Rampe 3 m schneidet in der engen Schlucht 15 m tiefe Kanten in die Wände; „Angle“ 60° noch mehr große Schnitte; erst Falloff 1 m +
     Rampe 1,5 m lässt die Wände unberührt (0 Zellen > 10 m neben der Mitte geändert, 7 Zellen > 5 m).
  7. Gebackene SWR-Fläche = exakt das Spline-Band (99,7 %), Tiefe Median 1,25 m – die Simulation „malt“ das Band aus (match_spline).
- Unser Weg zum Festschreiben: Brush-Ergebnis auslesen (`sample_landscape_heights`), Korridor um den Fluss als Delta in die Weltdaten, Feld für Feld in
  die Basisebene schreiben, Brush Manager löschen (nie speichern).

## Bitte recherchieren (Foren, Epic-Doku/Release-Notes 5.4–5.8, Talks, Breakdowns, Witcher-4-Demo/Unreal Fest)
1. **Best Practice Flussbett mit Water-Brush in großen WP-Landschaften:** Gibt es Berichte zu den Befunden 1, 4, 5 (Batch-Größe, Geisterformen aus
   ungeladenen Zellen, Nicht-Determinismus)? Empfohlene CVars (`landscape.BatchedMerge.*`), Brush-Cache leeren, Region-/Teil-Brushes, Workarounds.
2. **Alternativen in 5.8:** Landscape Patch (Plugin „LandscapePatch“), „Water Body Landscape Patch“ o. ä., PCG Water Interop, Mesh Partition Water –
   was nutzt Epic heute für Flussbetten in großen Welten? Wie wurden Flüsse in der Witcher-4-UE5-Demo / Electric Dreams / anderen Epic-Samples gemacht?
3. **Einstellungen für natürliche Gebirgsbäche:** Kanal (Rampe, Elevation Curve), Falloff, Effekte (Displacement-Textur statt Curl Noise?),
   Gewichtskarten (Kies/Schlamm im Bett), Becken-Schnellen-Folge über Spline-Tiefe/-Breite; Rezepte aus Foren mit Zahlen.
4. **Shallow Water River danach:** match_spline / match_spline_height_amount / remove_outside_spline / source_size – Werte, damit das Wasser dem
   gegrabenen Bett natürlich folgt statt das Spline-Band auszumalen; Schaum nur an Fällen (Ferat), Tempo nach Gefälle (16e).
5. **Witcher-Look Wasser:** klare Bäche mit sichtbarem Grund, Weißwasser an Schnellen, Steine/Totholz; Material-/Niagara-Tipps aus Breakdowns.
Bitte als Bericht `recherche/antworten/16f-water-plugin-bachbett-recherche.md` mit Quellen (Links) und **konkreten Empfehlungen/Zahlen** für unsere
Lage; Unsicheres als unsicher kennzeichnen.
