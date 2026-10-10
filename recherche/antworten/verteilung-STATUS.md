# Auftrag 11 – Status der Verteilungs-Arbeiten (Koordinator: Cloud-Session)

Stand: 2026-10-10 19:40 UTC. Runde 4 in Arbeit (alle 12 Planer).

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

Gesamtantworten: `verteilung-biome-witcher.md` (Auftrag 11) und `verteilung-korrektur-runde1.md` (Korrektur Runde 1).

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

## Runde 2 (Auftrag `auftraege/verteilung-korrektur-runde2.md`, erste Editor-Bilder 10.10. 18:15 lokal)

| Teil | Aufgabe | Stand |
|---|---|---|
| felsgruppen | Gruppen auf 300 m als Form (Hauptfels 4-10 m, Bloecke 1,5-4 m eng, Gruppe 10-30 m, halb so viele Gruppen; Felskrone an Graten, Blockstrom am Hangfuss); flache Platten nur auf Kies/Geroell/Fels/Felsplatte >= 100, >= 50 % eingegraben, an der Normale; Kleinmaterial nur im Kontaktsaum; gesperrte Netze | fertig, gepusht (synthetisch A5-artig: Gruppen 2 381 -> 515, Instanzen 39 802 -> 10 696, Hauptfels Grat/Kuppe Median 5,8 m / max 6,9 m, Gruppenbreite Median 24,7 m, Platten auf Gras 691 -> 0, Kleinmaterial ausserhalb Saum 34 % -> 0 %; B4 analog). Ursache: Hauptfels nur in 3 Klassen und ohne Zielhoehe, Faecher-Raster 9-16 m streute Kleinmaterial, Budget duennte Satelliten aus. Gruppenzahl 22-29 % statt 50 %: fuer mehr Gruppen klassen.band.raster_m bzw. klassen.fuss.strom_abstand_m in felsgruppen_regeln.json verkleinern. Hauptfels max ~7,6 m wegen 14-m-Fussbreitengrenze. Pruefkamera grat_300m fuer A5 in plan.json |
| spuren + mittelschicht | 1-3 sichtbare Spuren-Ensembles je Feld an Wegen/Orten statt vieler Einzelteile; Mittelschicht in Sichtachsen von Lichtungen lichter; gesperrte Netze | fertig, gepusht (synthetisch A5/G4 je 3 Ensembles mit 3-6 Teilen, 6 Typen: Wegkreuz, Mauerrest+Steinmann, Rastplatz, Ortsrand, Schrein, Ruinenrast; verstreute Einzelteile A5 57 -> 11, G4 40 -> 12; Mittelschicht G4 45 408 -> 45 139, im Sichtkorridor -30 %; gesperrte Netze 0). Planungsreihenfolge: spuren vor mittelschicht (Ensembles sind Blickziele) |
| Biom-Planer (9) | gesperrte Netze SM_Column_03 / SM_Main_Arch_01 entfernen; selbst gesetzte Platten nach derselben Lagen-Regel oder an felsgruppen abgeben; kein Kiesel-Hangteppich | fertig, gepusht: gesperrte Netze in elfenwald/lava/dschungel ersetzt (SM_Column_02, SM_Wall_01); Platten nur auf Kies/Geroell/Fels/Felsplatte >= 100 und nie wo Gras/Wiese ueberwiegt, >= 50 % eingegraben (nordkueste strandplatte, hochgebirge schneefleck 6 000 -> 1 505); Kiesel-Teppich synthetisch 0 (nordkueste, hochgebirge, aue, heide_tundra); Bloecke > 0,8 m aus elfenwald an felsgruppen, lava basaltsaeule an felsgruppen (aktiv) |

## Runde 3 (Auftrag `auftraege/verteilung-korrektur-runde3.md`, Bilder 10.10. 19:15 lokal)

| Teil | Aufgabe | Stand |
|---|---|---|
| felsgruppen | 8-20 Formgruppen je Feld mit Hero 10-30 m (Massive/Huge Nordic Coastal Cliff, Sharp_Cliff, big_rock_wall, Big_Rock; Skalierung 1,0-2,0, Akteure, 35-60 % eingegraben) auf markanten, von Taelern/Wegen sichtbaren Graten/Kuppen; Satelliten 2-6 m, Blockstrom; keine Gruppe auf Wiese ohne Hangknick; rote IcelandicBoulder (AncientContent) nur canyon/oedland/wueste/lava; uchoab3fa gesperrt | fertig, gepusht (synthetisch, Echtdaten ungetestet) |
| Biom-Regeldateien | rote IcelandicBoulder aus nordkueste, heide_tundra, hochgebirge entfernen, grauer Ersatz | fertig, gepusht: ersetzt durch SM_MossyForestBoulder_03/04, SM_ground_rock_01, SM_mountain_rock_big_02_4 (ueber Schneegrenze ohne Moos); assets-taxonomie.json: rote Findlinge nur noch canyon/oedland/wueste/lava geeignet |

