# fluss_sim – Exporter für Shallow Water River (Entscheidung 16, Format v3)

**Gültigkeitshinweis 15.10.2026:** Die folgenden Abschnitte dokumentieren Exportformat
und frühere Regeln, keine durchgehend bestätigten Engine-Funktionen. Die Annahme,
mehrere SWR auf demselben Quellfluss bekämen automatisch getrennte Rechenflächen, ist
laut [lokalem Befund 16h/6i §3](../../../auftraege/16h-nachtrag6i-baked-sim-tests-stand.md)
für den dort geprüften Build nicht erfüllt: die Fläche wird aus den Quell-Wasserkörpern
berechnet. Die anschließende Teilung mit Flusskopien wurde wegen Stillstand/trockener
Nähte [in 6j §1 verworfen](../../../auftraege/16h-nachtrag6j-teilung-ergebnis.md).
Teilungspläne unten deshalb nicht als freigegebene Spiellösung anwenden. Vor Anwendung
den aktuellen lokalen Stand und die wirklichen Bounds prüfen; Exporter/Regeldateien
wurden durch diesen Dokumentationshinweis nicht geändert.
Übergabe und Abnahme: [Recherche-README](../../../README.md).

Ferat hat am 12.10.2026 entschieden: Alle Bäche und Flüsse laufen mit `WaterBodyRiver` + `ShallowWaterRiver`
(UE 5.8.3, Plugins Water + Niagara Fluids); die Simulation wird im Editor **gebacken**; Seen bleiben `WaterBodyLake`
([`../../16-shallow-water-alle-gewaesser.md`](../../16-shallow-water-alle-gewaesser.md)).

**Format v3 (16c, `fluss_sim_v3`):**
- **Je Gewässer genau EIN `WaterBodyRiver`** von der Quelle bis zur Mündung (See, Fluss/Bach, Meer), über alle Fälle und
  Feldgrenzen hinweg. Keine Flussabschnitte mehr; die Simulation füllt Becken und überströmt Lippen selbst.
- **Je Gewässer EINE `ShallowWaterRiver`** (Nachtrag 17:45): Der SWR-Bereich ist das achsparallele Rechteck um den Fluss,
  `resolution_max_axis` = längste Rechteckseite / Zielzelle (Bach 0,25 m, Fluss 0,35 m), höchstens 2048. Nur wenn die
  Zelle dann über 0,30 m (Bach) bzw. 0,35 m (Fluss) läge, wird die **Simulation** in wenige lange Stücke geteilt
  (kleinste Rechteckfläche, nicht an Fällen); alle Stücke nennen denselben Fluss.
- Fälle (Vorhang, Niagara, Schaumobjekte) und Wasser-Kollision (`WH_…`) wie 16/16a; Vorhänge **warten** vorerst.

**Ergänzungen 16d** (Regeln Version 4, Format bleibt `fluss_sim_v3`, nur neue Felder bzw. Werte):
- **Eingaben:** nur echte Lauf-Pläne (`<lauf>/plan.json` mit `wasser_koerper`); Archivordner (Name mit „.“ oder führendem
  „_“) und andere Pläne (Feld-Instanzplan `gefaelle/C2/plan.json` von `a15_einbau.py`) werden übersprungen und genannt.
- **Gebaute Läufe:** Ihr Gelände-Delta wird nicht noch einmal addiert (`--gebaut`, `sehens_einbau/A15_<lauf>/lauf.json`).
- **Töpfe:** Kleine Sehens-Seen (< 30 m) an Sehens-Bächen sind Teil des Gewässers (Bereich `topf`, kein `WaterBodyLake`);
  eine Treppe wie die Elfentreppe ist **ein** Gewässer mit **einer** SWR.
- **Vorschläge:** Für offene Enden und Lücken stehen Vorschlagspunkte in `muendung.vorschlag` und `vorschlaege.json`,
  getrennt von der Spline.

**Ergänzungen 16e** (Regeln Version 5, Format bleibt `fluss_sim_v3`; Antwort
[`../../16e-ferat-schaum-weg-langsamer.md`](../../16e-ferat-schaum-weg-langsamer.md)):
- **Tempo nach Gefälle:** `water_body.spline.tempo_ms` je Punkt (m/s) nach Manning-Strickler aus dem Spiegelgefälle,
  `WaterVelocityScalar_cm_s` = `tempo_ms` × 100. Flache Becken 0,1–0,3 m/s, steile Rinnen 1,5–2,5 m/s, geglättet;
  globaler Regler `regeln.tempo.tempo_faktor`. Ersetzt das feste Rollen-Tempo des Plans (Becken 0,8, Lippe 2,4, Rampe 3 m/s).
- **Schaum-Maske (Option B):** `schaum_maske.kapseln` je Gewässer, eine Kapsel je Vorhang-Fall (Aufprall bis Ende
  des Aufprallteppichs, Radius, Stärke). Im Material: Simulationsschaum nur innerhalb der Kapseln.
- **Bäche ungeteilt bis 0,40 m Zelle** (`swr.zelle_max_bach_ungeteilt_m`); Teilstücke behalten höchstens 0,30 m.

**Ergänzungen 16c Nachtrag 3** (Regeln Version 6, Format bleibt `fluss_sim_v3`; Antwort: Nachtrag 3 in
[`../../16c-ferat-ein-fluss-je-gewaesser.md`](../../16c-ferat-ein-fluss-je-gewaesser.md)):
- **`holz_muster`** um `branch` und `mossytree` erweitert: Äste und Moosbäume (`SM_OldTreeBranch_*`,
  `SM_BrokenTreeBranch_*`, `SM_Pine_broken_branch_*`, `SM_mountain_branch_*`, `SM_detail_branches_*`, `SM_MossyTree_01`)
  laufen als `holz` statt `sonstiges`.
- **Feldgrenzen mit zwei Gefälle-Plänen:** Haben beide Teile einer Überlappung einen Plan mit `feldgrenzen`
  (`gefaelle_daten.feldgrenzen`), schneidet der Export die Kette an der Besitzgrenze `grenze_s_m` (die Lippe gehört dem
  Plan ihres Felds, im selben Feld dem oberen). Damit entfällt keine Stufe mehr (`abstuerze_entfallen` leer). Ohne
  `feldgrenzen` gilt die alte Regel (das untere Teil wird gekürzt).
- **Roh-Lauf-Ebene** (`gefaelle/bachbett_roh.py`, Option `--roh DIR`, Standard `bachbett_roh` neben `--gefaelle`): Der
  Export liest `<roh>/<lauf>/instanzen/<Feld>/plan.json` in den Objekt-Pool (Felsen und großes Totholz der Läufe ohne
  Stufenplan → Wasser-Kollision, überspannende Stämme ohne). Der Prüfer nimmt `--roh` ebenso. `zusammenfassung.json`
  nennt die Ebene unter `eingaben.bachbett_roh`.

**Ergänzungen 16c Nachtrag 4** (Regeln Version 7, Format bleibt `fluss_sim_v3`; Antwort: Nachtrag 4 in
[`../../16c-ferat-ein-fluss-je-gewaesser.md`](../../16c-ferat-ein-fluss-je-gewaesser.md)):
- **Grenzen der Hindernis-Akteure** (`swr.hindernis_grenzen`): höchstens `instanzen_je_komponente_max` = 4 000
  Instanzen je Komponente. Hat ein Netz in einer Kachel mehr, teilt der Export es auf weitere Komponenten desselben Netzes
  (`teil`, `teile`; Funktion `hindernis_komponenten`). Je Netz bleibt es sonst eine HISM-Komponente (16a d2).
- **Prüfer:** FEHLER über 4 000 Instanzen je Komponente, über `komponenten_max` = 128 Komponenten je Akteur, bei
  `n_komponenten` ≠ Liste und bei geteilten Netzen ohne Teil-Nummern 1 … n. HINWEIS mit den größten Werten
  (größte Komponente, meiste Komponenten, größter Akteur) und mit der Zahl der Akteure über dem Richtwert
  `komponenten_richtwert` = 16.

**Ergänzungen 16f Rückfrage** (Regeln Version 8, Format bleibt `fluss_sim_v3`; Antwort
[`../../16f-rueckfrage-epic-parameter-lokal.md`](../../16f-rueckfrage-epic-parameter-lokal.md), Quelle: Epic „Baked River
Simulations – Parameter Reference“, lokal gelesen):
- **SWR-Startwerte je SWR-Bereich** (`swr.sim_vorgaben`): `match_spline` true (auch Teilstücke),
  `match_spline_height_amount` **0,02** (Nachfüllrate; vorher 2 = Ursache von Befund 7), `remove_outside_spline_amount` 50,
  `source_size_cm` = `RiverWidth` des ersten Splinepunkts des Bereichs (Bachbreite an der Quelle), `sim_speed` 10,
  `num_steps` 10. `resolution_max_axis` wie bisher nach Zielzelle. Testreihe in den Regeln (`testreihe`: 0 / 0,02 / 0,05;
  `source_size` 300 / 1000 cm).
- **`back_liste.json`** nennt je SWR `sim_vorgaben` (Auflösung, die Felder oben, `use_capture`). Sie stehen **nicht** im
  Fingerabdruck; das lokale Werkzeug backt neu, wenn Fingerabdruck **oder** `sim_vorgaben` vom letzten Backen abweichen.
