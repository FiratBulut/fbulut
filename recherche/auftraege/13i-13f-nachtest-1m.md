> **Auftrag 13i** (Claude lokal, 12.10. 00:10): Nachtest eures Stands 13f auf den echten 1-m-Daten. Danke, fast alles ist wirklich behoben.
> **Dringend sind K1** (Querprofil schneidet bis 30 m seitlich in steile Hänge, senkrechte Wände, gletscher_03 bis 57 m) **und K2** (SM_Fern_02a steckt
> zu 54 % im Boden). Treppenbäche baue ich erst mit 13g. Zum Gestalterischen siehe 13h (Pilot-Bilder). Rollout-Reihenfolge lokal: zuerst oedland, kueste,
> sumpf; der Rest nach K1/K2/13g.

# Auftrag 13 Phase 2 – Korrekturen nach dem lokalen 1-m-Lauf mit dem Stand 13f (an die Cloud)

Stand 11.10.2026 nachts, Claude lokal (Hilfsagent). Getestet: Repo-Stand 93234af, Skripte = **8c47f54** (13f-Korrektur 9e180f5 plus euer
WIP mit Fallketten, Uferring + 0,20 m, Wulst ≤ 1,5 m). Lokale Kopie **ohne** Patches; alle lokalen Übergangslösungen aus. Alle 15 Planer auf den
echten 1-m-Daten, gleiches Inventar wie der vorige 1-m-Lauf (netze_masse 485 Einträge). Laufzeit 22–47 s je Biom (86 s mit Cache-Aufbau).

**Was 13f behoben hat (gleiche Prüfer für alt und neu):** euer Lib-Prüfer findet im alten 1-m-Stand 94 FEHLER, im neuen **5**; unser
Einbau-Prüfer 43 → **11** (davon 6 Eigenheiten unseres Prüfers, siehe unten). Bäume schwebend 108 → 1 (0,23 m), Stücke im falschen Feld 359 → 1,
Bach-Ufer unter dem Spiegel 634 → 74 m (Längsschnitt), Gelände über dem Spiegel 185 → 9 m, Mündungen/Abflüsse unter dem Spiegel 14 → 0,
versickert < 25 m 5 → 0, Seen < 10 m² 24 → 0, Lagen am Fensterrand 137 → 0, Materialwünsche biomweit vollständig, sumpf_05 jetzt verdeckt,
Efeu „im Meer“ 0. Danke!

Die folgenden Punkte betreffen nur Planer oder Bibliothek. Koordinaten X/Y in m (Unreal/100).

**Nachtest mit eurem neueren Zwischenstand ff10214 (23:29, 8 Biome, sonst gleich):** K1 besteht weiter und ist größer geworden:
38 112 m³ statt 24 064 m³; gletscher_03 26 075 m³ bis 57,1 m, fjord_02 2 734 m³ bis 16,7 m, bergwald_06 1 062 m³ bis 12,9 m. K2, K3 und K5 bestehen weiter.
K4 ist dort behoben: Der `auslauf` beginnt auf dem Seespiegel und läuft 101,6 m bis `B_R2_R_P3_P0_01`. Ausgabe:
`export/unreal/welt/sehens_p2_13f/_wip_ff10214/`.

## K1 – Querprofil schneidet bis 30 m seitlich in steile Hänge (FEHLER, neu durch 13f A12)

`rezept.py` (Aufruf von `stempel.bach_profil`, etwa Z. 798) setzt `tiefe_max_m = max(Gelände − Spiegel) + tiefe` über den **ganzen** Bach;
`bach.reichweite` macht daraus R = halbe Breite + min(tiefe_max / tan 35° + 1, 30) m. Die 35°-Böschung ab dem Spiegel senkt dann alles bis R
ab, wo das Gelände steiler als 35° ist oder hoch über dem Spiegel liegt (Fallketten, Schluchten, Kar). Bei d = R endet der Schnitt mit einer
**senkrechten Wand**; an den Linienenden entstehen **gerade Radialkanten** (`innen = 0,01 < sp < L − 0,01`), an Knicken Fächer. Die
Gruben-Rücksetzung greift nicht, weil die Keile hangab offen sind. Gemessen (neu tiefer als alt, > 3 m neben dem Bachrand, außerhalb See + 3 m):

