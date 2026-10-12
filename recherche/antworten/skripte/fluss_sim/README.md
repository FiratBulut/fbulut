# fluss_sim – Exporter für Shallow Water River (Entscheidung 16)

Ferat hat am 12.10.2026 entschieden: Alle Bäche und Flüsse laufen mit `WaterBodyRiver` + `ShallowWaterRiver`
(UE 5.8.3, Plugins Water + Niagara Fluids). Die Simulation wird im Editor **gebacken**. Seen bleiben `WaterBodyLake`.
Begründung und Arbeitsablauf stehen in [`../../16-shallow-water-alle-gewaesser.md`](../../16-shallow-water-alle-gewaesser.md).

**Format v2 (16b, `fluss_sim_v2`):** Die Einheit für Simulation, Backen und Fingerabdruck ist die **Strecke**: je Gewässer
**ein** `ShallowWaterRiver` mit **einem** `WaterBodyRiver` (lokal an C2 bestätigt: 1 SWR über die ganze Strecke,
Auflösung 512, gebacken 0,2 ms). Nur Strecken, deren Box bei 512 Zellen > 0,5 m je Zelle ergäbe (≈ 256 m), werden geteilt.
Vorhang und Schaumobjekte gibt es nur noch an echten Fallkanten (Regel unten); alle anderen Fälle zeichnet die Simulation
als Wildwasserrinne. Antwort dazu: [`../../16b-swr-c2-ganze-strecke.md`](../../16b-swr-c2-ganze-strecke.md).

Der Exporter **liest nur**: die Planer-Ausgaben von `gefaelle_plan.py` (`<lauf>/plan.json`, `instanzen/`,
`gelaende/`) und der Sehens-Planer (`<biom>/orte.json`, `sw_<biom>/`, `gelaende/`) sowie die Weltdaten. Er ändert
keine Stufe, kein Becken, keine Lippe und kein Gelände. Die Treppen der Sehens-Bäche bleiben exakt wie 13f; der
Prüfer vergleicht Lippen- und Fußhöhen mit der Quelle.

| Datei | Inhalt |
|---|---|
| `fluss_sim_export.py` | Exporter: `fluss_sim.json` je Gewässer (v2: `swr_einheiten` führend), `back_liste.json` (je SWR-Einheit), `zusammenfassung.json`; enthält die Referenz-Funktionen für den Fingerabdruck |
| `fluss_sim_pruefen.py` | Prüfer (FEHLER/WARNUNG/HINWEIS wie `gefaelle_pruefen.py`), Exit-Code 1 bei FEHLER |
| `fluss_sim_regeln.json` | alle Zahlen (Fall-Schwelle, Abschnittslängen, Kollision, Schaum, Vorhang, SWR-Einheit und Teilung, Kacheln, Fingerabdruck), Version 2 |

## Aufruf

Cloud (2 m), Planer-Ausgaben vorher in den Scratchpad erzeugen:

```
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --alle --daten2m recherche/vorlagen/daten/sehens --aus <s>/gef
python -I recherche/antworten/skripte/sehens_<biom>/sehens_<biom>.py --daten2m recherche/vorlagen/daten/sehens --aus <s>/sehens/<biom>   # je Biom
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle <s>/gef --sehens <s>/sehens \
       --daten2m recherche/vorlagen/daten/sehens --aus <s>/fs
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_pruefen.py <s>/fs --gefaelle <s>/gef --sehens <s>/sehens \
       --daten2m recherche/vorlagen/daten/sehens [--vergleich <s>/fs_zweiter_lauf]
```

Lokal (1 m), nach den Planer-Läufen auf 1 m:

```
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle \
       --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt \
       --aus export/unreal/welt/fluss_sim
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_pruefen.py export/unreal/welt/fluss_sim \
       --gefaelle export/unreal/welt/gefaelle --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt \
       --daten1m export/unreal/welt
```

Optionen: `--nur ID …` (Lauf-, Fluss- oder Ort-IDs; der Objekt-Pool wird trotzdem ganz geladen; die Zuordnung der
Hindernis-Objekte zu Einheiten anderer Gewässer fehlt dann), `--ohne-fluesse`, `--ohne-roh`, `--regeln`.
Laufzeit 2 m: ~15 s Export, ~15 s Prüfung (ohne Planer).

**Ausgabe** (`--aus`), nicht ins Repo (25 MB auf 2 m):

```
gefaelle/<lauf>/fluss_sim.json          je Lauf mit Plan (98) und je Lauf der 161 Strecken ohne Plan (25, roh)
sehens/<biom>/<ort>/fluss_sim.json      je Sehens-Ort mit Bach (26 Orte, 42 Bäche)
fluesse/<fluss>/fluss_sim.json          Flüsse >= 15 m Breite ohne Plan und ohne Strecke (12, roh)
back_liste.json                         alle SWR-Einheiten mit Fingerabdruck und Back-Reihenfolge (back_liste_v2)
zusammenfassung.json                    Zahlen je Kategorie
```

Beispiele im Repo: [`../../fluss_sim/`](../../fluss_sim/) (C2, Sehens-Ort `bergwald_06_karsee`, Zusammenfassung,
Auszug der Back-Liste).

## Format `fluss_sim.json` (v2)

Neu in v2 sind `swr_einheiten`, `ohne_wasser_kollision`, je Fall `vorhang`/`vorhang_grund`/`versatz_m`/`einheit_*`, je
Kollisionsobjekt `einheit`/`hindernis_akteur`/`unterkante_ueber_spiegel_m` und je Abschnitt bzw. Kachel `einheit`.
Gekürzt aus C2:

