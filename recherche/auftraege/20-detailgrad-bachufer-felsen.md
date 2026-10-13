# 20 – Detailgrad Bachufer: Felsen, Schutt, Farne, Wasserkante (Referenz Ferat 13.10.)

Ferat (13.10. spät abends, nach 6f): „Schau mal, das ist auch ein Bild von einem River mit Unreal Engine, und schau unser – merkst du die
Qualität? Es geht hier nicht um Licht oder was anderes, rein um Detailgrad.“ Messlatte Witcher 4.

**Bilder:**
- Referenz: `bilder/zielbilder/unreal_fluss_detail_01.jpg` (1025 × 619 px, fremde UE-Szene, nachgeschärft mit Farbsäumen; Zählungen ±20 %). Original bei uns:
  `docs/zielbilder/ferat_2026-10-13/unreal_fluss_detail_01.png` (1025 × 619, identisch mit dem Repo-JPG; alle Pillow-Werte unten sind am PNG gemessen).
- Unsere: `bilder/swr_p2/bettplan_p2c_vorher_nachher.jpg` (Zeilen t430/t500/t550 Auge + t430 schräg; links alte Treppe, rechts P2C = Bettplan 6c
  eingebaut, 13.10. 21:52) und `bilder/swr_p2/bettplan_p2c_oben.jpg` (m_talkaskade, t500_schraeg). Einordnung: `bilder/zielbilder/witcher_01.jpg`.
- **Stand der P2C-Bilder:** Gelände + 621 Blöcke nach 6f, aber bachdekor_swr, kantenufer_p2 und die Lagen sind NICHT neu gerechnet (Stand vor 6f) – die
  Bach-Steine in den Bildern sind der Rest des alten Bachdekors (siehe §0 und §6). Jüngerer gespeicherter Stand **P2D** (`bilder/swr_p2/bettplan_p2d_dicht.jpg`,
  Screenshots 22:29–22:36, 388 Spline-Punkte je 1 m + 5 cm): laut Kontaktbogen Steine/Pflanzen identisch zu P2C, nur das Wasser anders → **für den
  Detailgrad gilt P2C**, P2D ändert keine Zahl in diesem Auftrag.

**Lesehinweis:** Alle Zahlen sind **Sichtschätzungen aus den Bildern**. Maßstabs-Anker Referenz: Vordergrundblock ≈ 1,5 m, Farn ≈ 0,6 m, Fluss ≈ 6–10 m
breit, linkes Ufer ≈ 15 m sichtbar, rechte Felswand ≈ 10 m lang / 6–8 m hoch, Kiefern 15–20 m. Eine Farb-Pixelmessung (grau/grün/ocker) konnte Fels
nicht von Boden trennen (warmes Licht färbt den Referenzfels ocker) – daher bei Stein und Bewuchs nur Sichtzählung; beim Wasser und für die Fugenschatten
Pillow-Messungen (Mittel-RGB → HSV, Luminanz-Streuung, Anteil hell-farbloser Pixel V > 0,80 / S < 0,20, dunkle V < 0,18), **immer mit Ausschnitt-Box
(x0, y0)–(x1, y1) in Pixeln des 1025 × 619-Bildes**, damit sie nachrechenbar sind (Boxen in §0 und §3).
Die Spalte **„Messlatte aus dem Bild“ (§1–§4) enthält nur, was in der Referenz zählbar ist – keine Regel von uns.** Werte, die NICHT aus dem Bild kommen
(Ableitungen aus der Witcher-Analyse, Potenzgesetz, Kamera-/Prüfregeln), stehen dort als Frage „Soll …?“ und gesammelt in §8.7 – bitte bestätigen, korrigieren
oder ersetzen (Regel „Details gibt die Cloud vor“). Wo sich frühere Sichtzählungen widersprachen, gilt die **Zähltabelle in §0**; alle anderen Stellen verweisen
darauf. Referenz ist Nadelwald/Felsbiom, unser Bach liegt im Heide-Tundra-Hang (C2): Ziele betreffen Struktur und Platzierung, nicht die Art.

## 0. Kurzbefund (die fünf Zahlen, die den Unterschied machen)

**Stand:** Die P2C-Bilder zeigen Gelände und Blöcke nach 6f, aber Bachdekor, Kantenufer und Lagen vom Stand VOR 6f (noch nicht neu gerechnet). Die Spalte
„unsere“ ist also ein Zwischenstand – bitte nicht als Endstand der 6f-Kette kalibrieren; nach der Neurechnung zählen wir neu.

**Zähltabelle Referenz** (EINE Sichtschätzung, ±20 %; gilt für alle Abschnitte – §1–§4 verweisen hierher):

| Klasse | linkes Ufer je 10 m (Band 0–3 m) | rechtes Ufer (Wandfuß, ≈ 8–10 m sichtbar) | ganzes Bild | Anmerkung |
|---|---|---|---|---|
| Kleinschutt 0,05–0,3 m | ≈ 50–100 einzeln erkennbar (Ausschnitt (0, 330)–(560, 619), 2× vergrößert); Lagen nicht ablesbar | > 200 im Schuttkegel, nicht einzeln zählbar | ≈ 300–400 | Lagen bei 5–30-cm-Stücken sind aus dem Bild nicht bestimmbar |
| Steine 0,3–1 m | ≈ 25–40, kantig/plattig, 3+ Größenstufen | ≈ 25–35 (Schuttband + Wandfuß) | ≈ 60–100 | |
| Blöcke 1–3 m | ≈ 5–8, davon ≈ 3 mit Fuß im Wasser | ≈ 4–6, davon ≈ 3–4 im Wasser | ≈ 10–15, davon ≈ 6–7 im Wasser | |
| Steine/Blöcke 0,5–2 m mit Fuß im Wasser | ≈ 3 | ≈ 3–4 | ≈ 6–7, dazu 4–5 Felsinseln im Bett | frühere „8–10 je 10 m“ zählte Blöcke und Inseln zusammen |
| Anstehender Fels > 3 m | 1 Terrasse ≈ 4–6 m (Mittelgrund) | Wand 6–8 m hoch, ≥ 10 m lang | 3–4 Massen | |
| Farne | 2 sichere Horste (Bildmitte unten, x ≈ 370–520 px) + 1 unsicherer am rechten Rand des linken Ufers | 0 | 2–3 | nur am Gleitufer |
| Verhältnis je Größenklasse abwärts | 1–3 m → 0,3–1 m ≈ 5–6 : 1; 0,3–1 m → 0,1–0,3 m ≈ 1,5–3 : 1 (links allein) | | 0,3–1 m → 0,1–0,3 m ≈ 3–6 : 1 nur mit Schuttkegel | das glatte „× 3–10 je Klasse“ (§4) ist eine Ableitung, keine Zählung |

**Kurzbefund** (Band 0–3 m vom Wasser, je 10 m Ufer; Referenz = linkes Ufer der Zähltabelle):

| Größe | Referenz | unsere (P2C) | Faktor |
|---|---|---|---|
| Stein-/Felsbedeckung | ≈ 85–95 % | ≈ 3–5 % 3D-Stein (+ 30–40 % nackter Boden) | ≈ 20× |
| Kleinschutt 0,05–0,3 m | ≈ 50–100 links; > 200 nur im Schuttkegel rechts; füllt jede Lücke | 0 (Kies nur als Textur unter Wasser) | – |
| Steine 0,3–1 m | ≈ 25–40, kantig/plattig, 3+ Größenstufen | ≈ 8–14, gerundet, eine Größe 0,4–0,7 m | ≈ 3× |
| Steine mit Fuß im Wasser | ≈ 3 je 10 m und Ufer (6–7 im Bild + 4–5 Felsinseln) | ≈ 1–2 | ≈ 2–3× |
| Stapelung / Einbettung | 2–3 Lagen, 30–50 % eingegraben | 0 Lagen, ≈ 0 % eingegraben (Unterkante sichtbar) | – |
| Fugen-/Kontaktschatten zwischen Steinen | ≈ 20–30 % der Steinfläche (Sicht); Pillow Uferband links (0, 420)–(560, 619): 24,5 % Pixel V < 0,18 (inkl. Pflanzenschatten) | ≈ 0 (jeder Stein liegt frei auf glattem Boden) | – |

**Einheitliche Messlatten** (gelten in §1–§4, dort nur noch verwiesen): Kontakt (Stein berührt einen Nachbarn oder liegt auf einem) **≥ 60 %** der Stücke > 0,3 m;
Eingraben **≥ 50 % der Stücke zu ≥ 1/3** der Netzhöhe (Referenz: 30–50 % sichtbar eingegraben, Rest verkeilt); sichtbare Erde/Schlamm am Wasser (0–1 m)
**≤ 5 %** der Uferlänge, im Band 1–3 m **≤ 10 %**; Kleinschutt-Ziel **≤ Referenz = 50–100 je 10 m am Gleitufer, > 200 nur als Schuttband am Wandfuß** –
Frage an die Cloud: Soll es ≥ 2 Lagen sein? (aus dem Bild nicht ablesbar); Farne **2–3 je 10 m, nur Gleitufer** (beide Ufer wäre mehr als die Referenz – Frage).

Der Unterschied ist nicht Licht: Es ist (1) Stein als Füller statt Erde, (2) fünf Größenklassen statt zwei, (3) Kontakt/Stapel statt Perlenkette,
(4) Pflanzen in Ritzen statt Teppich, (5) Wasserkante aus Stein mit Gischt statt glatter Erdkante, (6) dunkle Fugen zwischen gestapelten Platten statt frei
liegender Einzelsteine.

## 1. Blickwinkel FELSEN UND STEINE am Ufer

**Referenz (Sichtschätzung):**
- Bedeckung: linkes Ufer 0–4 m vom Wasser ≈ 85–90 % Stein/Fels, Rest Farn/Grasbüschel ≈ 10–15 %, nackter Boden ≈ 0 %; rechtes Ufer ≈ 95 % Fels
  (anstehende Wand + Schutthalde am Fuß).
- Größenklassen links je 10 m Ufer (Zähltabelle §0): < 0,3 m ≈ 50–100 einzeln erkennbar – die Hunderte liegen rechts im Schuttkegel; 0,3–1 m ≈ 25–40 Platten;
  1–3 m ≈ 5–8 Blöcke; > 3 m: 1 anstehende Felsterrasse ≈ 4–6 m im Mittelgrund. Rechts: Wand ≈ 6–8 m hoch, ≥ 10 m lang, Bäume obenauf; Schuttband ≈ 2 × 8 m
  mit > 200 Splittern 0,1–0,5 m; davor 4–6 Blöcke 1–2 m im Wasser.
- Form: ≈ 80–90 % kantig, plattig/schichtig (Schiefer-Art), scharfe Kanten; die Blöcke im Wasser (Mittelgrund) und am rechten Wandfuß sind blockig-gerundet
  (≈ 10–20 %); 0 Findlinge mit Mooskappe.
- Stapelung: Platten in 2–3 Lagen, gleiche Fallrichtung (Kippwinkel ± ≈ 20°), verkeilt; ≈ 30–50 % halb eingegraben; Splitter in den Rissen; Haufen
  von 5–15 Stück, dazwischen Lücken 1–3 m mit Farn/Gras.
- Fugen: dunkle Kontaktschatten zwischen den gestapelten Platten ≈ 20–30 % der Steinfläche (Sicht; Pillow 24,5 % Pixel V < 0,18 im Uferband links, §0) – bei uns
  0, weil jeder Stein frei auf glattem Boden liegt. Rechts hängen Felsplatten mit dunklem Schattensaum über das Wasser (Unterschneidung/Überhang).
- Übergang Ufer → Wasser: je 10 m und Ufer ≈ 3 Blöcke 0,5–2 m mit Fuß im Wasser (6–7 im Bild, Zähltabelle §0); Wasserkante fast überall Stein (Erdkante ≤ 5 %);
  Wildwasser/Schaum um die Blöcke; Nasszone dunkel ≈ 0,2–0,5 m über Wasser; im Bett 4–5 Felsinseln.
- Tiefe: Felsrippen bis zum Horizont (links 3 Staffeln, rechts 2); Blöcke in 30 m noch als Einzelformen lesbar.
- witcher_01 (Einordnung): Ufersteine 0,3–1 m in Gruppen (≈ 15 auf ≈ 20 m), halb im Gras, 3–4 im Wasser, Kieszone – weniger Fels, gleicher Grundsatz.

**Unsere (alle 5 P2C-Bilder):**
- Bedeckung Ufer 0–3 m: echte 3D-Steine ≈ 3–5 %; Heide/Gras ≈ 50–55 %; nackter beiger Boden ≈ 30–40 %; Bettwände = dunkle „geschmolzene“
  Verschiebungs-Textur ohne Einzelstücke (t430 rechts, t550 links: ≈ 60 % der sichtbaren Wand).
- Größenklassen je 10 m: < 0,3 m auf dem Ufer ≈ 0; 0,3–1 m ≈ 8–14 (Talkaskade ≈ 35 auf ≈ 25 m, t500: 12 an einer Stufe, schräg ≈ 20 auf ≈ 15 m);
  1–3 m ≈ 0,5–1 (t500: 2, t430/t550: je 1, Talkaskade: 2); > 3 m anstehend: 0.
