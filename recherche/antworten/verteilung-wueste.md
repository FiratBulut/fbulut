# Verteilung Biomgruppe 9: Wüste/Canyon/Ödland – Ergänzung (Velen-Ödnis, Toussaint-Trockenhänge, Schichtstufen-Canyon)

**Auftrag 11, Teil B9.** Biome `wueste`, `canyon`, `oedland`; Foliage-Präfix `FT_EL_WE_`, Ordner `/Game/Eldarien/Welt/Foliage/WuesteErgaenzung`,
Ebene `wueste_ergaenzung`. Stand 2026-10-10 (Fortsetzung nach API-Abbruch; Regeln und Planer-Entwurf des Vorgängers geprüft, korrigiert,
kalibriert und rauchgetestet). Lieferung: dieser Bericht, `skripte/wueste_ergaenzung_regeln.json` (23 Klassen, 166 Paletteneinträge, alle
gegen `netze.csv` geprüft, 0 fehlend; dazu `felsgruppen_overrides`, `spuren_overrides`, `mittelschicht_overrides`, `pruefkameras`,
`erwartung_je_feld`), `skripte/wueste_ergaenzung_plan.py` (Planer nach FORMAT §3/§5). **Alles UNGETESTET MIT ECHTDATEN** – in der Cloud nur
`py_compile` und Rauchtest mit synthetischen Rastern (D4, E6; §5). Web-Quellen waren nur als Suchmaschinen-Auszüge lesbar; solche Belege
sind mit **[Suchauszug]** markiert, Zahlen ohne Beleg mit **Richtwert**.

**Korrektur Runde 1 (10.10.2026):** Zuständigkeit strikt nach Biom-Zellen + 30-m-Saum, leerer `plan.json` bei < 2 %, Pflichtschlüssel §2, harte Budgets, Exit 2; generische Mittelschicht-Klassen jetzt als `mittelschicht_overrides` (Palette + Faktor statt `biom_faktor` 0), Geröllplatten/Terrassenkanten/Felsnadeln als `felsgruppen_overrides.zusatzklassen`, Knochen-Ersatz als `spuren_overrides.zusatzklassen` – Details im folgenden Abschnitt „Korrektur Runde 1“, der vor §1–§7 gilt.

**Felder.** Wüstenfelder mit eigenem Namaqualand-Planer (`FT_EL_WU_*`): C3, C4, D3, D4, D5, E3, E4, E5 → **nur ergänzen**, Budget
≤ 15 000, kein `entfernen`. Außerhalb davon volle Schichten 0/1/2/5: D6 (oedland 61 %), E6 (oedland 96 %), E7 (oedland 72 %, 13 % Land),
F6/F7 (oedland 4 %/3 %, nur Saum). Innerhalb eines Feldes läuft der Planer ausschließlich auf Zellen der drei Biome (`eigner.r8` +
`welt.json`; `wueste_namaqualand` wird als `wueste` erkannt), seit Korrektur Runde 1 mit 30-m-Saum nach außen (Landbezug, < 2 % → leerer Plan); Aue-, Tundra- und Lava-Anteile bleiben B2/B3/B8.

## Korrektur Runde 1 (10.10.2026): gilt vor allen folgenden Abschnitten

Grundlage: `auftraege/verteilung-korrektur-runde1.md` (lokaler Echtdaten-Test 10.10. 15:30) und `antworten/verteilung-KONVENTIONEN.md` §1–§6
(verbindlich). Geändert wurden nur `skripte/wueste_ergaenzung_plan.py`, `skripte/wueste_ergaenzung_regeln.json` und dieser Bericht. Wo §1 bis §7
etwas anderes sagen, gilt dieser Abschnitt. Das betrifft vor allem den 6-m-Saum, die Schicht-1-Tabelle, Geröllplatten und Knochen-Ersatz in
Schicht 0 sowie den Vorschlag `biom_faktor` 0 für die Mittelschicht.

**Echtdaten-Befund (Referenz, alte Fassung):** A5 (bergwald/fjord), G4 (elfenwald), E1 (gletscher 100 %) und C6 (lava 99 %) hatten je
**0 Instanzen**. Das ist korrekt, denn in keinem der vier Felder gibt es wueste, canyon oder oedland. Die Korrektur war trotzdem nötig, und zwar
aus drei Gründen. (1) Die Pflichtschlüssel aus §2 fehlten teilweise. (2) Die Saumlogik war ein 6-m-Box-Mittel statt eines 30-m-Saums auf
Landbezug. (3) Die Planer-Ebene setzte generische Mittelschicht-Klassen und Geröllplatten, die nach §4 anderen Planern gehören.

### Änderungen

| Punkt | Runde 0 | Korrektur Runde 1 |
|---|---|---|
| Biom je Zelle (§1) | `eigner.r8` + `welt.json`; unbekanntes Rezept → Feld-Fallback der Regeln | Kennzahl 0 → **aue**, Vulkan/Lava → **lava**, `rezept_alias` (namaqualand → wueste, badland/steppe → oedland, mesa/schlucht → canyon). Ein Rezept, das nicht erkannt wird, ergibt **aue** und eine WARNUNG. Nur wenn `eigner.r8`/`welt.json` fehlen, gilt das dominante Feldbiom aus `daten/biome_je_feld.json` (Hinweis), danach `feld_biom_fallback` |
| Zuständigkeit (§1) | `biom_faktor` je Biom, 6-m-Box-Mittel (verwischt die Kante nach innen und außen) | `zustaendigkeit.biome_eigen` = wueste, canyon, oedland. Eigene Landzellen haben Gewicht 1. Der **30-m-Saum** nach außen fällt linear 1 → 0 (Jump-Flooding-Distanz mit Quellzelle). Im Saum gelten die Regeln des **nächsten** eigenen Bioms, zwischen eigenen Biomen gibt es einen weichen Wechsel (6 m). Jitter-/Gruppenpunkte, die außerhalb der Zuständigkeit oder auf Sperrzellen landen, werden verworfen |
| Landbezug (§1) | alle Fensterzellen | `biome_fenster`, Eigenanteil und Saum beziehen sich nur auf Landzellen (ohne `karte_wasser`); `plan.json["biome_fenster_bezug"] = "land"` |
| Leerplan (§1) | Planung lief leer durch, `plan.json` ohne Teil der Schlüssel | Eigenanteil im Fenster **< 2 %** oder keine zuständige Feldzelle → sofort leerer `plan.json` (`instanzen` 0, `dateien` {}, alle Pflichtschlüssel, alte f32 gelöscht), eine Logzeile, Exit 0 |
| plan.json (§2) | `biome_fenster` über alle Zellen, `zellen_zustaendig` ohne Saum, `entfernen` nur außerhalb der Wüstenfelder | `biome_fenster` (Land, absteigend), `biome_fenster_bezug`, `zellen_zustaendig` (Feldzellen inkl. Saum), `biome_eigen`, `kollision_anzahl`, `entfernen` **immer** `""` (es wird nichts ersetzt, auch nicht in C3–E5), `dateien[].ebene` (0/1/2/5). Dazu `statistik.zustaendigkeit` (Quelle, Eigenanteil Fenster/Feld, Zellen eigen/Saum), `statistik.roh_vor_budget` und `overrides_geliefert` |
| Budget (§3) | proportionale Ausdünnung mit `min` der Faktoren, keine harte Grenze | Faktoren multiplizieren sich. Danach folgt eine **exakte Kappung** per Hash-Rang, niedrigste Priorität zuerst: hart 60 000 / Kollision 3 000 (Ziel 50 000), in den Wüstenfeldern 15 000 / 1 200. Jede Kürzung erscheint als `WARNUNG` in Log und `hinweise`; wird Schicht 0 gekürzt, folgt der Hinweis „Landschafts-Gras übernimmt“ |
| Ebenen (§4) | Schicht 1 mit 9 Klassen, Schicht 0 mit Zweigen, Knochen-Ersatz, Geröllplatten | Schicht 1 enthält nur noch **Sonderformen**: `dornstrauch` (Dornbusch-Ödland) und `sukkulent` (Sukkulenten-Polster, ohne Rooibos). Schicht 0 hat Kiesel, Steine **< 0,8 m** (Maßstab 0,8–1,25, SandstoneBoulder_03 max. 0,78 m), Trockenbett-Platten und Trockenlaub. Wandfuß-Faktor und Schuttsortierung von Kiesel/Stein sind auf 1,0/0 gesetzt, weil Schuttfächer und Geröllsaum Teil C gehören. Schicht 2 und 5 bleiben unverändert. **13 statt 23 Klassen** |
| Ergänzungsprinzip | C3–E5: `wuestenfeld_faktor`, `netze_wuestenfeld`, Budget 15 000 | unverändert: In den Wüstenfeldern wird nichts entfernt, Klassen mit Faktor 0 entfallen, die WU-Ebene gilt als belegt (`--wueste_ebene`) |
| Logs/Fehler (§5) | `SystemExit` (Exit 1), Umlaute in Meldungen, `netze.csv` optional | Alle `print()` laufen über `ascii_()`. Eine fehlende `hoehe.f32`, Regeldatei oder `daten/netze.csv`, eine Regeldatei ohne Block `zustaendigkeit` (Runde-0-Fassung) und ein ungültiges Feld ergeben jeweils eine `FEHLER`-Zeile und **Exit 2**. Die Netzpfade der drei Override-Blöcke werden gegen `netze.csv` geprüft und gemeldet |

