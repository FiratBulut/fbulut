# Antwort zu Auftrag 13h – Bildbefund erster Sehens-Pilot (Bergwald B5: Säulenhain + Karsee)

Stand 12.10.2026 – **Vorfassung Bergwald** (Karsee und Säulenhain fertig für den zweiten Pilot). Die Abschnitte „Alle Biome“
und „Ergebnis je Biom“ folgen mit der Endfassung.

## Kurzfazit

- **Karsee:** Keine glatten Erdwände mehr.
  - Neue Flächen steiler als 45° tragen jetzt Fels: an der Rückwand eine Klippenreihe, am Auslauf eine Schwelle aus Felsbuckeln.
  - Wo kein Fels steht, wird flacher gestempelt: Schutthalde ≤ 35° mit Geröll-Lage und Blöcken.
  - Die Karwand ist gegliedert: Felsbänder, Schuttkegel an den Rinnen, oben Moos und Schneereste.
  - Die Seefarbe ist jetzt `tiefblau`. Die Insel ist eine Geländekuppe 0,6 m über dem Spiegel, die Kiefer steht darauf.
  - Seelage, Spiegel und Stufen sind wie in 13f.
- **Säulenhain:** Der Kern besteht nur noch aus Riesentannen, 13 × `Fir_07_Forest` ×2,6–2,9.
  - Mit 57–64 m sind sie im Median 59,5 m hoch, der Bestand ringsum 27 m (90-%-Wert). Das ist das 2,2-Fache.
  - Bestand und Unterholz im Kern werden entfernt (Freiraum).
  - Nach ONO liegt eine Lichtung in der Achse von `_fern`, Pfad und `_anmarsch`.
  - Dazu kommen drei Lichtstreifen mit Nebel und liegendes Altholz.
  - `_fern` steht jetzt an einem Wegpunkt, von dem aus die Kronen **vor dem Himmel** stehen. Vorher stand dahinter der Kamm.
- **Neue Lib-Regeln für alle Planer:**
  - Steilflächen-Regel im Prüfer.
  - Böschung, Halde und automatische Verkleidung im Stempel.
  - Kamera-Prüfung mit freiem Strahl, Kronenabstand und Leuchtfeuer-Silhouette.
  - Blöcke im See nie knapp unter dem Spiegel (Nachtrag 01:00).
  - Alles neu und additiv: `sehens_lib/steilwand.py`, `kamera_frei.py`, `see_bloecke.py`, `Stempel.boeschung`.
- **Bergwald auf 2 m:** Prüfer **0 FEHLER**, zwei Läufe byteidentisch. Die alte Fassung hatte unter den neuen Regeln 15 FEHLER.

## Karsee (bergwald_06)

### Befund 1 – senkrechte, glatte Erdwände

**Ursache:**
- Das Seebecken (`see_becken`, Sohle „nur absenken“) schneidet hangseitig bis 9 m senkrecht in den 25°-Trog.
- Der Uferring hebt talseitig einen Damm bis +7,5 m, dessen Außenseite fast senkrecht ist. Das ist die „Wand mit waagrechter
  Stufe“ in `…karsee_anmarsch`.
- Unter der neuen Prüfer-Regel waren das 6 FEHLER (85, 49, 42, 39, 34 und 29 m²).

**Was geändert ist:**
- **Flacher stempeln** (`gelaende.max_neigung_grad: 35`):
  - Neue Steilheit wird zuerst am Fuß aufgeschüttet (Schuttkegel, ≤ 4 m) und dann an der Oberkante abgetragen (≤ 3 m).
  - Die Wirkung läuft linear aus, damit der Ausgleich nicht den ganzen Hang hinaufläuft.
  - Seefläche, Uferring (nie unter Spiegel + 0,3 m), Auslasslippe und Bachkern bleiben fest.
  - Ergebnis: 496 m² Halde aufgeschüttet, 2 212 m² abgetragen.
  - Auf der Halde liegen die Lage `Geroell` 205 und Blöcke aus `kegelschutt` (0,1 je m²).