- Form: ≈ 90 % gerundet/oval (Findling-Netze mit Moos), ≈ 10 % flache Platten; 0 kantige Schichtplatten.
- Stapelung: 0 Lagen – jeder Stein einzeln auf der Oberfläche, keiner in Rissen, ≈ 0 % eingegraben (Unterkante sichtbar, t500 Stufe, Talkaskade Reihe).
- Anordnung: Perlenkette entlang der Stufenkanten (Abstand ≈ 1 m, gleiche Größe 0,4–0,7 m), je Stufe 4–7 Stück, keine Haufen, keine Lücken-Rhythmik –
  Ferats „alle gleich groß, regelmäßig“ ist aus Talkaskade/schräg direkt ablesbar.
- Übergang: je 10 m ≈ 1–2 Steine mit Fuß im Wasser; Wasserkante = glatte Textur/Erde auf ≈ 80 % der Länge; keine Nasszone; Schaum nur als Streifen an der Lippe.
- Schutt/Kies zwischen Blöcken: 0 auf dem Ufer. Tiefe: ab ≈ 15 m keine Steinformen mehr lesbar (nur Farbtupfer); keine Felsrippen am Hang.

| Element | Referenz | unsere | Messlatte aus dem Bild | Wirkung |
|---|---|---|---|---|
| Steinbedeckung 0–3 m | ≈ 85–90 % links, ≈ 95 % rechts, nackt ≈ 0 % | ≈ 3–5 % 3D-Stein, nackt ≈ 30–40 % | Fels/Stein ≥ 70 % (Prallhang ≥ 85 %), nackter Boden ≤ 5 % am Wasser / ≤ 10 % im Band 1–3 m (§0), Rest Farn/Gras in Lücken | groß |
| Kleinschutt < 0,3 m | ≈ 50–100 je 10 m links, > 200 im 2-m-Schuttband am Wandfuß (§0) | 0 auf dem Ufer | 50–100 Stück 0,05–0,3 m je 10 m als 3D-Netze in den Lücken (≤ Referenz); Soll ≥ 2 Lagen? (nicht ablesbar); 1 Schuttband 1–2 m mit > 200 Stücken am Fuß jeder Wand | groß |
| Fugen-/Kontaktschatten | ≈ 20–30 % der Steinfläche dunkel (Pillow 24,5 % V < 0,18 im Uferband links (0, 420)–(560, 619)) | ≈ 0 % (t500-Ufer: Steine frei auf glattem Boden) | Pillow im Uferband 0–3 m unserer Prüfbilder: Anteil V < 0,18 ≥ 15 % (Referenz-Ausschnitt gegen t500-Ufer, gleiche Box-Definition) | groß |
| Mittelklasse 0,3–1 m | ≈ 25–40 je 10 m, kantig, 3+ Größenstufen (§0) | ≈ 8–14, gerundet, eine Größe | 25–40 je 10 m; ≥ 70 % kantig/plattig, gerundet ≤ 30 % und nur im Bett; Stufen 0,3/0,5/0,8 m je ≥ 20 % | groß |
| Stapelung/Verzahnung | 2–3 Lagen, gleiche Fallrichtung, 30–50 % eingegraben | 0 Lagen, 0 % eingegraben | Kontakt ≥ 60 %, Eingraben ≥ 50 % zu ≥ 1/3 (§0); Kipp je Gruppe ± 20°; Haufen 5–15 mit Lücken 1–3 m | groß |
| Übergang Ufer → Wasser | ≈ 3 Blöcke je 10 m und Ufer im Wasser (§0), Kante ≈ 100 % Stein, Nasszone 0,2–0,5 m | ≈ 1–2, Kante ≈ 80 % Erde, keine Nasszone | ≥ 3 Steine 0,5–2 m je 10 m und Ufer mit Fuß im Wasser; Erdkante am Wasser ≤ 5 % (§0); Nasslinie 0,2–0,5 m (ue_fels_nasslinie.py in Arbeit) | groß |
| Blöcke 1–3 m | ≈ 5–8 je 10 m, 2–3 im Wasser, 4–5 Felsinseln | ≈ 0,5–1, meist auf dem Ufer | 3–6 je 10 m, 1–3 ins Wasser ragend; je 20 m Bett 1–2 Felsinseln 1–2 m | mittel |
| Anstehender Fels > 3 m | Terrasse ≈ 5 m, Wand 6–8 × ≥ 10 m mit Bäumen | 0 (Bettwände nur Textur) | je 50 m ≥ 1 Felskörper ≥ 3 m (Prallhang); Bettwände ≥ 60 % mit 3D-Netzen, „geschmolzene“ Textur ≤ 20 % | mittel |
| Lesbarkeit in der Tiefe | Einzelblöcke bis ≈ 30 m, 3 Felsstaffeln | ab ≈ 15 m Farbtupfer, 0 Rippen | aus 30 m je 10 m Ufer ≥ 10 Einzelformen ≥ 0,5 m; je 100 m Talhang ≥ 2 Felsrippen > 3 m | mittel |

## 2. Blickwinkel BEWUCHS

**Referenz:**
- Zonierung: 0–1 m vom Wasser ≤ 5 % Pflanzen (nasser nackter Stein; links stehen stellenweise Grasbüschel ≤ 0,5–1 m am Wasser – Ausschnitt links vorn und
  rechter Rand des linken Ufers); 1–3 m ≈ 15–25 % bewachsen, ausschließlich in Spalten/Steinlücken; 3–10 m ≈ 50–60 % (Gras, Moos/Flechte, Busch, Baum);
  keine Pflanze im Wasser.
- Farne (Zähltabelle §0): 2 sichere Horste (Bildmitte unten, x ≈ 370–520 px) + 1 unsicherer am rechten Rand des linken Ufers = 2–3 auf ≈ 10 m Gleitufer, 0 am
  rechten Ufer; 0,5–0,9 m breit, 0,3–0,5 m hoch, in Lücken ZWISCHEN Blöcken 1–3 m vom Wasser.
- Grasbüschel: ≈ 10–15 auf 10 m, 0,2–0,4 m, jedes in einer Steinlücke (≈ 100 % berühren einen Stein); ≈ 50 % braun-trocken gemischt. Rechte Platte:
  niedriger Grasfilz 0,1–0,2 m über 40–60 % der Fläche.
- Moos/Flechte: Felsoberseiten ab ≈ 2 m über Wasser 30–50 % mit Flecken 0,2–1 m (nie Vollkappe); Steine 0–1 m über Wasser 0 % Moos, grau-nass.
- Bäume: ≈ 8–9 Kiefern/Fichten 12–20 m in 2 Gruppen (2 + 6–7), Stammfuß 2–6 m vom Wasser auf dem 4–6 m hohen Felsvorsprung, Wurzeln zwischen Steinen.
- Büsche: 2–3 niedrige 0,5–1,2 m an Baumfuß/Vorsprungsfuß (2–6 m vom Wasser). Nackter Boden 3–10 m: ≈ 0–5 % – der Füller ist Fels.
- Bildanteile (Schätzung): Fels/Stein ≈ 45–50 %, Wasser ≈ 25–30 %, Pflanzen ≈ 15–20 %, Himmel ≈ 10 % (Pillow: helle, ungesättigte Pixel V > 0,80 / S < 0,20
  allein in den Zeilen 0–200 = 10,4 % des ganzen Bildes = Himmel + Dunst). Totholz: 0 Stämme, höchstens 2–3 dürre Zweige (unsicher).
- Artenzahl 5 (Nadelbaum, Farn, Grasbüschel, Moos/Flechte, Kleinbusch) – Pflanzen sind Beiwerk in den Lücken, nie Fläche.

**Unsere:**
- Zonierung (t550, m_talkaskade, schräg): 0–0,5 m vom Wasser 0 % (glattes dunkles Erdband 0,5–1,5 m, ohne Steine); ab ≈ 1 m sofort die Hangdecke:
  1,5–2 Pflanzen/m² gleichmäßig, beide Ufer und bis zum Grat identisch – kein Übergang, keine Lücken-Logik.
- Je 10 m Uferhang (≤ 5 m vom Wasser): ≈ 15–25 Heidebüschel (rosa, 0,3–0,5 m) + ≈ 15–20 Grasbüschel (einheitlich grün-gelb, 0 % trocken). Schräg auf
  ≈ 40 m Bach: > 150 Blüten- + > 150 Grasbüschel, Teppich ohne Inseln.
- Farne: 0 in allen 5 Bildern. Moos: nur Vollkappe auf 3–4 Großblöcken (100 % der Oberseite); 0 % auf Uferfels/Böschung/12–40 Kaskadensteinen.
- Bäume: 1–3 je Bild in 60–150 m; 0 innerhalb 20 m des Ufers. Büsche: 0 am Ufer. Nackter Boden 1–10 m: ≈ 40–50 % heller Ockerboden.
- Totholz: 0; Kleinzeug 30–40 Fallblätter je Bild, 1 Fliegenpilz (t430) + 2 Pilze (schräg).
- Fehler: t500_auge ein Grashalm ≈ 1,5 m über dem halben Bach (Kamera im Gras, laut 6f kein Weltfehler – trotzdem Kamera-Regel nötig); m_talkaskade
  unten links weißliche flache Form (Knochen/Blattrest?); Pflanzen „schweben“ auf glatter Erde statt an Steinen anzuliegen. Artenzahl 4, alle als Fläche.

| Element | Referenz | unsere | Messlatte aus dem Bild | Wirkung |
|---|---|---|---|---|
| Füller zwischen Pflanzen | 3–10 m: 0–5 % nackte Erde; Zwischenraum = Fels, Moosflecken, Grasfilz 0,1–0,2 m | 1–10 m: ≈ 40–50 % Ockerboden | nackte Erde ≤ 15 % im Band 1–10 m, Rest Stein ≥ 0,2 m / Moos / Grasfilz ≥ 80 % Deckung; Prüfung je 10-m-Abschnitt beider Ufer | groß |
| Pflanzen in Ritzen | 0–3 m: ≈ 100 % berühren einen Block ≥ 0,3 m | ≈ 0 % berühren einen Stein | ≥ 80 % der Büschel/Farne im Band 1–3 m ≤ 0,3 m an einem Stein ≥ 0,3 m; 5–8 Grasbüschel je 10 m in Lücken | groß |
| Farne | 2–3 Horste je 10 m, nur Gleitufer, 1–3 m vom Wasser, in Blocklücken (§0) | 0 | 2–3 Horste 0,4–0,9 m je 10 m Gleitufer, in Lücken zwischen Steinen ≥ 0,5 m; Fragen: Soll es beide Ufer sein (wäre mehr als die Referenz)? Soll die Schattenseite bevorzugt werden (nicht aus dem Bild)? | groß |
| Teppich statt Inseln | Dichte wechselt 0 % ↔ 50–60 % über 3–5 m; witcher_01 Blüteninseln 2–5 m auf 20–30 % | 1,5–2/m² überall gleich, > 150 auf 40 m | Heide auf ≤ 30 % des Hangs in Inseln 2–5 m, Abstand 3–10 m; Frage: Soll die Dichte benachbarter 5-m-Felder um ≥ Faktor 3 wechseln? (Prüfregel, nicht aus dem Bild) | mittel |
| Moos/Flechte als Flecken | Fels ≥ 2 m über Wasser 30–50 % Flecken 0,2–1 m; 0–1 m: 0 % | 3–4 Vollkappen, sonst 0 % | 30–50 % der Steine > 1,5 m über Spiegel mit Flecken 20–60 % Deckung; < 1 m über Spiegel 0 % | mittel |
| Ufergehölz | 8–9 Nadelbäume in 2 Gruppen, Fuß 2–6 m vom Wasser auf Fels | 0 innerhalb 20 m | je 50 m ≥ 1 Gruppe 3–6 Bäume 8–20 m, Fuß 2–6 m vom Wasser auf Schulter/Fels, von ≥ 2 Steinen ≥ 0,3 m umgeben; Art nach Biom | mittel |
| Büsche/Kraut oben | 2–3 je 10 m, 0,5–1,2 m, an Baum-/Vorsprungsfuß | 0 am Ufer | 1–3 je 10 m im Band 2–6 m, je an Stein oder Baumfuß | mittel |
| Trockene Alt-Halme | ≈ 50 % der Büschel braun gemischt | 0 % | 30–50 % der Büschel im Band 0–10 m mit braunen Halmen (Variante/Tint) | klein |
| Maßstabs-/Platzierungsfehler | höchster Halm 0,4 m, nichts über dem Wasser | 1,5-m-Halm (Kamera), weiße Form | kein Grasnetz > 0,6 m im Band 0–3 m; 0 Halme über Wasser; Form identifizieren | klein |
| Totholz | 0 Stämme, 2–3 Zweige (unsicher) | 0 Stämme; Blätter + Pilze | aus der Referenz nicht ableitbar; Frage: Sollen die Witcher-Analyse-Werte gelten (1–2 Stücke 1–3 m je 20 m, Zweige in 3–5 Steinlücken je 10 m)? | klein |

## 3. Blickwinkel WASSER (Pillow-Messungen + Sichtschätzung)

