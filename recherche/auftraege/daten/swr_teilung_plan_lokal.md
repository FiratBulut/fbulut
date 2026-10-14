# SWR-Teilung Erlenbach p2 – Plan und Werkzeuge (Hilfsagent 14.10.2026)

Bezug: Cloud-Antwort 16h-Nachtrag 6g (`recherche/antworten/16h-nachtrag6g-uferstufe-simulation.md`, §1.3 „Test für Ferat“, Variante B)
und Rückfrage 2 der Cloud. Alles offline erarbeitet: Editor-Skripte sind **ungetestet im Editor**, nur per Trockenlauf
(`python -I scripts/swr/teilung_trockenlauf.py` → 87 Prüfungen OK, 0 Fehler; `bash -n` der Kette OK). Nichts wurde im Editor geändert,
nichts gespeichert, nichts gelöscht.

## 1. Antwort auf Rückfrage 2: Wie legt unser Bauwerkzeug die Rechenfläche einer SWR fest?

**Gar nicht – die Engine legt sie selbst fest.** Weder Actor-Box noch Skalierung noch eine Property setzen bei uns das Rechteck.

Aus `scripts/unreal/ue_swr_bauen.py`:

| Stelle | Was passiert |
|---|---|
| Z. 1–2, 29–32 (Kopf) | „Messung 12.10.: Simulationsbereich = achsparalleles Rechteck um die Quell-Flüsse“; Kachelmodus: „jedes davon rechnet das Rechteck um den **ganzen** Fluss (begrenzt nichts)“ |
| Z. 311–316 `rechteck(P)` | **Vorhersage**: Hülle der Spline-Punkte ± halbe Spline-Breite → `[x0, y0, x1, y1]` cm. Wird nirgends in den Editor geschrieben |
| Z. 318–319 `seite_m` | längste Rechteckseite in m |
| Z. 322–332 `aufloesung(L)` | `resolution_max_axis = ceil(L / Zielzelle)` auf Vielfache von 32, 256…2048 (`RESWERT` erzwingt) – **das** ist der einzige Wert, der aus dem Rechteck in die SWR fließt |
| Z. 303–304 `erweitert(bx, 800)` | nur der Suchbereich (+8 m) für Felder, Landschaft und Boden-Akteure (`bereich`), nicht die Simulation |
| Z. 531–559 `stuecke_bilden` | teilt nur nach Länge (> 2048 × Zielzelle) und erzeugt `_T01, _T02 …` als **eigene WaterBodyRiver-Stücke** – d. h. auch dort kommt die kleinere Rechenfläche nur über einen kleineren Quell-Fluss zustande |
| Z. 904–960 (v3) | `begrenzung.rechteck_cm` wird nur in `rechteck` der Einheit übernommen (Auflösung + Ablageort); keine Property |
| Z. 2427–2434 `swr_spawnen` | `spawn_actor_from_class(ShallowWaterRiver, Mitte des Rechtecks, Rotator 0)`; Label, Ordner, Etiketten, HLOD aus – **keine Skalierung, keine Box-Extent** |
| Z. 2436–2449 `swr_einrichten` | gesetzte Properties: `resolution_max_axis`, `render_state` LIVE_SIM, `disable_cpu_throttling`, `bottom_contour_landscape_actors`, `source_river_water_bodies`, `sink_river_water_bodies`, `bottom_contour_tags`, `bottom_contour_actors`, `baked_sim_material` (v3 dazu `use_capture`, `match_spline`) |
| Z. 2497–2503 `ph_swr` | Ablageort = Rechteckmitte, z = zmax + 1 m |
| Z. 1650–1664 `flaeche_text` | prüft **nach** dem Bake, ob die gemeldete Fläche „Einheit“ oder „GANZEN FLUSS“ deckt – d. h. das Werkzeug erwartet selbst, dass die Engine das Rechteck wählt |

Engine (lokal gelesen: `UE_5.8/Engine/Plugins/Experimental/WaterAdvanced/Source/WaterAdvanced/Public/ShallowWaterRiverActor.h`):
`UShallowWaterRiverComponent` hat **keine** editierbare Bounds-Property. `WorldGridSize` (FVector2D) und `SystemPos` (FVector) sind
`private: UPROPERTY()` ohne `EditAnywhere` (Z. 225–229) → aus Python nicht erreichbar; sie werden in `Rebuild()` aus den Wasserkörpern
(`AllWaterBodies`, Z. 222–223, `QueryWaterAtSplinePoint`) berechnet. Belege: der Dump vom 13.10. meldet `groesse_cm [11682, 73988]`,
`mitte_cm [-173328, -239773]`; meine Nachrechnung „Hülle der Spline-Punkte ± halbe Spline-Breite“ aus `lauf_p2.json` ergibt
116,9 × 741,6 m, Mitte (−173326, −239859) – Abweichung < 2 m. Der Akteur selbst steht woanders (Rechteckmitte beim Bau) und ist egal.

