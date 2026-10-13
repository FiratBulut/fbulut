# Antwort zu 16h Nachtrag 2 – TL, T0, Kasten-Statistik, Mündung

Stand 13.10.2026. Grundlage: `auftraege/16h-nachtrag2-tl-t0-kasten.md` (e833e0d), Bilder `bilder/swr_p2/tl_landschaft_bachwerte.jpg`,
`t0_zerlegung.jpg`, `kasten_statistik_p2.png`, Ferats Daten `antworten/fluss_sim/p2_lokal/querschnitte_p2.json` und
`kasten_statistik_p2.json`, unsere Antworten [`16h-erlenbach-p2-talkaskade-ufer-wasser.md`](16h-erlenbach-p2-talkaskade-ufer-wasser.md)
und [`16h-nachtrag-materialtest.md`](16h-nachtrag-materialtest.md), dazu die 16g-Antwort
[`16g-nachtrag2-feinwerte-und-rueckfragen.md`](16g-nachtrag2-feinwerte-und-rueckfragen.md) (fluss_sim v11, Mündung §8).

**Kennzeichnung:** [Befund] Ferats Messung, [Projekt] eigene Daten und Rechnung, [Ableitung] geschlossen, [Gestaltung]
Gestaltungsentscheidung, [unsicher] im Test klären.

---

## Kurzfazit

1. **Korrekturen unserer Annahmen.**
   - Die Bach-Werte im Landschaftsmaterial (TL) machen das Bett nicht grau. Der Hebel ist die **Houdini-Tal-Tönung** (bis
     Faktor 1,05 / 0,86 / 0,77), dazu die selbst orangen Kies- und Geröll-Texturen.
   - **Unsere Aussage zur Streuung war falsch.** „Scattering A wirkt je cm, A 0,1 ist milchig“ stimmt nicht: Bei 0,5 m ist
     A 0,1 nicht sichtbar milchig (T0 c), und schon das Glas ist goldbraun (T0 a).
   - Das Wasser färbt nichts. **Variante F bleibt.**
2. **Frage TL 1: ja, Tönung am Wasser neutral, und zwar im Material.**
   - Unter Wasser bei allen Gewässern, im Uferband nur bei Bächen: voll bis 0,3 m über dem Spiegel, auslaufend bis 0,8 m.
   - Gewicht W = max(1 − SmoothStep(−0,05; 0,05; h), Bachgewicht × (1 − SmoothStep(0,3; 0,8; h))).
   - Dann gilt `ToenungStaerke` × (1 − W). Das sind fünf Knoten; die Spiegel-Textur gibt es schon.
   - Die Houdini-Daten bleiben unverändert, die Tal-Tönung ist für die trockenen Hänge gewollt.
3. **Frage TL 2: Texturen nur aus dem Inventar.** Kachelbar und passend sind nur zwei Surfaces:
   - `T_MossyRockyGround_01` für Geröll im Bach;
   - `T_IcelandicQuarryRock_01` für Fels unter Wasser.
   - Eine **graue, kachelbare Bachkiesel-Textur fehlt**: Vorschlag ist eine kostenlose Megascans-Suche.
   - Bis dahin unter Wasser und im nassen Band 35 % entsättigen. Die Lagen unter dem Spiegel neu: Geroell 30, Kies 15, Fels 20,
     Felsplatte 10, Schlamm 12, Algen 13.
