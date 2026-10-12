# Antwort zu Auftrag 16b – Shallow Water River je Strecke (fluss_sim v2), Dispatches, Schaum, Sichtbarkeit

Stand 12.10.2026. Grundlage sind Auftrag 16b mit dem Nachtrag 16:30, die Bilder `bilder/swr/c2_ganz_netz_live_gebacken.jpg`,
`c2_wcbs_klar.jpg` und `t1_live_gegen_gebacken.jpg`, Datei 16, Datei 16a mit allen Nachträgen (Entscheidungen 1–6 des
Koordinators gelten) und `skripte/fluss_sim/`.

**Quellenlage:** `dev.epicgames.com`, `forums.unrealengine.com` und `lilys.ai` antworten aus der Cloud weiter mit **Proxy 403**
(curl) bzw. DNS-Fehler (WebFetch). Web-Belege stammen deshalb aus **Suchmaschinen-Auszügen**. Kennzeichnung wie in 16a:
[Doku] Epic-Doku/API, Auszug · [Forum] · [Drittquelle] · [Projekt] eigene Daten · [Test 16b] lokaler Befund ·
[Ableitung] · [Schätzung] · [vermutlich] Name oder Wirkung nicht belegt.

## Kurzfazit

- **Export v2 ist fertig** (Commit `6f7f315`). Die SWR-Einheit ist die **Strecke**: je Gewässer **ein** `ShallowWaterRiver`
  mit **einer** `WaterBodyRiver`-Spline (Punktabstand ≥ 2 m), `resolution_max_axis`, Zelle, Hindernis-Akteur `WH_<einheit>`
  und Fingerabdruck je Einheit.
  - **249 SWR-Einheiten** für 177 Gewässer (v1: 555 Back-Kacheln). 143 Strecken bleiben eine Einheit, **34 werden geteilt**
    (in 106 Einheiten, 72 Nähte: 22 an Fällen, 16 in Becken, 34 an ruhigen Stellen, 0 ohne geeignete Stelle).
  - **Zellen:** Median 0,343 m, Bereich 0,17–0,498 m, keine über 0,5 m. Bäche (205 Einheiten) liegen zu 79 % bei
    ≤ 0,40 m; 42 Bach-Einheiten liegen bei 0,40–0,50 m (Box 205–256 m). Flüsse (44) liegen bei 0,45–0,50 m.
  - **Hindernis-Akteure:** 182 `WH_<einheit>` mit 20 521 Instanzen in 2 001 Komponenten, dazu 998 Akteure mit Tag.
    67 Einheiten haben kein Hindernis.
  - **C2:** eine Einheit, 203 m Lauf, Box 91 × 218 m, **512 → 0,425 m** je Zelle (2-m-Daten; lokal 179 m / 0,35 m, siehe
    Rückfrage 1).
- **Vorhang nur an echten Fallkanten:** Einzelabsturz ≥ 3 m oder senkrechte Felslippe ab 2 m. Das trifft **170 von 765
  Fällen**. Nur dort gibt es Kaskadennetz-Vorhang und Schaumobjekte (1 231 statt 5 563). An C2 betrifft es S04, S05, S10 und
  S13; S03 und S15 bleiben Rinnen.
- **Prüfer v2: 0 FEHLER, 0 WARNUNG, 52 HINWEIS** (42 × Bach-Zelle > 0,4 m, 9 × Fuß im See, 1 × Determinismus). Zwei Läufe
  sind byte-gleich (163 Dateien). Alle 8 neuen Gegenproben ergeben FEHLER.
- **Frage 1 (3 Dispatches):** Sie gehören zum Niagara-System **der Fluss-SWR** (`Grid2D_SW_River`), nicht zur Interaktion um
  die Spielfigur. Am wahrscheinlichsten ist der **Sekundär-Emitter** (Gischt-Teilchen, im gebackenen Bild sichtbar) samt einer
  Gitter-Stufe, die die gebackenen Daten für ihn liest [vermutlich].
  - **Abschalten lohnt sich unbedingt.** Bei 1 km Ladebereich sind bis zu 62 Einheiten geladen, im Median 26. Das wären
    5–12 ms bei 0,2 ms je Einheit [Schätzung].
  - Vorschlag: Abschalten nach **Kamera-Entfernung bzw. Sichtbarkeit**, nicht nach „Pawn im Wasser“. Diagnose D8 unten.
- **Frage 2 (Schaum dünner):** zuerst `Foam Boost` senken, dann `Foam powr` erhöhen, erst danach `SimFoam Contrast` und
  `Foam Opacity`. Stufen siehe Tabelle. Das braucht kein neues Backen. Die Schwelle der Simulation selbst ist nicht belegt und
  erst der zweite Hebel (braucht neues Backen).
- **Frage 4 (klarer Bach von der Seite unauffällig):** leicht mehr Rauheit und Normalen für Glanzlichter, dunkler, nasser
  Grund mit Kieseln, Uferband aus Nässe. Die Klarheit bleibt.

## 1. Umsetzung v2 (`fluss_sim_v2`)

### 1.1 Was sich ändert

| Teil | v1 | **v2** |
|---|---|---|
| Einheit für Simulation, Backen, Fingerabdruck | Back-Kachel ≤ 128 m (555) | **Strecke** (249 SWR-Einheiten) |
| `WaterBodyRiver` | je Abschnitt zwischen Fällen (1 120) | **einer je Einheit** (`water_body.spline`); je Abschnitt nur Rückfall |
| `ShallowWaterRiver` | je Kachel, Quelle/Senke = Abschnitte | je Einheit, Quelle = Senke = eigener River |
| Hindernis-Akteur | `WH_<kachel>` (Spezifikation 16a) | **`WH_<einheit>`**, umgesetzt |
| Kacheln (`sim_bereiche`) | Back-Einheit | Unterteilung (13k-Akteurgrenze, Teil-Fingerabdruck zur Ortung) |
| Vorhang + Schaumobjekte | an jedem Fall ≥ 1 m | nur `vorhang: true` (Regel 1.4) |
| Überspannende Objekte | mit Kollision | **ohne** (`ohne_wasser_kollision`, Entscheidung 5) |
| Back-Liste | je Kachel (`back_liste_v1`) | je Einheit mit Reihenfolge (`back_liste_v2`) |

Abschnitte, Becken, Fälle, Effekte und die Fingerabdruck-Formel bleiben gleich. Ein Werkzeug, das noch v1 liest, findet die
Felder weiterhin. Es muss nur `swr_einheiten` vor `sim_bereiche` stellen.

### 1.2 Regel: eine Einheit je Strecke, Teilung nur wenn nötig

