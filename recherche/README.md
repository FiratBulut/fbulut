# Zusammenarbeit: Claude Code lokal und Cloud-Sitzung

Ferat hat Codex am 15.10.2026 beauftragt, den Ablauf ergebnisorientiert zu korrigieren.
**Ziel: bestätigte Lösungen und sichtbare Fortschritte statt wiederholter Aufträge.**

**Aktualisierte Rollenentscheidung vom 17.10.2026:** Opus 5.5 (Opus-PM) übernimmt die Projektleitung,
fünf Opus-5.5-Subagenten erhalten feste Fachrollen, Codex liefert angeforderte Assetbilder.
Fable übernimmt ausschließlich die Endprüfung des vollständig umgesetzten Auftrags;
vorherige operative Prüfungen erledigt das Opus-Team. Bis zur Endprüfung bleibt der Auftrag
„umgesetzt – Endprüfung offen“. Das ersetzt die frühere Projektmanager-Rolle von Fable.
Der [Teamworkflow](TEAM_WORKFLOW.md) regelt diese Arbeitsaufteilung und die lokale
Bild-/Blender-Produktion. Diese README bleibt maßgeblich für Recherche, Quellenbelege,
Shallow-Water-Prüfungen und Git-Übergaben. Die Cloud-Recherche wird dadurch nicht ersetzt.
Ferat hat am 17.10. zusätzlich eine [30-Minuten-Abfrage für Codex-Bildaufträge](codex/README.md)
autorisiert. Dort stehen Eingangs-/Antwortpfade und die Regel für Ergebnisabfragen durch
den zuständigen Auftraggeber. Andere Abfragewege dadurch nicht doppelt starten.

## Start und nächstes Ergebnis

