# Antwort 16h-6s – Wasserplatte nach Editorstart: wahrscheinlich ein veralteter Boden-Bezug der SWR-Darstellung; sechs Einzeltests, billigster zuerst; dauerhaft per Subsystem oder `bUseCapture`

Gelesen: recherche/auftraege/16h-nachtrag6s-saegezahn-nach-neustart.md @ e1505773808d70404f1b5cf22e0a14c563dfc461 (Commit 034e372)

Stand 19.10.2026. Bezug: 16h-6r (e8fa4d7) §2, Stand `T6N1b_2` (BAKED_SIM, Breite 1). Bearbeiter: Cloud-Recherche. Bilder
`bilder/swr_p2/saegezahn_muendung_reihe.jpg` und `saegezahn_wasserplatte_editor.jpg` selbst angesehen.

## Kurzfazit

1. **Material ausgeschlossen – bestätigt.** Die Offset-Klammer hat keine Wirkung; damit gilt die Abbruchregel aus 6r, der Fehler ist Geometrie.
   Den Nebenbefund (das Wasser der Quell- und Senkenkörper wird nicht mit umgestellt) bitte im Bericht festhalten.
2. **Mechanismus – wartet auf Beleg, wahrscheinlichste Erklärung:**
   - Im Bild sieht man ein Wasserprisma über trockenem Kies, mit senkrechten Wänden und Stufen von etwa 1 m. Das passt zum 1-m-Raster der
     Simulation: Zellen, die die Darstellung für nass hält, werden mit flacher Oberseite und senkrechtem Rand gezeichnet.
   - Nass gilt dann, wo der gebackene Spiegel über dem **Boden-Bezug der Darstellung** liegt. Ist dieser Bezug nach dem Start zu tief oder
     fehlt er (Landschaft noch nicht bzw. in alter Fassung gezeichnet), entsteht die Platte.
   - Erneuert wird der Bezug offenbar nur durch ein Ereignis „Landschaft geändert“. Die Wasserzone (ForceUpdateWaterInfo, Zonen-Neuaufbau)
     erneuert ihn nicht. Deshalb halfen F und H nicht [Hypothese H1].
   - Zwei Gegenhypothesen:
     - **H2:** eine veraltete Nanite-Darstellung der Landschaft im Boden-Bezug;
     - **H3:** World-Partition-Streaming, d. h. die Landschaft war beim Erfassen nicht geladen.
3. **Auslöser – beantwortet als Testreihe:** sechs Einzeltests, billigster zuerst. Vor jedem Test harter Neustart, damit der Fehler sicher
   vorliegt. Je Test ein Bild und ein Dump-Vergleich, damit der Bake unverändert bleibt (§2). Der erste Test, der heilt, nennt den
   Mechanismus.
4. **Spiel – wartet auf Beleg:** Ob es im Spiel auftritt, wissen wir nicht. Wahrscheinlich ja, wenn H1 oder H3 zutrifft (gleicher Ablauf beim
   Laden).
   - **Dauerhafte Abhilfe**, je nach Testergebnis: entweder `bUseCapture` aus, falls die SWR den Boden dann aus den Landschaftsdaten liest;
     oder ein Schritt im `EldarienMap`-WorldSubsystem, der den heilenden Auslöser auslöst, sobald die Landschaft im SWR-Bereich geladen und
     gezeichnet ist (§3).
5. **PIE-Bild – beantwortet:** feste CameraActor als View Target, `HighResShot` im Kontext der PIE-Welt auslösen. Alternativ ein
   Standalone-Start mit Befehlszeile. Die API-Namen sind in 5.8 zu prüfen (§4).

---

## 1. Was die Bilder zeigen (selbst angesehen)

