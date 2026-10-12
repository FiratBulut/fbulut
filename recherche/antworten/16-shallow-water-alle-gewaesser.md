# Entscheidung 16 – Shallow Water River für alle Bäche und Flüsse (dynamische Welt)

Stand 12.10.2026. **Ferat hat entschieden:** Alle Bäche und Flüsse laufen mit Epics **Shallow Water River**. Es geht nicht um einen Vorschlag
und nicht um einen Test mit offenem Ausgang. Ziel ist eine dynamische Welt: Später gesetzte Felsen und Geländeänderungen soll das Wasser selbst
erkennen, ohne Neuplanung.

## Umbau (verbindlich)

| Teil | Wer liefert | Was |
|---|---|---|
| Gelände, Stufen, Becken, Lippen | Planer (unverändert, 13f-Regel bleibt) | Form des Bachbetts |
| Wasseroberfläche Bäche + Flüsse | **WaterBodyRiver + ShallowWaterRiver** | Strömung, Füllen der Becken, Umfließen von Hindernissen, Kehrwasser |
| Fälle (Stufe ≥ 1 m, Schwelle wird im Einrichtungstest geprüft) | Kaskadennetz-Vorhang + Niagara (Nature Water FX) + Schaumobjekte | was 2D nicht kann |
| Hindernisse | jede Instanz/jeder Akteur im Wasser oder ≤ 1 m daneben: `wasser_kollision: true` | Wasser erkennt Felsen automatisch |
| Seen | bleiben `WaterBodyLake` | nicht Teil dieser Entscheidung |

**Planer-Ausgabe (neu):** Je Gewässerstrecke eine Liste `fluss_sim` mit Abschnitten zwischen den Fällen. Jeder Abschnitt hat Splinepunkte
(Lage, Breite, Tiefe, Fließgeschwindigkeit). Dazu je Fall einen Eintrag mit oberem/unterem Abschnitt, Vorhang, Effekten und Schaumobjekten
sowie eine Liste aller Objekte mit Wasser-Kollision. Das lokale Bau-Werkzeug erzeugt daraus `WaterBodyRiver` + `ShallowWaterRiver` und
setzt die Kollision.

**Bisherige Kaskadennetz-Oberfläche** in Becken und flachen Strecken wird durch die Simulation ersetzt. Ob sie als ferne Darstellung bleibt,
hängt von Reichweite und Kosten der Simulation ab (Einrichtungstest unten).

**Die Simulation wird gebacken (Ferat, 12.10.):** Sie läuft im Editor, das gebackene Ergebnis steht im Spiel fest und kostet kaum
Leistung. Nach Detailänderungen (Felsen setzen, Gelände ändern) werden nur die betroffenen Back-Kacheln neu gebacken. Ablauf siehe
„Arbeitsablauf“ unten.

**Offene Risiken (ehrlich, Stand nach der Back-Entscheidung):**
- **Laufzeitkosten** sind durch das Backen weitgehend erledigt. Kein Simulationsbereich um den Spieler mehr nötig; es bleiben die Kosten
  der gebackenen Darstellung (Texturen, Material) und die Effekte an den Fällen (bestehende Niagara-Grenzen).
- **Offen ist der gebackene Zustand selbst:** ob und wie Shallow Water River in 5.8 ihn speichert (Format, Speicherbedarf je Kachel,
  Backzeit, Streaming mit World Partition). Belegt ist nur, dass es gebackene Simulationsdaten gibt (Abschnitt „Umsetzung Cloud“,
  Recherche). Grobe Schätzung bei 555 Kacheln: 0,5–2,2 GB Texturen, je nach Auflösung 256² oder 512² (Ableitung, nicht gemessen).
  Das klärt die lokale Instanz im Einrichtungstest.
- Ein Forenbericht meldet einen Startfehler in 5.7.4. Laut Ferats Video läuft es in 5.8.
- Ob Wasser-Kollision bei instanzierten Felsen (HISM/Foliage) wirkt und wie die Einstellung genau heißt, ist offen.

## Einrichtungstest (lokal, vor dem Gesamtbau)

Die Teststrecken und Fragen unten bleiben gültig. Sie dienen jetzt der **Einrichtung**: Werte, Schwelle für Fälle, Reichweite, Budget,
Kollisionseinstellung. Es ist keine Ja/Nein-Entscheidung mehr. Dazu kommen die Back-Fragen in „Umsetzung Cloud“, Abschnitt 6.

## Arbeitsablauf (gebacken)

```
einrichten  ->  backen  ->  Details bearbeiten  ->  betroffene Kacheln neu backen  ->  fest
```

1. **Einrichten** (einmal, Einrichtungstest an C2 und einem Sehens-Ort): Plugins Water, Water Advanced und Niagara Fluids; Projekt-
   einstellung Shallow Water Simulation; Kollisionseinstellung für Felsen; Auflösung je Kachel; Schwelle für Fälle; Back-Ablage.
