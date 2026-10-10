# Verteilung Biomgruppe 5: Elfenwald (alter Laubwald mit Lichtungen, Elfenruinen)

**Auftrag 11, Teil B5.** Biom `elfenwald`, Foliage-Präfix `FT_EL_EW_`, Ordner `/Game/Eldarien/Welt/Foliage/Elfenwald`. Stand 2026-10-10
(Fortsetzung nach API-Abbruch; Regeln und Planer-Entwurf des Vorgängers geprüft, korrigiert und rauchgetestet). Lieferung: dieser
Bericht, `skripte/elfenwald_regeln.json` (8 Baumklassen + 26 Streuklassen in 4 Schichten, 247 eindeutige Netzpfade, alle gegen
`netze.csv` geprüft, 0 fehlend), `skripte/elfenwald_plan.py` (1 179 Zeilen, FORMAT §3/§5). **Alles UNGETESTET MIT ECHTDATEN** – in der
Cloud nur mit synthetischen Rastern (G4, §5) rauchgetestet. Web-Quellen waren nur als Suchmaschinen-Auszüge lesbar (6 WebSearch-Läufe,
mode extended); solche Belege sind mit **[Suchauszug]** markiert, Zahlen ohne Beleg mit **Richtwert**.

Felder (laut `biome_je_feld.md`): **G3** (elfenwald 97 %, Land 72 %, Laub 56 %), **H3** (100 %, Land 89 %, 60 % steil, Fels 26 %),
**G4** (76 % + heide 22 %, Land 100 %, Laub 75 %, Moos 6 %, Wasser 5 %), **H4** (82 % + aue/sumpf, Land 100 %, 33 % steil), **I4**
(bergwald 78 / elfenwald 21), **H2** (kueste 78 / elfenwald 20), **G2** (Land 4 %). Der Planer läuft je Zelle mit Biomfaktor (elfenwald
1,0; bergwald 0,6; aue 0,5; sumpf 0,35; kueste 0,3; heide 0,25; alles andere 0) aus `eigner.r8`/`welt.json`; Kennzahl 0 und fehlende
Datei → dominantes Feldbiom aus `feld_biom_fallback` (I4 bergwald, H2 kueste, G2 aue, sonst elfenwald). **Überholt durch Korrektur
Runde 1 (nächster Abschnitt):** nur elfenwald-Zellen + 30-m-Saum, Kennzahl 0 = aue, Budget 60 000/3 000 je Feld, Mittelschicht in Teil D.

---

## Korrektur Runde 1 (10.10.2026): gilt vor allen folgenden Abschnitten

Grundlage: `auftraege/verteilung-korrektur-runde1.md` (Echtdaten-Test 10.10. 15:30) und `antworten/verteilung-KONVENTIONEN.md` (verbindlich).
Geändert wurden nur `skripte/elfenwald_plan.py` (jetzt 1 373 Zeilen), `skripte/elfenwald_regeln.json` und dieser Bericht. Wo §2, §4, §5 und §7
etwas anderes sagen, gilt dieser Abschnitt.

**Echtdaten-Befund (Referenz, lokal, alte Fassung):** A5 (bergwald/fjord) **2 152** Instanzen, G4 (elfenwald) **86 811**, E1 (gletscher) 0,
C6 (lava 99 %) **5 875**. Dabei war G4 um 45 % über dem Deckel von 60 000, und A5/C6 lagen in fremden Biomen. Ursachen: (1) `biom_faktor` hat
auch bergwald ×0,6, aue ×0,5, kueste ×0,3 und heide ×0,25 bebaut, und Kennzahl 0 wurde auf das dominante Feldbiom statt auf `aue` gelegt;
(2) das Budget galt je Schicht (Boden 52 000 + Mittel 48 000 + …) statt je Feld; (3) die Mittelschicht doppelte Teil D.

### Was sich geändert hat

1. **Zuständigkeit (§1):** Das Biom je Zelle kommt aus `eigner.r8` + `welt.json["kacheln"][k]["rezept"]`. **Kennzahl 0 ist `aue`**, ein Rezept mit
   „vulkan“ oder „lava“ ist `lava`, unbekannte Rezepte zählen als `aue` und erzeugen eine Logzeile. Nur wenn `eigner.r8` oder `welt.json` fehlt,
   gilt das dominante Feldbiom aus `daten/biome_je_feld.json` (sonst `feld_biom_fallback`, dazu ein Hinweis im Log). `biome_eigen = ["elfenwald"]`;
   `biom_faktor` ist ersetzt durch `zustaendigkeit` in der Regeldatei. Bebaut werden nur elfenwald-Zellen und ein **Saum von 30 m**, in dem der
   Faktor linear von 1 auf 0 fällt. Er wird aus einem Jump-Flooding-Distanzfeld über die Biom-Maske berechnet, also in NumPy ohne Zellschleife,
   und gilt für alle Schichten einschließlich der Bäume. Liegt der Eigenanteil im Fenster unter **2 %**, schreibt der Planer einen **leeren
   `plan.json`** (`instanzen: 0`, `dateien: {}`, `leer: true`, ohne f32; alte f32 werden gelöscht) und meldet das in einer Zeile.
   Das `entfernen` für Witcher-Netze setzt er nur noch, wenn der elfenwald-Anteil **im Feld** mindestens 50 % beträgt; in I4, H2 und G2 behalten
   die Fremdbiome dadurch ihre Witcher-Ebene.
2. **Pflichtschlüssel (§2)** in jedem `plan.json`, auch im leeren: `biome_fenster` (Anteile aller Biome im Fenster), `zellen_zustaendig`
   (Zellen im Feld mit Faktor > 0, also mit Saum, nur Land), `biome_eigen`, `kollision_anzahl` (Summe der Dateien mit `kollision: true`).
   Zusätzlich gibt es `eigenanteil_fenster/_feld`, `saum_m`, `biom_quelle`, `budget` (Deckel, Ziel, Zahl vor der Ausdünnung, Faktoren je Klasse,
   Netze ohne Kollision) und `an_landschaftsgras`.
3. **Budget (§3, hart), Schlüssel `budget`:** `deckel_je_feld` 60 000 für die ganze Ebene `elfenwald/`, `ziel_je_feld` 45 000–52 000,
   `ausduennen_auf` 52 000, `kollision_je_feld` **3 000 einschließlich der Bäume**. Die frühere Ausnahme `kollision_baum_je_feld` 20 000 entfällt.
   - **Dichten der Bodenschicht gesenkt:** Laubhaufen [0,006; 0,024] → [0,004; 0,015] (−37,5 %), Zweige [0,004; 0,014] → [0,0025; 0,009]
     (−36 %), Moos [0,003; 0,020] → [0,002; 0,014] (−30 %), Sauerklee/Kraut [0,004; 0,016] → [0,003; 0,011] (−31 %). Ast und Pilz sind in die
     Mittelschicht gewandert (Teil D).
   - **Ausdünnung bei Überlauf:** Liegt die Summe über 52 000, wird deterministisch per Hash in der Reihenfolge `prioritaet_ausduennen`
     ausgedünnt: zuerst Laubhaufen, Zweige, Kraut, Moos und Kleinsteine, dann kleine Uferpflanzen, Blumen, Ringe, Moos-Stamm, Bäume zuletzt.
     Je Klasse fallen höchstens 60 % weg, danach folgt die nächste Klasse; reicht das nicht, werden alle Nicht-Baum-Klassen gleichmäßig
     ausgedünnt, und eine harte Sicherung hält 60 000. Jede Ausdünnung schreibt eine `WARNUNG` ins Log und einen Hinweis ins `plan.json`.
   - **Kleinzeug an das Landschafts-Gras:** `hinweise` und `an_landschaftsgras` nennen Laub, Zweige, Moos und Kraut → `GT_Kraut` (die Grasart
     enthält laut `netze.csv` bereits DeadLeaves_01/02/05/10/12/13, WoodenSticksAndTwigs_01/04/07, DryBranches_01/04 und Pilze) sowie
     Kleinsteine → `GT_Steinchen`. Ebenfalls dort steht der Anteil, der wegen des Budgets abgegeben wurde. Empfehlung: Lage Laub/Moos im
     Elfenwald mit hoher GT_Kraut-Dichte malen. Die Elfenwald-Ebene setzt dann nur die Haufen in Mulden und am Stammfuß.
   - **Kollision je Netz:** Die Netze bekommen Kollision in der Reihenfolge `kollision_prioritaet` (hero, tot, alt, moosstamm, pappel, mittel,
     birke, weide, jung), innerhalb einer Klasse das kleinste Netz zuerst, bis 3 000 erreicht sind. Alle weiteren Netze erhalten
     `kollision: false`, und der Hinweis nennt die betroffenen Klassen. Im Standardmodus `ergaenzen` (G4 mit Bestand-Ebene) sind es nur
     ~200–300 Kollisionen. Im Modus `--baum voll` (G3/H3/H4 ohne Bestand) haben nur hero, tot und ein Teil von alt Kollision. Wer dort volle
     Baumkollision braucht, sollte `bestand_plan.py` laufen lassen (eigene Ebene, eigenes Budget) und dann `--baum ergaenzen` nutzen.
