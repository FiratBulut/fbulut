# Antwort zu Auftrag 13j – `quer` für die Treppenbäche, Netzmaße, Akteur-Budget

Stand 12.10.2026. Grundlage ist der 13h-Endstand (dadcc24/146e49c) mit den neuen Netzmaßen (46bd196). Commits:

| Punkt | Commit |
|---|---|
| `quer` für die Kaskadennetze (Bergwald zuerst, gilt für alle 15 Biome) | `291ae73` |
| Akteur-Budget | `41952fe` |
| Abschlusslauf, Testbilder, diese Antwort | siehe Commit dieser Datei |

## Kurzfazit

- **Treppenbäche mit `quer`:**
  - Jedes Kaskadennetz in `orte.json` → `wasser[]` → `wasser_koerper` hat jetzt das 15f-Format: `quer` mit 11
    Stützpunkten `[dz_cm, deckung, schaum, tiefe_cm]`, `quer_punkte`, `quer_felder`, `quer_lage`,
    `mittellinie_s_m`, `material_parameter` (Schaum_Menge 0,15, Zungen_Schaum 0,25), `farbe_hinweis`, `schaum_regel`;
    `knick` kennt `uebergang`.
  - Die Lippen sind **gerade** (Ferat: Stufen wie 13f). Die Lippen-Unregelmäßigkeit aus 15f ist nicht angewendet.
  - Der Stufenvergleich gegen c945f93 ist unverändert (K5-Klassen aus 13i).
- **Netzmaße:**
  - `inventar.netz()` liest Pivot und Unterkante schon aus `vorlagen/daten/netze_masse.json` (Box im Netz-Raum).
    Mit den 1 017 Einträgen sind 773 der 799 Netze aus den Rezepten gemessen.
  - Die übrigen 26 sind die Houdini-Netze K7/K9/K13 (werden nicht gesetzt), einige Zwergkiefern, `SM_Poplar_tree_07_Optimised`
    und `SM_MassiveSandstoneCliff_01/03`. Für sie gilt weiter die Annahme „unten Mitte“; `pivot` im Plan sagt
    es je Netz.
  - K2 (Pivot in der Netzmitte → Unterkante auf den Boden) und A3 rechnen damit. Klippen, Basalt und Mountain-Wände
    stehen jetzt mit gemessener Unterkante.
  - Alle 15 Planer sind neu gelaufen.
- **Akteur-Budget:**
  - Netze, die in einem Ort ≥ 12-mal als Akteur stehen, werden Instanzen der Ebene `sw_<biom>` mit Kollision. Das
    gilt auch für die 13h-Wandverkleidung.
  - Lage, Größe, Drehung und Gestaltung bleiben gleich; einzelne Heldenstücke bleiben Akteure.
  - Prüfer-HINWEIS bei mehr als 50 Akteuren je Ort.
  - Die 13h-Steilflächenregel zählt Fels-Instanzen mit Kollision jetzt wie Fels-Akteure; sonst würde die
    umgewandelte Verkleidung als „ungedeckt“ gelten.

## 1. `quer` für die Treppenbäche

- `sehens_lib/bach.wasser_koerper` ruft `gefaelle_plan.bauen_wasser_A` jetzt mit `lf` (LippenFeld) und `rw`
  (Regelwerk) auf. Damit läuft `quer_ergaenzen` (15f): Verdichtung um jede Lippe alle 0,25 m (`uebergang`), Deckung,
  Schaum, `tiefe_cm` aus dem gestempelten Bett.
- **Gerade Lippen:** Jede Sehens-Stufe bekommt die Lippenform Winkel 0, kein Pfeil, eine Kerbe über die ganze Breite.
  Daraus folgt:
  - `dz_cm` nach A15-Konvention (korrigiert im Nachtrag, siehe unten): relativ zu `z_cm` des eigenen Punkts; quer zur
    Lippe ist die absolute Wasserhöhe gleich, an Punkten mit gleichem s ebenfalls.
  - `deckung` = 1.
  - `schaum` nur am Lippensaum (≤ 0,5 m) und in Zunge und Aufprallkreis (≤ 30 % des Beckens), wie die 15f-Regel.
  - `tiefe_cm` = Spiegel − Bett je Stützpunkt.
