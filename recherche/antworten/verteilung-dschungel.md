# Verteilung Biomgruppe 7: Dschungel inkl. Karst-Kalktürme (Guilin / Ha Long, Yakushima, Azoren-Lorbeerwald)

**Auftrag 11, Teil B7.** Biom `dschungel`, Foliage-Präfix `FT_EL_DS_`, Ordner `/Game/Eldarien/Welt/Foliage/Dschungel`. Stand 2026-10-10.
Lieferung: dieser Bericht, `skripte/dschungel_regeln.json` (Korrektur Runde 1: 18 Planer-Klassen, dazu `mittelschicht_overrides` mit
12 Klassen-Paletten + 3 Zusatzklassen für Teil D, `felsgruppen_overrides` und `spuren_overrides` für Teil C/D; alle Pfade gegen
`daten/netze.csv` geprüft, 0 fehlend), `skripte/dschungel_plan.py` (Planer, FORMAT §3/§5, Konventionen §1–§5).
**Alles UNGETESTET MIT ECHTDATEN** – in der Cloud nur syntaxgeprüft und mit synthetischen Rastern (H6, §5) rauchgetestet; der
Rauchtest wurde nach dem Sitzungsabbruch wiederholt, zwei Fehler behoben (Wandkanten, Budget) und das Ergebnis nachgeprüft.
Web-Quellen konnten nur als Suchmaschinen-Auszüge gelesen werden; solche Belege sind mit **[Suchauszug]** markiert, Zahlen ohne
Beleg als **Richtwert**. Quellenliste am Ende von §1.

Betroffene Felder: **H6** (dschungel 100 %, Laub 59, Fels 12, Kraut 8, Schlamm 8, Moos 7), **I6** (100 %, Sand 33, Laub 26, Fels 8, Moos 5,
steil 31 %), **G6** (97 %, Laub 33, Fels 13, Schlamm 9, Wasser 1,4 %), **G7/H7/I7** (73–76 %, Rest aue, 10–22 % Land), Anteile in **G5**
(22 %, Heide dominant), **I5** (21 %, Bergwald), **H5** (12 %, Sumpf). Karst-Kalktürme laut Auftrag in G6, H6, I6, I7 (`felder[..].karst`).
Der Planer bebaut nur Zellen mit Biom `dschungel` (`eigner.r8` + `welt.json`, Kennzahl 0 = `aue`) plus einen 30-m-Saum mit linear
fallender Dichte; bei weniger als 2 % Dschungel im Fenster schreibt er einen leeren `plan.json` (Abschnitt **Korrektur Runde 1**; die
Runde-0-Regeln mit Grundfaktoren für Nachbarbiome und `feld_biom_fallback` sind gestrichen).

## Korrektur Runde 1 (10.10.2026, nach `auftraege/verteilung-korrektur-runde1.md` und `verteilung-KONVENTIONEN.md`)

**Anlass (Echtdaten-Test 10.10. 15:30).** Der Dschungel-Planer lief ohne Absturz, setzte aber Instanzen in Feldern ohne Dschungel:
A5 (kueste/bergwald/aue) **1 038**, G4 (elfenwald 76 %, heide 22 %) **15 590**, E1 (gletscher) 0, C6 (lava 99 %) **2 783**. Ursache war
die Biom-Logik aus Runde 0. Nachbarbiome bekamen nach dem 30-m-Saum einen Grundfaktor (aue/bergwald 0,3, elfenwald 0,25, kueste 0,2,
sumpf 0,45), und Kennzahl 0 wurde über `feld_biom_fallback` gelesen. Felder, die in dieser Tabelle fehlen, fielen damit auf `aue` mit Faktor 0,3 zurück. Daher kamen C6 und G4 zu
ihren Instanzen, obwohl es dort kaum Dschungel-Zellen gibt.

### Änderungen

| Punkt | Runde 0 | Korrektur Runde 1 |
|---|---|---|
| Biom je Zelle (§1) | Kennzahl 0 → dominantes Feldbiom (`feld_biom_fallback`) | Kennzahl 0 und Kennzahlen ohne erkennbares Rezept → **`aue`**, Vulkan/Lava-Rezept → `lava`; nur wenn `eigner.r8`/`welt.json` fehlen: dominantes Feldbiom aus `daten/biome_je_feld.json` (Hinweis im Log). `feld_biom_fallback` und `biom_faktor` sind gestrichen |
| Zuständigkeit (§1) | Dschungel 1,0, Nachbarbiome Grundfaktor 0,2–0,45 überall | `zustaendigkeit.biome_eigen = ["dschungel"]`. Nur eigene Zellen plus **30-m-Saum, linear 1 → 0** (Distanztransformation über Jump-Flooding, NumPy). Fremde Zellen weiter weg bekommen 0 |
| Leerplan (§1) | – | Eigenanteil im Fenster (Feld + 64 m) **< 2 %** → `plan.json` mit `instanzen: 0`, `dateien: {}`, `entfernen: ""`, alte `.f32` gelöscht, eine Logzeile |
| plan.json (§2) | – | neu: `biome_fenster` (Anteile, absteigend), `zellen_zustaendig` (Feldzellen mit Faktor > 0), `biome_eigen`, `kollision_anzahl`; in `statistik` zusätzlich `anteil_eigen_fenster`, `biom_quelle`, `saum_m` |
| Budget (§3) | proportionale Hash-Ausdünnung. Weil die Faktoren mit `min` statt multiplikativ verknüpft waren, blieb im Rauchtest 3 005 > 3 000 Kollision stehen | Faktoren multiplizieren sich, danach **exakte Kappung** (`kappe`): Kollision ≤ `kollision_je_feld` 3 000, gesamt ≤ `hart_instanzen_je_feld` 60 000; Ziel 50 000; je Schicht Boden 22 000 / Mittel 12 000 / Baum 9 000 / Wasserkante 5 000; jede Ausdünnung als `WARNUNG` in Log und `hinweise`, Kleinzeug-Hinweis „Landschafts-Gras übernimmt“ |
| Lianen-Satelliten | entstanden vor der Baum-Ausdünnung, an gestrichenen Bäumen blieben dadurch Lianen ohne Stamm stehen | werden erst **nach** dem Budget an den verbliebenen Laubbäumen erzeugt (geprüft: max. 1,60 m zum nächsten eigenen Laubbaum) |
| Ebenen (§4) | Schicht 1 mit 15 Klassen (Farne, Stauden, Strauch, Jungpalme, Totholz, Wurzel, Gras, Karstplatte …), Pilz/Ast in Schicht 0 | Schicht 1 nur noch **Dschungel-Sonderformen**: `liane_stamm` (Epiphyten-/Lianen-Ersatz an Stämmen eigener Laubbäume), `liane_wand` (Kletterpflanzen in Karstspalten/Steilwänden 40–78°), `moos_polster` (aus Schicht 0 hierher, kletterfähig bis 75°, Karstfuß 2-fach). Generische Klassen → `mittelschicht_overrides`, `karstplatte` → `felsgruppen_overrides.karstplatte` (Teil C hat dieselben Netze schon als `geroell_platte`). Schicht 0 (Streu, Bodendecker, Zweige, Keimlinge, Blüteninseln), 2 (Bäume, Palmen) und 5 (Wasserkante) bleiben |
| entfernen | `sm_fern_01a,sm_fern_02a,sm_vines_01a` | B7 entfernt nur noch `sm_vines_01a` (setzt Lianen selbst); Farn-Entfernung steht als `mittelschicht_overrides.entfernen_je_feld`, weil jetzt Teil D die Farne setzt |
| Blickziele | Karstturm, Wasserfall und Tempelruine auf jeder Feldzelle möglich | nur auf Dschungel-Zellen |
| Logs (§5) | Umlaute, „→“, „…“ in `print()` | alle Logs über `ascii_text()` nur ASCII (ae/oe/ue/ss, `->`, `...`), geprüft: 0 Nicht-ASCII-Bytes; fehlende `hoehe.f32`/Regeldatei/unbekanntes Feld → `FEHLER: …`, **Exit-Code 2** |

