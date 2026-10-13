# Antwort 16h Nachtrag 6f – Bettplan eingebaut: Werkzeug, Überlauf 85 %, Lagen je Zone, Beckenfarbe, Blöcke

Stand 13.10.2026. Bezug: `auftraege/16h-nachtrag6f-bettplan-eingebaut.md` (Ferat 893c194), Bilder `bilder/swr_p2/bettplan_p2c_vorher_nachher.jpg`,
`bettplan_p2c_oben.jpg`, `bettplan_delta_welt.png`, lokale Lagen-Annahme `fluss_sim/p2_lokal/p2_bett_lagen_regeln_lokal.json`, unsere Antworten
6b, 6c, 6d, 6e und N6.

**Kennzeichnung:**
- [Ferat]: eure Messung bzw. euer Bild
- [Plan]: im Bettplan gerechnet
- [UE-API]: Namen aus der Engine-Schnittstelle, aus dem Gedächtnis, in 5.8 zu prüfen
- [Ableitung] / [Annahme]: von uns geschlossen bzw. als Gestaltungswert gesetzt

## Kurzfazit

1. **Werkzeug:** Der `TypeError` kam aus dem **alten Stand bd593e8**. Euer Fall ist nachgestellt: parallele Listen `i`, `j`, `s`, `sohle`, `spiegel`, `tiefe`, `breite`, 790 Punkte.
   - bd593e8 bricht ab mit „'float' object is not subscriptable“. Seit 09bf669 wird die Liste gelesen.
   - Neu: Das Objekt mit `i`/`j` wird auch verschachtelt gefunden (bis Tiefe 2). Der Selbsttest prüft genau eure Struktur, oben und verschachtelt: OK, byte-gleich.
   - Euer Adapter `p2_bett_einbau.py` ist der richtige Weg. Unser Format bleibt.
2. **Überlauf 85 %:** Eure Ursache stimmt. 54 Spline-Punkte (~3,5 m) verschmieren jede Stufe.
   - Spline-Punkte je 1 m sind richtig. Besser sind die neuen **`spline_stufenpunkte`**: je Lippe ein Punkt auf der Lippe (Spiegel oben) und einer am Fuß der Stufenwand (Spiegel unten), sonst je 1 m. Das sind 237 Punkte in s 389–580.
   - Punkttyp **linear**, damit die Kurve zwischen Lippe und Fuß nicht überschwingt [UE-API: `ESplinePointType::Linear`; Wirkung auf die SWR = Ableitung].
   - „Spline einen Tick höher“: **nein**, erst nach der Messung und nur, wenn das Bett nicht voll nass ist.
   - Bleibt das Band über 5 %: zuerst Punkte und Spiegel prüfen, dann die Schulter an den Lippen anheben, dann das Band schmaler machen. `remove_outside` 50 kommt zuletzt (Reihenfolge in §2).
   - Euer zweiter Fund ist festgehalten: Nach einem Bake simuliert ein Reset ohne LIVE_SIM nicht.
3. **Problem A, Lagen je Zone:** Tabelle §3, in `p2_bett_regeln.json` → `lagen_je_zone_6f`.
   - Fels nur noch an Lippenkrone und Stufenwand, dort höchstens 30 %.
   - Böschung: Erde, Geröll, Trockengras und Moos.
   - Das Bett wird kiesig mit Algen statt 30 % Fels.
   - Die schwarzen Wände kommen vermutlich auch vom Bach-Ton der Landschaft. Prüfhinweis in §3.
4. **Problem B, Tiefe und Farbe:**
   - p90 0,72 m über alle Bettzellen ist **kein Kolkmaß**. Im Plan selbst liegt p90 bei 0,55 m und der Median bei 0,21 m. Die Kolke sind nur ein kleiner Teil der Bettfläche.
   - Richtig gemessen wird die **tiefste Stelle je Hauptbecken**: im Plan 0,84–1,20 m, Median 1,03 m. Nach dem Spline-Fix so neu messen.
   - **Farbe, entschieden:** eine Kind-Instanz **`MI_EL_SWR_Bergbach`** mit Absorption (160; 650; 850) cm, sonst E16. Ein 1-m-Kolk wird damit etwa 25 % dunkler als der Auslauf, mit F nur etwa 19 %.
