# fluss_sim – Exporter für Shallow Water River (Entscheidung 16, Format v3)

Ferat hat am 12.10.2026 entschieden: Alle Bäche und Flüsse laufen mit `WaterBodyRiver` + `ShallowWaterRiver`
(UE 5.8.3, Plugins Water + Niagara Fluids); die Simulation wird im Editor **gebacken**; Seen bleiben `WaterBodyLake`
([`../../16-shallow-water-alle-gewaesser.md`](../../16-shallow-water-alle-gewaesser.md)).

**Format v3 (16c, `fluss_sim_v3`):**
- **Je Gewässer genau EIN `WaterBodyRiver`** von der Quelle bis zur Mündung (See, Fluss/Bach, Meer), über alle Fälle und
  Feldgrenzen hinweg. Keine Flussabschnitte mehr; die Simulation füllt Becken und überströmt Lippen selbst.
- **Je Gewässer EINE `ShallowWaterRiver`** (Nachtrag 17:45): Der SWR-Bereich ist das achsparallele Rechteck um den Fluss,
  `resolution_max_axis` = längste Rechteckseite / Zielzelle (Bach 0,25 m, Fluss 0,35 m), höchstens 2048. Nur wenn die
  Zelle dann über 0,30 m (Bach) bzw. 0,35 m (Fluss) läge, wird die **Simulation** in wenige lange Stücke geteilt
  (kleinste Rechteckfläche, nicht an Fällen); alle Stücke nennen denselben Fluss.
- Fälle (Vorhang, Niagara, Schaumobjekte) und Wasser-Kollision (`WH_…`) wie 16/16a; Vorhänge **warten** vorerst.

Antwort dazu: [`../../16c-ferat-ein-fluss-je-gewaesser.md`](../../16c-ferat-ein-fluss-je-gewaesser.md); v2 (Strecken-Einheiten):
[`../../16b-swr-c2-ganze-strecke.md`](../../16b-swr-c2-ganze-strecke.md).

Der Exporter **liest nur**: die Planer-Ausgaben von `gefaelle_plan.py` (`<lauf>/plan.json`, `instanzen/`), der Sehens-Planer
(`<biom>/orte.json`, `sw_<biom>/`) und die Weltdaten (`wasser_welt.json`, `baeche_alle.json`, Höhe, Meer). Er ändert keine
Stufe, kein Becken, keine Lippe und kein Gelände (13f-Regel); der Prüfer vergleicht Lippen- und Fußhöhen mit der Quelle.

| Datei | Inhalt |
|---|---|
| `fluss_sim_export.py` | Exporter: Läufe verketten, Mündungen, `fluss_sim.json` je Gewässer, `back_liste.json` (je SWR-Bereich), `zusammenfassung.json`; Referenz-Funktionen für den Fingerabdruck |
| `fluss_sim_pruefen.py` | Prüfer (FEHLER/WARNUNG/HINWEIS), Exit-Code 1 bei FEHLER |
| `fluss_sim_regeln.json` | alle Zahlen (Verkettung, Mündung, Spline, SWR/Auflösung/Teilung, Fall, Kollision, Schaum, Vorhang, Fingerabdruck), Version 3 |

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

Option `--nur ID …` (Gewässer-, Lauf- oder Ort-IDs; verkettet wird immer über alle Läufe). Laufzeit 2 m: ~17 s Export,
~12 s Prüfung. Ausgabe (`--aus`, 24 MB auf 2 m, nicht ins Repo):

```
gewaesser/<gewaesser>/fluss_sim.json     je Welt-Gewässer (154; Gefälle-Läufe mit Plan und rohe Läufe verkettet)
sehens/<biom>/<ort>/fluss_sim.json       je Sehens-Ort mit Bach (26 Orte, 42 Gewässer)
back_liste.json                          alle SWR-Bereiche mit Fingerabdruck und Back-Reihenfolge (back_liste_v3)
zusammenfassung.json                     Zahlen (Gewässer, Mündungen, SWR, Auflösungen, Varianten, Höhen)
```

Beispiele im Repo: [`../../fluss_sim/`](../../fluss_sim/) – `gewaesser/F_ERLENBACH` (enthält C2 bei s 17,4–220,6 m),
`sehens/bergwald/bergwald_06_karsee`, `zusammenfassung.json`, `back_liste_auszug.json`.

