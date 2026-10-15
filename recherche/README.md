# Zusammenarbeit: Claude Code lokal und Cloud-Sitzung

## Auftrag von Ferat – gültig ab 15.10.2026

Ferat hat Codex beauftragt, den Arbeitsablauf zu korrigieren und effizienter zu machen.
**Ziel: mehr überprüfbare Ergebnisse im Unreal-Projekt, weniger gegenseitige Aufträge,
Wiederholungen und lange Antworten ohne Umsetzung.**

Diese Datei ist zu Beginn jeder Sitzung zu lesen. Sie regelt die Zusammenarbeit.
Bestehende Projektregeln und Ferats fachliche Entscheidungen gelten weiter. Diese
Änderung ist keine Freigabe für zusätzliche Dienste, Ausgaben oder destruktive Aktionen.

## Rollen und Übergabe

- **Claude Code lokal** hat Zugriff auf das Projekt und die installierte Engine.
  Es prüft APIs und Assets, setzt freigegebene Lösungen um, testet in Unreal und liefert
  Messwerte, Bilder und den tatsächlichen Umsetzungsstand.
- **Cloud-Sitzung** recherchiert, prüft Quellen und bereitgestellte Daten, wertet Befunde
  aus und liefert konkrete Entscheidungen, verwendbare Artefakte oder kurze Testpläne.
  Alles, was sie mit ihren vorhandenen Werkzeugen selbst erledigen kann, erledigt sie selbst.
- GitHub ist gemeinsame Ablage und Gedächtnis. Austauschbranch:
  `claude/recherche-auftrag-s5m3y6`. Keine Übergaben auf beliebige andere Branches.
- Lokale Übergaben stehen unter `recherche/auftraege/<id>.md`, Cloud-Antworten unter
  `recherche/antworten/<id>.md`. Der gleiche Dateiname verbindet beide Seiten.
  Vorhandene Daten-, Bilder- und Artefaktpfade weiterverwenden und konkret verlinken.

## Start jeder Sitzung

1. Aktuellen Branchstand holen und diese README lesen.
2. Zum bearbeiteten Problem den **neuesten lokalen Befund und die neueste Cloud-Antwort**
   lesen, einschließlich Nachträgen. Nicht allein vom ursprünglichen Auftrag ausgehen.
3. Prüfen, ob die letzte Antwort bereits getestet, widerlegt oder durch einen neueren
   Befund ersetzt wurde. Bereits erledigte Arbeit nicht erneut beauftragen.
4. Den nächsten Schritt nach seinem Nutzen wählen: einen konkreten Fehler beheben,
   eine entscheidende Unsicherheit klären oder ein verwendbares Ergebnis liefern.
   Pro Problem nur einen aktiven Übergabevorgang führen.

## Arbeitszyklus: Ergebnis vor neuem Auftrag

1. **Lokal beschreibt die Entscheidung**, die fehlt: Ziel, Istzustand, bereits getestete
   Varianten, Einschränkungen und messbares Erfolgskriterium. Nur notwendige Belege beifügen.
2. **Cloud prüft zuerst vorhandene Befunde.** Danach nur die noch offene Frage recherchieren.
   Antwortbeginn: Ergebnis, Beleg, konkrete nächste Handlung. Wenn Daten und Befugnisse
   ausreichen, das benötigte Artefakt direkt mitliefern, statt seine Erstellung zurückzugeben.
3. **Lokal führt den entscheidenden Test bzw. die Umsetzung aus** und meldet knapp:
   Änderung, Ergebnis gegenüber dem Ausgangszustand, bestanden/nicht bestanden, gespeichert
   oder nur im Speicher getestet, zugehörige Belege.
4. **Cloud gleicht Erwartung und Ergebnis ab.** Widerlegte Annahmen zurückziehen und die
   aktuelle Empfehlung korrigieren. Keine erneute Empfehlung derselben gescheiterten
   Variante ohne neue Evidenz und eine ausdrücklich benannte Änderung.
5. Erfüllt das Ergebnis das vereinbarte Kriterium, Vorgang abschließen. Andernfalls den
   nächsten unterscheidenden Test wählen. Nach zwei erfolglosen Runden zuerst Ursachen,
   Voraussetzungen und bisherigen Ansatz überprüfen, bevor weitere Parameter probiert werden.