### Entscheidung `mittelschicht_overrides`: Palette + Faktor statt `biom_faktor` 0

Runde 0 schlug `biom_faktor` 0 für wueste/canyon/oedland vor. Das widerspricht §4, nach dem `mittelschicht_plan.py` die **einzige** Quelle
der generischen Klassen ist. Weil die Planer-Ebene diese Klassen jetzt selbst nicht mehr setzt, hätten die gebauten Wüstenfelder C3–E5 und die
Ödland-Felder D6, E6, E7, F6, F7 gar keine Trockengras-Büschel, kein Totholz und keine Zweige mehr bekommen. Deshalb liefert B9 jetzt Palette,
Parameter und Faktoren. Die Runde-0-Klassen gehen dabei vollständig in die Mittelschicht über (`herkunft`, `herkunft_runde0` mit Lagen-Dichten
und Formfaktoren):

| Mittelschicht-Klasse | Palette (aus Runde-0-Klasse) | Parameter | Faktor oedland / canyon / wueste |
|---|---|---|---|
| `grasbueschel` | Tundra Grass Var A–I + Meadow dead_grass 01–03 (12; aus trockengras_hoch/niedrig/flach) | Gruppen 4–10 / 2,5 m, Maßstab 0,8–1,35, Hang ≤ 38°, Feuchte 1→2, Mulde ×1,6, Lagen Trockengras ×1,8, Sand ×0,4, Fels/Felsplatte ×0,5 | 2,4 / 2,7 / 1,2 |
| `strauch` | searsia burchellii small/medium, lucida a–d + wild_rooibos a–e (11; trockenhang_strauch + Rooibos aus sukkulent) | Gruppen 1–3 / 4 m, Hang ≤ 40°, Feuchte 1→2, Mulde ×1,4 | 0,3 / 0,33 / 0,2 |
| `totholz_liegend` | dead_log 01–04, OldFallenTree 01/02, Forest_pine_04/08_log, beach_driftwood_01 (9) | Gruppen 1–2, eingraben 8 cm, **Kollision**, längs Hang, Mulde ×2 | 2,5 / 3,0 / 1,9 |
| `totholz_stumpf` | pine_stump 01–03 | Gruppen 1–3 / 5 m, Wegrand ×1,5, Hang ≤ 32° (Vorlage heide) | 1,2 / 0,72 / 0,36 |
| `totholz_ast` | DryBranches 01–08, dead_quiver_branch 01/02 (10; aus zweige) | Gruppen 1–3, Sicht 50 m, Mulde ×1,6, an Totholz ×3 | 1,5 / 1,6 / 1,5 |
| `beere` | Mittelschicht-Palette (heath/heather) | – | 0,25 / 0 / 0 |
| `farn`, `jungbaum`, `hochstaude`, `pilz` | – | – | 0 |

**Kalibrierung.** Grundlage ist ein Lauf von `mittelschicht_plan.py` mit allen Faktoren 1 auf dem synthetischen Feld E6. Auf den oedland-Zellen
ergab das grasbueschel 8 336, totholz_ast 3 382, strauch 1 707, totholz_liegend 226 und totholz_stumpf 170. Die Ziele kommen aus den Runde-0-Zahlen
dieses Planers auf demselben Raster: Trockengras 29 827, Zweige 5 888, Totholz 613, Stümpfe 219, Strauch ~460. Gras ist bewusst auf ~75 % gesetzt,
weil kleine Büschel das Landschafts-Gras übernimmt (§3). canyon und wueste sind aus den Runde-0-Biomgewichten und den Grunddichten von
`mittelschicht_regeln.json` abgeleitet; canyon hat eigene, kleinere Grunddichten, wueste nutzt die oedland-Vorlage. Der Höchstwert ist 3,0.

**Gebaute Wüstenfelder C3–E5.** Dort gilt `faktor_je_feld`: grasbueschel 0,7, strauch 0,4, totholz_liegend 0,8, totholz_stumpf 0,4,
totholz_ast 0,6, beere 0. Zusammen mit `wuesten_feld_faktor` 0,5 der Mittelschicht wirkt das als **0,35 / 0,2 / 0,4 / 0,2 / 0,3 / 0** des
Werts außerhalb der Wüstenfelder, also im geforderten Bereich 0,2–0,4. Die Namaqualand-Ebene streut dort schon Sträucher und Sukkulenten,
deshalb ist strauch am kleinsten. Die Mittelschicht ergänzt vor allem Gras und Totholz, das der WU-Ebene fehlt.

### Override-Schema (alle drei Blöcke in `wueste_ergaenzung_regeln.json`)

```
"mittelschicht_overrides": {
  "gilt_fuer": ["wueste", "canyon", "oedland"],
  "vorlage_biom": {"grasbueschel": "oedland", "totholz_liegend": "oedland", "totholz_stumpf": "heide", "totholz_ast": "oedland", "strauch": "oedland"},
  "palette":   {klasse: [Pfade]},                 # 5 Klassen, 45 Netze
  "parameter": {klasse: {gruppe, radius_m, massstab, eingraben_cm, kippen, sichtweite, hang_max, feuchte, mulde, lagen_faktor, wegrand, an_totholz, kollision, laengs_hang}},
  "faktor":    {"farn": 0, "jungbaum": 0, "hochstaude": 0, "pilz": 0},
  "je_biom":   {"wueste": {"faktor": {...}}, "canyon": {"faktor": {...}}, "oedland": {"faktor": {...}}},
  "faktor_je_feld": {"C3": {...}, ..., "E5": {...}},   # Wüstenfelder, multiplikativ
  "herkunft": {...}, "herkunft_runde0": {...}, "begruendung": "...", "faktor_hinweis": "..."
}
"felsgruppen_overrides": {
  "biom_palette": {wueste/canyon/oedland: "sandstein"}, "klassen_faktor": {...}, "eingraben_anteil": [0.3, 0.45],
  "kiesel_ring": {netze, kiesel_dichte_je_m2},
  "zusatzklassen": {                                   # KONVENTIONEN §6
    "terrassenkanten": {palette (4), rolle fels_block, dichte_je_ha 83.3, hang_grad [0, 14], massstab [0.7, 1.2], eingraben_anteil [0.3, 0.45],
                        gruppe {groesse [1, 2], radius_m 3}, kollision, sichtweite [0, 60000], akteur false, biome {canyon 1, oedland 0.5, wueste 0.4},
                        abbruch_min_m 3, umkreis_m 6, abstand_m [6, 14]},          # letzte drei: felsgruppen-Erweiterung (Kantenstreifen)
    "felsnadel":       {palette (3), rolle fels_hero, akteur true, je_km2 [1, 3], kuppen_prominenz_min_m 12, max_je_feld 3, massstab [0.6, 1.1],
                        eingraben_anteil [0.25, 0.35], kollision, sichtweite [0, 0], biome {canyon 1, wueste 1, oedland 0.5}},
    "geroellplatte":   {palette ErodedRockyGround 01–03, rolle geroell_platte, dichte_je_ha 6, hang_grad [0, 18, 18, 32],
                        lagen {Geroell 1, Felsplatte 0.8, Sandstein 0.7, Fels 0.4}, zonen_faktor {fuss 3, wand 0}, fuss_breite_m 30,
                        massstab [0.8, 1.3], eingraben_anteil [0.3, 0.42], gruppe {groesse [1, 2], radius_m 4}, kollision false, sichtweite [0, 20000]}},
  "_vorschlag_teil_c": {schichtung, kippen_in_hang, wueste_felder_faktor 0.4, kiesel_ring_m}   # nicht gelesen, als Doku geführt
}
"spuren_overrides": {
  "gilt_fuer": [...], "palette": {"karren": [3], "stoppel": [2]},
  "faktor": {"wueste": {feld 0, obstgarten 0, kopfweiden 0, hecke 0, holzschlag 0, koehler 0, steg 0.5},
             "canyon": {feld 0.2, ..., holzschlag 0.3, steg 0.5}, "oedland": {feld 1, obstgarten 0, kopfweiden 0, hecke 0.3, holzschlag 0.6, koehler 0.4}},
  "zusatzklassen": {"knochen_ersatz": {palette bark_debris a–d + dead_log_05, rolle kleinzeug, dichte_je_ha 3.5, hang_grad [0, 30],
                                       massstab [1.0, 1.6], eingraben_anteil [0.1, 0.2], gruppe {groesse [2, 6], radius_m 1.4}, kollision false, sichtweite [0, 7000]}},
  "karren": {je_km_weg 2.6, anteil_schwer 0.5, kippen_grad, beiwerk, beiwerk_netze}, "brunnen": {...}, "galgen_ersatz": {bauteile ...},
  "steinmann": {...}, "graeber": {...}, "feldstreifen_verlassen": {...}, "blickziele_typ": {...}, "wueste_felder_faktor": 0.6
}
```

