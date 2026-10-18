# Auftrag 22 – Wasserpflanzen fern vom Wasser: Regeln für Prüfung und Reparatur

Stand 18.10.2026, 13:35 PC-Uhr. Anlass: Ferat sieht „immer wieder Assets, die komisch platziert sind“. Die laufende Platzierungsprüfung v3 repariert
Bäume, Büsche, Pflanzen und Gras im Wasser, Bäume und Büsche auf Wegen und überlappende Bäume. Wasserpflanzen sind davon ausgenommen. Eine
Zählung zeigt jetzt das umgekehrte Problem: Wasserpflanzen stehen weit weg von jedem Wasser.

## 1. Zahlen (Zensus aller 70 Felder, 18.10. 08:28; Wasser = gebaute Gewässer laut abgeglichener Wasser-Wahrheit)

Klasse „wasserpflanze“ = Netznamen mit reed|rush|schilf|binse|lily (nicht lilyofthevalley)|seerose|rohrkolben|alge|cattail|lotus|nymph|waterplant|duckweed
(24 Netze, darunter `SM_Rohrkolben_Horst_1..6`, `SM_Rohrkolben_Jung_1..3`, `SM_ToadRush_*`, `SM_WaterPlant01–04`, `SM_lily_01_1/_2`).

| Maß | Anzahl | Anteil |
|---|---:|---:|
| Wasserpflanzen gesamt | 67 990 | |
| in einer Wasserzelle | 37 327 | 54,9 % |
| > 5 m vom Wasser | 18 839 | 27,7 % |
| > 15 m | 9 680 | 14,2 % |
| > 50 m | 6 095 | 9,0 % |
| Boden > 1 m über dem nächsten Spiegel | 8 402 | 12,4 % |
| Boden > 3 m über dem nächsten Spiegel | 3 460 | 5,1 % |
| auf einem Weg | 3 | |

- 80 % der Fälle > 15 m liegen in 10 Feldern: H5 2 151, H4 1 072, D6 838, C4 724, F6 693, E5 659, F5 456, D4 432, B5 356 (alle > 50 m), G5 348.
- Betroffen sind vor allem Binsen (`ToadRush_00/_02/_010`: 24–28 % > 15 m) und alle Rohrkolben (16–22 %). `SM_WaterPlant01–04` stehen alle im Wasser.
- 40 % der Fälle > 15 m stehen ≤ 5 m an Wasser einer alten Karte (Gewässer, die später ersetzt oder entfernt wurden); von allen Wasserpflanzen
  sind es 23 %. H5 (Sumpf-Zone, 2 147 ohne jedes Wasser in der Nähe) hat vermutlich eine andere Ursache: Biom-Zone statt Wasserzelle.
- Dazu kommt Landschaftsgras `GT_Schilf` (Netze `SM_Rohrkolben_Horst_*`, Dichte aus der Bewuchskarte `v_schilf`, 2-m-Raster): von 514 129 Zellen mit
  Dichte ≥ 10 % liegen 54 % > 5 m und 27 % > 15 m vom Wasser (H5 90 544, I5 22 859, F5 13 982 Zellen > 15 m).

## 2. Bilder (Repo `bilder/platzierung/`)

- `wasserpflanzen_fern_2026-10-18.jpg`: die 10 weitesten Fälle (346–621 m vom Wasser) + 2 Kontrollen in D5.
  - C4, D4, D6, E6: große Rohrkolben-Horste im trockenen Steppengras, auf Geröll und am Fuß roter Canyonwände.
  - B5: Binsen über steile Felsflächen verteilt (Klippenzone).
  - D5 (Kontrolle): Rohrkolben am Flussufer neben einer Brücke – richtig platziert.
- `wasserpflanzen_typisch_2026-10-18.jpg`: 9 typische Fälle 20–40 m vom Wasser.
  - C4 und F6: Rohrkolben am Rand ausgetrockneter Bachbetten (dunkler Schlamm, rissiger Boden ohne Wasser) – Reste alter Gewässer.
  - E5: im Bild ist Wasser zu sehen, das die Wasser-Wahrheit nicht als gebaut führt. Prüfen wir lokal.
  - H4/D4: Rohrkolben im Waldboden. H5: Binsen in einer Wiese der Sumpf-Zone.

## 3. Fragen

1. **Regel je Pflanzenart:** Wie weit dürfen Rohrkolben, Binsen (`ToadRush`), Seerosen, `WaterPlant` vom Wasser stehen (horizontal) und wie hoch
   über dem Spiegel? Binsen wachsen auch auf nassen Wiesen – gilt für sie eine andere Grenze oder eine Feuchte-Bedingung (z. B. Mulde, Senke)?
2. **Biome:** Gilt in der Sumpf-Zone (H5, Teile I5) eine Ausnahme? Welche Wasserpflanzen sind in Wüste/Canyon (C4, D4, D6, E6) überhaupt plausibel?
3. **Ausgetrocknete Bachbetten** (alte Gewässer, heute trocken, oft dunkle Schlamm-/Risstextur): Wasserpflanzen dort entfernen, durch
   Trockenbett-Bewuchs ersetzen, oder ist „Trockenbach mit Rohrkolben“ an manchen Stellen plausibel? Soll stattdessen eher Wasser zurück?
4. **`GT_Schilf` (Landschaftsgras über Dichtekarte):** Regel zum Ausdünnen der Dichte nach Abstand zum Wasser (Abstand, Übergangsbreite), Ausnahmen?
5. **`SM_lily_01_1/_2`** (Forest-Set, 0,3 m hoch, im Projekt als Seerose gedacht, 54,9 % aller Wasserpflanzen stehen in Wasserzellen – ohne lily
   ändert sich die Aussage nicht): Ist das eine Wasserpflanze oder eine Landlilie?
6. **Reparaturform:** Entfernen wie bei der v3-Reparatur (gesichert, rücknehmbar), oder versetzen an die nächste Uferlinie?

Bitte Regeln als Tabelle (Art × Biom → Grenzen) und eine Entscheidungsfolge für die drei Fallgruppen (fern im Trockenen, am Trockenbett,
Sumpf-Zone). Lokal setzen wir das als neue Prüfklasse in v3 um (Pilot, Belege, Nachprüfung wie gehabt).