- **Mindestgröße der Hindernisse:** größte Ausdehnung = max über x, y, z von (Netz-Bounds) × |Skala|, ohne Drehung,
  ≥ 0,4 m (Ferat: „Steine ≥ 0,4 m eintragen“); Höhe der Welt-Box ≥ 0,2 m wie bisher. Bis v7 zählte die größte Seite der
  gedrehten Welt-Box im Grundriss; ein schräg liegender 0,3-m-Stein kam so über 0,4 m. Kleinere Objekte bekommen keine
  `wasser_kollision` und stehen in keinem `WH_`-Akteur. Feld `ausdehnung_m` je Eintrag. 2-m-Lauf: 42 285 → 40 980
  eindeutige Objekte (1 323 kleine Felsen und Steinpackungen weg, 18 lange bzw. hohe Objekte neu), WH-Instanzen
  41 251 → 39 946.
- **Prüfer:** FEHLER, wenn ein SWR-Feld von der Vorgabe abweicht, `num_steps` < `sim_speed`, `source_size_cm` ≠ Breite am
  ersten Punkt, `sim_vorgaben` in der Back-Liste ≠ SWR, `ausdehnung_m` ≠ neu gerechnet (eigene Rechnung aus Bounds × Skala)
  oder < 0,4 m.

**Ergänzungen 16g** (Regeln Version 9, Format bleibt `fluss_sim_v3`; Antwort
[`../../16g-swr-steiler-bergbach.md`](../../16g-swr-steiler-bergbach.md)). Nur **Diagnose**: Spline, SWR-Werte,
`sim_vorgaben` und Fingerabdrücke bleiben gleich.
- **`swr_bereiche[].rand_steil`** je SWR-Bereich (Grenzen in `swr.rand_steil`, Status „Vorschlag 16g“):
  - `rechteck_ue_cm`: Box der Splinepunkte **ohne** Breite. So bildet UE die Simulationsfläche (16g Befund 8: Quelle 0,2 m vom
    Rand). `rechteck_m` und die Zelle rechnet der Export weiter mit ± halber Breite (Rückfrage 3 in 16g).
  - `anfang`: Seite und Abstand des ersten Punkts zum UE-Rechteck; `zu_nah` unter `quelle_abstand_min_m` (10 m).
  - `kontakte`: Punktfolgen, deren halbe Breite über das UE-Rechteck ragt (dort liegt das Bett teils außerhalb der
    Simulation); `am_ende` = beginnt in den ersten bzw. endet in den letzten 10 m des Bereichs.
  - `rahmen_cm` / `rahmen_m`: Soll-Rechteck, jedes Bett ± (halbe Breite + `rand_zugabe_m` 5 m).
  - `hoehenspanne_m`, `z_m`, `gefaelle_fenster_max` (Spiegelgefälle im 20-m-Fenster, Stufen zählen mit).
  - `steilstrecken`: zusammenhängende Strecken ≥ `strecke_min_m` (50 m) mit ≥ 30 % (`kaskade`) bzw. 15–30 % (`pruefen`).
  - `eignung`: `swr` / `pruefen` / `kaskade_vorschlag` (Plan B: Kaskadennetz + Speisepunkt am Fuß).
- **`zusammenfassung.json` → `swr_rand_steil`:** Quellen zu nah am Rand, SWR mit Kontakt mitten im Lauf, Höhenspannen,
  Eignung, Kaskaden-Länge, die zehn steilsten SWR.
- **Prüfer:** rechnet `rand_steil` neu (Abweichung = FEHLER), prüft Steilstrecken und Rahmen und meldet zwei HINWEIS-Zeilen
  (Rand, Steil).

**Ergänzungen 16g Nachtrag** (Regeln Version 10, Format bleibt `fluss_sim_v3`; Antwort
[`../../16g-nachtrag-ursache-gefunden.md`](../../16g-nachtrag-ursache-gefunden.md)). Ursache des Stillstands war die zu grobe
**Wasser-Info der Water Zone** (C2: 1208 m / 1024 = 1,18 m je Pixel; mit 4096 ist das Bett zu 99,9 % nass). Spline,
SWR-Werte, `sim_vorgaben`, `back_liste.json` und Fingerabdrücke bleiben gleich.
- **Regel** (`swr.water_info`, Ferat): Pixel der Wasser-Info der zuständigen Zone ≤ **schmalste Bachbreite / 6**. Breite =
  `RiverWidth` der Splinepunkte (Plan-Bett).
- **`swr_bereiche[].water_info`** je SWR-Bereich: `breite_min_m` (+ s), `breite_median_m`, `pixel_max_m` (= Breite / 6),
  `zone_max_m` je Auflösung 1024/2048/4096 (größte Zone, die die Regel erfüllt, also „Zone ≤ X m bei 4096“),
  `zone_bekannt` (nötige Auflösung in einer 1208-m-Zone wie `C2_Wasserzone`, Zweierpotenz; `ueber_max` über 4096;
  `pixel_quer` = Pixel quer über das schmalste Bett bei 1024/2048/4096).
- **`wasserzonen.json`** (neu): Vorschlag für die ganze Welt. Grundzone `WZ_WELT` (9 577 × 7 057 m, 4096², 2,34 m je Pixel)
  für Seen, Meer und Gewässer ab 14 m Breite; feine Zonen `WZ_Fnn` gruppiert (nach geforderter Pixelgröße, eine Zone wächst,
  solange sie mit ≤ 4096 je Achse die Regel hält und das nicht mehr Speicher kostet als eine eigene Zone + 32 MB).
  Je Zone Rechteck, Ausdehnung, Auflösung (Zweierpotenz je Achse), Pixel, schmalstes Gewässer, `overlap_priority`
  (Welt 0, fein 10), Speicher RGBA16F/RGBA32F (Format unbekannt), Gewässer und SWR-Bereiche.
- **`water_body.water_zone_vorschlag`** je Gewässer = seine Zone (als `WaterZoneOverride` setzen; ein Water Body gehört zu
  genau einer Zone, also muss sein ganzes Bett darin liegen).
- **`zusammenfassung.json` → `water_info`**: Breiten, Pixel, Zonengrößen, Auflösungen in einer 1208-m-Zone, Zonenvorschlag.
- **`rand_steil`** ist nur noch **Info** (Status-Text): Vorlauf 10 m an der Quelle ist eine Option, `pruefen` /
  `kaskade_vorschlag` heißen „im Bild ansehen“, Plan B nur, wenn das Bild es braucht.
- **Prüfer:** `water_info` je SWR-Bereich und `wasserzonen.json` neu gerechnet (Abweichung = FEHLER); jede vorgeschlagene Zone
  hält die Regel für alle ihre SWR-Bereiche und enthält deren Bett (sonst FEHLER); `water_zone_vorschlag` passt. Mit
  **`--zonen DATEI`** (bekannte Zonen, Beispiel [`zonen_beispiel_c2.json`](zonen_beispiel_c2.json)): zuständige Zone je
  Gewässer (Liste `gewaesser` = Override, sonst überlappend mit höchster `overlap_priority`), **Pixel > Breite / 6 = FEHLER**,
  Bett ragt aus der Zone = WARNUNG. Ohne `--zonen` nur die Empfehlung (zwei HINWEIS-Zeilen).

**Ergänzungen 16h** (Regeln bleiben Version 10, Format `fluss_sim_v3`; Antwort
[`../../16h-erlenbach-p2-talkaskade-ufer-wasser.md`](../../16h-erlenbach-p2-talkaskade-ufer-wasser.md)):
- **[`ersetzt.json`](ersetzt.json):** Welt-Läufe, die lokal durch einen eigenen Lauf ersetzt sind. Stand: `F_ERLENBACH_1_C2`,
  `F_ERLENBACH_1V_C2` (bisher Pilot C2), `F_ERLENBACH_2_C2` und `B_R3_K10_TUNDRA_01` → **Erlenbach p2** (Ferats lokaler Lauf).
  Unsere C2-Pläne ruhen.
- **Export:** Teile, Lauf-Pläne (`<lauf>/plan.json`) und Roh-Ebenen ersetzter Läufe werden übersprungen
  (`zusammenfassung.json` → `eingaben.uebersprungen` mit Grund, `laeufe.ersetzt`). Ein Gewässer, das am ersetzten Lauf
  beginnt, trägt `anfang.ersetzter_oberlauf`; eine offene Mündung an einem ersetzten Lauf `muendung.ersetzter_lauf`.
  `tempo.c2` nennt nur noch den Ersatz.
- **Prüfer:** Soll-Läufe ohne die ersetzten; ein ersetzter Lauf in einem Gewässer ist FEHLER; HINWEIS mit der Liste.
- Planer (`gefaelle_daten.lade_strecken`/`alle_laeufe`, `gefaelle_plan.py`, `bachbett_roh.py` und beide Prüfer) lesen
  dieselbe Datei. Die Roh-Ebene spart die ersetzten Linien wie fremdes Wasser aus (dort fließt lokal der Ersatz).

