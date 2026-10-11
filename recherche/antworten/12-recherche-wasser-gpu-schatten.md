# Antwort zu Auftrag 12 – Stufen-Wasserfälle, GPU-Hänger, VSM-Cache-Kacheln (UE 5.8)

Stand: 11.10.2026. Reine Web-Recherche aus der Cloud. Wichtig zur Quellenlage: Die Epic-Seiten (dev.epicgames.com, forums.unrealengine.com,
issues.unrealengine.com, fab.com) waren von hier aus nicht abrufbar. Aussagen von dort beruhen auf Suchergebnis-Auszügen und sind markiert
([S] bzw. „(Auszug)“). CVar-Namen und Standardwerte wurden gegen Engine-Quelltext 5.4–5.6 abgeglichen ([Q…]), nicht gegen 5.8. **Jeden Namen
im Editor einmal mit `help <CVar>` bestätigen.**

## Kurzfazit

- **Wasserfälle:** Die „Terrassen ohne Fallkante“ kommen sehr wahrscheinlich aus der Water-Info-Textur: ein Höhenwert je ~1,2 m und
  standardmäßig 16-Bit-Höhen über den ganzen Höhenbereich der Zone (Stufen von 15–50 cm). Erster Test: `bHalfPrecisionTexture = false`
  an der Water Zone. Aufbau: je Becken ein eigener `WaterBodyRiver`, an der Stufe mit Lücke ≥ 1,2 m getrennt, Vorhang als Translucent-Mesh
  2–5 cm über dem Wasser mit Depth Fade, Schaum als gebackene Maske im Wassermaterial plus kleine Flipbook-Scheibe; Niagara nur nah.
- **GPU-Hänger:** PatchSplit ist der Nanite-Tessellations-Shader. Ein bekannter Epic-Bug (UE-277458, VSM-Schatten tessellierter
  Nanite-Landschaft) galt seit 5.6 als behoben, der Fall ist also vermutlich ein neuer Grenzfall in 5.8. Erste Abhilfe ohne Optikverlust im
  Hauptbild: Tessellation nur in den Schatten aus (`r.Shadow.Virtual.Nanite.AllowTessellationDirectional 0`, `...Local 0`, neu in 5.8),
  dann `r.Nanite.DicingRate 4`. Die „5 s“ sind Unreals D3D12-Wachhund `r.D3D12.SubmissionTimeout`, nicht Windows-TDR.
- **VSM-Kacheln:** Bekanntes Muster: Seiten werden nach Geometriewechsel beim Streaming nicht invalidiert (am nächsten UE-215659,
  HLOD-Tausch, offen mit Ziel 5.8). Einen Befehl, der nur den Cache leert, gibt es nicht. Praktisch: `r.Shadow.Virtual.Cache 0` nur für die
  Aufnahme, einige Frames warten, HighResShot, dann `1`. Im Spiel hilft nur die Ursache (HLODs und Nanite-Landschaft aktuell bauen).


## Teil A – Kleine Wasserfälle an Bachstufen

Stand 11.10.2026. Quellenlage: dev.epicgames.com, forums.unrealengine.com, issues.unrealengine.com, fab.com, 80.lv, therookies.co und lilys.ai waren per WebFetch **nicht erreichbar (DNS-Fehler)**. Diese Quellen sind nur aus Suchmaschinen-Auszügen belegt und mit „(Auszug)“ markiert. Direkt gelesen wurden zwei Dinge: der Water-Plugin-Quellcode in einem inoffiziellen Spiegel (nicht verlinkt) (**Engine-Version 5.6.1**, laut `Version.h` des Spiegels) und Epics Water-Doku als Markdown-Kopie (**Stand 5.6**, verarbeitet am 14.06.2025). Was nur für 5.6 oder älter belegt ist, steht mit [≤5.6] dabei. „Ableitung“ heißt: aus Code oder Doku gefolgert, nicht im Editor getestet.

### Kurzfazit

1. **Epic Water kann keine Fallkante darstellen.** Die Höhe der Wasseroberfläche kommt aus der Water-Info-Textur, die das Wasser von oben aufnimmt (ein Höhenwert je Texel, ~1,2 m). Jede Stufe wird deshalb zur Rampe über mindestens 1–2 Texel. Zusätzlich speichert die Zone die Wasserhöhe standardmäßig als 16-Bit-Float, normiert auf den gesamten Höhenbereich der Zone. Bei mehreren hundert Metern Höhenunterschied ergibt das **Höhenstufen von 15–50 cm**. Das erklärt sehr wahrscheinlich die „regelmäßigen Terrassen“ (Ableitung aus Code). Erster Test: `bHalfPrecisionTexture = false` an der Water Zone.
2. **Bewährter Aufbau:** Je Becken ein eigener `WaterBodyRiver`, an der Stufe mit Lücke getrennt. Darüber kommt der Vorhang als **Translucent**-Static-Mesh (nicht Single Layer Water, nicht Nanite), 2–5 cm über der Wasserfläche, mit Depth Fade an Felsen und Becken. Der Teil unter der Beckenoberfläche wird von der Engine ohnehin nicht gezeichnet (5.8-Forum, Epic-Antwort). Das ist für den Vorhangfuß sogar nützlich.
3. **Schaum am Fuß:** Kein Decal (Decals greifen nach Forenberichten nicht auf Single Layer Water). Am günstigsten und sortierfrei ist eine **im Wassermaterial gesampelte, per Python gebackene Schaummaske** (Weltraum-Textur je Zone), ergänzt um eine kleine durchscheinende Flipbook-Schaumscheibe direkt am Aufprall. **Niagara** (GPU-Sprites für Gischt/Nebel) nur in der Nähe der Kamera: Cull-Distanz ~40–60 m, kein Schattenwurf.
4. **Water Body Exclusion Volume und Water Mesh Override taugen nicht zum Ausschneiden von Flussstücken.** Das Exclusion Volume ist für Gameplay-Abfragen gedacht; das Ausblenden der Oberfläche war in 5.1 fehlerhaft, und ein 5.8-Forenbericht sagt, es wirkt gar nicht. Den Override setzt der Code beim Laden bei Rivers sehr wahrscheinlich zurück [≤5.6].
5. **Fertig-Assets:** Nichts Kostenloses mit belegter 5.8-Freigabe gefunden. Kandidaten sind *Waterfall Pro* (Niagara, ab ~50 $), *Realistic Waterfall and Water VFX* (Dr.Game, ab ~20 $), *Waterfall Fx* (VFX4GAME, ab ~40 $) und *SHADERSOURCE Waterfall Tool 2* (Editor-Modus). Preise und Engine-Versionen sind auf Fab ungeprüft. Für Eldarien lohnt eher der Eigenbau (Vertex-Farb-Vorhang), mit Paketen nur als Textur- und Flipbook-Quelle.

---

### Frage 1 – Wie lösen andere das? Übergänge Fluss-Spline ↔ Wasserfall-Netz

**Befund aus der Praxis**
- **Mesh-Vorhang mit Flowmap/Vertex-Farbe, Depth Fade und Schaum aus Vertex-Farbe ist der verbreitete Ansatz.** Ein UE5-Open-World-Breakdown (The Rookies, 2024, Auszug) beschreibt das so: Wasserfall-„enclosure meshes“ mit dem Wassermaterial, Flowmap aus den R/G-Vertex-Farben, Schaum aus Vertex-Farbe plus Kollision mit opaker Geometrie, Opazität und Refraktion über Depth Fade. Epics Forum nennt Wasserfälle allgemein „hard tweaking“ und verweist auf die Cave- und Particle-Demos (UE4-Ära, Auszug).
- **Epic Water liefert keine eigene Wasserfall-Lösung.** Die Doku (5.6) kennt nur River, Lake, Ocean und Custom sowie Übergangsmaterialien River→Lake und River→Ocean. Ein River→River-Übergang ist ausdrücklich nicht vorgesehen: „rivers can't have custom transitions to other rivers“ (Code-Kommentar in `WaterQuadTree.cpp` [≤5.6]). Kontaktschaum am Fluss ist laut früherer Recherche nicht vorgesehen; Epics eigene Demo nutzte dafür Niagara (Forum, Auszug).
- **Alternativen mit Simulation:** Niagara Fluids und der 5.6 eingeführte, experimentelle *Shallow Water River* aus dem Plugin *Water Advanced* (Witcher-4-Demo, Unreal Fest 2025). Der Shallow Water River ist **in 5.8 gemeldet defekt** (frühere Recherche), in 5.7 scheitert das Baking mit mehreren Flüssen (Forum, Auszug). Für Eldarien deshalb **nicht** einplanen. Kommerziell gibt es Fluid Flux (80.lv-Wasserfall-Demo, Auszug).

**Übergangs-Tricks**

| Trick | Wirkung | Bewertung für Eldarien |
|---|---|---|
| **Fluss an der Stufe teilen** (ein `WaterBodyRiver` je Becken, Ende ~0,5–1 m hinter der Kante, nächster Anfang 1–2 m stromab der Fallfußlinie) | Keine Rampe im Wassernetz, jede Beckenfläche bleibt flach. Den Spalt deckt der Vorhang ab. | **Empfohlen.** Achtung: In der Draufsicht dürfen sich die Teilstücke nicht überlappen, sonst schreibt die Info-Textur dort die Höhe des oberen Stücks (Aufnahme von oben, Tiefentest; Ableitung aus `WaterInfoRendering.cpp`). Abstand ≥ 1 Info-Texel (≥ 1,2 m). |
| **Höhenversatz Vorhang** | Vorhang-Oberkante 2–5 cm über der Wasserfläche des oberen Beckens, ~0,3–0,5 m stromauf der Kante beginnen und dort per Vertex-Alpha auf 0 ausblenden | Verhindert Z-Fighting mit der Wasserfläche. Den Vorhang-Fuß 0,2–0,5 m unter die Beckenoberfläche ziehen. |
| **Durchscheinend vs. Single Layer Water** | Single Layer Water rendert *nach* Base Pass und Lighting, *vor* der normalen Translucency (Epic SLW-Doku, Auszug). Zwei SLW-Flächen hintereinander sind eine Engine-Grenze (Forum, Epic-nahe Antwort, Auszug). | Vorhang **muss Translucent sein**. Das Becken bleibt SLW. Translucent unter der Wasseroberfläche wird bei Kamera über Wasser **nicht gezeichnet**: In 5.8 bestätigt, Epic: „task in our backlog … not on the roadmap for UE5“ (Forum, Auszug). Den versenkten Teil also nicht sichtbar einplanen. |
| **Depth Fade** | Weicher Übergang des Vorhangs an Fels und Beckenoberfläche. Die SLW-Fläche liegt beim Translucency-Pass schon im Tiefenpuffer (Ableitung aus Renderreihenfolge plus 5.8-Befund). | `DepthFade` FadeDistance 15–40 cm auf Opacity. Gleiche Werte im Schaummaterial. |
| **Translucency Sort Priority** | Sortiert nur durchscheinende Objekte untereinander, nicht gegen SLW. Bei gleicher Priorität gilt die Reihenfolge nach Bounds-Ursprung, hinten zuerst (Epic-API, Auszug). Forenfälle: Spritzer hinter Wasser nur über Sort Priority lösbar (Auszug). | Vorhang 0, Schaumscheibe 1, Niagara-Gischt 2. Bei Spritzer-Fehlern zusätzlich „Separate Translucency“ und „Render After DOF“ im Material prüfen (Forum, Auszug). |
| **Water Zone / Water Mesh Override** | Ein Override auf einem River ersetzt die Wassernetz-Kacheln durch **SplineMeshComponents je Spline-Segment** (folgen exakt dem Spline, `SetCastShadow(false)`). Aber `PostLoad` setzt `WaterMeshOverride` bei allen Nicht-Custom-Bodies auf `nullptr`, wenn das Alt-Flag `bOverrideWaterMesh_DEPRECATED` nicht gesetzt ist (Code 5.6.1). | **Nicht nutzen.** Der Override überlebt das Neuladen sehr wahrscheinlich nicht (Ableitung, ungeprüft in 5.8). Water Body Custom mit Static Mesh hat eigene Bugs: kein Info-Mesh bis 5.6.1 offen; Nanite-Mesh als Override → Absturz (5.1). Alles Auszüge. |
| **Water Body Exclusion Volume** | Doku 5.6: „excludes all Water Bodies from visually appearing“. Klassenkommentar im Code: nur „players not enter surface swimming“. UE-170684 (5.1): Oberfläche bleibt sichtbar. Forum 5.8: „does nothing“. | **Nicht verlassen.** |
| **Eigene Water Zone für den Bach** | `WaterZoneOverride` am Body und `OverlapPriority` an der Zone existieren (Code 5.6.1). Eine kleine Zone (z. B. 256 m × 256 m bei 1024² → 25 cm/Texel) nur für den Bach gibt viel feinere Höhen. | Plausibel, **ungeprüft**. In 5.8 braucht eine Zone nach TileSize-/Extent-Änderung ein zweites `MarkForRebuild` (frühere Recherche). |

