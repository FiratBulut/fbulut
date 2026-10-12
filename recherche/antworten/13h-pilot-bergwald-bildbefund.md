# Antwort zu Auftrag 13h – Bildbefund erster Sehens-Pilot (Bergwald B5: Säulenhain + Karsee)

Stand 12.10.2026 – **Endfassung** (alle 15 Biome). Die Vorfassung Bergwald (`73e5cb3`) war für den zweiten Pilot gedacht.
Die Zahlen unten stammen aus dem Endstand. Er enthält auch die 13g/13i-Änderungen am Bach (Querprofil, Ufer).
Deshalb weichen einige Karsee-Zahlen von der Vorfassung ab.

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
- **Alle 15 Biome auf 2 m:** Prüfer **0 FEHLER**, zwei Läufe byteidentisch, Selbsttest Schritt 12 mit 0 FEHLER.
  Die Bergwald-Fassung vor 13h hatte unter den neuen Regeln 15 FEHLER.
- **Testbilder:** alle Biome neu erzeugt, liegen unter `recherche/antworten/sehens/<biom>/`.
- **13i K9:** Gletscher, Canyon, Küste und Lava sind organischer und kleiner geworden. `_nah` am Karsee steht nicht mehr
  im See (Abschnitt „13i K9“).

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
  - Ergebnis im Endstand: 36 m² Halde aufgeschüttet, 56 m² abgetragen. In der Vorfassung waren es 496 und 2 212 m².
    Die Rückwand ist jetzt fast ganz mit Fels verkleidet. Der Bach-Einschnitt ist begrenzt (siehe „Allgemein“).
    Deshalb bleibt weniger offene Steilheit, die abgeflacht werden muss.
  - Auf der Halde liegen die Lage `Geroell` 205 und Blöcke aus `kegelschutt` (0,1 je m²).
- **Auslaufseite:**
  - Gruppe `schwelle_buckel` (`verteilung.typ: steilwand` um den Auslass).
  - 14 Rundhöcker aus `SM_NordicBoulder_01`, `SM_Big_rock_01/02` und `SM_mountain_rock_big_02_1/_6`, 4–7 m groß.
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
- Dazu kommen 5 Netze aus der automatischen Verkleidung (`wandverkleidung`).
- **Ergebnis (Prüfer, 1 m):**
  - 241 m² neu > 45°, davon 233 m² mit Fels verkleidet.
  - Die restlichen 8 m² liegen in Gebieten ≤ 20 m².
  - **0 FEHLER.**

### Befund 2 – Seefarbe

