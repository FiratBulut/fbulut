# Bildkritik: 17 Editor-Screenshots gegen die Witcher-Messlatte

**Projekt:** Eldarien (UE 5.8.3, 9,6 × 7 km Nanite-Landscape, Lumen, VSM, Epic Water, alles per Editor-Python). **Stand:** 2026-10-10. **Messlatte:** witcher_01–07 (W3 Next-Gen und W4-UE5-Techdemo). **Methode:** Alle 7 Zielbilder und alle 17 Ist-Bilder wurden einzeln betrachtet; die Maßnahmen stützen sich, wo möglich, auf die fünf vorhandenen Rechercheberichte (siehe Quellen). Zahlen ohne Beleg sind als **Richtwert** markiert.

---

## 1. Kurzfazit

Das Muster über alle 17 Bilder ist dasselbe: **jede Fläche trägt genau einen Maßstab.** Der Berg ist eine Kachel (V16) plus eine gleichmäßig gestreute Schicht gleich großer Felsschalen; der Wald ist eine Kiefernart in einem Abstand und einer Höhe; der Waldboden ist eine Laubtextur plus gleich große grüne Sprösslinge; das Wasser ist eine Fläche mit einer harten Kante. Die Witcher-Bilder bauen jede Fläche dagegen aus drei bis vier ineinandergreifenden Größenstufen (witcher_06: Felswand → Hausgroße Blöcke → Kopfsteine → Schnee in Rissen; witcher_07: Fichten dunkel, Lärchen rostrot, Mischhöhen, Nebelbänder dazwischen) und aus Makro-Variation im 100–500-m-Maßstab (Farbbänder, Rinnen, Lichtungen). Zweitens ist das Licht in fast allen Ist-Bildern Mittagslicht aus hohem Winkel: keine Warm-Kalt-Trennung, Schatten grau statt blau, kein Gegenlicht; die Witcher-Bilder stehen alle in tiefem Seitenlicht oder Gegenlicht mit kühlem Dunst dahinter. Drittens fehlen Übergänge (Fels→Gras in harten Dreiecken, Wasser→Ufer als weiße Linie, Fels→Boden ohne Eingraben). Viertens gibt es vier harte Fehler, die vor jeder Ästhetik zu beheben sind: schwebende Felsschalen (BERG8_A5), ein schwarzer Placeholder-Würfel (NORD3_D3), ein polygonaler Wolkenschatten (BACH3_G5) und die weiße Kantenlinie an allen Fließgewässern.

**Der eine wichtigste Hebel** ist eine **Makro-Variation im Landscape-Material** (Kopie plus wenige Nodes): ein world-aligned Großnoise (200–800 m) auf Albedo-Tint und Rauheit, eine noise-gestörte Hangneigungsmaske für den Fels/Gras-Übergang und ein Distanz-Tile-Break für V16. Das trifft 12 der 17 Bilder, kostet keine neuen Assets und keinen Speicher nennenswert. Unmittelbar dahinter steht der Licht-/Dunst-Umbau nach dem Dunst-Bericht, weil er ohne Content-Arbeit jedes Bild gleichzeitig hebt.

---

## 2. Was die Witcher-Bilder durch Komposition und Kamera gewinnen – und was echte Welt-Lücken sind

**Nur Kamera und Komposition (für uns: Kamerawahl beim Screenshot):**

- **Kamerahöhe 1,5–2 m** (witcher_01, 03, 04) statt 50–500 m. Aus Bodenhöhe verschwinden Kachelwiederholung und Streu-Gleichmäßigkeit hinter Verdeckung; aus der Luft (BERG8_A5, FELS7_A4, W6FIN_G3) sieht man jedes Raster.
- **Brennweite ~35–50 mm äquivalent** (FoV ca. 45–60°); witcher_03/04 sind eher enger. Unsere Shots wirken wie 80–90° FoV: Berge werden flach, Entfernungen gestaucht.
- **Vordergrund-Rahmung in 1–3 m:** Fichtenast (witcher_03), Felskante mit Blumen (witcher_04), Figur (01, 03, 04). Kein Ist-Bild hat einen Vordergrund.
- **Horizont im oberen Drittel**, Hauptmotiv auf einer Drittellinie; bei uns liegt der Horizont oft mittig (BERG8_C2, D2, NORD3_D3, TEICH1_H5) mit 50 % Himmel.
- **Sonnenstand 10–25°, Seiten- oder Gegenlicht** (witcher_03, 04, 06): Kanten leuchten, Schatten sind lang und blau. Unsere Sonne steht 45–60° hoch (BERG8, FELS7, TEICH1); nur W6FIN_E5 hat tiefes Licht und wirkt sofort besser.
- **Tiefenschärfe/Bokeh** (witcher_03) und ein leichtes Filmgrading (Schatten kühl, Lichter warm) – reine Post-Process-Entscheidung.
- **Atmosphärische Schichtung** ist halb Kamera (Blickrichtung gegen die Sonne, drei Ebenen im Bild) und halb Welt (Nebelbänder zwischen Kämmen).

**Echte Welt-Lücken (bleiben bei jeder Kamera sichtbar):**

