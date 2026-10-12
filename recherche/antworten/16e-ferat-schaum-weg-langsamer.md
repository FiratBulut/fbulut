# Antwort zu Auftrag 16e – Schaum weg, langsamer, Tempo nach Steigung

Stand 12.10.2026. Grundlage sind Auftrag 16e (Ferat 18:50), der 16d-Nachtrag 19:00 (Punkt 2: drei lange Bäche
ungeteilt), die Antworten 16a mit allen Nachträgen, 16b, 16c und 16d, `vorlagen/daten/material_parameter.json`
(`M_Eldarien_Wasser_Schaum8`), das Bild `bilder/swr/c2_wcbs_klar.jpg` und `skripte/fluss_sim/`.

**Quellenlage:** `dev.epicgames.com`, `docs.unrealengine.com` und `forums.unrealengine.com` sind aus der Cloud weiter nicht
lesbar (DNS-Fehler bzw. Proxy 403). Web-Belege stammen deshalb aus **Suchmaschinen-Auszügen**. Kennzeichnung wie in 16a–16d:
- [Doku]: Epic-Doku bzw. API, Auszug
- [Code 12]: Epic-Quelltext 5.6.1, gelesen in der früheren Antwort `12-recherche-wasser-gpu-schatten.md`
- [Forum]: Auszug
- [Projekt]: eigene Daten
- [Test 16b]: eure Messung
- [Ableitung]: aus den Belegen geschlossen
- [vermutlich]: Name oder Wirkung nicht belegt

## Kurzfazit

- **Schaum aus, ohne die Oberfläche zu verlieren:** Ferats Vorabtest ist der richtige erste Schritt.
  - `Foam Opacity` 0 und `Foam Boost` 0 in `MI_EL_SWR_Klar` blenden den gebackenen Simulationsschaum aus.
  - Normalen, Spiegelung und Refraktion hängen an eigenen Werten und bleiben.
  - `Sim Foam Scale` ist sehr wahrscheinlich die Kachelgröße der Schaumtextur, **kein Schalter**: auf 350 lassen.
- **Allein reicht das wahrscheinlich nicht.** Ihr habt in 16b gesehen, dass `Foam Opacity` 0,9 → 0,5 „nur wenig“ ändert.
  Ein großer Teil des Weiß kommt also an `Foam Opacity` vorbei. Zwei Quellen sind wahrscheinlich:
  1. **unsere eigenen `ELD_*`-Schaumregeln** im Master (Strömung, Fels, Ufer);
  2. **die Gischt-Teilchen des Sekundär-Emitters** der SWR. Sie laufen auch gebacken (3 Dispatches) und hängen an keinem
     Wasser-Material.

  Darum gibt es eine Reihenfolge mit Prüfbild nach jedem Schritt (Tabelle 1).
- **Neu backen muss man dafür nicht.** Alle Material-Werte wirken sofort. Der gebackene Schaum bleibt in den Daten, wird aber
  nicht mehr gezeigt.
- **„Ein wenig Schaum nur an Fällen“:** Ich empfehle **Option B**. Das Material lässt den Simulationsschaum nur in kleinen
  Kapseln am Aufprall der Vorhang-Fälle durch. Die Daten stehen jetzt im Export (`schaum_maske`, 170 Kapseln in
  33 Gewässern).
  - Dazu bleiben die Niagara-Aufprall-Effekte an den Vorhang-Fällen.
  - Schaumobjekte (Option A) nur als Rückfall: Decals erscheinen auf Single-Layer-Water nicht, und starre Teppiche fließen
    nicht mit.
- **Tempo nach Steigung (im Export umgesetzt, Commit `b71fd13`):**
  - Jeder Splinepunkt bekommt `tempo_ms` nach Manning-Strickler aus dem Spiegelgefälle.
  - Becken haben Rückstau: v = Abfluss / Querschnitt.
  - Die Werte werden geglättet; dazu kommt ein globaler `tempo_faktor` (1,0).
  - Für UE: `WaterVelocityScalar` = `tempo_ms` × 100 in **cm/s**.

  | | vorher | nachher |
  |---|---|---|
  | flache Becken (Median) | 0,8 m/s | **0,21 m/s** |
  | Lippen (Median) | 2,4 m/s | **1,21 m/s** |
  | Strecken mit Gefälle > 15 % (Median) | 2,4 m/s | **1,26 m/s** |
  | alle Punkte im Mittel | 1,64 m/s | **0,69 m/s** |
  | C2 im Mittel | 1,75 m/s | **1,36 m/s** |
  | C2-Becken | 0,8 m/s | **0,23 m/s** |
- **Sichtbares Fließen im Spiel:** Im Spiel (WCBS) kommt es aus der **gebackenen** Strömung mal den Flowmap-Werten des
  Materials. Die Spline-Werte überschreibt die gebackene Simulation [Doku].
  - Für „einen Tick langsamer“ reichen `Simulation Flowmap Speed` 0,75 → **0,5** und `SIm Flowmap Speed` 1,5 → **1,0**.
    Neu backen ist dafür nicht nötig.
  - `MaxFlowVelocity` 1024 ist kein Tempo-Regler, sondern die Kodiergrenze. Nicht ändern.
- **`sim_speed` 10 / `num_steps` 10:** Nach Name und Verhalten sind das Zeitraffer und Teilschritte [vermutlich]. Sie
  bestimmen, wie schnell die Simulation einläuft, nicht die Strömung im eingelaufenen Zustand.
  - Deshalb fließt **LIVE_SIM** sichtbar zu schnell. Tempo bitte nur in WCBS bzw. PIE beurteilen.
  - Für das Backen lassen. Ein Test (V1 unten) klärt, ob die gebackene Strömung davon abhängt.
