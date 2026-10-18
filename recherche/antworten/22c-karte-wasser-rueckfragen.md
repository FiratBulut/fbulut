# Antwort 22c – karte_wasser: sichtbares Wasser, Höhe < 0, Wasserfall-Becken, Nässe entkoppeln

Gelesen: recherche/auftraege/22c-karte-wasser-rueckfragen.md @ b7a15c9a199eac2fad4ea3392c01edd13f5778c4 (Commit cebf729)

Stand 18.10.2026. Bearbeiter: Cloud-Recherche. Bezug: Antwort 22b §5 (Blob 153651cd0e51) und Antwort 22 (ec8434570446).
Im Projekt ist hier **nichts geprüft oder angewendet**. Die neue Karte `karte_wasser_22b.r8` bleibt **nicht eingesetzt**, bis K1–K9 (§5) bestanden sind.
Kennzeichnung: [Repo] = Datei im Repository, [Ableitung] = aus Belegen geschlossen, [Annahme] = Startwert, lokal zu bestätigen.

## Kurzfazit

1. **Umriss oder sichtbar: entschieden – zwei Ebenen.** `karte_wasser.r8` (Planerkarte) = **sichtbares** gebautes Süßwasser
   (Spiegel − Gelände > 2 cm, wie die v3-Regel). Der Umriss bleibt in der Wasser-Wahrheit und wird als eigene Datei
   `karte_wasser_umriss.r8` (anzulegen) für Sperren beim nächsten Planerlauf geführt. D5 ist kein Fehler: Prüfung umformuliert.
2. **Höhe < 0: entschieden – V1 hat Vorrang, aber nur für Süßwasser.** Die Planerformel definiert Meer als `hoehe < 0 und
   karte_wasser == 0`. Unsere Prüfungen „Meer unverändert“ und „V1 = 0“ in 22b widersprechen sich daher zwangsläufig. Das ist unser
   Fehler. Neue Regel mit vier Klassen in §2; die Zählung der 68 147 Zellen nach Klassen ist lokal offen.
3. **Wasserfall-Becken: entschieden – vor dem Einsetzen nachtragen.** Quelle: `houdini_sichtbar` der 10 bleibenden Netze aus der
   Rest-Liste, nur Becken und Abfluss (§3). Typ `houdini_bleibt` (anzulegen) zuerst in die Wasser-Wahrheit, die Karte liest ihn von dort.
4. **Nässe-Textur: Empfehlung B – jetzt entkoppeln.** Eingefrorene Quelle `karte_naesse.r8` (anzulegen) als Byte-Kopie der heutigen
   Karte, `bewuchs_texturen.py` liest nur noch sie, mit SHA-256-Sperre. Eine Nässe-Änderung ist später ein eigener, bildgeprüfter Schritt.
5. **Prüfungen: revidiert (K1–K9, §5).** Vier der 22b-Prüfungen waren falsch gestellt, nicht nur die Karte. Gründe stehen je Zeile.
6. **Nächste Handlung: T22c-1 Nässe entkoppeln** (§6). Danach T22c-2 Karte v2 neben der alten rechnen. Einsetzen erst nach K1–K9.

---

## 0. Was in 22b §5 nicht stimmte

Offen benannt, damit die Fehlschläge richtig gelesen werden:

- **Meer gegen V1:** Wir verlangten „Meer nach Planerformel unverändert“ und „V1-Abweichung 0“. Liegt gebautes Süßwasser unter 0 m
  (Mündung, Strandsee), schließen sich beide aus: Trägt man es ein, sinkt die Meerzahl; lässt man es weg, bleibt V1 > 0. Die 68 147 Zellen
  sind genau dieser Widerspruch, kein Rechenfehler der lokalen Seite.
- **„30 Felder byte-gleich“:** Die 40 V1-Felder stammen aus T22-0 und zählen nur Felder mit Wasserpflanzen. Die Karte weicht aber in
  50 Feldern ab (22c §2, Unterschied lokal erklärt). Wir haben die Grundgesamtheit von T22-0 als Grundgesamtheit der Karte genommen.
- **„D5 unverändert“:** Ziel war, die Karte an das gebaute Wasser anzugleichen. Der gebaute Fluss ist an der Brücke breiter als das alte
  Band. Eine Änderung dort ist also gewollt; „unverändert“ war die falsche Kontrolle.