**Folge für Variante B:** Drei SWR auf **demselben** `WaterBodyRiver` rechnen alle das 740-m-Rechteck (bei 2048 → 0,36 m, kein Gewinn).
Variante B „ohne Codeänderung“ geht nur, wenn jede SWR einen **eigenen Quell-Fluss** bekommt, der nur ihren s-Bereich abdeckt. Das ist
praktisch die Cloud-Variante C in leichter Form: drei WaterBodyRiver-**Kopien** der heutigen Spline (je ein s-Bereich, gleiche Punkte,
Breiten, Tiefen, Materialien, Zone), das Original bleibt versteckt erhalten. Das Skript unten baut genau das (`MODUS fluss`) und kann
zum Beleg auch die wörtliche Variante B bauen (`MODUS gleich`, dann zeigt `status` bei allen dreien „geschrumpft nein“).

## 2. Rechtecke und Zellen der drei Teile (Vorhersage aus `lauf_p2.json`, Spline-Band = Bett + 2 m bis s 575, danach Bettbreite)

| SWR | s (m) | Rechteck (m) | Auflösung | Zelle | Raster | Zellen | gebackene Texturen (3 Stück) |
|---|---|---|---|---|---|---|---|
| heute ganz (Fluss + Arm) | 0–788 | 116,9 × 741,6 | 2016 | 0,368 m | 2016 × 318 | 641 k | ≈ 12 MB |
| **T00 oben** | 0–393 | 53,2 × 381,0 | 2048 | **0,186 m** | 2048 × 286 | 586 k | ≈ 11 MB |
| **T01 Talkaskade** | 385–583 | 67,2 × 185,2 | 2048 | **0,090 m** | 2048 × 743 | 1 522 k | ≈ 27 MB |
| **T02 unten (+ Ost-Arm)** | 575–788 | 93,9 × 201,2 | 2048 | **0,098 m** | 2048 × 956 | 1 958 k | ≈ 35 MB |
| T02 ohne Arm (Arm bliebe trocken) | 575–788 | 71,7 × 201,2 | 2048 | 0,098 m | 2048 × 730 | 1 495 k | ≈ 27 MB |
| T01 bei 1024 | 385–583 | 67,2 × 185,2 | 1024 | 0,181 m | 1024 × 372 | 381 k | ≈ 7 MB |
| T02 bei 1024 | 575–788 | 93,9 × 201,2 | 1024 | 0,196 m | 1024 × 478 | 489 k | ≈ 9 MB |

- Die Cloud rechnete mit „~200 × 30 m“ (0,6 Mio. Zellen). Tatsächlich mäandert der Bach: Talkaskade 67 m, unten 72 m (94 m mit Arm) breit →
  **T01 und T02 haben je 2,4–3× so viele Zellen wie heute der ganze Bach**. Das kostet Zeit beim Einlaufen/Backen und Grafikspeicher für die
  Live-Simulation (Niagara-Grid ≈ 2 Mio. Zellen). Falls das klemmt: `RES=1024` für die Kette → Zellen 0,18/0,20 m, d. h. halb so grob wie
  heute (Band-Ziel dann nach Cloud §3: 0,25–1 m ≤ 30 %, 1–2 m ≤ 5 %).
- Der Ost-Arm mündet bei s ≈ 660–770 (Pfad 40 m östlich der Mittellinie) → gehört zu T02 (Quelle + Senke wie heute).
- Nähte: oben T00/T01 überlappen 385–393 (Becken zwischen Lippe 0 bei s 389,0 und Lippe 1 bei 392,9 im Bettplan); unten T01/T02 überlappen
  575–583 (letztes Becken bis Stufe 46 bei s 579, dann Kies). Bei 3-m-Punktabstand landen die Schnittpunkte bei s ≈ 387/393 bzw. 576/582
  (Trockenlauf: Überlappung je 6 m); liegt kein Spline-Punkt im 8-m-Fenster, fügt das Skript einen Zwischenpunkt in der Fenstermitte ein.

