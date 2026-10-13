# 21 – Detailgrad Landschaft: Felsdeckung statt Textur (Referenz Ferat 13.10.)

Ferat (13.10. 22:20, nach einem Referenzbild aus einer Unreal-Hobbyszene): „auch die landschaft, sieht viel besser aus, wie können wir
witcher qualität erreichen, wenn wir nicht mal das erreichen was ein hobby unreal bastler schafft“. Messlatte bleibt **Witcher 4 (Demo) /
Witcher 3 Next-Gen für alle Biome** (`bilder/zielbilder/witcher_01…07.jpg`, Analyse `ANALYSE_WITCHER_2026-10-08.md`).

Kurz: Das Referenzbild zeigt praktisch keine Landschaftstextur als Fläche – die sichtbare Geländefläche besteht zu ≥ 80 % aus Felsnetzen
(Klippenmodule, Blöcke, Platten). Bei uns tragen Landschaftstextur und Houdini-Tönung das Bild; Netze sitzen nur auf Wandzellen (fs_plan:
Biom-Schwelle 40–55°, Wandhöhe ≥ 6 m) und decken 1–24 % der Feldfläche. Die Tabellen in §2 nennen nur **Referenz-Maß, unser Maß und die
Lücke**; unsere eigenen Zahlen-Ableitungen (aus Beschreibung und Witcher-Bildern) stehen getrennt in **Anhang A „nur zur Prüfung“** – es sind
keine Vorgaben, die Regeln sollen von euch kommen (§5). Zahlen aus Bildern sind Schätzungen (Pixelmessung noch offen, §2.1).

## 1. Referenz

REFERENZBILD (liegt nicht als Datei vor – Beschreibung des Hauptagenten, der es gesehen hat; Unreal-Hobbyszene, Ferat 13.10. 22:20):
Blick leicht von oben über ein Tal auf ein Klippenmassiv. Hinten: eine 100–150 m hohe Felswand aus waagrechten Schichtbändern
(Sandstein-/Kalkbänder, jede Stufe 2–6 m, Bänder versetzt, Grat oben mit Plateau, rechts ein senkrechter Felsklotz wie ein Turm, links fällt
die Wand gestuft zum Meer ab). Unter der Wand: ein Hang ganz aus Halden und Blöcken (kantige Brocken 1–8 m, Platten, Schutt dazwischen),
nirgends glatter Boden; darin Gruppen von Nadelbäumen (Fichten/Kiefern 8–15 m, 3–8 je Gruppe, dazwischen Lücken), Gras nur als Flecken
zwischen den Steinen. Mitte: ein von Blöcken verstopfter Bach, Wasser dunkel mit Gischt an Steinen. Vordergrund: große flache Felsplatten
und Klötze 3–10 m mit Grasbüscheln und Flechten in den Fugen, Moos-Säume. Geschätzt ≥ 80 % der sichtbaren Geländefläche ist Felsnetz
(Klippenmodule, Blöcke, Platten), ≤ 20 % Gras/Boden. Hintergrund: Dunst, Meer, weitere Berge. Maßstab konsistent: Bäume gegen Blöcke gegen
Wand. Keine Landschaftstextur als Fläche sichtbar, kein nackter Erdhang.

Für den Vergleich wichtig (fehlt sonst in §2):
- **Kamera:** Referenz = leicht von oben über ein Tal, Wand 100–150 m im oberen Bilddrittel. Damit Pilotbilder vergleichbar werden, braucht der
  Pilot einen festgelegten Prüfbild-Standpunkt (Schätzung aus der Beschreibung: 300–500 m Abstand zur Wand, 20–40 m über dem Talboden, Blick
  10–20° nach oben). Unsere heutigen Prüfbilder (GEF_*, BERG11_*) stehen anders (Bachnähe von unten bzw. Rundgang) – nur bedingt vergleichbar.
- **Küstenanschluss:** „links fällt die Wand gestuft zum Meer ab“ = Stufen bis ans Wasser. A5/B4/B5 sind Küstenfelder, der Klippenplan 2.1
  verkleidet dort nur die Wandfront (2 Reihen), kein Stufenanschluss ans Meer – eigene Lücke, in §2 nicht als Zeile geführt.
- **Keine Heide, keine Blumen:** Die Referenz hat weder Heide noch Blumenwiese; unser p2-Tal (GEF_C2_p2_talkopf, P2C) ist 95–100 % Heide/Gras
  (D2 2 813, C2 1 237 Heide-Instanzen gleichmäßig) → eigene Lücke (§2.2 Zeile „Gras als Flecken“).
- **„Wasser dunkel“** hängt bei uns am gespeicherten Wasser-Material (Variante F + S6: Absorption 222/1000/1250, Wirbel/Schaum 0, Grund
  dunkelbraun) – ist seit 13.10. 19:00 weitgehend erreicht und hier kein Thema; Blöcke im Bach und Gischt sind es (§2.1).

## 2. Befund je Blickwinkel

Bildquellen: unsere Prüfbilder `GEF_D2_p2_quelle`, `GEF_D2_p2_bergrinne`, `GEF_C2_p2_schlucht` / `_uebersicht` / `_talkopf`,
`P2C_C2_t500_schraeg` (lokal `Saved/Screenshots/WindowsEditor/`, noch nicht im Repo – auf Wunsch nach `bilder/detailgrad/`),
`BERG11_D2/A5/B4_rundgang` (`bilder/sehens13/`). Daten: `hoehe.f32` (1-m-Raster), Felsschalen-Protokolle `fertig_<Feld>.json`,
Klippenplan 2.1, Bachdekor/Uferplan p2, `steilhang_je_feld.md`.

### 2.1 Fels, Klippen, Halden – Anteil Felsnetz an der sichtbaren Geländefläche

**Referenz** (Beschreibung + Witcher 01–07):
- ≥ 80 % der sichtbaren Geländefläche Felsnetz (Klippenmodule, Blöcke, Platten), ≤ 20 % Gras/Boden; keine Landschaftstextur als Fläche, kein nackter Erdhang.
- Klippenwand 100–150 m aus waagrechten Schichtbändern, jede Stufe 2–6 m, Bänder gegeneinander versetzt, oben Grat mit Plateau, rechts
  senkrechter Turmklotz, links gestuft zum Meer – 3D-Stufen, nicht Streifen in der Textur.
- Hang unter der Wand ganz aus Halden: kantige Blöcke 1–8 m, Platten, Schutt dazwischen, nirgends glatter Boden (abgeleitet: Blöcke berühren
  sich, ≥ 8–15 Blöcke je 100 m² plus Schutt 0,2–0,8 m).
- Vordergrund: flache Platten und Klötze 3–10 m, Grasbüschel und Flechten in den Fugen, Moos-Säume (Witcher 04: Klippenkante im Vordergrund =
  100 % Platte mit Flechten; Witcher 06: Blöcke 5–15 m links, 30–50 % eingegraben, Schnee obenauf).
- Bach von Blöcken verstopft (Blöcke 1–3 m im Wasser), Wasser dunkel, Gischt an den Steinen; Witcher 01/03: Ufer und Bett aus Steinen
  0,3–1,5 m, Geröll 0,2–0,5 m dicht, Totholz.
- Nadelbäume 8–15 m in Gruppen von 3–8 mit Lücken; Gras nur Flecken zwischen den Steinen; Maßstab Baum–Block–Wand stimmig.
- Witcher 06/07 Hintergrund: Berge mit Farbbändern rot/grau, Dunst an den Gipfeln, Meer/weitere Berge im Dunst.

**Unsere Bilder/Daten:**
- `GEF_D2_p2_quelle` (Bergrinne von unten): Bergflanke links = helle Fels-Landschaftstextur als glatte Fläche (~55–65 % des Bildes, Schätzung),
  1 Felsklotz ~8–10 m oben links, 1 Gruppe von 3–5 Blöcken 2–4 m in der Mitte, rechts oben Schichtfels-Schalen; Felsnetz-Anteil ~15–20 %;
  Rinne nur Kleinsteine 0,2–0,5 m, dazu 1 liegender Stamm quer im Bach und ≥ 1 bemooster Block unten rechts; rechter Hang = Textur mit
  Streu-Pflanzen.
- **Pixelmessung steht aus:** Alle Felsnetz-Anteile aus Bildern (3–25 %) sind Schätzungen. Die vorgeschlagene Messung (SceneCapture mit
  `hide_actor_components`, Landschaft ausgeblendet → Pixelanteil Netz/Landschaft) ist für GEF_D2_p2_quelle, GEF_C2_p2_uebersicht und
  BERG11_A5 noch nicht gemacht (braucht den Editor, Ferat lädt gerade Rural Australia); wir liefern sie nach `bilder/detailgrad/` nach.
- `GEF_D2_p2_bergrinne` (von oben): rechts Kalkwand aus Schalen 2–6 m (~25 % des Bildes), links KEIN Block, nur ~10 Kleinsteine 0,2–0,4 m auf
  ~200 m², Boden beidseits = Fels-/Sandtextur als Fläche ~50 %.
- `GEF_C2_p2_schlucht` / `_uebersicht` / `_talkopf`: Talboden und Hänge = Gras-/Trockengras-Textur als Fläche (Übersicht rechter Hang ~100 %
  Textur, nur Büsche; unten Mitte ein Weg), Berg hinten = helle Felstextur mit verstreuten Schalen-Flecken 2–6 m (ca. 1 je 100–200 m² Wand),
  keine 3D-Stufen; Kiefernwald gleichmäßig (Einzelbaum-Raster 4–8 m, keine Gruppen/Lücken); Felsnetz-Anteil 3–10 %.
- `BERG11_D2_rundgang`: Berg = Textur mit Streifenmuster (V17-Schichtbänder in der Textur) + Schalen 3–8 m verstreut, sichtbare Wanddeckung
  ~25–35 %, runder Gipfel ohne Grat/Plateau, Schnee als Fläche, keine Halde am Fuß.
- `BERG11_A5_rundgang`: Wand = Streifen-Textur mit 10–15 dunklen Schalen-Flecken auf ~5 ha, dazu **2 weiße, unstrukturierte Stücke** an der
  Wand (oben Mitte; Material fehlt oder Schnee-Auflage MI_EL_Auf_*? ungeprüft); Grashang ~95 % Textur mit ~30 sichtbaren flachen Platten 2–5 m
  (~0,03 je 100 m²) – das sind die 167 `platte`-Stücke (rcygn) des Klippenplans 2.1 am Wandfuß, sie liegen auf, nicht eingegraben; Felsnetz
  ≤ 5 % der sichtbaren Fläche. Daten: Klippenplan 2.1 A5 = 357 Stücke (110 Hero, 70 Reihe 2, 167 Platten, 10 Geröll), Front 1 (2,41 ha,
  Median 48,1 m hoch) Deckung 65,2 % (bis 30 m Höhe 73,3 %); Felsschalen A5 432 Stücke, Wanddeckung 43,9 %; Felsgruppen R5 A5 19 Akteure +
  3 245 Instanzen.
- `BERG11_B4_rundgang`: dichteste Wand (3 213 Schalen, Wanddeckung 64 % gemessen, sichtbar ~50–60 %), aber Rest Textur, Grat = Baumreihe
  1 Baum je ~5 m in Linie, kein Plateau, keine Blöcke/Halde am Wandfuß.
- `P2C_C2_t500_schraeg` (Talkaskade): Ufer = Heide-/Trockengras-Textur flächig, Steine nur im Bett 0,3–1 m (~15 je 10 m), keine Blöcke > 1 m
  neben oder im Bach, Becken regelmäßig 3–4 m. Daten p2: 21 448 Bachdekor-Teile auf 788 m, davon 6 155 unter Wasser und 4 232 SmallStonesPack
  (≤ 0,5 m), Hindernisse 1 362 (≤ 40 % Bettbreite = ≤ ~1 m), 9 Flussfelsen entfernt / 3 gesenkt → Blöcke ≥ 1 m im Bach ≈ 0.
- **Systemgrund (Daten):** Felsschalen-Planer setzt nur auf Wandzellen (fs_plan: Biom-Schwelle 40–55°, Wandhöhe ≥ 6 m; `fertig_<Feld>.json`
  `wandzellen`): D2 178 058 = 17,8 ha, C2 239 953 = 24,0 ha, A5 25 224 = 2,5 ha, B4 388 011 = 38,8 ha; Deckung dort 0,693 / 0,677 / 0,439 /
  0,639 → Netz auf 12,3 / 16,2 / 1,1 / 24,8 ha = **12 % (D2), 16 % (C2), 1,1 % (A5), 24 % (B4)** der Feldfläche (101,6 ha). Achtung, zwei
  „Wand“-Flächen: `steilhang_je_feld.md` zählt ≥ 50° (D2 19,1 ha, C2 24,9 ha, A5 7,3 ha, B4 41,6 ha), fs_plan nur Wandzellen mit Wandhöhe
  ≥ 6 m (Binnenfelder ±2 ha gleich, A5 2,5 statt 7,3 ha – Meer-Sonderbehandlung, siehe §3.3). Steile Hänge 38–50° (D2 22 ha, C2 17 ha,
  B4 27 ha, B5 28–33 ha je Meer-Methode) bekommen 0 Schalen, nur die Fels-LAGE als Textur (Fels-Lage auf steil D2 45 %, C2 59 %, B4 70 %).
  Fußbrocken je Feld (fs_plan `je_klasse.fuss`, 07.10.) D2 37, C2 8, A5 8, B4 75 (= 0,004–0,008 je 100 m²); in A5/B4 hat die
  Felsgruppen-Ebene (11.10.) diese FT_EL_FS_*-Füller laut `plan.json` `entfernen` möglicherweise ersetzt → Dichte heute dort aus der
  Felsgruppen-Ebene (§3.1 Halde), ungeprüft.
- Gut/erfüllt: Kleinsteine im Bachbett dicht; Heide-/Blumeninseln am Talkopf; B4-Wand ist die einzige, die als Felsnetz liest; Nahtprüfung
  0 Lücken, Kollision 0 Löcher.

