# Auftrag 16a – Einrichtungstest Shallow Water River, Teil 1 (C2 Version 3)

Stand 12.10.2026, 14:20. C2 ist als Version 3 gebaut (euer Plan `0e00d17`, noch mit Kaskadennetz). Test T1 im Abschnitt s 99–139 m um `kn0_nah_s119`:
eigener `WaterBodyRiver` entlang eurer Mittellinie (19 Punkte, Breite 18–26 m, Spiegel 70,1 → 55,6 m), dazu ein `AShallowWaterRiver`, Kaskadennetz für
den Test ausgeblendet. Nichts gespeichert. Bilder: [`bilder/swr/t1_c2_netz_gegen_swr.jpg`](../bilder/swr/t1_c2_netz_gegen_swr.jpg) (links Netz, rechts
Simulation; außerhalb von T1 ist das Bett im Test trocken), [`bilder/swr/t1_fels_kollision.jpg`](../bilder/swr/t1_fels_kollision.jpg) (Becken von oben).

## Ergebnisse

1. **Läuft in UE 5.8.3.** Plugins Water, NiagaraFluids, WaterAdvanced waren im Projekt schon an. Klasse `AShallowWaterRiver`, Komponente
   `UShallowWaterRiverComponent`, Standard-Simulation `/WaterAdvanced/Niagara/Systems/Grid2D_SW_River`. Per Python sind alle Eigenschaften setzbar
   (`resolution_max_axis`, `source_river_water_bodies`, `sink_river_water_bodies`, `render_state`, `bottom_contour_landscape_actors`,
   `bottom_contour_actors`, `bottom_contour_tags`, `match_spline`, `sim_speed`, `num_steps` …). „Reset“ und „Bake“ gibt es nur als Knöpfe im
   Details-Fenster; die C++-Funktionen `Rebuild()`/`Bake()` sind exportiert, aber nicht für Python freigegeben → wir rufen sie über unser eigenes Plugin
   auf (geplant). Das Ändern einer Eigenschaft startet die Simulation neu.
2. **Becken und Lippen:** Die Simulation füllt das Becken, fließt über die Lippe und um die Felsnase, an der Stufe entsteht Wildwasser mit Strudeln.
3. **Kosten:** Raster 186 × 256 Zellen bei `resolution_max_axis` 256 (≈ 0,16 m), GPU ≈ 0,3–0,6 ms (ProfileGPU, Summe der `Grid2D_SW_River`-
   Dispatches; ganzes Bild im Editor 11,9 ms). Für den Nahbereich tragbar; alle Strecken gleichzeitig live nicht.
4. **Fels-Kollision:** Ein großer Fels (8,7 m breit, 1 m über dem Wasser) wird **nur mit Eintrag** erkannt: Etikett in `bottom_contour_tags` und
   Akteur in `bottom_contour_actors` (beides gesetzt). Die Debug-Ansicht `DEBUG_RENDER_BOTTOM_CONTOUR` zeigt ihn dann als Hindernis; das Wasser teilt
   sich und zieht eine Schaumspur. Ohne Eintrag ignoriert die Simulation ihn. Getestet mit einem einzelnen StaticMeshActor. Foliage/ISM ist ungetestet;
   ein Etikett am Foliage-Akteur würde vermutlich alle seine Instanzen erfassen (auch Gras) → **Steine im Wasser bitte als Akteure planen** (oder eine
   eigene Instanz-Gruppe je Fluss), Feld `wasser_kollision: true` wie in 16 beschrieben.
5. **Material:** Die Simulation zeichnet mit `/WaterAdvanced/Niagara/Materials/SW_Water_Material_River` (Eltern `SW_Water_Material`; Spline-Fassung
   `SW_Water_Material_River_Spline`). Werte dort: Absorption 20,8/25/24,7, Scattering 0,77/1,0/0,92 (A 0,5), Albedo 0,083, Schaum-Grundfarbe grünlich
   → hell-türkis, marmoriert. Unser `MI_Eldarien_Wasser_Fluss` (Master `M_Eldarien_Wasser_Schaum8`) hat dieselbe Parameterfamilie inklusive
   Fluidsim-Parametern. Lokal als Nächstes: `MI_EL_SWR_Fluss` als Kind von `SW_Water_Material_River` mit unseren Klar-Werten.
6. **Fälle:** Eine 2D-Höhe kann keinen Vorhang zeigen; Vorhang + Niagara + Schaumobjekte bleiben wie in 16 vorgesehen. Schwelle noch offen.

## Fragen an euch

a) **Einbacken:** Was speichert „Bake“ genau (`BakedWaterSurfaceTexture`, `BakedFoamTexture`, `BakedWaterSurfaceNormalTexture`, virtuelle Texturen)?
   Speicher je 100 m Fluss? Welcher `render_state` im Spiel (`BAKED_SIM` oder `WATER_COMPONENT_WITH_BAKED_SIM`)? Geht „live nahe beim Spieler, gebacken
   in der Ferne“?
b) **Material:** Welche Parameter in `SW_Water_Material` steuern Weißwasser und Schaum, damit klares Bergbachwasser entsteht und weißer Schaum nur an
   Stufen und Hindernissen?
c) **Größe:** Grenzen für `resolution_max_axis` und Fläche; ein `AShallowWaterRiver` je Fluss oder je Abschnitt zwischen den Fällen?
d) **ISM/Foliage als Hindernis:** Gibt es Erfahrungen, ob die Bodenerfassung Instanzen einzeln erfassen kann?

## Nachtrag 15:05 – Material: das Marmormuster kommt nicht aus den Wasserfarben

- `MI_EL_SWR_Fluss` (Kind von `SW_Water_Material_River`, unsere Absorption/Streuung, Schaum neutral) als `baked_sim_material` + `spline_river_material`:
  kaum Unterschied ([`bilder/swr/t1_material_epic_gegen_eigen.jpg`](../bilder/swr/t1_material_epic_gegen_eigen.jpg)).
- In LIVE_SIM zeichnet der Fluss mit seinem eigenen Wassermaterial (`MI_Eldarien_Wasser_Fluss`, Master `M_Eldarien_Wasser_Schaum8`, dieselbe
  Parameterfamilie inkl. „Fluidsim …“/„Sim Foam …“). Drei Varianten mit ruhigeren Werten (`Sim Velocity Normal Strength` 40 → 10 → 3,
  `Fluidsim Normal Strength` 1 → 0,5 → 0,25, `WPO Flowmap` 6 → 3 → 1,5, `Foam Opacity` 0,45 → 0,25/0,3, `Sim Foam Scale` 350 → 700):
  **praktisch identisch** ([`bilder/swr/t1_material_varianten.jpg`](../bilder/swr/t1_material_varianten.jpg)).
- Vermutung: Das hell-türkis-weiße Marmormuster entsteht in der Darstellung der Simulation selbst (Sekundär-Emitter `SW_River_Secondary_Emitter`
  mit 50 000 Teilchen, `M_SW_Foam`, Simulations-Normalen) oder im Wasser-Info-Pfad, nicht in den Material-Parametern, die wir geändert haben.
- **Bitte gezielt recherchieren:** Welche Einstellungen an `AShallowWaterRiver`/`Grid2D_SW_River` (Emitter-Parameter, Benutzerparameter des
  Niagara-Systems) und welche Material-Parameter steuern das Aussehen in LIVE_SIM bzw. BAKED_SIM? Gibt es Beispiel-Szenen von Epic (5.6/5.7) mit
  klarem Bachwasser, und welche Werte nutzen sie? Ferats Video bitte einbeziehen, sobald er Titel/Kanal nennt.
