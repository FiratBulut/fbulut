# 19 – Bach- und Flussanfänge: 43 beginnen aus dem Nichts, alle 177 mit voller Breite (FERAT 13.10. 21:00)

Ferat: „Prüfe die River-Splines, vor allem wo ein Bach startet – nicht, dass er aus dem Nichts auftaucht.“ Messlatte Witcher 4.

## Befund (lokale Prüfung aller 193 Fließgewässer, `daten/bach_anfaenge/bach_anfaenge.md|json|png`)

| Klasse | Anzahl |
|---|---|
| e – aus dem Nichts (offener Hang, keine Quelle erkennbar) | **43** |
| d – Quellmulde / Hangfuß unter Fels | 93 |
| c – Gletscher / Schnee | 7 |
| b – Abzweig / Fortsetzung / Zusammenfluss / Lücke / Wasserfall | 47 |
| a – Seeabfluss | **3** |

- **Alle 177 echten Anfänge beginnen breiter als 1,5 m; 115 ohne jede Verjüngung** (Breite bei Punkt 0 = Breite nach 20 m). Kein Bach beginnt als Rinnsal.
- **Enden:** 59 versickern im Nichts, 18 Meer, 22 Zusammenfluss, 6 See, 88 Fortsetzung an Feldgrenzen.
- Die 20 schlimmsten Fälle mit Vorschlag stehen im MD (Schwere aus Klasse, Anfangsbreite, Verjüngung, Ende). Spitze:
  1. `F_CANYONBACH_D4` – 51 m breit aus dem Nichts (Trockengras, Canyon).
  2. `F_DSCHUNGELFLUSS_H5` – 49 m breit aus dem Nichts (Sumpf, 72 m neben Teich `T_3313_789`).
  3. `F_HAUPTFLUSS_3_C4` – 47 m breit; Vorgänger `F_HAUPTFLUSS_2_B4` endet 570 m entfernt und 156 m höher = die **offene Kaskade K1 (B4/C4)**, dort fehlt das Epic-Wasser noch (bekannt).
  4. `F_HAUPTFLUSS_2_B4` – Lücke, 37 m breit.
  5. `F_HAUPTFLUSS_1_B4` – 32 m breit aus dem Nichts (Bergwald).
  Dann Elfenfluss H4 (Wasserfall, ok?), Gletschertal D2, Erlenbach 2 D3 (Abzweig) und 12 Bäche „e“ mit 2–4 m Breite.
- Daten je Gewässer: Feld, Anfang X/Y/Z, Breite Anfang/+20 m, Gefälle, Lagen, Biom, Mulde (Anstieg in 4 Richtungen), Fels hangauf, nächste Gewässer, Ende.

## Auftrag

1. **Regeln „Wie beginnt ein Bach“ je Klasse und Biom** (Witcher 4 / Witcher 3 als Maß): Quellmulde mit Quellfelsen und Moos („Quellfassung“, 3–6 Felsen 0,6–1,5 m, Moospolster, Farn, nasser Boden), Schneefeld-/Gletscherfuß (Schmelzwasser aus Schutt), Seeabfluss (Lippe), Zusammenfluss, Karst-/Felsquelle (Wasser tritt unter einer Felsplatte aus). Dazu das **Breitenprofil am Anfang**: ab welcher Länge welche Breite (z. B. 0,3 m → volle Breite über 30–60 m?) und die Tiefe.
2. **Je Klasse-e-Fall ein Plan** (43 Stück, die 12 breiten zuerst): Anfang verlängern/verlegen (Koordinaten), Quellfassung setzen, oder an einen See anschließen. Für die 3 großen Flüsse (Canyonbach D4 51 m, Dschungelfluss H5 49 m, Hauptfluss B4 32 m): Was ist glaubwürdig – Quellsee (Water-Brush-Becken 40–60 m), Zufluss aus einer Schlucht, Karstquelle? Für Hauptfluss C4: Kaskade K1 (bekannt offen) – bitte als eigenen Punkt einplanen.
3. **Breitenverjüngung als Regel für alle Bäche** (Planer-Vorgabe, die unsere `baeche_bauen.py`-Splines nachziehen können: Breite je Punkt im Anfangsbereich).
4. **Enden**: die 59, die versickern – Regel (Versickern im Geröll/Moor ist ok, aber sichtbar: Schotterfächer, Moorwiese) und Liste.
5. Ausgabe als JSON im Format der bisherigen Pläne (Instanzen FORMAT §3 + Spline-Änderungen je Gewässer: neue Punkte [X, Y, Z, Breite, Tiefe, Tempo] cm) plus Bilder/Skizzen je Typ.

Das Werkzeug `scripts/wasser/bach_anfaenge.py` kann nach Änderungen jederzeit neu laufen (1 min); die Klassen-Schwellen stehen im MD unter „Hinweise“.
