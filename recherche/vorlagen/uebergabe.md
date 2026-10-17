# Kurze Übergaben

Es gilt der [Arbeitsablauf](../README.md). Nur eine passende Vorlage am Kopf der bestehenden
Auftrags-/Antwortdatei verwenden. Je Feld ein Satz plus Beleglink genügt. Ein Feld wird
erst ausgefüllt, wenn es für den aktuellen Schritt gebraucht wird; kein erfundenes Ergebnis.
Neue ID nur für ein eigenständiges Problem, keine neue Datei für jede Rückfrage.
Für Bild-/Blender-Arbeit stattdessen den lokalen [Assetauftrag](asset-auftrag.md) verwenden;
Rollen und Ablage stehen im [Teamworkflow](../TEAM_WORKFLOW.md). Nur eine davon unabhängige,
entscheidende Quellenfrage bekommt einen Forschungsauftrag mit Querverweis.

Gemeinsamer Kopf: ID, Datum, Status, Bearbeiter/Seite/Sitzungskennung, betroffener Bereich,
gelesene Gegenstellen-Version und nächste Handlung samt Budget. Beispiel für den Bezug:
`Gelesen: recherche/auftraege/<id>.md @ <Blob-SHA>
(Commit <SHA>)`. Bei einem neuen Erstauftrag entfällt dieser Bezug. Antworten auf reine
Quittungsänderungen sind nicht nötig. Überholte Empfehlungen bei Bedarf ausdrücklich nennen.
Wenn blockiert: „wartet auf <konkreter Beleg>, zuständig <Seite>; weiter bei <neuem Eingang>“
im vorhandenen Kopf ergänzen. Unverändert blockierte Vorgänge nicht erneut beauftragen.
Bei Übernahme letzte Test-ID und bestätigten Ausführungsstand nennen. Bei fehlgeschlagener
Veröffentlichung „lokal fertig, nicht veröffentlicht“ samt erhaltenem Commit/Entwurf nennen;
ein erneuter Push ist kein neuer Umsetzungstest.

## Starttext für die nächste Sitzung

> Lies `CLAUDE.md`, `recherche/README.md`, `recherche/TEAM_WORKFLOW.md` und den aktuellen Auftrag samt Antwort für den
> aktiven Vorgang. Prüfe Zuständigkeit, gelesene Revision und tatsächlichen Ausführungsstand.
> Setze genau die nächste autorisierte Handlung fort und liefere ein überprüfbares Ergebnis.
> Übernimm keinen noch laufenden Eingriff einer anderen Sitzung. Bei fehlendem Zugriff
> benenne einmal den konkreten benötigten Beleg und bearbeite unabhängig mögliche Arbeit.
> Halte Ergebnis, Beleg, Stand und nächsten Schritt im vorhandenen Vorgang fest.

Im vorhandenen Startprompt verwenden; keine zweite Zeitsteuerung einrichten. Ist kein
aktiver Vorgang eindeutig erkennbar, aktuelle offene Köpfe und Ferats jüngste Priorität
vergleichen. Bleiben mehrere gleichrangige Aufgaben mit gemeinsamer Ressource, die
Priorität einmal klären und bis dahin nur unabhängige Arbeit ausführen.

## A. Quellenfrage

- **Frage / Zielversion:** Welche nächste Entscheidung hängt davon ab, welcher Beleg fehlt
  trotz vorhandener Befunde und lokaler Möglichkeiten noch?
- **Befund / Beleg:** Antwort mit URL, Abschnitt/Beitrag, Datum und Gültigkeitsbereich.
- **Grenze / Abschluss:** bestätigt oder offen; fehlender Zugriff und genau benötigter
  lokaler Beleg, falls entscheidend. Sonst als beantwortet abschließen.

Kein Testlevel, Messprotokoll oder Bildnachweis nötig, solange keine entsprechende Aussage
gemacht wird. Eine bloße Suchvorschau ist keine vollständige Quellenbestätigung.

## B. Umsetzungstest

- **Ziel / Erwartung:** Eine Änderung und ihr Erfolgskriterium; bei aufwendigen Versuchen
  außerdem Fehler-/Abbruchbedingung. Bei zwei möglichen Ursachen die unterscheidende
  Beobachtung nennen.
- **Basis / Paket:** Ausgangsstand-ID, relevante Eingabeversionen und Artefaktversion;
  [Wiederherstellungs-/Messnachweise](pruefung.md) verlinken statt wiederholen.
  Bei Shallow-Water-Exporten Paketordner, Paket-ID aus `paket.json` und Ergebnis von
  `--uebergabe` nennen; bei Teilpaketen Zielgewässer und mitgelieferten Kontext angeben.
  Die verlangten Quelloptionen stehen in `pruefprofil.json`; passende lokale Pfade einsetzen.
  `quellgeometrie.json` muss zum aktuellen Planbestand passen. Bei Abweichung Eingabestand
  klären bzw. neu exportieren; Projekt-/Assetstand zusätzlich abgleichen.
- **Ausführung:** Test-ID; vorbereitet / angewendet / geprüft / verworfen bzw. zurückgesetzt;
  im Speicher oder gespeichert; erwarteter Eingang vor Anwendung bestätigt oder abweichend.
- **Ergebnis / Erklärung:** vorher → nachher mit Beleg; Ursache nachgewiesen oder Hypothese.
- **Mitbetroffene Stellen:** Bei gemeinsamen Ressourcen Vergleichsstellen und Ergebnisse
  nach [Prüfregeln](pruefung.md#auswirkungen-auf-andere-stellen); fehlende Prüfungen nennen.
- **Entscheidung:** übernehmen, verwerfen oder genau nächster Test; was wird dadurch ersetzt?
  Beantwortete Teilfrage schließen und verbleibende Folgefrage ausdrücklich abgrenzen.

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
