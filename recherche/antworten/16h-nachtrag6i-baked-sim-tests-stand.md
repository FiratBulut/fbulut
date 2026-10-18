# Antwort 16h Nachtrag 6i – BAKED_SIM im Spiel, Regel §5.4, Umschalten zur Laufzeit, Nasslinien-Master, Breitenauslauf

Gelesen: recherche/auftraege/16h-nachtrag6i-baked-sim-tests-stand.md @ 11c254f0c95defaa25c481ed4047bf7c68625309 (Commit 999ddfe)

Stand 18.10.2026. Gesamtauftrag: 16h (Erlenbach p2, Talkaskade). Bearbeiter: Cloud-Recherche. Bereich: SWR-Darstellung p2, Steinmaterial
Talkaskade, Profilregel 19. Nächste Handlung: lokal die Tests T-c1, T-a1, T-b1 und T-a2 aus §1 (zusammen ≈ 45 min, alles im Speicher).

**Bezug, weitere gelesene Eingaben:**
- `recherche/README.md` @ 778d8a7b8ac1 (Commit 2b38873)
- `auftraege/16h-nachtrag6j-teilung-ergebnis.md` @ a49de2d42844 (8749f1c)
- `antworten/16h-nachtrag6h-live-vs-gebacken-dichte.md` @ bd89e6d10a0c (4bef977), §5 ganz
- `auftraege/16b-swr-c2-ganze-strecke.md` @ c9317909de90 (Kostentabelle, Nachtrag 16:30)
- 16a §a3/B1, 16f, 6d, 6e, 6f §5, 20 §5, Paketregeln `skripte/fluss_sim/README.md`
- `antworten/fluss_sim/p2_lokal/stein_albedo.json` @ de519d4e95d0
- `antworten/bach_anfaenge/bach_anfaenge_plan.json` @ 3f3f0c41a607 und `skripte/bach_anfaenge/bach_anfaenge_plan.py` @ a4e276e891e6 (beide 29a15c3)

**Kennzeichnung:**
- [Ferat]: euer lokaler Befund
- [Projekt]: Daten bzw. Regeln im Repository
- [Doku]: Epic-API- bzw. Python-Doku, nur als Suchauszug gelesen (siehe Quellen)
- [Forum]: Epic-Forum, nur als Suchauszug gelesen
- [Rechnung]: von mir mit den Repo-Daten gerechnet
- [Ableitung]: geschlossen, nicht belegt
- [offen]: nur durch den genannten Test zu klären

**Quellenzugang:** `dev.epicgames.com` und `forums.unrealengine.com` waren aus der Cloud nicht erreichbar (WebFetch: DNS-Fehler; curl: Proxy
403). Alle Web-Belege unten stammen deshalb aus Suchauszügen. Ein Suchauszug ist ein Hinweis, keine vollständige Quellenbestätigung. Die
entscheidende Frage (c) lässt sich lokal in einer Minute am 5.8.3-Header klären (T-c1). Das ist sicherer als jede Doku-Seite.

## Kurzfazit

1. **§1 (a) BAKED_SIM im Spiel – wartet auf Messung T-a1/T-a2 und Paket-Test T-a3.**
   - Belegt ist nur eure Einzelmessung an C2 (179 m, Auflösung 512, PIE): BAKED_SIM 0,3 ms und 3 Dispatches, WCBS 0,2 ms und 3 Dispatches.
     Gezählt wurde nur `Grid2D_SW_River`. Die Kosten für das Zeichnen der Fläche (Wasser-Pass) sind darin **nicht** enthalten.
   - Für p2 (≈ 2016 × 319 Zellen, also ≈ 6-mal so viele Zellen wie C2) gibt es keine Messung.
   - Zum gepackten Build gibt es **keinen positiven Beleg**. Ein Forenbericht (5.5/5.6) meldet eine gebackene SWR, die im gepackten Build
     nicht zeichnet. Im Log stehen dort „Ocean simulation system not loaded“ und „ocean patch normal RT is not initialized“ [Forum].
     Eine Lösung steht im Auszug nicht. PIE ersetzt diesen Test nicht.
2. **§1 (b) Regel §5.4 – beantwortet mit Einschränkung.** „Höchstens 3 Schaustellen“ war eine Budgetannahme (3 × 0,3 ms) und gilt nicht
   als Grenze. Neue Regel: BAKED_SIM dort, wo WCBS sichtbar versagt, solange die **gemessene** Summe im Wasserbudget 1,5 ms bleibt (§1.2).
   - Ob man die WCBS-Fläche auf die Simulationshöhe bringen kann, entscheidet **T-b1**: Messlatte und Drahtgitter in WCBS und in BAKED_SIM,
     dazu zwei MI-Schalter. Die Erwartungen und die jeweilige Entscheidung stehen vorab in §1.2.
   - Bis dahin bleibt Erlenbach p2 auf BAKED_SIM. Das ist euer gespeicherter Stand.
3. **§1 (c) Laufzeit-Umschalten – teilweise beantwortet.**
   - Im Editor und in PIE geht es per Python (`set_editor_property`). Das ist bei euch belegt: „Umschalten sofort“.
   - Im gepackten Spiel ist es **nach der Doku-Lage nicht möglich**: Laut API-Auszug ist von der SWR-Komponente nur `SetPaused` für
     Blueprint freigegeben. `RenderState` ist eine öffentliche Variable; `UpdateRenderState()` und `Rebuild()` erscheinen ohne
     Blueprint-Kennung [Doku].
   - Endgültig entscheidet die Zeile `UPROPERTY(...)` vor `RenderState` im 5.8.3-Header (T-c1, 1 min).
   - **Planungsfolge:** Den Render-State je Akteur fest wählen. Kein Umschalten nach Entfernung einplanen.
4. **§3 Prüfpunkte Flusskopien – erledigt durch 6j §1.** Der Versuch ist verworfen, und der Exporter sperrt Teilungspläne. Was vom
   Rebuild()-Befund bleibt, steht in §2 (drei Punkte). 6j wird getrennt beantwortet.