4. **Ebenen-Abgrenzung (§4):** Schicht 1 enthält nur noch **Elfenwald-Sonderformen**:
   - `wurzel`: Wurzelanlauf-Ring 0,7–2,2 m am Stamm von alt/hero/tot, radial; aus Schicht 0 hierher verschoben.
   - `efeu`: Efeu-Ring 0,35–0,6 m mit Blick zum Stamm.
   - `moosstamm` (neu): MossyTree_01, LargeFallenTree_02, Fallen/BrokenTreeAssembly als Baumleiche 2,5–6 m neben stehendem Totholz (0,5 je tot,
     0,2 je hero, 0,02 je Altbaum), radial ausgerichtet, mit Kollision.
   - `blume_lichtung`: Lichtungsblumen-Inseln.

   Die generischen Klassen `strauch, jungbaum, farn, totholz_liegend/stumpf/ast, hochstaude, grasbueschel, beere, pilz` (bisher farn,
   adlerfarn, jungbaum, strauch, beere, stamm_liegend, stumpf, grasbueschel, grashorst, hochstaude, ast, pilz) setzt der Planer **nie mehr**,
   auch nicht mit `--mittel voll`. Dafür sorgt die Liste `ebenen.generisch_mittelschicht` samt Alias im Code; eine Klasse dieses Namens in der
   Regeldatei wird mit Hinweis übersprungen. `--mittel` bleibt als Schalter erhalten, `voll` verhält sich wie `zusatz` und schreibt einen Hinweis.
   Der Abschnitt `teil_d` (zusatz_faktor) ist durch `mittelschicht_overrides` ersetzt. `felsgruppen_overrides` hat zusätzlich
   **`"mindestdichte_je_ha": 1.0`** (`mindestdichte_klassen`: fels_block, fels_stein; Moosfelsen auch im flachen Wald, wo `nur_wo` nicht
   greift). `spuren_overrides` bleibt bis auf den Elfenpfad-Text gleich.
5. **ASCII (§5):** Alle Ausgaben laufen über `meld()`/`fehler()`. Beide wandeln Umlaute in ae/oe/ue/ss um, → in ->, ≤ in <=, – in -, × in x,
   ° in „ Grad“, und alles Übrige in „?“. Auch die `hinweise` und Blickziel-Regeln im `plan.json` sind ASCII. Fehlende Pflichtdateien
   (hoehe.f32, Regeldatei, `netze.csv`, Weltordner) und ein unbekanntes Feld führen zu einer Meldung auf stderr und **Exit-Code 2**.
   `netze.csv` wird jetzt auch unter `vorlagen/daten/` neben dem Skript gesucht.

### Override-Schema `mittelschicht_overrides` (für `mittelschicht_plan.py`, Teil D)

```
"mittelschicht_overrides": {
  "biom": "elfenwald",
  "klassen_alias": {"totholz_liegend": "totholz", "totholz_stumpf": "stumpf", "totholz_ast": "ast"},   # Namen in mittelschicht_regeln.json
  "palette":  {"farn": [12 Pfade], "strauch": [14], "jungbaum": [12], "totholz_liegend": [13], "totholz_stumpf": [6],
               "totholz_ast": [8], "hochstaude": [2], "grasbueschel": [8], "beere": [3], "pilz": [2]},          # ersetzt die Teil-D-Palette
  "faktor":   {"farn": 1.5, "strauch": 0.5, "jungbaum": 1.0, "totholz_liegend": 1.0, "totholz_stumpf": 1.0, "totholz_ast": 0.35,
               "hochstaude": 0.5, "grasbueschel": 1.0, "beere": 1.0, "pilz": 0.3, "adlerfarn": 1.0, "grashorst": 1.0,
               "wurzel": 0.0, "kletter": 0.0, "totbaum": 0.0},                                                 # x Teil-D-Dichte
  "parameter": {"farn": {"gruppe": [6, 18], "radius_m": 3.5, "mulde": 1.4, "lagen_faktor": {"Moos": 1.6, ...}, ...},   # optional
                "jungbaum": {"lichtungsrand": 4.0, "saum": 3.0, ...}, "pilz": {"an_totholz": 4.0, ...}, ...},
  "zusatzklassen": {"beere": {...}, "adlerfarn": {...}, "grashorst": {...}},     # volle Klassendefinition im mittelschicht-Format
  "faktor_begruendung": {...}, "entfernen_witcher_vorschlag": [27 Witcher-Praefixe der generischen Mittelschicht]
}
```

Regeln für Teil D: Die Overrides gewinnen gegen `mittelschicht_regeln.json["biome"]["elfenwald"]`. `faktor` multipliziert die Teil-D-Dichte
der Klasse; 0 heißt „Klasse im Elfenwald aus“. Das gilt für `wurzel`, `kletter` und `totbaum`: Wurzel- und Efeu-Ring setzt der
Elfenwald-Planer, stehendes Totholz kommt aus der Baumschicht. `zusatzklassen` sind Klassen, die Teil D im Elfenwald nicht hat (Heidelbeere,
Adlerfarn am Lichtungsrand, Moos-Grashorst); `faktor` gilt auch für sie. Die **Farninseln** sind jetzt `faktor.farn` = 1,5 plus
`parameter.farn` (Gruppen 6–18 im Radius 3,5 m, Mulde ×1,4, Moos ×1,6) statt eines eigenen Elfenwald-Farns ×0,45 obendrauf. Die Faktoren
sind aus dem Verhältnis der bisherigen Elfenwald-Dichten zu den Teil-D-Dichten im Schatten (Beschattung 0,8–0,9) abgeleitet;
`faktor_begruendung` nennt die Werte je Klasse. Die Witcher-Präfixe der generischen Klassen (Farne, Holunder, Hasel, Stümpfe, liegende
Stämme, Äste, Gras) entfernt der Elfenwald-Planer nicht mehr. Sie stehen als Vorschlag für den `entfernen`-Filter von Teil D in
`entfernen_witcher_vorschlag`, Felsblöcke analog in `felsgruppen_overrides.entfernen_witcher_vorschlag`.

### Rauchtest Runde 1 (Cloud, synthetisch; Raster danach gelöscht)

Die Raster wurden neu erzeugt, in voller Größe 7 057 × 9 577 (memmap, nur die Fenster beschrieben):

- **G4:** elfenwald 68 % / heide 21 % / Kennzahl 0 → aue 11 % im Fenster (im Feld 74 / 21 / 5 %), Bach, Teich, Weg, Ort, `lage_Laub/Moos/Gras`.
  Die **Bestand-Ebene hat 17 000 Bäume** (Echtdaten-Größenordnung) in Gruppen 8–40 m mit drei Lichtungen. Die Witcher-Ebene hat 300 Farne,
  120 Laub und 50 Moosstämme.
- **I4 (Mischfeld):** elfenwald-Streifen West 21 % des Feldes, bergwald, eine aue-Ecke, keine Bestand-Ebene.
- **C6 (Fremdbiom):** Rezept „Vulkanregion“ 97 % + bergwald 3 %.

Umgebung: Python 3.13.16, NumPy 2.5.3, ohne numba, 4 Kerne, Aufruf `python -I -X utf8`.

