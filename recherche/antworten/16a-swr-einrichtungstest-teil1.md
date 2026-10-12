# Antwort zu Auftrag 16a – Einrichtungstest Shallow Water River, Teil 1 (Bake, Material, Größe, ISM als Hindernis)

Stand 12.10.2026. Grundlage sind Auftrag 16a (T1 an C2 Version 3, UE 5.8.3), die Bilder `bilder/swr/t1_c2_netz_gegen_swr.jpg` und
`bilder/swr/t1_fels_kollision.jpg`, Datei 16 und `skripte/fluss_sim/README.md`. In dieser Runde ändere ich **kein Skript**. Die
Export-Änderung steht unten nur als Spezifikation.

**Quellenlage (ehrlich):** `dev.epicgames.com`, `forums.unrealengine.com`, die japanischen Leitfäden, 80.lv und GitHub antworten
aus der Cloud mit **Proxy 403** (curl und WebFetch). Alle Belege stammen deshalb aus **Suchmaschinen-Auszügen** der verlinkten
Seiten. YouTube ist gesperrt. Kennzeichnung wie in 14b/16:
- [Doku]: Epic-Doku bzw. Python-API, Auszug
- [Forum]: Epic-Forum, Auszug
- [Leitfaden]: Community-Tutorial, Auszug
- [Projekt]: unsere eigenen Daten (z. B. `vorlagen/daten/material_parameter.json`)
- [Test 16a]: Ferats lokaler Befund
- [Ableitung]: aus den Belegen geschlossen, nicht belegt
- [Schätzung]: Rechnung mit angenommenen Werten
- [ungeprüft]: nur ein Hinweis, Bestätigung fehlt

## Kurzfazit

- **a) Bake.** Gespeichert werden gebackene Texturen am `ShallowWaterRiverComponent` (`baked_water_surface_texture` u. a.) und ein
  `BakedShallowWaterSimulationComponent` mit den Simulationsdaten [Doku]. Diese Daten **gehören dem Water Body** und dienen auch für
  Abfragen und Physik [Doku].
  - Unser eigener Wasser-Master hat bereits die Material-Eingänge `BakedWaterSimTex`, `BakedWaterSimTexVT` (virtuelle Textur) und
    `BakedWaterSimSize` [Projekt]. Das gebackene Ergebnis kommt also als Textur im Water-Body-Material an, auf Wunsch als virtuelle
    Textur [Ableitung].
  - **Speicher [Schätzung]:** etwa **1,1–4,2 MB je 100 m** Bach bei 0,25-m-Zellen, für alle 35,4 km **0,4–1,5 GB** auf der Platte. Im
    Grafikspeicher liegen nur die geladenen Kacheln.
- **`render_state` im Spiel: `WATER_COMPONENT_WITH_BAKED_SIM`.** Nur damit zeichnet der Water Body selbst (Water-Zone-Netz,
  LOD, Material), und Interaktion, Auftrieb und Abfragen funktionieren [Leitfaden, Forum]. `BAKED_SIM` ist die Ersatzlösung. Für
  beide Zustände gibt es Forenberichte, dass gebacken nichts gezeichnet wird → im Teil-2-Test **im gepackten Build** prüfen.
- **„Live nah, gebacken fern“ gibt es nicht als Umschaltung je Entfernung.** Eingebaut ist etwas anderes: gebackene Strömung plus
  eine kleine **Interaktions-Simulation um die Spielfigur** (Shallow-Water-Subsystem, Projekteinstellung; begrenzt aktive Pawns
  und Impulse) [Doku]. Mein Vorschlag: das so nutzen, keine Live-Flusssimulation im Spiel. Ein Konzept für eine Umschaltung je
  Entfernung steht in a), es hängt aber an einer offenen Testfrage (startet `LIVE_SIM` aus dem gebackenen Zustand oder trocken?).
- **b) Material.** `SW_Water_Material` gehört zur Parameterfamilie von Epics `Water_Material`; dieselbe Familie steckt in unserem
  `M_Eldarien_Wasser_Schaum8` [Test 16a, Projekt].
  - **Absorption ist dort eine Absorptions-LÄNGE in cm**: Das Material rechnet 1/Wert und gibt den Kehrwert als SLW-Koeffizienten je cm
    weiter (in 13k von Ferat bestätigt). Die SWR-Standardwerte **20,8/25/24,7** bedeuten also 21–25 cm Sichttiefe in allen Kanälen.
    Daher kommt das deckende Hell-Türkis im Bild.
  - **Startwerte für klares Bergbachwasser:** Absorption **250 / 1 430 / 2 000** (A unverändert). Das sind genau unsere
    0,40/0,07/0,05 je m aus 15g/13k. Streuung und Albedo siehe Tabelle in b).
  - **Schaum:** Die Werte `Sim Foam *`, `SimFoam Contrast`, `Foam Opacity`, `Foam Emissive` (im Standard grünlich!) und
    `Foam Scattering` regeln, wie viel Schaum aus der Simulation sichtbar wird. Startwerte in b).
- **c) Größe.** Eine dokumentierte Obergrenze für `resolution_max_axis` habe ich nicht gefunden.
  - Die Kosten wachsen mit der Zellzahl: T1 hatte 47 616 Zellen bei 0,3–0,6 ms; 512² Zellen kosten hochgerechnet ≈ 1,7–3,3 ms,
    1 024² ≈ 7–13 ms. Das gilt nur im Editor beim Backen [Ableitung].
  - **Empfehlung: ein `AShallowWaterRiver` je Back-Kachel (555), nicht je Abschnitt (1 120) und nicht je Fluss.**
  - Zelle **≤ 0,25 m** an Bächen: `resolution_max_axis` = ⌈längste Kachelseite / 0,25 m⌉, aufgerundet auf ein Vielfaches von 32,
    höchstens 512. Flüsse ≥ 15 m Breite und Kacheln > 128 m bekommen 0,5 m.
  - Verkettung: Die Abschnitte der Kachel stehen in `source_river_water_bodies`, der letzte Abschnitt in `sink_river_water_bodies`.
- **d) ISM/Foliage.** Die Bodenerfassung ist eine **Tiefen-Aufnahme von oben** (Niagara-Datenschnittstelle Scene Capture 2D,
  Schalter `use_capture`) [Forum]. Sie zeichnet **ganze Akteure**: Getaggte Akteure und Einträge in `bottom_contour_actors` kommen
  in die Aufnahme [Leitfaden, Forum, Test 16a].
  - Daraus folgt: **Alle Komponenten und alle Instanzen** eines markierten Akteurs werden erfasst. Instanzen einzeln geht nicht, denn
    eine ISM-Komponente ist ein einziges Grafikobjekt [Ableitung].
  - Ein Etikett am Foliage-Akteur erfasst also auch das Gras. **Lösung:** je Back-Kachel **ein** Akteur `WH_<kachel>`
    („Wasserhindernisse“) mit HISM/ISM-Komponenten, der nur die festen Objekte aus `wasser_kollision` enthält und getaggt ist. Das
    sind 555 Akteure statt 22 825, genau **1 Akteur je Kachel**.
  - **Neue Regel aus der Erfassung von oben:** Ein Stamm, der das Wasser überspannt (Unterkante über dem Spiegel), würde zum Damm.
    Er bekommt keine Wasser-Kollision.
- **Neues Risiko:** Ein Forenbericht zu 5.8 meldet, dass die Tiefenaufnahme Bodenhöhen bei **65 504** abschneidet (Grenze von
  16-bit-Gleitkomma). Bei Ferat lief 5.8.3 an C2 (z ≈ 98 m) richtig. Teil 2 prüft deshalb zusätzlich die höchstgelegene Kachel.

## a) Bake: was gespeichert wird, Speicher, `render_state`, live/gebacken

### a1. Was „Bake“ speichert

| Was | Wo | Beleg |
|---|---|---|
| `baked_sim` (`BakedShallowWaterSimulationComponent`, nur lesbar) | `ShallowWaterRiverComponent` | [Doku] Python 5.5 |
| `baked_water_surface_rt` (Render Target, nur lesbar), `baked_water_surface_texture` (`Texture2D`) | `ShallowWaterRiverComponent` | [Doku] Python 5.5 |
| `BakedFoamTexture`, `BakedWaterSurfaceNormalTexture` | laut Ferat in 5.8.3 vorhanden (Auftrag a) | [Test 16a]; in keinem Auszug gefunden |
| `baked_shallow_water_sim`: „Baked simulation data for this water body, owned by a UShallowWaterRiverComponent“ | `WaterBodyRiverComponent`, `WaterBodyLakeComponent`, `WaterBodyCustomComponent` | [Doku] Python 5.7 |
| Schalter, um die gebackene Simulation für Kollisionen und Abfragen abzuschalten | Water Body (Auszug: „turn off the baked simulation for collisions and other queries“) | [Doku], Name im Auszug nicht wörtlich |
| Material-Eingänge `BakedWaterSimTex` (`Texture2D`), `BakedWaterSimTexVT` (virtuelle Textur), `BakedWaterSimSize` (Vektor) | unser `M_Eldarien_Wasser_Schaum8` (Epic-Familie), Standard leer bzw. `/Water/Textures/BlackVT4x4` | [Projekt] |

**Lesart [Ableitung]:**
- **Darstellung:** In `WATER_COMPONENT_WITH_BAKED_SIM` setzt das Water-Body-Material die gebackene Textur über
  `BakedWaterSimTex`/`…VT` ein. Die Lage auf der Welt kommt über `BakedWaterSimSize`.
- Das Material liest die Strömung bisher aus `WaterVelocityAndHeight` (`Texture2DArray`, Water Info). Deshalb packt die gebackene
  Textur sehr wahrscheinlich **Höhe + Geschwindigkeit (+ Schaum)** in einem RGBA-Texel.
- Die Textur gibt es auch als **virtuelle Textur** (`BakedWaterSimTexVT`). Dann liegen nur sichtbare Kacheln im Speicher.
- **Eigene Darstellung der SWR** (`BAKED_SIM`): Sie nutzt die eigenen gebackenen Texturen (Oberfläche, Schaum, Normale) mit
  `SW_Water_Material_River`.
- **CPU-Daten:** `baked_sim` hält ein Raster für Abfragen (Wassertiefe, Strömung für Auftrieb und Schwimmen). Das gibt es nur,
  weil „Use baked sim for queries/physics“ existiert.
- **Ablage:** Sehr wahrscheinlich als Unterobjekte im Akteur. Unter World Partition liegen sie dann in der Akteur-Datei
  (`__ExternalActors__`) und **streamen mit der Zelle des Akteurs**. Das prüft Teil 2 (T2-2).
- **Auflösung:** Unbelegt. Erwartet wird die Simulationsauflösung (`resolution_max_axis` × proportional), also bei T1 186 × 256.
- **Format:** Unbelegt. Höhe und Strömung brauchen Gleitkomma, wahrscheinlich RGBA16F.

### a2. Speicher je 100 m [Schätzung]

Annahmen:
- Fläche je 100 m aus den drei C2-Kacheln: 75 × 121 + 60 × 107 + 44 × 74 m = 18 751 m² für 203 m Lauf, also **9 237 m² je 100 m**.
  Die Simulation deckt die Bounding-Box ab, nicht nur das Wasser.
- Zellen je 100 m:
  - 0,25 m: 147 800
  - 0,16 m (wie T1): 361 200
  - 0,5 m: 36 900
- Bytes je Zelle, drei Fälle:
  - **8 B**: nur die Spieltextur, RGBA16F
  - **14 B**: dazu Schaum R16F und Normale RGBA8
  - **30 B**: dazu das CPU-Raster mit 4 × float32