5. **§4 Nasslinie – beantwortet.**
   - **Mountain:** neuer Master **`M_EL_Mountain_NL` (anzulegen)**. Er entsteht als Kopie von `M_Master_material` plus `MF_EL_Spiegelhoehe`
     und `MF_EL_Nasslinie`, so wie MSR → MS2. Die Kinder `MI_EL_NL_<Paket-MI>` übernehmen alle Werte 1:1.
   - **Fab-Raw und Namaqualand:** keine neue Master-Datei, sondern `MI_EL_*` auf dem vorhandenen **`M_EL_Fels_MS2`**. Vorher die
     Kanalbelegung prüfen (ORM gegen AoRT).
   - **Neu für alle Nasslinien-Master:** `Nass_Spiegel_Versatz_cm` (anzulegen, Standard 0). Grund: Der gebackene Spiegel liegt 15–25 cm
     über der Spiegeltextur, aus der die Nasslinie liest (§4 eures Befunds).
   - Parameterliste und Werte stehen in §3.
6. **§6 Breitenauslauf – beantwortet, mit Formel.** Nach L kommt ein **Steigungsbegrenzer**: `b_i = min(b_orig,i; b_i−1 + g·Δs)` mit
   `g = max(0,10 m/m; 0,8·(B−b0)/L)`. Er gilt bis zum ersten Punkt, an dem das Original unter der Rampe liegt.
   - Mit den 2-m-Daten im Repo habe ich eure 9 Sprünge ≥ ×1,5 nachgerechnet [Rechnung]: 9 von 148 Anfängen, darunter
     B_R2_R_P3_P1_05 mit 1,89 → 4,00 m. Nach der Regel wird daraus 1,89 → **2,37** → 2,83 m (Original).
   - Insgesamt ändern sich 40 Punkte an 35 Anfängen. Der Auslauf ist höchstens 29 m lang. Drei der Gewässer stehen noch nicht in der
     Neu-Backen-Liste.
7. **§2 Band nass – zur Kenntnis, unsere Erwartung ist widerlegt.** 65 % bei > 5 cm und 46 % bei > 10 cm sind echtes Wasser neben dem Bett,
   kein dünner Film. Unsere Annahme „20–30 % bei > 5 cm“ (6g) war falsch. Das Weitere gehört zu 6j (T01 mit 8,7 cm: 13 % bei > 10 cm).
8. **§4/§5 Rückfragen – geschlossen**, je eine Zeile in §5.

## 1. BAKED_SIM im Spiel (§1 a–c)

### 1.1 (a) Kosten und gepackter Build: was belegt ist

| Aussage | Stand |
|---|---|
| C2, 179 m, Auflösung 512, PIE, `ProfileGPU`: LIVE_SIM 0,6 ms / 59 Dispatches, BAKED_SIM 0,3 ms / 3, WCBS 0,2 ms / 3 | [Ferat 16b], einmal gemessen, ohne Streuung |
| Gemessen wurde nur die Summe `Grid2D_SW_River`. Das Zeichnen der Fläche (Single-Layer-Water-Pass bzw. Niagara-Renderer) fehlt in der Zahl | [Ferat 16b], Folgerung [Ableitung] |
| Die 3 Dispatches laufen in beiden gebackenen Zuständen. Wahrscheinlich sind es der Gischt-Emitter `SW_River_Secondary_Emitter` und eine Lesestufe | [Ableitung 16b §2.1]; D8 lief nie |
| „Gebacken ≈ 0,2 ms, unabhängig von der Auflösung“ (16f) | stammt aus derselben C2-Messung; an p2 **nicht** geprüft |
| BAKED_SIM: Die SWR zeichnet selbst, ohne Water Zone und ohne Interaktion | [Leitfaden, 16a a3] |
| `EShallowWaterRenderState` hat sechs Werte: WaterComponent, WaterComponentWithBakedSim, LiveSim, BakedSim, DebugRenderBottomContour, DebugRenderFoam | [Doku] |
| Gepackter Build: gebackene SWR zeichnet nicht, Log „Ocean simulation system not loaded“ / „ocean patch normal RT is not initialized“, Auftrieb läuft | [Forum 2634176], 5.5/5.6, Lösung nicht im Auszug |
| WCBS zeichnet bei einem Nutzer nur Schaum | [Forum 2688228] |
| „Wasserwand“ in der Ferne bei gebackenem Zustand, verschwindet beim Näherkommen | [Forum 2818892] |
| Die Niagara-Systeme der SWR kommen aus den Projekteinstellungen, z. B. `UShallowWaterSettings.DefaultOceanPatchNiagaraSystem` (EditAnywhere, BlueprintReadOnly) | [Doku] |

**Lesart** [Ableitung]:
- Die Log-Zeile im Forum passt zu einem Niagara-System, das nur über die Projekteinstellungen verknüpft ist und deshalb nicht mitgekocht
  wird.
- Das ist eine Hypothese, kein Befund. T-a3 prüft sie.

**Offene Messfragen, die die Regel ändern:**
1. Was kostet BAKED_SIM an p2 **insgesamt**, also System **und** Zeichnen? Was kostet es aus 300 m Entfernung und bei abgewandtem Blick?
2. Zeichnet BAKED_SIM noch, wenn das Niagara-System der SWR aus ist? Dann ließe es sich nach Entfernung abschalten wie in 16b §2.2.
   Sonst kostet jede BAKED_SIM-Einheit, solange sie geladen ist.
3. Zeichnet BAKED_SIM im gepackten Development-Build?

### 1.2 (b) Regel §5.4 und der Weg, die WCBS-Fläche anzuheben

**Ersetzte Regel** (statt „höchstens 3 Schaustellen“):

| Fall | Nah sichtbar | Fern |
|---|---|---|
| T-b1 zeigt einen Hebel, der WCBS auf Sim-Höhe bringt | **WCBS überall** (Interaktion, Water-Zone-LOD) | WCBS |
| WCBS bleibt flach, BAKED_SIM zeichnet im Paket (T-a3) | **BAKED_SIM**, wo WCBS sichtbar versagt (Talkaskade, Becken, Stufen) | wie T-a2 Punkt 2: abschaltbar, dann aus bzw. WCBS; sonst fest BAKED_SIM |
| BAKED_SIM zeichnet im Paket nicht | WCBS plus der beste Hebel aus T-b1; BAKED_SIM nur als Editor-Vorschau | WCBS |

