# Antwort zu 16h Nachtrag 3 – Teile A und C1, Plan C.2–C.4, T3 (Tempo), FoamAtten, B.6, Mündung

Stand 13.10.2026. Grundlage: `auftraege/16h-nachtrag3-teile-a-c1-t3-schaum.md` (1680127), Bilder `bilder/swr_p2/teila_vorher_nachher.jpg`,
`teilc1_vorher_nachher.jpg`, `muendung.jpg`, Daten `antworten/fluss_sim/p2_lokal/querschnitte_p2.json` und
`master_graph_schaum8.json`, unsere Antworten 16h, [16h-Nachtrag](16h-nachtrag-materialtest.md) und
[16h-Nachtrag 2](16h-nachtrag2-tl-t0-kasten.md), 16f-Rückfrage (FoamAtten), 16g-Nachtrag 2 (v11).

**Kennzeichnung:** [Befund] Ferats Messung, [Projekt] eigene Daten und Rechnung, [Graph] aus Ferats Graph-Dump,
[Suchauszug] nur aus Suchergebnissen, [Ableitung] geschlossen, [Gestaltung] Entscheidung, [unsicher] im Test klären.

---

## Kurzfazit

1. **Teil A und C1:** gut umgesetzt.
   - Die Prallhänge (s 534–540 links, 550–556 rechts) sind zu Recht nicht zurückgelegt; sie werden jetzt felsig (Punkt 2).
   - **Kiesfeld:** Der pauschale Schutzabstand von 15 m ist für die C3-Bäche (2–10 m breit) zu groß. Neu: halbe Breite +
     clamp(1,5 × Breite; 6; 12) m.
   - 15 m bleiben nur am C3-Fluss selbst und im Mündungsfächer (≤ 40 m um die Mündung). Dort ist breiter Schotter natürlich.
2. **C.2–C.4 als Plan je Querschnitt: fertig.**
   - `skripte/ufer_regeln/ufer_plan_p2.py` → `ufer_p2/ufer_plan_p2.json`, in Bach-Koordinaten (s, Seite, d) mit Lagen,
     Kanten und Instanzen je Netz wie FORMAT.md §3.
   - Talkaskade, Kiesbett und Mündung: 414 Lagen-Abschnitte, 89 Kanten, 1 730 Instanzen in 21 Netzen. Alle Netze stehen in
     `netze.csv` und sind nicht gesperrt.
   - Der felsige Prallhang s 534–538 links ist eingeplant: Fels unten, Erdanriss oben, Blockfuß und 2 Uferfelsen.
   - Zwei Läufe byte-gleich; 0 FEHLER, Selbsttest 0 FEHLER.
3. **T3 – unsere Schwelle 250/450 cm/s war falsch.**
   - Sie beruhte auf dem freien Fall √(2gh). Die gebackene Simulation erreicht an Stufenfüßen nur 125–188 cm/s (Median), und die
     Rinnen der Talkaskade (209) sind schneller als ihre Stufenfüße.
   - Tempo allein trennt Rinne und Stufe nicht. Neu:
     - mit Tempo **FoamAttenMin/Max = 350/600 cm/s**: nur die steilen Stufen der Bergrinne (P90 664);
     - für Stufen ≥ 0,8 m sonst die **Steilheit der Wasserfläche** (57–70°) × Tempo ≥ 150–300 cm/s.
   - Gegen Manning: Talkaskade-Rinnen +67 %, Bergrinne-Stufenfüße +55 % (P90 3-fach), Becken im Durchbruch 5-mal langsamer.
4. **FoamAtten-Plan** (niedrige Priorität, Bachschaum ist nicht gewünscht).
   - Laut Graph-Dump liegen Simulationsschaum und dekodierte Strömung **nicht** im Master. Kandidat ist `/Water/Materials/Functions/WaterRiverFlowmaps`:
     sie bekommt die Wellenattribute und die Wasserzeit und speist den Schalter `Enable River` (bei uns True).
   - `SampleFluidSimulation` speist nur die Opazitäts-Maske (Interaktions-Sim und Ozean-Schaum), nicht die Flussfarbe.
   - Nicht belegt; deshalb **ein kurzer Dump-Auftrag an Ferat** statt Raten (4.3).
   - Alternative ohne Funktionskopie: Steilheit aus den Ableitungen der Weltposition, 8 Knoten im eigenen ELD-Zweig.
   - **Sofort:** `ELD_Strom_Schaum` 0, denn er liest die alte Strömungstextur `T_Eldarien_Wasserfluss` und nicht die SWR.