2. **Bauen und backen** (je Kachel aus `back_liste.json`): `WaterBodyRiver` je Abschnitt, `ShallowWaterRiver` je Kachel, Wasser-
   Kollision an den gelisteten Objekten, Kaskadennetz nur an Fällen, Schaumobjekte. Reset, laufen lassen, bis das Wasser die Senke
   erreicht, backen. Danach den **Editor-Fingerabdruck** der Kachel berechnen und mit dem Backstand speichern.
3. **Details bearbeiten**: Felsen setzen, verschieben oder löschen (mit Wasser-Kollision), Gelände modellieren, Spline anpassen.
4. **Betroffene Kacheln neu backen**: Das Werkzeug rechnet für jede Kachel den Fingerabdruck aus dem Editor-Zustand neu
   (Formel in `skripte/fluss_sim/README.md`, Abschnitt „Fingerabdruck“). Geändert → neu backen. Nach einer Neuplanung (neuer Export)
   zusätzlich die Planer-Fingerabdrücke der alten und neuen `back_liste.json` vergleichen.
5. **Fest**: Alle Kacheln haben einen aktuellen Backstand; im Spiel läuft nur das gebackene Ergebnis.

## Umsetzung Cloud (Stand 12.10.2026)

Commits: siehe Abschnitt 8. Code: `skripte/fluss_sim/` (Exporter, Prüfer, Regeln, README mit dem vollständigen Format).
Beispiele: `antworten/fluss_sim/` (C2, Sehens-Ort `bergwald_06_karsee`, Zusammenfassung, Auszug der Back-Liste).

### 1. Kurzfazit

- **Neuer, eigenständiger Exporter** `fluss_sim_export.py`. Er liest nur die Planer-Ausgaben (Gefälle-Pläne, Sehens-`orte.json`,
  Instanz-Ebenen, Gelände-Deltas) und ändert keine Stufe, kein Becken und kein Gelände. Die 13f-Treppen der Sehens-Bäche bleiben exakt;
  der Prüfer vergleicht Lippen- und Fußhöhen jedes Falls mit der Quelle (±2 cm).
- **Lauf über alles (2 m):** 177 Gewässer, 35,4 km Wasserlinie, **1 120 Abschnitte, 765 Fälle, 22 820 Objekte mit Wasser-Kollision,
  5 562 Schaumobjekte, 555 Back-Kacheln**.
- **Prüfer: 0 FEHLER, 0 WARNUNG**, 10 HINWEIS (Fälle, deren Fuß in einem See liegt). Zwei Läufe sind byte-gleich (163 Dateien).
  Gegenproben mit absichtlich verfälschten Daten ergeben FEHLER.
- **Back-Liste:** je Kachel ein SHA-256-Fingerabdruck aus Gelände, Splines und Kollisionsobjekten. Das lokale Werkzeug rechnet dieselbe
  Formel aus dem Editor und backt nur geänderte Kacheln neu, auch nach Handänderungen.
- **13k war beim letzten Lauf fertig:** `13k-pilot2-bildbefund-15g-nachtrag.md` liegt im Remote-Branch (Commit `2e36947`). Die
  Planer-Ausgaben stammen vom Code-Stand `97e82a3` (danach keine Planer-Änderung).

### 2. Was der Exporter ausgibt

Je Gewässer eine `fluss_sim.json` (Gefälle-Lauf, Sehens-Ort oder Fluss), dazu `back_liste.json` und `zusammenfassung.json`.
Gefälle-Pläne gelten je **Lauf** (ein Lauf kann mehrere der 161 Strecken enthalten, `strecken` nennt sie). Gekürzt aus C2:

```json
{"id": "F_ERLENBACH_1V_C2", "kategorie": "gefaelle", "quelle": {"plan": "gefaelle/F_ERLENBACH_1V_C2/plan.json"},
 "abschnitte": [{"id": "F_ERLENBACH_1V_C2_A01", "s_m": [14.75, 21.85],
   "punkte": [[-172690.6, -238034.1, 9818.7, 2310.2, 228.2, 150.0], ...],
   "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
   "punkt_typen": ["CURVE_CLAMPED", ..., "LINEAR", "LINEAR", ...], "tangenten_cm": [[-64.7, 121.7, -2.8], ...],
   "anschluss": {"oben_fall": "..._S01_T2", "unten_fall": "..._S01_T4", "spiegel_anfang_cm": 9818.7, "spiegel_ende_cm": 9717.6},
   "becken": [{"s_m": [14.75, 18.87], "spiegel_cm": [9818.7, 9810.4]}, ...], "faelle_innen": []}, ...],
 "faelle": [{"id": "F_ERLENBACH_1V_C2_s1_S04", "fall_m": 4.67, "abschnitt_oben": "..._A04", "abschnitt_unten": "..._A05",
   "lippe_cm": [-174147.3, -234539.3, 8884.6], "fuss_cm": [-174161.7, -234491.4, 8417.3], "strahl_breite_m": 1.76,
   "kaskadennetz": {"id": "..._KN0", "bereich_s_m": [52.15, 54.65], "vorhang": true},
   "effekte": [{"quelle": "gefaelle/.../plan.json#effekte", "index": 3, "asset": "/Game/NatureWaterFX/FX/NS_Impact_Small", "cull_m": 45.0}, ...],
   "schaum_objekte": [{"art": "aufprallteppich", "pos_cm": [-174237.4, -234256.2, 8418.3], "groesse_m": [6.17, 8.99],
                       "drehung_yaw_grad": 106.9, "seed": 762259202},
                      {"art": "schaumstrasse", "punkte_cm": [[-174236.3, -233987.7, 8408.5], ...], "groesse_m": [2.32, 0.39]},
                      {"art": "kehrwasser", "pos_cm": [...], "groesse_m": [1.2, 1.2], "grund": "neben dem Aufprall (links)"}]}],
 "wasser_kollision": [{"ref": {"quelle": "gefaelle/F_ERLENBACH_1V_C2/instanzen/C2/plan.json",
                               "datei": "SM_ForestRockFormation_05_kol", "index": 2},
                       "pfad": "/Game/Megascans/3D_Assets/ForestRockFormation/SM_ForestRockFormation_05",
                       "lage": "im_wasser", "abschnitt": "..._A08", "kollision_im_plan": true, "wasser_kollision": true}, ...],
 "sim_bereiche": [{"id": "F_ERLENBACH_1V_C2_K00", "bereich_cm": [-177406.5, -241656.6, -169942.9, -229584.4],
                   "abschnitte": ["..._A00", ..., "..._A07"], "source_river": "..._A00", "sink_river": "..._A07",
                   "grenze_oben": "laufanfang", "grenze_unten": "fall", "fingerabdruck": "1bae85d4...", "n_objekte": 336}]}
```

