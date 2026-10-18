# Antwort 22b – Wasserpflanzen: Rückfragen zu T22-0, Regeln 22.2, Pilot F6

Gelesen: recherche/auftraege/22b-wasserpflanzen-t22-0-rueckfragen.md @ 26be0ab7e6f28a6ac34a8356f83ecef977609c02 (Commit 13d268e)

Stand 18.10.2026. Bearbeiter: Cloud-Recherche. Bezug: Antwort 22 (Blob ec8434570446, Commit 41e3ca5), inklusive „Nachtrag 16:45“.
Im Projekt ist hier **nichts geprüft oder angewendet**. Der Patch 22.2 (§8) lief nur synthetisch in der Cloud.
Kennzeichnung: [Repo] = Datei im Repository, [Ableitung] = aus Belegen geschlossen, [Annahme] = Startwert, im Pilot zu bestätigen.

## Kurzfazit

1. **Kriterium 3 gegen §4.1: beantwortet.** Antwort 22 war in zwei Punkten widersprüchlich. Das ist unser Fehler.
   - In einer Wasserzelle wird nur noch „zu_tief“ entfernt: bei sicherem Spiegel und Tiefe > Grenze + 0,2 m. Sonst ist es ein Hinweis.
   - Im Uferband mit `dh ≤ 0,5 m` gilt nur die harte Hanggrenze von 35°, nicht mehr 15°.
   - Neue Regelversion 22.2, korrigierte Pilot-Kriterien in §1.3.
2. **Houdini-Wassernetze (V0): beantwortet.**
   - Die 10 bleibenden Wasserfälle zählen als gebautes Wasser, aber nur ihr Tosbecken bzw. Abfluss.
   - An den 15–18 Netzen, die wegfallen, bleiben die Pflanzen gesperrt. Netz und Pflanzen werden im selben Arbeitsgang behandelt, das Netz zuerst.
3. **„zu tief“ an der SWR in C2 (246): beantwortet.** Ja, auslassen. Die Wasserzellen im SWR-Gebiet gelten als „Spiegel unsicher“ und
   ergeben nur einen Hinweis. Der Grund ist der Befund aus 6k/6l: Simulationsboden und -oberfläche weichen vom Gelände ab.
4. **Trockenbett-Ersatz: beantwortet.**
   - Neue Bettsohle-Gruppe für das Standardbiom aus Ufer-Kieseln und Ästen des grünen Satzes.
   - Statt abzurunden gilt: je Bett ⌈n/2⌉ Gruppen.
   - Für „quelle“ gilt die wörtliche Definition (39 Flächen, dazu `quellsumpf_see`). Die 50 weiteren Flächen sind keine Ausnahme.
5. **V1: beantwortet.** `karte_wasser.r8` jetzt mit Sicherung neu schreiben. **Kein** Planer läuft deswegen neu. Ein späterer Neulauf ist erst
   möglich, wenn es eine Reparatur-Sperrliste gibt; Reihenfolge und Ausschlüsse stehen in §5.
6. **lily: beantwortet.** Einverstanden: Die 8 470 lily in Wasserzellen laufen als eigene Nachrunde mit der normalen v3-Regel.
   Die Klassenzuordnung prüft künftig Importquelle und Material statt eines Musters im Netznamen.
7. **T22-0: angenommen.**
   - 12 979 Verstöße liegen im erwarteten Bereich.
   - Den Rest > 15 m messen wir ohne lily: 4,0 % (obere Kante), > 50 m 1,7 %.
   - TWI bleibt aus.
   - Pilot F6 statt C4: einverstanden.
8. **Nächste Handlung:** T22-0b. Die Prüfklasse wird auf 22.2 umgestellt, der Trockenlauf läuft nur lesend, und die F6-Liste wird eingefroren (§9).

---

## 1. Kriterium 3 und §4.1 (Frage 1)

### 1.1 Was in Antwort 22 nicht zusammenpasste

- §4.1 Schritt 2 entfernt Rohrkolben über 0,8 m und Binsen über 0,3 m Tiefe als „zu_tief“. §8.2 Kriterium 3 verlangt aber „0 Entfernungen in
  Wasserzellen“. Kriterium 3 sollte nur verhindern, dass richtig stehende Pflanzen entfernt werden. Formuliert war es weiter als die Regel.
- Tabelle §3 verlangt im Uferband `hang ≤ 15°` (Binse 20°). Kriterium 3 schützt dagegen das 6-m-Band mit `dh ≤ 0,5 m` ohne
  Hangbedingung. Die 15 C4-Fälle zeigen, dass beides zusammen nicht erfüllbar ist.
- Der Referenzcode §7 führt Hang > 35° am Altbett als Fall „trockenbett“. Die Aktion „entfernen“ ist richtig, die Bezeichnung falsch.
  So entstanden die 350 B5-Binsen, die als Trockenbett gezählt wurden, aber nicht ersetzt werden. 22.2 nennt den Fall „hang“ und
  setzt das Merkmal `am_altbett`.

### 1.2 Entscheidung (Regeln 22.2)

- **Welche Wasserzellen zählen:** nur gebaute Wasserzellen der Wasser-Wahrheit. Für Rohrkolben und Binsen ist das Süßwasser, für
  Schwimmblätter zusätzlich das Meer. **Nicht** dazu gehören:
  - der SWR-Überlauf;
  - Zellen der alten Karte;
  - V0-Flächen an Houdini-Netzen, die noch stehen.