5. **B.6:**
   - Flussfelsen über 1,5 m **entfernen**. Ausnahme: ein Block im Prallhang (bis 6 m vom Bett) bleibt als Uferfels, ≥ 50 % versenkt.
   - Klänge: Im Repo nachweisbar sind 10 Cues `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_I_Cue` … `_X_Cue`
     (`inventar_extra.json`); ihr Inhalt ist unbekannt.
   - 40 % (−8 dB) ist als Zwischenstand in Ordnung; Ziel für Stufen −12 dB (≈ 25 %).
6. **Mündung:** `F_ERLENBACH` wird gekürzt, **umgesetzt (v12)**.
   - Der Exporter liest `ersetzt.json` → `muendung_anschluss` und kürzt den Kopf von `F_ERLENBACH_2_C3` bis zum p2-Spiegel
     (36,86 m + 2 cm): Schnitt bei **s 33,57 m**, Anfang jetzt auf 36,88 m statt 37,785 m; `F_ERLENBACH` 623,7 → 590,1 m.
   - Der Prüfer prüft den Anfangsspiegel. Prüfer **0 FEHLER**, 0 WARNUNG.
   - Der Hinweis in 16g §8 ist aktualisiert.

---

## 1. Teil A und C1

### 1.1 Würdigung

- **Teil A:** Mehr Moos und Gras am Ufer, der tote Streifen ist weg. Das entspricht dem Ziel; Gras-Karten 0 falsch [Befund].
  Die Box-Füllung wirkt.
- **C1:** 109 Zellen, 61 m³, höchstens 1,61 m Abtrag [Befund]. Das passt zu unserer Rechnung (15 Querschnitte, 56 m³;
  16h Nachtrag 2 §3).
  - Die kleine Sichtwirkung ist erwartet: Zurückgelegt wurden nur 0,5–1,6 m hohe Kästen.
  - Den Eindruck „sandiger Kasten“ machen vor allem die Lagen und die Tönung (Nachtrag 2 §1); dagegen helfen der Plan C.2–C.4
    und der Tönungs-Knoten.
- **Prallhänge ausgenommen:** richtig. Radius 6,8–16,8 m bei 3,6–3,9 m Breite liegt unter 5 B, und Prallhänge sind nach
  unserer Regel steil (45–70°).
  - Nach Regel `prallhang.felsig_ab_hoehe_m` werden sie ab 1,5 m Wandhöhe felsig. Im Plan trifft das auf s 534–538 links zu
    (Wandhöhe ≥ 1,5 m). s 550–556 rechts bleibt unter 1,5 m und damit Erdanriss mit Blockfuß.

### 1.2 Kiesfeld im 15-m-Schutzabstand der C3-Bäche: Abstand verkleinern

**Entscheidung** [Gestaltung, Ableitung]: Der Schutzabstand soll das **Hochwasserbett** des anderen Gewässers schützen, nicht
mehr. Für unser eigenes Bett gilt Teil A (Hochwasserbett 0–6 m, alte Bänke 6–12 m). Dieselbe Logik gilt für die Nachbarn:

| Nachbar | Breite | Schutzabstand neu | Begründung |
|---|---|---|---|
| C3-Bäche (`B_R2_K10_TUNDRA_01/_02`, `B_R_M1_*` usw.) | 2–10 m | **halbe Breite + clamp(1,5 × B; 6 m; 12 m)**, also 7 m bei 2 m Breite, 8 m bei 4 m, 16 m bei 8 m | Hochwasserbett eines Gebirgsbachs = 1–3 Bachbreiten |
| C3-Fluss `F_ERLENBACH_2_C3` | 25–36 m | **15 m** wie bisher | breite Schotterflur des Flusses; das Mündungsbild zeigt ihn als Tümpel im Schotterbett |
| Mündungsfächer p2 → C3 | – | **40 m Radius** um die Mündung (p2-s ≈ 748) bleibt Schotter | Schwemmkegel am Zusammenfluss: Kies ist dort natürlich |

