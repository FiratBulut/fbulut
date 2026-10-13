# 16h Nachtrag 6d – Antwort 18 §7.7 und §7.9 erledigt; Coast-&-Dunes-Wasser als Vergleich

Stand 13.10. abends. Der Vorrang-Auftrag 6c (natürlicher Bettplan Talkaskade) bleibt offen und geht vor.

## 1. §7.7 Wasser-Materialien inventarisiert

`antworten/fluss_sim/p2_lokal/wasser_material_inventar.json`: 74 Materialien und Instanzen außerhalb `/Game/Eldarien`. Je Eintrag stehen
Pfad, Klasse, Master, Domain, Blend, Shading Model und Texturnamen. Am Projekt wurde nichts geändert.

## 2. Coast & Dunes `MI_Coast_Water_Material` am p2 (nur Speicher, wieder zurück)

Bild `bilder/swr_p2/coast_wasser_cw.jpg` (links unser Stand S6, rechts Coast; t430/t500/t550 Auge).

- **Technik:** läuft auf der SWR (Single Layer Water, `used_with_water`), anders als Rural Australia (Deckkraft aus gemalter Maske → unsichtbar).
- **Look:** klares Türkis wie ein Pool, Steine erscheinen mintgrün. Die Oberfläche ist **ruhiger** als unsere (weniger „Quecksilber“-Schlieren).
- **Werte der Instanz:**
  - Absorption (10, 150, 350, 8). Unser F: (222, 1000, 1250, 8).
  - Scattering (1, 1, 1, 0,5); Water Albedo (0,85, 0,85, 0,85).
  - Water Roughness 0,02; Water Specular 0,225; Refraction 1,15.
  - Default Near Normal Strength 0,25; Distant 0,3 / B 0,25; Far Normal Fresnel Power 9.
  - Fluidsim Normal Strength 1,0; Sim Velocity Normal Strength 40; River Normal Flatness 0,5; WPO Flowmap 6.
  - Schalter: Enable River aus, Enable Waves an, Caustics aus.
- **Frage:** Welche Oberflächenwerte (Normalen, Rauheit) sollen wir auf `MI_EL_SWR_Klar` übertragen? Die dunkelbraune Farbe (S6) bleibt.

## 3. §7.9 Helle Steine unter Wasser

**Messung der Albedo:** mittlere Luminanz Y (linear) der Grundfarb-Textur × Helligkeits-Parameter der Instanz
(`antworten/fluss_sim/p2_lokal/stein_albedo.json`). Zum Vergleich: Bachbett unter Wasser misst 0,067 (BaseColor-Messung t500), trockener Kies 0,129.

| Netz (Bachdekor) | Y | ganz unter Wasser | teils |
|---|---|---|---|
| `SM_mountain_rock_small_01_1…5` (Mountain, Kopf-/Bachstein) | **0,229** | 1 370 | 295 |
| `SM_SmallStonesPack_*` (11 Varianten, Kiesel/Stein) | **0,125** | 4 505 | 747 |
| `SM_flat_rock_03`, `SM_ground_rock_03_01`, `SM_SmoothRockShelf_01` (Platten) | 0,16–0,18 | 5 | 9 |
| dunkle Steine und Hölzer (Y < 0,10) zusammen | 0,04–0,09 | 92 | 182 |

Zusammen liegen **5 886 helle Steine ganz unter Wasser** und nur 92 dunkle (`antworten/fluss_sim/p2_lokal/helle_steine_p2.json`).
Die hellen „Laub“-Flecken in G0–G4 sind also vor allem diese Kleinsteine, nicht die Platten.

**Test SD0/SD1** (`bilder/swr_p2/steine_dunkel_sd0_sd1.jpg`, nur Speicher): Helligkeit `SmallStonesPack` × 0,55 und `mountain_rock` × 0,30
ergeben Y ≈ 0,069. Die Flecken werden zu dunklen Bachsteinen; unter dem braunen Wasser wirken sie etwas orange.

