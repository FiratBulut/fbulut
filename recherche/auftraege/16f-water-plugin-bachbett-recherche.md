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

## Nachtrag 22:55 – Ferat: „auch andere Plugins von der UE-Engine recherchieren“
Bitte zusätzlich bewerten, welche **Engine-Plugins von UE 5.8** uns für Witcher-Qualität helfen (Gelände, Flüsse/Seen, Bewuchs, Felsen, Wind,
Streaming großer Welten) – Reife in 5.8, bekannte Probleme mit World Partition/großen Landschaften, ob Epic/CDPR sie in der Witcher-4-Demo oder in
Samples (Electric Dreams, PCG Biome Sample, City Sample …) einsetzen, und eine **Empfehlung je Plugin** (einschalten ja/nein, wofür, Risiko, Aufwand).
Besonders: Mesh Partition + Mesh Terrain Mode (+ Mesh Partition Water), Landscape Patch, Landmass, PCG Biome Core/Sample, PCG Primitives,
PCG Water/Niagara/Nanite-Assemblies-Interop, Procedural Vegetation Editor (bei uns AN), Dynamic Wind (Nanite-Foliage), Nanite Assemblies,
Nanite Displaced Mesh, FastGeo Streaming (+ PCG FastGeo Interop), Volumetrics, Niagara Fluids (bei uns AN; Wasserfälle?), Buoyancy.
Liste aus unserer Installation (Ordner, Plugin, Reife, Status bei uns, Engine-Beschreibung; Filter Gelände/Wasser/Bewuchs/PCG/Nanite/…):

