# Auftrag 15d / 13e – Fehler im 1-m-Lader: Biome um eine Kachel verschoben (dringend, eine Zeile)

Stand 11.10.2026, 20:05. Betrifft `antworten/skripte/sehens_lib/daten.py`, `lade_1m` (Biom aus `eigner.r8` + `welt.json["kacheln"]`),
also **alle Planer, die auf 1 m laufen**: A15-Gefälle und die 15 Sehens-Planer. Die 2-m-Daten (`biom_2m.png`) sind richtig.

## Befund

- `welt.json["kacheln"]` ist eine **Liste** mit 78 Einträgen `{"kennzahl": n, "rezept": …, "name": …}`. Die Kennzahl ist Listenindex + 1:
  Index 0 = Kennzahl 1 = K10_TUNDRA, Index 1 = Kennzahl 2 = K11_LAVAFELD und so weiter. `eigner.r8` enthält die **Kennzahl**, 0 steht für Weltgelände.
- `lade_1m` läuft mit `enumerate(kach)` über die Liste und setzt `lut[Index] = rezept`. Dadurch ist jedes Biom um eine Kachel verschoben:

  | eigner.r8 | richtig | 1-m-Lader heute |
  |---|---|---|
  | 0 (Weltgelände) | aue | **tundra** (Rezept von Index 0) |
  | 1 (K10_TUNDRA) | tundra | **lava** |
  | 2 (K11_LAVAFELD) | lava | wueste |
  | 78 (VULKAN_REGION, rezept None) | lava | **aue** (lut nie gesetzt) |

- **Beispiel C2 (A15-Pilot):** Der Lauf liegt in K10_TUNDRA (`biom_2m.png` = 3 = tundra an allen Punkten). Auf 1 m plante der Planer alle 16
  Stufen als **lava** (Basaltsäulen, Lavafels/Lavasand), in der Cloud als tundra.

## Korrektur (Vorschlag)

```python
for v in (kach.values() if isinstance(kach, dict) else kach):
    if not isinstance(v, dict):
        continue
    k = int(v.get("kennzahl", v.get("id", -1)))
    if not (0 <= k < 256):
        continue
    rz = str(v.get("rezept") or "").lower()
    lut[k] = BIOME.index(rz) if rz in BIOME else BIOME.index("lava")   # VULKAN_REGION ohne Rezept = lava (wie sehens_daten.py)
```

Danach ergibt `lade_1m` dieselben Biome wie `biom_2m.png` (Prüfvorschlag: 1-m-Biom auf 2 m ausdünnen und mit `biom_2m.png` vergleichen,
Abweichung 0 außerhalb der Kachelränder).

## Bitte

1. `daten.py` korrigieren und pushen, mit Commit-Hinweis.
2. Prüft, ob Sehens- oder A15-Ergebnisse von 1-m-Läufen in der Cloud abhängen. Laut 15b wurden dort 1-m-**Fenster** nur für die Höhen benutzt, die Biome kamen aus 2 m;
   dann ist bei euch nichts betroffen.
3. Lokal benutze ich bis dahin eine korrigierte Kopie. C2 rechne ich nach eurem Push neu. Die Felsnetze werden dann wieder tundra statt Basalt.
