# Antwort 18 – Bäche in Witcher-Qualität: was fehlt, welche Wege gibt es außer Fluid Flux 3.0

Stand 13.10.2026. Ferats Frage: „recherchier mal was wir für unser bächer brauchen, damit es witcherqualität erreicht. komm nicht
fluid flux 3.0, der ist zu teuer. was haben wir noch für möglichkeiten“.

Grundlage im Projekt: Antworten 16, 16e, 16f, 16h mit Nachträgen 1–5b, 17, `bildkritik-witcher-messlatte.md`,
`vorlagen/doku/fab_pakete_bewertung_2026-10-10.md`, der Graph-Dump `antworten/fluss_sim/p2_lokal/master_graph_schaum8.json`,
die Bilder `bilder/swr_p2/wasser_oberflaeche_g0_g4.jpg` und `bilder/zielbilder/witcher_01.jpg`.

**Quellenlage:** Aus der Cloud war keine Webseite direkt abrufbar (Fab, Epic, GDC Vault, 80.lv, YouTube, SIGGRAPH-Archiv: DNS-Fehler).
Alle Web-Aussagen stammen aus **Suchmaschinen-Auszügen**. Preise auf Fab konnte ich deshalb nicht live prüfen.

**Kennzeichnung:**
- [Beleg] Aussage steht so im Auszug einer Primärquelle (Hersteller, Epic, CDPR, Valve, SideFX)
- [Auszug] nur Suchauszug einer Sekundärquelle (Presse, Forum, Mod-Seite, YouTube-Zusammenfassung)
- [Projekt] eigene Daten im Repo
- [Bild] aus unseren Bildern abgelesen
- [Ableitung] eigene Schlussfolgerung, nicht belegt
- [unsicher] im Test klären

---

## Kurzfazit

1. **Witcher-Qualität ist bei Bächen Kunst, nicht Simulation:** Witcher 3 legt laut REDkit flache Wasserflächen in die Betten, der Pontar steht still [Beleg/Auszug]. Es wirken klare Spiegelung, dunkle Tiefe, gebrochene Ufer und der Wechsel Ruhe–Schnelle.
2. **Unsere Technik (Water + gebackene SWR) reicht.** Kein Kaufprodukt schließt die Lücken. Fluid Flux kostet ab 349,99 USD [Auszug]; die günstigen Fab-Flusswerkzeuge sind Spline-Mesh-Flüsse (teils UE4) und würden die SWR ersetzen.
3. **Lücken [Bild]:** Die Oberfläche spiegelt nicht klar; unter Lumen sind SLW-Spiegelungen „forced to mirror“, also sind die **Normalen** der Hebel, nicht die Rauheit. Das Wasser liegt als dünner Film bündig im Talboden, ohne Uferstufe und dunkle Becken. Die Kante ist glatt, helle Platten unter Wasser wirken wie Laub.
4. **Weg (0 €):** Messbasis → ELD-Wirbel aus, Normalen nach Tempo → Rural-Australia-A/B → Uferstufe, tiefere Becken, Kante brechen, Nasslinie → Lippen → Partikel nur an Fällen → Ton.
5. **Schon bezahlt und ungenutzt:** vier NatureManufacture-Pakete mit Fluss-/Wassermaterialien und 14 Nassufer-Decals [Projekt]. Kaufen lohnt sich derzeit für nichts.

---

## 1. Was Witcher 3 und RDR2 bei Bächen tun (belegt, soweit möglich)

### 1.1 Witcher 3

