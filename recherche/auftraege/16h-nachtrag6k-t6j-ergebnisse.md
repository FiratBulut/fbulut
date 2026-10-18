# 16h Nachtrag 6k – Ergebnisse T6j-A/B/C, T-b1, T-c1, B5-Vereinigung; Frage Simulationsboden

Stand 18.10.2026, 12:00 PC-Uhr. Bezug: Antworten 6i (§1.2) und 6j (§1.1, §4). Alle Editor-Tests liefen nur im Speicher, nichts wurde gespeichert.
Stand auf Platte unverändert: ganze SWR, Zelle 36,7 cm, Nachfüllen 0,3, Band = Bett + 2 m, BAKED_SIM.

## 1. T6j-A (ohne Editor)

- Euer Skript liefert mit den Repo-Dateien genau eure Ausgabe: H1 Spline 13,7 / 13,6 / 13,4 / 12,8 %, H2 Plan+0,20 5,5 / 5,2 / 3,8 / 1,9 %,
  Lippenschatten 16,6 % des Bands.
- Maske im Welt-1-m-Raster wie das Prüfband: Bett 722, Band 554 (Maske 2) + 111 (Maske 3) Zellen.
- Formale Entscheidung nach eurer Tabelle: **uneindeutig** (T01: K1 56,3 %, K2 −14,0 cm, K3 6,9 %).
- **Neu:** Die Editor-Spline trägt nicht eure 237 Stufenpunkte, sondern 1-m-Proben aus `spline_z.json` + 5 cm.
  - Gegen die Stufenpunkte liegt sie im Median 5,0 cm höher, p90 10,7 cm, höchstens 53 cm.
  - Mit einer Lippenschatten-Maske nach der Editor-Spline (Schwelle 5 cm) wäre der Lippenschatten 37,6 % des Bands.
  - Mit dieser Maske erfüllt T01 K1 (77,0 %) und K2 (+3,1 cm), K3 knapp nicht.
- Kolke: An 15 von 24 Hauptbecken liegt der Simulationsboden über 10 cm über dem Gelände, bis 84 cm. Vermutlich sind das die Beckenblöcke als
  Hindernisse. Im Bild ungeprüft.

## 2. T-b1 (6i §1.2, Latten im Becken)

Latte 2 (Becken 45): Boden 44,050 m, Spline 45,030 m, gebacken 45,190 m.

| Darstellung | abgelesener Spiegel |
|---|---|
| BAKED_SIM | ≈ 45,16 m (≈ Simulation) |
| WCBS | ≈ 45,03 m (= Spline) |
| WCBS, Fluid Displacement Multiplier 2 bzw. 0 | unverändert ≈ 45,03 m |
| `UseBakedSim` True | Wasser nicht mehr sichtbar |

**Ergebnis:** H1 bestätigt, H2 und H3 widerlegt. Der Bach bleibt auf BAKED_SIM.

## 3. T-c1 (Header UE 5.8, lokal)

`RenderState` ist `UPROPERTY(EditAnywhere)` ohne Blueprint-Zugriff. Nur `SetPaused` ist BlueprintCallable, `Rebuild()` gibt es nur im Editor,
`UpdateRenderState()` ist öffentliches C++. Ein Umschalten im Spiel geht also nur mit eigenem C++. Wir lassen BAKED_SIM fest gespeichert.

## 4. T6j-B (Nachfüllen)

- Basis frisch mit 0,3: stabil, Bett 100 %, Front 788 m. Band „Tiefe“ > 1/2/5/10 cm = 83,2 / 78,8 / 65,4 / 45,7 % (Dump 14.10.: 83,3 / 78,8 /
  65,0 / 45,9 %).
- **B0:** 30 s nach `match_spline_height_amount` 0,3 → 0 ist das Bett 0 % nass, die Front steht bei 72 m. Das Umschalten setzt die Simulation zurück.
  B1 entfällt deshalb.
- **B2** (Lauf ab Reset mit 0,4 gegen 0,3, je stabil), > 10 cm:

  | Messgröße | Maske 3 (Lippenschatten) | Maske 2 (übriges Band) |
  |---|---|---|
  | Tiefe | +12,6 pp | +5,1 pp |
  | sichtbar | +7,2 pp | +2,0 pp |

  Formal „zwischen“ (Maske 3 steigt um mindestens 3 pp, aber Maske 2 bleibt nicht gleich). Sichtbar gemessen wirkt das Nachfüllen vor allem im Lippenschatten.

**„sichtbar“** heißt: Simulationstiefe G > 0,1 cm und Simulationsoberfläche − echtes Gelände (`hoehe.f32`) > x cm. Grund: siehe §6.

## 5. T6j-C (Band nur s 389–580 = Bett + 0,5 m, ganze SWR)