5. **Problem C, Blöcke:**
   - **Neue Größenregel** nach Bachbreite B und Fall D:
     - Keystone = clamp(min(0,7 D + 0,3; 0,22 B + 0,2); 0,5; 1,1)
     - Lippenblock = 0,65 × Keystone
     - Eckblock = clamp(0,18 B + 0,35 D + 0,2; 0,6; 1,3)
   - Größte Blöcke jetzt 1,3 m statt 1,79 m; Median 0,76 statt 1,0; 0 statt 13 Blöcke ≥ 1,5 m.
   - **Liste der Netze ohne Nasslinie** mit MI-Vorschlag in §5, auch als `material_vorschlag` im Plan.
   - Das helle `mountain_rock_small` kommt nicht mehr an Lippen.
   - Plan neu: 0 FEHLER, 3 WARNUNGEN (unverändert), zwei Läufe byte-gleich. Das **Gelände ist unverändert** (`talkaskade_soll.f32` gleicher Hash f274fd1b66d7). Neu setzen müsst ihr nur Blöcke und Instanzen.

## 1. Werkzeug

- **Nachstellung** [Plan], Probe mit eurer Struktur (`i`, `j`, `s` mit 790 Punkten bis 788,37; `sohle`, `spiegel`, `tiefe`, `breite`; `marken_s_m`):
  - bd593e8 (6c): `TypeError: 'float' object is not subscriptable`. Diese Fassung nahm die erste Liste als Punktliste.
  - 09bf669 (6e): liest richtig, 790 Punkte, Raster, s bis 788,37.
- **Jetzt:** Die Suche nach dem Objekt mit parallelen `i`/`j`-Listen reicht bis Tiefe 2, also auch `{"lauf": ..., "daten": {i, j, ...}}`. Der Selbsttest liest beide Formen.
- **`a15_einbau.py` gegen euren Adapter:** `a15_einbau` erwartet einen Gefälle-Plan mit `wasser_koerper` (Kaskadennetz). Die p2-Talkaskade hat bewusst keinen, denn ihr Wasser ist die SWR.
  - Euer Adapter (Gelände im sehens_einbau-Format, Instanzen nach FORMAT §3, Spline-Z, Prüfband) ist deshalb der passende Weg. An unserem Format ändern wir nichts.
  - Neu im Plan, bitte im Adapter übernehmen:
    - `spline_stufenpunkte` (auch in `spline_spiegel.json` → `stufenpunkte`)
    - `material_vorschlag` je Datei
    - `z_absolut` für Kantengras und Totholz (6e)

## 2. Überlauf 85 % und Spline

**Ursache** [Ferat]:
- Die SWR füllt zur Spline-Höhe. Mit Punkten alle ~3,5 m liegt die Spline zwischen Lippe und Kolk bis 0,9 m über dem Plan-Spiegel.
- Beispiel: s 398 Soll 98,81 m, Spline 99,72 m. Das passt zum Bild: Das Gelände hält (0,5 m hinter der Kante +0,21 m), das Wasser steht zu hoch.

**Spline-Punkte:**
- **1-m-Punkte aus `spline_z.json` sind richtig.** Sie treffen jede Stufe aber nur auf ±0,5 m.
  - Eine Stufe von 2 m Fall wird dann über einen Meter geneigt. Ein Kurvenpunkt kann davor bzw. dahinter überschwingen [Ableitung].
- **Empfohlen:** `bettplan_p2.json` → `spline_stufenpunkte` (237 Punkte, in `spline_spiegel.json` als `stufenpunkte` mit Weltlage):
  - Auf jeder Lippe auf u = 0 ein Punkt 2 cm davor mit dem Spiegel oben.
  - Am Fuß der Stufenwand 2 cm dahinter ein Punkt mit dem Spiegel unten.
  - Dazwischen je 1 m, kein Punkt näher als 0,25 m an einem anderen.
- **Punkttyp:**
  - USplineComponent kennt die Typen `Linear`, `Curve`, `Constant`, `CurveClamped` und `CurveCustomTangent` [UE-API]. Für s 389–580 alle Punkte auf **`Linear`** stellen.
  - `Curve` (Auto-Tangenten) kann an Sprüngen überschwingen [Ableitung]. `Constant` ergäbe senkrechte Sprünge auch in der Breite; das brauchen wir nicht.
  - Ob die Water-Body-Spline der SWR den Punkttyp beim Füllen beachtet, ist nicht belegt. Nach dem Setzen vergleichen: Spline-Z an den Lippen ±3 cm zum Plan.