## Gewässer bilden (Verkettung, Mündung)

- **Läufe:** alle 27 Feld-Stücke aus `wasser_welt.json` und alle 168 Bäche aus `baeche_alle.json` (98 mit Gefälle-Plan,
  97 roh) sowie die 42 Sehens-Bäche.
- **Fortsetzung** (gleiches Gewässer): Ende von P ≤ 8 m vom Anfang von N und N beginnt nicht höher (+ 0,5 m), oder
  Feldgrenze mit Überlappung (Ende von P liegt ≤ 1 m auf N bei s ≤ 40 m und umgekehrt). Gekürzt wird das Stück ohne Plan,
  sonst das untere (`laeufe[].gekuerzt_m`, `abstuerze_entfallen`). Je Lauf höchstens ein Vorgänger.
- **Name:** Flüsse nach dem gemeinsamen Präfix der `fluss`-Namen (`F_ERLENBACH`, `F_HAUPTFLUSS_3`), Bachketten nach dem
  obersten Lauf, Sehens-Bäche wie bisher (`SW_<ort>_<bach>`).
- **Mündung** (Reihenfolge, Zahlen in `regeln.gewaesser`):
  1. ausdrücklich: Sehens `muendung`/`muendung_art`, R2-Bäche `anschluss.ende` (wenn das Ende ≤ 15 m neben dem Ziel liegt);
  2. **Fluss/Bach** (Zusammenfluss): Ende ≤ halbe Breite + 3 m neben der Mittellinie eines anderen Laufs, nicht > 1 m
     unter dessen Spiegel. Der Nebenlauf **endet** im Hauptlauf; seine Spline bleibt bis ins Wasser des Hauptlaufs.
     Senkt der Gefälle-Plan des Hauptlaufs sein Becken (`zufluesse`), wird das Endstück des Nebenlaufs abgesenkt
     (`muendung.endstueck_angepasst`). Der Hauptlauf führt den Nebenlauf in `zufluesse` (s, SWR-Bereich);
  3. **See** (Umriss Welt- oder Sehens-See + halbe Breite + 5 m);
  4. **Meer** (Meer-Raster ≤ halbe Breite + 10 m, oder Ende ≤ 2 m hoch und Meer ≤ 150 m: Bach endet am Strand);
  5. **nah** (Lücke in den Weltdaten): Lauf bzw. See ≤ 25 m neben dem Ende → Mündung mit `luecke_m`;
  6. **Wasserfall** (Welt-Wasserfall ≤ 120 m), sonst **versickert** (Sehens) bzw. **offen** (mit `naechster_lauf`).
- `overlap_material_priority` = 10 − Stufe im Mündungsbaum (Hauptlauf 10, Zufluss 9 …).
- `anfang`: `quelle`, `see` (Seeabfluss) oder `wasserfall`.

## Format `fluss_sim.json` (v3)

Gekürzt aus `F_ERLENBACH`:

```json
{"format": "fluss_sim_v3", "regeln_version": 3, "fall_schwelle_m": 1.0, "daten": "2m (Cloud-Test)",
 "gewaesser": [{"id": "F_ERLENBACH", "kategorie": "welt", "art": "fluss", "laenge_m": 1006.7,
   "laeufe": [{"id": "F_ERLENBACH_1_C2", "herkunft": "roh", "s_m": [0.0, 17.23], "gekuerzt_m": [0.0, 11.74], "...": "..."},
              {"id": "F_ERLENBACH_1V_C2", "art": "fluss", "herkunft": "plan", "feld": "C2", "s_m": [17.4, 220.56],
               "s_quelle_m": [0.0, 203.16], "gekuerzt_m": [0.0, 0.0], "quelle": {"plan": "gefaelle/F_ERLENBACH_1V_C2/plan.json"},
               "abstuerze_entfallen": [], "anschluss_oben": "ueberlappung", "swr_typ": "bach"}, "..."],
   "anfang": {"art": "quelle", "punkt_cm": [-171943.9, -241121.6, 10395.2]},
   "muendung": {"art": "meer", "ziel": "meer", "abstand_m": 37.62, "punkt_cm": [-154268.1, -149865.4, 158.2],
                "quelle": "geometrie (Meer-Raster)", "stufe": 0},
   "zufluesse": [{"gewaesser": "B_R3_K10_TUNDRA_01", "art": "bach", "s_m": 376.42, "swr_bereich": "F_ERLENBACH_T00",
                  "water_body": "WBR_B_R3_K10_TUNDRA_01"}, "..."],
   "water_body": {"id": "WBR_F_ERLENBACH", "klasse": "WaterBodyRiver", "affects_landscape": false, "overlap_material_priority": 10,
     "spline": {"s_m": [0.0, 1006.7],
       "punkte": [["...", "..."], [-172505.0, -238470.5, 10043.5, 2500.1, 194.6, 240.0], [-172522.1, -238423.5, 9953.5, 2480.1, 215.4, 150.0], "..."],
       "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
       "punkt_typen": ["...", "LINEAR", "LINEAR", "..."], "tangenten_cm": ["..."],
       "punkte_s_m": ["...", 27.4, 27.9, "..."], "punkt_rollen": ["...", "lippe", "fuss", "..."]}},
   "abstuerze": [{"id": "F_ERLENBACH_1V_C2_s1_S01_T2", "lauf": "F_ERLENBACH_1V_C2", "s_lippe_m": 31.65, "s_fuss_m": 32.15,
                  "fall_m": 1.27, "rampe": false, "z_oben_cm": 9946.0, "z_unten_cm": 9818.7, "punkt_lippe": 15, "punkt_fuss": 16}, "..."],
   "bereiche": [{"id": "F_ERLENBACH_A03", "s_m": [43.06, 50.34], "rolle": "becken", "oben_fall": "…_S01_T5",
                 "unten_fall": "…_S02_T2", "abstuerze_innen": ["…_S02_T1"],
                 "becken": [{"s_m": [43.06, 48.13], "spiegel_cm": [9474.2, 9464.1], "...": "..."}],
                 "laeufe": ["F_ERLENBACH_1V_C2"], "swr_bereiche": ["F_ERLENBACH_T00"]}, "..."],
   "faelle": [{"id": "F_ERLENBACH_1V_C2_s1_S04", "fall_m": 4.67, "s_lippe_m": 70.05, "s_fuss_m": 70.55,
               "punkt_lippe": 39, "punkt_fuss": 40, "bereich_oben": "F_ERLENBACH_A06", "bereich_unten": "F_ERLENBACH_A07",
               "swr_bereich": "F_ERLENBACH_T00", "vorhang": true, "vorhang_status": "wartet (Ferat 16c …)", "...": "wie v2"}, "..."],
   "swr_bereiche": [{"id": "F_ERLENBACH_T00", "s_m": [0.0, 468.88], "s_sim_m": [0.0, 472.88], "punkt_index": [0, 260],
     "rechteck_cm": [-180504.0, -242771.6, -167447.0, -196865.4], "rechteck_m": [130.57, 459.06],
     "naht_oben": {"art": "quelle", "s_m": 0.0},
     "naht_unten": {"art": "becken", "s_m": 468.88, "ueberlappung_m": 8.0, "ueberlappung_s_m": [464.88, 472.88]},
     "vorgaenger": [], "nachfolger": ["F_ERLENBACH_T01"], "back_reihenfolge": 0, "geteilt": true,
     "swr": {"id": "SWR_F_ERLENBACH_T00", "klasse": "ShallowWaterRiver", "typ": "bach", "zelle_ziel_m": 0.25, "zelle_max_m": 0.3,
             "achse_m": 459.06, "resolution_max_axis": 1856, "zelle_m": 0.247, "raster_erwartet": [528, 1856],
             "source_river_water_bodies": ["WBR_F_ERLENBACH"], "sink_river_water_bodies": ["WBR_F_ERLENBACH"],
             "bottom_contour_tags": ["SWR_Hindernis"], "bottom_contour_actors": ["WH_F_ERLENBACH_T00"], "use_capture": true,
             "match_spline": "lokal testen", "begrenzung": {"art": "rechteck_teil", "rechteck_cm": ["..."], "hinweis": "…"},
             "render_state": {"backen": "LIVE_SIM", "spiel": "WATER_COMPONENT_WITH_BAKED_SIM", "ersatz": "BAKED_SIM"},
             "material": {"water_body": "MI_EL_SWR_Klar", "baked_sim_material": "MI_EL_SWR_Klar"}},
     "bereich_cm": [-181304.0, -243571.6, -166647.0, -196065.4], "zufluesse": ["WBR_B_R3_K10_TUNDRA_01"],
     "hindernis_akteur": {"id": "WH_F_ERLENBACH_T00", "...": "wie v2"}, "fingerabdruck": "34f419d2…"}, "..."],
   "wasser_kollision": [{"...": "wie v2", "s_m": "…", "bereich": "F_ERLENBACH_A…", "swr_bereich": "F_ERLENBACH_T00",
                         "hindernis_akteur": "WH_F_ERLENBACH_T00"}],
   "ohne_wasser_kollision": ["..."]}]}
```