1. Fehlende Größenstaffelung von Fels und Geröll, keine Clusterung, kein Eingraben.
2. Keine Makro-Variation auf Landschaft: eine Kachel pro Fläche, harte Layer-Grenzen in Dreiecksform (Reste der Terrassen-Glättung).
3. Wald-Monokultur: eine Art, eine Höhe, ein Abstand, keine Lichtungen, kein Unterwuchs, keine toten Bäume, keine Farbvarianz.
4. Wasserkanten: weiße Linie, kein Nassband, keine Steine im Bett, falsche Wasserfarbe (Türkis) für Sumpf und Küste.
5. Silhouetten: Berge sind glatte Kuppeln (BERG8_D2, W6FIN_G3-Hintergrund) statt Grate und Zacken; Kämme tragen Baumreihen wie Zäune.
6. Bodenkleinzeug ohne Stufen (Zweige, Äste, Wurzeln, Moos fehlen; nur grüne Punkte).
7. Licht/Atmosphäre-Setup selbst (Farbtemperatur, Schattenfarbe, Dunst-Schichten) – kein Kameraproblem, sondern Szenen-Einstellung.

---

## 3. Bildkritik

### BERG8_C2_rundgang, BERG8_H3_rundgang, BERG8_D2_rundgang (Bergwände, V16 + Felsschalen, Dunst W6)

Gesehen: grau-beige V16-Kachel mit horizontaler Schichtung, die über die ganze Kuppel in gleicher Dichte wiederholt; dunkle Felsschalen als gleichmäßiges „Konfetti“ (C2 besonders), in H3 drei große helle Platten mitten auf der Wand ohne Bezug zur Schichtung; D2 zwei glatte Doppelkuppeln wie Dünen, rosa-grauer Dunst links; H3 Baumreihe exakt auf der Kammlinie und rotbrauner Fels rechts als harter Flächenwechsel. Licht hoch und frontal, Schatten kurz und grau.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Keine Makro-Variation, Kachel sichtbar | C2/H3: identische Schichtlinien alle ~15–20 m über die ganze Wand; D2 linker Gipfel reine Textur | Landscape-Material-Kopie: `WorldAlignedTexture`-Noise (Tiling 300–600 m, **Richtwert**) → Lerp Albedo-Tint ±15 % Helligkeit, ±10 % Sättigung Richtung Rost/Ocker; zweiter V16-Sample mit 3,7× anderem Tiling, Lerp über Distanz 80–200 m (Tile-Break); Rauheit ±0,1 über dasselbe Noise. Max. 6–8 Nodes, kein Layer, kein neuer Sampler über das Budget hinaus | 4–6 h |
| Felsschalen ohne Größenstufen und ohne Clusterung | C2: ~200 gleich große dunkle Shards gleichverteilt; H3: 3 Platten ohne Satelliten | Nach klippennetze-a5.md: Gruppen 2–5 Meshes mit einem dominanten Stück (15–25 m) + Satelliten (5–10 m) + Geröll (1–3 m, PCG), Eingraben 25–40 %, eine Schichtneigung (`strata_yaw`) pro Front, Yaw ±20°; Dichte auf 1/3 der heutigen Shard-Anzahl, dafür geclustert entlang Kanten/Rinnen (Slope > 35°, Curvature-Maske) | 8–12 h |
| Silhouette Kuppel, Licht flach | D2: Dünen-Profil, kein Grat; alle drei: Schatten grau, keine Kantenlichter | Kurzfristig: Sonne auf 18–24° Elevation, Azimut seitlich (Dunst-Bericht, Schritt 0/4); `Use Temperature` 5900 K, Shadows Gain B 1,08/R 0,95. Mittelfristig: Heightmap-Pass per Python auf den Hauptkämmen (Ridge-Noise 20–60 m Amplitude, **Richtwert**) oder 3–5 Nanite-Gratkronen als Hero-Meshes aufsetzen | 2 h (Licht) / 10–16 h (Grate) |

### BERG8_A5_rundgang (Steilwand von oben, Gras-Keile)

Gesehen: Kamera hoch, Wand fast formatfüllend; Grasflächen als grüne Keile mit Zacken-/Dreieckskanten (Terrassenreste); links eine Felsschalen-Reihe, die über die Kante hinaus **in der Luft schwebt**; die Wand selbst wieder V16 mit horizontaler Wiederholung alle ~12 m; winzige Einzelbäume ohne Gruppierung.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Schwebende Felsschalen (Fehler) | Linker Bildrand: 8–10 Shards frei über dem Meer | Platzierungsskript: Line-Trace nach unten **und** Prüfung, dass ≥ 60 % der Bounding-Box-Unterseite Terrain trifft; sonst verwerfen; Eingraben 25–40 % (klippennetze-a5.md) | 1–2 h |
| Harte, gezackte Fels/Gras-Grenze | Grüne Keile mit Dreieckszacken mitten in der Wand | Im Landscape-Material die Layer-Maske mit Slope-Maske überblenden: `smoothstep(30°, 45°)` × Noise (20–40 m), 2–3 Nodes; zusätzlich Weightmap-Pass per Python: Gras-Weight auf Slope > 40° auf 0, 5 px Blur | 3–4 h |
| Fehlende Mittelstufe (Rinnen, Schuttkegel) | Zwischen Kachel und Shards gibt es nichts im 20–100-m-Maßstab | PCG-Scree am Fuß der Keile: Normal-To-Density 0,5–1,0, Dichte 0,5–2 Steine/m² (Richtwerte, boden-kleinzeug-gras.md Schicht C); Rinnen über das Makro-Noise des Materials (Abdunklung + Rauheit) | 4–6 h |

