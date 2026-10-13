# Antwort 16h Nachtrag 6d – Coast-Wasser, Steine unter Wasser, übrige Punkte

Stand 13.10.2026. Bezug: `auftraege/16h-nachtrag6d-steine-coast-inventar.md`, Bilder `bilder/swr_p2/coast_wasser_cw.jpg`, `steine_dunkel_sd0_sd4.jpg`,
`endstand_e16.jpg`, `fels_master_repariert_msr.jpg` (6e). Wegen 6e sind alle Bildurteile zu Steinen bis zur Reparatur neu bewertet. Die
Albedo-Messung (`stein_albedo.json`) gilt weiter, weil sie an den echten Texturen lief.

**Kennzeichnung:** [Ferat] = eure Angabe bzw. euer Bild; [Ableitung] = aus Belegen geschlossen; [Annahme] = Gestaltungswert.

## Kurzfazit

1. **Coast-Wasser:**
   - **Keinen Zahlenwert übertragen.** Rauheit (0,02 gegen unsere 0,025), Normalen nah/fern, Fresnel-Potenz 9, River Normal Flatness 0,5 und WPO Flowmap 6 sind praktisch gleich. Coast hat sogar `Sim Velocity Normal Strength` 40 (wir 5).
   - Ruhiger ist Coast, weil die Schalter anders stehen: **Enable River aus**, **Enable Waves an**. Damit fällt die Flowmap-Normalen-Kette weg, die bei uns die Schlieren macht [Ableitung].
   - Für einen Fluss schalten wir River nicht ab: Die Strömung muss lesbar bleiben.
   - **Entscheidung:** E16 bleibt, dazu **V20a** (`ELD_Normal_Nah` 0,35). Nur zur Diagnose ein Speicher-Bild „E16 + Enable River aus“. Bestätigt es die Ursache, kommt danach „Normalen nach Tempo“ (18 §3.1).
   - Absorption von Coast (Türkis) nicht übernehmen, die S6-Farbe bleibt.
2. **Steine unter Wasser:**
   - **Frage 1, eigene Palette:** Keine eigene Palette, sondern die **Nasslinie** (MS2, jetzt gebaut). Die `_Nass`-Kopien braucht es nur noch, bis `M_Master_material` auch eine Nasslinie hat.
   - **Frage 2, Zielhelligkeit:** Y ≈ **0,08** (0,075–0,09), also etwa das 1,4-Fache des Grunds (0,054–0,063). Dann bleiben die Steine als Steine lesbar und leuchten nicht. Faktoren: `SmallStonesPack` × 0,65, `mountain_rock` × 0,35.
   - **Frage 3, Nasslinie für `M_Master_material`:** **ja.** Die Aufteilung nach der Steinmitte reicht an Lippen und Ufern nicht: Dort ragen Steine halb aus dem Wasser, und die 6c-Lippen werden aus diesen Netzen gebaut.
   - **Nie doppelt abdunkeln:** MS2-Nasslinie (`Nass_Albedo` 0,50) und `_Nass`-Kopie (0,55) zusammen ergeben 0,28 × Albedo, also Y ≈ 0,035. Das ist zu dunkel.
3. **Übriges:**
   - Die Aufteilung der 9 840 Steine nach dem **SWR-Spiegel** ist richtig, auch künftig: Der Plan-Spiegel schneidet Stufen schräg.
   - RA auf dem See: zuerst der Bach. Die Prüfliste für später steht in §3.
   - `Caustics` ohne Wirkung: abgehakt. V20c streiche ich aus der nahen Liste.

## 1. Coast & Dunes gegen `MI_EL_SWR_Klar` (E16)

