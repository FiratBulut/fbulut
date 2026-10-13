# Antwort 16h Nachtrag 6b – Wasser neben dem Bett, Beckenform, Abstürze

Stand 13.10.2026. Bezug: `auftraege/16h-nachtrag6b-wasser-neben-dem-bett.md`, der neue Bettplan
[`16h-nachtrag6c-becken-kuenstlich.md`](16h-nachtrag6c-becken-kuenstlich.md) (`p2_bett/bettplan_p2.json`), Antwort 14 (Nature Water FX)
und 16h N5 (N5-Filter für Hindernisse).

## Kurzfazit

- **(a) Wasser neben dem Bett:** Die Hauptlösung ist die **Uferstufe** im neuen Bettplan.
  - Der Spiegel liegt an jeder Lippe 0,25–0,45 m unter der Narbe, an der Schulter überall mindestens 0,22 m.
  - Geometrisch liegt das 2-m-Band dann nur zu **0,1 %** unter dem Spiegel; heute sind es 94 %. Grundlage ist das angenommene Ist im alten Bett.
  - Das SWR-Band bleibt **Bett + 2 m**, die Nachfüllrate bleibt. Das Band ist dann trockenes Land über dem Spiegel.
  - Die anderen Wege sind nur Rückfall (Tabelle unten).
  - **Prüfkriterium für den nächsten Bake:** ≤ 5 % nass im Band 0,25–2 m hinter der neuen Bettkante; dazu Front 788/788 m.
- **(b) Beckenform:** Ferats Korrektur stimmt, der Kolk liegt unter dem Absturz. Im neuen Plan liegt er unter der Hauptkerbe, ist länglich, 0,8–1,2 m tief und läuft flach zur nächsten Lippe aus. Mehr in 6c §3 und §8.
- **(c) Abstürze:** Vorschlag nach Fallhöhe, Ferat entscheidet.
  - < 0,7 m: Rampe, nur SWR.
  - 0,7–1,0 m: SWR über die Lippe.
  - ≥ 1 m freier Fall: zusätzlich `NS_Impact_Small` am Fuß.
  - ≥ 1,8 m: zusätzlich `NS_Waterfall_Small` an der Lippe.
  - Ein Vorhang kommt erst später und nur an Stufen ≥ 2 m, falls die SWR dort sichtbar abreißt.
  - Im Plan sind das 24 Impact- und 3 Waterfall-Systeme. Sie stehen nur als Vorschlag in `bettplan_p2.json` → `effekte_vorschlag`.

## (a) Wie das Wasser im Bett bleibt

**Ursache [Ferat]:**
- Das Band ist Bett + 2 m, und die Ufer liegen bündig: 0,5 m neben dem Bett im Median nur 0,16 m über dem Spiegel.
- Bei Nachfüllrate 0,3 füllt die Simulation alles, was unter dem Spiegel liegt.

**Hauptlösung (6c):**
- Uferstufe 0,2–0,5 m an Lippen und Ausläufen, Schulter 1 m breit auf mindestens Spiegel + Uferstufe (höchstens 0,29 m Anhebung über die alte Narbe). Am Beckenkopf liegt das Ufer höher, weil das Becken eingeschnitten ist.
- Damit liegt das ganze Band über dem Spiegel. Das Band selbst kann bleiben: Breiter ist kein Nachteil, und die Front kommt durch (F2).

| Option | Bewertung |
|---|---|
| Ufer an den Stufen höher bzw. Bett an den Lippen tiefer | **ja, steckt im Plan:** Uferstufe, Schulter, Eckblöcke an jedem Lippenende; Kronen 4–10 cm unter Wasser, Rinne in der Kerbe 0,2–0,4 m |
| `remove_outside` (F1: Überlauf −38 %, Bett 15 % flacher) | nur Rückfall, wenn nach dem Bake > 5 % nass bleibt. Ein flacheres Bett widerspricht den 0,8–1,2-m-Becken |
| Band nur an den Stufen breiter | nicht nötig. Mit Uferstufe ist die Bandbreite für die Nässe gleich, ein schmales Band bringt das Risiko des Front-Stopps zurück (F2) |
| Hindernis-Wände am Ufer | nein: wirkt künstlich, staut, und der N5-Filter schließt Randhindernisse aus |
| feineres Raster | erst prüfen, wenn die Uferstufe im Bake nicht hält. Die Stufe ist 0,25–0,9 m breit, also 1–3 Zellen bei ~0,3 m. Halbe Zelle heißt etwa 4-mal so viele Zellen |

