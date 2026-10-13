# Antwort 16h Nachtrag 6e – Messlatte Witcher 4, Fels-Master repariert, was der Talkaskade noch fehlt

Stand 13.10.2026. Bezug: `auftraege/16h-nachtrag6e-ferat-witcher4-fels-master.md` (§1–§6), Bild `bilder/swr_p2/fels_master_repariert_msr.jpg`,
unsere Antworten 6c (Bettplan), 6d (Steine und Wasser, gleichzeitig), N6 §4.2 (Nasslinie) und 18.

**Kennzeichnung:**
- [Ferat]: eure Angabe oder euer Bild
- [Plan]: im Bettplan gerechnet
- [Suchauszug]: Web-Suche; die Seiten selbst sind nicht gelesen
- [Ableitung]: aus Belegen geschlossen
- [Annahme]: Gestaltungswert

## Kurzfazit

- **Der kaputte Master** erklärt die „hellen Platten wie Laub“ [Ferat]. Er war ein Pflanzen-Master mit Windröschen-Textur, Blattlöchern und Wind.
  - Unsere Deutungen in 18 §2, N2 und N5 lagen deshalb auf falscher Grundlage. Die Korrekturen stehen in §1.
  - Die Albedo-Messung aus 6d bleibt gültig: Sie wurde an den echten Texturen gemessen.
- **Auf dem MSR-Bild** sind die Laubflecken weg. Jetzt sieht man zwei Fehler:
  - **helle Steine unter Wasser:** `mountain_rock_small` grau-hell, `SmallStonesPack` beige
  - **das Spiegelmuster der Oberfläche:** Quecksilber-Schlieren bei t430 und t550
  - Beides geht 6d an: Zielhelligkeit unter Wasser 0,08, Nasslinie auch für `M_Master_material`, V20a.
- **Stein-Palette im Bett:**
  - Die 6c-Zusatznetze bleiben.
  - Neu: Unter Wasser bevorzugt Netze, deren Material eine Nasslinie hat. Bis `M_Master_material` eine Nasslinie hat, bleiben dessen Steine in den `_Nass`-Typen mit Faktor 0,35.
  - Nie doppelt abdunkeln: Nasslinie und `_Nass`-Kopie zusammen ergäben ≈ 0,28 × Albedo (6d §2).
- **Was der Talkaskade nach Bettplan und Steinen bis Witcher 4 fehlt,** nach Wirkung (§3):
  1. Vegetation bis an die neue Kante
  2. nasse, bemooste Steine
  3. ruhigere Oberfläche (6d)
  4. Licht und Schatten im Einschnitt
  5. Totholz
  6. Fall-Effekte
  7. Details

  Punkte 1 und 5 habe ich als **Ergänzung des Bettplans** gerechnet: 279 Kantengras, 432 Moos, 65 Farne (nur Nordufer), 5 Totholz. Alle Netze aus dem Inventar, 0 FEHLER.
- **`lauf_p2.json`:**
  - `p2_bett_welt.py` passt zu euren Schlüsseln: `i`, `j` = Raster, X = (j − 4730,5) m, Y = (i − 4060,5) m, `s` je Punkt.
  - Neu liest es auch die Spaltenform `{i: [...], j: [...], s: [...]}`.
  - Selbsttest erneut: p95 3 cm, byte-gleich, Spaltenform gelesen.
  - Die flachere Variante habe ich nicht gerechnet; Durchbruch und Bergrinne folgen später.

## Was fehlt bis Witcher 4 (fester Abschnitt, gilt für die ganze Landschaft)

**Was über die Witcher-4-Techdemo öffentlich bekannt ist** [Suchauszug]:
- Gezeigt auf der State of Unreal 2025. Die Demo spielt in der Region Kovir (Ciri, Pferd Kelpie). Sie lief auf einer PS5 mit 60 fps und Raytracing.
- CDPR betont: Es ist eine Techdemo, kein Spielausschnitt, und nicht repräsentativ für das fertige Spiel.
- Gezeigte Technik:
  - **Nanite Foliage**: dichte Wälder und Felder ohne LOD-Sprünge, einzelne Nadeln nah sichtbar.
  - Unreal Animation Framework, MetaHuman mit Mass AI (bis 300 Figuren), ML Deformer für den Pferdekörper.
  - FastGeo Streaming. Die Werkzeuge erscheinen ab UE 5.6.