**Erwartete Zahlen Runde 3 (Echtdaten, aus synthetischem Test abgeleitet):**

| Feld | Formgruppen | Instanzen gesamt | Akteure |
|---|---|---|---|
| A5 | 10-16 | ca. 4 800-5 600 | ca. 45-60 |
| B4 | 8-14 | - | - |
| G4 | 0-3 | - | - |

- Hero-Klippen (Akteure, Kollision, Massstab 1,0-2,0, 35-60 % eingegraben, Rueckseite hangwaerts): rcygn, vfmjadufa, vdssailfa, veqnci0db, MassiveNordicCoastalCliff_01, HugeNordicCoastalCliff_01/02; Canyon Sandstein-Klippen, Lava LavaSpire_02. Groesse 18-38 m breit (Median ca. 25-30 m), sichtbar 5-18 m hoch (Median ca. 8-12 m). Synthetisch: A5 10, B4 8, G4 1 Formgruppen.
- Auswahl: Kruemmung + Prominenz + Sichtbarkeit von Weg/Tal/Wasser aus 300-1 500 m, Mindestabstand 120 m, Hangknick Pflicht (Wiese ohne Hangknick 0). Je Formgruppe 3-6 Satelliten 2-6 m und Blockstrom.
- Runde-2-Gruppen (4,5-8,5 m) nur noch als Begleiter: max. 3 je Formgruppe, sonst max. 6 je Feld.
- SM_Big_Rock_0* und big_rock_wall_02 erreichen auch bei Massstab 2,0 keine 10 m und sind aussortiert (`groesse_min_m` auf 8 senken, falls gewuenscht). Graue /Game/Megascans/.../SM_IcelandicBoulder_* gibt es im Inventar nicht; Ersatz pkeeM/skjsL, MossyForestBoulder_03/04, mountain_rock_big_02_4.
- Vor dem Setzen pruefen: offene Seite der Klippennetze angenommen auf lokal +y (veqnci0db +x) - falls in Kamera `formgruppe_front_120m` von vorn offen, je Netz `"rueckseite": "-y"` in `formgruppen.hero.paletten`; Pivot unten angenommen (keines der Hero-Netze in netze_masse.json). Pruefkameras in plan.json: formgruppe_300m_1..3, formgruppe_front_120m, formgruppe_flanke_120m. Klasse `band` unveraendert (Hebel `klassen.band.p`).

## Runde 3b (Auftrag `auftraege/verteilung-korrektur-runde3b.md`, Nahbilder 10.10. 20:20 lokal)

| Teil | Aufgabe | Stand |
|---|---|---|
| hochgebirge + mittelschicht | Pflanzen nur wo lage_Schnee < 60 und lage_Eis < 30; auf Schnee nur Steine/Flechtensteine (tiefer eingegraben) und Eiszapfen an Felskanten | fertig, gepusht (synthetisch E1-artig: Pflanzen auf Schnee/Eis hochgebirge 679 -> 0, mittelschicht 161 -> 0; Steine auf Schnee 40-60 % eingegraben; Bergwiese -0,4 %; polster auf Wiese +11 %, weil Klassenbudget nicht mehr auf Schnee verbraucht wird). Neuer Schluessel lagen_max (KONVENTIONEN §6); mittelschicht sperrt Pflanzen auf Schnee/Eis global in allen Biomen (lagen_max_pflanzen) |
| nordkueste + dschungel | `entfernen`-Filter je Feld begruenden, erwartete Zahl entfernter Baeume; ohne Freigabe nichts entfernen | fertig, gepusht: Schalter `--ersetzen` / Regel `entfernen_aktiv` (Standard aus). Ohne Freigabe `entfernen` leer, Kandidaten in plan.json["entfernen_vorschlag"] (eigen/Saum/fremd, je Netz). nordkueste-Filter war zu breit (traf liegende Staemme und Jungpflanzen, zaehlte Meerzellen) - korrigiert. Details: verteilung-entfernen.md |

### entfernen-Filter je Feld (Runde 3b, Schaetzung Dichte x Flaeche, ohne Echtdaten)

Ohne Freigabe entfernt kein Planer etwas. Mit `--ersetzen` greift nordkueste nur, wenn das Feldland zu >= 85 % eigenes Biom ist und <= 5 % der
Kandidaten in Saum-/Fremdzellen stehen, und nur auf Baeume, die der Planer selbst neu setzt. Der Setzer sollte nur auf `entfernen_nur_ft`
(`FT_EL_WIT_`/`FT_EL_BST_`) wirken, sonst trifft er eigene neue Baeume. Exakte Zahl lokal: Planer ohne `--ersetzen` laufen lassen und
`entfernen_vorschlag` lesen; mit Freigabe steht sie in `entfernen_zaehlung`.