4. **Kasten (Frage C): Die Statistik zählt die Talhänge mit.** Nur im Uferbereich (≤ 4 m ab der Kante) gezählt:
   - Bergrinne 33 statt 93, Durchbruch **0** statt 34, Talkaskade 16 statt 32.
   - **Durchbruch: nichts zu tun.** Seine Kästen sind natürliche Talhänge 4–9,5 m vom Wasser.
   - **Talkaskade: zurücklegen ja**, an 15 Querschnitten (s 446–550, nicht nur 500–575), **56 m³**.
     - Unser Rezept mit hartem 4-m-Korridor hätte am Korridorrand neue Stufen gebaut. Neu ist ein zweistufiges Profil
       (32° bis 1,5 m, darüber 38°), das am Gelände endet (höchstens 6 m).
     - Danach bleiben 0 Kästen, nur s 534 links (2,7 m) wird Uferfels.
   - **Bergrinne:** Ferats Lagen-Prüfung annehmen.
     - Zurücklegen nur, wo Fels + Felsplatte vor dem Graben unter 50 % liegt, in Strecken ab 3 Querschnitten (6 m) je Seite,
       und nur, wo die Linie das Gelände innerhalb von 6 m trifft.
     - 26 der 33 Ufer-Kästen sind ohnehin höhere Felswände. Die Bergrinne „sieht gut aus“ (Ferat), deshalb dort im Zweifel nichts
       abtragen.
5. **Teil A:** Die Box-Füllung statt des Medians ist richtig; der Median holte den Schotter der C3-Ufer herein. Die Kappe Kies
   ≤ 5 % / Geröll ≤ 10 % passt zu unseren Richtwerten, gilt aber nur in der Altbett-Maske. Die Rest-Schotterflecken dürfen örtlich
   darüber liegen.
6. **Mündung: Ich weiche begründet von 16g ab**, dort vorgeschlagen war p2 um 0,9 m anzuheben.
   - Die 37,78 / 37,42 / 37,00 m am Kopf von `F_ERLENBACH_2_C3` sind **Kopien des Endes des ersetzten `F_ERLENBACH_2_C2`**
     (dort s 174–204 mit genau diesen Höhen), also die alte Feld-Überlappung und kein Flussspiegel.
   - Es entsteht weder Rückstau noch Stufe. **Es gilt der p2-Spiegel:** `F_ERLENBACH` soll erst dort beginnen, wo sein Spiegel
     ≤ 36,86 m ist (2-m-Daten s ≈ 34 m), wie die bestehende Feldgrenzen-Regel „Anschluss bei passendem Spiegel“.
   - In `ersetzt.json` steht der Anschluss als Datensatz (`muendung_anschluss`, wird noch nicht gelesen).
   - Die Umsetzung im Export gehört zu 16g (v12); ich habe am fluss_sim-Code nichts geändert.
   - `F_ERLENBACH` erst nach dieser Kürzung backen.
7. **Nächste Schritte:**
   - die 14 übrigen Flussfelsen nach Nachtrag-1-Antwort §5 (≤ 1,5 m im Band 0–12 m halb eingraben, sonst weg);
   - die Klänge nach §6 (Stufen 15–20 m Reichweite bei −12 dB, Fälle ≥ 1 m 30–40 m).
8. **Neu im Repo** (alle Prüfungen 0 FEHLER):
   - `bachbett_ufer_regeln.json`: Abschnitte `toenung_16h2`, `entsaettigung_nass`, `texturen_inventar` und `zuruecklegen_16h2`;
     Lagen unter dem Spiegel neu.
   - `skripte/ufer_regeln/ufer_regeln.py`: `kasten_nah`, `boeschung_zweistufig`, `strecken_auswahl`,
     `toenung_neutral_gewicht`; Selbsttest 0 FEHLER.
   - `skripte/ufer_regeln/zuruecklegen_p2.py` mit Ergebnis `ufer_p2/zuruecklegen_p2.json` (deterministisch).

---

## 1. TL – Tal-Tönung

### 1.1 Einordnung

| Größe | Wert [Befund] | Faktor nach `ToenungStaerke` 0,5 |
|---|---|---|
| Tal (Talkaskade, Kiesbett), auch 40–80 m vom alten Fluss | R 66–79, G 43–47, B 30–34 (64 = neutral) → (1,1; 0,72; 0,53) | **(1,05; 0,86; 0,77)** |
| Bergrinne | (43; 49; 36) | kühler, dunkler |
| Weltmittel | (61; 59; 54) | fast neutral |

- Grau kann das Bett so nicht werden: Ein grauer Stein (0,30; 0,30; 0,29) wird zu (0,32; 0,26; 0,22), also ocker. Nässe dunkelt
  ab, ändert aber den Farbton nicht.