- **Budget:** Summe aus „BAKED_SIM-Mehrkosten × geladene BAKED_SIM-Einheiten“ und „3-Dispatch-Kosten × alle geladenen SWR“ ≤ 1,5 ms (Datei 16).
  Es gilt der Median aus T-a1, nicht 0,3 ms.
- **Unabhängig vom Render-State:** Die 3 Dispatches fallen auch in WCBS an. Der größte Hebel ist deshalb der SWR-Manager bzw. das Culling
  aus 16b §2.2. Die Wahl BAKED_SIM oder WCBS ist es nicht.
- **Kein Wechsel nach Entfernung**, solange T-c1 ihn im Spiel nicht erlaubt.
- **Schaum-Vorgabe beachten:** In 6i Test 0 zeigt BAKED_SIM „Schaum an Lippen“. Stammt er vom Gischt-Emitter, gilt die Entscheidung „kein
  Schaum im Bach außer an Fällen“. Dann den Emitter an Bach-SWR ausschalten (16b D8 a). Das spart zugleich einen Teil der 3 Dispatches.
  Lippen echter Fälle behalten die Nature-Water-FX.

**Warum WCBS flach bleibt: drei Hypothesen, ein Test (T-b1).**

Euer Befund aus Test 2: WCBS zeichnet eine sehr dünne Schicht, BAKED_SIM die volle Höhe.

- **H1, Fläche = Spline-Spiegel.** Das WCBS-Netz liegt auf der Höhe des Water Body, also auf dem Plan-Spiegel der Spline. Laut eurem §4
  liegt der gebackene Spiegel 0,15–0,25 m darüber.
  - Bett-Median 0,34 m − 0,15…0,25 m ergibt 9–19 cm Rest. Das passt zu „fast auf dem Boden“ [Rechnung].
  - Hebel: Spline-z je Punkt auf den gebackenen Spiegel heben. Das ändert aber den Eingang der Simulation (`match_spline_height_amount`
    0,02) und verlangt neues Backen [Ableitung].
- **H2, Fläche aus der Wasser-Info, Verschiebung gedämpft.** Das Netz wird über die Wasser-Info bzw. die Material-Verschiebung angehoben.
  Im Master stehen `Fluid Displacement Multiplier` 1 und `Max Fluid Displacement` 1024 [Projekt].
  - Hebel: Werte im MI, ohne neues Backen.
- **H3, direkter Weg über die gebackene Textur ist aus.** Im MI stehen `UseBakedSim` False und `BakedWaterSimSize` 0 [Projekt 16h, 6h].
  Test T3 aus 16h lief nie.
  - Hebel: der Schalter. Er wirkt nur, wenn die SWR `BakedWaterSimSize` im MID selbst setzt [offen].

**T-b1 (≈ 15 min, nur im Speicher):**
- Aufbau: Kamera m_talkaskade. Eine Messlatte (`/Engine/BasicShapes/Cube`, 5 × 5 × 150 cm, Striche alle 5 cm, Vorschlag aus 6h §1.1)
  senkrecht ins Hauptbecken stellen.
- Je Zustand die Spiegelhöhe ablesen, dazu `r.Water.WaterMesh.ShowWireframe 1` und `r.Water.WaterMesh.ShowWireframeAtBaseHeight 1` (CVars
  aus 14b [Drittquelle]; vorher mit der Konsolen-Vervollständigung prüfen, ob sie in 5.8.3 existieren).
- Zum Vergleich die Spline-z am Becken aus dem Export.

| Schritt | Zustand | Erwartung H1 | Erwartung H2 | Erwartung H3 |
|---|---|---|---|---|
| 1 | BAKED_SIM | Referenz z_sim | Referenz | Referenz |
| 2 | WCBS (heute) | z ≈ Spline-z (± 3 cm), Drahtgitter = Gitter auf Grundhöhe | z zwischen Boden und z_sim, Gitter ≠ Grundhöhe | wie H1 oder H2 |
| 3 | WCBS, `Fluid Displacement Multiplier` 2, dann 0 | keine Änderung | z ändert sich mit dem Wert | keine Änderung |
| 4 | WCBS, `UseBakedSim` True (Schalter, neu kompilieren) | keine Änderung | – | z bzw. Farbe nähern sich BAKED_SIM |

**Entscheidung nach T-b1:**
- **H2 bestätigt:** WCBS-Werte im MI anpassen, die Messlatte gegen BAKED_SIM halten. Ziel: |Δz| ≤ 3 cm im Becken. Dann WCBS für alle
  SWR, und BAKED_SIM entfällt.
- **H3 bestätigt:** wie H2, Schalter im MI gesetzt lassen. Die Vergleichsstelle C2 nach den Prüfregeln mitprüfen, denn das MI wird
  gemeinsam genutzt.
- **Nur H1:** Kein Spline-Umbau ohne eigenen Testgrund. BAKED_SIM bleibt an der Talkaskade. Die Spline-Anhebung wird ein eigener,
  später zu planender Versuch (neues Backen, Nähte, Spiegeltextur).

### 1.3 (c) `render_state` zur Laufzeit

| Weg | Stand |
|---|---|
| Python im Editor, `set_editor_property('render_state', …)` | geht [Ferat 6i Test 0: „Umschalten sofort“]; Python-Doku 5.5: `render_state` Read-Write [Doku] |
| Python in PIE (euer Test 5.3 mit `karte/pie_test.py`) | wahrscheinlich ja, weil auch dort die Editor-Benachrichtigungen laufen [Ableitung]. **Aussagekraft fürs Spiel: keine.** Python und Editor-Benachrichtigungen gibt es im gepackten Build nicht |
| Blueprint im Spiel | Von `UShallowWaterRiverComponent` ist nur `Set Paused` als Blueprint-Knoten dokumentiert (Kategorie „Shallow Water River“). `RenderState` ist öffentliche Variable, `UpdateRenderState()` ohne Blueprint-Kennung [Doku] |
| C++ (`RenderState` setzen + `UpdateRenderState()`) | wäre der Weg, aber Projekt-Quellcode ändern wir nicht (Entscheidung) |

**T-c1 (1 min, ohne Editor):**
- Im Engine-Ordner 5.8.3 die Datei `Engine/Plugins/Experimental/WaterAdvanced/Source/WaterAdvanced/Public/ShallowWaterRiverActor.h` öffnen
  (Pfad laut API-Seite [Doku]).
