# Antwort 22d – T22-0b: Lesart Kriterium 4, Houdini-Sperre im Piloten F6, Status Q_bach_E6_K2

Gelesen: recherche/auftraege/22d-t22-0b-ergebnis.md @ 0a6532dba38ec1e5149d8616126788efe012c731 (Commit 3050d50)

Stand 18.10.2026. Bezug: Antworten 22 (41e3ca5), 22b (3256039) §1.3, §2, §7, §9 und 22c (27435ad). Bearbeiter: Cloud-Recherche.
Bereich: Prüfklasse Wasserpflanzen (Regeln 22.2), Pilot F6. Nur Auswertung, keine eigene Rechnung auf Projektdaten.

## Kurzfazit

1. **Kriterium 4 – beantwortet.** Wir haben das Kriterium in 22b §9 unscharf formuliert, das ist unser Fehler. Verbindlich ist die Zählweise,
   aus der der Zielwert stammt. Die 4,0 % kamen aus T22-0 (22b §7) mit dem Nenner alle 67 990 und ohne lily im Zähler. Ergänzung für 22.2:
   `gesperrt` zählt **nicht** zum Rest, sondern wird als eigene Zahl gemeldet. Damit gilt **3,78 % → erfüllt**. Die anderen Lesarten
   (5,42 / 6,37 / 4,44 %) werden im Bericht mitgeführt, entscheiden aber nicht. Zielwert nach Auflösung aller Sperren: ≤ 4,0 % **mit** den
   früher gesperrten Fällen (§1).
2. **`houdini_bleibt` fehlt – beantwortet:** Für den Piloten F6 genügt die V0-Sperre, denn dort ist kein Fall betroffen. Vor dem zweiten
   Piloten (D4/D6) und vor jeder Reparatur in C4 muss der Typ nach 22c §3 in die Wahrheit eingetragen sein (§2).
3. **`Q_bach_E6_K2` – beantwortet, mit einer Bedingung:** Den Status auf „gebaut“ erst setzen, wenn eine Lesung bestätigt, dass `E6_Bach_K2`
   im Editor derselbe Bach ist (drei Prüfpunkte in §3). Die Änderung wird als eigener, gesicherter Eintrag in der Wahrheit protokolliert.
   Danach T22-0b nur für E5/E6 nachrechnen. Die 224 lily gehören zur v3-Nachrunde, nicht zur Wasserpflanzen-Regel.
4. **Pilot F6 und lily – beantwortet:** Der Vorschlag mit 1 222 Einträgen, 409 Ersatzorten und Ersatz als eigenem Schritt entspricht
   22b §1.3. Die 1 696 lily-Einträge kommen in die v3-Nachrunde nach dem Piloten. Sie gehören nicht in die F6-Liste, weil H5/I5 dort
   ohnehin nicht dabei sind und die F6-Liste eingefroren bleibt.
5. **Nächste Handlung:** unabhängige Nachprüfung von r006 nach Teamworkflow, danach T22-F6-1 mit den Kriterien aus 22b §1.3 (§5).

---

## 1. Kriterium 4: welche Lesart gilt

**Was schiefging:** In 22b §9 steht nur „Rest > 15 m ohne lily ≤ 4,0 %“. Damit war weder der Nenner festgelegt noch, wie die neue Klasse
`gesperrt` aus 22.2 zählt. Eine Zahl ohne festgelegte Zählweise ist nach `vorlagen/pruefung.md` (Messwerkzeuge: Zähler, Nenner, Klassen
vorab definieren) kein gültiges Kriterium. Wir legen sie jetzt fest und begründen sie; den Wert wählen wir nicht nach dem Ergebnis.

**Verbindliche Lesart (K4):**

| Teil | Festlegung | Grund |
|---|---|---|
| Nenner | alle Wasserpflanzen des Zensus 18.10. 08:28, **67 990** | Der Zielwert 4,0 % stammt aus T22-0 mit diesem Nenner (22b §7). Ein anderer Nenner vergleicht Äpfel mit Birnen. |
| Zähler | Instanzen > 15 m vom gebauten Wasser **nach** Anwendung von 22.2, ohne `SM_lily_01_*` | lily ist laut Editor-Lesung 22b-Nachtrag eine Landpflanze. |
| `gesperrt` | nicht im Zähler, **eigene Zahl** im Bericht | Diese Fälle sind zurückgestellt (V0, Netze, die wegfallen), nicht von der Regel als richtig beurteilt. Sie mitzuzählen bewertet den Stand der Wahrheit, nicht die Regel. |
| `hinweis`, `tiefe_unsicher` | nicht im Zähler; eigene Zahl | gleicher Grund |

→ **3,78 %: K4 erfüllt.** Bericht zusätzlich: Zahl `gesperrt` > 15 m und die drei anderen Lesarten, je mit Definition in einer Zeile.

**Gegenbedingung, damit die Lesart nichts versteckt:** Sobald V0 für ein Feld aufgehoben ist (Houdini zugeordnet, `houdini_bleibt`
eingetragen), werden dessen Fälle normal beurteilt. Das Weltziel nach Auflösung aller Sperren ist **≤ 4,0 % einschließlich der früher
gesperrten Fälle**, im gleichen Nenner. Wird das verfehlt, liegt der Hebel bei H5/Sumpf und `quelle` (22b §7 Punkt 2–3), nicht bei einer
neuen Lesart.

K4 ist ein Weltmaß und **kein Pilotkriterium.** Ob der Pilot F6 gelingt, entscheiden die Kriterien aus 22b §1.3.

## 2. `houdini_bleibt` und der Pilot F6

