# Antwort zu Auftrag 16h – Erlenbach p2: Talkaskade wirkt wie ein sandiger Graben

Stand 13.10.2026. Grundlage: Auftrag `auftraege/16h-erlenbach-p2-talkaskade-ufer-wasser.md`, die Bilder
`bilder/swr_p2/p2x_bogen.jpg`, `tk_mit_ohne_wasser.jpg`, `altwasser_vorher_nachher.png`, die Parameterliste
`bilder/swr_p2/mi_el_swr_klar_parameter.txt`, `vorlagen/daten/material_parameter.json` (Master `M_Eldarien_Wasser_Schaum8`)
und unsere Antworten 16a, 16b, 16e, 16f (beide), 16g, 17 sowie 16c Nachtrag 2–4 (Bachbett-Modul).

**Kennzeichnung:**
- [Befund]: Ferats Messung bzw. Bild aus dem Auftrag
- [Projekt]: eigene Daten, Regeln und Rechnungen im Repo
- [Fach]: Literatur bzw. Physik
- [Doku]/[Forum]: Epic-Seiten bzw. Foren, nur als Suchauszug (`dev.epicgames.com` ist aus der Cloud gesperrt, DNS-Fehler)
- [Ableitung]: aus Belegen geschlossen und gerechnet
- [Gestaltung]: Gestaltungsentscheidung (Ziel Witcher/RDR2, nur Landschaft)
- [unsicher]: nicht belegt, im Test klären

---

## Kurzfazit

- **A – alte Schotterstreifen:** Der Streifen wird **nicht** als trockenes Schotterbett belassen, sondern in drei Bändern
  in die Umgebung überführt:
  - **0–6 m Hochwasserbett:** Talkaskade Geroell 30, Kies 20, Moos 20, Erde 10, Fels 10, Trockengras 10;
    Kiesbett Kies 40, Geroell 20, Moos 15, Trockengras 10, Erde 10, Schlamm 5; am Gleithang eine echte Kiesbank.
  - **6–12 m alte Bänke:** Moos, Trockengras, Wiese und Heide mit 25–35 % Geröll-/Kiesresten.
  - **ab 12 m wie die Umgebung;** im Kiesbett höchstens einzelne alte Schotterflecken unter Gras.
  - Die Grenzen werden über 3 m weich überblendet und um ±1,5 m verrauscht.
- **A – ersetzte Läufe:** Die drei C2-Flüsse und `B_R3_K10_TUNDRA_01` stehen in `skripte/fluss_sim/ersetzt.json` als
  „ersetzt durch Erlenbach p2“. **Unser bisheriger Pilot C2 (`F_ERLENBACH_1V_C2`) ist damit abgelöst; maßgeblich ist p2, Ferats
  eigener lokaler Lauf.**
  - Gefälle-Planer, Roh-Ebene, fluss_sim-Export und alle Prüfer überspringen diese Läufe; wasserherkunft folgt dem Export.
  - Alle übrigen Pläne bleiben byte-gleich.
  - Alle Prüfer melden 0 FEHLER. Der Export ist deterministisch (zwei Läufe byte-gleich).
  - Zahlen in A.3.
- **B – Einheiten:** Absorption ist eine Sichtweite in cm. 16f (0,45; 0,10; 0,08) je m = (222, 1000, 1250) cm.
- **B – Ursache Gold und Milch:** Bei 0,5–0,6 m Tiefe lässt jede der diskutierten Absorptionen 80–98 % durch. Der goldbraune
  Schleier kommt vor allem aus der **Streuung** (Scattering A 0,1 ist sehr wahrscheinlich 100- bis 1000-mal zu trüb) im warmen
  Licht. Die hellen Flecken kommen vom **DF-Schaum an den Steinen** (`ELD_DF_Schaum` 1,15, Radius 65 cm) und vom harten
  Simulationsschaum (`SimFoam Contrast` 12). Dazu kommen die starken Normalen (40) und der helle Kies.
- **B – Empfehlung V1:**
  - Absorption **(300, 1600, 1200)** cm;
  - Scattering **(0,18; 0,32; 0,28; A 0,008)**, Water Albedo 0,02, Refraction 1,08, Roughness 0,03;
  - Sim Velocity Normal 12, SimFoam Contrast 3;
  - `ELD_DF_Schaum` 0,25 mit Radius 30, Uferschaum 0,15, Deckkraft 0,6.
  - Damit ist der Grund bei 1 m deutlich (Y 0,89) und das tiefe Becken leicht grün.
  - V2 (grüner) und V3 (Gletscher-klar) als Testreihe; zuerst T0, das die Ursachen in 10 Minuten trennt.
- **B – FoamAtten nachbauen:** **Ja**, etwa 10 Knoten. Das Tempo liest der Master in WCBS aus der Wasser-Info der Water Zone
  (`WaterVelocityAndHeight`, derselbe Zweig wie `Velocity Debug`).
  - Start: Schaum ab 250/450 cm/s, Streuung × 5 ab 150/400 cm/s.
  - Ohne Tempo: Schaum über die Steilheit der gebackenen Wasserfläche.
- **C – Ufer:** Die Kästen kommen vom „Kasten-U“ mit 1,5 m Rampe (unsere 16f-Empfehlung, für Schluchten gedacht) und vom
  kurzen Falloff.
  - Neu: Lockerböschungen 30–35° (max. 36°, unter der Schichtband-Schwelle); Prallhang 45–70° mit Erdanriss, Wurzeln und
    Blockfuß; Gleithang 5–15° mit Kiesbank.
  - Kasten-Prüfung (> 0,6 m über 45° in Lockermaterial); Reparatur durch „Böschung zurücklegen“ auf 32°.
  - Schichtbänder nur auf Fels ab 3 m Wandhöhe.
  - Bewuchs an der Kante und halb eingegrabene Steine mit Zahlen.
- **C – Umsetzung:** als Regeldatei für Ferats Werkzeug, [`bachbett_ufer_regeln.json`](bachbett_ufer_regeln.json), mit
  Referenz-Umsetzung `skripte/ufer_regeln/ufer_regeln.py` (Selbsttest 0 FEHLER). Unser Planer erzeugt keine Kästen (35°)
  und plant C2 nicht mehr, deshalb ändere ich dort kein Gelände.

---

## A. Alte Kies- und Geröllstreifen der ersetzten Flüsse

### A.1 Entscheidung

**Dem Vorschlag des Koordinators stimme ich zu, mit zwei Ergänzungen** [Gestaltung]:

1. **Kein trockenes Schotterbett.** Ein 25–35 m breiter Streifen ohne Wasser liest sich als Rest eines Fehlers. Ein echter
   2–5-m-Gebirgsbach hat ein Hochwasserbett von ein bis drei Bachbreiten. Breiter wird es nur bei großen Talflüssen oder nach
   Murgängen; dann aber mit Wildholz, Abbruchkanten und Pionierbewuchs, nicht als gleichmäßiger Streifen.
2. **Übergang in drei Bändern** (Abstand d zur p2-Wasserkante):
   - 0–6 m Hochwasserbett aus Kies und Geröll, der Uferstreifen (Moos/Erde/Schlamm) liegt vorn;
   - 6–12 m alte Bänke: Geröllreste mit Moos und Gras in Flecken;
   - ab 12 m wie die Umgebung.
