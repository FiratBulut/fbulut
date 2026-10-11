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
python -I recherche/antworten/skripte/gefaelle/gefaelle_pruefen.py <aus> [--daten2m DIR | --daten1m DIR]
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
| `stufen` | je Stufe `lippe_cm` (3–7 Punkte, links → rechts mit Blick talwärts, Bogen mit Scheitel stromab), `ueberfall_cm`, `fuss_cm`, `fuss_z_cm`, `fall_m`, `art` (fall, kaskade oder schnelle; die Blockstufe wird als `kaskade` ausgegeben), `art_regel` (schnelle, stufe, kaskade oder fall), `teilstufen`, `kolk`, `klasse`, `biom`, `felstyp`, `holzstufe`, `vorhang` (≥ 3 m), `vorhang_niagara` (0,8–3 m) |
| `wasser_koerper` | Liste: `river` (Epic, `punkte` [x, y, z, breite, tiefe, velocity] + `punkt_typen`) und `kaskadennetz` (`s_m`, `mittellinie` [x, y, z, breite, tempo, fallanteil, schaum, abstand_bett], `knick` je Punkt: becken, lippe, bogen, wand, fuss, rampe; `rand_ueberstand_m` 0,4, `material`, `vorhang_an_stufen`, `pruefung`). Nachbarn überlappen 0,5 m. |
| `abschnitte` | je Strecke (lange Strecken: `_a1`, `_a2`, Fenster ≤ 600 m) `gelaende` (`datei`, `fenster_ij`, `max_aenderung_m`, `werkzeuge`: Bett, Kolk, Felsstufe, Klamm, Uferklippen), `lagen`, `budget`, `detail_ebenen` |
| `wandzonen` | Uferklippen/Klamm entlang des Laufs (s, Höhe, Grund, Wasserhöhe) |
| `instanzen`, `akteure` | Ebene `gefaelle` in `instanzen/<Feld>/plan.json` + f32 (FORMAT.md §3, FT-Präfix `FT_EL_GEF_`), Akteure dort in `plan["akteure"]` mit `klasse` `<abschnitt>_<gruppe>` |
| `effekte` | Nature Water FX (`typ: niagara`, `pos_cm`, `rot_q`, `skala`, `cull_m`, `stufe`, `rolle`), ≤ 3 je Stufe, ≤ 6 gleichzeitig |
| `kameras` | §8, je Pilot-Strecke `<id>_vorher`/`_nachher` (unterhalb der größten Stufe) und, wenn sichtbar, `<id>_weg_vorher`/`_nachher` vom Weg, `Hoch = -170` |
| `strecken` | Status, Rang, ausgesparte Zonen mit Grund, Segmente, Stufen-IDs, Arten, gestufter Fall |

## Ablauf (Regelwerk `ablauf`)

1. **Feste Zonen**, in denen der alte Spiegel bleibt: Wege und Pfade (Stempelschutz 4 m + 4 m Übergang), Orte, Städte,
   Sehenswürdigkeiten (Radius + 18 m), Umbau durch einen Sehens-Planer, Zuflüsse und fremdes Wasser, Anschluss 2 B an
   den Laufenden, Abschnittsgrenzen (±10 m).
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
5. **Gelände** (1-m-Delta, Rand 0): Bett = Spiegel − max(Tiefe; 0,5 m), Krone 0,15 m unter der Lippe, Kolk nach `kolk`,
   Böschung 35°, Uferklippe 60–90° (`ufer_klippen`), Klamm 85° mit `klamm.sohlbreite`, Uferwulst Spiegel + 0,15 m
   (höchstens 1 m anheben).
6. **Netze** je Biom am Stufenort (`biome.<biom>.netze`, gesperrte Netze werden übersprungen): Fallwand (held, Akteur),
   durchgehende Lippe aus Riegel-Netzen, Keystone + Stufenblöcke (`schutt.stufenblock_D`), Holz, Uferwände (Reihe beidseitig,
   hohe Wände in 2–3 Reihen übereinander), Sturzblöcke (`schutt.unter_fall`), Beckenblöcke, Wandschutt (`kegel_laenge`),
   Kies, Moos (Kontaktzone Nordseite).