- **„Spline einen Tick höher“:** **nein**, das füllt das Band wieder.
  - Erst wenn nach dem Fix das Bett unter 99 % nass ist oder die Front vor 788 m stehen bleibt: +2 cm.
  - Danach Band und Kolke erneut messen.

**Reihenfolge, falls das Band nach dem Fix weiter über 5 % nass ist** (je Schritt messen: Band ≤ 5 %, Bett ≥ 99 %, Front 788 m, Kolk-Maximum je Hauptbecken Median ≥ 0,8 m):
1. **Spline prüfen:** Abweichung Spline gegen Plan an Lippen und Füßen ≤ 3 cm. Prüfband nach Zonen auswerten: Liegt die Nässe an den Stufenwänden schräger Lippen?
2. **Örtlich:** Wenn ja, die Schulter neben den Lippen anheben (+0,15 m über 1 m Länge; das kann ich als Regel ergänzen). Das ist besser als eine globale Änderung.
3. **Band schmaler:** Bett + 1 m statt Bett + 2 m, nur wenn die Front weiter 788 m erreicht. F2 lehrt: Ein schmales Band kann die Front stoppen.
4. **`remove_outside` 50 (F1):** zuletzt. Der Überlauf sank damals um 38 %, aber das Bett wurde 15 % flacher, und genau das kostet Kolktiefe.

**Euer zweiter Fund** [Ferat]: Nach einem Bake steht die Darstellung auf WCBS. Ein Reset ohne LIVE_SIM simuliert nicht. Danke, das steht jetzt in eurem Reset-Werkzeug fest.

## 3. Problem A – Lagen je Zone (ersetzt die lokale Annahme)

Zonen aus `talkaskade_zonen.u8`. Prozentwerte, je Zelle auf 100 normiert; das Gewicht wie in eurer lokalen Datei.

| Zone | Mischung | Gewicht | gegenüber lokal |
|---|---|---|---|
| 1 Bett | Kies 35, Geröll 30, Algen 15, Schlamm 10, Felsplatte 10 | 1 | Fels 30 → 0; Algen und Schlamm dazu |
| 2 Kolk | Kies 25, Schlamm 25, Geröll 20, Algen 20, Felsplatte 10 | 1 | Fels 10 → 0 |
| 3 Lippenkrone | Geröll 40, Fels 25, Algen 20, Kies 15 | 1 | Fels 55 → 25 |
| 4 Stufenwand/Rampe | Geröll 40, Fels 30, Algen 15, Moos 15 | 1 | Fels 60 + Felsplatte 25 → Fels 30 |
| 5 Uferstufe | Erde 35, Moos 25, Geröll 20, Schlamm 10, Kies 10 | 1 | ähnlich, mehr Erde und Moos |
| 6 Schulter | Trockengras 35, Moos 20, Gras 15, Erde 15, Geröll 15 | fest 0,6 | Gras dazu |
| 7 Böschung | Erde 30, Trockengras 25, Geröll 20, Moos 15, Kies 10 | delta (voll bei 0,5 m) | wie lokal, kein Fels |
| 7 Böschung > 40° | Erde 40, Geröll 35, Moos 25 (Erdanriss wie `C_ufer` steil) | delta | neu |

- **Regeln:**
  - Zonen 1–5 ohne Graslagen (6b).
  - Fels nur in Zone 3 und 4 und höchstens 30 %. Die Stufe bilden dort die Blöcke, die Lage gibt nur Fels-Reste.
- **Warum die Wände schwarz sind** [Ableitung, bitte prüfen]:
  1. Fels und Felsplatte zu 85 % auf den Stufenwänden.
  2. **Der Bach-Ton der Landschaft** (`Ufer_Farbe_Bach` (0,20; 0,14; 0,09), Nässe-Band 50 cm). Er hängt am 2-m-Raster von `T_Eldarien_Bachgewicht_2m` bzw. dem Spiegel-Raster.
     - Im Einschnitt (Böschung bis 2,6 m hoch) kann eine 2-m-Zelle Bett und Wand zugleich treffen. Dann wird die ganze Wand braun-dunkel getönt.
     - **Prüfung:** Gelände-Z minus Spiegel-Textur an den dunklen Wänden. Liegt die Wand > 0,5 m über dem Spiegel und ist trotzdem dunkel, wirkt der Bach-Ton zu weit.
     - Abhilfe: Nässe und Ton zusätzlich über die Höhe begrenzen (h > 0,5 m → 0, wie im Material schon für das Nässe-Band). Das ist ein Knoten im V18-Zweig.