- **Drei lange Bäche jetzt ungeteilt** (Bach bis 0,40 m Zelle):

  | Bach | Zelle |
  |---|---|
  | `B_R_P4_M2_04` | 0,311 m |
  | `B_K1_WASSERFALL_WEST_03` | 0,362 m |
  | `B_R_P3_P0_04` | 0,400 m |

  - Geteilte Gewässer 8 → 5, SWR 202 → 199.
  - **Eure Vergleichsbilder 0,27 / 0,19 m stehen noch aus.** Bis dahin gibt der Prüfer für diese drei einen HINWEIS.
- **Prüfer:** 0 FEHLER, 0 WARNUNG, 68 HINWEIS. Zwei Läufe sind byte-gleich (183 Dateien). Alle 9 neuen Gegenproben ergeben
  FEHLER.

## 1. Schaum aus

### 1.1 Wo der Schaum im Spielbild (WCBS) herkommt

Im Spiel zeichnet der Water Body mit unserem Master (`MI_EL_SWR_Klar`, Kind von `MI_Eldarien_Wasser_Fluss`) und liest die
gebackenen Daten über `BakedWaterSimTex(VT)` [Projekt, 16a B5]. Daneben läuft das Niagara-System der SWR mit 3 Dispatches
weiter [Test 16b].

| Quelle | was es ist | Schalter | wirkt in WCBS |
|---|---|---|---|
| **S1 Simulationsschaum** | Die Simulation schreibt beim Backen einen Schaumwert in die gebackenen Daten. Das Material liest ihn und mischt ihn in Farbe, Rauheit und Normale. | `Foam Opacity`, `Foam Boost`, `Foam powr`, `SimFoam Contrast`, `Sim Foam *` | ja, sofort, ohne neues Backen |
| **S2 Epic-Flussschaum** aus der Water-Info-Strömung (Spline-Tempo), Ufer- und Distanzfeld-Schaum | Schaumtextur nach Strömung und Abstand zu Felsen | `Foam Opacity`/`Foam Boost` (gleiche Familie [vermutlich]), `River Foam Scale`, `Foam Distance`, `Depth for DF Foam` | ja |
| **S3 unsere `ELD_*`-Schaumregeln** | Strom-, Fels-, Distanzfeld- und Uferschaum aus Schaum6–8 | `ELD_Strom_Schaum`, `ELD_Fels_Schaum`, `ELD_DF_Schaum`, `ELD_Ufer_Schaum`, `ELD_Schaum_Deckkraft` | ja; ob `Foam Opacity` sie mit abdeckt, ist unbelegt |
| **S4 Gischt-Teilchen** `SW_River_Secondary_Emitter` (`M_SW_Foam`) | GPU-Teilchen über der Fläche, auch gebacken aktiv (3 Dispatches) | keiner im Water-Body-Material; Emitter aus | ja |
| S5 Nature-Water-FX an den Fällen | `NS_Impact_*`, `NS_Waterfall_*`, `NS_Wake_*` aus dem Plan | Effekte je Fall | nur an Fällen |

- **Befund aus 16b:** `Foam Opacity` 0,9 → 0,5 änderte das Bild „nur wenig“.
  - Läge alles Weiß in S1/S2, müsste es dabei deutlich dünner werden.
  - Das spricht für einen großen Anteil von S3 und/oder S4 [Ableitung].
  - Im Bild `c2_wcbs_klar.jpg` (rechts unten) wirkt der Schaum flockig-körnig. Das passt zu Teilchen (S4) oder zum
    `ELD`-Fleckenschaum (S3) besser als zu einer glatten Zelltextur [Ableitung].
- **Was die Simulation erzeugt (gebacken):** nur S1. S4 entsteht zur Laufzeit aus den gebackenen Daten [vermutlich]. S2 und S3
  sind reine Material-Logik.

### 1.2 Werte in Reihenfolge (Tabelle 1, `MI_EL_SWR_Klar` und Kopie für die Vorschau)

Nach jedem Schritt ein Bild von `kn0_unten` und `kn0_nah_s119` in WCBS. Erst weitermachen, wenn noch Schaum zu sehen ist.

| Schritt | Parameter | heute (`MI_EL_SWR_Klar`) | **neu** | Begründung |
|---|---|---|---|---|
| 1 | `Foam Opacity` | 0,6 (Auftrag 203) | **0** | blendet S1 und S2 aus. Farbe, Rauheit und Streuung des Schaums fallen weg; Wasserfarbe, Normalen und Refraktion bleiben |
| 2 | `Foam Boost` | 0,8 | **0** | Faktor auf die Schaummenge [vermutlich]. Doppelt sicher, falls `Foam Opacity` nur die Deckkraft der Farbe regelt und der Schaumwert noch Rauheit oder Normale formt |
| 3 | `Sim Foam Normal` | 1 | **0** | Normalen-Anteil aus dem Schaumwert [vermutlich]. Sonst bleiben schaumförmige Beulen auf klarem Wasser |
| 4 | `ELD_Strom_Schaum` / `ELD_Fels_Schaum` / `ELD_DF_Schaum` | 0,8 / 1,6 / 1,2 | **0 / 0 / 0** | unser eigener Strom- und Felsschaum (S3) |
| 5 | `ELD_Ufer_Schaum` | 0,45 | **0** (später ggf. 0,1) | Ferat will gar keinen Schaum; ein ganz dünner Saum hilft nur, die Wasserlinie zu lesen |
| 6 | `ELD_Schaum_Deckkraft` | 0,05 | **0** | Grunddeckkraft des `ELD`-Schaums [vermutlich] |
| 7 | **Sekundär-Emitter aus** | an | **aus** | S4. Test: `nc.set_emitter_enable('SW_River_Secondary_Emitter', False)` (16a D3, 16b D8); dauerhaft siehe 1.3 |
| – | `Sim Foam Scale` | 350 | **350 lassen** | wahrscheinlich die Kachelgröße der Schaumtextur in cm, nicht die Menge. In 16a (Variante 350 → 700) ohne Wirkung. „Hoch“ macht die Flocken größer, nicht weniger |
| – | `SimFoam Contrast`, `Foam powr`, `Foam Texture Blend Min` | 4 / 0,6 / 0,6 | lassen | ohne Wirkung, wenn Opacity bzw. Boost 0 sind; für Option B wieder wichtig |
| – | `Foam Emissive` | 0 | 0 | bleibt aus |