| Zelle | B/Zelle | je 100 m | 35,4 km gesamt | mit Mips (+⅓) |
|---|---|---|---|---|
| 0,25 m | 8 | 1,1 MB | 0,39 GB | 0,52 GB |
| 0,25 m | 14 | 2,0 MB | 0,68 GB | 0,91 GB |
| 0,25 m | 30 | 4,2 MB | 1,46 GB | 1,95 GB |
| 0,16 m | 30 | 10,3 MB | 3,6 GB | – |
| 0,5 m | 30 | 1,1 MB | 0,37 GB | – |

- Das sind **Plattenwerte**. Im Grafikspeicher liegt nur, was World Partition geladen hat. Bei einer virtuellen Textur sind es nur die
  sichtbaren Seiten.
- Breite Flüsse (141 Kacheln, 6,3 km) haben mehr Fläche je Meter. Mit 0,5-m-Zellen bleiben sie im selben Rahmen.
- Die Schätzung aus Datei 16 (0,5–2,2 GB) passt dazu. **Teil 2 misst die echten Werte** (T2-2).

### a3. `render_state`: Werte und Bedeutung

Die Aufzählung (`ShallowWaterRenderState`) nennt in keinem Auszug alle Werte. Belegt sind:

| Wert | Bedeutung | Beleg |
|---|---|---|
| `LIVE_SIM` (UI „Live Sim“) | Niagara-Simulation läuft und zeichnet selbst mit `SW_Water_Material_River`. Kostet GPU je Bild (T1: 0,3–0,6 ms). Nach „Bake“ sieht man weiter die Live-Fassung, bis man umschaltet. | [Leitfaden] „was man sieht, ist live sim“ |
| `BAKED_SIM` | Die SWR zeichnet ihr gebackenes Ergebnis selbst, ohne Simulation. Keine Interaktion. | [Leitfaden] |
| `WATER_COMPONENT_WITH_BAKED_SIM` | Der **Water Body** zeichnet über sein normales Wasser-Netz und Material und nutzt dabei die gebackenen Daten. Laut Leitfaden nur so mit Interaktion; laut Forum greifen manche Material-Einstellungen nur hier. | [Leitfaden], [Forum] |
| `WATER_COMPONENT` (vermutet) | normaler Water Body ohne Simulation | [Ableitung aus der Namensreihe] |
| `DEBUG_RENDER_BOTTOM_CONTOUR` und vermutlich weitere `DEBUG_*` | zeigt die erfasste Bodenkontur | [Test 16a] |

Bekannte Fehler (alle Forum, Auszug):
- `WATER_COMPONENT_WITH_BAKED_SIM` zeichnet bei einem Nutzer **nur Schaum**.
- Im **gepackten Build** zeichnet eine gebackene SWR nicht. Im Log steht dazu, das Normalen-Render-Target des Ozeans sei nicht
  initialisiert; der Auftrieb läuft trotzdem.
- In 5.6 stürzt der Editor beim Backen ab.
- In 5.7 schlägt das Backen fehl, sobald ein dritter River dazukommt.

**Empfehlung:**
- **Im Spiel:** `WATER_COMPONENT_WITH_BAKED_SIM` für alle Kacheln. Dazu gehören Water-Zone-LOD, unser Water-Body-Material, Auftrieb,
  Schwimm-Abfragen und Spieler-Interaktion.
- **Ersatz:** `BAKED_SIM`, falls der gepackte Build nicht zeichnet.
- **Beim Backen:** `LIVE_SIM`.
- Teil 2 prüft alle Zustände per Python-Liste und im gepackten Build (T2-1, T2-3).

### a4. „Live nahe, gebacken fern“

**Eingebaut ist keine Umschaltung je Entfernung.**
- `render_state` ist eine Eigenschaft je Akteur.
- Jede Eigenschaftsänderung startet die Simulation neu [Test 16a]. Eine Live-Simulation füllt die Becken erst über Sekunden bis
  Minuten.
- Was es gibt:
  - **Interaktion über das Shallow-Water-Subsystem** (Projekteinstellung „Shallow Water Simulation“; aktive Pawns und Impulse
    begrenzt; Kollisions-Kontexte für Akteure und Physik-Assets) [Doku, Datei 16]. Sie legt Wellen um die Spielfigur auf das
    gebackene Wasser, nur mit `WATER_COMPONENT_WITH_BAKED_SIM` [Leitfaden]. **Das ist das eingebaute „live nah“.**
  - **Fern:** Water-Zone-Netz-LOD und das Streaming der Kachel mit World Partition [Ableitung].

**Konzept, falls doch ein Live-Nahbereich gewünscht ist** (z. B. an Sehens-Orten mit beweglichen Objekten). Es lohnt nur, wenn T2-4
zeigt, dass `LIVE_SIM` **aus dem gebackenen Zustand** startet:
1. Ein eigenes Weltsubsystem (in unserem Plugin) hält je Kachel die Mitte der Bounding-Box und den Zustand.
2. Die nächste Kachel innerhalb **R_live = 40 m** (Hysterese: ab 50 m zurück) schaltet auf `LIVE_SIM`, alle anderen bleiben auf
   `WATER_COMPONENT_WITH_BAKED_SIM`. Höchstens **1–2 Kacheln** gleichzeitig live; bei 512² Zellen sind das ≈ 1,7–3,3 ms
   [Ableitung aus T1]. Das ist zu teuer für das Budget von 1,5 ms aus Datei 16, mit 256² (≈ 0,8 ms) eben tragbar.
3. Verlässt die Spielfigur die Kachel, wird zurückgeschaltet. Die Live-Änderung geht verloren; das gebackene Ergebnis zählt.
4. **Startet `LIVE_SIM` trocken**, entfällt das Konzept: Der Spieler würde das Becken leer sehen und volllaufen sehen.

**Simulation pausieren:** Im Spiel läuft mit `BAKED_SIM`/`WATER_COMPONENT_WITH_BAKED_SIM` voraussichtlich keine Niagara-Simulation
mehr. T2-3 prüft das mit ProfileGPU: Es darf kein `Grid2D_SW_River`-Dispatch mehr erscheinen. Für das Backen ist die eingebaute
CPU-Drossel da (Datei 16, Abschnitt 7).

## b) Material: Schaum, Weißwasser, klares Bergbachwasser

### b1. Absorption und Streuung: Konvention

- Die Simulation zeichnet mit `SW_Water_Material_River`, Eltern `SW_Water_Material` [Test 16a].
- Laut Test 16a hat es dieselbe Parameterfamilie wie unser `M_Eldarien_Wasser_Schaum8`. Dort stehen die Epic-Werte
  `Absorption` [10, 150, 350, 8], `Scattering` [1, 1, 1, 0,5], `Water Albedo` [0,85; 0,85; 0,85; 0,5] [Projekt].
- **Absorption = Absorptionslänge in cm.** Das Material rechnet 1/Wert und gibt das als SLW-Koeffizienten je cm weiter.
  - Das ist die Konvention von `wasserfarben.json`, in 13k (Abschnitt 5) erklärt und durch Ferats Test 8/40/160 belegt.
  - Epics SLW-Seite schreibt laut Auszug, dass die Absorptionswerte beim Standard-Wassermaterial „reversed“ sind [Doku, Auszug,
    Wortlaut nicht sicher].
- **SWR-Standard 20,8/25/24,7** heißt also: Rot nach 21 cm auf 1/e, Grün und Blau nach 25 cm. Schon 50 cm Wasser lassen vom Grund
  fast nichts durch, die Farbe kommt nur noch aus der Streuung (0,77/1,0/0,92). Ergebnis: **deckendes Hell-Türkis** wie rechts oben
  im Bild `t1_c2_netz_gegen_swr.jpg`.
- **Wichtig:** Die Längen sind cm, keine Koeffizienten je m. Die **Skalierung 0,01 gilt hier NICHT** (sie gilt nur für die
  Koeffizienten je m der Kaskadennetze). Umrechnung: Länge [cm] = 1 / (Koeffizient [je m] × 0,01).

**Kontrolle in Teil 2 (T2-9):**
1. Im Graph von `SW_Water_Material` dem Parameter `Absorption` bis zum SLW-Knoten folgen. Erwartet wird ein Kehrwert (1/x bzw.
   Divide).
2. Gegenprobe: Absorption 1 000/1 000/1 000 → Wasser fast glasklar. Wird es dunkler, ist es ein Koeffizient.
3. Messung wie in 15g: Gumpe 1,5 m tief, Rot auf ≈ 55 %.

### b2. Startwerte klarer Bergbach (`MI_EL_SWR_Fluss` und Water-Body-Material)

Ziel aus 15g/13k: Absorption 0,40/0,07/0,05 je m, Streuung 0,02/0,03/0,04 je m.

| Parameter | SWR-Standard | **Startwert** | Begründung |
|---|---|---|---|
| `Absorption` (R, G, B, A) | 20,8 / 25 / 24,7 / – | **250 / 1 430 / 2 000**, A unverändert | 1/(0,40·0,01) = 250 cm usw. Bei 1,5 m Tiefe bleiben Rot 55 %, Grün 90 %, Blau 93 %: klar, leicht türkis. |
| `Scattering` (Farbe, A) | 0,77 / 1,0 / 0,92, A 0,5 | **0,6 / 0,8 / 1,0**, A 0,5 | weg vom Grünstich, kein Blau-Überhang über den Rest |
| `Albedo` bzw. `Water Albedo` | 0,083 | **0,03** | weniger Körper im Volumen, Grund sichtbar. Bei zu milchigem Wasser halbieren. Wie Albedo und Scattering verrechnet werden, ist unbelegt [Ableitung] → T2-9. |
| `Water Roughness` | – | 0,02 | wie unser Master |
| `Refraction` | – | 1,15 nah / 1,02 fern | wie unser Master (`Refraction Far`) |

Streuung als Länge? Falls T2-9 zeigt, dass `Scattering` auch über 1/x läuft, gilt 5 000 / 3 333 / 2 500 cm (= 0,02/0,03/0,04 je m).

### b3. Schaum und Weißwasser

Die Namen stammen aus unserem Master (Epic-Familie) [Projekt]. Teil 2 bestätigt sie per Liste an `SW_Water_Material` (T2-1).

| Gruppe | Parameter | Wirkung [Ableitung aus Name und Wert] | **Startwert** |
|---|---|---|---|
| Schaum aus der Simulation | `Sim Foam Scale` (350), `SimFoam Contrast` (0), `Sim Foam Dpeth Min` (8, sic), `Sim Foam Velocity Mip` (128), `Sim Foam Normal` (1) | Menge und Kontrast des simulierten Schaums | `SimFoam Contrast` **0 → 2**: schwacher Schaum fällt weg, nur kräftiger an Stufen und Hindernissen bleibt. `Sim Foam Dpeth Min` lassen (sonst verschwindet Schaum an flachen Lippen). |
| Sichtbarkeit | `Foam Opacity` (1), `Foam Boost` (1), `Foam powr` (0,2), `FoamContrast` (1) | Deckkraft und Kurve | `Foam powr` **0,2 → 0,6**, `Foam Boost` **1 → 0,8**, `Foam Opacity` 0,9 |
| Farbe | `Foam Emissive` [0,287; 1,0; 0,188] (**grün**), `Foam Scattering` [1, 1, 1, 5] | Grünstich des Schaums im Test | `Foam Emissive` **→ 0 / 0 / 0** (Test: wird der Schaum grau, ist es eine Grundfarbe → dann 0,80 / 0,84 / 0,82 wie `ELD_Schaum_Farbe`). `Foam Scattering` 1/1/1 lassen. |
| Marmorierung | `Foam MacroScale` (1536), `Foam Texture Blend Min/Width` (0,4/0,4), `River Foam Scale` (512), `Fluidsim Flow Density` (0,25) | großflächige Schaumtextur über das ganze Wasser | `Foam Texture Blend Min` **0,4 → 0,6**: Textur erst bei mehr Schaum. Den Rest lassen. |
| Schaum an Hindernissen (Distanzfeld) | `Depth for DF Foam` (64), `Foam Distance` (256), `Wave Over Object Mask Distance` (256) | Saum um Felsen über Mesh-Distanzfelder | lassen; die Simulation liefert die Spur hinter dem Fels selbst (Bild `t1_fels_kollision.jpg`) |
| Rauheit | `Foam Roughness` (0,4) | | 0,4 |

