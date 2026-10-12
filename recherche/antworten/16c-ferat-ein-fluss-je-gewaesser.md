# Antwort zu Auftrag 16c – Ein Fluss je Gewässer (fluss_sim v3), eine SWR je Gewässer, T2-10

Stand 12.10.2026. Grundlage sind Auftrag 16c mit den Nachträgen 17:45 und 18:15, der Nachtrag 17:05 in 16b, die Bilder
`bilder/swr/c2_wcbs_klar.jpg` und `c2_aufloesung_512_1024_2048.jpg`, die Antworten 16, 16a und 16b sowie `skripte/fluss_sim/`.

**Quellenlage:** `dev.epicgames.com` und `forums.unrealengine.com` sind aus der Cloud weiter nicht erreichbar (DNS-Fehler bei
WebFetch). Web-Belege stammen aus **Suchmaschinen-Auszügen**. Kennzeichnung: [Doku] Epic-Doku/API (Auszug) · [Forum] (Auszug) ·
[Test 16c] eure Messung · [Projekt] eigene Daten · [Ableitung] · [vermutlich] Name oder Wirkung nicht belegt.

## Kurzfazit

- **Export v3 ist fertig** (Commit `3ce41a5`). Je Gewässer gibt es **genau einen `WaterBodyRiver`** von der Quelle bis zur
  Mündung, über alle Fälle und Feldgrenzen hinweg.
  - Die 195 Welt-Läufe (27 Feld-Stücke aus `wasser_welt.json`, 168 Bäche) werden an ihren Enden zu **154 Gewässern**
    verkettet. Dazu kommen 42 Sehens-Bäche, zusammen **196 Gewässer** mit 45,8 km.
  - Beispiel: `F_ERLENBACH` (1 007 m) besteht aus 7 Läufen; C2 liegt darin bei s 17,4–220,6 m.
  - Jede Stufe hat einen Punkt an der Lippe (Oberwasser) und einen am Fuß (Unterwasser), 2 074 Stufen. Die Abschnitte gibt
    es nur noch als Bereiche (`s_m` mit Rolle).
- **Mündungen:** Meer 55, Bach 61, Fluss 13, See 23, versickert 19, Wasserfall 1, offen 24.
  - Zusammenflüsse (74) sind Mündungen. Der Nebenlauf endet im Hauptlauf, und der Hauptlauf führt ihn unter `zufluesse`.
  - 23 Mündungen haben eine Lücke von 3–25 m in den Weltdaten (`luecke_m`).
- **SWR nach eurem Nachtrag 17:45:** je Gewässer **eine** SWR mit Rechteck, Auflösung (Zielzelle Bach 0,25 m, Fluss 0,35 m)
  und Zelle, Auflösung höchstens 2048.
  - **188 von 196 Gewässern kommen mit einer SWR aus.**
  - Nur 8 sind größer als ≈ 614 m (Bach) bzw. 717 m (Fluss). Sie werden für die Simulation in 23 lange Stücke geteilt.
    Geteilt wird nach kleinster Rechteckfläche und nie an einer Stufe.
  - Auflösungen: 106 × ≤ 512, 56 × 513–1024, 49 × 1025–2048. Zelle im Median 0,244 m.
- **Prüfer v3: 0 FEHLER, 0 WARNUNG, 61 HINWEIS.** Zwei Läufe sind byte-gleich (182 Dateien). Alle 10 Gegenproben ergeben
  FEHLER.
- **Recherche Punkt 3:**
  - Eine Eigenschaft, mit der man den Bereich einer SWR auf einen Teil des Flusses begrenzt, ist **nicht belegt**. Gemessen
    habt ihr: Der Bereich ist das Rechteck um die Quell-Flüsse.
  - Ein Forenfall zeigt außerdem: Zwei gebackene SWR, die sich berühren, verlieren an der Verbindung das Wassernetz. Der
    Rat dort lautet: eine SWR mit mehreren Flüssen, nicht umgekehrt [Forum].
  - Für die 8 langen Gewässer ist die Naht deshalb das Hauptrisiko. Der Testplan (Abschnitt 4) klärt das in drei Schritten.
- **T2-10: Nein.** Kein Sehens-Bach liegt über 655 m. Der höchste ist `gletscher_05_die_waechte` Mühlenbach mit **307,1 m**.
  Das höchste Sehens-Wasser überhaupt ist die Wasserfall-Kante `fjord_02` mit 361,2 m. Im Frost liegt alles unter 44 m. Im
  Gelände der SWR-Rechtecke steht nichts über 332 m.
- **Schaum flockig:** Feinere Zellen helfen; euer 1024-Bild zeigt es. Mit der neuen Regel liegen 189 von 200 Bach-SWR bei
  ≤ 0,25 m. Dafür muss **kein** zusätzliches Gewässer geteilt werden (Zwischenregel bei 512: 66 Gewässer, 570 SWR).

## 1. Format v3

### 1.1 Was sich gegenüber v2 ändert

| Teil | v2 (16b) | **v3 (16c)** |
|---|---|---|
| Gewässer | Strecke = ein Lauf je Feld bzw. Bach (177) | **Quelle bis Mündung**, Läufe verkettet (196) |
| `WaterBodyRiver` | je SWR-Einheit (249) | **genau einer je Gewässer** (196) |
| Abschnitte | Unterteilung + Rückfall-River | nur **Bereiche** (`bereiche[].s_m`, `rolle`) |
| Stufe in der Spline | Lippen-Anker, Punkte ≥ 2 m | **Lippe + Fuß** je Stufe (`LINEAR`), dazwischen 2–4 m (roh 5–10 m) |
| SWR | je Einheit, ≤ 512, Zelle 0,35/0,5 m | **eine je Gewässer**, ≤ 2048, Zelle 0,25 (≤ 0,30)/0,35 m; Teilung nur bei sehr großem Rechteck |
| Mündung | – | `muendung` (Art, Ziel, Punkt), `anfang`, `zufluesse` |
| Kacheln (`sim_bereiche`) | Unterteilung | entfallen |
| Back-Liste | je Einheit (`back_liste_v2`) | je SWR-Bereich (`back_liste_v3`, mit `punkt_index`) |

Unverändert bleiben Fall-Einträge (Vorhang-Regel, Kaskadennetz-Bereich, Schaumobjekte, Effekte), Wasser-Kollision,
`ohne_wasser_kollision`, Hindernis-Akteur und die Fingerabdruck-Formel. Die Vorhänge tragen jetzt
`vorhang_status: "wartet"`.

### 1.2 Beispiel-JSON (gekürzt aus `antworten/fluss_sim/gewaesser/F_ERLENBACH/fluss_sim.json`)

```json
{"format": "fluss_sim_v3", "regeln_version": 3,
 "gewaesser": [{"id": "F_ERLENBACH", "kategorie": "welt", "art": "fluss", "laenge_m": 1006.7,
   "laeufe": [{"id": "F_ERLENBACH_1_C2", "herkunft": "roh", "s_m": [0.0, 17.23], "gekuerzt_m": [0.0, 11.74]},
              {"id": "F_ERLENBACH_1V_C2", "herkunft": "plan", "feld": "C2", "s_m": [17.4, 220.56], "s_quelle_m": [0.0, 203.16],
               "quelle": {"plan": "gefaelle/F_ERLENBACH_1V_C2/plan.json"}, "anschluss_oben": "ueberlappung", "swr_typ": "bach"},
              {"id": "F_ERLENBACH_2_C2", "s_m": [220.57, 412.66], "abstuerze_entfallen": ["F_ERLENBACH_2_C2_s1_S01_T1"]},
              "… 2_C3, 2_D3, 2V_D3, 3_D3"],
   "anfang":   {"art": "quelle", "punkt_cm": [-171943.9, -241121.6, 10395.2]},
   "muendung": {"art": "meer", "ziel": "meer", "abstand_m": 37.62, "punkt_cm": [-154268.1, -149865.4, 158.2], "stufe": 0},
   "zufluesse": [{"gewaesser": "B_R3_K10_TUNDRA_01", "art": "bach", "s_m": 376.42, "swr_bereich": "F_ERLENBACH_T00"}, "… 3"],
   "water_body": {"id": "WBR_F_ERLENBACH", "klasse": "WaterBodyRiver", "affects_landscape": false, "overlap_material_priority": 10,
     "spline": {"s_m": [0.0, 1006.7],
       "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
       "punkte":      ["…", [-172434.3, -238669.5, 10079.2, 2584.6, 111.3, 300.0],
                            [-172505.0, -238470.5, 10043.5, 2500.1, 194.6, 240.0],
                            [-172522.1, -238423.5,  9953.5, 2480.1, 215.4, 150.0], "…"],
       "punkte_s_m":  ["…", 25.29, 27.40, 27.90, "…"],
       "punkt_typen": ["…", "CURVE_CLAMPED", "LINEAR", "LINEAR", "…"],
       "punkt_rollen":["…", "rampe", "lippe", "fuss", "…"], "tangenten_cm": ["…"]}},
   "abstuerze": [{"id": "F_ERLENBACH_1V_C2_s1_S01_T2", "lauf": "F_ERLENBACH_1V_C2", "s_lippe_m": 31.65, "s_fuss_m": 32.15,
                  "fall_m": 1.27, "z_oben_cm": 9946.0, "z_unten_cm": 9818.7, "punkt_lippe": 15, "punkt_fuss": 16}, "…"],
   "bereiche": [{"id": "F_ERLENBACH_A03", "s_m": [43.06, 50.34], "rolle": "becken",
                 "oben_fall": "…_S01_T5", "unten_fall": "…_S02_T2", "abstuerze_innen": ["…_S02_T1"],
                 "becken": [{"s_m": [43.06, 48.13], "spiegel_cm": [9474.2, 9464.1]}, "…"], "swr_bereiche": ["F_ERLENBACH_T00"]}, "…"],
   "faelle": [{"id": "F_ERLENBACH_1V_C2_s1_S04", "fall_m": 4.67, "s_lippe_m": 70.05, "s_fuss_m": 70.55, "punkt_lippe": 39,
               "punkt_fuss": 40, "bereich_oben": "F_ERLENBACH_A06", "bereich_unten": "F_ERLENBACH_A07", "vorhang": true,
               "vorhang_status": "wartet (Ferat 16c …)", "…": "wie v2"}, "…"],
   "swr_bereiche": [
     {"id": "F_ERLENBACH_T00", "s_m": [0.0, 468.88], "s_sim_m": [0.0, 472.88], "punkt_index": [0, 260],
      "rechteck_cm": [-180504.0, -242771.6, -167447.0, -196865.4], "rechteck_m": [130.57, 459.06],
      "naht_unten": {"art": "becken", "s_m": 468.88, "ueberlappung_m": 8.0, "ueberlappung_s_m": [464.88, 472.88]},
      "geteilt": true,
      "swr": {"id": "SWR_F_ERLENBACH_T00", "typ": "bach", "zelle_ziel_m": 0.25, "zelle_max_m": 0.3, "achse_m": 459.06,
              "resolution_max_axis": 1856, "zelle_m": 0.247, "raster_erwartet": [528, 1856],
              "source_river_water_bodies": ["WBR_F_ERLENBACH"], "sink_river_water_bodies": ["WBR_F_ERLENBACH"],
              "bottom_contour_actors": ["WH_F_ERLENBACH_T00"], "match_spline": "lokal testen",
              "begrenzung": {"art": "rechteck_teil", "rechteck_cm": ["…"]}},
      "hindernis_akteur": {"id": "WH_F_ERLENBACH_T00", "…": "wie v2"}, "fingerabdruck": "34f419d2…"},
     {"id": "F_ERLENBACH_T01", "s_m": [468.88, 1006.7], "s_sim_m": [464.88, 1006.7], "rechteck_m": [201.22, 539.86],
      "swr": {"resolution_max_axis": 2048, "zelle_m": 0.264, "…": "…"}}]}]}
```

Ein ungeteiltes Gewässer (188 von 196) hat genau einen Eintrag in `swr_bereiche`. Dessen `id` ist die Gewässer-ID; SWR und
Hindernis-Akteur heißen `SWR_<gewaesser>` und `WH_<gewaesser>`, dazu kommen `match_spline: true` und
`begrenzung.art = "rechteck_um_fluss"`. Karsee (`sehens/bergwald/bergwald_06_karsee`):

| Gewässer | Länge | Anfang → Mündung | Fälle (Vorhang) | Rechteck | Auflösung | Zelle |
|---|---|---|---|---|---|---|
| `…_karsee_abfluss` | 45,2 m | See `karsee` → **offen** (Sehens nennt Netz `R_M2_P0__WASSER`, kein Lauf ≤ 15 m) | 12 (8) | 44,1 × 14,1 m | 192 | 0,230 m |
| `…_zulauf_sued` | 21,2 m | Quelle → See `karsee` | 6 (6) | 18,5 × 16,9 m | 96 | 0,192 m |
| `…_zulauf_west` | 20,4 m | Quelle → See `karsee` | 6 (6) | 23,2 × 3,8 m | 96 | 0,242 m |

### 1.3 Regeln (Zahlen in `skripte/fluss_sim/fluss_sim_regeln.json`, Version 3)

**Läufe verketten (ein Gewässer):**
- Läuft ein Lauf N dort weiter, wo P endet, gehören beide zu einem Gewässer. Das gilt in zwei Fällen:
  - **Anschluss:** Das Ende von P liegt ≤ 8 m vom Anfang von N, und N beginnt nicht höher als P endet (+ 0,5 m).
  - **Feldgrenze:** P und N überlappen 12–30 m. Das Ende von P liegt ≤ 1 m neben N bei s ≤ 40 m, und umgekehrt.
- An einer Überlappung wird das Stück **ohne** Gefälle-Plan gekürzt, sonst das untere.
- Gefunden: 23 Anschlüsse und 18 Feldgrenzen. 26 Gewässer bestehen aus 2–7 Läufen.
- Benannt werden Flüsse nach dem gemeinsamen Namensteil (`F_ERLENBACH`, `F_ELFENFLUSS`, `F_HAUPTFLUSS_3`), Bachketten nach
  ihrem obersten Lauf.

**Mündung** (Reihenfolge):
1. **Ausdrücklich:** Sehens-Feld `muendung` oder R2-Feld `anschluss.ende`, wenn das Ende ≤ 15 m neben dem Ziel liegt.
2. **Fluss/Bach:** Das Ende liegt ≤ halbe Breite + 3 m neben der Mittellinie eines anderen Laufs und höchstens 1 m unter
   dessen Spiegel.
3. **See:** Umriss eines Welt- oder Sehens-Sees + halbe Breite + 5 m.
4. **Meer:** Meer-Raster ≤ halbe Breite + 10 m. Oder das Ende liegt ≤ 2 m hoch und das Meer ≤ 150 m entfernt (der Bach
   endet am Strand).
5. **Nah:** Lauf oder See ≤ 25 m neben dem Ende → Mündung mit `luecke_m`.
6. **Welt-Wasserfall** ≤ 120 m, sonst **versickert** (Sehens) bzw. **offen**. Bei `offen` stehen der nächste Lauf und der
   nächste See dabei.

**Zusammenfluss:**
- Der Nebenbach **endet** im Hauptfluss. Seine Spline reicht bis ins Wasser des Hauptlaufs (die Bäche sind dort schon 5–7 m
  verlängert, `verlaengert_m`).
- Senkt der Gefälle-Plan des Hauptlaufs sein Becken (`plan.zufluesse`), wird das Endstück des Nebenbachs mit abgesenkt.
  Das betrifft 8 Gewässer; es steht in `muendung.endstueck_angepasst`.
- Der Hauptlauf führt den Nebenlauf unter `zufluesse` (s, SWR-Bereich, Water Body). Seine SWR führt ihn unter
  `swr_bereiche[].zufluesse` als Hinweis.
- `overlap_material_priority` = 10 − Stufe im Mündungsbaum: Hauptläufe 10 (122), Zuflüsse 9 (54), dann 8 (16), 7 (4). Der
  Hauptlauf zeichnet damit über dem Ende des Nebenlaufs.

**Spline:**
- Je Stufe ein Punkt an der Lippe (z = Oberwasser) und einer am Fuß (z = Unterwasser), beide `LINEAR`, dazwischen kein Punkt.
  Das gilt für jeden Absturz aus Plan bzw. Sehens, auch für Kaskaden-Teilstufen und Schnellen.
- Fuß ≥ Lippe + 0,1 m. Sonst liegen die Punkte im Abstand 2–4 m, auf rohen Läufen 5–10 m.
- Becken-Punkte liegen auf dem Becken-Spiegel. Wo Sehens-Linien zwischen zwei Stufen Gefälle haben, heißt die Rolle `rinne`.
- Ergebnis: 17 105 Punkte; 2 074 Lippen und 2 074 Füße; kein Punkt musste sich Fuß und Lippe teilen.

**SWR (Nachtrag 17:45):**
- Zielzelle je Lauf: Bach 0,25 m (höchstens 0,30 m), Fluss 0,35 m. Bach heißt: Abstürze im Plan, Median der Breite < 15 m
  oder Sehens-Bach. Ein SWR-Bereich, der einen Bach-Lauf berührt, gilt als Bach.
