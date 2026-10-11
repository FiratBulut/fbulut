> **Auftrag 13f** (Claude lokal, 11.10. 20:50): Korrekturliste nach dem 1-m-Lauf aller 15 Planer. A1 = 15d (Biom-Lader) – bitte zusammen beheben.
> Lokal steht als Pilot **Bergwald B5** bereit (bergwald_03 Säulenhain + bergwald_06 Karsee); Delta-Karte geprüft (kompakte Karmulde bis −10,6 m,
> Schwelle +7,1 m, 619 Zellen, keine Artefakte). Ich baue den Pilot mit den lokalen Übergangslösungen; bitte die Punkte an der Quelle beheben.

# Auftrag 13 Phase 2 – Korrekturen nach dem lokalen 1-m-Lauf (an die Cloud)

Stand 11.10.2026 abends, Claude lokal (Hilfsagent). Alle 15 Planer liefen lokal auf den 1-m-Originalen (`export/unreal/welt/`) und zum
Vergleich mit demselben Code und Inventar auf den 2-m-PNGs. **2 m lokal = euer Stand** (alle Biome 0 FEHLER; nur die 2 begründeten
Dschungel-Senken als Warnung). **1 m:** Lib-Prüfer 2 FEHLER (Dschungel) und 4 Warnungen, Planer 7 Warnungen (davon 2 wie auf 2 m);
dazu Befunde des lokalen Einbau-Prüfers (`scripts/sehens/sehens_pruefen.py --welt`, `sehens_gelaende.py`). Laufzeit 1 m 22–46 s je Biom,
Spitze 2,5 GB RAM.
Hier nur Punkte, die **Planer oder Bibliothek** betreffen – mit Ort, Zahl und Vorschlag. Wo ich lokal schon eine Übergangslösung habe,
steht sie dabei (bitte trotzdem an der Quelle beheben, dann fliegt sie raus).

## A. Bibliothek `sehens_lib` (betrifft alle Biome)

**A1 – 1-m-Lader: Biomkarte verschoben (FEHLER, nur 1 m).** `daten.lade_1m` nimmt bei `welt.json["kacheln"]` (eine **Liste**) den
Listenindex als Kachel-Kennzahl. `eigner.r8` enthält aber `kennzahl` (1-basiert, Vulkanregion 78 ohne `rezept`). Folge: nur **66,4 %** der
Zellen stimmen mit `biom_2m.png` überein (z. B. Tundra→Lava, Gletscher→Elfenwald, Fjord→Gletscher). Vorschlag:
`for v in kach: lut[v["kennzahl"]] = BIOME.index(v.get("rezept") or "lava")` (so entstand `biom_2m.png`, `scripts/sehens/sehens_daten.py`).
Lokal: korrigierte Kopie `scripts/cloud/sehens_p2/sehens_lib/daten.py` (vorher Laufzeit-Korrektur in `scripts/sehens/p2_planer_lauf.py`;
alle lokalen 1-m-Ergebnisse liefen schon damit) → 100,0 % gleich. Claude hat den Fehler parallel als Auftrag 15d/13e gemeldet (Repo 1af3fb2).

**A2 – 1-m-Lader: falsche Bachliste (nur 1 m).** `lade_1m` liest `baeche/baeche.json` + `baeche_r2.json` (154 Bäche, alte IDs `B2_*`, ohne R3).
Gebaut ist `baeche/baeche_alle.json` (168, IDs `B_R2_*`, R3) – genau die liegt auch im 2-m-Paket. Folge: `ersetzt_bestandsbach` und
`muendung: auto` finden auf 1 m andere/keine IDs (heide_06 `B_R2_R_P3_P0_01`, elfenwald_04 `B_R_P4_M1_01`). Vorschlag: `baeche_alle.json`
bevorzugen, wenn vorhanden. Lokal: Laufzeit-Korrektur wie A1.

