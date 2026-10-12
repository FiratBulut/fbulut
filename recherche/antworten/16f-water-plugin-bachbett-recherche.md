# Antwort Auftrag 16f – Bachbett mit dem Water-Plugin, Engine-Plugins, Witcher-4-Technik

Stand 12.10.2026. Der Bericht hat drei Teile: **A** Bachbett mit dem Water Brush (Punkte 1–5), **B** Engine-Plugins aus eurer Liste (Nachtrag 22:55)
und **C** die Technik der Witcher-4-Demo (Nachtrag 23:15).

**Quellenlage:** Aus der Cloud waren dev.epicgames.com, das Epic-Forum, der Bugtracker, 80.lv, Reddit, YouTube und die Seiten von CDPR und der Presse
gesperrt. Alle Belege stammen deshalb aus Suchmaschinen-Auszügen. Jede Aussage ist nach Herkunft gekennzeichnet; Ableitungen sind als solche markiert.

## Gesamtfazit (Koordinator)

1. **Die Befunde 1 und 4 (Batch-Größe, Geisterformen) sind sehr wahrscheinlich Engine-Fehler, kein Bedienfehler.**
   - Bekannt ist UE-221427: Bei einer nicht quadratischen Landschaftsauflösung (bei uns 9577 × 7057) legt der Water Brush die Verformungen an falsche Stellen.
   - Für Landschaften über 8 km gibt es Berichte, die laut Forum bis 5.7 nicht behoben sind.
   - Der Brush Manager legt Render Targets in Landschaftsgröße an. Das erklärt die +20 GB.
   - Prüfschritte stehen in Teil A, Abschnitt 1.3: Skalier-Test, `landscape_rt_res`, CVars auflisten, Spline auf höchstens 15 Punkte verdünnen.
2. **Curl Noise immer auf 0.** Curl Noise ist seit 2020 als fehlerhaft gemeldet und vermischt bei 40 m Abstand die beiden Hälften der U-Schleife. Struktur im Bett kommt stattdessen aus Displacement oder aus Rauschen im eigenen Delta.
   - Falloff: Width-Modus, Blend „Min“, in Schluchten 1 m Falloff und 1,5 m Rampe.
   - Tiefe und Breite nur über die Splinepunkte. Laut Doku gilt Channel Depth nur für Seen.
3. **Euer Festschreib-Weg (Brush auslesen → Korridor-Delta → Basisebene → Brush Manager löschen) ist der übliche und richtige.** Er braucht drei Ergänzungen:
   - eine Korridor-Maske;
   - zwei gleiche Lesungen nach `landscape.ForceLayersFullUpdate`;
   - `affects_landscape = False` an allen Wasserkörpern der Welt, sonst legt der Editor den Brush Manager neu an.
   - Epics „Collapse“ ist schlechter: destruktiv, unter World Partition müssen alle Teile geladen sein, und die Geisterformen würden mit eingebacken.
4. **Epic hat für Flussbetten in großen Welten nichts Besseres als Brush oder vorgeformtes Bett.**
   - Mesh Partition Water ist experimentell und gilt nur für Mesh Terrain. Für uns: nein.
   - Landmass nutzt dieselbe alte Technik.
   - Landscape Patch bleibt eine Option, um das Bett nicht-destruktiv zu halten.
   - PCG Water Interop ist gut zum Ausstatten des Ufers (Kies, Steine, Totholz aus Breite und Tiefe der Spline).
5. **Shallow Water River nach dem Festschreiben (Befund 7):** die Spline von der Bettform lösen. Startwerte:
   - Breite = Bett + 2 m;
   - `match_spline_height_amount` ≈ 0,05;
   - `source_size` = Bachbreite;
   - `remove_outside_spline` 50 nur als Sicherheitsnetz.

   Ziel: mindestens 95 % der nassen Zellen im Bett. Die Testmatrix steht in Teil A, Abschnitt 4.3.
6. **Witcher 4:** Flüsse liefen sehr wahrscheinlich mit Water Body River + gebackenem Shallow Water River, also unser Weg. Das ist ein Indiz aus der Talk-Ankündigung eines Epic-Ingenieurs, keine Primärquelle.
   - Kerntechnik der Demo: FastGeo Streaming, Nanite Foliage (Assemblies, Voxel, Dynamic Wind), Runtime-GPU-PCG statt Landscape-Gras, Mass, ML Deformer, UAF.
   - Wie das Flussbett entstand und ob ein Wasserfall vorkommt, ist nicht belegt.
7. **Plugins** (Details in Teil B):
   - **Jetzt einschalten:** PCG Water Interop, Geometry Script (+ PCG Geometry Script Interop), World Streaming Insights.
   - **Testen** (Kopie bzw. Testkarte):
     - FastGeo Streaming (größter erwarteter Nutzen);
     - Landscape Patch;
     - PCG Biome Core/Sample;
     - Dynamic Wind + Nanite Assembly Editor Utils (Nanite-Foliage-Pilot in einem Waldbiom);
     - Runtime-GPU-PCG für Gras und Kleinkram (Empfehlung Nr. 1 aus Teil C).
   - **Aus lassen:** Mesh Partition, Mesh Terrain und Mesh Partition Water (erste experimentelle Fassung, viele Streaming-Fehler, Umbau der ganzen Landschaft), Landmass, Buoyancy, Volumetrics.
   - **Wichtig:** Das Plugin „Water“ steht bei euch auf „aus“. Bitte in der `.uproject` ausdrücklich aktivieren, weil Water Advanced und der Water Body es brauchen. Water Extras vor dem Packen ausschalten.
   - Vor dem Einsatz von Procedural Vegetation Editor bzw. Nanite Foliage in der Welt einen kleinen Package-Test machen. Ein Forenbericht zu 5.8 meldet Abstürze im gepackten Spiel.

**Rückfragen:** stehen am Ende der Teile A–C. Am wichtigsten: Lokal die Epic-Seite „Baked River Simulations – Parameter Reference“ öffnen und die
Bedeutung von `match_spline*` und `source_size` bestätigen. Aus der Cloud war sie gesperrt.

---

## Teil A – Bachbett mit dem Water-Plugin

Stand 12.10.2026. Bearbeitet sind die Punkte 1–5 aus Auftrag 16f. Grundlage sind die Befunde 1–7 aus dem Auftrag und die Antworten 16, 16a, 16b, 16c und 16e.

**Quellenlage (bitte beachten):**
- `dev.epicgames.com`, `forums.unrealengine.com`, `issues.unrealengine.com`, `80.lv`, `reddit.com` und die Übersetzungs-Spiegel waren aus der Cloud gesperrt (Proxy 403). WebFetch lieferte für jede Adresse einen DNS-Fehler.
- Alle Belege stammen deshalb aus **Suchmaschinen-Auszügen** der verlinkten Seiten. Volltexte habe ich nicht gelesen.
- Das Suchkontingent dieser Sitzung (200 Suchen) war am Ende aufgebraucht. Zwei Nachfragen blieben offen (Abschnitt 6).
- YouTube-Titel nenne ich nur als Titel.

**Kennzeichnung:**
- [Doku]: Epic-Doku oder API, Auszug
- [Bug]: Epic-Bugtracker, Auszug
- [RN 5.8]: Release Notes 5.8, Auszug
- [Forum]: Epic-Forum, Auszug
- [Blog]: Drittquelle
- [Fach]: Fachliteratur Geomorphologie
- [Ableitung]: aus Belegen und unseren Befunden geschlossen
- [unsicher]: nicht belegt, im Test klären

---

## Kurzfazit

1. **Befunde 1 und 4 sind sehr wahrscheinlich bekannte Fehler des Water Brush bei großen und nicht quadratischen Landschaften.** Es sind keine Bedienfehler.
   - UE-221427: „Water Brush incorrectly captures rivers with non-square landscape resolution“. Flussverformungen landen an zufälligen Stellen [Bug].
   - UE-256695: Der Brush Manager legt **elf Render Targets** in Landschaftsgröße an, aufgerundet auf eine Zweierpotenz [Bug].
   - Unsere Landschaft ist 9 577 × 7 057, also nicht quadratisch und über 8 km. Für genau diesen Fall gibt es zwei Forenfäden mit „Geisterformen“ neben dem Fluss [Forum].
2. **Curl Noise ist seit 2020 als fehlerhaft gemeldet** (Ränder verformen sich und sinken ein) [Forum]. Bei uns: Curl Noise immer **0**. Wer Struktur im Bett will, nimmt **Displacement** oder Rauschen im eigenen Delta.
3. **Ferats Weg (auslesen → Korridor-Delta in die Basisebene → Brush weg) ist sinnvoll.** Er entspricht dem in Foren üblichen Weg: Bett vorab formen, die Wasserkörper mit „Affects Landscape“ aus betreiben.
   - Er ist besser als Epics „Collapse“. Collapse ist destruktiv, braucht unter WP alle Teile geladen und würde die Geisterformen mit einbacken.
   - Zwei Pflichtschritte fehlen noch:
     1. zweimal lesen und vergleichen (Determinismus);
     2. **vorher** an allen Wasserkörpern „Affects Landscape“ aus. Sonst legt der Editor den Brush Manager beim nächsten Start neu an [Forum].
4. **Epic hat für Flussbetten in großen Welten kein besseres fertiges Werkzeug.**
   - Mesh Partition Water ist experimentell. Laut Doku ist „nicht alle Carving-Funktion übertragen“, und es gilt nur für Mesh Terrain.
   - Landmass nutzt dieselbe alte Brush-Technik.
   - Landscape Patch eignet sich zum **Festhalten** (Texture Patch, „Reinitialize Heights“), nicht zum Graben.
   - PCG Water Interop liest die Spline (Breite, Tiefe, Tempo) für Bewuchs, Kies und Holz.
5. **Shallow Water River:**
   - Nach dem Festschreiben ist die Spline frei. Ihre Breite muss nicht mehr gleich der Bettbreite sein.
   - Wasser folgt dem Bett, wenn `match_spline_height_amount` klein ist (0–0,1), `source_size` ≈ Bachbreite (2–6 m statt 10 m) und `remove_outside_spline` nur als Sicherheitsnetz dient.
   - Diese Werte sind nicht dokumentiert, daher die Testmatrix in 4.3.

---

## 1. Best Practice: Flussbett mit Water Brush in großen WP-Landschaften

### 1.1 Befunde aus Quellen

**Befund 1 – Batch-Größe 7057×4537 und +20 GB Speicher**

- **Render Targets des Brush Managers (UE-256695)** [Bug]:
  - Text: „When a Water Body River is added to a Scene with a Landscape, eleven Render Targets are allocated … sized according to the resolution of the Landscape“.
  - Sie werden auf die nächste Zweierpotenz aufgerundet. Beispiel aus dem Bericht: 5121 → 11 × 8192.
  - Betroffen ist 5.5, Ziel-Fix 5.6 (Commit 41105785). Ob der Fix in 5.8.3 steckt, ist nicht belegt.
- **Eigenschaft `landscape_rt_res`** [Doku Python]: Sie ist an `WaterBrushManager` nur lesbar und zeigt diese Größe.
- **Hochrechnung für uns** [Ableitung, Format der Targets nicht belegt]:

  | Fall | Pixel je Target | 11 × RGBA16F (8 B) | 11 × RGBA32F (16 B) |
  |---|---|---|---|
  | ohne Fix (Zweierpotenz 16384 × 8192) | 134 M | 11,8 GB | 23,6 GB |
  | mit Fix (genau 9577 × 7057) | 67,6 M | 5,9 GB | 11,9 GB |

  Ferats „+20 GB Editor-Zusage“ passt zur Größenordnung „ohne Fix, 32 Bit“ oder „mit Fix, plus Zwischenpuffer“. Der Speicher hängt an der **Landschaftsgröße**, nicht am Fluss. Mit keiner CVar wird er kleiner.
- **CVar `landscape.BatchedMerge.MaxResolutionPerRenderBatch`:** Dazu gibt es keine öffentliche Doku, keinen Forenbericht und keinen Eintrag in den Release Notes 5.4–5.8.
  - Belegt ist nur das Prinzip [Doku, API `FMergeRenderContext`/`FMergeRenderBatch`]: Ein Batch ist „a set of weightmaps (or the heightmap) to render on a portion of the world“. Edit-Layer-Renderer arbeiten auf „a limited set of components (depending on the size of the render batches)“.
  - Blueprint-Brushes laufen im Modus „global merge“.
- **Ableitung:** Ein alter Blueprint-Brush wie der Water Brush muss seinen **ganzen Einflussbereich in einem Batch** rendern. Darum erzwingt er einen Batch von 7 057 × 4 537 Punkten (≈ 7 × 4,5 km). Das Maximum von 1024 wird ignoriert („läuft trotzdem“).
  - Wichtig: Für einen 405-m-Fluss ist ein Einflussbereich von 7 × 4,5 km viel zu groß. Der Brush rechnet also über weite Teile der Welt. Das stützt Befund 4.
- **5.8:** `landscape.ForceLayersUpdate` ist veraltet. Neu heißt es **`landscape.ForceLayersFullUpdate`** [RN 5.8]. In 5.8 gibt es außerdem eine „Landscape brush optimization“ (ohne Details) und einen Absturzschutz des Water Brush bei OnLevelAdded/Removed [RN 5.8].
- **Speicherfehler (UE-355956):** Ein Bug meldet zu hohen Speicher über `landscape.ForceLayersUpdate 1` im Landscape Mode, betroffen 5.6/5.7, Ziel-Fix 5.8, Status offen [Bug].

**Befund 4 – fremde Ellipsen und Balken 40–65 m neben dem Bach**

- **UE-221427** [Bug]: Bei **nicht quadratischer Landschaftsauflösung** fängt der Water Brush die Flüsse falsch ein.
  - Die Verformungen landen an zufälligen Stellen und sind nicht unbedingt zusammenhängend.
  - Ist der Zustand einmal kaputt, sind auch **neu angelegte** Flüsse kaputt.
  - Edit Layers aus- und einschalten hilft nicht, solange Wasserkörper in der Ebene sind.
  - Workaround laut Eintrag: **alle** Wasser-Assets der Ebene löschen, Edit Layers aus/an, speichern, neu laden, dann neu anlegen. Status laut Auszug: ungelöst.
- **„Rivers are invisible on the landscape with size more than 8×8 km“** [Forum]: Der Fluss fehlt in der Verformungstextur, auf kleineren Karten nicht. Spätere Antworten: Der Fehler besteht **noch in 5.6 und 5.7**.
- **„Broken rivers when landscape size is too large“** [Forum]:
  - Bild: Flussform seltsam, „pieces of terrain are automatically generated on one side of the river“. Das entspricht unseren Balken neben dem Bach.
  - Vermutung des Autors: Der Abtastbereich des Flusses ist zu groß; die Punkte liegen „too far out and not part of the river bed“.
  - Workaround dort: Querschnitt mit einem Hydro-Werkzeug selbst formen.
- **UE5.1-Faden** [Forum]: Zwei weitere Ursachen für verzerrte Flüsse:
  - zu viel Höhe in Z;
  - **zu viele Splinepunkte in einem Fluss** („after about 15 it will start to happen“) [Forum, unsicher]. Wir haben 75 Punkte.
- **`WaterBodyBrushCacheContainer`** [Doku Python]: Es gibt nur Name und Signatur. `get_water_cache_key` gibt Container + Cache zurück, `cache` ist eine Map Akteur → Objekt. Wann der Cache geleert wird, steht nirgends.
- **WP-Probleme mit dem Water Brush allgemein** [Forum, mehrere Fäden 5.2–5.4]:
  - Nach dem Hinzufügen eines Wasserkörpers bleiben alle Landschaftsteile geladen. „Known issue but likely requires a refactor of the landscape system“.
  - Abhilfe dort: abgeleitete Wasserkörper mit „Affects Landscape“ aus; im Brush Manager „Affect Heightmap“ aus; Brush Manager löschen („regenerated next editor start“).
- **Ableitung:** Unser Befund passt besser zu **UE-221427 / große Landschaft** als zu Formen aus ungeladenen Zellen:
  - Der Brush Manager meldet nur einen Körper, und die Formen bleiben auch mit frischem Manager.
  - Der Einflussbereich (7 × 4,5 km) ist viel größer als der Fluss.

  Ein Test, der beides trennt, steht in 1.3 (T-A).

**Befund 5 – nicht deterministisch**

- Es gibt keinen direkten Bericht.
- Mögliche Ursachen [Ableitung]:
  - Die Höhen werden gelesen, bevor der (verteilte) Merge fertig ist.
  - Der übergroße Batch erzwingt einen Sonderpfad.
  - UE-221427 schreibt verschoben, abhängig vom Zustand.
- Der Jump-Flood-Algorithmus, den man hinter der Abstandsberechnung des Brush vermutet, ist nur näherungsweise genau, aber bei gleicher Eingabe gleich [Blog Wikipedia-Auszug; dass Epic ihn nutzt: unsicher]. Er erklärt 21 m Unterschied nicht.

**Befund 3 – Curl Noise vermischt die U-Schleife**

- Forenfaden „Water Body River actor renders strangely when curl noise is applied“ [Forum]: Ränder verformen sich und sinken unter die Landschaft. Laut Antworten ist der Fehler bekannt seit Anfang 2020 und auch in UE5 da.
- Epic-Doku: Curl Noise „adds procedural distortion to the Water Body's spline“ [Doku]. Standard: Amount 0/0, Tiling 16/3 [Doku Python].
- **Ableitung:** Curl Noise verschiebt die **Lage**, an der der Brush seine Flussform nachschlägt, nicht nur die Höhe. Liegen zwei Schleifenhälften 40 m auseinander, holt eine verschobene Abfrage die Höhe der anderen Hälfte. Darum hilft auch 0,05/0,02 nicht.

**Befund 6 – Falloff schneidet die Wände**

- Epic-Doku [Doku]:
  - **Angle-Falloff** „extends … at a specified angle until an intersection with the landscape terrain occurs“.
  - **Width-Falloff** nimmt eine feste Breite, unabhängig vom Gelände.
  - **Alpha Blend** hebt **und** senkt; **Min** senkt nur; **Max** hebt nur; **Additive** arbeitet relativ (laut Forum Gefahr großer Klippen).
- Forum „fix jagged edges“: Zacken an Flussrändern entstehen, wo das Bett steiler als etwa 25° ist. Abhilfe dort: Auflösung erhöhen, glätten, Fluss breiter, Felsen an die Kante [Forum].
- **Ableitung:**
  - In einer Schlucht mit Wänden steiler als der Falloff-Winkel liegt die Falloff-Fläche immer **unter** der Wand. Angle schneidet deshalb bis zum Schnittpunkt hoch.
  - Width schneidet um seine ganze Breite in die Wand.
  - Ferats Messung (Falloff 1 m + Rampe 1,5 m → 0 Zellen > 10 m neben der Mitte geändert) ist deshalb die richtige Richtung.

**Befund 2 (zur Bestätigung)**

- Epic-Doku: „Channel Depth applies only to Lake water bodies, since River depth is set per spline point“ [Doku].
- Die Kurve (Elevation Curve) wird mit der Tiefe je Splinepunkt multipliziert [Doku].
- Euer Befund „ChannelDepth ändert nichts“ ist also **dokumentiertes Verhalten**.

### 1.2 Ferats Weg zum Festschreiben – sinnvoll und üblich?

**Ja**, mit den Ergänzungen unten.

