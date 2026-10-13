# Antwort 16h Nachtrag 6c – Becken wirken künstlich: neuer natürlicher Bettplan für die p2-Talkaskade

Stand 13.10.2026. Bezug: `auftraege/16h-nachtrag6c-becken-kuenstlich.md` (Vorrang), Bild `bilder/swr_p2/talkaskade_treppe_von_oben.jpg`,
Ferats Querschnitte `fluss_sim/p2_lokal/querschnitte_p2.json`, unsere Regeln aus 15f/15g (`skripte/gefaelle/gefaelle_regeln.json`),
Antwort 18 und 16h Nachtrag 5 (N5-Filter für SWR-Hindernisse). Frage 4 aus Nachtrag 6 §8 (Step-Pool-Regeln) beantwortet §8 hier.

**Kennzeichnung:** [Ferat] = eure Messung bzw. Angabe; [Plan] = in diesem Plan gerechnet; [Fach] = Literatur (Kürzel wie in
`gefaelle_regeln.json` → `quellen`); [Annahme] = unser Gestaltungswert; [angenommen] = Ist-Gelände im alten Bett, das wir nicht kennen.

## Kurzfazit

- **Neuer Plan fertig:** 25 Einheiten statt der gleichförmigen Treppe. Jede Einheit besteht aus einer Stufe oder Blockkaskade, einem länglichen Becken und einem Auslauf bis zur nächsten Lippe.
  - **Abstände:** 1,1–3,8 Bachbreiten, im Median 1,9 B ≈ 7 m. Sie richten sich nach dem Gefälle.
  - **Ruhige Strecken:** drei, bei s 406–419, 455–466 und 500–510. Ihre Hauptbecken sind 10,6 m, 7,8 m und 6,0 m lang.
  - **Lippen:** 46, alle schräg (Median 22°), gekrümmt und gekerbt, aus Blöcken. Die Abstände streuen von 1,8 bis 11 m (CV 0,54), die Fallhöhen von 0,5 bis 2,5 m (CV 0,33).
  - **Talweg:** Er pendelt. Die Hauptkerbe wechselt an 76 % der Lippen die Seite.
- **Becken richtig herum und länglich:** Der Kolk liegt direkt unter der Hauptkerbe der oberen Lippe (Ferats Korrektur).
  - Kolktiefe 0,84–1,20 m, Median 1,03 m.
  - Der Kolk ist 1,9–7,6 m lang und 1,3- bis 4-mal so lang wie breit.
  - Er ist steil zur Stufe hin und läuft flach zur nächsten Lippe aus. In der Hauptkerbe liegt eine Rinne von 0,2–0,4 m.
- **Uferstufe:** Der Spiegel liegt an jeder Lippe 0,25–0,45 m unter der Narbe, an der Schulter überall mindestens 0,22 m darunter.
  - Geometrisch liegt das 2-m-Band neben dem Bett nur zu 0,1 % unter dem Spiegel (heute 94 % nass). Grundlage ist das angenommene Ist; die echte Messung bringt erst der Bake, Kriterium in 6b.
- **Die Grenze bei 30 % Talgefälle (wichtig):** Ein waagrechtes Becken von L Metern liegt am Kopf um etwa 0,3·L + Uferstufe unter der Narbe. Lange, ruhige Becken bedeuten deshalb einen Einschnitt.
  - Im Plan sind das am Beckenkopf 1,2–2,6 m (Median 1,6 m), mit auf 35° zurückgelegter Böschung statt Kasten.
  - Geschätzter Abtrag ~1 470 m³, Auftrag ~100 m³.
  - Wer flachere Ufer will, nimmt kürzere Einheiten. Die Stellschraube ist `kopf_ufer_max_m` je Klasse in den Regeln (§2).
