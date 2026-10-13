# 16h Nachtrag 5 – Plan C.2–C.4 eingebaut, Lagen unter dem Spiegel, BaseColor gemessen, B.6 (13.10.2026, 17:05)

Bezug: eure Antworten `antworten/16h-nachtrag3-teile-a-c1-t3-schaum.md` (b588a8d) §1.2, §2, §4.5, §5 und
`antworten/16h-nachtrag4-v18-muendung.md` (5fdba07) §1.2, §2.3, §3.2, §4.

**Kurz:** Alles aus eurer Liste ist eingebaut außer V19. Die BaseColor-Messung zeigt: Der Grund unter Wasser ist mit Y 0,067 schon
**dunkler als euer Ziel** (≤ 0,15). Der helle, milchige Eindruck in den Augenhöhe-Bildern kommt deshalb nicht mehr vom Boden.
**Frage (Abschnitt 4):** Soll V19 trotzdem kommen, oder ist jetzt die Wasseroberfläche der Hebel?

## 1. Antworten auf eure Rückfragen

**Nachtrag 3, Rückfrage 1 (Format):** Bach-Koordinaten (s, Seite, d) sind gut so. Wir rechnen lokal um; Weltkoordinaten sind nicht
nötig. So rechnen wir, damit ihr es nachbauen könnt:
- Mittellinie und Normale aus `lauf_p2.json` (1-m-Punkte) wie in den Querschnitten: Sehne über ±3 Punkte, links = (−t_j, t_i) im Raster.
- Wasserkante d_kante aus `querschnitte_p2.json` (dieselbe Datei wie eure, md5 gleich), linear zwischen den Querschnitten derselben Seite.
- Abstand von der Mitte = d_kante(s) + d; z = Gelände **jetzt** (nach C1 und Mündung) − Einbettung × Netzhöhe × Skala.
- Gier = Fließrichtung + `yaw_rel`. Gras: +Z um |kipp| zum Wasser geneigt. Flache Steine (Höhe < 0,35 × Länge): an der Geländenormalen,
  dazu die Dachziegel-Kippung stromauf. Rundliche Blöcke: halb angelehnt. Uferfelsen: aufrecht. Moos und Kiesel: an der Geländenormalen.
- **Euer `h_ueber_spiegel_m` beim Gras ist die Schulterhöhe**, die Mitte liegt aber 0,15–0,35 m vor der Schulter. Wir setzen den Fuß
  deshalb auf Schulterhöhe (begrenzt durch das Gelände jetzt). So hängt der Büschel über die Kante. Bitte bestätigen, dass das gemeint war.
- Prüfung der Umrechnung: Beim Moos liegt Gelände − Spiegel jetzt im Median 0,6 cm neben eurem `h_ueber_spiegel_m` (95 % unter 31 cm).

**Nachtrag 3, Rückfrage 2 (Dump 4.3):** Noch nicht nötig. Schaum bleibt aus; `ELD_Strom_Schaum` steht auf 0 (vorher 0,8).

**Nachtrag 3, Rückfrage 3 (Klänge):** Ferat hat die zehn Cues noch nicht angehört. Zwischenstand: die drei Flussklänge auf 30 %
(`C2_Ton_Fluss_01/05` 1,0 → 0,3, `_02` 0,91 → 0,27).

**Nachtrag 4, Rückfrage 1 (BaseColor):** Abschnitt 4.

**Nachtrag 4, Rückfrage 2 (Folgebreiten):** Ja. Die C3-Punkte 3–6 sind unverändert die Weltpunkte bei dist 44,5 / 59,4 / 74,2 / 89,0 m.
Breiten jetzt 17 / 22 / 26 / 25 m.

**Nachtrag 4, Rückfrage 3 (SRV-Liste):**
- Prüflauf über alle 70 Felder mit V18: **0 Teile über 64**. Umgestellt ist nur `_504_6_10_0` (D6, V18s).
- Nach den Lagen unter dem Spiegel meldet der Gras-Karten-Schritt für C2, C3 und D2 **0 neue SRV-Fehler**.
- Nebenbefund: 20 Landschaftsteile um C2 (B1–D3) waren seit dem V18-Umhängen ungespeichert. World Partition hält solche Teile
  geladen. Ihre Höhen stimmten mit den Weltdaten (6 000 Punkte, höchstens 1,2 cm); wir haben sie gezielt gespeichert.

## 2. Plan C.2–C.4 eingebaut

**Teile (C.3/C.4):** 1 592 von 1 730 gesetzt (C2 1 539, C3 53), Thema `kantenufer_p2`.

