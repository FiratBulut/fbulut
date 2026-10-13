# 16h Nachtrag 5b – A/B der Wasseroberfläche (zu Nachtrag 5 §4, Frage 2) (13.10.2026, 17:25)

Bild: `bilder/swr_p2/wasser_oberflaeche_g0_g4.jpg`. Kameras t430/t500/t550 auf Augenhöhe und t500 schräg. Die Werte waren nur im Speicher
gesetzt, danach wieder G0. Alle Varianten haben Absorption 222/1000/1250, Streuung (0,5; 1; 1) × 0,02, Schaum 0 und Brechung 1,15.

| Variante | Water Roughness | Sim Velocity Normal Strength | Water Specular / Fresnel Specular | Eindruck |
|---|---|---|---|---|
| G0 (jetzt, = F) | 0,04 | 15 | 0,225 / 0,225 | golden-milchig, Wirbelmuster |
| G1 | **0,12** | 15 | 0,225 / 0,225 | **deutlich kühler und grauer**, weniger Gold; Steine im Grund bleiben sichtbar |
| G2 | 0,04 | **5** | 0,225 / 0,225 | wie G0, Wirbel ruhiger |
| G3 | 0,04 | 15 | **0,12 / 0,12** | kaum anders als G0 |
| G4 | 0,12 | 5 | 0,225 / 0,225 | wie G1, ruhiger |

**Unsicher:** Zwischen den Aufnahmen ändert sich der Himmel (Wolken), deshalb schwankt das Licht leicht. Dass G3 kaum wirkt, spricht dafür,
dass `Water Specular` in der gebackenen Darstellung (WCBS) nicht den Hauptanteil steuert. Oder das Gold ist kein Glanzlicht, sondern
Brechung und Streuung.

**Frage:** Welche Werte sollen wir setzen? Wir würden G1 oder G4 nehmen und dazu eine Augenhöhe-Messung machen (Szenenfarbe statt BaseColor).
Oder seht ihr einen anderen Hebel, zum Beispiel Streuung, `Water Fresnel Roughness` oder `Fluidsim Normal Strength`?