- Die Netze sagen `"lippen": "gerade (Sehens-Stufen wie 13f, keine Unregelmaessigkeit aus 15f)"`.
- **`dz_cm` an Bogen und Wand (korrigiert im Nachtrag):**
  - Der letzte Bogenpunkt und der Wandpunkt einer Stufe haben in `bauen_wasser_A` dasselbe s. `dz_cm` ist dort groß,
    weil es relativ zu `z_cm` des eigenen Punkts gilt. Das ist kein Fehler (A15, 15f-Nachtrag `099f902`).
  - Mein früherer Workaround (`dz_cm` = 0) ist entfernt. `dz_cm` kommt unverändert aus `quer_ergaenzen`.
- **Bergwald:** 4 Kaskadennetze (bergwald_05 `klammbach`, bergwald_06 `abfluss`, `zulauf_sued`, `zulauf_west`). Alle
  haben `quer`; der Prüfer meldet 0 FEHLER; die Stufen sind wie 13f/13i.

## 2. Netzmaße

- Es war keine Code-Änderung nötig. `inventar.lade()` liest `netze_masse.json` (min/max in cm je Netzpfad).
  `inventar.netz()` gibt `bounds_cm` und `pivot: "bounds"` zurück; nur ohne Eintrag gilt `"angenommen_unten_mitte"`.
- Mit den neuen Daten stehen alle gesetzten Sehens-Netze auf `bounds`, außer den oben genannten.
- Drei Einträge in `netze_masse.json` gehören zu Netzen, die nicht im Inventar stehen (`netze.csv`): die
  Namaqualand-NN-Klippen. Sie werden derzeit nicht gesetzt.

## 3. Akteur-Budget

- **`rezept._akteure_buendeln`:** Läuft nach allen Gruppen, nach der 13h-Verkleidung und den Halden-Blöcken, und vor
  Pfad und Lagen.
  - Je Ort und Netz: ab 12 Akteuren werden alle Stücke dieses Netzes Instanzen: `akteur` = false, `kollision` = true,
    `extra.aus_akteur` = true.
  - Sie liegen dann in der f32-Datei `<Netz>_kol` der Ebene `sw_<biom>`.
- **Beispiel bergwald_03 Säulenhain:** 26 → 13 Akteure. Die 13 Riesentannen (`Fir_07_Forest`) sind ein
  wiederholtes Netz und laufen jetzt als Instanzen mit Kollision.
  - Sollen solche Stücke Heldenstücke bleiben, setzt man an der Gruppe `"akteur_fest": true`; dann bleiben sie
    Akteure. In den Rezepten ist das noch nirgends gesetzt.
  - Rückfrage: Sollen die Riesentannen im Säulenhain Akteure bleiben?
- **Prüfer** (`pruefe_ebene`): HINWEIS „n Akteure > Richtwert 50 je Ort“.
- **`steilwand.pruefe_orte_steil`:** Fels-Instanzen mit Kollision (`ist_fels`) aus den Ebenen-Dateien zählen als
  Verkleidung, wie bisher die Fels-Akteure. Sonst nichts an der 13h-Gestaltung geändert.

## Prüfergebnis

| Lauf | Ergebnis |
|---|---|
| 2 m, alle 15 (mit neuen Netzmaßen, `quer`, Akteur-Budget) | Planer 0 FEHLER; Prüfer 0 FEHLER |
| synthetisch 1 m | 0 FEHLER bis auf gletscher_03/06, lava_08 und tundra_08 (s. u.) |
| Selbsttest | 0 FEHLER (68 Prüfungen) |
| Stufenvergleich gegen c945f93 | wie 13i: 26 nur Fuß, 7 gleich, 5 Schluss-Stufe; 4 gletscher-Bäche „anders“ durch die 13h-Umformung des Geländes |