Kontrolle im Editor: `status` gibt je SWR „Vorhersage“ (aus den Quell-Splines) und, wenn das Plugin antwortet, `swr_info` (SimRes, SimDx,
groesse_cm) aus und die Zeile `TEILEN STATUS PRUEF <SWR> … geschrumpft ja|nein` (Bezug: 741,6 m der Sicherung, Schwelle 80 %).

## 3. Neue Dateien

| Datei | Zweck |
|---|---|
| `live/claude_code/swr/swr_teilen_p2.py` | Editor-Skript, `PHASENAME lesen|bauen|zurueck|status`, `MODUSWERT fluss|gleich` [fluss], `RESWERT` [2048], `ALTWERT lassen|leeren` [lassen]. Speichert nicht |
| `live/claude_code/swr/frisch_reset_akteur.py` | `frisch_reset.py` je Akteur: `AKTEURNAME`, optional `FLUSSNAME` (Standard: erster Quell-Fluss der SWR = Teilfluss), `HOEHEWERT`/`REMOVEWERT`/`QUELLEWERT`, `HINDWERT ja|nein|unersetzt=lassen`, `BANDWERT ja|nein`. Band −2/+2 m, LIVE_SIM als Property, Echtzeit an, `swr_rebuild` |
| `live/claude_code/swr/_teilung_bake.py` | `swr_bake(akteur, True)` + Darstellung WCBS (Property, Rückfall `swr_set_render_state(a, 1)`), meldet SimRes/SimDx |
| `live/claude_code/swr/teilung_speichern.py` | gezieltes Speichern: Erlenbach-Satz + `_T00…_T02` (Fluss und SWR). Nur bewusst aufrufen |
| `live/claude_code/swr/_teilung_kette.sh` | Ablauf (unten), Log `swr/_teilung_kette.log`, Marken `TEILUNG_START/TEILUNG_FERTIG/TEILUNG_ABBRUCH` |
| `scripts/swr/swr_dumps_vereinen.py` | drei 1-m-Raster → `<ZIEL>_sim_{tiefe,spiegel,tempo}.f32` + `_sim_herkunft.u8` + `_sim_meta.json` (je Zelle der Teil mit der größten Tiefe); Naht-Messung (Spiegelsprung median/p90/max, trockene Meter auf der Mittellinie, Deckung je Teil). Exit 3 bei leerem Teil |
| `scripts/swr/teilung_trockenlauf.py` | Ersatzmodul `unreal` + Testwelt aus `lauf_p2.json`; prüft alle Phasen, Reset/Bake/Speichern, Vereinen (mit dem echten ENDSTAND_1015-Dump, Ausgabe nur in %TEMP%) |
| `live/claude_code/wasser_check/swr_teilen_sicherung.json` | entsteht erst im Editor durch `lesen`/`bauen` (Rückweg-Wahrheit; wird nicht überschrieben, solange die alte SWR das Etikett `EL_SWR_TEILUNG_ALT` trägt) |

### Was `bauen` (MODUS fluss) genau tut

1. Sicherung schreiben, falls sie fehlt (alle Editor-Properties der SWR-Komponente, Transform/Bounds, Quellen/Senken als Labels, Fluss-Properties, Vorhersage).
2. Je Teil: Punkte der heutigen Spline im s-Bereich (s über die nächste Lauflinien-Stelle) → neuer `WaterBodyRiver` `SWR_Fluss_F_ERLENBACH_1V_C2_T0x`
   (Reihenfolge wie `fluss_bauen`: `eld.ohne_pinsel`, `affects_landscape` aus und `water_zone_override` **vor** den Punkten, `set_spline_points`,
   LINEAR bleibt LINEAR, sonst Original-Tangenten als CUSTOM (Geometrie identisch), Breite/Tiefe/Tempo/Audio je Index, Materialien/Kollision/
   Islands/Exclusions kopiert, `overlap_material_priority` = Original + 2 (Talkaskade) bzw. + 1, `rebuild_native_body`).
3. Je Teil: `ShallowWaterRiver` `SWR_Sim_F_ERLENBACH_1V_C2_T0x` an der Rechteckmitte; alle 28 kopierbaren Komponenten-Properties von der alten SWR
   (Nachfüllen 0,3, remove 0, source_size 300, Materialien, `bottom_contour_actors` = WH, Landschafts-Proxys, Tags), `resolution_max_axis` RES,
   Quelle = Senke = Teilfluss (T02 + Ost-Arm), `render_state` erst WATER_COMPONENT (billige Neuaufbauten), **LIVE_SIM zuletzt**.
