# Antwort 16h Nachtrag 6m – Der Deckel ist ein Ausgabe-Saum: 3a mit Bildprüfung, Boden aus der Kontur, Kolkhebung vermutlich im Vergleichsraster

Gelesen: recherche/auftraege/16h-nachtrag6m-schritt2-band-b.md @ 99b0bf3963d8dc1729fcf46c0e262abfcf050053 (Commit 5481238)

Stand 18.10.2026. Gesamtauftrag 16h (Erlenbach p2, Talkaskade s 389–580). Bearbeiter: Cloud-Recherche. Bereich: Bodenbefund der SWR p2,
Messdefinition, Kolke. Wasser bleibt lokal unverändert; die nächste Handlung ist ein Speicherlauf (§1).

**Bezug, ebenfalls gelesen (alle Commit 5481238, seither unverändert):**
- `recherche/antworten/16h-nachtrag6l-boden-schritt1.md` @ 68e2f510532a8edb5b921e981f02359c76a30fea (ganz)
- `recherche/antworten/16h-nachtrag6k-t6j-ergebnisse.md` @ bd2ee3191705d425ce7d96a826143f2de3b26667 (ganz)
- `recherche/auftraege/16h-nachtrag6l-boden-schritt1.md` @ 1c84f6b03dfb4401c5ebf4a0924076b322ce028d und
  `recherche/auftraege/16h-nachtrag6k-t6j-ergebnisse.md` @ 1c29f5b8d00bf866f0dd923c37c55bf5fbf11993 (überflogen)
- `recherche/README.md` @ 778d8a7b8ac17fcaceb262ee8b63e46898ff7051 und `recherche/vorlagen/pruefung.md` @ 5daf4a9187ba35288dc4838f9461118e0960d068
- `recherche/antworten/16f-rueckfrage-epic-parameter-lokal.md` @ 2df21f03041f4840d29cb206a62cf9a709ea33da (Zeilen zu Smoothing) und
  `recherche/auftraege/16h-nachtrag6i-baked-sim-tests-stand.md` @ 11c254f0c95defaa25c481ed4047bf7c68625309 (BAKED_SIM nach jedem Bake)

**Kennzeichnung:** [Ferat] eure Messung bzw. Rolle-1-Lesung aus 6m · [Rechnung] von mir mit Repo-Daten gerechnet (Code unten) ·
[Projekt] Befund im Repo · [Suchauszug] nur Suchauszug · [Ableitung] geschlossen, nicht belegt · [zu prüfen] Name/Wert nicht belegt.

## Kurzfazit

1. **Erklärt der Saum alles? – beantwortet: ja, alle fünf Merkmale; offen ist nur, ob der Saum in den Löser zurückwirkt.**
   Der „Deckel“ ist kein Boden, sondern R − G auf trockenen Zellen, in die das Programm Nachbarspiegel und gemittelte Tiefe schreibt (§2).
   Unsere Mechanismus-Kandidaten D1 (Wasser-Info-Deckel), Variante 2 und die Phantom-Schulter aus 6k §2.5 sind damit **überholt**.
2. **F1 3a – beantwortet: einverstanden**, mit drei Ergänzungen: Hydraulik-Kriterium (wirkt der Saum zurück?), Vorher/Nachher-Bilder in
   BAKED_SIM an drei festen Kameras, und keine neue Konturlesung (der Boden hängt laut Programm nicht an `smoothing_width`). Erwartet:
   Saum schrumpft auf ≤ 2 Zellen, Hydraulik gleich, Ufer im Bild treppig (§1).
3. **F2 Boden aus der Kontur – beantwortet: ja.** Boden = Kontur, einmal je Bodenkonfiguration gelesen. „Nass“ allein über G reicht
   **nicht**, weil der Saum G > 0 trägt; neu: `nass_sim` = G > 1 mm **und** W − G = Kontur ± 5 cm. „Sichtbar“ bleibt gegen `hoehe.f32` (§3).
4. **F3 Kolke +10 cm – wartet auf Beleg (Kontur gegen Landschaft an Texelmitten).** Die Zahl passt zur O2-Beobachtung, aber vermutlich nicht
   als Hebung in der Simulation: Ein Vergleich im 1-m-Raster hebt Mulden im Modell um +10,7 bis +15,8 cm (51–69 % > +10 cm), ohne Bett und
   Band im Median zu verschieben [Rechnung]. Für das Bild ist es unerheblich, denn die sichtbare Kolktiefe misst W − H und ist erfüllt (§4).
5. **Ortsabweichung R1–R5 – beantwortet: angenommen.** Sie schwächt nur den Einzelwert der Uferlatte. Band B trägt die Flächenauswertung
   (§5).