- **Üblich in Foren:** „Affects Landscape“ aus und mit vorgeformten Betten arbeiten („working with presculpted river beds“). Die Wasserkörper behalten Spline, Breite, Tiefe, Wellen und Material [Forum, mehrere Fäden]. Gaea- und Houdini-Nutzer formen das Bett außerhalb und richten die Splines danach aus [Forum Gaea, Blog].
- **Epics eingebauter Weg „Collapse All Layers“** [Doku]: Er klappt alle Ebenen destruktiv in die Basisebene und **entfernt alle Blueprint-Brushes**. Bei uns ist das schlechter:
  1. Unter WP müssen alle Landschaftsteile geladen sein. Laut SideFX-Doku markieren Ebenen-Operationen alle geladenen Teile als geändert und speichern sie [Blog SideFX].
  2. Collapse backt die Geisterformen aus Befund 4 mit ein.
  3. Auch die Houdini-Basis wird mit der Wasserebene verschmolzen, und die Trennung geht verloren.
- **Landscape Texture Patch als Alternative** [Doku Landscape Patch System]:
  - „Reinitialize Heights“ fängt die aktuellen Höhen unter dem Patch ein und backt sie in die Patch-Textur.
  - Das wäre ein **nicht-destruktiver** Speicher je Fluss: Patch über den Korridor legen, Brush rechnen lassen, Reinitialize, Brush weg.
  - Risiken:
    - 5.8-Forenfaden: Der Modus „Texture Backed Render Target“ legt manchmal eine flache Platte statt der Höhen an [Forum, ungelöst]. Wenn überhaupt, den internen Texturmodus nehmen.
    - Ob ein Patch die Höhen **mit** oder **ohne** die Ebenen über ihm einfängt, ist nicht belegt [unsicher].
  - Deshalb nur als Option für später.

### 1.3 Empfehlungen mit Zahlen (Befunde 1, 3–6 und Festschreiben)

**Speicher und Batch (Befund 1)**

1. `print(bm.get_editor_property('landscape_rt_res'))` am Brush Manager lesen und notieren.
   - 16384 bei einer Achse → Fix UE-256695 fehlt in 5.8.3.
   - 9577 × 7057 → Fix ist drin; der Speicher kommt dann aus der Größe selbst.
2. CVars lokal auflisten, weil es keine Doku gibt:
   - `DumpConsoleCommands landscape.BatchedMerge`
   - `help landscape.BatchedMerge.MaxResolutionPerRenderBatch`
3. **CVar-Empfehlung [unsicher]:** `MaxResolutionPerRenderBatch` auf **8192** setzen, nur für die Brush-Sitzung.
   - Das spart keinen Speicher, entfernt aber den Sonderpfad „Mindest-Batch > Maximum“.
   - Prüfen, ob dann Befund 5 verschwindet (T-C).
   - Danach für normales Malen und Formen auf 1024 zurück.
4. **Brush-Sitzung isolieren:** Nur Region um C2 laden (Region ≈ Fluss-Box + 256 m), keine anderen Wasserkörper laden. Bei 64 GB RAM / 24 GB VRAM: Editor nach jeder Brush-Sitzung neu starten [Ableitung].

**Geisterformen (Befund 4) – Testreihe T-A**

1. Ellipsen und Balken aus Lauf 1 als Maske speichern.
2. Die C2-Spline um den Landschaftsursprung strecken und vergleichen: X × 7057/9577 oder Y × 9577/7057, und dasselbe um die Landschaftsmitte.
   - **Deckt sich eine Form → UE-221427** (Achsenmaßstab falsch).
3. Spline auf **≤ 15 Punkte** verdünnen (gleiche Form, `CURVE_AUTO`) und neu rechnen. Verschwinden die Formen, ist es der Punkt-Effekt aus dem 5.1-Faden.
4. Workaround aus UE-221427 nur in einer **Kopie der Karte**:
   - alle Wasserkörper der Welt löschen (nicht nur geladene);
   - Edit Layers aus/an; speichern; neu laden;
   - nur C2 neu anlegen.
5. Bleiben die Formen: Sie entstehen aus der Größe (Faden > 8 km). Dann gilt: **Korridor-Maske beim Festschreiben ist Pflicht** (unten).

**Determinismus (Befund 5) – Testreihe T-C**

Vor jedem Auslesen:

```python
unreal.SystemLibrary.execute_console_command(None, 'landscape.ForceLayersFullUpdate')   # 5.8-Name [RN 5.8]
## danach einige Editor-Ticks warten (z. B. 120 Frames bzw. 5 s per Slate-Tick-Callback), dann lesen
h1 = sample_landscape_heights(korridor)
## erneut ForceLayersFullUpdate + warten
h2 = sample_landscape_heights(korridor)
assert max(abs(h1 - h2)) < 0.01   # 1 cm
```

- Nur festschreiben, wenn zwei Lesungen **≤ 1 cm** auseinanderliegen.
- Unterscheiden sich zwei **Brush-Läufe** weiter in tausenden Zellen, liegt es am Brush selbst und nicht am Auslesen. Dann gilt der Lauf mit der kleinsten Abweichung zum Soll-Profil (Mitte ±0,15 m wie in Befund 2), und die Korridor-Maske schneidet den Rest ab.

**Curl Noise (Befund 3)**

- Curl 1/2 Amount **0/0** für alle Flüsse. Das ist auch Epics Standard.
- Struktur im Bett kommt aus Displacement (Abschnitt 3) oder aus eigenem Rauschen im Delta: 0,1–0,3 m, Wellenlänge 1–3 m, nur innerhalb der Wasserbreite.

**Falloff (Befund 6)**

- Immer **Width-Modus**, Blend Mode **Min** (nur senken). Damit können keine Balken über dem Gelände entstehen [Doku zu Min].
- Breite nach Platz zur Wand. Regel [Ableitung]: Falloff + Rampe ≤ 0,5 × Abstand Wasserkante → Wandfuß.

  | Lage | Falloff Width | Curve Ramp Width |
  |---|---|---|
  | Schlucht (Wand ≤ 4 m neben dem Wasser) | **1,0 m** | **1,5 m** (Ferats Wert) |
  | Kerbtal (4–10 m) | 1,5–2 m | 2 m |
  | Talboden, Fluss 15–30 m | 3–4 m | 3–5 m |

- Edge Offset 0; Z Offset 0.
- Kontrolle wie bisher: 0 Zellen > 10 m neben der Mitte geändert, ≤ 10 Zellen > 5 m.

**Festschreiben (Ergänzungen zu Ferats Weg)**

1. **Korridor-Maske:** halbe Wasserbreite + Rampe + Falloff + **2 m**, entlang der Spline, nicht als Rechteck.
   - Außerhalb Delta = 0 (schneidet Geisterformen weg).
   - Innerhalb nur Delta ≤ +0,10 m zulassen (Blend Min ⇒ es sollte ohnehin ≤ 0 sein).
   - Zellen mit |Delta| > Spline-Tiefe + 1 m melden (Plausibilität).
2. Zwei gleiche Lesungen (oben), dann schreiben.
3. **Vor** dem Löschen des Brush Managers:
   - an **allen** Wasserkörpern der Welt `affects_landscape = False` setzen, auch in ungeladenen Zellen (per WP-Builder oder abgeleitete Klasse mit Standard „aus“);
   - die Ebene „Water“ leeren oder entfernen.

   Sonst entsteht der Manager beim nächsten Editor-Start neu und gräbt doppelt [Forum].
4. Die Ebene „Houdini“ bleibt Basis. Das Delta gehört wie bisher in die Weltdaten, damit Planer und Prüfer es sehen (Doppel-Delta-Schutz aus 16d beachten).

---

## 2. Alternativen in 5.8 und was Epic nutzt

### 2.1 Befunde

| Werkzeug | Was es kann (Beleg) | Für unser Bachbett |
|---|---|---|
| **Water Brush** (Water, Landschaftsebene „Water“) | gräbt nach Spline, Breite/Tiefe je Punkt, Kurve, Falloff, Effekte, Gewichte [Doku] | nur als **Werkzeug zum einmaligen Formen**, danach festschreiben (Abschnitt 1) |
| **Landscape Patch** (Plugin LandscapePatch, bei uns aus) | Patches auf eigener Patch-Ebene, ins Ergebnis gebacken. Texture Patch mit „Reinitialize Heights/Weights“, Circle Height Patch (flacher Kreis mit linearem Auslauf) [Doku]. 5.8: Absturz-Fix bei BP-Eigenschaften [RN 5.8]; 5.8-Fehler im RT-Modus [Forum] | gut zum **Halten** eines Korridor-Deltas je Fluss (verschiebbar, abschaltbar); kein Graben entlang einer Spline belegt |
| **„Water Body Landscape Patch“** | Kein Werkzeug dieses Namens gefunden [unsicher] | – |
| **PCG Water Interop** (bei uns aus) | Knoten „Get Water Spline“ liefert Punkte entlang der Wasser-Spline mit Metadaten (Tiefe, Breite „from center“, Tempo); seit 5.4, „WIP“ [Doku, Forum] | Kies, Steine, Totholz, Ufer-Bewuchs an der **echten** Spline ausrichten; formt kein Gelände |
| **Mesh Partition + Mesh Terrain + Mesh Partition Water** (alle Exp., aus) | Wasser über RiverModifier/LakeModifier an einer Mesh Partition. Doku: nicht alle Carving-Funktionen der Landschafts-Integration sind übertragen. Forum: RiverModifier versagt auf konvertiertem Gelände [Doku, Forum, Blog] | **nein** für Eldarien: anderes Geländesystem, experimentell, Carving unvollständig |
| **Landmass** (Beta, aus) | Blueprint-Brushes, gleiche Effekt-Strukturen (Curl, Displacement, Smooth, Terracing) [Doku] | gleiche alte Brush-Technik, gleiche WP-Probleme; kein Gewinn |
| **Heightfield-Werkzeuge außerhalb** (Houdini, Gaea) | Bett in Houdini-Heightfield formen, Spline separat, Wasserkörper mit Carving aus. Houdini: Flow Field, Masken; Gaea: Spline-Export per Skript [Blog SideFX, Forum Gaea] | **Industrie-Normalfall** für große Welten; entspricht unserem Planer + Delta |

**Was Epic in Beispielen gemacht hat** (kurz; Witcher 4 ausführlich bei einem anderen Agenten):

- **Electric Dreams** (4 × 4 km): Flussbett und Bach sind **prozedural mit PCG** gebaut. Die Ebene `PCGCloseRange` „only contains the procedural river bed and creek area“ [Doku]. Ob dort der Water Brush gräbt, ist nicht belegt [unsicher].
- **Valley of the Ancient**: Wüste (Moab-Scans, 2 × 2 km), kein Fluss belegt [Doku].
- **Witcher-4-Demo (UE 5.6)**: Epics Tutorial nennt den **Shallow Water River** (Water Advanced) als „featured at Unreal Fest 2025 in Orlando“ [Doku]. Dass er **in** der Witcher-Demo lief, sagen nur Community-Quellen [Forum, unsicher]. Wie das Bett geformt wurde, ist nicht veröffentlicht.

### 2.2 Empfehlung

- **Weg bleibt:** Water Brush nur als Formwerkzeug je Fluss, Ergebnis per Korridor-Delta festschreiben, danach `affects_landscape = False` überall.
- **Landscape Patch** als zweite Stufe testen (eine Kopie von C2): Texture Patch 512 × 64 über den 405-m-Lauf, interner Texturmodus, „Reinitialize Heights“.
  - Vorteil: Das Bett bleibt einzeln verschiebbar und abschaltbar.
  - Nur übernehmen, wenn der eingefangene Stand ±2 cm zum Delta passt.
- **PCG Water Interop einschalten**, sobald die Ausstattung (Kies, Steine, Holz) aus dem Planer an die echte Spline angepasst werden soll. Kein Muss für das Bett.
- **Mesh Partition Water: nicht** (Begründung in der Tabelle).

---

## 3. Einstellungen für natürliche Gebirgsbäche

### 3.1 Befunde (Namen und Standardwerte)

| Gruppe | Feld (Python) | Standard | Bedeutung (Beleg) |
|---|---|---|---|
| Kurve | `use_curve_channel` | True | Kanal unter dem Wasser an/aus [Doku] |
| | `elevation_curve_asset` | None | Querschnitt; X und Y 0–1, **Y × Tiefe je Splinepunkt** [Doku] |
| | `channel_edge_offset` | 0 | Abstand Wasserkante → Beginn der Kurve [Doku] |
| | `channel_depth` | 0 | **nur Seen** [Doku] |
| | `curve_ramp_width` | **512** (cm) | Breite der Kurve in Welteinheiten [Doku] |
| Falloff | `falloff_mode` | – | Angle oder Width [Doku] |
| | `falloff_angle`, `falloff_width` | – | Winkel bis Schnitt mit Gelände bzw. feste Breite [Doku] |
| | `edge_offset`, `z_offset` | 0 | flacher Versatz vor dem Falloff; Höhe der Schnittfläche [Doku] |
| Mischen | `blend_mode` | Alpha Blend | Alpha (hoch+runter), Min, Max, Additive [Doku] |
| Effekte | Curl `curl1/2_amount`, `curl1/2_tiling` | 0/0, 16/3 | Verzerrung der Spline [Doku] |
| | Displacement `displacement_height`, `displacement_tiling`, `texture`, `midpoint`, `channel`, `weightmap_influence` | Mitte −128 (4.26), Kanal A | Höhe aus Textur [Doku Python] |
| | Smooth Blending `inner/outer_smooth_distance` | 0,01/0,01 | weiches Einblenden innen/außen [Doku Python, Landmass] |
| | Blurring, Terracing | – | Felder in 5.8 per `dir()` prüfen [unsicher] |
| Gewichte | `layer_weightmap_settings` (Map Ebene → `WaterBodyWeightmapSettings`) | `falloff_width` 512 (min 0,1), `edge_offset` 0, `modulation_texture`, `texture_tiling` 4, `texture_influence` 0,5, `midpoint` 0,5, `final_opacity` 1 (Werte aus 5.0) [Doku] | Ebene unter dem Wasser malen |

**Forenrezepte mit Zahlen:** Es gibt kaum welche.

- Gefunden: „Default Falloff ist ein guter Start“ (Gumroad-Autor) [Blog].
- „Angle größer gegen platt gemachte Landschaft“ [Forum].
- „Ab 25° Bettneigung Zacken“ [Forum].
- „FixedWaterDepth und FixedZOffset im Wassermaterial an“ gegen nicht anliegende Flüsse [Forum, 5.1].

Fertige Gebirgsbach-Rezepte mit Zahlen gibt es in den gefundenen Quellen nicht. Die Werte unten sind deshalb aus Doku, euren Messungen und der Geomorphologie abgeleitet.

**Geomorphologie (für die Becken-Schnellen-Folge)** [Fach]:
- **Gefälleklassen (Montgomery & Buffington 1997):** Riffle-Pool < 1,5 %, Plane Bed 1,5–3 %, Step-Pool 3–6,5 %, Cascade > 6,5 %.
- **Abstand der Becken:** Beim Pool-Riffle liegen die Becken 2–4 Breiten auseinander (Montgomery et al. 1995, wenig Holz). Step-Pool-Abstände aus der Arbeit von 1997 konnte ich nicht nachlesen [unsicher].
- **Stufensteilheit:** H/L liegt zwischen 1 und 2 × Gefälle S (Abrahams et al. 1995; Feldstudien in den Adirondacks und im Lake District). Eine Preprint-Kritik von 2026 zweifelt das Modell an, nicht die Spannweite.
- **C2 mit 36 % mittlerem Gefälle (16a)** ist ein **Cascade-Bach**. Dort sind Becken kurz und Fälle häufig. Das passt zur bisherigen Planerlogik.

### 3.2 Empfehlungen für unsere Lage (Bäche 2–30 m, enge Schluchten)

**Kanal**

| Feld | Bach 2–6 m (Schlucht) | Bach/Fluss 6–15 m | Fluss 15–30 m |
|---|---|---|---|
| `use_curve_channel` | an | an | an |
| `elevation_curve_asset` | **eigene Kurve „Kasten-U“** (s. u.) | Kasten-U | „flaches U“ |
| `channel_edge_offset` | 0 | 0 | 0,5 m |
| `curve_ramp_width` | **1,5 m** (statt 5,12) | 2–3 m | 3–5 m |
| Tiefe je Splinepunkt | Becken 0,6–1,2 m, Rinne 0,2–0,4 m | Becken 1,0–1,8 m, Rinne 0,3–0,6 m | Kolk 1,5–3 m, Furt 0,4–0,8 m |
| Breite je Splinepunkt | Becken 1,2–1,4 × Rinne | 1,2–1,3 × | 1,1–1,2 × |

- **Kasten-U** (X = 0 Wasserkante … 1 Mitte, Y = Anteil der Tiefe): (0; 0), (0,15; 0,55), (0,35; 0,9), (1; 1). Steile Ränder, flacher Grund wie bei Gebirgsbächen mit Grobblock-Ufern.
- **Flaches U:** (0; 0), (0,3; 0,6), (0,6; 0,9), (1; 1).
- Ob X von der Kante zur Mitte läuft oder umgekehrt, ist nicht belegt → an einem 6-m-Stück einmal ansehen [unsicher].
- **Splinepunkte:** an Übergängen Becken ↔ Rinne höchstens 2 m Abstand, sonst ≤ 5 m. Gesamt so wenig wie möglich. T-A Schritt 3 zeigt, ob > 15 Punkte stören.

**Falloff:** wie in 1.3 (Width-Modus, Blend Min, 1 / 1,5 m in der Schlucht).

**Effekte**

| Effekt | Wert | Grund |
|---|---|---|
| Curl Noise | **0 / 0** | Befund 3, Forenfehler |
| Displacement | Textur: kachelbare Kies-/Blockhöhenkarte (z. B. aus einem Megascans-Displacement); `displacement_height` **0,15–0,30 m** (Bach), 0,3–0,5 m (Fluss); `displacement_tiling` so, dass eine Kachel **2–4 m** misst; `midpoint` 0,5; `weightmap_influence` 0 | Höhe aus Weltkoordinaten. Nach dem Aufbau wird an fester Stelle nachgeschlagen, also keine Vermischung der Schleife [Ableitung]. Prüfen: max. Fehler in der U-Schleife < 0,3 m |
| Smooth Blending | inner **0,3 m**, outer **0,5 m** | weicher Übergang ohne Wandschnitt |
| Blurring | aus (oder Radius 1) | verwischt sonst Stufen |
| Terracing | aus. Optionaler Test: Stufenabstand 0,5 m, Smoothness 0,2, nur Cascade-Strecken | könnte Stufen erzeugen, aber die Tiefe je Punkt steuert das schon sauber (Befund 2) [unsicher] |

**Gewichtskarten (Kies und Schlamm im Bett)**

- Der Brush kann je Wasserkörper nur **eine** Regel je Ebene. Becken und Rinnen unterscheidet er nicht.
- Empfehlung:
  - Kies und Schlamm bleiben im **Planer** (16c: „Ruhe“ ≤ 0,4 % → Schlamm, Schnelle ab 2 % → Kies).
  - Im Brush höchstens eine Ebene „Nassstein“ oder „Kies“: `falloff_width` 1,0 m, `edge_offset` −0,3 m (endet 30 cm innerhalb der Wasserkante), `modulation_texture` Rauschen, `texture_tiling` 4, `texture_influence` 0,4, `final_opacity` 0,8.
  - Sonst Gewichte im Brush **aus**, damit beim Festschreiben nur Höhen übertragen werden.

**Becken-Schnellen-Folge über die Spline**

- **Spiegel:** Becken waagrecht, Lippe als `LINEAR`-Punkt (wie fluss_sim).
- **Abstand zwischen zwei Becken:**

  | Strecke | Abstand |
  |---|---|
  | Cascade (> 6,5 %) | 1–2 × Breite |
  | Step-Pool (3–6,5 %) | 2–4 × Breite |
  | Pool-Riffle | 4–7 × Breite |

  Die Werte stammen aus der Fachliteratur, die Spannweiten sind nur teilweise belegt.