**Eine Einheit je Strecke**, solange die längste Achse der Box (Spline ± halbe Breite) bei 512 Zellen eine Zelle ≤ 0,5 m
ergibt, also ≤ 256 m. „Strecke“ ist ein Gewässer der Ausgabe: Gefälle-Lauf (kann mehrere der 161 Strecken enthalten),
Sehens-Bach oder Fluss.

**Zelle und Auflösung:**
- Zielzelle: **0,35 m für Bäche**, das ist die Mitte von 0,3–0,4 m. Bach heißt: Strecke mit Abstürzen im Plan oder Median der
  Breite < 15 m. **0,5 m für Flüsse** (Entscheidung 3).
- `resolution_max_axis` = ⌈Achse / Ziel / 32⌉ × 32, begrenzt auf [32; 512]. `zelle_m` = Achse / Auflösung.
- Ist ein Bach so lang, dass auch 512 nicht für 0,4 m reicht (Box 205–256 m), bleibt er eine Einheit mit 0,4–0,5 m.
  Der Prüfer gibt dafür einen HINWEIS (42 Einheiten, Rückfrage 3).
- C2 ist ein Bach (Abstürze im Plan), obwohl der Median der Breite 21,7 m beträgt.

**Teilung längerer Strecken** (gierig von oben, möglichst wenige Einheiten):
1. Ab dem Anfang `a` das größte `b` bestimmen, bis zu dem die Box ≤ 252 m bleibt (256 m minus 4 m Überlappung).
2. Eine Teilstelle im hinteren Teil [a + 0,5 · (b − a); b] wählen. Gibt es dort keine, im Notfall ab 0,1. Rangfolge:
   1. **Fall mit Vorhang**
   2. **anderer Fall**
   3. **Becken:** Mitte eines Beckens ≥ 8 m, Gefälle ≤ 3 % über ± 2 m
   4. **ruhige Stelle:** flachstes Gefälle über ± 5 m, ≥ 1 m von jedem Absturz entfernt

   Bei gleichem Rang gewinnt die talwärts letzte Stelle (weniger Einheiten) bzw. die flachste.
3. Keine Rest-Einheit < 30 m (sonst entstanden 4-m-Stummel am Laufende).

**Begründung der Rangfolge:**
- **Fall:** Das Wasser fällt frei über die Lippe. Was unterhalb passiert, wirkt nicht nach oben zurück (Fließwechsel an der
  Lippe). Die obere Simulation darf an der Lippe enden (Senke), die untere am Fuß beginnen (Quelle). Die Naht liegt unter
  Vorhang bzw. Aufprallschaum. → **Source/Sink-Verkettung ohne Überlappung.**
- **Becken / ruhige Stelle:** Der Spiegel ist waagrecht und die Strömung langsam. Zwei Simulationen haben dort fast
  denselben Spiegel, also sieht man keine Stufe. → **Splines überlappen 4 m** (je 2 m über die Teilstelle). Senke und Quelle
  liegen dadurch außerhalb der sichtbaren Naht; der obere River hat Vorrang (`overlap_material_priority`).
- **Nie mitten in eine Rinne:** Dort ändern sich Höhe und Geschwindigkeit je Zelle, eine Naht wäre sichtbar.

**Ergebnis (2 m, alle Gewässer):**

| Kategorie | Gewässer | Einheiten | davon geteilt (Strecken → Einheiten) |
|---|---|---|---|
| Gefälle-Läufe mit Plan | 98 | 139 | 24 → 65 |
| Läufe der 161 Strecken ohne Plan (roh) | 25 | 31 | 4 → 10 |
| Sehens-Bäche | 42 | 42 | 0 |
| Flüsse ≥ 15 m ohne Plan | 12 | 37 | 6 → 31 |
| **Summe** | **177** | **249** | **34 → 106** |

- Am stärksten geteilt: `F_DSCHUNGELFLUSS_H6` (2,0 km, 8 Einheiten), `F_ELFENFLUSS_3_G4`, `F_HAUPTFLUSS_3_D5` und
  `_E5` (je 7), `F_HAUPTFLUSS_3_C5` (6), `F_HAUPTFLUSS_3_F5` (5, bis 222 m breit).
- Bei den Gefälle-Läufen ist 1 von 2 Nähten ein Fall (22 von 41). Die Flüsse ohne Plan haben keine Fälle; dort liegen die
  Nähte in Becken bzw. an der flachsten Stelle.

**Verteilung der Zellgrößen und Auflösungen:**

| Zelle | ≤ 0,30 | 0,30–0,35 | 0,35–0,40 | 0,40–0,45 | 0,45–0,50 |
|---|---|---|---|---|---|
| Bach (205) | 26 | 120 | 17 | 18 | 24 |
| Fluss (44) | – | – | – | 3 | 41 |

`resolution_max_axis`: 82 × 512, 24 × 480, 36 × 384–448, 28 × 256–352, 79 × 32–224.

### 1.3 Felder je Einheit (Beispiel-JSON)

Ausschnitt aus C2 (`antworten/fluss_sim/gefaelle/F_ERLENBACH_1V_C2/fluss_sim.json`):

