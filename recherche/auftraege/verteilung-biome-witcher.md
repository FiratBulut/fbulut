# Auftrag 11: Asset-Analyse und Verteilungs-Skripte je Biom in Witcher-Qualität (parallel, mehrere Agenten)

- Projekt: Eldarien (Spielwelt zum Roman „Das Lied der Asche“), Unreal Engine **5.8.3**, World Partition, Nanite, Landschaft 9,6 × 7 km.
- Priorität: **hoch** (Ferat, 10.10. 13:35). Detailgrad: Regelwerke knapp und zahlenfest, Skripte vollständig lauffähig (ungetestet markieren).
- Ziel: Ferats Messlatte **Witcher 3 Next-Gen / Witcher-4-Demo** (`bilder/witcher_01…07.jpg`, Analyse in `vorlagen/doku`, Vorgaben in
  `antworten/bildkritik-witcher-messlatte.md`). Ferats Befund zur heutigen Welt (wörtlich sinngemäß): „Auch wenn die Welt korrekt aussieht,
  fehlt etwas, was mir ein Gefühl der Leere gibt. Die Asset-Platzierung ist nicht gut gelungen. Vor allem die Felsen an den Bergen sehen aus,
  als wären sie einfach hingeklebt, nicht organisch verbunden.“

**Bitte parallel mit mehreren Agenten arbeiten** (Ferat will die Parallelität der Cloud ausnutzen). Jeder Agent liefert eigene Dateien
(Abschnitt „Lieferung“); ein Koordinator pflegt `antworten/verteilung-STATUS.md` (welcher Teil fertig, welcher offen).

## Material im Repo

| Was | Wo |
|---|---|
| Datenformate, Konventionen, Budgets, vorhandene Ebenen (**zuerst lesen**) | `vorlagen/FORMAT.md` |
| Asset-Inventar: 1 435 Netze (Pfad, Paket, Dreiecke, Nanite, Maße m, Material-Anzahl, Kollision, in welchem Foliage-Typ/Gras benutzt) | `vorlagen/daten/netze.csv` (Trenner `;`), vollständig `vorlagen/daten/inventar.json` (auch 1 373 Pflanzentypen, 19 Grasarten, Material-/Texturzählung je Paket) |
| Zählung je Paket | `vorlagen/daten/zusammenfassung.md` |
| Netz-Bounds (min/max cm) für 451 bereits genutzte Netze | `vorlagen/daten/netze_masse.json` |
| Biome, Land-, Höhen-, Steilheits-, Wasser- und Lagenanteile je Gitterfeld (62 Landfelder) | `vorlagen/daten/biome_je_feld.md` / `.json` |
| Ist-Zustand (17 Bilder, Stand 10.10. früh) und 7 Zielbilder | `bilder/` |
| Frühere Antworten (Kleinzeug, Ufer, Klippen, Dunst, HLOD, Bildkritik) | `antworten/` |

Nicht im Repo (nur lokal): die Rasterdaten selbst (`hoehe.f32`, `lage_*.r8`, …) und der Quellcode der vorhandenen Planer. Die Skripte
werden deshalb **blind** geschrieben und lokal getestet; Fehler kommen als `auftraege/verteilung-<thema>-korrektur.md` zurück.

## Teil A (ein Agent, zuerst, kurz): Asset-Taxonomie

Alle 1 435 Netze aus `netze.csv` nach Rolle und Biom-Eignung einordnen. Rollen: `fels_hero` (> 3 m), `fels_block` (0,8–3 m), `fels_stein`
(< 0,8 m), `geroell_platte`, `klippe_schale`, `baum_<art>_<alter>` (jung/mittel/alt/tot), `jungbaum`, `strauch`, `farn`, `bodendecker`, `blume`,
`grasbueschel`, `totholz_stehend|liegend|stumpf|ast|wurzel`, `ufer_stein`, `schilf`, `mensch_<zaun|mauer|ruine|karren|brunnen|schrein|…>`,
`sonst`. Biom-Eignung 0–2 für jedes der 15 Biome (`FORMAT.md` §2). Qualitätsmarken: Dreiecke je m², Nanite ja/nein, Megascans-Stufe
(Raw 8K / High / Medium aus Pfad `…/Raw/…`), Material-Anzahl, Kollision vorhanden. Ergebnis `antworten/assets-taxonomie.json`
(`{"<pfad>": {"rolle": …, "biome": {…}, "hoehe_m": …, "note": …}}`) + `antworten/assets-taxonomie.md` (Lücken je Biom: was fehlt?).
Wichtig: Netzname und Paket verraten viel (Megascans-Namen, `Mountain_Environment_Set`, `Coast_Dunes`, `Meadow`, `Forest`, `Lava_Volcano`,
`Namaqualand`, `Megaplant_Library`, `Fab/Megascans/3D|Plants`); Maße stehen in der CSV.