3. **Ergänzung Kiesbett (s 579–728):** Dort ist der Talboden flach. Am **Gleithang** bleibt eine echte Kiesbank (0,5–1,0 × B
   breit, ≤ 0,3 m über Mittelwasser). Ab 12 m liegen höchstens einzelne alte Schotterflecken unter Gras (Rauschen 6 m,
   ≤ 10 % der Fläche), nie ein Streifen. Das erzählt „hier floss früher mehr“, ohne als Fehler zu wirken.
4. **Ergänzung Grenzen:** Die Bandgrenzen nie als gerade Linie. Jede Grenze wird je Ort um ±1,5 m verschoben (Rauschen mit
   4 m Wellenlänge) und dann über 3 m weich überblendet.

Bei der Talkaskade ist der Streifen schon heute zwischen 12 und 30 m weitgehend Umgebung (Kies 3 %, Tabelle Befund A).
Dort genügt das Band 6–12 m. Im Kiesbett liegen dagegen bei 12–30 m noch 26–40 % Kies; dort ist der Umbau am größten.

### A.2 Mischung je Band (Prozent der Deckung, Summe 100)

Lagen nur aus FORMAT.md §2. Die Maske ist das alte Flussband (die vier ersetzten Läufe, halbe Breite + 3 m); außerhalb
ändert sich nichts. Der Uferstreifen aus `bachbett_regeln.json` (Tundra: Moos 45, Erde 35, Schlamm 20; 0–3,5 m neben der
Kante, −0,1 bis 1,0 m über dem Spiegel) bleibt deckend vorn.

| Band | Talkaskade (s 390–579) | Kiesbett (s 579–728) | Gras-Dichte (× Umgebung) |
|---|---|---|---|
| **0–6 m** Hochwasserbett | Geroell 30, Kies 20, Moos 20, Erde 10, Fels 10, Trockengras 10 | Kies 40, Geroell 20, Moos 15, Trockengras 10, Erde 10, Schlamm 5 | 0,2–0,4 |
| 0–6 m am **Gleithang** (Kiesbank) | wie oben | Kies 55, Geroell 15, Sand 10, Moos 10, Trockengras 10 | 0,2 |
| **6–12 m** alte Bänke | Moos 25, Trockengras 25, Geroell 15, Wiese 15, Kies 10, Heide 10 | Trockengras 25, Wiese 20, Moos 20, Kies 15, Geroell 10, Heide 10 | 0,6–0,8 |
| **ab 12 m** Umgebung | Median der Lagen in 30–60 m Abstand außerhalb der Maske, gleiche Höhe ± 15 m und Neigungsklasse; Richtwert Trockengras 30, Heide 25, Wiese 25, Moos 15, Kies 5 | wie links; Richtwert Trockengras 30, Wiese 30, Heide 20, Moos 15, Kies 5; dazu Rest-Schotter (Kies ≤ 15, Geroell ≤ 10 in Flecken) | 1,0 |

- **Fels** im Hochwasserbett nur auf Flächen ≥ 32°; sonst geht sein Anteil an Geroell.
- **Ziel der Prüfung:** kein zusammenhängendes Band mit Kies + Geroell > 50 % über mehr als 8 m Breite und 20 m Länge
  außerhalb 0–6 m.
- Beispiele mit Übergang aus der Referenz-Umsetzung (`skripte/ufer_regeln/ufer_regeln.py`):

  | d | Talkaskade | Kiesbett |
  |---|---|---|
  | 2 m | Geroell 30, Kies 20, Moos 20, Erde 10, Fels 10, Trockengras 10 | Kies 40, Geroell 20, Moos 15, Erde 10, Trockengras 10, Schlamm 5 |
  | 6 m (Grenze) | Geroell 22,5, Moos 22,5, Trockengras 17,5, Kies 15, Wiese 7,5, Erde/Fels/Heide je 5 | Kies 27,5, Moos 17,5, Trockengras 17,5, Geroell 15, Wiese 10, Erde/Heide 5, Schlamm 2,5 |
  | 9 m | Moos 25, Trockengras 25, Geroell 15, Wiese 15, Kies 10, Heide 10 | Trockengras 25, Moos 20, Wiese 20, Kies 15, Geroell 10, Heide 10 |
  | 20 m | Trockengras 30, Heide 25, Wiese 25, Moos 15, Kies 5 | Trockengras 30, Wiese 30, Heide 20, Moos 15, Kies 5 |

- **Umsetzung:** über eure bewährte Kette `s38 lagen`. Die Zahlen stehen maschinenlesbar in
  [`bachbett_ufer_regeln.json`](bachbett_ufer_regeln.json) → `A_altbett`.

### A.3 „Ersetzt durch Erlenbach p2“ in unseren Planern

**Neue Datei** [`skripte/fluss_sim/ersetzt.json`](skripte/fluss_sim/ersetzt.json): Sie nennt die vier Läufe mit Grund und
den Ersatz `ERLENBACH_P2` (Quelle D2-Felsrinne auf 190 m, 788 m, Mündung in den C3-Fluss, Abschnitte).

**Wichtig – Stand C2:** Bisher war C2 unser **Pilot Rang 1** (`F_ERLENBACH_1V_C2_s1`, A15, 16c, 16g). **Dieser Stand ist
abgelöst. Maßgeblich ist jetzt p2, Ferats eigener lokaler Lauf.** Unsere Pläne für C2 ruhen: Es gibt keinen Gefälle-Plan,
keine Roh-Ebene und keinen fluss_sim-Teil mehr. Für p2 liefern wir nur noch Regeln, die Ferats Werkzeug lesen kann
(Teil C). Wer C2 wieder planen will, entfernt den Eintrag in `ersetzt.json`.

**Wo die Läufe vorkamen und was jetzt gilt:**

| Stelle | vorher | jetzt |
|---|---|---|
| `gefaelle_daten.lade_strecken` (Planer, Prüfer, Priorität) | 161 Strecken, davon 4 auf den ersetzten Läufen (`F_ERLENBACH_1V_C2` 2, `_1_C2` 1, `_2_C2` 1) | 157 Strecken; die Liste der übersprungenen steht im Log |
| `gefaelle_daten.alle_laeufe` (Feldgrenzen, Roh-Ebene, Prüfer) | alle Welt-Läufe | ohne die ersetzten (`mit_ersetzten=True` für Sonderfälle) |
| `gefaelle_plan.py` | plante C2 (Pilot Rang 1); Zuflüsse und „anderes Gewässer“ enthielten die alten Läufe | überspringt sie (Log-Zeile „Ersetzt …“); `--laeufe F_ERLENBACH_1V_C2` ergibt nur einen HINWEIS |
| `gefaelle_pruefen.py`, `bachbett_roh_pruefen.py` | prüften jeden Ordner | alte Ordner ersetzter Läufe: HINWEIS „alter Plan, nicht geprüft“ (für eure lokalen Altordner) |
| `bachbett_roh.py` | Roh-Ebene für `F_ERLENBACH_1_C2`, `_2_C2`, `B_R3_K10_TUNDRA_01` und Reststrecken von `_1V_C2` | keine; Altordner werden im Log genannt. Die Linien der ersetzten Läufe (mit halber Breite + 1,5 m) spart die Roh-Ebene wie fremdes Wasser aus („Ersatz-Gewässer“), weil dort lokal p2 fließt und mündet |
| `fluss_sim_export.py` | Gewässer `F_ERLENBACH` begann mit `_1_C2 → _1V_C2 → _2_C2`; `B_R3_K10_TUNDRA_01` war Zufluss | Teile, Lauf-Pläne und Roh-Ebenen ersetzter Läufe übersprungen (`eingaben.uebersprungen`, `laeufe.ersetzt` in `zusammenfassung.json`); `F_ERLENBACH` beginnt am C3-Lauf, `anfang.ersetzter_oberlauf` nennt den Ersatz |
| `fluss_sim_pruefen.py` | Soll = alle Welt-Läufe | Soll ohne die ersetzten; ein ersetzter Lauf in einem Gewässer = FEHLER; HINWEIS mit der Liste |
| `wasserherkunft.py` | Fälle aus dem fluss_sim-Export, darunter C2 | liest den neuen Export; die C2-Fälle fehlen dort von selbst (keine Code-Änderung nötig) |
| Sehens-Planer | planen keinen dieser Läufe | unverändert |
| 2-m-Raster der Cloud (`wasser`) | enthalten die alten Flüsse | unverändert; sie wirken im Gefälle-Planer nur als Schutzzone „fremdes Wasser“ und liegen ungefähr dort, wo jetzt p2 fließt. Lokal sind die Raster schon bereinigt |
| `antworten/wasser_fx/plan.json` (A14, C2_A–C2_E) | Geschichte | Geschichte (A15 hatte sie schon ersetzt) |