| Lauf | Instanzen | Boden / Mittel / Baum / Wasserkante | Kollision | in eigenen Zellen / Saum / fremd (> 31 m) | Laufzeit |
|---|---|---|---|---|---|
| G4, **alte Fassung** (Kalibrierung) | 61 623 | 39 428 / 21 003 / 19 / 1 173 | 19 (+0) | – | 13,0 s |
| **G4 Standard** (ergaenzen) | **31 023** | 21 787 / 8 085 / 19 / 1 132 | **215** | 30 012 / 1 011 / **0** | 12,6 s |
| G4 `--mittel voll` | 31 023 (MD5 gleich) | wie Standard, Hinweis „wirkungslos“ | 215 | wie Standard | 12,6 s |
| G4 `--baum voll` | 44 296 | 28 279 / 3 855 / 11 061 / 1 101 | **3 000** (23 Netze; 14 Netze / 5 562 Bäume ohne) | 42 868 / 1 428 / 0 | 11,3 s |
| G4 `--faktor 2.5` (Überlauf) | 74 215 → **51 980** | Laub ×0,40, Zweige ×0,39, Kraut ×0,85 | 258 | – | 12,6 s |
| **I4 Mischfeld** (voll) | 13 979 | 9 076 / 1 083 / 3 567 / 253 | 2 800 | 13 177 / 802 / **0** | 10,8 s |
| **C6 Fremdbiom** | **0 (Leerplan)** | – | 0 | – | < 1 s |
| G4 ohne `eigner.r8` (Fallback biome_je_feld → elfenwald) | 40 543 | 28 172 / 11 146 / 26 / 1 199 | 271 | 100 % zuständig | 12,2 s |
| C6 ohne `eigner.r8` (Fallback → lava) | 0 (Leerplan) | – | 0 | – | < 1 s |

Einzelheiten zu den Läufen:

- **G4 Standard je Klasse:** Laub 8 284 (vorher 14 798, −44 %), Zweige 5 474 (9 401, −42 %), Moos 3 439, Kraut 3 635, Kleinsteine 955;
  Wurzel 2 559, Efeu 492, Moos-Stamm 196, Lichtungsblumen 4 838; Bäume: hero 14, tot 5. Farn, Adlerfarn, Beere, Grashorst, Pilz und Ast
  (vorher zusammen 15 121) setzt jetzt Teil D.
- **Plan-Schlüssel G4:** `biome_fenster` {elfenwald 0,681, heide 0,213, aue 0,106}, `zellen_zustaendig` 785 621.
- **Plan-Schlüssel I4:** `biome_fenster` {bergwald 0,708, elfenwald 0,243, aue 0,049}, `zellen_zustaendig` 242 928.
- **Plan-Schlüssel C6:** `biome_fenster` {lava 0,917, bergwald 0,083}, `zellen_zustaendig` 0, `instanzen` 0, 0 f32.
- **Saum-Abfall** (Instanzen je m², Distanz in 4er-Nachbarschaft):

  | | innen | 1–6 m | 6–12 m | 12–18 m | 18–24 m | 24–31 m | > 31 m |
  |---|---|---|---|---|---|---|---|
  | G4 | 0,0403 | 0,0307 | 0,0269 | 0,0204 | 0,0095 | 0,0045 | 0 |
  | I4 | 0,0619 | 0,0475 | 0,0454 | 0,0261 | 0,0179 | 0,0037 | 0 |

Weitere Prüfungen, alle bestanden:

- **Schlüssel und Budget:** Alle Pflichtschlüssel sind vorhanden, auch im Leerplan, und Σ `biome_fenster` = 1,000. Jede f32 ist durch 10
  teilbar, die Anzahl stimmt mit `plan.json` überein, und `kollision_anzahl` = Σ Kollisionsdateien. In keinem Lauf mehr als 60 000 Instanzen
  oder 3 000 Kollisionen, keine generische Mittelschicht-Klasse in der Ausgabe.
- **Geometrie:** |q| − 1 ≤ 1,2·10⁻⁷. 0 Instanzen auf Wasser, Weg oder Ort, 0 außerhalb des Feldes; z − Gelände −0,32 bis +0,19 m.
- **Determinismus:** Zwei Läufe sind byte-identisch (G4: MD5 aller f32 `d749b884…`, `plan.json` ohne `stand`/`laufzeit_s` `9b98dd30…`;
  I4: `f96c3295…`).
- **ASCII:** Alle Logs (G4, `--mittel voll`, `--baum voll`, Überlauf, I4, C6, Fehlertexte) haben 0 Nicht-ASCII-Bytes.
- **Exit-Code 2:** bei Feld `K9`, fehlender `hoehe.f32`, fehlender `netze.csv` und fehlender Regeldatei, jeweils mit einzeiliger Meldung.
- **Inventar:** 1 435 Netze, 0 fehlen (inklusive Override-Paletten). `py_compile` ok.

### Erwartete Zahlen mit Echtdaten (ersetzt die Tabelle in §5)

Die alte Fassung ergab auf der neuen G4-Synthetik 61 623 Instanzen, echt 86 811, also einen Faktor Echtdaten zu Synthetik von ≈ 1,41 (mehr
Wasser, Laub-Lage und Saum als in der Synthetik). Neue Fassung, Standardmodus:

| Feld | Biom-Anteil (biome_je_feld) | Erwartung neu | Kollision | Anmerkung |
|---|---|---|---|---|
| **G4** | elfenwald 76 / heide 22 / aue 3 | **≈ 44 000** (Spanne 38 000–50 000) | 200–400 | 31 023 × 1,41; Deckel 60 000 nicht erreicht, Ausdünnung erst ab 52 000 |
| G3, H3, H4 (`voll`, keine Bestand-Ebene) | 97–100 / 82 | 45 000–52 000 (Ausdünnung greift ggf.) | 3 000 | Baumschicht 9 000–15 000, kleinere Baumklassen ohne Kollision |
| I4 | elfenwald 21 | 10 000–18 000 | ≤ 3 000 | nur elfenwald-Streifen + 30 m |
| H2 | elfenwald 20, Land 39 | 4 000–10 000 | ≤ 2 000 | |
| G2 | elfenwald 20, Land 4 | 0–1 500 | < 200 | |
| **A5** | kueste 75 / bergwald 14 / aue 11 | **0 (Leerplan)** | 0 | vorher 2 152 |
| **C6** | lava 99 | **0 (Leerplan)** | 0 | vorher 5 875 |
| E1 | gletscher 100 | 0 (Leerplan) | 0 | unverändert 0 |

Falls ein Feld lokal doch über 52 000 liegt, steht im Log `WARNUNG: … Budget … ausgeduennt` und im `plan.json` unter `budget.ausduennung`.
Dann sollte die Dichte von Laub und Zweigen in der Regeldatei weiter gesenkt werden, statt sie ausdünnen zu lassen. Offen bleiben die Seite
von Teil D, das `mittelschicht_overrides` (palette, faktor, parameter, zusatzklassen, klassen_alias) lesen muss, und Teil C, das
`mindestdichte_je_ha` lesen muss. Die Abgrenzung gehört außerdem in `verteilung-STATUS.md`; diese Datei ist nicht Teil von B5.

---

## 1. Witcher-Analyse: Waldpfad, Laubwälder von Velen/Toussaint, Elfenruinen

**witcher_03 (Waldpfad, Kovir-Techdemo).** Das Bild ist zu etwa 60 % mit Objekten zwischen 0,3 und 3 m Höhe gefüllt, obwohl es ein
„Baumbild“ ist: rechts ein Fichtenast als Vordergrund (1–2 m vor der Kamera), links ein liegender Stamm und ein Wurzelteller, am Hangfuß
drei junge Fichten (1,5–3 m) und ein Felsblock-Trio (0,8–2 m), dazwischen Kopfsteine 10–40 cm, Grasbüschel und Schneereste in den Rinnen.
Die Bäume stehen in zwei Höhenklassen (Hero-Fichten 25–30 m im Mittelgrund, 8–12 m am Hang), der Pfad selbst ist nackter Boden mit
Kieseln, keine Textur ohne Objekt. Auf 10 m um die Kamera stehen geschätzt **4–5 Objekte je 100 m²** in der Mittelschicht (Zählung in
`verteilung-leere-fuellen.md` §1). Das ist die Messlatte: **kein Blick ohne Objekt in 0,5–3 m innerhalb 10 m.**

**Velen/Toussaint (W3 Next-Gen).** Belegbar nur indirekt: Velens Wälder sind Mischbestände verschiedenen Alters mit Kronenlücken, in denen
Jungwuchs und blühende Sträucher stehen, Vorbild Białowieża **[Suchauszug Kotaku]**; Kräuter wurden nach ihren natürlichen Standortansprüchen
gesetzt **[Suchauszug VICE]**; Toussaint-Laubwälder sind SpeedTree-Bestände mit zusätzlichen Arten **[Suchauszug SpeedTree]**; das REDkit-
Vegetation-Edit-Tool platziert per Pinsel je Geländetyp, nennt aber keine Dichten. Es bleibt die Bildauswertung (`bildkritik-witcher-messlatte.md`
Rang 4): 2–3 Arten, Höhenvarianz 0,7–1,3, Clumping mit 15–25 % Lichtungen, Waldkanten-Falloff 30–60 m, Totholz 2–3 %, Farbinseln.