| Grund | Anzahl | Regel |
|---|---|---|
| Pflanze im Wasser | 38 | Gelände < Spiegel − 2 cm |
| überdeckt von Felsen | 37 | Bodenpunkt in der gedrehten Hülle eines Bachdekor-Felsens/Stamms oder einer Felsschale (85 %) |
| überdeckt von Bachsteinen | 32 | nur Kopfsteine und Kiesel; Blöcke und Uferfelsen dürfen kleine Bachsteine überdecken |
| zu tief eingegraben | 20 | Oberseite der Mitte < 25 % der Höhe über dem Gelände (flache Steine an 40–57°-Ufern) |
| Lippe | 9 | Steine mit \|s − s_lippe\| ≤ 0,75 m und d ≤ 0,5 m (Hauptstrahl frei) |
| doppelt | 2 | zwei Steine des Plans überdecken sich |

- Eine erste Fassung mit eurer Lippenzone als Band (s_lippe − 1,5 … s_fuss + 1,0, d ≤ 2 m) deckte **84 % der Talkaskade** ab: 77
  Lippen auf 189 m, Stufen alle 5–7 m. Sie hätte 77 von 81 Kopfsteinen entfernt. Die Widerlager liefert das Bachdekor schon, darum prüfen
  wir jetzt die Überdeckung mit dessen Felsen.
- Steine sitzen ohne schwebende Ecke. Die Auflage nehmen wir mit 60 % der Hülle an, weil Felsen unten nicht kastenförmig sind; die
  Absenkung ist das Größere aus eurer Einbettung und „keine Ecke schwebt“.
- Gesetzt: 204 Grasbüschel/Embankments, 1 037 Moos, 306 Kiesel-Packs, 42 Kopfsteine, 1 Prallhang-Block, 2 Uferfelsen.
- **SWR-Hindernisse:** 35 Steine ≥ 0,4 m im Wasser oder ≤ 1 m daneben aus dem Plan. Mit Bachdekor zusammen gefiltert (keine Lippen-,
  Rand-, Bettfelsen; Teil ≤ 40 % der Bettbreite; je Meter ≤ 50 %): 1 753 → 1 362. Neubau des Hindernis-Akteurs, Reset und Bake folgen
  in Abschnitt 5.

**Lagen (C.2):** 408 Zielzellen (steil 354, Erdanriss oben 33, Prallhang-Fels 21) mit 1 m weichem Rand, zusammen 1 693 Zellen in C2.
- Den Uferstreifen unter 0,65 m über dem Spiegel lassen wir unverändert.
- Mittel der Zielzellen vorher: Moos 23 / Kies 16 / Fels 16 / Felsplatte 13 / Geröll 12 / Erde 10 %.
- Nachher: Moos 26 / Geröll 23 / Erde 22 / Trockengras 14 / Kies 8 / Lehm 3 %.

**Bilder** `bilder/swr_p2/kant_vorher_nachher_1.jpg` und `_2.jpg`:
- Vorher ist der Stand nach den Lagen unter Wasser, nachher kommen Lagen und Teile dazu; je 7 Standorte auf Augenhöhe.
- Am deutlichsten sind die überhängenden Grasbüschel an der Kante (s 545 und s 565). Moos und Kiesel sieht man aus 4–6 m kaum.

## 3. Lagen unter dem Spiegel, Altbett-Schutz, Mündungsfächer

- **Lagen unter dem Spiegel** (eure Mischung aus Nachtrag 2 §1.3) über `s38 lagen` in C2, C3 und D2 eingespielt; 0 neue SRV-Fehler.
  Bilder `bilder/swr_p2/v18_lagen_vorher_nachher.jpg`: grauer und steiniger an den Rändern, die Mitte bleibt bei Augenhöhe hell (Abschnitt 4).
- **Schutzabstand je Nachbar (§1.2):** Die C3-Bäche sind hier 8–10 m breit, die neue Regel ergibt halbe Breite + 12 m. Das ist fast
  dasselbe wie bisher (3 559 statt 3 604 geschützte Zellen im alten Band, nur **34 Zellen** neu gerechnet). Das Kiesfeld bleibt daher
  größtenteils.
- **Mündungsfächer:** 40 m um p2-s 748. Die 523 Zellen, die Teil A dort schon umgefärbt hatte, haben wir auf den Stand davor (Schotter)
  zurückgesetzt.
- **Eigener Fehler, behoben:** Der Neu-Lauf von Teil A hat den Gras-Faktor ein zweites Mal auf die schon ausgedünnten Dichten angewendet.
  Die Heide stand dadurch bei etwa 0,67 × eurem Wert. Das ist korrigiert, die Dichten sind wieder wie nach Teil A. Das Werkzeug
  rechnet die Dichten jetzt immer vom Stand vor dem ersten Lauf aus.

## 4. `Ufer_Staerke` Bach 0 und BaseColor (eure Rückfrage 1)

`Ufer_Staerke_Bach` 0,25 → **0** (beide Instanzen). Messung: orthografische Szenenaufnahme senkrecht von oben, Quelle **BaseColor**
(GBuffer, linear).
- Ausschnitt 48 × 48 m um p2-s 500, 384² Pixel (12,5 cm). Wasser, SWR und Wasserzonen ausgeblendet.
- Ausrichtung über die Szenentiefe gegen die Weltdaten geprüft: Median 0,9 cm.

