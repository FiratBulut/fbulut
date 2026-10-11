# Antwort Auftrag 15d / 13e – Biom-Fehler im 1-m-Lader

Stand 11.10.2026. Der Fehler ist in `skripte/sehens_lib/daten.py` behoben; Commit-Hinweis siehe unten (Commit „Auftrag 15d: 1-m-Lader …“).

## Kurzfazit

- **Befund bestätigt.** `lade_1m` hat `welt.json["kacheln"]` (Liste) mit `enumerate` gelesen. Dadurch wurde der **Listenindex** statt der **Kennzahl**
  als Schlüssel genommen, und jedes Biom war um eine Kachel verschoben.
- **Korrektur:** Schlüssel ist jetzt immer das Feld `kennzahl` (ersatzweise `id`). Fehlt beides, gilt bei einer Liste Index + 1, bei einem Dict der Schlüssel.
  - Kennzahl 0 = Weltgelände = aue.
  - Eine Kachel ohne bekanntes Rezept (z. B. VULKAN_REGION, `rezept: null`) wird lava, wie in `sehens_daten.py`.
- **Cloud-Ergebnisse sind nicht betroffen.** Alle Läufe hier (15 Sehens-Planer, A15 inklusive 15b/15c) liefen auf `--daten2m`; das Biom kam aus
  `biom_2m.png`. Die 1-m-Fenster aus 15b haben nur die Höhen ersetzt. Die echte 1-m-Welt (`export/unreal/welt`) gibt es nur lokal.
- **Lokal:** C2 und alle 1-m-Läufe der Sehens-Planer bitte mit dem neuen Stand neu rechnen. C2 bekommt dann wieder Tundra-Fels statt Basalt.
- `sehens_lib/selbsttest.py` läuft durch. Der Selbsttest nutzt eine synthetische `welt.json` mit Feld `kennzahl`, das Verhalten dort ist unverändert.

## Geänderter Code (`lade_1m`)

```python
lut = np.zeros(256, np.uint8)  # 0 = aue (Weltgelaende)
kach = wj.get("kacheln", {})
if isinstance(kach, dict):
    items = [(k, v) for k, v in kach.items()]
else:
    items = [(i + 1, v) for i, v in enumerate(kach)]       # Kennzahl = Index + 1, falls das Feld fehlt
for k, v in items:
    if not isinstance(v, dict):
        continue
    try:
        k = int(v.get("kennzahl", v.get("id", k)))           # die Kennzahl aus dem Eintrag hat Vorrang
    except (TypeError, ValueError):
        continue
    if not (0 < k < 256):
        continue
    rz = str(v.get("rezept") or "").lower()
    lut[k] = BIOME.index(rz) if rz in BIOME else BIOME.index("lava")   # ohne Rezept (VULKAN_REGION) = lava
```

## Prüfvorschlag lokal

1-m-Biom aus `lade_1m` auf 2 m ausdünnen (jede zweite Zelle) und mit `biom_2m.png` vergleichen. Außerhalb von Kachelrändern muss die Abweichung 0 sein.

## Nebenbefund: Planer aus Auftrag 11

Die Verteilungsplaner aus Auftrag 11 haben den Index-Fehler **nicht**: Sie lesen alle das Feld `kennzahl` (geprüft).
Dazu gehören `aue_plan.py`, `lava_plan.py`, `sumpf_plan.py`, `dschungel_plan.py`, `elfenwald_plan.py`, `heide_tundra_plan.py`, `hochgebirge_plan.py`,
`wueste_ergaenzung_plan.py`, `felsgruppen_plan.py`, `nordkueste_plan.py`, `mittelschicht_plan.py` und `spuren_plan.py`.

**Unterschied:** Mehrere dieser Planer ordnen eine Kachel **ohne Rezept** der aue zu. Lava wird sie dort nur, wenn das Rezept „vulkan“ oder „lava“ enthält.
Damit wäre VULKAN_REGION (Kennzahl 78, `rezept: null`) dort aue, nicht lava. Falls VULKAN_REGION wirklich lava sein soll, muss jeder
Rezept-Zuordner auch den Kachel-`name` prüfen, z. B. „VULKAN“ im Namen → lava. **Rückfrage:** Soll ich das in den Auftrag-11-Planern nachziehen?
