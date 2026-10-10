# Verteilung Biomgruppe 2: Aue/Flussauen (Velen, Weißgarten, Kovir)

**Auftrag 11, Teil B2.** Biom `aue`, Foliage-Präfix `FT_EL_AU_`, Ordner `/Game/Eldarien/Welt/Foliage/Aue`. Stand 2026-10-10.
Lieferung: dieser Bericht, `skripte/aue_regeln.json` (ursprünglich 25 Klassen und 193 Netze in 211 Paletteneinträgen; nach Korrektur Runde 1 16 Klassen und 137 Netze, die generischen Klassen stehen in `mittelschicht_overrides`; alle gegen `netze.csv` geprüft),
`skripte/aue_plan.py` (Planer, FORMAT §3/§5). **Alles UNGETESTET MIT ECHTDATEN** – in der Cloud nur mit synthetischen
Rastern (E5, siehe §4) rauchgetestet; der Rauchtest wurde nach dem Sitzungsabbruch am 10.10. wiederholt und nachgeprüft
(byte-identische Ausgabe, Schema, Sperrflächen). Web-Quellen konnten nur als Suchmaschinen-Auszüge gelesen werden (80.lv,
GDC Vault, Fab per Proxy nicht direkt erreichbar); solche Belege sind mit **[Suchauszug]** markiert, Zahlen ohne Beleg mit
**Richtwert**. Quellenliste am Ende von §1.

Betroffene Felder (aue dominant): F1, I1, F2, G2, F3, J3, C4, C5, D5, E5, J5, A6, F6, J6, A7, B7, D7, F7, J7; Aue-Anteile in
F4, F5, H5, E7 (und kleiner in C3, B6, D6, C7, G7–I7, E4, D4, H4, A5). Der Planer läuft in jedem Feld nur auf Zellen mit Biom
`aue` (`eigner.r8` + `welt.json`, Kennzahl 0 = aue laut FORMAT §2), in den Wüstenfeldern C4, D5, E5 (und C3/D3/D4/E3/E4) zusätzlich
nur außerhalb Sand/Sandstein ≥ 0,5 und mit Faktor 0,6.

## Korrektur Runde 1 (10.10.2026): gilt vor allen folgenden Abschnitten

Grundlage: `auftraege/verteilung-korrektur-runde1.md` (Echtdaten-Test 10.10. 15:30) und `antworten/verteilung-KONVENTIONEN.md` (verbindlich).
Geändert wurden nur `skripte/aue_plan.py` (jetzt 1 262 Zeilen), `skripte/aue_regeln.json` und dieser Bericht. Wo §2 bis §4 etwas anderes
sagen, gilt dieser Abschnitt.

**Echtdaten-Befund (Referenz, lokal, alte Fassung):** A5 (bergwald/fjord; laut `biome_je_feld` kueste 75 / bergwald 14 / aue 11 %)
**1 743** Instanzen, G4 (elfenwald 76 / heide 22 / aue 3 %) **1 433**, E1 (gletscher 100 %) 0, C6 (lava 99 %) 0. Die alte Fassung bebaute
schon nur aue-Zellen, ohne Biomfaktoren für fremde Biome. In A5 und G4 lagen die Instanzen also auf Zellen mit Kennzahl 0 (Weltgelände → aue).
Zu viel waren sie aus zwei Gründen: (1) Etwa ein Drittel der Aue-Ebene waren generische Mittelschicht-Klassen (Grasbüschel, Sträucher,
Hochstauden, Farn, Jungbäume, Totholz, Pilze), die Teil D noch einmal setzt. (2) Es gab keine Mindestgrenze: Jeder aue-Fleck wurde voll
bebaut, und Meer- oder Seezellen mit Kennzahl 0 zählten im Anteil als aue.

### Was sich geändert hat

1. **Zuständigkeit (§1):** Das Biom je Zelle kommt aus `eigner.r8` + `welt.json["kacheln"][k]["rezept"]`. **Kennzahl 0 ist `aue`**, ein Rezept
   mit „vulkan“ oder „lava“ ist `lava`. Eine Kennzahl ohne Biom-Zuordnung bekommt das dominante Feldbiom und erzeugt eine `WARNUNG`; sie wird
   also nicht automatisch aue. Nur wenn `eigner.r8` oder `welt.json` fehlt, gilt für alle Zellen das dominante Feldbiom aus
   `daten/biome_je_feld.json` (zweiter Fallback: `feld_biom_fallback`, dazu eine Logzeile). `biome_eigen = ["aue"]`, Block
   `zustaendigkeit` in der Regeldatei.
   - **Saum:** Bebaut werden aue-Zellen plus ein **Saum von 30 m**, in dem der Faktor von 1 an der Biomgrenze linear auf 0 fällt
     (Jump-Flooding-Distanzfeld). Er gilt für alle Schichten einschließlich der Bäume und wirkt als Multiplikator auf λ.
   - **Leerplan:** Liegt der aue-Anteil im Fenster unter **2 %**, schreibt der Planer einen **leeren `plan.json`** (`instanzen: 0`,
     `dateien: {}`, `leer: true`, ohne f32; alte f32 werden gelöscht) und meldet das in einer Zeile.
   - **Landbezug (Präzisierung):** Anteil und Saum beziehen sich auf **Landzellen** (ohne `karte_wasser`). Kennzahl 0 deckt auch Meer
     und Seen ab. Sonst würde Wasser den aue-Anteil in Küstenfeldern wie A5 aufblähen, und der Saum würde von Meereszellen 30 m in die Küste
     reichen. `plan.json["biome_fenster_bezug"]` nennt das.
   - Die bisherigen Biom-Sonderwege (Fallback-Biom für unbekannte Rezepte = Feldbiom aus der Regeldatei) sind durch diese Regel ersetzt.
     Biomfaktoren für fremde Biome gibt es nicht.
2. **Wüstenfelder C3 C4 D3 D4 D5 E3 E4 E5:** Hier wird nur ergänzt, mit Faktor 0,6. Zellen mit Sand/Sandstein ≥ 0,5 sind gesperrt, auch für
   den Saum. `entfernen` bleibt dort **immer leer**, auch wenn in der Regeldatei etwas stünde. Außerhalb der Wüste wird `entfernen` (Standard
   leer) nur gesetzt, wenn aue im Feld ≥ 50 % hat.
3. **Pflichtschlüssel (§2)** stehen in jedem `plan.json`, auch im leeren: `biome_fenster` (Anteile aller Biome, Σ = 1), `zellen_zustaendig`
   (Landzellen im Feld mit Faktor > 0, also einschließlich Saum), `biome_eigen`, `kollision_anzahl` (Σ der Dateien mit `kollision: true`).
   Zusätzlich gibt es `eigenanteil_fenster/_feld`, `saum_m`, `biom_quelle`, `budget` (Deckel, Ziel, Zahl vor der Ausdünnung, Faktoren je
   Klasse), `an_landschaftsgras` und `statistik.saum_zellen_feld`.
4. **Budget (§3, hart), Block `budget`:** `deckel_je_feld` 60 000, `ziel_je_feld` 45 000–52 000, `ausduennen_auf` 52 000,
   `kollision_je_feld` 3 000. Die Ausdünnung ist deterministisch per Hash je Instanz und hat drei Stufen:
   - **Kollision:** Liegt sie über 3 000, wird in der Reihenfolge Kiefer → Hain → Pappel → Weide → Totbaum → Solitär ausgedünnt (je Klasse
     höchstens 60 %), danach gleichmäßig.
   - **Schichtziele (weich):** Boden 26 000, Mittel 12 000, Baum 2 600, Wasserkante 12 000, jeweils innerhalb der Schicht nach Priorität.
   - **Feld:** Über 52 000 wird zuerst Kiesel, dann Zweige, Laub usw. ausgedünnt, danach alle Nicht-Baum-Klassen gleichmäßig. Eine harte
     Sicherung hält 60 000.

   Jede Stufe schreibt eine `WARNUNG` ins Log und einen Hinweis ins `plan.json`. Kleinzeug geht an das Landschafts-Gras: `an_landschaftsgras`
   nennt Laub, Zweige und Bodendecker → `GT_Kraut` sowie Kiesel → `GT_Steinchen`, jeweils mit dem behaltenen Anteil.
5. **Ebenen-Abgrenzung (§4):** Die generischen Klassen sind aus dem Planer entfernt und stehen jetzt als `mittelschicht_overrides` im Regel-JSON
   (Schema unten). Das betrifft Grasbüschel, Hochstauden, Sträucher, Jungbäume, Farn, Totholz klein/groß, Stümpfe und Pilze (Schicht 0).
   Steht eine Klasse dieses Namens oder Alias (`ebenen.generisch_mittelschicht`, `ebenen.alias`) trotzdem in `schichten`, überspringt der
   Planer sie mit Hinweis. Felsen > 0,8 m setzt der Planer weiterhin nicht (nur `felsgruppen_overrides`), Spuren ebenso nicht (nur
   `spuren_overrides`).
