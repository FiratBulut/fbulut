# Auftrag 13 – Sehenswürdigkeiten (8 je Biom): Status

Stand: 2026-10-11 14:16 UTC. **Phase 1 abgeschlossen** (Antwort `13-sehenswuerdigkeiten-8-je-biom.md`). Koordinator: Cloud-Session. Wird bei jedem Push aktualisiert.

## Phase 1

| Teil | Inhalt | Stand |
|---|---|---|
| A | Download-Liste für Ferat (`sehens-downloadliste.md`, `sehens/downloadliste.json`) | **Stand Inventar 13d** (Antwort `13d-sehens-bestand-komplett.md`): 13 Pakete erledigt; noch fehlend 28 (A 1 Driftwood, B 12, C 15) – 6 kostenlos (Claude lädt auf Wunsch), 22 nur nach Ferats OK; Limestone nicht im Inventar |
| Baukasten | `skripte/sehens_lib/` (Laden 2 m, Hang/Krümmung/Abfluss, Sichtbarkeit vom Weg, Kandidatensuche, Draufsicht-PNG, Format-Prüfer `sehens_pruefen.py`) | fertig, gepusht (Selbsttest auf echten 2-m-Daten ohne Fehler; Grenzen: Bäume nur 4-m-Näherung, 1-m-Lader nur synthetisch getestet) |
| B/C | Katalog + `sehens/<biom>/standorte.json` + Draufsichten je Ort | **fertig**: 120 Orte (48 Leuchtfeuer/72 Fundstücke), 19 Pfade (20,9 km) in `pfade`; Gesamtkatalog `sehens-katalog.md` mit allen Ortsabschnitten; `sehens/marker.json`; Prüfer über alle Biome 0 FEHLER, 1 WARNUNG (Tundra-Pfad streift ROMAN_LOC_018) |
| D | diese Datei | aktuell |
| Pfade | `pfade` in `standorte.json` (Schema 13c), Lib rastert sie als Wege | fertig: alte `standorte_*.json` aufgelöst, Lava/Gletscher/Frost/Fjord je 8 Orte |
| Phase 2 | Planer `skripte/sehens_<biom>/` + Lib-Erweiterung | **Lib fertig** (`inventar.py`, `stempel.py`, `instanzen.py`, `rezept.py`, `vorschau.py`, Prüfer Phase 2, `PLANER_ANLEITUNG.md`); **Referenzplaner Bergwald fertig** (8 Orte, alle 6 Detail-Ebenen, Prüfer 0 FEHLER/0 WARNUNG, deterministisch, Testbilder `sehens/bergwald/test_*.png`). Übrige 14 Biome laufen parallel: aue+sumpf · elfenwald+dschungel · lava · gletscher+frost+fjord · tundra+heide · canyon+wueste+oedland · kueste |

### Phase 2 – Planer je Biom

| Biom | Planer | Stand | Anmerkungen |
|---|---|---|---|
| bergwald | `skripte/sehens_bergwald/` | **fertig** (Inventar 13d; Planer + Prüfer 0 FEHLER/0 WARNUNG; deterministisch) | Klamm mit NS_Waterfall_Medium/NS_Impact_Medium/NS_Stream_Small; Mountain-Wurzeln/Pilze; Nassband-Decals; Karsee ±9 m |
| aue | `skripte/sehens_aue/` | **fertig** (Inventar 13d; 0 FEHLER/0 WARNUNG; byteidentisch) | Biberstau-Teich mit Dammbogen; Die Alte = Schwarzpappel ×1,3; Schwalbenwand mit eigener Brutröhren-Decal-Textur; Mondarm-Gürtel 220 m (Verdeckung bestanden); Blautopf-Trichter 9 m (Stempel 10,4 m, begründet). Mondarm-Spiegel aus Gelände geschätzt ~14,2 m (teiche.json kennt nur Westarm 13,22 m) |
| sumpf | `skripte/sehens_sumpf/` | **fertig** (Inventar 13d; 0 FEHLER/0 WARNUNG; byteidentisch) | Epic-See als `bestandswasser`; 47 tote Fichten im Ertrunkenen Wald; Weidendom auf `SM_SwampCypress_A`; Riesenseerosen ×2,5–4; Erlenbruch-Gehölzring (Verdeckung bestanden); Irrlichtsenke mit Nebel, NS_Sparkling_Glow und 2 Punktlichtern ≤ 2 cd |
| kueste | `skripte/sehens_kueste/` | **fertig** (Inventar 13d; 0 FEHLER/0 WARNUNG; byteidentisch) | Brandungspfeiler aus 3 Stücken (Kopf ~49 m); Nadeltor-Stempel −49 m (begründet); Seefall 54 m mit NS_Waterfall_Large; Blasloch mit NS_Geyser_Large; alle 4 Fundstücke verdeckt. Korrekturen: Guano-Wand der Vogelinsel an der Ostflanke (Kameras stehen im Osten), Kreidewand-Hauptwand nach Süden; Klang-Ersatz für Brandung/Seevögel |


