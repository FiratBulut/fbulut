# Antwort 23f – Umriss nur zum Außenraum (23.7), Wandfels-Überhang mit Verankerung, trockene Bettzellen zählen mit, Planer-Neulauf im Plan-Modus frei

Gelesen: recherche/auftraege/23f-t23e-ergebnisse-rueckfragen.md @ 7d933a1c5fd7b3aa509dbb60067850dbafeb1787 (Commit 0898ccf)

Stand 19.10.2026. Bezug: Antwort 23e (91a4043), Regeln 23.6 (`regeln_23f_2ae02a28`). Bearbeiter: Cloud-Recherche. Bereich: Sitzprüfung Stufe B,
Deckung C2 Talkaskade. Neue Regelversion **23.7** (Block `nachtrag_23_7` in `steine_sitz_regeln.json`); lokal ausdrücklich zu übernehmen.
Bild `bilder/platzierung/t23e/t23e2_vier_kameras_mitte.jpg` selbst angesehen (§4).

## Kurzfazit

1. **Unsere Hypothese aus 23e §2 war falsch.** Wir hatten vermutet, ein Teil der 66 % nasser Kante sei ein Glättungsartefakt der Breite 5. Ihr
   habt gemessen, dass die Breite die sichtbare Wasserkante kaum verschiebt (+2 / 0 pp) und dass die 66 % aus dem falschen Raster stammten.
   Daraus folgt eine Lockerung: Der **Planer-Neulauf darf jetzt im Plan-Modus auf dem gespeicherten Stand T6N1_0 rechnen**. Nach dem Speichern
   von T6N1/T6N1b wird nachgerechnet (§5).
2. **Trockene Bettzellen – beantwortet:** Sie zählen zur Kante, wenn sie in **beiden** Dumps trocken sind. Dort sind aber nur Lage und Stücke
   **ohne Kollision** zulässig (Kiesel, Kiesel-Haufen, K2 ohne Kollision). Blöcke mit Kollision sind SWR-Hindernisse und kommen erst im
   16h-Bettschritt (§1).
3. **Wandfelsen – beantwortet:** Nicht um 1,8–3,2 m absenken. Ab L × Skala ≥ 4 m gilt ein Überhang als **WARNUNG „ueberhang“** statt
   FEHLER, wenn drei Bedingungen erfüllt sind:
   - der Fels ist bergseitig verankert;
   - die Lücke beträgt höchstens 0,25 × Instanzhöhe;
   - die Luft ist nur zu einer Seite offen.

   Danach entscheidet das Bild. Sonst gilt eine feste Reparaturreihenfolge: Felsfuß, Drehung, Netztausch und Absenken nur bis
   min(1 m; 0,1 × Höhe) (§2).
4. **Wasserkante – beantwortet:** `sichtbar_1` bleibt der Bezug. Es soll nur **eine** Wasserdefinition geben, die für Zonen und Wasserregeln
   gilt. Die Rundung in 2/4-cm-Schritten wird als Spanne mitgeführt; `sichtbar_5` wird einmal als Empfindlichkeit berichtet. Die ±5 pp
   ändern keine Entscheidung (§3).
5. **Neu, aus eurer Diagnose:** Unsere Umriss-Definition aus 23.6 war unvollständig. Ein Loch **im Inneren** einer ausgedünnten Hülle
   galt als „außen“. Ab 23.7 gilt nur der echte Außenraum als Umriss. Das ist eure Variante „nur zum Außenraum“ (83 von 116 ok);
   synthetisch gerechnet und belegt (§1.2).
6. **Nächste Handlung:** Planer-Neulauf C2 Talkaskade im Plan-Modus (ohne Welt-Schreiben) und Abnahme offline (§6).

---

## 1. Stufe B und trockene Bettzellen

### 1.1 Trockene Bettzellen in der Kante (Frage 1)

Die 15,6 % bzw. 11,5 % der neuen Kantenfläche liegen innerhalb der geplanten Bettkante, sind aber im gespeicherten Stand trocken. Vom Ufer
aus sieht man sie als Ufer, deshalb gehören sie in den Nenner der Kante. „Steine ins Wasser nicht in diesem Schritt“ (23e §2) hat zwei
Gründe:

- **Wasser:** Diese Zellen sind trocken.
- **SWR-Hindernis:** Ein Stück mit Kollision im Bettbereich kann den Bake ändern. Dieser Grund gilt für diese Zellen weiter.