### Override-Schema `mittelschicht_overrides` (in `dschungel_regeln.json`, für `mittelschicht_plan.py`)

```
"mittelschicht_overrides": {
  "biom": "dschungel",
  "alias":   {"totholz_liegend": "totholz", "totholz_stumpf": "stumpf", "totholz_ast": "ast"},   # Konventionsname → heutiger Klassenname in mittelschicht_regeln.json
  "palette": {klasse: [Unreal-Pfade]},       # ersetzt die Netzliste von mittelschicht_regeln.json["biome"]["dschungel"][klasse]
  "faktor":  {klasse: float},                # multipliziert deren "dichte" [licht, schatten]; 0 = Klasse aus
  "parameter": {klasse: {schluessel: wert}}, # optional: einzelne Klassenschlüssel überschreiben (massstab, eingraben_cm, kippen, sichtweite, kollision, laengs_hang, hang_max)
  "zusatzklassen": {name: Klassenblock},     # vollständige Klassen im mittelschicht-Schema (netze, dichte [licht, schatten], gruppe, radius_m, massstab, eingraben_cm, kippen,
                                             # sichtweite, kollision, saum, feuchte, hang_max, hoehe_max_m, lichtungsrand, laengs_hang, an_baum) + farbe + herkunft_b7
  "entfernen_je_feld": {feld: "praefix,…"}   # Witcher-Farne, die Teil D beim Setzen der Mittelschicht entfernt (G6, H6, I6, G7, H7, I7)
}
```

Die verbindliche Dschungel-Palette aus §3 ist damit maschinenlesbar. Alle 75 Pfade (59 Palette, 16 Zusatzklassen) wurden gegen `vorlagen/daten/netze.csv` geprüft, es fehlen 0.

| Klasse | Palette (Netze) | Faktor | Parameter / Begründung |
|---|---|---|---|
| farn | Megascans Fern 01/02/04/05, EagleFern M_01/S_01/S_02, SilverLadyFern 01/02, BeechFern 04/09, `SM_Fern_01a/02a` (13) | 1,3 | Maßstab 0,9–1,5, kippen 0,5, Hang ≤ 45°; farnreicher Unterwuchs |
| strauch | nur `SM_Bush_01a` | 0,6 | Maßstab 0,45–0,8; Unterholz ist Farn/Staude |
| jungbaum | `SM_Palm_01_07…12_G` (6) – keine Hainbuchen-Schösslinge | 1,5 | Maßstab 0,8–1,4, Sicht 150 m (Palms_Pack ohne Nanite) |
| hochstaude | Crownbeard 03/04/07/08, Pestwurz 01–03 | 0,6 | weil `staudenflur` als Zusatzklasse kommt |
| grasbueschel | KikuyuGrass 01/04/05/06/07/10 | 0,6 | nur Lichtungen/Karstgipfel |
| totholz_liegend | MossyTree_01, LargeFallenTree_02, OldFallenTree_01, FallenTreeAssembly_01 | 1,0 | eingraben 28 cm, kippen 0,9, **Kollision**, längs Hang, Sicht 500 m |
| totholz_stumpf | RottenTreeStump 01/02, TreeStump_01, BrokenStump_01 | 1,0 | eingraben 18 cm, Sicht 400 m |
| totholz_ast | OldTreeBranch 01/04/06, BrokenTreeBranch_01, OakBranch_01 | 0,8 | eingraben 6 cm, längs Hang |
| wurzel | MossyForestRoots 01–03, ForestRoots_01 | 1,2 | eingraben 10 cm, Normale voll |
| kletter | `SM_Vines_01a`, Ivy 11/12/17/18/21/25 | 0,5 | B7 bedient eigene Laubbäume (`liane_stamm`) und Wände (`liane_wand`), Teil D die Bestand-/Witcher-Bäume |
| pilz | Meadow `SM_mushroom_01/02` | 1,0 | bis tropische Pilze importiert sind |
| beere | – | 0 | keine Beerensträucher im Dschungel |
| **Zusatz** `riesenfarn_insel` | Fern 01/02/04/05, `SM_Fern_01a` | dichte [0,006 licht, 0,03 schatten] | Gruppen 3–12 in 4 m, Maßstab 1,1–1,9, Lichtungsrand 0,4 (B7 Runde 0: 0,045/m², Farninseln 22 m, Karstfuß 1,7) |
| **Zusatz** `staudenflur` | Crownbeard 03/04/07/08, Pestwurz 01/02, Holunder 05/07 | [0,02, 0,003] | Gruppen 3–8, Lichtungsrand 2,5 (Lichtungs-Staudenflur) |
| **Zusatz** `bananen_ersatz` | Holunder 08/09, Pestwurz 03 (×1,5–2,4) | [0,006, 0,003] | Gruppen 1–3, Feuchte 0,6–1,8 (B7: nur 0–40 m vom Wasser), bis Megascans Banana importiert ist |

Die bisherigen B7-Parameter (Lichtkurve, Karstfaktoren, Kern-Dichte) stehen je Zusatzklasse unter `herkunft_b7`, damit nichts verloren
geht. `felsgruppen_overrides` (Karsttürme als Akteure, Moosblöcke, Geröllplatten, neu `karstplatte` mit Dichte 0,004, Fuß 3,0, Gipfel 1,5)
und `spuren_overrides` (Tempelruine, Pfad; `um_ruine.riesenfarn` → `riesenfarn_insel`) bleiben erhalten.

### Rauchtest Korrektur Runde 1 (synthetisch, Raster neu erzeugt, danach gelöscht)

Synthetische Produktionswurzel im Scratchpad. `hoehe.f32` hat volle Größe (memmap) mit zwei Karsttürmen (110/80 m) in H6, einem 2-m-Bach, einem Weg und einem Ort.
`eigner.r8`/`welt.json`: 5 = dschungel, 7 = elfenwald, 8 = heide, 0 = Weltgelände. H6 ist Dschungel mit einer Weltgelände-Ecke (→ aue, 5 %),
G4 hat nur elfenwald/heide, G5 ist im Westen heide und im Osten dschungel. Dazu `lage_*.r8`, `bestand/H6` (300 Bäume), `daten/netze.csv` und `biome_je_feld.json`.
Aufruf `python -I -X utf8 dschungel_plan.py H6 G4 G5 --bild`:

| Feld | Instanzen | Kollision | Schichten Baum / Mittel / Boden / Wasser | biome_fenster | zellen_zustaendig | Zeit |
|---|---|---|---|---|---|---|
| H6 (eigene Zellen) | **30 343** | 2 690 | 8 330 / 4 047 / 17 715 / 251 | dschungel 0,949, aue 0,051 | 990 479 | 15 s |
| G4 (elfenwald/heide) | **0** (Leerplan) | 0 | – | elfenwald 0,862, heide 0,138 | 0 | < 1 s |
| G5 (Mischfeld, Saum) | **13 568** | 1 226 | 4 050 / 1 728 / 7 790 / 0 | heide 0,546, dschungel 0,414, elfenwald 0,041 | 452 886 | 9 s |

