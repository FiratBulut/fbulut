# sehens_bergwald – Referenzplaner Sehenswürdigkeiten Bergwald (Auftrag 13, Phase 2)

Baut die 8 Bergwald-Orte aus `antworten/sehens/bergwald/standorte.json` nach `sehens_bergwald_regeln.json`
(Katalog `sehens/bergwald/katalog.md` inkl. „Abgleich 13b/13c“, `asset_bedarf.json`) im Lieferformat
`vorlagen/SEHENS_FORMAT.md`. Muster für alle anderen Biome: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_bergwald/sehens_bergwald.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/bergwald]
python -I sehens_bergwald.py --basis <production>      # lokal: 1 m aus export/unreal/welt, Ausgabe dort
```

Ausgabe: `<aus>/orte.json`, `gelaende/`, `lagen/`, `sw_bergwald/<Feld>/` (plan.json + f32), mit `--bild` je Ort
`test_<id>.png`. Eigener Code nur im Hook `hook_windwurf_anker` (Stammfüße, Wurzelteller, Wurzellöcher, Pfützen);
alles andere sind Regeln.

## Testlauf 2 m (Inventar 13d, 11.10.2026, 84 s, deterministisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer (`orte.json` + `sw_bergwald`, mit Daten und Inventar 13d) **0 FEHLER, 0 WARNUNG**,
2 HINWEISE (2 Kiesel am Karsee im Bestandswasser, 1 Stein in der Klamm ganz im Boden).

| Ort | Instanzen | Kollision | Akteure | Wasser | Effekte | Stempel |
|---|---|---|---|---|---|---|
| 01 Mönch | 1 788 | 274 | 9 | – | Nebel, 4 Decals | 1,9 m |
| 02 Brandkiefer | 786 | 80 | 6 | – | Niagara opt., 8 Decals | – |
| 03 Säulenhain | 3 289 | 104 | 22 | Bach bleibt | Spot, Nebel, 4 Decals | – |
| 04 Felsenmeer | 2 507 | 212 | 11 | – | Nebel, 4 Decals | 1,7 m |
| 05 Klemmblock-Klamm | 667 | 138 | 18 | Gumpe, Bach, Schleierfall 30 m | `NS_Waterfall_Medium`, `NS_Impact_Medium`, `NS_Stream_Small`, Licht, Nebel, 8 Decals (3 × `MI_Deca_Wet`) | 9,6 m |
| 06 Karsee | 1 845 | 287 | 7 | See + Abfluss + 2 Zuläufe | `NS_Stream_Small` am Auslass, Nebel, 8 Decals (5 × `MI_Deca_Wet_Flat`) | 9,1 m |
| 07 Windwurf | 2 792 | 168 | 41 | 4 Pfützen | Niagara opt., 6 Decals | 1,6 m |
| 08 Wurzelstein | 1 254 | 140 | 15 | – | Spot, 3 Decals | 4,4 m |

Alle Orte unter §9 (≤ 15 000 / 1 500 / 80, ≤ 3 Niagara). Je Feld: B3 1 786, B4 4 549, B5 5 124, C5 10, I4 3 459 Instanzen.
Jeder Ort hat alle sechs Witcher-Detailebenen (`orte.json["detail_ebenen"]`).
Material-Instanzen 5 von 6: `MI_EL_SW_Verkohlt`, `_Klammfels_Nass`, `_Granit_Moos`, `_Block_Moos`, `_Stamm_Windstill`.

## Umstellung auf Inventar 13d

- **Nature Water FX** statt Ersatz: Schleierfall `NS_Waterfall_Medium` an der Kante, `NS_Impact_Medium` an der Gumpe,
  `NS_Stream_Small` im Klammbach und am Karsee-Auslass (nicht mehr `optional`).
- **Mountain-Fluss-/Wasserfallmaterial:** `inventar.json` nennt nur Materialnamen ohne Pfad (`M_River_Water_Translucent`) →
  als `material_hinweis` an Bach/Wasserfall von Klamm und Karsee, kein erfundener Pfad.
- **Mountain-Netze (+243):** Hangwurzeln `SM_roots_slope_02/03_*` und `SM_Pine_roots_04` am Wurzelstein,
  freigespülte Wurzeln `SM_Pine_roots_05/06` an der Fallkante, Wurzelteller `SM_stones_roots_04/05` im Windwurf,
  Zapfen `SM_Pine_cone_*` (Mönch, Säulenhain, Wurzelstein), 7 Pilzarten `SM_mushroom_*` (Säulenhain, Windwurf),
  Bruchäste `SM_Pine_broken_branch_04–10`, Steine `SM_stone_09–12`, Beeren/Heide/Latschen-Varianten,
  Jungbäume `SM_Forest_pine_tree_00_A/B`, Platte `SM_flat_rock_01`.
- **Coast & Dunes:** Nassband-Decals `MI_Deca_Wet` (Klamm) und `MI_Deca_Wet_Flat` (Karsee-Ufer, Verteilung `ufer`).
- `assets_wunsch` bereinigt: Nature Water FX und Mountain entfernt; übrig sind nur noch fehlende Pakete
  (Forest Fungi – jetzt optional –, Niagara VFX Pack Autumn Leaves, Wilderness Nature Loops).
- `SM_Forest_pine_06` gibt es seit 13d zweimal (Foliage und Roots) → voller Pfad in den Regeln.

## Abgleich 13b/13c umgesetzt

- **Mönch:** `veqnci0db_tier_2` hochkant (lokal Y nach oben, `skala_xyz` 0,55 / 0,95 / 0,45 → ~36 m, 7 m eingegraben),
  Kappe `rcygn_tier_0`, Rückseite `vdssailfa_tier_2`, Sockel `Basalt_Basalt_Cliff_Rock_A_SM` + Schutt
  `Basalt_Basalt_Rock_C/D_SM` mit `MI_EL_SW_Granit_Moos`. Katalog |Δ| ≤ 3 m eingehalten (Stempel 1,9 m).
- **Säulenhain:** 12 × `Fir_07_Forest`/`Fir_04_Standalone` ×2,2–2,5 (Nicht-Nanite), Ammenstamm mit Jungtannen darauf.
- **Windwurf:** 11 × `SM_Forest_pine_08/09` liegend (Kronen landeinwärts, Sturm von See), `MI_EL_SW_Stamm_Windstill`
  (`Wind_Staerke` 0), Wurzelteller `SM_stones_roots_02` hochkant, Wurzellöcher mit Pfützen.
- **Karsee:** eigener `see` (`schwarz_spiegel`), Becken automatisch eingepasst, Schwelle als Lippe am Abfluss.
  Stempel 9,1 m statt der ±6 m aus 13c, weil der Karboden in den 2-m-Daten 18–27° geneigt ist (Begründung in `gelaende`);
  Ferat hat am 11.10. „Gelände frei“ gegeben – bitte im 1-m-Lauf prüfen.
- **Klemmblock-Klamm:** `wasserfall` (Kante aus der Stufe, Fuß = Gumpe), Gumpe `smaragd`, Bach zum Bestandsgerinne,
  Effekte aus Nature Water FX (siehe oben).

## Auftrag 13h – Bildbefund erster Pilot (12.10.2026)

Details und Vorbilder: `recherche/antworten/13h-pilot-bergwald-bildbefund.md`.

- **Karsee (`bergwald_06`):**
  - `gelaende.max_neigung_grad: 35` und `halde`: neue Steilheit wird am Fuß als Schutthalde aufgeschüttet und an der
    Kante abgetragen, mit Lage `Geroell` und Blöcken.
  - Rückwand `karwand_fels`: 18 Klippennetze mit `verteilung.typ: steilwand`, `front_an_linie`, gestapelt.
  - Auslauf: `schwelle_buckel` aus 14 Rundhöckern.
  - Gliederung: `felsbaender`(`_west`), `rinnenkegel_sued/_west`, Moos- und Schnee-Lagen.
  - Seefarbe `tiefblau` mit `farbe_begruendung`.
  - Insel: `becken.insel` ist eine Kuppe 0,6 m über dem Spiegel; Blöcke und Kiefer stehen darauf.
  - Spiegel 256,17 m und die Bachstufen sind unverändert.
- **Säulenhain (`bergwald_03`):**
  - 13 × `Fir_07_Forest` ×2,6–2,9 (Median 59,5 m; Bestand P90 27 m).
  - Freiraum `kreis` r 34 m für den Kern, `rechteck` 70 × 42 m für die Lichtung nach ONO.
  - `saum_jungwuchs`, `lichtung_gras`, `altholz`, drei Spotlichter, Nebel 0,05.
  - Kameras werden über die Regel `kameras` gesetzt; `_fern` wird an einem Wegpunkt gesucht (570 m, Kronen vor dem Himmel).
- **Windwurf:** `kameras.nah` zielt auf die Gruppe `wurzelteller`.
- **Prüfer 2 m:** 0 FEHLER. Es bleiben 4 WARNUNGen am Karsee, alle aus 13g/13i (Stufen ohne Niagara, Ufer 4 von 168 Proben).
- **Steilflächen am Karsee:** 241 m² neu > 45°, davon 233 m² verkleidet.

## Auftrag 13k – Bildbefund Pilot 2 (12.10.2026)

Details: `recherche/antworten/13k-pilot2-bildbefund-15g-nachtrag.md`.

- **Säulenhain (`bergwald_03`):** keine gesägten Stammstücke mehr (Regel in der Bibliothek). Totholz: 3 abgestorbene
  Riesentannen (`Fir_08_Dead_Forest` ×2,0–2,4) mit Gruppen großer liegender Stämme darunter, hangparallel; mittleres
  Totholz und Äste in Nestern (Richtwert Altwald je 100 m²: 1–3 Stämme, 5–15 Äste). Waldboden in Schichten: Moospolster,
  Farngruppen zu 3–7, Heidelbeer-Inseln, bemooste Steine, Wurzeln; Nadelstreu deckend (255) gegen Landschaftsgras.
  `_fern` mit freier Achse (Gelände und Baumkronen).
- **Karsee (`bergwald_06`):** `gelaende.verkleiden_60` – alle Flächen > 60° im Kar (75 m, zum See gewandt) bis zur
  Oberkante verkleidet, Schuttkegel am Fuß; Seefarbe `bergsee` (Ferat Variante C).
- `paletten.stammstuecke`, `brandholz`, `treibholz`, `nadeln_zweige` und `MI_EL_SW_Verkohlt.fuer` ohne `*_log`.

## Grenzen und offene Punkte

- Pivot/Front: `veqnci0db_tier_2`, `rcygn_tier_0`, `vfmjadufa_tier_2`, die Basalt- und Mountain-Netze haben keine Bounds
  in `netze_masse.json` → „Pivot unten Mitte“ angenommen (`pivot` im Akteur). Die Schauseite der Schalen
  (`front_achse`) ist eine Annahme – Prüfbild `_held`/`_fern` entscheidet.
- 2-m-Daten: Klamm (2 m Raster, ~20 m breit) wird mit Wänden auf ~8 m verengt; Stempelkanten sind 2 Zellen breit.
  Lokal auf 1 m laufen lassen und Fallkante/Fuß der Klamm prüfen.
- Ameisen (`SM_anthill_ants_anim_random`) am Ameisenhaufen sind aktiv (E04); andere Tiere (Forellen) bleiben aus.
- Pfadbänder werden auf das Lagenfenster (400/600 m) gekappt; der volle Pfad steht in `orte.json["pfad"]`.
- **13f (Pilot bergwald_03 + bergwald_06):** Riesentannen stehen am Stammfuß (A3). Karsee: Zulauf West beginnt im alten
  Houdini-Lauf `R_M2_P0__WASSER` (Anker `rinne_w` ohne Wasserausschluss) und endet auf dem Umriss, der Abfluss läuft im
  alten Lauf nach Osten (`muendung_houdini`); das Houdini-Netz ist im See und in beiden Bachkorridoren ausgeblendet
  (`houdini_ausblenden` → `bestand_ausblenden` art `houdini`); `ist_wasser_r_m` 68; `tiefe_m` steht nach dem Stempel in
  `orte.json`. Klemmblock-Klamm: Fenster 130 m, Klammbach endet im bestehenden Houdini-Gerinne (`muendung_houdini: true`).
