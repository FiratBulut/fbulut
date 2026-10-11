# Antwort zu Auftrag 13f – Korrekturen an den Sehenswürdigkeiten-Planern nach dem 1-m-Lauf

Stand 11.10.2026. Bergwald-Pilot: Commit **`68739d4`**. Alle Biome: Commit **`9e180f5`** (enthält auch die
Zwischenstände `29af1dd`, `efded23`, `7184139`). Diese Antwort steht im Commit danach.

## Kurzfazit

- **Alle Punkte A1–A13 und B sind an der Quelle behoben**, bis auf die Niagara-User-Parameter (B, nicht belegt → so
  gelassen) und C (nur zur Kenntnis).
- **Neues Modul `sehens_lib/bach.py`:** Jeder Bach wird jetzt gestempelt.
  - Enden: Ein Bach endet auf dem Seeumriss (Spiegel = See + 2 cm). Ein Abfluss beginnt auf dem Seespiegel.
  - Mündung zählt nur in Epic-Gewässer. Sonst läuft der Bach entlang der Tiefenlinie weiter, oder er endet
    `versickert` mit mindestens 25 m.
  - Der Spiegel ist eine Treppe: Becken ≤ 3 % und ≥ 3 m, dazwischen Stufen. Die Zahlen kommen aus dem Regelwerk
    Auftrag 15. Die Stufen stehen explizit im Bach (`stufen`).
  - Querprofil wie 15b: Wasserkante innen, Bett = Spiegel − Tiefe, Ufer ≥ Spiegel + 5 cm.
  - Der Spiegel im Plan **ist** das gestempelte Bett + Tiefe.
- **Prüfer:** Neue FEHLER-Regeln für A4, A9/A13 (Mündung) und A12 (Querprofil), Seeufer, die Schutzzone an Wegen
  und Orten sowie `materialwuensche_biom`.
- **2 m, alle 15 Planer:** Prüfer **0 FEHLER**, zwei Läufe byteidentisch.
- **Synthetische 1-m-Welt (2-m-Daten hochgerechnet):** 14 von 15 Biomen 0 FEHLER. Es bleibt 1 FEHLER:
  gletscher_06 `klammbach_oben`, Ufer an 1 von 26 m 0,31 m unter dem Spiegel.
- **Selbsttest:** 0 FEHLER. Neuer Schritt 11 mit Fällen für A1, A2, A3, A4, A5, A8, A10, A12 und A13.
- **Lokale Übergangslösungen,** die entfallen können: Laufzeit-Korrektur A1/A2, `--korrektur-baumfuss` (A3),
  Normalisierung der Bachenden in `p2_einbau.py` (A4), Materialwunsch-Übernahme in der Brücke (A7), Umsortieren
  der Felder (A10), Abdeckungsmaske Karsee (B). Bitte erst nach dem lokalen 1-m-Lauf mit diesem Stand abschalten.

## Bergwald-Pilot (bergwald_03 Säulenhain + bergwald_06 Karsee)

Commit `68739d4` (vorab gepusht), Feinschliff in `9e180f5`.

**bergwald_03:**
- Die Riesentannen stehen auf dem Boden am Pivot (A3).
- Auf 2 m liegen die Unterkanten jetzt 1,2–1,5 m unter dem Boden. Das ist das Eingraben des Rezepts
  (`eingraben_m` 0,6–1,0 m geteilt durch die Normale). Vorher waren es 0,9–3,7 m, eine Tanne schwebte.

**bergwald_06 Karsee:**
- **Ersetzt den alten Lauf:** Ja. Der Karsee liegt mitten im Houdini-Lauf `R_M2_P0__WASSER`, der von Westen nach
  Osten durch das Kar fällt.
- **`zulauf_west`** beginnt jetzt im alten Lauf. Der Anker `rinne_w` sucht dafür mit `ohne_wasser: false`. Der Zulauf
  endet auf dem Umriss.
- **`abfluss`** läuft im alten Lauf nach Osten und geht am Fensterrand in ihn über (`muendung_houdini`).
- **Stufen (2 m):**
  - `zulauf_sued`: 7 Stufen, größte 8,7 m.
  - `zulauf_west`: 7 Stufen, größte 6,4 m.
  - `abfluss`: 12 Stufen. Die größte ist 12,0 m über die Karschwelle direkt hinter der Seelippe.
- **Houdini-Netz:** in drei Umrissen ausgeblendet, als `bestand_ausblenden` mit `art: houdini`:
  - See + 2 m: 768 m²
  - Zulauf West: 163 m²
  - Abfluss: 406 m²