**Regel 23.7 (`zonen_bezug_23_7.trockene_bettzellen`):**

- Die Zelle zählt zur Kante, wenn sie **in beiden Dumps** (T6N1_0 und T6N1_2) nicht `sichtbar_1` ist. Das schützt gegen eine leicht andere
  Wasserlinie aus T6N1b.
- **Zulässig:**
  - Lage Kies oder Geröll (≤ 38°);
  - `kiesel`, `kiesel_haufen` (23.5) und K2 **ohne Kollision**.
- **Nicht zulässig bis zum 16h-Bettschritt:** K3 und Blöcke mit Kollision.
- Eine Lage ändert keine Geländehöhe, die Simulation sieht sie also nicht [Annahme]. Ist im Projekt eine Rauheits- oder Reibungskarte aus
  Lagen für die SWR eingerichtet, gilt das nicht; das ist kurz lokal zu bestätigen.

### 1.2 Umriss nur zum Außenraum (Korrektur 23.6 → 23.7)

In 23.6 war der Umriss jede Zelle mit einem Nachbarn ohne Treffer. Bei `netz_huellen` mit höchstens 2 000 Eckpunkten hat die Hülle aber
**Löcher im Inneren**. Ein solches Loch neben einem Hohlraum hat den Hohlraum fälschlich „nach außen“ geöffnet.

**Neu (23.7):** Außenraum sind die Zellen ohne Treffer, die über Zellen ohne Treffer mit dem Rand des Rasters verbunden sind. Nur Zellen
neben dem Außenraum gelten als Umriss. Größere Zellen (0,20/0,30 m) übernehmen wir nicht, weil sie auch echte Lücken wegglätten.

**Selbst gerechnet** (Patch 23.6, dann 23.7 auf den Referenzcode):

- Hauptselbsttest unverändert: `SELBSTTEST OK  Regeln 23.1  Faelle 33  Signatur 64a654746495eca8`.
- Neuer Fall **SB6** (SB5-Hohlraum mit einem Loch in der Eckpunkt-Hülle darüber):
  - 23.7: ok, Hohlraum-Anteil 0,50;
  - 23.6-Weg: FEHLER deckung, luecke mit +0,188 m.
- SB1–SB5 bleiben unverändert. Ausgabe: `SELBSTTEST 23.7 OK  Faelle 11`. Der Schalter heißt weiter `--selbsttest-23-6`.

```
python -I patch_23_7.py sitz_pruefung_23_6.py sitz_pruefung_23_7.py
python -I sitz_pruefung_23_7.py --selbsttest          # Signatur 64a654746495eca8
python -I sitz_pruefung_23_7.py --selbsttest-23-6     # SELBSTTEST 23.7 OK  Faelle 11
```