- **Stufen:** Höhe H und Länge L so wählen, dass H/L = 1–2 × Streckengefälle. Beispiel: 10 % Gefälle, 4-m-Bach, Becken alle 10 m ⇒ H = 1,0–2,0 m Fall, verteilt auf Lippe und Rinne.
- **Becken:** Tiefe ≈ 0,3–0,5 × Fallhöhe des oberen Falls + 0,4 m. Breite 1,2–1,4 × Rinne. Länge ≥ 1,5 × Breite, damit die SWR es füllt (16b: kurze Becken < 4 m werden zusammengelegt).

---

## 4. Shallow Water River danach (Befund 7)

### 4.1 Befunde

- **Belegte Felder** [Doku Python 5.5]: `source_size` (float, ohne Beschreibung), `use_capture`, `bottom_contour_*`, `resolution_max_axis`, `sim_speed`, `num_steps`.
- `match_spline_height_amount` und `remove_outside_spline` stehen in keinem gefundenen Auszug.
- **„Remove Outside Spline Amount“** (Shallow Water → Simulation) [Blog, japanische Leitfäden]:
  - Es regelt, wie stark Wasser außerhalb der Spline entfernt wird.
  - Rat bei Überlaufen: **200**.
  - Warnung: zu starkes Entfernen sieht unnatürlich aus; besser Gelände, Tiefe und Breite anpassen oder Hindernisse setzen.
  - Ein weiterer Rat: am Water Body River `ZOffset` 100–200 heben, um die Ufer zu erhöhen.
- CAD-Center-Leitfaden: Den **ersten** Splinepunkt höher setzen ergibt natürlicheren Fluss [Blog].
- „5.6: are shallow water river destructive?“ [Forum]: Die SWR überschreibt die River-Ebene. Nach Änderungen Reset, nach dem Bearbeiten Bake.
- „5.6 ShallowWaterRiver simulation nowhere near the WaterBodyRiver spline“ [Forum]:
  - Simulation etwa 150 m zu tief.
  - Ursache vermutet: Bounds-Berechnung des Landschafts-Pivots unter WP.
  - `use_capture` aus richtet aus, fängt aber keine Hindernisse mehr.
- „Shallow Water River – Water Body River“ [Forum]: SWR passt nicht mehr zur Höhe der River-Spline, auch in fertigen Projekten. Keine Antwort.
- Epic hat eine Parameter-Referenz „Baked River Simulations – Parameter Reference“ (SWR-Akteur, Niagara, Material) [Doku]. Inhalt nicht lesbar (gesperrt). **Bitte lokal im Browser öffnen**; sie klärt die Felder vermutlich direkt.

### 4.2 Deutung von Befund 7 [Ableitung]

- Fläche = Spline-Band (99,7 %), Tiefe Median 1,25 m.
- Wahrscheinliche Wirkung der Felder:
  - `match_spline` zieht die Wasserhöhe in Richtung Spline-Spiegel. Bei uns steht es auf 2 (bei 5.8 vermutlich ein Modus oder eine Stärke).
  - `remove_outside_spline` entfernt alles außerhalb.
- Ergebnis: ein Wasserkörper, der genau das Band bis zum Spline-Spiegel füllt.
- Solange **Bettbreite = Splinebreite** (der Brush gräbt genau das Band), ist das sogar formgleich mit dem Bett. Sichtbar falsch wird es dort, wo das Bett schmaler, flacher oder versetzt ist (Rampe, Falloff 1 m, Wände).

### 4.3 Empfehlungen und Testmatrix

**Grundsatz:** Nach dem Festschreiben (Affects Landscape aus) ist die River-Spline **nur noch Strömungs- und Grenzvorgabe** für die SWR.

- Breite und Tiefe der Spline dürfen dann vom Bett abweichen.
- Ziel: Das Wasser findet seinen Spiegel aus Zufluss und Bett, die Spline hält es nur grob zusammen.

| Feld | jetzt | Start neu | Testwerte | Begründung |
|---|---|---|---|---|
| `match_spline` | 2 | **1** (bzw. „nur Lage“, falls Modus) | 0 / 1 / 2 | Bedeutung von 2 erst mit `help(unreal.ShallowWaterRiverComponent)` klären [unsicher] |
| `match_spline_height_amount` | ? | **0,05** | 0 / 0,05 / 0,15 / 0,3 | kleine Stärke = Wasser folgt Bett und Zufluss, nicht dem Spline-Spiegel |
| `remove_outside_spline` | 50 | **50 lassen** | 20 / 50 / 200 | nur Sicherheitsnetz. 200 laut Blog gegen Überlaufen, aber „unnatürlich“ |
| `source_size` | 10 m | **= Bachbreite an der Quelle** (C2: 2–4 m) | 2 / 4 / 10 m | 10 m Quelle über einem 3-m-Bett flutet die Ränder am Anfang [Ableitung] |
| Spline `RiverWidth` | = Bett | **Bettbreite + 2 × 1 m** | +0 / +2 / +4 m | Band breiter als Bett: füllt die SWR dann nur das Bett, ist der Bandeffekt weg |
| Spline `Depth` | Plan | **Plan** (für Tempo/Abfluss) | – | 16e: Tempo nach Manning |
| erster Splinepunkt | Plan | **+0,3 m** über Spiegel | – | CAD-Center-Rat, besserer Anlauf |

- **Messgröße je Lauf** (WCBS, gebacken):
  - Anteil nasser Zellen innerhalb des Betts (Gelände < Planspiegel − 5 cm): Ziel **≥ 95 %**.
  - Anteil nasser Zellen im Band, aber außerhalb des Betts: Ziel **≤ 5 %**.
  - Tiefe Median gegen Plan: Becken ±0,2 m, Rinnen ±0,1 m.
- **Reihenfolge:**
  1. RiverWidth +2 m.
  2. `match_spline_height_amount` 0,05.
  3. `source_size`.
  4. Erst dann `remove_outside_spline`.

  Nach jedem Schritt Reset, einlaufen lassen, Bake (Forum: Reset/Bake-Pflicht).
- **Fällt der Spiegel zu tief**, weil das Wasser abläuft: `match_spline_height_amount` auf 0,15. Sonst die Velocity am Quellpunkt (16e) nicht senken.
- **Schaum nur an Fällen und Tempo nach Gefälle:** bleibt wie in 16e.
  - Option B Schaum-Maske, Sekundär-Emitter aus, Flowmap-Speed 0,5/1,0.
  - `WaterVelocityScalar` = `tempo_ms` × 100.
  - Zusätzlich: `Sim Foam Dpeth Min` 8 → 15–25 cm, damit dünne Rinnen ohne Fall keinen Schaum zeigen (16b-Leiter).
- **Wasser-Höhe falsch unter WP:** Liegt die SWR nach dem Festschreiben versetzt, ist es der 5.6-Fehler mit `use_capture`.
  - Prüfen: Abstand gebackener Spiegel ↔ Spline-Z.
  - Ist er > 0,5 m: `use_capture` einmal aus. Hindernisse dann über `bottom_contour_actors` (WH-Akteur) prüfen.

---

## 5. Witcher-Look: klare Bäche, Weißwasser, Steine und Totholz

### 5.1 Befunde

- **Klares Wasser (Single Layer Water)** [Doku, Forum]:
  - Eingänge: Scattering und Absorption Coefficients, PhaseG, Color Scale Behind Water.
  - Forumswerte für klares Wasser (physikalisch, je m, ×0,01 für cm): Absorption (0,35; 0,07; 0,03), Scattering (0,0007; 0,0021; 0,0025), Phase 0,1.
  - Niedrige Absorption hält den Grund sichtbar. Für Flüsse sind Reflexions-Captures und ein guter Himmel nötig, sonst wirkt das Wasser „unsichtbar, nur verschwommen“.
- **Kaustik** [Blog, Forum]:
  - Kurs Alkawadri: Kaustik auf Flussgrund per **Material-Decal**.
  - Reddit/Forum: gepannte Texturen statt berechneter Kaustik; Vier-Panner-Funktion für natürlichere Bewegung.
  - Forum: Wasser-Plugin-Kaustik nur an der Oberfläche, nicht im Unterwasser-Material.
- **Weißwasser** [Blog 80.lv-Auszüge, ArtStation]:
  - Game-„White Water“ hat drei Teile: Splash, Oberflächenschaum, Blasen.
  - Schaum aus **Vortizität** bzw. Geschwindigkeit als Maske (Houdini → UE, Reguera).
  - Schaum in mehreren Maßstäben mischen statt einer Textur.
  - Schaum an Hindernissen über Depth Fade bzw. Distance Field.
  - Flowmap kodiert Richtung und Tempo, besonders in Kurven und Schnellen.
- **Epic-Weg in 5.6+:** SWR erzeugt Weißwasser, kollidiert mit Gelände und Objekten und trägt Treibgut (Buoyancy) [Doku Tutorial-Auszug].

### 5.2 Empfehlungen für Eldarien

**Wassermaterial (`MI_EL_SWR_Klar`, Namen aus 16a)**

- **Absorption** ≈ (0,45; 0,10; 0,08) je m. Das ist leicht grünlich-klar für Gebirgsbäche mit etwas Humus. Wolfsschlucht oder Moor dunkler: (0,6; 0,25; 0,2).
- **Scattering:**
  - in Becken ≈ (0,002; 0,004; 0,004) je m;
  - in Schnellen ×5 über die Geschwindigkeit, für Luftbläschen und leicht milchiges Wasser.
- Die Einheiten in unserem Master sind nicht geprüft (16a). Erst mit einem Becken von 1,5 m Tiefe testen. Ziel: Grund bei 1 m Tiefe noch deutlich sichtbar, bei 2,5 m nur noch Umrisse.
- Refraction 1,15 lassen; Water Roughness 0,03–0,05; `Sim Velocity Normal Strength` 15 (16e).

**Kaustik**

- Eigenes Decal oder eine Materialfunktion im Landschaftsmaterial unter der Wassermaske.
- Zwei bis vier gepannte Kaustik-Texturen, Kachel 1,5–3 m, Tempo nach Flowmap.
- Stärke nach Tiefe: voll bei 0,2–0,8 m, aus ab 2 m.
- Nur bis 60 m Sichtweite.

**Weißwasser nur an Schnellen und Fällen** (Ferat)

- Simulationsschaum per Schaum-Maske (16e Option B).
- An Schnellen ohne Fall: nur Normalen und Glanz, kein Weiß.
- Niagara an Fällen bleibt (NS_Impact, Cull 45 m).
- Zusätzlich je Fall ≥ 1 m ein dünner **Bläschen-Schleier** unter Wasser im Becken, 1–2 m hinter dem Aufprall (Sprite, additiv, Tiefe < 0,8 m). Das ist das dritte Weißwasser-Teil „Blasen“, das bei uns fehlt.

**Steine und Totholz**

- **Nasse Ränder:** Feuchtelinie im Material der Felsen und Stämme = Wasserspiegel + 5–15 cm. Darunter Albedo × 0,6 und Rauheit 0,2–0,3; darüber normal.
- **Spiegel der Feuchtelinie:** gebackene Wasserhöhe oder Spline-Spiegel.
- **SWR-Kollision** für Steine ≥ 0,4 m (16a); dann entsteht die Strömungsspur hinter dem Stein aus der Simulation.
- Der DF-Schaumsaum (`Foam Distance` 256) bleibt sehr dünn (≤ 0,3 m).
- **Totholz:** Stämme quer zur Strömung (15–55°, 16c) erzeugen in der SWR Rückstau. Ihr Kollisionsnetz muss das Wasser wirklich berühren, sonst fehlt der Effekt.

---

## 6. Was offen blieb (unsicher)

- Volltexte von Epic-Seiten und Forenfäden waren nicht erreichbar. Besonders wichtig zum lokalen Nachlesen:
  1. „Baked River Simulations – Parameter Reference“ (Epic): Bedeutung von `match_spline`, `match_spline_height_amount`, `remove_outside_spline` und `source_size`.
  2. UE-221427 und UE-256695: Status in 5.8.
  3. Forenfaden „Broken rivers when landscape size is too large“: Antworten und Workarounds.
- Keine Quelle zu den CVars `landscape.BatchedMerge.*`. Liste lokal mit `DumpConsoleCommands`.
- Ob Landscape Patch und Water Brush in 5.8 noch über den alten globalen Merge laufen, konnte ich wegen des aufgebrauchten Suchkontingents nicht mehr prüfen.
- Keine Belege, wie das Bett in der Witcher-4-Demo geformt wurde.

---

## Quellen

