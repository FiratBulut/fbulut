# Antwort zu Auftrag 15c – Nachtest auf 1 m nach 15b

Stand 11.10.2026. Die Fassung ist Commit **`4ccb479`**.

## Kurzfazit

- **B_R_P4_M2_04_KN0 (Bett):** Die Ursache ist gefunden und behoben. Der Planer-Prüfer meldet jetzt 0 FEHLER.
  - Die Bettprobe direkt unter dem 15-m-Fall am Segmentanfang lag nur 0,7 m neben der Oberwasser-Seitenwand.
  - Bilinear auf 1 m zog die Wand das gemittelte Bett hoch. In der Cloud blieb es mit 0,00 m Reserve gerade noch
    knapp richtig, lokal knapp falsch.
  - Abhilfe: Becken unter Stufen ≥ 1,5 m sind mindestens 5 m breit, und das Bett liegt 0,7 m statt 0,5 m tief.
  - Die kleinste Bett-Reserve aller 19 Pilotläufe liegt jetzt bei +0,09 m. Dort lag der Fehler vorher bei 0,00 m,
    jetzt bei +0,24 m.
- **Die 7 Einzelpunkte sind bestätigt.**
  - 5 sind Mündungen: Die Probe liegt 0,3–1,4 m neben der Zuflusslinie, das Ufer ist dort zu Recht offen.
  - 2 sind Bestand (D3): WARNUNG.
  - Keiner ist „nahe Stufe“; auf 1 m schließt der Prüfer nichts wegen Stufennähe aus.
  - Die Mündungs-Ausnahme gilt jetzt nur noch für die eine Seite an der Zuflusslinie.
- **River < 15 m** gibt der Planer jetzt als Rampe im Kaskadennetz aus. Bei C2 wird `R0` zu `KN0` mit
  `rampen_s_m` [0, 10]. Der Prüfer meldet River < 15 m als FEHLER.
- **Läufe:**

  | Lauf | Läufe | FEHLER | WARNUNG | Anmerkung |
  |---|---|---|---|---|
  | 19 Pilotläufe, `--hoehe1m-fenster` | 19 | 0 | 10 | zweiter Lauf byteidentisch |
  | alle 161 Strecken, 2 m | 98 mit Stufen | 0 | 27 | kein River < 15 m |

- **C2:** Nur `wasser_koerper` ändert sich (R0 → Rampe in KN0). Gelände-Delta, Lagen, Instanzen, Stufen, Effekte und
  Kameras sind **byteidentisch** zur Fassung 15b (93ca592). Der laufende Einbau von C2 kann bleiben. Er baut R0 lokal
  schon als Rampe.

## 1. B_R_P4_M2_04_KN0 – Bett an 1 von 132 Beckenpunkten

**Befund:**

- Der KN0 beginnt mit einem Fall von 15,4 m direkt am Segmentanfang (s = 5,2 m). Oberhalb liegt die feste Zone an
  elfenwald_04_elfentreppe.
- Der erste Beckenpunkt liegt 1,4 m hinter dem Fuß, bei einem Bach von 3,5 m Breite.
- Neben dem Fuß steht 1,5 m lang die Oberwasser-Seitenwand des Falls. Das ist absichtlich so (15b, `ufer_z`); sie liegt
  bei halber Breite, also 0,7 m neben der Bettprobe (mittlere 60 %).
- Auf 1 m mischt die bilineare Abfrage die 15 m hohe Wand ins Bett. Cloud-Nachmessung: Reserve 0,00 m. Lokal fiel der
  Punkt um wenige Zentimeter darunter.
- Die Ursache liegt also in der Geometrie: Die Wand steht zu nah am nassen Bett. Das 2-m-Restraster spielt keine Rolle.

**Entscheidung:** Die Geometrie wird geändert, kein Prüf-Zuschlag:

1. Becken unter Stufen ≥ 1,5 m sind von der Lippe bis Kolkende + 1,5 m mindestens 5 m breit. Die Breite ändert sich
   weiter höchstens um 0,2 m je m. Damit liegt die Seitenwand ≥ 1 m, also eine 1-m-Zelle, neben dem nassen Bett.
2. Das Bett liegt mindestens 0,7 m unter dem Spiegel (vorher 0,5 m). Das gibt Sicherheitszuschlag gegen Rasterreste.

**Ergebnis:**

- Der Punkt hat jetzt +0,24 m Reserve.
- Die kleinste Bett-Reserve aller 19 Pilotläufe liegt bei +0,09 m (B_R_P3_M2_01 KN1), sonst bei ≥ +0,11 m.
- Die Ufer-Reserven bleiben wie in 15b. Lokal gab es dort keinen Befund mehr.

## 2. Die 7 Einzelpunkte

Die Punkte stammen aus der Nachmessung in 15c. Bei mir haben sie dieselben X/Y. Die k-Nummern sind bei B_R_P1_M2_01
und B_R_P3_M2_01 um 5 verschoben (217–218 bzw. 132–134), weil die Beckenpunkte auf 2 m und 1 m etwas anders verteilt
sind.