Rückfragen nur stellen, wenn ihre Antwort den nächsten Schritt tatsächlich verändert.
Zusammengehörige Fragen bündeln; unabhängige Arbeit währenddessen fortsetzen. Ferat nur
für fehlende Zielentscheidungen oder tatsächlich erforderliche Freigaben einbeziehen.
Bereits autorisierte Schritte nicht erneut zur Entscheidung vorlegen.

## Wenn die Cloud Quellen nicht öffnen kann

Bisherige Antworten dokumentieren Zugriffsprobleme auf Epic-Dokumentation und Foren.
Das ist eine Einschränkung der jeweiligen Sitzung, keine allgemeine Aussage, dass
diese Quellen immer unzugänglich sind.

- Den direkten Abruf prüfen. Bei Fehlschlag einen verfügbaren alternativen Zugang
  versuchen; anschließend die Zugriffslücke dokumentieren. Keine wiederholten identischen
  Abrufversuche ohne geänderte Voraussetzung.
- Suchauszüge ausschließlich als **Hinweis** kennzeichnen. Daraus weder verifizierte
  UE5.8-Funktionen noch abschließende Fehlerursachen oder exakte API-Namen ableiten.
- Wenn der Inhalt entscheidend fehlt, **einmal gezielt lokal anfordern**:
  genaue URL, benötigter Abschnitt und die damit zu klärende Frage.
- Lokal liefert eine knappe Zusammenfassung mit URL, Datum, Versionsbezug und relevanten
  Angaben; nötigenfalls einen zulässigen kurzen Auszug oder einen eigenen Engine-/Graph-Dump.
  Keine Zugangsdaten oder vertraulichen Inhalte ins öffentliche Repository stellen.
- Beide Seiten verwenden diese Belege anschließend erneut. Nicht dieselbe Quelle in jeder
  Runde neu anfordern. Bei veränderter Engine-Version die Gültigkeit neu prüfen.
- Forumsthreads vollständig bis zu den neuesten relevanten Beiträgen lesen:
  spätere Korrekturen können die ursprüngliche Empfehlung aufheben.
- Jede technische Schlussfolgerung als **lokal bestätigt**, **Quelle bestätigt**,
  **Hypothese**, **widerlegt** oder **offen** kennzeichnen. Fremde Tests bestätigen
  nicht automatisch das Verhalten im eigenen Projekt.

## Aktueller Stand statt widersprüchlicher Nachträge

Am Anfang beider Übergabedateien steht eine kurze, aktualisierte Übersicht:

| Feld | Inhalt |
|---|---|
| ID / Bezug | Stabile ID, relevante Dateien und Commitstände |
| Ziel | Konkretes Ergebnis und Abnahmekriterium |
| Stand | Datum, exakte Engine-Version/Build, relevante Plugins |
| Status | offen / in Arbeit / wartet auf Beleg / bereit zum Test / bestätigt / verworfen |
| Verantwortlich | lokal oder Cloud; nächster konkreter Schritt |
| Gültiger Befund | Was heute gilt, mit Beleg |
| Widerlegt / ersetzt | Welche frühere Aussage nicht mehr gilt und warum |

**Eine vorhandene Antwortdatei bedeutet nur „beantwortet“, nicht „erledigt“.**
Bei einer Umsetzung bestätigt lokal den Abschluss anhand des Tests. Bei reiner Recherche
genügt die belegte Beantwortung der vereinbarten Frage; eine offene Rückfrage genügt nicht.

Rückmeldungen zum selben Problem in den bestehenden Dateien fortführen. Neue IDs nur für
eigenständige Probleme. Bestehende Nachtragsketten nicht umbenennen: am Kopf auf den aktuell
maßgeblichen Befund verweisen. Alte Aussagen bleiben als Verlauf erhalten, müssen aber
sichtbar als überholt markiert werden. Die nächste Sitzung soll den gültigen Stand verstehen,
ohne die gesamte Geschichte erneut auszuwerten.

## UE5.8 Shallow Water: nächste Arbeit und Prüfregeln

Zuerst die jeweils neuesten Befunde prüfen. Ausgangspunkt dieser Ablaufkorrektur sind
`auftraege/16h-nachtrag6i-baked-sim-tests-stand.md` und
`auftraege/16h-nachtrag6j-teilung-ergebnis.md` sowie die Antworten 6g und 6h.
Neuere Ergebnisse haben Vorrang.

