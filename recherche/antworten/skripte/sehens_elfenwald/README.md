# sehens_elfenwald – Sehenswürdigkeiten-Planer Elfenwald (Auftrag 13, Phase 2)

Baut die 8 Elfenwald-Orte aus `antworten/sehens/elfenwald/standorte.json` nach `sehens_elfenwald_regeln.json`
(Katalog `sehens/elfenwald/katalog.md` inkl. „Abgleich 13b/13c“, `asset_bedarf.json`, Inventar **13d**) im Lieferformat
`vorlagen/SEHENS_FORMAT.md`. Muster und Schema: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_elfenwald/sehens_elfenwald.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/elfenwald]
python -I sehens_elfenwald.py --basis <production>      # lokal: 1 m aus export/unreal/welt
```

Eigener Code nur im Hook `hook_treppe_kanten` (Elfentreppe): Er setzt nach den Seebecken je Stufe zwei Kalktuff-Kanten
links und rechts des Überlaufs (Anker `kante_<k>_l/_r`, `fall_<k>`). Alles andere sind Regeln.

## Testlauf 2 m (11.10.2026, 91 s, zwei Läufe byte-identisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer (`orte.json` + `sw_elfenwald`) **0 FEHLER, 0 WARNUNG, 0 HINWEIS**.

| Ort | Inst. | Koll. | Akt. | Held / Begl. / Schutt / Kleinzeug / Bewuchs / Kontakt | Stempel | Wasser | Niagara (13d) |
|---|---|---|---|---|---|---|---|
| 01 Mutterbaum | 2 608 | 105 | 14 | 1 / 15 / 91 / 2 184 / 108 / 199 (+24 Wurzelstufen) | 1,4 m | Pfütze im Wurzelloch | NS_Sparkling_Glow (opt.) |
| 02 Nebelhain | 3 596 | 178 | 16 | 9 / 7 / 69 / 3 030 / 111 / 277 (+109 Pfadstufen) | – | – | – (2 Nebel in den Kronen) |
| 03 Rotlaubhain | 3 721 | 60 | 12 | 1 / 11 / 60 / 3 341 / 151 / 169 | – | – | NS_leaf (opt., rot) |
| 04 Elfentreppe | 3 455 | 94 | 16 | 10 / 6 / 59 / 1 640 / 1 335 / 337 (+70 Beckenkiesel) | 1,8 m | 5 Becken `tuerkis` + 6 Bachstücke | NS_Stream_Small ×2, NS_Impact_Small |
| 05 Farnschlucht | 5 387 | 151 | 13 | 1 / 12 / 170 / 850 / 2 664 / 1 675 | 2,5 m | Tobelbach (Quelle) + Tropfwand 6 m | NS_Waterfall_Small, NS_Impact_Small, NS_Stream_Small |
| 06 Blauer Grund | 8 276 | 40 | 10 | 2 / 8 / 40 / 1 520 / 6 595 / 121 | – | – | NS_Sparkling_Noise (opt.) |
| 07 Schwammgrund | 1 809 | 90 | 7 | 2 / 5 / 90 / 1 444 / 125 / 150 | 0,2 m | Pfütze in der Tellergrube | NS_Sparkling (opt.) |
| 08 Wurzelbrücke | 2 106 | 56 | 8 | 1 / 7 / 71 / 1 113 / 517 / 393 | 1,9 m | Tümpel im Wurzelloch | NS_Wake_Small |

Alle Orte unter §9. Je Feld: G3 2 608, G4 10 085, H3 11 756, H4 2 913, I4 3 596 Instanzen.
Material-Instanzen 5 von 6: `MI_EL_SW_Rotlaub` (rot getönte **Kopie** der Buchenblatt-Instanz, Original bleibt – 13c),
`_Rotlaub_Boden`, `_Bartflechte`, `_Kalktuff`, `_Blaugrund`.

## Umsetzung (Katalog + 13c/13d)

- **Mutterbaum:** `SM_beech_tree_05` ×2,5 (≈ 54 m) auf der Kuppe, 6 Brettwurzeln `SM_beech_old_roots_01` ×5–6 radial
  (Nischen mit Mountain-Pilzen + 2 kalt-grünen Punktlichtern), toter Rivale + liegender Partner mit Wurzelteller
  `SM_stones_roots_01` hochkant und Wurzelsträngen `SM_roots_04_A/B`, Lichtung als Freiraum r 25 m.
- **Nebelhain:** Serpentinenpfad 0,9 km (`pfad_cm` aus `standorte.json`, Ferat 13c: ja) mit Felsstufen; 9 windgebeugte
  Altbäume (kipp 6–12° nach W), Bartflechten `SM_Ivy_11/21` (Pivot oben, hängen) mit `MI_EL_SW_Bartflechte`, Felsrippen,
  Moosbett mit ausgefranstem Rand, Mountain-Hangwurzeln über Fels; 2 lokale Nebel in 14/20 m Höhe, keine FogBank-Blueprints
  (E06); bewegte Fetzen optional als Niagara-Kopie `NS_EL_SW_Nebelfetzen` (kopie_von `NS_Smoke_Plume`, 12 m, Cull 120 m, E07).
- **Rotlaubhain:** Altbuche + Hain in Gruppen (Cluster statt Raster), Laubzunge 90 m hangab, Rand fleckig.
- **Elfentreppe:** der Bach `B_R_P4_M1_01` wird zu 5 Tuffbecken (Seen mit Uferring = Sinterdamm) und 4 Stufen mit Fällen
  > 0,8 m; Tuffkanten-Akteure seitlich der Überläufe (Hook). `ist_wasser`: der Ort IST dieser Bach.
  **E10:** `ersetzt_bestandsbach` (s 0–72 m der Linie `treppe`) → `orte.json` `bestand_ausblenden`: der Setzer blendet
  `B_R_P4_M1_01` auf diesem Abschnitt aus, oben und unten schließt der Bestand an.
- **Farnschlucht:** Tobellinie aus dem Wasserraster, Rinne + Wände nachgeschärft, Quellwand `SM_HugeMossyForestCliff_01`
  hochkant, Farnwände in drei Dichten (kein Rechteck-Rand), Tropfwand-Decals `MI_Leakage_05–08`.
- **Blauer Grund:** Teppich aus `SM_Periwinkle_*` ×0,35–0,5 mit `MI_EL_SW_Blaugrund`, dichter im Lichtschacht, fleckiger
  Übergang; Spotlicht + Nebel, Kronenlücke als Freiraum.
- **Schwammgrund:** liegender Riese (`SM_LargeFallenTree_02` ×4,6 + `SM_MossyTree_01` ×3, 48 m), Riesenschirmlinge
  (Ersatz), Konsolen = Mountain `SM_mushroom_red-belted_conk_*`, Kleinpilze Mountain-Arten, Brennnessel am Teller.
- **Wurzelbrücke:** Stamm 34 m quer über die Kerbe, Unterkante 6 m über dem Bach, Enden 0,5 m in den Ufern; Ammenbuchen
  und Moos auf dem Stamm, Wurzelteller 8 m hochkant, Tümpel im Wurzelloch.
- **13d:** Nature Water FX an allen Fällen/Stufen (nicht mehr optional), Nassband `MI_Deca_Wet(_Flat)` mit Verteilung `ufer`
  an allen Wasserorten, `material_hinweis` Mountain-Wassermaterial an Bächen/Fällen, `SM_Pine_roots_01` mit vollem Pfad.

## Grenzen

- Pivot/Schauseite: `SM_HugeMossyForestCliff_01`, `SM_stones_roots_01` (Hochkant-Schauseite) sind Annahmen – Editorbild.
- Skalierte Nicht-Nanite-Buchen (×2,5) und Pilze (×7–12) können grob wirken (Katalog-Risiko; Pakete in `assets_wunsch`).
- 2-m-Daten: Tuffbecken-Ufer 2 Zellen breit; lokal auf 1 m werden Stufen und Dämme feiner.