## Teil B (parallel, ein Agent je Biomgruppe): Regelwerk + Planer-Skript

Biomgruppen (Felder laut `biome_je_feld.md`): 1 **Nordküste** (fjord, kueste, bergwald), 2 **Aue/Flussauen** (aue), 3 **Heide/Tundra**,
4 **Gletscher/Frost/Hochgebirge**, 5 **Elfenwald**, 6 **Sumpf**, 7 **Dschungel** (inkl. Karst-Kalktürme G6 H6 I6 I7), 8 **Lava**,
9 **Wüste/Canyon/Ödland** (nur ergänzen, eigener Planer existiert).

Je Gruppe:
1. **Witcher-Analyse** des vergleichbaren Schauplatzes (Skellige für Fjord/Küste/Bergwald, Velen für Sumpf/Aue, Weißgarten/Toussaint für
   Aue/Heide, Kaer Morhen für Hochgebirge, Witcher-4-Demo Kovir/Flussauen): Welche Schichten füllen das Bild zwischen Boden und Krone?
   Dichten, Gruppengrößen, Höhenstufen, Farbakzente, Blickziele, Spuren von Leben. Mit Quellen (Breakdowns, GDC-Talks, Artstation).
2. **Regelwerk** als `<thema>_regeln.json`: Schichten `0 boden` (Laub, Zweige, Kiesel, Pilze), `1 mittel` (0,3–3 m: Sträucher, Jungbäume,
   Farninseln, Beeren, liegendes Holz, Grasbüschel verschiedener Höhe), `2 baum`, `3 fels` (siehe Teil C), `4 spuren` (Teil D),
   `5 wasserkante`. Je Schicht: Netzpalette (Pfade aus der Taxonomie), Dichte je m² nach Lage (`lage_*`), Hang, Höhe, Nähe zu Wasser/Weg/
   Wald/Fels, Gruppengrößen und -abstände, Maßstabsbereiche, Eingraben, Ausrichtung, Sichtweiten, Kollision, Budget je Feld.
3. **Planer-Skript** `<thema>_plan.py` nach `FORMAT.md` §3/§5 (NumPy/numba, deterministisch, Fenster Feld + Rand, Ausgabe f32 + plan.json,
   `--bild`). Es ersetzt NICHT die vorhandenen Ebenen (Witcher, Bestand, Ufer, Felsschalen), sondern ergänzt sie; wo es ersetzen soll,
   `entfernen`-Filter im plan.json und Begründung.
4. **Testanleitung**: erwartete Instanzzahlen je Feld (Spanne), Prüfkameras (Feld, Position, Blickrichtung), woran man Erfolg erkennt.
5. **Einkaufsliste**: fehlende Assets mit exaktem Fab-/Megascans-Namen (frei bevorzugt), Stufe (High 4K reicht meist), wofür.

## Teil C (parallel, Querschnitt): „Fels organisch“ – Felsen, die zum Berg gehören

Heute: Felsschalen (offene Klippenschalen an Steilwänden, statistisch verteilt) + kleine Füller als Foliage, dazu Megascans-Blöcke.
Wirkung: aufgeklebt. Gesucht:
1. **Geologische Platzierungsregeln** aus den Rasterdaten: Grate und Kämme (Krümmung/Hangknick aus `hoehe.f32`), Felsbänder in gleicher
   Höhenlage und gleicher Schichtneigung je Berg, Schuttfächer unter Wänden > 50° (Größe nimmt hangabwärts ab), Blockströme am Hangfuß,
   Einzelblöcke auf Kuppen, Felsnasen an Flussprallhängen; nichts in Mulden ohne Wand darüber. Gruppengrammatik: Hauptfels + 2–5 Nebenblöcke
   + Schutt + Kiesel, gemeinsame Hauptrichtung, Eingraben 25–45 %, Kippen in den Hang, Lehnen an die Wand.