6. **Eigene Fehler korrigiert (§6):** Unter anderem haben wir D3 in 6l mit falscher Begründung zurückgestuft, und die Deckel-Kern-Vorhersage
   (≥ 75 %) ist gescheitert (57 %).

**Nächste Handlung (genau eine, im Editor, nur im Speicher, ≈ 45 min): Test T6M3A = Schritt 3a, `smoothing_width` 1 ab Reset wie B2, mit
Bake, Dump und Bildern in BAKED_SIM.** Ablauf, Vorhersage und Entscheidung stehen in §1.
- **Erfolgskriterium:** stabil und gültig zurückgesetzt; das Ergebnis fällt in E1–E4 (§1.3).
- **Abbruch:** nach 25 min nicht stabil, oder der Rückweg zeigt nicht wieder `smoothing_width` 5 und BAKED_SIM.

---

## 1. F1: Test 3a (T6M3A)

### 1.1 Ablauf

Ausgangsstand wie gespeichert: ganze SWR, Zelle 36,7 cm, Nachfüllen 0,3, Band Bett + 2 m, BAKED_SIM, `smoothing_width` 5.
Jede Eigenschaftsänderung setzt zurück (B0), das Umschalten auf LIVE_SIM ebenso (6m). Deshalb gilt diese Reihenfolge:

1. **Nur lesen:**
   - `smoothing_width`, `render_state` und den Glättungs-Cutoff (C++ `SmoothingCutoff` [Suchauszug], Python-Name per `dir()` [zu prüfen]);
   - im Niagara-Bauteil der SWR den Benutzerparameter für die Glättungsbreite (Name [zu prüfen]). 16f nennt eine zweite „Smoothing Width“
     im System; ändern nur über die SWR-Eigenschaft.
2. **Vorher-Bilder in BAKED_SIM** (gespeicherter Bake, kein Reset nötig), Kamera und Licht festhalten:
   - K1 flaches Ufer s 506,5 schräg von oben, 3–4 m Abstand (Ort von Schritt 2);
   - K2 eine Lippe mit Fall und Schaum;
   - K3 ein Becken mit Ufer, 15–20 m Überblick.
3. `render_state` = LIVE_SIM und `smoothing_width` = 1 setzen. Die Laufzeit zählt ab der letzten Änderung.
4. Lauf bis stabil wie B2, dann Bake und Dump (RGBA16F) als T6M3A_1.
5. `render_state` = BAKED_SIM setzen (Regel 6i nach jedem Bake), dann Nachher-Bilder K1–K3 mit denselben Kameras.
6. Level ohne Speichern neu laden. Prüfen: `smoothing_width` 5, BAKED_SIM, und K1 gleicht dem Vorher-Bild. Speicherstatus wie in 6m melden.

**Keine Konturlesung in 3a.** Laut Programm ist der Boden max(Akteur-, Landschaftsaufnahme); `smoothing_width` geht nicht ein [Ferat].
Die Kontur aus Schritt 2 gilt deshalb als Boden auch für T6M3A. Neu gelesen wird sie nur bei E3 (§1.3), in einem eigenen Durchgang.

### 1.2 Vorhersage (vorab, [Ableitung] aus der Rolle-1-Lesung)

Auswertung im nativen Raster mit dem Boden F aus der Kontur (§3). Die Saumzelle ist definiert als G > 1 mm und |W − G − F| > 5 cm.
Der Abstand n zählt in Zellen zur nächsten `nass_sim`-Zelle.

| Größe | Basis (Breite 5) | Erwartung Breite 1 | Lesart, wenn verfehlt |
|---|---|---|---|
| Saumzellen bei n = 3…6 | ≥ 50 % (Rolle 1: Nachbarspiegel 3–6 Zellen hinter der Kante) | ≤ 10 % | Reichweite hängt nicht an der Breite |
| Welt-1-m: Band 0,25–2 m, Dump-Boden − Gelände, Median | −62,3 cm | −20 … 0 cm | wie oben |
| Welt-1-m: „gedeckelt“ (< Gelände − 10 cm) bei Kante 2–2,5 m | 48–55 % | ≤ 15 % | wie oben |
| **Hydraulik:** Front, Bett `nass_sim`, W an den 24 tiefsten Kolkpunkten | 788 m, 100 %, – | 788 m ± 2 m, ≥ 97 %, Median |ΔW| ≤ 2 cm, kein Kolk > 5 cm | Saum wirkt in den Löser zurück |
| Kernbett sichtbar_1, Kolktiefe sichtbar | Ziel erfüllt | ± 1 pp, 24/24 ≥ 0,8 m | wie Hydraulik |
| Band sichtbar_5 (Bild-Definition §3) | 14,0 % | ± 1 pp | Saum trägt sichtbares Wasser > 5 cm |
| Band sichtbar_1/2 | 15,9 / 15,3 % | sinkt um 0–2 pp (Filme 1–5 cm, 6k §3.2) | – |