- **`ist_wasser_r_m`** 68.
- **`tiefe_m`** ist die Tiefe nach dem Stempel: 4,4 m auf 2 m. Das Rezept hat 3,5 m (`tiefe_regel_m`). Lokal auf
  1 m wird der Wert größer sein (gemeldet: 5,39 m).
- **Prüfer auf 2 m:** 0 FEHLER, 0 WARNUNG. Auf der synthetischen 1-m-Welt ebenfalls 0 FEHLER.

## Punkte im Einzelnen

Kürzel der Dateien: `lib/` = `recherche/antworten/skripte/sehens_lib/`.

| Punkt | Was geändert ist | Datei(en) | Übergangslösung entfällt? |
|---|---|---|---|
| **A1** | Biom über die Kennzahl (schon f04230b). Neu: Selbsttest mit synthetischem 1-m-Ordner (Kennzahl 3 = fjord, 5 ohne Rezept = lava). | `lib/daten.py`, `lib/selbsttest.py` | ja |
| **A2** | `lade_1m` liest `baeche/baeche_alle.json`, wenn vorhanden; sonst wie bisher `baeche.json` + `baeche_r2.json`. Selbsttest dazu. | `lib/daten.py` | ja |
| **A3** | `platziere(bezug="mitte")` mit Fußradius ≥ 1,5 m: `z = Boden(Pivot) − eingraben − max(0, bmin_z·sz)`. Selbsttest am Hang. | `lib/instanzen.py` | ja (`--korrektur-baumfuss`) |
| **A4** | Siehe Abschnitt A4 unten. | `lib/bach.py`, `lib/rezept.py`, `lib/sehens_pruefen.py` | ja (Normalisierung in `p2_einbau.py`) |
| **A5** | Siehe Abschnitt A5 unten. | `lib/stempel.py`, `lib/rezept.py` | – |
| **A6** | Gruppen-Feld `"z_frei": true`. `plan.json` führt `z_frei_index`. Der Prüfer zählt diese Stücke nicht als „schwebt“ oder „im Meer“. Gesetzt für dschungel `luftwurzeln`, `nadellianen`, `lianenvorhang`; bergwald `efeu_nordwand`; kueste `efeu_kante`; aue `efeu`, `stammefeu`; canyon `ranken`. | `lib/rezept.py`, `lib/instanzen.py`, `lib/sehens_pruefen.py`, Rezepte | – |
| **A7** | `orte.json` oben `"materialwuensche_biom": [...]` (alle Wünsche des Bioms). Beim Ort stehen sie weiter genau einmal. Der Prüfer verlangt, dass jeder Ort-Wunsch in der Liste steht. | `lib/rezept.py`, `lib/sehens_pruefen.py` | ja (Brücke) |
| **A8** | Siehe Abschnitt A8 unten. | `lib/bach.py` | ja |
| **A9** | Siehe Abschnitt A9 unten. | `lib/bach.py`, `lib/rezept.py` | ja |
| **A10** | `feld_von_m`/`feld_von_cm`: `s = floor((x_cm + 473050)/100800)`, `r = floor((y_cm + 406050)/100800) + 1`. `feld_grenzen_m` passt dazu (Grenze = Mitte der Zelle j = 1008·s). Siehe Abschnitt A10 unten. | `lib/daten.py` | ja (Umsortieren) |
| **A11** | Siehe Abschnitt A11 unten. | `lib/stempel.py`, `lib/rezept.py` | ja |
| **A12** | Siehe Abschnitt A12 unten. | `lib/bach.py`, `lib/stempel.py`, `lib/sehens_pruefen.py` | ja |
| **A13** | Siehe Abschnitt A13 unten. | `lib/stempel.py`, `lib/rezept.py`, Rezepte | ja |
| **B** | Siehe Abschnitt B unten. | Rezepte, READMEs | Karsee-Maske: ja |
| **C** | Nur zur Kenntnis. Keine Änderung nötig. Das Kürzen gebauter Epic-Bäche (`bestand_ausblenden` art `bach`) und neu `art: houdini` (Umriss) liegen lokal. | – | – |

### A4 – Bachenden an Seen

- Ein Bach mit eigenem Zielsee wird am Umriss abgeschnitten. Der Endpunkt liegt auf dem Umriss, sein Spiegel ist
  See + 2 cm. Erreicht der Lauf den See nicht, wird er gerade bis ans Ufer verlängert (HINWEIS).
- `abfluss_von` beginnt am Auslass auf dem Seespiegel. Bis hinter die Lippe bleibt der Spiegel flach. Danach läuft
  der Bach radial vom See weg, nicht am Ufer oder Damm entlang.
