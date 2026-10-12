# gefaelle – Planer für steile Fluss- und Bachstrecken (Auftrag 15)

Baut die steilen Strecken aus `vorlagen/daten/gefaelle/steile_strecken.json` (161 Strecken, 19 Fluss, 142 Bach) zu
Becken, Blockstufen, Kaskaden, Fällen, Klammen und Uferklippen um. Alle Zahlen stammen aus **`gefaelle_regeln.json`**
(Regelwerk v2, Prosa und Quellen: `antworten/15-gefaelle-regelwerk.md`). Das Wasser folgt der verbindlichen
**Variante A aus Befund 14b** (`antworten/14b-befund-geteilte-baeche.md`): Epic-River nur ober- und unterhalb der
Stufenstrecke, dazwischen ein Kaskadennetz.

| Datei | Inhalt |
|---|---|
| `gefaelle_prioritaet.py` | Prioritätenliste → `antworten/gefaelle/prioritaet.json` (Sicht vom Weg, Sehens-Kameras, Fall, Status, Pilot) |
| `gefaelle_plan.py` | Planer je Lauf → `<aus>/<lauf>/plan.json`, `gelaende/`, `lagen/`, `instanzen/<Feld>/` |
| `gefaelle_pruefen.py` | Prüfer der Planausgaben (auch eingebaut im Planer) |
| `gefaelle_regelwerk.py` | liest `gefaelle_regeln.json` und wertet seine Formeln aus (AST-geprüft) |
| `gefaelle_daten.py` | Strecken (stabile IDs `<lauf>_s<k>`), Läufe, Sehens-Orte, Umbau der Sehens-Planer, gebaute Stufen |
| `gefaelle_regeln.json` | Regelwerk (Regelwerk-Agent, nicht von diesem Planer geschrieben) |
| `bachbett_roh.py` | 16c Nachtrag 3: Bachbett (Felsen, Totholz, Schlamm, Uferstreifen) für Läufe ohne Stufenplan → `<aus>/<lauf>/plan.json`, `instanzen/<Feld>/`, `lagen/` |
| `bachbett_roh_pruefen.py` | Prüfer der Roh-Lauf-Ebene (auch eingebaut in `bachbett_roh.py`) |

## Aufruf

```
python -I recherche/antworten/skripte/gefaelle/gefaelle_prioritaet.py [--daten2m DIR | --daten1m DIR] [--p2 DIR]
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py [--laeufe ID …] [--strecken ID …] [--alle]
       [--daten2m DIR] [--aus DIR] [--bild [--bild-ordner DIR]] [--variante A|C] [--ohne-pruefung]
       [--hoehe1m-fenster DIR]
python -I recherche/antworten/skripte/gefaelle/gefaelle_pruefen.py <aus> [--daten2m DIR | --daten1m DIR]
       [--hoehe1m-fenster DIR]
```

- Ohne `--laeufe/--strecken/--alle` plant der Planer die Läufe der 20 Pilot-Strecken aus `prioritaet.json`.
- Lokal (1 m): `--basis <production>` bzw. ohne `--daten2m` → liest `export/unreal/welt/`, schreibt nach
  `export/unreal/welt/gefaelle/<lauf>/`. `baeche_alle.json` wird in `export/unreal/welt/baeche/` gesucht, sonst die
  Kopie in `vorlagen/daten/sehens/` (gleiche IDs wie `steile_strecken.json`).
- Cloud-Test: `--daten2m recherche/vorlagen/daten/sehens --aus <scratchpad>/a15/plan`. Die Planausgaben gehören nicht ins Repo.
- `--variante C` gibt zusätzlich `wasser_koerper_alternativ` aus (gestufter Einzelspline + eigene Bach-Zone, 14b Rückfall C).

## Ausgabe `plan.json` je Lauf

| Schlüssel | Inhalt |
|---|---|
| `spiegel_alt_cm`, `spiegel_neu_cm` | alte Laufpunkte bzw. neue Wasserlinie `[[x, y, z, breite], …]`, nie steigend; dazu `spiegel_neu_s_m` und `spiegel_neu_art` (alt, becken, lippe, fuss, rampe). Stufe = Lippe + Fuß 0,5 m auseinander. |
| `stufen` | je Stufe `lippe_cm` (3–7 Punkte, links → rechts mit Blick talwärts, Bogen mit Scheitel stromab), `ueberfall_cm`, `fuss_cm`, `fuss_z_cm`, `fall_m`, `art` (fall, kaskade oder schnelle; die Blockstufe wird als `kaskade` ausgegeben), `art_regel` (schnelle, stufe, kaskade oder fall), `teilstufen`, `kolk`, `klasse`, `biom`, `felstyp`, `holzstufe`, `vorhang` (einzelner Absturz ≥ 3 m, wie `vorhang_an_stufen`), `vorhang_niagara` (sonst ab 0,8 m) |
| `wasser_koerper` | Liste: `river` (Epic, `punkte` [x, y, z, breite, tiefe, velocity] + `punkt_typen`) und `kaskadennetz` (`s_m`, `mittellinie` [x, y, z, breite, tempo, fallanteil, schaum, abstand_bett], `knick` je Punkt: becken, lippe, bogen, wand, fuss, rampe; `rand_ueberstand_m` 0,4, `material`, `vorhang_an_stufen`, `pruefung`). Nachbarn überlappen 0,5 m. |
| `abschnitte` | je Strecke (lange Strecken: `_a1`, `_a2`, Fenster ≤ 600 m) `gelaende` (`datei`, `fenster_ij`, `max_aenderung_m`, `werkzeuge`: Bett, Kolk, Felsstufe, Klamm, Uferklippen), `lagen`, `budget`, `detail_ebenen` |
| `wandzonen` | Uferklippen/Klamm entlang des Laufs (s, Höhe, Grund, Wasserhöhe) |
| `instanzen`, `akteure` | Ebene `gefaelle` in `instanzen/<Feld>/plan.json` + f32 (FORMAT.md §3, FT-Präfix `FT_EL_GEF_`), Akteure dort in `plan["akteure"]` mit `klasse` `<abschnitt>_<gruppe>` |
| `effekte` | Nature Water FX (`typ: niagara`, `asset`, `pos_cm`, `rot_q`, `skala`, `cull_m`, `stufe`, `rolle`, `effekt_art`), nur an Stufen ≥ 1 m, ≤ 3 je Stufe, ≤ 6 gleichzeitig mit Cull ≥ 30 m, dazu je Stufe ≥ 1 m ohne Aufprall ein `NS_Impact_Small` mit Cull 20 m (`effekt_art: zusatz_aufprall`), hart ≤ 8 gleichzeitig |
| `zufluesse` | Zuflüsse, die in die Stufenstrecke münden: Mündung `s_m`, `punkte_neu_cm` (Endstück an den neuen Spiegel angepasst, nie höher als vorher) |
| `a14` | nur C2: `ersetzt_a14`, ersetzte A14-Gruppen (C2_A–C2_E) aus `antworten/wasser_fx/plan.json`, Hinweis |
| `kameras` | §8, je Pilot-Strecke `<id>_vorher`/`_nachher` (unterhalb der größten Stufe) und, wenn sichtbar, `<id>_weg_vorher`/`_nachher` vom Weg, `Hoch = -170` |
| `strecken` | Status, Rang, ausgesparte Zonen mit Grund, Segmente, Stufen-IDs, Arten, gestufter Fall |