- **Ungeteiltes Gewässer** (188 von 196): ein Eintrag in `swr_bereiche` mit `id` = Gewässer-ID, SWR `SWR_<gewaesser>`,
  WH `WH_<gewaesser>`, `begrenzung.art = "rechteck_um_fluss"`, `match_spline: true`.
- **Geteilt** (8): `<gewaesser>_T00 …`, `geteilt: true`, `match_spline: "lokal testen"`, `begrenzung.art = "rechteck_teil"` mit
  dem Rechteck des Stücks (Weltkoordinaten, cm). Alle nennen denselben `WBR_<gewaesser>` als Quelle und Senke.
- **Bau-Werkzeug (v3):** je Gewässer **einen** `WaterBodyRiver` aus `water_body.spline`, je `swr_bereiche[]` eine
  `ShallowWaterRiver` und einen `WH_…` aus `hindernis_akteur`. `bereiche` sind nur s-Bereiche (Rolle `becken`, `rinne`,
  `gerinne`, `lauf`) für Becken, Fall-Zuordnung und Prüfung, keine Water Bodies.

## Regeln

**Spline** (`regeln.spline`). Anfang, Ende und je Stufe (jeder Absturz aus Plan bzw. Sehens, auch Kaskaden-Teilstufen und
Schnellen) ein Punkt an der **Lippe** (z = Oberwasser `z_oben_cm`) und einer am **Fuß** (z = Unterwasser `z_unten_cm`), beide
`LINEAR`, dazwischen kein Punkt. Sonst gleichmäßig mit Abstand ≥ 2 m (roh ≥ 5 m), also 2–4 m (5–10 m). Fuß ≥ Lippe + 0,1 m;
liegt die nächste Lippe näher als 0,05 m am Fuß, teilen sie sich einen Punkt (`fuss_lippe`). z nie steigend. Rollen der
übrigen Punkte: `becken` (Spiegel flach ≤ 3 % zu den Nachbarn), `rampe`, `gerinne`, `rinne`, `river`, `roh`.
**Tangenten** wie v2 (Catmull-Rom in xy, z monoton, 0 an `LINEAR` und flachen Nachbarn).

**SWR** (`regeln.swr`, Nachtrag 17:45). Zielzelle je Lauf: Bach (Abstürze im Plan, Median der Breite < 15 m, Sehens-Bach)
0,25 m, höchstens 0,30 m; Fluss 0,35 m. Ein SWR-Bereich, der einen Bach-Lauf berührt, gilt als Bach.
`resolution_max_axis` = ⌈längste Rechteckseite / Ziel / 32⌉ × 32, in [32; 2048]; `zelle_m` = Seite / Auflösung.
**Teilung** nur, wenn das Rechteck des ganzen Flusses bei 2048 die Höchstzelle überschreitet (Bach > 614 m, Fluss > 717 m):
kleinste Anzahl Stücke, unter gleich vielen die kleinste Summe der Rechteckflächen (dynamische Programmierung über die
Splinepunkte), Naht ≥ 5 m von jeder Stufe und ≥ 50 m vom Anfang/Ende, Nachbarn überlappen 8 m (`s_sim_m`).
`naht.art` = `becken`, wenn die Naht in einem Becken liegt, sonst `lauf`.

**Fall, Vorhang, Schaumobjekte** wie v2 (`fall_schwelle_m` 1,0, Vorhang ab 3 m bzw. senkrechte Felslippe ab 2 m, Schaum nur
an Vorhang-Fällen); `vorhang_status` = „wartet“ (Ferat 16c).

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
liegen in der Cloud nicht vor; lokal setzt das Bau-Werkzeug dieselbe Regel auf alle Ebenen im SWR-Bereich an.

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