- Wörtlich kopieren: die `UPROPERTY(...)`-Zeile vor `RenderState` und die `UFUNCTION(...)`-Zeilen vor `Rebuild`, `UpdateRenderState` und
  `SetPaused`.
- **Entscheidung:**
  - Kein `BlueprintReadWrite`, kein `BlueprintSetter` und `UpdateRenderState` nicht `BlueprintCallable` → Render-State ist im Spiel
    fest. §1.2 gilt ohne Entfernungswechsel, T-c2 entfällt.
  - Sonst T-c2.

**T-c2 (5 min, nur falls T-c1 eine Blueprint-Freigabe zeigt):** Im Level-Blueprint per Taste `Render State` auf `Water Component with Baked
Sim` und zurück setzen. Ändert sich das Bild nicht, wird die Variable zwar gesetzt, aber nicht angewendet. Dann gilt dieselbe Entscheidung.

Python für euren PIE-Test. Er beantwortet nur die Editor-Frage und die Frage nach Ruckeln bzw. doppelter Fläche:

```python
import unreal
welt = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()   # PIE-Welt
swr = [a for a in unreal.GameplayStatics.get_all_actors_of_class(welt, unreal.ShallowWaterRiver)
       if 'ERLENBACH' in a.get_name()][0]
comp = swr.get_component_by_class(unreal.ShallowWaterRiverComponent)
RS = unreal.ShallowWaterRenderState
print(comp.get_editor_property('render_state'))
comp.set_editor_property('render_state', RS.WATER_COMPONENT_WITH_BAKED_SIM)   # danach zurueck auf RS.BAKED_SIM
# T-a2 Punkt 2: zeichnet BAKED_SIM ohne laufendes System?
nc = comp.get_editor_property('river_sim_system')   # NiagaraComponent, nur lesen (16a B1)
nc.deactivate()      # Bild ansehen; danach nc.activate(True)
```

Die Namen stammen aus 16a/16b und eurem 6i-Test. Nur `get_game_world` ist hier neu [Doku UnrealEditorSubsystem]; wenn es fehlt, wie in 16b
`EditorLevelLibrary.get_game_world()` nehmen.

### 1.4 Messplan zu (a): T-a1, T-a2, T-a3

Die Regeln für GPU-Zeit aus `vorlagen/pruefung.md` gelten: gleiche Szene, Hardware, Auflösung und Render-State; vergleichbar aufwärmen;
wiederholt messen; Streuung nennen.

**T-a1, Kosten an p2 (PIE, ≈ 20 min):**
- Feste Auflösung und Screen Percentage, VSync aus, gleiche Upscaler-Einstellung.
- Kameras: m_talkaskade (nah), ein Punkt 300 m entfernt mit Blick auf p2, derselbe Punkt mit abgewandtem Blick.
- Zustände: WCBS, BAKED_SIM, BAKED_SIM mit Gischt-Emitter aus (`nc.set_emitter_enable('SW_River_Secondary_Emitter', False)`, 16b D8).
- Je Kombination nach dem Umschalten 10 s warten, dann 5 × `ProfileGPU`.
- Notieren: `Grid2D_SW_River`, den Wasser-Pass (Single Layer Water bzw. Translucency) und die gesamte GPU-Bildzeit, jeweils Median und
  Spanne.
- Ein Unterschied innerhalb der Spanne gilt nicht als Gewinn.
- Gegenprobe ohne Wasser: SWR ausblenden, dieselbe Kamera.

**T-a2, Abschaltbarkeit (5 min):**
- Mit dem Python oben in BAKED_SIM das System ausschalten (`nc.deactivate()`).
- Erwartung A: Die Fläche bleibt. Dann ist BAKED_SIM nach Entfernung abschaltbar (Manager 16b), die Fernkosten fallen weg.
- Erwartung B: Die Fläche verschwindet. Dann kostet jede BAKED_SIM-Einheit, solange sie geladen ist.

**T-a3, gepackter Build (eigener Rahmen, lange Bauzeit):**
- Kleinster Fall: Im vorhandenen Wasser-Testlevel einen kurzen Bach backen; eine SWR auf BAKED_SIM, eine auf WCBS. Development-Build
  packen, nur diese Karte.
- Abbruchbedingung: Der Kochvorgang scheitert am Wasser-Plugin. Dann Log sichern und nicht weiterprobieren.
- Prüfen:
  1. Zeichnet die Fläche ja oder nein, je SWR?
  2. Stehen die Forum-Zeilen „Ocean simulation system not loaded“ oder „ocean patch normal RT is not initialized“ im Log?
  3. `stat gpu` gegen T-a1.
- **Falls nichts zeichnet und die Log-Zeile kommt:** einmal den Inhaltsordner der WaterAdvanced-Niagara-Systeme unter Project Settings →
  Packaging → „Additional Asset Directories to Cook“ eintragen und neu packen. Das ist eine Hypothese [Ableitung]; ob Plugin-Pfade dort
  angenommen werden, lokal prüfen.
- Danach den Befund einmal an p2 im vollen Build bestätigen (Streaming, World Partition).

## 2. §3 Flusskopien – erledigt durch 6j §1

Der Versuch „Variante C light“ ist verworfen: Die Front stand bei T00 still, und die Nähte waren trocken. Exporter und Prüfer sperren
Teilungspläne seit 15.10. Vom Befund 6i §3 bleibt dreierlei [Ferat, Ableitung]:

1. **Die Rechenfläche ist nicht einstellbar.** `WorldGridSize`/`SystemPos` sind privat und werden in `Rebuild()` aus den
   Quell-Wasserkörpern berechnet.
   - Für eine ganze SWR ist `resolution_max_axis` deshalb der **einzige** Hebel für die Zellgröße. Er wirkt auf die lange Achse.
   - p2 (740 m) hat bei 2048 Zellen rund 0,36–0,37 m je Zelle. Feiner geht es nur, wenn die Engine mehr als 2048 zulässt. Das ist nicht
     belegt; an C2 kostete 2048 live schon 9,7 ms (16c), und das Einlaufen dauert lange.
2. **Das Modell ist bestätigt.** Eure Nachrechnung ergibt 116,9 × 741,6 m gegen 116,8 × 739,9 m im Dump.
   - Damit kann `rechteck_m` im Export für die 188 ungeteilten Gewässer als Vorhersage der echten Rechenfläche dienen. Das gilt nicht als
     Unreal-Nachweis.
   - Je Gewässer genügt ein Bounds-Vergleich nach dem Bau.