## Ablauf (Regelwerk `ablauf`)

1. **Feste Zonen**, in denen der alte Spiegel bleibt (Entscheidung Koordinator 11.10., weicher als zuvor):
   - Wege und Pfade: nur die **Furt** (ruhiges Becken auf altem Spiegel) im Abstand max(3 + 2 m + B/2; 6 m) um die
     Querung, also ≥ 12 m ruhiges Wasser. Stufen dürfen bis 6 m an einen Weg heran, nie auf oder unter ihn.
   - Orte (5 m + 4 m + B/2), Städte, Sehenswürdigkeiten (Radius + 18 m + B/2) und der Umbau durch einen Sehens-Planer
     bleiben fest.
   - **Zuflüsse werden mit umgebaut:** Sie münden in ein Becken, ihr Endstück wird über L = clamp(Δz/0,15; 3; 40) m an
     den neuen Spiegel angepasst (`zufluesse`). Fest bleibt nur fremdes Wasser, das weder Zufluss noch eigener Lauf
     ist (Raster mit Rand B/2 + max(6 m; 0,3 B)), und Seen bzw. kreuzende Gewässer.
   - Anschluss max(2·min(B; 5 m); 3 m) an den Laufenden, Abschnittsgrenzen (±10 m).
2. **Klasse** je Ort aus S im Fenster `klassen.fenster`; **Einzelfälle** aus `faelle.einzelfall_statt_kette`
   (S_lok ≥ 0,6, D ≥ 4 m bzw. 2 m an Fels nach `ablauf.fels_anstehend`), gebündelt über `buendeln`, höchstens
   `hoehe_max_einzeln` (25 m) je Fall.
3. **Stufen** nach `stufen.abstand_L` (Fluss `abstand_L_fluss`), Fallketten nach `faelle.kette_glied`, Zufall
   `stufen.zufall`, Mindestabstand `min_abstand_stufen`, höchstens `max_stufen_je_100m`. Die Lippe sitzt am steilsten
   Punkt im Fenster ±25 % (Knick) und **auf dem alten Spiegel**; das Becken fällt mit `becken.gefaelle` bis zur
   nächsten Lippe. Damit gilt D = S·L − S_Becken·(L − Stufenlänge) exakt, die Summe ergibt D_ges, und der neue Spiegel
   liegt nie über dem alten.
4. **Arten:** Fall (nur an Fels oder als erzwungener Knick), Blockstufe 0,8–2 m, Kaskade (Teilstufen ≤ 1,5 m; kurze
   Becken werden zu Kaskaden mit 2–4 Teilstufen gebündelt, deren Teil-Lippen ebenfalls auf dem alten Spiegel liegen),
   Schnelle als Rampe. Holzstufen nach `stufen.holzstufe.anteil` je Biom.
5. **Gelände** (1-m-Delta, Rand 0; Querprofil seit 15b):
   - Bett = Spiegel − max(Tiefe; 0,5 m), Krone 0,15 m unter der Lippe, Kolk nach `kolk`.
   - Wasserkante 0,3–0,5 m innerhalb der halben Breite, Böschung 35° durch die Wasserkante. Bett und Kolke sind so nie
     breiter als das Wasser.
   - Außerhalb der halben Breite die Uferwand mit dem Uferwinkel: 35°, Uferklippe 60–90° (`ufer_klippen`), Klamm 85°
     mit `klamm.sohlbreite`. Neben dem Fuß einer Stufe bleibt das Ufer 1,5 m lang auf Oberwasserhöhe.
   - Uferring: ab der Wasserkante mit 35° auf Spiegel + 0,15 m bis Netzrand + 1,5 m, dann 1:2 auslaufen, höchstens 1 m
     anheben.
   - Die Breite ändert sich höchstens um 0,2 m je m.
   - **1-m-Feinschliff:** Das Delta wird auf dem 1-m-Ausgaberaster gegen das alte 1-m-Gelände nachgezogen (Wasser =
     Querprofil, Uferring), mit denselben Schutzfaktoren. Lokal ist das die 1-m-Welt; in der Cloud kommt das alte
     Gelände aus `--hoehe1m-fenster`, sonst aus dem 2-m-Raster.
6. **Netze** je Biom am Stufenort (`biome.<biom>.netze`, gesperrte Netze werden übersprungen): Fallwand (held, Akteur),
   durchgehende Lippe aus Riegel-Netzen, Keystone + Stufenblöcke (`schutt.stufenblock_D`), Holz, Uferwände (Reihe beidseitig,
   hohe Wände in 2–3 Reihen übereinander), Sturzblöcke (`schutt.unter_fall`), Beckenblöcke, Wandschutt (`kegel_laenge`),
   Kies, Moos (Kontaktzone Nordseite). Entscheidungen Koordinator 11.10.:
   - `uk5ebcp` wird übersprungen.
   - **Elfenwald:** Wände aus gestapeltem `SM_HugeMossyForestCliff_01` / `SM_ForestRockShelf_*` (bis 4 Reihen).
   - **Aue:** keine Felswände; Stufen sind Erdanrisse (Gelände), Wurzelstufen und Holz-Verklausungen (3 Stämme) im
     Wechsel.
   - **Holz (13k-Rückfrage 2, 12.10.):** nur natürliche liegende Stämme und Äste, kein Sägeschnitt; Netz nach Länge,
     Skala 0,6–1,8 (Abschnitt „Holz und Akteure“).
