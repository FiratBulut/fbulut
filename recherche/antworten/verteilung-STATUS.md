# Auftrag 11 – Status der Verteilungs-Arbeiten (Koordinator: Cloud-Session)

Stand: 2026-10-10 16:15 UTC. Korrektur Runde 1 fuer alle 12 Planer abgeschlossen.

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
| felsgruppen (C) | korrigiert, gepusht (synthetisch B4: 55 196 Inst., 3 000 Kollision, 150 Akteure; Kollision in *_kol.f32). zusatzklassen aus felsgruppen_overrides aller Biom-Regeln nach §6 werden gesetzt (z_<name>), Altstellen heide_tundra/wueste/dschungel/lava abgebildet; Nachbesserung: palette/faktor je Biom wieder gelesen, karst_faktor als Zonenfaktor (G6 758 Platten), heide_tundra-Feinparameter wirken, findling_frei eigene Klasse; z_versatz_anteil fuer Eis, wueste-Klassen auf D4 getestet |
| mittelschicht + spuren (D) | korrigiert, gepusht (synthetisch Mittelschicht G4 51 943 / C6 8 147 / A1 Leerplan; Spuren G4 9 564, H5 aue+sumpf 16 551, C6 402). spuren liest spuren_overrides aller neun Biom-Planer (Sonderformen je Biom), mittelschicht kennt relative Hoehenstufen (stufe/stufen/hoehe_rel_baumgrenze_m); hochgebirge-Overrides darauf umgestellt |
| nordkueste (B1) | korrigiert, gepusht (synthetisch B5: 14 083 Inst.; C6 lava Leerplan; H4 Saum, Kollision gedeckelt 2 998). Hinweis: C6 hat echt 3 % bergwald > 2 %-Schwelle, daher dort einige hundert Instanzen moeglich; fuer Leerplan zustaendigkeit.min_anteil_eigen = 0.04 |
| elfenwald (B5) | korrigiert, gepusht (synthetisch G4 mit 17 000 Baeumen: 31 023 Inst., 215 Kollision; Fremdbiom-Feld Leerplan; Saum 30 m) |
| dschungel (B7) | korrigiert, gepusht (synthetisch H6: 30 343 Inst., 2 690 Kollision; G4 Leerplan; G5 Saum) |
| aue (B2) | korrigiert, gepusht (synthetisch E5 21 085 Inst./621 Kollision, H5 Mischfeld 12 836, C6 Leerplan, A5 859; Anteil/Saum nur ueber Landzellen) |
| heide_tundra (B3) | korrigiert, gepusht (synthetisch D2 16 399 / G5 36 674 / F4 Mischfeld 10 595 / D3 Wueste 14 816; E1, C6 Leerplan; Ursache E1: profil_je_biom-Abbildung fremder Biome, gestrichen) |
| hochgebirge (B4) | korrigiert, gepusht (synthetisch D2 35 187 / E2 43 235, Kollisionsdeckel greift / C2 Mischfeld 43 765 davon 1 788 im Saum / C6 Leerplan; Erwartung E1 26 000-34 000) |
| sumpf (B6) | korrigiert, gepusht (synthetisch H5 26 512 Inst./602 Kollision, H4 Mischfeld 8 503 davon 1 319 im Saum, C6 Leerplan statt 5 063; Ursache: Nassmaske galt in jedem Biom) |
| lava (B8) | korrigiert, gepusht (synthetisch C6 40 840 Inst./75 Kollision/28 Spire-Punkte, C5 Mischfeld 17 240 max. 29,1 m Saum, G4 Leerplan; Erwartung Echtdaten C6 28 000-31 000; Basaltsaeulen bleiben im Planer, spire an felsgruppen) |
| wueste_ergaenzung (B9) | korrigiert, gepusht (synthetisch D4 Wuestenfeld 4 158 statt 12 631, E6 Oedland 12 675 statt 49 993, D6 Mischfeld 7 523, G4 Leerplan; mittelschicht_overrides mit palette/faktor statt biom_faktor 0) |

### Abgrenzung Mittelschicht / Biom-Planer (aus verteilung-leere-fuellen.md 8.2)

`mittelschicht_plan.py` ist der einzige Planer der generischen Klassen **strauch, jungbaum, farn, totholz_liegend, totholz_stumpf, totholz_ast, hochstaude, grasbueschel, beere, pilz** (Umbenennung totholz/stumpf/ast → totholz_*; alte Namen in Overrides werden weiter verstanden). Eigene Zusatzklassen nur dort, wo kein Biom-Planer dieselbe Form setzt:

