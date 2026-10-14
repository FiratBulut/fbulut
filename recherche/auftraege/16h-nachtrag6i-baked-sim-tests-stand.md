# 16h Nachtrag 6i – Tests aus 6h §5 und 6g: BAKED_SIM zeichnet wie live; Stand der Umsetzung 20/21/19

Stand 14.10.2026, 23:15 (PC-Uhr). Ferat schläft. Antworten 6g, 6h (+§5), 19, 20, 21 sind gelesen und in Arbeit.

## 1. Tests 6h §5.2 am gebackenen Erlenbach p2 (gleiche Kameras m_talkaskade / t430 / t500 / t550, alles nur im Speicher)

Bilder: `bilder/swr_p2/baked_sim_test0_p2n0.jpg` (links WCBS heute = P2NA, rechts Test 0 = P2N0), `bilder/swr_p2/wcbs_tests123_p2n.jpg`
(Spalten: P2NA Referenz, P2N1 Test 1, P2N2 Gegenprobe, P2N3 Test 3).

| # | Test | Ergebnis |
|---|---|---|
| 0 | `render_state` = **BAKED_SIM** | **Wasserkörper wie live:** Becken grün-türkis gefüllt bis zur Kante, Stufen mit Körper, Schaum an Lippen, Grund nah sichtbar – praktisch das P2L-Bild. WCBS daneben: braunes Bett, kaum Wasserfläche. Kein Reset/Bake nötig, Umschalten sofort. |
| 1 | MI `UseFixedWaterDepth` = True (WCBS) | kein sichtbarer Unterschied zu P2NA |
| 2 | Gegenprobe Absorption 2/2/2 (WCBS) | Wasser wird **schwarz-deckend** (Becken und Rinne) → die Koeffizienten kommen im WCBS-Weg an; der Wasserkörper ist dort nur so dünn/flach, dass bei 222/1000/1250 nichts färbt |
| 3 | `r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames 10` | kein Unterschied |
| 5 | Material-Pfad: `SW_Water_Material_River_Niagara` → `SW_Water_Material_River` → `SW_Water_Material` | Blend **Masked**, Shading **SingleLayerWater** – identisch mit `M_Eldarien_Wasser_Schaum8` (Masked, SLW). Ursache 5 (anderes Shading) scheidet aus. |
| 2 (Fläche) | Messlatte | nicht gemacht; Test 0 macht sie entbehrlich |

**Entscheidung (umgesetzt, gespeichert in der Nachtkette):** Erlenbach p2 läuft dauerhaft mit `render_state` BAKED_SIM
(`SWR_Sim_F_ERLENBACH_1V_C2`), Material unverändert MI_EL_SWR_Klar (Werte F). Nach jedem neuen Bake wird BAKED_SIM wieder gesetzt.
Folgerung aus Test 2: Im WCBS-Weg liegt die gezeichnete Wasserfläche fast auf dem Boden (Wasser-Info-Höhe), das Gebackene zeichnet die
Simulationshöhe – das ist eure Ursache 2 (Fläche zu tief/dünn), nicht die Maske (1) und nicht veraltete Info (3).

**Fragen:** (a) BAKED_SIM im Spiel: Bitte, was zu Kosten (0,3 ms + 3 Dispatches laut 16b) und zur Darstellung im gepackten Build belegt ist;
wir testen in PIE (`karte/pie_test.py`). (b) Regel §5.4: Gilt sie so – BAKED_SIM nur an ≤ 3 Schaustellen, Rest WCBS? Oder lohnt ein Weg, die
WCBS-Fläche auf die Simulationshöhe zu bringen (Zonenauflösung ist schon 0,29 m/Pixel; die Fläche selbst scheint nicht die Sim-Höhe zu nehmen)?
(c) Ist bekannt, ob `render_state` zur Laufzeit per Blueprint/Python umstellbar ist (5.3 Test läuft bei uns morgen in PIE)?

## 2. 6g Rückfrage 1 – Band 0,25–2 m der Talkaskade, nass je Tiefenschwelle (Dump dichte Spline 22:30)

| Schwelle | 1 cm | 2 cm | 5 cm | 10 cm |
|---|---|---|---|---|
| Band nass | 83,0 % | 78,6 % | 65,1 % | 45,9 % |
| Bett nass | 100 % | 100 % | 99,9 % | 97,8 % |

Bei > 10 cm immer noch 46 % → das ist kein grauer Film, sondern echtes Wasser neben dem Bett. Eure Erwartung „bei > 5 cm nur 20–30 %“ trifft
nicht zu. Bett-Median 0,34 m, p90 0,60 m.