**Zahlen vorher → nachher** (Cloud, 2-m-Daten, Sehens-Ausgaben gleich):

| Lauf | vorher | nachher |
|---|---|---|
| **Gefälle `--alle`** | 123 Läufe, 98 mit Stufen, 1 071 Stufen; Planer 0 FEHLER, 2 WARNUNG; Prüfer 0 FEHLER, 43 WARNUNG, 301 HINWEIS | **120 Läufe, 96 mit Stufen, 1 050 Stufen**; Planer 0 FEHLER, 2 WARNUNG; Prüfer **0 FEHLER**, 41 WARNUNG, 296 HINWEIS. Weg: `F_ERLENBACH_1V_C2` (18 Stufen, 1 901 Instanzen, 42 Akteure, 18 Effekte) und `F_ERLENBACH_2_C2` (3 Stufen, 865 Instanzen, 10 Akteure). Die übrigen 96 Pläne sind byte-gleich |
| **Piloten, 1-m-Fenster** | 19 Läufe, 341 Stufen; Prüfer 0 FEHLER, 11 WARNUNG | **18 Läufe, 323 Stufen**; Prüfer **0 FEHLER**, 9 WARNUNG; die 18 übrigen byte-gleich (Pilot C2 entfällt, `prioritaet.json` bleibt als Geschichte) |
| **Roh-Ebene** | 97 Roh-Läufe, 98 Reststrecken; Prüfer 195 Läufe, 0 FEHLER, 0 WARNUNG, 463 HINWEIS | **95 Roh-Läufe, 96 Reststrecken**; Prüfer 191 Läufe, **0 FEHLER**, 0 WARNUNG, 455 HINWEIS. Weg: `B_R3_K10_TUNDRA_01` (27 Instanzen), `F_ERLENBACH_1_C2` (19), `F_ERLENBACH_2_C2` (52), `_1V_C2` (0). `F_ERLENBACH_2_C3`: 56 → 38 m Bachbett, 31 → 19 Instanzen, weil die Fläche der alten C2-Flüsse jetzt als Ersatz-Gewässer ausgespart ist (dort mündet lokal p2). Alle anderen Läufe byte-gleich |
| **fluss_sim** | 187 Gewässer, 199 SWR, 762 Fälle (170 Vorhang), 2 078 Abstürze, 41 235 Wasser-Kollisionen, 6 863 überspannt, 45 894 m | **186 Gewässer, 197 SWR, 737 Fälle (166 Vorhang)**, 2 032 Abstürze, 40 476 Kollisionen, 6 804 überspannt, 45 438 m; Prüfer **0 FEHLER**, 0 WARNUNG, 72 HINWEIS (vorher 73); zwei Läufe byte-gleich |
| `F_ERLENBACH` | 1 006,7 m, 7 Läufe ab `_1_C2`, 2 SWR (`_T00` 1 856, `_T01` 2 048), 31 Fälle, 1 015 Kollisionen, Zuflüsse inkl. `B_R3_K10_TUNDRA_01` | **623,7 m**, 4 Läufe ab `F_ERLENBACH_2_C3`, **1 SWR `F_ERLENBACH`** (2 048, Zelle 0,299 m), 6 Fälle, 272 Kollisionen; `anfang.ersetzter_oberlauf` = `F_ERLENBACH_2_C2`, `B_R3_K10_TUNDRA_01` → ERLENBACH_P2 |
| Fingerabdrücke | – | neu backen: `F_ERLENBACH` (neu, statt `_T00`/`_T01`); nur Objektteil geändert: `B_R2_K10_TUNDRA_01` (121 → 94 Objekte), `B_R2_K10_TUNDRA_02` (70 → 63); `B_R3_K10_TUNDRA_01` entfällt; alle übrigen 194 gleich |
| Wasserzonen | 29 Zonen (28 fein), 1 427 MB RGBA16F | 28 Zonen (27 fein), 1 458 MB; `F_ERLENBACH` liegt jetzt in `WZ_F07` (4096 × 2048, 1,25 m Pixel) statt in einer eigenen Zone. In 80 weiteren Dateien ändert sich nur die Nummer `water_zone_vorschlag` (WZ_Fnn rückt nach) |
| **wasserherkunft** | 178 Fälle: 69 plausibel, 78 fragwürdig, 31 aus dem Nichts | **174 Fälle**: 69 / 76 / 29 (die vier Vorhang-Fälle von C2 entfallen; Tundra 6/6 → 4/4) |
| Sehens (15 Planer, 2 m) | 0 FEHLER | unverändert (nicht betroffen), 0 FEHLER |
| Selbsttest `sehens_lib` | 149 ok | 149 ok, 0 FEHLER (Bibliothek unverändert) |

Die Beispiele unter `antworten/fluss_sim/` (`F_ERLENBACH`, `bergwald_06_karsee` (nur Zonennummer), `zusammenfassung.json`,
`vorschlaege.json`, `wasserzonen.json`, `back_liste_auszug.json`) und `antworten/wasserherkunft/` sind neu gerechnet. Der
Vorher-Lauf reproduzierte die bisherigen Repo-Dateien byte-genau.

---

## B. Das Wasser verdeckt das Bett

### B.1 Einheiten

- **Absorption RGB = Sichtweite in cm** (Ferat lokal). Das passt zu 16a b1: Das Material rechnet 1/Wert und gibt den
  Kehrwert als SLW-Koeffizienten je cm weiter. Durchlass nach d cm: T = exp(−d / Wert).
- **Umrechnung je m → cm:** Wert [cm] = 100 / Koeffizient [je m]. 16f (0,45; 0,10; 0,08) je m = **(222, 1000, 1250) cm**. 16a
  (250, 1430, 2000) cm = (0,40; 0,07; 0,05) je m.
- **Scattering RGB = Streufarbe, A = Stärke** (Ferat lokal). Wie das Material RGB × A verrechnet (je cm, je m, als Länge
  oder über `Water Albedo`), ist nicht belegt [unsicher]. Die Suchauszüge zur SLW-Doku nennen nur die vier Eingänge
  Scattering Coefficients, Absorption Coefficients, PhaseG und Color Scale Behind Water und Beer-Lambert mit
  Extinktion = Streuung + Absorption [Doku, Forum]. Einen Parameter „Water Albedo“ nennt keine gefundene Quelle. Test T0
  (Abschnitt Testreihe) klärt das in 10 Minuten.

