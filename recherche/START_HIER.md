# Start für Claude am Sonntag, 18.10.2026

Ferat plant den Start **ab 04:00 Uhr Schweizer Zeit**, nach der angezeigten Rücksetzung
des Wochenlimits. Gemeint ist das Nutzungslimit; die bisherige Sitzung und gespeicherte
Ergebnisse bleiben Ausgangspunkt. Die Zeitangabe allein startet keine Sitzung.

## Einstiegstext für Ferat

Diesen Text bei der Fortsetzung in Claude verwenden:

> Übernimm meine aktuelle Arbeitsteilung: Opus 5.5 leitet das Projekt. Fünf Fachrollen
> arbeiten je nach Aufgabe mit Sonnet 5.5 oder Opus 5.5. Fable prüft erst den vollständig
> umgesetzten Gesamtauftrag. Die Cloud bleibt Recherchepartner, Codex liefert Assetbilder.
> Lies `D:\Das Lied der Asche\recherche_repo\recherche\START_HIER.md` und folge dem Einstieg.
> Prüfe zuerst den vorhandenen Arbeitsstand und laufende Prozesse, damit nichts doppelt
> ausgeführt wird. Verwende bestehende Ergebnisse und liefere die nächste konkrete Umsetzung.

## Die ersten Schritte für Opus-PM

1. **Stand sichern und fortsetzen.** Aktuellen Branch, eigene/unveröffentlichte Änderungen,
   aktive Agenten, laufende Editor-/Bake-Arbeit und letzten Teststand prüfen. In der
   Recherche-Kopie nur einen sicheren Git-Abgleich vornehmen; bei Konflikten keine fremden
   Änderungen verwerfen. Den separaten Unreal-Projektbranch nicht deshalb wechseln.
2. **Aktuelle Regeln übernehmen.** [CLAUDE.md](../CLAUDE.md), die relevanten Abschnitte der
   [Recherche-Regeln](README.md) und den [Teamworkflow](TEAM_WORKFLOW.md) lesen. Die alte
   Desktop-Anweisung „alles in die Cloud“ ist keine aktuelle Aufgabenverteilung. Vorhandene
   Gestaltungsentscheidungen Ferats und Projekt-/Editor-Schutzregeln weiter beachten.
3. **Verfügbarkeit tatsächlich prüfen.** Projektmanager Opus 5.5, Sonnet/Opus für Fachpakete,
   Fable nur für die spätere Endprüfung. Werkzeuge und Modellkennungen nachsehen; keinen
   verfügbaren Agenten oder Modellwechsel nur behaupten. Sonnet-Ausfall darf durch Opus
   übernommen werden. Bei weiter erschöpftem Limit einmal benennen und vorhandene Arbeit
   erhalten; keine wiederholten Fehlstarts, keine zusätzlichen bezahlten Konten/Dienste.
4. **Eine Priorität übernehmen.** Ferats jüngsten konkreten Auftrag und den letzten offenen
   Schritt verwenden. Historische Wasser-Befunde prüfen, bevor verworfene Ansätze wiederholt
   werden. Der bisherige Wasser-Meilenstein ist ein kurzer repräsentativer Bachabschnitt;
   ein Assetauftrag wird nur begonnen, wenn er die aktuelle Aufgabe tatsächlich unterstützt.
5. **Nur ausführbare Pakete starten.** Keine Pflicht, alle fünf Plätze zu belegen. Sonnet
   zuerst für Dateien/Belege/Dokumentation; Opus für Diagnose und neue Verfahren. Nur
   Opus-PM steuert den laufenden Unreal-Editor. Vor einem Bake/Rendervorgang Ausgangsstand,
   Pflichtkriterium, Aufwand und Abbruchbedingung festlegen.

Den übernommenen Workflow-Commit, die tatsächlich verfügbaren Rollen/Werkzeuge, den
aktuellen Auftrag und die nächste Handlung einmal im bestehenden Bericht nennen.
Keine separate Empfangsbestätigung an jede beteiligte Sitzung erzeugen.

## Bildauftrag und Rückweg