Außerhalb dieser Zonen gelten die A-Bänder, also auch die Kappe Kies ≤ 5 % / Geröll ≤ 10 % in der Umgebung. Für Ferats Kette
ist das eine Zeile in der Maske: Abstand je Nachbar-Gewässer statt pauschal 15 m.

## 2. Plan C.2–C.4 je Querschnitt

### 2.1 Aufbau

- **Skript:** `python -I recherche/antworten/skripte/ufer_regeln/ufer_plan_p2.py [--abschnitte …] [--alle]`.
  - Standard: Talkaskade, Kiesbett und Mündung. Bergrinne und Durchbruch nur mit `--alle`, denn sie „sehen gut aus“.
  - Zwei Läufe byte-gleich, eingebaute Prüfung 0 FEHLER (Lagen-Summen, Lagen-Namen, Netze in `netze.csv` und nicht gesperrt,
    nichts tiefer als 0,6 m im Wasser).
- **Ausgabe** `ufer_p2/ufer_plan_p2.json` (`format` `ufer_plan_p2_v1`):
  - `lagen`: je Querschnitt und Seite Abschnitte `d_m` [von, bis] mit `klasse` (steil, prallhang_fels, erdanriss_oben),
    Neigung, `lagen` (Prozent, Summe 100) und `streifen_vorn` (der Uferstreifen bleibt dort vorn).
  - `kanten`: Böschungsschulter (d, Höhe über dem Spiegel, Wandhöhe, Prallhang).
  - `instanzen`: je Netz wie FORMAT.md §3 `dateien` (`pfad`, `rolle`, `gruppe`, `kollision`, `sichtweite`, `groesse_m`,
    `anzahl`), dazu `eintraege` mit den Spalten `s_m, seite, d_m, skala, yaw_rel_grad, kipp_grad, einbettung,
    h_ueber_spiegel_m`.
- **Koordinaten:** Bach-Koordinaten wie in Ferats Querschnitten.
  - Ferats Kette rechnet (s, Seite, d) mit derselben p2-Spline in x/y um.
  - z = Gelände − Einbettung × Netzhöhe (Netzhöhe = `groesse_m[2]` × Skala).
  - `yaw_rel_grad` gilt gegen die Fließrichtung, `kipp_grad` stromauf (Dachziegellage).
  - Das Format von `brush_uebernahme.py` liegt nicht im Repo. Deshalb sind die Felder an FORMAT.md §3 angelehnt (Rückfrage 1).

### 2.2 Regeln im Plan

| Teil | Regel (aus `bachbett_ufer_regeln.json`) |
|---|---|
| C.2 Lagen | je Profilpunkt bis 6 m mit Neigung ≥ 20°: `steil_mischung` (locker / steil / Erdanriss / Fels-Wand nach Neigung und Wandhöhe). Am **felsigen Prallhang** (Liste `C_ufer.prallhaenge_p2`, Wandhöhe ≥ 1,5 m): Fels-Wand unten, die oberen 0,8 m Erdanriss |
| C.3 Kante | Schulter = erster Punkt nach ≥ 30°, an dem die Neigung unter 20° fällt (≤ 6 m), nicht an Felswänden ≥ 3 m |
| Gras | 60–80 % der Kantenlänge, Abstand 0,4–0,8 m, 0,15–0,35 m über die Kante, 20–40° zum Wasser: `SM_grass_bush_01`–`04`, `SM_GrassyEmbankment_01/02` |
| Moos | 1 Gruppe je 1,5–3 m, 2–3 Polster, 0–1,2 m über dem Spiegel: `SM_MossClump_01/03/05`, `SM_moss_01/02` |
| Wurzeln | nur felsiger Prallhang mit Kante, Rolle `wurzel_bedingt_baum_6m` (nur mit Baum ≤ 6 m): `SM_Pine_roots_03/04`, `SM_crooked_root_01/04`, `SM_ForestRoots_01`. Im jetzigen Plan trifft das nicht zu (keine Kante am felsigen Abschnitt) |
| Farne | **nicht gesetzt**: Nordseite und Baumnähe fehlen in den Querschnitten |
| C.4 Prallhang-Fuß | Blöcke 0,6–1,4 m, d −0,4…+0,6 m, Einbettung 35–55 %, 1–2 je 2 m: `skjsL_tier_0`, `texndcpda_tier_0`, `SM_mountain_rock_big_02_2` (Skala 0,35–1,8) |
| Uferfels | felsiger Prallhang mit Wand ≥ 2,5 m: 1,5–2,5 m, Einbettung 50–60 %: `SM_mountain_rock_big_02_1/2` |
| Kopfsteine | Ufer mit Kante bzw. Wand ≥ 0,5 m: 3–6 je 10 m, 0,3–0,6 m, Einbettung 30–50 %: `SM_mountain_rock_small_01_1/2/3` |
| Kiesel | flache Ufer (Kiesbett, Mündung): 2–4 Packs je 10 m: `SM_SmallStonesPack_01/03/06/13` |
| nicht im Plan | Stufen-Widerlager und Lippenzonen (die Querschnitte kennen die Lippen nicht): Ferats Bachdekor filtert und setzt sie |