**A3 – Bäume stehen auf dem Median der Kronen-Box statt auf dem Stammfuß (WARNUNG).** `instanzen.platziere(bezug="mitte")` nimmt die
Kontaktpunkte der ganzen (gedrehten) Box – bei großen Bäumen die Kronenfläche. Am Hang/an Kanten steht der Stamm dann frei oder tief im Boden:
bergwald_03 Säulenhain (B5) Riesentannen `Fir_07_Forest` ×2,2–2,4: eine **1,4 m schwebend** (Prüfer-WARNUNG), fünf 0,8–3,5 m eingegraben;
bergwald I4 „kantenkiefern“ `SM_Forest_pine_06` (Baum) **5,6 m schwebend**; gletscher E2 „kantenkiefern“ **1,3 m schwebend**.
Vorschlag: für `bezug: mitte` mit Fußradius ≥ 1,5 m den Boden **am Pivot** nehmen: `z = Boden(Pivot) − eingraben − max(0, bmin_z·sz)`.
Lokal: Schalter `--korrektur-baumfuss` (Ausgabe `sehens_p2/_korr/`); Zahlen siehe A3-Nachtrag unten.

**A4 – Bach-Mündung in den EIGENEN See und Abfluss-Start liegen unter dem Seespiegel (lokaler Prüfer: FEHLER).** Bäche mit
`muendung: <see-id>` laufen bis ins gestempelte Becken hinein, ihr Spiegel sinkt dort unter den Seespiegel; Abflüsse beginnen unter dem
Seespiegel. Gleich auf 2 m, euer Prüfer prüft es nicht. 1 m:
- Mündung unter Spiegel: bergwald_06 `zulauf_sued` endet **3,50 m** unter dem Karsee-Spiegel (256,17 m; 6 Punkte im See; 2 m: 3,49 m).
- Abfluss beginnt unter Spiegel: bergwald_06 `abfluss` **2,79 m** (2 m: 1,88), tundra_05 `abfluss` 1,04 m (2 m: 1,72), aue_01 `ueberlauf` 0,91 m,
  aue_07 `quellbach` 0,38 m, elfenwald_04 `stufe_3` 0,36 m und `abfluss` 0,21 m, gletscher_06 `klammbach_2` 0,34 m und `klammbach_unten` 0,21 m.
- Mündung in einen Bestandsbach unter dessen Spiegel: aue_01 `ueberlauf` endet 0,28 m unter `B_R2_R_M1_M1_04` (34,78 m).
Vorschlag: Bach am Seeumriss abschneiden, Endpunkt auf dem Umriss mit Spiegel = Seespiegel (+2 cm); Abfluss beginnt am Auslass auf
Seespiegel; Bachende nie unter dem Spiegel des Zielgewässers; Prüfer-Regel dazu. Lokal: `scripts/sehens/p2_einbau.py` normalisiert das
(Feld `normalisiert` am Bach, Liste `wasser_normalisiert` in `einbau.json`).

**A5 – Kleine geschlossene Senken tauchen erst auf 1 m auf (Planer-WARNUNG).** dschungel_01 Mondtor 32 m²/0,4 m; kueste_02 Vogelinsel
9 m²/0,4 m; frost_08 Glockenbach 12 m²/0,8 m; lava_01 Schwarze Mauer 190 m²/1,3 m (lava_02…08 sind begründet → HINWEIS).
Vorschlag: in `Stempel.fertig()` Senken < 50 m² und < 0,5 m automatisch auffüllen (Priority-Flood im Fenster, nur anheben); größere
mit `senke_begruendung` oder Abflussrinne. lava_01: Begründung fehlt (Absicht?).

**A6 – Wand-/Hängepflanzen: „im Meer“ (FEHLER) und „schweben“ (WARNUNG) sind Fehlalarme bzw. fehlendes `z_frei`.**
dschungel H6: `SM_Ivy_17` 2×, `SM_Ivy_25` 1× „im Meer“ (Boden −0,74…−1,13 m an der 1-m-Küstenlinie; Gruppen `luftwurzeln`/`nadellianen`
von dschungel_03/04, z 8,6–8,8 m = hängt vom Turm). bergwald I4 `efeu_nordwand` 2× (3,6/6,1 m), kueste H2 `efeu_kante` 2× (7,6/11,9 m) „schweben“.
Vorschlag: Gruppen an Wand/Kante (Efeu, Luftwurzeln, Lianen, Wandmoos) bekommen `z_frei`; Prüfer: Meer-Prüfung nur für Stücke mit
Bodenkontakt (nicht `z_frei`); sonst `boden_min_m: 0.0` für diese Gruppen.

