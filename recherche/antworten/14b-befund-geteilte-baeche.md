# Antwort zu Auftrag 14b – Geteilte Bäche: trockene Becken und Vorhang-Rechtecke (UE 5.8.3)

Stand 11.10.2026. Grundlage: Auftrag 14b, die Bilder `DEKOR1_*` und `STUFEN1_*`, die Antworten 12 (Teil A), 14 und 15, die Daten in
`vorlagen/daten/wasser_fx/*.json` und der Planer-Zwischenstand `skripte/gefaelle/gefaelle_plan.py` (`bauen_wasser_koerper`).

**Quellenlage:** dev.epicgames.com, forums.unrealengine.com und fab.com waren auch diesmal nicht direkt lesbar. WebFetch scheiterte mit
einem DNS-Fehler, curl über den Proxy mit 403. Alle Web-Belege stammen deshalb aus **Suchmaschinen-Auszügen** der verlinkten Seiten.
Inoffizielle Quellcode-Spiegel habe ich wie verlangt nicht benutzt. Kennzeichnung:

- **[Doku]** Epic-Doku, Python-API oder Release Notes (Auszug)
- **[Forum]** Epic-Forum, Nutzeraussage (Auszug)
- **[A12]** frühere Code-Lesung aus Antwort 12, Stand 5.6.1, für 5.8 nicht geprüft
- **[Ableitung]** aus Daten, Bildern oder Belegen gefolgert, nicht im Editor getestet
- **[ungeprüft]** nirgends belegt

## Kurzfazit

1. **Ursache, vermutet und gut begründet:** Ein Epic-`WaterBodyRiver` wird nicht als eigenes Netz gezeichnet. Seine Oberfläche entsteht
   aus den Kacheln des Wassernetzes der Water Zone und bekommt ihre Höhe aus der **Water-Info-Textur**. Bei C2 hat ein Texel 1,18 m
   (`stufen_netze.json → texel_m`). Ein Becken mit 4,5–5,6 m Länge deckt damit nur 4–5 Texel. An beiden Enden grenzen Lücken-Texel mit
   viel tieferer Höhe (das untere Becken oder die unter das Gelände gedrückte Dilatation). Das Netz interpoliert dazwischen. Über einen
   großen Teil des Beckens sinkt die Wasserfläche dadurch **unter das Bett**. Sichtbar bleiben nur die tiefsten Stellen, und zwar als
   schmale Streifen mit geraden Kanten (Ebene schneidet Ebene). Genau das zeigen `DEKOR1_C2_Nah_*`. Beim durchgehenden Fluss gibt es keine
   Lücken-Texel, darum war dort Wasser sichtbar. Epic nennt keine Mindestlänge für einen River. Im Forum gilt alles **unter ~512 uu
   (5 m) Breite** bei der Standardauflösung als problematisch [Forum]. Unsere Becken liegen genau an dieser Grenze. Epic beschreibt die
   Info-Textur selbst als „low-resolution water information“ und bietet die Dilatation nur als Abhilfe gegen deren Artefakte an [Doku].
2. **Empfehlung A – „Kaskadennetz“:** Innerhalb einer Stufenstrecke kein Epic-Wasser mehr, sondern **ein statisches Netz mit
   Single-Layer-Water-Material**. Es besteht aus flachen Becken auf `spiegel_cm` und dünnen Überfall-Zungen über jede Stufe und hängt
   nicht an der Water-Info-Textur. Damit ist es **garantiert sichtbar**, solange das Bett unter dem Spiegel liegt. Darüber kommt
   **Nature Water FX** (`NS_Waterfall_Small`/`NS_Stream_Small` an der Lippe, `NS_Impact_Small` am Fuß). An Stufen unter ~3 m entfällt
   der durchscheinende Vorhang, die Schaumscheibe entfällt überall: Den Schaum trägt die Vertexfarbe des Netzes. Epic-`WaterBodyRiver`
   bleibt nur oberhalb und unterhalb der Stufenstrecke und für Becken ≥ 15 m Länge.
3. **Rückfall B:** dasselbe Becken-Netz, aber nur die flachen Becken (ohne Zungen) und gegebenenfalls als `WaterBodyCustom` (dann mit
   Schwimm- und Unterwasser-Logik). An den Stufen bleiben Vorhang und Niagara wie in A14. **Rückfall C:** ein durchgehender
   `WaterBodyRiver` mit gestuftem Spline und einer **eigenen kleinen Bach-Water-Zone**: ≤ 0,25 m/Texel, 32-Bit-Höhen,
   `WaterZoneOverride`. Das ist der bekannte sichtbare Stand, nur feiner. Die Stufen bleiben aber Rampen von ≥ 1–2 Texeln.
4. **Planer (Auftrag 15):** **Keine Flussstücke mit Lücken mehr ausgeben.** Die Variante `flussstuecke` in `wasser_koerper` wird
   gestrichen. Der Planer gibt je Lauf eine Liste von Wasserkörpern aus: `river` für die Strecken außerhalb, `kaskadennetz` (statisch) für
   jede Stufenstrecke, optional `custom`. Die Felder stehen in Abschnitt 4. `gestufter_spline` bleibt als Variante C erhalten.
5. **Vorhang-Rechtecke:** Ursache ist eine Deckkraft, die an den Netzrändern nicht auf 0 läuft. Dazu kommt flächig gleichmäßiger
   Schaum unter grob beleuchteter Translucency. Abhilfe: alle vier Ränder per Vertex-Alpha ausblenden, Fresnel, Depth Fade, kein Emissive.
   An kleinen Stufen den Vorhang durch Niagara und die SLW-Zunge ersetzen. Die Schaumscheibe streichen oder radial maskieren.

---

## 1. Befund an Bildern und Daten

| Bild | Was zu sehen ist |
|---|---|
| `DEKOR1_C2_KA_K10a_Stufen` (Blick talab) | Weiße, fast deckende Vorhang-Rechtecke mit eingezogenen Seiten (Sanduhr-Form). Dazwischen statt Becken braunes Bett mit Steinen, nur am Fuß jedes Vorhangs ein schmaler, grünlich durchsichtiger Streifen. |
| `STUFEN1_C2_KA_K10a_Stufen` / `_Kaskade` | Gleiches Bild bei geteilten Stücken: Becken trocken, Vorhänge als helle Kacheln mit harten Seitenrändern. |
| `DEKOR1_C2_Nah_Stufe2` (Draufsicht) | Zwei Vorhänge als helle Trapeze. Darunter ein **dunkler, scharf rechteckiger Wasserfleck**, oberhalb ein schmaler, schräger Wasserstreifen mit geraden Kanten in der Bettmitte. Der Rest des Betts ist trocken. |
| `DEKOR1_C2_Nah_Verklausung` (Draufsicht) | Becken fast ganz trocken (Kies). Wasser nur als schmales, dunkles Band mit geraden Kanten und harten Ecken, schräg zur Bettachse. Die Ränder folgen nicht dem Ufer. |
| `STUFEN1_C2_Stufe01_Fall` | Unter S01 ist das Becken nur zur Hälfte nass, die Wasserfläche endet mit **gerader Kante quer durch das Becken**. Der Vorhang ist eine helle, fast deckende Fläche. |
| `DEKOR1_H4_Nah_Stufe1` (H4, nicht geteilt) | Das Wasser ist durchgehend sichtbar. Die Schaumscheibe zeichnet sich als **Rechteck mit gerader Kante** und einer feinen Diagonale (Dreieckskante) ab. |
| `DEKOR1_H4_Nah_Verklausung`, `DEKOR1_H4_KA_K8_Klamm` | H4 ungeteilt, Wasser überall sichtbar. Die Schaumscheibe bildet einen hellen Bogen mit harter Unterkante. |

