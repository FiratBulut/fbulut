# Antwort zu Auftrag 15e – Rechteckige Abgrabungen abseits des Bachs, Lagen an der Feldgrenze

Stand 11.10.2026. Die Fassung ist Commit **`aaf330c`**. Die Vorfassung `34336b5` (nur C2) ist überholt: Der Uferring
liegt jetzt 5 cm höher.

## Kurzfazit

- **Ursache gefunden.** Es war kein Akteur-, Wand- oder Kolk-Rechteck. Die 35°-Uferböschung des Querprofils war eine
  **Obergrenze für das Gelände bis 60 m neben dem Bach**, und jeder Hang, der steiler als 35° ist, wurde
  abgeschnitten. Die Abgrabungen folgten deshalb den steilen Hangteilen, und ihre geraden Kanten lagen dort, wo die
  Berechnung endet: an der 60-m-Grenze und an den Segmentenden.
- **Behoben.** Außerhalb der Wasserbreite wird nur noch so viel abgetragen, wie die Eintiefung des Spiegels verlangt.
- **C2:** Abtrag weiter als 20 m vom Bach entfernt **0 m³** (vorher 50 %), max. Δ 7,4 m am Bach (vorher 12,4 m
  abseits).
- **Lagen:** Jede Zelle mit |Δ| > 0,3 m hat jetzt eine Lage, auch jenseits der Feldgrenze C2/D2.
- **Zwei neue Prüfer-Regeln**, beide FEHLER, auch auf 2 m:
  1. |Δ| > 0,3 m nur im erlaubten Bereich am Bach.
  2. Jede Zelle mit |Δ| > 0,3 m braucht eine Lage.
- **Alle Läufe geprüft.** Mit den neuen Regeln hatte der alte Stand bei allen 161 Strecken (2 m) 93 FEHLER:
  - Fehlstempel in 41 Abschnitten von 40 Läufen.
  - 36 Abschnitte mit Δ-Zellen ohne Lage.
- **Jetzt:**

  | Lauf | Läufe | FEHLER | WARNUNG | Anmerkung |
  |---|---|---|---|---|
  | 19 Pilotläufe, `--hoehe1m-fenster` | 19 | 0 | 10 | zweiter Lauf byteidentisch |
  | alle 161 Strecken, 2 m | 98 mit Stufen | 0 | 27 | |

- Das Testbild von C2 ist neu erzeugt: `gefaelle/test_F_ERLENBACH_1V_C2_s1.png`. Das blaue Quadrat ist weg.

## 1. Ursache

Das Querprofil `profil_T` (seit 15b) gab außerhalb der halben Breite eine Böschung vor:
max(35° ab der Wasserkante; Uferwand mit Uferwinkel). Der Stempel rechnet „neu = min(alt, Profil)“ für alle Zellen bis
60 m neben dem Bach (`reach`).

- Bei 35° liegt das Profil 40 m neben dem Bach etwa 28 m über dem Spiegel.
- Wo der Hang steiler ist, liegt das alte Gelände höher und wurde auf die 35°-Ebene abgeschnitten.
- Am Osthang von C2 (s ≈ 36 m) ergab das das schräge Quadrat bis 9 m tief. Die Kanten sind die Grenze des
  60-m-Bands und das Abschnittsfenster.
- Bei s ≈ 150–160 m ergaben sich die Bänder West und Ost bis 12,7 m. Ihre Kanten sind die Segmentgrenze: Die
  Projektion auf das Segmentende schneidet quer zum Lauf ab.

Der Fehler war schon vor 15b angelegt; die alte Uferböschung `z + 0,05 + (d − B/2) · tan 35°` hatte dieselbe
Wirkung. Die Lagen dagegen werden nur als Bänder entlang des Bachs gemalt (bis Breite + 4 m). Weit abseits gab es
deshalb Delta ohne Lage, in C2 die ganze D2-Seite.

## 2. Änderungen

Die Änderungen stehen in `skripte/gefaelle/gefaelle_plan.py` und `gefaelle_pruefen.py`.

1. **Abtrag begrenzt (`abtrag_grenze`, `aussen_begrenzen`).**
   - Außerhalb der halben Breite darf höchstens (Eintiefung + 0,5 m) − (d − halbe Breite) · tan 35° abgetragen
     werden. Die Eintiefung ist alter Spiegel − neuer Spiegel.
   - Das Gelände liegt dabei nie tiefer als das Querprofil. Das Ufer am Netzrand bleibt so geschützt (15b/15c).
   - Gilt im 2-m-Stempel und im 1-m-Feinschliff. Unter Fällen (große Eintiefung) bleibt die Schlucht, an Hängen ohne
     Eintiefung wird nichts mehr abgegraben.