| Element | Referenz-Maß | Unser Maß | Lücke | Wirkung |
|---|---|---|---|---|
| Felsnetz-Anteil an der sichtbaren Geländefläche (Berg-/Steilszenen) | ≥ 80 % Felsnetz, ≤ 20 % Gras/Boden; Witcher 06 Vordergrund ~50 % Blöcke, Witcher 04 Vordergrund 100 % Platte | Bild (Schätzung, Pixelmessung offen): D2 Quelle 15–20 %, D2 Bergrinne ~25 %, C2 Schlucht/Übersicht 3–10 %, A5 ≤ 5 %, B4 ~50 % nur auf der Wand; Daten: Schalen nur auf Wandzellen → 12 % (D2), 16 % (C2), 1,1 % (A5), 24 % (B4) der Feldfläche | Faktor 3–25 unter der Referenz; Hänge 25–50° ganz ohne Netz; Prüfmaß „Pixelanteil Netz je Bild“ fehlt noch | groß |
| Halden/Blockhang unter den Wänden (Größenklassen, Dichte, Einbettung) | Hang ganz aus Blöcken 1–8 m + Platten + Schutt, nirgends glatter Boden; Witcher 06: Blöcke 5–15 m, 30–50 % eingegraben | Halde = 0: nur Fußbrocken (D2 37, C2 8, A5 8, B4 75 je km² = 0,004–0,008 je 100 m²); Hänge 38–50° (D2 22 ha, C2 17 ha, B4 27 ha) tragen nur Fels-Lage als Textur; Felsgruppen (11.10.): B4 150 Akteure + 13 039 Instanzen (≈ 1 100 Blöcke = 0,11 je 100 m²), A5 19 Akteure + 3 245 Instanzen (block 210) | Halde fehlt als Element; Haldenhänge 25–45° unter Wänden sind da (4,6–15,7 % der Feldfläche, §2.3), alle ohne Netz; Prüfraster für 25–50° fehlt | groß |
| Klippen als 3D-Schichtbänder (Bandhöhe, Versatz, Grat/Plateau, Turmklotz) | Wand 100–150 m, Stufen je 2–6 m, Bänder versetzt, Grat mit Plateau, senkrechter Turmklotz; Witcher 06/07: Bänder rot/grau mit Simsen | Bänder nur als Textur-Streifen (V17 Band 0,9 / Wand 1,4) auf glattem Gelände (BERG11_D2, _A5); 3D nur Schalen-Flecken 2–8 m: A5 Front 1 Deckung 65 % (bis 30 m 73 %), Schalen-Wanddeckung D2 69 %, C2 68 %, A5 44 %, B4 64 % – sichtbar 25–60 %; 0 Plateaus, D2-Gipfel rund, B4-Grat = Baumreihe | Keine 3D-Stufen (Stufenzellen 0,0 %), 0 Plateaus, 0 Türme; Reihen-/Bandlogik nur im Küsten-Klippenplan; Nordic-Bandmodule 2–6 m fehlen | groß |
| Nackte Erd-/Texturflächen (Landschaftstextur als Fläche, Houdini-Tönung trägt das Bild) | 0 % Landschaftstextur als Fläche, kein nackter Erdhang; Witcher 01/03: Boden immer 4–6 Schichten + 3D-Kleinzeug | Bild: D2 Bergrinne ~50–65 % Textur, C2 Übersicht rechter Hang ~100 %, A5 Grashang ~95 %, Wände D2/C2 50–70 % Textur; Daten: Fels-Lage auf steil = reine Textur (D2 45 %, C2 59 %, B4 70 % der steilen Pixel) | Textur 50–100 % der Hangflächen statt 0 %; Band 38–50° ohne Netz 17–33 ha je Feld; Prüfmaß „Fels-Lage ≥ 38° ohne Netz“ fehlt (Daten dafür vorhanden) | groß |
| Vordergrund-Platten 3–10 m mit Fugenbewuchs (Gras, Flechten, Moos-Säume) | Platten/Klötze 3–10 m, Grasbüschel + Flechten in den Fugen, Moos-Säume; Witcher 04 Vordergrund = Platte mit Flechten | A5 Hang: 167 Klippenplan-Platten (rcygn) am Wandfuß, ~30 sichtbar, 2–5 m, ~0,03 je 100 m², aufliegend; Felsgruppen-Rolle „platte“ A5 0 / B4 1 / D3 379; Fugenbewuchs 0 (Planer schließt Fugen, bewächst sie nicht); Flechten/Moos nur als Auflage-Material MI_EL_Auf_* (tundra/frost) | Plattenfelder fehlen (kein Planer), Fugenbewuchs 0, Moos-Säume 0, Flechten-Material für bergwald/kueste nicht kalibriert | mittel |
| Bach von Blöcken verstopft (Blöcke im Wasser, dunkles Wasser, Gischt) | Blöcke 1–3 m im und über dem Wasser, „verstopft“, Gischt an den Steinen; Witcher 01/03: Ufer aus Steinen 0,3–1,5 m, Bett voller Geröll | p2: 21 448 Teile/788 m, 4 232 SmallStonesPack (≤ 0,5 m), 6 155 unter Wasser; Hindernisse 1 362 (≤ ~1 m); Blöcke ≥ 1 m im Bach ≈ 0 (9 Flussfelsen entfernt); Bild P2C: Steine 0,3–1 m, ~15 je 10 m, Becken regelmäßig 3–4 m; Ufer 0,16 m über Spiegel | 0 Blöcke ≥ 1 m im Wasser (SWR-Front verträgt heute keine), Becken gleichförmig, Gischt nur an 2 Wasserfällen; Uferstufe läuft (16h-N6) | mittel |
| Nadelbaum-Gruppen in der Felszone (Gruppengröße, Lücken, Grat) | Fichten/Kiefern 8–15 m in Gruppen von 3–8, Lücken dazwischen, Gras nur Flecken; Witcher 04/06: Gruppen + Lichtungen, kein Raster | C2 Schlucht/Übersicht: gleichmäßiger Kiefernwald, Abstand 4–8 m, kein Gruppen/Lücken-Muster; B4 Grat: Baumreihe 1 je ~5 m; Witcher-Durchgang (Haine) in Felszonen nicht sichtbar | Raster statt Gruppen (Altbestand wird nie gelichtet), Grat-Reihen, Hauptbäume 16–29 m statt 8–15 m | mittel |
| Maßstabsanker Baum–Block–Wand | Maßstab konsistent: Bäume gegen Blöcke gegen Wand lesbar | BERG11 D2/A5: Wand ohne Blöcke am Fuß und ohne 3D-Stufen → Textur-Kachelung (Fels 550) ist die einzige Größenangabe, Berg wirkt klein; Bäume nur als Saum oben | Kein Maßstabsanker im unteren Wanddrittel (weder Block 3–8 m noch Baumgruppe noch Stufe) | klein |

### 2.2 Bewuchs – Nadelbaumgruppen, Grasflecken, Büschel in Fugen, Moos/Flechten, Totholz

**Referenz** (Beschreibung; Witcher 03/04/06/07 nur zur Einordnung):
- Nadelbäume 8–15 m in Gruppen von 3–8, zwischen den Gruppen Lücken; Gruppen stehen IM Blockhang zwischen Brocken 1–8 m, nicht auf glattem Boden.
- Gras nur als Flecken zwischen den Steinen; ≤ 20 % Gras/Boden, ≥ 80 % Felsnetz. Abgeleitet: Fleckengröße 1–5 m², kein geschlossener Teppich.
- Vordergrund-Platten 3–10 m mit Grasbüscheln und Flechten in den Fugen, Moos-Säume an den Rändern – jeder Fels trägt Bewuchs an Kanten/Fugen, die Flächen bleiben Stein.
- Maßstab: Baum 8–15 m gegen Block 1–8 m gegen Wand 100–150 m (Stufen 2–6 m) – Bäume klein vor der Wand, groß neben den Blöcken.
- Kein Laubbaum, keine Heide-/Blumenwiese am Hang; Farbe aus Nadelgrün, Moos, Flechte, dunklem Wasser und Gischt.
- Totholz: in der Referenz NICHT erwähnt. Witcher 3 Bild 03: liegender Stamm quer im Bachbett, Steine mit Moos; Bild 06: Totholz und Büsche
  zwischen Blöcken, Baumgruppen 3–10 mit Lichtungen; Bild 07: Nadelwald mit 3 Höhenklassen und Lärchen-Rost.
- Witcher 4 Bild 04 (Klippenkante): Nadelbäume in Grüppchen von 2–5 mit nacktem Fels dazwischen, verschiedene Höhen – keine Reihe.

**Unsere Bilder/Daten:**
- `GEF_C2_p2_uebersicht` (Hangwald Bergflanke): geschlossener Kiefernbestand, Abstand ~5–7 m, alle ~12–15 m (Höhenstreuung ≤ 20 %), Waldgrenze
  scharf gegen gelbe Grasfläche rechts (100 % Textur, 0 Blöcke), oberhalb nackte Schichtwand als Textur; kein Totholz, keine Lichtungen.
- `GEF_C2_p2_schlucht` (von oben): dichte Kiefern im Raster, Boden gelbgrüner Grasteppich ~95 %, Felsnetze ≈ 0, keine Lücken > 15 m.
- `GEF_D2_p2_quelle`: Boden = helle Landschaftstextur ~75 % glatt, 3–4 Felsnetze am Rand, Kiefern nur als Linie auf dem Grat (~15), Kleinpflanzen
  (Heide/Farn) gleichmäßig gestreut; im Bach 1 liegender Stamm quer und ≥ 1 bemooster Block (unten rechts), die übrigen Bachsteine 0,2–0,8 m
  ohne Moos – „0 Moos, Totholz nur am Talkopf“ gilt hier also nicht.
- `GEF_D2_p2_bergrinne`: 5–6 Birken (~10 m) über der Rinne statt Nadelbäume; Fels rechts 0 % Moos/Flechte; Heidebüschel gleichmäßig (keine Inseln).
- `GEF_C2_p2_talkopf` + `P2C_C2_t500_schraeg`: Heide-/Graswiese 95–100 % beidseits, Steine NUR im Bett (0,3–0,8 m, ~25 sichtbar, 0 mit Moos),
  keine Blöcke/Platten im Hang; 1 stehender Totstamm.
- `BERG11_B4_rundgang`: ~25 Kiefern in EINER Reihe entlang der Gratkante, gleiche Größe; Wand ohne Bewuchs in Fugen.
- `BERG11_A5_rundgang`: Grashang ~90 % Textur, 5–8 Einzelkiefern (~8 m), ~15 flache Platten 1–3 m auf ~2 ha, keine Gruppen, keine Büschel an Platten, keine Moos-Säume.
- `BERG11_D2_rundgang`: Gipfel ohne Bewuchs, nur Textur + dunkle Felsnetze; Bäume erst unten links.
- Planer-Zahlen (wit1, nur Zusätze): D2 (1 km²) 45 Hangwald-Gruppen, 6 Haine, 368 Waldzellen Altbestand, neu 63 Kiefer / 189 Jungkiefer / 13 Tanne /
  60 Birke, Totholz 8 stehend + 19 liegend + 55 Stümpfe, Großfelsen 12, Bergsteine 116. C2: 20 Hangwald, 2 Haine, 156 Waldzellen, 6 Großfelsen.
  A5: 14 Hangwald, 17 Kiefern, 6 Großfelsen. B4: 2 Hangwald, 769 Waldzellen.
- Planer-Regeln (`wit_plan.py`): Hangwald = 3–7 Bäume, Radius 6–12 m, Mindestabstand 5 m, Zelle 34 m; NUR wo Felslage ≤ 0,6 und Baumabstand ≥ 9 m →
  Bäume meiden Fels systematisch; 0,3 Großfelsen je Gruppe; Haine 3–11 Bäume, Radius 7–15 m, 6 % stehendes Totholz; Altbestand wird nicht gelichtet.

| Element | Referenz-Maß | Unser Maß | Lücke | Wirkung |
|---|---|---|---|---|
| Baumgruppen statt geschlossener Bestand (Hangwald) | 3–8 Nadelbäume je Gruppe, klar getrennt, Lücken dazwischen | C2/D2-Flanke: durchgehender Bestand, Abstand ~5–7 m, Lücken < 15 m; Planer legt 3–7er-Gruppen an, Altbestand (D2 368, B4 769 Waldzellen) bleibt ungelichtet | Bestand statt Gruppen; Ausdünn-Maske für den Altbestand fehlt (`remove_foliage_by_mask` vorhanden) | groß |
| Standort der Bäume: zwischen Blöcken statt auf Gras | Jede Gruppe steht IM Blockhang (Brocken 1–8 m rundum) | Bäume nur auf Landschaftstextur; Planer verbietet Felslage > 0,6; Großfelsen D2 12 / C2 6 / A5 6 je km² = 0,3 je Gruppe | Bäume meiden Fels systematisch; Block : Baum ≈ 0,3 : 5; kein gemeinsamer Planer Baum + Block | groß |
| Gras als Flecken zwischen Steinen statt Teppich | Gras/Boden ≤ 20 %, nur Flecken zwischen Steinen; keine Heide, keine Blumen | Talkopf/Talkaskade 95–100 % Heide/Gras, Flanke rechts 100 % Textur, A5-Hang ~90 %; Heide gleichmäßig gestreut (D2 2 813, C2 1 237 Instanzen ohne Inseln) | Teppich statt Flecken (~5× zu viel Gras/Heide); Maske „Gras aus unter Blöcken/Schutt“ fehlt | groß |
| Büschel, Flechten, Moos-Säume an Platten/Klötzen | Grasbüschel + Flechten in JEDER Fuge, Moos-Säume an den Rändern | D2-Quelle ≥ 1 bemooster Block; Talkopf 0 von ~25 sichtbaren Bachsteinen mit Moos; Felsnetze D2/A5 ohne Fugenbewuchs; MI_EL_Auf_* in den Bildern nicht sichtbar | Fugenbewuchs 0, Moos-Säume 0, Flechten 0 (Auflage nur tundra/frost kalibriert) | mittel |
| Höhen-/Altersmischung in der Gruppe | 8–15 m (1:1,9); Witcher 07: 3 Höhenklassen + Farbwechsel | C2-Flanke Kronen fast gleich hoch (Streuung ≤ 20 %); Jungkiefern im Planer (D2 189), im Bild unsichtbar | Streuung ≤ 20 % statt ~1:1,9; keine Höhenklassen-Regel im Planer | mittel |
| Baumreihen auf Graten und Kanten | Grat/Plateau ohne Baumreihe; Witcher 04: Grüppchen 2–5, nackter Fels dazwischen | B4: ~25 Kiefern in Linie am Grat, gleiche Größe; D2-Quelle: ~15 Kiefern als Linie | Reihen auf 2 von 3 geprüften Graten; Grat-Regel fehlt | mittel |
| Baumart am Felshang (Nadel statt Laub) | Nur Fichten/Kiefern am Block- und Wandhang | D2-Bergrinne 5–6 Birken; Biom bergwald Birke 20 %, A5 21 Birken zu 17 Kiefern | Birken am Felshang (Artgewicht tundra 0,65, bergwald 0,2); keine Standortregel Birke–Wasser | klein |
| Totholz (nicht in der Referenz beschrieben) | Referenz: keine Angabe. Witcher 03: 1 liegender Stamm im Bach; 06: Totholz zwischen Blöcken | D2-Quelle 1 liegender Stamm quer im Bach; Talkopf 1 stehender Totstamm; Flanke C2 0; Planer D2 8 stehend / 19 liegend / 55 Stümpfe = ~0,2 liegende je ha | Nur Dichte (Werkzeug und Netze da); Bachdekor hat keine Totholz-Klasse | klein |

### 2.3 Geländeform und Maßstab – Wand → Halde → Tal, Stufigkeit, Bachbett, Nah/Mittel/Fern

**Referenz:**
- Drei klar getrennte Zonen: Wand (100–150 m, nahezu senkrecht, Stufen 2–6 m, Bänder versetzt, Plateau, Turmklotz) → Halde (ganz aus Blöcken 1–8 m,
  Platten, Schutt, kein glatter Boden) → Tal (Platten 3–10 m, Bach).