Daten C2 (`stufen_fluss_teile.json`): 11 Stücke, davon **7 Becken mit 4,5–5,6 m Länge und 4 Spline-Punkten** (T01, T03, T04, T05, T07,
T08, T09). Sie sind 8,0–8,7 m breit, haben die Tiefe 109 cm und die Velocity 80 cm/s. Die Lücken messen 1,26–2,95 m, der Info-Texel
1,18 m. Ein Becken entspricht damit **≈ 4 × 7 Texeln**, eine Lücke 1–2,5 Texeln. Die langen Stücke T00 (56 m), T02 (24 m),
T06 (15 m) und T10 (50 m) enthalten die Schnellen. **Wichtig:** Die Spiegelhöhen der Stücke sind die alten Punkthöhen des
durchgehenden Flusses (`herkunft` = Punktindex). Das Bett hat sich durch das Teilen nicht geändert. Wasser fehlt also nicht, weil das
Bett zu hoch wäre, sondern weil die **gezeichnete** Höhe falsch ist [Ableitung].

## 2. Wie Epic Water arbeitet (UE 5.x) – Belege

### 2.1 Water Zone, Wassernetz, Info-Textur

- Ohne Water Zone gibt es keine Wasseroberfläche. Die Zone erzeugt die Oberfläche für alle Water Bodies, zeichnet selbst aber nichts
  [Doku: Water Body Actors / 5.8-Release-Notes-Umfeld].
- **Wassernetz:** Es besteht aus Kacheln. `TileSize` ist die Weltgröße einer Kachel auf LOD0, `ExtentInTiles` die Zahl der Kacheln, die
  Quadtree-Auflösung ist Extent / TileSize. `TessellationFactor` ist die höchste Unterteilung (LOD0), `LODScale` verschiebt die
  LOD-Ringe [Doku: Water Meshing System; API `UWaterMeshComponent`]. Ein Quadtree erzeugt jedes Frame die sichtbaren Kacheln [API].
  Projektwerte: Kachel 24 m, Faktor 6 [A12].
- **Water-Info-Textur:** Jeder Water Body zeichnet sich über sein *Water Info Material* in diese Textur [Doku]. Die Zone hat dafür
  `render_target_resolution` (IntPoint; ab 5.4 in Python nur lesbar), `zone_extent` (maximale Größe der Zone) und
  `half_precision_texture` („16 or 32 bits per channel“, ab 5.4) [Python-API WaterZone 5.1–5.5]. Kanäle laut A12: XY = Velocity,
  Z = Wasserhöhe, W = Bodenhöhe [A12].
- **Dilatation:** Ein Water Body kann seine Form in der Info-Textur um eine Strecke erweitern, „to alleviate artifacts created by having
  low-resolution water information“ [Doku: Water Body Actors]. In Python heißt das `shape_dilation` [API 5.1–5.3]. Standard 4096 cm,
  über dem Gelände wird die Dilatation unter den Boden gedrückt (`UndergroundDilationDepthOffset` 64) [A12].
- **Boden in der Info-Textur:** Ab 5.5 lassen sich beliebige Akteure per `WaterTerrainComponent` als „ground“ markieren. Sie gehen in die
  Gelände-Höhenkarte der Info-Textur ein und beeinflussen „wave attenuation, water rendering“ [Doku: 5.5 Release Notes].
- **Local Only Tessellation (ab 5.4):** Die Info-Textur deckt dann nur ein Gleitfenster um die Kamera ab, Größe
  `LocalTessellationExtent`. Ein kleineres Fenster ergibt eine höhere Pixeldichte. Außerhalb fällt das Wasser auf **statische Netze in
  Form des Water Body** zurück [Doku: 5.4 Release Notes, Roadmap, Python-API 5.4/5.5]. Diese Netze steuert
  `WaterBodyStaticMeshSettings.enable_water_body_static_mesh` (plus `section_water_body_static_mesh`) [API 5.3/5.4]. Dazu gibt es eine
  GPU-Quadtree-Variante (`r.Water.WaterMesh.GPUQuadTree.NumQuadsPerTileSide`, Standard 8, 5.4–5.8) [Drittquelle unrealdirective].
- **5.8:** Die Release Notes enthalten zum Wasser nur Fehlerbehebungen (Water Brush, ungültige Water Bodies), Simulation
  (Cloth/Buoyancy, River-Baking) und die Ablösung von `r.Water.SingleLayer.ForceVelocity`. **Nichts zur Info-Textur oder zum
  Wassernetz** [Doku: 5.8 Release Notes, Auszug]. Was für 5.4–5.6 gilt, gilt also sehr wahrscheinlich weiter [Ableitung].

### 2.2 WaterBodyRiver

- Offener Spline, Höhe je Punkt frei. Breite, Tiefe und Velocity hängen am Spline-Punkt. Die Velocity wird in eine Flowmap geschrieben
  und treibt das Fließen [Doku]. Damit die Tiefe stimmt, muss der Y-Wert der Elevation-Kurve 1 bleiben [Doku-Auszug].
- **Mindestlänge oder -breite:** Epic nennt keine [ungeprüft, nicht gefunden]. Forum: „anything less than 512u thickness has resolution
  issues“. Abhilfe dort: Info-Auflösung von 512 auf 1024–2048 und `Zone Extent` passend setzen; im gepackten Spiel seien Lücken
  zurückgekehrt [Forum: jagged edges / WaterBody Plugin 5.1].
- **Mehrere Bodies, Überlappung:** Bei Überlappung ohne Übergangsmaterial entscheidet `OverlapMaterialPriority` (−8192 … 8191, höher
  gewinnt) **nur über das Material** [Doku/API]. Übergangsmaterialien gibt es nur für River→Lake und River→Ocean [Doku], River→River
  nicht [A12]. Eine Info-Textur-Höhe wird damit nicht gesteuert. Werden zwei Bodies übereinander in die Textur gezeichnet, gewinnt laut
  A12 der obere (Aufnahme von oben) [A12].
- **Zone-Zuordnung:** `WaterZone.overlap_priority` (höher gewinnt) entscheidet bei überlappenden Zonen, sofern der Body keinen
  `WaterZoneOverride` hat [API 5.1–5.5]. Den Override gibt es auch als Blueprint-Knoten *Set Water Zone Override* [Doku].
- **Steile Flüsse:** Forum: Beispiele zeigen nur flache Flüsse, steile Rivers „get out of position“ [Forum, 5.1]. Ein Nutzer berichtet,
  dass ein River nach dem Anheben eines Spline-Punkts in getrennte Ebenen zerfällt [Forum, 4.27]. Eine Epic-Aussage zu Stufen gibt es nicht.