Opus-PM veröffentlicht bei tatsächlichem Bedarf einen vollständigen Bildauftrag nach
[GitHub-Protokoll](codex/README.md). Der Codex-Zeitplan läuft alle 30 Minuten; erfolgreiche
Abrufe ohne offene Bildaufträge sind am 17.10. in diesem Chat nachgewiesen. Damit ist die
Abfrage bestätigt, noch nicht eine erfolgreiche Bild-/Blender-Lieferkette.

Opus-PM ist zunächst der Ergebnisabfrager. Beim Start und vor dem nächsten abhängigen
Schritt die passende GitHub-Antwort prüfen. Nur wenn die Claude-Sitzung einen funktionierenden
Zeitgeber unterstützt, die autorisierte 30-Minuten-Abfrage dort aktivieren. Einmal ihren
tatsächlichen Abruf nachweisen. Ohne diesen Mechanismus „manuell“ melden; keine automatische
Fortsetzung vortäuschen. Ein noch ausstehendes Bild hält nur seine abhängigen Schritte auf.
Eine Cloud-Abfrage darf den lokalen Rückweg nicht ersetzen, wenn sie Opus-PM nicht erreicht.

Codex sichert einen Bildstart zusätzlich mit dem lokalen Werkzeug
[bildstart.py](codex/bildstart.py). Es verhindert doppelte Reservierungen derselben
Assetrevision auf diesem Dateisystem. Die GitHub-Besitzprüfung und die Pflicht, vorhandene
Ergebnisse wiederzuverwenden, gelten zusätzlich. Fable beteiligt sich nicht an diesem Warten.

## Eine vollständige praktische Probe

Für ein wirklich benötigtes einfaches Asset: klare Maße und wenige Pflichtkriterien → ein
Codex-Bild → Modell → Material/Export → lokaler Unreal-Test → vollständiges Paket an Fable.
Falls für den aktuellen Auftrag kein neues Asset nötig ist, zuerst dessen konkrete Umsetzung
abschließen; keine unnötige Bilderzeugung nur für den Workflow. Die Bildkette bleibt dann offen.

Rolle 5 sammelt vorhandene Belege; Opus-PM prüft den tatsächlichen Projektstand. Fable erst
starten, wenn er auf das vollständige Paket und die Bilder zugreifen kann. Sein Urteil gilt
für genau diese Ergebnisrevision. Optionale Wünsche getrennt von verletzten Pflichtkriterien.

Zusätzlich an einer Testkopie prüfen: unveränderte Eingabe startet kein zweites Bild;
gespeichertes Ergebnis wird nach einem Übertragungsfehler weiterverwendet. Keine laufende
Produktionsarbeit für einen Ausfalltest abbrechen. Die [Ablaufprobe](vorlagen/pruefung.md#ablaufprobe-für-die-sitzungsübergabe)
beschreibt weitere gezielte Fälle, die nur bei relevantem Risiko nötig sind.

## Bereits belegt und noch offen

| Stand am 17.10.2026 | Aussage |
| --- | --- |
| Codex-Zeitplan und GitHub-Abruf | Aktiv; mehrere planmäßige Abrufe erfolgreich, bisher keine Bildaufträge. |
| Lokale Sicherung gegen doppelte Bildstarts | 12 Offline-Tests bestanden, einschließlich zwei konkurrierender Prozesse und Windows-Verzeichnisverknüpfung; keine echte Generierung ausgelöst. |
| Claude-Start und Rollenübernahme | Erst beim tatsächlichen Fortsetzen nachzuweisen; ältere Desktop-Anweisungen/Erinnerungen wurden nicht umgeschrieben. |
| Automatische Claude-/Cloud-Ergebnisabfrage | Noch nicht eingerichtet/nachgewiesen; beim Start tatsächlichen Modus nennen. |
| Bild → Blender → Unreal → Fable | Noch kein vollständiger praktischer Nachweis. |

Die Testzahl bezieht sich ausschließlich auf das neue Sicherungswerkzeug. Sie bestätigt
keine Unreal-Qualität, Modellverfügbarkeit oder automatische Zusammenarbeit aller Sitzungen.