- **Ausgabe:**
  - Bach-Koordinaten (wie `ufer_plan_p2`) plus Gelände-Soll-Raster.
  - Ein lokales Werkzeug rechnet beides über `lauf_p2.json` in das A15-Format um (Delta je Feld mit `fenster_ij`, Instanzen je Feld, Spline-Z je Meter).
  - Die Bilder zum Ansehen vor dem Graben liegen unter `p2_bett/`.
- **Prüfungen:**
  - Planer: 0 FEHLER und 3 WARNUNGEN (drei Hauptbecken 2,8–3,3 m statt ≥ 0,8 B). Zwei Läufe sind byte-gleich.
  - Weltwerkzeug, Selbsttest mit künstlicher Spline: Rückrechnung p95 3 cm, zwei Läufe byte-gleich.
  - Die Mündung bleibt bei 36,80 m. Am fluss_sim-Export ändert sich nichts (§6).

## 1. Warum die Becken künstlich wirken [Ferat]

- **Abstände:** 26 Stufen auf 189 m, alle 3–4 m eine, alle Becken gleich groß und rund (3–4 m lang, ~4 m breit).
- **Form:** Alle sind mit derselben Brush-Form „Kasten-U“ gegraben (Falloff 1,5, Rampe 1,5).
- **Ufer:** Sie liegen bündig. 0,5 m neben der Planbreite liegt das Gelände im Median nur 0,16 m über dem Spiegel.

Natürlich wirkt dagegen [Fach: MB1997, CHIN1999, ABR1995, CW2005; 15f/15g]:
- Abstände, Fallhöhen und Beckenlängen streuen.
- Die Lippen sind Blockreihen mit Lücken, schräg und gekrümmt.
- Der Hauptstrahl liegt seitlich, und der Kolk liegt darunter.
- Der Talweg wechselt die Seite.
- Die Becken sind breiter als die Lippen, die Ränder haben Buchten und Eckblöcke.

## 2. Die geometrische Grenze und wie der Plan damit umgeht

**Gefälle:** Die Talkaskade fällt von 100,65 m (s 390) auf 44,98 m (s 578), also 55,7 m auf 188 m. Das sind **29,6 %** [Ferat, Querschnitte].

**Was die Literatur dazu sagt [Fach]:**
- Bei diesem Gefälle liegen Bäche im Bereich *Cascade/Step-Pool*.
- MB1997 nennt Beckenabstände unter 1 B (Cascade) bzw. 1–4 B (Step-Pool), CHIN1999 0,43–2,4 B.
- Längere ruhige Becken gibt es in so steilen Bächen nur hinter einem höheren Riegel.

**Folge für den Spiegel:**
- Jedes waagrechte Becken liegt am Kopf um Fall + Uferstufe unter der Narbe.
- Die Uferstufe von 0,2–0,5 m (Antwort 18) lässt sich deshalb nur an den Lippen und im Auslauf einhalten.
- Am Beckenkopf entsteht ein Einschnitt. Der Plan legt dort die Böschung auf höchstens 35° zurück (Regel aus 16h N2: 32°/38°).
- Es wird nur so tief abgetragen, wie der neue Spiegel unter dem alten liegt, plus 0,3 m. Nach außen läuft der Abtrag bis 6 m auf 0 aus; die Talflanke bleibt stehen.

**Wie der Plan den Kompromiss löst:**
- **Einheiten-Klassen:**

  | Klasse | Anteil | Länge | Ufer am Kopf höchstens | größter Einzelfall |
  |---|---|---|---|---|
  | kurz | 38 % | 1,0–1,3 B | 2,0 m | 1,8 m |
  | mittel | 32 % | 1,5–2,2 B | 2,4 m | 1,8 m |
  | lang | 20 % | 2,4–3,0 B | 2,9 m | 2,2 m |
  | ruhig | 10 % | 3,0–4,0 B | 3,4 m | 2,6 m |

  - Die Länge wird mit (0,30 / örtliches Gefälle)^0,5 skaliert: steiler heißt kürzer.
  - Höchstens zwei gleiche Klassen folgen aufeinander. Zwischen ruhigen Strecken liegen mindestens 35 m.