### 2.3 Lake, Custom, statisch

- **WaterBodyLake:** Geschlossener Spline, schnitzt die Landschaft, zeichnet über **dasselbe Wassernetz und dieselbe Info-Textur**
  [Doku]. Eine Mindestgröße ist nicht dokumentiert. **Für 5×8-m-Becken bringt ein Lake deshalb nichts.** Er hat dieselbe Texel-Grenze,
  dazu River↔Lake-Übergänge an jeder Stufe [Ableitung].
- **WaterBodyCustom:** Form aus einem Static Mesh, **nutzt das Wassernetz nicht** und schnitzt kein Gelände. Epic nennt einen Pool als
  Beispiel. Das Material braucht das Usage-Flag *Used with Water* [Doku]. Wave Source und Unterwasser-Postprozess gehen. Der
  Unterwasser-PP braucht `bGenerateCollisions` [API]. Bekannte Probleme: PP an Custom-Bodies im Forum mehrfach gestört [Forum 4.26–5.0];
  Custom ohne Info-Mesh [A12, UE-300372]; Nanite-Override stürzt ab [A12, 5.1].
- **Single Layer Water auf eigenem Netz:** SLW ist ein Shading Model (Blend *Opaque* oder *Masked*, eigener Render-Pass). `Opacity`
  steuert das Verhältnis Volumen-BSDF zu Oberflächen-BRDF; die Durchsicht ergibt sich aus dem Volumenmodell. Der Ausgabeknoten
  *Single Layer Water Material* hat Scattering, Absorption, PhaseG und Color Scale Behind Water [Doku SLW]. Es funktioniert auf
  **jedem Static Mesh** (Pool-Tutorials) [Doku/Tutorial-Auszug]. Ein Forenbeitrag empfiehlt für „Wasser in einem Netz“ ausdrücklich
  „separate water mesh with a flow material“ [Forum].
- **Grenzen:** Translucent unter der SLW-Oberfläche wird bei Kamera über Wasser nicht gezeichnet (5.8, Epic: nicht auf der Roadmap)
  [A12, Forum]. Zwei SLW-Flächen hintereinander zeigen nur die vordere [A12].

### 2.4 Eigene, feinere Water Zone

Belegt sind `WaterZoneOverride` am Body und `overlap_priority` an der Zone [API]. Ebenso, dass eine höhere Info-Auflösung schmale Flüsse
repariert [Forum]. Dass eine kleine zweite Zone innerhalb der Feldzone sauber funktioniert (Kachel-Übergang am Zonenrand,
World-Partition-Streaming), ist **[ungeprüft]**. A12 vermerkt für 5.8 ein nötiges zweites `MarkForRebuild` [A12].

### 2.5 Gestufter Einzelspline – stellt Epic Stufen dar?

- Nein. Die Höhe kommt je Texel aus der Info-Textur, eine Stufe wird zur Rampe über ≥ 1 Texel (C2: ≥ 1,2 m, mit LOD weicher) [A12].
  Bei 16-Bit-Höhen kommen Terrassen von 15–50 cm dazu [A12]. Mit eigener Zone bei 0,25 m/Texel und 32 Bit wird daraus eine
  **0,25–0,5 m lange, sehr steile Rampe**. Das Netz hat auf LOD0 bei 24-m-Kacheln und Faktor 6 ≈ 0,375 m Vertexabstand
  (24 m / 2⁶) [Ableitung aus A12-Werten]. Die Rampe ist also darstellbar, aber nie senkrecht.
- **Fließrichtung und -tempo:** Die Velocity ist ein 2D-Wert in der Draufsicht (XY der Info-Textur), begrenzt auf
  `r.Water.MaxFlowVelocity` 1024 cm/s [A12]. Auf der Rampe läuft das Normalen-Muster also **waagrecht** und wird auf der steilen Fläche
  gestreckt. Das wirkt wie Gleiten, nicht wie Fallen [Ableitung]. Darum muss an jeder Stufe Vorhang oder Niagara darüber.

### 2.6 Forum: bekannte Fälle

| Fall | Lösung laut Forum | Quelle |
|---|---|---|
| Schmale Flüsse oder Becken mit Lücken, „jagged edges“ | Info-Auflösung 1024–2048, Zone Extent korrekt; Fluss breiter; Landschaft feiner; Lücken mit Steinen kaschieren | [Forum jagged edges], [Forum 5.1 issue] |
| River im Editor sichtbar, im Spiel nicht | Water Zone wieder in die Bounds des Body schieben | [Forum not visible in Game Mode] |
| River verschwindet nach Änderung an Island/Body | ungelöst, „messing around“ | [Forum river disappears] |
| Laufzeit-River unsichtbar | `UpdateAll` aufrufen bzw. Transform ändern | [Forum runtime river] |
| Lücken am Ufer nur im gepackten Spiel | Shader-/Material-Kompilierung | [Forum artefacts packaged] |
| Steiler Gebirgsfluss | Zone Extent 0 (Nebenwirkungen: Unterwasser-PP weg), Water Body Static Mesh einschalten | [Forum need advice] |

---

## 3. Lösung – sichtbares Wasser in jedem Becken

### Ursache, Stufen der Gewissheit

| # | Vermutung | Gewissheit | Unterscheidender Test (Abschnitt 5) |
|---|---|---|---|
| U1 | Becken zu kurz für die Info-Textur. Bilinearer Übergang zu den Lücken-Texeln (tiefer gelegenes Nachbarstück oder unterirdische Dilatation) zieht die Fläche unter das Bett. | **hoch** (Bilder, Texel-Rechnung, Forum < 5 m) | Wireframe mit Grundhöhe vs. ohne; Probe mit eigener feiner Zone |
| U2 | 16-Bit-Höhenstufen (15–50 cm) treffen flache Becken stärker als die frühere Rampe | mittel [A12] | `half_precision_texture = False` |
| U3 | Dilatation (4096 cm) des oberen Stücks überdeckt das untere Becken | mittel–niedrig | `shape_dilation` der Kurzstücke auf 100 cm |
| U4 | Kachel-/Quadtree-Zuordnung, mehrere Bodies je 24-m-Kachel | niedrig [ungeprüft] | `r.Water.WaterMesh.ShowTileBounds 1` |

Alle vier entfallen bei Empfehlung A, weil das Becken-Wasser dort nicht mehr über Zone und Info-Textur läuft.

### Empfehlung A – Kaskadennetz (statisch, Single Layer Water) + Nature Water FX

**Idee:** Je Stufenstrecke ein Static Mesh, das wie ein Wasserspiegel gebaut ist. Die Becken sind waagrecht auf `spiegel_cm`. An jeder
Stufe läuft eine dünne Zunge über die Lippe (Überfallbogen) und liegt 0,1–0,2 m vor der Felswand, bis 0,3 m unter den unteren Spiegel.
Material ist SLW, Schaum über die Vertexfarbe. Wo das Bett tiefer liegt als das Netz, ist Wasser, ohne jede Abhängigkeit von Zone und
Textur [Ableitung, gestützt auf Doku SLW + Doku Custom/Pool].

**Bau (Claude lokal, Reihenfolge):**