## 3. 6g Rückfrage 2 – Rechenfläche der SWR (Antwort aus unserem Code, Bericht `auftraege/daten/swr_teilung_plan_lokal.md`)

- Unser Bauwerkzeug setzt die Rechenfläche **nicht**: `rechteck(P)` ist nur eine Vorhersage (Hülle der Spline-Punkte ± halbe Breite), daraus
  kommt allein `resolution_max_axis`. Die SWR wird per `spawn_actor_from_class` an der Rechteckmitte gesetzt, ohne Scale/Box.
- Engine-Header `ShallowWaterRiverActor.h` (5.8): keine editierbare Bounds-Property; `WorldGridSize`/`SystemPos` sind private, in `Rebuild()`
  aus den **Quell-Wasserkörpern** berechnet. Nachrechnung aus lauf_p2: 116,9 × 741,6 m gegen Dump 116,8 × 739,9 m – Modell bestätigt.
- **Folge:** Variante B wörtlich (drei SWR auf demselben WaterBodyRiver) ergibt dreimal das 740-m-Rechteck, kein Gewinn. Ohne Codeänderung geht
  nur je Teil ein eigener Quell-Fluss → wir testen heute Nacht **Variante C light**: drei Spline-Kopien des Flusses (T00 s 0–393, T01 385–583,
  T02 575–788 + Ost-Arm; Original versteckt, Prioritäten 12/11/11), je eine SWR mit `resolution_max_axis` 2048 → Zellen 0,186 / 0,090 / 0,098 m.
  Der Bach mäandert (Rechtecke 53–94 m breit statt eurer 30 m) → T01/T02 ≈ 1,5–2,0 Mio. Zellen (2,4–3× heute; Rückfall 1024 → 0,18/0,20 m).
  Nähte 387/393 und 576/582 (6 m Überlappung). Messung: vereinigtes 1-m-Raster, Naht-Spiegelsprung, Prüfband bei 1/2/5/10 cm, Bilder P2T.
  Ergebnis folgt (6j). **Frage:** Spricht aus eurer Sicht etwas gegen drei Flusskopien übereinander (Wasser-Info der Zone, Zeichnen des
  versteckten Originals)? Bitte Prüfpunkte.

## 4. Stand Antwort 20 (Uferplan Talkaskade) – lokal umgesetzt, Setzen läuft in der Nachtkette

- Alle vier Skripte laufen lokal mit 1-m-Daten byte-gleich zum Repo (Gelände-Hash f274fd1b66d7 = eingebaut, Delta max 0,000 m → nicht neu geschrieben).
- Datensätze: Bettplan neu 645/149, Detailgrad **7 659 Instanzen / 545 Kollision, 47 Netze** (Kürzel bei uns DETA → `FT_EL_DETA_*`, nicht DG).
  z neu auf dem eingebauten Gelände gerechnet (eure z lagen an Böschungen bis 1,23 m daneben: Delta der nächsten Zelle statt Ist-Höhe; 2 811 > 10 cm).
- **Material:** 21 vorgeschlagene MIs fehlen (6 455 Instanzen): alle `MI_EL_NL_*` – **`M_EL_Mountain_NL` existiert bei uns nicht** (es gibt
  M_EL_Fels_MS2/MSR, M_EL_Fels_Auflage, M_EL_Klippe_RVT; Mountain-Netze zeigen ihr Paketmaterial), Fab `MI_EL_<id>_tier_0` (nur Klippe_xjijbgx da),
  Namaqualand grau (nur Wüsten-MIs), 4 `_trocken`-Kopien. Gesetzt wird zunächst mit Paketmaterial bzw. vorhandenen MS2-Instanzen (1 204 Instanzen).
  **Frage:** Nasslinie für Mountain-/Fab-Netze – lieber je Paket-MI eine MS2-Kopie mit deren Texturen (Albedo/Normal/ORM-Belegung prüfen) oder ein
  neuer Master `M_EL_Mountain_NL` aus dem Mountain-Paketmaster + MF_EL_Nasslinie? Bitte Vorgabe (Parameterliste), wir bauen.
- Befund: gebackener Spiegel liegt 0,15–0,25 m über dem Plan-Spiegel und 1–2 m über die Plan-Bettkante hinaus → 46 % der Instanzmitten unter
  dem gebackenen Spiegel (Kante 1 702/2 496). Steine werden gesetzt, Bewuchs (§5 Schritt 6) erst nach korrigiertem Bake (Teilung).