```json
{"format": "fluss_sim_v2", "regeln_version": 2, ...,
 "gewaesser": [{"id": "F_ERLENBACH_1V_C2", ...,
   "swr_einheiten": [{
     "id": "F_ERLENBACH_1V_C2_E00", "s_m": [0.0, 203.16], "laenge_m": 203.16,
     "abschnitte": ["…_A00", …, "…_A17"], "kacheln": ["…_K00", "…_K01", "…_K02"], "faelle_innen": ["…_s1_S01_T2", …],
     "naht_oben": {"art": "laufanfang", "s_m": 0.0, "fall": null, "ueberlappung_m": 0.0},
     "naht_unten": {"art": "laufende", "s_m": 203.16, "fall": null, "ueberlappung_m": 0.0},
     "vorgaenger": [], "nachfolger": [], "back_reihenfolge": 0,
     "water_body": {"id": "WBR_F_ERLENBACH_1V_C2_E00", "klasse": "WaterBodyRiver", "affects_landscape": false,
                    "overlap_material_priority": 1,
                    "spline": {"s_m": [0.0, 203.16], "punkte": [[-172182.5, -239417.0, 10206.1, 2879.3, 91.7, 300.0], …],
                               "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
                               "punkt_typen": […], "tangenten_cm": […], "punkte_s_m": [0.0, 2.0, 4.0, …], "punkt_rollen": […]}},
     "swr": {"id": "SWR_F_ERLENBACH_1V_C2_E00", "klasse": "ShallowWaterRiver", "typ": "bach", "breite_median_m": 21.73,
             "zelle_ziel_m": 0.35, "achse_m": 217.64, "box_m": [91.47, 217.64], "resolution_max_axis": 512, "zelle_m": 0.425,
             "raster_erwartet": [216, 512],
             "source_river_water_bodies": ["WBR_F_ERLENBACH_1V_C2_E00"], "sink_river_water_bodies": ["WBR_F_ERLENBACH_1V_C2_E00"],
             "bottom_contour_tags": ["SWR_Hindernis"],
             "bottom_contour_actors": ["WH_F_ERLENBACH_1V_C2_E00", "WH_F_ERLENBACH_2_C2_E00"],
             "bottom_contour_landscape_actors": "lokal", "use_capture": true, "match_spline": true,
             "render_state": {"backen": "LIVE_SIM", "spiel": "WATER_COMPONENT_WITH_BAKED_SIM", "ersatz": "BAKED_SIM"},
             "material": {"water_body": "MI_EL_SWR_Klar", "baked_sim_material": "MI_EL_SWR_Klar"}},
     "bereich_cm": [-180689.4, -241656.6, -169942.9, -218292.2],
     "hindernis_akteur": {"id": "WH_F_ERLENBACH_1V_C2_E00", "klasse": "Actor", "tags": ["SWR_Hindernis", "SWR_E_F_ERLENBACH_1V_C2_E00"],
                          "ursprung_cm": [-175316.1, -229974.4, 0.0],
                          "komponenten": [{"netz": "/Game/…/texndcpda_tier_0", "klasse": "HISM", "nanite": null, "kollision": "wie_quelle",
                                           "instanzen": [{"ref": {…}, "pos_cm": […], "quat_xyzw": […], "skala": […], "lage": "im_wasser"}, …]}, …],
                          "akteure_mit_tag": [{"ref": {"quelle": "…", "liste": "akteure", "index": 0}, …}, …],
                          "n_instanzen": 526, "n_komponenten": 20, "n_akteure_mit_tag": 46, "umzug": "verschieben"},
     "fingerabdruck": "7d2b1daf…", "fingerabdruck_teile": {"gelaende": "…", "splines": "…", "objekte": "…"},
     "n_hoehen": 6318, "raster_cm": 200.0, "n_objekte": 614}],
   "abschnitte": [{"id": "…_A00", "einheit": "…_E00", … wie v1 …,
                   "water_body": {"klasse": "WaterBodyRiver", "affects_landscape": false, "nur_rueckfall": true, …}}, …],
   "faelle": [{"id": "…_s1_S10", "fall_m": 2.84, "versatz_m": 0.73, "vorhang": true,
               "vorhang_grund": "senkrechte felslippe (versatz 0.73 m <= 0.3 x fall)",
               "einheit_oben": "…_E00", "einheit_unten": "…_E00",
               "kaskadennetz": {"id": "…_KN0", "bereich_s_m": [104.25, 106.75], "vorhang": true, "vorhang_planer": false},
               "schaum": "objekte", "schaum_objekte": [ … ], …},
              {"id": "…_s1_S09", "fall_m": 2.63, "versatz_m": 2.31, "vorhang": false,
               "kaskadennetz": {"id": "…_KN0", "bereich_s_m": null, "vorhang": false, "vorhang_planer": false},
               "schaum": "simulation", "schaum_objekte": [], …}, …],
   "wasser_kollision": [{… wie v1 …, "einheit": "…_E00", "unterkante_ueber_spiegel_m": -3.57,
                         "hindernis_akteur": "WH_F_ERLENBACH_1V_C2_E00"}, …],
   "ohne_wasser_kollision": [{… "lage": "im_wasser", "unterkante_ueber_spiegel_m": 0.24, "wasser_kollision": false,
                              "grund": "ueberspannt"}, …],
   "sim_bereiche": [{"id": "…_K00", "einheit": "…_E00", "rolle": "unterteilung", … wie v1 …}, …]}]}
```