### FELS7_B5_rundgang (Gipfel mit Felsschalen und Kiefernreihe)

Gesehen: linke Flanke grasgrün und glatt, rechte Flanke blassgrauer Fels mit hellen Platten; Kiefern sitzen exakt auf der Kammkante wie ein Zaun; Schneehaube; links rosa-violetter Dunst (W6) – der Dunst selbst ist nahe am Witcher-Ton von witcher_04/07, nur ist das Nahfeld dazu zu grau.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Baumreihe auf der Kammlinie | Kiefern folgen der Kante in einer Linie, gleiche Höhe | Baum-Scatter: Ridge-Ausschluss über Curvature (negativ = Kamm) oder Abstand zur Kammlinie 15–40 m; Clumping-Noise (50–120 m, **Richtwert**) mit 20–30 % Leerflächen; Höhenvarianz 0,7–1,3 | 4–6 h |
| Fels ohne Farb- und Rauheitsvarianz | Rechte Flanke einheitlich hellgrau, Platten gleich hell wie Wand | Macro-Noise (siehe BERG8) plus Platten-Material-Instanz dunkler (−15 % Albedo) und mit Moos-Höhenband über `WorldAlignedBlend` (klippennetze-a5.md, Moos nur Krone) | 2–3 h |
| Nahfeld zu grau gegen den Dunst | Grasflanke und Fels sitzen ohne Warm-Kalt-Trennung vor dem Violett | Dunst-Bericht Schritt 1/4: AP View Distance Scale 2 (von 3), Rayleigh R 0,25, Highlights Gain R 1,04, Saturation 1,05 (Richtwerte); Sonne tiefer | 1–2 h |

### FELS7_A4_rundgang (Felsreihen auf Terrassenstufen)

Gesehen: die problematischste Bergwand. Horizontale „Perlenketten“ aus Felsschalen auf jeder Reststufe, alle Shards ~5–10 m, gleiche Farbe wie die Kachel; dazwischen grüne Keile mit Dreieckskanten, orange Bodenflecken; Kiefern gleich groß und gleich dicht über die ganze Flanke; Licht frontal.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Felsreihen folgen den Terrassenstufen | 8–10 horizontale Reihen im gleichen Abstand, keine Lücke | Platzierung nicht nach Stufenkante, sondern nach Curvature + Noise; Reihen durch Cluster (3–7 Stücke, 15–30 m Abstand zwischen Clustern, **Richtwert**) ersetzen; Reststufen vorher mit Python-Heightmap-Glättung (Gauss 3–5 px in 1-m-Auflösung) entfernen | 6–8 h |
| Fels und Kachel gleichfarbig, keine Tiefe | Shards verschwinden im Grau der Wand | Fels-Material: RVT-Höhenblend am Fuß (BlendHeight 100–200 cm), Albedo der Shards 10–20 % dunkler und kühler als V16, Moos-Krone; VSM-Kontaktschatten werden erst bei tiefer Sonne lesbar | 3–4 h |
| Wald als gleichmäßige Streuung | Kiefern gleich groß, Abstand ~10 m, keine Gruppen, keine Totbäume | Clumping-Noise, Höhenvarianz, 10–20 % zweite Art (Birke/Lärche aus Megaplants oder gekauftem Pack per Kopie), 2–3 % Totholz-Mesh, Dichte auf Slope > 35° halbieren | 6–8 h |

### FELS6_B6_rundgang (Küstenhang nach Terrassen-Glättung)

Gesehen: Hang mit braunem Trockengras, grüne Senke, Kiefern gleichmäßig; eine helle diagonale Terrassenkante läuft noch sichtbar durch den Hang; links Klippe mit vertikal gestreckter Textur; Wasser dunkel und tot (kein Ufersaum); Kiefern gleiche Höhe.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Restterrasse als helle Linie | Diagonale Kante rechts-mitte, Layer-Wechsel folgt ihr | Heightmap-Glättung lokal; Layer-Maske mit Slope-Noise aufbrechen (siehe BERG8_A5); Kante zusätzlich mit Felsgruppe (3–5 Stück) kaschieren, nicht mit Reihe | 2–3 h |
| Vertikales Textur-Stretching an der Klippe | Linke Klippe: dunkle, gezogene Streifen | Triplanar/World-Aligned nur für den Fels-Layer (klippennetze-a5.md nennt die Alternative Tiling über Object Scale); bei Landscape: Slope-abhängiger Sample mit XZ/YZ-Projektion, 3–4 Nodes | 2–3 h |
| Ufer ohne Saum | Wasser stößt direkt an Gras, kein Nassband, kein Kies | ufer-kies-coast-dunes.md: Nässe im Landscape-Material `smoothstep(z_wasser+h_hi, z_wasser+h_lo, WorldPosition.z)`, Rauheit −0,3, Albedo −25 %; Kopfsteine 8–25 cm 1–4/m² als Nanite-ISM (Richtwerte) | 4–6 h (Material) |

