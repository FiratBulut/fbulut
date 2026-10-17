# Lokaler Assetauftrag – Vorlage

Opus-PM kopiert diese Vorlage einmal nach `<Assetwurzel>/<asset-id>/auftrag.md`.
Nur benötigte Felder ausfüllen; Pflichtangaben für den aktuellen Schritt nicht erraten.
Es gilt der [Teamworkflow](../TEAM_WORKFLOW.md). Nur Opus-PM pflegt den Auftragsstatus.
Diese Vorlage ist kein gestarteter Auftrag.

## Auftrag und nächster Schritt

- ID / Auftragsrevision / Datum:
- Opus-PM-Sitzung / Ferats Ziel / Priorität:
- Status / nächste ausführbare Handlung / zuständige Sitzung und tatsächliches Modell:
- Erlaubter Schreibbereich / exklusive Ressource und Besitzer:
- Abhängigkeiten / konkreter Blocker / Wiederaufnahmebedingung:
- Aufwandrahmen / erlaubte Bildanzahl / Abbruchkriterium:

## Asset und Abnahme

- Verwendung im Projekt / Zielpfad / benötigter Ausschnitt:
- Vorhandene Assets geprüft / warum Neuanfertigung nötig:
- Objekt / Maße und Einheit / Pivot / relevante technische Budgets:
- Stil / Materialien / sichtbare Kriterien:
- Referenzdateien mit SHA-256 / führende Ansicht / bekannte Widersprüche:
- Offene Rückseiten/Details und entschiedene Annahmen:
- Benötigte Lieferungen (.blend, Austauschformat, Texturen, Ansichten):
- Benötigte UE-Prüfungen / sichtbare Erfolgskriterien / Wiederherstellungsplan:

## Konkreter Auftrag an Codex

Den folgenden ausgefüllten Abschnitt samt erreichbaren Eingaben zustellen, nicht nur einen
Ordnerpfad nennen. Eingabestand vor Zustellung unter `eingaben/<revision>/bildauftrag.md`
einfrieren. Einen bestehenden identischen Auftrag nicht erneut auslösen.
Für die von Ferat autorisierte 30-Minuten-Abfrage auf GitHub nach dem
[Abfrageprotokoll](../codex/README.md) veröffentlichen; genau eine Sitzung als
Ergebnisempfänger benennen. Eine Veröffentlichung ist noch kein Bearbeitungsbeginn.

> Erzeuge für Asset [ID] auf Basis der Eingaberevision [Revision / SHA-256 des Bildauftrags]
> [Anzahl] Referenzbild(er) für die Modellierung in Blender.
> Motiv und Proportionen: […]. Stil und Materialien: […].
> Referenzen (tatsächlich erreichbare Dateien): […].
> Benötigte Ansicht(en), Hintergrund/Transparenz und Bildformat: […].
> Sichtbare Abnahmekriterien: […]. Ungewünschte Elemente: […].
> Speichere die Bilddatei(en) unter [absoluter Zielpfad codex/Revision/].
> Prüfe Lesbarkeit und liefere Dateipfad, tatsächliche Pixelmaße, SHA-256, verwendete
> Eingaberevision und Abweichungen in lieferung.md. Ist genau dieser Auftrag bereits
> geliefert, verwende die bestehende Lieferung. Melde fehlenden Zugriff konkret.

Die SHA-256 des Bildauftrags wird außerhalb der eingefrorenen Datei im Zustelltext ergänzt;
eine Datei enthält nicht ihre eigene Prüfsumme. Referenzdateien separat identifizieren.

## Annahmen und Übergaben – von Opus-PM fortführen

| Stufe | Angenommene Lieferung / Pfad / SHA-256 | Prüfer und Beleg | Entscheidung / nächster Besitzer |
| --- | --- | --- | --- |
| Bild | | | |
| Modell | | | |
| Material/Export | | | |
| Integration | | | |
| Projektabnahme | | | |
| Fable-Endprüfung des gesamten Auftrags | | | |

Fable erst aufrufen, wenn die gesamte vereinbarte Umsetzung samt Pflichtprüfungen geliefert
ist. Opus-PM hält bis dahin „umgesetzt – Endprüfung offen“ fest. Für Fable ein kompaktes
vollständiges Paket mit Kriterien, Dateirevisionen, Belegen und bekannten Grenzen verlinken.
Nach bestandenem Endurteil abschließen; Korrekturen weiterhin durch Opus-PM vergeben.

Korrekturen hier mit Mangel, betroffener Revision und Besitzer ergänzen. Alte angenommene
Stände nachvollziehbar erhalten. Bei geänderten Eingaben nur betroffene Stufen erneut prüfen.
Forschungsfrage bei Bedarf als Link auf den bestehenden Recherchevorgang, ohne Statuskopie.
