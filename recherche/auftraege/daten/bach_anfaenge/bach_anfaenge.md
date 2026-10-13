# Bach- und Flussanfänge – Prüfung (13.10.2026)

Ferat (13.10. 21:00): „Prüfe die River-Splines, vor allem wo ein Bach startet – nicht, dass er aus dem Nichts auftaucht.“ Messlatte Witcher 4: Anfang sichtbar begründet (Mulde/Fels/Moos, Seeabfluss, Schneefeld, Zusammenfluss) und schmal.

Werkzeug: `python -I scripts/wasser/bach_anfaenge.py` (offline, nur Weltdaten, ~1 min). Daten: `wasser_welt.json` (Flüsse), `baeche/baeche_alle.json` (Bäche R1–R3), Erlenbach p2 (`lauf_p2.json`), SWR-Arm Ost (`arm_ost_pfad.json`), Seen/Teiche, `hoehe.f32`, `lage_*.r8`, `eigner.r8` (Biom = Houdini-Kachel-Rezept). Ausgelassen (im Editor ersetzt): F_ERLENBACH_1V_C2, F_ERLENBACH_1_C2, F_ERLENBACH_2_C2, B_R3_K10_TUNDRA_01.

**Format-Befund:** Punkte `[X, Y, Z, Breite, Tiefe, Tempo]` in cm (Tempo cm/s); Punkt 0 = oben (Spiegel fällt in Fließrichtung; 0 Gewässer mussten gedreht werden). Seen/Teiche: `umriss` cm, `spiegel_cm`. p2: 1-m-Linie i/j/s/sohle/spiegel/tiefe/breite in m (Spline-Band im Editor = Bett + 2 m). Flussabschnitte desselben Flusses überlappen an Feldgrenzen (Anfang liegt bei 78–97 % des Vorgängers) → „Fortsetzung“, kein Fehler.

## Summen

| Klasse | Bedeutung | Anzahl | davon Anfang > 1,5 m |
|---|---|---|---|
| e | aus dem Nichts | 43 | 43 |
| d | Quellmulde/Hangfuß Fels | 93 | 93 |
| c | Gletscher/Schnee | 7 | 7 |
| b | Abzweig/Fortsetzung/Zusammenfluss/Lücke/Wasserfall | 47 | 47 |
| a | Seeabfluss | 3 | 3 |
| | **gesamt** | **193** | **193** |

Unterarten: a/seeabfluss 3, b/abzweig 11, b/fortsetzung 16, b/luecke 2, b/wasserfall 3, b/zusammenfluss 15, c/biom 4, c/schnee 3, d/mulde 93, e/- 43.

Echte Anfänge (ohne Fortsetzungen): 177 – davon > 1,5 m breit: 177, ohne Verjüngung: 115.

Enden: fortsetzung 88, meer 18, nichts 59, see 6, zusammenfluss 22.

Anfänge ohne Verjüngung (Breite Punkt 0 ≥ Breite nach 20 m, > 0,6 m): 125 von 193. Fließgewässer geprüft: 193 (Flüsse 24, Bäche 167, SWR 2); stille Gewässer: 78 (Seen 65, Teiche 13).

Schwere = Klasse (e 100, schwache Mulde 60, c ohne Schnee 45, d 40, c 30, Lücke 30, Zusammenfluss mit Breitensprung 25, Abzweig 20, a 5, Fortsetzung 0) + 10 × Anfangsbreite [m] + 10 ohne Verjüngung + 5 wenn das Ende versickert (Fortsetzung/Seeabfluss höchstens 15).

## Die 20 schlimmsten Fälle mit Vorschlag

### 1. F_CANYONBACH_D4 – Klasse e (-), Schwere 620

- Feld **D4**, Anfang X -1156.7 / Y -285.5 m (cm -115670 / -28553), Spiegel 25.70 m, Boden 24.42 m (Spiegel über Boden 1.28 m), Länge 282 m.
- Breite Anfang **51.0 m**, nach 20 m 43.3 m, Verjüngung: nein; Gefälle erste 20 m: Spline 0.0 %, Boden 0.0 %.
- Lage Trockengras 53%, Erde 27%, Sand 9%; Biom canyon (K3_CANYON); Mulde 0/4 (Anstieg [0.26, 0.03, 0.01, 0.09] m), Fels hangauf 0 %, Geröll 7 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See T_-1344_-574 330 m; Fließgewässer F_CANYONBACH_D5 252 m (Mittellinie). Ende: Fortsetzung: F_CANYONBACH_D5 (Mittellinie 0.0 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Ein 51 m breiter Fluss beginnt aus dem Nichts (Lage Trockengras). Zwei Wege: (1) Quellsee: mit dem Water-Brush ein Becken 40–60 m (Blend Min) am Anfang eingraben und als WaterBodyLake anschließen; (2) Anfang 150–250 m hangauf ziehen und stufig verjüngen 51 → 6 → 2 m, die obersten 50 m als Bach 0,5 m in Mulde/unter Fels (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)).

### 2. F_DSCHUNGELFLUSS_H5 – Klasse e (-), Schwere 600