| Befund | Herkunft |
|---|---|
| Wasser wird in REDkit als **Local Water Areas** angelegt: Umrisse einer Wasserform, „usually inside river or lake beds“, wo das Gelände unter eine Höhe fällt. Ablauf: Gelände mit dem Shape Brush flach machen, dann Wasserflächen setzen und skalieren. | [Beleg] [CDPR REDkit: HOW-TO Add water areas](https://cdprojektred.atlassian.net/wiki/spaces/W3REDkit/pages/6325854/HOW-TO:+Add+water+areas) |
| Witcher-2-REDkit: Wellenhöhe ist begrenzt, weil sie ein Normal-Map-Effekt ist; die Geometrie bewegt sich nicht. | [Beleg für W2] [Witcher 2 REDkit Wiki](https://redkitwiki.cdprojektred.com/get+the+water+you+want.htm); für W3 nur [Ableitung] |
| Landschaft und Wasser werden tesselliert (Interview mit Lead Engine Developer Balázs Török). | [Auszug] [PCGH-Interview](https://www.pcgameshardware.de/The-Witcher-3-Spiel-38488/Specials/The-Witcher-3-welche-Grafikkarte-welche-CPU-1107469/2/) |
| Grafikoption „Water Quality“ ändert laut Nutzer hauptsächlich die Tessellationsstufe; die Wassersimulation (Boot schaukelt) laut NVIDIA-Leitfaden ab High. | [Auszug, Forum] [Guru3D](https://forums.guru3d.com/goto/post?id=5079202) |
| Der Pontar wirkt im Spiel **statisch**; im Gebirge im Osten gibt es ein eigenes Flusssystem, in dem das Wasser fließt (Analyse des YouTubers Any Austin). | [Auszug] [Boing Boing](https://boingboing.net/2025/10/20/examining-the-rivers-of-the-witcher-3.html), [ixbt.games](https://ixbt.games/en/news/2025/10/19/bloger-proveril-realisticnost-reki-iz-the-witcher-3-cdpr-udivila-detalizaciei-urovnia-rockstar.html) |
| Die Mod „Better FX“ fügt einen Fluss-Shader hinzu, der „foam at the edges of the river“ bildet, und färbt Flüsse in Skellige und Kaer Morhen um. Im Grundspiel gibt es diesen Uferschaum also nicht. | [Auszug] [Nexus Better FX](https://nexusmods.com/witcher3/mods/9173) |
| Next-Gen-Fassung 2022: Raytracing-Spiegelungen auf PC verbessern laut Presse Wasser deutlich, von Buchten über Pfützen bis zu Brunnen. | [Auszug] [NVIDIA](https://www.nvidia.com/en-au/geforce/news/witcher-3-wild-hunt-dlss-rtx-ray-tracing-free-update-out-now), [LevelUp](https://www.levelup.com/en/news/the-witcher-3-nextgen-pc-incredible-graphics-but-disappointing-performance/) |
| Die SIGGRAPH-2015- und GDC-2014-Vorträge von CDPR (Török/Krzyścin, Gollent) behandeln laut Kurztext Rendering und Landschaft. Ob Wasser vorkommt, ließ sich nicht prüfen. | [Auszug] [SIGGRAPH-Archiv](https://history.siggraph.org/learning/building-the-world-of-the-witcher-3-wild-hunt-by-torok-and-krzyscin/), [GDC Vault](https://www.gdcvault.com/play/1020394/Landscape-Creation-and-Rendering-in) |

**Nicht belegt:** Wie CDPR fließende Bergbäche, Stromschnellen und Wasserfälle technisch baut (Flowmap auf Mesh? Karten mit Partikeln?).
Dazu fand ich keine Primärquelle. Eine Wasserfall-Mod tauscht „waterfall rushing water“-Texturen [Auszug, [Nexus 901](https://www.nexusmods.com/witcher3/mods/901)].
Das deutet auf texturierte Netze bzw. Partikel hin, mehr nicht.

**Was man im Zielbild sieht** ([Bild] `bilder/zielbilder/witcher_01.jpg`, W3 Next-Gen):
- Das Wasser ist fast **spiegelglatt**. Bäume, Hang und Himmel stehen als zusammenhängende Spiegelbilder im Wasser.
- Wo es flach ist, sieht man den hellen Kies. Wo es tiefer ist, wird es **dunkel**, und dort dominiert die Spiegelung.
- Die Wasserkante ist überall gebrochen: weiße, kantige Felsen mit Fuß im Wasser, Gras hängt über die Kante, Kiesbänke.
- Die Wasserfläche liegt **sichtbar unter** dem Gras-Ufer, das Ufer hat eine kleine Stufe.
- Kein Schaum, keine Strömungstextur im ruhigen Teil.

### 1.2 RDR2 (Zweitreferenz)

| Befund | Herkunft |
|---|---|
| Flüsse haben „different rates of flow even in small sections based on how deep or shallow they are and how they bend“; viele Wasserfall-Arten, von breit bis zu kleinen Stufen an Geländeknicken. | [Auszug] [GamesRadar über Any Austin](https://www.gamesradar.com/games/open-world/red-dead-redemption-2-has-some-of-the-most-accurate-rivers-in-video-games-according-to-the-video-game-geographer-who-charted-skyrim-and-zeldas-waterways/) |
| Spieler können mit dem Pferd kleine Strudel in Bächen erzeugen (dynamisches Wasser). | [Auszug] [GameRant](https://gamerant.com/video-games-best-water-physics/) |
| PC-Optionen: Water Quality mit Unteroptionen Refraction, Reflection, Physics. **Water Physics** ist mit Abstand am teuersten und bringt sichtbar wenig. | [Auszug] [Shacknews](https://shacknews.com/article/115067/red-dead-redemption-2-pc-graphics-settings-guide), [GamingBolt](https://gamingbolt.com/red-dead-redemption-2-pc-tech-analysis-comparison-with-ps4-pro-and-more/amp) |
| Spiegelungen sind nach PC-Analyse Standard-Screen-Space-Reflections. | [Auszug] GamingBolt (wie oben) |
| David O'Reilly, früherer Rockstar-Umgebungskünstler und an RDR2-Wasser beteiligt: Flowmaps sind wie ein Kompass für die Fließrichtung, werden meist **vorab gebacken**, und ein versetzter Stein kann die ganze Map verderben. | [Auszug] [ixbt.games](https://ixbt.games/en/news/2026/04/04/crimson-desert-udivliaet-prorabotkoi-v-duxe-red-dead-redemption-2-igroki-zametili-stroitelstvo-v-realnom-vremeni-i-starenie-geroia.html), [GamingBolt](https://gamingbolt.com/crimson-deserts-rivers-attention-to-detail-praised-by-red-dead-redemption-2s-water-artist) |
| Derselbe lobt Crimson Desert: Flüsse „level out and alternate between rapids and calm stretches rather than looking like tilted ribbons“. Laut einer russischen Quelle nutzt Pearl Abyss Shallow-Water-Gleichungen. | [Auszug] [VGTimes](https://vgtimes.com/gaming-news/152644-finally-a-game-with-better-rivers-than-rdr2-rockstar-artist-impressed-by-crimson-deserts-world-detail.html), [Shazoo (ru)](https://shazoo.ru/2026/04/03/181947/xudoznik-red-dead-redemption-2-sdelal-podrobnyi-razbor-vody-v-crimson-desert-i-nazval-ee-lucsei-v-istorii-videoigr) |

**Nicht belegt:** ein Rockstar-Vortrag oder eine Digital-Foundry-Analyse speziell zu RDR2-Flüssen. Ich fand keine.

### 1.3 Was daraus folgt [Ableitung]

- **Treppen statt Rampe ist richtig.** Das Lob „ruhige Abschnitte und Schnellen im Wechsel statt schräger Bänder“ beschreibt genau
  Ferats Treppen-Design der Sehens-Bäche. Es bleibt.
- **Simulation ist nicht das Unterscheidungsmerkmal.** Witcher 3 kommt mit flachen Wasserflächen aus, RDR2s teure Wasserphysik bringt
  laut Spielern wenig fürs Bild. Wir haben mit der gebackenen SWR schon Strömung, Kehrwasser hinter Steinen und Tempo nach Gefälle (16e).
- **Was den Unterschied macht:** klare Spiegelung, Tiefe, Ufer, Ruhe. Das sind Material-, Gelände- und Dekor-Aufgaben.

---

## 2. Was uns fehlt (Bildvergleich)

[Bild] `bilder/swr_p2/wasser_oberflaeche_g0_g4.jpg` (C2, Augenhöhe) gegen `witcher_01.jpg`:

| Merkmal | Witcher 3 | Eldarien heute | Hebel |
|---|---|---|---|
| Spiegelbild | scharfe, zusammenhängende Spiegelbilder von Bäumen und Hang | keine erkennbaren Spiegelbilder; das Bett erscheint durch eine verzerrte, marmorierte Haut | Normalen (§3.1) |
| Tiefe | flach hell, tief dunkel | überall gleich flach (Talkaskade im Mittel 0,47 m, 16h N5) und hell | Becken vertiefen (§3.3) |
| Lage des Spiegels | 0,2–0,5 m unter der Grasnarbe (geschätzt) | bündig, das Wasser füllt den ganzen Talboden | Uferstufe (§3.2) |
| Wasserkante | Felsen, Gras, Kies brechen sie | lange, glatte Linie; Gras endet vor dem Wasser | Uferdekor (§3.2) |
| Grund | Kies gemischt, kleinkörnig | große helle flache Steine, die durch die Verzerrung wie Laub aussehen | Bettlagen, Steinwahl (§3.3) |
| Licht | tiefe Sonne, kühler Dunst | hohe Mittagssonne (bildkritik) | Licht für Vergleiche (§3.7) |

Das deckt sich mit 16h N5/5b: Der Boden ist mit V18 gelöst. **Offen sind Oberfläche und Form des Gewässers.**

---

## 3. Bausteine für Witcher-Qualität, nach Wirkung sortiert

### 3.1 Oberflächen-Shading (größte Wirkung)

**Belegte Grundlagen:**
- Lumen: „Lumen Reflections support Single Layer Water materials, with reflections forced to mirror“ [Beleg, Auszug aus der
  [Epic-Lumen-Doku](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine),
  schon in `ufer-kies-coast-dunes.md` zitiert]. Damit ist die **Rauheit unter Lumen kaum ein Hebel**. Das erklärt, warum G1 und G4
  in 5b nicht eindeutig wirkten.
- Flowmap-Technik (Valve, Portal 2, SIGGRAPH 2010): Eine Normal-Map wird entlang eines 2D-Vektorfelds verzogen, zwei Lagen mit halber
  Phase versetzt werden überblendet. Hauptprobleme: **Wiederholung und Pulsieren**. Valve bricht das Pulsieren mit einem Rauschwert
  in der Phase [Beleg, [Vlachos 2010](https://www.advances.realtimerendering.com/s2010/Vlachos-Waterflow(SIGGRAPH%202010%20Advanced%20RealTime%20Rendering%20Course).pdf),
  [Grimes GDC 2011](https://www.hlportal.de/files/GDC2011_BronwenGrimes_NonstandardTextures.pdf)].
- Unser Master enthält bereits Epics `WaterRiverFlowmaps` (an `Enable River`), `WaterTextureSurface`, `SampleFluidSimulation`,
  `WaterCaustics_GerstnerWaves` (an `Caustics`) und **dazu** unsere eigenen Lagen `ELD_Wirbel_*` und `MF_EL_LocalRipples` [Projekt, Graph-Dump].

**Folgerung [Ableitung]:**
- Wir brauchen keine neue Flowmap-Pipeline für die Bewegung: Die Flowmap-Animation über die SWR-Strömung ist schon da.
- Das „Wirbelmuster“ ist sehr wahrscheinlich unsere **zusätzliche** ELD-Wirbel-Lage über den Epic-Normalen (16h N5).
- „Flowmap-Normalen statt Wirbel“ heißt also: ELD-Wirbel aus, Epic-Flowmap-Normalen als einzige Bewegungsquelle,
  und deren Stärke **nach Tempo** steuern: Becken fast glatt (klares Spiegelbild), Rinnen und Lippen kräftiger.
- Ob unser ELD-Zweig die dekodierte SWR-Geschwindigkeit lesen kann, ist **nicht belegt** (16h N3 §4: sie liegt in `WaterRiverFlowmaps`).
  Rückfall ohne Funktionskopie: Steilheit der Wasserfläche aus den Ableitungen der Weltposition (16h N3), weil Becken flach und Rinnen steil sind.

**Werte zum Start [Ableitung, im Test prüfen]:**

| Größe | Becken (v < 0,3 m/s bzw. flach) | Rinne/Lippe (v > 1,2 m/s bzw. steil) |
|---|---|---|
| Normalstärke gesamt (Faktor auf die Epic-Lagen) | 0,15–0,25 | 0,8–1,0 |
| `ELD_Wirbel_Normal`, `ELD_Wirbel_Staerke` | 0 | 0 |
| `WPO Flowmap` | 2 | 3 |
| Rauheit | 0,04–0,10, egal (Lumen) | gleich |

Erfolg: Bei t430/t500 Auge sind Hang und Bäume im Becken als Spiegelbild erkennbar (Kriterium K1, §6).

### 3.2 Uferübergang und Nässe

- **Uferstufe:** Der Spiegel liegt sichtbar unter der Grasnarbe. Für einen 2–4-m-Bach etwa 0,2–0,5 m an Geraden und Gleithängen
  flacher, am Prallhang höher [Ableitung aus witcher_01 und den Böschungsregeln 16h C]. Das betrifft Gelände bzw. Bettform, nicht die SWR-Werte.
- **Wasserkante brechen**, je 10 m Ufer mindestens drei Größenstufen:
  - Blöcke mit Fuß im Wasser (≥ 30 % unter dem Spiegel);
  - Kopfsteine und Kies;
  - Gras bzw. Moos, das 10–30 cm über die Kante hängt.

  Die Ausschlussregeln aus 16h N5 (`C_ufer.ausschluss_16h5`) gelten weiter [Projekt].
- **Nasslinie an Steinen und Holz:** Unter Spiegel + 5–15 cm Albedo × 0,6 und Rauheit 0,2–0,3 (16f §5.2). Physik: Nässe dunkelt
  poröse, raue Oberflächen ab und glättet sie [Auszug, [Lekner & Dorf](https://www.wgtn.ac.nz/scps/staff/pdf/darkerwhenwet.pdf), [Polycount](https://polycount.com/discussion/154210)].
  Auf Wasserflächen erscheinen Decals laut 16e nicht, auf Steinen und am Ufer aber schon.
- **Vorhandene Nassufer-Decals:** Coast & Dunes enthält 14 Decals (Nassufer, Lehm, Fels, Kiesel, Sand) [Projekt, `fab_pakete_bewertung`].
  Bisher ungenutzt.
- Ein „River in Utah“-Breakdown löst die Nässe des Flussbetts mit einem Decal mit passender Specular und Rauheit [Auszug,
  [80.lv](https://80.lv/articles/creating-a-river-simulation-in-houdini-unreal-engine-5)].

### 3.3 Bachbett-Komposition und Tiefe

- **Becken vertiefen**, damit sie dunkel werden: 0,8–1,2 m in Becken der Sehens-Bäche, Rinnen 0,2–0,4 m [Ableitung aus witcher_01
  und der Absorption 16h: Sichtweite (300, 1600, 1200) cm färbt erst ab etwa 1 m deutlich].
- **Helle flache Steine** unter Wasser seltener und kleiner. In G0–G4 wirken sie wie Laub [Bild]. Mehr kleinkörniger Kies und dunkle
  Steine; große helle Platten nur am Ufer.
- Totholz, Schlamm und Felsen in jedem Bett bleiben (Ferat). Stämme quer zur Strömung erzeugen Rückstau in der SWR (16f).

### 3.4 Kleine Schwellen, Kaskaden und Kehrwasser

- Treppen-Design bleibt. **Je Stufe eine Lippe aus Felsen oder einem Stamm**, über die das Wasser glatt abläuft. Die glatte
  „Zunge“ entsteht, wenn die Normalstärke an der Lippe nicht hochgeht [Ableitung]. Darunter wird es unruhig.
- **Kehrwasser:** Die SWR erzeugt es hinter Hindernissen mit Wasser-Kollision (≥ 0,4 m, 16f-Regeln) [Projekt]. Keine Extra-Arbeit nötig.
- **Weiß nur an Fällen ≥ 1 m** (Ferat): über die Schaum-Kapseln (16e Option B) [Projekt].

### 3.5 Partikel und Gischt (nur an Fällen)

- Wasserfälle warten (Ferat). Wenn sie kommen:
  - Aufprall-Niagara wie geplant (16, 16e);
  - Nebelkarten: Epics kostenloses **Niagara Examples Pack** (Januar 2026, für 5.7) enthält „mist cards“ [Beleg, [Epic News](https://www.unrealengine.com/en-US/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7)].
    Auf 5.8 testen;
  - Bläschen-Schleier unter Wasser im Becken (16f).
- Weißwasser besteht aus drei Teilen: Spritzer, Oberflächenschaum, Blasen [Auszug, Asher Zhu, Epic,
  [80.lv](https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations)].

### 3.6 Ton

- Plan aus 16h Nachtrag-Materialtest §6 gilt: Stufe −12 dB, Fall −6 bis −8 dB, ruhige Strecke −16 bis −18 dB, höchstens 3–4 Quellen hörbar [Projekt].
- Für lange ruhige Strecken: **eine** Tonquelle, die auf der Spline zum Punkt neben dem Hörer wandert, statt vieler Punktquellen.
  - Das ist das übliche Verfahren [Auszug, [Epic-Forum](https://forums.unrealengine.com/t/how-to-have-a-sound-cue-follow-a-playercontroller-along-a-spline/786593)].
  - Es gibt ein quelloffenes Plugin dafür [Auszug, [JDSherbert Audio Spline](https://jdsherbert.itch.io/audio-spline-plugin)]; Lizenz vor Nutzung prüfen.
  - In Blueprint sind es wenige Knoten (Find Location Closest to World Location → Set World Location) [Ableitung].
- Klangmaterial:
  - im Projekt 10 Cues `CUE_Water_Stream_I…X_Cue` [Projekt];
  - kostenlos die Sonniss-GDC-Bundles: lizenzfrei, ohne Namensnennung, seit 2024 nicht für KI-Training [Auszug, [rekkerd.org GDC 2026](https://rekkerd.org/sonniss-releases-gdc-2026-game-audio-bundle/), [GameFromScratch 2024](https://gamefromscratch.com/sonniss-27-5gb-sound-effect-giveaway-at-gdc-2024/)].
    Ob Bachgeräusche dabei sind, ist nicht belegt.

### 3.7 Licht und Kaustiken

- **Licht für Vergleiche:** Sonne 10–25° seitlich oder im Gegenlicht (bildkritik). Für die Messung eingefroren (5b §5).
- **Kaustik:** niedrige Priorität.
  - Der `Caustics`-Schalter im Master hängt an `WaterCaustics_GerstnerWaves` [Projekt]. Bei Flüssen ohne Gerstner-Wellen wirkt er
    vermutlich kaum [Ableitung, unsicher].
  - Wenn gewünscht: gepannte Kaustik-Textur im Landschaftsmaterial unter `Bachgewicht`, voll bei 0,2–0,8 m Tiefe (16f §5.2).
  - Die Directional Light liest den Light-Function-Atlas nicht [Auszug, `ufer-kies-coast-dunes.md`].

### 3.8 Ufer-Vegetation

- Gras und Moos bis an bzw. über die Wasserlinie; Farne und Gebüsch im 1–4-m-Band; an ruhigen Becken Schilf.
- Kandidaten im Projekt [Projekt, `fab_pakete_bewertung`]: `SM_MossClump_04`, `SM_EagleFern_S_04` (Hivemind Docks),
  Totholz `SM_dead_log_03`, `SM_beech_old_roots_01` (Forest Set), Treibholz `FT_SM_beach_driftwood_01…09` (Coast & Dunes).
  Vor dem Einsatz ein Bild-Check.

### 3.9 LOD und Leistung

- SWR gebacken bleibt bei etwa 0,2 ms (Messung 16) [Projekt].
- Normalen nach Tempo kosten nur wenige Knoten; der ELD-Wirbel fällt weg. Insgesamt eher billiger [Ableitung].
- Ufer-Dekor kostet Instanzen. Für den VSM-Pool gelten die Regeln aus `boden-kleinzeug-gras.md` (2K-Stufe, wenig WPO).
- Niagara nur an Fällen, Cull 45 m (16f).

---

## 4. Optionen außer Fluid Flux 3.0

Fab-Preise sind **Suchauszüge, nicht live geprüft** (Fab aus der Cloud gesperrt). Prüfdatum der Auszüge: 13.10.2026.
Vor jeder Entscheidung den Preis im Launcher bzw. auf Fab nachsehen.

| # | Option | Kosten | UE 5.8 / SWR + WCBS | Aufwand | Leistung | Lizenz | Bewertung |
|---|---|---|---|---|---|---|---|
| 1 | **Epic Water + SWR + eigener Master** (Stand) | 0 | ist unser Weg | – | ~0,2 ms | Engine | **Basis** |
| 2 | **Material-Umbau:** ELD-Wirbel aus, Normalen nach Tempo (§3.1) | 0 | voll | 2–6 h | eher billiger | eigen | **zuerst** |
| 3 | **Rural Australia** Wassermaterial ([Fab](https://www.fab.com/listings/1c1467ce-a2f5-4be1-8988-9069f90a8571); Epic: „Permanently Free Collection“ [Beleg, [UE-Blog](https://www.unrealengine.com/en-US/blog/rural-australia-environment-collection-now-available-for-free)]) | 0 | Paket enthält genau **1** Wassermaterial und eine Flussschlucht-Karte; laut Auszug zuletzt „compatible with UE 5.3“, eigene `DefaultEngine.ini` nötig [Auszug]. Ob SLW und SWR-fähig: **unbekannt**, Prüfliste 5b §6 | 2–4 h A/B | unbekannt, messen | Epic/Fab, nur prüfen | **A/B-Test**; die `DefaultEngine.ini` **nicht** ins Eldarien-Projekt übernehmen, nur im Testprojekt öffnen |
| 4 | **Schon gekaufte Pakete** im Projekt: NatureManufacture Mountain (Fluss-Material mit Auto-Wasserfällen, Fluss-Splines), Coast & Dunes (Meer-/Fluss-Material, 14 Nassufer-Decals), Lava (Flowmaps über Epic Water), Forest (Sumpf-Wasser) [Projekt] | 0 (bezahlt) | 4.21–5.8 bzw. 5.5–5.8 laut Fab [Projekt]; ihre Fluss-Materialien sind für Spline-Meshes oder Epic Water gebaut, SWR-Tauglichkeit unbekannt | 1–3 h je Paket | – | Fab-Standard | **Decals und Normal-Texturen sofort nutzen**; Materialien nur als Vergleich |
| 5 | **Houdini + SideFX Labs Flowmap** (Flowmap, Flowmap Obstacle, Guide Flowmap, Flowmap to Color, Flowmap Visualize) [Beleg, [SideFX Labs](https://www.sidefx.com/docs/houdini/labs/index.html), [Flowmap Obstacle](https://www.sidefx.com/ja/docs/houdini/nodes/sop/labs--flowmap_obstacle-3.0.html)] | 0 (Labs frei, quelloffen) | für **Netze** (Kaskaden-Vorhänge, ferne Bäche ohne SWR); für die SWR nicht nötig, die liefert die Strömung | 1–2 Tage für die Pipeline | eine Textur je Netz | Labs frei; **Houdini-Lizenzart** (Apprentice/Indie/Commercial) für kommerzielle Nutzung prüfen [unsicher] | erst, wenn Fälle kommen |
| 6 | **Niagara Fluids** (Plugin an) | 0 | 5.8 ja; 3D-FLIP nur für einen Schau-Wasserfall mit Cache (16g) | hoch | teuer | Engine | nur Schau-Fall |
| 7 | **Niagara Examples Pack** (über 50 Systeme, u. a. Nebelkarten; Januar 2026) [Beleg] | 0 | gelistet für 5.7, auf 5.8 testen | 1 h | je System | Fab | für Fälle |
| 8 | **Content Examples** (Karte `Niagara_Fluids` mit Fluss) [Auszug, [80.lv](https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations)]; Engine-Testlevel `WaterFluidSimtestShallow` [Auszug, [Forum 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772)] | 0 | Referenz | 1 h | – | Epic | nur Referenz |
| 9 | **Flowmap selbst malen** in UE (Scriptable Tools; Devlog von Ghislain Girardot, Projektdateien auf Patreon) [Auszug, [80.lv](https://80.lv/articles/tutorial-paint-flow-maps-with-ue5-s-scriptable-tools/)] | 0 bzw. Patreon | für Netze; mit SWR unnötig | mittel | – | prüfen | nicht nötig |
| 10 | **Megascans** (eigene 956 Assets im Projekt [Projekt]; seit 2025 überwiegend bezahlt ab 0,99 USD je Asset, Pakete ab 24,99 USD, frei: Starter-Paket mit 1 500+ Assets und monatliche Gratis-Drops, Megaplants frei) [Beleg, [CG Channel](https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/), [Fab FAQ](https://support.fab.com/s/article/Fab-Transition-FAQs?language=en_US)] | 0 für Starter-Paket und Monats-Drops | Nanite, 5.8 | gering | 2K-Stufe wählen | Fab-Standard bzw. alte UE-only-Lizenz je Claim-Weg | **Bachsteine, nasse Oberflächen zuerst in der eigenen Bibliothek suchen** |
| 11 | **Fab, günstig, Spline-Mesh-Flüsse** [Auszug, Preise ungeprüft]: [SHADERSOURCE Branching River Tool](https://www.fab.com/listings/e0e83ded-b935-42c2-a247-7afb6f2e70f8) 34,99 USD (Vertex Painting ab 5.2 aus); [River Generation Plugin](https://www.fab.com/listings/9412f4c6-cccf-4e12-98af-c1b17a1c5cc0) 34,99 USD (Fixes für 4.26/4.27); [Ultimate River Tool](https://www.fab.com/listings/bb780ac6-c2a4-4b0c-a3ae-820485d234e9) 149,99 USD (UE4); [River-ology](https://www.fab.com/listings/36933ae4-eb48-4395-951b-6357e0ff2c17) (Preis nicht gefunden) | 35–150 USD | **ersetzen** die SWR durch eigene Netze; 5.8 meist unbelegt | hoch (Neubau) | unbekannt | Fab-Standard | **nein** |
| 12 | **Fab, groß**: [UIWS](https://www.fab.com/listings/798b269a-b760-42c5-9c2c-8e11d723d5be) (früher etwa 350 USD, 2020 einmal gratis) [Auszug, [GameFromScratch](https://gamefromscratch.com/uiws-unified-interactive-water-system/)]; Fluid Flux ab 349,99 USD [Auszug] | ~350 USD | eigenes System statt Epic Water | sehr hoch | – | Fab | **nein** (Ferat) |

**Was die Bezahl-Optionen gegenüber dem kostenlosen Weg wirklich mehr bringen [Ableitung]:**
- **Spline-Mesh-Werkzeuge (Nr. 11):** automatische Flowmap am Netz, Verzweigungen. Beides haben wir mit Water Body River + SWR schon.
  Mehrwert für uns: keiner. Risiko: Umbau aller Gewässer und unklare 5.8-Tauglichkeit.
- **Fluid Flux / UIWS (Nr. 12):** eigene Simulation mit Interaktion, Unterwasser-Effekten und Kaustik aus einer Hand. Fluid Flux wirbt
  mit „besserer Qualität auf Hängen“ (16g). Unsere SWR läuft aber an den Hängen der Talkaskade. Der sichtbare Abstand zu Witcher
  liegt in Oberfläche und Ufer, und dort hilft keines der Pakete.
- **Einzige Lage, in der Kaufen sinnvoll würde:** Steile Wasserfälle bzw. Kaskaden sehen mit Netz und Niagara nicht gut genug aus,
  **und** Houdini-Flowmaps (Nr. 5) reichen nicht. Das ist erst nach den Fall-Tests zu entscheiden.

---

## 5. Empfehlung: Weg und Reihenfolge

Grundsatz: Alles baut auf SWR/WCBS, `M_Eldarien_Wasser_Schaum8` und V18 auf. Kein Geld. Kein Bachschaum außer an Fällen. Treppen bleiben.

| Schritt | Was | Woran sieht man den Erfolg |
|---|---|---|
| **0 Messbasis** | Himmel, Sonne und Belichtung einfrieren (5b §5). Vier Kameras von 5b plus **zwei neue**: ein Becken und eine Stufe der Talkaskade, Augenhöhe 1,7 m, FoV 50–60°, Sonne 15–20° seitlich | gleiche Werte für Y(Himmel) ±5 % zwischen Aufnahmen |
| **1 Material** | W1: `ELD_Wirbel_Normal` 0, `ELD_Wirbel_Staerke` 0, `ELD_Schaum_Normal` 0. Dann W2 (ruhigere Epic-Lagen, 16h N5). Dann **Normalen nach Tempo bzw. Steilheit** als kleiner ELD-Zweig (§3.1). Rauheit bleibt beim Zwischenstand, sie ist unter Lumen kein Hebel | K1, K2, K5 (§6) |
| **2 Rural Australia A/B** | im Testprojekt öffnen, Prüfliste 5b §6. Nur übernehmen, was SLW-fähig ist (Normal-Texturen, Werte) | gleiche Kameras; K1/K2 besser als Schritt 1? |
| **3 Ufer und Becken** | Uferstufe 0,2–0,5 m; Becken 0,8–1,2 m; helle Platten unter Wasser ersetzen; Kante brechen (Blöcke, Kies, Gras-Überhang); Nasslinie an Steinen und Holz; Coast-&-Dunes-Decals am Ufer | K3, K4, K7 |
| **4 Lippen** | je Stufe Lippenfels oder Stamm; glatte Zunge (Normalen an der Lippe nicht erhöhen); Kehrwasser über die vorhandene Wasser-Kollision | K5, K6 |
| **5 Fälle** (wenn Ferat sie freigibt) | Schaum-Kapseln, Aufprall-Niagara, Nebelkarten aus dem Niagara Examples Pack, Bläschen-Schleier; Vorhang-Netze mit Houdini-Labs-Flowmap | K6, Leistung K9 |
| **6 Ton** | Plan 16h §6; eine Spline-Tonquelle je ruhiger Strecke | K8 |

---

## 6. Woran wir „Witcher-Qualität“ messen

**Vergleichsbilder:**
- `bilder/zielbilder/witcher_01.jpg` (ruhiges Gewässer mit Ufer).
- Dazu sollte Ferat **eigene Aufnahmen** aus Witcher 3 Next-Gen machen, auf Augenhöhe an einem Bergbach (z. B. bei Kaer Morhen oder
  auf Skellige, wo es laut Mod-Seite fließende Flüsse gibt), mit Sonne seitlich. Falls RDR2 vorhanden ist, dasselbe an einem Bach mit Stufen.
- Unsere Aufnahme immer mit derselben Brennweite, Augenhöhe und Tageszeit.

**Kriterien** (je Kamera ja/nein bzw. Zahl, Richtwerte sind [Ableitung]):

| # | Kriterium | Prüfung |
|---|---|---|
| K1 | **Spiegelbild:** Hang und Bäume sind im Becken bei 8–15 m als zusammenhängende Form erkennbar | Blick; dazu Kantenschärfe: Laplace-Varianz im Bereich „Wasser fern“ höher als bei G0 |
| K2 | **Durchsicht nah:** Grund bei 2–4 m klar erkennbar, nicht stumpf | K(Wasser nah) ≥ 90 % von G0 (5b §4) |
| K3 | **Tiefe lesbar:** Becken dunkler als Rinne | Y(Becken) / Y(Ufer-Gras) ≤ 0,6; Y(Rinne) / Y(Ufer) ≥ 0,8 |
| K4 | **Wasser im Bett:** Uferstufe sichtbar | auf ≥ 70 % der Bildbreite eine Kante über dem Spiegel |
| K5 | **Bewegung:** Becken ruhig, Rinnen gerichtet, **kein Marmor- oder Wirbelmuster** | 5-s-Video je Kamera; Ferats Urteil |
| K6 | **Weiß nur an Fällen** | keine weißen Flächen > 0,3 m außerhalb der Kapseln |
| K7 | **Kante gebrochen:** je 10 m Ufer mindestens drei Größenstufen und Gras über der Kante | Zählung im Bild |
| K8 | **Ton:** höchstens 3–4 Bachquellen hörbar, Stufen hörbar vor dem Sehen | im Spiel abhören |
| K9 | **Leistung:** Wasser + Ufer-Dekor + Partikel zusammen höchstens +0,5 ms gegen heute | `stat gpu` / ProfileGPU an t500 |

---

## 7. Aufträge für den lokalen Claude

1. **Messbasis:** Sonne fest auf 15–20° und seitlich, Wolken einfrieren, Belichtung manuell (5b §5). Zwei neue Kameras setzen,
   `C2_tk_becken_auge` und `C2_tk_stufe_auge` (Talkaskade, 1,7 m, FoV 55°). Alle sechs Kameras als PNG/EXR aufnehmen → `G0b`.
   *Prüfung:* Y(Himmel) zweier Leeraufnahmen weicht ≤ 5 % ab.
2. **W1:** In `MI_EL_SWR_Klar` `ELD_Wirbel_Normal` 0, `ELD_Wirbel_Staerke` 0, `ELD_Schaum_Normal` 0 → Aufnahme `W1`.
   *Prüfung:* K1, K2, K5 gegen `G0b`; dazu ein 5-s-Video an t500 Auge.
3. **W2:** auf W1 die Werte aus 16h N5 §2.2 (`Default Near/Distant Normal Strength`, `…StrengthB`, `River Normal Flatness`,
   `WPO Flowmap` 3) → `W2`. *Prüfung:* wie 2.
4. **Graph-Dump** der Ketten von `WaterRiverFlowmaps` bis zum Ausgang. Frage: Gibt die Funktion die dekodierte Geschwindigkeit
   oder eine Normalstärke aus, die ein ELD-Zweig nutzen kann? *Ergebnis:* JSON wie `master_graph_schaum8.json`, Abschnitt `ketten`.
5. **Normalen nach Tempo** (nur nach 4): kleiner ELD-Zweig. Lerp der Normalstärke zwischen `ELD_Becken_Normal` (0,2) und
   `ELD_Rinne_Normal` (1,0) über saturate(Tempo / 150 cm/s). Rückfall ohne Tempo: Steilheit aus den Ableitungen der Weltposition.
   *Prüfung:* Shader-Statistik (Instruktionen ≤ G0) und K1 im Becken, K5 in der Rinne.
6. **Rural Australia** in einem **eigenen** Testprojekt öffnen (nicht das Eldarien-`DefaultEngine.ini` überschreiben). Material nach
   5b §6 dokumentieren: Shading Model, Funktionen, Texturen, Parameter. *Ergebnis:* kurze Liste plus Screenshot des Graphen.
   Erst danach entscheiden, was nach 5.8 migriert wird.
7. **Vorhandene Fluss-Materialien inventarisieren:** In Mountain, Coast & Dunes, Lava und Forest die Wasser- bzw. Flussmaterialien und
   die Nassufer-Decals mit Pfad, Shading Model und Texturen auflisten. *Ergebnis:* Tabelle; keine Änderungen am Projekt.
8. **Becken und Uferstufe planen** (Talkaskade p2): je Becken Ziel-Tiefe 0,8–1,2 m, Uferstufe 0,2–0,5 m über dem Spiegel als Vorschlag
   in den Querschnitten (`querschnitte_p2.json`). *Prüfung:* Prüfer 0 FEHLER, Treppen-Lippen unverändert; danach SWR neu backen und
   die Tiefe je Becken messen.
9. **Helle Platten unter Wasser:** Liste der flachen, hellen Steine unter dem Spiegel aus der Instanz-Ebene; Vorschlag zum Ersatz durch
   dunklere Kopfsteine bzw. Kies. *Prüfung:* Anzahl vorher/nachher, Bild t500 Auge.
10. **Wasserkante brechen:** In einem 50-m-Abschnitt Blöcke mit Fuß im Wasser, Kopfsteine und Gras-Überhang setzen; zwei
    Coast-&-Dunes-Nassufer-Decals testen. *Prüfung:* K7 und K9 im Abschnitt.
11. **Nasslinie:** Im Fels- und Holzmaterial (Kopie) eine Feuchtelinie = Spiegel + 10 cm, darunter Albedo × 0,6 und Rauheit 0,25.
    *Prüfung:* Bild Stufe, VSM- und Instruktionskosten.
12. **Ton:** Eine Spline-Tonquelle an einer ruhigen Strecke (Closest Point auf der Water-Body-Spline), dazu die Stufen-Quellen nach 16h §6.
    *Prüfung:* K8.
13. **Vergleichsbilder:** Ferat um 3–5 eigene Witcher-3-Aufnahmen an Bergbächen bitten (Augenhöhe, Sonne seitlich) und unter
    `bilder/zielbilder/` ablegen.
14. **Bericht:** je Schritt eine Zeile in der Antwortdatei: Kamera, K1–K9, ms. Erst danach über Fälle (Schritt 5) und Kaufoptionen reden.

---

## 8. Was unsicher bleibt

- Wie CDPR und Rockstar Stromschnellen und Wasserfälle technisch bauen: keine Primärquelle gefunden (GDC Vault und Digital Foundry nicht lesbar).
- Der Inhalt des Rural-Australia-Wassermaterials (SLW oder nicht, Flowmap oder nicht) und seine 5.8-Tauglichkeit.
- Ob unser ELD-Zweig an die SWR-Geschwindigkeit kommt (Auftrag 4).
- Alle Fab-Preise und Engine-Versionen von Fremdpaketen (nur Suchauszüge).
- Ob die Sonniss-Bundles Bachgeräusche enthalten.
- Die Richtwerte in §3 und §6 sind Ableitungen und im Bild zu bestätigen.

---

## Quellen

**CDPR / Witcher 3**
- [CDPR REDkit: HOW-TO Add water areas](https://cdprojektred.atlassian.net/wiki/spaces/W3REDkit/pages/6325854/HOW-TO:+Add+water+areas)
- [Witcher 2 REDkit: Get the water you want](https://redkitwiki.cdprojektred.com/get+the+water+you+want.htm)
- [PCGH-Interview (Tessellation Landschaft und Wasser)](https://www.pcgameshardware.de/The-Witcher-3-Spiel-38488/Specials/The-Witcher-3-welche-Grafikkarte-welche-CPU-1107469/2/)
- [Guru3D-Forum: Water Quality](https://forums.guru3d.com/goto/post?id=5079202)
- [SIGGRAPH 2015: Building the World of The Witcher 3](https://history.siggraph.org/learning/building-the-world-of-the-witcher-3-wild-hunt-by-torok-and-krzyscin/), [ACM](https://dl.acm.org/doi/10.1145/2775280.2775286)
- [GDC 2014: Landscape Creation and Rendering in REDengine 3](https://www.gdcvault.com/play/1020394/Landscape-Creation-and-Rendering-in)
- [Boing Boing: Examining the rivers of The Witcher 3](https://boingboing.net/2025/10/20/examining-the-rivers-of-the-witcher-3.html), [ixbt.games](https://ixbt.games/en/news/2025/10/19/bloger-proveril-realisticnost-reki-iz-the-witcher-3-cdpr-udivila-detalizaciei-urovnia-rockstar.html), [YouTube: Are The Witcher 3's Rivers Realistic?](https://www.youtube.com/watch?v=A1pIpfRb8fk)
- [Nexus: Better FX](https://nexusmods.com/witcher3/mods/9173), [Nexus: Wasserfall-Retexture](https://www.nexusmods.com/witcher3/mods/901)
- [NVIDIA: Witcher 3 Next-Gen Update](https://www.nvidia.com/en-au/geforce/news/witcher-3-wild-hunt-dlss-rtx-ray-tracing-free-update-out-now), [LevelUp](https://www.levelup.com/en/news/the-witcher-3-nextgen-pc-incredible-graphics-but-disappointing-performance/)
- [CDPR: Witcher 4 UE5 Tech Demo](https://www.cdprojektred.com/en/blog/149/working-with-epic-to-debut-the-witcher-4-unreal-engine-5-tech-demo-at-unreal-fest)

**RDR2 und Vergleich**
- [GamesRadar: RDR2 rivers (Any Austin)](https://www.gamesradar.com/games/open-world/red-dead-redemption-2-has-some-of-the-most-accurate-rivers-in-video-games-according-to-the-video-game-geographer-who-charted-skyrim-and-zeldas-waterways/)
- [GameRant: Water physics](https://gamerant.com/video-games-best-water-physics/)
- [Shacknews: RDR2 PC settings](https://shacknews.com/article/115067/red-dead-redemption-2-pc-graphics-settings-guide), [GamingBolt: PC tech analysis](https://gamingbolt.com/red-dead-redemption-2-pc-tech-analysis-comparison-with-ps4-pro-and-more/amp)
- [GamingBolt: O'Reilly über Crimson Desert](https://gamingbolt.com/crimson-deserts-rivers-attention-to-detail-praised-by-red-dead-redemption-2s-water-artist), [VGTimes](https://vgtimes.com/gaming-news/152644-finally-a-game-with-better-rivers-than-rdr2-rockstar-artist-impressed-by-crimson-deserts-world-detail.html), [ixbt.games](https://ixbt.games/en/news/2026/04/04/crimson-desert-udivliaet-prorabotkoi-v-duxe-red-dead-redemption-2-igroki-zametili-stroitelstvo-v-realnom-vremeni-i-starenie-geroia.html), [Shazoo](https://shazoo.ru/2026/04/03/181947/xudoznik-red-dead-redemption-2-sdelal-podrobnyi-razbor-vody-v-crimson-desert-i-nazval-ee-lucsei-v-istorii-videoigr), [Notebookcheck](https://www.notebookcheck.net/Former-Rockstar-Games-artist-Crimson-Desert-s-water-physics-better-than-Red-Dead-Redemption-2-s.1257889.0.html)

**Technik**
- [Vlachos 2010: Water Flow in Portal 2](https://www.advances.realtimerendering.com/s2010/Vlachos-Waterflow(SIGGRAPH%202010%20Advanced%20RealTime%20Rendering%20Course).pdf), [Grimes GDC 2011](https://www.hlportal.de/files/GDC2011_BronwenGrimes_NonstandardTextures.pdf)
- [Epic: Lumen GI und Reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine)
- [GDC 2018: Water Rendering in Far Cry 5](https://gdcvault.com/play/1025033/Advanced-Graphics-Techniques-Tutorial-Water), [80.lv dazu](https://80.lv/articles/the-gdc-talk-water-rendering-in-far-cry-5), [SideFX: Far Cry 5](https://www.sidefx.com/community/far-cry-5/)
- [80.lv: River Simulation in Houdini & UE5](https://80.lv/articles/creating-a-river-simulation-in-houdini-unreal-engine-5), [80.lv: Niagara Fluids (Asher Zhu)](https://80.lv/articles/working-with-niagara-fluids-to-create-water-simulations)
- [80.lv: Flow Maps mit Scriptable Tools](https://80.lv/articles/tutorial-paint-flow-maps-with-ue5-s-scriptable-tools/), [80.lv: Physics-Based Flowmap Painter](https://80.lv/articles/physics-based-flowmap-painter-for-unreal)
- [SideFX Labs](https://www.sidefx.com/docs/houdini/labs/index.html), [Labs Flowmap Obstacle](https://www.sidefx.com/ja/docs/houdini/nodes/sop/labs--flowmap_obstacle-3.0.html), [Labs Guide Flowmap](https://www.sidefx.com/ja/docs/houdini/nodes/sop/labs--flowmap_guide.html), [Labs Flowmap to Color](https://www.sidefx.com/ja/docs/houdini/nodes/sop/labs--flowmap_to_color.html)
- [cgworld: Shallow Water River 5.6](https://cgworld.jp/flashnews/01-202602-UE-Water.html), [Epic Forum: Baked River Simulations – Parameter Reference](https://forums.unrealengine.com/t/2512112)
- Nässe: [Lekner & Dorf: Why some things are darker when wet](https://www.wgtn.ac.nz/scps/staff/pdf/darkerwhenwet.pdf), [Polycount](https://polycount.com/discussion/154210)
- Ton: [Epic Forum: Sound entlang Spline](https://forums.unrealengine.com/t/how-to-have-a-sound-cue-follow-a-playercontroller-along-a-spline/786593), [JDSherbert Audio Spline](https://jdsherbert.itch.io/audio-spline-plugin), [CRIWARE River Implementation](https://blog.criware.com/?p=4344)

**Assets, Preise, Lizenzen** (Suchauszüge, 13.10.2026)
- [Rural Australia auf Fab](https://www.fab.com/listings/1c1467ce-a2f5-4be1-8988-9069f90a8571), [UE-Blog: Rural Australia free](https://www.unrealengine.com/en-US/blog/rural-australia-environment-collection-now-available-for-free), [GameFromScratch](https://gamefromscratch.com/unreal-add-rural-australia-environment-to-permanently-free-collection/)
- [Epic: Niagara Examples Pack](https://www.unrealengine.com/en-US/news/discover-over-50-free-niagara-systems-ready-to-use-in-unreal-engine-5-7)
- [CG Channel: Megascans](https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/), [Fab Transition FAQ](https://support.fab.com/s/article/Fab-Transition-FAQs?language=en_US), [Epic Forum: Legacy Megascans](https://forums.unrealengine.com/t/access-legacy-megascans-on-bridge-and-quixel-com/2142664)
- Fab-Flusswerkzeuge: [SHADERSOURCE Branching River Tool](https://www.fab.com/listings/e0e83ded-b935-42c2-a247-7afb6f2e70f8), [River Generation Plugin](https://www.fab.com/listings/9412f4c6-cccf-4e12-98af-c1b17a1c5cc0), [Ultimate River Tool](https://www.fab.com/listings/bb780ac6-c2a4-4b0c-a3ae-820485d234e9), [River-ology](https://www.fab.com/listings/36933ae4-eb48-4395-951b-6357e0ff2c17), [UIWS](https://www.fab.com/listings/798b269a-b760-42c5-9c2c-8e11d723d5be) ([GameFromScratch](https://gamefromscratch.com/uiws-unified-interactive-water-system/))
- Fluid Flux: [80.lv 3.0](https://80.lv/articles/fluid-flux-3-0-arrives-with-a-glass-system-underwater-lighting-decals-rain-more/), [digitalproduction](https://digitalproduction.com/2024/11/25/fluid-flux-3-0-new-tools-forfluid-dynamics-in-unreal-engine/), Preis „ab 349,99 USD“ aus einem Fab-Suchauszug
- Sonniss: [rekkerd.org GDC 2026](https://rekkerd.org/sonniss-releases-gdc-2026-game-audio-bundle/), [GameFromScratch GDC 2024](https://gamefromscratch.com/sonniss-27-5gb-sound-effect-giveaway-at-gdc-2024/)

**Projekt**
- `antworten/16-…`, `16e-…`, `16f-…`, `16g-…`, `16h-…` mit Nachträgen 1–5b, `17-…`, `bildkritik-witcher-messlatte.md`,
  `ufer-kies-coast-dunes.md`, `boden-kleinzeug-gras.md`
- `vorlagen/doku/fab_pakete_bewertung_2026-10-10.md`
- `antworten/fluss_sim/p2_lokal/master_graph_schaum8.json`
- `bilder/swr_p2/wasser_oberflaeche_g0_g4.jpg`, `bilder/zielbilder/witcher_01.jpg`