- Deshalb wirkte TL bei t500 sogar oranger: Ohne die helle Kies-Ersetzung kommen die Lagen-Texturen (selbst orange) mit der
  Tönung durch.
- Das korrigiert unsere Nachtrag-1-Antwort: `Ufer_Staerke` und `Ufer_Farbe` allein reichen nicht. Die Entscheidung „Lagen
  zeigen, nicht übermalen“ bleibt, braucht aber 1.2 und 1.3.

### 1.2 Frage 1 – Tönung unter dem Spiegel und im Uferband auf neutral: **ja**

**Im Material, nicht in den Houdini-Daten** [Ableitung]:
- Die Tönung ist ein Talmaß (Dutzende Meter). Das Wasserband ist 1–3 m breit und ändert sich mit jedem Bett (p2 lokal,
  Planer-Läufe).
  - Im Material folgt es automatisch der vorhandenen Spiegel-Textur, wirkt bei allen Gewässern und ist mit einem Regler
    umkehrbar.
  - In den Houdini-Daten müsste man die Tönungslagen bei jeder Wasseränderung neu schreiben und die Kette neu bauen.
- Die Hänge bleiben golden. Das ist für die trockene Bergtundra gewollt und passt zum Witcher-Herbstlicht.

| Teil | Regel |
|---|---|
| h | Gelände − Spiegel (m), aus `T_Eldarien_Wasserspiegel_2m` wie bei der Nässe |
| unter Wasser | W_unter = 1 − SmoothStep(−0,05; 0,05; h), **alle Gewässer**: Unter Wasser ist eine Erdtönung nie richtig |
| Uferband | W_ufer = **Bachgewicht** × (1 − SmoothStep(0,3; 0,8; h)): voll bis 0,3 m, Auslauf bis 0,8 m; passt zum Uferstreifen (−0,1…0,65 m, Auslauf 1,0 m) und zum Nässeband 50 cm |
| Gewicht | W = max(W_unter, W_ufer) × `Toenung_Wasser_Neutral` (neu, 1,0) |
| Anwendung | `ToenungStaerke`_eff = `ToenungStaerke` × (1 − W) im bestehenden Lerp |

**Knotenskizze** (5 Knoten + 1 Parameter):
1. `h` (vorhanden aus dem Nässe-Zweig) →
2. `SmoothStep(-0.05, 0.05, h)` → `OneMinus` = W_unter
3. `SmoothStep(0.3, 0.8, h)` → `OneMinus` → `Multiply(Bachgewicht)` = W_ufer
4. `Max(W_unter, W_ufer)` → `Multiply(Toenung_Wasser_Neutral)` = W
5. `ToenungStaerke × OneMinus(W)` → in den vorhandenen Tönungs-Lerp

Ohne Bachgewicht-Kanal funktioniert Schritt 2 sofort für alle Gewässer; das Uferband kommt dazu, sobald der Kanal existiert.
Referenz: `ufer_regeln.toenung_neutral_gewicht`.

**Option, nicht nötig fürs Bachbett** [Gestaltung]: Die Tönung auf Gesteinslagen (Kies, Geroell, Fels, Felsplatte) weltweit halbieren
(`ToenungStaerke` × (1 − 0,5 × Gesteinsanteil)). Steine nehmen die Bodenfarbe in der Natur schwächer an als Erde und Gras.
Das ist eine Entscheidung für Ferat.

### 1.3 Frage 2 – Texturen für den nassen Bachgrund (nur Inventar)

**Quelle:** `vorlagen/daten/inventar.json` → `fab_texturen` (839 Pfade).
- `export/unreal/welt/inventar/` liegt nicht im Repo.
- Für `Environment_Set` und `Mountain_Environment_Set` nennt das Inventar nur Anzahlen, keine Texturnamen. Dort kann es graue
  Varianten geben, die ich nicht sehe → Rückfrage 2.
- Die **Farben** der Texturen habe ich nicht gesehen [unsicher]: bitte im Editor prüfen.