**Elfenruinen (Aen Seidhe).** Elfenarchitektur ist „elegant, organisch, asymmetrisch“, Bauten „verschmelzen mit der Umgebung“, Ornamente mit
Ranken- und Baummotiven **[Suchauszug historicalgames.net]**; Beispiele Termes, Arthach, Ruinen am Wyndamer-See **[Suchauszug Witcher-Wiki]**.
Spielerisch immer Blickziel plus Kleinraum: Säulenreihe oder Bogen auf Kuppe/Hangschulter, halb im Boden, Efeu, Moos am Fuß, Bruchsteine
(ein Modder-Breakdown nennt genau diese Moos-/Rissstein-Schichten als das, was den Spielruinen fehlte **[Suchauszug Patreon BetterRuins]**).
Kein Zaun, kein Karren: der Elfenwald ist unbewohnt, seine Spuren sind Ruine, Schrein, Steinmann, Hügelgrab.

**Witcher-4-Techdemo (Kovir).** Nanite Foliage mit modellierten Blättern und voxelisierten Kronen, 60 fps auf PS5 **[Suchauszug PlayStation
Blog, Game Informer]** – keine Dichtezahlen; Grenze ist bei uns der Setzer (60 000 je Ebene), nicht die GPU.

**Botanik als Zahlenquelle (für Lückenanteil und Jungwuchs).** Urwald-Buchenbestände haben Lückenanteile von 3–11 % der Fläche (Slowenien,
Kopa 3,2→4,5 %, Gorjanci 9,1→10,6 %) **[Suchauszug PLOS ONE 2013]**; in Karpaten-Tannen-Buchen-Urwäldern 11,3 % Lücken bzw. 37,9 % erweiterte
Lücken **[Suchauszug Springer]**; Jungwuchs keimt bevorzugt an Lückenrändern und unter halbgeschlossenem Dach, nicht in der Lückenmitte
**[Suchauszug Oxford Forestry]**; Totholz 115 m³/ha im Urwald Sitno **[Suchauszug MDPI Forests]**. Daraus: Lichtungsziel 15–25 % (Spiel
liest besser als Urwald, Bildkritik), Jungbäume ×3–4 am Lichtungsrand, Farn/Moos/Pilze mit Beschattung steigend.

**Was heute in G3/G4 fehlt (Ist-Bilder).** `KLEIN12_G3_boden`: braune Laubtextur, gleich große Sprösslinge, ein roter Strauch, eine
aufliegende Platte ohne Laubkante; keine Zweige, Äste, Wurzelanläufe, Farne, Moospolster, Pilze; Buchenstämme ohne Fuß. `W6FIN_G3_rundgang`:
eine Art, eine Höhe, harte Waldkante, keine Lichtungen, roter Boden zwischen den Kronen. Der Elfenwald-Planer liefert genau die fehlenden
Stufen (Schichten 0 und 1, Bachsaum) und – wo keine Bestand-Ebene liegt – einen Altersmix-Bestand mit Lichtungen.

**Quellen (6 WebSearch-Läufe, nur Suchauszüge):** Kotaku „There's Real History, And Beauty, In The Witcher 3's Forests“ · VICE „Designing the
World of The Witcher 3“ · SpeedTree „The Witcher 3: Blood and Wine“ · REDkit-Wiki „Tools“ (Vegetation Edit Tool) · historicalgames.net
„Echoing the Past: Spoliation, Memory, and Power in the Witcher 3“ · Witcher-Wiki „Elven Sanctuary Ruins“, „Elven ruins near Lake Wyndamer“ ·
Patreon „Elven ruins from The Witcher 3 – Build Breakdown“ · PlayStation Blog / CDPR / Game Informer zur W4-Techdemo (2025) · PLOS ONE
10.1371/journal.pone.0052641 (Gap Dynamics Slovenia) · Springer 10.1007/s10342-009-0322-2 (Carpathian gaps) · Forestry 80(4):431 (Gap
regeneration) · MDPI Forests 11(1):81 (Sitno deadwood). Keine Quelle nennt Instanzen je m²; alle Dichten unten sind Richtwerte aus den
Zielbildern und dem Teil-D-Befund.

---

## 2. Regelwerk (`elfenwald_regeln.json`) – je Schicht mit Zahlen

Dichten sind Instanzen je m² als Paar **[offen, voll beschattet]**, linear über die Beschattung interpoliert. Beschattung = 1 − exp(−1,4 ·
π·5² · Kronendichte), Kronendichte = Baumpositionen (Gewicht Maßstab²) mit Gauß σ = 6 m geglättet (wie Teil D, k 1,4 statt 1,6: Hainbuche/
Buche sind dichter als Kiefer, die Schwelle greift früher). Wald = Beschattung > 0,35; Lichtung = Beschattung < 0,18 innerhalb 40 m der
Waldkante; Saum 15 m nach innen / 10 m nach außen; Lichtungsrand = Lichtungszellen ≤ 8 m zur Kante. Feuchte = 0,8·(1 − d_Wasser/30 m) +
0,7·Moos + 1,0·Schlamm + 1,0·Algen + 0,3·Lehm + 0,15·Erde (0–1). Hang voll bis 22°, dann linear 0 bis `hang_max` je Klasse. Mulde =
Laplace der 4-m-geglätteten Höhe > 0,015 (Senken bekommen Laub ×1,8, Farn ×1,4, Moos ×1,3, Pilze ×1,5). Wegrand 2,5–8 m: Blumen ×2,
Farn ×1,4, Hochstauden ×1,8, Laub ×0,6 (Elfenpfad: Blüten statt Kies). Sperrflächen: Wasser (+0,5 m), Weg 2,5 m Kleinzeug / 4 m Große,
Ort 5 m, vorhandene Nicht-Baum-Instanzen 1,2 m, Baumstämme 1 m; neue Bäume 6 m von Bestand-Bäumen.

### Schicht 2 Baum (Modus `auto`: `ergaenzen` wenn `bestand/<Feld>/plan.json` existiert, sonst `voll`)

| Klasse | Netze | Dichte je m² | Jitter-Raster | Maßstab | Kippen | Eingraben | Besonderes |
|---|---|---|---|---|---|---|---|
| hero | Hornbeam_Field_01/02, beech_tree_06/07 | 0,00003 | 40 m | 1,25–1,55 | 0 | 25 cm | nur Lichtungsrand ×12, Saum ×6, Abstand 10 m, Kollision |
| alt | Hornbeam_Field_03/04, Forest_01/02/04, beech_tree_04/05/08/09 | 0,0062 | 7 m | 0,95–1,25 | 0,05 | 20 cm | Fels ×0,3, Abstand 3 m, Kollision |
| mittel | Hornbeam_Forest_03/05–08, beech_tree_02/03 | 0,0090 | 5 m | 0,85–1,12 | 0,05 | 15 cm | Lichtungsrand ×1,2, Abstand 2,2 m, Kollision |
| jung | Hornbeam_Forest_09/10, beech_tree_00_C/D, 01 | 0,006 / 0,0018 | 3,5 m | 0,7–1,05 | 0,08 | 8 cm | Lichtungsrand ×3, Saum ×2,5, ohne Kollision |
| pappel | Poplar_06/07_Forest, 03_Medium, 04_Small | 0,0012 / 0,0005 | 9 m | 0,85–1,15 | 0,03 | 20 cm | Feuchte 0,5→2,2, Lichtungsrand ×2,5, Fels 0 |
| birke | Big_Tree_birch_01 | 0,0008 / 0,0002 | 9 m | 0,8–1,15 | 0,05 | 12 cm | Saum ×3, Kies ×1,5 (Herbstakzent) |
| weide | Big_Tree_willow_01/02 | nur Bachband 3–14 m: 0,0025 | 10 m | 0,8–1,1 | 0,05 | 15 cm | Hang < 25° |
| tot | EuropeanBeech_Dead_XL/M, DeadTree_01/02, Graveyard Dead_Tree_01/03 | 0,0004 / 0,0005 | 12 m | 0,9–1,3 | 0,10 | 15 cm | Lichtung ×0,4, Kollision |