### 2.3 Zahlen

| Abschnitt | Querschnitte | Lagen-Abschnitte | Kanten | felsiger Prallhang |
|---|---|---|---|---|
| Talkaskade | 190 | 411 (403 steil, 5 Fels, 6 Erdanriss oben) | 89 | 5 |
| Kiesbett | 148 | 3 | 0 | 0 |
| Mündung | 60 | 0 | 0 | 0 |

**Instanzen 1 730:**
- Gras an der Kante 217: Büschel 141, Embankment 76.
- Moos 1 089, meist kleine Polster.
- Kopfsteine 81, Prallhang-Blöcke 10, Uferfelsen 2.
- Kiesel-Packs 331.

Das liegt weit unter dem Budget (≤ 60 000 je Feld). Mit Kollision sind nur die Blöcke ≥ 0,8 m und die Uferfelsen; Steine
≥ 0,4 m am Wasser als SWR-Hindernis eintragen, dann Reset + Bake.

## 3. T3 – Schaum-Schwellen aus dem gemessenen Tempo

### 3.1 Korrektur

**Unsere Annahme (16f-Rückfrage §3.1):** Fallfuß ≈ √(2gh), also 4,4 m/s ab 1 m Fall; FoamAtten 250/450 cm/s.

**Befund T3:** Stufenfüße im Median 125–188 cm/s, nur die Bergrinne erreicht im P90 664 cm/s. Die Rinnen der Talkaskade liegen
bei 209 (P90 250) und sind damit schneller als ihre Stufenfüße (125).

**Warum** [Ableitung]:
- Die Simulation (Zellen 0,25–0,37 m) mittelt den Strahl über Zellen und verliert Energie an der Stufe.
- In steilen Rinnen fließt dagegen gleichmäßig schnelles, flaches Wasser.

**Damit war 250/450 falsch:** Diese Schwelle hätte die Rinnen der Talkaskade leicht schäumen lassen und die Stufen kaum.

### 3.2 Neue Schwellen (Ferats Regel: kein Schaum im Bach, nur etwas an Fällen)

| Variante | Formel | Wirkung nach T3 |
|---|---|---|
| **A: nur Tempo** (mit FoamAtten-Kopie) | `FoamAttenMin` **350**, `FoamAttenMax` **600** cm/s, `LowVelocityFoamScale` 0 | Schaum nur an den steilsten Stufen der Bergrinne (P90 664, alle Zellen P99 609); Talkaskade (P90 250/285), Kiesbett und Durchbruch frei |
| **B: Steilheit × Tempo** (empfohlen, wenn Fälle der Talkaskade etwas Schaum zeigen sollen) | Schaum = SmoothStep(0,45; 0,66; 1 − N_z) × SmoothStep(150; 300; v) | 1 − N_z = 0,45…0,66 entspricht 57–70° Flächenneigung. So steil ist das Wasser nur über einer Stufe ≥ ~0,8 m (bei 0,25–0,37 m Zellen); eine Rinne mit 30 % Gefälle hat 17° → kein Schaum, auch bei 209 cm/s |
| **B ohne Tempo** | Schaum = SmoothStep(0,45; 0,66; 1 − N_z) | wie B; ruhige, steile Ränder kommen in Wasserflächen praktisch nicht vor |

- Für Ferats Wunsch reicht **A**. **B** ist die Kombination „Tempo × Stufenhöhe“; die Steilheit vertritt die Stufenhöhe.
- [unsicher] B hängt an der Auflösung der WCBS-Wasserfläche: Ein grobes Netz glättet die Stufen. Test: Steilheit als Debug-Farbe
  (4.4).

