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

Planer 0 FEHLER / 0 WARNUNG; Prüfer **0 FEHLER, 0 WARNUNG** (Lagenfenster 01 akzeptiert, E49). Seit **E46** hat der Fjord
7 Leuchtfeuer und 1 Fundstück (07 Brandungsgrotte).

| Ort | Inst. | Koll. | Akteure | Stempel | Held / Besonderheit |
|---|---|---|---|---|---|
| 01 Kanzel | 1 049 | 188 | 7 | 9,0 m | Platte `SM_MassiveTundraRockFormation_01` ×0,42 nach 313°, Wand darunter `vmnmbhv`/`veqnci0db`, Riss als Rinne mit Blöcken und Moos, Windkiefern |
| 02 Schleierwand | 1 903 | 232 | 7 | 17,1 m | 5 Fallbänder 204–228 m (E24) mit eigenem Vorhang `MI_EL_SW_Schleierfall` (E48, `material_wunsch`), Gumpen/Bäche mit `material_hinweis` M_River_Water_Translucent, 3 Gumpen + Abflüsse, NS_Waterfall_Small × 2 + NS_Impact_Small, Felsrippen `vdssailfa`/`vfmjadufa` (Klippe_Fjordnass), Sturzkegel, Birken, Leakage + Deca_Wet |
| 03 Trollzunge | 713 | 151 | 6 | 1,0 m | Zunge `uchoab3fa` ragt hangab frei (Unterkante absolut 381,5 m), Unterbau `rcygn` 7 m im Grat, Frostschutt, Moospolster |
| 04 Hängetal | 2 027 | 300 | 7 | 14,6 m | Hochtalboden als ebene Stufe in die V-Rinne gesetzt (**begruendung**), mäandrierender Bach, Lippenfall 33 m, Gumpe; Klamm-Vorlage: NS_Waterfall_Medium an der Lippe, NS_Impact_Medium in der Gumpe, NS_Stream_Small im Bach |
| 05 Fjordkopf | 2 064 | 155 | 8 | 0,5 m | Schwemmfächer +0,5 m mit 2 Prielen, Watt-Blöcke, Treibholz `SM_beach_driftwood_*`, Tang `SM_seaweed_01_*`, Sanddorn, Decals Algae/Sand_Wet/Deca_Wet_Flat, NS_Stream_Small |
| 06 Bergsturz | 1 431 | 282 | 13 | 4,4 m | Abrissnische −3 m, Sturzkegel +4 m am Fuß, 11 Blöcke 5–9 m nach unten größer (Fächer t 0,6–1), sortierter Schutt, Pionierbirken |
| 07 Brandungsgrotte | 762 | 58 | 9 | 25,9 m | Spalt bis unter den Meeresspiegel geschnitten, Wände `SM_HugeNordicCoastalCliff_01/02`, Dach `SM_MassiveNordicCoastalCliff_01`, NS_Impact_Small + NS_Wake_Small, grünes Punktlicht, Algen-/Nassband |
| 08 Alte Ufer | 3 256 | 275 | 20 | 1,8 m | 3 Strandlinien entlang der Höhenlinien 31/51/73 m (Strandwälle als Damm), Kanten `SM_LS_beach_escarpment_*`, Rundkiesel, Muschelschill `SM_shells_01_A/B`, Birkengehölz |

Je Feld: C1 8 424, C2 103, D1 1 870, D2 2 808 Instanzen. Materialwünsche 3/6: `Klippe_Fjordnass`, `Schleierfall`
(E48: Vorhang der Schleierwand-Fälle; der Vorhang trägt die Fernsicht, Niagara ergänzt in der Nähe), `Fels_Flechte`.
`M_River_Water_Translucent` steht nur noch als `material_hinweis` an Bächen und Gumpen.

**Lagenfenster > 400 m (E49, akzeptiert):** 410 × 154 m bei 01 (Leuchtfeuer). Der Kanzel-Ast `fjord_pfad_kanzel` gehört ganz
zu diesem Ort und ist 410 m lang; Begründung in `warnung_akzeptiert.lagen_fenster`, der Prüfer meldet nur einen HINWEIS.

Neu in der Lib für die Küste: Gruppenschlüssel `boden_min_m`. Rundkiesel und Tang an Prielen und im Spalt setzen
`boden_min_m: 0.0`, damit Rundungsunterschiede zwischen Stempelboden und Prüferboden kein „im Meer“ auslösen.

## E46 – Fundstück → Leuchtfeuer (04, 05, 06, 08)

Ein Fjord ist eine Aussichtslandschaft, der Fjordsteig ein Panoramaweg. Im offenen U-Tal ließen sich 04/05/06/08 nicht
verstecken: Wälle sperrten 0–3 Steigpunkte und wurden wieder entfernt. Deshalb sind die vier Orte jetzt Leuchtfeuer
(`standorte.json`: `art`, `ziel_hoehe_m`, `sicht`, neue Kamera `_fern`; Katalog mit Vermerk E46). Nachweis mit
`sicht.sicht_von_wegen` gegen Wege + Steige, Ring 300–800 m:

| Ort | Silhouette | Punkte mit Sicht (≥ 30 %) | lesbar bis | `_fern` |
|---|---|---|---|---|
| 04 Hängetal | 12 m (Lippe + Fall) | 6 / 134 | 465 m | 465 m (X −1642 / Y −2312) |
| 05 Fjordkopf | 4 m (Fächer) | 19 / 66 | 433 m | 433 m (X −1616 / Y −2948) |
| 06 Bergsturz | 10 m (Blockkegel) | 16 / 69 | 330 m | 330 m (X −1562 / Y −3008) |
| 08 Alte Ufer | 4 m (Stufenbänder) | 37 / 76 | 628 m | 498 m (X −1664 / Y −3072) |

Von bestehenden Wegen allein sieht keiner der vier Orte (der Fjord hat keinen Weg). Die Marker haben jetzt
`entdeckung_m` 100. Für 07 (Fundstück) zeigt die Verdeckungsprüfung den Kern **verdeckt** (0 Steigpunkte).

## Grenzen

- Die Mitte von 02 (Wand, 66°) und 06 (Wand, 70°) liegt in der Felswand, und `pfad_cm` endet dort. Besser wäre ein Ende am Wandfuß.
- 04: Das Gelände ist eine gleichmäßige V-Rinne mit 40–50° Gefälle, ein Hängetal gibt es dort nicht. Die Stufe (−11…+11 m) ist gebaut.
- Pivot/Schauseite: Arbeitsannahme E35 (Zunge 03 und Grottenwände 07 im Editor prüfen).
- Klang: Für Brandung, Möwen und Höhle gibt es keinen Cue. Ersatz sind Water-Stream- und Wind-Cues (Cave Ambience und Fantasy Ambiences stehen auf der Kaufliste).
- **13f:** fjord_02: Geländefenster 270 × 200 m, damit die Abflüsse unter den Gumpen ganz gestempelt werden (≥ 25 m).