**Oberfläche erhalten** (nicht anfassen bzw. leicht anheben, damit das klare Wasser nicht „tot“ wirkt):

| Parameter | Wert | Wirkung |
|---|---|---|
| `Sim Velocity Normal Strength` | 10 → **15** | Riffel aus der gebackenen Strömung; ohne Schaum der wichtigste Hinweis auf fließendes Wasser (16b Abschnitt 4) |
| `Fluidsim Normal Strength` | 1 | Interaktion um die Spielfigur |
| `Default Near Normal Strength` | 0,25 → **0,4** | feine Kräuselung nah |
| `Water Roughness` / `Water Specular` | 0,02 → **0,04** / 0,225 | breitere Glanzlichter, sichtbar aus mehr Winkeln (16b) |
| `Refraction` | 1,15 | Grund verzerrt sichtbar |

- **Erwartung:** Becken und Rinnen klar. In den Rinnen sieht man die Strömung an Riffeln, Glanzlichtern und am verzerrten
  Grund statt an weißer Fläche.
- **Bleibt nach Schritt 7 noch Weiß,** zeichnet ein anderer Pfad. Dann bitte die Liste aus 1.4 schicken.

### 1.3 Sekundär-Emitter dauerhaft aus

- **Für das ganze Spiel:** eine Kopie von `Grid2D_SW_River` unter `/Game/Eldarien/Welt/Wasser/SWR/NS_EL_SW_River` anlegen.
  Darin `SW_River_Secondary_Emitter` abhaken und die Kopie in den Projekteinstellungen (Plugins → Water ShallowWaterSimulation)
  eintragen. Das ist Weg B aus 16a.
  - Das spart zugleich einen Teil der 3 Dispatches je geladener SWR (16b 2.3) [Ableitung].
- **Neu backen?** Wahrscheinlich nicht. Die Teilchen sind Darstellung, nicht Simulationsdaten [vermutlich].
  - Prüfen an C2: Nach dem Umstellen und einem Editor-Neustart in WCBS ansehen. Zeichnet `SWR_C2` nichts mehr, weil die SWR
    das System neu anlegt, einmal neu backen.
- **Gischt an Fällen** kommt weiter aus den Nature-Water-FX (S5).

### 1.4 Namen prüfen (Python, nur lesen)

Alle Namen stammen aus `material_parameter.json` (unser Master, Epic-Familie) [Projekt]. Ihre Wirkung ist aus dem Namen
abgeleitet. So liest man sie aus:

```python
import unreal
MEL = unreal.MaterialEditingLibrary
mi = unreal.load_asset('/Game/Eldarien/Welt/Wasser/MI_EL_SWR_Klar')          # Pfad ggf. anpassen
schl = ('foam', 'schaum', 'flow', 'velocity', 'speed', 'tempo', 'sim', 'normal', 'eld_')
for art, namen, wert in (
        ('s', MEL.get_scalar_parameter_names(mi), MEL.get_material_instance_scalar_parameter_value),
        ('v', MEL.get_vector_parameter_names(mi), MEL.get_material_instance_vector_parameter_value),
        ('x', MEL.get_static_switch_parameter_names(mi), MEL.get_material_instance_static_switch_parameter_value)):
    for n in sorted(str(x) for x in namen):
        if any(k in n.lower() for k in schl):
            print(art, n, wert(mi, n))
# Niagara der SWR: Emitter und Materialien (16a D1)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
swr = next(a for a in eas.get_all_level_actors() if isinstance(a, unreal.ShallowWaterRiver))
c = swr.get_component_by_class(unreal.ShallowWaterRiverComponent)
nc = c.get_editor_property('river_sim_system')
for e in unreal.NiagaraFunctionLibrary.get_all_emitters(nc.get_asset()):          # vermutlich (16a: per hasattr pruefen)
    print(e.get_editor_property('emitter_name'), e.get_editor_property('is_enabled'),
          [m.get_name() for m in e.get_editor_property('used_renderer_materials') if m])
for n in ('sim_speed', 'num_steps', 'source_size', 'resolution_max_axis', 'render_state'):
    print(n, c.get_editor_property(n))                                               # source_size: vermutlich
```

- **Benutzerparameter von `Grid2D_SW_River`** (Schaum-Schwelle, Zerfall, Reibung): Ihre Namen sind weiter unbelegt; die
  Parameter-Referenz von Epic ist nicht lesbar.
  - Bitte ein Bildschirmfoto des Panels „User Parameters“ bzw. „Override Parameters“ an der Niagara-Komponente der SWR.
  - Gesucht sind Namen mit „Foam“, „Threshold“, „Decay“, „Friction“, „Manning“, „Drag“.
  - Für „Schaum aus“ braucht man sie nicht: Das Material blendet ihn aus.

### 1.5 „Ein wenig Schaum“ nur an Fällen: Option A oder B