**Referenz:** Riffel-Fluss 6–10 m breit (durchgehende Schnelle, KEINE Becken-Stufen-Folge). **Pillow am PNG, Boxen (x0, y0)–(x1, y1) in Pixeln:**
ruhiges Wasser rechts unten (620, 470)–(1000, 600): RGB 78/72/60 = Farbton 42°, Sättigung 0,23, Helligkeit V 0,30, Luminanz-Streuung 53, hell-farblos
4,4 %, dunkel (V < 0,18) 37 %; Mitte (560, 330)–(760, 420): 67/58/47, 34°, 0,29, V 0,26, Streuung 42, hell 2,2 %, dunkel 33 %; ferne Schnelle
(330, 290)–(520, 340): 150/141/128, 37°, 0,14, V 0,59, Streuung 68, hell 28 %, dunkel 10 %. (Die früheren Werte „V 0,38–0,42 / hell 9–10 % / dunkel
13–21 %“ standen ohne Box, sind nicht nachrechenbar und treffen keine dieser Zonen – gestrichen.) Dunkel-olivgrau, klar; Farbe aus dunklem Grund +
Himmelsglanz. Kräuselung ≈ 5–15 cm + Wellen 20–40 cm, nirgends spiegelglatt. Schaum: weiße Streifen 0,5–2 m an der fernen Schnelle um 3 Felsen; **auch im
Mittelgrund (10–15 m) weißer Schaum am Fuß der angeströmten Uferblöcke** (x ≈ 560–700, y ≈ 380–440 px), Kragen ≈ 0,2 m an der Anströmseite; nah (< 5 m)
nur Glanzlichter. Himmel nur als zerbrochene Glanzpunkte; Strömung in < 1 s lesbar (alle Streifen talwärts). Grund: rechts 0–1,5 m vom Rand Steine unter
Wasser sichtbar, Mitte dunkel (> 1 m) → Tiefenverlauf lesbar. Wasserkante links auf ≈ 10 m: Zähltabelle §0 (≈ 25–40 Steine 0,3–1 m + 5–8 Blöcke 1–3 m,
≈ 3 mit Fuß im Wasser), Steinbedeckung 0–3 m ≈ 90–95 %, nackte Erde ≤ 5 %, Gras/Farn fast immer ≥ 1 m hinter der Steinkante. Steine ≥ 3 Formen,
grau/braungrau, ≈ 30 % Moos oben, dunkler Nassstreifen 10–20 cm. Vorbehalt: Nachschärfung erhöht die Kontrastzahlen geschätzt 10–15 % – die Lücke bei der
Streuung ist in der Nahzone Faktor 1,2–2, in Schnellen > 2.

**Unsere** (Nachmessung 13.10. spät, reproduziert ± 5 Einheiten; Boxen unserer Bilder = Nahzone ≤ 5 m, Ausschnitt ≥ 300 × 150 px – die genauen Pixelboxen
werden mit der nächsten Messreihe nachgetragen, damit beide Seiten gleich definiert sind): Bach 2–4 m, Becken 3–4 × 4–5 m hinter Lippen (t500_schraeg:
12 Becken auf ≈ 30 m, alle 3–4 m lang). Farbe: t430 RGB 78/66/63 (13°, 0,19, V 0,31, Streuung 25); t550 129/106/84 (30°, 0,35, 0,51, 29); Talkaskade
105/87/64 (34°, 0,39, 0,41, 31); t500 100/80/57 (32°, 0,43, 0,39, 37) → braun-golden bis trüb, Sättigung bis 0,43, Farbton rötlicher. Luminanz-Streuung
25–37 (Referenz nah 42–53); hell-farblose Pixel 0,0–0,2 % (Referenz nah 2–4 %); dunkle Täler 0–7,5 % (Referenz nah 33–37 %); statt Kräuselung
marmorierte Schlieren 30–60 cm ohne Richtung. Schaum: 0 Streifen, 0 Kragen; Stufen-Überlauf = 2 Fäden ≈ 2 cm; schräg 1,4 % helle Pixel = der
milchige Fleck, keine Gischt. Brechung: Ufer durch die Fläche gesehen = senkrechte Schlieren 0,5–1 m (t430 rechts, t550 links). Grund: Beckenboden
glatter Schlamm, 0 Steine sichtbar, Tiefe nicht lesbar; ≈ 75 % des Bettes nacktes Braun; ≈ 45 Steine 0,3–0,7 m auf 30 m fast nur auf den Lippen.
Wasserkante: Steinbedeckung 0–3 m ≈ 15–20 % (t430), ≈ 0 % (t550 links); Beckenwand glatt 0,6–0,8 m ohne Steine; Grasnarbe bündig am Spiegel; 2–3
Steine je 10 m ragen heraus. Steine 1 Farbe (hellocker), 1–2 Formen, Moos ≈ 10 %, kein Nassstreifen.

| Element | Referenz | unsere | Messlatte aus dem Bild | Wirkung |
|---|---|---|---|---|
| Mikrokontrast / Wellenmaßstab | nah ruhig (Boxen oben): Streuung 42–53, hell 2–4 %, dunkel 33–37 %; Schnelle: Streuung 68, hell 28 %, dunkel 10 %; Kräuselung 5–15 cm | Streuung 25–37; hell 0–0,2 %; dunkel 0–7,5 %; Schlieren 30–60 cm | Nahzone ≤ 5 m, gleiche Box-Definition für Referenz und uns (Ausschnitt ≥ 300 × 150 px, Box angeben): Streuung ≥ 40, hell-farblos 2–5 % ruhig / 15–30 % Schnelle, dunkel ≥ 25 % ruhig; Kräuselung 5–15 cm, Schlieren ≤ 15 cm | groß |
| Farbe / Klarheit | nah ruhig 34–42°, S 0,23–0,29, V 0,26–0,30; Schnelle V 0,59 | 13–34°, S 0,19–0,43, V 0,31–0,51 | Nahzone ruhig: 35–45°, S ≤ 0,30, V 0,25–0,35; Schnellen V ≥ 0,5; Steine bis 0,5 m Tiefe erkennbar | groß |
| Schaum/Gischt | Streifen 0,5–2 m fern; Kragen ≈ 0,2 m am Fuß angeströmter Blöcke auch in 10–15 m; 28 % Weiß in der Schnelle | 0 / 0 / 0,0–0,2 % | je ragendem Stein in Strömung Kragen 0,1–0,3 m + Nachlauf 0,5–1 m (sichtbar bis ≥ 15 m); je Lippe weiße Schürze ≥ 60 % der Breite, 0,5–1,5 m ins Becken; Weiß ≥ 15 % in Schnellen | groß |
| Wasserkante Steine 0–3 m | Zähltabelle §0: 25–40 + 5–8 Blöcke je 10 m, ≈ 3 mit Fuß im Wasser, Bedeckung 90–95 % | 15–20 % / ≈ 0 %; 2–3 ragen heraus; Beckenwände 0 Steine | je 10 m und Seite 25–40 Steine 0,3–1 m + 3–6 Blöcke 1–3 m; Bedeckung ≥ 70 %; ≥ 2 je 10 m mitten im Wasser; Steine in ALLEN Lagen (Bett, Beckenwand, Lippe, Uferband); Erde/Schlamm am Wasser ≤ 5 % (§0) | groß |
| Grund / Tiefe lesbar | 0–1,5 m Steine sichtbar, Mitte dunkel | Schlamm, 0 Steine, ≈ 75 % nacktes Braun | erste 1,5 m vom Spiegel ≥ 50 % Steine 0,1–0,5 m; Beckenböden ≥ 30 % Stein; Helligkeitsgefälle Ufer → Mitte ≥ 0,15 (V) | groß |
| Brechungs-Schlieren | 0 | senkrecht 0,5–1 m in 2 Bildern | 0 in Nahbildern; Ursache vermutlich Normalen-Verzerrung × steile Uferwand – Frage: Soll dafür die Diagnose-Reihe D/W laufen? (nicht aus dem Bild) | mittel |
| Strömung / Spiegelung | Streifen talwärts, Himmel als Glanzpunkte | Wirbel ohne Richtung, milchige Lumen-Fläche | ≥ 80 % der Streifen ≤ 30° zur Bachachse; je Becken Zu- und Ablaufzunge; keine helle Spiegelfläche > 1 m² | mittel |
| Steinvielfalt / Nassstreifen | ≥ 3 Formen, 0,2–5 m, grau, 30 % Moos, Nass 10–20 cm | 1 Farbe, 1–2 Formen, 2 Blöcke > 1,5 m in 5 Bildern, 0 Nass | ≥ 3 Formen je 20 m; ≥ 1 Block ≥ 2 m je 20 m; S ≤ 0,25; Moos 20–40 %; Nassstreifen 0,1–0,3 m | mittel |
| Grasnarbe an der Kante | Gras fast immer ≥ 1 m hinter der Steinkante, direkt am Wasser ≤ 5 % | bündig am Spiegel | Gras ≥ 1 m hinter der Steinkante; Gras direkt am Wasser ≤ 5 % der Länge (§0); Frage: Soll der Grasfuß ≥ 0,3 m über dem Spiegel liegen? (nicht aus dem Bild) | mittel |
| Bettform (6c-Einordnung) | durchgehende Schnelle, 5–10 m ohne Becken | 12 Becken/30 m, alle 3–4 m, gleich tief | aus dem Bild nur: keine gleichförmige Beckenfolge. Frage: Soll Beckenabstand 3–12 m, jede 3. Stufe ohne Becken (Rinne ≥ 5 m), Breite ± 30 % gelten? (unsere Ableitung für euren Bettplan) | mittel |

## 4. Blickwinkel KOMPOSITION UND MASSSTAB

**Referenz:** Fluss vorn 6–10 m, hinten 15–20 m. Uferform links Felsböschung 15–25°, ≈ 80–90 % geschichtete Platten (Zähltabelle §0: ≈ 25–40 Platten
0,3–1 m je 10 m links, 60–100 im ganzen Bild), Profil in 5–8 Stufen 0,3–1 m gebrochen; rechts Wand 5–8 m, 70–90°, am Fuß Schuttkegel 0,05–0,3 m (> 200),
dann Gras, dann Wasser. **5 Größenklassen in einem Bild** – Kies < 0,1 m (Schuttkegel), 0,1–0,3 m (≈ 300–400 mit Schuttkegel, davon ≈ 50–100 links einzeln
erkennbar), 0,3–1 m (60–100), 1–3 m (10–15, davon 6–7 im Wasser), Fels > 5 m (3–4 Massen). Gezähltes Verhältnis abwärts: 1–3 m → 0,3–1 m ≈ 6 : 1;
0,3–1 m → 0,1–0,3 m ≈ 3–6 : 1 nur mit Schuttkegel, links allein ≈ 1,5–3 : 1 – ein glattes „× 3–10 je Klasse“ (Potenzgesetz) ist Ableitung, keine Zählung.
70–80 % der Steine berühren einen Nachbarn, ≥ 50 % eingegraben, Kiesel-Anteil ≈ 10 %.
Uferlinie gezackt: 5–8 Vorsprünge/Buchten ≥ 0,5 m je 10 m. Bewuchs 15–20 % des Ufers in Steinlücken; 5–6 Nadelbäume 15–20 m direkt am Wasser rahmen.
Staffelung 3 Ebenen (0–5 m Platten + Farn / 10–40 m Felsnase, Wand, Bäume / Bergkette als Silhouette – Dunst nur benannt); Wasser führt als S-Kurve
zur hellen Öffnung = Blickziel. Maßstab stimmig: Blöcke 1–2 m im Wasser = 15–25 % der Flussbreite, größtes Objekt nie allein.

**Unsere:** Bettbreite 2–4 m; Böschungswände 0,5–1 m hoch, 35–70° steil, als GLATTE Erd-/Plattenfläche („gezogener Graben“); senkrechte Texturstreifen
über 1–2 m an den steilen Wänden (t430 rechts, t550 links) – sofort als Fehler lesbar. **2 Größenklassen:** Kiesel 0,3–0,6 m (t500_auge ≈ 16,
t500_schraeg ≈ 45 auf ≈ 60 m = 7–8 je 10 m), Blöcke 1–1,5 m 2–4 je Bild; nichts < 0,3 m, kein Fels > 3 m. ≈ 0 % Kontakt, ≈ 0 % eingegraben, 1 Formfamilie,
Kiesel-Anteil ≈ 90 %. Band 0–3 m ≈ 5–10 % Stein; Hang 3–15 m: 0 Felsnasen, 0 Steingruppen auf ≈ 30 × 10 m. Uferlinie = glatte Brush-Kurve, 0 Vorsprünge;
≈ 10 Becken auf ≈ 60 m, alle 3–4 × 4 m, Wand 0,8 m bei 60–70°. Blöcke 1–1,5 m = 40–60 % der Bettbreite ohne Begleitsteine → isolierte Riesen.
Staffelung 2 Ebenen (Bett / Heidehang), Berge in 2–3 km scharf (Dunst nur benannt); Wasser führt zu keinem Ziel. 0 Bäume ≤ 10 m vom Wasser in 4 von 5
Bildern. witcher_01: Ufersteine in Gruppen (≈ 20–30 vorn), Gras bis ans Wasser – näher an der Referenz als an uns, aber Wiesenbach.

