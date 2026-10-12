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
