# sehens_lava – Planer Sehenswürdigkeiten Lava (Auftrag 13, Phase 2)

Baut die 8 Lava-Orte aus `antworten/sehens/lava/standorte.json` nach `sehens_lava_regeln.json` (Katalog
`sehens/lava/katalog.md` inkl. „Abgleich mit Inventar 13b und Entscheidungen 13c“, `asset_bedarf.json`, Inventar **13d**)
im Lieferformat `vorlagen/SEHENS_FORMAT.md`. Muster: [`../sehens_bergwald/`](../sehens_bergwald/README.md),
Schema: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_lava/sehens_lava.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/lava] [--gruppen] [--ohne-verdeckung]
python -I sehens_lava.py --basis <production>      # lokal: 1 m aus export/unreal/welt, Ausgabe dort
```

`--gruppen` listet je Ort die Stückzahl je Gruppe (Rezept-Abgleich). Ausgabe wie Bergwald, dazu Kachel-Dateien
`lagen/<ort>__<steig>_<k>_<Lage>.r8` für die ganzen Steige.

## Eigene Hooks (sehens_lava.py, keine Lib-Änderung)

| Regel-Schlüssel | Wirkung |
|---|---|
| `zugang` | Ort am Steig (`pfad_id`): zusätzlich der Fußweg `pfad_cm` (Steig → Ort) als Bodenband + Felsstufen, `orte.json` → `pfad_zugang`. `zugang.punkte` ersetzt ihn (Basaltorgel), `zugang.ende` lässt ihn am Blickpunkt statt im Loch enden (Glutauge). |
| `pfade_zusatz` | ganzer Steig aus `pfade` als Bodenband in Kacheln ≤ 400 m, `orte.json` → `pfade_zusatz` (mit `bodenband`-Blöcken). Kratersteig West (lava_07), Ost (lava_06), **Gipfelsteig** (lava_08, `serpentine`; die Kehren und den Anschnitt rechnet Ferats Werkzeug). |
| `pfad.ende` | Fußweg `pfad_cm` endet nicht in der Hohlform: bis `ab_m` vor dem Ort, dann eigene Punkte (Spalte: am Rand zur Rampe; Röhrenfenster: auf den Druckrücken). |
| `gelaende.senken_erlaubt` | geschlossene Senken einzeln bewertet: gewollte Hohlform im Kreis → HINWEIS mit Grund; Bestandsmulden (\|Δ\| < 0,5 m, nur am Stempelrand berührt) → HINWEIS; sonst bleibt die WARNUNG mit Lage der Restsenke. |
| `"mitte±x"` | Höhenangabe relativ zum Boden an der Ortsmitte (Grubensohle = Röhrenkerben, Spaltenspiegel). |
| `wasser[].ufer_erzwingen_m` | metrischer Uferring für den 106 × 11 m langen Spaltensee (der radiale Ring erreicht die Flanken nahe der Spitzen nicht). |
| `verdeckung` | Fundstücke 04/05/07/08 mit Stempel + Stücken gegen alle Wegpunkte (sehens_lib.verdeckung): alle **verdeckt** (Kern 0 Wegpunkte). |
| `materialien_mit` | Materialwunsch, den nur ein Decal nutzt (MI_EL_SW_Schwefel_Decal → lava_02). |

## Testlauf 2 m (Inventar 13d, 11.10.2026, 68 s, zwei Läufe byteidentisch)

Planer **0 FEHLER / 0 WARNUNG**; Prüfer (`orte.json` + `sw_lava`, mit Daten und Inventar) **0 FEHLER, 0 WARNUNG**,
7 HINWEISE (3 × optionales Decal `MI_EL_SW_Schwefel_Decal`, das Ferat aus dem Materialwunsch anlegt; 4 × Materialbefund
`SM_DryBranches_*` → Material-Fix sw_*). Eigene Prüfung `pfad_zugang`/`pfade_zusatz`: 0 FEHLER.

| Ort | Inst. | Koll. | Akt. | Held / Begl. / Schutt / Kleinz. / Bewuchs / Kontakt | Wasser | Effekte | Stempel |
|---|---|---|---|---|---|---|---|
| 01 Schwarze Mauer | 2 826 | 248 | 24 | 2 / 22 / 250 / 1 232 / 316 / 1 021 | – | 3 Decals | 3,0 m |
| 02 Schwefelgrund | 1 796 | 54 | 3 | 3 / 7 / 134 / 804 / 354 / 488 | 2 Quellen `thermal` | 3 Niagara, 2 Nebel, 12 Decals | 3,0 m |
| 03 Kraterkinder | 2 486 | 117 | 5 | 3 / 6 / 160 / 1 138 / 189 / 985 | 2 Kraterteiche, Rinnsal | Nebel, 6 Decals | 5,5 m |
| 04 Röhrenfenster | 1 948 | 66 | 8 | 3 / 5 / 118 / 806 / 590 / 426 | – | Nebel, 8 Decals | 8,9 m |
| 05 Klare Spalte | 3 232 | 110 | 46 | 1 / 49 / 114 / 1 570 / 1 178 / 317 (+30 Grund) | Spaltensee `tuerkis` | 8 Decals | 12,8 m |
| 06 Kraterreihe | 2 900 | 259 | 9 | 3 / 14 / 260 / 1 809 / 536 / 256 | – | Niagara, Nebel, 4 Decals | 2,2 m |
| 07 Basaltorgel | 2 020 | 139 | 21 | 16 / 15 / 111 / 575 / 1 010 / 296 | – | 6 Decals | 4,0 m |
| 08 Glutauge | 1 211 | 69 | 8 | 4 / 4 / 69 / 618 / 58 / 466 | – | Licht, 3 Niagara, Nebel, 9 Decals | 6,0 m |

Alle Orte unter §9. Je Feld: B6 3 208, C5 5 900, C6 8 694, D6 617 Instanzen. Material-Instanzen 6 von 6:
`MI_EL_SW_Lava_Moos`, `_Schlacke_Rot`, `_Schwefelkruste`, `_Schwefel_Decal`, `_Basalt_Saeule`, `_Lava_Glasur`.

## Umsetzung (Abgleich 13b/13c/13d)

- **Inventar 13d:** `SM_lava_wall_01…09` wieder da → Stirnschollen (01), Deckenplatten/-lippe (04), Spaltenwände 04/05 (05),
  Spatter (03, 06), Krustenlider und -platten 06/07/08 (08). Lava-Niagara statt Ersatz: `FX_Smoke_Volcano_01`
  (Dampfsäule 02), `FX_Lava_Smoke_02/03/1` (Fumarole, Quelle, Restdampf 06, Schacht 08), `FX_Lava_Bubble` und
  `FX_Distortion_Small` (Glutauge). Glut-Decals `MI_NM_Decal_Lava_NoAlbedoNoNormals_02`, Stricklava-Relief
  `MI_NM_Decal_Lava_Normals_04`, Glutfläche `SM_lava_disc` im Schacht; Nassband `MI_Deca_Wet`/`_Flat`, Lehm
  `MI_Decal_Clay_02` (Coast & Dunes).
- **Basaltorgel:** `Basalt_Basalt_Pillars_Wall/WallSlope/WallOverhang_SM` ×4,0–4,6 als Wand (Fuß am Schluchtboden,
  Oberkante 56–60 m ≈ gestempelte Kante 57–59 m), `Pillars_Cluster_High_SM` als freistehende Pfeifen, Säulengruppen
  `Pillar_*` ×4,5–6 als Foliage (nicht Akteur, kein Nanite), gekippte Säulen, Halde aus Säulenstücken in Schuttkegeln,
  nur **1** `Basalt_Basalt_Cliff_SM` (193 000 Dreiecke) am Nordende. 21 Akteure.
- **Verdeckung gebaut:** Druckrücken +3,5 m (04), Spalte unter Flur + Tumulus (05), Schlucht unter der Plateaukante (07),
  Schacht mit flachen Lidern ≤ 0,5 m über Grund (08) – Prüfung mit Plan: Kern 0 Wegpunkte (heute 6/79/1/96).
- **Senken:** Röhrenfenster, Glutschacht, Kraterkessel und Spalte sind gewollt (begründet); Schwefelmulde entwässert über
  eine Sinterrinne, Kerben der Mauer und kleine Krater sind nach außen offen, Sickerrinne hinter der Orgelkante.

## Grenzen und offene Punkte

- **Pivot `SM_lava_wall_*` unbekannt** (kein Eintrag in `netze_masse.json`): „unten Mitte“ angenommen; die
  `SM_lava_b/m/s_rock` desselben Pakets haben den Pivot in der Mitte – im Editor prüfen (sonst z + H/2).
- Schauseite der Basalt-Wandmodule (`front_achse +y`) ist eine Annahme – Prüfbild `_held`.
- Spaltensee: Breite 11 m in der Mitte (Katalog 4–9 m), sonst hält der Prüfer-Ufertest auf 2 m nicht; lokal auf 1 m enger möglich.
- Rinnsal der Kraterkinder versickert in der Senke (sie liegt 2–4 m unter dem Aue-Bach, ein Abfluss nach Norden ist
  ohne tiefen Einschnitt nicht möglich).
- Niagara-Systeme sind Vorlagen (Farbe/Dichte als Kopie anpassen, Hinweis je Effekt). **E14:** Dampfsäule (lava_02) als
  Kopie `NS_EL_SW_Dampfsaeule` (kopie_von `FX_Smoke_Volcano_01`, weiß 0,95/0,94/0,90, Deckkraft und Spawn ×0,5),
  Fumarolenfahne (lava_02, lava_06) als `NS_EL_SW_Fumarole` (kopie_von `FX_Lava_Smoke_03`); Ablage
  `/Game/Eldarien/Welt/FX/Sehens/` (E45).
- Klänge nur Wind/Wasser/Tropfen aus Free City & Nature Sounds als Platzhalter (Ferat erzeugt Klänge per KI, Klangpakete
  nicht geladen). **E18:** Wind-Cue an lava_01/06/07 mit `bedingung` – nur wenn der Laubanteil leise ist (Hörprobe), sonst
  dort stumm.
- **E16:** `MI_EL_SW_Basalt_Saeule` bekommt Albedo/Normal/ORM aus `/Game/Basalt` (Texturnamen lokal ablesen); haben Pillars-
  und Cliff-Netz verschiedene Textursätze, gilt das MI nur für die Pillars-Netze.
- **E17:** Der Gipfelsteig (`lava_pfad_gipfelsteig`) wird neu aus Ferats Serpentinen-Werkzeug gerechnet (`status` in
  `pfade_zusatz`); das Bodenband folgt bis dahin den Phase-1-Kehren. E40 (`SM_lava_disc`-Material) nur bei Befund.