7. **Lagen** nach `lagen.zonen` × `biome.<biom>.lagen`, **Effekte** nach `effekte.je_art`. Stufen < 1 m bekommen
   kein Niagara. 1–3 m: `NS_Waterfall_Small` + `NS_Impact_Small`, ab 3 m Vorhang-Netz plus Niagara (14b). Cull 30–60 m
   (Heldenfälle bis 150 m). Ausdünnen auf ≤ 6 gleichzeitig mit Cull ≥ 30 m (große Fälle zuerst), danach je Stufe ≥ 1 m
   ohne Aufprall ein `NS_Impact_Small` mit Cull 20 m, hart ≤ 8 gleichzeitig (Koordinator 11.10.).
8. **Wasserkörper** Variante A: Kaskadennetz von der ersten Lippe bis 1,5 m hinter den Fuß der letzten Stufe, River
   davor und danach. Prüfung (a) Bett ≥ 0,2 m unter dem Spiegel und (b) Ufer am Netzrand ≥ 0,1 m darüber, gegen das
   Gelände nach dem Stempel.

## C2 und H4 (Koordinator 11.10.)

- **C2 (`F_ERLENBACH_1V_C2`)** ist zurückgestellt (14b) und wird vollständig mit Kaskadennetz geplant, Pilot Rang 1.
  Die Stufenlagen aus `vorlagen/daten/wasser_fx/stufen.json` sind Vorgabe, wo sie zum Regelwerk passen
  (`stufen[].vorgabe_stufen_json`). **Für C2 ersetzt der A15-Plan die A14-Einträge** (Gruppen C2_A–C2_E in
  `antworten/wasser_fx/plan.json`, Teilung in `stufen_fluss_teile.json`), siehe `plan.json` → `a14`.
- **H4:** Die beiden A14-Schnellen liegen auf `F_ELFENFLUSS_2_H4`. Diese Strecke ist `kaum_planbar` (Ort/Stadt),
  bleibt Fluss mit `NS_Stream` aus A14 und bekommt keinen A15-Plan. `F_ELFENFLUSS_3_H4` (45 m Fall auf 418 m) ist ein
  anderer Lauf, für den das Regelwerk Stufen verlangt; dort plant A15 ein Kaskadennetz. Läge eine Vorgabe-Stufe in
  einem Nicht-C2-Lauf, blieben ihre A14-Effekte (`a14_effekte_bleiben`).

## Prüfer

`gefaelle_pruefen.py` prüft:
- Spiegel monoton, Anfang und Ende auf alter Höhe, nie über dem alten, Zwei-Punkt-Abstand, Becken ≤ 3 % (FEHLER) bzw. ≤ 2 % (WARNUNG), Rampen.
- Stufenhöhen gegen `stufen.arten`, Dichte, Lippenform.
- Wasserkörper: monoton, Überlappung genau 0,5 m, keine weitere Überlappung (auch in der Draufsicht), jede Stufe im Netz, Niagara oder Vorhang je Stufe ≥ 1 m (sonst WARNUNG).
- Bett und Ufer an jedem Beckenpunkt des Netzes (Becken seit 15b alle ≤ 2 m beschrieben), gegen das Gelände nach dem
  Stempel:
  - Bett ≥ 0,2 m unter dem Spiegel, gemittelt über die mittleren 60 % der Breite.
  - Ufer am Netzrand (halbe Breite + 0,4 m) ≥ 0,1 m über dem Spiegel.
  - „Bestand“ (WARNUNG) nur, wenn das alte Ufer dort tiefer liegt als Spiegel + 0,1 m − 1 m, der Uferring es also nicht
    erreichen kann.
  - Mit `--hoehe1m-fenster` rechnet die Prüfung exakt auf 1 m: altes Gelände aus den Fenstern + 1-m-Delta, bilinear.
- Effekte: Inventar, ≤ 3 je Stufe, ≤ 6 gleichzeitig mit Cull ≥ 30 m, ≤ 8 gesamt, Cull ≥ 20 m nur für `zusatz_aufprall`.
- Kameras.
- Gelände: Rand 0, |Δ| > 40 m, nicht ≤ 2 m an Weg/Pfad, ≤ 5 m an Ort, nicht in Sehenswürdigkeiten, Anheben > 1 m.
- Lagen-Dateien.
- Instanz-Ebene über `sehens_lib.sehens_pruefen.pruefe_ebene(…, kontext="gefaelle")`: Format, Inventar (auch
  Sägeschnitt = FEHLER, Wildnis), Feldrechteck, Budget §9 je Abschnitt, Schweben, Weg, dazu Ortsflächen.
- Akteure: höchstens 50 je 200 m Lauflänge (gleitendes Fenster entlang der neuen Wasserlinie), sonst FEHLER. Die
  Sehens-Grenze „50 je Ort“ gilt im Kontext `gefaelle` nicht je Abschnitt.

Auf 2-m-Daten zählt eine Bett- oder Uferabweichung an höchstens 1 Punkt bzw. 10 % eines Netzes als WARNUNG
(Rasterverschmierung an kurzen Kaskadenbecken). Lokal auf 1 m gilt FEHLER.

## Testlauf 2 m (11.10.2026, nach den Entscheidungen des Koordinators)

- **Priorität:** 117 offen, 2 teilweise_sehens, 6 umgebaut_von_sehens, **36 kaum_planbar (vorher 76)**. 30 der 36 sind
  kürzer als 40 m.
- **20 Pilot-Strecken (19 Läufe, C2 Rang 1):** 346 Stufen, Prüfer **0 FEHLER**, 13 WARNUNG (vor allem Stufen ≥ 1 m
  ohne Niagara wegen der Grenze gleichzeitig, sowie 2-m-Rasterfälle bei Bett/Ufer). Zwei Läufe ergeben byteidentische
  Ausgaben (`diff -r` ohne Bilder). Laufzeit ~110 s.