6. **ASCII und Exit-Codes (§5):** Alle Ausgaben laufen über `meld()`/`fehler()` und werden in ASCII umgewandelt: ä→ae, ß→ss, →→->, ≤→<=, –→-.
   Auch `plan.json["hinweise"]` ist ASCII. Ein unbekanntes Feld, eine fehlende Regeldatei, ein fehlendes `daten/netze.csv` (gesucht unter
   `basis/daten/`, neben dem Skript und unter `vorlagen/daten/`, oder per `--inventar PFAD`), ein fehlendes `hoehe.f32` oder ein fehlender
   Weltordner führen jeweils zu einer Meldung auf stderr und **Exit-Code 2**. Eine Regeldatei ohne `zustaendigkeit`/`budget` (alte Fassung)
   ebenfalls.

### Neue Schicht-1-Definition (nur Aue-Sonderformen)

| Schicht | Klassen (16 statt 25; 137 Netze statt 193) |
|---|---|
| 0 boden | laub, zweige, kiesel, bodendecker (`pilz` → Teil D) |
| **1 mittel** | **`blumeninsel`**: Auenwiesen-Blumeninseln (10–26 Stück, Hauptart 60 %, 14 Meadow-Blumen). **`hecke_weg`**: Wegsaum-Hecken 4–7 m neben Wegen auf 40 % der 48-m-Abschnitte, außerhalb von 150 m um Orte, Yaw entlang des Weges |
| 2 baum | auwald_weide, auwald_pappel, hain_terrasse, kiefer_hain, solitaer, totbaum (stehendes Totholz bleibt hier, Teil D setzt in der Aue keinen Totbaum) |
| 5 wasserkante | schilf, seggen, **uferstaude** (= Uferstauden-Saum 2–16 m vom Wasser, Pestwurz/Goldrute/Topinambur/Nessel), uferwurzel |

Was nicht mehr in Schicht 1 steht:

- **Feldrand-Hecken und Kopfweiden-Reihen** stehen nur in `spuren_overrides` (`feldstreifen.hecke_am_feldrand`, `kopfweiden_reihe`) und
  werden deshalb hier nicht gesetzt.
- **Holzschlag-Stümpfe** um Orte (bisher `stumpf.ort_nah_faktor` ×3 in 200 m) entfallen; sie kommen aus `spuren_plan.py` (`holzschlag`).

### Override-Schema

```
"mittelschicht_overrides": {            # für mittelschicht_plan.py (Teil D), gewinnt gegen mittelschicht_regeln.json["biome"]["aue"]
  "biom": "aue",
  "palette":  {"grasbueschel": [11 Pfade], "hochstaude": [8], "strauch": [15], "jungbaum": [9], "farn": [8],
               "totholz_liegend": [9: dead_log_01-04, trunk_01/02, LargeFallenTree_02, FallenTreeAssembly_01, MossyTree_01],
               "totholz_stumpf": [7: stump_03, TreeStump_01, BirchTreeStump_01, RottenTreeStump_01, Tree_Stump_01/02/03],
               "totholz_ast": [OldTreeBranch_03], "pilz": [2]},            # bisherige Aue-Paletten, 70 Pfade, alle im Inventar
  "faktor":   {jede der 9 Klassen: 1.0},                                   # Stellschraube x Teil-D-Dichte (0 = aus)
  "parameter": {klasse: {"dichte": [offen, beschattet], "gruppe", "radius_m", "massstab", "eingraben_cm", "kippen", "sichtweite",
                         "hang_max", "saum", "feuchte", "lichtungsrand", "lagen_faktor"}},   # bisherige Aue-Werte im mittelschicht-Format
  "zusatzklassen": {},                                                     # Teil D hat alle Aue-Klassen
  "herkunft": {...}, "nicht_uebertragbar_hinweis": "..."
}
```

- **Dichte:** `parameter.<klasse>.dichte` ist die bisherige Aue-Dichte als Mittel der Höhenstufen (Ufer 6,5 / Aue 36,2 / Terrasse 57,3 %,
  E5-Synthetik) mal `licht` [offen, beschattet]. Beispiele: Grasbüschel [0,0118; 0,0030], Strauch [0,0029; 0,0009], Farn [0,00008; 0,0062],
  Totholz liegend [0,00047; 0,00175].
- **Faktor:** Weil die Dichte schon in `parameter` steht, sind alle `faktor` = 1,0. Das Verhältnis zur Teil-D-Grunddichte wäre Grasbüschel
  0,74, Hochstaude 0,32, Strauch 0,60, Jungbaum 0,45.
- **Prüfung:** `mittelschicht_plan.effektive_regeln()` liest den Block (`palette, faktor, zusatzklassen, parameter`); alle 9 Klassen haben
  Quelle `aue`.
- **Nicht übertragbar:** Teil D kennt keine Höhenstufen. Die Ufer-Betonung (Hochstaude, Farn, Strauch) trägt `parameter.feuchte`.

```
"felsgruppen_overrides": {"biom": "aue", "palette": "moos", "faktor": {"gesamt": 0.35, "klassen": {"kuppe": 0.625, "blockstrom": 0.4}},
                          "klassen_aus": ["band", "wand", "grat", "fuss"],
                          "rollen": {"kiesel": {"sichtweite_cm": [0, 5000]}, "stein": {"eingraben": [0.4, 0.55]}},
                          "wunsch_hinweis": "...", "wuesten_felder_hinweis": "..."}
```

- **Auf das gelesene Schema gebracht:** Die Werte sind dieselben wie bisher (`biom_faktor` 0,35, Klassen `kuppe` p 0,5 → 0,625,
  `blockstrom` p 0,2 → 0,4).
- **Als Text abgelegt:** Was Teil C nicht auswertet (Höhenstufe Terrasse, Prallhang-Zahlen, Lagen), steht jetzt in `wunsch_hinweis`
  und erscheint nicht mehr als „ignoriert“.
- **Prüfung mit `OverrideLeser`:** gelesen werden `biom, faktor.gesamt, faktor.klassen, klassen_aus, rollen.kiesel.sichtweite_cm,
  rollen.stein.eingraben`.
- **Hinweis an Teil C:** Die aktuelle Arbeitskopie von `felsgruppen_plan.py` meldet `palette` (Name) als ignoriert, weil der Zweig
  `palette`/`biom_palette` in `lies()` fehlt. Laut eigener Doku wird er gelesen. Die Wirkung ist null, weil `moos` ohnehin die
  Standardpalette für aue ist.

`spuren_overrides`: Neu ist ein Kopf mit `biom`, `palette` und `faktor`:

- `palette`: Hecke am Feldrand (4 Netze), Obstgarten (4), Kopfweiden-Reihe (2).
- `faktor`: feldstreifen, obstgarten, zaun_weg, kopfweiden_reihe, muehle und steg, jeweils 1,0.

Die Elementparameter sind unverändert. `spuren_plan.py` liest in der Arbeitskopie noch keine `spuren_overrides`; der Block ist als
Vorgabe abgelegt.

### Rauchtest Runde 1 (Cloud, synthetisch; Raster danach gelöscht)

Die Raster wurden neu erzeugt, in voller Größe 7 057 × 9 577 (memmap, nur die Fenster beschrieben):

- **E5:** wie Runde 0, alles Kennzahl 0.
- **H5 (Mischfeld):** aue im Westen mit welliger Grenze, sumpf, eine dschungel-Ecke und ein 40 × 40-m-Block mit Kennzahl 99 ohne
  `welt.json`-Eintrag. Dazu Fluss, zwei Teiche und ein Weg; keine Bestand-Ebene.
- **C6 (Fremdbiom):** Vulkanregion 96,6 %, bergwald 2,5 % und ein aue-Fleck mit 0,9 %.
- **A5 (Küste):** Meer mit Kennzahl 0 (Wasser), kueste-Land und ein aue-Fleck mit 13 % des Landes am Ostrand.

Umgebung: Python 3.13.16, NumPy 2.5.3, ohne numba, 4 Kerne, Aufruf `python -I -X utf8`.