| Zweck | Textur (Inventar) | Art | Eignung |
|---|---|---|---|
| Geröll im Bach | `/Game/Megascans/Surfaces/MossyRockyGround/T_MossyRockyGround_01_BC` (+ `_N`, `_AoRDp`) | Surface, kachelbar | **erste Wahl** für Geroell unter Wasser und im nassen Band (moosig-dunkel) |
| Fels unter Wasser | `/Game/Megascans/Surfaces/IcelandicQuarryRock/T_IcelandicQuarryRock_01_BC` (+ `_AoRDp`) | Surface, kachelbar | **erste Wahl** für Fels/Felsplatte im Bett (isländischer Bruchstein, grau) |
| Bachbett-Flecken | `/Game/Megascans/3D_Assets/DryRiverBed/T_DryRiverBed_01_BC`, `NordicBeachRockyGround/T_NordicBeachRockyGround_01_BC` / `_02_BC`, `TundraRockyGround/T_TundraRockyGround_01_BC`, `NordicBeachRocks/T_NordicBeachRocks_01_BC` | Texturen von 3D-Scans | **nicht kachelbar**: als Landschaftslage nur nach Nahttest. Besser die zugehörigen Netze als Bettflecken setzen (`SM_TundraRockyGround_01` ist schon in der Tundra-Palette) |
| Kies (grau, gerundet) | – | **fehlt** | Megascans-Suche (kostenlos über Fab): „river pebbles“, „riverbed gravel“, „wet pebbles“, „mossy river stones“; grau-blau, gerundet, 2 × 2 m. Ich nenne bewusst keine Asset-Namen, die ich nicht prüfen kann |

**Bis die Textur da ist** [Ableitung]:
- Unter Wasser und im nassen Band entsättigen: Farbe = Lerp(Farbe; Luminanz; **0,35**), danach `Nass_Abdunkeln` 0,40.
  - Das nimmt den Orangestich der Kies- und Geröll-Texturen (`T_ground_big_pebbles_01`, `T_ground_stones_01`) zurück, ohne
    sie zu tauschen.
- **Lagen unter dem Spiegel** neu, weg von den zwei orangen Texturen:

  | Lage | Nachtrag 1 | **neu** | Bedingung |
  |---|---|---|---|
  | Geroell | 40 | **30** | überall (mit `MossyRockyGround` dann wieder 40) |
  | Kies | 25 | **15** | nur vorn an Schnellen (Ruhe < 0,6) |
  | Fels | 10 | **20** | Lippen, Stufen, Rinnen (mit `IcelandicQuarryRock`) |
  | Felsplatte | 5 | **10** | Becken-Grund der Talkaskade (Stufen-Becken auf Fels) |
  | Schlamm | 10 | **12** | ruhige Becken ≥ 0,25 m |
  | Algen | 10 | **13** | ruhige Becken ≥ 0,4 m |

  Die Farbe der Fels- und Felsplatten-Texturen kenne ich nicht. Sind sie auch ocker, gilt die Entsättigung für alle Lagen
  unter Wasser.

## 2. T0 – Korrektur zur Streuung

| Unsere Aussage (Hauptantwort B.2, Rang 1) | Befund T0 | Korrektur |
|---|---|---|
| „Wirkt Scattering RGB × A je cm, ist A 0,1 = 2–3 je m; bei 0,5 m zwei Drittel Streulicht, milchig“ | c) A 0,1 bei 0,5 m: **nicht milchig**; a) schon Glas goldbraun | **Falsch.** A ist nicht „je cm“, oder es wirkt mit einem kleinen inneren Faktor. Die Einheit bleibt unbekannt [unsicher], ist für Bäche aber unwichtig |
| „DF-Schaum macht die Steinflecken“ (Rang 2) | e) ELD-Schaum an/aus: gleich | **Falsch.** Die Flecken sind Steine, verzerrt durch die Normalen |
| „Absorption ist nicht der Hebel“ | b) gleich | bestätigt |