- **Alle 161 Strecken (`--alle`):** 123 Läufe, 98 mit Stufen, 1089 Stufen (664 Kaskaden, 381 Blockstufen, 35 Fälle,
  9 Schnellen), 128 Kaskadennetze, 16 angepasste Zuflüsse, **0 FEHLER**, 32 WARNUNG, ~145 s.
- `sehens_lib/selbsttest.py` und der Bergwald-Planer melden weiter 0 FEHLER (einzige Lib-Änderung:
  `instanzen.Ebene(…, ebene_name, ft_praefix)`).
- Testbilder: `antworten/gefaelle/test_<strecke>.png` (lange Strecken `_a1`, `_a2`), oben die Draufsicht, unten das
  Längsprofil vorher und nachher.

## Korrektur 15b (1-m-Test)

Ergebnis und Vorher-Nachher-Tabelle stehen in `antworten/15b-korrektur-1m-ufer-netzrand.md`.

- **Pilotläufe auf den 1-m-Fenstern:** 19 Läufe, 0 FEHLER (vorher 29), zwei Läufe identisch.
- **Alle 161 auf 2 m:** 0 FEHLER.

## Nachtest 15c

- **Bett:** mindestens 0,7 m unter dem Spiegel (vorher 0,5 m), als Sicherheitszuschlag gegen das Raster.
- **Becken unter Stufen ≥ 1,5 m:** mindestens 5 m breit, bis Kolkende + 1,5 m. So liegt die Oberwasser-Seitenwand
  ≥ 1 m neben dem nassen Bett.
- **Kurze River-Stücke:** Ein River < 15 m wird nicht als Epic-River ausgegeben, sondern als Teil des Kaskadennetzes
  (`knick` = `rampe`, `rampen_s_m`). Das gilt am Laufanfang, am Laufende und zwischen zwei Netzen. Flache Teile
  (≤ 2 %) haben Becken-Tempo. Der Prüfer meldet River < 15 m als FEHLER.
- **Mündungen:**
  - Ausgenommen ist nur noch die Uferprobe einer Seite, die ≤ Zuflussbreite/2 + 1 m von der Zuflusslinie liegt
    (`kaskadennetz.muendungen[].linie_cm`). Die Gegenseite und der Rest des Netzes werden geprüft.
  - Der Uferring hebt an der Zuflusslinie nicht an.

## Korrektur 15e

- **Abtrag außerhalb der Wasserbreite** ist begrenzt: höchstens (alter − neuer Spiegel + 0,5 m) − (Abstand −
  halbe Breite) · tan 35° (`aussen_begrenzen`). Vorher war die 35°-Böschung eine Obergrenze bis 60 m neben dem Bach
  und schnitt steile Hänge ab.
- **Uferring:** auf Spiegel + 0,2 m. Auch das Anheben läuft außen 1:2 aus.
- **„Bestand“** zählt, wenn das alte Ufer tiefer als Spiegel − 0,75 m liegt.
- **Lagen:** Jede Zelle mit |Δ| > 0,3 m bekommt eine Lage, sonst die erste Lage der Zone `ufer_nah`. Das gilt auch
  jenseits von Feldgrenzen.
- **Neue Prüfregeln:**
  - |Δ| > 0,3 m ist nur innerhalb von halbe Breite + 0,4 + 1,5 m + (Eintiefung + 0,5 m) / tan 35° + 1 m erlaubt,
    dazu an den Zufluss-Endstücken.
  - Jede Zelle mit |Δ| > 0,3 m braucht eine Lage.

## Unregelmäßige Stufen und Querprofil (15f)

Die Parameter stehen in `gefaelle_regeln.json`, Abschnitt `stufen.unregelmaessig`.

**Lippen**
- Jede Lippe (auch jede Teil-Lippe einer Kaskade) liegt 15–30° schräg zur Querrichtung, das Vorzeichen ist zufällig.
- Sie ist gekrümmt (Pfeil 0,05–0,15 B, Scheitel stromab) und hat 1–2 Kerben für den Hauptstrahl.
- Teil-Lippen einer Kaskade haben dieselbe Schrägrichtung, aber einen anderen Winkel. Die Kerbe sitzt auf der anderen
  Seite (versetzt).
- Der Längsversatz wird so begrenzt, dass zwischen Nachbarlippen |ΔVersatz| ≤ 0,6 × Becken gilt. Damit bleibt
  `s_eff(s, u) = s − Versatz` monoton und der Spiegel steigt nie.
- Gelände, Bett, Krone (neben der Kerbe 5 cm unter Wasser, in der Kerbe tiefer), Uferring und Netz rechnen alle mit
  `s_eff`.

**Abstände und Höhen**
- `stufen.zufall` ±40 %, Suchfenster für die nächste Lippe 0,6–1,4 L.
- Teilstufen einer Kaskade streuen ±45 % (Blockkaskade). Es wird eher eine Teilstufe mehr gelegt, die mittlere Höhe
  liegt bei ≤ 0,75 × D_max.
- 30 % der Teilstufen bis 0,8 m werden zur Rampe (Schnelle), wo Platz ist.

**Breite:** Lippen 0,8 B (Einschnürung ±1,5 m), Becken 1,2 B. Die Breite ändert sich höchstens 0,4 m je m.

**Netze**
- Lippen sind dicht mit Blöcken besetzt (Abstand 0,75 × Blockgröße); die Kerben bleiben frei, Keystones sitzen an den
  Kerbenrändern.
- Neu: Kies im Kolk, Totholz quer im Becken (30 %), mehr Beckenblöcke.

**Kaskadennetz**
- `mittellinie_s_m`: Laufkoordinate je Punkt.
- `knick` hat zusätzlich den Wert `uebergang`: Querschnitte alle 0,25 m um jede Lippe, damit der schräge Absturz
  aufgelöst ist.
- `quer` (je Punkt `quer_punkte` Stützpunkte, seit 15g mindestens 21 und Querabstand ≤ 1 m, also je Netz
  N = max(21; ⌈(Breite_max + 0,8 m)/1 m⌉ + 1), ungerade; Index 0 = rechts, Lage
  u = (−1 + 2 j/(N − 1)) × (breite/2 + rand_ueberstand_m)) mit den Feldern:
  - `dz_cm`: Wasserhöhe gegen `z_cm`.
  - `deckung` 0–1: In der Kerbe ist die Zunge deckend, daneben 0,15–0,35, sodass Fels durchscheint.
  - `schaum` 0–1: nur am Lippensaum (≤ 0,5 m, Seiten 0,15), auf der Zunge (Seiten 0,1) und im Aufprallkreis
    (≤ 30 % der Beckenlänge), sonst 0.
  - `tiefe_cm`: Wasser über dem Bett, für die Beckenfarbe.