| Lauf | Instanzen | Boden / Mittel / Baum / Wasserkante | Kollision | `biome_fenster` (Land) | `zellen_zustaendig` | Wanduhr |
|---|---|---|---|---|---|---|
| E5, **alte Fassung** (Runde 0) | 32 627 | 11 980 / 16 254 / 702 / 3 691 | 790 | – | – | 9,3 s |
| **E5** (eigene Zellen, Wüstenfeld ×0,6) | **21 085** | 11 704 / 4 996 / 621 / 3 764 | 621 | aue 1,0 | 971 132 | 9,4 s |
| **H5 Mischfeld** | **12 836** | 5 953 / 3 174 / 351 / 3 358 | 351 | sumpf 0,644, aue 0,322, dschungel 0,034 | 325 932 | 6,5 s |
| **C6 Fremdbiom** | **0 (Leerplan)** | – | 0 | lava 0,966, bergwald 0,025, aue 0,009 | 0 | 0,3 s |
| **A5 Küste** | **859** | 614 / 203 / 42 / 0 | 42 | kueste 0,866, aue 0,134 | 47 556 | 5,3 s |
| E5 `--faktor 3` (Überlauf) | 51 257 | 25 967 / 11 932 / 1 947 / 11 411 | 1 947 | – | – | 9,1 s |
| E5 `--faktor 6` (Kollisionsüberlauf) | 51 997 | 25 507 / 11 948 / 2 600 / 11 942 | **2 600** | – | – | 8,9 s |
| ohne `eigner.r8`: E5 / H5 / C6 | 21 085 / Leerplan / Leerplan | Fallback biome_je_feld → aue / sumpf / lava | | | | |

Einzelheiten zu den Läufen:

- **E5 je Klasse:** Blumeninsel 4 918, Bodendecker 3 626, Laub 3 448, Zweige 2 944, Seggen 1 966, Kiesel 1 686, Schilf 1 292, Uferstaude 505,
  Hain 236, Pappel 186, Kiefer 106, Hecke 78, Weide 55, Totbaum 21, Solitär 17. Die 11 542 Instanzen der früheren generischen Klassen
  (Grasbüschel 7 791, Strauch 1 251 usw.) setzt jetzt Teil D.
- **Überlauf `--faktor 3`:** Die WARNUNG nennt Schicht Boden 36 313 → 25 967 und Mittel 14 967 → 11 932, mit den Faktoren Kiesel ×0,39,
  Zweige ×0,40, Laub ×0,83 und Blumeninsel ×0,79.
- **Kollisionsüberlauf `--faktor 6`:** Die WARNUNG nennt Kollision 4 095 → 2 976 (Kiefer ×0,17, Hain ×0,41), Schicht Baum 2 976 → 2 600
  und Feld 52 383 → 51 997.
- **Saum-Abfall** (Instanzen je m² Land im Feld nach Abstand zur nächsten aue-Landzelle; Höchstabstand H5 26,0 m, A5 28,9 m):

  | | innen | 1–6 m | 6–12 m | 12–18 m | 18–24 m | 24–30 m | > 30 m |
  |---|---|---|---|---|---|---|---|
  | H5 | 0,0417 | 0,0268 | 0,0270 | 0,0216 | 0,0110 | 0,0019 | **0** (668 049 Zellen) |
  | A5 | 0,0229 | 0,0183 | 0,0079 | 0,0085 | 0,0050 | 0,0028 | **0** (201 519 Zellen) |

  In A5 bekommt die Küstenlinie (Meer = Kennzahl 0) keinen Saum, denn Instanzen stehen nur am aue-Fleck.
- **Kennzahl 99 (H5):** 1 521 Zellen. Die `WARNUNG` meldet sie, sie werden dem dominanten Feldbiom sumpf zugeordnet und nicht bebaut.

Weitere Prüfungen, alle bestanden:

- **Schlüssel und Budget:** Alle Pflichtschlüssel sind vorhanden, auch im Leerplan. Jede f32 ist durch 10 teilbar, die Summe stimmt mit
  `instanzen` überein, und `kollision_anzahl` = Σ Kollisionsdateien. In keinem Lauf mehr als 60 000 Instanzen oder 3 000 Kollisionen, keine
  generische Mittelschicht-Klasse in der Ausgabe.
- **Geometrie:** |q| − 1 ≤ 1,2·10⁻⁷. 0 Instanzen auf Wasser, Weg oder Ort, 0 außerhalb des Feldes, 0 jenseits des Saums;
  z − Gelände −0,12 bis −0,01 m.
- **Determinismus:** Zwei Läufe sind byte-identisch. MD5 aller f32: E5 `244f6b02…`, H5 `2f3f3573…`, A5 `383995fc…`. `plan.json` ohne
  `stand`/`laufzeit_s`: E5 `fb333e39…`, H5 `1757f578…`, A5 `f2d9dae1…`, C6 `aa679f6d…`.
- **ASCII:** Alle 17 Logs (Läufe, Überläufe, Fallbacks, Fehlertexte) und alle `hinweise` haben 0 Nicht-ASCII-Bytes.
- **Exit-Code 2:** bei Feld `K9`, fehlender Regeldatei, fehlender `netze.csv`, fehlender `hoehe.f32` und fehlendem Weltordner, jeweils mit
  einzeiliger Meldung.
- **Inventar:** 1 435 Netze, 0 fehlen (141 Paletteneinträge und 90 Override-Pfade). `py_compile` ok.

### Erwartete Zahlen mit Echtdaten (Referenz; ersetzt die Tabelle in §4)

Faktor neu/alt aus der E5-Synthetik: 21 085 / 32 627 ≈ **0,65**. Der Saum kommt nur in Mischfeldern hinzu, als Band von 30 m mit
mittlerem Faktor ≈ 0,5.

| Feld | Echtdaten alt | Erwartung neu | Anmerkung |
|---|---|---|---|
| **A5** (kueste/bergwald, aue 11 % des Landes) | 1 743 | **≈ 1 000–1 400** | aue ≥ 2 % der Landzellen → Plan; nur aue-Land + Saum, kein Saum entlang des Meeres |
| **G4** (elfenwald, aue 3 %) | 1 433 | **≈ 900–1 200** oder Leerplan | Plan, wenn aue ≥ 2 % der Landzellen im Fenster; Rest wie A5 |
| **E1** (gletscher 100 %) | 0 | **0, Leerplan** mit Pflichtschlüsseln | vorher Nullplan ohne Pflichtschlüssel `biome_fenster` usw. |
| **C6** (lava 99 %) | 0 | **0, Leerplan** | wie Synthetik C6 |
| C5 / E5, D5, C4 (Wüste ×0,6) | – | 20 000–28 000 / 13 000–22 000 | Spalte „mittel“ in §4 gilt nur noch für Blumeninseln/Hecken (≈ 30 % der alten Werte) |
| Kollision je Feld | – | 400–1 500 | nur Bäume, die liegenden Stämme liegen jetzt in Teil D |

Damit bleibt jedes Aue-Feld deutlich unter dem Ziel 45 000–52 000. Nur bei `--faktor` ≥ 2,5 greifen die Schichtziele, das Feldziel 52 000
und der Kollisionsdeckel mit WARNUNG.

## 1. Witcher-Analyse: Was Velen, Weißgarten und die Kovir-Auen zwischen Boden und Krone füllt

**Schichten.** Die Zielbilder (witcher_01: Flussaue mit Ruine; witcher_03: Waldpfad mit Bach; witcher_05: Dorfplatz) und die
Beschreibungen in `ANALYSE_WITCHER_2026-10-08.md` zeigen in der Aue durchgehend vier Höhenbänder, die sich gegenseitig verdecken:
(a) Boden 0–0,3 m: Laub, Zweige, Kiesel, Pilze, Klee, Moos auf Steinen; (b) 0,3–1,5 m: hohes Gras knie- bis hüfthoch in 3–5 Arten,
Blumen in Inseln (witcher_01: rote/orange Ähren in Gruppen von 10–30), Hochstauden an Wasser und Waldrand; (c) 1,5–4 m: Weidengebüsch
und Haselhecken, Jungbäume am Saum, liegende Stämme; (d) Krone: Weiden und Pappeln am Wasser, Eichen/Buchen/Hainbuchen auf der
Terrasse, dazwischen Lichtungen. Die Bildkritik (`bildkritik-witcher-messlatte.md`, W6FIN_E5) nennt als konkreten Mangel in
Eldarien: Bäume im 15-m-Raster ohne Clumps, Wiese „ein Beige ohne hohe Gräser, Büsche oder Felsanker“, und empfiehlt Weiden nur
20–40 m vom Wasser, Clumping-Noise 40–100 m, Büsche in 3–7er-Gruppen – diese Zahlen sind ins Regelwerk übernommen.

