# sehens_frost – Sehenswürdigkeiten-Planer Frost (Auftrag 13, Phase 2)

Baut die 8 Frost-Orte aus `antworten/sehens/frost/standorte.json` nach `sehens_frost_regeln.json` (Katalog
`sehens/frost/katalog.md` inkl. „Abgleich Inventar 13d“, `asset_bedarf.json`, `sehens/entscheidungen.json`).
`sehens_frost.py` ist eine Kopie von [`../sehens_gletscher/sehens_gletscher.py`](../sehens_gletscher/README.md) mit
ausgetauschtem Biomnamen; dort stehen die Hooks (`rahmen`, `fuellen`, `nach_ops`, Verdeckung, `pfad_regel`).

```
python -I recherche/antworten/skripte/sehens_frost/sehens_frost.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--orte ID ...] [--bild --bild-ordner recherche/antworten/sehens/frost] [--ohne-sicht]
```

## Testlauf 2 m (11.10.2026, ~60 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer **0 FEHLER, 0 WARNUNG** (Lagenfenster 02 akzeptiert, E49).

| Ort | Inst. | Koll. | Akteure | Stempel | Held / Besonderheit |
|---|---|---|---|---|---|
| 01 Eisfall | 1 155 | 113 | 13 | 7,9 m | Eissäulen aus Ice Cliffs + `SM_EISZAPFEN_*` (Spritzeis) an der Stufe, Restwasser-Fall, NS_Stream_Small, Rahmen Süd/Nordwest/Nordost, Sichtkern am Fuß |
| 02 Frostsee | 2 214 | 202 | 70 | 5,7 m | neuer gefrorener See `frostsee` (Spiegel Boden −0,25, `eis`), Presseis-Reihe gewellt (z über `spiegel:`), Uferwehen in Gruppen, Freiraum K13 r 150 m, Decals `Eisblasen`/`Eisrisse` |
| 03 Eisvorhang | 1 371 | 128 | 17 | 13,9 m | Vorhang aus 420 Eiszapfen, Rahmen SW/W (bis 11 m) |
| 04 Raureifhain | 1 216 | 154 | 39 | 0,4 m | Raureif-Kiefern (Mountain-Pine mit **vollem Pfad**, Name doppelt), NS_Sparkling als Glitzern |
| 05 Blockgletscher | 1 465 | 225 | 34 | 5,0 m | Stirn, Fließwülste (`nach_ops` Damm), gefrorener Blasensee, Rahmen West |
| 06 Eisküste | 1 313 | 121 | 24 | 3,9 m | NS_Geyser_Small × 2 (Spritzfontänen), NS_Impact_Small |
| 07 Frostblumen | 8 990 | 41 | 1 | 8,3 m | Lagune mit Frostblumen 6/m² (Eiszapfen 0,05–0,12×), Rahmen NW/SW |
| 08 Glockenbach | 1 383 | 38 | 2 | 5,6 m | Eisglocken (Rocky Snow Pile 0,15–0,3×, Spritzeis) auf Bachsteinen, Rahmen Nordufer |

Je Feld: E2 5 986, E3 387, F2 12 734 Instanzen. Materialwünsche **6/6**: `Raureif` (Pflanze), `Schwarzeis`, `Spritzeis`
(Eis4), `Fels_Eisglasur` (Auflage), `Eisblasen` und `Eisrisse` (M_MS_Decal mit eigenen Texturen
`antworten/sehens/frost/decal_eisblasen.png`, `decal_eisrisse.png`, prozedural erzeugt; Generator im Arbeitsordner).
Die Eis-/Schnee-Megascans behalten `M_MS_Base_Trm` (E34, `material_fix_ausnahmen`).

**Lagenfenster > 400 m (E49, akzeptiert):** 422 × 338 m bei 02 (Leuchtfeuer), wegen des langen Froststeig-Abschnitts am
See; Begründung in `warnung_akzeptiert.lagen_fenster`, der Prüfer meldet nur einen HINWEIS.

## Verdeckung der Fundstücke (Plan, Ziel 3 m)

| Ort | heute → mit Plan | Rest |
|---|---|---|
| 01 Eisfall | Kern 2 → 3 (Anteil 0,40) | 51°/234 m/+52; 180–184° in ~265 m (Bachlücke, die bleibt offen) |
| 03 Eisvorhang | Kern 32 → **0** | Kern verdeckt; die Ränder sieht man noch (Nord 41) |
| 05 Blockgletscher | 3 → 3 | 276–279° in 503–514 m, **+240 m** (Grat darüber) |
| 07 Frostblumen | 39 → 11 | NW 324–333° in ~330 m (+70) und ~780 m (+285) |
| 08 Glockenbach | Kern 49 → **0** | Ost/Süd-Rand teilweise |

Die Rahmen sind Damm-Bögen (Moräne/Blockwall) mit Felsen und Gehölz darauf. Die Restblicke kommen von hohen Steigpunkten,
dort hilft kein Wall.

## Grenzen

- `SM_K13_FROSTSEE__*` werden nicht verwendet, unter 02 steht ein Freiraum (E23). Nach der Prüfung im Editor das Bild `frost_02_frostsee_held` mit und ohne Freiraum vergleichen.
- Eisfall, Eisvorhang, Frostblumen und Glockenbach entstehen aus `SM_EISZAPFEN_*` + Spritzeis. CryoGen bleibt als Wunsch stehen (Kauf erst, wenn das im Bild nicht trägt).
- Pivot/Schauseite: Arbeitsannahme E35.
