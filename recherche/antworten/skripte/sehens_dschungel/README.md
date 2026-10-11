# sehens_dschungel – Sehenswürdigkeiten-Planer Dschungel / Turmkarst (Auftrag 13, Phase 2)

Baut die 8 Dschungel-Orte aus `antworten/sehens/dschungel/standorte.json` nach `sehens_dschungel_regeln.json`
(Katalog `sehens/dschungel/katalog.md` inkl. „Abgleich 13b/13c“, `asset_bedarf.json`, Inventar **13d**) im Lieferformat
`vorlagen/SEHENS_FORMAT.md`. Muster und Schema: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_dschungel/sehens_dschungel.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/dschungel]
```

Eigener Code nur im Hook `hook_see_kontur` (Blaues Auge, Verborgene Lagune; Regel-Schlüssel `see_kontur`): Seen in
natürlichen Kesseln, die keine Ellipse sind. Umriss = Kesselkontur aus dem Gelände (sternförmig, weitester Seepunkt je
Strahl), Grund nur vertieft und nur mit Abstand zur Kesselwand, Wände unverändert – so schneidet der Stempel keine
Schachtwand an und erzeugt keine neue Senke.

## Testlauf 2 m (11.10.2026, 51 s, zwei Läufe byte-identisch)

Planer 0 FEHLER, 2 WARNUNG (begründet, unten); Prüfer (`orte.json` + `sw_dschungel`) **0 FEHLER, 0 WARNUNG**, 3 HINWEIS
(5 Kleinteile ganz im Boden, 14 Instanzen im Bestandsbach am Quellbach).

| Ort | Inst. | Koll. | Akt. | Held / Begl. / Schutt / Kleinzeug / Bewuchs / Kontakt | Stempel | Wasser | Niagara (13d) |
|---|---|---|---|---|---|---|---|
| 01 Mondtor | 1 520 | 126 | 14 | 3 / 9 / 97 / 900 / 50 / 445 (+30 Kalkstufen) | 6,2 m | – | – |
| 02 Turmquelle | 2 418 | 125 | 6 | 1 / 5 / 120 / 866 / 529 / 862 (+40 Beckengrund) | 9,1 m | Tosbecken `tuerkis`, Quellbach 135 m, Fall 60 m | NS_Waterfall_Large, NS_Impact_Large, NS_Stream_Small |
| 03 Steinwald | 2 284 | 224 | 64 | 58 / 6 / 281 / 1 400 / 96 / 480 (+27) | 1,6 m | – | – |
| 04 Blaues Auge | 2 837 | 37 | 15 | 9 / 6 / 46 / 1 498 / 681 / 612 | 15,7 m | Cenote `tuerkis`, Spiegel +0,3 m, 18 m tief | – |
| 05 Verborgene Lagune | 1 261 | 97 | 9 | 5 / 4 / 67 / 494 / 163 / 495 (+42) | 32,2 m | Lagune `smaragd`, Spiegel 19 m | – |
| 06 Schluckhöhle | 1 386 | 77 | 11 | 3 / 8 / 108 / 950 / 222 / 106 | 5,7 m | Schwinde-Bach (versickert), Strudeltopf | NS_Stream_Small |
| 07 Garten der Riesen | 2 207 | 63 | 3 | 125 / 39 / 40 / 1 350 / 279 / 360 (+17 Trittsteine) | – | Bach bleibt (Trittsteine) | – |
| 08 Sinterhalle | 1 346 | 115 | 10 | 2 / 8 / 130 / 950 / 198 / 68 | 11,1 m | Tropfbecken `klar` | NS_Waterfall_Small, NS_Impact_Small |

Alle Orte unter §9. Je Feld: G5 2 914, G6 3 671, H6 5 801, I6 1 527, I7 1 346 Instanzen.
Material-Instanzen 3 von 6: `MI_EL_SW_Kalk_Nass`, `MI_EL_SW_Sinter`, `MI_EL_SW_Riesenblatt`. Die `SM_Cliff_01*`-Stücke
(Bogen, Nadeln, Schachtwände) bekommen **keine** Material-Überschreibung, damit sie die Felsfarbe der Türme behalten.

## Umsetzung (Katalog + 13c/13d)

- **Mondtor:** Bogen aus 2 Pfeilern `SM_Cliff_01c` ×0,35 und Sturz `SM_Cliff_01b` (0,7/0,33/0,32) auf dem Gipfelplateau,
  Torachse 30° = Kluftrichtung, Öffnung ≈ 16 × 14 m gegen den Himmel (Schauseite zur `_fern`-Kamera 120°). Fugen:
  4 Zwickelblöcke `SM_LimestoneRocks3`, Lianen vom Sturz, Moos-/Sinter-Decals an den Fugen, Grus- und Geröllsaum.
  Sockel per Geländestempel (2 Kuppen +2,5 m) und Torsohle als nach beiden Seiten offene Kerbe −4 … −6 m (13c).
- **Turmquelle:** Quellmund 45 m hangauf (Lippe `SM_Cliff_01e`), Fall in ein in den Wandfuß gegrabenes Tosbecken
  (Spiegel = tiefster Uferpunkt, Abfluss über eine Lippe), Quellbach nach WNW in `B_R2_R_P3_P1_01`, Sprühzone.
- **Steinwald:** 58 Kalknadeln (`SM_Cliff_01b–e` aufrecht, schmal skaliert, je anders gedreht), Gassen mit Karren, Palmen,
  Farn, Lianen; Schulter leicht verebnet.
- **Blaues Auge:** eigener See (13c, `tuerkis`, unabhängig vom Meer) mit Schachtkontur (Hook), 9 Wandschalen
  `SM_Cliff_01d` rundum (Fuß im Wasser), Riesenbaum, Luftwurzeln (Lianen + `SM_roots_04/05` hochkant), Lichtkegel.
- **Verborgene Lagune:** Gasse 43 × 7 m durch die Wand (Sohle 24,5 → 23,5 m, nach außen fallend), Überhänge
  `SM_Cliff_01b` an den Gassenkanten, Lagune in der Kesselkontur < 19 m (Hook), Seerosen, Lianenvorhang, Uferwurzeln.
- **Schluckhöhle:** Schwinde-Trichter 30 × 20 m, −5 m, Bachende als `bach` ins Portal (`versickert`), Portal aus
  Felsplatte + Laibung, Treibholzstau, Strudeltopf.
- **Garten der Riesen:** Pestwurz ×3–4 mit `MI_EL_SW_Riesenblatt` + `SM_Fern_01a` ×2 als Riesenblätter, 2 Urwaldriesen,
  gestürzter Stamm, Palmen, gelbe Blüten.
- **Sinterhalle:** Felsdach `SM_Cliff_01b` ×0,38 als Überhang (Unterkante ~10 m über dem Hallenboden), ebener Hallenboden
  (hinten abgetragen, vorne Schuttterrasse), Tropfbecken mit Sinterrand, 7 Sinter-/Nässe-Decals an der Wand.
- **13d:** Nature Water FX (Fall, Aufprall, Strom) statt der optionalen Platzhalter, Nassband `MI_Deca_Wet(_Flat)`
  (Verteilung `ufer`) an allen Wasserorten, Mountain-Wurzeln, `material_hinweis` Mountain-Wassermaterial.
  **Große Kalkfelsen fehlen laut `netze.csv` weiter** (nur `SM_LimestoneRocks2/3`, `Limestone_Rocks_ubqwdheda_High`)
  → Ersatz `SM_Cliff_01a–e` bleibt, „Megascans Limestone Rocks“ steht in `assets_wunsch`.

## Warnungen (begründet)

- **Verborgene Lagune, Senke 24 m²:** Der Kessel ist von Natur aus geschlossen (Boden 9,5 m, Überlauf 38 m). Die Gasse
  öffnet die Wand über seiner Schwelle; die Kesselzellen neben dem Gassenmund zählen nur wegen der Nachbarschaft zur
  Änderung. Wasser kann den Karstkessel nicht oberirdisch verlassen (versickert) – gewollt.
- **Schluckhöhle, Senke 52 m²:** Die Schwinde IST eine geschlossene Senke mit Abfluss in den Untergrund (Begründung in
  `gelaende.begruendung`).

## Grenzen

- `SM_Cliff_01*` haben keine Bounds in `netze_masse.json` → Pivot „unten Mitte“ angenommen, Schauseiten Annahme.
- Der Bogen ist zusammengesetzt; aus 500 m (`_fern`) zuerst prüfen (Katalog-Plan B: Kerbe statt Sturz).
- Riesenblätter bleiben „groß, aber europäisch“, bis ein Tropenpflanzen-Paket da ist.