```json
{"id": "F_ERLENBACH_1V_C2_E00", "s_m": [0.0, 203.16], "laenge_m": 203.16,
 "abschnitte": ["F_ERLENBACH_1V_C2_A00", "...", "F_ERLENBACH_1V_C2_A17"],
 "kacheln": ["F_ERLENBACH_1V_C2_K00", "F_ERLENBACH_1V_C2_K01", "F_ERLENBACH_1V_C2_K02"],
 "naht_oben": {"art": "laufanfang", "s_m": 0.0, "fall": null, "ueberlappung_m": 0.0},
 "naht_unten": {"art": "laufende", "s_m": 203.16, "fall": null, "ueberlappung_m": 0.0},
 "vorgaenger": [], "nachfolger": [], "back_reihenfolge": 0,
 "water_body": {"id": "WBR_F_ERLENBACH_1V_C2_E00", "klasse": "WaterBodyRiver", "affects_landscape": false,
   "overlap_material_priority": 1,
   "spline": {"s_m": [0.0, 203.16],
     "punkte": [[-172182.5, -239417.0, 10206.1, 2879.3, 91.7, 300.0], [-172245.4, -239227.2, 10175.0, 2805.5, 86.1, 300.0], "..."],
     "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
     "punkt_typen": ["CURVE_CLAMPED", "...", "LINEAR", "LINEAR", "..."], "tangenten_cm": [[-62.9, 189.8, -31.1], "..."],
     "punkte_s_m": [0.0, 2.0, 4.0, "..."], "punkt_rollen": ["rampe", "...", "lippe", "becken", "..."]}},
 "swr": {"id": "SWR_F_ERLENBACH_1V_C2_E00", "klasse": "ShallowWaterRiver", "typ": "bach", "breite_median_m": 21.73,
   "zelle_ziel_m": 0.35, "achse_m": 217.64, "box_m": [91.47, 217.64],
   "resolution_max_axis": 512, "zelle_m": 0.425, "raster_erwartet": [216, 512],
   "source_river_water_bodies": ["WBR_F_ERLENBACH_1V_C2_E00"], "sink_river_water_bodies": ["WBR_F_ERLENBACH_1V_C2_E00"],
   "bottom_contour_tags": ["SWR_Hindernis"],
   "bottom_contour_actors": ["WH_F_ERLENBACH_1V_C2_E00", "WH_F_ERLENBACH_2_C2_E00"],
   "bottom_contour_landscape_actors": "lokal", "use_capture": true, "match_spline": true,
   "render_state": {"backen": "LIVE_SIM", "spiel": "WATER_COMPONENT_WITH_BAKED_SIM", "ersatz": "BAKED_SIM"},
   "material": {"water_body": "MI_EL_SWR_Klar", "baked_sim_material": "MI_EL_SWR_Klar"}},
 "bereich_cm": [-180689.4, -241656.6, -169942.9, -218292.2],
 "hindernis_akteur": {"id": "WH_F_ERLENBACH_1V_C2_E00", "klasse": "Actor",
   "tags": ["SWR_Hindernis", "SWR_E_F_ERLENBACH_1V_C2_E00"], "ursprung_cm": [-175316.1, -229974.4, 0.0],
   "komponenten": [{"netz": "/Game/Fab/Megascans/3D/Icelandic_Boulder_texndcpda/.../texndcpda_tier_0", "klasse": "HISM",
                    "nanite": null, "kollision": "wie_quelle",
                    "instanzen": [{"ref": {"quelle": "gefaelle/F_ERLENBACH_1V_C2/instanzen/C2/plan.json",
                                           "datei": "texndcpda_tier_0", "index": 1},
                                   "pos_cm": [-173679.7, -235687.1, 9053.0],
                                   "quat_xyzw": [0.045956, 0.001879, 0.564777, 0.823961],
                                   "skala": [0.5826, 0.5826, 0.5826], "lage": "im_wasser"}, "..."]}, "..."],
   "akteure_mit_tag": [{"ref": {"quelle": "...", "liste": "akteure", "index": 0}, "...": "..."}],
   "n_instanzen": 526, "n_komponenten": 20, "n_akteure_mit_tag": 46, "umzug": "verschieben"},
 "fingerabdruck": "7d2b1dafeafa7c7c82da75ed9c89d73da1c22bffa11127b306c9b4a574ece20f",
 "fingerabdruck_teile": {"gelaende": "7772902a...", "splines": "28641044...", "objekte": "eaee9d02..."},
 "n_hoehen": 6318, "raster_cm": 200.0, "n_objekte": 614}
```

Eine geteilte Strecke (`B_R_M1_P0_03`, 571 m, gekürzt):

```json
{"id": "B_R_M1_P0_03_E00", "s_m": [0.0, 225.74], "naht_unten": {"art": "fall", "fall": "B_R_M1_P0_03_s2_S05_T2",
   "ueberlappung_m": 0.0, "verkettung": "Senke = eigener River, Spline endet an der Lippe"},
 "swr": {"resolution_max_axis": 480, "zelle_m": 0.337, "...": "..."}},
{"id": "B_R_M1_P0_03_E01", "s_m": [226.24, 398.83], "water_body": {"spline": {"s_m": [226.24, 400.83]}},
 "naht_oben": {"art": "fall", "verkettung": "Quelle = eigener River, Spline beginnt am Fuss"},
 "naht_unten": {"art": "becken", "s_m": 398.83, "ueberlappung_m": 4.0}},
{"id": "B_R_M1_P0_03_E02", "s_m": [398.83, 571.42], "water_body": {"spline": {"s_m": [396.83, 571.42]}},
 "naht_oben": {"art": "becken", "ueberlappung_m": 4.0}}
```

**Erläuterungen:**
- **Spline je Einheit** aus der Mittellinie (Kaskadennetz + River bzw. roher Lauf):
  - Anker sind Anfang, Ende und die Lippen; Vorhang-Fälle zuerst, dann nach Fallhöhe.
  - Dazwischen liegen die Punkte gleichmäßig mit Abstand ≥ 2 m, also 2–4 m (roher Lauf ≥ 5 m, also 5–10 m).
  - Lage, Breite, Tiefe und Tempo kommen je Punkt aus der Quelle.
  - `LINEAR` an jeder Lippe und am Punkt danach, damit die Spline nicht über die Stufe schwingt.
  - C2: 85 Punkte im Abstand 2,0–3,8 m.
- **`wasser_kollision`:** wie v1, je Eintrag dazu `einheit`, `hindernis_akteur` und `unterkante_ueber_spiegel_m`.
  - **Überspannend** heißt: `im_wasser` und Unterkante > Spiegel + 0,1 m. Solche Objekte haben keine Kollision und stehen in
    `ohne_wasser_kollision` (Entscheidung 5).
  - Gesamt: 22 043 Einträge, davon 21 519 eindeutig (v1: 22 825). **1 358 überspannt**, an C2 31 von 625.
- **`WH_<einheit>`:** genau ein Akteur je Einheit mit Hindernissen. Je Netz eine HISM-Komponente (`nanite: null` = lokal
  bestimmen, ISM bei Nanite).
  - Ein Objekt, das an zwei Gewässern liegt (Mündungen, überlappende Läufe), kommt nur in die Einheit mit dem kleinsten
    `abstand_rand_m`.
  - Die Nachbar-SWR erfasst es über `bottom_contour_actors`: Dort stehen alle WH, deren Objekte den Bereich schneiden.
    Das gilt für 127 Einheiten, z. B. C2 mit `WH_F_ERLENBACH_2_C2_E00`.
- **Fingerabdruck je Einheit:** dieselbe Formel (`FLUSS_SIM_FP1`), jetzt auf `bereich_cm` der Einheit (Box der Spline + 8 m
  Rand) und ihre eine Spline (`S|WBR_<einheit>|n`). Die Back-Liste (`back_liste_v2`) führt je Einheit SWR, River, WH, Nähte,
  Vorgänger/Nachfolger, `back_reihenfolge`, Auflösung und Zelle.
- **Kacheln** bleiben als Unterteilung einer Einheit. Sie tragen die 13k-Akteurgrenze und einen Teil-Fingerabdruck, der zeigt,
  wo sich etwas geändert hat. Es sind 559 Kacheln, jede in genau einer Einheit.