- `resolution_max_axis` = ⌈längste Rechteckseite / Ziel / 32⌉ × 32, höchstens 2048.
- **Teilung** nur, wenn das Rechteck des ganzen Flusses bei 2048 die Höchstzelle übersteigt:
  - möglichst wenige Stücke; unter gleich vielen die mit der kleinsten Summe der Rechteckflächen;
  - Naht ≥ 5 m von jeder Stufe und ≥ 50 m vom Ende;
  - Nachbarstücke überlappen 8 m.

## 2. Zahlen (2-m-Daten, alle Gewässer)

| | Gewässer | Länge km | Läufe | SWR | mit **einer** SWR |
|---|---|---|---|---|---|
| Welt-Flüsse | 9 | 11,1 | 27 | 20 | 5 |
| Welt-Bäche | 145 | 32,9 | 168 | 149 | 141 |
| Sehens-Bäche | 42 | 1,8 | 42 | 42 | 42 |
| **Summe** | **196** | **45,8** | **237** | **211** | **188** |

- **Läufe:** 98 mit Gefälle-Plan, 97 roh. Neu gegenüber v2 sind 60 flache Bäche, die in keiner der 161 Strecken lagen. Sie
  gehören jetzt zu ihren Gewässern bzw. sind eigene Gewässer.
- **Entfallene Stufen:** 5 Stufen in Feldgrenz-Überlappungen. Dort liegen zwei Pläne übereinander, und der obere behält das
  Stück (`F_ERLENBACH_2_C2`: 1, `F_HAUPTFLUSS_3_C5`: 2, `F_ELFENFLUSS_3_G4`: 2). Siehe Rückfrage 3.
- **Mündungen nach Art:**

  | Art | Welt | Sehens | Summe |
  |---|---|---|---|
  | Meer | 55 | – | 55 |
  | Bach (Zusammenfluss) | 56 | 5 | 61 |
  | Fluss (Zusammenfluss) | 12 | 1 | 13 |
  | See | 8 | 15 | 23 |
  | versickert | – | 19 | 19 |
  | Wasserfall (`F_HAUPTFLUSS_1` → WF_K1) | 1 | – | 1 |
  | offen | 22 | 2 | 24 |

  - **Herkunft der Zuordnung:** 47 aus R2-`anschluss`, 42 aus Sehens-Daten, 107 geometrisch (55 Meer-Raster, 20 „nah“ mit
    Lücke, 32 übrige).
  - **Lücken:** 23 Mündungen mit `luecke_m` 3–25 m.
  - **Offen** (Lücke > 25 m oder Bach endet tiefer als der Fluss daneben): z. B. `B_R_M1_P0_01/02` enden 6 m unter dem
    Spiegel von `F_HAUPTFLUSS_3`; `F_HAUPTFLUSS_2` endet in B4 ohne Anschluss; dazu der Karsee-Abfluss. Die Liste steht in
    `zusammenfassung.json` (`muendungen_offen`).
  - **Anfang:** 168 Quelle, 25 Seeabfluss, 3 Wasserfall (`F_HAUPTFLUSS_1` und `_2` an WF_K1, `F_ELFENFLUSS` unter WF_K8).
- **Längen:** Median 136 m, längstes `F_HAUPTFLUSS_3` mit 3 856 m.

  | ≤ 50 | ≤ 100 | ≤ 130 | ≤ 180 | ≤ 256 | ≤ 500 | ≤ 1 000 | ≤ 2 000 | > 2 000 m |
  |---|---|---|---|---|---|---|---|---|
  | 34 | 42 | 20 | 23 | 30 | 32 | 9 | 3 | 3 |

  Längste Rechteckseite je Gewässer: Median 122 m; 9 über 614 m (davon `F_CANYONBACH` 651 m als Fluss ungeteilt), 2 über 2 km.
- **SWR (Regel 17:45):** 211 SWR-Bereiche (200 Bach, 11 Fluss). **188 Gewässer mit einer SWR, 8 geteilt.**

  | Gewässer | Länge | Rechteck ganz | Zelle bei 2048 | Stücke | Zellen der Stücke |
  |---|---|---|---|---|---|
  | `F_HAUPTFLUSS_3` | 3 856 m | 3 498 × 1 070 m | 1,71 m | 6 | 0,30 / 0,30 / 0,35 / 0,35 / 0,35 / 0,35 |
  | `F_DSCHUNGELFLUSS` | 2 867 m | 963 × 1 770 m | 0,86 m | 3 | 0,35 |
  | `F_ELFENFLUSS` | 2 213 m | 2 024 × 530 m | 0,99 m | 4 | 0,25 / 0,30 / 0,30 / 0,30 |
  | `B_R_P3_P0_02` | 1 295 m | 981 × 506 m | 0,48 m | 2 | 0,25 / 0,25 |
  | `B_K1_WASSERFALL_WEST_03` | 1 040 m | 742 × 330 m | 0,36 m | 2 | 0,30 / 0,25 |
  | `F_ERLENBACH` | 1 007 m | 301 × 968 m | 0,47 m | 2 | 0,25 / 0,26 |
  | `B_R_P3_P0_04` | 945 m | 819 × 217 m | 0,40 m | 2 | 0,25 / 0,25 |
  | `B_R_P4_M2_04` | 744 m | 636 × 206 m | 0,31 m | 2 | 0,26 / 0,25 |

  - Alle 15 Nähte liegen in einem Becken.
  - **Auflösung:** 106 × ≤ 512, 56 × 513–1024, 49 × 1025–2048, keine darüber (Median 512).
  - **Zelle:** Bach 8 × ≤ 0,20, 181 × 0,20–0,25, 11 × 0,25–0,30 m; Fluss 11 × 0,30–0,35 m.
  - **Rechteck** je SWR: längste Seite im Median 129 m, höchstens 716 m. Zusammen 79 Mio. Zellen.
- **Varianten** (wie viele Gewässer müssten geteilt werden?):

  | Variante | geteilt | eine SWR | SWR gesamt | ≤ 512 / 1024 / 2048 |
  |---|---|---|---|---|
  | **Regel: Bach 0,25 (max 0,30), Fluss 0,35, bis 2048** | **8** | **188** | **211** | 106 / 56 / 49 |
  | Bach fest 0,25, Fluss 0,35 | 11 | 185 | 216 | 106 / 58 / 52 |
  | alles 0,25 | 12 | 184 | 220 | 105 / 59 / 56 |
  | Bach 0,30, Fluss 0,35 | 8 | 188 | 211 | 120 / 53 / 38 |
  | Zwischenregel 16c (bis 512, Bach 0,35, Fluss 0,5) | 66 | 130 | 570 | 570 / – / – |

- **Fälle und Kollision** wie v2: 765 Fälle, 170 mit Vorhang (wartet), Schaumobjekte 170 / 784 / 273
  (Teppich / Straße / Kehrwasser).
  - 21 715 Kollisionseinträge, davon 21 582 eindeutig; 1 368 überspannt.
  - **141 Hindernis-Akteure** (je SWR) mit 20 429 Instanzen und 1 151 Akteuren mit Tag; 70 SWR haben kein Hindernis.
  - Das passt zu Ferats Nachtrag 18:15 Punkt 3: Hindernis-Akteur je Gewässer statt je Kachel.
- **Prüfer v3:** 0 FEHLER, 0 WARNUNG, 61 HINWEIS (24 × Mündung offen, 23 × Mündung mit Lücke, 8 × geteilte Simulation,
  7 × Fuß am Gewässerende, 1 × „alle 195 Welt-Läufe in genau einem Gewässer“, 1 × Determinismus).
  - Neu geprüft werden:
    - genau ein Fluss je Gewässer, jeder Lauf genau einmal;
    - Spline durchgehend und nie steigend;
    - jede Stufe mit Lippen- und Fußpunkt (Rolle, s, z = Ober-/Unterwasser ± 2 cm), Stufen aus der Quelle neu gezählt;
    - Bereiche lückenlos und von SWR-Bereichen abgedeckt;
    - Auflösung ≤ 2048 und = Regel, Zelle ≤ Höchstwert + 0,005 m, Teilung nur wenn nötig;
    - Mündungsziel, Mündungspunkt und `zufluesse`;
    - Determinismus.
  - **Gegenproben** an `F_ERLENBACH`, alle FEHLER mit Exit 1: steigende Spline, Stufe ohne Fußpunkt, Fußpunkt auf
    Oberwasser, Lücke zwischen SWR, Auflösung 4096, Zelle 0,45 m, zweiter Fluss als Quelle, Lauf doppelt, Naht an einem Fall,
    Grundriss-Sprung.

## 3. Schaum flockig (Punkt 4)

- **Feinere Zellen verbessern das.** Der Schaum ist ein Zellwert der Simulation; das Material liest ihn bilinear. Ein
  Schaumfleck ist darum mindestens etwa 2 Zellen groß [Ableitung].
  - Bei 0,35 m sind das ≈ 0,7 m.
  - Bei 0,25 m sind es ≈ 0,5 m, bei halber Zellfläche.
  - Euer Bild `c2_aufloesung_512_1024_2048.jpg` zeigt das: bei 1024 (≈ 0,17 m an C2) klar feinere Flocken und Streifen statt
    Marmor-Flächen.
  - Das 2048-Bild war nach 45 s noch nicht eingelaufen und ist daher kein Vergleich.
- **Was die Regel dafür bedeutet:**
  - 189 der 200 Bach-SWR liegen bei ≤ 0,25 m, die übrigen 11 bei 0,25–0,30 m. Das sind die großen Bach-Rechtecke über 512 m.
  - Die Zielzelle 0,25 m erzwingt **kein** zusätzliches geteiltes Gewässer, denn die Höchstzelle 0,30 m begrenzt nur bei
    > 614 m.
  - Wer 0,25 m auch als Höchstwert will, teilt 3 Gewässer mehr (11 statt 8, 216 SWR).
  - Bei der Zwischenregel (512) wären es 66 geteilte Gewässer gewesen.
- **Kosten:** Sie fallen nur beim Backen an (1024: 6,3 ms, 2048: 9,7 ms live [Test 16c]). 2048-SWR brauchen länger, bis sie
  eingelaufen sind; vor dem Backen genug Laufzeit geben (Testplan T5).
- **Material:** Die Schaumleiter aus 16b (`Foam Boost`, `Foam powr`, `Sim Foam Scale`) bleibt gültig. `Sim Foam Scale` ist
  vermutlich die Kachelgröße der Schaumtextur. Bei feinerer Zelle lohnt eine Gegenprobe 350 → 250 [vermutlich].

## 4. Recherche Punkt 3 und Testplan

### 4.1 Bereich einer SWR begrenzen

- **Gemessen** [Test 16c]: Der Simulationsbereich ist das achsparallele Rechteck um die Quell-Flüsse. C2 ergab
  `sim_res` 255 × 512 und 33,1 cm (≈ 84 × 170 m). Der Export rechnet genau so (längste Rechteckseite / Auflösung). Damit
  ist 16b-Rückfrage 1 geklärt: Die 0,35 m waren das Rechteck des 179-m-Kaskadennetzes; v2 nahm den ganzen 203-m-Lauf.
- **Belegte Eigenschaften** von `ShallowWaterRiverComponent` aus 16a/16b [Doku, Python 5.5]: `resolution_max_axis`,
  `source_river_water_bodies`, `sink_river_water_bodies`, `use_capture`, `bottom_contour_actors`, `bottom_contour_tags`,
  `render_state`, `baked_sim_material`.
  - Die C++-Seite nennt dazu `bMatchSpline` (Python `match_spline`). Was es genau tut, steht im Auszug nicht [Doku, Auszug].
- **Nicht belegt:** eine Eigenschaft für Bounds, „Source Size“ oder Ausdehnung des Bereichs. Die Suche nach
  `SourceSize`/Bounds in der API brachte nichts. Denkbar ist, dass bei `match_spline = False` die Akteur-Transformation (Lage,
  Skalierung) oder eine eigene Größe den Bereich setzt [vermutlich].
  - Wenn das nicht geht, decken zwei SWR mit demselben Fluss beide **das ganze Rechteck** ab. Die Teilung brächte dann keine
    feinere Zelle.
- **Zwei SWR an einem Ort** [Forum, Auszug, japanischer Thread]:
  - Fall: zwei SWR an einer Flussverzweigung. Live ist alles in Ordnung. **Nach dem Backen** (WCBS) verschwindet an der
    Verbindung das Wassernetz.
  - Ohne die zweite SWR tritt der Fehler nicht auf.
  - Rat im Thread: **eine** SWR mit **mehreren** `WaterBodyRiver`. Die gebackenen Oberflächendaten liegen je SWR, und jede
    hält nur das Wasser in ihrem eigenen Bereich.
- **Folgerung für uns** [Ableitung]:
  - Der Normalfall (188 Gewässer) ist sicher: ein Fluss, eine SWR.
  - Für die 8 langen Gewässer ist die Naht das Risiko. Der eine `WaterBodyRiver` hält vermutlich nur **einen** Verweis auf
    gebackene Daten; dann gewinnt die zuletzt gebackene SWR, und das andere Stück ist leer.
  - Rückfall 1 für diese 8: den Fluss nur dort an der Naht in zwei `WaterBodyRiver` teilen (v2-Verkettung in einem Becken).
  - Rückfall 2: gröbere Zelle für die breiten Unterläufe (Fluss 0,5 m statt 0,35 m). Damit bleiben `F_DSCHUNGELFLUSS` und
    `F_ELFENFLUSS` trotzdem geteilt (0,86 bzw. 0,99 m bei 2048); die Teilung ist also nötig.
- **Zusammenflüsse** (74): Zwei SWR stoßen dort ebenfalls aneinander (Nebenbach-SWR endet im Hauptfluss-SWR). Nach dem
  Forenfall kann das Netz an der Einmündung fehlen. Abhilfe laut Thread: den Nebenbach als **zweiten Quell-Fluss** in die SWR
  des Hauptflusses aufnehmen (`zufluesse` liefert die Kandidaten). Das ist lokal zu testen (T4).

### 4.2 Testplan (lokal, an C2 bzw. Erlenbach; etwa 1–2 h)

**T1 – Eigenschaften auslesen** (5 min). Python-Ausgabe der Namen; nicht belegte Namen sind [vermutlich].

```python
import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
swr = next(a for a in eas.get_all_level_actors() if isinstance(a, unreal.ShallowWaterRiver) and 'C2' in a.get_actor_label())
c = swr.get_component_by_class(unreal.ShallowWaterRiverComponent)
schl = ('bound', 'size', 'extent', 'source', 'sink', 'match', 'resolution', 'box', 'grid', 'origin', 'bake', 'capture', 'domain', 'sim')
print([n for n in dir(c) if any(k in n.lower() for k in schl)])
print(unreal.ShallowWaterRiverComponent.__doc__)            # Abschnitt "Editor Properties" listet alle Eigenschaften
for n in ('match_spline', 'source_size', 'sim_bounds', 'world_grid_size', 'grid_extent'):   # ausser match_spline: vermutlich
    try:
        print(n, c.get_editor_property(n))
    except Exception as e:
        print(n, '-', e)
wbr = c.get_editor_property('source_river_water_bodies')[0]
print([n for n in dir(wbr.get_water_body_component()) if 'bake' in n.lower() or 'shallow' in n.lower()])   # Verweis auf Gebackenes
```

**T2 – Bereich begrenzen** (20 min, `F_ERLENBACH` als ein `WBR_F_ERLENBACH` bauen, eine SWR):
1. `match_spline = True` → `swr_info` notieren. Erwartet: Rechteck ≈ 301 × 968 m, bei 2048 ≈ 0,47 m.
2. `match_spline = False`, dann Reset → `swr_info`. Dann die Akteur-Lage auf die Mitte von `F_ERLENBACH_T00`
   (`begrenzung.rechteck_cm`) setzen, Skalierung 1, danach Skalierung so, dass das Rechteck 130 × 459 m wird → je
   `swr_info`.
   ```python
   c.set_editor_property('match_spline', False)
   r = [-180504.0, -242771.6, -167447.0, -196865.4]                       # rechteck_cm von F_ERLENBACH_T00
   swr.set_actor_location(unreal.Vector((r[0]+r[2])/2, (r[1]+r[3])/2, swr.get_actor_location().z), False, False)
   # Skalierung nur testen, wenn sim_res/sim_dx auf Lage reagiert:
   # swr.set_actor_scale3d(unreal.Vector((r[2]-r[0])/100/100, (r[3]-r[1])/100/100, 1))   # vermutlich 1 = 100 m
   # danach Reset der Simulation (wie in 16a) und swr_info
   ```
3. Weitere Kandidaten aus T1 (alles mit size/extent/bounds) setzen und `swr_info` vergleichen.
- **Ergebnis:** Ändern Lage, Skalierung oder eine Eigenschaft `sim_res`/`sim_dx` bzw. den Bereich? Wenn ja: Mit welchem Wert
  ergibt sich das Rechteck von T00?

