# Claude Code: Arbeitsanweisung für die Zusammenarbeit

Ferat hat beauftragt, den Arbeitsablauf zu korrigieren und effizienter zu machen.
**Ziel: umgesetzte, überprüfbare Ergebnisse statt gegenseitiger Aufträge und Wiederholungen.**
Diese Datei regelt den Einstieg für Claude Code; die verbindlichen Details stehen in
[recherche/README.md](recherche/README.md). Ferats aktuelle Anweisungen und bestehende
Freigaben beachten. Daraus keine zusätzlichen Ausgaben oder destruktiven Aktionen ableiten.

## Bei jedem Sitzungsstart

1. Repository, Branch, lokale Änderungen und laufende Arbeit prüfen. Der Austausch liegt
   auf `claude/recherche-auftrag-s5m3y6` in diesem Repository. Eigene unveröffentlichte
   Ergebnisse erhalten, fremde Änderungen nicht überschreiben. Den Forschungsstand
   aktualisieren; nicht deshalb den Branch eines getrennten Unreal-Projekts wechseln.
2. Die Workflow-README und den aktiven Auftrag samt Antwort lesen. Fachliche Änderungen
   bestehender Dateien anhand ihrer Revision erkennen; „Antwort existiert“ genügt nicht.
   Historische Nachträge nur nach Bedarf lesen. Den aktiven Vorgang aus Ferats Priorität
   und dem letzten offenen Schritt bestimmen, nicht allein aus dem neuesten Dateinamen.
3. Bearbeiter/Sitzung, betroffenen Bereich, letzte Test-ID und tatsächlichen Projektstand
   abgleichen. Dieselben Assets oder Tests nicht parallel übernehmen. Nach Abbruch zuerst
   feststellen, ob der Eingriff bereits angewendet oder gespeichert wurde.
4. Genau eine nächste ausführbare Handlung mit Erfolgskriterium wählen. Im bestehenden
   Vorgang festhalten und innerhalb der bestehenden Freigabe ausführen. Den Kopf nicht
   als eigene Quittungsrunde veröffentlichen; sachlichen Fortschritt mitliefern.

## Lokal umsetzen und belegen

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

## Zusammenarbeit mit der Cloud

Lokal schreibt den Befund in `recherche/auftraege/<id>.md`, die Cloud ihre Antwort in
`recherche/antworten/<id>.md`. Bestehende Vorgänge und Artefaktzuständigkeiten fortführen.
Die [Übergabevorlage](recherche/vorlagen/uebergabe.md) passend zur Aufgabe verwenden.

- Recherche nur übergeben, wenn eine konkrete fehlende Erkenntnis die nächste Entscheidung
  beeinflusst. Bereits geprüfte Ansätze, genaue Frage, Zielversion und benötigten Beleg
  mitgeben. Keinen neuen Auftrag nur deshalb erzeugen, weil die andere Seite geantwortet hat.
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
Keine separate Statusablage, zusätzliche Zeitsteuerung oder neue Datei je Rückfrage anlegen.

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
