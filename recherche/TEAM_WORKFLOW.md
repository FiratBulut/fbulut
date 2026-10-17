# Opus-Projektleitung, fünf Opus-Rollen und Fable-Endprüfung

Ferat hat Codex am 17.10.2026 beauftragt, diese Arbeitsteilung festzulegen.
Seine jüngste Entscheidung ersetzt die frühere Zuordnung: Opus 5.5 leitet das Projekt;
Fable prüft nur vollständig umgesetzte Aufträge abschließend. Damit soll Fable seltener
aufgerufen werden; eine konkrete Kosten-/Limitersparnis ist hier nicht gemessen.
Ziel sind verwendbare Assets und überprüfte UE5.8-Ergebnisse. Opus-PM übernimmt Verantwortung
für das Ergebnis; die Zahl gestarteter Agenten oder erteilter Aufträge ist kein Fortschrittsmaß.
Für Recherche und technische Nachweise gelten weiterhin [README](README.md) und
[Prüfregeln](vorlagen/pruefung.md). Aktuelle Anweisungen und Freigaben Ferats haben Vorrang.

## 1. Rollen und Grenzen

| Rolle | Liefert | Grenze |
| --- | --- | --- |
| **Opus-PM – Opus 5.5, Projektmanager / primäre Claude-Code-Sitzung** | Priorität, Asset-/Testauftrag, Aufgabenvergabe, Annahme von Zwischenlieferungen oder konkrete Korrektur, lokale Unreal-Ausführung, Abschlussbericht | Einziger Bediener des laufenden Unreal-Editors; respektiert Ferats aktive Arbeit und bestehende Ausführungsschleifen. Endgültiger Abschluss nach Fables Endprüfung. |
| **Opus 1 – Technik und Shallow Water** | Lokale Quell-/Datenanalyse, überprüfbare Ursachenabgrenzung, Offline-Testskripte und Parameterpläne; technische Assetvorgaben | Kein eigener paralleler Web-Recherchekreislauf, keine Live-Editor-Steuerung. Fehlende externe Erkenntnisse einmal über Opus-PM an die Cloud. |
| **Opus 2 – Blender-Modellierung** | Maßstäbliche Geometrie, Silhouette, Pivot, benannte Objekte, editierbare `.blend`-Datei und Ansichten | Arbeitet auf dem von Opus-PM angenommenen Bildstand; keine erfundene automatische Bild-zu-3D-Fähigkeit. |
| **Opus 3 – Materialien und Assetaufbereitung** | UVs, Materialien/Texturen, benötigte Kollision/Detailstufen und freigegebener Export aus einer eigenen Folgerevision | Beginnt am übergebenen Modell; bearbeitet nicht gleichzeitig dieselbe `.blend` wie Opus 2. Technische Anforderungen aus dem Auftrag übernehmen. |
| **Opus 4 – Unreal-Integration vorbereiten** | Import-/Platzierungsskripte, Abhängigkeiten, Zielpfade, Wiederherstellungsplan und gezielte Prüfungen | Offline-Vorbereitung; kein `ue.py`, kein Start/Ende des Editors, kein Schreiben in das aktive Unreal-Projekt. Opus-PM führt aus. |
| **Opus 5 – technische Vorprüfung und Belege** | Prüfung der tatsächlichen Lieferdateien, gezielte Zwischenkontrollen, Abweichungsliste und vollständiges Belegpaket für den Projektmanager | Prüft Arbeit anderer; keine eigene Implementierung abnehmen. Laufzeitbehauptungen brauchen von Opus-PM ausgeführte Messungen. Ersetzt nicht Fables Endurteil. |
| **Fable – abschließender Qualitätsmanager** | Ein gebündeltes Urteil zum vollständig umgesetzten Auftrag anhand der vereinbarten Kriterien und echten Belege | Kein laufender Manager, keine Zwischenfreigaben, kein Polling, keine Editorsteuerung. Erst nach dem Abschluss der Umsetzungsarbeit aufrufen. |
| **Cloud-Sitzung – Recherche** | Belegte Antworten, Quellen, verwendbare Daten/Versuchsvorschläge nach dem bestehenden Rechercheablauf | Bleibt außerhalb der fünf Subagenten. Fehlender Quellenzugriff wird einmal konkret überbrückt; kein dauerhaftes Hin-und-her. |
| **Codex – Bildlieferant** | Angeforderte Referenz-/Assetbilder als echte Dateien mit Liefernachweis | Bleibt außerhalb der fünf Subagenten; erzeugt durch diese Rolle noch kein Blender-Modell und übernimmt keine Projektleitung. |