## Fingerabdruck (Back-Liste)

Je **SWR-Bereich** (v3; v2: je Einheit, v1: je Kachel) legt ein SHA-256-Fingerabdruck fest, was die Simulation dort sieht. Das
lokale Werkzeug backt nur SWR neu, deren Fingerabdruck sich gegenüber dem letzten Backen geändert hat. Die Formel ist
unverändert (`FLUSS_SIM_FP1`); bezogen wird sie auf `bereich_cm` des SWR-Bereichs (Rechteck + 8 m Rand) und auf die
Splinepunkte `punkt_index` [i0, i1] des **einen** `WaterBodyRiver` (`S|WBR_<gewaesser>|n`, n = i1 − i0 + 1). Die Funktionen
`fp_gelaende_text`, `fp_splines_text`, `fp_objekte_text` und `fingerabdruck` in `fluss_sim_export.py` sind die
Referenz; sie brauchen nur `hashlib`, `math` und NumPy und laufen auch im Unreal-Python.

Quantisierung überall `q(v, s) = floor(v / s + 0,5)` (ganzzahlig, kein Banker's Rounding). Texte ASCII, Zeilen mit
`\n` getrennt, letzte Zeile mit `\n` abgeschlossen.

1. **Gelände** – Abtastpunkte = Pixelmitten des Planrasters in `bereich_cm` (Rand inklusive):
   lokal 1 m mit x = j − 4730,5 m, y = i − 4060,5 m; in der Cloud 2 m mit x = 2j − 4730 m, y = 2i − 4060 m.
   Höhe = Gelände nach allen Stempeln (Welt + 1-m-Deltas der Planer) bzw. im Editor die Landschaftshöhe an genau
   diesen Punkten.
   ```
   G|r=<raster_cm>|x0=<q(x0_cm,1)>|y0=<q(y0_cm,1)>|nx=<nx>|ny=<ny>|q=5
   <q(h,5) für x aufsteigend, mit Komma>      ← eine Zeile je y, y aufsteigend
   ```
2. **Splines** – die Punkte i0 … i1 des Flusses (v1/v2: je Abschnitt bzw. Einheit, sortiert nach ID):
   ```
   S|WBR_<gewaesser>|<anzahl punkte>
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

**Beispiel** (Format unverändert seit v1: ein 3 × 2-Raster bei 1 m, eine Spline mit 2 Punkten, ein Fels):

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

**Handänderungen im Editor.** Das lokale Werkzeug rechnet je SWR-Bereich aus `back_liste.json` (`bereich_cm`) dieselbe
Formel aus dem **Editor-Zustand**:
- Gelände: Landschaftshöhe an den Rasterpunkten (z. B. `Landscape.get_height_at_location` bzw. Line Trace auf den
  Kanal der Landschaft) auf dem 1-m-Raster.
- Splines: der `WaterBodyRiver` des Gewässers (Label `WBR_<gewaesser>`), Splinepunkte i0 … i1 in Weltkoordinaten mit `RiverWidth`,
  `Depth`, `WaterVelocityScalar` aus den Spline-Metadaten.
- Objekte: alle Akteure mit Tag `SWR_Hindernis` **und** alle Instanzen der `WH_…`-Akteure, deren Weltbounds den Bereich
  schneiden – auch die von Hand gesetzten Felsen. Netzpfad ohne `.Objektname`-Suffix.

Es vergleicht immer gleich mit gleich: den Editor-Fingerabdruck beim letzten Backen (gespeichert je SWR-Bereich) mit dem
aktuellen Editor-Fingerabdruck, und den Planer-Fingerabdruck dieser Liste mit dem der vorigen Liste (neue
Planung). Planer- und Editor-Wert sind wegen Landschafts-Quantisierung (16 bit) und Interpolation nicht
zwingend gleich; ein Unterschied an einer Rundungsgrenze löst höchstens ein unnötiges Neu-Backen aus. Die Teil-Hashes
zeigen, was sich geändert hat.

## Prüfer

`fluss_sim_pruefen.py` prüft (FEHLER, wenn nicht anders gesagt):
- **Ein Fluss je Gewässer:** `water_body.id` = `WBR_<gewaesser>`, global eindeutig; jede SWR nennt genau ihn als Quelle und
  Senke; jeder Welt-Lauf in genau einem Gewässer, mit `--daten2m/--daten1m` kommen alle Läufe aus `wasser_welt.json` und
  `baeche_alle.json` vor; Läufe hintereinander von 0 bis `laenge_m`.
- **Spline durchgehend und monoton:** ≥ 2 Punkte, Felder gleich lang, s steigend 0 … `laenge_m`, kein Grundriss-Sprung,
  Abstand ≤ 2 × Ziel (außer Lippe → Fuß), z nie steigend, Breite/Tiefe > 0, Tempo 0–1024 cm/s, Stufenpunkte `LINEAR`,
  Becken-Punkte flach (≤ 3 %) und auf dem Becken-Spiegel (± 2 cm).
- **Jede Stufe hat Lippe und Fuß:** Punkt-Index gültig, Rolle, s ± 6 cm, z = Ober- bzw. Unterwasser ± 2 cm. Mit
  `--gefaelle/--sehens` werden die Stufen je Lauf aus der Quelle neu gezählt (Höhen ± 2 cm, s, Fall-Einträge); entfallene
  Stufen nur im gekürzten Teil eines Laufs.
- **Bereiche und Abdeckung:** Bereiche + Fälle lückenlos; jeder Bereich liegt in der Vereinigung der Simulationsbereiche;
  `swr_bereiche` je Bereich stimmt.
- **SWR:** Kette 0 … `laenge_m`, Überlappung je Naht, keine Naht an einer Stufe; Rechteck/Achse aus den Splinepunkten
  `punkt_index` neu gerechnet; `resolution_max_axis` Vielfaches von 32 in [32; **2048**] und = Regel; **Zelle ≤ Höchstzelle
  + 0,005 m** (Bach 0,30, Fluss 0,35); geteilt nur, wenn das ganze Rechteck nicht passt (HINWEIS je geteiltem Gewässer).
- **Mündung:** Art bekannt; Mündungspunkt = Spline-Ende; Fluss/Bach: Ziel existiert, `ziel_s_m` im Ziel, Punkt im
  Wasserstreifen des Ziels (+ `luecke_m` + 5 m), Eintrag in dessen `zufluesse`; See bekannt (Welt bzw. Sehens);
  `offen` und Lücken als HINWEIS.
- **Fälle, Vorhang, Schaum, Kollision, Hindernis-Akteure (je SWR), Back-Liste mit Fingerabdruck** (Splines, Objekte und mit
  Daten auch Gelände neu gerechnet), **Determinismus** (`--vergleich`: alle Dateien byte-gleich) wie v2.

Gegenproben (F_ERLENBACH verfälscht), alle FEHLER mit Exit 1: steigende Spline, Stufe ohne Fußpunkt, Fußpunkt auf
Oberwasser, Lücke zwischen SWR-Bereichen, Auflösung 4096, Zelle 0,45 m (Auflösung 1024), zweiter Fluss als Quelle, Lauf
doppelt, Naht an einem Fall, Grundriss-Sprung.

## Grenzen

- **2-m-Daten:** Längen, Tiefen und Gelände-Fingerabdrücke stammen aus dem 2-m-Raster; lokal auf 1 m neu exportieren.
- **Andere Ebenen:** Felsen anderer Ebenen (Bestand, Felsgruppen) findet erst der lokale Lauf.
- **Mündungen mit Lücke** (`luecke_m`, 23) und **offene Enden** (24) sind Lücken in den Weltdaten (Bach endet 25–700 m vor
  dem nächsten Wasser oder tiefer als der Fluss daneben); die Spline wird nicht erfunden, nur gemeldet.
- **Geteilte Simulation** (8 Gewässer): Der gemessene SWR-Bereich ist das Rechteck um den Quell-Fluss; zwei SWR mit
  demselben Fluss decken ohne eigene Begrenzung beide das ganze Rechteck ab. Begrenzung und Naht lokal testen (16c).
- **Überlappende Gewässer:** Sehens-Bäche, die einen Bestandsbach ersetzen (`heide_06` → `B_R2_R_P3_P0_01`), stehen weiter
  als zwei Gewässer an derselben Stelle.