- `schwarz_spiegel` → **`tiefblau`** (`farbe_begruendung` im Rezept).
- Karseen im Kristallin sind klar und tiefblau, am Ufer heller über dem Kies.
  - Tatra: [Morskie Oko](https://de.wikipedia.org/wiki/Meerauge_(Tatra)) und
    [Czarny Staw pod Rysami](https://de.wikipedia.org/wiki/Czarny_Staw_pod_Rysami).
  - Alpen: der [Seebensee](https://de.wikipedia.org/wiki/Seebensee).
  - Dort steigt die Karwand als Fels und Schuttkegel auf. Die Halden liegen im
    [Schüttwinkel](https://de.wikipedia.org/wiki/Sch%C3%BCttwinkel) von 30–35°, glatte Erdwände gibt es nicht
    (vgl. [Kar](https://de.wikipedia.org/wiki/Kar_(Geomorphologie))).
- `smaragd` passt eher zu flachen Kalkseen mit Algen, nicht zu 4 m Tiefe im Granit.
- **Mulde geöffnet:** Böschung und Halde nehmen den Seiten des Beckens die senkrechten Kanten.
  - Uferkies mit Lage `Kies` 210 bleibt.
  - Der Nebel über dem See bleibt dezent (0,06).
- `_nah` steht nicht mehr im See (13i K9). Sie steht jetzt am Südufer bei (−3204/56), 15 m vor der Insel.
  - Der Blick geht über das Wasser auf die Rückwand. Damit spiegeln sich Hang und Himmel im Bild.
  - `_anmarsch` (−3167/47) und `_held` (−3212/43) sind versetzt. Ihr Strahl ging durch Blöcke der Schwelle.

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
  - Im Karsee: 25 gehoben, 5 gesenkt, 16 entfernt. Das sind vor allem Steine aus Schuttkegel und Uferkies.
  - Ausnahmen:
    - Gruppen mit `"teilweise_ueberflutet": true`. Sie stehen in `orte.json` je Ort, der Prüfer lässt sie aus.
    - Zugefrorene Seen (`"eis"`), dort liegt alles auf dem Eis.
  - Ein Verstoß ist ein **FEHLER**.
  - Weitere Treffer: gletscher_03 (27 gehoben, 5 entfernt) und lava_05 (12 / 4 / 6).

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
- [Białowieża](https://de.wikipedia.org/wiki/Bia%C5%82owie%C5%BCa-Urwald): Urwald mit Altholz am Boden.
- [Cathedral Grove](https://en.wikipedia.org/wiki/Cathedral_Grove): Säulenhalle.
- [Hoh Rainforest](https://en.wikipedia.org/wiki/Hoh_Rainforest): Ammenstämme, Moos.
- [Giant Forest, Sequoia](https://en.wikipedia.org/wiki/Giant_Forest): Lichtung vor den Riesen. Die Riesen wirken dort,
  weil man sie aus einer offenen Wiese sieht (Round Meadow).

## Allgemein (Lib, alle Planer)

| Regel | Wo | Was |
|---|---|---|
| Steilflächen | `steilwand.pruefe_orte_steil` (im Prüfer) | Mehr als 20 m² zusammenhängend steiler als 45°, vom Stempel neu geschaffen (\|Δ\| > 0,25 m, um > 5° steiler) und nicht von einem Fels-Akteur gedeckt (XY-Hülle der gedrehten Bounds, Höhe ± 1 m) → **FEHLER**. Ausgenommen sind Seegrund unter dem Spiegel, Meeresboden und das benetzte Bachbett (halbe Breite + 1 m). |
| Flacher stempeln | `Stempel.boeschung`, `steilwand.boeschung_anwenden` (nach `fertig()`) | Standard 38°, je Ort über `max_neigung_grad`. Zuerst wird am Fuß aufgefüllt, dann an der Kante abgetragen, linear auslaufend. Das gilt nur dort, wo das natürliche Gelände höchstens 3° steiler ist; natürliche Felshänge bleiben. Es entstehen keine neuen geschlossenen Senken, Land kommt nie unter +0,3 m. Die Halde bekommt Lage und Blöcke aus `gefaelle_regeln.json` → `biome.<biom>`. |
| Verkleiden | Gruppe `verteilung.typ: steilwand`, dazu `steilwand.auto_verkleiden` | Gierige Überdeckung im 1-m-Raster von unten nach oben mit den Wandnetzen des Bioms (A15). Front talwärts, `front_an_linie`, überlappend. Hohe Wände werden gestapelt (`z:`-Bezug). Je Zelle gibt es drei Versuche mit ±25° Gier. Budget: höchstens 78 Akteure je Ort. `gelaende.verkleiden: false` schaltet die Automatik ab; `verkleiden.netze/groesse_m` setzt große Klippen. |
| Bachprofil | `steilwand.bach_einschnitt_begrenzen` | Außerhalb von Netzrand + Uferring wird höchstens Tiefe + 0,5 m eingetieft (vgl. 13i K1). Spiegel und Stufen bleiben unverändert, `bach.py` ist nicht angefasst. Wird zum No-op, sobald K1 im Profil selbst gelöst ist. |
| Kameras | `kamera_frei.py` (Planer und Prüfer) | Nicht im geplanten Wasser, nicht in einem Netz. Abstand zu neuen Bäumen ≥ Kronenradius + 2 m. Freier Strahl gegen neue Netze: Bäume als Krone + Stamm, liegende Bäume und Laub mit 80 % Kern, sonst gedrehte Box. Dazu Bestandskronen (4 m, ohne Freiräume) und das Gelände nach dem Stempel. Der Planer versetzt blockierte Kameras (Ring um das Ziel, zwei Durchgänge mit Rand 0,6 / 0,25 m) oder räumt eigene Pflanzen am Standplatz frei. Je Ort gibt es die Regel `kameras` (`pos`, `ziel_gruppe`, `abstand_m`, `richtung`, `suche: wegpunkte`). |
| Leuchtfeuer | `kamera_frei.pruefe_leuchtfeuer` | `_fern` muss die Held-Silhouette zeigen (≥ 30 % und ≥ 10 m oder ganz). Ein Baumhain muss ≥ 1,5 × Bestand hoch sein (P90 im Ring). Info: Silhouette vor dem Himmel ja/nein. |
| Blöcke im See | `see_bloecke.py` (Planer `korrigieren`, Prüfer) | Stücke ≥ 0,5 m (ohne Pflanzen) mit Oberkante ≥ Spiegel + 0,3 m oder ≤ Spiegel − 1,5 m. Ausnahmen: `teilweise_ueberflutet`, zugefrorene Seen. Verstoß → **FEHLER**. |
| Organische Kanten | `Stempel.rauschen_spec` (Feld `rauschen` je Op oder `gelaende`) | Wertrauschen auf Radius und Rand von Mulde, Kuppe, Terrasse, Rinne, Abbruch und Damm (`anteil`, `wellenlaenge_m`). Seebecken bleiben ohne Rauschen. |

Dokumentation: `PLANER_ANLEITUNG.md` §3.12, README „Auftrag 13h“. Selbsttest: `selbsttest.py` Schritt 12 (`selbsttest_13h.py`)
mit synthetischer Abbruchkante, Fels-Deckung, Böschung am Säulenhain, Kronenabstand, Strahl durch die Krone, Riesen-Regel
und Seeblock-Band.

## Alle Biome (2 m, Endstand)

**Gesamtergebnis:**
- In allen Biomen **0 FEHLER**.
- Zwei Läufe sind byteidentisch (alle 15 Biome, Diff 0).
- Geprüft in einem eigenen Worktree ohne fremde, nicht committete Änderungen.
- Die Bachstufen aus 13f sind unverändert.

**Was die Regeln gefunden haben:**
- Steile Erdwände gab es in 14 von 15 Biomen. Am stärksten betroffen waren Gletscher, Canyon und Fjord.
- Repariert wurde gestalterisch:
  - verkleidet mit den A15-Wandnetzen;
  - Becken und Terrassen kleiner gemacht;
  - Kameras versetzt.
- Keine Regel wurde aufgeweicht.

| Biom | Steil neu / verkleidet (m²) | Wandnetze | Kameras versetzt | Prüfer | WARNUNG (Herkunft) |
|---|---|---|---|---|---|
| aue | 113 / 106 | 14 | 10 | 0 FEHLER | 0 |
| bergwald | 819 / 808 | 76 | 19 | 0 FEHLER | 4: Stufen ohne Niagara, Karsee-Ufer 4 von 168 Proben (13g/13i) |
| canyon | 2 587 / 2 580 | 120 | 16 | 0 FEHLER | 1: versickert 16 m (A9) |
| dschungel | 532 / 527 | 67 | 13 | 0 FEHLER | 0 |
| elfenwald | 377 / 371 | 37 | 18 | 0 FEHLER | 3: `_nah` 16,0 m bei elfenwald_02, Stufen ohne Niagara |
| fjord | 2 030 / 2 006 | 179 | 6 | 0 FEHLER | 5: Stufen ohne Niagara, 2 m² Änderung < 3 m am Wasser |
| frost | 619 / 618 | 50 | 12 | 0 FEHLER | 0 |
| gletscher | 4 265 / 4 149 | 249 | 12 | 0 FEHLER | 9: Stufen ohne Niagara, versickert 15 m |
| heide | 8 / 8 | 2 | 7 | 0 FEHLER | 0 |
| kueste | 1 231 / 1 222 | 79 | 11 | 0 FEHLER | 0 |
| lava | 907 / 875 | 73 | 17 | 0 FEHLER | 1: versickert 23 m |
| oedland | 201 / 196 | 26 | 10 | 0 FEHLER | 0 |
| sumpf | 0 / 0 | 0 | 12 | 0 FEHLER | 0 |
| tundra | 126 / 126 | 13 | 11 | 0 FEHLER | 1: Stufen ohne Niagara |
| wueste | 270 / 268 | 31 | 14 | 0 FEHLER | 1: versickert 23 m |

Lesehilfe:
- „Steil neu“ ist die Fläche > 45° nach dem Stempel im 1-m-Raster.
- Der unverkleidete Rest liegt in Gebieten ≤ 20 m².
- Alle WARNUNGen stammen aus Bach- und Wasserregeln (13g/13i/A9), keine aus 13h.

**Leuchtfeuer in anderen Biomen**

Die Riesen-Regel (≥ 1,5 × Bestand) hat zwei Haine angehoben bzw. freigestellt:
- **elfenwald_02:** Altbäume ×1,3–1,6.
- **frost_04 Raureifhain:**
  - Bäume ×0,8–1,1, Freiraum r 106 m.
  - Die Raureifbäume stehen frei auf der Ebene wie die Schneemonster
    am [Zaō](https://de.wikipedia.org/wiki/Za%C5%8D-san) (Juhyō).
  - `_fern` sieht sie vor dem Himmel.

## 13i K9 (Koordinator)

**gletscher_03 Moränensee (Karbank):**
- Bank kleiner und niedriger: Terrasse r 18 m, Streckung 1,3, Rand 10 m.
- Stempel 46,5 m → **37,5 m**. Der Schnitt bleibt groß, weil der Moränensee in einen steilen Hang gesetzt ist.
- Die Hangseite trägt massive Klippen 12–22 m (`verkleiden`, 64 Netze, 1 760 von 1 783 m²).

**gletscher_05 Wächte:**
- Damm breiter und flacher (Breite 26 m, Höhe 1,8 m), Bergschrund 6 m breit.
- Das Rauschen bricht das gerade Band auf.
- Schrundkante ohne eigenen Akteur.

**gletscher_01/04/08 (Balken- und Halbringformen):**
- Rauschen auf alle Stempel-Ops (`anteil` 0,15, Wellenlänge 8 m).
- gletscher_01 trägt die Torwände mit Klippen 10–16 m (47 Netze).

**canyon_03 Rote Stufe:**
- Das Terrassenband über 142 m ist **gewollt**: Es ist die Stufe selbst, ein durchgehendes Schichtband wie im Colorado-Plateau.
- Die Kanten sind jetzt organisch (Rauschen), der Stempel liegt bei 5,4 m.
- Die Abbruchkante trägt Klippen 10–18 m (39 Netze).

**Küste:**
- kueste_06 (Stadionform), kueste_02 (Ellipse) und kueste_07 (Balken) haben Rauschen auf Rand und Radius.
- `sockelgeroell` mit `boden_min_m` 0,0.
- Kleinzeug an der Meereskante wird entfernt, wenn es im 1-m-Raster unter dem Meer läge.

**lava_05 Klare Spalte:**
- Die Spalte hat organische Wände (Rauschen mit kleinem Anteil, damit das Ufer hält).
- 32 Netze verkleiden die Wände.
- `_held` und `_nah` standen im Spaltwasser und sind ans Ufer versetzt.

**bergwald_06 `_nah`:** steht nicht mehr im See, sondern am Südufer (siehe Befund 2).

**K1 (Bachquerschnitt):**
- Liegt beim 13g-Agenten, `bach.py` ist nicht geändert.
- Meine Begrenzung `bach_einschnitt_begrenzen` greift nur außerhalb von Netzrand + Uferring.

## Rückfragen

1. **Schauseite der Klippennetze:** `front_achse +y` für `rcygn_tier_0`, `SM_HugeNordicCoastalCliff_*` und
   `SM_big_rock_wall_01` ist angenommen (E35). Wenn die Schauseite im Editor nach hinten zeigt, reicht ein Eintrag in
   `gefaelle_regeln.json` → `biome.<biom>.netze.wand`.
2. **`Fir_07_Forest` auf 570 m:** Es ist ein Nicht-Nanite-Netz. Bitte prüfen, ob LOD oder Impostor die Kronen in `_fern`
   zu früh vereinfachen.
3. **Fels-Erkennung im Prüfer:** `ist_fels` arbeitet mit Namensmustern (rock, cliff, boulder, stone, basalt, wall …, dazu
   Megascans-Scans `*_tier_N` und Ordner `/Rocks/`, `/Cliffs/`).
   Ein eigenes Kennzeichen im Inventar wäre robuster.
4. **Akteur-Budget:** Durch die Verkleidung haben einige Orte bis 78 Akteure (Katalog-Richtwert 25). Soll ein Teil der
   Wandnetze als ISM-Instanzen laufen, oder ist das Budget so in Ordnung?
5. **sumpf_02 `_fern`:** Der Planer meldet eine WARNUNG: Nach 540 m liegt ein Rohrkolben-Horst im Strahl. Der Prüfer
   meldet dort nichts. Bitte im Bild ansehen, ob der Horst die Silhouette stört.

## Commits

- Vorfassung Bergwald für den zweiten Pilot: **`73e5cb3`**.
- Alle Biome (Verkleidung, Kameras): `8c6514e`.
- Doku und Eis-Ausnahme: `d0c6e3a`.
- Testbilder aller 15 Biome (erzeugt aus `d0c6e3a`): im Zwischenstand-Commit `2dc19e6`.
- Endfassung dieser Antwort und Bergwald-README: siehe Commit-Nachricht „Auftrag 13h: Endfassung“ auf dem Branch.