- Ein Bachende liegt nie unter dem Spiegel des Ziels.
- Neue Prüferregeln (FEHLER):
  - Ende unter dem Seespiegel
  - Punkte im See
  - Abfluss beginnt unter dem Seespiegel
  - Ende unter dem Spiegel des Epic-Ziels
- Beim Seeufer-Check zählen Zu- und Abflüsse als offen.
- Ergebnisse auf 2 m:
  - bergwald_06 `zulauf_sued` endet bei 256,19 m (See 256,17 m).
  - Der Abfluss beginnt bei 256,17 m.
  - aue_01 `ueberlauf` endet bei 34,14 m über `B_R2_R_M1_M1_04` (33,87 m).

### A5 – Kleine Senken

- `Stempel.fertig(senken_fuellen=True)` füllt Senken < 50 m² und < 0,5 m auf: Priority-Flood im Fenster, nur
  anheben, nur Senken, die der Stempel erzeugt hat, nicht im Schutzstreifen. Die Fläche wird wie bei der
  Senkenprüfung gemessen (Fülltiefe > 0,3 m).
- Größere Senken brauchen `senke_begruendung`. Per Ort sind eigene Grenzen möglich:
  `"senken_fuellen": {"max_flaeche_m2", "max_tiefe_m"}`.
- **lava_01:** keine Absicht. Die Kerben sollen zur Front hin abfallen. Die Senke wird mit Grenzen 400 m² / 1,5 m
  aufgefüllt (synthetisches 1 m: 120 m², bis 0,68 m).
- Synthetisches 1 m: dschungel_01 Mondtor (32 m², 0,36 m) wird aufgefüllt.
- dschungel_05 und dschungel_06 haben jetzt eine `senke_begruendung` (Karstkessel, Schwinde-Trichter).

### A8 – Spiegel als Treppe

- Der Spiegel ist eine Treppe. Die Becken haben ≤ 3 % Gefälle und sind ≥ 3 m lang. Grundlage ist das Regelwerk
  Auftrag 15 über `gefaelle_regelwerk.Regelwerk`, nur importiert: `becken_laenge_min`, `abstand_L`,
  `becken_gefaelle_hart`, `art_bereich`, `hoehe_max_einzeln`.
- Jede Stufe hat zwei Punkte: Lippe → Fuß 0,5 m (`stufen.zwei_punkte`).
- In `orte.json` steht je Bach `"stufen": [{"lippe_cm", "fuss_cm", "fall_m", "art"}]`.
- Auf 2 m: 370 Stufen in 42 Bächen (143 schnelle, 89 stufe, 138 fall). Selbsttest: Becken ≥ 3 m und ≤ 3 %.

### A9 – Mündungen

- Als Mündung zählen nur Epic-Gewässer (`baeche_alle`, `wasser_welt` Flüsse und Seen, `teiche`). `karte_wasser`
  zählt nicht mehr.
- `muendung: auto` sucht am Ende. Findet es nichts, läuft der Bach entlang der Tiefenlinie weiter: erst steilster
  Abstieg, dann D8 auf dem gefüllten Gelände, bis 40 m (`verlaengern_m`). Sonst endet er `versickert` mit ≥ 25 m.
- Ein Bestandsgewässer, das höher liegt als der Bachanfang, ist keine Mündung (aue_07: vorher 7,65 m darunter).
- Der Prüfer meldet `suesswasser_bestand` als FEHLER und `versickert` < 25 m als WARNUNG.
- Ein sichtbarer Houdini-Lauf als Ziel muss ausdrücklich angegeben werden: `muendung_houdini`.
- Muster auf 2 m: 15 eigener See, 5 Bestandsbach, 1 Fluss, 2 Houdini, 19 versickert.

### A10 – Feldzuordnung

- Alle Nutzer von `feld_von_m`/`feld_von_cm` (Ebene, Prüfer, Kandidaten, Vorschau, `gefaelle_plan.py`) bekommen die
  neue Grenze über die Bibliothek. `gefaelle_plan.py` selbst ist nicht geändert.
- Selbsttest: Grenze in x und y, 300 Zufallspunkte gegen `feld_grenzen_m`.

### A11 – Lagenränder

- Ränder ≥ 3 m weich, auch innen bei `ring`, `um_gruppe` und `ufer`.
- Pfad-Bodenband: 1 m Übergang beidseits (0,5 m innen + 1 m außen). 10 m vor dem Lagenfenster wird es ausgeblendet,
  statt hart abgeschnitten.