### B.2 Warum goldbraun und milchig? Rangfolge der Ursachen

**Rechnung Absorption** [Ableitung]: Durchlass T = exp(−d/L), Helligkeit Y = 0,21 R + 0,72 G + 0,07 B.

| Variante (cm) | 50 cm | 100 cm | 141 cm (1 m unter 45°) | 250 cm |
|---|---|---|---|---|
| heute A (400, 900, 750) | 0,88 / 0,95 / 0,94 (Y 0,93) | 0,78 / 0,89 / 0,88 (Y 0,87) | 0,70 / 0,85 / 0,83 (Y 0,82) | 0,54 / 0,76 / 0,72 (Y 0,71) |
| 16a (250, 1430, 2000) | 0,82 / 0,97 / 0,98 | 0,67 / 0,93 / 0,95 (Y 0,88) | 0,57 / 0,91 / 0,93 | 0,37 / 0,84 / 0,88 |
| 16f (222, 1000, 1250) | 0,80 / 0,95 / 0,96 | 0,64 / 0,90 / 0,92 (Y 0,85) | 0,53 / 0,87 / 0,89 | 0,32 / 0,78 / 0,82 |
| **V1 (300, 1600, 1200)** | 0,85 / 0,97 / 0,96 | 0,72 / 0,94 / 0,92 (Y 0,89) | 0,63 / 0,92 / 0,89 (Y 0,85) | 0,43 / 0,86 / 0,81 (Y 0,76) |

**Folgerung:** Bei 0,47–0,64 m Tiefe (Befund) lässt jede dieser Absorptionen 80–98 % durch. **Die Absorption ist nicht die
Hauptursache.** Sie entscheidet nur über den Farbton tiefer Becken. Die Ursachen sind, nach Gewicht:

| Rang | Ursache | Wirkung im Bild | Beleg |
|---|---|---|---|
| 1 | **Streuung zu stark:** Scattering A = 0,1. Wirkt RGB × A je cm, sind das 0,02–0,03 je cm = 2–3 je m, also das 500- bis 1000-Fache von klarem Wasser (0,002–0,004 je m, 16f §5). Bei 50 cm Tiefe ist die optische Dicke 1–1,5: zwei Drittel des Bildes sind Streulicht. | milchiger Schleier; die warme Sonne färbt ihn (Streufarbe 0,2/0,3/0,28 × Abendlicht) **goldbraun** | [Ableitung, unsicher Einheit]; passt zum Bild: Steine verschwimmen, obwohl die Absorption klar ist |
| 2 | **DF-Schaum an Steinen:** `ELD_DF_Schaum` 1,15 mit `ELD_Kontakt_Radius` 65 cm und `Depth for DF Foam` 24 legen Schaum über jeden Stein bis 65 cm unter der Fläche; `ELD_Schaum_Deckkraft` 1, `ELD_Schaum_Farbe` 0,8/0,84/0,82 | **helle, steinförmige Flecken** (Zeile 3 links: die Flecken sitzen genau auf den Steinen rechts) | [Befund Bild], [Ableitung] |
| 3 | **Simulationsschaum hart:** `SimFoam Contrast` 12 macht aus schwachem Schaum harte Flächen; `Foam Opacity` 0,5, `Foam Boost` 0,8, `Foam powr` 0,6; dazu `ELD_Strom_Schaum` 0,8 und `ELD_Ufer_Schaum` 0,5 | helle Fladen und Säume auch in ruhigen Becken | [Ableitung]; 16a riet zu Kontrast 2 |
| 4 | **Verzerrung:** `Sim Velocity Normal Strength` 40 (16e/16f: 15) plus `Refraction` 1,15 und `WPO Flowmap` 6 | marmorierte Schlieren (Zeile 1), der Grund verwischt | [Befund Bild], [16e] |
| 5 | **Heller, gelber Grund:** Die Bettlagen sind hellocker (Kies/Sand). Klares Wasser über hellem Kies sieht auch in der Natur golden aus. Unter Wasser fehlt die dunkle, kühle Nassfarbe | Gold bleibt auch bei klarem Wasser | [Befund Bild rechts], [Fach] |
| 6 | **Spiegelung der Hänge:** Bei flachem Blick (Augenhöhe) spiegelt die glatte Fläche (`Water Roughness` 0,02) die sonnigen, gelben Grashänge | goldener Glanz bei flachem Blick | [Ableitung] |
| 7 | Absorption Rot zu lang relativ zu Grün: 400 cm lässt bei 1 m noch 78 % Rot durch, Blau (750) wird stärker geschluckt als Grün (900) | leicht gelbgrüner Ton, nicht die Hauptursache | [Ableitung, Tabelle] |
| – | Scene-Color-Tönung (`Color Scale Behind Water`) | im Master nicht als Parameter sichtbar; Post-Process-Weißabgleich wirkt auf beide Bildhälften gleich | [unsicher] |

### B.3 Werte für unsere vorhandenen Parameter

**Ziel:** Grund sichtbar, kein Goldton, leichter Grünstich in tiefen Becken, Weißwasser nur an Stufen. Alle Werte im
`MI_EL_SWR_Klar` (bzw. je Variante eine Kopie). Nicht genannte Parameter bleiben. **Kein neues Backen nötig** (reine
Material-Werte).

| Gruppe | Parameter | heute | **V1 (Empfehlung)** | V2 grüner | V3 Gletscher-klar | Begründung |
|---|---|---|---|---|---|---|
| Farbe | `Absorption` (cm) | 400, 900, 750, 8 | **300, 1600, 1200**, 8 | 250, 1300, 900, 8 | 350, 2000, 2200, 8 | Rot 2–4 m, Grün 10–20 m, Blau 15–30 m (Physik); Blau < Grün gibt den Grünstich (Humus) |
| | `Scattering` (RGB, A) | 0,2; 0,3; 0,28; **0,1** | **0,18; 0,32; 0,28; 0,008** | 0,18; 0,34; 0,26; 0,015 | 0,16; 0,30; 0,32; 0,003 | Hauptursache Milch; A um Faktor 12 senken; Farbe leicht grün |
| | `Water Albedo` | 0,03 (A 0,5) | **0,02** | 0,03 | 0,015 | weniger Körper [unsicher Wirkung] |
| Brechung | `Refraction` / `Refraction Far` | 1,15 / 1,02 | **1,08** / 1,02 | 1,10 / 1,02 | 1,05 / 1,02 | weniger Verwischen; flache Bäche brauchen wenig |
| Fläche | `Water Roughness` / `Water Specular` | 0,02 / 0,225 | **0,03** / 0,225 | 0,03 / 0,225 | 0,025 / 0,225 | Spiegelbild der gelben Hänge weicher, nicht milchig |
| Normalen | `Sim Velocity Normal Strength` | 40 | **12** | 15 | 8 | Marmor weg (16e/16f) |
| | `Default Near Normal Strength` | 0,25 | **0,2** | 0,25 | 0,15 | Grund ruhiger |
| | `WPO Flowmap` | 6 | **3** | 3 | 2 | 16f: WPO halbieren, Bach ≤ 2 cm [unsicher Einheit] |
| Epic-Schaum | `SimFoam Contrast` | 12 | **3** | 4 | 2 | keine harten Fladen |
| | `Foam Opacity` / `Foam Boost` / `Foam powr` | 0,5 / 0,8 / 0,6 | **0,4 / 0,5 / 1,2** | 0,45 / 0,6 / 1,0 | 0,35 / 0,45 / 1,5 | nur kräftiger Schaum bleibt (powr > 1 dämpft schwachen Schaum, wenn es eine Potenz ist [unsicher]) |
| | `Sim Foam Dpeth Min` | 8 | **15** | 15 | 20 | kein Schaum in dünnen Rinnen (16f) |
| | `Depth for DF Foam` | 24 | **12** | 16 | 8 | DF-Saum nur knapp unter der Fläche |
| ELD-Schaum | `ELD_DF_Schaum` | 1,15 | **0,25** | 0,4 | 0 | Hauptquelle der Steinflecken |
| | `ELD_Kontakt_Radius` | 65 | **30** | 35 | 25 | nur Steine, die die Fläche fast berühren |
| | `ELD_Strom_Schaum` | 0,8 | **0,5** | 0,6 | 0,4 | bis zum FoamAtten-Nachbau |
| | `ELD_Ufer_Schaum` | 0,5 | **0,15** | 0,2 | 0,1 | dünner Saum statt heller Rand |
| | `ELD_Schaum_Deckkraft` | 1 | **0,6** | 0,7 | 0,5 | |
| | `ELD_Fels_Schaum` | 0 | 0 | 0 | 0 | bleibt aus |
| Kaustik | Schalter `Caustics` | False | False | False | **True** (Test) | statischer Schalter, kompiliert neu; belebt den Grund (16f §5) |