| | **Option A**: Schaumobjekte + Niagara nur an Vorhang-Fällen | **Option B**: Maske über den Simulationsschaum |
|---|---|---|
| Daten | vorhanden: `faelle[].vorhang`, `schaum_objekte` (170 Teppiche, 784 Straßen, 273 Kehrwasser) | **neu im Export:** `schaum_maske` je Gewässer (170 Kapseln) |
| Aussehen | starre Netze; fließen nicht mit, liegen auf dem gebackenen Wasser | Schaum der Simulation: liegt genau am Aufprall, fließt mit, läuft talwärts aus |
| Technik | Decals erscheinen auf SLW nicht ([Forum], Antwort 12) → Translucent- oder Masked-Netze mit Flipbook; Overdraw | eine Maske im Master (Abstand zu bis zu 8 Kapseln, weicher Rand) × Simulationsschaum; kein Overdraw |
| Aufwand | Bau-Werkzeug setzt Netze | Master einmal erweitern; je Gewässer ein Kind-MI mit den Kapsel-Werten (vom Bau-Werkzeug aus dem Export) |
| neu backen | nein | nein (der Schaum ist schon gebacken) |

**Empfehlung: Option B**, dazu die Niagara-Aufprall-Effekte (`effekte` mit Rolle `aufprall`/`fall`) **nur an Vorhang-Fällen**.

Begründung:
- Der Schaum entsteht dort, wo die Simulation ihn rechnet, und bewegt sich mit der gebackenen Strömung.
- Option A braucht wegen SLW durchscheinende Netze, die sich nicht mitbewegen. Das wirkt an einem 4-m-Fall eher wie ein
  Aufkleber.
- Antwort 12 hatte die Maske im Wassermaterial schon als besten Weg für Fallschaum genannt.
- Option A bleibt der Rückfall, falls die Maske im Master nicht geht.

**Felder `schaum_maske`** (Beispiel C2 im Gewässer `F_ERLENBACH`):

```json
"schaum_maske": {"kapseln": [
   {"fall": "F_ERLENBACH_1V_C2_s1_S04", "s_m": [70.55, 76.55], "a_cm": [-174161.7, -234491.5, 8421.5],
    "b_cm": [-174375.6, -233931.6, 8405.4], "radius_m": 3.0, "staerke": 0.93}, "… S05, S10, S13"],
 "n": 4, "slots_max": 8, "ueber_slots": false,
 "felder_material": "je Slot k: ELD_Fall_A_k = (a.x, a.y, radius_cm, staerke), ELD_Fall_B_k = (b.x, b.y, 0, 0) (Vorschlag)"}
```

- **Regel** (`regeln.schaum.maske`):
  - je Vorhang-Fall eine Kapsel vom Fuß `a_cm` bis zum Ende des Aufprallteppichs `b_cm`, höchstens Fuß + 6 m;
  - Radius = halbe Teppichbreite in [1; 3] m;
  - Stärke = Fallhöhe / 5 m in [0,4; 1].
- **Zahlen:** 170 Kapseln in 33 Gewässern, Radius im Median 1,26 m (1,06–3,0 m).
- **Mehr als 8 Kapseln:** 6 Sehens-Gewässer (Treppen in Farnschlucht, Schleierwand, Moränensee, Gletschertöpfen; 9–17
  Vorhang-Fälle). Dort braucht es 16 Slots oder eine kleine Maskentextur je Gewässer. Bitte im Master gleich 16 Slots
  vorsehen.
- **Im Master (Vorschlag):** `Maske = max_k (staerke_k × (1 − smoothstep(r_k − 1 m, r_k, Abstand(xy, Strecke a_k b_k))))`.
  Dann `Foam Opacity` × Maske statt `Foam Opacity`. Innerhalb der Kapsel gelten die 16b-Werte (`Foam Boost` 0,45,
  `Foam powr` 1,5), außerhalb ist es 0.

## 2. Tempo nach Steigung

### 2.1 Wie das Tempo heute in den Export kommt

- **Gefälle-Pläne:** Das Tempo hängt fest an der Rolle des Punkts (`gefaelle_plan.py`, `KN["tempo"]`).

  | Rolle | Becken | Lippe | Fuß | Rampe, Bogen, Wand |
  |---|---|---|---|---|
  | Tempo | 0,8 m/s | 2,4 m/s | 1,5 m/s | 3,0 m/s |

  Flussstücke mit Plan haben 0,8 m/s, ohne Plan das `v` der Weltdaten.
- **Rohe Läufe:** `v` aus `wasser_welt.json` bzw. `baeche_alle.json`, Median 1,8 m/s, bis 4,5 m/s.
- **Sehens-Bäche:** über dieselben Rollen. Töpfe hatten 0,1 m/s.
- Der Exporter hat das bisher nur auf [0,1; 10,24] m/s begrenzt und als `WaterVelocityScalar_cm_s` (6. Feld je Punkt)
  ausgegeben.

### 2.2 Was UE erwartet

- `WaterVelocityScalar` ist ein `FInterpCurveFloat` in `UWaterSplineMetadata`, „the current of the water at this vertex“
  [Doku 4.27/5.x, Auszug].
- **Einheit cm/s**, Standard 128 (`FWaterSplineCurveDefaults.DefaultVelocity`). In die Water-Info-Textur wird der Wert
  relativ zu `r.Water.MaxFlowVelocity` = 1024 kodiert; ein negativer Wert kehrt die Richtung um [Code 12].
  - Die Einheit selbst steht in keinem Auszug wörtlich. Sie folgt aus den UE-Längeneinheiten (cm) und der 1024er-Grenze
    [Ableitung].
- **Mit gebackener Simulation** überschreibt diese Höhe, Tiefe, Strömung und Normale der Spline für Auftrieb und Abfragen.
  Gemeint ist `FBuoyancyWaterSplineData.ShallowWaterSimData`: „overrides the splines for water height/depth/velocity/normal“
  [Doku, Auszug].
