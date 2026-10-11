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

## Testlauf 2 m (11.10.2026, 57 s, deterministisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer (`orte.json` + `sw_bergwald`, mit Daten und Inventar) **0 FEHLER, 0 WARNUNG**,
1 HINWEIS (2 Kiesel am Karsee im Bestandswasser).

| Ort | Instanzen | Kollision | Akteure | Held / Begl. / Schutt / Kleinzeug / Bewuchs / Kontakt | Wasser | Effekte | Stempel |
|---|---|---|---|---|---|---|---|
| 01 Mönch | 1 751 | 275 | 9 | 2 / 7 / 162 / 928 / 40 / 504 (+117 Pfadstufen) | – | Nebel, 4 Decals | 1,9 m |
| 02 Brandkiefer | 780 | 53 | 6 | 1 / 5 / 60 / 540 / 115 / 61 | – | Niagara opt., 8 Decals | – |
| 03 Säulenhain | 2 889 | 104 | 22 | 12 / 10 / 90 / 1 968 / 294 / 523 | Bach bleibt | Spot, Nebel, 4 Decals | – |
| 04 Felsenmeer | 2 513 | 214 | 11 | 3 / 8 / 173 / 1 895 / 69 / 345 | – | Nebel, 4 Decals | 1,7 m |
| 05 Klemmblock-Klamm | 667 | 138 | 18 | 1 / 17 / 66 / 350 / 41 / 111 (+40 Gumpengeröll) | Gumpe, Bach, Schleierfall 30 m | Licht, Nebel, Niagara opt., 5 Decals | 9,6 m |
| 06 Karsee | 1 845 | 287 | 7 | 2 / 5 / 154 / 1 106 / 321 / 123 | See + Abfluss + 2 Zuläufe | Nebel, 3 Decals | 9,1 m |
| 07 Windwurf | 2 782 | 160 | 41 | 14 / 27 / 160 / 2 209 / 280 / 133 | 4 Pfützen | Niagara opt., 6 Decals | 1,6 m |
| 08 Wurzelstein | 1 243 | 140 | 13 | 2 / 11 / 45 / 900 / 55 / 148 (+95 Pfadstufen) | – | Spot, 3 Decals | 4,4 m |

Alle Orte unter §9 (≤ 15 000 / 1 500 / 80). Je Feld: B3 1 749, B4 4 538, B5 4 724, C5 10, I4 3 449 Instanzen.
Material-Instanzen 5 von 6: `MI_EL_SW_Verkohlt`, `_Klammfels_Nass`, `_Granit_Moos`, `_Block_Moos`, `_Stamm_Windstill`.

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
- **Klemmblock-Klamm:** `wasserfall` (Kante aus der Stufe, Fuß = Gumpe), Gumpe `smaragd`, Bach zum Bestandsgerinne;
  **Nature Water FX** ist gekauft, aber noch nicht im Inventar → `niagara` `NS_Smoke_Plume` (Kopie, weiß) mit
  `"optional": true`, `wunsch_paket` und `assets_wunsch`; Gischt sonst über `lokaler_nebel`.

## Grenzen und offene Punkte

- Pivot/Front: `veqnci0db_tier_2`, `rcygn_tier_0`, `vfmjadufa_tier_2`, die Basalt- und Mountain-Netze haben keine Bounds
  in `netze_masse.json` → „Pivot unten Mitte“ angenommen (`pivot` im Akteur). Die Schauseite der Schalen
  (`front_achse`) ist eine Annahme – Prüfbild `_held`/`_fern` entscheidet.
- 2-m-Daten: Klamm (2 m Raster, ~20 m breit) wird mit Wänden auf ~8 m verengt; Stempelkanten sind 2 Zellen breit.
  Lokal auf 1 m laufen lassen und Fallkante/Fuß der Klamm prüfen.
- Ameisen (`SM_anthill_ants_anim_random`) und Forellen sind abgeschaltet (offene Frage 8: Tiere).
- Pfadbänder werden auf das Lagenfenster (400/600 m) gekappt; der volle Pfad steht in `orte.json["pfad"]`.
