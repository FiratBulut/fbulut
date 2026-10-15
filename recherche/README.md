# Zusammenarbeit: Claude Code lokal und Cloud-Sitzung

Ferat hat Codex am 15.10.2026 beauftragt, den Ablauf ergebnisorientiert zu korrigieren.
**Ziel: bestätigte Lösungen und sichtbare Fortschritte statt wiederholter Aufträge.**

## Start und nächstes Ergebnis

1. Branch `claude/recherche-auftrag-s5m3y6` aktualisieren, diese README und die neuesten
   Befunde des aktiven Problems lesen. Pro Problem einen Vorgang mit stabiler ID führen.
2. Genau eine nächste Entscheidung wählen. Vorhandene Belege, Inventare und Werkzeuge
   verwenden; nur die dafür fehlenden Angaben beschaffen.
3. Die passende [Kurzvorlage](vorlagen/uebergabe.md) verwenden: Quellenfrage,
   Umsetzungstest oder Bildbewertung. Unpassende Felder entfallen.
4. Cloud liefert eine belegte Antwort, ein verwendbares Artefakt oder einen unterscheidenden
   Test. Lokal prüft Voraussetzungen, setzt um und meldet Ergebnis samt Beleg zurück.
5. Entscheiden: übernehmen, verwerfen, gezielt weiterprüfen oder begründet zurückstellen.
   Negative Tests zählen als Fortschritt, wenn sie eine Ursache ausschließen.

Lokal prüft Engine, Projekt, Materialgraphen, echte Bounds und Laufzeit. Die Cloud übernimmt
Recherche und Auswertung sowie alles, was ihre Werkzeuge selbst erlauben. Unabhängige Arbeit
läuft weiter. Rückfragen bündeln und nur stellen, wenn sie den nächsten Schritt verändern.
Ferats bestehende Entscheidungen und Freigaben gelten; keine erneute Bestätigung bereits
autorisierter Arbeit. Zusätzliche Ausgaben oder destruktive Aktionen sind damit nicht freigegeben.

## Welche Aussage gilt?

- Ferat bestimmt Ziele und Freigaben. Ein abweichender Messbefund verändert diese nicht,
  sondern zeigt eine technische Grenze oder einen Entscheidungsbedarf.
- Für Tatsachen im Projekt gilt der neueste nachvollziehbare lokale Nachweis **für denselben
  Build und Gegenstand**. Ein neuerer Text ohne Beleg verdrängt keinen älteren Messnachweis.
- Lieferformate regeln Datenstrukturen; ihre historischen Bestandsangaben sind kein Beleg
  für den heutigen Projektzustand. Bei Konflikten die betroffene Stelle mit Datum,
  Gültigkeitsbereich und Link zum ersetzenden Befund kennzeichnen.
- Beobachtung, Ursachenhypothese und Entscheidung trennen. Ein besseres BAKED_SIM-Bild
  beweist allein keine bestimmte WCBS-Ursache. Zustimmung einer zweiten KI ist kein
  unabhängiger Nachweis; beide können dieselbe Vermutung wiederholen.
- Belege kennzeichnen: lokal bestätigt / Quelle bestätigt / Hypothese / widerlegt / offen.
  Bei fehlendem Nachweis keinen API-Namen, Messwert oder vorhandenen Assetbestand erfinden.

## Eine Inventarablage

Maßgebliche Ablage für gemeinsame Inventare bleibt [vorlagen/daten](vorlagen/daten/),
Einstieg und Exportstand: [zusammenfassung.md](vorlagen/daten/zusammenfassung.md).
Claude Code lokal pflegt diese Exporte; die Cloud liest sie und meldet Abweichungen.
Die vorhandenen Werte bleiben bis zum nächsten Export ein **datierter Bestand**, kein
neu bestätigter Live-Stand. Neue Assets ausdrücklich als anzulegen kennzeichnen.

Bei relevanten Änderungen aktualisiert lokal die zusammengehörigen Exporte und ihren
Stand gemeinsam; betroffene Dateiversionen im Vorgang verlinken. Engine-/Pluginstand und
projektspezifische Nachweise nur im nötigen Umfang ergänzen. Keine zweite vollständige
Inventarkopie unter `auftraege/daten/`: dort bleiben Testdaten und gezielte Befunde.
Neuere Einzelbefunde gelten nur für die konkret geprüften Einträge; Abweichungen im
Inventareinstieg verlinken, bis der Export nachgezogen ist.