- **Bau-Werkzeug (v2):** je Einheit **einen** `WaterBodyRiver` aus `water_body.spline` (Punkttypen, Tangenten,
  Metadaten wie v1), **einen** `ShallowWaterRiver` mit den Feldern aus `swr` und **einen** `WH_<einheit>` aus
  `hindernis_akteur`. Die Abschnitte sind nur noch Unterteilung (Becken, Lippen, Fall-Zuordnung, Prüfung); ein
  `WaterBodyRiver` je Abschnitt ist der Rückfall, falls eine Spline je Einheit lokal nicht geht.
- **`hindernis_akteur`** ist `null`, wenn der Einheit kein Objekt zugeordnet ist. Ein Objekt, das in mehreren Gewässern
  steht (Mündungen, überlappende Läufe), kommt genau in den WH-Akteur der Einheit mit dem kleinsten `abstand_rand_m`;
  die anderen Einheiten erfassen es über `bottom_contour_actors` (alle WH, deren Objekte den `bereich_cm` schneiden).
- **Spline je Einheit:** Anfang, Ende und Lippen (Vorhang-Fälle zuerst, dann nach Fallhöhe) als Anker, dazwischen
  gleichmäßig mit Abstand ≥ 2 m (roh ≥ 5 m), also 2–4 m (roh 5–10 m). Lippen, die < 2 m an einem stärkeren Anker liegen,
  fallen weg. `LINEAR` an jeder Lippe und am Punkt danach. Endet die Einheit an einem Fall, liegt der letzte Punkt auf
  dem Oberwasser der Lippe; beginnt sie an einem Fall, liegt der erste auf dem Fuß.

### Format v1 (Abschnitte, Fälle, Kollision; in v2 unverändert, soweit oben nicht anders gesagt)

```json
{"format": "fluss_sim_v1", "regeln_version": 1, "fall_schwelle_m": 1.0, "daten": "2m (Cloud-Test)",
 "gewaesser": [{
   "id": "F_ERLENBACH_1V_C2", "kategorie": "gefaelle", "art": "gefaelle",
   "quelle": {"plan": "gefaelle/F_ERLENBACH_1V_C2/plan.json", "wasser_koerper": ["…_KN0", "…_R0"]},
   "laenge_m": 203.16,
   "abstuerze": [{"id": "…_s1_S01_T2", "s_lippe_m": 14.25, "s_fuss_m": 14.75, "fall_m": 1.27, "rampe": false}, …],
   "abschnitte": [{
     "id": "F_ERLENBACH_1V_C2_A01", "s_m": [14.75, 21.85], "laenge_m": 7.1, "teil": [1, 1],
     "punkte": [[-172690.6, -238034.1, 9818.7, 2310.2, 228.2, 150.0], …],
     "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
     "punkt_typen": ["CURVE_CLAMPED", …, "LINEAR", "LINEAR", …], "tangenten_cm": [[-64.7, 121.7, -2.8], …],
     "punkte_s_m": [14.75, 16.12, …], "punkt_rollen": ["becken", …, "lippe", "fuss", …],
     "anschluss": {"oben_fall": "…_S01_T2", "unten_fall": "…_S01_T4", "spiegel_anfang_cm": 9818.7,
                   "spiegel_ende_cm": 9717.6, "rest_oben": false, "rest_unten": false},
     "faelle_innen": [],
     "becken": [{"s_m": [14.75, 18.87], "spiegel_cm": [9818.7, 9810.4], "oben": "…_S01_T2", "unten": "…_S01_T3"}, …],
     "water_body": {"klasse": "WaterBodyRiver", "affects_landscape": false}}, …],
   "faelle": [{
     "id": "…_s1_S04", "stufe": "…_s1_S04", "teil": 0, "art": "fall", "fall_m": 4.67,
     "s_lippe_m": 52.65, "s_fuss_m": 53.15, "abschnitt_oben": "…_A04", "abschnitt_unten": "…_A05", "im_abschnitt": false,
     "lippe_cm": [-174147.3, -234539.3, 8884.6], "fuss_cm": [-174161.7, -234491.4, 8417.3], "lippe_breite_m": 13.54,
     "strahl_breite_m": 1.76, "strahl_quelle": "stufen.ueberfall_breite_cm",
     "kaskadennetz": {"id": "…_KN0", "bereich_s_m": [52.15, 54.65], "vorhang": true},
     "effekte": [{"quelle": "gefaelle/F_ERLENBACH_1V_C2/plan.json#effekte", "index": 3,
                  "asset": "/Game/NatureWaterFX/FX/NS_Impact_Small", "rolle": "aufprall", "cull_m": 45.0,
                  "pos_cm": [-174204, -234351, 8427]}, …],
     "gischt": true,
     "schaum_objekte": [
       {"art": "aufprallteppich", "pos_cm": [-174237.4, -234256.2, 8418.3], "groesse_m": [6.17, 8.99],
        "drehung_yaw_grad": 106.9, "form": "unregelmaessig, Rand ausgefranst", "seed": 762259202, "s_m": [53.15, 59.32]},
       {"art": "schaumstrasse", "punkte_cm": [[-174236.3, -233987.7, 8408.5], … 5 Punkte], "pos_cm": […],
        "groesse_m": [2.32, 0.39], "drehung_yaw_grad": 106.9, "auslaufend": true,
        "folgt": "Stroemung (Shallow Water) sonst mittellinie"},
       {"art": "kehrwasser", "pos_cm": […], "groesse_m": [d, d], "drehung_yaw_grad": …, "grund": "neben dem Aufprall (links)",
        "ruhend": true}]}, …],
   "wasser_kollision": [{"ref": {"quelle": "gefaelle/F_ERLENBACH_1V_C2/instanzen/C2/plan.json",
                                 "datei": "SM_NordicBoulder_01_kol", "index": 3},
                         "netz": "SM_NordicBoulder_01", "pfad": "/Game/Megascans/3D_Assets/NordicBoulder/SM_NordicBoulder_01",
                         "art": "fels", "pos_cm": […], "groesse_m": [dx, dy, dz], "lage": "im_wasser",
                         "abstand_rand_m": -8.56, "abschnitt": "…_A08", "kollision_im_plan": true,
                         "wasser_kollision": true}, …],
   "sim_bereiche": [{"id": "F_ERLENBACH_1V_C2_K00", "bereich_cm": [xmin, ymin, xmax, ymax],
                     "abschnitte": ["…_A00", …, "…_A07"], "source_river": "…_A00", "sink_river": "…_A07",
                     "grenze_oben": "laufanfang", "grenze_unten": "fall", "groesse_m": [74.6, 120.7],
                     "fingerabdruck": "<sha256>", "fingerabdruck_teile": {"gelaende": "…", "splines": "…", "objekte": "…"},
                     "n_hoehen": 2318, "raster_cm": 200.0, "n_objekte": 336}],
   "effekte_ohne_fall": ["gefaelle/…/plan.json#effekte[12]", …]}]}
```