- Schon die Hauptantwort war nach dem ersten Nachtrag umgestellt (Landschaftsmaterial als Hauptursache, Wasserwerte
  zweitrangig). T0 schließt die Wasserseite jetzt ab: **Gold = Grund-Texturen × Tal-Tönung × warmes Licht.**
- **Variante F bleibt.** Refraction 1,0 nimmt etwas Verzerrung. Für die Bäche reichen 1,05–1,08 (Hauptantwort B.3); die Farbe
  ändert sich nicht.
- Die V1–V3-Tabelle der Hauptantwort gilt nur noch für tiefe Becken ≥ 1 m. Die Streustärke darin ist ein Bildwert, kein
  physikalischer.

## 3. Kasten-Statistik und Zurücklegen (Frage C)

### 3.1 Nachgerechnet

Ferats Zahlen lassen sich mit `kasten_hoehe` über das ganze Profil (bis 9,5 m) genau nachrechnen: 93 / 34 / 32 Kästen,
113 / 23 / 76 m³ [Projekt]. Das Profil reicht aber weit über das Ufer hinaus. **Steile Talhänge 4–9,5 m vom Wasser zählen dort
als Kasten**, obwohl sie natürlich und nicht gegraben sind.

| Abschnitt | Querschnitte | Kästen, ganzes Profil (Ferat) | **Kästen ≤ 4 m ab der Kante** | Folgerung |
|---|---|---|---|---|
| Bergrinne | 200 | 93 | **33** (26 davon Wände, die eine 32/38°-Linie in 6 m nicht erreicht) | Felsrinne; nur nach Lagen-Prüfung |
| Durchbruch | 190 | 34 (s 199–270) | **0** | **nichts zu tun**: alles natürliche Talhänge |
| Talkaskade | 190 | 32 (s 446–566) | **16** (s 446–550) | zurücklegen |
| Kiesbett, Mündung | 208 | 0 | 0 | – |

**Talkaskade im Detail:** Von Ferats 32 sind 16 natürliche Hänge weiter draußen (s 480 und 488–494 links, 542–546 und 552–566 rechts). Echte
Ufer-Kästen liegen bei s 446, 452, 454, 482, 512, 526–540 und 548–550, also auch oberhalb von s 500.

### 3.2 Unser Rezept korrigiert: zweistufig bis zum Gelände

- **Fehler im Rezept:** Der alte `boeschung_zuruecklegen` (32°, harter 4-m-Korridor) erzeugt an Ufern über 2,5 m eine neue Stufe
  am Korridorrand. Bei 6 der 16 Talkaskaden-Querschnitte blieben 0,7–2,2 m Kasten.
- **Neu (`boeschung_zweistufig`):** 32° bis 1,5 m über der Kante, darüber 38°, bis die Linie das Gelände trifft; höchstens 6 m;
  nur abtragen.
  - Trifft die Linie das Gelände nicht, wird statt Abtrag ein **Uferfels** gesetzt (Hauptantwort C.4).
  - 38° liegt genau an der Schichtband-Schwelle, also kein Band.
  - Oben ist es eine Erd- bzw. Rasenböschung (Klasse „Böschung steil“).

| Variante (Talkaskade, 16 Ufer-Kästen) | gelöst | Rest-Kasten | Abtrag |
|---|---|---|---|
| alt: 32°, 4-m-Korridor | 10 | 6 | 69 m³ |
| 32°, 6-m-Korridor | 15 | 1 (dazu 4 ohne Schnitt mit dem Gelände) | 82 m³ |
| **32° / 38° ab 1,5 m, 6 m (gewählt)** | **15** | **0** (s 534 links → Uferfels) | **56 m³** |

Ergebnis je Querschnitt: [`ufer_p2/zuruecklegen_p2.json`](ufer_p2/zuruecklegen_p2.json) (s, Seite, Kasten nah/voll, Schnittpunkt,
Abtrag, Rest). Aufruf: `python -I recherche/antworten/skripte/ufer_regeln/zuruecklegen_p2.py [--fels DATEI]`. Zwei Läufe
byte-gleich.

### 3.3 Bergrinne und Durchbruch: Regel mit Lagen-Prüfung