| Klasse | bleibt in | entfällt in (Grund) |
|---|---|---|
| schilf | – | aue, sumpf (Schilfgürtel = Sonderform/Schicht 5 der Biom-Planer) |
| totbaum | elfenwald, dschungel | alle übrigen (Biom-Planer setzen Totbäume in Schicht 2) |
| wurzel | elfenwald, dschungel | sumpf, bergwald, fjord (Sonderform sumpf/nordkueste) |
| kletter | elfenwald, sumpf, dschungel | – (Lianen an Stamm/Wand bleiben Sonderform B7) |
| strauch | – | gletscher, frost, lava (Latschen/Krummholz/Kiefernstrauch = Sonderform hochgebirge/lava) |
| beere (heath/heather) | Preisel-/Heidelbeere | heide, tundra (Heidekraut-Flecken = Sonderform heide_tundra), Dichte 0,02/0,012 bzw. 0,02/0,014 |

**Dschungel:** Palette nach `verteilung-dschungel.md` §3 übernommen (Farne Megascans/EagleFern/SilverLady/BeechFern/`SM_Fern_01a/02a`; Strauch nur `SM_Bush_01a` 0,45–0,8 plus Holunder 05/07/08/09 als Bananen-Ersatz 1,5–2,4 über `netze_massstab`, Gewicht Busch 4 : je Holunder 1; Hochstaude Crownbeard 03/04/07/08 + Pestwurz; Jungbaum Palmen 07–12; Totholz/Stumpf/Wurzel Megascans; Kletter Vines + Ivy; Kikuyu-Gras). Die §3-Tabelle (in G6, H6, I6, I7, G7, H7 Farn/Kletter/Totholz/Stumpf/Wurzel/Pilz = 0, Strauch/Jungbaum/Hochstaude × 0,5) steht als `feld_klassen_faktor.dschungel` mit `nur_ohne_override: true` in den Regeln: Sie gilt nur, solange `dschungel_plan.py` diese Klassen selbst setzt. Seit B7 in Runde 1 einen `mittelschicht_overrides`-Block liefert (und nur noch Lianen, Moospolster, Bäume, Boden, Wasserkante setzt), ist sie inaktiv – sonst blieben die Karstfelder ohne Farn und Totholz. B7 kann Karstfelder über `faktor_je_feld` steuern; `entfernen_je_feld` (G6–I7: `sm_fern_01a,sm_fern_02a`) landet im Mittelschicht-`plan.json["entfernen"]`.

**Heide/Tundra:** Zwergstrauch (Preisel-/Heidelbeere) und Grasbüschel kommen nur noch aus der Mittelschicht; `heide_tundra` setzt künftig nur Heidekraut-Flecken und Sonderformen. Bis `heide_tundra_regeln.json` einen Override-Block hat und `grasbueschel`/`wacholder`/`kruepelkiefer`/`jungwuchs`/`totholz`/`stumpf` nicht mehr selbst setzt, doppeln sich diese Klassen in den zehn Heide/Tundra-Feldern.

Erledigt: wueste_ergaenzung liefert jetzt palette/parameter/faktor fuer Gras, Strauch, Totholz (Wuestenfelder C3-E5 mit 0,2-0,4). alle anderen Biome haben ihre Override-Bloecke.

Pruefpunkt Echtdaten (Hinweis heide_tundra): an plan.json["biome_fenster"] kontrollieren, dass heide/tundra-Gebiete nicht als Kennzahl 0 kodiert sind - sonst werden sie als aue gelesen und der heide_tundra-Planer bleibt dort leer.

### Runde-2-Punkte (gesammelt)

- erledigt: mittelschicht relative Hoehenstufen; hochgebirge beere/grasbueschel/alpenrose nutzen sie (synthetisch E2: Alpenrose nur noch Krummholz/Matte).
- spuren: nicht umgesetzt mangels Netzen - Muehle, Boot, Laternen, Steinbruecke, Gipfelkreuz, Unterstand, Seilbruecke (Einkaufsliste); Torfstich ohne Instanzen-Spur.
- erledigt: felsgruppen `z_versatz_anteil` (Eis haengt 0,6-4,7 m ueber Boden), lava `spire` als echte Zusatzklasse.
- Echtdaten-Pruefpunkt sumpf: liegen Teiche/Gewaesser in eigner.r8 auf Kennzahl 0, zaehlen sie als aue; der Sumpf-Planer setzt dann Schilfguertel nur ueber den Saum. Falls so, Gewaesser im Sumpf dem Sumpf-Rezept zuordnen oder Wasserzellen dem Biom der naechsten Landzelle zuweisen (Runde 2, alle Planer).
- erledigt: felsgruppen/lava - Spires genau nach Lava-Plan-Punkten (auch 0), Ersatzmaske nur ohne Lava-Plan; netz/yaw_grad aus dem Punkt werden uebernommen.
- mittelschicht liest die vorhandene Namaqualand-Ebene in C3-E5 nicht als belegt: einzelne Mittelschicht-Straeucher koennen neben vorhandenen stehen (Runde 2).
- Override-Faktoren aller Biome nur synthetisch kalibriert: nach erstem gemeinsamen Echtlauf nachstellen.
- erledigt: wueste-Felsklassen synthetisch D4 getestet (terrassenkanten 632, felsnadel 3 Akteure).