| Element | Referenz | unsere | Messlatte aus dem Bild | Wirkung |
|---|---|---|---|---|
| Steilufer als Fels | ≈ 100 % der Flächen > 35° Fels/Steinpackung; Erde am Wasser ≤ 5 % | 0 % Fels an > 35°; glatte Wände mit Texturstreifen; Erde 60–80 % | jede Fläche > 35° zu ≥ 90 % Felsnetze/Steinpackung; Erde am Wasser ≤ 5 %, Band 1–3 m ≤ 10 % (§0); Frage: Soll ab 45° gar keine Landschaftstextur mehr sichtbar sein? (nicht aus dem Bild) | groß |
| Größenspektrum | 5 Klassen (Zähltabelle §0) | 2 Klassen | je 10 m im Band 0–3 m: 50–100 × 0,05–0,3 m (Gleitufer; > 200 nur als Schuttband am Wandfuß) + 25–40 × 0,3–1 m + 3–6 × 1–3 m; je 20–30 m 1 Felsmasse > 3 m; Frage: Soll die Stückzahl je Klasse ≥ 3× die nächstgrößere sein (Potenzgesetz = Ableitung, Entscheidung Cloud)? | groß |
| Packung statt Perlenkette | 70–80 % Kontakt, ≥ 50 % eingegraben, 3 Formfamilien, Kiesel ≈ 10 % | ≈ 0 % / ≈ 0 % / 1 Familie / Kiesel ≈ 90 % | Kontakt ≥ 60 %, Eingraben ≥ 50 % zu ≥ 1/3 (§0); ≥ 3 Familien je 10 m; runde Kiesel ≤ 30 % der Stücke > 0,3 m | groß |
| Uferlinie / Becken | 5–8 Vorsprünge je 10 m; keine zwei gleichen Formen | 0 Vorsprünge; 10 gleiche Becken auf 60 m | ≥ 4 Vorsprünge/Buchten ≥ 0,5 m je 10 m (durch Stein, nicht Erde); Beckenlängen 2–8 m, größtes/kleinstes ≥ 3:1; Frage: Sollen Erdwände ≤ 45° bleiben, steiler nur als Fels? (nicht aus dem Bild) | groß |
| Hang über dem Bett | ≈ 5 Felsnasen/Gruppen auf ≈ 300 m², Steine bis 10–20 m vom Wasser | 0 / 0 | ≥ 1 Felsnase oder Gruppe (≥ 5 Steine 0,3–1 m) je 100 m² im 10-m-Streifen; Stein 3–10 m ≥ 20 %; je 10 m Hanglinie ≥ 2 Höhensprünge ≥ 0,3 m | mittel |
| Großblock-Maßstab | größter Block 15–25 % der Breite, nie allein (immer mit Begleitsteinen) | 40–60 % der Bettbreite, ohne Begleiter | Block > 40 % Breite nie allein; sonst ≤ 0,8 m; Fragen: Sollen es ≥ 5 Begleitsteine 0,3–1 m im Umkreis 2 m + Kleinschutt sein? Prüfregel „keine Gras-Instanz < 0,5 m an der Prüfkamera“? (beides nicht aus dem Bild) | mittel |
| Staffelung / Blickziel | 3 Ebenen; Wasser führt zur Öffnung; 5–6 Bäume am Wasser rahmen | 2 Ebenen; Wasser endet hinter Lippe | ≥ 1 Baum ≥ 8 m innerhalb 5 m vom Wasser je 30 m; Frage: Soll die Blickachse in ≥ 2 von 3 Prüfkameras ein Ziel in 20–60 m treffen? (Prüfregel, nicht aus dem Bild) | mittel |
| Bewuchs in Lücken | 15–20 % des Ufers zwischen Steinen | 0 % im Bett/an Wänden, Teppich endet an der Lippe | 10–25 % des 0–3-m-Bandes mit Büscheln/Farn IN Lücken, ≥ 3 Arten je 10 m, ≥ 1 Farn je 10 m; harte Kante ≤ 20 % der Länge | klein |

## 5. Inventar-Zuordnung (was wir haben, womit wir es heute setzen, was fehlt)

Quelle: `export/unreal/welt/inventar/` (1 965 Netze, 13d), `scripts/bachdekor/bachdekor_swr_regeln.json`, `kantenufer_p2`, Cloud-Bettplan 6c, Rural Australia
`swr/ra_inventar.json`. Maße = Netz-Bounds (L × B × H). „fehlt“ = Netz oder Planer-Rolle fehlt; sonst nur Dichten/Regelwerte. Fab-Megascans-Netze führt
netze.csv nur mit der ID als Namen (`uk4qcgx_tier_0`, `texndcpda_tier_0` …); der Klartext (`Patch_Ground_Rock_Small`) steht nur im Pfad
(`/Game/Fab/Megascans/3D/Desert_Western_Patch_Ground_Rock_Small_01_uk4qcgx/…`). Die letzte Spalte sind **unsere Vermutungen zu Parameterwerten – bitte
ersetzen** (§8.3 fragt die Werte ohnehin bei euch ab).

