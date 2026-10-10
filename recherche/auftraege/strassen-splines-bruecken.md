# Auftrag 07: Straßen als Landscape-Splines und Brücken per Python in UE 5.8.3

Kontext: Eldarien, UE 5.8.3, World Partition (1-km-Zellen, 266 Landschaftsteile), Nanite-Landschaft 1-m-Raster, RVT-Boden. Heute: 35 Wegnetze
liegen als Landschafts-Lage „Weg“ mit Material `MI_EL_Strasse_<biom>` (Material-Master V2) – also nur als bemalte Bodenlage, ohne Spline-Geometrie,
ohne Brücken. Daten offline: Wege als Polylinien (JSON, 1-m-Raster), Breite, Biom; Flussquerungen bekannt (Schnittpunkte Weg × Flussband).
Alles per Editor-Python (`unreal`-Modul), nicht von Hand. Ziel-Look: Witcher 3 (Lehmwege mit Spurrillen, Pfützen, Kies, Steinkanten in Dörfern,
Holz- und Steinbrücken, Furten).

**Frage 1 – Landscape Splines per Python:** Lassen sich Landscape-Splines (Control Points, Segments, Mesh-Zuordnung, Breite, Falloff, Layer-Paint
„Weg“, Terrain-Anpassung „Raise/Lower“) in 5.8 per Python anlegen (`LandscapeSplinesComponent`, `LandscapeSplineControlPoint`, `LandscapeSplineSegment`,
Editor-Subsystem/Blueprint-Funktionen wie `add_spline_control_point`/`add_spline_segment`, World-Partition-Besonderheit „Landscape Spline Actors“
in 5.1+)? Welche Funktionen sind exponiert, was fehlt (Forum-/Doku-Belege 5.3–5.8), Workarounds (Blueprint-Funktionsbibliothek, Editor Utility)?
Alternative: Spline-Mesh-Straßen (eigener Spline-Actor + `SplineMeshComponent`) mit RVT-Blend ins Gelände – Vor-/Nachteile, Nanite-Spline-Meshes
(`r.Nanite.AllowSplineMeshes`), Kollision.

**Frage 2 – Straßen-Look:** Material-Aufbau für Lehm-/Kieswege mit Spurrillen (Tiling entlang der Spline-U-Koordinate), Pfützen (Wetness-Maske),
Rand-Blend über RVT, Decals für Spurrillen/Kies; Beispiele aus Fab-Paketen (Brushify Roads, NatureManufacture „Roads“, Meadow-Set Wege) und was
davon in UE 5.8 mit Nanite-Landschaft funktioniert.

**Frage 3 – Brücken:** Regeln für Platzierung (Spannweite vs. Flussbreite, Höhe über Wasserspiegel, Widerlager im Ufer), modulare Brücken-Assets
(kostenlos: Pierogi3 „Medieval Stone Bridge – Nanite“, Fab-ID 4c64ce34-195b-4b45-8e14-70273cc984b5; Meshingun Village; Hivemind Docks), Spline-Brücken
(Blueprint mit Spline-Mesh-Segmenten), Furten statt Brücken bei Bächen. Python-Skelett: Brücke aus 2 Uferpunkten + Wasserhöhe setzen, Gelände unter
den Widerlagern anpassen, Kollision/Navigation.

**Frage 4 – Dörfer-Anschluss (später):** Wie binden Epic-/Fab-Beispiele (City Sample, Project Titan) Straßen an Gebäude-Kits (Hivemind Medieval Town)?
Nur Überblick.

Antwort bitte als kompakter deutscher Bericht mit Quellen, API-Liste (was in 5.8 per Python geht) und Python-Skelett. Ergebnis als Datei
`recherche/antworten/strassen-splines-bruecken.md`.
