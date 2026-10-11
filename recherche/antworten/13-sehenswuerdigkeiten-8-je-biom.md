# Antwort Auftrag 13: Sehenswürdigkeiten neu – 8 je Biom (Phase 1 abgeschlossen)

Stand: 11.10.2026, abends. Bearbeitet von der Cloud-Session (Koordinator + 8 Biom-Agenten + Pfad- und Inventar-Agent).

## Kurzfazit

- **120 Orte in 15 Biomen, je 8 Orte.** Davon sind 52 Leuchtfeuer und 68 Fundstücke.
  - Fast überall gilt die Aufteilung 3 Leuchtfeuer / 5 Fundstücke.
  - Ausnahmen: Lava, Tundra und Küste mit 4 / 4, Fjord mit 7 / 1 (Panoramaweg, E46). Begründung in `sehens-katalog.md`.
- **Nur Landschaft:** Fels, Wasser, Eis, Feuer und Pflanzen. Keine Bauten, Ruinen, Knochen oder Menschenspuren und keine Houdini-`SW_*`-Assets.
- **Alle 120 Orte liegen 80–300 m vom nächsten Weg oder Pfad.** Dafür braucht es **18 neue Pfade, zusammen 20,6 km.**
  - Pfade gibt es in Lava, Gletscher, Frost, Fjord, Tundra, Küste und Ödland.
  - Das folgt Ferats Linie aus 13c: „lieber ein Pfad mehr als ein Ort weniger“.
  - Die Pfade stehen als `pfade` in den `standorte.json`, im Schema aus 13c.
- **Prüfer über alle Biome** (`skripte/sehens_lib/sehens_pruefen.py`, Wege + Pfade): **0 FEHLER, 1 WARNUNG.** Die Warnung: Der Pfad zum Trunkenen Grund (Tundra) streift den Rand der geplanten Stadt ROMAN_LOC_018.
  - Alle Mindestabstände halten: ≥ 350 m, in kleinen Biomen 200 m, ≥ 150 m zu Städten.
  - Alle Kameras nach SEHENS_FORMAT §8 (`_anmarsch`, `_held`, `_nah`, bei Leuchtfeuern zusätzlich `_fern`) sind vorhanden.
- **Download-Liste** ist auf dem Stand des Inventars 13b und aller Nachträge von Ferat:
  - gekauft: Nature Water FX, Basalt
  - im Laden: Megascans, Limestone, Desert Cliffs
  - gestrichen: Forest Cretaceous, Brushify
- **Phase 2 (Planer-Skripte)** beginnt mit dem Inventar 13b. Was noch geladen wird (Lava & Volcano, Coast & Dunes, Mountain, Limestone, Desert Cliffs, Nature Water FX), bekommt bis zum Inventar 13d einen Ersatz aus dem Bestand.

## Lieferung Phase 1

| Teil | Datei | Inhalt |
|---|---|---|
| A | [`sehens-downloadliste.md`](sehens-downloadliste.md), [`sehens/downloadliste.json`](sehens/downloadliste.json) | Kurzfassung für Ferat. Abschnitte: erledigt / läuft / erneut versuchen / noch fehlend (A/B/C mit Ort-IDs, Ersatz im Bestand) / Lücken ohne Paket / bewusst nicht aufgenommen |
| B | [`sehens-katalog.md`](sehens-katalog.md) | Übersicht, Pfadtabelle, je Biom eine Tabelle und je Ort der volle Abschnitt: was man sieht, Vorbild, Standort aus den Daten, Komposition, Detail-Ebenen, Wasser/Effekte/Licht, Gelände, Assets, Risiko |
| C | `sehens/<biom>/standorte.json` + `sehens/<biom>/<id>.png` (120 Draufsichten) | Orte mit Mitte, Radius, Feldern und Kameras (§8), Sicht- und Wegnachweis, Fußweg `pfad_cm`; Pfade unter `pfade`; die Draufsichten zeigen Gelände, Wege, Pfade, Wasser und geplante Elemente |
| C+ | `sehens/<biom>/katalog.md`, `sehens/<biom>/asset_bedarf.json` | Herleitung je Biom; Bestand mit echten Pfaden, Wünsche, Material-Instanzen (≤ 6), Bildwünsche mit Kameras |
| – | [`sehens/marker.json`](sehens/marker.json) | alle 120 Orte als Punktliste für Kartenmarker |
| D | [`sehens-STATUS.md`](sehens-STATUS.md) | Stand je Biom, Bildwünsche, Entscheidungen, offene Fragen |
| Baukasten | `skripte/sehens_lib/` | Laden 2 m (1 m vorbereitet), Hang/Krümmung/Abfluss, Wegabstand inkl. Pfade, Sicht vom Weg, Kandidatensuche, Draufsicht, Prüfer, Selbsttest |