1. **Material** `M_EL_Kaskade_SLW` (neuer Master, Ordner `/Game/Eldarien/Welt/Wasser/Stufenfall`):
   - Shading Model *Single Layer Water*, Blend *Opaque*, Two Sided aus, Usage *Static Mesh*. *Used with Water* ist nicht nötig, weil es
     kein Water Body ist [Ableitung]. Nanite am Netz aus (SLW-Unterstützung durch Nanite [ungeprüft]).
   - Ausgabeknoten *Single Layer Water Material*: Absorption und Scattering **aus `MI_Eldarien_Wasser_Fluss` übernehmen** (Werte im
     Editor ablesen), damit Becken und Epic-Fluss gleich aussehen. PhaseG 0,1, Color Scale Behind Water 1. Anfangswerte, falls nichts
     ablesbar ist [Annahme]: Absorption (0,35, 0,09, 0,06) /m, Scattering (0,02, 0,035, 0,03) /m.
   - Normalen: zwei Normal-Samples mit Panner entlang **UV.x = Fließrichtung**, Tempo = `VertexColor.R × 3 m/s` (R = Tempo/300 cm/s),
     klassisches Flowmap-Überblenden mit `Frac(Time·0,5)` [A12]. Becken R ≈ 0,27 (80 cm/s), Zunge R = 0,8–1,0.
   - Schaum = `VertexColor.B × Rauschen(UV, Zeit)`. Schaum mischt BaseColor zu (0,80, 0,84, 0,86), **Opacity → 1** (Oberflächen-BRDF,
     wirkt weiß) und Roughness → 0,6. Grundlage: Opacity-Bedeutung laut Doku SLW. Specular 0,255, Roughness Wasser 0,03–0,06.
   - Kein Emissive, Cast Shadow aus.
   - MI `MI_EL_Kaskade_SLW` mit Parametern `Tempo_Skala`, `Schaum_Menge`, `Absorption`, `Scattering`, `Normal_Staerke`.
2. **Netz** `SM_KN_<lauf>_<nr>` aus dem Planer-Datensatz `kaskadennetz` (Abschnitt 4). Format wie die Vorhang-Netze
   (`*.pos.f32/.tri.i32/.nrm.f32/.col.u8`, `stufen_netze.json`).
   - Becken: Streifen quer zur Mittellinie, 0,5 m Zellen. Breite = Wasserbreite + 2 × 0,4 m Überstand (das Ufer verdeckt den Rand), z = `spiegel_cm`.
   - Zunge: 3–5 Querreihen auf dem Überfallbogen x = v·t, z = −g·t²/2 mit v = 2,4 m/s (`stufen_netze.json → vorhang.v_kante_m_s`),
     dann senkrecht an der Wand mit ≥ 0,15 m Abstand zum Bett (`abstand_bett_m` 0,2), Fuß 0,3 m unter dem unteren Spiegel.
   - Vertexfarbe: R = Tempo/300, G = Fallanteil (0 Becken, 1 Zunge), B = Schaum: 1 an der Lippe, 1 im Radius
     clamp(0,5·D + 0,5; 1; 3) m um den Aufprall, nach 2–4 m auf 0; A = 1.
   - Normalen nach oben bzw. aus der Wand heraus. UV.x = Bogenlänge entlang der Mittellinie / 2 m, UV.y = quer / 2 m.
   - Kollision: keine (oder `NoCollision`); Spieler-Wasserlogik siehe Rückfrage 2.
3. **Epic-Fluss anpassen:**
   - Den durchgehenden C2-Fluss (heutiger Rückweg-Stand) durch **zwei** `WaterBodyRiver` ersetzen: oben T00 bis zur Lippe S01
     + 0,5 m, unten ab dem Fuß der letzten Stufe (S10) + 1 m (T10).
   - Übergang: Das Kaskadennetz beginnt 0,5 m **vor** dem Ende des oberen Rivers und liegt dort 2 cm unter dessen Spiegel. Das River-SLW
     verdeckt es, es gibt kein Z-Fighting, und wo das River-Ende in der Info-Textur abfällt, trägt das Netz [Ableitung]. Unten genauso,
     die Naht liegt im Schaum des letzten Aufpralls.
   - Becken innerhalb der Strecke ≥ 15 m (bei C2 keines, T02 mit 24 m enthält eine Schnelle) dürfen River bleiben. Einfacher und
     einheitlicher ist es, **alles zwischen erster Lippe und letztem Fuß ins Kaskadennetz** zu nehmen.
   - Schnellen innerhalb der Strecke (S00/S11 sind Rand) werden als geneigte Zunge mit R = 1 und B = 0,3–0,6 gebaut.
4. **Vorhang und Schaumscheibe:**
   - An Stufen mit Fall < 3 m: **Vorhang-Netz weg** (Koordinator-Regel `NIAGARA_KLEIN` im Planer stimmt damit überein). Statt dessen
     SLW-Zunge plus `NS_Waterfall_Small` (Fall 2–3 m) bzw. `NS_Stream_Small` an der Lippe (Fall < 2 m) plus `NS_Impact_Small` am Fuß.
   - **Schaumscheiben überall weg**, den Schaum liefert B im Netz.
   - Stufen ≥ 3 m (C2: S01, S02, S03 am Vorhang 2,4–3,3 m; S07 5,3 m gesamt): Vorhang mit den Kantenmasken aus Abschnitt 6 behalten
     **oder** nur SLW-Zunge plus `NS_Waterfall_Small`. Entscheidung nach Bildprobe S01.
   - Große Fälle K1/K8 bleiben wie in A14.
5. **Niagara** wie A14/A15 2.9: Pivot 3–10 cm über `spiegel_cm`, Cast Shadow aus, Sort 2, Cull 30/45 m, ≤ 6 gleichzeitig. Was
   unter den Spiegel fällt, wird nicht gezeichnet, das ist erwünscht [A12].

**Prüfschritte A:**

1. Draufsicht C2 (Kamera wie `DEKOR1_C2_Nah_*`): Jedes Becken ist **von Ufer zu Ufer** nass. Wo Kies durchscheint, liegt das Bett höher
   als `spiegel_cm` → Planer-Prüfung `bett_unter_spiegel` (Abschnitt 4).
2. Blick talab wie `DEKOR1_C2_KA_K10a_Stufen`: keine weißen Rechtecke. An den Stufen glasige Zunge mit Schaumsaum, Strähnen von Niagara.
3. Aus 60–100 m (Niagara gecullt): Die Stufen bleiben als helle Schaumbänder (B) lesbar.
4. `stat Niagara`, `profilegpu`: Ziel ≤ 0,5 ms für alle Wasser-FX im Bild (A14).
5. Übergänge oben und unten: kein Spalt, kein Flimmern (`r.Water.WaterMesh.ShowWireframe 1` zeigt, wo der River endet).

**Folgen und Risiken A:**

- Kein Epic-Schwimmen, keine Buoyancy, kein Unterwasser-PP in den Becken. Bei 1,1 m Tiefe wird ohnehin gewatet [Ableitung]. Falls doch
  nötig: Rückfall B (Custom) für einzelne tiefe Kolke.