Die 2 cm bei ΔW entsprechen der Half-Float-Stufe von R bei |R| 20–41 m (16g-N2).

**Erwartung im sichtbaren Wasser** [Ableitung; der Bake enthält die Saumwerte, BAKED_SIM zeigt also dasselbe wie live]:
- **Uferlinie:** Der Saum gibt der Darstellung hinter der nassen Kante eine glatte Fläche, die das Gelände schneidet. So entsteht die
  Wasserlinie als Schnitt statt als Zellrand. Mit Breite 1 endet die Fläche nach 1–2 Zellen.
  - Erwartet ist eine treppige Linie im 0,367-m-Takt, vor allem an flachen Ufern (K1).
  - An steilen Ufern können Spalten oder dunkle Schlitze zwischen Wasserrand und Böschung entstehen.
  - Das passt zur Epic-Regel „Smoothing bei Treppen-Artefakten erhöhen“ [Epic lokal, 16f].
- **Weicher Rand:** Ob die Darstellung zum Rand hin über G ausblendet, ist nicht belegt [zu prüfen]. Wenn ja, wird der Übergang
  schmaler und härter.
- **Schaum an Lippen (K2):** Fälle liegen in nassen Zellen; der Schaum selbst sollte bleiben. Am seitlichen Ende der Lippe kann er an
  der Treppenkante abgeschnitten wirken. Unsere Regel „Schaum nur an Fällen“ bleibt davon unberührt.
- **Kolke (K3):** Die Fläche über dem Becken bleibt; nur der Uferring ändert sich.

### 1.3 Entscheidung je Ergebnis (vorab)

| Ergebnis | Bedeutung | Entscheidung |
|---|---|---|
| **E1:** Saum schrumpft wie vorhergesagt, Hydraulik in Toleranz | Der Deckel ist reine Ausgabe; die Simulation ist gesund | Deckel geschlossen. `smoothing_width` bleibt 5 (gespeichert ohnehin). Messdefinition §3 gilt. Wirkt Breite 1 im Bild besser (unerwartet), entscheidet Ferat über einen eigenen Lauf mit Vergleichsstellen |
| **E2:** Saum schrumpft, Hydraulik verschiebt sich | Der Saum wirkt in den Löser zurück | trotzdem 5. Vermerk: Alle sichtbar-Ziele gelten nur für Breite 5. Rolle 1 liest nach, wohin die Saumwerte geschrieben werden |
| **E3:** Muster unverändert ± 3 cm, Parameter angekommen (Niagara-Wert 1 oder treppige Ränder im Bild) | Die Reichweite kommt nicht aus der Glättungsbreite | Rolle 1 liest im Programm nach weiteren Schreibzugriffen auf trockene Zellen (auch Cutoff). Danach Kontur bei Breite 1 in eigenem Durchgang. Kein weiterer Editorlauf vorher |
| **E4:** unverändert, Parameter nicht angekommen | Messweg ungültig | Parameterweg zur Niagara-Kopie klären, einmal wiederholen |

**Abbruch:** Ist der Lauf nach 25 min nicht stabil (zwei Messungen im Abstand von 3 min unterscheiden sich um > 1 pp), Level neu laden
und „nicht stabil“ melden. Fallen Front oder Bett unter die Grenzen, ist das kein Abbruch, sondern das Ergebnis E2.

---

## 2. Bewertung des Rolle-1-Befunds: Was der Saum erklärt

Saummodell [Ferat, Rolle 1]: Trockene Zelle bis etwa 5–6 Zellen hinter der nassen Kante: W = Mittel der nassen bzw. schon gefüllten
Nachbarn (+1…+4 cm), G = gemittelte Tiefe, nach außen auf 0 fallend. Ab etwa 7 Zellen gilt W = Gelände und G = 0.
Unser „Boden“ R + Akteurhöhe − G ist dort W_Nachbar − G_Mittel.