`RiverWidth`, `Depth` und `WaterVelocityScalar` sind die Felder von `UWaterSplineMetadata` (je Splinepunkt, `FInterpCurveFloat`; Epic:
„The Depth of the water at this vertex“, „The Current of the water at this vertex“) [Doku, Auszug]. **Achtung RiverWidth:** Der
Doku-Kommentar lautet „Rivers Only: The width of the river (from center) in each direction“. Das kann volle Breite oder halbe Breite
bedeuten. Der Export gibt wie A15 die **volle Wasserbreite**; die lokale Instanz prüft das im Einrichtungstest an einem Abschnitt mit
bekannter Breite.

**Regeln (Kurzform, Zahlen in `fluss_sim_regeln.json`):**

| Teil | Regel |
|---|---|
| Fall | Einzelabsturz ≥ 1,0 m ohne Rampe (Stufe ohne Teilstufen bzw. jede Teilstufe einer Kaskade). Kleinere Abstürze bleiben im Abschnitt, Spline Lippe → Fuß `LINEAR`. |
| Abschnitt | je Becken vom Fuß des oberen bis zur Lippe des unteren Falls; Spiegelhöhen unverändert aus der Quelle, Punkte ≤ 2 m. |
| kurze Becken | < 4 m (≈ 3,4 Water-Info-Texel bei 1,18 m, 14b) werden mit dem talwärts folgenden Abschnitt zusammengefasst; der Fall liegt dann innen (`faelle_innen`), Vorhang und Effekte bleiben. Betrifft 141 von 765 Fällen, vor allem Sehens-Treppen mit 2–3-m-Becken. |
| lange Abschnitte | Teile ≤ 112 m (Kachel 128 m − 2 × 8 m), bei breiten Flüssen kürzer; gemeinsamer Endpunkt. |
| Wasser-Kollision | fest (Kollision im Plan, Fels, Holz; nie Pflanzen), Grundriss ≥ 0,4 m, Höhe ≥ 0,2 m, im Wasser oder ≤ 1 m neben der Wasserfläche, Unterkante ≤ Spiegel + 0,5 m. |
| Schaum | Aufprallteppich (r = 0,5–1 × Fallhöhe), 2–6 Schaumstraßen (2–4 m), Kehrwasser neben dem Aufprall, im Lee von Randblöcken und in Buchten (15g-`ufer_rand`); Gischt = vorhandene Niagara-Effekte. |
| Back-Kachel | aufeinanderfolgende Abschnitte bis 128 m (Bounding-Box + 2 × 8 m Rand), Grenzen bevorzugt an Fällen. |

Schaum-Netze und Decals wählt das lokale Werkzeug; im Inventar stehen als Kandidaten `MI_EL_Fluss_Schaum` und
`MI_EL_Stufenfall_Schaum` (`inventar_extra.json`). Andere Asset-Namen nennt der Export nicht.

### 3. Zahlen (2 m, letzter Lauf)

| Kategorie | Dateien | Gewässer | Länge km | Abschnitte | Fälle | davon im Abschnitt | Kollision (im Wasser) | Schaumobjekte (Teppich/Straße/Kehrwasser) | Kacheln |
|---|---|---|---|---|---|---|---|---|---|
| Gefälle-Läufe mit Plan (161 Strecken, C2 inkl.) | 98 | 98 | 23,3 | 745 | 561 | 47 | 21 021 (20 558) | 561 / 1 719 / 1 992 | 304 |
| Läufe der 161 Strecken ohne Plan (roh) | 25 | 25 | 4,0 | 75 | 0 | 0 | 353 (302) | – | 64 |
| Sehens-Bäche (15 Biome) | 26 | 42 | 1,8 | 135 | 204 | 94 | 1 732 (1 386) | 204 / 788 / 298 | 46 |
| Flüsse ≥ 15 m ohne Plan (roh) | 12 | 12 | 6,3 | 165 | 0 | 0 | 291 (265) | – | 141 |
| **Summe** | **161** | **177** | **35,4** | **1 120** | **765** | **141** | **23 397 (22 511)**, eindeutig 22 820 | **765 / 2 507 / 2 290** | **555** |