**Altstellen-Kompatibilität (felsgruppen).** In Runde 0 standen `terrassenkanten` und `felsnadel` direkt im Block. `felsgruppen_plan.py` las
sie als „Altstelle“ (siehe `verteilung-fels-organisch.md` h). Jetzt stehen sie unter `zusatzklassen`, mit denselben Werten. Beide Wege laufen
in felsgruppen über dieselbe Funktion `zusatz_lesen`, und bei gleichem Namen gewinnt `zusatzklassen`. Die alten Schlüssel sind entfernt, damit
nichts doppelt gelesen wird. `schichtung`, `kippen_in_hang`, `wueste_felder_faktor` und `kiesel_ring_m` las felsgruppen schon in Runde 0 nicht.
Sie stehen jetzt unter `_vorschlag_teil_c`, damit sie nicht mehr als „ignoriert“ gemeldet werden.

**Gegenprobe mit den Querschnitts-Planern (unverändert, synthetische Wurzel aus dem Rauchtest):**
- **mittelschicht_plan.py:** Der Block wird gelesen (palette, faktor, parameter, je_biom, faktor_je_feld, vorlage_biom), 0 unbekannte Schlüssel.
  In E6 ergeben sich auf oedland grasbueschel 20 583, totholz_ast 5 215, beere 773, totholz_liegend 620, strauch 525 und totholz_stumpf 199
  (Feld gesamt 29 308, Kollision 856). D4 (Wüstenfeld) hat 7 789 Instanzen, davon canyon 4 962 und wueste 1 523; die Quelle zeigt
  „wueste_ergaenzung x1.89“ (2,7 × 0,7) für canyon-grasbueschel.
- **felsgruppen_plan.py:** Gelesen werden 8 Schlüssel, ignoriert 0. Die Zusatzklassen terrassenkanten (16 Schlüssel gelesen / 0 ignoriert),
  felsnadel (11/0) und geroellplatte (15/0) sind ok. In D4 entstehen terrassenkanten 728 Instanzen (394 mit Kollision), felsnadel 3 Akteure und
  geroellplatte 25, in E6 112 / 1 / 5.
- **spuren_plan.py:** Alle Schlüssel werden umgesetzt (palette, faktor, zusatzklassen, karren, brunnen, galgen_ersatz, steinmann, graeber,
  feldstreifen_verlassen, blickziele_typ, wueste_felder_faktor). knochen_ersatz ergibt D4 361 und E6 286, dazu E6 1 Galgen-Ersatz, je 2
  Brunnen und je 14 Karren.

### Rauchtest Korrektur Runde 1 (synthetisch, Cloud: Python 3.13, NumPy 2.5, kein numba; Raster neu erzeugt, danach gelöscht)

Für den Test gab es eine Produktionswurzel im Scratchpad (`wueste_test`) mit vollen Rastern (memmap). Die Felder waren so aufgebaut:
- **D4** (Wüstenfeld): Canyon-Schichtstufen mit Rinne, Fluss, Weg und Ort. Im Westen canyon (Kennzahl 7), im Osten `wueste_namaqualand` (11),
  im Süden ein Streifen Weltgelände 0 (→ aue). Die WU-Ebene hat 3 000 Instanzen.
- **E6** (Ödland, außerhalb der gebauten Felder): Kuppen, Gullies, Teich, aue-Ecke im Nordosten und 200 Bestand-Bäume.
- **D6** (Mischfeld): oedland im Westen, `vulkanregion_asche` (→ lava) im Osten, mit gewellter Grenze.
- **G4** (Fremdfeld): elfenwald/heide.
Dazu kamen 9 Lagen, `welt.json`, `daten/netze.csv`, `biome_je_feld.json` und `netze_masse.json`. Aufruf:
`python -I -X utf8 wueste_ergaenzung_plan.py D4 E6 D6 G4 --wueste_ebene … --bild`.

| Feld | Instanzen | Kollision | Schicht 2 / 1 / 0 / 5 | biome_fenster (Land) | zellen_zustaendig (eigen + Saum) | Zeit | Runde 0, gleiches Raster |
|---|---|---|---|---|---|---|---|
| D4 Wüstenfeld | **4 158** (≤ 15 000) | 52 | 52 / 0 / 3 789 / 317 | canyon 0,527, wueste 0,309, aue 0,165 | 916 742 (887 655 + 29 087) | 6,5 s | 12 631 |
| E6 Ödland | **12 675** | 173 | 173 / 1 912 / 10 206 / 384 | oedland 0,804, lava 0,141, aue 0,056 | 917 469 | 5,8 s | 49 993 |
| D6 Mischfeld | **7 523** | 79 | 79 / 887 / 6 549 / 8 | oedland 0,5005, lava 0,4995 | 538 985 (508 562 + 30 423) | 4,3 s | 27 250 |
| G4 Fremdfeld | **0** (leerer plan.json) | 0 | – | elfenwald 0,765, heide 0,235 | 0 | < 1 s | 0 |

Zusammen mit der Mittelschicht (oedland-Anteil in E6 ~27 900) liegt E6 bei ~40 600 Instanzen über beide Ebenen; in Runde 0 waren es 49 993
in einer Ebene. Ein zweiter Lauf mit vorhandenen felsgruppen-, mittelschicht- und spuren-Ebenen, die dann als belegt gelten, ergab D4 3 986,
E6 10 840 und D6 6 656.

Folgendes wurde geprüft:
- **Schlüssel:** Alle Pflichtschlüssel (FORMAT §3 und KONVENTIONEN §2) sind in allen vier Plänen vorhanden. `instanzen` ist gleich der Summe
  der f32-Zeilen und gleich der Summe von `dateien[].anzahl`, `kollision_anzahl` ist gleich der Zahl der Instanzen in Dateien mit
  `kollision=true`, jede Datei hat `ebene`, `entfernen` ist `""`.
- **Zuständigkeit/Saum:** Der Abstand wurde unabhängig per Brute-Force je Instanz zur nächsten eigenen Landzelle gemessen. Auf fremden
  Biomzellen liegen in D4 63 Instanzen (0–10 m: 37, 10–20 m: 15, 20–30 m: 11), in E6 322 (168 / 115 / 39) und in D6 210 (121 / 71 / 18).
  **Jenseits von 30 m: 0** (Maximum 29,4 m). Im Prüfbild ist der Saum grau, fremde Biome sind abgedunkelt.
- **Sperrflächen/Format:** 0 Instanzen auf Wasser, Weg oder Ort; alle Instanzen liegen im Feld; 0 NaN; Quaternionen normiert (Fehler
  ≤ 1,2e-7); Maßstab ≥ 0,70; z zwischen −0,74 und +0,35 m zur Geländehöhe (Eingraben).
- **Determinismus:** Bei zwei Läufen sind alle 191 f32 byteidentisch (md5), und `plan.json` ist bis auf `stand`/`laufzeit_s` identisch.
- **Budget:** Mit `--faktor 6` wurde E6 von 65 979 auf **50 067** gekürzt (Kiesel ×0,57), D4 von 22 619 auf **14 933** (≤ 15 000), jeweils mit
  WARNUNG und Gras-Hinweis. Mit Testregeln (Kollision 100, hart 5 000) ergab E6 Kollision 142 → **exakt 100** und gesamt 10 798 → 4 934.