### 1.4 `faelle.vorhang`: Regel und Abgleich mit C2

**Regel** (`regeln.vorhang`): `vorhang: true` nur an einem Einzelabsturz (keine Kaskaden-Teilstufe, keine Schnelle) mit
- **Fallhöhe ≥ 3,0 m** (wie `vorhang_ab_m` des Planers, 14b), oder
- **senkrechter Felslippe:** Fallhöhe ≥ 2,0 m, Art `fall`, keine Holzstufe, horizontaler Versatz Lippe → Fuß ≤ 0,3 × Fallhöhe
  (also ≥ 73°).

**Begründung:**
- Die Simulation hat eine Höhe je Zelle (0,35–0,5 m). Einen Absturz zeichnet sie als Rinne über 1–2 Zellen.
- Unter 2 m liegt diese Rinne im weißen Schaumband an der Lippe. Sie liest sich als Wildwasser; das zeigt C2 (16b: „deutlich
  natürlicher als das Netz“).
- Ab 3 m, oder an einer senkrechten Wand schon ab 2 m, wird daraus eine geneigte „Glaswand“: kein freier Strahl, keine Luft
  dahinter, keine Gischtwolke. Das kann 2D nicht [Ableitung].
- Nur dort kommen Vorhang (Kaskadennetz-Bereich) und Schaumobjekte dazu; sonst gilt `schaum: "simulation"`. Die
  Niagara-Effekte bleiben an allen Fällen.

**Abgleich C2** (2-m-Plan; die IDs entsprechen den Stufen-IDs `F_ERLENBACH_1V_C2_s1_Sxx`):

| Stufe | Art | Fall | Versatz | **vorhang** | Grund |
|---|---|---|---|---|---|
| S03 | Kaskade 0,66 / 0,99 / 1,07 m | 2,72 m | – | **nein** | Teilstufen; Rinne wie im Bild |
| S04 | Fall | 4,67 m | 0,31 m | **ja** | ≥ 3 m (wie bisher) |
| S05 | Fall | 3,51 m | 3,01 m | **ja** | ≥ 3 m (wie bisher) |
| S09 | Fall | 2,63 m | 2,31 m | nein | geneigt (≈ 49°) |
| S10 | Fall | 2,84 m | 0,73 m | **ja (neu)** | senkrechte Lippe (≈ 76°), Klamm unterhalb |
| S13 | Fall | 2,96 m | 0,35 m | **ja (neu)** | senkrechte Lippe (≈ 83°) |
| S15 | Kaskade 0,80 / 0,97 / 0,56 m | 2,33 m | – | kein Fall | alle Teilstufen < 1 m, Simulation allein |

- Ihr seht S05 und S10 derzeit als steile Rinne. Bei S05 (3,5 m) ist der Vorhang wie bisher gesetzt. **S10 ist der
  Grenzfall:** Zeigt die Seitenansicht S10 ohne Vorhang so natürlich wie S09 daneben, setzt ihr
  `vorhang.senkrecht_ab_m` = 3,0. Dann gilt nur noch ≥ 3 m (99 Fälle). Das ist eine Zahl in `fluss_sim_regeln.json`
  (Rückfrage 2).
- **Gesamt:** 170 von 765 Fällen.
  - 99 Fälle ≥ 3 m (= alle bisherigen Planer-Vorhänge)
  - 71 senkrechte Lippen 2–3 m: 4 an Gefälle-Läufen, 67 an Sehens-Treppen (13f-Stufen sind senkrecht gebaut)
  - 595 Fälle ohne Vorhang: 292 Kaskaden-Teilstufen, 296 unter 2 m, 7 geneigt
- **Schaumobjekte:** 170 Aufprallteppiche, 784 Schaumstraßen, 277 Kehrwasser (v1: 765 / 2 507 / 2 291).

### 1.5 Prüfer und Lauf

- **Neu im Prüfer:**
  - lückenlose Kette der Einheiten mit Nähten (Fall: Lippe/Fuß, sonst gemeinsame Stelle und 4 m Überlappung)
  - jeder Abschnitt und jede Kachel in genau einer Einheit, keine Rest-Einheit < 30 m
  - Spline: Abstand ≥ 2 m und < 2 × Ziel, z nie steigend, Becken-Punkte auf dem Spiegel (± 2 cm), Ende an der Lippe =
    Oberwasser, Anfang am Fuß = Unterwasser
  - `achse_m` aus der Spline neu gerechnet, Auflösung ein Vielfaches von 32 in [32; 512], `zelle_m` = Achse / Auflösung,
    **Zelle ≤ 0,5 m** (FEHLER), Bach > 0,4 m (HINWEIS)
  - Quelle/Senke = eigener River
  - Vorhang-Regel aus den Fall-Feldern neu gerechnet; Schaum und Kaskadennetz nur an Vorhang-Fällen
  - global: jedes Kollisionsobjekt in genau einem WH, Zahlen stimmen, keine Pflanze, nichts Überspanntes;
    `bottom_contour_actors` vollständig
  - Back-Liste v2, Fingerabdrücke von Einheiten und Kacheln neu gerechnet
- **Ergebnis:** 0 FEHLER, 0 WARNUNG, 52 HINWEIS. Zwei Läufe sind byte-gleich (163 Dateien). Export ≈ 15 s, Prüfung
  ≈ 15 s auf 2 m.
- **Gegenproben** (C2 verfälscht), alle FEHLER mit Exit 1:
  - Auflösung 400
  - Vorhang an S09
  - Schaum an einem Fall ohne Vorhang
  - Objekt aus dem WH entfernt
  - Punkte 0,5 m auseinander
  - steigende Spline
  - überspanntes Objekt mit Kollision
  - abgesenkter Becken-Punkt
- **Beispiele aktualisiert** unter `antworten/fluss_sim/`: C2, `bergwald_06_karsee`, `zusammenfassung.json`,
  `back_liste_auszug.json`.
  - Karsee: Abfluss eine Einheit, 44 m, 128 → 0,345 m, 8 von 12 Fällen mit Vorhang.
  - Zuläufe Süd und West je eine Einheit, 64 → 0,24 / 0,31 m, je 6 von 6 Fällen mit Vorhang; sie erfassen gegenseitig
    ihre WH.
- README in `skripte/fluss_sim/` beschreibt Format v2, Regeln, Fingerabdruck je Einheit und Prüfer.

## 2. Frage 1: Die 3 Dispatches im gebackenen Zustand

### 2.1 Was es sehr wahrscheinlich ist