- **Wasser undefiniert:** Wir schrieben „gebaute Süßwasserzellen“, ohne Umriss oder sichtbar festzulegen. Daraus kommen 255 733 trockene
  der 775 775 neuen Zellen.
- **Leserliste unvollständig:** Wir haben nur das Repository durchsucht (19 Leser). Lokale Leser fehlten: `bewuchs_texturen.py`
  (Nässe), `t22_0.py` und die Pilotwerkzeuge (`d_alt`). Ohne Ferats Prüfung wäre die Nässe in 50 Feldern still geändert worden.
- **Becken:** 22b verlangte die Becken in der Karte, aber `houdini_bleibt` war erst „anzulegen“. Diese Abhängigkeit war ein Blocker,
  den wir nicht als solchen markiert haben.

## 1. Umriss oder sichtbares Wasser (Frage 1)

**Befund [Repo]:** Alle 19 Leser im Repo werten `karte_wasser > 0` als Süßwasser, auch den Saum 1–127 (z. B. `aue_plan.py` 729,
`sehens_lib/daten.py` 229/535, `felsgruppen_plan.py` 1845, `gefaelle_plan.py` 267). Die Schwelle > 127 nutzt nur T22. Die Planerkarte kann
also nur **eine** Bedeutung tragen. Zwei Zwecke brauchen zwei Ebenen:

| Ebene | Inhalt | Wer liest | Zweck |
|---|---|---|---|
| `karte_wasser.r8` (Planerkarte) | 255 = gebautes Süßwasser der Wahrheit mit Spiegel − Gelände > 2 cm, plus Becken §3; Saum wie bisher, aber aus der sichtbaren Maske, ≤ 127 | 19 Planer-Leser | Röhricht und Uferrollen messen ab der sichtbaren Kante. Der Saum steht an der Wasserlinie, nicht 2–6 m daneben im trockenen Uferband |
| `karte_wasser_umriss.r8` (anzulegen) | 255 = Umriss der Wahrheit (inkl. 309 082 trockener Zellen), sonst 0 | heute niemand; beim nächsten Planerlauf als Zusatzsperre | Sperre für Bäume, Büsche, Felsgruppen im Spline-Band, das bei abweichendem Spiegel (C2: −166/+50 cm, 6l) Wasser tragen kann |
| Wasser-Wahrheit (status24) | Umriss, Spiegel, Typ | T22, Prüfungen | „Wasserzelle“ und Tiefe in 22.2 bleiben unverändert |

- **Schwelle 2 cm [Ableitung]:** dieselbe wie „Pflanze im Wasser: Gelände < Spiegel − 2 cm“ (Antwort 16h-Nachtrag 5, v3). Damit urteilen
  Planerkarte und Reparatur gleich: Was v3 als Land behandelt, ist auch für die Planer Land.
- **Warum nicht der Umriss als Planerkarte:** An der D5-Brücke sind 4 013 der 5 504 neuen Zellen trocken (73 %). Mit dem Umriss setzte ein
  künftiger Planerlauf das Röhricht an den äußeren Rand dieses trockenen Bands, also teils mehrere Meter von sichtbarem Wasser. Genau diesen
  Fehler („Wasserpflanzen fern vom Wasser“) soll V1 beheben.
- **Umriss-Datei ohne Leser ist kein Risiko:** Kein Planer läuft vor der Reparatur-Sperrliste (22b §5). Die Sperre aus dem Umriss wird mit
  dem ersten Neulauf eingebaut (Planer-Änderung, lokal; bis dahin nur spezifiziert).
- **Erwartete Zahlen [Ableitung]:** Neue Wasserzellen ≈ 775 775 − 255 733 = 520 042 (vor Becken und Klasse a aus §2). An D5 bleiben
  ≈ 1 491 bzw. ≈ 1 500 Zellen je Fenster neu. Das ist der breitere gebaute Fluss und **richtig**.
- **D5 neu:** Die Kontrolle heißt jetzt „Pflanzen an der Brücke bleiben gültig“, nicht „Karte unverändert“ (K2).

## 2. Höhe < 0 (Frage 2)

**Planerformel [Repo]:** `meer = (hoehe < 0) & (karte_wasser == 0)` (Konventionen §1b; `sehens_lib/daten.py` 229, `aue_plan.py` 688,
`sumpf_plan.py` 864; `felsgruppen_plan.py` 2493 mit Blockmittel und Blockmaximum). Folgen:

- Jede Zelle unter 0 m ohne Eintrag gilt als Meer, auch eine Flussmündung oder eine Senke im Binnenland. Dort dürfen die Planer
  zwischen −0,3 und 0 m nur Meeres-Rollen (Tang, Muscheln, Treibgut) setzen und darunter nichts.
- Die Karte ist der einzige Hebel. „Meer unverändert“ ist daher keine unabhängige Prüfung, sondern eine Folge der Kartenwahl.

**Regel (Vorrang je Klasse):** Für jede Zelle mit `hoehe < 0` wird lokal die Klasse bestimmt:

| Klasse | Bedingung | Karte | Begründung |
|---|---|---|---|
| a | Wahrheit: gebautes Süßwasser, sichtbar (> 2 cm) | 255 (V1 hat Vorrang) | Eine Mündung ist kein Meer. Heute gilt sie nach der Formel als Meer, dort stehen womöglich Meeres-Rollen |
| b | Wahrheit: Meer | 0 | wie Konventionen §1b |
| c | weder noch, 4-verbunden mit Klasse b | 0 | Strand und Watt unter 0 m; die Formel ergibt richtig Meer |
| d | weder noch, ohne Verbindung zu b (Binnensenke unter 0 m) | byte-gleich zur alten Karte, je Feld gezählt | Die Karte kann „trocken unter 0 m“ nicht ausdrücken: 0 heißt Meer, > 0 heißt Süßwasser. Lösung später über eine Meer-Maske, nicht über `karte_wasser` |

- Die Felder F4, F5, F6 und H7 sind Küstenfelder (Landanteil 51–58 % bzw. 22 %, `biome_je_feld.md`) [Repo]. Dort erwarte ich vor allem
  a und c [Ableitung]. H5 (99 % Land, Sumpf) ist der wahrscheinlichste Ort für Klasse d.
- **Meerzahl:** Sie ändert sich genau um −(neue a-Zellen) + (alte Wasserzellen der Klassen b/c, jetzt 0). Diese Bilanz wird geprüft,
  nicht die Gleichheit (K3).

## 3. Houdini-Wasserfälle (Frage 3)

**Ja, vor dem Einsetzen nachtragen.** Sonst verliert die Planerkarte das sichtbare Wasser an 10 bleibenden Fällen. Außerdem verlangt das
Aufheben der V0-Sperre nach 22b §2 diese Becken in der Wahrheit.

**Minimale Regel:**

1. **Quelle:** das lokale Raster `houdini_sichtbar` (sichtbare Houdini-Wasserflächen, schon für V0 gerechnet), beschränkt auf die 10 Netze,
   die die Rest-Liste `houdini_wasser_rest_r4.md` (nur lokal) als bleibend führt. Nicht das Rechteck und nicht die ganze Rest-Liste.
2. **Zellen:** Netzoberfläche − Gelände > 2 cm (wie §1) **und** Oberflächenneigung ≤ 35° (22b: der Fallschleier liegt darüber).
3. **Nur Becken und Abfluss:** davon die 8-verbundene Komponente, die den tiefsten Netzpunkt enthält. Höher gelegene flache Stücke
   (Oberbecken, Lippe) bleiben draußen [Annahme; bei einem Fall mit Zwischenbecken einzeln entscheiden].
4. **Eintrag:** als Typ `houdini_bleibt` mit Spiegel = Netzoberfläche je Zelle in die Wasser-Wahrheit; die Karte übernimmt ihn wie jedes
   gebaute Süßwasser. Eine eigene Sonderquelle in der Karte gibt es nicht.

- **Wegfallende Netze (15–18):** bleiben draußen, wie 22b §5. Ihre Pflanzen bleiben `gesperrt`. In ihren Feldern läuft kein Planer, bis das
  Netz entfernt ist; das gilt ohnehin bis zur Sperrliste.
- **Abbruch:** Kann die Rest-Liste die 10 Netze nicht eindeutig benennen oder ergibt ein Fall keine Komponente, nicht schätzen. Den Fall melden.

## 4. Nässe im Landschaftsmaterial (Frage 4)

**Empfehlung: Option B, jetzt entkoppeln.** Gründe:

- **Pilot F6 bliebe sonst nicht messbar.** T22-F6-1 Kriterium 7 vergleicht „F6 typisch“ vorher/nachher mit gleicher Kamera (22b §1.3).
  Ändert sich die Bodennässe im selben Zeitraum, lässt sich der Effekt der Pflanzenreparatur nicht mehr vom Boden trennen.