```python
# patch_23_7.py
"""Patch 23.7 (Antwort 23f) auf sitz_pruefung_23_6.py: Umriss = Grenze zum AUSSENRAUM (Zellen ohne Treffer, die mit dem Rand des
Rasters verbunden sind). Loecher im Inneren einer ausgeduennten Eckpunkt-Huelle gelten nicht mehr als aussen.
Aufruf: python -I patch_23_7.py sitz_pruefung_23_6.py sitz_pruefung_23_7.py"""
import sys
src = open(sys.argv[1], encoding="utf-8").read()
def rep(alt, neu):
    global src
    assert src.count(alt) == 1, alt[:60]
    src = src.replace(alt, neu)

rep('''    tol = R["tol"]["kontakt"]; offen = {k for k, v in d.items() if v > tol}; nb = ((1, 0), (-1, 0), (0, 1), (0, -1))
    erreicht = {k for k in offen if any((k[0] + a, k[1] + b) not in d for a, b in nb)}; st = list(erreicht)
''', '''    tol = R["tol"]["kontakt"]; offen = {k for k, v in d.items() if v > tol}; nb = ((1, 0), (-1, 0), (0, 1), (0, -1))
    aussen = aussenraum(d)                                                   # 23.7: nur echte Aussenzellen sind Umriss
    erreicht = {k for k in offen if any((k[0] + a, k[1] + b) in aussen for a, b in nb)}; st = list(erreicht)
''')
rep('''def luecke_sichtbar(i, welt, insts, kern, zelle=0.10):''', '''def aussenraum(zellen):
    """23.7: Zellen ohne Treffer, die ueber Zellen ohne Treffer mit dem Rand des (um 1 erweiterten) Rasters verbunden sind."""
    i0 = min(k[0] for k in zellen) - 1; i1 = max(k[0] for k in zellen) + 1
    j0 = min(k[1] for k in zellen) - 1; j1 = max(k[1] for k in zellen) + 1
    st = [(i0, j0)]; aussen = {(i0, j0)}
    while st:
        k = st.pop()
        for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (k[0] + a, k[1] + b)
            if i0 <= n[0] <= i1 and j0 <= n[1] <= j1 and n not in zellen and n not in aussen: aussen.add(n); st.append(n)
    return aussen

def luecke_sichtbar(i, welt, insts, kern, zelle=0.10):''')
rep('''            "SB5": (48, 24, 0.5, (36, 8, 10.0 - 0.35), "ok")}.items():
        P, T = ellipsoid(0.8, 0.6, 0.5, nu, nv, 0.0, beule)''', '''            "SB5": (48, 24, 0.5, (36, 8, 10.0 - 0.35), "ok"), "SB6": (48, 24, 0.5, (39, 8, 10.0 - 0.35), "ok")}.items():
        P, T = ellipsoid(0.8, 0.6, 0.5, nu, nv, 0.0, beule)
        if nr == "SB6":   # 23.7: ausgeduennte Huelle mit Loch im Inneren (Netz-Export mit Punktgrenze); nur Eckpunkt-Weg
            P = [p for p in P if (p[0] / 0.8) ** 2 + ((p[1] - 0.15) / 0.6) ** 2 > 0.03]; T = None''')
rep('''            if weg == "d": inst.dreiecke = T''', '''            if weg == "d" and T is None: continue
            if weg == "d": inst.dreiecke = T''')
rep('''("SELBSTTEST 23.6 OK" if not fehl else "SELBSTTEST 23.6 FEHLGESCHLAGEN")''', '''("SELBSTTEST 23.7 OK" if not fehl else "SELBSTTEST 23.7 FEHLGESCHLAGEN")''')
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(src)
print("patch 23.7 ok")
```

**Für die 44 verbleibenden FEHLER:**

- **23.7 laufen lassen.** Erwartet werden etwa 83 von 116 wieder ok, also eure Variante.
- **Danach T23e-3 wie geplant:** Dreiecks-Hüllen und Kameras mit freier Sicht.
- **Die drei `SM_mountain_rock_big_01_5`:** Der „Schornstein“ ist die ausgedünnte Hülle (U1). Mit der Dreiecks-Hülle muss er verschwinden.
  Tut er das nicht, das Netz einzeln melden.

## 2. Wandfelsen mit echter Luft (Frage 2)

Bei 22–32 m großen Felsen ist ein Überhang an einer Wand geologisch normal (Felsdach, Abri). Absenken um 1,8–3,2 m würde die Silhouette
verschieben und den Fels in den Hang drücken. **Unsere Formulierung „tiefer eingraben“ (23e) gilt hier nicht.** Sie war für Steine und
Felsen in Stückgröße gemeint.

**Regel 23.7 (`wandfels`, ab L × Skala ≥ 4 m):**

| Bedingung | Festlegung |
|---|---|
| verankert | ≥ 40 % der Hüllen-Zellen mit d ≤ 3 cm, davon die Mehrheit in der bergseitigen Hälfte (Geländegradient) |
| Überhang statt FEHLER | verankert **und** Lücke ≤ 0,25 × Instanzhöhe **und** offene Umrisszellen ≤ 50 % des Umrisses → **WARNUNG „ueberhang“** |
| Bildprüfung | Kamera mit freier Sicht unter die Lippe. Kein Tageslicht scheint durch, die Lippe liest nicht als schwebend. |
| sonst | FEHLER Lücke wie bisher |

**Reparaturreihenfolge bei FEHLER:**

1. **Felsfuß:** Blöcke 1–3 m nach den Stapelregeln (23) unter die Lippe setzen, bis ≥ 60 % des offenen Umrisses geschlossen sind. So
   entsteht auch in der Natur ein Überhang: Am Fuß liegt Blockschutt.
2. **Drehung** ≤ 10° um die waagrechte Achse parallel zur Wand, Lippe nach unten.
3. **Netztausch** gegen eine Variante mit passender Basis.
4. **Absenken** nur bis `dz ≤ min(1,0 m; 0,1 × Instanzhöhe)`. Das ist die Größengrenze, nach der ihr gefragt habt.
5. Kein Geländeeingriff in diesem Schritt.