- **Entfernen in einer Wasserzelle** ist nur als „zu_tief“ erlaubt, und nur wenn beides gilt:
  1. Der Spiegel stammt aus `spiegel_cm` oder dem Fluss-Spline. Er ist also nicht die Geländehöhe der Randzelle als Ersatz und
     liegt nicht im SWR-Gebiet.
  2. Die Tiefe liegt über Grenze + 0,2 m: Rohrkolben > 1,0 m, Binse > 0,5 m.

  Sonst gilt `hinweis` / `tiefe_unsicher`, und die Pflanze bleibt stehen. Begründung [Ableitung]: Typha-Bestände reichen bis
  etwa 100 cm Wassertiefe (Antwort 22 §2). 0,2 m ist dieselbe Raster- und Pivot-Toleranz wie bei `dh`. Schwimmblätter werden in
  Wasserzellen nie entfernt.
- **Hang im Uferband:** Bei `d_w ≤ d_max` und `dh ≤ 0,5 m` gilt nur die harte Grenze von 35°. Der Grund ist geometrisch
  [Ableitung]:
  - Wer höchstens 0,5 m über dem Spiegel und höchstens 6 m vom Wasser steht, hat zur Wasserkante im Mittel höchstens
    atan(dh/d_w) Neigung.
  - Der lokale Hang aus `hoehe.f32` mit σ 1,5 m misst an eingeschnittenen Ufern dagegen die Böschung über und unter dem Standort.
  - Ein schmaler Röhrichtsaum am Fuß eines steilen Ufers ist der natürliche Fall, kein „komisch platziertes“ Asset.

  Über `dh` 0,5 m (das betrifft nur Binsen, bis 1,5 m bzw. 2,5 m) bleiben die Grenzen 20°/25° aus Tabelle §3. Die
  Feuchte-Ausnahme behält ihre 8°/12°.
- **Folge für C4 [Ableitung]:** Die 15 Fälle im Uferband werden `ok`, sofern ihr Hang ≤ 35° ist. Die 9 „zu tief“ werden nur bei
  Tiefe > Grenze + 0,2 m und sicherem Spiegel entfernt.

### 1.3 Korrigierte Pilot-Kriterien (T22-F6-1, Regeln 22.2)

| Nr | Prüfung | Kriterium | Stand |
|---|---|---|---|
| 1 | Messweg | T22-0 trifft den Zensus auf ±1 % (9 679 statt 9 680, 6 094 statt 6 095, 18 839). Der Selbsttest liefert dieselbe Signatur. Die D5-Kontrollen (Brücke) sind `ok`. | erfüllt bis auf D5: in 22b nicht berichtet, mit T22-0b nachliefern |
| 2 | Eingabestand | F6-Liste aus T22-0b eingefroren mit SHA-256 (Teamworkflow, „Feste Prüfeingaben“ Punkt 1). Altwasser aus der gesicherten alten Karte. V0-Anteil ≤ 2 %. | offen |
| 3 | Nachprüfung | 22.2 ist eine Korrektur. Vor der Anwendung prüft ein unabhängiger technischer Prüfer nach Teamworkflow Punkt 2 die Fälle aus §1.1 nach. | offen |
| 4 | Formal | Nach der Anwendung hat F6 0 Verstöße (Rohrkolben, Binse, Schwimmblatt) außer `gesperrt`/`hinweis`. Sicherungszeilen = entfernte Instanzen, Zugaben = Protokollzeilen. Die 1-%-Rücknahme-Stichprobe ist transformgleich. Je Paket gibt es einen Speicherbeleg. Nach dem Neustart reproduziert der Zensus die Zahlen. | offen |
| 5 | Fehlalarm | 0 Entfernungen von Instanzen, die 22.2 als `ok`, `ok_feucht`, `ok_ausnahme`, `hinweis` oder `gesperrt` führt. Insbesondere 0 in Wasserzellen ohne „zu_tief“ nach §1.2 und 0 im Uferband mit `dh ≤ 0,5 m` und Hang ≤ 35°. Stichprobe: 20 entfernte und 20 behaltene Instanzen per Draufsicht gegen die Rasterwerte; jede „zu_tief“-Entfernung einzeln. | offen |
| 6 | Ersatz | Je Bett ⌈n/2⌉ Gruppen, Gruppenwahl nach §4.1. Keine Zugabe in einer Wasserzelle, auf `karte_weg` oder über 25° Hang. Rücknahme = Zugaben löschen. | offen |
| 7 | Bild | „F6 typisch“ mit gleicher Kamera: kein grüner Rohrkolben auf Riss-Schlamm, das Bett zeigt Kies und Trockengras. Die D5-Brücke ist unverändert (Kontrollstelle). Ein F6-Ufer an gebautem Wasser zeigt unveränderten Röhrichtsaum (Vergleichsstelle nach `pruefung.md`). | offen |
| – | Abbruch | Abbrechen, wenn V0 > 2 %, wenn mindestens 2 der 20 entfernten Stichproben sichtbar richtig standen oder wenn ein Speicherbeleg fehlt. Dann wird nicht ausgeweitet, sondern die Regel geprüft. | |

---

## 2. Houdini-Wassernetze (Frage 2)