- **Die Nässe ist ein Bildergebnis, keine Planereingabe.** Sie gehört zur Abnahme mit Kameras, nicht in eine Routine-Kette.
- **[Hypothese]:** Die 457 603 Zellen, die Nässe verlören, sind Altwasser. Die „dunkler Schlamm“-Ränder alter Bachbetten (Bildfälle C4/F6,
  Auftrag 22 §2) könnten teils diese Alpha-Nässe sein. Ein späterer Nässe-Schritt könnte sie also gewollt aufhellen. Das ist im Bild zu
  entscheiden, nicht nebenbei.

**Umsetzung (lokal, hier nur spezifiziert):**

1. `karte_naesse.r8` (anzulegen) = Byte-Kopie der heutigen `karte_wasser.r8`, SHA-256 im Standmanifest. Getrennt von
   `karte_wasser_alt_2026-10-18.r8` (22b, `d_alt`): Inhalt heute gleich, Aufgabe verschieden. `d_alt` bleibt eingefroren, die Nässe darf
   später bewusst neu werden.
2. `bewuchs_texturen.py` packt den Alpha-Kanal von `T_Eldarien_Bewuchs_D` nur noch aus `karte_naesse.r8` und liest `karte_wasser.r8` dafür nicht mehr.
3. **Sperre gegen stilles Neubauen: beides, getrennte Datei und Prüfsumme.**
   - Die getrennte Datei entkoppelt die Nässe von der Karte.
   - Die SHA-256-Prüfung im Skript schützt die Datei selbst: Weicht der Hash vom Manifest ab, bricht das Skript **vor** dem Schreiben ab.
   - Ein Hash allein auf `karte_wasser.r8` wäre falsch, denn er sperrte jede Kartenpflege.
   - Bewusste Änderung nur mit einer ausdrücklichen Option samt Test-ID (anzulegen), die den neuen Hash ins Manifest schreibt.
4. Da alle Ketten (`sehens_gelaende_kette.sh`, `gef_gelaende_kette.sh`, `altwasser_kette.sh`, Kette 230) über `bewuchs_texturen.py`
   bauen, deckt die Sperre sie mit ab. Das ist lokal zu bestätigen (§6 Punkt 4). Schreibt eine Kette die Textur auf anderem Weg, ist das ein Befund.

**Späterer Nässe-Schritt (eigene Test-ID, Bildprüfung):** Quelle ist das sichtbare gebaute Wasser (§1) bzw. besser direkt Spiegel und
gebackene SWR-Oberfläche. Das passt zur Linie aus V18 (`T_Eldarien_Wasserspiegel_2m`, `Nass_Breite_cm`) und zur Nasslinie (6e:
„nie doppelt abdunkeln“). Vorher lokal klären, wie V18 die Alpha-Nässe mit der Spiegel-Nässe verknüpft (Maximum oder Produkt). Bei einem Produkt
würde gebautes Wasser doppelt abgedunkelt. Ein Landschaftsmaterial V20 ist im Repo nicht belegt; letzter Repo-Stand ist V18/V18s.

## 5. Revidierte Kontrollprüfungen (Karte v2, vor dem Einsetzen)