**nordkueste** (Kiefern/Tannen):

| Feld | Biomanteil (Land %) | Begründung | Kandidaten (Schätzung) | erwartet entfernt: ohne Freigabe / mit `--ersetzen` | neue Bäume: ohne Freigabe (ergänzen) / mit `--ersetzen` |
|---|---|---|---|---|---|
| A3 | bergwald 92, aue 8 (16) | Filter möglich: Kiefern-Monokultur am Hang → Artenmix | 150–650 | 0 / 150–650 | 70–200 / 200–600 |
| B3 | bergwald 100 (47) | Filter möglich: reiner Bergwald, Monokultur → Mix mit Tanne, Birke, Hainbuche, Totbaum | 300–1 550 | 0 / 300–1 550 | 150–450 / 450–1 400 |
| I3 | bergwald 94, elfenwald 6 (31) | Filter möglich; der Elfenwald-Planer entfernt hier nichts (6 % < 50 %) | 200–1 000 | 0 / 200–1 000 | 100–300 / 300–900 |
| A4 | bergwald 92, aue 8 (36) | Filter möglich: FELS7_A4 zeigt die Kiefern-Monokultur am Fjordhang | 250–1 150 | 0 / 250–1 150 | 100–350 / 350–1 000 |
| B4 | bergwald 100 (100) | Filter möglich: steiler Bergwald, Waldgrenze 420–560 m, darüber nur Krüppelkiefer | 600–3 050 | 0 / 600–3 050 | 300–900 / 900–2 750 |
| A5 | kueste 75, bergwald 14, aue 11 (24) | Filter möglich: Klippenküste, Küstenkiefer/-eiche statt Forstkiefer. Entfällt, wenn > 5 % der alten Kiefern in den Aue-Zellen stehen | 150–650 | 0 / 0–650 | 70–200 / 200–600 |
| B5 | bergwald 79, kueste 21 (98) | Filter möglich: Küste → Hangwald → Grat; Synthetiktest mit Filter aktiv | 600–2 950 | 0 / 600–2 950 | 300–900 / 900–2 650 |
| H2 | kueste 78, elfenwald 20 (39) | kein Filter: Landanteil 78 % < 85 %, sonst würden Elfenwald-Bäume gelöscht | 200–1 000 | 0 / 0 | 100–300 / 100–300 (ergänzen) |
| I4 | bergwald 78, elfenwald 21 (63) | kein Filter: 78 % < 85 % | 300–1 600 | 0 / 0 | 150–500 / 150–500 |
| I5 | bergwald 68, dschungel 21, sumpf 11 (50) | kein Filter: 68 % < 85 % | 350–1 700 | 0 / 0 | 150–500 / 150–500 |
| B6 | bergwald 63, aue 24, lava 13 (63) | kein Filter: 63 % < 85 % | 350–1 800 | 0 / 0 | 200–550 / 200–550 |
| C1 | fjord 31, gletscher 69 (38) | kein Filter: nur Fjordzellen bis zur Gletschergrenze | 70–350 | 0 / 0 | 30–100 / 30–100 |
| D1 | fjord 26, gletscher 72 (40) | kein Filter | 60–300 | 0 / 0 | 30–90 / 30–90 |
| C2 | fjord 23, gletscher 46, tundra 21 (65) | kein Filter | 100–500 | 0 / 0 | 50–150 / 50–150 |
| D2 | fjord 19, tundra 47, gletscher 34 (100) | kein Filter | 150–700 | 0 / 0 | 70–200 / 70–200 |
| B2 | bergwald 20, gletscher 80 (25) | kein Filter | 30–150 | 0 / 0 | 10–40 / 10–40 |
| C3 | bergwald 6 (62) | kein Filter: nur Saumfeld | 40–200 | 0 / 0 | 20–50 / 20–50 |
| C4 | bergwald 6 (100) | kein Filter: nur Saumfeld | 60–300 | 0 / 0 | 30–90 / 30–90 |
| C5 | bergwald 6 (100) | kein Filter: nur Saumfeld | 60–300 | 0 / 0 | 30–90 / 30–90 |
| H1, A2, I2 | kueste 19 / bergwald 19 / bergwald 20 (Land 0) | kein Land, also keine Bäume | 0 | 0 / 0 | 0 / 0 |
| **Summe** | | **Filter möglich nur in A3, B3, I3, A4, B4, A5, B5** | | **0 / ≈ 2 100–11 000** | |

**dschungel** (keine Baeume; nur Witcher-Lianen `sm_vines_01a`):

