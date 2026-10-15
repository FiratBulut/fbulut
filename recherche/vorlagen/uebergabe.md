# Kurze Übergaben

Es gilt der [Arbeitsablauf](../README.md). Nur eine passende Vorlage am Kopf der bestehenden
Auftrags-/Antwortdatei verwenden. Je Feld ein Satz plus Beleglink genügt. Ein Feld wird
erst ausgefüllt, wenn es für den aktuellen Schritt gebraucht wird; kein erfundenes Ergebnis.
Neue ID nur für ein eigenständiges Problem, keine neue Datei für jede Rückfrage.

Gemeinsamer Kopf: ID, Datum, Status/Zuständigkeit, gelesene Gegenstellen-Version und nächste
Handlung samt Budget. Beispiel für den Bezug: `Gelesen: recherche/auftraege/<id>.md @ <Blob-SHA>
(Commit <SHA>)`. Bei einem neuen Erstauftrag entfällt dieser Bezug. Antworten auf reine
Quittungsänderungen sind nicht nötig. Überholte Empfehlungen bei Bedarf ausdrücklich nennen.

## A. Quellenfrage

- **Frage / Zielversion:** Welche Entscheidung hängt davon ab?
- **Befund / Beleg:** Antwort mit URL, Abschnitt/Beitrag, Datum und Gültigkeitsbereich.
- **Grenze / Abschluss:** bestätigt oder offen; fehlender Zugriff und genau benötigter
  lokaler Beleg, falls entscheidend. Sonst als beantwortet abschließen.

Kein Testlevel, Messprotokoll oder Bildnachweis nötig, solange keine entsprechende Aussage
gemacht wird. Eine bloße Suchvorschau ist keine vollständige Quellenbestätigung.

## B. Umsetzungstest

- **Ziel / Erwartung:** Eine Änderung und ihr Erfolgskriterium.
- **Basis / Paket:** Ausgangsstand-ID, relevante Eingabeversionen und Artefaktversion;
  [Wiederherstellungs-/Messnachweise](pruefung.md) verlinken statt wiederholen.
- **Ausführung:** Test-ID; vorbereitet / angewendet / geprüft / verworfen bzw. zurückgesetzt;
  im Speicher oder gespeichert; erwarteter Eingang vor Anwendung bestätigt oder abweichend.
- **Ergebnis / Erklärung:** vorher → nachher mit Beleg; Ursache nachgewiesen oder Hypothese.
- **Mitbetroffene Stellen:** Bei gemeinsamen Ressourcen Vergleichsstellen und Ergebnisse
  nach [Prüfregeln](pruefung.md#auswirkungen-auf-andere-stellen); fehlende Prüfungen nennen.
- **Entscheidung:** übernehmen, verwerfen oder genau nächster Test; was wird dadurch ersetzt?

Vor Ausführung stehen nur Plan und Basis fest. Nach Abbruch Ausführungsstand mit dem echten
Projekt abgleichen. Ein bereits angewendetes Paket nicht nochmals blind ausführen.

## C. Bildbewertung

- **Ziel / Referenz:** Konkrete Bildpfade und höchstens drei entscheidende sichtbare Merkmale.
- **Gesehen:** Tatsächlich betrachtete Ziel-/Projektbilder mit Version; fehlenden Zugriff nennen.
- **Vergleich:** Vorher/nachher aus gleicher Kamera/Beleuchtung; fremde Perspektive berücksichtigen.
- **Urteil / nächste Änderung:** besser, schlechter oder unklar je Merkmal; eine priorisierte
  Maßnahme. Technische Abnahme separat verlinken, falls erforderlich.

Ein technisches Testergebnis ersetzt keine Bildbewertung. Wer die Bilder nicht sehen kann,
leistet weiter unabhängige technische Arbeit und übernimmt kein eigenes visuelles Urteil.