Opus 5.5 und Fable sind die **gewünschten Modellbezeichnungen**; Opus-PM ist die Rollenkennung
des Projektmanagers, kein weiterer Modellname. Opus-PM prüft beim tatsächlichen
Start, welche Modellkennungen, Agentenplätze und Werkzeuge verfügbar sind, und notiert die
Zuordnung im bestehenden Sitzungsbericht. Nicht verfügbare Modelle einmal melden; einen
Ersatz nur mit Ferats Entscheidung einsetzen. Diese Anleitung konfiguriert keine Modelle.
Die Cloud behält ihre bisherige Sitzung; sie wird nicht automatisch in einen Subagenten umgewandelt.

Fünf feste Rollen, maximal fünf aktive Subagenten; keine weiteren Unteragenten erzeugen.
Der Opus-Projektmanager ist zusätzlich zu diesen fünf Rollen vorgesehen. Fable bleibt
außerhalb des operativen Subagententeams und wird erst nach dessen fertiger Lieferung
für die Endprüfung aktiviert. Nicht vorsorglich starten oder dauerhaft mitlaufen lassen.
Opus-PM hält im bestehenden Sitzungsbericht Rolle, tatsächliche Agent-/Sitzungskennung und
offenes Arbeitspaket fest. Eine vorhandene passende Sitzung fortsetzen; kein Duplikat nur
wegen einer neuen Nachricht starten. Beim Neustart aktive Agenten zuerst abgleichen.
Es müssen nicht alle gleichzeitig laufen. Bei Wasserproblemen arbeiten etwa Opus 1 und 4
an getrennten Eingaben, danach Opus 5 an den Belegen. Opus 2/3 werden nur bei benötigten
Assets gestartet. Pro Agent genau ein ausführbares Arbeitspaket; wartende Rollen ruhen.
Opus-PM bündelt Entscheidungen und beseitigt Blockaden, statt jede kleine Handlung erneut
genehmigen zu lassen. Bestehende Freigaben gelten, zusätzliche Ausgaben sind nicht pauschal erlaubt.

## 2. Ein Auftrag, klare Eingaben, eine zuständige Stelle

Opus-PM prüft zuerst vorhandene Ergebnisse, passende Assets und Ferats aktuelle Priorität.
Ein neues Bild ist nur nötig, wenn es eine konkrete Modellierungs-/Gestaltungsentscheidung
verbessert. Eine bereits passende Referenz verwenden; keine Pflicht-Bilderzeugung für jedes Asset.

Für neue Assets legt Opus-PM einmal den [Assetauftrag](vorlagen/asset-auftrag.md) an. Darin:
stabile ID, Revision, Ziel, vorhandene Referenzen, Maße, Abnahmekriterien, benötigte Lieferungen,
zuständige Sitzung und nächste Handlung. Technische Maße kommen aus dem Auftrag, nicht aus
geschätzten Pixelabständen eines generierten Bildes. Nicht sichtbare Rückseiten und Details
als Annahmen kennzeichnen und von Opus-PM vor abhängiger Ausarbeitung entscheiden lassen.

