# Opus-Projektleitung, fünf Fachrollen und Fable-Endprüfung

Ferat hat Codex am 17.10.2026 beauftragt, diese Arbeitsteilung festzulegen.
Seine jüngste Entscheidung ersetzt die frühere Zuordnung: Opus 5.5 leitet das Projekt;
Fable prüft nur vollständig umgesetzte Aufträge abschließend. Damit soll Fable seltener
aufgerufen werden; eine konkrete Kosten-/Limitersparnis ist hier nicht gemessen.
Ferat hat zusätzlich Sonnet 5.5 für einfachere Aufgaben innerhalb der fünf bestehenden
Subagenten-Plätze freigegeben. Die Fachrolle bleibt gleich; das Modell wird pro Paket gewählt.
Ziel sind verwendbare Assets und überprüfte UE5.8-Ergebnisse. Opus-PM übernimmt Verantwortung
für das Ergebnis; die Zahl gestarteter Agenten oder erteilter Aufträge ist kein Fortschrittsmaß.
Für Recherche und technische Nachweise gelten weiterhin [README](README.md) und
[Prüfregeln](vorlagen/pruefung.md). Aktuelle Anweisungen und Freigaben Ferats haben Vorrang.

## 1. Rollen und Grenzen

| Rolle | Liefert | Grenze |
| --- | --- | --- |
| **Opus-PM – Opus 5.5, Projektmanager / primäre Claude-Code-Sitzung** | Priorität, Asset-/Testauftrag, Aufgabenvergabe, Annahme von Zwischenlieferungen oder konkrete Korrektur, lokale Unreal-Ausführung, Abschlussbericht | Einziger Bediener des laufenden Unreal-Editors; respektiert Ferats aktive Arbeit und bestehende Ausführungsschleifen. Endgültiger Abschluss nach Fables Endprüfung. |
| **Rolle 1 – Technik und Shallow Water** | Lokale Quell-/Datenanalyse, überprüfbare Ursachenabgrenzung, Offline-Testskripte und Parameterpläne; technische Assetvorgaben | Kein eigener paralleler Web-Recherchekreislauf, keine Live-Editor-Steuerung. Fehlende externe Erkenntnisse einmal über Opus-PM an die Cloud. |
| **Rolle 2 – Blender-Modellierung** | Maßstäbliche Geometrie, Silhouette, Pivot, benannte Objekte, editierbare `.blend`-Datei und Ansichten | Arbeitet auf dem von Opus-PM angenommenen Bildstand; keine erfundene automatische Bild-zu-3D-Fähigkeit. |
| **Rolle 3 – Materialien und Assetaufbereitung** | UVs, Materialien/Texturen, benötigte Kollision/Detailstufen und freigegebener Export aus einer eigenen Folgerevision | Beginnt am übergebenen Modell; bearbeitet nicht gleichzeitig dieselbe `.blend` wie Rolle 2. Technische Anforderungen aus dem Auftrag übernehmen. |
| **Rolle 4 – Unreal-Integration vorbereiten** | Import-/Platzierungsskripte, Abhängigkeiten, Zielpfade, Wiederherstellungsplan und gezielte Prüfungen | Offline-Vorbereitung; kein `ue.py`, kein Start/Ende des Editors, kein Schreiben in das aktive Unreal-Projekt. Opus-PM führt aus. |
| **Rolle 5 – technische Vorprüfung und Belege** | Prüfung der tatsächlichen Lieferdateien, gezielte Zwischenkontrollen, Abweichungsliste und vollständiges Belegpaket für den Projektmanager | Prüft Arbeit anderer; keine eigene Implementierung abnehmen. Laufzeitbehauptungen brauchen von Opus-PM ausgeführte Messungen. Ersetzt nicht Fables Endurteil. |
| **Fable – abschließender Qualitätsmanager** | Ein gebündeltes Urteil zum vollständig umgesetzten Auftrag anhand der vereinbarten Kriterien und echten Belege | Kein laufender Manager, keine Zwischenfreigaben, kein Polling, keine Editorsteuerung. Erst nach dem Abschluss der Umsetzungsarbeit aufrufen. |
| **Cloud-Sitzung – Recherche** | Belegte Antworten, Quellen, verwendbare Daten/Versuchsvorschläge nach dem bestehenden Rechercheablauf | Bleibt außerhalb der fünf Subagenten. Fehlender Quellenzugriff wird einmal konkret überbrückt; kein dauerhaftes Hin-und-her. |
| **Codex – Bildlieferant** | Angeforderte Referenz-/Assetbilder als echte Dateien mit Liefernachweis | Bleibt außerhalb der fünf Subagenten; erzeugt durch diese Rolle noch kein Blender-Modell und übernimmt keine Projektleitung. |

