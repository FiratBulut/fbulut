# Auftrag 09: Spielfigur-Test (PIE) per Editor-Python in UE 5.8.3 starten, prüfen, beenden – mit Epics GASP-Figur

Kontext: Eldarien, UE 5.8.3, World Partition (1-km-Zellen), Epic „Game Animation Sample“ (GASP) als Spielfigur: `SandboxCharacter_CMC`,
GameMode `GM_Eldarien`, PlayerStart `Spielstart_E5` (Feld E5, Aue). Alles wird per Editor-Python über eine Fernsteuerung (`unreal`-Modul im
laufenden Editor, keine Blueprints von Hand) gemacht; der PIE-Test ist noch nie gelaufen.

**Frage 1 – PIE per Python:** Wie startet man in 5.8 Play-In-Editor aus Python (`unreal.LevelEditorSubsystem.editor_play_simulate` ist nur
Simulate; gibt es `editor_request_begin_play`/`EditorLevelLibrary`-Wege, Konsolenbefehle wie `PlayInEditor`/`pie`, `UnrealEditorSubsystem`,
`EditorUtilityLibrary`?), wie erkennt man den laufenden PIE (`unreal.EditorLevelLibrary.is_playing`?), wie macht man darin Screenshots
(`HighResShot` greift auf das Editor-Viewport; `shot`/`ScreenshotRequest`), wie beendet man PIE sauber (`editor_request_end_play`)? Mit
Quellenangaben (Epic-Python-Doku 5.6–5.8, Foren). Fallen: World-Partition-Streaming im PIE um den PlayerStart (Zellen laden), Python-Skript
blockiert den Game-Thread (PIE braucht Ticks → Skript muss zurückkehren und später erneut aufgerufen werden).

**Frage 2 – GASP-Checkliste:** Was muss für GASP in einem fremden Projekt gesetzt sein (GameMode Default Pawn, PlayerController, Input
Mapping Context/Enhanced Input, Project Settings „Default Input Component“, Plugins: Motion Warping, Pose Search, Chooser, Animation
Locomotion Library, Motion Trajectory, Gameplay Cameras), typische Fehler („Figur fällt durch den Boden“: Kollision der Nanite-Landschaft /
PlayerStart unter Gelände; „T-Pose“: fehlende Chooser-Tabellen; Kamera schwarz) und ihre Erkennung im Log?

**Frage 3 – Mindest-Spieltest ohne Menschen am Rechner:** Ablauf, um per Python automatisch 20 s zu spielen (Figur spawnt, läuft geradeaus,
Screenshot aus PIE, Log auf Fehler prüfen, PIE beenden) – welche Teile gehen per Python, welche brauchen einen Blueprint/EUW (dann Skelett dafür).

Antwort als kompakter deutscher Bericht mit Python-Snippets (ungetestet markiert) und Quellen. Ergebnis als Datei `recherche/antworten/pie-test-python-gasp.md`.