- Felsnetz ≥ 80 % der sichtbaren Fläche; Landschaftstextur nirgends als Fläche; Gras nur Flecken in Fugen (≤ 20 %).
- Maßstabskette: Nadelbaum 8–15 m : Block 1–8 m : Wand 100–150 m ≈ 10 : 3 : 120; Bäume in Gruppen 3–8 mit Lücken.
- Bach von Blöcken verstopft (Bettgröße), Wasser dunkel, Gischt; Ufer = Blöcke, nicht Wiese.
- Staffelung: Vordergrund Platten 3–10 m mit Büscheln/Flechten/Moos-Säumen; Mitte Halde + Baumgruppen; Fern Dunst, Meer, weitere Berge.
- Witcher 06/07 bestätigen: Wände aus Türmen/Pfeilern mit 5–20 m Felsflächen, Schnee nur auf Simsen, Dunst an den Wänden; Vordergrund-Felsen
  5–15 m (06) bzw. 2–5 m mit Grasbüscheln (04).

**Unsere Daten/Bilder** (`hoehe.f32`, 1 m, Felder D2/C2/A5/B4):
- Hangwinkel: D2 57,6 % der Fläche > 30° (30–45°: 30,5 %, 45–60°: 20,1 %, > 60°: 7,0 %), B4 79,8 % > 30°, C2 48,7 %, A5 23,5 % – aber
  **Stufenzellen** (Zelle < 5° in einem 7 × 7-m-Umfeld mit > 20°) **0,0 %** (D2 0,03 %, C2 0,02 %, B4 0,05 %, B5 0,03 %, A5 0,01 %): die
  Hänge sind steil UND glatt, eine durchgehende Rampe ohne Wand/Halde/Tal-Zonierung. **Haldenhang unter Wänden** (Definition: `hoehe.f32`,
  `np.gradient` 1 m; Wand = ≥ 50°; Hang 25–45° auf Land im Umkreis 40 m einer Wandzelle, Zellhöhe unter der mittleren Wandhöhe im Umkreis):
  **D2 15,4 ha = 15,2 %, C2 7,3 ha = 7,2 %, B4 11,8 ha = 11,6 %, B5 16,0 ha = 15,7 %, A5 4,6 ha = 4,6 %** der Feldfläche (eine frühere
  Fassung nannte 0,6–2,1 % – Definition nicht mehr nachvollziehbar, ersetzt). Folge: die Hänge für Halden SIND da, nur ohne Netz –
  Halde ist zuerst eine Netz-Aufgabe (Blöcke/Schutt auf 25–45°), ein Höhenplan (Schüttkegel) wäre nur für Stufen/Plateau/Turm nötig.
- Felsnetz-Bedeckung je Feld (Schalen nur auf Zellen ≥ 35° mit Wandhöhe ≥ 6 m, Deckung × Wandanteil): D2 ≈ 12 % (0,693 × 17,5 %), C2 ≈ 16 %,
  B4 ≈ 24 %, A5 ≈ 1 %. Fußbrocken D2 37, C2 8, B4 75, A5 8 je 102 ha = 0,004–0,007 je 100 m². Alle Felsstücke D2 1 510 (0,015 je 100 m²).
- `GEF_D2_p2_quelle`: glatter beiger Hang ohne Halde, 5–8 Einzelblöcke 2–4 m, Kiefern ~20 m, rechte Wand mit gestreckter Textur (senkrechte
  Schlieren), Uferkante 1-m-facettiert (Treppen).
- `GEF_C2_p2_uebersicht` / `BERG11_D2` / `BERG11_B4`: Berg = runde Kuppe in einer Farbe (beige), Felsschalen aus 300–650 m Relief (D2 26–446 m,
  B4 34–684 m) als schwarze Punkte („Kopfsteinpflaster“), Tönung als senkrechte Streifen 20–40 m statt waagrechter Bänder, keine Stufen, kein
  Plateau, kein Turm; Grat-Zellen 0,2 % (D2/C2) bis 1,2 % (A5).
- `BERG11_A5`: Wand konvex-glatt, Textur-Band ~0,5–1 m wiederholt sich (Kachelung 550 cm), Grashang mit aufgelegten dünnen Platten-Rechtecken =
  die 167 `platte`-Stücke (rcygn) des Klippenplans 2.1 – sie liegen auf, nicht eingegraben. (Der Wert `platte_duenn_ueber_4m2` = 658 in
  fertig_D2.json ist ein Prüfwert des Schalen-Planers – flache Oberseiten von Wandschalen, = `tisch_c_ueber_4m2` –, kein Zähler aufgelegter
  Platten; A5 hat dort 0.)
- `GEF_C2_p2_schlucht`: geschlossener Kiefernbestand, Abstand ~4–6 m, Höhe einheitlich ~18–22 m, flacher gelber Boden ohne Blöcke; `BERG11_B4`:
  Baumreihe auf dem Grat wie eine Hecke.
- `P2C_C2_t500_schraeg` / `GEF_C2_p2_talkopf`: Bach als Rinne im Heideteppich, Steine 0,2–0,8 m, keine Blöcke ≥ 1,5 m, Ufer bündig (0,16 m über
  Spiegel), 26 Becken/189 m alle 3–4 m gleich. Daten: Bachdekor C2+D2 21 448 Teile, Kiesel 8 509, Steine ab Bachstein-Klasse ≈ 2 900 (3,7 je m);
  größere Klassen (Lippenfels 137, Bettfels 19, Randfels 167 = 0,4 je m) werden aus der SWR-Hindernisliste gefiltert (Teil ≤ 40 % Bettbreite).
- **Was aus unserer Sicht zuerst bricht (Hypothese aus den Bildern, keine Vorgabe – §5 f fragt nach eurer Reihenfolge):** 1. glatte Hänge
  ohne Halde unter den Wänden, 2. Felsgröße zu klein für die Wandhöhe (Punktmuster), 3. keine Stufen/Bänder in Wänden, 4. Bach ohne Blockwerk
  mit gleichförmigen Becken, 5. Wald als Fläche statt Gruppen, 6. 1-m-Facetten an Uferkanten.

| Element | Referenz-Maß | Unser Maß | Lücke | Wirkung |
|---|---|---|---|---|
| Zonierung Wand → Halde → Tal | 3 Zonen: Wand 100–150 m fast senkrecht, Halde aus Blöcken (kein glatter Boden), Tal | durchgehende glatte Rampe: D2 57,6 % > 30°, Stufenzellen 0,0 %; Haldenhang 25–45° unter Wänden D2 15,2 %, C2 7,2 %, B4 11,6 %, B5 15,7 %, A5 4,6 % der Feldfläche – ohne Netz | Zonen sind im Gelände angelegt (Hang unter Wand vorhanden), aber nicht lesbar: keine Blöcke auf dem Haldenhang, keine Stufen an der Wand | groß |
| Felsnetz-Bedeckung | ≥ 80 % Felsnetz, ≤ 20 % Gras/Boden, keine Textur als Fläche | D2 12 %, C2 16 %, B4 24 %, A5 1,1 % (nur fs_plan-Wandzellen, Deckung 0,44–0,69) | 1–24 % statt ≥ 80 % | groß |
| Blockgröße und Maßstabskette | Baum 8–15 : Block 1–8 : Wand 100–150 m ≈ 10 : 3 : 120 | Kiefer 18–22 m : Fels 1–3 m : Relief 300–650 m ≈ 20 : 1,5 : 400 → Felsen als Punkte; Fußbrocken 0,004–0,007 je 100 m² | Felsen 2–3× zu klein, Bäume ~2× zu groß für die Kette; Blöcke 4–8 m fast nicht gesetzt (Netze dünn, §3.1) | groß |
| Wandstufen und Bänder | waagrechte Schichtstufen 2–6 m, versetzt, Grat mit Plateau, Turmklotz | 0 Stufen (0,0–0,1 % Stufenzellen); Wand = glatte 1-m-Fläche mit Texturband 0,5–1 m und senkrechten Tönungsstreifen 20–40 m; Kuppen rund, Grat-Zellen 0,2–1,2 % | 0 Stufen, 0 Plateau, 0 Turm; Bänder nur als Textur | groß |
| Bachbett im Blockwerk | Bett von Blöcken 1–3 m verstopft, Wasser dunkel, Gischt, Ufer = Blöcke | p2 788 m: Steine 0,2–0,8 m (3,7 je m), Blöcke ≥ 1 m 0,4 je m und aus der Hindernisliste gefiltert; 26 Becken/189 m alle 3–4 m gleich; Ufer 0,16 m über Spiegel | Blöcke ≥ 1 m im Wasser 0, Becken gleichförmig (eine Brush-Form), Ufer bündig; Bettplan 16h-N6 wartet | groß |
| Baumgruppen statt Waldfläche | Nadelbäume 8–15 m in Gruppen 3–8, Lücken, Gras nur Flecken | C2-Schlucht: geschlossener Bestand, Abstand 4–6 m, Höhe ~20 m einheitlich; Waldstreifen mit scharfer Obergrenze; B4 Grat-Reihe | Fläche statt Gruppen; Grat-Reihe; Höhe einheitlich | mittel |
| Vordergrund-Platten | flache Platten/Klötze 3–10 m, Büschel/Flechten in Fugen, Moos-Säume, halb eingegraben | A5: 167 Klippenplan-Platten (rcygn) liegen auf dem Gras auf; Talboden p2 = Heideteppich ohne Platten; Felsgruppen-Rolle „platte“ A5 0 / B4 1 | Platten nur an einem Wandfuß (A5), aufliegend statt eingegraben; Fugenbewuchs 0 | mittel |
| Gleichförmige Tönung der Wände | Farbbänder waagrecht entlang der Schichten; Witcher rot/ocker/grau | eine Beige-Fläche; Houdini-Tönung als senkrechte Streifen entlang der Falllinie (D2); Textur wiederholt sich alle 0,5–1 m (A5) | Bänder senkrecht statt waagrecht, 1 Farbton je Wand, Kachelung sichtbar | mittel |
| 1-m-Raster-Facetten | keine Rasterkanten; Uferkanten und Blockränder aus Netzen | Landschaft 1 m/Vertex (9 577 × 7 057); Uferkanten in GEF_D2_p2_quelle als 1-m-Treppen; Uferlippen 0,16 m | 1-m-Treppen an Uferkanten; Netz-Lippen auf 0 % der Uferlänge (Escarpment-Module ungenutzt) | mittel |
| Blickführung / Blickziel | Tal → Bach → Wand mit Turm als Ziel; Fern Dunst, Meer, weitere Berge | GEF_C2_p2_uebersicht ohne Blickziel (Kuppenlinie), Wald als Band; BERG11: Berg allein vor Himmel/Meer, Dunst gering | 0 Türme, Fernebene 0–1 Silhouetten, Dunst an Wänden gering | klein |

## 3. Inventar, heutige Dichten, Grenzen, Steilflächen, Pilotfeld-Kandidaten

### 3.1 Zuordnung Element → Netze / Werkzeug / Dichte heute / Lücke

Quelle: Inventar 13d (1 965 Netze, 2 960 Foliage-Typen, `export/unreal/welt/inventar/`), Planer-Protokolle, Rural Australia `swr/ra_inventar.json`.

**Felsnetz-Anteil (Wand + Steilhang)** – fehlt
- Netze: Schalen-Satz misch (Nordic): SM_MassiveNordicCoastalCliff_01 21,0 × 15,0 × 14,7 m (28 k Dreiecke, Nanite); SM_HugeNordicCoastalCliff_01/02
  13,8 × 8,5 × 9,1 / 12,2 × 6,2 × 7,1 m (Nanite); Wandmodule Mountain_Environment_Set SM_big_rock_wall_01/02/03 7,8 × 3,9 × 3,4 / 5,2 × 1,5 × 2,5 /
  4,3 × 1,3 × 2,3 m (4 889 / 3 385 / 3 000 Dreiecke, 3 LODs, **Nanite = 1** laut netze.csv 11.10.; 5–9× vergrößert → Quellnetz grob);
  SM_mountain_rock_big_02_7/_8 5,8 × 2,9 × 3,2 / 5,0 × 3,3 × 3,2 m; Füller
  bergwald SM_MossyForestBoulder_04/03/01 3,3/2,0/1,7 m, SM_NordicBoulder_01 6,8 × 8,9 × 4,1 m, SM_TundraMossyBoulder_01 7,4 × 3,7 × 1,8 m,
  SM_ForestRockShelf_01 5,4 × 2,4 × 1,0 m (nur Sims); Fab-Klippen (Klippenplan, nur Küste) liegen nur als `_tier_2` vor: vfmjadufa
  21,5 × 10,2 × 13,8 m (4 796 Dreiecke), vdssailfa 21,0 × 15,0 × 14,8 m (7 191), veqnci0db Turm 22,9 × 37,7 × 33,8 m (4 940) – alle Nanite,
  3 LODs, für Nahsicht grob.
- Werkzeug: `scripts/felsschalen/fs_plan.py` v8 misch (Kandidaten = Wandzellen ≥ Biom-Schwelle 40–55°, Wandhöhe ≥ 6 m, Wandebene ≥ 35°; Klassen
  groß 16–40 m / mittel 9–16 / klein 4,5–9 m, Füllung 0,9 × Wandhöhe, Überdeckung k 0,6, Wiederholung 20 m; Wandmodule ab 60 m Wandhöhe); Setzen
  `felsschalen/feld_setzen.py` + `fs_foliage_setzen.py` (groß = Akteur, mittel/klein/Füller/Fuß = Foliage FT_EL_FS_*).
- Dichte heute: Wanddeckung (nur ≥ 50°) D2 69 % (1 510 Stücke: 1 150 Akteure + 360 Foliage), C2 68 % (1 931), B4 64 % (3 213), B5 66 % (2 630),
  A4 61 % (1 036), B3 56 % (509), A5 44 % (432). Auf die Feldfläche (Wandzellen × Deckung): D2 12 %, C2 16 %, B4 24 %, A5 1,1 %. Hänge
  38–50° (B4 27 ha, B5 28 ha [33,5 ha ohne Meer-Sonderbehandlung, §3.3], D2 22 ha, C2 17 ha) bekommen 0 Netze: Schalter `luecke_roh = False`
  (Probe E4: +1 327 Füller, Deckung 61 → 83 %; Ferat: „keine Brockenflut“).
- Hinweis/Frage: Referenz ≥ 80 %; wir ≤ 24 % der Feldfläche, sichtbar 3–25 % (Schätzung). Es fehlt ein Planer für 25–50°-Hänge (fs_plan rechnet
  nur Wandzellen). Ist `luecke_roh` + WELT_FUELLER (1–3-m-Brocken) ein brauchbarer Hebel, oder braucht die Halde einen eigenen Planer mit
  Größenklassen? Wo liegt Ferats Grenze „Brockenflut“ – Anzahl, Größe oder Gleichförmigkeit (Anhang A, Rechnung)? Prüfmaß „Pixelanteil
  Netz/Landschaft je Bild“ gibt es noch nicht (SceneCapture mit `hide_actor_components` vorhanden).

