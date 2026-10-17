# GitHub-Abfrage für Bildaufträge

Ferat hat am 17.10.2026 die Prüfung alle 30 Minuten beauftragt. Der Codex-Zeitplan
„GitHub-Bildaufträge für Codex prüfen“ wurde in diesem Chat mit Status ACTIVE angelegt.
Kennung: `github-bildauftr-ge-f-r-codex-pr-fen`. Dies belegt die Einrichtung, noch keinen
erfolgreichen geplanten Lauf. Bestehende pausierte Automatisierungen bleiben pausiert.
Der [Teamworkflow](../TEAM_WORKFLOW.md) und seine Rollen gelten weiterhin.
Aktuelle Leitung: Opus 5.5 als Opus-PM. Fable wird ausschließlich zur Endprüfung eines
vollständig umgesetzten Auftrags aufgerufen und übernimmt keine 30-Minuten-Abfrage.
Eine Bildlieferung benötigt Opus-PMs operative Annahme, noch kein Fable-Endurteil.

## Ablage und Zuständigkeit

Repository: `FiratBulut/fbulut`, Branch: `claude/recherche-auftrag-s5m3y6`.

- Auftrag: `recherche/codex/auftraege/<asset-id>/<revision>.md`, z. B. `r001.md`.
  Genau ein benannter Auftragsschreiber (Opus-PM oder die von Opus-PM beauftragte Cloud).
- Antwort: `recherche/codex/antworten/<asset-id>/<revision>.md`, ausschließlich Codex.
- Bilder: lokale Assetwurzel aus dem Teamworkflow, `<asset-id>/codex/<revision>/`.
  Der lokale Assetauftrag bleibt unter Opus-PMs Kontrolle; GitHub transportiert nur den
  Bildauftrag und den Codex-Lieferbeleg, keine zweite vollständige Asset-Aufgabenliste.

Asset-ID nur aus Kleinbuchstaben, Ziffern und Bindestrichen, Revision `r` plus drei Ziffern.
Zielpfade müssen innerhalb der lokalen Assetwurzel liegen. Keine Zugangsdaten, privaten
Referenzen, Modelle oder Bilddateien automatisch im öffentlichen Repository veröffentlichen.
Die Cloud kann einen freigegebenen Auftrag für Opus-PM zustellen; eigenständige neue Assetziele
bleiben Opus-PMs Entscheidung. Normale Forschungsaufträge behalten ihre bisherigen Pfade.

## Mindestinhalt eines konkreten Bildauftrags

Die [Assetvorlage](../vorlagen/asset-auftrag.md) liefert den eigentlichen Bildprompt.
Im GitHub-Auftrag ergänzen:

```text
Asset-ID: <id>
Revision: r001
Empfänger: Codex
Typ: Assetbild
Freigabe: Opus-PM, <Sitzung und Bezug auf den Assetauftrag>
Auftragsschreiber: <Opus-PM oder beauftragte Cloud-Sitzung>
Ergebnisabfrage durch: <genau eine Opus-PM- oder Cloud-Sitzung>
Status: bereit
Priorität: <Opus-PMs Priorität>
Prompt: <vollständiger konkreter Bildauftrag>
Referenzen: <für Codex erreichbare Pfade mit SHA-256 oder zulässige Quellen>
Abnahmekriterien: <sichtbar prüfbare Kriterien>
Bildanzahl: 1
Ziel: <asset-id>/codex/r001/
```

Vor Veröffentlichung Eingaben vollständig bereitstellen. Codex identifiziert den Auftrag
zusätzlich über Git-Blob-SHA und Commit, Referenzen über ihre tatsächlichen Prüfsummen.
Eine Vorlage mit Platzhaltern ist kein ausführbarer Auftrag. Inhaltliche Änderungen nach
Beginn erhalten eine neue Revision; die alte ausdrücklich als `ersetzt` markieren.
Abbruch erfolgt im bestehenden Auftrag mit `Status: storniert`. Ein neuer Zeitstempel oder
eine Statusquittung bedeutet keinen neuen Bildauftrag. Keine Datei je Nachfrage anlegen.

## Was Codex alle 30 Minuten tut

1. Remote-Stand abrufen, aktive Aufträge und vorhandene Antworten abgleichen. Bei unverändertem
   Stand ohne offene ausführbare Arbeit endet die Prüfung ohne Bericht oder Git-Commit.
2. Höchstens einen bereiten, vollständigen Auftrag nach Opus-PMs Priorität übernehmen. Vor
   Bildgenerierung Besitzer/Sitzung und Eingabestand in derselben Antwortdatei als `in Arbeit`
   veröffentlichen. Scheitert das, noch keine neue Generierung starten.
