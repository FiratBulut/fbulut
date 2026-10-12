# SWR-Parameter laut Epic (lokal gelesen 12.10.2026, 23:40)

Quelle: Epic-Tutorial „Baked River Simulations – Parameter Reference“ (Devon Penney, 15.05.2025, aktualisiert 17.06.2025),
https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference
(aus der Cloud gesperrt, lokal lesbar). Eigene Zusammenfassung, kein Wortlaut.

## ShallowWaterRiver-Akteur (Python-Namen in Klammern)

| Feld | Bedeutung laut Epic | Folge für Eldarien |
|---|---|---|
| Match Spline (`match_spline`, bool) | schaltet den künstlichen Abgleich der Simulation an die Spline ein/aus; kann unrealistisches Verhalten erzeugen | an lassen, nur wegen des Überlauf-Schutzes |
| Match Spline Height Amount (`match_spline_height_amount`) | Rate, mit der Wasser nachgefüllt wird, wo die Simulation unter der Spline-Höhe liegt (Niagara „Add Water To Match Spline Rate“); für Flüsse, die Volumen verlieren | **bei uns 2 → füllt das ganze Band bis zum Spline-Spiegel = Ursache „Wasser passt nicht zum Becken“**. Neu 0 … 0,05 |
| Remove Outside Spline Amount (`remove_outside_spline_amount`) | Rate, mit der Wasser außerhalb der Spline entfernt wird (Niagara „Remove Water Outside Spline Rate“) | 50 lassen (Netz gegen Überlaufen) |
| Source Width (`source_size`) | Größe des Bereichs, aus dem an der Quelle Wasser austritt; „Standard meist gut“ | Test 300 / 1000 cm (Bach 3 m breit) |
| Resolution Max Axis | Zellen auf der längsten Achse; „so hoch wie das Budget erlaubt, ideal ≥ 1024“ | C2 bisher 512 → 1024 prüfen |
| Speed / Num Substeps | Tempo-Multiplikator zum schnelleren Einschwingen; Substeps ≥ Speed | wie bisher 10/10 |
| Smoothing Width / Cutoff | Glättung der Oberflächen-Verschiebung bei harten Kanten | bei Treppen-Artefakten erhöhen |
| Use Capture, Bottom Contour Actors/Tags, Capture Offset | Hindernisse per Szenen-Capture als Tiefenkarte | Steine ≥ 0,4 m eintragen |
| Dilated Bottom Contour Actors/Tags + Collision Dilation | Hindernisse vergrößern, wenn Wasser durch Geometrie läuft | bei Durchlaufen erhöhen |
| Reset / Bake | Reset = neu aufbauen + Live Sim; Bake = in Textur backen, danach Render-Zustand auf gebacken | nach jeder Gelände-/Kollisionsänderung Reset |
| Render State | Water Component (ohne Sim) / mit Baked Sim (Spiel, Displacement gröber) / Live Sim / Baked Sim (genaueste Ansicht) / Debug Bottom Contour / Debug Foam | Spiel: Water Component With Baked Sim |

## Material (Baked Sim Material, SW_Water_Material_River)

- Schaum nur bei schnellem Wasser: **FoamAttenMin** (darunter kein Schaum), **FoamAttenMax** (ab da voller Schaum), **LowVelocityFoamScale**.
- Velocity Scattering: Scattering Min/Max Velocity (mehr Trübung bei Tempo).
- Wellen: Low Velocity Wave Scale, Wave Atten Min/Max, WPO-Wellen.
- Absorption/Scattering als globale Vektorparameter.

## Niagara Grid2D_SW_River (nur in einer Kopie ändern)

- Friction (bremst flaches Wasser, stabilisiert), Velocity Dissipation, Smoothing Width.
- Weißwasser-Emission: Curvature/Velocity/Vorticity/Depth-Difference Mult + Range, **Restrict Emission Depth/Speed Range**
  (kein Weißwasser in flachen/langsamen Bereichen), Dissipation Rate.
- Sekundär-Emitter (Gischt-Partikel) mit gleichen Emissionsreglern.