- **Auslaufseite:**
  - Gruppe `schwelle_buckel` (`verteilung.typ: steilwand` um den Auslass).
  - 7 Rundhöcker aus `SM_NordicBoulder_01`, `SM_Big_rock_01/02` und `SM_mountain_rock_big_02_1/_6`, 4–7 m groß.
  - Sie verkleiden die Außenseite des Uferrings.
  - Vom See aus bleibt das Ufer flach: Lippe auf dem Spiegel, Schwelle aus Felsbuckeln.
- **Rückwand:**
  - Gruppe `karwand_fels` mit 18 Klippennetzen: `rcygn_tier_0` (Sharp Cliff), `SM_HugeNordicCoastalCliff_01/02` und
    `SM_big_rock_wall_01`, 6–9 m hoch.
  - Die Vorderkante steht an der Zelle (`front_an_linie`), die Netze überlappen sich.
  - Hohe Wände werden gestapelt, das obere Netz ist dann `z_frei`.
  - Vorbild sind die Uferklippen aus A15 (`gefaelle_regeln.json` → `ufer_klippen`, `biome.bergwald.netze.wand`).
  - Schauseite: `front_achse +y` ist angenommen (E35). Bitte im Editorbild prüfen.
- **Gliederung der Karwand:**
  - Zwei Felsbänder quer zur Wand (`felsbaender`, `felsbaender_west`, 46 Blöcke) mit Latschen.
  - Schuttkegel am Fuß beider Zulaufrinnen (`rinnenkegel_sued/_west`).
  - Geröll-Bänder entlang der Rinnen.
  - Moos-Lage oben am Hang.
  - Schnee-Lage fleckig auf den schattigen Nordhängen über dem Kar (zwei Flecken, 160–175).
  - Moos auf den Nordseiten von Klippen und Bändern.
  - Die ebene, waagrechte Stufe ist weg: Der Dammfuß ist jetzt Halde, die Dammkrone liegt hinter Felsbuckeln.
- **Ergebnis (Prüfer, 1 m):**
  - 513 m² neu > 45°, davon 422 m² mit Fels verkleidet.
  - Der Rest liegt in Gebieten ≤ 20 m².
  - **0 FEHLER.**

### Befund 2 – Seefarbe

- `schwarz_spiegel` → **`tiefblau`** (`farbe_begruendung` im Rezept).
- Karseen im Kristallin sind klar und tiefblau, am Ufer heller über dem Kies: Morskie Oko und Czarny Staw pod Rysami in der
  Tatra, der Seebensee in den Alpen.
- `smaragd` passt eher zu flachen Kalkseen mit Algen, nicht zu 4 m Tiefe im Granit.
- **Mulde geöffnet:** Böschung und Halde nehmen den Seiten des Beckens die senkrechten Kanten.
  - Uferkies mit Lage `Kies` 210 bleibt.
  - Der Nebel über dem See bleibt dezent (0,06).
- `_nah` steht nicht mehr im See (13i K9). Sie steht jetzt am Ostufer, 15 m vor der Insel, mit Blick über das Wasser auf die
  Rückwand. Damit spiegeln sich Hang und Himmel im Bild.

### Befund 3 – gestreifte Formen um die Insel (mit Nachtrag 01:00)

- **Ursache:**
  - `insel` und `inselblock` standen mit `z_bezug: see:karsee` im Wasser.
  - Sie wurden in Z gestreckt (×1,5 bzw. ×2,5), damit sie den Seegrund erreichen.
  - Ihre Oberkanten bzw. Flanken lagen knapp unter dem Spiegel. Das passt zu eurer Diagnose: Pivot 252,1 / 252,3 m unter
    256,17 m.