4. Alte SWR: `render_state` WATER_COMPONENT, `set_paused(True)` (BlueprintCallable laut Header), versteckt (Editor + Spiel), Etikett
   `EL_SWR_TEILUNG_ALT`; Quelle/Senke bleiben (`ALTWERT=leeren` leert sie). Die Komponente kennt kein `enabled`; `auto_activate`/`visible` werden
   nur gelesen. Alter Fluss (nur MODUS fluss): versteckt (Editor + Spiel + `set_visibility(False)`), Etikett `EL_SWR_TEILUNG_ALT`.
5. Alle neuen Akteure tragen `EL_SWR_TEILUNG` (+ `EL_SWR_TEILUNG_T0x`, `_FLUSS`/`_SIM`); absichtlich **nicht** `EL_SWR_F_ERLENBACH_1V_C2`, damit
   `ue_swr_bauen.py zurueck` sie nicht mit erfasst.

## 4. Aufrufe (Git-Bash, aus `live/claude_code`)

```bash
# Vorab, nur lesen (schreibt die Sicherung):
sed -e "s|PHASENAME|lesen|" swr/swr_teilen_p2.py > $TEMP/t_lesen.py && python ue.py $TEMP/t_lesen.py | grep -a "^TEILEN"

# Beleg für die Cloud (3 SWR auf demselben Fluss rechnen das ganze Rechteck) – ca. 10 min, dann zurück:
MODUS=gleich NURBAU=ja bash swr/_teilung_kette.sh        # bauen + status (ohne Reset: SimRes erst nach einem Reset je SWR)
ZURUECK=ja bash swr/_teilung_kette.sh

# Der eigentliche Test (Teilflüsse, 2048, 3 × 5 min + 3 Bakes + Dumps + Messung + Bilder P2T):
bash swr/_teilung_kette.sh
#   Varianten: RES=1024 bash swr/_teilung_kette.sh | WARTE=420 … | BILDER=nein … | TEILE="T01 T02" … (nur diese Teile resetten/backen)
#   NURBAU=ja … = nur lesen + bauen + status (zum Ansehen im Editor)
#   Achtung: die Kette baut immer neu; steht der Bau schon (Etikett EL_SWR_TEILUNG), bricht sie ab -> erst ZURUECK=ja, oder einen
#   einzelnen Teil von Hand: sed AKTEURNAME -> frisch_reset_akteur.py, 5 min, _teilung_bake.py, swr_dump.py (Zeilen wie in der Kette)

# Rückweg (löscht nur Akteure mit EL_SWR_TEILUNG, schließt alte SWR/Fluss aus der Sicherung wieder an, speichert nicht):
ZURUECK=ja bash swr/_teilung_kette.sh
timeout 300 python ue.py swr/frisch_reset.py      # LIVE_SIM + Reset der alten SWR, 5 min, dann Bake wie _sim_neu.sh
timeout 600 python ue.py swr/fluss_swr_speichern.py

# Speichern des geteilten Stands (nur wenn gewollt):
timeout 600 python ue.py swr/teilung_speichern.py
```

Ablauf der Kette je Teil: `frisch_reset_akteur` (Band −2/+2 am Teilfluss, LIVE_SIM, Reset) → `status` (bei MODUS fluss Abbruch, wenn
„geschrumpft nein“) → WARTE s (Standard 300, Viewport-Echtzeit an) → `_teilung_bake` → `swr_dump.py` → `swr_dump_lesen.py` (als Spline-Band
dient die vorhandene `SWR_Sim_F_ERLENBACH_1V_C2_meta.json`/`_spiegel.f32`, kopiert auf den Teilnamen) → bei leerem Dump Abbruch.
Danach: `swr_dumps_vereinen.py --naht 385 393 --naht 575 583` → `P2T_VEREINT`, `p2bett_pruefband.py --dump P2T_VEREINT --nass-cm 1|2|5|10`
(zugleich Rückfrage 1 der Cloud), `swr_p2_messen.py P2T_VEREINT --bild`, `status`, Bilder `witcher/blick_bilder.sh` mit `swr/_kam_talk.json`
(m_talkaskade, t430/t500/t550 schräg + Auge), Präfix P2T. Ergebnisse: `export/unreal/welt/fluss_sim/swr_wasser/P2T_VEREINT_*`,
`SWR_Sim_F_ERLENBACH_1V_C2_T0x_sim_*`, Log `swr/_teilung_kette.log`.