- Dazu `material_parameter` (Schaum_Menge 0,15, Zungen_Schaum 0,25) und `farbe_hinweis`.
- Die Spalte `schaum` der Mittellinie ist der mittlere Querpunkt.

**Prüfer**
- Querprofil passt zur Mittellinie, Wasserlinie je Längsstreifen monoton, Werte 0–1, Anfang und Ende eben
  (Anschluss River).
- Ufer und Bett gegen das Wasser an der jeweiligen Seite. Uferproben direkt neben einem schrägen Absturz
  (≤ 1,5 m stromab, ≤ 1 m stromauf auf dieser Seite) zählen wie Lippenpunkte (`ufer_an_lippe`).
- HINWEIS „Regelmäßigkeit“: CV der Lippenabstände bzw. Fallhöhen < 0,2 oder Lippenwinkel alle gleich.

## Bildbefund 15g (C2 Version 2)

Ergebnis und Zahlen: `antworten/15g-c2-v2-bildbefund.md`. Parameter in `gefaelle_regeln.json`,
`stufen.unregelmaessig` (`schaum`, `quer_punkte`, `quer_abstand_max_m`, `deckung_ufer`, `ufer_rauschen`,
`rand_bloecke`, `material`).

**Schaum weich (`quer_ergaenzen`, `kerben_weich`, `schaum_weich`)**
- Querpunkte: mindestens 21, Querabstand ≤ 1 m (`quer_n`; C2: 31).
- Quer: Kerbenrand smoothstep über ≥ 3 Querabstände, Kerbenbreite mit Rauschen entlang s.
- Längs: Kern am Lippensaum (Schaum ≥ 0,5 höchstens 0,5 m oberhalb), Anstieg oberhalb über ~0,8 m, Abklingen
  unterhalb über clamp(0,15 × Beckenlänge; 0,8; 1,5) m, beides ±20 % Rauschen. Aufprall: Kern ≤ 30 % der
  Beckenlänge, endet vor der Beckenmitte, elliptischer Rand, nur unterhalb der eigenen Lippe.
- Rauschen: `rauschen2` (Wertrauschen mit ganzzahligem Hash, Seed aus Lauf-ID und Netznummer), deterministisch.
- Verdichtung: Mittellinie alle 0,25 m über die ganze Schaumzone jeder Lippe.
- Sicherheitsnetz `schaum_weich`: Sprung höchstens 0,45 je Querabstand bzw. je 0,5 m längs; hebt nur die
  niedrigere Seite an.

**Deckung und Tiefe**
- `tiefe_cm` ≥ 0 (0 = Gelände über dem Wasser).
- `deckung` = 0, wo das Gelände über dem Wasser liegt; sonst 0,3 + 0,7 × smoothstep(Tiefe / 0,6 m), quer höchstens
  0,5 je Stützpunkt. Die Zunge in der Kerbe bleibt deckend.
- `material_parameter`: Werte für `M_EL_Kaskade_SLW2` (klares Gebirgsbachwasser, Koeffizienten je m). Opacity nur aus
  Schaum, nicht aus Deckung.

**Unregelmäßige Beckenränder (`UferRand`)**
- Je Seite zieht die Wasserkante um Einzug(s) = amp × n(s) nach innen; n ist weiches Rauschen (Wellenlänge ~6,5 m).
  So entstehen Vorsprünge, dazwischen Buchten auf voller Breite.
- amp = clip(0,2 B − 0,3 m; 0; 1,2 m). Je Seite ist amp = 0 am Lippenende (0,3 m frei, 1 m Übergang), an
  Segmentenden, Mündungen und Wand-/Klammzonen (> 50°).
- Die Netzbreite wird um max(amp links, amp rechts) verbreitert und bleibt die Hülle. An den Lippen bleibt die
  Breite, die Spiegel bleiben waagrecht.
- Gelände: `profil_T`, `aussen_begrenzen` und `ring_ziel` rechnen mit der Wasserkante je Seite. Der Uferring
  (Spiegel + 0,2 m, ≤ 1 m Anheben) bildet die Vorsprünge; das Plateau endet weiter am Netzrand + 1,5 m. Abtrag
  neben dem Wasser ≤ Eintiefung + 0,5 m.
- `plan.json` → `ufer_rand`: Einzug je 1 m links/rechts und Kennzahlen.

**Randblöcke (`bauen_instanzen`)**
- `randecke_<n>`: je Lippenende (auch Teil-Lippen) mit 85 % ein Eckblock 0,9–1,8 m, knapp außerhalb der Wasserkante,
  0,2–0,8 m stromab.
- `randbloecke_<n>`: am Beckenrand alle 2,5–5 m je Seite; auf Vorsprüngen sicher, sonst mit 33 %.
- Netze aus der Biom-Palette `bloecke` (geprüft gegen das Inventar), Ebene `schutt`, keine Akteure.

**Prüfer (neu, FEHLER)**
- Querprofil: ≥ 21 Stützpunkte, Abstand ≤ 1 m, `tiefe_cm` ≥ 0.
- Schaumkante: Sprung zwischen Nachbarpunkten quer ≤ 0,5, längs ≤ 0,5 je 0,5 m.
- Schaum nur auf feinem Längsraster: Abstand ≤ 0,6 m, wo Schaum > 0,05.
- Kein Schaum ≥ 0,5 in der Beckenmitte, je Längsstreifen: in Becken ≥ 6 m im Bereich
  [Anfang + 0,5 L + 1,5 m; Ende − 1 m].
- WARNUNG: Schaum ≥ 0,5 auf > 25 % der Netzfläche.

## Holz und Akteure (13k-Rückfragen 2 und 6, Koordinator 12.10.)

Ergebnis und Zahlen: Nachtrag in `antworten/13k-pilot2-bildbefund-15g-nachtrag.md`.