- **Fall einer Einheit:** Der Beckenspiegel ist die Narbe an der unteren Lippe minus die Uferstufe U (0,25–0,45 m, je Einheit zufällig).
- **Blockkaskade:**
  - Liegt der Fall über dem größten Einzelfall der Klasse, wird die Stufe eine Blockkaskade aus 2–3 Teilstufen (0,35–1,6 m, Streuung ±75 %).
  - Die Teilbecken sind kurz (0,3–0,5 B). Nur so behält das Hauptbecken Länge, denn eine Kaskade mit Teilbecken von 1 B wäre wieder eine Treppe im Talgefälle.
  - Teilstufen bis 0,7 m werden zu 30 % eine Rampe (15f).
- **Ergebnis:** Der Einschnitt am Beckenkopf ist 1,2–2,6 m tief (Median 1,6 m).
- **Flachere Variante:** Kleinere `kopf_ufer_max_m`, z. B. 1,4 / 1,7 / 2,0 / 2,4 m, geben kürzere Einheiten (mehr bei 1–1,5 B) und weniger Abtrag. Die ruhigen Strecken werden dann kürzer.

## 3. Der neue Plan im Einzelnen

Alle Zahlen stehen in `skripte/p2_bett/p2_bett_regeln.json`, Herkunft je Block.

1. **Spiegel:**
   - Je Becken waagrecht.
   - Kopf: s 389, die bestehende Durchbruch-Stufe 100,96 → 100,65 m bleibt unverändert.
   - Fuß: Die letzte Lippe bei s 579 fällt von 44,98 m auf das unveränderte Kiesbett (44,23 m).
   - Talwärts steigt der Spiegel nie (geprüft je Spalte).
2. **Lippen (15f):**
   - Schräg 15–30° (Teilstufen einer Kaskade gleichsinnig ±8°), Bogen mit Pfeil 0,05–0,15 B, Scheitel stromab.
   - 1 Hauptkerbe (0,2–0,35 B, 0,6–1,4 m breit, 0,2–0,4 m tief = Rinne). Ab B ≥ 4,4 m in 40 % der Fälle eine zweite, flachere Kerbe.
   - Krone neben der Kerbe 4–10 cm unter Wasser. Lippe auf 0,85 B eingeschnürt.
   - Der Versatz ist begrenzt: Lippenlinien schneiden sich nie, jedes Becken behält an jeder Stelle die halbe Nennlänge.
3. **Becken und Kolk:**
   - Becken 1,1–1,25 B breit.
   - Der Kolk ist eine Schüssel (Kern voll tief, weich bis zum Rand):
     - Länge 55–80 % des Beckens, Breite 0,5–0,7 B, Länge mindestens 1,3 × Breite.
     - Der tiefste Punkt liegt 30 % der Kolklänge unter der Lippe, also steil zur Stufe und flach zum Auslauf.
     - Tiefe 0,8–1,2 m, mit dem Fall zunehmend; Teilbecken der Kaskaden 0,55–0,8 m.
   - Querprofil: Rand 3–8 cm tief, Talweg 0,2–0,4 m. Der Talweg wandert vom Kolk zur Kerbe der nächsten Lippe, Krone 0,8 m davor.
4. **Breite und Ränder (15g):**
   - Der Lauf pendelt bis ±0,45 m (Wellenlänge 16–28 m).
   - Buchten bis 0,8 m, an den Lippen 0,6 m frei.
5. **Ufer:**
   - Uferstufe: 0,25–0,4 m Lauf an der Prallseite (Kolkseite), 0,5–0,9 m an der Gleitseite, von Spiegel − Randtiefe auf Spiegel + U.
   - Dann 1 m Schulter auf mindestens Spiegel + U. Angehoben wird nur dort, wo die alte Narbe tiefer liegt, höchstens 0,29 m.
   - Dahinter höchstens 35° bis 6 m, Übergang 2 m.
