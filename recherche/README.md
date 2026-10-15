# Zusammenarbeit: Claude Code lokal und Cloud-Sitzung

## Auftrag von Ferat – gültig ab 15.10.2026

Ferat hat Codex beauftragt, den Arbeitsablauf zu korrigieren und effizienter zu machen.
Ferat hat auch die nachfolgenden Ergänzungen zu Inventar, Vorprüfung, Testlevel,
Ergebnisformat und Zeitbudget zur Übernahme in den Arbeitsablauf beauftragt.
**Ziel: mehr überprüfbare Ergebnisse im Unreal-Projekt, weniger gegenseitige Aufträge,
Wiederholungen und lange Antworten ohne Umsetzung.**

Diese Datei ist zu Beginn jeder Sitzung zu lesen. Sie regelt die Zusammenarbeit.
Bestehende Projektregeln und Ferats fachliche Entscheidungen gelten weiter. Diese
Änderung ist keine Freigabe für zusätzliche Dienste, Ausgaben oder destruktive Aktionen.

## Kurzablauf für die nächste Sitzung

1. Neuesten Befund lesen; ein konkretes Ergebnis wählen.
2. **Lokal:** wiederherstellbaren Ausgangsstand sichern und die für diesen Test benötigten
   Messwerkzeuge an bekannten Kontrollfällen prüfen. Belege im bestehenden Vorgang ablegen.
3. **Cloud:** diese Belege auswerten, Beobachtung und Ursachenhypothese trennen und nur
   die entscheidende offene Frage bearbeiten. Zustimmung einer zweiten KI ist kein Beleg.