- **Karsee (bergwald_06):** Der Karboden ist in den 2-m-Daten 18–27° geneigt; der See braucht ~±9 m Erdbau statt ±6 m (Gelände frei → umgesetzt, begründet im Stempel). Im 1-m-Lauf prüfen.
- **Mönch (bergwald_01):** Sockelplateau entfällt (Hang 52°); die Nadel steckt hangseitig tiefer im Boden.
- **Pivot/Schauseite:** Für Klippenschalen, Basalt und viele Mountain-Netze fehlen Maße in `netze_masse.json` → Annahme „Pivot unten Mitte“, Schauseite angenommen; das Prüfbild im Editor entscheidet.
- **1-m-Daten:** Planer noch nicht mit 1 m getestet (lokal bei Claude).

### Inventar 13d (komplett nach Ferats Downloads)

- Nature Water FX, Lava & Volcano (inkl. `SM_lava_wall_*`), Coast & Dunes, Mountain, Desert Western sind im Projekt; alle 15 `asset_bedarf.json` haben einen Block `abgleich_13d` (85 Wünsche erfüllt, 49 Ersatzlösungen → echte Assets, 60 Punkte fehlen weiter). Planer werden gerade umgestellt; Bergwald ist umgestellt (0 FEHLER).
- **Nicht verwenden** (unvollständig): `Desert_Western_Cluster_Rock_Medium_05_uldubik`, `Desert_Western_Ledge_Rock_Small_07_uk5ebcp`. Hinweis an Claude lokal: beide stehen auch in Auftrag-11-Dateien (`skripte/felsgruppen_regeln.json`, `skripte/wueste_ergaenzung_regeln.json`, `assets-taxonomie.*`, `verteilung-*.md`) – dort bitte vorerst ausfiltern oder nach dem Neuladen prüfen.
- Doppelnamen brauchen den vollen Pfad: `SM_Forest_pine_06` (Baum 25 m vs. Wurzel 2,5 m); `SM_Big_rock_01/02` ≠ `SM_Big_Rock_01/02`; `SM_pine_roots_01` (Coast) ≠ `SM_Pine_roots_01` (Mountain).

## Biome