Opus 5.5, Sonnet 5.5 und Fable sind die **gewünschten Modellbezeichnungen**; Opus-PM ist die Rollenkennung
des Projektmanagers, kein weiterer Modellname. Opus-PM prüft beim tatsächlichen
Start, welche Modellkennungen, Agentenplätze und Werkzeuge verfügbar sind, und notiert die
Zuordnung im bestehenden Sitzungsbericht. Die unten definierte Zuteilung zwischen Sonnet
und Opus ist von Ferat autorisiert und braucht keine erneute Bestätigung. Nicht verfügbare
Modelle einmal melden; keine ungenannten Ersatzmodelle verwenden. Diese Anleitung
konfiguriert keine Modelle. Die früheren Bezeichnungen „Opus 1“ bis „Opus 5“ entsprechen
den Fachrollen 1 bis 5; vorhandene Belege und Aufgaben behalten dadurch ihre Identität.
Die Cloud behält ihre bisherige Sitzung; sie wird nicht automatisch in einen Subagenten umgewandelt.

Fünf feste Rollen, maximal fünf aktive Subagenten; keine weiteren Unteragenten erzeugen.
Der Opus-Projektmanager ist zusätzlich zu diesen fünf Rollen vorgesehen. Fable bleibt
außerhalb des operativen Subagententeams und wird erst nach dessen fertiger Lieferung
für die Endprüfung aktiviert. Nicht vorsorglich starten oder dauerhaft mitlaufen lassen.
Opus-PM hält im bestehenden Sitzungsbericht Rolle, tatsächliche Agent-/Sitzungskennung und
Verweis auf das aktive Arbeitspaket fest; dessen Besitzer und Stand führt allein der Auftrag.
Eine vorhandene passende Sitzung fortsetzen; kein Duplikat nur
wegen einer neuen Nachricht starten. Beim Neustart aktive Agenten zuerst abgleichen.
Es müssen nicht alle gleichzeitig laufen. Bei Wasserproblemen arbeiten etwa Rolle 1 und 4
an getrennten Eingaben, danach Rolle 5 an den Belegen. Rollen 2/3 werden nur bei benötigten
Assets gestartet. Pro Agent genau ein ausführbares Arbeitspaket; wartende Rollen ruhen.
Die fünf Plätze sind eine Obergrenze, kein Auslastungsziel. Nur unabhängige Arbeit ohne
gemeinsame Schreib-/Rechenressource parallel starten; vorhandene Speicher- und GPU-Grenzen
beachten. Einen kleinen direkt erledigbaren Schritt nicht eigens zum Delegationspaket machen.
Opus-PM bündelt Entscheidungen und beseitigt Blockaden, statt jede kleine Handlung erneut
genehmigen zu lassen. Bestehende Freigaben gelten, zusätzliche Ausgaben sind nicht pauschal erlaubt.

### Modellwahl pro Arbeitspaket

Opus-PM entscheidet vor dem Start anhand von Aufgabe, Eingaben und Abnahmekriterien.
Sonnet belegt einen der fünf vorhandenen Plätze. Ein Wechsel zu Opus übernimmt denselben
Vorgang samt brauchbaren Ergebnissen; die bisherige Ausführung muss vorher beendet sein.
Rollenbesitzer, Modell und Eingabestand im bestehenden Auftrag notieren, keine Modellwarteschlange
oder neue Datei je Wechsel anlegen. Kein zusätzliches dauerhaftes Sonnet-Team starten.