## 4. Problem B – Tiefe und Beckenfarbe

**Tiefe** [Plan]:

| Maß | Plan | eure Messung |
|---|---|---|
| alle Bettzellen, Median | 0,21 m | 0,40 m |
| alle Bettzellen, p90 | 0,55 m | 0,72 m |
| tiefste Stelle je Hauptbecken (min / Median / max) | 0,84 / 1,03 / 1,20 m | – |

- Ihr messt mehr Wasser als der Plan. Das passt zur zu hohen Spline: Die SWR steht bis 0,9 m zu hoch.
- Die Ziele 0,8–1,2 m gelten für das **Kolk-Maximum je Hauptbecken**. Nach dem Spline-Fix bitte so messen:
  - je Hauptbecken die tiefste Zelle innerhalb der Kolk-Ellipse aus `becken[].kolk` (s, u, Länge, Breite)
  - Erwartung: Median ≈ 1,0 m; Bettzellen gesamt Median ≈ 0,2–0,3 m

**Farbe, Entscheidung: Kind-Instanz `MI_EL_SWR_Bergbach`** (Eltern `MI_EL_SWR_Klar`, E16):

| Parameter | F (heute) | Bergbach |
|---|---|---|
| Absorption (Sichtweite cm, R/G/B) | 222 / 1000 / 1250 | **160 / 650 / 850** |
| alles andere | E16 | gleich |

- **Rechnung** [Ableitung, Lichtweg ≈ 2 × Tiefe beim Blick schräg nach unten]:

  | Variante | Y bei 0,3 m (Auslauf) | Y bei 1,0 m (Kolk) | Kolk gegen Auslauf |
  |---|---|---|---|
  | F | 0,91 | 0,74 | −19 % |
  | Bergbach | 0,87 | 0,64 | **−26 %** |

  Der Kolk wird damit lesbar dunkel und leicht grünlich-blau. Der flache Auslauf ändert sich wenig (−5 %).
- Klarer bleiben die Becken nicht durch die Absorption, sondern durch den dunklen Grund (S6) und eine ruhige Oberfläche (V20a).
- **Prüfung:** an `C2_tk_becken_auge` Y(Kolk) / Y(Ufer-Gras) ≤ 0,6 (K3) und Y(Auslauf) / Y(Ufer) ≥ 0,8. Wird der Auslauf zu dunkel, Rot 160 → 190.
- Die Instanz nur auf die p2-SWR legen. Andere Bäche bleiben bei F, bis ihr sie anseht.

## 5. Problem C – Blöcke

**Größe** (Regel `bloecke.groesse_6f`):
- **Grundlage:** Stufenhöhe ≈ Blockgröße [RC2021]; Klemmverhältnis Bachbreite/Block ≈ 3–6 [CZ2007]. Bei B = 4 m liegt der größte Block also bei ≈ 1 m, nicht bei 1,8 m.
- **Formeln:**
  - Keystone = clamp(min(0,7 D + 0,3; 0,22 B + 0,2); 0,5; 1,1)
  - Lippenblock = clamp(0,65 × Keystone; 0,35; 0,8) ± 25 %
  - Eckblock = clamp(0,18 B + 0,35 D + 0,2; 0,6; 1,3) ± 15 %
  - Randblock 0,4–0,9 m, Beckenblock 0,4–0,8 m
- **Vergleich mit dem gebauten Stand** (bd593e8):

  | | gebaut | neu |
  |---|---|---|
  | Median | 1,0 m | 0,76 m |
  | p90 | 1,42 m | 1,23 m |
  | Maximum | 1,79 m | 1,30 m |
  | Blöcke ≥ 1,5 m | 13 | 0 |

- **Neuer Planstand:** 1 449 Instanzen. Darin enthalten sind 6e-Bewuchs und Totholz, 155 mit Kollision, 5 SWR-Hindernisse.

**Netze ohne eigene MI / ohne Nasslinie** (im Plan je Datei `paket_mi` und `material_vorschlag`):