**Ergänzungen 16g Nachtrag 2** (Regeln Version 11, Format bleibt `fluss_sim_v3`; Antwort
[`../../16g-nachtrag2-feinwerte-und-rueckfragen.md`](../../16g-nachtrag2-feinwerte-und-rueckfragen.md)). Grundlage: Ferats
Läufe N1–N7, F1 und F2 an C2 (Zone 4096).
- **SWR-Vorgaben** (`swr.sim_vorgaben`, auch in `back_liste.json`):
  - `match_spline_height_amount` **0,3** (0,1 und 0,2 bleiben bei s 76 stehen; 0,3 = gemessene Schwelle). Testreihe 0,3 / 0,4.
  - `remove_outside_spline_amount` **0** (F1: 50 nimmt 38 % des Überlaufs, macht das Bett aber 15 % flacher).
  - **`band_zugabe_m` 2** (neu, F2): `RiverWidth` im Editor = Bett (`punkte[3]`, Plan-Bett) + 2 m. Der Export behält in
    `punkte[3]` das Bett, weil Kollision, Filter und Tempo damit rechnen; das Bau-Werkzeug addiert die Zugabe.
    Der Planer-Fingerabdruck (Splineteil) rechnet weiter mit `punkte[3]`; der Editor-Fingerabdruck mit der Editor-Breite.
    Verglichen wird immer gleich mit gleich, und `band_zugabe_m` steht in `sim_vorgaben`, also löst eine Änderung Neu-Backen aus.
  - `source_size_cm` = max(**300**, `RiverWidth` am ersten Punkt). 55 von 197 SWR ändern sich (vorher ab 70 cm).
- **Regel Wasser-Info** (`swr.water_info`): Pixel ≤ **schmalstes Band (Bett + 2 m) / 12** (Ferats Vorschlag nach F2:
  Band = Bett mit 6,8 Pixeln quer → Front s 59; Bett + 2 m mit 12–14 Pixeln → durch). Teiler 6 auf das Bett (v10) reicht
  nicht. `water_info` je SWR-Bereich nennt zusätzlich `band_min_m`; `pixel_quer` zählt über das Band.
- **Hindernis-Filter** (`swr.hindernis_filter`, Ferats N5):
  - Lippen-, Rand- und Bettfelsen bekommen keine Wasser-Kollision (Rolle aus der Instanz-Ebene, `dateien.<netz>.rolle`).
  - Dazu jedes Teil, das quer im Bett mehr als **40 %** der Bettbreite belegt.
  - Je Meter Lauflänge zusammen höchstens **50 %** der Bettbreite (gierig, schmalste Teile zuerst).
  - Ausgefilterte Teile bleiben Deko: Sie stehen in `ohne_wasser_kollision` mit `grund` `filter_rolle` / `filter_teil` /
    `filter_meter` / `filter_anderes_gewaesser`. Jeder Eintrag hat `filter` (`rolle`, `quer_im_bett_m`, `bett_breite_m`,
    `s_laengs_m`).
  - 2-m-Lauf: 40 221 → **20 225** eindeutige Objekte mit Wasser-Kollision, WH-Instanzen 39 239 → 19 864, Akteure mit Tag
    982 → 361. `zusammenfassung.json` → `hindernis_filter`.
- **Fingerabdrücke:** Bei 194 von 197 SWR ändert sich der **Objektteil**. Gelände und Splines bleiben gleich, bei allen 197
  ändern sich die `sim_vorgaben`. Alle SWR sind neu zu backen.
- **`wasserzonen.json`** je Zone `hoehe_m`, `half_float_stufe_cm` (absolut / relativ / maßgeblich), `half_precision_ok`
  (Stufe ≤ 4 cm) und `format_empfohlen`; Summe `half_precision` mit dem Speicher bei empfohlenem Format.
- **Prüfer:** rechnet den Filter unabhängig nach (eigene Drehung der Netz-Bounds, eigene Meter-Rechnung). FEHLER bei Lippen-,
  Rand- oder Bettfelsen mit Wasser-Kollision, bei einem Teil über 40 %, bei einem Meter über 50 %, bei falschem Grund und
  bei einem ausgefilterten Teil mit Wasser-Kollision in einem anderen Gewässer. Dazu SWR-Vorgaben v11 und `source_size_cm`.
  Mit `--zonen`: Zone mit `half_precision: true` und Höhenstufe über 4 cm = WARNUNG.
- `zonen_beispiel_c2.json` hat jetzt Ferats echte C2-Werte (Zentrum, 1208 m, 4096, Half Precision aus).

**Ergänzungen 16h Nachtrag 3** (Regeln bleiben Version 11, Format `fluss_sim_v3`; Antwort
[`../../16h-nachtrag3-teile-a-c1-t3-schaum.md`](../../16h-nachtrag3-teile-a-c1-t3-schaum.md)):
- **Kopf-Kürzung am Ersatz** (`ersetzt.json` → `ersatz.<ID>.muendung_anschluss`, `aktiv`): Ein Ziel-Lauf ohne Gefälle-Plan, in
  den ein lokal ersetzter Lauf mündet (`F_ERLENBACH_2_C3` ← Erlenbach p2), beginnt erst am ersten Punkt mit Spiegel ≤ Ersatz-Spiegel
  + `toleranz_cm`. Der Kopf davor ist der Rest des ersetzten Laufs (alte Feld-Überlappung). Umgesetzt wie die Feldgrenzen-Kürzung
  (`s_quelle_m`, `gekuerzt_m`); `anfang.kopf_gekuerzt` nennt den Schnitt, `anfang.punkt_cm` den neuen Anfang.
- **Prüfer:** FEHLER, wenn ein Gewässer am Ziel-Lauf über dem Ersatz-Spiegel beginnt oder der Schnitt nicht zum Lauf passt;
  sonst HINWEIS.

**Ergänzung 16h Nachtrag 4:** `muendung_anschluss.lokaler_kopf` (s, Spiegel, Breite je Kopfpunkt, optional `folge_breite`)
übernimmt Ferats lokalen C3-Kopf: Die Linie des Ziel-Laufs beginnt am ersten Kopfpunkt (s 24 m), die Kopfpunkte ersetzen die
Weltpunkte bis s 38 m. p2-Spiegel jetzt 36,80 m. Antwort
[`../../16h-nachtrag4-v18-muendung.md`](../../16h-nachtrag4-v18-muendung.md).

Antwort dazu: [`../../16c-ferat-ein-fluss-je-gewaesser.md`](../../16c-ferat-ein-fluss-je-gewaesser.md); v2 (Strecken-Einheiten):
[`../../16b-swr-c2-ganze-strecke.md`](../../16b-swr-c2-ganze-strecke.md).

Der Exporter **liest nur**: die Planer-Ausgaben von `gefaelle_plan.py` (`<lauf>/plan.json`, `instanzen/`), der Sehens-Planer
(`<biom>/orte.json`, `sw_<biom>/`) und die Weltdaten (`wasser_welt.json`, `baeche_alle.json`, Höhe, Meer). Er ändert keine
Stufe, kein Becken, keine Lippe und kein Gelände (13f-Regel); der Prüfer vergleicht Lippen- und Fußhöhen mit der Quelle.

| Datei | Inhalt |
|---|---|
| `fluss_sim_export.py` | Exporter: Läufe verketten, Mündungen, `fluss_sim.json` je Gewässer, `back_liste.json` (je SWR-Bereich), `zusammenfassung.json`; Referenz-Funktionen für den Fingerabdruck |
| `fluss_sim_pruefen.py` | Prüfer (FEHLER/WARNUNG/HINWEIS), Exit-Code 1 bei FEHLER |
| `fluss_sim_regeln.json` | alle Zahlen (Verkettung, Mündung, Spline, SWR/Auflösung/Teilung, Fall, Kollision, Schaum, Vorhang, Fingerabdruck, Grenzen der Hindernis-Akteure, SWR-Startwerte, Rand/Steil, Wasser-Info und Zonen, Hindernis-Filter, Half Precision), Version 11 |
| `ersetzt.json` | 16h: lokal ersetzte Welt-Läufe (C2 → Erlenbach p2); Planer, Export und Prüfer überspringen sie |
| `zonen_beispiel_c2.json` | Beispiel für `--zonen` (bekannte Water Zones; C2 nach Ferat: Zentrum (−221 050; −254 850) cm, 1208 m, 4096, Half Precision aus) |

## Aufruf

Cloud (2 m), Planer-Ausgaben vorher in den Scratchpad erzeugen:

```
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --alle --daten2m recherche/vorlagen/daten/sehens --aus <s>/gef
python -I recherche/antworten/skripte/sehens_<biom>/sehens_<biom>.py --daten2m recherche/vorlagen/daten/sehens --aus <s>/sehens/<biom>   # je Biom
python -I recherche/antworten/skripte/gefaelle/bachbett_roh.py --gefaelle <s>/gef --daten2m recherche/vorlagen/daten/sehens \
       --aus <s>/bachbett_roh                                                                       # 16c Nachtrag 3
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle <s>/gef --sehens <s>/sehens \
       --roh <s>/bachbett_roh --daten2m recherche/vorlagen/daten/sehens --aus <s>/fs
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_pruefen.py <s>/fs --gefaelle <s>/gef --sehens <s>/sehens \
       --roh <s>/bachbett_roh --daten2m recherche/vorlagen/daten/sehens [--vergleich <s>/fs_zweiter_lauf] [--zonen DATEI]
```

Lokal (1 m), nach den Planer-Läufen auf 1 m:

```
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_export.py --gefaelle export/unreal/welt/gefaelle \
       --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt --daten1m export/unreal/welt \
       --aus export/unreal/welt/fluss_sim
python -I recherche/antworten/skripte/fluss_sim/fluss_sim_pruefen.py export/unreal/welt/fluss_sim \
       --gefaelle export/unreal/welt/gefaelle --sehens export/unreal/welt/sehens --sw-ordner export/unreal/welt \
       --daten1m export/unreal/welt
```