| Element (Ziel) | Netze im Projekt | Werkzeug heute | fehlt | Befund / unsere Vermutung – bitte ersetzen |
|---|---|---|---|---|
| Steinbedeckung 0–3 m ≥ 70 %, nackt ≤ 5 % | Bodenplatten: `SM_TundraRockyGround_01` (6,0 × 4,7 × 0,84 m, MI_EL; heute Palette kiesbank Skala 0,22–0,45), `SM_NordicBeachRockyGround_01/_02` (3,4 × 3,3 × 0,77 / 3,5 × 3,4 × 0,25 m), `SM_ErodedRockyGround_01–03` (7,3 × 3,7 × 0,33 m), `SM_RockyForestPath_01` (4,9 × 3,5 × 0,42 m), `SM_NordicBeachRocks_01` (5,8 × 3,6 × 2,5 m Haufen); Fab Desert_Western `Patch_Ground_Rock_Small uk4qcgx` (2,2 × 1,8 × 0,22 m), `Ground_Patch_Rocky ulksbcz` (4,3 × 2,3 × 0,33 m), `Canyon_Sandstone_Rocky_Ground uk5ocf2` (3,2 × 2,1 × 0,22 m) – Sandsteinton, MI-Override nötig; Lagen Geroell/Kies/Fels/Felsplatte | bachdekor_swr (kiesbank 0,06 je m bei ≤ 14°, kiesel_ufer_m2 0,3 bis 3 m, randstein-Saum 0,8–1,4 m außen) + kantenufer_p2 (C4 „gerade“ 3–6 Steine 0,3–0,6 m je 10 m je Seite; gesetzt 2,2 je 10 m) + Lagen über Sehens-Kette | nein | Netze reichen, Dichten nicht (3–5 % gegen 70 %). Rechenprobe: 10 m × 3 m = 30 m²; 70 % = ≈ 20 m² Stein = 2 RockyGround-Platten + 30 Steine 0,3–1 m + 50–100 Kleinsteine. Frage: Reicht kiesel_ufer_m2 0,3 → 3–5, kiesbank 0,06 → 0,3–0,5, Lage Erde im Band ≤ 15 %? (unsere Vermutung) |
| Kleinschutt 0,05–0,3 m 50–100 je 10 m (§0), Lagen offen, Schuttband | `SM_SmallStonesPack_01–14` (0,10–0,19 m, MI_EL auf M_EL_Fels_MS; _01 schon MS2 mit Nasslinie; gerundet), `SM_stone_01–12` (0,04–0,25 m, Mountain, M_Master_material), `SM_namaqualand_stones_01_a–e` (0,08–0,15 m) / `rocks_01_a–d` (0,20–0,23 m) / `boulders_01_a–b` (0,55–0,59 m; grauer Granit, bisher nur Wüste), `Small_Sandstone vd5rfiq` (0,13 m), `Sandstone_Rock wddjfdw` (0,30 m), `SM_NordicBeachRock_01` (0,26 m); Haufen: Desert_Western `Pile_Rock_Small ul4lehiga` (3,2 × 1,9 × 0,33 m) / `ulnfeaw` (1,45 × 1,76 × 0,33 m) / `Pile_Rock_Rough ulcceh3` (1,9 × 1,7 × 0,26 m) – Sandsteinton; `Patch_Ground_Slate_Small venodhb` (2,2 × 1,9 × 0,07 m Schieferstreu); `Rocky_Snow_Pile vcyiccyga/vcytca0fa/xfroec0qx` (3,0–4,7 m, mit Schnee) | bachdekor Klasse kiesel (bett_m2 1,6 nur im Bett, saum_m2 1,5 im Saum, ufer_m2 0,3), kantenufer Rolle kiesel (gleithang 2–4 Packs je 10 m), felsgruppen „kleinmaterial“ (Kontaktsaum 2 m, < 0,5 m) | **ja** | p2 gesetzt 8 509 Kiesel, 7 861 (92 %) unter Wasser; an Land 648 = 7 je 10 m (Messlatte 50–100). Fehlt: (a) graues Schutthaufen-Netz, (b) kantiger Kleinschutt (alle Kiesel gerundet), (c) Stapel-Logik (Abstandsfaktor kiesel/kiesel 0,8 + graben 0,3–0,5 → nie 2 Lagen). Sichtweite kiesel 60 m / 35 m |
| Mittelklasse 0,3–1 m: 25–40 je 10 m, ≥ 70 % kantig, 3 Stufen | `SM_mountain_rock_small_01_1–5` (0,41–0,52 m, Mountain; Hauptpalette, gerundet), `SM_MossyForestRock_01` (0,71 × 0,55 × 0,44 m), `SM_stones_01_1–6` (0,44–1,21 m, Forest, nicht in Palette), `SM_s_rock_01–03` (0,41–0,56 m, Meadow); Fab grau: `Icelandic_Boulder texndcpda` (0,95 × 1,34 × 0,28 m flach), `Icelandic_Rock skjsL` (1,55 × 1,3 × 0,91 m), `Nordic_Forest_Rock_Small xjijbgx` (1,2 × 0,9 × 0,56 m), `Cluster_Rock_Small xjijdiz` (1,94 × 1,69 × 0,41 m), `Forest_Rock wjxqcct` (1,23 × 1,0 × 0,65 m), `Forest_Boulder wgosajs` (1,25 × 0,92 × 0,89 m), `Granite_Rock pjEr1/pjtsT/pkeeM` (1,26–1,51 m); Platten: `Sharp_Sandstone pjcxN` (1,3 × 0,67 × 0,32 m), `Rock_Sandstone rkdau` (1,86 × 0,97 × 0,15 m), `SM_ground_rock_03_01` (2,4 × 1,4 × 0,22 m), `SM_road_stone_01` (2,7 × 1,0 × 0,23 m), `SM_MossyForestRock_03` (1,74 × 0,75 × 0,18 m), `SM_LimestoneRocks2/3` (2,4 × 0,47–0,6 m), `SM_flat_rock_03` (2,0 × 4,05 × 0,47 m), `SM_SmoothRockShelf_01` (3,1 × 2,7 × 0,43 m); kantig: `Basalt_Basalt_Rock_A_SM/_B_SM` (0,81 × 0,86 × 0,67 / 1,17 × 1,52 × 0,78 m), `Basalt_Basalt_Pillar_B_SM…D_SM` (0,29 × 0,26 × 0,74–2,63 m), `Basalt_Basalt_Pillars_Cluster_Low_SM` (1,09 × 0,93 × 0,62 m) – **alle 22 Basalt-Netze Nanite 0** (Budget!); RA `SM_Rock_S_02` (1,5 × 1,6 × 0,4 m), `SM_Rock_M_03` (2,0 × 1,3 × 0,9 m) | bachdekor (bachstein_bett_m2 0,14, geroell 5–9 je Stufe + 3 je m Fall, randstein 4–7 Glieder je 9 m, felsplatte uferplatte_anteil 0,22); kantenufer kopfstein (nur 3 Netze mountain_rock_small_01_1–3; Plan 81, gesetzt 42) | **ja** | p2 gesetzt 2 492 Steine 0,3–1 m auf 895 m = 28 je 10 m, aber 1 979 (79 %) unter Wasser; trocken am Ufer 5,7 je 10 m. Palette = eine Formfamilie; Größenstufen nur Skala 0,55–1,5. Fehlt: graues Schiefer-/Plattenstapel-Netz 0,3–1 m; Icelandic/Nordic/Granite (kantig-grau) sind nicht in der Bach-Palette. Material: mountain_rock_small und Fab-MIs ohne Nasslinie |
| Stapelung/Verzahnung (Kontakt ≥ 60 %, Eingraben ≥ 50 % zu ≥ 1/3, Kipp je Gruppe, Haufen 5–15; §0) | Haufen-Netze: `SM_NordicBeachRocks_01`, `Nordic_Forest_Cluster_Medium xisgcic` (2,2 × 1,6 × 1,1 m), `Nordic_Forest_Cluster_Rock_Medium xf3odif` (2,7 × 2,0 × 0,88 m) / `xfplcbf` (1,9 × 2,0 × 1,0 m), `Basalt_Basalt_Cluster_A_Rocks_SM` (3,4 × 3,2 × 3,1 m), `Basalt_Basalt_Pillars_Cluster_High_SM/_Low_SM` (0,76 × 0,79 × 2,62 / 1,09 × 0,93 × 0,62 m; Nanite 0), Desert_Western `Pile_Rock_*` (1,5–3,2 m), `SM_stones_roots_01–05` (3,1–7,5 m); alle Einzelsteine oben | bachdekor bettgruppen (1 Fels 0,8–1,9 m + 3–6 kleine; 0,06 je m = 1 Gruppe je 17 m, 19 gesetzt, 4,6 Glieder), randfels_gruppe 0,11 (4–7 Glieder, 201 Gruppen); kantenufer Dachziegel-Kipp 10–20° stromauf, Einbettung 0,3–0,55, abstand_min 0,3 m; 6c Lippenblöcke Abstand 0,75 × Größe, 40–60 % eingegraben | **ja (Logik)** | Kein Asset-Problem: Abstandsfaktoren stein/stein 0,85, fels/fels 0,75, kiesel 0,8 (auf r1 + r2) verbieten Berührung; graben 0,25–0,4 der Netzhöhe, Bilder zeigen trotzdem sichtbare Unterkanten → Pivot/Netzmaß prüfen (FORMAT §3: z = Gelände − Eingraben × Netzhöhe). Nötig: Faktor ≤ 0 in Gruppen, „liegt auf Nachbar“ (z = Oberkante), gemeinsamer Kipp je Gruppe, Haufen mit Lücken 1–3 m statt Rate je m. Cluster-Netze liefern Stapel sofort, sind nicht in der Palette |
| Übergang Ufer → Wasser (≥ 3 je 10 m und Ufer im Wasser, Erdkante ≤ 5 %, Nasslinie; §0) | mit Nasslinie umhängbar (MI_EL auf M_EL_Fels_MS → MS2): `SM_SmallStonesPack_*`, `SM_MossyForestBoulder_01–07`, `SM_NordicBoulder_01`, `SM_LichenedForestBoulder_01`, `SM_TundraRockyGround_01`, `SM_MossyForestRock_01–03`. Material `M_EL_Fels_MS2` = MS + `MF_EL_Nasslinie` + `MF_EL_Spiegelhoehe` (gebaut 13.10. 20:3x, +27 Anweisungen, +1 Sampler; Nass_Albedo 0,50, Nass_Entsaettigung 0,3, Nass_Rauheit_Linie 0,2, Nass_Voll_cm 8, Nass_Rand_cm 20). Umgehängt 1 von 121 Instanzen (Sicherung `nasslinie_eltern_sicherung.json`, 120 warten). Sofortlösung `_Nass`-Kopien: `MI_EL_Nass_SmallStonesPack_01` (0,55), `MI_EL_Nass_mountain_rocks_small_01` (0,30, OHNE Nasslinie), `MI_EL_SW_Klammfels_Nass`; 9 840 Steine unter dem SWR-Spiegel umgestellt | `scripts/unreal/ue_fels_nasslinie.py` (lesen/bauen/umhaengen/werte/zurueck; Cloud 6d: Nass_Albedo 0,65 für SmallStonesPack, Ziel Y 0,08, nie doppelt mit _Nass); kantenufer C4 u_m −0,3..+1,0 m (höchstens 0,3 m ins Wasser), stufe_widerlager 1–2; bachdekor randstein/randfels Saum AUSSEN; `hindernisse_filter_p2.py` + WH-Akteur (1 362) | **ja** | Nasslinie für `M_Master_material` (mountain_rock_small/big, flat_rock, ground_rock, stone_01–12) und Fab-MIs (skjsL, texndcpda, Nordic_Forest_Cluster, Granite) fehlt (Cloud 6d: ja, als Kopie wie MS2). Planer-Rolle „Stein mit Fuß im Wasser, Oberkante 15–40 cm über Spiegel“ fehlt. Gesetzt im Wasser ragend ≈ 1–2 je 10 m |
| Blöcke 1–3 m (3–6 je 10 m, 1–3 im Wasser) + Felsinseln | `SM_mountain_rock_big_02_1–8` (2,7–6,4 m; uferfels/prallhang_fuss, Cloud „block“), `SM_mountain_rock_big_01_1–5` (0,92–1,05 m), `SM_MossyForestBoulder_01–07` (0,94–3,3 m, MI_EL), `SM_LichenedForestBoulder_01` (0,85 × 0,63 × 0,46 m), `SM_ground_rock_02` (1,37 × 0,99 × 0,93 m), `Icelandic_Rock skjsL` (Skala bis 1,7 = 2,6 m), `Nordic_Forest_Cluster_Rock_Medium xf3odif/xfplcbf`, `Granite_Rock pkeeM` (1,5 × 1,2 × 1,0 m), `SM_Middle_Rock_01` (1,3 × 1,4 × 1,85 m), `SM_Rock_01–07` (1,25–3,1 m, Meadow), `Basalt_Basalt_Rock_C_SM/_D_SM` (1,31 × 1,19 × 1,67 / 2,10 × 2,29 × 1,36 m, Nanite 0), RA `SM_Rock_M_01/_02` (3,3 / 2,4 m), `SM_Rock_S_01` (3,1 × 2,65 × 0,87 m); `SM_IcelandicBoulder_01–03` (1,4–3,2 m, rötlich – Cloud R3: nur canyon/oedland/wueste/lava) | bachdekor bettgruppen (bettfels/lippenfels/randfels 323 = 3,6 je 10 m), kantenufer uferblock (Plan 10, gesetzt 1), 6c-Bettplan (203 Blöcke auf 190 m = 10,7 je 10 m, eingebaut 6f: 621 Blöcke/Kies, 216 Kollision) | nein | Felsinseln mitten im Lauf: bachdekor-Bettgruppe lässt Oberkante 15 cm über den Spiegel (s_raus), Rate 0,06 je m × Breite/12 → bei 2–4 m Breite 1 Gruppe je 17 m; Ziel 1–2 je 20 m nur mit Faktor 2 |
| Anstehender Fels > 3 m, Steilufer > 35° als Fels, Bettwände ≥ 60 % 3D | Uferwand 1–2 m geschichtet: `SM_beach_escarpment_01_A–C` (8,0–8,6 × 1,6 × 1,0–1,1 m), `_02_A–D` (8,1–11,2 × 2,7–3,0 × 1,8–1,9 m), Coast_Dunes Sandstein-gelb (Cloud „band“); `SM_LS_*` gleich groß. Erdböschung: `SM_scarp_01/_02` (3,1 × 1,15 × 1,24 / 2,8 × 1,2 × 0,54 m), `SM_sandy_slope_01–05` (3,4–7,2 × 1,4–1,8 × 1,2–1,4 m), `SM_MossyEmbankment_01/_02` (5,4 × 2,1 × 0,6 / 4,8 × 1,7 × 0,8 m, MI_EL). Terrasse: `SM_ForestRockShelf_01–03` (5,4–7,1 m × 0,6–1,3 m), `SM_ForestRockSlab_01` (7,2 × 3,5 × 0,66 m), `SM_ForestRockFormation_01–06` (3,3–5,8 m, geschichtet, MI_EL _02–_05), `SM_flat_rock_01` (9,9 × 7,0 × 1,5 m). Wandmodule: `SM_big_rock_wall_01–03` (7,8 × 3,9 × 3,4 / 5,2 × 1,5 × 2,5 / 4,3 × 1,3 × 2,3 m), `SM_mountain_rock_big_02_7/_8`. Klippen: `SM_HugeNordicCoastalCliff_01/_02` (13,8 × 8,5 × 9,1 / 12,2 × 6,2 × 7,1 m, MI_EL_*_tundra), `SM_MassiveNordicCoastalCliff_01` (21 × 15 × 14,7 m), `SM_MassiveTundraRockFormation_01/_02` (77 × 29 × 12 / 29 × 20 × 7 m), `Massive_Layered_Rock_Cliff ukjhcamga` (30 × 9,3 × 10,9 m), `Sharp_Cliff rcygn` (18,8 × 4,6 × 10,9 m); RA `SM_Cliff_M_01_A/B` (8,0 × 29,6 × 7,8–9,7 m), `SM_Cliff_M_02_A–C`, `SM_Cliff_M_03` (6,8 × 39 × 9 m), `SM_Cliff_L_01_A/B` (20,6–22,8 × 41–50 × 35–47 m), `SM_Ridge_Rock_01/_02` (8,6 × 14,5 × 1,5 / 7,8 × 18,6 × 1,8 m flache Rippen), `SM_Ridge_Dirt_01/02` – nicht in Paletten, Material RA | felsschalen (v8 misch, nur Wände über der Hangschwelle; `fertig_C2.json` liegt vor), felsgruppen (Cloud-Planer, Klassen wand/band/prallhang/blockstrom/steilhang; lokal gesetzt nur A5 B4 C6 D3 E1 E4 G4 H3 H5 H6, **kein C2**), klippen_plan (A5/B5), kantenufer uferfels (2 gesetzt, prallhang_fuss ab 1,5 m) | **ja** | Für die Bettwand 0,5–1,5 m setzt kein Werkzeug Netze AUF die Wand: bachdekor felsplatte_wand 0,22 wirkt nur bei wand_grad 30–40° in 9–13 m Abstand; kantenufer kennt nur Steine am Fuß. Nötig: Rolle „Wandverkleidung“ (Escarpment/Scarp/Embankment, Normale = Wandnormale, 40–60 % eingegraben, Kette entlang s). Coast-Escarpments brauchen MI-Override (grau, Flechten) wie `MI_EL_HugeNordicCoastalCliff_01_tundra`; graues Uferwand-Netz 0,5–1,5 m × 3–6 m fehlt |
| Lesbarkeit in der Tiefe + Felsrippen am Talhang | `SM_Ridge_Rock_01/_02` (RA), `SM_ForestRockFormation_05/_06` (5,6–5,8 × 4,2 × 0,65 m), `SM_MassiveTundraRockFormation_02`, `SM_big_rock_wall_02/_03`, `SM_mountain_rock_big_02_3` (6,4 × 3,6 × 1,9 m) – Cloud „band“ tundra | felsgruppen (Formgruppen 10–30 m, 8–20 je Feld; `cloud_setzen_feld.sh felsgruppen <Feld>`; kein Plan für C2); Sichtweiten bachdekor (kiesel 60, bachstein 180, geroell 150, randstein 250, bettfels 500, lippen-/randfels 600, felsplatte 450 m), kantenufer (kiesel 35, moos 60, ufergras 90, kopfstein 90, uferblock 450, uferfels 600 m) | nein | Werkzeug da, auf C2 nicht angewandt. kopfstein 90 m / kiesel 35 m sind für Lesbarkeit aus 30 m knapp (Nanite: Sichtweite kostet kaum). Rippen: Klasse band/grat auf dem C2-Talhang rechnen (Hangknick-Regel R3 – das Bachtal hat Knicke) |
| Füller zwischen Pflanzen (Erde ≤ 15 %) | Lagen Geroell/Kies/Fels/Felsplatte/Moos/Trockengras/Heide (ufer_lagen_p2 boeschung_locker Geroell 25/Moos 25/Trockengras 20/Erde 15/Kies 15; boeschung_steil Erde 30/Moos 30/Geroell 25; ufer_feucht tundra Moos 90/Erde 60/Kies 55/Heide 30/Geroell 20); Gras 20 Arten (`GT_Heide`, `GT_Gras_Berg`, `GT_Gras_Duerr`, `GT_Steinchen`, `GT_Kraut`, `GT_Farn`, `GT_Wiese_Kurz`); Moos `SM_moss_01/_02` (0,49 × 0,43 × 0,03 / 0,58 × 0,41 × 0,02 m), `SM_CustomMoss_01–05` (0,10–0,17 m), `SM_MossClump_01/03/05`; Grasfilz `SM_GrassyEmbankment_01/_02`, `Tundra_Grass wk2oaeyqx VarA–I` (0,34–0,96 m), `SM_grass_bush_01–04` (0,66–1,3 m) | Sehens-Kette Lagen (altbett_p2c / kantenufer_p2_lagen / bettlagen_p2), Gras-Karten, bachdekor moos_ufer_m2 0,8 (Breite 1,8 m), insel_m2 0,06, kantenufer moos 1 037 (55 je 10 m) | nein | 40–50 % Ockerboden. Erde-Anteil 15–30 % in den Lagen ist nicht die Hauptursache: der Stein als Füller fehlt; V18 zeichnet Erde hell (Entsaettigung_Nass 0,5 nur nass). Frage: Reicht Erde ≤ 10, Geroell/Kies +15, GT_Heide/GT_Gras_Berg im 1–10-m-Band, moos_ufer_m2 0,8 → 2? (unsere Vermutung) |
| Pflanzen in Ritzen (≥ 80 % ≤ 0,3 m am Stein) | Büschel/Farne unten, Steine oben | bachdekor fels_begleiter 2–4, aber Abstandsfaktoren pflanze/fels 0,9, pflanze/stein 0,9, moos/fels 0,6 (Pflanzen HALTEN Abstand); kantenufer ufergras nur Schulterlinie, Überdeckungstest 85 % entfernt Pflanzen in Felsnähe (37) | **ja (Logik)** | Ritzen-Logik fehlt in allen Planern. Nötig: Rolle „ritze“ = Pflanze am Kontaktpunkt zweier Steine oder am Steinfuß (0–0,3 m, Faktor ≤ 0,1), NACH dem Steinsatz; heute Reihenfolge Pflanzen vor Steinen (moos, gras, kraut, blume, farn … vor kiesel/bachstein) |
| Farne (2–3 je 10 m Gleitufer, in Blocklücken) | `SM_SilverLadyFern_01–03` (1,28 × 1,26 × 0,62 / 1,34 × 1,09 × 0,59 / 1,04 × 0,75 × 0,46 m; Skala 0,65–1,1), `SM_Fern_01–06` (1,4–2,0 × 0,65–1,04 m; C.3 nennt _01/_02/_04), `SM_BeechFern_04/05/09/10/15` (0,3–0,5 m, MI_EL an M_EL_Fels_MS), `SM_foliage_fern_01_1–4` (0,7–1,1 m), `SM_fern_01_0–2` (0,6–1,0 m), `SM_EagleFern_S_01/_02/_04` (0,90 × 1,07 × 0,55 / 0,58 × 0,85 × 0,56 / 0,54 × 0,73 × 0,42 m) + `SM_EagleFern_M_01` (1,26 × 1,59 × 0,97 m; Hivemind Medieval_Docks, Nanite 1, Foliage-Typen FT_EL_WIT_/MITT_ vorhanden – die C.3-Netze sind also da) | bachdekor farn nur in Inseln (insel_m2 0,06, farn 1,0 je m², Anteil nass 0,1 / mitte 0,2, e_min 0,35 m; 633 im Plan = 7 je 10 m, in den Bildern 0 sichtbar → prüfen: bett_freihalten/Nass-Filter oder 0,3-m-BeechFern gehen unter); Cloud 6e +65 Farne (Nordufer); kantenufer: „Farne werden nicht gesetzt“ | **ja (Regel)** | Netze reichen (8 Arten 0,3–2 m). Fehlt die Platzierungsregel „Lücke zwischen Blöcken ≥ 0,5 m, 1–3 m vom Wasser“ (C.3: Gruppen 2–5, Abstand 4–8 m, offene Tundra max 1 je 15 m – sparsam gegenüber der Messlatte 2–3 je 10 m Gleitufer, §0) |
| Teppich → Inseln (Heide ≤ 30 %) | GT_Heide/GT_Gras_Berg/GT_Blumen_Kalt (aus Lagen); `SM_heath_A_01/B_01`, `SM_forest_heather_01` (0,55 × 0,48 × 0,52 m), `SM_lingonberry_01/02`, `SM_billberry_01/02`; Blumen `SM_WhiteWindflower_01/02/05`, `SM_Crownbeard_03/04/07`, `SM_flower_chamomile_01`, `SM_kidney_vetch_01` | Cloud-Ebene heide_tundra, wit_plan Abschnitt 5 Blumeninseln (Zellen 26 m), bachdekor blumen_insel 0,04 (6–12 Glieder), insel_m2 0,06 (Radius 0,8–2,2 m), Lagen Heide (ufer_feucht 30) + Gras-Karten | nein | Teppich kommt aus dem Landschaftsgras der Hangdecke, nicht aus den Bach-Planern. Frage: Heide-Lage über Fleck-Rauschen (wie kies_fleck Skala 5 m / Schwelle 0,52–0,68) auf ≈ 30 % begrenzen – richtig? (unsere Vermutung; Dichte/Gewicht je m² siehe §6 offene Zahlen) |
| Moos/Flechte-Flecken auf Felsoberseiten | `M_EL_Fels_Auflage` (`ue_fels_auflage.py`): von oben projiziert, Maske < ≈ 45°, Mulden, Auflage_Flecken 0,5; tundra Moos `T_ground_moss_01`, Menge 0,35, Schwelle 0,72; Instanzen `MI_EL_Auf_<Netz>_<biom>` nur für Felsschalen-Netze; Vollkappen-Netze `SM_MossyForestRock_01`, `SM_LichenedForestBoulder_01`, `SM_TundraMossyBoulder_01`, `SM_MossyForestBoulder_*`; Polster `SM_MossClump_01/03/05`, `SM_moss_01/_02`, `SM_CustomMoss_01–05` | ue_fels_auflage.py, bachdekor bachstein_moos/bettfels_moos (nur trockene Oberseite), kantenufer moospolster (ab h 0,25 m, 60 % der Steine, 0,33–0,67 je m, Nordseite ×2) | **ja** | Fehlt: (a) `MI_EL_Auf_*_tundra` für die Bach-Steinnetze (Mountain/Fab brauchen Kopie des Auflage-Masters mit deren Texturen), (b) Höhenregel 0 % unter 1 m über Spiegel (`MF_EL_Spiegelhoehe` gebaut, Knoten „Auflage × smoothstep(100, 150 cm, z − Spiegel)“ fehlt), (c) Flechten-Textur (nur Moos/Schnee/Sand) |
| Ufergehölz (Gruppe 3–6 Bäume je 50 m, Fuß 2–6 m auf Schulter/Fels) | Kiefern `SM_Forest_pine_01–09` (16,4–28,6 m), `_10_dead` (24,9 m), `SM_Forest_pine_tree_00_A–D` (4,8–12,3 m), `SM_Forest_pine_plant_00–05` (1,1–4,1 m); `SM_pine_beach_01–04_A` (5,3–10,3 m), `SM_pine_beach_crooked_01/_02` (4,45 × 5,37 × 3,36 / 2,10 × 1,77 × 1,72 m, Nanite 0); Birke `Big_Tree_Birch_01` (11,5 m, Blatt-Tint), Weiden `Big_Tree_Willow_01/_02` (16–21 m); Wurzeln `SM_Pine_roots_01–06` (Mountain; _01 5,09 × 1,57 × 1,64, _03 2,99 × 0,87 × 1,01, _04 1,97 × 1,36 × 0,82 m; _04–_06 Nanite 0 – die C.3-Netze `SM_Pine_roots_03/04` sind da) + Coast `SM_pine_roots_01` (2,83 × 3,35 × 3,23 m, Nanite 0), `SM_roots_01–05` (1,4–4,5 m), `SM_stones_roots_01–05`, `SM_ForestRoots_01/_02`, `SM_MossyForestRoots_01–03`, `SM_crooked_root_01–05`; **Erle: keine** | wit_plan Abschnitt 4 Ufergehölz (Zellen 22 m, 2–14 m vom Wasser, Hang ≤ 28°, Treffer 45 %, Weide + Büsche; auf C2 ohne Wirkung: 0 Bäume ≤ 20 m), Cloud C.3 wurzeln (nur Erdanriss am Prallhang), bett_freihalten.py | **ja (Regel)** | Bäume vorhanden (Kiefern wie Referenz), Erle fehlt. Fehlt die Regel „Gehölzgruppe auf Schulter/Felsnase am Bach, Fuß von ≥ 2 Steinen umgeben“ (wit_plan nur Hang ≤ 28°; Talkaskade liegt in 25–30°). Stammfuß-Höhe aus `lauf_p2.json`/Querschnitten |
| Büsche/Kraut oben (1–3 je 10 m) | `SM_grey_willow_01–04` (0,57 × 0,72 × 0,82 bis 1,67 × 1,78 × 1,23 m; Palette strauch), `SM_dwarf_pine_small_01–04` (0,9–1,2 m) / `medium_01–06` (1,7–2,0 m), `SM_maple_bush_01–04` (0,8–1,8 m), Heide/Beeren oben; Megaplant `Branch_Goat_Willow_*` (0,8–1,1 m), `Branch_Common_Hazel_*` (0,6–1,0 m), `Branch_Beach_Rose_*` (0,9–1,0 m) – 122 Netze ohne Foliage-Typen, ungeprüft | bachdekor strauch_gruppe 0,06 (1–3 Glieder; 70 auf 895 m = 0,8 je 10 m), kraut-Inseln; kantenufer kraut_blumen (nur Hinweis) | nein | Frage: strauch_gruppe 0,06 → 0,15 je m und Bindung an Stein/Baumfuß (Ritzen-Logik)? (unsere Vermutung, Wert bitte setzen) |
| Trockene Alt-Halme (30–50 %) | `SM_dead_grass_01–03` (2,0 × 2,3 × 0,16 / 2,0 × 2,0 × 0,17 / 1,0 × 0,8 × 0,19 m; flache Streu), `GT_Gras_Duerr`, Lage Trockengras (10–20 %), Megaplant `Branch_*_Dead` / `Twig_*_Dead` (0,3–2,9 m); Tint-Muster `ue_blatt_tint.py` | Palette gras (8 Netze, 0 trockene) / kantenufer ufergras (6 Netze, 0 trockene) | nein | Kleine Wirkung: Trockengras-Lage im Uferband anheben + MI-Kopie der Büschel mit braunem Tint (50 % der Gewichte; nie unter gleichem Namen) |
| Maßstabs-/Platzierungsfehler | Halm: GT_* an der Prüfkamera oder `Tundra_Grass VarB/VarG` (0,63–0,73 m, Skala 1,3 = 0,95 m) – laut 6f die Kamera im Gras; weiße Form: `SM_DeadLeaves_12–14` (0,8–1,7 m flach), `SM_half_log` (1,5 × 0,12 m), `SM_detail_leaves_01` – ungeprüft | bett_freihalten.py (107), bachdekor_freihalten.py, hang_max_grad_pflanzen 50, Kamera-Regel bachdekor kameras (6–11 m vom Ziel, frei von Felsen) | nein | Frage: Kamera-Regel „keine Gras-Instanz < 0,5 m“ und Grasnetze im Band 0–3 m ≤ 0,6 m (Palette ohne `SM_grass_02_A_1` Skala 0,9–1,4, Tundra_Grass ≤ 1,0) – als Prüfregel bestätigen? (unsere Vermutung); Form im Editor lesen |
| Totholz/Äste | Stämme `SM_dead_log_01–05` (0,25–1,74 m), `SM_OldFallenTree_01/_02`, `SM_LargeFallenTree_01`, `SM_beach_driftwood_01`, `SM_Forest_Pine_09_log` (5,6 m), `SM_FallenSpruceTree_01` (7,3 m), RA `SM_Log_S_01/02` (5,5 / 5,0 m), `SM_Log_M_01` (8,6 m), `SM_Log_L_01` (17,7 m); Äste `SM_OldTreeBranch_01–06` (1,0–6,9 m), `SM_Pine_broken_branch_01/02`, `SM_mountain_branch_01_01/02`, `SM_BrokenTreeBranch_01`, `SM_branch_01_1/2`; Zweige `SM_DryBranches_01–08` (0,3–0,5 m), `SM_WoodenSticksAndTwigs_01–10` (0,06–0,13 m), `SM_detail_branches_01–03` (1,7–3,6 m); Nasslinie Vorlage „holz“ (33 Instanzen an M_EL_Fels_MS) | bachdekor stamm 0,065 (60, 55 % im Wasser), steg (6), ast 0,32 (295), zweig_gruppe 0,12 × 3–7 (575), Verklausungen 3 | nein | Dichte schon über dem Ziel (ast 3,3 / zweig 6,4 je 10 m); Referenz zeigt kaum Totholz. Nur Bindung an Steinlücken fehlt |
| Wasser: Mikrokontrast / Wellen | `MI_EL_SWR_Klar` (Kind von MI_Eldarien_Wasser_Fluss ← _Basis ← Master `M_Eldarien_Wasser_Schaum8`): Sim Velocity Normal Strength 5 (E16), Fluidsim Normal Strength 1, River Normal Flatness 0,5, WPO Flowmap 6, Far Normal Fresnel Power 9, ELD_Wirbel_Normal/_Staerke 0, ELD_Schaum_Normal 0 (S6), ELD_Normal_Nah (V20a 0,35 geplant); Vergleich Coast `M_River_Water_Vertex_Offset` (Enable River aus / Waves an, Sim Velocity Normal 40), RA `M_Water_01` (am Bach unsichtbar), NatureWaterFX `M_WaterSurface/M_WaterSoft/M_WaterSharp` (ungeprüft) | `swr/wasser_diag.py` (D0 Da Db Dc Dac Dd De W1 W2 W3 W12 W123 W1R; erledigt D0 + Da), `swr/wasser_varianten.py`, `ue_swr_material.py`, `basecolor_messen.py` | **ja** | Im Master fehlt „Normalen nach Tempo“ (Antwort 18 §3.1: Becken glatt, Rinnen kräftig) und eine Kräusel-Normale 5–15 cm; heute Schlieren 30–60 cm aus der Flowmap-Kette. Cloud 6d: E16 bleibt, V20a bauen |
| Wasser: Farbe/Klarheit | Material F: Absorption 222/1000/1250, Streuung (0,5; 1; 1) × 0,02, Rauheit 0,025 (E16), Schaum 0 (Rückweg A0); Grund V18 `Ufer_Farbe_Bach` 0,20/0,14/0,09, `Ufer_Staerke_Bach` 1,0 (S6), `Entsaettigung_Nass` 0,5; Bachgewicht `T_Eldarien_Bachgewicht_2m`; Lagen bett_lagen_p2; Steine unter Wasser Ziel Y 0,08 (Cloud 6d) | s6_speichern.py, wasser_varianten.py, landschaft_wert.py, basecolor_auswerten.py (unter Wasser Y 0,067, nasses Band 0,063, trockener Kies 0,129), nass_typen.py | nein | Braun-Gold kam aus dem Grund (T0) und ist mit S6 weitgehend weg. Für Olivgrau: Grund grau (Kies/Geröll statt Schlamm 80 in bett_becken), Steine Y 0,08, Absorption Richtung 16a (Variante B) prüfen |
| Wasser: Schaum/Gischt | Master SimFoam-Zweig: SimFoam Contrast 2,0, Foam Opacity (KLAR 0,9, F 0), Foam Boost 0,8, Foam powr 0,6, Foam Texture Blend Min 0,6, Sim Foam Scale 700; eigene `ELD_Fels_Schaum`, `ELD_DF_Schaum` (Distance-Field-Saum um Netze = Kragen-Kandidat), `ELD_Ufer_Schaum`, `ELD_Schaum_Zug/_Tempo/_Groesse/_Schwelle/_Kontrast/_Farbe/_Rauheit/_Deckkraft/_Normal`, `ELD_Strom_Schaum` (0); Epic SWR FoamAttenMin/Max, LowVelocityFoamScale, Render State „Debug Foam“; Hindernisse WH (1 362 Teile); Niagara-Gischt NatureWaterFX (116 Niagara), Gischt an WF_K1/K8; Schaumflächen-Netze `SM_SF_F_ERLENBACH_1V_C2_*` (16g SLW2, wartend) | ue_swr_material.py schaum, _strom_schaum_aus.py, hindernisse_filter_p2.py + WH, swr_bake; `M_EL_Wasserfall3` (163) | **ja** | Schaum heute 0 (F). Master hat KEIN FoamAtten/Velocity-Scattering (16f §3.2/§4 nicht umsetzbar); SimFoam-Kanal der gebackenen SWR ist da, Kragen je Stein (Anströmseite) und Schürze je Lippe ungeprüft – `ELD_DF_Schaum` einziger Kragen-Kandidat, Wirkung ungetestet. Niagara-Gischt je Hindernis fehlt als Werkzeug |
| Wasser: Grund/Tiefe lesbar | Lagen bett_becken (Kies 90 / Sand 60 / Schlamm 80 / Algen 25), bett_rau (Geroell 130 / Kies 80 / Fels 35 / Felsplatte 10), bett_kies, bett_sand; Steine unter Wasser `_Nass` (9 840); Cloud 6c Kies im Kolk 331 | bachdekor kiesel_bett_m2 1,6 (× 2,2 Stufe, +0,6 Schnelle, −55 % Becken, ab 1 m −40 %), bachstein_bett_m2 0,14 (× 3,5 Stufe, × 2,5 Schnelle, −60 % Becken), bett_lagen_p2.py, swr_dump.py | nein | Beckenböden durch becken_minus 0,55/0,6 und Schlamm 80 bewusst leer; Frage: Braucht die Messlatte 30 % Stein becken_minus → 0,2 und Schlamm → 30? (unsere Vermutung, Werte bitte setzen) |
| Wasser: Schlieren / Strömung / Spiegelung | MI_EL_SWR_Klar Normalen-Parameter oben; Lumen-Spiegelung (Diagnose D/W/N: Milchiges = Lumen über hellem Grund, S6 behoben); Coast-Vergleich Enable River aus / Waves an | wasser_diag.py (Rest Db..W1R offen), swr_dump.py + swr_dump_lesen.py (Tempo-Richtung), ue_swr_material.py varianten (V3/V4) | **ja** | Diagnose da, Lösung nicht: „Normalen nach Tempo“ und gerichteter Glanz entlang der Fließrichtung fehlen im Master; Schlieren = Flowmap-Normalen × steile Uferwand (Ableitung). Flachere Ufer (32°) helfen teils |
| Grasnarbe an der Kante | kantenufer ufergras `SM_grass_bush_01–04`, `SM_GrassyEmbankment_01/_02` (204 gesetzt, Fuß Schulterhöhe, Überhang 0,15–0,35 m, 60–80 % der Kantenlänge laut C.3 – **widerspricht der Referenz**); Landschaftsgras bis an die Kante | kantenufer (ueberhaengendes_gras 0,6–0,8), bett_freihalten.py (Maske `maske_swr_wasser.r8`), bachdekor wasser_saum_m 1,5 / frei.wasserlinie 0,3 m, Gras-Lagen im 0–1-m-Band | nein | Regelwerte sind das Gegenteil des Referenzbildes (16h-N3 wollte Gras über die Kante). **Entscheidung an die Cloud:** Referenz zeigt 0–1 m nackten nassen Stein |
| Bettform / Uferlinie / Wände (Frage ≤ 45°) | Cloud-Bettplan 6c (`antworten/p2_bett/bettplan_p2.json` + talkaskade_*.png/.f32/.u8; Regeln/Skripte in `antworten/skripte/p2_bett/p2_bett_regeln.json`, `p2_bett_welt.py`): 25 Einheiten, 46 Lippen schräg (Median 22°), Abstände 1,8–11 m (CV 0,54), Fälle 0,5–2,5 m, Blockkaskaden, Buchten, Eckblöcke, Uferstufe 0,2–0,5 m; 6e +279 Kantengras / 432 Moos / 65 Farne / 5 Totholz; Kurven `C_EL_Bach_KastenU/_FlachU`, Falloff 32° / 25°, Blend Min; kasten_verbot, zuruecklegen_16h2 (32/38°) | `scripts/swr/p2_bett_einbau.py` (Adapter, 6f), Sehens-Kette, kurven_anlegen.py, brush_*, teilc_zuruecklegen_p2.py, kasten_statistik_p2.py, frisch_reset.py + swr_bake; Rückbau einbau_rueckbau.py Pflicht | nein | **Eingebaut (6f)**: Gelände, 621 Blöcke, Spline-Z, Bake. Danach müssen bachdekor_swr, kantenufer_p2 und Lagen neu gerechnet werden (Reihenfolge-Falle Feldhöhen) – die P2C-Bilder zeigen den Stand VOR dieser Neurechnung |
| Großblock-Maßstab (Begleitsteine) | Begleiter `SM_mountain_rock_small_01_1–5`, `SM_MossyForestRock_01`, Fab `xjijbgx`, `wjxqcct`; Kleinschutt oben | bachdekor bettgruppen (1 groß + 3–6 klein), fels_begleiter 2–4, randfels_gruppe_glieder 4–7 mit randfels_gross_anteil 0,75–0,9 (= 75–90 % GROSSE Stücke je Gruppe – umgekehrt zur Referenz 1:3–10), felsgruppen kleinmaterial (Saum 2 m, < 0,5 m) | nein | Frage: Regelwerte drehen – randfels_gross_anteil 0,75–0,9 → 0,15–0,25, Glieder 4–7 → 6–12, Kleinschutt-Saum 1–2 m um jeden Fels? (unsere Vermutung; das Potenzgesetz × 3 je Klasse abwärts wie felsgruppen „steilhang“ ist Ableitung, §4) |
| Staffelung / Blickziel | Bäume/Felsnasen oben | Prüfkameras bachdekor kameras (6 je Lauf), sehens_kameras.py, `swr/_kam_*.json`; Dunst W7 nicht Thema | nein | Folgt aus Ufergehölz + Felsrippen; Blickziel-Prüfung als Kamera-Regel (Ziel in 20–60 m entlang der Achse) ergänzbar |