7. **Lagen** nach `lagen.zonen` × `biome.<biom>.lagen`, **Effekte** nach `effekte.je_art`. Unter 3 m Fall gilt
   `NS_Waterfall_Small` + `NS_Impact_Small` (Koordinator, 14b), Cull 30–60 m (Heldenfälle bis 150 m). Danach wird auf
   ≤ 6 gleichzeitig ausgedünnt, große Fälle haben Vorrang.
8. **Wasserkörper** Variante A: Kaskadennetz von der ersten Lippe bis 1,5 m hinter den Fuß der letzten Stufe, River
   davor und danach. Prüfung (a) Bett ≥ 0,2 m unter dem Spiegel und (b) Ufer am Netzrand ≥ 0,1 m darüber, gegen das
   Gelände nach dem Stempel.

## Prüfer

`gefaelle_pruefen.py` prüft:
- Spiegel monoton, Anfang und Ende auf alter Höhe, nie über dem alten, Zwei-Punkt-Abstand, Becken ≤ 3 % (FEHLER) bzw. ≤ 2 % (WARNUNG), Rampen.
- Stufenhöhen gegen `stufen.arten`, Dichte, Lippenform.
- Wasserkörper: monoton, Überlappung genau 0,5 m, keine weitere Überlappung (auch in der Draufsicht), jede Stufe im Netz, Bett und Ufer am Netz, Niagara oder Vorhang je Stufe.
- Effekte: Inventar, ≤ 3 je Stufe, ≤ 6 gleichzeitig, Cull.
- Kameras.
- Gelände: Rand 0, |Δ| > 40 m, nicht ≤ 2 m an Weg/Pfad, ≤ 5 m an Ort, nicht in Sehenswürdigkeiten, Anheben > 1 m.
- Lagen-Dateien.
- Instanz-Ebene über `sehens_lib.sehens_pruefen.pruefe_ebene`: Format, Inventar, Feldrechteck, Budget §9 je Abschnitt, Schweben, Weg, dazu Ortsflächen.

Auf 2-m-Daten zählt eine Bett- oder Uferabweichung an höchstens 1 Punkt bzw. 10 % eines Netzes als WARNUNG
(Rasterverschmierung an kurzen Kaskadenbecken). Lokal auf 1 m gilt FEHLER.

## Testlauf 2 m (11.10.2026)

- **20 Pilot-Strecken (19 Läufe):** 299 Stufen, Prüfer **0 FEHLER**. Je Lauf bleibt 1 WARNUNG: Stufen ohne Niagara wegen
  ≤ 6 gleichzeitig, der Schaum liegt dann im Netz. Zwei Läufe ergeben byteidentische Ausgaben (`diff -r` ohne Bilder). Laufzeit ~40 s.
- **Alle 161 Strecken (`--alle`):** 123 Läufe, 76 mit Stufen, 731 Stufen (die Regel ohne Bündelung ergäbe ~2 300),
  **0 FEHLER**, ~90 s.
- `sehens_lib/selbsttest.py` und der Bergwald-Planer melden nach der additiven Lib-Änderung weiter 0 FEHLER.
  Die Änderung: `instanzen.Ebene(…, ebene_name, ft_praefix)`.
- Testbilder: `antworten/gefaelle/test_<strecke>.png`, oben die Draufsicht, unten das Längsprofil vorher und nachher.

## Grenzen

- **2-m-Daten:** Ein 4-m-Bach ist dort nur 2 Zellen breit. Riser, Becken und Ufer verschmieren, deshalb gelten Bett- und
  Uferprüfung mit Rasterzuschlag. Lokal auf 1 m laufen lassen und streng prüfen.
- **Gleichzeitig ≤ 6 Niagara** verträgt sich nicht mit Niagara an jeder Stufe: Bei Stufen alle 5–10 m bleibt etwa jede
  zweite Stufe ohne FX und zeigt nur Netzschaum.
- **Feste Zonen** sind streng. 76 von 161 Strecken sind `kaum_planbar` (< 15 m oder < 30 % frei), vor allem wegen
  Wegquerungen, Zuflüssen und Sehenswürdigkeiten.
- **Pivot und Schauseite** der Wand- und Riegelnetze sind angenommen (`front_achse` +y, „Pivot unten Mitte“). Bei
  Wandnetzen mit geringer Höhe (elfenwald max. 3,4 m) wird gestapelt.
- **Uferwulst:** Bis 1 m Anheben ist nötig, wo das alte Ufer kaum über dem Wasser liegt.