Klumpen: Wertrauschen (Hash der Weltkoordinate, nahtlos) mit Wellenlängen 48 m (0,65) + 16 m (0,35); Zellen < 0,34 sind Lichtung (Dichte
×0,03), darüber steigt die Dichte linear von 0,7 auf 1,6. Gruppen 8–40 m ergeben sich aus den Wellenlängen. Höhe: ab 350 m linear
abnehmend, 0 ab 600 m. Artenmix bei `voll` (Rauchtest, synthetisches G4): Hainbuche/Buche alt 31 %, mittel 37 %, jung 24 %, Pappel 3 %,
Birke 3 %, tot 1,7 %, Hero 0,5 %, Weide < 0,3 %. Bei `ergaenzen` (G4 mit `FT_EL_BST_*`) werden **nur** Hero-Altbäume (0,35/ha: ×8 am
Lichtungsrand des vorhandenen Kronendachs, ×0,5 in Lichtungen, ×0,15 im Wald) und stehendes Totholz (0,45/ha) ergänzt, 7 m Abstand zum
Bestand; erwartet 30–120 Stück je Feld.

### Schicht 1 Mittelschicht 0,3–3 m (Standard `--mittel zusatz`, siehe §4)

*Stand vor Korrektur Runde 1. Seitdem setzt Schicht 1 nur noch wurzel, efeu, moosstamm und blume_lichtung; die übrigen Klassen
stehen als `mittelschicht_overrides` in der Regeldatei (siehe Abschnitt Korrektur Runde 1).*

| Klasse | Netze (Auszug) | Dichte je m² | Gruppe / Radius | Maßstab | Steuerung | Sichtweite |
|---|---|---|---|---|---|---|
| farn (Farninsel) | Fern_01–06, SilverLadyFern_01–03, BeechFern_09/10/15 | 0,003 / 0,034 (×0,45 im Zusatz) | 6–18 / 3,5 m | 0,8–1,45 | Lichtung ×0,15, Feuchte 0,5→1,9, Moos ×1,6, Mulde ×1,4 | 300 m |
| adlerfarn | EagleFern_M_01, S_01/02/04 | 0,009 / 0,002 | 8–25 / 5 m | 0,9–1,5 | Saum ×2, Lichtungsrand ×3, Gras ×1,3 | 300 m |
| beere (Heidelbeere) | billberry_01–03 | 0,002 / 0,016 | 8–24 / 3 m | 0,9–1,4 | Lichtung ×0,2, Moos ×1,8 | 150 m |
| grashorst | GrassyEmbankment_01/02 | 0,0025 / 0,0004 | 1–3 / 1,5 m | 0,9–1,4 | Moos ×1,8, Mulde ×1,5, Feuchte 0,7→1,6 | 200 m |
| blume_lichtung | WhiteWindflower ×5, LilyOfTheValley ×3, Periwinkle ×3, YellowArchangel ×2 | 0,010 / 0,001 | 10–30 / 4 m | 0,9–1,4 | Lichtung ×2, Lichtungsrand ×2, Wegrand ×2, Hang < 30° | 120 m |
| efeu | Ivy_09–22, EnglishIvy_01/05/08 | am Stamm: 6 % der alt/hero/tot-Bäume, Ring 0,35–0,6 m | 1 | 0,9–1,4 | Yaw zum Stamm, Kippen 0 | 200 m |
| jungbaum | Hornbeam_Sapling_01–07, Seedling_01/02, beech_plant_01–03 | 0,009 / 0,003 (nur `voll`) | 2–6 / 2,5 m | 0,8–1,3 | Saum ×3, Lichtungsrand ×4, Lichtung ×0,7 | 350 m |
| strauch | Elderberry_05–12, hazel_01/02, black_cherry_02/03, maple_bush_02/03 | 0,008 / 0,002 (nur `voll`) | 1–3 / 2,5 m | 0,8–1,4 | Saum ×3, Lichtungsrand ×2,2 | 350 m |
| stamm_liegend | MossyTree_01, LargeFallenTree_01/02, OldFallenTree_01/02, FallenTreeAssembly, dead_log_01/02/04 … | 0,0008 / 0,0016 (nur `voll`) | 1 | 0,9–1,35 | längs Hang ±20°, Eingraben 12 cm, **Kollision** | 500 m |
| stumpf | TreeStump_01, RottenTreeStump_01/02, BirchTreeStump, BrokenStump, stump_03 | 0,0005 / 0,0010 (nur `voll`) | 1 | 0,85–1,4 | Eingraben 8 cm, **Kollision** | 400 m |
| grasbueschel | grass_01/02/03 (Forest), grass_clover_01 | 0,025 / 0,003 (nur `voll`) | 3–9 / 2 m | 0,8–1,5 | Gras/Wiese ×2, Lichtung ×1,5 | 150 m |
| hochstaude | nettle_01_0/1 | 0,008 / 0,002 (nur `voll`) | 4–12 / 2,5 m | 0,9–1,4 | Saum ×2,5, Feuchte 0,5→2,0, Erde/Lehm ×1,6 | 150 m |

### Schicht 0 Boden

| Klasse | Netze | Dichte je m² | Gruppe / Radius | Steuerung | Sichtweite |
|---|---|---|---|---|---|
| laubhaufen | DeadLeaves_01/05/12/13/14, poplar_leaves_01/02, detail_leaves_01/03 | 0,006 / 0,024 | 3–8 / 2 m | Laub ×1,6, Mulde ×1,8, nah Baum (3 m) ×1,4, Lichtung ×0,4 | 60 m |
| zweige | WoodenSticksAndTwigs_01–09 (7), DryBranches_01/04/05/07 | 0,004 / 0,014 | 2–5 / 1,5 m | Laub ×1,3, nah Baum ×2 | 70 m |
| ast | OldTreeBranch_01/04/05, BrokenTreeBranch_01, OakBranch_01, branch_01_1/2, detail_branches_02 | 0,0012 / 0,0035 (nur `voll`) | 1 | Laub ×1,2, nah Baum ×1,6 | 120 m |
| pilz | mushroom_01/02 | 0,0002 / 0,003 (×0,4 im Zusatz) | 3–9 / 0,9 m | an Totholz ×4, Moos ×1,6, Feuchte 0,5→2,2, Lichtung ×0,1 | 60 m |
| wurzel (Wurzelanlauf) | beech_old_roots_01, MossyForestRoots_01–03, ForestRoots_01/02, crooked_root_01 | 30 % der alt/hero/tot-Bäume, max 2, Ring 0,7–2,2 m | 1 | Yaw radial vom Stamm, Kippen 0,8, Eingraben 6 cm | 150 m |
| moos | CustomMoss_01–05, moss_01/02 | 0,003 / 0,020 | 4–12 / 1,5 m | Moos ×2,5, Fels ×1,4, an Totholz ×3, Feuchte 0,6→1,8, Hang bis 45° | 50 m |
| kraut (Sauerklee/Klee) | Violet_Wood_Sorrel VarA/B/D/F/H, CloverVarieties_01–03 | 0,004 / 0,016 | 6–16 / 2 m | Moos ×1,3, Wegrand ×1,3, Feuchte 0,7→1,6 | 70 m |
| stein_klein | MossyForestRock_01, SmallStonesPack_01/03/05/07, stone_03/04/06 | 0,0015 / 0,003 | 2–6 / 1,2 m | Kies/Fels/Geröll ×2,5–3, Hang bis 45°, Eingraben 4 cm, Kippen 1,0 | 80 m |

### Schicht 5 Wasserkante (Bachsaum; Fluss/See ×0,3, dort bleibt `FT_EL_UF_*` führend)

Bach = Wasserzellen, deren lokale Halbbreite (Distanz zum Nichtwasser, Maximum im Umkreis 8 m) ≤ 4 m ist. Band 0,5–6 m vom Wasser, Dichte
fällt linear vom Innen- zum Außenwert: moosstein_bach (MossyForestRock_01–03, MossyRocks_01/02, MossyForestBoulder_02/05/06/07,
LichenedForestBoulder_01) 0,08→0,015, Gruppen 2–5, Maßstab 0,6–1,4, Eingraben 18 cm, Kippen 1,0; embankment (MossyEmbankment_01/02,
ForestRockShelf_01) 0,012→0,002 nur bei Hang 18–60°, Eingraben 30 cm; farn_ufer 0,06→0,012 (0,8–6 m); schachtelhalm (rough_horsetail_01–03)
0,05→0,004 (0,5–3,5 m, Schlamm ×1,8); binse (ToadRush_00/01/02/012) 0,03→0,002 (0,5–2,5 m, Hang < 20°); moos_ufer 0,08→0,01 (0,5–3,5 m).
Alles ohne Kollision, Sichtweiten 50–300 m.

