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
  - `dz_cm` = 0 überall. Das Wasser steht quer auf der Mittellinie.
  - `deckung` = 1.
  - `schaum` nur am Lippensaum (≤ 0,5 m) und in Zunge und Aufprallkreis (≤ 30 % des Beckens), wie die 15f-Regel.
  - `tiefe_cm` = Spiegel − Bett je Stützpunkt.
- Die Netze sagen `"lippen": "gerade (Sehens-Stufen wie 13f, keine Unregelmaessigkeit aus 15f)"`.
- **Hinweis zu `quer_ergaenzen`:**
  - Der letzte Bogenpunkt und der Wandpunkt einer Stufe haben in `bauen_wasser_A` dasselbe s. Die Interpolation in
    `quer_ergaenzen` nimmt dort die Höhe des Nachbarpunkts; `dz_cm` lag dadurch an diesen Punkten bei bis zu 6 m.
  - Für gerade Lippen setze ich `dz_cm` = 0. Im A15-Werkzeug selbst (`skripte/gefaelle/`, nicht geändert) besteht das
    wohl auch: Bitte bei Gelegenheit prüfen, ob die C2-Netze dort springende Querprofile haben.
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

ERGEBNIS_13J

## Beobachtung

Bei parallel laufenden Planern (3 Prozesse) waren elfenwald und lava einmal nicht byteidentisch: Die Kameraversätze aus
`kamera_frei` unterschieden sich um Zentimeter. Nacheinander gerechnet waren sie identisch. Ich vermute
Gleitkomma-Reihenfolgen in mehrfädigen NumPy-Operationen unter Last. Nicht behoben, nur zur Kenntnis.