**Niagara-Seite:**
- Wie viel Schaum entsteht (Schwelle aus Geschwindigkeit/Gefälle, Zerfall), steuern Benutzerparameter von `Grid2D_SW_River`.
- Ihre Namen kenne ich nicht, denn die Parameter-Referenz von Epic ist aus der Cloud nicht lesbar. Laut Forum gehören Schaum-Erzeugung
  und Schwelle sowohl zur Simulation als auch zum Material.
- T2-1 listet die Benutzerparameter auf. Ziel: Schaum ab ≈ 1,5 m/s Fließgeschwindigkeit bzw. an Stufen, Halbwertszeit 2–4 s
  (gibt 2–4 m lange Spuren wie unsere Schaumstraßen).

**Unser Master als Alternative [Ableitung]:**
- In `WATER_COMPONENT_WITH_BAKED_SIM` zeichnet das Material des **Water Body**.
- `M_Eldarien_Wasser_Schaum8` hat die nötigen Eingänge `BakedWaterSimTex(VT)`/`BakedWaterSimSize` und unsere `ELD_*`-Schaumregeln
  (`ELD_Fels_Schaum`, `ELD_Strom_Schwelle`, `ELD_Schaum_Schwelle` …).
- Dann wäre `MI_Eldarien_Wasser_Fluss` mit den Werten aus b2 das **Spielmaterial**. `MI_EL_SWR_Fluss` (Kind von
  `SW_Water_Material_River`) bliebe die Vorschau beim Backen und die Ersatzlösung `BAKED_SIM`.
- Prüfung: T2-9.

## c) Größe: Grenzen, Kacheln, Zellgröße

**Grenzen:**
- `resolution_max_axis` ist `int32`. Eine Obergrenze steht in keinem Auszug.
- Technische Decke ist die größte 2D-Textur bzw. Grid2D-Größe (16 384) [Ableitung].
- Die Zellgröße folgt aus längste Seite der River-Bounds / `resolution_max_axis`. T1 bestätigt das: 256 → 186 × 256 bei ≈ 0,16 m.
- Die **Fläche ist also nur durch die Zellzahl begrenzt.** Bei 0,25 m und 512 sind es 128 × 128 m.
- Kosten je Bild, hochgerechnet aus T1 (47 616 Zellen = 0,3–0,6 ms), linear [Ableitung]:

| Raster | Zellen | GPU je Bild (Editor) | Kachel bei 0,25 m |
|---|---|---|---|
| 256² | 65 536 | 0,4–0,8 ms | 64 m |
| 512² | 262 144 | 1,7–3,3 ms | 128 m |
| 1 024² | 1 048 576 | 7–13 ms | 256 m |

- **Zeitschritt:** Kleinere Zellen brauchen kleinere Zeitschritte (Stabilität), also mehr Schritte bis zum ruhigen Zustand. Die
  Backzeit wächst daher stärker als die Zellzahl [Ableitung]. T2-8 misst sie.

**Empfehlung: ein `AShallowWaterRiver` je Back-Kachel.**

| Variante | Akteure | Bewertung |
|---|---|---|
| je Fluss/Lauf | 177 | geht nicht: 35,4 km Lauf bzw. bis 1 km Bounding-Box bei 0,25 m sprengen jedes Raster |
| je Abschnitt | 1 120 | doppelt so viele Nähte und Bake-Läufe; 141 Becken < 4 m wären einzelne Mini-Simulationen; mehr Akteure |
| **je Back-Kachel** | **555** | eine Einheit für Fingerabdruck, Neu-Backen, Hindernis-Akteur und World-Partition-Zelle; Grenzen bevorzugt an Fällen (unter Vorhang und Aufprallschaum); ≤ 128 m passt zu 512 bei 0,25 m |

**Zellgröße:**
- **Bäche (Breite < 15 m): 0,25 m.** `resolution_max_axis` = ⌈L / 0,25⌉, aufgerundet auf ein Vielfaches von 32, höchstens 512
  (L = längste Seite der Kachel ohne Rand). Für C2 heißt das 75 × 121 m → 484 → **512**; 60 × 107 m → 428 → 448; 44 × 74 m → 296 → 320.
- **Flüsse ≥ 15 m und Kacheln > 128 m** (28 Kacheln, bis 246 m): **0,5 m**, höchstens 512. Die Strömungsformen sind dort größer;
  1 024² würde ≈ 10 ms je Kachel beim Backen kosten.
- **T1 hatte 0,16 m.** Teil 2 vergleicht 0,16 / 0,25 / 0,5 m an derselben Kachel. Wenn 0,25 m an Lippen sichtbar gröber ist, bekommt
  die Nahzone (Sehens-Orte) 0,2 m bei kleineren Kacheln.

**Verkettung (Quelle/Senke):**
- In 5.8 sind `source_river_water_bodies` und `sink_river_water_bodies` **Listen** [Test 16a]. Der Leitfaden zu 5.6 sagt: Ein River
  in der Quelle wird automatisch auch Senke [Leitfaden, ungeprüft].
- **Variante V1 (Standard):** Quelle = alle Abschnitte der Kachel in Fließreihenfolge, Senke = letzter Abschnitt (bzw. der See bei
  `abschnitt_unten = null`). So gehören die gebackenen Daten jedes Abschnitts genau einer SWR (`baked_shallow_water_sim` je Water Body).
- **Variante V2:** Quelle = erster Abschnitt, Senke = letzter, die Zwischenabschnitte nur über die Bounds. Wird gewählt, wenn V1
  zusätzliche Einläufe in der Mitte erzeugt (T2-7).
- **Nachbarkacheln:** Es gibt keine gemeinsame Quelle/Senke über Kachelgrenzen, sonst gehörte ein Water Body zwei Simulationen.
  - An Fällen (Kante unter Vorhang) ist das unkritisch.
  - An 353 offenen Grenzen in fließendem Wasser liegt die Naht an einer Abschnittsgrenze. Die Bodenerfassung reicht 8 m in die
    Nachbarkachel, also sieht die Simulation dort dasselbe Bett.
  - Teil 2 prüft die Naht (T2-7). Ist sie sichtbar, wird die Grenze in ein Becken gelegt (ruhiges Wasser) oder die Kachel bis zum
    nächsten Fall verlängert.

## d) ISM/Foliage als Hindernis

### d1. Wie die Bodenerfassung Geometrie sieht

- **Tiefen-Aufnahme:**
  - Das 5.8-Forum verfolgt einen Fehler bis in Niagaras **Scene-Depth-Abtastung**
    (`NiagaraDataInterfaceSceneCapture2DTemplate.ush`). Bodenhöhen „saturated at 65504“; danach wird `Grid2D_SW_River` neu gebaut.
  - Mit `use_capture` aus läuft die Simulation „als Rechteck, das die Landschaft ignoriert“.
  - Im 5.6-Forum gilt: `use_capture` aus → keine Objekte mit Bottom-Contour-Tag mehr.
  - Die Python-API 5.5 nennt `use_capture`, `bottom_contour_actors` und `bottom_contour_capture_offset` [Forum, Doku].
- **Auswahl der Objekte:**
  - Japanische Leitfäden: Unter „Collision → Bottom Contour Tags“ an der SWR und als Actor Tag am Hindernis denselben Namen eintragen,
    dann Reset. „Platzierte Objekte erkennt die Simulation nicht als Hindernis.“ [Leitfaden]
  - Ferats T1: Der Fels wird mit Tag + Liste erkannt, ohne nicht [Test 16a].
- **Datenschnittstelle:** Sie hat eine Liste `managed_show_only_actors` [Doku, Python 5.3]. Eine Scene Capture mit Show-Only-Liste
  zeichnet alle Grafik-Komponenten der gelisteten Akteure. Für Komponenten gibt es eine eigene Liste `ShowOnlyComponents` [Doku 4.26].
- **Daraus folgt [Ableitung]:**
  1. **Akteur-genau:** Alle Komponenten eines markierten Akteurs kommen in die Aufnahme, auch jede ISM/HISM-Komponente mit allen
     Instanzen.
  2. **Instanz-genau geht nicht:** Eine ISM-Komponente ist ein Grafikobjekt. Auch eine Komponentenliste könnte nur ganze
     Komponenten wählen [Doku 4.26; Forum: „show only one static mesh within the actor“ ohne Lösung].
  3. **Foliage:** Ein `InstancedFoliageActor` hält je World-Partition-Zelle alle Foliage-Typen. Ein Tag daran erfasst Gras, Farn und
     Felsen gemeinsam. **Nicht taggen.**
  4. **Filter je Komponente (falls nötig):** Die Grafik-Komponente hat „Hidden In Scene Capture“ (`hidden_in_scene_capture`, aus
     *allen* Scene Captures ausblenden) und „Visible In Scene Capture Only“ (`visible_in_scene_capture_only`, nur in Scene Captures
     sichtbar). Damit lässt sich in einem markierten Akteur eine Komponente ausschließen bzw. ein unsichtbarer Erfassungs-Stellvertreter
     bauen. Ob die SWR-Aufnahme diese Schalter beachtet, prüft T2-5.
  5. **Von oben:** Eine Tiefen-Aufnahme sieht nur die **Oberseite**. Was das Wasser überspannt (Stamm als Brücke, überhängender Fels,
     Äste), wird zur Wand bzw. zum Damm. Unterspülung gibt es nicht.
  6. **Landschaft:** Sie kommt über `bottom_contour_landscape_actors` dazu. Ob deren **Landschafts-Gras** (Grass-Type-HISM als
     Komponenten des Landschafts-Proxys) mit erfasst wird, ist offen. Im Bild `t1_fels_kollision.jpg` (Debug Boden) erscheinen grüne
     Pflanzenpunkte → T2-5.
  7. **World Partition:** Erfasst wird nur, was beim Reset/Bake **geladen** ist. Die Hindernis-Akteure der Kachel und ihrer Nachbarn
     müssen im Editor geladen sein.
- Am `AShallowWaterRiver` selbst gibt es keine Kollisionseinstellung für Laufzeit-Overlaps [Forum, Datei 16]. **Mit
  „Wasser-Kollision“ ist also nichts anderes als das Bottom-Contour-Tag bzw. die Liste gemeint.** Ein eigenes Kollisionsprofil ist
  nicht nötig. Die normale Kollision der Felsen für den Spieler bleibt, wie sie ist.

### d2. Lösung ohne Akteurflut: ein Hindernis-Akteur je Kachel

**`WH_<kachel_id>` („Wasserhindernisse“), genau einer je Back-Kachel:**
- Klasse: einfacher `Actor` mit `SceneComponent` als Wurzel.
- Je Netz eine Komponente: **ISM** bei Nanite-Netzen, **HISM** sonst (Nanite braucht die HISM-Baumstruktur nicht) [Ableitung].
  Kollision und Material wie in der Quelle.
- **Inhalt:** nur Objekte mit `wasser_kollision: true` aus `fluss_sim.json` (Fels, Holz, Grundriss ≥ 0,4 m, Höhe ≥ 0,2 m, im Wasser
  oder ≤ 1 m daneben), dazu lokal dieselbe Regel auf allen anderen Ebenen der Kachel (Bestand, Felsgruppen, Witcher).
  **Nie Pflanzen, kein Gras, keine Foliage-Akteure.**