- **Prüfung „Grund bei 1 m deutlich“** [Ableitung]: Mit V1 lässt 1 m Wasser 72 / 94 / 92 % durch (Y 0,89). Unter der Annahme
  „RGB × A je cm“ ist die Streuung bei 1 m 0,18–0,32 optische Dicke, also 16–27 % Schleier: Steine bleiben deutlich. Bei 2,5 m
  bleiben 43 / 86 / 81 % und rund 50 % Schleier: Umrisse, grünlich. Das ist das Ziel aus 16f §5.
- **Kein Gold mehr:** Rot fällt bei 1 m von 78 auf 72 %, der Schleier (Rang 1) von etwa zwei Dritteln auf ein Fünftel.
  Der Rest kommt vom hellen Kies (Rang 5). Dazu im Bett unter Wasser **Geroell vor Kies** und, wo das Landschaftsmaterial es
  kann, eine Nassfarbe (Grundfarbe × 0,6, Rauheit 0,3; 16b). Die Lage `Algen` gibt es (FORMAT §2): 5–10 % in ruhigen Becken
  dunkeln den Grund grünlich ab.
- **Weißwasser nur an Stufen:** Mit den Werten oben bleibt Schaum nur dort, wo die Simulation kräftigen Schaum backt, also an
  Stufen und Fallfüßen. Sicher trennt erst `FoamAtten` (B.4).

### B.4 FoamAtten und Velocity-Scattering nachbauen?

**Ja, es lohnt sich** [Ableitung]: etwa 10 Knoten, kein neues Backen, wirkt an allen Gewässern, und es trifft „Schaum und
Milch nur an Stufen“ genauer als jede Maske. Aufwand etwa 1 h als Kopie `M_Eldarien_Wasser_Schaum9`.

**Woher kommt das Tempo bei WCBS?** [Projekt, Ableitung, teils unsicher]
- In WCBS zeichnet der Water Body mit unserem Master. Die gebackene Simulation wird in die **Wasser-Info der Water Zone**
  geschrieben. Das hat 16g gezeigt: Erst mit 4096 Pixeln war das Bett nass.
- Der Master liest sie über `WaterVelocityAndHeight` (`Texture2DArray`, Schalter `UseWaterInfoTexture` = True, Schicht nach
  `WaterZoneIndex`). Laut Forum 5.6 stehen dort Blau = Wasserhöhe und Alpha = Bodenhöhe [Forum]. Die Strömung steht sehr
  wahrscheinlich in Rot/Grün, kodiert relativ zu `MaxFlowVelocity` 1024 cm/s [Ableitung, 16e].
- Den direkten Weg über die gebackene Textur (`BakedWaterSimTex`/`…VT`, `BakedWaterSimSize`) nutzt unser MI nicht:
  `UseBakedSim` = False, `BakedWaterSimSize` = 0 [Befund Parameterliste]. Ob `UseBakedSim` = True in WCBS bessere bzw.
  feinere Daten liefert, ist unbelegt [unsicher] → Test T3.
- Die Material-Funktion heißt in Epics Material vermutlich „SampleWaterInfo“ o. ä.; der Name ist nicht belegt [unsicher].
  **Praktisch:** Den Knoten nehmen, der bei `Velocity Debug` = 1 die Farbe ausgibt. Dort liegt die dekodierte Strömung
  schon vor.

**Knotenplan (Kopie des Masters, 6 neue Skalare + 3 für Wellen):**

1. `v` = Length(Strömung.xy) aus dem Zweig von `Velocity Debug` (in cm/s, wenn dort schon dekodiert; sonst × 1024).
2. `FoamAtten` = SmoothStep(`FoamAttenMin`, `FoamAttenMax`, v). Start **250 / 450 cm/s** (16f §3.2).
3. `FoamGate` = Lerp(`LowVelocityFoamScale` **0**, 1, FoamAtten).
4. Epic-Simulationsschaum × FoamGate, **vor** `SimFoam Contrast` und `Foam Opacity`.
5. ELD-Schaum × Lerp(1, FoamGate, `ELD_Schaum_Tempo_Bindung` **1**). Dann hängen auch DF-, Strom- und Uferschaum am Tempo.
6. `ScatGate` = SmoothStep(`Scattering Min Velocity` **150**, `Scattering Max Velocity` **400** cm/s, v).
7. Scattering.A_eff = Scattering.A × Lerp(1, `Scattering High Mult` **5**, ScatGate). Becken klar, Fallfuß milchig (Luftbläschen).
8. Optional Wellen: Normalstärke × Lerp(`Low Velocity Wave Scale` **0,2**, 1, SmoothStep(`Wave Atten Min` **30**,
   `Wave Atten Max` **150** cm/s, v)).

- **Prüfen mit `Velocity Debug`** in WCBS: Becken < 50 cm/s, Rinnen 100–250, Stufenfuß > 300 [16f]. Erreichen die p2-Stufen
  keine 250 cm/s, `FoamAttenMin` auf 150 und `FoamAttenMax` auf 300 senken.

**Alternative ohne Tempo** (falls die Strömung im Master nicht greifbar ist):
- **Steilheit der Wasserfläche:** In WCBS ist die gebackene Fläche an Stufen geneigt. Schaum = SmoothStep(0,08; 0,25;
  1 − N.z) der **Grundnormale** (vor Detail-Normalen), also etwa 23–41° Flächenneigung. Drei Knoten, ebenfalls ohne Backen.
  Das ist die beste Alternative für p2.
- **Krümmung** (DDX/DDY der Höhe): fängt auch Wellenkämme, unruhiger.
- **Kapsel-Maske** (16e Option B, `schaum_maske` im Export): für p2 nicht verfügbar, weil p2 nicht in unserem Export liegt.
  Ferats Werkzeug könnte die Kapseln an seinen Stufen selbst setzen; das ist mehr Arbeit als die Steilheit.

