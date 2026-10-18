# Antwort 16h Nachtrag 6l – Deckel mit weichem Rand: Kriterium korrigiert, Schritt 2 an flacher Stelle, Bettziel im Kernbett, Kolkziel erfüllt

Gelesen: recherche/auftraege/16h-nachtrag6l-boden-schritt1.md @ 1c84f6b03dfb4401c5ebf4a0924076b322ce028d (Commit c1a707d)

Stand 18.10.2026. Gesamtauftrag 16h (Erlenbach p2, Talkaskade s 389–580). Bearbeiter: Cloud-Recherche. Bereich: Bodenbefund der SWR p2,
Bettziel, Kolkziel. Wasser bleibt lokal unverändert; die nächste Handlung ist ein reiner Speichertest (§3).

**Bezug, ebenfalls gelesen (alle Commit c1a707d):**
- `recherche/antworten/16h-nachtrag6k-t6j-ergebnisse.md` @ bd2ee3191705d425ce7d96a826143f2de3b26667 (ganz, mit `boden_befund.py`,
  `boden_modelle.py`, §2.4–§2.6, §3.1, §3.3, §5)
- `recherche/auftraege/16h-nachtrag6k-t6j-ergebnisse.md` @ 1c29f5b8d00bf866f0dd923c37c55bf5fbf11993 (ganz)
- `recherche/auftraege/16h-nachtrag6j-teilung-ergebnis.md` @ a49de2d42844b7e0b1488209f1a0dccc872f2d44 und
  `recherche/auftraege/16h-nachtrag6i-baked-sim-tests-stand.md` @ 11c254f0c95defaa25c481ed4047bf7c68625309 (ganz)
- `recherche/antworten/16h-nachtrag6j-teilung-ergebnis.md` @ 322982b7a365180b078aac3f5c6bdd66eb92365a (Kurzfazit) und
  `recherche/antworten/16h-nachtrag6i-baked-sim-tests-stand.md` @ b3582ca1c2e105c43cbb346c06418a212d133e4b (nur über die Verweise in 6k)
- `recherche/antworten/16a-swr-einrichtungstest-teil1.md` @ aa728f71135565e070421f96982fc2dd6397661e (§d1 Bodenerfassung, B1, B4, D6)
- `recherche/antworten/16g-nachtrag-ursache-gefunden.md` @ 7c9737666113ff9d8ff87c480467715f0aca483d (Kurzfazit 1: Spline-Information
  der SWR aus der Wasser-Info der Zone)
- `recherche/antworten/16g-nachtrag2-feinwerte-und-rueckfragen.md` @ 9ca6b951895690bce4f6140dd77aba2b0b843d1b (§1.3, §1.4)
- `recherche/antworten/16f-rueckfrage-epic-parameter-lokal.md` @ 2df21f03041f4840d29cb206a62cf9a709ea33da (§6 Capture, Dilation)
- `recherche/antworten/14b-befund-geteilte-baeche.md` @ afd77f95b06fe7c3d571f5b41b50a334338a477e (§2.1 Dilatation der Wasser-Info)
- `recherche/antworten/skripte/fluss_sim/fluss_sim_regeln.json` @ 9e232c1fd2bac846d6f2c16f41db3728b251e06f (`sim_vorgaben` mit Hinweisen)
- Rechengrundlage: `recherche/antworten/p2_bett/bettplan_p2.json` @ 0013ef4a1922330462308bc7dbad8729ae6a1ef3,
  `recherche/antworten/p2_bett/talkaskade_soll.f32` @ b6f4e2a48fe045ac9e7fdcbb4846ede85cd9153b,
  `recherche/antworten/p2_bett/talkaskade_zonen.u8` @ 8d006acdc26852775efc75583baab32f0cfea422,
  `recherche/antworten/skripte/p2_bett/p2_bettplan.py` @ c65918691ffef1214808d17f86ef1bc21cf2a5c2
- Bild `recherche/bilder/swr/t1_fels_kollision.jpg` (wie die Debug-Bodenkontur aussieht: farbige Fläche über der Szene)

**Kennzeichnung:** [Ferat] eure Messung aus 6l/6k · [Rechnung] von mir mit Repo-Daten gerechnet, Skript in „Code“ · [Projekt] Regel
oder Befund im Repo · [Suchauszug] nur Suchauszug; `dev.epicgames.com` und `forums.unrealengine.com` aus der Cloud nicht erreichbar
(DNS-Fehler, je ein Versuch am 18.10.) · [Ableitung] geschlossen, nicht belegt · [zu prüfen] Name/Wert nicht belegt.

## Kurzfazit

0. **Geschlossen, je eine Zeile:**
   - **O1 ist widerlegt, unser Verdacht war falsch.** Nur 1 von 15 angehobenen Kolken hat ein Hindernis (verlangt ≥ 13). Die „906
     Alt-Hindernisse im Korridor“ aus 6k §5 gab es dort nicht mehr: Der Filter vom 14.10. hatte s 385–585 schon bis auf 13 Teile geräumt.
     Wir hatten die 906 aus 6f übernommen, ohne den Filterstand zu prüfen. Die Beckenblöcke und der Hindernis-Akteur bleiben, wie sie sind.
   - **Editor-Landschaft = `hoehe.f32`** (2 118 Zellen, größte Abweichung 0,89 cm, keine > 5 cm) [Ferat]. Eine abweichende Landschaft
     oder eine aktive Water-Brush-Ebene scheidet als Ursache aus. Das Deckel-Modell auf `hoehe.f32` (−27,9 / −83,3 / −129,4 cm) ist damit
     die gültige Vorhersage; unsere Plan-Vorhersage (p10 −149 cm) war es nicht.
1. **F1 – beantwortet: Ja, das ist ein DECKEL, und zwar ein Deckel mit weichem Rand.** Unser Kriterium „eng ≤ 15 cm“ war falsch gestellt.
   - Es mischte die Auslaufzone des Deckels (Kante 1,5–3 m) in die Bandzellen 0,25–2 m.
   - Es übersah, dass die Editor-Spline an „Rampen“ nicht 0,35, sondern im Median **0,64 m/m** (p90 1,27) fällt, weil ihre 1-m-Proben die
     Stufen tragen. Ein Lagefehler von ±0,5 m (halbe 1-m-Zelle) ergibt darauf allein 57 cm Spanne, ±0,18 m (halbe Sim-Zelle) nur 21 cm
     [Rechnung]. Mit 0,35 m/m × 0,367 m wären es nur 10 cm; das erklärt die 80 cm also **nicht**.
   - Das beste Modell (Spline-Deckel, voll bis Kante 1,5 m, Auslauf bis 2,5 m, Lagefehler ±0,5 m) trifft flach / Rampe / 0,25–1 m / 1–2 m
     mit 41 / 79 / −31 / −80 cm (gemessen 34,5 / 80 / −29,8 / −82). Ein Deckel auf dem Stufenspiegel trifft die Rampen nicht (139 cm)
     [Rechnung].
   - **Neues Kriterium „Deckel-Kern“** (§2.3), vor jeder Messung festgelegt, Selbsttest 9/9. Die alten Urteile ERSATZWERT/GLÄTTUNG waren
     Folgen unserer Prüfreihenfolge, keine Befunde.
   - **Mechanismus – wartet auf Beleg Schritt 2.** Eure Hypothese „die Aufnahme sieht eine Fläche auf Spline-Höhe“ habe ich in sechs
     Varianten geprüft (§2.4).
     - Wassernetz in einer Tiefenaufnahme von oben: verworfen, weil es das Bett anheben würde (gemessen −1,2 cm).
     - Eine Aufnahmeebene mit Offset: als Ursache verworfen, denn eine einzelne Ebene folgt keinem Gefälle von 155 m.
     - Bester Kandidat bleibt die **Wasserhöhe aus der Wasser-Info als Deckel (D1)**: Die Höhe passt (Spline), die Rampenstreuung passt.
       Nur die Reichweite widerspricht, denn sie folgt nicht der Spline-Breite. Das Modell sagt für T6j-C in der Klasse 2–2,5 m 0 % statt
       80 % voraus, gemessen sind 48–55 % in beiden Läufen.
2. **F2 – beantwortet: Ja, Schritt 2 an einer flachen Stelle, nicht an s 439.**
   - An s 439 überlagern sich drei Effekte: die Auslaufzone, die schrägen Lippen 10/11 (27°/32°) und der Lagefehler auf der Rampe.
   - Durch die schrägen Lippen liegt der Plan-Spiegel 4 m neben der Achse 0,58 m unter bzw. bis 0,78 m über der Editor-Spline [Rechnung].
   - Die 21 Kandidaten genügen; die Auswahlregel steht in §3.2, eine Liste brauche ich nicht.
3. **F3 – beantwortet: Es liegt am 1-m-Raster, nicht am Deckel. Das Ziel ist korrigiert.**
   - Auf dem Plan-Gelände mit Spiegel + 13 cm gibt dasselbe 1-m-Raster ohne Versatz 100 %. Mit 0,5 m Querversatz zwischen Wasser und
     Gelände sind es **89,5 %** (gemessen 88,6 %): Randzellen 83,6 %, Kernbett 99,6 % [Rechnung].
   - **Neues Bettziel:** Kernbett (Innenabstand ≥ 2 Zellen, Geländeneigung < 0,5 m/m) sichtbar_1 ≥ 99 %. Das ganze Bett bleibt bei
     „nass ≥ 97 %“ als Gesundheits- und Abbruchgrenze; sichtbar_1 des ganzen Betts wird nur gemeldet.
   - Die Aufteilung eurer 82 Fehlzellen **wartet auf Beleg** (`bett_fehlzellen.py` auf T6JB0_2). Sie läuft mit dem nächsten Dump, kein
     eigener Schritt.