- **Koordinaten** in cm (Unreal-Welt), Laufkoordinate `s` in m wie im Planer (`mittellinie_s_m`).
- **`punkte`**: `RiverWidth` = volle Wasserbreite (A15-Konvention `breite`; im Einrichtungstest prüfen, siehe
  Datei 16), `Depth` = Wasser über dem Bett (Kaskadennetz: größtes `tiefe_cm` der mittleren 60 % des Querprofils,
  sonst `abstand_bett_cm` bzw. `tiefe` des Rivers; mindestens 10 cm), `WaterVelocityScalar` = Tempo aus dem Netz bzw.
  River (10–1024 cm/s, `r.Water.MaxFlowVelocity`). `z_cm` = Spiegel.
- **`punkt_typen`**: `LINEAR` an Lippe und Fuß jedes Absturzes im Abschnitt (kein Überschwingen über die Stufe),
  sonst `CURVE_CLAMPED`. **`tangenten_cm`** (Ankunft = Abgang): Catmull-Rom in xy, z monoton (0 an flachen
  Nachbarn und an `LINEAR`-Punkten, sonst die kleinere Nachbarstufe).
- **`punkt_rollen`**: `becken` (geplanter Spiegel, waagrecht bzw. ≤ 3 %), `lippe`, `fuss`, `rampe` (Schnelle,
  frühere River < 15 m), `gerinne` (feste Zone mit altem Spiegel), `river`, `roh`.
- **`water_body.affects_landscape: false`**: Das Gelände kommt aus dem Planer-Delta, der River schnitzt nicht.

## Regeln

**Fall.** Ein Einzelabsturz ist eine Stufe ohne Teilstufen bzw. jede Teilstufe einer Kaskade. Fall = Absturz
≥ `fall_schwelle_m` (1,0 m) und keine Rampe/Schnelle. Alle kleineren Abstürze bleiben im Abschnitt; die Spline
fällt dort von der Lippe (`LINEAR`) zum Fuß (`LINEAR`, 0,5 m weiter), und die Simulation lässt das Wasser darüber
laufen.

**Abschnitt.** Je Becken zwischen zwei Fällen ein `WaterBodyRiver` vom Fuß des oberen bis zur Lippe des unteren
Falls, am Laufanfang bzw. -ende bis zum Laufrand.
- **Kurze Becken** (< `min_laenge_m` = 4 m) werden mit dem talwärts folgenden Abschnitt zusammengefasst (am Laufende
  mit dem oberen). Der Fall liegt dann innen (`faelle_innen`, `im_abschnitt: true`), Vorhang und Effekte bleiben.
  Grund: Der River zeichnet sich in die Water-Info-Textur; unter etwa 3,4 Texeln (1,18 m je Texel bei C2, 14b)
  entstehen Lücken. 4 m entspricht dem 10-%-Quantil der Abstände zwischen Fällen in allen Gefälle-Läufen
  (Median 10 m).
- **Reste < 0,5 m** am Laufrand (Fall direkt am Laufanfang/-ende) bekommen keinen Abschnitt; der Fall mündet dann
  aus bzw. in ein anderes Gewässer (`rest_oben`/`rest_unten`, Fall mit `abschnitt_oben` bzw. `abschnitt_unten` = null).
- **Lange Abschnitte** werden in gleich lange Teile geteilt (`teil`), höchstens 112 m (Kachel 128 m − 2 × 8 m Rand),
  bei breiten Flüssen max(128 − 16 − größte Breite; 32) m. Teile teilen den Endpunkt.
- **Splinepunkte**: Anfang, Ende, Lippe/Fuß jedes Absturzes, dazwischen alle ≤ 2 m (roher Lauf: Originalpunkte,
  verdichtet auf ≤ 10 m). Spiegelhöhen kommen unverändert aus der Quelle; der Abschnitt füllt damit jedes Becken
  bis zur Lippe (`becken[].spiegel_cm`).