Dazu die Antworten [`13b-sehens-downloads-stand.md`](13b-sehens-downloads-stand.md) und [`13c-antworten-offene-fragen.md`](13c-antworten-offene-fragen.md).

## Die 120 Orte in einem Satz je Biom

Die vollständigen Namen und Beschreibungen stehen in `sehens-katalog.md`.

- **aue:** Riesen-Stieleiche, Prallhang-Schwalbenwand und Treibholzwerder als Leuchtfeuer; Biberstau, Lilienrinne, Mondarm, Blautopf und Lianenhalle versteckt.
- **bergwald:** Felsnadel „Der Mönch“, Blitzkiefer und Säulenhain; Felsenmeer, Klemmblock-Klamm mit Schleierfall, Karsee, Windwurf und Wurzelstein.
- **elfenwald:** Mutterbaum, Nebelhain und Rotlaubhain; Kalktuff-Treppe, Farnschlucht, Blauer Grund, Schwammgrund und Wurzelbrücke.
- **dschungel:** Felsbogen Mondtor, Turmquelle und Steinwald aus Kalknadeln; Cenote „Blaues Auge“ (eigener türkiser See), Verborgene Lagune, Schluckhöhle, Garten der Riesen und Sinterhalle.
- **lava:** Schwarze Mauer, Schwefelgrund, Kraterkinder und Kraterreihe; Röhrenfenster, Klare Spalte, Basaltorgel (`/Game/Basalt`) und Glutauge. Dazu der Kratersteig mit Gipfelsteig zum Krater.
- **gletscher:** Gletschertor mit Séracbruch, Lawinenkegel und Wächte; Toteisloch, Moränensee, Gletschertöpfe, Nunatak und Gletscherschliff.
- **frost:** Frostsee mit Presseis, Raureifhain und Eisküste; Eisfall, Eisvorhang, Blockgletscher, Frostblumen und Glockenbach.
- **fjord:** Kanzel, Schleierwand, Trollzunge, Hängetal, Fjordkopf, Bergsturzkegel und alte Strandterrassen als Leuchtfeuer (Panoramaweg, Entscheidung E46); Brandungsgrotte versteckt.
- **tundra:** Pingo, Findling auf Rundhöcker, Eiswand und Fließtreppe; Trunkener Grund (Thermokarst), Schneetälchen, Steinringe und Wabenmoor.
- **heide:** Granit-Tor „Graue Burg“, Ginstergold und Wacholderprozession; Kolk, Wackelstein, Wollsackfall, Totengrund und Windkante.
- **kueste:** Granitpfeiler „Die Alten“, Vogelinsel, Nadeltor und Kreidewand; Seefall ins Meer, Gezeitenbank, Dünenkamm und Blasloch.
- **sumpf:** Ertrunkener Wald, Weidendom und Reiherhorst; Schwingrasen, Erlenbruch, Bultenfeld, Tellerweiher (Riesenseerose) und Irrlichtsenke.
- **canyon:** Sonnenfenster, Der Wäger und Rote Stufe; Flüsterschlucht, Hoodoo-Kessel, Kolke, Smaragdgumpe und Die Welle.
- **wueste:** Yardang-Flotte, Sterndüne und Die Wächter; Quelloase, Salzpfanne, Windkanter-Feld, Trockenes Wadi und Wabenwand.
- **oedland:** Rippenland, Regenbogenhang und Höllentor (brennender Gaskrater); Dornbusch-Senke, Kugelsteine, Schlammvulkänchen, Totenpfanne und Erdröhren.

## Wichtige Entscheidungen (aus 13c und dem Chat mit Ferat)