**Dichten und Gruppen (Richtwerte, aus den Bildern abgeschätzt).** witcher_01 zeigt in 10 m Bildtiefe ~6 Grasarten/Höhen,
1 Blumeninsel je 15–25 m², 1 Busch je 20–40 m², einen Stein je 3–5 m² am Ufer; witcher_03 im Auwald 1 liegenden Stamm je ~100 m²,
Zweige/Äste 0,05–0,1 je m². CDPR beschreibt das Verfahren hinter diesen Dichten: Die GDC-2014-Session „Landscape Creation and
Rendering in REDengine 3“ (Marcin Gollent) nennt laut Vault-Beschreibung Vegetation, die „procedurally generated, offline and in
real time“ gesetzt wird, ohne Handplatzierung **[Suchauszug: GDC Vault 1020197, Folien-PDF media.gdcvault.com, Mitschnitt
archive.org/GDC2014Gollent]**. Dass der Offline-Generator Wasseransammlung und Sonnenlicht simuliert (Hangneigung zu Nachbarzellen
verteilt „Ressourcen“, Sonnenbahn → Schattenanteil je Zelle, Vergleich mit dem Lichtbedarf jeder Art, handgemalte Flächen
ausgenommen), steht nur im Sekundärbericht von DualShockers **[Suchauszug, nicht in den Folien geprüft]**. Die REDkit-Doku
beschreibt das Vegetation Edit Tool mit Pinseln je Geländetyp („fields, meadows, swamps and forests“) mit einstellbarem Spacing und
Scale-Variation; 80.lv ergänzt den Ablauf „von großen Bäumen zu kleinen, dann Farne und Gras“, Asset-Bibliotheken je Region
und Sichtweiten je Netz **[Suchauszug: W3REDkit „Vegetation Edit Tool“; 80.lv „World building of Witcher 3“]**. Genau das bildet
der Planer nach: Wasserabstand + relative Höhe (Feuchte) und Kronendach (Licht) steuern jede Klasse; die Reihenfolge Baum → Strauch
→ Farn/Gras entspricht Schicht 2 → 1 → 0.

**Höhenstufen Ufer → Aue → Terrasse.** In Velen liegen drei Stufen über dem Wasser: der Uferstreifen (0–8 m, Schilf, Seggen,
Kies, Weidengebüsch, freigespülte Wurzeln an Prallhängen), die Aue (bis ~4 m über Wasser, Wiese mit Blumeninseln, Pappel-/Weiden-
gruppen, Altarme und Teiche mit dichtem Schilf) und die Terrasse (höher, trockener: Hainbuchen-/Eichenhaine, Kiefern auf
Sandkuppen, Felder und Dörfer). Der Planer berechnet beides aus `hoehe.f32` und `karte_wasser.r8`: Distanz zum nächsten Wasser und
Höhe über dem nächsten Wasserpunkt (Jump-Flooding, §2).

**Farbakzente.** Blumeninseln (Mohn rot, Kornblume blau, Kamille weiß, Wegwarte hellblau, Flockenblume violett) in 10–26er-Gruppen
mit einer Hauptart je Insel (60 %), nicht gleichmäßig gestreut; Goldrute/Topinambur gelb am Ufer; Herbstlaub kommt in Eldarien nur
über Material (PerInstanceRandom-Tint) – die Palette hat keine Herbstbäume, siehe Einkaufsliste.

**Blickziele und Spuren von Leben.** Weißgarten ist „known for its fruit orchards“, der Fluss Ismena durchzieht das Dorf
**[Suchauszug: thewitcher3.wiki.fextralife.com/White_Orchard]**; Velen wird als „barren, dotted with skeletal trees and broken
structures“, mit „dense forests, sprawling swamps, and war-ravaged villages“ beschrieben **[Suchauszug: primoumo.medium.com; xgamerss.com]**.
Für Eldarien heißt das: je Weiler Feldstreifen bis an den Ortsrand, lückige Zäune, ein Obstgarten, Kopfweiden-Reihen an Gräben und
Wegen, eine Wassermühle am Bach mit Gefälle, Solitärbäume als Blickziel auf freier Wiese, Totbäume als Velen-Akzent. Die
Witcher-4-Demo (Kovir, State of Unreal 2025, PS5 bei 60 fps, Tech-Demo statt Gameplay) belegt die Technikseite: Nanite Foliage mit
voll dreidimensionalen Blättern statt Flachkarten, dynamisch skalierende Foliage-Elemente, Mass-Crowds, Fast Geometry Streaming
**[Suchauszug: press.cdprojektred.com Pressemitteilung; vgtimes/gamespace-Breakdowns]**; der Digital-Foundry-Befund, dass Gras und
Kleinzeug über Runtime-GPU-PCG kommen, ist in `boden-kleinzeug-gras.md` bereits ausgewertet. Für den Planer folgt daraus nur:
Kleinzeug kurz cullen (3 500–7 000 cm), Bäume ohne Cull.

**Was in E5/G5/I5 heute fehlt (Ist-Bilder).** W6FIN_E5: Weiden und Kiefern gleichmäßig verteilt, kein Uferband, keine Büsche,
keine Stämme; BACH3_G5: Bach ohne Uferraum, Wiese ohne Höhenstaffel, Büsche als gleichmäßige Punkte; TERR3_I5: Ufer als Kiesstreifen
ohne Schilf, keine Stufe Ufer/Aue. Die Aue-Ebene adressiert genau diese drei Lücken (Schichten 1, 2, 5).

**Quellen (5 WebSearch-Läufe, nur Suchauszüge):** GDC Vault 1020197 „Landscape Creation and Rendering in REDengine 3“ (Folien
media.gdcvault.com/GDC2014/Presentations/Gollent_Marcin_Landscape_Creation_and.pdf; Mitschnitt archive.org/details/GDC2014Gollent) ·
DualShockers-GDC-Bericht (Vegetationsgenerator) · W3REDkit-Wiki „TOOL: Vegetation Edit Tool“ · 80.lv „World Building of Witcher 3“ ·
CDPR Press Center news/1778 (Witcher-4-Tech-Demo 2025) · Fab „Megaplants: Dry Common Reed“ · Fextralife „White Orchard“. Keine
Quelle nennt Instanzen je m²; alle Dichten unten sind Richtwerte aus den Zielbildern.

## 2. Regelwerk (`aue_regeln.json`) – Erklärung je Schicht

Alle Dichten sind Instanzen je m² je Höhenstufe (`ufer` / `aue` / `terrasse`), multipliziert mit dem Lichtfaktor
`licht[offen, beschattet]`, Lagenfaktoren (`lage_*.r8`), Feuchte (Wassernähe 40 m + Lagen Schlamm/Algen/Moos/Kraut/Lehm), Hang
(voll bis 18°, Klassen-Maximum 12–60°), Höhe (Abnahme ab 80 m, 0 ab 260 m), Sand-Dämpfung (Sand-Lage 100 % → ×0,25, außer Kiefern,
Kiesel, Zweige) und Wüstenfaktor 0,6. Gruppen: die Dichte ist Einzelinstanz-Dichte, Gruppenzentren = Dichte/Gruppenmittel; Mitglieder
liegen in `radius_m` um das Zentrum und werden an Sperrzellen erneut geprüft. Zufall ist ein Hash aus globaler Rasterkoordinate, Seed
1105 und Klassenkanal – deterministisch und nahtlos über Feldgrenzen. Abstände: 2,5 m Kleinzeug / 4 m Bäume, Sträucher, Totholz zu
Wegen; 5 m zu Orten; 0,5 m (Schilf, Kleinzeug) bzw. 1,5 m (Bäume, Sträucher) zu Wasser; 1 m zu Bestandsstämmen, 3 m für neue Bäume;
0,8 m zu Ufer-Ebene-Instanzen; 60 m Radius um `docs/staedte/standorte.json` (optional).

**Höhenstufen.** `ufer`: Wasserabstand ≤ 8 m oder (Höhe über nächstem Wasser ≤ 1 m und Abstand ≤ 40 m); `aue`: Höhe über Wasser ≤ 4 m
und Abstand ≤ 120 m; sonst `terrasse`. Fenster ohne Wasser: `aue` dort, wo Wiese+Moos+Gras ≥ 0,45, sonst Terrasse. `stillwasser`
(Altarm/Teich): Zelle in einem See-/Teichumriss (`wasser_welt.json` `seen[].umriss`, `teiche/teiche.json`, Polygonrasterung im Planer)
oder Wasseranteil im 61-m-Fenster < 0,12 (schmales, stilles Gewässer); dort Schilf ×2, Seggen ×1,5, Kiesel ×0,3.

**Schicht `0 boden`** (Sichtweite 4 000–7 000 cm, kein Schatten, keine Kollision, Eingraben 1–3 cm, Kippen 0,5–1,0):
- `laub` (DeadLeaves_01/12/13/14, poplar_leaves_01/02, detail_leaves_01/03): 0,004–0,008/m² offen, ×9 unter Kronen, Laub-Lage ×2,
  Wiese ×0,5; Gruppen 2–5 in 1,5 m.