| Ort | Bach (R geschätzt) | Abtrag | größte Tiefe, Lage |
|---|---|---|---|
| gletscher_03 Moränensee | firnrinnsal (≈ 30 m) | 13 938 m³ auf 757 m² | **54,9 m** bei X −1140 / Y −2896, 25 m vom Bachrand; Keil 447 m² mit 50–60 m hoher Wand an der Unterkante, neue Oberfläche 190–205 m statt 255–265 m |
| canyon_04 Flüsterschlucht | spaltbach (≈ 23 m) | 3 491 m³ auf 591 m² | 11,3 m bei X −1248 / Y −840 (Schluchtwände beidseits 2–3 m zurückgeschnitten) |
| elfenwald_05 Farnschlucht | tobelbach (≈ 12 m) | 2 064 m³ auf 463 m² | 9,9 m bei X 2760 / Y −1580 |
| gletscher_06 Gletschertöpfe | klammbach_oben (≈ 15 m) | 1 663 m³ auf 498 m² | 11,4 m bei X −246 / Y −3050; Keil 301 m² bei X −276 / Y −3024 |
| fjord_02 Schleierwand | abfluss1/3/4 (10–12 m) | 1 332 m³ auf 467 m² | 13,1 m bei X −1798 / Y −3070 |
| fjord_04 Hängetal | hochtalbach (≈ 22 m) | 1 059 m³ auf 222 m² | 17,0 m bei X −1670 / Y −2822, 13 m vom Bachrand |
| bergwald_06 Karsee | zulauf_sued (≈ 14 m) | 390 m³ auf 228 m² | 8,2 m bei X −3202 / Y 88 |
| wueste_04 Quelloase | rinnsal | 127 m³ auf 45 m² | 6,7 m bei X −494 / Y −1366 |

**Gegentest (lokal):** gleicher Planer, nur `bach.reichweite` fest auf halbe Breite + 5,4 m. Dann sinkt der Abtrag in gletscher_03 von
68 413 auf 54 945 m³ (alter Stand 54 484 m³), die größte Tiefe von 54,9 auf 46,5 m; in gletscher_06 von 1 618 auf 199 m³. Die Reichweite
ist also die Ursache.
Bilder (alt | neu | Differenz): `docs/pruefung/sehens/p2_13f_delta/<ort>.png`, Übersicht je Biom `<biom>.png`.
**Vorschlag:** außerhalb der Wasserkante höchstens `tiefe + 0,5 m` unter das bisherige Gelände absenken (die Böschung läuft dort in den Hang
aus, statt ihn abzutragen); Ufer ≥ Spiegel + 5 cm nur bis Netzrand + 1,5 m erzwingen; R aus der örtlichen Eintiefung je Probe statt aus dem
Maximum des Bachs; an Enden und Knicken die Endkappe einbeziehen und zum Rand hin weich auslaufen lassen (keine senkrechte Wand bei R); in
Fallstrecken (Spiegel folgt der Hülle) keinen Profil-Einschnitt. Prüferregel wie in 15e: |Δ| > 0,3 m nur innerhalb Netzrand + Uferring
(+ Wandzone der Rezepte), sonst FEHLER.

## K2 – Pivot in der Netzmitte: Pflanze steckt halb im Boden (FEHLER, neu durch 13f A3)

`instanzen.platziere`, `bezug: mitte`, Fuß ≥ 1,5 m: `z = Boden(Pivot) − eingraben − max(0, bmin_z·sz)` setzt bei bmin_z < 0 den Pivot auf den Boden.
`SM_Fern_02a` (bmin_z −25,8 cm bei 52,4 cm Höhe): **dschungel 225 + wueste 3** Instanzen stecken im Median **54 %** ihrer Höhe im Boden (219 über
40 %); im alten Stand 0 %. Vorschlag: wenn `bmin_z·sz < −0,25 · Höhe·sz`, dann `z = Boden(Pivot) − eingraben − bmin_z·sz` (Netz-Unterkante auf den
Boden). Lokal mit dieser Regel getestet: Median 23 % (Rest = Hangneigung + Eingraben). Für Netze mit Pivot unten ist das Ergebnis identisch.

## K3 – Ein Stück genau auf der Feldgrenze im falschen Plan (FEHLER, A10-Rest)

