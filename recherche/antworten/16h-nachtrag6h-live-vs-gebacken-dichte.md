# Antwort 16h Nachtrag 6h – Live gegen gebacken, Dichte-Zensus

**Gültigkeitskorrektur 16.10.2026 (in Ferats Auftrag):** Diese Antwort enthält historische
Hypothesen und Testaufträge. [6i §1](../auftraege/16h-nachtrag6i-baked-sim-tests-stand.md)
dokumentiert den optischen Erfolg von BAKED_SIM sowie Ergebnisse zu FixedWaterDepth,
Absorption 2/2/2, Water-Info-Aktualisierung und Materialpfad. Die entsprechenden Tests aus
§5.2 sind daher keine offenen Erstaufträge mehr. Den vorhandenen Befund verwenden;
Wiederholung nur mit neuem Eingang oder begründetem Testzweck. Die frühe Empfehlung
„Live-Werte übernehmen“ wurde bereits durch §5 eingeschränkt und darf nicht isoliert
als Lösung gelesen werden.

[6j §2 und Nachtrag 09:00](../auftraege/16h-nachtrag6j-teilung-ergebnis.md) melden die
verwendeten Ausblend-/Stencil-Pixelmessungen als unbrauchbar bzw. ungeeicht. §2 unten
beschreibt deshalb keinen abgenommenen Messweg. Erst die
[Messkontrollen](../vorlagen/pruefung.md#messwerkzeuge) erfüllen, dann Zahlen zur Optimierung
verwenden. Der optische Befund allein bestätigt weder die genaue WCBS-Ursache noch
gepackten Build, Streaming oder aktuelle GPU-Kosten. Die Werte und Schaustellenzahlen
aus §5.4 sind keine pauschale Freigabe für den heutigen Projektstand.

Stand 14.10.2026. Bezug: `auftraege/16h-nachtrag6h-live-vs-gebacken-dichte.md` (0bf16f1), Bilder `bilder/swr_p2/wasser_live_vs_gebacken_p2l.jpg`,
`epic_material_gebacken_p2h.jpg`, `mi_el_swr_klar_parameter.txt`, Graph-Dump `antworten/fluss_sim/p2_lokal/master_graph_schaum8.json`.

**Kennzeichnung:** [Graph] Dump unseres Masters, [Ferat] euer Test/Bild, [Doku/Forum] Quelle aus früheren Antworten, [Ableitung] gerechnet
bzw. geschlossen, [offen] nur durch Test zu klären.

## Kurzfazit

> **Nachtrag 14.10. (§5):** Punkt 1–2 sind für das gebackene Wasser **widerlegt**. Ferats EpicKlar-Test (P2M) zeigt: Live-Werte im MI
> ändern gebacken nichts. Die Einheit stimmt weiter, aber das Braun entsteht im Zeichenweg, nicht in den Werten.

1. **Gleiche Einheit, keine Umrechnung.** `Absorption` ist in unserem Master und nach allem, was wir wissen, auch in Epics Niagara-Master
   eine **Sichttiefe in cm** (das Material bildet den Kehrwert). Die Live-Werte gehören **1:1** in `MI_EL_SWR_Klar`. Einen Parameter
   `Koeff_Skala` gibt es nicht, weder im Graph noch in der MI-Liste, und er wird nicht gebraucht.
2. **Warum gebacken braun aussieht:** Unsere Sichttiefe ist rund **10-mal so lang** wie live (222/1000/1250 gegen 20,8/25/24,7 cm). Bei 0,5 m
   Tiefe lässt unser Wasser 80–96 % durch, das Live-Wasser nur 9–14 %. **Das Braun ist also unser S6-Grund, gesehen durch fast klares
   Glas.** Live verdeckt das Wasser den Grund und färbt sich selbst grünlich (wirksame Streuung 23- bis 38-mal stärker).
3. **Ein Widerspruch bleibt offen:** Laut 16a trug schon `SW_Water_Material_River` die Werte 20,8/25/24,7. Dann wäre P2H bereits der Test mit
   Live-Werten gewesen, und das Braun käme nicht aus den Werten. **Darauf zielt euer EpicKlar-Test** (§1.4).
4. **V20a fällt nicht automatisch weg.** `Default Near Normal Strength` hat schon in N4 (0,05) nichts geändert. Mit Live-Werten verschwindet
   aber der gebrochene helle Grund, und genau der war der Marmor. **V20a erst nach den P2M-Bildern entscheiden.**
5. **Dichte:** Zustimmung, es fehlt Komposition, nicht Stückzahl. Pixelmessung je Prüfbild: **ja**, als Prüfmaß in 21 §5 g (§2).
6. **6g ist beantwortet** (ff5d298, `16h-nachtrag6g-uferstufe-simulation.md`). 20 und 21 sind in Arbeit.

## 1. Live gegen gebacken

### 1.1 Einheiten: was belegt ist und was nicht

| Aussage | Stand |
|---|---|
| Unser Master: `Absorption` → `Divide` (zwei Knoten) → `Water_Underside` → `WaterCoefficientMask` → SLW-Ausgang | **[Graph]** |
| Unser Master: Wert = Sichttiefe in cm (große Zahl = klarer) | **belegt:** [Graph] + [Ferat 13k, Test 8/40/160] |
| `Scattering` → `Multiply` → `Add` (+ `Foam Scattering`) → `Divide` → `Water_Underside`; durch was geteilt wird, zeigt der Dump nicht | [Graph], Teiler [offen] |
| `Water Albedo` liegt nicht im Master, sondern in einer Funktion (`WaterAttributes`); die Verrechnung ist unbekannt | [Graph], Wirkung [offen] |
| Epics SLW-Ausgang: Koeffizienten ohne angegebene Einheit; Beispiel Absorption 0,0033/0,0016/0,0011 | [Doku] (13k, 15g, ufer-kies) |
| Diese SLW-Koeffizienten gelten **je cm**, weil die Engine die Wasserstrecke in Welteinheiten (cm) rechnet; das Doku-Beispiel ≈ 0,33/m Rot passt dazu | [Ableitung] |
| `SW_Water_Material` (Niagara-Master): dieselbe Parameterfamilie wie unser Master; Kehrwert im Graph **nicht** nachgesehen (T2-9 aus 16a ist nie gelaufen) | [Ferat 16a] / Einheit [Ableitung] |
| Live mit 20,8 cm sieht farbig-deckend aus, wie eine Sichttiefe von 21 cm es verlangt | [Ferat Bild P2L] passt zur Ableitung |

**Fazit:** Für beide Master gilt mit hoher Wahrscheinlichkeit „Sichttiefe in cm“. Für Epics Niagara-Master ist das nicht belegt, nur
abgeleitet → 2-Minuten-Test unten.

**2-Minuten-Test (Messlatte):** einen `/Engine/BasicShapes/Cube`, skaliert auf 5 × 5 × 200 cm, mit weißem Material senkrecht in ein Becken
von mindestens 80 cm Tiefe stellen. Absorption 30/30/30 einmal live (Niagara-MI) und einmal gebacken (`MI_EL_SWR_Klar`) setzen.
- Erwartet in beiden: In 30 cm Tiefe hat die Latte noch etwa 37 % ihrer Helligkeit, in 60 cm etwa 14 %.
- Verschwindet sie in einem der beiden Materialien erst rund 100-mal tiefer bzw. gar nicht, rechnet dieses Material anders.
- Senkrecht von oben ablesen; von der Seite ist der Weg durchs Wasser länger (§1.2).

### 1.2 Übersetzung in `MI_EL_SWR_Klar` (Rechenweg)

Da die Einheit gleich ist, gilt **neu = live**, ohne Faktor.

| Parameter (MI) | heute (F) | **neu (= Niagara-Kind)** | Rechnung |
|---|---|---|---|
| `Absorption` R, G, B (A bleibt 8) | 222 / 1000 / 1250 | **20,8 / 25 / 24,7** | Koeffizient = 1/L: 0,048 / 0,040 / 0,040 je cm (= 4,8 / 4,0 / 4,0 je m). Heute: 0,0045 / 0,001 / 0,0008 je cm |
| `Scattering` R, G, B, A | 0,5 / 1 / 1, A 0,02 | **0,77 / 1,0 / 0,92, A 0,5** | Wirksam (RGB × A, wenn `Multiply` so verdrahtet ist): heute 0,01/0,02/0,02, neu 0,39/0,50/0,46 → **≈ 23–38-fach** |
| `Water Albedo` RGB (A bleibt) | 0,03 | **0,083** | × 2,8 |
| `Water Roughness` | 0,025 | **0,02** | wie Niagara |
| `Default Near Normal Strength` | 0,25 | **0** | wie Niagara (§1.3) |
| `Default Distant Normal Strength` / `…StrengthB` | 0,3 / 0,25 | **0,3 / 0** | wie Niagara |

**Durchlass senkrecht, T = exp(−d/L)** [Ableitung]:

| Tiefe | heute R / G / B | neu R / G / B |
|---|---|---|
| 0,2 m | 91 / 98 / 98 % | 38 / 45 / 45 % |
| 0,5 m | 80 / 95 / 96 % | 9 / 14 / 13 % |
| 1,0 m (Kolk) | 64 / 91 / 92 % | 0,8 / 1,8 / 1,7 % |

- Aus Augenhöhe ist der Weg länger: Bei 20° Blickneigung etwa 2,9 × die Tiefe. Schon eine 20-cm-Rinne wirkt dann wie 58 cm Wasser.
  Daher kommt der „Körper“ im Live-Bild.
- Ist ein 1-m-Kolk damit zu deckend, wäre der nächste Schritt **50 / 70 / 70 cm** (bei 0,5 m: 37 / 49 / 49 %) [Gestaltung].

**Was ich offen korrigiere:**
- **16a b1/b2:** Die Einheit (Sichttiefe in cm) stimmt. Falsch war die Empfehlung, die SWR-Werte auf 250/1430/2000 zu verlängern. Damit haben
  wir den Look verlassen, den Ferat jetzt will.
- **16h-Hauptantwort und Materialtest („Absorption ist nicht der Hebel“):** Das gilt nur für den Bereich 220–2000 cm, den wir getestet haben.
  Bei 20–25 cm ist die Absorption **der** Hebel.
- **6/6d/6f (S6, „Grund ist der Haupthebel“, „Coast-Absorption nicht übernehmen“, „Becken klar durch dunklen Grund“, Bergbach
  160/650/850):** Bei fast klarem Wasser sieht man vor allem den Grund. S6 hat das Milchige entfernt, aber das Braun ist **S6 selbst**. Die
  Coast-Größenordnung (10/150/350) lag näher am Ziel als F. S6 darf bleiben; mit kurzen Sichttiefen wirkt er nur noch in Rinnen unter 20 cm.

### 1.3 V20a und Near Normal = 0

- Live hat keine Flowmap-Normalen-Kette, nur die Normalen der Simulation. Gebacken laufen die Schlieren über `Enable River` (Flowmap-Normalen,
  6d) [Ableitung].
- `Default Near Normal Strength` auf 0 nimmt nur die Textur-Normale nah weg. In N1–N4 hat das (0,05) den Marmor **nicht** entfernt [Ferat].
  **Near Normal 0 ersetzt V20a also nicht.**
- Aber: Der Marmor war zum großen Teil heller Grund, gebrochen durch die Normalen (S2-Befund). Mit Sichttiefe 21–25 cm ist der Grund ab
  etwa 0,3 m kaum noch sichtbar, also bricht sich dort auch nichts mehr.
- **Entscheidung:** Near Normal 0 im MI mitnehmen (ein Wert, kostet nichts). V20a bauen wir nur, wenn in P2M in Rinnen unter 0,3 m noch Marmor
  stört.

### 1.4 Worauf Ferat beim EpicKlar-Test (P2M) achten soll

1. **Zuerst die Parameter vergleichen:** `SW_Water_Material_River` gegen `SW_Water_Material_River_Niagara`, Absorption, Scattering und
   Albedo (Details-Panel oder `get_vector_parameter_value`).
   - Hat `SW_Water_Material_River` schon 20,8/25/24,7 (so steht es in 16a), dann ist EpicKlar gleich P2H und wird ebenso braun.
   - In diesem Fall liegt die Ursache **nicht** in den Werten, sondern in einem der Punkte 3 und 4.
2. **Unterscheidet sich P2M deutlich von P2H** (grünlich, Grund ab ≈ 0,3 m verdeckt): Die Werte sind der Hebel. Dann die Tabelle aus §1.2 in
   `MI_EL_SWR_Klar` übernehmen und gegen P2L prüfen, mit derselben Kamera und Uhrzeit (t430, t500, m_talkaskade).
3. **Sieht P2M aus wie P2H:** Gegenprobe mit Absorption **5/5/5**. Das muss deckend werden.
   - Bleibt es braun, kommen die Werte nicht an. Prüfen, wer zeichnet: Water-Body-Material **und** `baked_sim_material` müssen beide EpicKlar
     sein (16b/6g).
4. **Wird es erst bei 5/5/5 farbig:** Dann dämpft die Tiefenmaske die Koeffizienten.
   - [Graph]: `WaterOpacityMaskFromDepth` → `WaterCoefficientMask` → SLW. Gebacken kommt die Tiefe aus der Wasser-Info; bei uns stehen
     `UseBakedSim` False, `BakedWaterSimSize` 0 und `Water Opacity Mask Offset` −24.
   - Test: `Water Opacity Mask Offset` einmal 0 und einmal −100 [offen, Richtung unbekannt].
5. **Schaum und Marmor nicht vergleichen.** Live kommt der Schaum zum Teil aus der Darstellung der Simulation (16a). Bewertet nur Farbe,
   Durchsicht und Ruhe der Fläche.
6. **Kolk und Rinne getrennt ansehen:** Der Kolk darf dunkel-grün werden. Rinnen unter 20 cm sollen den Grund noch zeigen.

## 2. Dichte-Zensus

- **Zustimmung zum Befund:** Bei Stückzahlen je 100 m² liegen wir gleichauf oder darüber (C2 9,4, Talkaskade 24,0 gegen RA 3,8–10,5 Netze). Den
  Unterschied machen Größe, Überlappung und Ort: RA2 hat 378 % Felsfuß-Deckung (gestapelte Blöcke an der Klippe), die Talkaskade 1,2 %
  (Kleinsteine ≤ 0,5 m). Dazu kommen 294 verschiedene Netze gegen 35–53 bei den Demos.
- **Folgerung:** Weniger Sorten, große Blöcke von 1–8 m in Stapeln auf Steilflächen und Ufern. Das stützt 20/21.
- **Grenze der Kennzahl:** Die Deckung als Summe der Fußflächen zählt verdeckte Teile doppelt (deshalb über 100 %). Für das Bild zählt, was
  sichtbar ist. Deshalb ja zur Pixelmessung.

**Pixelmessung je Prüfbild (für 21 §5 g):**

**Nicht abgenommen:** Der lokale Nachtest in 6j meldet Fehler auch beim Stencil-Weg.
Die folgende Konstruktion erst an Kontrollfällen validieren; ihre Kennzahlen noch nicht
zur Bestands-/Dichteentscheidung verwenden. Siehe Gültigkeitskorrektur am Dateianfang.

1. Je Prüfkamera (GEF_*, BERG11_*, die RA-Bilder zur Eichung) einen SceneCapture2D mit derselben Lage und demselben FOV.
2. Alle Netz-Komponenten in Sicht bekommen `Render CustomDepth` und einen Stencil-Wert: 1 Fels/Stein, 2 Pflanze, 3 Sonstiges. Die Landschaft
   bekommt keinen.
3. Zwei Aufnahmen machen: Stencil (Netz-Pixel je Klasse) und SceneDepth (Himmel und Wasser ausschließen, Abstandsbänder nah < 30 m,
   mittel 30–150 m, fern).
4. **Kennzahl:** Netzanteil = Netz-Pixel / (Netz- + Landschafts-Pixel), je Klasse und Band. Ausgabe als JSON und als Overlay-Bild.
   - Der Weg über `hide_actor_components` (21 §2.1) geht auch, braucht aber drei Aufnahmen statt zwei.
5. **Kriterium:** Fels-Netzanteil in Berg- und Steilszenen gegen die Referenz (≥ 80 % laut 21), geeicht an RA2. Ein Zielwert je Szene folgt
   in 21 §5.

## 3. Hinweis an Ferat

- **6g ist beantwortet:** ff5d298, `antworten/16h-nachtrag6g-uferstufe-simulation.md`.
- **Aufträge 20 und 21 sind in Arbeit.** Die Pixelmessung aus §2 geht dort ein.

## Was fehlt bis Witcher 4

1. **Wasserfarbe:** Den EpicKlar-Befund (P2M) klären, dann die Live-Werte im MI setzen. Ist das Braun nicht aus den Werten, erst Punkt 3/4
   aus §1.4 lösen.
2. **Ruhige Fläche nah, gerichtet in Rinnen:** Near Normal 0 setzen, V20a nur bei Bedarf, danach „Normalen nach Tempo“ (18 §3.1).
3. **Weißwasser nur an Stufen**, auch gebacken (FoamAtten-Plan, 16h Nachtrag 3 §4.2).
4. **Ufer und Hänge aus großen Blöcken** in Stapeln statt Kleinsteinen und Textur (20/21), gemessen mit dem Pixelanteil aus §2.
5. **Bett:** längliche Kolke und die Uferstufe aus 6f/6g, damit die neue Wasserfarbe Tiefe zeigen kann.

## §5 Nachtrag zu Ferats §4 (EpicKlar gebacken = kein Unterschied)

Bezug: Auftrag §4 (4f9785c), Bild `bilder/swr_p2/wasser_p2d_p2l_p2m.jpg`.

### Kurzfazit

1. **Widerlegt:** „Live-Werte 1:1 ins MI lösen es“ (Kurzfazit 1–2, §1.2) stimmt für gebackenes Wasser nicht. Die Einheit stimmt weiter, sie
   ist aber nicht die Ursache. Ebenso widerlegt ist „das Braun ist S6 durch zu klare Werte“: Das Braun ist zwar der Grund, aber weil gebacken
   **kaum ein Wasserkörper gezeichnet wird**, nicht wegen der Werte. Meine Prüfpunkte 3/4 aus §1.4 (Maske, Tiefe, Zeichenweg) waren die
   richtige Spur.
2. **Bild:** P2M ist praktisch gleich P2D. Bei 21 cm Sichttiefe müsste schon eine 10-cm-Schicht deutlich färben, man sieht aber keine Färbung.
   Also ist die wirksame Wassertiefe gebacken nahe 0, oder die Koeffizienten werden weggemaskt [Ableitung].
3. **Erster Test, 2 min:** `render_state` = **`BAKED_SIM`**. Dabei zeichnet die SWR das Gebackene selbst, ohne Water Zone. Kosten: 0,3 ms und
   3 Dispatches (16b gemessen).
   - Laut Forum 5.8 zeigen „Live Sim“ und „Baked Sim“ korrekt; nur „Water Component with Baked Sim“ macht Probleme, weil die SWR ihre Fläche
     anders baut als der Water Body [Forum, Suchauszug].
   - **Sieht BAKED_SIM aus wie live, ist das die Spiellösung ohne Live-Simulation.**
4. **Regel:** LIVE_SIM im Spiel nur, wenn auch BAKED_SIM braun bleibt, und dann nur an 1–2 Schaustellen (§5.4).

### 5.1 Was das Bild zeigt [Ferat]

| Blick | P2L live | P2D und P2M gebacken |
|---|---|---|
| m_talkaskade | Hauptbecken bis zur Kante grün-türkis gefüllt, die Beckenwand verschwindet unter dem Spiegel | braune Beckenwand und Grund frei sichtbar, kaum Wasserfarbe |
| t500 schräg | jede Stufe mit grünem Wasserkörper, Spiegel in jedem Becken | dunkel-nasse Stufen ohne Körper; nur im untersten Becken Spiegelung |
| t430 / t500 Auge | ruhiger, durchscheinend grüner Körper, Grund nah sichtbar | Schlieren-Spiegelung über braunem Grund; P2M nur etwas heller (Licht), sonst gleich |

**Rechnung** [Ableitung]: Bei L = 21 cm lässt eine 10-cm-Schicht senkrecht nur 62 % durch, aus Augenhöhe (Weg × 2,9) nur 25 %. Das wäre klar
sichtbar. Weil gebacken nichts färbt, ist die wirksame Tiefe dort höchstens wenige Zentimeter.

### 5.2 Ursachen nach Wahrscheinlichkeit, je ein Test unter 5 min

**Befund vorhanden:** 6i §1 dokumentiert Ergebnisse zu 0, 1 (beide Gegenproben), 3 und 5.
Die Messlatte unter 2 wurde dort ausdrücklich nicht durchgeführt. Kein vollständiges
Bestehen dieser Tabelle und keine gesicherte Ursachenbestimmung daraus ableiten.

| # | Ursache | Stand | Test | Erwartung |
|---|---|---|---|---|
| 0 | **Weiche:** Liegt es am Zeichenweg der Water Zone (WCBS) oder an den gebackenen Daten selbst? | – | `render_state` `BAKED_SIM`, gleiche Kameras | live-ähnlich → Ursache 1–3 (WCBS-Weg). Ebenfalls braun → Ursache 4 (Daten) |
| 1 | **Tiefe und Maske im WCBS-Weg:** Die Koeffizienten laufen über `WaterOpacityMaskFromDepth` → `WaterCoefficientMask`. Die Tiefe kommt aus der Wasser-Info (Wasser-Z minus Boden-W in Zonenauflösung). Live rechnet auf dem Simulationsnetz mit der echten Höhe | Kette [Graph]; dass die Maske ≈ 0 liefert [Ableitung] | im MI den Schalter `UseFixedWaterDepth` → True (steht in der MI-Liste); dazu die Gegenprobe Absorption 2/2/2 | färbt sich das Wasser mit festem Tiefenwert bzw. bei 2/2/2 sichtbar → Tiefe oder Maske ist schuld. Bleibt es braun → Ursache 2 |
| 2 | **Fläche zu tief bzw. zu dünn:** Die Water-Zone-Fläche liegt auf der Höhe aus der Wasser-Info, nicht auf der Simulationshöhe (vgl. 16g: grobe Info → Bett trocken) | [Ableitung] aus 16g | Messlatte aus §1.1 mit 10-cm-Strichen ins Hauptbecken; Spiegelhöhe live und WCBS ablesen; dazu `r.Water.WaterMesh.ShowWireframe 1` [Doku 5.2] | Spiegel gebacken ≥ 10 cm tiefer, oder Drahtgitter deckt das Becken nicht → Ursache 2. Abhilfe: Zonenauflösung (Regel Pixel ≤ Band/12, 16g-2) |
| 3 | **Wasser-Info nach dem Bake veraltet** | CVar belegt [Doku 5.2]; Wirkung [offen] | `r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames 10` in der Konsole, dasselbe Bild | ändert sich das Bild → veraltet; dann nach jedem Bake erzwingen bzw. Level neu laden |
| 4 | **Gebackene Daten grob:** Normal-, Schaum- und Höhentextur niedrig aufgelöst bzw. komprimiert (Bake 319 × 2016) | [Ableitung] | im BAKED_SIM-Bild nah vergleichen; die gebackene Textur im Texture-Viewer öffnen (Größe, Kompression) | erklärt Detail und Schlieren, **nicht** die fehlende Farbe. Niedrige Priorität für das Braun |
| 5 | **Anderes Material im Niagara-Renderer** (Blend, Shading, eigenes Netz je Zelle) | Netz je Zelle [Leitfaden: „zeichnet selbst“]; Blend/Shading [offen] | `SW_Water_Material_River_Niagara` öffnen → Eltern-Material → Details: Blend Mode, Shading Model; mit `M_Eldarien_Wasser_Schaum8` vergleichen (SingleLayerWater) | anderes Shading (z. B. Translucent) → Live-Look ist im WCBS-Weg nur über einen eigenen Pfad nachbaubar. Gleiches Shading → 1–3 bleiben |

- `r.Water.WaterInfo.RenderMethod` gibt es laut Forum [Forum]; welche Werte gelten, ist unbelegt. Nur abfragen, nicht raten.
- `Lip Refraction` (0,95) steht auch in unserem MI. Sie erklärt allein nicht, warum der Körper fehlt [Ableitung].

**Nachbau in WCBS:**
- Bei Ursache 1 oder 3 ja: ein Schalter oder ein CVar.
- Bei Ursache 2 teilweise, über eine feinere Zone; das kostet Speicher (16g: 100–400 MB bei 2–4 feinen Zonen).
- Bei Ursache 5 nur mit eigenem Material-Pfad. Dann lohnt eher BAKED_SIM nah.

### 5.3 Umschalten nach Entfernung in 5.8

- **Nicht als eingebaute Funktion belegt** [16a, Suche ohne Treffer].
- Belegt ist nur: Steht die SWR auf Live oder Baked Sim, blendet sie die Water-Body-Fläche des Flusses selbst aus; für Seen nicht [Forum 5.8,
  Suchauszug].
- Ob `render_state` zur Laufzeit umstellbar ist, ist [offen] (T2-4 aus 16a lief nie).
- **Test (5 min, PIE):** per Blueprint oder Python `render_state` WCBS ↔ BAKED_SIM bzw. LIVE_SIM schalten, zweimal hin und her. Darauf achten:
  1. Wechselt es ohne Ruckeln und ohne doppelte Fläche?
  2. Startet LIVE_SIM trocken oder aus dem gebackenen Zustand (Zeit bis ruhig)?
  3. `ProfileGPU` vorher und nachher.
  4. Danach einmal im **gepackten Build** prüfen. Laut Forum zeichnet die gebackene SWR dort teils gar nicht (16a).

### 5.4 Entscheidungsregel LIVE_SIM gegen WCBS

**Historische Planungswerte:** Die nachfolgende Tabelle ersetzt keine aktuelle Messung
am Zielgerät und keine Prüfung im gepackten Build. Insbesondere „höchstens 3“ ist hier
eine damalige Budgetannahme, kein nachgewiesenes Engine-Limit und keine aktuelle Abnahme.

| Fall | Nah (≤ 100 m, sichtbar) | Fern |
|---|---|---|
| BAKED_SIM sieht aus wie live (Test 0) | **BAKED_SIM** an Schaustellen, höchstens 3 gleichzeitig (≈ 0,9 ms). Keine Interaktion [Leitfaden] → nur, wo man nicht watet | WCBS (0,2 ms) bzw. Water Body |
| Ursache 1–3 in WCBS behoben | WCBS überall | WCBS |
| nur LIVE_SIM sieht richtig aus | **LIVE_SIM nur an 1–2 Schaustellen** (Talkaskade), höchstens 1 gleichzeitig (0,6 ms für 179 m, 59 Dispatches, 16b), über den Manager aus 16b (≤ 100 m, sichtbar) | WCBS |
| nie | LIVE_SIM an allen Bächen: 12 ms bei 1 km Ladebereich (16b) | – |

Budget: 1,5 ms für Wassersimulation und Effekte (Datei 16). Umschalten nach Entfernung nur, wenn der Test aus 5.3 sauber läuft. Sonst bleibt die
Schaustelle fest im gewählten Zustand.

**„Was fehlt bis Witcher 4“, Punkt 1, wird ersetzt:** zuerst Test 0 (BAKED_SIM), dann 1–3. Die Live-Werte im MI erst setzen, wenn der Weg
die Wasserfarbe überhaupt zeigt.

**Quellen (neu):**
- [Forum: ShallowWaterRiver – Lake/Ocean, 5.7/5.8](https://forums.unrealengine.com/t/shallowwaterriver-lake-ocean/2838534) – Live Sim und
  Baked Sim zeigen korrekt, WCBS nicht für Seen; die SWR baut ihre Fläche anders als der Water Body (Suchauszug).
- [Tutorial: Baked River Simulations – Parameter Reference](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112)
  (Leitfaden, wie in 16a).
