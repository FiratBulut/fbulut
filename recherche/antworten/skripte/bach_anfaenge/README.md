# bach_anfaenge – Wie beginnt ein Bach? (Auftrag 19)

Bericht: [`../../19-bach-anfaenge-quellen.md`](../../19-bach-anfaenge-quellen.md).
Ergebnis (Vorschlagsdaten, nichts eingebaut, Exporter unverändert): [`../../bach_anfaenge/`](../../bach_anfaenge/).

| Datei | Inhalt |
|---|---|
| `bach_anfaenge_plan.py` | Plan je Anfang „aus dem Nichts“ (Klasse e), Kaskade K1, versickernde Enden, Verjüngung aller Anfänge, Instanzen (FORMAT §3), Neu-Backen-Liste, Bilder |
| `bach_anfaenge_regeln.json` | alle Zahlen: Profil (b0, L, Exponent, Tiefe), Entscheidungsbaum, Quellfassung je Typ, Netze, Einzelfälle, K1, Enden |
| `bach_anfaenge_pruefen.py` | Prüfer P1–P8 (Vollständigkeit, Punkte, Gefälle, Profil, Instanzen, Effekte, FORMAT §3, Neu-Backen) und Byte-Vergleich zweier Läufe |

## Aufruf

```
python -I recherche/antworten/skripte/bach_anfaenge/bach_anfaenge_plan.py --bild
python -I recherche/antworten/skripte/bach_anfaenge/bach_anfaenge_plan.py --bild --aus <tmp>/lauf2
python -I recherche/antworten/skripte/bach_anfaenge/bach_anfaenge_pruefen.py --vergleich <tmp>/lauf2
```

Lokal mit 1-m-Daten: `--daten1m export/unreal/welt` (nicht getestet). Eingaben siehe Kopf des Skripts; alle
Standardpfade liegen im Repo. Laufzeit 2 m: etwa 8 s mit Bildern. Deterministisch: Zufall aus
sha256(Seed, Gewässer, Rolle), feste Reihenfolgen, gerundete Werte. Das Skript löscht vor dem Schreiben nur seine eigenen
Ordner `instanzen/` und `bilder/` unter `--aus`.

## Anwendung der Spline-Änderungen

Punkte `[X, Y, Z, Breite, Tiefe, Tempo]` in cm bzw. cm/s, Punkt 0 oben, wie `baeche_alle.json`.

| Modus | neue Spline |
|---|---|
| `kopf_ersetzen` | `punkte + alt[alt_bis_index_exkl:]` |
| `anhaengen` | `alt + punkte` |
| `ende_ersetzen` | `alt[:alt_ab_index] + punkte` |
| `verjuengung_alle` | nur Breite/Tiefe/Tempo der genannten Indizes setzen |