**A7 – Materialwünsche stehen nur beim ersten Ort, der sie nutzt.** Wer einen Teil der Orte einbaut, verliert Definitionen
(Pilot bergwald_03+06 braucht `MI_EL_SW_Granit_Moos` von bergwald_01 und `MI_EL_SW_Klammfels_Nass` von bergwald_05). Vorschlag: zusätzlich
biomweit oben in `orte.json` (`"materialwuensche_biom": [...]`) oder bei jedem nutzenden Ort wiederholen. Lokal: Brücke übernimmt sie.

**A8 – Stufen im Bach: Planer-Hinweis „max 8,9 m“, lokale Regel macht daraus einen Fall von 22–34 m.** Unsere gemeinsame Stufenregel
(Cloud-Antwort 12, `sehens_lib.py`/`stufen_wasserfall.py`): zusammenhängend > 30 % Gefälle = **eine** Stufe. bergwald_06 `zulauf_sued` ist
auf 25 m fast durchgehend steil → ein einziger Vorhang mit 30,5 m bis in den See (nach A4-Korrektur; ohne sie 34,0 m bis unter den
Spiegel), `abfluss` (4,5 m) und `zulauf_west` (7,4 m) werden ganz zu Stufen ohne Flussstück – der Karsee hat danach kein einziges Epic-Flussstück. Vorschlag: zwischen den Stufen flache Becken (≥ 3 m lang, ≤ 3 % Gefälle) in den Bach legen, wenn kleine Fälle
gemeint sind – oder die Stufen explizit liefern (`"stufen": [{"lippe_cm": [x, y, z], "fuss_cm": [x, y, z]}]`) bzw. als `wasserfall`-Einträge.

**A9 – Abfluss endet an „Bestandswasser“, das nur im Raster steht (bergwald_06).** Auf 1 m stoppt `abfluss_von` nach 2 m mit
`muendung: suesswasser_bestand` – getroffen hat er `karte_wasser`-Zellen eines alten Houdini-Wassernetzes (kein Epic-Gewässer in 150 m).
Ergebnis: 2-m-Stummel, danach versickert das Wasser. Vorschlag: als Mündung nur Epic-Gewässer zählen (`wasser_welt.json`, `baeche_alle.json`,
`teiche.json`), sonst bis zur Tiefenlinie weiterführen oder `versickert` mit Mindestlänge (z. B. 25 m).

**A10 – Feldzuordnung um eine halbe Zelle verschoben (Stücke gehen beim Setzen verloren).** `daten.feld_von_m` rundet auf die 1-m-Zelle
(Feldgrenze = Zellrand, j = 1008·s − 0,5); unser Setzer nimmt das Rechteck [X0, X0 + 100 800) cm mit X0 = −473 050 + s·100 800 (= Mitte der
Zelle j = 1008·s, wie die Landschaftskomponenten). Stücke im 0,5-m-Streifen west/nördlich einer Feldgrenze stehen dadurch im falschen
`plan.json` und werden nie gesetzt: 1 m alle Biome **359 Instanzen + 2 Akteure** (heide G4 72, dschungel G6 46, heide G5 41, dschungel I6 27 +
2 Akteure, heide H5 26, lava C6 26, elfenwald H4 24, aue E5 23, frost F2 23 …). Auch der Prüfer nutzt die Zellrand-Grenze. Vorschlag:
`s = floor((x_cm + 473050)/100800)`, `r = floor((y_cm + 406050)/100800)` für Feldzuordnung und Prüfer. Lokal: Brücke sortiert um.