| Biom | Stand | Orte |
|---|---|---|
| elfenwald | fertig (Prüfer 0 Fehler/0 Warnungen) | Leuchtfeuer: 01 Mutterbaum, 02 Nebelhain, 03 Rotlaubhain; Fundstücke: 04 Elfentreppe (Kalktuff-Stufen im Bach), 05 Farnschlucht, 06 Blauer Grund (Immergrün unter Buchen), 07 Schwammgrund (Riesenpilze auf gestürztem Riesen), 08 Wurzelbrücke |
| dschungel | fertig (Prüfer 0 Fehler/0 Warnungen) | Leuchtfeuer: 01 Mondtor (Felsbogen), 02 Turmquelle, 03 Steinwald (Kalknadeln); Fundstücke: 04 Blaues Auge (Cenote), 05 Verborgene Lagune (Turmspalte), 06 Schluckhöhle, 07 Garten der Riesen, 08 Sinterhalle (Felsdach) |
| aue | fertig (Prüfer 0 Fehler/0 Warnungen; Mondarm nur mit neuem Ufergehölz-Gürtel voll verdeckt) | Leuchtfeuer: 02 Die Alte (Riesen-Stieleiche), 03 Schwalbenwand (Prallhang-Lehmwand), 04 Treibholzwerder (Kiesinsel mit Treibholz); Fundstücke: 01 Biberstau, 05 Lilienrinne, 06 Mondarm (Altwasser), 07 Blautopf (Quelltopf), 08 Lianenhalle (Auwald) |
| lava | fertig (8 Orte; Kratersteig West/Ost + Gipfelsteig in `pfade`, Ferat 13c: bauen; Prüfer 0 Fehler, alle Orte 80–300 m vom Weg/Pfad) | Leuchtfeuer: 01 Die Schwarze Mauer (Stromkante mit Schlotturm), 02 Schwefelgrund (Fumarolenfeld), 03 Die Kraterkinder (Pseudokrater); Fundstücke: 04 Das Röhrenfenster (eingestürzte Lavaröhre mit Farnoase), 05 Die Klare Spalte (Grundwasserspalte); am Kratersteig: 06 Die Kraterreihe (Leuchtfeuer), 07 Die Basaltorgel, 08 Das Glutauge |
| bergwald | fertig (Prüfer 0 Fehler/0 Warnungen) | Leuchtfeuer: 01 Der Mönch (Felsnadel), 02 Die Brandkiefer (Blitzbaum), 03 Säulenhain (Riesentannen); Fundstücke: 04 Felsenmeer, 05 Klemmblock-Klamm mit Schleierfall, 06 Karsee, 07 Windwurf, 08 Der Wurzelstein |
| gletscher | fertig (8 Orte; Weststeig, Oststeig, Nordhang als Serpentinen in `pfade`; Prüfer 0 Fehler) | heute: 01 Gletschertor mit Séracbruch (Leuchtfeuer), 02 Lawinenkegel (Leuchtfeuer), 04 Toteisloch (Fundstück); mit Steig: 05 Die Wächte (Leuchtfeuer), 03 Moränensee, 06 Gletschertöpfe, 07 Der Nunatak, 08 Gletscherschliff |
| frost | fertig (8 Orte; Froststeig + Südsteig in `pfade`; Prüfer 0 Fehler; Fundstücke brauchen Fels-/Wallrahmen gegen Sicht vom Steig) | Leuchtfeuer: 02 Frostsee (Presseis, Blasen), 04 Raureifhain, 06 Eisküste (schwach: nur 6 Steigpunkte sehen sie); Fundstücke: 01 Eisfall, 03 Eisvorhang, 05 Blockgletscher, 07 Frostblumen, 08 Glockenbach – in Phase 2 Fels-/Wallrahmen nötig, sonst vom Steig aus 500–800 m sichtbar |
| fjord | fertig (8 Orte; Fjordsteig + Kanzelsteig als Serpentinen in `pfade`; Prüfer 0 Fehler) | Leuchtfeuer: 01 Die Kanzel, 02 Schleierwand, 03 Trollzunge; Fundstücke: 04 Hängetal, 05 Fjordkopf, 06 Bergsturzkegel, 07 Brandungsgrotte (Tauschkandidat, falls die Küste eine Grotte hat), 08 Strandterrassen (Die alten Ufer) |
| tundra | fertig (Prüfer 0 Fehler; 1 Warnung: Pfad zum Trunkenen Grund streift den Rand der geplanten Stadt ROMAN_LOC_018). 4 Leuchtfeuer/4 Fundstücke statt 3/5, weil die offene Küstenebene unter dem höheren Küstenweg kaum Verstecke bietet. 4 Pfade nach 13c-Schema in `pfade`. | Leuchtfeuer: 01 Der Pingo (Eisbuckel), 02 Der Wanderer (Findling auf Rundhöcker), 03 Die Eiswand (Auftaurutschung mit Bodeneis), 04 Die Fließtreppe (Solifluktionszungen); Fundstücke: 05 Der Trunkene Grund (Thermokarstsee, schiefe Bäume), 06 Das Aufeis, 07 Die Steinringe, 08 Das Wabenmoor (Eiskeil-Polygone) – 07/08 vom höheren Küstenweg teilweise einsehbar |
| heide | fertig (Prüfer 0 Fehler/0 Warnungen); keine Pfade nötig (Wege überall 80–150 m entfernt); Fundstücke durch geplante Senken/Ränder verdeckt (Kern überall verdeckt) | Leuchtfeuer: 01 Die Graue Burg (Granit-Tor), 02 Ginstergold (schwach, wirkt nur über Farbe), 03 Die Wacholderprozession; Fundstücke: 04 Der Kolk (Moorauge), 05 Der Wackelstein, 06 Der Wollsackfall, 07 Der Totengrund (Heidekessel), 08 Die Windkante (Parabeldüne) |
| kueste | fertig (Prüfer 0 Fehler/0 Warnungen). Heute kein Weg (nächster 543 m entfernt) → zwei neue Pfade in `pfade`: Klippensteig 4,35 km (max. 33°, 114 m als Kehren mit Felsstufen; Start am Weg südlich von Zalas verborgener Stadt, außerhalb des Stadtkreises) und Kap-Pfad 1,93 km (max. 27°). 4 Leuchtfeuer/4 Fundstücke, weil vom Pfad aus kein Uferpunkt verdeckt ist | Leuchtfeuer: 01 Die Alten (Granitpfeiler), 02 Die Vogelinsel, 03 Das Nadeltor, 06 Die Kreidewand; Fundstücke: 04 Der Seefall (57 m ins Meer), 05 Die Gezeitenbank, 07 Der Dünenkamm, 08 Das Blasloch |
| sumpf | fertig (Prüfer 0 Fehler/0 Warnungen); alle Orte 154–286 m vom Weg, keine Pfade nötig. Wasser = Epic-See `T_2954_391` (Spiegel 1,58 m, 22 % des Bioms) | Leuchtfeuer: 01 Der Ertrunkene Wald, 02 Der Weidendom, 03 Der Reiherhorst; Fundstücke: 04 Der Schwingrasen, 05 Der Erlenbruch (voll verdeckt nur mit geplantem Erlenring), 06 Das Bultenfeld, 07 Der Tellerweiher (Riesenseerose), 08 Die Irrlichtsenke |
| canyon | fertig (Prüfer 0 Fehler/0 Warnungen); 5 Zugänge mit Kehren als `pfad_cm` am Ort; Flüsterschlucht und Welle erst mit Geländestempel verdeckt | Leuchtfeuer: 01 Sonnenfenster (Felsbogen), 02 Der Wäger (Balancierfels), 03 Rote Stufe (Tafelberg-Abbruch); Fundstücke: 04 Flüsterschlucht (Slot-Canyon), 05 Hoodoo-Kessel, 06 Die Kolke (Potholes), 07 Smaragdgumpe (Wasserfall + hängender Garten), 08 Die Welle |
| wueste | fertig (Prüfer 0 Fehler/0 Warnungen); gebaute Wüstenfelder werden nur ergänzt | Leuchtfeuer: 01 Yardang-Flotte, 02 Sterndüne (22 m), 03 Die Wächter (Pilzfelsen); Fundstücke: 04 Quelloase, 05 Salzpfanne, 06 Windkanter-Feld, 07 Trockenes Wadi, 08 Wabenwand (Tafoni, Wüstenlack) |
| oedland | fertig (Prüfer 0 Fehler/0 Warnungen); nur 0,064 km² Ödland-Boden 80–300 m vom Weg → **„Ödlandpfad“** in `pfade` (3 Äste, 1,93 km, Abstieg mit Kehren max. 19,8°) – **Koordinator: wird gebaut** (Ferats Linie „lieber ein Pfad mehr als ein Ort weniger“); 03/06/07/08 hängen daran | Leuchtfeuer: 01 Rippenland (Badlands), 02 Regenbogenhang, 03 Höllentor (brennender Gaskrater); Fundstücke: 04 Dornbusch-Senke, 05 Kugelsteine, 06 Schlammvulkänchen, 07 Totenpfanne, 08 Erdröhren |