- **Zuordnung:** Eure Messung zählt die 3 Dispatches unter **`Grid2D_SW_River`**. Das ist das Niagara-System der Fluss-SWR
  (`river_sim_system`) [Test 16b, Doku].
  - Die Interaktion um die Spielfigur ist ein **anderes** System: Es hängt am `BasicShallowWaterSubsystem` als
    `shallow_water_niagara_simulation`. Das Subsystem hat dazu `normal_rt`, `velocity_rt` und eine `mpc` [Doku].
  - Es gibt das Interaktions-System einmal je Welt, nicht je Fluss [Ableitung]. Gesteuert wird es über
    `UShallowWaterSettings` (Kategorie „Interaction“: `MaxActivePawnNum`, `MaxImpulseForceNum`, `bVisualizeActivePawn`)
    und `GetPawnsInRange` [Doku].
  - **Die 3 Dispatches sind also nicht die Interaktion.**
- **Kandidaten im Fluss-System:**
  1. **Sekundär-Emitter** `SW_River_Secondary_Emitter` (GPU-Teilchen, bis 50 000, `M_SW_Foam`). Im gebackenen Bild
     (`t1_live_gegen_gebacken.jpg`, `c2_wcbs_klar.jpg`) sieht man weiter Gischtwolken am Fels und an den Lippen; die
     Teilchen laufen also auch gebacken. Ein GPU-Emitter braucht je Bild mindestens die Spawn/Update-Stufe, dazu meist
     Zähler bzw. indirekte Argumente [vermutlich].
  2. Eine **Gitter-Stufe**, die die gebackenen Daten (Höhe, Strömung, Schaum) in das Gitter bzw. ein Render Target liest,
     aus dem der Sekundär-Emitter seine Spawn-Orte nimmt [vermutlich].
  3. Ein **Kopiervorgang** in `baked_water_surface_rt` [Doku: Feld vorhanden; vermutlich nicht je Bild].
- **Erwartung:** 2 Dispatches Teilchen + 1 Gitter-Lesestufe. Mit Teilchen-Zahl und Bildschirmfläche wächst nur die
  Darstellung, nicht die Zahl der Dispatches [Ableitung]. D8 klärt das in ≈ 10 Minuten.

### 2.2 Kann man sie abschalten, wenn kein Pawn im Wasser ist?

- **„Pawn im Wasser“ ist das falsche Kriterium.** Die Gischt soll man auch sehen, wenn man am Ufer steht. Richtig ist
  **Entfernung zur Kamera + Sichtbarkeit**. Das Interaktions-System regelt sich über `MaxActivePawnNum` selbst und kostet
  nicht je Fluss.
- **Wege, sicherster zuerst:**
  1. **Eigener Manager** (Weltsubsystem in unserem Plugin, wie das Konzept in 16a a4):
     - Je SWR-Einheit die Box aus `bereich_cm` merken.
     - Nur Einheiten, deren Box näher als **R_an = 80 m** an der Kamera liegt (aus ab 100 m) **und** im Sichtkegel liegt,
       behalten den Sekundär-Emitter. Höchstens **4** gleichzeitig.
     - Schalten mit `NiagaraComponent.set_emitter_enable('SW_River_Secondary_Emitter', False)` bzw. `deactivate()` am
       `river_sim_system`. Die Funktion gibt es, der Fehler mit wirkungslosem Aufruf ist seit 5.4 behoben [Doku, 16a].
     - **Vorher prüfen (D8):** Zeichnet der Water Body in WCBS weiter, wenn das Niagara-System aus ist? Erwartet ja, denn
       das Gebackene liegt als Textur am Water Body [Ableitung aus 16a B5].
  2. **Niagara-Skalierbarkeit (Effect Type)** an einer **Kopie** von `Grid2D_SW_River` (Weg B, 16a, Rückfrage 4 dort noch
     offen):
     - „Cull by distance“ mit Max Distance ≈ 100 m
     - Sichtbarkeits-Culling
     - Significance Handler „Distance“ mit Max Instances 4 („nur die N wichtigsten bleiben, der Rest wird gekullt“) [Doku]
     - Unsicher ist, von welchem Punkt die Entfernung gemessen wird (Komponentenort oder Bounds). Bei 250-m-Einheiten
       wäre der Komponentenort falsch [vermutlich]. Außerdem muss die Kopie in den Projekteinstellungen stehen.
  3. **Teilchen-Emitter ganz aus**, wenn die Gischt aus den Nature-Water-FX an den Fällen reicht: einfach, aber dann fehlt
     die Gischt an Felsen in Rinnen.
- **Nicht empfohlen ohne Test:** die SWR-Akteure in ein Runtime-Grid mit kleinem Ladebereich legen. Die gebackenen Daten
  „gehören“ der SWR-Komponente [Doku]. Entlädt die SWR, verliert der Water Body womöglich sein Gebackenes [Ableitung].

### 2.3 Lohnt sich das bei 0,2 ms? Hochrechnung

- **Gleichzeitig geladene Einheiten:** gezählt aus den 249 Einheiten des Exports (Mittelpunkt der Box im Radius um eine
  Einheit). „Flächengewichtet“ heißt: in 512²-Äquivalenten, falls die Kosten mit der Zellzahl wachsen.

| Ladebereich (Radius) | Einheiten max / Median | Kosten bei 0,2 ms je Einheit | flächengewichtet |
|---|---|---|---|
| 256 m (Standard-Ladebereich WP [Drittquelle]) | 17 / 4 | 3,4 / 0,8 ms | 1,5 / 0,6 ms |
| 1 km (Grid „Wasser“, Richtwert aus der HLOD-Antwort [Projekt]) | 62 / 26 | **12,4 / 5,2 ms** | 7,2 / 3,1 ms |
| 2 km (MainGrid-Richtwert) | 101 / 73 | 20 / 15 ms | 12 / 8 ms |
| 3 km | 175 / 118 | 35 / 24 ms | 21 / 14 ms |

- **Bewertung:** Ohne Abschalten sprengt das das Budget aus Datei 16 (1,5 ms für Wasser-Simulation und Effekte) schon
  bei 256 m im dichten Gebiet und bei 1 km überall.
  - Mit dem Manager (≤ 4 Einheiten, ≤ 100 m, sichtbar) bleiben **≤ 0,8 ms**, meist 0,2–0,4 ms.
  - **Es lohnt sich also unbedingt; es ist Pflicht** [Schätzung].
- **Annahme in der Rechnung:** Ein geladenes, aber nicht sichtbares Niagara-System rechnet ohne Effect-Type-Culling weiter.
  Die Doku sagt, dass Entfernungs-, Sicht- und Anzahl-Culling nur über den Effect Type wirken [Doku]. Ob der SWR-Akteur
  selbst etwas abschaltet, ist offen. D8 Schritt 4 misst das.