Messbar ist das mit vorhandenen Größen. Der Anteil der offenen Umrisszellen fällt in `luecke_sichtbar` ohnehin an. Für die bergseitige
Hälfte genügt das Vorzeichen von (Zelle − Mitte) · Gradient. Für 55360 und 21633 rechnet ihr die drei Bedingungen; Zahlen dazu liegen mir
nicht vor.

## 3. Wasserkante: `sichtbar_1` bleibt (Frage 3)

- **Für `sichtbar_5`:** Die Schwelle läge über der Rundung von 4 cm. Ein Schwellwert unter der Auflösung misst teilweise die Rundung.
- **Dagegen spricht:**
  - `sichtbar_1` ist die Wasserdefinition der Wasserregeln aus 23 (treiben, Kiesel im Wasser) und aus 6k/6m.
  - Mit `sichtbar_5` als Zonenbezug zählten Zellen mit 1–5 cm Wasser zur Kante. Die Wasserregeln nennen sie aber Wasser; ein Stück dort
    wäre gleichzeitig „Kante“ und „im Wasser“.
  - Eure Empfindlichkeit beträgt 0,05–0,06 am Anteil. Der Kanten-Fehlbetrag liegt bei 2,3/2,4 m² je 10 m, der Hang bei 10,5/11,0. Den
    Ausschlag gibt der Hang, und er hängt an der Kante nur über deren Lage.
- **Entscheidung:** `sichtbar_1`. `sichtbar_5` wird einmal als Empfindlichkeit mitgeliefert, mit der Spanne je Zone.
- **Bildkontrolle:** Die im Spiel sichtbare Wasserlinie muss an 2 festen Kameras zwischen den beiden Linien liegen.

## 4. Bildbefund (selbst angesehen, `t23e2_vier_kameras_mitte.jpg`)

| Kamera | Befund |
|---|---|
| C2_48022 | Links neben dem Kreuz liegt eine dunkle Höhlung unter einem Block am Heidehang. Aus Spielerhöhe sichtbar; das passt zu einer echten Lücke. Der Block ist kein Wandfels, die Lücke bleibt also FEHLER (Felsfuß bzw. Erde andecken). |
| C2_64801 | Eine dunkle Platte liegt auf Rundsteinen, die linke Kante wirkt hohl. Das ist wahrscheinlich, aber nicht belegt; T23e-3 mit freier Sicht. **Zusätzlich:** Die Rundsteine zeigen senkrechte Streifen an den Flanken. Das sieht nach einer von oben projizierten Textur (RVT-Fuß bzw. Überblendung) aus, die die Flanken hochgezogen wird (**zu prüfen**). Ein eigener Bildfehler, unabhängig von der Lücke. |
| C2_16606 | Das Ziel ist von Bewuchs verdeckt und nicht beurteilbar. |
| C2_55360 | Das Kreuz liegt auf der Wandfläche. Darüber hängt ein Block zwischen den Wänden; das liest sich als Klemmblock und nicht als Fehler. Die gemessene Lücke selbst ist aus dieser Kamera nicht zu sehen. Erst die Prüfung nach §2 mit Sicht unter die Lippe entscheidet. |

## 5. Gelockerte Regel zum gespeicherten Stand und die übrigen Punkte

**Planer auf T6N1_0:** In 23e hatten wir den Planer bis zum gespeicherten Stand gesperrt, weil Breite 1 die Kante verschieben könnte. Eure
Messung widerlegt das: Die sichtbare Wasserkante bewegt sich kaum, und ein Vergleichslauf mit Breite 1 ändert die Zonen fast nicht.

- **Neu (23.7):** Der Planer-Neulauf darf **im Plan-Modus** auf T6N1_0 rechnen.
- Nach dem Speichern von T6N1 oder T6N1b werden die Zonen nachgerechnet. Verschiebt sich die Kante im Median um mehr als 0,3 m, wird neu
  geplant.
- Das Schreiben in die Welt bleibt ein eigener Schritt mit Pilotfreigabe.

**Fels-Lage über 38°:** Nahe Ansichten mappen ab ~33° triplanar. In der Ferne zeigt die RVT die Projektion von oben, mit einer Streckung von
1/cos(Neigung), also 1,27–1,41 bei 38–45°. Daher:

- 38–45° zulässig, wenn eine Fernkamera (≥ 80 m) keine gestreckte Textur zeigt;
- über 45° nur Netz.