**Halde / Blockhang unter den Wänden (Blöcke 1–8 m, Schutt 0,2–0,8 m)** – fehlt
- Netze 1–3 m (Nanite, Foliage-Typen da): SM_MossyForestBoulder_01–07 0,9–3,3 m (ft 6–10), SM_IcelandicBoulder_01/02/03 1,4/1,8/3,2 m,
  SM_MossyForestRock_01–03 0,7–1,7 m, Meadow SM_Rock_01–07 1,3–3,1 m, Mountain SM_ground_rock_01–03 1,4–3,8 m, Fab Granite_Rock pjEr1/pjtsT/pkeeM
  1,3–1,5 m, Forest_Boulder wgosajs 1,25 m, Icelandic_Rock skjsL 1,55 m, Mossy_Rock_Formation plFhY 3,3 m, Nordic_Forest_Cluster_Rock
  xf3odif/xfplcbf 2,7/1,9 m (Raw 8K; netze.csv zeigt nur das Fallback-Netz 19 998/20 000 Dreiecke – die Rohdaten-Werte „~1 M Dreiecke,
  364–381 MB“ sind eine Schätzung aus den Fab-Rohdaten-Paketen, nicht aus dem Inventar).
- Netze 2–8 m: SM_mountain_rock_big_02_1–8 2,7–6,4 m (Nanite), SM_NordicBoulder_01 6,8 × 8,9 × 4,1 m, SM_TundraMossyBoulder_01 7,4 × 3,7 × 1,8 m,
  SM_SandstoneBoulder_04/05 2,6/3,6 m, SM_RockSandstone_040 5,6 × 4,6 × 3,6 m, Mountain SM_Big_rock_01/02 8,2 × 9,4 × 6,3 / 9,4 × 10,2 × 4,3 m
  (KEIN Nanite; **Namensfalle:** Environment_Set SM_Big_Rock_01/02 4,7 × 4,1 × 3,6 / 4,6 × 3,9 × 4,0 m sind Nanite und werden von den
  Felsgruppen genutzt – anderes Netz), Rural Australia SM_Rock_S/M 1,5–3,3 m (LODs, kein Nanite), Basalt_Rock_A–D 0,8–2,3 m (kein Nanite, ft 0).
- Schutt 0,2–0,8 m: SM_mountain_rock_small_01_1–5 0,4–0,5 m, Forest SM_stones_01_1–6 0,4–1,2 m, Meadow SM_s_rock_01–03 0,4–0,6 m,
  SM_NordicBeachRock_01 0,26 m, SM_SmallStonesPack_01–14 0,1–0,2 m, RA SM_Scatter_01/02 0,2–2,7 m, Rocky_Snow_Pile 3–8,7 m (Schnee).
- Werkzeug: fs_plan Fußzone (fuss_abstand_m 5 vor der Wand, fuss_raster 3 m, fuss_anteil 0,5, fuss_k 3,0 = Brocken weit auseinander,
  fuss_flach_grad = Schwelle − 15°); Cloud-Ebene felsgruppen (`export/unreal/welt/felsgruppen`, Klassen grat/band/wand/fuss/blockstrom/kuppe/
  prallhang; nur 10 Felder A5 B4 C6 D3 E1 E4 G4 H3 H5 H6); wit_plan Bergsteine + fels_gross (30 % je Hangwald-Gruppe).
- Dichte heute: Fußbrocken je Feld (1 km², fs_plan 07.10.) D2 37, C2 8, A5 8, B4 75, B5 32 = 0,004–0,008 je 100 m². Felsgruppen-Ebene
  (`felsgruppen/<Feld>/plan.json`, 11.10. Runde 5) B4: **150 Akteure + 13 039 Instanzen** (je Rolle: hero 45, wand 145, band 234, block 862,
  platte 1, stein 2 262, kiesel 9 490 = 13 039; die Zonen-Statistik fuss 5 552 + band 4 912 + wand 2 992 + grat 1 824 + formgruppe 577 +
  blockstrom 132 + kuppe 37 + prallhang 28 = 16 054 zählt Instanzen in mehreren Zonen doppelt); nach Netz-Gruppe: kiesel 9 490, stein 2 170,
  block 545, block/stein 405, band 234, hero/wand 117, wand 47, hero 30, platte 1 → Blöcke ≈ 1 100 = **0,11 je 100 m²**. A5: 19 Akteure +
  3 245 Instanzen (block 210, stein 553, kiesel 2 390, band 73, hero 16). Der Felsgruppen-Plan hat ein Feld `entfernen` (FT_EL_FS_IcelandicBoulder_0*,
  MossyForestBoulder_0*, TundraMossyBoulder_01, SandstoneBoulder_0*, RockSandstone_040, namaqualand_boulder_0*, mountain_rock_big_02_*) →
  die fs_plan-Fußbrocken/Füller in A5/B4 (75 Fuß / 786 Foliage aus fertig_B4.json) sind dort möglicherweise ersetzt; „Dichte heute“ für A5/B4
  deshalb aus der Felsgruppen-Ebene nehmen (ungeprüft, ob gesetzt). Haldenhang 25–45° unter Wänden (§2.3): A5 4,6 %, C2 7,2 %, B4 11,6 %,
  D2 15,2 %, B5 15,7 % der Feldfläche – praktisch ohne Netz.
- Hinweis/Frage: Ein Halden-Planer fehlt (Zellen 25–50° unter Wänden, Prüfraster wie fs_deckung_c). Netze reichen für 1–8 m; nur 4–8 m sind dünn
  (NordicBoulder, TundraMossyBoulder, Mountain Big_rock ohne Nanite). Fragen an euch: Welche Dichte je Größenklasse liest als „Halde“, ohne
  Ferats „Brockenflut“ zu sein (Anhang A rechnet unsere Ableitung auf 110 000–165 000 Instanzen je Feld hoch – das Doppelte des heutigen
  Bestands)? Reicht Foliage/ISM (FT_EL_FS_*) für alles ≤ 4 m, Akteure nur für Hero-Blöcke? Müssen die Cluster-Rock-Raw-Sätze vorher auf 4K
  geklemmt werden?

**Klippen als 3D-Schichtbänder (Bandhöhe 2–6 m, Versatz, Grat/Plateau, Turmklotz)** – fehlt
- Netze geschichtet Nordic: Massive_Layered_Rock_Cliff ukjhcamga 30,0 × 9,3 × 10,9 m (Raw 8K, `_tier_0`; netze.csv 39 955 Dreiecke = Fallback,
  Nanite; „2 M Dreiecke, 400 MB“ = Schätzung aus dem Fab-Rohdaten-Paket, nicht im Inventar; nur_einzeln). Geschichtet rot
  (Wüste/Canyon): Desert_Western_Cliff_Layered Large_02/03 26 × 8,7 × 5,8 / 22 × 7 × 3,8 m, XL_01–16 9–54 m (9 Stück), Desert_Western_Formation_
  Layered_XL 7,6–68,6 m (5), Desert_Western_Spire 8–28 m (5), Massive_Sandstone_Cliff vmnmbhv 40 × 29 × 23 m (netze.csv 59 999 Dreiecke =
  Fallback; „3 M“ Schätzung), SM_MassiveSandstoneCliff_01/02/03/05
  20–42 m, SM_HugeSandstoneCliff_02/05/07 17–31 m, Red_Sandstone_Cliff 10,5 × 6,2 × 2,3 m.
- Bandmodule in Reihen (einzige echten Reihen-Kits): Coast_Dunes SM_beach_cliff_01_A/B/C + endings 6–14 m breit × 2,9 m hoch, SM_beach_cliff_02_A/B/C
  + endings 15–23 m × 6,6 m hoch (Spline-Klippen, Nanite nur bei 6 von 17).
- Türme: veqnci0db 22,9 × 37,7 × 33,8 m (`_tier_2`, 4 940 Dreiecke), AsianTemple SM_Cliff_01a–e 27–45 × 29–75 m (Karst, grau), Desert_Western_Spire_Layered_XL 10–28 m,
  Basalt_Basalt_Cliff_SM 8,6 × 5,3 × 6,0 m (193 k Dreiecke, kein Nanite) + Pillars_Wall 1,6 × 0,8 × 2,6 m. Rural Australia (kein Nanite, 5 LODs):
  SM_Cliff_L_01_A/B 20,6 × 49,8 × 47 / 22,8 × 41 × 35 m, Cliff_M_01–03 8 × 30 × 8–11 m, Ridge_Rock_01/02 8,6 × 14,5 × 1,5 / 7,8 × 18,6 × 1,8 m.
- Werkzeug: `scripts/klippen/klippen_plan.py` 2.1 (NUR Küstenwände: Neigung > 40°, Meer < 60 m; Verkleidung 2 Reihen, Hero 1,6–2,4×, Überlappung
  35 %, Reihe 2 bei 62 % der Sichthöhe, Schichtung strata_yaw je Front, Kipp 4–10°, Oberkante ≤ krone_max über Wandkante; Deckung je 120-m-Abschnitt
  gemessen); fs_plan misch für Binnenwände (keine Reihen, Zufallsnetze, Wiederholung 20 m); Material V17/V18 Schichtbänder nur als Textur
  (Band 0,9 / Wand 1,4 / Makro2 0,5).
- Dichte heute: A5 Klippenplan 357 Stücke (110 Hero, 70 Reihe 2, 167 Platten rcygn, 10 Geröll) auf 2 366 m Wandfuß, Front 1 Deckung 65 % / bis 30 m
  73 %; B5: 64 Stücke auf 807 m, Deckung 52 %. Binnenwände (B4 41,6 ha, B5 33,9 ha, C2 24,9 ha, D2 19,1 ha): 0 Klippenplan, nur Schalen 64–69 %.
  Stufenzellen 0,0 %, Grat-Zellen 0,2–1,2 %, Plateaus 0.
- Hinweis/Frage: Band-/Reihenlogik existiert nur im Küsten-Klippenplan; für Binnenwände fehlt sie (`klippen_regeln.md` Abschnitt 4 „Geschichtet:
  Reihen auf festen Höhen Δz = 0,75 × Modulhöhe“ ist beschrieben, nicht gebaut). Nordic-Bandmodule 2–6 m gibt es nicht (nur Coast_Dunes-Spline-
  Klippen 2,9/6,6 m und rote Desert-Layered-Kits = Farbe falsch für bergwald). Fragen: Reihenlogik aus klippen_plan 2.1 auf Binnenwände übertragen,
  oder Bandmodule kaufen (e)? Grat/Plateau als Gelände (Terrassen-Werkzeug R1–R4 kann Stufen ≥ 1 m schreiben) plus Gratkanten-Netze, oder nur
  Netze? Turmklotz je Massiv: welches Netz, wie gesetzt (veqnci0db/AsianTemple vorhanden, Setzer fehlt)?

**Nackte Erd-/Texturflächen (Fels-Lage auf 38–50° als reine Textur)** – fehlt
- Material: M_V18/M_V18s (MI_V12/V12s): Felstextur T_Flat_rock_01_tiled (V16), Schichtfels T_beach_cliff_01, Kachelung Fels 550 cm, Fern_Faktor 4,
  ToenungStaerke 0,5, Makro 0,8, Entsaettigung_Nass 0,5. Füller-Netze (siehe Halde) + Platten (siehe Vordergrund); Felsgruppen-Klassen band/wand/grat.
- Werkzeug: Fels-Lage aus Houdini (`lage_Fels.r8`) + Lagen-Schreiber `write_layers_rect_ex` (Sehens-Kette s38); Netze darauf nur über fs_plan
  (Wandzellen) bzw. felsgruppen (10 Felder). Prüfung „Fels-Lage-Pixel ≥ 38° ohne Netz“ gibt es nicht (fs_deckung_c misst nur ≥ 50°).
- Dichte heute: Fels-Lage auf steilen Pixeln (≥ 38°): B4 70 %, H3 58 %, C2 59 %, B5 61 %, E1 51 %, D2 45 %, A5 46 %; Band 38–50° ohne Netz: B4 27 ha,
  B5 28 ha, D2 22 ha, C2 17 ha, H3 21 ha (100 % Textur). Bild: D2 Bergrinne 50–65 % Textur, A5 Grashang 95 %, C2 Übersicht rechter Hang ~100 %.
- Hinweis: gleiche Lücke wie Halde/Felsnetz-Anteil, aber aus Daten messbar: „Fels-Lage ≥ 38° ohne Netz ≤ 10 %“ braucht nur `lage_Fels.r8` +
  `hoehe.f32` + `gesetzt_<Feld>.json` (alle vorhanden). Texturseitig hilft kein weiterer Materialumbau (SRV-Grenze 64, 447 Anweisungen);
  Nanite-Displacement ist aus (VSM-Schutz).

**Vordergrund-Platten 3–10 m mit Fugenbewuchs** – fehlt
- Netze: SM_flat_rock_01 9,9 × 7,0 × 1,5 m (kein Nanite), SM_flat_rock_02/03/04 2–5 m, SM_ForestRockSlab_01 7,2 × 3,5 × 0,7 m, SM_ForestRockShelf_01–03
  5,4–7,1 m, SM_SmoothRockShelf_01 3,1 × 2,7 × 0,4 m, SM_ForestRockFormation_01–06 3,3–5,8 m, SM_ErodedRockyGround_01–03 7,3 × 3,7 × 0,3 m,
  SM_TundraRockyGround_01 6,0 × 4,7 × 0,8 m, SM_NordicBeachRockyGround_01/02 3,4 m, SM_MassiveTundraRockFormation_01/02 77 × 29 × 12 / 29 × 20 × 7 m,
  Sharp_Cliff rcygn 18,8 × 4,6 × 10,9 m, RA Ridge_Rock_01/02 14,5/18,6 m (kein Nanite), Basalt_Cliff_Rock_B 7,5 × 5,4 × 1,5 m. Fugen/Auflage: GT_*
  Landschaftsgras (19 Arten), Heide-/Grasbüschel-Foliage (welt_bewuchs), Nordic_Moss_se4rwei 8K-Surface (424 MB), MI_EL_Auf_* (Moos/Schnee nur
  tundra/frost), Hivemind SM_MossClump (Quarantäne), Coast SM_stonecrop_01/02 0,4–0,7 m.
- Werkzeug: Felsgruppen-Rolle „platte“ (A5 0, B4 1, D3 379) und Klippenplan-Rolle „platte“ (A5 167 rcygn am Wandfuß); fs_plan Sims-Füller
  ForestRockShelf nur auf Absätzen ≤ 40°; Fugenbewuchs: kein Planer (Uferplan 16h-N3 setzt Gras-Fuß an Steinen nur am Bach).
- Dichte heute: A5 Hang: 167 Klippenplan-Platten (rcygn) am Wandfuß, ~30 sichtbar, 2–5 m, ≈ 0,03 je 100 m², aufliegend; Felsgruppen-Rolle
  „platte“ A5 0 / B4 1 / D3 379; Fugenbewuchs 0; Moos-Säume 0. (Der fertig_D2-Wert `platte_duenn_ueber_4m2` 658 ist ein Planer-Prüfwert für
  flache Schalen-Oberseiten, keine Platten – siehe §2.3.)