- **Bleibende Netze (10 Wasserfälle) sind gebautes Wasser, aber nur ihr Tosbecken bzw. der Abfluss am Fuß.**
  - In die Wasser-Wahrheit aufnehmen als Typ `houdini_bleibt` (anzulegen), mit dem Spiegel des Beckens.
  - Die fallende Fläche selbst zählt nicht. Sie liegt ohnehin über 35°, und Rohrkolben neben dem Fallschleier wären falsch.
  - Danach entfällt die V0-Sperre, und die normale Regel urteilt. Pflanzen werden also nicht pauschal behalten: Wer weit vom Becken
    steht, bleibt ein Verstoß.
- **Netze, die wegfallen (15–18):** Die Pflanzen bleiben bis zur Entfernung gesperrt (`gesperrt`, keine Reparatur). Die Reihenfolge
  je Feld läuft in einem Test unter einer Test-ID:
  1. Netz und Instanzen sichern.
  2. Netz entfernen, mit Speicherbeleg.
  3. Die V0-Sperre entfällt. Die Regel 22.2 läuft auf dem eingefrorenen Stand des Feldes, danach wird entfernt oder ersetzt.
  4. Neuer Zensus.
- **Nicht** zuerst die Pflanzen entfernen: Dann stünde sichtbares Wasser ohne Saum da. Und nicht das Netz entfernen und die Pflanzen
  lange stehen lassen: Dann stünde Röhricht im Nichts.
- **Ausnahme:** Ist an derselben Stelle neues Wasser geplant (z. B. ein See aus Antwort 19), bleiben die Pflanzen gesperrt, bis dieses
  Wasser gebaut ist. Dann bestimmt dessen Ufer das Urteil.
- **C4:** Die 175 Fälle bleiben gesperrt, bis die C4-Netze zugeordnet sind. Die Netzliste `houdini_wasser_rest_r4.md` liegt nur lokal,
  nicht im Repo. Welche der 175 an bleibenden Netzen stehen, kann ich daher nicht prüfen.

## 3. „zu tief“ an der Shallow-Water-Simulation in C2 (Frage 3)

**Entscheidung: auslassen, wie in v3.**

- **Umsetzung:** Wasserzellen im SWR-Gebiet bekommen `spiegel_sicher = false`. Das ergibt `tiefe_unsicher`, und die Pflanze bleibt
  stehen. Landpflanzen im Überlauf werden wie in v3 als Land beurteilt, gemessen am gebauten Bett. Der Überlauf ist kein gebautes Wasser.
- **Begründung [Repo]:** Weder die Spline-Tiefe noch die Simulationstiefe G sagt, wie tief eine Pflanze in C2 sichtbar im Wasser steht.
  - **6k §6:** Im Band liegt der Simulationsboden im Median 64,7 cm unter `hoehe.f32`.
  - **6l:** Boden − Spline p10/p50/p90 = −28,7/+4,2/+41,7 cm. Auch das Deckel-Modell lässt 25–30 cm RMS unerklärt.
  - **Profil s 439:** Simulationsoberfläche − Gelände schwankt zwischen −166 und +50 cm.
  - **Laufende Arbeit:** Das C2-Wasser ist noch in Arbeit (6k: „Wasser bleibt unverändert, bis eure Antwort zu §6 da ist“). Jede
    Bett- oder Pegeländerung würde die Urteile verschieben.
- **Wiederaufnahme:** Erst wenn das C2-Wasser abgenommen ist. Dann wird die sichtbare Tiefe gemessen: gebackene Oberfläche
  (Dump R + Akteurhöhe) − `hoehe.f32` am Instanzort, abgetastet wie in 6l bestätigt. Entfernt wird nur bei Tiefe > Grenze + 0,2 m.
  Das ist nicht Teil des Piloten.

## 4. Trockenbett-Ersatz §6.2 (Frage 4)

### 4.1 Fehlende Gruppe: Bettsohle im Standardbiom (neue Zeile der Tabelle §6.2)

| Lage | Gruppe | Netze (Foliage-Typ) [Repo: `netze.csv`, `inventar.json`] |
|---|---|---|
| standard, Bettsohle (`d_alt = 0`, `hang < 10°`) | 3–5 Kiesel + 0–1 Ast + 0–1 Laubfleck | `SM_SmallStonesPack_08–14` (`FT_EL_UF_SmallStonesPack_<nn>_gruen_kiesel`), `SM_WoodenSticksAndTwigs_01–05` (`FT_EL_UF_WoodenSticksAndTwigs_<nn>_gruen_ast`), `SM_detail_leaves_01/03` (`FT_EL_AUE_detail_leaves_01/03`) |

- **Begründung [Ableitung]:**
  - Das sind die Kiesel- und Ast-Typen des grünen Satzes der Ufer-Ebene. Das Altbett liest sich damit als Geschiebebett derselben Bäche.
  - Laub sammelt sich in trockenen Rinnen der Laubwald- und Auenbiome.
  - Kiesel und Äste sind Nanite-Netze (`nanite = 1`), 0,1–0,2 m groß.
- **Nicht `SM_DryRiverBed_01/02`:** Davon gibt es nur einen Wüsten-Foliage-Typ (`FT_EL_WUES_*`). Die Platten haben 28–30 k Dreiecke
  und sind etwa 1 × 1,66 m groß; ihr Aussehen im Standardbiom ist ungeprüft.