Die Roh-Lauf-Ebene `export/unreal/welt/bachbett_roh/` (vorher `gefaelle/bachbett_roh.py --basis <production>` laufen
lassen) liegt neben `gefaelle/` und wird ohne `--roh` gefunden.

Optionen:
- `--nur ID …` (Gewässer-, Lauf- oder Ort-IDs; verkettet wird immer über alle Läufe);
- `--gebaut LAUF …` (16d): schon gebaute Läufe, deren Gelände-Delta lokal bereits in `welt/` eingestempelt ist
  (Gefälle-Lauf-ID, Sehens-Ort-ID oder `SW_<ort>_<bach>`);
- `--einbau DIR` (16d): Ordner `sehens_einbau/` für die automatische Erkennung, Standard `<daten1m>/sehens_einbau`, sonst
  neben `--gefaelle` (`export/unreal/welt/gefaelle` → `export/unreal/welt/sehens_einbau`), neben `--sw-ordner` oder
  neben `--sehens`; `--ohne-erkennung` schaltet die Erkennung ab.

Der Prüfer nimmt dieselben Optionen nur zum Abgleich; maßgeblich ist, was der Export in `back_liste.json`
(`gelaende.deltas_ohne`) vermerkt hat. Laufzeit 2 m: ~36 s Export (davon ~15 s Vorschläge), ~40 s Prüfung. Ausgabe (`--aus`, 24 MB auf 2 m, nicht ins Repo):

```
gewaesser/<gewaesser>/fluss_sim.json     je Welt-Gewässer (154; Gefälle-Läufe mit Plan und rohe Läufe verkettet)
sehens/<biom>/<ort>/fluss_sim.json       je Sehens-Ort mit Bach (26 Orte, 42 Bäche in 33 Gewässern)
vorschlaege.json                         Vorschläge für offene Enden und Lücken (16d), nicht in der Spline
back_liste.json                          alle SWR-Bereiche mit Fingerabdruck und Back-Reihenfolge (back_liste_v3)
wasserzonen.json                         Vorschlag Water Zones (Grundzone + feine Zonen, Auflösung, Speicher; v10)
zusammenfassung.json                     Zahlen (Gewässer, Mündungen, SWR, Auflösungen, Varianten, Höhen)
```

Beispiele im Repo: [`../../fluss_sim/`](../../fluss_sim/) – `gewaesser/F_ERLENBACH` (seit 16h ab dem C3-Lauf; C2 ist durch Erlenbach p2 ersetzt, `ersetzt.json`),
`sehens/bergwald/bergwald_06_karsee`, `sehens/elfenwald/elfenwald_04_elfentreppe` (ein Gewässer mit 5 Töpfen, eine SWR),
`zusammenfassung.json`, `vorschlaege.json`, `back_liste_auszug.json`, `wasserzonen.json`.

## Eingaben und gebaute Läufe (16d)

**Nur Lauf-Pläne.** Unter `--gefaelle` zählt ein Ordner nur, wenn sein Name kein „.“ enthält, nicht mit „_“ beginnt und
seine `plan.json` den Schlüssel `wasser_koerper` hat. Übersprungen und im Protokoll genannt (`uebersprungen: …`, in
`zusammenfassung.json` unter `eingaben.uebersprungen`) werden
- Archivkopien wie `F_ERLENBACH_1V_C2.alt_v1_gebaut`, `.alt_vor15b`, `_alt/`;
- andere Pläne ohne `wasser_koerper`, z. B. der Feld-Instanzplan `gefaelle/C2/plan.json` von `a15_einbau.py`;
- Archiv-Feldordner unter `<lauf>/instanzen/` und `sw_<biom>/` (z. B. `C2.alt`, `_G3`).
Die Sehens-Biome werden über ihre festen Namen gelesen (`<biom>/orte.json`), Archivordner dort also nie.

**Gelände gebauter Läufe.** Der Fingerabdruck rechnet mit Welt + Planer-Deltas. Lokal sind gebaute Läufe schon in
`welt/hoehe.f32` eingestempelt; ihr Delta würde sonst doppelt zählen. Ein Delta wird **nicht** addiert, wenn
- die Lauf-ID (bzw. Sehens-Ort-ID oder `SW_<ort>_<bach>`) in `--gebaut` steht, oder
- `sehens_einbau/A15_<lauf>/lauf.json` existiert und `nachgezogen` das Feld des Eintrags enthält (bei Plänen über mehrere
  Felder je Abschnitt: alle `felder` des Abschnitts). Sehens: `A15_<ort>/lauf.json` oder `A15_SW_<ort>_<bach>/lauf.json`
  gegen `felder` des Orts.
- Fehlt die Datei, ist der Lauf ungebaut. Ist sie unlesbar oder nennt das Feld nicht, wird das Delta addiert und das
  Protokoll nennt die Datei (`lauf_json_ungebaut`).

Das Format von `lauf.json` ist hier nicht bekannt; gelesen werden (Annahme, `nachgezogen_felder()`):
`["C2", "C3"]`, `[{"feld": "C2", "ok": true}]` (auch `id`/`name`; `ok`/`nachgezogen`/`fertig`/`erledigt` falsch = nicht
nachgezogen), `{"C2": true | {…}, "C3": false}`, `{"felder": ["C2"]}`, `"C2,C3"`, `true` (alle Felder). Steht
`nachgezogen` nicht oben, wird in Unterobjekten bis Tiefe 3 gesucht. Groß-/Kleinschreibung egal.

Protokoll (`gebaut: … nicht addiert (…)`), `zusammenfassung.json` (`gelaende_deltas.gebaut`, mit Quelle und Form) und
`back_liste.json` (`gelaende.gebaut`, `gelaende.deltas_ohne`) nennen die gebauten Läufe. Die `lage` der
Kollisionsobjekte hängt nicht vom Gelände ab (Objekt-Bounds gegen Spline und Wasserstand aus dem Plan); das doppelte
Delta verfälschte nur den Gelände-Teil des Fingerabdrucks.

## Gewässer bilden (Verkettung, Mündung)

- **Läufe:** alle 27 Feld-Stücke aus `wasser_welt.json` und alle 168 Bäche aus `baeche_alle.json` (98 mit Gefälle-Plan,
  97 roh) sowie die 42 Sehens-Bäche.
- **Fortsetzung** (gleiches Gewässer): Ende von P ≤ 8 m vom Anfang von N und N beginnt nicht höher (+ 0,5 m), oder
  Feldgrenze mit Überlappung (Ende von P liegt ≤ 1 m auf N bei s ≤ 40 m und umgekehrt). Gekürzt wird das Stück ohne Plan,
  sonst das untere (`laeufe[].gekuerzt_m`, `abstuerze_entfallen`). Je Lauf höchstens ein Vorgänger.
- **Name:** Flüsse nach dem gemeinsamen Präfix der `fluss`-Namen (`F_ERLENBACH`, `F_HAUPTFLUSS_3`), Bachketten nach dem
  obersten Lauf, Sehens-Bäche wie bisher (`SW_<ort>_<bach>`).
- **Mündung** (Reihenfolge, Zahlen in `regeln.gewaesser`):
  1. ausdrücklich: Sehens `muendung`/`muendung_art`, R2-Bäche `anschluss.ende` (wenn das Ende ≤ 15 m neben dem Ziel liegt);
  2. **Fluss/Bach** (Zusammenfluss): Ende ≤ halbe Breite + 3 m neben der Mittellinie eines anderen Laufs, nicht > 1 m
     unter dessen Spiegel. Der Nebenlauf **endet** im Hauptlauf; seine Spline bleibt bis ins Wasser des Hauptlaufs.
     Senkt der Gefälle-Plan des Hauptlaufs sein Becken (`zufluesse`), wird das Endstück des Nebenlaufs abgesenkt
     (`muendung.endstueck_angepasst`). Der Hauptlauf führt den Nebenlauf in `zufluesse` (s, SWR-Bereich);
  3. **See** (Umriss Welt- oder Sehens-See + halbe Breite + 5 m);
  4. **Meer** (Meer-Raster ≤ halbe Breite + 10 m, oder Ende ≤ 2 m hoch und Meer ≤ 150 m: Bach endet am Strand);
  5. **nah** (Lücke in den Weltdaten): Lauf bzw. See ≤ 25 m neben dem Ende → Mündung mit `luecke_m`;
  6. **Wasserfall** (Welt-Wasserfall ≤ 120 m), sonst **versickert** (Sehens) bzw. **offen** (mit `naechster_lauf`).
- `overlap_material_priority` = 10 − Stufe im Mündungsbaum (Hauptlauf 10, Zufluss 9 …).
- `anfang`: `quelle`, `see` (Seeabfluss), `topf` oder `wasserfall`.

**Töpfe (16d, Regel `gewaesser.topf`).** Ein Sehens-See mit größter Ausdehnung (größter Abstand zweier Umrisspunkte)
< 30 m, in den ein Sehens-Bach mündet oder aus dem einer abfließt, ist ein **Topf** des Gewässers:
- **Durchfluss** (Zulauf und Abfluss): Zulauf → Topf → Abfluss wird **ein** Gewässer (Elfentreppe: 6 Bäche, 5 Töpfe;
  Gletschertöpfe: 4 Bäche, 3 Töpfe; Wollsackfall: 2 Bäche, 1 Gumpe). Bei mehreren Zuläufen geht der längste weiter.