### 3.3 Vergleich mit Manning `tempo_ms` (fluss_sim)

p2 liegt nicht in unserem Export; verglichen werden die Mediane der Gefälleklassen aller exportierten Gewässer
(`zusammenfassung.json` → `tempo`, Manning-Strickler, k_st 15 für Bäche).

| Abschnitt (Gefälle) | Manning (Klasse) | gemessen (Median) | Abweichung |
|---|---|---|---|
| Bergrinne (39,7 %) | > 15 %: 125 cm/s; Rolle Fuß 121 | Rinnen 47, Stufenfuß 188 (P90 664) | Rinnen −60 %, Fuß **+55 %**, P90 rund dreimal Manning |
| Durchbruch (5,4 %) | 5–15 %: 74; Becken 21 | Rinnen 45, Becken **4** | Becken 5-mal langsamer (Totwasser) |
| Talkaskade (29,6 %) | > 15 %: 125 | Rinnen **209**, Stufenfuß 125 | Rinnen **+67 %**, Fuß gleich |
| Kiesbett (5,0 %) | 1–5 % / 5–15 %: 45–74; Becken 21 | Rinnen 95, Becken 20 | Rinnen +30 bis +110 %, Becken gleich |

**Folgerung:**
- Manning beschreibt den Mittelwert über Becken und Rinne gut.
- In steilen, schmalen Rinnen bündelt die Simulation das Wasser schneller. Im Durchbruch stehen die Becken fast still.
- Für die Spline (`WaterVelocityScalar`) ändert das nichts, denn die gebackene Strömung ersetzt sie in WCBS.
- Wo die Spline-Strömung sichtbar ist (Flowmap ohne SWR), wären steile Rinnen leicht zu langsam. Das ist ein Hinweis, keine
  Änderung.

## 4. FoamAtten: wo liegen Geschwindigkeit und Simulationsschaum?

### 4.1 Was der Graph-Dump zeigt [Graph]

| Funktion | Eingänge (im Master) | Ausgänge (im Master) | Deutung |
|---|---|---|---|
| `/Water/Materials/Functions/WaterRiverFlowmaps` | Wellenattribute (Reroute nach `SetWaveAttributes`), `GetWaterTime` | Schalter `Enable River` (bei uns True) → Reroute → `BeachFoam` | **Flusspfad.** Hier kommen Flussströmung, Flowmap-Normale und vermutlich der Fluss- und Simulationsschaum zusammen [Ableitung]. **Kopier-Kandidat** |
| `/Water/Materials/Layers/BeachFoam` | Ausgang des Flusspfads | Schalter `Enable Ocean Foam`, `Multiply` | mischt Schaum in die Attribute [Ableitung] |
| `/Water/Materials/Functions/SampleFluidSimulation` | Schalter `Enable Ocean Foam` (bei uns False), `GetWaterTime` | nur `WaterOpacityMaskFromDepth` | **Interaktions-Simulation** (Spieler) bzw. Ozean-Schaum, wirkt bei uns auf die Opazitätsmaske, nicht auf die Flussfarbe |
| `/Water/Materials/Layers/WaterAttributes` | – | `Water_Underside`, `GetMaterialAttributes` | Grund-Attributsatz [Ableitung] |
| `WaveVelocityMask` | Gerstner-Wellen | See-/Ozean-Übergang | Wellen, nicht Fluss |

- **Absorption** → `Divide` (Kehrwert): Damit ist 16a b1 bestätigt.
- **Scattering** → `Multiply` → `Add` (+ Foam Scattering) → `Divide` → `Water_Underside`: Der Weg ist geteilt bzw. skaliert. Das
  erklärt, warum A 0,1 so schwach wirkt (T0).
- **Nicht im Master:** `Velocity Debug`, `SimFoam Contrast`, `Foam Opacity`, `Sim Foam Normal`, `Foam Boost`, `MaxFlowVelocity`
  [Befund]. Sie stecken in einer der Funktionen oben, nach der Verdrahtung am wahrscheinlichsten in `WaterRiverFlowmaps`.