- **Tags:** `SWR_Hindernis` (global, steht in `bottom_contour_tags` jeder SWR) und `SWR_K_<kachel_id>`.
- **Zusätzlich** steht der Akteur in `bottom_contour_actors` der eigenen SWR und der Nachbar-SWR, deren Bereich er schneidet. So sind
  beide Wege gesetzt wie in T1.
- **Instanzen werden verschoben, nicht kopiert (Variante A):** Das Bau-Werkzeug entfernt die Instanz aus ihrer Quell-Ebene
  (Instanz-Ebene des Planers) und setzt sie in `WH_…`. Es bleibt eine Wahrheit, nichts wird doppelt gezeichnet, und die Kollision ist
  dieselbe.
- **Variante B (Erfassungs-Stellvertreter), falls die Quell-Ebenen unangetastet bleiben müssen:** Die Instanzen bleiben in der
  Quelle. `WH_…` bekommt Kopien mit `visible_in_scene_capture_only = true` und ohne Kollision. Kosten: doppelte Transformationen
  (≈ 41 je Kachel), keine doppelte Darstellung. Voraussetzung: T2-5 zeigt, dass die Aufnahme den Schalter beachtet.
- **Gilt nur, falls die Erfassung je Komponente filtert:** Kommt in T2-5 heraus, dass die SWR doch einzelne Komponenten mit Tag sucht
  (Komponenten-Tags), dann bleiben die Steine in den Quell-Ebenen. Getaggt werden nur die Komponenten der Stein-Netze, nie die des
  Grases, und `WH_…` entfällt. Der Spezifikation unten schadet das nicht: Gruppierung und Felder bleiben, nur das Bau-Werkzeug setzt
  Tags statt umzuziehen.
- **Hand gesetzte Felsen:** einzelner `StaticMeshActor` mit Tag `SWR_Hindernis` (Werkzeug „Wasser-Kollision an Auswahl“).
  - Gelegentlich übernimmt das Werkzeug „In Hindernis-Akteur übernehmen“ sie in `WH_…`; danach gilt wieder 1 Akteur je Kachel.
  - Der Fingerabdruck erfasst beide Formen gleich (Objekte mit Tag, Instanzen aus `WH_…`).
- **Überspannende Objekte:** Ein Objekt, dessen Grundriss die Wasserfläche schneidet und dessen **Unterkante > Spiegel + 0,1 m** liegt
  (Stamm als Brücke, überhängender Fels), bekommt **keine** Wasser-Kollision. Grund: Die Aufnahme von oben macht daraus einen Damm.
  Die bisherige Regel „Unterkante ≤ Spiegel + 0,5 m“ wird für `lage = im_wasser` auf **+ 0,1 m** verschärft. Für `ufer` bleibt
  + 0,5 m (dort ist ohnehin kein Wasser).

**Passt zur Akteurgrenze:**
- Je Kachel kommen genau **2 Akteure** dazu (`SWR_…`, `WH_…`), dazu ≈ 2 `WaterBodyRiver` (1 120 / 555).
- Ganz Eldarien hat damit 555 + 555 + 1 120 = **2 230 Wasser-Akteure statt 22 825 Hindernis-Akteuren**.
- Die Grenze aus 13k (≤ 50 Akteure eines Gefälle-Laufs je Kachel bzw. je 200 m Lauflänge) zählt SWR und WH als eigene Wasser-Akteure.
  Der Prüfer weist sie getrennt aus (siehe Spezifikation).

## Spezifikation der Export-Änderung (`fluss_sim_v2`, nur Beschreibung)

Umsetzung in einem späteren Schritt. Diese Antwort ändert keinen Code unter `skripte/`.

### S1. Gruppierung `wasser_kollision` → Hindernis-Akteur je Kachel

- **Je Eintrag in `wasser_kollision` neue Felder:**
  - `kachel` (ID der Kachel, die den `abschnitt` des Objekts enthält)
  - `hindernis_akteur` (`WH_<kachel>`)
  - `komponente` (Index), `instanz` (Index in der Komponente)
  - `umzug` (`"verschieben"` | `"stellvertreter"`, Standard `verschieben`)
- **Neue Regel:** `lage = im_wasser` und Unterkante > Spiegel + 0,1 m → `wasser_kollision: false`, `grund: "ueberspannt"`, nicht in
  `WH_…`. Neues Regelfeld in `fluss_sim_regeln.json`: `kollision.ueberspannt_unterkante_max_m = 0.1`.
- **Je `sim_bereiche[]` neuer Block:**

```json
"hindernis_akteur": {
  "id": "WH_F_ERLENBACH_1V_C2_K00", "klasse": "Actor", "label": "WH_F_ERLENBACH_1V_C2_K00",
  "tags": ["SWR_Hindernis", "SWR_K_F_ERLENBACH_1V_C2_K00"],
  "ursprung_cm": [-173674.7, -235620.5, 0.0],
  "komponenten": [
    {"netz": "/Game/Megascans/3D_Assets/NordicBoulder/SM_NordicBoulder_01", "klasse": "HISM", "nanite": false,
     "kollision": "wie_quelle", "instanzen": [
       {"ref": {"quelle": "gefaelle/F_ERLENBACH_1V_C2/instanzen/C2/plan.json", "datei": "SM_NordicBoulder_01_kol", "index": 3},
        "pos_cm": [-172818.7, -238622.3, 9795.7], "quat_xyzw": [-0.239743, -0.187143, 0.128668, 0.943899],
        "skala": [0.3468, 0.3468, 0.3468], "lage": "im_wasser"}, ...]}, ...],
  "n_instanzen": 336, "n_komponenten": 14,
  "akteure_mit_tag": [{"ref": {"quelle": "...", "liste": "akteure", "index": 7}}],
  "umzug": "verschieben"
}
```

- Zahlen im Beispiel sind teils beispielhaft (`n_komponenten`, Akteur-Index); Lage und Bereich stammen aus K00.
- `ursprung_cm`: Mitte von `bereich_cm` in xy, z = 0. Die Instanz-Lagen bleiben Weltkoordinaten; das Werkzeug rechnet sie relativ.
- `klasse`: ISM, wenn das Netz Nanite hat (lokal aus dem Asset; in der Cloud `"nanite": null` = vom Werkzeug bestimmen).
- `akteure_mit_tag`: Objekte, die schon in der Quelle Akteure sind (`liste: "akteure"`). Sie bleiben Akteure und bekommen nur das Tag.
- **Neu im Prüfer:**
  - **FEHLER:** jedes `wasser_kollision: true` in genau einem `WH_…`; Instanzzahl = Liste; kein Pflanzennetz; je Kachel höchstens ein
    `WH_…`; kein `ueberspannt`-Objekt in `WH_…`.
  - **HINWEIS:** Anzahl Wasser-Akteure je Kachel.
- **Fingerabdruck:** Formel unverändert. Neu ist nur, dass `ueberspannt`-Objekte aus dem Objektteil fallen; das ändert die
  betroffenen Kacheln einmalig. Editorseitig: alle Instanzen aller Komponenten von Akteuren mit Tag `SWR_Hindernis` plus einzelne
  Akteure mit Tag.

### S2. Ein SWR je Kachel

```json
"swr": {
  "id": "SWR_F_ERLENBACH_1V_C2_K00", "klasse": "ShallowWaterRiver",
  "zelle_m": 0.25, "resolution_max_axis": 512, "raster_erwartet": [512, 318],
  "source_river_water_bodies": ["F_ERLENBACH_1V_C2_A00", "...", "F_ERLENBACH_1V_C2_A07"],
  "sink_river_water_bodies": ["F_ERLENBACH_1V_C2_A07"],
  "quelle_variante": "V1",
  "bottom_contour_tags": ["SWR_Hindernis"],
  "bottom_contour_actors": ["WH_F_ERLENBACH_1V_C2_K00", "WH_F_ERLENBACH_1V_C2_K01"],
  "bottom_contour_landscape_actors": "lokal",
  "use_capture": true, "match_spline": true,
  "render_state": {"backen": "LIVE_SIM", "spiel": "WATER_COMPONENT_WITH_BAKED_SIM", "ersatz": "BAKED_SIM"}
}
```

- **`zelle_m`:** 0,25 bei größter Wasserbreite der Kachel < 15 m, sonst 0,5. `resolution_max_axis` = min(512, ⌈L/zelle/32⌉ × 32),
  L = längste Seite von `groesse_m`. Neue Regelfelder: `swr.zelle_bach_m`, `swr.zelle_fluss_m`, `swr.breite_fluss_ab_m`,
  `swr.resolution_max`, `swr.resolution_schritt`.
- **`sink_river_water_bodies`:** letzter Abschnitt. Mündet die Kachel in einen See (`abschnitt_unten = null` am letzten Fall), kommt
  zusätzlich die See-ID aus der Quelle (`see_id`) dazu, wenn bekannt.
- **`bottom_contour_actors`:** eigenes `WH_…` plus jedes Nachbar-`WH_…`, dessen Instanz-Bounds `bereich_cm` dieser Kachel schneiden.
- **Prüfer FEHLER:** `resolution_max_axis` ≤ 512; Zelle an Bächen ≤ 0,25 m; jeder Abschnitt in genau einer `source`-Liste (V1).

### S3. Verkettung

- **Je Kachel neu:**
  - `vorgaenger` und `nachfolger`: Listen von Kachel-IDs. An Mündungen sind es mehrere Vorgänger.
  - `naht_oben` und `naht_unten`: `fall` | `offen` | `see` | `laufrand`, entspricht den bisherigen `grenze_*`.
- Für eine offene Grenze kommt dazu `naht_abschnitte`: die beiden Abschnitte, die sich den Endpunkt teilen. Damit prüft das Werkzeug
  nach dem Backen die Höhendifferenz an der Naht (Ziel ≤ 2 cm, T2-7).
- **Reihenfolge beim Backen** = topologische Reihenfolge von oben nach unten. Unabhängige Kacheln (verschiedene Läufe) dürfen
  gleichzeitig laufen.

### S4. `render_state` je Entfernung

```json
"darstellung": [
  {"bis_m": "ladebereich", "render_state": "WATER_COMPONENT_WITH_BAKED_SIM", "interaktion": "subsystem"},
  {"ab_m": "ladebereich", "art": "fern", "quelle": "offen (Rueckfrage 1)"}
],
"live_nah": {"aktiv": false, "radius_m": 40, "hysterese_m": 10, "max_kacheln": 1,
             "bedingung": "nur wenn T2-4 zeigt: LIVE_SIM startet aus dem gebackenen Zustand"}
```

- **Im Ladebereich der World Partition:** gebacken mit Interaktion.
- **Außerhalb:** Die Kachel ist entladen. Wasser-Komponenten gehen nicht in HLOD ein (HLOD-Seite 5.0–5.4, siehe
  `hlod-fernansicht-world-partition.md`). Die ferne Darstellung ist deshalb eine eigene Entscheidung (Rückfrage 1).
- `live_nah` steht nur als Platzhalter im Format und ist bis zu einer Entscheidung aus.

## Testplan Teil 2 (lokale Instanz)

Ort: C2 Version 3, Kachel `K00` (75 × 121 m, 336 Kollisionsobjekte) und ihr Nachbar `K01`. Bilder bitte unter `bilder/swr/`.