2. **Lagen über das ganze Delta (`schreibe_lagen_1m`).**
   - Die Lagen werden auf 1 m geschrieben.
   - Jede Zelle mit |Δ| > 0,3 m, die keine Zone abdeckt, bekommt die erste Lage der Zone `ufer_nah` des Bioms
     (Gewicht 200). Bei C2 (Tundra) ist das „Geroell“.
   - Das Lagenfenster deckt das Deltafenster ab; Feldgrenzen spielen keine Rolle.
3. **Uferring** auf Spiegel + 0,2 m (vorher 0,15 m) als Reserve. Auch das Anheben selbst läuft außerhalb des Rings
   1:2 aus. Sonst hob ein sehr tiefes Altufer bis 1 m weit außerhalb des Rings an, etwa bei D3.
4. **„Bestand“** zählt, wenn das alte Ufer tiefer als Spiegel − 0,75 m liegt. Dann erreicht der Ring (höchstens 1 m)
   mit 0,15 m Rasterreserve die Höhe Spiegel + 0,1 m nicht. Ausgelöst hat das B_R_P0_P2_05: Dort liegt das alte
   Ufer 0,8 m unter dem Spiegel.
5. **Prüfer-Regeln (`pruefe_gelaende`):**
   - |Δ| > 0,3 m ist erlaubt bis halbe Breite + 0,4 m (Netzrand) + 1,5 m (Uferring) + (Eintiefung + 0,5 m) / tan 35°
     (Böschung) + 1 m Rasterreserve.
   - Die Eintiefung zählt dabei als Maximum über ±3 m, wegen der Fallkanten.
   - Dazu kommen die Zufluss-Endstücke (Breite/2 + 4 m). Klamm und Wandzonen stecken in der Breite.
   - Sonst FEHLER, mit Fläche, größtem Δ und Abstand.
   - Jede Zelle mit |Δ| > 0,3 m braucht in einer Lagendatei einen Wert > 0, sonst FEHLER.

## 3. Delta-Statistik C2

Gemessen wird der Abtrag (Summe −Δ, 1-m-Zellen) nach dem Abstand zur neuen Wasserlinie `spiegel_neu_cm`.

| Abstand | 15e lokal (1af3fb2) | Cloud vorher (15c) | **Cloud nachher (aaf330c)** |
|---|---|---|---|
| 0–10 m | 8 420 m³ | 6 600 m³ | **6 583 m³** |
| 10–20 m | 2 527 m³ | 4 243 m³ | **1 977 m³** |
| 20–30 m | 440 m³ | 2 237 m³ | **0** |
| 30–45 m | 3 529 m³ | 7 248 m³ | **0** |
| 45–80 m | 5 173 m³ | 5 670 m³ | **0** |
| **gesamt** | 20 124 m³ | 25 998 m³ | **8 560 m³** |
| davon > 30 m | 43 % | 50 % | **0 %** |
| Zellen Δ < −0,5 m und > 25 m vom Bach | 1 774 | 3 322 | **0** |
| max. Abtrag > 25 m vom Bach | 12,68 m | 12,43 m | **–** |

- Max. |Δ| gesamt: 7,4 m, im Bett und an den Fällen. Angehoben werden 76 m³ (Uferring).
- Bei C2 unverändert gegenüber 15c: Stufen, Spiegel, Wasserkörper (KN0 mit Rampe 0–10 m, R0 174–203 m), Effekte
  und Kameras.
- Bei C2 geändert: Gelände-Delta, Lagen (jetzt mit allen Δ-Zellen) und die Instanzen am Hang (folgen dem neuen
  Gelände).

## 4. Alle Läufe

Fehlstempel gab es im alten Stand bei vielen Läufen. Mit den neuen Regeln geprüft:

| Prüfung | Läufe mit FEHLER | Abschnitte mit Fehlstempel | Abschnitte mit Δ ohne Lage | Läufe ohne Abtrag > 25 m |
|---|---|---|---|---|
| alter Stand (15c), alle 161 auf 2 m | 40 | 41 | 36 | 80 von 98 |
| neuer Stand (aaf330c), alle 161 auf 2 m | **0** | **0** | **0** | 94 von 98 |

Die 4 Läufe, die noch Abtrag weiter als 25 m von der Mittellinie haben, sind breite Flüsse oder Fälle mit großer
Eintiefung. Dort liegt der Abtrag innerhalb des erlaubten Bereichs.

## 5. Aufruf

```
# lokal (1 m)
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis . --laeufe F_ERLENBACH_1V_C2
# Cloud-Test
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --daten2m recherche/vorlagen/daten/sehens \
    --hoehe1m-fenster recherche/vorlagen/daten/gefaelle/hoehe_1m_fenster --aus <scratchpad>/a15e/plan
```
