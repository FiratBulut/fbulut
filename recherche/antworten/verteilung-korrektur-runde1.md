# Antwort zu Korrektur Runde 1 (Auftrag 11)

Stand: 10.10.2026. Alle 12 Planer sind korrigiert, synthetisch rauchgetestet und gepusht. Echtdaten-Läufe gab es in der Cloud nicht.
Verbindliche Regeln: `verteilung-KONVENTIONEN.md`. Einzelstand je Planer: `verteilung-STATUS.md`. Jeder Bericht hat einen Abschnitt
„Korrektur Runde 1“ mit Ursache, Änderungen und Testzahlen.

## Kurzfazit zu den vier Punkten

1. **Zuständigkeit:** umgesetzt in allen Biom-Planern. Biom je Zelle aus `eigner.r8` und `welt.json`; Kennzahl 0 ist aue, Vulkanregion
   ist lava. Bebaut werden nur eigene Zellen plus 30 m Saum mit linear fallender Dichte. Unter 2 % Eigenanteil entsteht ein leerer
   `plan.json`. Anteil und Saum zählen nur Landzellen ohne `karte_wasser`, damit Meer mit Kennzahl 0 den aue-Anteil nicht aufbläht.
   Neue Schlüssel in jedem `plan.json`: `biome_fenster`, `zellen_zustaendig`, `biome_eigen`, `kollision_anzahl`, `biome_fenster_bezug`.
2. **Budget:** hart in allen Planern, 60 000 je Feld und Planer, davon höchstens 3 000 mit Kollision. Gekappt wird deterministisch, jede
   Ausdünnung steht als WARNUNG im Log. elfenwald G4 sinkt synthetisch von 86 811 auf 31 023.
3. **Doppelungen:** entschieden und in `verteilung-STATUS.md` dokumentiert. `mittelschicht_plan.py` setzt als einziger Planer strauch,
   jungbaum, farn, totholz_liegend/stumpf/ast, hochstaude, grasbueschel, beere und pilz. Er liest je Biom `mittelschicht_overrides` aus
   der Regeldatei des Biom-Planers. Biom-Planer setzen nur noch Sonderformen. Felsen über 0,8 m kommen nur aus `felsgruppen_plan.py`,
   Spuren nur aus `spuren_plan.py`; beide lesen ebenfalls Overrides der Biome.
4. **Kleinigkeiten:** `print()` überall nur ASCII. nordkueste schreibt in fremden Biomen einen leeren `plan.json`. Fehlende Pflichtdatei
   oder ungültiges Feld enden mit Exit-Code 2.

## Ursachen der Fremdbiom-Instanzen

| Planer | Ursache | Behoben durch |
|---|---|---|
| dschungel | Fallback auf das dominante Feldbiom bebaute fremde Felder | Fallback nur ohne `eigner.r8`/`welt.json` |
| elfenwald | zu hohe Bodendichte, dazu nicht deterministischer Python-`hash()` | Dichte −30 bis −38 %, CRC32 |
| sumpf | Nässe-Maske galt in jedem Biom; Moos auf Lava wurde Bultenzone | Maske nur in Sumpf-Zellen |
| heide_tundra | `profil_je_biom` bildete fremde Biome mit Faktor ab, Lagen-Regel machte jede Heide-Zelle zuständig | beide Regeln gestrichen |
| aue, nordkueste, hochgebirge, lava, wueste | Kennzahl 0 wurde als Feldbiom gelesen, kein Saum | Kennzahl 0 = aue, 30-m-Saum |

## Synthetische Testzahlen nach der Korrektur

| Planer | Eigenes Feld | Mischfeld (Saum) | Fremdfeld |
|---|---|---|---|
| felsgruppen | B4 55 681 | – | – |
| mittelschicht | G4 51 943 | C6 8 147 | A1 leer |
| spuren | G4 9 564, H5 16 551 | C6 402 | A1 leer |
| nordkueste | B5 14 083 | H4 | C6 leer |
| aue | E5 21 085 | H5 12 836 | C6 leer |
| heide_tundra | G5 36 674 | F4 10 595 | E1, C6 leer |
| hochgebirge | E2 43 235 | C2 43 765 | C6 leer |
| elfenwald | G4 31 023 | – | Fremdfeld leer |
| sumpf | H5 26 512 | H4 8 503 | C6 leer |
| dschungel | H6 30 343 | G5 | G4 leer |
| lava | C6 40 840 | C5 17 240 | G4 leer |
| wueste_ergaenzung | E6 12 675, D4 4 158 | D6 7 523 | G4 leer |

Erwartung mit Echtdaten laut Berichten: hochgebirge E1 26 000–34 000, lava C6 28 000–31 000, aue A5 1 000–1 400,
heide_tundra A5/E1/C6 0.

## Zusätzlich erledigt

- `felsgruppen` liest die `zusatzklassen` aller Biome nach KONVENTIONEN §6. Dazu gehören Küstenfelsen, Eisvorhänge an der Wand,
  Karstfüße und -platten, Terrassenkanten, Felsnadeln und Lava-Spires aus den Punkten des Lava-Plans.
- `spuren` setzt die Sonderformen der Biome, zum Beispiel Hecken, Kopfweiden, Stege, Pferche, Tempelruinen, Karren und Schwefelgruben.
- `mittelschicht` kennt relative Höhenstufen wie `hochgebirge_plan.py`. hochgebirge nutzt sie für Beere, Grasbüschel und Alpenrose.

## Bitte lokal prüfen

1. `biome_fenster` in den ersten Echtläufen lesen: Heide, Tundra, Sumpf oder Teiche auf Kennzahl 0 würden als aue zählen.
2. C6 hat 3 % bergwald. nordkueste setzt dort einige hundert Instanzen. Für einen Leerplan `min_anteil_eigen` auf 0.04 setzen.
3. Override-Faktoren nach dem ersten gemeinsamen Lauf nachstellen. Sie sind nur synthetisch kalibriert.
4. Offene Punkte für Runde 2 stehen in `verteilung-STATUS.md` unter „Runde-2-Punkte“.
