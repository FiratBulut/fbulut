# Prüfregeln für Umsetzungstests

Zum [Arbeitsablauf](../README.md). Diese Regeln nur auf betroffene Umsetzungstests anwenden,
nicht auf reine Quellenfragen. Vorhandene Prüfnachweise verwenden, solange Messweg,
Engine-/Renderfunktionen und relevante Daten unverändert sind. Durchführung liegt lokal;
die Cloud prüft die gelieferten Belege. Diese Datei ist kein Nachweis ausgeführter Tests.

## Wiederherstellbarer Ausgangsstand

Im vorhandenen Datenbereich ein kurzes Manifest mit Ausgangsstand-ID führen:
Projektcommit plus uncommittierte Abweichungen, Engine-/Pluginstand, Karte/relevante Assets,
Gelände-/Spline-/Eingabeversionen oder Hashes, Material-/Simulationsparameter, Kamera,
Beleuchtung und Reset-/Bake-Ablauf; Zufalls-Seed, falls verwendet. Große Projektstände/Bakes
lokal wiederherstellbar sichern, öffentlich nur zulässige Metadaten und Belege ablegen.

Einmal neu laden/zurücksetzen und das Ausgangsergebnis erneut erfassen. Vorab Toleranz
festlegen, natürliche Streuung berücksichtigen. Eine feste Wartezeit beweist noch keinen
eingeschwungenen Zustand: passendes Stabilitätskriterium wie stabile Pegel/Front über
mehrere Messzeitpunkte verwenden.

Jede Variante beginnt vom benannten Stand und ändert möglichst eine Einflussgröße.
Kombinierte Versuche ausdrücklich kennzeichnen. Eine neue Referenz erst nach Abnahme
festlegen, alte Sicherung erhalten. Vor jeder Anwendung relevante Eingabeversionen erneut
vergleichen; nach Abbruch echten Ausführungsstand prüfen, bevor fortgesetzt wird.

## Messwerkzeuge

Nur benötigte Werkzeuge an Kontrollfällen prüfen. Dokumentieren: unabhängig bekannter
Sollwert, vorab festgelegte Toleranz, Istwert, Werkzeugversion und Gültigkeitsbereich.
Den Sollwert nicht mit demselben Algorithmus erzeugen, den der Test prüfen soll.

- **Pixelanteile:** einfache Flächen mit bekanntem sichtbarem Anteil und Verdeckungsfall;
  Zähler, Nenner, Hintergrund und Klassen definieren. Danach Nanite/Foliage prüfen, soweit
  verwendet. Ein bestandener einfacher Fall bestätigt nicht automatisch andere Renderwege.
- **Wassertiefe/Uferband:** synthetisches Raster mit bekannten Boden-/Wasserhöhen, Einheiten,
  trockenen/ungültigen Zellen, Bandzuordnung und Tiefenschwellen. Danach Stichproben im
  Projekt mit unabhängig abgelesenen Höhen vergleichen.
- **GPU-Zeit:** gleiche Szene, Hardware, Auflösung und Renderzustand nach vergleichbarem
  Aufwärmen wiederholt messen. Messumfang und Streuung nennen; Unterschiede innerhalb
  dieser Streuung nicht als Leistungsgewinn ausgeben.

Bei Fehlern betroffene Zahlen als „nicht belastbar“ markieren; keine davon abhängige
Optimierungsentscheidung. Andere Arbeit und ausdrücklich qualitative Beobachtungen bleiben
möglich. Nach relevanten Änderungen nur betroffene Kontrollen wiederholen.

## Vom Kontrollfall zum Projekt

Vorhandenes Wasser-Testlevel mit geradem Bach, steilem Abschnitt, Becken und Übergang
verwenden oder nur den benötigten Fall ergänzen. Ist der Fehler dort nicht reproduzierbar,
einen begrenzten echten Projektabschnitt testen und die Unterschiede dokumentieren.
Erfolge anschließend im betroffenen Gewässer bestätigen; Laufzeitfragen auch im gepackten
Build und beim relevanten Streaming-/Ladeablauf prüfen.

Je nach Fragestellung vollständigen Wasserlauf, nasses Bett/Uferband mit identischen
Tiefenschwellen, Nahtsprünge/trockene Stellen, Bildqualität und Kosten erfassen. Fehlende
Messung heißt „nicht gemessen“, nicht Null oder bestanden. Zahlenziele sind Projektziele,
keine garantierten Engine-Grenzen.

