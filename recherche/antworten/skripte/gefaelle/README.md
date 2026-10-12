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
- Instanz-Ebene über `sehens_lib.sehens_pruefen.pruefe_ebene`: Format, Inventar, Feldrechteck, Budget §9 je Abschnitt, Schweben, Weg, dazu Ortsflächen.

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
- `quer` (je Punkt `quer_punkte` = 11 Stützpunkte, Index 0 = rechts, Lage
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
