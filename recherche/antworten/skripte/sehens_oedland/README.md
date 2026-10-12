# sehens_oedland – Sehenswürdigkeiten-Planer Ödland (Auftrag 13, Phase 2)

Baut die 8 Ödland-Orte aus `antworten/sehens/oedland/standorte.json` (inkl. **Ödlandpfad**, 3 Äste in `pfade`) nach
`sehens_oedland_regeln.json` (Katalog, `asset_bedarf.json` inkl. `abgleich_13d`, Inventar 13d). Aufbau wie
[`../sehens_canyon/`](../sehens_canyon/) (Hook `daemme`, Verdeckungsprüfung der Fundstücke).

```
python -I recherche/antworten/skripte/sehens_oedland/sehens_oedland.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--bild --bild-ordner recherche/antworten/sehens/oedland]
```

## Ödlandpfad – jeder Meter in genau einem Lagenfenster

| Ast (Länge) | Abschnitt → Ort |
|---|---|
| Abstieg (490 m) | 0–160 m → oedland_02 (`pfad.abschnitte`), 160–490 m → oedland_05 |
| Ost (827 m) | 0–230 m → oedland_05, 230–608 m → oedland_06 (+ Zugang), 608–827 m → oedland_03 |
| West (550 m) | 0–380 m → oedland_05, 380–530 m → oedland_07, 530–550 m → oedland_08 (+ Zugang) |

Dafür hat die Lib (additiv) `pfad.pfad_id`, `pfad.abschnitt [von, bis]` und `pfad.abschnitte` bekommen (`orte.json`:
`pfad`, `pfad_zugang`, `pfad_abschnitte`). Die übrigen Orte bekommen ihren Fußweg `pfad_cm` als Band. Felsstufen ab 18°.

## Testlauf 2 m (11.10.2026, ~43 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer **0 FEHLER, 0 WARNUNG**, 1 HINWEIS.

| Ort | Inst. | Koll. | Akteure | Stempel | Held / Besonderheit |
|---|---|---|---|---|---|
| 01 Rippenland | 2 798 | 78 | 12 | 5,3 m | 8 Rinnen radial vom Grat (verschieden lang/tief), 7 Messerrücken (Formation Layered), Schwemmkegel aus Mound/Slope Mud, toter Baum auf dem Grat |
| 02 Regenbogenhang | 2 275 | 60 | 27 | 3,4 m | Bänder: Cliff Layered + `SM_big_rock_wall_*` in Rot/Violett, farbige Schwemmkegel, Ödlandpfad-Abstieg 0–160 m |
| 03 Höllentor | 1 247 | 69 | 24 | 4,5 m | Krater (Boden +0,3 m, Auswurfwall +4,5 m → ~8 m tief), verrußte Wand, NS_EL_SW_Gasflammen (Kopie von NS_Fire, E15) + FX_Lava_Smoke_02 + FX_Distortion_Big, 2 Glutlichter, Glut-/Ruß-Decals |
| 04 Dornbusch-Senke | 1 632 | 31 | 1 | 3,2 m | Senke −1,5 m mit Abflussrinne, toter Baum `SM_Dead_Tree_02`, Dornriegel, Nebel |
| 05 Kugelsteine | 1 908 | 94 | 11 | 6,4 m | Fächer +1,5 m, Kolk bis +0,4 m, Konkretionen halb in der Wand, Pfad-Knoten (3 Abschnitte) |
| 06 Schlammvulkänchen | 799 | 16 | 0 | 3,5 m | 7 Kegel mit Krater-`see` (moorbraun), Mud-Mound-Mäntel, Ringwall, 2× NS_EL_SW_Schlammblasen (Kopie von NS_Bubble_Burst, E15) + NS_SmokePuffLight |
| 07 Totenpfanne | 866 | 26 | 11 | 3,7 m | Pfanne −3,5 m + Uferwall Nord, 11 schwarze tote Bäume, Riss-Decals |
| 08 Erdröhren | 933 | 12 | 5 | 8,0 m | 3 Schlucklöcher (−7/−5/−4 m), Einbruchrinne, Erdbrücke über dem Hauptschacht, Nebel im Schacht |

Verdeckung: 04–08 verdeckt; 05, 07, 08 erst mit dem Stempel (Pflicht), 06 dank Ringwall.
Materialwünsche 6/6: `Oedland_Ton`, `_Rot`, `_Violett`, `Russ`, `Konkretion`, `Totholz_Schwarz`.

## Grenzen und offene Punkte

- Meeresniveau: Krater (03), Kolk (05) und Salsenmulde (06) liegen im Flachland bei 4–7 m; Sohlen bleiben ≥ +0,3 m, die
  Tiefe kommt zum Teil aus Wällen. Gewollte Hohlformen tragen `senke_begruendung`.
- Niagara-Kopien entschieden (E15/E45): `NS_EL_SW_Gasflammen` (Flammen 0,3–0,8 m, viele Quellen auf r 12 m, ohne Funken)
  und `NS_EL_SW_Schlammblasen` (schlammgrau 0,35/0,32/0,28, Größe ×0,5, Spawn ×0,4) unter `/Game/Eldarien/Welt/FX/Sehens/`,
  jeweils mit `kopie_von` und `kopie_aenderungen` in `orte.json`; die Originale bleiben unberührt.
- Ein Feuerklang fehlt im Bestand (Wunsch Fantasy Ambiences).
- **13f:** Salsen < 10 m² sind jetzt Lage Schlamm statt Epic-See (A13).
- **Nachtrag 13k (Stammausrichtung):** Die Gruppe `staemme` der Dornbusch-Senke steht weiter auf `liegend`. Das passt
  nur zum stehend modellierten `SM_EuropeanBeech_Dead_M_01`. Die liegend modellierten `SM_dead_log_01/03` standen
  damit senkrecht. Das Rezept setzt sie jetzt selbst mit `normale` (8 Stämme, der Hangnormalen folgend, lange Achse in
  Yaw-Richtung). Liegende Stämme als Instanzen sind auf Skala ≤ 1,8 begrenzt: 4 Stämme der Dornbusch-Senke und 9 der
  Totenpfanne (`liegende`, vorher bis × 2,0). Ergebnis in `antworten/13k-pilot2-bildbefund-15g-nachtrag.md`.