- `zweige` (WoodenSticksAndTwigs_01–10, DryBranches_01/03/04/05, branch_01_1/2): 0,004–0,006, ×6 unter Kronen, Laub ×1,8.
- `kiesel` (SmallStonesPack_01–14): nur Aue/Terrasse 0,004–0,006 auf Kies ×4, Geröll ×3, Erde ×1,5, Wiese ×0,3, am Ufer 0 – Kiesbänke
  kommen aus `FT_EL_UF_*`.
- `pilz` (mushroom_01/02): 0,0005–0,001, ×4 im Schatten, Feuchte 0,5–2,0, Gruppen 3–7.
- `bodendecker` (CloverVarieties_01–04, GroundCover_01/05–08, ground_foliage_02_0/1): 0,006–0,010, Wiese ×1,4, Moos ×1,5, Trockengras ×0,5.

**Schicht `1 mittel`** (0,3–3 m):
- `grasbueschel` (grass_meadow_01/02/03/04/06/08 = 0,6–1,7 m, grass_bush_02–04, dead_grass_01/02): 0,010–0,016, im Wald ×0,25;
  Gruppen 2–6, Maßstab 0,8–1,4 → Witcher-Höhenstaffel knie- bis hüfthoch, ergänzend zum GPU-Gras (0,2–1,2 m).
- `blumeninsel` (Mohn, Kornblume, Kamille, Wegwarte, Flockenblume, Seifenkraut, Johanniskraut, Margerite, Wundklee; 14 Netze):
  0,004–0,009 als 10–26er-Inseln, Radius 4,5 m, Hauptart je Insel 60 %, Wiese ×1,5, Laub ×0,1 → ~1 Insel je 1 600–3 000 m².
- `hochstaude` (Goldrute, Topinambur, Nessel, Crownbeard_07/08; 0,65–1,7 m): Ufer 0,010, Aue 0,005, Terrasse 0,002, Saum ×2, Feuchte 0,6–2,0.
- `strauch` (Elderberry_05–09 Nanite, grey_willow_02–04, hazel_01/02, maple_bush_02–04, sea_buckthorn_01/02 als Weißdorn-Ersatz):
  0,0026–0,0045, Gruppen 1–4 in 2,8 m, Saum ×2,5, Maßstab 0,85–1,5, Sichtweite 30 000.
- `hecke_weg` (hazel_02, Elderberry_08/09, sea_buckthorn_01/02, maple_bush_04): Band 4–7 m neben Wegen, auf 40 % der 48-m-Abschnitte,
  0,12/m² → ~1 Strauch je 2,8 m Wegstrecke, Yaw entlang des Weges ± 15°, nur > 150 m vom Ort (Feldrand-Hecken um Orte: `spuren_overrides`).
- `jungbaum` (Hornbeam_Sapling_01–04 Nanite, Poplar_plant_A/B/C, beech_plant_02/03): 0,0012–0,0016, Saum ×3, Lichtungsrand ×2.
- `farn` (Fern_01–06, SilverLadyFern_01/02): nur beschattet (offen ×0,05, Schatten ×4), Feuchte 0,5–1,8, Gruppen 3–10.
- `totholz_klein` (dead_log_01–04, Tree_Stump_02/03, OldTreeBranch_03): 0,0005–0,0008, Yaw hangabwärts bzw. flussparallel (< 12 m vom Wasser).
- `totholz_gross` (trunk_01/02, LargeFallenTree_02, FallenTreeAssembly_01, MossyTree_01, Tree_Stump_01): 0,0002–0,00035, **Kollision**,
  Eingraben 8 cm + 25 % der Netzhöhe (FORMAT §3: Stämme 20–35 %), Sichtweite 60 000.
- `stumpf` (stump_03, TreeStump_01, BirchTreeStump_01, RottenTreeStump_01): 0,0002–0,0004, ×3 innerhalb 200 m um Orte (Holzschlag).

**Schicht `2 baum`** (Kollision, Sichtweite 0, Eingraben 8–12 cm, Kippen ≤ 0,08, Hang ≤ 28–32°, 3 m Abstand zu Bestandsbäumen):
- `auwald_weide` (Big_Tree_willow_01/02, kein Nanite, 30–38 k Dreiecke mit LOD): nur 3–28 m vom Wasser, Ufer 0,0035, Aue 0,0006,
  Gruppen 2–5 in 9 m, Maßstab 0,55–0,9 (9–19 m hoch).
- `auwald_pappel` (Poplar_01_Standalone, Poplar_03/04/05, SM_Poplar_tree_02/03/04/05_Optimised): 6–45 m vom Wasser, Aue 0,0022,
  Gruppen 2–6 in 11 m, Moos ×1,3, Trockengras ×0,6.
- `hain_terrasse` (Hornbeam_Field_01–04 + Forest_01/02/03/05/07 Nanite, beech_tree_01/02/03/04/06): Terrasse 0,0016, Aue 0,0010,
  Haine 6–18 Bäume in 15 m, Mindestabstand 4 m, Lichtungsfenster: 25 % aller 120-m-Zellen ohne Hain-Zentren, im Bestandswald ×0.
- `kiefer_hain` (pine_beach_01_A/B, 02_A, 03_A): Terrasse 0,0006 auf Trockengras ×2 / Sand ×2, Wiese ×0,3, Gruppen 3–7 (Velen-Mix, E5-Ist).
- `solitaer` (Hornbeam_Field_01/02, Poplar_02_Standalone, beech_tree_06/09, Big_Tree_willow_02 nur < 30 m Wasser): Blickziel, 1 Baum je
  96-m-Raster mit p = 0,45, 40 m frei von Bestandsbäumen, Beschattung ≤ 0,08, Maßstab 1,1–1,4 → 20–45 je Vollfeld.
- `totbaum` (DeadTree_01/02 Nanite, EuropeanBeech_Dead_M_01): 0,00005–0,00012, Feuchte ×1,6 (Velen-Akzent, Ufer).

**Schicht `5 wasserkante`** (Abstimmung mit `FT_EL_UF_*`: Instanzen der Ufer-Ebene werden geladen, 0,8 m Sperrradius; Zellen mit > 3
Ufer-Steinen im 7×7-Fenster gelten als Kiesbank → Schilf ×0,3):
- `schilf` (Rohrkolben_Horst_1–6, Rohrkolben_Jung_1–3 = Eldarien-Netze 0,4–3,2 k Dreiecke, ToadRush_00/02): Band 0,5–6 m, 0,22/m²,
  Gruppen 4–12 in 2,2 m, Hang ≤ 12°, Kippen 0,1 (aufrecht), Stillwasser ×2.
- `seggen` (grass_meadow_02/04/08, grass_bush_02/03, beach_grass_01_1/2, rough_horsetail_01–03): Band 1–12 m, 0,10/m², Stillwasser ×1,5.
- `uferstaude` (petasites_spurius_01–03 = Pestwurz, Goldrute, Topinambur, Nessel, hedge_bedstraw, Periwinkle_01): Band 2–16 m, 0,03/m².
- `uferwurzel` (crooked_root_01/021/04/05, MossyForestRoots_01/02): Steilufer (Hang ≥ 14°) 0,8–4 m vom Wasser, 0,012/m², voll gekippt.

**Budget** (`budget`): 60 000 je Feld (Ziel 52 000), ≤ 3 000 mit Kollision; Schichtziele 22 000 / 22 000 / 2 600 / 12 000; Ausdünnung
deterministisch in der Reihenfolge Kiesel → Zweige → Laub → … → Haine → Weiden → Totbaum → Solitär (Solitäre zuletzt).

**Overrides für Teil C/D** (gleiche Schlüssel wie `felsgruppen_regeln.json` / `spuren_regeln.json`):
- `felsgruppen_overrides`: Palette `moos`, Biomfaktor 0,35, Klassen `band`, `wand`, `grat`, `fuss` aus; `kuppe` nur Terrasse (p 0,5,
  Hang 4–30°), `blockstrom` nur Terrasse p 0,2, `prallhang` mit Krümmung ≥ 0,003, Uferabstand 2–8 m, 2–5 Blöcke + 6–14 Steine +
  15–30 Kiesel; Steine 40–55 % eingegraben; Lagen-Boost Geröll/Kies, Hemmung Wiese/Schlamm.
- `spuren_overrides`: Feldstreifen Ring 20–220 m, 70 % der Zellen, max 18 je Ort / 40 je Feld, Hang ≤ 6°, 45 % mit Frucht, Zaunlücken
  25 %, **Feldrand-Hecke** auf 50 % der Ränder (hazel_02, Elderberry_08, sea_buckthorn_01/02, Abstand 2,5 m, 30 % Lücken); Obstgarten
  max 2 je Ort, Ring 15–140 m, Reihe 6,5 m × 5,5 m, Ersatznetze Hornbeam_Forest_09/10 + beech_tree_00_C/D; Zäune 2–4 je Ort à 30–90 m;
  **neu `kopfweiden_reihe`** entlang Weg/Bach/Graben, Abstand 6–9 m, 30–90 m lang, 1–3 je Ort, ≤ 25 m vom Wasser, Ersatz
  Big_Tree_willow_01 auf 0,45–0,6 (7–10 m) als Akteur; **neu `muehle`** (nur Positionsliste: Bach mit ≥ 2 m Gefälle je 100 m, ≤ 250 m
  vom Ort); Stege nur an Stillwasser; Blickziel-Typen aue = Solitärbaum, Kopfweiden-Reihe, Ruine, Blumenlichtung, Mühle.