3. **Mäander blähen das Rechteck auf.** Die Zellgröße hängt an der Hülle der Spline, nicht an der Lauflänge.
   - Eine feinere Uferstufe erreicht man an der ganzen SWR nur über das Bett: Boden-Trick, schmaleres Band oder Bettgeometrie (6g §2).
   - Die Fragen dazu, auch zu Variante A, beantwortet die getrennte Antwort zu 6j.

## 3. §4 Nasslinien-Material für Mountain-, Fab- und Namaqualand-Netze

### 3.1 Entscheidung

| Paket | Master | Begründung |
|---|---|---|
| **Mountain** (`M_Master_material`-Kinder: `MI_mountain_rocks_big_01`, `MI_mountain_rocks_atlas_01/_02`, `MI_rocks_atlas_01`, `MI_Flat_rock_01`, `MI_Big_rock_03`, `MI_mountain_rocks_small_01` [Projekt Inventar]) | **neu: `M_EL_Mountain_NL`** (anzulegen) = Kopie von `/Game/Mountain_Environment_Set/Master_Materials/M_Master_material` nach `/Game/Eldarien/Welt/Material/Fels/`, plus `MF_EL_Spiegelhoehe` und `MF_EL_Nasslinie` vor BaseColor und Roughness, genau wie MSR → MS2 | Die Mountain-Texturen sind gepackt (z. B. `T_Flat_rock_01_tiled_BC_H`, BaseColor + Höhe im Alpha [Projekt stein_albedo]). Der Master hat eigene Regler (`Base Brightness`, `Normal Power`, `Detail *`, `Specular Value`, RVT-Blend; 6d). Eine MS2-Kopie je MI müsste Kanäle umbelegen und verlöre Detail und RVT-Blend. Die Kopie behält alle Parameternamen, also werden die Kinder reine Wertkopien ohne Belegungsrisiko |
| **Fab Raw** (`skjsL`, `texndcpda`, `xjijbgx`, `pjcxN`, `pkeeM` …; Texturen `_B`, `_N`, `_ORM` 8K [Projekt Inventar]) | **vorhanden: `M_EL_Fels_MS2`**, je Netz `MI_EL_<id>` (anzulegen) | MS2 hat die Nasslinie schon. Eure Regel „jedes Fab-Raw-Netz braucht ein MI_EL“ (6j Nachtrag 09:00) wird damit gleich erfüllt. Kein zweiter Master |
| **Namaqualand** (`MI_Namaqualand_Boulders_01`, `_Rocks_01`, `_Stones_01` [Projekt Inventar]) | **vorhanden: `M_EL_Fels_MS2`**, `MI_EL_NL_namaqualand_<boulders/rocks/stones>_01` (anzulegen) mit den Namaqualand-Texturen | Die Netze sind grauer Granit (Auftrag 20); „grau“ heißt hier nur: neutrale `Toenung` statt der Wüstentönung |

**Pflichtprüfung vor dem Bau der Fab- und Namaqualand-MIs (5 min, im Graph von `M_EL_Fels_MSR`):**
- Welcher Kanal von `AoRT` speist AO, welcher Rauheit, welcher `Durchscheinen`?
- Fab `ORM` ist R = AO, G = Rauheit, B = Metallic.
  - **Liest MS2 R = AO und G = Rauheit:** ORM direkt in `AoRT` und `Durchscheinen` = 0, denn B ist dann Metallic, für Fels ≈ 0.
  - **Sonst:** Fab und Namaqualand ebenfalls auf eine Kopie mit Nasslinie, und zwar von `M_EL_Klippe_RVT`. Er liest Albedo/Normal/ORM schon
    (`MI_EL_Klippe_ukjhcamga`, 6j). Name `M_EL_Klippe_NL` (anzulegen).
  - MS2 selbst nicht umbauen. Er versorgt mehr als 120 Instanzen.
- Namaqualand: zuerst die Texturbelegung der Paket-MIs auslesen. Nicht raten.

**Nie doppelt abdunkeln** (6d):
- MS2 hat die alte Nässe unter dem Objekt-Ursprung (`Nass_Dunkel`, `Nass_Weich`; 6e §6). Für die neuen Fab- und Namaqualand-MIs auf neutral
  stellen.
- Ob neutral 1 oder 0 heißt, zeigt der Graph [offen].
- Mountain-Netze nicht mehr über die `_Nass`-Typen setzen; `MI_EL_Nass_mountain_rocks_small_01` entfällt dort.

### 3.2 Parameterliste `M_EL_Mountain_NL` (und Ergänzung der Nasslinien-Master)

Die Parameter des Paketmasters bleiben unverändert und gehen mit den Werten des jeweiligen Paket-MI 1:1 ins Kind. Neu ist nur die Gruppe
„Nasslinie“. Die Namen sind wie bei MS2, damit `ue_fels_nasslinie.py` (werte/umhaengen/zurueck) ohne Sonderfall für beide Master läuft:

| Parameter | Typ | Standard | Talkaskade p2 | Herkunft |
|---|---|---|---|---|
| `Nass_Albedo` | Skalar | 0,50 | je MI: clamp(0,08 / Y_trocken; 0,35; 0,65) | Zielhelligkeit Y 0,08 [6d] |
| `Nass_Entsaettigung` | Skalar | 0,3 | 0,3 | MS2 [6e] |
| `Nass_Rauheit_Linie` | Skalar | 0,20 | 0,20 | MS2-Name [6e §6] |
| `Nass_Voll_cm` | Skalar | 8 | **12** | Spritzzone [20 §5] |
| `Nass_Rand_cm` | Skalar | 20 | **30** | Spritzzone [20 §5] |
| **`Nass_Spiegel_Versatz_cm`** | Skalar, **anzulegen** | **0** | **+20** (vorläufig, Mitte von 15–25 cm) | gebackener Spiegel über Plan-Spiegel [Ferat 6i §4] |

**`Nass_Albedo` je Mountain-MI** aus `stein_albedo.json` [Projekt, Rechnung]:

| MI | Y trocken | Wert |
|---|---|---|
| `MI_mountain_rocks_small_01` | 0,229 | 0,35 |
| `MI_mountain_rocks_atlas_01` | 0,204 | 0,39 |
| `MI_rocks_atlas_01` | 0,177 | 0,45 |
| `MI_Flat_rock_01` | 0,164 | 0,49 |

- `MI_mountain_rocks_big_01`, `_atlas_02`, `MI_Big_rock_03`, Fab und Namaqualand: Y nicht gemessen. Mit dem Verfahren von
  `stein_albedo.json` messen, dann dieselbe Formel. Bis dahin 0,50.

**Knoten für den Versatz:** In `MF_EL_Nasslinie` `h = WorldPosition.Z − (Spiegel + Nass_Spiegel_Versatz_cm)`, 2 Anweisungen.
- Der Standard 0 lässt alle vorhandenen MS2-Kinder unverändert.
- Weil die Funktion gemeinsam genutzt wird: eine MS2-Vergleichsstelle (C2 bzw. t430, `MI_EL_SmallStonesPack_01`) vorher und nachher mit
  derselben Kamera prüfen. Erwartet: kein Unterschied.
- Richtig wäre langfristig, `T_Eldarien_Wasserspiegel_2m` aus dem gebackenen Spiegel neu zu erzeugen. Das trifft aber auch die Nässe der
  Landschaft und ist ein eigener Schritt.

**Bau** (Reihenfolge, Werkzeug = euer `ue_fels_nasslinie.py`, das MSR → MS2 schon gebaut hat):
1. `unreal.EditorAssetLibrary.duplicate_asset(<M_Master_material>, '/Game/Eldarien/Welt/Material/Fels/M_EL_Mountain_NL')`.
   Das Paket-Asset bleibt unberührt.
2. Die Funktionen einhängen wie bei MS2 (`ue_fels_nasslinie.py bauen`, Ziel umgestellt). Danach 0 Kompilierfehler, Stats vorher und
   nachher. Erwartet etwa +27 Anweisungen und +1 Sampler wie bei MS2.
3. Bei Sampler-Grenze: die Spiegeltextur auf „Shared: Wrap“ stellen.
4. Je Paket-MI ein Kind `MI_EL_NL_<Paket-MI>` mit Eltern `M_EL_Mountain_NL`. Alle Skalar-, Vektor-, Textur- und Schalterwerte des Paket-MI
   übernehmen, z. B. über `unreal.MaterialEditingLibrary.get_scalar_parameter_names` und
   `set_material_instance_scalar_parameter_value`.
5. Ob es für statische Schalter einen Python-Setzer gibt, mit `hasattr` prüfen; sonst die Schalter von Hand übernehmen.
6. Die Nasslinien-Werte aus der Tabelle setzen.

**Abnahme an der Talkaskade:**
- Formal: 0 Kompilierfehler, die Paket-MIs bleiben unverändert, und `MI_EL_NL_*` ohne Nasslinie (`Nass_Albedo` 1) sieht aus wie das
  Paket-MI. Kamera t430, Differenzbild.
- Bild: In BAKED_SIM endet der dunkle Streifen bei ≥ 80 % der Steine im Wasser 8–30 cm über der **sichtbaren** Wasserlinie (Ziel aus 20 §5).
  - Liegt er unter Wasser, `Nass_Spiegel_Versatz_cm` in 5-cm-Schritten nachstellen.
  - Zieht er über 40 cm hoch, zurücknehmen.

## 4. §6 Breitenprofil: Auslauf nach dem Anfangsbereich

### 4.1 Befund [Rechnung, 2-m-Daten im Repo]

- Heute gilt nach `s = L` die Original-Breite (`profil()` und Aufrufer in `bach_anfaenge_plan.py`).
- Die Houdini-Breiten schwanken stark. Bei B_R2_R_P3_P1_05 sind es 8,0 / 4,0 / 2,8 / 4,0 / 2,0 / 2,0 m auf 37 m.
- Am Übergang springt die Breite deshalb oft. Der Sprung liegt auf einem Segment von 5–10 m, also bei 0,17–0,48 m/m.
- Prüfskript (Scratch, nicht im Repo) über alle 148 Anfänge mit Folgepunkt:

| Gewässer | Ende Profil → nächster Punkt | Faktor | B / b0 / L |
|---|---|---|---|
| B_R2_R_M3_P1_01 (Abzweig) | 1,83 → 4,00 m | ×2,19 | 2,0 / 1,2 / 20 |
| B_R_P3_P0_05 | 3,69 → 8,00 m | ×2,17 | 4,0 / 0,4 / 44 |
| **B_R2_R_P3_P1_05** | **1,89 → 4,00 m** | ×2,11 | 2,0 / 0,4 / 30 |
| B_R_P4_M1_03 | 3,01 → 6,00 m | ×1,99 | 4,0 / 0,4 / 30 |
| B_R2_R_P4_M2_01 | 2,83 → 4,83 m | ×1,71 | 4,41 / 0,4 / 30 |
| B_R2_R_P3_P0_02 | 2,38 → 4,00 m | ×1,68 | 2,83 / 0,4 / 38 |
| B_R3_R_P2_M1_01 | 2,08 → 3,22 m | ×1,54 | 2,28 / 0,4 / 31 |
| B_R2_R_M2_M2_01 (Abzweig) | 3,68 → 5,66 m | ×1,54 | 4,0 / 2,4 / 20 |
| B_R_M2_P1_02 | 3,75 → 5,66 m | ×1,51 | 4,0 / 0,4 / 32 |

Das sind genau eure 9 Fälle (×1,5–2,2). Die Steigung, die die Regel am Ende des Anfangsbereichs selbst erzeugt (0,8·(B−b0)/L), liegt über
alle Anfänge bei Median 0,080, p90 0,103 und höchstens 0,184 m/m.

### 4.2 Regel

- **Steigungsbegrenzer** ab dem letzten Profilpunkt:
  `b_i = min(b_orig,i ; b_i−1 + g · Δs_i)`, mit `g = max(0,10 m/m ; 0,8 · (B − b0) / L)`.