| Nr. | Test | Vorgehen | Ergebnis zurück |
|---|---|---|---|
| T2-1 | **Listen** | Python: `dir(unreal.ShallowWaterRenderState)`, `[p for p in dir(swr_comp) if not p.startswith('_')]`; Material: `unreal.MaterialEditingLibrary.get_scalar_parameter_names(m)` und `get_vector_parameter_names`, `get_texture_parameter_names` für `SW_Water_Material` und `SW_Water_Material_River`; Niagara: Benutzerparameter von `Grid2D_SW_River` (Panel „User Parameters“, Bildschirmfoto) | Textdateien, neben die Bilder |
| T2-2 | **Bake-Inhalt** | Nach Bake: für jede `baked_*`-Textur Name, Größe, Pixelformat, Kompression, Virtual Texture ja/nein, Mips, `get_outer().get_path_name()`, Resource Size (Size Map); `water_body_comp.get_editor_property('baked_shallow_water_sim')`; im Material des Water Body (MID) Wert von `BakedWaterSimTex`/`…VT`/`BakedWaterSimSize`; Größe der Akteur-Datei in `__ExternalActors__` vor/nach dem Speichern | Tabelle; ersetzt die Schätzung a2 |
| T2-3 | **`render_state`** | Jeden Zustand aus T2-1 einmal: Bild + ProfileGPU (Summe `Grid2D_SW_River`; in BAKED/WCBS soll sie 0 sein); dann **gepackter Development-Build** mit WCBS und BAKED_SIM | zeichnet ja/nein, ms, Log-Warnungen |
| T2-4 | **Umschalten** | gebacken, dann zur Laufzeit (PIE, Blueprint/Python) auf `LIVE_SIM`: Startet die Simulation aus dem gebackenen Zustand oder trocken? Zeit bis zum ruhigen Zustand | entscheidet über `live_nah` |
| T2-5 | **Erfassungsmatrix** | Mit `DEBUG_RENDER_BOTTOM_CONTOUR`, je Zeile Reset: (a) nur Tag, (b) nur `bottom_contour_actors`, (c) beides; Objekte: StaticMeshActor, Actor mit 1 ISM (3 Felsen), Actor mit HISM, Nanite-Fels, Foliage-Akteur (Fels-Typ + Gras-Typ), Landschafts-Gras am Ufer; dazu: Gras-Komponente im getaggten Akteur mit `hidden_in_scene_capture = True`; Stellvertreter mit `visible_in_scene_capture_only = True`; **Stamm quer über dem Wasser, Unterkante 0,3 m über dem Spiegel** (Damm?); Komponenten-Tag statt Akteur-Tag | Matrix erkannt ja/nein + Debug-Bilder |
| T2-6 | **Hindernis-Akteur K00** | `WH_…K00` aus den 336 Objekten von K00 bauen (Variante A), Originale entfernen; Reset, laufen lassen, Bake; Vergleich mit 3 einzeln getaggten Akteuren derselben Stelle | Bild Debug-Boden + Wasser, Unterschiede |
| T2-7 | **Naht und Quelle/Senke** | K00 und K01 je eine SWR; V1 (alle Abschnitte als Quelle) gegen V2 (nur erster); an der Grenze Wasserhöhe beider Seiten (Line Trace bzw. Abfrage) | Höhendifferenz cm, Bild der Naht |
| T2-8 | **Auflösung** | K00 mit 256 / 512 (≈ 0,24 m) / 768 (≈ 0,16 m): Raster, ms je Bild, Zeit bis ruhig (Wasser erreicht die Senke, Pegel ändert sich < 1 cm in 10 s), Backzeit, Texturgröße | Tabelle; bestätigt 0,25 m |
| T2-9 | **Material** | Graph von `SW_Water_Material`: Weg von `Absorption`, `Scattering`, `Albedo` zum SLW-Knoten (Bild); Gegenprobe Absorption 1 000; `MI_EL_SWR_Fluss` mit b2/b3; Gumpe 1,5 m: Rot ≈ 55 %; in WCBS dasselbe mit `MI_Eldarien_Wasser_Fluss` (unser Master am Water Body) | Bilder vorher/nachher, Kurvenbild |
| T2-10 | **Höhe** | Eine SWR an der höchstgelegenen Bachkachel bzw. testweise Landschaft + River bei z ≈ 700 m und 1 500 m (> 655,04 m): Erfasst die Simulation den Boden? | ja/nein (Forum 5.8: Abschneiden bei 65 504) |
| T2-11 | **World Partition** | Level mit K00 + K01 speichern, Editor neu, nur K01 laden: Bleibt das Gebackene? PIE mit Streaming: lädt und entlädt das Gebackene mit der Zelle? | ja/nein |
| T2-12 | **Viele SWR** | 10 SWR in einem Level nacheinander backen (Forum 5.7: Bake bricht ab dem dritten River ab); gleichzeitig 4 live laufen lassen (Stapelbacken) | ja/nein, Backzeit je Kachel |

## Quellen

Alle aus der Cloud nicht direkt lesbar (Proxy 403); Inhalte aus Suchmaschinen-Auszügen.