- Hinweis/Frage: Netze reichen (3–10 m Platten in 3 Paketen + Fab). Es fehlen Plattenfeld-Planer (Flat-Area-Detector wie Electric-Dreams-PCG;
  Eingraben-Tiefe? eure frühere Recherche nannte 40–50 % der Höhe; Fugenlinien → Grasbüschel/Moos?) und Flechten-Material (MI_EL_Auf_* nur
  tundra/frost kalibriert; M_EL_Klippe_RVT mit WorldAlignedBlend-Moos liegt, Custom Primitive Data 1 = Moosmenge).

**Bach von Blöcken verstopft (Blöcke 1–3 m im Wasser, dunkles Wasser, Gischt)** – fehlt
- Netze: Bachdekor-Klassen (Planer `--spline`): Lippenfels 137, Bettfels 19, Randfels 167 (≈ 1–2 m), Bachsteine ≈ 2 900, Kiesel 8 509,
  SM_SmallStonesPack 4 232 (≤ 0,5 m). Blöcke 1–3 m: SM_MossyForestBoulder_03/04 2,0/3,3 m, SM_IcelandicBoulder_02/03 1,8/3,2 m, SM_NordicBeachRocks_01
  5,8 × 3,6 × 2,5 m, Fab Nordic_Forest_Cluster 1,9–2,7 m; alte C2_Flussfels_* (9 entfernt, 3 gesenkt, Sicherung C2_Flussfels_B6_2026-10-13).
  Gischt/Schaum: 116 Niagara-Systeme (NiagaraExamples), Gischt an WF_K1/WF_K8, NatureWaterFX (gekauft 11.10., nicht eingebaut), ELD_Strom_Schaum
  (0 gesetzt), Wasser-Material F (MI_EL_SWR_Klar, Absorption 222/1000/1250).
- Werkzeug: `scripts/bachdekor` (21 448 Teile/788 m = 27 je m, 6 155 unter Wasser), `scripts/swr/hindernisse_filter_p2.py` (Teil ≤ 40 % Bettbreite
  = ≤ 0,8 m bei 2-m-Bett, je Meter ≤ 50 %: 1 718 → 1 362, Akteur WH_F_ERLENBACH_1V_C2_K00), SWR EldarienTransfer 0.20 (swr_rebuild/bake, Bett 99,9 %
  nass), Water-Brush Blend Min (Becken 3–4 m, eine Form), Uferplan kantenufer_p2 (1 592 Teile, 35 Ufersteine), muendung_p2.
- Dichte heute: Blöcke ≥ 1 m im Bach ≈ 0; Steine 0,2–0,8 m 3,7 je m; Lippen-/Bettfels 0,4 je m; Becken 26 auf 189 m alle 3–4 m gleich; Ufer 0,16 m
  über Spiegel (2-m-Band 94 % nass).
- Hinweis: harte Grenze = SWR-Front: zwei ~1-m-Lippenfelsen nebeneinander dämmen das 2-m-Bett. Blöcke gehen nur mit breiterem Bett (≥ 4 m, dann
  Block ≤ 40 % = 1,6 m) oder als Filter-Ausnahme mit geprüftem Umfluss (Wasser-Info 0,29 m/Pixel bei Zone 4096). Beckenform: Cloud 16h-N6 (neuer
  Bettplan A15-Format, Becken 0,8–1,2 m, Uferstufe 0,2–0,5 m) wartet; Werkzeug a15_einbau + brush_p2_kombinieren vorhanden. Gischt je Block: kein Setzer.

**Nadelbaum-Gruppen in der Felszone (3–8 Bäume 8–15 m, Lücken, keine Grat-Reihen, Höhenmischung, Nadel statt Laub)** – fehlt
- Netze 8–15 m (nur 7, keins Nanite): Mountain SM_Forest_pine_tree_00_C/D 9,0/12,3 m, SM_Forest_pine_10_special 14,6 m (8 447 Dreiecke),
  Environment_Set Fir_03_Medium 12,7 m, Coast SM_pine_beach_01_A/B 8,4/9,1 m, SM_pine_beach_02_A 10,3 m (Küstenkiefern, krumm). Hauptbäume
  heute: SM_Forest_pine_01–09 16,4–28,6 m (2 400–11 300 Dreiecke), Fir_04–07 18,4–21,9 m, Fir_08_Dead 18 m, SM_Forest_pine_10_dead 24,9 m.
  Jung/Latschen: SM_Forest_pine_plant_01–05 1,7–4,1 m, pine_tree_00_A/B 4,8/6,5 m, Fir_01/02 5,5/6,8 m, SM_dwarf_pine_big/medium/small
  1,0–3,1 m (23 Typen). **Megaplant_Library ist schon im Projekt** (122 Netze, alle Nanite), enthält aber nur Blätter/Zweige/Äste (Norway Maple,
  Goat Willow, Common Hazel, Yoshino Cherry u. a., größtes Teil 4,4 m) – **keinen Baum ≥ 8 m**. Nicht geladen (Fab kostenlos, UE 5.7+, Nanite
  Foliage experimentell): Megaplants Norway Spruce, Baltic Pine (+ Saplings), Dead Pine – Fab-IDs f87364c9 / a2b04e81 / ae732b47 / bc9e4e89
  lokal nicht prüfbar, unverifiziert.
- Werkzeug: `scripts/witcher_bewuchs/wit_plan.py` Hangwald (Zelle 34 m, Hang 18–44°, Baumabstand ≥ 9 m, Schnee ≤ 0,2, fels_lage ≤ 0,6; 3–7 Bäume
  im Radius 6–12 m, Mindestabstand 5 m, Wahrscheinlichkeit bergwald 0,5 / fjord 0,35 / gletscher 0,2 / tundra+kueste 0,15 × Rauschen) und Haine
  (Zelle 46 m, 3–11 Bäume, Radius 7–15 m, 6 % Totbaum); Artwahl nach Gewicht (bergwald Kiefer 0,55 / Tanne 0,25 / Birke 0,2; tundra Birke 0,65),
  keine Höhenklassen-Regel; Altbestand (Houdini-Waldzellen) wird nur angereichert, nie gelichtet.
- Dichte heute: Hangwald-Gruppen je km² D2 45, B5 51, C2 20, A5 14, B4 2; Haine D2 6, B5 12, B4 0; Altbestand D2 368, B5 333, B4 769 Waldzellen
  ungelichtet (C2-Flanke: Abstand 4–7 m, Höhe ~20 m, Streuung ≤ 20 %). Grat B4: ~25 Kiefern in Reihe je ~5 m.
- Hinweis/Frage: Der Planer kann Gruppen, aber (1) er darf keinen Altbestand entfernen (`remove_foliage_by_mask` im Plugin vorhanden → Ausdünn-Maske
  fehlt: nach welcher Regel ausdünnen?), (2) Hauptbäume sind 16–29 m statt 8–15 m → Maßstab gegen 1–3-m-Felsen 2× zu groß, 8–15-m-Nadelnetze
  fehlen fast (Megaplants-Nadelbäume nicht geladen, braucht Ferat + Experimental-Risiko) – kleinere Bäume kaufen oder größere Blöcke setzen?,
  (3) Grat-Regel und Höhenklassen-Mischung fehlen als Regeln. Birken am Felshang: Artgewicht tundra Birke 0,65 / bergwald 0,2 – braucht es eine
  Standortregel Birke–Wasser, und mit welchem Abstand?

**Standort der Bäume zwischen Blöcken statt auf Grasfläche** – fehlt
- Netze: Blöcke 1–8 m wie Halde; wit_plan Palette fels_gross (0,3 je Hangwald-Gruppe) und bergstein (SM_mountain_rock_small_01_1–5, SM_MossyForestRock_01).
- Werkzeug: wit_plan: Gruppenmitte nur bei fels_lage ≤ 0,6, Baum nur bei fels_lage ≤ 0,7 und Hang ≤ 46° → Bäume meiden Fels systematisch;
  Felsgruppen-Ebene kennt keine Bäume; kein gemeinsamer Planer Baum + Block.
- Dichte heute: Großfelsen aus wit_plan je km² D2 12, C2 6, A5 6 = 0,3 je Gruppe; Bergsteine D2 116. Block:Baum ≈ 0,3:5.
- Hinweis/Frage: Die fels_lage-Grenze (0,6) und die Zahl Blöcke je Baum sind reine Planer-Parameter (Netze da) – welche Werte schlagt ihr vor, und
  gehört die Block-Setzung zum Baum-Planer oder zum (fehlenden) Halden-Planer? Ohne Halden-Planer bleibt der Boden dazwischen Textur.

**Gras als Flecken zwischen Steinen statt Teppich** – fehlt
- Netze/Daten: GPU-Gras GT_* 19 Arten über Houdini-Dichtekarten (`welt/*.r8`) + Landschaftsmaterial V18 (Bachgewicht-Textur T_Eldarien_Bachgewicht_2m
  als Muster für Masken); Heide/Grasbüschel-Foliage aus welt_bewuchs (D2 2 813, C2 1 237 Heide gleichmäßig), Blumeninseln (FT_EL_WIT_*); Lagen-Schreiber
  `write_layers_rect_ex` + Sehens-Kette s38 (bettlagen_p2, altbett_p2b, kantenufer_p2_lagen als Vorlagen).
- Werkzeug: Gras-Dichte aus Houdini-Karten und Fels-Lage im Material (kein Gras auf Fels-Lage); welt_bewuchs/wit_plan streuen Heide/Büschel
  gleichmäßig; keine Maske „unter Blöcken/Schutt Gras aus“.
- Dichte heute: Talkopf/Talkaskade p2 Heide/Gras 95–100 % beidseits; A5 Grashang ~90 % Textur+Gras; Heideinseln 0.
- Hinweis/Frage: Schreibwerkzeuge vorhanden (Lagen + rebuild_grass_maps + grass.FlushCache, 3–5 min bis Gras steht); es fehlt die Regel/Maske,
  die zum (noch fehlenden) Halden-Plan gehört – z. B. Fels-/Geröll-Lage unter Blöcken, Gras nur in Fugen: welcher Radius um Block/Schutt, welche
  Lagen? Falle: Gras-Karten nie während Shader-Übersetzung bauen; `grass_maps_check` „falsch 0 max 0“.

**Moos/Flechten auf Fels, Moos-Säume, Bachsteine ohne Moos** – fehlt
- Material: MI_EL_Auf_<Netz>_<biom> (Moos/Schnee-Auflage, `ue_fels_auflage`; nur tundra/frost), M_EL_Fels_MS-Instanzen (übrige Biome),
  M_EL_Klippe_RVT (RVT-Höhenblend + WorldAlignedBlend-Moos, Moosmenge per Custom Primitive Data 1; kompilierte 10.10. 4 h nicht – Log prüfen),
  MI_EL_Berg_* (Wandmodule, Base Brightness × 0,55–0,7). Moos-Netze: SM_MossyForestBoulder_01–07, SM_MossyRocks_01/02 1,9–3,4 m, SM_MossyRockFace_02
  2,4 m, Japanese_Mossy_Boulder 1,2 m, Mossy_Rock_Formation 3,3 m, SM_TundraMossyBoulder_01; Surface Nordic_Moss_se4rwei 8K; Decal
  TileableMossPatches (Megascans). Nasslinie an Steinen: `scripts/unreal/ue_fels_nasslinie.py` (Agent-Auftrag aus Antwort 18, Kopie M_EL_Fels_MS2 +
  Spiegel-Textur).
- Werkzeug: Auflage je Biom beim Setzen (`feld_setzen.py`: tundra/frost → MI_EL_Auf_*, sonst M_EL_Fels_MS); kein Saum-/Flechten-Planer, kein Moos auf
  Bachsteinen (Bachdekor nutzt helle SmallStonesPack).
- Dichte heute: Bachsteine mit Moos 0 von ~25 sichtbaren; Felsnetze D2/A5 ohne Fugenbewuchs; 4 232 helle SmallStonesPack im p2, 6 155 Teile ganz unter Wasser.
- Hinweis/Frage: materialseitig fast fertig (M_EL_Klippe_RVT: Up-Maske aus VertexNormalWS + Welthöhen-Band, RVT-Bodenblend 20–60 cm für Blöcke);
  offen: Auflage für bergwald/fjord/kueste kalibrieren (euer VORSCHLAG.md Stufe 3 nannte Helligkeit × 1,2–1,3 – gilt das noch?), Flechten-Variante,
  Moos-Saum als RVT-Decal am Fuß (eure Recherche: RVT-Decal, nicht DBuffer), Nasslinie an Bachsteinen (Skript in Arbeit).

**Totholz (liegende Stämme unter Gruppen, stehend 1 je 15–25 Bäume, Stamm quer im Bach)** – vorhanden, nur Dichte
- Netze liegend: SM_FallenSpruceTree_01 7,3 m (Nanite), Forest SM_dead_log_03, SM_beech_old_roots_01, Coast SM_beach_driftwood_01–09, RA SM_Log_L/M/S
  17,7/8,6/5,5 m + SM_Roots_01 3,2 m (kein Nanite), Electric-Dreams-Totholz (Hainbuche), Mountain SM_stones_roots_01–05 3–7,5 m. Stehend:
  SM_Forest_pine_10_dead 24,9 m, Fir_08_Dead 18 m, Graveyard SM_Dead_Tree_01–03, MedievalFantasyVillage SM_EuropeanBeech_Dead_M/XL, Fab Dead_Tree_qlEtl
  6,2 m, Megaplants tote Zweige (SKM_Twig_*_Dead).
- Werkzeug: wit_plan (Haine 6 % Totbaum, Bestand 3,5 % stehend, Unterwuchs: liegend Poisson 1,6 je Gruppe, Stümpfe), Mittelschicht-Ebene (A5
  totholz_liegend 434 / Stumpf 257, B4 24/31), Totholz an die Normale gelegt (11.10.); Bachdekor hat keine Totholz-Klasse.
- Dichte heute: D2 (1 km²) 8 stehend, 19 liegend, 55 Stümpfe = 0,2 liegende je ha; B4 Mittelschicht 24 liegend; Talkopf 1 stehender Totstamm, C2-Flanke 0.
- Hinweis/Frage: Werkzeug und Netze da; offen ist nur die Dichte (Planer heute Poisson 1,6 liegende je Gruppe – welcher Wert für die Referenz?)
  und ob eine Klasse „Stamm quer“ im Bachdekor-Planer sinnvoll ist (Lippenfels-Logik, Filter gegen SWR-Front wie Hindernisse).

**Zonierung Wand → Halde → Tal und Maßstabskette (Geländeform: Stufen, Schüttkegel 30–38°, Grat/Plateau)** – fehlt
- Werkzeuge Höhen: EldarienTransfer `write_heights_from_file` (2 Phasen, ≤ 1,2 cm Abweichung), Houdini-Terrassen R1–R4 (A4 A5 B4 B5 B6 D3 H2 H5 I5),
  Serpentinen-Kette (28 Felder), Water-Brush Blend Min (Bett), `scripts/gelaende/brush_p2_kombinieren.py`, `scripts/gefaelle/a15_einbau.py`,
  sehens_gelaende-Kette, Rückbau `einbau_rueckbau.py`. Houdini-Felshaut SM_K*/SM_R_*__FELS (je 1 km, 3–27 k Dreiecke; H1 gesichert, ausgeblendet)
  – nicht wiederverwendbar für Stufen.
