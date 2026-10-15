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
