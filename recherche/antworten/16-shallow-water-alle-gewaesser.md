# Entscheidung 16 – Shallow Water River für alle Bäche und Flüsse (dynamische Welt)

Stand 12.10.2026. **Ferat hat entschieden:** Alle Bäche und Flüsse laufen mit Epics **Shallow Water River**. Es geht nicht um einen Vorschlag
und nicht um einen Test mit offenem Ausgang. Ziel ist eine dynamische Welt: Später gesetzte Felsen und Geländeänderungen soll das Wasser selbst
erkennen, ohne Neuplanung.

## Umbau (verbindlich)

| Teil | Wer liefert | Was |
|---|---|---|
| Gelände, Stufen, Becken, Lippen | Planer (unverändert, 13f-Regel bleibt) | Form des Bachbetts |
| Wasseroberfläche Bäche + Flüsse | **WaterBodyRiver + ShallowWaterRiver** | Strömung, Füllen der Becken, Umfließen von Hindernissen, Kehrwasser |
| Fälle (Stufe ≥ 1 m, Schwelle wird im Einrichtungstest geprüft) | Kaskadennetz-Vorhang + Niagara (Nature Water FX) + Schaumobjekte | was 2D nicht kann |
| Hindernisse | jede Instanz/jeder Akteur im Wasser oder ≤ 1 m daneben: `wasser_kollision: true` | Wasser erkennt Felsen automatisch |
| Seen | bleiben `WaterBodyLake` | nicht Teil dieser Entscheidung |

**Planer-Ausgabe (neu):** Je Gewässerstrecke eine Liste `fluss_sim` mit Abschnitten zwischen den Fällen. Jeder Abschnitt hat Splinepunkte
(Lage, Breite, Tiefe, Fließgeschwindigkeit). Dazu je Fall einen Eintrag mit oberem/unterem Abschnitt, Vorhang, Effekten und Schaumobjekten
sowie eine Liste aller Objekte mit Wasser-Kollision. Das lokale Bau-Werkzeug erzeugt daraus `WaterBodyRiver` + `ShallowWaterRiver` und
setzt die Kollision.

**Bisherige Kaskadennetz-Oberfläche** in Becken und flachen Strecken wird durch die Simulation ersetzt. Ob sie als ferne Darstellung bleibt,
hängt von Reichweite und Kosten der Simulation ab (Einrichtungstest unten).

**Offene Risiken (ehrlich):**
- Kosten in einer offenen Welt mit über 160 Strecken sind unbekannt. Wahrscheinlich ist ein Simulationsbereich um den Spieler nötig, der Rest
  als ruhender WaterBodyRiver.
- Ein Forenbericht meldet einen Startfehler in 5.7.4. Laut Ferats Video läuft es in 5.8.
- Ob Wasser-Kollision bei instanzierten Felsen (HISM/Foliage) wirkt, ist offen.

## Einrichtungstest (lokal, vor dem Gesamtbau)

Die Teststrecken und Fragen unten bleiben gültig. Sie dienen jetzt der **Einrichtung**: Werte, Schwelle für Fälle, Reichweite, Budget,
Kollisionseinstellung. Es ist keine Ja/Nein-Entscheidung mehr.

---
*Ursprünglicher Vorschlag (zur Nachvollziehbarkeit):*

## Kurzfazit (Vorschlag)

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
| **Nachbearbeitung:** einen Megascans-Felsen (Static Mesh) mitten in den Fluss stellen und Landschaft leicht modellieren, dann Reset. Reagiert die Strömung auf beides oder nur auf die Landschaft? Braucht der Fels Kollision bzw. Distance Field? | Ferats Wunsch: Details später ändern, ohne neu zu planen |

## Entscheidung danach

- **Läuft gut und Export möglich:** Wir übernehmen Flowmap, Tiefe und Schaum als Feld je Kaskadennetz. Der Planer liefert dann nur noch Stufen, Gelände und Fälle.
- **Läuft gut, aber nur live:**
  - Wir setzen Shallow Water nur an Sehenswürdigkeiten ein, nah am Spieler.
  - Grenzen: höchstens etwa 1,5 ms GPU; zusammen mit den Niagara-Effekten höchstens 8 gleichzeitig (bestehende Regel).
  - Fern übernimmt das Kaskadennetz.
