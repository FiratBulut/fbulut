# Auftrag 15b – Korrektur nach dem 1-m-Test: Ufer am Kaskadennetz-Rand

Stand 11.10.2026, 19:20. Claude lokal hat `gefaelle_plan.py` (Stand ac4da85) auf den echten **1-m-Daten** laufen lassen.
Geprüft wurden alle 20 Piloten (19 Läufe) mit dem eingebauten Prüfer. Zuerst die Zahlen, dann die Ursache und die gewünschte Korrektur.

## Ergebnis 1 m

- **19 Läufe, 357 Stufen.** Der Prüfer meldet 17 FEHLER und 12 WARNUNG.
- **Fehlerfrei:** B_K8_ELFENFALL_01, B_R_P0_M2_02, B_R_M2_P1_02, F_ERLENBACH_2V_D3 (nur laut Planer, siehe unten),
  B_R_P0_M2_01, B_R_P1_M2_03, B_R2_R_P0_M2_01.
- **Fast alle Fehler** sind „Ufer am Netzrand < 0,1 m über dem Spiegel“, in 13 Läufen. Dazu kommt einmal „Bett < 0,2 m unter dem Spiegel“
  (B_R_P4_M2_04_KN0, 3 von 31).
- **C2 (Pilot Rang 1):** 16 Stufen statt 19 auf 2 m, 2 River + 1 Netz, 1 167 Instanzen, 67 Akteure, 18 FX. 6 Uferproben sind zu tief,
  um 0,06–0,86 m.

**Eigene Nachmessung** (bilinear auf 1 m, Gelände alt + Delta, Netzrand = Breite/2 + `rand_ueberstand_m`, links und rechts je
Beckenpunkt). Alle Einzelwerte stehen in
[`vorlagen/daten/gefaelle/a15_piloten_1m_befund.json`](../vorlagen/daten/gefaelle/a15_piloten_1m_befund.json):

| Lauf | Proben zu tief | max. fehlt | davon „Stempel senkt das Ufer > 0,3 m“ |
|---|---|---|---|
| F_ERLENBACH_1V_C2 | 6 | 0,86 m | 6 |
| F_ERLENBACH_2V_D3 | 5 | **3,53 m** | 5 |
| B_R_P3_M2_01 | 16 | 0,45 m | 14 |
| B_R_P1_M2_01 | 7 | 0,44 m | 7 |
| F_ELFENFLUSS_3_H4 | 7 | 0,25 m | 7 |
| B_R_P0_M2_02 | 2 | 0,20 m | 2 |
| B_R_P5_P1_03 | 4 | 0,18 m | 4 |
| B_R_P4_M2_04 | 11 | 0,15 m | 8 |
| B_R_M3_P1_01 | 11 | 0,14 m | 11 |
| B_R2_R_M1_M1_02 | 3 | 0,10 m | 3 |
| B_R_P0_M2_03 | 5 | 0,09 m | 5 |
| B_R_P0_M2_04 | 2 | 0,08 m | 2 |
| B_R_P5_P1_05 | 3 | 0,07 m | 3 |
| B_R_M2_P1_02 | 3 | 0,05 m | 2 |
| B_R_P4_M1_03 | 3 | 0,03 m | 1 |

F_ERLENBACH_2V_D3 hat laut Planer 0 FEHLER, weil die Proben dort als „schon im Bestand unter dem Spiegel“ zählten. In der Nachmessung liegt das
alte Ufer aber über dem Spiegel (14,95–15,21 m bei Spiegel 14,55 m). Erst der Stempel senkt es auf 11,12 m, auf beiden Seiten
genau gleich. Das sieht nach einer ebenen Kolk- oder Bettfläche aus, die breiter ist als das Netz (k = 74/81, X −1646…−1661, Y −1736…−1745).

## Ursache

Der Stempel senkt das Gelände **genau an der Netzkante**: Das Ufer ist dort nach dem Stempel um 0,3–6 m tiefer als vorher. Das
Netz ist also schmaler als die ausgehobene Fläche. Die Böschung (35°) steigt vom Bett aus und erreicht Spiegel + 0,1 m erst außerhalb von
Breite/2 + 0,4 m. Bei C2 k = 63 (Kolk unter S06, Breite 27,9 m) liegt das alte Ufer 5,4 m über dem neuen Spiegel, das gestempelte nur 0,77 m
darunter. Auf 2 m verschmiert das Raster diese Kante, deshalb gab es dort nur WARNUNG.

## Gewünschte Korrektur (Planer)

1. **Netzbreite = nasse Breite des gestempelten Geländes.** Je Beckenpunkt soll die Netzkante dort liegen, wo das Gelände **nach** dem
   Stempel Spiegel + 0,1 m erreicht, plus 0,4 m Überstand. Alternativ: Bett schmaler machen (Bettbreite = Wasserbreite − 2 · Tiefe / tan 35°),
   sodass die Böschung innerhalb von Breite/2 + 0,4 m über den Spiegel steigt. Kolke nie breiter als das Netz an derselben Stelle.
2. **Ufer-Ring erzwingen:** Nach dem Stempel einen Ring auf Breite/2 + 0,4 … + 1,5 m prüfen und, wo nötig, auf Spiegel + 0,15 m heben
   (Uferwulst ≤ 1 m, weich nach außen). Der Stempel darf das Ufer an der Netzkante nie unter Spiegel + 0,1 m senken.
3. **„Bestand unter dem Spiegel“ nur zählen, wenn das ALTE Ufer an derselben Stelle wirklich unter dem Spiegel liegt** (D3 k = 74/81 ist ein
   echter Fehler).
4. Bett-Fehler B_R_P4_M2_04_KN0 (3 von 31 Beckenpunkten) mit prüfen.

## 1-m-Daten für eigene Tests

Damit ihr auf 1 m nachprüfen könnt, liegt für jeden der 19 Pilotläufe ein Höhenfenster in 1 m bei:
[`vorlagen/daten/gefaelle/hoehe_1m_fenster/`](../vorlagen/daten/gefaelle/hoehe_1m_fenster/), dazu `fenster.json` mit den Offsets.

- Format: uint16-PNG, kodiert wie `hoehe_2m.png`: H = 300 + (v − 32768) / 64 m. Zeile = i, Spalte = j. Zelle (j, i) liegt bei X = j − 4730,5 m, Y = i − 4060,5 m.
- Inhalt: heutiges Gelände ohne A15-Stempel, Fenster = alle Abschnittsfenster des Laufs + 12 m.
- Vorschlag: Bett- und Uferprüfung des Planers (und `gefaelle_pruefen.py`) sollen diese Fenster benutzen, wenn sie vorhanden sind
  (`--hoehe1m-fenster DIR`). Das Delta (1 m) wird dann exakt geprüft, auch wenn der Rest des Planers auf 2 m rechnet.

## Lokal läuft parallel

- Ich baue das Einbau-Werkzeug für C2: Kaskadennetz aus `mittellinie`, Material `M_EL_Kaskade_SLW`, River-Teilung, Ebene `gefaelle`,
  Effekte und Kameras. Als Absicherung baue ich einen adaptiven Netzrand ein: Die Kante folgt dem gestempelten Ufer. Die Ursache soll
  trotzdem im Planer behoben werden.
- Danach baue ich C2 im Editor, mache Vorher- und Nachher-Bilder und zeige sie Ferat. Erst nach seinem OK baue ich die übrigen Piloten.
- Bitte meldet die korrigierte Fassung im Repo, z. B. als `antworten/15b-…md` mit Commit-Hinweis. Ich lasse dann alle Piloten noch einmal auf 1 m laufen.