- Rückfrage 1: Slab X = lange Achse 7,15 m, Pivot an der Y-Kante (Körper nur +Y, 3,45 m); Rocky-Grounds mittig, X lang. `yaw_rel` ±90/`kipp` > 0 =
  Nase nach unten stimmt mit unserer Konvention; Slab-Versatz 1,55 m × Skala entlang +Y beachten. Rückfrage 2: volle Dichte nur Talkaskade.
  Rückfrage 3: keine `MI_EL_NL_*`. Rückfrage 4: Unterordner helfen bei unserem Setzer nicht (keine Rollenauswahl; alles in einem Lauf).

## 5. Stand Antwort 21 (Pilot B5-Ost) – lokal vorbereitet, Einbau läuft in der Nachtkette

- Planer lokal mit 1-m-Daten: **6 881 Instanzen + 7 Akteure** (Cloud 2 m: 6 471), 46 Netze, alle .uassets da; Prüfer: Deckung Halde 79 %, Schrofen
  61 %, Wand 83 %; 1 FEHLER (Gratgruppe 4 statt ≤ 3 Bäume, kosmetisch). Lokale Masken 481 × 501 (Cloud 482 × 502).
- Lagen: Geröll/Fels/Felsplatte = max(alt, ziel) über die Sehens-Kette (178 565 Zellen, 20 Komponenten). **Rückfrage 3:** Gras hängt bei uns nicht
  an den Lagen, sondern an den Bewuchskarten `v_*.r8` (≈ 2,3 m/Texel) → Grasdichte-Maske als Faktor auf v_gras_berg/v_kraut/v_heide, dann
  Texturen + Gras-Karten neu. Rückfrage 2: `remove_foliage_by_mask` = Wert ≥ 128 entfernen, Filter Netz|Typ mit „!“-Ausschluss, keine
  Sicherung → eigenes Skript mit Sicherung je Instanz (zaehlen/sichern/entfernen/zurueck). Rückfrage 5: 493 kleinste ohne Kollision ok.
  Rückfrage 8: Variante B verworfen. Rückfrage 1: Pivot der Bandnetze an der −Y-Seite (Bounds) → Prüfung in K3 folgt.
- Pixelmessung (6h §2): Werkzeug gebaut (`ue_pixel_messung.py`, zwei Wege: SceneDepth + Ausblenden je Klasse (Vorgabe) oder CustomDepth-Stencil;
  Gras = Klasse 4 getrennt, drei Lesarten; Wasser Klasse 5; Auswertung offline mit Zusammenhangsflächen). Trockenlauf 96/96. Erste echte Messung
  B5P heute Nacht, Eichung an RA2 danach.
- Raw-8K-Sätze (xf3odif, xfplcbf, xjijbgx, ukjhcamga; 15 Texturen, 1,26 GB) werden vor dem Setzen auf 4K geklemmt.

## 6. Stand Antwort 19 (Bachanfänge) – vorbereitet, wartet auf Ferat

- Plan ↔ Daten: 162 IDs, 0 fehlend, alt_punkte 0 Abweichungen. Anwendung (Trockenlauf): 161 Änderungen auf 155 Gewässer, Punkte 3 712 → 4 427,
  Verlängerung Köpfe 1 036 m, Breite Punkt 0 Median 4,0 → 0,4 m, 0 FEHLER, 21 Warnungen (27 Punkte > 30 cm schwebend in Endpfanne/Moorwiese/K1;
  9 Gewässer springen am Ende des Anfangsbereichs auf die Houdini-Breite ×1,5–2,2, z. B. B_R2_R_P3_P1_05 1,9 → 4,0 m – bitte Profil über L hinaus
  weich auslaufen lassen?). Instanzen 1 713 in 28 Feldern, alle Netze da. Eure Rückfragen 1–9 liegen Ferat als Entscheidungsvorlage vor
  (Empfehlung: 1 ja 0,4 m; 2 ja nur Anfangsbereich; 3 Kar-Tümpel 270 m²; 4 ja; 5 so lassen, Abtrag ≤ 1,5 m; 6 K1 eigener Abschnitt, SWR zuerst; 7 Sickerquelle;
  9 Schwelle 1,0 m). Die drei Beispielfälle (G6/I6) bauen wir nach seinem Ja.

## 7. Bitte

1. §1 (a)–(c): BAKED_SIM im Spiel, Regel, Laufzeit-Umschalten.
2. §3: Prüfpunkte für drei Flusskopien (Variante C light), bevor wir das Ergebnis speichern.
3. §4: Vorgabe Nasslinien-Material für Mountain-/Fab-/Namaqualand-Netze (Masterwahl, Parameter).
4. §6: Auslauf des Breitenprofils bei Houdini-Sprung.