## 6. Heutige Dichten (Stand 13.10., Lauf p2 = HAUPT 788,2 m + Arm 106,7 m = 895 m; nasse Fläche 2 421 m², Band 3 885 m²; 21 448 Instanzen)

**Stand:** Alle Zahlen hier sind der Planer-Stand VOR der Neurechnung nach 6f (bachdekor_swr, kantenufer_p2, Lagen noch nicht neu gerechnet; nur Gelände +
6c-Blöcke sind nach 6f). Die P2C-Bilder zeigen genau diesen Zwischenstand – bitte nicht als Endstand kalibrieren.

- **Kiesel < 0,25 m:** kiesel_bett_m2 1,6 (× 2,2 Stufen, +0,6 Schnellen, × 1,5 Rand, −55 % Becken, Fleck 3,5 m); saum_m2 1,5 (Saum 0,8–1,4 m außen); ufer_m2 0,3 (bis 3 m);
  aue_m2 0,7; ab 1 m Tiefe −40 %. Gesetzt 8 509 = 95 je 10 m, davon 7 861 (92 %) unter Wasser = 3,2 je m² nass; **an Land 648 = 7,2 je 10 m**.
- **Bachsteine 0,3–1 m:** bachstein_bett_m2 0,14 (× 3,5 Stufe, × 2,5 Schnelle, −60 % Becken, +30 % größer in Gumpen, ab 1 m −30 %); saum 0,05; aue 0,04. Gesetzt
  bachstein 839 + geroell 860 + randstein 793 = 2 492 = 27,8 je 10 m, davon 1 979 (79 %) unter Wasser; **trocken am Ufer 513 = 5,7 je 10 m**.