- **Quelltopf** (nur Abfluss): Das Gewässer beginnt in der Topfmitte (`anfang.art = "topf"`).
- **Endtopf** (nur Zulauf): Das Gewässer endet in der Topfmitte (`muendung.art = "topf"`).
- Spline: ein Punkt in der Mitte des Topf-Rechtecks auf dem Spiegel, Rolle `topf`, Breite = größte Rechteckseite + 2 × 1 m
  (so schließt das SWR-Rechteck den Topf ein), Tiefe aus `tiefe_m`, Tempo 10 cm/s; dazwischen wie üblich 2–4 m.
- Export: `toepfe[]` (See, Art, `s_m`, Spiegel, Rechteck, `water_body_lake: false`) und ein Bereich mit `rolle: "topf"`.
  Lokal für diese Seen **keinen** `WaterBodyLake` bauen; die SWR des Gewässers füllt sie.
- Größere Seen (Biberstau 36 m, Karsee 34 m, Moränensee 32 m, Trunkensee 50 m) bleiben `WaterBodyLake` und Mündungsziel;
  Welt-Seen bleiben unverändert. Beginnt ein anderes Gewässer an einem Topf (`B_R_P2_M1_01` am Blautopf), heißt der
  Anfang `topf` mit `gewaesser` = Besitzer.

**Vorschläge (16d, Regel `gewaesser.vorschlag`).** Für jede Mündung `offen` und jede Mündung mit `luecke_m` steht in
`muendung.vorschlag` (und gesammelt in `vorschlaege.json`) ein Vorschlag; die Spline bleibt unverändert:
- **Lücke:** gerade vom Spline-Ende bis 1 m hinter den Wasserrand des bekannten Ziels.
- **Offen:** auf einem 4-m-Suchraster (Umkreis 1 500 m, Gelände = Welt + Deltas) entlang des **steilsten Gefälles** (D8);
  endet das in einer Senke, weiter auf dem Weg des **geringsten Anstiegs** (Dijkstra, Kosten = Länge + 20 × Anstieg) bis
  zur ersten Wasserzelle (Gewässer-Streifen, See ohne Töpfe, Meer) mit Spiegel ≤ Ende + 1 m. Das eigene Gewässer, seine
  Zuflüsse und Gewässer, deren Mündungskette selbst offen endet, zählen nicht als Ziel.
- Felder: `punkte` (erster = Spline-Ende; Punkte ≤ 5 m; z = min(vorheriges z, Gelände), nie steigend; Breite/Tiefe/Tempo
  vom Ende), `ziel` (Art, ID, Spiegel, ggf. `s_m`), `laenge_m`, `dz_m`, `einschnitt_max_m` (Gelände über dem Wasser),
  `kreuzt` (Wasser mit höherem Spiegel auf dem Weg), `methode`, `begruendung`.

## Format `fluss_sim.json` (v3)

Gekürzt aus `F_ERLENBACH`:

```json
{"format": "fluss_sim_v3", "regeln_version": 3, "fall_schwelle_m": 1.0, "daten": "2m (Cloud-Test)",
 "gewaesser": [{"id": "F_ERLENBACH", "kategorie": "welt", "art": "fluss", "laenge_m": 1006.7,
   "laeufe": [{"id": "F_ERLENBACH_1_C2", "herkunft": "roh", "s_m": [0.0, 17.23], "gekuerzt_m": [0.0, 11.74], "...": "..."},
              {"id": "F_ERLENBACH_1V_C2", "art": "fluss", "herkunft": "plan", "feld": "C2", "s_m": [17.4, 220.56],
               "s_quelle_m": [0.0, 203.16], "gekuerzt_m": [0.0, 0.0], "quelle": {"plan": "gefaelle/F_ERLENBACH_1V_C2/plan.json"},
               "abstuerze_entfallen": [], "anschluss_oben": "ueberlappung", "swr_typ": "bach"}, "..."],
   "anfang": {"art": "quelle", "punkt_cm": [-171943.9, -241121.6, 10395.2]},
   "muendung": {"art": "meer", "ziel": "meer", "abstand_m": 37.62, "punkt_cm": [-154268.1, -149865.4, 158.2],
                "quelle": "geometrie (Meer-Raster)", "stufe": 0},
   "zufluesse": [{"gewaesser": "B_R3_K10_TUNDRA_01", "art": "bach", "s_m": 376.42, "swr_bereich": "F_ERLENBACH_T00",
                  "water_body": "WBR_B_R3_K10_TUNDRA_01"}, "..."],
   "water_body": {"id": "WBR_F_ERLENBACH", "klasse": "WaterBodyRiver", "affects_landscape": false, "overlap_material_priority": 10,
     "spline": {"s_m": [0.0, 1006.7],
       "punkte": [["...", "..."], [-172505.0, -238470.5, 10043.5, 2500.1, 194.6, 240.0], [-172522.1, -238423.5, 9953.5, 2480.1, 215.4, 150.0], "..."],
       "punkte_felder": ["x_cm", "y_cm", "z_cm", "RiverWidth_cm", "Depth_cm", "WaterVelocityScalar_cm_s"],
       "punkt_typen": ["...", "LINEAR", "LINEAR", "..."], "tangenten_cm": ["..."],
       "punkte_s_m": ["...", 27.4, 27.9, "..."], "punkt_rollen": ["...", "lippe", "fuss", "..."]}},
   "abstuerze": [{"id": "F_ERLENBACH_1V_C2_s1_S01_T2", "lauf": "F_ERLENBACH_1V_C2", "s_lippe_m": 31.65, "s_fuss_m": 32.15,
                  "fall_m": 1.27, "rampe": false, "z_oben_cm": 9946.0, "z_unten_cm": 9818.7, "punkt_lippe": 15, "punkt_fuss": 16}, "..."],
   "bereiche": [{"id": "F_ERLENBACH_A03", "s_m": [43.06, 50.34], "rolle": "becken", "oben_fall": "…_S01_T5",
                 "unten_fall": "…_S02_T2", "abstuerze_innen": ["…_S02_T1"],
                 "becken": [{"s_m": [43.06, 48.13], "spiegel_cm": [9474.2, 9464.1], "...": "..."}],
                 "laeufe": ["F_ERLENBACH_1V_C2"], "swr_bereiche": ["F_ERLENBACH_T00"]}, "..."],
   "faelle": [{"id": "F_ERLENBACH_1V_C2_s1_S04", "fall_m": 4.67, "s_lippe_m": 70.05, "s_fuss_m": 70.55,
               "punkt_lippe": 39, "punkt_fuss": 40, "bereich_oben": "F_ERLENBACH_A06", "bereich_unten": "F_ERLENBACH_A07",
               "swr_bereich": "F_ERLENBACH_T00", "vorhang": true, "vorhang_status": "wartet (Ferat 16c …)", "...": "wie v2"}, "..."],
   "swr_bereiche": [{"id": "F_ERLENBACH_T00", "s_m": [0.0, 468.88], "s_sim_m": [0.0, 472.88], "punkt_index": [0, 260],
     "rechteck_cm": [-180504.0, -242771.6, -167447.0, -196865.4], "rechteck_m": [130.57, 459.06],
     "naht_oben": {"art": "quelle", "s_m": 0.0},
     "naht_unten": {"art": "becken", "s_m": 468.88, "ueberlappung_m": 8.0, "ueberlappung_s_m": [464.88, 472.88]},
     "vorgaenger": [], "nachfolger": ["F_ERLENBACH_T01"], "back_reihenfolge": 0, "geteilt": true,
     "swr": {"id": "SWR_F_ERLENBACH_T00", "klasse": "ShallowWaterRiver", "typ": "bach", "zelle_ziel_m": 0.25, "zelle_max_m": 0.3,
             "achse_m": 459.06, "resolution_max_axis": 1856, "zelle_m": 0.247, "raster_erwartet": [528, 1856],
             "source_river_water_bodies": ["WBR_F_ERLENBACH"], "sink_river_water_bodies": ["WBR_F_ERLENBACH"],
             "bottom_contour_tags": ["SWR_Hindernis"], "bottom_contour_actors": ["WH_F_ERLENBACH_T00"], "use_capture": true,
             "match_spline": true, "match_spline_height_amount": 0.02, "remove_outside_spline_amount": 50.0,
             "source_size_cm": 3300.0, "sim_speed": 10, "num_steps": 10, "begrenzung": {"art": "rechteck_teil", "rechteck_cm": ["..."], "hinweis": "…"},
             "render_state": {"backen": "LIVE_SIM", "spiel": "WATER_COMPONENT_WITH_BAKED_SIM", "ersatz": "BAKED_SIM"},
             "material": {"water_body": "MI_EL_SWR_Klar", "baked_sim_material": "MI_EL_SWR_Klar"}},
     "bereich_cm": [-181304.0, -243571.6, -166647.0, -196065.4], "zufluesse": ["WBR_B_R3_K10_TUNDRA_01"],
     "hindernis_akteur": {"id": "WH_F_ERLENBACH_T00", "...": "wie v2"}, "fingerabdruck": "34f419d2…"}, "..."],
   "wasser_kollision": [{"...": "wie v2", "s_m": "…", "bereich": "F_ERLENBACH_A…", "swr_bereich": "F_ERLENBACH_T00",
                         "hindernis_akteur": "WH_F_ERLENBACH_T00"}],
   "ohne_wasser_kollision": ["..."]}]}
```

- **Ungeteiltes Gewässer** (188 von 196): ein Eintrag in `swr_bereiche` mit `id` = Gewässer-ID, SWR `SWR_<gewaesser>`,
  WH `WH_<gewaesser>`, `begrenzung.art = "rechteck_um_fluss"`, `match_spline: true` (v8: alle SWR, Startwerte s. o.).