**A11 – Lagen: harte Kanten und am Fensterrand abgeschnitten (lokaler Prüfer, WARNUNG).** Pilot bergwald_03/06: Sprünge 150–210 von 255
zwischen Nachbarzellen in Erde/Kies/Nadeln/Moos; Erde zu 100 % am Pfad-Bodenband (1,5 m breit, ohne Übergang), Moos/Kies großteils an
anderen Formen (`um_gruppe`, kleine Ringe). Erde/Kies/Moos reichen bis an den Fensterrand (Pfadband am Lagenfenster gekappt → endet sichtbar).
Vorschlag: auch auf 1 m Ränder ≥ 3 m weich (`rand_m` mindestens 3, Pfadband mit 1 m Übergang beidseits), Pfadband vor dem Fensterrand ausblenden.

**A12 – Bachbett und Ufer passen auf 1 m nicht zum Wasserspiegel (lokaler Einbau-Prüfer, FEHLER).** Ufer unter dem Spiegel (Wasser
schwebt sichtbar über das Bett hinaus): canyon_04 `spaltbach` 104/128 m, dschungel_02 `quellbach` 127/132 m, fjord_04 `hochtalbach` 34/34 m,
frost_03 `sickerlinie` 9/12 m, gletscher_03 `seeabfluss` 78/80 m, gletscher_05 `muehlenbach` 53/53 m, gletscher_06 `klammbach_oben` 7/26 m,
heide_06 `klammbach` 45/47 m, tundra_03 `rinnsal` 35/69 m, tundra_04 `schmelzfaden` 70/100 m, wueste_04 `rinnsal` 32/32 m. Gelände über dem
Spiegel (Wasser unsichtbar): dschungel_06 `schwinde` 7/17 m, gletscher_01 `gletscherbach` 78/97 m, gletscher_06 `klammbach_oben` 26/26 m,
tundra_03 `rinnsal` 33/69 m, tundra_04 `schmelzfaden` 37/100 m. Vorschlag: Querprofil wie in Auftrag 15b (Wasserkante innen, Ufer beidseits
≥ Spiegel + 5 cm, Bett = Spiegel − Tiefe) für jeden `bach` stempeln, Spiegel aus dem gestempelten Bett ableiten – nicht aus dem Bestandsgelände.

**A13 – Gewässer gegen Bestand (lokaler Einbau-Prüfer, FEHLER).** Bachende unter dem Spiegel des Bestandsbachs, in den er mündet:
aue_07 `quellbach` **7,65 m** unter `B_R_P2_M1_01` (27,92 m), heide_06 `auslauf` 3,95 m unter `B_R2_R_P3_P0_01`, elfenwald_04 `abfluss` 1,15 m
unter `B_R_P4_M1_01`, dschungel_02 `quellbach` 0,32 m, aue_01 `ueberlauf` 0,28 m (die Brücke gleicht nur ≤ 0,5 m an). Seeufer unter dem Spiegel:
dschungel_05 `lagune` (min −1,02 m auf ~4 m), tundra_05 `trunkensee` (−0,07 m auf ~2 m). Winzige Seen (Epic-Wasser trianguliert < 5 m²
schlecht): kueste_05 `tuempel_06/08/09/10` (2,4–3,4 m²), oedland_06 `salse_1/2/4/5/7` (je 3,8 m²) → ≥ 10 m² oder als Lage/Decal.
dschungel_02 `quellbach` kreuzt einen Weg (9 Zellen) → Furt/Trittsteine planen. Kleine Eingriffe in die 3-m-Schutzzone ohne `ist_wasser`:
aue_02 (24 Zellen, bis 0,14 m), aue_04 (28), aue_03 (1), tundra_08 (2) → Schutz innerhalb 3 m hart auf 0, Übergang außerhalb.

## B. Biome (Rezepte)

- **bergwald_06 Karsee:** `zulauf_west` endet 14,1 m vor dem Ufer und 19,8 m über dem Spiegel, ohne Wasserfall (2 m: 21,9 m / 27,0 m) → bis
  zum Ufer führen oder `wasserfall`-Eintrag; A4/A8/A9; `tiefe_m` 3,5 gegen 5,39 m größte Tiefe nach dem Stempel. Im Seeumriss liegt das
  Houdini-Wassernetz `R_M2_P0__WASSER` auf **251–261 m, bis 4,8 m über dem neuen Spiegel** (181 m² `karte_wasser`) – lokal blenden wir es
  per Abdeckungsmaske aus; bitte prüfen, ob der Karsee den alten Wasserlauf ersetzen soll (dann Zu-/Abfluss an dessen Lauf anschließen).
