# Nordküste – Fjord, Küste, Bergwald in Witcher-Qualität (Auftrag 11, Teil B1)

**Projekt:** Eldarien, UE 5.8.3, 1-m-Raster 9577 × 7057, World Partition, Nanite. **Stand:** 2026-10-10.
**Biomgruppe 1:** `fjord`, `kueste`, `bergwald` – Felder C1, D1, C2, H2, A3, B3, I3, A4, B4, I4, A5, B5, I5, B6 (Thema `nordkueste`,
Foliage-Typen `FT_EL_NK_*` unter `/Game/Eldarien/Welt/Foliage/Nordkueste`).
**Lieferung:** dieses Dokument, `skripte/nordkueste_regeln.json` (alle Zahlen, 34 Klassen, 301 Netze), `skripte/nordkueste_plan.py`
(Planer nach FORMAT.md §3/§5, Ebenen 0 boden, 1 mittel, 2 baum, 5 wasserkante; Ebenen 3 fels und 4 spuren als `felsgruppen_overrides` /
`spuren_overrides` für die Planer aus Teil C und D).
**Status:** Skript syntaxgeprüft und mit einem **synthetischen** B5-Fenster rauchgetestet (Abschnitt 4). **UNGETESTET MIT ECHTDATEN, kein
Setzen im Editor.** Alle 301 Netzpfade maschinell gegen `daten/netze.csv` geprüft (0 Fehler). Zahlen ohne Quelle sind Richtwerte.
Web-Quellen liegen nur als Suchauszüge vor (kein Direktzugriff auf 80.lv/GDC Vault/Kotaku aus dieser Umgebung) und sind so gekennzeichnet.
**Korrektur Runde 1 (10.10.2026):** Zuständigkeit strikt nach Biom-Zellen + 30-m-Saum, leerer `plan.json` bei < 2 % Eigenanteil, neue
Pflichtschlüssel, Feld-Budget, Schicht 1 nur noch Sonderformen (generische Klassen → `mittelschicht_overrides`). Regeldatei jetzt 21 Klassen,
150 Netze im Planer. **Abschnitt 7 ersetzt, wo er abweicht, die Abschnitte 2–4 und 6.**

## 1. Witcher-Analyse: Skellige als Messlatte für Fjord, Küste und Bergwald

**Was die Zielbilder zeigen** (witcher_03/04/06/07, Analyse in `bildkritik-witcher-messlatte.md`): witcher_07 baut den Nadelwald aus
dunklen Fichten, rostroten Lärchen und Mischhöhen, dazwischen Nebelbänder; witcher_04 setzt eine Felskante mit Blumen und Kräutern in
1–3 m als Vordergrund vor Wand und Dunst; witcher_06 staffelt Wand → hausgroße Blöcke → Kopfsteine → Schnee in Rissen; witcher_03 füllt den
Nadelwald in Augenhöhe mit Fichtenast, jungen Fichten 1–3 m, liegenden Stämmen, Wurzelteller und Blöcken. In keinem Zielbild fehlt ein
Objekt in 0,5–3 m innerhalb von 10 m, in keinem trägt eine Fläche nur einen Maßstab.

**Was über Skellige belegt ist (Suchauszüge).**