**Plan-Modus der alten Planer:** Danke, damit ist 23e §5 Schritt 2 konkret.

- Ausgabe nur über `--aus`, `--basis`, `--nur-zaehlen`, `--nur-statistik` bzw. `--ohne-veroeffentlichen`.
- Bei WIT, BACH, KANT und `wueste_bewuchs` **keine Rekonstruktion** über eine Kopie der production-Wurzel; dort gilt `folge_unklar` (23.4).
  Eine Kopie der Wurzel mit festem Löschen im Zielordner ist zu riskant für den Nutzen.

## 6. Nächste Handlung (eine, offline): Planer-Neulauf C2 Talkaskade im Plan-Modus

**Eingaben:**

- Regeln 23.7;
- Zonen ab `sichtbar_1` von T6N1_0;
- trockene Bettzellen nach §1.1;
- Ausgabe nur über `--aus` (DETA/P2BE), ohne Welt-Schreiben.

Der Planer setzt nach 23e §4 Stück für Stück und rechnet die Vereinigung neu.

**Abnahme (23d §1.4 a–e, mit 23.7):**

- Jedes Stück hat 0 FEHLER in der Sitzprüfung; 23.2- und 23.3-Prüfung ohne FEHLER.
- Die Zonenziele sind erreicht: Kante sichtbar ≥ 0,85 und Netz ≥ 0,50, Ufer ≥ 0,75 / 0,40, Hang Netz ≥ 0,25.
- Überlappungsfaktor und Kleinzeug in den Grenzen (K1 ≤ 10, K2 ≤ 85).
- In trockenen Bettzellen nur kollisionsfreie Stücke.
- Anteil der Netze ≥ 1 m an der neuen Netz-Vereinigung ≥ 0,5.
- Gegenrechnung mit den Zonen aus T6N1_2: keine Zone weicht um mehr als 0,03 ab.

**Abbruch:**

- Ein Zonenziel ist nur mit mehr als dem Doppelten eures Stück-Fehlbetrags erreichbar (Kante 260, Ufer 30, Hang 480).
- Oder die Reihen-/Ring-Prüfung (23.3) greift. Dann melden und nicht nachschieben.

**Parallel, bereits bei Rolle 1:** T23e-3 (Dreiecks-Hüllen, Kameras mit freier Sicht) mit 23.7 und den Wandfels-Bedingungen nach §2.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Hang 3–10 m:** Netz-Deckung 0,11 statt 0,25. Das ist der größte sichtbare Fehlbetrag (10,5/11 m² je 10 m). Erst Blöcke ≥ 1 m am Hang
   lassen die Talkaskade als Felstal lesen.
2. **Überblendung an Rundsteinen:** Die senkrechten Streifen an den Flanken (64801) fallen in jeder Nahansicht auf. Die Blend-Höhe bzw. die
   Projektion des Steinmaterials prüfen; das ist billiger als jede Neuplanung.
3. **Überhänge mit Felsfuß:** Ein Felsdach liest sich erst mit Blockschutt darunter als Geologie; ohne wirkt es wie ein Platzierungsfehler.
4. **Kiesbank in trockenen Bettzellen:** Kies-Lage und Kiesel-Haufen am trockenen Bettrand ergeben den Übergang Wasser → Ufer, den
   Witcher-Bäche zeigen, und zwar ohne SWR-Risiko.

## Quellen

- `recherche/auftraege/23f-t23e-ergebnisse-rueckfragen.md` (Commit 0898ccf), Bild `bilder/platzierung/t23e/t23e2_vier_kameras_mitte.jpg`
  (selbst angesehen)
- `recherche/antworten/23e-deckung-stufe-b-rueckfragen.md` §1–§6, Patch 23.6 (Commit 91a4043)
- `recherche/antworten/23d-t23-1-neuplanung-rueckfragen.md` §1.3, §1.4 (Commit 8dce6ec)
- `recherche/antworten/23-steine-organisch-im-boden.md`: Referenzcode, Stapelregeln, Wasserregeln (Commit 264a4d8)
- `recherche/antworten/steine_sitz_regeln.json`: jetzt 23.7, Block `nachtrag_23_7`

## Rückfragen

Keine, die den nächsten Schritt ändern. Ob für die SWR eine Rauheitskarte aus Lagen eingerichtet ist (§1.1), ist lokal feststellbar.