| Merkmal (6k/6l) | Saummodell | Urteil |
|---|---|---|
| **Höhe:** Boden ≈ Spline + 2…4 cm, G im Band 11/12/7/2 cm nach außen fallend | Nachbarspiegel = Beckenspiegel ≈ Spline + 13–16 cm (T-b1), abzüglich G ≈ 7–12 cm, ergibt Spline + 1…+9 cm; außen G → 0, also Boden → Nachbarspiegel | erklärt |
| **Weicher Rand,** Übergang über 1–2 m | G fällt über die Ringe ab, W mischt mit Gelände-Nachbarn | erklärt |
| **Reichweite** ≈ 3 m ab Plan-Bettkante, gleich bei Bett + 0,5 m und + 2 m (T6j-C) | gezählt ab der nassen Kante: 5–6 Zellen ≈ 1,8–2,2 m plus 0,3–1 m nasses Band; die Spline-Breite geht nicht ein | erklärt (D1 scheiterte genau hier) |
| **Band B:** Kontur auf dem Gelände (+7,9 cm), Fläche −0,7 cm | Saum entsteht nach dem Schritt, nicht im Eingang | erklärt |
| **Rampenstreuung** 78–82 cm, Rest 45 cm, Zellen auf Stufenspiegel bei s 439 | Nachbarn liegen bis 1,8 m längs entfernt. Auf Rampen (0,64 m/m) mischt der Saum Spiegel ober- und unterhalb; bei s 439 übernimmt er den oberen Beckenspiegel (90,11 m) | erklärt; unser „Lagefehler ±0,5 m“ war ein Stellvertreter dafür [Ableitung] |
| **Deckel-Kern 57,1 / 56,2 %** (vorhergesagt ≥ 75 %) | Der Saum folgt dem **simulierten** Spiegel der Nachbarn (Becken, Fälle), nicht der Editor-Spline. Ein Kriterium „Boden − Spline ≤ 10 cm + 0,5 m × Neigung“ trifft deshalb nur die flachen Becken | erklärt; das Kriterium wird nicht mehr gebraucht |
| **Bett −1,2 cm, Kolke** | nasse Zellen, kein Saum | unberührt; die Kolke brauchen ihre eigene Erklärung (§4) |

**Offen** [zu prüfen, Rolle 1 im schon gelesenen Programm, kein eigener Schritt]: Werden die Saumwerte nur in den Ausgabekanal bzw. Bake
geschrieben oder auch in den Zustand des nächsten Schritts? Ab welcher Tiefe gilt eine Zelle als trocken? Was tut der Cutoff?
T6M3A beantwortet die erste Frage empirisch über das Hydraulik-Kriterium.

**Was `SmoothingWidth` tut:** laut Programm die Reichweite (in Zellen) der Saum-Extrapolation in trockene Zellen [Ferat]. Das passt zur
Epic-Beschreibung „Glättung der Oberflächen-Verschiebung an harten Kanten“ (16f).
- Unsere 6k-Hypothese S „Glättung des **Bodens**“ hatten wir schon selbst rechnerisch widerlegt: Band-Median ≈ 0 statt −65 cm, alle
  24 Kolke gehoben (6k §2.3). Der Befund bestätigt das.
- Falsch war in 6k die Erwartung, 3a teste eine Glättung der gebackenen Ausgabe. 3a testet die Reichweite des Saums.

---

## 3. F2: Messdefinition ab jetzt

| Größe | Definition | Zweck |
|---|---|---|
| **Boden F** | Render-Target in `DEBUG_RENDER_BOTTOM_CONTOUR`, natives Sim-Raster, einmal je Bodenkonfiguration (Landschaft, Hindernisliste bzw. Tags, Aufnahme-Felder, Zellgröße, Akteurlage). Nicht neu bei Nachfüllen oder Glättung | ersetzt R − G |
| **nass_sim** | G > 0,001 m **und** |W − G − F| ≤ 5 cm, mit W = R + Akteurhöhe | Gesundheitsgrenze Bett ≥ 97 %, Front, Hydraulik |
| **Saum** | G > 0,001 m und |W − G − F| > 5 cm | Diagnose, nie als Wasser zählen |
| **sichtbar_x (Bild)** | G > 0,001 ∧ W − H > x, mit H = `hoehe.f32` | Zielmaß Band, Bett, Kolke (wie 6k §3.1), denn der Bake zeichnet auch den Saum |
| **sichtbar_x (Sim)** | nass_sim ∧ W − H > x | Meldewert; die Differenz zum Bild-Wert ist der Saumanteil |
| Kolktiefe sichtbar | W − H am tiefsten Landschaftspunkt | unverändert |

- **Lesen der Kontur:** Das Umschalten setzt zurück. Deshalb nie in einem Lauf, der gebacken werden soll. Eigener Durchgang: umschalten,
  lesen, Level ohne Speichern neu laden. Ablage als Kontur-ID mit Ausgangsstand-ID; die Kontur aus Schritt 2 ist die erste.
- **Raster:** Kontur und Dump im selben nativen Raster vergleichen (euer Leseweg ist gegen den Bake-Dump geprüft). Auf das
  Welt-1-m-Raster erst für `sichtbar` gehen. Wie ihr Texel auf 1 m abbildet (nächster, bilinear, Mittel), bitte mitmelden; das ist der
  Kern von §4.