- **Suche:** Zu `WaterRiverFlowmaps`, `SampleFluidSimulation` und `WaterAttributes` gibt es keine öffentliche Doku
  [Suchauszug].
  - Belegt ist nur das Prinzip: Die Strömung kommt von den Spline-Geschwindigkeiten, wird als Flowmap geschrieben und treibt
    die Fläche ([Water Body Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-body-actors-in-unreal-engine)).
  - Fluss-Schaum braucht laut Forum den Schalter in der MI und die Fluid-Sim im Level
    ([Forum](https://forums.unrealengine.com/t/water-plugin-in-ue5-does-anyone-know-how-to-use-the-foam-on-rivers-see-video-linked/688819)).
  - Den genauen Knoten belegt das nicht; deshalb nicht raten.

### 4.2 Plan (wenn Schaum doch gewünscht wird)

1. `WaterRiverFlowmaps` nach `/Game/Eldarien/Welt/Wasser/Funktionen/MF_EL_WaterRiverFlowmaps` **kopieren** (Plugin-Inhalt nie
   ändern).
2. In der Kopie den Knoten suchen, an dem die Länge der Strömung entsteht (Vergleich mit `River Flowmap Detection Velocity`) bzw.
   der Schaumwert vor `SimFoam Contrast`.
3. Dort `FoamGate = Lerp(LowVelocityFoamScale; 1; SmoothStep(FoamAttenMin; FoamAttenMax; v))` einschleifen (Werte 3.2 A).
   Die Geschwindigkeit zusätzlich als Ausgang `EL_Tempo_cm_s` herausführen (für die Velocity-Streuung).
4. Master-Kopie `M_Eldarien_Wasser_Schaum9` ruft die Kopie statt der Epic-Funktion. `MI_EL_SWR_Klar` umhängen.

Schritt 2 setzt den Dump 4.3 voraus.

### 4.3 Dump-Auftrag an Ferat (10 Minuten, mit eurem Graph-Werkzeug wie für `master_graph_schaum8.json`)

Für **`/Water/Materials/Functions/WaterRiverFlowmaps`**, **`/Water/Materials/Layers/BeachFoam`** und
**`/Water/Materials/Functions/SampleFluidSimulation`** je eine Datei `funktion_<Name>.json`:
- alle `FunctionInput`- und `FunctionOutput`-Namen;
- alle Parameter (Skalar, Vektor, Textur, Schalter) mit ihren Ziel-Knoten;
- verschachtelte Funktionsaufrufe (Pfad);
- die Ketten (wie `ketten` im Master) für `Velocity Debug`, `SimFoam Contrast`, `Foam Opacity`, `Sim Foam Scale`,
  `River Foam Scale`, `MaxFlowVelocity`, `WaterVelocityAndHeight`, `BakedWaterSimTex` bis zum Ausgang.

Damit kann ich den Einschleifpunkt aus Schritt 2 knotengenau nennen.

### 4.4 Steilheits-Alternative (ohne Funktionskopie)

- Eine eigene Normale der gebackenen Fläche ist im Master-Graph nicht zu sehen [Graph].
- Die Steilheit lässt sich aber im Pixel-Shader aus der Weltposition bilden, unabhängig von Epics Funktionen [Ableitung]. Die
  WCBS-Fläche ist über `WaterHeightMappingVS` (Schalter `Enable Water VS Mapping` = True) schon verschoben.
- **Knoten (8):** `AbsoluteWorldPosition` → `DDX` und `DDY` → `Cross` → `Normalize` → `ComponentMask(B)` → `Abs` → `OneMinus` =
  Steilheit → `SmoothStep(0,45; 0,66)` → `Multiply` in den ELD-Schaum (Alpha des Lerps an `ELD_Schaum_Deckkraft`).
- **Test:** zuerst die Steilheit als Emissive-Debug an t430/t500 ansehen. Sind Stufen klar und Rinnen dunkel, reicht B ohne Tempo
  (3.2).
- [unsicher] Die Normalen sind je Pixel-Quad facettiert; bei grobem Wassernetz kann die Steilheit flackern oder zu schwach sein.

### 4.5 Sofort

- **`ELD_Strom_Schaum` 0:** Er liest laut Graph die alte Strömungstextur `T_Eldarien_Wasserfluss` [Befund], nicht die SWR. Seine
  Flecken folgen also der alten Strömung.
- Variante F bleibt. Alles Weitere zum Schaum hat **keine Eile**; zuerst die Fall-FX.

## 5. B.6

### 5.1 Die 14 Flussfelsen (1,9–12 m vom p2-Bett)

Konsistent mit Nachtrag-1-Antwort §5 (Band 0–12 m):

| Größe | Lage | Entscheidung |
|---|---|---|
| ≤ 1,5 m | 0–12 m | behalten, 40–60 % eingraben, Moos oben; ≤ 1 m am Wasser als SWR-Hindernis |
| > 1,5 m | Prallhang s 534–540 links bzw. 550–556 rechts, ≤ 6 m vom Bett | **ein** Block als Uferfels behalten, **versenken auf ≥ 50 %** (Mittelpunkt um (0,5 − heutiger Anteil im Boden) × Höhe senken); er ersetzt dort einen der geplanten Uferfelsen aus 2.3 |
| > 1,5 m | sonst | **entfernen** |

- Warum nicht alle versenken: Ein Feld großer, versenkter Blöcke ohne den Fluss, der sie abgelegt hat, wirkt wie der alte
  Schotterstreifen.
- Erlaubt bleibt höchstens 1 Findling je 50 m außerhalb 12 m. Die Blöcke liegen aber alle innerhalb 12 m.
- „Mittelpunkt −30 % der Höhe“ reicht nicht, wenn der Block heute auf dem Gelände sitzt: Das sind nur 30 % im Boden.

### 5.2 Klänge

- **Im Repo nachweisbar** (`vorlagen/daten/inventar_extra.json` → `klaenge`): 10 SoundCues
  `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_I_Cue` bis `…_X_Cue`.
- Ihren Inhalt kenne ich nicht. `export/unreal/welt/inventar/` mit der vollständigen Liste liegt nicht im Repo.
- NatureWaterFX ist ein Niagara-Paket; Klänge dazu finde ich im Inventar nicht.
- **Vorschlag:** Ferat hört die zehn Cues an und sortiert sie in drei Gruppen:
  - leises Gluckern → ruhige Strecken (−16 bis −18 dB, Reichweite 10–15 m);
  - Plätschern → Stufen 0,5–1 m (−12 dB, 15–20 m);
  - kräftiges Rauschen → Fälle ≥ 1 m (−6 bis −8 dB, 30–40 m).
- **40 % als Zwischenstand: ja.** 40 % Amplitude sind etwa −8 dB. Für die alten Flussklänge an Stufen ist das noch etwas laut;
  30 % (−10 dB) wären näher am Ziel.

## 6. Mündung: `F_ERLENBACH` gekürzt (v12)

- **Bild bestätigt:** C3 ist an der Mündung ein Tümpel im breiten Schotterbett, es gibt keine Glaswand [Befund]. Rückfrage 3
  aus Nachtrag 2 ist damit weitgehend erledigt.
- Die Lesart gilt: Der Kopf 37,78 / 37,42 / 37,00 m ist der Rest des ersetzten 2_C2.
- **Umgesetzt** (klein und sauber):

| Datei | Änderung |
|---|---|
| `skripte/fluss_sim/ersetzt.json` | `ersatz.ERLENBACH_P2.muendung_anschluss`: `aktiv` true, `toleranz_cm` 2, Status „umgesetzt“ |
| `fluss_sim_export.py` | `ersatz_anschluesse()` liest den Anschluss. `kopf_kuerzen()` sucht auf der Linie des Ziel-Laufs (nur ohne Gefälle-Plan) den ersten Punkt mit Spiegel ≤ p2-Spiegel + 2 cm (linear). `zusammenfuegen` beginnt den ersten Lauf der Kette dort, wie die Feldgrenzen-Kürzung: `s_quelle_m`/`gekuerzt_m` zeigen den Schnitt. `anfang.kopf_gekuerzt` nennt ihn, `anfang.punkt_cm` ist der neue Anfang |
| `fluss_sim_pruefen.py` | FEHLER, wenn ein Gewässer am Ziel-Lauf über dem Ersatz-Spiegel beginnt oder der Schnitt nicht zum Lauf passt; sonst HINWEIS mit Anfangsspiegel |

**Zahlen** (2-m-Daten; v11 = Stand des 16g-Agenten, gegen die Repo-Beispiele byte-gleich nachgerechnet):

| | v11 | v12 (Kopf gekürzt) |
|---|---|---|
| `F_ERLENBACH` | 623,7 m, Anfang 37,785 m, Fingerabdruck `d48d07dd22ff…`, 139 Objekte, Zelle 0,299 m | **590,1 m**, Anfang **36,88 m** (Schnitt s 33,57 m auf `F_ERLENBACH_2_C3`), `3fab28f7938b…`, 131 Objekte, Zelle 0,284 m |
| Zuflüsse | `B_R2_K10_TUNDRA_02` / `_01` bei s 148,5 / 192,9 | bei s 114,95 / 159,29 (nur verschoben) |
| Fingerabdrücke | – | geändert: `F_ERLENBACH`, `B_R2_K10_TUNDRA_02` (Objektteil 32 → 31); alle übrigen 195 gleich |
| Wasserzonen | 35 Zonen, 1 378,5 MB | gleich |
| Prüfer | 0 FEHLER, 0 WARNUNG, 73 HINWEIS | **0 FEHLER, 0 WARNUNG, 74 HINWEIS** (neu: „Anschluss an ERLENBACH_P2 … Kopf 33,57 m gekürzt“) |

Die Beispiele `antworten/fluss_sim/` (`F_ERLENBACH`, `zusammenfassung.json`, `wasserzonen.json`, `back_liste_auszug.json`) sind
neu. Zwei Exporte sind byte-gleich: ja (`diff -r` leer), Prüfer des zweiten Laufs ebenfalls 0 FEHLER.

- 16g-Nachtrag-2 §8: Der Nachtrag-Hinweis ist auf „umgesetzt (16h Nachtrag 3)“ aktualisiert.
- **Backen:** `F_ERLENBACH` mit dem neuen Fingerabdruck backen. Ferats p2-Spline endet bei s ≈ 748.

## 7. Was lokal zu tun ist

Commit **`@@HASH@@`** holen.

1. **Plan C.2–C.4:** `ufer_p2/ufer_plan_p2.json` über eure Kette einbauen.
   - (s, Seite, d) → Welt mit der p2-Spline; Lippenzonen mit dem Bachdekor filtern.
   - Wurzeln nur mit Baum ≤ 6 m.
   - Danach Reset + Bake (Steine ≥ 0,4 m am Wasser als Hindernis).
2. **Kiesfeld:** Schutzabstand der C3-Bäche nach 1.2 verkleinern, Teil A dort neu rechnen; C3-Fluss und Mündungsfächer bleiben.
3. **Schaum:** `ELD_Strom_Schaum` 0. Optional Steilheits-Debug (4.4) und Dump 4.3. Sonst keine Eile.
4. **Flussfelsen** nach 5.1; **Klänge** anhören, sortieren, 30–40 %.
5. **fluss_sim** neu exportieren, `F_ERLENBACH` neu backen.

## Quellen

- Ferats Nachtrag 3 mit Bildern, Querschnitten und Graph-Dump (siehe Kopf); `vorlagen/daten/netze.csv`, `netz_sperre.json`,
  `inventar_extra.json` (Klänge); `vorlagen/FORMAT.md` §3.
- [Water Body Actors (Epic-Doku, Suchauszug)](https://dev.epicgames.com/documentation/en-us/unreal-engine/water-body-actors-in-unreal-engine)
  – Strömung aus den Spline-Geschwindigkeiten als Flowmap.
- [Epic-Forum: foam on rivers (Suchauszug)](https://forums.unrealengine.com/t/water-plugin-in-ue5-does-anyone-know-how-to-use-the-foam-on-rivers-see-video-linked/688819)
  – Fluss-Schaum über MI-Schalter und Fluid-Sim im Level.
- Montgomery & Buffington 1997 (Hochwasserbett/Gerinnetypen), wie 16f; unsere Antworten 16f-Rückfrage §3 (alte Schwelle),
  16h Nachtrag 2 (Mündung, Zurücklegen).

## Rückfragen

1. **Format für eure Kette:** Liest `brush_uebernahme.py`/`sehens_einbau` Bach-Koordinaten (s, Seite, d)? Sonst bitte ein kurzes
   Beispiel eures Eingabeformats; dann schreibe ich die Ausgabe direkt in Weltkoordinaten (dazu bräuchte ich die p2-Spline als
   Punkte).
2. **Dump 4.3**, falls Schaum später doch kommt.
3. **Klänge:** die Gruppierung der zehn `CUE_Water_Stream_*`-Cues nach dem Anhören.