- **Wirkung:** laut T22-0 weltweit 1 Fall, also klein. Die Zeile legt die Regel für spätere Läufe fest.

### 4.2 Rundung „je 2“

- **Nicht abrunden.** Abrunden lässt Betten mit einer einzigen entfernten Instanz leer und kostet je ungeradem Bett eine Gruppe; bei
  1 169 Betten sind das bis zu 1 169 Gruppen.
- **Regel 22.2:** Die entfernten Instanzen eines Betts werden nach dem Hash ihrer Instanz-ID geordnet. Auf Rang 0, 2, 4 … steht je eine
  Gruppe, das ergibt **⌈n/2⌉**. Den Gruppentyp bestimmt die Lage der Instanz auf diesem Rang (Funktion `ersatz_raenge`, §8).

### 4.3 Ausnahmeflächen „quelle“

**Die wörtliche Definition gilt.** Dazu kommt `quellsumpf_see`. [Repo: `bach_anfaenge_plan.json`, 83 Fälle, 8 Enden]

- **Wo Antwort 19 Binsen oder Rohrkolben setzt:** Nur `sickerquelle` (23 von 23), `quellsumpf_see` (1 von 1) und beide Enden
  `versickern_moorwiese` (C4, G4) setzen solche Instanzen. `hangquelle` (37), `quellmulde` (6), `felsquelle` (11) und die übrigen setzen keine.
- **Zusammensetzung eurer 39 [Ableitung]:** Sie ergeben sich vermutlich aus 23 Sickerquellen, 11 Felsquellen, 2 Moorwiesen und den
  Sehens-Orten (u. a. `wueste_04_quelloase`). Fehlt `quellsumpf_see`, kommt diese Fläche dazu (dann 40).
- **`felsquelle` bleibt drin**, obwohl ihr Plan keine Binsen setzt. Sie ist in den trockenen Biomen der einzige Ort für Sickerstellen-Binsen
  (Tabelle §3).
- **Die 50 weiteren Flächen** (`hangquelle`, `quellmulde`, Karsee, Kaskade, Schneetälchen, Seeabfluss, Karstquelle) sind keine Ausnahme.
  - Echte Nässe erkennen dort Mulde und Nassmaske.
  - Ist der Bach gebaut, greift das Uferband.
  - Die 38 Verstöße laufen nach der normalen Regel.
  - F6 enthält zwei Hangquellen (`B_R_P2_P1_02`, `B_R2_R_P2_P1_02`). Eine davon gehört in die Bildstichprobe.

## 5. V1: `karte_wasser.r8` neu schreiben (Frage 5)

**Ja, jetzt und mit Sicherung.** Das Neuschreiben ändert nur eine Eingabe, keine Instanz.

1. **Sichern:** die alte Karte als `karte_wasser_alt_2026-10-18.r8` (Datei anzulegen), mit SHA-256 im Standmanifest.
   - **Wichtig:** Diese Sicherung ist zugleich die Quelle der Altwasser-Schicht `d_alt`. Liest T22 `d_alt` aus der neuen Karte, wird
     `d_alt` überall ∞ und die Fallgruppe Trockenbett verschwindet.
2. **Neu schreiben:** gebaute Süßwasserzellen der Wasser-Wahrheit, mit gleichem Raster, Ursprung und Kodierung (uint8).
   - Die bleibenden Wasserfall-Becken (§2) kommen hinein.
   - Nicht hinein kommen der SWR-Überlauf, die wegfallenden Houdini-Netze und das **Meer**: Es bleibt 0, sonst kippt die Planerregel
     „Meer = hoehe < 0 und karte_wasser == 0“ (Konventionen §1b) [Repo].
   - Als Vorlage dient das lokale `scripts/swr/altwasser_reinigen_p2.py`, mit dem Ferat die C2-Raster schon bereinigt hat (`fluss_sim/ersetzt.json`).
3. **Welche Planer neu laufen müssen: keiner, jetzt nicht.**
   - Die Planer schreiben je Feld die ganze Ebene neu. Eine Option zum Filtern nach Klassen gibt es nicht (CLI: `--basis --bild --faktor --regeln …`).
   - Ein Neulauf würde v3- und T22-Entfernungen zurückbringen und den Piloten aufheben.
   - Die neue Karte verhindert nur, dass ein **künftiger** Lauf wieder an Altwasser setzt.

**Leser von `karte_wasser.r8` im Repo [Repo, grep]:**

- Biom-Planer: aue, sumpf, wueste_ergaenzung, elfenwald, dschungel, heide_tundra, hochgebirge, lava, nordkueste;
- mittelschicht, spuren, felsgruppen (Sperre);
- gefaelle (fremdes Wasser als Schutzzone, also ein Geländeeingriff);
- die Sehens-Planer über `sehens_lib` (bach, daten, rezept, vorschau) sowie sehens_aue und sehens_sumpf.

`welt_bewuchs` liegt nicht im Repo. Ob er `karte_wasser` oder Houdini-Karten liest, ist lokal zu prüfen; er stellt 1 579 der Fälle.

**Wenn später ein Neulauf gewollt ist** (z. B. Röhricht an neuem Wasser):

- nur in den 40 V1-Feldern;
- erst wenn eine **Reparatur-Sperrliste** (anzulegen) existiert. Der Importschritt verwirft damit geplante Instanzen, die einer
  v3- oder T22-Sicherungszeile entsprechen (gleiches Netz, Position ±0,5 m);