| Arbeitspaket | Modell und Begrenzung |
| --- | --- |
| Dateien, Benennung, Vollständigkeit und Prüfsummen kontrollieren | Sonnet 5.5; feste Soll-Liste und tatsächliche Dateien vergleichen. |
| Protokolle auswerten, Belege zusammenstellen, Liefernachweise/Dokumentation vorbereiten | Sonnet 5.5; Aussagen an vorhandene Belege binden, fehlende Nachweise offen lassen. |
| Geprüftes Offline-Skript mit festgelegten Parametern ausführen | Sonnet 5.5, wenn Opus-PM Eingaben, Schreibbereich, erwartetes Ergebnis und Wiederanlauf geklärt hat. Live-Unreal-Ausführung bleibt bei Opus-PM. |
| Unklare Fehlerursache, neue Blender-/Unreal-Verfahren, komplexe Geometrie-/Materialentscheidungen | Opus 5.5; keine Routineannahme trotz unklarer Voraussetzungen. |
| Architektur, Prioritäten, Zwischenannahme und lokale Editorsteuerung | Opus-PM mit Opus 5.5. |
| Endurteil zum vollständig umgesetzten Auftrag | Fable, ausschließlich nach Abschnitt 6. |

**Sonnet zuerst für Dateiprüfung, Protokollauswertung und Dokumentation einsetzen.** Das
betrifft besonders Routinepakete der Rolle 5 und klar begrenzte Teilaufgaben anderer Rollen.
Anspruchsvolle technische Bewertung innerhalb derselben Rolle bleibt bei Opus. Keine
pauschale Zuweisung einer ganzen Fachrolle an Sonnet nur aufgrund ihres Namens.

Jeder Sonnet-Auftrag braucht konkrete Eingaben, erlaubte Änderungen, ein gefordertes
Ergebnis, prüfbare Erfolgskriterien und einen Aufwandrahmen. Bei unklaren Anforderungen
oder einem nicht lösbaren Fehler meldet Sonnet einmal Befund, bereits ausgeführte Schritte,
Dateistand und konkrete offene Frage an Opus-PM. Keine eigenständige Weiterdelegation,
kein blindes Wiederholen und keine spekulative Erweiterung des Auftrags. Opus-PM klärt den
Eingang, übernimmt mit Opus oder stellt das Paket begründet zurück. Kein Modellwechsel
behebt fehlenden Zugriff; diesen zuerst klären. Ist Sonnet nicht verfügbar, darf Opus-PM
das Paket selbst erledigen oder mit verfügbarem Opus 5.5 besetzen und die Abweichung notieren.

Opus-PM kontrolliert die Lieferung an den vereinbarten Kriterien und verwendet brauchbare
Ergebnisse weiter. Vorhandene maschinelle Prüfer bevorzugen; keine vollständige zweite
Bearbeitung desselben Routinepakets durch Opus allein wegen des Sonnet-Einsatzes.
Sonnet bestätigt weder eigene Implementierungen unabhängig noch Fables Endabnahme.
Unabhängigkeit bezieht sich auf die tatsächliche Sitzung und Arbeit: ein Modellwechsel
oder die Umbenennung des Erstellers in Rolle 5 macht dessen Selbstprüfung nicht unabhängig.
Der erste echte Routineauftrag dient als Eignungsprobe: verwertbares Ergebnis, Prüfbeleg
und nötige Nacharbeit im bestehenden Bericht nennen. Eine konkrete Kosten-/Limitersparnis
erst aus tatsächlicher Nutzung ableiten, nicht aus dem Modellnamen.

## 2. Ein Auftrag, klare Eingaben, eine zuständige Stelle

Opus-PM prüft zuerst vorhandene Ergebnisse, passende Assets und Ferats aktuelle Priorität.
Ein neues Bild ist nur nötig, wenn es eine konkrete Modellierungs-/Gestaltungsentscheidung
verbessert. Eine bereits passende Referenz verwenden; keine Pflicht-Bilderzeugung für jedes Asset.

Für neue Assets legt Opus-PM einmal den [Assetauftrag](vorlagen/asset-auftrag.md) an. Darin:
stabile ID, Revision, Ziel, vorhandene Referenzen, Maße, Abnahmekriterien, benötigte Lieferungen,
zuständige Sitzung und nächste Handlung. Technische Maße kommen aus dem Auftrag, nicht aus
geschätzten Pixelabständen eines generierten Bildes. Nicht sichtbare Rückseiten und Details
als Annahmen kennzeichnen und von Opus-PM vor abhängiger Ausarbeitung entscheiden lassen.
Den Gesamtauftrag und seine Pflichtkriterien beim Start benennen. Interne Recherche-, Bild-
und Fachpakete verweisen darauf; sie dürfen ihre Teilziele abschließen, ohne eine eigene
Fable-Endprüfung auszulösen. Ein freigegebener fertiger Teil darf sofort weiterverarbeitet werden.