- **Darstellung zuerst absichern:** Der lokale Bericht beschreibt BAKED_SIM als optisch
  erfolgreich. Daraus folgt noch keine bestätigte Laufzeitlösung. Darstellung im gepackten
  Build, Laden/Entladen durch World Partition, Materialparameter nach dem Laden und
  tatsächliche GPU-Kosten prüfen. Alte Zeitmessungen nur mit ihrem Hardware-, Szenen-
  und Auflösungsbezug verwenden; keine pauschale Anzahl zulässiger Flüsse daraus ableiten.
- **Simulation getrennt untersuchen:** Der Teilungstest verbessert das nasse Uferband,
  erzeugt aber Stillstand und trockene Nähte. Er gilt deshalb nicht als fertige Lösung.
  Vor weiteren Teilungsvarianten tatsächliche Engine-Bounds, Quellen/Senken und Übergänge
  anhand der lokalen Implementierung prüfen.
- **Kontrollierte Tests:** Darstellung, Material, Nachfüllrate, Auflösung und Gelände
  getrennt untersuchen. Je Vergleich eine Einflussgröße ändern; sonst den kombinierten
  Versuch ausdrücklich kennzeichnen. Gleiche Kameras, Beleuchtung, Ausgangsdaten und
  vergleichbaren eingeschwungenen Zustand verwenden.
- **Kurzes Testprotokoll:** Hypothese → Änderung → erwarteter Unterschied → gemessener
  Unterschied → Entscheidung. Dazu Parameter, Commit/Datenstand, Reset-/Bake-Ablauf und
  Bilder bzw. Messdaten verlinken.
- **Gemeinsame Kriterien:** vollständiger Wasserlauf, nasses Bett/Uferband mit identischen
  Tiefenschwellen, Nahtsprünge und trockene Stellen, Bildqualität sowie Laufzeitkosten.
  Numerische Schwellen als Projektziele kennzeichnen, nicht als garantierte Engine-Grenzen.
- Uferdekoration und weitere großflächige Anpassungen erst auf einen ausreichend
  bestätigten Wasserstand aufbauen. Keine wiederholten Materialkorrekturen, wenn die
  offene Frage tatsächlich den Zeichenweg oder die Simulationshöhe betrifft.

## Kurzer Sitzungsabschluss / bestehender Morgenbericht

Jede Sitzung hinterlässt höchstens einige Punkte zum aktuellen Stand:

- **Geliefert:** verwendbare Ergebnisse mit Datei-/Commitbezug.
- **Geprüft:** Test und tatsächlicher Befund; auch negative Ergebnisse zählen, wenn sie
  eine Hypothese ausschließen.
- **Offen:** konkrete verbleibende Unsicherheit und zuständige Seite.
- **Als Nächstes:** eine priorisierte Handlung mit Erfolgskriterium.

Anzahl geschriebener Aufträge, Antwortlänge und Recherchemenge sind keine Erfolgsmaße.
Entscheidend sind bestätigte Lösungen, ausgeschlossene Ursachen und nutzbare Artefakte.
Diese Regel beschreibt auch den Inhalt eines bestehenden Morgenberichts; sie richtet
keine neue Zeitsteuerung oder automatische Sitzung ein.

## Schreib- und Git-Regeln

- Lokal pflegt seine Auftrags-/Befunddateien, Cloud ihre Antwortdateien.
  Vorhandene Zuständigkeiten für weitere Artefakte beibehalten.
- Dateinamen in Kleinbuchstaben mit Bindestrichen; vorhandene Pfade nicht unnötig ändern.
- Bei Git-Nutzung vor dem Push `git pull --rebase`; bei Konflikten die Änderungen beider
  Seiten erhalten und zusammenführen. Keine erzwungenen Pushes.
- Bei GitHub-API-Änderungen unmittelbar vorher die Datei lesen und ihre aktuelle SHA
  verwenden; bei einem Versionskonflikt neu lesen und zusammenführen.
- Ein Git-Push startet allein keine neue KI-Sitzung. Ausführung und Abruf erfolgen über
  die bereits vorhandene Sitzung bzw. deren eingerichteten Ablauf.