### 2.1 Planer `aue_plan.py` (FORMAT §3/§5)

- **Aufruf:** `python -I scripts/aue/aue_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]`; ohne
  `--basis` ist die production-Wurzel das Arbeitsverzeichnis, ohne `--regeln` gilt `aue_regeln.json` neben dem Skript. Keine
  Unreal-Importe, nur NumPy (+ Pillow für `--bild`); numba wird erkannt, aber nicht benötigt.
- **Lesen:** `hoehe.f32` als memmap, nur das Fenster Feld + 64 m (`fenster_rand_m`), ebenso `karte_*.r8`, `lage_*.r8`, `eigner.r8`
  (alle optional außer `hoehe.f32`; fehlende Dateien → Hinweis im Protokoll und in `plan.json["hinweise"]`). Randspalte J wird bei
  `NX` geklippt. Bestand aus `bestand/`, `witcher/` (Feld + 8 Nachbarn), `ufer/foliage_<Feld>`, `instanzen/instanzen.json`.
- **Rechnen:** Hang/Normale aus dem Gradienten; Wasserdistanz, nächste Wasserzelle und deren Höhe per Jump-Flooding (max 128 m);
  Stillwasser aus Polygonrasterung; Kronendach als Gauß-geglättete Baumdichte (σ 6 m) → Beschattung 0–1; Saum 10–12 m um Waldkanten;
  je Klasse eine Dichtekarte λ, dann Bernoulli-Zug per Hash (Rasterkoordinate, Seed 1105, Kanal) → Gruppenzentren → Mitglieder im
  Radius; Haine mit Mindestabstand über ein grobes Raster; Solitäre als 96-m-Raster. Kein Python-Loop über Zellen.
- **Budget:** Kollision > 3 000 → proportional; Schichtziele; dann Gesamtziel 52 000 über die Prioritätsliste. Harte Grenze 60 000.
- **Schreiben:** `export/unreal/welt/aue/<Feld>/<Netz>.f32` (10 float32 LE, alte f32 werden vorher gelöscht) und `plan.json` mit
  `stand, feld, instanzen, dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene}, entfernen (leer),
  ft_ordner, ft_praefix, statistik{je_klasse, je_schicht, kollision, hoehenstufen_anteil, …}, hinweise, ungetestet`.
  `--bild` → `docs/pruefung/aue/<Feld>.png` (1 px = 1 m; Höhenstufen getönt, Wasser blau, Stillwasser hellblau, Weg braun, Ort rot,
  Klassen nach `bild_farben`, Bäume/Kollision als Kreuz).
- **Inventarprüfung:** alle 211 Paletteneinträge (193 verschiedene Netze) gegen `daten/netze.csv`; fehlende Pfade werden mit Warnung
  gestrichen, der Lauf bricht nicht ab. Die 10 Override-Pfade (5 nur dort) wurden in der Cloud ebenfalls geprüft: alle vorhanden. Wüstenfelder C3 C4 D3 D4 D5 E3 E4 E5: Faktor 0,6, Sand/Sandstein ≥ 0,5 gesperrt,
  `entfernen` bleibt leer (nur ergänzen).

## 3. Abgrenzung zu vorhandenen Ebenen: ergänzen, nicht ersetzen

| Ebene | Verhältnis zur Aue-Ebene | `entfernen`? |
|---|---|---|
| Witcher-Bewuchs `FT_EL_WIT_*` (50 000 Kleinzeug: Haine, Waldsaum, Totholz, Farne, Laub, Blumeninseln Crownbeard/Lachenalia/Windflower, Gebüsch) | Aue nutzt **andere Netze** (Meadow-Blumen, Rohrkolben, Weiden, Pappeln, Hainbuchen-Haine) und andere Steuergrößen (Höhenstufe, Wasserabstand); WIT-Instanzen werden als `belegt` (1,2 m) geladen | nein. Vorschlag `entfernen_vorschlag`: `SM_KikuyuGrass_` (warmes Namaqualand-Gras der WIT-Ebene passt nicht in die Aue) – Standard aus, nach Abnahme einschalten |
| Wald-Bestand `FT_EL_BST_*` (17 000 Bäume) | Liefert das Kronendach (Beschattung → Laub/Zweige/Farn/Pilz hoch, Gras/Blumen niedrig) und den Saum; neue Bäume halten 3 m Abstand, Haine nur außerhalb (Beschattung ×0), Solitäre 40 m frei | nein |
| Ufer `FT_EL_UF_*` (26 000 Kiesel/Kopfsteine/Blöcke/Treibholz) | Aue setzt **keine** Uferkiesel und kein Treibholz; Schilf/Seggen/Stauden füllen die Pflanzenlücke 0,5–16 m; Kiesbänke dämpfen Schilf ×0,3; 0,8 m Sperrradius um Ufer-Instanzen | nein |
| Felsschalen `FT_EL_FS_*` | unberührt (Aue hat fast keine Felsen; Felsgruppen-Planer mit Overrides) | nein |
| Landschafts-Gras `GT_*` | bleibt die Basis 0,2–1,2 m; Aue-Grasbüschel (0,6–1,7 m) sind die Hero-Staffel darüber | nein |
| Wüste `FT_EL_WU_*` (C3–E5) | nur ergänzen: Faktor 0,6, Sand/Sandstein ≥ 0,5 gesperrt | nein |

Begründung „kein Ersetzen“: Jede vorhandene Ebene trägt einen anderen Maßstab (Bildkritik §1: „jede Fläche trägt genau einen
Maßstab“); die Aue-Ebene fügt die fehlenden Stufen dazwischen ein. Erst wenn im Editor doppelte Blumenflächen oder zu dichter
Unterwuchs sichtbar werden, sollte man die WIT-Dichte je Feld über deren Planer senken, nicht per `entfernen`.

## 4. Testanleitung

**Rauchtest Cloud (gelaufen, am 10.10. nach dem Abbruch wiederholt und nachgeprüft).** Mini-Produktionswurzel mit `hoehe.f32` in
voller Größe 7057 × 9577 (memmap, nur E5-Fenster beschrieben: flache Aue 12 m, Mäanderfluss 18 m breit, Bach, Altarm 110 × 36 m
mit Umriss in `wasser_welt.json`, Terrassenstufe +18 m, Kuppe), `karte_wasser/weg/ort.r8`, `lage_Wiese/Trockengras/Moos/Laub/Sand.r8`,
`eigner.r8` + `welt.json`, `bestand/E5` (190 Bäume in 3 Hainen), `ufer/foliage_E5` (3 000 Kiesel), `daten/netze.csv`. Ergebnis
`python -I scripts/aue/aue_plan.py E5 --bild --basis .`: **32 627 Instanzen (790 mit Kollision), 188 Netze, Laufzeit 8,5 s**
(9,3 s Wanduhr inkl. Bild; 4 Kerne, Python 3.13, NumPy 2.5, ohne numba), Schichten boden 11 980 / mittel 16 254 / baum 702 /
wasserkante 3 691 (E5 ist Wüstenfeld → Faktor 0,6; Anteil aue-Zellen 97,9 %, Höhenstufen Ufer 6,5 / Aue 36,2 / Terrasse 57,3 %).
Größte Klassen: Grasbüschel 7 791, Blumeninsel 4 516, Bodendecker 3 775, Laub 3 448, Seggen 1 755, Schilf 1 433, Strauch 1 251,
Hain 319, Pappel 177, Hecke 61, Weide 48, Solitär 40, Totbaum 19, Uferwurzel 1 (Synthetik-Ufer flach, Regel Hang ≥ 14° greift nicht).
Prüfskript: alle 188 f32 durch 10 teilbar, Anzahl = `plan.json`, Quaternionen normiert (|q|−1 ≤ 1,2·10⁻⁷), Schema inkl. `ebene`
vollständig, **0 Instanzen** auf Wasser/Weg/Ort oder außerhalb des Feldes, z − Gelände −0,82 m (Stämme 25 % eingegraben) bis
+0,41 m (Vergleichsartefakt an der Terrassenkante); zwei Läufe byte-identisch (MD5); Stillwasser-Umriss erkannt (28,9 % der
Uferzellen); Kiesbank-Dämpfung aktiv (8,7 % der Uferzone). Lauf mit nur `hoehe.f32` (F6, J7; keine Karten, kein Inventar): je
fehlender Datei ein Hinweis, Schichtbudget Boden 23 447 → 22 000 greift, J7 (Randspalte, 505 m breit) 22 774 Instanzen in 0,9 s;
ungültiges Feld (K9), fehlende Basis und fehlende Regeldatei → klare Meldung, Exit. Prüfbild `docs/pruefung/aue/E5.png` (1008 × 1008): Höhenstufen
getönt (Ufer blau, Aue grün, Terrasse beige), Stillwasser hellblau, Hain-Beschattung dunkel, Klassen nach `bild_farben`.