- Reihenfolge nach Konventionen §4: felsgruppen → Biom-Planer → mittelschicht → spuren, je Feld eine Test-ID.

**Nicht neu laufen lassen:**

- gefaelle/bachbett: Das ist Gelände.
- fluss_sim-Export.
- sumpf in H5: Die Nassmaske ist gewollt, 1 312 Binsen gehalten.
- C2: Die 16h-Arbeit läuft noch.
- Jede Ebene in Feldern mit abgeschlossener v3-Reparatur oder im F6-Piloten, solange die Sperrliste fehlt.

**Prüfung der neuen Karte** (vor der Nutzung; Teamworkflow Punkt 3 verlangt dazu den Abgleich mit dem Editor):

| Kontrollfall | Erwartung |
|---|---|
| C2, alter `F_ERLENBACH_1_C2` (Houdini-Stand, 23–39 m breit, „existiert lokal nicht mehr“, `ersetzt.json`) | Zellen außerhalb des p2-Betts = 0, das Bett von Erlenbach p2 = Wasser. Abweichung zur lokal mit `altwasser_reinigen_p2.py` bereinigten C2-Karte ≤ 1 % der Fensterzellen |
| D5-Brücke | Wasserzellen im Kontrollfenster unverändert, D5-Kontrollen bleiben `ok` |
| Meer | Zahl der Meer-Zellen nach Planerformel unverändert, 0 Zellen mit `hoehe < 0` neu in der Karte |
| Felder | 30 Felder außerhalb von V1 byte-gleich; in den 40 Feldern genau die 1,13 Mio. gemeldeten Zellen geändert |
| T22 mit neuer Karte | V1-Abweichung 0 in allen Feldern, Urteile unverändert (T22 nutzt schon die Wasser-Wahrheit) |

## 6. lily = Maiglöckchen (Frage 6)

**Einverstanden.**

- **Nachrunde:** Nach Abschluss der laufenden v3-Reparatur kommt eine eigene Nachrunde nur für `SM_lily_01_1/_2` mit eigener Test-ID.
  - Sie nutzt die normale v3-Regel: Pflanze im Wasser (Gelände < Spiegel − 2 cm), Basis-Regel, Bodenstreu-Ausnahme.
  - Die Ausschlüsse wie in v3 gelten: Der SWR-Überlauf ist kein Wasser, V0-Flächen bleiben gesperrt.
  - Erwartung [Ableitung]: Weniger als 8 470 werden entfernt; an der Wasserlinie (Gelände ≥ Spiegel − 2 cm) bleiben einige stehen.
  - Zuerst ein Feld mit festen Kameras, dann die übrigen.
- **Klassenmuster:** `lily(?!ofthevalley)` entfällt. Wasserpflanzen werden nur noch über die festen Präfixe aus §7 erkannt
  (`SM_Rohrkolben_`, `SM_ToadRush_`, `SM_WaterPlant0`, `Rembrandt_Water_Lily_`).
  - Zusätzlich gilt als Landpflanze, wenn der normalisierte Netzname, die Importquelle oder das Material `lilyofthevalley` enthält.
    Normalisiert heißt: Kleinbuchstaben, nur a–z und 0–9. Aus `SM_lily-of-the-valley_beech_forest_01_1.fbx` wird so `…lilyofthevalley…`.
  - Der Netzname allein reicht nicht, weil er `SM_lily_01` lautet.
- **Zählung:** lily fällt aus dem Nenner der Wasserpflanzen-Kennzahlen.
- **Katalog (nur Hinweis, hier nicht geändert):** `sehens/aue/katalog.md` und `asset_bedarf.json` führen `SM_lily_01_1` als
  Seerosen-Ersatz. Ersatz sind `SM_WaterPlant01–04` oder die flache Rembrandt Water Lily VarB (0,01 m).

## 7. Zu den T22-0-Ergebnissen

- **12 979 Verstöße (19,1 %): angenommen.** Das liegt in 10 500–15 500.
- **Rest > 15 m 5,3 % gegen unsere 2–4 %: angenommen, aber ohne lily gemessen (4,0 %, > 50 m 1,7 % ≤ 2 %).** Gründe [Ableitung]:
  1. **lily:** War Teil der Klasse, wurde aber nicht geprüft. Jedes Maiglöckchen fern vom Wasser zählte als Rest, obwohl es dort richtig
     steht. Das erklärt 1,3 Prozentpunkte.
  2. **H5 hält mehr als erwartet:** Die Nassmaske hält 1 312 Binsen; 407 statt 850–1 400 Verstöße. Wir hatten 35–60 % Verbleib
     angenommen, der Schätzwert war zu niedrig.
  3. **Übrige Ausnahmen:** `quelle`-Flächen, die Nasswiesen-Ausnahme der Binsen (`feucht` überall) und, falls mitgezählt, die
     V0-gesperrten Fälle (C4 175).
  - **Offen, kein Blocker:** Das Urteil zum Bildfall „H5 typisch“ (ToadRush_00, 19 m, Grasmatte ohne sichtbaren Schlamm). Ist es
    `ok_feucht`, ist die Maske für Binsen außerhalb der Bultzone zu großzügig. Das wird bei H5 entschieden, nicht im Piloten.