- Feld **H5**, Anfang X 3296.6 / Y 872.8 m (cm 329657 / 87284), Spiegel 6.54 m, Boden 5.99 m (Spiegel über Boden 0.55 m), Länge 151 m.
- Breite Anfang **49.0 m**, nach 20 m 48.3 m, Verjüngung: nein; Gefälle erste 20 m: Spline 0.0 %, Boden 0.0 %.
- Lage Gras 72%, Schlamm 20%, Laub 5%; Biom sumpf (K5_SUMPF); Mulde 2/4 (Anstieg [0.12, -0.02, 1.55, 0.83] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See T_3313_789 72 m; Fließgewässer F_DSCHUNGELFLUSS_H6 102 m (Mittellinie). Ende: Fortsetzung: F_DSCHUNGELFLUSS_H6 (Mittellinie 0.0 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Ein 49 m breiter Fluss beginnt aus dem Nichts (Lage Gras). Zwei Wege: (1) Quellsee: mit dem Water-Brush ein Becken 40–60 m (Blend Min) am Anfang eingraben und als WaterBodyLake anschließen; (2) Anfang 150–250 m hangauf ziehen und stufig verjüngen 49 → 6 → 2 m, die obersten 50 m als Bach 0,5 m in Mulde/unter Fels (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)). Nächster See T_3313_789 nur 72 m entfernt → Weg (1) über diesen See.

### 3. F_HAUPTFLUSS_3_C4 – Klasse e (-), Schwere 580

- Feld **C4**, Anfang X -2614.7 / Y -63.7 m (cm -261465 / -6367), Spiegel 42.80 m, Boden 41.71 m (Spiegel über Boden 1.09 m), Länge 135 m.
- Breite Anfang **47.0 m**, nach 20 m 38.3 m, Verjüngung: nein; Gefälle erste 20 m: Spline 17.5 %, Boden 0.2 %.
- Lage Kies 99%, Nadeln 1%; Biom aue (R_M1_P0); Mulde 2/4 (Anstieg [-0.15, 1.67, -0.08, 1.02] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar; Vorgänger F_HAUPTFLUSS_2_B4 endet 570 m entfernt, 156 m höher (Strecke dazwischen ohne Epic-Wasser). Nächste Gewässer: See S_R_M1_P0_00 455 m; Fließgewässer F_HAUPTFLUSS_3_C5 105 m (Mittellinie). Ende: Fortsetzung: F_HAUPTFLUSS_3_C5 (Mittellinie 0.0 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Ein 47 m breiter Fluss beginnt aus dem Nichts (Lage Kies). Zwei Wege: (1) Quellsee: mit dem Water-Brush ein Becken 40–60 m (Blend Min) am Anfang eingraben und als WaterBodyLake anschließen; (2) Anfang 150–250 m hangauf ziehen und stufig verjüngen 47 → 6 → 2 m, die obersten 50 m als Bach 0,5 m in Mulde/unter Fels (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)).

### 4. F_HAUPTFLUSS_2_B4 – Klasse b (luecke), Schwere 405

- Feld **B4**, Anfang X -3081.5 / Y -568.7 m (cm -308152 / -56871), Spiegel 206.56 m, Boden 205.70 m (Spiegel über Boden 0.86 m), Länge 120 m.
- Breite Anfang **37.0 m**, nach 20 m 40.0 m, Verjüngung: schwach; Gefälle erste 20 m: Spline 2.5 %, Boden 0.0 %.
- Lage Kies 100%; Biom bergwald (K1_WASSERFALL_WEST); Mulde 0/4 (Anstieg [-0.01, 0.09, -0.02, 0.2] m), Fels hangauf 1 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: Lücke zum Vorgänger F_HAUPTFLUSS_1_B4: endet 133 m entfernt, 76 m höher (Schlucht/Wasserfall/Houdini-Netz?). Nächste Gewässer: See S_R_M1_M1_01 966 m; Fließgewässer F_HAUPTFLUSS_1_B4 133 m (Mittellinie). Ende: versickert im Nichts (nächste: See S_R_M1_M1_01 917 m, B_K1_WASSERFALL_WEST_03 219 m). Flags: breit>1,5m, Ende versickert, Lücke 133 m.
- **Vorschlag:** Lücke zum Vorgänger prüfen (F_HAUPTFLUSS_1_B4, 133 m, 76 m Höhe): liegt dort noch ein Houdini-Wassernetz/Wasserfall? Wenn nicht: Vorgänger als Kaskade/Wasserfall-Fluss bis hierher verlängern (Muster kaskaden_k8_k10a.md) oder Anfang bis zum Vorgänger-Ende hochziehen.

### 5. F_HAUPTFLUSS_1_B4 – Klasse e (-), Schwere 325

- Feld **B4**, Anfang X -3189.9 / Y -690.1 m (cm -318990 / -69011), Spiegel 288.15 m, Boden 287.43 m (Spiegel über Boden 0.71 m), Länge 30 m.
- Breite Anfang **21.0 m**, nach 20 m 21.0 m, Verjüngung: nein; Gefälle erste 20 m: Spline 17.7 %, Boden 0.2 %.
- Lage Kies 100%; Biom bergwald (K1_WASSERFALL_WEST); Mulde 2/4 (Anstieg [-0.11, 2.32, -0.12, 3.56] m), Fels hangauf 11 %, Geröll 18 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_M1_M2_00 1011 m; Fließgewässer F_HAUPTFLUSS_2_B4 163 m (Mittellinie). Ende: versickert im Nichts (nächste: See S_R_M1_M2_00 1012 m, F_HAUPTFLUSS_2_B4 133 m). Flags: breit>1,5m, keine Verjüngung, Ende versickert.
- **Vorschlag:** Ein 21 m breiter Fluss beginnt aus dem Nichts (Lage Kies). Zwei Wege: (1) Quellsee: mit dem Water-Brush ein Becken 40–60 m (Blend Min) am Anfang eingraben und als WaterBodyLake anschließen; (2) Anfang 150–250 m hangauf ziehen und stufig verjüngen 21 → 6 → 2 m, die obersten 50 m als Bach 0,5 m in Mulde/unter Fels (SM_MossyForestBoulder_01 (1.7×1.0 m), SM_MossyForestBoulder_03 (2.0×1.3 m), SM_MossyForestBoulder_04 (3.3×2.0 m)).

### 6. F_ELFENFLUSS_1_H4 – Klasse b (wasserfall), Schwere 325

- Feld **H4**, Anfang X 3084.6 / Y -695.4 m (cm 308456 / -69544), Spiegel 127.72 m, Boden 126.94 m (Spiegel über Boden 0.78 m), Länge 194 m.
- Breite Anfang **32.0 m**, nach 20 m 34.3 m, Verjüngung: schwach; Gefälle erste 20 m: Spline 6.8 %, Boden 0.1 %.
- Lage Kies 100%; Biom elfenwald (K8_ELFENFALL); Mulde 0/4 (Anstieg [0.38, -0.05, -0.01, 0.11] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: Wasserfall WF_K8 in 46 m. Nächste Gewässer: See T_2719_39 802 m; Fließgewässer F_ELFENFLUSS_2_H4 181 m (Mittellinie). Ende: Fortsetzung: F_ELFENFLUSS_2_H4 (Mittellinie 0.0 m). Flags: breit>1,5m.
- **Vorschlag:** Wasserfall-Fuß: Becken + Gischt vorhanden lassen; Breite am Beckenausgang prüfen.

### 7. F_GLETSCHERTAL_D2 – Klasse c (biom), Schwere 302

- Feld **D2**, Anfang X -740.2 / Y -2656.1 m (cm -74024 / -265611), Spiegel 90.58 m, Boden 90.29 m (Spiegel über Boden 0.29 m), Länge 59 m.
- Breite Anfang **25.7 m**, nach 20 m 38.2 m, Verjüngung: ja; Gefälle erste 20 m: Spline 0.4 %, Boden 0.0 %.
- Lage Geroell 80%, Trockengras 8%, Moos 6%; Biom gletscher (K7_GLETSCHER); Mulde 2/4 (Anstieg [0.58, -0.08, 0.07, 0.85] m), Fels hangauf 0 %, Geröll 80 %, Schnee/Eis 0 %.
- Befund: Gletscher/Schnee: Schnee+Eis 0 % in 20 m, Biome ['gletscher']. Nächste Gewässer: See S_K7_GLETSCHER_00 58 m; Fließgewässer B_R_P0_M2_01 407 m (Mittellinie). Ende: See: S_K7_GLETSCHER_00 (1.1 m). Flags: breit>1,5m, kein Schnee/Eis in 20 m.
- **Vorschlag:** Gletscher-Biom, aber kein Schnee/Eis am Anfang: Gletschertor bauen – Eis-/Schneefeld (Megascans Eis/Schnee, Lage Eis/Schnee 30 × 30 m schreiben) direkt über dem ersten Punkt, Wasser tritt unter der Eiskante aus; Breite dort halbieren (25.7 → 12.8 m) und erst über 50 m auf volle Breite.

### 8. F_ERLENBACH_2_D3 – Klasse b (abzweig), Schwere 290

- Feld **C3**, Anfang X -1707.1 / Y -2004.6 m (cm -170707 / -200456), Spiegel 36.13 m, Boden 35.26 m (Spiegel über Boden 0.87 m), Länge 191 m.
- Breite Anfang **26.0 m**, nach 20 m 25.6 m, Verjüngung: nein; Gefälle erste 20 m: Spline 2.0 %, Boden 0.0 %.
- Lage Wiese 66%, Trockengras 20%, Moos 8%; Biom tundra (K10_TUNDRA); Mulde 3/4 (Anstieg [0.63, 0.72, -0.0, 0.69] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: Abzweig von F_ERLENBACH_2_C3 (Mittellinie 0.0 m, dort 26.0 m breit, bei 67 % seiner Länge). Nächste Gewässer: See S_K10_TUNDRA_03 150 m; Fließgewässer F_ERLENBACH_2_C3 0 m (Mittellinie). Ende: Fortsetzung: F_ERLENBACH_2V_D3 (Mittellinie 0.0 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Abzweig: Ufer am Abzweig mit Kies/Steinen betonen; Breite am Abzweig ≤ 60 % des Hauptlaufs.

### 9. B_R_P3_P1_03 – Klasse e (-), Schwere 223

- Feld **G6**, Anfang X 1499.5 / Y 1179.5 m (cm 149950 / 117950), Spiegel 11.43 m, Boden 10.87 m (Spiegel über Boden 0.56 m), Länge 108 m.
- Breite Anfang **11.3 m**, nach 20 m 4.0 m, Verjüngung: nein; Gefälle erste 20 m: Spline 9.8 %, Boden 0.1 %.
- Lage Schlamm 44%, Wiese 25%, Trockengras 13%; Biom dschungel (R_P3_P1); Mulde 1/4 (Anstieg [0.82, -0.13, -0.11, 0.33] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_P3_P1_01 21 m; Fließgewässer B_R_P3_P1_04 83 m (Mittellinie). Ende: Fortsetzung: B_R2_R_P3_P1_03 (Mittellinie 2.2 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Ein 11 m breiter Fluss beginnt aus dem Nichts (Lage Schlamm). Zwei Wege: (1) Quellsee: mit dem Water-Brush ein Becken 40–60 m (Blend Min) am Anfang eingraben und als WaterBodyLake anschließen; (2) Anfang 150–250 m hangauf ziehen und stufig verjüngen 11 → 6 → 2 m, die obersten 50 m als Bach 0,5 m in Mulde/unter Fels (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)). Nächster See S_R_P3_P1_01 nur 21 m entfernt → Weg (1) über diesen See.

### 10. F_ALTARM_FLUSSAUE_D5 – Klasse b (abzweig), Schwere 201

- Feld **D5**, Anfang X -819.5 / Y 424.5 m (cm -81950 / 42450), Spiegel 20.00 m, Boden 18.67 m (Spiegel über Boden 1.33 m), Länge 159 m.
- Breite Anfang **17.1 m**, nach 20 m 8.8 m, Verjüngung: nein; Gefälle erste 20 m: Spline 0.0 %, Boden -0.0 %.
- Lage Sand 78%, Geroell 19%, Gras 2%; Biom aue (K2_FLUSSAUE); Mulde 2/4 (Anstieg [0.78, -0.14, -0.16, 1.48] m), Fels hangauf 0 %, Geröll 17 %, Schnee/Eis 0 %.
- Befund: Abzweig von F_HAUPTFLUSS_3_D5 (Mittellinie 24.4 m, dort 75.0 m breit, bei 84 % seiner Länge). Nächste Gewässer: See T_-809_226 162 m; Fließgewässer F_HAUPTFLUSS_3_D5 24 m (Mittellinie). Ende: Fortsetzung: F_ALTARM_FLUSSAUE_E5 (Mittellinie 0.0 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Abzweig: Ufer am Abzweig mit Kies/Steinen betonen; Breite am Abzweig ≤ 60 % des Hauptlaufs.

### 11. B_R_M2_P0_01 – Klasse e (-), Schwere 190

- Feld **B5**, Anfang X -2778.5 / Y 190.5 m (cm -277850 / 19050), Spiegel 66.26 m, Boden 65.80 m (Spiegel über Boden 0.46 m), Länge 128 m.
- Breite Anfang **8.0 m**, nach 20 m 2.0 m, Verjüngung: nein; Gefälle erste 20 m: Spline 28.5 %, Boden 0.3 %.
- Lage Kies 47%, Nadeln 44%, Fels 8%; Biom bergwald (R_M2_P0); Mulde 1/4 (Anstieg [0.39, 0.27, 0.11, 2.38] m), Fels hangauf 17 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_M1_P0_00 571 m; Fließgewässer B_R3_R_M2_P0_01 104 m (Mittellinie). Ende: Zusammenfluss: B_R2_R_M1_P0_03 (Mittellinie 3.0 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 8.0 m am Anfang, 2.0 m nach 20 m); Quellfassung: 2–3 Felsen (SM_MossyForestBoulder_01 (1.7×1.0 m), SM_MossyForestBoulder_03 (2.0×1.3 m), SM_MossyForestBoulder_04 (3.3×2.0 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

### 12. B_R_P2_P0_06 – Klasse e (-), Schwere 178

- Feld **F5**, Anfang X 391.5 / Y 750.5 m (cm 39150 / 75050), Spiegel 6.73 m, Boden 6.82 m (Spiegel über Boden -0.09 m), Länge 207 m.
- Breite Anfang **6.8 m**, nach 20 m 4.0 m, Verjüngung: nein; Gefälle erste 20 m: Spline 3.4 %, Boden 0.0 %.
- Lage Wiese 41%, Sand 30%, Trockengras 23%; Biom aue (R_P2_P1); Mulde 0/4 (Anstieg [-0.02, 0.14, -0.05, 0.37] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See T_K2_FLUSSAUE_00 717 m; Fließgewässer F_HAUPTFLUSS_3_F5 70 m (Mittellinie). Ende: Meer (Spiegel 0.57 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 6.8 m am Anfang, 4.0 m nach 20 m); Quellfassung: 2–3 Felsen (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

### 13. B_R_P1_P0_02 – Klasse e (-), Schwere 170

- Feld **E5**, Anfang X 1.5 / Y 440.5 m (cm 150 / 44050), Spiegel 7.49 m, Boden 7.95 m (Spiegel über Boden -0.45 m), Länge 288 m.
- Breite Anfang **6.0 m**, nach 20 m 2.8 m, Verjüngung: nein; Gefälle erste 20 m: Spline 4.5 %, Boden 0.0 %.
- Lage Wiese 65%, Moos 16%, Trockengras 13%; Biom aue (R_P1_P0); Mulde 1/4 (Anstieg [-0.06, 1.05, 0.28, 0.37] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See T_K2_FLUSSAUE_00 387 m; Fließgewässer B_R2_R_P1_P0_01 183 m (Mittellinie). Ende: Fortsetzung: B_R2_R_P1_P0_01 (Mittellinie 12.5 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 6.0 m am Anfang, 2.8 m nach 20 m); Quellfassung: 2–3 Felsen (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

### 14. B_R_P5_P1_04 – Klasse e (-), Schwere 170

- Feld **I6**, Anfang X 3633.5 / Y 1476.5 m (cm 363350 / 147650), Spiegel 47.94 m, Boden 48.49 m (Spiegel über Boden -0.55 m), Länge 81 m.
- Breite Anfang **6.0 m**, nach 20 m 4.0 m, Verjüngung: nein; Gefälle erste 20 m: Spline 39.3 %, Boden 0.5 %.
- Lage Moos 46%, Laub 32%, Kraut 9%; Biom dschungel (R_P5_P1); Mulde 2/4 (Anstieg [-0.34, 3.91, 3.75, 0.14] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See T_3778_1327 198 m; Fließgewässer B_R_P5_P1_03 87 m (Mittellinie). Ende: Fortsetzung: B_R_P5_P1_03 (Mittellinie 7.3 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 6.0 m am Anfang, 4.0 m nach 20 m); Quellfassung: 2–3 Felsen (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

### 15. B_R2_R_M1_M1_06 – Klasse e (-), Schwere 170

- Feld **C4**, Anfang X -2645.5 / Y -451.5 m (cm -264550 / -45150), Spiegel 59.73 m, Boden 59.43 m (Spiegel über Boden 0.30 m), Länge 264 m.
- Breite Anfang **6.0 m**, nach 20 m 4.9 m, Verjüngung: nein; Gefälle erste 20 m: Spline 6.7 %, Boden 0.1 %.
- Lage Geroell 46%, Nadeln 40%, Gras 11%; Biom aue (R_M1_M1); Mulde 1/4 (Anstieg [-0.06, 0.58, 0.42, 0.19] m), Fels hangauf 0 %, Geröll 53 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_M1_M1_01 564 m; Fließgewässer B_K1_WASSERFALL_WEST_03 142 m (Mittellinie). Ende: Fortsetzung: B_R2_R_M1_M1_02 (Mittellinie 1.4 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Unter Geröll beginnen lassen: Felsgruppe mit Spalt über dem ersten Punkt (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)), Bach tritt unter dem Stein aus; auf 0,3–0,6 m verjüngen (jetzt 6.0 m am Anfang, 4.9 m nach 20 m).

### 16. B_R2_R_M1_M1_09 – Klasse e (-), Schwere 170

- Feld **C4**, Anfang X -2256.5 / Y -780.5 m (cm -225650 / -78050), Spiegel 26.68 m, Boden 26.73 m (Spiegel über Boden -0.05 m), Länge 120 m.
- Breite Anfang **6.0 m**, nach 20 m 4.1 m, Verjüngung: nein; Gefälle erste 20 m: Spline 2.9 %, Boden 0.0 %.
- Lage Kies 54%, Nadeln 33%, Wiese 11%; Biom aue (R_M1_M1); Mulde 1/4 (Anstieg [0.73, 0.47, -0.01, 0.34] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_M1_M1_01 182 m; Fließgewässer B_R2_R_M1_M1_08 66 m (Mittellinie). Ende: Fortsetzung: B_R2_R_M1_M1_03 (Mittellinie 4.0 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 6.0 m am Anfang, 4.1 m nach 20 m); Quellfassung: 2–3 Felsen (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

### 17. B_R2_R_P3_M1_04 – Klasse e (-), Schwere 167

- Feld **G4**, Anfang X 1819.5 / Y -871.5 m (cm 181950 / -87150), Spiegel 16.58 m, Boden 16.37 m (Spiegel über Boden 0.21 m), Länge 68 m.
- Breite Anfang **5.7 m**, nach 20 m 4.0 m, Verjüngung: nein; Gefälle erste 20 m: Spline 0.1 %, Boden -0.0 %.
- Lage Kies 72%, Laub 27%, Moos 1%; Biom elfenwald (R_P3_M1); Mulde 0/4 (Anstieg [0.34, 0.37, 0.28, 0.27] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_P3_M1_00 126 m; Fließgewässer B_R_P3_M1_05 42 m (Mittellinie). Ende: Fortsetzung: B_R_P3_M1_05 (Mittellinie 0.3 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 5.7 m am Anfang, 4.0 m nach 20 m); Quellfassung: 2–3 Felsen (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

### 18. B_R_M2_M1_02 – Klasse e (-), Schwere 163

- Feld **B3**, Anfang X -2857.5 / Y -1168.5 m (cm -285750 / -116850), Spiegel 56.05 m, Boden 55.81 m (Spiegel über Boden 0.24 m), Länge 66 m.
- Breite Anfang **4.8 m**, nach 20 m 4.8 m, Verjüngung: nein; Gefälle erste 20 m: Spline 6.0 %, Boden 0.1 %.
- Lage Kies 71%, Nadeln 20%, Gras 9%; Biom bergwald (R_M2_M1); Mulde 1/4 (Anstieg [-0.02, 0.44, 0.93, -0.08] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_M1_M2_00 441 m; Fließgewässer B_R_M2_M2_02 107 m (Mittellinie). Ende: versickert im Nichts (nächste: See S_R_M1_M2_00 376 m, B_R_M2_M2_03 43 m). Flags: breit>1,5m, keine Verjüngung, Ende versickert.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 4.8 m am Anfang, 4.8 m nach 20 m); Quellfassung: 2–3 Felsen (SM_MossyForestBoulder_01 (1.7×1.0 m), SM_MossyForestBoulder_03 (2.0×1.3 m), SM_MossyForestBoulder_04 (3.3×2.0 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

### 19. B_R_P3_M1_05 – Klasse e (-), Schwere 163

- Feld **G4**, Anfang X 1785.5 / Y -796.5 m (cm 178550 / -79650), Spiegel 16.98 m, Boden 16.76 m (Spiegel über Boden 0.23 m), Länge 283 m.
- Breite Anfang **4.8 m**, nach 20 m 4.0 m, Verjüngung: nein; Gefälle erste 20 m: Spline 3.8 %, Boden 0.0 %.
- Lage Kies 75%, Laub 23%, Gras 1%; Biom elfenwald (R_P3_M1); Mulde 1/4 (Anstieg [0.02, -0.05, 0.47, 0.51] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_P3_M1_00 133 m; Fließgewässer B_R2_R_P3_M1_04 56 m (Mittellinie). Ende: versickert im Nichts (nächste: See S_R_P3_M1_00 105 m, F_ELFENFLUSS_3_G4 104 m). Flags: breit>1,5m, keine Verjüngung, Ende versickert.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 4.8 m am Anfang, 4.0 m nach 20 m); Quellfassung: 2–3 Felsen (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

### 20. B_R_P2_M1_03 – Klasse e (-), Schwere 158

- Feld **F4**, Anfang X 1240.5 / Y -424.5 m (cm 124050 / -42450), Spiegel 9.60 m, Boden 9.43 m (Spiegel über Boden 0.17 m), Länge 104 m.
- Breite Anfang **4.8 m**, nach 20 m 2.3 m, Verjüngung: nein; Gefälle erste 20 m: Spline 5.9 %, Boden 0.1 %.
- Lage Kies 55%, Laub 29%, Moos 16%; Biom aue (R_P2_M1); Mulde 1/4 (Anstieg [0.17, 0.38, -0.1, 1.11] m), Fels hangauf 0 %, Geröll 0 %, Schnee/Eis 0 %.
- Befund: offener Hang/Wiese, keine Quelle erkennbar. Nächste Gewässer: See S_R_P3_P0_06 365 m; Fließgewässer F_ELFENFLUSS_3_F4 41 m (Mittellinie). Ende: Zusammenfluss: F_ELFENFLUSS_3_F4 (Mittellinie 33.0 m). Flags: breit>1,5m, keine Verjüngung.
- **Vorschlag:** Keine Mulde in 30 m hangauf gefunden: Anfang 15–25 m hangauf ziehen und mit dem Water-Brush eine 0,5 m tiefe Quellmulde (6 × 8 m, Blend Min) formen; auf 0,3–0,6 m verjüngen (jetzt 4.8 m am Anfang, 2.3 m nach 20 m); Quellfassung: 2–3 Felsen (SM_IcelandicBoulder_02 (1.8×1.5 m), SM_IcelandicBoulder_03 (3.2×2.6 m), SM_big_rock_wall_02 (5.2×2.5 m)) halb eingegraben um den ersten Punkt, Moos-Netze (SM_MossClump_01…05, SM_moss_01/02) auf Fels und Ufer.

## Tabelle aller Gewässer (sortiert nach Schwere)

| # | Gewässer | Kl. | Unterart | Feld | X / Y (m) | Spiegel m | Boden m | Breite 0 / 20 m | Verj. | Gefälle 20 m % | Lage | Biom | Ende | Flags | Schwere |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | F_CANYONBACH_D4 | e | - | D4 | -1157 / -286 | 25.70 | 24.42 | 51.0 / 43.3 | nein | 0.0 | Trockengras | canyon | fortsetzung | breit>1,5m, keine Verjüngung | 620 |
| 2 | F_DSCHUNGELFLUSS_H5 | e | - | H5 | 3297 / 873 | 6.54 | 5.99 | 49.0 / 48.3 | nein | 0.0 | Gras | sumpf | fortsetzung | breit>1,5m, keine Verjüngung | 600 |
| 3 | F_HAUPTFLUSS_3_C4 | e | - | C4 | -2615 / -64 | 42.80 | 41.71 | 47.0 / 38.3 | nein | 17.5 | Kies | aue | fortsetzung | breit>1,5m, keine Verjüngung | 580 |
| 4 | F_HAUPTFLUSS_2_B4 | b | luecke | B4 | -3082 / -569 | 206.56 | 205.70 | 37.0 / 40.0 | schwach | 2.5 | Kies | bergwald | nichts | breit>1,5m, Ende versickert, Lücke 133 m | 405 |
| 5 | F_HAUPTFLUSS_1_B4 | e | - | B4 | -3190 / -690 | 288.15 | 287.43 | 21.0 / 21.0 | nein | 17.7 | Kies | bergwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 325 |
| 6 | F_ELFENFLUSS_1_H4 | b | wasserfall | H4 | 3085 / -695 | 127.72 | 126.94 | 32.0 / 34.3 | schwach | 6.8 | Kies | elfenwald | fortsetzung | breit>1,5m | 325 |
| 7 | F_GLETSCHERTAL_D2 | c | biom | D2 | -740 / -2656 | 90.58 | 90.29 | 25.7 / 38.2 | ja | 0.4 | Geroell | gletscher | see | breit>1,5m, kein Schnee/Eis in 20 m | 302 |
| 8 | F_ERLENBACH_2_D3 | b | abzweig | C3 | -1707 / -2005 | 36.13 | 35.26 | 26.0 / 25.6 | nein | 2.0 | Wiese | tundra | fortsetzung | breit>1,5m, keine Verjüngung | 290 |
| 9 | B_R_P3_P1_03 | e | - | G6 | 1500 / 1180 | 11.43 | 10.87 | 11.3 / 4.0 | nein | 9.8 | Schlamm | dschungel | fortsetzung | breit>1,5m, keine Verjüngung | 223 |
| 10 | F_ALTARM_FLUSSAUE_D5 | b | abzweig | D5 | -820 / 424 | 20.00 | 18.67 | 17.1 / 8.8 | nein | 0.0 | Sand | aue | fortsetzung | breit>1,5m, keine Verjüngung | 201 |
| 11 | B_R_M2_P0_01 | e | - | B5 | -2778 / 190 | 66.26 | 65.80 | 8.0 / 2.0 | nein | 28.5 | Kies | bergwald | zusammenfluss | breit>1,5m, keine Verjüngung | 190 |
| 12 | B_R_P2_P0_06 | e | - | F5 | 392 / 750 | 6.73 | 6.82 | 6.8 / 4.0 | nein | 3.4 | Wiese | aue | meer | breit>1,5m, keine Verjüngung | 178 |
| 13 | B_R_P1_P0_02 | e | - | E5 | 2 / 440 | 7.49 | 7.95 | 6.0 / 2.8 | nein | 4.5 | Wiese | aue | fortsetzung | breit>1,5m, keine Verjüngung | 170 |
| 14 | B_R_P5_P1_04 | e | - | I6 | 3634 / 1476 | 47.94 | 48.49 | 6.0 / 4.0 | nein | 39.3 | Moos | dschungel | fortsetzung | breit>1,5m, keine Verjüngung | 170 |
| 15 | B_R2_R_M1_M1_06 | e | - | C4 | -2646 / -452 | 59.73 | 59.43 | 6.0 / 4.9 | nein | 6.7 | Geroell | aue | fortsetzung | breit>1,5m, keine Verjüngung | 170 |
| 16 | B_R2_R_M1_M1_09 | e | - | C4 | -2256 / -780 | 26.68 | 26.73 | 6.0 / 4.1 | nein | 2.9 | Kies | aue | fortsetzung | breit>1,5m, keine Verjüngung | 170 |
| 17 | B_R2_R_P3_M1_04 | e | - | G4 | 1820 / -872 | 16.58 | 16.37 | 5.7 / 4.0 | nein | 0.1 | Kies | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung | 167 |
| 18 | B_R_M2_M1_02 | e | - | B3 | -2858 / -1168 | 56.05 | 55.81 | 4.8 / 4.8 | nein | 6.0 | Kies | bergwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 163 |
| 19 | B_R_P3_M1_05 | e | - | G4 | 1786 / -796 | 16.98 | 16.76 | 4.8 / 4.0 | nein | 3.8 | Kies | elfenwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 163 |
| 20 | B_R_P2_M1_03 | e | - | F4 | 1240 / -424 | 9.60 | 9.43 | 4.8 / 2.3 | nein | 5.9 | Kies | aue | zusammenfluss | breit>1,5m, keine Verjüngung | 158 |
| 21 | B_R_P3_P1_02 | e | - | G5 | 1422 / 802 | 7.76 | 7.50 | 4.8 / 4.0 | nein | 5.9 | Wiese | dschungel | fortsetzung | breit>1,5m, keine Verjüngung | 158 |
| 22 | B_R2_R_P1_P0_01 | e | - | E5 | 184 / 432 | 5.27 | 5.06 | 4.8 / 3.7 | nein | 7.3 | Wiese | aue | fortsetzung | breit>1,5m, keine Verjüngung | 158 |
| 23 | B_R_M2_P1_01 | e | - | B6 | -3374 / 1098 | 56.04 | 55.53 | 4.0 / 3.9 | nein | 26.3 | Moos | bergwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 155 |
| 24 | B_R_M2_P1_03 | d | mulde | B6 | -2912 / 1640 | 3.94 | 4.14 | 8.0 / 4.0 | nein | 4.0 | Lavafels | bergwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert, schwache Mulde 0.5 m | 155 |
| 25 | B_R_P0_M2_02 | e | - | D2 | -832 / -2186 | 69.33 | 69.36 | 4.0 / 4.0 | nein | 37.6 | Wiese | tundra | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 155 |
| 26 | B_R_P0_P2_04 | e | - | D7 | -1288 / 2126 | 30.97 | 30.42 | 4.0 / 2.9 | nein | 23.8 | Lavasand | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 155 |
| 27 | B_R_P0_P2_06 | e | - | D7 | -1554 / 2334 | 27.26 | 26.85 | 4.0 / 4.0 | nein | 43.6 | Lavasand | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 155 |
| 28 | B_K8_ELFENFALL_04 | e | - | H4 | 2980 / -364 | 57.36 | 56.78 | 4.8 / 6.8 | schwach | 22.0 | Kies | elfenwald | nichts | breit>1,5m, Ende versickert | 153 |
| 29 | B_R_M1_P0_04 | e | - | D5 | -1652 / 630 | 30.28 | 30.17 | 4.0 / 4.0 | nein | 3.8 | Wiese | aue | see | breit>1,5m, keine Verjüngung | 150 |
| 30 | B_R_P0_P2_02 | e | - | D6 | -1242 / 1758 | 30.74 | 31.12 | 4.0 / 2.8 | nein | 21.0 | Lavasand | VULKAN_REGION | fortsetzung | breit>1,5m, keine Verjüngung | 150 |
| 31 | B_R_P2_P1_03 | e | - | G5 | 1344 / 974 | 4.06 | 3.80 | 4.0 / 2.8 | nein | 3.2 | Moos | aue | meer | breit>1,5m, keine Verjüngung | 150 |
| 32 | B_R_P3_M2_04 | e | - | G3 | 1874 / -1362 | 47.75 | 45.82 | 4.0 / 4.0 | nein | 38.5 | Kies | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung | 150 |
| 33 | B_R_P3_P2_01 | d | mulde | G6 | 2138 / 1820 | 4.00 | 4.10 | 8.0 / 4.0 | nein | 5.9 | Laub | dschungel | meer | breit>1,5m, keine Verjüngung, schwache Mulde 0.7 m | 150 |
| 34 | B_R2_R_P0_P2_02 | e | - | D7 | -1198 / 2046 | 18.49 | 17.91 | 4.0 / 2.8 | nein | 32.3 | Lavasand | aue | fortsetzung | breit>1,5m, keine Verjüngung | 150 |
| 35 | B_R2_R_P3_P1_05 | d | mulde | G6 | 1556 / 1304 | 7.00 | 6.97 | 8.0 / 3.0 | nein | 2.1 | Wiese | dschungel | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.7 m | 150 |
| 36 | B_R2_K10_TUNDRA_02 | b | zusammenfluss | D2 | -1698 / -2066 | 37.76 | 36.83 | 13.3 / 9.8 | nein | 3.2 | Trockengras | tundra | zusammenfluss | breit>1,5m, keine Verjüngung | 148 |
| 37 | B_R_M1_M2_01 | e | - | C3 | -2564 / -1328 | 11.79 | 11.61 | 4.0 / 5.9 | ja | 19.4 | Kies | aue | nichts | breit>1,5m, Ende versickert | 145 |
| 38 | B_R_P4_M2_02 | e | - | H3 | 2366 / -1566 | 17.40 | 17.09 | 4.0 / 6.0 | ja | 16.9 | Kies | elfenwald | nichts | breit>1,5m, Ende versickert | 145 |
| 39 | B_R_P4_M2_01 | e | - | H3 | 2590 / -1596 | 28.40 | 27.89 | 4.0 / 4.1 | schwach | 40.1 | Kies | elfenwald | meer | breit>1,5m | 140 |
| 40 | B_R2_R_M1_M1_01 | e | - | C3 | -2650 / -1138 | 17.89 | 17.95 | 4.0 / 5.9 | ja | 8.7 | Kies | aue | zusammenfluss | breit>1,5m | 140 |
| 41 | B_R_P0_P2_01 | d | mulde | D6 | -1134 / 1752 | 9.50 | 9.46 | 6.8 / 4.0 | nein | 5.3 | Wiese | aue | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.6 m | 138 |
| 42 | B_R2_R_M1_P0_02 | e | - | C5 | -2462 / 52 | 28.02 | 27.75 | 2.8 / 2.8 | nein | 10.9 | Wiese | aue | zusammenfluss | breit>1,5m, keine Verjüngung | 138 |
| 43 | B_R2_R_P3_P1_03 | d | mulde | G6 | 1550 / 1006 | 11.02 | 10.99 | 6.8 / 2.8 | nein | 2.3 | Wiese | dschungel | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.8 m | 138 |
| 44 | B_R_M1_M1_01 | d | mulde | C3 | -2352 / -1128 | 17.34 | 17.30 | 8.0 / 2.9 | nein | 8.5 | Kies | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 135 |
| 45 | B_R3_R_P3_P0_02 | e | - | G5 | 2314 / 78 | 3.50 | 3.22 | 3.5 / 4.0 | schwach | 9.9 | Gras | heide | fortsetzung | breit>1,5m | 135 |
| 46 | B_R_P0_P2_03 | e | - | D6 | -1210 / 1896 | 21.35 | 19.79 | 2.8 / 4.8 | ja | 34.6 | Lavasand | aue | nichts | breit>1,5m, Ende versickert | 133 |
| 47 | B_R_M1_P0_01 | d | mulde | C4 | -2084 / -176 | 23.03 | 22.70 | 5.7 / 4.0 | nein | 1.5 | Trockengras | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert, schwache Mulde 0.9 m | 132 |
| 48 | B_R_M3_M2_03 | d | mulde | A3 | -3884 / -1250 | 16.35 | 16.20 | 5.7 / 4.8 | nein | 21.8 | Gras | bergwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert, schwache Mulde 0.6 m | 132 |
| 49 | B_R2_R_P2_P1_02 | d | mulde | F6 | 384 / 1010 | 8.20 | 8.03 | 6.0 / 2.8 | nein | 5.3 | Kies | aue | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.9 m | 130 |
| 50 | B_R2_R_P3_P1_01 | d | mulde | G5 | 2128 / 904 | 24.19 | 23.82 | 6.0 / 4.0 | nein | 0.6 | Kraut | dschungel | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 1.0 m | 130 |
| 51 | B_R2_R_P3_P1_04 | d | mulde | G6 | 1596 / 1336 | 8.26 | 8.19 | 6.0 / 4.0 | nein | 3.2 | Trockengras | dschungel | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.6 m | 130 |
| 52 | B_R_P1_P0_01 | e | - | E5 | 2 / 116 | 3.72 | 3.75 | 2.8 / 4.0 | schwach | 6.0 | Trockengras | aue | meer | breit>1,5m | 128 |
| 53 | B_R2_R_P0_P2_01 | e | - | D6 | -1188 / 1966 | 17.75 | 17.38 | 2.8 / 7.5 | ja | 32.0 | Wiese | aue | fortsetzung | breit>1,5m | 128 |
| 54 | B_R2_R_P5_P1_01 | e | - | I6 | 3520 / 1178 | 27.73 | 27.27 | 2.8 / 4.0 | schwach | 19.4 | Laub | dschungel | fortsetzung | breit>1,5m | 128 |
| 55 | B_R3_R_M2_P2_01 | e | - | B6 | -2938 / 1750 | 5.87 | 5.59 | 2.7 / 7.2 | ja | 9.0 | Lavasand | aue | fortsetzung | breit>1,5m | 127 |
| 56 | B_R_P0_M2_03 | e | - | D2 | -1074 / -2080 | 77.03 | 77.24 | 2.0 / 2.9 | ja | 43.5 | Wiese | tundra | nichts | breit>1,5m, Ende versickert | 125 |
| 57 | B_K8_ELFENFALL_03 | d | mulde | H4 | 2706 / -392 | 35.32 | 34.77 | 6.8 / 4.8 | nein | 9.4 | Kies | elfenwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 123 |
| 58 | B_R_M2_M2_01 | d | mulde | B3 | -3418 / -1506 | 45.91 | 45.53 | 4.8 / 2.8 | nein | 32.6 | Kies | bergwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert, schwache Mulde 0.6 m | 123 |
| 59 | B_R3_K12_WUESTE_01 | d | mulde | D4 | -818 / -460 | 77.08 | 76.80 | 7.8 / 8.1 | schwach | 5.8 | Sand | wueste | nichts | breit>1,5m, Ende versickert | 123 |
| 60 | B_R_M2_P1_02 | e | - | B6 | -3560 / 1106 | 50.56 | 51.15 | 2.0 / 4.0 | ja | 30.7 | Wiese | bergwald | zusammenfluss | breit>1,5m | 120 |
| 61 | B_R2_K10_TUNDRA_01 | e | - | C2 | -1776 / -2078 | 38.66 | 38.72 | 2.0 / 4.0 | ja | 0.4 | Kies | tundra | zusammenfluss | breit>1,5m | 120 |
| 62 | B_R2_R_M1_M1_03 | e | - | C4 | -2638 / -784 | 44.58 | 44.75 | 2.0 / 2.9 | schwach | 7.5 | Nadeln | aue | fortsetzung | breit>1,5m | 120 |
| 63 | B_R2_R_P0_P2_03 | e | - | D7 | -1380 / 2276 | 30.51 | 30.67 | 2.0 / 2.9 | ja | 23.0 | Lavasand | aue | fortsetzung | breit>1,5m | 120 |
| 64 | B_R_P3_P0_02 | d | mulde | G4 | 2068 / -44 | 24.96 | 24.67 | 4.8 / 4.0 | nein | 3.3 | Moos | heide | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.9 m | 118 |
| 65 | B_R_P3_P0_03 | d | mulde | G5 | 1656 / 376 | 15.10 | 14.84 | 4.8 / 4.0 | nein | 1.8 | Moos | heide | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.9 m | 118 |
| 66 | B_R2_R_P3_P1_02 | d | mulde | G6 | 2016 / 1066 | 25.10 | 24.69 | 4.8 / 4.0 | nein | 1.8 | Moos | dschungel | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.9 m | 118 |
| 67 | B_R3_R_P3_P0_01 | d | mulde | G5 | 1774 / -16 | 19.83 | 19.55 | 4.5 / 4.0 | nein | 2.0 | Trockengras | heide | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.7 m | 116 |
| 68 | B_R_M1_M1_02 | d | mulde | C3 | -2232 / -1106 | 15.50 | 15.52 | 4.0 / 4.0 | nein | 10.2 | Sand | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert, schwache Mulde 0.8 m | 115 |
| 69 | B_R_P1_M2_01 | c | biom | E2 | -546 / -2250 | 52.78 | 53.00 | 6.0 / 4.0 | nein | 12.3 | Geroell | tundra | zusammenfluss | breit>1,5m, keine Verjüngung, kein Schnee/Eis in 20 m | 115 |
| 70 | B_R_P1_P0_03 | d | mulde | E5 | 308 / 444 | 4.98 | 4.71 | 4.0 / 4.0 | nein | 3.0 | Wiese | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert, schwache Mulde 0.8 m | 115 |
| 71 | B_R3_R_M2_P1_01 | d | mulde | B6 | -3622 / 1264 | 9.05 | 8.77 | 4.3 / 4.1 | nein | 5.5 | Wiese | bergwald | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.9 m | 113 |
| 72 | B_R_P3_M1_09 | d | mulde | G4 | 2100 / -468 | 19.22 | 18.90 | 4.0 / 2.9 | nein | 4.3 | Kies | elfenwald | zusammenfluss | breit>1,5m, keine Verjüngung, schwache Mulde 0.8 m | 110 |
| 73 | B_R_P3_M2_02 | d | mulde | G3 | 2174 / -1588 | 40.28 | 40.50 | 6.0 / 4.0 | nein | 21.4 | Kies | elfenwald | zusammenfluss | breit>1,5m, keine Verjüngung | 110 |
| 74 | B_R2_R_M1_M1_08 | d | mulde | C4 | -2432 / -890 | 29.43 | 29.15 | 4.0 / 2.9 | nein | 2.1 | Kies | aue | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.8 m | 110 |
| 75 | B_R2_R_M1_P0_05 | d | mulde | C5 | -2122 / 448 | 20.70 | 20.34 | 4.0 / 2.8 | nein | 3.3 | Gras | aue | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.6 m | 110 |
| 76 | B_R2_R_M2_M2_01 | b | abzweig | C3 | -2658 / -1246 | 8.24 | 8.04 | 8.0 / 4.9 | nein | 10.2 | Kies | bergwald | zusammenfluss | breit>1,5m, keine Verjüngung | 110 |
| 77 | B_R2_R_P2_P1_01 | d | mulde | F5 | 350 / 906 | 5.41 | 5.26 | 4.0 / 2.8 | nein | 1.8 | Wiese | aue | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.9 m | 110 |
| 78 | B_R2_R_P3_M1_05 | d | mulde | G4 | 1378 / -594 | 20.96 | 20.90 | 4.0 / 2.8 | nein | 7.8 | Kies | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.9 m | 110 |
| 79 | B_R2_R_P3_P0_01 | d | mulde | G5 | 1482 / 38 | 19.22 | 18.81 | 4.0 / 4.0 | nein | 0.4 | Trockengras | heide | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.7 m | 110 |
| 80 | B_R2_R_P3_P0_04 | d | mulde | G5 | 1794 / 400 | 16.64 | 16.34 | 4.0 / 4.0 | nein | 3.3 | Moos | heide | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.6 m | 110 |
| 81 | B_R3_R_M1_M1_02 | d | mulde | C4 | -2060 / -544 | 25.02 | 24.74 | 4.0 / 3.9 | nein | 5.1 | Wiese | aue | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.8 m | 110 |
| 82 | B_R_P2_M3_01 | c | biom | F2 | 362 / -3050 | 26.89 | 26.68 | 4.8 / 2.9 | nein | 8.3 | Wiese | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert, kein Schnee/Eis in 20 m | 108 |
| 83 | B_R3_R_P5_P1_01 | d | mulde | I6 | 3370 / 1020 | 15.09 | 14.81 | 3.6 / 3.6 | nein | 5.8 | Laub | dschungel | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.9 m | 106 |
| 84 | B_K1_WASSERFALL_WEST_02 | d | mulde | B4 | -2838 / -678 | 85.45 | 84.73 | 4.8 / 4.8 | nein | 23.2 | Kies | bergwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 103 |
| 85 | B_R_M1_P0_03 | b | zusammenfluss | C5 | -2650 / 116 | 48.36 | 48.06 | 6.8 / 4.2 | nein | 21.4 | Kies | aue | see | breit>1,5m, keine Verjüngung, Breitensprung 3.9→6.8 m | 103 |
| 86 | B_R_P0_M2_04 | d | mulde | D3 | -784 / -1990 | 23.34 | 22.98 | 4.8 / 4.8 | nein | 24.4 | Moos | tundra | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 103 |
| 87 | B_R_P3_M2_01 | d | mulde | G3 | 1946 / -1530 | 51.21 | 50.68 | 4.8 / 4.0 | nein | 23.0 | Kies | elfenwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 103 |
| 88 | B_R_P3_P1_01 | d | mulde | G6 | 2174 / 1278 | 48.03 | 47.73 | 4.8 / 2.9 | nein | 16.7 | Laub | dschungel | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 103 |
| 89 | B_R3_R_P2_M1_01 | d | mulde | G4 | 1334 / -930 | 9.41 | 9.13 | 3.2 / 2.9 | nein | 11.1 | Kies | aue | fortsetzung | breit>1,5m, keine Verjüngung, schwache Mulde 0.7 m | 102 |
| 90 | SWR_ARM_OST (C2) | d | mulde | C2 | -1744 / -2150 | 39.68 | 39.68 | 4.0 / 7.9 | ja | 1.2 | Kies | tundra | fortsetzung | breit>1,5m, schwache Mulde 0.6 m | 100 |
| 91 | B_R2_R_P3_P0_03 | d | mulde | G5 | 1872 / 94 | 19.31 | 19.00 | 4.0 / 4.1 | schwach | 1.1 | Schlamm | heide | fortsetzung | breit>1,5m, schwache Mulde 0.8 m | 100 |
| 92 | B_R_P4_M1_04 | d | mulde | H4 | 2406 / -854 | 28.41 | 28.17 | 4.8 / 4.9 | nein | 9.8 | Kies | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung | 98 |
| 93 | B_R_M1_P0_02 | d | mulde | C4 | -2338 / -172 | 26.70 | 26.45 | 4.0 / 4.0 | nein | 5.3 | Wiese | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 95 |
| 94 | B_R_M3_M2_02 | d | mulde | A3 | -3822 / -1250 | 24.55 | 24.52 | 4.0 / 3.9 | nein | 26.8 | Kies | bergwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 95 |
| 95 | B_R_P1_P0_04 | d | mulde | E5 | 224 / 710 | 9.53 | 9.24 | 4.0 / 3.9 | nein | 1.3 | Gras | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 95 |
| 96 | B_R_P3_P1_05 | d | mulde | G6 | 1974 / 1502 | 13.91 | 13.63 | 4.0 / 4.0 | nein | 6.2 | Gras | dschungel | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 95 |
| 97 | B_R_P5_P1_02 | d | mulde | I6 | 3610 / 1372 | 37.86 | 38.01 | 4.0 / 2.0 | nein | 26.7 | Laub | dschungel | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 95 |
| 98 | B_R3_R_M1_P0_01 | d | mulde | C5 | -1902 / 124 | 21.80 | 21.52 | 4.0 / 3.3 | nein | 10.9 | Wiese | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 95 |
| 99 | B_K8_ELFENFALL_05 | d | mulde | H4 | 2718 / -280 | 25.46 | 24.95 | 4.8 / 4.9 | schwach | 7.5 | Kies | elfenwald | nichts | breit>1,5m, Ende versickert | 93 |
| 100 | B_R_P2_M3_02 | c | schnee | F2 | 466 / -2936 | 29.99 | 27.79 | 4.8 / 4.2 | nein | 15.2 | Schnee | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 93 |
| 101 | B_R3_R_M1_M1_01 | d | mulde | C4 | -2572 / -722 | 36.51 | 36.23 | 4.3 / 3.2 | nein | 6.2 | Kies | aue | fortsetzung | breit>1,5m, keine Verjüngung | 93 |
| 102 | B_R3_R_M2_P0_02 | d | mulde | B5 | -2748 / 374 | 62.94 | 62.66 | 3.2 / 3.9 | schwach | 18.4 | Gras | bergwald | fortsetzung | breit>1,5m, schwache Mulde 0.9 m | 92 |
| 103 | B_R_M1_M2_02 | b | abzweig | C3 | -2650 / -1294 | 4.05 | 3.79 | 5.7 / 5.6 | nein | 4.5 | Kies | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 92 |
| 104 | B_R_M1_M1_03 | d | mulde | C4 | -2536 / -296 | 49.28 | 49.25 | 4.0 / 2.8 | nein | 28.0 | Kies | aue | zusammenfluss | breit>1,5m, keine Verjüngung | 90 |
| 105 | B_R_M2_M2_02 | d | mulde | B3 | -2846 / -1274 | 16.02 | 15.46 | 4.0 / 2.8 | nein | 24.1 | Kies | bergwald | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 106 | B_R_P2_P0_01 | d | mulde | F5 | 1234 / 46 | 5.94 | 5.69 | 4.0 / 2.9 | nein | 4.2 | Wiese | heide | meer | breit>1,5m, keine Verjüngung | 90 |
| 107 | B_R_P2_P0_02 | d | mulde | F5 | 1282 / 234 | 7.71 | 7.39 | 4.0 / 4.0 | nein | 3.4 | Moos | heide | meer | breit>1,5m, keine Verjüngung | 90 |
| 108 | B_R_P2_P1_02 | d | mulde | F6 | 352 / 988 | 8.28 | 7.96 | 4.0 / 4.0 | nein | 3.9 | Kies | aue | meer | breit>1,5m, keine Verjüngung | 90 |
| 109 | B_R_P3_P0_01 | d | mulde | G4 | 2212 / -144 | 20.86 | 20.63 | 4.0 / 4.0 | nein | 6.4 | Kies | heide | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 110 | B_R_P3_P0_04 | d | mulde | G5 | 2006 / 564 | 19.13 | 18.83 | 4.0 / 4.0 | nein | 1.9 | Moos | heide | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 111 | B_R_P4_M1_03 | d | mulde | H4 | 2586 / -932 | 58.56 | 58.33 | 4.0 / 4.0 | nein | 20.9 | Laub | elfenwald | zusammenfluss | breit>1,5m, keine Verjüngung | 90 |
| 112 | B_R_P5_P1_05 | d | mulde | I6 | 3686 / 1554 | 42.45 | 40.38 | 4.0 / 4.0 | nein | 24.7 | Wiese | dschungel | meer | breit>1,5m, keine Verjüngung | 90 |
| 113 | B_R2_R_P1_M2_01 | d | mulde | E2 | -402 / -2136 | 49.61 | 49.20 | 4.0 / 4.0 | nein | 17.0 | Wiese | tundra | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 114 | B_R2_R_P2_M1_01 | d | mulde | F4 | 968 / -628 | 12.86 | 12.41 | 4.0 / 2.8 | nein | 12.7 | Wiese | aue | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 115 | B_R2_R_P3_M1_01 | d | mulde | G3 | 1806 / -1158 | 14.68 | 14.42 | 4.0 / 2.8 | nein | 9.0 | Kies | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 116 | B_R2_R_P3_P0_02 | d | mulde | G5 | 2232 / 68 | 8.06 | 7.84 | 4.0 / 4.0 | nein | 5.6 | Laub | heide | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 117 | B_R2_R_P3_P1_06 | d | mulde | G6 | 1818 / 1550 | 7.53 | 7.18 | 4.0 / 4.0 | nein | 4.3 | Laub | dschungel | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 118 | B_R2_R_P4_M1_01 | d | mulde | H3 | 2376 / -1250 | 33.10 | 32.83 | 4.0 / 2.2 | nein | 15.7 | Kies | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung | 90 |
| 119 | B_K1_WASSERFALL_WEST_03 | d | mulde | B4 | -2814 / -550 | 92.03 | 91.33 | 4.8 / 7.6 | ja | 20.8 | Kies | bergwald | fortsetzung | breit>1,5m | 88 |
| 120 | B_R_P3_M1_08 | d | mulde | G4 | 1430 / -596 | 21.22 | 20.82 | 2.8 / 4.0 | schwach | 9.6 | Kies | elfenwald | zusammenfluss | breit>1,5m, schwache Mulde 0.9 m | 88 |
| 121 | B_R_P5_P1_01 | d | mulde | I6 | 3616 / 1268 | 30.66 | 30.47 | 2.8 / 2.9 | schwach | 21.9 | Kraut | dschungel | meer | breit>1,5m, schwache Mulde 0.6 m | 88 |
| 122 | B_K1_WASSERFALL_WEST_01 | d | mulde | B4 | -2918 / -842 | 95.22 | 94.52 | 4.0 / 4.8 | schwach | 27.2 | Kies | bergwald | nichts | breit>1,5m, Ende versickert | 85 |
| 123 | B_K8_ELFENFALL_06 | d | mulde | H4 | 3066 / -246 | 60.73 | 60.35 | 4.0 / 5.6 | schwach | 25.5 | Kies | elfenwald | nichts | breit>1,5m, Ende versickert | 85 |
| 124 | B_R_P2_P1_01 | b | zusammenfluss | G5 | 1350 / 816 | 4.82 | 4.78 | 6.8 / 4.0 | nein | 4.8 | Wiese | dschungel | meer | breit>1,5m, keine Verjüngung | 83 |
| 125 | B_R_P4_M1_02 | b | abzweig | H3 | 2588 / -1116 | 54.62 | 54.29 | 4.8 / 4.0 | nein | 21.5 | Kies | elfenwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 83 |
| 126 | B_R3_R_M1_M1_03 | d | mulde | C4 | -2330 / -414 | 25.86 | 25.57 | 3.3 / 3.0 | nein | 3.5 | Gras | aue | fortsetzung | breit>1,5m, keine Verjüngung | 83 |
| 127 | B_K8_ELFENFALL_02 | d | mulde | H4 | 2868 / -704 | 93.98 | 93.58 | 4.0 / 5.6 | schwach | 24.6 | Kies | elfenwald | zusammenfluss | breit>1,5m | 80 |
| 128 | B_R_P3_P0_05 | d | mulde | G5 | 2246 / 576 | 12.57 | 12.67 | 2.0 / 4.0 | ja | 6.2 | Gras | heide | see | breit>1,5m, schwache Mulde 0.8 m | 80 |
| 129 | B_R2_R_M1_M1_05 | b | luecke | C4 | -2342 / -276 | 27.00 | 26.73 | 4.0 / 4.0 | nein | 0.7 | Gras | aue | fortsetzung | breit>1,5m, keine Verjüngung, Lücke 42 m | 80 |
| 130 | B_R2_R_P3_M2_01 | d | mulde | G3 | 1848 / -1742 | 35.97 | 35.61 | 4.0 / 4.1 | schwach | 35.8 | Kies | elfenwald | fortsetzung | breit>1,5m | 80 |
| 131 | B_R2_R_P4_M2_01 | d | mulde | H3 | 2962 / -1494 | 160.91 | 160.60 | 4.0 / 4.8 | schwach | 54.9 | Kies | elfenwald | fortsetzung | breit>1,5m | 80 |
| 132 | B_R_M2_M1_01 | b | abzweig | C3 | -2650 / -1188 | 13.63 | 13.34 | 4.8 / 4.8 | nein | 9.4 | Kies | aue | zusammenfluss | breit>1,5m, keine Verjüngung | 78 |
| 133 | B_R_P3_M1_02 | b | abzweig | H3 | 2350 / -1182 | 22.34 | 22.06 | 4.8 / 4.8 | nein | 7.2 | Kies | elfenwald | see | breit>1,5m, keine Verjüngung | 78 |
| 134 | B_R_P3_M1_07 | d | mulde | H4 | 2336 / -618 | 26.30 | 25.99 | 2.8 / 2.8 | nein | 9.9 | Kies | elfenwald | zusammenfluss | breit>1,5m, keine Verjüngung | 78 |
| 135 | B_R3_R_P4_M1_01 | d | mulde | H4 | 2482 / -250 | 25.30 | 25.02 | 3.2 / 4.0 | schwach | 7.7 | Kies | aue | nichts | breit>1,5m, Ende versickert | 77 |
| 136 | B_R_P2_P0_03 | b | zusammenfluss | G5 | 1350 / 320 | 8.42 | 8.23 | 5.7 / 4.1 | nein | 2.8 | Moos | heide | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 77 |
| 137 | B_R_P3_M1_04 | b | zusammenfluss | H4 | 2350 / -896 | 20.75 | 20.58 | 5.7 / 3.9 | nein | 12.5 | Kies | elfenwald | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 77 |
| 138 | B_R_M2_P1_04 | b | zusammenfluss | B6 | -2966 / 1750 | 3.73 | 3.62 | 6.0 / 4.7 | nein | 4.5 | Lavasand | aue | meer | breit>1,5m, keine Verjüngung | 75 |
| 139 | B_R_P1_M2_02 | c | schnee | E2 | -258 / -2250 | 72.00 | 71.91 | 4.0 / 5.8 | ja | 11.6 | Schnee | tundra | nichts | breit>1,5m, Ende versickert | 75 |
| 140 | B_R_P1_M2_04 | c | schnee | E3 | -246 / -1902 | 10.27 | 9.98 | 4.0 / 4.8 | schwach | 10.6 | Schnee | tundra | nichts | breit>1,5m, Ende versickert | 75 |
| 141 | B_R2_R_M1_P0_01 | b | abzweig | C4 | -2378 / -250 | 28.52 | 28.36 | 4.0 / 4.0 | nein | 4.1 | Erde | aue | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 75 |
| 142 | B_R2_R_P3_M1_03 | b | zusammenfluss | G4 | 1350 / -956 | 6.44 | 6.18 | 4.0 / 2.8 | nein | 6.9 | Kies | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung, Breitensprung 2.3→4.0 m | 75 |
| 143 | B_K8_ELFENFALL_01 | d | mulde | H3 | 3012 / -1078 | 178.67 | 178.19 | 2.8 / 6.0 | ja | 62.7 | Geroell | elfenwald | nichts | breit>1,5m, Ende versickert | 73 |
| 144 | B_R_P0_P2_05 | d | mulde | D7 | -1388 / 2192 | 44.43 | 40.30 | 2.8 / 3.0 | schwach | 33.4 | Lavasand | aue | nichts | breit>1,5m, Ende versickert | 73 |
| 145 | B_R_P1_M2_03 | b | abzweig | E2 | -650 / -2152 | 32.31 | 32.12 | 4.8 / 6.0 | schwach | 11.2 | Trockengras | tundra | nichts | breit>1,5m, Ende versickert | 73 |
| 146 | B_R_P2_M1_01 | d | mulde | F4 | 1166 / -828 | 27.92 | 27.52 | 2.8 / 4.0 | schwach | 18.2 | Kies | aue | nichts | breit>1,5m, Ende versickert | 73 |
| 147 | B_R_P2_M1_02 | d | mulde | F4 | 1028 / -604 | 17.67 | 17.29 | 2.8 / 4.7 | ja | 16.2 | Kies | aue | nichts | breit>1,5m, Ende versickert | 73 |
| 148 | B_R_P3_M1_06 | d | mulde | H4 | 2334 / -740 | 26.95 | 26.81 | 2.8 / 4.0 | schwach | 14.7 | Kies | elfenwald | nichts | breit>1,5m, Ende versickert | 73 |
| 149 | B_R_P4_M2_03 | d | mulde | H3 | 2406 / -1458 | 41.35 | 41.12 | 2.8 / 4.8 | ja | 19.5 | Kies | elfenwald | nichts | breit>1,5m, Ende versickert | 73 |
| 150 | B_R2_R_P0_M2_01 | c | biom | E2 | -650 / -2242 | 46.63 | 46.48 | 2.8 / 4.8 | ja | 14.4 | Wiese | tundra | fortsetzung | breit>1,5m, kein Schnee/Eis in 20 m | 73 |
| 151 | B_R3_R_M2_P0_01 | d | mulde | B5 | -2818 / 92 | 86.96 | 86.68 | 3.2 / 4.3 | schwach | 26.2 | Kies | bergwald | fortsetzung | breit>1,5m | 72 |
| 152 | B_R_M2_M2_03 | b | wasserfall | B3 | -2784 / -1250 | 12.10 | 11.98 | 5.7 / 5.5 | nein | 14.1 | Kies | bergwald | fortsetzung | breit>1,5m, keine Verjüngung | 72 |
| 153 | B_R_P2_P0_05 | b | zusammenfluss | G5 | 1350 / 648 | 4.58 | 4.33 | 4.8 / 4.8 | nein | 2.5 | Moos | heide | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 68 |
| 154 | B_R_P3_M1_03 | d | mulde | G4 | 1412 / -842 | 14.99 | 14.68 | 2.8 / 4.8 | ja | 8.6 | Kies | elfenwald | meer | breit>1,5m | 68 |
| 155 | B_R_P3_M2_03 | d | mulde | G3 | 2182 / -1458 | 47.34 | 47.07 | 2.8 / 2.9 | schwach | 15.5 | Kies | elfenwald | zusammenfluss | breit>1,5m | 68 |
| 156 | B_R2_K8_ELFENFALL_01 | d | mulde | H3 | 2638 / -1124 | 62.24 | 61.98 | 2.8 / 5.1 | ja | 16.7 | Kies | elfenwald | fortsetzung | breit>1,5m | 68 |
| 157 | B_R2_R_P3_M2_02 | d | mulde | G3 | 2206 / -1650 | 38.51 | 38.23 | 2.8 / 4.0 | schwach | 22.7 | Kies | elfenwald | fortsetzung | breit>1,5m | 68 |
| 158 | B_R2_R_P3_M2_03 | d | mulde | G3 | 1902 / -1638 | 36.20 | 36.01 | 2.8 / 4.0 | schwach | 17.6 | Kies | elfenwald | fortsetzung | breit>1,5m | 68 |
| 159 | B_R_M3_M2_01 | d | mulde | B3 | -3694 / -1286 | 51.89 | 52.29 | 2.0 / 4.8 | ja | 50.9 | Kies | bergwald | nichts | breit>1,5m, Ende versickert | 65 |
| 160 | B_R_M3_P1_01 | d | mulde | B6 | -3650 / 1074 | 44.90 | 44.98 | 2.0 / 4.8 | ja | 31.2 | Wiese | bergwald | nichts | breit>1,5m, Ende versickert | 65 |
| 161 | B_R_P4_M1_01 | b | zusammenfluss | H3 | 2420 / -1250 | 39.45 | 39.24 | 4.8 / 4.0 | nein | 24.5 | Kies | elfenwald | zusammenfluss | breit>1,5m, keine Verjüngung | 63 |
| 162 | B_R_P0_M2_01 | d | mulde | D2 | -732 / -2250 | 48.73 | 49.77 | 2.0 / 5.7 | ja | 14.0 | Moos | tundra | fortsetzung | breit>1,5m | 60 |
| 163 | B_R_P2_P0_04 | b | zusammenfluss | G5 | 1344 / 496 | 6.55 | 6.20 | 4.0 / 2.9 | nein | 4.4 | Trockengras | heide | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 60 |
| 164 | B_R_P4_M2_04 | d | mulde | H3 | 2954 / -1276 | 172.96 | 172.77 | 2.0 / 4.0 | ja | 60.3 | Kies | elfenwald | fortsetzung | breit>1,5m | 60 |
| 165 | B_R2_R_P4_M1_02 | d | mulde | H3 | 2536 / -1180 | 45.10 | 45.15 | 2.0 / 4.7 | ja | 17.3 | Kies | elfenwald | fortsetzung | breit>1,5m | 60 |
| 166 | F_ERLENBACH_1V_C2 (p2) | d | mulde | D2 | -1680 / -2768 | 189.96 | 189.47 | 1.8 / 2.3 | schwach | 67.5 | Fels | fjord | fortsetzung | breit>1,5m | 58 |
| 167 | B_R_P3_M1_01 | b | zusammenfluss | G3 | 1786 / -1250 | 22.35 | 22.08 | 4.0 / 4.0 | nein | 15.4 | Kies | elfenwald | meer | breit>1,5m, keine Verjüngung | 55 |
| 168 | B_R2_R_M1_P0_04 | b | zusammenfluss | C5 | -2650 / 410 | 46.29 | 46.03 | 4.0 / 4.0 | nein | 9.4 | Kies | aue | fortsetzung | breit>1,5m, keine Verjüngung | 55 |
| 169 | B_R2_R_P4_P1_01 | b | zusammenfluss | I6 | 3350 / 994 | 13.26 | 13.02 | 4.0 / 3.0 | nein | 5.7 | Laub | dschungel | zusammenfluss | breit>1,5m, keine Verjüngung | 55 |
| 170 | B_R2_R_M1_P0_03 | b | abzweig | C5 | -2654 / 198 | 45.54 | 45.49 | 2.0 / 4.0 | ja | 9.7 | Trockengras | bergwald | fortsetzung | breit>1,5m | 40 |
| 171 | B_R2_R_M3_P1_01 | b | abzweig | B6 | -3650 / 1274 | 7.38 | 7.32 | 2.0 / 4.8 | ja | 7.6 | Wiese | bergwald | fortsetzung | breit>1,5m | 40 |
| 172 | B_R2_R_M1_M1_02 | b | zusammenfluss | C4 | -2654 / -608 | 56.20 | 56.74 | 2.0 / 3.7 | ja | 13.0 | Kies | bergwald | nichts | breit>1,5m, Ende versickert | 30 |
| 173 | B_R2_R_M1_M1_04 | b | wasserfall | C4 | -2606 / -864 | 41.07 | 41.16 | 2.0 / 4.0 | ja | 8.8 | Kies | aue | fortsetzung | breit>1,5m | 25 |
| 174 | B_R2_R_P3_M1_02 | b | zusammenfluss | H4 | 2354 / -996 | 19.58 | 19.19 | 2.0 / 4.0 | ja | 10.5 | Kies | elfenwald | see | breit>1,5m | 25 |
| 175 | F_HAUPTFLUSS_3_C5 | b | fortsetzung | C4 | -2515 / -30 | 30.79 | 29.38 | 48.0 / 50.0 | schwach | 5.7 | Kies | aue | fortsetzung | breit>1,5m | 15 |
| 176 | F_HAUPTFLUSS_3_D5 | b | fortsetzung | C5 | -1714 / 251 | 21.60 | 19.27 | 67.0 / 67.0 | nein | 0.1 | Geroell | aue | fortsetzung | breit>1,5m, keine Verjüngung | 15 |
| 177 | F_HAUPTFLUSS_3_E5 | b | fortsetzung | D5 | -705 / 538 | 18.99 | 16.98 | 63.0 / 69.0 | schwach | 0.9 | Geroell | aue | fortsetzung | breit>1,5m | 15 |
| 178 | F_HAUPTFLUSS_3_F5 | b | fortsetzung | E5 | 298 / 802 | 8.43 | 5.90 | 98.0 / 101.0 | schwach | 2.7 | Geroell | oedland | meer | breit>1,5m | 15 |
| 179 | F_CANYONBACH_D5 | b | fortsetzung | D4 | -1091 / -42 | 24.11 | 22.74 | 40.0 / 41.0 | schwach | 1.0 | Geroell | aue | zusammenfluss | breit>1,5m | 15 |
| 180 | F_ERLENBACH_2_C3 | b | fortsetzung | C2 | -1738 / -2055 | 37.78 | 36.39 | 36.0 / 35.0 | nein | 2.6 | Geroell | tundra | fortsetzung | breit>1,5m, keine Verjüngung | 15 |
| 181 | F_ERLENBACH_3_D3 | b | fortsetzung | D3 | -1646 / -1713 | 12.37 | 11.02 | 75.3 / 59.9 | nein | 9.4 | Schlamm | tundra | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 15 |
| 182 | F_ELFENFLUSS_3_H4 | b | fortsetzung | H4 | 2711 / -547 | 67.21 | 65.76 | 41.0 / 39.7 | nein | 16.0 | Schlamm | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung | 15 |
| 183 | F_ELFENFLUSS_3_G4 | b | fortsetzung | H4 | 2334 / -538 | 23.98 | 22.64 | 42.0 / 41.7 | nein | 5.8 | Geroell | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung | 15 |
| 184 | F_ELFENFLUSS_3_F4 | b | fortsetzung | G4 | 1321 / -403 | 12.24 | 10.05 | 72.0 / 73.4 | schwach | 5.7 | Kies | aue | meer | breit>1,5m | 15 |
| 185 | F_DSCHUNGELFLUSS_H6 | b | fortsetzung | H5 | 3288 / 975 | 6.54 | 6.54 | 26.0 / 27.0 | schwach | 0.0 | Geroell | dschungel | fortsetzung | breit>1,5m | 15 |
| 186 | F_DSCHUNGELFLUSS_H7 | b | fortsetzung | H6 | 2526 / 1980 | 6.48 | 5.11 | 66.1 / 59.3 | nein | 1.5 | Laub | dschungel | meer | breit>1,5m, keine Verjüngung | 15 |
| 187 | F_ERLENBACH_2V_D3 | b | fortsetzung | D3 | -1660 / -1852 | 33.33 | 32.38 | 40.7 / 38.1 | nein | 9.1 | Trockengras | tundra | fortsetzung | breit>1,5m, keine Verjüngung | 15 |
| 188 | F_ALTARM_FLUSSAUE_E5 | b | fortsetzung | D5 | -707 / 466 | 18.69 | 17.72 | 14.3 / 9.5 | nein | 1.4 | Schlamm | aue | zusammenfluss | breit>1,5m, keine Verjüngung | 15 |
| 189 | F_ELFENFLUSS_2_H4 | b | fortsetzung | H4 | 2914 / -635 | 108.45 | 107.73 | 32.0 / 28.9 | nein | 13.4 | Kies | elfenwald | fortsetzung | breit>1,5m, keine Verjüngung | 15 |
| 190 | B_R_P3_P1_04 | a | seeabfluss | G6 | 1574 / 1216 | 11.43 | 11.01 | 7.7 / 3.7 | nein | 11.9 | Trockengras | dschungel | nichts | breit>1,5m, keine Verjüngung, Ende versickert | 15 |
| 191 | B_R_P5_P1_03 | b | fortsetzung | I6 | 3720 / 1462 | 25.86 | 25.72 | 4.0 / 4.0 | nein | 22.6 | Laub | dschungel | meer | breit>1,5m, keine Verjüngung | 15 |
| 192 | B_R2_R_M1_M1_07 | a | seeabfluss | C4 | -2072 / -634 | 26.92 | 26.66 | 4.0 / 4.0 | nein | 2.9 | Trockengras | aue | fortsetzung | breit>1,5m, keine Verjüngung | 15 |
| 193 | B_R2_R_P3_P0_05 | a | seeabfluss | G5 | 1680 / 710 | 15.59 | 15.66 | 2.0 / 5.0 | ja | 1.9 | Schlamm | heide | fortsetzung | breit>1,5m | 15 |

## Hinweise

- Felsen/Bachdekor-Akteure (Felsschalen, Bachdekor) wurden NICHT gegen die Anfänge geprüft (nur Gelände, Lagen, Biom, Gewässer).
- Für den Erlenbach p2 gilt die Bettbreite aus `lauf_p2.json`; das Spline-Band im Editor ist 2 m breiter (SWR-Simulationsbereich).
- „Quellmulde“ nach Vorgabe (≥ 3 von 4 Seiten steigen in 10 m um ≥ 0,5 m) trifft in Kerbtälern fast immer zu; „schwache Mulde“ = dritthöchster Anstieg < 1 m.
- Kameras für die 6 schlimmsten Fälle: `live/claude_code/swr/_kam_anfaenge.json` (15 m talwärts auf der Spline, Blick bachauf auf den Anfang, Hoch −170).
- Bild: `docs/pruefung/wasser/bach_anfaenge.png` (Schummerung, Gewässer, Anfänge farbig: rot e, orange d, weiß c, gelb b, blau a; Nummern = Top 20).