**Quellen der Linie.** Gefälle und Sehens-Bäche mit `wasser_koerper`: Kaskadennetz-Mittellinie + River-Punkte,
in der 0,5-m-Überlappung zählt das Netz. Gefälle-Läufe ohne Plan (25 der 123 Läufe der 161 Strecken), Flüsse
≥ 15 m Breite ohne Plan und Sehens-Bäche ohne Stufe ≥ 0,5 m: roher Lauf (`wasser_welt.json`, `baeche_alle.json`,
`punkte_cm`).

**Wasser-Kollision.** Ein Objekt (Instanz einer Ebene oder Akteur) bekommt `wasser_kollision: true`, wenn es
- **fest** ist: Kollision im Plan, Fels-/Klippennetz (`sehens_lib.steilwand.ist_fels`) oder Holz (`holz_muster`),
  nie eine Pflanze (`pflanze_muster`);
- **groß genug** ist: Grundriss ≥ 0,4 m und Höhe ≥ 0,2 m (gedrehte Bounds aus `netze_masse.json`, sonst `netze.csv`
  „unten Mitte“). Kies und Steinpackungen bleiben ohne;
- **im Wasser oder ≤ 1 m daneben** steht: Abstand Mittelpunkt–Spline − Grundriss-Radius − halbe Breite ≤ 1 m,
  Unterkante ≤ Spiegel + 0,5 m, Oberkante ≥ Bett − 0,1 m.

`lage`: `im_wasser` (Grundriss schneidet die Wasserfläche) oder `ufer`. Der Verweis `ref` ist eindeutig:
`quelle` (Ebene `gefaelle/<lauf>/instanzen/<Feld>/plan.json` bzw. `sw_<biom>/<Feld>/plan.json`) + `datei` + `index`
(Zeile in `<datei>.f32`) bzw. `liste: "akteure"` + `index`. Objekte anderer Ebenen (Bestand, Felsgruppen, Witcher)
liegen in der Cloud nicht vor; lokal setzt das Bau-Werkzeug dieselbe Regel auf alle Ebenen der Kachel an.

**Schaumobjekte** je Fall (Nachtrag Datei 16):
- **Aufprallteppich**: am Fuß, Radius r = f × Fallhöhe mit f ∈ [0,5; 1] (deterministisch aus der Fall-ID), mindestens
  0,5 m; Länge 2r × 1,3 in Fließrichtung, höchstens 60 % des Beckens; Breite 2r, höchstens 90 % der Wasserbreite,
  mindestens Strahlbreite + 0,4 m. Rand ausgefranst (`seed`).
- **Schaumstraßen**: n = clamp(round(2 + 0,8 × Fallhöhe); 2; 6), ab dem Ende des Teppichs talwärts, 2–4 m lang
  (höchstens bis 0,3 m vor die nächste Lippe), 0,15–0,4 m breit, ±0,3 m gebogen, auslaufend; seitlich über die
  Strahlbreite + 0,5 m verteilt und innerhalb der Wasserbreite. Keine Straßen, wenn das Becken < 1 m Platz lässt.
- **Kehrwasser** (ruhend, Ø 0,6–1,6 m, ≤ 4 je Becken): neben dem Aufprall beidseitig, wenn neben dem Strahl Platz ist;
  im Lee von Randblöcken (feste Objekte, deren Grundriss die Wasserkante ±0,5 m schneidet, z. B. 15g-Randblöcke);
  in Buchten hinter Vorsprüngen (`ufer_rand` aus 15g, Einzug ≥ 0,4 m → 0).
- **Gischt** an Fällen ≥ 3 m: kein neues Objekt, sondern die vorhandenen Nature-Water-FX-Effekte (`effekte`, `cull_m`
  aus 13k).
- Netze und Decals wählt das lokale Bau-Werkzeug. Kandidaten im Inventar (`inventar_extra.json`):
  `/Game/Eldarien/Welt/Wasser/MI_EL_Fluss_Schaum`, `/Game/Eldarien/Welt/Wasser/Stufenfall/MI_EL_Stufenfall_Schaum`.

**Kaskadennetz nur noch an Vorhang-Fällen (v2).** `kaskadennetz.bereich_s_m` = [Lippe − 0,5 m; Fuß + 1,5 m] auf
`mittellinie_s_m` des bisherigen Netzes, nur bei `vorhang: true` (sonst `null`). Das Bau-Werkzeug schneidet das Netz auf
diese Bereiche zu; Becken, flache Strecken und alle anderen Fälle übernimmt die Simulation.

**Vorhang (v2, 16b).** `vorhang: true` nur an einer echten Fallkante:
- Einzelabsturz (keine Kaskaden-Teilstufe, keine Schnelle) **≥ 3,0 m** (wie `vorhang_ab_m` des Planers, 14b), oder
- **senkrechte Felslippe**: Einzelabsturz ≥ 2,0 m, Art `fall`, keine Holzstufe, horizontaler Versatz Lippe → Fuß
  (`versatz_m`, Überfall-Mitte bzw. Lippenpunkt gegen `fuss_cm`) ≤ 0,3 × Fallhöhe (≥ 73°).
- Begründung: Die Simulation ist 2D (eine Höhe je Zelle von 0,35–0,5 m). Einen Absturz zeichnet sie als Rinne über
  1–2 Zellen. Unter 2 m liegt diese Rinne im Schaumband der Lippe und liest sich als Wildwasser (16b: C2 natürlicher
  als das Netz). Ab 3 m bzw. an einer senkrechten Wand ab 2 m entstünde eine geneigte „Glaswand“ ohne freien Strahl und
  ohne Luft dahinter; dort braucht es Vorhang und Aufprallschaum.