### Budget und Priorität

*Überholt durch Korrektur Runde 1: Deckel 60 000 je Feld, Ziel 45 000–52 000, Kollision ≤ 3 000 einschließlich Bäume.*

Ziel je Schicht: Boden 52 000, Mittel 48 000, Baum 22 000, Wasserkante 15 000 (Obergrenzen 60 000 / 20 000). Bei Überschreitung dünnt der
Planer die Klassen von hinten in der Prioritätsliste (Boden: wurzel > ast > stein > pilz > zweige > kraut > moos > laubhaufen; Mittel:
stamm > stumpf > strauch > jungbaum > farn > adlerfarn > efeu > hochstaude > beere > blume > grashorst > grasbueschel) mit einem
gemeinsamen Hash-Faktor, bis das Ziel erreicht ist. Kollision: Schichten 1/5 (liegende Stämme, Stümpfe) ≤ 3 000 je Feld; die Baumschicht
hat ein eigenes Budget `kollision_baum_je_feld` = 20 000 (wie die Bestand-Ebene mit 17 000 Bäumen in G4 – Bäume ohne Kollision sind kein
Spiel). Setzt man es auf 3 000, bekommen nur hero/tot/alt Kollision (Reihenfolge der Prioritätsliste), die übrigen Klassen `kollision:false`.

---

## 3. Overrides für Teil C und Teil D (nur JSON, keine Instanzen aus diesem Planer)

**Moosfelsen (`felsgruppen_overrides`, für `felsgruppen_plan.py`).** Felsen im Elfenwald sind bemooste Granit-/Gneisblöcke im Laubwald,
keine Wände, keine Schuttfächer (Ausnahme H3/H4, Fels-Lagen > 25 %). Palette: Hero `Mossy_Rock_Formation_plFhY`, `MossyForestBoulder_04`,
`TundraMossyBoulder_01`; Block 11 Moos-/Forest-Boulder (Megascans + Fab); Stein `MossyForestRock_01/02`; Platten `MossyRocks`, `ForestRockSlab/
Shelf/Formation`, `MossyEmbankment`; Schale nur `HugeMossyForestCliff_01`. Gruppendichte ×0,7; nur Hang ≥ 12°, Kuppe oder Bach-Prallhang, keine
Mulden ohne Wand. Gruppe = 1 Hauptfels + 2–5 Nebenblöcke + 4–10 Schutt + 10–30 Kiesel, Hauptrichtung ±15°, Eingraben 35–50 % (weicher
Waldboden), Kippen voll in den Hang. Kontaktzone: Geröllsaum 0,6/m² im Ring 0,5–2 m, Farnring 2–6 nur Schattseite, Moos am Fuß 4–10,
RVT-Fußblend 30–60 cm, Auflage Moos 0,85 / Flechte 0,2. Abstand zu Bäumen 2,5 m; Budget 120 Akteure + 6 000 Foliage je Feld.

**Ruinen/Schreine (`spuren_overrides`, für `spuren_plan.py`).** Aus: Zaun, Feldstreifen, Obstgarten, Karren, Holzschlag, Köhler, Rauch, Steg,
Mauer. **Ruine** 1–3 Gruppen je Feld à 3–8 Stücke (Radius 6–18 m) auf Kuppe/Hangschulter < 12°, 20–80 m vom Weg, nicht im Ort (+30 m), ≥ 10 m
vom Wasser, Beschattung 0,3–0,7; Foliage `SM_Column_02/03`, `SM_Wall_02`; Akteure `SM_Main_Arch_01` (529 640 Dreiecke, ≤ 1 je Feld) und
`SM_Wall_01` (372 163, ≤ 2); Eingraben 15–35 %, Kippen 2–8°, Hauptrichtung ±12°, Säulenreihe 3–4 m; Bewuchs Efeu an 40 % der Wände, Moos
6–12, Farn 2–5, Bruchsteine 3–8 je Stück. **Schrein** 1–2 je Feld: `SM_Sviatovid_Stone` an Wegkreuzung/Bachquerung, 2–4 m neben dem Weg,
unter Altbaum oder vor Hero-Fels, 6–12 Kiesel + 8–16 Blumen; `SM_Cross` (christlich) nicht. **Steinmann** 2–6 je Feld an Wegen, 4–7 Steine.
**Hügelgrab/Steinkreis** 0–1 je Feld in der Lichtungsmitte (Hang < 6°, ≥ 40 m vom Weg), 7–12 Moosblöcke, Blumeninsel innen ×3. Standorte
liefert der Elfenwald-Planer als `blickziele` in `plan.json` (größte Lichtung mit Radius, Kuppe nahe Weg, Bachquerung) – Rauchtest: Lichtung
r = 36 m bei X 1 391 / Y −863 m, Schrein an der Bachquerung X 1 734 / Y −548 m.

---

## 4. Abgrenzung zu vorhandenen Ebenen

**`FT_EL_BST_*` (Bestand, G4 gesetzt, 17 000 Bäume).** Bleibt. Der Planer erkennt `bestand/G4/plan.json`, liest alle Baumpositionen
(Feld + 8 Nachbarn, nur im Fenster) für das Kronendach, hält 6–7 m Abstand und ergänzt nur Hero-Altbäume und stehendes Totholz (§2).
In G3/H3/H4/I4/H2/G2 (keine Bestand-Ebene) liefert er den Bestand selbst (`voll`) und setzt dann `entfernen` auch für Witcher-Haine
(`sm_europeanhornbeam_field_0`, `sm_beech_tree_0`, …) – nur für Präfixe, die laut `witcher/<Feld>/plan.json` dort wirklich vorkommen.
Will man G4 ebenfalls vom Elfenwald-Planer bestücken: `--baum voll` setzt `entfernen` für die Bestand-Netze (Rauchtest: 13 519 Bäume,
Lichtungsanteil 19 %, Beschattung 0,67).

**`FT_EL_WIT_*` (Witcher-Bewuchs).** Die Witcher-Ebene streut im Elfenwald generische Farne, Laub, Zweige, Gebüsch, Totholz, Blumen und
Namaqualand-Netze ohne Beschattungs-, Saum- und Feuchte-Regel. Alle Nicht-Baum-Rollen, die der Elfenwald neu setzt, kommen in den
`entfernen`-Filter (57 Präfixe in der JSON; wirksam nur die im Feld vorhandenen – Rauchtest G4: `sm_fern_0,sm_mossytree_01`). Die
Witcher-Haine bleiben, solange der Planer selbst keine Bäume liefert.

**Teil-D-Mittelschicht (`mittelschicht_plan.py`, `FT_EL_MS_*`).** Teil D liefert im Elfenwald bereits farn 0,006/0,022, strauch 0,014/0,005,
jungbaum 0,010/0,003, hochstaude 0,008/0,010, grasbueschel 0,012/0,002, totholz 0,0006/0,0022, stumpf, ast 0,004/0,010, wurzel, pilz
0,002/0,010, kletter, totbaum. Damit nichts doppelt steht, läuft der Elfenwald-Planer standardmäßig mit **`--mittel zusatz`**: Klassen
strauch, jungbaum, hochstaude, grasbueschel, stamm_liegend, stumpf und ast entfallen (Faktor 0 in `teil_d.zusatz_faktor`), farn ×0,45 und
pilz ×0,4 bleiben als Verdichtung. Der elfenwaldspezifische Zusatz ist: **Farninseln** (6–18 Stück, Radius 3,5 m, nur Schatten/Mulde/
Feuchte – Teil D streut Farn gleichmäßig), **Adlerfarn** am Lichtungsrand, **Heidelbeere** (Teil D: „–“), **Grashorste**, **Lichtungsblumen-
Inseln**, **Efeu und Wurzelanlauf am Stamm** (Teil D streut Efeu/Wurzeln frei), dazu die komplette Bodenschicht (Laub, Zweige, Moos,
Sauerklee, Kleinsteine) und der Bachsaum, die Teil D nicht hat. `--mittel voll` nur, wenn `mittelschicht_plan.py` in den Elfenwald-Feldern
nicht läuft. Rauchtest-Differenz (dichter Synthetik-Bestand): Mittelschicht 24 839 (zusatz) gegen 48 019 nach Budget (voll, 68 388 vor
Ausdünnung).