- **Fallback:** Ohne `eigner.r8` gilt `biome_je_feld.json`. D4 wird dann als canyon gelesen (4 719 Instanzen), E6 als oedland (12 677), G4 als
  elfenwald (leerer Plan); der Log enthält einen Hinweis.
- **Fehlerfälle:** Feld K9, fehlende `hoehe.f32`, fehlende Regeldatei, Runde-0-Regeldatei (ohne `zustaendigkeit`) und fehlende `netze.csv`
  ergeben jeweils eine `FEHLER`-Zeile und **Exit 2**.
- **Logs:** 0 Nicht-ASCII-Bytes in allen Logs (12 Läufe). `py_compile` ist ok, pyflakes meldet nur den optionalen numba-Import.

### Erwartung mit Echtdaten (`erwartung_je_feld`) und offene Punkte

A5, G4 und E1 ergeben einen leeren Plan, wie im Echtlauf. Auch C6 wird leer, es sei denn, oedland-Zellen aus D6 liegen im 64-m-Rand über
der 2-%-Schwelle. Dann bebaut der Planer nur den 30-m-Saum am Ostrand, mit höchstens einigen hundert Instanzen; die Zahl lässt sich an
`statistik.zustaendigkeit` prüfen. Für die eigenen Felder gelten die Runde-0-Spannen × 0,25–0,35:
- E6 10 000–17 000, D6 6 000–11 000, E7 1 000–2 500
- D4 3 500–5 500, E4 1 500–4 000, C4/D3/E3 700–2 500, D5 500–1 700, E5 200–800

Die Mittelschicht kommt jeweils dazu.

Offen sind drei Punkte:
1. Teil D liest den neuen Block bereits richtig. Die Faktoren sind aber nur synthetisch kalibriert und sollten nach dem ersten
   gemeinsamen Echtlauf (Reihenfolge felsgruppen → wueste_ergaenzung → mittelschicht → spuren) an E6/D4 gegen die Prüfkameras nachgestellt werden.
2. In `verteilung-STATUS.md` (Abgrenzung, letzter Absatz) ist der offene Punkt „wueste_ergaenzung biom_faktor 0“ damit erledigt; der
   Koordinator sollte die Zeile austauschen (die Datei liegt außerhalb dieses Auftrags).
3. `mittelschicht_plan.py` liest die Namaqualand-Ebene (`wueste/`) nicht als belegt. In C3–E5 können Mittelschicht-Sträucher (Faktor 0,2) also
   neben WU-Sträuchern stehen. Abhilfe wäre, `wueste` in die belegten Ebenen der Mittelschicht aufzunehmen (Teil D).

## 1. Referenzanalyse: was Velen-Ödnis, Toussaint-Trockenhang, Schichtstufen-Canyon und Steppe zwischen Boden und Krone füllt