- **Flüsse ≥ 15 m:** Alle 27 Flüsse aus `wasser_welt.json` sind ≥ 15 m breit (größte Breite je Fluss). 9 haben einen Gefälle-Plan
  (u. a. C2, `F_ERLENBACH_2V_D3`, `F_ELFENFLUSS_3_H4`, `F_HAUPTFLUSS_3_C5`), 6 sind Läufe der 161 Strecken ohne Plan
  (z. B. `F_ELFENFLUSS_2_H4` mit den A14-Schnellen), 12 werden nur als Fluss exportiert (u. a. `F_HAUPTFLUSS_3_D5/E5/F5`,
  `F_DSCHUNGELFLUSS_H6`).
- **Läufe ohne Plan** (25): Läufe der 161 Strecken, für die der Planer keine Stufe legt (kaum planbar, < 15 m, feste Zonen). Sie
  bekommen Abschnitte aus dem rohen Lauf, keine Fälle.
- **C2:** 18 Abschnitte, 24 Fälle (5 im Abschnitt), 625 Kollisionsobjekte, 3 Kacheln (75 × 121 m, 60 × 107 m, 44 × 74 m), Grenzen
  an Fällen. 19 Stufen ergeben 24 Fälle, weil jede Teilstufe einer Kaskade ≥ 1 m ein eigener Fall ist.
- **Sehens-Beispiel `bergwald_06_karsee`:** Abfluss 45 m mit 12 Fällen (1,1–12 m) in 7 Abschnitten, Zuläufe Süd und West mit je 6
  Fällen in 2 Abschnitten; der letzte Fall jedes Zulaufs mündet in den See (`abschnitt_unten` = null).
- **Kacheln:** Median 105 m, 28 Kacheln größer als 128 m, alle an Flüssen mit 85–222 m Breite (größte 246 m, `F_HAUPTFLUSS_3_F5`).
  Grenzen: 35 Kacheln mit Fällen an beiden Enden, 71 umfassen einen ganzen Lauf, 353 haben mindestens eine offene Grenze in
  fließendem Wasser (lange Läufe und Flüsse, die in 112-m-Stücke geteilt werden).
- **Größe:** 17 MB auf 2 m. Ins Repo kommen nur die Beispiele; der Rest ist mit den Befehlen in Abschnitt 4 erzeugbar.

### 4. Befehle

```
# Planer-Ausgaben (Scratchpad, nicht ins Repo)
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --alle --daten2m recherche/vorlagen/daten/sehens --aus <s>/gef
python -I recherche/antworten/skripte/sehens_<biom>/sehens_<biom>.py --daten2m recherche/vorlagen/daten/sehens --aus <s>/sehens/<biom>
# Export und Prüfung
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle <s>/gef --sehens <s>/sehens \
       --daten2m recherche/vorlagen/daten/sehens --aus <s>/fs
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_pruefen.py <s>/fs --gefaelle <s>/gef --sehens <s>/sehens \
       --daten2m recherche/vorlagen/daten/sehens --vergleich <s>/fs2
# lokal 1 m
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle \
       --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt --aus export/unreal/welt/fluss_sim
```

**Prüfergebnis (letzter Lauf):** 0 FEHLER, 0 WARNUNG, 10 HINWEIS. Geprüft: Spline durchgehend und nie steigend, Becken waagrecht
(≤ 3 %), Breite/Tiefe > 0, Velocity ≤ 1024 cm/s, jede Stufe ≥ 1 m aus der Quelle ist ein Fall mit Lippe/Fuß ±2 cm, kein Becken ohne
Abschnitt, Beckenspiegel ±2 cm, jedes Objekt im Wasser in `wasser_kollision`, Schaum im Wasser und auf dem Spiegel, jeder Abschnitt in
genau einer Kachel, Fingerabdrücke neu gerechnet (auch Gelände), zwei Läufe byte-gleich.

**Beobachtung am Rand:** Der Gefälle-Planer meldet auf 2 m seit den 13k-Regeln der gemeinsamen Bibliothek 189 FEHLER (gesägte
`*_log`-Stämme in der Wildnis, mehr als 50 Akteure je Ort, z. B. C2 mit 62). Die Pläne werden trotzdem vollständig geschrieben, der
Export liest sie unverändert. Das gehört zum Gefälle-Planer, nicht zu diesem Auftrag.

### 5. Was das lokale Bau-Werkzeug tun muss