- Niagara-Systeme, die die Water-Info abfragen, sehen kein Wasser. Ob NWFX das tut, ist **[ungeprüft]** (Prüfliste A14).
- Das Material muss zum Epic-Fluss passen (Absorption/Scattering übernehmen), sonst sieht man an den Übergängen einen Farbsprung.
- Lumen-Reflexionen und Refraktion arbeiten auf SLW-Static-Meshes wie auf dem Wassernetz [Ableitung aus Doku SLW].

### Rückfall B – Becken-Platten (statisch oder WaterBodyCustom) + Vorhang/Niagara an den Stufen

Wenn die SLW-Zunge auf der steilen Fläche nicht überzeugt (zu glasig, Spiegelungen):

1. Nur die flachen Becken als Netz bauen, Umriss = Planer-`becken[].umriss_cm` + 0,4 m. Dazu `spiegel_cm`, Material und Vertexfarbe wie
   A (B = Aufprallschaum).
2. Stufen wie A14: Vorhang mit Kantenmasken (Abschnitt 6) plus Niagara. Der Vorhangfuß reicht 0,3 m unter den Beckenspiegel.
3. **Variante B-Custom**, nur wo Schwimmen oder Unterwasser-PP gebraucht wird (Kolke ≥ 1,5 m):
   - `WaterBodyCustom` mit dem Platten-Netz als Static Mesh, Material SLW mit *Used with Water*, `bGenerateCollisions = True`,
     `overlap_material_priority` 0, `WaterZoneOverride` auf die Feldzone.
   - Erst an **einem** Becken testen: PP, Kollision, Speichern und Neuladen (A12: Override-Rücksetzung bei Nicht-Custom, Custom-Bugs).
4. Prüfschritte wie A 1–5.

### Rückfall C – Ein gestufter WaterBodyRiver + eigene Bach-Zone

Für den Fall, dass statische Netze verworfen werden. Ausgangspunkt ist der heutige durchgehende Fluss, der Wasser zeigte.

1. **Bach-Zone** `C2_Bach_Wasserzone`:
   - Mitte = Mitte der Kaskade, `zone_extent` = Kaskaden-Rechteck + 20 m (C2: ≈ 200 × 200 m).
   - `render_target_resolution` 800 × 800 → **0,25 m/Texel**. Im Details-Panel setzen; in Python ab 5.4 nur lesbar
     (Setzen per `set_editor_property` [ungeprüft]).
   - `half_precision_texture = False`, `overlap_priority` = Feldzone + 10.
   - TileSize 1200 cm und `TessellationFactor` 6 → 0,19 m Vertexabstand auf LOD0 [Ableitung].
   - Danach `r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames 2` und in 5.8 zweimal *Mark for Rebuild* [A12].
2. **River** `F_ERLENBACH_1V_C2_GS` aus der Planer-Variante `gestufter_spline`:
   - An jeder Stufe Lippe und Fuß ≤ 1 m auseinander, Typ LINEAR; Becken CURVE_CLAMPED.
   - Velocity Becken 80, Lippe/Fuß 300.
   - `WaterZoneOverride` = Bach-Zone, `shape_dilation` 200 cm (statt 4096, damit nichts über die Stufen greift [Ableitung]).
3. Stufen: Vorhang (Kantenmasken) bzw. Niagara wie A. Die steile Rampe (0,25–0,5 m) liegt unter dem Vorhang.
4. **Prüfschritte C:**
   - `r.Water.WaterMesh.ShowWireframe 1` und `...ShowWireframeAtBaseHeight 1`: Liegen Kacheln über allen Becken?
   - Draufsicht: Becken nass?
   - Seitenblick: Rampe ≤ 0,5 m lang?
   - Speicher: 800² × 16 B ≈ 10 MB, unkritisch.
   - Am Rand der Bach-Zone (Übergang zur Feldzone) auf Sprünge achten **[ungeprüft]**.
5. **Grenzen:** Stufe nie senkrecht. Das Fließmuster läuft auf der Rampe waagrecht (2.5). Eine zweite Zone je Kaskade ist Pflegeaufwand
   bei 19+ Strecken (A15). Ob eine Zone in einer Zone mit World Partition sauber streamt, ist **[ungeprüft]**.

**Nicht empfohlen:**

- WaterBodyLake je Becken: dieselbe Info-Textur-Grenze (2.3).
- Getrennte Flussstücke mit Lücken: Ursache des Befunds.
- `WaterMeshOverride` am River und das Exclusion Volume (A12).

---

## 4. Folgen für den Planer (Auftrag 15)

**Antwort auf die drei Fragen:**

- **Keine Flussstücke mit Lücken mehr.** A15-Regel 2.1/3 („Flussstücke an jeder Stufe ≥ 0,8 m trennen“) wird gestrichen. Ersatz:
  „Innerhalb einer Stufenstrecke ein Kaskadennetz. Epic-River nur außerhalb, Übergang 0,5 m überlappend, Netz 2 cm unter dem River.“
- **Kein gestufter Einzelspline als Standard.** Er bleibt als Variante C in `wasser_koerper` (der Code ist schon da).
- **Becken nicht als Lake.** Becken gehen ins Kaskadennetz. `custom` nur auf ausdrücklichen Wunsch je Kolk.

**Schema** `plan.json → wasser_koerper` (ersetzt die heutigen drei „Varianten“ durch eine Liste gültiger Körper, Variante C bleibt
als Alternative):

```json
"wasser_koerper": [
  {"id": "F_ERLENBACH_1V_C2_R0", "typ": "river",
   "s_m": [0.0, 55.7],
   "punkte": [[x_cm, y_cm, z_cm, breite_cm, tiefe_cm, velocity_cm_s], "..."],
   "punkt_typen": ["CURVE", "CURVE_CLAMPED", "...", "CURVE"],
   "zone": "C2_Wasserzone", "overlap_material_priority": 0,
   "anschluss_unten": {"an": "F_ERLENBACH_1V_C2_KN0", "ueberlapp_m": 0.5}},

  {"id": "F_ERLENBACH_1V_C2_KN0", "typ": "kaskadennetz",
   "s_m": [55.2, 152.0],
   "mittellinie": [[x_cm, y_cm, z_cm, breite_cm, tempo_cm_s, fallanteil, schaum, abstand_bett_cm], "..."],
   "knick": ["becken", "lippe", "bogen", "wand", "fuss", "becken", "..."],
   "rand_ueberstand_m": 0.4, "zelle_m": 0.5,
   "anfang_unter_river_cm": 2, "ende_unter_river_cm": 2,
   "material": "/Game/Eldarien/Welt/Wasser/Stufenfall/MI_EL_Kaskade_SLW",
   "nanite": false, "schatten": false, "kollision": "keine",
   "vorhang_an_stufen": ["S01", "S07"],
   "pruefung": {"bett_unter_spiegel_min_m": 0.2, "ufer_ueber_spiegel_am_rand_m": 0.1}},

  {"id": "F_ERLENBACH_1V_C2_R1", "typ": "river", "s_m": [151.0, 201.4], "...": "..."},

  {"id": "F_ERLENBACH_1V_C2_K3", "typ": "custom", "optional": true,
   "umriss_cm": [[x, y], "..."], "spiegel_cm": 7275.0, "tiefe_m": 1.6,
   "material": "…SLW mit Used with Water…", "kollision": true, "zone": "C2_Wasserzone"}
],
"wasser_koerper_alternativ": {"variante": "gestufter_spline", "zone_neu": {
   "id": "C2_Bach_Wasserzone", "mitte_cm": [x, y, z], "ausdehnung_m": [200, 200],
   "aufloesung": [800, 800], "half_precision": false, "overlap_priority": 10, "tile_size_cm": 1200},
   "river": {"punkte": "...", "punkt_typen": "...", "shape_dilation_cm": 200}}
```