- **Nanite Foliage** ist laut Berichten zu UE 5.7 experimentell und besteht aus drei Teilen:
  - Nanite **Assemblies** (Varianten)
  - Nanite **Skinning** (Wind, Äste schwingen)
  - Nanite **Voxels** (Blätter und Nadeln in der Ferne als Voxel)
- Eine deutsche Analyse sah Spiegelungen in Seen und Pfützen klassisch per Screen-Space-Reflections, mit den typischen Artefakten. Zu Wasser und Flüssen sagen die Quellen sonst nichts Genaues.

**Was wir daraus als Messlatte nehmen** [Ableitung]:
1. **Vegetation:** sehr dicht und bis an jede Kante, ohne sichtbare LOD-Wechsel.
2. **Bewegung:** Bäume und Büsche schwingen im Wind.
3. **Licht:** Raytracing bzw. Lumen mit dichtem Bewuchs, also weiches Schattenlicht unter Büschen und in Rinnen.
4. **Wasser:** klare Formen mit Ufer, Steinen und Spiegelung; perfekte Spiegel verlangt die Demo nicht.

Unsere Stellen messen wir künftig gegen diese vier Punkte, jeweils mit „was fehlt“ nach Wirkung.

**Bei uns** [Ableitung, unsicher]:
- Wir arbeiten mit UE 5.8. Ob Nanite Foliage (Assemblies/Skinning/Voxels) dort produktiv nutzbar ist, ist nicht geprüft.
- Vorschlag für später: ein Test mit einem Busch- und einem Gras-Netz an der Talkaskade. Messen: FPS, Wind, Fernbild.
- Bis dahin ersetzt Dichte über Instanzen (§3) das Nanite-Foliage-Bild.

## 1. Korrekturen unserer Deutungen (kaputter Master seit 08.10.)

| Antwort | damalige Aussage | richtig |
|---|---|---|
| 18 Kurzfazit 3, §2.1, §3.3 | „helle Platten unter Wasser wirken wie Laub“, „große helle flache Steine, die durch die Verzerrung wie Laub aussehen“ | **Es war Laub:** Die Fels-Instanzen zeigten die Windröschen-Textur mit Blattlöchern [Ferat]. Die Verzerrung war nicht die Ursache. Die Folgerung „helle Platten ersetzen“ ist hinfällig. Neu zu beurteilen sind die echten hellen Steine (6d) |
| N2 Rang 2 | „Die Flecken sind Steine, verzerrt durch die Normalen“ | **halb richtig:** Es waren Stein-Netze, aber mit Pflanzentextur. Die Normalen verzerren zusätzlich, sind aber nicht der Grund für das Laub-Aussehen |
| N5 §4, 6d | Steine nass gegen trocken, Wirkung der Abdunklung (× 0,55 / × 0,30) im Bild | Die Bildurteile (z. B. „orange unter braunem Wasser“) galten der Pflanzentextur. Die **Rechnung** (Albedo × Faktor) stimmt weiter, weil die Messung an den echten Texturen lief. Die Faktoren lege ich in 6d §2 neu fest |
| N6 §4 | Nasslinie für `MI_EL_SmallStonesPack_01` (Master `M_EL_Fels_MS`) | gilt, jetzt auf `M_EL_Fels_MS2` [Ferat §6]. Der Parametername `Nass_Rauheit_Linie` passt |

**Am Master selbst** trifft uns keine Schuld: Das Bauskript lief bei euch. Unsere Bilddeutungen haben aber eine einfache Prüfung ausgelassen.

**Lehre:** Bei rätselhaften Flecken künftig zuerst die Material-Kette der betroffenen Netze prüfen: Shading Model, Blend, WPO, Texturname. Erst danach Optik deuten. Diese Prüfung steht ab jetzt in jeder Bildbefund-Antwort am Anfang.

## 2. Stein-Palette im Bett nach der Reparatur

Auf dem MSR-Bild sind die Steine jetzt lesbar [Ferat]:
- `SmallStonesPack` beige (Y 0,125)
- `mountain_rock_small` grau (Y 0,229, das hellste Netz)
- Stämme als Holz

Was das für die Palette heißt:
1. **Bettplan (6c):**
   - Die Zusatznetze bleiben, auch `SM_MossyForestBoulder_*`. Das sind `MI_EL_*`-Netze auf MS2, also mit Nasslinie.
   - Neu: Für Lippenblöcke **unter oder an der Wasserlinie** sollen Netze mit Nasslinie Vorrang haben. Das sind MS2-Netze, z. B. MossyForestBoulder und NordicBoulder.
   - `mountain_rock_small_01_*` (`M_Master_material`) bekommt erst einen Platz an der Lippe, wenn dieser Master eine Nasslinie hat (6d §2, Frage 3).
   - Welches Material `skjsL_tier_0` und `texndcpda_tier_0` (Megascans-Fab) nutzen, kenne ich nicht. Bitte nennen (Rückfrage 1). Dann trage ich die Material-Spalte in die Paletten-Regel ein.