## Übergabe nach Version, nicht nach Dateiexistenz

Lokal schreibt `auftraege/<id>.md`, Cloud `antworten/<id>.md`. Rückmeldungen zum selben
Problem in diesen Dateien fortführen. Historische Nachtragsketten nicht umbenennen,
sondern den aktiven Nachfolger verlinken. Vorhandene weitere Artefaktzuständigkeiten bleiben.

**Revisionsschlüssel = Repositorypfad + Git-Blob-SHA** der gelesenen Datei; ein Commitlink
macht diese Version aufrufbar. Die Empfängerseite nennt in ihrer nächsten sachlichen
Antwort: `Gelesen: <Pfad> @ <Blob-SHA> (Commit <SHA>)`. Keine eigenen „gelesen“-Nachrichten
erzeugen. Reine Quittungs-/Formatänderungen verlangen keine Gegenquittung und keinen Test.

Bei Sitzungsbeginn und vor Übernahme eines Ergebnisses die aktuellen Versionen der aktiven
Auftrags-, Antwort- und Eingabedateien mit dem zuletzt bearbeiteten Stand vergleichen.
Nicht nur neue Dateinamen, Zeitstempel oder „Antwort existiert“ prüfen. Inhaltsänderungen
lesen und beurteilen; eine geänderte SHA bedeutet nicht automatisch neue Ausführung.
„Bereit zum Test“ ersetzt nicht die unten beschriebene lokale Vorprüfung. Danach bereits
autorisierte Arbeit ohne erneute Freigabefrage ausführen.

**Noch lokal zu verifizieren:** Ob vorhandene Startprompts und Abfragen diese README lesen
und Änderungen bestehender Dateien erkennen, wurde nicht nachgewiesen. Beim nächsten
Sitzungsstart die gelesene README-Version einmal im vorhandenen Bericht festhalten.
Bis die bestehende Abfrage geprüft/angepasst ist, den Versionsvergleich bei diesen
Übergabepunkten manuell ausführen. Ein Push startet keine Sitzung. Keine zusätzliche
Zeitsteuerung oder Quittungsschleife einrichten.

## Anwendung und Wiederaufnahme

Vor einer Umsetzung prüft lokal: genannte Assets/APIs vorhanden, Einheiten und Formate
passend, benötigte Dateien vollständig und **erwarteter Eingabestand noch gültig**?
Zum Arbeitspaket gehören die relevanten Eingabeversionen und das gelieferte Artefakt.
Vor dem Anwenden erneut vergleichen. Ein fachlich veränderter Eingang macht nur die
abhängigen Teile neu prüfpflichtig; keine blinde Übernahme nach einem sauberen Git-Merge.

Jeder Versuch erhält eine Test-ID und im lokalen Befund einen Ausführungsstand:
`vorbereitet → angewendet → geprüft` bzw. `verworfen/zurückgesetzt`, jeweils mit
Speicherstatus und Beleg. Nach Abbruch zuerst den tatsächlichen Projektzustand feststellen.
Bei unklarem Stand nicht erneut blind anwenden: mit Sicherung abgleichen, fortsetzen oder
gezielt zurücksetzen. Eine bereits angewendete Revision nicht nochmals setzen; Wiederholung
als neuen Versuch vom bekannten Ausgangsstand dokumentieren. Vorhandene Setzer auf Verhalten
bei Wiederholung prüfen, insbesondere bei Gelände-Deltas und Instanzen.

Eine Antwortdatei bedeutet „beantwortet“, nicht „erledigt“. Quellenfragen enden mit belegter
Antwort; Umsetzungen mit lokalem Abnahmeergebnis. Für die Ausführung ist der lokale Befund
maßgeblich, die Cloud verweist darauf. Historische „fertig“-Angaben nicht ungeprüft übernehmen.

## Tests und sichtbare Abnahme

Nur für Umsetzungen: einen wiederherstellbaren Ausgangsstand sichern und benötigte
Messwerkzeuge an bekannten Kontrollfällen prüfen; [Prüfregeln](vorlagen/pruefung.md).
Voraussetzungen kostengünstig prüfen, bevor eine aufwendige Umsetzung startet.
Ein vorhandenes kleines Testlevel nutzen; sonst den notwendigen Kontrollfall klein ergänzen.
Kleintests anschließend am betroffenen Projektabschnitt bestätigen.

