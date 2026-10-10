# Korrektur Runde 1 zu Auftrag 11 (lokaler Test 10.10. 15:30, alle 12 Planer)

Projekt Eldarien, UE 5.8.3. Priorität hoch. Alle 12 Skripte aus `antworten/skripte/` liefen lokal (Windows, Python 3.11, `python -I -X utf8`,
Echtdaten) auf den Feldern A5, G4, E1, C6 **ohne Absturz** – gut. Daten für die Skripte liegen lokal unter `production/daten/` (netze.csv,
netze_masse.json, biome_je_feld.json, assets-taxonomie.json), Inventar-CSV auch neben jedem Skript.

Instanzen je Feld (OK = lief, Zahl = `plan.json["instanzen"]`):

| Planer | A5 (bergwald/fjord) | G4 (elfenwald) | E1 (gletscher 100 %) | C6 (lava 99 %) |
|---|---|---|---|---|
| felsgruppen | 13 311 (65 Akteure) | 114 | 18 482 | 27 357 |
| mittelschicht | 36 259 | 26 746 | 15 586 | 7 515 |
| spuren | 51 | 591 | 55 | 393 |
| nordkueste | 27 302 | kein Plan (richtig) | kein Plan (richtig) | **1 078** |
| aue | 1 743 | 1 433 | 0 | 0 |
| heide_tundra | 941 | 4 020 | 4 360 | 172 |
| hochgebirge | 0 | 0 | 35 132 | 0 |
| elfenwald | 2 152 | **86 811** | 0 | **5 875** |
| sumpf | 75 | 549 | 140 | **995** |
| dschungel | 1 038 | 15 590 | 0 | **2 783** |
| lava | 0 | 0 | 0 | 33 516 |
| wueste_ergaenzung | 0 | 0 | 0 | 0 |

## Bitte korrigieren (gleiche Dateinamen erneut pushen)

1. **Zuständigkeit strikt nach Biom-Zellen.** `dschungel`, `elfenwald`, `sumpf`, `nordkueste` setzen Instanzen in C6, obwohl das Fenster zu 96,8 %
   `lava` ist (plus 3 % bergwald). Auch `aue` 1 743 in A5 (bergwald/fjord) und `dschungel` 15 590 in G4 (elfenwald) wirken zu viel. Regel: jeder
   Biom-Planer darf nur Zellen bebauen, deren Biom (eigner.r8 + welt.json → rezept; 0 = Weltgelände → `aue`, Vulkanregion → `lava`) zu seiner Gruppe
   gehört, plus höchstens einen weichen Übergangssaum von 30 m (Dichte linear auf 0). Ist der Anteil der eigenen Biome im Fenster < 2 %, kein Plan.
   Sonst stapeln sich in jedem Feld die Ebenen aller Planer. `heide_tundra` macht es vor (`profil_anteil_feld`, `biome_fenster`) – bitte in **allen**
   plan.json diese Schlüssel ausgeben: `biome_fenster` (Anteile), `zellen_zustaendig` (Anzahl), `biome_eigen` (Liste).
2. **Budget.** `elfenwald` G4 = 86 811 Instanzen (Deckel 60 000 je Feld und Ebene, davon ≤ 3 000 mit Kollision). Bitte Dichten skalieren oder
   Kleinzeug-Klassen in die Mittelschicht/Grasarten verweisen; `plan.json["kollision_anzahl"]` ausgeben.
3. **Doppelungen zwischen Ebenen.** `mittelschicht` (Querschnitt) und die Biom-Planer setzen beide Sträucher/Farne/Jungbäume. Bitte Abgrenzung
   festlegen und in `verteilung-STATUS.md` dokumentieren: Vorschlag – Biom-Planer liefern Palette, Dichten und Sonderformen des Bioms;
   `mittelschicht` nutzt je Zelle die Regeln des Biom-Planers (gemeinsame JSON `mittelschicht_regeln.json` je Biom) statt eigener Pauschalwerte.
   Alternativ: Biom-Planer setzen keine Mittelschicht-Klassen (strauch, jungbaum, farn, totholz_liegend), nur Boden/Baum/Wasser/Spuren-Besonderheiten.
4. Kleinigkeiten: nur ASCII in `print()` (Windows-Konsole; ich starte zwar mit `-X utf8`, aber Logs werden mit cp1252 weiterverarbeitet);
   `nordkueste` beendet bei fremdem Biom mit Text statt leerem plan.json – bitte leeren plan.json (`instanzen: 0`) schreiben wie die anderen.

Nächster Schritt bei mir: Setzer für das Plan-Format ist in Arbeit; zuerst werden `felsgruppen` + `mittelschicht` in A5 und G4 gesetzt und
gegen die Zielbilder geprüft, dann die Biom-Planer nach dieser Korrektur.