### 2.4 Diagnose D8 (lokal, PIE an C2, nichts speichern)

1. **Namen der Dispatches:**
   - PIE starten, an C2 teleportieren, `ProfileGPU`.
   - Im Baum `Grid2D_SW_River` aufklappen und die drei Einträge mit Namen notieren (Emitter-/Stufen-Namen) [vermutlich
     sichtbar].
   - Zusätzlich **Niagara Debugger** (Tools → Debug → Niagara Debugger): System-Filter `Grid2D_SW_River`, aktive Emitter und
     Teilchenzahl je Emitter.
2. **Schalten und messen.** Je Schritt `ProfileGPU` und ein Bild; zeichnet der Water Body weiter?

```python
import unreal
welt = unreal.EditorLevelLibrary.get_game_world()                    # PIE-Welt
swr  = [a for a in unreal.GameplayStatics.get_all_actors_of_class(welt, unreal.ShallowWaterRiver)]
print([a.get_name() for a in swr])                                   # SWR_C2 heraussuchen
comp = swr[0].get_component_by_class(unreal.ShallowWaterRiverComponent)
nc   = comp.get_editor_property('river_sim_system')
print(nc.get_asset().get_path_name(), nc.is_active())
def gpu(): unreal.SystemLibrary.execute_console_command(welt, 'ProfileGPU')
# a) nur Gischt aus:           nc.set_emitter_enable('SW_River_Secondary_Emitter', False); gpu()
# b) System pausiert:          nc.set_emitter_enable('SW_River_Secondary_Emitter', True); nc.set_paused(True); gpu()
# c) System aus:               nc.set_paused(False); nc.deactivate(); gpu()
# d) zurueck:                  nc.activate(True)
```

3. **Interaktion:** Spielfigur ins Wasser laufen lassen. Erscheint ein zweites System im ProfileGPU? Wie viele Dispatches
   und ms? Zugriff [vermutlich]:
   `sub = unreal.SubsystemBlueprintLibrary.get_world_subsystem(welt, unreal.BasicShallowWaterSubsystem)`, dann
   `sub.get_editor_property('shallow_water_niagara_simulation').is_active()` einmal am Ufer und einmal im Wasser.
4. **Kulling heute:**
   - 300 m wegteleportieren bzw. von C2 wegschauen und `ProfileGPU`. Laufen die 3 Dispatches weiter, gibt es kein
     eingebautes Culling, und die Hochrechnung 2.3 gilt.
   - Dabei auf die „Wasserwand“ achten, die ein Forenbericht bei gebackenen Flüssen in der Entfernung meldet (verschwindet
     beim Näherkommen) [Forum].
- **Ergebnis zurück:** drei Namen, ms je Schritt a–d, „Water Body zeichnet ja/nein“ bei c, Interaktion ms.

## 3. Frage 2: Schaum in steilen Rinnen dünner

**Ausgangslage:** Die Werte in `MI_EL_SWR_Klar` sind
- `SimFoam Contrast` 2
- `Foam powr` 0,6
- `Foam Boost` 0,8
- `Foam Opacity` 0,9
- `Foam Texture Blend Min` 0,6
- `Sim Foam Scale` 350 (Standard)

In den Rinnen ist der Schaum fast flächig weiß. Das heißt: Der Schaumwert ist dort **gesättigt** (≈ 1). Kontrast und Kurve
wirken auf gesättigte Werte kaum. Erst muss der Wert unter 1 kommen, dann formt man ihn [Ableitung].

**Wichtig:** In WCBS liest unser Material die gebackene Schaumtextur. Materialwerte wirken **ohne neues Backen** sofort
[Ableitung aus 16a B5].

**Testleiter** (je Zeile einzeln, Kameras `kn0_unten`, `s1`, `kn0_nah_s119`):

| Reihenfolge | Parameter | Stufen | Erwartete Wirkung |
|---|---|---|---|
| 1 | `Foam Boost` | 0,8 → **0,6 → 0,45 → 0,3** | Faktor auf den Schaum [vermutlich]; holt die Rinnen aus der Sättigung, Becken bleiben klar |
| 2 | `Foam powr` | 0,6 → **1,0 → 1,5 → 2,0** | Exponent [vermutlich]; mittlere Werte werden dünn, Kerne an Lippe und Fels bleiben weiß, es entstehen Lücken mit dunklem Wasser |
| 3 | `SimFoam Contrast` | 2 → **3 → 4** | nur, wenn danach ein grauer Schleier bleibt; trennt Schaum und Wasser schärfer |
| 4 | `Foam Texture Blend Min` | 0,6 → **0,75 → 0,9**, Gegenprobe 0,45 | Schwelle, ab der die Schaumtextur statt Fläche erscheint [vermutlich]; Richtung im A/B bestimmen. Ziel: Schaum als Flocken und Streifen statt Decke |
| 5 | `Foam Opacity` | 0,9 → **0,75 → 0,6** | zuletzt; macht allen Schaum durchscheinend, auch den Saum an den Lippen |
| 6 | `Sim Foam Scale` | 350 → **700**, Gegenprobe 175 | sehr wahrscheinlich die Kachelgröße der Schaumtextur in cm, nicht die Menge [vermutlich]; ändert die Flockengröße. Ändert sich die Menge, gehört es vor Schritt 1 |
| gezielt | `Sim Foam Dpeth Min` (sic) | 8 → **15 → 25** | Schaum erst ab dieser Wassertiefe in cm [vermutlich]. In steilen Rinnen ist das Wasser dünn, also wirkt es genau dort. Nebenwirkung: Saum an flachen Lippen wird schwächer (16a b3) |

- **Ziel:** In den Rinnen 40–60 % weiß, dazwischen dunkle Wasserstreifen; Becken klar; ein weißer Saum an den Lippen
  bleibt. Bei 30–45 % Gefälle (C2, 16a) ist Wildwasser physikalisch richtig. Gesucht ist „durchbrochen“, nicht „ohne“.
- **Startpaket, falls schnell etwas stehen soll:** `Foam Boost` 0,45, `Foam powr` 1,5, Rest wie jetzt.

**Schaumschwelle der Simulation selbst:**
- Die Simulation schreibt einen Schaumwert in die gebackenen Daten. In 2D-Flachwasser-Verfahren entsteht Schaum
  üblicherweise, wenn eine Zelle eine **Geschwindigkeitsschwelle** und eine **Wirbel- bzw. Krümmungsschwelle**
  überschreitet; er klingt mit einer Zerfallsrate ab [Drittquelle, allgemein, nicht Epic].