- **Kontrollfall** (`pruefung.md` „Wassertiefe/Uferband“; Sollwerte von Hand, Toleranz 0 Zellen):

  | Zelle | F | H | W | G | Soll |
  |---|---|---|---|---|---|
  | KB1 Bett | 10,00 | 10,00 | 10,30 | 0,30 | nass_sim, sichtbar_5 Bild und Sim |
  | KB2 Saum am Hang | 10,80 | 10,80 | 10,22 | 0,08 | Saum, nicht sichtbar |
  | KB3 Saum flach | 10,10 | 10,10 | 10,16 | 0,12 | Saum; sichtbar_5 Bild ja, Sim nein |
  | KB4 trocken | 11,00 | 11,00 | 11,00 | 0 | trocken |
  | KB5 Kolk gehoben | 9,10 | 9,00 | 10,10 | 1,00 | nass_sim, Kolktiefe 1,10 m |
  | KB6 Half-Float-Stufe | 10,00 | 10,00 | 10,31 | 0,30 | nass_sim (Abweichung 1 cm) |

  Soll: nass_sim 3, Saum 2, trocken 1; sichtbar_5 Bild 4, Sim 3.
- **Grenze der Definition:** Ein Saum, dessen W − G zufällig auf F ± 5 cm fällt, zählt als nass. Solche Zellen liegen an der Wasserlinie mit
  W − H von wenigen cm; für sichtbar_5 ist das unerheblich [Ableitung].
- **Projektprobe F gegen das echte Gelände:**
  - Kontrollfall bestanden: Bettlatte (Median −1,0 cm, 71,7 % in ± 10 cm) und Uferlatte (+7,9 cm) [Ferat].
  - Toleranz ab jetzt, vorab: flache Kernbettzellen (Neigung < 0,2 m/m, Innenabstand ≥ 2) mit Median |F − H| ≤ 3 cm und ≥ 90 % in ± 10 cm.
    Für Wände und Rampen gilt 10 cm + 0,18 m × Neigung.
  - Die 71,7 % im ganzen Bett schließen Wände ein (Planneigung p50 1,6 m/m); dort erzeugt schon ein halber Texel ± 29 cm [Rechnung, 6l].
  - Verfehlt das flache Kernbett die Toleranz: `versatz_pruefen.py` (6l) mit F als `boden` laufen lassen, bevor eine F − H-Zahl verwendet
    wird.

---

## 4. F3: Kolke +10 cm

**Passt das zu O2?**
- Zur Beobachtung ja: Der Dump zählte 20/24 Kolke „hoch“ (Median der 1-m-Zellen). Die Kontur zeigt median +10,0 cm, 50,7 % > +10 cm.
  Pools sind nass, ein Saum liegt dort nicht vor; Dump und Kontur messen also denselben Boden [Ableitung].
- Zur Deutung „Simulation sieht gehobene Kolke“ noch nicht. Die gleiche Signatur entsteht beim Vergleich im 1-m-Raster: Mittelung oder
  Lageversatz hebt Mulden um ½ · Krümmung · Varianz und senkt Kuppen. Ebene Hänge bleiben im Median, streuen aber beidseitig.
- Die O2-Korrelation (r −0,52/−0,47, schmale Kolke stärker gehoben) passt dazu, denn die Krümmung wächst mit Tiefe/Breite².

**Modellrechnung** [Rechnung, `kolk_hebung.py`, Plan-Gelände, Vergleich im Welt-1-m-Raster; Beträge nur als Größenordnung, weil das Plan-Gelände
nicht `hoehe.f32` ist]:

| Modell | Kolk Median | Kolk > +10 cm | Krone | flaches Bett | Band Median | Band < −10 cm |
|---|---|---|---|---|---|---|
| **gemessen Kontur** [Ferat] | **+10,0** | **50,7 %** | – | −1,0 (Bett) | **−0,7** | **21,7 %** |
| Kastenmittel 1 m (Texel → 1 m gemittelt) | +15,8 | 68,8 % | −14,8 | +0,7 | 0,0 | 22,2 % |
| Lageversatz ± 0,5 m | +10,7 | 51,0 % | −2,5 | +0,3 | 0,0 | 36,8 % |
| Lageversatz ± 0,18 m (halber Texel) | 0,0 | 21,9 % | 0,0 | 0,0 | 0,0 | 12,0 % |
| Landschafts-LOD 2 m | +38,7 | 66,7 % | −33,0 | +0,3 | 0,0 | 25,5 % |
| Landschafts-LOD 4 m | +91,5 | 89,6 % | −4,9 | **+27,3** | +10,5 | 26,6 % |
| 3×3-Maximum (Dilatation der ganzen Kontur) | +40,2 | 100 % | +5,6 | +4,4 | **+27,8** | 0 % |