**Bugtracker und Release Notes**
- [UE-221427 – Water Brush incorrectly captures rivers with non-square landscape resolution](https://issues.unrealengine.com/issue/UE-221427) [Bug]
- [UE-256695 – Water Brush Render Targets auf Zweierpotenz (11 Targets)](https://issues.unrealengine.com/issue/UE-256695) [Bug]
- [UE-355956 – Speicher bei landscape.ForceLayersUpdate, 5.6/5.7](https://issues.unrealengine.com/issue/UE-355956) [Bug]
- [UE-164013 – Blend-Mode-Änderung kehrt bei See zurück](https://issues.unrealengine.com/issue/UE-164013) [Bug]
- [Unreal Engine 5.8 Release Notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US) – `landscape.ForceLayersFullUpdate`, Water-Brush-Fix, Landscape-Brush-Optimierung [RN 5.8]

**Epic-Doku und API**
- [Water Body Actors in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-body-actors-in-unreal-engine) – Kurve, Falloff, Blend Mode, Curl Noise, Channel Depth nur Seen
- [Landscape Edit Layers](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-edit-layers-in-unreal-engine) – Collapse, Collapse All Layers
- [Tech Note: Landscape Edit Layers Issues](https://dev.epicgames.com/community/learning/knowledge-base/ML6e/unreal-engine-tech-note-landscape-edit-layers-issues)
- [FMergeRenderContext](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Landscape/FMergeRenderContext), [FMergeRenderBatch](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Landscape/FMergeRenderBatch)
- [Python: WaterBrushManager](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBrushManager?application_version=5.3) – `landscape_rt_res`, `get_water_cache_key`
- [Python: BrushEffectCurves (4.27)](https://docs.unrealengine.com/4.27/en-US/PythonAPI/class/BrushEffectCurves.html), [BrushEffectCurlNoise](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/BrushEffectCurlNoise?application_version=5.0), [WaterBrushEffectDisplacement (4.26)](https://docs.unrealengine.com/4.26/en-US/PythonAPI/class/WaterBrushEffectDisplacement.html), [BrushEffectSmoothBlending](https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/BrushEffectSmoothBlending.html), [WaterBrushEffects](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBrushEffects)
- [Python: WaterBodyWeightmapSettings (5.0)](https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/WaterBodyWeightmapSettings.html), [FWaterBodyWeightmapSettings](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/Water/FWaterBodyWeightmapSettings), [WaterBodyHeightmapSettings (4.27)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyHeightmapSettings?application_version=4.27)
- [Landscape Patch System](https://dev.epicgames.com/documentation/unreal-engine/landscape-patch-system), [Python: LandscapeTexturePatch 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/LandscapeTexturePatch?application_version=5.7), [ULandscapeCircleHeightPatch](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/LandscapePatch/ULandscapeCircleHeightPatch)
- [Crafting Mesh Terrain](https://dev.epicgames.com/documentation/unreal-engine/crafting-mesh-terrain-in-unreal-engine?lang=en-US), [Mesh Terrain](https://dev.epicgames.com/documentation/unreal-engine/mesh-terrain-in-unreal-engine?lang=en-US)
- [PCG Water Interop: FPCGWaterSplineMetadataStruct](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/PCGWaterInterop/FPCGWaterSplineMetadataStruct), [Python: PCGGetWaterSplineSettings](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGGetWaterSplineSettings), [UWaterSplineMetadata](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterSplineMetadata)
- [Python: ShallowWaterRiverComponent 5.5](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent?application_version=5.5)
- [Baked River Simulations – Parameter Reference](https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference) (nicht lesbar, lokal öffnen)
- [New in UE 5.6 – Water Body River → Niagara 2D Fluid Simulation](https://dev.epicgames.com/community/learning/tutorials/OZMa/new-in-unreal-engine-5-6-turn-your-water-body-river-into-a-game-ready-niagara-2d-fluid-simulation)
- [Single Layer Water Shading Model](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine)
- [Electric Dreams Environment](https://dev.epicgames.com/documentation/unreal-engine/electric-dreams-environment-in-unreal-engine?lang=en-US), [PCG in Electric Dreams](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-in-electric-dreams), [Valley of the Ancient](https://dev.epicgames.com/documentation/en-us/unreal-engine/valley-of-the-ancient-sample-game-for-unreal-engine)

**Forum**
- [Rivers are invisible on the landscape with size more than 8x8 km](https://forums.unrealengine.com/t/rivers-are-invisible-on-the-landscape-with-size-more-than-8x8-km/1406714)
- [Broken rivers when landscape size is too large](https://forums.unrealengine.com/t/broken-rivers-when-landscape-size-is-too-large/2519345)
- [Issue with Water Body River not conforming to my landscape – UE5.1](https://forums.unrealengine.com/t/issue-with-water-body-river-not-conforming-to-my-landscape-ue5-1/741308)
- [Water Body River actor renders strangely when curl noise is applied](https://forums.unrealengine.com/t/water-body-river-actor-renders-strangely-when-curl-noise-is-applied/244961)
- [Water body river: fix jagged edges](https://forums.unrealengine.com/t/water-body-river-fix-jagged-edges/1949564)
- [WorldPartition Proxies Stuck Loaded After Adding Water Body](https://forums.unrealengine.com/t/worldpartition-proxies-stuck-loaded-after-adding-water-body/1293263), [Unreal Engine rivers don't work with world partition?](https://forums.unrealengine.com/t/unreal-engine-rivers-dont-work-with-world-partition/1481966), [Adding water body forces all WP cells to display](https://forums.unrealengine.com/t/bug-adding-water-body-forces-all-world-partition-cells-to-display-that-raises-out-of-video-memory-crash/1347710)
- [Waterbody heightmap blend mode additive bug?](https://forums.unrealengine.com/t/waterbody-water-heightmap-blend-mode-additive-bug/2550446), [Water Body Ocean flattens my heightmap](https://forums.unrealengine.com/t/unreal-water-body-ocean-flattens-my-heightmap-terrain/525984)
- [UE 5.8 – LandscapeTexturePatch (Texture Backed RT) not applying captured height](https://forums.unrealengine.com/t/ue-5-8-landscapetexturepatch-texture-backed-render-target-not-applying-captured-height-data-correctly/2739327)
- [Can't get RiverWaterBody to work with converted static mesh to MeshTerrain](https://forums.unrealengine.com/t/cant-get-riverwaterbody-to-work-with-converted-static-mesh-to-meshterrain/2723987)
- [Unreal 5.6 ShallowWaterRiver simulation nowhere near the WaterBodyRiver spline](https://forums.unrealengine.com/t/unreal-5-6-shallowwaterriver-simulation-nowhere-near-the-waterbodyriver-spline/2637929), [Shallow Water River – Water Body River](https://forums.unrealengine.com/t/shallow-water-river-water-body-river/2712606), [5.6 are shallow water river destructive?](https://forums.unrealengine.com/t/5-6-are-shallow-water-river-destructive/2659509)
- [Actually realistic water shader (SLW-Koeffizienten)](https://forums.unrealengine.com/t/actually-realistic-water-shader/141661), [Water too transparent](https://forums.unrealengine.com/t/how-do-i-fix-water-being-too-transparent-no-color-screenshots/257829), [Caustics question](https://forums.unrealengine.com/t/caustics-question/242480)
- [Gaea: Water Export to Splines (UE 5.6)](https://talk.gaea.app/t/water-export-to-splines-for-unreal-engine-5-6-water-bodies/947)

**Blogs und Breakdowns**
- [ue5exp0.com – UE5.6で高品質の川](https://ue5exp0.com/water5-6/) – Remove Outside Spline Amount 200, ZOffset 100–200
- [yossi40-100.com – Shallow Water River解説](https://yossi40-100.com/ue56shallow_water_river/), [CAD Center – WaterAdvancedで道頓堀に水を流す](https://www.cadcenter.co.jp/article/cclab/cclabno28_wateradvanced/), [Historia – ShallowWaterRiver](https://historia.co.jp/archives/53937/)
- [SideFX – Houdini Engine World Partition](https://www.sidefx.com/docs/houdini/unreal/worldpartition/worldpartition.html)
- [Victor Reguera – River simulation (Houdini + UE)](https://www.artstation.com/artwork/Pez60o), [80.lv – River Simulation in Houdini & UE5](https://80.lv/articles/creating-a-river-simulation-in-houdini-unreal-engine-5), [80.lv – Approaches to Realtime Foam Rendering](https://80.lv/articles/breakdown-back-approaches-to-realtime-foam-rendering), [80.lv – Niagara Fluids Water Simulations](https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations)
- [Mahmoud Alkawadri – UE5 Water Tool & Niagara Fluid (Kaustik-Decal)](https://mahmoudalkawadri.artstation.com/projects/5vrDv1), [Simon Schreibt – River](https://simonschreibt.de/gat/river)
- [StraySpark – Mesh Terrain UE 5.8](https://www.strayspark.studio/blog/mesh-terrain-ue5-8-caves-overhangs-guide), [projprod – Mesh Terrain 5.8](https://www.projprod.com/post/mesh-terrain-unreal-engine-5-8)
- [CD PROJEKT RED – Witcher 4 UE5 Tech Demo](https://www.cdprojektred.com/en/blog/149/working-with-epic-to-debut-the-witcher-4-unreal-engine-5-tech-demo-at-unreal-fest); YouTube-Titel: „Unreal Engine 5.6 New River Simulation Tools (Witcher 4 Tech)“

**Fachliteratur**
- [Montgomery & Buffington 1997, Channel-reach morphology in mountain drainage basins (USFS-PDF)](https://fs.usda.gov/rm/boise/publications/watershed/rmrs_1997_montomeryr001.pdf)
- [Abrahams, Li & Atkinson 1995 – Step-pool streams, maximum flow resistance (EarthRef)](https://earthref.org/ERR/68349/)

---

## Empfehlung in 5 Sätzen

1. Den Water Brush nur als **einmaliges Formwerkzeug je Fluss** benutzen: Curl Noise 0, Width-Falloff 1 m, Rampe 1,5 m und Blend Mode „Min“ in Schluchten, Tiefe und Breite nur über die Splinepunkte.
2. Vor dem Festschreiben `landscape_rt_res` und die `landscape.BatchedMerge.*`-CVars lokal auslesen. Mit dem Skalier-Test prüfen, ob die Geisterformen der bekannte Fehler UE-221427 bei nicht quadratischen bzw. > 8 km großen Landschaften sind.
3. Ferats Weg (Auslesen → Korridor-Delta → Basisebene) beibehalten, ergänzt um:
   - eine Spline-Korridor-Maske (halbe Breite + Rampe + Falloff + 2 m);
   - zwei gleiche Lesungen nach `landscape.ForceLayersFullUpdate`;
   - `affects_landscape = False` an allen Wasserkörpern, bevor der Brush Manager gelöscht wird.
4. Danach die River-Spline von der Bettform lösen und die SWR mit kleiner Höhenbindung laufen lassen: Breite = Bett + 2 m, `match_spline_height_amount` ≈ 0,05, `source_size` = Bachbreite, `remove_outside_spline` 50 nur als Netz. Ziel ≥ 95 % nasse Zellen im Bett, ≤ 5 % außerhalb.
5. Den Witcher-Look holen über:
   - niedrige Absorption (≈ 0,45/0,10/0,08 je m) und Kaustik-Decal für sichtbaren Grund;
   - Schaum nur per Maske an Fällen, dazu Bläschen-Schleier unter dem Aufprall;
   - Feuchtelinien an Steinen und Holz.

   Landscape Patch, PCG Water Interop und Mesh Partition Water bleiben Option, Ausstattungshilfe bzw. ein Nein.


---

## Teil B – Engine-Plugins für Eldarien

Stand 12.10.2026. Projekt: UE 5.8.3, Landschaft 9 577 × 7 057 m, World Partition (1-km-Raster, 266 Landschaftsteile), Nanite-Landschaft mit Tessellation, Lumen, VSM, RVT. Ziel ist Witcher-Qualität, Umfang nur Landschaft.

**Wie die Quellen gelesen wurden:** Seiten direkt abzurufen ging in dieser Sitzung nicht. WebFetch scheiterte bei unrealengine.com, 80.lv und gamefromscratch.com an der Namensauflösung (DNS), und dev.epicgames.com sowie forums.unrealengine.com sind laut früheren Sitzungen über den Proxy gesperrt. Alle Angaben zu Epic-Doku, Release Notes, Forum und 80.lv stammen deshalb aus **Suchauszügen** und sind mit **[S]** markiert. Mit **[2.]** markiert sind Zusammenfassungen von Dritten (Blogs, Händlerseiten, Reposts). **[V]** heißt: eigene Schlussfolgerung, nicht belegt. Forenberichte sind Einzelberichte von Nutzern und ohne Bestätigung durch Epic, solange nichts anderes dabei steht.

**Reife:** Sie stammt aus Ferats Tabelle (Exp = Experimental, Beta, leer = ohne Kennzeichnung, also produktiv). 5.8 ist laut Epic bzw. Tom Looman die letzte große UE5-Version vor UE6 [S]. Experimentelle Plugins können sich deshalb in UE6 stark ändern.

---

## Übersicht

| Plugin | Reife 5.8 | Empfehlung | wofür | Risiko | Aufwand |
|---|---|---|---|---|---|
| Mesh Partition + Mesh Terrain Mode | Exp (neu in 5.8) | **Aus**, später (UE6) neu prüfen | 3D-Gelände mit Höhlen, Überhängen und Schluchtwänden | **hoch**: viele WP-/PIE-Streaming-Fehler; ganze Landschaft müsste umgebaut werden | sehr hoch |
| Mesh Partition Water | Exp | **Aus** | Wasserkörper auf Mesh Terrain | hoch: Absturz mit RiverModifier, gezackte Kanten | – |
| PCG Mesh Partition Interop / PCG Primitives MP Interop | Exp | **Aus** | PCG auf Mesh Terrain | nur mit Mesh Terrain sinnvoll | – |
| Landscape Patch | ohne Kennz. (Editor) | **Testen** | Bachbett/Becken als Höhentextur auf eigener Patch-Ebene, statt per Water Brush | mittel: zusätzliche Edit-Layer-Ebene (Merge-Speicher); Patch-Komponenten hängen dann am Plugin | mittel |
| Landmass | Beta | **Aus** (Brushes nicht nutzen) | Blueprint-Brushes für Gelände | mittel bis hoch: hält Landschaftsteile „Always Loaded“ | – |
| Water | Exp | **An** (läuft faktisch schon) | Flüsse, Seen, Wassermaterial, SWR-Grundlage | mittel: Befunde 1/4/5 aus Teil A | – |
| Water Advanced | Exp | **An lassen** | Shallow Water River (Niagara Fluids 2D) | mittel: Kosten, Exp | – |
| Water Extras | Exp | An lassen **nur als Referenz** | Beispielkarten und Materialien | gering, aber „not intended for shipping“ | gering |
| PCG Water Interop | Exp | **Jetzt einschalten** | Ufer-Streuung (Kies, Steine, Totholz) entlang der WaterBodyRiver-Splines mit Breite/Tiefe | gering (nur Editor-Graph) | gering |
| Buoyancy | Exp | **Aus** | Schwimmphysik | – (Gameplay, kein Gelände) | – |
| Niagara Fluids | Beta | **An lassen** (Abhängigkeit von SWR); **nicht** für Wasserfälle im Weltmaßstab | SWR; höchstens Nah-Effekte (Spritzer) | mittel: GPU-Kosten; 5.8-Forenbericht „funktioniert nicht“ | – |
| PCG Biome Core | Exp | **Testen** (als Vorlage, Plugin kopieren) | Biom-Regeln, Runtime-GPU-Bodenstreuung um die Kamera | mittel: Neuaufbau-Lawinen bei Partitionierung | mittel bis hoch |
| PCG Biome Sample | Exp | **Testen** (Testkarte, Referenz) | Beispiel-Biome und Runtime-Streuung | gering (nur Lerninhalt) | gering |
| PCG Primitives | Exp (neu in 5.8) | **Später** | Beispielbibliothek (Wald, Park, Straße), City-Sample-Basis | mittel: zieht Biome Core/Sample/External Data mit | mittel |
| PCG FastGeo Interop | Exp | **Testen** zusammen mit FastGeo | Runtime-GPU-PCG ohne Komponenten (Gras, Kleinzeug) | mittel: 5.8-Fehler beim Soft-Release (Aufploppen) | mittel |
| FastGeo Streaming | Exp | **Testen** (früh, Testzelle) | schnelleres WP-Streaming statischer Geometrie (Felsen-HISM, Deko) | mittel: RT-Cache, Material/RVT mit Data Layers | mittel |
| PCG Instanced Actors Interop | Exp | **Aus** | Mass-basierte interaktive Instanzen | – (Gameplay) | – |
| PCG Niagara Interop | Exp | **Später** | PCG setzt Ambient-FX (Gischt, Nebel, Insekten) | gering bis mittel | gering |
| PCG Nanite Assemblies Interop | Exp | **Später** (mit Nanite-Foliage-Wald) | PCG spawnt Nanite-Assemblies | mittel | mittel |
| Procedural Vegetation Editor | Exp (bei uns AN) | **An lassen**, aber **Packaging prüfen**, bevor daraus Wald entsteht | eigene Nanite-Foliage-Bäume und -Büsche | **hoch**: 5.8-Bericht „PVE-Mesh crasht Packaged Build“ | mittel |
| Dynamic Wind | Exp („extremely experimental“) | **Testen** mit PVE-/Assembly-Bäumen | Wind für Nanite-Foliage über Skinning statt WPO | hoch: Bone-Ausrichtung falsch (PVE), CPU-Tick-Kosten (5.7) | mittel |
| Nanite Assembly Editor Utilities | Exp | **Testen** (mit Dynamic Wind) | Assemblies per Blueprint/Python bauen | mittel | mittel |
| Nanite Displaced Mesh | Beta | **Prüfen**: wenn Tessellation schon läuft, so lassen | Vorab-Displacement für Nanite-Meshes, Tessellation | mittel: 5.8-Regression bei Landschafts-Displacement (Forum) | gering |
| Niagara Nanite | Exp | **Aus** | Nanite-Meshes als Partikel (Steinschlag, Blätter) | gering, aber kein Nutzen für Landschaft | – |
| Volumetrics | ohne Kennz. (Exp-Ordner) | **Aus** | BP-Bibliothek für Volumentexturen | – (Wolken und Nebel sind Kern-Features) | – |
| World Partition HLOD Utilities | Standard (an) | **An lassen** | HLOD-Layer-Assets, Utility-Klassen | gering | – |
| World Streaming Insights | Exp (neu in 5.8) | **Jetzt einschalten** (nur Diagnose) | Streaming-Profiling (Zellen, Hänger) | gering, Einrichtung hakt laut Forum | gering |
| Level Streaming Persistence | Exp | **Aus** | Gameplay-Zustand speichern | – | – |
| Geometry Script | ohne Kennz. | **Jetzt einschalten** | Mesh-Bearbeitung aus Python/BP (Bachbett-Meshes, Felsen-Varianten, Prüfungen) | gering | gering |
| PCG Geometry Script Interop | Beta | **Jetzt einschalten** | Abhängigkeit von Biome Core/Primitives; Punkte auf Meshes sampeln | gering | gering |
| PCG Python Interop | Beta | **Testen** | Python-Datenknoten in PCG-Graphen, passend zu unserer Python-Pipeline | gering (nur Editor) | gering |

---

## Je Plugin

### 1. Mesh Partition + Mesh Terrain Mode (+ Mesh Partition Water, PCG Mesh Partition Interop, PCG Primitives MP Interop)

**Was es tut**
- Mesh Terrain ist Epics neues, in 5.8 als Experimental eingeführtes, „3D-mesh-based system for authoring larger, more complex terrains“.
- Anders als die 2,5D-Landschaft ist es ein echtes 3D-Mesh. Damit gehen Überhänge, Tunnel und senkrechte Klippen.
- Es arbeitet mit nicht-destruktiven Modifikatoren, ist mit PCG interoperabel und „tightly integrated with World Partition and OFPA“ (Epic-5.8-Ankündigung [S], 80.lv [S], GamesBeat [S]).
- Mesh Partition ist das Datensystem, Mesh Terrain Mode das Werkzeugset.
- Mesh Partition Water übersetzt Wasserkörper in Modifikatoren (`URiverModifier`, `UWaterModifier`, API-Doku [S]).

**Reife:** Exp, erste Version.

**Probleme mit WP und großen Welten (Forum 5.8–5.8.2 [S])**
- Ein leerer FarFieldMeshComponent zieht die Streaming-Grenzen aller CompiledSections auf den Weltursprung. Das bricht Streaming und HLOD-Platzierung; tritt laut Bericht schon mit den Standard-Pipelines auf.
- Mesh Terrain verschwindet in PIE: Die Kollision ist da, die Meshes laden nicht (5.8.1).
- Nach einem Levelwechsel lädt die Partition nicht; Assertion in `MeshPartitionWorldUpdater` (noch in 5.8.2).
- Nach einem Rebuild ist ein Quadrant verschoben; nach dem Build gibt es Löcher.
- PIE-Ladezeit bis 10 min.
- Ein 24k×24k-Heightmap-Import scheitert an der Dreieckszahl.
- Ein RiverModifier lässt PIE abstürzen (`MeshPartitionRiverModifier.cpp`).
- Lake-Modifier erzeugt gezackte Kanten. Antwort im Forum: Das Water-Plugin sei „mostly designed to work with regular landscapes“.

**Einsatz bei Epic, CDPR und in Samples:** Kein Beleg für den Einsatz in der Witcher-4-Demo (die lief auf 5.6, Mesh Terrain kam erst in 5.8). Auch kein offizielles Sample gefunden. Dritte (StraySpark, gamineai [2.]) nennen es ein Prototyping-Werkzeug, „not a production open-world replacement“.

**Empfehlung: aus lassen.**
- Ein Umstieg hieße, die 9,6 × 7,1-km-Landschaft samt Wasser, Grass, RVT und HLOD neu aufzubauen – auf einem System mit offenen Streaming-Fehlern.
- Für einzelne Höhlen oder Überhänge reichen Nanite-Felsmeshes auf der Landschaft (Teil A, Klippennetze).
- In UE6 neu bewerten. Höchstens eine kleine Sandbox-Karte zum Kennenlernen.

### 2. Landscape Patch

**Was es tut**
- Editor-Plugin. Es verändert Höhen- und Gewichtskarten prozedural über Patch-Komponenten, vor allem `ULandscapeTexturePatch` (Höhe/Gewicht aus Textur oder Render-Target, mit Falloff, Blend-Modus und Transform).
- Das Ergebnis wird in die Landschaft gebacken.
- Patch-Ebenen sind rein prozedural; Sculpt- und Paint-Werkzeuge gehen darauf nicht. Gewichts-Patches müssen den Ziellayer-Namen tragen.
- Quellen: Epic-Doku „Landscape Patch System“ [S], Python-API [S].

**Reife:** in der Tabelle ohne Kennzeichnung (Editor-Ordner).

**WP und große Landschaften**
- Keine WP-spezifischen Fehler gefunden.
- [V] Jede zusätzliche prozedurale Edit-Layer-Ebene läuft über denselben Merge wie der Water Brush. Befund 1 aus Teil A (Mindest-Batch 7057×4537, +20 GB) gilt dann vermutlich genauso.
- Forum (5.8, [S]): Eine Änderung an der Edit-Layer-Naht („seam fix“, gegen Nicht-Determinismus an Kanten) treibt Komponenten über das D3D12-Limit von 64 SRVs. Das ist auch für Befund 5 interessant.

**Einsatz bei Epic, CDPR und in Samples:** nichts gefunden.

**Empfehlung: testen**, als deterministischere Alternative zum Water Brush für Bachbett und Becken.
- Unser Python-Weg berechnet die Soll-Höhen ohnehin. Statt sie Feld für Feld in die Basisebene zu schreiben, könnte ein Texture Patch pro Bachabschnitt sie nicht-destruktiv halten.
- Risiko: Die Patch-Komponenten hängen danach am Plugin. Wird es wieder ausgeschaltet, sind sie verwaist. Deshalb erst in einer Testkopie.
- Aufwand mittel: Textur-Export aus Python, ein Patch je Abschnitt.

### 3. Landmass

**Was es tut:** Blueprint-Brushes (Landscape Blueprint Brushes) für prozedurales Gelände auf Edit Layers. Edit Layers müssen dafür aktiv sein (Epic-Doku [S]).

**Reife:** Beta.

**WP und große Landschaften (Forum [S])**
- Ein Landmass-Brush (z. B. Brushify SmartBrush als LandmassBrushManager) markiert alle betroffenen LandscapeStreamingProxies als „Always Loaded“ (5.6). Mit entferntem Plugin ist das Problem weg.
- Ältere Berichte: Teile entladen nicht mehr.
- Der Add-Tool verformt Landmass-Gelände (5.6).

**Einsatz bei Epic, CDPR und in Samples:** Project Titan (8 × 8 km, UE 5.5+) nennt „Nanite and Landmass“ als Kerntechnik (CG Channel [S], Epic [S]). Für Witcher 4 kein Beleg; dort wurde das Gelände laut DF-Interview-Repost außerhalb der Engine gebaut [2.].

**Empfehlung: aus lassen bzw. nicht nutzen.**
- Unser Gelände kommt aus Houdini und Python.
- Ob das Water-Plugin Landmass als harte Abhängigkeit mitlädt, ließ sich nicht belegen. Tutorials sagen, man brauche beide [2.]. Bei Bedarf in `Engine/Plugins/Experimental/Water/Water.uplugin` nachsehen.

### 4. Water / Water Advanced / Water Extras

**Was es tut**
- **Water:** Ozean, See, Fluss, Wasserkörper, die die Landschaft graben (Brush), Wassermaterial, Wasserzonen.
- **Water Advanced** (seit 5.6): „Collection of easy to use water simulation systems built on the Niagara Fluids and Water plugins“, darunter der Shallow Water River (API-Doku [S], Forum-Tutorial 5.6 [S]).
- **Water Extras:** Beispiele und Testkarten, „not intended to be used directly in a shipping product“ (Tabelle).

**Reife:** alle drei Exp. Die API-Seite trägt weiter den Experimental-Hinweis [S].

**5.8-Änderungen (Release Notes [S])**
- schnellere Kollisionsberechnung beim Backen von Flüssen
- „Preventive fix for water brush against OnLevelAdded/Removed callbacks“ – möglicherweise relevant für Befund 4 (Geisterformen aus ungeladenen Zellen) [V]
- Single Layer Water: Velocity-Ausgabe in den Depth-Prepass verschoben, `r.Water.SingleLayer.ForceVelocity` veraltet

Die Probleme mit WP sind in Teil A beschrieben (Batch-Größe, Geisterformen, Nicht-Determinismus).

**Einsatz bei Epic, CDPR und in Samples**
- Witcher-4-Demo: Wie Flüsse und Wasserfälle gemacht wurden, ist **nicht belegt**. PC Gamer zitiert nur, „landscape, ground, lakes, rivers“ liefen dank Nanite flüssig [2.].
- Project Titan: Die Nutzung der Water-Plugins ist nicht belegt; nur Landmass ist genannt.

**Hinweis zur Tabelle:** Water steht auf „aus“, Water Advanced und Extras auf „AN“. [V] Water wird als Abhängigkeit mitgeladen; das Projekt nutzt WaterBodyRiver und SWR, Water läuft also faktisch.

**Empfehlung**
- Water und Water Advanced an lassen; das ist unser Weg für Flüsse und Seen.
- Water Extras nur als Referenz an lassen. Nichts daraus in der Welt referenzieren, vor dem Packen prüfen bzw. ausschalten.

### 5. PCG Water Interop

**Was es tut**
- PCG-Knoten „Get Water Spline“ liefert `UPCGWaterSplineData`, eine Spline-Datenklasse mit Metadaten je Punkt: Flussbreite links und rechts, Tiefe, Strömung, Audio-Intensität (API-Doku [S]).
- Ein Community-Kommentar (5.4): Damit kommt man leicht an „properly sized points along the river spline“ inklusive Fließgeschwindigkeit, noch „wip“ [2.].

**Reife:** Exp.

**WP-Probleme:** keine gefunden.

**Einsatz bei Epic, CDPR und in Samples:** kein Beleg.

**Empfehlung: jetzt einschalten.**
- Ufer-Streuung (Kies im Bett, Steine an Schnellen, Totholz an Becken) direkt aus den echten Fluss-Splines. Breite und Tiefe je Punkt steuern Band und Dichte.
- Geringes Risiko: nur Editor-Graph, kein Laufzeit-Eingriff, solange die Ergebnisse gebacken werden.

### 6. Buoyancy

**Was es tut:** Auftrieb für Objekte in Water-Plugin-Wasserkörpern.

**Reife:** Exp.

**Empfehlung: aus.** Gameplay bzw. Physik, für reine Landschaft ohne Nutzen. Später höchstens für treibendes Totholz.

### 7. Niagara Fluids (bei uns AN)

**Was es tut:** FLIP-Löser für Wasser (2D/3D), Shallow Water, Rauch und Feuer (80.lv, Asher Zhu [S]).

**Reife:** Beta.

**5.8**
- Jesse Pitela behauptet „up to 30 % faster“ in 5.8, mit 1,3 Mio. GPU-Partikeln/s Flüssigkeit plus 40 000/s Gischt in seiner Demo [S]. Das ist eine Eigenaussage mit Kursbezug.
- Gegenbericht im Forum: „Niagara Fluids doesn't seem to work in UE 5.8“ [S], Inhalt nicht gelesen.

**Wasserfälle:** Für Wasserfälle in einer offenen Welt gibt es keinen Beleg, dass FLIP live genutzt wird. Üblich sind:
- Mesh mit Fließmaterial plus Niagara-Sprites für Gischt und Nebel.
- Eine vorab simulierte FLIP-Sequenz als Alembic-Geometry-Cache (ArtStation-Beispiel [2.]).

**Empfehlung: an lassen**, weil Water Advanced/SWR darauf aufbaut. Für Wasserfälle keine Live-Fluids im Weltmaßstab: Mesh + Material + Niagara-Gischt. FLIP höchstens nah und lokal (Becken unter dem Fall), mit Abschaltdistanz.

### 8. PCG Biome Core / PCG Biome Sample

**Was es tut**
- Datengetriebenes Biom-Werkzeug aus PCG-Knoten: Generatoren, Filter, rekursive Transforms, Spawn.
- Biom-Volumen, -Splines und -Texturen; in v2 (5.6) Blending und Schichtung je Biom.
- Eigener Teil „Biome Core Runtime“ für GPU-Runtime-Streuung um die Kamera.
- Hängt von PCG und PCG Geometry Script Interop ab.
- Epic rät: „copy the plugin“, wenn man es produktiv nutzt (Epic-Doku [S]).

**Reife:** Exp.

**WP und große Landschaften (Forum [S])**
- Partitionierte Local Biome Cores lösten in 5.7.2 über 200 000 PCG-Tasks aus, rund 1 min Neuaufbau.
- Jede Änderung läuft „up to the global biome core(s)“.
- 5.8 verbessert das: Nur noch die Grenzen der geänderten lokalen Komponenten werden weitergegeben. Die Kaskade über den globalen Core bleibt.

**Einsatz bei Epic, CDPR und in Samples**
- Biome Sample = offizielles Beispiel. GDC-2026-Talk von Epic zu Biome Core [S].
- Witcher-4-Demo: Runtime-GPU-PCG für Gras und Kleinzeug statt Auto-Grass (Örtegren im DF-Interview, Repost [2.]) und eine PCG-Schicht für Felsen und Bäume. Dass dafür Biome Core selbst genutzt wurde, ist **nicht** belegt.

**Empfehlung: testen**
- Biome Sample in einer Testkarte als Vorlage für die Runtime-Bodenstreuung.
- Im Produktionspfad einen eigenen, schlanken Graphen oder ein kopiertes Plugin; unsere Biom-Regeln liegen schon in Python.
- Aufwand mittel bis hoch.

### 9. PCG Primitives

**Was es tut:** „PCG Primitives and Examples Library for World Building“, neu in 5.8. Beispiele für Straßen, Gebäude, Wälder und Parks. Hängt ab von PCG, Geometry Script Interop, Biome Core, Biome Sample und External Data Interop (API-Index [S], UnrealDirective [2.]).

**Reife:** Exp.

**Einsatz bei Epic:** Das in 5.8 aktualisierte City Sample nutzt es, ausdrücklich für „roads, buildings, forests, and parks“ (Epic-Learning [S]). Laut Drittbericht startet die Demo mit abgeschaltetem Streaming und nicht partitionierten Ergebnissen [2.].

**Empfehlung: später.** Reine Lernbibliothek. Für Waldränder und Lichtungen eventuell lehrreich, bringt aber viele experimentelle Abhängigkeiten mit.

### 10. FastGeo Streaming (+ PCG FastGeo Interop)

**Was es tut**
- Wandelt beim Erzeugen des Streamings (PIE/Cook) unveränderliche statische Geometrie ohne Gameplay-Bezug in schlanke FastGeo-Primitive um, über einen World-Partition-„Runtime Cell Transformer“. Das spart Actor- und Komponenten-Registrierung beim Zellen-Laden.
- Einrichtung: Transformer in den WP-Einstellungen. Zeitbudget-CVars wie `FastGeo.AsyncRenderStateTask.TimeBudgetMS` (Epic-Roadmap [S]); Debug mit `FastGeo.EnableTransformerDebugMode` [2.].
- PCG FastGeo Interop lässt GPU-Runtime-PCG Primitive ohne Komponenten spawnen (`pcg.RuntimeGeneration.ISM.ComponentlessPrimitives 1`, ab 5.7).

**Reife:** beide Exp.

**Probleme (Forum [S])**
- Fehlender Raytracing-Cache bei Clustern, die zu PIE-Beginn versteckt sind. Laut Antwort in 5.7 behoben.
- Material- bzw. RVT-Fehler mit Data Layers (5.7.3, Ursache unklar).
- 5.8: Die Interop ignoriert das Soft-Release. Bei einem flachen Refresh verschwindet die Geometrie einer Zelle für 0,5–2 s.

**Einsatz bei Epic und CDPR:** gemeinsam mit CDPR für die Witcher-4-Demo entwickelt; lässt Kovir laut CDPR „without visual hiccups“ streamen (CDPR-Blog [S], Epic [S]).

**Empfehlung: testen, früh.**
- Unser „Schwebende-Felsen“-Befund (Rock-HISM in Foliage-Zellen) und Streaming-Hänger sind genau die Zielklasse.
- In einer 3×3-km-Testzone mit World Streaming Insights messen.
- Achtung: RVT und Data Layers prüfen, außerdem was ein Ausschalten für bereits gecookte Daten bedeutet.
- PCG FastGeo Interop erst zusammen mit Runtime-GPU-PCG.

### 11. PCG Instanced Actors Interop / Instanced Actors

**Was es tut:** Mass-basierte, leichte Instanzen, die nahe am Spieler zu echten Actors werden; mit Replikation und Persistenz (Python-API [S]).

**Reife:** Exp.

**Empfehlung: aus.** Für interaktive Objekte (fällbare Bäume, Erntbares) gedacht, nicht für reine Landschaft.

### 12. PCG Niagara Interop

**Was es tut:** PCG-Graphen geben Punkte an Niagara weiter oder spawnen Systeme.

**Reife:** Exp. Keine Berichte gefunden.

**Empfehlung: später.** Nützlich, um Gischt, Nebel und Insekten an Schnellen, Fällen und Sumpf aus denselben Regeln zu setzen wie die Streuung. Erst sinnvoll, wenn die Wasser-FX stehen (16e).

### 13. Procedural Vegetation Editor (bei uns AN)

**Was es tut:** Knotengraph-Editor für Nanite-Foliage-taugliche Vegetation (Skelett-Mesh plus Assemblies). Wuchs „directly in the editor“ ab 5.8 (Release Notes [S]).

**Reife:** Exp (seit 5.7).

**Probleme (Forum 5.8 [S])**
- **Jedes** PVE-Mesh (auch Megaplants) lässt das Packaged Game abstürzen. Ohne Nanite kein Absturz, aber falsche Darstellung; in 5.7.4 ging es.
- Der Grower-Knoten crasht (5.8.1, Mac/Metal).
- Die Bone-Ausrichtung ist „world-aligned“, dadurch biegt Dynamic Wind auf der falschen Achse.
- Ob 5.8.3 das behebt, ist **unbekannt**. Das 5.8.3-Hotfix betraf laut früherer Recherche vor allem Landschaft, Rendering und Nanite.

**Einsatz bei Epic und CDPR:** Die Witcher-Demo nutzte Nanite Foliage (Assemblies, Voxels, Skinning), lief aber auf 5.6. PVE als Werkzeug ist dort nicht belegt.

**Empfehlung: an lassen (Editor).** Bevor PVE-Bäume in die Welt kommen: einen Mini-Package-Test mit einem PVE-Baum auf 5.8.3. Stürzt er ab, bleibt PVE beim Experimentieren.

### 14. Dynamic Wind

**Was es tut**
- Wind für Nanite Foliage über Skinning (Bone-Hierarchie, „Simulation Groups“) statt WPO.
- Epic weicht von WPO-Wind ab, weil Skinning engere Cluster-Grenzen und besseres Culling bringt (Epic-Doku Nanite Foliage [S], Tom Looman 5.7 [S]).
- Keine lokale Kollision [2.].

**Reife:** Exp, „Extremely experimental“ (Tabelle).

**Probleme**
- Falsche Achsen mit PVE-Bäumen (s. o.).
- 5.7.x: hohe Game-Thread-Kosten durch `USkinnedMeshComponent::TickComponent` bei großen Nanite-Foliage-Wäldern (Forum [S]).

**Einsatz bei Epic und CDPR:** Witcher-4-Demo, laut Zusammenfassung des Talks „Large Scale Animated Foliage“ (Unreal Fest Stockholm 2025): „new dynamic wind plugin“, über 500 000 Bäume [2.].

**Empfehlung: testen** in einer Testkarte, zusammen mit Nanite Assembly Editor Utils. Erst produktiv, wenn CPU-Kosten und Achsenfehler auf 5.8.3 geklärt sind. Gras bleibt bei WPO bzw. Material-Wind mit WPO Disable Distance (siehe Gras-Bericht).

### 15. Nanite Assembly Editor Utilities (+ PCG Nanite Assemblies Interop)

**Was es tut**
- Blueprint- und Python-Bausteine (`UNaniteAssemblyStaticMeshBuilder`, `UNaniteAssemblySkeletalMeshBuilder`), um statische oder skelettale Nanite-Assemblies zu bauen (API [S]).
- Assemblies verkleinerten den größten Baum der Witcher-Demo von 3,5 GB auf rund 29 MB (Epic-Doku Nanite Foliage [S]).
- PCG Nanite Assemblies Interop lässt PCG Assemblies spawnen.

**Reife:** Exp.

**Einsatz:** Witcher-4-Demo (Assemblies). Ein Community-Werkzeug „NAWS“ baut Assembly plus Dynamic Wind automatisch [S].

**Empfehlung: testen**, zusammen mit Dynamic Wind, für Waldbäume aus Fab-Paketen oder SpeedTree. PCG-Interop später.

### 16. Nanite Displaced Mesh

**Was es tut:** „basic pre-displacement pipeline for Nanite meshes“ (Tabelle). Mehrere Anleitungen nennen es als nötig für Nanite-Tessellation [2.]. Ob das in 5.8 noch zutrifft, ist **unsicher**.

**Reife:** Beta. Die Tessellation selbst ist laut früherer Recherche seit 5.4 Exp.

**Probleme**
- Forum 5.8: Displacement auf derselben Landschaft geht in 5.8 nicht, in 5.7.4 schon [S].
- UE-370671 (5.7.3): Geisterflächen, wenn Displacement im Material skaliert wird [S].

**Empfehlung: prüfen.** Da die Eldarien-Landschaft Tessellation schon nutzt: Läuft sie bei ausgeschaltetem Plugin, aus lassen. Sonst an. Kein neues Feature.

### 17. Niagara Nanite

**Was es tut:** Renderer, der Niagara-Partikel als Nanite-Geometrie zeichnet (seit etwa 5.7 in der Engine laut Händlerhinweis [2.]).

**Reife:** Exp.

**Empfehlung: aus.** Für Landschaft höchstens Steinschlag oder Laub-Effekte, kein Bedarf.

### 18. Volumetrics

**Was es tut:** „library of volume creation and rendering tools using Blueprints“ (Volumentexturen, Raymarch-Beispiele; API-Index [S]).

**Empfehlung: aus.** Sky Atmosphere, Volumetric Cloud, Exponential Height Fog und Heterogeneous Volumes sind Engine-Kern und brauchen das Plugin nicht (siehe Bericht zu Höhennebel).

### 19. World Partition HLOD Utilities / World Streaming Insights / Level Streaming Persistence

**World Partition HLOD Utilities**
- Standard und an. HLOD-Layer-Assets und Utility-Klassen. So lassen; der HLOD-Bericht baut darauf auf.

**World Streaming Insights**
- Neu in 5.8, API mit `UE_EXPERIMENTAL`-Markierung („subject to change without deprecation“) [S].
- Forum: Nutzer sah im Spatial-Insights-Fenster „nicht aktiviert“, kein Trace-Kanal „worldstreaming“ [S]. Die Einrichtung braucht also mehr als nur das Häkchen.
- **Jetzt einschalten:** reines Diagnosewerkzeug für Streaming-Hänger und FastGeo-Tests.

**Level Streaming Persistence**
- Exp, speichert Actor- und Property-Zustände pro Streaming-Level. Bekannter Fehler UE-368857 (Komponentenwerte gehen nach BP-Änderung verloren) [S].
- **Aus:** Gameplay, nicht Landschaft.

### 20. Geometry Script / PCG Geometry Script Interop / PCG Python Interop

**Geometry Script**
- Ohne Kennzeichnung. Mesh-Erzeugung und -Bearbeitung aus Blueprint und Python (Boolean, Remesh, Displace, Sampling).
- **Jetzt einschalten:** für Editor-Werkzeuge wie Bachbett-Querschnitte als Mesh, Felsvarianten, Prüfungen von Klippen-Netzen. Geringes Risiko.

**PCG Geometry Script Interop**
- Beta. Abhängigkeit von Biome Core und Primitives; erlaubt Punkte auf Static Meshes (z. B. Moos auf Felsen) [S].
- **Jetzt einschalten.**

**PCG Python Interop**
- Beta, nur Editor. Knoten „Python Data Processor“ [S].
- **Testen:** passt zu unserer Python-Regel-Pipeline (Biom-Regeln, Verteilung). So könnten bestehende Python-Regeln direkt in PCG-Graphen laufen.

### Weitere aus der Liste (kurz)
- **SpeedTree Importer** (an): an lassen. Die 80.lv-Anleitung zeigt SpeedTree nach UE 5.7 Nanite Foliage mit Wind [S].
- **PCGToolset** (AN): KI-Assistenz für PCG-Graphen, kein Weltinhalt. Egal.
- **LiDAR Point Cloud, GeoReferencing, Interchange OpenVDB:** für Eldarien ohne Nutzen. Aus.

---

## Empfehlungslisten

**Jetzt einschalten (geringes Risiko)**
1. **PCG Water Interop:** Ufer-Streuung aus den echten Fluss-Splines
2. **Geometry Script:** Editor-Mesh-Werkzeuge
3. **PCG Geometry Script Interop:** Abhängigkeit von Biome Core, Punkte auf Felsen
4. **World Streaming Insights:** Messwerkzeug fürs Streaming

So lassen (schon an): Water, Water Advanced, Niagara Fluids (SWR braucht es), WP HLOD Utilities, SpeedTree Importer, Procedural Vegetation Editor (aber vor Weltnutzung Package-Test), Water Extras (nur als Referenz, vor dem Packen raus).

**Testen (Testkarte oder Projektkopie, eins nach dem anderen)**
1. **FastGeo Streaming:** höchster erwarteter Nutzen; Witcher-Technik gegen Streaming-Hänger und Felsen-HISM
2. **Landscape Patch:** deterministische Bachbett- und Becken-Formung statt Water Brush
3. **PCG Biome Sample + Biome Core** (kopiert): Vorlage für Runtime-GPU-Bodenstreuung
4. **PCG FastGeo Interop:** zusammen mit der Runtime-GPU-Streuung
5. **PCG Python Interop:** Python-Regeln in PCG
6. **Dynamic Wind + Nanite Assembly Editor Utilities:** Witcher-Wald-Pfad, erst nach PVE-Package-Test
7. **Nanite Displaced Mesh:** nur prüfen, ob die vorhandene Tessellation es braucht

**Später**
PCG Primitives, PCG Niagara Interop, PCG Nanite Assemblies Interop.

**Aus lassen**
Mesh Partition, Mesh Terrain Mode, Mesh Partition Water, PCG Mesh Partition Interop, PCG Primitives MP Interop (in UE6 neu bewerten); Landmass (Brushes nicht nutzen); Buoyancy; Volumetrics; Niagara Nanite; PCG Instanced Actors Interop; Level Streaming Persistence.

**Allgemeine Regel [V]:** Experimentelle Plugins nur in einer Projektkopie einschalten. Bevor Assets aus einem Plugin in die echte Welt kommen (Patch-Komponenten, Assemblies, FastGeo-Transformer), Backup anlegen und Packaging-Test machen. Ein späteres Ausschalten hinterlässt sonst verwaiste Klassen in OFPA-Dateien.

---

## Offene Punkte und Unsicheres
- Die vollständigen 5.8-Release-Notes konnten nicht gelesen werden, nur Auszüge. Status-Änderungen einzelner Plugins in 5.8.1–5.8.3 sind nicht bestätigt.
- Ob 5.8.3 den PVE-Package-Crash, die Landschafts-Displacement-Regression und die Mesh-Partition-Streamingfehler behebt: unbekannt.
- Witcher-4-Demo: Wie Flüsse und Wasserfälle gemacht wurden und ob Water-Plugin, Landmass oder Biome Core genutzt wurden, ist **nicht belegt**.
- Ob Water.uplugin Landmass als Abhängigkeit lädt: in der Engine-Installation nachsehen.

---

## Quellen
Fast alle Links wurden nur über Suchauszüge gelesen [S]; Direktabruf war gesperrt bzw. DNS-tot.

**Epic (offiziell)**
- UE 5.8 Ankündigung: https://www.unrealengine.com/en-US/news/unreal-engine-5-8-is-now-available
- UE 5.8 Release Notes: https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US
- UE 5.7 Release Notes: https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-7-release-notes
- Mesh Terrain – Plugins aktivieren: https://dev.epicgames.com/documentation/unreal-engine/accessing-mesh-terrain-in-unreal-engine
- Mesh Terrain – Level Requirements: https://dev.epicgames.com/documentation/unreal-engine/crafting-mesh-terrain-in-unreal-engine?lang=en-US
- MeshPartitionWater API: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/MeshPartitionWater
- RiverModifier (Python): https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/RiverModifier
- Landscape Patch System: https://dev.epicgames.com/documentation/unreal-engine/landscape-patch-system
- LandscapeTexturePatch (Python): https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/LandscapeTexturePatch
- Landscape Blueprint Brushes (Landmass): https://dev.epicgames.com/documentation/unreal-engine/landscape-blueprint-brushes-in-unreal-engine
- Water Plugin-Index: https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/Water?lang=en-US
- Water Advanced Plugin-Index: https://dev.epicgames.com/documentation/en-us/unreal-engine/API/PluginIndex/WaterAdvanced
- PCG Water Interop API: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/PCGWaterInterop
- UPCGWaterSplineData: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/PCGWaterInterop/UPCGWaterSplineData
- Biome Core Overview: https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-pcg-biome-core-and-sample-plugins-overview-guide-in-unreal-engine
- Biome Core Quick Start: https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-pcg-biome-core-and-sample-plugins-quick-start-guide-in-unreal-engine
- PCG Primitives Plugin-Index: https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/PCGPrimitives?lang=en-US
- City Sample PCG: https://dev.epicgames.com/documentation/unreal-engine/city-sample-pcg-for-unreal-engine
- City Sample Update (PCG Primitives): https://www.unrealengine.com/learning/city-sample-gets-a-major-update-with-pcg-and-unreal-mcp-workflows
- PCG FastGeo Interop Plugin-Index: https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/PCGFastGeoInterop
- FastGeoStreaming API: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/FastGeoStreaming?lang=en-US
- Roadmap Fast Geometry Streaming: https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/2022-fast-geometry-streaming-plugin-experimental-
- Nanite Foliage: https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-foliage
- Nanite Assemblies: https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-assemblies
- NaniteAssemblyEditorUtils API: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/NaniteAssemblyEditorUtils
- Volumetrics Plugin-Index: https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/Volumetrics
- WorldStreamingInsights API: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WorldStreamingInsights
- LevelStreamingPersistence Plugin-Index: https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/LevelStreamingPersistence
- InstancedActorsManager (Python): https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/InstancedActorsManager
- UE-368857 (Level Streaming Persistence): https://issues.unrealengine.com/issue/UE-368857
- UE-370671 (Displacement-Geister 5.7.3): https://issues.unrealengine.com/issue/UE-370671

**CDPR / Witcher 4**
- CDPR-Blog Witcher-4-Demo: https://www.cdprojektred.com/en/blog/149/working-with-epic-to-debut-the-witcher-4-unreal-engine-5-tech-demo-at-unreal-fest
- CDPR Press: https://press.cdprojektred.com/en/news/1778/cd-projekt-red-and-epic-games-present-the-witcher-4-unreal-engine-5-tech-demo-at-the-state-of-unreal-2025
- Epic State of Unreal 2025: https://www.unrealengine.com/news/all-the-big-news-and-announcements-from-the-state-of-unreal-2025
- Talk „Runtime PCG in The Witcher 4 UE Tech Demo“: https://www.youtube.com/watch?v=icIFFlOyob4
- Talk „Large Scale Animated Foliage in The Witcher 4“ (Listing) [2.]: https://www.classcentral.com/course/youtube-large-scale-animated-foliage-in-the-witcher-4-unreal-engine-5-tech-demo-unreal-fest-stockholm-2025-505458
- DF-Interview-Repost (Runtime-GPU-PCG statt Auto-Grass) [2.]: https://gamrconnect.vgchartz.com/thread/249372/df-inside-the-witcher-4-unreal-engine-5-tech-demo-cd-projekt-red-epic-deep-dive-interview/
- PC Gamer (Foliage, „lakes, rivers“) [2.]: https://www.pcgamer.com/hardware/the-witcher-4s-leafy-glory-is-all-down-to-epics-nanite-foliage-and-largely-so-is-the-fact-it-can-run-ray-traced-at-60-fps-on-a-lowly-ps5/

**Forum (Einzelberichte)**
- Mesh Partition FarField-Bounds: https://forums.unrealengine.com/t/meshpartition-mesh-less-farfieldmeshcomponent-drags-compiledsection-bounds-to-the-world-origin/2745901
- WP Mesh actors fail to load in PIE: https://forums.unrealengine.com/t/world-partition-mesh-actors-fail-to-load-in-pie/2753927
- Mesh Terrain Partitions don't load in PIE: https://forums.unrealengine.com/t/mesh-terrain-partitions-dont-load-in-pie/2734466
- Mesh Partition bei Levelwechsel: https://forums.unrealengine.com/t/ue5-8-mesh-partition-not-loading-in-when-using-level-change-name-or-object/2738290
- Mesh terrain build issue: https://forums.unrealengine.com/t/mesh-terrain-build-issue/2741216
- Mesh Terrain/Mesh Partition 5.8: https://forums.unrealengine.com/t/mesh-terrain-mesh-partition-5-8/2730153
- Mesh Terrain just not working: https://forums.unrealengine.com/t/mesh-terrain-just-not-working/2729438
- RiverModifier-Crash: https://forums.unrealengine.com/t/watersplinemetadata-check-causes-crash-when-entering-pie-with-a-rivermodifier-in-level/2735418
- Mesh Terrain + Lake Modifier: https://forums.unrealengine.com/t/mesh-terrain-lake-modifier-odd-edges/2732510
- Mesh Terrain: Sacam or no?: https://forums.unrealengine.com/t/mesh-terrain-sacam-or-no/2760344
- Brushify/Landmass „Always Loaded“: https://forums.unrealengine.com/t/brushify-smartbrush-world-partition-landscapestreamingproxy-stays-always-loaded-in-the-editor-any-workaround-or-fix/2564755
- Landmass + Add tool: https://forums.unrealengine.com/t/landscape-deformation-issue-when-using-landmass-plugin-and-add-tool/2626674
- Big Landscape + Landmass + Water: https://forums.unrealengine.com/t/ue5-big-landscape-world-partition-landmass-plugin-water-plugin/240148
- Edit Layers 5.8 Naht-Regression: https://forums.unrealengine.com/t/landscape-edit-layers-5-8-regression-neighbor-input-area-widening-for-seam-fix-leaks-into-persisted-weightmaplayerallocations-inflating-srv-usage/2743253
- Water Advanced 5.6 Tutorial: https://forums.unrealengine.com/t/community-tutorial-new-in-unreal-engine-5-6-turn-your-water-body-river-into-a-game-ready-niagara-2d-fluid-simulation/2583651
- Niagara Fluids 5.8: https://forums.unrealengine.com/t/niagara-fluids-doesnt-seem-to-work-in-ue-5-8/2764942
- PCG biome v2 Partitioning: https://forums.unrealengine.com/t/pcg-biome-v2-partitioning/2730977
- PCGFastGeoInterop Soft-Release: https://forums.unrealengine.com/t/pcgfastgeointerop-ignores-soft-release-runtime-gen-shallow-refresh-destroys-fastgeo-primitives-immediately/2737974
- FastGeo + Raytracing: https://forums.unrealengine.com/t/fastgeostreaming-with-raytracing/2653656
- FastGeo Material/Data Layers: https://forums.unrealengine.com/t/fastgeo/2720987
- PVE Packaged Crash: https://forums.unrealengine.com/t/procedural-vegetation-nanite-foliage-meshes-crash-packaged-project/2730886
- PVE Grower-Crash: https://forums.unrealengine.com/t/bug-ue-5-8-1-procedural-vegetation-grower-node-crashes-editor-assertion-failed-point-pvgrower-cpp-1004-light-detection-resolves-only-2-points/2745117
- PVE Bone-Ausrichtung / Dynamic Wind: https://forums.unrealengine.com/t/procedural-vegetation-editor-generates-incorrect-bone-orientations-causing-broken-dynamic-wind-animation/2742382
- Megaplants Game-Thread 5.7.2: https://forums.unrealengine.com/t/severe-game-thread-slowdown-with-megaplants-nanite-foliage-at-scale-ue-5-7-2/2698484
- Nanite Assembly + Dynamic Wind Tool: https://forums.unrealengine.com/t/5-7-setting-up-nanite-assembly-dynamic-wind-system-tool/2742537
- Nanite Displacement 5.8 vs 5.7: https://forums.unrealengine.com/t/nanite-displacement-bugged-in-exact-same-landscape-in-ue-5-8-but-not-in-ue-5-7/2739815
- World Partition Insights 5.8: https://forums.unrealengine.com/t/how-do-you-use-world-partition-insights-for-ue-5-8/2746656

**Presse / Dritte**
- 80.lv UE 5.8 + Mesh Terrain: https://80.lv/articles/unreal-engine-5-8-is-out-today-with-big-optimization-improvements-and-mesh-terrain
- 80.lv Terrain-System-Details: https://80.lv/articles/details-on-ue5-s-next-generation-terrain-system-revealed
- 80.lv Niagara Fluids 5.8 (Pitela): https://80.lv/articles/exploring-real-time-water-simulations-in-unreal-engine-5-8/
- 80.lv Niagara Fluids Grundlagen: https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations
- 80.lv SpeedTree → Nanite Foliage mit Wind: https://80.lv/articles/tutorial-speedtree-to-ue5-7-s-nanite-foliage-with-wind
- GamesBeat UE 5.8: https://gamesbeat.com/epic-games-launches-unreal-engine-5-8/
- Digital Production 5.8 Preview: https://digitalproduction.com/2026/05/14/unreal-engine-5-8-preview-rolls-in/
- StraySpark Mesh Terrain [2.]: https://www.strayspark.studio/blog/mesh-terrain-ue5-8-caves-overhangs-guide
- gamineai Mesh Terrain [2.]: https://gamineai.com/blog/unreal-mesh-terrain-experimental-first-ue-5-8-preview-evening-keep-hold-2026
- gamineai PVE [2.]: https://gamineai.com/blog/procedural-vegetation-editor-experimental-first-ue-5-8-preview-evening-keep-hold-2026
- UnrealDirective PCG Primitives [2.]: https://unrealdirective.com/resources/engine-plugins/pcgprimitives/
- ZerotoBeast City Sample 5.8 [2.]: https://zerotobeast.com/unreal-engine-5-8-city-sample-a-free-pcg-worldbuilding-lab/
- CG Channel Project Titan: https://www.cgchannel.com/2024/12/download-epic-games-free-project-titan-unreal-engine-sample
- Tom Looman 5.7 Performance: https://tomlooman.com/unreal-engine-5-7-performance-highlights/
- Tom Looman 5.8 Performance: https://tomlooman.com/unreal-engine-5-8-performance-highlights/
- hzFishy Notes FastGeo [2.]: https://notes.hzfishy.fr/Unreal-Engine/Engine--and--Editor/Content-Streaming/Fast-Geo


---

## Teil C – Was die Witcher-4-UE5-Demo nutzt

Stand der Recherche: 12.10.2026. Gegenstand ist die „The Witcher 4 Unreal Engine 5 Tech Demo“ von CD Projekt Red (CDPR) und Epic. Sie lief am 3. Juni 2025 in der State of Unreal 2025 auf dem Unreal Fest Orlando, auf UE 5.6, auf einer normalen PS5 mit 60 fps und Raytracing. Dazu kommen die Folge-Talks (Unreal Fest Orlando und Stockholm 2025), das Digital-Foundry-Interview und NVIDIAs Wald-Demo zur GDC 2026 mit CDPR-Bäumen.

## Wie belastbar die Belege sind

- **Kein einziger Volltext war abrufbar.** WebFetch und curl wurden für alle relevanten Seiten abgewiesen: cdprojektred.com, unrealengine.com, dev.epicgames.com, forums.unrealengine.com, 80.lv, eurogamer, digitalfoundry, pcgamer, gamesindustry, web.archive.org (DNS „ENOTFOUND“ bzw. Proxy „CONNECT 403“). YouTube ist ohnehin gesperrt.
- **Alles unten stammt aus Suchauszügen (WebSearch).** Die Kennzeichnung **[SA]** gilt deshalb implizit für jede Aussage. Zusätzlich vermerke ich die Art der Quelle:
  - **[offiziell]**: CDPR- oder Epic-Pressetext, Epic-Doku, Epic-Mitarbeiter
  - **[Presse]**: Fachpresse oder Interview-Zitat
  - **[Community]**: Forum, Tutorial, Kursanbieter
  - **[Titel]**: nur Titel oder Beschreibung eines Videos bzw. Talks
- **Wörtliche Zitate sind Zitate aus den Auszügen, nicht aus dem Original.** Vor einer Übernahme in Entscheidungsdokumente sollte man sie am Original prüfen.
- **„Tech-Demo ≠ Spiel“:** CDPR betont ausdrücklich: „a first look at the cutting-edge technology powering The Witcher 4 – but not The Witcher 4 itself“ [offiziell, über VGC/80.lv].

---

## Übersichtstabelle

Spalte „in 5.8“: Reifegrad laut unserer Plugin-Liste bzw. Release Notes. Exp = Experimental, Beta, Prod = production-ready.

| Feature | in der Demo | in 5.8 (Plugin/Feature, Reife) | Eldarien: nutzen? | Aufwand/Risiko |
|---|---|---|---|---|
| **Nanite Foliage** (Voxel-Fernstufe, Nanite Assemblies, Nanite Skinning) | Kernfeature: dichter Wald aus echter Geometrie bis zur Nadel, ohne Alpha-Karten. Laut Talk-Zusammenfassung über 500 000 Bäume. In der Ferne werden Cluster zu Voxeln. | Engine-Feature, **Exp** (seit 5.7). Plugins: `ProceduralVegetationEditor` (Exp, **bei uns AN**), `NaniteAssemblyEditorUtils` (Exp, aus) | **Ja, als Pilot** für ein Waldbiom (Bergwald/Elfenwald). Das ist *der* sichtbare Witcher-Qualitätssprung. | Aufwand hoch (neue Asset-Pipeline). Risiko mittel–hoch (Exp; Physik, Kollision und Wind unvollständig). |
| **Dynamic Wind** | „Neues Dynamic-Wind-Plugin“ für Skelett-Bäume, Animation-Instancing und Richtungsvarianten | `DynamicWind` – **Exp** („extremely experimental“), bei uns aus | **Ja, zusammen mit Nanite Foliage** im Pilot. Ohne Wind wirkt Nanite-Wald tot. | Aufwand mittel. Risiko hoch: nur globale Windrichtung, keine Kollision, abhängig von PVE-Presets bzw. JSON-Knochendaten. |
| **Runtime-GPU-PCG** (Gras, Kleinzeug, Debris) | CDPR ersetzt das Landscape-Auto-Gras durch Runtime-GPU-PCG. Offline-PCG für Bäume und Felsen kommt dazu. Eigener Talk in Stockholm. | `PCG` – **Prod** seit 5.7, GPU-Ausführung ab 5.5, stark optimiert in 5.6. Bei uns AN. | **Ja, hohe Priorität.** Passt direkt zu unserer PCG-Verteilung und skaliert auf 68 km². | Aufwand mittel. Risiko gering–mittel. |
| **FastGeo Streaming** (+ PCG FastGeo Interop) | Mit Epic entwickelt. Lädt „alles in Kovir“ ruckelfrei. Eigener Talk (Rudzki/Malo). | `FastGeoStreaming`, `PCGFastGeoInterop` – **Exp** (auch in 5.8 Exp, mit Fixes). Bei uns aus. | **Später.** Erst messen (World Streaming Insights), dann in einer Kopie testen, wenn statische Meshes (Felsen) das Streaming bremsen. | Aufwand mittel. Risiko mittel–hoch: Abstürze in 5.7.4 gemeldet, Material-Probleme mit dem ISM-Flag, `p.Chaos.EnableAsyncInitBody` nötig. |
| **Lumen mit Hardware-RT** | 60 fps auf PS5 „mit Raytracing“. Epic (Örtegren): HW-RT ist qualitativ besser, Distance Fields sind „effektiv statisch“. | Engine, **Prod**. Seit 5.6 kostet HW-Lumen so viel wie SW-Lumen. In 5.8 kommt „Lumen Lite“ dazu. | **Ja:** HW-Lumen als Standard auf PC, Lumen Lite als Skalierungsstufe | Aufwand gering, Risiko gering |
| **Virtual Shadow Maps** | Laut DF-Kapitel „für 60 fps hochgezogen“ | Engine, Prod | Ja (Standard) | gering |
| **Landschaft/Gelände** | Laut DF-Interview-Auszug: Gelände als Basisschicht (Heightmap vorab außerhalb erstellt, in UE nachmodelliert), darüber Fels-Meshes, Bäume und eine PCG-Schicht. Kein Hinweis auf Mesh Terrain. | Landscape (Prod). Mesh Terrain und Mesh Partition sind neu in 5.8 (Exp). | **Weiter wie bisher:** Landscape mit Houdini-Basisebene plus Mesh-Felsen und PCG. Mesh Terrain **nicht** einführen. | – |
| **Wasser: Flüsse** | Laut Epic-Ingenieur Devon Penney (Niagara Fluids) nutzt die Demo die **Shallow Water River**-Simulation (Water Advanced, 5.6). Im Video sind „icy river currents“ zu sehen. | `Water` (Exp), `WaterAdvanced` (Exp, **bei uns AN**), `NiagaraFluids` (Beta, **AN**) | **Ja, beibehalten** (ist unser 16e/16f-Weg). Bettform unabhängig davon festschreiben (siehe Detail C.7). | Aufwand mittel. Risiko mittel (Exp, Bake-Workflow, WP-Probleme). |
| **Wasser: Wasserfälle** | **Kein Beleg** für einen Wasserfall in der Demo | – | Eigenes Rezept: Mesh + Material + Niagara-Gischt (eigene Einschätzung) | mittel |
| **Himmel/Wolken/Nebel** | **Keine konkreten Angaben gefunden.** Schneefall, Sonne durch Baumkronen, Voxel-Wald reagiert auf Sonnenstand. | Engine: SkyAtmosphere, Volumetric Clouds, Height Fog/Volumetric Fog (Prod). `Volumetrics`-Plugin (BP-Bibliothek) ist **nicht** belegt. | Engine-Standardkette nutzen. `Volumetrics`-Plugin nicht nötig. | gering |
| **Mass / Smart Objects / Crowds** | Markt in Valdrest: 300 einzeln animierte NPCs. Smart Objects als eine der genannten Technologien. | MassEntity/MassGameplay (Engine-Plugins, nicht in unserer Liste). `SmartObjects` **bei uns AN**. | **Nein (jetzt)**, reiner Landschaftsfokus. Später für Siedlungen. | – |
| **MetaHuman** | Gesichter der NPCs, Ciri | MetaHuman Creator seit 5.6 in der Engine | Nein (jetzt) | – |
| **UAF (Unreal Animation Framework)** | Neues Animationssystem, mehr NPCs gleichzeitig, eigener Talk | `UAF` **Exp** (Plugin seit 5.7, in 5.8 weiter Exp). `UAFStateTree` Exp. | Nein | – |
| **ML Deformer / Pferd Kelpie** | Muskeln unter der Haut des Pferdes, Synchronisierung beim Aufsitzen, Root Motion | ML Deformer (Engine-Plugin) | Nein | – |
| **Motion Matching, Chaos Cloth** | Laut Presse „advanced motion matching“ und Chaos-Umhang (Ciri) | Engine-Plugins | Nein | – |
| **60-fps-Arbeit (CPU/RHI)** | Multithreading, Sync-Punkte entfernt, Time-Slicing aller Primitive-Typen. Konsolen-Device-Profiles für 60 Hz. | in 5.6+ eingeflossen (Engine) | Indirekt ja: 5.8-Device-Profiles und Scalability nutzen | gering |

---

## Details je Feature

### C.1 Rahmendaten der Demo

- **Was gezeigt wurde.** Ciri reitet auf Kelpie durch das Gebirge von Kovir (Wald, Schneegipfel, Täler) in die Hafenstadt Valdrest. Ausblick auf die Hauptstadt Lan Exeter. Etwa 9–10 Minuten, live gespielt auf einer Basis-PS5 mit 60 fps und Raytracing [offiziell: CDPR-Pressetext, PlayStation Blog].
- **Fünf Kerntechnologien nach CDPR-Blog.** FastGeo Streaming, Nanite Foliage, Mass System, ML Deformer und Unreal Animation Framework. „Each of the five … will be available to all Unreal Engine 5 developers“ [offiziell, CDPR-Blog über Auszug]. Andere Listen nennen statt Mass die Smart Objects [Presse: 80.lv, Icy Veins].
- **Einordnung von Epic.** Die Tools werden „developed, tested, and eventually released to all UE developers, starting with today’s Unreal Engine 5.6 release“ [offiziell]. Nanite Foliage kam tatsächlich erst mit 5.7 als Experimental [Presse].
- **Leistungsziel.** CDPR gegenüber Eurogamer: „This tech demo runs at 60fps on PS5, and that’s the performance we’re aiming for in The Witcher 4“ [Presse].
- **Auflösung unbekannt.** Gerüchte nennen intern ca. 900p, DF vermutet Upscaling auf 1440p [Community, **unbestätigt**].
- **Talks zur Demo:**
  - Unreal Fest Orlando 2025:
    - „Streaming Improvements for Dense Worlds in The Witcher 4 UE5 Tech Demo“ (Jarosław Rudzki, CDPR, und Richard Malo, Epic)
    - „Road to 60FPS in The Witcher 4 UE5 Tech Demo“ (Rudzki)
    - „Unreal Animation Framework in The Witcher 4 UE5 Tech Demo“ (mit Adrianna Bielak, CDPR: „Bringing Kovir to Life with UAF“)
    - Devon Penneys (Epic) Talk über Fluss-Simulation, die laut seinem Post die Witcher-4-Demo behandelt
  - Unreal Fest Stockholm 2025:
    - „Large Scale Animated Foliage in The Witcher 4 UE5 Tech Demo“ (37 min, advanced)
    - „Runtime PCG in The Witcher 4 Unreal Engine Tech Demo“ (ca. 40 min)
  - Digital-Foundry-Interview „Inside The Witcher 4 UE5 Tech Demo: CD Projekt RED + Epic Deep Dive“, aufgenommen in Warschau
  - Belegt ist bei allen nur [Titel/Beschreibung].
- **Folgeereignisse:**
  - **GDC 2026:** NVIDIA zeigt eine „Witcher 4 RTX Mega Geometry Foliage“-Demo mit CDPR-Baummodellen, Path Tracing, 5 × 5 km, ca. 60 Mio. Pflanzen, 1 Mio. Bäume, über 200 Arten. Leistung: RTX 5090 ca. 80 fps in 4K (DLSS Quality), RTX 4070 ca. 58 fps in 1440p [Presse: TechSpot, VideoCardz, Guru3D]. Das ist eine NVIDIA-Rendering-Demo, nicht der UE-Standardpfad.
  - **Unreal Fest Juni 2026:** Ob Witcher 4 dort gezeigt wurde, ist **ungeklärt**. Angekündigt, dann von CDPR relativiert [Presse: playstationinfo.de, Softonic]. Spätere Berichte (ExitLag, GamingBible) sind nicht verifizierbar.

### C.2 Nanite Foliage (Voxel, Assemblies, Skinning) – das Herzstück

**Was es tut:**
- **Bäume als Baukasten.** Bäume werden als **Nanite Assemblies** aus wiederverwendeten Teilen (Ast-Meshes) zusammengesetzt statt als ein großes Mesh. Das hält die Assets klein.
- **Voxel in der Ferne.** Werden Nanite-Cluster klein genug, wechseln sie nahtlos in eine **Voxel-Darstellung**. Ein Baum bleibt so auch fern „volumetrisch“ und nimmt dynamisches Licht und Schatten an [offiziell: Epic-Doku „Nanite Foliage“ über Auszug; Presse: Game Informer, HotHardware].
- **Animation ohne WPO.** Animiert wird über **Nanite Skinning**, also Skelett-Bäume mit compute-basiertem Rigid Skinning und Animation-Instancing über Richtungsvarianten, nicht über World Position Offset [Presse: 5.7-Berichte; Community: daily.dev-Zusammenfassung des Stockholm-Talks].

**Was in der Demo gezeigt bzw. entwickelt wurde:**
- **Echte Geometrie.** „Each leaf and pine needle“ als echte Geometrie mit „adaptive, volumetric … voxel representation“ [Presse: Game Informer].
- **Abgelöste Technik.** Laut Stockholm-Talk wurden Alpha-Karten ersetzt. Die Zusammenfassung nennt über 500 000 Bäume mit Milliarden Quelldreiecken. Thema waren außerdem Schatten, Raytracing und Far-Field-Instancing [Community, Zusammenfassung; **Zahl unbestätigt**].
- **CPU-Ersparnis.** Eine Live-Berichterstattung zitiert auf der Bühne genannte CPU-Kosten von „one fiftieth“ des Vorherigen [Presse: GamesRadar-Liveticker; **Bühnenaussage, unbelegt**].
- **Hauptproblem Wald.** CDPR-VP Technology Charles Tremblay: Der Wald war der schwierigste Teil. Epic-Ingenieure haben „extrem hart“ daran gearbeitet [Presse: Icy Veins].
- **Bildanteil.** „95 % des Bildes ist oft Vegetation“ (Art Director) [Presse: Creative Bloq, aus einem Suchauszug; eine zweite Suche fand die Stelle nicht → **unsicher**].

**In 5.8:**
- Nanite Foliage ist Engine-Feature, **Experimental**. Laut 5.8-Preview-Berichten sind die Renderpfade weiterhin Exp [Community: HardForum].
- Werkzeuge:
  - `ProceduralVegetationEditor` (PVE, Exp, **bei uns AN**): erzeugt Nanite-Skeletal-Assemblies samt Winddaten. Dazu gibt es Quixel-„Megaplants“-Presets (u. a. Schwarzerle, Hasel, Rotbuche).
  - `NaniteAssemblyEditorUtils` (Exp, aus).
  - PCG-Knoten „Instanced Skinned Mesh Spawner“ (5.7) zum Verteilen [Community/Presse].
- **Nicht belegt:** PVE selbst wurde **nicht nachweislich** in der Witcher-Demo eingesetzt. PVE kam erst mit 5.7. Die Bäume der Demo stammen von CDPR.

**Eldarien:**
- **Pilot in einem Waldbiom (Empfehlung):**
  1. 3–5 Baumarten in PVE bzw. als Megaplants-Preset bauen (heimische Arten passen zu unseren Biomen).
  2. Über PCG mit dem Instanced Skinned Mesh Spawner verteilen.
  3. Dynamic Wind dazuschalten.
  4. Mit der klassischen Nanite-/WPO-Bepflanzung vergleichen: GPU-Zeit, Speicher, Optik auf 100 m, 500 m und 2 km.
- **Begründung:** Witcher- und RDR2-Qualität entsteht im Wald vor allem durch volumetrische Ferne ohne LOD-Popping und Karten-Look. Genau das liefert die Voxel-Stufe.
- **Aufwand:** hoch, denn die Asset-Pipeline ändert sich. Eine SpeedTree-Übernahme geht nur über JSON-Winddaten.
- **Risiken:**
  - Experimental, keine Garantie auf Stabilität
  - Physik und Kollision mit Skelett-Bäumen unvollständig
  - Speicherbedarf der Voxel-Daten unklar
  - die Pipeline steht und fällt mit PVE
- **Fallback:** Die bestehende Bepflanzung bleibt erhalten.

### C.3 Dynamic Wind

**Was es tut:**
- Prozeduraler Wind auf den **Knochen** von Skelett-Bäumen (Nanite Skinning).
- Ein Asset „Dynamic Wind Skeletal Data“ teilt Knochen in Gruppen wie Stamm, Ast und Zweig mit eigener Windstärke.
- Die Daten kommen aus PVE (automatisch) oder per JSON- bzw. USD-Import. Für SpeedTree gibt es ein Community-Skript, das XML in JSON umwandelt [Community: Epic-Forum, GitHub obilang/UE_NaniteDynamicWindData].

**Demo:**
- Der Stockholm-Talk nennt „a new dynamic wind plugin“ und Animation-Instancing über Richtungsvarianten [Community, Zusammenfassung].
- Presse: Äste und Blätter reagieren auf dynamischen Wind [Presse: Tribune].

**5.8:** `DynamicWind`, **Exp**, Engine-Selbstbeschreibung „Extremely experimental“.

**Bekannte Grenzen:**
- nur eine globale Windrichtung
- keine Kollision mit Spieler oder Objekten
- Teams kritisieren die Abhängigkeit von PVE-Presets [Community: Epic-Forum]

**Eldarien:** Nur im Nanite-Foliage-Pilot einschalten. Aufwand mittel, Risiko hoch. Für lokale Effekte wie Böen an Graten oder Wasserfall-Gischt bleibt die klassische Material-/WPO-Lösung nötig.

### C.4 Runtime-GPU-PCG und Biome

**Was es tut:** PCG erzeugt Inhalte zur Laufzeit auf der GPU, im Umfeld der Kamera, statt sie vorab zu speichern.

**Demo:**
- Der Stockholm-Talk „Runtime PCG in The Witcher 4 …“ zeigt, wie **Offline-PCG und Runtime-PCG kombiniert** wurden, um die dichte Welt zu füllen. Er enthält einen Deep-Dive zum Grassystem [Titel/Beschreibung].
- Im DF-Interview sagt CDPR sinngemäß: „we replace the auto grass with the runtime GPU-based PCG, and we use that for the small debris, trash, grass“ [Presse/Community, Interview-Auszug aus einem Forum].
- Epic-Tutorial-Berichte: Der Großteil der Bodenvegetation der Demo wurde zur Laufzeit per GPU-PCG erzeugt [Presse: 80.lv-Tutorial-Auszug].
- Schichtung laut Interview-Auszug: Gelände → Fels-Meshes und Bäume → prozedurale Schicht [Community-Transkript, **ungeprüft**].
- Echte Referenzen und Scans fließen in eine „art-directed“ prozedurale Welt ein [Presse: Yahoo/TechRadar-Auszug].

**5.8:**
- `PCG` ist seit 5.7 **production-ready** [Presse: 5.7-Berichte].
- Biome-Werkzeuge `PCGBiomeCore`/`PCGBiomeSample` (Exp) sind **nicht** als Demo-Werkzeug belegt.

**Eldarien:**
- **Ja, hohe Priorität.** Gras, Kleinkram, Totholz und Kies im Bachbett per Runtime-GPU-PCG. Bäume und große Felsen bleiben im Offline-PCG (unser jetziger Weg).
- Begründung: Auf 68 km² sind gespeicherte Gras-Instanzen teuer (Speicher, Streaming). Runtime-GPU spart beides und ist der Weg, den CDPR nachweislich gegangen ist.
- Aufwand mittel (Graphen umbauen, GPU-Knoten-Unterstützung prüfen). Risiko gering–mittel: Determinismus und Wiederholbarkeit bei Laufzeit-Seeds testen; Kollision für Kleinkram ist ohnehin aus.

### C.5 FastGeo Streaming (+ PCG FastGeo Interop)

**Was es tut:**
- Beim Laden einer World-Partition-Zelle wandelt ein Cell-Transformer (`UFastGeoWorldPartitionRuntimeCellTransformer`) passende statische Actors bzw. Components in **leichtgewichtige Strukturen ohne AActor/UComponent** um.
- Das Streaming läuft auf Worker-Threads.
- Es ist **kein Ersatz für World Partition**, sondern eine Ergänzung für statische, nicht spielrelevante Geometrie [offiziell: API-Doku über Auszug; Community: hzFishy-Notizen].
- Einstellungen: erlaubte Actor-/Component-Klassen und die Instanz-Speicherform (COMPRESSED empfohlen) [offiziell, Python-API-Auszug].

**Demo:**
- „allows everything in Kovir … to seamlessly load without visual hiccups or performance compromises“ [offiziell, CDPR].
- Talk „Streaming Improvements for Dense Worlds“: wichtige, „unter dem Radar geflogene“ Features plus eigens für die Ziele implementierte [Titel/Beschreibung].
- Die 5.6-Release-Notes nennen asynchrones Erzeugen und Zerstören des Physik-Zustands als allgemeine Streaming-Verbesserung [offiziell, Auszug].

**5.8:**
- `FastGeoStreaming` **Exp** (5.8-Notes: Fixes und Refactors, „speed, stability, use case support“) [offiziell, Auszug].
- `PCGFastGeoInterop` Exp.
- Bekannte Probleme:
  - Absturz im Hintergrund-Thread in 5.7.4
  - Material-Probleme in Verbindung mit „Used with Instanced Static Meshes“
  - Warnung zum Texture-Streaming-Pool
  - Pflicht `p.Chaos.EnableAsyncInitBody=true` (read-only, DefaultEngine.ini) [Community: Epic-Forum]

**Eldarien:**
- **Noch nicht.** Zuerst das Plugin `WorldStreamingInsights` (Exp, aus) einschalten und messen, ob das Streaming statischer Meshes beim Reiten bzw. Fliegen über 9,6 km Hänger erzeugt.
- Erst wenn ja: FastGeo in einer **Kopie** der Welt testen.
- Aufwand mittel, Risiko mittel–hoch: experimentell, Umwandlung beim Cook, Debugging schwerer.

### C.6 Lumen, Hardware-RT, Schatten, 60 fps

- **Demo:**
  - 60 fps auf der Basis-PS5 „with raytracing“ [offiziell].
  - Kevin Örtegren (Epic) im DF-Interview, sinngemäß: Distance Fields sind „effectively static“, für dynamischere Welten ist HW-RT qualitativ deutlich besser [Presse, Interview-Auszug].
  - CPU-Arbeit: Multithreading, unnötige Sync-Punkte entfernt, „allowing all types of primitives to time slice“ [Presse].
  - DF-Kapitel behandeln Lumen in Zwischensequenzen, die Beleuchtung und Schattierung der Voxel sowie „Virtual Shadow Maps auf 60 fps gebracht“ [Titel/Kapitel].
- **5.6:**
  - HW-Lumen erreicht jetzt das Frame-Budget des Software-Modus.
  - ShortRangeAO läuft in halber Auflösung mit Denoiser (2× schneller auf Konsole).
  - Far Field ca. 30 % schneller.
  - Neue 60-Hz-Device-Profiles für Konsolen und Desktop [offiziell, Auszug über Tom Looman/Epic].
- **5.8:**
  - **Lumen Lite** (Irradiance Fields mit Probe Occlusion, ca. 2× schneller, Ziel Switch 2 bzw. 60 fps)
  - MegaLights production-ready
  - weniger aggressives Culling kleiner Objekte aus der Lumen Scene auf Epic/Cinematic
  - geänderte Lumen-Fog-Voreinstellung [Presse: Guru3D, Tom Looman]
  - **In der Witcher-Demo nicht belegt:** Lumen Lite und MegaLights
- **Eldarien:**
  - HW-Lumen als Standard (Wald und Wasser profitieren von korrekten Reflexionen und GI unter dichtem Blätterdach).
  - VSM an.
  - Lumen Lite als niedrige Scalability-Stufe.
  - Aufwand gering, Risiko gering.
  - Wichtig für Nanite Foliage: Die Voxel-Fernstufe ist auf Lumen/VSM ausgelegt. Den Lumen-Scene-Inhalt für Foliage prüfen.

### C.7 Wasser, Flüsse, Wasserfälle – was bekannt ist

**Was in der Demo zu sehen ist:**
- Kotaku beschreibt „gently falling snowflakes and icy river currents“ [Presse: Kotaku].
- VGTimes spricht von schimmerndem Wasser mit Reflexionen [Presse].
- Ein Rezensent nennt „lifelike water physics“ [Presse, subjektiv].
- Eine Flussquerung mit Spritz-Effekten oder einen **Wasserfall** belegt **keine** gefundene Quelle.
- Hafen und Meer in Valdrest: in den Auszügen **nicht** beschrieben.

**Wie die Flüsse gemacht wurden (beste Beleglage):**

1. **Epic-Ingenieur Devon Penney** (Senior Physics Engineer bzw. Lead Niagara Fluids) kündigte seinen Unreal-Fest-2025-Talk über **Fluss-Simulation** an (4. Juni 2025, 15:30, Raum South 4, gestreamt). Der Talk behandle „using it in the #Witcher4 demo and also a small whitewater rafting game we built“ [offiziell-nah: Post eines Epic-Mitarbeiters auf X, **nur Suchauszug**].
   - Der Talktitel ist unsicher. Im Orlando-Programm taucht „Realistic and Lightweight Baked Water Simulations for Games“ auf [Community-Auszug, **nicht verifiziert**].
2. **Epic-Forum / Epic-Learning-Tutorial** „New in Unreal Engine 5.6 – Turn your Water Body River into a Game Ready Niagara 2D Fluid Simulation“: „the WATER ADVANCED plug-in, featuring the SHALLOW WATER RIVER actor … featured at Unreal Fest 2025 in Orlando in the Witcher 4 Tech Demo“ [Community-Tutorial auf Epic-Plattform, Auszug].
3. **Jesse Pitela (RedefineFX)**, Niagara-Kursanbieter: „New Unreal 5.6 River tools used in The Witcher 4 demo … collides, generates whitewater, and even supports buoyancy … All in real-time“ [Community].
4. **Epic-Tutorials von Devon Penney** „Baked River Simulations – Overview and Quick Start“ und „… – Parameter Reference“. Workflow:
   - Fluss mit Landscape- und Water-Body-Werkzeugen anlegen
   - mit dem ShallowWaterRiverActor (Niagara-2D-Gitter) simulieren
   - in **statische Texturen backen** (Höhe, Geschwindigkeit, Schaum)
   - im Spiel günstig rendern
   - Parameter verteilen sich auf ShallowWaterRiverActor, Niagara und Material [offiziell: Epic-Tutorial, Auszug]
   - Die Python-API des `ShallowWaterRiverComponent` (Modul `WaterAdvanced`, Experimental) führt `baked_sim`, Render-Target und Textur der gebackenen Oberfläche [offiziell, API-Auszug].

**Schlussfolgerung (Indizienlage, keine CDPR-Primärquelle):**
- Die Flüsse der Demo liefen sehr wahrscheinlich über **Water Plugin (WaterBodyRiver) + Water Advanced / Shallow Water River (Niagara-Fluids-2D-Simulation, gebacken)**. Das ist genau die Kette, die Eldarien seit 16e nutzt.
- **Nicht bekannt:**
  - ob CDPR die Flussbetten per **Water-Brush** gegraben oder per Hand bzw. Houdini ins Landscape modelliert hat
  - welche SWR-Werte gesetzt waren
  - ob Schaum und Weißwasser aus der Sim oder aus Niagara-Partikeln kamen
  - Dazu gibt es weder Talk-Inhalt noch Interview-Aussage im Auszug.

**Wasserfälle:**
- Kein Beleg aus der Demo.
- Eigene Einschätzung: Der Shallow Water River ist eine 2D-Höhenfeld-Simulation und bildet senkrechte Fälle nicht sinnvoll ab. Üblich ist Fall-Mesh + Fließ-Material + Niagara-Gischt/-Nebel an Ober- und Unterkante.
- Das Becken unten bleibt Teil des SWR. Als Vorlage helfen Matt Oztalays Unreal-Fest-Talk „Chasing Waterfalls“ (Niagara, mobil) und Niagara-Fluids-Vorlagen [Titel].

**Probleme laut Community (5.6–5.8):**
- SWR-Simulation liegt in World-Partition-Levels teils ~15 000 Einheiten unter der Landschaft. Vermutet wird eine fehlerhafte Bounds-Berechnung in WP. „Use Capture“ aus richtet sie aus, erfasst dann aber keine Bottom-Contour-Objekte [Community].
- 5.8: Die Capture-Tiefe kommt nicht an, deshalb läuft mit „Use Capture“ keine Simulation [Community].
- SWR überschreibt den WaterBody-River-Layer, spätere Breiten- oder Tempo-Änderungen sind schwer [Community].
- Reset lässt den Water Body verschwinden (5.6.1 bis 5.8.1) [Community].
- Shader-Fehler in `Grid2D_SW_River` führt zu PIE-Absturz (5.7) [Community].
- Im Paket fehlt Wasser → `Water`/`WaterAdvanced` in `DirectoriesToAlwaysCook` aufnehmen [Community].
- Überlauf in Kurven: „Remove Outside of Spline Amount“ auf 100–200 setzen bzw. Z-Offset in den Water-Heightmap-Settings, z. B. 200 [Community: KI-Zusammenfassung eines Tutorials, **schwach**].

**Eldarien (Wasser):**
- **Beibehalten:** WaterBodyRiver + Shallow Water River gebacken. Das entspricht dem wahrscheinlichen Witcher-Weg. `WaterAdvanced` und `NiagaraFluids` sind bei uns AN.
- **Auffällig:** Unsere Liste führt `Water` als „aus“, obwohl WaterBodyRiver und WaterAdvanced es brauchen. Vermutlich wird es als Abhängigkeit mitgeladen. Bitte in `.uproject` prüfen und **explizit** aktivieren, damit Cook und Paketierung es sicher mitnehmen.
- **Bettform vom Brush entkoppeln.** Unser Plan, das Brush-Ergebnis auszulesen und in die Basisebene festzuschreiben, ist mit der Indizienlage vereinbar. Es gibt keinen Beleg, dass CDPR die Water-Brushes zur Laufzeit oder im Endstand aktiv lässt. Die SWR-Simulation braucht nur das fertige Bett.
- Schaum nur an Fällen bzw. Schnellen: über die SWR-/Material-Parameter der Parameter Reference steuern (Detail siehe Teil A/B).
- Wasserfälle über ein eigenes Mesh- und Niagara-Rezept.
- `Buoyancy` (Exp, aus) nur bei schwimmenden Objekten (Treibholz) einschalten.
- Aufwand mittel. Risiko mittel: Exp-Status, WP-Bounds-Bug, Bake bei jeder Bettänderung neu.

### C.8 Landschaft und Gelände

- **Demo:**
  - Kovir: Schneegipfel, tiefe Täler, dichte Wälder, verschneite Klippen [offiziell].
  - Laut Interview-Auszug (DF, Kapitel „How was the world and terrain created“, ca. 13:36) erste Geländestufe außerhalb der Engine, Heightmap importiert und in UE nachmodelliert, darüber Fels-Meshes, Bäume und PCG [Community-Transkript, **unsicher**].
  - Keine Quelle nennt das Tool (Houdini, Gaea …), Mesh Terrain, Landmass oder Landscape Patch.
- **5.8:** Mesh Terrain und Mesh Partition sind neu und **Exp** (3D-Mesh-Gelände für Überhänge und Höhlen). Keine Verbindung zur Witcher-Demo belegt.
- **Eldarien:** Bei Landscape + Houdini-Basisebene + Mesh-Felsen + PCG bleiben. Das ist strukturell dasselbe Schichtmodell. Mesh Terrain höchstens später für einzelne Höhlen bzw. Überhänge in einer Testkarte, nicht für die 68-km²-Welt. Aufwand 0, Risiko 0.

### C.9 Himmel, Wolken, Nebel, Volumetrics

- **Demo:**
  - Keine technischen Angaben gefunden.
  - Belegt: Schnee, Licht durch Baumkronen, Schatten im dichten Wald [Presse].
  - Die Voxel-Vegetation „reagiert auf die Bewegung der Sonne“ [Presse: GamesRadar-Liveticker].
- **Engine:**
  - SkyAtmosphere, Volumetric Clouds, Exponential Height Fog mit Volumetric Fog (Prod).
  - Ein Suchauszug erwähnt „cloud shadows and new froxel-based volumetric and translucency support“ in den Release Notes der Demo-Engine-Version. Die Version ist **nicht sicher** zugeordnet.
  - Das Plugin `Volumetrics` (BP-Bibliothek) ist **nicht** als Demo-Bestandteil belegt.
- **Eldarien:** Standardkette verwenden. Wichtig sind Lumen-HWRT, Volumetric Fog unter Lumen (5.8 hat die Fog-Voreinstellung geändert, siehe C.6) und Wolkenschatten. Kein Zusatz-Plugin.

### C.10 Mass, Smart Objects, MetaHuman, UAF, ML Deformer, Motion Matching

- **Demo:**
  - Markt in Valdrest mit 300 einzeln animierten NPCs; sie reden, reagieren, ein Obstkorb fällt herunter [Presse].
  - Laut CDPR erhöht UAF die NPC-Anzahl beim Bandauftritt drastisch [offiziell, CDPR-Blog-Auszug].
  - MetaHuman-Gesichter, Mass-AI-Crowd-Scaling [offiziell].
  - Pferd Kelpie: ML Deformer für Muskeln (eine Quelle nennt stattdessen Chaos Flesh), Root Motion, neue Synchronisierung beim Aufsitzen aus jedem Winkel [Presse].
  - Chaos Cloth für den Umhang, „advanced motion matching“ [Presse].
- **5.8:**
  - UAF: Plugin seit 5.7, in 5.8 weiter **Exp**. Epic: „use caution when shipping“ [offiziell, Auszug].
  - MetaHuman Creator seit 5.6 in der Engine.
  - Mass: Status nicht belegt.
  - `SmartObjects` bei uns AN.
- **Eldarien:** Für den reinen Landschaftsfokus **nicht** relevant. Erst bei Siedlungen bzw. Belebung wieder ansehen.

---

## Was Eldarien konkret übernehmen sollte (Reihenfolge)

1. **Runtime-GPU-PCG für Gras, Kleinkram und Bachbett-Kies.** Der direkteste CDPR-Beleg, PCG ist production-ready, passt zur bestehenden Pipeline.
2. **Hardware-Lumen + VSM als Basis-Rendering, Lumen Lite als niedrige Stufe.** Geringer Aufwand, Witcher-Demo-Standard.
3. **Wasser:** Kette WaterBodyRiver + Shallow Water River (gebacken) beibehalten. `Water` explizit aktivieren und Cook-Verzeichnisse setzen. Bett festschreiben, Brushes entfernen. Wasserfälle separat als Mesh + Niagara.
4. **Nanite-Foliage-Pilot** (PVE ist schon AN, dazu `DynamicWind` und `NaniteAssemblyEditorUtils`) in einem Waldbiom mit Messprotokoll. Größter optischer Hebel, größtes Risiko.
5. **World Streaming Insights** einschalten und messen. **FastGeo** erst danach in einer Weltkopie.
6. **Nicht** übernehmen (jetzt): Mesh Terrain/Mesh Partition, Landmass, Volumetrics-Plugin, Mass/UAF/ML Deformer/MetaHuman.

## Offene Punkte

Diese Punkte lassen sich nur mit Zugriff auf Video bzw. Volltext klären:

- Inhalt von Devon Penneys Fluss-Talk (Werte, Bettentstehung, Schaum) und genauer Titel
- DF-Interview ab ca. 13:36 (Geländeerstellung)
- „Road to 60FPS“ und „Streaming Improvements“: welche CVars bzw. Einstellungen
- Stockholm-Talks: Grassystem-Details, Foliage-Budgets
- Ob in der Demo überhaupt ein Wasserfall vorkommt (Bildanalyse des Videos)

---

## Quellen

Alle Quellen wurden nur über Suchauszüge gelesen; Volltexte waren über den Proxy gesperrt.

**Offiziell (CDPR / Epic / Epic-Mitarbeiter)**
- CDPR-Pressetext State of Unreal 2025: https://press.cdprojektred.com/en/news/1778/cd-projekt-red-and-epic-games-present-the-witcher-4-unreal-engine-5-tech-demo-at-the-state-of-unreal-2025 und https://www.cdprojekt.com/en/media/news/cd-projekt-red-and-epic-games-present-the-witcher-4-unreal-engine-5-tech-demo-at-the-state-of-unreal-2025/
- CDPR-Blog „Working with Epic to debut …“: https://www.cdprojektred.com/en/blog/149/working-with-epic-to-debut-the-witcher-4-unreal-engine-5-tech-demo-at-unreal-fest
- thewitcher.com News: https://www.thewitcher.com/us/en/news/51521/the-witcher-4-unreal-engine-5-tech-demo
- PlayStation Blog: https://blog.playstation.com/2025/06/03/the-witcher-4-unreal-engine-5-tech-demo-on-ps5-revealed/
- Epic – All the big news State of Unreal 2025: https://www.unrealengine.com/news/all-the-big-news-and-announcements-from-the-state-of-unreal-2025
- Epic – UE 5.6 verfügbar: https://www.unrealengine.com/news/unreal-engine-5-6-is-now-available
- Epic – UE 5.7 verfügbar: https://www.unrealengine.com/news/unreal-engine-5-7-is-now-available
- Epic – UE 5.8 verfügbar: https://www.unrealengine.com/news/unreal-engine-5-8-is-now-available
- UE 5.8 Release Notes: https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US
- Talk „Streaming Improvements for Dense Worlds …“ (Orlando 2025): https://dev.epicgames.com/community/learning/talks-and-demos/KWGD/streaming-improvements-for-dense-worlds-in-the-witcher-4-unreal-engine-5-tech-demo-unreal-fest-orlando-2025 · YouTube: https://www.youtube.com/watch?v=BdopUm1_1_E
- Talk „Unreal Animation Framework in The Witcher 4 …“ (Orlando 2025): https://dev.epicgames.com/community/learning/talks-and-demos/RmO5/unreal-animation-framework-in-the-witcher-4-unreal-engine-5-tech-demo-unreal-fest-orlando-2025
- Talk „Large Scale Animated Foliage in The Witcher 4 …“ (Stockholm 2025): https://www.youtube.com/watch?v=EdNkm0ezP0o · Beschreibung: https://www.classcentral.com/course/youtube-large-scale-animated-foliage-in-the-witcher-4-unreal-engine-5-tech-demo-unreal-fest-stockholm-2025-505458
- Talk „Runtime PCG in The Witcher 4 …“ (Stockholm 2025): https://www.youtube.com/watch?v=icIFFlOyob4 · Beschreibung: https://www.classcentral.com/course/youtube-runtime-pcg-in-the-witcher-4-unreal-engine-tech-demo-unreal-fest-stockholm-2025-506697
- Epic-Doku Nanite Foliage: https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-foliage
- Epic-API Dynamic Wind: https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/DynamicWind
- Epic-API FastGeoStreaming: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/FastGeoStreaming?lang=en-US
- Epic-API UAF: https://dev.epicgames.com/documentation/en-us/unreal-engine/API/PluginIndex/UAF
- Epic-Tutorial „Baked River Simulations – Parameter Reference“ (Devon Penney): https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference · Forum: https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112
- Epic-Tutorial „Baked River Simulations – Overview and Quick Start“: https://forums.unrealengine.com/t/tutorial-baked-river-simulations-overview-and-quick-start/2512102
- Python-API ShallowWaterRiverComponent: https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent?application_version=5.5
- Devon Penney (Epic) auf X, Ankündigung des Fluss-Talks mit Witcher-4-Bezug: https://x.com/dmpvfx?lang=en
- Epic-Blog Game Animation Sample 5.7 (UAF-Status): https://www.unrealengine.com/tech-blog/explore-the-updates-to-the-game-animation-sample-project-in-ue-5-7

**Presse / Interviews**
- Digital Foundry Reaction (YouTube): https://www.youtube.com/watch?v=5PIyPpB83Vw · DF auf X: https://x.com/digitalfoundry/status/1930303268724584549
- DF Deep-Dive-Interview (YouTube): https://www.youtube.com/watch?v=OplYN2MMI4Q · Forumsabschriften: https://www.resetera.com/threads/df-inside-the-witcher-4-unreal-engine-5-tech-demo-cd-projekt-red-epic-deep-dive-interview.1218510/ und https://gamrconnect.vgchartz.com/thread/249372/df-inside-the-witcher-4-unreal-engine-5-tech-demo-cd-projekt-red-epic-deep-dive-interview/
- N4G zum DF-Interview: https://n4g.com/news/2672078/inside-the-witcher-4-tech-demo-the-cd-projekt-red-and-epic-interview
- Game Informer: https://gameinformer.com/2025/06/03/get-a-new-look-at-the-witcher-iv-in-unreal-engine-technical-showcase
- Kotaku („icy river currents“): https://kotaku.com/witcher-4-ciri-trailer-gameplay-ue5-tech-demo-1851783467
- GamesRadar-Liveticker: https://www.gamesradar.com/news/live/the-witcher-4-state-of-unreal-2025-live-coverage-everything-announced/
- GamesRadar-Interview „worth it“: https://www.gamesradar.com/games/the-witcher/witcher-4-tech-demo-shows-swapping-to-unreal-engine-was-worth-it-cdpr-says-and-that-its-not-like-we-lost-things-because-of-the-transition-away-from-cyberpunk-2077s-red-engine/
- TechRadar „Five things we learned“: https://www.techradar.com/gaming/five-things-we-learned-from-the-witcher-4s-technical-demo
- HotHardware: https://hothardware.com/news/witcher-4-unreal-engine-5-6-demo
- Creative Bloq „infinite forest“: https://www.creativebloq.com/3d/video-game-design/how-the-witcher-4s-infinite-forest-is-being-built-one-branch-at-a-time-using-unreal-engine-5-6
- Creative Bloq Pferdephysik: https://www.creativebloq.com/3d/video-game-design/im-bewitched-by-the-horse-physics-in-the-stunning-witcher-4-unreal-engine-5-6-tech-demo
- Icy Veins: https://www.icy-veins.com/other-games/news/the-witcher-iv-taking-advantage-of-current-tech/
- 80.lv: https://80.lv/articles/a-first-look-at-the-witcher-4-s-graphics-gameplay
- VGTimes: https://vgtimes.com/articles/127439-new-details-about-the-witcher-4-from-the-state-of-unreal-2025-presentation-full-breakdown-of-the-gameplay-demo.html
- Player.One (300 NPCs): https://www.player.one/new-witcher-4-tech-demo-teases-insane-graphics-300-npcs-whole-new-world-unreal-engine-5-160728
- Tribune (Wind, Chaos): https://tribune.com.pk/story/2549319/witcher-4-tech-demo-shows-unreal-engine-5s-latest-features
- TechPowerUp (5.6 60 fps RT): https://www.techpowerup.com/337638/unreal-engine-5-6-brings-60-fps-ray-tracing-to-current-generation-hardware
- Tom Looman 5.6 / 5.7 / 5.8: https://tomlooman.com/unreal-engine-5-6-performance-highlights/ · https://tomlooman.com/unreal-engine-5-7-performance-highlights/ · https://tomlooman.com/unreal-engine-5-8-performance-highlights/
- Guru3D Lumen Lite 5.8: https://www.guru3d.com/story/unreal-engine-58-debuts-lumen-lite-and-productionready-megalights/
- DSOGaming UE 5.8: https://www.dsogaming.com/news/unreal-engine-5-8-released-fully-detailed/
- NVIDIA GDC 2026 Witcher-4-Wald-Demo: https://www.techspot.com/news/111936-nvidia-shows-witcher-4-forest-demo-running-path.html · https://videocardz.com/newz/the-witcher-4-path-traced-rtx-mega-geometry-demo-runs-at-around-80-fps-4k-on-rtx-5090-with-dlss · https://www.guru3d.com/story/nvidia-shows-the-witcher-4-forest-tech-at-4k-and-80-fps/
- Unreal Fest 2026 ungeklärt: https://www.playstationinfo.de/2026/03/03/the-witcher-4-doch-nicht-auf-dem-unreal-fest-2026-cd-projekt-red-stellt-geruechte-klar/ · https://en.softonic.com/articles/will-we-see-the-witcher-iv-at-the-next-unreal-fest-its-director-clarifies-it

**Community**
- Epic-Forum „New in UE 5.6 – Turn your Water Body River into a Game Ready Niagara 2D Fluid Simulation“ (Witcher-4-Bezug): https://forums.unrealengine.com/t/community-tutorial-new-in-unreal-engine-5-6-turn-your-water-body-river-into-a-game-ready-niagara-2d-fluid-simulation/2583651 · https://dev.epicgames.com/community/learning/tutorials/OZMa/new-in-unreal-engine-5-6-turn-your-water-body-river-into-a-game-ready-niagara-2d-fluid-simulation
- Jesse Pitela (RedefineFX) auf X: https://x.com/RedefineFX/status/1938222500858450359 · Video „UE 5.6 New River Simulation Tools (Witcher 4 Tech)“: https://www.youtube.com/watch?v=FSZnRLss4DQ
- SWR in WP unter der Landschaft: https://forums.unrealengine.com/t/unreal-5-6-shallowwaterriver-simulation-nowhere-near-the-waterbodyriver-spline/2637929
- SWR rendert nach dem Build nicht: https://forums.unrealengine.com/t/shallow-water-body-advanced-water-plugin-fails-to-render/2634176
- 5.7 Water-Plugin-Fehler: https://forums.unrealengine.com/t/5-7-water-plugin-error/2705317
- SWR destruktiv?: https://forums.unrealengine.com/t/5-6-are-shallow-water-river-destructive/2659509
- FastGeo AsyncInitBody: https://forums.unrealengine.com/t/how-to-properly-enable-asyncinitbody-to-be-able-to-use-fast-geo-streaming-ue-5-6/2613667 · FastGeo-Absturz 5.7.4: https://forums.unrealengine.com/t/fastgeo-streaming-5-7-4/2724674 · FastGeo-Materialproblem: https://forums.unrealengine.com/t/fastgeo/2720987/4
- hzFishy FastGeo-Notizen: https://notes.hzfishy.fr/Unreal-Engine/Engine--and--Editor/Content-Streaming/Fast-Geo
- Dynamic Wind/Nanite Assembly Setup: https://forums.unrealengine.com/t/5-7-setting-up-nanite-assembly-dynamic-wind-system-tool/2742537 · Fragen: https://forums.unrealengine.com/t/dynamic-wind-system-questions/2698278 · SpeedTree→JSON: https://github.com/obilang/UE_NaniteDynamicWindData
- daily.dev, Zusammenfassung des Foliage-Talks: https://app.daily.dev/posts/large-scale-animated-foliage-in-the-witcher-4-unreal-engine-5-tech-demo-unreal-fest-stockholm-2025-tnchqa4vo
- HardForum (Nanite Foliage in 5.6/5.8): https://hardforum.com/threads/ue5s-nanite-foliage-looks-amazing-in-new-witcher-4-demo.2041730/ · https://hardforum.com/threads/unreal-engine-5-8-preview-has-arrived.2047806/
- lilys.ai, KI-Notiz zu einem „Witcher 4 Baked Water Sim“-Tutorial (schwach): https://lilys.ai/de/notes/unreal-engine-5-20251128/witcher-4-baked-water-sim-ue5
- UAF-Plugin-Index (Status): https://unrealdirective.com/resources/engine-plugins/uaf/
- „Chasing Waterfalls“ (Niagara-Talk, Orlando 2025): https://forums.unrealengine.com/t/talks-and-demos-chasing-waterfalls-using-niagara-to-power-a-mobile-rts-unreal-fest-orlando-2025/2539568


---

