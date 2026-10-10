# Auftrag 11 – Status der Verteilungs-Arbeiten (Koordinator: Cloud-Session)

Stand: 2026-10-10 12:05 UTC. Wird bei jedem Push aktualisiert.

| Teil | Thema | Agent | Stand | Dateien |
|---|---|---|---|---|
| A | Asset-Taxonomie | 1 Agent | läuft | `assets-taxonomie.json`, `assets-taxonomie.md` |
| C | Fels organisch | 1 Agent | läuft | `verteilung-fels-organisch.md`, `skripte/felsgruppen_plan.py`, `skripte/felsgruppen_regeln.json` |
| D | Leere füllen (Mittelschicht, Spuren) | 1 Agent | läuft | `verteilung-leere-fuellen.md`, `skripte/mittelschicht_plan.py`, `skripte/mittelschicht_regeln.json`, `skripte/spuren_plan.py`, `skripte/spuren_regeln.json` |
| B1 | Nordküste (fjord, kueste, bergwald) | – | wartet auf A | `verteilung-nordkueste.md`, `skripte/nordkueste_*` |
| B2 | Aue/Flussauen | – | wartet auf A | `verteilung-aue.md`, `skripte/aue_*` |
| B3 | Heide/Tundra | – | wartet auf A | `verteilung-heide-tundra.md`, `skripte/heide_tundra_*` |
| B4 | Gletscher/Frost/Hochgebirge | – | wartet auf A | `verteilung-hochgebirge.md`, `skripte/hochgebirge_*` |
| B5 | Elfenwald | – | wartet auf A | `verteilung-elfenwald.md`, `skripte/elfenwald_*` |
| B6 | Sumpf | – | wartet auf A | `verteilung-sumpf.md`, `skripte/sumpf_*` |
| B7 | Dschungel (inkl. Karst) | – | wartet auf A | `verteilung-dschungel.md`, `skripte/dschungel_*` |
| B8 | Lava | – | wartet auf A | `verteilung-lava.md`, `skripte/lava_*` |
| B9 | Wüste/Canyon/Ödland (nur ergänzen) | – | wartet auf A | `verteilung-wueste.md`, `skripte/wueste_ergaenzung_*` |

Reihenfolge: A, C, D parallel → dann B1–B9 parallel (zwei Wellen). Alle Skripte sind in der Cloud nur syntaxgeprüft und mit
synthetischen Rastern rauchgetestet (keine echten Weltdaten in der Cloud); Korrekturen bitte als `auftraege/verteilung-<thema>-korrektur.md`.