6. **Blöcke:** alle Netze aus dem Inventar. Tundra-Palette aus `gefaelle_regeln.json` plus 9 Inventar-Felsen aus denselben Paketen (`zusatz_netze`, siehe §9).

   | Rolle | Anzahl | Regel |
   |---|---|---|
   | Lippenblöcke | 112 | entlang der Lippe, Abstand 0,75 × Größe, 0,5–1,2 m (mit dem Fall), 40–60 % eingegraben, Kerben frei |
   | Keystones | 87 | an beiden Rändern der Hauptkerbe (ab 0,6 m Fall), 0,8–1,5 m |
   | Eckblöcke | 58 | an den Lippenenden (85 %, Teilstufen 35 %), 0,9–1,8 m, 0,1–0,6 m außerhalb, 0,2–0,8 m stromab |
   | Randblöcke | 28 | Beckenrand alle 2,5–5 m (40 %) |
   | Beckenblöcke | 5 | 0,4–0,9 m, nicht im Strahl und nicht im Kolkkern |
   | Kies im Kolk | 331 | `SM_SmallStonesPack_*` als Fächer stromab |

   - **Kollision** haben nur Blöcke ≥ 0,8 m: 216.
   - **SWR-Hindernisse** nach dem N5-Filter: keine Lippen-, Eck- und Randblöcke, Teil ≤ 40 % der Bettbreite, je Meter ≤ 50 %. Das ergibt **5** (nur Beckenblöcke).
   - Lippenblöcke sind keine Hindernisse. Die Krone liegt im Gelände, die SWR sieht die Stufe über das Bett.
   - Flache Netze nur in der Lippe.

**Kennzahlen alt gegen neu**

| | alt (Ferat 6c) | neu (Plan) |
|---|---|---|
| Stufen / Lippen | 26 Stufen | 25 Einheiten, 46 Lippen (10 Einzelstufen, 34 Kaskaden-Teilstufen, 1 Rampe, 1 Endlippe) |
| Abstand | alle 3–4 m | Einheiten 4,2–13,3 m (1,1–3,8 B, CV 0,31); Lippen 1,8–11,1 m (Median 3,9 m, CV 0,54) |
| Fallhöhe | 0,68–3,74 m | Lippen 0,53–2,49 m (Median 1,19, CV 0,33); 2 Lippen ≥ 2 m |
| Becken | 3–4 m lang, ~4 m breit, rund | Hauptbecken 2,8–10,6 m (Median 4,5 m), Kolk 1,9–7,6 m lang, Länge/Breite 1,3–4,0 |
| Tiefe | Fuß 0,76–1,20, vor der Lippe 0,36–0,71 m | Kolk 0,84–1,20 m (Median 1,03), Rinne an der Kerbe 0,2–0,4 m, Krone daneben 4–10 cm |
| Lage des Kolks | mittig, rund | unter der Hauptkerbe, Seitenwechsel an 76 % der Lippen |
| Ufer 0,5 m neben dem Bett | im Median 0,16 m über dem Spiegel | Schulter mindestens 0,22 m, Median 0,72 m über dem Spiegel |
| Erdbau | – | Abtrag ~1 470 m³, Auftrag ~100 m³, Delta −3,2 … +1,7 m [angenommenes Ist im alten Bett] |

## 4. Bilder (zuerst ansehen, dann graben)

Alle Bilder sind abgewickelt (x = s, y = u, links oben). Die Ufer stammen aus euren Querschnitten. Das Bett im Ist ist **angenommen**: Kasten-U nach euren Kennzahlen, Tiefe von 1,0 m am Fuß auf 0,55 m an der Lippe.