| Klasse (je Pixel, ≤ 8 m von der Mitte) | Pixel | Y Median (10 % / 90 %) | RGB Median | euer Ziel |
|---|---|---|---|---|
| unter Wasser (Gelände < Spiegel − 5 cm) | 14 961 | **0,067** (0,042 / 0,117) | 0,078 / 0,065 / 0,051 | ≤ 0,15 |
| nasses Band (−5 … +15 cm) | 2 166 | **0,063** (0,036 / 0,106) | 0,074 / 0,061 / 0,048 | ≤ 0,25 |
| trockener Kies (> 0,65 m, Kies + Geröll ≥ 50 %) | 1 069 | **0,129** (0,069 / 0,213) | 0,162 / 0,122 / 0,074 | 0,30–0,40 |

Bild `bilder/swr_p2/basecolor_t500.png` (BaseColor mit Gamma 2,2, blau schraffiert = unter Wasser).

**Befund:**
- Unter Wasser und im nassen Band liegt der Grund schon **weit unter dem Ziel**. Er ist noch etwas warm (R > G > B).
- Der trockene Kies am Hang ist mit 0,13 eher **zu dunkel** für euer Ziel 0,30–0,40 und warm-orange.
- In den Augenhöhe-Bildern wirkt der Bach trotzdem hell und milchig, mit Wirbelmustern. Das sind nach unserer Deutung Spiegelungen des
  Himmels an der Wasseroberfläche bei flachem Blick (Fresnel), verzerrt von den Sim-Normalen (`Sim Velocity Normal Strength` 15,
  Rauheit 0,04).

**Fragen:**
1. **V19:** Mit V19 sänke der Grund unter Wasser auf etwa 0,04–0,05. Wollt ihr V19 trotzdem? Das Skript liegt fertig (50 Knoten,
   0 neue Texturen; Schalter `V19_Staerke`), es ist noch nicht gebaut.
2. **Wasseroberfläche:** Welche Werte am WCBS-Material (`MI_EL_SWR_Klar`: Rauheit, Normalstärke, Specular, Streuung) nehmen den milchigen
   Glanz bei Augenhöhe, ohne das Wasser stumpf zu machen? Wir testen gern 3–4 Varianten an t430/t500/t550.
3. **Trockener Kies 0,13 statt 0,30–0,40:** Liegt das an der Tal-Tönung (Stärke 0,5, R 66–79 / G 43–47 / B 30–34)? Oder ist euer Zielwert
   für dieses Tal zu hoch? Die Hänge sollen golden bleiben (eure Nachtrag-4-Aussage zum Licht).

## 5. Mündungskante und B.6

**B.6 (§5.1):** 14 alte Flussfelsen nach eurer Regel:
- 9 entfernt: alle größer als 1,5 m und keiner am Prallhang. `_014` lag im Bett.
- 5 flache `SM_NordicBeachRocks_01` (1,44 m) behalten; drei davon um 7–11 cm auf ≥ 40 % eingegraben.
- Keiner liegt ≤ 1 m am Wasser, also kein neues Hindernis. Ein Prallhang-Uferfels war nicht dabei, die 2 geplanten Uferfelsen bleiben.

**Mündungskante (Nachtrag 4 §3.2):**
- C3-Punkt 0 von dist 24 auf **20 m**, 8,7 m unter das p2-Wasser, das bis dist 28,7 m auf der C3-Achse läuft.
- Höhe 36,80 m, Breite 6 m (= p2-Breite dort); Punkt 1 auf 36,78 m.
- `Overlap Material Priority` p2 12 / C3 10.

**Neu gebacken** (Hindernis-Akteur neu mit 1 362 Teilen, Reset, 5 min, Bake WCBS):
- Bett zu 99,9 % nass, Front 788/788 m.
- Tiefe Mitte 0,54 m (Plan 0,59); Talkaskade 0,47 m (Plan 0,69), Kiesbett 0,53 m (Plan 0,53).
- Neben dem Bett 1–8 m nass: 1 722 Zellen (vorher 1 703).

**Bilder:**
- `bilder/swr_p2/muendung_kante_vorher_nachher.jpg`: Von oben ist die C3-Anfangskante weicher, aber noch zu ahnen (Bildmitte rechts).
  Die zwei großen alten Flussfelsen an der Mündung sind weg. Auf Augenhöhe ist der Kies grauer und wirkt nasser.
- `bilder/swr_p2/kant_vorher_jetzt.jpg`: KANT0 gegen den jetzigen Stand (Uferplan, `Ufer_Staerke_Bach` 0, Gras-Korrektur, neu gebacken).

## 6. Was wir als Nächstes machen (bis eure Antwort da ist)

- V19 bleibt fertig, aber ungebaut (Frage 4.1).
- Für Frage 4.2 machen wir A/B-Bilder der Wasseroberfläche an t430/t500/t550: Rauheit und Normalstärke, ohne zu speichern.
  Die Werte meldet der nächste Nachtrag.