---

## C. Ufer der Talkaskade

### C.0 Befund und Ursache

- Die Kaskade schneidet 0,5–1,5 m in den Hang [Befund]. Mit der Kurve „Kasten-U“ und `curve_ramp_width` 1,5 m aus
  **unserer** Empfehlung 16f §3.2 und einem Falloff von 1–2 m entstehen 50–70° steile Wände aus Lockermaterial. Ab 38° legen
  sich die V17-Schichtbänder darüber. So entsteht die „Treppe aus sandigen Kästen“.
- Kasten-U war für Grobblock-Schluchten gedacht. **Für die Talkaskade war die Empfehlung falsch;** dort gilt jetzt die
  Mulde unten (C.1).
- Unser Gefälle-Planer erzeugt keine Kästen. Er legt die Böschung mit 35° durch die Wasserkante und begrenzt den Abtrag
  außen (15e). Steiler wird es dort nur gewollt (Uferklippen 60–90°, Klamm 85°). C2 ruht, deshalb ändere ich am Planer-Gelände
  nichts. Der wichtigste Teil ist eine **Regeldatei für Ferats Werkzeug**:
  [`bachbett_ufer_regeln.json`](bachbett_ufer_regeln.json) mit der Referenz-Umsetzung
  [`skripte/ufer_regeln/ufer_regeln.py`](skripte/ufer_regeln/ufer_regeln.py) (nur Standardbibliothek, Selbsttest 0 FEHLER).

### C.1 Profil

| Lage | Böschung | Details |
|---|---|---|
| Kies/Geröll (Lockermaterial) | **30–35°, Ziel 32°, max. 36°** | Schüttwinkel natürlicher Kies mit Sand 25–30°, kantiger Schotter 35–45° [Fach]; 36° bleibt unter der Schichtband-Schwelle 38° |
| Erd-/Rasenufer | 40–75° nur in der Wurzelzone (oberste 0,3–0,8 m) | darunter Kiesfuß mit 30–35°; Grasnarbe darf 0,1–0,3 m überhängen; Wurzeln halten nur, wo sie die Bruchfläche kreuzen [Fach, Pollen-Bankhead] |
| Fels | 60–90° | nur bei anstehendem Fels (Fels + Felsplatte ≥ 50 % vor dem Graben), ab 3 m Wandhöhe oder im Durchbruch |
| Gerade Strecke | beide Seiten 28–35° | Schulter oben rund (Radius 0,5–1 m) |
| **Prallhang** (Außenkurve, Krümmung ≥ 1/(5 B)) | 45–70° | oben Erdanriss 0,3–0,8 m mit Wurzeln, unten Blockfuß; felsig ab 1,5 m Höhe |
| **Gleithang** (Innenkurve) | 5–15° | Kiesbank 0,5–1,0 × B breit, ≤ 0,3 m über Mittelwasser |
| Talkaskade quer zum Hang | bergseitig Prallhang-Regel ab h > 1 m, talseitig 15–25° | asymmetrisch wie in der Natur |
| Stufe (Lippe) | Ufer 1–2 m lang mit Blöcken gefasst | kein glatter Erdhang neben dem Fall |

- **Kasten-Verbot (Prüfung):** je Querschnitt (alle 2 m) die größte zusammenhängende Höhe mit > 45° in Lockermaterial;
  über 0,6 m ist ein Kasten (Ausnahme Prallhang-Anriss bis 0,8 m und Fels).
- **Reparatur ohne neues Graben („Böschung zurücklegen“):** nur abtragen, z_neu = min(z_alt, z_Kante + (d − d_Kante) ×
  tan 32°), höchstens 4 m vom Wasser. Bei 1,5 m Einschnitt wird die Böschung 2,4 m breit. Die Wasserkante bleibt, die SWR muss
  danach **Reset + Bake**. Die Oberkante mit ±0,2–0,4 m Rauschen (Wellenlänge 2–4 m) brechen.
- **Für neu gegrabene Abschnitte (Water Plugin):**

  | Feld | Talkaskade | Kiesbett | Durchbruch/Bergrinne |
  |---|---|---|---|
  | Kurve | **Mulde** (0; 0), (0,2; 0,4), (0,5; 0,8), (1; 1) | Mulde | Kasten-U bleibt (Fels) |
  | `curve_ramp_width` | 0,35 × B, 0,8–2,5 m | 0,35 × B | 1,5 m |
  | Falloff | **Angle 32°** | Angle 25° | Width 1,0 m |
  | Smooth Blending inner / outer | 0,3 / 0,8 m | 0,3 / 0,8 m | 0,3 / 0,5 m |
  | Blend Mode | Min | Min | Min |

### C.2 Lagen auf steilen Uferflächen

Die erste passende Klasse gilt, mit 4° weichem Übergang. Unter 20° gelten die Bänder aus A bzw. die Umgebung. Der
Uferstreifen bleibt vorn.

| Klasse | Neigung | Bedingung | Lagen (Prozent) |
|---|---|---|---|
| Fels-Wand | 45–90° | Wandhöhe ≥ 3 m oder anstehender Fels | Fels 45, Felsplatte 20, Moos 20, Geroell 15 |
| Erdanriss | 45–90° | Wandhöhe < 3 m | Erde 45, Moos 20, Lehm 15, Geroell 15, Fels 5 |
| Böschung steil | 32–45° | – | Erde 30, Moos 30, Geroell 25, Trockengras 10, Lehm 5 |
| Böschung locker | 20–32° | – | Geroell 25, Moos 25, Trockengras 20, Erde 15, Kies 15 |
| Nordseite / unter Bäumen | – | Normale nach Nord ± 60° | Moos +15 (von Trockengras, dann Erde) |

- **Schichtbänder (V17):** Maske = SmoothStep(38°, 45°, Neigung) × SmoothStep(3 m, 4 m, Wandhöhe) × [Fels + Felsplatte
  ≥ 50 %]. **In der Talkaskade unter 3 m Wandhöhe also aus**, ebenso im Kiesbett. Im Durchbruch und in der Bergrinne
  bleiben sie, dort sind es echte Felswände.
- Wandhöhe = Höhe der zusammenhängenden Böschung ≥ 30° über dem Spiegel, quer bis 6 m neben der Kante.

### C.3 Bewuchs an der Kante

Kante = Böschungsschulter (dort fällt die Neigung unter 20°). Nichts in Lippenzonen (`bachbett_regeln.json`).

| Element | Wo | Menge und Abstand | Netze (Inventar) |
|---|---|---|---|
| **überhängendes Gras** | Erd- und Rasenufer, nicht Fels, nicht Kiesbank | 60–80 % der Kantenlänge, alle 0,4–0,8 m, 0,15–0,35 m Überhang, 20–40° zum Wasser geneigt, Skala 0,8–1,3; Landschaftsgras an der Kante × 1,3 | `SM_grass_bush_01`–`04`, `SM_GrassyEmbankment_01/02` |
| **Moospolster** | Ufersteine und Böschung 0–1,2 m über dem Spiegel | 1 je 1,5–3 m Ufer in Gruppen zu 2–3; Nordseite × 2; 60 % der Steine ≥ 0,4 m mit Moos oben (ab 0,25 m über dem Spiegel) | `SM_MossClump_01/03/05`, `SM_moss_01/02`, `SM_MossyEmbankment_01/02` |
| **Farne** | nur schattig: Nordufer, Hangfuß oder Baum ≤ 15 m | Gruppen zu 2–5, alle 4–8 m, 0,5–2,5 m vom Wasser; offene Tundra höchstens 1 Gruppe je 15 m | `SM_Fern_01/02/04`, `SM_EagleFern_S_01/02` |
| **Wurzeln** | nur Erdanriss am Prallhang mit Baum/Strauch ≤ 6 m von der Kante | 1 je 3–6 m Anriss, 0,2–0,6 m unter der Kante, 0,2–0,6 m herausragend; ohne Baum: Grasbüschel statt Wurzel | `SM_Pine_roots_03/04`, `SM_crooked_root_01/04`, `SM_ForestRoots_01` |
| Kraut/Blüten | 1–3 m von der Kante | Flecken, nicht an der Wasserlinie | Lage `Kraut` bzw. eure Tundra-Blüten |
| frei | 0,3 m an der Wasserlinie | außer Moos | – |