- **Wozu das Spline-Tempo dann noch zählt** [Ableitung]:
  1. **Ferne:** Hinter dem Ladebereich zeichnet der Water Body ohne Simulation (16a, Entscheidung 1). Dort fließt die
     Flowmap mit dem Spline-Tempo (`River Flowmap Speed` × Water-Info-Strömung).
  2. Auftrieb und Abfragen, falls `use_baked_sim_for_queries_and_physics` aus ist.
  3. Wahrscheinlich der **Zufluss an der Quelle** der SWR beim Reset [vermutlich]. Deshalb gehört das Tempo zum
     Fingerabdruck.
- **Python:** Das Bau-Werkzeug setzt das Tempo wie bisher je Punkt aus `punkte[i][5]`. Gegenprobe im Editor:
  `wbc = wb.get_component_by_class(unreal.WaterBodyRiverComponent)`, dann
  `wbc.get_water_spline_metadata().get_editor_property('water_velocity_scalar')`. Die Methode `get_water_spline_metadata`
  ist als C++-Funktion belegt, ihr Python-Name nicht [vermutlich].

### 2.3 Regel (umgesetzt, `regeln.tempo`, Tabelle 2)

| Schritt | Formel / Wert | Begründung |
|---|---|---|
| Gefälle I | (z(s − 2 m) − z(s + 2 m)) / 4 m am Wasserspiegel der Spline, am Rand einseitig; Stufen zählen mit | Lippe und Fuß werden schnell, die Mitte langer Becken nicht |
| Abfluss Q | Q = 0,2 m/s × Median(Breite × 0,6 × Depth) über ± 100 m | Der Plan kennt keinen Abfluss. Ein Becken mittlerer Größe soll mit 0,2 m/s fließen. `Depth` ist die größte Bett-Tiefe; die mittlere Tiefe ist etwa 0,6 davon |
| Abfluss je Meter | q = Q / Breite | Kontinuität: Engstellen schneller, breite Stellen langsamer |
| Fließen | **v = k_st^0,6 · q^0,4 · max(I; 0,0001)^0,3** | Manning-Strickler bei Normalabfluss, breites Gerinne (R ≈ h). Die Planer-Tiefe ist in Rinnen keine Fließtiefe, daher die Normaltiefe aus q und I |
| Rauheit k_st | **Bach 15**, Fluss 25 m^(1/3)/s (n = 0,067 / 0,04) | Wildbach mit Blöcken und Stufen-Becken-Folge 10–20, Geröllfluss 25–30 |
| Becken, Töpfe | v = min(v; q / h) | Rückstau: Die Lippe unterhalb hält den Spiegel, die Planer-Tiefe ist dort die Wassertiefe. Die C2-Becken haben 2 % Spiegelgefälle; Manning allein gäbe dort 1 m/s |
| Grenzen | [0,1; 2,5] m/s | Becken 0,1–0,3, steile Rinnen 1–2,5 (mittlere Geschwindigkeit; Manning überschätzt über 10 % Gefälle wegen der Blöcke) |
| Glätten | Gauß σ 0,75 m (Gewicht × Punktabstand), dann Änderung ≤ 0,6 m/s je m (untere Hülle: nur Spitzen sinken) | keine Sprünge; das Wasser beschleunigt über 1–2 m zur Lippe |
| Feinabstimmung | × **`tempo_faktor`** (1,0) | z. B. 0,8 = alles 20 % langsamer. Die Grenzen gelten vor dem Faktor |
| Ausgabe | `spline.tempo_ms` (0,001 m/s); `WaterVelocityScalar_cm_s` = `tempo_ms` × 100; `spline.tempo_info` mit `gefaelle` und `kst` je Punkt | Der Prüfer rechnet aus den gerundeten Spline-Werten exakt nach |

**Kurven, wie sie sich ergeben** (Bach, q ≈ 0,2 m²/s, vor Glättung; Becken zusätzlich q / h):

| Gefälle | 0 % (Becken) | 0,1 % | 2 % | 5 % | 10 % | 36 % (C2-Rinne) |
|---|---|---|---|---|---|---|
| v | 0,2 | 0,3 | 0,8 | 1,1 | 1,35 | 1,95 m/s |

### 2.4 Vorher/nachher (2-m-Daten, 187 Gewässer, 18 721 Splinepunkte)

| Rolle | Punkte | vorher Median | **nachher Median** (p10–p90) |
|---|---|---|---|
| Becken | 2 432 | 0,80 | **0,21** (0,13–0,29) |
| Topf | 61 | 0,39 | **0,10** (0,10–0,14) |
| Lippe | 2 074 | 2,40 | **1,21** (0,77–1,55) |
| Fuß | 2 074 | 1,50 | **1,22** (0,77–1,53) |
| Rampe | 395 | 3,00 | **1,12** (0,14–1,74) |
| Fluss mit Plan (`river`) | 6 078 | 1,53 | **0,56** (0,19–1,03) |
| roh | 5 466 | 1,80 | **0,50** (0,16–1,28) |
| **alle** | 18 721 | 1,50 (Mittel 1,64) | **0,58** (Mittel 0,69) |

| Spiegelgefälle | < 1 % | 1–5 % | 5–15 % | > 15 % |
|---|---|---|---|---|
| vorher Median | 0,87 | 1,61 | 1,84 | 2,40 |
| **nachher Median** | **0,28** | **0,45** | **0,74** | **1,26** |

- Die Rangkorrelation zwischen Tempo und Gefälle liegt je Gewässer im Median bei 0,93 (126 Gewässer mit genug Punkten).
  Darunter liegt nur `B_R2_R_P1_M2_01` mit 0,22 (HINWEIS).