1. Branch `claude/recherche-auftrag-s5m3y6` aktualisieren, diese README und die neuesten
   Befunde des aktiven Problems lesen. Pro Problem einen Vorgang mit stabiler ID führen.
   Einstieg für neue Sitzungen: [CLAUDE.md](../CLAUDE.md); ein kurzer Starttext steht in
   der [Übergabevorlage](vorlagen/uebergabe.md#starttext-für-die-nächste-sitzung).
2. Genau eine nächste Entscheidung für Ferats aktuelle Priorität wählen. Einen begonnenen
   ausführbaren Schritt abschließen, bevor gleichrangige Nebenfragen begonnen werden.
   Vorhandene Belege, Inventare und Werkzeuge verwenden; nur fehlende entscheidende Angaben
   beschaffen. Der kleinste reversible, aussagekräftige Versuch hat Vorrang vor breiter Suche.
3. Die passende [Kurzvorlage](vorlagen/uebergabe.md) verwenden: Quellenfrage,
   Umsetzungstest oder Bildbewertung. Unpassende Felder entfallen.
4. Cloud liefert eine belegte Antwort, ein verwendbares Artefakt oder einen unterscheidenden
   Test. Lokal prüft Voraussetzungen, setzt um und meldet Ergebnis samt Beleg zurück.
5. Entscheiden: übernehmen, verwerfen, gezielt weiterprüfen oder begründet zurückstellen.
   Negative Tests zählen als Fortschritt, wenn sie eine Ursache ausschließen.
   Abgeschlossene Teilfragen schließen; offene Folgefragen getrennt im selben Vorgang
   kennzeichnen. Verworfene Ansätze nur mit neuer Evidenz oder geändertem Testgrund aufnehmen.

**Arbeitsregel ab 16.10.:** Pro Problem genau eine ausführbare nächste Handlung mit einer
zuständigen Seite. Kann diese Seite die Frage selbst beantworten, liefert sie das Ergebnis
in derselben Sitzung. Ein neuer Testauftrag ist nur nötig, wenn ein entscheidender Beleg
anders nicht erreichbar ist; erwartete Beobachtung und Entscheidung danach mitliefern.
Bei fehlenden Daten einmal konkret benennen, was fehlt und wer es liefern kann. Den Vorgang
auf „wartet auf <Beleg>“ setzen und unabhängig weiterarbeiten. Ohne neuen Eingang keine
erneute Rückfrage, Ersatzauftragskette oder bloße Statusantwort erzeugen.

Lokal prüft Engine, Projekt, Materialgraphen, echte Bounds und Laufzeit. Die Cloud übernimmt
Recherche und Auswertung sowie alles, was ihre Werkzeuge selbst erlauben. Unabhängige Arbeit
läuft weiter. Rückfragen bündeln und nur stellen, wenn sie den nächsten Schritt verändern.
Ferats bestehende Entscheidungen und Freigaben gelten; keine erneute Bestätigung bereits
autorisierter Arbeit. Zusätzliche Ausgaben oder destruktive Aktionen sind damit nicht freigegeben.

## Zuständigkeit und Unterbrechungen

Im bestehenden Vorgangskopf stehen **Bearbeiter/Sitzung, betroffener Bereich, Stand und
nächste Handlung**. Eine kurze Sitzungskennung genügt. Auftragsdatei und Antwort dürfen
verschiedene Bearbeiter haben; dieselbe Datei, dasselbe Asset oder derselbe Teststand
hat gleichzeitig nur einen ausführenden Bearbeiter. Unabhängige Recherche bleibt möglich.
Keine zusätzliche Statusdatei und keine eigene Quittungsrunde anlegen. Die neue lokale
Assetproduktion verwendet ihren eigenen einzelnen Assetauftrag gemäß Teamworkflow;
derselbe Vorgang wird nicht zusätzlich als Forschungsauftrag gespiegelt.

| Stand | Nächste Handlung |
| --- | --- |
| offen | Zuständigkeit im Vorgang klären, bestehenden Stand prüfen und Arbeit beginnen. |
| in Arbeit | Derselbe Bearbeiter setzt fort; weitere Sitzungen liefern nur unabhängige Beiträge. |
| wartet auf … | Konkreten fehlenden Eingang, Lieferseite und Wiederaufnahmebedingung nennen; unabhängig weiterarbeiten. |
| geliefert | Empfänger führt die benannte Prüfung/Entscheidung aus; reine Quellenantworten dürfen damit abgeschlossen sein. |
| abgeschlossen / verworfen | Befund wiederverwenden; nur bei neuem relevanten Eingang oder begründetem neuen Versuch öffnen. |

Bei zwei Sitzungen derselben Seite die bereits eingetragene ausführende Sitzung beibehalten.
Ein alter Zeitstempel, eine Pause oder ein fehlender Push gibt den Bereich nicht automatisch
frei. Vor Übernahme letzten gespeicherten Stand und laufende Prozesse prüfen und bestätigen,
dass die alte Ausführung beendet ist; andernfalls nur unabhängig weiterarbeiten. Die
Übernahme samt letzter Test-ID im bestehenden Vorgang notieren. Diese Regel ist organisatorisch,
keine technische Sperre gegen gleichzeitig gestartete Prozesse.

Ändert sich während der Arbeit eine relevante Vorgabe, das Ergebnis an die tatsächlich
verwendete Revision binden. Abweichung vor Anwendung prüfen: weiter gültig, gezielt
anzupassen oder überholt. Ein verspätetes Ergebnis darf einen neueren lokalen Befund nicht
still überschreiben. Prozessstatus und Ausführungsstand eines Tests getrennt halten:
„geliefert“ bedeutet insbesondere nicht „im Projekt angewendet“.

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

**Noch lokal zu verifizieren:** Der Repository-Einstieg ist in `CLAUDE.md` hinterlegt.
Ob vorhandene Startprompts und Abfragen diesen Einstieg bzw. diese README lesen
und Änderungen bestehender Dateien erkennen, wurde nicht nachgewiesen. Beim nächsten
Sitzungsstart die gelesene README-Version einmal im vorhandenen Bericht festhalten.
Bis die bestehende Abfrage geprüft/angepasst ist, den Versionsvergleich bei diesen
Übergabepunkten manuell ausführen. Ein Push startet keine Sitzung. Keine zusätzliche
Zeitsteuerung oder Quittungsschleife außer der ausdrücklich beauftragten Codex-Abfrage und
der zugehörigen Ergebnisabfrage einrichten; bestehende Abfragen dafür verwenden.

**Einmaliger Starttest am nächsten lokalen Termin:** Bestehenden Startprompt/Abfrageweg
prüfen und bei Bedarf auf diese README und Inhaltsversionen umstellen. Eine kontrollierte
Änderung in einer bestehenden aktiven Datei muss beim nächsten Start erkannt werden;
eine unveränderte oder nur quittierte Revision darf keine Wiederholung auslösen. Den
Erkennungsnachweis und das daraus tatsächlich gelieferte Ergebnis im bestehenden Bericht
festhalten. Bis dahin bleibt „automatische Übernahme des Ablaufs“ offen, auch bei grünen
Exporter-Tests. Dieser Test wurde hier nicht ausgeführt.
Für Unterbrechungen und konkurrierende Sitzungen die
[Ablaufprobe](vorlagen/pruefung.md#ablaufprobe-für-die-sitzungsübergabe) verwenden.

## Anwendung und Wiederaufnahme

Vor einer Umsetzung prüft lokal: genannte Assets/APIs vorhanden, Einheiten und Formate
passend, benötigte Dateien vollständig und **erwarteter Eingabestand noch gültig**?
Zum Arbeitspaket gehören die relevanten Eingabeversionen und das gelieferte Artefakt.
Vor dem Anwenden erneut vergleichen. Ein fachlich veränderter Eingang macht nur die
abhängigen Teile neu prüfpflichtig; keine blinde Übernahme nach einem sauberen Git-Merge.

Shallow-Water-Exporte nur als abgeschlossenes Paket aus einem neuen Zielordner übergeben.
Die technischen [Paketregeln](antworten/skripte/fluss_sim/README.md) sind die maßgebliche
Detailanleitung. Vor Anwendung `fluss_sim_pruefen.py <Paketordner> --uebergabe` mit den
Daten-/Quelloptionen aus `pruefprofil.json` ausführen. Alte Pakete ohne Profil oder
`quellgeometrie.json` neu exportieren; Dateien nicht mischen und Prüfsummen nicht anpassen.
Bei `--nur` den mitgelieferten Kontext prüfen; das Teilpaket ist keine Projektfreigabe.
Eingaben während Export/Prüfung unverändert halten. Projekt-, Asset- und Editorstand
zusätzlich abgleichen: das Paket bildet nicht sämtliche Eingaben ab.

Paket-ID, Ausgangsstand-ID und Test-ID im Befund verknüpfen. Gleiche Paket-ID plus gleicher
Ausgangsstand und vorhandenes Ergebnis bedeutet: Befund wiederverwenden, auch nach einem
Ordnerwechsel. Ein neuer Ausgangsstand oder begründeter Wiederholungstest erhält eine neue
Test-ID. Die Paket-ID allein bestätigt keine Gültigkeit im Projekt.

Jeder Versuch hat einen Ausführungsstand `vorbereitet → angewendet → geprüft` bzw.
`verworfen/zurückgesetzt`, mit Speicherstatus und Beleg. Nach Abbruch zuerst den tatsächlichen
Projektzustand feststellen: sichern, fortsetzen oder gezielt zurücksetzen. Fehlt nur der
Bericht, den vorhandenen Versuch rekonstruieren; einen angewendeten Eingriff nicht erneut
setzen. Wiederholungen vom bekannten Ausgangsstand ausführen, insbesondere bei Deltas und
Instanzen. Vorhandene Setzer auf ihr Verhalten bei Wiederholung prüfen.

Bei beschädigtem oder teilweise eingebautem Terrain lokal den tatsächlichen Stand klären
und Statusdaten wiederherstellen bzw. passende getrennte Deltas liefern; Details in den
Paketregeln. Ein Delta über erledigte und offene Felder weder vollständig addieren noch
auslassen. Statusdateien nicht löschen/leeren und `--gebaut` oder ausgeschaltete Erkennung
nicht zur Umgehung verwenden. Fehlende Statusdateien gelten technisch weiterhin als
„ungebaut“, daher bleibt der lokale Abgleich nötig. Die Cloud nennt Dateipfad und Fehler
einmal im bestehenden Vorgang; für diese Wiederherstellung keinen neuen Rechercheauftrag
erzeugen.

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
die entscheidende Antwort belegt ist. Zeitablauf ist kein Beleg; offene Fragen bleiben offen.
Vor aufwendigen Versuchen Erfolgs-, Fehler- und Abbruchbedingung festlegen; ungeklärte
Voraussetzungen zuerst kostengünstig prüfen. Lange Builds/Bakes gesondert planen. Nach zwei Runden ohne neue
Erkenntnis Ansatz prüfen, statt dieselbe Frage neu zu stellen. Zurückstellung braucht
einen Wiederaufnahmegrund. Hilfsmittel am konkreten Problem verbessern; kein Großprojekt
zur Prozesspflege starten.
Prozessregeln nur bei einem belegten Ablaufproblem oder auf Ferats Auftrag erweitern.
Nach einem bestandenen gezielten Test wieder am nächsten Wasser-/Bild-Ergebnis arbeiten;
keine weiteren Prüfrunden allein wegen eines unveränderten Status beginnen.

## Startpunkt Shallow Water und Sitzungsabschluss

Aktuell maßgebliche Einstiegspunkte sind die lokalen Befunde
[6i](auftraege/16h-nachtrag6i-baked-sim-tests-stand.md) und
[6j](auftraege/16h-nachtrag6j-teilung-ergebnis.md); spätere passende Belege haben Vorrang.
Die folgenden Zuordnungen beziehen sich auf diese datierten Befunde, nicht auf einen hier
neu geprüften Live-Stand. Korrekturen stehen auch direkt in den betroffenen Altantworten.

| Historischer Ansatz | Weiterarbeiten ab |
| --- | --- |
| [6g §1: SWR-Teilung](antworten/16h-nachtrag6g-uferstufe-simulation.md) | 6i §3 und 6j §1: Flächenannahme widerlegt, Flusskopien verworfen; keine Wiederholung ohne neuen Testgrund. |
| [6h §5.2: Darstellungstests](antworten/16h-nachtrag6h-live-vs-gebacken-dichte.md) | 6i §1: vorhandene Resultate verwenden; optischer Erfolg ist keine vollständige Ursachen-/Laufzeitabnahme. |
| [6h §2: Pixelmessung](antworten/16h-nachtrag6h-live-vs-gebacken-dichte.md) | 6j §2/Nachtrag: Messweg erst kalibrieren, dann Dichteentscheidungen treffen. |

BAKED_SIM ist lokal optisch erfolgreich beschrieben; gepackter Build, Streaming und
GPU-Kosten bleiben gesondert nachzuweisen. Die Teilung mit trockenen Nähten gilt nicht
als fertige Lösung. Vor weiteren Teilungen tatsächliche Engine-Bounds/Quellen/Senken prüfen.
Der [Exporter und Prüfer](antworten/skripte/fluss_sim/README.md) sperren seit 15.10.
Teilungspläne technisch. Formale Prüfung und lokaler Unreal-Nachweis bleiben getrennt.
Bei Änderungen an gemeinsamen Ressourcen auch die betroffenen Vergleichsstellen nach
den [Prüfregeln](vorlagen/pruefung.md#auswirkungen-auf-andere-stellen) kontrollieren.

Am Sitzungsende bzw. im bestehenden Morgenbericht knapp: geliefert, geprüft, offen,
nächster Schritt – jeweils mit Beleg und der dadurch möglichen Entscheidung. Ausführliche
Messdaten einmal ablegen und verlinken. Weitere Zeitsteuerung nur auf ausdrücklichen Auftrag;
für die autorisierte GitHub-Abfrage gelten die oben verlinkten Regeln.
Die Prüfungen sind Arbeitsaufträge für die zuständige Sitzung, keine bereits ausgeführten
Unreal-Tests. Codex hat am 15.10. die sieben Witcher-Zielbilder, die Flussreferenz und den
BAKED_SIM-Vergleich angesehen; dies ist keine Laufzeit- oder Gesamtprojektabnahme.

## Git

Eigene Änderungen gezielt committen; fremde/unzugehörige Änderungen erhalten. Vor Push
`git pull --rebase`; Konflikte unter Erhalt beider Beiträge lösen, kein Force-Push.
Bei API-Schreiben unmittelbar vorher lesen und aktuelle Datei-SHA verwenden. Änderungen
eines zusammengehörigen Arbeitspakets möglichst gemeinsam committen. Ein konfliktfreier
Push ersetzt weder die Eingabeprüfung noch die lokale Abnahme.

Bei Schreibkonflikten aktuelle Gegenfassung lesen und fachlich abgleichen; nicht blind
dieselben Inhalte erneut senden oder widersprüchliche Befunde zusammenkleben. Nur die vom
Konflikt betroffenen Prüfungen wiederholen. Ein Ergebnis gilt erst als im Repository
übergeben, wenn der Push/Schreibvorgang erfolgreich war und die veröffentlichte Version
bestätigt wurde.

Scheitert nur die Veröffentlichung, lokalen Commit/Entwurf und Testbelege erhalten und
„lokal fertig, nicht veröffentlicht“ im verfügbaren Bericht nennen. Beim Wiederanlauf
zuerst nachsehen, ob die Version trotz Verbindungsabbruch schon angekommen ist. Falls
nicht, nach Abgleich nur die Veröffentlichung wiederholen; den Test oder Projekteingriff
nicht deshalb erneut ausführen. Fehlt der neueren Sitzung der lokale Stand, diesen einmal
gezielt beschaffen statt aus einem alten Repositorystand eine Wiederholung abzuleiten.