- Werkzeug-Lage: Gelände wird nur für Bäche/Straßen/Sehens-Orte umgebaut; kein Planer für Halden-Schüttkegel oder Wandstufen. Landschaft 1 m/Vertex,
  Nanite-Boden ohne Displacement (Tessellation aus), Rasterfacetten < 10 m Abstand sichtbar.
- Dichte heute: Stufenzellen D2/C2/B4/B5 0,0 %, A5 0,0 % (Definition §2.3); Haldenhang 25–45° unter Wänden D2 15,2 %, C2 7,2 %, B4 11,6 %,
  B5 15,7 %, A5 4,6 % der Feldfläche (vorhanden, ohne Netz); Grat-Zellen 0,2–1,2 %; Relief D2 26–446 m, B4 34–684 m als durchgehende glatte
  Rampe. Maßstab heute Kiefer 18–22 m : Fels 1–3 m : Relief 300–650 m ≈ 20 : 1,5 : 400 (Referenz 10 : 3 : 120).
- Hinweis/Frage: Da die Haldenhänge schon da sind, ist die Halde zuerst eine Netz-Aufgabe; ein Höhenplan (A15-Format, über brush_uebernahme/
  sehens_gelaende schreibbar, je Feld komplett hoehen → 40 s → lagen → rest, danach Gras-Karten + Nanite je Teil + `shift_foliage_by_height_delta`)
  wäre nur für Stufen/Plateau/Turm nötig. Stufen 2–6 m sind im 1-m-Raster möglich (Terrassen-Werkzeug), Simse < 1 m nur als Netz. Frage: Braucht die
  Referenz-Zonierung überhaupt Geländeumbau, oder reichen Netze (Blöcke auf dem Hang, Bandmodule an der Wand, Gratkanten-Netze)?

**Gleichförmige Tönung der Wände / Farbbänder waagrecht** – fehlt
- Material/Daten: V18 (M_V18/M_V18s): V17-Bänder Band 0,9 / Wand 1,4 / Makro2 0,5, Felstextur T_Flat_rock_01_tiled, Kachelung 550 cm; Houdini-Tönung
  Toenung_R/G/B (steil C2 0,77/0,75/0,63, B4 0,69/0,68/0,60, D3 1,76/1,36/0,88) als senkrechte Streifen 20–40 m. MI_EL_Berg_* (Wandmodule abgedunkelt
  × 0,55–0,7; VORSCHLAG Stufe 3: × 1,25–1,45), MI_EL_<Netz>_<biom>, `klippen_toenung.py`, Cloud-Ebene berge_toenung (vorschau_toenung_B4/C2/E1/G6/H3/I4.png).
  Fab-Farbband-Kits (rot/ocker): Desert_Western_Cliff_Layered (9), Formation_Layered (5), Red_Sandstone_Cliff; Nordic Coastal Cliff f53f0b71 (empfohlen,
  nicht geladen).
- Werkzeug: Tönung = Houdini-Lage × ToenungStaerke 0,5 (`gelaende/fels_farbe.py`); Schichtbänder = Textur-Streifen im Material; kein Welthöhen-Band
  (RVT World Height / AbsoluteWorldPosition.z) im Landschafts- oder Felsmaterial.
- Dichte heute: 1 Beige-Fläche je Wand; Texturwiederholung alle 0,5–1 m (A5); 0 Farbbänder waagrecht.
- Hinweis/Frage: Material nicht neu bauen (Speicher, SRV 64). Zwei Wege wären bei uns technisch möglich – Kopie V18 + wenige Knoten (Welthöhe →
  Bandwechsel) oder Tönungs-DATEN (Houdini-Toenung_R/G/B über das altbett_lagen-Muster neu schreiben, 0 Materialänderung). Welcher Weg trägt die
  Referenz besser, und wie breit/wie viele Farbtöne je Band? Netze: Schalen folgen nicht der Bandhöhe (Wiederholung 20 m, Zufallsnetz).

**1-m-Raster-Facetten an Uferkanten / Uferlippen aus Netzen** – fehlt
- Netze (ungenutzt): Coast_Dunes SM_beach_escarpment_01_A–C 8–8,6 m × 1,0–1,1 m hoch, SM_beach_escarpment_02_A–D 8–11 m × 1,8–1,9 m (Nanite nur
  01_A–C), RA SM_Ridge_Dirt_01/02 A/B 14,5–16 m × 2 m (kein Nanite), Megascans SM_DryRiverBed_02, SM_NordicBeachRockyGround_01/02 3,4 m,
  SM_ErodedRockyGround 7,3 m; Ufersteine aus kantenufer_p2 (35), Randfels 167.
- Werkzeug: `scripts/swr/ufer_plan_einbau_p2.py` (Lippe ± 0,75 m bei d ≤ 0,5 m, Überdeckung, Auflage 60 %, 1 592 von 1 730 Teilen) + `ufer_lagen_p2.py`;
  Landschafts-Brush (landscape_rt_res 4096) formt Ufer nur im 1-m-Raster; Uferlippe heute 0,16 m (Kies 0,04 m).
- Dichte heute: Uferkanten in GEF_D2_p2_quelle als 1-m-Treppen; Lippenhöhe 0,16 m, 2-m-Band 94 % nass; Netz-Lippen auf 0 % der Uferlänge.
- Hinweis/Frage: Escarpment-Module sind genau „Uferstufe 0,2–0,5 m“ (16h-N6), liegen im Projekt und werden nirgends gesetzt. Sollen sie als
  Spline-Bänder entlang beider Uferlinien gesetzt werden (wie SWR-Band, Breite +2 m), und mit welchem Abstand/Überlappung? Die Nanite-Fehlenden
  (02_A–D, Ridge_Dirt) wären vorher umzustellen.

**Blickführung / Blickziel und Fernebene (Turm, Dunst, weitere Berge)** – fehlt
- Netze: Türme/Klötze ≥ 20 m veqnci0db 33,6 m, AsianTemple SM_Cliff_01a/c/d/e 64–75 m, Desert_Western_Spire_Layered_XL_03 28 m,
  SM_IcelandicLavaSpire_01/02 (Lava), SM_MassiveTundraRockFormation_01 77 m lang. Fernebene: Mountain_Environment_Set Background_Terrains (im Paket),
  Lava_Volcano 5 Hintergrund-Berge; Licht W7 (Nebel 0,0035/0,02 max 0,7, Rayleigh 0,045, Mie 0,004, AP 2), Talnebel-Kugeln `witcher/talnebel.py`.
- Werkzeug: Kameras/Prüfbilder (`blick_bilder.sh`, `sehens_kameras.py`); kein Setzer „ein Turm je Massiv“; Hintergrund-Berge nicht platziert; Dunst nur global.
- Dichte heute: BERG11: Berg allein vor Himmel/Meer, 0 Türme, Fernebene 0–1 Silhouetten; Dunst an Wänden gering.
- Hinweis/Frage: fs_plan hat einen Modus „turm“ (aufrecht, Fuß tief, Krone nicht über der Wand → Regel „nicht über Wand“ müsste für Blickziele
  fallen); Background_Terrains liegen ungenutzt. Fragen: Wie viele Blickziele je Massiv/Feld, welche Höhe über dem Grat, und gehören Hintergrund-Berge
  an den Meerrand? Dunst-Formel bei uns: Nebeldichte an der Kamera = Dichte × 2^(−Abfall × Höhe/10).

### 3.2 Grenzen (Speicher, Grafik, Instanzen, Nanite, Fab, Landschaft, SWR, Betrieb, PCG, Prüfung)

- **RAM 50,6 GB:** Editor-Neustart ab 60 GB Zusage (hart 90 GB), Auslagerung 64–128 GB (Zusagegrenze 111 GB); nie die ganze Welt laden (World Partition
  1-km-Felder, 266 Landschaftsteile, schmutzige Akteure bleiben geladen); Editor-Python ohne numpy; Editor oder Kommandozeile, nie beides.
- **Grafikspeicher 23,7 GB (RX 7900 XTX):** GPU-Absturz **08.10. 12:27** bei VRAM 14,4/23,7 GB (TerminateOnGPUCrash in ShadowDepths →
  RenderVirtualShadowMaps(Nanite); CLAUDE_ARCHIV_2026-10-09 Z. 893); Schutz-CVars `r.Shadow.Virtual.Nanite.AllowTessellationDirectional/Local = 0`
  seit 10.10., Nanite-Boden ohne Displacement; 10.10. 23:38 DXGI_ERROR_DEVICE_HUNG im Leerlauf (ohne VRAM-Wert). Textur-Streaming-Pool
  `r.Streaming.PoolSize=8000` (DefaultEngine.ini, 8 GB); ein Nanite-Streaming-Pool ist nicht gesetzt (Engine-Standard, Wert ungeprüft);
  Meer-Wasserdaten 4096² (0,75 m/Punkt) kosten schon.
- **Instanzen heute** (`docs/pruefung/lage/BERICHT.md`, 07.10. 13:05): Welt 2 922 841 Instanzen (Foliage + ISM) + 12 925 Einzelobjekte
  (+ 150 Felsgruppen-Akteure B4 vom 11.10. = 13 075); je Feld max G4 142 640, D2 122 674, E4 121 953, B4 106 925 + 3 819 Akteure (dazu
  Felsgruppen B4 +13 039 Instanzen + 150 Akteure, Felsschalen B4 2 427 Akteure/786 Foliage), C2 65 255 + Bachdekor p2 21 448 + Ufer 1 592 +
  Hindernisse 1 362; welt_bewuchs max 93 001 neue je Feld (D2). Eure früheren Hinweise (`antworten/klippennetze-a5.md`): „Zell-Ladehitches bei
  200+ Actors beobachten“, Primitive ≈ 10× Speicher einer Instanz (672 vs 64 Byte); die Werte „2–3 s Ladehänger“ und „~2 ms CPU je 10 000
  Nanite-Einzelakteure“ sind unsere Schätzung ohne Fundstelle → Halden/Schutt nur als Foliage/ISM (FT_EL_FS_*), Hero-Stücke als Akteure.
- **Nanite-Lücken** (netze.csv, Inventar 13d vom 11.10.): 1 082 von 1 965 Netzen Nanite (der Stand 07.10. „289 von 707 benutzten Netzen, 22 %
  der Stücke“ ist überholt; der Stück-Anteil wurde seither nicht neu gezählt). Die Mountain-Wandmodule SM_big_rock_wall_01/02/03 SIND Nanite
  (3 536 Akteure + 3 314 Instanzen, 3 000–4 900 Dreiecke, 5–9× skaliert = grobes Quellnetz, aber kein Nanite-Problem). Echte Lücken: Basalt 0/22,
  Coast_Dunes 11/196 (Escarpments 02_A–D, Spline-Klippen), Rural Australia 0/85 (5 LODs), alle Nadelbäume (Mountain/Environment/Coast 0),
  SM_flat_rock_01 (4 038 Dreiecke), Mountain SM_Big_rock_01/02 (7 068 / 7 148), Big_Tree_Birch_01 (28 486 Dreiecke, 24 160 Stück = größte Last),
  Lava 29 Felsen. Umschalten gruppenweise (`nanite_netze_einschalten.py`, Klasse A 154 Netze), nie > 20 000 Objekte auf einmal.
- **Fab-Rohdaten:** Raw-8K-Sätze (Cluster Rocks xf3odif/xfplcbf/xjijbgx bei 1,2–2,7 m Größe, ukjhcamga, vmnmbhv): netze.csv führt nur die
  Fallback-Netze (19 998 / 20 000 / 19 998 / 39 955 / 59 999 Dreiecke, NaniteFallbackPercent 100); die Rohdaten-Werte „1 M / 2 M / 3 M Dreiecke,
  340–510 MB je Netz“ sind Schätzungen aus den Fab-Paketen, nicht aus dem Inventar → max_texture_size 4096 + Fallback 2–5 %
  (`ue_klippen_import_pass.py`, ungetestet); Nordic-Hero-Klippen nur als `_tier_2` (4 796–7 191 Dreiecke, für 2 m Nahsicht zu grob; High nur
  durch Ferat im Fab-Fenster). Fab-Master M_MS_Base nach Neustart prüfen (Eltern = None-Falle). Ferat lädt gerade Rural Australia → kein Editor,
  kein Neustart bis „fertig“.
- **Landschaft** 1 m/Vertex (9 577 × 7 057), Höhen nur je Feld komplett in 2 Phasen (hoehen → 40 s → lagen → rest), danach Gras-Karten
  (`grass_maps_check` „falsch 0 max 0“) + Nanite je Teil + Foliage mitverschieben; GPU-Hänger bei Vollumbau/Undo/Materialwechsel; Landschaftsmaterial
  SRV-Grenze 64 (V18 → V18s an 1 Teil), 447 Anweisungen, nie per Python neu bauen, nur Kopie + wenige Knoten (danach gras_v14_welt 1,3 h).
- **SWR (Shallow Water River):** Bett 2 m, Wasser-Info Zone C2 4096 = 0,29 m/Pixel, Band = Bett + 2 m, match_spline_height_amount 0,3 = Schwelle,
  remove_outside 50 löscht; zwei 1-m-Lippenfelsen dämmen die Front; Messen erst nach ≥ 4–5 min (36 fps); Bake WCBS 0,2–0,3 ms im Spiel;
  ungespeicherte Akteure fehlen in PIE; `eld.ohne_pinsel()` macht alle Wasserkörper schmutzig.
- **Planer-Laufzeiten/Betrieb:** fs_plan B4 94 s je 64-m-Teil (Feld ~1–2 h), E4 Felsschalen 701 s, Welt-Bewuchs 70 s Befund/Welt, Klippenplan Minuten;
  Setzen nur über WMI-Ketten (welt_felsen_bau.sh aus), nie ue.py parallel; Themen-Kürzel „bach*“ = BACH löscht das Bachdekor (Setzer-Falle);
  feld_setzen.py nie auf Klippenpläne (löscht Schalen).
- **PCG (H3 offen):** Python-Klassen PCGSurfaceSampler/StaticMeshSpawner/Projection/WorldRaycast vorhanden, PCGMeshSampler fehlt;
  Electric-Dreams-Graphen (PCGDemo_ForestCliffs, Flat Area Detector, hero rock assemblies) im Projekt; Nanite Foliage (r.Nanite.Foliage) + Megaplants
  experimentell – Epic rät vom Ausliefern ab.
- **Qualitätsprüfung:** Prüfbilder nur ohne Ferat im Editor (Kameras verrutschen), erstes Bild nach Neustart verwerfen, VSM-Cache leeren
  (`blick_bilder.sh`), ≥ 90 s nach Feldladen; BaseColor-Messung `swr/basecolor_messen.py`; Deckungsraster fs_deckung_c nur für Wandzellen ≥ 50°
  (für 25–50° neu zu schreiben).