- Namen der Benutzerparameter von `Grid2D_SW_River` sind in keinem lesbaren Auszug belegt. Epics „Parameter Reference“
  ist nicht erreichbar. **Vermutlich** heißen sie etwa „Foam Velocity Threshold“, „Foam Curvature/Slope“, „Foam
  Decay/Dissipation“ bzw. „Foam Spawn Rate“.
- Liste holen mit D1 aus 16a (Benutzerparameter-Panel der Niagara-Komponente). Gesucht sind Namen mit „Foam“,
  „Threshold“, „Decay“, „Velocity“.
- **Zielwerte, falls vorhanden:** Schaum ab ≈ 1,5 m/s statt darunter; Abklingen 2–4 s.
- **Diese Werte brauchen neues Backen.** Darum zuerst die Materialleiter.

## 4. Klarer Bach von der Seite unauffällig

- **Glanzlichter:**
  - `Water Roughness` 0,02 → **0,04–0,06**: breitere Sonnen- und Himmelsglanzlichter, sichtbar aus mehr Winkeln.
  - `Water Specular` 0,225 bleibt nahe am physikalischen Wert. Höchstens **0,3**; mehr wirkt wie Lack.
- **Leichte Normalen:**
  - `Default Near Normal Strength` 0,25 → **0,4**.
  - In WCBS `Sim Velocity Normal Strength` von 10 (16a-Vorschlag gegen Marmor) auf **15–20**. Die Strömung zeichnet dann
    feine Riffel; das Marmormuster kam aus LIVE_SIM, nicht aus WCBS.
- **Dunklerer Grund im Bett:**
  - Landschafts-Lage „Bachbett nass“ unter dem Wasser mit Grundfarbe × 0,6 und Rauheit 0,3.
  - Dazu Kiesel bzw. kleine Steine (Megascans, ohne Wasser-Kollision, < 0,4 m) im Bett. Kontrast zum Ufer macht die
    Wasserfläche lesbar.
- **Ein Hauch Farbe:**
  - Absorption 250 / 1 430 / 2 000 → **180 / 900 / 1 400** cm. In 0,5–1 m tiefen Becken wird es leicht grün-blau, der Grund
    bleibt sichtbar.
  - `Refraction` 1,15 → **1,2**: Der Grund verzerrt sichtbar.
- **Ufer-Nässe:**
  - Ein 0,2–0,5 m breites dunkles, glänzendes Band an Ufer und Felsen knapp über dem Spiegel.
  - Unser `M_EL_Strasse_V2` hat dafür schon eine Nässe-Logik (`Naesse_Flaeche`, `Naesse_Glanz` 0,32, `Naesse_Max`)
    [Projekt]. Als Material-Funktion übertragen auf Landschaft und `M_EL_Fels_MS`, Maske über die Höhe zum Spiegel.
  - Die Spiegelhöhe kann aus der Spline der Einheit kommen, als Planer-Lage „Ufer_nass“ = Breite + 0,3–0,6 m [Ableitung].
- **Uferschaum:** `ELD_Ufer_Schaum` 0,45 lassen. Ein dünner Saum an Ufer und Felsen zeigt die Wasserlinie.

## 5. Was lokal zu tun ist

Commits: **`6f7f315`** (Exporter, Prüfer, Regeln v2, README, Beispiele) und der Commit dieser Antwort (Nachtrag 16b in
Datei 16).

1. `git pull`, dann den Exporter und Prüfer auf 1 m (Befehl wie bisher, siehe README):
   ```
   python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle \
          --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt --aus export/unreal/welt/fluss_sim
   python -I recherche/antworten/skripte/fluss_sim/fluss_sim_pruefen.py export/unreal/welt/fluss_sim \
          --gefaelle export/unreal/welt/gefaelle --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt
   ```
2. **Bau-Werkzeug auf v2 umstellen:**
   - Je `swr_einheiten[]` einen `WaterBodyRiver` (`water_body.spline`, `overlap_material_priority`).
   - Einen `ShallowWaterRiver` (`swr`: Auflösung, Quelle/Senke, Tags, `bottom_contour_actors`, Material `MI_EL_SWR_Klar`).
   - Einen `WH_<einheit>` (`hindernis_akteur`, Instanzen verschieben, Liste `umzug`).
   - Objekte in `ohne_wasser_kollision` bekommen **kein** Tag.
3. **Kaskadennetz** nur an Fällen mit `vorhang: true` auf `bereich_s_m` zuschneiden. **Schaumobjekte** nur dort.
   Niagara-Effekte an allen Fällen lassen.
4. **Backen je Einheit** in `back_reihenfolge`, danach den Editor-Fingerabdruck je Einheit speichern.
   - Bei geteilten Strecken zuerst die obere Einheit backen.
   - **Naht prüfen:** an einer Becken-Naht Wasserhöhe beider Seiten (Ziel ≤ 2 cm), Bild; an einer Fall-Naht, ob die Kante
     unter dem Vorhang liegt.
   - Gute Testfälle: `B_R_M1_P0_03` (Fall + Becken), `F_HAUPTFLUSS_3_F5` (ruhige Stellen).
5. **C2:** euer `SWR_C2` neben die Werte von `F_ERLENBACH_1V_C2_E00` legen (Achse, Auflösung, Rastergröße der
   `water_info_texture`). Bei S09 und S10 die Seitenansicht ohne und mit Vorhang vergleichen (Rückfrage 2).
6. **D8** (Abschnitt 2.4) ausführen, danach den Manager (2.2 Weg 1) bauen.
7. **Schaumleiter** (Abschnitt 3) und **Sichtbarkeit** (Abschnitt 4) an `MI_EL_SWR_Klar` testen, Bilder unter `bilder/swr/`.

## Quellen

Alle Epic-, Forums- und lilys-Seiten waren aus der Cloud nicht lesbar (Proxy 403/DNS); die Inhalte stammen aus
Suchmaschinen-Auszügen.