| Feld | Biomanteil (Land %) | Begründung | Bäume entfernt | Lianen `sm_vines_01a`: ohne Freigabe / mit `--ersetzen` (Schätzung) | Farne (Teil D, Vorschlag) | neue Bäume (Ergänzung, beide Fälle) |
|---|---|---|---|---|---|---|
| G6 | dschungel 97, aue 3 (80) | Filter möglich: Lianen an Stämmen und Wänden statt Streuung | 0 | 0 / 400–1 950 | nach Freigabe | 3 950–7 100 |
| H6 | dschungel 100 (94) | Filter möglich (Synthetiktest aktiv) | 0 | 0 / 500–2 400 | nach Freigabe | 4 800–8 600 |
| I6 | dschungel 100 (63) | Filter möglich | 0 | 0 / 300–1 600 | nach Freigabe | 3 200–5 750 |
| G7 | dschungel 73, aue 27 (10) | kein Filter: 73 % < 85 %; im Synthetiktest standen 29 % der Kandidaten in Aue- oder Saumzellen | 0 | 0 / 0 | nein | 350–650 |
| H7 | dschungel 76, aue 24 (22) | kein Filter: 76 % < 85 % | 0 | 0 / 0 | nein | 850–1 550 |
| I7 | dschungel 76, aue 24 (15) | kein Filter: 76 % < 85 % | 0 | 0 / 0 | nein | 600–1 050 |
| G5 | dschungel 22, heide 77 (100) | kein Filter (keine Kandidaten in den Regeln) | 0 | 0 / 0 | nein | 1 100–2 000 |
| H5 | dschungel 12, sumpf 78 (99) | kein Filter | 0 | 0 / 0 | nein | 600–1 100 |
| I5 | dschungel 21, bergwald 68 (50) | kein Filter | 0 | 0 / 0 | nein | 550–950 |

## Runde 4 (Auftrag `auftraege/verteilung-korrektur-runde4.md`, Meer fehlt in karte_wasser, 10.10. 21:40 lokal)

Regel verbindlich in `verteilung-KONVENTIONEN.md` §1b: Meer = hoehe < 0 und karte_wasser == 0; unter -0,3 m nichts; -0,3..0 nur Meeres-Rollen;
0..+0,3 m im Kuestensaum nur wasserkante/strand; karte_wasser als Sperre/Abstand/Landbezug durch wasser_alle ersetzt; plan.json meldet
`meer_zellen`, `meer_gefiltert`.

| Planer | Stand |
|---|---|
| felsgruppen, mittelschicht, spuren | laeuft |
| nordkueste, aue, heide_tundra | fertig, gepusht (synthetisch unter 0 m unzulaessig: nordkueste 783 -> 0, aue 20 342 (52 %) -> 0, heide_tundra Kuestensaum 420 -> 0; Gesamt nordkueste 28 504 -> 42 913, aue 39 244 -> 16 286, heide_tundra 8 565 -> 8 136). aue-Ursache bestaetigt: Meer mit eigner 0 zaehlte als aue, Kuestenfeld B5 jetzt Leerplan. nordkueste waechst, weil Kuestenklassen (tang, treibholz, strandkiesel = meer_rolle; strandplatte = strand) jetzt das echte Meer finden: 5 206 erlaubte Meeres-Rollen zwischen -0,3 und 0 m, hoechstens 8 m seewaerts der Wasserlinie (`meer.meer_band_m` = 8 in nordkueste_regeln.json). Wirkt das zu dicht, Faktoren der Strandklassen oder meer_band_m senken |
| hochgebirge, elfenwald, sumpf | fertig, gepusht (synthetisch: hochgebirge C2 Kuestensaum 905 -> 15 nur Bach-Steine, Gesamt 35 440 -> 34 570; elfenwald G4 13 -> 5 nur Wasserkante, 41 886 -> 42 145; sumpf H5 unter 0 m 868 -> 0, Saum 1 763 -> 0, 47 930 -> 47 823, Suesswasser-Klassen unveraendert). Nachruestung Landzellen-Bezug fuer Biom-Anteil laeuft |
| dschungel, lava, wueste_ergaenzung | fertig, gepusht (synthetisch Boden unter 0 m: dschungel G6 2 -> 0, lava C7 14 245 -> 0, wueste E7 7 969 -> 0; Gesamt 15 588 -> 15 171 / 32 892 -> 32 651 / 18 783 -> 10 428; Kuestensaum 0-0,3 m nur Wasserkante/Strand, im Dschungel vorher 95 Baeume/Palmen dort). Hinweis: z unter 0 durch Eingraben auf Strand ab 0 m moeglich (dschungel 87, lava 257, wueste 1) - kein Meer |