| Datei | Was man sieht |
|---|---|
| [`p2_bett/talkaskade_delta.png`](p2_bett/talkaskade_delta.png) | Gelände neu − Ist (blau Abtrag, rot Auftrag); neue Bettkante, alte Planbreite, Lippen, Hauptkerben, Kolke, Blöcke |
| [`p2_bett/talkaskade_tiefe.png`](p2_bett/talkaskade_tiefe.png) | Wassertiefe neu: dunkle, längliche Kolke unter den Kerben, helle Ausläufe, versetzte Becken |
| [`p2_bett/talkaskade_laengsprofil.png`](p2_bett/talkaskade_laengsprofil.png) | Spiegel alt/neu, Talweg, Narbe, relativ zur Tal-Trendlinie (sonst sind 0,3-m-Stufen auf 56 m nicht lesbar); Klassen der Einheiten |
| [`p2_bett/talkaskade_querschnitte.png`](p2_bett/talkaskade_querschnitte.png) | 8 Querschnitte: Lippe, Kolk einer ruhigen Strecke, Ausläufe, Teilbecken, Hauptbecken |

## 5. Ausgabe und Einbau

**Im Repo** (`antworten/p2_bett/`, erzeugt von `skripte/p2_bett/p2_bettplan.py`):
- `bettplan_p2.json` enthält:
  - Einheiten, Lippen (Lage, Fall, Winkel, Bogen, Kerben), Becken (Kolk, Rinne, Uferstufe je Seite)
  - `spiegel_je_m`: s 389–580, Z der SWR-Spline auf der lauf_p2-Mittellinie
  - Instanzen in (s, u) mit Spalten wie `ufer_plan_p2`
  - `effekte_vorschlag` (nur Vorschlag, siehe 6b), Kennzahlen, Prüfung
- `talkaskade_soll.f32`: Gelände-Soll, 6 Kanäle auf 0,5 m × 0,25 m:
  - Kanäle: `z_min`, `z_max`, `gewicht`, `spiegel`, `abtrag_max`, `kante_abstand`.
  - Regel: neu = max(Ist + w·(clip(Ist, z_min, z_max) − Ist), Ist − abtrag_max).
  - Dadurch wird die Ist-Höhe erst lokal gebraucht.
- `talkaskade_zonen.u8`: Zonen (Bett, Kolk, Krone, Stufenwand, Uferstufe, Schulter, Böschung), für Lagen und Prüfungen.

**Lokal** (`skripte/p2_bett/p2_bett_welt.py`):
- Liest `lauf_p2.json` und `welt/hoehe.f32`. Die Normale bildet es wie eure Querschnitte: Sehne ±3 Punkte, links = (−t_j, t_i).
- Schreibt `<welt>/p2_bett/ERLENBACH_P2/` im A15-Aufbau:
  - `plan.json` mit `abschnitte[]` je Feld: `gelaende` {`datei`, `fenster_ij` [i0, j0, Höhe, Breite], `max_aenderung_m`}
  - `gelaende/*.f32`
  - `instanzen/<Feld>/plan.json` + `.f32` nach FORMAT.md §3 (Ebene `p2_bett`, `FT_EL_P2B_*`, `_kol` = mit Kollision; `swr_hindernis_anzahl`)
  - `spline_spiegel.json` [s, x_cm, y_cm, z_cm] je Meter
  - `pruefband/*.u8` (Bett / 2-m-Band für 6b)
  - optional `delta_welt.png`

**Reihenfolge lokal:**
1. Bilder ansehen. Passt die Form, Commit dieser Antwort ziehen.
2. Im Talkaskaden-Korridor (s 389–580, ±8 m) entfernen:
   - das alte Bachdekor
   - die Talkaskaden-Teile des Kantenufers (`ufer_plan_p2`, Stand 16h N5), weil sie sich auf die alte Wasserkante beziehen
   - die Teile des Hindernis-Akteurs im Korridor