1. **Exporter lokal auf 1 m laufen lassen** (Befehl oben) und den Prüfer mit `--daten1m`. Die Cloud-Ausgabe ist nur ein Muster.
2. **Bisherige Wasserkörper ersetzen:** Die `river`-Stücke aus `wasser_koerper` und die Kaskadennetz-Flächen in Becken entfallen.
3. **Je Abschnitt ein `WaterBodyRiver`:** Splinepunkte aus `punkte` (Weltlage in cm), Punkttyp aus `punkt_typen` (`LINEAR` an
   Lippe/Fuß), Tangenten aus `tangenten_cm`, Metadaten `RiverWidth`, `Depth`, `WaterVelocityScalar` je Punkt. Landschaft nicht
   verändern (`affects_landscape: false`, das Gelände kommt aus dem Planer-Delta). Akteur-Tag bzw. Label = Abschnitt-ID.
4. **Je Kachel ein `ShallowWaterRiver`:** mit den Abschnitten der Kachel verknüpfen, `source_river` = erster, `sink_river` = letzter
   Abschnitt; Auflösung nach Einrichtungstest. Wenn nur ein River je Simulation geht: je Abschnitt ein `ShallowWaterRiver`
   (Grenzen liegen dann an Fällen, unter Vorhang und Aufprallschaum).
5. **Wasser-Kollision setzen:** an jedem Objekt in `wasser_kollision` (Instanz `quelle` + `datei` + `index` bzw. Akteur), auch wenn
   es im Plan keine Kollision hat (`kollision_im_plan: false`). Dieselbe Regel (README, „Wasser-Kollision“) auf alle anderen Ebenen
   der Kachel anwenden (Bestand, Felsgruppen, Witcher), die in der Cloud fehlen.
6. **Kaskadennetz nur noch an Fällen:** das bisherige Netz auf `kaskadennetz.bereich_s_m` jedes Falls zuschneiden (Lippe − 0,5 m bis
   Fuß + 1,5 m), Vorhang nur bei `vorhang: true`, Effekte aus `effekte` unverändert.
7. **Schaumobjekte** setzen: Lage, Größe, Drehung, Art; Netz/Decal nach eigener Wahl aus dem Inventar. Schaumstraßen folgen der
   gebackenen Strömung, wenn sie sich auslesen lässt, sonst `punkte_cm`.
8. **Backen** je Kachel, danach Editor-Fingerabdruck berechnen und mit dem Backstand speichern (README, „Fingerabdruck“).
9. **Werkzeug „Wasser-Kollision an Auswahl“** für Handarbeit und die Neu-Back-Prüfung über alle Kacheln.

### 6. Offene Punkte für den Einrichtungstest

| Frage | Wozu |
|---|---|
| Wie heißt die Einstellung, mit der die Simulation Felsen erkennt? Kollisionsprofil/-kanal (Forum: „Water Body Collision Response“ fehlt im 5.6-Standardprojekt), Distance Field oder Bodenhöhe der Water Info (`WaterTerrainComponent`, ab 5.5)? Wirkt sie bei ISM/HISM/Foliage? | Feld `wasser_kollision` umsetzen |
| Wie speichert 5.8 den gebackenen Zustand (Texturen, Asset, `WaterBodyCustom` mit `baked_shallow_water_sim`)? Speicher je Kachel, Backzeit je Kachel, Streaming mit World Partition | Back-Ablage, Budget |
| Kann ein `ShallowWaterRiver` mehrere River verknüpfen (Quelle/Senke als Liste) oder nur einen? | Kachel = Gruppe oder je Abschnitt |
| `RiverWidth` = volle oder halbe Breite? | Breite im Export |
| Auflösung (`resolution_max_axis`) und Zellgröße für 128-m-Kacheln; Naht an offenen Kachelgrenzen (353 Kacheln); bei sichtbarer Naht Kacheln überlappen lassen oder größer wählen | Kachelgröße, Überlappung |
| Füllt die Simulation die Becken bis zur Lippe und fließt sie über Abstürze < 1 m sauber? Ist 1 m die richtige Schwelle? | `fall_schwelle_m` |
| Kurze Abschnitte (4 m): zeichnen sie Lücken? Sonst `min_laenge_m` senken | Regel kurze Becken |
| Nach dem Backen: Bleiben River-Einstellungen wirksam? (Forum: manche wirken nach dem Backen nicht mehr) | Reihenfolge Werte → Backen |
| Lässt sich die gebackene Strömung auslesen (Velocity-Textur), damit Schaumstraßen ihr folgen? | Schaumstraßen |

### 7. Recherche Shallow Water River (Epic-Doku, Forum)

`dev.epicgames.com` und `forums.unrealengine.com` waren aus der Cloud wie in 14b nicht direkt lesbar (Proxy 403, WebFetch DNS-Fehler).
Die Belege stammen aus **Suchmaschinen-Auszügen** der verlinkten Seiten; YouTube ist gesperrt. Kennzeichnung wie in 14b:
[Doku], [Forum], [Ableitung], [ungeprüft].

- **Aufbau:** `AShallowWaterRiver` mit `UShallowWaterRiverComponent` im Plugin **WaterAdvanced** (`ShallowWaterRiverActor.h`). Das
  Niagara-System der Simulation wird in den Projekteinstellungen unter Plugins → Water ShallowWaterSimulation gesetzt [Doku].