- **Insel jetzt als Geländekuppe:**
  - Neues Feld `becken.insel` (`versatz_m`, `r_m` 4,5, `ueber_m` 0,6) legt nach dem Becken eine Kuppe ins Becken.
  - Die Krone liegt **0,6 m über dem Spiegel**.
  - Beide Blöcke stehen ungestreckt auf der Kuppe.
  - Die Kiefer `SM_dwarf_pine_big_01` steht mit dem Stammfuß auf der Inselkrone, nicht auf dem Block. Nichts liegt unter dem
    Spiegel.
- **Allgemeine Regel aus dem Nachtrag (`see_bloecke.py`, alle Planer):**
  - Fels und Steine ≥ 0,8 m in einem geplanten See liegen mit der Oberkante entweder ≥ Spiegel + 0,3 m oder ≤ Spiegel − 1,5 m.
  - Der Planer hebt solche Stücke (höchstens 0,8 m), senkt sie im tiefen Wasser ab oder entfernt sie.
  - Der Prüfer meldet FEHLER.
  - Im Karsee: 19 gehoben, 6 gesenkt, 17 entfernt. Das sind vor allem Steine aus Schuttkegel und Uferkies.

## Säulenhain (bergwald_03)

### Befund 4 – `_nah` in einer Krone

- **Ursache:**
  - `_nah` stand 10 m südlich der Mitte, 6 m neben einer Riesentanne.
  - Deren Kronenradius beträgt bei ×2,4 etwa 11–13 m.
  - Außerdem war `Fir_04_Standalone` als Freistand-Tanne bis zum Boden beastet.
- **Jetzt:**
  - Neue Lib-Prüfung: Abstand ≥ Kronenradius + 2 m, freier Strahl.
  - Regel `kameras.nah`: Ziel ist der Stammfuß der vordersten Riesentanne zur Lichtung (Boden + 2 m).
  - Die Kamera steht 13 m davor in der Lichtung.
  - Die Riesen sind nur noch `Fir_07_Forest`. Als Waldform hat sie eine hohe Kronenbasis und wirkt eher als Säulenstamm.
- Alle Kameras sind geprüft: `_held` 45 m (versetzt, stand an einer Maßstabstanne), `_anmarsch` 95 m in der Lichtung auf dem
  Zugang.

### Befund 5 – Leuchtfeuer aus `_fern`

**Messung mit den neuen Regeln:**
- Aus der alten `_fern`-Position sind 42 m von 51 m sichtbar (83 %).
- Die Kronen stehen aber **vor dem Kamm** (684 m) und nicht vor dem Himmel. Das erklärt, warum im Bild kein Unterschied
  zu sehen ist: dunkelgrün vor dunkelgrünem Hang.

**Was geändert ist:**
- **Höhe:**
  - 13 × `Fir_07_Forest` ×2,6–2,9, Median 59,5 m.
  - Bestand im Ring 50–110 m: 27 m (90-%-Wert).
  - Faktor 2,2, die Regel verlangt ≥ 1,5.
- **Lichtung und Saum:**
  - Freiraum `rechteck` 70 × 42 m nach ONO (60°). Das ist die Achse von `_fern`, Pfad und `_anmarsch`.
  - Lagen Gras und Moos, dazu Heide und Beeren (`lichtung_gras`).
  - Ein Saum aus Jungtannen (`saum_jungwuchs`) und Maßstabstannen bei 37–46 m.
- **Freie Achse:** Die Leuchtfeuer-Regel prüft die Mindesthöhe über Gelände und Bestand. Bestand in Freiräumen zählt dabei
  nicht.
- **`_fern` neu gesucht** (`kameras.fern.suche: wegpunkte`):
  - Wegpunkt (−2522/−412), 570 m vom Hain.
  - Die Kronen stehen **vor dem Himmel**, 29 m der Silhouette sind sichtbar (49 %).
- **Hinweis für den Editor:** Die Tannen sind Nicht-Nanite-Netze. Bitte auf 570 m prüfen, ob LOD oder Billboard die Kronen
  zu früh vereinfacht.

### Befund 6 – Hallenwald

**Kern:**
- Freiraum `kreis` r 34 m: Bestandskiefern und Unterholz entfernen.
- Nur Riesentannen.
- Farn nur noch in 8–11 kleinen Inseln.
- Nadelstreu 235.
- Heidelbeere nur am Rand.