### 3.3 Steilflächen der Welt (Daten)

Methode: `hoehe.f32` (1 m, ungeglätteter Gradient), Land = Höhe > 0,2 m, Biom = Houdini-Kachel-Rezept aus `eigner.r8`/`welt.json` (4 s Laufzeit).
Welt: 3 334 ha Land, > 30° 1 018 ha (30,5 %), > 45° 514 ha (15,4 %), > 50° 363 ha (10,9 %).

| Biom | Land ha | > 30° | > 45° | > 50° |
|---|---|---|---|---|
| fjord (steilstes) | 89 | 91,6 % (82 ha) | 62,3 % (56) | 48,0 % (43) |
| kueste | 73 | 76,3 % (56) | 39,7 % (29) | 24,3 % (18) |
| gletscher | 214 | 70,0 % (150) | 35,5 % (76) | 24,4 % (52) |
| bergwald (Referenz-Biom, größte Steilfläche absolut) | 436 | 59,4 % (259) | 31,1 % (135) | 21,8 % (95) |
| wueste | 143 | 39,0 % (56) | 21,9 % (31) | 17,3 % (25) |
| canyon | 101 | 14,7 % | 8,4 % | 6,6 % |
| elfenwald | 366 | 35,7 % (130) | 19,1 % (70) | 13,2 % (48) |
| dschungel | 327 | 21,6 % (70) | 12,2 % (40) | 10,3 % (34) |
| frost | 70 | 33,5 % | 10,6 % | 5,8 % |
| tundra | 169 | 24,2 % | 7,4 % | 4,5 % |
| lava | 100 | 17,7 % | 4,0 % | 2,1 % |
| oedland | 191 | 10,4 % | 6,4 % | 5,5 % |
| aue | 665 | 2,4 % | 0,7 % | 0,5 % |
| heide | 155 | 1,7 % | 0,3 % | 0,1 % |
| sumpf | 98 | 2,5 % | 0,3 % | 0,1 % |
| unbenannt (ohne Rezept) | 137 | 55,7 % | 19,4 % | 10,7 % |

Je Feld (`steilhang_je_feld.md`, steil ≥ 38° / Wand ≥ 50° in ha): B4 69,0/41,6; B5 61,6/33,9; H3 43,5/22,6; C2 41,5/24,9; D2 41,0/19,1; I4 34,7/14,8;
D1 33,0/15,8; E2 31,8/13,5; C1 28,2/12,6; B3 25,9/9,7; H4 25,1/10,7; C6 24,6/7,0; E4 22,5/13,3; A5 14,8/7,3. **Band 38–50° ohne jedes Netz:** B5 28 ha,
B4 27 ha, D2 22 ha, H3 21 ha, I4 20 ha, E2 18 ha, C6 18 ha, C2 17 ha, D1 17 ha, B3 16 ha. Fels-Lage auf steilen Pixeln (Textur statt Netz): B4 70 %,
B5 61 %, C2 59 %, H3 58 %, E1 51 %, D1 48 %, A4 48 %, I3 48 %, D2 45 %, A5 46 %, H4 45 %, C6 Lavafels 78 %, G6 76 %.

**Meerzellen (Küstenfelder A5/B5):** Wie `steilhang_je_feld` die Zellen an der Wasserlinie behandelt, ist im Bericht nicht dokumentiert (vermutlich
Gradient über die Wasserlinie hinweg, Land = Höhe > 0,2 m). Unsere Nachrechnung ohne diese Sonderbehandlung liefert A5 Wand ≥ 50° 5,6 ha (statt
7,3), B5 steil ≥ 38° 67,1 ha (statt 61,6) und Band 38–50° 33,5 ha (statt 28); fs_plan-Wandzellen (Wandhöhe ≥ 6 m) A5 2,5 ha. Binnenfelder D2/C2/B4
stimmen auf ±0,2 ha. Für Küstenfelder gilt daher eine Spanne (A5 Wand 2,5–7,3 ha, B5 Band 28–33,5 ha); Meerzellen wurden nirgends als Wand
gezählt. **Stufenzellen** (Definition: Zelle < 5° in einem 7 × 7-m-Umfeld mit > 20°): D2 0,03 %, C2 0,02 %, B4 0,05 %, B5 0,03 %, A5 0,01 %.

### 3.4 Pilotfeld-Kandidaten

- `Spielstart_E5` liegt bei X −205 / Y 495 m (Feldmitte E5, Aue, 1 % > 30°). Alle Nachbarfelder sind flach oder falsches Biom: D4 canyon 14 %,
  E4 wueste 34 %, F4 aue 2 %, D5 0 %, F5 1 %, D6 oedland/lava 19 %, E6 oedland 16 %, F6 4 % (> 30°). Die Nadelwald-/Skellige-Referenz beginnt erst
  2,6 km vom Start (B5).
- **Vorschlag 1 – B5** (Fenster um den Bach, 300 × 300 m): bergwald 79 % / kueste 21 %, 82 % > 30°, steil ≥ 38° 61,6 ha, Wand 33,9 ha (Platz 2 der
  Welt), Fels-Lage 39 %, Nadeln 16 %, Höhe 0–664 m; **größtes Band 38–50° ohne Netz der Welt (28–33,5 ha)** und bergwald = Referenz-Biom. Bach
  `B_R3_R_M2_P0_01` bei X −2731 / Y 90 (2,6 km vom Start): Spline 21 Punkte, 182 m waagrecht / 186 m 3D, 38,3 m Fall = 21 % (waagrecht);
  `baeche_alle.json` nennt `laenge_m` 194,3 (Houdini-Netzlänge) und `gefaelle` 0,197; Breite 3,2–6,2 m (Spline-Breiten; die frühere Angabe
  3,2–4,3 m war unvollständig). 200-m-Umkreis Relief 168 m, 31 % > 30°, 17 % > 38°, aber nur 0,3 ha Wand ≥ 50°. Schon da: Felsschalen 2 630
  (66 %, 2 005 Akteure + 625 Foliage), Klippenplan 2.1 Front 1 (807 m Kette, 64 Stücke, Deckung 52 %), Witcher 51 Hangwald + 12 Haine, Altbestand
  333 Waldzellen; Bestand 97 223 Instanzen + 1 454 Akteure (07.10.); Sehens-Pilot 1 (B5/C5) sauber zurückgebaut = Rückbau erprobt. Gegen: Wand
  und Bach ~300 m auseinander → die Kernforderung „Wand → Halde → Bach in EINEM Bild“ ist hier nicht erfüllbar (nur zwei Teilszenen oder
  Geländeumbau); B5 lädt mit Nachbar B4 (106 925 Instanzen + 3 819 Akteure + 13 039 Felsgruppen + 150) → Speicherrisiko beim Laden.
- **Vorschlag 2 – B4 K1-Fenster** (Hero-Szene mit Wasserfall): WF_K1 (59 m Fall, Kante X −3110 / Y −618, 3,1 km vom Start): 200-m-Umkreis Relief
  346 m, 80 % > 30°, 67 % > 38°, 33 % > 50° = 5,3 ha Wand – beste Wand+Wasser-Kombination; dazu 3 Bäche K1_WASSERFALL_WEST_01–03 (176–279 m, 36–48 m
  Gefälle, 4–7,7 m breit) + 2 Hauptfluss-Abschnitte; dichteste Wand der Welt (3 213 Schalen 64 %, Felsgruppen 150 Akteure + 13 039 Instanzen).
  Gegen: schwerstes Feld (106 925 Instanzen + 3 819 Akteure + Felsgruppen; Speicherrisiko beim Laden mit Nachbarn), Altbestand 769 Waldzellen +
  Grat-Baumreihe müssten gelichtet werden, Hauptfluss/Wasserfall nicht SWR (Ferat: Wasserfälle warten).
- **Vorschlag 3 – p2-Erlenbach C2/D2** (laufender Pilot, Quelle X −1680 / Y −2768, 3,6 km; Mündung C3 2,9 km): 200-m-Umkreis an der Quelle Relief
  355 m, 89 % > 30°, 70 % > 38°, 38 % > 50° = 6,1 ha Wand – beste Wand+Bach-Kombination der Welt; alle SWR-/Bett-/Ufer-/Lagen-Werkzeuge kalibriert
  (21 448 Bachdekor, 1 592 Uferteile, Bake 99,9 % nass). Gegen: Biom gletscher 46 % / fjord 23 % / tundra 21 % (Birke 65 % in tundra, Schnee 9 %)
  statt Nadelwald; 3 Felder (C2 D2 C3) zu laden; Bergrinne-Hang = helle Texturfläche (GEF_D2_p2_quelle ~55–65 % Textur).
- Nah, aber falsches Biom: **E4** (1,1 km, Wüste): Bach 686 m, 20 m Gefälle, 6,8–7,2 m breit, Umkreis 42 % > 30°, 19 % > 50° = 3,0 ha Wand,
  Felsschalen 2 921 (65 %, 649 Akteure + 2 272 Foliage), Sandstein-Kits mit Farbbändern (Desert_Western_Layered 9+5+5 Netze) – schnellster Test für
  „Schichtband-Klippen in Reihen“, nur nicht für die Nadelwald-Referenz. **D6** (1,6 km, Ödland 61 / Lava 26): 4 Bäche 79–261 m mit 9–30 m Gefälle,
  Wand 6,2 ha, Felsschalen nur 4 (freies Feld), 55 107 Instanzen, Palette Namaqualand/Totbäume.
- **Bewertung der Kandidaten (Zahlen aus oben; Rang = unsere Einschätzung, kein Beschluss):**

| Kriterium | B5-Fenster | B4 K1-Fenster | D2 p2-Quelle | E4 | D6 |
|---|---|---|---|---|---|
| Zonen im Bild (Wand ≥ 50° im 200-m-Umkreis / Wand–Bach-Abstand) | 0,3 ha / ~300 m → Wand+Halde+Bach NICHT in einem Bild; Nadelwald-Hang ja | 5,3 ha / Wasserfall + 3 Bäche im Umkreis → ja (mit Wasserfall) | 6,1 ha / Bach am Wandfuß → **ja, in einem Bild** | 3,0 ha / Bach 686 m im Umkreis → ja | 6,2 ha / 4 Bäche → ja |
| Biom (Referenz = Nadelwald/bergwald) | **bergwald 79 %** | bergwald/Nordic (Kiefern-Altbestand 769 Zellen) | gletscher 46 / fjord 23 / tundra 21 (Birke 65 %) | wueste (falsch) | oedland 61 / lava 26 (falsch) |
| Entfernung vom Start | 2,6 km | 3,1 km | 3,6 km (Mündung 2,9) | 1,1 km | 1,6 km |
| Instanz-Reserve (Bestand heute) | 97 223 + 1 454 Akteure (07.10.) + Schalen 2 630 | 106 925 + 3 819 Akteure + 13 039 FG → schwerstes Feld | 122 674 (Platz 2 der Welt) | 121 953 | 55 107 → größte Reserve |
| Werkzeuge kalibriert | Rückbau erprobt; Bach = Epic-Bach R3 (kein SWR) | Wasserfall/Hauptfluss nicht SWR (Ferat: warten) | **SWR/Bett/Ufer/Lagen/Bachdekor alle kalibriert** | Felsschalen v4, Desert-Kits | Felsschalen 4 |
| Ladelast Nachbarn | **B4** (106 925 + 3 819 + 13 039 + 150) → Risiko | selbst das schwerste Feld | 3 Felder C2 (65 255 + 21 448 + …) / D2 / C3 | E5 (Start) | gering |
| Rang „Wand → Halde → Bach“ | 3 | 2 | **1** | – (Biom) | – (Biom) |
| Rang „Nadelwald-Hang mit Halde“ | **1** | 2 | 3 (Birken) | – | – |

- **Unsere Einordnung (kein Beschluss):** Pilot = Fenster, nicht Feld; am ehesten **zwei Piloten mit klarer Rolle**: (a) **D2 p2-Quelle** =
  Wand → Halde → Bach in einem Bild, ohne Geländeumbau (Halde/Blöcke/Baumgruppen/Grasflecken fehlen; Birken → Kiefern tauschen; 3 Felder zu laden);
  (b) **B5-Fenster** = Nadelwald-Hang mit Halde im Referenz-Biom (größtes Band 38–50° ohne Netz; nur mit B4 als Nachbar laden, Speicher prüfen).
  Vorbereitung unabhängig vom Feld: Nanite-Umstellung der echten Lücken (Basalt, RA, Escarpments 02, SM_flat_rock_01, Mountain Big_rock,
  Nadelbäume, Birke; Klasse A, gruppenweise), Fab-Raw-Sätze auf 4K klemmen, Halde als FT_EL_FS_*-Foliage (≤ 200–300 Einzelakteure je Zelle).
  Prüfmaße je Pilotbild: unsere Vorschläge stehen in Anhang A (Netz-Pixelanteil, Blöcke je 100 m² auf 25–50°, Fels-Lage ≥ 38° ohne Netz) –
  Schwellen bitte von euch.

## 4. Kernthese als Frage

**„Die Netze müssen die Landschaft tragen, nicht die Textur.“** Stimmt das als Erklärung für den Unterschied zur Hobby-Szene – und wenn ja:
Wie erreicht man ≥ 80 % Felsnetz-Deckung auf Steilflächen in Weltgröße (67 km², 1 018 ha > 30°, 514 ha > 45°) **prozedural** und innerhalb
des Speicherbudgets (RAM 50,6 GB, Grafik 23,7 GB, heute 2,92 M Instanzen + 12 925 Einzelobjekte (07.10.) + 150, Nanite bei 1 082 von 1 965 Netzen,
Stück-Anteil zuletzt 07.10. 22 %)? Die Hobby-Szene ist
vermutlich ein von Hand gesetztes Fenster von wenigen Hektar; unser Problem ist, dieselbe Dichte als Regelwerk über 1 000 ha Steilfläche zu bekommen,
ohne dass ein Feld beim Laden kippt.

## 5. Auftrag

1. **(a) Regeln „Felsdeckung je Hangneigung und Biom“ mit Zahlen:** Welche Netzklasse auf welche Neigung – Klippenmodule in Schichtbändern an
   Wänden > 45° (Bandhöhe, Versatz, Reihenlogik, Grat/Plateau, Turmklotz je Massiv), Halden/Blockfelder 30–45° (Blöcke je 100 m² nach
   Größenklassen, Schutt, Eingraben, Stapelung, Abnahme hangab), Platten mit Fugenbewuchs an Hangfüßen, Baumgruppen zwischen Blöcken (Gruppengröße,
   Lücken, Höhenklassen, Grat-Regel, Nadel/Laub), Gras nur in Flecken. Je Biom (bergwald, fjord, gletscher, kueste, tundra, wueste/canyon,
   elfenwald, dschungel, lava/oedland) die Abweichungen. Bitte eure Zahlen – unsere Ableitungen in Anhang A sind nur zur Prüfung. Dazu die
   Grenze „keine Brockenflut“ (Ferat, E4: +1 327 Füller abgelehnt): Anhang A rechnet unsere Halden-Ableitung auf 110 000–165 000 Instanzen je Feld
   hoch – bitte eine Dichte vorschlagen, die als Halde liest, und benennen, ob Anzahl, Größe oder Gleichförmigkeit das Problem ist (wir fragen
   Ferat parallel).
