# Antwort zu Korrektur Runde 3 (Auftrag 11, Felsgruppen)

Stand: 10.10.2026. Beide Punkte sind umgesetzt und synthetisch getestet. Echtdaten-Zahlen sind Erwartungen, nicht gemessen. Details:
`verteilung-fels-organisch.md` Abschnitt j, Zahlen in `verteilung-STATUS.md` Abschnitt „Runde 3“.

## Kurzfazit

1. **Rote Findlinge:** `/Game/AncientContent/Megascans/3DAssets/IcelandicBoulder/SM_IcelandicBoulder_01–03` stehen nur noch in canyon,
   oedland, wueste und lava. felsgruppen erzwingt das zentral über den Block `netz_nur_biome`, auch für alle Overrides der Biome.
   nordkueste, heide_tundra und hochgebirge nutzen sie nicht mehr. Die Taxonomie markiert sie nur noch für diese vier Biome als geeignet.
   Graue `/Game/Megascans/…/SM_IcelandicBoulder_*` gibt es im Inventar nicht. Ersatz: pkeeM, skjsL, `SM_MossyForestBoulder_03/04`,
   `SM_ground_rock_01`, `SM_mountain_rock_big_02_4`.
2. **Formgruppen 10–30 m:** neue Klasse `formgruppe`. Je Feld 8–20 Gruppen auf den markantesten Graten und Kuppen, Mindestabstand 120 m.
   Hero ist eine große Klippe als Akteur mit Kollision, skaliert 1,0–2,0, 35–60 % eingegraben, Rückseite hangwärts, Schichtneigung je Massiv.
   Dazu 3–6 Satelliten von 2–6 m und ein Blockstrom am Fuß. Hangknick ist Pflicht, auf Wiesen ohne Hangknick entsteht keine Gruppe.
3. **Quarry Cliff `uchoab3fa`:** steht auf der Sperrliste.

## Erwartete Zahlen

| Feld | Formgruppen | Instanzen gesamt | Akteure |
|---|---|---|---|
| A5 | 10–16 | ca. 4 800–5 600 | ca. 45–60 |
| B4 | 8–14 | – | – |
| G4 | 0–3 | – | – |

- **Hero-Größe:** 18–38 m breit, Median ca. 25–30 m; sichtbar 5–18 m hoch, Median ca. 8–12 m.
- **Synthetisch gemessen:** A5 10, B4 8, G4 1 Formgruppen. Hero-Breite Median 25 bzw. 29 m, sichtbare Höhe Median 8 bzw. 11 m.
- **Hero-Netze:** rcygn (Sharp Cliff), vfmjadufa, vdssailfa, veqnci0db (Massive Nordic Coastal Cliff), `SM_MassiveNordicCoastalCliff_01`,
  `SM_HugeNordicCoastalCliff_01/02`; im Canyon Sandstein-Klippen, in Lava `LavaSpire_02`.
- **Auswahl:** Krümmung, Prominenz und Sichtbarkeit von Weg, Tal und Wasser aus 300–1 500 m, berechnet mit Sichtstrahlen auf einem 8-m-Raster.
- **Runde-2-Gruppen** mit 4,5–8,5 m Hauptfels bleiben nur als Begleiter: höchstens 3 je Formgruppe, sonst höchstens 6 je Feld.

## Bitte vor dem Setzen prüfen

1. **Offene Seite der Klippen:** angenommen auf lokal +y, bei veqnci0db +x. Ist sie in der Kamera `formgruppe_front_120m` von vorn sichtbar,
   je Netz `"rueckseite": "-y"` in `felsgruppen_regeln.json` unter `formgruppen.hero.paletten` setzen.
2. **Pivot:** Keines der Hero-Netze steht in `netze_masse.json`, der Pivot ist unten angenommen. Liegt er mittig, stimmt die Eingrabtiefe nicht.
3. **Prüfkameras** in `felsgruppen/<Feld>/plan.json`: `formgruppe_300m_1..3`, `formgruppe_front_120m`, `formgruppe_flanke_120m`.
4. **Big_Rock:** `SM_Big_Rock_0*` und `SM_big_rock_wall_02` erreichen auch bei Maßstab 2,0 keine 10 m und sind deshalb aussortiert.
   Sollen sie mitspielen, `groesse_min_m` auf 8 senken.
5. **Bänder:** Wirkt der Hang aus 300 m weiter punktig, ist `klassen.band.p` der Hebel. Diese Klasse ist unverändert.