Jeder Subagent erhält nur seinen klaren Ausschnitt: Ziel, unveränderliche Eingabepfade und
SHA-256, erlaubter Schreibbereich, Abhängigkeiten, Ergebnisformat, Kriterien und Aufwandrahmen.
Nur relevante Regeln und Belege mitgeben; vollständige Chatverläufe und wiederholtes Lesen
sämtlicher Workflow-Dateien sind keine Pflicht pro Teilaufgabe oder Polling-Lauf.
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
  modell/r001/                      # Rolle 2: .blend + Ansichten + lieferung.md
  material/r001/                    # Rolle 3: neue .blend + Texturen/Export + lieferung.md
  integration/r001/                 # Rolle 4: Skripte/Importplan + lieferung.md
  pruefung/r001/                    # Rolle 5: Prüfbericht; Opus-PM: getrennte UE-Belege
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
Für Codex-Bildstarts gibt es zusätzlich die lokale atomare Reservierung nach dem
[Abfrageprotokoll](codex/README.md#lokale-sicherung-vor-bildgenerierung). Sie gilt nur für
diesen Bildauftrag, nicht für Blender, Unreal oder unabhängige Dateisysteme.

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
   Korrektur im selben Auftrag. Erst dann übernimmt Rolle 2 genau diese Bildrevision.

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
| Modell in Arbeit → Modell angenommen | Rolle 2 modelliert in Blender; editierbare Datei lässt sich erneut öffnen. Maße, Silhouette und Ansichten geprüft; Opus-PM übernimmt mit Prüfbeleg. |
| Material/Export in Arbeit → Paket geprüft | Rolle 3 liefert Materialien, UVs und benötigte Exportdateien. Rolle 5 prüft die tatsächlichen Dateien gegen die Kriterien; Opus-PM entscheidet. |
| Integration vorbereitet → angewendet | Rolle 4 liefert Import-/Rücksetzplan; Opus-PM prüft aktuellen Projektstand, sichert Ausgangspunkt und importiert exklusiv in Unreal. |
| im Projekt geprüft → umgesetzt – Endprüfung offen | Opus-PM liefert reale Projektbilder/Messungen; Rolle 5 prüft Vollständigkeit und technische Kriterien. Erst wenn der ganze Auftrag umgesetzt und belegt ist, übergibt Opus-PM an Fable. |
| Endprüfung → abgeschlossen / Korrektur | Fable bewertet das vollständige Ergebnis. Bei bestandenem Urteil schließt Opus-PM ab; bei konkreten Mängeln vergibt Opus-PM die Korrektur. |
| wartet auf … / Korrektur / verworfen | Opus-PM nennt genau fehlenden Eingang bzw. Mangel, Besitzer und Wiederaufnahmebedingung; keine neue Auftragskette. |

Blender-Abnahme passend zum Asset: Maße/Einheiten, Transform/Pivot, Normalen, Silhouette,
benötigte Topologie, UVs, Materialzuordnung, auflösbare Texturpfade und vereinbarte Detail-/
Kollisionsbudgets. Blender-Version, tatsächliche Exportoptionen und Achsen/Einheiten nennen.
Nur das im Auftrag benötigte Austauschformat liefern; FBX/glTF nicht pauschal beide fordern.
Export separat wieder einlesen und gegen Maße/Materialien prüfen. Externe Texturen im Paket
mitliefern oder nachvollziehbar packen; keine nur auf dem Rechner des Erstellers gültigen Pfade.

Rolle 4 darf den Importplan früh auf festen technischen Vorgaben vorbereiten; endgültige
Dateinamen/Prüfsummen und Validierung erst am angenommenen Export festlegen. Rolle 3 kann
Materialrezepte unabhängig vorbereiten, aber das Modell erst nach Übergabe verändern.
Opus-PM allein führt Live-Editor- und Projektänderungen aus, auch wenn ein Hilfsagent Zugang hätte.
Bestehende Editoraufträge, Ferats Nutzung, Speicher-/PIE-Regeln und Wiederherstellung beachten.
Ein offline gültiger Export ist noch kein getestetes UE5.8-Asset; Laufzeit, Maßstab, Kollision,
Materialdarstellung und Einfügung in den Zielabschnitt lokal belegen, soweit im Auftrag nötig.

### Feste Prüfeingaben, Nachprüfung und Pilotfreigabe

Gilt für alle Arbeitspakete (Assets, Werkzeuge, Welt-Eingriffe); von Codex im Auftrag Ferats am 18.10. festgelegt.

1. **Feste Eingabestände.** Geprüft wird nur ein eingefrorener Stand, nie eine Datei, die eine laufende Kette noch schreibt.
   Nach abgeschlossener Schreibung sichert Opus-PM die benötigten Eingaben unter einer eindeutigen Standbezeichnung mit
   Zeitpunkt und SHA-256-Liste. Vorher- und Nachher-Stände eines Eingriffs bleiben getrennt. Fehlt ein historischer Eingang,
   heißt die betroffene Prüfung „nicht belegbar“; sie wird nicht aus späteren Daten nachgebaut. Jedes Prüfergebnis nennt
   die Standbezeichnung und die Prüfsummen, gegen die es gilt.
2. **Korrekturen erneut unabhängig prüfen.** Nach einer Korrekturrunde prüft ein unabhängiger technischer Prüfer (Opus 5.5,
   nicht der Ersteller, nicht Fable) die behobenen kritischen und wichtigen Mängel an der korrigierten Fassung und wiederholt
   die passenden Gegenfälle. Erst danach gibt Opus-PM die Ausführung frei. Bleibt ein solcher Mangel offen, bleibt das Paket
   gesperrt; keine automatische weitere Korrekturschleife (Grenzen nach Abschnitt 7). Fable bleibt der Endprüfung vorbehalten.
3. **Rekonstruierte Prüfgrundlagen vor großflächiger Anwendung bestätigen.** Neu berechnete Karten, Masken oder Klassenregeln
   gelten als unbestätigt, bis Opus-PM sie mit dem tatsächlich gebauten Zustand im Editor verglichen hat – an Fällen, die
   geändert werden sollen, und an Fällen, die erhalten bleiben müssen. Danach folgt eine begrenzte Pilot-Anwendung mit
   Sicherung, dokumentiertem Rückweg, festen Vorher-/Nachher-Kameras und erneutem Zensus. Erst nach bestandener Prüfung des
   Piloten wird ausgeweitet. Bei Widersprüchen wird das betroffene Gebiet ausgelassen und der Befund im Auftrag festgehalten.
4. **Jedes veränderte Paket gespeichert belegen** (Codex, 18.10.). Vor einem Eingriff ermittelt das Werkzeug die betroffenen Pakete.
   Enthält eines davon bereits ungespeicherte Änderungen, wird der Eingriff blockiert und Opus-PM klärt den Zustand; fremde
   Änderungen werden weder automatisch mitgespeichert noch verworfen. Nach dem Eingriff braucht jedes tatsächlich veränderte
   Paket einen erfolgreichen Speicherbeleg; fehlende oder fehlgeschlagene Speicherung ergibt keinen Erfolgsstatus. Bei
   ungespeicherten Änderungen oder unklarem Speicherzustand ist ein automatischer Neustart gesperrt. Der Beleg unterscheidet
   „im Speicher verändert“, „erfolgreich gespeichert“ und „nach erneutem Laden bestätigt“. Ein unterbrochener Lauf wird nicht
   blind wiederholt; zuerst Protokoll, Speicherstand und Projektzustand prüfen.
5. **Abweichende Eingabestände blockieren die Änderung.** Vor Sicherung und Änderung müssen Auswahl, Auswertung und eingefrorener
   Eingabestand über Standbezeichnung und SHA-256 zusammenpassen; Zeitstempel allein genügen nicht. Fehlt ein Nachweis oder
   weicht er ab: vor der Änderung abbrechen, Befund festhalten, Auswertung auf einem neuen konsistenten Stand wiederholen.
   Keine Warnung übergehen, keine Prüfsumme nachträglich passend schreiben. Zusätzlich im Editor prüfen, dass die ausgewählten
   Objekte noch dem geprüften Zustand entsprechen; Dateiprüfsummen allein belegen das nicht.

Welche Stände, Vergleichsfälle und Freigaben konkret gelten, steht im jeweiligen Auftrag (einziger Auftragsstatus).

## 6. Fable nur am Ende einsetzen

Opus-PM definiert den Umfang eines vollständigen Auftrags beim Start. Ein einzelnes
Referenzbild, Modell oder Teilpaket innerhalb eines Assetauftrags ist kein Gesamtabschluss.
Eine Quellenfrage innerhalb dieses Auftrags endet als beantworteter Teil. Nur wenn Ferat
die Recherche selbst als eigenständiges Gesamtziel beauftragt hat, ist ihre vollständige
belegte Antwort das Endpaket. Umfang nicht künstlich in Kleinstaufträge aufteilen, um Fable
öfter aufzurufen.

Vor Fables Aufruf müssen alle vereinbarten Lieferungen vorliegen, erforderliche lokale
Tests gelaufen und bekannte blockierende Mängel behoben sein. Fehlende Pflichtbelege
beschafft das Fachteam; Fable wird nicht zum Einsammeln oder zur Fortschrittskontrolle gestartet.
Opus-PM friert ein kompaktes Endpaket ein: Auftrag und Kriterien, angenommene Dateirevisionen
mit Prüfsummen, tatsächliche Testbelege, Ziel-/Ergebnisbilder und bekannte Grenzen. Keine
vollständigen Chatverläufe oder wiederholte Recherche als Standardkontext mitgeben.
Vor dem Aufruf klären, dass Fables Sitzung auf dieses Paket und seine Bilder zugreifen kann;
fehlenden Transfer zuerst erledigen. Ein lokaler Pfad allein bestätigt keinen Zugriff.

Fable prüft den vereinbarten Gesamtumfang, sieht die relevanten Bilder selbst an und liefert
einmal je vollständig vorbereiteter Ergebnisrevision ein Urteil: **bestanden**, **Korrektur
nötig** mit konkretem Kriterium/Beleg oder **nicht beurteilbar** mit fehlendem Nachweis.
Keine unbelegte pauschale Freigabe. Fable implementiert nichts, verteilt keine Subaufträge
und erweitert den Umfang nicht eigenständig. Opus-PM bleibt der einzige Koordinator.
Pflichtkriterium verletzt bedeutet Korrekturbedarf. Zusätzliche Verbesserungsideen getrennt
als optional kennzeichnen; sie verhindern keine Abnahme erfüllter Pflichtkriterien und
lösen ohne Priorisierung durch Opus-PM keinen weiteren Arbeitszyklus aus.

Bei Mängeln bearbeitet das Fachteam die betroffenen Teile, prüft Auswirkungen und liefert
wieder ein vollständiges korrigiertes Paket. Erst dann Fable erneut aufrufen, mit Fokus auf
die geänderten Kriterien und betroffenen Abhängigkeiten. Keine unveränderte Endprüfung im
30-Minuten-Takt. Ist Fable nicht verfügbar, bleibt der Stand „umgesetzt – Endprüfung offen“;
unabhängige nächste Aufgaben dürfen weiterlaufen. Fable ist kein Voraussetzungsschritt für
Bildgenerierung, Zwischenübergaben oder die GitHub-Abfrage.
Während der Endprüfung die referenzierten Dateien unverändert lassen. Bei neuer Eingabe
nur betroffene Teile erneut prüfen; Fables Urteil gilt ausschließlich für das benannte Paket.
Ein Urteil zu einer älteren Revision schließt den geänderten Auftrag nicht automatisch ab.

## 7. Fehler, Wiederaufnahme und Ergebnisdruck

- Eine Lieferung wird erst nach vollständigem Speichern geprüft. Eine fehlende oder nicht
  passende Prüfsumme, beschädigte Datei oder veraltete Eingabe blockiert nur abhängige Arbeit.
- Keine pauschale Wiederholung der Pipeline: bei UV-Fehler Rolle 3 korrigieren lassen, bei
  Importfehler Rolle 4/Opus-PM; ein fertiges Bild dafür nicht erneut generieren.
- Nach Sitzungsabbruch erst Lieferung, laufende Prozesse und tatsächlichen Projektstand
  prüfen. Bereits erfolgten Import nicht noch einmal ausführen, nur weil der Bericht fehlt.
- Opus-PM entzieht/überträgt einen Auftrag ausdrücklich. Bei geänderter Vorgabe laufende
  abhängige Arbeit kontrolliert stoppen; verspätete Lieferung auf ihre alte Revision beziehen.
  Keine angenommene neue Revision überschreiben; verwertbare unabhängige Teile erhalten.
- Höchstens zwei Korrekturrunden ohne messbaren Fortschritt; danach Ursache, Eingaben oder
  Methode ändern bzw. begründet zurückstellen. Kein dritter wortgleicher Auftrag.
- Bei teuren Bildern, Bakes und Renderings vorher Umfang und Stopkriterium festlegen;
  keine nicht verfügbaren Werkzeuge oder zusätzliche bezahlte Dienste als gegeben behandeln.
- Aufwand und Korrekturrunden gelten für das Arbeitspaket insgesamt. Modellwechsel, neue
  Sitzung oder Lieferrevision setzen sie nicht zurück. Nach Erreichen der Grenze Opus-PM
  entscheiden lassen, bevor weitere aufwendige Arbeit beginnt.
- Im bestehenden Morgen-/Sitzungsbericht: verwendbare Ergebnisse, Beleg, offene technische
  Grenze, nächster Besitzer/Schritt. Nicht zusätzlich fünf Statusberichte zusammenkopieren.

## 8. Übernahme und erste praktische Probe

Der kompakte Einstieg steht in [START_HIER.md](START_HIER.md). Ferat hat den Beginn nach
Rücksetzung des Wochenlimits für Sonntag, 18.10., ab 04:00 Uhr Schweizer Zeit genannt.
Das bedeutet kein Löschen der bisherigen Sitzung oder Neustart erledigter Arbeit.

Beim nächsten echten Start liest Opus-PM [CLAUDE.md](../CLAUDE.md), diesen Workflow und den
aktiven Vorgang. Startweg und ältere lokale Anweisungen auf diese Arbeitsteilung abgleichen;
die Veröffentlichung allein aktualisiert keine Desktop-Startdateien oder Erinnerungen.
Diese neue Rollenverteilung ersetzt ältere Rollenpläne; bestehende Projekt-, Editor- und
Zugriffsschutzregeln gelten weiter. Für die lokale Übernahme lautet der Einstieg:
`D:\Das Lied der Asche\recherche_repo\CLAUDE.md` und
`D:\Das Lied der Asche\recherche_repo\recherche\TEAM_WORKFLOW.md`.
Bekannte Einstiegslücke: die Desktop-`CLAUDE.md` und ältere Cloud-Erinnerungen enthalten
noch pauschale Cloud-Delegation bzw. alte Rollenregeln. Sie wurden bei dieser Prüfung nur
gelesen, nicht aktualisiert. Opus-PM muss beim realen Start nachweisen, dass er diesen neuen
Einstieg verwendet und die jüngste Rollenentscheidung übernimmt. Eine aktualisierte
Recherche-Kopie allein ist kein Nachweis dafür.
Tatsächliche Modell-/Werkzeugzuordnung und Codex-Zustellweg im bestehenden Bericht nennen.
Der Codex-Zeitplan und mehrere erfolgreiche planmäßige GitHub-Abrufe sind im Chat belegt;
bislang gab es dort keine Bildaufträge. Die Bild-Lieferkette ist noch praktisch nachzuweisen.
Die automatische Ergebnisabfrage bei Opus-PM/Cloud ist damit
nicht installiert. Keine bereits laufenden Subagenten oder getestete Gesamtkopplung behaupten.

Erste Probe: ein tatsächlich benötigtes einfaches Asset aus Ferats Priorität, ein Bild,
ein Blender-Modell, ein Material-/Exportpaket, ein Import in ein geeignetes kleines Testlevel.
Rolle 5 prüft die Lieferkette und Opus-PMs UE-Beleg. Dabei auch prüfen: unveränderter Auftrag
startet keine zweite Bildgenerierung; eine Korrektur betrifft nur abhängige Stufen; ein
unterbrochener Schritt wird vom gespeicherten Stand fortgesetzt. Fable erhält erst das
vollständige Endpaket; sein Urteil ist der letzte Abnahmeschritt. Im Bericht echte Ergebnisse
und noch ungeprüfte Fälle auseinanderhalten. Bis zu dieser Probe ist der Ablauf definiert,
aber die Modellkonfiguration und durchgehende Ausführung sind noch nicht praktisch bestätigt.