Epic-Doku und API:
- [Python: unreal.BasicShallowWaterSubsystem](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/BasicShallowWaterSubsystem) – `normal_rt`, `velocity_rt`, `mpc`, `shallow_water_niagara_simulation` (Asset aus den Projekteinstellungen)
- [Python: unreal.ShallowWaterSubsystem](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterSubsystem) – `set_water_body_mid_parameters`
- [API: UShallowWaterSettings](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterSettings) und [Python: unreal.ShallowWaterSettings](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterSettings) – Kategorie Interaction: `MaxActivePawnNum`, `MaxImpulseForceNum`, `bVisualizeActivePawn`; `output_velocity`
- [API: UShallowWaterSubsystem::GetPawnsInRange](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterSubsystem/GetPawnsInRange)
- [API: UBasicShallowWaterSubsystem](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UBasicShallowWaterSubsystem)
- [Python: unreal.BakedShallowWaterSimulationComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/BakedShallowWaterSimulationComponent), [WaterBodyRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyRiverComponent) – gebackene Daten „owned by a UShallowWaterRiverComponent“
- [Python 5.0: unreal.NiagaraSystemScalabilitySettings](https://docs.unrealengine.com/5.0/en-US/PythonAPI/class/NiagaraSystemScalabilitySettings.html), [NiagaraSystemScalabilityOverride](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/NiagaraSystemScalabilityOverride) – Cull by distance, Max Distance, Sichtbarkeits-Culling, Significance Handler („only the N most significant will be kept“)
- [Tutorial: Baked River Simulations – Parameter Reference](https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference), [Forum-Thread](https://forums.unrealengine.com/t/2512112) – Inhalt nicht erreichbar
- [Niagara Fluids Reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/niagara-fluids-reference-in-unreal-engine) – Shallow-Water-Vorlage
- [World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine) – Streaming-Quelle als Kugel mit dem Ladebereich
- [Single Layer Water Shading Model](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine)

Forum und Drittquellen:
- [Forum: ShallowWaterRiver and Landscape](https://forums.unrealengine.com/t/shallowwaterriver-and-landscape/2818892) – „Wasserwand“, die beim Näherkommen verschwindet (gebackener Fluss)
- [lilys.ai: Baked River Simulation UE 5.6 (KI-Zusammenfassung eines Videos)](https://lilys.ai/de/notes/unreal-engine-5-20251128/witcher-4-baked-water-sim-ue5) – „Water Component with Baked Sim“ empfohlen (Gebackenes plus Lauf-Wellen); [spanische Fassung](https://lilys.ai/es/notes/unreal-engine-5-20251128/witcher-4-baked-water-sim-ue5-tutorial) – Absorption/Scattering im Baked-Sim-Material
- [bugnet: Niagara GPU simulation stops at distance](https://bugnet.io/blog/fix-unreal-niagara-gpu-simulation-stops-at-distance) – Bounds- und Effect-Type-Culling (Drittquelle)
- [uhiyama-lab: World Partition und Level Streaming](https://uhiyama-lab.com/en/notes/ue/level-streaming-optimization/) – Standard Loading Range 25 600 uu (256 m), Zelle 12 800 uu (Drittquelle)
- [80.lv: Working with Niagara Fluids to Create Water Simulations](https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations) – Schaum/Sekundärteilchen über Geschwindigkeits- und Wirbelschwelle (allgemein)

Projekt:
- `antworten/hlod-fernansicht-world-partition.md` – Richtwerte MainGrid 1 km / 2–3 km, Grid „Wasser“ 1 km / 1 km
- `vorlagen/daten/material_parameter.json` – `M_Eldarien_Wasser_Schaum8` (Schaum-, Normal-, Specular-Werte), `M_EL_Strasse_V2` (Nässe)
- `antworten/16a-swr-einrichtungstest-teil1.md` (B3, B5, D1), `antworten/16-shallow-water-alle-gewaesser.md`

## Rückfragen

1. **C2-Zelle:** Lokal steht „179 m, 512, ≈ 0,35 m“. Auf den 2-m-Daten ist der Lauf 203 m lang, die Box 91 × 218 m, also
   0,425 m. Habt ihr die 0,35 m am Raster gemessen (Größe der `water_info_texture`) oder als 179 m / 512 gerechnet? Ist die
   1-m-Strecke kürzer? Das entscheidet, ob die Box-Achse die richtige Größe für die Auflösung ist.
2. **Vorhang an senkrechten Lippen 2–3 m** (C2: S10, S13; 67 Sehens-Treppenfälle): Behalten? Oder `senkrecht_ab_m` = 3,0,
   dann gilt nur ≥ 3 m (99 Fälle)? Bitte am Bildvergleich S09 gegen S10 entscheiden.
3. **Bäche mit Zelle 0,4–0,5 m** (42 Einheiten, Box 205–256 m): so lassen? Oder Bäche bei 0,4 m teilen? Dann gäbe es etwa
   40 Einheiten und Nähte mehr.
4. **Becken-Naht mit 4 m Überlappung:** Zeichnen zwei überlappende Water Bodies in WCBS sauber über
   `overlap_material_priority`? Wenn nicht: Variante ohne Überlappung (gemeinsamer Endpunkt) testen; das ist eine Zahl in den
   Regeln (`ueberlappung_m` = 0).
5. **Überspannt:** 1 358 Objekte (6 %) verlieren die Wasser-Kollision. Darunter sind auch Uferblöcke, deren Unterkante über
   dem Wasser liegt und deren Grundriss nur knapp über die Wasserkante reicht. Passt das zu Entscheidung 5? Oder soll die Regel
   nur greifen, wenn das Objekt die Wassermitte überdeckt (echte Brücke/Überhang)?
6. **Manager für die Gischt-Teilchen** (2.2 Weg 1) als eigenes Weltsubsystem im Plugin: einverstanden? Alternativ die Kopie
   des Niagara-Systems mit Effect Type (Weg 2, offene Rückfrage 4 aus 16a Nachtrag 2).

## Nachtrag 16c – T2-10 und Ablösung von v2

- **T2-10 (Höhe): Kein Sehens-Bach liegt über 655 m.**
  - Höchster Sehens-Bach: `gletscher_05_die_waechte` Mühlenbach mit **307,1 m**.
  - Höchstes Sehens-Wasser überhaupt: Wasserfall-Kante `fjord_02_schleierwand` mit 361,2 m.
  - Frost: höchstens 43,3 m. Welt-Gewässer: höchstens 288,2 m (`F_HAUPTFLUSS_1`).
  - Gelände in den SWR-Rechtecken: höchstens 331,9 m.
  - Die fp16-Grenze (65 504 cm) trifft also kein Gewässer; der Abstand beträgt mindestens 294 m.
- **Rückfrage 1 (C2-Zelle)** ist durch eure Messung geklärt: Der SWR-Bereich ist das Rechteck um den Fluss, Zelle =
  längste Seite / Auflösung.
- **Rückfrage 3 (Bach-Zelle 0,4–0,5 m)** entfällt: Mit Auflösung bis 2048 liegen Bäche bei 0,25 m, höchstens 0,30 m.
- **Format v2 ist abgelöst** durch v3: ein `WaterBodyRiver` und eine SWR je Gewässer. Siehe
  [`16c-ferat-ein-fluss-je-gewaesser.md`](16c-ferat-ein-fluss-je-gewaesser.md).

