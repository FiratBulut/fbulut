# Fable, fünf Opus-Rollen, Cloud-Recherche und Codex

Ferat hat Codex am 17.10.2026 beauftragt, diese Arbeitsteilung festzulegen.
Ziel sind verwendbare Assets und überprüfte UE5.8-Ergebnisse. Fable übernimmt Verantwortung
für das Ergebnis; die Zahl gestarteter Agenten oder erteilter Aufträge ist kein Fortschrittsmaß.
Für Recherche und technische Nachweise gelten weiterhin [README](README.md) und
[Prüfregeln](vorlagen/pruefung.md). Aktuelle Anweisungen und Freigaben Ferats haben Vorrang.

## 1. Rollen und Grenzen

| Rolle | Liefert | Grenze |
| --- | --- | --- |
| **Fable – Projektmanager / primäre Claude-Code-Sitzung** | Priorität, Asset-/Testauftrag, Aufgabenvergabe, Annahme oder konkrete Korrektur, lokale Unreal-Ausführung, Abschlussbericht | Einziger Bediener des laufenden Unreal-Editors; respektiert Ferats aktive Arbeit und bestehende Ausführungsschleifen. |
| **Opus 1 – Technik und Shallow Water** | Lokale Quell-/Datenanalyse, überprüfbare Ursachenabgrenzung, Offline-Testskripte und Parameterpläne; technische Assetvorgaben | Kein eigener paralleler Web-Recherchekreislauf, keine Live-Editor-Steuerung. Fehlende externe Erkenntnisse einmal über Fable an die Cloud. |
| **Opus 2 – Blender-Modellierung** | Maßstäbliche Geometrie, Silhouette, Pivot, benannte Objekte, editierbare `.blend`-Datei und Ansichten | Arbeitet auf dem von Fable angenommenen Bildstand; keine erfundene automatische Bild-zu-3D-Fähigkeit. |
| **Opus 3 – Materialien und Assetaufbereitung** | UVs, Materialien/Texturen, benötigte Kollision/Detailstufen und freigegebener Export aus einer eigenen Folgerevision | Beginnt am übergebenen Modell; bearbeitet nicht gleichzeitig dieselbe `.blend` wie Opus 2. Technische Anforderungen aus dem Auftrag übernehmen. |
| **Opus 4 – Unreal-Integration vorbereiten** | Import-/Platzierungsskripte, Abhängigkeiten, Zielpfade, Wiederherstellungsplan und gezielte Prüfungen | Offline-Vorbereitung; kein `ue.py`, kein Start/Ende des Editors, kein Schreiben in das aktive Unreal-Projekt. Fable führt aus. |
| **Opus 5 – unabhängige Qualitätssicherung** | Sichtprüfung der tatsächlichen Bilder/Modelle, Prüfung der Lieferdateien, Abweichungsliste und Abnahmeempfehlung | Prüft Arbeit anderer; keine eigene Implementierung abnehmen. Laufzeitbehauptungen brauchen von Fable ausgeführte Messungen. |
| **Cloud-Sitzung – Recherche** | Belegte Antworten, Quellen, verwendbare Daten/Versuchsvorschläge nach dem bestehenden Rechercheablauf | Bleibt außerhalb der fünf Subagenten. Fehlender Quellenzugriff wird einmal konkret überbrückt; kein dauerhaftes Hin-und-her. |
| **Codex – Bildlieferant** | Angeforderte Referenz-/Assetbilder als echte Dateien mit Liefernachweis | Bleibt außerhalb der fünf Subagenten; erzeugt durch diese Rolle noch kein Blender-Modell und übernimmt keine Projektleitung. |

Fable und Opus 5.5 sind die **gewünschten Modellbezeichnungen**. Fable prüft beim tatsächlichen
Start, welche Modellkennungen, Agentenplätze und Werkzeuge verfügbar sind, und notiert die
Zuordnung im bestehenden Sitzungsbericht. Nicht verfügbare Modelle einmal melden; einen
Ersatz nur mit Ferats Entscheidung einsetzen. Diese Anleitung konfiguriert keine Modelle.
Die Cloud behält ihre bisherige Sitzung; sie wird nicht automatisch in einen Subagenten umgewandelt.