2. **(b) Pilot: ein Fenster/Feld** aus den Kandidaten in §3.4 (oder ein besserer Vorschlag) mit vollständigem Plan: Instanzen im FORMAT-§3-Setzer-Format
   (`vorlagen/FORMAT.md`, Thema + Kürzel, Foliage FT_EL_FS_* für Blöcke/Schutt/Platten), **Akteure** für große Module (Klippenbänder, Türme, Hero-Blöcke
   ≥ 4 m), dazu – falls nötig – ein Höhenplan im A15-Format für Halde/Stufen/Plateau (Delta-Karte und Querschnitte als Bild vorher, wie 16h-N6c) und
   Lagen-/Grasmasken (Fels-/Geröll-Lage unter Blöcken, Gras-Lage nur in Fugen; Vorlage `sehens_einbau/*`). Ausdünnung des Altbestands als Maske für
   `remove_foliage_by_mask`.
3. **(c) Erweiterung unserer Planer oder PCG:** `fs_plan.py` v8 → v9 (Parameter: Neigungsklassen 25–50°, Halden-Poisson, Stapelung, Eingraben,
   Platten-Rolle, Band-/Reihenlogik aus `klippen_plan.py` 2.1 für Binnenwände, Turm-Modus ohne „nicht über Wand“), `wit_plan.py` (fels_lage-Grenze,
   Block je Baum, Höhenklassen, Grat-Regel, Ausdünn-Maske), Bachdekor (Blöcke ≥ 1 m mit SWR-Umfluss-Prüfung, „Stamm quer“) – oder stattdessen PCG
   (Electric-Dreams-Graphen liegen im Projekt, PCGMeshSampler fehlt in Python, Nanite Foliage experimentell). Bitte begründen, was bei 67 km² und
   unserem Betrieb (WMI-Ketten, Feld für Feld, kein ue.py parallel) realistischer ist.
4. **(d) Speicher-/Leistungs-Schätzung** je Regelwerk: Instanzen je Feld (heute max 142 640 + 3 819 Akteure; Halden-Ableitung aus Anhang A =
   +110 000–165 000 je Feld), Nanite-Dreiecke, Einzelakteure je Zelle (euer Hinweis: Hitches ab 200+ beobachten), VSM-Last (Absturz 08.10. bei
   14,4/23,7 GB), Textur-Pool 8 000 MB (Nanite-Pool Engine-Standard, ungeprüft), Ladezeit je Feld; welche Netze vorher auf Nanite (Basalt, RA,
   Escarpments 02, SM_flat_rock_01, Mountain Big_rock_01/02, Nadelbäume, Birke – die Mountain-Wandmodule sind schon Nanite) und welche Raw-8K-Sätze
   auf 4K geklemmt werden müssen.
5. **(e) Einkaufsliste nur als Vorschlag** (Ferat entscheidet; Kostenpflichtiges nur nach seiner Bestätigung): fehlende Netzklassen aus §3.1 – Nordic-
   Bandmodule 2–6 m für Binnenwände, Blöcke 4–8 m mit Nanite, Nadelbäume 8–15 m (Megaplants Spruce/Pine: kostenlos, aber Nanite Foliage experimentell),
   Flechten-/Moos-Material; je Posten Name/ID, Größe, Nanite ja/nein, wofür.
6. **(f) Reihenfolge nach Wirkung:** Was bricht zuerst sichtbar, und in welcher Reihenfolge lohnt der Einbau? Unsere Lesart in §2.3 (glatte Hänge
   ohne Halde → Felsgröße → Stufen/Bänder → Bach → Wald → Facetten) ist nur eine Hypothese aus den Bildern – bitte eure Reihenfolge mit Aufwand
   je Schritt und dem Punkt, ab dem ein Prüfbild wie die Referenz liest.
7. **(g) Messkriterien:** Bedeckung aus Draufsicht-/Schräg-Capture (SceneCapture mit `hide_actor_components`, Landschaft ausgeblendet → Pixelanteil
   Netz/Landschaft je Bild, wie `swr/basecolor_messen.py`), Deckungsraster für Zellen 25–50° (Erweiterung von fs_deckung_c), „Fels-Lage ≥ 38° ohne Netz“
   aus `lage_Fels.r8` + `hoehe.f32` + `gesetzt_<Feld>.json`, Blöcke je 100 m² nach Klasse, Baumgruppen-/Lücken-Statistik, Grat-Reihen-Zähler; je Maß
   Schwelle für „bestanden“.

Wir geben keine Gestaltungsregeln vor – in §1–§3 stehen Beobachtung, Zahlen und Fragen; unsere eigenen Zahlen-Ableitungen stehen getrennt in
Anhang A und sind nur zur Prüfung gedacht; die Regeln kommen von euch. Ferats Wünsche (Witcher-Qualität, „keine Brockenflut“, Wasserfälle warten,
SWR als Wasser, Fab-Downloads nur durch ihn) sind die einzigen festen Vorgaben.

## 6. Ausgabeformat

- Markdown `antworten/21-detailgrad-landschaft-felsdeckung.md` mit den Regeln (a), der Reihenfolge (f), den Messkriterien (g), der Schätzung (d) und
  der Einkaufsliste (e) als Tabellen mit Zahlen.
- Pilotplan (b) als JSON im FORMAT-§3-Setzer-Format (`vorlagen/FORMAT.md`) je Thema (z. B. `halde_<Feld>`, `klippenband_<Feld>`, `platten_<Feld>`,
  `baumgruppen_<Feld>`; Kürzel ≠ „bach*“), Akteure-Liste für große Module, optional Höhenplan im A15-Format (`sehens_einbau/A15_*`) + Lagen-/Grasmasken,
  Ausdünn-Maske für den Altbestand; dazu Delta-Karte, Querschnitte und eine Skizze „Wand → Halde → Tal“ als Bild.
- Planer-Änderungen (c) als Parameterliste bzw. Patch-Beschreibung gegen `scripts/felsschalen/fs_plan.py`, `scripts/witcher_bewuchs/wit_plan.py`,
  `scripts/klippen/klippen_plan.py`, `scripts/bachdekor`; Referenzskripte gern unter `antworten/skripte/felsdeckung/`.
- Unsere Prüfbilder GEF_*/P2C_* liegen lokal (`Saved/Screenshots/WindowsEditor/`); BERG11_* unter `bilder/sehens13/`. Weitere Bilder (z. B. Draufsicht
  der Kandidaten-Fenster, Delta-Karten) liefern wir auf Anfrage nach `bilder/detailgrad/`.

## Anhang A – Unsere Ableitungen (nur zur Prüfung, keine Vorgaben)

Abgeleitet aus der Referenz-Beschreibung (§1) und Witcher 01–07; je Maß EINE Zahl (frühere Fassungen dieses Auftrags hatten Doppelwerte, hier
bereinigt). Alles Diskussionsgrundlage für §5 (a) und (g) – bitte ersetzen, streichen oder bestätigen.

| Maß | Unsere Ableitung | Herkunft |
|---|---|---|
| Felsnetz-Anteil | Wand+Halde-Szenen (Kamera 0–150 m): ≥ 80 % der sichtbaren Geländefläche Netz, Textur ≤ 20 %; Talkopf-Szenen ≥ 40 %. Messung: Pixelanteil Netz/Landschaft je Prüfbild (SceneCapture, Landschaft ausgeblendet) | Referenz „≥ 80 %“ |
| Haldenband | am Fuß jeder Wand ≥ 20 m; Breite 0,3–0,5 × Wandhöhe (= 20–60 m bei 40–120 m Wand); Neigung 30–38°; ≥ 10 Blöcke 1–8 m je 100 m² (Mischung ~5 × 1–2 m, 4 × 2–4 m, 1 × 4–8 m; Median ≥ 2 m, ≥ 15 % ≥ 4 m) + ≥ 40 Schuttstücke 0,2–0,8 m je 100 m²; Netzbedeckung ≥ 80 % oben, Abnahme auf ≥ 20 % am unteren Rand; Blöcke 30–50 % eingegraben; Stapelung erlaubt. Prüfung: Deckungsraster wie fs_deckung_c auf Zellen 25–50° | Referenz „ganz aus Halden“, Witcher 06 (Eingraben), Natur-Schüttkegel |
| Klippen 3D | je Wandfront ≥ 30 m Schalen/Module in Reihen als Bänder; Bandhöhe 2–6 m; Rücksprung je Band 0,5–2 m; Bänder waagrecht ± 5°; Netzdeckung der Schauseite ≥ 90 % (deckung_bis_30m je 120-m-Abschnitt ≥ 0,9); Gratkante aus Netz mit Plateau ≥ 10 m Tiefe und Abbruch ≥ 10 m; je Massiv 1 Turmklotz ≥ 20 m über dem Grat | Referenz (Stufen 2–6 m, Plateau, Turm) |
| Texturflächen | zusammenhängende Texturfläche ohne Netz/Busch/Gras ≤ 10 × 10 m je Prüfansicht; Texturanteil in Berg-/Hangbildern ≤ 20 %; Fels-Lage ≥ 38° ohne Netz ≤ 10 % | Referenz „0 % Textur als Fläche“ |
| Vordergrund-Platten | an Hangfüßen/Blickpunkten (0–30 m) ≥ 3 Platten/Klötze 3–10 m je 100 m²; 30–50 % der Höhe eingegraben (eure frühere Recherche: 40–50 %); Fugen 0,2–1 m mit Grasbüschel/Moos auf ≥ 70 % der Fugenlänge; Flechten auf ≥ 50 % der Oberseiten | Witcher 04, Referenz |
| Bach | je 5 m Lauf 1 Block 1–3 m (≥ 1,5 m), der aus dem Wasser ragt, ≥ 30 % davon im Wasser als SWR-Hindernis; Beckenabstand unregelmäßig 3–12 m, Beckenbreite 1–3 × Bettbreite; Uferstufe 0,2–0,5 m (16h-N6); auf ≥ 50 % der Uferlänge ein Fels ≥ 0,8 m innerhalb 2 m; Gischt an jedem Block ≥ 1 m. SWR-Falle: Block ≤ 40 % Bettbreite oder Umfluss geprüft | Referenz „verstopft“, Witcher 01/03 |
| Baumgruppen | 3–8 Nadelbäume 8–15 m je Gruppe, Ø 12–25 m, Gruppenabstand 15–40 m; Hänge > 18°: ≥ 35 % baumfrei (Lücken ≥ 15 m), Altbestand auf max. 4 Bäume je 100 m²; Kronendeckung Felszone 15–30 %; ≥ 3 Höhenklassen (4–6 / 8–10 / 12–15 m), höchster ≥ 1,8 × niedrigster, 30–40 % Jungbäume | Referenz, Witcher 04/06/07 |
| Grat | keine Reihe > 3 Bäume; je 100 m Grat 0–2 Gruppen à 2–4; ≥ 60 % der Kante kahl | Witcher 04 |
| Baumart | Fels-/Schutthänge > 18° Nadelanteil ≥ 85 %; Birken ≤ 25 m zum Wasser/Aue | Referenz „nur Fichten/Kiefern“ |
| Standort | je Baum ≥ 1 Block 1–8 m im Radius 3 m (Block : Baum ≥ 1 : 1), Baumfuß 1–3 m neben einem Block; Planer-Versuch fels_lage-Grenze 0,6 → ~0,9 | Referenz „IM Blockhang“ |
| Gras | Block-/Schutthänge und unter Wänden Gras/Heide ≤ 20 %, Flecken 1–5 m² (≥ 70 % der Büschel in Flecken), ≥ 70 % Stein/Schutt; Auen dürfen dicht bleiben; keine Heide in Wand+Halde-Szenen | Referenz „≤ 20 %, nur Flecken“ |
| Moos/Flechten | jeder Fels ≥ 2 m: Moos/Flechte ≥ 30 % der Oberseite, Moos-Saum ≥ 50 % der Bodenkante; 0,5–1 Büschel je m Fuge | Referenz |
| Totholz | unter Gruppen 1 liegender Stamm je 400–600 m² (Planer ~Poisson 5 je Gruppe statt 1,6), 1 stehender je 15–25 Bäume, 1 Stamm quer im Bach je 100 m | Witcher 03/06 (Referenz: keine Angabe) |
| Tönung | Farbbänder folgen den Geometriestufen (± 5°), Bandhöhe 2–6 m, ≥ 2 Farbtöne je 20 m Wandhöhe; keine Texturwiederholung < 3 m aus 50 m sichtbar; technisch Kopie V18 + wenige Knoten (Welthöhe → Band) oder neu geschriebene Tönungs-Daten | Witcher 06/07 |
| Facetten | keine 1-m-Facetten unter 10 m Kameraabstand; Uferlippen 0,2–0,5 m aus Netzen (Escarpment-Module) auf ≥ 90 % der Uferlänge | Referenz |
| Blickziel / Maßstab | je Ausschnitt ≥ 1 Blickziel (Turm ≥ 20 m, Wasserfall, Bauwerk; 3–6 Türme je Massiv-Kette per fs_plan „turm“ als Versuch); Fernebene ≥ 2 Bergsilhouetten im Dunst; je Bergansicht ≥ 1 Block 3–8 m + 1 Baumgruppe im unteren Wanddrittel | Referenz |
| Prüfmaße Pilot | Netz-Pixelanteil ≥ 80 % (Wand+Halde-Bild vom festgelegten Standpunkt, §1); Blöcke je 100 m² auf 25–50° ≥ 10; Fels-Lage ≥ 38° ohne Netz ≤ 10 %; Grat-Reihen > 3 Bäume = 0 | — |

**A.2 Rechnung „Brockenflut“ (warum wir Ferats Grenze klären müssen):** ≥ 10 Blöcke + ≥ 40 Schutt = 50 Instanzen je 100 m². Auf dem Band 38–50°
ohne Netz (eigene Rechnung): D2 22 ha = 2 200 × 100 m² → **110 000**, B4 27 ha → **135 000**, B5 33 ha → **165 000 Instanzen je Feld**. Heute: D2
122 674, B4 106 925 + 3 819 Akteure (+ 13 039 Felsgruppen) → Verdopplung je Feld; Welt: 1 018 ha > 30° × 50 je 100 m² ≈ 5,1 M Instanzen
(heute 2,92 M insgesamt). Ferat lehnte in E4 +1 327 Füller (Wanddeckung 61 → 83 %) als „Brockenflut“ ab – unklar, ob Anzahl, Größe (viele kleine,
gleich große) oder Gleichförmigkeit (Raster) gemeint ist. Wir fragen Ferat; an euch (§5 a/d): Welche Dichte liest als Halde mit dem geringsten
Instanzbedarf – größere Blöcke 2–8 m, Stapelung, Schutt als Lage/Textur statt Instanzen?
