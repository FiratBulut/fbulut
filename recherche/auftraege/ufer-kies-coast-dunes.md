# Auftrag 06: Ufer und Flussbett wie Witcher 3 – Kies, Steine, Nassufer mit dem Coast-&-Dunes-Paket in UE 5.8.3

Kontext: Eldarien, UE 5.8.3, World Partition (1-km-Zellen), Nanite-Landschaft (1-m-Raster, 22 Lagen, Runtime Virtual Texture `RVT_Eldarien_Boden`
mit Basecolor/Normal/Roughness + World Height), Flüsse/Seen/Bäche/Teiche sind Epic-Water-Körper (Water-Plugin, Flussbreite 4–40 m, 101 Bäche,
53 Seitenarme, 13 Teiche). Daten offline: Uferlinien/Breiten/Wasserhöhe als JSON und 2-m-Rasterkarten (Wasserband, Wasserspiegel, Höhen).
Alles wird per Editor-Python gesetzt (Akteure, Foliage-Instanzen, Decals), nicht von Hand.

Installiert, aber ungenutzt: NatureManufacture „Coast & Dunes – Environment Set“ (UE 5.5–5.8): 14 Decals (Nassufer, Lehm, Fels, Kiesel, Sand),
2 Flächen-Netze (Fels, Lehm), 9 Treibholzstämme, 85 Bodentexturen in 28 Sets (Kiesel/Lehm/Steine), Fluss-Spline-Blueprint, Spline-Klippen.
Dazu Megascans-3D-Assets im Projekt: NordicBeachRocks, SmallStonesPack, DryRiverBed, BeachSandWithPebbles, Decals ScatteredSticksAndTwigs.
Ziel-Look (Witcher 3 Next-Gen): klares Wasser mit sichtbaren Steinen im Bett, Kies- und Felsufer, nasse dunkle Uferzone, Treibholz, Schilf/Gras bis ans Wasser.

**Frage 1 – Aufbau des Pakets:** Wie sind die Coast-&-Dunes-Decals und Flächen-Netze technisch gebaut (Decal-Typ: DBuffer-Decal, Mesh-Decal,
RVT-Decal? Material-Domain, Blend-Modus, Nanite?), wie werden sie laut Hersteller an Ufern eingesetzt, und wie verhalten sie sich auf einer
Nanite-Landschaft mit RVT in 5.8 (bekannte Fallen: DBuffer-Decals landen nicht im RVT; Mesh-Decals dürfen nicht Nanite sein)? Bitte Doku-/Forum-Belege
und die Asset-Namen (Ordnerstruktur im Paket, Material-Master, Parameter wie Wetness/Tiling).

**Frage 2 – Ufer-Pipeline per Skript:** Empfohlener Ablauf für ~250 km Uferlinie: (a) Nassufer-Streifen 1–3 m als RVT-Decal (Material mit
Virtual-Texture-Domain, „Draw in Main Pass = Never“) entlang der Uferlinie – als Spline-Mesh, als ISM-Planes oder als Landscape-Lage
(Lage „Nassufer“ in der Lagen-Blendung, dunkler/glänzender)? Welche Variante ist in 5.8 am stabilsten und billigsten? (b) Kies/Steine im Bett
und am Ufer als Nanite-ISM (PCG Surface Sampler + Water-Spline-Abstand, oder eigene Python-Platzierung aus der 2-m-Karte): Dichten
(Steine/m²), Größenstaffelung, Eingraben, Ausrichtung zur Strömung, Cull-Distanzen; (c) Treibholz/Stämme an Prallufern: Regeln.
Mit Python-Skelett (unreal-Modul: ISM-Komponenten, Decal-Actor/Spline-Mesh, Material-Parameter).

**Frage 3 – Wasser-Material:** Epic-Water-Flussmaterial so einstellen, dass das Bett sichtbar bleibt (Tiefenfärbung/Absorption, Roughness,
Schaum an Steinen über Distance Field, Unterwasser-Caustics): Parameter-Namen und Wertebereiche in 5.8, Beispiele aus Epic-Demos/Foren.

**Frage 4 – Performance:** Decals/ISM-Steine für 250 km Ufer in World Partition: Streaming-Kosten, HLOD für kleine Steine (aus), Grenzen (GPU-Scene
Instanzen), RVT-Seitenbudget.

Antwort bitte als kompakter deutscher Bericht mit Quellen und Python-Skelett. Ergebnis als Datei `recherche/antworten/ufer-kies-coast-dunes.md`.
