# wasserherkunft – Woher kommt das Wasser unserer Fälle? (Auftrag 17)

Bericht: [`../../17-wasserherkunft-wasserfaelle.md`](../../17-wasserherkunft-wasserfaelle.md).
Ergebnis (Vorschlagsdaten, nichts eingebaut): [`../../wasserherkunft/faelle_herkunft.json`](../../wasserherkunft/faelle_herkunft.json).

Das Skript **liest nur** (kein Planer, kein Gelände wird geändert):

| Eingabe | Wozu |
|---|---|
| Weltdaten 2 m (`sehens_lib.daten.lade`) | Höhe, Biom, Boden, Meer, `wasser_welt.json` (Welt-Wasserfälle WF_K1/WF_K8, Seen), `teiche.json` |
| `--fs` = Ausgabe von `fluss_sim/fluss_sim_export.py` | Fälle mit `vorhang: true`, Gewässer-Spline (Lauflänge oberhalb), Anfang/Mündung (auch `wasserfall`) |
| `--sehens` = Ausgaben der Sehens-Planer (`<biom>/orte.json`) | `wasser` vom Typ `wasserfall`, Bäche und Seen am Fall |
| `../../wasser_fx/plan.json` | Breite der Welt-Wasserfälle |
| `sehens_lib.gelaende.Gelaende` | D8-Abfluss mit gefüllten Senken (Cache `.npy`) |

## Aufruf (Cloud, 2 m)

Planer-Ausgaben wie im fluss_sim-README erzeugen (Gefälle `--alle`, 15 Sehens-Planer, `bachbett_roh.py`,
`fluss_sim_export.py`), dann:

```
python -I recherche/antworten/skripte/wasserherkunft/wasserherkunft.py --daten2m recherche/vorlagen/daten/sehens \
       --fs <s>/fs --sehens <s>/sehens --aus recherche/antworten/wasserherkunft --bild
```

Lokal (1 m): `--daten1m export/unreal/welt --fs export/unreal/welt/fluss_sim --sehens export/unreal/welt/sehens`
(nicht getestet; das D8-Raster auf 1 m braucht ~4x Speicher und Zeit).

Laufzeit 2 m: ~10 s Ganze-Welt-Raster (einmal, dann Cache), danach ~5 s für alle Fälle. Deterministisch (sortierte
Eingaben, keine Zufallszahlen).

## Was je Fall gerechnet wird

1. **Lippe → D8-Zelle**: größte Akkumulation im Radius 6 m, nicht tiefer als Gelände an der Lippe − 1,5 m.
2. **Einzugsgebiet** (m²) = D8-Akkumulation dort; **mittlerer Abfluss** = Summe über das Einzugsgebiet von
   Niederschlag × Abflussbeiwert je Biom (+15 % Nebel in Wald-/Inselbiomen über 120 m), siehe `wasserherkunft_regeln.json`.
3. **Bedarf** aus der Fallbreite nach Poleni (`q = 2/3·μ·√(2g)·h^1,5`, μ = 0,6, Überfallhöhe h = 2 cm für einen
   geschlossenen Vorhang, 5 mm für einen Schleier) → **V = Abfluss / Bedarf**.
4. **Wasser oberhalb** (m): Bogenlänge des Gewässers bis zur Lippe (fluss_sim-Spline), sonst Sehens-Bach bis zur Kante.
   Ebenso die **Welt-Wasserfläche** (`wasser_2m` > 0) entlang der Tiefenlinie aufwärts; es zählt das Längere.
   Dazu **längster Fließweg im Gelände**, **Gipfel über der Lippe** (höchster Punkt des Einzugsgebiets),
   **Rinne** (Tiefenlinie 10–120 m oberhalb, Median-TPI ≤ −0,4 m), **Quellmerkmale** (See/Teich/Sehens-See ≥ 200 m²
   oder Schnee/Eis ≥ 2 000 m² im Einzugsgebiet, geplante Quelle `bach.quelle`, Gewässer beginnt an See/Topf),
   **Biom**, **Landmasse** (8-m-Raster, Hauptland = größte, sonst `INSEL_nn`).
5. **Bewertung**: Herkunft sichtbar = Quellmerkmal oder ≥ 30 m Wasser oberhalb (eine trockene Rinne zählt nicht).
   `plausibel` = Herkunft sichtbar und V ≥ 0,1; `aus_dem_nichts` = keine sichtbare Herkunft und V < 0,1, oder kein
   Quellmerkmal, V < 0,05 und < 150 m Wasser oberhalb; sonst `fragwuerdig`. Spielfaktor 10 in V (verdichtete Welt).
6. **Maßnahmen** (`massnahmen`, erste = Hauptmaßnahme) und für nicht plausible Fälle ohne Quellmerkmal
   **Vorschlagspunkte** (`oberlauf.punkte_cm`, ab dem Ende des vorhandenen Wassers): Tiefenlinie aufwärts bis die
   Einzugsfläche unter 1 500 m² fällt (`mulde`) oder vorhandenes Wasser erreicht ist (`anschluss_wasser`); ist die
   Tiefenlinie kürzer als 30 m, steilster Anstieg bis zum Kamm (`kamm`, `anstieg_max`). `wasser_reicht_bis_mulde` =
   das Wasser beginnt schon an der Quellmulde, ein Oberlauf hilft nicht (dann Menge: Schneefeld, Kar, verkleinern).

## Dateien

| Datei | Inhalt |
|---|---|
| `wasserherkunft.py` | Analyse, schreibt `faelle_herkunft.json` (+ `faelle_herkunft.png` mit `--bild`) |
| `wasserherkunft_regeln.json` | alle Zahlen (Niederschlag, Abflussbeiwert, Nebel, Poleni, Schwellen, Oberlauf, Insel) |
| `wasserherkunft_pruefen.py` | Vorschlag der Prüferregel „nachweisbare Herkunft“ (liest `faelle_herkunft.json`), nicht in Planer eingebaut |