- **Eigenschaften (Python 5.5):** `resolution_max_axis` (int32), `sim_speed`, `source_size`, `source_river_water_body`,
  `sink_river_water_body` (je ein WaterBody), `river_sim_system` (NiagaraComponent, nur lesbar), `water_info_texture`
  (TextureRenderTarget2DArray) [Doku]. Ein japanischer Leitfaden beschreibt für 5.6 eine Quell-Liste; ein River in der Quelle wird
  automatisch auch Senke [Auszug, ungeprüft].
- **Backen:** Die C++-Komponente hat gebackene Simulationsmaterialien, gebackene Schaum- und Oberflächentexturen, eine CPU-Drossel und
  eine Option zum Anpassen an die Spline [Doku]. In 5.7 hat `WaterBodyCustomComponent` ein nur lesbares `baked_shallow_water_sim`,
  „baked simulation data owned by a ShallowWaterRiverComponent“ [Doku]. Daraus folgt: Das Backen erzeugt Texturen bzw. Daten, die ein
  Water Body anzeigt [Ableitung]. Format, Größe und Backzeit sind nicht belegt [ungeprüft].
- **Ablauf im Editor:** Nach Änderungen an den Rivers „Reset“ drücken, nach dem Bearbeiten „Bake“. Einige River-Einstellungen wirken
  nach dem Backen nicht mehr, weil die Simulation die River-Ebene überschreibt [Forum]. Backen, wenn das Wasser das Ende erreicht hat
  [Auszug, ungeprüft].
- **Kollision mit Meshes:** Unter World Partition brauche jedes Kartenstück eine Kollisions-Kennung; zu stark vergrößerte Splines
  verlieren Kollision, teils nur in einem Teil des Flusses [Forum]. Das Profil „Water Body Collision“ fehle im 5.6-Standardprojekt
  [Forum]. Am `ShallowWaterRiver` selbst gibt es keine Kollisionseinstellung, Overlap-Events kommen nicht an [Forum]. Das Subsystem
  verwaltet Kollisions-Kontexte und -Tracker für Akteure und Physik-Assets (Interaktion bewegter Körper) [Doku]. Niagara-Fluids-
  Kollision mit Static Meshes läuft allgemein über Mesh Distance Fields markierter Netze [Drittquelle]. Welche Einstellung Felsen in die
  Shallow-Water-Simulation bringt, ist damit **nicht belegt** → Einrichtungstest.
- **Reichweite:** Die Simulation deckt die Bounds ihrer River ab; die Auflösung richtet sich nach `resolution_max_axis` [Doku-Feld,
  Ableitung]. Mit dem Backen ist die Laufzeit-Reichweite um den Spieler nicht mehr nötig. Die Projekteinstellungen begrenzen aktive
  Pawns und Impulse für die Interaktion [Doku].
- **Bekannte Fehler:** River verschwindet nach dem Kompilieren (verschieben/Reset/neu anlegen) [Forum]; Shallow Water Body wird nicht
  gezeichnet [Forum]; Startfehler in 5.7.4 (oben) [Forum].

### 8. Commits

| Was | Commit |
|---|---|
| Exporter, Prüfer, Regeln (Zwischenstand) | `8c0406d` |
| README, Beispiele, diese Umsetzung, Endlauf | Commit dieser Datei |

---
*Ursprünglicher Vorschlag (zur Nachvollziehbarkeit):*

## Kurzfazit (Vorschlag)

- **Shallow Water River** ist seit UE 5.6 Teil von Water + Niagara Fluids und kostenlos. Er simuliert die Wasseroberfläche eines Flusses (`WaterBodyRiver`):
  Strömung um Hindernisse, Füllen von Becken, Wellen. Die Lage des Flusses gibt weiter die Spline vor.
- **Erwartung:** Ränder, Strömung und Schaum werden natürlicher. Die 15g-Punkte „eckiger Schaum“ und „gerade Ränder“ könnte er besser lösen als Regeln.
- **Grenze:** Er rechnet 2D, also eine Höhe pro Punkt. Senkrechte Fälle und Vorhänge (Stufen ≥ 3 m) kann er nicht darstellen. Die bleiben bei Kaskadennetz und Niagara.
- **Plan:** Zuerst testen, ob er auf unseren gebauten Stufen läuft und was er kostet. Danach entscheiden:
  - **Hybrid:** Unser Kaskadennetz liefert Stufen und Fälle, Shallow Water den Abschnitt in Spielernähe.
  - **Einbacken:** Wir übernehmen nur Strömung, Tiefe und Schaum als Flowmap bzw. Vertexwerte.

## Test (lokal, etwa 1–2 h)

1. **Plugins:** Water und Niagara Fluids aktiv.
2. **Abschnitt T1:** C2 Version 3, etwa 40 m um `kn0_nah_s119` mit 3–4 Lippen und einer Gumpe.
   - `WaterBodyRiver` entlang der `mittellinie` aus dem Plan (`0e00d17`) setzen. Breite und Tiefe je Punkt aus `breite` / `tiefe_cm`.
   - `ShallowWaterRiver` setzen, mit dem Fluss verknüpfen und Reset.
   - Das Kaskadennetz in diesem Abschnitt für den Test ausblenden.
