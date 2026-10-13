# 16g Nachtrag – Ursache gefunden (13.10.2026, 07:05)

**Die Wasser-Info der Wasserzone war zu grob.** `C2_Wasserzone`: Zone 1208 × 1208 m, `render_target_resolution` 1024 → **1,18 m je Pixel**.
Der Erlenbach ist in der Rinne 1,6–2,4 m breit und liegt schräg im Raster: In der Draufsicht ist er 1–2 Pixel breit und bekommt beim
Rastern Lücken. Dort „gibt es“ für die SWR keinen Fluss: kein Nachfüllen, `remove_outside_spline` löscht, die Front bleibt stehen.

Belege:

| Lauf | Band (Spline-Breite) | Zonen-Auflösung | Ergebnis |
|---|---|---|---|
| remove 50 | Bett + 2 m | 1024 | nass nur bis s 62 (gerade Kante) |
| remove 0 | Bett + 2 m | 1024 | Front s 231, steht |
| remove 0, Tangenten repariert | Bett (1,6–7,8 m) | 1024 | Front **s 74**, steht |
| remove 0 | Bett + 2 m | **4096 (0,29 m/Pixel)** | **Bett zu 99,9 % nass bis s 780**, keine Lücke; Tiefe Mitte 0,44–0,64 m (Plan 0,53–0,69) |

Die Lage der Kante wanderte mit Splineform und -breite – passt zu Rasterlücken, nicht zu Physik. Die Zone ist **nicht** lokal
tesselliert (`enable_local_only_tessellation` False), Höhen weit unter 16-Bit-Grenzen.

Folgerung für den Export/die Regeln: je SWR-Bereich die Pixelgröße der zuständigen Zone prüfen: **Pixel ≤ schmalste Bachbreite / 6**
(z. B. 2 m Bach → ≤ 0,33 m → bei 1208-m-Zonen 4096). Testplan-Stufen 1–5 sind damit überholt; offen bleiben nur Feinwerte
(Überlauf neben dem Bett, Schaum, Tempo).