| Zeile | Bild |
|---|---|
| A, B, D–G | Rechts der Mündung ein treppiger Rand mit senkrechten, hellen Wasserwänden. Links staffelt sich die Wasserfläche in Stufen über den Kies. |
| C | Glatter Rand, die Wasserfläche folgt dem Bett. Der Unterschied zu D ist deutlich, das ist kein Rauschen. |
| H | Unverändert fehlerhaft, Wand am Ufer sichtbar. |
| Editorbild | Eine flache Wasserplatte etwa 0,3–0,5 m über trockenem Kiesbett, senkrechte, gestreifte Seitenwände, Kante in Stufen von etwa 1 m |

**Folgerung:**

- Die Oberfläche selbst ist der gebackene Spiegel; Lage und Höhe der Platte passen zum Wasser.
- Falsch ist die **Ausdehnung**: Trockene Zellen werden als nass gezeichnet.
- Die senkrechten Wände sind die Ränder dieser Zellen, also kein Materialeffekt.

## 2. Einzeltests, billigster zuerst

**Rahmen je Test:**

- harter Neustart ohne Speichern; 0 ungespeichert bestätigen;
- Mündungskamera und Editorkamera am C3-Kopf: Bild vorher und nachher;
- `swr_dump_baked` vorher und nachher. Der Bake muss bitgleich bleiben, sonst ist der Test ungültig.

Es wird nichts gespeichert.

| Nr | Test | Kosten | heilt, wenn … |
|---|---|---|---|
| T1 | `swr_set_render_state(BAKED_SIM)` erneut setzen, also denselben Zustand | 1 Aufruf | die Darstellung den Boden-Bezug beim Umschalten neu holt (H1, über den Zustand) |
| T2 | `BottomContourCaptureOffset` auf **denselben** Wert setzen, mit PostEditChange (`set_editor_property`) | 1 Aufruf | das Erfassen des Bodens an einer Eigenschaftsänderung hängt (H1, über die Erfassung). **Achtung:** Prüft der Dump-Vergleich ein Zurücksetzen des Bakes, gilt der Test als „verändert den Bake“ und bekommt Speichersperre. |
| T3 | `bUseCapture` aus (nur Speicher) | 1 Aufruf | die SWR dann den Boden aus den Landschaftsdaten statt aus einer Bildaufnahme liest. Das wäre zugleich die dauerhafte Lösung (§3). |
| T4 | `build_landscape_nanite_for` nur für die C3- und C2-Teile im Umkreis von 100 m um die Mündung, **ohne** Lagenänderung | Minuten | die Nanite-Darstellung der Landschaft veraltet war (H2) |
| T5 | `write_layers_rect_ex` auf **einer** Komponente an der Mündung, mit **identischen** Lagenwerten (vorher gelesen) | Minuten | allein das Ereignis „Landschaft geändert“ den Bezug erneuert (H1, über das Ereignis) |
| T6 | World Partition: Bereich um die Mündung ausdrücklich laden, warten bis geladen, dann T1 | Minuten | die Landschaft beim Erfassen nicht geladen war (H3) |

**Reihenfolge:**

- Bricht ab, sobald ein Test heilt. Das Ergebnis heißt dann: Auslöser X genügt, Mechanismus Hn.
- Heilt keiner, bleibt die volle Bodenlagen-Kette der einzige Weg. Dann ihre Schritte einzeln abtragen: 1 ohne 3–5, dann 4 allein.
- Prüfbilder bis dahin wie geplant nur nach einer Landschaftsänderung, oder ausdrücklich als „nach Neustart“ markiert.

## 3. Dauerhafte Abhilfe (nach dem Testergebnis)

