# 16g Nachtrag 2 – Befunde nach 07:05, Antworten auf eure Rückfragen, Testreihe F (13.10.2026)

Bezug: eure Antwort `antworten/16g-nachtrag-ursache-gefunden.md` (a5be890). Eure Antwort entstand vor diesen Befunden.

## 1. Befunde nach 07:05 (C2, Zone 4096, Band = Bett + 2 m)

| Lauf | Änderung | Ergebnis |
|---|---|---|
| N1 | `match_spline_height_amount` **0,2** (sonst wie 4096-Lauf) | Front bleibt bei **s ≈ 76 m** stehen, 10 min unverändert |
| N2 | `match_spline_height_amount` **0,1** | wie N1, Front s ≈ 76 |
| N3 | **0,3** | Bett voll bis zur Mündung in ~4 min (bei 36 fps). **0,3 ist die Schwelle.** |
| N4 | Hindernisse: Akteur mit allen 1 718 Bachdekor-Teilen | Front bleibt hinter zwei ~1-m-Lippenfelsen nebeneinander stehen: Sie dämmen das 2-m-Bett der Bergrinne. |
| N5 | Hindernisse gefiltert: ohne Lippen-, Rand- und Bettfelsen; Teil ≤ 40 % der Bettbreite; je Meter zusammen ≤ 50 % (1 336 Teile: 669 Bachsteine, 359 Geröll, 226 Randsteine, 69 Äste, 7 Felsplatten, 6 Stämme) | läuft durch, Bett 99,8 % nass |
| N6 | Spline-Höhe nur im Kiesbett −12 cm | Front hängt in der **Rinne bei s 81** (knappe Lippe s 72–81). Die SWR reagiert **global** auf Spline-Höhen, vermutlich über die Höhenrundung relativ zum tiefsten Punkt. |
| N7 | Spline überall −10 cm | Front s 72 |
| **Endstand 10:15 (gespeichert)** | Spline oben (s < 560) **+10 cm**, Kiesbett (ab s 575) **−12 cm**, Band dort = Bettbreite; Nachfüllen 0,3, Entfernen 0, Quelle 300, Hindernisse N5 | Bett 99,8 % nass, Front 783 von 788 m, Tiefe Mitte 0,62 / 0,55 / 0,47 / 0,50 m (Plan 0,67 / 0,54 / 0,69 / 0,53), Überlauf im Kiesbett −35 % |

**Folgerung für F2:**
- `match_spline_height_amount` 0 / 0,02 / 0,05 liegt unter der gemessenen Schwelle (0,1 und 0,2 bleiben stehen).
- Ich teste F2 deshalb mit 0,3 / 0,4 und nur „Band = Bett“.
- Messen erst nach **≥ 4–5 min** statt 120 s. Die Füllzeit hängt an der Bildrate. Nach 3,5 min wirkte ein voller Lauf noch „hängend“.

## 2. Antworten auf eure Rückfragen (gelesen 13.10. 11:12)

1. **Teiler 6 oder 5:** F6 (Zone 2048) folgt nach F1/F2.
2. **Texturformat:**
   - `C2_Wasserzone`: Half Precision **aus** (32 Bit). Das wurde während der 16g-Diagnose umgestellt und so gespeichert.
   - C3, D2 und Meer: Half Precision **an**.
   - Speicher (`stat RHI`, Slices im `WaterInfoTextureArray`): noch nicht gemessen.
   - **Frage zurück:** Können wir C2 wieder auf 16 Bit stellen? Die Höhen liegen bei 30–190 m. Wenn die Wasser-Info Z in cm als Half Float
     speichert, sind das bei 190 m Stufen von 16 cm.
3. **World Partition:** `is_spatially_loaded` = **False** an allen Zonen (37 geladen). Alle Zonen sind also immer geladen.
4. **C2_Wasserzone:**
   - Lage (−221 050; −254 850; 4 953) cm, Ausdehnung 120 800 × 120 800 cm, Auflösung 4096², `enable_local_only_tessellation` False.
   - Der Erlenbach liegt **ganz** in dieser Zone. Fluss und Arm haben `water_zone_override` = diese Zone.
   - Erster Splinepunkt (−168 050; −276 750; 190,06 m), letzter (−172 297; −203 079; 35,81 m), 250 Punkte.
   - SWR: `sim_res` 319 × 2016, Zelle 36,7 cm, `resolution_max_axis` 2016, `source_size` 300 cm, `sim_speed`/`num_steps` 10/10,
     `smoothing_width` 5, `smoothing_cutoff` 500.
   - Gebackenes Rechteck (Dump): Quelle s 0 liegt 18 m vom oberen Rand, die Mündung 20 m vom unteren.
5. **`r.Water.WaterInfo.RenderTargetResolutionMax`:** Die Abfrage per Python liefert 0, ebenso für zwei andere Schreibweisen.
   Der Name existiert vermutlich so nicht. Bitte den genauen Namen nennen.
6. **Lokaler 1-m-Lauf des Exports:** folgt mit der Rollout-Planung.

## 3. Reihenfolge lokal

F1 (`remove_outside` 50) → F2 (Band = Bett, 0,3/0,4) → F6 (Zone 2048) → F4/F5 erst mit Antwort auf 16h §3 (unser Master hat kein `FoamAtten`).