- **C2** (Lauf `F_ERLENBACH_1V_C2`, 124 Punkte):

  | | vorher | nachher |
  |---|---|---|
  | Mittel | 1,75 m/s | **1,36 m/s** |
  | Becken (25) | 0,80 | **0,23** (0,15–0,44) |
  | Lippe (42) | 2,40 | **1,73** |
  | Fuß (42) | 1,50 | **1,72** |
  | Rampe (4) | 3,00 | **1,32** |
  | Gefälle > 15 % (88) | 2,40 | **1,71** |

  Beispiel S04/S05 (s im Gewässer `F_ERLENBACH`): Becken 72,6–78,8 m mit 0,21–0,27 m/s, Lippe 80,8 m mit 1,49 m/s, Fuß 1,62 m/s, Becken 83,7 m wieder
  0,21 m/s.
- **Bewertung:** C2 wird etwa ein Viertel langsamer, die Becken deutlich. Über alles halbiert sich das Spline-Tempo. Die alten
  Werte für flache Flussstücke (1,5–1,8 m/s aus Rolle bzw. Weltdaten) waren für 1–2 % Gefälle zu hoch.
  - Das sieht man im Spiel nur in der Ferne (ohne Simulation) und an der Flowmap.
  - Wirkt die Ferne danach zu träge: `tempo_faktor` 1,2–1,3 (Rückfrage 2).

### 2.5 Sichtbares Fließen im Material und in der SWR (Tabelle 3)

| Wert | heute | **Start** | wirkt auf | neu backen |
|---|---|---|---|---|
| `Simulation Flowmap Speed` | 0,75 | **0,5** | Laufgeschwindigkeit der Textur über die gebackene Strömung (WCBS) [vermutlich]; Hauptregler für „einen Tick langsamer“ | nein |
| `SIm Flowmap Speed` | 1,5 | **1,0** | zweite Flowmap-Lage bzw. Interaktion [vermutlich]; im gleichen Verhältnis senken, sonst laufen die Lagen auseinander | nein |
| `Sim Flowmap Detection` | 1,5 | lassen | Schwelle, ab der eine Flowmap gilt [vermutlich] | nein |
| `River Flowmap Speed` | 0,003 | **lassen** | × Water-Info-Strömung (Spline-Tempo in cm/s). Das Tempo sinkt schon in der Spline, sonst würde doppelt gebremst | nein |
| `River Flowmap Detection Velocity` | 64 | lassen | Schwelle in cm/s [vermutlich] | nein |
| `MaxFlowVelocity` | 1024 | **nie ändern** | Dekodiergrenze = `r.Water.MaxFlowVelocity`; ein anderer Wert verfälscht die Strömung, er bremst nicht | – |
| `WPO Flowmap` | 6 | 6 (bei Unruhe 4) | Vertex-Verschiebung längs der Strömung | nein |
| `ELD_Wirbel_Tempo` | 0,35 | 0,25 | Drehgeschwindigkeit unserer Wirbel-Normalen | nein |
| SWR `sim_speed` | 10 | **10 lassen** | Zeitraffer der Simulation [vermutlich]: läuft 10× schneller ein. In LIVE_SIM fließt dadurch alles zu schnell, in WCBS nicht | nur wenn geändert |
| SWR `num_steps` | 10 | **10 lassen** | Teilschritte je Bild [vermutlich]: Stabilität bei feinen Zellen | nur wenn geändert |
| Niagara-Reibung (Name unbelegt) | ? | erst nach der Liste aus 1.4 | die **physikalische** Strömung der Simulation: mehr Reibung, langsameres und tieferes Wasser | **ja** |

**Test V1 (5 min, C2):** `Velocity Debug` = 1 in WCBS zeigt die gebackene Strömung. Dann `sim_speed` 10 → 2 setzen, laufen
lassen, bis alles eingelaufen ist, neu backen und vergleichen.
- Gleiches Bild: `sim_speed` ist reiner Zeitraffer und bleibt 10.
- Langsamere Strömung: Der Wert skaliert die Strömung. Dann ist er ein zweiter Hebel (Backen dauert länger).

### 2.6 Prüfer

- `tempo_ms` und `tempo_info` je Punkt; `WaterVelocityScalar_cm_s` = `tempo_ms` × 100 (± 0,05).
- Im Rahmen [0,1; 2,5] × `tempo_faktor`; Änderung ≤ 0,6 m/s je m × Faktor.
- Mit `tempo_regel` nachgerechnet (± 0,0015 m/s); `kst` aus {15, 25}.
- **Monotonie-Bezug:**
  - global steigt das Median-Tempo je Gefälleklasse (FEHLER, wenn nicht);
  - flache Becken im Median ≤ 0,3 m/s, steile Rinnen ≥ 1,0 m/s;
  - je Gewässer Rangkorrelation < 0,3 = HINWEIS.

## 3. Drei lange Bäche ungeteilt (16d-Nachtrag Punkt 2)

- **Regel:** `swr.zelle_max_bach_ungeteilt_m` = 0,40. Ein Bach bleibt ungeteilt, solange seine Zelle bei 2048 ≤ 0,40 m
  bleibt, also bei einem Rechteck ≤ 819 m. Erst darüber wird geteilt; die Teilstücke halten wie bisher 0,30 m.
  `swr.zelle_max_m` nennt den jeweils geltenden Höchstwert.

| Bach | Länge | vorher (16d-Regel) | **nachher** | Hindernis-Instanzen |
|---|---|---|---|---|
| `B_R_P4_M2_04` | 744 m | 2 SWR: 522 × 63 m / 2048 / 0,255 m und 127 × 151 m / 608 / 0,248 m | **1 SWR, 636 × 206 m, 2048, 0,311 m** | 1 065 |
| `B_K1_WASSERFALL_WEST_03` | 1 040 m | 2 SWR: 614 × 120 m / 2048 / 0,300 m und 140 × 232 m / 928 / 0,250 m | **1 SWR, 742 × 330 m, 2048, 0,362 m** | 509 |
| `B_R_P3_P0_04` | 945 m | 2 SWR: 403 × 96 m / 1632 / 0,247 m und 429 × 131 m / 1728 / 0,248 m | **1 SWR, 819 × 217 m, 2048, 0,400 m** | 0 |
| `B_R_P3_P0_02` | 1 295 m | 2 SWR (0,25 m) | unverändert geteilt (ganz 0,48 m) | 0 |

