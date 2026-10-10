# Materialseitige Nässe schlägt platzierte Ufer-Decals

Recherchebericht für Projekt „Eldarien“ (UE 5.8.3, World Partition 1 km, Nanite-Landscape 1 m / 22 Layer, RVT_Eldarien_Boden, Epic-Water-Flüsse 4–40 m, ~250 km Uferlinie, alles per Editor-Python). Stand 2026-10-10. Alle Quellen konnten nur als Suchmaschinen-Auszüge gelesen werden; Details unter „Offene Punkte“.

## Kurzfazit

**Frage 1 (Coast & Dunes).** Das Fab-Listing belegt den Inhalt (14 Decals „from wet shore, clay, rocks, pebbles to different sand types and dunes“, 9 Treibholz-Logs, 85 Bodentexturen in 28 Sets, Spline-Cliffs, River-Spline-Blueprint, Nanite-fähiger 8-Layer-Landscape-Shader, „landscape blend RVT checkbox“ in allen opaken Materialien), aber **keine einzige Quelle nennt Ordnerstruktur, Master-Material- oder Parameternamen des Pakets; diese konnten nicht verifiziert werden**. Der Decal-Typ ist nicht dokumentiert; alles spricht für gewöhnliche DBuffer-Decal-Materialien, ein RVT-schreibender Decal-Typ wird nirgends erwähnt. Technisch gilt per Epic-Doku: Nanite-Oberflächen empfangen projizierte Decals, aber keine Mesh-Decals (translucent); in die RVT schreiben nur Materialien mit Virtual-Texture-Domain bzw. RuntimeVirtualTextureOutput; Decals können Nanite-Tessellation nicht beeinflussen. Folge für Eldarien: Die Pack-Decals erscheinen zwar auf der Nanite-Landscape, landen aber nicht in RVT_Eldarien_Boden, sodass jedes RVT-geblendete Mesh darüber eine Naht erzeugt (Ableitung aus Epic-Regeln, kein paketspezifischer Bericht).

**Frage 2 (Pipeline).** (a) Der 1–3 m Nassufer-Streifen gehört **ins Landscape-Material als Funktion „Wasserspiegel minus Weltposition Z“** aus einer groben Wasserspiegel-Textur; das ist billiger als jedes platzierte Decal (null Aktoren, kein RVT-Schreibpass, kein 23. Layer) und wird im Epic-Forum genau so für dieses Problem empfohlen. RVT-schreibende, nicht-Nanite ISM-Quads sind der Fallback für lokal autorisierte Details. DBuffer-Decal-Aktoren skalieren am schlechtesten (nicht instanziert, kein Occlusion Culling). (b) Steine als Nanite-ISM, ein Aktor pro Zelle und Größenklasse, aus dem 2-m-Raster per Python platziert (deterministisch, keine PCG-Bugs mit mehreren Flussplines); Kiesel 2–8 cm nur als Textur plus sparsame „Hero“-Kiesel, Kopfsteine 8–25 cm 1–4/m² auf Bänken, Blöcke 0,02–0,2/m² (alles Richtwert, nicht gemessen, es gibt keine Quelle für Steine/m²), 30–60 % eingegraben, Yaw entlang Fließrichtung ± 15°, flache Steine 10–25° stromaufwärts gekippt, Cull-Distanzen 20–40 m / 60–120 m / ≥300 m. (c) Treibholz: flussparallel, 0,3–1,5 m über Normalwasser, 20–40 % eingesunken, geclustert; „nur Außenbögen“ ist Stil, nicht Geomorphologie.

**Frage 3 (Wassermaterial).** Sichtbarer Grund = niedrige Scattering-Koeffizienten, niedrige Absorption, Opacity deutlich unter 1 am Single-Layer-Water-Knoten; Epic-Beispiel Absorption (0,0033 / 0,0016 / 0,0011). Die Instanzen heißen `Water_Material_River/_Lake/_Ocean` unter `/Water/Materials/WaterSurface/`; **die künstlerseitigen Parameternamen der Instanzen sind unverifiziert** (Binär-Asset). Schaum an Steinen liefert das Plugin nicht; Standardweg ist `DistanceToNearestSurface` plus `SceneDepthWithoutWater`. Kaustiken: Light-Function-Atlas (Spot/Point, nicht Directional) oder Kaustik-Textur im Bettmaterial; „Color Scale Behind Water“ projiziert nichts.

**Frage 4 (Performance).** Harte Grenze 16 777 216 gestreamte GPU-Scene-Instanzen; World-Partition-Registrierung zählt Komponenten, nicht Instanzen (ein riesiges ISM blockiert einen Streaming-Tick); deshalb ISM-Komponenten auf ~10–20k Instanzen splitten, keine Kollision, HLOD per `enable_auto_lod_generation=False` aus, VSM respektiert Nanite-Cull-Distanzen seit 5.3; ein RVT kann maximal 4096 Tiles pro Achse haben, über 250 km also ~24 cm/Texel bei 256-px-Tiles, folglich mehrere RVT-Volumes.

**Die eine Empfehlung:** Nassufer im Landscape-Material (Wasserspiegel-Textur), Steine als per Zelle gesplittete Nanite-ISM aus dem 2-m-Raster, Treibholz als gleiche ISM-Klasse mit Cluster-Regeln, Coast-&-Dunes-Decals nur für RVT-ferne Hero-Stellen oder als VT-Domain-Duplikat; die Paket-Assets zuerst im Editor inspizieren, weil kein Name aus dieser Recherche belastbar ist.

## Frage 1 – Coast & Dunes: Technik, Absicht, Verhalten auf Nanite-Landscape mit RVT

### Was belegt ist

Das Fab-Listing (ID 15697157) beschreibt das Paket als „scanned asset library with 4K textures, LOD'd meshes, and materials for coastal and dry-terrain scenes“ mit „a nanite landscape with an 8-layer height-blended shader, scanned cliffs for spline use, and a river blueprint for generating river splines“ und nennt als Feature-Zeilen **„14 decals from wet shore, clay, rocks, pebbles to different sand types and dunes“, „9 Dry driftwood, logs“, „85 Ground textures in 28 sets, 28 materials“, „Tilled scanned cliffs that are ready for use with splines“, „all textures are 4096x4096“** ([Fab-Listing](https://www.fab.com/listings/15697157-fccc-45dc-8e23-2897ece19c99)). Die beiden RVT/Nanite-Aussagen lauten wörtlich „Landscape nanite properly, height-blended 8 layers shader“ und **„All opaque shaders/materials support landscape blend runtime virtual texturing (RVT) checkbox“** ([Fab-Listing](https://www.fab.com/listings/15697157-fccc-45dc-8e23-2897ece19c99)). Als Setup-Hinweise stehen dort „Sea will work after you turn on the Unreal Water Plugin“ und „Turn on the distance field for foam on sea surface and use RVT virtual blend between cliffs and other models with the landscape“ ([Fab-Listing](https://www.fab.com/listings/15697157-fccc-45dc-8e23-2897ece19c99)). Das Promo-Video nennt **196 unique meshes und 142 material instances** ([YouTube-Auszug](https://www.youtube.com/watch?v=OQj1LpL4t14)). Die Schwesterpakete gaten dieselbe RVT-Blend-Technik auf Engine-Versionen: Mountain „requires Unreal 5.5 and higher“, Forest „On UE5.6 and higher … supports RVT Blend“ mit „nanite(UE5.6+) height blended landscape materials (8 layers)“ ([Fab Mountain](https://www.fab.com/listings/9ec7df30-3347-4056-8933-6156d983b0cf); [Fab Forest](https://www.fab.com/listings/11479aa9-a0bb-4292-80b7-1033c48df94c)). Der Hersteller hat das Paket mit dem 5.6-Water-Plugin demonstriert ([YouTube 5.6 Water](https://www.youtube.com/watch?v=81RaQ5eIC00)); ein „Unreal Engine 5 Tutorial“-Video existiert, ist aber die einzige „Dokumentation“ ([YouTube Tutorial](https://www.youtube.com/watch?v=87vuoLKz4DE)).

### Was nicht belegt ist