**Wer visuell bewertet, muss die relevanten Ziel- und Projektbilder selbst gesehen haben.**
Fehlenden Bildzugriff benennen und einmal gezielt eine zugängliche Darstellung anfordern.
Die andere Seite darf unabhängig technisch arbeiten, aber keine eigene Bildbewertung
behaupten. Kein Warten auf zwei identische Bildfreigaben.

Pro Bildaufgabe passende [Zielbilder](bilder/zielbilder/) und wenige sichtbare Kriterien wählen.
Bei Wasser etwa Uferform, Kolke, Transparenz und Schaumverteilung; für Fernansichten andere
Referenzen verwenden. Vorher/nachher mit gleicher Kamera und Beleuchtung vergleichen.
Fremde Perspektiven berücksichtigen; Simulation und Bewegung nicht aus Standbildern ableiten.

Nächster visueller Meilenstein: **ein kurzer repräsentativer Bachabschnitt** erfüllt die
vereinbarten technischen Kriterien und nähert sich sichtbar den ausgewählten Ufer-/Wasser-
Referenzen. Technischen und visuellen Befund getrennt festhalten. Feinere Zellen, höhere
Dichte oder eine bestandene Darstellungsprüfung allein bestätigen den Gesamtlook nicht.
Wasserverhalten/Darstellung vor abhängiger Uferanpassung, danach Dekoration bearbeiten.

## Quellenzugriff und Aufwand

Die Cloud hatte Zugriffsprobleme auf Epic-Seiten; das ist sitzungsabhängig.
Direktabruf und einen verfügbaren alternativen Zugang versuchen, dann die Lücke benennen.
Suchauszüge bleiben Hinweise. Für entscheidende Inhalte einmal gezielt lokal URL,
Abschnitt und Frage anfordern. Zusammenfassung mit Datum, Versionsbezug und zulässigem
Auszug bzw. eigenem Engine-Dump liefern, danach wiederverwenden. Keine vertraulichen Daten
ins öffentliche Repository. Bei Foren auch spätere Korrekturen lesen.

Pro Übergabe nur nächste Handlung, Zuständigkeit und angemessenes Budget nennen.
Bei engen Quellenfragen höchstens 20 Minuten ohne andere Vorgabe; früher aufhören, sobald
die Antwort vorliegt. Lange Builds/Bakes gesondert planen. Nach zwei Runden ohne neue
Erkenntnis Ansatz prüfen, statt dieselbe Frage neu zu stellen. Zurückstellung braucht
einen Wiederaufnahmegrund. Hilfsmittel am konkreten Problem verbessern; kein Großprojekt
zur Prozesspflege starten.

## Startpunkt Shallow Water und Sitzungsabschluss

Aktuell maßgebliche Einstiegspunkte sind die lokalen Befunde
[6i](auftraege/16h-nachtrag6i-baked-sim-tests-stand.md) und
[6j](auftraege/16h-nachtrag6j-teilung-ergebnis.md); spätere passende Belege haben Vorrang.
BAKED_SIM ist lokal optisch erfolgreich beschrieben; gepackter Build, Streaming und
GPU-Kosten bleiben gesondert nachzuweisen. Die Teilung mit trockenen Nähten gilt nicht
als fertige Lösung. Vor weiteren Teilungen tatsächliche Engine-Bounds/Quellen/Senken prüfen.

Am Sitzungsende bzw. im bestehenden Morgenbericht knapp: geliefert, geprüft, offen,
nächster Schritt – jeweils mit Beleg. Keine neue Zeitsteuerung aus dieser Anleitung ableiten.
Die Prüfungen sind Arbeitsaufträge für die zuständige Sitzung, keine bereits ausgeführten
Unreal-Tests. Codex hat am 15.10. die sieben Witcher-Zielbilder, die Flussreferenz und den
BAKED_SIM-Vergleich angesehen; dies ist keine Laufzeit- oder Gesamtprojektabnahme.

## Git

Vor Push `git pull --rebase`; Konflikte unter Erhalt beider Beiträge lösen, kein Force-Push.
Bei API-Schreiben unmittelbar vorher lesen und aktuelle Datei-SHA verwenden. Änderungen
eines zusammengehörigen Arbeitspakets möglichst gemeinsam committen. Ein konfliktfreier
Push ersetzt weder die Eingabeprüfung noch die lokale Abnahme.