- **Gesamt:**

  | | vorher | nachher |
  |---|---|---|
  | geteilte Gewässer | 8 | **5** |
  | Gewässer mit einer SWR | 179 | **182** |
  | SWR | 202 | **199** |
  | Nähte | 15 | **12** |
  | Auflösungen ≤ 512 / 513–1024 / 1025–2048 | 95 / 58 / 49 | 95 / 56 / 48 |

  Geteilt bleiben `F_HAUPTFLUSS_3`, `F_ELFENFLUSS`, `F_DSCHUNGELFLUSS`, `B_R_P3_P0_02` und `F_ERLENBACH`.
- **Zellen der Bach-SWR:** 176 × ≤ 0,25 m, 9 × 0,25–0,30 m, die drei oben 0,31 / 0,36 / 0,40 m.
- **Prüfer:** ungeteilter Bach ≤ 0,40 m (FEHLER), > 0,30 m als HINWEIS. Der HINWEIS lautet „Vergleichsbilder 0,27/0,19 m
  ausstehend“.
- **Offen:** Eure Vergleichsbilder C2 mit 0,27 m (205) und 0,19 m (210) stehen noch aus. Zeigt 0,27 m schon sichtbar gröberen
  Schaum bzw. gröbere Lippen, wird 0,40 m zu grob sein. Dann setzt ihr `zelle_max_bach_ungeteilt_m` auf 0,31 und neu
  exportieren: `B_R_P4_M2_04` bleibt ungeteilt, die anderen zwei werden wieder geteilt. Mit Option B (Schaum nur in Kapseln)
  fällt die Zelle beim Schaum weniger auf.

## 4. Lauf und Prüfung

- **Rechenweg:** in einem eigenen `git worktree` vom aktuellen HEAD (`6c8787b`). Die uncommitteten Planer-Dateien des anderen
  Agenten im Arbeitsbaum blieben unberührt.
  - Planer im Worktree: Gefälle-Planer `--alle` (98 Lauf-Pläne), Sehens-Planer für alle 15 Biome.
  - Exporter und Prüfer auf den 2-m-Daten.
  - Der HEAD enthält schon das Bachbett-Modul (Totholz, Schlamm). Deshalb steigen die Kollisionseinträge gegenüber 16d auf
    24 666 (24 512 eindeutig, 1 768 überspannt). Das ist unabhängig von 16e.
- **Export:** 187 Gewässer in 180 Dateien, 199 SWR-Bereiche, 47 Vorschläge, ~35 s. Zwei Läufe sind byte-gleich (183 Dateien).
- **Prüfer:** **0 FEHLER, 0 WARNUNG, 68 HINWEIS**.
  - 24 × Mündung offen, 20 × Lücke (3 weitere in Seen ohne HINWEIS), 6 × mehr als 8 Kapseln, 5 × geteilte Simulation, 5 × Fuß am Gewässerende,
    3 × Bach-Zelle > 0,30 m, 1 × schwache Tempo-Korrelation, je 1 × Tempo-Klassen, Läufe, Vorschläge und Determinismus.
- **Fingerabdrücke:** Bei allen 196 weiter bestehenden SWR-Bereichen ändert sich nur der Spline-Teil (Tempo). Gelände und
  Objekte bleiben gleich.
- **Gegenproben** (alle FEHLER mit Exit 1):
  - Tempo +0,9 m/s an einem Punkt (Sprung, Regel, Fingerabdruck);
  - Tempo 3,2 m/s;
  - `WaterVelocityScalar` ≠ `tempo_ms` × 100;
  - Tempo × 0,9 (nicht nach der Regel);
  - alle Tempi 1,0 m/s (Median steigt nicht, Becken zu schnell);
  - Kapsel an einem Fall ohne Vorhang;
  - Kapsel-Radius 5 m;
  - `zelle_max_m` 0,30 bei ungeteiltem Bach.
- **Beispiele** unter `antworten/fluss_sim/` neu: `F_ERLENBACH` (C2 mit `tempo_ms`, `schaum_maske` mit 4 Kapseln), Karsee,
  Elfentreppe, `zusammenfassung.json` (neu: `tempo` mit vorher/nachher je Rolle, Gefälleklasse, Kategorie und C2;
  `schaum_maske`; `varianten_zelle` mit Regel 16e und 16d), `vorschlaege.json`, `back_liste_auszug.json` (zusätzlich
  `B_R_P3_P0_04`).
- **README** (`skripte/fluss_sim/`): Abschnitte Tempo, Schaum-Maske, Zelle und Prüfer ergänzt.

## 5. Was neu gebacken werden muss

| Änderung | neu backen? |
|---|---|
| Schaum-Werte im Material (Tabelle 1, Schritte 1–6), Oberflächen-Werte, Flowmap-Geschwindigkeiten (Tabelle 3) | **nein**, wirken sofort in WCBS |
| Sekundär-Emitter aus (Laufzeit-Test oder Kopie des Systems) | wahrscheinlich nein; nach dem Umstellen auf die Kopie einmal C2 prüfen, sonst C2 neu backen |
| Option B (Maske im Master, Kind-MI je Gewässer) | **nein**, der Simulationsschaum ist schon gebacken |
| Neues Spline-Tempo (`WaterVelocityScalar`) | **ja, formal**: Der Fingerabdruck (Spline-Teil) ändert sich bei allen SWR. Betroffen ist heute nur C2, und C2 wird für v3 ohnehin als `WBR_F_ERLENBACH` + SWR neu gebaut |
| Drei lange Bäche ungeteilt | noch nichts gebacken → einfach so bauen |
| `sim_speed`/`num_steps` (nur Test V1) bzw. Niagara-Reibung oder Schaum-Schwelle | ja |