- **TWI-Zweig aus: bestätigt.** P20 nass 3,36 liegt unter P90 trocken 6,51, und die Schwelle läge außerhalb 7–12. Mit 9,0 gäbe es nur
  32 Verstöße weniger.
- **`GT_Schilf` −42,7 %:** liegt in 35–55 %. Die Anwendung kommt später als eigener Schritt.
- **1 169 Trockenbetten, keines erfüllt „Wasser zurück“:** Die Rechnung ist nicht belastbar (keine Senkenfüllung). Es gilt weiter
  „trocken mit Trockenbett-Bewuchs“, rücknehmbar. Ferats Rückfrage bleibt offen und blockiert nicht.
- **Pilot F6 statt C4: einverstanden.**
  - C4 erfüllt unser eigenes Abbruchkriterium (13,0 % > 2 % in V0), dort wird also nicht repariert.
  - F6 hat V0 0 % und 0 Fälle zu Kriterium 3. Es enthält den Bildfall „F6 typisch“ (Horst_3 auf Riss-Schlamm) und ist zu 96 % aue.
    Damit prüft F6 den Trockenbett-Pfad samt neuer Bettsohle-Gruppe und die Quell-Entscheidung (zwei Hangquellen).
  - Nicht abgedeckt sind „fern im Trockenen“ in der Wüste (C4_09), Sumpf, Hang > 35° und Houdini. Dafür folgt ein zweiter Pilot in einem
    Wüsten- oder Canyonfeld mit V0 ≤ 2 % (Kandidaten D4, D6 laut T22-0b-Liste).

## 8. Regeln 22.2 als Patch auf den Referenzcode §7

Der Patch wird angewendet mit `python -I patch_22_2.py wasserpflanzen_regel.py wasserpflanzen_regel_22_2.py`. Eingabe ist §7 wörtlich mit
LF-Zeilenenden; bricht ein `assert` ab, stimmt die Eingabe nicht.

**Cloud-Ergebnis:** §7 aus Antwort 22 ergibt unverändert `Signatur 521ccd76eaca5822`. Nach dem Patch ergibt sich zweimal
`SELBSTTEST OK  Regeln 22.2  Faelle 17  Cluster 1  Signatur 3a7bbb3194511658`.

Die drei neuen Fälle trennen die Versionen. Mit 22.1 wären „Uferfuß am Steilufer“ (Hang 26,3°, `dh` 0,23 m) und „Tiefe 0,88 m“ beide
`verstoss`, mit 22.2 sind sie `ok` bzw. `hinweis`.