- **Schaumobjekte** (Aufprallteppich, Schaumstraßen, Kehrwasser) nur bei `vorhang: true`; sonst `schaum: "simulation"`,
  `schaum_objekte: []`. Die Niagara-Effekte (`effekte`) bleiben an allen Fällen.

**Überspannende Objekte (16a Entscheidung 5).** `lage = im_wasser` und Unterkante > Spiegel + 0,1 m → keine
Wasser-Kollision, Eintrag in `ohne_wasser_kollision` mit `grund: "ueberspannt"` (die Erfassung von oben machte daraus
einen Damm). Für `lage = ufer` bleibt + 0,5 m.

**SWR-Einheit (v2, `swr` in den Regeln).**
- **Eine Einheit je Strecke** (Gewässer der Ausgabe: Gefälle-Lauf, Sehens-Bach, Fluss), solange die längste Achse der
  Box (Spline ± halbe Breite) bei `resolution_max` = 512 eine Zelle ≤ `zelle_max_m` = 0,5 m ergibt, also ≤ 256 m.
- **Zelle:** Ziel 0,35 m für Bäche (Strecke mit Abstürzen aus dem Plan oder Median der Breite < 15 m), 0,5 m für Flüsse.
  `resolution_max_axis` = ⌈Achse / Ziel / 32⌉ × 32, begrenzt auf [32; 512]; `zelle_m` = Achse / Auflösung. Bäche mit
  Zelle > 0,4 m (Box 205–256 m) bleiben eine Einheit und bekommen im Prüfer einen HINWEIS.
- **Teilung** längerer Strecken (gierig von oben, möglichst wenige Einheiten): Für den Anfang `a` wird das größte `b`
  bestimmt, bis zu dem die Box ≤ 256 m − 4 m (Überlappung) bleibt. Gesucht wird eine Teilstelle im hinteren Teil
  [a + 0,5 · (b − a); b] (Notfall: ab 0,1). Rangfolge: **Fall mit Vorhang** > **Fall** > **Becken** (Mitte eines
  Beckens ≥ 8 m, Gefälle ≤ 3 % über ± 2 m) > **ruhige Stelle** (flachstes Gefälle über ± 5 m, ≥ 1 m von jedem Absturz).
  Bei gleichem Rang die talwärts letzte (Fälle, Becken) bzw. die flachste. Keine Rest-Einheit < 30 m.
- **Naht an einem Fall:** Source/Sink-Verkettung ohne Überlappung. Die obere Spline endet an der Lippe (Senke = eigener
  River), die untere beginnt am Fuß (Quelle = eigener River). Die Kante liegt unter Vorhang bzw. Aufprall; das Wasser
  fällt frei über die Lippe und hängt nicht vom Unterwasser ab.
- **Naht in einem Becken bzw. an einer ruhigen Stelle:** Die beiden Splines überlappen 4 m (je 2 m über die Teilstelle).
  Dort ist der Spiegel waagrecht und die Strömung langsam; beide Simulationen haben an der Naht denselben Spiegel, Senke
  und Quelle liegen 2 m hinter bzw. vor der sichtbaren Naht. Der obere River hat Vorrang (`overlap_material_priority`).
- Die Einheit hat `naht_oben`/`naht_unten` (`laufanfang`, `fall`, `becken`, `ruhig`, `offen`, `laufende`), `vorgaenger`,
  `nachfolger` und `back_reihenfolge` (von oben nach unten backen).

**Kacheln (`sim_bereiche`, v2 nur Unterteilung).** Aufeinanderfolgende Abschnitte **einer Einheit**, bis die
Bounding-Box (Punkte ± halbe Breite) + 2 × 8 m Rand 128 m erreicht. Sie dienen der Akteur-Grenze aus 13k (≤ 50
Akteure eines Gefälle-Laufs je Kachel) und mit ihrem Teil-Fingerabdruck der Ortung von Änderungen. Gebacken wird je
Einheit. `grenze_oben`/`grenze_unten` wie v1.

## Fingerabdruck (Back-Liste)

Je **SWR-Einheit** (v2; v1: je Kachel) legt ein SHA-256-Fingerabdruck fest, was die Simulation dort sieht. Das lokale
Werkzeug backt nur Einheiten neu, deren Fingerabdruck sich gegenüber dem letzten Backen geändert hat. Die Formel ist
unverändert (`FLUSS_SIM_FP1`); bezogen wird sie auf `bereich_cm` der Einheit (Box der Spline + 8 m Rand) und auf die
**eine** Spline der Einheit (`S|WBR_<einheit>|n`). Die Kacheln tragen weiter einen eigenen Fingerabdruck mit den
Abschnitt-Splines; er zeigt, in welchem Teil einer Einheit sich etwas geändert hat. Die Funktionen
`fp_gelaende_text`, `fp_splines_text`, `fp_objekte_text` und `fingerabdruck` in `fluss_sim_export.py` sind die
Referenz; sie brauchen nur `hashlib`, `math` und NumPy und laufen auch im Unreal-Python.

