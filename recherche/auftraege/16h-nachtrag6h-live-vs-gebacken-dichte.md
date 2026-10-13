# 16h Nachtrag 6h – Live-Simulation sieht gut aus, gebacken nicht (Ferat 23:10); Dichte-Zensus Demo-Karten vs. Eldarien

Stand 14.10. 00:00. Ferat schläft; Wochenlimit fast erreicht → bitte kompakt antworten.

## 1. Wasser: Live (Niagara) vs. gebacken – Bilder `bilder/swr_p2/wasser_live_vs_gebacken_p2l.jpg`

- **Live** (Niagara `Grid2D_SW_River` mit `SW_Water_Material_River_Niagara`): klar, leicht grünlich, Grund und Steine sichtbar, feine Wellen,
  Schaum an Stufen. **Gebacken** (WaterBodyRiver + `MI_EL_SWR_Klar`, WCBS): braun-deckend, zäh. Ferat will den Live-Look.
- Epics gebackenes Gegenstück `SW_Water_Material_River` im vollen Zyklus (Reset, 5 min, Bake) sieht **genauso braun** aus wie unseres
  (`epic_material_gebacken_p2h.jpg`) → nicht das Master-Material, sondern die Instanzwerte: Das Niagara-Kind hat **Absorption (20,8; 25; 24,7)**,
  Scattering (0,77; 1,0; 0,92; 0,5), Water Albedo 0,083, Roughness 0,02, Near Normal 0, Distant 0,3/0. Unser MI_EL_SWR_Klar: Absorption
  (222; 1000; 1250) [Einheit in unserem Master = Sichttiefe cm], Scattering (0,5; 1; 1)×0,02.
- Test läuft: `MI_EL_SWR_EpicKlar` (Kind von SW_Water_Material_River mit den Niagara-Werten) auf dem gebackenen Fluss, Bilder P2M → 6i.
- **Frage:** Welche Absorptions-/Streu-Einheit hat `SW_Water_Material` (Niagara-Master) gegenüber Epics Water-Plugin-Master (unser Schaum8)?
  Wie übersetzen wir die Live-Werte in `MI_EL_SWR_Klar` (Koeff_Skala?), damit gebacken = live aussieht? Dazu: Niagara-Live hat Near Normal 0 –
  d. h. keine Textur-Normalen nah, nur Sim-Normalen; soll unser Master das übernehmen (V20a hinfällig?).

## 2. Dichte-Zensus (Werkzeug `ue_demo_dichte.py`, `daten/dichte/`, Tabelle `dichte_vergleich.md`)

Demo-Karten Rural Australia Example 01–03 (je 1 km² Landschaft, Bilder `demo_karten_rural_australia.jpg`) gegen Eldarien C2 (ganzes Feld) und
Fenster Talkaskade (200 × 200 m). Basalt/NWFX ohne Landschaft → Fläche 0 → **Spalten ignorieren (Demo-Mittel dadurch unbrauchbar, nur Einzelspalten lesen)**.

| je 100 m² | RA1 | RA2 | RA3 | C2 Feld | C2 Talkaskade-Fenster |
|---|---|---|---|---|---|
| Netze gesamt | 3,8 | 8,7 | 10,5 | 9,4 | 24,0 |
| Felsen/Steine | 1,2 | 1,8 | 0 | 3,4 | 4,7 |
| Pflanzen-Netze | 0 (Gras = Landschaftsgras) | 0 | 0 | 2,1 | 8,5 |
| Mittelgroß 0,5–3 m | 2,6 | 5,3 | 6,1 | 5,3 | 18,3 |
| Bäume ≥ 3 m je ha | 73 | 3 | 1,3 | 17 | 1,8 |
| Felsdeckung % (Obergrenze, Überlappung ignoriert) | 1,9 | **378** | 0 | 78 (wenige riesige Felsschalen) | **1,2** |
| verschiedene Netze | 35 | 53 | 45 | 294 | 181 |

- **Befund:** An Stückzahlen je Fläche liegen wir NICHT unter den Demo-Karten (sie sind über 1 km² gerechnet, die Demo-Szenen sind punktuell
  dicht). Der Unterschied steckt in **Größe, Überlappung und Ort**: RA2 hat Felsfußflächen von 378 % der Fläche (gestapelte, überlappende
  Felsblöcke, Klippe im Bild), unsere Talkaskade 1,2 % (Kleinsteine ≤ 0,5 m, keine Blöcke). Und: Die Demos nutzen 35–53 verschiedene Netze, wir
  181–294 – Vielfalt ist nicht das Problem, Komposition ist es.
- Das stützt Auftrag 20/21: große Felsnetze (1–8 m) in Stapeln auf Steilflächen/Ufern, nicht mehr Kleinzeug.
- Messung je Prüfbild (Pixelanteil Netz/Landschaft) folgt als Werkzeug, wenn ihr es als Kriterium wollt (21 §5 g).

## 3. Stand sonst
- Aufträge 20 (65da488) und 21 (ba23bb1) liegen bei euch; Fab-Bibliothek `daten/fab_bibliothek_2026-10-13.*`; Ladeliste an Ferat gegeben
  (Open World Demo Collection, Valley of the Ancient, Landscape Mountains, Nature Set, Park Photo Scanned, Rocks Packs, Beach cliff rock face,
  Stein-Piles, Megaplants Black Alder/Norway Spruce/Baltic Pine/Common Hazel; Megascans scree/slate/layered cliff/boulder/rock assembly/fern/lichen).
- 6g (Uferstufe/37-cm-Zellen) wartet auf Antwort.