3. **Abschnitt T2:** Treppenbach am Karsee mit dem 10,8-m-Fall S00. Hier soll sich zeigen, wo die Grenze liegt.
4. **Abschnitt T3:** ein flacher Abschnitt mit Biegung, als Vergleich.

### Bitte zurückmelden

| Frage | Wozu |
|---|---|
| Läuft die Simulation auf eigenem Fluss + 1-m-Gelände? Ein Forenbericht meldet einen Startfehler in 5.7.4, einzeln und unbestätigt. | Grundvoraussetzung |
| Füllt sie die Becken bis zur Lippe und fließt über die Lippen? | Kernfrage für Stufen |
| Verhalten an Stufen 0,3–1 m bzw. ≥ 3 m | Grenze 2D |
| GPU-Zeit (`stat GPU`, `stat Niagara`) je Abschnitt, Größe und Auflösung des Simulationsbereichs | Budget offene Welt |
| Läuft sie nur um die Kamera oder über den ganzen Fluss? Wie weit reicht sie? | Hybrid-Planung |
| Kann man Höhe, Geschwindigkeit und Schaum als Textur oder Zustand **speichern**? (Render Target exportieren, Einback-Funktion) | Einbacken ja/nein |
| Bilder von denselben Kameras wie in 15g: `s1`, `kn0_unten`, `kn0_nah_s119` | Vergleich mit Version 3 |
| **Nachbearbeitung:** einen Megascans-Felsen (Static Mesh) mitten in den Fluss stellen und Landschaft leicht modellieren, dann Reset. Reagiert die Strömung auf beides oder nur auf die Landschaft? Braucht der Fels Kollision bzw. Distance Field? | Ferats Wunsch: Details später ändern, ohne neu zu planen |

## Entscheidung danach

- **Läuft gut und Export möglich:** Wir übernehmen Flowmap, Tiefe und Schaum als Feld je Kaskadennetz. Der Planer liefert dann nur noch Stufen, Gelände und Fälle.
- **Läuft gut, aber nur live:**
  - Wir setzen Shallow Water nur an Sehenswürdigkeiten ein, nah am Spieler.
  - Grenzen: höchstens etwa 1,5 ms GPU; zusammen mit den Niagara-Effekten höchstens 8 gleichzeitig (bestehende Regel).
  - Fern übernimmt das Kaskadennetz.
- **Läuft nicht, oder nicht auf Stufen:** Wir bleiben beim Kaskadennetz und den SLW2-Werten.
- **Fluid Flux** (kostenpflichtig, kann Zustände einbacken) bleibt erst einmal draußen. Eine Frage für Ferat wird es erst, wenn der kostenlose Weg nicht reicht.

## Nachtrag: Fälle bleiben beim Kaskadennetz, dazu gezielt platzierter Schaum

Ferat (12.10.): Für die Wasserfälle ist das Kaskadennetz wahrscheinlich besser geeignet; realistischer wird es, wenn man nur Schaum gezielt platziert. Dafür sind
nach dem Test diese Schaumarten als eigene Objekte vorgesehen, statt nur Vertexschaum im Netz:

| Art | Wo | Form |
|---|---|---|
| Aufprallteppich | Fallfuß jeder Stufe ≥ 1 m | unregelmäßiger Fleck, Radius ≈ 0,5–1 × Fallhöhe, an den Rändern ausgefranst |
| Schaumstraßen | vom Aufprall talwärts in Hauptströmung | 2–6 dünne, gebogene Streifen, 2–4 m lang, auslaufend |
| Kehrwasserschaum | Buchten und hinter Randblöcken (15g) | kleine kreisende Flecken, ruhend |
| Gischt | Fälle ≥ 3 m | Niagara aus Nature Water FX (bestehende Effekte, `cull_m` aus 13k) |

Die Umsetzung erfolgt als Decals bzw. flache Schaumkarten (Netze und Materialien nur aus dem vorhandenen Inventar). Liefert Shallow Water später eine
Strömung, folgen die Schaumstraßen ihr; sonst folgen sie der `mittellinie`. Den Planer-Ausbau (Feld `schaum_objekte` je Kaskadennetz) mache ich, sobald
die Bilder von C2 Version 3 und dem Test da sind.

## Nachtrag: Felsen brauchen Wasser-Kollision

Ferat (12.10., aus dem Video): Felsen werden von der Simulation erkannt, wenn bei ihnen die **Wasser-Kollision** eingestellt ist. Folgen:

- **Test:** Den Felsen aus der Testfrage „Nachbearbeitung“ einmal mit und einmal ohne diese Einstellung prüfen. Den genauen Namen der Einstellung bzw. des
  Kollisionsprofils in 5.8.3 bitte zurückmelden. Prüfen, ob sie auch bei **instanzierten** Felsen (ISM/HISM, Foliage) wirkt oder nur bei einzelnen Akteuren.