**Feldregeln:**

- `typ ∈ {river, kaskadennetz, custom, statisch_platte}`. `lake` ist reserviert und wird nicht benutzt.
- `mittellinie`:
  - z = `spiegel_neu_cm` (schon berechnet, monoton fallend, Stufe = Lippe + Fuß ≤ 1 m);
  - zwischen Lippe und Fuß 3–5 Bogenpunkte (Überfallparabel, v = 2,4 m/s), dann Wandpunkte mit `abstand_bett_cm` ≥ 15;
  - Fuß bis 30 cm unter den unteren Spiegel;
  - `fallanteil` 0/1; `schaum` 0–1 nach der Aufprallregel (A: Radius clamp(0,5·D + 0,5; 1; 3) m).
- `knick` benennt die Rolle jedes Punkts, damit der Netzbauer Becken (waagrecht, quer flach) und Zunge (dünn, wandnah) richtig trianguliert.
- **Prüfungen im Planer** (als FEHLER melden):
  - (a) Bett im Becken (Mittel über den nassen Querschnitt) ≥ 0,2 m unter `spiegel_cm`, sonst bleiben trockene Flecken.
  - (b) Gelände am Umrissrand ≥ 0,1 m über `spiegel_cm`, sonst sieht man die Netzkante.
  - (c) Kaskadennetz und River überlappen nur in `ueberlapp_m`.
  - (d) An jeder Stufe des Kaskadennetzes mindestens Niagara **oder** Vorhang (Liste `vorhang_an_stufen`).
- `effekte` (A15 2.9) bleiben. **Neu:** Schaumscheibe nicht mehr ausgeben. Vorhang nur, wenn die Stufe in `vorhang_an_stufen` steht
  (Standard: Fall am Vorhang ≥ 3 m).
- Die Becken-Daten aus `bauen_wasser_koerper` (`umriss_cm`, `spiegel_cm` = Höhe der nächsten Lippe) bleiben für B und `custom` nutzbar.

---

## 5. Prüf- und Probe-Skript (Unreal Editor Python, optional)

Zweck: (1) Bestandsaufnahme Zone und Flussstücke, (2) Debug-Ansichten für U1–U4, (3) **Probe A an einem Becken** mit einer
SLW-Platte, die die Engine-Ebene `/Engine/BasicShapes/Plane` (100 × 100 cm) skaliert. Belegte API: `EditorActorSubsystem`
(`get_all_level_actors`, `spawn_actor_from_class`), `EditorAssetLibrary.load_asset`, `SystemLibrary.execute_console_command`,
`AssetToolsHelpers`/`MaterialFactoryNew`, `MaterialEditingLibrary` (`create_material_expression`, `connect_material_property`,
`recompile_material`), `WaterBody.get_water_body_component`. Eigenschaftsnamen `zone_extent`, `render_target_resolution`,
`half_precision_texture`, `overlap_priority`, `shape_dilation`, `overlap_material_priority` stehen in den Python-API-Seiten 5.1–5.5.
**[ungeprüft]**: der Enum-Name `MSM_SINGLE_LAYER_WATER`, ob 5.8 die Namen geändert hat, und ob SLW ohne eigenen Ausgabeknoten
brauchbare Standardwerte hat.

```python
# probe_14b.py – im UE-Editor: py "<pfad>/probe_14b.py"
import math, unreal
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
WELT = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
def cmd(c): unreal.SystemLibrary.execute_console_command(WELT, c)
def lies(o, n):
    try: return o.get_editor_property(n)
    except Exception as e: return "?(%s)" % e

# 1) Bestandsaufnahme
for a in EAS.get_all_level_actors():
    if isinstance(a, unreal.WaterZone):
        print("ZONE", a.get_actor_label(), [ (n, lies(a, n)) for n in
              ("zone_extent", "render_target_resolution", "half_precision_texture", "overlap_priority")])
    elif isinstance(a, unreal.WaterBody) and "ERLENBACH_1V" in a.get_actor_label():
        c = a.get_water_body_component()
        print("BODY", a.get_actor_label(), type(a).__name__,
              [(n, lies(c, n)) for n in ("shape_dilation", "overlap_material_priority")])

# 2) Debug-Ansichten (U1/U4): Kacheln vorhanden? Grundhoehe vs. verschoben?
def debug(an=True):
    v = 1 if an else 0
    for c in ("r.Water.WaterMesh.ShowWireframe", "r.Water.WaterMesh.ShowTileBounds"):
        cmd("%s %d" % (c, v))
# debug(True); danach mit cmd("r.Water.WaterMesh.ShowWireframeAtBaseHeight 1") vergleichen

# 3) Probe A: SLW-Platte auf Becken T03 (Daten aus stufen_fluss_teile.json, Weltkoordinaten cm)
P0 = (-175844.9, -230866.8); P1 = (-176065.7, -230401.1)   # erster/letzter Punkt T03
SPIEGEL_CM = 7275.0          # Hoehe der naechsten Lippe (S04) = flacher Beckenspiegel
BREITE_CM = 800.0 + 2 * 40.0 # Wasserbreite + 2 x 0,4 m Ueberstand
def slw_material(pfad="/Game/Eldarien/Test", name="M_EL_Test_SLW"):
    voll = "%s/%s" % (pfad, name)
    if unreal.EditorAssetLibrary.does_asset_exist(voll):
        return unreal.EditorAssetLibrary.load_asset(voll)
    m = unreal.AssetToolsHelpers.get_asset_tools().create_asset(name, pfad, unreal.Material, unreal.MaterialFactoryNew())
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_SINGLE_LAYER_WATER)  # [ungeprueft]
    MEL = unreal.MaterialEditingLibrary
    farbe = MEL.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, 0)
    farbe.set_editor_property("constant", unreal.LinearColor(0.02, 0.05, 0.05, 1.0))
    MEL.connect_material_property(farbe, "", unreal.MaterialProperty.MP_BASE_COLOR)
    rau = MEL.create_material_expression(m, unreal.MaterialExpressionConstant, -400, 200)
    rau.set_editor_property("r", 0.05)
    MEL.connect_material_property(rau, "", unreal.MaterialProperty.MP_ROUGHNESS)
    MEL.recompile_material(m)
    unreal.EditorAssetLibrary.save_asset(voll)
    return m

def probe_platte(fluss_verbergen=True):
    dx, dy = P1[0] - P0[0], P1[1] - P0[1]
    laenge = math.hypot(dx, dy) + 150.0                      # + 1,5 m in die Luecken
    mitte = unreal.Vector((P0[0] + P1[0]) / 2, (P0[1] + P1[1]) / 2, SPIEGEL_CM)
    rot = unreal.Rotator(0.0, 0.0, math.degrees(math.atan2(dy, dx)))   # (roll, pitch, yaw)
    a = EAS.spawn_actor_from_class(unreal.StaticMeshActor, mitte, rot)
    a.set_actor_label("PROBE14b_Becken_T03")
    smc = a.static_mesh_component
    smc.set_static_mesh(unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Plane"))
    smc.set_material(0, slw_material())
    smc.set_editor_property("cast_shadow", False)
    a.set_actor_scale3d(unreal.Vector(laenge / 100.0, BREITE_CM / 100.0, 1.0))
    if fluss_verbergen:                                       # Epic-Fluss nur im Editor ausblenden (nicht gespeichert)
        for b in EAS.get_all_level_actors():
            if isinstance(b, unreal.WaterBody) and "ERLENBACH_1V" in b.get_actor_label():
                b.set_is_temporarily_hidden_in_editor(True)
    return a
# probe_platte()  -> Draufsicht wie DEKOR1_C2_Nah_*: Becken T03 von Ufer zu Ufer nass?  Kies sichtbar = Bett > Spiegel.
# Aufraeumen: Akteur PROBE14b_* loeschen, Fluesse per set_is_temporarily_hidden_in_editor(False) wieder einblenden.
```

