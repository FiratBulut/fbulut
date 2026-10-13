# 19 – Bach- und Flussanfänge: 83 beginnen aus dem Nichts, keiner beginnt schmal (FERAT 13.10. 21:00)

Ferat: „Prüfe die River-Splines, vor allem wo ein Bach startet – nicht, dass er aus dem Nichts auftaucht.“ Messlatte Witcher 4.

## Befund (lokale Prüfung aller 193 Fließgewässer, `daten/bach_anfaenge/bach_anfaenge.md|json|png`, Werkzeug `scripts/wasser/bach_anfaenge.py`)

Mulde gemessen ab Uferniveau (Ring-Median) – mit der Bettsohle würde das eingeschnittene Bett eine Mulde vortäuschen (dann 93 d / 43 e).

| Klasse | Anzahl |
|---|---|
| e – aus dem Nichts (offener Hang, keine Quelle erkennbar) | **83** (78 Bäche, 5 Flüsse; Biome aue 36, dschungel 12, heide 10, bergwald 9, elfenwald 9, tundra 4; Felder G5 10, C4 8, G4 7, G6 6) |
| d – Quellmulde / Hangfuß | 53 (26 davon nur schwach, < 1 m Anstieg – im Spiel kaum als Quelle lesbar) |
| c – Gletscher / Schnee | 7 (nur 3 mit Schnee/Eis in 20 m; 4 ohne Gletschertor, u. a. `F_GLETSCHERTAL_D2`) |
| b – Fortsetzung 17 / Zusammenfluss 15 / Abzweig 10 / Wasserfall-Fuß 4 / Lücke 1 | 47 |
| a – Seeabfluss | **3** |

- **Kein Bach beginnt schmal:** Anfangsbreite Bäche min 2,0 m, Median 4,0 m, 122 von 167 ≥ 4 m; **125 von 193 ohne jede Verjüngung**, nur 32 verjüngen
  deutlich. Ursache: Die Houdini-Exporte tragen am ersten Punkt die volle Breite, `baeche_bauen.py` klemmt die Tiefe auf ≥ 40 cm.
- **Enden:** Fortsetzung 88, Meer 50, Zusammenfluss 22, See 6, Lücke ≤ 60 m 14, Wasserfallkante voraus 3, **versickert im Nichts 8**
  (u. a. `F_HAUPTFLUSS_2_B4` Ende bei 198 m, `B_R3_K12_WUESTE_01` 13,9 m breit).
- Die 20 schlimmsten mit Vorschlag im MD. Spitze: 1 `F_CANYONBACH_D4` (51 m, Gefälle 0 %, Canyon-Kopf; Teich `T_-1344_-574` 330 m entfernt und 12 m
  höher → Quelle + Wasserfall?), 2 `F_DSCHUNGELFLUSS_H5` (49 m, Sumpf → Quellsumpf-See), 3 `F_HAUPTFLUSS_3_C4` (47 m; beginnt 570 m unter dem Ende
  von `2_B4`, 156 m tiefer = **Kaskade K1**, bekannt offen), 4/5 `F_HAUPTFLUSS_2_B4` + `F_ELFENFLUSS_1_H4` (Wasserfall-Fuß, in Ordnung),
  6 `F_HAUPTFLUSS_1_B4` (21 m breiter 30-m-Stummel oberhalb WF_K1 ohne Quelle → Karsee ≈ 60 × 80 m bei 288 m?).
  Schlimmste Bäche: `B_R_P3_P1_03` (G6, 11,3 m, 21 m neben See `S_R_P3_P1_01` → Seeabfluss), `B_R_M1_M1_01` (C3, 8 m), `B_R_M2_P0_01` (B5),
  `B_R_M2_P1_03` (B6, Lavafels), `B_R_P3_P2_01`, `B_R2_R_P3_P1_05` (G6) – alle volle Breite ab Punkt 0, keine Mulde in 50 m hangauf.
- 10 der 83 e-Anfänge haben ≤ 50 m hangauf eine Mulde (`mulde_vorschlag` im JSON mit Koordinaten); 2 Anfänge liegen ≤ 60 m an einem See.
- Daten je Gewässer: Feld, Anfang/Ende X/Y/Z, Breite Anfang/+20 m, Gefälle, Lagen, Biom, Mulde (Anstieg in 4 Richtungen), Fels hangauf, nächste Gewässer.

## Auftrag

1. **Regeln „Wie beginnt ein Bach“ je Klasse und Biom** (Witcher 4 / Witcher 3 als Maß): Quellmulde mit Quellfelsen und Moos („Quellfassung“, 3–6 Felsen 0,6–1,5 m, Moospolster, Farn, nasser Boden), Schneefeld-/Gletscherfuß (Schmelzwasser aus Schutt), Seeabfluss (Lippe), Zusammenfluss, Karst-/Felsquelle (Wasser tritt unter einer Felsplatte aus). Dazu das **Breitenprofil am Anfang**: ab welcher Länge welche Breite (z. B. 0,3 m → volle Breite über 30–60 m?) und die Tiefe.
2. **Je Klasse-e-Fall ein Plan** (43 Stück, die 12 breiten zuerst): Anfang verlängern/verlegen (Koordinaten), Quellfassung setzen, oder an einen See anschließen. Für die 3 großen Flüsse (Canyonbach D4 51 m, Dschungelfluss H5 49 m, Hauptfluss B4 32 m): Was ist glaubwürdig – Quellsee (Water-Brush-Becken 40–60 m), Zufluss aus einer Schlucht, Karstquelle? Für Hauptfluss C4: Kaskade K1 (bekannt offen) – bitte als eigenen Punkt einplanen.
3. **Breitenverjüngung als Regel für alle Bäche** (Planer-Vorgabe, die unsere `baeche_bauen.py`-Splines nachziehen können: Breite je Punkt im Anfangsbereich).
4. **Enden**: die 59, die versickern – Regel (Versickern im Geröll/Moor ist ok, aber sichtbar: Schotterfächer, Moorwiese) und Liste.
5. Ausgabe als JSON im Format der bisherigen Pläne (Instanzen FORMAT §3 + Spline-Änderungen je Gewässer: neue Punkte [X, Y, Z, Breite, Tiefe, Tempo] cm) plus Bilder/Skizzen je Typ.

Das Werkzeug `scripts/wasser/bach_anfaenge.py` kann nach Änderungen jederzeit neu laufen (1 min); die Klassen-Schwellen stehen im MD unter „Hinweise“.