3. `python -I recherche/antworten/skripte/p2_bett/p2_bett_welt.py --plan recherche/antworten/p2_bett --lauf <lauf_p2.json> --welt <export/unreal/welt> --bild`
4. Einbau über `a15_einbau.py` bzw. die s38-Kette mit `<welt>/p2_bett/ERLENBACH_P2/plan.json`. Danach Instanzen setzen.
5. Spline-Z im Bereich s 389–580 auf `spline_spiegel.json` legen. Außerhalb bleibt alles: eine SWR von der Quelle bis zur Mündung, Mündung 36,80 m.
6. Hindernis-Akteur ergänzen: nur die 5 Beckenblöcke aus `swr_hindernis_anzahl`. Dann Reset + Bake. Prüfen nach 6b §1.
7. Neue Querschnitte schicken, dann rechnen wir Kantenufer und Lagen für die neue Kante neu.

## 6. Mündung und fluss_sim

- Die Mündung bleibt bei **36,80 m**. Kiesbett und Mündung sind nicht verändert.
- Der Plan endet bei s 579 auf dem alten Kiesbett-Spiegel.
- Am fluss_sim-Export ist **nichts zu ändern**:
  - p2 ist kein Lauf des Exports; die von p2 ersetzten C2-Läufe stehen in `ersetzt.json` und werden übersprungen.
  - `F_ERLENBACH` beginnt erst an der Mündung, und der Mündungsanschluss bezieht sich nur auf 36,80 m.
  - Neue Fingerabdrücke gibt es deshalb nicht.

## 7. Durchbruch und Bergrinne

- **Bergrinne** (s 0–198): 40 % Gefälle, B ≈ 2,3 m, Felsrinne.
- **Durchbruch** (s 200–388): Er hat schon eine lange ruhige Strecke (s 220–300 auf 106,40 m).
- Beide hat Ferat früher als gut bezeichnet. Wir haben sie wegen des Vorrangs **nicht** neu geplant.
- Der Planer ist nach Abschnitten aufgebaut (`abschnitte` in den Regeln). Für eine Felsrinne kämen dazu:
  - `zuruecklegen: false`, weil Fels nicht zurückgelegt wird (Regel aus 16h N2)
  - Lippen aus Felsriegeln
  - die ruhige Strecke im Durchbruch als festes Becken

  Das geht in einem kleinen Nachtrag, wenn ihr es wollt (Rückfrage 3).

## 8. Step-Pool-Regeln (Frage 4 aus Nachtrag 6 §8)

1. **Abstand:** Einheiten 1–4 B. Wie oft welche Länge vorkommt, hängt vom Gefälle ab (steiler = kürzer); die Klassen streuen. Lange Becken nur hinter einer höheren Stufe oder Kaskade [MB1997, CHIN1999].
2. **Fall:** Der Spiegel folgt der Narbe minus Uferstufe. Stufe 0,5–1,8 m (ruhige Strecken bis 2,6 m), darüber eine Blockkaskade mit Teilbecken 0,3–0,5 B [ABR1995: (H/L)/S 1–2; RC2021: Stufenhöhe ≈ Blockgröße].
3. **Lippe:** schräg 15–30°, gekrümmt, 1–2 Kerben, Krone neben der Kerbe knapp unter Wasser; Blockreihe, Kerbe frei, Keystones am Kerbenrand, Eckblöcke an den Enden [15f].
4. **Kolk:** unter der Hauptkerbe, länglich (≥ 1,3 × Breite), steil zur Stufe, flach zum Auslauf; 0,8–1,2 m tief, Teilbecken 0,55–0,8 m [Antwort 18, 15f].
5. **Talweg:** Die Hauptkerbe wechselt an 75 % der Lippen die Seite, der Talweg wandert vom Kolk zur nächsten Kerbe.
6. **Breite:** an Lippen 0,85 B, in Becken 1,1–1,25 B, Buchten bis 0,8 m, Pendel ±0,45 m [15g].
7. **Ufer:** Uferstufe 0,2–0,5 m an den Lippen; Prallseite steil, Gleitseite flacher; Böschung höchstens 35°, Talflanke nicht abgraben [Antwort 18, 16h N2].
8. **Prüfung:**
   - CV der Lippenabstände ≥ 0,45, der Einheiten ≥ 0,3, der Fallhöhen ≥ 0,3; Seitenwechsel ≥ 55 %
   - Kolk 0,8–1,2 m, Rinne 0,2–0,4 m, Uferstufe ≥ 0,2 m
   - 2-m-Band ≤ 5 % unter dem Spiegel, Lippenlinien schneiden sich nicht
   - Netze im Inventar, kein Block im Hauptstrahl, N5-Filter, Kollision ab 0,8 m