## bildwuensche

- aue: fünf Bildwünsche mit Kameras in `sehens/aue/asset_bedarf.json`
- lava: Kraterreihe (heutige Kachel), Westschlucht, Stromfront, Kraterkinder-Senke (Kameras in `sehens/lava/asset_bedarf.json`)
- bergwald: Mönch und Säulenhain `_fern`, Klamm und Karsee `_held` (Kameras in `sehens/bergwald/standorte.json`)
- gletscher/frost/fjord: `gletscher_01_gletschertor_held`, `gletscher_05_die_waechte_fern`, `frost_02_frostsee_held` (welche Houdini-Reste müssen weg?), `frost_04_raureifhain_fern`, `fjord_02_schleierwand_held`, `fjord_01_die_kanzel_anmarsch` (Kameras in den jeweiligen `standorte*.json`)
- canyon/wueste/oedland: Bildwünsche mit Kameras in den jeweiligen `asset_bedarf.json`

## Entscheidungen Ferat (Chat, 11.10. nachmittags)

- **Gelände darf frei angepasst werden** – die Landschaftsform ist keine feste Regel; Geländestempel auch über 40 m (z. B. −48 m unter dem Nadeltor, kueste_03) sind erlaubt.
- **Brushify – Moorlands Pack:** nicht im Bestand, zu teuer → nicht kaufen. Ginster/Wacholder/Wollgras mit Ersatz aus dem Bestand (Sanddorn, gestauchte Jungkiefern, Binsen).
- **Klippensteig (Küste):** Entscheidung beim Koordinator, Maßstab Witcher-Qualität nach unseren Referenzbildern. **Entschieden: voller Klippensteig (4,35 km) + Kap-Pfad bauen** – ein Steig an der Steilküste mit Kehren und Felsstufen, Blick auf Pfeiler, Vogelinsel und Nadeltor, ist genau die Skellige-Art Weg, die die Referenzen zeigen; die Kurzvariante würde Vogelinsel und Nadeltor (zwei der vier Küsten-Leuchtfeuer) kosten.
- **Nature Water FX: gekauft** (Import und Inventar folgen) → Gischt/Wasserfälle für Seefall, Blasloch, Schleierfall, Schleierwand, Eisfall.
- **Megascans:** größtenteils 2024 beansprucht, also kostenlos. Desert Western Cliff Layered, weitere Megascans-Limestone und das kostenlose „Limestone Rock Set“ (Ancraite) werden geladen. **Forest Cretaceous gestrichen** (teuer, schlecht bewertet).