4. **F4 – beantwortet: Kolkziel erfüllt.**
   - 24/24 Kolke haben ≥ 0,8 m sichtbare Tiefe, 18–20 liegen in 0,8–1,2 m, das Maximum ist 1,34 m.
   - Die Obergrenze gilt der Bettform. Sichtbar kommt der Überstand des gebackenen Spiegels hinzu (13–16 cm, T-b1). Verfeinert heißt das
     Ziel deshalb: sichtbar 0,8 m bis 1,2 m + 0,15 m.
   - Die Anhebung des Simulationsbodens in den Kolken bleibt eine Diagnose (O2 nicht erreicht, Ursache offen), kein Ziel.
5. **Eigene Fehler korrigiert (§6):** Kriterium „eng“, Plan- statt Weltgelände in der Vorhersage, O1-Prämisse, Schritt-2-Ort s 439,
   doppeldeutige Abbruchgrenze „Bett < 97 %“, D2 als gleichrangige Hypothese.

**Nächste Handlung (genau eine, im Editor, nur im Speicher, ≈ 30 min):** Schritt 2 an einem flachen Kandidaten (§3).
- **Ablauf:** Eigenschaften nur lesen, dann `render_state` = `DEBUG_RENDER_BOTTOM_CONTOUR` setzen. Zwei Messlatten wie in T-b1: eine
  am Ufer bei Kante 0,75–1,5 m, eine im Bett.
- **Erfolgskriterium:**
  - Die Bettlatte zeigt die Kontur auf dem Bettgelände ± 10 cm (Kontrollfall).
  - Die Uferlatte ist auf ± 5 cm abgelesen.
  - Das Ergebnis fällt in eines der drei vorab festgelegten Bänder:
    - **A:** Kontur auf Spline + 2…6 cm ± 10 cm, also ≥ 0,7 m unter dem Gelände.
    - **B:** Kontur auf dem Gelände ± 10 cm.
    - **Z:** dazwischen.
- **Entscheidung:**
  - A → Der Deckel sitzt in der Bodenkontur der Simulation, §2.5 aus 6k gilt. Dann T6j-C im Debug-Zustand mit erzwungener
    Wasser-Info-Erneuerung.
  - B → Schritt 3a (`smoothing_width` 1).
  - Z → wie A, mit Glättungsvermerk.

---

## 1. Geschlossene Befunde

| Punkt | Befund [Ferat] | Folge | Status |
|---|---|---|---|
| O1 (6k §5) | 1 statt ≥ 13 von 15; 3 Kolke berühren einen Grundriss, alle mit Ufersteinen aus „detailgrad“; in s 385–585 nur 13 Altbestand-Teile | Verdacht widerlegt; die Regel „Hindernisliste nach jedem Einbau neu bilden“ (6k §5) entfällt als Kolk-Hebel | **verworfen** |
| O2 (6k §5) | r(Anhebung; Kolkbreite) −0,52 / −0,47 / −0,13, verlangt ≤ −0,6 | nicht erreicht; nach der 6k-Regel wird das Kolkziel über „Kolktiefe sichtbar“ geprüft (§5) | Diagnose offen, kein Ziel |
| Landschaft | Editor − `hoehe.f32`: Median −0,03 cm, |max| 0,89 cm | Landschaft und Water-Brush als Ursache des tiefen Bodens ausgeschlossen | **geschlossen** |
| GLÄTTUNG (T6JC_2) | r_Laplace 0,504; 1-m-Umtasten allein 0,48, nativ 0,35 | Fehlurteil der Schwelle im 1-m-Raster; Glättung kann den Band-Median −64 cm ohnehin nicht erzeugen (6k §2.3) | **verworfen** |
| ERSATZWERT (T6JB0_2) | nur Rückfall über den Sprung −50 cm; Reichweite bei Bett + 0,5 m und Bett + 2 m gleich | Fehlurteil der Reihenfolge; F bleibt verworfen (6k) | **verworfen** |

---

## 2. F1: Deckel mit weichem Rand

### 2.1 Was die Messung festlegt [Ferat]

- **Höhe:** Boden ≈ min(Gelände; Editor-Spline + 2…4 cm). r(Versatz; Gelände − Spline) −0,82. Bett −1,2 cm.
- **Reichweite:** etwa 3 m hinter der Plan-Bettkante, mit einem Übergang über 1–2 m. Sie ist bei Spline Bett + 0,5 m und Bett + 2 m
  gleich.
- **Streuung von Boden − Spline:** flach 33–36 cm, an Stufen und Rampen 78–82 cm. In beiden Rastern echt, ein injizierter Deckel wird
  mit ≤ 8 cm Spanne wiedergefunden.
- **Tiefe G** im Band ≈ 0,1 m (Profil: 11, 12, 7, 2 cm nach außen abnehmend). Genau das erwartet ein Deckel im Eingang: Spiegel
  13–16 cm über der Spline (T-b1) minus Boden auf Spline + 2…4 cm ergibt G ≈ 9–14 cm.

### 2.2 Warum „eng ≤ 15 cm“ falsch gestellt war [Rechnung, `deckel_rand.py`]

| Ursache der Streuung | Spanne p90 − p10 an „hoch“-Zellen | Erklärt |
|---|---|---|
| Lagefehler ±0,18 m (halbe Sim-Zelle) auf 0,35 m/m | 10 cm | nein |
| ±0,18 m auf den echten Rampenneigungen (p50 0,64, p90 1,27 m/m) | 21 cm | nein |
| ±0,5 m (halbe 1-m-Zelle bzw. ganzzahliges s je Zelle) auf diesen Neigungen | 57 cm | den Rampen-Überschuss |
| Auslaufzone (Deckel bis Kante 1,5 m voll, bis 2,5 m auslaufend), ohne Lagefehler | flach 41 cm | den flachen Teil |
| Netz-Tessellierung: linear statt kubisch zwischen 1-m-Punkten | 2 cm | nein |
| Wasser-Info 0,29 m/Pixel (±0,15 m Lage) | ≤ 21 cm (wie ±0,18 m) | nein |

**Anpassung an eure Kennzahlen** (Gitter über Reichweite, Glättung, Lagefehler; Plan-Gelände):

| Modell | flach | Rampe | gesamt | 0,25–1 m | 1–2 m | p10 |
|---|---|---|---|---|---|---|
| **gemessen** [Ferat] | **34,5** | **80** | **70,5** | **−29,8** | **−82** | **−121** |
| Spline-Deckel, Reichweite 2,5 m, Lagefehler ±0,5 m | 41 | 79 | 53 | −31 | −80 | −132 |
| Spline-Deckel, Reichweite 2,5 m, Glättung 1,1 m, ohne Lagefehler | 59 | 69 | 62 | −36 | −69 | −117 |
| Deckel auf Plan-Stufenspiegel + 8 cm | 50 | **139** | 86 | −33 | −82 | −108 |

Werte in cm.
- **Lesart:** Ein Deckel auf Spline-Höhe mit weichem Rand und ±0,5 m Lagefehler erklärt Höhe, Mediane und beide Streuungen [Ableitung].
- **Rest:** In der Gesamtspanne (53 statt 70 cm) bleiben etwa 45 cm (quadratisch) unerklärt. Dazu passen einzelne Zellen auf
  Stufenspiegel-Höhe wie bei s 439 (§3.1).
- **Vorbehalt:** Die Reichweiten-Anteile habe ich mit „Boden < Gelände − 10 cm“ gezählt. Eure Definition von „gedeckelt“ steht nicht im
  Auftrag, deshalb vergleiche ich die Anteile nur qualitativ.
- **Der ±0,5-m-Lagefehler ist vermutlich unser Messweg, nicht die Engine** [Ableitung]. Mögliche Ursachen: ganzzahliges s je Zelle oder ein
  Halbzellen-Versatz zwischen Dump-Texel und Landschaftsscheitel. `versatz_pruefen.py` prüft den zweiten Fall am Bett. Er gehört in die
  Auswertung des nächsten Dumps, nicht vor Schritt 2, denn Schritt 2 liest im Editor ab.

### 2.3 Korrigiertes Kriterium „Deckel-Kern“ (vor dem Test festgelegt)

- **Kern:** Band (Maske 2/3), Kante 0,25–1,25 m, also vor dem Auslauf. Gelände > Spline + 0,30 m.
- **Toleranz je Zelle:** 10 cm + 0,5 m × Neigung der Spline-Höhe an der Zelle.
- **DECKEL-Kern,** wenn ≥ 75 % der Kernzellen in der Toleranz liegen **und** |Median(Boden − Spline)| ≤ 10 cm.
- **GLÄTTUNG** nur noch, wenn r_Laplace ≥ 0,5 im nativen Raster **und** |Band-Median| < 10 cm gilt. Glättung sagt einen Median ≈ 0
  voraus (6k §2.3).
- **Kontrollfälle** (Plan-Gelände, `deckel_kern.py --selbsttest`, 9/9 OK):
  - Die vier Deckel-Varianten liegen bei 86–100 % in der Toleranz.
  - Glättung 1,8/4 m, Ersatzwert, Bezugshöhe und „kein Versatz“ liegen bei 5–44 % bzw. haben einen Median > 10 cm.
- **Grenze:** Das Kriterium trennt Spline- und Stufen-Deckel nicht (80 %). Diese Trennung leistet die Rampenstreuung (§2.2).
- **Vorhersage für T6JB0_2/T6JC_2:** ≥ 75 % (Modell 97,5 %). Es läuft mit dem nächsten Dump mit und ist **nicht** Voraussetzung für
  Schritt 2. Den Weg zu Schritt 2 öffnet schon das Profil (6k-Regel „uneindeutig → Profil“), denn es zeigt den Deckel an beiden Ufern.

### 2.4 Woher kommt der Deckel? Eure Hypothese, Variante für Variante