| Ergebnis | Abhilfe |
|---|---|
| T3 heilt und das Bild ist sonst gleich | `bUseCapture = false` am SWR-Akteur speichern. Bake-Dump vorher und nachher bitgleich; Bildpaar an K1/K4/K5/Mündung |
| T1 oder T2 heilt | Im `EldarienMap`-WorldSubsystem: nach dem Laden warten, bis alle Landschaftsteile in den SWR-Grenzen registriert und gezeichnet sind (WP-Streaming fertig, Nanite bereit), dann einmal den heilenden Aufruf. In Editor und Spiel |
| T4 heilt | Nanite der Landschaft vor jedem Speichern bzw. Kochen aktuell halten (Build-Schritt in der Kette). Im gepackten Spiel ist die Nanite-Landschaft gebacken. Ob der Kochschritt sie neu baut, ist **zu prüfen** |
| T6 heilt | wie T1/T2, mit Streaming-Bedingung im Subsystem; zusätzlich SWR-Bereich und Landschaft im selben WP-Datenlayer oder immer geladen |

Bei allen Abhilfen gilt: keine Änderung am Bake, keine Änderung an Spline oder Gelände.

## 4. PIE-Bild aus fester Kamera

- **Kamera:** ein CameraActor an der Mündungsposition, nur im Testlevel bzw. nur im Speicher. In PIE `PlayerController.set_view_target_with_blend(Kamera)`.
- **Aufnahme in der PIE-Welt:** Den Konsolenbefehl im Kontext der Spielwelt ausführen, nicht im Editor. Zum Beispiel:

  ```python
  # Kontext Spielwelt holen und dort den Screenshot ausloesen (Namen in 5.8 zu pruefen)
  welt = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
  unreal.SystemLibrary.execute_console_command(welt, "HighResShot 1920x1080")
  ```

  Die Dateien liegen dann unter `Saved/Screenshots/`. Die PIE-Ansicht muss in Echtzeit zeichnen. Danach einige Frames warten (Tick-Rückruf),
  nicht im selben Python-Aufruf auslesen.
- **Ausweichweg:** Standalone-Start (`-game -windowed -ResX=1920 -ResY=1080`) mit Teleport per Konsole und `HighResShot`. Das kommt dem gepackten
  Spiel am nächsten.
- **Warum das HUD-Foto fehlte [Vermutung]:** `FScreenshotRequest` wird vom Viewport verarbeitet, der gerade zeichnet. Im eingebetteten PIE ist
  das nicht unbedingt der angesprochene. Den Weg über die Spielwelt-Konsole nehmen.

## 5. Nächste Handlung

**T1–T6 nach §2**, im Speicher, je mit hartem Neustart davor. Mit dem ersten heilenden Test endet die Reihe.

- **Danach:** dieselbe Kamera in PIE nach §4. Ist der Fehler dort auch nach Neustart vorhanden, wird die Abhilfe nach §3 gebaut.
- **Erfolg:** ein benannter Auslöser oder eine Einstellung, Bake-Dump bitgleich, Bildpaar Mündung vorher und nachher, Ergebnis in PIE.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Verlässliche Wasserdarstellung nach jedem Laden:** Eine Wasserplatte über trockenem Kies wäre im Spiel ein grober Fehler, schlimmer
   als jeder Sägezahn.
2. **Weicher Wasserrand** (6r): erst sinnvoll zu beurteilen, wenn der Startzustand stimmt.
3. **Kantenbewuchs und Steine an der Wasserlinie** (6q/16h-Bettschritt).

## Quellen

- `recherche/auftraege/16h-nachtrag6s-saegezahn-nach-neustart.md` (Commit 034e372), Bilder `bilder/swr_p2/saegezahn_muendung_reihe.jpg`,
  `saegezahn_wasserplatte_editor.jpg` (selbst angesehen)
- `recherche/antworten/16h-nachtrag6r-rauschband-muendung.md` §2 (Commit e8fa4d7)
- Eigenschaften aus `WaterAdvanced/Public/ShallowWaterRiverActor.h` laut Auftrag §3 (`bUseCapture`, `BottomContourCaptureOffset`,
  `BottomContourLandscapeActors`, `UpdateRenderState`, `Rebuild`). Was `bUseCapture` genau umschaltet, ist nicht belegt; deshalb steht es
  als Test T3, nicht als Behauptung.

## Rückfragen

Keine.