**Velen (Kriegsödnis, Hangman's Tree).** Kacper Niepokólczycki (Lead Environment Artist Velen) nennt als Thema „Verzweiflung, Hunger,
Hoffnungslosigkeit nach langem Krieg“, Vorbild polnische Dörfer und ihr Umland; der Hangman's Tree wird als „very creepy sight“ hervorgehoben
([Vice-Interview](https://www.vice.com/en/article/designing-the-world-of-the-witcher-3-wild-hunt/), **[Suchauszug]**). Michał Janiszewski
beschreibt den Workflow: Silhouetten aus Realreferenzen, dann Vegetation mit **getrennten Pinseln je Geländetyp** (Feld, Wiese, Sumpf, Wald)
([80.lv World Building of Witcher 3](https://80.lv/articles/world-building-of-witcher-3), **[Suchauszug]**). Übertragen auf das Ödland heißt
das: nicht „weniger Aue“, sondern ein eigener Pinselsatz – gebleichtes Trockengras in drei Höhen, dürre Zweige und Laubnester, einzelne tote
Bäume als Silhouette auf Kuppen (Hangman-Motiv), Stümpfe als Spur von Holzschlag, Karren-Wracks am Weg. Aus den Zielbildern (`witcher_01`,
`witcher_05`, Analyse in `bildkritik-witcher-messlatte.md`) ergibt sich die Faustregel „kein Blick ohne Objekt 0,5–3 m in 10 m“ – im Ödland
erfüllt durch Dornstrauch, Totholz, Stumpf oder Grasbüschel-Insel, nicht durch Wald.

**Toussaint (Trockenhänge).** Die Erweiterung orientiert sich laut Niepokólczycki an Südfrankreich/Italien („warm sun, vistas filled with
vineyards“); Kuba Wichnowski nennt die Toskana als Hauptreferenz der Weinbergregion ([PlayStation-Blog](https://blog.playstation.com/archive/2016/05/10/how-the-witcher-3-team-built-the-land-of-toussaint-for-upcoming-expansion-blood-wine),
**[Suchauszug]**). Belege zu Zypressen oder Trockenhängen fanden sich nicht; die Regel „größere Sträucher 1,5–2,7 m auf Hängen 10–30° und
Terrassen, krumme Einzeleichen nur bei Restfeuchte“ (`trockenhang_strauch`, `einzelbaum_rinne`) ist deshalb **Richtwert** aus `witcher_06`
(Nadelbäume auf Simsen) und mediterraner Garrigue-Optik.

**Schichtstufen-Canyon.** Geomorphologisch bestimmt das Einfallen der Schichten die Großform: harte Bänke (Sandstein, Kalk) bleiben als
Steilstufen stehen, weiche Lagen (Tonstein) verwittern zu Böschungen dazwischen; am Wandfuß sammelt sich Schutt (Talus), und Pflanzen wurzeln
dort in den Lücken zwischen Blöcken, wo Abfluss gefangen wird ([Grand-Canyon-Landformen](https://www.grandcanyon.net/faults-and-landforms),
[NatureServe Colorado Plateau Canyon](https://explorer.natureserve.org/Taxon/ELEMENT_GLOBAL.2.722907/Colorado_Plateau_Mixed_Bedrock_Canyon_and_Tableland),
[NPS Mesa Verde](https://www.nps.gov/parkhistory/online_books/archeology/7b/chap3d.htm), **[Suchauszug]**). Daraus die Planer-Regeln:
Wandfuß = flache Zelle, Wand > 35° in ≤ 12 m und ≥ 4 m höher; Schuttfächer bis 30 m mit hangabwärts abnehmender Steingröße (`massstab_schutt_abnahme`
0,5); Terrassenkante = flache Zelle (< 14°) mit Abbruch ≥ 3 m in 6 m → Krüppelkiefern (Faktor 3), Sukkulenten (2,5), Geröllplatten (2,5).
Die Bankung selbst (Dip 2–8°, Bandabstand 10–28 m) ist Vorschlag an Teil C (`felsgruppen_overrides.schichtung`).

**Steppe/Badlands.** Trockene Vegetation ist **fleckig** organisiert; Strauchdeckung in Sagebrush-Steppe < 10 %, dominante Pflanzen selten
über 1 m; Badlands sind von dichten Rinnen- und Gully-Netzen durchzogen, Sträucher konzentrieren Boden und Abfluss um sich ([Karoo-Studie](https://onlinelibrary.wiley.com/doi/abs/10.1002/ldr.2170),
[NatureServe Great Plains Badlands](https://explorer.natureserve.org/Taxon/ELEMENT_GLOBAL.2.860626/Great_Plains_Badlands_Macrogroup),
**[Suchauszug]**; Dichten je Hektar fanden sich nicht). Umsetzung: Sträucher in Gruppen 1–4 (Radius 3 m), Grasbüschel in Inseln 4–12 (Radius
2–2,5 m), alles in Rinnen ×1,6–2,5 und Senken ×1,5–2,0, auf Kuppen ×0,5–0,6; Strauchdeckung im Ödland rechnerisch ≈ 3–6 % (1 600–2 200
Sträucher × 2–3 m² je km²-Feld plus WU-Sträucher), Grasbüschel 20–28 000 je km² = eine Insel alle 6–7 m.

**Schichten-Fazit.** Zwischen Boden und Krone füllen im Trockenbiom fünf Dinge das Bild: (1) Kiesel/Steine in Rinnen und am Wandfuß,
(2) Trockengras-Büschel in drei Höhen (0,25 / 0,6–0,75 / 2 m flach), (3) Dornsträucher und Sukkulenten an Terrassen und in Senken,
(4) Totholz liegend + tote Bäume stehend, (5) Grün nur dort, wo Restfeuchte ist (Rinnen, Oasen, Uferband). Farbakzente: Gold (Trockengras),
Grün-Inseln (Kikuyu, Rohrkolben), Gebleicht (Rinde/„Knochen“, Treibholz), Rost (Sandstein).

## 2. Regelwerk je Schicht (Zahlen = `wueste_ergaenzung_regeln.json`)

Dichte je Zelle = Σ(Lagengewicht × `lage_dichte_je_m2`) × Biomfaktor × Hang-Rampe × Formfaktoren (rinne, kuppe, senke, wandfuss,
terrasse) × Restfeuchte-Rampe × Schnee (−85 % bei voller Schneelage) × `--faktor` × (im Wüstenfeld) `wuestenfeld_faktor`. Fehlen alle
`lage_*.r8`, gilt `dichte_ohne_lagen_je_m2`. Kleinzeug hält 1 m zu Wasser, 2,5 m zu Wegen, 5 m zu Orten; große Klassen (`gross`) 4 m zu
Wegen. Fremde Instanzen (bestand, witcher, mittelschicht, felsgruppen, spuren, ufer, Houdini, WU-Ebene) sperren 0,6 m (klein) / 1,5 m (groß);
fremde Bäume 2,5 m, eigene Bäume untereinander 4 m. Hang > 40° bekommt nur `kiesel`, `stein`, `geroellplatte` (bis 45°).

**Schicht 0 boden** (Sichtweite 40–200 m, keine Kollision):

| Klasse | Netze | Dichte je m² bei voller Lage | Form | Gruppe / Radius | Maßstab | Eingraben | Wüstenfeld |
|---|---|---|---|---|---|---|---|
| kiesel | 7 Megascans SmallStones + 5 Namaqualand stones | Geröll 0,043, Kies 0,051, Sandstein 0,030, Fels 0,017, Sand 0,010, Erde 0,007 | Rinne ×2,5, Wandfuß ×2, Kuppe ×0,8 | 3–9 / 1,2 m | 0,7–1,6 | 40 % Netzhöhe | 0,25, nur Megascans |
| stein 0,2–0,6 m | SandstoneBoulder_03, Namaqualand boulders/rocks, Meadow s_rock | Geröll 0,012, Sandstein/Kies 0,006, Fels 0,004 | Wandfuß ×3 (Größe −50 % bis 30 m), Rinne ×2, Terrasse ×1,5 | 2–5 / 1,8 m | 0,8–1,5 | 35 % | 0,5, ohne Namaqualand |
| lehmplatte (Trockenriss-Ersatz) | DryRiverBed_01/02 (+_GENERATED) | Lehm 0,006, Schlamm 0,004 | nur < 10°, Senke ×2,5, Rinne ×1,5 | 3–8 / 3 m | 0,9–1,4 | 3 cm | 0,5 |
| geroellplatte 7 × 3,7 m | ErodedRockyGround_01–03 | Geröll 0,0012, Felsplatte 0,001 | Wandfuß ×3, Terrasse ×2,5, < 32° | 1–2 / 4 m | 0,8–1,3 | 12 cm | 0,6 |
| zweige | DryBranches_01–08, dead_quiver_branch | Trockengras 0,008, Erde 0,007, Geröll 0,003 | ×4 im Umkreis 8 m toter Bäume, Rinne ×1,6 | 1–3 / 1,5 m | 0,8–1,3 | 2 cm | 0,5 |
| knochen_ersatz | bark_debris a–d, dead_log_05 | Erde/Lehm 0,0006, Sand 0,0004 | Wegband 8–40 m ×2, Senke ×1,5 | 2–6 / 1,4 m | 1,0–1,6 | 1 cm | 0,5 |
| laub_trocken | DeadLeaves_01/12–14, dry_quiver_leaf | Laub 0,01, sonst 0,001 | ×6 im Umkreis 10 m toter Bäume, Senke ×2 | 2–5 / 2 m | 0,9–1,3 | 1 cm | 0,3 |

**Schicht 1 mittel** (0,3–3 m; Sichtweite 80–500 m):

| Klasse | Netze | Dichte je m² | Form | Gruppe / Radius | Hang voll/null | Wüstenfeld |
|---|---|---|---|---|---|---|
| trockengras_hoch 0,6–0,75 m (Nanite) | Megascans Tundra Grass Var B/C/F/G | Trockengras 0,036, Wiese/Gras 0,0135, Heide 0,009, Erde 0,005 | Senke ×1,8, Rinne ×1,6, Kuppe ×0,6, Restfeuchte 1→2 | 4–10 / 2,5 m | 25°/38° | 0,35 (WU hat keine Büschel) |
| trockengras_niedrig 0,22–0,32 m | Tundra Grass Var A/D/E/H/I | Trockengras 0,0275, Geröll 0,0066, Sandstein/Heide 0,0055 | Terrasse ×1,4, Wandfuß ×1,3, Kuppe ×1,2 | 5–12 / 2 m | 30°/42° | 0,35 |
| trockengras_flach 2 m (kein Nanite) | Meadow dead_grass_01–03 | Trockengras 0,007, Erde 0,005 | Wegband 6–60 m ×1,8 („verlassene Felder“), < 28° | 6–14 / 4 m | 12°/28° | 0,3 |
| dornstrauch 0,7–2,1 m | Namaqualand didelta (3), searsia lucida e–g, othonna c/d | Trockengras 0,0018, Erde 0,0015, Heide 0,0014, Geröll 0,001 | Rinne ×2,5, Senke ×2, Kuppe ×0,5, Restfeuchte 1→2,5 | 1–4 / 3 m | 22°/34° | **0** (WU streut sie) |
| trockenhang_strauch 1,5–2,7 m | searsia burchellii/lucida a–d | Erde/Trockengras/Geröll/Heide 0,0008 | Terrasse ×2, Wandfuß ×1,5, Kuppe ×1,2 | 1–3 / 4 m | 30°/40° | **0** |
| sukkulent | cheiridopsis d–i, othonna e–g, wild_rooibos a–e | Sandstein 0,006, Geröll 0,005, Felsplatte 0,004 | Terrasse ×2,5, Wandfuß ×2 | 3–8 / 2 m | 28°/42° | **0** |
| totholz_klein 1–3,6 m | Forest dead_log_01–04, OldFallenTree_02 | Erde/Trockengras 0,0005, Laub 0,001 | Rinne ×2,5 (hangabwärts), Senke ×2, ×5 unter toten Bäumen | 1–3 / 2,5 m | 25°/38° | **1,0** (fehlt WU) |
| totholz_stamm 2,3–5,3 m, **Kollision** | pine_04/08_log, beach_driftwood_01, OldFallenTree_01 | Erde/Trockengras 0,00012 | Rinne ×3, ×4 unter toten Bäumen, Eingraben 30 % | 1 | 20°/32° | 1,0 |
| stumpf | pine_stump_01–03 | Erde 0,00025, Wiese/Trockengras 0,0002 | Wegband 5–50 m ×1,5, ×3 bei toten Bäumen | 1–4 / 5 m | 20°/32° | 0,3 |

**Schicht 2 baum** (zuerst geplant, damit Zweige/Laub/Totholz darunter folgen; Sichtweite 0 = unbegrenzt; Kollision):

| Klasse | Netze | Dichte je m² | Form | Gruppe / Radius | Wüstenfeld |
|---|---|---|---|---|---|
| totbaum_gross 10–25 m | Graveyard Dead_Tree_01–03, EuropeanBeech_Dead_XL, Forest_pine_10_dead, Fir_08_Dead | Erde/Trockengras 0,00005, Laub 0,0001 | **Kuppe ×2,5** (Hangman-Silhouette), Wegband 12–70 m ×1,6, < 28° | 1–3 / 9 m (toter Hain) | 0,5 |
| totbaum_klein 2–7 m (Nanite) | Megascans DeadTree_01/02, Fab Dead_Tree qlEtl, Beech_Dead_M, dead_quiver_trunk | Erde 0,00014, Trockengras 0,00012 | Rinne/Senke ×2, Terrasse ×1,5 | 1–3 / 6 m | 0,6, ohne Köcherstamm |
| einzelbaum_rinne 4–9 m (krumme Eichen) | Coast_Dunes dry_oak_01_A–E, 02_A–D | Lehm/Wiese/Gras 0,0005, Erde 0,0004 | **nur Restfeuchte ≥ 0,35** (Rinne, Senke, ≤ 25 m Wasser) | 1–4 / 10 m | 0,5 |
| krueppelkiefer_terrasse 1,7–4,8 m | pine_beach_crooked_01/02, medium_01/03, small_04 | Sandstein 0,0002, Geröll/Felsplatte 0,00015 | **Terrasse ×3**, Kuppe/Wandfuß ×1,5; canyon 1,0, oedland 0,3, wueste 0 | 1–2 / 5 m | 0,5 |
| koecherbaum | quiver_tree_01/02 | Sandstein 0,0002, Geröll 0,00015 | Kuppe ×2, Terrasse ×2 | 1–3 / 7 m | **0** |

Richtwert tote Bäume: 40–80 große und 100–200 kleine je km² Ödland, d. h. alle 100–150 m eine Silhouette.

**Schicht 5 wasserkante.** `schilf_rest` (9 Eldarien-Rohrkolben-Netze) nur im Band 0,8–5 m am Wasser, < 25°, Gruppen 3–8 / 1,8 m, Dichte
Schlamm/Algen 0,1, Lehm 0,08, Erde/Wiese 0,06 → Oasen und wasserführende Rinnen; `gras_gruen` (Megascans Kikuyu 01–06, Nanite) nur bei
Restfeuchte ≥ 0,55 (Uferband ≤ 12 m, Oasen-Senken), Wiese/Gras/Moos 0,048, Erde/Lehm 0,04, Gruppen 5–12 / 2,5 m. Restfeuchte =
clip(Wassernähe/25 m + 0,6·Senke + 0,35·Rinne + 0,3·Lehm + 0,8·Schlamm + 0,5·Moos + 0,3·Wiese/Gras + 0,8·Algen).

**Budget.** Ziel 50 000, Deckel 60 000, Kollision ≤ 3 000 je Feld; Wüstenfelder 15 000 / 1 200. Überschuss wird deterministisch in
`ausduenn_reihenfolge` (kiesel → trockengras_niedrig → trockengras_hoch → zweige → … → totbaum_gross zuletzt) gedünnt und in
`plan.json["hinweise"]` protokolliert. Nach der Kalibrierung (§5) liegt die Rohsumme nahe am Ziel, so dass der Deckel nur Kiesel und
niedrige Büschel um 40–50 % kürzt.

## 3. Overrides für Teil C (Fels) und Teil D (Spuren) – Vorschlag B9, Übernahme durch die jeweiligen Agenten/Koordinator

**Sandstein-Palette (Teil C).** `felsgruppen_overrides.biom_palette`: canyon/oedland/wueste → `sandstein` (Teil C führt diese Palette bereits:
Megascans Sandstone, Desert Western uk5ebcp/uldubik, RockSandstone). Klassenfaktoren canyon: band 1,6, fuss 1,5, wand 1,2, blockstrom 1,2,
grat 0,6; oedland: kuppe 1,6, prallhang 1,2, band 0,6; wueste: band 0 (Dünen), kuppe 1,2, fuss 1,0, Wüstenfeld-Faktor 0,4. Schichtung
(`schichtung`): Dip 2–8°, Bandabstand 10–28 m, Bandbreite 30 % – nahezu horizontale Bänke, harte Bank = Steilstufe, weiche Lage =
Schuttböschung 30–35°. Eingraben 30–45 %, in den Hang kippen, Kieselring 2,5 m mit 1,2 Kiesel/m² (7 SmallStones).

**Terrassenkanten.** `terrassenkanten`: Kante = flache Zelle (< 14°) mit Abbruch ≥ 3 m in 6 m (dieselbe Ableitung wie im Planer, so dass
Felskante, Krüppelkiefer und Sukkulenten zusammenfallen); Kantenstücke uk5ebcp, uldubik, HugeSandstoneCliff_07, RockSandstone_034 entlang
der Kante (Hauptrichtung = Kantenverlauf), Lücken 6–14 m, nie lückenlos, Eingraben 30–45 %. **Felsnadel/Hoodoo** als Akteur-Blickziel:
1–3 je km² auf Kuppen mit ≥ 12 m Prominenz (MassiveSandstoneCliff_01/03, HugeSandstoneCliff_05, Maßstab 0,6–1,1); ein Felsbogen fehlt im
Inventar (Einkaufsliste).

**Spuren (Teil D).** `spuren_overrides`: **Karren** 2,6 je km Weg (Velen-Kriegsödnis: doppelt so häufig wie in der Aue), 50 % zerbrochen
(`SM_BrokenWoodWagon` bevorzugt, `SM_cartB_a1`, `SM_Carriage_01a`), Kippen 8–22°, Beiwerk 1–4 Stück (Rad, Fass, Kiste, Sack) in 1–4 m
verstreut. **Brunnen** (`SM_Well_02a`) 1–2 je Ort und 0,6 je km² frei, Bedingung Restfeuchte ≥ 0,4 oder ≤ 40 m vom Ort. **Galgen-Ersatz**
aus zwei `SM_Beam_4m` (Abstand 3,2 m) und einem Querbalken `SM_Wood_Beam_4m_01a` bei z = 3,75 m – 0,4 je km Weg, Kuppen-Bonus ×3,
6–25 m vom Weg; Pivot/Rotation des Querbalkens **ungetestet**. Ohne Bauteile liefert `totbaum_gross` mit Kuppe ×2,5 das Hangman-Motiv.
**Steinmänner** zusätzlich in oedland/canyon/wueste (2 je km², SandstoneBoulder_03, Namaqualand boulder). **Einzelgräber** 1,2 je km
Weg, 60 % unter totem Baum. **Verlassene Feldstreifen** (oedland): Stoppeln `dead_grass_01/02` statt Frucht, Zaun zu 55 % lückig, 5–25°
gekippt. **Knochen**: keine im Inventar → bis zum Kauf `knochen_ersatz` (Schicht 0, gebleichte Rindenstücke in Gruppen 2–6 nahe Wegen).
Blickziel-Typen: oedland totbaum_solitaer/ruine/galgen/brunnen, canyon felsnadel/ruine/karren, wueste felsnadel/ruine/brunnen;
Wüstenfeld-Faktor 0,6.

## 4. Abgrenzung zu anderen Ebenen und Planern

- **Wüstenfelder C3–E5 (FT_EL_WU_\*).** Klassen, die die Namaqualand-Ebene schon streut (Dornsträucher, Trockenhang-Sträucher,
  Sukkulenten, Köcherbäume), haben `wuestenfeld_faktor` 0; Namaqualand-Netze werden dort durch `netze_wuestenfeld` (Megascans-Kiesel,
  Sandstone-Boulder, Megascans-Totbäume) ersetzt, damit keine Foliage-Typen doppelt entstehen. Ergänzt werden ausschließlich Rollen, die
  der WU-Ebene laut Taxonomie fehlen: Totholz liegend (Faktor 1,0), Trockengras-Büschel (0,35), Kiesel/Steine in Rinnen (0,25/0,5),
  Trockenbett-Platten, tote Bäume (0,5–0,6), Oasen-Grün. Budget 15 000, Kollision 1 200, **kein `entfernen`**; `plan.json["modus"]` =
  `ergaenzung`. Die WU-Ebene wird als belegt geladen (`--wueste_ebene PFAD`, sonst `export/unreal/welt/wueste/<Feld>/`; ihr Pfad ist in
  der Cloud unbekannt → Hinweis im Protokoll, Planung ohne Abstandsprüfung).
- *(Überholt durch Korrektur Runde 1: Palette + Faktor statt Faktor 0.)* **Teil D Mittelschicht** streut in wueste/canyon/oedland Rooibos/Totholz mit Faktor 0,5 und bittet um Abstimmung. Vorschlag
  (`mittelschicht_overrides`): sobald `wueste_ergaenzung` gesetzt ist, `biom_faktor` wueste/canyon/oedland in `mittelschicht_regeln.json`
  auf 0 (Schicht 1 kommt dann von hier). Alternativ Mittelschicht zuerst setzen – dieser Planer liest `mittelschicht/<Feld>/` als belegt.
- **Teil C Felsgruppen** liefert Schicht 3 (Blöcke > 0,8 m, Bänder, Wände, Fächer); dieser Planer setzt nur Kiesel, Steine 0,2–0,6 m
  und Geröllplatten als Kontaktzone und liest `felsgruppen/<Feld>/` als belegt. Dieselbe Terrassenkanten-Definition in beiden Regelwerken.
- **Aue (B2), Tundra (B3), Lava (B8)** in denselben Feldern: Biomfaktor 0 für alle anderen Biome; weicher Saum 6 m verhindert harte Kanten.
- **Ufer-Ebene / Witcher-Ebene / Houdini-Bestand** werden als belegt gelesen (Nachbarfelder eingeschlossen); nichts wird ersetzt
  (`entfernen` leer in Nicht-Wüstenfeldern).

## 5. Planer und Testanleitung

**Aufruf.** `python -I scripts/wueste_ergaenzung/wueste_ergaenzung_plan.py FELD [FELD …] [--bild] [--faktor 1.0] [--basis PFAD]
[--regeln PFAD] [--netze PFAD] [--wueste_ebene PFAD]`. Liest `hoehe.f32` als memmap (nur Fenster Feld + 64 m; NY 7057 × NX 9577, J-Spalte
auf 505 m geklippt), `lage_*.r8` optional (17 Lagen), `karte_wasser/weg/ort.r8` optional mit Meldung, `eigner.r8` + `welt.json` (0 → aue;
Fallback je Feld aus `feld_biom_fallback`), vorhandene Ebenen optional mit Meldung, `daten/netze.csv` (unbekannte Netze werden gemeldet
und aus der Palette entfernt). Schreibt `export/unreal/welt/wueste_ergaenzung/<Feld>/<Netz>.f32` (10 float32 LE) + `plan.json` (FORMAT §3
plus `ebene`, `modus`, `statistik`, `hinweise`) und bei `--bild` `docs/pruefung/wueste_ergaenzung/<Feld>.png` (1 px = 1 m; Rinnen blau,
Wandfuß braun, Terrassen orange, Kuppen hell; Klassenfarben in `bild_farben`). Nur NumPy (Box-/Gauß-Faltung, Jump-Flooding-Distanz,
Max/Min-Filter, Dilatation); numba optional, nicht nötig; Zufall aus Hash(Weltzeile, Weltspalte, Seed 1109, Kanal) → deterministisch und
nahtlos zu Nachbarfeldern. Geländeableitung: Hang/Normale aus σ 1,5 m, Rinnen = positiver Laplace der Höhe bei σ 3 m und 9 m
(0,03–0,16), Kuppen = Prominenz über dem 24-m-Mittel ≥ 0,6 m (voll 2,5 m) und lokal höchste Zelle in 16 m, Senken = 0,8–3 m unter dem
24-m-Mittel, Wandfuß/Schuttfächer/Terrassen wie §1.

**Rauchtest (synthetisch, 10.10.2026, Cloud).** Produktionswurzel unter dem Scratchpad: `hoehe.f32` in voller Größe (D4: schräg
verlaufende Canyon-Schichtstufen mit Rinne, Fluss und Weg; E6: Ödland-Kuppen, Senken, mäandrierende Gullies, Teich), `karte_wasser/weg/ort`,
`eigner.r8` (7 canyon, 11 wueste_namaqualand, 12 oedland) + `welt.json`, sechs Lagen (Summe ≈ 255 je Zelle), WU-Ebene D4 (3 000
didelta-Instanzen), Bestand E6 (200 Hainbuchen), `daten/netze.csv`.

| Feld | Modus | Instanzen | Kollision | Netze | Zeit | je Schicht (0/1/2/5) | Deckel |
|---|---|---|---|---|---|---|---|
| D4 (canyon 60 %, wueste 27 %) | ergaenzung | **14 998** (≤ 15 000) | 164 (≤ 1 200) | 82 | 6,5 s | 5 920 / 8 611 / 73 / 394 | Rohsumme 16 539 → Kiesel ×0,53 |
| E6 (oedland 96 %) | voll | **49 966** (≤ 60 000) | 345 (≤ 3 000) | 136 | 4,2 s | 16 129 / 33 311 / 199 / 327 | Rohsumme 58 916 → Kiesel, niedrige Büschel ×0,58 |

Prüfungen bestanden: alle f32 durch 10 teilbar, Anzahl je Datei = `plan.json`, Quaternionen normiert, Maßstab > 0, z innerhalb 3 m der
Geländehöhe; **0 Instanzen auf Wasser, Weg, Ort**; Hang > 41° nur Felsklassen (3 Grenzfälle in D4 durch Glättungsdifferenz); zweiter Lauf
byte-identisch (218 Dateien, md5); Feld ohne Zielbiom (A1) → Meldung, nichts geplant; fehlende Basis → klare Fehlermeldung; fehlende
WU-Ebene (E4) → Hinweis, Planung ohne Abstand. Behobene Fehler des Entwurfs: Rohdichten 2,1× über Ziel (Ausdünnung 0,42 auf alle
Kleinklassen → Dichten der Grasbüschel/Zweige/Laub um 45–55 % gesenkt), Kuppen-Erkennung per Laplace blind für flache Ödland-Kuppen
(E6 0 % → Prominenz-Regel, 1,2 %), Instanzen bis 0,5 m außerhalb des Feldes (Rundung → exakte Feldgrenze), Laplace-Randfüllung mit 0
(→ Randfortsetzung; wichtig für Felder am Rasterrand), Weg-Distanz auf 64 m gedeckelt (→ 96 m, Wegband 12–70 m wirkt). Je Klasse E6:
trockengras_hoch 17 632, niedrig 7 319, flach 5 003, zweige 6 991, kiesel 5 110, dornstrauch 1 596, stein 1 669, laub 1 041, lehmplatte
832, totholz 720, totbaum 172, Oasen-Grün 327. **Mit Echtdaten zuerst `--bild` ansehen und `--faktor` justieren**; Erwartungsspannen
je Feld in `erwartung_je_feld` (E6 38–55 000, D6 20–38 000, E7 3–8 000, D4 10–15 000, E4 4–12 000, C4/D3/E3 2–7 000, D5 1,5–5 000,
E5 0,5–2 500, F6 1–4 000).

**Prüfkameras.**

| Feld | Kamera | Position / Blick | Woran man Erfolg erkennt |
|---|---|---|---|
| D4 | Canyon-Wand | Wandfuß der höchsten Steilstufe (Zelle mit maximaler `wandfuss`-Stärke im PNG), 12 m vor der Wand, 1,7 m, 15° aufwärts | Schuttfächer: Steine groß am Fuß, kleiner hangabwärts; Terrassenkante mit Krüppelkiefer und Sukkulenten; kein Block ohne Rinnen-/Wandbezug; Trockengras gold in den Rinnen; WU-Sträucher unverändert, kein Doppel |
| E6 | Ödland Augenhöhe | Mitte einer Lehm-Senke mit Restfeuchte, 1,7 m, Blick zum Horizont mit Weg | in 10 m mindestens ein Objekt 0,5–3 m (Dornstrauch, Totholz, Stumpf); Trockenbett-Platten am Boden; Büschel in drei Höhen; toter Baum auf der Kuppe am Horizont; Karren-Wrack am Weg (Teil D) |
| E4 | Wüstenrand | Biom-Saum wueste/aue, 1,7 m, Blick entlang der Grenze | WU-Ebene unverändert; zusätzlich Totholz, Kiesel in Rinnen, vereinzelt Trockengras, Grün nur am Wasser; keine doppelten Sträucher; Gesamt ≤ 15 000 |

Im Editor: Sichtweiten und Kollision je Foliage-Typ aus `plan.json["dateien"]` übernehmen; Nicht-Nanite-Bäume (Graveyard, Forest,
Coast_Dunes) auf LOD-Übergänge prüfen.

## 6. Einkaufsliste (Fab/Megascans, frei bevorzugt, High 4K reicht)

| Asset (Fab-/Megascans-Name) | Stufe | Wofür | Ersetzt |
|---|---|---|---|
| Megascans „Desert Western Tree Log Dead Small 02 / Medium 02“, „Desert Western Tree Stump Dead Medium 01“ ([Fab-Suche](https://quixel.com/megascans/), **[Suchauszug]**) | High | vertrocknete Stämme/Stümpfe ohne Moos/Rinde; Ödland-Stumpf („abgeholzt, dann verbrannt“) | totholz_stamm (Forest-Logs, Treibholz), stumpf (pine_stump) |
| Megascans Dead Tree-Varianten (Fab „Dead Tree“, 2–3 weitere Nanite-Scans) | High | mehr Silhouetten für totbaum_klein; Graveyard-Bäume sind kein Nanite | totbaum_gross/klein (Graveyard, Forest) |
| Dornstrauch gemäßigt (Fab „Hawthorn“/„Blackthorn“ oder Megascans „Dry Shrub“, 3–4 Varianten 1–2 m) | High | Ödland-Mittelschicht ohne Namaqualand-Look; Velen-Dornhecke | dornstrauch (didelta/searsia) |
| Megascans „Sandstone Ledge Medium“ (3–6 m), geschichtete Sandstein-Bänke (vgl. Teil C) | High | Terrassenkanten/Bänder mit sichtbarer Bankung | uk5ebcp/uldubik 0,6–0,8 m |
| Felsbogen/Hoodoo-Säule 8–15 m (Fab „Sandstone Arch“/„Hoodoo“) | High | Blickziel Canyon (`felsnadel`, Bogen) | MassiveSandstoneCliff als Nadel |
| Megascans Decals „Cracked Mud“/„Dry Mud Cracks“, „Sandstone Rocky Ground“ ([Quixel Sandstone Rocky Ground](https://quixel.com/megascans/home?category=decal&assetId=vmnmcbr&environment=desert+biome), **[Suchauszug]**) | High | Trockenrisse in Lehm-Senken als Decal statt Platten | lehmplatte (DryRiverBed) |
| Megascans „Scattered Bones“ (Decal), „Ram Skull“, „Skull“ ([Quixel Scattered Bones](https://quixel.com/megascans/home?assetId=ukxiabph), [Ram Skull](https://quixel.com/megascans/home?assetId=tiiief2fa), **[Suchauszug]**) | High | Kadaverstellen, Knochen an Wegen und unter Galgen | knochen_ersatz (bark_debris) |
| Karren-Wrack/Wagenteile (Fab „Broken Cart“, „Wagon Wheel“ Set) | High | mehr Wrack-Varianten; heute nur BrokenWoodWagon zerbrochen | spuren_overrides.karren |
| Galgen (Fab „Gallows“/„Hangman“) | Medium reicht | Velen-Motiv, ersetzt den Balken-Bausatz | galgen_ersatz |
| Megascans „Desert Plant“/Agave-Scans ([Quixel Desert Plant](https://quixel.com/megascans/home?assetId=scvkX), **[Suchauszug]**) | High | Agaven/Sukkulenten außerhalb des Namaqualand-Stils | sukkulent |

Hinweis: das ältere „Megascans Desert Pack“ liegt nur im Epic-Vault, nicht auf Fab ([Fab-Support](https://support.fab.com/s/article/Deprecated-Megascans-Not-Transferring-to-Fab?language=en_US), **[Suchauszug]**).

## 7. Offene Punkte

1. **Echtdaten.** Alle Dichten sind auf synthetische Lagen (Summe 255, Erde/Trockengras-lastig) kalibriert; E6 real hat Lehm 25 %,
   Erde 18 %, Geröll 15 %, Sandstein 12 %, Trockengras 9 % → erwartbar 20–30 % weniger Büschel, mehr Lehmplatten/Kiesel. `--faktor`
   und `erwartung_je_feld` nach dem ersten Echtlauf nachziehen; Korrekturen als `auftraege/verteilung-wueste-korrektur.md`.
2. **Pfad der WU-Ebene** (`scripts/wueste_bewuchs/`) ist unbekannt; ohne `--wueste_ebene` plant der Planer in C3–E5 ohne Abstand zur
   Namaqualand-Ebene (Hinweis im Protokoll). Ebenso unbekannt: ob die WU-Ebene Kiesel/Steine streut – falls ja, `kiesel`/`stein`
   `wuestenfeld_faktor` auf 0.
3. *(Erledigt in Korrektur Runde 1: Override-Blöcke im Schema von Teil C/D, von allen drei Querschnitts-Planern gelesen.)* **Abstimmung Teil D:** `mittelschicht_regeln.json` Biomfaktor wueste/canyon/oedland → 0 oder Reihenfolge Mittelschicht → Wüste;
   `spuren_regeln.json` Übernahme der Karren-/Brunnen-/Galgen-/Steinmann-Overrides; Teil C Übernahme von `felsgruppen_overrides`
   (Sandstein-Palette ist dort vorhanden, Schichtungs- und Terrassenparameter noch nicht).
4. **Rinnen-Erkennung** (Laplace 0,03–0,16) ist auf 1-m-Raster mit glatten Houdini-Höhen abgestimmt; bei rauen Echtdaten evtl.
   `konkav_ab` anheben, sonst zu viele „Rinnen“ (Prüfbild: blaue Tönung sollte Linien zeigen, keine Flächen).
5. **Schichtstufen-Bankung** (Dip, Bandabstand) kann der Planer nicht aus `hoehe.f32` allein beweisen; die Werte sind Richtwerte aus
   Monument-Valley-/Wadi-Rum-Referenzen und müssen mit Teil C an der Kachel-Textur (V16-Kachel zeigt horizontale Linien) abgeglichen werden.
6. **Nicht-Nanite-Netze** (Graveyard-/Forest-Totbäume, Coast_Dunes-Eichen/-Kiefern, Meadow dead_grass) mit Sichtweite 0 kosten Drawcalls;
   nach Einkauf der Nanite-Dead-Trees Palette tauschen.
7. **Galgen-Bausatz:** Pivot/Rotation des Querbalkens ungetestet; Spuren-Setzer muss Bauteile relativ zum Fußpunkt setzen.
8. **Schnee** in E3 (17 %) reduziert alle Klassen auf 15 %; ob dort Frost-Ergänzung (B4) oder diese Ebene gilt, ist Koordinatorentscheidung.

## Quellen

- `vorlagen/FORMAT.md`, `vorlagen/daten/biome_je_feld.md`, `antworten/assets-taxonomie.md` (Lücken wueste/canyon/oedland),
  `antworten/bildkritik-witcher-messlatte.md`, `antworten/verteilung-fels-organisch.md` (Sandstein-Palette, Akteur-Konvention),
  `antworten/verteilung-leere-fuellen.md` (Mittelschicht Wüstenfelder, Spuren), `antworten/verteilung-aue.md` (Paketvorbild).
- [80.lv – World Building of Witcher 3](https://80.lv/articles/world-building-of-witcher-3); [Vice – Designing the World of The Witcher 3](https://www.vice.com/en/article/designing-the-world-of-the-witcher-3-wild-hunt/);
  [Console Pulse – Velen explained](https://consolepulse.com/multiplatform/the-witcher/guides/the-witcher-3-velen-explained) – **[Suchauszug]**.
- [PlayStation Blog – How the Witcher 3 team built Toussaint](https://blog.playstation.com/archive/2016/05/10/how-the-witcher-3-team-built-the-land-of-toussaint-for-upcoming-expansion-blood-wine);
  [80.lv – Toussaint-inspired environment in UE5](https://80.lv/articles/toussaint-the-witcher-3-inspired-environment-set-up-in-ue5) – **[Suchauszug]**.
- [grandcanyon.net – Faults and Landforms](https://www.grandcanyon.net/faults-and-landforms); [NatureServe – Colorado Plateau Mixed Bedrock Canyon and Tableland](https://explorer.natureserve.org/Taxon/ELEMENT_GLOBAL.2.722907/Colorado_Plateau_Mixed_Bedrock_Canyon_and_Tableland);
  [NPS – Mesa Verde (Kolluvium)](https://www.nps.gov/parkhistory/online_books/archeology/7b/chap3d.htm); [ScienceDirect – Landforms in clastic tablelands](https://www.sciencedirect.com/science/article/pii/S0341816222005318) – **[Suchauszug]**.
- [Wiley – Eco-geomorphological processes, semi-arid Karoo](https://onlinelibrary.wiley.com/doi/abs/10.1002/ldr.2170); [NatureServe – Great Plains Badlands](https://explorer.natureserve.org/Taxon/ELEMENT_GLOBAL.2.860626/Great_Plains_Badlands_Macrogroup);
  [ScienceDirect – Badlands overview](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/badlands) – **[Suchauszug]**.
- [Quixel/Fab – Scattered Bones](https://quixel.com/megascans/home?assetId=ukxiabph), [Ram Skull](https://quixel.com/megascans/home?assetId=tiiief2fa), [Desert Plant](https://quixel.com/megascans/home?assetId=scvkX),
  [Sandstone Rocky Ground Decal](https://quixel.com/megascans/home?category=decal&assetId=vmnmcbr&environment=desert+biome), [Fab-Support deprecated Megascans](https://support.fab.com/s/article/Deprecated-Megascans-Not-Transferring-to-Fab?language=en_US) – **[Suchauszug]**.