| # | Kandidat | Vorhersage | gegen die Messung | Urteil |
|---|---|---|---|---|
| 1 | Wassernetz bzw. Info-Netz des Flusses in der Tiefenaufnahme **von oben** | Boden = max(Gelände; Wasserfläche) → Bett auf Spline-Höhe angehoben | Bett −1,2 cm | **verworfen** |
| 2 | dasselbe, Aufnahme **von unten** bzw. Minimum der Tiefe | min(Gelände; Wasserfläche) | Forenbefund 5.7: Bei verdrehter Bodenkontur halten trockene Zellen „captureZ + depth statt der Geländehöhe“; normal ist also captureZ − Tiefe, eine Aufnahme von oben [Suchauszug, Ableitung]. Nur getaggte bzw. gelistete Akteure und die Landschaft werden aufgenommen (`managed_show_only_actors`, 16a §d1) | **unwahrscheinlich**; in Schritt 2 lesen, ob der Fluss-Akteur Tag oder Listeneintrag trägt |
| 3 | **Wasserhöhe der Wasser-Info als Deckel (D1):** Boden = min(Aufnahme; Wasser-Info-Z + c) im Fußabdruck des Flusses | Höhe = Spline; Rampenstreuung über Lagefehler; Reichweite = Spline-Breite + Dilatation | Höhe ✓, Streuung ✓ (§2.2). Belegt ist, dass die SWR ihre Spline-Information (innen/außen, Höhe) aus der Wasser-Info liest (16g-Nachtrag) [Projekt]. **Reichweite ✗:** Folgt sie der Spline-Kante, fällt in T6j-C die Klasse 2–2,5 m von 80 % auf 0 % [Rechnung]; gemessen 48–55 % in beiden | **bester Kandidat, offen.** Er passt nur, wenn (a) die Wasser-Info in T6j-C nicht erneuert wurde oder (b) der Fußabdruck nicht an `RiverWidth` hängt [zu prüfen] |
| 4 | Aufnahmeebene + `bottom_contour_capture_offset` (D2) | eine Ebene für die ganze SWR | Eine Ebene kann keinem Deckel folgen, der 155 m Gefälle auf 2–4 cm nachzeichnet [Ableitung]; Feld nur als `float` ohne Beschreibung belegt [Suchauszug] | **als Ursache verworfen**; Wert in Schritt 2 nur lesen |
| 5 | Deckel auf dem örtlichen Wasserstand (Stufenspiegel, z. B. Rückkopplung des gebackenen Spiegels über die Wasser-Info in WCBS) | Rampenstreuung ∝ Fallhöhen | Rampe 139 statt 80 cm [Rechnung]; einzelne Zellen bei s 439 passen (§3.1) | **nachrangig** |
| 6 | Glättung nur in der gebackenen Ausgabe (D3) | Kontur im Debug folgt dem Ufer | Dann müsste das Band echtes Wasser mit G ≈ 0,1 m auf bis zu 35° steilen Böschungen tragen (46 % der Bandzellen > 10 cm); das hält eine Flachwasser-Simulation in Ruhe nicht [Ableitung] | **nachrangig**; Schritt 2 trennt es ab |
| – | `remove_outside_spline_amount` 0 | entfernt Wasser außerhalb der Spline, keinen Boden (`fluss_sim_regeln.json`-Hinweis) | – | ohne Einfluss auf den Boden |

**Zur Dilatation:**
- Der Water Body hat `ShapeDilation` (float) [Suchauszug, API]. Im Repo steht als Standard 4 096 cm, im dilatierten Teil unter den Boden
  gedrückt (`UndergroundDilationDepthOffset` 64).
  - Das stammt aus einer früheren Code-Lesung (5.6.1). Ich habe es nicht neu belegt, für 5.8 gilt es als [zu prüfen].
  - Für Kurzstücke schlägt das Projekt 200 cm vor (14b, `gefaelle_plan.py`).
- Eine Reichweite von ≈ 2,5–3 m ab Bettkante passt nicht zu 41 m. Sie passt nur zu einem kleinen Wert oder dazu, dass D1 die Dilatation
  nicht nutzt.
- Den tatsächlichen Wert am Erlenbach liest Schritt 2 nur aus.
- `bottom_contour_collision_dilation` ist als C++-Feld `BottomContourCollisionDilation` belegt [Suchauszug]; der Python-Name ist
  [zu prüfen]. Er vergrößert laut Epic Hindernisse (16f §6) und betrifft die Landschaft nicht [Ableitung].

---

## 3. F2 und nächste Handlung: Schritt 2 an einer flachen Stelle

### 3.1 Warum nicht s 439 [Rechnung, `deckel_rand.py` D; Ferat §2]

- s 439 liegt im kurzen Becken (Plan-Spiegel 89,229 m) zwischen Lippe 10 (s 437,6, Fall 0,90 m, 27,4°) und Lippe 11 (s 439,88, Fall
  0,53 m, 32,0°). Die Editor-Spline glättet die Stufen zu einer Rampe (89,48 → 89,21 m zwischen s 438 und 439,5).
- Wegen der schrägen Lippen liegt der Plan-Spiegel bei u = −4 m schon auf dem unteren Becken (88,696 m, 0,58 m unter der Spline). Bei
  u = +4 m liegt er an s 438–438,5 noch auf dem oberen Becken (90,127 m, 0,65–0,78 m über der Spline).
- Eure Zellen u +4,11 (Boden 90,11 m) und u −4,11 (88,79 m) sitzen genau auf diesen Beckenspiegeln. u −3,16 und −4,43 (89,20 / 89,31 m)
  sitzen dagegen auf der Spline.
- Eine Latte dort trennt deshalb nicht sauber: Spline-Deckel, Stufen-Deckel und Auslaufzone (Kante 2,4–2,8 m) liegen auf engem Raum
  übereinander.

### 3.2 Auswahl unter den 21 flachen Kandidaten

Ein Kandidat muss alle Punkte erfüllen; unter den übrigen den mit dem größten Gelände − Spline nehmen:
1. Boden − Spline in beiden Dumps +2 bis +6 cm.
2. Spline-Neigung < 0,05 m/m über s ± 3 m (kein Lagefehler, keine schräge Lippe in der Nähe).
3. Kante 0,75–1,5 m (vor dem Auslauf, §2.2).
4. Gelände − Spline ≥ 0,8 m an der Latte, damit A und B ≥ 0,7 m auseinanderliegen.
5. Kein Hindernis-Fußabdruck im Umkreis von 2 m, nicht Maske 3.
6. Im selben Querschnitt eine Bettzelle mit W − H ≥ 0,2 m für die Kontrolllatte.

### 3.3 Ablauf (alles im Speicher, nichts speichern; Rückweg: Level ohne Speichern neu laden)

1. **Nur lesen** (Skript unten, Namen per `dir()`, nicht geraten):
   - an der SWR alle Felder mit `contour`, `capture`, `smooth`, `dilat`, `spline`, `water_info`;
   - am Erlenbach-Fluss alle Felder mit `dilation` sowie die Tags;
   - `bottom_contour_actors` / `bottom_contour_tags`: Steht der Fluss-Akteur darin? (Variante 2)
2. **Latten** wie in T-b1, **ohne** Tag `SWR_Hindernis` und nicht in `bottom_contour_actors` (sonst würden sie selbst aufgenommen).
   - **Uferlatte:** an der Kandidatenzelle, Bereich Gelände − 1,2 m bis Gelände + 0,3 m, also 1,2 m in den Boden versenkt.
   - **Bettlatte:** Bereich Bettgelände − 0,3 m bis + 1,2 m.
3. **Umschalten:** `render_state` = `DEBUG_RENDER_BOTTOM_CONTOUR` [belegt 16a]. Laut 16a D6 startet jede Änderung die Simulation neu
   (B0). Die Bodenkontur entsteht beim Reset, Warten auf volle Becken ist für die Kontur also nicht nötig [Ableitung].
4. **Ablesen:**
   - Die Kontur erscheint als farbige Fläche (Bild 16a).
   - Liegt sie unter der Landschaft, im Viewport „Show → Landscape“ ausschalten [zu prüfen in 5.8.3]. Das ist ein reiner Viewport-Schalter,
     der die Aufnahme nicht betrifft [Ableitung].
   - Ändert sich die Kontur beim Ausblenden der Landschaft, gilt der Lauf als ungültig (Abbruch unten).
   - Draufsicht-Bild: Wie weit reicht die flache Fläche quer, gemessen ab Bettkante und ab Spline-Kante (Bett + 1 m)?
5. Level ohne Speichern neu laden und prüfen, dass BAKED_SIM wieder steht.

### 3.4 Erwartung und Entscheidung (vorab festgelegt)

| Ergebnis an der Uferlatte | Bedeutung | Nächster Schritt |
|---|---|---|
| **A:** Kontur = Spline + 2…6 cm ± 10 cm (≥ 0,7 m unter dem Gelände) | Der Deckel sitzt in der Bodenkontur, die die Simulation bekommt (D1 oder Variante 2). 6k §2.5 gilt: Phantom-Schulter, Boden-Trick bleibt zurückgestellt, Kantenbewuchs erst nach der Behebung | **T6j-C im Debug-Zustand:** `RiverWidth` Bett + 0,5 m in s 389–580, `r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames 10` (belegt, 16g-N2), Reset, nur die Kontur ansehen. Rückt der Rand der flachen Fläche um ≈ 0,75 m nach innen, ist es der Wasser-Info-Fußabdruck (Hebel: Breite bzw. `shape_dilation`). Rückt er nicht, die Header-Kommentare zu den Bodenkontur-Feldern lokal lesen (5.8.3, nur lesen) |
| **B:** Kontur = Gelände ± 10 cm | Die Bodenkontur ist richtig; der Deckel entsteht später (Ausgabe D3 oder Begrenzung im Löser) | **Schritt 3a** (6k): `smoothing_width` 1, Lauf ab Reset bis stabil, Dump. Verschwindet der Deckel, war es die Ausgabe: „sichtbar“ bleibt das Maß, die Simulation ist gesund. Bleibt er, sitzt er im Löser: Header lesen wie bei A |
| **Z:** 0,15–0,6 m unter dem Gelände | Deckel in der Kontur mit Glättung | wie A, Wert notieren |
| Bettlatte zeigt nicht Bettgelände ± 10 cm, oder die Kontur ist nicht ablesbar | Messweg ungültig | Level neu laden, direkt Schritt 3a |