2. **Kontaktzone**: Geröllsaum (Foliage-Steine 5–40 cm im Umkreis 0,5–2 m), Moos/Gras hochkriechend (Netzpalette), Boden-Blend des
   Felsmaterials über die Runtime Virtual Texture (`RVT_Eldarien_Boden`; ein eigener Master `M_EL_Klippe_RVT` mit Fußblend ist in Arbeit):
   beste UE-5.8-Technik mit Quellen (RVT-Sample im Mesh-Material, Höhenband, Dither/Pixel-Depth-Offset, Normal-Blend, Kosten).
3. **Planer** `felsgruppen_plan.py` (Format §3; große Stücke als Akteurliste mit `rolle: akteur`, kleine als Foliage) + Regeln-JSON +
   Testanleitung (Kameras auf Grate B4, C2, D2, E1; Küste A5; Lava-Fuß), plus Empfehlung, welche Felsschalen-Klassen danach entfallen.

## Teil D (parallel, Querschnitt): „Leere füllen“ – Mittelschicht und Spuren von Leben

1. **Mittelschicht 0,3–3 m** in allen Biomen (Sträucher, Jungbäume, Farn-/Beereninseln, Schösslinge an Lichtungsrändern, Stümpfe, Holzstapel
   aus Totholz, Grasbüschel/Hochstauden verschiedener Höhe, Pilze): Regeln nach Lichtverhältnis (Kronendach aus Baum-Ebene schätzen), Wald-
   rand (Saum 5–15 m dichter), Feuchte (Wassernähe, Lagen Schlamm/Moos), Hang. Richtwert Witcher: kaum ein Blick ohne Objekt in 0,5–3 m Höhe
   innerhalb 10 m.
2. **Spuren von Leben**: Zäune, Steinmauern, Steinmänner, Wegkreuze/Schreine, verlassene Karren, Feldstreifen und Obstbäume um Orte
   (`docs/staedte/standorte.json` nur lokal: Felder/Positionen stehen in `biome_je_feld.md` nicht – Planer soll Orte aus `karte_ort.r8`
   ableiten), Fischerstege an Seen, Holzschlag-Lichtungen, Köhlerplätze, Gräber, Rauchsäulen-Positionen (als Punktliste für Partikel).
   Welche Assets dafür im Inventar sind (`Village`, `MedievalFantasyVillage`, `HauntedVillage`, `Graveyard`, `AncientRuins`, `Bazaar`) und was fehlt.
3. **Blickziele**: je Landfeld 1–3 Vorschläge (Ruine, Solitärbaum, Felsturm, Wasserfall, Lichtung mit Blumen) mit Koordinatenregel.
4. **Planer** `mittelschicht_plan.py` und `spuren_plan.py` (Format §3) + Regeln-JSON + Testanleitung.

## Lieferung (Dateien in `antworten/`)

- `assets-taxonomie.json` + `.md` (Teil A).
- `verteilung-<thema>.md` (Analyse, Regelwerk-Erklärung, Testanleitung, Einkaufsliste) je Teil B-Gruppe (`nordkueste`, `aue`, `heide-tundra`,
  `hochgebirge`, `elfenwald`, `sumpf`, `dschungel`, `lava`, `wueste`), `verteilung-fels-organisch.md` (C), `verteilung-leere-fuellen.md` (D).
- Skripte unter `antworten/skripte/`: `<thema>_plan.py`, `<thema>_regeln.json` (Teil B je Gruppe, C: `felsgruppen`, D: `mittelschicht`, `spuren`).
- `verteilung-STATUS.md` (Koordinator): Tabelle Teil/Agent/Stand/Datei; wird bei jedem Push aktualisiert.
- Reihenfolge nach Nutzen: **C und D zuerst** (Ferats Hauptkritik), dann B1 Nordküste (größte Fläche), B2 Aue, B4 Hochgebirge, B3, B5, B6, B7, B8, B9.

Rahmen: RAM 47 GB, Budget ≤ 60 000 Instanzen je Feld und Ebene (≤ 3 000 mit Kollision), HISM-Foliage, Nanite-Netze bevorzugt, keine
Blueprints. Antworten auf Deutsch, Zahlen statt Beteuerungen, Ungetestetes als ungetestet markieren.