Lokal:
1. `git pull`.
2. Exporter und Prüfer auf 1 m mit den Befehlen aus der README.
3. Material-Leiter (Tabelle 1, dann Tabelle 3) an `MI_EL_SWR_Klar` mit Bildern.
4. Liste aus 1.4 schicken.
5. V1 testen.

## Commits

- **`b71fd13`**: Exporter, Prüfer, Regeln v5, README, Beispiele.
- Commit dieser Antwort: siehe `git log` (Nachricht „Auftrag 16e: Antwort …“).

## Quellen

Alle Web-Seiten waren aus der Cloud nicht lesbar (DNS bzw. Proxy 403); die Inhalte stammen aus Suchmaschinen-Auszügen.

- [API 4.27: UWaterSplineMetadata::WaterVelocityScalar](https://docs.unrealengine.com/4.27/en-US/API/Plugins/Water/UWaterSplineMetadata/WaterVelocityScalar/index.html) und [UWaterSplineMetadata](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterSplineMetadata) – `FInterpCurveFloat`, „The current of the water at this vertex“ [Doku, Auszug]
- [API: FWaterSplineCurveDefaults](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/FWaterSplineCurveDefaults) – `DefaultVelocity`, `DefaultDepth`, `DefaultWidth` (float) [Doku, Auszug]; Standardwert 128 aus [Code 12]
- [API: FWaterSplineMetadataPhysics](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/FWaterSplineMetadataPhysics), [UWaterBodyComponent::GetWaterSplineMetadata](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterBodyComponent/GetWaterSplineMetadata) [Doku, Auszug]
- [API: FBuoyancyWaterSplineData](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Buoyancy/FBuoyancyWaterSplineData) – `ShallowWaterSimData` „overrides the splines for water height/depth/velocity/normal“; [FBuoyancyShallowWaterSampler](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Buoyancy/FBuoyancyShallowWaterSampler) [Doku, Auszug]
- [API: UShallowWaterRiverComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent) – `SimSpeed` (float), `SourceSize` (float), `NumSteps` (int), Bedeutung nicht im Auszug [Doku, Auszug]
- [Python: unreal.ShallowWaterSimParameters](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterSimParameters) – `ResolutionMaxAxis`, `WorldGridSize` [Doku, Auszug]
- [Tutorial/Forum: Baked River Simulations – Parameter Reference](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112) – nur Vorspann lesbar (SWR, Niagara, Material) [Forum]
- [Forum: Shallow body river – WCBS not rendering](https://forums.unrealengine.com/t/shallow-body-river-water-component-with-baked-sim-not-rendering/2688228) – WCBS zeigt nur Schaum (16a) [Forum]
- [Water Tools (UEFN)](https://dev.epicgames.com/documentation/en-us/fortnite/water-tools-in-unreal-editor-for-fortnite) – „Visualize Water Velocity“ zum Prüfen der Spline [Doku, Auszug]
- Fließformel und Rauheit (Lehrbuchwissen, nicht neu recherchiert): Manning-Strickler v = k_st R^(2/3) I^(1/2), bei
  Normalabfluss im breiten Gerinne v = k_st^(3/5) q^(2/5) I^(3/10). Strickler-Werte: Wildbach mit Blöcken 10–20, Geröllfluss
  25–30 m^(1/3)/s. Manning überschätzt die Geschwindigkeit in steilen Stufen-Becken-Bächen (Makrorauheit), daher die Kappe.
- Projekt:
  - `antworten/12-recherche-wasser-gpu-schatten.md`: Velocity-Kodierung bis 1024 cm/s, Standard 128, Decals auf SLW, Maske
    im Wassermaterial;
  - `vorlagen/daten/material_parameter.json` (`M_Eldarien_Wasser_Schaum8`);
  - `auftraege/16b-…` (Auftrag 203: Opacity wirkt wenig; 3 Dispatches);
  - `skripte/gefaelle/gefaelle_plan.py` (`KN["tempo"]`, `TEIL`), nur gelesen.

## Rückfragen

1. **Option B (Maske) bauen?** Wenn ja: Ist der Master-Umbau (16 Kapsel-Slots, Kind-MI je Gewässer aus `schaum_maske`) für
   euch machbar? Oder reicht vorerst „Schaum ganz aus“ plus Niagara-Aufprall nur an Vorhang-Fällen? Dann bleibt die Maske
   für später.
2. **Ferne zu träge?** Das Spline-Tempo halbiert sich im Mittel (0,69 statt 1,64 m/s), flache Flussstücke laufen mit
   0,5 m/s. Wenn die Ferne ohne Simulation danach steht, `tempo_faktor` 1,2–1,3 setzen; das ist eine Zahl in den Regeln.
3. **Niagara-Effekte an kleinen Fällen:** Bisher bleiben die Nature-Water-FX an **allen** 765 Fällen, auch an 0,7-m-Teilstufen.
   Ferat möchte Schaum nur an Wasserfällen. Sollen die Effekte mit Rolle `aufprall`/`wake` an Fällen ohne Vorhang entfallen?
   Das ließe sich im Export als Feld (`effekte_aktiv`) ausgeben.
4. **Bach-Zelle 0,40 m:** Nach euren Bildern 0,27/0,19 m bitte Bescheid geben, ob 0,40 m bleibt oder auf 0,31 m sinkt
   (Abschnitt 3).
5. **Liste aus 1.4** (Material-Schalter, Emitter, Benutzerparameter): Damit kann ich die [vermutlich]-Namen bestätigen bzw.
   die Reibung der Simulation als zweiten Tempo-Hebel nennen.
