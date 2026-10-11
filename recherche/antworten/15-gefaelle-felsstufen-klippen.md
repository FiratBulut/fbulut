# Antwort zu Auftrag 15 – Steile Fluss- und Bachstrecken: Felsstufen, Klippen, Wasserfälle (Kurzfassung)

Stand 11.10.2026. Die ausführliche Antwort steht in [`15-gefaelle.md`](15-gefaelle.md), das Regelwerk mit Quellen in
[`15-gefaelle-regelwerk.md`](15-gefaelle-regelwerk.md). Skripte und Format: [`skripte/gefaelle/README.md`](skripte/gefaelle/README.md).

## Kurzfazit

- **Steile Strecken werden zu Becken und Stufen statt Schrägen.** Becken haben ≤ 2 % Spiegelgefälle. Dazwischen
  liegen Blockstufen, Kaskaden und Fälle an Fels, dazu Kolke, Uferklippen und Klammen. Die Zahlen kommen aus
  `skripte/gefaelle/gefaelle_regeln.json`.
- **Prioritätenliste** aller 161 Strecken: [`gefaelle/prioritaet.json`](gefaelle/prioritaet.json).
  - Bewertet wird die Sicht vom Weg, die Nähe zu Sehenswürdigkeiten und deren Kameras sowie Fall und Gefälle.
  - Pilot sind die Top 20 mit C2 auf Rang 1.
  - 36 Strecken sind kaum planbar (vorher 76), meist weil sie kürzer als 40 m sind.
- **Planer** `skripte/gefaelle/gefaelle_plan.py`. Er schreibt je Lauf `plan.json` mit neuem Spiegel, Stufen, Gelände-Delta, Lagen,
  Instanzen und Akteuren, Effekten und Kameras `_vorher`/`_nachher`.
  - Das Wasser folgt 14b Variante A: River ober- und unterhalb, dazwischen ein Kaskadennetz, 0,5 m Überlappung.
  - Für C2 ersetzt dieser Plan die A14-Einträge.
- **Prüfer** `skripte/gefaelle/gefaelle_pruefen.py`, Testlauf auf 2 m:

  | Lauf | Läufe | Stufen | FEHLER | Anmerkung |
  |---|---|---|---|---|
  | 20 Piloten | 19 | 346 | 0 | zweiter Lauf identisch |
  | alle 161 Strecken | 98 mit Stufen | 1089 | 0 | |

  Testbilder liegen in `gefaelle/test_<strecke>.png`.
- **Lokal (1 m):** `python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis .`. Die einzelnen
  Schritte stehen in `15-gefaelle.md`, Abschnitt 5.