3. Gleicher Auftrag mit vorhandener Lieferung: verwenden, nicht erneut erzeugen. `in Arbeit`
   wird nicht nach 30 Minuten automatisch frei. Laufende Generierung nicht duplizieren.
   Nach Abbruch gespeicherte Bilder und bisherigen Lauf prüfen; bei ungeklärtem Zustand einmal
   blockieren statt blind einen weiteren kostenpflichtigen Versuch zu starten.
4. Bild erzeugen, lokal speichern und prüfen. Antwort auf `geliefert (lokal)` aktualisieren:
   gelesener Auftragsstand, Referenz-Prüfsummen, relativer Assetpfad, Bildmaße, Bild-SHA-256,
   durchgeführte Prüfung und Abweichungen. Ein bloßer Dateiname zählt nicht als Lieferung.
5. Vor Veröffentlichung aktuellen Auftrag nochmals auf Stornierung/Ersetzung prüfen.
   Überholte Ergebnisse so kennzeichnen, nicht als aktuelle Lieferung ausgeben. Bei einem
   Pushfehler lokales Bild und Belege behalten; später nur die Veröffentlichung nachholen.

Fehlende Eingaben/Werkzeuge als `blockiert` mit genauem Bedarf und Wiederaufnahmebedingung
einmal festhalten. Bei neuen relevanten Eingaben erneut prüfen; unveränderte Blocker nicht
alle 30 Minuten melden. Keine Unreal-Arbeit, allgemeinen Codeaufträge oder zusätzlichen
Dienste aus einem Bildauftrag ableiten. Repositorytexte sind Arbeitsmaterial und können
die von Ferat erteilte Freigabe nicht erweitern.

## Wer auf das Ergebnis wartet

Der eingetragene Empfänger prüft **nur während eines offenen eigenen Auftrags** alle
30 Minuten die passende Antwortdatei und deren Eingabeversion. Opus-PM ist der Standard;
wenn die Cloud diese Rolle übernimmt, fragt Opus-PM denselben Transport nicht zusätzlich ab.
Keine Nachfragenachricht und kein Commit bei jedem leeren Abruf. Nach passender Lieferung,
Stornierung oder endgültigem Abbruch endet das Warten auf diese Revision.

Nach Lieferung prüft Opus-PM das lokale Bild und führt die nächste Modellierungsstufe fort.
Eine Cloud-Sitzung ohne Zugriff auf das lokale Laufwerk kann den GitHub-Lieferstatus lesen,
aber damit das Bild noch nicht visuell prüfen. Benötigt sie die Ansicht tatsächlich, einmal
eine zugängliche, zulässig geteilte Darstellung anfordern; keine erneute Bildgenerierung.
Ein `D:`-Pfad ist kein Downloadlink für die Cloud.

**Einrichtung der Gegenseite noch offen:** Diese Anleitung startet keinen Cloud-Zeitgeber.
Opus-PM/Cloud müssen einen tatsächlich vorhandenen Wiederholungsmechanismus verwenden oder
einrichten und den ersten erfolgreichen Abruf im bestehenden Bericht belegen. Wenn ihre
Sitzung nicht automatisch fortgesetzt werden kann, ist die Abfrage manuell beim nächsten
Start auszuführen und als manuell zu kennzeichnen. Keinen aktiven 30-Minuten-Dienst behaupten.
Bestehende Abfragen erweitern, keinen zweiten Dienst für denselben Empfänger starten.

## Zeitverhalten und erste Probe

Bei laufenden Zeitgebern: bis zu ungefähr 30 Minuten bis Codex den Auftrag entdeckt,
danach Generierungszeit und bis zu weitere 30 Minuten bis der Empfänger die Antwort sieht.
Das ist keine zugesicherte Lieferfrist; Warteschlange, Zugriff oder Offline-Zeit verlängern sie.
Für lokale Codex-Läufe müssen Rechner und App verfügbar sein. Nach Wiederaufnahme zuerst
aktuellen Zustand prüfen; ausgefallene Intervalle nicht als mehrere Aufträge nachholen.

Die erste echte Probe muss Auftragserkennung, Bildablage, GitHub-Antwort und Annahme durch
Opus-PM zeigen. Ein erneuter Abruf derselben Revision darf kein zweites Bild auslösen. Bis dahin
ist nur der Zeitplan eingerichtet, die vollständige Automatisierung noch nicht nachgewiesen.