- **Bettgruppen** (1 Fels 0,8–1,9 m + 3–6 Steine): 0,06 je m × (nasse Breite/12, 1–3) → bei 2–4 m 1 Gruppe je ≈ 17 m; 19 Gruppen, 4,6 Glieder; Lippenabstand 1,5 m.
- **Geröll an Stufen:** 5–9 je Stufe + 3 je m Fall, Flanken 1–3; 76 Stufen → 860.
- **Randfelsen:** 0,11 je m (× 2 an Wänden), 4–7 Glieder, gross_anteil 0,75–0,9; randfels 167 + lippenfels 137 + bettfels 19 = 323 = 3,6 je 10 m.
- **Platten/Kiesbänke:** uferplatte_anteil 0,22; felsplatte_wand 0,22 (nur 30–40°, 9–13 m vom Lauf); kiesbank 0,06 (≤ 14°); gesetzt felsplatte 58 (0,65 je 10 m), kiesbank 27 (0,3 je 10 m).
- **Totholz:** stamm 0,065 (55 % im Wasser) → 60; steg alle 25 m → 6; ast 0,32 → 295 (3,3 je 10 m); zweig_gruppe 0,12 × 3–7 → 575 (6,4 je 10 m); wurzel 0.
- **Bewuchs Bach-Planer:** moos_ufer_m2 0,8 (Breite 1,8 m) → 4 145 (46 je 10 m); insel_m2 0,06 (Radius 0,8–2,2 m; je m² moos 4 / gras 2,5 / kraut 2,5 / farn 1 / blume 3 /
  schilf 3) → gras 1 678 (19), kraut 1 816 (20), farn 633 (7,1), blume 451 (5); strauch_gruppe 0,06 × 1–3 → 70 (0,8); blumen_insel 0,04 × 6–12; schilf_m2 0,8 → 310;
  wand_pflanzen_m2 0,1; fels_begleiter 2–4.
- **Eingraben** (Anteil Netzhöhe): kiesel 0,3–0,5; bachstein/geroell/randstein 0,25–0,4; bettfels/randfels 0,25–0,4; lippenfels 0,3–0,45; felsplatte 0,4–0,6; kiesbank 0,55–0,8;
  stamm 0,1–0,3; Pflanzen 1–5 cm, Strauch 5–12 cm.
- **Abstandsfaktoren** (auf r_neu + r_alt; 0 = Überlappen erlaubt): stein/stein 0,85, stein/fels 0,8, fels/fels 0,75, kiesel/kiesel 0,8, kiesel/stein 0,85, pflanze/fels 0,9,
  pflanze/stein 0,9, moos/fels 0,6, moos/stein 0,7, kiesbank/stein 0,3 → **Berührung ausgeschlossen, 0 Lagen**.
- **Sichtweiten bachdekor (cm;** Quelle `scripts/bachdekor/bachdekor_swr_regeln.json`, je Klasse `klassen/<Klasse>/sichtweite [0, …]`; die Basisdatei
  `bachdekor_regeln.json` hat denselben Schlüssel mit älteren Werten, z. B. bachstein 15 000, ohne geroell/bettfels/kiesbank**):** kiesel 6 000, bachstein 18 000,
  geroell 15 000, randstein 25 000, bettfels 50 000, lippen-/randfels 60 000, felsplatte 45 000, kiesbank 12 000, stamm 50 000, ast 12 000, zweig 4 500, moos 5 000,
  farn 9 000, gras/kraut 7 000, blume 6 000, strauch 30 000; Budget 45 000 Instanzen, 3 000 Kollision je Feld (C2 170, D2 122).
- **Kantenufer p2** (16h-N3 C.4, Talkaskade s 392–575 ≈ 190 m, beide Ufer): „gerade“ 3–6 Steine 0,3–0,6 m je 10 m je Seite (u −0,3..+1,0 m, Einbettung 0,3–0,5); prallhang_fuss
  0,6–1,4 m, Gruppen 2–4, Abstand 1,5–3 m, Lücke 3–6 m; stufe_widerlager 1–2 je Lippenende + Kolkrand 1–3 Steine 0,5–1 m; gleithang 2–4 Kiespacks je 10 m; moospolster 0,33–0,67
  je m, 60 % der Steine ab h 0,25 m; ueberhaengendes_gras 60–80 % der Kantenlänge; farne Gruppen 2–5, Abstand 4–8 m, offene Tundra max 1 je 15 m.
  **Gesetzt 13.10. 15:39:** Plan 1 730 → 1 592 (weg: überdeckt Fels 37, Pflanze im Wasser 38, überdeckt Stein 32, vergraben 20, Lippenzone 9, doppelt 2): kopfstein 42 (Plan 81)
  = 2,2 je 10 m, uferblock 1 (Plan 10), uferfels 2, kiesel 306 = 16 je 10 m, moos 1 037 = 55 je 10 m, ufergras 204 = 11 je 10 m; Kollision 3.
- **Cloud-Bettplan 6c** (eingebaut 6f, ≈ 190 m): Lippenblöcke 112 (0,5–1,2 m, Abstand 0,75 × Größe, 40–60 % eingegraben), Eckblöcke 58 (0,9–1,8 m), Randblöcke 28, Beckenblöcke 5
  = 203 = 10,7 je 10 m; Kies im Kolk 331; Kollision 216; SWR-Hindernisse 5; 6e: 279 Kantengras, 432 Moos, 65 Farne (Nordufer), 5 Totholz.