- **Pfade sind erwünscht.** Zusammen 18 Stück: Kratersteig mit Gipfelsteig, drei Gletschersteige, Frost- und Südsteig, Fjord- und Kanzelsteig, drei Tundra-Pfade, Klippensteig und Kap-Pfad an der Küste, dazu der Ödlandpfad mit drei Ästen.
  - Den vollen Klippensteig hat der Koordinator entschieden. Ein Steilküstensteig mit Blick auf Pfeiler, Vogelinsel und Nadeltor entspricht den Skellige-Referenzen.
  - Beim Ödlandpfad gilt Ferats Linie.
- **Gelände darf frei angepasst werden**, Stempel auch über 40 m (z. B. −48 m am Nadeltor).
- **Bestand statt Warten:**
  - Die Alte: Schwarzpappel ×1,3 oder `SM_dry_oak_0*`.
  - Erlen-Ersatz: Weiden, Pappeln, Birken.
  - Mönch: `veqnci0db_tier_2` auf Basalt-Sockel.
  - Windwurf und Säulenhain: Nicht-Nanite-Nadelbäume.
  - Mondtor: aus `SM_Cliff_01*`.
- **Material-Instanzen ≤ 6 je Biom**, z. B. Rotlaub (Kopie), Moos- und Schnee-Auflage, Tönungen.
- **Eigene Decal-Texturen:**
  - Brutröhren der Schwalbenwand: geliefert, `sehens/aue/decal_brutroehren*.png`.
  - Welle und Salzpfanne: geplant, gleiches Vorgehen.

## Grenzen und Risiken

- **Sicht:** Mehrere Fundstücke sind erst mit dem geplanten Geländestempel oder Gehölz voll verdeckt. Betroffen sind u. a.:
  - Mondarm, Erlenbruch, Flüsterschlucht, Welle
  - Kugelsteine, Totenpfanne, Erdröhren
  - die Frost-Fundstücke (brauchen einen Fels- oder Wallrahmen)

  Die Nachweise stehen in `standorte.json` unter `sicht` bzw. in den Katalogen. Die Planer in Phase 2 müssen diese Stempel und Gehölze setzen.
- **Teilweise sichtbar:** Steinringe und Wabenmoor (Tundra) sind vom höheren Küstenweg teilweise einsehbar.
- **Schwache Leuchtfeuer:** Ginstergold (Heide) wirkt nur über die Farbe, die Eisküste (Frost) ist nur von 6 Steigpunkten aus sichtbar.
- **Ungeprüft:** Bäume sind in den 2-m-Daten nur eine 4-m-Näherung, und der 1-m-Lader ist nur synthetisch getestet. Die Sicht im Editor entscheidet: Bildwünsche je Biom stehen in STATUS und in den `asset_bedarf.json`.
- **Preise und Größen** der Download-Liste sind ungeprüft, weil fab.com aus der Cloud nicht erreichbar ist.

## Weiter mit Phase 2

1. **Baukasten erweitern:**
   - Geländestempel (f32) und Bodenlagen (r8)
   - Instanzschreiber (FORMAT.md §3, Ebene `sw_<biom>`)
   - Akteure, Wasser und Effekte nach SEHENS_FORMAT
   - Pfad-Bodenband aus `pfade`
   - Vorschau-PNG und Prüfer für `orte.json`
2. **Planer je Biom** `skripte/sehens_<biom>/sehens_<biom>.py` + `_regeln.json`:
   - zuerst die Biome, deren Assets schon da sind (aue, bergwald, elfenwald, gletscher, frost, tundra, heide, sumpf)
   - dann die, die auf 13d warten (lava, kueste, canyon, wueste, oedland, dschungel, fjord), mit Ersatz und der Markierung `"optional": true`
3. **Test** mit `--daten2m vorlagen/daten/sehens`, Testbilder `sehens/<biom>/test_<id>.png`.

## Rückfragen

Die offenen Fragen stehen gesammelt in [`sehens-STATUS.md`](sehens-STATUS.md), Abschnitt „Noch offen“. Die wichtigsten:

1. Hollowstone Canyon kaufen (Wabenwand, Hoodoos)? Liegen Megascans Desert Pack und Megascans Sandstone schon in der Bibliothek?
2. Kommen `SM_lava_wall_01…09` mit der Lava-Nachladung zurück?
3. Darf der Tundra-Pfad zum Trunkenen Grund den Rand von ROMAN_LOC_018 streifen?
4. Nebel: Dürfen `BP_FogBankCard`/`BP_FogBankVolume` als Akteure gesetzt werden, oder nur `lokaler_nebel`?