Werte in cm. Lesart:
- **Ausgeschlossen:** Dilatation der Landschaft (`BottomContourCollisionDilation` [Suchauszug] wirkt laut 16f auf Hindernisse) und ein
  globaler Aufnahme-Offset. Beide würden Band bzw. Bett heben; gemessen sind −0,7 bzw. −1,0 cm.
- **Ebenso ausgeschlossen:** grobe LOD (≥ 4 m).
- **Möglich bleiben** Umtasten bzw. Versatz im Vergleich (unser Messweg), LOD um 2 m und die Akteur-Aufnahme. Die Akteur-Aufnahme ist
  wenig wahrscheinlich: Nur 3 Kolke berühren einen Grundriss (6l).
- Der Fußabdruck einer 0,367-m-Zelle selbst hebt einen Kolk nur um ≈ 2–4 cm (½ · 2–4 m⁻¹ · 0,367²/12 je Achse) [Ableitung].

**Unterscheidender Test** (offline plus reiner Lesetest, läuft mit der T6M3A-Auswertung, kein eigener Schritt, kein Reset):
- Landschaft an den **Texelmitten** der Kontur lesen, wie euer Lesetest 6l §4 (`sample_landscape_heights`, dort 2 118 Punkte).
  Für alle Kolk-, Kronen- und flachen Bettzellen gilt dann F − Landschaft(Texelmitte), getrennt nach „unter Hindernis-Grundriss“ ja/nein.

| Befund | Ursache | Folge |
|---|---|---|
| Kolke ≤ +3 cm, Kronen ≈ 0 | Vergleichsraster (unser Messweg) | O2 geschlossen; Kolkwerte nur noch in Texelmitten |
| Kolke weiter ≈ +10 cm, Kronen < −10 cm, Muster im 2-m-Takt der Landschaftsscheitel | Landschafts-LOD in der Aufnahme | als Befund ablegen; Hebel nur mit Bildgrund prüfen |
| Hebung nur unter Grundrissen | Akteur-Aufnahme | betroffene Teile einzeln ansehen |

**Visuell unerheblich:** Gezeichnet wird W über dem echten Gelände; die sichtbare Kolktiefe (0,8–1,34 m, 24/24) ist schon gegen
`hoehe.f32` gemessen. Den Beckenspiegel setzt die Lippenkrone, nicht der Kolkboden. Selbst eine echte Hebung um 10 cm verkleinert nur das
Volumen und beschleunigt die Strömung im Kolk ein wenig; Schaum ist dort nach Regel aus. Deshalb kein eigener Editorlauf für Kolke.

---

## 5. Ortsabweichung R1–R5

**Angenommen.** Die Stelle erfüllt nach euren Angaben R1 (Spline + 5,7 cm), R3 (Kante 1,43 m), R4 (1,18 m), R6 (Bettlatte) und R2 bis
auf ± 0,5 m (flach von s 504 bis 509). Verletzt ist nur R5 (Stein diagonal 1,41 m).
- **Was es schwächt:** den Einzelwert +7,9 cm als lokalen Beleg. Ein gedehnter Hindernis-Grundriss könnte die Kontur an der Latte heben
  und eine tiefere Landschaftsaufnahme verdecken [Ableitung].
- **Warum das Urteil trotzdem trägt:** Ein Stein ergäbe Steinhöhe, nicht Gelände + 8 cm. Vor allem liegt die Fläche ohne Hindernisse bei
  −0,7 cm (Band A hätte ≈ 80 % unter −10 cm gezeigt, gemessen 21,7 %). Dazu kommt das Bild „Debug ohne Instanzen“.

---

## 6. Korrekturen an eigenen Antworten