- *Pipeline und Reihenfolge:* CDPR baute alle Pflanzen in SpeedTree; Vegetationsexperte Michał Buczkowski legte **eigene Asset-Bibliotheken
  je Region (u. a. Skellige)** an; die Künstler begannen mit Referenzen für die **großen Bäume, dann kleinere Bäume, dann Farne und Gras**,
  und setzten mit **Pinseln je Geländetyp** (Felder, Wiesen, Sümpfe, Wälder). LODs und Zeichenabstände wurden je Netz von Hand gesetzt
  ([80.lv „World Building of Witcher 3“](https://80.lv/articles/world-building-of-witcher-3)). Das ist genau die Schichtreihenfolge des
  Planers (Ebene 2 → Kronendach → 1 → 0 → 5) und der Grund, warum jede Schicht eigene Sichtweiten bekommt.
- *Baumdichte Skellige:* Kotaku beschreibt die Inseln als Heimat **vieler Nadelbaumarten, aber mit spärlichem Baumbestand**; Velen dagegen mit
  Beständen gemischten Alters und Kronenlücken, in denen Sämlinge und Sträucher wachsen
  ([Kotaku „There's Real History, And Beauty, In The Witcher 3's Forests“](https://kotaku.com/theres-real-history-and-beauty-in-the-witcher-3s-fore-1825547736)).
  Die Konzeptkunst nennt Skellige ein Land aus „looming cliffs, brisk streams, and dark pine forests“
  ([Valkyrie/Tumblr-Zitat der Concept-Art](https://nyiro.tumblr.com/post/144674276642/the-witcher-3-concept-art-skellige-the-rocky-and);
  Übersicht der Konzeptbilder bei [TCRF](https://tcrf.net/Prerelease:The_Witcher_3:_Wild_Hunt/Location_Concept_Art)). Folgerung: **offener
  Artenmix statt dichter Monokultur** – der Planer setzt im Ersetzen-Modus bewusst weniger, aber gemischte Bäume (Abschnitt 3, Ebene 2).
- *Reale Vorbilder:* Fan- und Reiseseiten nennen Norwegens Küste (Lofoten, Fjorde), Island, Irland und Schottland; der Name wird auf irisch
  „Sceilg“ (Fels/Klippe, Skellig Islands) zurückgeführt ([View Norway](https://viewnorway.no/only-in-norway/norway-witcher3-skellige-inspiration),
  [Consolepulse](https://consolepulse.com/multiplatform/the-witcher/guides/the-witcher-3-skellige-explained),
  [MultiplayUK](https://multiplayuk.com/the-real-life-inspirations-behind-the-witcher-3s-landscapes-and-locations/)). Kein CDPR-Zitat
  dazu gefunden; für die Regeln reicht die Landschaftslogik: **Klippenküste mit Strand nur in Buchten, Hangwald aus Nadelholz mit Birke als
  Pionier, tiefe Waldgrenze, darüber Krüppelholz, Heide, Gras und Fels.**
- *Verteilungstechnik W3:* Gollents GDC-2014-Vortrag beschreibt einen **Offline-Vegetationsgenerator plus On-the-fly-Verteilung**, eine
  **Pigment-Map**, die Pflanzen in die Bodenfarbe einblendet, und ein Stempel-/Pinselwerkzeug zur Handkorrektur
  ([GDC Vault](https://www.gdcvault.com/play/1020197/Landscape-Creation-and-Rendering-in),
  [Folien-PDF](https://media.gdcvault.com/GDC2014/Presentations/Gollent_Marcin_Landscape_Creation_and.pdf),
  [NeoGAF-Zusammenfassung](https://www.neogaf.com/threads/witcher-3-world-building-gdc-slides.790583/)). Dichtezahlen enthalten die
  Auszüge nicht. Die Pigment-Map entspricht bei uns dem RVT-Bodenblend (`fels-organisch.md` §c) und der Bodenlagen-Gewichtung je Klasse.
- *Witcher 4 (Kovir, State of Unreal 2025):* Nanite Foliage („jedes Blatt und jede Nadel modelliert“, voxelisierte Fernstufe), UAF,
  FastGeo-Streaming; PCG wird in den Auszügen nicht genannt ([CDPR Pressemitteilung](https://press.cdprojektred.com/en/news/1778/cd-projekt-red-and-epic-games-present-the-witcher-4-unreal-engine-5-tech-demo-at-the-state-of-unreal-2025),
  [Game Informer](https://gameinformer.com/2025/06/03/get-a-new-look-at-the-witcher-iv-in-unreal-engine-technical-showcase),
  [TechRadar](https://www.techradar.com/gaming/the-witcher-4-gets-new-tech-demo-showcasing-our-first-look-at-open-world-gameplay-and-it-gave-me-goosebumps)).
  Relevant: dichte Mittelschicht (Jungfichten, Totholz) und gestaffelter Boden – witcher_03.
- *Künstler-Portfolios* (Foreman, Niepokólczycki auf [ArtStation](https://www.artstation.com/artwork/L8LlP)) nennen nur „Skellige – final passes“, keine Zahlen.

**Abgeleitete Schichten zwischen Boden und Krone (Skellige-Typ), mit Zielwerten für den Planer:**

| Schicht | Inhalt in Skellige / Kovir | Dichte / Gruppe (Richtwert, aus Zielbildern gezählt) | Im Planer |
|---|---|---|---|
| Boden 0–0,3 m | Nadelstreu-Flecken, Zweige/Äste um Stämme, Kiesel und Geröllsaum an Fels, Moospolster am Felsfuß und am Bach, Pilze an Stämmen, Klee im Laubanteil | 0,03–0,07 Objekte/m² unter Kronen, Flecken 6–12 m | Ebene 0: 6 Klassen, 0,035+0,03+0,02+0,02+0,004+0,012 /m² beschattet |
| Mittel 0,3–3 m | Jungfichten/-kiefern 1,5–7 m in Saum und Lichtung, Hasel/Holunder, Farninseln, Heide-/Beerenteppiche, hohe Grasbüschel, liegende Stämme, Stümpfe, Wurzelanläufe, Efeu an Fels; an der Küste Strandrose, Sanddorn, Strandhafer, Klippenblumen | 2–5 Objekte je 100 m² innerhalb 10 m um jede Kamera; Inseln 4–30 Stück, Saum 2–3,5× | Ebene 1: 15 Klassen, Summe 0,02–0,06/m² je nach Licht |
| Baum | Kiefer 19–29 m als Leitart, mittelalte Kiefer, Tanne als Fichten-Ersatz (dunkle Horste in Schatten/Bachtälern), Birke als heller Akzent, Hainbuche unten, Küstenkiefer/-eiche windgeformt, Totbäume an der Waldgrenze | 60–150 Bäume/ha, Gruppen 18–60 m, Lichtungen 15–25 %, Höhen 0,7–1,3 | Ebene 2: 8 Klassen, Klumpung 35–60 m, Windflucht |
| Höhenstufen | 0–60 m Spülsaum/Strand/Klippenwiese; 40–450 m Hangwald; 450–700 m Waldgrenze, Krüppelkiefer, Heide, Fels | Waldgrenze tief (nordisch) | `waldgrenze` 420 → 560 m, Krüppel bis 640 m |
| Farbakzente | Birke (hell), Heide (violett), Strandrose (rosa/weiß), Stranddistel, Windröschen-Inseln, Rost von Totholz, Tang im Spülsaum | wenige, aber dichte Inseln (8–30 Stück) | `blume_wald`, `blume_kueste`, `heide_beere`, `birke` mit Klumpung-Schwelle 0,45–0,55 |
| Blickziele | Felsnase über dem Fjord, Solitär-Küsteneiche auf der Klippenwiese, Bachmündung mit Kiesfächer, Totbaum-Gruppe am Grat, Klippenwiese mit Blumen | 1–3 je Feld | Küsteneiche-Trupps (`kuesteneiche`), Totbaum ×2,5 an der Waldgrenze, Felsnasen über `felsgruppen_overrides` (wand 1,2–1,3) |
| Spuren | Fischersteg, Boote, Pfahlzäune, Trockenmauern um Weiden, Steinmänner am Grat, Hügelgräber, Holzschlag-Lichtungen im Bergwald | 1–2 je 100 m² im Umland | `spuren_overrides` (steinmann 1,2–1,8, steg 1,5–2,0, holzschlag 1,6 bergwald) + Stümpfe ×2,5 an Lichtungen |
| Wasserkante | Spülsaum mit Tang, Treibholz küstenparallel, Kiesel/Kopfsteine, Kiesplatten, Felsufer am Fjord | Kiesel 0,25/m² im 0–14-m-Band, Treibholz 0,012/m² in Buchten | Ebene 5: 5 Klassen, nur am Meer (`kueste_nur`) |

## 2. Regelwerk je Schicht (Zahlen aus `nordkueste_regeln.json`)

**Dichtemodell.** Je Klasse `d = dichte[licht] × biome[b] × biom_faktor_ebene × Lagen × Hang × Höhe × Küste × Wasser × Saum/Lichtung ×
Klumpung × Fels-/Baum-/Totholznähe × faktor`. `dichte = [offen, beschattet]` wird linear mit der Beschattung gemischt. **Licht** kommt aus
einem Kronendach: alle Bäume aus `bestand/`, `witcher/` (Feld + 8 Nachbarn), `instanzen/instanzen.json` und den hier geplanten Bäumen
werden mit π·(4,5 m·s)² gesplattet, Gauß σ 5 m geglättet, Beschattung = 1 − exp(−1,5·Deckung); Wald = Beschattung > 0,35, Saum 12 m außen
+ 8 m innen, Lichtung = Beschattung < 0,15 im 25-m-Umfeld des Waldes, Lichtungsrand 8 m. Ohne bekannte Bäume wird aus `lage_Nadeln/Laub`
(0,9) und `Moos` (0,4) geschätzt, Deckel 0,7. **Lagen** wirken als Gewicht `1 + Σ(w−1)·Deckung` (Modus `gewicht`) oder als reine Maske
`Σ w·Deckung` (Modus `nur`: Pilze, Klee, Waldblumen, Efeu). **Hang** `[voll_bis, null_ab]` je Klasse (Bäume 32–42°, Kleinzeug 25–44°),
harte Sperre > 40° außer `kletter`-Klassen (Moos bis 55°, Heide 44°, Krüppelkiefer 46°, Efeu 35–85°, Felsufer bis 60°). **Höhe** als Rampe
(Waldgrenze: Kiefer 420 → 560 m, Tanne 400 → 540, Birke 480 → 600, Krüppelkiefer 470 → 640, Grasbüschel bis 660, Totbaum bis 640 mit
Faktor 2,5 im Waldgrenzband). **Küste**: Trapez über den Abstand zur Meeres-Wasserlinie (`karte_wasser` ∧ Höhe ≤ 0,6 m, Abstandsfeld bis
500 m), **Wasser**: Trapez zu beliebigem Wasser (Bach/See/Meer). **Klumpung**: Wertrauschen (2 Oktaven, 6–60 m) mit Schwelle 0,25–0,55 –
Schwelle 0,4 bei Kiefern ergibt 15–20 % Lichtungen, 0,55 bei Blumen wenige dichte Inseln. **Gruppen** (`gruppe_n`, `gruppe_radius_m`):
Zentren mit d/⌀n gestreut, Mitglieder gleichverteilt in der Scheibe und an ihrer Zelle erneut gegen Sperren und d > 0 geprüft.
**Biomfaktor je Ebene:** fjord 0,8/0,8/0,55/1,0 (Ebene 0/1/2/5), kueste 0,8/1,0/0,7/1,0, bergwald 1,0/1,0/1,0/0 (kein Meer-Spülsaum im
Bergwald; Fjordufer am Bergwald-Feld A4 kommt über die Kueste-/Fjord-Zellen aus `eigner.r8`). **Sperren:** Wasser + 0,6 m, Weg 2,5 m
(klein) / 4 m (Bäume, Totholz), Ort 5 m, `standorte.json` 5 m (Format geraten, Fehlen wird gemeldet), vorhandene Bäume 0,9 m (klein) /
4,5 m (neue Bäume), Baum–Baum 3,5 m (eine Instanz je 3,5-m-Zelle, Hash-Priorität), vorhandenes Witcher-Kleinzeug 0,5 m, Lagen Lavafels/
Lavasand/Eis 0, Schnee 0,35, Sandstein 0,5. **Deterministisch:** 32-bit-Hash aus (Weltzeile, Weltspalte, Seed 1911 + Ebenenseed, Kanal);
Nachbarfelder planen im 64-m-Überlapp dieselben Instanzen.

**Ebene 0 – Boden (6 Klassen, Sichtweite 35–80 m, nie Kollision, kein Schatten, Kippen voll auf die Normale).**
`nadelstreu` 0,004 → 0,035/m² (offen → beschattet), Nadeln ×2,2, Laub ×2,0, Flecken 9 m (DeadLeaves/detail_leaves als Stand-in, Einkaufsliste);
`zweige` 0,003 → 0,03/m², ×2 im 6-m-Umkreis von Stämmen, 24 Netze (Sticks, DryBranches, OldTreeBranch kurz); `kiesel` 0,02 → 0,012/m², Kies ×3,
Geröll ×2,5, Fels ×2, ×2,5 im 8-m-Saum um Fels-Lage, Eingraben 35 % der Netzhöhe (SmallStonesPack, stone_03…08, mountain_rock_small);
`moos` 0,002 → 0,02/m², Moos ×3, Fels ×1,5, ×2 an Felsfüßen, Bachnähe (0–12 m voll, fern 0,5), bis 55°; `pilz` 0 → 0,004/m² nur in Nadel-/
Laub-/Moos-Lagen, Hexenringe 3–9 (Radius 0,3–1,2 m), ×2,5 an Stämmen (≤ 4 m) und ×2,5 an liegenden Stämmen/Stümpfen aus Ebene 1 (≤ 2,5 m);
`bodendecker` 0,003 → 0,012/m² (Klee, Sauerklee, Keimlinge) nur in Laub/Moos/Nadeln/Erde/Gras. Biome: fjord 0,3–1,2, kueste 0,4–1,0,
bergwald 0,8–1,0 (Kiesel im Fjord 1,2).

**Ebene 1 – Mittelschicht 0,3–3 m (15 Klassen).**

| Klasse | Dichte offen → beschattet /m² | Gruppe | Lage / Bedingung | Sichtweite m | Kollision |
|---|---|---|---|---|---|
| `strauch_wald` Hasel, Holunder, Ahorn-Busch | 0,0035 → 0,0012 | 1–4, r 1–3,5 m | Saum ×3, Lichtungsrand ×1,6, bis 520 m | 250–400 | nein |
| `strauch_kueste` Strandrose, Sanddorn, Krüppelkiefer klein | 0,006 → 0,002 | 2–6, r 1,5–5 m | 3–260 m Küstenabstand, bis 260 m Höhe, Yaw küstenparallel (Lee) | 250–400 | nein |
| `krueppelkiefer` Latsche | 0,004 → 0,001 | 2–7, r 1,5–6 m | 380/470 → 640/720 m Höhe, Fels/Heide/Trockengras ×1,2–1,5, bis 46° | 300–500 | nein |
| `jungbaum_nadel` Kiefer/Tanne 1,5–7 m | 0,005 → 0,0015 | 2–8, r 1,5–6 m | Saum ×3,5, Lichtungsrand ×2,5, bis 560 m | 300–500 | nein |
| `jungbaum_laub` Hainbuche | 0,002 → 0,0025 | 2–6 | Laub ×2, < 380 m, nur bergwald/kueste | 250–400 | nein |
| `farninsel` | 0,002 → 0,03 | 4–14, r 1,5–5 m | Moos ×1,8, Laub ×1,5, Wassernähe 0–25 m voll (fern 0,6), Nordhang ×1,5 | 120–200 | nein |
| `heide_beere` | 0,012 → 0,006 | 5–20, r 1,5–6 m | Heide ×3, Trockengras ×1,5, bis 44° | 120–200 | nein |
| `grasbueschel` hoch 0,6–1,5 m | 0,02 → 0,004 | – | Gras/Wiese/Trockengras ×1,3–1,6, ×1,8 um Fels, bis 660 m | 100–150 | nein |
| `strandgras` Strandhafer | 0,05 → 0,02 | 6–25, r 1,5–5 m | Sand ×2, 2–90 m hinter der Wasserlinie, ≤ 80 m Höhe | 100–150 | nein |
| `blume_wald` Windröschen, Maiglöckchen, Immergrün | 0,004 → 0,006 | 8–30 | nur Laub/Moos/Erde/Nadeln/Gras, Saum ×1,8, Klumpung 0,55 | 80–120 | nein |
| `blume_kueste` Stranddistel, Wundklee, Kamille | 0,01 → 0,002 | 8–30 | 3–400 m Küstenabstand, ≤ 320 m | 80–120 | nein |
| `totholz_liegend` | 0,0006 → 0,0018 | – | hangparallel (Yaw `hang`), Eingraben 28 %, ×1,6 an Stämmen, Weg 4 m | 350–600 | **ja** |
| `stumpf` | 0,0008 → 0,0012 | – | Lichtungsrand ×2,5 (Holzschlag) | 300–500 | **ja** |
| `wurzel` Wurzelanläufe | 0 → 0,0012 | – | nur ≤ 3 m um Stämme (×4), hangabwärts | 200–350 | nein |
| `kletter` Efeu | 0,012 fest | – | nur Fels/Moos/Felsplatte-Lage, Hang 35–85° | 80–120 | nein |

Im beschatteten Bergwald summieren sich Farn + Jungbaum + Strauch + Totholz + Stumpf auf ≈ 0,036/m² = **3,6 Objekte je 100 m²** in
0,3–3 m, im Saum (×3–3,5 auf Strauch/Jungbaum) ≈ 0,06/m² – die Witcher-Spanne aus `verteilung-leere-fuellen.md` §1.

**Ebene 2 – Bäume (8 Klassen, Sichtweite 0, Kollision, Schatten, Kippen 5–10 %, eine Instanz je 3,5 m).** `kiefer_alt` 0,0075/m² (Forest_pine
02–09, 19–29 m), Klumpung 45 m / Schwelle 0,4 (Lichtungen 15–20 %), Gruppenskala 18 m mit Höhen-Kohärenz 0,5 (Gruppen haben ähnliche Höhe, Maßstab
0,75–1,3); `kiefer_mittel` 0,0025 (Forest_pine_01, pine_beach_02, 10–16 m), Saum ×2; `tanne` 0,0035 (Fir_03–06, Fichten-Ersatz), Klumpung 60 m /
0,5 → dunkle Horste, Nordhang ×1,6, Bachnähe ×1 (fern 0,7), 140–400 m; `birke` 0,0012 → 0,0006 (Big_Tree_Birch_01, einziges Netz), Saum ×2,5,
Lichtung ×1,8, Fjord 1,0; `hainbuche` 0,0022 (Nanite, 6 Netze), Laub ×2, < 340 m; `kuestenkiefer` 0,004 → 0,003 (pine_beach 01/03/04, 5–10 m),
8–450 m Küstenstreifen, Yaw küstenparallel; `kuesteneiche` 0,0015 (dry_oak 01 A–F, 4–9 m), 15–500 m, Klippenwiese; `totbaum` 0,0005
(Forest_pine_10_dead, Fir_08_Dead, Beech_Dead), ×2,5 im Waldgrenzband. **Windflucht** (`meer.windflucht`): innerhalb 180 m vom Meer Z-Maßstab
0,65 → 0,9 und 5–12° Neigung landeinwärts (Lee), linear mit dem Küstenabstand. Biomfaktor Ebene 2: fjord 0,55, kueste 0,7, bergwald 1,0.
**Modus** `baum_modus = auto`: liegt `bestand/<Feld>/` vor → `ergaenzen` (Dichten × 0,35, ≥ 4,5 m Abstand zu vorhandenen Bäumen: Artenmix und
Küstenformen kommen dazu, die Monokultur bleibt); fehlt die Bestand-Ebene → `ersetzen` (volle Baumschicht, `entfernen`-Filter, Abschnitt 3).

**Ebene 5 – Wasserkante (5 Klassen, nur wo Meer im Fenster, `kueste_nur`; Bergwald 0).** `tang` 0,06/m² im Spülsaum 0–5 m über der Wasserlinie,
Höhe ≤ 3 m, Algen ×2 (STAND-IN WaterPlant01–04, flach, bis Tang gekauft); `treibholz` 0,012/m², 1–22 m, Höhe ≤ 6 m, Hang ≤ 25°, Yaw
küstenparallel ±20°, Eingraben 25 %, Kollision; `strandkiesel` 0,25/m², 0–14 m, Höhe ≤ 5 m, Hang ≤ 35°, Eingraben 40 %, Faktor 0,25 wenn die
Ufer-Ebene `ufer/foliage_<Feld>/` im Feld liegt; `strandplatte` 0,004/m² (NordicBeachRockyGround, BeachSandWithPebbles, 3 × 3 m), 45 %
eingegraben, Faktor 0,4 bei Ufer-Ebene; `felsufer` 0,008/m² (IcelandicBoulder, Nordic-Rock-Small, skjsL/xjijbgx 0,6–1,5 m) an Ufern mit
Hang 14–60°, Höhe ≤ 12 m, Fjord 1,0 / Küste 0,5, Kollision.

**Ebene 3 fels / 4 spuren (nur Overrides).** `felsgruppen_overrides`: Palette `nordisch` für alle drei Biome, Biomfaktor fjord 1,15 / kueste
1,0 / bergwald 0,95; Klassenfaktoren fjord wand 1,3, band 1,2, kuppe 1,2, blockstrom 0,8; kueste kuppe 1,4, wand 1,2; bergwald grat 1,2,
blockstrom 1,2, fuss 1,1, band 0,8; Palettenergänzung (NordicBeachRocks_01, TundraMossyBoulder_01 als Hero, MossyForestBoulder_03 als Block,
NordicBeachRockyGround_02/NordicBeach_02 als Platte) und Regel „unter Kronen Mossy-Netze ×2, über der Waldgrenze Granit/Icelandic ×2“.
`spuren_overrides`: Dichtefaktoren je Biom (fjord: Steinmann 1,8, Grab 1,5, Steg 1,5, Pfahlzaun 1,2, Obstbaum 0; kueste: Steg 2,0, Pfahlzaun 1,5;
bergwald: Holzschlag 1,6, Köhler 1,4) und Netzergänzungen (Coast_Dunes-Pfähle, NordicBeachRock/mountain_rock_small als Steinmann-Material).
Wie Teil C/D die Overrides lesen, ist offen (6.4).

**Feldbesonderheiten** (`feld_hinweise`): C1/D1/C2 sind zu 69–46 % Gletscher – Nordküsten-Klassen nur in Fjord-Zellen aus `eigner.r8`; ohne
`eigner.r8` Fallback `fjord` bis 230/260/260 m Höhe, darüber nichts. B6: Lavasand/Lavafels-Lage sperrt, nur Bergwald-Zellen. H2/I4: Laub-Lage →
Hainbuche voll. A5: Klippenküste, Strand nur in Buchten (Hang-Rampen der Ebene 5), Felsnasen vom Klippen-/Felsgruppen-Planer.

## 3. Abgrenzung zu vorhandenen Ebenen und `entfernen`-Filter

| Vorhandene Ebene | Überschneidung | Regel im Planer | `entfernen` |
|---|---|---|---|
| `FT_EL_WIT_*` Witcher-Bewuchs (Laub/Zweige, Farne, Unterwuchs, Blumeninseln, Gebüsch, Totholz, Haine) | Ebene 0/1 ergänzen dieselben Rollen | Vorhandene WIT-Instanzen werden gelesen und mit 0,5 m Sperre belegt; Haine zählen ins Kronendach; Farninseln/Blumen hier bewusst **geklumpt** (WIT ist gleichmäßiger); Küstenklassen und Höhenstufen gibt es in WIT nicht | **nein** (bleibt vollständig) |
| `FT_EL_BST_*` Wald-Bestand (Gruppen, Lichtungen, Artenmix, Totholz 3 %) | Ebene 2 | `baum_modus auto`: Bestand vorhanden → nur ergänzen (×0,35, ≥ 4,5 m Abstand). Bestand fehlt (heute alle Nordküstenfelder außer evtl. keinem) → ersetzen | nur bei `ersetzen`: `sm_forest_pine_0,fir_0,sm_pine_beach_0` – alte Kiefern/Tannen der Witcher-/Bestand-Ebene im Feld, **Begründung:** Monokultur (eine Art, eine Höhe, ein Abstand; W6FIN_G3, FELS7_A4) ist Ferats Hauptbefund; ein Doppelbestand würde die Dichte verdoppeln, ohne den Mix zu ändern. Kleinzeug der WIT-Ebene bleibt |
| `FT_EL_UF_*` Ufer (Kiesel, Kopfsteine, Blöcke, Platten, Treibholz an allen Ufern) | Ebene 5 | Liegt `ufer/foliage_<Feld>/` vor: Strandkiesel ×0,25, Strandplatten ×0,4; Tang, Treibholz (küstenparallel) und Felsufer bleiben voll, weil sie dort fehlen | **nein** |
| `FT_EL_FS_*` Felsschalen + Akteure | keine (Ebene 3 liefert `felsgruppen_plan.py`) | Kiesel-Saum (`kiesel`, `fels_nah`) und Moos/Efeu an Fels-Lage sind die Kontaktzone aus `fels-organisch.md` §c; Felsschalen-Netze werden nicht gesetzt | `entfernen` für FS kommt aus `verteilung-fels-organisch.md` §e, nicht von hier |
| Klippen (A5/B5, Akteure) | keine | Klippenfronten > 40° sind gesperrt; Klippenwiese (0–60 m hinter der Kante) bekommt `blume_kueste`, `kuesteneiche`, `strandgras` oberhalb der Kante nicht (≤ 80 m Höhe) | nein |
| Houdini-Bestand (`instanzen.json`) | Bäume | Als Bäume gelesen (Kronendach, Abstand); fehlt die Datei → Hinweis, Lauf geht weiter | nein |
| Landschafts-Gras `GT_*` 0,2–1,2 m | `grasbueschel` 0,6–1,5 m | bewusst höher als das GPU-Gras (Höhenstufen); Dichte 0,02/m² offen, damit das Gras nicht erstickt | nein |

Felder anderer Gruppen (z. B. G4) werden mit Meldung übersprungen, weil `eigner.r8` dort kein fjord/kueste/bergwald liefert.

## 4. Testanleitung

**Lauf.** `python -I scripts/nordkueste/nordkueste_plan.py B5 A5 B4 H2 C1 --bild` (Regeln neben dem Skript, `--basis` = production-Wurzel;
`--faktor 0.7` wenn das Budget greift). Ausgabe `export/unreal/welt/nordkueste/<Feld>/<Netz>.f32` + `plan.json` (FORMAT §3 plus `ebene` je
Datei und `statistik`: je Klasse, je Ebene, Kollision, Biomanteile, Waldanteil, mittlere Beschattung, Quellen, Modus, Laufzeit), Prüfbild
`docs/pruefung/nordkueste/<Feld>.png` (1 px = 1 m: Grau = Höhe, violett = Beschattung, rosa = Hang > 40°, blau = Wasser, dunkelblau = Meer,
braun = Weg, rot = Ort; Instanzfarben je Klasse aus `farben`, Bäume 2 px). Ein Netz, das in zwei Ebenen vorkommt (SmallStonesPack in 0 und 5),
erhält in der zweiten Ebene den Dateinamen `<Netz>_e5` → eigener Foliage-Typ mit eigener Sichtweite.

**Setzen.** Generischer Setzer auf den Ordner; Foliage-Typen `FT_EL_NK_<Netz>` unter `/Game/Eldarien/Welt/Foliage/Nordkueste`, Einstellungen
aus `dateien` (Sichtweite, Schatten, Kollision). Ebene 2 im `ersetzen`-Modus **zuerst** den `entfernen`-Filter anwenden. Reihenfolge der
Ebenen im Editor ist egal (alles im Planer schon abgestimmt). 300–320 Netze je Feld = ebenso viele HISM-Komponenten; zum Kürzen die `netze`-Listen der Kleinzeugklassen halbieren.

**Erwartete Instanzzahlen je Feld** (Spanne; abgeleitet aus dem synthetischen B5-Lauf, skaliert mit Landanteil und Steilheit aus
`biome_je_feld.md`; Echtdaten können um ±50 % abweichen):

| Feldtyp | Ebene 0 boden | Ebene 1 mittel | Ebene 2 baum (ergänzen / ersetzen) | Ebene 5 wasserkante | Summe | Kollision |
|---|---|---|---|---|---|---|
| Steiler Bergwald 100 % Land (B4, B5: 80 % > 30°) | 12 000–22 000 | 10 000–18 000 | 400–800 / 1 200–2 500 | 0 (B4) / 1 000–3 000 (B5) | 25 000–45 000 | 700–2 000 |
| Hangwald 30–65 % Land (B3, A4, I3, I4) | 6 000–16 000 | 5 000–14 000 | 300–600 / 1 000–2 500 | 0–2 000 (A4 Fjordufer) | 12 000–35 000 | 400–1 500 |
| Küste/Klippe (A5, H2: 24–39 % Land) | 4 000–10 000 | 4 000–10 000 | 200–500 / 600–1 500 | 2 000–6 000 | 10 000–25 000 | 300–1 200 |
| Fjordhang (C1, D1, C2: Fjord 23–31 %) | 2 000–6 000 | 2 000–6 000 | 100–300 / 300–900 | 1 500–5 000 | 6 000–18 000 | 200–900 |
| Flacher Küstenwald (A3 16 %, I5 50 %, B6 63 % Land) | A3 3 000–8 000; I5/B6 15 000–35 000 | 3 000–25 000 | 200–500 / 1 500–5 000 | A3/I5 1 000–4 000, B6 0 | 7 000–60 000 (I5 kann Ebene 0 deckeln) | 300–2 500 |

**Prüfkameras** (cm, FORMAT §1: X = (j − 4730,5)·100, Y = (i − 4060,5)·100; Z = Boden + Angabe):

| Feld / Lage | Position | Blick | Erfolg erkennbar an |
|---|---|---|---|
| **B5 Küste → Hang** (Mitte X −321 850, Y 47 550) | Spülsaum einer Bucht, 1,7 m über Grund | landeinwärts, 10° aufwärts | Tang/Treibholz/Kiesel → Strandhafer-Horste → Strandrosen-Trupps → windgeschobene Küstenkiefern (Z gestaucht, Lee-Neigung) → Hangwald; kein Objekt steht im Wasser, Treibholz liegt küstenparallel |
| **B5 Hangwald innen** | 150 m hangauf im Kiefernwald, 1,7 m | hangparallel | innerhalb 10 m: ≥ 3 Objekte 0,5–3 m (Jungkiefer, Farninsel, Strauch, Stamm oder Stumpf); Boden mit Nadelstreu-Flecken, Zweigen um Stämme, Pilzen an Totholz; Tannen-Horste dunkel in Bachnähe |
| **B5 Waldgrenze** (max 664 m) | 30 m unter dem höchsten Punkt, 2 m | entlang des Grats | Kiefern enden unregelmäßig 420–560 m, darüber Krüppelkiefer-Gruppen, Heide-Teppiche, hohe Grasbüschel, Totbäume gehäuft; keine Baumreihe auf der Kammlinie |
| **A5 Klippenwiese** (X −422 650, Y 47 550) | 20 m hinter der Klippenkante, 1,6 m | zum Meer, Gegenlicht | Vordergrund Stranddistel/Wundklee-Inseln, Küsteneiche als Solitär, Efeu/Moos an Felskanten, Klippenwand frei; Nachstellung witcher_04 |
| **A4 Fjordufer** (X −422 650, Y −53 250) | 2 m über dem Fjordwasser, 100 m vom Steilufer | zum Ufer | Felsufer-Blöcke 0,6–1,5 m statt Strand, Birken als helle Akzente am Hang, darüber Kiefern mit Lichtungen (FELS7_A4-Gegenprobe) |
| **B4 Grat** (X −321 850, Y −53 250; max 684 m) | Sattel, 10 m über Grund | auf den Grat | kahl bis auf Krüppelkiefer/Heide/Gras, Totbaum-Gruppen, Felsgruppen (Teil C) – Wald bleibt unter 560 m |
| **H2 Küstenwald/Elfenwald-Übergang** (X 282 950, Y −254 850) | Waldsaum zur Küstenwiese, 1,7 m | in den Wald | Saum 12 m dichter (Strauch ×3, Jungbaum ×3,5, Birke ×2,5), Hainbuche beigemischt, innen Farn/Klee im Laubanteil |
| **C1 Fjordhang** (X −221 050, Y −355 650) | Fjordufer, 5 m | hangauf | Nordküsten-Bewuchs nur in Fjord-Zellen bis zur Gletschergrenze, kein Nadelwald auf Gletscher-Kacheln |

Zwei-Meter-Probe an jeder Kamera: Pflanzen 2–5 cm im Boden, Steine 35–40 %, Stämme 28 %; Sträucher kippen 30–40 %, Bäume ≤ 10 %; nichts auf Weg, Ort, Wasser.

**Rauchtest (synthetisch, Cloud: Python 3.13, NumPy 2.5, Pillow 12, kein numba).** Mini-Produktionswurzel mit `hoehe.f32` in voller Größe
(memmap 270 MB) und einem synthetischen B5: Klippenküste im Norden, Bucht mit Strand im Süden, Hangwald, N–S-Grat bis 725 m mit Wandstufe,
Kuppe, Bach zum Meer, Weg, Ort, `lage_Fels/Nadeln/Gras/Kies/Sand`, `eigner.r8` (Kachel 7 „kueste_nordisch“ im 210-m-Küstenstreifen, Kachel 3
„aue_bachtal“, Rest 0), `welt.json`, 700 Bestand-Kiefern, 250 Witcher-Farne, `daten/netze.csv`, `netze_masse.json`, `biome_je_feld.json`;
21,6 % Meer, 55 % des Fensters > 40°. Ergebnis **B5 (ergaenzen): 27 114 Instanzen, 757 mit Kollision, Ebene 2: 452, 1: 12 032, 0: 13 098,
5: 1 532; 317 f32-Dateien; 11,7 s** (davon ~1 s Lesen). Größte Klassen: Kiesel 6 890, Grasbüschel 4 094, Zweige 2 901, Efeu 1 939, Nadelstreu 1 877,
Strandgras 1 373, Strandkiesel 1 347, Jungkiefer 1 313, Heide 1 183; Bäume 155 Altkiefern, 115 mittlere, 51 Küstenkiefern, 44 Birken, 46 Totbäume. **Ersetzen-Modus** (Bestand entfernt): 28 326 Instanzen, 1 708 Kollision, Ebene 2: 1 328 (502
Altkiefern, 327 mittlere, 148 Küstenkiefern, 124 Totbäume, 101 Birken, 57 Eichen, 39 Tannen, 30 Hainbuchen), `entfernen` gesetzt, 10,6 s.
**Budgetprobe** `--faktor 3`: 85 530 Instanzen (Ebene 0: 45 465, 1: 34 196, 5: 4 649, Kollision 2 287) – Deckel nicht erreicht, Ausdünnung also
nicht ausgelöst (Code vorhanden, nur gelesen). Geprüft: alle f32 mit 10 float32 je Instanz, keine NaN, Quaternionen normiert (Fehler
< 1,2e-7), x/y innerhalb des Feldes (j 1090–2015 wegen Meer im Westen, i 4032–5039), z −1,6 … 724 m (−1,6 m = bilinearer Spülsaum neben der
synthetischen Meeresstufe, Echtdaten haben einen stetigen Meeresboden), Maßstab 0,5–1,8; `plan.json` mit `dateien{pfad, anzahl, gruppe,
rolle, ebene, sichtweite, schatten, kollision}`, `ft_ordner`, `ft_praefix`, `statistik`, `hinweise`; PNG 1008 × 1008; **zweiter Lauf
byteidentisch** (317/317 Dateien); G4/J3 (fremde Biome, Randspalte J geklippt) → Meldung und kein Output; fehlende `hoehe.f32` → klare
Meldung; fehlende Lagen → Hinweis „Faktor neutral“, Lauf geht weiter. Die großen synthetischen Raster wurden danach gelöscht.

## 5. Einkaufsliste (Fab/Megascans, frei bevorzugt; Namen sind Fab-Suchbegriffe, Fab konnte nicht geöffnet werden)

| Asset (Fab-/Megascans-Name) | Stufe | Wofür | Lücke heute |
|---|---|---|---|
| Megascans „Norway Spruce“ / „European Spruce“ (3–4 Alter, 8–28 m) oder Fab „Spruce Forest Pack“ | High 4K, Nanite Foliage | Ebene 2 `tanne` → echte Fichte (dunkle Nadelmasse witcher_07), Jungfichten 1–3 m für `jungbaum_nadel` (witcher_03) | Fichte fehlt ganz; Tanne (Fir_03–06) als Ersatz, nur 5 Netze |
| Megascans „European Larch“ (Herbstvariante) | High 4K | Rostroter Farbakzent im Hangwald (witcher_07) | keine Lärche |
| Megascans „Silver Birch“ 2–3 Varianten, 6–14 m | High 4K, Nanite | `birke` hat genau 1 Netz (Big_Tree_Birch_01, 28 k Dreiecke, 5 Materialien) | Pionier-Akzent am Fjord ohne Varianz |
| Megascans „Bilberry“ / „Blueberry Shrub“ und „Juniper Shrub“ | High 2K | `heide_beere` (Blaubeere statt black_cherry/beach_rose-Stand-in), Wacholder für Krüppelgürtel | Beere und Wacholder fehlen |
| Megascans „Pine Needles Ground Cover“ / „Forest Floor Needles“ (Decal-/Platten-Netz) | High 2K | `nadelstreu` (heute DeadLeaves als Stand-in) | keine Nadelstreu |
| Megascans „Bladderwrack“ / „Kelp“ / „Seaweed Pile“ | High 2K | `tang` Spülsaum (heute WaterPlant-Stand-in, 2 cm hoch) | kein Tang |
| Megascans „Driftwood“ 3–5 Varianten, 1–4 m | High 2K | `treibholz` (heute 1 Treibholz + OldTreeBranch) | Treibholz-Varianten |
| Fab „Fishing Dock / Wooden Pier“ und „Rowing Boat“ (Medieval) | Medium/High | Spuren (Steg, Boot) via `spuren_overrides.steg` 1,5–2,0 | keine Stege/Boote im Inventar (`assets-taxonomie.md`) |
| Megascans „Nordic Rock Cliff“ 6–12 m | High 4K | siehe `verteilung-fels-organisch.md` §f (Bandstufe 4–8 m) | Fels-Mittelstufe |

Vor dem Kauf prüfen, ob das Megascans-Asset vor dem 31.12.2024 beansprucht wurde (dann frei); nach dem Import Post-Import-Pass aus
`klippennetze-a5.md` (Nanite, Kollision, 4K-Deckel).

## 6. Offene Punkte / Annahmen

1. **Ungetestet mit Echtdaten.** Die Hang-Rampen (Bäume 32–42°, harte Sperre 40°) treffen in B4/B5 (80 % > 30°) große Flächen; liefert der
   Echtlauf dort < 15 000 Instanzen, `hang` der Baum- und Mittelschichtklassen auf [36, 48] heben und `hang_sperre_grad` auf 45 – Nadelwald
   steht real bis ~45°.
2. **Baumzahl im Ersetzen-Modus** liegt mit ~1 300 (steil) bis ~5 000 (flach) je Feld deutlich unter der Bestand-Ebene (17 000 in G4) – gewollt
   (Skellige „sparse“, Lichtungen 15–20 %), aber eine Geschmacksfrage; `kiefer_alt.dichte` 0,0075 → 0,012 verdoppelt den Wald fast ohne Mehrkosten.
3. **Kronendach im Ersetzen-Modus** kommt allein aus den eigenen 1 300–5 000 Bäumen (mittlere Beschattung im Test 0,10, Waldanteil 12 %);
   Farne/Pilze liegen dann am unteren Ende. Die eigene Ebene wird bewusst nicht als „alt“ zurückgelesen (Wiederholbarkeit).
4. **Overrides für Ebene 3/4** (`felsgruppen_overrides`, `spuren_overrides`) sind geschrieben, aber `felsgruppen_plan.py`/`spuren_plan.py` lesen sie
   noch nicht; Abstimmung mit Teil C/D (gemeinsamer Schlüssel `biom_overrides` in deren Regeln).
5. **`welt.json`-Schema** nur aus FORMAT.md bekannt: `kacheln` als Dict oder Liste, Biom per Teilstring im `rezept`; unbekannte Rezepte → „sonst“.
   `standorte.json` Format geraten (x_cm/y_cm oder x/y, radius_m). `instanzen.json`: Dateinamen aus `datei` oder `<name>.f32` vermutet.
6. **Pivot** der Mountain_Environment_Set-/Coast_Dunes-Pflanzen nicht in `netze_masse.json`; Annahme Pivot unten (Pflanzen plausibel). Felsufer-Netze
   (Megascans) haben Einträge.
7. **Tang-Stand-in** (`SM_WaterPlant01–04`, 2 cm flach) ist sichtbar falsch, bis Tang gekauft ist; Klasse ggf. über `biome` auf 0 setzen.
8. **Foliage-Typen je Feld 300–320** (viele Varianten je Klasse) – HISM-Komponenten und Setzer-Laufzeit; kürzen siehe Abschnitt 4.
9. **Kollision**: 757–1 708 je Feld (Bäume, Totholz, Stümpfe, Treibholz, Felsufer), Deckel 3 000 mit proportionaler Ausdünnung – im Test nicht ausgelöst.
10. **Nicht geprüft:** `entfernen`-Verhalten des Setzers, Nanite Foliage (ab 5.7) für die Nicht-Nanite-Kiefern, HLOD der Baumebene.

## 7. Korrektur Runde 1 (10.10.2026)

**Anlass** (`auftraege/verteilung-korrektur-runde1.md`, lokaler Echtdatenlauf, Windows, Python 3.11): A5 (bergwald/fjord) **27 302**
Instanzen – in Ordnung; G4 (elfenwald) und E1 (gletscher) kein Plan – richtig, aber nur als Textmeldung statt leerem `plan.json`;
C6 (Fenster 96,8 % lava + 3 % bergwald) **1 078** Instanzen – zu viel, weil alle Ebenen aller Planer sich in jedem Feld stapeln.
Umgesetzt nach `verteilung-KONVENTIONEN.md` §1–§5.

### 7.1 Änderungen im Planer (`nordkueste_plan.py`)

| Punkt | Vorher | Jetzt |
|---|---|---|
| Biom je Zelle (§1) | eigner 0 → dominantes Feldbiom | eigner 0 → **aue**, Rezept mit „vulkan“ → **lava**; nur ohne `eigner.r8`/`welt.json` dominantes Feldbiom aus `daten/biome_je_feld.json` (Hinweis im Log), danach Regel-Fallback |
| Zuständigkeit (§1) | alle Zellen mit fjord/kueste/bergwald, harte Kante | `biome_eigen` = fjord, kueste, bergwald **plus 30-m-Saum** nach außen: exakte euklidische Distanztransformation (separierbar, NumPy, keine Zellschleifen), Dichtefaktor 1 an der Biomgrenze → 0 bei 30 m; im Saum gelten die Regeln des **nächsten** eigenen Bioms (Label-Weitergabe in derselben Transformation). Jitter-Punkte, die über die Saumgrenze oder auf Sperrzellen fallen, werden verworfen |
| Fremdes Biom (§1) | `return None` + Textzeile | Eigenanteil im Fenster < 2 % → **leerer `plan.json`** (`instanzen: 0`, `dateien: {}`, alle Pflichtschlüssel, alte f32 gelöscht), eine Hinweiszeile, Exit 0; ebenso, wenn eigene Zellen nur im Rand liegen |
| `plan.json` (§2) | `statistik.biome_anteil` | neu oben: `biome_fenster` (Anteile aller Biome im Fenster, absteigend), `zellen_zustaendig` (Feldzellen inkl. Saum), `biome_eigen`, `kollision_anzahl`; `statistik.zustaendigkeit` mit Quelle, Eigenanteil Fenster/Feld, Zellen eigen/Saum, Rohzahl vor Budget |
| Budget (§3) | 60 000 **je Schicht** (zusammen bis 135 000 möglich), Kollision proportional per Zufall | Schicht-Ziele (0: 30 000, 1: 20 000, 2: 12 000, 5: 15 000), dann **Feld-Ziel 50 000 für die ganze Nordküsten-Ebene**, hart 60 000; Kollision hart 3 000. Ausdünnung exakt (Hash-Rang, `floor`) von der niedrigsten Priorität aufwärts, `WARNUNG` im Log und Eintrag in `hinweise`; bei Schicht 0 zusätzlich Hinweis „Kleinzeug an Landschafts-Gras“ |
| `entfernen`-Filter | bei `ersetzen` immer | nur wenn Eigenanteil im Feld ≥ 85 % (`ersetzen_min_anteil`), sonst `ersetzen` ohne Filter (der Filter gilt feldweit und würde Bäume fremder Biome löschen) |
| Ausgabe (§5) | Umlaute, „→“, „–“ in `print()` | alle Konsolenzeilen ASCII (`ascii_text()`: ae/oe/ue/ss, `->`, `-`); `plan.json` bleibt UTF-8 |
| Fehler (§5) | `SystemExit` je Feld abgefangen, Exit 0; `netze.csv` optional | fehlende `hoehe.f32`, Regeldatei oder `daten/netze.csv`, ungültiger Feldname → Meldung, **Exit 2**; fehlende optionale Dateien → Hinweis, weiter |
| Overrides-Prüfung | – | alle `/Game/…`-Pfade in den drei Override-Blöcken werden gegen `netze.csv` geprüft (nur Warnung) |

### 7.2 Neue Schicht-1-Definition (§4)

Schicht 1 dieses Planers enthält **nur noch Nordküsten-Sonderformen** (alle mit `"sonderform": true` im Regel-JSON):

| Klasse | Inhalt | Wo |
|---|---|---|
| `krueppelkiefer` | Windflucht-Krüppelkiefern/Latschen-Gürtel (dwarf_pine, 7 Netze), Gruppen 2–7 | über der Waldgrenze 380–640 m, Grate bis 46°; < 180 m vom Meer zusätzlich Windflucht (Z-Stauchung, Lee-Neigung) |
| `windflucht_kiefer` (neu, aus `strauch_kueste` herausgelöst) | windgeschorene Jungkiefern-Trupps (pine_beach_crooked/short, 4 Netze), Gruppen 2–5 | nur Küste, 15–110 m hinter der Wasserlinie, bis 160 m Höhe, Windflucht |
| `strandgras` | Strandhafer-Horste | nur Küste (jetzt `kueste_nur`), 2–90 m hinter der Wasserlinie |
| `blume_kueste` | Klippenwiesen-Blumeninseln (Stranddistel, Wundklee, Meerkohl, Kamille) | nur Küste (jetzt `kueste_nur` – vorher auch im Binnen-Bergwald), 3–400 m |
| `kletter` | Efeu/Ranken an Fels | Hang 35–85° mit Fels-Lage |

Schicht 0 (Nadelstreu, Kiesel, Moos, Bodendecker), Schicht 2 (8 Baumklassen inkl. Totbaum) und Schicht 5 (Tang, Treibholz,
Strandkiesel, Strandplatten = Tang-/Treibholz-Säume) bleiben. **Wacholder-Gruppen** sind nicht möglich: kein Wacholder im Inventar
(Einkaufsliste, Abschnitt 5).

**Verschoben** (nichts geht verloren):

| Bisherige Klasse | Ziel | Grund |
|---|---|---|
| `strauch_wald`, `strauch_kueste` | `mittelschicht_overrides` → `strauch` | generisch |
| `jungbaum_nadel`, `jungbaum_laub` | → `jungbaum` | generisch |
| `farninsel` | → `farn` | generisch |
| `totholz_liegend`, `stumpf`, `zweige` (Schicht 0) | → `totholz_liegend`, `totholz_stumpf`, `totholz_ast` | generisch (Zweige = Astwurf) |
| `wurzel` | → `wurzel` (mittelschicht-Klasse) | generisch |
| `grasbueschel`, `heide_beere`, `pilz` (Schicht 0) | → `grasbueschel`, `beere`, `pilz` | generisch |
| `blume_wald` | → `mittelschicht_overrides.zusatzklassen.blume_wald` | keine generische Klasse, aber nicht biomspezifisch |
| neu | → `zusatzklassen.blaubeer_teppich` (billberry/lingonberry, 6 Netze) | Blaubeer-Teppiche unter lichtem Kiefernschirm |
| `felsufer` (Schicht 5, Blöcke > 0,8 m mit Kollision) | → `felsgruppen_overrides.zusatzklassen.felsufer` | §4: Felsen > 0,8 m nur felsgruppen |

### 7.3 Override-Schema (in `nordkueste_regeln.json`)

```
"mittelschicht_overrides": {
  "gilt_fuer": ["fjord", "kueste", "bergwald"],
  "klassen_alias_mittelschicht": {"totholz_liegend": "totholz", "totholz_stumpf": "stumpf", "totholz_ast": "ast"},
  "palette":  {"strauch": [22 Pfade], "jungbaum": [17], "farn": [15], "totholz_liegend": [11], "totholz_stumpf": [7],
               "totholz_ast": [24], "wurzel": [8], "grasbueschel": [15], "beere": [11], "pilz": [2]},     # gemeinsam (Fallback)
  "faktor":   {"strauch": 0.65, "jungbaum": 0.93, "farn": 2.18, ..., "totbaum": 0.0},                # Mittel der drei Biome
  "zusatzklassen": {"blaubeer_teppich": {...}, "blume_wald": {...}},   # Klassenformat von mittelschicht_regeln.json + biome/biom_faktor/lagen
  "je_biom": {"fjord":    {"palette": {...}, "faktor": {...}, "vorlage_biom": {"pilz": "bergwald"}},
              "kueste":   {"palette": {...}, "faktor": {...}, "vorlage_biom": {"farn": "bergwald", "wurzel": "bergwald", "pilz": "bergwald"}},
              "bergwald": {"palette": {...}, "faktor": {...}}},
  "herkunft": {"strauch": ["strauch_wald", "strauch_kueste"], ...}
}
```

Auflösung je Zelle mit Biom b: `je_biom[b].palette[k]` vor `palette[k]` vor `mittelschicht_regeln.json["biome"][b][k]`; Dichte =
mittelschicht-Dichte × `je_biom[b].faktor[k]` (sonst `faktor[k]`). Die Faktoren sind aus den bisherigen Nordküsten-Dichten abgeleitet
(Mittel offen/beschattet × Biomgewicht ÷ mittelschicht-Dichte, auf 0,25–3 begrenzt), z. B. bergwald strauch 0,29 / farn 2,91 /
totholz_ast 2,06, kueste strauch 0,98 / jungbaum 1,19. `totbaum` = 0, weil Totbäume hier in Schicht 2 geplant werden. `vorlage_biom`:
Klasse fehlt in `mittelschicht_regeln.json` für das Biom → Parameter aus bergwald. Netze aller Nordküsten-Sonderformen und Bäume sind aus
den Paletten entfernt (z. B. dwarf_pine aus `strauch`, beach_driftwood aus `totholz_liegend`), damit kein Netz doppelt gesetzt wird.

`felsgruppen_overrides` und `spuren_overrides` geprüft und auf dasselbe Schema gebracht (Inhalt unverändert):
`felsgruppen_overrides = {palette: {biom, ergaenzung, bevorzugt}, faktor: {biom, klassen, kiesel}, zusatzklassen: {felsufer}, eingraben,
auflage, kuesten_regel}`; `spuren_overrides = {palette: <Netze je Spurenart>, faktor: <Dichtefaktor je Biom und Spurenart>, verbote,
hinweis}`. Alle Pfade stehen in `netze.csv` (0 Warnungen). Teil C/D müssen die Blöcke noch einlesen (`<thema>_regeln.json` neben der
eigenen Regeldatei, §4).

### 7.4 Rauchtest Runde 1 (synthetisch, Cloud: Python 3.13, NumPy, Pillow, kein numba)

Mini-Produktionswurzel mit vollen Rastern (memmap, danach gelöscht): **B5** Meer im Westen, 210-m-Küstenstreifen (`kueste_nordisch`),
Hangwald (`bergwald_fichte`), Grat bis ~650 m, Bach mit 56 m breitem `aue_bachtal`-Band als Fremdbiom, Weg, Ort, 700 Bestand-Kiefern,
250 Witcher-Farne; **C6** `vulkanregion_asche` 99,7 % + 60 × 60 m bergwald; **H4** bergwald/heide 51/49 mit gewellter Grenze; **J1** nur
Kennzahl 0.

| Prüfung | Ergebnis |
|---|---|
| B5 (eigene Zellen) | 14 069 Instanzen, 360 Kollision; Schicht 2: 322, 1: 4 959 (nur Sonderformen), 0: 6 559, 5: 2 229; 153 f32; 8–10 s; `biome_fenster` bergwald 0,574 / aue 0,233 (inkl. Meer = Kennzahl 0) / kueste 0,180 / lava 0,013; `zellen_zustaendig` 883 740 (davon Saum 76 482) |
| C6 lava | **leerer `plan.json`** (instanzen 0, keine f32, `biome_fenster` lava 0,9972 / bergwald 0,0028), eine Zeile im Log, Exit 0; eine alte f32 im Ordner wurde gelöscht |
| H4 50/50 | 24 171 Instanzen (Kollisionsdeckel greift: 4 565 → 2 996), Schicht 2: 2 996, 0: 21 175; `entfernen` nicht gesetzt (Eigenanteil 51 % < 85 %); Saum im PNG als oranger Streifen entlang der weißen Biomgrenze, Instanzen dünnen nach außen aus, heide-Seite leer |
| J1 fremd | leerer `plan.json`, Exit 0 |
| 30-m-Saum (unabhängig per Brute-Force-Abstand je Instanz) | Instanzen auf Fremdzellen B5: 246 (0–10 m 142, 10–20 m 83, 20–30 m 21), H4: 447 (269/145/33); **jenseits 30 m: 0** |
| Pflichtschlüssel | `instanzen`, `dateien` (mit `ebene`), `biome_fenster`, `zellen_zustaendig`, `biome_eigen`, `kollision_anzahl`, `ft_ordner`, `ft_praefix` in allen vier Plänen; `anzahl` = Zeilen der f32 |
| Budget `--faktor 5` | B5 62 122 → **49 999** (Schicht 0 Nadelstreu, dann Feld-Ziel Kiesel/Nadelstreu), H4 Kollision 7 354 → **2 997**; Warnungen im Log |
| Determinismus | zweiter Lauf: alle f32 byteidentisch (B5 154, H4 80 Dateien), `plan.json` bis auf `stand`/`laufzeit_s` identisch |
| ASCII | 0 Nicht-ASCII-Zeichen in allen Konsolenausgaben (4 Läufe) |
| Fehlerfälle | ohne `netze.csv`, ohne `hoehe.f32`, Feld X9, Regeldatei fehlt → Meldung, Exit 2; ohne `eigner.r8` → dominantes Feldbiom (C6 lava → leer, B5 bergwald → 9 832) |
| Format | 10 float32 je Instanz, 0 NaN, Quaternionen normiert (Fehler ≤ 1,2e-7), alle Positionen im Feld; `py_compile` ok |

Die Zahlen sind nicht mit dem Rauchtest aus Abschnitt 4 vergleichbar (andere synthetische Biomkarte: Bach-Aue und Meer sind jetzt
Fremdbiom, und Schicht 1 enthält nur noch Sonderformen).

### 7.5 Echtdaten-Referenz und Erwartung nach der Korrektur

| Feld | Echtlauf 10.10. (vor Korrektur) | Erwartung jetzt | Begründung |
|---|---|---|---|
| A5 (kueste 75 / bergwald 14 / aue 11 % laut `biome_je_feld.md`) | 27 302 | etwa 10 000–18 000 | generische Schicht 1 und Zweige/Pilze entfallen (im Synthetiklauf ~60 % von Schicht 1), Kennzahl-0-Zellen sind jetzt aue statt Feldbiom |
| G4 (elfenwald) | kein Plan (Text) | leerer `plan.json`, Exit 0 | Eigenanteil ≈ 0 |
| E1 (gletscher 100 %) | kein Plan (Text) | leerer `plan.json`, Exit 0 | Eigenanteil 0 |
| C6 (lava 96,8 % + bergwald 3 %) | 1 078 | **nicht zwingend 0**: liegen die 3 % bergwald als eigene Kacheln im Fenster, ist die 2-%-Schwelle überschritten und der Planer bebaut genau diese Zellen + 30-m-Saum, ohne generische Mittelschicht – erwartet wenige hundert Instanzen | Regel aus §1 (< 2 % → leer); soll C6 leer bleiben, `zustaendigkeit.min_anteil_eigen` in `nordkueste_regeln.json` auf 0,04 setzen |

Bitte beim nächsten Echtlauf `biome_fenster`, `zellen_zustaendig` und `statistik.zustaendigkeit` von A5/C6 zurückmelden; daraus lässt
sich die Schwelle für C6 und die Dichte für A5 (Ziel 15 000–30 000) nachstellen.

### 7.6 Offene Punkte nach Runde 1

1. `mittelschicht_plan.py`, `felsgruppen_plan.py`, `spuren_plan.py` lesen die Override-Blöcke noch nicht (Teil C/D). Bis dahin fehlt in
   Nordküsten-Feldern die biomspezifische Feinsteuerung von Strauch/Farn/Totholz, nicht aber die Klassen selbst (mittelschicht setzt sie mit
   eigenen Pauschalwerten). Das Fjord-Felsufer fehlt, bis felsgruppen `zusatzklassen.felsufer` umsetzt.
2. Die Override-Faktoren sind aus Dichtemitteln abgeleitet, ohne Lagen-/Licht-/Klumpungsfaktoren beider Planer – Richtwerte, nach dem
   ersten gemeinsamen Setzen in A5/B5 gegen die Zielbilder nachstellen.
3. Abschnitt 5 korrigiert: Blaubeere/Preiselbeere **sind** im Inventar (`SM_billberry_01–03`, `SM_lingonberry_01–02`) und werden jetzt
   als `blaubeer_teppich` genutzt; es fehlt nur Wacholder.
4. Meer und andere Kennzahl-0-Flächen zählen in `biome_fenster` als aue (Konvention); Küstenklassen stehen auf kueste-Landzellen und
   werden davon nicht berührt.
5. Abschnitt 6 Punkt 9 überholt: der Kollisionsdeckel greift jetzt exakt (H4 synthetisch 4 565 → 2 996).