**Abbruch:** Ändert sich die Kontur beim Ausblenden der Landschaft, oder ist nach 30 min kein Ablesewert da: Level neu laden, Ergebnis
„Messweg ungültig“ melden, kein zweiter Versuch mit anderem Ort.

---

## 4. F3: Bettziel sichtbar_1 – 1-m-Raster statt Deckel

**Warum nicht der Deckel:** Er wirkt außerhalb des Betts, und der Bettboden passt (−1,2 cm). Der Spiegel im Becken steht 13–16 cm über der
Spline. Ein Deckel im Eingang senkt ihn nicht so, dass einzelne Bettzellen W − H ≤ 1 cm bekämen [Ableitung].

**Warum das Raster** [Rechnung, `bett_fehlzellen.py --kontrolle`; Plan-Gelände auf 1 m, Spiegel = Plan-Stufenspiegel + 13 cm]:

| Lage Wasser gegen Gelände | Bett sichtbar_1 | Randzellen (Innenabstand 1) | Innenabstand ≥ 2 | Neigung ≥ 0,5 | Kernbett |
|---|---|---|---|---|---|
| kein Versatz | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| 0,5 m längs | 99,0 % | 97,9 % | 100,0 % | 97,7 % | 100,0 % |
| **0,5 m quer** | **89,5 %** | 83,6 % | 95,0 % | 81,8 % | **99,6 %** |
| 0,5 m diagonal | 92,5 % | 84,4 % | 100,0 % | 88,7 % | 100,0 % |
| **gemessen** [Ferat] | **88,6 %** | – | – | – | – |

- Bei 4 m Bettbreite (Plan p50) ist im 1-m-Raster fast jede zweite Bettzelle eine Randzelle (384 von 802).
- Das Plan-Bett besteht zu 15,3 % aus Stufenwand/Rampe (Neigung p50 1,6 m/m) und zu 10,8 % aus Lippenkronen.
- Ein Lageversatz von ±0,18 m gefährdet 5,8 % der Bettfläche, ±0,5 m bis 33,9 % (obere Schranke), vor allem Rand und Wand.
- Eure 88,6 % liegen damit dort, wo ein halber Zellenversatz sie hinlegt [Ableitung].

**Korrigiertes Bettziel** (ersetzt „Bett: sichtbar_1 ≥ 99 %“ aus 6k §3.3):
- **Kernbett** = Bettzellen mit Innenabstand ≥ 2 Zellen und Geländeneigung < 0,5 m/m: **sichtbar_1 ≥ 99 %.**
- **Ganzes Bett:** nass (G > 0,001) ≥ 97 % bleibt Gesundheits- und Abbruchgrenze (6k §2.6). sichtbar_1 des ganzen Betts nur melden.
- Wände und Rampen urteilt ihr im Bild; dort zeichnen ohnehin Kaskadenvorhang und Fall-Effekte (Entscheidung 16).
- Kolke gelten über §5.
- **Wartet auf Beleg:** `bett_fehlzellen.py --dump` auf T6JB0_2 teilt die 82 Fehlzellen auf. `versatz_pruefen.py` zeigt, ob ein
  Halbzellen-Versatz vorliegt. Findet es einen, die Abtastung angleichen und Bett und Deckel-Kern neu auswerten.
- Beides läuft mit dem nächsten Dump. Liegt das Kernbett dann < 99 %, ist das ein echter Mangel: trockene oder dünne Kernzellen, die einzeln
  anzusehen sind.

---

## 5. F4: Kolke – Ziel erfüllt

- **Messung** [Ferat]: W − H an der tiefsten Zelle, Median 107 cm, Spanne 80–134 cm. 18–20 von 24 liegen in 0,8–1,2 m, keiner darunter.
- **Plan** [Rechnung]: Die Kolktiefe der 24 Hauptbecken beträgt 0,84–1,20 m, Median 1,06 m. Die sichtbare Tiefe entspricht also dem
  Entwurf.
  - Mit dem Überstand des gebackenen Spiegels (+0,13 m) lägen 11 Kolke über 1,2 m.
  - Gemessen sind es 4–6, weil die 1-m-Zelle den tiefsten Planpunkt selten trifft [Ableitung].
- **Ziel verfeinert:** Kolktiefe sichtbar ≥ 0,8 m an allen 24 und ≤ 1,2 m + 0,15 m Überstand = 1,35 m. Gemessen 24/24 ≥ 0,8 m,
  höchstens 1,34 m → **erfüllt**.
- Die Bettform wird nicht geändert (6k-Regel bei „kein O1“).
- **Was offen bleibt:** Der Simulationsboden liegt in 19–20 Kolken über +10 cm. Das betrifft Strömung und Schaumbildung im Kolk, nicht
  das Bild der Tiefe. Liegt der Deckel in der Bodenkontur (Ergebnis A), sieht man die Kolkböden im selben Debug-Bild mit. Dann zuerst dort
  nachsehen, bevor eine eigene Kolk-Hypothese aufgemacht wird.

---

## 6. Korrekturen an eigenen Antworten

| Antwort | Aussage | Korrektur |
|---|---|---|
| 6k §2.4 / `boden_befund.py` | DECKEL nur bei „eng“ p90 − p10 ≤ 15 cm über alle Bandzellen 0,25–2 m | **Falsch gestellt:** Es mischte Auslaufzone und Lagefehler auf steiler Spline ein. Ersetzt durch „Deckel-Kern“ (§2.3). Die Reihenfolge der Urteile erzeugte ERSATZWERT/GLÄTTUNG als Fehlurteile |
| 6k Kurzfazit/§2.6 | Vorhersage am Plan-Gelände (p10 −149 ± 20 cm) | Die Vorhersage gehört auf `hoehe.f32` (−129 cm); gemessen −121 cm. Unsere Toleranz war um den falschen Mittelwert gelegt |
| 6k §5 | „906 Alt-Hindernisse im Korridor, gesetzt auf das Gelände vor dem Aushub“ | **Falsch:** Der Filter vom 14.10. hatte den Korridor bis auf 13 Teile geräumt; O1 ist widerlegt |
| 6k §2.6 Schritt 2 | Latte bei s 439 | ungeeignet (§3.1); flacher Kandidat nach §3.2 |
| 6k §2.6 Abbruch | „Bett der Talkaskade < 97 %“ | gemeint ist **nass** (G > 0,001), nicht sichtbar_1; sonst bräche jeder Lauf bei 88,6 % ab |
| 6k §3.3 | „Bett: sichtbar_1 ≥ 99 %“ | ohne Rasterprüfung gesetzt; jetzt Kernbett (§4) |
| 6k §2.4 | D2 (Aufnahmeebene + Offset) gleichrangig mit D1 | Eine Ebene folgt keinem 155-m-Gefälle; als Ursache verworfen, Offset nur lesen |

---

## Code

Alle Skripte laufen mit `python -I` und NumPy, deterministisch, im Repo-Stand c1a707d (Aufruf mit dem Repo-Pfad bzw. einem
`befund.npz`). Sie liegen nicht im Repo, nur hier. Die Ausgaben vom 18.10.2026 stehen jeweils darunter.

**`deckel_rand.py`** – Spline- gegen Stufen-Deckel, Anpassung, Reichweite, Profil s 439, Bettflächen (§2.2, §3.1, §4):