Jeder Subagent erhält nur seinen klaren Ausschnitt: Ziel, unveränderliche Eingabepfade und
SHA-256, erlaubter Schreibbereich, Abhängigkeiten, Ergebnisformat, Kriterien und Aufwandrahmen.
Er prüft seine verfügbaren Werkzeuge vor Beginn. Ohne Blender-Zugriff kann er ein Skript
vorbereiten, aber keine ausgeführte Modellierung melden. Ohne Bildzugriff keine Sichtprüfung.
Fehlt ein entscheidender Eingang, einmal an Opus-PM melden und die betroffene Arbeit ruhen lassen.
Subagenten beauftragen einander nicht: Opus-PM übernimmt das fertige Paket und verteilt weiter.

## 3. Ablage und Schreibrechte

Lokale Assetwurzel für dieses Projekt (bei anderer Maschine einmal im Auftrag zuordnen):

`D:\Das Lied der Asche\ELDARIEN_ENVIRONMENT_SKILLS_V1\production\source\asset_pipeline\`

Diese Ablage wird beim ersten realen Assetauftrag angelegt. Die Struktur ist eine Vorgabe,
kein Nachweis bereits vorhandener Bilder oder Modelle. Repository enthält Regeln/Vorlagen;
Projektbilder, `.blend`, Texturen und Exporte bleiben lokal. Keine privaten Inhalte automatisch
ins öffentliche Recherche-Repository oder zu einem zusätzlichen 3D-Dienst hochladen.

```text
asset_pipeline/<asset-id>/
  auftrag.md                       # nur Opus-PM; einziger maßgeblicher Auftragsstatus
  eingaben/r001/                    # Opus-PM: eingefrorener Bildauftrag/Referenzkopien
  codex/r001/                       # Codex: Bilddateien + lieferung.md
  modell/r001/                      # Opus 2: .blend + Ansichten + lieferung.md
  material/r001/                    # Opus 3: neue .blend + Texturen/Export + lieferung.md
  integration/r001/                 # Opus 4: Skripte/Importplan + lieferung.md
  pruefung/r001/                    # Opus 5: Prüfbericht; Opus-PM: getrennte UE-Belege
  endpruefung/r001/                 # erst am Ende: Fables Urteil zum eingefrorenen Gesamtpaket