Geprüft wurde Folgendes:
- **Schlüssel:** Alle Pflichtschlüssel (FORMAT §3 und Konventionen §2) sind vorhanden. `instanzen` ist gleich der Summe der `.f32`, `kollision_anzahl` ist gleich der Zahl der Instanzen mit `kollision=true`, und jede Datei hat `ebene`.
- **Zuständigkeit:** Außerhalb von Dschungel-Zellen liegen in H6 139 Instanzen (höchstens 25 m entfernt) und in G5 869 (höchstens 29 m entfernt). Im Westsaum von G5 stehen innen 219 Instanzen je 10-m-Band, außen 166 / 95 / 38 in 0–10 / 10–20 / 20–30 m und 0 ab 30 m. Die Dichte fällt also linear.
- **Determinismus:** Bei zwei Läufen sind die MD5 aller `.f32` gleich, und `plan.json` ist bis auf `stand`/`laufzeit_s` identisch.
- **Budget mit `--faktor 3`:** 40 656 Instanzen, davon 2 988 mit Kollision. Die Ausdünnung steht als WARNUNG im Log.
- **Harte Kappung:** Mit Testregeln (Kollision 1 000, gesamt 20 000) ergeben sich exakt 1 000 / 20 000 Instanzen. Gestrichen wurden zuerst `laub_mittel` bzw. Keimlinge.
- **Fallback ohne `eigner.r8`:** G4 wird über `biome_je_feld` als elfenwald gelesen und bekommt einen Leerplan. H6 wird als dschungel gelesen (31 225 Instanzen), mit Hinweis im Log.
- **Fehlerfälle:** Fehlende `hoehe.f32` und ein unbekanntes Feld (K9) enden mit Exit-Code 2 und einer `FEHLER`-Zeile.
- **Logs:** Sie enthalten 0 Nicht-ASCII-Bytes. `py_compile` und pyflakes sind sauber (nur der optionale numba-Import ist ungenutzt).

Der Wert für H6 ist nicht 1:1 mit Runde 0 vergleichbar (54 932, anderes synthetisches Raster). Der Rückgang kommt vor allem aus der Mittelschicht:
23 944 → 4 047, weil Farne, Stauden, Totholz und Gras jetzt Teil D setzt.

**Erwartung mit Echtdaten** (`erwartung_je_feld`):
- A5, G4, E1 und C6 → **0** (Leerplan), weil `biome_je_feld` dort keinen Dschungel zeigt. Dschungel-Zellen aus Nachbarfeldern im 64-m-Rand liegen unter 2 %.
- H6 30 000–45 000, G6 25 000–42 000, I6 18 000–35 000.
- G7/H7/I7 3 000–11 000.
- G5/I5/H5 2 000–10 000, nur auf ihren Dschungel-Zellen plus Saum.

**Offen für Echtdaten:**
- **Kennzahl 0:** Sind die Dschungelflächen in `eigner.r8` als Kennzahl 0 (Weltgelände) kodiert, liest der Planer sie nach Konvention als `aue`, und H6 bleibt fast leer. `biome_je_feld.json` meldet für H6 100 % dschungel, die Kacheln sollten also das Rezept `dschungel` tragen. Das bitte beim ersten Lauf an `biome_fenster` prüfen.
- **Teil D:** Teil D muss `mittelschicht_overrides` lesen, bis dahin fehlen im Dschungel die Farne/Stauden der Runde 0.

## 1. Referenzanalyse: Was einen Fantasy-Dschungel mit Kalktürmen zwischen Boden und Krone füllt

**Karst-Dschungel Guilin / Yangshuo (Fenglin, „Turmkarst“).** Die Türme bestehen aus massivem Kalk mit **nahezu senkrechten Flanken,
30–80 m hoch** in der Zentralebene; isolierte Hügel stehen auf einer flachen, sedimentbedeckten Kalkebene (Peak-Forest-Plain,
~800 km²), Turmkarst macht 47 % der Guilin-Karstfläche aus **[Suchauszug: Wikipedia „Li River“, Huang (UW-Milwaukee-Dissertation),
guilindeeptour]**. Vegetation: immergrün, subtropisch, Wald und Bambus auf den Hängen, Ackerland und Dörfer in der Ebene **[Suchauszug:
GeoExpro, factsanddetails]**. Für Eldarien: der Turm ist **kahl an der Wand**, bewachsen an **Fuß, Spalte und Gipfel** – genau diese vier
Karstlagen unterscheidet der Planer (§2.4). Die flache Ebene zwischen den Türmen ist offen oder bewirtschaftet: Lichtungen (16 %),
Tempel-/Pfadspuren (Teil D) und Reisfeld-Ersatz (Schlamm-Lagen, Stauden) gehören dorthin, nicht geschlossener Wald.