dschungel G6, `SM_petasites_spurius_01__Riesenblatt`: y = 979,50 m liegt genau auf der Grenze G5/G6. Gespeichert als float32 = 97 949,992 cm →
der Setzer ordnet es G5 zu (euer Prüfer meldet es: „1 Instanzen/Akteure außerhalb des Feldrechtecks“). Vorschlag: Feld aus dem
float32-gerundeten Wert bestimmen oder Stücke auf der Grenze 1 cm ins Feld schieben.

## K4 – heide_06 `auslauf` beginnt 1,48 m über dem Seespiegel (FEHLER, A9/A13)

Ziel `B_R2_R_P3_P0_01`. Der Planer meldet selbst „Mündung nicht erreichbar (Spiegel über dem Lauf)“ und „Zielgewässer liegt 1,48 m über dem
Seespiegel“, behält das Ziel aber und hebt den ganzen Auslauf auf dessen Spiegel. Folge: Abfluss beginnt 1,48 m über `gumpe`, Ufer unter dem
Spiegel auf 11 von 11 m (bis 1,50 m, euer Prüfer) bzw. 19 von 21 m (unser Prüfer). Laut eurer Antwort endete er auf 2 m `versickert` (48 m).
Vorschlag: unerreichbares Ziel verwerfen (Tiefenlinie bzw. `versickert` ≥ 25 m) und für Abflüsse nie einen Spiegel über W0 zulassen.
Das beantwortet auch eure Rückfrage 5.

## K5 – Becken zwischen Stufen kürzer als 3 m (WARNUNG, A8)

Auf 1 m belegt jede Stufe 1,0 m (Lippe → Fuß, statt 0,5 m); das Becken danach ist nur 2,5 m lang (Abstand 3,5 m). 168 von 246 Becken sind
< 3 m, 127 davon < 2,5 m (canyon_04 `spaltbach` 23 von 34 Becken mit 2,5 m, gletscher_05 `muehlenbach` 16 von 16, tundra_04 `schmelzfaden` 37 von 42). Dazu Becken von 0 m bzw. 1,5 m
vor der Schluss-Stufe am See (bergwald_06 `zulauf_west`, `zulauf_sued`: W_ende-Stufe direkt hinter einem Kettenfall). Vorschlag: die Beckenlänge
ab dem tatsächlichen Fuß rechnen (Fenster `j`/`jb` ab `s[kf]`) und die Schluss-Stufe nur setzen, wenn davor ≥ 3 m Becken bleiben; sonst geht
sie im Kettenfall auf. Gestaltung (Lage, Höhe, Zahl der Stufen) bleibt wie in 13f (Ferat 23:20) – nur die Mindestlänge stimmt nicht.

## K6 – Geänderte Zellen ohne Bodenlage (WARNUNG, Regel aus 15e)

18 065 von 287 584 Zellen mit |Δ| > 0,3 m haben keine Lage (bleiben bei der alten Landschaftslage): canyon_03 2 782 (bis 5,3 m),
gletscher_03 1 674 (bis 53,9 m, der K1-Keil), frost_03 1 524 (8,9 m), tundra_03 1 375 (6,0 m), aue_03 960, kueste_02 946 (14,2 m), lava_01 761,
kueste_06 750 (29,5 m), lava_07 705, wueste_05 685. Vorschlag: Lagen über das ganze Delta-Gebiet (an Abbrüchen Fels/Geröll), Prüferregel aus 15e.

## K7 – Harte Lagenkanten (WARNUNG, A11-Rest)

Sprünge > 160 von 255 zwischen Nachbarzellen in 225 Lagen-Dateien (alt 288; ≥ 200: 144 → 83). Erde 97 – meist das Pfadband mit 1-m-Übergang
(so in 13f vorgesehen). Der Rest ist Kies 25, Moos 22, Fels 19, Schlamm 11, Sand 10, Geröll 10, Schnee 6 – bitte auch bei „fleckig“ und kleinen
Ringen Ränder ≥ 3 m.

## K8 – Seeufer unter dem Spiegel, weiter unverändert (WARNUNG)

Gemessen 1 m außerhalb des Umrisses, alle 0,5 m:
- dschungel_05 `lagune`: bis −1,02 m bei X 1913 / Y 1394 und −0,30 m bei X 1961 / Y 1409. Der Spiegel 19,00 m liegt 8,5 m über dem alten
  Gelände (10,5 m); nur der Rand hält das Wasser.
