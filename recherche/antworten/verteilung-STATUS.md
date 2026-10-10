# Auftrag 11 – Status der Verteilungs-Arbeiten (Koordinator: Cloud-Session)

Stand: 2026-10-10 13:35 UTC. Wird bei jedem Push aktualisiert. Welle K1 nach Abbruch durch Nutzungslimit neu gestartet.

Hinweis: Um 12:40 UTC brach ein API-Sitzungslimit alle zehn laufenden Agenten ab (Teil D und B1–B9). Die bis dahin
geschriebenen Dateien sind als Zwischenstand gepusht (Skripte syntaxgeprüft, aber Rauchtests und Berichte teils offen).
Fortsetzung ab 12:55 UTC in drei Wellen zu je 3–4 Agenten, die auf den vorhandenen Dateien aufsetzen.

| Teil | Thema | Agent | Stand | Dateien |
|---|---|---|---|---|
| A | Asset-Taxonomie | 1 Agent | fertig, gepusht | `assets-taxonomie.json`, `assets-taxonomie.md` |
| C | Fels organisch | 1 Agent | fertig, gepusht (Rauchtest synthetisch B4: 55 856 Inst., 7,9 s) | `verteilung-fels-organisch.md`, `skripte/felsgruppen_plan.py`, `skripte/felsgruppen_regeln.json` |
| D | Leere füllen (Mittelschicht, Spuren) | 1 Agent | fertig (Welle 1): Inventarprüfung + Budget-Deckel + Akteur-Dateien ergänzt; Rauchtest synthetisch G4: Mittelschicht 52 047 Inst./4,3 s, Spuren 6 257 Inst./10 Akteure/9,2 s, deterministisch | `verteilung-leere-fuellen.md`, `skripte/mittelschicht_plan.py`, `skripte/mittelschicht_regeln.json`, `skripte/spuren_plan.py`, `skripte/spuren_regeln.json` |
| B1 | Nordküste (fjord, kueste, bergwald) | 1 Agent | fertig, gepusht (Rauchtest synthetisch B5: 27 114 Inst., 10–12 s) | `verteilung-nordkueste.md`, `skripte/nordkueste_*` |
| B2 | Aue/Flussauen | 1 Agent | fertig, gepusht (Rauchtest synthetisch E5: 32 627 Inst., 8,5 s) | `verteilung-aue.md`, `skripte/aue_*` |
| B3 | Heide/Tundra | 1 Agent | fertig, gepusht (Rauchtest synthetisch D2/G5: je ~44 900 Inst., ~4,8 s) | `verteilung-heide-tundra.md`, `skripte/heide_tundra_*` |
| B4 | Gletscher/Frost/Hochgebirge | 1 Agent | fertig (Rauchtest synthetisch D2: 44 107 Inst., 4,1 s, deterministisch; ungetestet mit Echtdaten) | `verteilung-hochgebirge.md`, `skripte/hochgebirge_plan.py`, `skripte/hochgebirge_regeln.json` |
| B5 | Elfenwald | 1 Agent | fertig, gepusht (Rauchtest synthetisch G4: 40 846 Inst., 12–14 s; Schalter --mittel zusatz/voll) | `verteilung-elfenwald.md`, `skripte/elfenwald_plan.py`, `skripte/elfenwald_regeln.json` |
| B6 | Sumpf | 1 Agent | fertig, gepusht (Rauchtest synthetisch H5: 37 789 Inst., 7,1 s) | `verteilung-sumpf.md`, `skripte/sumpf_*` |
| B7 | Dschungel (inkl. Karst) | 1 Agent | fertig, gepusht (Rauchtest synthetisch H6: 54 932 Inst., 16 s) | `verteilung-dschungel.md`, `skripte/dschungel_*` |
| B8 | Lava | 1 Agent | fertig, gepusht (Rauchtest synthetisch C6: 42 169 Inst., 23 Punkte, ~4 s) | `verteilung-lava.md`, `skripte/lava_plan.py`, `skripte/lava_regeln.json` |
| B9 | Wüste/Canyon/Ödland (nur ergänzen) | 1 Agent | Erstfassung fertig, gepusht (lokal auf Echtdaten A5/G4/E1/C6 ohne Absturz, 0 Instanzen ausserhalb Wueste korrekt) | `verteilung-wueste.md`, `skripte/wueste_ergaenzung_plan.py`, `skripte/wueste_ergaenzung_regeln.json` |

Reihenfolge: A, C, D parallel → dann B1–B9 parallel (zwei Wellen). Alle Skripte sind in der Cloud nur syntaxgeprüft und mit
synthetischen Rastern rauchgetestet (keine echten Weltdaten in der Cloud); Korrekturen bitte als `auftraege/verteilung-<thema>-korrektur.md`.

## Korrektur Runde 1 (Auftrag `auftraege/verteilung-korrektur-runde1.md`, 10.10. 15:30 lokal)

Alle zwölf Planer werden nach `antworten/verteilung-KONVENTIONEN.md` überarbeitet: strikte Biom-Zuständigkeit mit 30-m-Saum und
Leerplan bei < 2 % Eigenanteil, Pflichtschlüssel `biome_fenster`/`zellen_zustaendig`/`biome_eigen`/`kollision_anzahl`, hartes Budget,
ASCII-Logs, leerer plan.json statt Textabbruch.

**Ebenen-Abgrenzung (Entscheidung):** `mittelschicht_plan.py` ist der einzige Planer für die generischen Mittelschicht-Klassen
(strauch, jungbaum, farn, totholz_liegend/stumpf/ast, hochstaude, grasbueschel, beere, pilz) und liest je Biom Palette und Faktoren aus
seinem eigenen JSON plus `mittelschicht_overrides` der Biom-Regeldateien. Biom-Planer setzen in Schicht 1 nur biomspezifische Sonderformen
und liefern ihre bisherigen generischen Klassen als Overrides. Felsen > 0,8 m nur über `felsgruppen_plan.py`, Spuren nur über `spuren_plan.py`.
Setz-Reihenfolge: felsgruppen → Biom-Planer → mittelschicht → spuren.

| Planer | Korrektur-Stand |
|---|---|
| felsgruppen (C) | Welle K1 läuft |
| mittelschicht + spuren (D) | Welle K1 läuft |
| nordkueste (B1) | Welle K1 läuft |
| elfenwald (B5) | Welle K1 läuft |
| dschungel (B7) | Welle K1 läuft |
| aue (B2), heide_tundra (B3), hochgebirge (B4), sumpf (B6), lava (B8) | Welle K2 wartet |
| wueste_ergaenzung (B9) | Welle K2 wartet |