**Ha Long Bay / Cat Ba (Kalk-Inselkarst).** Die Kalkinseln sind „sparsely tree-covered“; Primärwald steht auf den größeren, weniger steilen
Inseln, auf den Steilkalk-Inseln nur dünn **[Suchauszug: World-Heritage-Datasheet]**. Endemiten wachsen „on mountain slopes, cliffs,
mountain peaks, cave entrances or rock crevices“: *Chirita* „everywhere on exposed limestone rocks“, *Cycas tropophylla*, Palmen
(*Livistona halongensis*), *Schefflera*, Orchideen (*Paphiopedilum*); die Vegetation wirkt teils trockenheitsangepasst (*Euphorbia
antiquorum*) **[Suchauszug: halongbay.com.vn; Gardens' Bulletin Singapore 52 (2000); vietnam.travel]**. Übertragen: die Kletterklassen
(`liane_wand`, `farn_klein`, `moos_polster`) besetzen Spalten 40–78°, am Gipfel stehen Sträucher und Grasbüschel 1,8-fach, Jungpalmen
1,2-fach (Faktoren `karst.gipfel`), und die Wand selbst bleibt leer (Faktor 0).

**Yakushima, Shiratani Unsuikyō (Moosurwald).** Hyperhumid (Jahresniederschlag > 8 m), Moose und Farne dominieren den Boden, überziehen
Blöcke, Stämme, Wurzelteller und **jeden liegenden Stamm**; Sämlinge keimen auf Nurse-Logs; Epiphytenfarne an den Stämmen; „hunderte
Moosarten“ (nicht gegen eine Artenliste geprüft) **[Suchauszug: japanjourneys.jp, 37framesphotographyblog, world-natural-heritage.jp]**.
Daraus: liegende Moosstämme erhalten 4–9 Moospolster-Satelliten im Radius 0,4–2,6 m, Karstplatten 2–5, Stümpfe 2–6 Pilze; Wurzelteller
(`SM_MossyForestRoots_*`) steigen mit Beschattung von 0,1 auf 1,0; Moospolster dürfen bis 75° klettern (Fuß-Faktor 2,0, Spalte 1,0,
Wand 0,4). Eine eigene Moos-Auflage auf den Türmen kommt aus dem Material (WorldAlignedBlend), nicht aus Zusatznetzen (§2.5).

**Azoren-Laurisilva („Nebelwald“).** Dichte, „nahezu undurchdringliche“, strukturell komplexe Kronen aus *Laurus azorica*, *Ilex perado*,
*Juniperus brevifolia*, Bäume > 5 m, wo erhalten > 10 m; **mehr als sieben Straten**, weil viele Individuen als Epiphyten oder auf toten
Stämmen wachsen; Moosteppich je nach Wasserhaushalt; ~80 Farnarten **[Suchauszug: Azores Central Islands field guide (ResearchGate);
EBSCO „Azores temperate mixed forests“]**. Madeira-Zahlen (*Laurus novocanariensis* ~20 m) gelten nicht direkt. Für Eldarien liefert das
die Begründung für den gemäßigt-subtropischen Mix: Hainbuchen-Keimlinge, Megascans-Farne und Efeu sind kein Stilbruch, solange sie unter
tropischen Kronen stehen – die Krone macht den Dschungel, nicht der Farn. Deshalb bleiben die 54 gemäßigten Füller von Teil D zulässig (§3).

**Witcher-Dichteprinzipien.** Die GDC-2014-Session „Landscape Creation and Rendering in REDengine 3“ (Gollent) beschreibt Vegetation, die
offline und in Echtzeit prozedural ohne Handplatzierung gesetzt wird; der Offline-Generator simuliert Wasseransammlung und Sonnenlicht je
Zelle, vergleicht den Schattenanteil mit dem Lichtbedarf jeder Art und skaliert; Handmalerei nur in Kampf-/Cutscene-Zonen **[Suchauszug:
GDC Vault 1020197; DualShockers-Bericht]**. Gras ist prozedural, Foliage-Qualität steuert Instanzzahl und Billboard-Übergang; SpeedTree +
Simplygon für LODs **[Suchauszug: targetfps/wccftech-Guides]**; die Witcher-4-Demo baut Wälder aus Nanite-Foliage und Fast Geometry
Streaming **[Suchauszug: tech.yahoo.com]**. Der Planer übernimmt den Kern: **Licht je Zelle** (Kronendach aus allen gesetzten Baum-Ebenen plus
eigener Baumschicht) entscheidet über Farn/Moos/Pilz (Schattenpflanzen) gegen Staude/Gras/Strauch (Lichtpflanzen) mit vier Stützstellen je
Klasse; Feuchte kommt aus Lagen (Schlamm, Moos, Kraut) und Wasserabstand. Die Bildkritik (`bildkritik-witcher-messlatte.md`) liefert
Lichtungen 15–25 % (hier 16 %, Wertrauschen 110 m), Größenstaffelung und „kaum ein Blick ohne Objekt in 0,5–3 m innerhalb 10 m“.

Quellen (alle nur als Suchauszug gelesen): [Li River – Wikipedia](https://en.wikipedia.org/wiki/Li_River) ·
[Huang, Spatial dimensions of tower karst (UWM)](https://minds.wisconsin.edu/bitstream/handle/1793/94010/Huang_uwm_0263D_10889.pdf?sequence=1&isAllowed=y) ·
[GeoExpro Guilin](https://geoexpro.com/crowns-of-nature-the-majestic-landscape-of-guilin/) ·
[Ha Long Bay Biodiversity](https://halongbay.com.vn/en/p/67-gia-tri-da-dang-sinh-hoc) ·
[Gardens' Bulletin Singapore 52: New plants from Ha Long Bay](https://www.nparks.gov.sg/sbg/research/publications/gardens-bulletin-singapore/-/media/sbg/gardens-bulletin/gbs_52_01_y2000/52_01_06_y2000_v52p1_gbs_pg185.pdf) ·
[Ha Long Bay World Heritage Datasheet](http://www.yichuans.me/datasheet/output/site/ha-long-bay/) ·
[Shiratani Unsuikyo (japanjourneys)](https://japanjourneys.jp/kagoshima/yakushima/hiking/shiratani-unsuikyo) ·
[Yakushima (world-natural-heritage.jp)](https://world-natural-heritage.jp/en/yakushima/) ·
[Azores Central Islands field guide](https://www.researchgate.net/publication/228973592_Azores_Central_Islands_vegetation_and_flora_field_guide) ·
[Azores temperate mixed forests (EBSCO)](https://www.ebsco.com/research-starters/environmental-sciences/azores-temperate-mixed-forests) ·
[GDC Vault: Landscape Creation and Rendering in REDengine 3](https://www.gdcvault.com/play/1020197/Landscape-Creation-and-Rendering-in) ·
[DualShockers GDC-Bericht](https://www.dualshockers.com/amazing-the-witcher-3-work-in-progress-screenshots-and-development-information-showcased-at-gdc/) ·
[Witcher 4 Tech-Demo (Yahoo)](https://tech.yahoo.com/gaming/articles/step-inside-witcher-4-infinite-154314015.html) ·
[Fab „Tropical Vegetation Assets“](https://www.fab.com/listings/5eee4638-6c25-489c-9b93-4fc720e2085f?lang=en) ·
[Fab „Subtropical flora“](https://www.fab.com/listings/deca6ad1-3cae-4cbb-9039-14b64c7c7028?lang=en) ·
[Quixel „Huge Banana Leaf“](https://quixel.com/megascans/home?category=decal&category=vegetation&search=plants&assetId=slpmfhp).

## 2. Regelwerk (`dschungel_regeln.json`)

Dichte je Zelle = Kern-Dichte · Biom · Lage · Licht · Höhenstufe · Karstlage · Hang · Gruppen-Rauschen · Sperren (Wasser, Weg 2,5/4 m,
Ort 5 m, Standorte, fremde Bäume 4 m groß / 1,2 m klein). Streuung über gejitterte Weltgitter (Zelle ≈ Mindestabstand), Zufall = Hash aus
Weltraster-Koordinate → deterministisch und nahtlos. Alle Zahlen stehen in der JSON; hier die Erklärung je Schicht.

### 2.1 Schicht 2 baum (Budget 9 000)

| Klasse | Netze | Dichte /m² | Zelle | Licht [0/0,33/0,67/1] | Hang max | Stufe Tal/Hang/Karst | Karst Fuß/Gipfel | Maßstab | Sicht (cm) | Koll. |
|---|---|---|---|---|---|---|---|---|---|---|
| emergent | `SM_Tree_Big_01b` (49 m) | 0,0005 | 36 m | 1/1/0,8/0,5 | 28° | 1/0,8/0 | 0,6/0 | 0,62–0,9 | 0 | ja |
| laubriese | `SM_Tree_Big_01a` (32 m), `SM_Tree_Small_01a` (20 m) | 0,0028 | 16 m | 1/1/0,85/0,55 | 32° | 1/1/0,3 | 0,35/0,3 | 0,8–1,15 | 0 | ja; 0–2 Lianen-Satelliten |
| laub_mittel | `SM_Tree_Medium_01a` (16 m) | 0,0035 | 10 m | 0,9/1/0,9/0,6 | 35° | 1/1,1/0,5 | 0,35/0,5 | 0,85–1,3 | 0 | ja; 0–1 Liane |
| palme_alt | `SM_Tree_Palm_01` (30 m, Bazaar) | 0,0018 | 18 m | 1/0,9/0,6/0,3 | 25° | 1/0,4/0 | 0,5/0 | 0,6–0,9 | 0 | ja |
| palme | `SM_Palm_01_01–06_G` (6,5–9,2 m, **kein Nanite**, 19–31 k Dreiecke) | 0,014 | 7 m | 1/1/0,7/0,35 | 30° | 1/0,7/0,15 | 0,4/0,4 | 0,9–1,4 | 0–28 000 | nein |
| palme_jung | `SM_Palm_01_07–09_G` (3,7–5,3 m, kein Nanite) | 0,02 | 5 m | 0,6/1/1/0,5 | 32° | 1/0,9/0,3 | 0,6/1,2 | 0,8–1,3 | 0–20 000 | nein |

Gruppen: `laubriesen` (Wertrauschen 90 m, Rest 0,25) und `palmenhain` (70 m, Rest 0,2) trennen Laubriesen-Kerne von Palmenhainen;
Lichtungen (16 %) haben Baumfaktor 0,12. Bäume werden groß → klein geplant; jede Klasse vergrößert das Kronendach für die folgenden
(Kronenradius 0,33 · Höhe · Maßstab, 1,5–14 m; Beschattung = 1 − exp(−1,4 · Kronenzahl), Gauß σ 4 m). Palms_Pack ohne Nanite → Sichtweite
280/200/150 m und keine Kollision (Stamm < 40 cm; Capsule im Foliage-Typ, falls nötig).

### 2.2 Schicht 1 mittel (Budget 24 000)

> **Stand Runde 0.** Seit Korrektur Runde 1 setzt B7 in Schicht 1 nur noch `liane_stamm`, `liane_wand` und `moos_polster` (Budget 12 000).
> Riesenfarn, Kleinfarn, Staude, Bananen-Ersatz, Strauch, Jungpalme, Totholz, Wurzel und Gras stehen als `mittelschicht_overrides` für
> Teil D, die Karstplatte steht als `felsgruppen_overrides.karstplatte` für Teil C. Die Tabelle bleibt als Herkunft der Parameter stehen.

| Klasse | Netze (Auszug) | Dichte /m² | Zelle | Licht | Hang max | Karst Fuß/Spalte/Gipfel | Maßstab | Eingraben | Sicht | Besonderes |
|---|---|---|---|---|---|---|---|---|---|---|
| riesenfarn | Megascans `SM_Fern_01/02/04/05`, `SM_Fern_01a` | 0,045 | 2 m | 0,25/0,7/1/1 | 38° | 1,7/0/0,5 | 1,1–1,9 | 4 cm | 140 m | Farninseln (Rauschen 22 m) |
| farn_klein | EagleFern M/S, SilverLadyFern, BeechFern, `SM_Fern_02a` | 0,045 | 1 m | 0,3/0,8/1/1 | 60° **kletter** | 1,4/0,5/0,6 | 0,9–1,5 | 3 cm | 100 m | Spaltenfarn |
| staude | Crownbeard 03/04/07/08, Pestwurz 01/02, Holunder 05/07 | 0,05 | 2 m | 1/1/0,6/0,2 | 36° | 0,8/0/1,0 | 1,0–1,6 | 3 cm | 120 m | Staudenflur (30 m) |
| bananen_ersatz | Holunder 08/09, Pestwurz 03 (×1,5–2,4) | 0,012 | 4 m | 0,9/1/0,7/0,3 | 30° | 1,2/0/0,3 | 1,5–2,4 | 4 cm | 200 m | nur 0–40 m vom Wasser |
| strauch | `SM_Bush_01a` (3,4 m) | 0,0035 | 8 m | 1/1/0,6/0,25 | 36° | 0,7/0/1,8 | 0,7–1,2 | 6 cm | 300 m | Gipfelgebüsch |
| jungpalme | `SM_Palm_01_10–12_G` (1,3–2,7 m, kein Nanite) | 0,02 | 3 m | 0,5/1/1/0,6 | 34° | 0,9/0/1,2 | 0,8–1,4 | 4 cm | 150 m | |
| stamm_moos | MossyTree, LargeFallenTree_02, OldFallenTree, FallenTreeAssembly | 0,0012 | 14 m | 0,4/0,8/1/1 | 30° | 1,3/0/0,4 | 0,9–1,3 | 28 cm | 500 m | **Kollision**, quer zum Hang ±25°, 4–9 Moospolster |
| stumpf | RottenTreeStump 01/02, TreeStump, BrokenStump | 0,0009 | 12 m | 0,5/0,9/1/1 | 32° | 1,0/0/0,5 | 0,9–1,3 | 18 cm | 400 m | 2–6 Pilze |
| wurzel | MossyForestRoots 01–03, ForestRoots | 0,004 | 6 m | 0,1/0,5/1/1 | 36° | 1,2/0/0,5 | 0,9–1,4 | 10 cm | 300 m | Normale voll |
| liane_stamm | `SM_Vines_01a`, Ivy 11/17/21/25 | nur Satellit | – | – | 78° | – | 0,9–1,6 | **−40 cm** (angehoben) | 150 m | 0,6–1,6 m um Laubriesen/Mittelbäume |
| liane_wand | `SM_Vines_01a`, Ivy 11/12/17/18 | 0,03 | 2 m | 1/1/0,9/0,7 | **40–78°** | 0,5/1,0/0,2 (Wand 1,0) | 0,9–1,7 | 5 cm | 150 m | Spaltenvegetation |
| karstplatte | LimestoneRocks2/3, MossyRocks 01/02, MossyForestRock_03 | 0,004 | 6 m | 1 | 34° | **3,0**/0/1,5 | 0,8–1,4 | 22 cm | 400 m | nur Karstfelder; 2–5 Moospolster |
| grasbueschel | KikuyuGrass 01/04/05/06/07/10 | 0,034 | 1 m | 1/0,9/0,4/0,1 | 38° | 0,6/0/1,8 | 0,9–1,5 | 3 cm | 90 m | Lichtungen, Gipfel |

Blick-Test (10-m-Umkreis ≈ 300 m²): im beschatteten Talboden summieren sich Riesenfarn (0,045·1,0) + Kleinfarn + Jungpalme (0,02) +
Wurzeln + Stämme/Stümpfe auf ≈ 0,09/m² Kernwert, nach Lagen-/Gruppenfaktoren real **5–9 Objekte je 100 m²** in 0,3–3 m Höhe (Rauchtest H6:
23 944 Mittelschicht-Instanzen auf 0,94 km² Dschungel = 2,5/100 m² im Feldmittel, in Farninseln 6–10). Lichtpflanzen stehen zu 39–47 % in
Beschattung < 0,33 (Flächenanteil 27 %), Schattenpflanzen zu 70–78 % in > 0,67 (Flächenanteil 60 %) – die Lichtsteuerung wirkt.

### 2.3 Schicht 0 boden (Budget 22 000) und Schicht 5 wasserkante (Budget 5 000)

| Klasse | Netze | Dichte /m² | Licht | Lagengruppe | Sicht | Hinweis |
|---|---|---|---|---|---|---|
| streu | DeadLeaves 01/12/13/14 | 0,012 | 0,4/0,8/1/1 | streu (Laub 1,3) | 70 m | Streuhaufen (Rauschen 12 m) |
| streu_klein | GroundCover 01–04/06 | 0,010 | 0,6/0,9/1/1 | streu | 50 m | |
| zweige | WoodenSticksAndTwigs 01/04/05/07, DryBranches 01/04/07 | 0,016 | 0,5/0,8/1/1 | streu | 60 m | Maßstab 1,2–2,2 |
| ast | OldTreeBranch 01/04/06, BrokenTreeBranch, OakBranch | 0,003 | 0,4/0,8/1/1 | streu | 250 m | quer zum Hang |
| pilz | Meadow `SM_mushroom_01/02` (kein Nanite, 470 Dreiecke) | 0,004 + Stumpf-Satelliten | 0,1/0,5/1/1 | moos | 50 m | tropische Pilze fehlen |
| moos_polster | MossClump 01/03/05, CustomMoss 01/02/05, MossPlane | 0,017 + Satelliten | 0,2/0,6/1/1 | moos (Moos 1,6, Fels 0,9) | 60 m | bis 75° kletter, Fuß 2,0 |
| keimling | Crownbeard 01/02/10, Hornbeam-Seedling 03/04 | 0,009 | 0,7/1/0,9/0,6 | feucht | 50 m | |
| bluete_boden | LilyOfTheValley, WhiteWindflower, Periwinkle, YellowArchangel | 0,015 | 0,6/1/0,9/0,4 | feucht | 80 m | Blüteninseln (34 m, Schwelle 0,66) |
| moosstein (5) | MossyForestRock 01/02, SmallStonesPack 01/07/14 | 0,05 im Band 0,3–3,5 m | 1 | moos | 90 m | Ufer-Ebene bleibt führend |
| uferfarn (5) | Fern 03/06, EagleFern_M, SilverLadyFern_03 | 0,08, Band 1–7 m | 0,7/1/1/1 | feucht | 120 m | |
| schilf (5) | Rohrkolben Horst 1/3, Jung 1, ToadRush 00/013 | 0,04, Band 0,3–2,5 m, Hang ≤ 14° | 1/1/0,7/0,4 | feucht | 150 m | ToadRush 15–29 k Dreiecke |
| horsetail (5) | rough_horsetail 01–03 | 0,05, Band 0,5–5 m | 1/1/0,8/0,5 | feucht | 90 m | |

Höhenstufen: Talboden h < 35 m, Karst-hoch bei Relief > 45 m im 96-m-Umkreis, Hang dazwischen; jede Klasse nennt Faktoren (Palmen Tal 1,0 →
Karst 0,15; Grasbüschel/Strauch Karst 1,0–1,2). Globale Hangsperre: **> 40° nur Klassen mit `kletter`** (Kleinfarn, Moospolster, Lianen);
seit dem Rauchtest prüfen Nicht-Kletterer den steilsten Nachbarn im 3×3-Umfeld, damit nichts auf Wandkanten steht.

### 2.4 Karstlagen (G6, H6, I6, I7)

`wand` = Hang > 50°; `fuss` = ≤ 22 m von einer Wand mit Hang < 30°; `spalte` = Hang 40–78°; `gipfel` = Relief > 40 m, Hang < 26°, ≤ 40 m von
einer Wand. Ein Turm gilt als erkannt bei ≥ 60 Wandzellen im Feld und ≥ 15 m Höhenspanne (sonst Hinweis „Karstfeld ohne Wandzellen“).
Faktoren je Klasse (Tabellen oben): am Fuß Farne 1,4–1,7, Moospolster 2,0, Karstplatten 3,0, Stämme 1,3, Bäume 0,35–0,6; in der Spalte nur
Kleinfarn 0,5, Moos 1,0, Liane 1,0; am Gipfel Strauch/Gras 1,8, Jungpalme 1,2, Laubriese 0,3; an der Wand nur Moos 0,4 und Liane 1,0.

### 2.5 Overrides für Schicht 3 fels (Teil C) und 4 spuren (Teil D)

`felsgruppen_overrides`: Karsttürme als **Akteure an Steilstellen > 50°** in G6/H6/I6/I7 (Wandhöhe ≥ 15 m): Schalen `SM_Cliff_01a–e`
(29–75 m hoch, Nanite) und `SM_HugeMossyForestCliff_01`, Maßstab 0,35–0,8 (→ 12–60 m Türme), Eingraben 30–45 %, Kippen in den Hang 4–12°,
Schichtneigung 3–10°, je Turm 1 Hauptschale + 1–2 Nebenschalen mit 10–30 % Überlappung; **Moos-Auflage über WorldAlignedBlend im Material**
(`M_EL_Klippe_RVT`-Variante mit Moos oben/Kalk an der Flanke), nicht über Zusatznetze. Karstfuß 0–22 m: Blöcke 0,012/m² (Mossy-Boulder-
Palette, LimestoneRocks als Platten), 1–3 Hero je Turm (`Mossy_Rock_Formation_plFhY`, `MossyForestBoulder_04`, `TundraMossyBoulder_01`)
mit 2–5 Nebenblöcken, Kollision ab 0,8 m. `dschungel_plan.py` liefert dafür in `plan.json["karst"]` Zellzahlen und in `blickziele[]` die
höchsten Wandzellen (`karstturm`, bis 3 je Feld, 150 m Sperrkreis).
`spuren_overrides`: AsianTemple-Spuren – im Inventar sind vom Paket **nur** Bush/Cliff/Fern/Tree/Vines, keine Tempel-, Laternen-, Brücken-
oder Treppennetze. Ersatz: AncientRuins `SM_Column_02`, `SM_Wall_01/02` (Runde 2: Säule 03 und Hauptbogen gesperrt), 1–2 Ruinen je Feld auf flachem Karstfuß
10–40 m von der Wand und ≤ 60 m vom Weg (Blickziel `tempelruine`), 18–30 m Fläche, 10–30 % eingegraben, um die Ruine Lianen ×2,
Moos ×2,5, Riesenfarn ×1,5. Dazu `doline` (geschlossene Senke, Relief ≥ 8 m in 40 m: Farne/Moos, Nebel-Volumen) und `wasserfall`
(Wasserzelle mit ≥ 8 m Abfall in 10 m: Gischt, Moos + Farne im Umkreis 15 m) als Blickziele.

### 2.6 Planer `dschungel_plan.py`

`python -I scripts/dschungel/dschungel_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD] [--regeln PFAD]`. Liest
`hoehe.f32` per `np.memmap` nur im Fenster Feld + 64 m (NY 7057 × NX 9577, Spalte J auf 9577 geklippt), `lage_*.r8` (optional, sonst
Faktor 0,8), `karte_wasser/weg/ort.r8` (optional, Hinweis), `eigner.r8` + `welt.json` (optional, Fallback Feldbiom), `bestand/<Feld>/`,
`witcher/<Feld>/` (+ 8 Nachbarn), `instanzen/instanzen.json` (+ `instanzen/<name>.f32`, optional mit Meldung), `docs/staedte/standorte.json`
(optional), `daten/netze.csv` (Pfadprüfung, fehlende Netze werden mit Hinweis gestrichen). Hang/Normale aus Zentraldifferenz (Gauß 1 m),
Relief über separierbares Min-Filter, Distanzen per Jump-Flooding, Kronendach über Dilatation je Radiusstufe – **nur NumPy**, numba optional
(Cloud ohne numba: 16 s je Feld). Schreibt `export/unreal/welt/dschungel/<Feld>/<Netzname>.f32` (10 float32 LE) + `plan.json` (FORMAT §3:
`stand, feld, instanzen, dateien{pfad, anzahl, gruppe, rolle, sichtweite, schatten, kollision, ebene[, nanite:false]}, entfernen, ft_ordner,
ft_praefix` plus `statistik, karst, blickziele, hinweise, ungetestet`) und mit `--bild` `docs/pruefung/dschungel/<Feld>.png` (1 px = 1 m,
Farben je Klasse, Karstwand weiß, Fuß hellblau, Lichtung dunkel, Blickziele magenta). Budget: je Schicht 22 000/24 000/9 000/5 000, gesamt
60 000, Kollision 3 000 – deterministische Ausdünnung in `budget.prioritaet` (Keimling, Zweige, Streu … zuletzt Emergent), protokolliert
in `hinweise`.

## 3. Abgrenzung: ergänzen, nicht ersetzen

- **`FT_EL_WIT_*` (Witcher-Bewuchs):** setzt im Dschungel bereits `SM_Fern_01a`, `SM_Fern_02a`, `SM_Vines_01a`, `SM_Bush_01a`, AsianTemple-
  Bäume und `SM_Tree_Palm_01` (laut `netze.csv`). Der Dschungel-Planer **entfernt** in G6–I7 `sm_fern_01a, sm_fern_02a, sm_vines_01a`
  (`entfernen`-Filter), weil er diese drei Netze selbst lichtgesteuert und an Stämmen/Wänden setzt; Laub, Zweige, Blumeninseln der Witcher-
  Ebene bleiben, die eigene Streu-Dichte ist deshalb niedrig (0,012). In G5/I5/H5 wird nichts entfernt.
- **`FT_EL_BST_*` (Wald-Bestand):** falls dort Dschungelbäume gesetzt sind, werden sie gelesen, ins Kronendach gerechnet und mit 4 m
  (groß) / 1,2 m (klein) Abstand respektiert. Die eigene Baumschicht ergänzt Emergenten, Palmen und Jungpalmen; wo der Bestand bereits
  > 300 Bäume/ha liefert, sinken Laubriesen über `licht` auf 0,55.
- **`FT_EL_FS_*` (Felsschalen):** `SM_Cliff_01a/b/c/e_dschungel` existieren bereits als Schalen-Foliage-Typen. Empfehlung: in den vier
  Karstfeldern durch die Akteur-Türme aus Teil C (`felsgruppen_overrides`) ersetzen und die Klassen `FT_EL_FS_Cliff_01*_dschungel` dort
  entfallen lassen (Begründung: Türme brauchen Gipfel-/Fußlogik und Moos-Blend, nicht Statistik); außerhalb der Karstfelder unverändert.
- **`FT_EL_UF_*` (Ufer):** bleibt führend an allen Ufern; die Wasserkante hier ist nur Moosstein (0,05/m², 0,3–3,5 m), Uferfarn, Schilf,
  Schachtelhalm, alle ohne Kollision.
- **Teil D (`mittelschicht_plan.py`, `spuren_plan.py`)** – *überholt durch Korrektur Runde 1:* Die Palette unten steht jetzt
  maschinenlesbar in `dschungel_regeln.json["mittelschicht_overrides"]`. Teil D setzt die generischen Klassen im Dschungel selbst
  (kein Nullsetzen mehr), B7 nur noch Lianen und Moospolster. Ursprünglicher Text: Teil D nutzt im Dschungel 54 Netz-Zuordnungen mit Taxonomie-Eignung 0 und bittet um
  Abstimmung. **Verbindliche Dschungel-Palette für Teil D** (gleiche Netze wie hier, damit beide Ebenen ein Bild ergeben):
  - farn: `SM_Fern_01/02/04/05` (Megascans Fern), `SM_EagleFern_M_01/S_01/S_02`, `SM_SilverLadyFern_01/02`, `SM_BeechFern_04/09`, `SM_Fern_01a/02a`;
  - strauch: nur `SM_Bush_01a` (Maßstab 0,45–0,8 wie bei Teil D); Holunder **nur** `SM_Elderberry_05/07/08/09` als Bananen-Ersatz 1,5–2,4-fach,
    keine Weiden (`SM_grey_willow_*` raus);
  - hochstaude: `SM_Crownbeard_03/04/07/08`, `SM_petasites_spurius_01–03`;
  - jungbaum: `SM_Palm_01_10/11/12_G` (Jungpalmen), `SM_Palm_01_07–09_G`; keine Hainbuchen-/Buchen-Jungbäume;
  - totholz/stumpf/wurzel: `SM_MossyTree_01`, `SM_LargeFallenTree_02`, `SM_OldFallenTree_01`, `SM_FallenTreeAssembly_01`, `SM_RottenTreeStump_01/02`,
    `SM_TreeStump_01`, `SM_BrokenStump_01`, `SM_MossyForestRoots_01–03`, `SM_ForestRoots_01`;
  - kletter: `SM_Vines_01a`, `SM_Ivy_11/12/17/18/21/25`; pilz: `SM_mushroom_01/02` (bis tropische Pilze da sind); grasbueschel: `SM_KikuyuGrass_*`.
  Damit Teil D und B7 sich nicht verdoppeln: Teil D soll in G6, H6, I6, I7, G7, H7 die Klassen `farn`, `kletter`, `totholz`, `stumpf`, `wurzel`,
  `pilz` auf **0** setzen (B7 setzt sie lichtgesteuert) und `strauch`/`jungbaum`/`hochstaude` mit Faktor 0,5 behalten; in G5/I5/H5 (Dschungel-
  anteil 12–22 %) umgekehrt Teil D voll, B7 liefert dort nur Palmen/Riesenfarn im Saum. Die Mittelschicht-Dichten von Teil D (`farn`
  0,010/0,030) brauchen dann keine Halbierung mehr. Spuren: Obstgarten-Ersatz `SM_Palm_01_06–08_G` ist stimmig; Tempelruinen-Standorte
  und Wasserfälle liest Teil D aus `plan.json["blickziele"]` des Dschungel-Planers (Art `tempelruine`, `wasserfall`, `doline`, `karstturm`).

## 4. Testanleitung

**Erwartete Instanzen je Feld** (`erwartung_je_feld`, Schätzung ohne Echtdaten): H6 45 000–60 000 (Rauchtest 54 932), G6 35 000–55 000,
I6 25 000–45 000 (31 % steil, 33 % Sand), I7 6 000–13 000, H7 8 000–15 000, G7 4 000–9 000, G5 6 000–13 000, I5 5 000–11 000, H5 3 000–8 000.
Je Schicht in H6: Baum 8 000–9 000 (davon ≈ 2 700 mit Kollision), Mittel 22 000–24 000, Boden 20 000–22 000, Wasserkante 300–3 000 (hängt
an der Uferlänge; Rauchtest hatte nur einen 2-m-Bach). Kollision ≤ 3 000 immer; Laufzeit ≤ 20 s je Feld ohne numba.

**Prüfkameras** (Welt-cm; Z = Boden + 170 cm):

| Feld | Position | Blick | Woran man Erfolg erkennt |
|---|---|---|---|
| H6 Talboden | Feldmitte X 282 950, Y 148 350 (i 5544, j 7560), 1,7 m | nach Nord, dann 360° | Unter Laubriesen Riesenfarn-Inseln 3–12 Stück, Moosstämme mit Polstern, Lianen an 20–40 % der Stämme, keine 10 m ohne Objekt 0,5–3 m; in Lichtungen (16 %) Stauden, Grasbüschel, Jungpalmen statt Farn; Boden mit Laub/Zweigen/Keimlingen, Pilze nur im Schatten |
| I6 Karstfuß | 25 m vor dem ersten `karstturm`-Blickziel aus `plan.json` (Fuß, Hang < 30°), 1,7 m | zur Wand, 15° aufwärts | Fuß: Kalkplatten/Moosblöcke 3-fach, Riesenfarn 1,7-fach, Moospolster 2-fach; Spalte 40–78°: Lianen, Kleinfarn, Moos; Wand kahl bis auf Lianen/Moos 0,4; Gipfel: Gebüsch und Gras, Jungpalmen; **keine Palme, kein Laubriese auf > 40°** |
| G6 Wasserfall | 20 m unterhalb des `wasserfall`-Blickziels (Wasserzelle mit ≥ 8 m Abfall), 1,7 m | stromauf | Uferfarne 1–7 m, Moossteine 0,3–3,5 m, Schilf nur an flachen Stellen ≤ 14°, Bananen-Ersatz (Holunder/Pestwurz groß) bis 40 m vom Wasser, Beschattung durch Palmen am Ufer; Gischt/Moos sind Teil D/Material |
| H6 Lichtung | größte Lichtungszelle (dunkle Flecken im Prüfbild) | 360° | Lichtung sichtbar: Bäume 12 %, Stauden/Gras/Strauch 1-fach, Farne 0,3-fach; Rand weich (Beschattungsgradient, kein Zaun) |

**Prüfbild** `docs/pruefung/dschungel/<Feld>.png`: grün = Beschattung, weiß = Karstwand, hellblau = Fuß, magenta-Quadrate = Blickziele;
Farne grün, Palmen gelb, Laubriesen rot/orange, Streu braun, Moos dunkelgrün. Im Editor nach dem Setzen: Foliage-Statistik je `FT_EL_DS_*`
mit `plan.json["dateien"]` vergleichen; Palms-Pack-Typen müssen Cull 150–280 m haben (Non-Nanite, 19–31 k Dreiecke je Palme).

**Rauchtest-Ergebnis (synthetisch, H6).** Synthetische Produktionswurzel: `hoehe.f32` voller Größe (memmap) mit Talboden ~20 m, zwei
Karsttürmen (Wände 18–118 m, 14 863 Wandzellen > 50°, 31 091 Fußzellen), Bach 2 m, Weg, Ort 40 × 30 m, `eigner.r8` (Kennzahlen 0/5,
`welt.json` 5 = dschungel), `lage_Laub/Moos/Schlamm/Fels/Kraut.r8`, `bestand/H6` mit 300 `SM_Tree_Big_01a`, `daten/netze.csv`.
Ergebnis: **54 932 Instanzen** (Baum 8 656, Mittel 23 944, Boden 21 962, Wasserkante 370), 3 005 mit Kollision (nach Deckel), 130 Netze,
**15,9 s**, byte-identisch bei Wiederholung (MD5 gleich), alle `.f32` lesbar (Größe = 10 · anzahl, Quaternionen normiert, z = Boden −2 … −28 cm
bzw. +40 cm für Lianen), `plan.json`-Schema vollständig. Beschattung im Feld 0,47 (Lichtanteil < 0,33: 27 %, > 0,67: 60 %): Riesenfarn
steht zu 72 % im tiefen Schatten, Pilze 71 %, Wurzeln 78 %; Staude 39 %, Strauch 41 %, Grasbüschel 47 % im Licht – Dichte folgt der
Beschattung. Hang > 40° tragen **nur** Kletterklassen (Liane_stamm 44, Liane_wand 26, Kleinfarn 1, Moospolster 2 Instanzen); Palmen,
Laubriesen, Stauden, Stämme, Karstplatten alle ≤ 35°. Blickziele: 2 Karsttürme, 2 Dolinen, 1 Tempelruinen-Standort (kein Wasserfall, weil
der synthetische Bach eben ist). Behobene Fehler: (1) Nicht-Kletterer standen vereinzelt auf Wandkanten (Zellmitte flach, Nachbar
senkrecht) → Prüfung gegen steilsten 3×3-Nachbarn, auch für Satelliten; (2) Kern-Dichten der Bodenschicht lagen 4,5-fach über dem Budget
(100 183 → 22 000) → Dichten gesenkt, jetzt Ausdünnung 0,46 nur für Keimling/Zweige/Kleinstreu, Mittelschicht 0,67 für Gras/Kleinfarn,
Kollision 0,81 für Mittelbäume; (3) `eigner` 0 → Feldbiom statt `aue`; (4) fehlende `instanzen.json` meldet sich. Randfälle: J6 (Spalte J
geklippt, leeres Gelände) 0 Instanzen in 4,2 s mit Hinweisen, fehlende Basis → „Pflichtdatei fehlt: …/hoehe.f32“, `--faktor 0.5` → 39 396.

## 5. Einkaufsliste (frei bevorzugt, High 4K reicht)

| Asset (Fab-/Megascans-Name) | Stufe | Wofür | Ersetzt heute |
|---|---|---|---|
| Megascans „Banana Plant“ / „Huge Banana Leaf“ (Quixel), Fab „Subtropical flora“ (4 Bananenstauden, 6 Palmen) oder „Tropical Vegetation Assets“ (Banana, Philodendron) | High | `bananen_ersatz` am Wasser, Staudenflur | Holunder/Pestwurz 1,5–2,4-fach skaliert (Texel sichtbar gestreckt) |
| Megascans „Tree Fern“ (Dicksonia/Cyathea) oder Fab Riesenfarn 2–4 m | High | `riesenfarn` – echte Höhe 1,5–3 m statt Fern ×1,9 | Megascans Fern (0,6–1,0 m) hochskaliert |
| Megascans „Liana“ / „Jungle Vines“ hängend und stammumschlingend (Spline-fähig), Quixel „Huge Money Plant Vine“ | High | `liane_stamm`, `liane_wand` – 5-m-Ranken mit Pivot oben | `SM_Vines_01a` (12 Dreiecke, kein Nanite) + Efeu |
| Megascans Epiphyten: „Bromeliad“, „Staghorn Fern“, „Bird's Nest Fern“ | High | Epiphyten-Satelliten 2–6 m am Stamm (neue Klasse `epiphyt`, Eingraben −250 cm) | fehlt ganz |
| Megascans „Limestone Rock Formation“ 5–15 m, „Limestone Boulder“ 1–3 m, „Limestone Cliff“ (grau, gelöst, scharfkantig) | High | Karst-Mittelstufe zwischen Cliff_01 (30–75 m) und Moosblöcken; `karstplatte`, Turmfuß | nur 2 LimestoneRocks + Mossy-Boulder |
| Megascans „Tropical Fallen Tree“, „Rotten Log tropical“, „Buttress Root“ | High | `stamm_moos`, `wurzel` tropisch (Brettwurzeln!) | gemäßigte Moosstämme |
| Megascans „Tropical Dead Leaves“, „Palm Frond Debris“ | Medium | `streu` tropisch | DeadLeaves (Buche/Eiche) |
| Megascans „Tropical Mushrooms“/„Bracket Fungi“ | Medium | `pilz` | Meadow-Pilze |
| Blüten: „Heliconia“, „Ginger Lily“, „Hibiscus“ | High | `bluete_boden` Farbakzent rot/orange | Maiglöckchen/Windröschen |
| Nanite-Palmen (Fab, 6–12 m, Nanite) | High | `palme`/`palme_jung` ohne Cull 150–280 m | Palms_Pack (kein Nanite, 19–31 k Dreiecke) |
| AsianTemple-Tempelteile (Laterne, Treppe, Tor, Brücke) aus dem bereits lizenzierten Paket importieren | – | `spuren_overrides.tempelruine` | AncientRuins-Säulen |

## 6. Offene Punkte

1. **Echtdaten**: *(Runde 1 erledigt: Kennzahl 0 → `aue` nach Konvention, `feld_biom_fallback` gestrichen.)* Am echten `welt.json`
   prüfen, dass die Dschungelkacheln eine eigene Kennzahl mit Rezept `dschungel` haben (`plan.json["biome_fenster"]`).
2. **Wandzellen**: `wand_grad` 50 setzt voraus, dass die Karsttürme im Landschafts-Höhenfeld stehen. Sind sie nur als Felsschalen-Akteure
   vorhanden (Höhenfeld flach), erkennt der Planer keinen Turm (Hinweis im Log) – dann `karst`-Lagen aus den Akteur-Positionen von Teil C
   ableiten (Erweiterung: `felsgruppen/<Feld>/plan.json` lesen).
3. **Lianen-Pivot**: `SM_Vines_01a` ist 5,68 m hoch, Pivot vermutlich oben; `eingraben_cm: −40` ist ein Platzhalter, im Editor an einem
   Stamm prüfen und ggf. auf −500 (Aufhängung in Kronenhöhe) ändern. Efeu-Netze haben Pivot unten (bleiben bei −40).
4. **Palms_Pack**: 19–31 k Dreiecke ohne Nanite × 5 800 Palmen je Feld – mit Cull 150–280 m im Rahmen, aber die LOD-Stufen im Editor
   prüfen (Billboard ab LOD 3?). Ersatz durch Nanite-Palmen (Einkaufsliste) hat Priorität.
5. **Budget**: H6 landet bei 55 000; mit Witcher- (50 000) und Ufer-Ebene (bis 26 000) liegen > 130 000 Instanzen im Feld. Wenn das
   streamt, gut; sonst `je_schicht` Boden auf 16 000 senken (Witcher-Laub bleibt).
6. **Wasserkante** wurde nur an einem 2-m-Bach getestet; an Seen/Flüssen (G6 1,4 %, H6 3,8 % Wasser) sind 2 000–4 000 Instanzen zu erwarten,
   Deckel 5 000.
7. **Sumpf-Übergang H5** (sumpf 78 %, dschungel 12 %): Biomfaktor sumpf 0,45 lässt Palmen in den Sumpfsaum laufen – gewollt (Palmsumpf),
   aber mit B6 abstimmen, damit beide Planer nicht dieselben Zellen füllen.
8. *(Runde 1 geändert)* Teil D liest `mittelschicht_overrides` aus `dschungel_regeln.json` (Palette, Faktor, Zusatzklassen,
   `entfernen_je_feld`); bis das umgesetzt ist, fehlen im Dschungel Farne/Stauden statt doppelt zu stehen.

## Korrektur Runde 2 (10.10.2026)

- Gesperrte AncientRuins-Netze (Saeule Nr. 03, Hauptbogen Nr. 01) aus `spuren_overrides.tempelruine.netze` entfernt; es bleiben SM_Column_02, SM_Wall_01, SM_Wall_02.
- `moosstein` (Schicht 5): Massstab 0,8-1,6 -> 0,8-1,1, damit MossyForestRock_02 (0,71 m) unter 0,8 m bleibt. Keine Platten im Planer (Karstplatten/geroell_platte nur in `felsgruppen_overrides`).
- Rauchtest synthetisch H6: 26 768 Instanzen, zwei Laeufe byteidentisch, gesperrte Netze 0, Log ASCII, 16 s.

## Korrektur Runde 3b (10.10.2026)

- Dschungel entfernt keine Baeume. `sm_vines_01a` (Witcher-Lianen) nur mit Freigabe (`--ersetzen` oder `entfernen_aktiv`, Standard aus) und nur bei Dschungel-Landanteil >= 85 % (G6/H6/I6, nicht G7/H7/I7); sonst `entfernen ""` + `entfernen_vorschlag` mit Zahl. Farn-Entfernung fuer Teil D liegt jetzt in `mittelschicht_overrides._entfernen_je_feld_vorschlag` (`entfernen_je_feld` leer). Details: `verteilung-entfernen.md`.