**Erwartete Instanzzahlen je Feld (Richtwert, Spanne ±35 %; Grundlage: Land-/Wasseranteil aus `biome_je_feld.md`, 0,05–0,06
Instanzen je m² Aue-Land nach Budget):**

| Feld | Land % / aue % | gesamt | boden | mittel | baum | wasserkante |
|---|---|---|---|---|---|---|
| C5 | 100 / 63 | 30 000–42 000 | 12 000–17 000 | 12 000–17 000 | 900–1 600 | 5 000–9 000 (Wasser 5,8 %) |
| E5, D5, C4 (Wüste ×0,6) | 97–100 / 93–75 | 20 000–34 000 | 8 000–13 000 | 8 000–14 000 | 500–1 100 | 3 000–7 000 |
| F4, F6 | 54 / 79, 51 / 96 | 20 000–30 000 | 8 000–12 000 | 8 000–12 000 | 500–1 000 | 2 500–5 000 |
| J6, D7, B7, F2 | 41–28 / 98–54 | 8 000–20 000 | 3 000–8 000 | 3 000–8 000 | 200–600 | 500–3 000 |
| A7, I1, F1, J5, A6, J3 (Sand 86–92 %) | 13–7 / 98–100 | 1 500–6 000 | 600–2 500 | 500–2 500 | 100–400 | 0–800 |
| G2, J7, F3 | 4–1 | 200–2 000 | – | – | 0–100 | – |

Kollision je Feld: 600–2 200 (Bäume 500–2 000, große Stämme 50–200) – unter 3 000; bei Überschreitung dünnt der Planer alle
Kollisionsklassen proportional.

**Prüfkameras (Feld, Position als Raster-/Weltkoordinate, Blick):**
1. **E5 Flussufer, Augenhöhe 1,7 m**, am Außenbogen des Hauptflusses, Blick flussaufwärts gegen die Sonne (Vergleich W6FIN_E5, witcher_01).
   Erfolg: Schilfgürtel 0,5–6 m mit Lücken an Kiesbänken, dahinter Seggen/Pestwurz, Weiden 3–28 m in 2–5er-Gruppen, keine Pflanze
   schwebt über der Wasserkante (Eingraben 3–4 cm), keine Instanz im Wasser.
2. **C5 Aue, 2 m Höhe, 60 m vom Wasser**, Blick quer zur Aue auf die Terrasse. Erfolg: innerhalb 10 m mindestens ein Objekt in 0,5–3 m
   Höhe (Grasbüschel/Strauch/Jungbaum), Blumeninseln als Flecken (nicht Streu), Pappelgruppe im Mittelgrund, Hainbuchen-Hain mit
   Lichtung am Horizont, Solitärbaum als Blickziel.
3. **F6 Altarm/Teich (Stillwasser)**, 3 m Höhe, Blick über das Wasser. Erfolg: Schilf doppelt so dicht wie am Fluss, Totbaum am Ufer,
   keine Kiesel am Stillufer.
4. **D5 Weg mit Hecke, 1,7 m, Blick entlang des Weges** (außerhalb 150 m vom Ort). Erfolg: Heckenabschnitte 4–7 m neben dem Weg, 40 %
   der Strecke, Sträucher längs ausgerichtet, nichts näher als 4 m am Weg.
5. **Draufsicht 300 m über C5** (Prüfbild und Editor). Erfolg: Haine als Clumps 20–40 m mit 25 % Lichtungsfenstern, kein 15-m-Raster,
   Weiden nur am Wasserband, Terrasse mit Kiefern-Gruppen auf Trockengras.
6. **Nahtprüfung** an der Grenze C5/D5 und E5/F5 (Draufsicht 100 m): keine Dichtesprünge, Gruppen laufen über die Grenze (Fenster + 64 m).

**Erfolgskriterien in Zahlen:** Instanzen je Schicht innerhalb der Tabelle; Kollision < 3 000; Setzer-Zeit je Feld < 5 min
(188 Netze → 188 Foliage-Typen `FT_EL_AU_*`, davon 25 Baum-/Stammtypen mit Kollision); kein Netz mit Nicht-Nanite-Bäumen
(Poplar, Big_Tree_willow) ohne LOD-Prüfung; PNG und `plan.json` je Feld vorhanden.

## 5. Einkaufsliste fehlender Assets (frei bevorzugt, Stufe High 4K)

| Was | Exakter Name (Fab/Megascans) | Stufe | Wofür | Status |
|---|---|---|---|---|
| **Kopfweide** (Salix alba, pollard) | nicht gefunden; Megascans führt keine Kopfweide. Kandidaten: Fab-Suche „Pollard Willow“ (Drittanbieter) oder eigene Variante aus `Big_Tree_willow_01` (Stamm kürzen) | High | `kopfweiden_reihe` (Spuren-Override), Gräben, Weg- und Bachränder | **offen**, Ersatz Big_Tree_willow_01 × 0,45–0,6 |
| **Weide/Erle Nanite** (Salix, Alnus) | Fab „Stylized Willow Tree“ (c6bfbdf6-…) ist stilisiert, 2 947 Dreiecke, Nanite „not recommended with wind“ **[Suchauszug]** – ungeeignet; Megascans Trees „European Black Alder“ / „White Willow“ bei Erscheinen prüfen | High | Ersatz der Nicht-Nanite Big_Tree_willow (30–38 k Dreiecke) | offen |
| **Obstbäume** (Apfel, Birne, Pflaume) | Fab-Suche „apple tree Nanite“ lieferte keinen Treffer **[Suchauszug]**; Megascans „Apple Tree“ (Trees-Kollektion) prüfen | High | Obstgarten je Weiler (Weißgarten) | offen, Ersatz Hornbeam_Forest_09/10 |
| **Hecken** (Weißdorn, Schlehe, Haselhecke als Segment 2–4 m) | keine Treffer; Megascans „Hawthorn“ / „Blackthorn“ prüfen | High | Feldrand- und Wegsaum-Hecken | offen, Ersatz sea_buckthorn + hazel |
| **Schilf-Varianten** (Phragmites) | Quixel „Megaplants: Dry Common Reed“ (fab.com/listings/00299cb6-8602-4736-8565-4b19b41f5686): prozedurales Asset, braucht Plugin Procedural Vegetation Editor + „Nanite Foliage (Experimental)“, erzeugt mehrere Varianten je Paket **[Suchauszug]**; im Projekt ist Megaplant_Library nur als Karten da, kein Streunetz. Alternative Drittanbieter „Common Reed mid poly, 3 Netze, auto LODs“ **[Suchauszug]** | High | Schilfgürtel am Fluss (Rohrkolben = Teich-Optik) | **prüfen**: Megaplants in 5.8.3 (PVE experimentell) oder 3-Netz-Set |
| **Liegender Hero-Stamm am Ufer** (> 5 m, mit Wurzelteller, freigespült) | Taxonomie-Lücke aue: nur 5 Netze > 5 m, keines mit Uferbezug. Megascans „Fallen Tree“ / „Uprooted Tree“ (Trees-Kollektion) oder Fab „Nanite Fallen Tree with Roots“ prüfen | High | Prallhang-Akzent, Totholz quer zum Bach (witcher_03) | offen, Ersatz LargeFallenTree_02 + MossyForestRoots |
| **Seggen/Binsen** (Carex, Juncus) | Megascans „Soft Rush“ / „Sedge“ prüfen; ToadRush vorhanden (15–29 k Dreiecke ohne Nanite, nur 2 Netze eingesetzt) | High | Band 1–12 m | offen |
| **Feldfrüchte** | Fab „Nanite Foliage – Wheat Field“ (dbcbdc42-…), Vollgeometrie ohne Alpha, Wind + Interaktion, UE 5.1+, Update 08/2025 **[Suchauszug]** | – | Feldstreifen (Spuren) | **kaufen** (Preis nicht ermittelt) |
| **Wassermühle** | kein Mühlen-Netz im Inventar; Fab-Suche „medieval watermill“ (Hivemind/Meshingun-Kits enthalten keine) | High | Blickziel am Bach | offen |
| **Herbstlaub-Varianten** | Megascans Hornbeam hat nur Sommerlaub; Alternative: Material-Instanz `MI_EuropeanHornbeam_*` mit Tint (kein Kauf) | – | Farbakzent Herbst (witcher_07) | Material statt Kauf |
| **Uferstauden** (Mädesüß, Blutweiderich, Iris) | Megascans „Purple Loosestrife“, „Meadowsweet“, „Yellow Iris“ prüfen | High | `uferstaude` | offen, Ersatz Pestwurz/Goldrute |

