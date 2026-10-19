# Auftrag 22f – T22-F6-2 Ersatz r004 (nachgeprüft, noch nicht gesetzt), lily-Nachrunde komplett, Rückfragen vor dem Setzen

Stand 19.10.2026, 04:20 PC-Uhr. Bezug: Antwort 22e (3c99edc) §2–§7, Regeln 23.5 (lokal `regeln_23e_d5cc8d04`).

## 1. lily-Nachrunde: komplett (22e §6)

Ablauf je Feld: eingefrorener Stand → zaehlen → entfernen mit Speicherbeleg je Paket → Neustart → Zensus → Abgleich.
Revision r006b, Klassen-Korrektur lily an.

| Feld | entfernt | aus der Auswahl | außerhalb | hinzugekommen |
|---|---:|---:|---:|---:|
| H5 | 1 553 | 1 553 | 0 | 0 |
| I5 | 100 | 100 | 0 | 0 |
| G5 | 25 | 25 | 0 | 0 |
| H6 | 14 | 14 | 0 | 0 |
| I7 / C5 / G6 | 2 / 1 / 1 | alle | 0 | 0 |
| E5 | 318 | 318 | 0 | 0 |
| E6 | 2 | 2 | 0 | 0 |
| **Summe** | **2 016** | **2 016** | **0** | **0** |

- Davon sind 1 920 lily.
- E5 enthält 94 Landpflanzen im jetzt gebauten Bach Q_bach_E6_K2 (darunter 11 Bäume und 9 Büsche); E6 enthält 2.
- **Eine Abweichung von 22e §6:** In H5 gab es nur die Draufsicht-Stichprobe (19/20 klar im Wasser, 1 Grenzfall nasse Wiese/Flachwasser). Die
  zusätzlich verlangte Schrägsicht aus 1,5–2 m fehlte. Eure Antwort kam an, nachdem der Lauf schon gestartet war.
- Rückweg je Feld: die Sicherung `sicherung_<Feld>_v3_entfernt_<Zeit>.txt`.
- Bitte sagt, ob die Schrägsicht nachträglich an 20 Orten (ohne Pflanze, nur der Untergrund) nötig ist.

## 2. T22-F6-2 Schritt 1: verdeckte Ansichten

12 Kameras (je 2 je Ort), 170 cm über Grund, 45° nach unten, außerhalb der Stämme. Kette speichert nichts. Bild:
`bilder/platzierung/pilot_f6/t22f62_verdeckt_12.jpg`; der rote Kreis markiert den Ort der entfernten Pflanze.

| Ort | Befund (selbst angesehen) | stand die entfernte Pflanze sichtbar richtig? |
|---|---|---|
| sp_07 | trockener Sand-/Erdboden unter der Weide, kein Wasser | nein |
| sp_11 | trockener Riss-Schlamm | nein |
| sp_22 | trockener Riss-Schlamm, daneben Geröll; r003-Trockengras in der Mitte | nein |
| sp_29 | dichtes Röhricht mit behaltenen Rohrkolben, Farn; Boden nicht sichtbar, kein Wasser sichtbar | **Grenzfall** |
| sp_34 | trockener Riss-Schlamm | nein |
| sp_39 | trockener Riss-Schlamm (bei `_a` hängt ein Weidenzweig ins Bild, die Mitte ist frei) | nein |

**Kriterium 5 jetzt mit 20/20 beurteilt:** 19 entfernte standen sichtbar falsch, 1 ist ein Grenzfall (sp_29). Der Abbruch (≥ 2 von 20) ist nicht
ausgelöst. Ob sp_29 zählt, bitte bewerten: Der Ort liegt im Röhricht, dessen übrige Rohrkolben nach der Mulden-Regel `ok_feucht` stehen bleiben.

## 3. Ersatz r004 (Rolle 4, unabhängig nachgeprüft: „freigegeben mit Bedingungen“; noch NICHT gesetzt)

Von den 926 r003-Teilen bleiben **295**. Gestrichen werden 631, angehoben wird 1, neu gesetzt nichts.

| Klasse | r003 | r004 | gestrichen (Hauptgründe) |
|---|---:|---:|---|
| Trockengras | 407 | 200 | 207 (Meer 175, bewachsen 52, 20 mit beiden Gründen) |
| Äste | 160 | 81 | 79 (Meer 63, bewachsen 23) |
| Schachtelhalm | 17 | 13 | 4 (Meer) |
| Kieselhaufen | 342 | 1 | 341 (339 außerhalb der Sohle) |

- **Kahl-Kalibrierung:** Messung A trennt nicht. Die grüne Wiese ist Landschaftsgras, also keine Mittelschicht-Instanzen; A = 0 an allen
  Kalibrierorten. Messung B trennt klar: Gras-Lagen 0,89–0,97 (bewachsen) gegen 0 (kahl).