| Antwort | Aussage | Korrektur |
|---|---|---|
| 6k Kurzfazit 1, §2.3–§2.4 | „Simulationsboden ≈ min(Gelände; Spline + c)“, Deckel als Bodenmodell | R − G ist auf trockenen Zellen kein Boden. Der „Deckel“ ist der Saum der Ausgabe; die Simulation rechnet auf dem echten Gelände (Band B) |
| 6k §2.1, §3.1 | „G ist im Band großteils Wasser unter dem Gelände“; „verdeckt = Phantomwasser“ | Es ist gemittelte Saumtiefe, kein Wasser. „Verdeckt“ heißt jetzt Saum (§3) |
| 6k §2.5 | Phantom-Schulter, Boden-Trick und Kantenbewuchs warten auf Schritt 2 | Phantom-Schulter entfällt. Kantenbewuchs ist nicht mehr blockiert; der Boden-Trick nur mit eigenem Testgrund |
| 6k §2.6 3a | 3a prüft „D3 über die Glättung der Ausgabe“ | 3a prüft die Reichweite der Saum-Extrapolation (§2) |
| 6l Kurzfazit 1, §2.4 | D1 (Wasser-Info-Deckel) bester Kandidat | **überholt** durch Band B und die Programmlesung, ebenso Variante 2 |
| 6l §2.4 Nr. 6 | D3 „nachrangig“, weil eine Simulation G ≈ 0,1 m auf 35°-Hängen nicht hält | Die Physik war richtig, der Schluss falsch: Das Programm schreibt G dort jeden Schritt neu. Wir hätten „Ausgabe schreibt trockene Zellen“ prüfen müssen |
| 6l §2.2 | ± 0,5 m Lagefehler „vermutlich unser Messweg“ | wahrscheinlich die Längsmischung des Saums auf Rampen [Ableitung]; `versatz_pruefen.py` bleibt nur als Prüfung für F gegen H |
| 6l §2.3 | Deckel-Kern-Vorhersage ≥ 75 % (Modell 97,5 %) | gescheitert (57 %). Das Kriterium setzte die Spline als Deckelhöhe voraus; es wird zurückgezogen |
| 6l §4, 6k §2.6 | Bett „nass ≥ 97 %“ über G > 0,001 | Der Saum kann trockene Bettflecken bis 5 Zellen als nass zeigen. Grenze ab jetzt über `nass_sim` |

---

## Code

**`kolk_hebung.py`** – python -I, NumPy, deterministisch, Repo-Stand 5481238 (nicht im Repo, nur hier):

```python
# kolk_hebung.py - python -I kolk_hebung.py <repo>
# 16h-6m F3 offline: Welche Abtast-/Aufnahmeart hebt Kolke um ~+10 cm, ohne Bett und Band im Median zu verschieben?
# Grundlage Plan-Gelaende p2 (z_neu aus p2_bettplan.py), Raster 0,5 m (s) x 0,25 m (u); Vergleich im Welt-1-m-Raster.
import importlib.util, sys, numpy as np
from numpy.lib.stride_tricks import sliding_window_view as sw
R = sys.argv[1].rstrip('/') + '/recherche/antworten/'
sp = importlib.util.spec_from_file_location('p2b', R + 'skripte/p2_bett/p2_bettplan.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
Z = m.rechne()['z_neu']
zon = np.fromfile(R + 'p2_bett/talkaskade_zonen.u8', np.uint8).reshape(384, 101)
kante = np.fromfile(R + 'p2_bett/talkaskade_soll.f32', '<f4').reshape(6, 384, 101)[5]
hs, hu = 0.5, 0.25
def box(z, w):                       # Kastenmittel ueber w x w Meter
    ns = max(1, int(round(w / hs))); nu = max(1, int(round(w / hu))); ns += (ns + 1) % 2; nu += (nu + 1) % 2
    return sw(np.pad(z, ((ns // 2,), (nu // 2,)), mode='edge'), (ns, nu)).mean(axis=(2, 3))
def lod(z, step):                    # Scheitel alle step Meter, dazwischen bilinear (Landschafts-LOD-Naeherung)
    ks, ku = int(step / hs), int(step / hu); S = np.arange(z.shape[0]); U = np.arange(z.shape[1])
    si, ui = S[::ks], U[::ku]; v = z[np.ix_(si, ui)]; out = np.empty_like(z)
    for i in S:
        k = min(np.searchsorted(si, i, 'right') - 1, len(si) - 2); t = (i - si[k]) / ks
        out[i] = np.interp(U, ui, (1 - t) * v[k] + t * v[k + 1])
    return out
rng = np.random.default_rng(3)
def jit(z, d):                       # Lagefehler gleichverteilt +-d (s und u), naechster Rasterpunkt
    di = np.rint(rng.uniform(-d, d, z.shape) / hs).astype(int); dj = np.rint(rng.uniform(-d, d, z.shape) / hu).astype(int)
    I, J = np.indices(z.shape); return z[np.clip(I + di, 0, z.shape[0] - 1), np.clip(J + dj, 0, z.shape[1] - 1)]
neig = np.hypot(*np.gradient(Z, hs, hu)); sel = (slice(None, None, 2), slice(None, None, 4))   # Welt-1-m-Raster
Z1, zon1, k1, n1 = Z[sel], zon[sel], kante[sel], neig[sel]
kolk = zon1 == 2; krone = zon1 == 3; flachbett = (zon1 == 1) & (n1 < 0.2); band = np.isin(zon1, [5, 6, 7]) & (k1 >= 0.25) & (k1 <= 2)
modelle = {'Kasten 1,0 m (Umtasten Texel->1 m)': box(Z, 1.0)[sel], 'Lagefehler +-0,18 m': jit(Z, 0.18)[sel],
           'Lagefehler +-0,5 m': jit(Z, 0.5)[sel], 'LOD 2 m (Scheitel alle 2 m)': lod(Z, 2.0)[sel], 'LOD 4 m': lod(Z, 4.0)[sel],
           'Max-Dilatation 3x3 (0,5 x 0,25 m)': sw(np.pad(Z, ((1,), (1,)), mode='edge'), (3, 3)).max(axis=(2, 3))[sel]}
print(f'Kolkzellen 1 m: {kolk.sum()}, Kronen {krone.sum()}, flaches Bett {flachbett.sum()}, Band {band.sum()}')
for nm, b in modelle.items():
    d = (b - Z1) * 100
    print(f'{nm:40s} Kolk {np.median(d[kolk]):+6.1f} ({100*np.mean(d[kolk]>10):5.1f} % > +10) Krone {np.median(d[krone]):+6.1f}'
          f' Bett flach {np.median(d[flachbett]):+5.1f} Band {np.median(d[band]):+5.1f} (< -10: {100*np.mean(d[band]<-10):4.1f} %)')
```