- Er läuft bis zum ersten Punkt mit `b_orig,i ≤ b_i−1 + g · Δs_i`. Ab dort gilt wieder das Original.
- Er endet vorzeitig an einem Zufluss- oder Fallpunkt (`zufluesse[].s_m`, `abstuerze` im fluss_sim-Export). Dort ist ein Sprung echt.
- **0,10 m/m** heißt: höchstens 1 m Verbreiterung je 10 m. Das liegt etwa beim p90 der Profilsteigung bei L. Der Auslauf ist also nie
  steiler als das Ende des Profils selbst [Gestaltung, Ableitung aus der hydraulischen Geometrie in 19: Breite wächst stetig mit dem
  Einzugsgebiet].
- **Tiefe** im Auslauf: `tiefe_von(W, b_i, t_orig)` wie im Anfangsbereich. **Tempo**: Original.
- **Ergebnis** (2-m-Daten):
  - B_R2_R_P3_P1_05: 1,89 → **2,37** (statt 4,00) → 2,83 m (Original), Auslauf 14 m.
  - Alle Fälle: 35 Anfänge mit 40 geänderten Punkten, längster Auslauf 29 m (B_R2_R_P4_M2_01: 2,83 → 3,95 → 4,93 → 4,83).
  - Davon 16 Änderungen > 0,5 m.
  - Neue Zwischenpunkte braucht es nicht. Der Begrenzer an den vorhandenen Punkten deckelt auch die Steigung zwischen ihnen.
- **Neu backen:** B_R2_R_M3_P1_01 und B_R2_R_M2_M2_01 (beide Abzweig) sowie B_R_P1_M2_03 (×1,44) stehen nicht in `neu_backen`.
  Sie kommen durch die geänderte Spline dazu.

### 4.3 Vorgeschlagene Code-Änderung

Nicht im Repo angewandt; Ferat oder der Planerbesitzer übernehmen.
- In `bach_anfaenge_regeln.json` unter `anfang` ergänzen: `"auslauf_steigung_m_je_m": 0.10`.
- Im Planer zwei Stellen ändern:

```python
def auslauf_g(W, B, b0, L):
    A = W.R["anfang"]
    return max(A.get("auslauf_steigung_m_je_m", 0.10), A["exponent_breite"] * (B - b0) / L)

# verjuengung_alle(): statt "if s[i] >= L: break"
        g = auslauf_g(W, B, b0, L)
        b_vor = None
        for i, p in enumerate(alt):
            b_orig = p[3] / 100
            if s[i] < L:
                b = max(min(profil(W, s[i], L, b0, B), b_orig), min(b0, b_orig))
                v = tempo_von(W, s[i], L, p[5])
            else:
                grenze = b_vor + g * (s[i] - s[i - 1])
                if b_orig <= grenze:          # Original unter der Rampe: Auslauf zu Ende
                    break
                b, v = grenze, p[5]
            pts.append([i, r(b * 100), r(tiefe_von(W, b, p[4] / 100, ist_fluss) * 100), r(v)])
            b_vor = b

# kopf_bauen(): nach der Schleife ueber alt[0..k-1] mit b_vor = letzte Kopfbreite (m)
    g = auslauf_g(W, B, b0, L)
    while k < len(alt):
        ds = (s_alt[k] - s_alt[k - 1])
        grenze = b_vor + g * ds
        if alt[k][3] / 100.0 <= grenze:
            break
        p = alt[k]
        kopf.append([p[0], p[1], p[2], grenze * 100.0, tiefe_von(W, grenze, p[4] / 100.0, ist_fluss) * 100.0, p[5]])
        b_vor, k = grenze, k + 1
    return kopf, k                            # alt_bis_index_exkl rueckt mit
```

- Der Abbruch an Zufluss- und Fallpunkten fehlt im Ausschnitt. Er braucht die s-Werte aus dem fluss_sim-Export, die der Planer schon liest
  (`vorschlaege.json`).
- **Prüfer P4 ergänzen:** Ab `s = L` bis zum Fangpunkt gilt `(b_i − b_i−1)/Δs ≤ g + 0,005`, sonst FEHLER. Dazu eine WARNUNG für jeden
  Sprung ≥ ×1,5 in den ersten L + 30 m.
- **Gegenprobe:** heutigen Stand mit ausgeschaltetem Begrenzer laufen lassen. Erwartet: genau diese 9 WARNUNGEN.
- Außerhalb dieses Schritts: Die Houdini-Schwankung **hinter** dem Fangpunkt bleibt, z. B. 2,83 → 4,00 → 2,00 m. Ein Glätten des ganzen
  Laufs ändert Bett und SWR. Das ist eine eigene Entscheidung und kommt erst, wenn es im Bild stört.

## 5. Zu §2, §4 und §5: Kenntnisnahme und geschlossene Rückfragen

- **§2 Band nass:**
  - Eure Zahlen widerlegen unsere 6g-Erwartung (20–30 % bei > 5 cm). Es ist echtes Wasser neben dem Bett.
  - Folge für die Nasslinie: 46 % der Instanzmitten liegen unter dem gebackenen Spiegel. Deshalb der Versatz-Parameter in §3.
  - Die Ursache und der nächste Schritt gehören zu 6j.
- **§4 z-Korrektur:** Unsere z lagen an Böschungen bis 1,23 m daneben, weil wir das Delta der nächsten Zelle statt der Ist-Höhe nahmen. Das
  war unser Fehler. Eure neu gerechnete z gilt.
- **§4 Rückfrage 1 (Slab-Achsen und Pivot):** geschlossen. Die Konvention passt; den Slab-Versatz von 1,55 m × Skala entlang +Y übernimmt
  der Setzer.
- **§4 Rückfrage 2 (volle Dichte nur Talkaskade):** geschlossen.
- **§4 Rückfrage 3 (keine `MI_EL_NL_*`):** beantwortet durch §3.
- **§4 Rückfrage 4 (Unterordner):** geschlossen, nicht nötig.
- **§4 Bewuchs nach korrigiertem Bake:** einverstanden. Steine jetzt, Bewuchs (20 §5 Schritt 6) danach.
- **§5 Rückfrage 3 (Gras über `v_*.r8`):** geschlossen. Die Grasdichte-Maske wird Faktor auf `v_gras_berg`/`v_kraut`/`v_heide`.
- **§5 Rückfrage 2 (`remove_foliage_by_mask` ohne Sicherung):** geschlossen. Euer eigenes Skript mit Sicherung je Instanz gilt.
- **§5 Rückfragen 5 und 8:** geschlossen.
- **§5 Rückfrage 1 (Pivot der Bandnetze an −Y):** wartet auf eure K3-Prüfung.
- **§5 Raw-8K → 4K klemmen:** einverstanden.