**Kamera-Prüfung nach dem Akteur-Budget:**
- Der Prüfer (`kamera_frei.hindernisse_aus_ebene`) gab Instanzen bisher die Ebene der Datei („begleiter/held“ zählte
  nicht als `held`). Deshalb galten umgewandelte Wandmodule nicht mehr als eigenes Heldenstück und sperrten die
  `_held`-Kamera (frost_02).
- Jetzt gilt die Ebene aus der Gruppe der Datei (`held` vor `begleiter` …), wie im Planer.

**Synthetische 1-m-Welt, offen:**
- **gletscher_03:**
  - `seeabfluss` „Gelände über dem Spiegel“ (bis 4,9 m) und eine Steilfläche.
  - Ursache: Nach der 13h-Umformung (Karbank, organische Ränder) laufen `seeabfluss` und `firnrinnsal` am Moränensee
    1–2 m nebeneinander. Der Uferring des zweiten schüttet das Bett des ersten zu.
  - Schützt man das Bett, fehlt dem zweiten das Ufer.
  - Lösung im Rezept (Linien trennen). Das ändert aber die Stufen; Rückfrage, ob das erlaubt ist.
- **gletscher_06:** zwei Steilflächen ohne Fels-Akteur (13h-Regel, 21 und 45 m²).
- **lava_08:** Kamera `_nah`, Sicht nach 3 m durch Basaltsäulen (13h-Kameraregel). Mit den gemessenen Netzmaßen ist der
  Säulenstock größer als angenommen.
- **tundra_08:** ein Moospolster 0,25 m unter dem Tümpelspiegel (13h-Seeblock-Regel, neue Netzmaße).
- Diese vier betreffen die 13h-Regeln bzw. das 13h-Gelände; auf 2 m sind sie ohne Meldung.

## Beobachtung

~~Bei parallel laufenden Planern waren elfenwald und lava einmal nicht byteidentisch (Kameraversätze aus `kamera_frei`).~~
Korrigiert im Nachtrag: Der Unterschied lag nicht in `kamera_frei`, sondern in einer A15-Änderung zwischen den beiden
Läufen (neues Feld `pruefung.ufer_an_lippe`); siehe Nachtrag, Abschnitt Determinismus.

## Nachtrag (Koordinator, 12.10.)

Commits: `47a97a9`, `4a95150`, `0e22f82`, `725a69e`; Einzelheiten in der 13i-Antwort, Abschnitt Nachtrag.

- **`dz_cm` nach A15-Konvention:** Workaround (`dz_cm` = 0) entfernt; `dz_cm` kommt unverändert aus `quer_ergaenzen`.
  Der Prüfer `sehens_pruefen.pruefe_wasser_koerper` importiert die Regel aus `099f902` (`gefaelle_pruefen.pruefe_wasser`,
  zweiter Aufruf mit Welt, gefiltert auf Querprofil/Wasserhöhe/Deckung): absolute Wasserhöhe bei gleichem s gleich,
  Sprünge längs und quer ≤ größte Lippenhöhe + 5 cm. Gegenprobe: ein verfälschtes `dz_cm` ergibt FEHLER.
- **Fuß hinter dem Bogen:** Bei einer Schluss-Stufe, deren 13f-Fuß näher als `bogen_x_m` + 5 cm an der Lippe liegt
  (elfenwald_04 `stufe_1`), setzt das Netz seinen Fuß auf Lippe + `bogen_x_m` + 5 cm. Die Stufen bleiben wie 13f.
- **Akteur-Budget:** Riesentannen (bergwald, Gruppe `riesen`) bleiben mit `akteur_fest` Akteure. Neue Option
  `gelaende.verkleiden.budget_nach_buendeln` (nur gletscher_06): Die 13h-Verkleidung rechnet das Budget ohne die
  Netze, die danach gebündelt werden.
- **Determinismus:** Der frühere Unterschied kam aus einer A15-Änderung zwischen zwei Läufen, nicht aus `kamera_frei`
  (siehe Beobachtung). Zusätzlich ist der Hindernis-Cache in `kamera_frei` jetzt lagegenau.

**Prüfergebnis (Endstand):**

ERGEBNIS_NACHTRAG