Quantisierung überall `q(v, s) = floor(v / s + 0,5)` (ganzzahlig, kein Banker's Rounding). Texte ASCII, Zeilen mit
`\n` getrennt, letzte Zeile mit `\n` abgeschlossen.

1. **Gelände** – Abtastpunkte = Pixelmitten des Planrasters in `bereich_cm` (Rand der Kachel inklusive):
   lokal 1 m mit x = j − 4730,5 m, y = i − 4060,5 m; in der Cloud 2 m mit x = 2j − 4730 m, y = 2i − 4060 m.
   Höhe = Gelände nach allen Stempeln (Welt + 1-m-Deltas der Planer) bzw. im Editor die Landschaftshöhe an genau
   diesen Punkten.
   ```
   G|r=<raster_cm>|x0=<q(x0_cm,1)>|y0=<q(y0_cm,1)>|nx=<nx>|ny=<ny>|q=5
   <q(h,5) für x aufsteigend, mit Komma>      ← eine Zeile je y, y aufsteigend
   ```
2. **Splines** – je Abschnitt der Kachel, sortiert nach ID:
   ```
   S|<abschnitt_id>|<anzahl punkte>
   <q(x,1)>,<q(y,1)>,<q(z,1)>,<q(RiverWidth,1)>,<q(Depth,1)>,<q(Velocity,1)>   ← je Splinepunkt in Reihenfolge
   ```
3. **Objekte mit Wasser-Kollision**, deren gedrehte Bounds `bereich_cm` schneiden, je eine Zeile, die Zeilen als
   Text sortiert:
   ```
   O|<netzpfad>|q(x,1)|q(y,1)|q(z,1)|q(qx·10000,1)|q(qy·10000,1)|q(qz·10000,1)|q(qw·10000,1)|q(sx·1000,1)|q(sy·1000,1)|q(sz·1000,1)
   ```
   Quaternion normiert und kanonisch: das erste von 0 verschiedene Element in der Reihenfolge qw, qz, qy, qx ist
   positiv (q und −q sind dieselbe Drehung).
4. `teil = sha256(text).hexdigest()` je Teil, **Fingerabdruck =
   sha256("FLUSS_SIM_FP1\n" + gelaende + "\n" + splines + "\n" + objekte + "\n").hexdigest()**.

**Beispiel** (eine 3 × 2-Kachel bei 1 m, ein Abschnitt mit 2 Punkten, ein Fels):

```
G|r=100|x0=-172182|y0=-239417|nx=3|ny=2|q=5
2041,2041,2041
2040,2041,2041

S|BEISPIEL_A00|2
-172182,-239417,10206,2879,70,300
-172263,-239173,10166,2785,70,300

O|/Game/Megascans/3D_Assets/NordicBoulder/SM_NordicBoulder_01|-172819|-238622|9796|-2397|-1871|1287|9439|347|347|347

gelaende d9ed1638941691faf8ceea836ff5839c862d5b1df8b2dd03cf111c069be66efd
splines  e16deb08d1ec274db38a11934bfe52e6d79a44137388df79804edaf25af0076e
objekte  e8316276836cdc46b521a41235aa6c31889f4aec5a58c56cdf413c0991e198ea
gesamt   afb13e88e9db310d08eadd51b6d036af7646ff5fb08916b46c28600d78cfa2c9
```

(Eingaben: Höhen 10203,7/10204,9/10206,2 und 10201,1/10202,6/10204,0 cm; Splinepunkte
[−172182,5; −239417,0; 10206,1; 2879,3; 70,4; 300] und [−172263,2; −239173,4; 10166,2; 2784,6; 69,5; 300]; Fels
x/y/z −172818,7/−238622,3/9795,7, q (−0,239743; −0,187143; 0,128668; 0,943899), Skala 0,3468.)

**Handänderungen im Editor.** Das lokale Werkzeug rechnet je Kachel aus `back_liste.json` (`bereich_cm`) dieselbe
Formel aus dem **Editor-Zustand**:
- Gelände: Landschaftshöhe an den Rasterpunkten (z. B. `Landscape.get_height_at_location` bzw. Line Trace auf den
  Kanal der Landschaft) auf dem 1-m-Raster.
- Splines: der `WaterBodyRiver` der Einheit (Label `WBR_<einheit>`), Splinepunkte in Weltkoordinaten mit `RiverWidth`,
  `Depth`, `WaterVelocityScalar` aus den Spline-Metadaten.
- Objekte: alle Akteure mit Tag `SWR_Hindernis` **und** alle Instanzen der `WH_…`-Akteure, deren Weltbounds den Bereich
  schneiden – auch die von Hand gesetzten Felsen. Netzpfad ohne `.Objektname`-Suffix.

Es vergleicht immer gleich mit gleich: den Editor-Fingerabdruck beim letzten Backen (gespeichert je Einheit) mit dem
aktuellen Editor-Fingerabdruck, und den Planer-Fingerabdruck dieser Liste mit dem der vorigen Liste (neue
Planung). Planer- und Editor-Wert sind wegen Landschafts-Quantisierung (16 bit) und Interpolation nicht
zwingend gleich; ein Unterschied an einer Rundungsgrenze löst höchstens ein unnötiges Neu-Backen aus. Die Teil-Hashes
zeigen, was sich geändert hat.

## Prüfer

`fluss_sim_pruefen.py` prüft (alles FEHLER, wenn nicht anders gesagt):
- **Spline**: ≥ 2 Punkte, z nie steigend, Becken (`punkt_rollen` = becken) ≤ 3 %, Punktabstand ≤ 2 m (roh ≤ 10 m),
  kein Grundriss-Sprung; Abschnitte lückenlos: an Fällen Ende = Lippe und Anfang = Fuß, an offenen Grenzen
  gemeinsamer Endpunkt.
- **Werte**: `RiverWidth`, `Depth` > 0, Velocity 0–1024 cm/s; Punkttypen, Tangenten, Rollen so lang wie die Punkte.
- **Fälle** (aus der Quelle neu gezählt): jeder Einzelabsturz ≥ Schwelle ohne Rampe hat einen Fall-Eintrag, Lippen-
  und Fußhöhe ±2 cm wie in der Quelle, oberer/unterer Abschnitt existiert, jeder Fall hat einen Aufprallteppich.
- **Becken** (aus der Quelle): kein Becken ohne Abschnitt; Spline-Spiegel am Becken = Quellspiegel ±2 cm.
- **Kollision**: Jedes feste, große Objekt, dessen Mittelpunkt im Wasserstreifen liegt (Unterkante ≤ Spiegel
  + 0,5 m, nicht ganz unter dem Bett), steht in `wasser_kollision`; jeder Verweis existiert; `wasser_kollision: true`.
- **Schaum**: Art bekannt, Größe > 0, jeder Punkt im eigenen Wasser (± 0,5 m) und auf dessen Spiegel (± 0,5 m);
  Fälle, deren Fuß in einem anderen Gewässer liegt, als HINWEIS.
- **Kacheln**: jeder Abschnitt in genau einer Kachel, jede Kachel in genau einer Einheit; Teil-Fingerabdrücke neu gerechnet.
- **SWR-Einheiten (v2)**: lückenlose Kette über die Strecke (Naht an Fall = Lippe/Fuß, sonst gemeinsame Stelle mit 4 m
  Überlappung), jeder Abschnitt in genau einer Einheit, keine Rest-Einheit < 30 m; Spline ≥ 2 Punkte, Abstand ≥ 2 m und
  < 2 × Ziel, z nie steigend, Becken-Punkte auf dem Spiegel der Abschnitt-Spline (± 2 cm), Ende an Lippe = Oberwasser,
  Anfang am Fuß = Unterwasser; `resolution_max_axis` Vielfaches von 32 in [32; 512], `achse_m` aus der Spline neu
  gerechnet, `zelle_m` = Achse / Auflösung, **Zelle ≤ 0,5 m**; Bach > 0,4 m als HINWEIS; Quelle/Senke = eigener River.
- **Vorhang (v2)**: `vorhang` = Regel aus den Fall-Feldern; nur Vorhang-Fälle haben Kaskadennetz-Bereich und
  Schaumobjekte (mit Aufprallteppich), alle anderen keine.
- **Hindernis-Akteure (v2, global)**: jedes Objekt mit `wasser_kollision: true` in genau einem `WH_<einheit>`, Verweis
  `hindernis_akteur` passt, Instanzzahlen stimmen, kein Pflanzennetz, kein überspanntes Objekt; `ohne_wasser_kollision`
  erfüllt die Regel; `bottom_contour_actors` enthalten die eigene WH und nur vorhandene.
- **Back-Liste (v2)**: Einheiten = Einheiten der Dateien; Fingerabdruck (Splines, Objekte, mit `--daten2m/--daten1m`
  auch Gelände) neu gerechnet = gespeichert.
- **Akteure** (mit `--gefaelle`): höchstens 50 Akteure eines Gefälle-Laufs je Kachel (13k-Rückfrage 6, wie
  „50 je 200 m Lauflänge“ im Gefälle-Prüfer).
- **Determinismus** mit `--vergleich`: alle Dateien byte-gleich.

Gegenproben (C2, absichtlich verfälscht): fehlender Fall, fehlendes Kollisionsobjekt, steigende Spline, Breite 0,
entferntes Becken, Lücke im Grundriss und abgesenkter Beckenspiegel ergeben jeweils FEHLER (Exit 1). v2 zusätzlich:
Auflösung 400 (kein Vielfaches von 32, Zelle 0,54 m), Vorhang an S09 umgeschaltet, Schaum an einem Fall ohne Vorhang,
Objekt aus dem WH-Akteur entfernt, Splinepunkte 0,5 m auseinander, steigende Einheiten-Spline, überspanntes Objekt mit
Kollision, abgesenkter Becken-Punkt der Einheiten-Spline: jeweils FEHLER (Exit 1).

## Grenzen

- **2-m-Daten**: Tiefen und Gelände-Fingerabdrücke stammen aus dem 2-m-Raster. Lokal auf 1 m neu exportieren; die
  Back-Liste der Cloud ist nur ein Muster.
- **Andere Ebenen**: In der Cloud liegen nur die Gefälle- und Sehens-Ebenen vor. Felsen anderer Ebenen im Wasser
  (Bestand, Felsgruppen) findet erst der lokale Lauf bzw. das Bau-Werkzeug.
- **Überlappende Gewässer**: Mündungen und von Sehens-Planern umgebaute Strecken können zwei Gewässer an derselben
  Stelle haben; das Bau-Werkzeug legt die Kacheln dann zusammen.
- **Nähte zwischen SWR-Einheiten** (v2: 72 Nähte in 34 geteilten Strecken, davon 22 an Fällen): an Becken/ruhigen
  Stellen 4 m Überlappung; ob zwei überlappende Water Bodies im Spiel sauber über `overlap_material_priority` gezeichnet
  werden, ist lokal zu prüfen (16b, Rückfragen).
- **Mündungen** zwischen Gewässern sind nicht verkettet (jede Strecke backt für sich); gemeinsame Objekte erfasst die
  Nachbar-SWR über `bottom_contour_actors`.