| Ordner | Plugin | Name | Reife | bei uns | Beschreibung (Engine) |
|---|---|---|---|---|---|
| DataflowVolumetricPlugin | DataflowVolumetricPlugin | DataflowVolumetric |  | aus | Adds volumetric support to Dataflow |
| Developer | OneSkyLocalizationService | OneSky | Beta | aus | OneSky localization service |
| Editor | GeometryMode | GeometryMode |  | an (Standard) | Geometry and BSP editing |
| Editor | LandscapePatch | Landscape Patch |  | aus | Support for adding landscape patches- components that can be attached to meshes to affect the landscape as the mesh is repositioned. |
| Editor | SpeedTreeImporter | SpeedTree Importer |  | an (Standard) | An importer for SpeedTree runtime files. |
| Editor | WorldPartitionHLODUtilities | World Partition HLOD Utilities |  | an (Standard) | Editor utility classes & HLOD layer asset types |
| Enterprise | LidarPointCloud | LiDAR Point Cloud Support |  | aus | Adds support for importing, processing and rendering of LiDAR Point Clouds. |
| Experimental | Buoyancy | Buoyancy | Exp | aus | Set of tools for adding buoyant behavior to objects which interact with water bodies generated by the Water plugin |
| Experimental | ChaosNiagara | Chaos Niagara | Beta | an (Standard) | Import destruction data from Chaos into Niagara to generate secondary destruction effects. |
| Experimental | CommonConversation | Common Conversation | Exp | aus | An *experimental* plugin for authoring graph-based conversation trees |
| Experimental | DataprepGeometryOperations | Dataprep Geometry Operations | Beta | aus | Experimental geometry processing operations usable in the Dataprep Editor. |
| Experimental | DynamicWind | Dynamic Wind | Exp | aus | Extremely experimental dynamic wind support for Nanite foliage. |
| Experimental | FastGeoStreaming | FastGeo Streaming | Exp | aus | A system that extracts and converts a partitioned world's geometry to optimize world streaming performance. |
| Experimental | GeometryCacheAbcFile | Geometry Cache from Alembic File(Experimental) | Beta | aus | Support Geometry Cache from Alembic file without importing |
| Experimental | GeometryCacheLevelSequenceBaker | GeometryCacheLevelSequenceBaker | Exp | aus | Bake Skeletal Meshes in Level Sequence to Geometry Cache |
| Experimental | GeometryCollectionPlugin | Geometry | Beta | aus | Adds Geometry Collection Container. |
| Experimental | GeometryDataflow | Geometry Dataflow Nodes |  | aus | Geometry Processing in Dataflow. |
| Experimental | GeometryFlow | GeometryFlow | Exp | aus | Geometry DataFlow Graph |
| Experimental | HairCardGenerator | Hair Card Generator | Exp | aus | Procedurally generate hair cards from hair strands |
| Experimental | Landmass | Landmass | Beta | aus |  |
| Experimental | Locomotor | Locomotor | Exp | AN | Procedural animation for Control Rig. |
| Experimental | MeshPartition | Mesh Partition | Exp | aus | Large-scale mesh authoring system through spatial partitioning, non-destructive modifier editing, and platform-adaptive runtime representations. |
| Experimental | MeshPartitionWater | Mesh Partition Water | Exp | aus | Interoperability of Mesh Partition with the Water plugin. |
| Experimental | MeshTerrainMode | Mesh Terrain Mode | Exp | aus | Mesh Terrain Mode includes a suite of interactive tools for creating and editing Mesh Partitions in the Editor |
| Experimental | NaniteAssemblyEditorUtils | Nanite Assembly Editor Utilities | Exp | aus | Experimental support for Nanite Assembly creation in blueprint. |
| Experimental | NaniteDisplacedMesh | Nanite Displaced Mesh | Beta | aus | Asset and component types that provide a basic pre-displacement pipeline for Nanite meshes |
| Experimental | NiagaraToolsets | Niagara Toolsets | Exp | aus | A collection of tool calls allowing an AI assistant the ability to interact with Niagara. |
| Experimental | PCGBiomeCore | PCG Biome Core | Exp | aus | PCG Biome Creation Tool |
| Experimental | PCGBiomeSample | PCG Biome Sample | Exp | aus | PCG Biome Sample Plugin |
| Experimental | PCGFastGeoInterop | Procedural Content Generation Framework (PCG) FastGeo Interop | Exp | aus | Extra plugin for Procedural Content Generation Framework which enables runtime spawning of primitives using FastGeo components. |
| Experimental | PCGInstancedActorsInterop | Procedural Content Generation Framework (PCG) Instanced Actors Interop | Exp | aus | Extra plugin for Procedural Content Generation Framework interacting with Instanced Actors plugin. |
| Experimental | PCGMeshPartitionInterop | Procedural Content Generation Framework (PCG) Mesh Partition Interop | Exp | aus | Interoperability of Mesh Partition with PCG. |
| Experimental | PCGNaniteAssembliesInterop | Procedural Content Generation Framework (PCG) Nanite Assemblies Interop | Exp | aus | Extra plugin for Procedural Content Generation Framework interacting with Nanite Assemblies. |
| Experimental | PCGNiagaraInterop | Procedural Content Generation Framework (PCG) Niagara Interop | Exp | aus | Extra plugin for Procedural Content Generation Framework interacting with the Niagara system. |
| Experimental | PCGPrimitives | PCG Primitives | Exp | aus | PCG Primitives and Examples Library for World Building |
| Experimental | PCGPrimitives_MeshPartitionInterop | PCG Primitives Mesh Partition Interop | Exp | aus | Extra PCG Primitives and Examples Library for Mesh Partition interop |
| Experimental | PCGToolset | PCGToolset | Exp | AN | A collection of tools allowing the assistant to create and modify PCG graphs |
| Experimental | PCGWaterInterop | Procedural Content Generation Framework (PCG) Water Interop | Exp | aus | Extra plugin for Procedural Content Generation Framework interacting with the Water system. |
| Experimental | PixelStreamingPlayer | Pixel Streaming Player | Beta | aus | Support for receiving a pixel streaming stream and displaying it in game. |
| Experimental | ProceduralVegetationEditor | Procedural Vegetation Editor | Exp | AN | Node Graph based Editor that allows users to create Nanite Foliage ready vegetation directly in the engine. Users can load Procedural Vegetation Prese |
| Experimental | StateTreeToolset | StateTreeToolset | Exp | aus | Toolset for StateTree Inspection |
| Experimental | UAFStateTree | UAF State Tree | Exp | aus | StateTree integration for UAF. |
| Experimental | Volumetrics | Volumetrics |  | aus | A library of volume creation and rendering tools using Blueprints. |
| Experimental | Water | Water | Exp | aus | Full suite of water tools and rendering techniques to easily add oceans, river, lakes or custom water bodies that carve landscape and interacts with g |
| Experimental | WaterAdvanced | Water Advanced | Exp | AN | Collection of easy to use water simulation systems built on the Niagara Fluids and Water plugins |
| Experimental | WaterExtras | Water Extras | Exp | AN | Samples, test maps, etc intended to help developers start using the water system. Not intended to be used directly in a shipping product. |
| Experimental | WorldConditionsToolset | WorldConditionsToolset | Exp | aus | Toolset for WorldConditions Inspection |
| FX | CascadeToNiagaraConverter | Cascade To Niagara Converter | Beta | aus | Add support for scriptable conversion of Cascade Systems to Niagara Systems. |
| FX | ExampleCustomDataInterface | Niagara Example Custom DataInterface |  | aus | This plugin contains C++ example content that shows how to write your own data interface for Niagara.  Check out the plugin folder Engine/Plugins/FX/E |
| FX | Niagara | Niagara |  | an (Standard) | Niagara effect systems. |
| FX | NiagaraFluids | NiagaraFluids | Beta | AN | Fluid simulation toolkit for Niagara |
| FX | NiagaraInsights | Niagara Insights |  | an (Standard) | Niagara Unreal Insights Debugging and Performance |
| FX | NiagaraNanite | Niagara Nanite | Exp | aus | Adds a new renderer for rendering Nanite geometry. |
| FX | NiagaraPreviewContent | NiagaraPreviewContent |  | an (Standard) | Contains movie files used in Niagara |
| FX | NiagaraSimCaching | NiagaraSimCaching |  | an (Standard) | Adds support for recording and playing back Niagara simulations in sequencer via take recorder |
| FX | NiagaraUIRenderer | Niagara UI Renderer | Exp | aus | Renders Niagara CPU particle systems inside Slate/UMG widgets using a dedicated UI sprite renderer. |
| Interchange | InterchangeOpenUSD | Interchange OpenUSD | Exp | aus | Allows translation of OpenUSD files via the Interchange framework |
| Interchange | InterchangeOpenUSDChaosClothAsset | Interchange OpenUSD Chaos Cloth Asset | Exp | aus | Allows translation of OpenUSD files with Chaos Cloth Asset schemas via Interchange |
| Interchange | InterchangeOpenVDB | Interchange OpenVDB | Exp | aus | Allows translation of OpenVDB files via the Interchange framework |
| MovieScene | CinematicPrestreaming | Cinematic Prestreaming | Beta | aus | Adds a way to record certain types of streaming data requests in cinematic cutscenes. The requests can then be played back in advance on the Sequencer |
| PCG | PCG | Procedural Content Generation Framework (PCG) |  | an (Standard) | Visual scripting framework for procedurally populating worlds with content in editor and/or at run-time. |
| PCGInterops | PCGGeometryScriptInterop | Procedural Content Generation Framework (PCG) Geometry Script Interop | Beta | aus | Extra plugin for Procedural Content Generation Framework interacting with Geometry Scripts. |
| PCGInterops | PCGPythonInterop | Procedural Content Generation Framework (PCG) Python Interop | Beta | aus | Extra plugin for Procedural Content Generation Framework interacting with the Editor Python Interpreter. |
| Runtime | ChunkDownloader | Chunk Downloader |  | an (Standard) | Implements a streaming install client |
| Runtime | CustomMeshComponent | Custom Mesh Component |  | an (Standard) | A new renderable Component class that allows you to specify custom geometry via C++ or Blueprint. |
| Runtime | DummyMeshReconstructor | Sample Mesh Reconstructor | Beta | aus | Sample of how to drive mesh reconstruction. Generates dummy geometry to demonstrate API usage. |
| Runtime | GameplayStateTree | GameplayStateTree |  | aus | StateTree for AI/Gameplay Behaviors |
| Runtime | GeoReferencing | GeoReferencing |  | aus | GeoReferencing tools for UE worlds |
| Runtime | GeometryCache | Geometry Cache |  | an (Standard) | Support for distilled Geometry animations |
| Runtime | GeometryProcessing | Geometry Processing | Beta | aus | Data Structures and Algorithms for Processing 2D and 3D Geometry |
| Runtime | GeometryScripting | Geometry Script |  | aus | Geometry Script provides a library of functions for creating and editing Meshes in Blueprints and Python |
| Runtime | HTTPChunkInstaller | HTTP Chunk Installer |  | aus | Implements a streaming install client |
| Runtime | LevelStreamingPersistence | Level Streaming Persistence | Exp | aus | An experimental framework for persisting world state: actor and subobject property values, actor destroyed states, and actor respawning. State is asso |
| Runtime | ProceduralMeshComponent | Procedural Mesh Component |  | an (Standard) | A renderable component and library of utilities for creating and modifying mesh geometry procedurally. |
| Runtime | SmartObjects | SmartObjects |  | AN | Support for ambient life populating the game world |
| Runtime | StateTree | StateTree |  | aus | General purpose hierarchical state machine |
| Runtime | WorldConditions | World Conditions | Exp | aus | General purpose cached conditions |
| VirtualProduction | Avalanche | Motion Design |  | aus | Compositing, designer and broadcasting tool.  Plugin Dependencies: Advanced Renamer, Custom Details View, Dynamic Material, Geometry Cache, Geometry S |
| VirtualProduction | ClonerEffector | Cloners and Effectors |  | aus | Niagara based cloner system with various layouts and effector affecting each clone instances |
| VirtualProduction | GeometryMask | Geometry Mask |  | aus |  |
| WorldMetrics | WorldMetrics | World Metrics | Exp | an (Standard) | Provides access to the world metrics system |
| WorldStreamingInsights | WorldStreamingInsights | World Streaming Insights | Exp | aus | Suite of tools to profile, debug, and monitor aspects of world streaming in the Unreal Engine. |

## Nachtrag 23:15 – Ferat: „welche UE5-Plugins und Features waren für Witcher 4 im Einsatz?“
Bitte gezielt recherchieren (State of Unreal 2025 Witcher-4-UE5-Tech-Demo, CDPR/Epic-Talks, Unreal Fest, Epic-Blog, Interviews, Release-Notes 5.6–5.8,
Breakdowns): **welche Engine-Features und Plugins** CDPR/Epic für die Witcher-4-Demo (und die Zusammenarbeit an UE5 für Witcher 4) genutzt oder
entwickelt haben – z. B. Nanite Foliage, FastGeo Streaming, Mass/Crowds, MetaHuman, Animation (Motion Matching, Unreal Animation Framework,
ML Deformer), Lumen/Raytracing-Einstellungen, Landschaft/Gelände, Wasser/Flüsse (wie wurden Flüsse und Wasserfälle gemacht?), Himmel/Wolken/Nebel,
PCG/Biome – je Feature: was es tut, ob in 5.8 verfügbar (Plugin-Name aus der Liste oben oder Engine-Feature), Reife, und was Eldarien davon nutzen
sollte (mit Begründung, Aufwand, Risiko). Quellen mit Links, Unsicheres kennzeichnen.