## Noch offen (kompakt, Stand Phase-1-Abschluss)

1. **Hollowstone Canyon kaufen?** (Wabenwand wueste_08, Hoodoos canyon_05; sonst Ersatz aus Sandstein + Tafoni-Material.) **Megascans Desert Pack / Megascans Sandstone** schon in der Bibliothek?
2. **Inventar:** Kommen `SM_lava_wall_01…09` mit der Lava-Nachladung zurück? Behalten die Eis-Netze `M_MS_Base_Trm`? Dürfen Basalt-Instanzen eigene Texturen bekommen? Welche Assets stecken hinter den zwei fehlgeschlagenen Megascans-IDs?
3. **Nebel:** `BP_FogBankCard`/`BP_FogBankVolume` als Akteure setzen, oder nur `lokaler_nebel`? Irrlichter (Sumpf) mit 2 schwachen Punktlichtern oder nur Nebel?
4. **Tundra:** Darf der Pfad zum Trunkenen Grund den Rand von ROMAN_LOC_018 streifen? Aufeis/Thermokarstsee neben Frost/Gletscher in Ordnung? Steinringe Fundstück lassen (vom Küstenweg teils sichtbar) oder Leuchtfeuer?
5. **Eis:** Darf ein Steig über Gletschereis führen? Houdini-Reste `SM_K7_GLETSCHER__EIS`, `SM_K13_FROSTSEE__*` und die alten Klippenkacheln der Steilküste (K9) ausblenden? Wasserfälle > 150 m Fallhöhe in Ordnung?
6. **Sumpf:** See stellenweise eigene Farbe `schwarz_spiegel`?
7. **Canyon:** später einen „Canyonsteig“ (Nordhälfte heute nur über Wasser; +2–3 Orte möglich)?
8. Optionale Tiere (Fische, Ameisen) mit „nur Landschaft“ vereinbar?