### TERR3_I5_rundgang (Küstenhügel mit Teich)

Gesehen: türkisfarbenes Wasser mit weißen Flecken (Wolkenreflexion/Schaumartefakte), Kiesband grau und gleich breit; hellgrüne Laubbäume gleichmäßig bis zum Gipfel verteilt; Vordergrund flächig braun ohne Struktur; Himmel milchig hell, Licht diffus; Berg ohne Fels/Gras-Differenzierung.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Wasserfarbe Türkis, Oberfläche fleckig | Teich leuchtet wie Lagune; weiße Flecken auf der Fläche | Water_Material_Lake-Kopie: Absorption Richtung (0,006/0,003/0,002), Scattering 0,0001–0,0003, PhaseG 0,2 (ufer-kies-coast-dunes.md, Richtwerte); Reflexion prüfen: Lumen-Reflections auf Wasser, SSR-Fallback; weiße Flecken sind vermutlich Wolken-Reflexion bei zu hoher Roughness-Varianz → Normal-Stärke der Wellen halbieren | 2–3 h |
| Baumverteilung gleichmäßig bis zum Gipfel | Gleiche Lücken auf Hang und Gipfel; keine Baumgrenze | Dichte über Höhe (ab 60 % Berghöhe linear auf 0, **Richtwert**) und über Slope; Clumping; Laubbaum-Anteil in Senken, Kiefern auf Rücken | 3–4 h |
| Vordergrund ohne Boden-Struktur | Braune Fläche ohne Gras-Tiers, Steine oder Pfade | Grass Types Schicht A/B nach boden-kleinzeug-gras.md (Hero-Gras End Cull 80–100 m, Kräuter 40–60 m); Makro-Noise auf Albedo; 2–3 Felsgruppen als Anker | 3–4 h |

### NORD3_D3_rundgang (Wüsten-Canyon)

Gesehen: orange-brauner Fels mit **glänzenden** Schichtkanten (liest sich nass/plastisch), gleiche Rillenstruktur über den ganzen Rücken; verstreute dunkle Blöcke ohne Bezug zu den Rinnen; unten rechts ein **schwarzer Würfel** (Placeholder-Actor). Sonne hoch, Horizont mittig. Farbwelt an sich stimmig für den Biom-Kontrast zu Nord.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Schwarzer Würfel im Bild (Fehler) | Unten rechts, unbeleuchteter Block | Actor finden (Python: alle `StaticMeshActor` mit Default-Cube oder ohne Material in Zelle D3), löschen oder verstecken | 0,5 h |
| Fels zu glänzend | Helle Spiegelglanz-Kanten an jeder Schicht | Wüsten-Layer: Roughness 0,75–0,9, Specular 0,3–0,4 (Richtwert); Normal-Stärke 0,6; keine Nässe-Maske hier aktiv lassen | 1 h |
| Blöcke ohne Bezug zur Erosion | Felsen gleich verteilt, nicht in Rinnen/Schuttfächern | PCG/Python: Platzierung nach Flow-Akkumulation (Senken) und Fuß von Steilstufen; 3 Größenstufen; Eingraben 30 % | 4–6 h |

### W6FIN_G3_rundgang und LUFT4_G3_rundgang (Bergwald, Dunst W6 vs. W7)

Gesehen: identischer Blick, Kiefern-Monokultur in einem Grünton, roter Boden zwischen den Kronen, Waldkante hart, ferne Berge nackt und kuppelig in Rosa (W6) bzw. Braun (W7). W6 wäscht das Nahfeld milchig aus und lässt die Ebene hinten verschwinden; W7 hält Kontrast und Sättigung, der Fern-Dunst ist aber flacher und weniger blau als witcher_07. Keine Nebelbänder zwischen Kämmen, keine zweite Baumart, keine Lichtungen.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Wald-Monokultur, keine Struktur | Eine Art, eine Höhe, gleichmäßige Dichte bis zur harten Kante | Zweite/dritte Art 20–35 % (Lärche rostig, Fichte dunkel), Höhenvarianz 0,7–1,3, Clumping-Noise mit 15–25 % Lichtungen, Waldkante mit Dichte-Falloff über 30–60 m (Richtwerte); PerInstanceRandom Hue ±6 %, Value ±10 % | 8–12 h |
| Dunst: W6 milchig, W7 ohne Blau-Schichtung | W6: Nahfeld grau, Ebene weg; W7: ferner Berg braun statt blau | Dunst-Bericht: Primärschicht Density 0,0035, Falloff 0,02, Max Opacity 0,7; Second Fog Density 0,3 / Falloff 0,8 / Offset auf Talboden für Nebelbänder; Rayleigh R 0,25, Scale 0,045, Mie 0,004; AP Scale 2 (alle Richtwerte). Ziel: W7-Kontrast nah + Blauwand bei 3 km | 2–4 h |
| Ferne Berge nackt und kuppelig | Hintergrund: glatte Rosa-Hügel ohne Wald, Fels oder Grat | Kurz: Wald-Dichte in der Ferne nicht auf 0 (HLOD-Instancing-Layer aus klippennetze-a5.md), Fels-Layer auf Hängen > 30°; lang: Grat-Pass auf Heightmap | 4 h (HLOD) / 10–16 h (Grate) |