| Wert | Coast | wir (E16, MI-Dump) | Folge |
|---|---|---|---|
| Water Roughness | 0,02 | 0,025 | praktisch gleich; E16 bleibt |
| Default Near / Distant / B | 0,25 / 0,3 / 0,25 | 0,25 / 0,3 / 0,25 | gleich |
| Far Normal Fresnel Power | 9 | 9 | gleich |
| River Normal Flatness, WPO Flowmap | 0,5 / 6 | 0,5 / 6 (MI-Dump) | gleich |
| Sim Velocity Normal Strength | 40 | 5 | Coast ist **höher** und trotzdem ruhiger → bei Coast wirkt dieser Zweig nicht |
| Enable River / Enable Waves | **aus / an** | an / aus | **der Unterschied** [Ableitung] |
| Absorption, Streuung, Albedo | Türkis (10/150/350) | S6 braun | nicht übernehmen |

**Warum ruhiger** [Ableitung]:
- Mit `Enable River` aus fallen die Flowmap-Normalen weg. Das sind die Schlieren, die die SWR-Strömung in die Oberfläche zieht.
- `Enable Waves` gibt ruhige, gleichmäßige Wellen-Normalen.
- Auf der SWR sähe das ruhig aus, aber ohne Fließrichtung. Rinnen und Kaskaden würden wie ein Teich wirken; das widerspricht K5 aus 18 („Rinnen gerichtet“).

**Entscheidung:**
1. E16 bleibt.
2. V20a bauen (in Arbeit [Ferat]) mit `ELD_Normal_Nah` 0,35. Es flacht nur die Nähe ab (≤ 3 m), dort stören die Schlieren am meisten.
3. Diagnose, nur im Speicher, ein Bild: „E16 + Enable River aus“ an t430/t500.
   - Wird es so ruhig wie Coast, ist die Ursache belegt.
   - Der nächste Hebel ist dann **„Normalen nach Tempo“** (18 §3.1): Becken fast glatt, Rinnen kräftig. Er wird nicht global abgeschaltet.
4. `River Normal Flatness` 0,5 → 0,7 nur als Einzeltest, falls V20a nicht reicht.

## 2. Steine unter Wasser (Fragen 1–3, neu bewertet nach 6e)

**Rechnung** (Albedo Y aus `stein_albedo.json`, echte Texturen):

| Netz | Y trocken | Faktor für Ziel 0,08 | bisher | Material |
|---|---|---|---|---|
| `SM_SmallStonesPack_*` | 0,125 | **0,65** | 0,55 (`_Nass`) bzw. 0,50 (MS2 `Nass_Albedo`) | `M_EL_Fels_MS2` mit Nasslinie |
| `SM_mountain_rock_small_01_*` | 0,229 | **0,35** | 0,30 (`_Nass`) | `M_Master_material`, ohne Nasslinie |
| Platten (Y 0,16–0,18) | 0,17 | 0,47 | – | Nasslinie, sofern MS2 |

- **Ziel 0,08 statt 0,069:**
  - Grund unter Wasser 0,054–0,063 [Ferat, BaseColor S6]. Steine mit 0,069 verschwinden fast im Grund. Mit 0,08 sind sie gut 1,3- bis 1,5-mal heller, also als Steine lesbar, aber keine Flecken.
  - Im Witcher-Bild (18) sind Bachsteine dunkle, aber erkennbare Formen [Ableitung].
- **Wenn V20b gebaut wird** (`Color Scale Behind Water` 0,8): Alle Faktoren durch 0,8 teilen. Dann gilt `SmallStonesPack` 0,8 und `mountain_rock` 0,44.
- **„Orange unter braunem Wasser“ (SD1):** Das Bild zeigte noch die Pflanzentextur. Bitte nach der Reparatur neu ansehen. Bleibt ein Orangeton, `Nass_Entsaettigung` 0,3 → 0,45.

**Frage 1, eigene Palette oder Abdunkeln:** **Abdunkeln über die Nasslinie.**
- Für MS2-Steine (SmallStonesPack, NordicBoulder, MossyForestBoulder, TundraRockyGround):
  - `Nass_Albedo` 0,65 in `MI_EL_SmallStonesPack_01`.
  - Die `_Nass`-Kopie auf die normale Instanz zurückstellen bzw. ihre Helligkeit auf 1. Sonst wird doppelt abgedunkelt.