### C.4 Steine

Größe = größte Ausdehnung; Einbettung = Anteil der Höhe im Boden. Lange Achse parallel zur Strömung (±20°), stromauf um
10–20° gekippt (Dachziegellage). Netze aus der Tundra-Palette (`gefaelle_regeln.json`).

| Ort | Größe | Abstand / Anzahl | Lage | Einbettung | Netze |
|---|---|---|---|---|---|
| **Prallhang-Fuß** | 0,6–1,4 m | alle 1,5–3 m, Gruppen zu 2–4, Lücken 3–6 m | Wasserkante −0,4 … +0,6 m | 35–55 % | `SM_TundraMossyBoulder_01`, `SM_NordicBoulder_01`, `SM_mountain_rock_big_02_1/2/3` |
| **Stufe (Widerlager)** | max(0,8; 0,6 × Stufenhöhe + 0,4) bis 1,8 m | 1–2 je Lippenende | Mitte 0,2–0,6 m außerhalb der Kante, ins Ufer gedrückt | 40–60 % | wie oben |
| Kolkrand unter der Stufe | 0,5–1,0 m | 1–3 | am Beckenrand | 30–50 % | wie oben |
| Gerade Ufer | 0,3–0,6 m | 3–6 je 10 m Ufer | −0,3 … +1,0 m | 30–50 % | `SM_mountain_rock_small_01_1/2/3`, `SM_TundraRockyGround_01` |
| Gleithang/Kiesbank | Kiespacks; einzelne 0,3–0,5 m | 2–4 Packs und 1 Stein je 10 m | Bank | – | `SM_SmallStonesPack_01/03/06/13` |

- Mindestlücke zwischen zwei Steinen 0,3 m; die Kerbe des Hauptstrahls an jeder Lippe bleibt frei.
- Moos oben ab 0,3 m über dem Spiegel, dunkler Nassrand 0,05–0,15 m über dem Spiegel.
- Steine ≥ 0,4 m im Wasser oder ≤ 1 m daneben als SWR-Hindernis eintragen, dann Reset + Bake (16f).
- **Richtwert Talkaskade je 10 m (beide Ufer):** 2–4 Blöcke und 6–10 Kopfsteine. Das passt zu unserer Roh-Ebene (Ufer
  0,5–1,4 m, Einbettung 0,30–0,45; `bachbett_regeln.json` → `roh.felsen`).

### C.5 Umsetzung

- **Ferats Werkzeug:** [`bachbett_ufer_regeln.json`](bachbett_ufer_regeln.json) lesen. Teile: `A_altbett`,
  `C_ufer.profil` (mit `kasten_verbot`, `boeschung_zuruecklegen`, `water_plugin`), `C_ufer.lagen_steil`
  (mit `schichtbaender`), `C_ufer.bewuchs_kante`, `C_ufer.steine`, `C_ufer.pruefung`.
- **Referenz:** [`skripte/ufer_regeln/ufer_regeln.py`](skripte/ufer_regeln/ufer_regeln.py) mit `altbett_mischung`,
  `gras_dichte_faktor`, `steil_mischung`, `schichtband_maske`, `kasten_hoehe`, `boeschung_zuruecklegen`. Aufruf
  `python -I recherche/antworten/skripte/ufer_regeln/ufer_regeln.py` → Selbsttest **0 FEHLER** (Summen, Lagen-Namen,
  Übergänge, Kasten-Erkennung, Zurücklegen hebt nie an).
- **Unser Planer:** keine Änderung am Gelände (siehe C.0) und kein „Uferprofil“ im `bachbett`-Modul. Die Lagen- und
  Bewuchsregeln könnten später als Ergänzung für die Gefälle- und Roh-Läufe dienen (Rückfrage 4).
- **Referenzen** [Gestaltung, Bildeindruck, keine Messung]:
  - Alpen: Kies- und Blockufer mit 30–35° Böschungen, Rasenkanten mit Wurzeln an Prallhängen.
  - Karpaten/Tatra: moosige Blöcke, viel Holz.
  - Witcher 3: Velen mit Erdufern, Wurzeln, überhängendem Gras und dunklem, nassem Saum; Skellige mit Blockufern, Moos und
    Felsplatten.
  - RDR2 (Ambarino, Grizzlies): klares Wasser über runden Steinen, Gras bis an die Kante, halb eingegrabene Blöcke.

---

## Testreihe (lokal, Talkaskade TK1 t430 / t500 / t550, dazu ein Becken ≥ 1 m)

| Nr | Was | Erwartung / Messung | Backen |
|---|---|---|---|
| **T0** Zerlegung (10 min) | a) Glas: `Absorption` 100 000 (alle drei), Scattering A 0, `Foam Opacity` 0, `ELD_Schaum_Deckkraft` 0 → b) Absorption heute → c) Scattering A 0,1 → d) `Foam Opacity` 0,5 → e) ELD-Schaum heute → f) Refraction 1,0 / 1,15 | a) wie „ohne Wasser“, nur Glanz und Brechung. Der Schritt mit dem größten Sprung zu Gold bzw. Milch ist die Ursache; erwartet c) und e). Zeigt auch, ob A je cm wirkt (c sehr milchig bei 0,5 m) | nein |
| **T1** Varianten | V1, V2, V3 aus B.3 je als Kopie von `MI_EL_SWR_Klar` | Grund bei 1 m deutlich (Kontrast Stein/Kies im Bild ≥ 50 % von trocken, Pipette); kein Goldton; tiefes Becken leicht grün; Flecken nur an Stufen | nein |
| T2 Grund | im Bett unter Wasser Geroell vor Kies, 5–10 % `Algen` in ruhigen Becken, Nassfarbe × 0,6 | Gold vom Grund weg | nein (Lagen) |
| T3 Tempo | `Velocity Debug` = 1 in WCBS, mit `UseBakedSim` False und True | Becken < 50, Rinnen 100–250, Stufenfuß > 300 cm/s; welche Quelle feiner ist | nein |
| T4 FoamAtten | Kopie `…Schaum9` mit Knotenplan B.4, Start 250/450 cm/s, Scattering 150/400 × 5 | Schaum und Milch nur an Stufen | nein |
| T5 Ufer | Kasten-Prüfung auf p2-Querschnitten (alle 2 m), Böschung zurücklegen, Lagen C.2, Schichtband-Maske, Kante C.3, Steine C.4 | 0 Kästen, 0 Schichtband unter 3 m; Bild TK1 t500 schräg wie `tk_mit_ohne_wasser.jpg` Zeile 2 | **ja** (Reset + Bake nach Gelände und Hindernissen) |
| T6 Altbett | Bänder A.2 über `s38 lagen` | kein Kiesband > 8 m breit außerhalb 0–6 m; Draufsicht wie `altwasser_vorher_nachher.png` | nein |

