# Auftrag 15e – Rechteckige Abgrabungen abseits des Bachs (C2), Lagen enden an der Feldgrenze

Stand 11.10.2026, 20:40. Plan C2 lokal auf 1 m (Stand 1af3fb2, mit lokaler Biom-Korrektur aus 15d, Biom tundra). **Das hält den C2-Bau auf.**

## 1. Rechteckige Abgrabungen 25–60 m neben dem Bach (Hauptbefund)

Das Delta `gelaende/F_ERLENBACH_1V_C2_s1.f32` (Fenster i0 1615, j0 2887, 281 × 180) enthält drei große, gerade begrenzte Abgrabungen, die mit Bett,
Ufer oder Kolk nichts zu tun haben. Ausgewertet wurden Zellen mit Δ < −0,5 m und mehr als 25 m Abstand zur Mittellinie `spiegel_neu_cm`:

| Bereich | Zellen | X (m) | Y (m) | Abtrag Mittel / max | Abstand zum Bach |
|---|---|---|---|---|---|
| 1 – schräges Quadrat am Osthang (C2/D2) | 1 344 | −1714 … −1670 | −2374 … −2330 | 5,28 / **9,35 m** | 25–60 m |
| 3 – Band West | 166 | −1822 … −1808 | −2248 … −2236 | 1,92 / 3,24 m | 26–40 m |
| 4 – Keil Ost (gleiches Y-Band wie 3) | 264 | −1752 … −1722 | −2248 … −2236 | 6,19 / **12,68 m** | 30–60 m |

- Bild: [`bilder/gefaelle/c2_delta_1m.png`](../bilder/gefaelle/c2_delta_1m.png). Schummerung des heutigen Geländes, blau = Abtrag (voll blau = 10 m),
  gelb = neue Wasserlinie, rote Senkrechte = Feldgrenze C2/D2.
- Abtrag nach Abstand zur Mittellinie: 0–10 m 8 420 m³, 10–20 m 2 527 m³, 20–30 m 440 m³, **30–45 m 3 529 m³, 45–80 m 5 173 m³**. Zusammen sind das 20 124 m³,
  davon 43 % weiter als 30 m vom Bach.
- Das Quadrat war schon im ersten Testbild sichtbar (`test_F_ERLENBACH_1V_C2_s1.png`, blaues Rechteck rechts, „Stempel max 9,7 m“).
- Die Ursache sehe ich offline nicht. In Frage kommen ein Stempel für Akteure (Fallwand/Held, Freiraum) mit falscher Lage oder Drehung, eine Wandzone mit falscher Seite oder
  ein Fallbecken- bzw. Kolk-Rechteck in Weltachsen statt entlang des Laufs. Bereiche 3 und 4 liegen bei s ≈ 150–160 m, Bereich 1 neben s ≈ 36 m.

**Bitte:** Ursache finden und beheben. Prüfer-Regel: Δ mit |Δ| > 0,3 m nur innerhalb von Netzrand + Uferring + Wandzone, sonst FEHLER (auch auf 2 m).

## 2. Lagen enden an der Feldgrenze, das Delta nicht

- Das Delta ändert 1 247 Zellen in D2 (j ≥ 3024), bis −9,35 m. Das ist fast nur Bereich 1.
- Die Lagen-Dateien `lagen/F_ERLENBACH_1V_C2_s1_<Lage>.r8` (Fenster 1614/2886, 283 × 181) sind in den D2-Spalten für alle 6 Lagen überall 0.
- **Bitte:** Lagen über das ganze Delta-Gebiet ausgeben, über Feldgrenzen hinweg. Prüfer-Regel: Jede Zelle mit |Δ| > 0,3 m braucht eine Lagenzuweisung.

## Bitte zusammen mit 15d pushen

Erst danach rechne ich C2 neu und baue. Das Einbau-Werkzeug ist fertig, im Trockenlauf ok; den Feldschreiber habe ich gegen den Plugin-Quelltext
geprüft.
