# Auftrag 22h/23j – Stand: F6 r005c eingebaut (22g §4), Talkaskade gesetzt + Bodenlagen nachgezogen; Fragen zum nächsten Schritt

Stand 19.10.2026 16:50. Bezug: Antworten 22g (05933d7) §4/§6, 23i (05933d7) §5/§6.
Bilder: `bilder/platzierung/f6_r005c_rueckhol.jpg` (links r005b, rechts r005c, Kameras z402/z430/z443),
`bilder/platzierung/talkaskade_freilagen_T23FL.jpg` (Talkaskade C2, 5 Kameras, links vor, rechts nach den Bodenlagen).

## 1. F6 – r005c (22g §4) eingebaut und bestätigt

- **r005c:** r005b minus die 7 Teile der Ersatzgruppen an den Rückhol-Orten 402, 412, 424 und 425 (6 Trockengras, 1 Ast). Damit sind alle 9 Gruppen mit
  eigenem Ersatz ganz gestrichen, keine fremde Gruppe ist betroffen.
- Gesetzt mit dem vorhandenen Setzer (Plan neu: 447). 5 IFA-Pakete gespeichert, jedes mit Speicherbeleg.
- **Nach Neustart bestätigt:**
  - Zensus 36 960 → 36 953.
  - pilot_zensus_diff: entfernt 7, alle aus der Auswahl, außerhalb 0, hinzugekommen 0.
  - 447/447 transformgleich.
  - Rückholung 37/37 transformgleich.
- Abnahme 22g §4: Gruppen gleich, Simulation F6 170 / 0 Verstöße (offline), 3 Bilder an Rückhol-Orten ohne Doppelung (z402: die Trockengras-Scheibe der Gruppe
  ist weg).
- **Welle 1:** Die Werkzeug-Revision r008 mit 22.3 (Toleranz, Sumpf-Vorrang, Reihenfolge §3) ist im Bau. Danach folgen eine unabhängige Nachprüfung
  mit den Selbsttest-Fällen §5, ein Pilotfeld und dann der Rest.

## 2. Talkaskade C2 – Plan 23f gesetzt, Bodenlagen an den frei gewordenen Stellen

- **23f gesetzt** (Ferat-Freigabe 12:55):
  - `p2bett_talkaskade` 645 → 627, `detailgrad` 7 659 → 6 511.
  - 2 047 schräge Platten bzw. Kleinschutt an Land ersatzlos entfernt.
  - Platten im und am Wasser bleiben bis zum 16h-Bettschritt.
- **Bodenlagen nachgezogen** (nur Lagen, keine Höhen):
  - 777 m² frei gewordene Fläche = Grundriss alter Teile ohne neuen Partner.
  - Ausgeschlossen: nass nach Dump T6N1b_2, Bettzellen, Wege, Hang > 38°.
  - Kern: Geröll 20 → 38 %, Moos 25 → 12 %, Gras-Lagen 17,5 → 10,9 %. Kies bleibt bei 20 % (Displacement seit V18c 11,2 cm).
  - Rand 1–2 m weich auslaufend.
  - Wirkung im Bild: vor allem s415 (Rasen → Geröllboden), sonst fein.
- **V18c global** (23g): Kies-Hub 31,5 → 11,2 cm, die Streifen sind weg. Fels-Hub (V18d) ist in Arbeit.

## 3. Ferat 14:10 – schwebende Felsen/Blumen

Ferat zeigte schwebende Felsen und Blumen im Bild `V18Q1_streifen_C2_nah_sonne`. Seine Vorgabe: „nie einzeln korrigieren, sondern Ursache finden und
prozedural korrigieren“. Ursachensuche und Weltzählung laufen lokal. Bericht folgt mit eigenem Auftrag.

## Fragen

1. **Hang-Blöcke (23i §4):** Ist der Neulauf Planer C2 nach 23.10/23.11 jetzt der richtige nächste Schritt? Oder soll zuerst die Weltreparatur
   „schwebend“ (Abschnitt 3) laufen, weil beide dieselben Altstücke betreffen?
2. **Bodenlagen-Stärke:** Reicht die Mischung im Kern (Geröll 38 / Kies 20 / Erde 12 / Moos 12)? Oder lieber stärker, z. B. Geröll 50 und Gras-Lagen ≤ 5 %?
   Die Wirkung ist an 4 von 5 Kameras fein.
3. **Gespiegelte Foliage (23i §2):** Wir zählen weltweit und bauen ein Umstell-Werkzeug (Vorzeichen +, Yaw + 180°, Sitzprüfung, Pilot in einem Feld).
   Gilt das auch für Gras/Pflanzen-Foliage oder nur für Steine/Totholz/Bäume?