Fünf feste Rollen, maximal fünf aktive Subagenten; keine weiteren Unteragenten erzeugen.
Fable hält im bestehenden Sitzungsbericht Rolle, tatsächliche Agent-/Sitzungskennung und
offenes Arbeitspaket fest. Eine vorhandene passende Sitzung fortsetzen; kein Duplikat nur
wegen einer neuen Nachricht starten. Beim Neustart aktive Agenten zuerst abgleichen.
Es müssen nicht alle gleichzeitig laufen. Bei Wasserproblemen arbeiten etwa Opus 1 und 4
an getrennten Eingaben, danach Opus 5 an den Belegen. Opus 2/3 werden nur bei benötigten
Assets gestartet. Pro Agent genau ein ausführbares Arbeitspaket; wartende Rollen ruhen.
Fable bündelt Entscheidungen und beseitigt Blockaden, statt jede kleine Handlung erneut
genehmigen zu lassen. Bestehende Freigaben gelten, zusätzliche Ausgaben sind nicht pauschal erlaubt.

## 2. Ein Auftrag, klare Eingaben, eine zuständige Stelle

Fable prüft zuerst vorhandene Ergebnisse, passende Assets und Ferats aktuelle Priorität.
Ein neues Bild ist nur nötig, wenn es eine konkrete Modellierungs-/Gestaltungsentscheidung
verbessert. Eine bereits passende Referenz verwenden; keine Pflicht-Bilderzeugung für jedes Asset.

Für neue Assets legt Fable einmal den [Assetauftrag](vorlagen/asset-auftrag.md) an. Darin:
stabile ID, Revision, Ziel, vorhandene Referenzen, Maße, Abnahmekriterien, benötigte Lieferungen,
zuständige Sitzung und nächste Handlung. Technische Maße kommen aus dem Auftrag, nicht aus
geschätzten Pixelabständen eines generierten Bildes. Nicht sichtbare Rückseiten und Details
als Annahmen kennzeichnen und von Fable vor abhängiger Ausarbeitung entscheiden lassen.

Jeder Subagent erhält nur seinen klaren Ausschnitt: Ziel, unveränderliche Eingabepfade und
SHA-256, erlaubter Schreibbereich, Abhängigkeiten, Ergebnisformat, Kriterien und Aufwandrahmen.
Er prüft seine verfügbaren Werkzeuge vor Beginn. Ohne Blender-Zugriff kann er ein Skript
vorbereiten, aber keine ausgeführte Modellierung melden. Ohne Bildzugriff keine Sichtprüfung.
Fehlt ein entscheidender Eingang, einmal an Fable melden und die betroffene Arbeit ruhen lassen.
Subagenten beauftragen einander nicht: Fable übernimmt das fertige Paket und verteilt weiter.

## 3. Ablage und Schreibrechte

Lokale Assetwurzel für dieses Projekt (bei anderer Maschine einmal im Auftrag zuordnen):

`D:\Das Lied der Asche\ELDARIEN_ENVIRONMENT_SKILLS_V1\production\source\asset_pipeline\`

Diese Ablage wird beim ersten realen Assetauftrag angelegt. Die Struktur ist eine Vorgabe,
kein Nachweis bereits vorhandener Bilder oder Modelle. Repository enthält Regeln/Vorlagen;
Projektbilder, `.blend`, Texturen und Exporte bleiben lokal. Keine privaten Inhalte automatisch
ins öffentliche Recherche-Repository oder zu einem zusätzlichen 3D-Dienst hochladen.

```text
asset_pipeline/<asset-id>/
  auftrag.md                       # nur Fable; einziger maßgeblicher Auftragsstatus
  eingaben/r001/                    # Fable: eingefrorener Bildauftrag/Referenzkopien
  codex/r001/                       # Codex: Bilddateien + lieferung.md
  modell/r001/                      # Opus 2: .blend + Ansichten + lieferung.md
  material/r001/                    # Opus 3: neue .blend + Texturen/Export + lieferung.md
  integration/r001/                 # Opus 4: Skripte/Importplan + lieferung.md
  pruefung/r001/                    # Opus 5: Prüfbericht; Fable: getrennte UE-Belege
