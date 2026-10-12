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
