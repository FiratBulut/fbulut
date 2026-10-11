# Auftrag 14: Nature Water FX an unseren Wasserfällen und Bachstufen einplanen (11.10.2026, 16:10)

Ferat hat **Nature Water FX** gekauft (`/Game/NatureWaterFX/FX/`: `NS_Waterfall_Small/Medium/Large`, `NS_Impact_Small/Medium/Large`,
`NS_Stream_Small/Medium/Large`, `NS_Geyser_Small/Medium/Large`, `NS_Wake_*`, `NS_Fountain_1–5`). Er möchte, dass ihr die Effekte an unseren
Wasserfällen einplant; ich setze danach genau nach eurem Plan. Bis dahin lasse ich die Wasserfälle unverändert.

## Was heute steht (Daten `vorlagen/daten/wasser_fx/`, Bilder `bilder/wasser_fx/`)

- **2 große Fälle** (`wasserfaelle.json`): WF_K1 (B4, Westfall, Kante 263,4 m, Fall 56,9 m, Vorhang 14,9 m breit) und WF_K8 (H4, Elfenfall, Fall 53,9 m,
  16,6 m breit). Vorhang = eigenes Netz mit `M_EL_Wasserfall2` (Translucent, Parameter siehe `vorlagen/daten/material_parameter.json`), Becken =
  Epic-See, dazu 4 einfache Gischt-Akteure. Bilder `WASSER3_*`: Vorhänge sichtbar, Aufprall/Gischt schwach.
- **Bachstufen** (`stufen.json`, `stufen_fluss_teile.json`, `stufen_netze.json`): C2 F_ERLENBACH_1V_C2 mit 12 Stufen (10 Fälle 1,8–5,3 m, 2 Schnellen),
  in 11 Epic-Flussstücke geteilt (Lücke 1,26–2,95 m an jeder Kante); je Fall ein Vorhang-Netz + Schaumscheibe (`MI_EL_Stufenfall_Vorhang/_Schaum`,
  seit 16:04 ruhiger: Deckkraft 0,55/0,45, Schaum 0,45/0,55); H4 F_ELFENFLUSS_2_H4 mit 2 Schnellen (Schnellen-Haut ausgeblendet, wirkte wie Folie).
  Bilder `STUFEN1_*` sind VOR dem Ruhigstellen entstanden (weiße Kacheln) – genau das soll mit Effekten natürlich werden.
- Gischt-Orte der C2-Fälle: `stufen_netze.json` → `gischt_cm`.
- Recherche dazu: `antworten/12-recherche-wasser-gpu-schatten.md` Teil A (Translucent unter Wasser unsichtbar, Niagara nur nah: Cull 40–60 m,
  kein Schattenwurf, Sort Priority Vorhang 0 / Schaum 1 / Gischt 2).

## Bitte liefern (`antworten/14-wasser-fx.md` + `antworten/wasser_fx/plan.json`)

1. Je großem Fall und je Bachstufe: welche Systeme (Name), Ort (cm, Weltkoordinaten), Drehung (Quaternion oder Yaw), Skala, ggf. User-Parameter
   (sofern aus der Paketbeschreibung bekannt), Cull-Distanz; Lärm/Klang-Wunsch (City_Nature_Sounds hat Wasser-Klänge? sonst Liste).
2. Ob unsere Vorhang-Netze bleiben, ersetzt oder nur ergänzt werden sollen (NS_Waterfall_* vs. eigener Vorhang), und welche Materialwerte dann passen.
3. Optional: Geysir- und Quell-Orte aus euren Sehenswürdigkeiten (Der Atem, Blasloch, Blautopf, Warme Quelle …) im selben Format, damit ich alles in
   einem Durchgang setze. Format für Effekte wie `vorlagen/SEHENS_FORMAT.md` §6 (`typ: niagara`).
4. Budget: Niagara je Ort ≤ 3, Systeme GPU, kein Schatten; die Leistung im Editor muss bleiben.