## Was fehlt bis Witcher 4

Messlatte ist die UE5-Techdemo, belegt wie in 6e nur über Suchauszüge: Wasser mit Körper und Farbe, nasse, dunkle Steine an der Linie,
Bewuchs bis ans Wasser, weiches Licht. Nach Wirkung sortiert:

1. **Wasser mit Körper auch im Spiel.**
   - BAKED_SIM zeigt es im Editor. Für das Spiel fehlen der gepackte Build (T-a3) und die echten Kosten an p2 (T-a1/T-a2).
   - Alternativ die WCBS-Anhebung (T-b1).
   - Ohne einen dieser Nachweise ist der wichtigste Bildgewinn der letzten Tage nicht spielfest.
2. **Wasser im Bett:** Das Band ist bei > 10 cm zu 46 % nass. Feine Zellen helfen (6j: 13 %), die Teilung aber reißt den Bach auf. Der
   Weg kommt aus 6j über Bett und Boden, nicht über mehr SWR.
3. **Nasse Steine an der sichtbaren Linie:** `M_EL_Mountain_NL`, die MS2-MIs für Fab und Namaqualand und der Versatz an den gebackenen
   Spiegel (§3). Erst damit lesen sich Fußsteine und Lippen als nass.
4. **Kein Schaum außer an Fällen, auch in BAKED_SIM:** Gischt-Emitter an Bach-SWR prüfen bzw. ausschalten (§1.2).
5. **Bewuchs an der Kante** nach dem korrigierten Bake (20 §5 Schritt 6, 6e).
6. **Weiche Bachanfänge:** Auslaufregel (§4) und die Frage aus 6j zum unsichtbaren 0,4-m-Rinnsal (wird dort beantwortet).
7. **Fernwirkung:** Die „Wasserwand“ in der Ferne [Forum] und Water-Zone-LOD erst nach T-a2 bewerten.

## Rückfragen

Nur eine, sie ändert den nächsten Schritt:
1. Gibt es im Projekt ein kleines Wasser-Testlevel mit gebackener SWR, das sich allein packen lässt? Falls nicht, startet T-a3 mit dem
   Anlegen und Backen eines kurzen Bachs. Das verlängert den Rahmen um die Backzeit.

## Quellen

Abgerufen am 18.10.2026. Alle nur als Suchauszug gelesen; ein Direktabruf war nicht möglich (DNS bzw. Proxy 403).

- [API: UShallowWaterRiverComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent?lang=en-US)
  – öffentliche Variable `RenderState` (`TEnumAsByte<EShallowWaterRenderState>`), Funktionen `Rebuild`, `UpdateRenderState`, `SetPaused`
  (nur diese BlueprintCallable, Category „Shallow Water River“); Header `ShallowWaterRiverActor.h`. Versionsbezug der Seite nicht erkennbar.
- [API: EShallowWaterRenderState](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/EShallowWaterRenderState?lang=en-US)
  – sechs Werte (WaterComponent, WaterComponentWithBakedSim, LiveSim, BakedSim, DebugRenderBottomContour, DebugRenderFoam).
- [Blueprint API: Set Paused](https://dev.epicgames.com/documentation/unreal-engine/BlueprintAPI/ShallowWaterRiver/SetPaused?lang=en-US)
  – einziger dokumentierter Blueprint-Knoten der SWR-Komponente in der Suche.
- [Python 5.5: unreal.ShallowWaterRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent?application_version=5.5)
  – `render_state` Read-Write (Editor-Python).
- [Python: PropertyAccessChangeNotifyMode](https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/PropertyAccessChangeNotifyMode.html)
  – `set_editor_property` löst Änderungsbenachrichtigungen aus (DEFAULT/ALWAYS/NEVER); Grundlage für „Editor/PIE ja, Paket nein“
  [Ableitung].
- [API: UShallowWaterSettings](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterSettings?lang=en-US)
  – `DefaultOceanPatchNiagaraSystem` (EditAnywhere, BlueprintReadOnly).
- [Forum: Shallow Water Body (Advanced Water Plugin) Fails To Render](https://forums.unrealengine.com/t/shallow-water-body-advanced-water-plugin-fails-to-render/2634176)
  – gepackter Build zeichnet nicht, Log-Zeilen wie oben; Lösung nicht im Auszug.
- [Forum: Water Component with Baked Sim not rendering](https://forums.unrealengine.com/t/shallow-body-river-water-component-with-baked-sim-not-rendering/2688228)
  – WCBS nur Schaum.
- [Forum: ShallowWaterRiver and Landscape](https://forums.unrealengine.com/t/shallowwaterriver-and-landscape/2818892) – „Wasserwand“ in
  der Ferne bei gebackenem Zustand.
- [Forum: ShallowWaterRiver – Lake/Ocean (5.7/5.8)](https://forums.unrealengine.com/t/shallowwaterriver-lake-ocean/2838534) – wie in 6h:
  Live und Baked Sim zeigen korrekt, die SWR baut ihre Fläche anders als der Water Body.
- [Tutorial: Baked River Simulations – Parameter Reference](https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference)
  – Leitfaden aus 16a; Inhalt diesmal nicht erneut lesbar.
- Projekt: `auftraege/16b-swr-c2-ganze-strecke.md` (Kostentabelle), `antworten/16a-swr-einrichtungstest-teil1.md` §a3/B1,
  `antworten/14b-befund-geteilte-baeche.md` (Water-Mesh-CVars), `antworten/fluss_sim/p2_lokal/stein_albedo.json`,
  `antworten/bach_anfaenge/bach_anfaenge_plan.json`, `vorlagen/daten/inventar*.json`.

**Nicht erreichbar bzw. nicht belegt:**
- Volltext der Epic-API- und Python-Seiten 5.6–5.8.
- Spätere Antworten in den Forenthreads, falls es dort eine Lösung für den gepackten Build gibt.
- Ein offizieller Beleg zu den Kosten von BAKED_SIM oder zu seinem Verhalten im gepackten Build. T-c1 und T-a3 schließen diese Lücken
  lokal.
