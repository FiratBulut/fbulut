# Antwort zu Auftrag 14 – Nature Water FX an Wasserfällen und Bachstufen (Kurzfassung)

Stand 11.10.2026. Die ausführliche Antwort steht in [`14-wasser-fx.md`](14-wasser-fx.md), der maschinenlesbare Plan in
[`wasser_fx/plan.json`](wasser_fx/plan.json) (Format SEHENS_FORMAT §6, `typ: niagara`, plus `cull_m`, `sort_priority`,
`user_parameter`, `ziel`, `optional`, Blöcke `material`, `klang`, `sehens13`). Erzeugt wird er mit `wasser_fx/plan_erzeugen.py`,
geprüft mit `wasser_fx/plan_pruefen.py`: 291 OK, 0 Warnungen, 0 Fehler (Stand nach Auflösung des tundra_06-Konflikts).

## Kurzfazit

- **Vorhänge bleiben überall, Nature Water FX ergänzt nur.** Der Vorhang deckt die 1,3–3-m-Lücken der geteilten Flussstücke und
  trägt jenseits der Niagara-Cull-Distanz.
- **WF_K1 und WF_K8:** `NS_Waterfall_Large` (Lippe), `NS_Impact_Large` (Gischt) und `NS_Wake_Large` (Becken), je 3 Systeme. Cull
  150/100/60 m. Am Vorhang weniger und dunklerer Schaum.
- **C2 (12 Stufen):** 10 Systeme in 5 Gruppen mit je ≤ 3, abwechselnd Impact und Stream. `NS_Waterfall_Small` nur an S01 (Probe) und
  S07 (optional). Cull 30/45 m, an jedem Standort höchstens 6 Systeme gleichzeitig aktiv.
- **H4 (2 Schnellen):** je `NS_Stream_Medium`, optional `NS_Wake_Small`.
- **Weiße Kacheln:** Material statt Niagara. `MI_EL_Stufenfall_Vorhang` mit Deckkraft 0,5, `Schaum_Menge` 0,3, mehr Strähnen und
  Randdurchsicht, kein Schaumleuchten.
- **Klang:** `CUE_Water_Stream_I…X` an 11 Orten. Ein echtes Wasserfall-Tosen fehlt im Inventar.
- **Ungeprüft:** die Namen der User-Parameter, die Größe der Systeme bei Skala 1 und ihre lokale Fließachse. Die Prüfliste steht in
  14-wasser-fx.md §9.
- **Konflikt (erledigt):** `tundra_06_das_aufeis` (Auftrag 13) lag auf der C2-Kaskade; ersetzt durch `tundra_06_das_schneetaelchen`, siehe Nachtrag.
- Die Geysir- und Quellorte aus Auftrag 13 (Blasloch, Blautopf, Seefall u. a., 26 Orte) stehen nur zur Übersicht unter `sehens13`.
  Sie werden nicht doppelt gesetzt, weil die Sehenswürdigkeiten-Planer sie selbst liefern.

## Nachtrag Koordinator (Konflikt tundra_06) – erledigt

Entschieden: **Die C2-Kaskade hat Vorrang.** Für das Aufeis gab es in der Tundra keinen regelkonformen Ersatzstandort (unterhalb der Kaskade öffnet sich die Schlucht zur Ebene, die Straße ist 59–70 m entfernt). Deshalb wurde `tundra_06_das_aufeis` durch **`tundra_06_das_schneetaelchen`** ersetzt (Altschneefeld mit Blutschnee-Algen in einer Hangmulde, Feld E3, ~1,55 km von der Kaskade, ohne Niagara). `plan.json` ist neu erzeugt: kein Konflikt mehr, Prüfung 291 OK / 0 WARNUNG / 0 FEHLER.