- Angewendet ist kahl ⇔ K ≥ 0,5075 und G < 0,4448 (Mitte zwischen den Gruppen).
- An sp_04/06/08/15 sind alle Matten gestrichen; bei gras4/gras5/fix_1 bleiben sie.
- **sp_31 geklärt:** Die behaltene ToadRush_02 steht unverändert. Im Umkreis von 3 m wurden 14 Rohrkolben entfernt; das erklärt den Bildunterschied.
  Rasterwerte: nass 0,36, Mulde 0,80 m, d_alt 6,0 m. `ok_feucht` folgt schon aus der Mulde.

## 4. Fragen (vor dem Setzen; jede Änderung am Plan wird eine neue Revision mit Nachprüfung)

1. **Kiesel-Lage:** 22e §3 sagt in der Regel-Tabelle „nur in der Bettsohle (d_alt = 0) und an Innenkurven“, im Abschnitt „Bestand“ aber „gelöscht
   nur, wenn außerhalb der Sohle **auf Riss-Schlamm**“. Der Erfolg nennt „342 Haufen mit 10–20 %“.
   - r004 setzt die Tabelle um: 3 Haufen in der Sohle, davon 2 im 15-m-Meerabstand, es bleibt **1**.
   - Wörtlich nach „Bestand“ (Riss-Schlamm = Lehm ≥ 0,5) wären es 67 angehobene Haufen und insgesamt 361 Teile.
   - Innenkurven sind nicht umgesetzt (keine Kurvenerkennung).
   - Was gilt?
2. **Kahl-Lagen:** 22e §4 B nennt „Schlamm + Lehm + Kies (+ Riss-Lage)“. r004 zählt alle unbewachsenen Lagen (zusätzlich Geröll, Erde, Sand, Fels,
   Felsplatte, Sandstein). Wörtlich würden **114** Teile mehr fallen (Trockengras 74, Äste 33, Schachtelhalm 6, Kiesel 1), alle auf Geröll,
   also auf kahlem Steinbett. Gilt Geröll als kahl?
3. **Schwellen B:** 22e nennt fest K ≥ 0,5 und G < 0,3. r004 nimmt die Mitte der Kalibriergruppen (K ≥ 0,5075, G < 0,4448), wie es Messung A
   verlangt. Mit G < 0,3 fielen 23 Teile mehr (16 Trockengras, 7 Äste). Laut Nachprüfer liegen 11 davon in den Bildern sp_05/sp_13 auf Geröll,
   nicht auf Wiese. Mitte oder fest?
4. **Meer-Regel:** „≤ 15 m von Meer-Wasserzellen kein Ersatz“ trifft 392 der 926 Teile, 217 nur deshalb.
   - Die meisten liegen auf Geröll (226) und Erde (69), nur 39 auf Sand.
   - Es sind Trockenbetten an Flussmündungen, nicht der Strand.
   - Ohne die Regel wären es 512 Teile. Soll die Regel nur für Strand (Sand-Lage) gelten?
5. **Haufenhöhe:** Ihr nennt für `SM_SmallStonesPack_01` 0,26 × 0,18 × 0,16 m. Unsere Punktwolke aus dem Editor (Nanite-Ersatznetz, Skala 1) ergibt
   13,1 × 9,2 × 8,3 cm. r004 rechnet mit 8,3 cm. Woher stammen eure Maße (Skala 2 im alten Planer?)?
6. **Nassmaske Lehm:** Die Riss-Schlamm-Lage `Lehm` zählt in der Nassmaske mit Gewicht 0,4 als nass (sp_31: nass 0,36 nur aus Lehm). Trockener
   Riss-Schlamm ist aber gerade das Zeichen für „trocken“. Soll Lehm aus der Nassmaske?
7. **Weitere SmallStonesPack-Netze:** Die Punktwolken enthalten keine Dreiecke, die Inselzahl lässt sich daraus nicht bestimmen.
   - `_08` bis `_14` haben dieselbe Form wie `_01` bis `_07`; `_08` und `_10` gelten damit wie `_01`/`_03` als Haufen.
   - `_02` und `_04` bis `_07` brauchen eine Nahaufnahme.
   - Dreiecks-Export wird gerade gebaut (T23e-3).

## Dateien (lokal)

`docs/pruefung/platzierung/wasserpflanzen22/ersatz_F6/r004/` (lieferung.md, SHA256SUMS, kahl_kalibrierung_r004.json, sp31_klaerung_r004.json);
Nachprüfung `docs/pruefung/nachpruefung/ersatz_trockenbett22/nachpruefung_r004.md`; lily: `docs/pruefung/platzierung/auftrag.md`.
