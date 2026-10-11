# Antwort zu Auftrag 15b – Korrektur nach dem 1-m-Test: Ufer am Kaskadennetz-Rand

Stand 11.10.2026. **Vorfassung mit dem Ergebnis für C2.** Die übrigen 18 Pilotläufe und der 2-m-Lauf über alle 161
Strecken folgen in der Endfassung.

## Kurzfazit

- **Ursache bestätigt.** Der Stempel senkte das Gelände genau an der Netzkante. Gründe in Abschnitt 2.
- **C2 ist korrigiert:** Auf den 1-m-Fenstern meldet der Prüfer **0 FEHLER**. Geprüft sind 63 Beckenpunkte (vorher 15)
  mit Ufer links und rechts sowie dem Bett.
- **Aufruf lokal:** wie bisher, der Planer zieht das Delta auf 1 m nach. Für Cloud-Tests gibt es neu
  `--hoehe1m-fenster DIR`.

## Ergebnis C2 auf 1 m

| Lauf | Fassung | Beckenpunkte | Ufer zu tief | Bett zu flach | FEHLER |
|---|---|---|---|---|---|
| F_ERLENBACH_1V_C2 | lokal, Stand ac4da85 (Befund 15b) | – | 6 Proben | 0 | ja |
| F_ERLENBACH_1V_C2 | Cloud, alter Planer, 1-m-Fenster | 15 | 15 | 0 | ja |
| F_ERLENBACH_1V_C2 | **Cloud, korrigiert, 1-m-Fenster** | **63** | **0** | **0** | **0** |

Die korrigierte Fassung von C2 hat 19 Stufen, 1 Netz + 2 River, 1 112 Instanzen, 46 Akteure und 18 Effekte. Es bleibt
1 WARNUNG: 6 Stufen ≥ 1 m ohne Niagara, weil die Grenze für gleichzeitige Effekte greift.

## Aufruf für Claude lokal (C2)

```
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis . --laeufe F_ERLENBACH_1V_C2
```

Der Commit-Hash steht in der Endfassung.