```python
# deckel_rand.py - python -I deckel_rand.py <repo>
# 16h-6l offline (Plan-Gelaende p2, Raster 0,5 x 0,25 m): Deckel mit weichem Rand. A Bezug Spline/Stufenspiegel, B Gitter-Anpassung an
# Ferats 6l-Kennzahlen, C Reichweite bei schmalerer Spline, D Plan-Profil s 439, E Bettziel: Lageversatz an Wand/Rand.
import importlib.util, itertools, json, sys, numpy as np
R = sys.argv[1].rstrip('/') + '/recherche/antworten/'
sp = importlib.util.spec_from_file_location('p2b', R + 'skripte/p2_bett/p2_bettplan.py')
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
X = m.rechne(); Z = X['z_neu']; S = np.asarray(X['G']['S']); U = np.asarray(X['G']['U'])
a = np.fromfile(R + 'p2_bett/talkaskade_soll.f32', '<f4').reshape(6, 384, 101); kante, stufe = a[5], a[3]   # stufe = Plan-Spiegel
zon = np.fromfile(R + 'p2_bett/talkaskade_zonen.u8', np.uint8).reshape(384, 101)
J = np.array(json.load(open(R + 'p2_bett/bettplan_p2.json'))['spiegel_je_m']['punkte'])
def cr(s):                                    # Catmull-Rom durch die 1-m-Proben (Naeherung der Editor-Spline, CurveAuto; +5 cm folgt)
    x, y = J[:, 0], J[:, 1]; s = np.clip(s, x[0], x[-1]); i = np.clip(np.searchsorted(x, s) - 1, 1, len(x) - 3); t = s - x[i]
    p0, p1, p2, p3 = y[i - 1], y[i], y[i + 1], y[i + 2]
    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
s1 = cr(S) + 0.05; spl = np.repeat(s1[:, None], 101, 1); SL = np.repeat(np.abs(np.gradient(s1, S))[:, None], 101, 1)
ss, uu = np.meshgrid(S, U, indexing='ij'); bett = np.isin(zon, [1, 2, 3, 4]); aus = ~bett
band = (kante >= 0.25) & (kante <= 2.0) & np.isin(zon, [5, 6, 7])
hoch = band & (Z - spl > 0.15); fl, ra = hoch & (SL < 0.05), hoch & (SL >= 0.25)
pc = lambda v, q: float(np.percentile(v, q))
def box(z, w):
    for ax, hh in ((0, 0.5), (1, 0.25)):
        n = max(1, int(round(w / hh))); n += (n + 1) % 2; k = np.ones(n) / n
        p = np.pad(z, [(n // 2, n // 2) if q == ax else (0, 0) for q in (0, 1)], mode='edge')
        z = np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), ax, p)
    return z
E = np.random.default_rng(6).uniform(-1, 1, Z.shape)
def weich(cap, R_, w=0.0):                     # Deckel bis Kante R_-1 voll, bis R_ linear auslaufend, optional Kastenglaettung
    b = Z + np.clip(R_ - kante, 0, 1) * (np.minimum(Z, cap) - Z)
    return np.where(bett, Z, box(b, w)) if w else b
def kenn(b):
    o, v = (b - spl) * 100, (b - Z) * 100; spn = lambda mk: pc(o[mk], 90) - pc(o[mk], 10)
    sh = lambda lo, hi: 100 * np.mean((b - Z)[aus & (kante >= lo) & (kante < hi)] < -0.10)
    return {'flach': spn(fl), 'rampe': spn(ra), 'gesamt': spn(hoch), 'b1': pc(v[band & (kante < 1)], 50), 'b2': pc(v[band & (kante >= 1)], 50),
            'p10': pc(v[band], 10), 'r05': sh(0.5, 1), 'r20': sh(2, 2.5), 'r30': sh(3, 3.5)}
if __name__ == '__main__':
    print(f'A  hoch-Zellen {hoch.sum()}: flach {100*fl.mean()/hoch.mean():.0f} %, Rampe {100*ra.mean()/hoch.mean():.0f} %; Neigung der Editor-Spline an'
          f' Rampenzellen p10/p50/p90 {pc(SL[ra],10):.2f}/{pc(SL[ra],50):.2f}/{pc(SL[ra],90):.2f} m/m')
    dd = (stufe - spl) * 100
    print(f'   Stufenspiegel - Editor-Spline p10/p50/p90 cm: flach {pc(dd[fl],10):+.0f}/{pc(dd[fl],50):+.0f}/{pc(dd[fl],90):+.0f}, '
          f'Rampe {pc(dd[ra],10):+.0f}/{pc(dd[ra],50):+.0f}/{pc(dd[ra],90):+.0f}')
    for d_ in (0.18, 0.5):
        e = SL[ra] * np.random.default_rng(1).uniform(-d_, d_, ra.sum()) * 100
        print(f'   nur Lagefehler +-{d_} m auf diesen Neigungen: Spanne p90-p10 {pc(e,90)-pc(e,10):.0f} cm (linear 0,35 m/m: {0.8*2*d_*35:.0f} cm)')
    ziel = {'flach': (34.5, 5), 'rampe': (80, 8), 'gesamt': (70.5, 8), 'b1': (-29.8, 5), 'b2': (-82, 8), 'p10': (-121, 10),
            'r05': (72, 8), 'r20': (51, 8), 'r30': (10, 8)}
    print('B  Ziel [Ferat 6l]:', ' '.join(f'{n} {z:+g}' for n, (z, s) in ziel.items()))
    res = []
    for art, R_, w, dj in itertools.product(('Spline', 'Stufe'), (1.5, 2.0, 2.5, 3.0), (0.0, 0.73, 1.10, 1.83), (0.0, 0.25, 0.5, 0.7)):
        if art == 'Stufe' and dj: continue
        cap = cr(np.clip(ss + dj * E, S[0], S[-1])) + 0.08 if art == 'Spline' else stufe + 0.08
        k = kenn(weich(cap, R_, w)); res.append((sum(((k[n] - z) / s) ** 2 for n, (z, s) in ziel.items()), art, R_, w, dj, k))
    res.sort(key=lambda r: r[0])
    for f, art, R_, w, dj, k in res[:3] + [r for r in res if r[1] == 'Stufe'][:1] + [r for r in res if r[4] == 0 and r[1] == 'Spline'][:1]:
        print(f'   chi2 {f:6.1f} {art:6s} R {R_} Glaettung {w:.2f} Lagefehler +-{dj}:', ' '.join(f'{n} {v:+.0f}' for n, v in k.items()))
    print('C  Anteil Boden < Gelaende - 10 cm je Kantenabstand, Spline-Deckel Lagefehler +-0,5 m (gemessen B0 und C: 72 % | 48-55 % bei 2-2,5 | < 15 % ab 3):')
    for R_ in (2.5, 1.75):
        b = weich(cr(np.clip(ss + 0.5 * E, S[0], S[-1])) + 0.08, R_)
        print(f'   R {R_} m:', ' | '.join(f'{lo}-{hi}: {100*np.mean((b-Z)[aus&(kante>=lo)&(kante<hi)]<-0.10):.0f} %'
                                        for lo, hi in ((0.5, 1), (1, 1.5), (1.5, 2), (2, 2.5), (2.5, 3), (3, 3.5))))
    print('D  Plan quer bei s 439 und Stufenspiegel je s (u > 0 links):')
    i = int(np.argmin(np.abs(S - 439.0)))
    for u in (-4.0, -3.0, -2.0, 0.0, 2.0, 3.0, 4.0):
        j = int(np.argmin(np.abs(U - u)))
        print(f'   u {u:+4.1f}: Kante {kante[i,j]:4.2f} Zone {zon[i,j]} Gelaende {Z[i,j]:6.2f} Stufenspiegel {stufe[i,j]:6.3f} Editor-Spline {spl[i,j]:6.2f}')
    for s0 in (438.0, 438.5, 439.0, 439.5):
        i = int(np.argmin(np.abs(S - s0))); q = lambda u: stufe[i, int(np.argmin(np.abs(U - u)))]
        print(f'   s {s0}: Stufenspiegel u -4 {q(-4):.3f} | u 0 {q(0):.3f} | u +4 {q(4):.3f} | Editor-Spline {s1[i]:.3f}')
    print('E  Bettflaeche, an der ein Lageversatz d des Abtastpunkts Grund ueber Spiegel + 13 cm treffen kann:')
    inn = np.zeros(Z.shape)
    for i in range(Z.shape[0]):
        e = np.where(~bett[i])[0]
        for j in np.where(bett[i])[0]:
            inn[i, j] = 0.25 * np.min(np.abs(e - j)) - 0.125
    for d_, rs, ru in ((0.18, 0, 1), (0.5, 1, 2)):
        mx = Z.copy()
        for di, dj in itertools.product(range(-rs, rs + 1), range(-ru, ru + 1)):
            sh = np.full_like(Z, -np.inf); ns, nu = Z.shape
            sh[max(0, di):ns + min(0, di), max(0, dj):nu + min(0, dj)] = Z[max(0, -di):ns + min(0, -di), max(0, -dj):nu + min(0, -dj)]
            mx = np.maximum(mx, sh)
        r = bett & (mx > stufe + 0.12); q = lambda mk: 100 * (r & mk).sum() / bett.sum()
        print(f'   +-{d_} m: {q(bett):4.1f} % des Betts | Zone 1 {q(zon==1):4.1f} Kolk {q(zon==2):3.1f} Krone {q(zon==3):3.1f} Wand/Rampe {q(zon==4):4.1f}'
              f' | Innenabstand < 0,5 m {q(inn<0.5):4.1f}, >= 0,5 m {q(inn>=0.5):4.1f} pp')
    print('   Zonenanteile am Bett: ' + ', '.join(f'{nm} {100*(zon==z).sum()/bett.sum():.1f} %' for nm, z in (('Bett', 1), ('Kolk', 2), ('Krone', 3), ('Wand/Rampe', 4))) +
          f'; Kernbett (Zone 1/2, Innenabstand >= 0,5 m) {100*(bett & np.isin(zon,[1,2]) & (inn>=0.5)).sum()/bett.sum():.1f} %')
```

