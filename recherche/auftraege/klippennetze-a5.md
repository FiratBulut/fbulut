# Auftrag 04: Nanite-Klippennetze statt flacher Wandplatten (Küste A5/B5), Import- und Setz-Workflow für UE 5.8.3

Kontext: Eldarien, Unreal Engine 5.8.3, World Partition (1-km-Zellen), Nanite-Landschaft 1-m-Raster, Runtime Virtual Texture `RVT_Eldarien_Boden`
(Basecolor/Normal/Roughness + World Height). Unsere Felswände an der Nordküste (Felder A5/B5, Nordic-Biom) bestehen aus eigenen „Wandmodulen“
(Static-Mesh-Platten, Material `MI_EL_Berg_*`), die im Bild wie flache Platten wirken. Vorbild: Witcher 3 Next-Gen Skellige-Klippen (geschichtet,
halb eingegraben, Moos obenauf). Eine erste Recherche nennt als kostenlose Kandidaten die Megascans-3D-Klippen „Massive Nordic Coastal Cliff“
(15×21×15 m), „Huge Nordic Coastal Cliff“ (8,5×14×9 m) und „Desert Western Cliff Layered XL 14“ sowie Brushify Cliffs Pack (Fab).

Wir setzen alles per Editor-Python (`unreal`-Modul) und können Static Meshes importieren, Akteure setzen, Foliage-Instanzen schreiben.

**Frage 1 – Import:** Wie kommen Fab/Megascans-3D-Klippen in UE 5.8.3 sauber ins Projekt (Fab-Plugin „Add to project“ vs. Download + Interchange-Import
per Python)? Bekommen sie automatisch Nanite? Welche Importeinstellungen (Nanite an, Fallback-Prozent, Lightmap aus, Kollision „Complex as simple“ vs.
konvexe Hülle, LOD) sind für 10–25 m große Klippen richtig? Speicherkosten pro Klippe (Nanite-Daten, 8K-Texturen → Pool 8 GB)? Python-Beispiel
(`unreal.AssetImportTask`/Interchange, `NaniteSettings`, `BodySetup`).

**Frage 2 – Setzen und Verschmelzen:** Bewährte Regeln, damit gesetzte Klippennetze nicht wie „aufgestellte Steine“ wirken: Eingrabtiefe (20–40 %?),
Neigung zur Hangrichtung, Gruppierung (2–5 Netze, Größenstaffelung), Überlappung, Drehung um die Z-Achse, Skalierungsbereich ohne sichtbares
Texturstretching. RVT-Verschmelzung: Material der Klippe liest RVT-Basecolor/World-Height am Fuß (Blend-Höhe, Normal-Blend) – wie baut man das
Material (Knoten, Beispiele von Epic: Electric Dreams, Valley of the Ancient, Brushify)? Moos/Schnee-Auflage über Welt-Normal (Up-Vector-Maske)
im Material statt extra Netzen – Standardknoten dafür?

**Frage 3 – Performance/Streaming:** Klippen als einzelne Static-Mesh-Akteure je World-Partition-Zelle vs. Instanced Static Mesh (ISM) vs. Foliage
(HISM) für Nanite: was empfiehlt Epic für 5.8 (Nanite braucht kein HISM-Culling)? HLOD für Nanite-Netze in World Partition (HLOD-Layer-Einstellung,
„Instancing“ vs. „Merged Mesh“), damit Klippen aus 2–5 km Entfernung sichtbar bleiben. Kollision: Nanite-Fallback-Mesh vs. einfache Kollision,
Kosten bei 200–500 Klippen pro Zelle.

**Frage 4 – Lücken füllen:** Übergang Klippe → Landschaft (Schutt/Geröll-Decals, kleine Felsen als Foliage, Landschaftslage „Fels“ unter der Klippe
anheben). Welche Decal-Technik (Mesh-Decals, DBuffer) läuft mit Nanite + RVT in 5.8?

Antwort bitte als kompakter deutscher Bericht mit Quellen (Epic-Doku 5.6–5.8, Foren, Talks), konkreten Zahlen und einem Python-Skelett für
Import + Setzen. Ergebnis als Datei `recherche/antworten/klippennetze-a5.md`.