- **Geteilt** (5): `<gewaesser>_T00 …`, `geteilt: true`, `match_spline: true` (bis v7 „lokal testen“), `begrenzung.art = "rechteck_teil"` mit
  dem Rechteck des Stücks (Weltkoordinaten, cm). Alle nennen denselben `WBR_<gewaesser>` als Quelle und Senke.
- **Bau-Werkzeug (v3):** je Gewässer **einen** `WaterBodyRiver` aus `water_body.spline`, je `swr_bereiche[]` eine
  `ShallowWaterRiver` und einen `WH_…` aus `hindernis_akteur`. `bereiche` sind nur s-Bereiche (Rolle `becken`, `rinne`,
  `gerinne`, `lauf`) für Becken, Fall-Zuordnung und Prüfung, keine Water Bodies.

## Regeln

**Spline** (`regeln.spline`). Anfang, Ende und je Stufe (jeder Absturz aus Plan bzw. Sehens, auch Kaskaden-Teilstufen und
Schnellen) ein Punkt an der **Lippe** (z = Oberwasser `z_oben_cm`) und einer am **Fuß** (z = Unterwasser `z_unten_cm`), beide
`LINEAR`, dazwischen kein Punkt. Sonst gleichmäßig mit Abstand ≥ 2 m (roh ≥ 5 m), also 2–4 m (5–10 m). Fuß ≥ Lippe + 0,1 m;
liegt die nächste Lippe näher als 0,05 m am Fuß, teilen sie sich einen Punkt (`fuss_lippe`). z nie steigend. Rollen der
übrigen Punkte: `becken` (Spiegel flach ≤ 3 % zu den Nachbarn), `rampe`, `gerinne`, `rinne`, `river`, `roh`.
**Tangenten** wie v2 (Catmull-Rom in xy, z monoton, 0 an `LINEAR` und flachen Nachbarn).

**SWR** (`regeln.swr`, Nachtrag 17:45). Zielzelle je Lauf: Bach (Abstürze im Plan, Median der Breite < 15 m, Sehens-Bach)
0,25 m, höchstens 0,30 m (16e: ein ungeteilter Bach bis 0,40 m, `zelle_max_bach_ungeteilt_m`); Fluss 0,35 m. Ein SWR-Bereich, der einen Bach-Lauf berührt, gilt als Bach.
`resolution_max_axis` = ⌈längste Rechteckseite / Ziel / 32⌉ × 32, in [32; 2048]; `zelle_m` = Seite / Auflösung.
**Teilung** nur, wenn das Rechteck des ganzen Flusses bei 2048 die Höchstzelle überschreitet (16e: Bach > 819 m bei
0,40 m, vorher > 614 m; Fluss > 717 m); die Teilstücke halten dann Bach 0,30 m bzw. Fluss 0,35 m:
kleinste Anzahl Stücke, unter gleich vielen die kleinste Summe der Rechteckflächen (dynamische Programmierung über die
Splinepunkte), Naht ≥ 5 m von jeder Stufe und ≥ 50 m vom Anfang/Ende, Nachbarn überlappen 8 m (`s_sim_m`).
`naht.art` = `becken`, wenn die Naht in einem Becken liegt, sonst `lauf`.

**Tempo (16e, `regeln.tempo`).** Je Splinepunkt, nur aus den gerundeten Spline-Werten (der Prüfer rechnet nach):
1. Spiegelgefälle I = (z(s − 2 m) − z(s + 2 m)) / 4 m (am Rand einseitig); Stufen zählen mit, Lippe und Fuß werden schnell.
2. Abfluss Q = 0,2 m/s × Median(Breite × 0,6 × Depth) über ± 100 m: ein Becken mittlerer Größe fließt mit 0,2 m/s
   (der Plan kennt keinen Abfluss; seine Tiefe ist die Bett-Tiefe, keine Fließtiefe). q = Q / Breite.
3. Manning-Strickler bei Normalabfluss (breites Gerinne): v = k_st^0,6 · q^0,4 · max(I; 0,0001)^0,3,
   k_st = 15 (Bach, Blöcke, Stufen-Becken) bzw. 25 m^(1/3)/s (Fluss). In Becken und Töpfen (Rückstau von der Lippe, die
   Planer-Tiefe ist die Wassertiefe) zusätzlich v = min(v; q / h): ein mittleres Becken fließt mit 0,2 m/s.
4. v in [0,1; 2,5] m/s, Gauß-Glättung (σ 0,75 m), dann Änderung ≤ 0,6 m/s je m (nur Spitzen sinken), × `tempo_faktor` (1,0).
5. `tempo_ms` (0,001 m/s), `WaterVelocityScalar_cm_s` = `tempo_ms` × 100 (UE-Einheit cm/s, Standard 128, Kodierung bis
   `r.Water.MaxFlowVelocity` 1024). `tempo_info.gefaelle` und `tempo_info.kst` je Punkt.
- Die Spline-Werte ändern den Fingerabdruck (Splineteil) → alle SWR gelten als „neu backen“.

**Schaum-Maske (16e, `regeln.schaum.maske`).** Je Vorhang-Fall eine Kapsel `a_cm` (Fuß) → `b_cm` (Ende des
Aufprallteppichs, höchstens Fuß + 6 m), Radius = halbe Teppichbreite in [1; 3] m, Stärke = Fallhöhe / 5 m in [0,4; 1].
`slots_max` 8 je Water-Body-Material (`ueber_slots`, wenn mehr). Für Option B im Material; bei Option A bleibt das Feld unbenutzt.

**Fall, Vorhang, Schaumobjekte** wie v2 (`fall_schwelle_m` 1,0, Vorhang ab 3 m bzw. senkrechte Felslippe ab 2 m, Schaum nur
an Vorhang-Fällen); `vorhang_status` = „wartet“ (Ferat 16c).

**Wasser-Kollision.** Ein Objekt (Instanz einer Ebene oder Akteur) bekommt `wasser_kollision: true`, wenn es
- **fest** ist: Kollision im Plan, Fels-/Klippennetz (`sehens_lib.steilwand.ist_fels`) oder Holz (`holz_muster`),
  nie eine Pflanze (`pflanze_muster`);
- **groß genug** ist (v8): größte Ausdehnung ≥ 0,4 m (Netz-Bounds aus `netze_masse.json`, sonst `netze.csv` „unten Mitte“,
  × |Skala|, ohne Drehung; Feld `ausdehnung_m`) und Höhe der gedrehten Welt-Box ≥ 0,2 m. Kies, Steinpackungen und kleine
  Steine bleiben ohne und kommen in keinen `WH_`-Akteur;
- **im Wasser oder ≤ 1 m daneben** steht: Abstand Mittelpunkt–Spline − Grundriss-Radius − halbe Breite ≤ 1 m,
  Unterkante ≤ Spiegel + 0,5 m, Oberkante ≥ Bett − 0,1 m.

`lage`: `im_wasser` (Grundriss schneidet die Wasserfläche) oder `ufer`. Der Verweis `ref` ist eindeutig:
`quelle` (Ebene `gefaelle/<lauf>/instanzen/<Feld>/plan.json` bzw. `sw_<biom>/<Feld>/plan.json`) + `datei` + `index`
(Zeile in `<datei>.f32`) bzw. `liste: "akteure"` + `index`. **v11:** Danach wirkt der Hindernis-Filter (Ergänzungen 16g Nachtrag 2). Objekte anderer Ebenen (Bestand, Felsgruppen, Witcher)
liegen in der Cloud nicht vor; lokal setzt das Bau-Werkzeug dieselbe Regel auf alle Ebenen im SWR-Bereich an.

**Schaumobjekte** je Fall (Nachtrag Datei 16):
- **Aufprallteppich**: am Fuß, Radius r = f × Fallhöhe mit f ∈ [0,5; 1] (deterministisch aus der Fall-ID), mindestens
  0,5 m; Länge 2r × 1,3 in Fließrichtung, höchstens 60 % des Beckens; Breite 2r, höchstens 90 % der Wasserbreite,
  mindestens Strahlbreite + 0,4 m. Rand ausgefranst (`seed`).
- **Schaumstraßen**: n = clamp(round(2 + 0,8 × Fallhöhe); 2; 6), ab dem Ende des Teppichs talwärts, 2–4 m lang
  (höchstens bis 0,3 m vor die nächste Lippe), 0,15–0,4 m breit, ±0,3 m gebogen, auslaufend; seitlich über die
  Strahlbreite + 0,5 m verteilt und innerhalb der Wasserbreite. Keine Straßen, wenn das Becken < 1 m Platz lässt.
- **Kehrwasser** (ruhend, Ø 0,6–1,6 m, ≤ 4 je Becken): neben dem Aufprall beidseitig, wenn neben dem Strahl Platz ist;
  im Lee von Randblöcken (feste Objekte, deren Grundriss die Wasserkante ±0,5 m schneidet, z. B. 15g-Randblöcke);
  in Buchten hinter Vorsprüngen (`ufer_rand` aus 15g, Einzug ≥ 0,4 m → 0).
- **Gischt** an Fällen ≥ 3 m: kein neues Objekt, sondern die vorhandenen Nature-Water-FX-Effekte (`effekte`, `cull_m`
  aus 13k).
- Netze und Decals wählt das lokale Bau-Werkzeug. Kandidaten im Inventar (`inventar_extra.json`):
  `/Game/Eldarien/Welt/Wasser/MI_EL_Fluss_Schaum`, `/Game/Eldarien/Welt/Wasser/Stufenfall/MI_EL_Stufenfall_Schaum`.