Kostenhinweis aus `boden-kleinzeug-gras.md`: Megascans ist seit 2025 pro Asset kostenpflichtig (ab 0,99 USD), sofern nicht vor dem
31.12.2024 beansprucht – zuerst im Fab-Konto prüfen, welche der oben genannten Namen schon lizenziert sind.

## 6. Offene Punkte und Annahmen

1. **Formate der optionalen Dateien** (`wasser_welt.json` `seen[].umriss` als `[[x_cm, y_cm], …]`, `teiche/teiche.json`,
   `docs/staedte/standorte.json` mit `x_cm/y_cm` oder `x/y` + `radius_m`) sind aus FORMAT §2 abgeleitet; abweichende Strukturen werden
   mit Hinweis ignoriert, der Planer läuft dann ohne Stillwasser bzw. ohne Standortsperre.
2. **Höhe des nächsten Wassers** wird aus `hoehe.f32` an der nächsten Wasserzelle gelesen (Jump-Flooding). Liegt das Wasserspiegel-
   Mesh höher als die Landschaft unter dem Fluss, ist `hrel` zu groß → Aue-Stufe zu schmal; dann `aue_hrel_max_m` auf 6–8 setzen.
3. **Ufer-Ebene**: Der Planer liest `ufer/foliage_<Feld>/plan.json` + f32 und erkennt Kiesbänke an der Steindichte (> 3 im 7×7-Fenster).
   Falls die Ufer-Ebene ihre Instanzen unter anderem Pfad ablegt, greift nur noch die Wasserabstands-Regel.
4. **Witcher-Ebene `witcher/<Feld>/`**: Als Nicht-Baum-Instanzen „belegt“ gelesen; der Planer erkennt Bäume dort nur am Namen
   (Hornbeam, beech, pine, willow, poplar, birch); Rollenfeld `rolle` in deren `plan.json` wäre zuverlässiger.
5. **Nicht-Nanite-Bäume** (Poplar_*, Big_Tree_willow, beech_tree, pine_beach): Sichtweite 0, aber LOD-Übergänge im Editor prüfen; bei
   Nanite-Umstellung Masken-Material/WPO beachten (Taxonomie, Qualitätshinweise). ToadRush ohne Nanite (15–18 k Dreiecke) steht nur mit
   2 von 11 Schilf-Netzen in der Palette.
6. **Hecken-Richtung** kommt aus dem Gradienten des geglätteten Weg-Distanzfelds; an Kreuzungen ist der Yaw unbestimmt (±90°) –
   dort stehen Sträucher schief zur Straße; akzeptabel, sonst Kreuzungszellen (zwei Wege < 10 m) ausnehmen.
7. **Eingraben nach Netzhöhe** gilt nur für `totholz_gross` (25 % der Höhe aus `netze.csv`); Pivot-Lage der Stämme (Mitte oder unten)
   ist unbekannt – `netze_masse.json` hat für `SM_trunk_01/02` keine Bounds; nach dem ersten Setzen prüfen, ob Stämme schweben.
8. **Zahlen** aller Dichten sind aus Bildern geschätzte Richtwerte; die Witcher-Quellen nennen keine Instanzen je m². Erster
   Kalibrierschritt: C5 und E5 setzen, Kamera 1 und 2 aufnehmen, `--faktor 0,7 … 1,4` vergleichen.
9. **Felder mit Sand-Strand** (F1, I1, J3, J5, A6, A7, J7: Sand 86–98 %) bekommen über die Sand-Dämpfung nur ~25 % der Aue-Dichte; ob
   dort überhaupt Aue-Bewuchs gewünscht ist (Küstenwiese?) entscheidet Ferat – sonst diese Felder nicht planen.
10. **Grenzen des Rauchtests**: flaches Synthetik-Gelände → Hangregeln (Uferwurzel ≥ 14°, Bäume ≤ 30°, Schilf ≤ 12°) und
    Höhenabnahme ab 80 m ungetestet; `witcher/<Feld>/` und `instanzen.json` fehlten (Code nur syntaktisch geprüft). Erstes
    Echtdaten-Feld daher D7 (bis 319 m, 27 % steil) neben C5.
11. **Status-Datei** `verteilung-STATUS.md` wurde nicht verändert (Koordinator); B2 kann auf „fertig (ungetestet mit Echtdaten)“
    gesetzt werden.

## Korrektur Runde 2 (10.10.2026)

- Keine gesperrten Netze und keine Platten im aue-Planer. `kiesel` (Schicht 0) hat `teppich_sperre`: nur auf/bis 6 m um Kies-/Geroell-/Fels-Lagen >= 80/255, bis 3 m am Weg, bis 5 m am Wasser (Kiesbaenke bleiben Ufer-Ebene).
- Rauchtest synthetisch F5 (Wiese-dominiert, wenig Kies): Kiesel 3 285 -> 245, Flaechenteppich-Kiesel 3 019 -> 0; Feld 25 796 Instanzen, zwei Laeufe byteidentisch, Log ASCII, 8 s. Auf Echt-F5 (Geroell 15 %, Sand 35 %) faellt der Rueckgang kleiner aus.

## Korrektur Runde 4 (10.10.2026): Meer fehlt in `karte_wasser`

Ursache: Der Landzellen-Bezug war `karte_wasser == 0`. Das Meer steht nicht in `karte_wasser` und hat eigner 0, zählte also als aue-Landzelle. Deshalb lagen 51 % der Instanzen unter 0 m (gemessen 176 k). Umgesetzt nach Konventionen §1b:

- `meer = hoehe < 0 & karte_wasser == 0`, `wasser_alle = karte_wasser > 0 | meer`. Landzellen = ohne `wasser_alle`. Das gilt für aue-Anteil, Leerplan-Schwelle 2 %, Saum, `zellen_zustaendig`, `biome_fenster` (`biome_fenster_bezug`), Sperre (`abstand_m.wasser_klein/gross`) und Ufer-Kieselmaske. Am Süßwasser bleiben: Höhenstufen ufer/aue/terrasse, Feuchte, `d_wasser_m` von Schilf/Seggen/Uferstauden/Uferwurzeln/Auwald, Weiden-Solitäre und Ufer-Yaw.
- Neuer Block `meer` in `aue_regeln.json` (`tief_m` −0,3, `saum_hoehe_m` 0,3, `saum_m` 30). Unter −0,3 m nichts. −0,3…0 m nur `meer_rolle`, aue hat keine. 0…+0,3 m im Küstensaum nur Schicht 5 wasserkante oder `strand: true`.
- Schlussfilter: Er prüft die Geländehöhe bilinear am Instanzort und an der Küste z nach dem Eingraben ≥ −0,3 m. `plan.json` meldet `meer_zellen` und `meer_gefiltert` (auch im Leerplan), `statistik` meldet `meer_anteil`, `kuestensaum_zellen_feld` und `meer_gefiltert_je_klasse`.
- Rauchtest synthetisch (A5/B5 Küstenfelder mit aue-Band am Fluss bzw. ohne aue-Land, J6 aue-Küstenfeld mit Fluss und Sandbank; Meer nicht in `karte_wasser`; Raster danach gelöscht):

| Feld | Gesamt vorher → nachher | Gelände < 0 m vorher → nachher | 0…0,3 m Küstensaum vorher → nachher |
|---|---|---|---|
| A5 | 10 275 → 2 340 | 7 142 → 0 | 798 (Bäume 18, Kiesel 420, Laub/Zweige/Bodendecker 207, Blumeninseln 89, Wasserkante 64) → 57 (nur Schilf/Seggen/Uferstauden an der Flussmündung) |
| B5 | 7 237 → 0 (Leerplan: aue-Anteil der Landzellen 0 %) | 6 517 → 0 | 702 → 0 |
| J6 | 21 732 → 13 946 | 6 683 → 0 | 1 091 → 34 (nur Wasserkante) |
| Summe | 39 244 → 16 286 | 20 342 (52 %) → 0 | 2 591 → 91 |

`meer_gefiltert` J6 7. Instanz-z < −0,3 m: 0. Zwei Läufe byteidentisch, Log ASCII, `py_compile` ok, 3–8 s je Feld. Ein Feld ohne Meer (C6) läuft unverändert durch, `meer_zellen` ist dort 0.