**Ferats Angebot annehmen:** je Querschnitt und Seite der Anteil Fels + Felsplatte **vor dem Graben** (0…1), als JSON
`[{s, seite, fels_anteil}]` → `zuruecklegen_p2.py --fels`.

| Regel (`zuruecklegen_16h2` in `bachbett_ufer_regeln.json`) | Wert |
|---|---|
| Kasten zählt nur im Uferbereich | d ≤ 4 m, > 0,6 m über 45° |
| Zurücklegen, wenn | Fels + Felsplatte < **50 %** und die Linie das Gelände in ≤ 6 m trifft |
| zusammenhängend (Bergrinne, Durchbruch) | ≥ **3 Querschnitte (6 m)** je Seite, eine Lücke von einem Querschnitt wird überbrückt |
| Talkaskade, Kiesbett (Lockermaterial) | jeder Kasten-Querschnitt; der Abtrag läuft je 2 m stromauf und stromab aus |
| ohne Lagen-Prüfung | Bergrinne und Durchbruch gelten als Fels: nichts abtragen |
| Linie trifft das Gelände nicht | Uferfels statt Abtrag |

**Erwartung Bergrinne:** Nur 7 der 33 Ufer-Kästen sind überhaupt zurücklegbar (zusammen etwa 12 m³), der Rest sind höhere Wände.
Ferat bewertet die Bergrinne als „sieht gut aus“. Ich rechne dort mit wenig bis nichts und würde nur Stellen mit Fels < 50 % in
Strecken ≥ 6 m anfassen.

## 4. Teil A – Box-Füllung und Kappe

- **Box-Füllung statt Median: bestätigt** [Ableitung].
  - Unser Median „30–60 m, ±15 m Höhe, Neigungsklasse“ holt im Kiesbett die Schotterufer der C3-Bäche herein (60 % Kies).
  - Natürliche Zellen ≥ 30 m von jedem Wasser sind die richtige „Umgebung“.
  - In `bachbett_ufer_regeln.json` (A_altbett, Band „umgebung“) ist der Median nur noch Richtwert; Ferats Weg gilt.
- **Kappe Kies ≤ 5 %, Geröll ≤ 10 %: passt.**
  - Sie entspricht unseren Richtwerten (Kies 5) und der Grenze des Rest-Schotters.
  - Sie gilt nur innerhalb der Altbett-Maske. Echte Schotterufer anderer Gewässer bleiben, wie sie sind.
  - Die Rest-Schotterflecken (Rauschen 6 m, ≤ 10 % der Fläche) dürfen örtlich bis Kies 15 / Geröll 10 gehen.
- Prüfung „0 Kies-Bänder > 8 × 20 m außerhalb 0–6 m“: wie gefordert.
- Die Tal-Tönung (1.2) betrifft auch Teil A. Die Bilder erst nach dem Tönungs-Knoten beurteilen, sonst wirkt alles ocker.

## 5. Mündung bei s ≈ 748

### 5.1 Befund

- p2 erreicht `F_ERLENBACH_2_C3` bei s ≈ 748 (Abstand = halbe Breite 18 m); ab s 760 liegt p2 in der C3-Mitte [Befund].
- C3-Spiegel 37,78 m, p2 bei s 740 36,86 m [Befund].
- Die Kopfpunkte von `F_ERLENBACH_2_C3` in den 2-m-Daten (`wasser_welt.json`) [Projekt]:

  | s (m) | 0 | 14,8 | 29,7 | 44,5 | 59,4 |
  |---|---|---|---|---|---|
  | Spiegel (m) | **37,78** | **37,42** | **37,00** | 36,55 | 36,13 |

- Das Ende des **ersetzten** `F_ERLENBACH_2_C2` bei s 174,3 / 189,2 / 204,0 hat genau **37,78 / 37,42 / 37,00 m**. Der Kopf von
  C3 ist also die alte Feld-Überlappung der beiden Houdini-Flüsse. Die Feldgrenzen-Regel (16c Nachtrag 3) hat dort den Anschluss
  „bei passendem Spiegel“ gesetzt. Seit 2_C2 ersetzt ist, ist dieser Kopf ein Rest ohne eigenes Wasser.

