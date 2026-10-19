# Antwort 22g – r007 so annehmen: Tiefe mit Toleranz, Sumpf-Regel vor Wiesen-Regel, feste Prüfreihenfolge, ganze Ersatzgruppe fällt; Lehm bleibt 0,4

Gelesen: recherche/auftraege/22g-zwergbinse-r007-rueckfragen.md @ 61ff5a12a297d046dcaa26a0f399ff4c37864fcc (Commit a6d95ca)

Stand 19.10.2026. Bezug: Antworten 22b (3256039) §1.2, 22 (41e3ca5) §4.4, 22f (fdd7f1a), 22f-2 (1868e8f). Bearbeiter: Cloud-Recherche. Bereich: Regel 22.3,
Klasse `zwergbinse`, Pilot F6.

## Kurzfazit

1. **Tiefe – beantwortet:** Eure Lesart gilt. Die 0,10 m aus 22f-2 sind die Grenze, und dazu kommt die Toleranz aus 22b §1.2:
   - Verstoß erst über **0,30 m** bei sicherem Spiegel;
   - 0,10–0,30 m nur Hinweis.

   Die Spiegelunsicherheit von etwa 0,2 m ist dieselbe wie bei Rohrkolben. Wörtlich gelesen würden 1 647 Pflanzen nach einer Messung
   entfernt, die das nicht trägt. Die 232 neuen `zu_tief` bleiben (§1).
2. **Sumpf – beantwortet:** In der Sumpf-Zone gilt **22 §4.4 vor der Wiesen-Regel**. Unsere Tabelle in 22f-2 §1 hat den Sumpf-Zweig
   vergessen; das war unser Fehler. Binsen, und damit ToadRush, bleiben dort bei `feucht` (Nassmaske, Mulde oder TWI) und Hang ≤ 12° stehen.
   Die 52 neuen Verstöße in H5/H4/I5 entfallen dadurch (§2).
3. **Reihenfolge – beantwortet:** zuerst Wasser, dann alle „ok“-Standorte, zuletzt die Verstöße. Die Abfolge steht in §3.
4. **Gruppen-Rest – beantwortet:** Die **ganze Ersatzgruppe** eines Rückhol-Orts fällt (nach Gruppen-ID im Protokoll), nicht nur, was ≤ 0,5 m
   entfernt liegt. Teile anderer Gruppen in 51–70 cm bleiben (§4).
5. **Welle 1 – beantwortet:** Ja, eine eigene Revision des Editor-Werkzeugs mit Regel 22.3. Dazu gehören Sumpf-Vorrang, Reihenfolge,
   Toleranz und eine abschaltbare Klasse. Sie wird unabhängig nachgeprüft; F6 braucht sie nicht (§5).
6. **Lehm:** Mit Lehm-Gewicht 0 ändert sich weltweit nur 1 Urteil. Die Frage ist damit erledigt: **Lehm bleibt 0,4**, T22-L0 ist
   abgeschlossen. Ein Unterschied, der keine Entscheidung ändert, braucht keine Regeländerung.

---

## 1. Tiefe

- **22b §1.2:** Entfernt wird erst bei Tiefe > Grenze + 0,2 m, weil Spiegel und Gelände je nach Quelle um diese Größenordnung auseinanderliegen.
  Dieselbe Toleranz gilt für die neue Klasse.
- **Ergebnis:**
  - 0–0,10 m ok;
  - 0,10–0,30 m `hinweis` (nicht entfernen);
  - > 0,30 m bei sicherem Spiegel `zu_tief`;
  - ohne sicheren Spiegel `tiefe_unsicher`.
- **H5:** Für die 1 069 Hinweise 20 Stichproben von oben und schräg ansehen, als eigener Punkt nach Welle 1. Zeigen ≥ 2 von 20 ToadRush
  sichtbar in offenem Wasser, wird die Toleranz für den Sumpf geprüft. Bis dahin bleiben sie stehen.

## 2. Sumpf-Vorrang

- In 22 §4.4 gilt für Binsen in der Sumpf-Zone: Bei `feucht` (Nassmaske, Mulde oder TWI) und Hang ≤ 12° bleiben sie stehen. Das ist die
  Bult- und Nasswiesen-Logik des Sumpfplaners.
