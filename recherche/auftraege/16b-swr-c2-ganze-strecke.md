# Auftrag 16b – Shallow Water River auf der ganzen C2-Strecke (gespeichert)

Stand 12.10.2026, 16:10. Mit Ferats Freigabe steht C2 jetzt dauerhaft mit Shallow Water River: `SWR_C2_Fluss` (WaterBodyRiver, s 0–179 m entlang
eurer Mittellinie, Breite/Tiefe/Tempo je Punkt) + `SWR_C2` (`resolution_max_axis` 512), das Kaskadennetz ist unsichtbar geschaltet (rückbaubar).
Bild: [`bilder/swr/c2_ganz_netz_live_gebacken.jpg`](../bilder/swr/c2_ganz_netz_live_gebacken.jpg) (links Kaskadennetz Version 3, Mitte live,
rechts gebacken).

## Befund

- **Deutlich natürlicher als das Netz:** von der Seite (`s1`) und von unten (`kn0_unten`) ein durchgehender Wildbach, keine Terrassen mehr; im oberen
  Becken (`kn0_oben`) klares Wasser mit sichtbarem Grund, an der Lippe Beginn des Wildwassers. Nah von oben (`kn0_nah_s119`) weiter zu türkis/marmoriert
  (siehe 16a-Nachtrag), aus normaler Entfernung liest es sich als schäumendes Wasser.
- **Einbacken** geht über `EldarienTransferLib.shallow_water_river_bake(komponente)` (ruft `UShallowWaterRiverComponent::Bake()`); danach
  `render_state = BAKED_SIM`. Gebacken sieht es aus wie live ([`bilder/swr/t1_live_gegen_gebacken.jpg`](../bilder/swr/t1_live_gegen_gebacken.jpg)).
- **Im Editor** rechnet die Simulation auch gebacken und mit `set_paused(True)` weiter (0,6–0,8 ms bei 256 auf 40 m). Ungespeicherte Akteure erscheinen in
  PIE nicht (World Partition). Messung im Spielmodus mit Teleport nach C2 läuft gerade (Auftrag 200).
- Die Fälle (S03, S05, S10, S15) zeichnet die Simulation als steile Wildwasserrinne; die bestehenden Niagara-Effekte bleiben. Wie in 16 vorgesehen,
  kommen Vorhang und Schaumobjekte nur dort dazu, wo eine echte Fallkante sichtbar sein soll.

## Für euren Umbauplan

1. Je Gewässerstrecke **ein** `fluss_sim`-Abschnitt über die ganze Strecke funktioniert (C2: 179 m, 30 m breit, Auflösung 512, ≈ 0,35 m je Zelle).
   Eure Splinepunkte (Lage, Breite, Tiefe, Tempo) reichen; wir nehmen derzeit `mittellinie` [x, y, z, breite, tempo, …, abstand_bett] alle ≥ 2 m.
2. Stufen/Becken im Gelände (13f-Regel) bleiben die Grundlage – die Simulation füllt die Becken selbst.
3. Bitte im Plan je Strecke eine empfohlene `resolution_max_axis` (Zellgröße ≈ 0,3–0,5 m) und die Liste der Objekte mit `wasser_kollision`.

## Nachtrag 16:30 – D6 umgesetzt: gebacken im Spielweg mit klarem Wasser (gespeichert), Kosten im Spiel

- `MI_EL_SWR_Klar` = Kind von `MI_Eldarien_Wasser_Fluss` (unser Master) mit euren Werten aus 16a b2/b3: Absorption 250/1430/2000 (A 8),
  Scattering 0,6/0,8/1,0 (A 0,12 wie bei uns), Water Albedo 0,03, Foam Emissive 0, SimFoam Contrast 2, Foam powr 0,6, Foam Boost 0,8,
  Foam Opacity 0,9, Foam Texture Blend Min 0,6, Water Roughness 0,02.
- `SWR_C2`: gebacken (Plugin), `render_state = WATER_COMPONENT_WITH_BAKED_SIM`, Water-Body-Material und `baked_sim_material` = `MI_EL_SWR_Klar`.
  **Gespeichert.** Bild: [`bilder/swr/c2_wcbs_klar.jpg`](../bilder/swr/c2_wcbs_klar.jpg) (links Netz, Mitte LIVE_SIM, rechts WCBS klar).
- **Aussehen:** Marmor-Türkis weg. Becken klar mit sichtbarem Grund, weißer Schaumsaum an den Lippen, steile Rinnen weißes Wildwasser.
  Offen: in den steilen Rinnen eher zu viel Schaum (fast flächig weiß), von der Seite ist der klare Bach sehr unauffällig.
- **Kosten im Spielmodus (PIE, Teleport an C2, ProfileGPU, ganze C2-Strecke 179 m, Auflösung 512):**

  | Zustand | `Grid2D_SW_River` GPU | Dispatches |
  |---|---|---|
  | LIVE_SIM | 0,6 ms | 59 |
  | BAKED_SIM | 0,3 ms | 3 |
  | WATER_COMPONENT_WITH_BAKED_SIM | **0,2 ms** | 3 |

  Wichtig: Ungespeicherte Akteure erscheinen in PIE nicht (World Partition); PIE startet am PlayerStart (E5) → Teleport nötig.
- **Fragen:** (1) Was sind die 3 verbleibenden Dispatches im gebackenen Zustand (Sekundär-Emitter/Interaktion?) – lassen sie sich im Spiel abschalten,
  wenn kein Pawn im Wasser ist? (2) Schaum in steilen Rinnen dünner: welche Werte zuerst (SimFoam Contrast höher, Foam Opacity, Sim Foam Scale)?