**Eingebaut (gespeichert, C2 + D2):**
- **Aufteilung:** Jeder dieser Kleinsteine, dessen Mitte unter dem **gebackenen SWR-Spiegel** + 3 cm liegt, wandert in einen eigenen Typ
  `FT_EL_BACH_<Netz>_Nass` (`scripts/swr/nass_steine_split_p2.py`). Spiegel je 1-m-Zelle, am Wasserrand Median der nassen Nachbarn.
- **Ergebnis:** C2 8 057 von 8 527 Steinen, D2 1 783 von 2 246, zusammen **9 840**.
  - Eine erste Fassung mit dem Plan-Spiegel aus `lauf_p2.json` erfasste nur 6 704. Der Plan-Spiegel ist alle ~3 m linear und schneidet die Stufen
    schräg; in den Becken vor einer Lippe liegt er bis 0,5 m zu tief. Außerdem kennt er den Ost-Arm nicht.
  - Die Steinmitten liegen im Median 0,39 m unter dem SWR-Spiegel. Fast alle Bachdekor-Kleinsteine liegen also im Wasser, auch weil das
    Wasser heute über die Ufer läuft (6b).
- **Dunkle Material-Kopien:** `MI_EL_Nass_SmallStonesPack_01` (Helligkeit 0,55) und `MI_EL_Nass_mountain_rocks_small_01` (Base Brightness 0,30).
  Der Setzer übernimmt das Material jetzt aus dem Plan (`"material"` je Datei). Trockene Steine bleiben unverändert.
- **Bilder:** `bilder/swr_p2/steine_dunkel_sd0_sd4.jpg`. Die meisten Flecken sind weg; bei t500 bleiben 4–5 helle.
- **Die übrigen hellen Steine gehören zu anderen Ebenen** (Zählung in der SWR-Nassmaske):
  - `FT_EL_UF_*`: 917 `SmallStonesPack` (Ufer-Steine aus Auftrag 152, entlang der alten Gewässer);
  - `FT_EL_HEID_*`: 82 `SmallStonesPack` (Heide-Bodenschicht).
  - Nach euren Bachdekor-Regeln (`bestand_im_wasser_bleibt`: ufer, felsschalen) bleiben sie als Steine im Bett. Wir haben sie nicht entfernt.
  - Sie benutzen dasselbe `MI_EL_SmallStonesPack_01`. Die Nasslinie (§4.2 eurer Antwort), umgehängt an diese MI, würde sie mit abdunkeln.
- Nach dem neuen Bettplan (6c) rechnet der Bachdekor-Planer neu; dann wiederholen wir die Aufteilung (Werkzeug liegt bereit).

**Fragen:**
1. Soll der Bachdekor-Planer unter Wasser lieber eine eigene Palette nutzen (dunkle Kopfsteine, Kies) statt der Abdunklung?
2. Sind 0,069 richtig, oder sollen die Steine heller als das Bett bleiben (z. B. 0,08–0,09), damit sie als Steine lesbar bleiben?
3. Die Nasslinie (§7.11, Kopie `M_EL_Fels_MS2`) ist in Arbeit. Sie würde `SmallStonesPack` (Master `M_EL_Fels_MS`) pixelgenau abdunkeln,
   `mountain_rock` (Master `M_Master_material`) aber nicht. Reicht die Aufteilung dort, oder bekommt auch dieser Master eine Nasslinie?

## 4. Antwort 16h-N6 (8a746d9) – erste Schritte erledigt, Rückfragen

**§6.1 Endstand gesetzt und gespeichert** (`MI_EL_SWR_Klar`): Water Roughness 0,025, Sim Velocity Normal Strength 5, Refraction 1,10; ELD-Wirbel
bleiben 0, Fluidsim Normal Strength 1, Default Near 0,25. Bild `bilder/swr_p2/endstand_e16.jpg` (links SD4 = S6 + dunkle Steine, rechts E16):
der Unterschied ist klein, das Wasser etwas ruhiger und schärfer; keine Rückschritte.

**Rückfrage 1 – BaseColor bei S6 (+ dunkle Steine), Draufsicht 48 m, Y linear, Median:**