### 5.2 Rückstau oder Stufe? Welcher Spiegel gilt?

- **In der Natur** ist der Spiegel an einer Mündung stetig. Liegt der Hauptfluss höher, staut er den Nebenbach zurück
  (flacher Auslauf); eine Stufe nach oben gibt es nicht [Fach].
- Hier ist aber **p2 der Oberlauf** dieses Wassers. Das Gewässer `F_ERLENBACH` beginnt jetzt am C3-Lauf (`anfang.ersetzter_oberlauf`).
  Der 0,9 m höhere Kopf stammt vom ersetzten Fluss.
- **Also gilt der p2-Spiegel:** Es gibt weder Rückstau noch Stufe. `F_ERLENBACH` beginnt dort, wo sein Spiegel ≤ p2-Spiegel an der
  Mündung ist. In den 2-m-Daten ist das s ≈ **34 m** (36,86 m, interpoliert zwischen 37,00 und 36,55 m), bzw. an der
  Projektion der p2-Mündung, wenn diese weiter stromab liegt.

### 5.3 Abweichung von 16g §8 (begründet)

- 16g schlägt vor, p2 von s ≈ 700 bis 748 um 0,9 m anzuheben, alternativ den Flussspiegel lokal neu zu setzen.
- **Ich empfehle die Alternative, konkret als Kürzung des C3-Kopfs.**
  1. Die 37,78 m sind ein Überlappungsrest, kein echter Flussspiegel (5.1).
  2. Das Anheben ändert Ferats fertiges p2-Bett: 0,9 m auf 50 m würden einen künstlichen Stau-Teich ins Kiesbett legen. Das
     Kürzen nimmt nur einen Rest weg.
  3. Die Kürzung ist dieselbe Regel, die der Export schon an Feldgrenzen anwendet („Anschluss erst bei passendem Spiegel“).
- **Vorbehalt:** Liegt das Gelände unter dem C3-Kopf (s 0–34) lokal höher als 36,56 m (Spiegel − 0,3 m), fällt der Kopf beim
  Senken trocken. Er wird dann ohnehin nicht gebraucht und kann entfallen. Nur wenn **lokal im 1-m-Gelände** der C3-Fluss an
  der Mündung wirklich bei 37,8 m steht (eigener Pegel, nicht der Rest), gilt 16g: p2 anheben bzw. flacher Auslauf.

### 5.4 Folgen für SWR, Backen und `ersetzt.json`

- **`ersetzt.json`:** Datensatz `ersatz.ERLENBACH_P2.muendung_anschluss` mit Ziel-Lauf, p2-s, p2-Spiegel, den Kopfhöhen, der
  Regel und den lokalen Prüfpunkten. **Wird vom Export noch nicht gelesen.** Die vier ersetzten Läufe sind unverändert, der
  Export liest daraus weiter nur `laeufe`.
- **fluss_sim-Code: nicht geändert** (16g baut v11/v12).
  - Vorschlag für 16g: in `gewaesser_bilden` bzw. beim Zusammenfügen den Kopf eines Teils mit `anfang.ersetzter_oberlauf`
    bis zum ersten Punkt mit Spiegel ≤ `muendung_anschluss.p2_spiegel_m` + 0,02 m kürzen (wie `feldgrenzen` → `grenze_s_m`).
  - Prüfer: Anfangsspiegel ≤ p2-Spiegel + 0,02 m, sonst FEHLER.
- **Backen:** `F_ERLENBACH` (v11-Fingerabdruck `d48d07dd22ff…`) **erst nach der Kürzung backen**. Der Kopf ändert Spline, Rechteck
  und damit den Fingerabdruck.
  - Lokal bis dahin: im Level die ersten 2–3 Splinepunkte des C3-Water-Body auf ≤ 36,86 m fallend setzen bzw. die SWR erst an der
    Mündung beginnen lassen.
  - Ferats p2-Spline endet bei s ≈ 748 (wie 16g).