```python
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)
rep('REGEL_VERSION = "22.1"', 'REGEL_VERSION = "22.2"')
rep('    ("lily_pruefen", ("SM_lily_01_",)),       # bis zur Netzpruefung (Frage 5) weder Wasser- noch Landregel\n',
    '    # 22.2: SM_lily_01_* ist Maigloeckchen (Importquelle/Material lily-of-the-valley) -> keine Wasserpflanze\n')
rep('def art(netz):\n    n = netz.split("/")[-1].split(".")[0]\n',
    'def _norm(t):\n    return "".join(c for c in (t or "").lower() if c.isalnum())\n\n\n'
    'def art(netz, import_quelle=None, material=None):\n    n = netz.split("/")[-1].split(".")[0]\n'
    '    if any("lilyofthevalley" in _norm(t) for t in (n, import_quelle, material)):\n        return None                      # Landpflanze, normale v3-Regel\n')
rep('HANG_HART = 35.0                                    # darueber nie (B5-Felsflaechen), ausser Quellpolygon\n',
    'HANG_HART = 35.0                                    # darueber nie (B5-Felsflaechen), ausser Quellpolygon\n'
    'UFERFUSS_DH = 0.5                                   # 22.2: im Uferband mit dh <= 0,5 m gilt nur HANG_HART\n'
    'TIEFE_TOL = 0.2                                     # 22.2: zu_tief erst ab TIEFE_MAX + 0,2 m; spiegel_sicher False = SWR-Gebiet, Gelaende-Ersatz\n')
rep('def felder(hoehe, wasser, spiegel, altwasser, lagen=None, quellpoly=None, zelle=ZELLE_M):',
    'def felder(hoehe, wasser, spiegel, altwasser, lagen=None, quellpoly=None, zelle=ZELLE_M, sperre=None, spiegel_sicher=None):')
rep('    return dict(hoehe=hoehe, wasser=wasser, spiegel=spiegel, d_w=d_w, sp=sp_naechst, d_alt=d_alt, hang=hang,',
    '    leer = np.zeros(hoehe.shape, bool)\n'
    '    return dict(sperre=sperre if sperre is not None else leer,\n'
    '                sicher=spiegel_sicher if spiegel_sicher is not None else ~leer,\n'
    '                hoehe=hoehe, wasser=wasser, spiegel=spiegel, d_w=d_w, sp=sp_naechst, d_alt=d_alt, hang=hang,')
rep('def pruefe(netz, x, y, biom, F):\n    a = art(netz)\n    if a is None or a == "lily_pruefen":',
    'def pruefe(netz, x, y, biom, F, import_quelle=None, material=None):\n    a = art(netz, import_quelle, material)\n    if a is None:')
rep('    if F["wasser"][i, j]:\n',
    '    if F["sperre"][i, j]:                # V0: Houdini-Netz, das noch steht (+ 25 m)\n'
    '        return dict(m, urteil="gesperrt", fall="sperre", grund="V0-Sperrflaeche", aktion="behalten")\n'
    '    if F["wasser"][i, j]:\n')
rep('        if tiefe > TIEFE_MAX[a]:\n',
    '        if tiefe > TIEFE_MAX[a] and (tiefe <= TIEFE_MAX[a] + TIEFE_TOL or not F["sicher"][i, j]):\n'
    '            return dict(m, urteil="hinweis", fall="tiefe_unsicher", grund="Tiefe %.2f m, Toleranz/Spiegelquelle" % tiefe, aktion="behalten")\n'
    '        if tiefe > TIEFE_MAX[a]:\n')
rep('        fall = "trockenbett" if d_alt <= ALT_M else "hang"\n        return dict(m, urteil="verstoss", fall=fall,',
    '        m["am_altbett"] = bool(d_alt <= ALT_M)   # 22.2: Fall bleibt "hang", kein Ersatz\n        return dict(m, urteil="verstoss", fall="hang",')
rep('    if d_w <= r["d_max"] and dh <= r["dh_max"] and hang <= r["hang_max"]:',
    '    hang_ok = hang <= r["hang_max"] or dh <= UFERFUSS_DH      # 22.2: Uferfuss nur HANG_HART (oben)\n'
    '    if d_w <= r["d_max"] and dh <= r["dh_max"] and hang_ok:')
# Selbsttest: steiles Ufer x 150..190 suedlich des Flusses, 0,45 m/m (~24 Grad)
rep('    h = np.where((x > 200) & (y > 100), h + (x - 200) * 1.2, h)   # Steilwand Osten (~50 Grad)\n',
    '    h = np.where((x > 200) & (y > 100), h + (x - 200) * 1.2, h)   # Steilwand Osten (~50 Grad)\n'
    '    steil = (x > 150) & (x < 190) & (y > 44) & (y < 52)\n'
    '    h = np.where(steil, 19.5 + 0.02 * x + 0.45 * (y - 44), h)       # 22.2: steiles Ufer, Fuss knapp ueber Spiegel\n')
rep('        ("SM_LilyOfTheValley_02", 100.5, 80.5, "nicht_geprueft"),\n',
    '        ("SM_LilyOfTheValley_02", 100.5, 80.5, "nicht_geprueft"),\n'
    '        ("SM_Rohrkolben_Jung_1", 170.5, 44.5, "ok"),               # 22.2: Uferfuss am Steilufer (Hang > 15 Grad, dh 0,2 m)\n'
    '        ("SM_Rohrkolben_Jung_1", 100.5, 42.5, "hinweis"),          # 22.2: Tiefe 0,88 m, innerhalb Toleranz\n'
    '        ("SM_Rohrkolben_Jung_1", 100.5, 40.5, "verstoss"),         # Tiefe 1,38 m -> zu_tief\n')
rep('    assert urteile[3]["fall"] == "fern_trocken" and urteile[9]["fall"] == "hang"\n',
    '    assert urteile[3]["fall"] == "fern_trocken" and urteile[9]["fall"] == "hang"\n'
    '    assert urteile[14]["hang"] > 15.0 and urteile[16]["fall"] == "zu_tief", (urteile[14], urteile[16])\n'
    '    assert art("SM_lily_01_1", "SM_lily-of-the-valley_beech_forest_01_1.fbx") is None and art("Rembrandt_Water_Lily_x_VarB") == "schwimmblatt"\n'
    '    Fs = felder(h, fluss, spiegel, bett, lagen, sperre=np.ones(h.shape, bool))\n'
    '    assert pruefe("SM_Rohrkolben_Horst_6", 30.5, 80.5, "wueste", Fs)["urteil"] == "gesperrt"\n'
    '    Fu = felder(h, fluss, spiegel, bett, lagen, spiegel_sicher=np.zeros(h.shape, bool))\n'
    '    assert pruefe("SM_Rohrkolben_Jung_1", 100.5, 40.5, "aue", Fu)["fall"] == "tiefe_unsicher"\n'
    '    assert [len(ersatz_raenge(range(n))) for n in (1, 2, 5)] == [1, 1, 3]\n')
rep('def cluster_versetzen(', 'def ersatz_raenge(ids):\n    """22.2: je Bett ceil(n/2) Ersatzgruppen: Rang nach Hash der Instanz-ID, Gruppe an Rang 0, 2, 4 ..."""\n'
    '    r = sorted(ids, key=lambda k: hashlib.sha256(str(k).encode()).hexdigest())\n    return r[0::2]\n\n\ndef cluster_versetzen(')
open(sys.argv[2], "w", encoding="utf-8").write(s)
```

**Lokale Anbindung:**

- `sperre` = V0-Flächen (stehende Houdini-Netze bzw. Altwasser mit Wasserakteur, + 25 m).
- `spiegel_sicher = false` gilt für Wasserzellen im C2-SWR-Gebiet und für Zellen mit dem Spiegel-Ersatz aus der Geländehöhe.
- `import_quelle`/`material` kommen aus den AssetImportData bzw. dem Material-Slot 0.

## 9. Nächste Handlung (eine, lokal)

**T22-0b:** Die Prüfklasse wird auf 22.2 umgestellt (§8), dann läuft der Trockenlauf über alle 70 Felder, nur lesend.