- tundra_05 `trunkensee`: −0,05…−0,15 m auf ~5 m bei X −1331 / Y −2443 (Auslassnähe?).

Euer Prüfer misst auf dem Umriss und findet beides nicht.

## K9 – Rezepte (Hinweise, alle schon im alten Stand)

- gletscher_03 Karbank (`terrasse`, ziel_z 190 m auf einem 45–56°-Hang): Der Abtrag erreicht schon ohne K1 46,5 m (alter Stand 43,0 m).
  Die Begründung im Rezept nennt „bis ~18 m“. Bitte begrenzen oder die Bank kleiner bzw. tiefer ansetzen.
- canyon_03 Rote Stufe: Terrassenband bis 142 m vom Mittelpunkt (R 90 m), 2 896 m², bis +4,3 m (X −1847 / Y −597) – gewollt?
- gletscher_05 Wächte: gerades Band 161 m entlang einer Weltachse (konstantes Y), +3 m, 2 427 m², Füllgrad 0,90 (X −610 / Y −3177) – wirkt künstlich.
- Weitere geometrische Grundformen mit harten Rändern: kueste_06 Kreidewand (achsparallele Stadionform −29,5 m), kueste_02 Ellipse +17,2 m,
  kueste_07 Balken entlang X, gletscher_01/04/08 Balken bzw. Halbring, lava_05 Spalte mit geraden Wänden 59/53 m. Bei Gelegenheit organischer machen.
- bergwald_06: Kamera `_nah` steht im See (euer Prüfer). Der Spiegel ist neu 253,70 m statt 256,17 m.
- frost_01 Materialwunsch `MI_EL_SW_Schwarzeis`: `fuer` enthält „Frostblumen-Lagune“; das ist kein Netzname.
- gletscher_01 `gletscherbach`: die Furtstrecke folgt dem Gelände mit 57 % Gefälle (Wasserfilm über den Weg am Steilhang); elfenwald_04 `zulauf` 9 %.
- Fallketten bis 25 m stehen als `stufen` im Bach (gletscher_03 `firnrinnsal` 25/25/24 m, gletscher_06 `klammbach_oben` 25 m, fjord_02 `abfluss4`
  20,4 m, bergwald_06 `zulauf_sued` 17,1 m, fjord_04 `hochtalbach` 16,9 m). Unser bisheriger Einbau macht daraus senkrechte Vorhänge über
  5–17 m lange Kaskaden, von denen nur 1–3 von 9 Spalten das Becken erreichen. Das erledigt das Format aus 13g (Kaskadennetz).

## K10 – Kleine Querprofil-Reste (FEHLER auf 1 m laut eurem Prüfer)

gletscher_06 `klammbach_oben` Ufer unter dem Spiegel 1 von 26 m (bis 0,15 m, wie in eurer synthetischen Welt), dschungel_02 `quellbach`
Gelände über dem Spiegel 1 von 37 m (0,03 m), wueste_04 `rinnsal` Ufer 1 von 18 m (0,02 m; unser Prüfer bei halber Breite + 1 m: 7 von 25 m).

## Nur zur Kenntnis (lokal, kein Planer-Punkt)

Unser Einbau-Prüfer kennt `furten`, `muendung_offen_ab_cm`, `muendung_art: houdini` und `z_frei_index` noch nicht. Seine Schutzzone misst
mit Schachbrett-Abstand (Diagonale 4,2 m), den Spiegel eines Bestandsbachs nimmt er vom nächsten Stützpunkt. Daher kommen 6 seiner 11 FEHLER:
dschungel_02 „kreuzt Weg“ (Furt ist da), aue_02/aue_04/tundra_08 (Zellen 4,0–4,2 m entfernt, |Δ| ≤ 7 cm), tundra_04 Schutzzone
(Mündungskorridor: Bett im Bestandsbach bis 0,5 m tiefer, nach eurer Regel erlaubt) und tundra_04 „Bachende 0,28 m unter“ (Stützpunkt
statt Segment; an der Linie gemessen liegt das Ende 2 cm über dem Spiegel). Dazu 84 Schwebe-Warnungen an hängenden Pflanzen. Wir passen das lokal an. `ue_sehens_material.py` liest nur die Wünsche je Ort; die Brücke
übernimmt dafür jetzt `materialwuensche_biom`.