**Holz.** Die Sägeschnitt-Regel der Bibliothek (`inventar.saegeschnitt`: `*_log` aus
`Mountain_Environment_Set/Details`, Material `*ends*`, Holzlager) gilt auch für A15, weil Gefälle-Bäche Wildnis sind.
- `biome.bergwald.netze.holz`: statt `SM_Forest_pine_04_01/02/03_log` die natürlichen Netze aus 13k: liegende Stämme
  `SM_OldFallenTree_01/02`, `SM_LargeFallenTree_01/02`, `SM_FallenSpruceTree_01`, `SM_MossyTree_01` und Äste
  `SM_OldTreeBranch_01/02/03/04/06`, `SM_detail_branches_01/02/03`.
- Elfenwald, Aue, Sumpf, Dschungel und Ödland bekommen dazu lange natürliche Stämme bzw. Äste, damit breite Bäche
  passende Längen finden. Küste (Treibholz), Canyon und Wüste bleiben. `SM_dead_log_*` bleibt (13k-Rückfrage 1 offen).
- **Netz nach Länge** (`holz_setzen`): Ziel-Länge wie bisher (Holzstufe 0,45–0,7 × Lippenbreite, Totholz
  0,6–0,95 × B). In Frage kommen Netze mit Ziel-Länge / Netzlänge in `stufen.holzstufe.netz_skala` [0,6; 1,8];
  sonst das nächstliegende Netz. Die Länge wird auf 0,6–1,8 × Netzlänge begrenzt. Vorher lag die Skala bis × 45.
- **Ausrichtung** aus den Bounds (`holz_form`): Liegend modellierte Stämme (lange Achse x/y) werden `normale` gesetzt,
  die lange Achse quer zum Bach, wie das 13k-Totholz. Mit `liegend` standen sie vorher schräg bis senkrecht.
  Nur stehend modellierte Stücke (lange Achse z, z. B. `Branch_Goat_Willow_Decaying_*`) bleiben `liegend`.
- Je Holzstück eine Gruppe `holz_<nr>_<teil>_<i>` bzw. `totholz_<nr>_0`. Lage, Zahl und Höhe der Stufen ändern sich
  nicht.

**Akteure.** Die 13k-Grenze „höchstens 50 Akteure je Ort“ gilt für Sehens-Orte. Ein Gefälle-Abschnitt ist bis 600 m
lang, deshalb gilt hier:
1. Je Abschnitt die 13j-Regel: ≥ 12 gleiche Akteure (`AKTEUR_WIEDERHOLT_AB`) werden Instanzen mit Kollision
   (`OrtKontext._akteure_buendeln(grenze_je_ort=False)`).
2. Je Lauf höchstens 50 Akteure je 200 m Lauflänge (`akteure_je_lauflaenge`, gleitendes Fenster mit 2 m Reserve).
   Ist ein Fenster voll, stellt die 13k-Logik (`sehens_lib.instanzen.akteure_auf_grenze`) weitere Netze um: zuerst
   die häufigsten, dann die kleinsten, nie die Held-Ebene. Eine Back-Kachel ist ≤ 128 m lang und liegt damit in
   einem Fenster. Der fluss_sim-Prüfer zählt zusätzlich je Kachel.
- Lage, Größe und Drehung bleiben, nur die Ausgabeform ändert sich. Niagara-Effekte und Vorhänge sind unverändert.
- In der Bibliothek trennt `pruefe_ebene(…, kontext="sehens" | "gefaelle")` die beiden Fälle. Im Kontext `gefaelle`
  entfällt nur die Grenze je Ort, alle anderen Regeln gelten wie in Sehens.

**Prüfung (12.10.):**
- Alle 161 auf 2 m: 0 FEHLER (vorher 193 im Prüfer bzw. 189 im Planer), 42 WARNUNG (vor 13k 51), zwei Läufe
  identisch.
- 19 Piloten auf den 1-m-Fenstern: 0 FEHLER (vorher 21), 11 WARNUNG (vor 13k 12), zwei Läufe identisch.
- Weggefallen sind 9 Warnungen „Instanzen schweben“. Stufen, Spiegel, Wasserkörper, Effekte, Kameras, Gelände und
  Lagen sind gegenüber dem Stand vor 13k unverändert.
- Die Zahl der Instanzen und Akteure ist gleich (64 951 ohne Holz, 1 002 Holzstücke). Etwa 1 800 kleine Steine und
  Kiesel rücken neben dem Holz leicht, weil die Abstandsregel die neue Holzgröße sieht.

## Einheitenfelder und Stammausrichtung (Nachtrag 13k, 12.10.)

Ergebnis und Zahlen: Abschnitt „Nachtrag: Stammausrichtung Sehens, Einheitenfelder A15“ in
`antworten/13k-pilot2-bildbefund-15g-nachtrag.md`.

- **`material_parameter` jedes Kaskadennetzes** trägt jetzt dieselben Einheitenfelder wie die Sehens-Netze
  (`slw_einheit`): `einheit: "je_m"`, `skalierung_ue: 0.01`, `SLW_Absorption_pro_cm` (0,004/0,0007/0,0005),
  `SLW_Streuung_pro_cm` (0,0002/0,0003/0,0004) und `einheit_hinweis`. UE 5.8 rechnet die SLW-Koeffizienten je cm
  (Ferat-Test 13k). Die je-m-Werte `SLW_*_pro_m` bleiben unverändert. Sonst ändert sich an den Netzen nichts.
- **Prüfer:** `pruefe_ebene` (auch im Kontext `gefaelle`) meldet FEHLER, wenn ein liegend modelliertes Holznetz steht
  (Hochachse > 45° gegen die Hangnormale) oder eine Holz-Instanz außerhalb der Skala liegt (Stämme 0,6–1,8, Äste
  ≤ 1,8). Die A15-Läufe sind seit `024d25f` regelkonform (0 FEHLER).

## Bachbett: Totholz, Schlamm, Uferstreifen (16c Nachtrag 18:15)

Ferat zu C2: „Felsen, totes Holz und Schlamm gehören in jedes Bachbett.“ Logik und Zahlen liegen gemeinsam für A15 und
die Sehens-Bach-Planer in `sehens_lib/bachbett.py` und `sehens_lib/bachbett_regeln.json` (Dichten je Biom mit Quellen).
Antwort: Nachtrag 2 in `antworten/16c-ferat-ein-fluss-je-gewaesser.md`.