Ausgabe:
```
A  hoch-Zellen 4365: flach 50 %, Rampe 36 %; Neigung der Editor-Spline an Rampenzellen p10/p50/p90 0.34/0.64/1.27 m/m
   Stufenspiegel - Editor-Spline p10/p50/p90 cm: flach -10/-5/+1, Rampe -56/-2/+92
   nur Lagefehler +-0.18 m auf diesen Neigungen: Spanne p90-p10 21 cm (linear 0,35 m/m: 10 cm)
   nur Lagefehler +-0.5 m auf diesen Neigungen: Spanne p90-p10 57 cm (linear 0,35 m/m: 28 cm)
B  Ziel [Ferat 6l]: flach +34.5 rampe +80 gesamt +70.5 b1 -29.8 b2 -82 p10 -121 r05 +72 r20 +51 r30 +10
   chi2   23.2 Spline R 2.5 Glaettung 0.00 Lagefehler +-0.5: flach +41 rampe +79 gesamt +53 b1 -31 b2 -80 p10 -132 r05 +80 r20 +80 r30 +0
   chi2   25.3 Spline R 2.5 Glaettung 0.00 Lagefehler +-0.7: flach +41 rampe +96 gesamt +57 b1 -31 b2 -79 p10 -132 r05 +80 r20 +80 r30 +0
   chi2   36.0 Spline R 2.5 Glaettung 0.00 Lagefehler +-0.25: flach +41 rampe +57 gesamt +46 b1 -31 b2 -80 p10 -130 r05 +79 r20 +80 r30 +0
   chi2  101.6 Stufe  R 2.5 Glaettung 0.00 Lagefehler +-0.0: flach +50 rampe +139 gesamt +86 b1 -33 b2 -82 p10 -108 r05 +98 r20 +86 r30 +0
   chi2   53.4 Spline R 2.5 Glaettung 1.10 Lagefehler +-0.0: flach +59 rampe +69 gesamt +62 b1 -36 b2 -69 p10 -117 r05 +86 r20 +87 r30 +15
C  Anteil Boden < Gelaende - 10 cm je Kantenabstand, Spline-Deckel Lagefehler +-0,5 m (gemessen B0 und C: 72 % | 48-55 % bei 2-2,5 | < 15 % ab 3):
   R 2.5 m: 0.5-1: 80 % | 1-1.5: 86 % | 1.5-2: 91 % | 2-2.5: 80 % | 2.5-3: 0 % | 3-3.5: 0 %
   R 1.75 m: 0.5-1: 80 % | 1-1.5: 84 % | 1.5-2: 27 % | 2-2.5: 0 % | 2.5-3: 0 % | 3-3.5: 0 %
D  Plan quer bei s 439 und Stufenspiegel je s (u > 0 links):
   u -4.0: Kante 2.26 Zone 7 Gelaende  90.36 Stufenspiegel 88.696 Editor-Spline  89.28
   u -3.0: Kante 1.26 Zone 6 Gelaende  89.78 Stufenspiegel 88.696 Editor-Spline  89.28
   u -2.0: Kante 0.26 Zone 5 Gelaende  88.80 Stufenspiegel 88.696 Editor-Spline  89.28
   u +0.0: Kante 0.00 Zone 1 Gelaende  89.01 Stufenspiegel 89.229 Editor-Spline  89.28
   u +2.0: Kante 0.18 Zone 5 Gelaende  89.46 Stufenspiegel 89.229 Editor-Spline  89.28
   u +3.0: Kante 1.18 Zone 6 Gelaende  90.57 Stufenspiegel 89.581 Editor-Spline  89.28
   u +4.0: Kante 2.18 Zone 7 Gelaende  91.14 Stufenspiegel 89.581 Editor-Spline  89.28
   s 438.0: Stufenspiegel u -4 89.144 | u 0 89.432 | u +4 90.127 | Editor-Spline 89.482
   s 438.5: Stufenspiegel u -4 88.696 | u 0 89.229 | u +4 90.127 | Editor-Spline 89.347
   s 439.0: Stufenspiegel u -4 88.696 | u 0 89.229 | u +4 89.581 | Editor-Spline 89.279
   s 439.5: Stufenspiegel u -4 88.696 | u 0 89.229 | u +4 89.229 | Editor-Spline 89.213
E  Bettflaeche, an der ein Lageversatz d des Abtastpunkts Grund ueber Spiegel + 13 cm treffen kann:
   +-0.18 m:  5.8 % des Betts | Zone 1  1.7 Kolk 0.0 Krone 0.1 Wand/Rampe  4.0 | Innenabstand < 0,5 m  3.8, >= 0,5 m  2.0 pp
   +-0.5 m: 33.9 % des Betts | Zone 1 17.7 Kolk 2.7 Krone 1.7 Wand/Rampe 11.8 | Innenabstand < 0,5 m 18.4, >= 0,5 m 15.6 pp
   Zonenanteile am Bett: Bett 63.1 %, Kolk 10.8 %, Krone 10.8 %, Wand/Rampe 15.3 %; Kernbett (Zone 1/2, Innenabstand >= 0,5 m) 56.9 %
```

Hinweise:
- Die Editor-Spline ist hier aus `spiegel_je_m` + 5 cm genähert (wie 6k). Eure trägt 1-m-Proben aus `spline_z.json` + 5 cm.
- „R“ ist die Kante, bis zu der der Deckel ausläuft (voll bis R − 1 m).
- Der Plan-Gelände-Raster ist nicht `hoehe.f32`; die Rechnung trennt Modelle, sie belegt keinen Mechanismus.

**`deckel_kern.py`** – korrigiertes Kriterium mit Kontrollfällen (§2.3):

```python
# deckel_kern.py - korrigiertes DECKEL-Kriterium (16h-6l), ersetzt "eng <= 15 cm" aus boden_befund.py
#   python -I deckel_kern.py --dump befund.npz [--zelle 1.0]     Felder wie boden_befund.py (boden, gelaende, spline, kante, maske)
#   python -I deckel_kern.py --selbsttest <repo>                 Kontrollfaelle auf dem Plan-Gelaende (Raster 0,5 x 0,25 m)
# Kern = Band (Maske 2/3), Kante 0,25-1,25 m (vor dem Auslauf des Deckels), Gelaende > Spline + 0,30 m.
# Toleranz je Zelle = 10 cm + 0,5 m x Neigung der Spline-Hoehe an der Zelle (Lagefehler 1-m-Raster gegen Sim-Zelle).
# DECKEL-Kern, wenn >= 75 % der Kernzellen innerhalb der Toleranz liegen und |Median(Boden - Spline)| <= 10 cm.
import argparse, json, sys, numpy as np
def kern(boden, gelaende, spline, kante, bandmaske, h):
    gs, gu = np.gradient(spline, *h); neig = np.hypot(gs, gu)
    k = bandmaske & (kante >= 0.25) & (kante <= 1.25) & (gelaende - spline > 0.30)
    d = (boden - spline)[k]; q = float(np.mean(np.abs(d) <= 0.10 + 0.5 * neig[k])); med = 100 * float(np.median(d))
    return {'kernzellen': int(k.sum()), 'in_toleranz_pct': round(100 * q, 1), 'median_boden_minus_spline_cm': round(med, 1),
            'urteil': 'DECKEL-Kern' if q >= 0.75 and abs(med) <= 10 else 'kein DECKEL-Kern'}
def selbsttest(repo):
    import importlib.util
    R = repo.rstrip('/') + '/recherche/antworten/'
    sp = importlib.util.spec_from_file_location('p2b', R + 'skripte/p2_bett/p2_bettplan.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    X = m.rechne(); Z = X['z_neu']; S = np.asarray(X['G']['S'])
    a = np.fromfile(R + 'p2_bett/talkaskade_soll.f32', '<f4').reshape(6, 384, 101); kante, stufe = a[5], a[3]
    zon = np.fromfile(R + 'p2_bett/talkaskade_zonen.u8', np.uint8).reshape(384, 101); bett = np.isin(zon, [1, 2, 3, 4])
    J = np.array(json.load(open(R + 'p2_bett/bettplan_p2.json'))['spiegel_je_m']['punkte'])
    def cr(s):
        x, y = J[:, 0], J[:, 1]; s = np.clip(s, x[0], x[-1]); i = np.clip(np.searchsorted(x, s) - 1, 1, len(x) - 3); t = s - x[i]; p0, p1, p2, p3 = y[i - 1], y[i], y[i + 1], y[i + 2]
        return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
    spl = np.repeat((cr(S) + 0.05)[:, None], 101, 1); ss = np.repeat(S[:, None], 101, 1); bandm = np.isin(zon, [5, 6, 7])
    E = np.random.default_rng(6).uniform(-1, 1, Z.shape)
    def box(z, w):
        for ax, hh in ((0, 0.5), (1, 0.25)):
            n = max(1, int(round(w / hh))); n += (n + 1) % 2; k = np.ones(n) / n
            p = np.pad(z, [(n // 2, n // 2) if q == ax else (0, 0) for q in (0, 1)], mode='edge'); z = np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), ax, p)
        return z
    weich = lambda cap, R_=2.5, w=0.0: (lambda b: np.where(bett, Z, box(b, w)) if w else b)(Z + np.clip(R_ - kante, 0, 1) * (np.minimum(Z, cap) - Z))
    F = {'DECKEL hart, c 3 cm': (np.minimum(Z, spl + 0.03), True),
         'DECKEL weich R 2,5 m, Lagefehler +-0,5 m': (weich(cr(np.clip(ss + 0.5 * E, S[0], S[-1])) + 0.08), True),
         'DECKEL weich R 2,5 m, Lagefehler +-0,7 m': (weich(cr(np.clip(ss + 0.7 * E, S[0], S[-1])) + 0.08), True),
         'DECKEL weich R 3 m, Glaettung 1,83 m': (weich(spl + 0.03, 3.0, 1.83), True),
         'GLAETTUNG 1,83 m': (box(Z, 1.83), False), 'GLAETTUNG 4 m': (box(Z, 4.04), False),
         'ERSATZWERT -1,5 m ab Kante 1 m': (np.where((kante >= 1.0) & ~bett, Z - 1.5, Z), False),
         'BEZUGSHOEHE -0,65 m': (Z - 0.65, False), 'kein Versatz': (Z, False)}
    ok = True
    for nm, (b, soll) in F.items():
        r = kern(b, Z, spl, kante, bandm, (0.5, 0.25)); hit = (r['urteil'] == 'DECKEL-Kern') == soll; ok &= hit
        print(f"{nm:42s} in Toleranz {r['in_toleranz_pct']:5.1f} %  Median {r['median_boden_minus_spline_cm']:+6.1f} cm -> {r['urteil']:16s} {'OK' if hit else 'FALSCH'}")
    r = kern(weich(stufe + 0.08), Z, spl, kante, bandm, (0.5, 0.25))
    print(f"(Info) Deckel auf Stufenspiegel + 8 cm: in Toleranz {r['in_toleranz_pct']} %, {r['urteil']} - das Kriterium trennt Spline- und Stufen-Deckel nicht")
    print('Selbsttest', 'bestanden' if ok else 'NICHT bestanden'); return ok
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--dump'); ap.add_argument('--zelle', type=float, default=1.0); ap.add_argument('--selbsttest'); A = ap.parse_args()
    if A.selbsttest: sys.exit(0 if selbsttest(A.selbsttest) else 1)
    D = dict(np.load(A.dump))
    print(json.dumps(kern(D['boden'], D['gelaende'], D['spline'], D['kante'], np.isin(D['maske'], [2, 3]), (A.zelle, A.zelle)), ensure_ascii=False))
```