### W6FIN_E5_rundgang (Küstenwiese mit Weiden, tiefes Licht)

Gesehen: das beste Ist-Bild. Sonne tief von rechts, warmer Dunst, lange Schatten, Weiden und Kiefern gemischt. Aber: Bäume in gleichem Abstand über die ganze Ebene, keine Gruppen; Wiese ein Beige ohne hohe Gräser, Büsche oder Felsanker; Mesa hinten flach-braun ohne Schichtung oder Schatten.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Baumverteilung gleichmäßig | Weiden/Kiefern ~15 m Raster ohne Clumps | Clumping-Noise 40–100 m, Weiden nur innerhalb 20–40 m vom Wasser (Distanz-Maske aus 2-m-Raster), Kiefern in 3–7er-Gruppen | 3–4 h |
| Wiese ohne Tiers | Eine Grasfarbe, keine Hochgräser, keine Büsche, keine Steine | Grass Type Schicht A (Hero-Gras 2–4 Arten, Density 150–300) + Schicht B (Kräuter) nach boden-kleinzeug-gras.md; 1–2 Buscharten 0,02/m²; Felsgruppen alle 60–100 m (Richtwert) | 4–6 h |
| Mesa ohne Relief | Flache braune Wand, keine Schichtung, kein Schatten | Fels-Layer-Macro-Noise; 3–5 Nanite-Klippen-Hero-Stücke an der Mesa-Kante (klippennetze-a5.md Pipeline) | 4–6 h |

### KLEIN12_G3_boden (Waldboden Buche, Augenhöhe)

Gesehen: braune Laubtextur flächig, darauf gleichmäßig verteilte hellgrüne Sprösslinge in einer Größe; ein rot blühender Strauch; rechts eine große Megascans-Platte, die **auf** dem Boden liegt (keine Eingrabung, keine Laubkante, kein Moos-Übergang); keine Zweige, keine Äste, keine Wurzeln, kein Farn, kein Moos; Buchenstämme ohne Wurzelanlauf. Licht sonnig-fleckig, gut.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Kleinzeug ohne Größenstufen | Nur gleich große grüne Sprösslinge; keine Zweige/Äste | boden-kleinzeug-gras.md Schicht C: Zweige 1–3/m², Zapfen/Äste 0,2–1/m², Laubhaufen 5–15/m², kleine Steine 0,5–2/m² (Richtwerte), Nanite opak, End Cull 25–40 m; Sprösslinge auf 1/3 Dichte und geclumpt; Farn 0,1–0,3/m² in Senken | 6–8 h |
| Fels liegt auf, nicht im Boden | Platte rechts mit sichtbarer Unterkante, Textur-Hartkante | Eingraben 40–50 % (Platten), RVT-Höhenblend BlendHeight 20–60 cm am Fuß (klippennetze-a5.md); Laub-Decal (RVT-Decal) um den Fuß | 2 h |
| Bodentextur flächig, keine Feucht/Trocken-Zonen | Ein Braun überall, keine dunklen Senken | Macro-Noise auf Albedo (−20 % in Senken) und Rauheit; Moos-Layer-Anteil über Curvature (Senken) 2–3 Nodes | 2–3 h |

### KLEIN12_C4_boden (Kiefernwald mit Blumenwiese)

Gesehen: dichte beige Trockengras-Wiese mit Mohn, Kornblumen, gelben Blüten in gleichmäßiger Verteilung; Gras überall gleich hoch bis an jeden Stamm; kein Nadelstreu, keine Lücken, keine Wurzeln; Stämme ohne Bodenkontakt-Übergang. Hübsch, aber ein Gartenbild, kein Kiefernwald und nicht „dark fantasy“.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Gras-Dichte und -Höhe uniform | Kein Fleck ohne Gras, keine Höhenstufen | Grass Type: AllowedDensityRange/bWeightAttenuatesMaxScale für Übergang hoch→kurz (boden-kleinzeug-gras.md), Noise-Lücken 20–30 %, Dichte innerhalb 1,5 m um Stämme auf 20 %; Nadelstreu-Layer um Kiefern | 3–4 h |
| Blumen zu dicht und zu bunt | Mohn/Kornblume/Gelb gleichmäßig; Sättigung hoch | Blumen-Varieties auf 1/4 Dichte, geclumpt (Noise 5–15 m), Sättigung der Blüten −20 %; für Witcher-Ton 1–2 Arten mit gedecktem Rot/Violett (witcher_01: Blutweiderich-Spitzen) | 1–2 h |
| Kein Stamm-Boden-Übergang | Stämme stehen wie gesteckt | Wurzelanlauf-Meshes (Megascans Nordic-Forest-Wurzeln, boden-kleinzeug-gras.md) oder RVT-Decal „Nadelstreu“ 1,5 m um den Stamm; PerInstance-Yaw | 3–4 h |

### BACH4_C4_bach_B2_R_M1_M1_03 (Bach im Kiefernwald)