- **Planer (nach dem Test):** Jede Instanz und jeder Akteur, der im Wasser oder bis 1 m daneben steht (Blöcke in Stufen, Randblöcke aus 15g, Felsnasen),
  bekommt ein Feld `wasser_kollision: true`. Das lokale Bau-Werkzeug setzt damit die Einstellung automatisch, auch bei späteren Neuplanungen.
- **Handarbeit später:** Von Hand gesetzte Felsen im Fluss brauchen dieselbe Einstellung. Am einfachsten geht das über eine eigene Kollisions-Voreinstellung
  bzw. ein Editor-Werkzeug „Wasser-Kollision an Auswahl“. Dann reagiert das Wasser nach einem Reset bzw. Neu-Einbacken ohne neue Planung.

## Rückfrage

- Ferat: Wie heißt das Video bzw. der Kanal? Dann kann ich die gezeigten Einstellungen gezielt nachrecherchieren.

## Quellen

Zur Umsetzung Cloud (Abschnitt 7; Inhalte aus Suchmaschinen-Auszügen, Seiten aus der Cloud nicht direkt lesbar):

- [Epic API: AShallowWaterRiver (WaterAdvanced)](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/WaterAdvanced/AShallowWaterRiver)
- [Epic API: UShallowWaterRiverComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent?lang=en-US)
- [Epic Python 5.5: unreal.ShallowWaterRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent?application_version=5.5)
- [Epic Python 5.5: unreal.ShallowWaterRiver](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiver?application_version=5.5)
- [Epic Python 5.7: unreal.WaterBodyCustomComponent (`baked_shallow_water_sim`)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyCustomComponent?application_version=5.7)
- [Epic API: UShallowWaterSettings](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterSettings?lang=en-US)
- [Epic API: UShallowWaterSubsystem](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterSubsystem)
- [Epic API: UWaterSplineMetadata (RiverWidth, Depth, WaterVelocityScalar)](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterSplineMetadata)
- [Epic API: FPCGWaterSplineMetadataStruct](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/PCGWaterInterop/FPCGWaterSplineMetadataStruct)
- [Epic Blueprint: Set River Width at Spline Input Key](https://dev.epicgames.com/documentation/unreal-engine/BlueprintAPI/WaterBody/SetRiverWidthatSplineInputKey)
- [Epic Tutorial: Baked River Simulations – Overview and Quick Start](https://dev.epicgames.com/community/learning/tutorials/Y5J6/unreal-engine-baked-river-simulations-overview-and-quick-start), [Forum-Thread dazu](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-overview-and-quick-start/2512102)
- [Epic Forum: Tutorial Baked River Simulations – Parameter Reference](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112)
- [Epic Forum: Community Tutorial 5.6 – Water Body River als Niagara-2D-Simulation](https://forums.unrealengine.com/t/community-tutorial-new-in-unreal-engine-5-6-turn-your-water-body-river-into-a-game-ready-niagara-2d-fluid-simulation/2583651)
- [Epic Tutorial: Next-Level Water FX in UE 5.6](https://dev.epicgames.com/community/learning/tutorials/d6Jy/unreal-engine-next-level-water-fx-in-ue-5-6)
- [Epic Forum: 5.6 are shallow water river destructive? (Reset, Bake)](https://forums.unrealengine.com/t/5-6-are-shallow-water-river-destructive/2659509)
- [Epic Forum: Unreal 5.6 water simulation (Kollision, World Partition)](https://forums.unrealengine.com/t/unreal-5-6-water-simulation/2626503)
- [Epic Forum: ShallowWaterRiver Collision](https://forums.unrealengine.com/t/shallowwaterriver-collision/2734514)
- [Epic Forum: ShallowWaterRiver disappear after compiling](https://forums.unrealengine.com/t/shallowwaterriver-disappear-after-compiling/2682125)
- [Epic Forum: Shallow Water Body (Advanced Water Plugin) Fails To Render](https://forums.unrealengine.com/t/shallow-water-body-advanced-water-plugin-fails-to-render/2634176)
- [Leitfaden (japanisch): UE5.6 Shallow Water River](https://yossi40-100.com/ue56shallow_water_river/) – nur Auszug
- [80.lv: Working with Niagara Fluids to Create Water Simulations](https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations)

Zum ursprünglichen Vorschlag:

- [Epic Forum: Community Tutorial „New in Unreal Engine 5.6 – Shallow Water River“](https://forums.unrealengine.com/t/community-tutorial-new-in-unreal-engine-5-6-part-2-how-to-float-objects-on-your-shallow-water-river-simulation/2583650)
- [Epic Forum: ShallowWaterRiver startet nicht in 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772)
- [Epic Doku: Water Body Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-body-actors-in-unreal-engine)
- [Epic Doku: Fluid Simulation Overview (Niagara Fluids)](https://dev.epicgames.com/documentation/unreal-engine/fluid-simulation-in-unreal-engine---overview)
- [Epic Forum: Tutorial Shallow Water Simulation with Niagara Fluids](https://forums.unrealengine.com/t/tutorial-shallow-water-simulation-with-niagara-fluids/1786912)
- [80.lv: Fluid Flux](https://80.lv/articles/fluid-flux-a-cool-water-simulation-system-for-unreal-engine/)