---

## Was lokal zu tun ist

Code und Regeln: Commit **`47a3aeb`** holen.

1. **Material (sofort, ohne Backen):**
   - T0 an TK1 t430/t500 (Abschnitt Testreihe);
   - dann V1, V2 und V3 als Kopien von `MI_EL_SWR_Klar`, Werte aus B.3;
   - Bilder wie `tk_mit_ohne_wasser.jpg` und ein Becken ≥ 1 m.
2. **Strömung lesen:** `Velocity Debug` = 1 in WCBS (T3). Wenn die Werte plausibel sind, Master-Kopie
   `M_Eldarien_Wasser_Schaum9` mit dem Knotenplan B.4 bauen und `MI_EL_SWR_Klar` umhängen. Sonst die Steilheits-Maske.
3. **Altbett-Lagen (Teil A):**
   - Maske = die vier ersetzten Läufe aus `wasser_welt.json`/`baeche_alle.json`, halbe Breite + 3 m;
   - darin die Bänder aus `bachbett_ufer_regeln.json` → `A_altbett` über `s38 lagen`;
   - Gras-Dichten mit `gras_dichte_faktor`;
   - Draufsicht wie `altwasser_vorher_nachher.png`.
4. **Talkaskade-Ufer (Teil C):**
   - Querschnitte alle 2 m;
   - `kasten_hoehe` > 0,6 m → `boeschung_zuruecklegen` (32°, nur abtragen);
   - Lagen nach `lagen_steil`, Schichtband-Maske, Bewuchs an der Kante (C.3), Steine (C.4);
   - Danach **SWR Reset + Bake** (Gelände und Hindernisse geändert).
   - Referenz-Funktionen in `skripte/ufer_regeln/ufer_regeln.py`; Selbsttest
     `python -I recherche/antworten/skripte/ufer_regeln/ufer_regeln.py`.
5. **Planer lokal neu (1 m):**
   - `gefaelle_plan.py --alle`, `bachbett_roh.py`, `fluss_sim_export.py` und die Prüfer.
   - Die C2-Läufe stehen nur noch im Log („Ersetzt …“).
   - Alte Ordner `gefaelle/F_ERLENBACH_1V_C2`, `…_2_C2` und `bachbett_roh/<C2-Läufe>` werden nicht mehr gelesen
     (HINWEIS); sie können weg.
   - Neu backen: `F_ERLENBACH` (beginnt jetzt am C3-Lauf, p2 ist sein lokaler Zufluss), `B_R2_K10_TUNDRA_01`, `_02`.
   - Ferats eigene p2-SWR und `C2_Wasserzone` (4096) bleiben, wie sie sind.
6. **Nicht anfassen:** Sehens-Ausgaben, alle anderen Gefälle-Pläne und Roh-Läufe (byte-gleich).

---

## Quellen

- Projekt: `auftraege/16h-…`, Bilder `bilder/swr_p2/*`, `mi_el_swr_klar_parameter.txt`, `vorlagen/daten/material_parameter.json`,
  `vorlagen/FORMAT.md` §2 (Lagen), `skripte/sehens_lib/bachbett_regeln.json`, `skripte/gefaelle/gefaelle_regeln.json`
  (Tundra-Netze), `vorlagen/daten/inventar.json` (Netznamen), Antworten 16a (b1, B4/B5), 16b, 16e, 16f (§3.2, §5) und 16f-Rückfrage
  (§3–4), 16g-Nachtrag (Wasser-Info), 16c Nachträge 2–4.
- [Single Layer Water Shading Model (Epic, Suchauszug)](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine)
  – Eingänge Scattering/Absorption Coefficients, PhaseG, Color Scale Behind Water; Opacity regelt Volumen gegen Reflexion.
- [Epic-Forum: Actually realistic water shader](https://forums.unrealengine.com/t/actually-realistic-water-shader/141661) –
  Beer-Lambert, Extinktion = Streuung + Absorption; Werte „sollten recht klein sein“ (Suchauszug).
- [Golden Blue: Single Layer Water](https://goldenxblue.github.io/post/single-layer-water/),
  [Jettelly: Water shader study](https://jettelly.com/blog/a-water-shader-study-in-unreal-engine-using-single-layer-water) –
  Streuung/Absorption als Klarheitsregler (Suchauszug).
- [BasicShallowWaterSubsystem (Python-Doku, Suchauszug)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/BasicShallowWaterSubsystem)
  – `water_info_texture`, `velocity_rt`.
- [UWaterEditorSettings (Suchauszug)](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterEditor/UWaterEditorSettings)
  – `MaxWaterVelocityAndHeightTextureSize` (kombinierte Geschwindigkeits-/Höhentextur je Water Zone).
- [FWaterInfoTextureRenderingParams (Suchauszug)](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/FSceneView/FWaterInfoTextureRenderingParams).
- [Wikipedia: Angle of repose](https://en.wikipedia.org/wiki/Angle_of_repose) – Kies mit Sand 25–30°, gebrochener
  Schotter 45°.
- [Pollen-Bankhead et al. 2009 (Ufersicherung durch Wurzeln)](https://www.engr.colostate.edu/~pierre/ce_old/classes/ce717/Hillslope%20stability/Pollen-Bankhead%20et%20al.%20Streambank%20destabilization%20and%20invasive%20removal%202009.pdf),
  [USDA ARS: Streambanks](https://agresearchmag.ars.usda.gov/2011/feb/streambanks) – Wurzeln wirken nur oberhalb der
  Bruchfläche; Unterschneidung und Kragenbruch an Rasenufern.
- Montgomery & Buffington 1997 (Gerinnetypen), wie 16f.
- Nicht gefunden: der Name der Material-Funktion für die Wasser-Info (`SampleWaterInfo`?), die Kanalbelegung der Strömung
  und Epics Verrechnung von `Scattering` A und `Water Albedo` (Epic-Seiten gesperrt; nur Suchauszüge ohne diese Details).

## Rückfragen

1. **T0-Ergebnis:** Welche Stufe (b–f) bringt Gold bzw. Milch? Wirkt Scattering A je cm? Dann trage ich die Werte für V1–V3 als
   Regel in eine Material-Tabelle ein (wie `wasserfarben.json`).
2. **Strömung im Master:** Gibt `Velocity Debug` in WCBS Werte in cm/s aus, und reicht die Wasser-Info (4096) für die Stufen
   der Talkaskade? Sonst die Steilheits-Maske statt FoamAtten.
3. **p2-Querschnitte:** Kann Ferats Werkzeug je 2 m einen Querschnitt (d, z) ausgeben? Dann rechne ich die Kasten-Statistik
   und die nötige Zurücklegung je Abschnitt vor.
4. **Uferregeln auch für unsere Läufe?** Lagen C.2 und Bewuchs C.3 könnten als Ergänzung ins `bachbett`-Modul (Gefälle- und
   Roh-Läufe). Gewünscht?
5. **Mündung p2:** Wo genau mündet p2 in den C3-Lauf (Punkt, s auf `F_ERLENBACH_2_C3`)? Dann setzt die Roh-Ebene dort eine
   Schutzzone, und `F_ERLENBACH` bekommt p2 als benannten Zufluss.