```

`r001` ist die Revision der jeweiligen Lieferung, nicht automatisch aller Stufen. Neue
Korrekturen erhalten im betroffenen Bereich `r002` usw.; die vorher angenommene Lieferung
bleibt erhalten. Jede Lieferung benennt ihre tatsächlich verwendeten Eingaben mit Prüfsumme.
Keine unscharfen Verweise auf „latest“. Fable verzeichnet im Auftrag die angenommenen
Revisionen und das nächste Paket. Nur der zuständige Produzent schreibt in seinen Bereich;
Fable legt eigene UE-Belege getrennt unter `pruefung/<revision>/ue-fable/` ab.
Liefernachweise sind Ergebnisbelege, keine zweite Aufgabenliste. Berichte verlinken den Auftrag.
Subagenten committen oder pushen nicht parallel im gemeinsamen Recherche-Checkout.
Fable veröffentlicht zusammengehörige freigegebene Textänderungen nach den Git-Regeln;
lokale Assetdateien bleiben außerhalb dieser Veröffentlichung.

Blender-Dateien, GPU-Bakes und Editor sind exklusive Ressourcen. Fable vergibt ihren Besitzer
vor dem Start; eine Übergabe erfolgt erst nach gespeichertem Ergebnis und beendeter Ausführung.
Kein Timeout gibt eine Ressource frei. Nach Absturz Prozesse und gespeicherten Stand prüfen.
Bei getrennten Arbeitskopien Dateien tatsächlich übertragen und Prüfsummen auf Empfängerseite
prüfen; ein lokaler Pfad allein macht sie für einen anderen Agenten nicht zugänglich.
Diese Regeln sind organisatorisch; eine technische Sperre ist damit noch nicht installiert.

## 4. Bildauftrag von Fable an Codex

1. Fable friert den konkreten Prompt samt Referenzen unter `eingaben/<revision>/` ein.
   Angeben: ID, Revision, Zweck, Objekt, Maße/Proportionen, Stil, Material, benötigte Ansichten,
   Hintergrund/Transparenz, Dateiformat, Zielordner und sichtbare Abnahmekriterien.
   Für Modellierung bevorzugt klare Silhouette, vollständiges Objekt, ruhiger Hintergrund
   und wenig perspektivische Verzerrung. Weitere Ansichten nur, wenn sie eine offene Frage lösen.
2. **Zustellung über GitHub:** Ferat hat am 17.10. die Prüfung alle 30 Minuten autorisiert.
   Fable veröffentlicht den Bildauftrag nach dem [Abfrageprotokoll](codex/README.md).
   Codex hat dafür einen aktiven Zeitplan in diesem Chat. Status bleibt „wartet auf
   Codex-Start“, bis die Bearbeitung tatsächlich beginnt. Ein Push löst keinen sofortigen
   Lauf aus. Bei ausgefallenem Zeitplan kann Ferat denselben Auftrag hier direkt starten;
   vorherige Antworten und lokale Lieferungen dabei ebenfalls auf Doppelarbeit prüfen.
3. Codex liest den tatsächlichen Auftrag und sieht bereitgestellte Referenzbilder an. Prüft
   vor Generierung: gleiche ID + gleicher Eingabestand schon geliefert? Dann vorhandene
   Lieferung verwenden. Ohne andere Vorgabe ein Bild erzeugen; kein unbegrenztes Variantenbudget.
4. Codex nutzt sein verfügbares Bildwerkzeug, speichert das echte Ergebnis im vereinbarten
   `codex/<revision>/` und prüft Öffnen, Format, tatsächliche Pixelmaße und SHA-256.
   [Liefernachweis](vorlagen/asset-lieferung.md) ausfüllen. Fehlt Schreibzugriff auf den Zielordner,
   tatsächliche erreichbare Ergebnisdatei liefern und Transfer als offen markieren.
   Fable bestätigt nach Kopie den lokalen Pfad und dieselbe Prüfsumme.
5. Codex meldet Bildpfad, Auftrag/Revision, Prüfsumme und Abweichungen zurück. Fable sieht
   das Bild selbst an und entscheidet an den vereinbarten Kriterien: annehmen oder gezielte
   Korrektur im selben Auftrag. Erst dann übernimmt Opus 2 genau diese Bildrevision.

Ein schönes Bild ist keine maßhaltige Geometrie. Mehrere generierte Ansichten können sich
widersprechen: Fable benennt die führende Ansicht und lässt entscheidende Widersprüche vor
Modellierung klären. Bilddatei darf nicht einfach in ein 3D-Dateiformat umbenannt werden.
Bildgenerierung liefert keine automatische UV-, Topologie-, Material- oder Kollisionsgarantie.

## 5. Von der Referenz zum verwendbaren Unreal-Asset

| Phase / Status im Auftrag | Zuständig und nötiges Ergebnis für die nächste Phase |
| --- | --- |
| vorbereitet | Fable hat Ziel, Eingaben, Kriterien, Zugriff und nächsten Besitzer geklärt. |
| wartet auf Codex-Start / Bild in Arbeit | Auftrag ist zugestellt bzw. Codex hat tatsächlich begonnen. Keine Blender-Arbeit auf einem noch unbekannten Bildstand. |
| Bild geliefert → Bild angenommen | Datei nachweislich vorhanden und lesbar; Fable hat genau diese Revision visuell geprüft. |
| Modell in Arbeit → Modell angenommen | Opus 2 modelliert in Blender; editierbare Datei lässt sich erneut öffnen. Maße, Silhouette und Ansichten geprüft; Fable übernimmt mit Prüfbeleg. |
| Material/Export in Arbeit → Paket geprüft | Opus 3 liefert Materialien, UVs und benötigte Exportdateien. Opus 5 prüft die tatsächlichen Dateien gegen die Kriterien; Fable entscheidet. |
| Integration vorbereitet → angewendet | Opus 4 liefert Import-/Rücksetzplan; Fable prüft aktuellen Projektstand, sichert Ausgangspunkt und importiert exklusiv in Unreal. |
| im Projekt geprüft → abgeschlossen | Fable liefert reale Projektbilder/Messungen; Opus 5 prüft Kriterien und Referenzen. Fable schließt nur mit technischem und visuellem Ergebnis ab. |
| wartet auf … / Korrektur / verworfen | Fable nennt genau fehlenden Eingang bzw. Mangel, Besitzer und Wiederaufnahmebedingung; keine neue Auftragskette. |

Blender-Abnahme passend zum Asset: Maße/Einheiten, Transform/Pivot, Normalen, Silhouette,
benötigte Topologie, UVs, Materialzuordnung, auflösbare Texturpfade und vereinbarte Detail-/
Kollisionsbudgets. Blender-Version, tatsächliche Exportoptionen und Achsen/Einheiten nennen.
Nur das im Auftrag benötigte Austauschformat liefern; FBX/glTF nicht pauschal beide fordern.
Export separat wieder einlesen und gegen Maße/Materialien prüfen. Externe Texturen im Paket
mitliefern oder nachvollziehbar packen; keine nur auf dem Rechner des Erstellers gültigen Pfade.

Opus 4 darf den Importplan früh auf festen technischen Vorgaben vorbereiten; endgültige
Dateinamen/Prüfsummen und Validierung erst am angenommenen Export festlegen. Opus 3 kann
Materialrezepte unabhängig vorbereiten, aber das Modell erst nach Übergabe verändern.
Fable allein führt Live-Editor- und Projektänderungen aus, auch wenn ein Hilfsagent Zugang hätte.
Bestehende Editoraufträge, Ferats Nutzung, Speicher-/PIE-Regeln und Wiederherstellung beachten.
Ein offline gültiger Export ist noch kein getestetes UE5.8-Asset; Laufzeit, Maßstab, Kollision,
Materialdarstellung und Einfügung in den Zielabschnitt lokal belegen, soweit im Auftrag nötig.

## 6. Fehler, Wiederaufnahme und Ergebnisdruck

- Eine Lieferung wird erst nach vollständigem Speichern geprüft. Eine fehlende oder nicht
  passende Prüfsumme, beschädigte Datei oder veraltete Eingabe blockiert nur abhängige Arbeit.
- Keine pauschale Wiederholung der Pipeline: bei UV-Fehler Opus 3 korrigieren lassen, bei
  Importfehler Opus 4/Fable; ein fertiges Bild dafür nicht erneut generieren.
- Nach Sitzungsabbruch erst Lieferung, laufende Prozesse und tatsächlichen Projektstand
  prüfen. Bereits erfolgten Import nicht noch einmal ausführen, nur weil der Bericht fehlt.
- Fable entzieht/überträgt einen Auftrag ausdrücklich. Bei geänderter Vorgabe laufende
  abhängige Arbeit kontrolliert stoppen; verspätete Lieferung auf ihre alte Revision beziehen.
  Keine angenommene neue Revision überschreiben; verwertbare unabhängige Teile erhalten.
- Höchstens zwei Korrekturrunden ohne messbaren Fortschritt; danach Ursache, Eingaben oder
  Methode ändern bzw. begründet zurückstellen. Kein dritter wortgleicher Auftrag.
- Bei teuren Bildern, Bakes und Renderings vorher Umfang und Stopkriterium festlegen;
  keine nicht verfügbaren Werkzeuge oder zusätzliche bezahlte Dienste als gegeben behandeln.
- Im bestehenden Morgen-/Sitzungsbericht: verwendbare Ergebnisse, Beleg, offene technische
  Grenze, nächster Besitzer/Schritt. Nicht zusätzlich fünf Statusberichte zusammenkopieren.

## 7. Übernahme und erste praktische Probe

Beim nächsten echten Start liest Fable [CLAUDE.md](../CLAUDE.md), diesen Workflow und den
aktiven Vorgang. Startweg und ältere lokale Anweisungen auf diese Arbeitsteilung abgleichen;
die Veröffentlichung allein aktualisiert keine Desktop-Startdateien oder Erinnerungen.
Diese neue Rollenverteilung ersetzt ältere Rollenpläne; bestehende Projekt-, Editor- und
Zugriffsschutzregeln gelten weiter. Für die lokale Übernahme lautet der Einstieg:
`D:\Das Lied der Asche\recherche_repo\CLAUDE.md` und
`D:\Das Lied der Asche\recherche_repo\recherche\TEAM_WORKFLOW.md`.
Tatsächliche Modell-/Werkzeugzuordnung und Codex-Zustellweg im bestehenden Bericht nennen.
Der Codex-Zeitplan ist eingerichtet; der erste geplante Lauf und die Bild-Lieferkette sind
noch praktisch nachzuweisen. Die automatische Ergebnisabfrage bei Fable/Cloud ist damit
nicht installiert. Keine bereits laufenden Subagenten oder getestete Gesamtkopplung behaupten.

Erste Probe: ein tatsächlich benötigtes einfaches Asset aus Ferats Priorität, ein Bild,
ein Blender-Modell, ein Material-/Exportpaket, ein Import in ein geeignetes kleines Testlevel.
Opus 5 prüft die Lieferkette und Fables UE-Beleg. Dabei auch prüfen: unveränderter Auftrag
startet keine zweite Bildgenerierung; eine Korrektur betrifft nur abhängige Stufen; ein
unterbrochener Schritt wird vom gespeicherten Stand fortgesetzt. Im Bericht echte Ergebnisse
und noch ungeprüfte Fälle auseinanderhalten. Bis zu dieser Probe ist der Ablauf definiert,
aber die Modellkonfiguration und durchgehende Ausführung sind noch nicht praktisch bestätigt.
