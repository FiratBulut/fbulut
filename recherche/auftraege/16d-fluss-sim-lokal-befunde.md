# Auftrag 16d – fluss_sim lokal: zwei Fehler im lokalen Modus, Bauwerkzeug fertig

Stand 12.10.2026, 18:40.

## Fehler im lokalen Modus von `fluss_sim_export.py`

1. **Archivordner werden mitgelesen:** Der Exporter nimmt jeden Unterordner von `--gefaelle` mit `plan.json`. Lokal lagen dort meine Archivkopien
   `F_ERLENBACH_1V_C2.alt_v1_gebaut`, `.alt_v2_gebaut`, `.alt_vor15b`, `.alt_vor15e`, `.alt_lava_biomfehler` → 2 952 der 3 512 Kollisionsobjekte
   stammten aus alten Plänen. Lokal behoben (Archivordner nach `gefaelle/_alt/` verschoben): jetzt **532 Objekte, alle aus `F_ERLENBACH_1V_C2`**
   (28 überspannt), 1 SWR-Einheit, 19 Fälle (6 mit Vorhang). Bitte im Exporter Ordner mit „.“ im Namen oder führendem „_“ überspringen.
   Achtung auch: `gefaelle/C2/plan.json` ist ein **Feld-Instanzplan** (Ausgabe von `a15_einbau.py` für den Setzer), kein Lauf – bitte nur Ordner mit
   Lauf-Plänen lesen (z. B. Schlüssel `wasser_koerper` vorhanden).
2. **Geländedeltas doppelt bei schon gebauten Plänen:** `gel.delta_hinzu(...)` (Zeile ~1512/1527) addiert die Deltas aller Pläne auf `hoehe.f32`.
   Lokal sind gebaute Pläne (C2 Version 3) schon in `welt/` eingestempelt → doppelt (Becken/Fälle bis −9,95 m zweimal). Bitte Option
   `--gebaut <lauf …>` bzw. Erkennung über `export/unreal/welt/sehens_einbau/A15_<lauf>/lauf.json` → `nachgezogen` enthält das Feld → dann kein Delta
   addieren. Bis dahin sind lokal z. B. die `lage`-Einstufungen (im Wasser / am Ufer) der C2-Objekte möglicherweise falsch.

## Lokal fertig

- Bauwerkzeug `ue_swr_bauen.py` (Editor): ein `WaterBodyRiver` je SWR-Einheit aus den Abschnittspunkten, eine SWR je Einheit (Auflösung nach Rechteck,
  Zelle 0,3 m, 256–2048), Hindernis-Akteur(e) mit ISM/HISM aus `wasser_kollision`, Einlaufen + Bake über Plugin 0.18, Spielweg WCBS mit
  `MI_EL_SWR_Klar`, Protokoll + Rückweg. Offline-Trockenlauf 96/96; im Editor kommt jetzt C2 (Auftrag 205), danach die Tests aus Teil 2 (206).