## 6. Nächste Schritte: 14 Flussfelsen und Klänge

- **Flussfelsen** (Nachtrag-1-Antwort §5):
  - je Block: Abstand zum p2-Bett und Größe messen;
  - ≤ 1,5 m im Band 0–12 m: 40–60 % eingraben, Moos oben, ≤ 1 m am Wasser als SWR-Hindernis;
  - größer: nur als Uferfels am Prallhang (der Uferfels bei s 534 links ist ein guter Platz für einen großen Block statt
    eines neuen);
  - sonst entfernen; außerhalb 12 m höchstens 1 Findling je 50 m;
  - danach Reset + Bake (zusammen mit dem Zurücklegen).
- **Klänge** (§6): `C2_Ton_Fluss_01/02/05` entfernen.
  - Je Stufe ≥ 0,5 m eine Bachquelle (Reichweite 15–20 m, −12 dB gegen den Flussklang).
  - Fälle ≥ 1 m 30–40 m (innen 3–5 m), −6 bis −8 dB.
  - Ruhige Strecken alle 25–40 m mit 10–15 m bei −16 bis −18 dB.
  - Höchstens 4 gleichzeitig hörbar. Zuerst die Talkaskade.

## 7. Was lokal zu tun ist

Regeln und Skripte: Commit **`aceac7f`** holen.

1. **Tönungs-Knoten** (1.2) ins Landschaftsmaterial, zuerst nur W_unter, dann mit Bachgewicht. Bilder an `C2_t430_auge`, `C2_t500_auge`,
   `C2_t500_schraeg`, `C2_t550_auge`.
2. **Entsättigung** 0,35 unter Wasser und im nassen Band. Lagen unter dem Spiegel nach 1.3; `T_MossyRockyGround_01` und
   `T_IcelandicQuarryRock_01` testen; Megascans-Suche nach grauen Bachkieseln.
3. **Talkaskade zurücklegen** nach `ufer_p2/zuruecklegen_p2.json` (15 Querschnitte, 56 m³, zweistufig); s 534 links Uferfels.
   Bergrinne erst mit `--fels`-Daten. Danach Reset + Bake der p2-SWR.
4. **Mündung:** Gelände unter dem C3-Kopf prüfen, Projektion der p2-Mündung auf `F_ERLENBACH_2_C3` messen, C3-Kopf lokal senken
   bzw. kürzen (5.3). `F_ERLENBACH` nicht vor der Kürzung backen.
5. Flussfelsen und Klänge nach 6.

## Quellen

- Ferats Nachtrag 2 mit Bildern und Daten (siehe Kopf); `vorlagen/daten/inventar.json` (`fab_texturen`);
  `vorlagen/daten/sehens/wasser_welt.json` (Kopfpunkte C2/C3).
- Unsere Antworten 16h, 16h-Nachtrag, 16g Nachtrag 2 (§8 Mündung, v11), 16c Nachtrag 3 (Feldgrenzen „passender Spiegel“).
- Montgomery & Buffington 1997 und Schüttwinkel wie in der Hauptantwort; Mündungsspiegel stetig (Rückstau): allgemeine
  Gerinnehydraulik [Fach].

## Rückfragen

1. **Lagen-Prüfung Bergrinne:** bitte `[{s, seite, fels_anteil}]` je Querschnitt (Fels + Felsplatte vor dem Graben) liefern.
2. **Texturnamen:** Welche Boden-Texturen haben `Environment_Set` und `Mountain_Environment_Set` außer `T_ground_big_pebbles_01`
   und `T_ground_stones_01`? Gibt es graue Varianten? Und welche Texturen nutzen die Lagen Fels und Felsplatte?
3. **Mündung:** Wie hoch steht das 1-m-Gelände unter dem C3-Kopf (s 0–34), und wo projiziert sich die p2-Mündung auf
   `F_ERLENBACH_2_C3`? Steht der C3-Water-Body im Level wirklich bei 37,78 m?
4. **Gestein-Option:** Soll die Tal-Tönung auf Gesteinslagen weltweit halbiert werden (1.2, Option)?