**Auswertung:**

- Die Platte zeigt das Becken nass, das Epic-Stück an derselben Stelle nicht → U1–U4 bestätigt, Weg A ist richtig.
- Die Platte zeigt Kies → Das Bett liegt höher als 72,75 m, die Planer-Prüfung (a) greift. Dann `SPIEGEL_CM` in 5-cm-Schritten anheben
  und den Wert melden.
- U1 gegen U2/U3 trennen: `half_precision_texture` der Feldzone auf False und `shape_dilation` der Kurzstücke auf 100 setzen, neu
  bauen. Sind die Becken dann nass, ist U2/U3 die Ursache und C wird aussichtsreicher.

---

## 6. Vorhang-Rechtecke und Schaumscheibe

**Ursache [Ableitung aus Bildern + A14 + Forum]:**

1. Die Deckkraft läuft an den Netzrändern (oben, seitlich, unten) nicht auf 0. Ein durchscheinendes Netz zeigt dann seine Silhouette als
   harte Kante. `Rand_Durchsicht` wirkt laut A14 nur über Vertexfarbe G/B an den Seiten.
2. Gleichmäßiger Schaum über die ganze Fläche und Lit Translucency, die unter Lumen nur grob über das Translucency Lighting Volume
   beleuchtet wird [A12, Epic Lit Translucency]. Das gibt eine flächig helle Kachel ohne Struktur.
3. Schaumscheibe: Ein Quad mit Textur, das am Rand nicht auf 0 geht. In H4 sieht man die Diagonale zwischen den beiden Dreiecken
   (Schattierungs- oder Normalensprung).

Die Translucent-Sortierung ist **nicht** die Hauptursache. Sie würde Flackern und falsche Reihenfolge zeigen, keine stabilen Rechtecke.

**Abhilfe, wo Vorhang oder Scheibe bleiben:**

| Maßnahme | Wert | Beleg |
|---|---|---|
| Kantenmaske im Netz: Vertex-Alpha 0 an **allen** Rändern, ansteigend über 0,3–0,5 m (oben 0,4 m vor der Kante, seitlich 0,5 m, unten via Depth Fade) | Netzbauer: ≥ 2 Vertexreihen je Rand, sonst wirkt der Verlauf abrupt | [Forum/Polycount: Vertex-Alpha, „distance them more“] |
| Opacity = `Deckkraft × VertexColor.A × (Strähnen-Textur) × Fresnel(Exp 3, Basis 0,2) × DepthFade(30 cm)` | Deckkraft 0,45–0,5 | [A12], [Forum: Gradient/UV-Maske] |
| Schaum nur in Streifen: Schaum = `Schaum_Menge × Strähnen × (1 − G)`, Schaum nur am Fuß (unteres Drittel) und an der Lippe | Schaum_Menge 0,3 | [A14] |
| Kein Emissive, `Schaum_Leuchten` 0. Lighting Mode *Surface ForwardShading* für Lichtung pro Pixel (teurer) statt *TranslucencyVolume* | probeweise an S01 | [Epic Lit Translucency, via A12] |
| Schaumscheibe: Opacity × `RadialGradientExponential(Radius 0,5, Dichte 2)` × DepthFade(20 cm), Netz als 8–12-Eck statt Quad | oder Scheibe ganz weg (Empfehlung A) | [Ableitung] |
| Translucency Sort Priority: Vorhang 0, Scheibe 1, Niagara 2; Separate Translucency an | wie A12 | [A12] |
| MSAA aus, falls weiße Säume an Depth-Fade-Kanten | – | [Forum: depth fade outline] |

**Nature Water FX statt eigenem Vorhang** (Ferats Wunsch):

- An Stufen < 3 m ersetzt `NS_Waterfall_Small` bzw. `NS_Stream_Small` + `NS_Impact_Small` den Vorhang. Den Spalt schließt in A die
  SLW-Zunge, nicht mehr der Vorhang. Damit fällt das A14-Argument „Vorhang nötig wegen 1,3–3-m-Lücke“ weg.
- Jenseits des Cull (30–45 m) bleibt die Stufe durch Zunge und Schaum (B) lesbar.
- Die Systeme sind laut Fab „optimized, loop continuously“ mit User-Parametern je Teil, Impact und Wakes getrennt [Fab-Auszug]. Skalen
  und Parameter-Namen bleiben **[ungeprüft]** (Prüfliste A14 Punkt 1–3).
- Breite Stufen (8 m) bei NS_Waterfall_Small (~3 m angenommen): zwei Systeme versetzt (−2 m/+2 m quer) oder ein System mit Skala
  quer [ungeprüft, ob das System nicht-uniforme Skala verträgt]. Budget ≤ 6 gleichzeitig beachten (A14).

---

## 7. Unsicherheiten

- Ursache U1 ist abgeleitet, nicht im Editor gemessen; Epic dokumentiert die Interpolation am Body-Rand nicht. Das Skript in
  Abschnitt 5 entscheidet das in ~10 min.
- Ob SLW auf Static Mesh in 5.8.3 mit Lumen-Reflexionen genau wie das Wassernetz aussieht, ist **[ungeprüft]**. Darum Absorption und
  Scattering aus dem Flussmaterial übernehmen.
- Wie eine steile SLW-Zunge optisch wirkt (glasig?), ist **[ungeprüft]** → Probe S01 vor dem Ausrollen. Rückfall B hält die Zunge aus
  dem Spiel.
- `render_target_resolution` ist ab 5.4 in Python nur lesbar. Variante C setzt den Wert im Details-Panel.
- Alle Web-Belege sind Suchauszüge (Seiten gesperrt). Werte aus A12 stammen aus Code 5.6.1.

## Quellen

**Epic-Doku und API (Auszüge):**