- Alle Lagen laufen am Fensterrand auf 3 m aus.

### A12 – Querprofil

- `Stempel.bach_profil` stempelt jeden Bach:
  - Die Wasserkante liegt 0,3–0,5 m innen, mindestens 0,75 Zellen von der Mitte.
  - Bett = Spiegel − Tiefe, Böschung 35°.
  - Uferring auf Spiegel + 0,15 … 0,5 m bis Netzrand + 1,5 m. Er hebt höchstens 1 m an.
  - Neben dem Fuß einer Stufe gilt 1,5 m lang der Oberwasser-Spiegel.
  - Der Spiegel liegt 0,3 m eingetieft. Liegt eine Uferseite tiefer, sinkt er bis 2 m.
  - Fremde Seen samt Uferring werden nicht angeschnitten.
  - Gruben aus Projektionssprüngen werden zurückgesetzt.
- Der Spiegel im Plan = gestempeltes Bett + Tiefe. Der Planer warnt, wo Schutz oder Rand das Bett geschwächt haben.
- Neue Prüferregel am Netzrand `max(B/2 + 0,4, Wasserkante + 0,3)`:
  - „Ufer unter dem Spiegel“ und „Gelände über dem Spiegel im Wasser“ sind auf 1 m FEHLER, auf 2 m WARNUNG.
  - Begründung für 2 m: Ein 1–2 m breiter Bach ist im 2-m-Raster nicht auflösbar.
  - Ausgenommen sind Furten, Stufenzonen ±(0,5 + 0,75 Zellen), Seen, offene Mündungen und die Innenseite enger Bögen.
- Selbsttest auf 1 m: 0 FEHLER. Absichtlich kaputte Fälle ergeben FEHLER.

### A13 – Gewässer gegen Bestand

- **Bachende:** nie unter dem Ziel (siehe A4/A9). aue_07 mündet jetzt bei 25,14 m in `B_R_P2_M1_01`, elfenwald_04
  bei 25,42 m über `B_R_P4_M1_01` (25,40 m).
- **Seeufer** unter dem Spiegel ist jetzt FEHLER (Toleranz 5 cm).
- **Seen < 10 m²** werden Lage (Standard Schlamm) oder optional ein Decal, ohne Becken:
  - oedland_06: alle Salsen sind jetzt Lage Schlamm.
  - kueste_05: Tümpel jetzt mit r ≥ 1,8 m. Es passen 4 auf die Bank, alle ≥ 10 m².
- **Furt:** dschungel_02 `quellbach` hat jetzt ein Fenster von 210 × 130 m und eine Furt am Weg mit 4 Trittsteinen
  (`furt`). Im Eintrag stehen `furten` mit von/bis.
- **Schutzzone:**
  - 3 m um Wege **und Orte** sind hart 0, gemessen bis zum Zellrand. Der Übergang beginnt erst außerhalb.
  - `ist_wasser` hebt nur noch den Wasserschutz auf.
  - Prüfer: Änderung ≤ 3 m an Weg oder Ort ist FEHLER.
  - Offene Mündungen in Bestandswasser sind im Korridor (letzte 8 m) vom Wasserschutz ausgenommen
    (`muendung_offen_ab_cm`).

### B – Biome

- **bergwald_06:** siehe Pilot-Abschnitt.
- **aue_01:** `ersetzt_bestandsbach` für `B_R2_R_M1_M1_04` im Teich, von `einlauf` bis `ueberlauf` (43,1 m).
  Houdini `R_M1_M1__WASSER` ist im Teich + 2 m ausgeblendet (807 m²).
- **frost_02:** Houdini `K13_FROSTSEE__WASSER` ist im Seeumriss + 3 m ausgeblendet (bevorzugte Variante). Der
  Spiegel bleibt.
- **sumpf_05:** neue Gruppe `erlenring_ost` mit 45 Erlen-Ersatz im Ostsektor (30–46 m). Außerdem liegt die Schlenke
  jetzt am tiefsten Punkt der Rinne: Vorher floss das Rinnsal bergauf und endete 2,97 m unter der Schlenke.
- **Decals mit eigener Textur:** heide `MI_EL_SW_Russ_Decal` ist `optional: true`. Alle übrigen Decals mit eigener
  Textur waren schon optional (geprüft).
- **Niagara-Kopien:** Die User-Parameter-Namen sind nirgends belegt („Namen nicht veröffentlicht“,
  `antworten/14-wasser-fx.md`). `kopie_aenderungen` bleiben deshalb beschreibend.