- **Felsgruppen** (Cloud-Ebene, Erwartung je Bergfeld, für C2 nicht gerechnet): grat 80–250, band 200–600, wand 20–80, fuss 300–900, blockstrom 40–150, kuppe 5–25 Gruppen;
  Instanzen hero 60–300, block 600–2 000, stein 3 000–9 000, kiesel 10 000–35 000; kleinmaterial nur im Kontaktsaum 2 m.
- **Bild-Ist (Sichtschätzung, 5 Kameras):** 3D-Stein im 0–3-m-Band 3–5 %, Steine 0,3–1 m sichtbar 8–14 je 10 m, Blöcke 1–3 m 0,5–1 je 10 m, Steine mit Fuß im Wasser 1–2 je 10 m,
  Kleinschutt am Ufer 0, Farne 0, Bäume ≤ 20 m 0, nackter Boden 30–50 %. Die Lücke zwischen „gesetzt“ (28 Steine je 10 m) und „gesehen“ (8–14): **ungeprüft** – die frühere
  Erklärung (79 % unter Wasser, kurze Sichtweiten, Perlenkette) ist nur eine Vermutung. Wahrscheinlichste Ursache ist die Geländeänderung 6f: der Kontaktbogen „MSR vorher“
  (`bilder/swr_p2/fels_master_repariert_msr.jpg`, Stand vor 6f) zeigt im Bett t500 ≈ 15–20 kleine Steine, P2C an derselben Stelle ≈ 12 + die 6c-Großblöcke → alte
  Bachdekor-Steine wurden beim Bettumbau vergraben oder entfernt; die Neurechnung nach 6f muss das klären.
- **Fehlende Zahlen (nachzuliefern, bevor die Cloud kalibriert):** (a) alle Dichten oben gelten für 895 m – für die Talkaskade s 392–575 (≈ 190 m) fehlt die Zählung je 10 m
  und je Größenklasse aus den Plänen (bachdekor + 6c 203 Blöcke + kantenufer 1 592), getrennt nass/trocken und für das Band 0–3 m; (b) Landschaftsgras: der Heide-Teppich kommt
  aus den GT_*-Grasarten (§5 Teppich), aber Dichte/Gewicht je m² und die tatsächlichen Lagen-Anteile Erde/Heide/Moos im Band 1–10 m aus altbett_p2c/kantenufer_p2_lagen
  fehlen – Zahlen statt „40–50 % Ockerboden“ aus dem Bild; (c) Nanite-Status der Paletten-Kandidaten fürs Budget (netze.csv): alle 22 Basalt-Netze 0,
  `SM_beach_escarpment_02_A–D` 0 (`_01_A–C` 1), `SM_Forest_pine_01–10` 0, `SM_pine_beach_crooked_01/_02` 0, `SM_Pine_roots_04–06` 0; Fab-MIs (skjsL, texndcpda, xjijbgx,
  wjxqcct, pjcxN, rkdau), TundraRockyGround, NordicBeachRockyGround, SmallStonesPack, mountain_rock_small, MossyForestBoulder, IcelandicBoulder = 1.

## 7. Was im Inventar fehlt (für d)

1. Graues Schutthaufen-/Scree-Netz 1–3 m mit ≥ 20 Stücken 0,05–0,3 m (vorhanden nur Desert_Western-Piles in Sandsteinton, Schnee-Piles, `SM_NordicBeachRocks_01` 5,8 m zu groß).
2. Kantiger Schiefer-/Plattenstapel 0,3–1 m grau, 2–3 Lagen mit gleicher Fallrichtung (nur Einzelplatten: texndcpda 0,95 m, pjcxN 1,3 m, rkdau 1,86 m, ground_rock_03_01 2,4 m,
   MossyForestRock_03 1,74 m; Slate-Streu venodhb 0,07 m hoch).
3. Kantiger Kleinschutt 0,05–0,3 m grau als Streu-Netz (SmallStonesPack und stone_01–12 sind gerundet; Namaqualand-Granit grau, nur Wüste eingeplant).
4. Anstehende graue Uferwand 0,5–1,5 m hoch, 3–6 m lang, geschichtet (Coast-Escarpments 1,0–1,9 m hoch / 8–11 m lang Sandstein-gelb → MI-Override; scarp/sandy_slope = Erde;
   MossyEmbankment 0,6–0,8 m bemoost).
5. Erle als Ufergehölz (keine; Kiefern 5–29 m, Birke 11,5 m, Weiden 16–21 m da).
6. Nasslinie-Material für `M_Master_material` (Mountain) und die Fab-MIs (Icelandic, Nordic_Forest_Cluster, Granite, Forest_Rock) – heute nur `M_EL_Fels_MS2`; Umhängen der 120
   wartenden MI_EL_*-Instanzen (1 von 121 erledigt).
7. Moos-/Flechten-Auflage `MI_EL_Auf_*_tundra` für die Bach-Steinnetze + Höhenregel 0 % unter 1 m über Spiegel; Flechten-Textur.
8. SWR-Schaum: FoamAtten/Velocity-Scattering im Master; Kragen an angeströmten Steinen, Schürze je Lippe (`ELD_DF_Schaum` ungetestet); Niagara-Gischt je Hindernis.
9. Wasser-Normalen nach Tempo + Kräuselung 5–15 cm (Antwort 18 §3.1); V20a `ELD_Normal_Nah` 0,35 nicht gebaut.
10. Grasbüschel-Variante mit braunen Alt-Halmen 0,2–0,4 m (als MI-Kopie mit Tint lösbar).
11. Planer-Logik (kein Asset): Stapel/Kontakt (Faktor ≤ 0, z auf Nachbar-Oberkante, Kipp je Gruppe), Haufen 5–15 mit Lücken 1–3 m statt Rate je m, Ritzen-Bewuchs nach dem
    Steinsatz, Rolle „Stein mit Fuß im Wasser“ (Oberkante 15–40 cm über Spiegel), Rolle „Wandverkleidung“ für Bettwände 0,5–1,5 m, Gehölzgruppe auf Schulter/Felsnase,
    Stückzahl je Größenklasse abwärts (Verhältnis offen, §4/§8.7).

## 8. Auftrag

1. **Regeln „Detailgrad Bachufer“** mit messbaren Werten je Biom-Typ, zuerst tundra/Talkaskade C2 (danach bergwald, heide, aue, elfenwald, dschungel, wueste): Bedeckung im Band
   0–3 m und 3–10 m, Stückzahlen je 10 m je Größenklasse (< 0,1 / 0,1–0,3 / 0,3–1 / 1–3 / > 3 m) und ihr Verhältnis, Stapelung/Kontakt-Anteil, Einbettung, Kipprichtung je Gruppe,
   Haufen-Rhythmus (Größe, Lücke), Farn/Gras in Ritzen (Anteil, Abstand zum Stein), Schutt/Schuttband am Wandfuß, Wasserkante (Steine mit Fuß im Wasser, Erdkante, Nasszone,
   Grasnarbe – bitte die C.3-Regel „Gras 60–80 % über die Kante“ gegen die Referenz entscheiden), Moos/Flechte nach Höhe über dem Spiegel, Ufergehölz, Lesbarkeit aus 30 m.
   Unsere abgeleiteten Zielspalten in §1–§4 sind nur die Messlatte aus dem Bild – bitte bestätigen, korrigieren oder ersetzen.
2. **Konkreter Plan für die p2-Talkaskade** (s 392–575, gern Durchbruch und Bergrinne dazu) im **FORMAT §3-Setzer-Format** (`vorlagen/FORMAT.md`): Instanzen mit Rolle
   (z. B. schutt, platte, stapel, wandverkleidung, fussstein_wasser, ritze_farn, ritze_gras, gehoelz), Netz aus unserem Inventar (§5), Skala, Drehung, Eingraben, `material`
   (Nass/Auflage), **Kollision ab 0,8 m**, **Hindernis-Kennzeichnung für die SWR** (welche Instanzen in den WH-Akteur, Lippen-/Ufer-/Bettfelsen-Filter wie
   `hindernisse_filter_p2.py`), Sichtweite je Rolle. Grundlage ist das Gelände nach 6f (Bettplan 6c eingebaut; `lauf_p2.json`, `spline_z.json`, Querschnitte). Bitte Budget nennen
   (Instanzen, Kollision je Feld; heute Budget 45 000 / 3 000).
3. **Palette und Dichten** als Zahlen für `bachdekor_swr_regeln.json` (Klassen, *_m2 / *_je_m, Abstandsfaktoren, Eingraben, Sichtweiten, Gruppenlogik) und für den Uferplan
   (`kantenufer_p2`-Regeln C.4) – je Rolle die Netzliste aus §5 mit Gewichten; welche Fab-/Mountain-/RA-Netze neu in die Bach-Palette sollen und welche MI-Overrides sie brauchen.
4. **Was gekauft/geladen werden müsste** (nur Liste mit Name, Anbieter, Preis, Größe, Lizenz; **Ferat entscheidet**): für §7 Punkte 1–5 (Scree/Schutthaufen grau, Schieferstapel,
   kantiger Kleinschutt, Uferwand-Module, Erle) – Fab/Megascans/Quixel-Vorschläge, und ob ein vorhandenes Netz mit MI-Override reicht (z. B. Desert_Western-Piles grau,
   Coast-Escarpments grau mit Flechten).
5. **Reihenfolge nach Wirkung** (lokale Aufträge wie in Antwort 18): was zuerst die größte sichtbare Änderung bringt (unsere Lesung: Stein als Füller + Kleinschutt + Stapel-Logik
   vor Farnen/Moos/Gehölz; Wasser-Schaum parallel), mit Prüfkriterium je Schritt (Zählung je 10 m aus Prüfbild oder aus dem Plan) und Prüfkameras.
6. **Wasserkante und Schaum an Steinen in der SWR:** Was ist mit unserem Master `M_Eldarien_Wasser_Schaum8` (ohne FoamAtten/Velocity-Scattering) erreichbar – Kragen an der
   Anströmseite (`ELD_DF_Schaum`?), Schürze je Lippe aus dem SimFoam-Kanal, Nassstreifen über `MF_EL_Nasslinie` –, und was braucht Niagara je Hindernis (NatureWaterFX)?
   Dazu die Kräuselung 5–15 cm und „Normalen nach Tempo“ (V20a) – Parameter oder Knoten, Reihenfolge mit der Diagnose-Reihe D/W.
7. **Offene Punkte – Werte, die NICHT aus dem Referenzbild kommen** (in §1–§5 als „Soll …?“ markiert; bitte entscheiden oder ersetzen):
   Kleinschutt ≥ 2 Lagen (Lagen im Bild nicht ablesbar); Farne an beiden Ufern (Referenz nur Gleitufer) und Schattenseite bevorzugt; Dichte benachbarter 5-m-Felder
   ≥ Faktor 3; Totholz-Werte aus der Witcher-Analyse; Diagnose-Reihe D/W für die Brechungs-Schlieren; Grasfuß ≥ 0,3 m über dem Spiegel; Beckenabstand 3–12 m /
   jede 3. Stufe ohne Becken / Breite ± 30 %; keine Landschaftstextur > 45° und Erdwände ≤ 45°; ≥ 5 Begleitsteine im Umkreis 2 m; Prüfregeln (keine Gras-Instanz
   < 0,5 m an der Kamera, Blickachse in ≥ 2 von 3 Prüfkameras); Stückzahl je Größenklasse ≥ 3× die nächstgrößere (Potenzgesetz – gezählt sind 6 : 1 bzw. 1,5–6 : 1, §4);
   alle Parameter-Vermutungen aus §5 (kiesel_ufer_m2, kiesbank, Erde/Geroell/Kies-Lagen, moos_ufer_m2, Heide-Begrenzung, strauch_gruppe, becken_minus/Schlamm,
   randfels_gross_anteil/Glieder).

Keine eigenen Gestaltungsregeln von uns: §1–§4 sind Beobachtung und Frage, die Regeln kommen von euch.

## 9. Ausgabeformat

- `antworten/20-detailgrad-bachufer.md` mit Regeln je Biom (Tabelle Element → Wert → Prüfung), Reihenfolge, Fab-Liste, Antworten zu 6.
- `antworten/skripte/detailgrad/detailgrad_regeln.json` (Werte, die `bachdekor_swr_regeln.json` und `kantenufer_p2` direkt übernehmen können, Schlüssel wie dort) +
  `plan_p2_talkaskade.json` im FORMAT §3 (Instanzen mit Rolle, Kollision, Hindernis-Flag, Material) + Planer-Skript, das aus `lauf_p2.json`/Querschnitten rechnet (damit wir es
   nach jeder Bettänderung neu laufen lassen können; Reihenfolge-Falle Feldhöhen).
- Bilder/Skizzen: Querschnitt Ufer 0–10 m mit den Zonen und Stückzahlen je Klasse, Draufsicht 10 m Ufer mit Haufen/Lücken-Rhythmus, Beispiel Stapel (Kipp, Einbettung).
- Zahlen so, dass wir sie je 10-m-Abschnitt aus dem Plan und aus Prüfbildern nachzählen können (Sichtschätzung wie hier, Pillow für Wasser).