| Lauf | Netz / k (15c) | Seite | Abstand zur Zuflusslinie | Mein Prüfer | Sachlich | Entscheidung |
|---|---|---|---|---|---|---|
| B_R_P1_M2_01 | KN0 / 212 | links | 1,2 m (Zufluss B_R2_R_P1_M2_01, 2 m breit) | Mündung | ja: die Probe liegt in der Zuflussrinne | bleibt offen |
| B_R_P1_M2_01 | KN0 / 213 | links | 0,3 m | Mündung | ja | bleibt offen |
| B_R_P3_M2_01 | KN1 / 127 | rechts | 1,1 m (Zufluss B_R2_R_P3_M2_01, 2 m breit) | Mündung | ja | bleibt offen |
| B_R_P3_M2_01 | KN1 / 128 | rechts | 0,4 m | Mündung | ja | bleibt offen |
| B_R_P3_M2_01 | KN1 / 129 | rechts | 1,4 m | Mündung | ja (fehlt nur 0,01 m) | bleibt offen |
| F_ERLENBACH_2V_D3 | KN0 / 32 | links | – | Bestand (WARNUNG) | ja: altes Ufer 22,24 m, Spiegel 23,53 m | WARNUNG, wie lokal bestätigt |
| F_ERLENBACH_2V_D3 | KN0 / 33 | links | – | Bestand (WARNUNG) | ja: altes Ufer 22,02 m, Spiegel 23,50 m | WARNUNG |

**Engere Mündungs-Ausnahme:**

- Bisher galt die Ausnahme für beide Seiten und für ±(Zuflussbreite/2 + 2 m) entlang des Laufs. Jetzt gilt sie nur
  für die Uferprobe, die ≤ Zuflussbreite/2 + 1 m von der Zuflusslinie liegt.
- Die Zuflusslinie ist bis zur Mittellinie verlängert und steht im Netz unter `muendungen[].linie_cm`.
- Die Gegenseite und die Nachbarpunkte werden normal geprüft und haben den Uferring.
- Der Uferring hebt an der Zuflusslinie selbst nicht an, sonst würde er die Mündung abdämmen.
- Planer und `gefaelle_pruefen.py` prüfen das Ufer jetzt je Seite. Sie nutzen dieselbe Funktion `ufer_proben`.

**„Nahe Stufe“** gibt es nur auf 2 m (Rasterzuschlag). Auf 1 m und mit `--hoehe1m-fenster` werden alle Beckenpunkte
geprüft.

## 3. Kurze River-Stücke

- Ein River-Eintrag unter 15 m wird nicht mehr ausgegeben. Das betrifft den Laufanfang, das Laufende und Stücke
  zwischen zwei Netzen.
- Das Stück wird Teil des Kaskadennetzes:
  - Am Laufanfang beginnt das Netz bei s = 0, am Laufende endet es am Laufende.
  - Zwei Netze mit kurzem River dazwischen werden ein Netz.
- In diesem Stück haben die Punkte `knick` = `rampe`. Das Netz bekommt `rampen_s_m` mit den Bereichen.
  - Steile Teile (> 2 %) sind schnell und schäumen leicht (Tempo 300, Fallanteil 0,5).
  - Flache Teile sind ruhig wie Becken (Tempo 80, kein Schaum).
- Der Prüfer meldet River < 15 m als FEHLER.
- Alle 161 Strecken: Es gibt keinen River < 15 m mehr.
- Beispiele:
  - **C2:** `KN0` 0–174,5 m mit Rampe 0–10 m, danach nur `R0` 174,0–203,2 m. Der alte River `R0` 0–10,5 m entfällt,
    der alte `R1` heißt jetzt `R0`.
  - **B_R_P1_M2_01:** ganz ein Netz, mit Rampen 0–9,5 m und 328,8–341,3 m.

## 4. Ergebnis

| Lauf | FEHLER | WARNUNG | Inhalt der WARNUNGEN |
|---|---|---|---|
| 19 Pilotläufe auf 1-m-Fenstern | 0 | 10 | 7 × Stufen ≥ 1 m ohne Niagara (Grenze gleichzeitig), 2 × Beckengefälle 2–3 %, 1 × Bestand D3 (2 Proben) |
| Alle 161 Strecken auf 2 m | 0 | 27 | |

- Zwei Läufe ergeben byteidentische Ausgaben (`diff -r` ohne Bilder).
- Die Testbilder sind neu erzeugt, unverändert.

## 5. C2

Gegenüber 15b (93ca592) ändert sich **nur `wasser_koerper`**: R0 (10,5 m) wird Rampe in KN0, `muendungen` steht
jetzt im Netz.

- **Byteidentisch:** Stufen, Spiegel, `gelaende/F_ERLENBACH_1V_C2_s1.f32`, Lagen, Instanzen, Effekte und Kameras.
- **Ufer- und Bettprüfung:** 0 FEHLER.
- Der Mindestwert von 0,7 m für das Bett greift bei C2 nicht: Die Flusstiefe ist größer.
- Die 5-m-Fallbecken greifen auch nicht: C2 ist 9–28 m breit.
- Der laufende Einbau muss also nichts neu machen. Er baut R0 schon als Rampe.

## 6. Aufruf

```
# lokal (1 m)
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis .
# Cloud-Test
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --daten2m recherche/vorlagen/daten/sehens \
    --hoehe1m-fenster recherche/vorlagen/daten/gefaelle/hoehe_1m_fenster --aus <scratchpad>/a15c/plan
```