| Netz | Paket-MI | Anzahl (neu) | Vorschlag | Vorrang |
|---|---|---|---|---|
| `SM_mountain_rock_big_01_1`, `_01_5` | `MI_mountain_rocks_big_01` | 83 | `MI_EL_NL_mountain_rocks_big_01` auf **`M_EL_Mountain_NL`** (= `M_Master_material` + `MF_EL_Nasslinie` + `MF_EL_Spiegelhoehe`) | 1 (viele, an Lippen) |
| `SM_ground_rock_02` | `MI_rocks_atlas_01` | 26 | `MI_EL_NL_rocks_atlas_01` auf `M_EL_Mountain_NL` | 1 |
| `SM_mountain_rock_big_02_*` (gebaut, im neuen Plan nicht mehr) | `MI_mountain_rocks_atlas_01` | 0 | `MI_EL_NL_mountain_rocks_atlas_01` | 3 |
| `SM_mountain_rock_small_01_*` | `MI_mountain_rocks_small_01` | nur noch Bachdekor | `MI_EL_NL_mountain_rocks_small_01` (`Nass_Albedo` 0,35, 6d); bis dahin nicht an Lippen | 2 |
| `skjsL_tier_0` | `MI_skjsL` (Fab) | 40 | `MI_EL_skjsL` auf **`M_EL_Fels_MS2`** mit den Fab-Texturen; Kanalbelegung (AO/Rauheit/Höhe) prüfen | 2 |
| `texndcpda_tier_0` | `MI_texndcpda` (Fab) | 8 | `MI_EL_texndcpda` auf `M_EL_Fels_MS2` | 3 (nur Lippe, flach) |
| `SM_LichenedForestBoulder_01` | Megascans-Paket-MI | 28 | `MI_EL_LichenedForestBoulder_01` auf MS2 | 2 |
| `SM_MossyForestRock_02` | Megascans-Paket-MI | 23 | `MI_EL_MossyForestRock_02` auf MS2 | 2 |
| `SM_MossyForestBoulder_01/02/06/07` | Megascans-Paket-MI | 129 | **vorhandene** `MI_EL_*` der Bachdekor-Steine (MS2) im Setzer zuweisen | 1 |

- **Ergebnis der Prüfung:** 11 Netze; mit den `_kol`-Varianten sind es 21 Dateien. Das passt zu euren „20 Netztypen“.
- **Kosten:** Eine Kopie von `M_Master_material` mit Nasslinie kostet wie MS2 etwa +27 Anweisungen und 1 Sampler (euer Wert 336 → 363). Die vier `MI_EL_NL_*` sind dann reine Kind-Instanzen.

## Was fehlt bis Witcher 4 (Talkaskade nach dem Einbau)

Messlatte und Quellen wie in 6e: dichte Vegetation bis an die Kante, Wind, weiches Licht, klare Wasserformen. Die Techdemo ist nur über Suchauszüge belegt.

Nach Wirkung, Stand nach euren Bildern:
1. **Wasser im Bett halten** (Spline-Stufenpunkte, linear). Ohne das liegt ein grauer Film über allem; jeder andere Punkt wirkt erst danach.
2. **Wände entdunkeln** (Lagen je Zone §3, Bach-Ton nach Höhe begrenzen). Im Bild das Auffälligste nach dem Wasser.
3. **Blöcke im Maßstab** (neue Größenregel) und **nass** (Nasslinie für Mountain, MI-Liste §5).
4. **Bewuchs an der Kante** (6e: 279 Kantengras, 432 Moos, 65 Farne). Er ist noch nicht gebaut. Die Böschungen lesen sich heute als nackte Gräben; Witcher-4-Bilder zeigen Bewuchs bis ans Wasser.
5. **Becken lesbar dunkel** (`MI_EL_SWR_Bergbach`, Kolk-Maß je Hauptbecken) und **ruhige Oberfläche** (V20a).
6. **Totholz** (5) und Fall-Effekte (6b).
7. **Licht im Einschnitt:** Distance Fields der neuen Netze, Prüfwert K3.

## Rückfragen

1. Welche `MI_EL_*`-Namen haben die Bachdekor-Instanzen von `SM_MossyForestBoulder_*`? Dann schreibe ich sie direkt als `material_vorschlag` in den Plan.
2. Kann die Water-Body-Spline der SWR den Punkttyp `Linear` je Punkt? Falls die SWR nur Auto-Tangenten kennt, reichen die Stufenpunkte allein, nur mit etwas Restschwingen.