Gesehen: Bach als dünner hellblauer Streifen mit **weißer Kantenlinie** beidseitig; keine Böschung, keine Steine im Bett, kein Nassband, keine Ufervegetation, Wasser ohne sichtbaren Grund; Kiefern gleichmäßig; Boden beige-sandig mit grünen Punkten.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Weiße Kantenlinie, harter Übergang | Bach wie ein aufgeklebtes Band | Vermutlich Schaum-/Shoreline-Term der River-Instanz oder Depth-Fade zu kurz: `Water_Material_River`-Kopie, Foam-Parameter auf 0, Depth-Fade 30–60 cm; danach Nassband im Landscape-Material (ufer-kies-coast-dunes.md, Variante A) | 2–3 h |
| Bett leer, Wasser ohne Grund | Kein Stein, keine Kiesbank, Blau deckend | Absorption (0,003–0,006/0,0007–0,002/0,0003–0,001), Scattering ≤ 0,0003, Opacity < 1 am SLW-Knoten (ufer-kies-coast-dunes.md, Richtwerte); Kopfsteine 8–25 cm 1–4/m² als Nanite-ISM im Bett und an der Böschung, Yaw entlang Fließrichtung ±15°, 30–50 % eingegraben | 4–6 h |
| Keine Ufer-Vegetationszone | Gras/Punkte laufen unverändert an den Bach | Grass-Type-Variety „Ufer“ (Binsen, Farn) über Distanz-Maske 0–3 m zum Wasser; Kiefern-Ausschluss < 2 m | 2–3 h |

### BACH3_G5_bach_B2_R_P3_P0_01 (Bach in der Wiese)

Gesehen: gute Grundkomposition (Mäander, Birken am Ufer, Felskuppe hinten). Aber: ein **polygonaler Wolkenschatten** mit harten Zackenkanten mitten im Bild; Bach wieder mit weißer Kante; Wiese flächig beige, Büsche als gleichmäßige Punkte; Heidefleck rechts abrupt.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Polygonaler Wolkenschatten (Fehler) | Dunkle Fläche mit geraden Zacken-Kanten | Quelle prüfen: Volumetric-Cloud-Schatten (`r.VolumetricCloud.ShadowMap.Resolution` erhöhen, Shadow-Map-Extent prüfen) oder ein großes Mesh/Blocking-Volume, das Schatten wirft; wenn Mesh: `Cast Shadow` aus | 0,5–1 h |
| Bach als Linie ohne Uferraum | Weiße Kante, keine Steine, Wiese bis an das Wasser | Wie BACH4: Foam aus, Depth-Fade, Nassband 1–3 m, Kopfsteine, Treibholz an Außenbögen 20–40 % eingesunken (ufer-kies-coast-dunes.md) | 4–6 h |
| Wiese ohne Makro- und Mikro-Struktur | Ein Beige; Büsche gleichmäßig; Heide als harter Fleck | Macro-Noise auf Albedo; Hochgras-Variety geclumpt; Heide-Layer-Kante mit Noise 10–20 m aufbrechen; Büsche in Gruppen 3–7 | 3–4 h |

### TEICH1_H5_teich_T_K5_SUMPF_00 (Sumpfteich)

Gesehen: klares türkis-blaues Wasser mit sichtbarem Grund, dichter hellgrüner Grasrand als scharfe Kante, Weiden verstreut, Mittagslicht, Cumulus. Das liest sich als Badesee, nicht als Sumpf: kein braunes Tannin-Wasser, keine Schilfzone im Wasser, keine Totbäume, kein Nebel, keine dunkle Spiegelung.

| Abweichung | Beleg im Bild | Maßnahme in UE 5.8 (mit Werten) | Aufwand |
|---|---|---|---|
| Wasserfarbe und Klarheit falsch für Sumpf | Türkis, Grund sichtbar, hell | Lake-Instanz-Kopie „Sumpf“: Absorption hoch Richtung (0,02/0,012/0,008), Scattering 0,002–0,004 braun-grün (Richtwerte, Parameter-Namen laut ufer-kies-coast-dunes.md unverifiziert); Roughness der Oberfläche niedrig für dunkle Spiegelung; Fläche windstill (Wellen-Normal 0,3) | 2 h |
| Scharfer Grasrand statt Schilfzone | Gras endet auf einer Linie am Wasser | Variety „Schilf/Rohrkolben“ 0,5–1,5 m **in** das Wasser (Distanz-Maske −1,5 bis +3 m, Wassertiefe < 60 cm); Nassband; Totholz-Stämme 0,02/m² am Rand | 3–4 h |
| Licht und Luft wie Hochsommer-Mittag | Blauer Himmel, keine Nebelschwaden, kurze Schatten | Local Fog Volume für diesen Kessel (Dunst-Bericht Schritt 6: weiße Albedo, nicht überlappend) oder Second Fog Offset auf Teichhöhe; Sonne 15–20°; Sättigung −10 % lokal per Post-Process-Volume | 2–3 h |

---

## 4. Top 5 Maßnahmen