- **Eingaben:**
  - `d_alt` aus der unveränderten bzw. gesicherten alten `karte_wasser.r8`;
  - die C2-SWR-Wasserzellen mit `spiegel_sicher = false`;
  - V0 als `sperre`;
  - `quelle` nach §4.3.
- **Erfolg, wenn alle Punkte gelten:**
  1. Der Selbsttest ergibt lokal zweimal `Signatur 3a7bbb3194511658`.
  2. Verstöße ≤ 12 979. Alle Änderungen in 22.2 halten Instanzen oder lassen sie unverändert.
  3. C2: 0 Fälle „zu_tief“, die 246 erscheinen als `tiefe_unsicher`.
  4. Rest > 15 m ohne lily ≤ 4,0 %.
  5. Die D5-Kontrollen sind `ok`.
  6. Die Zahl der Ersatzgruppen entspricht Σ⌈n/2⌉ je Bett.
  7. Die F6-Liste ist mit SHA-256 eingefroren, V0 0 %.
- **Abbruch:**
  - Weicht die Signatur ab, läuft T22-0b nicht. Zuerst die Eingabe prüfen (§7 wörtlich, LF).
  - Steigen die Verstöße, ist die Umstellung fehlerhaft. Dann melden, nicht anwenden.
- **Danach:** unabhängige Nachprüfung nach Teamworkflow Punkt 2, dann T22-F6-1 mit den Kriterien aus §1.3.
- **Unabhängig davon** kann die Karte nach §5 neu geschrieben werden. Sie blockiert den Piloten nicht.

---

## Was fehlt bis Witcher 4

Messlatte: Witcher-4-Techdemo (UE5, State of Unreal 2025), Belege in `boden-kleinzeug-gras.md`. Sortiert nach Wirkung:

1. **Eine Wasser-Wahrheit für alle Verbraucher.** `karte_wasser.r8`, Houdini-Restnetze, SWR-Überlauf und Wasser-Wahrheit laufen in
   40 Feldern auseinander (1,13 Mio. Zellen). In der Demo entsteht Vegetation zur Laufzeit per PCG aus einer Datenquelle. Bei uns
   erzeugt jede Abweichung neue „komisch platzierte“ Instanzen.
2. **Neuläufe, die Reparaturen erhalten.** Ohne Reparatur-Sperrliste macht jeder Planerlauf v3 und T22 rückgängig. Darum kann die
   Projektleitung heute weder Planer verbessern noch reparierte Felder neu bepflanzen, ohne Arbeit zu verlieren.
3. **Sichtbares Wasser als Messgröße.** Die Platzierung misst gegen Spline und Gelände, gesehen wird aber die gebackene Oberfläche, die
   in C2 bis −166/+50 cm abweicht (6l). Nötig ist ein Raster „sichtbare Tiefe“ (Oberfläche − Gelände) je gebackenem Gewässer als
   Eingabe für Prüfung und Planer (anzulegen).
4. **Röhricht-Assets:** Horste ohne Kolben lesen sich im Trockenen als Agave. Es fehlen Nanite-Röhricht mit Kolben und Wind und eine
   vertrocknete Variante (anzulegen). Echte Seerosen in Stillwasser sind kaum gesetzt; der Aue-Katalog führt noch das Maiglöckchen.
5. **Boden und Bewuchs widersprechen sich:** Riss-Schlamm neben Röhricht, Kiesbett ohne Nassband. Das Bodenmaterial braucht eine
   Feuchte-Lage an Ufer und Mulde, die aus derselben Wasser-Wahrheit kommt.

## Quellen

Alle aus dem Repository, Stand Commit 13d268e. Eine Webrecherche war nicht nötig.

- `recherche/auftraege/22b-wasserpflanzen-t22-0-rueckfragen.md` (Blob 26be0ab7e6f2), `auftraege/22-…` (8bb2f7c07609),
  `antworten/22-wasserpflanzen-fern-vom-wasser.md` (ec8434570446: §2, §3, §4.1, §5, §6.2, §7, §8.2).
- `antworten/bach_anfaenge/bach_anfaenge_plan.json` (3f3f0c41a607): Lösungen, Enden, Instanzen je Fall.
- `vorlagen/daten/netze.csv` (d9bc963cfd32), `inventar.json`, `biome_je_feld.md` (F6 aue 96 %).
- `antworten/skripte/*_plan.py`, `sehens_lib/*.py` (Leser von `karte_wasser`), `aue_regeln.json` (Schilf 0,5–6 m, 12°),
  `sumpf_regeln.json` (`schilf_land` 25°), `fluss_sim/ersetzt.json` (f8548591e5f5), `verteilung-KONVENTIONEN.md` §1b, §4.
- `auftraege/16h-nachtrag6k-t6j-ergebnisse.md` §6, `auftraege/16h-nachtrag6l-boden-schritt1.md` §1–2 (Simulationsboden/-oberfläche).
- `auftraege/16h-nachtrag5-ufer-c2-c4-lagen.md` und `antworten/16h-nachtrag5-…` (Regel „Pflanze im Wasser: Gelände < Spiegel − 2 cm“).
- `auftraege/daten/bach_anfaenge/bach_anfaenge.md` (10 Wasserfälle bleiben; `houdini_wasser_rest_r4.md` nur lokal).
- `recherche/TEAM_WORKFLOW.md` „Feste Prüfeingaben, Nachprüfung und Pilotfreigabe“, `recherche/vorlagen/pruefung.md`.