- [Water Meshing System and Surface Rendering](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-meshing-system-and-surface-rendering-in-unreal-engine)
- [Water Body Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-body-actors-in-unreal-engine)
- [Water Debugging and Scalability Options](https://dev.epicgames.com/documentation/unreal-engine/water-debugging-and-scalability-options-in-unreal-engine)
- [Water System](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-system-in-unreal-engine)
- [Single Layer Water Shading Model](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine)
- [Python WaterZone 5.5](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterZone?application_version=5.5)
- [Python WaterZone 5.4](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterZone?application_version=5.4)
- [Python WaterZone 5.1](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterZone?application_version=5.1)
- [Python WaterBodyComponent 5.2](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyComponent?application_version=5.2)
- [Python WaterBodyComponent 5.3](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyComponent?application_version=5.3)
- [Python WaterBodyRiverComponent 5.4](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyRiverComponent?application_version=5.4)
- [Python WaterBodyStaticMeshSettings 5.3](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyStaticMeshSettings?application_version=5.3)
- [Python WaterBodyCustom 5.2](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyCustom?application_version=5.2)
- [Python WaterBodyCustomComponent 5.4](https://docs.unrealengine.com/5.4/en-US/PythonAPI/class/WaterBodyCustomComponent.html)
- [Python WaterBody 5.4](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBody?application_version=5.4)
- [API UWaterMeshComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/Water/UWaterMeshComponent)
- [Blueprint Set Water Zone Override](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Water/SetWaterZoneOverride)

**Release Notes und Roadmap:**

- [Unreal Engine 5.4 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5.4-release-notes?application_version=5.4)
  (Local Only Tessellation, statische Rückfallnetze)
- [Unreal Engine 5.5 Release Notes](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-5-release-notes)
  (WaterTerrainComponent, Info-Textur je View)
- [Unreal Engine 5.8 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US)
- [Roadmap Water Scalability](https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/1453-water-scalability)

**Forum (Auszüge):**

- [Water body river: fix jagged edges](https://forums.unrealengine.com/t/water-body-river-fix-jagged-edges/1949564)
- [WaterBody Plugin in 5.1 issue](https://forums.unrealengine.com/t/waterbody-plugin-in-5-1-issue/726667)
- [River not conforming to landscape 5.1](https://forums.unrealengine.com/t/issue-with-water-body-river-not-conforming-to-my-landscape-ue5-1/741308)
- [Water body river split into separated planes](https://forums.unrealengine.com/t/water-body-river-split-into-separated-planes/1856214)
- [Water Plugin, need advice (steiler Fluss)](https://forums.unrealengine.com/t/water-plugin-need-advice-help-pl/755781)
- [Water Body River not visible in Game Mode](https://forums.unrealengine.com/t/water-body-river-not-visible-in-editor-game-mode/157386)
- [River disappears after changing values](https://forums.unrealengine.com/t/water-plugin-river-disappears-after-changing-values-from-island-body/633575)
- [Runtime water body river creation](https://forums.unrealengine.com/t/runtime-water-body-river-creation-c/2281463)
- [River artefacts in packaged game](https://forums.unrealengine.com/t/water-body-river-artefacts-in-packaged-windows-game/2405500)
- [WaterBodyCustom post processing 4.26](https://forums.unrealengine.com/t/is-post-processing-broken-on-the-4-26-waterbodycustom-of-the-water-plugin/482024)
- [Fill static mesh with water](https://forums.unrealengine.com/t/how-to-fill-the-deeper-in-static-mesh-with-water/629383)
- [Waterbody Transition Issue](https://forums.unrealengine.com/t/waterbody-transition-issue/2514058)
- [Material edge fade](https://forums.unrealengine.com/t/material-edge-fade/458145)
- [Depth fade outline](https://forums.unrealengine.com/t/how-can-i-fix-outline-effect-using-depth-fade/412826)
- [Polycount: Fading waterfall effect](https://polycount.com/discussion/156300/fading-waterfall-effect)

**Sonstige:**

- [unrealdirective: r.Water.WaterMesh.GPUQuadTree.NumQuadsPerTileSide](https://unrealdirective.com/resources/console-variables/r-water-watermesh-gpuquadtree-numquadspertileside/)
  (Drittquelle)
- [Fab: Nature Water FX](https://www.fab.com/listings/c34e8871-3585-4381-b21f-1b895814472b)

**Projektintern:**

- `antworten/12-recherche-wasser-gpu-schatten.md` Teil A
- `antworten/14-wasser-fx.md`
- `antworten/15-gefaelle-regelwerk.md`
- `vorlagen/daten/wasser_fx/stufen_fluss_teile.json`, `stufen_netze.json`, `stufen.json`
- `skripte/gefaelle/gefaelle_plan.py` (`spiegel_punkte`, `bauen_wasser_koerper`, `NIAGARA_KLEIN`)

## Rückfragen

1. **Freigabe A (Kaskadennetz) als Standard für alle Stufenstrecken?** Erst Probe an C2 S01–S03 (Skript Abschnitt 5 + ein echtes
   Netz), dann Ausrollen auf die A15-Strecken.
2. **Gameplay in Becken:** Müssen Spieler in den Kolken schwimmen bzw. braucht es Unterwasser-PP? Dann für Kolke ≥ 1,5 m `custom`
   (Rückfall B), sonst reicht statisch.
3. **Vorhang an Stufen ≥ 3 m behalten** (C2 S01/S02/S03/S07) oder auch dort nur SLW-Zunge + `NS_Waterfall_Small`? Vorschlag:
   Entscheidung nach Bildprobe S01.
4. **Absorption/Scattering von `MI_Eldarien_Wasser_Fluss`**: Bitte die Ist-Werte (oder die Parameterliste) exportieren, damit
   `MI_EL_Kaskade_SLW` farbgleich wird.
5. Soll der Planer Variante C (`gestufter_spline` + Bach-Zone) weiter mit ausgeben (für einen Vergleich), oder nur noch A?

## Entscheidungen Koordinator zu den Rückfragen (Ferat: „du entscheidest“)

1. **Variante A „Kaskadennetz“ ist Standard**; der Planer aus Auftrag 15 gibt keine Flussstücke mit Lücken mehr aus.
2. **Schwimmen in den Becken ist nicht nötig** (Becken 5–7 m, flach) → kein `WaterBodyCustom` als Standard.
3. **Vorhang:** Unter 3 m Fallhöhe nur Nature Water FX (`NS_Waterfall_Small` + `NS_Impact_Small`); ab 3 m bleibt der eigene Vorhang für die Fernsicht (mit den Rand-Abhilfen aus Abschnitt „Vorhang-Rechtecke“), Niagara ergänzt nah. Schaumscheiben entfallen.
4. **Absorption/Scattering von `MI_Eldarien_Wasser_Fluss`:** bitte im Editor auslesen und ins Kaskadennetz-MI übernehmen (Prüfschritt für Claude lokal; aus der Cloud nicht lesbar).
5. **Variante C** gibt der Planer nur auf Schalter `--variante C` aus.

Erster Prüfschritt lokal: das Python-Skript aus Abschnitt 5 (Zonenwerte, Kachelgrenzen, SLW-Probeplatte auf T03), dann Bildprobe der SLW-Zunge an S01.
