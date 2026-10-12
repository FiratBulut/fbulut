# Vorschlag 16 – Test „Shallow Water River“ (Epic) an C2

Stand 12.10.2026. Ferat fragte, warum wir nicht mit Unreals Shallow-Water-Fluss arbeiten. Laut Ferat zeigt ein Video, dass er in 5.8 gut läuft.
Die Cloud kann YouTube nicht öffnen; das Video selbst habe ich nicht gesehen. Dieser Vorschlag ist ein **Test für die lokale Instanz**, kein Umbau.

## Kurzfazit

- **Shallow Water River** ist seit UE 5.6 Teil von Water + Niagara Fluids und kostenlos. Er simuliert die Wasseroberfläche eines Flusses (`WaterBodyRiver`):
  Strömung um Hindernisse, Füllen von Becken, Wellen. Die Lage des Flusses gibt weiter die Spline vor.
- **Erwartung:** Ränder, Strömung und Schaum werden natürlicher. Die 15g-Punkte „eckiger Schaum“ und „gerade Ränder“ könnte er besser lösen als Regeln.
- **Grenze:** Er rechnet 2D, also eine Höhe pro Punkt. Senkrechte Fälle und Vorhänge (Stufen ≥ 3 m) kann er nicht darstellen. Die bleiben bei Kaskadennetz und Niagara.
- **Plan:** Zuerst testen, ob er auf unseren gebauten Stufen läuft und was er kostet. Danach entscheiden:
  - **Hybrid:** Unser Kaskadennetz liefert Stufen und Fälle, Shallow Water den Abschnitt in Spielernähe.
  - **Einbacken:** Wir übernehmen nur Strömung, Tiefe und Schaum als Flowmap bzw. Vertexwerte.

## Test (lokal, etwa 1–2 h)

1. **Plugins:** Water und Niagara Fluids aktiv.
2. **Abschnitt T1:** C2 Version 3, etwa 40 m um `kn0_nah_s119` mit 3–4 Lippen und einer Gumpe.
   - `WaterBodyRiver` entlang der `mittellinie` aus dem Plan (`0e00d17`) setzen. Breite und Tiefe je Punkt aus `breite` / `tiefe_cm`.
   - `ShallowWaterRiver` setzen, mit dem Fluss verknüpfen und Reset.
   - Das Kaskadennetz in diesem Abschnitt für den Test ausblenden.
3. **Abschnitt T2:** Treppenbach am Karsee mit dem 10,8-m-Fall S00. Hier soll sich zeigen, wo die Grenze liegt.
4. **Abschnitt T3:** ein flacher Abschnitt mit Biegung, als Vergleich.

### Bitte zurückmelden

| Frage | Wozu |
|---|---|
| Läuft die Simulation auf eigenem Fluss + 1-m-Gelände? Ein Forenbericht meldet einen Startfehler in 5.7.4, einzeln und unbestätigt. | Grundvoraussetzung |
| Füllt sie die Becken bis zur Lippe und fließt über die Lippen? | Kernfrage für Stufen |
| Verhalten an Stufen 0,3–1 m bzw. ≥ 3 m | Grenze 2D |
| GPU-Zeit (`stat GPU`, `stat Niagara`) je Abschnitt, Größe und Auflösung des Simulationsbereichs | Budget offene Welt |
| Läuft sie nur um die Kamera oder über den ganzen Fluss? Wie weit reicht sie? | Hybrid-Planung |
| Kann man Höhe, Geschwindigkeit und Schaum als Textur oder Zustand **speichern**? (Render Target exportieren, Einback-Funktion) | Einbacken ja/nein |
| Bilder von denselben Kameras wie in 15g: `s1`, `kn0_unten`, `kn0_nah_s119` | Vergleich mit Version 3 |

## Entscheidung danach

- **Läuft gut und Export möglich:** Wir übernehmen Flowmap, Tiefe und Schaum als Feld je Kaskadennetz. Der Planer liefert dann nur noch Stufen, Gelände und Fälle.
- **Läuft gut, aber nur live:**
  - Wir setzen Shallow Water nur an Sehenswürdigkeiten ein, nah am Spieler.
  - Grenzen: höchstens etwa 1,5 ms GPU; zusammen mit den Niagara-Effekten höchstens 8 gleichzeitig (bestehende Regel).
  - Fern übernimmt das Kaskadennetz.
- **Läuft nicht, oder nicht auf Stufen:** Wir bleiben beim Kaskadennetz und den SLW2-Werten.
- **Fluid Flux** (kostenpflichtig, kann Zustände einbacken) bleibt erst einmal draußen. Eine Frage für Ferat wird es erst, wenn der kostenlose Weg nicht reicht.

## Rückfrage

- Ferat: Wie heißt das Video bzw. der Kanal? Dann kann ich die gezeigten Einstellungen gezielt nachrecherchieren.

## Quellen

- [Epic Forum: Community Tutorial „New in Unreal Engine 5.6 – Shallow Water River“](https://forums.unrealengine.com/t/community-tutorial-new-in-unreal-engine-5-6-part-2-how-to-float-objects-on-your-shallow-water-river-simulation/2583650)
- [Epic Forum: ShallowWaterRiver startet nicht in 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772)
- [Epic Doku: Water Body Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-body-actors-in-unreal-engine)
- [Epic Doku: Fluid Simulation Overview (Niagara Fluids)](https://dev.epicgames.com/documentation/unreal-engine/fluid-simulation-in-unreal-engine---overview)
- [Epic Forum: Tutorial Shallow Water Simulation with Niagara Fluids](https://forums.unrealengine.com/t/tutorial-shallow-water-simulation-with-niagara-fluids/1786912)
- [80.lv: Fluid Flux](https://80.lv/articles/fluid-flux-a-cool-water-simulation-system-for-unreal-engine/)