Epic-Doku und API:
- [Python 5.5: unreal.ShallowWaterRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent?application_version=5.5) – `render_state` (`ShallowWaterRenderState`), `baked_sim`, `baked_water_surface_rt`, `baked_water_surface_texture`, `resolution_max_axis`, `use_capture`, `bottom_contour_actors`, `bottom_contour_capture_offset`
- [Python 5.5: unreal.ShallowWaterRiver](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiver?application_version=5.5)
- [Python 5.7: unreal.WaterBodyCustomComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyCustomComponent?application_version=5.7), [WaterBodyRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyRiverComponent), [WaterBodyLakeComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyLakeComponent) – `baked_shallow_water_sim`
- [API: Water-Plugin (UBakedShallowWaterSimulationComponent)](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water?lang=en-US)
- [API: UShallowWaterSubsystem](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterSubsystem)
- [Python 5.3: unreal.NiagaraDataInterfaceSceneCapture2D](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/NiagaraDataInterfaceSceneCapture2D?application_version=5.3) – `managed_show_only_actors`
- [API 4.26: USceneCaptureComponent::ShowOnlyComponents](https://docs.unrealengine.com/4.26/en-US/API/Runtime/Engine/Components/USceneCaptureComponent/ShowOnlyComponents/index.html)
- [Single Layer Water Shading Model](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine)
- [Water Meshing System and Surface Rendering](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-meshing-system-and-surface-rendering-in-unreal-engine)
- [Unreal Engine 5.8 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US) – im Auszug nichts zu Shallow Water River, nur Water-Brush-/SLW-Änderungen
- [Tutorial: Baked River Simulations – Parameter Reference](https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference), [Forum-Thread](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112) – Inhalt nicht erreichbar
- [Tutorial: Baked River Simulations – Overview and Quick Start (Forum)](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-overview-and-quick-start/2512102)
- [Community-Tutorial 5.6: Water Body River als Niagara-2D-Simulation](https://dev.epicgames.com/community/learning/tutorials/OZMa/new-in-unreal-engine-5-6-turn-your-water-body-river-into-a-game-ready-niagara-2d-fluid-simulation)

Epic-Forum:
- [Shallow water plugin not working in 5.8](https://forums.unrealengine.com/t/shallow-water-plugin-not-working-in-5-8/2763339) – `use_capture`, Scene-Depth-Abtastung, 65 504
- [Unreal 5.6 ShallowWaterRiver simulation nowhere near the WaterBodyRiver spline](https://forums.unrealengine.com/t/unreal-5-6-shallowwaterriver-simulation-nowhere-near-the-waterbodyriver-spline/2637929) – `use_capture` aus → keine Bottom-Contour-Objekte; Landschafts-Bounds unter WP
- [Shallow body river – Water Component with Baked Sim not rendering](https://forums.unrealengine.com/t/shallow-body-river-water-component-with-baked-sim-not-rendering/2688228)
- [Shallow Water Body (Advanced Water Plugin) Fails To Render](https://forums.unrealengine.com/t/shallow-water-body-advanced-water-plugin-fails-to-render/2634176) – gepackter Build
- [UE 5.7 Water Plugin – Baking fails after adding an additional WaterRiver](https://forums.unrealengine.com/t/ue-5-7-water-plugin-baking-fails-after-adding-an-additional-waterriver/2732713)
- [5.6 are shallow water river destructive?](https://forums.unrealengine.com/t/5-6-are-shallow-water-river-destructive/2659509) – Reset/Bake
- [Unreal 5.6 water simulation](https://forums.unrealengine.com/t/unreal-5-6-water-simulation/2626503) – Projekteinstellung, Kollisionsprofil
- [Too much foam on water](https://forums.unrealengine.com/t/too-much-foam-on-water/2404908), [Unreal Engine 5.6 shallow water river (Schaum und Tiefe)](https://forums.unrealengine.com/t/unreal-engine-5-6-shallow-water-river/2657057)
- [Show Specific Actors In Scene Capture Component 2d](https://forums.unrealengine.com/t/show-specific-actors-in-scene-capture-component-2d/622274), [Help with Scene Capture Component 2d](https://forums.unrealengine.com/t/help-with-scene-capture-component-2d/404748)
- [ShallowWaterRiver simulation does not initialize in 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772)

Leitfäden (japanisch, nur Auszug):
- [Historia: ShallowWaterRiverを使って流れる川を作ってみよう](https://historia.co.jp/archives/53937/) – Tags an Hindernissen, Collisions → Bottom Contour Tags
- [ue5exp0: UE5.6で高品質の川が簡単に作れます](https://ue5exp0.com/water5-6/) – Tag „Rock“, Backen gegen Laufzeitkosten
- [yossi40-100: UE5.6 Shallow Water River解説](https://yossi40-100.com/ue56shallow_water_river/) – Render State nach dem Backen (Baked Sim bzw. Water Component with Baked Sim, nur Letzteres mit Interaktion)

Projekt:
- `vorlagen/daten/material_parameter.json` (`M_Eldarien_Wasser_Schaum8`: Schaum-, Fluidsim- und `BakedWaterSim*`-Parameter)
- `antworten/13k-pilot2-bildbefund-15g-nachtrag.md` (Abschnitte 5 und 8: Längen in cm, Skalierung 0,01)
- `antworten/15g-c2-v2-bildbefund.md` (2.2: Klarwasser-Werte)
- `antworten/16-shallow-water-alle-gewaesser.md`, `skripte/fluss_sim/README.md`

## Rückfragen

1. **Ferne Darstellung:** Hinter dem Ladebereich sind Kachel und Water Body entladen, und Wasser geht nicht in HLOD. Was soll man dort
   sehen?
   - (a) eigenes Runtime-Grid „Wasser“ mit großem Ladebereich (gebacken ist billig),
   - (b) die bisherigen Kaskadennetz-Flächen als Fern-Netz im HLOD,
   - (c) beides.
2. **Umzug der Instanzen:** Darf das Bau-Werkzeug die Hindernis-Instanzen aus den Planer-Ebenen **verschieben** (Variante A)? Oder
   müssen die Ebenen unverändert bleiben (Variante B, Stellvertreter nur für die Aufnahme)?
3. **Breite Flüsse mit 0,5-m-Zellen** (Breite ≥ 15 m und Kacheln > 128 m): einverstanden?
4. **Live-Nahbereich:** Reicht die eingebaute Interaktion auf gebackenem Wasser? Oder soll `live_nah` nach T2-4 eingeschaltet werden
   (nur, wenn `LIVE_SIM` aus dem gebackenen Zustand startet)?
5. **Überspannende Stämme** ohne Wasser-Kollision (Unterkante > Spiegel + 0,1 m): einverstanden? Betrifft auch überhängende Felsnasen.
6. **Spielmaterial:** unser Master am Water Body (`MI_Eldarien_Wasser_Fluss` mit `BakedWaterSimTex`) oder Epics `SW_Water_Material`?
   Ich empfehle unseren Master, wenn T2-9 zeigt, dass er die gebackenen Daten liest.

## Nachtrag Koordinator: Rückfragen 1–6 entschieden

Ferat hat Designfragen an die Cloud übergeben („du entscheidest“). Gilt, bis Ferat es anders sagt:

1. **Hinter dem Ladebereich:** `WaterBodyRiver` ohne Simulation (Flowmap aus der Spline, unser Material). Das Gebackene braucht man nur im Ladebereich.
2. **Instanzen verschieben:** ja. Das Bau-Werkzeug verschiebt die Wasser-Kollisionsobjekte aus den Planer-Ebenen in den `WH_<kachel>`-Akteur
   (Variante A). Damit gibt es keine Doppelten. Rückbau über die Liste `umzug`.
3. **Breite Flüsse mit 0,5-m-Zellen:** ja. Bäche bekommen 0,25 m.
4. **Eigener Live-Nahbereich:** nein. Wir nutzen die eingebaute Interaktion um die Spielfigur plus das Gebackene. Erst wenn Teil 2 zeigt, dass `LIVE_SIM`
   aus dem gebackenen Zustand startet und das sichtbar besser ist, kommt die Frage wieder auf.
5. **Überspannende Objekte (Brückenstamm, überhängender Fels) ohne Wasser-Kollision:** ja. Von oben gesehen wären sie sonst ein Damm.
6. **Spielmaterial:** unser Master `M_Eldarien_Wasser_Schaum8` bzw. `M_EL_Kaskade_SLW2` am Water Body. Damit sind die Einheit und die Klar-Werte aus 13k/15g
   durchgehend gleich. `MI_EL_SWR_Fluss` dient nur als Vorschau beim Backen und als Ersatz.

Umsetzung im Export (`fluss_sim_v2`) folgt nach Teil 2, sobald die Erfassung von ISM/HISM im `WH`-Akteur bestätigt ist.

## Nachtrag 2: Woher das Marmormuster kommt (Antwort auf Nachtrag 15:05)

Stand 12.10.2026. Grundlage sind Nachtrag 15:05, die Bilder `bilder/swr/t1_material_epic_gegen_eigen.jpg`,
`t1_material_varianten.jpg` und `t1_c2_netz_gegen_swr.jpg` sowie `vorlagen/daten/material_parameter.json` und
`vorlagen/daten/inventar_extra.json`. Quellenlage wie oben: `dev.epicgames.com` und das Forum antworten aus der Cloud mit Proxy 403,
`web.archive.org` und GitHub ebenfalls. Alle Web-Belege stammen aus **Suchmaschinen-Auszügen** und sind so gekennzeichnet wie
oben ([Doku], [Forum], [Leitfaden], [Projekt], [Test 16a], [Ableitung], [ungeprüft]). Ferats Video kenne ich noch nicht (Rückfrage 1).

### Kurzfazit

- **Die beiden Material-Tests haben das Material, das in LIVE_SIM zeichnet, sehr wahrscheinlich gar nicht erreicht.**
  - In LIVE_SIM zeichnet das **Niagara-System** der SWR die Wasseroberfläche (über `river_sim_system`, eine `NiagaraComponent`) mit
    dem Material seines eigenen Renderers. Nach Test 16a ist das `SW_Water_Material_River`.
  - Der Water Body ist in LIVE_SIM ausgeblendet. Ein Forenbericht zu 5.6.1 sagt: Nach „Reset“ an der SWR verschwindet der Water Body
    vollständig [Forum]. In Ferats Bild rechts ist auch keine zweite Wasserfläche zu sehen [Test 16a].
  - Damit wirkt **`MI_Eldarien_Wasser_Fluss` am Water Body in LIVE_SIM nicht**. Das erklärt, warum die Varianten V2–V4 identisch
    aussehen: `Sim Velocity Normal Strength` 40 → 3 hätte sonst deutlich sichtbar sein müssen [Ableitung].
  - `baked_sim_material` und `spline_river_material` sind nach ihren Namen die Materialien für die **gebackene** bzw. die
    **Spline**-Darstellung, nicht für LIVE_SIM [Ableitung]. Daher „kaum Unterschied“ bei `MI_EL_SWR_Fluss`.
  - **Unsere Klar-Werte auf `SW_Water_Material_River` in LIVE_SIM sind also noch gar nicht getestet.**
- **Das Muster selbst hat zwei Teile** [Ableitung aus den Bildern]:
  1. **Grundfarbe deckend oliv-türkis:** Sie kommt aus Absorption 20,8/25/24,7 cm und Streuung 0,77/1,0/0,92 im Niagara-Material.
     Man sieht das im unteren Becken, wo das Wasser ruhig ist: einheitlich oliv, kein Grund sichtbar.
  2. **Weiß-cremige Marmorflecken und türkise Schlieren nur im schnellen Teil:** simulierter Schaum, mit der Strömung verzogen, dazu
     Spiegelungen an steilen Simulations-Normalen. Im Becken fehlen sie. Das Muster folgt also der **Geschwindigkeit**.
- **Der Sekundär-Emitter ist wahrscheinlich nicht die Ursache des Marmors.** Seine Teilchen sieht man als Gischtwolke am Fels und als
  körnige beige Flecken (Bild Varianten, untere Reihe). Der Marmor ist dagegen eine geschlossene Fläche auf der Oberfläche
  [Ableitung]. D3 im Plan prüft das in einer Minute.
- **Die Strecke ist für eine Flachwasser-Simulation sehr steil:** 70,1 → 55,6 m auf 40 m sind **36 % mittleres Gefälle**. Zwischen den
  Becken ist das Wasser überall schnell. Schaum und unruhige Normalen sind dort physikalisch „richtig“ [Ableitung]. Klares Wasser
  bekommt man in den **Becken**; in den Rinnen kann man den Schaum nur weißer, dünner und kürzer machen.
- **Für das Spiel ist LIVE_SIM nur die Vorschau beim Backen.** Nach Entscheidung 6 zeichnet im Spiel `WATER_COMPONENT_WITH_BAKED_SIM`
  mit **unserem** Master. Ein Forenauszug zu 5.6 sagt dasselbe von der anderen Seite: Die Einstellungen im überschriebenen Material
  greifen nur, wenn die SWR auf „Water Component with Baked Sim“ steht [Forum]. **Der wichtigste Test ist deshalb D6:** einmal
  backen und T1 in WCBS mit `MI_Eldarien_Wasser_Fluss` ansehen.

### Befunde

**B1. Eigenschaften der SWR (belegt) [Doku Python 5.5, Test 16a]**

| Eigenschaft | Typ | Bedeutung für das Aussehen |
|---|---|---|
| `render_state` | `ShallowWaterRenderState`, lesen/schreiben | wählt den Darstellungsweg (LIVE_SIM, BAKED_SIM, WATER_COMPONENT_WITH_BAKED_SIM, DEBUG_RENDER_BOTTOM_CONTOUR …) |
| `river_sim_system` | `NiagaraComponent`, nur lesen | die laufende Simulation; ihr Asset kommt laut Doku aus den Projekteinstellungen („Plugins – Water ShallowWaterSimulation“) |
| `water_info_texture` | `TextureRenderTarget2DArray`, nur lesen | Water-Info-Aufnahme der SWR (Eingang der Simulation, siehe B4) |
| `baked_sim`, `baked_water_surface_rt`, `baked_water_surface_texture` | nur lesen | gebackene Daten |
| `baked_sim_material`, `spline_river_material` | Material | in 5.8.3 vorhanden [Test 16a]; in keinem Auszug beschrieben |
| `resolution_max_axis`, `sim_speed`, `num_steps`, `match_spline`, `use_capture`, `bottom_contour_*`, `source/sink_river_water_bodies` | | Simulation, nicht Optik |

- Weitere Material-Felder (z. B. Übergänge zu See und Meer) gibt es vielleicht, belegt ist nichts davon. D1 listet alle Felder.
- **Am Water Body** (5.7): `baked_shallow_water_sim` (nur lesen) und ein Schalter `use_baked_sim_for_queries_and_physics` [Doku].

**B2. Was in LIVE_SIM zeichnet [Doku, Forum, Projekt, Ableitung]**

- Das Niagara-System zeichnet die Wasserfläche über seine Renderer. Welche Materialien die Renderer nutzen, lässt sich per Python
  auslesen: `unreal.NiagaraFunctionLibrary.get_all_emitters(system)` liefert je Emitter eine `NiagaraMinimalEmitterInfo` mit
  `emitter_name`, `is_enabled`, `is_lightweight`, `used_renderer_materials`, `used_renderer_meshes` [Doku, Auszug; Versionsangabe
  fehlt im Auszug, deshalb im Skript mit `hasattr` abgesichert].
- Im Projekt gibt es schon **`MI_Eldarien_Wasser_FlussSim`, Eltern `/WaterAdvanced/Niagara/Materials/SW_Water_Material_River_Niagara_Cached`**
  [Projekt, `inventar_extra.json`]. Es gibt also mindestens vier SW-Materialien: `SW_Water_Material`, `…_River`, `…_River_Spline`,
  `…_River_Niagara_Cached`. Welches davon in welchem Zustand zeichnet, zeigt D1. Wofür `…_Niagara_Cached` gedacht ist, ist
  unbelegt; der Name deutet auf eine Fassung für zwischengespeicherte Simulationsdaten [Ableitung].
- Material in den Niagara-Renderer bringen, ohne Engine-Inhalt zu speichern:
  - **Weg A:** Hat `Grid2D_SW_River` einen Benutzerparameter vom Typ Material, setzt man ihn mit
    `NiagaraComponent.set_variable_material(name, material)` [Doku Python 5.0–5.6].
  - **Weg B:** Kopie des Systems nach `/Game/…`, dort Renderer-Material oder Emitter ändern, Kopie in den Projekteinstellungen
    eintragen (Feldname dort unbelegt) oder mit `NiagaraComponent.set_asset(kopie)` setzen. Ob die SWR beim nächsten Reset wieder
    das Projekt-Asset setzt, ist offen [ungeprüft].
  - **Weg C (Schnelltest):** Werte in `SW_Water_Material_River` nur im Speicher ändern und wieder zurücksetzen (Skript D4). Nicht
    speichern, denn das ist Engine-Inhalt.

**B3. Sekundär-Emitter [Test 16a, Doku, ungeprüft]**

- `SW_River_Secondary_Emitter` (50 000 Teilchen) mit `M_SW_Foam` zeichnet nach Name und Bild **Gischt- und Schaumteilchen** über der
  Fläche. Seine Parameter (Spawn-Schwelle, Lebensdauer, Größe) kenne ich nicht; die Parameter-Referenz von Epic ist nicht lesbar.
- **Abschalten:**
  - `NiagaraComponent.set_emitter_enable(emitter_name, bool)`: Die C++-Funktion `SetEmitterEnable` gibt es [Doku 4.26]. Ein
    Fehler, durch den sie wirkungslos blieb, ist seit 5.4 behoben [Doku, Jira UE-89870]. Der Python-Name ist vermutlich
    `set_emitter_enable`; das Skript prüft es mit `hasattr`. **Ob sie bei GPU-Emittern wirkt, ist unbelegt.**
  - Sicher geht es nur in einer **Kopie des Systems** (Weg B): Emitter-Haken aus oder Renderer-Haken aus.
- Ob es Benutzerparameter für Teilchenzahl oder Schwelle gibt, zeigt die Liste aus D1.

**B4. Water-Info-Pfad [Doku, Forum, Projekt, Ableitung]**

- Die Water Zone zeichnet eine Water-Info-Textur (`Texture2DArray`). Laut Forum 5.6 steht im Blau-Kanal die Wasserhöhe und im
  Alpha-Kanal die Bodenhöhe [Forum]. Die Strömung steht sehr wahrscheinlich in Rot/Grün [Ableitung].
- Das Water-Body-Material liest sie über `WaterVelocityAndHeight` (in unserem Master Standard `/Water/Textures/BlackTexture2DArray`,
  zur Laufzeit von der Water Zone gesetzt) [Projekt]. Daraus kommen Flowmap, Wellenmaske und Strömungsschaum am normalen Water Body.
- Die SWR hat eine **eigene** `water_info_texture` [Doku]. Sie dient vermutlich als Eingang der Simulation (Wasserflächen der Quell-
  und Senken-Bodies, Höhen) [Ableitung].
- In **LIVE_SIM** ist der Water Body ausgeblendet. Der Water-Info-Pfad hat dort **keinen Einfluss auf das Aussehen** [Ableitung].
- In **WCBS** zeichnet der Water Body wieder. Die gebackene Simulation kommt dann über `BakedWaterSimTex`/`…VT`/`BakedWaterSimSize`
  und vermutlich auch über die Water-Info-Textur ins Material [Projekt, Ableitung].
- Daneben gibt es die **Interaktions-Simulation** um die Spielfigur: `BasicShallowWaterSubsystem` hat `normal_rt`, `velocity_rt`,
  `water_info_texture` und eine `mpc` (Material Parameter Collection) [Doku]. Sie speist sehr wahrscheinlich die Material-Eingänge
  `NormalAndHeight` und `Velocity` und die `Fluidsim *`-Werte [Ableitung].

**B5. Welche Parameter aus `M_Eldarien_Wasser_Schaum8` wo wirken können [Projekt, Ableitung]**

| Gruppe (Werte aus `material_parameter.json`) | Liest | LIVE_SIM (am Water Body) | WCBS | Interaktion (PIE) |
|---|---|---|---|---|
| `BakedWaterSimTex`, `BakedWaterSimTexVT`, `BakedWaterSimSize` | gebackene Simulation | nein | **ja** | – |
| `Sim Foam Scale` 350, `SimFoam Contrast` 0, `Sim Foam Dpeth Min` 8, `Sim Foam Velocity Mip` 128, `Sim Foam Normal` 1, `Sim Velocity Normal Strength` 40, `SIm Flowmap Speed` 1,5, `Sim Flowmap Detection` 1,5, `Simulation Flowmap Speed` 0,75 | Simulationsdaten (gebacken oder Water Info) | nein | **vermutlich ja** | – |
| `Fluidsim Flow Density` 0,25, `Fluidsim Normal Strength` 1, `Fluidsim Velocity EdgeFalloff` 0,2, `Fluidsim Velocity Edgeoffset` 0,02, `Fluid Displacement Multiplier` 1, `Max Fluid Displacement` 1024, `Fluid Eraose Ssaler` 0,5, `Mask Wave Foam near FluidSim` 1, `Wave Foam Erase Near FluidsimSize` 0,5, `ShowSim` 1, `Velocity Debug` 0; Texturen `NormalAndHeight`, `Velocity` | Interaktions-Simulation (Render Targets) | nein | nur um die Spielfigur | **vermutlich ja** |
| `WaterVelocityAndHeight`, `River Flowmap *`, `WPO Flowmap` 6 | Water Info der Water Zone | nein | ja | ja |
| `Absorption`, `Scattering`, `Water Albedo`, `Foam *` | – | nein | ja | ja |

- Kurz: **Am Water Body wirkt in LIVE_SIM keiner dieser Werte**, weil der Water Body dort nicht zeichnet.
- Dieselben Namen in `SW_Water_Material_River` (dieselbe Familie) wirken in LIVE_SIM nur, wenn dieses Material im Niagara-Renderer
  steckt. Das prüft D1.
- `ShowSim` 1 und `Velocity Debug` 0 sind Debug-Schalter: Mit `Velocity Debug` = 1 sollte man in WCBS die Strömung sehen
  [Ableitung aus dem Namen].

**B6. Beispiel-Szenen**

- **Epic:** Ein Forenbericht zu 5.7.4 nennt die mitgelieferte Testkarte **`WaterFluidSimtestShallow`**, in der die SWR funktioniert
  [Forum]. Ältere Leitfäden legen sie unter `Water/Content/FluidSimulation/` ab, damals für die alte Fluid-Sim [Leitfaden]. Im Content
  Browser bei eingeschaltetem „Show Engine Content“ und „Show Plugin Content“ nach `WaterFluidSimtest` bzw. in `/WaterAdvanced/`
  nach `Maps` suchen. Werte daraus kenne ich nicht.
- **Tutorials von Epic:** „Baked River Simulations – Overview and Quick Start“ und „Parameter Reference“ (2025) beschreiben die
  Parameter von SWR, Niagara und Material. Der Inhalt ist aus der Cloud nicht lesbar, nur der Vorspann [Doku].
- **Klares Bachwasser mit Werten:** Weder bei Epic noch in der Community habe ich ein Beispiel gefunden. Die japanischen Leitfäden
  und die 5.6-Videos zeigen den Standard (türkis, viel Schaum). **Bitte die Testkarte lokal öffnen** (D7) und ihre Material- und
  Niagara-Werte mit Skript D1 auslesen.

### Diagnoseplan (lokale Instanz, T1, nichts speichern)

Reihenfolge: Jeder Schritt schließt eine Ursache aus. D1 und D2 dauern zusammen etwa 5 Minuten. Die Ausgabe von D1 bitte als
`bilder/swr/t1_diag_liste.txt` zurück.

**D0. Griffe holen (für alle Schritte)**

```python
import unreal
eas  = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
alle = eas.get_all_level_actors()
swr  = next(a for a in alle if isinstance(a, unreal.ShallowWaterRiver))
comp = swr.get_component_by_class(unreal.ShallowWaterRiverComponent)
nc   = comp.get_editor_property('river_sim_system')          # NiagaraComponent (belegt, nur lesen)
wbs  = [a for a in alle if isinstance(a, unreal.WaterBodyRiver)]
```

**D1. Bestandsaufnahme: wer zeichnet womit (nur lesen)**

```python
def felder(obj):
    aus = []
    for n in sorted(dir(obj)):
        if n.startswith('_'):
            continue
        try:
            aus.append(f'  {n} = {obj.get_editor_property(n)}')
        except Exception:
            pass                                              # Methode oder nicht freigegeben
    return aus

z = ['== ShallowWaterRiverComponent'] + felder(comp)
sysa = nc.get_asset()
z.append(f'== Niagara-System: {sysa.get_path_name()}')
NFL = unreal.NiagaraFunctionLibrary
if hasattr(NFL, 'get_all_emitters'):
    for e in NFL.get_all_emitters(sysa):
        mats = [m.get_path_name() for m in e.get_editor_property('used_renderer_materials') if m]
        nets = [m.get_path_name() for m in e.get_editor_property('used_renderer_meshes') if m]
        z.append(f"  Emitter {e.get_editor_property('emitter_name')} an={e.get_editor_property('is_enabled')} "
                 f"Material={mats} Netze={nets}")
z.append('== NiagaraFunctionLibrary (user/emitter): ' +
         str([f for f in dir(NFL) if 'user' in f.lower() or 'emitter' in f.lower()]))
for wb in wbs:
    wbc = wb.get_component_by_class(unreal.WaterBodyRiverComponent)
    z.append(f'== Water Body {wb.get_actor_label()}')
    for n in ('water_material', 'baked_shallow_water_sim', 'use_baked_sim_for_queries_and_physics'):
        try:
            z.append(f'  {n} = {wbc.get_editor_property(n)}')
        except Exception as ex:
            z.append(f'  {n}: {ex}')
cdo = unreal.ShallowWaterRiverComponent.get_default_object()   # Epic-Standard der Material-Felder
for n in ('baked_sim_material', 'spline_river_material'):
    try:
        z.append(f'  Standard {n} = {cdo.get_editor_property(n)}')
    except Exception as ex:
        z.append(f'  Standard {n}: {ex}')
pfad = unreal.Paths.project_saved_dir() + 't1_diag_liste.txt'
open(pfad, 'w', encoding='utf-8').write('\n'.join(z))
print(pfad)
```

- **Benutzerparameter:** Ob `NiagaraFunctionLibrary` eine Funktion dafür hat (im Auszug `get_all_user_parameters` genannt), ist
  nicht sicher belegt. Die letzte Zeile der Liste zeigt es; dann `help(unreal.NiagaraFunctionLibrary.<name>)` für die Argumente.
- **Sicherer Weg ohne Python:** Im Outliner die SWR wählen, im Komponentenbaum die Niagara-Komponente anklicken. Im Details-Fenster
  steht der Abschnitt mit den Benutzerparametern (je nach Version „User Parameters“ oder „Override Parameters“). Bitte ein
  Bildschirmfoto, dazu ein Foto der Emitter-Liste von `Grid2D_SW_River` im Niagara-Editor (nur ansehen, nicht speichern).
- **Erwartung:** Der Emitter, der die Fläche zeichnet, nennt `SW_Water_Material_River` (oder `…_Niagara_Cached`), der Sekundär-Emitter
  `M_SW_Foam`. `MI_EL_SWR_Fluss` taucht nirgends auf.

**D2. Zeichnet der Water Body in LIVE_SIM überhaupt?**

```python
nc.set_visibility(False)    # Niagara-Ausgabe aus
# Bild ansehen: Ist das Bett jetzt trocken, zeichnet in LIVE_SIM nur Niagara.
nc.set_visibility(True)
```

- Gegenprobe ohne Python: In der Konsole des Viewports `ShowFlag.Particles 0`, danach `ShowFlag.Particles 1`. Ob der Schalter auch
  Niagara-Netz-Renderer ausblendet, ist nicht belegt; `set_visibility` ist der sichere Weg.
- **Ergebnis „trocken“:** Alle Material-Tests am Water Body sind für LIVE_SIM gegenstandslos. Weiter mit D3.

**D3. Sekundär-Emitter aus**

```python
EM = 'SW_River_Secondary_Emitter'          # genauen Namen aus D1 übernehmen
if hasattr(nc, 'set_emitter_enable'):
    nc.set_emitter_enable(EM, False)       # zurück: True
else:
    print('nicht freigegeben -> Kopie des Systems (Weg B)')
```

- Wenn sich nichts ändert, im Output Log nach einer Niagara-Meldung zu `SetEmitterEnable` suchen. Dann **Weg B**:
  `unreal.EditorAssetLibrary.duplicate_asset('/WaterAdvanced/Niagara/Systems/Grid2D_SW_River', '/Game/Eldarien/Welt/Wasser/SWR/NS_EL_SW_River_Diag')`.
  In der Kopie den Haken am Sekundär-Emitter entfernen, `nc.set_asset(unreal.load_asset('/Game/Eldarien/Welt/Wasser/SWR/NS_EL_SW_River_Diag'))`
  und 1–2 Minuten laufen lassen. In derselben Kopie lassen sich auch die Renderer des Haupt-Emitters einzeln abhaken.
- **Erwartung:** Gischtwolke und körnige Flecken verschwinden, der Marmor bleibt. Verschwindet der Marmor, ist meine Annahme falsch und
  die Teilchenzahl bzw. Schwelle des Sekundär-Emitters ist der Hebel.

**D4. Signalfarbe im richtigen Material (Weg C, nur im Speicher)**

```python
MEL = unreal.MaterialEditingLibrary
mi  = unreal.load_asset('/WaterAdvanced/Niagara/Materials/SW_Water_Material_River')   # Pfad aus D1 nehmen
print(MEL.get_scalar_parameter_names(mi)); print(MEL.get_vector_parameter_names(mi))

alt = {}
def setze_v(n, v):
    alt[n] = ('v', MEL.get_material_instance_vector_parameter_value(mi, n))
    MEL.set_material_instance_vector_parameter_value(mi, n, v)
def setze_s(n, v):
    alt[n] = ('s', MEL.get_material_instance_scalar_parameter_value(mi, n))
    MEL.set_material_instance_scalar_parameter_value(mi, n, v)

setze_v('Foam Emissive', unreal.LinearColor(20, 0, 0, 1))     # Probe 1: Schaum leuchtet rot
MEL.update_material_instance(mi)
# Bild. Danach Probe 2 und 3 einzeln: setze_s('Foam Opacity', 0.0) / setze_v('Absorption', unreal.LinearColor(1000, 1000, 1000, 1))

def zurueck():
    for n, (t, w) in alt.items():
        (MEL.set_material_instance_vector_parameter_value if t == 'v' else MEL.set_material_instance_scalar_parameter_value)(mi, n, w)
    MEL.update_material_instance(mi)
# zurueck() aufrufen; beim Schließen „nicht speichern“ wählen.
```

- Die Namen `Foam Emissive`, `Foam Opacity` und `Absorption` stammen aus unserem Master und gelten in `SW_Water_Material` vermutlich
  gleich. Die beiden `print`-Zeilen zeigen die echten Namen.
- **Lesart:**
  - **Probe 1** (Schaum rot): Wird der Marmor rot, ist er Simulations-Schaum. Dann helfen `SimFoam Contrast`, `Foam powr`,
    `Foam Texture Blend Min` und die Schaum-Schwelle im Niagara-System.
  - **Probe 2** (`Foam Opacity` 0): Bleiben nur türkise Schlieren, kommen sie aus Normalen und Spiegelung. Dann helfen die
    Normalstärken, besonders `Sim Velocity Normal Strength` (40 im Standard der Familie) und die Flowmap-Geschwindigkeiten im
    SW-Material.
  - **Probe 3** (Absorption 1000): Wird das Becken glasklar, ist die Konvention „Länge in cm“ auch hier bestätigt (b1).
  - **Ändert sich bei keiner Probe etwas,** zeichnet ein anderes Material. Dann den Pfad aus D1 nehmen, auch `…_Niagara_Cached`.
- Hat D1 einen Benutzerparameter vom Typ Material gezeigt, ist **Weg A** sauberer: `MI_EL_SWR_Fluss` mit
  `nc.set_variable_material('<Name>', unreal.load_asset('/Game/…/MI_EL_SWR_Fluss'))` einsetzen. So wird die Engine nicht angefasst.

**D5. Ansichtsmodi (Konsole im Viewport)**

- `viewmode unlit`: Bleibt der Marmor, steckt er in Farbe/Schaum. Verschwindet er, sind es Licht und Spiegelung (Normalen).
- `viewmode wireframe`: Dichte des Niagara-Netzes. Grobe Dreiecke an den Lippen würden die harten Kanten erklären.
- Zurück mit `viewmode lit`.

**D6. `render_state` durchschalten**

```python
RS = unreal.ShallowWaterRenderState
print([n for n in dir(RS) if n.isupper()])          # alle Zustände, auch DEBUG_*
comp.set_editor_property('render_state', RS.DEBUG_RENDER_BOTTOM_CONTOUR)   # je Aufruf ein Zustand
welt = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
unreal.SystemLibrary.execute_console_command(welt, 'HighResShot 1')        # Bild nach Saved/Screenshots
```

- Jede Änderung startet die Simulation neu [Test 16a]. Deshalb **einen Zustand je Aufruf** und warten, bis die Becken voll sind.
  Kein `time.sleep` im Skript, das blockiert den Editor.
- **DEBUG-Zustände:** Belegt ist nur `DEBUG_RENDER_BOTTOM_CONTOUR`. Gibt es weitere (z. B. für Geschwindigkeit oder Schaum), bitte je
  ein Bild. Liegen die hellen Bereiche des Schaum-Debugs auf dem Marmor, ist D4 Probe 1 bestätigt.
- **Wichtigster Teil:** Einmal **Bake** (Knopf), dann `WATER_COMPONENT_WITH_BAKED_SIM`. Jetzt zeichnet der Water Body mit
  `MI_Eldarien_Wasser_Fluss`. Dann die drei Varianten aus Nachtrag 15:05 wiederholen und zusätzlich `Velocity Debug` = 1 setzen.
  - Wirken die Varianten jetzt, ist bestätigt, dass LIVE_SIM nur die Vorschau ist.
  - Bleibt der Marmor auch hier, steckt er im gebackenen Schaum. Dann ist der Hebel die Schaum-Erzeugung im Niagara-System (D1-Liste).
- Danach `BAKED_SIM`: Das ist die SWR-eigene gebackene Darstellung mit `baked_sim_material`. Hier sollte `MI_EL_SWR_Fluss` wirken.

**D7. Vergleich mit Epics Testkarte**

- `WaterFluidSimtestShallow` öffnen (B6) und D1 dort ausführen. Material- und Niagara-Werte gegen T1 vergleichen.
- Prüfen, ob die Karte dasselbe Muster zeigt. Wenn ja, ist es das Standardaussehen der SWR in schnellem Wasser und kein Fehler bei uns.

### Startwerte für klares Wasser

**Wo:** in dem Material, das D1 als zeichnend ausweist. Für die Vorschau (LIVE_SIM, BAKED_SIM) ist das `MI_EL_SWR_Fluss` (über
Weg A oder B im Niagara-Renderer bzw. als `baked_sim_material`). Für das Spiel (WCBS) ist es `MI_Eldarien_Wasser_Fluss`.

| Parameter | Standard der Familie | **Start** | Zweck |
|---|---|---|---|
| `Absorption` | SW 20,8/25/24,7 | **250 / 1 430 / 2 000** | klar, Grund sichtbar (wie b2) |
| `Scattering` | 0,77/1,0/0,92 | **0,6 / 0,8 / 1,0** | kein Grünstich |
| `Albedo` bzw. `Water Albedo` | 0,083 | **0,03** | weniger milchig |
| `Foam Emissive` | 0,287/1,0/0,188 | **0 / 0 / 0** | kein grüner Schaum |
| `SimFoam Contrast` | 0 | **2** | nur kräftiger Schaum bleibt |
| `Foam powr` | 0,2 | **0,6** | dünner Schaum fällt weg |
| `Foam Texture Blend Min` | 0,4 | **0,6** | Marmortextur erst bei viel Schaum |
| `Sim Velocity Normal Strength` | 40 | **10** | weniger Schlieren in schnellem Wasser (falls D4 Probe 2 Normalen zeigt) |
| `SIm Flowmap Speed` / `Simulation Flowmap Speed` | 1,5 / 0,75 | **0,75 / 0,4** | Textur weniger verzogen [Ableitung] |

- **Niagara-Seite:** Namen erst nach D1. Gesucht sind Benutzerparameter mit „Foam“, „Spawn“, „Threshold“, „Dissipation“/„Decay“ oder
  „Secondary“ im Namen. Ziel wie in b3: Schaum erst ab ≈ 1,5 m/s bzw. an Stufen, Abklingen 2–4 s, Sekundär-Emitter auf ≈ ¼ der
  Teilchen (Gischt nur an Lippe und Fels).
- **Erwartung für T1:** Die Becken werden klar. Die Rinnen bleiben weiß, aber mit weißem statt grünlich-cremigem Schaum und ohne
  flächigen Marmor.

### Quellen (alle Auszüge aus Suchmaschinen; die Seiten selbst gaben Proxy 403)

Epic-Doku und API:
- [Python 5.5: unreal.ShallowWaterRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent?application_version=5.5) – `render_state`, `river_sim_system` (Asset aus den Projekteinstellungen), `water_info_texture`, `baked_*`
- [Python 5.5: unreal.ShallowWaterRiver](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiver?application_version=5.5)
- [Python 5.7: unreal.WaterBodyCustomComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyCustomComponent?application_version=5.7) – `baked_shallow_water_sim`, `use_baked_sim_for_queries_and_physics`
- [Python: unreal.BasicShallowWaterSubsystem](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/BasicShallowWaterSubsystem) – `mpc`, `normal_rt`, `velocity_rt`, `water_info_texture`, `shallow_water_niagara_simulation`
- [Python: unreal.NiagaraFunctionLibrary](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/NiagaraFunctionLibrary) und [unreal.NiagaraMinimalEmitterInfo](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/NiagaraMinimalEmitterInfo) – `get_all_emitters`, `used_renderer_materials`
- [Python 5.6: unreal.NiagaraComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/NiagaraComponent?application_version=5.6) – `set_variable_material`, `set_variable_float`
- [API 4.26: UNiagaraComponent::SetEmitterEnable](https://docs.unrealengine.com/4.26/en-US/API/Plugins/Niagara/UNiagaraComponent/SetEmitterEnable/index.html), [Jira UE-89870](https://issues.unrealengine.com/issue/UE-89870) – behoben ab 5.4
- [Tutorial: Baked River Simulations – Parameter Reference](https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference), [Overview and Quick Start (Forum)](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-overview-and-quick-start/2512102) – Inhalt nicht erreichbar

Epic-Forum:
- [5.6.1: Nach Reset an der SWR verschwindet der Water Body](https://forums.unrealengine.com/t/hi-everyone-new-to-ue-as-i-was-working-on-a-shot-in-ue-5-6-1-i-got-stuck-somewhere-i-was-using-water-body-river-the-i-used-shallow-water-river-and-attached-the-water-body-and-clicked-reset-but-as-soon-as-i-clicked-reset-the-water-body-completely/2741247)
- [Unreal 5.6 water simulation](https://forums.unrealengine.com/t/unreal-5-6-water-simulation/2626503) – Material-Überschreibung wirkt nur mit „Water Component with Baked Sim“ (Auszug; Zuordnung zu genau diesem Thread nicht sicher)
- [ShallowWaterRiver simulation does not initialize in 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772) – Testkarte `WaterFluidSimtestShallow`
- [Shallow body river – Water Component with Baked Sim not rendering](https://forums.unrealengine.com/t/shallow-body-river-water-component-with-baked-sim-not-rendering/2688228) – WCBS zeigt nur Schaum
- [GPU Water Depth calculated wrong in Water Info](https://forums.unrealengine.com/t/gpu-water-depth-calculated-wrong-in-water-info/2743113) – Kanäle der Water-Info-Textur
- [Too much foam on water](https://forums.unrealengine.com/t/too-much-foam-on-water/2404908) – Schaum in Simulation und Material (ältere Fluid-Sim)

Leitfäden:
- [hxsd: Unreal Wasser-System Teil 2 (chinesisch)](https://jiaocheng.hxsd.com/course/content/12003/) – Lage von `WaterFluidSimtestShallow` (ältere Version)

Projekt:
- `vorlagen/daten/material_parameter.json` (`M_Eldarien_Wasser_Schaum8`, alle `Sim *`-, `Fluidsim *`- und `BakedWaterSim*`-Werte)
- `vorlagen/daten/inventar_extra.json` (`MI_Eldarien_Wasser_FlussSim` → `SW_Water_Material_River_Niagara_Cached`)

### Rückfragen

1. **Ferats Video:** Titel und Kanal? Dann ziehe ich die Werte daraus nach (über Suchauszüge, YouTube ist gesperrt).
2. **`MI_Eldarien_Wasser_FlussSim`** (Eltern `SW_Water_Material_River_Niagara_Cached`) liegt schon im Projekt. Wofür wurde es angelegt,
   und war es irgendwo eingesetzt? Es ist der natürliche Kandidat für den Niagara-Renderer (Weg A/B).
3. **Reihenfolge:** Darf D6 (Bake + WCBS) vor D3–D5 laufen? Für das Spiel zählt nur WCBS. Zeigt T1 dort klares Wasser, reicht für
   LIVE_SIM eine grobe Vorschau, und D3–D5 werden zur Kür.
4. **Kopie des Niagara-Systems** unter `/Game/Eldarien/Welt/Wasser/SWR/` (Weg B): einverstanden? Sie wäre auch der Ort für eigene
   Schaum-Schwellen im Spiel, wenn die Benutzerparameter nicht reichen.