**`FT_EL_UF_*` (Ufer, 5 Felder)** bleibt an Fluss/See führend (Wasserkante ×0,3); am Bach (Halbbreite ≤ 4 m) setzt der Elfenwald den
Saum voll. **Felsschalen/Klippen** werden nicht berührt (Fels ist Teil C).

---

## 5. Testanleitung

**Rauchtest Cloud (gelaufen).** Synthetische production-Wurzel: `hoehe.f32` in voller Größe 7 057 × 9 577 (memmap, nur das G4-Fenster + 64 m
beschrieben: Relief 15–45 m, Bachtal, Kuppe NW, Gefälle nach Osten), `karte_wasser.r8` (Bach 3–5 m breit, Teich 60 × 90 m), `karte_weg.r8`
(Weg N–S, kreuzt den Bach), `karte_ort.r8`, `eigner.r8` + `welt.json` (Kachel 7 elfenwald, 9 heide in der SO-Ecke, 0 im Norden),
`lage_Laub/Moos/Gras.r8`, `bestand/G4` (1 938 bzw. 11 064 Bäume in Gruppen 12–28 m mit drei Lichtungen 38–60 m), `witcher/G4`
(300 Farne + 50 Moosstämme), `daten/netze.csv`. Python 3.13, NumPy 2.5, ohne numba, 4 Kerne.

| Lauf | Instanzen gesamt | Boden | Mittel | Baum | Wasserkante | Kollision Baum / andere | Netze | Laufzeit |
|---|---|---|---|---|---|---|---|---|
| G4, 1 938 Bäume, Standard (ergaenzen + zusatz) | 40 846 | 16 494 | 23 100 | 34 | 1 218 | 34 / 0 | 123 | 12,6 s |
| G4, 1 938 Bäume, `--mittel voll` | 67 348 | 17 967 | 48 129 (Ziel greift, ×0,52) | 34 | 1 218 | 34 / 1 144 | 186 | 13,1 s |
| G4, 11 064 Bäume, Standard | 60 824 | 34 818 | 24 839 | 43 | 1 124 | 43 / 0 | 122 | 13,5 s |
| G4, 11 064 Bäume, `--mittel voll` | 87 229 | 38 043 | 48 019 (×0,51) | 43 | 1 124 | 43 / 1 519 | 185 | 13,7 s |
| G4, `--baum voll` (eigener Bestand) | 88 092 | 52 014 (Ziel, Laub ×0,91) | 21 496 | 13 519 | 1 063 | 10 324 / 0 | 151 | 10,9 s |
| G3 (Synthetik: nur 64 m Land am Südrand, keine Bestand-Ebene → `voll`) | 5 069 | 2 815 | 1 577 | 677 | 0 (kein Wasser, Hinweis) | 474 / 0 | – | 7,5 s |

Prüfskript (alle Läufe): jede f32 durch 10 teilbar, Anzahl = `plan.json`, Quaternionen normiert (|q| − 1 ≤ 1,1·10⁻⁷), Schema je Datei
(`pfad, anzahl, gruppe, rolle, ebene, sichtweite, schatten, kollision`) vollständig, **0 Instanzen auf Wasser/Weg/Ort, 0 außerhalb des
Feldes** (nach Korrektur: Feldgrenze jetzt auf der Gleitkomma-Koordinate, vorher 40 Instanzen bis 0,5 m außerhalb), z − Gelände −0,31 m
(Moossteine 18 cm, Böschungen 30 cm eingegraben) bis +0,23 m (Bilinear-Vergleichsartefakt am Bachhang), Maßstab 0,53–2,20 (Pilze bis
Moospolster), zwei Läufe byte-identisch (MD5 `44d47005…`). **Farninseln folgen der Beschattung:** Feldmittel 0,41 (dicht) – an
Farn-Instanzen 0,59, Heidelbeere 0,60, Moos 0,60, Laub 0,57; Lichtungsblumen 0,23, Adlerfarn 0,31 (Lichtungsrand). Im dünnen Bestand
(Mittel 0,09): Farn 0,33, Blumen 0,07. Fehlerpfade: Feld `K9`, fehlende Basis, fehlende Regeldatei → klare Meldung, Exit; fehlende
`lage_*`/Karten → Hinweis je Datei, Lauf geht weiter; fehlende Netzpfade würden aus den Paletten gestrichen (Meldung mit Liste).
Prüfbild `docs/pruefung/elfenwald/G4.png` (1 008 × 1 008): Höhe grau, Beschattung grün getönt, Wasser blau, Weg braun, Ort rot, Klassen
nach `bild_farben`, Blickziele als rotes Kreuz. Große Synthetik-Raster nach dem Test gelöscht.

**Behobene Fehler des Entwurfs:** Klassen-Kanäle aus Pythons `hash()` (je Prozess zufällig, nicht deterministisch) → CRC32; `eigner` 0
pauschal `aue` → dominantes Feldbiom; `SM_MossyTree_01` (liegender Stamm) als Baum gezählt; Python-Schleife im Wurzel-/Efeu-Ring
vektorisiert; Feldgrenze auf Zellen statt Koordinaten; Dichten offener Lagen gesenkt (Grasbüschel 0,040→0,025, Lichtungsblumen 0,028→0,010,
Beere 0,026→0,016, Lichtungsschwelle 0,42→0,34, Kerndichte 0,7–1,6), damit `voll`-Läufe nahe am Ziel landen.

**Erwartete Instanzzahlen je Feld mit Echtdaten (Richtwert, Spanne ±35 %; Grundlage: Land-/Laub-/Wasseranteil, Beschattung 0,8–0,9 bei
170 Bäumen/ha, Standardmodus):**

| Feld | Land % / elfenwald % | Baum (Modus) | Boden | Mittel (zusatz) | Wasserkante | Kollision |
|---|---|---|---|---|---|---|
| G4 | 100 / 76 (Bestand da) | 40–120 (ergaenzen) | 45 000–52 000 (Ziel greift) | 18 000–28 000 | 2 000–5 000 (Wasser 5 %) | 50–150 |
| G3 | 72 / 97 | 9 000–15 000 (voll) | 30 000–45 000 | 12 000–20 000 | 400–1 500 | 7 000–12 000 (Bäume) |
| H3 | 89 / 100, 60 % steil, Fels 26 % | 7 000–12 000 | 25 000–40 000 | 10 000–18 000 | 1 500–4 000 | 6 000–10 000 |
| H4 | 100 / 82 | 9 000–15 000 | 35 000–52 000 | 14 000–24 000 | 1 500–4 000 | 7 000–12 000 |
| I4 | 63 / 21 (bergwald ×0,6) | 2 000–5 000 | 6 000–14 000 | 3 000–7 000 | 300–1 200 | 1 500–4 000 |
| H2 | 39 / 20 (kueste ×0,3) | 800–2 500 | 2 500–7 000 | 1 200–3 500 | 100–500 | 600–2 000 |
| G2 | 4 / 20 | 0–100 | 100–600 | 50–300 | 0 | 0–80 |

Bleibt eine Schicht in G4 unter 50 % der Spanne, stimmt wahrscheinlich die Beschattung nicht (zu wenige Bäume erkannt: Hinweis
„Kronendach aus N Bäumen“ prüfen – N sollte ≈ 17 000 + Nachbarn sein); liegt sie darüber, greift das Ziel (Hinweis „Ausdünnung“).

**Prüfkameras (Augenhöhe 1,7 m, FoV 50°, Sonne 18–24° seitlich):**
1. **G4 Bachquerung** – auf dem Weg 10 m vor der Kreuzung Weg × Bach (Blickziel `schrein_an_bachquerung` in `plan.json`), Blick bachaufwärts.
   Erfolg: Moossteine 0,5–6 m vom Wasser in 2–5er-Gruppen, Farn/Schachtelhalm dazwischen, nichts im Wasser, nichts näher als 2,5 m am Weg;
   innerhalb 10 m ≥ 3 Objekte in 0,5–3 m Höhe (Farninsel, Moosstein, Weide/Pappel am Band 3–14 m).
2. **G4 Lichtung** – Mitte der größten Lichtung (Blickziel `lichtung_mit_blumen`), Blick nach Nordost gegen das Licht. Erfolg:
   Blumeninseln als Flecken 4–8 m (nicht Streu), Adlerfarn und Jungbäume (Teil D) am Rand dichter als innen, ein Hero-Altbaum am Rand
   (Maßstab 1,25–1,55), kein Baum in der Mitte.
