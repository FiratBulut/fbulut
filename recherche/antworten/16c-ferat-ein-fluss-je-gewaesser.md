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