2. **Bachdekor-Planer unter Wasser:** keine eigene Palette nötig. Die Nasslinie dunkelt pixelgenau ab. Die Zielhelligkeit steht in 6d §2: Y ≈ 0,08.
3. **Große helle Platten** (`SM_flat_rock_03`, `SM_SmoothRockShelf_01`, `SM_ground_rock_03_01`): nur 5 ganz unter Wasser [Ferat 6d]. Kein Handlungsbedarf, mit Nasslinie sind sie nass-dunkel.

## 3. Was der Talkaskade nach Bettplan und reparierten Steinen bis Witcher 4 fehlt (nach Wirkung)

| Rang | Was | konkret (Regel, Wert, Netz) | Stand |
|---|---|---|---|
| 1 | **Bewuchs bis an die neue Kante** | **Kantengras** (überhängend) auf der Schulter, Fuß auf Spiegel + Uferstufe, 0,15–0,35 m über die Uferstufe, alle 0,4–0,8 m auf 60–80 % der Kante, 20–40° zum Wasser geneigt: `SM_grass_bush_01…04`, `SM_GrassyEmbankment_01/02`. Dazu Landschaftsgras an der Kante × 1,3 (`C_ufer.bewuchs_kante`) | **im Bettplan: 279** |
| | | **Moos** auf Uferstufe und Schulter 0,05–1,2 m über dem Spiegel, 0,33–0,67 Gruppen je m: `SM_moss_01/02`, `SM_MossClump_01/03/05` | **im Bettplan: 432** |
| | | **Farne** nur am Ufer, dessen Böschung nach Norden schaut (Schatten im Einschnitt), Gruppen 1–3 alle 8–15 m, 0,3–2 m hinter der Schulter: `SM_Fern_01/02/04`, `SM_EagleFern_S_01/02`. Das Weltwerkzeug filtert das Nordufer (Selbsttest: 33 von 65 weggelassen) | **im Bettplan: 65 Kandidaten** |
| 2 | **Nasse, bemooste Steine** | Nasslinie MS2 (erledigt [Ferat]); dieselbe für `M_Master_material` (6d §2). **Algen unter der Linie** [Annahme]: Albedo × (0,75; 0,85; 0,60), nur ab 5 cm unter dem Spiegel, im Material über h < −5 cm, 4 Knoten. **Moos oben** auf Blöcken über Wasser [Annahme]: Lerp zur Moosfarbe (0,10; 0,13; 0,05) über WorldNormal.Z 0,6–0,85, nur ab Nasslinie + 0,3 m, Stärke 0,6, ca. 8 Knoten. Ersetzt Moos-Instanzen auf Blöcken (deren Höhe kennt erst der Setzer) | Material-Skizze |
| 3 | **Ruhigere Oberfläche** | E16 bleibt; V20a (`ELD_Normal_Nah` 0,35); Coast-Vergleich, siehe 6d §1 | V20a in Arbeit [Ferat] |
| 4 | **Licht und Schatten im Einschnitt** | Der Einschnitt (Median 1,6 m) gibt von selbst Schatten. Dafür müssen Lumen und Schatten die neuen Blöcke kennen: Mesh Distance Fields für die Netze der Ebene `p2_bett` (Projekt-Einstellung bzw. Netz-Option, Name in 5.8 prüfen), Contact Shadows an der Sonne. **Prüfung:** Y(Becken) / Y(Ufer-Gras) ≤ 0,6 an `C2_tk_becken_auge` (K3 aus 18) | Einbau-Hinweis |
| 5 | **Totholz** | quer über Hauptbecken ≥ 4,5 m (auf beiden Schultern, 0,15–0,35 m über der Schulter, Länge 1,15–1,45 × Breite) oder schräg am Lippenende auf dem Eckblock; alle 28–45 m; `SM_OldTreeBranch_02`, `SM_FallenSpruceTree_01`, `SM_OldFallenTree_02` (gewählt), Kandidaten auch `_03/_06`, `SM_dead_log_03/04`; Skala 0,6–1,8, kein Sägeschnitt (13k geprüft); Kollision ja, kein SWR-Hindernis (liegt über dem Wasser) | **im Bettplan: 5** |
| 6 | **Fall-Effekte** | `NS_Impact_Small` je Einheit an der höchsten Stufe ≥ 1 m (24), `NS_Waterfall_Small` ab 1,8 m (3); Ferat entscheidet (6b c) | Vorschlag im Plan |
| 7 | **Details** | Kies im Kolk (331, im Plan); Lagen nach Zonen: Kolk Kies/Geröll, Lippe Geröll/Fels, Uferstufe Erde/Moos, Bett ohne Graslage (`talkaskade_zonen.u8`); Klang `CUE_Water_Stream_*` an 2–3 Kaskaden (Antwort 14) | Zonen liegen bereit |
| später | **Nanite Foliage, Wind** | Test in 5.8, siehe oben | offen |

