# Auftrag 22g – Regel 22.3 Zwergbinse umgesetzt (r007), Rückholung F6 vorbereitet (37), drei Auslegungsfragen

Stand 19.10.2026, 12:10 PC-Uhr. Bezug: Antworten 22f (fdd7f1a) und 22f-2 (1868e8f). Rolle 4 offline, unabhängig nachgeprüft: „freigegeben mit Bedingungen“.
Im Editor ist noch nichts gesetzt; der Einbau folgt nach dem Testlevel-Lauf T23b-S.

## 1. Ergebnisse

- **Zählung F6 (22f-2 §3.1):** In der F6-Sicherung stehen 157 ToadRush. 37 davon liegen auf Lehm + Schlamm ≥ 0,5 bei Hang ≤ 8°:
  - 25 × `_00`, 12 × `_02`;
  - Lehm 0,51–1,00, Schlamm 0, Hang 0,2–5,4°, alle am Altbett;
  - auf Wiese (Gras ≥ 0,45) 0 von 37. Die Abbruchregel greift nicht.
- **r007:** Klasse `zwergbinse`, abschaltbar. Mit abgeschalteter Klasse ist das Ergebnis byte-gleich zu r006b; Rohrkolben und lily bleiben unverändert.
- **r005b** = r005 minus 29 Ersatzteile (22 Trockengras, 7 Äste) ≤ 0,5 m von Rückhol-Orten, also **454 Teile**. Nach Rückholung und Ersatz hat F6
  (Simulation) 170 Wasserpflanzen und 0 Verstöße.
- **Lehm-Prüfung T22-L0:** Lehm-Gewicht 0 statt 0,4 ändert weltweit nur 1 Urteil (F6:7557, eine ToadRush). Die Regel „≥ 8 von 10 Draufsichten“ lässt
  sich damit nicht anwenden. Für Rohrkolben ändert Lehm 0 nichts.

## 2. T22 weltweit mit Regel 22.3

| | Verstöße |
|---|---:|
| r006b (22.2) | 9 333 |
| r007 (22.3) | 9 617 |
| davon neu `zu_tief` (ToadRush) | 232 |
| davon neu Sumpf-ToadRush auf Wiese fern vom Wasser ohne Mulde | 52 (H5 34, H4 9, I5 9) |

Kein heute bestehender Verstoß wird ok; außerhalb der ToadRush ändert sich nichts.

## 3. Fragen

1. **Tiefe:** 22f-2 sagt „im Wasser, Tiefe > 0,10 m = Verstoß zu_tief“. r007 hat das mit der Toleranz aus 22b §1.2 umgesetzt: Verstoß erst ab 0,30 m bei
   sicherem Spiegel, dazwischen nur Hinweis. Daraus kommen die 232. Wörtlich gelesen kämen weltweit **1 647** Verstöße dazu (H5 allein 1 069), in F6 keiner.
   Welche Lesart gilt?
2. **Sumpf:** Die 52 neuen Verstöße liegen in Sumpfgebieten (H5, H4, I5). Bisher hielt die Nassmaske sie fest. Soll die Wiesen-Regel im Sumpf gelten, oder
   hat der Sumpfplaner (Bulten, Nasswiese) dort Vorrang?
3. **Reihenfolge:** Wird „Schlammboden ok“ vor der Wiesen-Regel geprüft? Heute betrifft das 0 Fälle (in H4 zwei mit Gras ≥ 0,45, beide ≤ 15 m vom Wasser).
4. **Gruppen-Rest:** 14 r005b-Teile bleiben 51–70 cm neben Rückhol-Orten stehen, 7 davon aus der Ersatzgruppe genau dieses Orts. 22f-2 streicht nach
   Abstand (≤ 0,5 m), nicht nach Gruppe. Soll die ganze Ersatzgruppe eines Rückhol-Orts fallen?
5. **Welle 1:** Mit 22.3 braucht das Editor-Reparaturwerkzeug eine eigene Revision (heute nur Regelversion 22.2). Wir bauen sie nach eurer Antwort; F6
   braucht sie nicht.
