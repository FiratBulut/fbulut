# sehens_fjord – Sehenswürdigkeiten-Planer Fjord (Auftrag 13, Phase 2)

Baut die 8 Fjord-Orte aus `antworten/sehens/fjord/standorte.json` nach `sehens_fjord_regeln.json` (Katalog
`sehens/fjord/katalog.md` inkl. „Abgleich Inventar 13d“, `asset_bedarf.json`, `sehens/entscheidungen.json`).
`sehens_fjord.py` ist eine Kopie von [`../sehens_gletscher/sehens_gletscher.py`](../sehens_gletscher/README.md) mit
ausgetauschtem Biomnamen.

```
python -I recherche/antworten/skripte/sehens_fjord/sehens_fjord.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--orte ID ...] [--bild --bild-ordner recherche/antworten/sehens/fjord] [--ohne-sicht]
```

## Testlauf 2 m (11.10.2026, ~50 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer **0 FEHLER, 1 WARNUNG** (`lagen-Fenster` 01, s. u.).

| Ort | Inst. | Koll. | Akteure | Stempel | Held / Besonderheit |
|---|---|---|---|---|---|
| 01 Kanzel | 1 049 | 188 | 7 | 9,0 m | Platte `SM_MassiveTundraRockFormation_01` ×0,42 nach 313°, Wand darunter `vmnmbhv`/`veqnci0db`, Riss als Rinne mit Blöcken und Moos, Windkiefern |
| 02 Schleierwand | 1 903 | 232 | 7 | 17,1 m | 5 Fallbänder 204–228 m (E24) mit `material_hinweis` M_River_Water_Translucent, 3 Gumpen + Abflüsse, NS_Waterfall_Small × 2 + NS_Impact_Small, Felsrippen `vdssailfa`/`vfmjadufa` (Klippe_Fjordnass), Sturzkegel, Birken, Leakage + Deca_Wet |
| 03 Trollzunge | 713 | 151 | 6 | 1,0 m | Zunge `uchoab3fa` ragt hangab frei (Unterkante absolut 381,5 m), Unterbau `rcygn` 7 m im Grat, Frostschutt, Moospolster |
| 04 Hängetal | 2 027 | 300 | 7 | 14,6 m | Hochtalboden als ebene Stufe in die V-Rinne gesetzt (**begruendung**), mäandrierender Bach, Lippenfall 33 m, Gumpe; Klamm-Vorlage: NS_Waterfall_Medium an der Lippe, NS_Impact_Medium in der Gumpe, NS_Stream_Small im Bach |
| 05 Fjordkopf | 2 064 | 155 | 8 | 0,5 m | Schwemmfächer +0,5 m mit 2 Prielen, Watt-Blöcke, Treibholz `SM_beach_driftwood_*`, Tang `SM_seaweed_01_*`, Sanddorn, Decals Algae/Sand_Wet/Deca_Wet_Flat, NS_Stream_Small |
| 06 Bergsturz | 1 431 | 282 | 13 | 4,4 m | Abrissnische −3 m, Sturzkegel +4 m am Fuß, 11 Blöcke 5–9 m nach unten größer (Fächer t 0,6–1), sortierter Schutt, Pionierbirken |
| 07 Brandungsgrotte | 762 | 58 | 9 | 25,9 m | Spalt bis unter den Meeresspiegel geschnitten, Wände `SM_HugeNordicCoastalCliff_01/02`, Dach `SM_MassiveNordicCoastalCliff_01`, NS_Impact_Small + NS_Wake_Small, grünes Punktlicht, Algen-/Nassband |
| 08 Alte Ufer | 3 256 | 275 | 20 | 1,8 m | 3 Strandlinien entlang der Höhenlinien 31/51/73 m (Strandwälle als Damm), Kanten `SM_LS_beach_escarpment_*`, Rundkiesel, Muschelschill `SM_shells_01_A/B`, Birkengehölz |

Je Feld: C1 8 424, C2 103, D1 1 870, D2 2 808 Instanzen. Materialwünsche 3/6: `Klippe_Fjordnass`, `Schleierfall`
(nur falls der eigene Vorhang statt M_River_Water_Translucent genommen wird), `Fels_Flechte`.

**Warnung (begründet):** `lagen-Fenster 410 × 154 m` bei 01 (Leuchtfeuer). Der Kanzel-Ast `fjord_pfad_kanzel` gehört ganz
zu diesem Ort und ist 410 m lang.

Neu in der Lib für die Küste: Gruppenschlüssel `boden_min_m`. Rundkiesel und Tang an Prielen und im Spalt setzen
`boden_min_m: 0.0`, damit Rundungsunterschiede zwischen Stempelboden und Prüferboden kein „im Meer“ auslösen.

## Verdeckung der Fundstücke

| Ort | Ergebnis (Plan, Ziel 3 m) | Ursache |
|---|---|---|
| 04 Hängetal | 22 Punkte sehen den Kern | Fjordsteig in 86–151 m Abstand, **87–176 m höher**, Blick steil hinab |
| 05 Fjordkopf | 41 | Steig rundum an den Fjordwänden, 90–113 m, +29…+76 m |
| 06 Bergsturz | 49 | Ort liegt in einer 60–70°-Wand, Blick von unten (−41…−91 m) aus 90–290 m |
| 07 Brandungsgrotte | **verdeckt** (Kern 0) | – |
| 08 Alte Ufer | 43 | Hang mit Exposition 75°, der Oststeig gegenüber liegt in 280–340 m |

Der Fjord ist ein offenes U-Tal. Der Steig läuft an den Wänden über oder gegenüber den Orten. Ein Wall kann diese Blicke
nicht sperren. Die Versuche (Rahmen 04/05/06/08) sperrten 0–3 Punkte, standen teils quer im Bach und wurden deshalb
wieder herausgenommen. Gehölz (Birken 04/06/08) ist gesetzt, ändert die Zahlen aber kaum. Der Katalog beschreibt die Orte
selbst als „vom Fjordsteig erst auf den letzten 100 m“ sichtbar. Die Einstufung als Fundstück muss Ferat entscheiden
(siehe Bericht).

## Grenzen

- Die Mitte von 02 (Wand, 66°) und 06 (Wand, 70°) liegt in der Felswand, und `pfad_cm` endet dort. Besser wäre ein Ende am Wandfuß.
- 04: Das Gelände ist eine gleichmäßige V-Rinne mit 40–50° Gefälle, ein Hängetal gibt es dort nicht. Die Stufe (−11…+11 m) ist gebaut.
- Pivot/Schauseite: Arbeitsannahme E35 (Zunge 03 und Grottenwände 07 im Editor prüfen).
- Klang: Für Brandung, Möwen und Höhle gibt es keinen Cue. Ersatz sind Water-Stream- und Wind-Cues (Cave Ambience und Fantasy Ambiences stehen auf der Kaufliste).
