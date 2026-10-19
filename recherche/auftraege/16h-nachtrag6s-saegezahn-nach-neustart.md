# Auftrag 16h-6s – Sägezahn/„Wasserplatte“ an der Mündung entsteht nach jedem Editor-Neustart und verschwindet erst nach einer Landschaftsänderung

Stand 19.10.2026 16:30. Bezug: Antwort 16h-6r §2 (Sägezahn-Test), Stand T6N1b (gespeichert, `render_state` BAKED_SIM, smoothing_width 1).
Bilder: `bilder/swr_p2/saegezahn_muendung_reihe.jpg` (8 Zeilen A–H, je 2 Ausschnitte derselben Kamera „muendung“),
`bilder/swr_p2/saegezahn_wasserplatte_editor.jpg` (Editor-Ansicht in Bodennähe am C3-Kopf, zufällig per HighResShot aufgenommen).

## 1. Ergebnis T6R (6r §2) – Material ist es nicht

- Kontrolle −24 sowie A −48, B −12 und C 0 als Kopie von `MI_EL_SWR_Klar`: an allen drei Plätzen angekommen, also SWR `baked_sim_material`,
  `SWR_Fluss…water_material` und `SWR_Arm…water_material`.
- **Der Sägezahn ist in allen Stufen gleich** (Reihe A/B). K1/K4/K5 zeigen nur Rauschen; schon die Kontrolle weicht im Mittel 18–24/255 von IST ab
  (Lumen/Animation).
- Nebenbefund: `UpdateRenderState` stellt das `water_material` der Quell- und Senken-Wasserkörper **nicht** um. Wir setzen es jetzt direkt
  (`set_water_material`).
- `UseBakedSim` haben wir nicht mehr getestet. Laut 6r gilt: Wirkt keine Stufe, dann ist es Geometrie.

## 2. Neuer Befund – der Fehler hängt am Zustand nach dem Editorstart

| Zeile | Zustand | Sägezahn / senkrechte Wasserwände |
|---|---|---|
| A, B | T6R, 13–30 min nach hartem Neustart | ja |
| C | 15:56, nach der Bodenlagen-Kette C2 (siehe unten) | **nein, glatter Rand** |
| – | dasselbe mit Wasserzone C3 auf 4096 statt 1024 (nur Speicher) | nein (also auch nicht die Zonenauflösung) |
| D | 16:04, frisch nach hartem Neustart ohne Speichern | ja |
| E | +5 min warten | ja |
| F | Konsole `r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames 10` + 30 s | ja |
| G | Viewport-Echtzeit an + 60 s | ja |
| H | Wasserzonen C2/C3/D2 neu aufbauen lassen (`zone_extent` per `set_editor_property` geändert und zurückgesetzt) | ja |

Was die Bodenlagen-Kette vor Zeile C getan hat, ist das Einzige, was den Fehler bisher beseitigt hat:

1. `write_layers_rect_ex` in C2: 18 Komponenten, 4 Blöcke, nur Lagen, keine Höhen.
2. Speichern der Landschaftsteile C2.
3. Neuimport der Bewuchs-Texturen `T_Eldarien_Bewuchs_A–D` (4096²).
4. `rebuild_grass_maps` und `build_landscape_nanite_for` für die 17 Teile von C2.
5. `grass.FlushCache`.

Die Mündung liegt 5 m innerhalb von C3 (Y = −2039 m, Feldgrenze C2/C3 bei −2044,5 m). Die Zonen C2 und C3 überlappen dort.

**Wasserplatte (zweites Bild):** Am C3-Kopf liegt das Wasser wie eine Platte über dem trockenen Kiesbett. Die Ränder sind senkrecht, die Kante
ist gestuft mit etwa 1 m Schrittweite. Der Ausschnitt ist ein Editorbild aus Bodennähe.

## 3. Was wir in UE 5.8 sehen (Kopf `WaterAdvanced/Public/ShallowWaterRiverActor.h`)

- Öffentlich sind `UpdateRenderState()`, `Rebuild()`, `Bake()`, `OnWaterInfoTextureArrayCreated(const UTextureRenderTarget2DArray*)` (UFUNCTION),
  `BottomContourLandscapeActors`, `bUseCapture`, `BottomContourCaptureOffset` und `WaterInfoTexture` (RT-Array).
- Die Wasserzone hat in Python **kein** `mark_for_rebuild`. Verfügbar sind nur `on_water_info_texture_array_created` und
  `water_info_texture_array(_num_slices)`.
- Unsere Plugin-Funktionen (C++, eigenes Plugin, erweiterbar):
  - `swr_set_render_state` (= `UpdateRenderState`)
  - `swr_rebuild`
  - `swr_bake`
  - `swr_info`
  - `swr_dump_baked`
- Ob der Fehler auch **im Spiel** auftritt, ist ungeprüft. PIE im Viewport lief mit Teleport an die Mündung. Das HUD-Foto wurde aber nicht
  geschrieben, und `HighResShot` traf den Editor-Viewport statt des Spiels.

## Fragen

1. **Mechanismus:** Was zeichnet im Zustand BAKED_SIM senkrechte, gestufte Wasserwände? Eine Wasser-Info, deren Bodentiefe noch ohne
   (gestreamte) Landschaft gerendert ist? Ein Höhen-Capture der SWR? Etwas anderes? Und warum heilt es eine Lagenänderung der Landschaft, während
   ForceUpdateWaterInfo und der Zonen-Neuaufbau nicht helfen?
2. **Auslöser im Editor:** Welcher billigste Schritt ohne Inhaltsänderung bildet den Effekt der Bodenlagen-Kette nach? Dann können wir ihn nach jedem
   Neustart ausführen bzw. vor jedem Prüfbild. Bitte als Reihenfolge von Einzeltests (je ein Bild), billigster zuerst.
3. **Spiel:** Tritt das nach eurer Kenntnis auch in PIE bzw. im gepackten Spiel auf? Welche dauerhafte Abhilfe empfehlt ihr? Möglich wäre etwa
   eigener C++-Code im WorldSubsystem unseres Plugins (`EldarienMap`) nach dem Laden der Landschaft, oder eine Einstellung an SWR, Zone bzw.
   Wasserkörper.
4. **Prüfweg im Spiel:** Wie nehmen wir ein PIE-Bild aus einer festen Kamera auf? Das HUD-Foto (FScreenshotRequest) wurde im Viewport-PIE nicht
   geschrieben.

## Was wir parallel tun

Nichts mehr am Wasser, bis eure Antwort da ist. Prüfbilder des Bachs entstehen ab jetzt erst nach einer Landschaftsänderung, oder sie werden als
„nach Neustart“ markiert.