**Kaskadennetz nur noch an Vorhang-Fällen (v2).** `kaskadennetz.bereich_s_m` = [Lippe − 0,5 m; Fuß + 1,5 m] auf
`mittellinie_s_m` des bisherigen Netzes, nur bei `vorhang: true` (sonst `null`). Das Bau-Werkzeug schneidet das Netz auf
diese Bereiche zu; Becken, flache Strecken und alle anderen Fälle übernimmt die Simulation.

**Vorhang (v2, 16b).** `vorhang: true` nur an einer echten Fallkante:
- Einzelabsturz (keine Kaskaden-Teilstufe, keine Schnelle) **≥ 3,0 m** (wie `vorhang_ab_m` des Planers, 14b), oder
- **senkrechte Felslippe**: Einzelabsturz ≥ 2,0 m, Art `fall`, keine Holzstufe, horizontaler Versatz Lippe → Fuß
  (`versatz_m`, Überfall-Mitte bzw. Lippenpunkt gegen `fuss_cm`) ≤ 0,3 × Fallhöhe (≥ 73°).
- Begründung: Die Simulation ist 2D (eine Höhe je Zelle von 0,35–0,5 m). Einen Absturz zeichnet sie als Rinne über
  1–2 Zellen. Unter 2 m liegt diese Rinne im Schaumband der Lippe und liest sich als Wildwasser (16b: C2 natürlicher
  als das Netz). Ab 3 m bzw. an einer senkrechten Wand ab 2 m entstünde eine geneigte „Glaswand“ ohne freien Strahl und
  ohne Luft dahinter; dort braucht es Vorhang und Aufprallschaum.
- **Schaumobjekte** (Aufprallteppich, Schaumstraßen, Kehrwasser) nur bei `vorhang: true`; sonst `schaum: "simulation"`,
  `schaum_objekte: []`. Die Niagara-Effekte (`effekte`) bleiben an allen Fällen.

**Überspannende Objekte (16a Entscheidung 5).** `lage = im_wasser` und Unterkante > Spiegel + 0,1 m → keine
Wasser-Kollision, Eintrag in `ohne_wasser_kollision` mit `grund: "ueberspannt"` (die Erfassung von oben machte daraus
einen Damm). Für `lage = ufer` bleibt + 0,5 m.


## Fingerabdruck (Back-Liste)

**v8:** Die SWR-Einstellungen (`sim_vorgaben` je Eintrag der Back-Liste: Auflösung, `match_spline*`,
`remove_outside_spline_amount`, `source_size_cm`, `sim_speed`, `num_steps`, `use_capture`) gehören nicht zur Formel. Weicht
eine davon vom Stand beim letzten Backen ab, gilt die SWR ebenfalls als „neu backen“.

Je **SWR-Bereich** (v3; v2: je Einheit, v1: je Kachel) legt ein SHA-256-Fingerabdruck fest, was die Simulation dort sieht. Das
lokale Werkzeug backt nur SWR neu, deren Fingerabdruck sich gegenüber dem letzten Backen geändert hat. Die Formel ist
unverändert (`FLUSS_SIM_FP1`); bezogen wird sie auf `bereich_cm` des SWR-Bereichs (Rechteck + 8 m Rand) und auf die
Splinepunkte `punkt_index` [i0, i1] des **einen** `WaterBodyRiver` (`S|WBR_<gewaesser>|n`, n = i1 − i0 + 1). Die Funktionen
`fp_gelaende_text`, `fp_splines_text`, `fp_objekte_text` und `fingerabdruck` in `fluss_sim_export.py` sind die
Referenz; sie brauchen nur `hashlib`, `math` und NumPy und laufen auch im Unreal-Python.

