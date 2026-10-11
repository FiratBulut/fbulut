# sehens_wueste – Sehenswürdigkeiten-Planer Wüste (Auftrag 13, Phase 2)

Baut die 8 Wüsten-Orte aus `antworten/sehens/wueste/standorte.json` nach `sehens_wueste_regeln.json` (Katalog
`sehens/wueste/katalog.md`, `asset_bedarf.json` inkl. `abgleich_13d`, Inventar 13d) im Lieferformat `vorlagen/SEHENS_FORMAT.md`.
Aufbau wie [`../sehens_canyon/`](../sehens_canyon/) (Hook `daemme`, Verdeckungsprüfung der Fundstücke).

```
python -I recherche/antworten/skripte/sehens_wueste/sehens_wueste.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/wueste]
```

**Die gebauten Wüstenfelder werden nur ergänzt:** keine `freiraeume`, kein `entfernen` in `plan.json`.

## Testlauf 2 m (11.10.2026, ~58 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer **0 FEHLER, 0 WARNUNG**, 12 HINWEIS (eigenes Salz-Decal optional).

| Ort | Inst. | Koll. | Akteure | Stempel | Held / Besonderheit |
|---|---|---|---|---|---|
| 01 Yardang-Flotte | 2 684 | 106 | 12 | 3,0 m | 4 Rümpfe NW→SO: Bug `veonegs` (Formation XL 01), Rumpf/Heck Cliff/Ledge Layered; Schutt nur am Bug, Sandfahnen im Lee |
| 02 Sterndüne | 947 | 37 | 1 | 22,5 m | Düne aus Kegel + 3 Kammwällen (Hook `daemme`), halb begrabener toter Köcherbaum, Rippel-Decals (Coast & Dunes) |
| 03 Die Wächter | 2 451 | 77 | 19 | 1,7 m | 7 Pilzfelsen: Fuß Desert Spire (gedrungen) + Kappe `SM_RockSandstone_040` (Wüstenlack), Deflationspflaster |
| 04 Quelloase | 1 364 | 113 | 12 | 7,0 m | Quelltopf `tuerkis` + Rinnsal (versickert), 5 Fächerpalmen + Jungpalmen, Feuchtring, NS_Stream_Small, Nassband |
| 05 Salzpfanne | 1 033 | 18 | 10 | 6,0 m | Pfanne −1 m + Dünenriegel +6 m (Pflicht-Verdeckung), Restsole `salzweiss`, 9 Salz-Decals (eigene Textur `decal_salzkruste.png`) |
| 06 Windkanter-Feld | 8 255 | 141 | 1 | – | 8 000 eingeregelte Pflastersteine (NW–SO), Dreikanter mit Wüstenlack |
| 07 Trockenes Wadi | 1 392 | 110 | 7 | 2,0 m | Flutrinne mit sortiertem Geröll, Fallkante (Ledge Rock), Prallhänge mit Treibholz 1,8 m über der Sohle, 2 Akazien-Ersatz |
| 08 Wabenwand | 961 | 36 | 10 | – | Nordwand aus Cliff Layered, Nische mit Köcherbaum, 12 Decals (Lack + Waben-Ersatz Clay) |

Je Feld: D3 2 640, E3 3 786, E4 12 661 Instanzen. Verdeckung (Fundstücke 04–08): alle verdeckt.
Materialwünsche 6/6: `Wuestenlack`, `Salzkruste`, `Wueste_Sandauflage`, `Salz_Decal` (M_MS_Decal + PNG),
`Waechter_Kreide` (E01: M_MS_Base, kreidehell, Füße der Wächter nur `ulbwebv_tier_0`, `vepoda2_tier_0` entfällt) und
`Wabenfels` (E30: M_EL_Fels_MS in Sandsteintönung für die Wabennischen).

## Grenzen und offene Punkte

- Wadi (07): der 2-m-Talgrund ist schon eine geschlossene Hohlform → `senke_begruendung`; im 1-m-Lauf prüfen.
- Pilzfelsen (03) sind gebändert statt kreideweiß (Desert-Western-Spires laut 13d); weiße Kappen nur per Material möglich.
- Wabenwand (08): Decals + Probe `wabennischen` (4 Akteure `SM_lava_wall_04`/`_09`, 3–5 m, `MI_EL_SW_Wabenfels`, E30).
  Hollowstone Canyon entscheidet Ferat nach dem Editorbild der Probe.