Ausgabe `python -I deckel_kern.py --selbsttest <repo>` (Exit 0):
```
DECKEL hart, c 3 cm                        in Toleranz 100.0 %  Median   +3.0 cm -> DECKEL-Kern      OK
DECKEL weich R 2,5 m, Lagefehler +-0,5 m   in Toleranz  97.5 %  Median   +3.0 cm -> DECKEL-Kern      OK
DECKEL weich R 2,5 m, Lagefehler +-0,7 m   in Toleranz  93.0 %  Median   +3.0 cm -> DECKEL-Kern      OK
DECKEL weich R 3 m, Glaettung 1,83 m       in Toleranz  85.7 %  Median   +2.3 cm -> DECKEL-Kern      OK
GLAETTUNG 1,83 m                           in Toleranz  11.8 %  Median  +65.6 cm -> kein DECKEL-Kern OK
GLAETTUNG 4 m                              in Toleranz  12.3 %  Median  +69.4 cm -> kein DECKEL-Kern OK
ERSATZWERT -1,5 m ab Kante 1 m             in Toleranz   9.6 %  Median  +44.0 cm -> kein DECKEL-Kern OK
BEZUGSHOEHE -0,65 m                        in Toleranz  44.4 %  Median   +2.6 cm -> kein DECKEL-Kern OK
kein Versatz                               in Toleranz   5.0 %  Median  +67.6 cm -> kein DECKEL-Kern OK
(Info) Deckel auf Stufenspiegel + 8 cm: in Toleranz 80.0 %, DECKEL-Kern - das Kriterium trennt Spline- und Stufen-Deckel nicht
Selbsttest bestanden
```

Im Welt-1-m-Raster `--zelle 1.0`. Die Neigung kommt aus dem Feld `spline`. Ist `spline` je Zelle auf ganzzahliges s gerundet, vorher auf
stetiges s umstellen; dann schrumpft der Lagefehler aus §2.2 [Ableitung].

**`bett_fehlzellen.py`** – Bett-Fehlzellen aufteilen, mit Kontrolle (§4):

```python
# bett_fehlzellen.py - 16h-6l F3: Bettzellen ohne sichtbar_1 nach Innenabstand, Gelaendeneigung und Kolk aufteilen (Welt-1-m-Raster).
#   python -I bett_fehlzellen.py --dump befund.npz       Felder wie boden_befund.py (boden, gelaende, tiefe, maske, optional kolk)
#   python -I bett_fehlzellen.py --kontrolle <repo>      Plan-Gelaende p2 auf 1 m, Spiegel = Plan-Stufenspiegel + 13 cm (T-b1),
#                                                         einmal ohne und dreimal mit 0,5 m Lageversatz zwischen Wasser und Gelaende
import argparse, json, numpy as np
def aufteilen(D, name=''):
    B = D['maske'] == 1; W = D['boden'] + D['tiefe']; sicht = (D['tiefe'] > 0.001) & (W - D['gelaende'] > 0.01)
    inn = np.zeros(B.shape, int); m = B.copy(); k = 0                   # Innenabstand in Zellen (4er-Nachbarschaft)
    while m.any():
        k += 1; inn[m] = k; p = np.pad(m, 1)
        m = m & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    gy, gx = np.gradient(D['gelaende']); neig = np.hypot(gy, gx)
    kolk = (D['kolk'] >= 0) if 'kolk' in D else np.zeros_like(B); f = B & ~sicht
    q = lambda mk: f'{(B & mk).sum():4d} Zellen, {100*sicht[B & mk].mean():5.1f} %' if (B & mk).any() else '-'
    print(f'{name}Bett {B.sum()}: sichtbar_1 {100*sicht[B].mean():.1f} %, ohne {f.sum()} (trocken {(f & (D["tiefe"] <= 0.001)).sum()})'
          f' | Rand (Innenabstand 1) {q(inn == 1)} | Innenabstand >= 2 {q(inn >= 2)} | Neigung >= 0,5 {q(neig >= 0.5)} | Kolk {q(kolk)}'
          f' | Kernbett (Innenabstand >= 2, Neigung < 0,5) {q((inn >= 2) & (neig < 0.5))}')
def kontrolle(repo):
    import importlib.util
    R = repo.rstrip('/') + '/recherche/antworten/'
    sp = importlib.util.spec_from_file_location('p2b', R + 'skripte/p2_bett/p2_bettplan.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    Z = m.rechne()['z_neu']; a = np.fromfile(R + 'p2_bett/talkaskade_soll.f32', '<f4').reshape(6, 384, 101)
    zon = np.fromfile(R + 'p2_bett/talkaskade_zonen.u8', np.uint8).reshape(384, 101); W0 = a[3] + 0.13
    maske = np.where(np.isin(zon, [1, 2, 3, 4]), 1, np.where(np.isin(zon, [5, 6, 7]), 2, 0)).astype(np.uint8)
    sl = (slice(2, -2, 2), slice(4, -4, 4))                              # 1-m-Raster (0,5 m laengs x 2, 0,25 m quer x 4)
    for nm, (di, dj) in (('ohne Versatz', (0, 0)), ('0,5 m laengs', (1, 0)), ('0,5 m quer', (0, 2)), ('0,5 m diagonal', (1, 2))):
        Ws, Zs = np.roll(W0, (di, dj), (0, 1)), np.roll(Z, (di, dj), (0, 1)); t = np.maximum(Ws - Zs, 0)
        aufteilen({'boden': (Ws - t)[sl], 'tiefe': t[sl], 'gelaende': Z[sl], 'maske': maske[sl], 'kolk': np.where(zon == 2, 0, -1)[sl]}, f'{nm:14s} ')
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--dump'); ap.add_argument('--kontrolle'); A = ap.parse_args()
    kontrolle(A.kontrolle) if A.kontrolle else aufteilen(dict(np.load(A.dump)))
```

Ausgabe `--kontrolle <repo>`:
```
ohne Versatz   Bett 802: sichtbar_1 100.0 %, ohne 0 (trocken 0) | Rand (Innenabstand 1)  384 Zellen, 100.0 % | Innenabstand >= 2  418 Zellen, 100.0 % | Neigung >= 0,5  346 Zellen, 100.0 % | Kolk   96 Zellen, 100.0 % | Kernbett (Innenabstand >= 2, Neigung < 0,5)  282 Zellen, 100.0 %
0,5 m laengs   Bett 802: sichtbar_1 99.0 %, ohne 8 (trocken 8) | Rand (Innenabstand 1)  384 Zellen,  97.9 % | Innenabstand >= 2  418 Zellen, 100.0 % | Neigung >= 0,5  346 Zellen,  97.7 % | Kolk   96 Zellen, 100.0 % | Kernbett (Innenabstand >= 2, Neigung < 0,5)  282 Zellen, 100.0 %
0,5 m quer     Bett 802: sichtbar_1 89.5 %, ohne 84 (trocken 49) | Rand (Innenabstand 1)  384 Zellen,  83.6 % | Innenabstand >= 2  418 Zellen,  95.0 % | Neigung >= 0,5  346 Zellen,  81.8 % | Kolk   96 Zellen,  99.0 % | Kernbett (Innenabstand >= 2, Neigung < 0,5)  282 Zellen,  99.6 %
0,5 m diagonal Bett 802: sichtbar_1 92.5 %, ohne 60 (trocken 60) | Rand (Innenabstand 1)  384 Zellen,  84.4 % | Innenabstand >= 2  418 Zellen, 100.0 % | Neigung >= 0,5  346 Zellen,  88.7 % | Kolk   96 Zellen,  97.9 % | Kernbett (Innenabstand >= 2, Neigung < 0,5)  282 Zellen, 100.0 %
```

**`versatz_pruefen.py`** – Messweg-Kontrolle Halbzellen-Versatz, mit Kontrolle (§2.2, §4):