**Prüfkriterium nach dem nächsten Bake (Talkaskade):**
- `p2_bett_welt.py` schreibt `pruefband/<Feld>.u8` mit 1 = neues Bett und 2 = Band 0,25–2 m hinter der neuen Bettkante.
  - Die ersten 0,25 m der Uferstufe liegen gewollt unter Wasser: Dort ist die Wasserlinie.
- Ziel 1: Zellen mit Wert 2, die nass sind, ≤ **5 %**. „Nass“ wie bei eurer 94,1-%-Messung.
- Ziel 2: Front 788/788 m, Bett (Wert 1) ≥ 99 % nass.
- Ziel 3: Kolke der Hauptbecken in der Simulation im Median ≥ 0,8 m tief (Plan 1,03 m).
- Danach die Wasserspiegel- und Bachgewicht-Texturen der Landschaft für den neuen Spiegel neu erzeugen (`T_Eldarien_Wasserspiegel_2m`, `T_Eldarien_Bachgewicht_2m`).
- **Grasbüschel im Bach (Punkt 4):** Im Korridor fallen die alten Kantenufer-Teile weg (6c §5, Schritt 2). In der Bettzone bekommen die Lagen keine Graslage; die Zonen stehen in `talkaskade_zonen.u8`.

## (b) Beckenform

- Ferats eigene Korrektur in 6c ist richtig: Der Kolk liegt schon heute unter dem Absturz. Die Aussage „verkehrt herum“ aus 6b ist damit überholt.
- Der neue Plan legt den Kolk unter die Hauptkerbe der oberen Lippe:
  - Der tiefste Punkt liegt 30 % der Kolklänge stromab.
  - Der Kolk ist 1,9–7,6 m lang, 1,3- bis 4-mal so lang wie breit und 0,84–1,20 m tief.
  - Zur nächsten Lippe läuft er flach aus und mündet in eine Rinne in deren Kerbe.
- Details in [6c](16h-nachtrag6c-becken-kuenstlich.md) §3 und §8.

## (c) Abstürze: welche Lösung ab welcher Fallhöhe

**Fallhöhen im neuen Plan [Plan]:** 46 Lippen.

| Fall | Lippen |
|---|---|
| < 0,7 m | 4 |
| 0,7–1,0 m | 9 |
| ≥ 1,0 m | 33 |
| davon ≥ 1,8 m | 4 |
| davon ≥ 2 m | 2 (2,01 und 2,49 m) |

| Fallhöhe (frei) | Lösung | im Plan |
|---|---|---|
| < 0,7 m | Rampe bzw. Schnelle, nur SWR | 4 |
| 0,7–1,0 m | SWR über die Lippe; Schaum über ELD/Material, keine Niagara | 9 |
| ≥ 1,0 m | SWR + `/Game/NatureWaterFX/FX/NS_Impact_Small` am Fuß unter der Hauptkerbe, **je Einheit nur an der höchsten Stufe** | 24 |
| ≥ 1,8 m | zusätzlich `/Game/NatureWaterFX/FX/NS_Waterfall_Small` an der Lippe | 3 |
| ≥ 2 m, nur wenn die SWR dort sichtbar abreißt | später ein Vorhang wie in Antwort 14 | 0, vorgemerkt sind 2 Lippen |

- **Grenzen wie in Antwort 14:** Cull 30–45 m, höchstens 6 aktive Systeme je Standort. Wer weniger will, nimmt Impact nur an jeder zweiten Einheit (12).
- **Belegt:** Die Systemnamen stehen in `vorlagen/daten/inventar_extra.json`.
- **Ungeprüft** (Antwort 14 §9): die User-Parameter, die Größe der Systeme bei Skala 1 und ihre Fließachse.
- **Lage der Vorschläge:** s, u und z stehen in `bettplan_p2.json` → `effekte_vorschlag`. Nichts davon ist gesetzt, bis Ferat entscheidet.