**Licht:**
- Drei Spotlichter (Lichtstreifen in Sonnenrichtung, schwach, ohne Schatten).
- Lokaler Nebel mit Dichte 0,05 (vorher 0,03).

**Altholz:**
- Ammenstamm mit Jungtannen.
- 2 × `SM_LargeFallenTree_02`.
- 2 × liegender `SM_MossyTree_01` (`altholz`).
- 90 Stück Moderholz.
- Pilze am Holz.

**Kontrast:**
- Innen dunkle Säulenhalle aus Tannen, außen der lichte, orangestämmige Kiefernbestand.
- Dazwischen Saum und Lichtung.

**Vorbilder:**
- Białowieża: Urwald mit Altholz am Boden.
- Cathedral Grove: Säulenhalle.
- Hoh Rainforest: Ammenstämme, Moos.
- Sequoia/Giant Forest: Lichtung vor den Riesen.

## Allgemein (Lib, alle Planer) – Stand der Vorfassung

| Regel | Wo | Was |
|---|---|---|
| Steilflächen | `steilwand.pruefe_orte_steil` (im Prüfer) | > 20 m² zusammenhängend > 45°, vom Stempel neu geschaffen (\|Δ\| > 0,25 m, um > 5° steiler), ohne Fels-Akteur (XY-Hülle der gedrehten Bounds, Höhe ± 1 m) → **FEHLER**. Ausgenommen: Seegrund unter dem Spiegel, Meeresboden, benetztes Bachbett (halbe Breite + 1 m). |
| Flacher stempeln | `Stempel.boeschung`, `steilwand.boeschung_anwenden` (nach `fertig()`) | Standard 38°, je Ort `max_neigung_grad`. Auffüllen am Fuß, dann Abtrag an der Kante, linear auslaufend. Keine neuen geschlossenen Senken. Halde mit Lage und Blöcken aus `gefaelle_regeln.json` → `biome.<biom>`. |
| Verkleiden | Gruppe `verteilung.typ: steilwand`, dazu `steilwand.auto_verkleiden` | Gierige Überdeckung von unten nach oben mit den Wandnetzen des Bioms (A15). Front talwärts, `front_an_linie`, überlappend, hohe Wände gestapelt. `gelaende.verkleiden: false` schaltet die Automatik ab. |
| Bachprofil | `steilwand.bach_einschnitt_begrenzen` | Außerhalb von Netzrand + Uferring höchstens Tiefe + 0,5 m eintiefen (vgl. 13i K1; Spiegel und Stufen unverändert). Wird ein No-op, sobald K1 im Profil selbst gelöst ist. |
| Kameras | `kamera_frei.py` (Planer und Prüfer) | Nicht im geplanten Wasser, nicht in einem Netz. Abstand zu neuen Bäumen ≥ Kronenradius + 2 m. Freier Strahl gegen neue Netze (Bäume als Krone + Stamm, sonst gedrehte Box), Bestandskronen (4 m, ohne Freiräume) und Gelände. Der Planer versetzt blockierte Kameras (Ring um das Ziel) oder räumt eigene Pflanzen am Standplatz frei; Regel `kameras` je Ort. |
| Leuchtfeuer | `kamera_frei.pruefe_leuchtfeuer` | `_fern` muss die Held-Silhouette zeigen (≥ 30 % und ≥ 10 m oder ganz). Ein Baumhain muss ≥ 1,5 × Bestand hoch sein. Info: Silhouette vor dem Himmel ja/nein. |
| Blöcke im See | `see_bloecke.py` | Oberkante ≥ Spiegel + 0,3 m oder ≤ Spiegel − 1,5 m (Nachtrag 01:00). |

## Commit für den zweiten Pilot

Vorfassung Bergwald: siehe Commit-Nachricht „Auftrag 13h: Vorfassung Bergwald …“. Den Hash nennt die Endfassung.
