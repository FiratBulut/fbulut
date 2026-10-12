# Auftrag 16g – Shallow Water River in einem steilen Bergbach: Wasser bleibt stehen (13.10.2026, 01:40)

## Lage

Erlenbach C2 neu als **ein** WaterBodyRiver (Ferat: „vom Berg“): Quelle am Fuß einer Felsrinne auf 190 m, 788 m Lauf bis in einen Fluss auf 36 m.
Gefälle: Bergrinne 0–199 m 21–64 % (Mittel ~39 %), Durchbruch 199–390 m (flacher Abschnitt, Spiegel 90 m waagrecht auf 106,4 m, dann Stufe),
Talkaskade 390–579 m ~31 %, Kiesbett 579–788 m ~2 %. 250 Spline-Punkte, 103 Becken-Stufen-Einheiten (Becken waagrecht, Lippe LINEAR),
Stufen im Median 1,6 m (max 3,7 m). Das Bett wurde mit dem Water-Brush aus **derselben** Spline gegraben (Blend Min, Kasten-U, festgeschrieben) –
Bett und Spline-Spiegel passen also zusammen (Bett in der Mitte im Median 4 cm vom Plan).

ShallowWaterRiver (UE 5.8.3): Quelle = Senke = der Fluss + ein zweiter Fluss (Arm in einer flachen Mulde). Fläche 118 × 741 m, resolution_max_axis
2016 (Zelle 0,37 m), sim_speed 10, num_steps 10, use_capture an, Boden-Landschaft gesetzt (Boden der Sim stimmt entlang des Laufs auf cm mit dem
Gelände überein – per swr_dump_baked geprüft). Spline nach dem Festschreiben 2 m breiter als das Bett, erster Punkt +0,3 m.

## Befunde (alle gemessen, gebackene Textur → 1-m-Raster)

1. **remove_outside_spline_amount 50:** Wasser nur von der Quelle bis s ≈ 62 m, dort **schnurgerade Abbruchkante** quer zum Lauf; egal ob
   match_spline_height_amount 0,05 / 0,3 / 2,0, Kamera nah/fern, Editor im Vordergrund, r.AllowOcclusionQueries 0.
2. **remove_outside_spline_amount 0:** Bergrinne in 90 s voll (Bett 99,8 % nass, Tiefe 0,59 m bei Plan 0,67), Kiesbett 96 % nass (Nachfüllen wirkt
   im Flachen), aber die **Front bleibt am Anfang des Durchbruchs stehen** (s ≈ 231 m, 16 %), Talkaskade 0 %. Zustand nach 90 s = nach 210 s = nach
   5 min (bis auf Zellenzahl gleich). Wasser steht also 0,6 m tief **still** in einer 39-%-Rinne – physikalisch unmöglich.
3. Editor tickt (≈ 40 fps, Spielzeit läuft mit), Niagara-Komponente aktiv und nicht pausiert (SetPaused(false) gesetzt), Viewport realtime.
4. Mit source_size 1000 + Nachfüllen 2,0: Bergrinne 2,08 m tief (Plan 0,67), Kies 1,02 m (Plan 0,53), Durchbruch bleibt trocken.
5. Umschalten der Darstellung (UpdateRenderState) startet die Sim neu; Bake verlangt LiveSim.
6. `WaterBodyComponent.get_water_surface_info_at_location(Vector(x, y, 0))` liefert in der steilen Rinne Spiegelhöhen bis 30 m unter dem Plan (nächster
   3D-Splinepunkt?). Vermutung: Die SWR bildet „innerhalb der Spline“ / Spline-Höhe in steilem Gelände ebenso falsch ab.
7. Log: nur „Mismatch between required interpolation parameters in GPUContext(1) vs calculated(0) Sim(Grid2D_SW_River:SW_River_Secondary_Emitter)“.
8. Header ShallowWaterRiverActor.h: Quelle/Senke über `QueryWaterAtSplinePoint(WaterBody, SplinePoint, OutPos, OutTangent, OutWidth, OutDepth)` –
   also an EINEM Splinepunkt (erster/letzter). Die Simulationsfläche ist das Rechteck um die Splinepunkte ohne Rand: die Quelle liegt 0,2 m vom Nordrand.
9. Bisheriger Erfolg (12.10.): flacherer Lauf (102 → 37 m), match 2 / remove 50 / source 1000 → Band voll (aber Band-Look, deshalb entkoppelt).

## Fragen

1. Warum bleibt das Wasser stehen bzw. warum friert die Sim nach ~60–90 s ein? Bekannte Grenzen der SWR bei steilen Flüssen (Gefälle > 20–30 %,
   Höhenunterschied > 100 m in einer Fläche), bei vielen LINEAR-Punkten, bei Quelle am Flächenrand? Epic-Forum, Tutorial-Kommentare, UDN-Zitate,
   5.6–5.8 Release Notes, Witcher-4-Vortrag.
2. Wie speist die Quelle ein (Tiefe/Breite/Tangente des ersten Splinepunkts, „Source Width“)? Was muss am ersten Punkt stehen, damit dauerhaft
   Wasser nachläuft (flaches Quellbecken? Tiefe? Tempo?) – und wie viel (m³/s) ergibt das?
3. Wie bestimmt die SWR „innerhalb der Spline“ und die Spline-Höhe (Water-Info-Textur der Wasserzone? 2D/3D?) – und warum versagt das in steilem
   Gelände? Gibt es eine Einstellung (Zone, Water-Info-Auflösung, River-Mesh, Spline-Punkttypen, Tangenten), die das behebt?
4. Empfohlene Einstellungen für einen 2–8 m breiten Wildbach mit 30–60 % Gefälle und 1–3-m-Stufen: Speed/Substeps, Friction, Velocity Dissipation,
   Smoothing, Auflösung; und ob man lange steile Bäche in **mehrere Simulationsflächen** teilen sollte (Ferat erlaubt Teilen nur der Sim-Flächen,
   nicht des Flusses) – mit Überlappung, damit die obere Fläche die untere speist?
5. Falls die SWR für steile Bäche ungeeignet ist: Was nutzt man stattdessen für Witcher-Qualität (gebackene Flowmaps, Niagara Fluids 2D, statische
   Kaskaden-Netze + Spline-Wasser)? Konkrete Werkzeugkette in UE 5.8.

Antwort bitte als `recherche/antworten/16g-swr-steiler-bergbach.md`, mit Quellenangaben und klaren Testschritten (Werte, Reihenfolge, Messgröße).