| Stelle | Grund unter Wasser | nasses Band | trockener Kies | Stein nass | Stein trocken |
|---|---|---|---|---|---|
| s 430 | 0,057 | 0,055 | 0,109 | 0,058 | 0,065 |
| s 500 | 0,054 | 0,055 | 0,123 | 0,058 | 0,062 |
| s 550 | 0,063 | 0,058 | 0,114 | 0,068 | 0,060 |

- „Stein“ = Bildpunkte, die > 3 cm über dem Gelände liegen und nicht grün sind; „trocken“ = Gelände > Spiegel + 0,2 m. Das Band 10–90 % ist
  breit (0,01–0,21), weil Schatten und Moos hineinspielen. Die trockenen Steine liegen mit 0,06 unter eurem Ziel 0,13–0,22 – vermutlich
  Schatten und Moosflecken am Ufer; nicht als Aufhellungsbedarf lesen.
- Grund unter Wasser 0,054–0,063 statt 0,067 vor S6 (die Messung bei S6 lag schon vor; die Steine ziehen den Wert jetzt mit).

**Rückfrage 2 – Stein-Material:** `MI_EL_SmallStonesPack_01` → Master `M_EL_Fels_MS` (unser Megascans-Ersatz). Regler: `Helligkeit`, `Farbe`
(Vektor), `Toenung` (Vektor), `Rauheit`, `Specular`, `Normal_Flach`, `Variation`, `Durchscheinen`, **`Nass_Weich` 15, `Nass_Dunkel` 0,55**
(vorhandene Nässe-Regler – was sie genau tun, prüft der Nasslinien-Agent im Graph), Wind. Texturen Albedo/Normal/DpRF.
`SM_mountain_rock_small_01_*` → `M_Master_material` (Mountain-Paket): `Base Brightness`, `Normal Power`, `Detail *`, `Specular Value`, RVT-Blend.
Die Bachdekor-Steine sind **Foliage-Instanzen** (FFoliageInfo in InstancedFoliageActors, HISM), keine Akteure. Per-Instanz-Daten gingen nur
über `NumCustomDataFloats` am Foliage-Typ + Instanz-Custom-Data; unser Setzer schreibt das nicht. Deshalb die Aufteilung in `_Nass`-Typen (§3).

**Rückfrage 3 – `Caustics`-Schalter:** Test läuft (CS1 bei t430/t500/t550), Ergebnis im nächsten Nachtrag.

**Rückfrage 4 – Rural Australia, Konstanten-Test:** nicht nötig. **Auf dem Elfenwald-See (WaterBodyLake `S_R_P3_M1_00`, G3/G4, 72 000 m²) ist
die RA-Kopie sichtbar** (`bilder/swr_p2/elfenwald_see_ra_sr0_sr1.jpg`), nur auf dem SWR-Fluss war sie unsichtbar. Das stützt Ursache 1
(Maske/UV auf dem Flussnetz der Water Zone) oder 2 (Ufer-Ausblendung über die Tiefe: Bach 0,47 m, See 1,4 m). Ferat wollte den See damit
sehen; Varianten `elfenwald_see_ra_varianten.jpg` (ohne Kaustik, Rauheit 0,3). Befund: wirkt als ruhiger Spiegel-See; der weiße Streifen am
Ufer ist der helle Kiesrand der Landschaft (V12 „helle Kiesufer“), nicht das Wasser (bleibt bei Deckkraft 0,85 gleich). Graph der RA-Datei:
`antworten/fluss_sim/p2_lokal/rural_australia_m_water_01_graph.json`. **Ferat 20:30: See auf die To-do-Liste, zuerst der Bach.** Nichts gespeichert.

**Nächste lokale Schritte (eure §6):** 3 Grund-Ton ab 0 cm (Agent schreibt `ue_landschaft_v18b_bachton.py`), 4 Nasslinie (Agent, mit euren
Werten §4.2), 5 V20a (Agent schreibt `ue_wasser_v20a.py`, Kopie des Masters). 6c (Bettplan) bleibt der Vorrang.
