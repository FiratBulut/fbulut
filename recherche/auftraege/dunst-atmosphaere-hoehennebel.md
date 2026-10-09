# Auftrag 05: Luftperspektive wie Witcher 3 – „Sky Atmosphere affects Height Fog“ in UE 5.8.3 sauber einführen

Kontext: Eldarien, UE 5.8.3, Open World 9,6 × 7 km, Meeresspiegel = 0, Berge bis ~900 m. Licht: Directional Light 24° Höhe, 5900 K;
Sky Atmosphere (Aerial Perspective View Distance Scale 3, Mie Scattering Scale 0,006); Exponential Height Fog (Dichte 0,006–0,009, Height Falloff
0,05–0,12, Volumetric Fog an, Volumetric Fog Distance 150–200 m); Lumen, Virtual Shadow Maps. Ziel: der blau-weiße Fernedunst der Witcher-3-Next-Gen-
Bilder (Ferne Bergwände hell und bläulich, Nähe klar, warmes Licht gegen kühle Schatten), auch von Kameras aus, die 400–600 m hoch stehen.

Eine erste Recherche empfiehlt: Projekteinstellung „Support Sky Atmosphere Affecting Height Fog“ an, Fog Inscattering Color und Directional Inscattering
Color = Schwarz, Stärke über „Height Fog Contribution“ (Sky Atmosphere), Fog Density 0,003–0,006, Height Falloff 0,02–0,05.

**Frage 1:** Was genau löst die Projekteinstellung aus (Config-Schlüssel in `DefaultEngine.ini`, `r.SupportSkyAtmosphereAffectsHeightFog`)?
Werden alle Materialien neu übersetzt oder nur globale Shader? Editor-Neustart nötig? Gibt es Berichte zu Dauer/Risiken bei großen Projekten
(mehrere tausend Materialien)? Nebenwirkungen auf Volumetric Fog, Lumen-Himmelslicht, Wasser (Epic Water Plugin, Single Layer Water)?

**Frage 2:** Wie verhält sich der Höhennebel bei Kameras hoch über dem Nebel-Akteur (Formel `FogDensity * 2^(-HeightFalloff * dz)`): empfohlene
Kombination aus Nebelhöhe (Akteur-Z), Dichte, Falloff und „Second Fog“ (Talnebel) für Welten mit 0–900 m Höhenunterschied? Beispielwerte aus
Epic-Projekten (Project Titan, Electric Dreams, Valley of the Ancient, City Sample) – konkrete Zahlen, wenn auffindbar.

**Frage 3:** Alternative ohne Projekteinstellung: „Inscattering Color Cubemap“ des Höhennebels (Sky-Cubemap, Capture) und „Directional Inscattering“
– Qualität, Kosten, Grenzen? Local Fog Volumes (5.4+) für Täler vs. Second Fog?

**Frage 4:** Farbgebung Witcher/Dragon-Age-artig: wie färbt man den Fernedunst leicht violett-blau und die Luft warm, ohne die Nähe zu waschen
(Post Process: Color Grading Shadows/Highlights, Lumen Skylight Tint, Sky Atmosphere Rayleigh/Mie-Absorption)? Werte mit Quellen.

Antwort bitte als kompakter deutscher Bericht mit Quellen und einer Schritt-Liste (Reihenfolge, Risiken, Prüfbilder bei 300 m / 1 km / 3 km).
Ergebnis als Datei `recherche/antworten/dunst-atmosphaere-hoehennebel.md`.