Technisch erfolgreich und visuell gelungen getrennt beurteilen. Am nächsten kurzen
Bachabschnitt müssen passende Referenzbilder und wenige sichtbare Kriterien die
Gestaltungsentscheidung tragen. Statische Bilder belegen weder Strömung noch Laufzeitkosten.

## Auswirkungen auf andere Stellen

Vor Änderungen an gemeinsam genutzten Materialien, Wasserzonen, Kollisionsregeln oder
Exportparametern deren betroffene Nutzer/Flächen ermitteln. Neben dem Zielabschnitt wenige
aussagekräftige Vergleichsstellen wählen: den angeschlossenen Übergang oder die Mündung,
einen weiteren Nutzer derselben Ressource und, soweit verfügbar, eine unveränderte
Kontrollstelle. Fehlt eine passende Stelle, die Prüflücke nennen.

Für Ziel und Vergleichsstellen vorher dieselben relevanten Kriterien und Toleranzen
festlegen. Vom gesicherten Ausgangsstand vor/nach der Änderung unter gleichen Bedingungen
prüfen: je nach Änderung Wasserlauf/Naht, Pegel/Uferband, Bild oder GPU-Zeit. Bei gemeinsamem
Material auch dessen weitere relevante Varianten prüfen; bei Zonen die betroffenen
Gewässer und Ladegrenzen. Unabhängige Bereiche brauchen keinen erneuten Volltest.

Eine Verbesserung am Ziel bei Verschlechterung einer betroffenen Vergleichsstelle ist
keine bestandene Abnahme. Ursache eingrenzen, Änderung lokal begrenzen oder zurücksetzen;
einen gewünschten Kompromiss ausdrücklich mit Ferat entscheiden. In der vorhandenen
Übergabe betroffene Stellen, Ergebnisse und verbleibende Prüflücken verlinken.

## Ablaufprobe für die Sitzungsübergabe

Diese Fälle beschreiben das erwartete Verhalten, keine hier ausgeführten Sitzungs- oder
Unreal-Tests. Beim nächsten lokalen Start den vorhandenen Start-/Abfrageweg mit einer
harmlosen Änderung prüfen. Unterbrechungen in einer Testkopie bzw. anhand gespeicherter
Belege nachstellen, nicht durch Abbruch eines produktiven Bakes. Den Nachweis im vorhandenen
Bericht festhalten; keine dauerhafte neue Prüfroutine daraus machen.

| Fall | Erwartetes Verhalten |
| --- | --- |
| Bestehende Antwort erhält einen neuen fachlichen Befund. | Inhalt und Revision erkennen, die nächste Entscheidung bearbeiten; nicht nur neue Dateinamen suchen. |
| Nur Lesebestätigung oder Formatierung ändert sich. | Kein neuer Test und keine Gegenquittung. |
| Zweite Sitzung beginnt am selben Asset/Teststand. | Bestehenden Bearbeiter beachten; keine zweite Ausführung starten, unabhängig arbeiten. |
| Alte Sitzung scheint inaktiv. | Prozesse und letzten gespeicherten Stand prüfen; kein automatisches Übernehmen nach Zeitablauf. |
| Ergebnis stammt aus einer inzwischen ersetzten Eingabeversion. | Ergebnis an alte Basis binden und Anwendbarkeit klären; neueren Befund nicht überschreiben. |
| Test ist durchgeführt, Push scheitert oder Verbindung bricht ab. | Beleg lokal erhalten, Remote-Stand prüfen und nötigenfalls nur Veröffentlichung wiederholen. |
| Eingriff ist angewendet, Ergebnisbericht fehlt nach Neustart. | Tatsächlichen Zustand und Test-ID rekonstruieren, Eingriff nicht nochmals anwenden. |
| Cloud erreicht Quelle oder Zielbild nicht. | Zugriffslücke einmal konkret benennen; unabhängig weiterarbeiten, keine Quellen-/Bildbestätigung erfinden. |
| Derselbe Blocker bleibt unverändert. | Auf den benannten Eingang warten; keine neue Auftragsschleife oder bloße Statusänderung erzeugen. |

Bestehen heißt: der echte Sitzungsweg zeigt die erwartete Entscheidung und liefert einen
nachvollziehbaren Beleg. Das Lesen dieser Tabelle oder grüne Exporter-Tests genügen nicht.
