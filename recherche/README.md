# Recherche-Übergabe zwischen lokalem Claude Code und der Cloud-Session

Dieser Ordner ist die Schnittstelle zwischen der lokalen Claude-Code-Instanz
(arbeitet am Unreal-Engine-Projekt) und der Cloud-Session (recherchiert).
Beide Seiten tauschen ausschließlich Dateien über dieses Git-Repository aus.

## Ablauf

1. **Lokale Instanz** legt einen Auftrag als Markdown-Datei unter
   `recherche/auftraege/<name>.md` ab, committet und pusht ihn
   (Branch `claude/recherche-auftrag-s5m3y6`, notfalls ein beliebiger Branch).
2. **Cloud-Session** prüft das Repository regelmäßig, recherchiert und schreibt
   die Antwort nach `recherche/antworten/<name>.md` (gleicher Dateiname wie der
   Auftrag) und pusht sie auf `claude/recherche-auftrag-s5m3y6`.
3. **Lokale Instanz** liest die Antwort. Das Repository ist öffentlich, die
   Rohdatei ist direkt erreichbar:
   `https://raw.githubusercontent.com/FiratBulut/fbulut/claude/recherche-auftrag-s5m3y6/recherche/antworten/<name>.md`

Ein Auftrag gilt als erledigt, sobald eine gleichnamige Datei unter
`recherche/antworten/` liegt. Rückfragen stellt die Cloud-Session in der
Antwortdatei; die lokale Instanz antwortet mit einem neuen Auftrag
(`<name>-2.md` o. ä.).

## Format eines Auftrags

```markdown
# Titel des Auftrags

**Projekt:** kurze Beschreibung (Genre, C++/Blueprints, Zielplattform)
**Unreal-Engine-Version:** z. B. 5.5
**Priorität:** hoch / normal / niedrig
**Gewünschter Detailgrad:** Kurzantwort / ausführlich mit Codebeispielen

## Frage
Konkrete Fragestellung. Was wurde schon versucht, was ist das Ziel?

## Kontext
Relevante Code-Ausschnitte, Fehlermeldungen, Einschränkungen.
```

## Regeln

- Lokale Instanz schreibt nur in `recherche/auftraege/`.
- Cloud-Session schreibt nur in `recherche/antworten/`.
- Dateinamen in Kleinbuchstaben mit Bindestrichen, z. B. `nanite-landscape-performance.md`.
- Vor jedem Push `git pull --rebase`, damit sich beide Seiten nicht überschreiben.