Beantwortet (13c bzw. Chat, siehe „Entscheidungen Ferat“ und `13c-antworten-offene-fragen.md`): Pfade/Steige (alle gebaut), Kratersteig + Gipfelsteig, Basalt, Mondtor, Rotlaub, Cenote-See, Tausendfuß, Die Alte, Erlen-Ersatz, Mondarm-Gehölz, Schwalbenwand-Decal, Mönch, Windwurf/Säulenhain, Karsee-Stempel, Gelände frei, Klippensteig, Brushify, Forest Cretaceous, Nature Water FX. Die Einträge unten sind der Verlauf.

**Neu aus Phase 2 (Küste):** Darf die Guano-Wand der Vogelinsel an der Ostseite liegen (Katalog sagte West, alle Kameras stehen im Osten)? Editorbild für Schauseite der Klippenschalen und die Unterseite des Nadeltor-Sturzes. Vogelwolke über der Vogelinsel (`NS_feather`) behalten (Frage Tiere)?

**Neu aus Phase 2 (Aue/Sumpf):** Stimmt der Mondarm-Spiegel ~14,2 m? Schauseiten von Lehm- und Kalkwand (`front_achse +y`), Reiherhorste und die Blattkarten der Graveyard-Totbäume bitte im Editorbild prüfen.

**Neu aus 13d:**
9. **Limestone:** nicht im Inventar 13d – soll Claude (lokal) die Megascans-Limestone-Assets und das Ancraite „Limestone Rock Set“ laden? Link zum Ancraite-Set?
10. `uldubik`/`uk5ebcp` neu laden und dabei die zwei fehlgeschlagenen IDs aus 13b prüfen?
11. Die 6 kostenlosen Pakete (Electric Dreams, European Black Alder, Icelandic Sand, Tundra Icelandic Rock Cluster, Megascans Desert Pack, Megascans Sandstone) gleich mitladen?
12. **Kostenpflichtig – welche?** Empfehlung nach Wirkung: Nanite Driftwood Props (einziges A: Treibholzburg aue_04), Quercus Robur (Die Alte), CryoGen (Frost), Hollowstone Canyon (Wabenwand), Arctic Cliffs.
13. Name/Pfad des Mountain-Wasserfall-Materials (`M_River_Water_Translucent` hat im Inventar keinen Pfad)? Wo liegen die Coast-&-Dunes-„Stempel“ (nicht in `netze.csv`)?

## Offene Fragen – Verlauf