- **Unverändert:** Stufen, Lippen, Becken, Spiegel, Gelände, Wasserkörper, Effekte und Kameras. Neu sind nur Instanzen
  (Gruppen `bb_<art>_<nr>`, nach allen anderen Gruppen gesetzt) und Lagen.
- **Totholz je Segment** (`bachbett_instanzen`): Ziel = `lw_je_100m` des Bioms × Waldfaktor × Länge, abzüglich der
  vorhandenen Holzstufen/Totholz-quer-Stücke (`holz_*`, `totholz_*`, `wurzel_*`).
  - Verklausungen oberhalb von Lippen (Becken davor ≥ 3 m) und an Engstellen (B ≤ 0,85 × Median): 2–3 Stämme schräg
    (12–35°), verkeilt (Unterkante auf Spiegel − 0,6 × Dicke bzw. auf dem Stamm darunter, `z_frei`), Äste obenauf.
  - Überspannende Stämme an schmalen Becken (B ≤ 5 m): auf beiden Ufern aufliegend, Unterkante ≥ Spiegel + 0,25 m. Der
    fluss_sim-Export führt sie als `ueberspannt` (16a Entscheidung 5, keine Wasser-Kollision).
  - Stämme am Ufer, teils im Wasser (15–55° zur Fließrichtung), Wurzelstöcke an der Wasserkante, Äste am Ufer, Zweige
    am Innenufer (Gleithang).
  - Netz nach Länge wie 13k (Skala 0,6–1,8), liegend modelliert → `normale` (Hangnormale), nie Sägeschnitt, nie Akteure.
  - Kollision für alles große Holz (und Äste ≤ 1 m neben dem Wasser) → Datei `<netz>_kol`, damit der fluss_sim-Export
    es als Wasser-Kollision aufnimmt (`fluss_sim_regeln.kollision`: Kollision im Plan, Grundriss ≥ 0,4 m, Höhe ≥ 0,2 m).
  - Kein Stück mit der Achse mitten in einer Lippe bzw. einem Vorhang: Lippenzone in s − Schrägversatz(u) von
    Lippe − 0,3 m bis Fuß + 0,5 m (Stufen ≥ 1 m: − 0,5 / + 1,5 m), quer bis Lippenbreite/2 − 0,3 m. Geprüft wird nach
    dem Setzen mit der Achse des gesetzten Netzes (gedrehte Bounds), wie im Prüfer.
  - Liegend modellierte Stücke weichen ≤ 30° von der Hangnormalen ab (Prüfer-Grenze 45°, Reserve für den 1-m-Boden);
    verkeilte und überspannende Stämme folgen der Normalen so weit, dass es ≤ 20° sind. Nach dem 1-m-Feinschliff
    entfernt `bachbett_neigung_1m` Stücke, die auf dem endgültigen Boden > 40° abweichen.
- **Lagen** (`bachbett_lagen_1m`, auf dem 1-m-Raster gegen den Boden nach dem Stempel):
  - Schlamm (Lava: Lavasand) in ruhigen, tiefen Becken (Ruhe 0 an Lippe/Kolk/Schnelle → Übergang zu Kies) und am
    Gleithang (Innenufer, ≤ 0,35 m tief); Kies darunter gedämpft.
  - Nasser Uferstreifen 0–1 m über dem Spiegel bis 3,5 m neben die Wasserkante: Schlamm/Erde/Moos je Biom, Summe 255
    (deckend). Wiese/Gras/Trockengras/Kraut/Heide dort auf 0 (wie die Nadelstreu in 13k), übrige Lagen × 0,4.
- **plan.json → `bachbett.abschnitte[<id>]`:** `stuecke` (Art, Netz, Lage, Achse, s/u, Unterkante über dem Spiegel,
  Kollision), `bestand` (Holzstufen), `dichte` je Segment (Ziel, gesetzt, abgelehnt, Waldfaktor, je 100 m), `lagen`
  (Streifen- und Schlamm-Fläche m²).
- **Prüfer** (`pruefe_bachbett`, FEHLER): Liste ↔ Instanz-Ebene, Kollision des großen Holzes am Wasser, kein Stück mitten
  in einer Lippe/einem Vorhang, Dichte je Segment im Rahmen (über max; unter min ab 60 m), Uferstreifen ≥ 80 % der
  Uferzellen (0,05–0,5 m über dem Spiegel bis 1,5 m neben dem Netzrand, außerhalb der Lippenzonen) mit Streifenlagen
  ≥ 200. Spiegel an schrägen Lippen über `bachbett.Lippenfeld` aus `lippe_form` und `segmente_m`.

## Nachtrag 3 zu 16c: Totholz nach Waldnähe, Feldgrenzen, Roh-Läufe (Koordinator 12.10.)

Antwort und Zahlen: „Nachtrag 3“ in `antworten/16c-ferat-ein-fluss-je-gewaesser.md`.

**Totholz nach Waldnähe** (`sehens_lib.bachbett.dichte`, Regeln v2): Der Baumanteil (4-m-Raster, Bäume ≥ 5 m) im Radius
40 m um den Bach zählt jetzt in jedem Biom. Ein Bach mit Bäumen am Ufer bekommt die Dichte des Ersatz-Waldbioms
(`wald_ersatz`, z. B. Tundra → Bergwald) × Waldfaktor, gewichtet mit g = glatt((Anteil − 0,01)/0,04). Baumlose Strecken
behalten ihr Biom („kaum“ bzw. 0) und bekommen Treibholz und Äste, wenn die 300 m Oberlauf bewaldet sind. Waldbiome
rechnen wie bisher. `plan.json → bachbett.abschnitte[*].dichte[*]` trägt dazu `wald_biom`, `wald_gewicht`,
`oberlauf_anteil`, `treibholz`, `rahmen_lw` [min, Ziel, max] und `palette`. Der Prüfer rechnet den Rahmen nach (Oberlauf
aus `spiegel_neu_cm`) und meldet eine Abweichung als FEHLER.