- **Weitere Rezeptkorrekturen** (durch das neue Bachverhalten nötig):
  - dschungel_06: Der Strudeltopf liegt am Grund des Trichters. Die Schwinde mündet dort. Vorher lag er 6,5 m über
    dem Bachende an der Portalwand.
  - bergwald_05: Fenster 130 m, der Klammbach geht ins Houdini-Gerinne über (Name unbekannt, `muendung_houdini: true`).
  - fjord_02: Fenster 270 × 200 m.
  - gletscher_06: Topfkette mit `abfluss_von` + `bis_see`.

## Prüfergebnis

| Lauf | Ergebnis |
|---|---|
| 2 m, alle 15 Planer | Prüfer 0 FEHLER; zwei Läufe byteidentisch (`diff -r`) |
| 2 m Prüfer-WARNUNG | canyon_07 `abfluss` versickert 16 m; gletscher_01 Ufer 1/76 m; gletscher_06 Ufer 4/24 m; lava_03 versickert 23 m; wueste_04 versickert 23 m |
| 2 m Planer-WARNUNG | fjord_02 `abfluss4`, gletscher_03 `firnrinnsal`, gletscher_06 `klammbach_unten`, heide_06 `fall3` 0,8 m, lava_03: Bett an 1–3 Punkten über dem Spiegel bzw. kleine Fallhöhe |
| synthetische 1-m-Welt, alle 15 | 1 FEHLER (gletscher_06 `klammbach_oben`, Ufer an 1/26 m 0,31 m unter dem Spiegel); WARNUNG: versickert < 25 m (canyon_07, lava_03, wueste_04), fjord_02 `abfluss4`, je 1 alte (dschungel H6 schwebt, fjord_06 Kamera) |
| Selbsttest `lib/selbsttest.py` | 0 FEHLER (Schritte 1–11) |
| Testbilder | alle 120 `antworten/sehens/<biom>/test_*.png` erneuert. Die Vorschau zeigt jetzt Bachstufen (weiß, Fallhöhe ab 2 m), Furten und ausgeblendetes Houdini-Wasser (magenta). |

**Synthetische 1-m-Welt:**
- Die 2-m-Daten werden bilinear bzw. blockweise auf 9577 × 7057 hochgerechnet. Damit läuft die 1-m-Logik auch in der
  Cloud: native 1-m-Stempel, 1-m-Prüfer-Toleranzen.
- Die Skripte liegen nur im Scratchpad, nicht im Repo.
- Die echten 1-m-Daten sind rauer. Der lokale Lauf bleibt der Maßstab.

## Rückfragen

1. **Mündung in Houdini-Wasser** (bergwald_06 Abfluss, bergwald_05 Klammbach):
   - Ich gebe sie ausdrücklich als `muendung` = Netzname (bzw. `houdini`) mit `muendung_art: houdini` an. Ist das so
     für euch lesbar?
   - Für bergwald_05 kenne ich den Netznamen nicht. Bitte lokal zuordnen.
2. **Offene Mündung:**
   - Im Mündungskorridor (letzte 8 m, halbe Breite + 1 m) ändere ich Gelände am Bestandswasser.
   - Darf das bleiben, oder soll der Bach 3 m vor dem Bestand enden und eure Brücke den Rest schließen?
3. **2-m-Prüfung A12:**
   - Auf 2 m ist die Querprofil-Regel WARNUNG, auf 1 m FEHLER.
   - Prüft euer Einbau-Prüfer die Ufer am Netzrand (halbe Breite + 0,4 m)? Bei Bächen schmaler als zwei Zellen prüfe
     ich bei Wasserkante + 0,3 m.
4. **Stufendichte:**
   - Auf Hängen > 60 % entsteht alle 3,5 m eine Stufe. Das sind die 3-m-Becken aus A8. Einzelne Fälle gehen bis 12 m,
     etwa bergwald_06 über die Karschwelle.
   - Soll ich dort Ketten nach `faelle.kette_glied` (~8 m) bündeln?
5. **heide_06 `auslauf`:**
   - Er endet jetzt `versickert` (48 m) statt in `B_R2_R_P3_P0_01`. Der Bestandsbach lag dort höher als der Anfang
     des Auslaufs (vorher 3,95 m darunter).
   - Soll der Auslauf an den Bach unterhalb des ausgeblendeten Abschnitts angeschlossen werden (`punkte`)?
6. **kueste_05:** Nur 4 Tümpel ≥ 10 m² passen auf die Felsbank (vorher 11 kleine). Reicht das, oder lieber die Bank
   vergrößern?