```python
# versatz_pruefen.py - 16h-6l Messweg-Kontrolle: Liegt der Dump gegen hoehe.f32 um eine halbe Zelle versetzt?
#   python -I versatz_pruefen.py --dump befund.npz        Felder wie boden_befund.py (boden, gelaende, maske, optional kolk)
#   python -I versatz_pruefen.py --kontrolle <repo>       Plan-Gelaende p2 auf 1 m, ohne und mit injiziertem Versatz (+0,5 Spalte)
# Im Bettinneren (ohne Kolke) ist Boden = Gelaende (6l: Median -1,2 cm). Gelaende um (di, dj) halbe Zellen verschieben, kleinstes RMS suchen.
import argparse, numpy as np
def schieb(z, di, dj):                                # bilinear um eine halbe Zelle (Mittel der Nachbarn)
    if di: z = 0.5 * (z + np.roll(z, -int(np.sign(di)), 0))
    if dj: z = 0.5 * (z + np.roll(z, -int(np.sign(dj)), 1))
    return z
def pruefen(D, name=''):
    H = D['gelaende'].astype(float); B = D['maske'] == 1
    inn = B & np.roll(B, 1, 0) & np.roll(B, -1, 0) & np.roll(B, 1, 1) & np.roll(B, -1, 1); inn[[0, -1], :] = False; inn[:, [0, -1]] = False
    if 'kolk' in D: inn &= D['kolk'] < 0
    res = sorted((100 * float(np.sqrt(np.mean((D['boden'] - schieb(H, di, dj))[inn] ** 2))), di, dj) for di in (-0.5, 0, 0.5) for dj in (-0.5, 0, 0.5))
    rms0 = next(r for r, di, dj in res if (di, dj) == (0, 0))
    print(f'{name}bestes RMS {res[0][0]:.1f} cm bei Versatz Zeile {res[0][1]:+.1f} / Spalte {res[0][2]:+.1f} (ohne Versatz {rms0:.1f} cm) ->',
          'kein Halbzellen-Versatz' if res[0][1:] == (0, 0) else 'Versatz: Abtastung angleichen, dann sichtbar_1 und deckel_kern neu')
def kontrolle(repo):
    import importlib.util
    R = repo.rstrip('/') + '/recherche/antworten/'
    sp = importlib.util.spec_from_file_location('p2b', R + 'skripte/p2_bett/p2_bettplan.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    Z = m.rechne()['z_neu']; zon = np.fromfile(R + 'p2_bett/talkaskade_zonen.u8', np.uint8).reshape(384, 101); sl = (slice(2, -2, 2), slice(4, -4, 4))
    H = Z[sl]; maske = np.where(np.isin(zon, [1, 2, 3, 4]), 1, 0)[sl]; kolk = np.where(zon == 2, 0, -1)[sl]
    pruefen({'boden': H, 'gelaende': H, 'maske': maske, 'kolk': kolk}, 'Kontrolle ohne Versatz:      ')
    pruefen({'boden': schieb(H, 0, 0.5), 'gelaende': H, 'maske': maske, 'kolk': kolk}, 'Kontrolle Versatz +0,5 Spalte: ')
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--dump'); ap.add_argument('--kontrolle'); A = ap.parse_args()
    kontrolle(A.kontrolle) if A.kontrolle else pruefen(dict(np.load(A.dump)))
```

Ausgabe `--kontrolle <repo>`:
```
Kontrolle ohne Versatz:      bestes RMS 0.0 cm bei Versatz Zeile +0.0 / Spalte +0.0 (ohne Versatz 0.0 cm) -> kein Halbzellen-Versatz
Kontrolle Versatz +0,5 Spalte: bestes RMS 0.0 cm bei Versatz Zeile +0.0 / Spalte +0.5 (ohne Versatz 17.3 cm) -> Versatz: Abtastung angleichen, dann sichtbar_1 und deckel_kern neu
```

**Schritt 2, Teil 1: nur lesen** (Editor-Python; Namen per `dir()`, Werte mit `try`, nichts setzen):

```python
import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
akt = eas.get_all_level_actors()
swr = next(a for a in akt if isinstance(a, unreal.ShallowWaterRiver) and a.get_actor_label() == 'SWR_Sim_F_ERLENBACH_1V_C2')
c = swr.get_component_by_class(unreal.ShallowWaterRiverComponent)
def zeige(obj, wer, keys):
    for n in sorted(n for n in dir(obj) if any(k in n.lower() for k in keys)):
        try: print(wer, n, obj.get_editor_property(n))
        except Exception as e: print(wer, n, '-', type(e).__name__)
zeige(c, 'SWR', ('contour', 'capture', 'smooth', 'dilat', 'spline', 'water_info', 'render_state'))
for a in akt:
    if isinstance(a, unreal.WaterBodyRiver) and 'ERLENBACH' in a.get_actor_label().upper():
        print('Fluss', a.get_actor_label(), 'Tags', list(a.tags))
        zeige(a.get_component_by_class(unreal.WaterBodyComponent), 'Fluss', ('dilation', 'water_info'))
```

Teil 2 (Umschalten) wie 16a D6: `c.set_editor_property('render_state', unreal.ShallowWaterRenderState.DEBUG_RENDER_BOTTOM_CONTOUR)`.
Danach Level ohne Speichern neu laden.

---

## Was fehlt bis Witcher 4

Messlatte ist die UE5-Techdemo, belegt nur über Presse und Suchauszüge (wie 6e/6k): Wasser mit Körper im Bett, dunkle klare Kolke,
nasse Steine an der Linie, Bewuchs bis ans Wasser, Halden als Fläche aus Fels. Nach Wirkung sortiert:

1. **Wasser sitzt physikalisch richtig im Bett.**
   - Der Deckel ist als Muster bestätigt. Schritt 2 klärt, ob die Simulation auf einer Phantom-Schulter rechnet.
   - Erst danach sind Beckenspiegel, Lippenschatten und Front belastbar. Im Bild ist das Prüfband schon im Ziel (sichtbar_5 14,0 %).
2. **Kantenbewuchs bis an die Wasserlinie** (6e/6j): Kantengras, Moos, Farne. Er verdeckt Filme von 1–5 cm und die Ränder des
   Lippenschattens. Gesetzt wird er nach Schritt 2, weil eine Behebung des Deckels die Wasserlinie verschieben kann.
3. **Tiefe, dunkle Kolke:** Im Bild erfüllt (0,8–1,34 m sichtbar). Offen ist nur der gehobene Simulationsboden in den Kolken; er betrifft
   Strömung und Schaum (Schaum nur an Fällen bleibt Regel).
4. **BAKED_SIM spielfest:** Gepackter Build (T-a3) und Kosten an p2 (T-a1/T-a2) sind offen; BAKED_SIM bleibt fest gespeichert.
5. **Verlässliche Messwege:**
   - Halbzellen-Versatz Dump ↔ Landschaft prüfen (§4).
   - Pixelmessung KF1–KF7 (6j §2). Erst dann Halde und Talkaskade im Bild statt im Grundriss bewerten.
6. **Nasse Steine an der sichtbaren Linie:** `M_EL_Mountain_NL` (**anzulegen**) und die MS2-MIs; Versatz +20 cm passt zu T-b1.
7. Rinnenköpfe an den Bachanfängen, Fall-Effekte nur an Fällen, Licht im Einschnitt (6e/6f/6j §3).

## Quellen

Abruf 18.10.2026.
- **Nicht erreichbar** (je ein Versuch, kein weiterer Zugang):
  - `dev.epicgames.com` (WebFetch: DNS-Fehler ENOTFOUND)
  - `forums.unrealengine.com` (WebFetch: DNS-Fehler ENOTFOUND)
- **Darum** sind alle Epic-Angaben unten **Suchauszüge**. Einen Quelltext-Spiegel der Engine habe ich nicht benutzt.

- [Python: unreal.ShallowWaterRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent)
  – `bottom_contour_capture_offset` (float, lesen/schreiben), ohne Beschreibung und Einheit [Suchauszug].
- [API: UShallowWaterRiverComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent)
  – `BottomContourCaptureOffset`, `BottomContourCollisionDilation` (float), `BottomContourActors`, Header `ShallowWaterRiverActor.h`
  (WaterAdvanced), ohne Beschreibung [Suchauszug].
- [API: UWaterBodyComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterBodyComponent)
  – `ShapeDilation` (float), ohne Beschreibung [Suchauszug].
- [Python: unreal.WaterBodyInfoMeshComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyInfoMeshComponent)
  – Netz, das den Water Body in die Wasser-Info-Textur zeichnet; außerhalb der Wasser-Info-Durchgänge verborgen [Suchauszug]. Für
  Variante 1/2: Das Info-Netz ist in anderen Durchgängen unsichtbar [Ableitung].
- [Forum 2841669: Grid2D_SW_ComputeBottomContour kommt auf NVIDIA-D3D12-Treibern ab 610.88 verdreht heraus](https://forums.unrealengine.com/t/water-niagarafluids-grid2d-sw-computebottomcontour-comes-out-inverted-on-nvidia-d3d12-drivers-610-88-so-shallow-water-sims-stay-dry-driver-miscompile-workaround-inside/2841669)
  – „dry cells hold roughly captureZ + depth instead of the terrain height“, 5.7 [Suchauszug]. Daraus normal: Boden = captureZ − Tiefe,
  Aufnahme von oben [Ableitung]. Unser Bett passt, die Verdrehung liegt bei uns also nicht vor.
- [Forum 2763339: Shallow water plugin not working in 5.8](https://forums.unrealengine.com/t/shallow-water-plugin-not-working-in-5-8/2763339)
  – mit `use_capture` keine Tiefe; ohne ein Rechteck, das die Landschaft ignoriert [Suchauszug, wie 16a].
- Im Repo:
  - 16a §d1 (Aufnahme ganzer Akteure, `managed_show_only_actors`, `DEBUG_RENDER_BOTTOM_CONTOUR`, D6 „jede Änderung startet neu“)
  - 16g-Nachtrag (Spline-Information der SWR aus der Wasser-Info der Zone)
  - 16g-N2 (`r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames` belegt)
  - 14b §2.1 (`shape_dilation`, Standard und `UndergroundDilationDepthOffset` aus früherer Code-Lesung 5.6.1, für 5.8 nicht geprüft)
  - 16f §6 (Collision Dilation, Capture Offset „Standard lassen“)
  - `fluss_sim_regeln.json` (`remove_outside_spline_amount` = Rate für Wasser außerhalb der Spline)
  - 6k (Skripte, Definitionen, B0)

**Nicht belegt bzw. nicht erreichbar:**
- Wie die SWR Aufnahme und Wasser-Info zum Boden verrechnet.
- Bedeutung und Einheit von `bottom_contour_capture_offset`.
- Der Wert von `shape_dilation` am Erlenbach.
- Ob der Viewport-Schalter „Landscape“ in 5.8.3 so heißt.

Schritt 2 liest die Werte und Namen lokal aus. Bei Ergebnis A bzw. bei einem bleibenden Deckel nach 3a sind die Header-Kommentare zu den
Bodenkontur-Feldern aus eurer 5.8.3-Installation der sichere Beleg.

## Rückfragen

Keine, die den nächsten Schritt ändert.