Die im Auftrag genannten „2 surface meshes (rock, clay)“ tauchen in keinem Auszug auf. Ordnernamen, Master-Materialien (M_…, DM_…), Parameter wie Wetness/Tiling/RVT-Blend-Height, Decal-Blend-Mode, Nanite-Flags der Meshes, Kollisionen, der Fab-Block „Supported Engine Versions“ und die Lizenz konnten nicht gelesen werden (fab.com durch den Proxy blockiert). Die naturemanufacture.com-Seite nennt abweichend „116 Ground textures in 26 sets, 34 materials … albedo/smoothness“ – Unity-Terminologie, vermutlich die Unity-Edition ([naturemanufacture.com](https://naturemanufacture.com/coast-dunes-environment-dynamic-nature/)); für UE gilt die Fab-Zahl 85/28.

**Ableitung zum Aufbau:** „Decals“ im Listing plus das Fehlen jeder VT-/RVT-Decal-Erwähnung bedeutet mit hoher Wahrscheinlichkeit klassische Decal-Domain-Materialien (DBuffer-Blend, die UE5-Voreinstellung: „DBuffer Decals are enabled by default in the Project Settings for all Unreal Engine 5 projects“, [Epic Decal Materials](https://dev.epicgames.com/documentation/en-us/unreal-engine/decal-materials-in-unreal-engine)). Die „RVT checkbox“ ist nach dem Muster von Forest/Mountain ein Static Switch, der die Landscape-RVT **sampelt** und den Mesh-Fuß in den Boden blendet, kein RVT-Schreiben. „LOD'ed“ deutet auf klassische LOD-Ketten; ob Nanite auf den Meshes aktiv ist, ist unbekannt. Dass der Hersteller Mesh Distance Fields für den RVT-Blend verlangt, legt eine DF-/Höhen-Maskierung nahe (Ableitung).

### Verhalten auf Nanite-Landscape mit RVT in 5.8

Drei Epic-Regeln bestimmen das Verhalten. Erstens: **„Nanite-enabled meshes can receive decals projected onto their surfaces but do not support Mesh Decals, which require materials to use a Translucent Blend Mode“** ([Epic Nanite](https://dev.epicgames.com/documentation/unreal-engine/nanite-virtualized-geometry-in-unreal-engine)); im Forum war der Workaround, Mesh-Decal-Geometrie als separates Nicht-Nanite-Mesh abzutrennen ([Forum Mesh decals and Nanite](https://forums.unrealengine.com/t/mesh-decals-and-nanite/1359353)). Zweitens: **„Before a component is rendered to the RVT through the RVT Volume, its Materials must use the Virtual Texture Material Domain or use properly setup RVT Material Expressions“**; ein „Static Mesh plane with a material outputting to an RVT will write the material like a decal to the RVT landscape material“ ([Epic RVT](https://dev.epicgames.com/documentation/en-us/unreal-engine/runtime-virtual-texturing-in-unreal-engine); [RVT Quick Start](https://dev.epicgames.com/documentation/en-us/unreal-engine/runtimevirtual-texturing-quick-start-in-unreal-engine)). Drittens: **„Non-Nanite Landscape data is required for Runtime Virtual Textures, water rendering, and more. This means twice the amount of data is streamed“** ([Epic Nanite Landscapes](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-nanite-with-landscapes-in-unreal-engine)). Decals lesen den Depth-Buffer und „cannot alter anything that would impact the depth buffer“ – Nanite-Tessellation, WPO, PDO bleiben unberührt ([Forum Decals/Displacement](https://forums.unrealengine.com/t/decals-affecting-landscape-displacement/2195439)).

Für Eldarien heißt das: Die 14 DBuffer-Decals rendern auf der Nanite-Landscape, aber nicht in RVT_Eldarien_Boden; Cliffs oder Steine mit RVT-Blend blenden zur un-decalten Bodenfarbe und erzeugen eine Naht; „pebbles“-Decals bleiben auf tessellierter Landscape flach. Epic sagt nirgends wörtlich „DBuffer-Decals landen nicht in der RVT“; die Folgerung ergibt sich aus der VT-Domain-Regel. Relevante Bugmeldungen: **UE-217644 „Runtime Virtual Textures are slow to update when enabling Nanite tessellation on a landscape“ (5.4, Fix-Ziel 5.5, Status in 5.8 unbestätigt)** ([UE-217644](https://issues.unrealengine.com/issue/UE-217644)); UE-263182 RVT instabil mit ClearCoat/Cloth auf Nanite-Landscape ([UE-263182](https://issues.unrealengine.com/issue/UE-263182)); 5.6-Thread „RVT display breaks“ bei Displacement ([Forum 5.6](https://forums.unrealengine.com/t/runtime-virtual-texture-is-broken-if-displacement-is-used-in-a-landscape-material-currently-using-5-6/2663851)); ein **UE-5.8-Thread** (ca. Aug 2026), in dem die RVT „only outputs the landscape's default/base material“ trotz korrekt gemalter Layer – ohne Lösung im Auszug ([Forum 5.8 RVT base color](https://forums.unrealengine.com/t/runtime-virtual-texture-only-outputs-landscape-base-color-instead-of-painted-landscape-layers-ue-5-8/2739603)); der Fehler „Virtual texture samples are not allowed during runtime virtual texture outputs“ (5.6+, erneut 5.8.1→5.8.2), behoben per Virtual Texture Feature Switch bzw. „Relax Runtime Virtual Texture Restrictions“ ([Forum](https://forums.unrealengine.com/t/problem-with-runtime-virtual-textures-and-landscape-material/2049913); [Forum 2](https://forums.unrealengine.com/t/virtual-texture-and-runtime-virtual-texture-in-landscape/2661222)); Nanite-Landscape bricht Landscape-Spline-Meshes in 5.6 (Position-Precision/Skirt als Fix) ([Forum](https://forums.unrealengine.com/t/nanite-on-landscape-breaks-landscape-spline-meshes-on-5-6/2701969)). Berichte „RVT geht nicht mit Nanite“ sind alt (5.3-Writer-Limit), Volume-Größen-Probleme oder Plugin-spezifisch ([Forum 5.3/5.4](https://forums.unrealengine.com/t/rvt-is-not-working-with-nanite-enabled-meshes/1927428); [TerraPrime #8](https://github.com/OrchidIsle/TerraPrimePlugin/issues/8)); Epics Position ist, dass RVT auf Nanite-Landscape über die Nicht-Nanite-Daten funktioniert. Ein Coast-&-Dunes-spezifischer Bericht zu Nanite oder RVT wurde nicht gefunden.

## Frage 2 – Skript-Pipeline für ~250 km Uferlinie

### (a) Nassufer-Streifen 1–3 m

| Option | Mechanik | Kosten/Stabilität in 5.8 | Urteil |
|---|---|---|---|
| Landscape-Material: Nässe aus Wasserspiegel | `smoothstep(z_wasser+h_hi, z_wasser+h_lo, WorldPosition.z)` × Hang-/Noise-Maske; Roughness senken, Albedo dunkeln | Einige ALU + 1 grobe Textur, keine Aktoren, kein Schreibpass, kein Layer | **Primär** |
| RVT-schreibende Quads (ISM, VT-Domain) | Planes mit RuntimeVirtualTextureOutput, Pass Type „nur VT“, nicht-Nanite | Nach Caching billig; tausende Komponenten; RVT/Nanite-Bugs 5.4–5.6 | Fallback, lokal |
| 23. Layer „Nassufer“ | 8-bit-Weightmap aus 2-m-Raster | Sampler-Budget pro Komponente; Python-Import unbestätigt | Nur als Maske |
| DBuffer-Decal-Aktoren | DecalActor je ~5 m | Nicht instanziert, kein Occlusion Culling | Nur Hero-Stellen |

Die Material-Lösung wird im Epic-Forum genau für dieses Problem empfohlen: Der Fragesteller wollte „the water on the shores to affect the landscape wetness“, die Antwort lautet **„Calculate the water level in the landscape's material and change roughness based on whether a pixel is below or above it“** ([Forum Landscape wetness](https://forums.unrealengine.com/t/how-to-get-water-to-affect-landscape-wetness/414538)). Der Look selbst ist trivial: nasser Sand ist „basically just darker and more reflective“ ([Cyanilux](https://www.cyanilux.com/tutorials/shoreline-shader-breakdown/)). Wichtige Ableitung: Das Landscape-Material kennt sein eigenes `WorldPosition.z`; es braucht die World-Height-RVT nicht. Es braucht eine **Wasserspiegel-Karte** (nicht die Nassband-Maske): Weil der Wasserspiegel entlang eines Flusses langsam variiert, reicht ein grobes Raster (8–32 m/px, 16 bit), und die Streifenbreite wird bei Landscape-Pixelpräzision ausgewertet – nicht durch das 2-m-Raster begrenzt. Ist das Landscape-Material RVT-getrieben, muss der Nässe-Term im Zweig liegen, der in die RVT schreibt; dann wird er gratis gecacht. Die Water-Info-Textur des Plugins enthält den Wasserspiegel (Z = normalisierte Wasserhöhe, siehe Frage 3), ihr Sampling aus dem Landscape-Material ist aber nicht belegt.

Der RVT-Quad-Fallback folgt dem Epic-Muster: RVT ist „a good fit for Landscape shading that uses decal-like materials and splines“; per „Virtual Texture Pass Type“ hält die Option „Never“ eine Komponente aus dem Main Pass ([Epic RVT](https://dev.epicgames.com/documentation/en-us/unreal-engine/runtime-virtual-texturing-in-unreal-engine); [Epic RVT 4.27](https://docs.unrealengine.com/4.27/en-US/RenderingAndGraphics/VirtualTexturing/Runtime)); „draw in main pass“ ist zur Laufzeit nicht änderbar, im Editor-Python schon ([Forum](https://forums.unrealengine.com/t/virtual-texture-draw-in-main-pass/666436)). Die Quads müssen nicht-Nanite sein, da Nanite-Meshes zumindest in älteren Versionen nicht in die RVT schrieben ([Forum 5.3](https://forums.unrealengine.com/t/rvt-is-not-working-with-nanite-enabled-meshes/1927428)). Für den 23. Layer gilt: Weightmaps sind „single-channel, grayscale, 8 bits per pixel“ in Landscape-Auflösung ([Epic Custom Layers](https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-and-using-custom-heightmaps-and-layers-in-unreal-engine)); die Praxisgrenze liegt bei etwa „12 user textures per component“, und „a new paint stroke can barely touch one corner and send a component over the limit“ ([Polycount](https://polycount.com/discussion/102539/limited-number-of-textures-on-a-landscape-compnent)) – bei 22 Layern ist das schon knapp. Der Landscape-Patch-Plugin kann „read from a texture or render target and apply the results to the landscape in the editor“ ([Epic Landscape Patch](https://dev.epicgames.com/documentation/unreal-engine/landscape-patch-system)). Decal-Aktoren „do not currently support instancing“ und sind „exempt from occlusion culling“; in einer gemessenen Szene (5.4) kamen „about 4,000 draws … almost entirely from decal actors“ ([blog.rime.red](https://blog.rime.red/unreal-static-mesh-and-decal-optimisations/)); 250 km / 5 m wären ~50 000 Decal-Aktoren (Ableitung).

### (b) Kies und Steine in Bett und Böschung

Geomorphologie liefert belastbare Regeln für Orientierung und Sortierung, aber **keine Quelle nennt Steine pro m² nach Größenklasse oder Eingrabungsanteile** – alle Dichten unten sind Richtwerte, nicht gemessen. In einem verflochtenen Kiesfluss gilt: **„The imbrication of AB-planes reveals a close correspondence with the channel direction; the deviations seldom exceed 30°“ und „irrespective of size, there is a strong upcurrent imbrication“** ([Gravel fabric, IAS](https://repository.ias.ac.in/67306)); isolierte große Kiesel auf Sand zeigen die stärkste Vorzugsrichtung, flache Kiesel in Kontakt „develop a stronger upstream imbrication mode“ ([Rust 1972](https://archives.datapages.com/data/sepm/journals/v42-46/data/042/042002/0384.htm)). In Bögen bewegen sich „particles finer than d50 preferentially … up the point bar and particles coarser than d50 … toward the thalweg“ ([Julien & Anthony, IAHR](https://iahr.org/library/info?pid=5624)). Bank-D50 liegt bei **6–43 mm** ([Berkeley 1994](https://creeks.berkeley.edu/sites/default/files/publications/1994.sc.sfc.bedsize.morley.pdf)) und schwankt zwischen Bänken um über 30 mm ([USGS 2011-5041](https://pubs.usgs.gov/sir/2011/5041/section5.html)).

| Klasse | Größe | Dichte (Richtwert, nicht gemessen) | Eingraben | Cull-Ende (Richtwert) |
|---|---|---|---|---|
| Kiesel | 2–8 cm | 0 Instanzen; Textur/RVT/Tessellation; „Hero“-Kiesel 2–5/m² in 3 m Uferabstand | 40–60 % | 20–40 m |
| Kopfsteine | 8–25 cm | 1–4/m² Kiesbank, 0,3–1/m² Böschung, 6–8/m² Riffel/Außenbogen-Fuß | 30–50 % | 60–120 m |
| Blöcke | 25–100 cm | 0,02–0,2/m², Cluster 3–7 an Außenbögen, Prallhängen, Mündungen | 20–40 % | ≥300 m / kein |

Begründung: Eine vollflächige Kiesbank mit D50 ≈ 30 mm hätte ~1000 Klasten/m² – als Instanzen sinnlos (Ableitung). 250 km × ~10 m angezogener Breite ≈ 2,5 km²; bei im Mittel 2 Instanzen/m² sind das ~5 Mio. Instanzen weltweit, mit Zonierung nach Wasserabstand und Krümmung weniger. Orientierung: Yaw = Fließrichtung ± N(0°, 15°), Pitch 10–25° stromaufwärts für flache Klasten, ~0° für runde, Roll klein; Fließrichtung ist die Tangente des Water-Splines (`get_water_spline()`, `get_water_velocity_at_spline_input_key`, beide in 5.2-Python-Doku belegt, [WaterBodyComponent 5.2](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyComponent?application_version=5.2)) oder bei Arbeit aus dem 2-m-Raster der Gradient der Wasserband-Distanz. Größengradient: grob zum Thalweg und Außenbogen-Fuß, fein auf die Gleituferbank (Innenbogen).

Cull-Distanzen sind der wichtigste Hebel, weil **„Nanite geometry always renders to the Virtual Shadow Map regardless of distance“** ([Epic VSM](https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine)), seit 5.3 aber „VSMs now respect the Nanite cull distance even when shadow caching is enabled“ ([UE Roadmap VSM](https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/1166-virtual-shadow-maps)). Die Quellen widersprechen sich, ob Nanite-ISM Instanz-Cull-Distanzen beachten: Foliage-Doku „Nanite-enabled meshes are not affected by culling distance and instance fading“ ([Epic Foliage](https://dev.epicgames.com/documentation/unreal-engine/foliage-mode-in-unreal-engine)) gegen `r.Nanite.Culling.DrawDistance` = 1 ([CVar-Wiki 5.4.4](https://indxzero.github.io/ue544cvarwiki/articles/r.nanite.culling.drawdistance/)) und einen 5.6-Fix für „per instance cull distance (foliage)“ in CSM ([Tom Looman 5.6](https://tomlooman.com/unreal-engine-5-6-performance-highlights/)). **In 5.8.3 testen.** Eine PCG-Faustregel nennt 5000 cm für Gras und 15000 cm für Steine ([gamedevcore PCG](https://www.gamedevcore.com/blog/ue5-pcg-tutorial-procedural-generation)). ISM statt HISM: „if your project only uses Nanite then ISM is always the choice since Nanite has its own culling and LOD system“ ([Epic ISM](https://dev.epicgames.com/documentation/en-us/unreal-engine/instanced-static-mesh-component-in-unreal-engine)).

PCG oder Python: PCG liest Water-Splines nativ („Get Spline Data“ auf Water-Bodies, benötigt PCG Geometry Script Interop; 5.5 brachte den PCGWaterInterop-Plugin mit „Get Water Spline Data“) ([Epic PCG Node Reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine); [UE 5.5 Release Notes](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-5-release-notes)), aber ein Bug-Thread meldet, dass Get Spline Data „only gets one of the two rivers in the scene“ ([Forum PCG](https://forums.unrealengine.com/t/pcg-graph-not-recognising-all-the-river-splines-in-my-scene/2672967)). Bei 101 Streams und 53 Seitenarmen und der Vorgabe „alles per Python“ ist direkte Python-Platzierung aus dem 2-m-Raster die konsistentere Wahl: deterministisch, exakte Regeln, ISM-Aktoren passend zur 1-km-Zelle; ein Hybrid (Python erzeugt PCG-Punktdaten) wurde nicht recherchiert.

### (c) Treibholz an Außenbögen

Die Literatur stützt flussparallele Ausrichtung in größeren Gerinnen („tree boles and jams shift from fairly random orientations in small channels toward parallel-to-flow arrangements in larger channels“, [Abbe & Montgomery 1996](https://archive-wpg.forestry.oregonstate.edu/sites/wpg/files/bibliopdfs/01_Brauderick%26Grant.pdf)), bank- und mäandergebundene Jam-Typen (bar top, bar apex, meander jams; ebd.), das Einsedimentieren von Außenbogen-Stämmen („gradually buried by the sediment it trapped“, [GSA 2005](https://gsa.confex.com/gsa/2005CD/webprogram/Paper85754.html)) und Verankerung an stehenden Bäumen („a majority of jams were pinned by standing trees“, [NSF PAR](https://par.nsf.gov/servlets/purl/10342965)). Aber eine tschechische Studie fand **keine Beziehung zur Position im Mäanderbogen** ([Masaryk Univ.](https://www.muni.cz/en/research/publications/958160)) – „Außenbögen only“ ist eine Stilentscheidung. Regeln für das Skript (Ableitung, keine Zahl ist gemessen): Kandidaten = Uferzellen mit |Krümmung| über Schwelle auf der Außenseite plus Bankköpfe, Inselspitzen und Stellen mit Anker (Baum/Block); Höhe 0,3–1,5 m über Normalwasser auf Kies/Sand; Yaw = Fließtangente ± N(0°, 20°), jeder fünfte Stamm quer an einem Anker; 20–40 % des Stammdurchmessers eingesunken, Wurzelteller stromaufwärts; Poisson-Cluster mit Elternpunkt alle 150–600 m Ufer und 2–6 Stämmen plus Astwerk-Halo (Megascans ScatteredSticksAndTwigs) und dunkler Nässe-Override darunter; an Seen windgetrieben an Lee-Ufern statt nach Krümmung.

## Frage 3 – Epic-Water-Flussmaterial mit sichtbarem Grund

Die physikalischen Regler liegen am **Single Layer Water Material**-Ausgabeknoten (Blend Mode Opaque/Masked, Shading Model SingleLayerWater): **Scattering Coefficients** („Low values make the water look clear, high values thicker/more opaque“), **Absorption Coefficients** („larger values make colors fade faster“; Epic-Beispiel R 0,0033, G 0,0016, B 0,0011, Rot verschwindet zuerst), **PhaseG** (−1…1), **Color Scale Behind Water** (multipliziert die Leuchtdichte unter Wasser; „It is a visual effect only. It does not project caustics or shadows“), plus **Opacity** am Hauptknoten: „An Opacity of 1 looks dark because no light penetrates the surface“ ([SLW-Doku 5.6, Spiegel](https://github.com/ReduxST/UE5.6-Markdown-Docs/blob/73fd2bd6d444820f2acbc81878f685c0482524d5/Designing_Visuals,_Rendering,_and_Graphics/Materials/Material_Properties/Shading_Models/Single%20Layer%20Water%20Shading%20Model.md); [Epic live](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine)). Ein dunkles Bett ist fast immer Opacity nahe 1 oder zu hohe Absorption, nicht Water-Zone-Auflösung: SLW liest Szenenfarbe und echten Depth-Buffer, die Water-Info-Textur dient Schaum/Flow/Queries (Ableitung aus Doku und Engine-Code).

Die ausgelieferten Instanzen sind in Engine-Quellen belegt: `/Water/Materials/WaterSurface/Water_Material_River`, `_Lake`, `_Ocean`, LOD-Variante `…/LODs/Water_Material_River_LOD` ([WaterEditorSettings.cpp](https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Editor/Private/WaterEditorSettings.cpp)); alle sind Kinder eines Masters `Water_Material` mit Switches je Body-Typ, Flüsse haben Zusatzparameter für „velocity, flow control, and density“, eigene Materialien brauchen das Usage-Flag „Used with Water“ ([Water Meshing 5.6](https://github.com/ReduxST/UE5.6-Markdown-Docs/blob/73fd2bd6d444820f2acbc81878f685c0482524d5/Building_Virtual_Worlds/Water_System/Water%20Meshing%20System%20and%20Surface%20Rendering.md)). Der Ordner ist nur mit „Show Engine Content“ und „Show Plugin Content“ sichtbar ([Forum](https://forums.unrealengine.com/t/where-is-the-water-content-listed-in-the-official-unreal-engine-documentation/2550316)). **Die künstlerseitigen Parameternamen der Instanzen sind unverifiziert.** Indizien: ein Projektskript setzt auf einem Kind von Epics Ozeanmaterial die Vektorparameter `Absorption` = (8, 70, 420) und `Scattering` = (0, 0.25, 0.40) mit dem Kommentar „Absorption ranges roughly 0 to 500, Scattering ranges 0 to 1“ ([NaviSense](https://github.com/LemuelHornsby/NaviSense)); ein anderer Backlog nennt „Foam Scattering“/„Foam Scatter Bias“ ([voxelsim](https://github.com/mnoles1911/voxelsim)). Wenn die Instanz wirklich 0–500 anbietet, rechnet der Master intern um, und kleine Zahlen bedeuten weniger Absorption – vor dem Eintippen den Parameter im Editor prüfen. Forum-Falle: Absorption ist „not a color, it's the rate at which the RGB wavelengths are absorbed“; der Value-Slider macht das Wasser schwarz ([Forum](https://forums.unrealengine.com/t/changing-water-material-color-value-breaks-it/1227565)). Ein Einzelbericht sagt, das Material im Water-Material-Slot des Bodys wurde ignoriert und nur das Engine-Material wirkte ([Forum](https://forums.unrealengine.com/t/water-plugin-cant-change-river-color/2571248)).

| Parameter (SLW-Knoten, per cm – Ableitung) | Epic-/Community-Wert | Startwert klarer Bergfluss (Richtwert) |
|---|---|---|
| Absorption Coefficients | Epic (0,0033/0,0016/0,0011); Forum (0,35/0,07/0,03)×0,01 | (0,003–0,006 / 0,0007–0,002 / 0,0003–0,001) |
| Scattering Coefficients | Forum (0,0007/0,0021/0,0025)×0,01; Skript (0,001/0,0025/0,003) | 0,00001–0,0003 je Kanal, Blau/Grün leicht über Rot |
| PhaseG | Forum 0,1; Skript 0,25; Doku-Beispiele −0,75/0,5 | 0,1–0,5 |
| Opacity | Pool-Tutorial 0,5 | 0,3–0,6 |
| Roughness | – | 0,02–0,08 |

Quellen der Community-Werte: [Forum „Actually realistic water shader“](https://forums.unrealengine.com/t/actually-realistic-water-shader/141661), [WoLD SLW-Pool](https://www.worldofleveldesign.com/categories/ue5/single-layer-water-pool-still.php), [Kitchen-Water-Skript](https://github.com/kagura-yami/AGift4MyYoungerSelf). Die Einheit „pro cm“ ist Ableitung: Die 5.6-Doku sagt „reciprocal meters“, das älteste Rezept multipliziert mit 0,01, und Epics 0,0033 entspricht ~3 m Rot-Extinktion, was zu realem Wasser passt. Roughness ist unter Lumen fast wirkungslos: „Lumen Reflections support Single Layer Water materials, with reflections forced to mirror“ ([Epic Lumen](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine)); Nimue nutzte Roughness nur zur Specular-Skalierung ([80.lv Nimue](https://80.lv/articles/how-to-build-stylized-water-shader-design-implementation-for-nimue)). Bettschärfe: `r.Water.SingleLayer.RefractionDownsampleFactor` ist in ≥5.5-Code 1 (früher 2) ([SingleLayerWaterRendering.cpp](https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Source/Runtime/Renderer/Private/SingleLayerWaterRendering.cpp)).

**Tiefe und Water Zone.** Die Water-Info-Textur ist eine Top-down-Ortho-Aufnahme je Zone: XY Fließgeschwindigkeit, Z normalisierte Wasserhöhe, W normalisierte Bodenhöhe; Landscape-Proxies werden mit `bAutoIncludeLandscapesAsTerrain = true` automatisch als Boden gerendert (LOD-Override ~2 Quads pro Texel), **ohne Nanite-Sonderpfad**; `bHalfPrecisionTexture = true`, `VelocityBlurRadius = 1`, `CaptureZOffset = 64`, Lokal-Tessellation per `bEnableLocalOnlyTessellation` ([WaterZoneActor.h](https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Public/WaterZoneActor.h); [WaterInfoRendering.cpp](https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Private/WaterInfoRendering.cpp)). Für Eldarien: bei Zonen mit hunderten Metern Höhenunterschied `bHalfPrecisionTexture` aus, `RenderTargetResolution` hoch, oder Zonen je Talabschnitt (Ableitung). Body-Defaults: `ShapeDilation` 4096, `FixedWaterDepth` 512 ([WaterBodyComponent.h](https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Public/WaterBodyComponent.h)); Spline-Metadaten `Depth` 150 cm, `RiverWidth` 2048, `WaterVelocityScalar` 128 ([WaterSplineMetadata.h](https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Public/WaterSplineMetadata.h)); Breite/Tiefe per `GetRiverWidthAtSplineInputKey`/`GetRiverDepthAtSplineInputKey` auf `UWaterBodyRiverComponent` ([WaterBodyRiverComponent.h](https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Public/WaterBodyRiverComponent.h)). 5.8-Eigenheit: nach TileSize/Extent-Änderung meldet die Zone ein veraltetes Grid, zweites `MarkForRebuild` nötig ([ue-mcp #1156](https://github.com/db-lyon/ue-mcp/issues/1156)).

**Schaum an Steinen.** Das Plugin hat „no real support for contact foam“; Epics Demo nutzte Niagara ([Forum Foam](https://forums.unrealengine.com/t/water-plugin-in-ue5-does-anyone-know-how-to-use-the-foam-on-rivers-see-video-linked/688819)). Standard: `DistanceToNearestSurface` (Global Distance Field) „combine Depth Fade with DistanceToNearestSurface“ für gleichmäßige Kanten ([80.lv Nimue](https://80.lv/articles/how-to-build-stylized-water-shader-design-implementation-for-nimue)); bei SLW statt SceneDepth den Knoten `SceneDepthWithoutWater` nutzen ([iby-z](https://iby-z.blogspot.com/2019/05/distance-field-water-foamflow-maps.html)); „Generate Mesh Distance Fields“ an, „Affect Distance Field Lighting“ am Wasser aus, sonst wird alles Schaum ([Gumroad-Notizen](https://noro.gumroad.com/l/HEppY)). Rezept (Ableitung): `1 − saturate(dist / FoamWidth)` mit FoamWidth 30–120 cm, multipliziert mit Fließgeschwindigkeits-Maske, plus flacher Tiefe-Maske für Uferschaum; GDF ist grob, also Schaum nur an Blöcken ≥ 50 cm. Der 5.6-„Shallow Water River“ (Water Advanced) ist in 5.8 gemeldet defekt („doesn't capture any depth information“, Einzelpatch am Shader auf 5.8.2) ([Forum 5.8](https://forums.unrealengine.com/t/shallow-water-plugin-not-working-in-5-8/2763339)) – meiden.

**Kaustiken.** Light Function Atlas: „Single Layer Water Uses Light Function Atlas“ ist standardmäßig aus; mit ihm „Water bodies receive light functions“; aber **„Directional lights are currently forced not to sample the atlas“** ([Light Functions 5.6](https://github.com/ReduxST/UE5.6-Markdown-Docs/blob/73fd2bd6d444820f2acbc81878f685c0482524d5/Building_Virtual_Worlds/Lighting_the_Environment/Direct_Lighting/Light%20Functions.md)). Für Sonnenlicht bleibt: Kaustik-Textur im Kies-/Bettmaterial, maskiert mit `WasserspiegelZ − WorldPosition.z` (0–1,5 m Falloff), oder Light Function am Directional Light (Legacy-Pfad); „cheap caustics“ kosten „49 instructions and 1 texture sample“ ([Medium](https://medium.com/hri-tech/cheap-water-caustics-in-ue4-ee1d3ac0cae1); [MrTapa](https://threadreaderapp.com/thread/1170897412103299077.html)). Ini-Block für Lumen+VSM (Read-only-CVars in DefaultEngine.ini): `r.Water.SingleLayer.DepthPrepass=1`, `r.Water.SingleLayer.ShadersSupportVSMFiltering=1`, `r.Water.SingleLayer.VSMFiltering=1` ([Forum Blocky Shadows](https://forums.unrealengine.com/t/blocky-shadows-on-single-layer-water/1151034)); optional `r.Water.SingleLayer.Refraction.DepthCulling` (seit 5.6) für tiefe Pools ([unrealdirective](https://unrealdirective.com/resources/console-variables/r-water-singlelayer-refraction-depthculling/)). 5.8 verschiebt die SLW-Velocity-Ausgabe in den Depth-Prepass (`r.Water.SingleLayer.VelocityOutputPass`, ersetzt `ForceVelocity`) ([UE 5.8 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes); [Tom Looman 5.8](https://tomlooman.com/unreal-engine-5-8-performance-highlights/)) – Default belassen.

## Frage 4 – Performance für 250 km in World Partition

**Instanzlimit.** „The maximum number of instances that can be present in the scene is hard-locked to 16 million instances, which includes all instances that are streamed in … Only instances streamed in are counted“ ([Epic Nanite](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine)); `INSTANCE_ID_NUM_BITS (24u)` = 16 777 216, Überlauf meldet „GPU-Scene Instance data overflow detected“ ([Forum 16M](https://forums.unrealengine.com/t/instance-limit-16m-debugging/2688178); [Forum Overflow](https://forums.unrealengine.com/t/gpu-scene-instance-data-overflow-detected-reduce-instance-count-to-avoid-rendering-artifacts/2666774)). Ein 64-B/Instanz-Wert ist nicht belegt; belegt ist nur die Forumsangabe 48 B für die Transform. Nanite-Cluster-Puffer kosten 12 B (Kandidat) / 16 B (sichtbar), sind nicht dynamisch, Überlauf = „missing or blinking geometry“, Diagnose `NaniteStats` ([Epic Nanite Technical](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-technical-details)); `r.Nanite.MaxVisibleClusters` ≤ 16×1024×1024 ([Forum](https://forums.unrealengine.com/t/nanite-overflow-error-in-packaged-build-5-3/1325562)). Ziel (Richtwert): ≤ 5 Mio. gestreamte Instanzen gesamt inkl. Gras, Steine ≤ 2–3 Mio.; der Lade-Radius, nicht die Weltsumme, zählt.

**Streaming.** Ein Entwickler-Trace: Epics inkrementelle Registrierung „covers actors but not individual instances“, das Budget „counts components rather than the instances inside them, so a single large ISM can stall a streaming tick“, Physik-Registrierung fällt pro Instanz an ([Forum WP Streaming](https://forums.unrealengine.com/t/world-partition-streaming-performance/2577446)). Folge: Stein-ISM auf ~10–20k Instanzen je Komponente splitten (Richtwert), keine Kollision, und die Steine in ein eigenes Runtime-Grid mit kleineren Zellen (`runtime_grid`), denn 1 km liegt beim 4-fachen der Community-Startgröße 256 m ([StraySpark WP](https://www.strayspark.studio/blog/ue5-world-partition-deep-dive-streaming-hlod)). Fast Geometry Streaming (5.6, „immutable static geometry“) ist genau für diese Hitch-Klasse gedacht, war aber „not yet recommended for production“; 5.7/5.8-Status unbekannt ([UE 5.6](https://www.unrealengine.com/news/unreal-engine-5-6-is-now-available); [Roadmap FastGeo](https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/2022-fast-geometry-streaming-plugin-experimental-)).

**HLOD und Licht.** Python-Property ist `enable_auto_lod_generation` („Whether this actor should be considered or not during HLOD generation“), `hlod_layer`, `is_spatially_loaded`, `runtime_grid` ([unreal.Actor](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/Actor)); ISM: `instance_start_cull_distance`/`instance_end_cull_distance`, `visible_in_ray_tracing` ([ISM 5.3](https://docs.unrealengine.com/5.3/en-US/PythonAPI/class/InstancedStaticMeshComponent.html)); `affect_distance_field_lighting` „is only used if CastShadow is true“ ([PrimitiveComponent 5.3](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PrimitiveComponent?application_version=5.3)). Epic lässt „Affect Distance Field Lighting“ bei Foliage aus, weil „thousands or tens of thousands of instances would overflow the tile culling buffer“ ([Epic Mesh DF](https://dev.epicgames.com/documentation/en-us/unreal-engine/mesh-distance-fields-in-unreal-engine)) – gilt für Kiesel ebenso. VSM: `r.Shadow.Virtual.MaxPhysicalPages` Default 4096 à 128×128 ([PerfGuard VSM](https://getperfguard.com/tutorials/virtual-shadow-maps)); 8192 auf 24 GB kostet je nach Quelle +128–256 MB ([StraySpark VSM 5.7](https://www.strayspark.studio/blog/virtual-shadow-map-optimization-open-worlds-ue5-7); [ibbles](https://github.com/ibbles/LearningUnreal/blob/main/Virtual%20Shadow%20Maps.md)).

**Decals.** Kosten = „shader complexity × bounding box size on screen, not the mesh complexity“ ([Epic Decal Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/decal-actors-in-unreal-engine)); DBuffer braucht den Depth-Prepass, der mit Nanite/Lumen/VT ohnehin läuft ([Epic Decal Materials](https://dev.epicgames.com/documentation/en-us/unreal-engine/decal-materials-in-unreal-engine)). Tausende Decals je Zelle sind fein, solange sich wenige überlappen; statische Decals besser in die RVT backen und ggf. nach dem Schreiben verstecken ([Forum RVT cost](https://forums.unrealengine.com/t/how-mu-h-cost-write-in-rvt/266509)).

**RVT-Budget.** „A maximum of 4096 tiles is currently supported“, Auflösung = Tiles × Tile Size ([Epic RVT](https://dev.epicgames.com/documentation/unreal-engine/runtime-virtual-texturing-in-unreal-engine)); 4096 × 256 px = 1 048 576 Texel über 250 km ≈ **24 cm/Texel**, mit 1024-px-Tiles ≈ 6 cm; 1 cm/Texel ist unmöglich (Ableitung). Also mehrere RVT-Volumes je 10–25 km oder je WP-Region, jedes ≤ 4096 Tiles. Low-Mips sind teuer: „Actors also have to be permanently resident to be available to render to low mips“ – gestreamte RVT-Quads fehlen in Fern-Mips, sofern nicht „Virtual Texture Skip Mips“ gesetzt ist ([Epic RVT](https://dev.epicgames.com/documentation/unreal-engine/runtime-virtual-texturing-in-unreal-engine)); Uploads sind auf `r.VT.MaxUploadsPerFrame` = 8 im Spiel gedrosselt ([Epic VT Pools](https://dev.epicgames.com/documentation/unreal-engine/virtual-texture-memory-pools-in-unreal-engine)). Das ist ein weiteres Argument für den Nässe-Term im Landscape-Material statt tausender RVT-Quads.

| Posten | Grenze/Default (belegt) | Ziel (Richtwert, nicht gemessen) |
|---|---|---|
| GPU-Scene-Instanzen | 16 777 216 gestreamt | ≤ 5 Mio., Steine ≤ 2–3 Mio. |
| ISM pro Komponente | keine Epic-Zahl | 10–20k, keine Kollision |
| Cull-Ende Steine | VSM folgt seit 5.3 | 20–40 / 60–120 / ≥300 m |
| VSM-Seiten | 4096 | 8192 |
| RVT | ≤ 4096 Tiles/Achse | Volumes je 10–25 km |
| DF-Licht/RT | Foliage: aus | ADFL, ADIL, RT aus |

## Python-Skelett (UNGETESTET)

Legende: `# OK` = Name in Python-/Engine-Doku-Auszügen (5.0–5.6) belegt; `# ?` = unverifiziert, mit `help(unreal.X)`/`dir(unreal.X)` in der 5.8.3-Konsole prüfen. Kein 5.8-Python-Dokument war erreichbar. **Größte Unsicherheit:** `Actor.add_component_by_class` ist als Blueprint-Knoten belegt, in Python-Auszügen nicht; ein Forum berichtet, dass per Python erzeugte Komponenten „doesn't get serialized or registered properly“ ([Forum add component](https://forums.unrealengine.com/t/editor-python-script-how-to-add-component-to-actor/1039923)). Fallback ist ein Blueprint-Aktor `BP_ShoreISM` mit vorgefertigten ISM-Komponenten, die per `get_components_by_class` geholt werden ([Forum Add Component by Python](https://forums.unrealengine.com/t/add-component-by-python/143662)).

```python
# -*- coding: utf-8 -*-
"""Eldarien Ufer-Dressing, UE 5.8.3, Editor-Python. UNGETESTET.
Eingaben: 2-m-Raster (Wasserband, Wasserspiegel, Höhe) als numpy-Arrays je 1-km-Zelle,
Shoreline-JSON. Ausgabe: je Zelle ein ISM-Aktor pro Steinklasse + Treibholz,
Material-Parameter für Nassufer und Wasser.
"""
import unreal, random, math

# ---------- Konfiguration ----------
CELL_M      = 1000                       # World-Partition-Zelle
MAX_PER_ISM = 15000                      # Richtwert: Komponenten splitten (WP registriert pro Komponente)
VERSION     = "v1"                       # in Seed/Label, damit Re-Runs stale Zellen erkennen
STONE_CLASSES = {
    # Klasse: (Mesh-Pfad [Projektpfad prüfen], Dichte/m² Ufer, Dichte/m² Bett, Höhe cm, Eingraben, Cull-Start cm, Cull-Ende cm)
    "pebble":  ("/Game/Megascans/3D_Assets/SmallStonesPack/SM_SmallStone_01",  3.0, 1.0,   5, (0.40, 0.60),  1500,  3000),
    "cobble":  ("/Game/Megascans/3D_Assets/DryRiverBed/SM_DryRiverBed_01",     1.5, 2.5,  15, (0.30, 0.50),  4000,  9000),
    "boulder": ("/Game/Megascans/3D_Assets/NordicBeachRocks/SM_NordicRock_01", 0.05, 0.1, 60, (0.20, 0.40), 20000, 40000),
}
DRIFTWOOD_MESHES = ["/Game/CoastDunes/Meshes/SM_Driftwood_01"]   # ? Paketpfad unbekannt, im Editor nachsehen
RVT_ASSET = "/Game/Eldarien/RVT/RVT_Eldarien_Boden"

EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)   # ? (Standard seit 5.0)

# ---------- Rasterzugriff (projektseitig, kein UE-API) ----------
def load_cell_rasters(cx, cy):
    """Liefert dict mit 2-m-Arrays: 'band' (0 Land, 1 Ufer, 2 Wasser), 'wlevel' (Wasserspiegel cm),
    'height' (Gelände cm), 'dist' (Abstand zur Wasserlinie m, signiert), 'flow' (Fließrichtung rad)."""
    raise NotImplementedError  # numpy aus vorbereiteten .npy; Fließrichtung = Gradient von 'dist' um 90° gedreht

def cell_rng(cx, cy, cls):
    return random.Random(f"{cx}:{cy}:{cls}:{VERSION}")        # deterministisch je Zelle und Klasse

# ---------- Aktor + ISM ----------
def find_or_spawn_cell_actor(label, folder):
    for a in EAS.get_all_level_actors():                        # OK
        if a.get_actor_label() == label:
            return a
    a = EAS.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, 0))   # ? Signatur prüfen
    a.set_actor_label(label)
    a.set_folder_path(folder)
    # World Partition / HLOD
    a.set_editor_property("enable_auto_lod_generation", False) # OK  (nicht b_enable_...)
    a.set_editor_property("hlod_layer", None)                   # OK
    a.set_editor_property("is_spatially_loaded", True)          # OK
    a.set_editor_property("runtime_grid", unreal.Name("StonesGrid"))  # OK (Grid vorher in WP-Settings anlegen)
    return a

def make_ism(actor, mesh, cull_start, cull_end, cast_shadow):
    try:
        ism = actor.add_component_by_class(unreal.InstancedStaticMeshComponent, False, unreal.Transform(), False)  # ? BP-Knoten belegt, Python nicht
    except AttributeError:
        # Fallback: BP_ShoreISM mit vorgefertigten ISM-Komponenten spawnen und holen:
        # comps = bp_actor.get_components_by_class(unreal.InstancedStaticMeshComponent)   # Forum-Muster
        raise
    ism.set_static_mesh(mesh)                                   # ? (StaticMeshComponent-Standard)
    ism.set_mobility(unreal.ComponentMobility.STATIC)           # ?
    ism.set_cull_distances(cull_start, cull_end)                # OK
    ism.set_editor_property("cast_shadow", cast_shadow)         # OK
    ism.set_editor_property("affect_distance_field_lighting", False)   # OK
    ism.set_editor_property("affect_dynamic_indirect_lighting", False) # OK
    ism.set_editor_property("visible_in_ray_tracing", False)    # OK
    # Kollision: 'No Collision' setzen – Property-Name in 5.8.3 prüfen (set_collision_enabled ?)
    return ism

def stone_transform(rng, x, y, z_ground, flow_rad, h_cm, bury, flat):
    yaw   = math.degrees(flow_rad) + rng.gauss(0, 15)            # Imbrikation: selten > 30° Abweichung
    pitch = rng.uniform(10, 25) if flat else rng.gauss(0, 3)     # flache Klasten stromaufwärts gekippt
    roll  = rng.gauss(0, 5)
    s     = rng.uniform(0.7, 1.4)
    z     = z_ground - rng.uniform(*bury) * h_cm * s             # Eingraben 20–60 %
    return unreal.Transform(unreal.Vector(x, y, z), unreal.Rotator(pitch, yaw, roll), unreal.Vector(s, s, s))

def dress_cell_stones(cx, cy):
    R = load_cell_rasters(cx, cy)
    for cls, (mesh_path, d_bank, d_bed, h_cm, bury, c0, c1) in STONE_CLASSES.items():
        rng  = cell_rng(cx, cy, cls)
        mesh = unreal.load_asset(mesh_path)                     # ? (Standard)
        xf   = []
        rows, cols = R["band"].shape
        for j in range(rows):
            for i in range(cols):
                band = R["band"][j, i]
                if band == 0 and R["dist"][j, i] > 6.0:          # nur 6 m Uferzone + Bett
                    continue
                dens = d_bed if band == 2 else d_bank
                # Größengradient (Ableitung): grob am Außenbogen/Thalweg – hier über 'dist' und Krümmungsmaske erweitern
                n = rng.poisson(dens * 4.0) if hasattr(rng, "poisson") else int(dens * 4.0 + rng.random())  # 2 m × 2 m = 4 m²
                for _ in range(n):
                    x = (cx * CELL_M + i * 2 + rng.random() * 2) * 100.0
                    y = (cy * CELL_M + j * 2 + rng.random() * 2) * 100.0
                    xf.append(stone_transform(rng, x, y, R["height"][j, i], R["flow"][j, i],
                                              h_cm, bury, flat=rng.random() < 0.4))
        # Splitten in Komponenten ≤ MAX_PER_ISM
        for k in range(0, len(xf), MAX_PER_ISM):
            label = f"SHORE_{cls}_X{cx:04d}_Y{cy:04d}_{k // MAX_PER_ISM:02d}_{VERSION}"
            actor = find_or_spawn_cell_actor(label, f"Shore/Cells/X{cx:04d}_Y{cy:04d}")
            ism   = make_ism(actor, mesh, c0, c1, cast_shadow=(cls != "pebble"))
            ism.clear_instances()                               # ? (für Re-Runs)
            ism.add_instances(xf[k:k + MAX_PER_ISM], False, True)   # OK: (transforms, return_indices, world_space=True)

# ---------- Treibholz ----------
def dress_cell_driftwood(cx, cy, shoreline_segments):
    """shoreline_segments: Liste von (x, y, tangente_rad, kruemmung, z_wasser) in 2-m-Schritten aus dem JSON."""
    rng = cell_rng(cx, cy, "driftwood")
    meshes = [unreal.load_asset(p) for p in DRIFTWOOD_MESHES]
    xf = []
    i = 0
    while i < len(shoreline_segments):
        x, y, t, curv, zw = shoreline_segments[i]
        # Elternpunkt alle 150–600 m; bevorzugt Außenbogen (|curv| hoch), Stil-Entscheidung
        if abs(curv) > 0.004 and rng.random() < 0.5:
            for _ in range(rng.randint(2, 6)):
                off  = rng.uniform(100, 600)                    # 1–6 m landwärts
                nx, ny = -math.sin(t), math.cos(t)
                yaw  = math.degrees(t) + (rng.gauss(0, 20) if rng.random() > 0.2 else rng.gauss(90, 15))
                z    = zw + rng.uniform(30, 150)                 # 0,3–1,5 m über Normalwasser (Höhe aus Raster übernehmen)
                dia  = 40.0
                z   -= rng.uniform(0.2, 0.4) * dia               # 20–40 % eingesunken
                xf.append(unreal.Transform(unreal.Vector(x + nx * off, y + ny * off, z),
                                           unreal.Rotator(rng.gauss(0, 4), yaw, rng.gauss(0, 8)),
                                           unreal.Vector(1, 1, 1)))
            i += int(rng.uniform(150, 600) / 2)
        else:
            i += 1
    if xf:
        actor = find_or_spawn_cell_actor(f"SHORE_driftwood_X{cx:04d}_Y{cy:04d}_{VERSION}", f"Shore/Cells/X{cx:04d}_Y{cy:04d}")
        ism = make_ism(actor, meshes[0], 30000, 60000, cast_shadow=True)
        ism.clear_instances()                                   # ?
        ism.add_instances(xf, False, True)                      # OK

# ---------- Nassufer: Variante A (Landscape-Material-Parameter) ----------
def set_wet_shore_material_params(landscape_mic_path, wlevel_texture_path):
    mic = unreal.load_asset(landscape_mic_path)
    MEL = unreal.MaterialEditingLibrary
    MEL.set_material_instance_scalar_parameter_value(mic, "WetBandHigh", 60.0)   # ? Name der Funktion Standard, Parameter projektseitig
    MEL.set_material_instance_scalar_parameter_value(mic, "WetBandLow", -40.0)   # ?
    MEL.set_material_instance_scalar_parameter_value(mic, "WetRoughnessMul", 0.35)  # ?
    # Textur-Parameter 'WaterLevelMap' (Wasserspiegel cm, 16 bit, 8–32 m/px) setzen: Textur-Variante in dir(MEL) suchen
    MEL.update_material_instance(mic)                           # ?

# ---------- Nassufer: Variante B (RVT-Quads als Fallback) ----------
def make_rvt_wet_quads(cx, cy, quads, plane_mesh, vt_material):
    """quads: Liste unreal.Transform entlang der Uferlinie; plane_mesh NICHT-Nanite; vt_material = Virtual-Texture-Domain."""
    actor = find_or_spawn_cell_actor(f"SHORE_wetquad_X{cx:04d}_Y{cy:04d}_{VERSION}", f"Shore/Cells/X{cx:04d}_Y{cy:04d}")
    ism = make_ism(actor, plane_mesh, 0, 0, cast_shadow=False)
    ism.set_material(0, vt_material)                            # ?
    ism.set_editor_property("runtime_virtual_textures", [unreal.load_asset(RVT_ASSET)])        # ? Property-Name
    ism.set_editor_property("virtual_texture_render_pass_type",
                            unreal.RuntimeVirtualTextureMainPassType.NEVER)                     # ? Enum/Name
    ism.clear_instances()                                       # ?
    ism.add_instances(quads, False, True)                       # OK

# ---------- Wasser-Material-Instanz ----------
def set_river_material(mic_path):
    """mic_path: Projekt-Kopie von /Water/Materials/WaterSurface/Water_Material_River (OK: Pfad in Engine-Quellen belegt).
    Parameternamen der Instanz sind UNVERIFIZIERT – im Editor am Material nachsehen."""
    mic = unreal.load_asset(mic_path)
    MEL = unreal.MaterialEditingLibrary
    MEL.set_material_instance_scalar_parameter_value(mic, "Opacity", 0.45)   # ? Name
    # Vektorparameter (z. B. 'Absorption', 'Scattering' laut Drittskript, Skala unklar): Vektor-Variante in dir(MEL) suchen
    MEL.update_material_instance(mic)                           # ?

# ---------- Flussdaten direkt aus Water-Bodies (Alternative zum Raster) ----------
def river_flow_samples():
    out = []
    for a in EAS.get_all_level_actors():                        # OK
        if isinstance(a, unreal.WaterBodyRiver):                # OK (5.6-Doku)
            wbc = a.get_editor_property("water_body_component") # OK
            spl = wbc.get_water_spline()                        # OK
            n   = spl.get_number_of_spline_points()             # ? (SplineComponent-Standard)
            for k in range(n):
                vel = wbc.get_water_velocity_at_spline_input_key(float(k))   # OK (5.2)
                out.append((k, vel))
            # Breite/Tiefe: Spline-Metadaten (RiverWidth, Depth) – Python-Zugriff unverifiziert
    return out

# ---------- Lauf ----------
def run(cells, shoreline_by_cell):
    with unreal.ScopedEditorTransaction("Eldarien Ufer-Dressing"):     # ?
        with unreal.ScopedSlowTask(len(cells), "Ufer-Dressing") as task:  # ?
            task.make_dialog(True)
            for (cx, cy) in cells:
                task.enter_progress_frame(1, f"Zelle {cx},{cy}")
                dress_cell_stones(cx, cy)
                dress_cell_driftwood(cx, cy, shoreline_by_cell.get((cx, cy), []))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, False)  # ? OFPA-Aktorpakete speichern
```

## Empfohlene Vorgehensweise

1. **Paket inspizieren (vor allem anderen).** Content Browser mit Engine-/Plugin-Content öffnen, Coast-&-Dunes-Ordner aufnehmen: Decal-Materialien (Domain, Blend Mode, DBuffer-Kanäle), Mesh-Nanite-Flags, LOD-Anzahl, Master-Parameter (RVT-Switch, Tiling, Wetness). Prüfung: Decal auf die Nanite-Landscape setzen, RVT-Debug-Ansicht einschalten – das Decal darf in der RVT **nicht** erscheinen; ist das so, ist Frage 1 bestätigt.
2. **Nassufer im Landscape-Material.** Wasserspiegel-Raster (16 bit, 8–32 m/px) aus den 2-m-Daten erzeugen, als Texturparameter einbinden, Nässe-Term im RVT-schreibenden Zweig. Prüfung: 1–3 m dunkler Streifen entlang eines 4-m-Baches und eines 40-m-Flusses, kein Banding; Roughness unter Wasser sinkt sichtbar; Fehler „Virtual texture samples are not allowed during RVT outputs“ ggf. per Feature Switch lösen.
3. **Eine Testzelle Steine.** Skript auf einer 1-km-Zelle laufen lassen; `add_component_by_class` testen, Aktor speichern, Editor neu starten, Instanzen müssen erhalten sein. Sonst BP_ShoreISM-Fallback. Prüfung: `NaniteStats` ohne Cluster-Overflow, Log ohne „GPU-Scene Instance data overflow“, `r.Nanite.Culling.DrawDistance=1` und Cull-Kanten sichtbar.
4. **Wassermaterial.** Projekt-Kopie von `Water_Material_River`, SLW-Werte aus der Tabelle, `r.Water.SingleLayer.VSMFiltering`-Block in DefaultEngine.ini; Water Zone: HalfPrecision aus, Auflösung hoch. Prüfung: Kies in 1 m Tiefe sichtbar, 3–5 m leicht grünblau, keine blockigen Schatten.
5. **Schaum und Kaustiken.** DF-Schaum an Blöcken ≥ 50 cm; Kaustik im Bettmaterial maskiert durch Wasserspiegel. Prüfung: kein Vollflächen-Schaum (ADFL am Wasser aus).
6. **Skalieren.** Eigenes Runtime-Grid „StonesGrid“ (kleinere Zellen, kürzere Loading Range), Komponenten ≤ 15k, Streaming mit Unreal Insights (`AddToWorld`, `RegisterComponent`) profilieren, ggf. Fast Geometry Streaming auf einer Küstenzelle vergleichen.
7. **Treibholz und Hero-Decals.** Cluster-Regeln anwenden; Coast-&-Dunes-Decals nur an RVT-fernen Hero-Stellen oder als VT-Domain-Duplikat auf nicht-Nanite-Planes.
8. **RVT-Volumes.** Mehrere Volumes ≤ 4096 Tiles entlang der Flüsse; „Skip Mips“ an RVT-Quads setzen.

## Fallen und Risiken

Die DBuffer-Decals des Pakets landen nicht in RVT_Eldarien_Boden; RVT-geblendete Cliffs darüber zeigen Nähte. Mesh-Decals (translucent) funktionieren nicht auf Nanite-Meshes. Nanite-Landscape behält die Nicht-Nanite-Daten für RVT und Wasser – doppelte Streaming-Daten. UE-217644 (RVT langsam bei Nanite-Tessellation) ist für 5.8 unbestätigt; ein 5.8-Thread meldet RVT nur mit Basismaterial. Nanite-ISM-Cull-Distanzen sind quellenwidersprüchlich – testen, sonst sind Millionen Kiesel VSM-Vollkosten. Ein ISM mit 100k+ Instanzen blockiert einen Streaming-Tick; Kollision an Steinen vervielfacht das. 16,78 Mio. Instanzen sind hart; Gras und Foliage zählen mit. RVT-Quads, die World Partition ausstreamt, fehlen in Fern-Mips. Light-Function-Kaustiken gehen nicht über das Directional Light. „Shallow Water River“ (5.6) ist in 5.8 defekt. Absorption per Value-Slider schwärzt das Wasser. Python-erzeugte Komponenten werden möglicherweise nicht serialisiert. Die Python-Property heißt `enable_auto_lod_generation`, nicht `b_enable_auto_lod_generation`. Water-Zone-Grid nach Extent-Änderung zweimal rebuilden. Nanite auf Landscape bricht in 5.6 Landscape-Spline-Meshes (Position Precision/Skirt) – relevant, falls das Pack-Flussblueprint Landscape-Splines nutzt.

## Offene Punkte / Rückfragen

Die Recherche-Agenten konnten ausschließlich Suchmaschinen-Auszüge lesen; fab.com, dev.epicgames.com, forums.unrealengine.com und youtube.com waren durch Proxy/DNS gesperrt. **Der Paketinhalt wurde nie inspiziert**: Ordner, Master-Materialien, Parameternamen, Decal-Blend-Mode, Nanite-Flags, „Supported Engine Versions“ und Lizenz sind unbekannt; die „2 surface meshes“ sind nicht belegt. **Die Parameternamen von `Water_Material_River` sind unverifiziert** (Binär-Asset); belegt sind nur die SLW-Knoten-Eingänge, die Engine-MID-Parameter (`WaterBodyIndex`, `WaterVelocityAndHeight` u. a.) und die Pfade. **Es gibt keine Quelle für Steine/m² nach Größenklasse oder Eingrabungsanteile**; alle Dichten sind Richtwerte. Keine 5.8-Python-Dokumentation war erreichbar; `add_component_by_class`, `runtime_virtual_textures`, `virtual_texture_render_pass_type`, Landscape-Weightmap-Import per Python und Water-Spline-Metadaten-Zugriff sind offen. Der Kanalaufbau der Water-Info-Textur ist aus Engine-Quellen ≥5.5 belegt, die 5.8-Version wurde nicht diffgeprüft. Rückfragen: Ist das Landscape-Material RVT-getrieben (sampelt es seine Ausgabe aus RVT_Eldarien_Boden)? Wird Nanite-Tessellation auf der Landscape genutzt? Soll das Pack-Flussblueprint neben Epic-Water überhaupt eingesetzt werden? Welche Zielplattform (die Budget-Notizen gingen von RX 7900 XTX aus)?

## Quellen

**Coast & Dunes / NatureManufacture**
- Fab-Listing Coast & Dunes: https://www.fab.com/listings/15697157-fccc-45dc-8e23-2897ece19c99
- Fab Forest: https://www.fab.com/listings/11479aa9-a0bb-4292-80b7-1033c48df94c
- Fab Mountain: https://www.fab.com/listings/9ec7df30-3347-4056-8933-6156d983b0cf
- naturemanufacture.com Coast & Dunes: https://naturemanufacture.com/coast-dunes-environment-dynamic-nature/
- YouTube Promo: https://www.youtube.com/watch?v=OQj1LpL4t14 ; Tutorial: https://www.youtube.com/watch?v=87vuoLKz4DE ; 5.6 Water: https://www.youtube.com/watch?v=81RaQ5eIC00

**Epic-Dokumentation**
- Decal Materials: https://dev.epicgames.com/documentation/en-us/unreal-engine/decal-materials-in-unreal-engine
- Decal Actors: https://dev.epicgames.com/documentation/en-us/unreal-engine/decal-actors-in-unreal-engine
- Nanite Virtualized Geometry: https://dev.epicgames.com/documentation/unreal-engine/nanite-virtualized-geometry-in-unreal-engine
- Nanite Technical Details: https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-technical-details
- Using Nanite with Landscapes: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-nanite-with-landscapes-in-unreal-engine
- Runtime Virtual Texturing: https://dev.epicgames.com/documentation/en-us/unreal-engine/runtime-virtual-texturing-in-unreal-engine ; Quick Start: https://dev.epicgames.com/documentation/en-us/unreal-engine/runtimevirtual-texturing-quick-start-in-unreal-engine ; 4.27: https://docs.unrealengine.com/4.27/en-US/RenderingAndGraphics/VirtualTexturing/Runtime
- Virtual Texture Memory Pools: https://dev.epicgames.com/documentation/unreal-engine/virtual-texture-memory-pools-in-unreal-engine
- Custom Heightmaps and Layers: https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-and-using-custom-heightmaps-and-layers-in-unreal-engine
- Landscape Patch: https://dev.epicgames.com/documentation/unreal-engine/landscape-patch-system
- Virtual Shadow Maps: https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine
- Mesh Distance Fields: https://dev.epicgames.com/documentation/en-us/unreal-engine/mesh-distance-fields-in-unreal-engine
- Lumen: https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
- ISM Component: https://dev.epicgames.com/documentation/en-us/unreal-engine/instanced-static-mesh-component-in-unreal-engine
- Foliage Mode: https://dev.epicgames.com/documentation/unreal-engine/foliage-mode-in-unreal-engine
- PCG Node Reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine
- Single Layer Water: https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine
- UE 5.5 Release Notes: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-5-release-notes ; 5.8: https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes
- Python unreal.Actor: https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/Actor ; ISM 5.3: https://docs.unrealengine.com/5.3/en-US/PythonAPI/class/InstancedStaticMeshComponent.html ; PrimitiveComponent 5.3: https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PrimitiveComponent?application_version=5.3 ; WaterBodyComponent 5.2: https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyComponent?application_version=5.2 ; DecalComponent: https://docs.unrealengine.com/en-US/PythonAPI/class/DecalComponent.html ; SplineMeshComponent 5.3: https://docs.unrealengine.com/5.3/en-US/PythonAPI/class/SplineMeshComponent.html ; Landscape 5.4: https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/Landscape?application_version=5.4
- UE-217644: https://issues.unrealengine.com/issue/UE-217644 ; UE-263182: https://issues.unrealengine.com/issue/UE-263182
- Roadmap VSM: https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/1166-virtual-shadow-maps ; FastGeo: https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/2022-fast-geometry-streaming-plugin-experimental- ; UE 5.6 News: https://www.unrealengine.com/news/unreal-engine-5-6-is-now-available

**5.6-Doku-Spiegel und Engine-Quellen (GitHub)**
- SLW-Doku 5.6: https://github.com/ReduxST/UE5.6-Markdown-Docs/blob/73fd2bd6d444820f2acbc81878f685c0482524d5/Designing_Visuals,_Rendering,_and_Graphics/Materials/Material_Properties/Shading_Models/Single%20Layer%20Water%20Shading%20Model.md
- Water Meshing 5.6: https://github.com/ReduxST/UE5.6-Markdown-Docs/blob/73fd2bd6d444820f2acbc81878f685c0482524d5/Building_Virtual_Worlds/Water_System/Water%20Meshing%20System%20and%20Surface%20Rendering.md
- Light Functions 5.6: https://github.com/ReduxST/UE5.6-Markdown-Docs/blob/73fd2bd6d444820f2acbc81878f685c0482524d5/Building_Virtual_Worlds/Lighting_the_Environment/Direct_Lighting/Light%20Functions.md
- WaterEditorSettings.cpp: https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Editor/Private/WaterEditorSettings.cpp
- WaterZoneActor.h: https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Public/WaterZoneActor.h
- WaterInfoRendering.cpp: https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Private/WaterInfoRendering.cpp
- WaterBodyComponent.h: https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Public/WaterBodyComponent.h
- WaterSplineMetadata.h: https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Public/WaterSplineMetadata.h
- WaterBodyRiverComponent.h: https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Plugins/Experimental/Water/Source/Runtime/Public/WaterBodyRiverComponent.h
- SingleLayerWaterRendering.cpp: https://github.com/orgitcog/u9n/blob/97a2175ec82798dc0e55e679c738b2fb7c773bdf/Engine/Source/Runtime/Renderer/Private/SingleLayerWaterRendering.cpp
- NaviSense Ocean-Skript: https://github.com/LemuelHornsby/NaviSense ; Kitchen-Water-Skript: https://github.com/kagura-yami/AGift4MyYoungerSelf ; voxelsim: https://github.com/mnoles1911/voxelsim ; ue-mcp #1156: https://github.com/db-lyon/ue-mcp/issues/1156 ; TerraPrime #8: https://github.com/OrchidIsle/TerraPrimePlugin/issues/8 ; ibbles VSM: https://github.com/ibbles/LearningUnreal/blob/main/Virtual%20Shadow%20Maps.md

**Epic-Forum**
- Mesh decals and Nanite: https://forums.unrealengine.com/t/mesh-decals-and-nanite/1359353
- Decals affecting landscape displacement: https://forums.unrealengine.com/t/decals-affecting-landscape-displacement/2195439
- RVT not working with Nanite meshes: https://forums.unrealengine.com/t/rvt-is-not-working-with-nanite-enabled-meshes/1927428
- RVT only base color (5.8): https://forums.unrealengine.com/t/runtime-virtual-texture-only-outputs-landscape-base-color-instead-of-painted-landscape-layers-ue-5-8/2739603
- RVT and Landscape Material: https://forums.unrealengine.com/t/problem-with-runtime-virtual-textures-and-landscape-material/2049913 ; https://forums.unrealengine.com/t/virtual-texture-and-runtime-virtual-texture-in-landscape/2661222
- RVT broken with displacement (5.6): https://forums.unrealengine.com/t/runtime-virtual-texture-is-broken-if-displacement-is-used-in-a-landscape-material-currently-using-5-6/2663851
- Nanite breaks landscape splines (5.6): https://forums.unrealengine.com/t/nanite-on-landscape-breaks-landscape-spline-meshes-on-5-6/2701969
- Draw in main pass: https://forums.unrealengine.com/t/virtual-texture-draw-in-main-pass/666436
- Landscape wetness: https://forums.unrealengine.com/t/how-to-get-water-to-affect-landscape-wetness/414538
- Instance limit 16M: https://forums.unrealengine.com/t/instance-limit-16m-debugging/2688178 ; GPU-Scene overflow: https://forums.unrealengine.com/t/gpu-scene-instance-data-overflow-detected-reduce-instance-count-to-avoid-rendering-artifacts/2666774 ; Nanite overflow: https://forums.unrealengine.com/t/nanite-overflow-error-in-packaged-build-5-3/1325562
- World Partition streaming performance: https://forums.unrealengine.com/t/world-partition-streaming-performance/2577446
- RVT write cost: https://forums.unrealengine.com/t/how-mu-h-cost-write-in-rvt/266509
- PCG river splines: https://forums.unrealengine.com/t/pcg-graph-not-recognising-all-the-river-splines-in-my-scene/2672967
- Python add component: https://forums.unrealengine.com/t/editor-python-script-how-to-add-component-to-actor/1039923 ; https://forums.unrealengine.com/t/add-component-by-python/143662
- Water foam: https://forums.unrealengine.com/t/water-plugin-in-ue5-does-anyone-know-how-to-use-the-foam-on-rivers-see-video-linked/688819 ; Shallow water 5.8: https://forums.unrealengine.com/t/shallow-water-plugin-not-working-in-5-8/2763339
- Realistic water shader: https://forums.unrealengine.com/t/actually-realistic-water-shader/141661 ; Absorption/Value: https://forums.unrealengine.com/t/changing-water-material-color-value-breaks-it/1227565 ; River color: https://forums.unrealengine.com/t/water-plugin-cant-change-river-color/2571248 ; Blocky shadows: https://forums.unrealengine.com/t/blocky-shadows-on-single-layer-water/1151034 ; Water Content: https://forums.unrealengine.com/t/where-is-the-water-content-listed-in-the-official-unreal-engine-documentation/2550316

**Community / Drittquellen**
- blog.rime.red Decal-Optimierung: https://blog.rime.red/unreal-static-mesh-and-decal-optimisations/
- Polycount Landscape-Sampler: https://polycount.com/discussion/102539/limited-number-of-textures-on-a-landscape-compnent
- Cyanilux Shoreline: https://www.cyanilux.com/tutorials/shoreline-shader-breakdown/
- gamedevcore PCG: https://www.gamedevcore.com/blog/ue5-pcg-tutorial-procedural-generation
- CVar-Wiki r.Nanite.Culling.DrawDistance: https://indxzero.github.io/ue544cvarwiki/articles/r.nanite.culling.drawdistance/
- Tom Looman 5.6: https://tomlooman.com/unreal-engine-5-6-performance-highlights/ ; 5.8: https://tomlooman.com/unreal-engine-5-8-performance-highlights/
- StraySpark WP: https://www.strayspark.studio/blog/ue5-world-partition-deep-dive-streaming-hlod ; VSM 5.7: https://www.strayspark.studio/blog/virtual-shadow-map-optimization-open-worlds-ue5-7
- PerfGuard VSM: https://getperfguard.com/tutorials/virtual-shadow-maps
- 80.lv Nimue: https://80.lv/articles/how-to-build-stylized-water-shader-design-implementation-for-nimue
- iby-z DF foam: https://iby-z.blogspot.com/2019/05/distance-field-water-foamflow-maps.html ; Gumroad-Notizen: https://noro.gumroad.com/l/HEppY
- WoLD SLW-Pool: https://www.worldofleveldesign.com/categories/ue5/single-layer-water-pool-still.php
- Medium Cheap Caustics: https://medium.com/hri-tech/cheap-water-caustics-in-ue4-ee1d3ac0cae1 ; MrTapa: https://threadreaderapp.com/thread/1170897412103299077.html
- unrealdirective Refraction.DepthCulling: https://unrealdirective.com/resources/console-variables/r-water-singlelayer-refraction-depthculling/

**Geomorphologie**
- Gravel fabric braided stream (IAS): https://repository.ias.ac.in/67306
- Rust 1972 (SEPM): https://archives.datapages.com/data/sepm/journals/v42-46/data/042/042002/0384.htm
- Julien & Anthony (IAHR): https://iahr.org/library/info?pid=5624
- Berkeley Strawberry Creek 1994: https://creeks.berkeley.edu/sites/default/files/publications/1994.sc.sfc.bedsize.morley.pdf ; USGS SIR 2011-5041: https://pubs.usgs.gov/sir/2011/5041/section5.html
- Abbe & Montgomery 1996: https://archive-wpg.forestry.oregonstate.edu/sites/wpg/files/bibliopdfs/01_Brauderick%26Grant.pdf ; NSF PAR Colorado jams: https://par.nsf.gov/servlets/purl/10342965 ; Masaryk Univ. 958160: https://www.muni.cz/en/research/publications/958160 ; GSA 2005: https://gsa.confex.com/gsa/2005CD/webprogram/Paper85754.html
