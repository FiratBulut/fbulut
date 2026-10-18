# Auftrag 22b – Wasserpflanzen: Ergebnis T22-0, Pilot-Feld, Rückfragen

Stand 18.10.2026, 16:35 PC-Uhr. Bezug: Antwort 22 (41e3ca5). Lokal nur gerechnet, nichts im Editor geändert.

## 1. T22-0 (Referenzcode §7 wörtlich, Selbsttest Signatur 521ccd76eaca5822 zweimal gleich)

| Maß | Ergebnis | eure Erwartung |
|---|---|---|
| Verstöße | 12 979 von 67 990 (19,1 %) | 10 500–15 500 |
| Messweg > 5 / > 15 / > 50 m | 18 839 / 9 679 / 6 094 | ±1 % zum Befund 22 |
| Rest > 15 m nach Reparatur | 5,3 %, ohne lily 4,0 % | 2–4 % |
| Rest > 50 m nach Reparatur | 2,4 %, ohne lily 1,7 % | ≤ 2 % |

- Fallgruppen: Trockenbett 7 253 (6 903 ersetzen, 350 nur entfernen = B5-Binsen mit Hang > 35°, vom Referenzcode als „trockenbett“ gezählt),
  fern im Trockenen 4 047, zu tief 963 (davon 246 an der Shallow-Water-Simulation in C2), Sumpf-Zone 701, Hang 15.
- H5: nur 407 Verstöße statt 850–1 400, die Nassmaske hält 1 312 Binsen.
- Herkunft (über die Planer-Dateien zugeordnet): aue 7 189, welt_bewuchs 1 579, wueste_ergaenzung 1 500 = 79 % → stützt eure Altkarten-These.
- TWI trennt nass/trocken nicht (P20 nass 3,36, P90 trocken 6,51) → TWI-Zweig aus, wie von euch vorgesehen (mit 9,0 nur 32 Verstöße weniger).
- GT_Schilf-Faktor (nur berechnet): Dichte −42,7 % (eure Erwartung 35–55 %); Zellen ≥ 10 % und > 15 m vom Süßwasser 162 221 → 4 252.
- V1: In 40 Feldern weicht die alte `karte_wasser.r8` von der Wasser-Wahrheit ab (1,13 Mio. Zellen). Ohne neue Karte setzen die Planer die Pflanzen
  beim nächsten Lauf wieder.
- 1 169 Trockenbetten; keines erfüllt die berechenbaren „Wasser zurück“-Kriterien (D8-Einzugsfläche ohne Senkenfüllung, nur Feld + 64 m – nicht belastbar).
- SM_lily_01: Importquelle `SM_lily-of-the-valley_beech_forest_01_1.fbx`, Material `M_lily-of-the-valley_beech_forest_01`, Eltern `M_Grass` → Maiglöckchen.
  8 470 lily stehen in Wasserzellen. Bildprüfung im Editor steht noch aus.

## 2. Pilot-Feld

- **C4 erfüllt euer Abbruchkriterium:** 175 von 1 166 Verstößen (13,0 %) liegen in V0-Sperrflächen, alle an sichtbaren Houdini-Wassernetzen
  (`houdini_sichtbar`); nur nach dem Rechteck gezählt wären es 1,6 %. Außerdem 9 Entfernungen in Wasserzellen („zu tief“) und 15 im 6-m-Uferband
  (dort wegen Hang > 15°), wo eure Pilot-Kriterien 0 verlangen.
- **Entscheidung lokal (Projektleitung): Pilot in F6** (1 222 Einträge, V0 0 %, Kriterium-3-Fälle 0, euer Bildfall „F6 typisch“ dabei).
  Ablauf wie die v3-Reparatur: feste Kameras, sichern, entfernen mit Speicherbeleg, Neustart, neuer Zensus. Ersatz (Trockenbett-Bewuchs) als eigener,
  protokollierter Schritt danach.

## 3. Fragen

1. **Kriterium 3 gegen §4.1:** „zu tief“ soll laut §4.1 entfernt werden, die Pilot-Kriterien verlangen 0 Entfernungen in Wasserzellen. Und am Ufer
   greift die Hanggrenze (> 15°) im 6-m-Band. Was gilt?
2. **Houdini-Wassernetze (V0):** Sollen Pflanzen an sichtbaren Houdini-Wassernetzen wie an gebautem Wasser behandelt werden (= behalten), oder sind diese
   Netze selbst Altbestand, der ersetzt wird? (Rest-Netze laut Liste: 10 Wasserfälle bleiben, 15–18 Netze sollen weg.)
3. **„zu tief“ an der Shallow-Water-Simulation (246 in C2):** Wie in v3 auslassen (Überlauf der Simulation ist kein gebautes Wasser)?
4. **Trockenbett-Ersatz §6.2:** Für die Bettsohle im Standardbiom fehlt eine Gruppe (vorläufig Bettrand-Gruppe genommen, 1 Fall); „je 2“ abgerundet.
   Ausnahmeflächen „quelle“: wörtlich 39 Flächen; in weiteren 50 Flächen lägen 38 Verstöße. Passt das?
5. **V1:** Soll `karte_wasser.r8` jetzt aus der Wasser-Wahrheit neu geschrieben werden (damit die Planer nicht wieder an Altwasser setzen), und welche
   Planer-Ebenen müssen danach neu laufen?
6. **lily:** Bei Bestätigung als Maiglöckchen: 8 470 in Wasserzellen – über die normale v3-Regel („Pflanze im Wasser“) mitbehandeln?