**T3 – Zwei SWR, ein Fluss** (30 min, nur wenn T2 eine Begrenzung findet):
1. `SWR_F_ERLENBACH_T00` und `_T01` mit derselben Quelle/Senke `WBR_F_ERLENBACH`, Bereiche wie im Export (Naht bei s 468,9 in
   einem Becken, 8 m Überlappung).
2. Live: Wasserhöhe beidseits der Naht (Ziel ≤ 2 cm), Strömung, Schaumkante.
3. T00 backen, dann T01 backen. Danach WCBS: Zeigt der Fluss beide Stücke, oder ist eines leer bzw. gibt es eine Lücke an der
   Naht? Den Verweis auf die gebackenen Daten am Water Body aus T1 vor und nach dem zweiten Backen ausgeben.
4. Gegenprobe: Rückfall 1 (zwei `WaterBodyRiver`, an der Naht verkettet wie v2).

**T4 – Zusammenfluss** (15 min): `B_R3_K10_TUNDRA_01` mündet bei s 376 in `F_ERLENBACH`.
1. Zwei SWR backen (je Gewässer eine) und die Einmündung in WCBS ansehen.
2. Danach die SWR des Erlenbachs mit beiden Flüssen als Quelle (`source_river_water_bodies = [WBR_F_ERLENBACH,
   WBR_B_R3_K10_TUNDRA_01]`) und den Nebenbach ohne eigene SWR.

**T5 – Einlaufzeit 2048** (10 min): an `F_ERLENBACH_T01` (2048, 0,264 m) die Zeit bis zum Einlaufen messen (Wasser erreicht
die Mündung, Schaum stabil), dann backen. Backzeit und Größe der gebackenen Texturen notieren.

**Ergebnis zurück:** T1-Liste, T2 `swr_info` je Schritt, T3/T4 Bilder (live, WCBS), T5 Zeiten. Danach legen wir fest:
Teilung als SWR-Bereiche, Rückfall 1 für die 8 langen Gewässer oder Rückfall 2.

## 5. T2-10: Liegt ein Sehens-Bach über 655 m?

**Nein.** Geprüft mit den Sehens-Planer-Ausgaben aller 15 Biome (125 Wasser-Elemente: Bäche samt Kaskadennetz, Seen,
Wasserfälle) und dem Gelände (2 m):

| Was | höchster Punkt | Ort |
|---|---|---|
| Sehens-Bach | **307,1 m** | `gletscher_05_die_waechte` Mühlenbach |
| danach | 288,2 / 280,1 / 265,8 m | `bergwald_06_karsee` Zulauf Süd / West, `gletscher_03_moraenensee` Firnrinnsal |
| Sehens-Wasser überhaupt | 361,2 m | `fjord_02_schleierwand` Wasserfall-Kante `fall1` |
| Sehens-See | 256,2 m | `bergwald_06_karsee` |
| Frost (alle Wasser) | 43,3 m | `frost_03_eisvorhang` Sickerlinie |
| Gletscher (alle Wasser) | 307,1 m | wie oben |
| Welt-Gewässer | 288,2 m | `F_HAUPTFLUSS_1` (B4) |
| Gelände in einem SWR-Rechteck | 331,9 m | `F_HAUPTFLUSS_1` |
| Gelände im Umkreis wasserführender Sehens-Orte | 454,1 m (Gletscher: 418,6 m) | `fjord_02` (`gletscher_05`) |

- Kein Gewässer kommt der Grenze von 655,04 m nahe. Der Abstand beträgt beim Wasser mindestens 294 m, beim Gelände in den
  SWR-Rechtecken mindestens 323 m.
- Gelände über 655 m gibt es nur an Gipfeln (0,026 % der Zellen, höchster 684,1 m); dort liegt keine SWR.
- Die Werte stehen auch im Export (`zusammenfassung.json`: `hoehe`, `swr.gelaende_max_in_swr_m`).

## 6. Was lokal zu tun ist

Commits: **`3ce41a5`** (Exporter, Prüfer, Regeln v3, README, Beispiele) und der Commit dieser Antwort (Nachträge in 16 und
16b).

1. `git pull`, dann Exporter und Prüfer auf 1 m (Befehle wie bisher, siehe `skripte/fluss_sim/README.md`):
   ```
   python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle \
          --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt --aus export/unreal/welt/fluss_sim
   python -I recherche/antworten/skripte/fluss_sim/fluss_sim_pruefen.py export/unreal/welt/fluss_sim \
          --gefaelle export/unreal/welt/gefaelle --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt
   ```
2. **Testplan 4.2** (T1–T5) an Erlenbach/C2, Ergebnisse zurück.
3. **Bau-Werkzeug auf v3 umstellen:**
   - Je Gewässer **einen** `WaterBodyRiver` aus `water_body.spline` (Punkttypen, Tangenten, Breite/Tiefe/Tempo je Punkt,
     `overlap_material_priority`).
   - Je `swr_bereiche[]` eine SWR (Auflösung, Quelle/Senke, Tags, `bottom_contour_actors`, `MI_EL_SWR_Klar`) und ein `WH_…`.
   - Die 8 geteilten Gewässer erst nach T2/T3 bauen.
   - Bestehendes `SWR_C2_Fluss`/`SWR_C2` durch `WBR_F_ERLENBACH` + SWR ersetzen. C2 liegt dort bei s 17,4–220,6 m.
4. **Vorhänge/Kaskadennetze** nicht bauen (wartet); Niagara-Effekte bleiben wie gehabt.
5. **Mündungen mit Lücke** (23) und **offene Enden** (24) beim Bauen ansehen: Spline bis ins Ziel verlängern bzw. die
   Weltdaten nachziehen (Liste in `zusammenfassung.json`).
6. Backen je SWR in `back_reihenfolge`, danach den Editor-Fingerabdruck je SWR speichern. Die Formel ist unverändert; die
   Spline ist der `WBR_<gewaesser>` mit den Punkten `punkt_index`.

## Quellen

Web-Seiten waren aus der Cloud nicht lesbar (DNS); Inhalte aus Suchmaschinen-Auszügen.