3. **G4 Altwald** – 80 m in den Wald (Beschattung > 0,8), Blick quer zum Hang. Erfolg: Laub- und Zweighaufen um die Stämme, Wurzelanläufe
   an 30 % der alten Stämme, Moospolster und Heidelbeere in Senken, Farninseln im Schatten; in 10 m ≥ 4 Objekte in 0,5–3 m (Witcher-
   Richtwert 4–5 je 100 m² zusammen mit Teil D). Vergleich: `KLEIN12_G3_boden` (heute 0,5–0,7).
4. **G3 Waldkante** – an der Grenze Laub (56 %) → Sand (23 %), Blick entlang der Kante. Erfolg: Dichte-Falloff über 15 m innen / 10 m außen,
   Birken und Jungwuchs im Saum, keine harte Linie wie in `W6FIN_G3_rundgang`; Lichtungen 15–25 % (`statistik.lichtung_anteil`).
5. **H3 Hang** – Hangfuß unter einer Fels-Lage (Fels 26 %), Blick hangaufwärts. Erfolg: Bäume dünnen über 30° aus (Fels ×0,3), Moos und
   Kleinsteine ziehen auf den Fels, Farn nur auf der Schattseite; keine Instanz an Hängen > 40° außer Moos/Steinen (bis 45°).
6. **Draufsicht 300 m über G4** (Prüfbild und Editor): Farninseln als Flecken im dunklen Kronendach, Blumen nur in Lichtungen, Heide-Ecke
   (22 %) deutlich dünner (×0,25); **Naht G3/G4 und G4/H4** ohne Dichtesprung (Fenster + 64 m, nahtloses Wertrauschen).

**Erfolgskriterium in Zahlen:** an Kamera 1–3 kein 10-m-Umkreis ohne Objekt in 0,5–3 m Höhe (Mittelschicht Teil D + Elfenwald-Zusatz
zusammen ≥ 3–5 je 100 m²); Instanzen je Schicht in der Tabelle; Kollision Schichten 1/5 < 3 000; Setzer-Zeit je Feld < 5 min (≈ 120–190
Foliage-Typen `FT_EL_EW_*`); keine Instanz schwebt (Eingraben 1–30 cm) und keine steht im Wasser/auf dem Weg.

---

## 6. Einkaufsliste (frei bevorzugt, Stufe High 4K; Raw 8K nur für Hero-Stücke)

| Was | Wofür | Fab-/Megascans-Name (Vorschlag) | Stufe |
|---|---|---|---|
| **Hero-Laubbaum > 25 m** (alte Buche/Eiche, Wurzelanlauf, breite Krone) | Blickziel am Lichtungsrand, Hero-Klasse (heute nur Hornbeam_Field 1,25–1,55 skaliert; AsianTemple-Bäume 31–49 m stilistisch fremd) | Fab: „European Beech – Old / Hero“ (Megascans Trees: European Beech Forest Hero), „English Oak Hero“; ersatzweise Quixel „Common Oak“ | High, Nanite |
| **Eiche** als zweite Hauptart (Elfenwald hat Eiche 0 im Inventar) | Artenmix 20–30 %, Herbstakzent, Hero | Megascans Trees „English Oak“ Set (Forest/Field, Sapling) | High |
| **Ruinenstücke elfisch** (gebogene Bögen, Säulenstümpfe, Reliefplatten, Treppenreste, Bodenplatten) | `spuren_overrides.ruine` – heute nur 5 AncientRuins-Netze, zwei davon > 370 k Dreiecke | Fab „Ancient Ruins Modular“ / „Overgrown Ruins Kit“, Megascans „Ruined Wall Section“, „Stone Column Fragment“, „Carved Stone Slab“ | High, Nanite |
| **Pilze** (Steinpilz, Fliegenpilz, Baumpilz/Zunderschwamm, Pilzgruppen) | Boden-Klasse pilz hat nur 2 Meadow-Netze; Baumpilze an Totholz fehlen ganz | Megascans 3D Plants „Mushroom“ (Fly Agaric, Bolete, Shelf Fungus), Fab „Forest Mushrooms Pack“ | High |
| **Efeu/Ranken** als Stammhüllen und Wandbewuchs (gebogene Karten, Ranken 2–4 m) | Efeu am Stamm (heute flache Ivy-Karten), Ruinenbewuchs 40 % | Megascans „English Ivy Climbing“ (Trunk/Wall-Varianten), „Wild Grape Vine“, Fab „Vines & Creepers“ | High |
| Waldbodenblumen 0,5–1,5 m (Fingerhut, Bärlauch) | Taxonomie-Lücke Lichtpflanzen 0,5–1,5 m | Megascans „Foxglove“, „Wild Garlic“ | High |
| Liegender Hero-Stamm > 8 m mit Wurzelteller | Blickziel im Altwald (LargeFallenTree 5–6 m) | Megascans „Fallen Beech Tree Large“, „Uprooted Tree“ | High/Raw |
| Opfergaben/Kerzen für Schreine | `spuren_overrides.schrein.beigaben` (fehlt) | Fab „Shrine Offerings“, „Medieval Candles“ | Medium |

---

## 7. Offene Punkte und Annahmen

1. **Ungetestet mit Echtdaten.** Beschattungs-Kalibrierung (k = 1,4, σ = 6 m) ist aus Teil D übernommen und an einem Synthetik-Bestand
   geprüft; mit 17 000 Bäumen in G4 wird die Beschattung ≈ 0,9 und die Bodenschicht läuft ins Ziel (52 000). Dann die Boden-Dichten um 20 %
   senken statt ausdünnen zu lassen (Laub 0,024 → 0,019).
2. **Baumschicht-Kollision** 10–13 000 bei `voll` überschreitet den Rahmen „≤ 3 000 Kollision“ bewusst (Bestand-Ebene hat 17 000); wenn
   Ferat das nicht will: `kollision_baum_je_feld` auf 3 000, dann nur hero/tot/alt mit Kollision.
3. **Teil-D-Kopplung.** `--mittel zusatz` setzt voraus, dass `mittelschicht_plan.py` in G3/H3/G4/H4/I4/H2/G2 läuft, und zwar **nach** dem
   Elfenwald-Planer, damit Teil D das Elfenwald-Kronendach (Schicht 2 bei `voll`) sieht; Teil D liest `bestand/` und `witcher/`, nicht
   `elfenwald/` – dort die Ebene `elfenwald` in die Baumquellen aufnehmen (eine Zeile in `lade_baeume`). Umgekehrt liest der Elfenwald-Planer
   keine `mittelschicht/`-Instanzen für den 1,2-m-Abstand; Doppelbelegung derselben Zelle ist bei den entfallenen Klassen ausgeschlossen,
   bei Farn (×0,45) möglich und gewollt (Insel-Verdichtung).
4. **Witcher-Haine bei `voll`.** `entfernen` löscht Witcher-Bäume nur mit den gelisteten Präfixen; Netznamen, die in `witcher/<Feld>/plan.json`
   anders heißen, bleiben stehen → nach dem ersten Echtlauf den Hinweis „entfernen-Filter“ gegen die Witcher-Dateinamen prüfen.
5. **Hang > 40°** bekommt nur Moos/Kleinsteine (bis 45°) und Böschungsstücke am Bach (bis 60°). **Nicht-Nanite-Netze** (Poplar_*,
   Big_Tree_*, hazel, black_cherry, maple_bush, nettle, Forest-grass/-fern) brauchen LOD-Prüfung im Setzer; Sichtweiten 150–350 m.
6. **I4/H2/G2** (20 % Elfenwald): der Planer setzt elfenwald-Zellen voll, bergwald/kueste/aue-Zellen mit 0,6/0,3/0,5; Biomgruppen 1 und 2
   bleiben dort führend. Dopplungen sind über `eigner.r8` ausgeschlossen, solange jeder Planer nur auf seinem `rezept` den Faktor 1,0 hat.
7. **Blickziele** sind Vorschläge in `plan.json` (3 Arten, cm); Instanzen setzt `spuren_plan.py` nach den Overrides; der Elfenwald-Planer
   liefert nur Blumeninsel (Lichtung ×2) und Hero-Altbaum (Lichtungsrand ×12). **Laufzeit** 8–14 s je Feld (4 Kerne, ohne numba; Distanzfelder
   ≈ 6 s).