- F6 hat V0 = 0 % (T22-0b, Kriterium 7). Damit wirkt die fehlende Klasse dort nicht. **Der Pilot kann ohne sie laufen.**
- Die Sperre ist die richtige Voreinstellung: Pflanzen an Houdini-Flächen bleiben unangetastet, bis die Zuordnung steht (22b §2).
- **Vor dem zweiten Piloten** (Wüste/Canyon, D4/D6) und **vor C4** muss `houdini_bleibt` nach 22c §3 in der Wahrheit stehen: nur Becken
  und Auslauf der 10 bleibenden Fälle, Zellen > 2 cm über Gelände, ≤ 35°, mit dem Tiefpunkt verbunden. Erst dann V0 für diese Felder
  aufheben und dort T22-0b nachrechnen.

## 3. `Q_bach_E6_K2`: „vermutlich“ → „gebaut“

Ein „gebaut“ in der Wahrheit ändert drei Dinge auf einmal: die Wasserpflanzen-Regel, die neue `karte_wasser.r8` (22c) und später die
Nässe. Deshalb vorher eine Lesung im Editor, nur lesend:

1. **Identität:** `E6_Bach_K2` ist ein WaterBodyRiver mit Spline. Die Spline-Punkte liegen in der Draufsicht auf der Linie von
   `Q_bach_E6_K2`: Median-Abstand ≤ 1 m, höchstens 3 m.
2. **Ausdehnung:** Anfang und Ende stimmen mit der Wahrheit auf ≤ 5 m überein. Sonst nur den gebauten Abschnitt als „gebaut“ eintragen.
3. **Sichtbarkeit:** Der Bach ist mit Wasser gezeichnet. Ob SWR oder Plugin-Netz, ist zu prüfen; im Bericht als Typ angeben.

Sind alle drei erfüllt: Status setzen, die alte Wahrheit sichern, eine Protokollzeile anlegen (Gewässer, alter und neuer Status, Datum,
Beleg). Danach T22-0b nur für E5/E6 nachrechnen.

Folgen für die 224 lily: lily ist nach 22b eine Landpflanze. Sie fällt also nicht unter die Wasserpflanzen-Regel, sondern unter die
v3-Regel „Pflanze im Wasser“. Steht ein Maiglöckchen im gebauten Bach, wird es dort in der lily-Nachrunde behandelt. Die echten
Wasserpflanzen an diesem Bach werden mit dem neuen Status normal nach 22.2 beurteilt.

Ist eine der drei Bedingungen verletzt, bleibt „vermutlich“, und die Stelle bleibt für beide Regeln unverändert.

## 4. Pilot F6 und lily-Nachrunde

- **F6:** einverstanden, so wie in 22d §2 beschrieben. Zwei Punkte aus 22b §1.3 bitte ausdrücklich mitführen:
  - die Stichprobe mit 20 entfernten und 20 behaltenen Instanzen in der Draufsicht;
  - die 1-%-Stichprobe zur Rücknahme, bei der die Transform gleich bleiben muss.
- Der Ersatz bleibt ein eigener Schritt mit eigenem Speicherbeleg. Die Bilder vorher und nachher mit denselben Kameras gehören zum
  Entfernen und zum Ersatz.
- **lily:** 1 696 Einträge (H5 1 553). Erst nach dem Piloten und als eigene Runde mit der normalen v3-Regel; die Ausnahme für Bodenstreu
  gilt dabei wie in v3. Da 1 277 davon Kleinzeug sind, in H5 zuerst eine Stichprobe von 20 per Draufsicht. Eine „Pflanze im Wasser“ in
  der Nassmaske des Sumpfs kann eine Bult-Zelle sein, und die ist kein Wasser.

## 5. Nächste Handlung (eine, lokal)

**Nachprüfung r006, danach T22-F6-1.**

- **Erfolg der Nachprüfung:**
  - Eine zweite, unabhängige Rechnung reproduziert 10 715 Verstöße, 1 222 F6-Einträge und 409 Ersatzorte exakt.
  - Der SHA-256 der F6-Liste stimmt.
  - K4 wird nach §1 berechnet und mit allen Nebenzahlen berichtet.
- **Danach:** T22-F6-1 mit den Kriterien aus 22b §1.3.
- **Abbruch:** Weicht eine Zahl ab, wird T22-F6-1 nicht gestartet. Zuerst die Eingabestände per SHA-256 vergleichen.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Ersatz statt Lücke:** Entfernte Rohrkolben ohne passenden Trockenbett-Bewuchs hinterlassen kahle Stellen. Erst der Ersatz mit eigenem
   Bildvergleich macht die Bachbetten glaubwürdig.
2. **Planer-Rückfall verhindern (V1, 22c):** Solange die Planer an Altwasser setzen, kommt der Fehler beim nächsten Lauf zurück.
3. **Houdini-Becken in der Wahrheit:** Ohne `houdini_bleibt` bleiben die Ufer an den Schaufällen gesperrt und ungepflegt, also gerade dort,
   wo der Blick hinfällt.
4. **Feuchte-Abstufung am Ufer:** Witcher-Ufer zeigen einen Verlauf von nass zu trocken (Moos, Binsen, Gras). Das braucht die Nässe aus
   gebautem Wasser (22c §4, später als eigener Schritt).

## Quellen

- `recherche/antworten/22b-wasserpflanzen-t22-0-rueckfragen.md` §1.3, §2, §7, §9 (Commit 3256039)
- `recherche/antworten/22c-karte-wasser-rueckfragen.md` §3, §4 (Commit 27435ad)
- `recherche/vorlagen/pruefung.md`, Abschnitt Messwerkzeuge
- `recherche/auftraege/22d-t22-0b-ergebnis.md` (Commit 3050d50)

## Rückfragen

Keine. §3 ist als Bedingung formuliert und blockiert den Piloten F6 nicht.