Quantisierung überall `q(v, s) = floor(v / s + 0,5)` (ganzzahlig, kein Banker's Rounding). Texte ASCII, Zeilen mit
`\n` getrennt, letzte Zeile mit `\n` abgeschlossen.

1. **Gelände** – Abtastpunkte = Pixelmitten des Planrasters in `bereich_cm` (Rand inklusive):
   lokal 1 m mit x = j − 4730,5 m, y = i − 4060,5 m; in der Cloud 2 m mit x = 2j − 4730 m, y = 2i − 4060 m.
   Höhe = Gelände nach allen Stempeln (Welt + 1-m-Deltas der Planer) bzw. im Editor die Landschaftshöhe an genau
   diesen Punkten.
   ```
   G|r=<raster_cm>|x0=<q(x0_cm,1)>|y0=<q(y0_cm,1)>|nx=<nx>|ny=<ny>|q=5
   <q(h,5) für x aufsteigend, mit Komma>      ← eine Zeile je y, y aufsteigend
   ```
2. **Splines** – die Punkte i0 … i1 des Flusses (v1/v2: je Abschnitt bzw. Einheit, sortiert nach ID):
   ```
   S|WBR_<gewaesser>|<anzahl punkte>
   <q(x,1)>,<q(y,1)>,<q(z,1)>,<q(RiverWidth,1)>,<q(Depth,1)>,<q(Velocity,1)>   ← je Splinepunkt in Reihenfolge
   ```
3. **Objekte mit Wasser-Kollision**, deren gedrehte Bounds `bereich_cm` schneiden, je eine Zeile, die Zeilen als
   Text sortiert:
   ```
   O|<netzpfad>|q(x,1)|q(y,1)|q(z,1)|q(qx·10000,1)|q(qy·10000,1)|q(qz·10000,1)|q(qw·10000,1)|q(sx·1000,1)|q(sy·1000,1)|q(sz·1000,1)
   ```
   Quaternion normiert und kanonisch: das erste von 0 verschiedene Element in der Reihenfolge qw, qz, qy, qx ist
   positiv (q und −q sind dieselbe Drehung).
4. `teil = sha256(text).hexdigest()` je Teil, **Fingerabdruck =
   sha256("FLUSS_SIM_FP1\n" + gelaende + "\n" + splines + "\n" + objekte + "\n").hexdigest()**.

**Beispiel** (Format unverändert seit v1: ein 3 × 2-Raster bei 1 m, eine Spline mit 2 Punkten, ein Fels):

```
G|r=100|x0=-172182|y0=-239417|nx=3|ny=2|q=5
2041,2041,2041
2040,2041,2041

S|BEISPIEL_A00|2
-172182,-239417,10206,2879,70,300
-172263,-239173,10166,2785,70,300

O|/Game/Megascans/3D_Assets/NordicBoulder/SM_NordicBoulder_01|-172819|-238622|9796|-2397|-1871|1287|9439|347|347|347

gelaende d9ed1638941691faf8ceea836ff5839c862d5b1df8b2dd03cf111c069be66efd
splines  e16deb08d1ec274db38a11934bfe52e6d79a44137388df79804edaf25af0076e
objekte  e8316276836cdc46b521a41235aa6c31889f4aec5a58c56cdf413c0991e198ea
gesamt   afb13e88e9db310d08eadd51b6d036af7646ff5fb08916b46c28600d78cfa2c9
```

(Eingaben: Höhen 10203,7/10204,9/10206,2 und 10201,1/10202,6/10204,0 cm; Splinepunkte
[−172182,5; −239417,0; 10206,1; 2879,3; 70,4; 300] und [−172263,2; −239173,4; 10166,2; 2784,6; 69,5; 300]; Fels
x/y/z −172818,7/−238622,3/9795,7, q (−0,239743; −0,187143; 0,128668; 0,943899), Skala 0,3468.)

**Handänderungen im Editor.** Das lokale Werkzeug rechnet je SWR-Bereich aus `back_liste.json` (`bereich_cm`) dieselbe
Formel aus dem **Editor-Zustand**:
- Gelände: Landschaftshöhe an den Rasterpunkten (z. B. `Landscape.get_height_at_location` bzw. Line Trace auf den
  Kanal der Landschaft) auf dem 1-m-Raster.
- Splines: der `WaterBodyRiver` des Gewässers (Label `WBR_<gewaesser>`), Splinepunkte i0 … i1 in Weltkoordinaten mit `RiverWidth`,
  `Depth`, `WaterVelocityScalar` aus den Spline-Metadaten.
- Objekte: alle Akteure mit Tag `SWR_Hindernis` **und** alle Instanzen der `WH_…`-Akteure, deren Weltbounds den Bereich
  schneiden – auch die von Hand gesetzten Felsen. Netzpfad ohne `.Objektname`-Suffix.

Es vergleicht immer gleich mit gleich: den Editor-Fingerabdruck beim letzten Backen (gespeichert je SWR-Bereich) mit dem
aktuellen Editor-Fingerabdruck, und den Planer-Fingerabdruck dieser Liste mit dem der vorigen Liste (neue
Planung). Planer- und Editor-Wert sind wegen Landschafts-Quantisierung (16 bit) und Interpolation nicht
zwingend gleich; ein Unterschied an einer Rundungsgrenze löst höchstens ein unnötiges Neu-Backen aus. Die Teil-Hashes
zeigen, was sich geändert hat.

## Prüfer

`fluss_sim_pruefen.py` prüft (FEHLER, wenn nicht anders gesagt):
- **Ein Fluss je Gewässer:** `water_body.id` = `WBR_<gewaesser>`, global eindeutig; jede SWR nennt genau ihn als Quelle und
  Senke; jeder Welt-Lauf in genau einem Gewässer, mit `--daten2m/--daten1m` kommen alle Läufe aus `wasser_welt.json` und
  `baeche_alle.json` vor; Läufe hintereinander von 0 bis `laenge_m`.
- **Spline durchgehend und monoton:** ≥ 2 Punkte, Felder gleich lang, s steigend 0 … `laenge_m`, kein Grundriss-Sprung,
  Abstand ≤ 2 × Ziel (außer Lippe → Fuß), z nie steigend, Breite/Tiefe > 0, Tempo 0–1024 cm/s (16e: siehe unten), Stufenpunkte `LINEAR`,
  Becken-Punkte flach (≤ 3 %) und auf dem Becken-Spiegel (± 2 cm).
- **Jede Stufe hat Lippe und Fuß:** Punkt-Index gültig, Rolle, s ± 6 cm, z = Ober- bzw. Unterwasser ± 2 cm. Mit
  `--gefaelle/--sehens` werden die Stufen je Lauf aus der Quelle neu gezählt (Höhen ± 2 cm, s, Fall-Einträge); entfallene
  Stufen nur im gekürzten Teil eines Laufs.
- **Bereiche und Abdeckung:** Bereiche + Fälle lückenlos; jeder Bereich liegt in der Vereinigung der Simulationsbereiche;
  `swr_bereiche` je Bereich stimmt.
- **SWR:** Kette 0 … `laenge_m`, Überlappung je Naht, keine Naht an einer Stufe; Rechteck/Achse aus den Splinepunkten
  `punkt_index` neu gerechnet; `resolution_max_axis` Vielfaches von 32 in [32; **2048**] und = Regel; **Zelle ≤ Höchstzelle
  + 0,005 m** (Bach 0,30, ungeteilt 0,40 (16e), Fluss 0,35); geteilt nur, wenn das ganze Rechteck nicht passt (HINWEIS je geteiltem Gewässer).
- **Mündung:** Art bekannt; Mündungspunkt = Spline-Ende; Fluss/Bach: Ziel existiert, `ziel_s_m` im Ziel, Punkt im
  Wasserstreifen des Ziels (+ `luecke_m` + 5 m), Eintrag in dessen `zufluesse`; See bekannt (Welt bzw. Sehens);
  `offen` und Lücken als HINWEIS.
- **Fälle, Vorhang, Schaum, Kollision, Hindernis-Akteure (je SWR), Back-Liste mit Fingerabdruck** (Splines, Objekte und mit
  Daten auch Gelände neu gerechnet), **Determinismus** (`--vergleich`: alle Dateien byte-gleich) wie v2.
- **16f Rückfrage (v8):** SWR-Startwerte (`match_spline`, `match_spline_height_amount`, `remove_outside_spline_amount`,
  `sim_speed`, `num_steps` = Regel, `num_steps` ≥ `sim_speed`, `source_size_cm` = Breite am ersten Punkt), `sim_vorgaben` der
  Back-Liste = SWR; Hindernisse: `ausdehnung_m` neu gerechnet (± 1 mm) und ≥ 0,4 m. Gegenproben (alle FEHLER, Exit 1):
  Nachfüllrate 2, `source_size_cm` 1000, `ausdehnung_m` 0,3, Back-Liste `remove_outside_spline_amount` 200, `num_steps` 5,
  Regel 0,5 m (167 FEHLER: Objekte 0,4–0,5 m).
- **16c Nachtrag 4, Hindernis-Akteure:** je `WH_…` höchstens 4 000 Instanzen je Komponente und 128 Komponenten
  (FEHLER), `n_komponenten` = Liste, geteilte Netze mit `teil` 1 … n; HINWEIS mit den größten Werten und den Akteuren über
  16 Komponenten.

- **16d:** Pool und Gelände nur aus Lauf-Plänen (wie Export); Gelände ohne `back_liste.gelaende.deltas_ohne`, Erkennung
  heute anders = WARNUNG; Töpfe (Bereich `topf`, Splinepunkte auf dem Spiegel ± 3 cm, SWR-Rechteck schließt den Topf
  ein, < 30 m, nur in einem Gewässer, kein See-Ziel mehr, `water_body_lake: false`); Läufe + Töpfe lückenlos;
  Vorschläge (am Spline-Ende, z nie steigend, Abstand ≤ 5 m, `laenge_m`, Ziel erreicht, gleich `vorschlaege.json`).

- **16e:** Tempo: `tempo_ms` und `tempo_info` je Punkt, `WaterVelocityScalar_cm_s` = `tempo_ms` × 100, im Rahmen
  [`tempo_faktor` × 0,1; `tempo_faktor` × 2,5] m/s, Änderung ≤ 0,6 m/s je m, nachgerechnet mit `tempo_regel`
  (± 0,0015 m/s); global steigt das Median-Tempo je Gefälleklasse (< 1 %, 1–5 %, 5–15 %, > 15 %), flache Becken im
  Median ≤ 0,3 m/s, steile Rinnen ≥ 1,0 m/s (je × `tempo_faktor`); Rangkorrelation Tempo/Gefälle je Gewässer < 0,3 =
  HINWEIS. Schaum-Maske: genau eine Kapsel je Vorhang-Fall, keine an anderen Fällen, s ab Fuß bis ≤ 6 m, Radius und Stärke
  in den Grenzen; mehr als 8 = HINWEIS. Bach-Zelle: ungeteilt ≤ 0,40 m (> 0,30 m = HINWEIS), Teilstücke ≤ 0,30 m,
  `zelle_max_m` = Regel.

Gegenproben (F_ERLENBACH verfälscht), alle FEHLER mit Exit 1: steigende Spline, Stufe ohne Fußpunkt, Fußpunkt auf
Oberwasser, Lücke zwischen SWR-Bereichen, Auflösung 4096, Zelle 0,45 m (Auflösung 1024), zweiter Fluss als Quelle, Lauf
doppelt, Naht an einem Fall, Grundriss-Sprung. 16d (Elfentreppe, `B_R_M2_M2_01`, `B_R3_K10_TUNDRA_01`, Karsee): Topf
nicht auf dem Spiegel, Topf ≥ 30 m, Rechteck ohne Topf, Topf ohne Bereich, Topf als `WaterBodyLake`, Mündung in einen
Topf als See, Vorschlag steigt / beginnt nicht am Ende / Abstand 8 m / Ziel verfehlt / fehlt, `vorschlaege.json` weicht ab.
Gelände: Fingerabdruck mit gebautem Lauf, aber Welt ohne Stempel → FEHLER.

- **v10 (16g Nachtrag):** `water_info` und `wasserzonen.json` neu gerechnet, Regel je vorgeschlagener Zone, `--zonen`
  (siehe „Ergänzungen 16g Nachtrag“). Gegenproben (alle FEHLER, Exit 1): `water_info.pixel_max_m` von Hand 0,5
  (2 FEHLER), `WZ_F15` auf 2048² (19 FEHLER), `water_zone_vorschlag` von `F_ERLENBACH` auf `WZ_WELT` (1), `water_info`
  entfernt (1); `--zonen zonen_beispiel_c2.json` (C2 1024): 7 FEHLER, mit 4096: 0 FEHLER (je 2 WARNUNG: Bett ragt aus
  der angenommenen Lage der Zone).

- **v11 (16g Nachtrag 2):** SWR-Vorgaben v11, `source_size_cm` ≥ 300, Hindernis-Filter nachgerechnet (siehe „Ergänzungen 16g
  Nachtrag 2“), `--zonen` mit `half_precision`. Gegenproben (alle FEHLER, Exit 1): gefilterter Randfels zurück in
  `wasser_kollision` (4 FEHLER), `quer_im_bett_m` auf 90 % der Breite (5), `filter_teil` als `filter_meter` (1),
  Nachfüllrate 0,02 (2), `source_size_cm` 200 statt 300 (2); C2 mit `half_precision: true` → 1 WARNUNG (16 cm Stufe).

## Grenzen

- **2-m-Daten:** Längen, Tiefen und Gelände-Fingerabdrücke stammen aus dem 2-m-Raster; lokal auf 1 m neu exportieren.
- **Breiten (v10):** Die Plan-Breiten der 2-m-Daten sind oft breiter als das lokale Bett (Erlenbach C2: 2 m: ≥ 12,7 m,
  lokal 1,6–2,4 m). `water_info` und `wasserzonen.json` deshalb lokal auf 1 m neu rechnen; erst dann gelten die Zonen.
- **Andere Ebenen:** Felsen anderer Ebenen (Bestand, Felsgruppen) findet erst der lokale Lauf.
- **Mündungen mit Lücke** (`luecke_m`, 23) und **offene Enden** (24) sind Lücken in den Weltdaten (Bach endet 25–700 m vor
  dem nächsten Wasser oder tiefer als der Fluss daneben); die Spline wird nicht erfunden. Die Vorschläge (16d) stehen
  getrennt daneben und sind lokal zu prüfen (2-m-Gelände, 4-m-Suchraster).
- **Geteilte Simulation** (8 Gewässer): Der gemessene SWR-Bereich ist das Rechteck um den Quell-Fluss; zwei SWR mit
  demselben Fluss decken ohne eigene Begrenzung beide das ganze Rechteck ab. Begrenzung und Naht lokal testen (16c).
- **Überlappende Gewässer:** Sehens-Bäche, die einen Bestandsbach ersetzen (`heide_06` → `B_R2_R_P3_P0_01`), stehen weiter
  als zwei Gewässer an derselben Stelle.
