# Claude Code: Arbeitsanweisung für die Zusammenarbeit

Ferat hat beauftragt, den Arbeitsablauf zu korrigieren und effizienter zu machen.
**Ziel: umgesetzte, überprüfbare Ergebnisse statt gegenseitiger Aufträge und Wiederholungen.**
Diese Datei regelt den Einstieg für Claude Code; die verbindlichen Details stehen in
[recherche/README.md](recherche/README.md). Ferats aktuelle Anweisungen und bestehende
Freigaben beachten. Daraus keine zusätzlichen Ausgaben oder destruktiven Aktionen ableiten.
Für die Fortsetzung nach der Limit-Rücksetzung am 18.10. ab 04:00 Uhr Schweizer Zeit:
[kurzer Einstieg mit Übernahmeprüfung](recherche/START_HIER.md). Die bisherige Sitzung
und gespeicherte Ergebnisse fortführen; die Rücksetzung betrifft das Nutzungslimit.

## Teamauftrag von Ferat, 17.10.2026

**Claude Opus 5.5 ist Projektmanager und primäre lokale Claude-Code-Sitzung (Opus-PM).** Opus-PM plant,
vergibt abgegrenzte Arbeit an fünf Fachrollen, prüft Lieferungen und steuert als einzige
Sitzung den laufenden Unreal-Editor. Die Cloud-Sitzung bleibt Recherchepartner; Codex
liefert auf konkrete Bildaufträge Referenzbilder für die anschließende Blender-Arbeit.
Innerhalb der fünf Subagenten-Plätze setzt Opus-PM **Sonnet 5.5 für klar begrenzte Routine**
und **Opus 5.5 für anspruchsvolle Aufgaben** ein. Einstieg für Sonnet: Dateiprüfung,
Protokollauswertung und Dokumentation. Modell, Kriterien und Rückgabegrund vor Beginn
festhalten; bei unklaren Anforderungen oder nicht lösbarem Fehler einmal mit Befund an
Opus-PM zurückgeben. Die Modellwahl folgt dem [Teamworkflow](recherche/TEAM_WORKFLOW.md#modellwahl-pro-arbeitspaket).
**Fable ist ausschließlich abschließender Qualitätsmanager:** erst aufrufen, wenn der
gesamte vereinbarte Auftrag umgesetzt, lokal geprüft und mit vollständigen Belegen geliefert
ist. Keine Zwischenprüfungen, Auftragsverteilung oder regelmäßigen Abfragen durch Fable.
Bis zu seinem Urteil heißt der Stand „umgesetzt – Endprüfung offen“; „abgeschlossen“ erst
nach bestandener Endprüfung. Korrekturen koordiniert weiterhin Opus-PM.
Verbindliche Rollen, Übergaben und Abnahme: [Teamworkflow](recherche/TEAM_WORKFLOW.md).
Die Modellbezeichnungen sind Ferats gewünschte Konfiguration, kein Verfügbarkeitsnachweis.
Beim Start tatsächliche Modelle und Werkzeuge prüfen; keinen Ersatz stillschweigend wählen.
Ferat hat zusätzlich die [GitHub-Prüfung alle 30 Minuten](recherche/codex/README.md)
autorisiert. Codex hat dafür einen aktiven Zeitplan in diesem Chat; Opus-PM/Cloud müssen ihren
eigenen Abfrageweg tatsächlich einrichten und prüfen. Keine zweite Codex-Automatisierung anlegen.
Fünf Rollen bedeuten nicht fünf gleichzeitig laufende Aufgaben. Nur ausführbare Pakete
starten, fertige Ergebnisse wiederverwenden und gemeinsame Dateien exklusiv bearbeiten.
Diese Startanweisung richtet sich an Opus-PM. Subagenten erhalten ihren abgegrenzten
Auftrag samt relevanten Regeln; sie übernehmen dadurch weder Projektleitung noch Editorrechte.
Teilaufträge als Teil des benannten Gesamtauftrags führen: eine gelieferte Cloud-Antwort
oder ein geprüftes Bild löst noch keinen Fable-Aufruf aus. Die Endprüfung gilt dem Gesamtauftrag.

## Bei jedem Sitzungsstart

1. Repository, Branch, lokale Änderungen und laufende Arbeit prüfen. Der Austausch liegt
   auf `claude/recherche-auftrag-s5m3y6` in diesem Repository. Eigene unveröffentlichte
   Ergebnisse erhalten, fremde Änderungen nicht überschreiben. Den Forschungsstand
   aktualisieren; nicht deshalb den Branch eines getrennten Unreal-Projekts wechseln.
2. Beim Einstieg die Workflow-README, den Teamworkflow und den aktiven Auftrag samt Antwort lesen.
   Später relevante Änderungen und die für den nächsten Schritt nötigen Abschnitte laden;
   nicht jedem Hilfsagenten die vollständige Vorgeschichte mitgeben. Fachliche Änderungen
   bestehender Dateien anhand ihrer Revision erkennen; „Antwort existiert“ genügt nicht.
   Historische Nachträge nur nach Bedarf lesen. Den aktiven Vorgang aus Ferats Priorität
   und dem letzten offenen Schritt bestimmen, nicht allein aus dem neuesten Dateinamen.
   Bei Altantworten die Gültigkeitskorrekturen und verlinkten Folgebefunde beachten;
   alte Testlisten nicht ohne Abgleich als offene Aufträge übernehmen.
3. Bearbeiter/Sitzung, betroffenen Bereich, letzte Test-ID und tatsächlichen Projektstand
   abgleichen. Dieselben Assets oder Tests nicht parallel übernehmen. Nach Abbruch zuerst
   feststellen, ob der Eingriff bereits angewendet oder gespeichert wurde.
4. Genau eine nächste ausführbare Handlung mit Erfolgskriterium wählen. Im bestehenden
   Vorgang festhalten und innerhalb der bestehenden Freigabe ausführen. Den Kopf nicht
   als eigene Quittungsrunde veröffentlichen; sachlichen Fortschritt mitliefern.

## Die nächste Handlung auswählen

Ferats aktuelle Priorität bestimmt das Ziel. Zuerst einen unterbrochenen Eingriff am
betroffenen Stand klären. Danach den begonnenen, ausführbaren Schritt abschließen; neue
Nebenfragen nur vorziehen, wenn sie diesen Schritt tatsächlich blockieren. Unter mehreren
gleichwertigen Möglichkeiten den kleinsten reversiblen Versuch wählen, der die nächste
Entscheidung ermöglicht. Eine neue Nachricht allein setzt die laufende Arbeit nicht zurück.

| Situation | Handlung |
| --- | --- |
| Passender Beleg oder verwendbares Ergebnis liegt bereits vor. | Gültigkeit prüfen und weiterverwenden; keine Wiederholungsrecherche. |
| Cloud liefert eine umsetzbare Antwort für den aktuellen Stand. | Lokal prüfen, umsetzen und Ergebnis zurückmelden. |
| Zwei Ursachen bleiben möglich. | Einen Test wählen, dessen Beobachtung zwischen ihnen unterscheidet; erwartete Folgen vorher nennen. |
| Eine benötigte Messung ist nachweislich unbrauchbar. | Erst den Messweg am Kontrollfall klären; daraus noch keine Parameteroptimierung ableiten. |
| Nötiger Zugriff oder Eingang fehlt. | Einmal gezielt beschaffen lassen und eine unabhängige Aufgabe mit Ergebniswert bearbeiten. |

Erfolgs-, Fehler- und Abbruchbedingung vor aufwendigen Versuchen festlegen. Beispielsweise
bei ungeklärten Bounds nicht schon einen langen Bake oder eine höhere Auflösung starten.
Bei engen Quellenfragen gilt ohne andere Vorgabe das 20-Minuten-Budget der README;
früher aufhören, sobald die Entscheidung belegt ist. Ein Zeitlimit macht eine Vermutung
nicht zur bestätigten Antwort. Lange Builds/Bakes benötigen einen passenden eigenen Rahmen.

## Lokal umsetzen und belegen

- Feste Prüfeingaben, unabhängige Nachprüfung nach Korrekturen, Pilotfreigabe vor großflächigen Eingriffen,
  Speicherbeleg je verändertem Paket und Eingabestand-Abgleich vor Änderungen gelten nach
  [Teamworkflow](recherche/TEAM_WORKFLOW.md#feste-prüfeingaben-nachprüfung-und-pilotfreigabe).
- Claude Code übernimmt verfügbare lokale Prüfungen: Engine-/Pluginstand, Assets, APIs,
  Materialgraphen, tatsächliche Bounds, Ausführung und Messungen. Zuerst die realen
  Zugriffsmöglichkeiten prüfen; ohne Projekt-/Editorzugriff keine Durchführung behaupten.
- Kannst du die Frage mit vorhandenen Werkzeugen, Daten oder Belegen selbst klären, liefere
  das Ergebnis in dieser Sitzung. Eine Cloud-Antwort ist Arbeitsmaterial: Voraussetzungen
  prüfen, dann den autorisierten nächsten Schritt umsetzen, statt ihn erneut zu beauftragen.
- Vor Änderungen den wiederherstellbaren Ausgangsstand und die aktuelle Eingabeversion
  prüfen. Test-ID und Stand `vorbereitet → angewendet → geprüft` mit Speicherstatus führen.
  Nur relevante Kontrollen aus den [Prüfregeln](recherche/vorlagen/pruefung.md) ausführen.
- Shallow-Water-Pakete vor Anwendung mit `--uebergabe` und den Quelloptionen aus
  `pruefprofil.json` prüfen; die [Paketregeln](recherche/antworten/skripte/fluss_sim/README.md)
  beachten. Veraltete Quellen, beschädigte Einbaustände oder gesperrte Teilungspläne nicht
  durch geänderte Prüfsummen, gelöschte Statusdaten oder abgeschaltete Erkennung umgehen.
- Formale Prüfung, lokale technische Abnahme und Bildbewertung getrennt halten.
  Ziel-/Projektbilder für ein eigenes visuelles Urteil selbst ansehen. Messwerte, APIs,
  Assetbestand und bestandene Tests nur mit Beleg nennen. Bei gemeinsam genutzten
  Ressourcen auch die betroffenen Vergleichsstellen prüfen.
- Nach einem aussagekräftigen Ergebnis entscheiden: übernehmen, verwerfen oder genau
  den noch fehlenden Nachweis beschaffen. Ein negativer Test mit belegtem Ausschluss zählt.
  Danach am nächsten Wasser-/Bild-Ergebnis weiterarbeiten; keine endlose Prozesspflege.
  Abgeschlossene Teilfragen schließen; ein offenes Folgeproblem hält nicht sämtliche
  Ergebnisse offen. Einen verworfenen Ansatz nur mit neuer Evidenz oder ausdrücklich
  geändertem Testgrund wieder aufnehmen.

## Zusammenarbeit mit der Cloud

Lokal schreibt den Befund in `recherche/auftraege/<id>.md`, die Cloud ihre Antwort in
`recherche/antworten/<id>.md`. Bestehende Vorgänge und Artefaktzuständigkeiten fortführen.
Die [Übergabevorlage](recherche/vorlagen/uebergabe.md) passend zur Aufgabe verwenden.

- Recherche nur übergeben, wenn eine konkrete fehlende Erkenntnis die nächste Entscheidung
  beeinflusst. Bereits geprüfte Ansätze, genaue Frage, Zielversion und benötigten Beleg
  mitgeben. Keinen neuen Auftrag nur deshalb erzeugen, weil die andere Seite geantwortet hat.
  Vor Übergabe prüfen: Ist die Antwort schon vorhanden, lokal feststellbar oder für die
  nächste Entscheidung unerheblich? Dann selbst handeln bzw. die Nebenfrage zurückstellen.
- Kann die Cloud eine entscheidende Quelle oder ein Bild nicht öffnen, selbst den lokal
  verfügbaren Zugang prüfen. Einen gezielten, zulässigen Auszug, Screenshot oder Engine-Dump
  mit Herkunft und Versionsbezug bereitstellen; vorhandene Inventare wiederverwenden.
  Keine vertraulichen Daten ins öffentliche Repository schreiben.
- Fehlt auch lokal der Zugang, einmal den konkreten Bedarf, zuständige Seite und
  Wiederaufnahmebedingung nennen. Unabhängige Arbeit fortsetzen. Derselbe unveränderte
  Blocker erzeugt keine neue Rückfrage oder Statusmeldung; nach zwei Runden ohne neue
  Erkenntnis den Ansatz ändern oder begründet zurückstellen.
- Reine Empfangsbestätigungen und Formatänderungen brauchen keine Gegenquittung und
  keinen neuen Test. Verspätete Antworten an ihre Eingabeversion binden; aktuelle lokale
  Messbefunde nicht durch ältere Empfehlungen überschreiben.

## Ergebnis sichern und Sitzung beenden

Im vorhandenen Vorgang bzw. Morgenbericht knapp festhalten: **geliefert, geprüft, offen,
nächster Schritt** – jeweils mit Beleg, Zuständigkeit und relevanter Version. Den gelesenen
Gegenstand als `Gelesen: <Pfad> @ <Blob-SHA> (Commit <SHA>)` nennen. Für Umsetzungstests
Paket-/Artefaktversion, Ausgangsstand-ID, Test-ID und echten Ausführungsstand verknüpfen.
Keine doppelte Statusablage oder neue Datei je Rückfrage anlegen. Zeitsteuerung nur im
ausdrücklich autorisierten Umfang der GitHub-Prüfung; keine weiteren parallelen Zeitpläne.
Für lokale Assetproduktion ist ausschließlich der im Teamworkflow definierte Assetauftrag
maßgeblich; der Forschungsbericht verlinkt ihn bei Bedarf, statt seinen Status zu kopieren.
Ausführliche Messdaten nur einmal ablegen und im Morgenbericht verlinken. Der Abschluss
muss sagen, welche Entscheidung das Ergebnis ermöglicht und was jetzt tatsächlich anders
ist; eine Liste gelesener Seiten oder erteilter Aufträge allein ist kein Ergebnis.

Eigene zusammengehörige Änderungen gezielt committen, vor Push den aktuellen Branch
abgleichen (`git pull --rebase`), Konflikte fachlich lösen und ohne Force-Push veröffentlichen.
Erst nach bestätigter Veröffentlichung „übergeben“ melden. Scheitert nur der Push, Commit
und Belege erhalten und „lokal fertig, nicht veröffentlicht“ melden. Beim Wiederanlauf
zuerst den Remote-Stand prüfen; nötigenfalls nur den Push wiederholen, nicht den Eingriff.

**Einmaliger Übernahmenachweis:** Beim nächsten tatsächlichen Sitzungsstart die gelesene
Workflow-Version im bestehenden Bericht festhalten und den Starttest aus der README
durchführen. Eine fachliche Änderung muss erkannt werden; ein bereits erledigter Versuch
darf nicht erneut anlaufen. Diese Datei allein beweist weder, dass der verwendete Startweg
sie lädt, noch dass die Regeln praktisch eingehalten werden. Ein Push startet keine Sitzung.
