# Auftrag 13g – Treppenbäche der Sehenswürdigkeiten im 14b/A15-Format ausgeben (river + kaskadennetz)

Stand 11.10.2026, 23:15. Danke für 13f. Ich teste den neuen Stand (9e180f5/c945f93) heute Nacht lokal auf 1 m. Vorher ein Formatwunsch, der sich aus 14b ergibt.

## Problem

Seit 13f ist jeder Bach eine Treppe mit Becken ≤ 3 % und ≥ 3 m und Stufen dazwischen (`sehens_lib/bach.py`). Das lokale Einbau-Werkzeug der Sehenswürdigkeiten
(`ue_sehens_wasser.py`, Format aus SEHENS_FORMAT/`wasser.json`) baut Bäche als Epic-River-Stücke, an Stufen geteilt.

Nach Befund 14b zeichnet Epic Water River-Stücke unter ca. 15 m Länge nicht zuverlässig: Die Becken bleiben trocken. Genau das ist C2 am 11.10. nachmittags passiert,
mit 11 Teilstücken.

Kurze Becken (3–15 m) zwischen Stufen würden also wieder trocken aussehen.

## Wunsch

Bäche mit Stufen (Fall ≥ 0,5 m) bitte zusätzlich im **gleichen `wasser_koerper`-Format wie A15** ausgeben (14b Abschnitt 4):
- `river` für Strecken ≥ 15 m außerhalb der Stufenstrecke;
- `kaskadennetz` für jede zusammenhängende Stufenstrecke (`mittellinie` [x, y, z, breite, tempo, fallanteil, schaum, abstand_bett], `knick`,
  `rand_ueberstand_m`, `vorhang_an_stufen`, Überlappung 0,5 m, Netz dort 2 cm unter dem River);
- River-Stücke < 15 m gehen als Rampe ins Netz, so wie in A15 seit 15c;
- Effekte an den Stufen nach A15 2.9 (Niagara-Grenzen wie dort).

Am besten je Ort in `orte.json` beim Bach ein Feld `wasser_koerper` mit genau dieser Liste und einer Lauf-ID wie `SW_<ortid>_<bachid>`. Lokal baue ich das dann mit dem
fertigen A15-Werkzeug (`a15_einbau.py` → Kaskadennetz-Netz, Material `MI_EL_Kaskade_SLW`, `ue_gefaelle_wasser.py`). Das erprobe ich heute Nacht an C2 im Editor.
So gibt es nur noch **einen** Weg für gestuftes Wasser.

Seen, Teiche und große Wasserfälle bleiben wie bisher (Lake, Vorhang, Niagara).

## Sonst

- Der laufende lokale Pilot (bergwald B5) rechnet noch mit dem Stand vor 13f, damit der Einbau im Editor erprobt wird. Danach stelle ich auf 13f um.
- Bitte die Antwort wieder mit Commit-Hinweis.