- **Läuft nicht, oder nicht auf Stufen:** Wir bleiben beim Kaskadennetz und den SLW2-Werten.
- **Fluid Flux** (kostenpflichtig, kann Zustände einbacken) bleibt erst einmal draußen. Eine Frage für Ferat wird es erst, wenn der kostenlose Weg nicht reicht.

## Nachtrag: Fälle bleiben beim Kaskadennetz, dazu gezielt platzierter Schaum

Ferat (12.10.): Für die Wasserfälle ist das Kaskadennetz wahrscheinlich besser geeignet; realistischer wird es, wenn man nur Schaum gezielt platziert. Dafür sind
nach dem Test diese Schaumarten als eigene Objekte vorgesehen, statt nur Vertexschaum im Netz:

| Art | Wo | Form |
|---|---|---|
| Aufprallteppich | Fallfuß jeder Stufe ≥ 1 m | unregelmäßiger Fleck, Radius ≈ 0,5–1 × Fallhöhe, an den Rändern ausgefranst |
| Schaumstraßen | vom Aufprall talwärts in Hauptströmung | 2–6 dünne, gebogene Streifen, 2–4 m lang, auslaufend |
| Kehrwasserschaum | Buchten und hinter Randblöcken (15g) | kleine kreisende Flecken, ruhend |
| Gischt | Fälle ≥ 3 m | Niagara aus Nature Water FX (bestehende Effekte, `cull_m` aus 13k) |

Die Umsetzung erfolgt als Decals bzw. flache Schaumkarten (Netze und Materialien nur aus dem vorhandenen Inventar). Liefert Shallow Water später eine
Strömung, folgen die Schaumstraßen ihr; sonst folgen sie der `mittellinie`. Den Planer-Ausbau (Feld `schaum_objekte` je Kaskadennetz) mache ich, sobald
die Bilder von C2 Version 3 und dem Test da sind.

## Nachtrag: Felsen brauchen Wasser-Kollision

Ferat (12.10., aus dem Video): Felsen werden von der Simulation erkannt, wenn bei ihnen die **Wasser-Kollision** eingestellt ist. Folgen:

- **Test:** Den Felsen aus der Testfrage „Nachbearbeitung“ einmal mit und einmal ohne diese Einstellung prüfen. Den genauen Namen der Einstellung bzw. des
  Kollisionsprofils in 5.8.3 bitte zurückmelden. Prüfen, ob sie auch bei **instanzierten** Felsen (ISM/HISM, Foliage) wirkt oder nur bei einzelnen Akteuren.
- **Planer (nach dem Test):** Jede Instanz und jeder Akteur, der im Wasser oder bis 1 m daneben steht (Blöcke in Stufen, Randblöcke aus 15g, Felsnasen),
  bekommt ein Feld `wasser_kollision: true`. Das lokale Bau-Werkzeug setzt damit die Einstellung automatisch, auch bei späteren Neuplanungen.
- **Handarbeit später:** Von Hand gesetzte Felsen im Fluss brauchen dieselbe Einstellung. Am einfachsten geht das über eine eigene Kollisions-Voreinstellung
  bzw. ein Editor-Werkzeug „Wasser-Kollision an Auswahl“. Dann reagiert das Wasser nach einem Reset bzw. Neu-Einbacken ohne neue Planung.

## Rückfrage

- Ferat: Wie heißt das Video bzw. der Kanal? Dann kann ich die gezeigten Einstellungen gezielt nachrecherchieren.

## Quellen

- [Epic Forum: Community Tutorial „New in Unreal Engine 5.6 – Shallow Water River“](https://forums.unrealengine.com/t/community-tutorial-new-in-unreal-engine-5-6-part-2-how-to-float-objects-on-your-shallow-water-river-simulation/2583650)
- [Epic Forum: ShallowWaterRiver startet nicht in 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772)
- [Epic Doku: Water Body Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-body-actors-in-unreal-engine)
- [Epic Doku: Fluid Simulation Overview (Niagara Fluids)](https://dev.epicgames.com/documentation/unreal-engine/fluid-simulation-in-unreal-engine---overview)
- [Epic Forum: Tutorial Shallow Water Simulation with Niagara Fluids](https://forums.unrealengine.com/t/tutorial-shallow-water-simulation-with-niagara-fluids/1786912)
- [80.lv: Fluid Flux](https://80.lv/articles/fluid-flux-a-cool-water-simulation-system-for-unreal-engine/)