### Frage 2 – Schaum: Decal vs. Mesh mit Flipbook vs. Niagara

| Variante | Kosten | Lumen/VSM | Eignung |
|---|---|---|---|
| **Decal (DBuffer)** | Billig auf opaken Flächen | Forenberichte: Decals erscheinen auf SLW nicht. Deferred-Decals gehen über den GBuffer, SLW und Translucency liegen nicht im GBuffer (Auszüge, keine Epic-Bestätigung). | **Für Schaum auf dem Wasser ungeeignet.** Nur für nassen Fels und Ufer am Fuß. |
| **Schaummaske im Wassermaterial** (gebackene Weltraum-Textur, z. B. 1 Texel = 0,25–0,5 m, R = Fallfuß-Schaum, G = Schnellen-Turbulenz) | 1 Textur-Sample + wenige ALU im SLW-Pass, **kein Overdraw, keine Sortierung** | Wird von SLW korrekt beleuchtet und reflektiert | **Primär** (Ableitung). Fügt sich in den vorhandenen Abstandsfeld-Schaum ein (frühere Recherche: `DistanceToNearestSurface`). Animation über Panner/Flow aus Water-Info-Velocity. |
| **Mesh-Scheibe mit Flipbook** (Translucent, 1 Layer, 2–4 m Ø) | 1 Lage Overdraw auf kleiner Bildfläche. Flipbook = 1 Sample (SubUV/`FlipBook`-Knoten). | Translucent: Lumen nur grob über das Translucency Lighting Volume. Directional Light mit Self-Shadow pro Pixel, Punkt- und Spotlichter grob (Epic Lit Translucency, Auszug, teils UE4-Stand). | **Sekundär**, direkt am Aufprall. Lighting Mode *Surface TranslucencyVolume* oder *Volumetric NonDirectional* (Empfehlung, ungeprüft). Alternative: **Masked + DitherTemporalAA**. Schreibt Tiefe, keine Sortierprobleme, korrektes VSM, aber Dither-Rauschen unter TSR. |
| **Niagara GPU-Sprites** (Gischt/Nebel) | Overdraw = Bildfläche × Lagen. Lit-Material wird schnell teuer. Weniger, größere Sprites sind besser. **Particle Cutout** senkt Overdraw stark (realtimevfx, Auszug). GPU-Sim braucht feste Bounds (Epic-Doku, Auszug). | Translucent, s. o. **Cast Shadow aus.** Bewegte Schattenwerfer invalidieren VSM-Seiten jedes Frame (Shadow Cache Invalidation „Auto“, Epic-API, Auszug). | **Tertiär.** 1 System je Stufe, Spawn ~20–60 Sprites/s, Lebensdauer 1–2 s, Cull 40–60 m (Werte = Ableitung). |
| **Niagara Ribbons / Mesh-Partikel** | Ribbons für Strahlen-Einzelfäden; Mesh-Partikel (Masked) für Gischtklumpen ohne Translucency-Overdraw (realtimevfx, Auszug) | Masked-Mesh-Partikel: korrektes VSM, aber Cast Shadow aus | Für kleine Stufen (2–4 m) verzichtbar |

**Empfehlung:** Maske im Wassermaterial (immer an) + 1 Flipbook-Scheibe am Fuß + optional 1 GPU-Sprite-Gischtsystem mit kurzer Cull-Distanz. Für Vorhang und Schaum: Nanite aus (Nanite unterstützt keine Translucency; allgemeine Epic-Nanite-Regel, hier nicht neu belegt), Cast Shadow aus. Bei WPO-Animation `Shadow Cache Invalidation Behavior = Rigid`.

### Frage 3 – Zeichnet Epic Water steile Flussstücke korrekt?

**Mechanik laut Code (5.6.1) und Doku (5.6)**
- **Body-Mesh folgt dem Spline.** `GenerateWaterBodyMesh` tastet den Spline adaptiv ab (`ConvertSplineToPolyLineWithDistances(…, FMath::Square(5.f), …)`). Die Ecken übernehmen die Spline-Höhe, Breite = `RiverWidth.Eval(Key)`. Quer zur Fließrichtung bleibt die Fläche waagerecht (`OutwardDistance.Z = 0`). Tempo und Richtung stehen gepackt in der Vertex-Farbe (`PackFlowData`).
- **Gerendert wird aber über das Wassernetz.** Jede River-Kachel liegt auf einer Basishöhe = **Oberkante ihrer Bounding-Box** („for rivers: top of the bounding box“, `WaterQuadTree.cpp`). Die echte Höhe kommt per Verschiebung im Material aus der Water-Info-Textur. Das Material bekommt dazu den Parameter `WaterVelocityAndHeight` = `WaterInfoTextureArray`, und die Doku-CVar `ShowWireframeAtBaseHeight` zeigt das Netz „with no displacement“.
- **Water-Info-Textur:** XY = Velocity, Z = Wasserhöhe, W = Bodenhöhe. Z ist normiert auf `WaterHeightExtents` = min/max der **Bounds aller Bodies der Zone** (`WaterInfoMerge.usf`, `WaterZoneActor.cpp`). Standard: 512² über 512 m (1 m/Texel), Format `RGBA16f` bei `bHalfPrecisionTexture = true`.
- **Folge 1 – Treppeneffekt (Ableitung):** Ein Half-Float hat im Bereich [0,5; 1) eine Schrittweite von 2⁻¹¹ ≈ 0,00049. Bei 600 m Zonen-Höhenbereich sind das **~29 cm Höhenstufen**, bei 1000 m ~49 cm. Im Becken (12 % Gefälle, 1,2 m Texel → 14 cm je Texel) teilen sich so 2–4 Texel denselben Wert, dann springt er. Das ergibt flache Terrassen mit kurzer Rampe, ohne Fallkante.
- **Folge 2 – keine senkrechte Kante:** Ein Höhenwert je Texel. Eine 2–4-m-Stufe wird bei 1,2 m/Texel zur Rampe von ≥ 1,2–2,4 m Länge, bei LOD-Vergröberung in der Ferne noch weicher. `TileSize` 2400 cm, `TessellationFactor` 6 (max. 12), `LODScale` 1. LOD halbiert die Vertexdichte je Ring (Doku).
- **Folge 3 – Velocity:** Begrenzt durch `r.Water.MaxFlowVelocity` = 1024 (cm/s) bei der Kodierung. Pro Zone wird geblurrt (`VelocityBlurRadius`, 0–16). Das Wasser „fließt“ nur in der Draufsicht, es gibt keinen Fallanteil.
- **Spline-Punkte:** `Depth` (Standard 150 cm), `RiverWidth` (2048), `Velocity` (128) gelten je Punkt. Negative Velocity kehrt die Richtung um (Doku und Code). Die Tiefe formt nur das Bett bzw. das Landschaftsschnitzen (Elevation Curve, Y = 1 lassen), nicht die Oberfläche.
- **Bekannte Grenzen (Auszüge):** Steile Flüsse am Hang sind „very difficult“ (Kommentar unter einem YouTube-Tutorial). Water-Info-Fehler zeigen sich als „strange blocks“ (UE-296375, VR). In MRQ fehlt das Info-Update (UE-213949). Eine Epic-Aussage speziell zu steilen Flüssen wurde nicht gefunden.

**Tipps**
1. Zuerst `bHalfPrecisionTexture = false` setzen (RGBA32F). Speicher: 2048² × 16 B ≈ 64 MB je Slice statt 32 MB. Danach prüfen, ob die Terrassen verschwinden.
2. Flussstücke an jeder Stufe teilen (s. Frage 1). Pro Becken liegt dann 1 Body mit fast konstanter Höhe vor.
3. Feinere Info-Auflösung: kleinere Bach-Zone oder höhere `RenderTargetResolution`. Alternativ Zonen je Talabschnitt, damit der Höhenbereich klein bleibt (verringert auch Punkt 1).
4. Spline-Punkte gezielt setzen: je Stufe ein Punkt an der Kante und einer am Fuß, Tangenten flach (Spline-Punkt-Typ *Linear* oder *Curve Clamped*), damit die Polylinie nicht überschwingt.
5. Velocity: Becken 50–100 cm/s, Schnelle 200–400 cm/s. Unter 1024 bleiben, sonst wird abgeschnitten.
6. Fallanteil nur im Vorhang-Material: Fallgeschwindigkeit ≈ √(2·g·h), bei 2 m ≈ 6,3 m/s (Physik, Ableitung).

### Frage 4 – Fertig-Assets (Fab), Preise und Versionen ungeprüft