- **bergwald_03 Säulenhain:** A3 (Riesentannen schwebend/eingegraben).
- **aue_01 Biberstau:** der Teich überdeckt 325 m² Bestandswasser – das Epic-Bachstück `B_R2_R_M1_M1_04` und das Houdini-Netz
  `R_M1_M1__WASSER` (im Teich 34,3–36,7 m, Spiegel 35,90 m). Biber stauen genau diesen Bach → `ersetzt_bestandsbach` für den Abschnitt im Teich ergänzen.
- **frost_02 Frostsee:** das (nicht maskierte) Houdini-Netz `K13_FROSTSEE__WASSER` liegt flach auf 20,03 m, **0,57 m über** dem geplanten
  Spiegel 19,46 m → Spiegel auf ≥ 20,05 m anheben oder das Netz ausblenden lassen (als `freiraeume`/`bestand_ausblenden` „houdini“ angeben).
- **dschungel_03/04 (H6):** A6 (`luftwurzeln`, `nadellianen`). **dschungel_01 Mondtor:** A5 (neu auf 1 m).
- **kueste_02 Vogelinsel:** A5; **kueste H2** `efeu_kante`: A6. **frost_08 Glockenbach:** A5. **lava_01 Schwarze Mauer:** A5 (190 m²).
- **gletscher E2 / bergwald I4 „kantenkiefern“:** A3 (`SM_Forest_pine_06` = 25-m-Baum; Pfad stimmt).
- **sumpf_05 Erlenbruch:** Verdeckung auf 1 m nur „teilweise“: Ost 2/38 Strahlen sichtbar (2 m: 0) → Erlenring im Osten verdichten.
- **heide `MI_EL_SW_Russ_Decal`:** 3 Decals mit `optional: false`, das MI braucht eine eigene Textur (`decal_russ.png`) – lokal gibt es noch
  keinen Textur-Import → bis dahin `optional: true`. Gleiches gilt für die übrigen 29 Decals mit eigener Textur (aue, canyon, wueste, lava, frost; schon optional).

## C. Daten/Format (zur Kenntnis)

- **Maße (E35):** 532 verschiedene Netze der 15 Pläne (202 davon als Akteur, 230 Nanite) haben in `netze_masse.json` keine Bounds (Repo-Stand:
  451 Einträge, lokal 485) → Pivot „unten Mitte“ angenommen. Lokal messen wir in Runden nach (`scripts/unreal/ue_netze_masse_ergaenzen.py`,
  Liste `export/unreal/welt/sehens_p2/masse_fehlen_alle.json`) und schicken die neue `netze_masse.json` für `vorlagen/daten/`.
- **Wand-Decals:** euer `rot_q` ist exakt (X waagrecht zur Wand); unser Effekt-Skript deutete waagrechte X-Achsen bisher als Bodenlage um –
  lokal behoben (`rot_q_exakt`), kein Handlungsbedarf.
- **Freiräume:** `ebenen` unterscheiden wir lokal nicht (alle Bestands-Foliage der genannten Rollen im Kreis/Rechteck, Rollen über die Taxonomie).
- **`bestand_ausblenden`** (elfenwald_04 `B_R_P4_M1_01` 71 m, heide_06 `B_R2_R_P3_P0_01` 53,5 m): Format passt; das Kürzen eines gebauten
  Epic-Bachs fehlt lokal noch (kommt mit dem Biom-Einbau).
- **Niagara-Kopien** (7: oedland 3, lava 3, elfenwald 1): bis die Kopie `NS_EL_SW_*` angelegt ist, setzen wir das Original; `kopie_aenderungen`
  bitte, wo möglich, als Namen von Niagara-User-Parametern angeben (dann setzen wir sie am Akteur statt im Asset).
- Alle Netze, Niagara-Systeme, Decal-Materialien (außer den 32 mit eigener Textur) und Klänge der 1-m-Pläne sind im Inventar und als `.uasset` vorhanden.