4. Einen kontrollierten Vergleich durchführen; technische und visuelle Abnahme trennen.
5. Die [Kurzvorlage](#kurzvorlage-für-jede-übergabe) aktualisieren und eine Entscheidung
   festhalten. Bestehende Nachweise verlinken, nicht den gesamten Verlauf wiederholen.

Priorität: belastbare Messung und reproduzierbarer Ausgangsstand vor weiterer Optimierung.
Nicht betroffene Arbeiten können weiterlaufen. Die hier festgelegten Prüfungen sind noch
keine durch Codex ausgeführten Unreal-Tests; Durchführung und Nachweis liegen lokal.

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
   Aktuelles Projektinventar prüfen; bei visuellen Fragen die relevanten Zielbilder
   und aktuellen Projektbilder tatsächlich öffnen (siehe unten).
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

## Verbindliche Ergänzungen ab der nächsten Sitzung

Die folgenden Schritte gehören zum Arbeitsablauf. Vorhandene Werkzeuge und Daten zuerst
verwenden. Fehlende Hilfsmittel lokal schrittweise ergänzen; keinen eigenen großen
Infrastrukturauftrag daraus machen. Diese README legt den Ablauf fest, sie behauptet
nicht, dass Inventarexport, Testlevel oder automatische Prüfungen bereits existieren.

### 1. Aktuelles Projektinventar

Lokal pflegt einen kompakten, möglichst automatisch erzeugten Inventarexport unter
`recherche/auftraege/daten/` und verlinkt ihn im aktiven Vorgang. Er enthält Engine-Build,
relevante Plugins, vorhandene Assets/Materialien mit exakten Pfaden, benötigte APIs und
Parameter sowie wesentliche Einstellungen. Datum und Projekt-/Datenstand mitführen.
Nur bei relevanten Änderungen aktualisieren; nur den benötigten Ausschnitt exportieren.
Die Cloud nutzt diesen Stand und kennzeichnet neu anzulegende Assets ausdrücklich.
Sie darf vorgeschlagene Namen nicht als bereits vorhandene Projektbestandteile behandeln.

### 2. Voraussetzungen prüfen, bevor gebaut wird

Die Cloud liefert ein direkt prüfbares Paket: Ziel, Voraussetzungen, konkrete Änderung
oder verwendbares Artefakt, Test und Erfolgskriterium. Lokal prüft zuerst kostengünstig:
Existieren Parameter, API und Materialien? Ist die vorgeschlagene Funktion im installierten
Build verfügbar? Stimmen Einheiten, Datenstände und tatsächliche Simulationsgrenzen?
Bei einer falschen Voraussetzung den betroffenen Schritt stoppen, den konkreten Befund
zurückmelden und eine belegte Alternative wählen. Keine aufwendige Umsetzung auf bloßer
Annahme starten. Vorhandene lokale Nachweise nicht für jeden Auftrag neu erzeugen.

### 3. Kleines, wiederverwendbares Wasser-Testlevel

Lokal verwendet ein bestehendes geeignetes Testlevel oder richtet eines mit geradem Bach,
steilem Abschnitt, Becken und Übergang ein. Feste Kameras, Beleuchtung, Ausgangsparameter
und Rücksetzstand dokumentieren. Neue technische Varianten zunächst dort prüfen, sofern
der relevante Fehler dort reproduzierbar ist. Falls nicht, einen begrenzten Abschnitt
des echten Projekts verwenden und die Abweichung festhalten.
Ein erfolgreicher Kleintest ist noch keine Projektfreigabe: anschließend am Erlenbach
bzw. betroffenen Gewässer prüfen; Laufzeitfragen zusätzlich im gepackten Build testen.

### 4. Einheitliche Rückmeldung mit Belegen

Die Kurzvorlage unten verwenden; Messdaten soweit bereits verfügbar maschinenlesbar
beilegen. Keine zweite Zusammenfassung mit denselben Angaben anlegen.

Bei Wasserproblemen je nach Test Wasserlauf, nasses Bett/Uferband samt Tiefenschwellen,
Nahtsprünge/trockene Stellen und GPU-Zeit mit Hardware-/Auflösungsbezug erfassen.
Fehlende Messungen nicht als Null oder Erfolg behandeln. Lokal ergänzt nach Bedarf einen
einfachen wiederverwendbaren Prüfer für Pflichtangaben, vorhandene Belegpfade und
Assetreferenzen; die Cloud prüft diese Angaben vor ihrer nächsten Empfehlung.

### 5. Zeitbudget und Ende einer Schleife

Jede Übergabe nennt ein angemessenes Recherche-/Testbudget und ein Abbruchkriterium.
Für eine eng begrenzte Quellenfrage gelten ohne andere Vorgabe zunächst 20 Minuten
Recherche. Bei fehlendem entscheidendem Inhalt dann gezielt einen lokalen Beleg anfordern
oder einen unterscheidenden Test vorbereiten. Lange Builds/Bakes separat abschätzen;
laufende Vorgänge nicht allein wegen dieses Recherchebudgets abbrechen.
Nach zwei erfolglosen Runden ausdrücklich entscheiden: Ansatz ändern, einen brauchbaren
Zwischenstand mit Grenzen übernehmen oder begründet zurückstellen. Ein zurückgestellter
Punkt braucht einen Wiederaufnahmegrund, etwa neue Messdaten oder eine geänderte Version.
Keine weiteren Aufträge mit derselben Frage ohne neue Grundlage erzeugen.

### 6. Messwerkzeuge vor ihrer Verwendung prüfen

Lokal prüft nur die Werkzeuge, deren Zahlen für die nächste Entscheidung gebraucht werden.
Für jedes davon Kontrollfall, unabhängig bekannten Sollwert, vorab festgelegte Toleranz,
Istwert, Werkzeugversion und Gültigkeitsbereich festhalten. Den Sollwert nicht mit genau
dem Algorithmus erzeugen, der geprüft werden soll.

- **Pixelanteile:** zuerst einfache Flächen mit bekanntem sichtbarem Bildanteil sowie
  einen Verdeckungsfall verwenden. Zähler, Nenner, Hintergrund und Klassen explizit
  definieren. Danach relevante Darstellungsarten wie Nanite und Foliage getrennt prüfen.
  Erfolgreiche einfache Geometrie bestätigt noch nicht die Messung dieser Darstellungsarten.
- **Wassertiefe/Uferband:** ein kleines synthetisches Raster mit bekannten Boden- und
  Wasserhöhen prüfen; Einheiten, trockene/ungültige Zellen, Bandzuordnung und Werte direkt
  an den verwendeten Tiefenschwellen berücksichtigen. Danach lokale Stichproben im Projekt
  mit unabhängig abgelesenen Höhen vergleichen.
- **GPU-Zeit:** dieselbe Szene, Hardware, Auflösung und denselben Renderzustand nach
  vergleichbarer Aufwärmphase wiederholt messen. Messumfang und Streuung angeben;
  Unterschiede innerhalb der Streuung nicht als Leistungsgewinn bewerten.

Besteht ein Werkzeug einen relevanten Kontrollfall nicht, betroffene Zahlen als
**nicht belastbar** markieren und daraus keine Optimierungsentscheidung ableiten.
Nur abhängige Entscheidungen warten; qualitative Beobachtungen bleiben als solche nutzbar.
Nach Änderungen am Messweg oder relevanten Engine-/Renderfunktionen betroffene Kontrollen
wiederholen; sonst vorhandene Prüfnachweise wiederverwenden. Die Cloud prüft Methode und
Belege, erklärt aber ungeprüfte Messungen nicht durch bloße Plausibilität für gültig.

### 7. Reproduzierbaren Ausgangsstand sichern

Vor einem Vergleich lokal eine eindeutige Ausgangsstand-ID vergeben und im vorhandenen
Datenbereich ein kurzes Manifest führen: Projektcommit plus uncommittierte Abweichungen,
Engine-/Pluginstand, Karte und relevante Assets, Gelände-/Spline-/Eingabedaten mit Hash
oder eindeutiger Version, Material- und Simulationsparameter, Kameras/Beleuchtung sowie
Reset-, Einschwing- und Bake-Ablauf. Bei Zufallsprozessen den Seed mitführen.
Binäre Projektstände und große Bakes lokal wiederherstellbar sichern; im öffentlichen
Repository genügen zulässige Metadaten und Belege, keine kompletten Projektkopien.

Einmal tatsächlich aus diesem Stand neu laden/zurücksetzen und das Ausgangsergebnis
erneut erfassen. Die Wiederholung muss innerhalb einer vorher festgelegten Toleranz
liegen; andernfalls die Ursache oder die natürliche Streuung klären. „Fünf Minuten
gewartet“ allein beweist keinen eingeschwungenen Zustand: ein zum Versuch passendes
Stabilitätskriterium, etwa stabile Pegel/Front über mehrere Messzeitpunkte, festlegen.

Jede Variante beginnt von diesem Stand; unbeabsichtigte Reständerungen ausschließen.
Nur geplante Einflussgrößen variieren. Einen verbesserten Stand erst nach Abnahme zur
neuen Referenz machen, mit Bezug zur bisherigen ID. Den alten Rücksetzstand erhalten.
Nicht alle historischen Versuche nacharbeiten; mit dem nächsten entscheidenden Test starten.

## Schlussfolgerungen und Zuständigkeit

- **Beobachtung, Erklärung und Entscheidung getrennt schreiben.** „BAKED_SIM zeigt einen
  Wasserkörper“ kann beobachtet sein; „WCBS zeichnet zu tief“ benötigt einen eigenen
  Nachweis. Auch eine wirksame Zwischenlösung bestätigt nicht automatisch ihre Erklärung.
- Für eine Ursachenbehauptung angeben, welcher Test sie von einer plausiblen Alternative
  unterscheidet. Wo dieser fehlt, bleibt die Ursache eine Hypothese. Ein funktionierender
  Zwischenstand darf trotzdem übernommen werden, wenn seine Grenzen klar dokumentiert sind.
- Engine-Verknüpfungen, echte Bounds, Materialgraphen und Ladeverhalten lokal prüfen.
  Die Cloud analysiert diese Nachweise und externe Quellen. Eine Aussage zählt nicht als
  unabhängig bestätigt, wenn beide Sitzungen lediglich dieselbe ursprüngliche Vermutung
  oder denselben Suchauszug wiederholen.
- Pro Vorgang eine Entscheidung bearbeiten. Wasserverhalten/Darstellung → davon abhängige
  Uferanpassung → Dekoration nach Abhängigkeit ordnen. Unabhängige Arbeiten weiterführen;
  gemischte bestehende Nachträge über getrennte Punkte und Belege erschließen, nicht
  durch eine neue Kette gegenseitiger Aufträge vervielfachen.

## Zielbilder sind Teil der Abnahme

- Ferats ausgewählte Zielbilder mit konkreten Pfaden/Links und ihrem Zweck im aktiven
  Vorgang festhalten. „Witcher 4“ oder „Rural Australia“ allein ist kein Abnahmekriterium.
- Vor einer visuellen Empfehlung müssen beide Seiten die relevanten Zielbilder und
  aktuellen Projektbilder tatsächlich ansehen. Falls eine Seite sie nicht öffnen kann,
  einmal gezielt eine zugängliche Darstellung anfordern und „nicht selbst gesehen“
  festhalten. Textberichte und Bildverweise ersetzen keine eigene Bildprüfung.
- Wenige sichtbare Merkmale festlegen: etwa Wasserfarbe und Transparenz, Form der Kolke,
  Schaumverteilung, Uferübergang, Felsmaßstab und Vegetation. Ferats vorhandene Vorgaben
  verwenden; nur bei einer entscheidenden Unklarheit nachfragen.
- Vorher/nachher aus derselben Kamera und Beleuchtung vergleichen. Bei fremden Zielbildern
  Unterschiede in Szene und Blickwinkel berücksichtigen. Technische Messwerte und
  visuelle Zielerreichung getrennt bewerten; höhere Dichte oder feinere Zellen allein
  bedeuten keinen besseren Look. Ohne eigene Bildprüfung kein visuelles Qualitätsurteil.
- Codex hat bei dieser Ablaufkorrektur die Berichte und Bildverweise gelesen, die
  Zielbilder selbst jedoch nicht geprüft. Die bisherigen Empfehlungen zum Ablauf sind
  daher keine Bestätigung der Bildqualität oder der Nähe zum visuellen Ziel.

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

## Kurzvorlage für jede Übergabe

Am Kopf der bestehenden Auftrags- bzw. Antwortdatei aktualisieren. Pro Feld möglichst
ein Satz plus Beleglink; Details und Messdaten darunter oder in vorhandenen Dateien.
„Nicht gemessen“, „nicht gesehen“ oder „noch offen“ statt erfundener Vollständigkeit.
Die lokale Seite pflegt den Ausführungsstand, die Cloud ihre Auswertung und verweist
auf diesen Stand. Keine parallelen widersprüchlichen Statuslisten führen.

```markdown
**ID / Stand:** <ID, Datum, Bezugscommit; Engine-/Inventarlink>
**Status / zuständig:** <offen | in Arbeit | wartet auf Beleg | bereit zum Test | bestätigt | verworfen | zurückgestellt; lokal/Cloud>
**Ziel:** <eine Entscheidung und messbares/visuelles Abnahmekriterium>
**Ausgangsstand:** <Referenz-ID und Manifest; Wiederherstellung geprüft/offen>
**Messung / Bilder:** <Kontrollnachweis und Gültigkeitsbereich; Zielbilder gesehen/nicht gesehen>
**Änderung / Erwartung:** <eine Einflussgröße; erwarteter Unterschied>
**Beobachtung:** <vorher → nachher, Einheit/Schwelle/Streuung; Beleg>
**Erklärung:** <bestätigte Ursache mit unterscheidendem Test oder ausdrücklich Hypothese>
**Entscheidung:** <übernehmen | verwerfen | weiterer Test; gespeichert oder nur im Speicher>
**Ersetzt:** <überholte Empfehlung und Grund, sonst keine>
**Nächster Schritt:** <eine Handlung, zuständige Seite, Budget/Abbruchkriterium; bei Zurückstellung Wiederaufnahmegrund>
```

## Aktueller Stand statt widersprüchlicher Nachträge

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

Reihenfolge für die Einführung: Inventar und Vorprüfung im laufenden Vorgang aktualisieren,
einen wiederherstellbaren Ausgangsstand sichern und benötigte Messwerkzeuge an Kontrollfällen
prüfen; dazu das geeignete Testlevel nutzen oder klein ergänzen. Anschließend den nächsten
entscheidenden Wassertest ausführen. Kurzvorlage und Zeitbudget sofort verwenden.
Diese Vorbereitungen am konkreten Test erledigen; keine vollständige Umstellung abwarten.

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