| Name | Inhalt | Preis-Hinweis | UE-Version | Link |
|---|---|---|---|---|
| Waterfall Pro (vermutlich JVAD3D) | Interaktives Niagara-Wasserfallsystem, CPU- und GPU-Variante, „blends with the top river and bottom river“, nur Niagara + 4 Sounds | „From $49.99“ (Kategorie-Auszug) | ungeprüft | [Fab](https://www.fab.com/listings/024c679f-c9b7-453b-bd6b-2416acd5c4fc) |
| Realistic Waterfall and Water VFX (Dr.Game) | 12 Partikelsysteme, 19+ Texturen, 13 Blueprints, 9 Loop-Sounds | „From $19.99“ | ungeprüft (UE4 auf Anfrage) | [Fab](https://fab.com/s/2963561bcd7f) |
| Waterfall Fx (VFX4GAME) | Wasserfall-VFX | „From $39.99“ | ungeprüft | [Fab-Kategorie Liquid](https://www.fab.com/category/vfx/liquid) |
| Nature Water FX (SHOGUN GAMES) | Brunnen, Geysire, Bäche, Wasserfälle | „From $44.99“ | ungeprüft | [Fab-Kategorie Liquid](https://www.fab.com/category/vfx/liquid) |
| SHADERSOURCE Waterfall Tool 2 | Editor-Modus: Wasserfall-Actor erzeugt Pfade, Meshes und VFX am Felsen, Beispielmaterialien und Niagara | ungeprüft | ungeprüft | [Fab](https://fab.com/listings/f44cd11c-4202-4e63-b74d-be09b1749b6e) |
| Twinkle Pop VFX – Realistic Waterfall VFX | Animiertes Wasserfallmaterial, gebogene Fläche, Schaum-Partikel | ungeprüft | ungeprüft | [Forum](https://forums.unrealengine.com/t/twinkle-pop-vfx-realistic-waterfall-vfx/2737739) |
| Niagara Examples Pack (Epic) | 50+ Niagara-Systeme, u. a. Mist Cards. Kein Wasserfall, aber Nebel/Gischt-Vorlagen. | **kostenlos** | 5.7 | [Epic News](https://www.unrealengine.com/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7) |
| Content Examples (Epic), Karte *Niagara_Fluids* | Fluss mit Niagara Fluids und SLW | kostenlos | aktuelle 5.x (laut 80.lv „constantly updated“) | [80.lv](https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations) |

Kein Paket hat eine belegte **5.8**-Freigabe. Vor dem Kauf auf Fab „Supported Engine Versions“ prüfen. Niagara- und Material-Assets aus 5.4–5.7 lassen sich erfahrungsgemäß hochmigrieren; für 5.8 ist das ungeprüft.

---

### Konkrete Einstellungen/Werte

**Water Zone (Bach-Bereich)**
- `bHalfPrecisionTexture = False`
- `RenderTargetResolution`: so wählen, dass ≤ 0,5 m/Texel (z. B. 1024 für 512 m)
- `VelocityBlurRadius = 1`
- `CaptureZOffset = 64`
- `OverlapPriority = 1` bei einer Bach-Zone innerhalb der Hauptzone; an den Bach-Bodies `WaterZoneOverride` = Bach-Zone (ungeprüft)
- Nach Änderung: `r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames 2` und in 5.8 zweimal `MarkForRebuild`

**WaterBodyRiver je Becken**
- Endpunkt 0,5–1 m hinter der Kante, Startpunkt 1–2 m stromab des Fallfußes, XY-Lücke ≥ 1,2 m
- `Velocity` 50–100 (Becken) / 200–400 (Schnelle)
- `OverlapMaterialPriority` gleich lassen
- `ShapeDilation` Standard 4096 lassen (füllt Lücken in der Info-Textur; über Gelände wird gestaucht, `UndergroundDilationDepthOffset` 64)

**Vorhang-Material** (`M_Eldarien_Wasserfall`)
- Blend Mode *Translucent*, Shading *Default Lit*, Lighting Mode *Surface TranslucencyVolume*
- Separate Translucency an, Two Sided an, Usage *Static Mesh*; Nanite am Mesh aus
- Opacity = `VertexColor.A × Fresnel(Exponent 3) × DepthFade(FadeDistance 25)`
- Flow: `Panner(Speed Y = 0,3–1,5 × VertexColor.R)` auf zwei phasenversetzten Normal-Samples (klassisches Flowmap-Crossfade mit `Frac(Time × 0,5)`)
- Schaumanteil = `VertexColor.B`, Rand = `VertexColor.G` (Konvention aus dem Auftrag)
- Translucency Sort Priority 0, Cast Shadow aus

**Schaumscheibe:** Translucent, `FlipBook`-Knoten (4×4 oder 8×8), `DepthFade` 15–30 cm, 2–3 cm über der Beckenfläche, Sort Priority 1. Alternative: Masked + `DitherTemporalAA`.

**Wassermaterial (Kind von MI_Eldarien_Wasser_Basis):**
- Neuer Texturparameter `SchaumMaske` (Weltraum-UV = `(WorldPosition.xy − ZonenUrsprung) / ZonenGröße`)
- Schaum = max(Abstandsfeld-Schaum, `SchaumMaske.R × Noise(Flow)`)
- Maske per Python aus den Stufen-Fußpunkten backen (Radius 1,5–3 m, Ableitung)

**Niagara-Gischt:** GPU Sim, Fixed Bounds, Sprite Renderer mit Cutout (8 Vertices), Cull/MaxDistance 5000 cm, Scalability *Effect Type* mit Significance, Cast Shadow aus, Sort Priority 2.

**Debug:**
- `r.Water.WaterMesh.ShowWireframe 1`
- `r.Water.WaterMesh.ShowWireframeAtBaseHeight 1`
- `r.Water.WaterMesh.ShowTileBounds 1`
- `stat watermesh`
- `r.Water.WaterInfo.DrawPerViewDebugInfo 1`

### Risiken
- Die Half-Precision-Hypothese ist eine Ableitung aus dem Code (5.6.1). Ob das Material bilinear filtert und ob 5.8 den Code geändert hat, ist nicht geprüft. Erst testen, dann umbauen.
- Teilstücke, die sich in der Draufsicht überlappen, verfälschen die Höhen in der Info-Textur. Jede Teilung erzeugt zusätzlich eigenes Landschaftsschnitzen, falls `bAffectsLandscape` aktiv ist.
- Translucency unter der SLW-Oberfläche fehlt in 5.8 (Epic: nicht auf der UE5-Roadmap). Unterwasser-Vorhang oder Schaum ist bei Kamera über Wasser unsichtbar.
- `WaterMeshOverride` und das Exclusion Volume sind unzuverlässig (s. Frage 1).
- Viele durchscheinende Lagen im Nahbereich (Vorhang + Scheibe + Sprites) bedeuten Overdraw. Lit Translucency ist unter Lumen nur grob beleuchtet und kann im Schatten zu hell wirken. Gegenmittel: Emissive/Specular dämpfen, Sky-Occlusion-Faktor im Material.
- Shallow Water River und Water Advanced sind in 5.8 defekt bzw. experimentell.
- Fab-Preise und -Versionen stammen aus Suchauszügen.

### Quellen
- Epic-Doku (gelesen über eine Markdown-Kopie, Stand 5.6; nur Originale verlinkt): [Water Meshing System and Surface Rendering](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-meshing-system-and-surface-rendering-in-unreal-engine), [Water Body Actors](https://dev.epicgames.com/documentation/unreal-engine/water-body-actors-in-unreal-engine)
- Engine-Code 5.6.1 (inoffizieller Spiegel, nicht verlinkt; Original im zugangsbeschränkten Repo `EpicGames/UnrealEngine`, Plugin `Engine/Plugins/Experimental/Water`): `WaterBodyRiverComponent.cpp`, `WaterBodyComponent.cpp/.h`, `WaterZoneActor.cpp/.h`, `WaterInfoMerge.usf`, `WaterInfoRendering.cpp`, `WaterQuadTree.cpp`, `WaterMeshComponent.h`, `WaterMeshSceneProxy.cpp`, `WaterUtils.cpp`, `WaterBodyExclusionVolume.h`
- Single Layer Water / Translucency (Auszüge): [Epic SLW-Doku](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine) · [Forum 5.8: Translucent Objects do not render below water](https://forums.unrealengine.com/t/translucent-objects-do-not-render-below-water/2763121) · [Forum: zwei SLW-Flächen (Alembic Splash Pack)](https://forums.unrealengine.com/t/2450802) · [realtimevfx: Decal über Ozean](https://realtimevfx.com/t/scene-depth-lit-opaque-ocean-help/30739) · [Epic Lit Translucency](https://dev.epicgames.com/documentation/en-us/unreal-engine/lit-translucency-in-unreal-engine) · [TranslucencySortPriority API](https://docs.unrealengine.com/4.26/en-US/API/Runtime/Foliage/UFoliageType/TranslucencySortPriority/index.html) · [Forum Waterfall Study (Sort Order)](https://forums.unrealengine.com/t/waterfall-study/100448) · [Forum Separate Translucency + Sort Priority](https://forums.unrealengine.com/t/better-tooltip-for-translucency-sort-priority-separate-translucency/357692)
- Exclusion Volume / Override (Auszüge): [UE-170684](https://issues.unrealengine.com/issue/UE-170684) · [Forum 5.8 Exclusion Volumes](https://forums.unrealengine.com/t/waterbody-exlusion-volumes-dont-work/2740432) · [UE-189801 (Nanite-Override-Absturz)](https://issues.unrealengine.com/issue/UE-189801) · [UE-300372 (Custom ohne Info-Mesh)](https://issues.unrealengine.com/issue/UE-300372) · [UE-296375](https://issues.unrealengine.com/issue/UE-296375) · [UE-213949](https://issues.unrealengine.com/issue/UE-213949)
- Praxis/Breakdowns (Auszüge): [The Rookies – Open World UE5 Part 3](https://www.therookies.co/blog/breakdowns/creating-open-world-environments-in-unreal-engine-5-part-3) · [Forum „waterfall ?“](https://forums.unrealengine.com/t/waterfall/50020) · [Forum Foam on Rivers](https://forums.unrealengine.com/t/water-plugin-in-ue5-does-anyone-know-how-to-use-the-foam-on-rivers-see-video-linked/688819) · [80.lv Waterfall Scene UE5](https://80.lv/articles/fascinating-immersive-waterfall-scene-created-with-unreal-engine-5/) · [80.lv Fluid Flux Waterfall](https://80.lv/articles/real-time-waterfall-simulation-made-with-the-fluid-flux-add-on/) · [80.lv Water Sims UE 5.8](https://80.lv/articles/exploring-real-time-water-simulations-in-unreal-engine-5-8/) · [YouTube: UE 5.3 Forest/River/Lake (Kommentar steile Flüsse)](https://yt.d0.cx/v/yt/rNAzlf4vPV8?locale=en) · [cgworld: Shallow Water River 5.6](https://cgworld.jp/flashnews/01-202602-UE-Water.html) · [Forum 5.7 Baking fails](https://forums.unrealengine.com/t/ue-5-7-water-plugin-baking-fails-after-adding-an-additional-waterriver/2732713/2) · [Water Advanced Plugin-Index](https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/WaterAdvanced)
- Kosten Niagara/Schatten (Auszüge): [realtimevfx Niagara-Optimierung](https://realtimevfx.com/t/niagara-and-vfx-optimization-how/25656) · [realtimevfx Optimize VFX](https://realtimevfx.com/t/best-ways-to-optimize-vfx-in-unreal/828?page=2) · [Epic GPU-Sprite-Effekt](https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-create-a-gpu-sprite-effect-in-niagara-for-unreal-engine) · [ShadowCacheInvalidationBehavior](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShadowCacheInvalidationBehavior)
- Fab/Assets (Auszüge): [Fab VFX Liquid](https://www.fab.com/category/vfx/liquid) · [Waterfall Tool 2](https://fab.com/listings/f44cd11c-4202-4e63-b74d-be09b1749b6e) · [Waterfall Pro](https://www.fab.com/listings/024c679f-c9b7-453b-bd6b-2416acd5c4fc) · [Dr.Game Realistic Waterfall](https://fab.com/s/2963561bcd7f) · [Twinkle Pop Waterfall](https://forums.unrealengine.com/t/twinkle-pop-vfx-realistic-waterfall-vfx/2737739) · [Niagara Examples Pack 5.7](https://www.unrealengine.com/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7) · [80.lv Niagara Fluids / Content Examples](https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations)
- Kontext früherer Recherche: `recherche/antworten/ufer-kies-coast-dunes.md` (Water-Zone-Defaults, SLW-CVars, Shallow Water 5.8 defekt, ue-mcp #1156)


## Teil B – GPU-Hänger in Nanite PatchSplit

> **Wie belegt:** Epic-Seiten (dev.epicgames.com, forums.unrealengine.com, issues.unrealengine.com) waren von hier aus **nicht abrufbar** (DNS-Fehler bzw. Proxy-403). Was zu diesen Seiten unten steht, kommt aus **Suchergebnis-Auszügen** und ist mit **[S]** gekennzeichnet. CVar-Namen und Standardwerte habe ich mit der GitHub-Codesuche in Spiegeln des Engine-Quelltexts geprüft, meist **UE 5.6.0**, einige ältere 5.x-Stände. Diese sind mit **[Q5.6]** bzw. **[Q5.x]** markiert. Für **5.8** konnte ich keinen Quelltext prüfen. Was nur aus Drittquellen stammt, steht als **[D]**. **[ungeprüft]** heißt: nirgends sicher belegt, oder es ist meine eigene Schlussfolgerung.

### Kurzfazit

1. **PatchSplit gehört zur Nanite-Tessellation.** Gemeint ist der Compute-Shader `FPatchSplitCS` in `NaniteSplit.usf` [Q5.6]. Er teilt Patches von Meshes mit Displacement auf, bevor gerastert wird. Hängt die GPU dort, liegt das an **Nanite-Tessellation bzw. Displacement**: Megascans-Felsen mit Tessellation und/oder die Nanite-Landschaft mit Displacement. Dass es im **VSM-Schattenpass** passiert, passt zu einem bekannten Epic-Bug: **UE-277458**. Dort lief die GPU in NaniteSplit in einen Timeout, beim Zeichnen von VSM-Schatten für eine Nanite-tessellierte Landschaft. Das betraf 5.5 und gilt seit dem Umbau von PatchSplit in 5.6 als behoben [S]. Ein neuer Fall in 5.8 ist also gut möglich und wäre dann eine **Regression oder ein neuer Grenzfall**.
2. **Schnellste Abhilfe ohne Optikverlust im Hauptbild (neu in 5.8):** `r.Shadow.Virtual.Nanite.AllowTessellationDirectional 0` und `r.Shadow.Virtual.Nanite.AllowTessellationLocal 0` [D: Tom-Looman-Zusammenfassung der 5.8-Release-Notes]. Danach läuft PatchSplit nicht mehr im Schattenpass. Hängt es dann nicht mehr, ist die Ursache eingegrenzt.
3. **Weitere Hebel:** `r.Nanite.DicingRate` hochsetzen (Standard 2 px → 4) [Q5.6], damit weniger Patches entstehen. Async Compute testweise abschalten: `r.Nanite.AsyncRasterization 0`, notfalls `r.RDG.AsyncCompute 0`. Für eine harte Gegenprobe `r.Nanite.Tessellation 0` [Q5.6].
4. **Diagnose:** `-gpucrashdebugging` bzw. `r.GPUCrashDebugging=1` mit Aftermath (NVIDIA), RGD (AMD), DRED (für alle Hersteller). Die „5 s“ stammen aus Unreals eigenem D3D12-Wachhund `r.D3D12.SubmissionTimeout` (Standard 5,0 s) [Q5.6], nicht von Windows-TDR. TDR = 60 s ändert daran nichts, verlängert aber nur das Einfrieren.
5. **Vor allem anderen:** auf den neuesten 5.8-Hotfix gehen (5.8.3 ist erschienen [S]) und den Treiber sauber neu installieren. Bei NVIDIA belegt ein 5.8.2-Fall allerdings, dass ein neuer Treiber allein die Nanite/VSM-Hänger nicht immer behebt [S].

### Befund / Ursachen

**Was im Breadcrumb-Pfad passiert** (Quelltext 5.6 plus Interpretation):
`ShadowDepths → RenderVirtualShadowMaps(Nanite) → Nanite::DrawGeometry → PostPass → PatchSplit` heißt: Im **Nachpass (PostPass)** des zweistufigen Nanite-Occlusion-Cullings für die VSM-Seiten war der PatchSplit-Dispatch noch nicht fertig. Den Displacement-Rahmen gibt `DisplacementScaling.Magnitude` im Material vor. Er wird in die Bounds eingerechnet [D]. Die Unterteilung hängt von der Ziel-Dicing-Rate ab (`r.Nanite.DicingRate`, Pixel pro Mikropolygon) [Q5.6]. Ein Zusammenhang mit `r.Nanite.MaxPixelsPerEdge` wird behauptet (`InvDiceRate = MaxPixelsPerEdge / DicingRate`) [D, ungeprüft].

**Bekannte, belegte Fälle:**

| Fall | Version | Kern | Stand |
|---|---|---|---|
| **UE-277458** | 5.5 | GPU-Timeout in **NaniteSplit** beim Zeichnen von **VSM-Schatten** für **Nanite-tessellierte Landschaft**, mehrere Punktlichter mit Schatten. Callstack unter `RenderVirtualShadowMaps(Nanite)` / `Nanite::DrawGeometry`. Nachstellen: herumfliegen, bis die GPU abstürzt. | Behoben, Ziel 5.6. Verwandte CLs: 37563978 („Nanite patch split auf Multi-Pass umgestellt“) und 37869798 (fehlende Dreiecke, wenn die Kamera zu nah ist) [S] |
| Out-of-bounds-Read im Nanite-Rasterizer (`MicropolyRasterize`, Voxel-Brick-Pfad) | 5.8.0 | Feste Wiederholbarkeit, `DXGI_ERROR_DEVICE_HUNG`. Tritt unabhängig von Hersteller und Treiber auf. | Epic: in **5.8.1** gepatcht (CL 55449171) [S]. Anderer Pass (Raster, nicht PatchSplit) |
| DEVICE_HUNG in Nanite/VSM kurz nach dem Laden der Map | 5.8.2, RTX 4080 SUPER | Aftermath zeigt `NodeAndClusterCull` und VSM-Culling. Treiber 610.60 und 617.14 betroffen. | Offen [S] |
| DEVICE_HUNG bei der VSM-Invalidierung nach Level-Streaming (`Shadow.Virtual.ProcessInvalidationsGPU`) | 5.8.1 | Kein Page Fault in DRED, kein VRAM-Mangel | Offen [S] |
| DynamicWind und GI-Skalierung | 5.8.2, RX 7900 XTX | Hänger bei Nanite-Foliage | Offen [S] |
| Editor friert bei EndDrawingViewport ein | 5.8, RX 9070 XT | Regression gegenüber 5.6, auch ohne Raytracing | Offen [S] |
| Tessellation-Kamera zu nah (mit RVT) | 5.3/5.4 | Treiberabsturz, wenn die Kamera sehr nah an der Displacement-Fläche ist | [S] |
| AsyncCompute + Nanite | 5.6 | Ein Bericht: mit `r.RDG.AsyncCompute=0` war der Absturz weg. Ein anderer: ohne Wirkung. | Uneinheitlich [S] |
| UE-353634 (Nanite) | – | Als „Fixed, Ziel 5.8“ geführt, Inhalt unbekannt | [S, ungeprüft] |

**Mögliche Auslöser in Eldarien** (eigene Ableitung aus den Fällen oben, **[ungeprüft]**):
- **Nanite-Landschaft mit Displacement im VSM:** Das ist fast genau die Lage von UE-277458. Viele VSM-Seiten bzw. Clipmap-Stufen ergeben viele Ansichten, und PatchSplit läuft je Ansicht.
- **Megascans-Felsen mit hoher `DisplacementScaling.Magnitude`:** Große Bounds und viele Patches pro Cluster. Bei Kameraflügen nah an die Oberfläche steigt die Zahl der Unterteilungen stark an (vgl. CL 37869798 und den 5.3/5.4-Fall).
- **Leerlauf, ~100 s nach dem Editorstart:** Passt zeitlich dazu, dass Shader und Materialien fertig kompiliert werden und Nanite nachstreamt. Danach greift Tessellation plötzlich auf viele Objekte gleichzeitig, und die VSM-Seiten werden invalidiert. Dazu kommen DDC/PSO-Effekte.
- **Nicht wiederholbar** (dieselbe Kamera lief beim zweiten Mal): Das spricht für Timing, Async Compute oder Cache-Zustand und gegen einen festen Datenfehler.
- **LumenReflections als Nachbar-Breadcrumb:** Lumen-Arbeit läuft gleichzeitig auf der Async-Compute-Queue. Die Meldung „Compute queue … not completed“ kann auch heißen, dass die Compute-Payload auf die hängende Graphics-Arbeit wartet. **Lumen ist also eher Mitläufer als Ursache [ungeprüft]**. Das klärt sich, wenn man Async Compute abschaltet.

### Sofortmaßnahmen mit CVars und Werten

Vorgehen: erst **in der Konsole testen**, und zwar eine Maßnahme nach der anderen, damit man sieht, welche wirkt. Erst danach dauerhaft in `Config/DefaultEngine.ini` unter `[SystemSettings]` eintragen. In der Konsole ohne `=`, in der ini mit `=`.

```ini
[SystemSettings]
; ---------- Stufe 1: Tessellation aus den Schatten nehmen (UE 5.8) ----------
; Neu in 5.8 [D: Tom Looman / 5.8-Release-Notes]; Standardwert in 5.8 nicht geprüft.
; Kosten: Displacement fehlt nur im VSM-Schatten. Felsen und Landschaft werfen Schatten der
; Basisgeometrie: bei kleiner Magnitude kaum sichtbar, bei großer Abweichung Lichtlecks oder
; Selbstschatten-Fehler an den Rändern. Spart deutlich GPU-Zeit.
r.Shadow.Virtual.Nanite.AllowTessellationDirectional=0
r.Shadow.Virtual.Nanite.AllowTessellationLocal=0

; ---------- Stufe 2: weniger Patches erzeugen ----------
; [Q5.6] Standard 2.0 = Größe der Mikropolygone in Pixeln. 4 = etwa ein Viertel der Mikrodreiecke.
; Kosten: grobere Displacement-Details aus der Nähe. Ab >4 berichten Nutzer sichtbaren Detailverlust [S].
r.Nanite.DicingRate=4
; [Q5.6] Standard 1.0. Gröbere Cluster-LOD für alles in Nanite (beeinflusst Tessellation vermutlich mit, [ungeprüft]).
; Kosten: insgesamt etwas weniger Geometriedetail. Nur einsetzen, wenn Stufe 1+2 nicht reichen.
;r.Nanite.MaxPixelsPerEdge=2

; ---------- Stufe 3: Async Compute als Faktor ausschließen ----------
; [Q5.6] Standard 1. Nanite-Rasterung nicht mehr auf der Async-Queue.
; Kosten: etwas weniger Überlappung, typ. wenige Prozent GPU-Zeit.
r.Nanite.AsyncRasterization=0
; [Q5.6] Standard 0 in 5.6 (in älteren 5.x-Ständen 1). Nur sicherstellen, dass er aus ist.
r.Nanite.AsyncRasterization.ShadowDepths=0
; [Q5.6] Lumen-Async: Standard 1 bzw. Reflections 0. Nur zum Test, falls LumenReflections weiter auftaucht.
;r.Lumen.AsyncCompute=0
; Global: schaltet alle RDG-Async-Compute-Arbeit ab [S, Forum]. Name ist Standard-RenderGraph-CVar,
; in 5.8-Quelltext nicht geprüft. Kosten: spürbar mehr Frame-Zeit (Lumen, TSR, VSM überlappen nicht mehr).
;r.RDG.AsyncCompute=0

; ---------- Stufe 4: harte Gegenprobe (nur Diagnose) ----------
; [Q5.6] Standard 1, zur Laufzeit umschaltbar. 0 = keine Laufzeit-Tessellation, Displacement weg
; (Felsen und Landschaft flach bzw. nur Basisgeometrie). Hängt es damit nie mehr, ist es sicher die Tessellation.
;r.Nanite.Tessellation=0
```

Ergänzend nur in der Konsole bzw. nur zur Diagnose:

```text
; VSM-Cache als Faktor ausschließen [S]. Kosten: VSM wird jedes Frame neu gezeichnet, viel teurer.
r.Shadow.Virtual.Cache 0
; Neu in 5.8 [D]: Budget für Invalidierungen durch Nanite-LOD-Wechsel (Standard: unendlich). Glättet Lastspitzen nach dem Streaming.
r.Shadow.Virtual.DeferredInvalidationBudget <Wert>   ; Einheit/sinnvoller Wert [ungeprüft]
; Puffergrenzen für Patches [Q5.6/Q5.x], Standard je 2*1048576 = 2097152.
; Wirkung auf Hänger [ungeprüft]: kleiner = Patches werden verworfen (Löcher), größer = mehr VRAM.
r.Nanite.MaxCandidatePatches / r.Nanite.MaxVisiblePatches
; [Q5.6] Standard 5 "Maximum number of patches to process per rasterizer group". Nicht anfassen ohne Grund [ungeprüft].
r.Nanite.MaxPatchesPerGroup
; Startparameter (Forum-Vorschlag bei D3D12-Timeouts beim Start) [S]: Residency-Management aus
-dpcvars=D3D12.ResidencyManagement=0
```

**Am Asset statt global** [D, ungeprüft im Detail]:
- Bei den Megascans-Felsen **`DisplacementScaling.Magnitude`** im Material bzw. Material Instance verkleinern: nur so groß wie die echte Höhe der Displacement-Map, nicht als Sicherheitspuffer. Laut Drittquelle nicht animieren, weil der Wert in die Proxy-Bounds eingeht.
- Bei Felsen, die weit weg stehen, die Tessellation im Material abschalten.
- Bei der Landschaft prüfen, ob „Displacement Fade“ an ist. Epic sagt im VSM-Thread: Die Silhouette sollte in der Grundgeometrie stecken, nicht im dynamischen Displacement [S].
- `r.Nanite.AllowTessellation` ist laut Quelltext ein Projektschalter (Standard 0, „highly experimental“) [Q5.x]. Laut einer Drittquelle **gibt es ihn in neueren Versionen nicht mehr** [D, ungeprüft für 5.8]. Nicht als Abhilfe einplanen.

**Editor** [allgemein, ohne Quelle]:
- Viewport **Realtime aus** (Strg+R), wenn man nichts tut.
- Im Hintergrund weniger CPU/GPU verbrauchen lassen: Editor Preferences → Performance → „Use Less CPU when in Background“.
- Erst dann in die Map, wenn alle Shader fertig kompiliert sind (Zähler unten rechts).
- Die Editor-Viewport-Bildschirmauflösung nicht über 100 % setzen.

### Diagnose-Schritte

1. **Version und Treiber festhalten:** Help → About bzw. die Log-Kopfzeile. Bei Bedarf auf den neuesten 5.8.x-Hotfix gehen.
2. **Logs nach dem Hänger:**
   - `<Projekt>/Saved/Logs/<Projekt>.log`. Dort stehen die Zeile `GPU timeout: A payload (…) on the […, Compute] queue has not completed after 5.0 seconds` [Q5.6], die aktiven Breadcrumbs **pro Queue** (Graphics vs. AsyncCompute mit `[Active]`/`[Not Started]`) und gegebenenfalls DRED-Ausgaben.
   - Crash-Ordner: `<Projekt>/Saved/Crashes/<UECC-…>/` mit Log, `CrashContext.runtime-xml`, Minidump und bei NVIDIA `.nv-gpudmp`. Laut Epic wird die Datei aus `Saved/Logs` automatisch dorthin verschoben [S].
3. **Mit GPU-Crash-Debugging starten**, nur zum Testen, weil es etwas Leistung kostet:
   ```text
   UnrealEditor.exe Eldarien.uproject -gpucrashdebugging
   ```
   - `-gpucrashdebugging` schaltet alle Modi ein (Breadcrumbs, Aftermath, DRED) [Q5.x Quelltextkommentar].
   - Einzeln geht es über `-gpubreadcrumbs`, `-nvaftermath`, `-dred` (jeweils `=0` zum Abschalten) [Q5.x]. Epic-Doku nennt `-gpubreadcrumbs` und `-dred` ebenfalls [S].
   - Dauerhaft geht es über `r.GPUCrashDebugging=1` (ReadOnly, also nur per ini oder Startparameter, z. B. in `ConsoleVariables.ini` oder `DefaultEngine.ini [SystemSettings]`) [Q5.x, S].
   - Weitere belegte CVars:
     - `r.GPUCrashDebugging.Breadcrumbs` (Standard 1, ReadOnly) [Q5.x]
     - `r.GPUCrashDebugging.Aftermath.Markers`, `.Callstack`, `.ResourceTracking`, `.TrackAll` [Q5.x]
     - `r.GPUCrashDebugging.Aftermath.DumpShaderDebugInfo` [S]
     - `r.D3D12.DRED` (Standard 0, ReadOnly) und `r.D3D12.LightweightDRED` [Q5.6/Q5.x]
   - **Achtung:** Laut einem Forenbericht schaltet `r.GPUCrashDebugging=1` volles DRED ein, und Aftermath startet dann in manchen Versionen nicht [S]. Falls Aftermath keinen Dump schreibt, `-nvaftermath` allein versuchen.
4. **Shader-Symbole** für lesbare Shader in Aftermath und RGD: `r.Shaders.Symbols=1`. Laut Epic-Antwort ersetzt das `r.DumpShaderDebugInfo=1` [S]. Ablage in `Saved/ShaderSymbols/<Plattform>` [S].
5. **Timing-Probleme eingrenzen:** `-onethread -forcerhibypass` [D] bzw. `-rdgimmediate -onethread -rhivalidation`, Letzteres ein Vorschlag von Epic in einem Async-Compute-Hänger-Thread [S].
   - Kosten: sehr langsam.
   - **Heisenbug-Warnung:** Debug-Modi verändern das Timing. Bleibt der Hänger unter DRED oder Validierung aus, spricht das eher für ein Synchronisations- bzw. Race-Problem als für einen Speicherzugriff außerhalb der Grenzen [D].
6. **`-d3ddebug`** schaltet die D3D12-Debug-Schicht ein (Startparameter im Quelltext belegt [Q5.x]). Sehr langsam. Nur in einer kleinen Test-Map nutzen.
7. **Breadcrumbs lesen:**
   - Pro Queue den tiefsten Eintrag mit `[Active]` suchen. Das ist der Pass, der nicht fertig wurde. Hier ist es `PatchSplit` im `PostPass`.
   - Steht die AsyncCompute-Queue schon in einem späteren Frame bzw. Pass als Graphics, oder umgekehrt, spricht das für eine Abhängigkeit zwischen den Queues [D].
   - Laut UE-273713 fehlen manchen Breadcrumbs bzw. DRED-Einträgen Daten wegen eines Makrofehlers [S]. Den Status für 5.8 habe ich nicht geprüft.
8. **Reproduzieren:** dieselbe Kamerafahrt mehrfach abspielen, nacheinander mit Stufe 1, 2, 3 und 4 aus dem Codeblock. Nur eine Änderung pro Versuch.
9. **Melden:** Epic-Bugreport bzw. Forum mit Log, Breadcrumbs, `.nv-gpudmp`/`.rgd` und Verweis auf UE-277458 als ähnlichen Fall.

### Hinweise je Hersteller

**NVIDIA**
- **Aftermath** ist im Editor über `-gpucrashdebugging` bzw. `-nvaftermath` eingebaut [S]. Den Dump `.nv-gpudmp` in **Nsight Graphics** öffnen (File → Open). Dafür die Shader-Binaries bzw. Symbol-Verzeichnisse eintragen [S, NVIDIA-Doku].
- Bekannter Sonderfall: Hänger **ohne** Aftermath-Dump, zufällige Breadcrumbs und lange Hängezeit. Epic sah das als Erschöpfung des Treiberspeichers durch nicht freigegebene PSOs. Es gibt keinen Workaround, die Hoffnung liegt auf einem Treiber-Update [S].
- **Treiber:**
  - Die Engine führt in `BaseHardware.ini` einen empfohlenen Treiber und eine Sperrliste. Bei schlechten Treibern warnt sie, abschaltbar mit `r.WarnOfBadDrivers=0` (nicht empfohlen) [S].
  - Ein Forenbeitrag empfiehlt für RTX mindestens den Zweig 595.x, wegen Problemen mit überlaufenden Shader-Heaps [S, inoffiziell].
  - Die 5.8.2-Hänger traten auch mit 610.60 und 617.14 auf [S].
  - Empfehlung: aktuellen Studio- oder Game-Ready-Treiber **sauber** installieren (Clean Install). Ein Forenfall wurde dadurch gelöst [S].

**AMD**
- **Radeon GPU Detective (RGD)** [S, GPUOpen]:
  - Voraussetzungen: RDNA2 oder neuer (RX 6000/7000, neuere vermutlich ebenfalls [ungeprüft]), Adrenalin ab 23.7.2, Windows 10/11.
  - Im Radeon Developer Panel unter CAPTURE „Crash Analysis“ einschalten.
  - **TdrLevel muss 3 (Recover)** sein.
  - Optional die PDB-Suchpfade der DXC-Shader eintragen.
  - Der Bericht in Text bzw. JSON enthält den Execution-Marker-Baum und bei Page Faults die Adresse samt betroffener Ressourcen.
  - Ab RGD 1.6.3 werden auch PIX-Marker von D3D12-Anwendungen ausgewertet [S]. Ob UE-Breadcrumbs dort lesbar erscheinen, ist [ungeprüft].
- **Bekannte AMD-Fälle:**
  - 5.8 auf RX 9070 XT: Editor friert ein, Regression gegenüber 5.6 [S].
  - 5.8.2 auf RX 7900 XTX: DynamicWind [S].
  - UE-210759: Nanite-Landschaft mit Displacement auf einer 5700 XT, durch ein Treiber-Update behoben [S].
  - Treiberabsturz bei der PSO-Erstellung von Nanite (UE-204070, 5.3), Workaround `r.SceneCulling=1` [S].
  - Empfehlung: neuestes Adrenalin, und wenn es hängt, eine RGD-Aufnahme.

**Intel (Arc)**
- Ein Herstellerwerkzeug wie Aftermath oder RGD **habe ich nicht gefunden** [ungeprüft]. Also mit herstellerneutralen Mitteln arbeiten: RHI-Breadcrumbs, DRED (`-dred`), `-d3ddebug`.
- Bekannter Fall: UEFN, Arc A750, Nanite-`VisBuffer64`-Allokation scheitert, ein Treiber-Update hilft nicht [S].
- Empfehlung: neuester Arc-Treiber. Bei wiederholbaren Hängern nach Stufe 3/4 testen und an Epic melden.

**Windows TDR (alle Hersteller)**
- Laut Microsoft liegen die Schlüssel unter `HKLM\System\CurrentControlSet\Control\GraphicsDrivers`:
  - `TdrDelay` (Standard 2 s)
  - `TdrDdiDelay` (Standard 5 s)
  - `TdrLevel` (Standard 3 = Recover)
- Microsoft sieht diese Schlüssel **nur für Treiberentwicklung und Tests** vor [S].
- `TdrDelay=60` verhindert keinen echten Hänger. Laut Forenberichten „verzögert es nur den Absturz“ [S], und Unreals eigener 5-s-Wachhund (`r.D3D12.SubmissionTimeout`) meldet ohnehin früher.
- Empfehlung [ungeprüft]: `TdrDelay` auf 10–20 s zurücknehmen, `TdrLevel` auf 3 lassen (sonst laufen RGD und Aftermath nicht richtig), `TdrDdiDelay` nur gemeinsam anheben (z. B. 20).
- `r.D3D12.SubmissionTimeout` hochzusetzen löst nichts. Es verschiebt nur die Warnung [Q5.6; Wirkung über das Log hinaus ungeprüft].

### Risiken

- **Tessellation aus den Schatten nehmen** (Stufe 1): Schatten passen nicht mehr exakt zur sichtbaren Oberfläche. Mögliche Folgen sind Lichtlecks an Felskanten und Selbstschatten-Streifen. Bei großer Magnitude auffälliger. Die Optik nach der Änderung prüfen.
- **`r.Nanite.DicingRate` hoch / `MaxPixelsPerEdge` hoch:** sichtbarer Detailverlust aus der Nähe. Die Werte wirken auf alles im Projekt.
- **Async Compute aus:** höhere Frame-Zeit. Taugt als Diagnose, ist aber kein Dauerzustand.
- **`r.Nanite.Tessellation 0`:** Displacement überall weg. Nur als Gegenprobe gedacht.
- **Debug-Modi** (`-gpucrashdebugging`, DRED, `-d3ddebug`, `-onethread`): Leistung sinkt, das Timing ändert sich, und der Fehler kann dabei verschwinden.
- **Registry/TDR:** systemweite Änderung. `TdrLevel 0` würde Windows-Hänger provozieren.
- **CVar-Gültigkeit in 5.8:** Namen und Standardwerte sind nur gegen den 5.6-Quelltext bzw. eine 5.8-Release-Notes-Zusammenfassung geprüft. Vorher in der Editor-Konsole kontrollieren, ob die Variable existiert und welchen Wert sie hat: `r.Nanite.DicingRate ?` bzw. Name ohne Wert eingeben.
- **Ursache bleibt offen:** Ohne Aftermath- oder RGD-Dump bleibt es eine Indizienkette. Die Ähnlichkeit zu UE-277458 ist stark, aber kein Beweis.

### Quellen

Epic Issue-Tracker und Forum (nur über Suchergebnis-Auszüge, Seiten nicht direkt abrufbar):
- [UE-277458 – GPU-Timeout in NaniteSplit, VSM, Nanite-tessellierte Landschaft](https://issues.unrealengine.com/issue/UE-277458)
- [UE-273240 – Log-Beispiel „GPU timeout … has not completed“](https://issues.unrealengine.com/issue/UE-273240)
- [UE-273713 – fehlende Daten in Breadcrumbs/DRED](https://issues.unrealengine.com/issue/UE-273713)
- [UE-353634 – Nanite, Fixed 5.8 (Inhalt unbekannt)](https://issues.unrealengine.com/issue/UE-353634)
- [UE-210759 – Nanite-Landschaft mit Displacement, 5700 XT](https://issues.unrealengine.com/issue/UE-210759)
- [UE-204070 – AMD-Treiberhänger bei Nanite-PSO](https://issues.unrealengine.com/issue/UE-204070)
- [Forum: OOB-Read im Nanite-Rasterizer, Fix 5.8.1](https://forums.unrealengine.com/t/potential-gpu-crash-in-nanite-voxel-brick-rasterizer-out-of-bounds-groupshared-read-in-micropolyrasterize-naniterasterizer-usf-gpu-device-hung-lds-0xd74/2753987)
- [Forum: 5.8.2 DEVICE_HUNG Nanite/VSM, RTX 4080 SUPER](https://forums.unrealengine.com/t/ue-5-8-2-dx12-repeated-device-hung-crashes-in-nanite-vsm-shortly-after-map-load-on-rtx-4080-super/2836649)
- [Forum: 5.8.1 DEVICE_HUNG bei VSM-Invalidierung](https://forums.unrealengine.com/t/ue-5-8-1-d3d12-gpu-device-hung-during-virtual-shadow-map-invalidation-after-level-streaming/2742850)
- [Forum: 5.8.2 DynamicWind DEVICE_HUNG](https://forums.unrealengine.com/t/ue-5-8-2-dynamicwind-gpu-device-hung-when-changing-gi-scalability-with-a-dynamicwind-transform-provider-active/2765281)
- [Forum: 5.8 Editor-Freeze RX 9070 XT](https://forums.unrealengine.com/t/ue-5-8-dx12-editor-hard-freezes-at-enddrawingviewport-slate-on-rx-9070-xt-regression-from-5-6/2735270)
- [Forum: GPU Crash 5.6 AsyncCompute & Nanite](https://forums.unrealengine.com/t/gpu-crash-in-ue5-6-related-to-asynccompute-nanite/2664549)
- [Forum: GPU Hang on AsyncCompute TexturePoolCopyOps (-rdgimmediate -onethread -rhivalidation)](https://forums.unrealengine.com/t/gpu-hang-on-asynccompute-texturepoolcopyops/2743119)
- [Forum: Random GPU crashes/timeouts D3D12 (ResidencyManagement)](https://forums.unrealengine.com/t/random-gpu-crashes-and-timeouts-on-windows-with-d3d12-mostly-on-app-startup/2734981?page=2)
- [Forum: GPU crashes w/o Aftermath dumps](https://forums.unrealengine.com/t/gpu-crashes-w-o-aftermath-dumps-follow-up/2744946)
- [Forum: Aftermath dumps in cooked builds (r.Shaders.Symbols)](https://forums.unrealengine.com/t/aftermath-gpu-crash-hang-dumps-failing-on-standalone-cooked-builds/2738007)
- [Forum: Trouble getting Aftermath flow working (Dump-Pfade)](https://forums.unrealengine.com/t/trouble-getting-aftermath-flow-working-to-debug-gpu-crashes/2727921)
- [Forum: Aftermath documentation is misleading (DRED/Aftermath-Konflikt)](https://forums.unrealengine.com/t/aftermath-documentation-is-misleading/2678916)
- [Forum: Best practices GPU crash debugging live](https://forums.unrealengine.com/t/best-practices-for-gpu-crash-debugging-in-a-live-environment/2833500)
- [Forum: Nanite Tessellation – Dicing (DicingRate)](https://forums.unrealengine.com/t/nanite-tessellation-dicing-disable-distance/2623536)
- [Forum: VSM-Naht an Clip-Grenzen bei Displacement (Displacement Fade)](https://forums.unrealengine.com/t/sporadic-seam-along-boundary-between-2-vsm-clip-levels/2726896)
- [Forum: 5.3/5.4 Displacement-Crash, Kamera zu nah](https://forums.unrealengine.com/t/5-3-and-5-4-displacement-tessellation-crash-using-rvt-if-camera-too-close/1792531)
- [Forum: Treiberempfehlung für UE](https://forums.unrealengine.com/t/recommendation-gpu-driver-version-for-unreal-engine/2737752)
- [Forum: UEFN Nanite VisBuffer64 auf Arc A750](https://forums.unrealengine.com/t/uefn-crash-nanite-visbuffer64-on-intel-arc-a750/2836629)
- [Forum: 5.8.3 Hotfix](https://forums.unrealengine.com/t/5-8-3-hotfix-released/2833315)

Epic-Doku (nur über Suchergebnis-Auszüge):
- [Epic: Dealing with a GPU Crash](https://dev.epicgames.com/documentation/en-us/unreal-engine/dealing-with-a-gpu-crash-when-using-unreal-engine)
- [Epic: NVIDIA Nsight Aftermath in UE](https://dev.epicgames.com/documentation/en-us/unreal-engine/nvidia-nsight-aftermath-for-gpu-pipeline-debugging-in-unreal-engine)
- [Epic: UE 5.8 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes)
- [Epic: Using Nanite with Landscapes](https://dev.epicgames.com/documentation/unreal-engine/using-nanite-with-landscapes-in-unreal-engine)

Drittquellen:
- [Tom Looman: UE 5.8 Performance Highlights (VSM-Tessellation-CVars, DeferredInvalidationBudget)](https://tomlooman.com/unreal-engine-5-8-performance-highlights/)

Quelltext (inoffizielle Spiegel, nicht verlinkt; Original im zugangsbeschränkten Repo `EpicGames/UnrealEngine`):
- UE 5.6.0 `NaniteCullRaster.cpp` / `NaniteShared.cpp` / `D3D12Submission.cpp` / `D3D12Adapter.cpp` / `Lumen*.cpp`
- älterer 5.x-Stand `RHI.cpp` / `D3D12Adapter.cpp` / `NaniteResources.cpp`

NVIDIA, AMD, Microsoft:
- [NVIDIA: Nsight Aftermath – GPU Crash Dumps einrichten](https://docs.nvidia.com/nsight-aftermath/UserGuide/gpu-crash-dump-setting-up.html)
- [NVIDIA: Aftermath – Debugging Crashes and TDRs](https://developer.nvidia.com/aftermath-debugging-crashes-and-tdrs-gpu)
- [AMD GPUOpen: RGD 1.0 Tutorial](https://gpuopen.com/learn/rgd_1_0_tutorial/)
- [AMD RGD Handbuch](https://radeon-gpu-detective.readthedocs.io/en/latest/help_manual.html)
- [AMD GPUOpen: Tool-Suite-Update (PIX-Marker in RGD 1.6.3)](https://gpuopen.com/learn/radeon-developer-tool-suite-shader-source-code/)
- [Microsoft: TDR registry keys](https://learn.microsoft.com/en-us/windows-hardware/drivers/display/tdr-registry-keys)
- [Microsoft: Use DRED](https://learn.microsoft.com/en-us/windows/win32/direct3d12/use-dred)


## Teil C – Veraltete VSM-Cache-Kacheln

> Arbeitsbedingung: Alle Epic-Domains (dev.epicgames.com, forums.unrealengine.com, issues.unrealengine.com, unrealengine.com) waren für WebFetch und curl gesperrt (DNS-Fehler bzw. Proxy-403). Aussagen zu diesen Seiten stützen sich daher auf **Suchergebnis-Auszüge**. Sie sind mit **[S]** markiert. CVar-Namen und Standardwerte wurden zusätzlich per GitHub-Codesuche in öffentlich gespiegeltem Engine-Quelltext (Stand etwa 5.4/5.5) abgeglichen und mit **[Q]** markiert. Diese Spiegel werden aus Lizenzgründen nicht verlinkt. Das Original liegt im zugangsbeschränkten Repo `EpicGames/UnrealEngine`. Für 5.8 ist **nichts davon geprüft**: Im Editor sollte jeder Name einmal mit `help <CVar>` bzw. `<CVar> ?` bestätigt werden.

### Kurzfazit

- **Das Muster ist bekannt.** Ein Fall „World-Partition-Ladevorgang → scharfkantige dunkle Rechtecke → verschwinden nach VSM aus/an“ ist zwar nicht wörtlich dokumentiert. Epic führt aber mehrere offene bzw. verwandte Bugs, bei denen VSM-Seiten nach einem Wechsel der Geometrie **nicht invalidiert** werden. Am nächsten kommt UE-215659: HLOD ersetzt Meshes, die Seiten werden nicht invalidiert. Der Bug ist „Unresolved“ mit Ziel 5.8 [S]. Die Rechteckform passt zu VSM-Seiten (128×128 Texel je Seite [Q]). Dunkel heißt hier: Ein veralteter Schattenwerfer steckt noch im Cache, etwa ein HLOD-Proxy, ein Nicht-Nanite-Fallback der Landschaft oder Foliage vor dem Nachladen.
- **Einen dokumentierten Befehl, der nur den Cache leert, gibt es nicht.** Belegt ist `r.Shadow.Virtual.Cache 0`, was laut Epic-Doku das Caching „zum Debuggen“ abschaltet [S][Q]. Das praktische Vorgehen ist: `r.Shadow.Virtual.Cache 0`, ein paar Frames rendern lassen, Aufnahme machen, `r.Shadow.Virtual.Cache 1`. Der VSM-Pool bleibt dabei bestehen, anders als bei `r.Shadow.Virtual.Enable 0/1`.
- **Gezielter, nur für das Richtungslicht:** `r.Shadow.Virtual.Cache.ForceInvalidateDirectional 1` [Q][S].
- **Ein Editor-Artefakt ist es nicht zwingend.** Das Invalidieren beim Hinzufügen und Entfernen von Primitiven gilt in PIE und im Paket genauso. Die genannten Bugs (HLOD-Wechsel, Nanite-Landschaft fällt beim teilweisen Laden auf Nicht-Nanite zurück) betreffen ausdrücklich Streaming-Situationen. Im Paket hilft nur, die Ursache abzustellen. Ein Cache-Reset per CVar ist dort kein brauchbarer Dauerzustand.
- **Für reproduzierbare Screenshots** sollte `r.Shadow.Virtual.Cache 0` nur während der Aufnahme gelten. Für ein Standbild kostet das praktisch nichts. Dabei auf Pool-Überlauf achten (Logwarnung, s. Risiken).

### Befund

**Was der Cache tut.** VSM rendert nur Seiten neu, deren Inhalt ungültig ist. Laut Doku invalidieren Lichtbewegungen alle Seiten des Lichts. Bewegte, hinzugefügte oder entfernte Schattenwerfer invalidieren die Seiten, die ihre Bounds überlappen. WPO-, PDO- und Skelett-Geometrie invalidiert jeden Frame [S].

Intern (Quelltext-Notizen [Q]) markiert der Cache-Manager „Removed“, „Added“ und „UpdatedTransform“ jeweils vor und nach dem GPU-Scene-Update in den Request-Flags des **letzten** Frames. Er nutzt dabei standardmäßig die HZB (`r.Shadow.Virtual.Cache.InvalidateUseHZB=1`). Nicht angefragte Seiten bleiben bis zu `r.Shadow.Virtual.Cache.MaxPageAgeSinceLastRequest` = 1000 Frames im Pool. Ein Fehler in dieser Kette, etwa ein Wechsel ohne „Remove/Add“-Ereignis oder eine durch die HZB weggecullte Invalidierung, lässt alte Tiefen in der Seite stehen. Das ergibt scharfe Kanten an Seitengrenzen, je Mip/Clipmap-Stufe versetzt, also treppenartig.

**Bekannte, passende oder verwandte Fälle:**

| Fall | Version | Status | Bezug zum Befund |
|---|---|---|---|
| UE-215659 – „VSM do not invalidate pages when HLODs replace meshes“. Schattenlücken bleiben, bis die Kamera weg- und zurückgedreht wird | betrifft 5.4 | Unresolved, Ziel 5.8 [S] | **hoch**: WP-Laden im Editor schaltet zwischen HLOD-Proxy und echten Actors um |
| UE-352957 – Landschaftssplines in WP-Levels lassen Nanite-Landschafts-Proxys invalidieren und auf **Nicht-Nanite** zurückfallen, „nur wenn ein WP-Level teilweise geladen ist“ | k. A. | Status ungeprüft [S] | **mittel/hoch**: teilweises Laden per LocationVolume = genau dieser Zustand |
| Forum „World Partition – wrongly lit patches“: falsch beleuchtete Flecken = veraltete HLOD-Proxys. Test `r.HLOD 0`, Abhilfe *Build > Build HLODs*, sonst Nanite-Daten der Landschaft neu bauen | k. A. | Community-Rat [S] | **hoch**: schnelle Gegenprobe |
| UE-219540 – Geometrie mit „Static“-Invalidierungsverhalten zeichnet bei WPO trotzdem in den dynamischen Cache | k. A. | Status ungeprüft [S] | mittel (Foliage mit WPO) |
| UE-328823 – Nanite-Skeletal-Meshes ignorieren „Rigid“ und invalidieren immer | 5.6/5.6.1 | Ziel 5.8 [S] | gering (Megaplants/PVE, s. Forum 5.8) |
| UE-217513 – `r.Shadow.Virtual.Cache.DrawInvalidatingBounds` zeigt seit 5.4 nichts mehr (Code entfernt) | 5.4 | Fixed, Ziel 5.7 [S] | Debug-Werkzeug, s. CVars |
| Forum „VSM“ (2025): Artefakte bei Partikeln/WPO. Früherer Workaround `r.Shadow.Virtual.Cache.StaticSeparate 0` ist „in 5.6 deprecated“, `ForceInvalidateDirectional 1` half dort nicht | 5.6 | offen [S] | zeigt: StaticSeparate als Workaround ab 5.6 unsicher |
| Forum 5.7: `r.Shadow.Virtual.UseReceiverMaskDirectional` jetzt Standard 1, dynamische Seiten werden jeden Frame „uncached“, statische bleiben gecacht | 5.7 | by design [S] | Hinweis: Fehler sitzen in 5.7+ eher in **statischen** Seiten (Landschaft, statische Foliage) |
| Forum 5.8.1: GPU DEVICE_HUNG in `Shadow.Virtual.ProcessInvalidationsGPU` nach Level-Streaming (Paket, D3D12) | 5.8.1 | offen [S] | zeigt, dass die Streaming-Invalidierung in 5.8 ein aktiver Problembereich ist |
| Polycount 5.3.2: Artefakte nur mit **Nanite-Landschaft** + VSM, im Takt der VSM-Mips | 5.3 | ohne Fix [S] | mittel |

**Bewertung für Eldarien (Hypothese, ungeprüft):** Am wahrscheinlichsten ist ein Geometriewechsel ohne passende Invalidierung beim WP-Laden: HLOD-Proxy gegen Actor, Nanite-Landschaft gegen Fallback oder Foliage-HISM-Austausch. Die dunklen Flecken wären dann alte Schattentiefen eines Proxys oder Fallbacks. Gegenproben in dieser Reihenfolge:

1. `r.HLOD 0` vor dem Laden. Verschwinden die Flecken, ist HLOD die Ursache, passend zu UE-215659.
2. Im Viewport *Visualisieren > Virtual Shadow Map > Cached Page* aufrufen und beobachten, ob die Fleckenregion grün bleibt (gecacht), obwohl sich die Geometrie geändert hat.
3. Prüfen, ob Landschaftssplines im geladenen Bereich liegen (UE-352957).

### CVars/Befehle mit Werten

```ini
; --- Cache an/aus (belegt: Epic-Doku [S] + Quelltext [Q]) ---
r.Shadow.Virtual.Cache 1                               ; Standard. 0 = Caching aus, jede benötigte Seite wird jeden Frame neu gerendert ("for debugging")
r.Shadow.Virtual.Enable 1                              ; 0/1 = VSM komplett aus/an (baut auch den Pool neu auf; schwerer als nötig)

; --- gezielte Invalidierung (belegt [Q]; Wirkung bei diesem Bug ungeprüft) ---
r.Shadow.Virtual.Cache.ForceInvalidateDirectional 0    ; 1 = Richtungslicht-VSM jeden Frame komplett invalidieren (Fortnite-Blog/Forum [S])
r.Shadow.Virtual.Cache.ForceInvalidateLocal 0          ; 1 = lokale Lichter jeden Frame invalidieren ("generally only used for debugging") [ungeprüft, Name nur aus Suchtreffern]
r.Shadow.Virtual.Cache.InvalidateUseHZB 1              ; 0 = Invalidierung ohne HZB-Occlusion-Culling (konservativer; als Test sinnvoll, ungeprüft ob es den Bug behebt)
r.Shadow.Virtual.Cache.DeformableMeshesInvalidate 1    ; [Q laut Drittnotizen]
r.Shadow.Virtual.Cache.MaxPageAgeSinceLastRequest 1000 ; Frames, die nicht angefragte Seiten im Pool bleiben; 0 = deaktiviert [Q]
r.Shadow.Virtual.Cache.AllocateViaLRU 1                ; [Q]

; --- statisch/dynamisch getrennter Cache ---
r.Shadow.Virtual.Cache.StaticSeparate 1                ; [Q] Standard 1; laut Forum ab 5.6 "deprecated" [S] -> in 5.8 evtl. wirkungslos/entfernt (UNGEPRÜFT)
r.Shadow.Virtual.Cache.StaticSeparate.FramesStaticThreshold 100  ; [Q] Frames ohne Invalidierung bis "statisch"

; --- WPO-bezogen ---
r.Shadow.Virtual.Cache.MaxMaterialPositionInvalidationRange -1   ; cm; jenseits davon werden WPO/PDO-Invalidierungen ignoriert (Epic-Optimierungsdoku, über Drittnotizen [S]; Standardwert UNGEPRÜFT)
r.Shadow.Virtual.Clipmap.WPODisableDistance.LodBias <n>          ; existiert laut Epic-Vortrag (Drittnotiz) [S]; Standard ungeprüft

; --- Pool / Überlauf (Differenzialdiagnose) ---
r.Shadow.Virtual.MaxPhysicalPages 2048                 ; [Q] Standard (Projekt-/Scalability-Werte können abweichen)
; Logwarnung bei Überlauf [Q]: "Virtual Shadow Map Page Pool overflow (... page allocations were not served), this will produce visual artifacts (missing shadow)"

; --- Debug/Visualisierung ---
r.Shadow.Virtual.Visualize cache                       ; Modus "Cached Page": grün = gecacht, rot = neu/invalidiert, blau = nur statisch gecacht [Q: Beschreibung];
                                                        ; Modusname "cache" UNGEPRÜFT -> alternativ Viewport: Visualisieren > Virtual Shadow Map > Cached Page
r.Shadow.Virtual.Visualize.Advanced 1                  ; erweiterte Modi im Menü [Q]
r.ShaderPrintEnable 1
r.Shadow.Virtual.ShowStats 2                           ; Seiten-/Invalidierungsstatistik am Bildschirm [S, Epic-Vortrag über Drittnotiz]
stat VirtualShadowMapCache                             ; [S, Drittquelle] UNGEPRÜFT
r.Shadow.Virtual.Cache.DrawInvalidatingBounds 1        ; in 5.4 wirkungslos (UE-217513), laut Tracker in 5.7 gefixt [S]; in 5.8 testen
r.HLOD 0                                               ; Gegenprobe HLOD-Proxys (Forum [S])

; --- NICHT belegt (in keiner Quelle/keinem Quelltexttreffer gefunden) ---
; r.Shadow.Virtual.Cache.Invalidate / ...InvalidateAll / ResetCache  -> existieren nach heutigem Stand NICHT als Befehl (nicht gefunden)
; r.Shadow.Virtual.Cache.SkinnedMeshUpdateFrequency                 -> nur in Drittblog, nicht belegt
```

**Einmaliges Leeren aus Editor-Python vor HighResShot.** Ein Toggle `0 → 1` im **selben** Python-Aufruf bewirkt nichts, weil der Editor während der Skriptausführung nicht tickt (vgl. `recherche/antworten/pie-test-python-gasp.md`, Tick-Zustandsautomat). Deshalb verteilt das Snippet die Schritte über einen Slate-Post-Tick-Callback. Frame-Zahlen sind Erfahrungswerte (ungeprüft). Der Viewport muss auf „Echtzeit“ stehen.

```python
import unreal

WARM_FRAMES = 8          # Frames mit Cache aus, bevor aufgenommen wird
SHOT_CMD = "HighResShot 1920x1080"
AFTER_FRAMES = 15        # Frames nach dem Shot, bevor der Cache wieder an geht

_world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
_st = {"n": 0, "h": None}

def _cmd(c):
    unreal.SystemLibrary.execute_console_command(_world, c)

def _tick(_dt):
    _st["n"] += 1
    n = _st["n"]
    if n == 1:
        _cmd("r.Shadow.Virtual.Cache 0")          # alle Seiten neu rendern
    elif n == 1 + WARM_FRAMES:
        _cmd(SHOT_CMD)                            # Aufnahme mit frisch gerenderten Schatten
    elif n == 1 + WARM_FRAMES + AFTER_FRAMES:
        _cmd("r.Shadow.Virtual.Cache 1")          # Cache wieder an (startet leer/frisch)
        unreal.unregister_slate_post_tick_callback(_st["h"])

_st["h"] = unreal.register_slate_post_tick_callback(_tick)
```

Variante: Statt `Cache 0` das Paar `r.Shadow.Virtual.Cache.ForceInvalidateDirectional 1` / `0` verwenden. Das trifft nur die Sonne und lässt lokale Lichter gecacht. Ob das für die Bodenflecken reicht, ist ungeprüft. Im Forumsfall half es nicht [S].

### PIE/Paket: Vorbeugung

- **Tritt es dort auf?** Das ist plausibel und nicht ausgeschlossen. Die Invalidierungslogik ist dieselbe, und UE-215659 (HLOD-Wechsel) sowie UE-352957 (teilweise geladenes WP) sind Streaming-Fälle, die zur Laufzeit genauso vorkommen. Ein eigener PIE/Paket-Test für Eldarien steht aus. Prüfen: mit HLODs in PIE an die Grenze laufen und *Cached Page* beobachten.
- **HLODs aktuell halten:** *Build > Build HLODs* nach jeder Änderung an Landschaft und Foliage. Veraltete Proxys sind ein bekannter Fleckenverursacher [S]. Solange UE-215659 offen ist, gilt: HLOD-Übergangsdistanz nicht in typische Screenshot- oder Spielerdistanzen legen.
- **Nanite-Landschaft:** Nanite-Daten nach Änderungen neu bauen (*Build > Build Nanite Landscape* bzw. Landscape-Details, Menüname je nach Version ungeprüft). Splines im Blick behalten (UE-352957). Bei bleibenden Problemen Nanite-Landschaft testweise aus.
- **Shadow Cache Invalidation Behavior je Komponente** (`EShadowCacheInvalidationBehavior`, Python `unreal.ShadowCacheInvalidationBehavior`: AUTO=0, ALWAYS=1, RIGID=2, STATIC=3) [S]:
  - *Auto* (Standard): invalidiert bei WPO und Transform-Änderung.
  - *Always*: jeden Frame. Nur für Animationen, die das System nicht erkennt.
  - *Rigid*: unterdrückt WPO-Invalidierung. Für Foliage mit schwachem Wind die übliche Kostensenkung, „use with care“.
  - *Static*: zusätzlich keine Transform-Invalidierung. Add/Remove invalidiert weiterhin. Bewegt sich das Objekt doch, ist das Ergebnis undefiniert.
  - **Folge für diesen Befund:** Diese Einstellungen verhindern veraltete Kacheln nicht, sie können sie sogar erzeugen (Rigid/Static plus Bewegung oder WPO ergibt sichtbar veraltete Schatten). Gegen Streaming-Flecken also nicht auf *Static* stellen, sondern *Auto* lassen. Rigid nur für Foliage-WPO als Performance-Maßnahme einsetzen.
- **Mobility:** Was sich zur Laufzeit nie bewegt, sollte *Static* sein. Bewegliche Actors, die sich nie bewegen, invalidieren laut Forum dennoch laufend [S].
- **WPO/Foliage:** Für Foliage-Typen „World Position Offset Disable Distance“ setzen (Komponenten-Property, seit 5.1), ab dieser Distanz läuft wieder statisches Caching. Wo kein Wind nötig ist, „Evaluate World Position Offset“ aus. Beide Property-Namen stammen aus der Doku bzw. Vorträgen über Drittquellen und sind in 5.8 ungeprüft. Ergänzend `r.Shadow.Virtual.Cache.MaxMaterialPositionInvalidationRange` (cm) und `r.Shadow.Virtual.Clipmap.WPODisableDistance.LodBias` (2–4 laut Epic-Vortrag gegen „halber Schatten animiert“) [S].
- **Pool groß genug:** Im Log auf „Virtual Shadow Map Page Pool overflow“ achten und bei Bedarf `r.Shadow.Virtual.MaxPhysicalPages` erhöhen [Q].
- **Engine-Stand:** Mehrere Tickets haben Ziel 5.8 (UE-215659, UE-328823). Ob sie in 5.8.x tatsächlich gefixt sind, ließ sich nicht prüfen, weil der Tracker gesperrt war. Release Notes 5.8.x gezielt nach „Virtual Shadow“ und „HLOD“ durchsuchen.

### Risiken

- `r.Shadow.Virtual.Cache 0` dauerhaft bedeutet: Alle Seiten werden jeden Frame gerendert, mit deutlichen GPU-Kosten in offenen Welten. Nur für Aufnahmen verwenden und **nie** in `DefaultEngine.ini` bzw. Device Profiles fürs Paket eintragen.
- Bei HighResShot mit großem Faktor und `Cache 0` werden in einem Frame sehr viele Seiten angefordert. Das kann den Pool überlaufen lassen und **fehlende** (helle) Schatten erzeugen. Im Log prüfen und gegebenenfalls `MaxPhysicalPages` nur für die Aufnahme erhöhen.
- `ForceInvalidateDirectional` / `ForceInvalidateLocal` sind Debug-Schalter und gehören nicht ins Spiel.
- `StaticSeparate 0` als Workaround ist ab 5.6 laut Forum deprecated. Auf 5.8 nicht darauf bauen.
- Rigid/Static an Komponenten erzeugt selbst veraltete Schatten, wenn sich das Objekt doch verändert (laut Doku „undefined“).
- Ein Cache-Reset kaschiert die Ursache nur. Für das Spiel zählt HLOD-, Nanite- und Spline-Hygiene.
- Quellenlage: Epic-Seiten waren nur als Suchauszüge verfügbar, Quelltextabgleich nur gegen 5.4/5.5-Spiegel. Namen und Defaults in 5.8 deshalb im Editor mit `help <CVar>` bestätigen.

### Quellen

- [Epic-Doku: Virtual Shadow Maps in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine) [S]
- [Epic API: EShadowCacheInvalidationBehavior](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/EShadowCacheInvalidationBehavior) [S]
- [Epic Python-API: ShadowCacheInvalidationBehavior](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShadowCacheInvalidationBehavior) [S]
- [Epic Tech-Blog: Virtual Shadow Maps in Fortnite Battle Royale Chapter 4](https://www.unrealengine.com/en-US/tech-blog/virtual-shadow-maps-in-fortnite-battle-royale-chapter-4) [S]
- [UE-215659 – VSM invalidiert nicht bei HLOD-Wechsel](https://issues.unrealengine.com/issue/UE-215659) [S]
- [UE-352957 – Nanite-Landschafts-Proxys fallen bei teilweise geladenem WP zurück](https://issues.unrealengine.com/issue/UE-352957) [S]
- [UE-219540 – „Static“ zeichnet bei WPO in dynamischen Cache](https://issues.unrealengine.com/issue/UE-219540) [S]
- [UE-328823 – Nanite Skeletal Meshes ignorieren Rigid](https://issues.unrealengine.com/issue/UE-328823) [S]
- [UE-217513 – DrawInvalidatingBounds ohne Funktion (5.4), gefixt 5.7](https://issues.unrealengine.com/issue/UE-217513) [S]
- [Forum: World Partition – wrongly lit patches](https://forums.unrealengine.com/t/world-partition-wrongly-lit-patches/2746672/2) [S]
- [Forum: VSM (StaticSeparate deprecated 5.6, ForceInvalidateDirectional)](https://forums.unrealengine.com/t/vsm/2670676) [S]
- [Forum: Constant invalidation of VSM dynamic shadows in 5.7.0](https://forums.unrealengine.com/t/constant-invalidation-of-vsm-dynamic-shadows-in-5-7-0/2686534/3) [S]
- [Forum: VSM Shadow Cache Invalidation Behaviour and Separate Static Caching in UE5.4](https://forums.unrealengine.com/t/vsm-shadow-cache-invalidation-behaviour-and-separate-static-caching-in-ue5-4/1927473) [S]
- [Forum: Movable actors that never move are invalidating your VSM cache every frame](https://forums.unrealengine.com/t/movable-actors-that-never-move-are-invalidating-your-virtual-shadow-map-cache-every-frame/2747014) [S]
- [Forum: UE5.8 Procedural Vegetation/Megaplants Shadow Cache Invalidation](https://forums.unrealengine.com/t/ue5-8-procedural-vegetation-megaplants-shadow-cache-invalidation/2835995) [S]
- [Forum: UE 5.8.1 D3D12 DEVICE_HUNG during VSM invalidation after level streaming](https://forums.unrealengine.com/t/ue-5-8-1-d3d12-gpu-device-hung-during-virtual-shadow-map-invalidation-after-level-streaming/2742850) [S]
- [Polycount: Nanite-Landschaft + VSM-Artefakte (5.3.2)](https://polycount.com/discussion/comment/2794118) [S]
- [Drittquelle: VSM Optimization for Open Worlds in UE5.7 (StraySpark)](https://www.strayspark.studio/blog/virtual-shadow-map-optimization-open-worlds-ue5-7) – nicht autoritativ
- [Drittquelle: PerfGuard – VSM Performance & Tuning](https://getperfguard.com/tutorials/virtual-shadow-maps) – nicht autoritativ
- Quelltextabgleich [Q]: `Engine/Source/Runtime/Renderer/Private/VirtualShadowMaps/VirtualShadowMapCacheManager.cpp`, `VirtualShadowMapArray.cpp`, `Engine/Private/VirtualShadowMapVisualizationData.cpp` (über GitHub-Codesuche in Drittspiegeln. Original: `EpicGames/UnrealEngine`, Zugang über verknüpften Epic-Account)