| Nr | Prüfung | Kriterium | Änderung gegenüber 22b, Grund |
|---|---|---|---|
| K1 | C2 alter `F_ERLENBACH_1_C2` | p2-Bett = Wasser; altes Band außerhalb p2 = 0 (beides schon erfüllt). Abweichung zur bereinigten C2-Karte **in Planerbedeutung (> 0)**, zerlegt in Saum-Kodierung, trockene Umrisszellen, SWR-Überlauf, Rest: Rest ≤ 1 % der Fensterzellen | 3,40 % mischte Kodierungsunterschiede (972 Saumzellen sind für Planer gleich) mit echten Fehlern. Die Grenze gilt jetzt nur für unerklärte Zellen |
| K2 | D5-Brücke | Jede neue Wasserzelle im Fenster liegt im sichtbaren gebauten Wasser. Die D5-Kontrollinstanzen bleiben in T22 `ok`. Keine steht in sichtbarem Wasser tiefer als die Grenze + 0,2 m | Breiterer gebauter Fluss: Änderung ist gewollt (§1) |
| K3 | Höhe < 0 | Klassen a–d je Feld gezählt; 0 Zellen der Klasse b mit Karte > 0; neue Zellen unter 0 m nur aus Klasse a; Klasse d byte-gleich; Meerzahl-Bilanz nach §2 exakt | ersetzt „Meer unverändert“ und „0 neue Zellen < 0“, die einander und V1 widersprachen |
| K4 | Felder | Soll-Feldliste **vorher** aus dem Vergleich alte Karte gegen Regelraster (§1–3) bestimmt; geänderte Felder = Soll-Liste, alle übrigen byte-gleich | „30 byte-gleich“ beruhte auf der T22-0-Grundgesamtheit (nur Felder mit Wasserpflanzen) |
| K5 | V1 | Abweichung zur sichtbaren Wahrheit = SWR-Überlauf (3 770) + Klasse d, sonst 0 | Vergleich gegen „sichtbar“, nicht gegen den Umriss; Ausnahmen benannt statt „0“ |
| K6 | Becken (neu) | 10 bleibende Fälle mit je ≥ 1 Komponente; 0 Zellen aus wegfallenden Netzen; 0 Zellen > 35°; Restverlust gegenüber `houdini_sichtbar` nur Fallschleier und wegfallende Netze | Becken waren in 22b gefordert, aber nicht prüfbar |
| K7 | Nässe (neu) | Ketten-Lauf mit der neuen Karte in einer Arbeitskopie: Alpha von `T_Eldarien_Bewuchs_D` 0 Texel verschieden; geänderter Hash führt zum Abbruch ohne Schreiben | Seiteneffekt aus 22c §1 |
| K8 | Kodierung | nur Werte 0, 1–127 (Saum), 255; Saum nur an sichtbarem Wasser; `karte_wasser_umriss.r8` ⊇ sichtbares Wasser | Umriss/sichtbar getrennt (§1) |
| K9 | T22 mit Karte v2 | `d_alt` aus `karte_wasser_alt_2026-10-18.r8`: Trockenbett-Gruppe und alle Urteile gleich T22-0b | wie 22b, jetzt mit benannter `d_alt`-Quelle |

- **Unabhängigkeit (`pruefung.md`):** Die Soll-Feldliste (K4) und die Klassen (K3) werden aus Wahrheit und alter Karte gerechnet, nicht vom
  Schreibskript der neuen Karte. K1 vergleicht mit der unabhängig bereinigten C2-Karte.
- **Abbruch:** Ein Fehlschlag in K2, K3, K5, K6 oder K7 → nicht einsetzen; Ursache melden. Kein Lockern der Grenzen ohne neuen Grund.
- **Einsetzen** (eigene Test-ID, nach K1–K9): Sicherung prüfen, Karte und `karte_wasser_umriss.r8` schreiben, Hashes ins Manifest, ein
  Ketten-Lauf als Beleg für K7 im Projekt. Kein Planer läuft (22b §5).

## 6. Nächste Handlung (eine, lokal): T22c-1 Nässe entkoppeln

Klein, rücknehmbar und unabhängig von den offenen Kartenfragen; danach blockiert die Nässe das Einsetzen nicht mehr.

1. `karte_wasser.r8` nach `karte_wasser_alt_2026-10-18.r8` (falls noch nicht vorhanden) und nach `karte_naesse.r8` kopieren
   (beide anzulegen); SHA-256 ins Standmanifest.
2. `bewuchs_texturen.py` auf `karte_naesse.r8` umstellen, mit Hash-Sperre und Freigabe-Option nach §4.
3. **Beweislauf in einer Arbeitskopie des Weltordners** (nicht im Projekt, kein Import): dort `karte_wasser.r8` durch `karte_wasser_22b.r8`
   ersetzen und `bewuchs_texturen.py` laufen lassen. Ausgabe gegen die heutige Textur (exportiert) vergleichen.
4. Alle Aufrufer der Textur in den Ketten auflisten (lokale Suche nach `bewuchs_texturen` und `T_Eldarien_Bewuchs_D`).

**Erfolg, wenn alle gelten:**

- SHA-256 von `karte_naesse.r8` = SHA-256 der heutigen `karte_wasser.r8`;
- Alpha: 0 Texel verschieden, obwohl die Arbeitskopie die neue Karte trägt;
- RGB: 0 Texel verschieden. Ändert sich RGB, hängt auch RGB von `karte_wasser` ab. Das ist ein Befund, dann diesen Kanal ebenso einfrieren;
- Negativtest: ein geändertes Byte in `karte_naesse.r8` der Arbeitskopie → Abbruch, keine Ausgabedatei;
- Aufruferliste vollständig, kein zweiter Schreibweg;
- im Projekt keine Textur neu importiert, kein Paket gespeichert.