**Feldgrenzen mit zwei Plänen** (`gefaelle_daten.feldgrenzen`, 16d Punkt 3): Überlappen zwei Läufe 12–30 m an einer
Feldgrenze und haben beide Stufen, gehört eine Lippe nur in einen Plan: in den Plan ihres Felds (gleiches Feld: der obere
Lauf). Liegt beim ersten Legen eine Lippe in der Überlappung des Nachbarn oder läuft ein Becken hinein, wird die
Strecke mit dieser Zone als fester Zone neu gelegt (Spiegel dort alt, Anschluss passt). Der untere Lauf schließt erst
dort an, wo sein alter Spiegel nicht über dem des oberen liegt (`grenze_s_m` ≥ Feldgrenze `feldgrenze_s_m`). Ob der Nachbar Stufen bekommt, klärt ein Trockenlauf seiner
Stufenlage (`nachbar_hat_stufen`), unabhängig von `--laeufe`. `plan.json → feldgrenzen` (`ueberlappungen` mit
`fremd_s_m`, `grenze_s_m`, `nachbar_plan`, `lippen_in_fremd`; `neu_gelegt`). Der fluss_sim-Export schneidet die Kette an
`grenze_s_m`. Prüfer (`pruefe_feldgrenzen`): Lippe in einer fremden Überlappung = FEHLER, Geometrie nachgerechnet.

**Roh-Läufe** (`bachbett_roh.py`, Prüfer `bachbett_roh_pruefen.py`): Felsen, Totholz, Schlamm, Kies an Schnellen und
Uferstreifen für die Welt-Läufe ohne Stufenplan und die Reststrecken geplanter Läufe (Abstand 20 m zu den
Stufenstrecken). Keine Stufen, kein Gelände – nur Instanzen (Ebene `bachbett_roh`, `FT_EL_BBR_`) und Lagen. Format wie
die Gefälle-Pläne (`<aus>/<lauf>/plan.json` mit `spiegel_neu_cm` = Lauflinie, `abschnitte`, `bachbett`, `bereiche`),
Standard-Ausgabe lokal `export/unreal/welt/bachbett_roh/`. Ausgespart: Laufenden (3 m), Überlappungen, die der Export
kürzt, fremdes Wasser (Mündung, Seen, Teiche), Sehenswürdigkeiten (Radius + 10 m) und Felder mit lokaler Ufer-Ebene (nur
Felsen; `--ufer-felder`, lokal automatisch aus `ufer/foliage_<Feld>/`).

```
python -I recherche/antworten/skripte/gefaelle/bachbett_roh.py --gefaelle <gefaelle-Ausgabe> --daten2m recherche/vorlagen/daten/sehens \
       --aus <s>/bachbett_roh [--laeufe ID …] [--ohne-reststrecken] [--ufer-felder FELD …]
python -I recherche/antworten/skripte/gefaelle/bachbett_roh_pruefen.py <s>/bachbett_roh --daten2m recherche/vorlagen/daten/sehens
```

## Nachtrag 4 zu 16c: Hangeintrag Totholz, Roh-Ebene neben Ufer-Ebene (Koordinator 12.10.)

Antwort und Zahlen: „Nachtrag 4“ in `antworten/16c-ferat-ein-fluss-je-gewaesser.md`.

**Hangeintrag** (`sehens_lib.bachbett.baum_messung`, Regeln v3 `allgemein.hang`): In den Nicht-Waldbiomen (Tundra, Heide,
Ödland, Küste, Gletscher, Frost, Canyon, Wüste) zählen Bäume am Hang bis 150 m mit. Der Wald-Anteil ist der Ufer-Anteil
(40 m, wie bisher) plus der Hang-Anteil: Summe der Gewichte der Baumzellen 40–150 m, geteilt durch die Zahl der
Ufer-Zellen. Gewicht = Entfernung (40 m: 1, linear bis 0 bei 150 m) × Neigung (glatt von 3 % bis 15 % mittlerem Gefälle
Baum → Bach). Es zählen nur Zellen, die höher stehen als die Bachstelle und deren gerade Linie zum Bach keinen
Gegenanstieg über 3 m hat (Rücken, Querrinne). Gewertet wird die Bachstelle mit dem größten Gewicht. Waldfaktor,
Ufer-Wald-Gewicht und Treibholz am Oberlauf rechnen damit wie in Nachtrag 3. Waldbiome bleiben beim Ufer-Anteil.
`dichte[*]` trägt dazu `ufer_anteil`, `hang_anteil` und `hang_baeume` [Zellen mit Gewicht, Baumzellen 40–150 m]; der
Prüfer rechnet den Rahmen wie bisher nach.

**Roh-Ebene neben der Ufer-Ebene** (`bachbett_roh.py`, Regel `roh.ufer_ebene_ohne`): In Feldern mit lokaler Ufer-Ebene
(`ufer/foliage_<Feld>/`, `--ufer-felder`) setzt die Roh-Ebene weder Felsen noch Totholz; Schlamm, Kies im Bett und
Uferstreifen bleiben. Ein Segment ganz in solchen Feldern trägt `ufer_ebene: "ganz"` (keine Dichteprüfung), ein Segment
am Rand `ufer_ebene: "teil"` (abgelehnte Plätze zählen als blockiert). `plan.json → bachbett.totholz_ohne_felder`;
Prüfer: Totholz in diesen Feldern = FEHLER.

## Grenzen

- **2-m-Daten:** Ein 4-m-Bach ist dort nur 2 Zellen breit. Riser, Becken und Ufer verschmieren, deshalb gelten Bett- und
  Uferprüfung mit Rasterzuschlag. Lokal auf 1 m laufen lassen und streng prüfen.
- **Niagara-Grenze:** Mit ≤ 6 (Cull ≥ 30 m) + Zusatz-Aufprall (Cull 20 m) und hart ≤ 8 bleiben an dichten
  Kaskaden einzelne Stufen ≥ 1 m ohne FX (WARNUNG). Sie zeigen nur den Schaum im Netz.
- **Feste Zonen:** 36 von 161 Strecken sind `kaum_planbar` (< 15 m oder < 30 % frei). Meist sind sie sehr kurz oder
  liegen an Ort, Stadt, Sehenswürdigkeit oder fremdem Wasser.
- **Pivot und Schauseite** der Wand- und Riegelnetze sind angenommen (`front_achse` +y, „Pivot unten Mitte“). Bei
  Wandnetzen mit geringer Höhe (elfenwald max. 3,4 m) wird gestapelt.
- **Uferwulst:** Bis 1 m Anheben ist nötig, wo das alte Ufer kaum über dem Wasser liegt.