Ausgabe vom 18.10.2026 (Zahlen wie in der Tabelle §4, Kolk 96, Kronen 99, flaches Bett 293, Band 685 Zellen im 1-m-Raster).
Grenze: Das Plan-Gelände ist nicht `hoehe.f32`, und Kastenmittel unter 0,5 m löst das Planraster nicht auf.

---

## Was fehlt bis Witcher 4

Messlatte ist die UE5-Techdemo, belegt nur über Presse und Suchauszüge (wie 6e/6k/6l). Nach Wirkung sortiert:

1. **Kantenbewuchs bis an die Wasserlinie** (Kantengras, Moos, Farne). Er ist jetzt nicht mehr durch den Deckel blockiert, denn die
   Wasserlinie verschiebt sich nicht durch eine Behebung. Er verdeckt Filme von 1–5 cm, Lippenschatten-Ränder und eine treppige Saumkante.
2. **Saubere Uferlinie im Bild:** T6M3A zeigt, was der Saum leistet. Bleibt bei Breite 5 eine sichtbare Treppe oder ein Spalt (K1/K3),
   ist das der nächste Darstellungshebel, vor jeder Dekoration.
3. **Nasse Steine an der sichtbaren Linie:** `M_EL_Mountain_NL` (**anzulegen**) und die MS2-MIs; Versatz +20 cm passt zu T-b1.
4. **BAKED_SIM spielfest:** gepackter Build (T-a3) und Kosten an p2 (T-a1/T-a2) offen; BAKED_SIM bleibt fest gespeichert.
5. **Verlässliche Messwege:** Boden aus der Kontur, `nass_sim` (§3), Kolkvergleich an Texelmitten (§4), Pixelmessung KF1–KF7 (6j §2).
6. **Tiefe, dunkle Kolke:** im Bild erfüllt; die +10 cm sind Diagnose ohne Bildwirkung.
7. Rinnenköpfe an den Bachanfängen, Fall-Effekte nur an Fällen, Licht im Einschnitt (6e/6f/6j §3).

## Quellen

Abruf 18.10.2026.
- Websuche „Unreal Engine shallow water river Smoothing Width dry cells extrapolate“: kein Treffer zur Glättungsbreite oder zu trockenen
  Zellen [Suchauszug]; keine weiteren Versuche. Einen Quelltext-Spiegel der Engine habe ich nicht benutzt.
- [API: UShallowWaterRiverComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent)
  – `SmoothingWidth` (int), `SmoothingCutoff` (float), `BottomContourCollisionDilation` (float), ohne Beschreibung [Suchauszug, wie 6k/6l].
- [Tutorial: Baked River Simulations – Parameter Reference](https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference)
  – „Smoothing Width/Cutoff: glättet die Oberflächen-Verschiebung an harten Kanten; bei Treppen-Artefakten erhöhen“ [Epic lokal, 16f].
- Im Repo: 6m §2–§3 (Band B, Kontur, Rolle-1-Lesung von `Grid2D_SW_River.uasset`, 5.8.3), 6l (Profil s 439, Kolkzählung,
  Landschafts-Lesetest), 6k §2.3 (Glättungsmodelle) und §3.1 (sichtbar), 6i (BAKED_SIM nach jedem Bake), 16g-N2 (Half-Float-Stufen).

**Nicht belegt:** Wohin die Saumwerte geschrieben werden (Ausgabe oder Zustand), die Trockengrenze, die Rolle des Cutoff, ob die
Darstellung über G ausblendet. Die Namen des Niagara-Parameters und des Python-Felds für den Cutoff.

## Rückfragen

Keine, die den nächsten Schritt ändert. Mit T6M3A bitte mitmelden, wie das Render-Target auf das 1-m-Raster abgebildet wurde (§3).
