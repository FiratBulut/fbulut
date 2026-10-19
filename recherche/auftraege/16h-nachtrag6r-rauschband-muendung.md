# Nachtrag 16h-6r – Rauschband T6N1_2 gegen T6N1b_2 gemessen (6q §1/§2/§5); Tiefeneingang im Wassermaterial gefunden (6q §4)

Stand 19.10.2026, 09:20 PC-Uhr. Bezug: Antwort 16h-6q (1868e8f). Rolle 1 offline. Die Ergebnisse sind reproduzierbar: Zwei Läufe ergeben bitgleiche Ausgaben.
Feste Prüfeingabe: `rauschband_T6N1_2_T6N1b_2.json`, SHA `48422d87…`.

## 1. Kein Abbruch

- Die Enddumps sind nicht bitgleich: R weicht in 5 769 Texeln ab, G in 42 206.
- Die Startdumps `_0` sind bitgleich.
- SHA der Oberflächen: T6N1_2 `4b85a372…`, T6N1b_2 `d1e5f3f6…`.

## 2. Rauschband je Zone (Texel, die in beiden Dumps `sichtbar_1` sind)

| Zone | p95 \|ΔW\| | p99 \|ΔW\| | p95 \|ΔG\| | Wechsel `sichtbar_1` |
|---|---:|---:|---:|---:|
| Bergrinne (s 0–199) | 0 | 8 cm | 0,55 cm | 0,27 % |
| Talkaskade (s 390–578) | 0 | 2 cm | 0,33 cm | 0,10 % |
| Mündung (s 700–788) | 0,25 cm (= 1 Half-Float-Stufe) | 0,5 cm | 0,22 cm | 0,21 % |
| Rest | 0 | 0,25 cm | 0,06 cm | 0,06 % |

**Das Rauschband liegt auf der Rundungsstufe.** Eure Erwartung „an der Mündung deutlich darüber“ trifft nicht zu: Dort ist p95 genau eine Stufe.

## 3. Ursachenkarte Mündung (6q §2)

- **Auslass belegt:** Er liegt am unteren Rand der Rechenfläche zum C3 (Welt-Y −202 852,5 cm, X −173 127 … −171 845 cm). Die letzte nasse Zeile hat
  13–14 cm Wasser; der C3-Kopf liegt 1,6 m jenseits der Kante.
- **Hauptlauf = R1:**
  - Im Band 0–5 m vor dem Auslass weichen 55,6 % der Texel ab, ab 20 m nur noch 2–5 %.
  - Tiefe Texel weichen mit ab.
  - 520 von 612 Abweichungen haben dieselbe Richtung.
- **Ost-Arm-Fläche** (54 % der Zone): weder R1 noch sauber R2.
  - Dort weichen flächig 16–35 % der Texel ab, ohne Bezug zum Abstand oder zur Tiefe.
  - An Fronten ist der Anteil nur das 1,8-Fache.
- Eure Regel mit 1 cm Schwelle blieb „unklar“ (an der Mündung liegen nur 4 Texel über 1 cm). Rolle 1 hat deshalb nachträglich eine Regel in
  Half-Float-Stufen ergänzt; das steht offen im Bericht.
- **Folge laut euren Regeln:** Die letzten 20 m vor dem Auslass werden nicht mehr für Entscheidungen gemessen. An der Simulation ist nichts zu tun.

## 4. Einordnung T6N1_2 gegen T6M3A_2

- An der Mündung p95 2 cm; 27 % der Texel liegen über dem Rauschband. Das ist also mehr als Laufrauschen.
- **Eure Annahme in 6q §1 stimmt nicht:** T6M3A_2 lief laut `t6n1_auswerten.py` ebenfalls mit Breite 1. Der Unterschied ist also nicht die Breite.
  Die Ursache ist ungeprüft; die Eingaben beider Läufe unterscheiden sich vermutlich an anderer Stelle (Hindernisse, Spline-Stand vom 18.10.).

## 5. Sägezahnkante an der Mündung (6q §4)

- **Ein Tiefeneingang ist vorhanden.** Im Master `M_Eldarien_Wasser_Schaum8` hängt Epics `WaterOpacityMaskFromDepth`. Gesteuert wird er über
  `Water Opacity Mask Offset` (im Master −24). Laut Epic macht er flaches Wasser durchsichtig (Opacity/Specular 0, Refraction 1).
- **Ungeprüft:** ob die Maske in BAKED_SIM die gebackene Tiefe G sieht. `MI_EL_SWR_Klar` hat `UseBakedSim` = False.
- **Geplanter Test** (nur im Speicher, wie der Streifen-Test): `Water Opacity Mask Offset` an einer Kopie von MI_EL_SWR_Klar in 3 Stufen, Bilder an der
  Mündungskamera. Daneben `UseBakedSim` an/aus.

## 6. Fragen

1. **Befundschwelle:** Wo p95 = 0 ist, schlagen wir als Schwelle mindestens 1 Half-Float-Stufe der Zone vor. Einverstanden?
2. **Test Sägezahn:** Reicht der Offset-Test aus §5? Welche Stufen schlagt ihr vor? Gilt `UseBakedSim` = True als zulässiger Schalter, oder ändert er
   das gebackene Bild an anderer Stelle (Kolke, Klarheit)?
3. **T6N1_2 gegen T6M3A_2:** Lohnt es, die Ursache der 27 % zu klären, oder reicht K-Kolk als Tor, weil die Talkaskade im Band liegt?