## 9. Grenzen und Annahmen

- **Ist im alten Bett angenommen:** Es geht in Delta-Bild und Volumen ein. Lokal rechnet das Weltwerkzeug mit `hoehe.f32`; dort stimmen Delta und Volumen.
- **Narbe** = Gelände 1,5 m neben der alten Kante, Minimum beider Seiten, geglättet. Wo eure Brush-Rampe weiter reicht, liegt die Narbe zu tief; dann wird der Spiegel etwas tiefer als nötig.
- **Netze außerhalb der Tundra-Palette:** `SM_mountain_rock_big_01_1/_5`, `SM_ground_rock_02` (Mountain, wie die Palette), `SM_MossyForestBoulder_01/02/06/07`, `SM_LichenedForestBoulder_01`, `SM_MossyForestRock_02` (Megascans, bemoost wie `SM_TundraMossyBoulder_01`).
  - Grund: Unter 1,2 m hat die Palette nur einen klobigen Block.
  - Alle stehen in `netze.csv`, keiner ist gesperrt. Optik bitte prüfen.
- **Blöcke:** Die Neigung kommt im Weltwerkzeug nur als Kippen stromauf, ohne Anpassung an die Geländenormale. Die Blöcke sind 40–60 % eingegraben.
- **3 WARNUNGEN:** Drei Hauptbecken sind 2,8–3,3 m lang statt ≥ 0,8 B (≈ 3,4 m), weil dort die Uferhöhe die Einheit kürzt.

## 10. Prüfungen

| Lauf | Ergebnis |
|---|---|
| `p2_bettplan.py --selbsttest` | 0 FEHLER, 3 WARNUNGEN; zwei Läufe byte-gleich und gleich der Ausgabe (sha256 `bettplan_p2.json` 3a596467bdd9, `talkaskade_soll.f32` f274fd1b66d7, `talkaskade_zonen.u8` e9da20ba5dc6) |
| `p2_bett_welt.py --selbsttest` | künstliche gekrümmte Spline in C2, Gelände = angenommenes Ist: Weltdelta gegen Plandelta Median 0,0 cm, p95 3,1 cm; Abtrag 1 452 / Auftrag 91 m³ (Plan 1 469 / 100); zwei Läufe byte-gleich |

```
python -I recherche/antworten/skripte/p2_bett/p2_bettplan.py [--selbsttest] [--ohne-bilder]
python -I recherche/antworten/skripte/p2_bett/p2_bett_welt.py --selbsttest
```

## Rückfragen

1. **`lauf_p2.json`:** Bitte eine Probe der ersten 20 Punkte schicken, mit Schlüsseln und Einheit. Das Werkzeug erkennt Listen mit x/y (cm oder m) oder i/j, s je Punkt oder Bogenlänge, und hat sonst `--einheit`. Liegt s bei euch auf den 1-m-Punkten wie in den Querschnitten?
2. **Einschnitt:** Passt der Einschnitt am Beckenkopf (Median 1,6 m, bis 2,6 m) zu eurem Bild? Wenn nicht, rechne ich die flachere Variante (§2) und schicke dieselben vier Bilder.
3. **Durchbruch und Bergrinne:** Sollen sie auch neu geplant werden (§7)?
4. **`a15_einbau.py`:** Kann es einen Plan mit `abschnitte[]` je Feld ohne `wasser_koerper` lesen, wie hier geschrieben? Sonst bitte die Felder nennen, die es braucht.