| Rang | Maßnahme | Betroffene Bilder | Erwarteter Sprung | Aufwand (h) | Risiko | Erste Schritte |
|---|---|---|---|---|---|---|
| 1 | **Makro-Variation + Slope-Maske im Landscape-Material** (Kopie, 6–10 Nodes: world-aligned Großnoise 300–600 m auf Albedo/Rauheit, Tile-Break V16 über Distanz, noise-gestörte Fels/Gras-Grenze) | BERG8 ×4, FELS7 ×2, FELS6, TERR3, NORD3, W6FIN ×2, LUFT4, BACH3 | Groß: beendet sichtbare Kachelung und Dreieckskanten in 12 Bildern ohne neue Assets | 6–10 | Mittel: Sampler-Budget pro Komponente (22 Layer), 5.8-Bug „Layer Blend + Nanite schwarz“ (klippennetze-a5.md); Shader-Recompile-Zeit | Material duplizieren; ein Noise-Sample, ein Lerp auf BaseColor; Shader-Complexity gegen Original; dann Slope-Maske; dann Tile-Break |
| 2 | **Licht- und Dunst-Setup nach Dunst-Bericht** (Sonne 18–24°, Temperatur 5900 K, Shadows Gain B 1,08, Rayleigh R 0,25/Scale 0,045, Mie 0,004, AP Scale 2, Height Fog 0,0035/0,02, Second Fog für Täler, Exposure fixiert) | alle 17 | Groß: Warm-Kalt-Trennung und Blauwand in jedem Bild; billigster Hebel | 4–6 | Gering (alles live); Projekteinstellung SkyAtmosphereAffectsHeightFog nur bei Bedarf (Recompile) | Dunst-Bericht Schritt 0–2 und 4; Testshots 300 m / 1 km / 3 km; W7 als Basis, W6-Milchigkeit verwerfen |
| 3 | **Felsschalen-Hierarchie und Platzierungsregeln** (3 Größenstufen, Cluster 2–5, Eingraben 25–40 %, strata_yaw pro Front, Ridge/Curvature statt Stufenkante, Floating-Check, PCG-Scree) | BERG8 ×4, FELS7 ×2, FELS6, NORD3, W6FIN_E5 | Groß auf allen Bergbildern; behebt gleichzeitig den Schwebe-Fehler | 12–20 | Mittel: Instanzzahl und HLOD (klippennetze-a5.md), Texturspeicher bei 8K-Megascans (auf 4K klemmen) | Floating-Check ins Skript; eine Testfront in A5 nach klippennetze-a5.md Schritt 5; dann Dichte der Shards auf 1/3 und Clustern |
| 4 | **Wald-Bestandsstruktur** (2–3 Arten, Höhenvarianz 0,7–1,3, Clumping mit 15–25 % Lichtungen, Kamm-Ausschluss, Waldkanten-Falloff, Totholz 2–3 %, PerInstanceRandom-Farbe) | FELS7 ×2, FELS6, TERR3, W6FIN ×2, LUFT4, BACH4, KLEIN12 ×2 | Mittel-groß: witcher_07-Effekt (Mischwald mit Farbinseln) ist vor allem Artenmix und Lücken | 10–16 | Mittel: VSM-Kosten weiterer Arten (WPO begrenzen, boden-kleinzeug-gras.md), Speicher pro Art; Asset-Beschaffung nur Kopie/Override | Clumping-Noise und Höhenvarianz im bestehenden Scatter (keine neuen Assets, 2 h); dann zweite Art als Kopie eines vorhandenen Packs |
| 5 | **Ufer- und Wasser-Pass** (weiße Kante entfernen, Nassband im Landscape-Material, Kopfsteine als Nanite-ISM, SLW-Absorption/Scattering je Gewässertyp, Schilfzone, Sumpffarbe) | BACH4, BACH3, TEICH1, TERR3, FELS6, W6FIN_E5 | Mittel-groß: Wasser wird vom Band zum Gewässer; witcher_01 lebt vom Ufer | 10–14 | Mittel: Parameter-Namen der Water-Instanzen unverifiziert (ufer-kies-coast-dunes.md), RVT-Nahtrisiko bei Decals | Foam/Depth-Fade an einer Bach-Instanz; Nassband-Term ins Material (Maßnahme 1 wiederverwenden); Kopfsteine in einer Zelle |

**Rang 6 (knapp dahinter):** Bodenkleinzeug-Stufen nach boden-kleinzeug-gras.md (Zweige, Äste, Laubhaufen, Farn, Wurzelanlauf) für KLEIN12 ×2 und alle Bodenkameras, 6–8 h. Die vier harten Fehler (schwebende Felsen, schwarzer Würfel, polygonaler Wolkenschatten, weiße Wasserkante) sind zusammen 2–4 h und gehören **vor** Rang 1.

Realistische Reihenfolge: Fehler → Rang 2 (ein Tag) → Rang 1 (ein bis zwei Tage) → Rang 3 → Rang 5 → Rang 4. Nach Rang 1+2 sollten die Berg- und Waldbilder neu aufgenommen werden, bevor Rang 3/4 entschieden werden, weil tiefes Licht und Makro-Noise den Bedarf an Felsschalen und Baumarten sichtbar verändern.

---

## 5. Hinweise zur Vergleichbarkeit

Die heutigen Screenshots sind gegen die Zielbilder strukturell unfair: hohe Kamera, hohe Sonne, weites FoV, kein Vordergrund, Auto-Exposure. Für künftige Vergleiche:

- **Kamerahöhe:** 1,7 m (Augenhöhe) für alle Bild-Typen außer Vista; Vista von einem begehbaren Punkt (Felskante, Kamm), 2–5 m über Grund, nicht aus 300 m Luft. Je Motiv zusätzlich eine „Diagnose“-Luftaufnahme, aber getrennt bewertet.
- **FoV:** 55–60° horizontal (≈ 35–40 mm) als Standard, 45° für Vistas; nicht die Editor-Default-90°.
- **Sonnenstand:** 18–24° Elevation, Azimut 60–120° zur Blickrichtung (Seitenlicht) oder 150–180° (Gegenlicht); eine Tageszeit für alle Shots eines Vergleichs.
- **Exposure fixieren:** Min = Max EV100 (Dunst-Bericht, Schritt 0), sonst kaschiert Auto-Exposure jede Nebel- und Lichtänderung.
- **Vordergrund:** Mindestens ein Element in 1–3 m (Ast, Fels, Gras-Horst) im unteren Drittel; Horizont im oberen Drittel.
- **Maßstabsreferenz:** Ein 1,8-m-Mannequin im Mittelgrund jedes Shots, damit Felsschalen- und Baumgrößen beurteilbar sind (in BERG8/FELS7 ist die Größe der Shards heute nicht ablesbar).
- **Auflösung und Format:** 1920 × 1080 oder höher, gleiches Seitenverhältnis wie die Zielbilder (16:9), Editor-Icons/Gizmos aus (`Show > Sprites` aus), `r.ScreenPercentage 100`, kein Debug-Overlay.
- **Dunst-Preset:** W7 als Basis; W6 nur noch für Luft-Diagnose. Die drei Testshots 300 m / 1 km / 3 km aus dem Dunst-Bericht einmal pro Preset.
- **Benennung:** Zelle, Kamerahöhe, FoV, Sonnenwinkel, Preset im Dateinamen (z. B. `G3_h1.7_fov58_sun20_W7.jpg`), damit Vorher/Nachher ohne Rückfrage vergleichbar ist.

---

## 6. Quellen

**Projektinterne Berichte (gelesen, Werte daraus übernommen):**

- `/home/user/fbulut/recherche/antworten/boden-kleinzeug-gras.md` – Schichtarchitektur A–E, Grass-Type-Parameter, PCG-Kleinzeug-Dichten (Richtwerte), Cull-Distanzen, VSM/WPO-Kosten, Megascans-Kleinzeug als Quelle.
- `/home/user/fbulut/recherche/antworten/dunst-atmosphaere-hoehennebel.md` – Aerial Perspective vs. Height Fog, Rayleigh/Mie-Werte, Height-Fog-Formel, Schritt-Liste 0–6, Grading-Richtwerte, Testshot-Protokoll.
- `/home/user/fbulut/recherche/antworten/klippennetze-a5.md` – Eingraben, Schichtneigung, Gruppen 2–5, RVT-Höhenblend-Graph, Moos über WorldAlignedBlend, HLOD-Kette, Speicher pro Klippe, 5.8-Bug „Layer Blend + Nanite“.
- `/home/user/fbulut/recherche/antworten/ufer-kies-coast-dunes.md` – Nassband im Landscape-Material, Steinklassen und Dichten (Richtwerte), SLW-Absorption/Scattering, Water-Material-Instanzen, Instanz-Limits.
- `/home/user/fbulut/recherche/antworten/strassen-splines-bruecken.md` – RVT-Schreibpfad, Spline-Mesh-Material-Rezept (hier nur als Referenz für RVT-Decals an Felsfüßen und Uferkanten herangezogen).

**Epic-Doku aus dem Gedächtnis (nicht frisch verifiziert):**

- Sky Atmosphere Component Properties (Aerial Perspective View Distance Scale, Start Depth), Exponential Height Fog (Second Fog Data), Local Fog Volumes – Verhalten wie im Dunst-Bericht beschrieben; Default-Werte dort aus 5.3.2-Quellspiegel.
- Single Layer Water Shading Model (Absorption/Scattering/PhaseG, Opacity < 1 für sichtbaren Grund) – aus dem Gedächtnis, deckt sich mit ufer-kies-coast-dunes.md.
- Volumetric Cloud Shadow-Map-CVars (`r.VolumetricCloud.ShadowMap.*`) als vermutete Quelle des polygonalen Wolkenschattens in BACH3_G5 – **aus dem Gedächtnis, Name und Verhalten im 5.8.3-Editor prüfen**; alternativ ein schattenwerfendes Mesh.
- WorldAlignedTexture/WorldAlignedBlend-Materialfunktionen und Kosten („use sparingly“) – aus dem Gedächtnis und klippennetze-a5.md.
- Landscape-Layer-Sampler-Grenze (~12 Texturen pro Komponente in der Praxis) – aus ufer-kies-coast-dunes.md (Polycount-Zitat), nicht Epic-offiziell.

**Zielbilder:** `/home/user/fbulut/recherche/bilder/zielbilder/witcher_01.jpg` bis `witcher_07.jpg`; witcher_06/07 tragen den Vermerk „Technical Presentation – Not Actual Gameplay“, sind also als Obergrenze, nicht als Spiel-Realität zu lesen.