```

`r001` ist die Revision der jeweiligen Lieferung, nicht automatisch aller Stufen. Neue
Korrekturen erhalten im betroffenen Bereich `r002` usw.; die vorher angenommene Lieferung
bleibt erhalten. Jede Lieferung benennt ihre tatsächlich verwendeten Eingaben mit Prüfsumme.
Keine unscharfen Verweise auf „latest“. Opus-PM verzeichnet im Auftrag die angenommenen
Revisionen und das nächste Paket. Nur der zuständige Produzent schreibt in seinen Bereich;
Opus-PM legt eigene UE-Belege getrennt unter `pruefung/<revision>/ue-opus-pm/` ab.
Vorhandene Belege unter älteren Pfaden wie `ue-fable/` bleiben gültig, wenn ihr Inhalt zum
geprüften Stand passt; nicht umbenennen oder wiederholen, nur weil die Rollen sich ändern.
Nur Fable schreibt sein Endurteil in `endpruefung/<revision>/`; Opus-PM übernimmt die
Entscheidung anschließend in den Auftrag. Kein zweiter maßgeblicher Auftragsstatus.
Liefernachweise sind Ergebnisbelege, keine zweite Aufgabenliste. Berichte verlinken den Auftrag.
Subagenten committen oder pushen nicht parallel im gemeinsamen Recherche-Checkout.
Opus-PM veröffentlicht zusammengehörige freigegebene Textänderungen nach den Git-Regeln;
lokale Assetdateien bleiben außerhalb dieser Veröffentlichung.

Blender-Dateien, GPU-Bakes und Editor sind exklusive Ressourcen. Opus-PM vergibt ihren Besitzer
vor dem Start; eine Übergabe erfolgt erst nach gespeichertem Ergebnis und beendeter Ausführung.
Kein Timeout gibt eine Ressource frei. Nach Absturz Prozesse und gespeicherten Stand prüfen.
Bei getrennten Arbeitskopien Dateien tatsächlich übertragen und Prüfsummen auf Empfängerseite
prüfen; ein lokaler Pfad allein macht sie für einen anderen Agenten nicht zugänglich.
Diese Regeln sind organisatorisch; eine technische Sperre ist damit noch nicht installiert.

## 4. Bildauftrag von Opus-PM an Codex

1. Opus-PM friert den konkreten Prompt samt Referenzen unter `eingaben/<revision>/` ein.
   Angeben: ID, Revision, Zweck, Objekt, Maße/Proportionen, Stil, Material, benötigte Ansichten,
   Hintergrund/Transparenz, Dateiformat, Zielordner und sichtbare Abnahmekriterien.
   Für Modellierung bevorzugt klare Silhouette, vollständiges Objekt, ruhiger Hintergrund
   und wenig perspektivische Verzerrung. Weitere Ansichten nur, wenn sie eine offene Frage lösen.
2. **Zustellung über GitHub:** Ferat hat am 17.10. die Prüfung alle 30 Minuten autorisiert.
   Opus-PM veröffentlicht den Bildauftrag nach dem [Abfrageprotokoll](codex/README.md).
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
   Opus-PM bestätigt nach Kopie den lokalen Pfad und dieselbe Prüfsumme.
5. Codex meldet Bildpfad, Auftrag/Revision, Prüfsumme und Abweichungen zurück. Opus-PM sieht
   das Bild selbst an und entscheidet an den vereinbarten Kriterien: annehmen oder gezielte
   Korrektur im selben Auftrag. Erst dann übernimmt Opus 2 genau diese Bildrevision.

Ein schönes Bild ist keine maßhaltige Geometrie. Mehrere generierte Ansichten können sich
widersprechen: Opus-PM benennt die führende Ansicht und lässt entscheidende Widersprüche vor
Modellierung klären. Bilddatei darf nicht einfach in ein 3D-Dateiformat umbenannt werden.
Bildgenerierung liefert keine automatische UV-, Topologie-, Material- oder Kollisionsgarantie.

## 5. Von der Referenz zum verwendbaren Unreal-Asset

| Phase / Status im Auftrag | Zuständig und nötiges Ergebnis für die nächste Phase |
| --- | --- |
| vorbereitet | Opus-PM hat Ziel, Eingaben, Kriterien, Zugriff und nächsten Besitzer geklärt. |
| wartet auf Codex-Start / Bild in Arbeit | Auftrag ist zugestellt bzw. Codex hat tatsächlich begonnen. Keine Blender-Arbeit auf einem noch unbekannten Bildstand. |
| Bild geliefert → Bild angenommen | Datei nachweislich vorhanden und lesbar; Opus-PM hat genau diese Revision visuell geprüft. |
| Modell in Arbeit → Modell angenommen | Opus 2 modelliert in Blender; editierbare Datei lässt sich erneut öffnen. Maße, Silhouette und Ansichten geprüft; Opus-PM übernimmt mit Prüfbeleg. |
| Material/Export in Arbeit → Paket geprüft | Opus 3 liefert Materialien, UVs und benötigte Exportdateien. Opus 5 prüft die tatsächlichen Dateien gegen die Kriterien; Opus-PM entscheidet. |
| Integration vorbereitet → angewendet | Opus 4 liefert Import-/Rücksetzplan; Opus-PM prüft aktuellen Projektstand, sichert Ausgangspunkt und importiert exklusiv in Unreal. |
| im Projekt geprüft → umgesetzt – Endprüfung offen | Opus-PM liefert reale Projektbilder/Messungen; Opus 5 prüft Vollständigkeit und technische Kriterien. Erst wenn der ganze Auftrag umgesetzt und belegt ist, übergibt Opus-PM an Fable. |
| Endprüfung → abgeschlossen / Korrektur | Fable bewertet das vollständige Ergebnis. Bei bestandenem Urteil schließt Opus-PM ab; bei konkreten Mängeln vergibt Opus-PM die Korrektur. |
| wartet auf … / Korrektur / verworfen | Opus-PM nennt genau fehlenden Eingang bzw. Mangel, Besitzer und Wiederaufnahmebedingung; keine neue Auftragskette. |

Blender-Abnahme passend zum Asset: Maße/Einheiten, Transform/Pivot, Normalen, Silhouette,
benötigte Topologie, UVs, Materialzuordnung, auflösbare Texturpfade und vereinbarte Detail-/
Kollisionsbudgets. Blender-Version, tatsächliche Exportoptionen und Achsen/Einheiten nennen.
Nur das im Auftrag benötigte Austauschformat liefern; FBX/glTF nicht pauschal beide fordern.
Export separat wieder einlesen und gegen Maße/Materialien prüfen. Externe Texturen im Paket
mitliefern oder nachvollziehbar packen; keine nur auf dem Rechner des Erstellers gültigen Pfade.

Opus 4 darf den Importplan früh auf festen technischen Vorgaben vorbereiten; endgültige
Dateinamen/Prüfsummen und Validierung erst am angenommenen Export festlegen. Opus 3 kann
Materialrezepte unabhängig vorbereiten, aber das Modell erst nach Übergabe verändern.
Opus-PM allein führt Live-Editor- und Projektänderungen aus, auch wenn ein Hilfsagent Zugang hätte.
Bestehende Editoraufträge, Ferats Nutzung, Speicher-/PIE-Regeln und Wiederherstellung beachten.
Ein offline gültiger Export ist noch kein getestetes UE5.8-Asset; Laufzeit, Maßstab, Kollision,
Materialdarstellung und Einfügung in den Zielabschnitt lokal belegen, soweit im Auftrag nötig.

## 6. Fable nur am Ende einsetzen

Opus-PM definiert den Umfang eines vollständigen Auftrags beim Start. Ein einzelnes
Referenzbild, Modell oder Teilpaket innerhalb eines Assetauftrags ist kein Gesamtabschluss.
Eine eigenständige Quellenfrage kann dagegen mit ihrer vollständigen belegten Antwort
umgesetzt sein. Umfang nicht künstlich in Kleinstaufträge aufteilen, um Fable öfter aufzurufen.

Vor Fables Aufruf müssen alle vereinbarten Lieferungen vorliegen, erforderliche lokale
Tests gelaufen und bekannte blockierende Mängel behoben sein. Fehlende Pflichtbelege
beschafft das Opus-Team; Fable wird nicht zum Einsammeln oder zur Fortschrittskontrolle gestartet.
Opus-PM friert ein kompaktes Endpaket ein: Auftrag und Kriterien, angenommene Dateirevisionen
mit Prüfsummen, tatsächliche Testbelege, Ziel-/Ergebnisbilder und bekannte Grenzen. Keine
vollständigen Chatverläufe oder wiederholte Recherche als Standardkontext mitgeben.

Fable prüft den vereinbarten Gesamtumfang, sieht die relevanten Bilder selbst an und liefert
einmal je vollständig vorbereiteter Ergebnisrevision ein Urteil: **bestanden**, **Korrektur
nötig** mit konkretem Kriterium/Beleg oder **nicht beurteilbar** mit fehlendem Nachweis.
Keine unbelegte pauschale Freigabe. Fable implementiert nichts, verteilt keine Subaufträge
und erweitert den Umfang nicht eigenständig. Opus-PM bleibt der einzige Koordinator.

Bei Mängeln bearbeitet das Opus-Team die betroffenen Teile, prüft Auswirkungen und liefert
wieder ein vollständiges korrigiertes Paket. Erst dann Fable erneut aufrufen, mit Fokus auf
die geänderten Kriterien und betroffenen Abhängigkeiten. Keine unveränderte Endprüfung im
30-Minuten-Takt. Ist Fable nicht verfügbar, bleibt der Stand „umgesetzt – Endprüfung offen“;
unabhängige nächste Aufgaben dürfen weiterlaufen. Fable ist kein Voraussetzungsschritt für
Bildgenerierung, Zwischenübergaben oder die GitHub-Abfrage.

## 7. Fehler, Wiederaufnahme und Ergebnisdruck

- Eine Lieferung wird erst nach vollständigem Speichern geprüft. Eine fehlende oder nicht
  passende Prüfsumme, beschädigte Datei oder veraltete Eingabe blockiert nur abhängige Arbeit.
- Keine pauschale Wiederholung der Pipeline: bei UV-Fehler Opus 3 korrigieren lassen, bei
  Importfehler Opus 4/Opus-PM; ein fertiges Bild dafür nicht erneut generieren.
- Nach Sitzungsabbruch erst Lieferung, laufende Prozesse und tatsächlichen Projektstand
  prüfen. Bereits erfolgten Import nicht noch einmal ausführen, nur weil der Bericht fehlt.
- Opus-PM entzieht/überträgt einen Auftrag ausdrücklich. Bei geänderter Vorgabe laufende
  abhängige Arbeit kontrolliert stoppen; verspätete Lieferung auf ihre alte Revision beziehen.
  Keine angenommene neue Revision überschreiben; verwertbare unabhängige Teile erhalten.
- Höchstens zwei Korrekturrunden ohne messbaren Fortschritt; danach Ursache, Eingaben oder
  Methode ändern bzw. begründet zurückstellen. Kein dritter wortgleicher Auftrag.
- Bei teuren Bildern, Bakes und Renderings vorher Umfang und Stopkriterium festlegen;
  keine nicht verfügbaren Werkzeuge oder zusätzliche bezahlte Dienste als gegeben behandeln.
- Im bestehenden Morgen-/Sitzungsbericht: verwendbare Ergebnisse, Beleg, offene technische
  Grenze, nächster Besitzer/Schritt. Nicht zusätzlich fünf Statusberichte zusammenkopieren.

## 8. Übernahme und erste praktische Probe

Beim nächsten echten Start liest Opus-PM [CLAUDE.md](../CLAUDE.md), diesen Workflow und den
aktiven Vorgang. Startweg und ältere lokale Anweisungen auf diese Arbeitsteilung abgleichen;
die Veröffentlichung allein aktualisiert keine Desktop-Startdateien oder Erinnerungen.
Diese neue Rollenverteilung ersetzt ältere Rollenpläne; bestehende Projekt-, Editor- und
Zugriffsschutzregeln gelten weiter. Für die lokale Übernahme lautet der Einstieg:
`D:\Das Lied der Asche\recherche_repo\CLAUDE.md` und
`D:\Das Lied der Asche\recherche_repo\recherche\TEAM_WORKFLOW.md`.
Tatsächliche Modell-/Werkzeugzuordnung und Codex-Zustellweg im bestehenden Bericht nennen.
Der Codex-Zeitplan ist eingerichtet; der erste geplante Lauf und die Bild-Lieferkette sind
noch praktisch nachzuweisen. Die automatische Ergebnisabfrage bei Opus-PM/Cloud ist damit
nicht installiert. Keine bereits laufenden Subagenten oder getestete Gesamtkopplung behaupten.

Erste Probe: ein tatsächlich benötigtes einfaches Asset aus Ferats Priorität, ein Bild,
ein Blender-Modell, ein Material-/Exportpaket, ein Import in ein geeignetes kleines Testlevel.
Opus 5 prüft die Lieferkette und Opus-PMs UE-Beleg. Dabei auch prüfen: unveränderter Auftrag
startet keine zweite Bildgenerierung; eine Korrektur betrifft nur abhängige Stufen; ein
unterbrochener Schritt wird vom gespeicherten Stand fortgesetzt. Fable erhält erst das
vollständige Endpaket; sein Urteil ist der letzte Abnahmeschritt. Im Bericht echte Ergebnisse
und noch ungeprüfte Fälle auseinanderhalten. Bis zu dieser Probe ist der Ablauf definiert,
aber die Modellkonfiguration und durchgehende Ausführung sind noch nicht praktisch bestätigt.