- Stabil, Bett 100 %, Front 788 m. Die Front blieb also nicht stehen.
- **Formal: keine Wirkung, H1 falsch.** Tiefe in Maske 3 > 10 cm fällt nur um 6,2 % relativ (−3,6 pp). Gefordert waren mindestens 50 %.
- Sichtbar gemessen, > 1/2/5/10 cm:

  | Bereich | T6j-C sichtbar | Basis 0,3 sichtbar | T6j-C Tiefe |
  |---|---|---|---|
  | Band gesamt | 15,0 / 14,3 / 12,6 / 9,9 % | 15,9 / 15,3 / 14,0 / 11,0 % | 81,2 / 74,7 / 61,5 / 43,3 % |
  | Band 0,25–1 m | 28,9 / **27,9** / 25,4 / 20,0 % | 30,7 / **30,0** / 27,1 / 22,5 % | 95,7 / 90,0 / 79,6 / 63,9 % |
  | Band 1–2 m | 4,9 / **4,4** / 3,4 / 2,6 % | 5,2 / **4,7** / 4,4 / 2,6 % | 70,6 / 63,6 / 48,3 / 28,3 % |
  | Maske 3 | 55,0 / 53,2 / 45,9 / 39,6 % | 57,7 / 55,9 / 51,4 / 42,3 % | 96,4 / 87,4 / 75,7 / 55,0 % |

- Euer Ziel aus 6g §3 für 37-cm-Zellen (> 2 cm: 0,25–1 m ≤ 30 %, 1–2 m ≤ 5 %) ist sichtbar gemessen schon in der Basis fast erreicht
  (30,0 / 4,7 %). T6j-C bringt nur 2 bis 3 pp mehr. Wir übernehmen T6j-C deshalb nicht.

## 6. Frage: Simulationsboden 63–65 cm unter dem Gelände

- Im Band liegt der Simulationsboden aus dem Dump im Median **64,7 cm unter `hoehe.f32`** (T6j-C; in den anderen Läufen 63–65 cm).
  Im Bett passt er. In den Kolken liegt er dagegen bis 84 cm darüber (§1).
- Folge: Die Messgröße „Tiefe“ (Simulationsspiegel − Simulationsboden) ist im Band fast überall > 10 cm, obwohl dort sichtbar kein Wasser
  über dem Gelände steht. Darauf beruhten das 78,8-%-Band, das 5-%-Ziel des Prüfbands und die formalen Entscheidungen in T6j-A/B/C.
- Einstellungen der SWR: `use_capture` True, `smoothing_width` 5, `smoothing_cutoff` 500, `resolution_max_axis` 2016, `source_size` 300,
  `remove_outside_spline_amount` 0. Wasserzone C2: `render_target_resolution` 4096 (0,29 m/Pixel).
- So lesen wir den Boden: Der gebackene Dump ist RGBA16F. R ist die Wasseroberfläche relativ zur Akteurhöhe, G die Tiefe. Simulationsboden =
  R + Akteurhöhe − G. Die 16-Bit-Rundung von R macht bei |R| 20–40 m nur 2 cm aus, erklärt also keine 65 cm.

**Fragen:**
1. Woher kommt der tiefe Boden im Band? Unsere Vermutungen: Glättung des Bodens (`smoothing_width`/`smoothing_cutoff`), der Capture-Bereich
   endet an der Spline-Breite und dahinter steht ein Ersatzwert, oder der Dump gibt den Boden relativ zu einer anderen Bezugshöhe aus.
2. Ist „sichtbar“ die richtige Messgröße für alle weiteren Bandziele? Wenn ja: Gilt das Ziel aus 6g §3 damit als erreicht, und ist der nächste
   Hebel der Kantenbewuchs (6j „Was fehlt“ Punkt 2)?
3. Soll das Prüfband-Ziel (≤ 5 % nass) auf „sichtbar“ umgestellt werden? Welcher Wert gilt dann?
4. Nachfüllen: bei 0,3 bleiben (0,4 macht den Lippenschatten sichtbar nasser)?
5. Kolke bis 84 cm zu flach: Beckenblöcke als Hindernisse herausnehmen oder kleiner machen? Wie prüfen wir das ohne Bild?

## 7. B5-Ost: Deckung als Vereinigung (6j §4)

Raster 0,5 m, Fußabdruck am Pivot zentriert, Neigung ignoriert, Stand Zensus 18.10. 08:28. Fußflächen-Summe Fels im Fenster 109,1 %.

| Zone | Fläche ha | Fels vereinigt | alle Netze vereinigt | Prüfer 21 §(a) |
|---|---|---|---|---|
| Halde | 2,04 | 69,5 % | 85,5 % | 79 % |
| Schrofen | 8,38 | 61,6 % | 72,9 % | 61 % |
| Wand | 4,15 | 95,0 % | 95,1 % | 83 % |
| Fuß | 2,64 | 26,3 % | 64,8 % | – |
| Hangwald | 2,69 | 21,1 % | 57,0 % | – |
| Sperre | 4,18 | 23,3 % | 54,7 % | – |

Halde, Schrofen und Wand zusammen: Fels vereinigt 72,2 %. Die Halde liegt 9,5 pp unter dem Prüferwert. **Frage:** Reicht das, oder soll die
Halde nachverdichtet werden (Regel, Stückzahl)?

## Was wir als Nächstes tun

- Platzierungsprüfung weltweit läuft lokal (Pilot D5 heute). Wasser bleibt unverändert, bis eure Antwort zu §6 da ist.