- elfenwald/dschungel: Ist der 0,9-km-Serpentinenpfad zum Nebelhain akzeptabel? Mondtor-Bogen aus `SM_Cliff_01*` zusammengesetzt in Ordnung? Darf die Buchenblatt-Material-Instanz rot getönt werden (Rotlaubhain)? Ist im Cenote-Schacht heute Meerwasser zu sehen (Bildwunsch)? Welches Tropenpflanzen-Paket ist schon vorhanden? Einverstanden mit Streichen von „Tausendfuß“ (ersetzt durch Sinterhalle)?
- aue: Für Die Alte auf das Eichenpaket (Quercus Robur) warten oder Schwarzpappel aus dem Bestand (×1,3)? Megascans-Erlen (European Black Alder) schon in der Bibliothek? Einverstanden mit 220 m neuem Ufergehölz am Mondarm (sonst kein echtes Fundstück)? Darf für die Brutröhren der Schwalbenwand eine eigene kleine Decal-Textur erzeugt werden?
- **lava: Soll der Kratersteig gebaut werden (dann 8 Orte), oder wird für das Lava-Biom die Regel 80–300 m vom Weg gelockert?** Der Gipfelkrater ginge nur mit Serpentinen (Kegel 30–40°). Basalt Columns AssetKit (ca. 11 €) für die Basaltorgel kaufen?
- bergwald: Reicht für den Mönch eine hochkant gestellte Granit-Schale `veqnci0db_tier_2` (kein echtes Felsnadel-Netz)? Dürfen Nicht-Nanite-Nadelbäume liegend (Windwurf) und 2,5-fach skaliert (Säulenhain) gesetzt werden, oder auf Forest Cretaceous warten? Geländestempel ±6 m für den Karsee in B5 in Ordnung?
- **gletscher/frost/fjord: Welche Steige baust du?** Empfehlung: zuerst den Froststeig (1,3 + 0,7 km, flach), er trägt alle 8 Frost-Orte. Danach Gletschersteig West/Nordhang/Ost (3,7 km, +5 Orte) und den Fjordsteig (2,35 km + 0,32 km, +8 Orte) – oder statt des Fjordsteigs einen richtigen Weg vom Erlenbach in den Fjord? Darf ein Steig über Gletschereis führen (Karboden unter der Wächte)? Bleiben die Houdini-Reste `SM_K7_GLETSCHER__EIS` und `SM_K13_FROSTSEE__*` ausgeblendet? Wasserfälle mit über 150 m Fallhöhe mit dem Mountain-Set-Material bauen oder kürzer halten?
- tundra/heide: Aufeis (tundra_06) und Thermokarstsee (tundra_05) neben Frost/Gletscher in Ordnung? Steinringe Fundstück lassen oder zum Leuchtfeuer machen (vom Küstenweg teils sichtbar)? 4/4-Mischung in der Tundra in Ordnung? Ginster/Wacholder/Wollgras fehlen auf Fab → Ersatz (Sanddorn, gestauchte Jungkiefern, Binsen) oder Modelle außerhalb von Fab suchen? „Brushify – Moorlands Pack“ (Heidekraut, britischer Granit) schon in der Bibliothek? Darf der Pfad zum Trunkenen Grund den Rand von ROMAN_LOC_018 streifen?
- kueste/sumpf: Klippensteig (4,35 km) und Kap-Pfad bauen? (Kurzvariante nur bis zum Seefall → Vogelinsel und Nadeltor fallen weg.) Gelände unter dem Nadeltor bis −48 m absenken (über der 40-m-Grenze), sonst Bogen außen an den Pfeiler? Bleiben die alten Houdini-Klippenkacheln der Steilküste (K9)? Sumpf-See stellenweise eigene Farbe `schwarz_spiegel`? Irrlichter mit 2 schwachen Punktlichtern oder nur Nebel?
- **Inventar 13b (Abgleich):** `SM_lava_wall_01…09` fehlen im neuen `netze.csv` – bitte bei der Lava-&-Volcano-Nachladung mitnehmen (bis dahin Ersatz aus `/Game/Basalt`). Im Inventar stehen 31 statt 32 Eis/Schnee-Netze. Behalten die Eis-Netze `M_MS_Base_Trm`, und dürfen Basalt-Instanzen eigene Texturen bekommen? Dürfen `BP_FogBankCard`/`BP_FogBankVolume` als Akteure gesetzt werden, oder bleibt Nebel bei `lokaler_nebel`? Welche Assets stecken hinter den zwei fehlgeschlagenen Megascans-IDs?
- canyon/wueste/oedland: **Hollowstone Canyon kaufen?** (Preis ungeprüft; nötig für die Wabenwand, sonst Ersatz aus Sandstein-Netzen + Tafoni-Material). Megascans Desert Pack und Megascans Sandstone (Launcher-Vault) – schon in deiner Bibliothek? Ist die 22-m-Sterndüne direkt neben dem gebauten Palmental in Ordnung (Koordinator: ja, Prüfbild entscheidet)? Eigene prozedurale Decal-Texturen für Welle und Salzpfanne (Koordinator: ja, wie bei der Schwalbenwand)? Später einen „Canyonsteig“ bauen (Nordhälfte heute nur über Wasser erreichbar; +2–3 Orte möglich)?