- Eine eigene Palette brauchen wir nicht. Die Formen sind gut, nur die Helligkeit stimmt nicht.

**Frage 3, Nasslinie für `M_Master_material`:** **ja**, als Kopie wie MS2 (`MF_EL_Nasslinie` + `MF_EL_Spiegelhoehe`).
- Grund: Die Bachdekor-Aufteilung nach der Steinmitte macht einen Stein ganz nass oder ganz trocken. An Lippen, an der Uferstufe und bei den 6c-Lippenblöcken ragen Steine halb heraus.
- Bis dahin:
  - `MI_EL_Nass_mountain_rocks_small_01` Base Brightness 0,30 → **0,35**
  - im Bettplan `mountain_rock_small` nicht an Lippen setzen (6e §2)

**Übergang nach dem neuen Bettplan:** Der Bachdekor-Planer rechnet neu. Dann die Aufteilung wiederholen, aber nur für Netze ohne Nasslinie.

## 3. Übrige Punkte

- **9 840 `_Nass`-Steine:**
  - Gute Sofortlösung, und die Zuordnung über den gebackenen SWR-Spiegel ist die richtige Wahl.
  - Dass die Steinmitten im Median 0,39 m unter dem Spiegel liegen, zeigt das Überlaufen aus 6b. Nach dem Bettplan sinkt der Anteil.
  - Die 917 `FT_EL_UF_*`- und 82 `FT_EL_HEID_*`-Steine dunkelt die Nasslinie automatisch mit ab, weil sie dieselbe MI nutzen. Das ist gewollt, sie liegen im Bett.
- **SWR-Spiegel statt Plan-Spiegel:** richtig.
  - Für Nässe, Steine und Lagen künftig immer den gebackenen Spiegel nehmen.
  - Der Bettplan liefert seinen Spiegel nur für die Spline-Z (`spiegel_je_m`) und für die Gestalt.
- **RA auf dem Elfenwald-See (To-do, Bach zuerst).** Zu prüfen wäre:
  1. Liegt die Unsichtbarkeit am Fluss an der Tiefe (Bach 0,47 m, See 1,4 m)? Test: RA auf einem neuen Kolk von 1 m nach dem Bettplan.
  2. Wenn nicht: UV bzw. Maske auf dem Flussnetz der Water Zone.
  3. Shader-Kosten gegen `M_Eldarien_Wasser_Schaum8`.
  4. Der weiße Uferstreifen am See ist das V12-Kiesufer, kein Wasserfehler. Ob es am See schmaler sein soll, entscheiden wir mit dem See.
- **`Caustics` ohne Wirkung:** abgehakt.
  - Passt zur Doku-Aussage, dass `Color Scale Behind Water` keine Kaustik projiziert (N6 §2.2).
  - V20c (Kaustik) streiche ich aus der nahen Liste.

## Was fehlt bis Witcher 4 (für diese Punkte)

Messlatte nach 6e: dichte Vegetation bis an die Kante, Wind, weiches Licht, klare Wasserformen.
Belegt ist die Techdemo nur über Suchauszüge, Quellen in 6e.

Nach Wirkung:
1. **Steine:** nass-dunkel, aber lesbar (Y 0,08), mit Nasslinie auch an `M_Master_material`; Algen unter der Linie, Moos oben (Material-Skizze 6e §3).
2. **Oberfläche:** ruhig nah, gerichtet in den Rinnen. V20a, danach „Normalen nach Tempo“; kein Abschalten von River.
3. **Kante:** Bewuchs bis ans Wasser. Im Bettplan als Ergänzung gerechnet (6e §3: 279 Kantengras, 432 Moos, 65 Farne).
4. **Licht:** Schatten im Einschnitt; Distance Fields für die neuen Blöcke.
5. **See:** Er bleibt bis nach dem Bach auf dem Stand „RA sichtbar, ruhiger Spiegel“.