**Ergänzung des Bettplans** (`skripte/p2_bett/p2_bettplan.py`, Regeln `p2_bett_regeln.json` → `ausstattung_6e`):
- Neue Spalte `z_absolut` für Gras auf der Schulter und Holz auf den Schultern bzw. dem Eckblock. Diese Teile stehen sonst im Wasser.
- Der Prüfer verlangt:
  - Kantengras und Totholz ≥ 0,15 m über dem Spiegel
  - kein Totholz im Hauptstrahl
  - Kantengras nicht auf der Wand einer schrägen Stufe
- Ergebnis: 1 402 Instanzen, davon 221 mit Kollision. 0 FEHLER, 3 WARNUNGEN (unverändert die drei kurzen Hauptbecken). Zwei Läufe byte-gleich.
- Die Bilder zeigen das Totholz als braune Linie.
- Das Weltwerkzeug schreibt den Bewuchs in dieselben Feld-Pläne (Ebenen `bewuchs`/`kontakt`, `FT_EL_P2B_*`).

## 4. `lauf_p2.json` und Weltwerkzeug

- Euer Format (§3.1) passt: `i`/`j` werden als Raster erkannt, die Weltlage stimmt mit X = (j − 4730,5)·100 cm, Y = (i − 4060,5)·100 cm, `s` je Punkt (790 Punkte bis 788,37) wird übernommen.
- Neu erkannt wird auch die Spaltenform.
  - Selbsttest: Spline in C2, Rückrechnung gegen den Plan Median 0, p95 3,1 cm.
  - Abtrag 1 452 / Auftrag 91 m³.
  - Zwei Läufe byte-gleich.
- `sohle`, `spiegel`, `tiefe`, `breite` und `marken_s_m` braucht das Werkzeug nicht. Den Spiegel gibt der Plan vor.

## Rückfragen

1. Welches Material nutzen `skjsL_tier_0` und `texndcpda_tier_0` (Megascans-Fab), und haben sie schon eine Nasslinie? Danach richte ich die Lippen-Palette aus (§2.1).
2. Soll die Nasslinie für `M_Master_material` gebaut werden (Kopie wie MS2)? Ich empfehle ja (6d §2).
3. Nanite Foliage in 5.8: Gibt es bei euch die Schalter (Assemblies/Skinning/Voxels)? Wenn ja, schlage ich einen kleinen Test an der Talkaskade vor.

**Quellen** [Suchauszug, Seiten nicht gelesen]:
[CDPR Presse](https://press.cdprojektred.com/news/1778/cd-projekt-red-and-epic-games-present-the-witcher-4-unreal-engine-5-tech-demo-at-the-state-of-unreal-2025),
[PlayStation Blog](https://blog.playstation.com/?p=405351),
[RPG Site](https://www.rpgsite.net/news/17611-the-witcher-4-unreal-engine-5-technical-demo-video-showcased-running-at-60fps-on-base-ps5-with-ray-tracing),
[GameStar](https://www.gamestar.de/artikel/unreal-engine-5-6-state-of-recap,3434063.html),
[GamePro](https://www.gamepro.de/artikel/the-witcher-4-tech-demo-witcher-3-feeling,3433756.html),
[Hitmarker](https://hitmarker.net/news/cd-projekt-red-releases-new-witcher-4-tech-demo-confirms-it-does-not-reflect-the-final-release-3029129),
[Digital Production zu UE 5.7](https://digitalproduction.com/2025/11/12/unreal-engine-5-7-foliage-pcg-and-in-editor-ai/),
[PCGH zu UE 5.7](https://www.pcgameshardware.de/Unreal-Engine-Software-239301/News/Featureset-der-Version-5-6-1486389/),
[80.lv](https://80.lv/articles/picturesque-forest-scene-created-with-ue5-7-s-nanite-foliage).