Prüfkriterien (Cloud 6g): Front 788/788, Bett ≥ 99 % nass, Band 0,25–2 m ≤ 5 % (bei > 2 cm), Naht-Spiegelsprung ≤ 2 cm, kein trockener
Streifen (Zeile `NAHT … Mittellinie … trocken 0 m`), Kolk-Median ≥ 0,8 m, Bilder ohne Flackern beim Annähern.

## 5. Risiken und offene Punkte

1. **Konkurrierende SWR (Forum, Thread 2738013):** trockene Streifen / fehlendes Netz, wenn mehrere SWR bzw. Flüsse um dieselbe Fläche
   konkurrieren. Hier konkurrieren an den Nähten zwei Teilflüsse auf 6–8 m und darunter liegt der versteckte Original-Fluss. Gegenmaßnahmen im
   Skript: Prioritäten 12/11/11 (Talkaskade zeichnet in der Naht), Original versteckt + Komponente unsichtbar. **Nicht belegt:** ob die
   Wasserzone den versteckten Original-Fluss aus Water-Info und Netz wirklich herausnimmt. Falls im Bild die alte Fläche durchscheint:
   `ALT=leeren` hilft nicht (das ist die SWR), dann müsste der Original-Fluss aus der Zone (Breite auf 1 cm aus der Sicherung rückbaubar)
   oder zeitweise gelöscht werden – das macht das Skript bewusst nicht.
2. **Bake-Verknüpfung:** `swr_bake` meldet „N Wasserkörper verknüpft“ – die gebackenen Daten hängen am Wasserkörper. Jeder Teilfluss hat
   genau eine SWR, der Arm hängt an T02. Die alte SWR backt nicht mehr (pausiert, WATER_COMPONENT) → keine Doppelverknüpfung am Original.
3. **Speicher/Zeit:** T01/T02 ≈ 1,5–2,0 Mio. Zellen (2,4–3× heute). Einlaufen 5 min ist eine Annahme aus 2016 × 319; bei Verdacht
   `WARTE=420`. Bei Grafikspeicher-Not `RES=1024`.
4. **Nähte in Becken:** oben liegt das Anschlussbecken nur 389,0–392,9 m; Schnittpunkte 387/393 bei 3-m-Punkten. Beide SWR liefern dort
   Wasser (Deckung in der `NAHT`-Zeile); der Spiegelsprung entscheidet.
5. **Nachfüllen 0,3 je Teil:** die Front muss in jedem Teil von seiner Quelle (Spline-Anfang des Teilflusses, `source_size` 300) aus laufen; die
   Quelle von T01/T02 liegt mitten im Lauf – Cloud-Muster „Quelle = Senke = derselbe Fluss“. Ob das Einlaufen dort 5 min braucht, zeigt der Test.
6. **Spline-Kopie:** Tangenten werden als CUSTOM übernommen (exakte Geometrie), LINEAR bleibt LINEAR. Breiten werden nach dem Setzen
   zurückgelesen (Fehler ab > 1 cm Abweichung → `TEILEN BAUEN FEHLER`, Kette bricht ab, dann `ZURUECK=ja`).
7. **Nach Editor-Neustart** stehen die Raster wieder auf 1×1 bis zum Reset; `status` zeigt dann nur die Vorhersage – die Kette resettet ohnehin je Teil.
8. **Nicht geprüft:** Verhalten von `set_paused`, `set_visibility` und `get_tangent_at_spline_input_key` in 5.8 (im Header bzw. Spline-API
   vorhanden; alle in `try` gekapselt, Fehlschlag → WARNUNG, kein Abbruch).

## 6. Rückweg (Kurzform)

`ZURUECK=ja bash swr/_teilung_kette.sh` → entfernt alle Akteure mit `EL_SWR_TEILUNG`, hebt Etikett/Versteck der alten SWR und des alten
Flusses auf, setzt Quelle/Senke, `resolution_max_axis` 2016, Nachfüllen/remove/source_size und `render_state` (WCBS) aus der Sicherung,
Prioritätswert des Flusses zurück, `rebuild_native_body`. Dann wie bisher: `swr/frisch_reset.py` (LIVE_SIM + Reset), 5 min, Bake
(`_sim_neu.sh`-Teil bzw. `bau_direkt.sh backen bake`), `fluss_swr_speichern.py`. Die Sicherung bleibt liegen (Datum im Inhalt).