**Abbruch:** Weicht Alpha ab, liest das Skript die Karte noch an anderer Stelle. Nicht weiter umbauen, sondern melden.
**Danach:** T22c-2. Die Karte v2 wird nach §1–3 neben der alten gerechnet (`houdini_bleibt` zuerst in die Wahrheit), dann folgen K1–K9.

---

## Was fehlt bis Witcher 4

Messlatte wie in 22b (Witcher-4-Techdemo, Belege in `boden-kleinzeug-gras.md`). Sortiert nach Wirkung:

1. **Eine Wasser-Wahrheit mit getrennten Ebenen statt einer überladenen Byte-Karte.** `karte_wasser.r8` ist heute Planersperre,
   Uferabstand, Meer-Definition, Nässe und Altwasser-Quelle zugleich. Jede Korrektur an einer Bedeutung verschiebt die anderen. Nötig sind
   getrennte Ebenen (sichtbar, Umriss, Meer, Spiegel, Altwasser) aus einer Quelle mit Hash je Verbraucher.
2. **Nässe aus dem echten Wasser.** Die Bodennässe kommt aus einer Planungskarte von früher, nicht aus Spiegel und gebackener Oberfläche.
   Darum ist der Boden an Altwasser nass und an Teilen des gebauten Flusses nicht. Gezielt bildgeprüft umstellen, ohne doppelte
   Abdunkelung mit der Nasslinie.
3. **Explizite Meer-Maske** (anzulegen) statt `hoehe < 0 und karte_wasser == 0`. Mündungen und Binnensenken unter 0 m sind heute nicht
   ausdrückbar (Klasse d).
4. **Ketten ohne Seiteneffekte.** Jede Routine-Kette sollte je Ausgabe ihre Eingabe-Hashes prüfen und protokollieren. Der Fall
   `bewuchs_texturen.py` wurde nur durch Ferats Durchsicht entdeckt.
5. **Houdini-Fälle als gebautes Wasser.** Die 10 bleibenden Fälle sind Sonderfälle mit eigenem Typ. Langfristig gehören Becken und Abfluss als
   echte Wasserkörper mit Spiegel in die Welt, damit Uferband, Nässe und Pflanzen dort wie überall urteilen.

## Quellen

Alle aus dem Repository, Stand Commit cebf729. Eine Webrecherche war nicht nötig.

- `recherche/auftraege/22c-karte-wasser-rueckfragen.md` (b7a15c9a199e); `antworten/22b-…` (153651cd0e51: §1.3, §2, §5);
  `antworten/22-wasserpflanzen-fern-vom-wasser.md` (ec8434570446: §2, §5 V1, `d_alt`); `auftraege/22-…`, `auftraege/22b-…`.
- `antworten/verteilung-KONVENTIONEN.md` (fc1b7adaed9d) §1b; `antworten/skripte/*_plan.py`, `sehens_lib/daten.py` (89f30334e56b),
  `aue_plan.py` (2b6908cbbe3a), `felsgruppen_plan.py` (be2a3fe40cd3), `sumpf_plan.py`, `gefaelle/gefaelle_plan.py`: Leseschwelle `> 0`, Meerformel.
- `vorlagen/daten/biome_je_feld.md` (c4bb08096351): Landanteile F4–H7.
- `auftraege/16h-nachtrag4-v18-muendung.md` (82e74a871a63), `auftraege/16h-nachtrag-materialtest.md` (cb8831e2dfd3): V18, Spiegel-Nässe,
  `Nass_Abdunkeln`; `antworten/16h-nachtrag6e-…` (Nasslinie, nicht doppelt abdunkeln); `antworten/16h-nachtrag5-ufer-c2-c4-lagen.md`
  (e48509e19443: 2-cm-Regel); `auftraege/16h-nachtrag6l-…` (Oberfläche −166/+50 cm).
- `recherche/README.md` (778d8a7b8ac1), `recherche/vorlagen/pruefung.md` (5daf4a9187ba): unabhängiger Sollwert, Vergleichsstellen.
- Nicht im Repo, lokal zu prüfen: `scripts/bewuchs_texturen.py`, die vier Ketten, `t22_0.py`, `houdini_sichtbar`, `houdini_wasser_rest_r4.md`.