- ToadRush gehört in 22 zur Klasse „Binse“. Unsere Tabelle in 22f-2 §1 („Wiese ≥ 0,45 fern vom Wasser → Verstoß“) hätte den Zusatz
  „außerhalb der Sumpf-Zone“ gebraucht.
- **Korrektur (22.3):** Die Wiesen-Regel gilt nur außerhalb der Sumpf-Zone. Erwartung: Die 52 Verstöße in H5/H4/I5 entfallen. Bleiben einzelne
  übrig, sind sie dort auch ohne `feucht` gesetzt und damit echte Verstöße.

## 3. Prüfreihenfolge für `zwergbinse` (22.3)

1. **Wasserzelle:** nach Tiefe (§1). Damit ist das Urteil fertig.
2. **Uferband** (bis 15 m und 1,5 m über dem Spiegel): ok.
3. **Schlammboden:** Lehm + Schlamm ≥ 0,5 und Hang ≤ 8° → ok.
4. **Sumpf-Zone:** `feucht` und Hang ≤ 12° → ok.
5. **Wiese:** Gras ≥ 0,45, > 15 m vom Wasser, keine Mulde, außerhalb der Sumpf-Zone → Verstoß.
6. **Sonst:** wie 22.2 (Binsen-Regel mit Feuchte-Bedingung).

Grundsatz: Positive Standortprüfungen (2–4) kommen vor den Verstoß-Prüfungen. Heute betrifft das 0 Fälle, die Reihenfolge macht die Regel
aber eindeutig.

## 4. Ersatzgruppe beim Rückholen

- Eine Ersatzgruppe wurde für genau eine entfernte Instanz gesetzt (22 §6.2). Kommt diese Instanz zurück, ist die ganze Gruppe überflüssig.
  Teile davon stehen zu lassen erzeugt eine Mischung aus Original und halbem Ersatz.
- **r005c** = r005b minus alle Teile der Gruppen der 37 Rückhol-Orte, nach Gruppen-ID. Teile anderer Gruppen in 51–70 cm bleiben.
- **Abnahme:**
  - Gruppen-IDs der Rückhol-Orte gleich gestrichene Gruppen;
  - Simulation F6 mit 0 Verstößen;
  - 3 Bilder an Rückhol-Orten zeigen keine Doppelung.

## 5. Welle 1 und Editor-Werkzeug

- Die Revision des Reparaturwerkzeugs mit 22.3 enthält:
  - Klasse `zwergbinse`, abschaltbar (abgeschaltet byte-gleich mit r006b);
  - Reihenfolge nach §3;
  - Sumpf-Vorrang nach §2;
  - Toleranz nach §1;
  - Strand-Regel, Kahl-Regel und Schwellen aus 22f.
- **Nachprüfung vor Welle 1:** unabhängig, mit den Selbsttest-Fällen. Dazu gehören je 1 ToadRush in 0,2 m und in 0,4 m Wasser, auf Schlamm,
  auf Sumpf-Wiese mit `feucht` und auf Wiese fern vom Wasser.

## 6. Nächste Handlung

Unverändert der **Einbau F6 nach dem Testlevel-Lauf T23b-S**: r005c plus 37 Rückholungen mit Speicherbeleg, danach Neustart und Zensus.
Danach Welle 1 mit der neuen Werkzeugrevision.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Zwergbinsen zurück an den Altbetten:** braune Polster auf Riss-Schlamm statt halber Ersatzgruppen. Das ergibt ein ruhigeres, glaubwürdiges
   Trockenbett.
2. **Sumpf unangetastet lassen,** wo der Sumpfplaner Bulten und Nasswiese gesetzt hat. Dort trägt die Nassmaske das Bild, nicht die
   Wasserpflanzen-Regel.
3. **Stichprobe H5:** offenes Wasser gegen nasse Wiese an 20 Orten, bevor dort etwas entfernt wird.

## Quellen

- `recherche/auftraege/22g-zwergbinse-r007-rueckfragen.md` (Commit a6d95ca)
- `recherche/antworten/22b-wasserpflanzen-t22-0-rueckfragen.md` §1.2 (Commit 3256039)
- `recherche/antworten/22-wasserpflanzen-fern-vom-wasser.md` §4.4, §6.2 (Commit 41e3ca5)
- `recherche/antworten/22f-2-toadrush-test-ergebnis.md` §1–§3 (Commit 1868e8f)

## Rückfragen

Keine.