- [Python: unreal.ShallowWaterRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent) – Klasse im Plugin WaterAdvanced, Eigenschaften über `get_editor_property` [Doku, Auszug]
- [API: UShallowWaterRiverComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent?lang=en-US) – `bMatchSpline`, gebackene Texturen/Material [Doku, Auszug]
- [API: AShallowWaterRiver](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/WaterAdvanced/AShallowWaterRiver) [Doku, Auszug]
- [Forum: ShallowWaterRiver (Thread 2738013, japanisch)](https://forums.unrealengine.com/t/shallowwaterriver/2738013) – zwei SWR an einer Verzweigung, Netz fehlt nach dem Backen an der Verbindung; Rat: eine SWR mit mehreren WaterBodyRiver, Gebackenes je SWR nur im eigenen Bereich [Forum, Auszug]
- [Forum: ShallowWaterRiver simulation does not initialize in 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772) [Forum, Auszug]
- [Forum: ShallowWaterRiver and Landscape](https://forums.unrealengine.com/t/shallowwaterriver-and-landscape/2818892) – „Wasserwand“ bei gebackenen Flüssen (16b) [Forum, Auszug]
- Projekt: `auftraege/16c-ferat-ein-fluss-je-gewaesser.md` (Nachträge 17:45, 18:15), `bilder/swr/c2_aufloesung_512_1024_2048.jpg`,
  `antworten/16a-swr-einrichtungstest-teil1.md` (Eigenschaftsnamen, d1), `antworten/16b-swr-c2-ganze-strecke.md`,
  `vorlagen/daten/sehens/wasser_welt.json`, `baeche_alle.json`, `legende.json` (Meer = Höhe < 0 ohne Süßwasser)

## Rückfragen

1. **Lange Gewässer (8):** Wenn T2 keine Begrenzung findet oder T3 an der Naht ein leeres Stück zeigt, dürfen wir **nur für
   diese 8** den Fluss an der Naht in zwei `WaterBodyRiver` teilen (in einem Becken, Quelle/Senke verkettet)? Die Alternative
   wäre eine gröbere Zelle; sie reicht für `F_HAUPTFLUSS_3`, `F_DSCHUNGELFLUSS` und `F_ELFENFLUSS` nicht.
2. **Drei lange Bäche** (`B_R_P4_M2_04` 0,31 m, `B_K1_WASSERFALL_WEST_03` 0,36 m, `B_R_P3_P0_04` 0,40 m bei 2048): lieber
   ungeteilt mit etwas gröberer Zelle? Bei Höchstzelle Bach 0,31 m fiele die Teilung bei `B_R_P4_M2_04` weg.
3. **Feldgrenzen mit zwei Plänen** (3 Stellen, 5 Stufen): Der obere Plan behält die 12–30 m Überlappung, die Stufen des unteren
   Plans dort entfallen. Sollen wir stattdessen den unteren Plan bevorzugen? Oder bereinigt der Gefälle-Planer die
   Überlappung (Stufe nur in einem Plan)?
4. **Sehens-Treppen mit kleinen Becken-Seen** (`elfenwald_04_elfentreppe`, `gletscher_06_gletschertoepfe`): Nach der Regel
   „Mündung in See“ ist jede Stufe zwischen zwei Töpfen ein eigenes Gewässer (5 bzw. 4). Sollen solche Ketten ein Gewässer
   mit einer SWR werden, wobei die Töpfe als Becken des Flusses gelten?
5. **Offene Enden und Lücken** (24 + 23) liegen in den Weltdaten (`baeche_alle.json`). Bereinigt ihr sie lokal (Spline
   verlängern), oder sollen wir eine Liste mit Vorschlagspunkten liefern?
6. **Nachtrag 18:15 (Totholz, Schlamm):** Das ist Planer-Arbeit (Gefälle- und Sehens-Bach-Planer) und nicht Teil dieses
   Auftrags. Soll das als eigener Auftrag laufen? Der Export übernimmt neue Objekte automatisch (Wasser-Kollision,
   überspannte Stämme ohne).


## Nachtrag 2: Totholz, Schlamm, Uferstreifen (Antwort auf Nachtrag 18:15)

Stand 12.10.2026. Code für lokal: Commit `b841294` (Zwischenstand `6c8787b`). Gerechnet auf den 2-m-Daten (Gefälle `--alle`,
15 Sehens-Planer), auf den 1-m-Fenstern der Piloten und auf der synthetischen 1-m-Welt.

### Kurzfazit

- **Ein Modul für beide Planer:** `skripte/sehens_lib/bachbett.py` mit den Zahlen in `sehens_lib/bachbett_regeln.json`.
  Der Gefälle-Planer ruft es je Abschnitt auf, die Sehens-Planer über `rezept.py` für jeden geplanten Bach. Rezepte
  brauchen keine Änderung (Abschalten je Bach mit `"bachbett": false`).
- **Unverändert (13f-Regel):** Stufen, Lippen, Becken, Spiegel, Gelände-Deltas, Wasserkörper, Effekte und Kameras. Alle
  98 Gefälle-Pläne vergleichen gleich, `gelaende/*.f32` byte-gleich. Bei allen 42 Sehens-Bächen sind `punkte_cm`,
  `stufen` und `wasser_koerper` gleich. Akteure unverändert: Gefälle 771, Sehens 2 278. Neu sind nur Instanzen und Lagen.
- **Totholz** (nur Instanzen, nie Akteure), Gefälle `--alle`:
  - 1 299 neue große Stücke: 662 Stämme am Ufer, 362 Verklausungs-Stämme, 53 überspannende Stämme, 222 Wurzelstöcke.
  - Dazu 3 312 Äste und 5 300 Zweige.
  - Zusammen mit den 1 435 Holzstufen-Stücken sind das 24,5 große Stücke je 100 m Stufenstrecke.
  - Sehens: 84 große Stücke, 144 Äste und 237 Zweige an 42 Bächen (1,8 km).
- **Dichte nach Biom und Waldnähe:** Die Literaturwerte für Gebirgsbäche liegen bei 12–16 Stück je 100 m in
  Mitteleuropa und den Alpen und bis 60 in Naturwäldern (Quellen unten). Daraus:
  - Bergwald 15, Elfenwald 25, Aue 18, Sumpf 22 und Dschungel 18 je 100 m;
  - Tundra 3, Heide 3, Wüste 0,5;
  - Lava, Gletscher und Frost 0.
  - Der Waldfaktor 0,6–1,4 aus dem 4-m-Baumraster gilt in den Waldbiomen.
- **Schlamm:** Lage `Schlamm` gibt es (FORMAT.md §2), also keine Rückfrage zum Namen. Sie liegt in ruhigen, tiefen Becken
  und am Gleithang, an Lippe, Kolk und Schnelle bleibt Kies. In der Lava liegt Lavasand.
  - Gefälle: 34 639 m² mit Gewicht ≥ 0,3.
  - Sehens: 188 m². Die Treppenbäche haben kaum ruhige Becken.
- **Uferstreifen:** Ein nasser, dunkler Streifen 0–1 m über dem Spiegel aus Schlamm, Erde und Moos je Biom, Summe 255,
  also deckend. Wiese, Gras, Trockengras, Kraut und Heide stehen dort auf 0 (wie die Nadelstreu in 13k).
  - Gefälle: 53 928 m² Streifen; der Prüfer findet an 9 549 Uferzellen 100 % belegt.
  - Sehens: 18 156 m².
- **Felsen** bleiben, wie sie waren. Alles große Holz im Wasser oder ≤ 1 m daneben steht in `<netz>_kol` (3 026 Stücke
  mit Kollision im Wasser oder am Ufer, Äste eingeschlossen). Der fluss_sim-Export (16e-Stand) liest es ein:
  - 24 697 Wasser-Kollisionsobjekte, davon 1 782 überspannt (16d ohne Totholz: 22 025 bzw. 1 425).
  - Prüfer: **0 FEHLER**.
- **fluss_sim:** Der fluss_sim-Agent ist fertig (Antworten 16d und 16e im Repo). Ich habe den Exporter nach seiner
  README auf die neuen Pläne laufen lassen. Sein Prüfer meldet 0 FEHLER, deshalb sind die Beispiele unter
  `antworten/fluss_sim/` aktualisiert (Abschnitt 3).
- **C2:** C2 liegt im Biom **Tundra** (109 von 109 Punkten), also gilt „kaum“: 5 große Stücke, 12 Äste und 17 Zweige,
  dazu 329 m² Uferstreifen und 238 m² Schlamm (Abschnitt 6). Mehr Holz ginge nur mit einer Ausnahme für C2
  (Rückfrage 1).
- **Prüfung:**
  - Gefälle `--alle` 2 m und Piloten 1-m-Fenster: **0 FEHLER**, je zweimal byte-gleich.
  - 15 Sehens-Planer 2 m: **0 FEHLER**, zweimal byte-gleich; auf der synthetischen 1-m-Welt ebenfalls 0 FEHLER (Uferstreifen dort als FEHLER-Regel).
  - Selbsttest grün: 123 Prüfungen, 28 davon neu.

### 1. Totholz: Regeln

**Arten** (Gruppen `bb_<art>_<nr>` bzw. Sehens `bb_<bach>_<art>_<nr>`, nach allen anderen Gruppen gesetzt):

| Art | Lage | Ebene / Kollision |
|---|---|---|
| `verklausung` | oberhalb einer Lippe (das Becken davor ist ≥ 3 m lang) und an Engstellen (B ≤ 0,85 × Median): 2–3 Stämme mit 0,55–1,0 × B Länge, 12–35° schräg und im Wechsel, 0,7–1,6 m vor der Lippe. Verkeilt: Unterkante auf Spiegel − 0,6 × Dicke bzw. auf dem Stamm darunter (`z_frei`). Obenauf 1–2 Äste. | begleiter, Kollision |
| `ueberspannt` | an schmalen Becken (B ≤ 5 m), auf beiden Ufern aufliegend, 0,8–1,8 m Überstand je Seite, Unterkante ≥ Spiegel + 0,25 m | begleiter, Kollision für den Spieler; der Export führt ihn als `ueberspannt` ohne Wasser-Kollision (16a E5) |
| `stamm` | am Ufer, Mitte bei Wasserkante −0,6/+0,5 m, 15–55° zur Fließrichtung (teils im Wasser), 2–7 m, höchstens Bachbreite | begleiter, Kollision |
| `wurzel` | Wurzelstock an der Wasserkante (−0,2/+0,8 m), 1,2–3 m | begleiter, Kollision |
| `ast` | Ufer −0,5/+2 m, 1–2,6 m | schutt; Kollision, wenn ≤ 1 m neben dem Wasser |
| `zweig` | Kiesbank bzw. Innenufer (Gleithang: Krümmung zur Seite, 80 %), −0,6/+1,5 m | kleinzeug, ohne Kollision |

- **Anzahl** je Segment: Ziel = `lw_je_100m` × Waldfaktor × Länge/100, abzüglich der vorhandenen Holzstufen und
  Totholz-quer-Stücke (`holz_*`, `totholz_*`, `wurzel_*`). Davon sind 12 % überspannend und 15 % Wurzelstöcke, der
  Rest liegt am Ufer. Verklausungen und Äste kommen dazu.
  - In der **Aue** sind schon alle Stufen aus Holz. Mit 1 084 Holzstufen-Stücken liegt sie bei 41,7 je 100 m, deshalb
    kommen dort nur 12 Stücke dazu (Rückfrage 3).
- **Netze:** nur natürliche Netze aus `netze.csv`, je Biom eine Palette für Stamm, Ast, Zweig und Wurzel:
  - Bergwald: `SM_FallenSpruceTree_01`, `SM_OldFallenTree_*`, `SM_LargeFallenTree_*`, `SM_Pine_roots_*`,
    `SM_Pine_broken_branch_*`, `SM_mountain_branch_01_*`;
  - Elfenwald: `SM_MossyTree_01`, `SM_MossyForestRoots_*`;
  - Küste: Treibholz.
  - Geprüft: kein Sägeschnitt (`inventar.saegeschnitt`), kein Pflanzenmuster des Exports, alle im Inventar
    (Selbsttest). Stümpfe aus dem Mountain-Set (`SM_pine_stump_*`) sind nicht dabei: Sie sind wahrscheinlich gesägt,
    melden aber kein `*ends*`-Material.
- **Ausrichtung und Skala wie 13k:** Das Netz wird nach der Länge gewählt (Skala 0,6–1,8, Äste ≤ 1,8). Liegend
  modellierte Stücke liegen auf `normale`.
  - Die Hochachse weicht höchstens 30° von der Hangnormalen ab, mit Reserve zur Prüfergrenze 45°.
  - Verkeilte und überspannende Stämme folgen der Normalen so weit, dass es ≤ 20° sind.
  - Im Gefälle entfernt der Planer nach dem 1-m-Feinschliff jedes Stück, das auf dem endgültigen Boden mehr als 40°
    abweicht.
- **Kein Stück durch Blöcke:** Die mittleren 60 % der Achse halten den Kernradius aller massiven Stücke ein. Nur
  Verklausungen dürfen an Blöcken anliegen.
- **Kein Totholz mitten in einer Lippe oder einem Vorhang:** Die Lippenzone wird in der Lippen-Koordinate
  s − Schrägversatz(u) gemessen (15f-Lippenform, aus `lippe_form` nachrechenbar).
  - Normale Lippe: von 0,3 m vor der Lippe bis 0,5 m hinter dem Fuß.
  - Stufe ≥ 1 m oder Vorhang: von 0,5 m vor der Lippe bis 1,5 m hinter dem Fuß (Strahl und Aufprall).
  - Quer reicht die Zone bis Lippenbreite/2 − 0,3 m. An den Lippenenden darf Holz verkeilt liegen.
  - Geprüft wird nach dem Setzen, an der Achse des tatsächlich gesetzten Netzes (gedrehte Bounds) – genau wie im
    Prüfer.

### 2. Schlamm und Uferstreifen

- **Gefälle:** Die Lagen werden auf dem 1-m-Ausgaberaster gegen den Boden nach dem 1-m-Feinschliff gerechnet (altes
  Gelände + Delta). Der Spiegel folgt an den schrägen Lippen `s_eff`.
- **Sehens:** auf dem Lagenraster des Orts. Auf 2 m wird der Streifen um eine Zelle verbreitert, damit ein 1–3 m breiter
  Bach nach dem Hochrechnen seine Uferzellen deckt.
- **Schlamm** (`becken` je Biom, Gewicht 140–230):
  - Gewicht = Ruhe × Tiefe(0,25 → 0,6 m) × Abstand zur Wasserkante (≥ 0,3 m).
  - Die Ruhe ist 0 an der Lippe, bis Fuß + 1,5 m (an Stufen ≥ 1 m bis + 3 m) und 1,2 m vor der nächsten Lippe;
    dazwischen steigt sie auf 1.
  - Am Gleithang (Krümmung ≥ 0,01/m zur Seite der Zelle, ≤ 0,35 m tief, Ufernähe) liegt Schlamm mit 0,7.
  - Kies wird unter dem Schlamm um 75 % × Gewicht gedämpft. An den Schnellen bleibt Kies.
- **Uferstreifen:**
  - Höhe über dem Spiegel: voll von −0,1 bis 0,65 m, Auslauf bis 1,0 m.
  - Breite: bis 3,5 m neben die Wasserkante, Auslauf 1 m.
  - Mischung je Biom mit Rauschen (4 m), z. B. Bergwald Erde 45 %, Moos 35 %, Schlamm 20 %; Aue und Sumpf meist
    Schlamm; Canyon und Wüste Lehm/Schlamm; Gletscher Schlamm/Geröll (Gletschermehl); Lava Lavasand/Moos.
  - Die Summe ist 255, also deckend. Wiese, Gras, Trockengras, Kraut und Heide stehen im Streifen auf 0, alle übrigen
    Lagen auf × 0,4, damit der Streifen vorn liegt.

### 3. Felsen und Wasser-Kollision (Export nur gelesen, nicht geändert)

- Der Export (`fluss_sim_export.Pool.fertig`) wertet ein Objekt als fest, wenn es kein Pflanzennetz ist, im Plan Kollision
  hat oder ein Fels- bzw. Holznetz ist (`holz_muster`), und wenn es groß genug ist (Grundriss ≥ 0,4 m, Höhe ≥ 0,2 m).
  Fest heißt Wasser-Kollision im Wasser oder ≤ 1 m daneben. Liegt die Unterkante im Wasser mehr als 0,1 m über dem
  Spiegel, gilt das Objekt als `ueberspannt`.
- **Totholz:** Alle großen Stücke haben `kollision: true` (Datei `<netz>_kol`). Damit erkennt der Export sie auch dann,
  wenn der Name nicht unter `holz_muster` fällt (`SM_OldTreeBranch_*`, `SM_MossyTree_01` und die Äste laufen dort als
  `sonstiges`, Rückfrage 2). Kleine Zweige bleiben unter der Größengrenze.
- **Felsen:** unverändert. Der fluss_sim-Prüfer meldet 0 Objekte im Wasser ohne Wasser-Kollision.
- **Export-Lauf** (Nachtrag 16e, Exporter aus `b71fd13`): 187 Gewässer, 199 SWR-Bereiche.
  - 24 697 Wasser-Kollisionsobjekte (+31 gegen die 16e-Beispiele, die schon mit dem Zwischenstand gerechnet waren).
  - Davon 1 782 überspannt.
  - Prüfer **0 FEHLER**, 0 WARNUNG, 67 HINWEIS.
  - Die Beispiele unter `antworten/fluss_sim/` sind neu: `F_ERLENBACH`, `bergwald_06_karsee`, `zusammenfassung.json`,
    `back_liste_auszug.json`. Bei `elfenwald_04_elfentreppe` und `vorschlaege.json` ändert sich nichts.
  - Die SWR-Fingerabdrücke der Bereiche mit neuem Holz ändern sich (`objekte`). Diese SWR also neu backen.

### 4. Neue Prüfregeln

`gefaelle_pruefen.pruefe_bachbett` und `bachbett.pruefe_orte_bachbett` (Sehens, über `sehens_pruefen.pruefe_orte`):

| Regel | Stufe |
|---|---|
| `bachbett` im Plan bzw. je Bach in `orte.json` fehlt | FEHLER |
| gelistetes Stück fehlt in der Instanz-Ebene (Lage ± 2 cm, Netz) | FEHLER |
| großes Holz im Wasser bzw. ≤ 1 m daneben ohne Kollision | FEHLER |
| Achse eines Stücks in einer Lippenzone (mitten in Lippe/Vorhang) | FEHLER |
| Dichte großes Holz > max × Waldfaktor (+ 1 Stück Toleranz, bei max 0 keine) | FEHLER; HINWEIS, wenn schon der Bestand darüber liegt |
| Dichte < min × Waldfaktor | FEHLER ab 60 m (WARNUNG mit blockierten Plätzen, darunter HINWEIS) |
| Waldfaktor im Plan ≠ nachgerechnet | FEHLER |
| Uferstreifen: < 80 % der Uferzellen (0,05–0,5 m über dem Spiegel, bis 1,5 m neben dem Netzrand, außerhalb der Lippenzonen) mit Streifenlagen ≥ 200 | FEHLER (Sehens auf 2 m: WARNUNG) |

Dazu gilt weiter `pruefe_liegendes_holz`: Hochachse ≤ 45° gegen die Hangnormale, Skala im Rahmen.

### 5. Zahlen je Biom (vorher → nachher)

**Gefälle `--alle`, 2 m** (98 Läufe mit Stufen, 128 Segmente). Vorher gab es kein Totholz außer den Holzstufen
(„Bestand“) und keinen Schlamm bzw. Streifen.

| Biom | Länge m | Stamm | Verklausung | überspannt | Wurzel | Bestand | groß je 100 m | Äste | Zweige | Streifen m² | Schlamm m² |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Aue | 2 630 | 5 | 5 | 0 | 2 | 1 084 | 41,7 | 502 | 992 | 13 968 | 16 844 |
| Bergwald | 1 718 | 125 | 41 | 2 | 33 | 77 | 16,2 | 433 | 788 | 8 369 | 1 114 |
| Dschungel | 919 | 74 | 28 | 10 | 21 | 40 | 18,8 | 382 | 606 | 4 622 | 465 |
| Elfenwald | 3 958 | 425 | 270 | 41 | 161 | 234 | 28,6 | 1 864 | 2 723 | 18 314 | 12 820 |
| Heide | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 98 | 22 |
| Tundra | 1 909 | 33 | 18 | 0 | 5 | 0 | 2,9 | 130 | 189 | 8 557 | 3 374 |
| **Summe** | **11 152** | **662** | **362** | **53** | **222** | **1 435** | **24,5** | **3 312** | **5 300** | **53 928** | **34 639** |

- Instanzen 65 182 → 75 097 (+15 %), Akteure 771 → 771.
- Prüfer: 0 FEHLER; WARNUNG 42 → 43. Neu ist die Warnung `B_R2_R_P3_M2_02` (Elfenwald, 17,8 statt ≥ 19,6 je 100 m):
  Die Lippen der dichten Kaskade blockieren 145 Plätze.
- Piloten auf 1-m-Fenstern (19 Läufe):
  - Instanzen 20 102 → 22 987, Akteure 251 → 251.
  - 443 große Stücke neu (18,7 je 100 m mit Bestand).
  - Prüfer 0 FEHLER, WARNUNG 11 → 11.

**Sehens, 2 m** (42 Bäche in 26 Orten):

| Biom | Bäche | Länge m | groß | je 100 m | Äste | Zweige | Streifen m² | Schlamm m² | Instanzen vorher → nachher |
|---|---|---|---|---|---|---|---|---|---|
| Aue | 2 | 15 | 0 | 0 | 0 | 0 | 108 | 20 | 20 090 → 20 090 |
| Bergwald | 4 | 102 | 9 | 8,8 | 13 | 22 | 944 | 0 | 13 413 → 13 457 |
| Canyon | 2 | 144 | 2 | 1,4 | 4 | 6 | 1 248 | 0 | 17 826 → 17 838 |
| Dschungel | 2 | 156 | 28 | 17,9 | 59 | 96 | 1 736 | 36 | 15 317 → 15 500 |
| Elfenwald | 7 | 91 | 18 | 19,7 | 23 | 39 | 760 | 0 | 30 980 → 31 060 |
| Fjord | 4 | 235 | 9 | 3,8 | 13 | 23 | 2 344 | 32 | 13 405 → 13 450 |
| Frost | 1 | 26 | 0 | 0 | 0 | 0 | 272 | 0 | 19 611 → 19 611 |
| Gletscher | 11 | 522 | 0 | 0 | 0 | 0 | 5 268 | 40 | 16 743 → 16 743 |
| Heide | 2 | 103 | 3 | 2,9 | 4 | 9 | 1 052 | 20 | 25 451 → 25 467 |
| Lava | 1 | 23 | 0 | 0 | 0 | 0 | 216 | 0 | 18 685 → 18 685 |
| Sumpf | 1 | 30 | 5 | 16,4 | 5 | 8 | 324 | 0 | 21 704 → 21 722 |
| Tundra | 4 | 345 | 10 | 2,9 | 23 | 34 | 3 668 | 36 | 24 784 → 24 851 |
| Wüste | 1 | 23 | 0 | 0 | 0 | 0 | 216 | 4 | 19 326 → 19 326 |
| **Summe** | **42** | **1 816** | **84** | **4,6** | **144** | **237** | **18 156** | **188** | **279 647 → 280 112** |

- Küste und Ödland haben keinen Bach.
- In der Aue sind die zwei Bäche zusammen nur 15 m lang, unter der Mindestlänge. Frost, Gletscher und Lava haben nach
  der Regel kein Holz; in der Wüste ergibt das Ziel 0,1 Stück.
- Akteure 2 278 → 2 278. Warnungen gleich wie vorher (Fjord und Tundra je ein HINWEIS mehr).

### 6. C2 im Detail (`F_ERLENBACH_1V_C2_s1`, 1-m-Fenster)

- **Biom und Ziel:** Tundra auf 171 m Segment, Ziel 3 × 171/100 = 5,1 große Stücke. Der Waldfaktor gilt in der
  Tundra nicht.
- **Gesetzt:**

  | Art | Netz | Länge | Lage | Unterkante über dem Spiegel | Export |
  |---|---|---|---|---|---|
  | Verklausung bei s 60 (vor der Fallkette S04/S05) | `SM_FallenSpruceTree_01` | 7,0 m | im Wasser | −0,52 m | Wasser-Kollision |
  | Verklausung | `SM_OldTreeBranch_06` | 7,0 m | im Wasser | +0,05 m | Wasser-Kollision |
  | Verklausung (obenauf) | `SM_OldTreeBranch_06` | 7,0 m | im Wasser | +0,37 m | `ueberspannt` |
  | Wurzelstock bei s 90 | `SM_BrokenStump_01` | 2,0 m | Ufer | — | Wasser-Kollision |
  | Stamm bei s 167 | `SM_OldFallenTree_01` | 2,9 m | Ufer | +0,31 m | `ueberspannt` |

  Dazu 12 Äste (6 mit Kollision am Wasser) und 17 Zweige (`SM_Pine_broken_branch_*`, `SM_mountain_branch_01_*`).
- **Abgelehnt:** 3 Plätze in Lippenzonen, 4 Achsen durch Blöcke, 1 zu nah am Nachbarn. Die 18 Stufen mit 42 Lippen
  lassen auf 171 m wenig freies Bett.
- **Lagen:**
  - 329 m² Uferstreifen (Moos/Erde/Schlamm, Trockengras dort 0); der Prüfer zählt 32 Uferzellen, 100 % belegt. Das
    Ufer der Klamm ist steil, der Streifen deshalb meist 1–2 m schmal.
  - 238 m² Schlamm in den wenigen längeren Becken und am Innenufer.
- **Instanzen** 1 823 → 1 857, Kollision 522 → 533, Akteure 42 → 42.
- **Export:** `F_ERLENBACH` mit 6 Holzobjekten mit Wasser-Kollision und 2 überspannten in C2.
- Testbild: `antworten/gefaelle/test_F_ERLENBACH_1V_C2_s1.png`.

### 7. Prüfung

| Lauf | Ergebnis |
|---|---|
| Gefälle `--alle`, 2 m | Planer 0 FEHLER; Prüfer 0 FEHLER, 43 WARNUNG; zwei Läufe byte-gleich (`diff -r` ohne Bilder) |
| Piloten, 1-m-Fenster | Planer 0 FEHLER; Prüfer 0 FEHLER, 11 WARNUNG; zwei Läufe byte-gleich |
| 15 Sehens-Planer, 2 m | Planer und Prüfer je 0 FEHLER; zwei Läufe byte-gleich |
| 15 Sehens-Planer, synthetisch 1 m | Planer und Prüfer je 0 FEHLER; Warnungen wie im 13k-Lauf (Uferstreifen-Regel hier als FEHLER) |
| Selbsttest `sehens_lib/selbsttest.py` | grün, 123 ok, 0 FEHLER (neu Schritt 14 `selbsttest_16c.py`, 28 Prüfungen) |
| fluss_sim-Export + Prüfer (16e-Stand) | 0 FEHLER, 0 WARNUNG |

**Testbilder:**
- `antworten/gefaelle/test_*.png`: 22 Pilotbilder. Totholz ist als Achse eingezeichnet: Stamm und Wurzel braun,
  Verklausung rot, überspannt magenta, Äste hell.
- `antworten/sehens/<biom>/test_<ort>.png`: die 26 Orte mit Bach.

### 8. Lokal zu tun

1. Commit `b841294` holen und Gefälle und Sehens auf 1 m neu planen. Dabei ändern sich nur `instanzen/`, `sw_<biom>/` und
   die Lagen-Dateien; Gelände und Wasser bleiben.
2. Das lokale Bachdekor an C2 (Totholz, Schlamm, Uferpflanzen) entfernen oder abgleichen, sonst liegt Holz doppelt.
   Uferpflanzen setzt der Planer nicht; die dürfen bleiben.
3. Lagen einbauen. Der Streifen setzt seine Lagen deckend (Summe 255), das Landschaftsgras geht dort weg.
4. fluss_sim-Export neu laufen lassen und die SWR mit geändertem Fingerabdruck neu backen. Die Hindernis-Akteure `WH_…`
   bekommen das Holz.
5. Im Editor ansehen:
   - Liegen die Verklausungen verkeilt und nicht schwebend? Sie sind `z_frei`; die Unterkante steht im Plan.
   - Lesen sich die überspannenden Stämme als Brücke?
   - Ist der Streifen dunkel genug? Sonst Gewichte in `bachbett_regeln.json` → `biome.<biom>.streifen` anpassen.

### Quellen (Nachtrag 2)

Inhalte aus Suchmaschinen-Auszügen; Zahlen mit Messschwelle (meist ≥ 10 cm Durchmesser, ≥ 0,5–1 m Länge).

- [Repozitorij Univerze v Ljubljani – Totholz in Alpenbächen (Radovna, Triglavska Bistrica, Završnica)](https://repozitorij.uni-lj.si/IzpisGradiva.php?id=137595) – im Mittel 15,8 Stück (1,05 m³) je 100 m, obere Meža 14,4 Stück
- Hering et al. 2000, *Coarse woody debris quantity and distribution in Central European streams*, Int. Rev. Hydrobiol. 85 – geometrisches Mittel 12,5 Stämme (≥ 10 cm) je 100 m (Auszug)
- [Coarse woody debris in mountain streams (Tatra)](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-article-BUJ5-0053-0019/c/Coarse_woody_debris_in_mountain.pdf) – ca. 60 Stück je 100 m in Naturwald-Bächen
- [Comiti, Andreoli, Lenzi, Mao 2006, Geomorphology 78 – Dolomiten](https://core.ac.uk/works/29445906) – niedrige Mengen wie andere Alpenbäche, Dichte fällt mit der Einzugsfläche
- [Rigon, Comiti, Lenzi 2012, WRR 48 – Ostalpen](https://bia.unibz.it/esploro/outputs/journalArticle/Large-wood-storage-in-streams-of/991006492981701241) – 13 Bäche, 2–20 m breit, 3–38 % Gefälle; Holz vor allem aus Hangprozessen; Alpen 10–100 m³/ha ([EPICFORCE D20](https://research.ncl.ac.uk/epicforce/assets/D20.pdf))
- [Wohl & Cadol 2011, Neighborhood matters (Colorado Front Range)](https://mountainscholar.org/items/cd063216-3460-4cbc-a134-c5ef4f0604a0) und [GSA 2011](https://gsa.confex.com/gsa/2011AM/webprogram/Paper197961.html) / [AFS 2012](https://afs.confex.com/afs/2012/webprogram/Paper10921.html) – Altwald im Mittel 45 Verklausungen je km, jüngere Bestände 15–20 je km
- [Cadol & Wohl, La Selva (Costa Rica)](https://mountainscholar.org/handle/10217/39099) – 3,0–34,7 m³ je 100 m, viele kleine Stücke; [Saraiva et al. 2022, PLoS ONE](https://repositorio.ufmg.br/handle/1843/74863) – neotropische Bäche ähnlich gemäßigten Wäldern
- [Fox & Bolton 2007, NAJFM 27](https://salishsearestoration.org/wiki/Fox_and_Bolton_2007) – Referenz unbewirtschafteter Bäche; 75. Perzentil als Untergrenze
- Projekt: `antworten/13k-pilot2-bildbefund-15g-nachtrag.md` (Sägeschnitt, Stammausrichtung, Skala),
  `antworten/16a-swr-einrichtungstest-teil1.md` (d1, Entscheidung 5), `skripte/fluss_sim/fluss_sim_regeln.json`
  (`kollision`), `vorlagen/FORMAT.md` §2 (Lagen)

### Rückfragen (Nachtrag 2)

1. **C2 ist Tundra.** Damit liegen dort nur 5 große Stücke (Regel „kaum“). Im Bild stehen einzelne Kiefern und Birken
   am Hang. Soll C2 (oder der ganze Erlenbach) als Ausnahme Bergwald-Dichte bekommen? Das wären bei 171 m etwa
   25 Stücke statt 5. Technisch wäre das ein Eintrag „Lauf → Biom“ in `bachbett_regeln.json`.
2. **Export `holz_muster`:** `SM_OldTreeBranch_*`, `SM_MossyTree_01`, `SM_BrokenTreeBranch_01`, `SM_Pine_broken_branch_*`
   und `SM_mountain_branch_*` laufen im Export als `sonstiges`. Wasser-Kollision haben sie trotzdem (`kollision` im
   Plan). Soll der fluss_sim-Agent das Muster um `branch|mossytree` erweitern, damit die Art stimmt?
3. **Aue:** Die Holzstufen allein ergeben 41,7 große Stücke je 100 m, über dem Rahmen 10–30. Der Prüfer meldet das als
   HINWEIS, und der Planer setzt dort fast nichts dazu. Bleibt das so, oder soll der Anteil der Holzstufen in der Aue
   sinken?
4. **Dichte Kaskaden:** In 1 von 128 Segmenten reicht der Platz nicht für die Mindestdichte (WARNUNG). Die
   Lippenzonen gehen vor. Einverstanden?
5. **Roh-Läufe ohne Plan** (97 Welt-Läufe ohne Stufenplan, außerhalb der Stufenstrecken): Dort setzt bisher niemand
   Totholz oder Uferstreifen. Soll der Planer dafür einen eigenen Durchlauf bekommen (nur Totholz und Lagen, kein
   Gelände)?

## Nachtrag 3: Totholz nach Waldnähe, Roh-Läufe, Feldgrenzen

Stand 12.10.2026. Grundlage: Koordinator-Entscheidungen zu den Rückfragen aus Nachtrag 2, Ferats Nachtrag 18:15 („Felsen,
Totholz und Schlamm in jedem Bachbett“) und Punkt 3 der 16d-Antworten (Feldgrenzen). Code für lokal: Commit **`79670b9`**.
Gerechnet auf den 2-m-Daten (Gefälle `--alle`, 15 Sehens-Planer, Roh-Läufe, fluss_sim-Export), auf den 1-m-Fenstern der
Piloten und auf der synthetischen 1-m-Welt.

### Kurzfazit

- **Totholz nach Waldnähe:** Der Baumanteil im Umkreis von 40 m zählt jetzt in jedem Biom. Ein Bach mit Bäumen am Ufer
  bekommt Wald-Dichte, auch in Tundra und Heide. Baumlose Strecken bleiben bei „kaum“ bzw. 0, bekommen aber Treibholz und
  Äste, wenn der Oberlauf bewaldet ist. Waldbiome rechnen wie bisher.
- **C2 bleibt bei 5 großen Stücken.** Am Erlenbach stehen nach den Daten keine Bäume am Ufer: 2 Bäume (≥ 5 m) im Umkreis
  von 40 m, 38 im Umkreis von 80 m. Die Bäume aus Ferats Bild stehen 80–150 m entfernt am Hang. Ich habe das nicht
  erzwungen (Abschnitt 2, Rückfrage 1).
- **Feldgrenzen bereinigt:** Eine Stufe steht nur noch in einem Plan. Der Export verliert keine Stufe mehr (vorher 5).
  4 der 5 Lippen bleiben im Plan ihres Felds. Eine Lippe (gleiches Feld) entfällt, weil der obere Plan die Überlappung
  behält.
- **Roh-Läufe:** Die 97 Läufe ohne Stufenplan haben jetzt eine eigene Ebene `bachbett_roh` mit Felsen, Totholz, Schlamm,
  Kies an Schnellen und Uferstreifen. Dazu kommen die Reststrecken der 98 geplanten Läufe außerhalb ihrer Stufenstrecken.
  Es gibt keine Stufen und keine Geländeänderung, nur Instanzen und Lagen.
  - Roh-Läufe: 17,0 km Bachbett.
  - Reststrecken: 6,7 km Bachbett.
  - Zusammen 24 730 Instanzen, keine Akteure.
- **fluss_sim:** `holz_muster` erkennt jetzt Äste und Moosbäume. Der Export liest die Roh-Ebene mit ein.
  - Wasser-Kollision: 24 697 → 41 945 Objekte, davon 12 766 aus der Roh-Ebene.
  - 184 von 199 SWR-Fingerabdrücken ändern sich, fast nur im Teil `objekte`.
- **Unverändert:** Aue-Holzstufen über dem Rahmen (HINWEIS) und die enge Elfenwald-Kaskade `B_R2_R_P3_M2_02` (WARNUNG) so
  gelassen, wie entschieden.
- **Prüfung:** Alle Läufe haben 0 FEHLER und sind deterministisch (Tabelle in Abschnitt 6).
  - Gefälle `--alle` 2 m und Piloten 1 m.
  - 15 Sehens-Planer, 2 m und synthetisch 1 m.
  - Roh-Ebene und fluss_sim-Export.
  - Selbsttest grün: 139 Prüfungen, 16 davon neu.

### 1. Totholz nach Waldnähe

**Regel** (`sehens_lib/bachbett.py` → `dichte`, Regeln v2 in `bachbett_regeln.json`):

- Für jedes Segment wird der Baumanteil gemessen: der Anteil der 4-m-Zellen mit Bäumen ≥ 5 m (`baeume_4m`) im Radius
  40 m um den Bach. Das ist das Raster, das auch die Fern-Kameras aus 13k nutzen. Es enthält alle gesetzten Ebenen.
- **Waldbiome** (Bergwald, Elfenwald, Aue, Sumpf, Dschungel, Fjord) rechnen wie bisher: Biom-Dichte × Waldfaktor 0,6–1,4.
- **Übrige Biome:** Das Gewicht g = glatt((Anteil − 1 %) / 4 %) mischt zwei Dichten. Der Rahmen [min, Ziel, max] ist
  (1 − g) × Biom + g × Ersatz-Waldbiom × Waldfaktor.
  - Ab etwa 5 % Baumanteil gilt die volle Wald-Dichte. Das ist knapp die Hälfte des Bergwald-Mittels von 12 %.
  - Ersatz-Waldbiom: Tundra, Heide, Ödland, Küste, Gletscher und Frost → Bergwald; Canyon und Wüste → Aue (Galeriewald).
  - Lava hat kein Ersatz-Waldbiom und bleibt bei 0.
  - Ab g ≥ 0,5 kommen die Netze aus der Palette des Waldbioms.
- **Treibholz:** Baumlose Strecken (1 − g) bekommen zusätzlich h × 2 große Stücke je 100 m (max 4, kein Minimum), dazu
  0,3 Verklausungen, 4 Äste und 6 Zweige.
  - h = glatt(…) ist dieselbe Rampe, gemessen am Baumanteil der letzten 300 m Oberlauf.
  - Palette: verwitterte Stämme und Äste (`SM_OldFallenTree_*`, `SM_OldTreeBranch_*`, `SM_dead_log_03/04`,
    `SM_BrokenTreeBranch_01`), alle im Inventar, ohne Sägeschnitt.
- **Daten:** Baumanteil im 40-m-Umkreis aller Welt-Läufe, in 50-m-Stücken:
  - Bergwald: Median 12,5 %.
  - Elfenwald: 31,6 %.
  - Dschungel: 15,2 %.
  - Aue: 2,2 %.
  - Heide: 0,7 %, 90-%-Wert 2,0 %.
  - Tundra: 0,2 %, 90-%-Wert 2,2 %.

  Die meisten Tundra- und Heidebäche sind also wirklich offen.
- **Plan und Prüfer:** `dichte[*]` trägt `wald_anteil`, `wald_biom`, `wald_gewicht`, `oberlauf_anteil`, `treibholz`,
  `rahmen_lw` und `palette`. Die Prüfer rechnen den Rahmen nach und melden eine Abweichung als FEHLER: Gefälle, Sehens und
  Roh-Ebene; den Oberlauf nehmen sie aus `spiegel_neu_cm`. Die Dichte-Regel prüft gegen diesen Rahmen.
  - Über max: FEHLER.
  - Unter min: ab 60 m FEHLER, mit blockierten Plätzen WARNUNG.

**Gefälle `--alle`, 2 m** (große Stücke = Stamm, Verklausung, überspannt, Wurzelstock; „Bestand“ = Holzstufen):

| Biom | Länge m | Stamm | Verkl. | übersp. | Wurzel | Bestand | groß je 100 m | Äste | Zweige |
|---|---|---|---|---|---|---|---|---|---|
| Aue | 2 630 → 2 615 | 5 → 5 | 5 → 5 | 0 | 2 → 2 | 1 084 | 41,7 → 41,9 | 502 → 499 | 992 → 986 |
| Bergwald | 1 718 | 125 | 41 | 2 | 33 | 77 | 16,2 | 433 | 788 |
| Dschungel | 919 | 74 | 28 | 10 | 21 | 40 | 18,8 | 382 | 606 |
| Elfenwald | 3 958 → 3 946 | 425 → 421 | 270 | 41 | 161 → 160 | 234 | 28,6 → 28,5 | 1 864 → 1 860 | 2 723 → 2 714 |
| Heide | 18 | 0 → **2** | 0 | 0 | 0 | 0 | 0 → **11,1** | 1 → 3 | 2 → 5 |
| Tundra | 1 909 → 1 907 | 33 → **48** | 18 → **21** | 0 | 5 → **11** | 0 | 2,9 → **4,2** | 130 → 172 | 189 → 263 |
| **Summe** | 11 152 → 11 123 | 662 → 675 | 362 → 365 | 53 | 222 → 227 | 1 435 | 24,5 → 24,8 | 3 312 → 3 349 | 5 300 → 5 362 |

- Neu sind 1 299 → 1 320 große Stücke.
- Instanzen 75 097 → 74 729, Akteure 771 → 769. Weniger sind es, weil `F_HAUPTFLUSS_3_C4` und `F_ELFENFLUSS_3_H4` an der
  Feldgrenze früher enden (Abschnitt 3).
- Aue und Elfenwald ändern sich nur durch diese beiden Neuplanungen. Die Waldbiome rechnen wie vorher; die Anzahlen sind
  dort bitgleich.
- **Tundra mit Ufer-Wald bzw. Treibholz** (7 Segmente; g = Wald-Gewicht):

  | Segment | Baumanteil | g | Treibholz | Ziel je 100 m | gesetzt je 100 m |
  |---|---|---|---|---|---|
  | `B_R_P1_M2_02_s2` | 4,2 % | 0,89 | – | 10,2 | 7,0 |
  | `B_R_P1_M2_02_s3` | 2,7 % | 0,39 | 0,43 | 6,7 | 6,7 |
  | `B_R_P1_M2_02_s4` | 1,8 % | 0,12 | 0,67 | 5,2 | 4,9 |
  | `B_R_P1_M2_01_s1` | 2,1 % | 0,17 | 0,83 | 5,9 | 5,9 |
  | `B_R2_R_P0_M2_01_s1` | 3,3 % | 0,60 | 0,41 | 8,3 | 6,6 |
  | `B_R_P1_M2_04_s1` | 2,1 % | 0,19 | – | 4,3 | 4,0 |
  | `B_R_P3_P0_01_s1` (Heide) | 5,5 % | 1,0 | – | 11,7 | 11,1 |

  An `B_R_P1_M2_02_s2` blockieren die Lippenzonen 92 Plätze. Der Rahmen bleibt trotzdem eingehalten.
- **Piloten, 1-m-Fenster:** 443 → 449 große Stücke; Instanzen 22 987 → 22 842; Akteure 251 → 251.

**Sehens, 2 m** (42 Bäche): Es ändern sich nur Bäche mit Bäumen am Ufer.

| Bach | Baumanteil | groß vorher → nachher |
|---|---|---|
| `gletscher_01_gletschertor/gletscherbach` (132 m) | 7,2 % | 0 → 17 |
| `gletscher_02_lawinenkegel`, drei Schmelzbäche (96 m) | 6,8–13,9 % | 0 → 15 |
| `tundra_04_die_fliesstreppe/schmelzfaden` (192 m) | 3,3 % | 6 → 15 |
| `tundra_05_der_trunkene_grund/abfluss` (36 m) | 9,5 % | 1 → 5 |
| `tundra_06_das_schneetaelchen/schmelzwasser` (35 m) | 3,9 % | 1 → 3 |

- Summe der großen Stücke 84 → 131, Äste 144 → 209, Zweige 237 → 356.
- Instanzen 280 112 → 280 343, Akteure unverändert.
- Die Gletscher-Orte 01 und 02 liegen nach dem Baumraster am Waldrand. Deshalb gilt dort Bergwald-Dichte. Die übrigen
  Gletscherbäche bleiben ohne Holz (Baumanteil ≤ 1,7 %).
- Sehens-Bäche bekommen kein Treibholz vom Oberlauf, weil sie an einer Quelle oder einem See beginnen.

### 2. C2 im Detail

- **Bäume am Erlenbach** (Bäume ≥ 5 m im 4-m-Raster um `F_ERLENBACH_1V_C2`):

  | Umkreis | Zellen | mit Baum | Bäume | Anteil |
  |---|---|---|---|---|
  | 20 m | 586 | 1 | 1 | 0,2 % |
  | 40 m | 1 327 | 2 | 2 | 0,15 % |
  | 80 m | 3 281 | 33 | 38 | 1,0 % |
  | 150 m | 8 222 | 334 | 389 | 4,1 % |
  | 300 m | 25 257 | 1 396 | 1 585 | 5,5 % |

- **Ergebnis:** Am Ufer ist C2 offene Tundra. Das Gewicht ist g = 0, der Oberlauf ist 17 m Quellbach ohne Bäume, also gibt
  es auch kein Treibholz.
  - Rahmen 0–6, Ziel 3 je 100 m auf 171 m.
  - Wie in Nachtrag 2: 5 große Stücke, 12 Äste und 17 Zweige, 329 m² Uferstreifen, 238 m² Schlamm.
  - Instanzen 1 857, davon 533 mit Kollision.
  - Die Instanz-Dateien der Pilotplanung auf 1 m sind byte-gleich zum Stand `b841294`; nur `plan.json` hat die neuen
    Felder.
- **Warum nicht 20–25:** Die Kiefern und Birken aus Ferats Bild stehen 80–150 m vom Bach entfernt am Hang. Mit dem
  Radius 30–50 m aus der Entscheidung zählen sie nicht.
  - Mit 150 m Radius (Holz durch Lawinen und Steinschlag vom Hang, siehe Rigon 2012 in Nachtrag 2) wäre der Anteil 4,1 %.
  - Das ergäbe g ≈ 0,85 und etwa 17 große Stücke.
  - Das habe ich nicht eingebaut (Rückfrage 1).
- **fluss_sim, 2-m-Export:** In C2 haben jetzt 20 Holzobjekte Wasser-Kollision, 5 sind ohne (überspannt). Vorher waren es
  2 als `holz` und 4 als `sonstiges`. Die Äste am Wasser zählen jetzt als Holz.

### 3. Feldgrenzen mit zwei Gefälle-Plänen

**Regel** (`gefaelle_daten.feldgrenzen`, im Planer und im Prüfer):

1. Zwei Welt-Läufe überlappen sich, wenn das Ende des einen ≤ 1 m neben dem Anfang des anderen liegt und umgekehrt, bei
   bis zu 40 m Überlappung. Das sind dieselben Kriterien wie im Export.
2. Haben beide Läufe Stufen, gehört eine Lippe in den Plan, in dessen Feld sie liegt. Liegen beide Läufe im selben Feld
   (Verlängerungen wie `*_1V_C2` → `*_2_C2`), gehört die ganze Überlappung dem oberen Lauf. Ob der Nachbar Stufen bekommt,
   klärt ein Trockenlauf seiner Stufenlage (`nachbar_hat_stufen`). Das Ergebnis hängt also nicht von `--laeufe` ab.
3. Im fremden Teil (`fremd_s_m`) setzt ein Plan keine Lippe, und sein Becken darf nicht hineinlaufen. Dort bleibt der alte
   Spiegel, damit beide Pläne mit passendem Spiegel anschließen.
   - Verletzt das erste Legen diese Regel, wird die Strecke mit der Zone als fester Zone neu gelegt (`feldgrenzen.neu_gelegt`).
   - Der untere Lauf schließt erst dort an, wo sein alter Spiegel nicht über dem des oberen liegt (`grenze_s_m`). In den
     Daten fällt das mit der Feldgrenze zusammen.
4. **Export:** Haben beide Teile einen Plan mit `feldgrenzen`, schneidet der Export die Kette bei `grenze_s_m`, statt das
   untere Teil um die ganze Überlappung zu kürzen.
5. **Prüfer:** Eine Lippe im fremden Teil ist FEHLER, ebenso ein Becken, das hineinläuft. Die Überlappung wird aus den
   Weltdaten nachgerechnet.

**Die drei Fälle aus 16c** (vorher: der Export ließ 5 Teil-Lippen fallen):

| Überlappung | Feldgrenze | vorher | nachher |
|---|---|---|---|
| `F_ERLENBACH_1V_C2` → `F_ERLENBACH_2_C2` | gleiches Feld C2, Überlappung 0–11,9 m gehört C2 | `2_C2_s1_S01_T1` (s 10,0) im Export entfallen | `2_C2` neu gelegt, erste Lippe nach 11,9 m: 5 → 4 Lippen, Fall 3,36 → 3,11 m. C2 selbst unverändert. |
| `F_HAUPTFLUSS_3_C4` → `F_HAUPTFLUSS_3_C5` | C4/C5 bei C5 s 5,25 m | `C5_s1_S01_T1/T2` (s 10,0 und 24,3) entfallen | beide Lippen liegen in C5 und bleiben. C4 neu gelegt: Sein letztes Becken lief in die Überlappung, jetzt endet die Strecke an der Feldgrenze. 8 Lippen bleiben, Fall 9,77 → 9,06 m; die 0,71 m übernehmen die C5-Stufen. |
| `F_ELFENFLUSS_3_H4` → `F_ELFENFLUSS_3_G4` | H4/G4 bei G4 s 9,0 m | `G4_s1_S01_T1/T2` (s 10,0 und 21,0) entfallen | beide Lippen bleiben in G4. H4 neu gelegt wie C4: 6 Lippen, Fall 7,46 → 6,89 m. |

- **Export:** `abstuerze_entfallen` 5 → 0, Abstürze 2 074 → 2 078, Fälle 765 → 762.
- Die drei Gewässer `F_ERLENBACH`, `F_HAUPTFLUSS_3` und `F_ELFENFLUSS` haben neue Splines (Schnittpunkt verschoben).
- Alle übrigen 95 Pläne haben dieselben Stufen wie vorher. Insgesamt bleiben es 1 071 Stufen.
- `plan.json → feldgrenzen` nennt alle 36 Überlappungen mit `fremd_s_m`, `feldgrenze_s_m`, `grenze_s_m`, `nachbar_plan`,
  `lippen_in_fremd` und `neu_gelegt`.

### 4. Roh-Läufe: eigene Ebene `bachbett_roh`

**Wie der Export diese Läufe heute kennt:** als Teil `herkunft: "roh"`, Linie direkt aus den Weltdaten (`wasser_welt.json`
`fluesse` je Feld, `baeche_alle.json`; Punkte `[x, y, z, Breite, Tiefe, v]`, Spiegel = Punkt-z). Objekte hatten sie bisher
nicht (nur die Ufer-Ebene lokal in 5 Feldern).

**Skript** `skripte/gefaelle/bachbett_roh.py` (Prüfer `bachbett_roh_pruefen.py`, auch eingebaut):

- **Welche Läufe:**
  - Alle Welt-Läufe ohne Gefälle-Plan mit Stufen: 97 Roh-Läufe, 21,0 km.
  - Die Reststrecken der 98 geplanten Läufe, 20 m Abstand zu den Stufenstrecken. `--ohne-reststrecken` schaltet sie ab.
- **Linie und Spiegel:** Lauf-Punkte plus Zwischenpunkte alle 2 m. Der Spiegel ist Punkt-z, nie steigend.
- **Ruhe:** aus dem Spiegelgefälle über 20 m, ruhig bei ≤ 0,4 % und Schnelle ab 2 %. Sie steuert Schlamm (ruhig) und Kies
  im Bett (Schnelle).
- **Ausgespart** (`bereiche.ausgespart` mit Grund):
  - Laufenden (je 3 m).
  - Überlappungen, die der Export kürzt (340 m).
  - Mündung in fremdes Wasser (527 m) sowie Seen und Teiche.
  - Orte und Bauwerke bis halbe Breite + 4 m (3 240 m).
  - Sehenswürdigkeiten, Radius + 10 m (1 837 m); dort bauen die Sehens-Planer.
  - Bei Reststrecken die Stufenstrecken.
  - Nach dem Setzen wird zusätzlich alles entfernt, was auf einer Ortszelle oder in einem ausgesparten Bereich liegt.
- **Felsen** (`bachbett.felsen_setzen`, Regeln `roh.felsen`):
  - Ufersteine 0,5–1,4 m.
  - Störsteine im Wasser 0,4–1,6 m, höchstens 0,25 × Breite.
  - Kies und Steinpackungen 0,25–0,6 m.
  - Dichte nach dem Gefälle: Ufer 5–16, Wasser 1–8, Kies 8–24 je 100 m.
  - Netze aus den Biom-Paletten `bloecke`/`kies` des Gefälle-Regelwerks.
  - Ab 0,8 m mit Kollision.
  - Nicht in Feldern mit lokaler Ufer-Ebene: `--ufer-felder`, lokal automatisch aus `ufer/foliage_<Feld>/`. Dort liegen
    schon Kiesel, Kopfsteine und Blöcke.
- **Totholz, Schlamm, Uferstreifen:** dieselbe `bachbett`-Logik wie im Gefälle-Planer, mit Waldnähe und Treibholz vom
  Oberlauf (eigener Lauf, 300 m). Es gibt keine Stufen und keine Lippenzonen. Verklausungen entstehen an Engstellen.
- **Gelände:** keine Änderung. Die Lagen sind Zielgewichte auf 1 m. Laut `SEHENS_FORMAT` §3 gilt neu = max(alt, ziel); die
  übrigen Lagen werden skaliert. Der deckende Streifen verdrängt also das Gras.
- **Format** wie die Gefälle-Pläne, damit der Gefälle-Prüfer (`pruefe_instanzen`, `pruefe_bachbett`) direkt darauf läuft:
  - `<aus>/<lauf>/plan.json` mit `art` (`bachbett_roh` | `bachbett_rest`), `spiegel_neu_cm`/`_s_m` (Lauflinie),
    `stufen: []`, `gelaende: null`, `bereiche`, `abschnitte` (Fenster ≤ 450 m, Lagen, Budget) und
    `bachbett.abschnitte[*]` (`stuecke`, `felsen`, `felsen_bilanz`, `dichte`, `lagen`).
  - `instanzen/<Feld>/`: Ebene `bachbett_roh`, `FT_EL_BBR_`.
  - `lagen/<id>_<Lage>.r8`.
  - Lokal: `export/unreal/welt/bachbett_roh/`.

**Zahlen (2 m):**

| | Läufe | Länge km | Bachbett km | leer | Instanzen | Kollision | große Stücke | Felsen Ufer/Wasser/Kies |
|---|---|---|---|---|---|---|---|---|
| Roh-Läufe | 97 | 21,0 | 17,0 | 7 | 16 760 | 5 686 | 2 187 | 1 584 / 635 / 2 434 |
| Reststrecken | 98 | 23,3 | 6,7 | 57 | 7 970 | 2 807 | 1 199 | 710 / 308 / 1 076 |
| **Summe** | **195** | **44,3** | **23,7** | 64 | **24 730** | **8 493** | **3 386** | **2 294 / 943 / 3 510** |

- „Leer“ heißt: Der Lauf ist ganz ausgespart, z. B. ein kurzer Feldrest, ein Ort oder eine Sehenswürdigkeit, oder die
  Reststrecke ist kürzer als 12 m.
- Akteure: 0.
- Lagen: 183 000 m² Uferstreifen, 192 000 m² Schlamm, 127 000 m² Kies im Bett.

**Totholz je Biom (Roh-Ebene, Roh-Läufe und Reststrecken):**

| Biom | Bachbett m | Stamm | Verkl. | übersp. | Wurzel | groß je 100 m | Äste | Zweige | davon mit Ufer-Wald (m) |
|---|---|---|---|---|---|---|---|---|---|
| Aue | 8 699 | 786 | 144 | 79 | 184 | 13,7 | 1 748 | 3 314 | – |
| Bergwald | 471 | 52 | 0 | 1 | 8 | 13,0 | 84 | 167 | – |
| Canyon | 84 | 6 | 0 | 0 | 1 | 8,3 | 9 | 17 | 44 |
| Dschungel | 4 967 | 716 | 72 | 36 | 144 | 19,5 | 1 922 | 3 218 | – |
| Elfenwald | 2 768 | 641 | 60 | 54 | 132 | 32,0 | 1 101 | 1 782 | – |
| Gletscher | 53 | 7 | 0 | 0 | 1 | 15,2 | 11 | 22 | 53 |
| Heide | 4 577 | 136 | 2 | 2 | 22 | 3,5 | 269 | 517 | 187 |
| Ödland | 290 | 12 | 0 | 0 | 2 | 4,8 | 17 | 30 | – |
| Tundra | 1 130 | 30 | 2 | 0 | 2 | 3,0 | 65 | 113 | 4 |
| Wüste | 657 | 37 | 7 | 0 | 8 | 7,9 | 77 | 146 | 379 |
| **Summe** | **23 694** | **2 423** | **287** | **172** | **504** | **14,3** | **5 303** | **9 326** | **667** |

- Treibholz vom bewaldeten Oberlauf: auf 439 m (gewichtet).
- Der Wüstenbach `B_R3_K12_WUESTE_01` hat 3–4 % Baumanteil am Ufer und gilt deshalb teils als Galeriewald.

**Prüfer `bachbett_roh_pruefen.py`** (FEHLER):

- Stufen oder Gelände vorhanden; Spiegel steigt; Akteure.
- Instanz-Ebene wie bei den Gefälle-Plänen: Format, Inventar, Sägeschnitt, Feldrechteck, Budget, Schweben, Weg, Ortsflächen.
- Bachbett wie `pruefe_bachbett`:
  - Liste ↔ Ebene.
  - Kollision großer Stücke am Wasser.
  - Rahmen nach Waldnähe nachgerechnet.
  - Uferstreifen ≥ 80 %.
- Felsen:
  - in der Ebene vorhanden.
  - Blöcke ≥ 0,8 m am Wasser mit Kollision.
  - ≥ 2 Ufer- oder Störsteine je 100 m je Segment ab 30 m, außer in Ufer-Ebene-Feldern.
- Nichts in Sehenswürdigkeiten und in ausgesparten Bereichen.

Ergebnis: 195 Läufe, **0 FEHLER, 0 WARNUNG**, 463 HINWEIS (Uferstreifen-Anteile, Dichte kurzer Strecken).

### 5. fluss_sim-Export (Regeln v6)

- **`holz_muster`** = `(log|trunk|stamm|stump|root|driftwood|treibholz|branch|deadtree|dead_tree|fallen|mossytree)`.
  - Äste und Moosbäume laufen jetzt als `holz`.
  - Bei den Objekten mit Wasser-Kollision sinkt `sonstiges` von 2 168 auf 147. Es bleiben vor allem `SM_DryRiverBed_*`,
    Sandplatten und einzelne Bäume.
  - Selbsttest: Alle Stamm-, Ast- und Wurzelnetze der Bachbett-Paletten erkennt der Export als Holz.
- **Feldgrenzen:** Schnitt bei `grenze_s_m`, siehe Abschnitt 3.
- **Roh-Ebene:** neue Option `--roh` (Standard: `bachbett_roh` neben `--gefaelle`), auch im Prüfer.
  `zusammenfassung.json → eingaben.bachbett_roh` nennt 131 Läufe mit 163 Feld-Ebenen.
- **Zahlen** (2 m, vorher → nachher):

  | | vorher | nachher |
  |---|---|---|
  | Wasser-Kollision | 24 697 | 41 945 (12 766 aus der Roh-Ebene) |
  | davon im Wasser | 23 776 | 36 623 |
  | `holz` | 2 271 | 16 974 |
  | `fels` | 20 258 | 24 824 |
  | überspannt (ohne Wasser-Kollision) | 1 782 | 6 934 (3 428 aus der Roh-Ebene) |
  | Objekt-Pool | 358 258 | 382 849 |
  | fest und groß | 66 990 | 101 488 |

  Der Sprung bei `holz` kommt aus der Roh-Ebene (8 146) und aus den Ästen am Wasser in den Gefälle- und Sehens-Plänen.
  Die neuen „überspannt“ sind meist Ufersteine und Äste auf der Böschung über dem Spiegel, die noch im Spline-Streifen
  liegen.
- **Fingerabdrücke:**
  - 184 von 199 SWR-Bereichen ändern sich, 15 bleiben gleich.
  - 173 ändern sich nur im Teil `objekte`.
  - 8 auch in `splines`: `F_ELFENFLUSS_T02/T03`, `F_ERLENBACH_T01`, `F_HAUPTFLUSS_3_T01`–`T05`.
  - 3 auch in `gelaende`: `F_ELFENFLUSS_T01`, `F_ERLENBACH_T00`, `F_HAUPTFLUSS_3_T00` (neu gelegte Pläne an der Feldgrenze).
  - C2: `F_ERLENBACH_T00` `2ff2481e67e7…` → `8ca4e0808cd8…`, Objekte 678 → 802; `F_ERLENBACH_T01` 199 → 297.
  - Alle geänderten SWR neu backen.
- **Prüfer:** 0 FEHLER, 0 WARNUNG, 68 HINWEIS (vorher 67). Zwei Läufe sind byte-gleich (`--vergleich`).
- **Beispiele** unter `antworten/fluss_sim/` sind neu: `F_ERLENBACH`, `bergwald_06_karsee`, `elfenwald_04_elfentreppe`,
  `zusammenfassung.json`, `vorschlaege.json` und `back_liste_auszug.json`.

### 6. Prüfung

| Lauf | Ergebnis |
|---|---|
| Gefälle `--alle`, 2 m | Planer 0 FEHLER, 2 WARNUNG; Prüfer 0 FEHLER, 43 WARNUNG (dieselben wie vorher), 301 HINWEIS; zwei Läufe byte-gleich |
| Piloten, 1-m-Fenster | Planer 0 FEHLER; Prüfer 0 FEHLER, 11 WARNUNG (dieselben wie vorher); zwei Läufe byte-gleich |
| 15 Sehens-Planer, 2 m | Planer und Prüfer je 0 FEHLER; Prüfer 28 WARNUNG wie vorher; zwei Läufe byte-gleich |
| 15 Sehens-Planer, synthetisch 1 m | Planer und Prüfer je 0 FEHLER (31 WARNUNG) |
| Roh-Ebene `bachbett_roh` | Planer 0 FEHLER, 0 WARNUNG; Prüfer 0 FEHLER, 0 WARNUNG, 463 HINWEIS; zwei Läufe byte-gleich |
| fluss_sim-Export + Prüfer | 0 FEHLER, 0 WARNUNG, 68 HINWEIS; zwei Läufe byte-gleich |
| Selbsttest `sehens_lib/selbsttest.py` | grün: 139 ok, 0 FEHLER. Schritt 14 hat 16 neue Prüfungen: Tundra mit/ohne Ufer-Wald, Bergwald unverändert, Treibholz, Lava, Prüfer-Rahmen, Ruhe aus dem Gefälle, Holzmuster, Treibholz-Palette, Feldgrenzen (geteilt, Spiegel-Anschluss, gleiches Feld). |

**Testbilder neu:**
- Gefälle: `antworten/gefaelle/test_B_R_P1_M2_01_s1.png`, `test_B_R2_R_P0_M2_01_s1.png` (Tundra mit Ufer-Wald) und
  `test_F_ELFENFLUSS_3_H4_s1.png` (an der Feldgrenze neu gelegt).
- Sehens: `antworten/sehens/gletscher/test_gletscher_01_gletschertor.png`, `test_gletscher_02_lawinenkegel.png` und
  `antworten/sehens/tundra/test_tundra_04_…`, `_05_…`, `_06_….png`.

Die übrigen 19 Gefälle-Pilotbilder sind byte-gleich.

### 7. Lokal zu tun

1. Commit **`79670b9`** holen.
2. **Gefälle auf 1 m neu planen** (`--alle`):
   - Neu sind nur `F_ERLENBACH_2_C2`, `F_HAUPTFLUSS_3_C4` und `F_ELFENFLUSS_3_H4` (Stufen und Gelände) sowie das Totholz
     der Tundra- und Heide-Läufe mit Ufer-Wald.
   - **C2 (`F_ERLENBACH_1V_C2`) ändert sich nicht.** Seine Instanz-Dateien sind gleich; nur `plan.json` hat neue Felder.
3. **Das lokale Bachdekor an C2 entfernen:** Totholz, Schlamm und Uferpflanzen aus eurem Bachdekor-Werkzeug. Sonst liegt
   das Holz doppelt, denn der Planer setzt in C2 schon 5 große Stücke, 12 Äste und 17 Zweige sowie Schlamm und Streifen.
   Uferpflanzen setzt der Planer nicht; die dürfen bleiben.
4. **Sehens neu planen:** Es ändern sich `gletscher_01`, `gletscher_02`, `tundra_04`, `tundra_05` und `tundra_06`; die
   übrigen Orte bleiben gleich.
5. **Roh-Ebene erzeugen:** `python -I recherche/antworten/skripte/gefaelle/bachbett_roh.py --basis <production>`. Das liest
   `export/unreal/welt/gefaelle/`, schreibt `export/unreal/welt/bachbett_roh/` und prüft. Danach Instanzen und Lagen
   einbauen.
   - Die Felder mit Ufer-Ebene (`ufer/foliage_<Feld>/`) bekommen automatisch keine Felsen.
   - In diesen 5 Feldern liegt auch schon Treibholz der Ufer-Ebene. Bitte ansehen, ob dort Holz doppelt wirkt (Rückfrage 3).
6. **fluss_sim-Export und Prüfer neu.** Die Roh-Ebene wird neben `gefaelle/` automatisch gefunden. Dann die SWR mit neuem
   Fingerabdruck neu backen: fast alle, wegen der Roh-Objekte und der Äste.
7. **Im Editor ansehen:**
   - Liegen die Störsteine im Roh-Lauf glaubhaft?
   - Wirkt Kies an den Schnellen und Schlamm in den flachen Strecken?
   - Ist die Tundra mit Ufer-Wald (`B_R_P1_M2_02`) dichter als C2?

### Rückfragen (Nachtrag 3)

1. **C2 und Hang-Holz:** Am Erlenbach stehen die Bäume 80–150 m entfernt am Hang. Mit einem zweiten Radius, etwa „Hang bis
   150 m, nur bergauf“, wären es an C2 etwa 17 statt 5 große Stücke. Soll Holz vom Hang zählen, oder bleibt es beim
   40-m-Umkreis?
2. **Gletscherbäche am Waldrand** (`gletscher_01`, `gletscher_02`): Nach dem Baumraster stehen dort Bäume am Ufer, also gilt
   Bergwald-Dichte (17 bzw. 15 große Stücke). Passt das zum Bild, oder sollen Gletscher wie Lava ohne Ersatz-Waldbiom
   bleiben?
3. **Ufer-Ebene lokal:** In den 5 Feldern mit `ufer/foliage_<Feld>/` setzt die Roh-Ebene keine Felsen, aber Totholz. Die
   Ufer-Ebene hat dort ebenfalls Treibholz. Sollen wir dort das Totholz auch abschalten? Technisch wäre das ein zweiter
   Schalter wie `--ufer-felder`.
4. **Kollisionsmenge:** Die Roh-Ebene bringt 12 766 Objekte mit Wasser-Kollision, die meisten Äste und Ufersteine. Ist
   das für die Hindernis-Akteure (`WH_…`) unkritisch, oder sollen Äste ohne Plan-Kollision dort nicht zählen?

## Nachtrag 4: Hangeintrag Totholz, Roh-Ebene neben Ufer-Ebene

Stand 12.10.2026. Grundlage: Koordinator-Entscheidungen zu den Rückfragen 1–4 aus Nachtrag 3. Code für lokal: Commit
**`2c15bd4`**. Gerechnet auf den 2-m-Daten (Gefälle `--alle`, 15 Sehens-Planer, Roh-Ebene, fluss_sim-Export), auf den
1-m-Fenstern der Piloten und auf der synthetischen 1-m-Welt.

### Kurzfazit

- **Hangbäume zählen bis 150 m** (Rückfrage 1), in den Biomen ohne eigenen Wald (Tundra, Heide, Ödland, Küste, Canyon,
  Wüste, Gletscher, Frost). Gewichtet wird nach Entfernung und Neigung. Bäume tiefer als der Bach, auf ebenem Gelände oder
  hinter einem Rücken zählen nicht. Die Waldfaktor-Logik aus Nachtrag 3 bleibt; nur der Einzugsbereich ist größer.
  Die Waldbiome bleiben unverändert (Begründung in Abschnitt 1).
- **C2: 5 → 14 große Stücke** (171 m, Ziel 14,6). Dazu 24 statt 12 Äste und 40 statt 17 Zweige, Netze aus der
  Bergwald-Palette. Das liegt knapp unter den erwarteten 15–20. Ich habe nicht nachgeschoben: Von 286 Baumzellen
  zwischen 40 und 150 m zählen 130. Die übrigen stehen tiefer als der Bach, hinter dem Sattel nördlich des Bachanfangs
  bzw. hinter der Kuppe, oder zu flach (Abschnitt 2, Bild `antworten/gefaelle/c2_hangbaeume.png`).
- **Gletscherbäche am Waldrand** (Rückfrage 2): Bergwald-Dichte bleibt, keine Regeländerung. Durch die Hangbäume
  steigen `gletscher_01` von 17 auf 20 und `gletscher_02` von 15 auf 19 große Stücke.
- **Roh-Ebene in Feldern mit Ufer-Ebene** (Rückfrage 3): kein Totholz mehr, wie schon keine Felsen. Schlamm, Kies im Bett
  und Uferstreifen bleiben. In der Cloud gibt es keine Ufer-Ebene, deshalb ein eigener Testlauf mit 5 Feldern (Abschnitt 4).
- **Hindernis-Akteure** (Rückfrage 4): höchstens 531 Instanzen in einer Komponente (Grenze 4 000), bis 69 Komponenten
  in einem Akteur. Der Richtwert 16 ist mit „je Netz eine Komponente“ (16a) nicht zu halten (Abschnitt 5, Rückfrage).
- **Prüfung:** Alle Läufe haben 0 FEHLER und sind zweimal byte-gleich (Tabelle in Abschnitt 7). Selbsttest grün: 149
  Prüfungen, 10 davon neu.

### 1. Regel: Hangeintrag

**Was die Literatur sagt** (Quellen in `bachbett_regeln.json`):
- Baumfall liefert Holz aus etwa einer Baumlänge. Der größte Teil stammt aus weniger als 20–50 m Abstand (McDade et al.
  1990; Recruitment Distance im Modell RAIS, Welty et al. 2002).
- Von weiter oben kommt Holz mit Rutschungen, Murgängen und Lawinen. Die Holzbilanz von Benda & Sias (2003) führt
  diesen Eintrag als eigenen Term neben Baumfall und Ufererosion. Reeves et al. (2003) und May & Gresswell (2003) fanden
  einen großen Teil des Holzes aus Hangprozessen, Rigon et al. (2012) ebenso in den Ostalpen.
- An Hängen fallen Bäume bevorzugt hangab (Sobota et al. 2006). Bäume oberhalb des Bachs liefern also mehr als Bäume
  jenseits eines Rückens.

**Umsetzung** (`sehens_lib/bachbett.py` → `baum_messung`, Regeln v3 `allgemein.hang`):
- **Ufer-Anteil** wie bisher: Anteil der 4-m-Zellen mit Bäumen ≥ 5 m im Umkreis von 40 m, alle Seiten.
- **Hang-Anteil:** Jede Baumzelle zwischen 40 und 150 m bekommt ein Gewicht w = Entfernung × Neigung.
  - Entfernung: 1 bei 40 m, linear auf 0 bei 150 m.
  - Neigung G = (Höhe Baum − Höhe Bach) / Abstand. Unter 3 % zählt nichts (Talboden, Ebene; dort bleibt Holz liegen).
    Ab 15 % (8,5°) zählt der Baum voll, dazwischen glatter Übergang.
  - Die Zelle zählt nur, wenn sie höher steht als die Bachstelle und das Gelände auf der geraden Linie zum Bach keinen
    Gegenanstieg über 3 m hat. Ein Gegenanstieg über 3 m ist ein Rücken oder eine Querrinne. Kleinere Buckel,
    Wegböschungen und das Rauschen der 2-m-Daten zählen nicht; Lawinen und Rutschungen laufen über sie hinweg.
  - Je Zelle zählt die Bachstelle mit dem größten Gewicht (Proben alle 10 m).
  - Hang-Anteil = Summe der Gewichte / Zahl der Ufer-Zellen. Ein Hangbaum wirkt also wie ein Bruchteil eines Baums am Ufer;
    offene Hangfläche verdünnt nicht.
- **Wald-Anteil = Ufer-Anteil + Hang-Anteil.** Damit rechnen Ufer-Wald-Gewicht g, Waldfaktor und Treibholz am Oberlauf
  wie in Nachtrag 3, auch der Oberlauf mit Hangbäumen.
- **Waldbiome** (Bergwald, Elfenwald, Aue, Sumpf, Dschungel, Fjord) bleiben beim Ufer-Anteil. Ihre Literaturdichten
  stammen aus Feldaufnahmen, die alles Holz im Gerinne zählen, also auch das vom Hang. Mit Hangbäumen läge der
  Bergwald-Bach im Median bei 39 % statt 13 %, der Waldfaktor stünde fast überall bei 1,4, und der Hangeintrag zählte
  doppelt. Ihre Anzahlen sind bitgleich zu Nachtrag 3.
- **Plan und Prüfer:** `dichte[*]` trägt zusätzlich `ufer_anteil`, `hang_anteil` und `hang_baeume` (Zellen mit
  Gewicht, Baumzellen 40–150 m). Die Prüfer (Gefälle, Sehens, Roh-Ebene) rechnen den Rahmen mit derselben Funktion nach.
  Eine Abweichung ist FEHLER.

**Daten** (100-m-Stücke aller Welt-Läufe; Wald-Anteil ohne → mit Hang):

| Biom | Median | Anteil der Stücke ≥ 5 % (volle Wald-Dichte) |
|---|---|---|
| Tundra | 0,3 % → 1,0 % | 23 % |
| Heide | 0,7 % → 1,2 % | 10 % |
| Ödland | 0,1 % → 0,8 % | 0 % |
| Wüste | 3,2 % → 4,0 % | 14 % |

Die meisten offenen Bäche bleiben offen. Mehr Holz bekommen die Bäche unter bewaldeten Hängen.

### 2. C2 im Detail

- **Hangbäume am Erlenbach** (`F_ERLENBACH_1V_C2`, s 10–181 m): 286 Baumzellen zwischen 40 und 150 m, davon zählen 130.
  - Summe der Gewichte 36,5, auf 1 155 Ufer-Zellen → Hang-Anteil 3,2 %, Ufer-Anteil 0,2 %, zusammen 3,3 %.
  - Ufer-Wald-Gewicht g = 0,62, Waldfaktor 0,71, Netze aus der Bergwald-Palette.
  - Oberlauf (s 0–10 m mit dem Hang darüber): 13,6 % → Treibholz-Anteil 0,38 auf dem baumlosen Rest.
  - Rahmen 3,5–14,8, Ziel 8,5 große Stücke je 100 m → Ziel 14,6 auf 171 m.
- **Ergebnis (2 m und 1-m-Fenster gleich):**

  | | Nachtrag 3 | Nachtrag 4 |
  |---|---|---|
  | große Stücke (Stamm / Verklausung / überspannt / Wurzelstock) | 5 (1 / 3 / 0 / 1) | 14 (9 / 3 / 0 / 2) |
  | je 100 m | 2,9 | 8,2 |
  | Äste / Zweige | 12 / 17 | 24 / 40 |
  | Instanzen / davon mit Kollision | 1 857 / 533 | 1 901 / 548 |
  | Uferstreifen / Schlamm (1 m) | 329 / 238 m² | unverändert |

  Abgelehnt wurden 10 Plätze in Lippenzonen und 16 neben Blöcken. Stufen, Becken, Gelände und Lagen bleiben gleich.
- **Warum nicht 17–20:** Die Schätzung aus Nachtrag 3 (4,1 % im 150-m-Kreis) zählte alle Richtungen. Das Bild
  `antworten/gefaelle/c2_hangbaeume.png` zeigt, wer davon zählt:
  - grün (130 Zellen): vor allem der Nordosthang oberhalb des Bachs, Neigung zum Bach im Median 21 % (10–90 %: 11–48 %);
  - rot (51): im Nordwesten hinter der Kuppe, tiefer als die Bachstellen;
  - orange (92): im Norden hinter dem Sattel (103 m) und hinter der Kuppe, Gegenanstieg über 3 m;
  - violett (13): zu flach (unter 3 %).

  Auch mit 8 m Gegenanstieg stiege das Ziel nur auf 16,2 (5 m: 15,7), denn die Bäume hinter dem Sattel stehen flach
  zum Bach. Mehr gäbe es nur ohne Neigungsgewicht, und dann zählten auch Bäume, die kein Holz bis zum Bach bringen. Ich
  habe deshalb nichts nachgeschoben.
- **fluss_sim:** In `F_ERLENBACH_T00` 802 → 833 Objekte, `F_ERLENBACH_T01` 297 → 320 (die Strecke von `F_ERLENBACH_2V_D3`
  bekommt ebenfalls Hangholz).

### 3. Gletscherbäche am Waldrand

Keine Regeländerung; Gletscher und Frost bekommen nach Baumanteil die Bergwald-Dichte. Die Hangbäume erhöhen die
Anteile, deshalb ändern sich die Zahlen:

| Sehens-Bach | Ufer / Hang | groß vorher → nachher |
|---|---|---|
| `gletscher_01_gletschertor/gletscherbach` (132 m) | 7,2 % / 4,3 % | 17 → 20 |
| `gletscher_02_lawinenkegel`, drei Schmelzbäche (96 m) | 6,8–13,9 % / 6,7–9,6 % | 15 → 19 |
| `gletscher_06_gletschertoepfe/klammbach_unten` (33 m) | 1,3 % / 1,5 % | 0 → 1 |
| `frost_03_eisvorhang/sickerlinie` (22 m) | 1,2 % / 7,2 % | 0 → 3 |
| `tundra_04_die_fliesstreppe/schmelzfaden` (192 m) | 3,3 % / 6,2 % | 15 → 26 |
| `tundra_05_der_trunkene_grund/abfluss` (36 m) | 9,5 % / 25,8 % | 5 → 8 |
| `tundra_06_das_schneetaelchen/schmelzwasser` (35 m) | 3,9 % / 3,9 % | 3 → 4 |

`frost_03` ist neu dabei: Der Eisvorhang liegt unter einem bewaldeten Hang. Soll Frost wie Lava ohne Holz bleiben, reicht
`wald_ersatz` bei `frost` zu streichen (Rückfrage 1).

### 4. Roh-Ebene in Feldern mit Ufer-Ebene

- **Regel** `roh.ufer_ebene_ohne = ["felsen", "totholz"]`: In Feldern mit `ufer/foliage_<Feld>/` (lokal automatisch,
  sonst `--ufer-felder`) setzt die Roh-Ebene weder Felsen noch Totholz. Schlamm, Kies im Bett und Uferstreifen bleiben.
- **Umsetzung:** `bachbett.totholz_setzen(…, ohne_fn)`. Ein Segment ganz im Feld bekommt kein Totholz und den Eintrag
  `ufer_ebene: "ganz"`. Am Feldrand (`"teil"`) fallen nur die Plätze im Feld weg; sie zählen als blockiert. Nach dem
  Zentrieren werden Stücke im Feld noch einmal entfernt. `plan.json → bachbett.totholz_ohne_felder` nennt die Felder.
- **Prüfer:** Totholz in diesen Feldern ist FEHLER. Bei `"ganz"` gibt es keine Dichteprüfung, bei `"teil"` ist zu wenig
  Holz eine WARNUNG.
- **Testlauf** mit den 5 holzreichsten Feldern G4, H6, C4, G6 und E5 als Ufer-Feldern:
  - 87 Segmente ganz und 11 teilweise ohne Totholz.
  - 0 Totholz-Stücke und 0 Felsen in diesen Feldern.
  - Instanzen 25 201 → 13 162; Uferstreifen, Schlamm und Kies unverändert (183 000 / 192 000 / 127 000 m²).
  - Prüfer 0 FEHLER, 4 WARNUNG (Randsegmente).
- Der Hauptlauf in der Cloud hat keine Ufer-Ebene; dort ändert sich nur der Hangeintrag.

### 5. Hindernis-Akteure (`WH_…`)

- **Regeln** v7 `swr.hindernis_grenzen`:
  - Höchstens 4 000 Instanzen je Komponente. Hat ein Netz mehr, teilt der Export es auf weitere Komponenten desselben
    Netzes (`teil`, `teile`).
  - Prüfer: FEHLER über 4 000 Instanzen je Komponente und über 128 Komponenten je Akteur; HINWEIS mit den größten Werten.
- **Größte Werte** (197 Akteure):
  - Komponente: 531 Instanzen (`WH_F_ELFENFLUSS_T01`, `SM_MossyForestRock_01`). Geteilt werden musste nichts.
  - Akteur: 1 356 Instanzen (`WH_B_R_P4_M2_04`).
  - Komponenten: bis 69 (`WH_B_K1_WASSERFALL_WEST_03`), Median 28.
  - **167 von 197 Akteuren haben mehr als 16 Komponenten.**
- **Warum 16 nicht passt:** Eine HISM-Komponente hat genau ein Netz. Die Zahl der Komponenten ist also die Zahl der
  verschiedenen Netze mit Wasser-Kollision in der Kachel: Felsen, Stämme, Wurzeln und Äste mehrerer Paletten. Mehr
  Komponenten durch Teilen nach Netz senken sie nicht.
  - Unter 16 käme man nur mit weiteren Akteuren je Kachel (`WH_<kachel>_2` …), etwa 405 statt 197.
  - Das widerspricht „ein `WH_…` je Kachel“ aus 16a und spart keine Draw Calls, denn je Netz bleibt es eine Komponente.
  - Ich habe deshalb 16 als Richtwert (HINWEIS) und 128 als harte Grenze gesetzt (Rückfrage 2).

### 6. Zahlen vorher → nachher

**Gefälle `--alle`, 2 m** (große Stücke = Stamm, Verklausung, überspannt, Wurzelstock; „Bestand“ = Holzstufen):

| Biom | Länge m | Stamm | Verkl. | übersp. | Wurzel | Bestand | groß je 100 m | Äste | Zweige |
|---|---|---|---|---|---|---|---|---|---|
| Aue | 2 615 | 5 | 5 | 0 | 2 | 1 084 | 41,9 | 499 | 986 |
| Bergwald | 1 718 | 125 | 41 | 2 | 33 | 77 | 16,2 | 433 | 788 |
| Dschungel | 919 | 74 | 28 | 10 | 21 | 40 | 18,8 | 382 | 606 |
| Elfenwald | 3 946 | 421 | 270 | 41 | 160 | 234 | 28,5 | 1 860 | 2 714 |
| Heide | 18 | 2 → 3 | 0 | 0 | 0 | 0 | 11,1 → **16,7** | 3 → 5 | 5 → 10 |
| Tundra | 1 907 | 48 → 96 | 21 → 32 | 0 → 2 | 11 → 24 | 0 | 4,2 → **8,1** | 172 → 265 | 263 → 453 |
| **Summe** | 11 123 | 675 → 724 | 365 → 376 | 53 → 55 | 227 → 240 | 1 435 | 24,8 → 25,4 | 3 349 → 3 444 | 5 362 → 5 557 |

- Neu sind 1 320 → 1 395 große Stücke. Instanzen 74 729 → 75 095, Akteure gleich.
- 14 von 128 Segmenten ändern sich: 13 in der Tundra, 1 in der Heide (`B_R_P3_P0_01_s1`, 18 m, Hang-Anteil 73 %:
  2 → 3 große Stücke). Die größeren:

  | Segment | Ufer / Hang | g vorher → nachher | groß vorher → nachher |
  |---|---|---|---|
  | `B_R_P0_M2_01_s1` (116 m) | 0,6 % / 10,0 % | 0 → 1 | 3 → 17 |
  | `B_R_P1_M2_01_s1` (324 m) | 2,1 % / 4,7 % | 0,17 → 1 | 19 → 40 |
  | `B_R_P1_M2_02_s3` / `_s4` | 2,7 / 1,8 % + 4,6 / 2,5 % | 0,39 / 0,12 → 1 / 0,94 | 5 / 5 → 9 / 11 |
  | `B_R_P1_M2_04_s1` (76 m) | 2,1 % / 3,8 % | 0,19 → 1 | 3 → 9 |
  | `F_ERLENBACH_1V_C2_s1` (171 m) | 0,2 % / 3,2 % | 0 → 0,62 | 5 → 14 |
  | `F_ERLENBACH_2V_D3_s1` (94 m) | 0,9 % / 2,6 % | 0 → 0,69 | 3 → 8 |
  | `B_R_P0_M2_02_s1` (184 m) | 0,5 % / 1,4 % | 0 → 0,14 | 4 → 8 |
  | `B_R_P1_M2_03_s1` (60 m) | 0,2 % / 2,9 % | 0 → 0,54 | 2 → 4 |

- **Piloten, 1-m-Fenster:** große Stücke 449 → 507 (Tundra 3,7 → 7,8 je 100 m), Instanzen 22 842 → 23 112.

**Sehens, 2 m** (42 Bäche): große Stücke 131 → 157, Äste 209 → 245, Zweige 356 → 426. Es ändern sich nur die 9 Bäche
aus Abschnitt 3 (Instanz-Ebenen `sw_frost` E2, `sw_gletscher` D2/E1, `sw_tundra` D2/E2/E3). Alle übrigen Ebenen sind
byte-gleich; `orte.json` nennt überall die neue Regelversion 3.

**Roh-Ebene** (Roh-Läufe und Reststrecken, 23,7 km Bachbett):

| Biom | Bachbett m | Stamm | Verkl. | übersp. | Wurzel | groß je 100 m | Äste | Zweige |
|---|---|---|---|---|---|---|---|---|
| Canyon | 84 | 6 → 8 | 0 | 0 | 1 | 8,3 → 10,7 | 9 → 12 | 17 → 24 |
| Gletscher | 53 | 7 → 8 | 0 | 0 | 1 → 2 | 15,2 → 19,0 | 11 → 13 | 22 → 26 |
| Heide | 4 577 | 136 → 172 | 2 → 12 | 2 → 10 | 22 → 33 | 3,5 → 5,0 | 269 → 352 | 517 → 680 |
| Ödland | 290 | 12 | 0 | 0 | 2 | 4,8 | 17 | 30 |
| Tundra | 1 130 | 30 → 35 | 2 → 5 | 0 | 2 → 5 | 3,0 → 4,0 | 65 → 81 | 113 → 137 |
| Wüste | 657 | 37 → 53 | 7 | 0 | 8 → 10 | 7,9 → 10,7 | 77 → 100 | 146 → 193 |
| Waldbiome (Aue, Bergwald, Dschungel, Elfenwald) | 16 905 | unverändert | | | | | | |
| **Summe** | **23 694** | 2 423 → 2 483 | 287 → 300 | 172 → 180 | 504 → 521 | 14,3 → 14,7 | 5 303 → 5 430 | 9 326 → 9 572 |

- Neu sind 3 386 → 3 484 große Stücke. Instanzen 24 730 → 25 201, Akteure 0; 20 Läufe ändern sich.
- Lagen unverändert. Der Ufer-Wald (gewichtet) wächst von 667 auf 1 531 m Bachbett.

**fluss_sim, 2 m:**

| | vorher | nachher |
|---|---|---|
| Wasser-Kollision | 41 945 | 42 542 (13 014 aus der Roh-Ebene) |
| davon im Wasser | 36 623 | 37 081 |
| `holz` | 16 974 | 17 571 |
| überspannt (ohne Wasser-Kollision) | 6 934 | 7 103 |
| Objekt-Pool | 382 849 | 383 818 |

**SWR-Fingerabdrücke:** 35 von 199 ändern sich, alle nur im Teil `objekte`; 164 bleiben gleich. Neu backen:

- Gefälle- und Roh-Bäche: `B_R_P0_M2_01`, `B_R_P0_M2_02`, `B_R_P1_M2_01`, `B_R_P1_M2_02`, `B_R_P1_M2_04`,
  `B_R_P2_P0_01`, `B_R_P2_P0_04`, `B_R_P2_P0_06`, `B_R_P3_P0_01`, `B_R_P3_P0_02_T00`, `B_R_P3_P0_02_T01`,
  `B_R_P3_P0_04`, `B_R_P3_P0_05`, `B_R2_R_P0_M2_01`, `B_R2_R_P1_M2_01`, `B_R2_R_P3_P0_02`, `B_R2_R_P3_P0_03`,
  `B_R2_R_P3_P0_04`, `B_R2_R_P3_P0_05`, `B_R3_R_P3_P0_02`, `B_R3_K12_WUESTE_01`.
- Flüsse: `F_ERLENBACH_T00` (`8ca4e0808cd8…` → `6d654add5371…`), `F_ERLENBACH_T01` (`47d48db84e97…` →
  `f48e9bfb0d0b…`), `F_CANYONBACH`, `F_GLETSCHERTAL`, `F_HAUPTFLUSS_3_T05`.
- Sehens: `SW_frost_03_eisvorhang_sickerlinie`, `SW_gletscher_01_gletschertor_gletscherbach`,
  `SW_gletscher_02_lawinenkegel_schmelz_mitte` / `_ost` / `_west`, `SW_gletscher_06_gletschertoepfe_klammbach_oben`,
  `SW_tundra_04_die_fliesstreppe_schmelzfaden`, `SW_tundra_05_der_trunkene_grund_abfluss`,
  `SW_tundra_06_das_schneetaelchen_schmelzwasser`.

### 7. Prüfung

| Lauf | Ergebnis |
|---|---|
| Gefälle `--alle`, 2 m | Planer 0 FEHLER, 2 WARNUNG; Prüfer 0 FEHLER, 43 WARNUNG (dieselben wie vorher), 301 HINWEIS; zwei Läufe byte-gleich |
| Piloten, 1-m-Fenster | Planer 0 FEHLER; Prüfer 0 FEHLER, 11 WARNUNG (wie vorher); zwei Läufe byte-gleich |
| 15 Sehens-Planer, 2 m | Planer und Prüfer je 0 FEHLER; Prüfer-Warnungen wie vorher; zwei Läufe byte-gleich |
| 15 Sehens-Planer, synthetisch 1 m | Planer und Prüfer je 0 FEHLER; 36 WARNUNG, keine zum Bachbett; zwei Läufe byte-gleich |
| Roh-Ebene `bachbett_roh` | Planer 0 FEHLER, 0 WARNUNG; Prüfer 0 FEHLER, 0 WARNUNG, 463 HINWEIS; zwei Läufe byte-gleich |
| Roh-Ebene mit 5 Ufer-Feldern (Test) | Planer 0 FEHLER; Prüfer 0 FEHLER, 4 WARNUNG (Randsegmente), 0 Totholz und 0 Felsen in den Feldern |
| fluss_sim-Export + Prüfer | 0 FEHLER, 0 WARNUNG, 70 HINWEIS (2 neu: Hindernis-Akteure); zwei Läufe byte-gleich (183 Dateien) |
| Selbsttest `sehens_lib/selbsttest.py` | grün: 149 ok, 0 FEHLER. `test_16c4` hat 10 neue Prüfungen: Hangbäume oberhalb zählen; hinter dem Rücken, auf ebenem Gelände, tiefer als der Bach und über 150 m nicht; nähere wiegen mehr; Bergwald unverändert; Prüfer rechnet nach; WH-Komponenten nach Netz geteilt. |

**Testbilder neu:**
- Gefälle (Piloten): `antworten/gefaelle/test_F_ERLENBACH_1V_C2_s1.png`, `test_F_ERLENBACH_2V_D3_s1.png`,
  `test_B_R_P0_M2_01_s1.png`, `test_B_R_P0_M2_02_s1.png`, `test_B_R_P1_M2_01_s1.png`, `test_B_R_P1_M2_03_s1.png`,
  `test_B_R2_R_P0_M2_01_s1.png`. Die übrigen 15 Pilotbilder sind byte-gleich.
- Neu: `antworten/gefaelle/c2_hangbaeume.png` (welche Bäume an C2 zählen).
- Sehens: `tundra_04`, `_05`, `_06`, `gletscher_01`, `_02`, `_06` und `frost_03` (`antworten/sehens/<biom>/test_….png`).
- fluss_sim-Beispiele (`antworten/fluss_sim/`) neu, darunter `F_ERLENBACH` und `back_liste_auszug.json`.

### 8. Lokal zu tun

1. Commit **`2c15bd4`** holen.
2. **Gefälle auf 1 m neu planen** (`--alle`). Neu ist nur das Totholz der Tundra- und Heide-Läufe mit Hangwald, darunter
   C2 (`F_ERLENBACH_1V_C2`: 14 große Stücke, 24 Äste, 40 Zweige). Stufen, Gelände und Lagen bleiben gleich.
3. **Sehens neu planen:** Es ändern sich `tundra_04`–`06`, `gletscher_01`, `_02`, `_06` und `frost_03`.
4. **Roh-Ebene neu erzeugen** (`bachbett_roh.py --basis <production>`). In den Feldern mit `ufer/foliage_<Feld>/` fallen
   jetzt Felsen und Totholz weg. Bitte im Log die Zeile „Ufer-Ebene (ohne Felsen und Totholz): …“ prüfen.
5. **fluss_sim-Export und Prüfer neu.** Der Prüfer gibt die größten `WH_…`-Werte aus. Danach die SWR mit neuem
   Fingerabdruck neu backen; lokal kommen die Felder mit Ufer-Ebene dazu.
6. **Im Editor ansehen:** C2 von unten mit Blick zum Nordosthang. Liegt jetzt genug Holz im Bach, und passt die
   Bergwald-Palette zu den Kiefern und Birken am Hang?

### Rückfragen (Nachtrag 4)

1. **C2 bei 14 statt 15–20:** Reicht das? Ein lockerer Rücken (Gegenanstieg 8 m statt 3 m) brächte nur 16. Für 17–20
   müsste das Neigungsgewicht fallen; dann zählten auch flach stehende Bäume, die kein Holz bis zum Bach bringen. Und soll
   `frost` wie Lava ohne Holz bleiben (`frost_03`: 0 → 3)?
2. **Komponenten je `WH_…`:** 167 von 197 Akteuren haben mehr als 16 Komponenten, weil jedes Netz eine Komponente
   braucht. Bleibt es bei einem Akteur je Kachel (Richtwert 16 nur als HINWEIS, harte Grenze 128)? Oder sollen die
   Komponenten auf `WH_<kachel>_2` … verteilt werden (etwa 405 Akteure)?
