# Antwort zu Auftrag 16g – Shallow Water River im steilen Bergbach: Wasser bleibt stehen, Abbruch bei s 62 m

Stand 13.10.2026. Grundlage sind Auftrag 16g (Befunde 1–9, Fragen 1–5), die Antworten 16, 16a–16f, Ferats
Zusammenfassung der Epic-Seite „Baked River Simulations – Parameter Reference“ (`auftraege/16f-rueckfrage-epic-parameter-lokal.md`)
und `skripte/fluss_sim/`.

**Quellenlage:**
- Aus der Cloud waren `dev.epicgames.com`, `forums.unrealengine.com`, `issues.unrealengine.com`, 80.lv und lilys.ai gesperrt
  (WebFetch: DNS-Fehler). YouTube ist gesperrt. Alle Web-Belege stammen deshalb aus **Suchmaschinen-Auszügen**.
- Zu „SWR in steilen Flüssen“ gibt es **keinen** öffentlichen Beleg: keinen Forenfaden, keine Release-Note 5.6–5.8, keinen
  Tutorial-Kommentar. Einen Unreal-Fest-Vortrag von Devon Penney zur Flusssimulation habe ich nicht gefunden. Der einzige
  Unreal-Fest-2025-Treffer zu Wasser ist „Chasing Waterfalls“ (Matt Oztalay, Niagara, mobiles RTS) ohne Bezug zur SWR.
  Zur Witcher-4-Demo gibt es weiter nur den Stand aus 16f Teil C.
- Der größte Teil der Antwort ist deshalb **eigene physikalisch-numerische Analyse**, als [Ableitung] gekennzeichnet. Sie
  stützt sich auf eure Messwerte.

**Kennzeichnung:**
- [Epic lokal]: Ferats Zusammenfassung der Parameter Reference
- [Doku]: Epic-API- bzw. Python-Doku, Suchauszug
- [Forum]: Epic-Forum, Suchauszug
- [Fach]: Fachliteratur (Hydraulik, Geomorphologie), Suchauszug bzw. Lehrbuchwissen
- [Befund n]: eure Messung aus Auftrag 16g
- [Ableitung]: aus Belegen und Befunden geschlossen und gerechnet
- [unsicher]: nicht belegt, im Test klären

---

## Kurzfazit

1. **Die Simulation ist nicht eingefroren, sie ist im Gleichgewicht.** Sie tickt (Befund 3), und der Zustand nach 90 s, 210 s
   und 5 min ist gleich (Befund 2).
   - In einer Treppe aus waagrechten Becken und Lippen ist „volle Becken ohne Durchfluss“ ein gültiger Ruhezustand. Das ist
     nicht unmöglich, es heißt nur: **Durch die Rinne fließt fast nichts.**
   - Rechnung: Flösse das Wasser in 0,59 m Tiefe eine 39-%-Rinne hinunter, wären das etwa **15 m³/s**. Das kann weder die Quelle
     liefern, noch bliebe dann der Durchbruch trocken.
   - Die eigentliche Frage ist deshalb: **Warum kommt (fast) kein Wasser nach, und wo geht es verloren?**
2. **Befund 6 ist sehr wahrscheinlich ein Fehler der Abfrage, nicht der SWR.**
   - `get_water_surface_info_at_location(Vector(x, y, 0))` sucht den nächsten Splinepunkt **in 3D**. Von z = 0 aus liegt der
     nächste Punkt einer schrägen Spline talwärts.
   - Rechnung: Versatz Δs = m · H / (1 + m²). Bei Gefälle m = 0,39 und Höhe H = 190 m sind das **64 m und 25 m tiefer**. Gemessen
     habt ihr „bis 30 m unter dem Plan“.
   - Abhilfe: mit z = Planspiegel abfragen (Test T0-1). Für die SWR selbst beweist Befund 6 also nichts.
3. **Die Abbruchkante bei s ≈ 62 m (Befund 1) und das fehlende Nachfüllen im Durchbruch und in der Talkaskade (Befund 4,
   selbst bei Rate 2) haben sehr wahrscheinlich dieselbe Ursache:**
   - Die „Spline-Information“ der SWR (innen/außen und Spline-Höhe) fehlt ab etwa s 62 m oder ist dort falsch.
   - Träger ist sehr wahrscheinlich eine **2D-Textur**: Die SWR hat eine eigene `water_info_texture` [Doku]. Die Water Zone hat
     Höhenfelder (`WaterHeightExtents`, `GroundZMin`, `CaptureZOffset`), einen Schalter 16/32 Bit (`bHalfPrecisionTexture`) und
     eine **lokale Tessellation**, bei der die Water-Info-Textur nur ein „gleitendes Fenster um die Kamera“ abdeckt [Doku].
   - Eine **schnurgerade Kante** ist typisch für einen Textur- oder Zonenrand bzw. eine Höhenlinie. Für eine Spline-Rechnung
     wäre sie untypisch.
   - Welche Grenze es genau ist, entscheiden drei Messungen ohne neue Simulation (T0-2, T0-3) und zwei Läufe (T3-1, T3-2).
4. **Das Rechteck ohne Rand (Befund 8) kostet Wasser.**
   - An jedem Extrempunkt des Laufs liegt das halbe Bett außerhalb der Simulation: an der Quelle (0,2 m vom Nordrand), an der
     Mündung und an jedem äußersten Bogen.
   - Ist der Rand offen, fließt dort Wasser ab. Die stehende Front bei s ≈ 231 m ist zu prüfen: Liegt dort ein West- oder
     Ostextrem des Laufs? (T0-2).
   - Die Quelle speist zur Hälfte ins Nichts.
   - Im Export (2-m-Daten) liegt die Quelle bei **allen 187 Gewässern** weniger als 1 m vom UE-Rechteck. Bei 76 SWR-Bereichen ragt
     das Bett auch mitten im Lauf über den Rand. Beim Erlenbach der 2-m-Daten ist das die Strecke s 160–323 m am Westrand.
5. **16 Bit ist nicht die Ursache.**
   - Alle Höhen liegen zwischen 36 und 190 m, weit unter 655 m.
   - Der Boden der Simulation stimmt laut eurer Messung auf cm.
   - Bleibt die Water-Info-Textur in 16 Bit: Dort wäre die Höhe auf 8 cm (unter 163,84 m) bzw. 16 cm (darüber) gerastert. Das
     ist harmlos. Prüfzahl: Liegt die Abbruchkante bei z ≈ 163,8 m (= 2¹⁴ cm), wäre das ein Indiz.
6. **Reibung, Mindesttiefe und Zeitschritt sind Nebenursachen.**
   - In einer Becken-Stufen-Treppe läuft der Durchfluss über **dünne Überfälle an den Lippen** (5–15 cm). Reibung „bremst vor
     allem flaches Wasser“ [Epic lokal]. Eine hohe Reibung oder eine Trockenschwelle von einigen cm kann die Lippen
     „verstopfen“.
   - Der Zeitschritt bei `sim_speed` 10 / `num_steps` 10 (25 ms) liegt an Fallfüßen von 1,6–3,7 m knapp unter der
     Stabilitätsgrenze (30–35 ms bei 0,37 m Zelle). Das reicht nicht für einen Stillstand, wohl aber für Unruhe.
7. **Quelle:** Sie speist am ersten Splinepunkt über Lage, Tangente, Breite und Tiefe (`QueryWaterAtSplinePoint`, Befund 8).
   Ein Tempo gibt diese Abfrage nicht zurück.
   - Empfehlung: erster Punkt in einem flachen Quellbecken, mindestens 10 m vom Rechteckrand (Vorlauf 10 m die Felsrinne hinauf),
     Spiegel 0,25–0,35 m über Grund, `source_size` = Bettbreite (3–4 m).
   - Das ergibt rechnerisch **0,6–1,1 m³/s**, passend für einen 3–4 m breiten Wildbach.
   - Heute (Tiefe 0,67 m + 0,3 m, halb außerhalb) wären es rechnerisch 1,4–4,9 m³/s. Gemessen kommt viel weniger an. Das spricht
     wieder für Verlust am Rand.
8. **Teilen der Simulationsfläche** desselben Flusses geht mit der belegten API nicht.
   - Das Rechteck ist immer die Box um **alle** Quell-Flüsse (16c), und Quellen speisen nur am ersten Punkt eines Flusses.
   - Zwei SWR über demselben Fluss decken also beide das ganze Rechteck ab. Gebacken überschreiben sie sich [Forum].
   - Eine obere SWR kann eine untere nicht speisen [Ableitung].
   - Empfehlung: **eine SWR je Fluss bleibt.** Lange steile Rinnen bekommen Plan B.
9. **Plan B (Witcher-Qualität):**
   - Die SWR für flache und mittlere Abschnitte.
   - In langen steilen Rinnen (Spiegelgefälle ≥ 30 % über ≥ 50 m) das vorhandene **Kaskadennetz (A15)** mit Flowmap-Material,
     Schaumobjekten und Niagara-Gischt.
   - Die SWR wird dann erst am Fuß der Steilstrecke über einen **Speisepunkt** versorgt (Rückfrage 1).
   - Niagara Fluids 2D bringt für steile Rinnen nichts: dieselben Flachwassergleichungen. 3D-FLIP lohnt nur für einen einzelnen
     Schau-Fall.
10. **Export (Regeln v9):** Je SWR-Bereich gibt es neu die Diagnose `rand_steil`. Sie ändert weder Spline, SWR-Werte noch
    Fingerabdruck. Inhalt:
    - UE-Rechteck ohne Breite, Abstand der Quelle zum Rand, Stellen mit Bett über dem Rand, Soll-Rahmen;
    - Höhenspanne, Steilstrecken, Eignung `swr` / `pruefen` / `kaskade_vorschlag`.
    - Zahlen über alle Gewässer in Abschnitt 7. Prüfer 0 FEHLER, zwei Läufe byte-gleich.

---

## Wahrscheinlichste Ursachen (Rangfolge)

Getrennt nach den zwei Erscheinungen. **A** = Abbruchkante bei `remove_outside_spline_amount` 50 (Befund 1).
**B** = Front bleibt bei `remove` 0 am Durchbruch stehen, Becken stehen still (Befund 2, 4).

| Rang | Ursache | erklärt | passt zu | spricht dagegen | Gegenprobe |
|---|---|---|---|---|---|
| **1** | **Spline-Information der SWR (innen/außen, Spline-Höhe) endet bzw. ist falsch ab s ≈ 62 m**, getragen von einer 2D-Textur mit begrenzter Ausdehnung oder begrenztem Höhenbereich (Water-Info der SWR bzw. der Zone, lokale Tessellation, Capture-Höhe) | A, und B im Durchbruch/Talkaskade | gerade Kante; Lage unabhängig von Nachfüllrate, Kamera, Occlusion (Befund 1); Nachfüllen wirkt im Kiesbett, aber nicht im Durchbruch, selbst bei Rate 2 (Befund 4); Rinne bei Rate 2 1,4 m **über** Plan (Befund 4) | – | T0-2, T0-3, T3-1, T3-2 |
| **2** | **Kaum Durchfluss**: Quelle halb außerhalb (0,2 m vom Rand), Treppe aus 103 waagrechten Becken speichert, Nachfüllen hält die Becken genau auf Lippenhöhe → volle Becken ohne Überlauf | B | 0,59 m Tiefe ≈ Plan 0,67 (Nachfüll-Ziel); stationärer Zustand; 0,59 m fließend wären ~15 m³/s | Rinne war in 90 s voll (also kam anfangs Wasser) | T1-1, T1-2, T2-1 |
| **3** | **Abfluss über den Rechteckrand** (Rechteck ohne Rand): an der Quelle und an jedem äußersten Bogen liegt das halbe Bett außerhalb | B (Front bei s ≈ 231 m), weniger Speisung | Befund 8 | nur, wenn bei s ≈ 200–231 m ein Extrempunkt liegt | T0-2, T2-2 |
| 4 | **Zweiter Fluss (Arm)**: Seine Senke (letzter Punkt) saugt ab, oder er überdeckt in der Water-Info den Erlenbach | B, evtl. A | „Quelle = Senke = Fluss + Arm“ | Lage des Arms unbekannt | T0-2 (Lage), T1-1 ohne Arm |
| 5 | **Reibung / Trockenschwelle an dünnen Überfällen**: Lippen-Überfall 5–15 cm wird stark gebremst oder als trocken behandelt | B (Becken voll, kein Überlauf) | Epic: Friction bremst flaches Wasser | Standardwerte, keine Kopie geändert? | T5-2 |
| 6 | **Zeitschritt / Stabilität** (speed 10, steps 10 = 25 ms je Schritt; Grenze 30–35 ms bei 0,37 m und Fallfüßen bis 8,5 m/s) | Unruhe, lokale Fehler | 1–3,7-m-Stufen | stabiler Gleichgewichtszustand | T5-1 |
| 7 | 16 Bit (Half Float) in Boden- oder Höhentexturen | – | – | Höhen 36–190 m ≪ 655 m; Boden auf cm gemessen | T0-2 (z an der Kante = 163,8 m?), T3-2 |
| – | `MaxFlowVelocity` 1024 cm/s | nur die Kodierung der Strömung in der Water-Info (16e) | – | wirkt nicht in der Simulation | – |

**Zur Rangfolge:** Rang 1 ist die einzige Ursache, die Befund 1 **und** Befund 4 erklärt. Rang 2 und 3 erklären zusammen,
warum bei `remove` 0 kein Wasser durchkommt. Wahrscheinlich wirken 1 und 2 (bzw. 3) gleichzeitig. Deshalb trennt der Testplan
sie in eigenen Läufen.

---

## 1. Frage 1 – Warum bleibt das Wasser stehen?

### 1.1 Was die Befunde zusammen sagen [Ableitung]

| Abschnitt | `remove` 50 (Befund 1) | `remove` 0 (Befund 2) | `remove` 0, Nachfüllen 2, `source` 1000 (Befund 4) | Lesart |
|---|---|---|---|---|
| Bergrinne 0–62 m | nass | voll, 0,59 m | 2,08 m (Plan 0,67) | Quelle und Nachfüllen wirken |
| Bergrinne 62–199 m | **trocken, gerade Kante** | voll, 0,59 m | 2,08 m | Wasser kommt hin, wird aber bei `remove` 50 als „außen“ gelöscht |
| Durchbruch 199–390 m | trocken | 16 % nass, Front s ≈ 231 | **trocken** | Nachfüllen wirkt nicht → Spline-Höhe dort zu niedrig oder Zelle gilt als „außen“; dazu Verlust vor Ort |
| Talkaskade 390–579 m | trocken | 0 % | trocken | wie Durchbruch |
| Kiesbett 579–788 m | trocken | 96 % | 1,02 m (Plan 0,53) | Nachfüllen wirkt (Spline-Höhe dort ≈ richtig, mit Rate 2 sogar zu hoch) |

- **Die Maske „innen“ und die Nachfüll-Höhe sind zwei verschiedene Felder**, oder ein Feld mit zwei Schwellen. Denn bei
  `remove` 50 ist das Kiesbett trocken, bei `remove` 0 wird es nachgefüllt.
- **In der Bergrinne steht das Wasser bei Rate 2 1,4 m über dem Plan.** Das Nachfüll-Ziel liegt dort also zu **hoch**. Im
  Durchbruch ist es zu **tief** bzw. fehlt.
  - Ein „zu hoch in steilem Gelände“ passt zu einer **gerasterten 2D-Höhe**: eine Höhe je Texel, die obere Kante gewinnt.
    Fehler = Texelgröße × Gefälle (Tabelle in 1.3 g).
  - 1,4 m Fehler bei 39–64 % Gefälle entsprechen einem Texel von etwa **2,2–3,6 m**. Das wären bei 741 m Rechtecklänge etwa
    **256 Texel**. Das ist nur eine Vermutung; T0-3 liest die Größe aus.
- **Stillstand:** Die Rinne ist eine Treppe aus waagrechten Becken (103 Einheiten, Stufen im Median 1,6 m). Volle Becken ohne
  Zufluss stehen still. Fließt doch etwas, dann nur als dünne Schicht über die Lippen.
  - Normalabfluss nach Manning (k_St 15, 4 m breit, 39 %): Q = 1 m³/s → 0,11 m tief, 2,2 m/s.
  - Für 0,59 m Tiefe bräuchte es **15,5 m³/s** (6,5 m/s).
  - Die 0,59 m sind also die Becken-Tiefe, keine Fließtiefe. Ob Wasser fließt, zeigt nur das Tempo an den Lippen (T1-1).

### 1.2 Recherche: bekannte Grenzen und Fehler der SWR (Stand 5.6–5.8)

| Quelle | Aussage | Bezug zu uns |
|---|---|---|
| [Forum] „ShallowWaterRiver simulation does not initialize in Unreal Engine 5.7.4“ | Simulation startet in eigenen Levels nicht, Reset tut nichts; das Beispiel-Level `WaterFluidSimtestShallow` geht | bei uns läuft sie (Befund 3) |
| [Forum] „Shallow water plugin not working in 5.8“ | mit `use capture` keine Tiefe, ohne Capture „Rechteck, das die Landschaft ignoriert“; in 16a: Bodenhöhen „saturated at 65504“ | bei uns stimmt der Boden (Befund-Text); 65 504 cm = 655 m, weit über 190 m |
| [Forum] „ShallowWaterRiver and Landscape“ | nach dem Backen „Wasserwand“, die beim Näherkommen verschwindet, an wechselnden Stellen | Darstellung, nicht Simulation |
| [Forum] japanischer Faden „ShallowWaterRiver“ (16c) | gebackene Daten liegen je SWR; zwei SWR an einem Fluss → an der Verbindung fehlt das Netz; Rat: **eine** SWR mit mehreren Flüssen | gegen das Teilen (Frage 4) |
| [Forum] „UE 5.7 Water Plugin – Baking fails after adding an additional WaterRiver“ | Backen scheitert nach einem weiteren River | Vorsicht beim „Arm“ |
| [Forum] japanischer Faden „waterzone“ | große Welt: eine Zone über die ganze Fläche, Water Bodies streamen, **Local Tessellation** an | falls eure Zone so eingestellt ist: siehe nächste Zeile |
| [Doku] Water-Meshing-Seite / `AWaterZone` | Local Tessellation: „die WaterInfoTexture stellt nur ein **gleitendes Fenster um die Ansicht** dar“, Größe `LocalTessellationExtent`; Textur und Quadtree werden zur Laufzeit neu gebaut | Fenster-Rand = gerade, achsparallele Kante |
| [Doku] `AWaterZone` | `ZoneExtent` (größte Ausdehnung), `WaterHeightExtents` (FVector2f), `GroundZMin`, `CaptureZOffset` („Höhe über der Zone, in der die WaterInfoTexture gerendert wird; angewandt **nach** dem größten Z aller Wasserkörper der Zone“), `bHalfPrecisionTexture` („16 oder 32 Bit je Kanal“) | Höhenbereich und Genauigkeit der Water-Info |
| [Doku] `FWaterInfoTextureRenderingParams` | dieselben Felder (`WaterZoneExtents`, `WaterHeightExtents`, `GroundZMin`, `CaptureZ`) als Render-Parameter | Water-Info wird von oben in einem Höhenbereich gerendert |
| [Doku] `UShallowWaterRiverComponent` | Felder u. a. `bMatchSpline`, `MatchSplineHeightAmount`, `RemoveOutsideSplineAmount`, `bDisableCPUThrottling`, Baked-Texturen; `water_info_texture` (2D-Array, nur lesen) | SWR hat eine **eigene** Water-Info-Textur; „CPU Throttling“ ohne Beschreibung |
| [Doku] Water-Abfragen (`QueryWaterInfoClosestToWorldLocation`, `FindInputKeyClosestToWorldLocation`) | Abfrage über den **nächsten Spline-Schlüssel zur Weltposition** | erklärt Befund 6 (1.3 a) |
| [Fach] Flachwassergleichungen auf steilem Gelände (UCLouvain; Fenton; Van Emelen u. a.) | klassisch für kleine Sohlneigung hergeleitet („typisch < 10 %“), Abweichungen „erheblich über 20°“ (= 36 %); auf steilem Gelände ist der Druck nicht hydrostatisch; Korrektur mit g·cos²θ bzw. angepasster Manning-Rauheit | SWR wird in 30–60-%-Rinnen ungenau, aber nicht stillstehend |
| [Fach] Montgomery & Buffington 1997 | Gerinnetypen: Stufen-Becken 3–6,5 %, Kaskade > 6,5 %, darüber Fels/Kolluvium | 30–60 % ist weit jenseits; ein 2D-Höhenfeld zeigt hier nur „Treppe mit Rinnen“ |

**Nicht gefunden:** eine dokumentierte Gefällegrenze der SWR, eine Grenze der Höhenspanne je Fläche, Hinweise zu vielen
LINEAR-Punkten oder zu Quellen am Rand. Release Notes 5.6–5.8 nennen in den Auszügen keine SWR-Änderung zu Gefälle oder Höhe.

### 1.3 Physikalisch-numerische Analyse [Ableitung]

**a) Befund 6: Abfrage mit z = 0**

- Die Wasserabfrage am Water Body sucht den nächsten Spline-Schlüssel zur **3D**-Position [Doku, Funktionsname]. Von (x, y, 0)
  aus ist das bei einer schrägen Spline ein Punkt **talwärts**. Dort ist die Spline tiefer.
- Für eine gerade Rampe mit Gefälle m, Abfragehöhe z_ref und Spiegelhöhe z(s) über der Abfragestelle gilt:
  Δs = m · (z(s) − z_ref) / (1 + m²), Δz = m · Δs.

| m | z(s) − z_ref | Δs | Δz (Abfrage zu tief) |
|---|---|---|---|
| 0,21 | 190 m | 38 m | 8 m |
| **0,39** | **190 m** | **64 m** | **25 m** |
| 0,50 | 170 m | 68 m | 34 m |
| 0,64 | 150 m | 68 m | 44 m (praktisch begrenzt, weil der Durchbruch flach ist) |

- Das passt zu „bis 30 m unter dem Plan“. **Abhilfe:** mit z = Planspiegel (oder Gelände + 1 m) abfragen. Dann muss die
  Abweichung unter 0,1 m fallen (T0-1).
- **Auffällig:** Δs = 64 m bei s = 0 liegt nahe an der Abbruchkante s ≈ 62 m. Ob die SWR intern ebenfalls in 3D mit fester
  Bezugshöhe sucht, ist nicht belegt. Mit diesem Modell entstünde keine gerade Kante; deshalb steht es unter Rang 1 nur als
  Variante. T3-3 prüft es: Hängt die Kante an der z-Lage des SWR-Akteurs?

**b) Stillstand, Durchfluss und Tempo**

| Durchfluss Q (4 m breit, k_St 15) | 2 % (Kies) | 16 % | 39 % (Rinne) | 64 % |
|---|---|---|---|---|
| 0,3 m³/s | 0,14 m / 0,56 m/s | 0,07 m / 1,0 m/s | 0,06 m / 1,35 m/s | 0,05 m / 1,6 m/s |
| 1 m³/s | 0,28 m / 0,90 m/s | 0,15 m / 1,7 m/s | 0,11 m / 2,2 m/s | 0,10 m / 2,5 m/s |
| 5 m³/s | 0,73 m / 1,7 m/s | 0,39 m / 3,2 m/s | 0,30 m / 4,2 m/s | 0,26 m / 4,8 m/s |
| 15 m³/s | 1,41 m / 2,7 m/s | 0,76 m / 5,0 m/s | 0,58 m / 6,5 m/s | 0,50 m / 7,5 m/s |

(Normaltiefe / Tempo, Rechteckgerinne. In Becken gilt Rückstau, nicht Normalabfluss.)

- Über einer Lippe stellt sich die Grenztiefe h_c = (q²/g)^(1/3) ein: q = 0,1 m²/s → **10 cm**; 0,2 → 16 cm; 0,3 → 21 cm.
  Bei Q 0,3–1 m³/s auf 3–4 m Breite ist der Überfall 7–15 cm dick.
- **Folgerung:** Eine Trockenschwelle oder eine Reibung ∝ 1/h, die dünne Schichten stark bremst, wirkt genau an den Lippen. Die
  Becken bleiben dann voll, der Überlauf erstickt (Rang 5).

**c) Zeitschritt und Geschwindigkeitskappung**

- Freier Fall über eine Stufe: v = √(2 g Δz) → 1,6 m: 5,6 m/s; 3,7 m: 8,5 m/s. Ohne Becken über 24 m Höhe: 22 m/s.
- Stabilitätsgrenze (CFL ≤ 1): Δt ≤ Δx / (|v| + √(g h)).

| Zelle | v = 5 m/s | v = 8,6 m/s | v = 10,24 m/s | v = 20 m/s |
|---|---|---|---|---|
| 0,25 m | 34 ms | 23 ms | 20 ms | 11 ms |
| 0,37 m | 50 ms | 34 ms | 29 ms | 17 ms |

- Zeitschritt je Teilschritt [Ableitung aus Epic: „Speed beschleunigt das Einschwingen, Substeps ≥ Speed“]:
  Bildzeit × `sim_speed` / `num_steps`. Bei 40 fps: 10/10 → **25 ms**, 10/20 → 12,5 ms, 5/20 → 6,3 ms.
- 25 ms reichen bei 0,37 m Zelle bis etwa 10 m/s. Bei 0,25 m Zelle und Fallfüßen ab 3 m wird es knapp. Eine Kappung bzw.
  Dämpfung im Löser verhindert dann Explosionen. Sie macht das Wasser langsamer, aber **nicht stillstehend**.
- `MaxFlowVelocity` 1024 cm/s ist nur die Kodiergrenze der Strömung in der Water-Info-Textur (16e). Sie bremst die Simulation
  nicht. Im Spiel (WCBS) werden Werte über 10,24 m/s gekappt dargestellt.

**d) Reibung und Velocity Dissipation**

- Epic: Friction bremst flaches Wasser und stabilisiert [Epic lokal].
- Ein Stillstand von 0,6 m tiefem Wasser durch Reibung allein ist unplausibel. In tiefen Becken wirkt sie kaum.
- An den dünnen Lippen-Überfällen aber stark (b). Habt ihr in der Niagara-Kopie Friction × 2 gesetzt (16f, Abschnitt 5), dann
  für die Diagnose zurück auf den Standard (T5-2).

**e) Höhenspanne und 16 Bit**

| Größe | Wert | Grenze | Folge |
|---|---|---|---|
| Gelände in der Fläche | 36–190 m | Half Float 65 504 (cm) = 655 m | kein Überlauf |
| Tiefe unter Capture-Ebene (190 m + Offset) | bis ~154 m + Offset | 655 m | kein Überlauf |
| Raster von Half Float bei 106 m / 190 m Höhe (absolut in cm) | 8 cm / 16 cm | – | Spline-Höhe ± 4–8 cm; kann kein Austrocknen erklären |
| Raster bei Tiefe 82–164 m unter Capture | 8 cm | – | Boden ± 4 cm; euer Befund „auf cm“ spricht gegen 16-Bit-Boden |
| Exponentwechsel 2¹⁴ cm | **163,84 m** | – | Prüfzahl: Kante bei z ≈ 163,8 m wäre ein Indiz (T0-2) |

**f) Bodenerfassung relativ zum Rechteck**

- Erfasst wird von oben (Tiefenaufnahme). Eure Messung zeigt: Boden = Gelände entlang des Laufs.
- **Ausnahme:** Überhänge im Durchbruch (Felsnetze, `WH_`-Felsen über dem Wasser) werden zur Wand (16a d1). Im Bild
  `Debug Bottom Contour` den Durchbruch quer ansehen (T0-2).

**g) Spline-Höhe aus einer 2D-Textur**

Eine Höhe je Texel. In steilem Gelände steigt der Fehler mit Texelgröße × Gefälle:

| Texel | 21 % | 39 % | 64 % | Herkunft |
|---|---|---|---|---|
| 0,37 m | 0,08 m | 0,14 m | 0,24 m | = Simulationszelle (2016 über 741 m) |
| 0,72 m | 0,15 m | 0,28 m | 0,46 m | 1024 über 741 m |
| 1,18 m | 0,25 m | 0,46 m | 0,76 m | Zonen-Water-Info bei C2 (14b) |
| 1,45 m | 0,30 m | 0,57 m | 0,93 m | 512 über 741 m |
| 2,9 m | 0,61 m | 1,13 m | **1,86 m** | 256 über 741 m |

- Wird die obere Kante des Texels genommen (Draufsicht, nächste Fläche zur Kamera), liegt das Ziel um diesen Wert **zu hoch**.
- Befund 4 (+1,4 m in der Rinne) passt zu 256–512 Texeln. Bei der Simulationszelle wäre der Fehler nur 0,1–0,2 m.
- Das betrifft auch „innen/außen“: Eine schmale steile Rinne (3–5 m) ist bei 2,9-m-Texeln nur 1–2 Texel breit.

**h) Quelle am Rand**

- Die Quelle liegt 0,2 m vom Nordrand (Befund 8). Ein Quellbereich von 3 m (10 m) liegt also zu ~45 % außerhalb.
- Bei offenem Rand fließt ein Teil des eingespeisten Wassers sofort nach Norden ab, weil das Wasser am Quellpunkt in alle
  Richtungen auseinanderläuft.

**i) Remove-outside nach einer 2D-Maske**

- Wird die Maske aus derselben gerasterten Water-Info gebildet und endet diese Textur (Ausdehnung, Fenster, Höhenbereich), ist
  hinter der Grenze alles „außen“. Rate 50 löscht dort sofort.
- Das ist genau Befund 1. Es erklärt auch, warum die Nachfüllrate (0,05 / 0,3 / 2) nichts an der Lage ändert.

**j) Korrelation von s ≈ 62 m mit einer Höhendifferenz**

Mit Quelle 190 m (+0,3 m) und im Mittel 39 % liegt s = 62 m bei etwa **z ≈ 166 m**, also ~24 m unter der Quelle. Wegen des
Gefälles von 21–64 % kann z(62) zwischen etwa 150 und 177 m liegen. **Bitte den echten Wert aus dem Plan nennen** (T0-2).
Vergleich mit möglichen festen Grenzen:

| Kandidat | z an der Kante wäre | trifft zu, wenn … | Test |
|---|---|---|---|
| fester Höhenbereich unter der Capture-Ebene (Zone/SWR: max. Wasser-Z + `CaptureZOffset` − Bereich) | 190,3 m − Bereich (z. B. 20,48 m → 169,8 m; 25,6 m → 164,7 m) | die Kante wandert mit `CaptureZOffset` bzw. mit der höchsten Wasserfläche | T3-2 (`CaptureZOffset` + 50 m) |
| Half-Float-Exponentwechsel 2¹⁴ cm | 163,84 m | Kante liegt auf einer Höhenlinie bei 163,8 m und wandert nicht mit der Capture-Ebene | T3-2 (32 Bit) |
| 3D-Abfrage mit z_ref = 0 | s = 64 m | Kante wandert mit der Lage des SWR-Akteurs bzw. der Bezugshöhe | T3-3 |
| Rand der Zonen-Textur bzw. des Tessellations-Fensters | keine Höhenbeziehung, **achsparallel** | Kante ist achsparallel und liegt am Rand von `ZoneExtent` bzw. `LocalTessellationExtent` | T0-2, T0-3, T3-2 |
| Rand der SWR-eigenen Water-Info | achsparallel | Kante liegt auf einer Rechteck-Teilung (z. B. 1/12 von 741 m = 62 m!) | T0-3 |

- **Zur letzten Zeile:** 741 m / 62 m ≈ 12. Eine Kachelung der Water-Info mit 12 Stücken wäre ein Zufallstreffer. Ich nenne sie
  nur, weil die gerade Kante zu einem Kachelrand passt.
- **Entscheidend ist die Richtung der Kante:**
  - Läuft der Bach bei s 62 m nicht genau nord-südlich und ist die Kante trotzdem genau west-östlich, ist es ein
    Textur-/Zonenrand.
  - Steht sie senkrecht zum Lauf, ist es eher eine Höhenlinie.

---

## 2. Frage 2 – Wie speist die Quelle ein, und wie viel?

### 2.1 Was belegt ist

- **Header (Befund 8):** Quelle und Senke über `QueryWaterAtSplinePoint(WaterBody, SplinePoint, OutPos, OutTangent, OutWidth,
  OutDepth)`, also am ersten bzw. letzten Splinepunkt. Rückgabe: Lage, Tangente, Breite, Tiefe. **Kein Tempo.**
- **Epic [Epic lokal]:** `source_size` = Größe des Bereichs, aus dem an der Quelle Wasser austritt; „Standard meist gut“.
- **Daraus [Ableitung]:**
  - Die Quelle ist sehr wahrscheinlich eine **Höhen- bzw. Tiefenvorgabe** im Bereich `source_size` um `OutPos`, vermutlich
    entlang der Tangente ausgerichtet.
  - Die Breite begrenzt quer, die Tiefe bestimmt den Wasserstand.
  - Das Spline-Tempo am ersten Punkt (`WaterVelocityScalar`) wirkt vermutlich **nicht**. Der Abfluss entsteht aus dem
    Wasserstand, der talwärts überläuft.
  - Ob „Tiefe“ die Spline-Tiefe (`Depth`, Bett unter Spiegel) oder Spiegel − Boden ist, ist offen [unsicher].

### 2.2 Abfluss rechnen (Modell: Überfall aus einem Becken, Grenzabfluss)

Läuft Wasser aus einem Becken mit Wasserstand H über Grund in eine steile Rinne, stellt sich am Ausgang die Grenztiefe ein:
q = (2/3)^(3/2) · √g · H^(3/2) ≈ **1,705 · H^1,5** (m²/s), Q = b · q.
Das ist eine **Obergrenze**: Ist die Quelle eine Rate (wie das Nachfüllen), kommt weniger.

| Fall | H (Wasser über Grund an der Quelle) | b (wirksame Breite) | **Q** |
|---|---|---|---|
| heute, `source` 300 cm, halber Bereich außerhalb | 0,67 m (Plan) | 1,5 m | 1,4 m³/s |
| heute, `source` 300 cm, Spline +0,3 m | 0,97 m | 1,5–3 m | 2,4–4,9 m³/s |
| heute, `source` 1000 cm (Befund 4), Bett ~4 m | 0,97 m | 4 m | 6,5 m³/s |
| **Empfehlung**, Quellbecken innen, b = Bettbreite 3 m | **0,25 m** | 3 m | **0,64 m³/s** |
| **Empfehlung**, b = 4 m | **0,30 m** | 4 m | **1,1 m³/s** |
| Wildbach 2 m, ruhig | 0,15 m | 2 m | 0,20 m³/s |
| Wildbach 8 m, Hochwasser-Optik | 0,40 m | 8 m | 3,4 m³/s |

- **Abgleich mit der Messung:** Die Rinne (199 m × ~3,5 m × ~0,45 m ≈ 310 m³) war in 90 s voll.
  - Zählt `sim_speed` 10 als Zeitraffer (900 s Simulationszeit), sind das ≈ **0,35 m³/s**; ohne Zeitraffer 3,5 m³/s.
  - Der Durchbruch-Pool (90 m × 5 m × 0,7 m ≈ 315 m³) wäre mit 0,35 m³/s in weiteren 15 min Simulationszeit (≈ 90 s Echtzeit)
    voll. Nach 5 min ist er es nicht.
  - Also geht der Zufluss unterwegs verloren (Rang 1/3/4), oder er versiegt nach dem ersten Auffüllen (Rang 2).
- **Natürlicher Rahmen [Fach, Lehrbuchwerte]:** Ein 2–8 m breiter Wildbach führt bei Mittelwasser etwa 0,2–2 m³/s. Für sichtbares
  Weißwasser in einer Stufen-Becken-Folge reichen 0,5–1,5 m³/s. Die empfohlenen 0,6–1,1 m³/s liegen darin.

### 2.3 Was am ersten Punkt stehen soll (damit dauerhaft Wasser nachläuft)

| Punkt | Wert | Grund |
|---|---|---|
| Lage | **≥ 10 m innerhalb des Rechtecks**: Spline 10 m die Felsrinne hinauf verlängern (Vorlauf, 3–4 Punkte) | Rechteck = Box der Splinepunkte; nur so liegt die Quelle innen |
| Quellbecken | die letzten 4–6 m des Vorlaufs **waagrecht**, Bett 0,3–0,5 m unter dem Spiegel (Mulde im Fels; nur Gelände, kein Brush) | stabiler Wasserstand, Überlauf in die Rinne |
| Tiefe am ersten Punkt | so, dass der Spiegel **0,25–0,35 m** über dem Quellbecken-Grund liegt | Q 0,6–1,1 m³/s (Tabelle 2.2) |
| Breite | Bettbreite (3–4 m), nicht Bett + 2 m | wirksame Breite |
| `source_size` | = Bettbreite (300–400 cm) | 16f-Regel bleibt |
| Tangente | in Fließrichtung, flach (Punkttyp CURVE_CLAMPED bzw. LINEAR) | kein Überschwingen über den Rand |
| Tempo | 0,2–0,5 m/s (wirkt vermutlich nicht) | nur für Ferne und Abfragen |
| Erster Punkt +0,3 m | **weg** (Spiegel = Plan) | +0,3 m hebt H und Q um den Faktor (0,97/0,67)^1,5 = 1,7, löst aber das Randproblem nicht |

---

## 3. Frage 3 – Wie bestimmt die SWR „innerhalb der Spline“ und die Spline-Höhe?

- **Belegt** ist nur:
  - Die SWR hat eine eigene `water_info_texture` (`TextureRenderTarget2DArray`, nur lesen) [Doku].
  - `match_spline_height_amount` ist die Nachfüllrate für Zellen „unter der Spline-Höhe“, `remove_outside_spline_amount` die
    Löschrate „außerhalb der Spline“ [Epic lokal].
  - Quelle/Senke werden am ersten bzw. letzten Splinepunkt abgefragt (Befund 8).
- **Sehr wahrscheinlich [Ableitung]:**
  - Die SWR liest beides aus einer **Draufsicht** der Quell-Flüsse: ihre eigene Water-Info bzw. die der Zone (Wasserhöhe,
    Abdeckung).
  - Eine Draufsicht ist **2D**: eine Höhe und eine Abdeckung je Texel. In steilem Gelände ergibt das Texelgröße × Gefälle als
    Fehler (1.3 g).
  - Hat die Aufnahme einen begrenzten Bereich (Fläche oder Höhe), fehlt die Information dahinter ganz (1.3 i).
  - Ein CPU-Abgleich je Zelle über die nächste 3D-Spline-Stelle ist weniger wahrscheinlich. Er gäbe keine gerade Kante.
- **Einstellungen, die das beheben könnten** (je eine Prüfung im Testplan):

| Einstellung | wo | Wert für den Test | Wirkung, falls Ursache |
|---|---|---|---|
| Local Tessellation | Water Zone | aus, bzw. `LocalTessellationExtent` ≥ Rechteck + 100 m | Water-Info deckt den ganzen Fluss |
| `ZoneExtent` | Water Zone | Zone deckt das SWR-Rechteck + 100 m | dito |
| `bHalfPrecisionTexture` | Water Zone | **aus** (32 Bit) | genauere Höhen; Exponent-Grenzen fallen weg |
| `CaptureZOffset` | Water Zone | +50 m (5000) | Kante wandert, wenn ein Höhenbereich begrenzt |
| Render-Target-Auflösung der Zone (`RenderTargetResolution`, Editor-Vorgabe [Doku]) | Water Zone | doppelt | Texel halb so groß → Fehler aus 1.3 g halbiert |
| SWR `resolution_max_axis` | SWR | 2016 lassen | vermutlich auch Auflösung der SWR-Water-Info [unsicher] |
| Spline-Punkttypen | River | Lippen LINEAR lassen; zwischen den Stufen CURVE_CLAMPED; **keine** Tangenten, die über den Lippenpunkt hinausschießen | glatte Draufsicht ohne Rückwärts-Schleifen |
| River-Mesh / Water-Info-Netz | River | – | keine Einstellung bekannt |

- `bDisableCPUThrottling` an der SWR ist unbeschrieben. Der Name deutet auf ein Drosseln der CPU-Seite (z. B. Aktualisierung
  der Quell- und Spline-Daten) hin [unsicher]. In T3-2 einmal **an** setzen, ohne Erwartung.

---

## 4. Frage 4 – Wildbach 2–8 m, 30–60 %, Stufen 1–3 m: Einstellungen und Teilung

### 4.1 Startwerte (nach T1–T5 anpassen)

| Feld | Wert | Begründung |
|---|---|---|
| Zelle | **0,25 m** (2-m-Bach: 8 Zellen quer); höchstens 0,30 m | steile Rinnen brauchen ≥ 8 Zellen quer, sonst ist die Rinne 1–2 Texel |
| `resolution_max_axis` | nach Zelle (≤ 2048) | wie Export |
| `sim_speed` / `num_steps` | **5 / 20** (Steilstrecken), sonst 10 / 10 | 6 ms je Schritt statt 25 ms; Stabilitätsreserve für Fallfüße bis 8,6 m/s bei 0,25 m (1.3 c) |
| Friction (Niagara-Kopie) | **Standard** (× 1); bei erstickten Lippen × 0,5 | Reibung wirkt auf dünne Überfälle (1.3 b) |
| Velocity Dissipation | Standard | – |
| Smoothing Width / Cutoff | Standard; nur bei Treppen-Artefakten + 1 Zelle | Epic: für harte Kanten |
| `match_spline` | an | Überlauf-Schutz |
| `match_spline_height_amount` | **0** für die Diagnose; danach 0–0,02 | hält sonst Becken auf Lippenhöhe ohne Durchfluss |
| `remove_outside_spline_amount` | **0**, bis T3 die Maske über den ganzen Lauf zeigt; dann 50 | sonst löscht sie hinter einer fehlerhaften Maske alles |
| Quelle | Abschnitt 2.3 (Vorlauf 10 m, Quellbecken, H 0,25–0,35 m, `source_size` = Bettbreite) | Q 0,6–1,1 m³/s |
| Spline-Breite | Bett + 2 m (wie jetzt) | Maske etwas weiter als das Bett |
| Becken/Lippen | Becken waagrecht, Lippe LINEAR (wie jetzt) | – |

### 4.2 Teilen in mehrere Simulationsflächen

- **Mit der belegten API nicht möglich, ohne den Fluss zu teilen** [Ableitung aus 16c und Befund 8]:
  1. Das SWR-Rechteck ist die Box um **alle** Quell-Flüsse. Eine zweite SWR mit demselben Fluss bekommt dasselbe Rechteck.
     Eine Eigenschaft für eigene Grenzen ist nicht gefunden (16c T1/T2).
  2. Gespeist wird nur am **ersten** Punkt jedes Quell-Flusses. Eine untere SWR bekäme das Wasser der oberen nicht. Zwischen
     zwei SWR gibt es keine Kopplung.
  3. Zwei SWR über demselben Fluss überschreiben sich beim Backen [Forum, 16c].
- **Prüfen:** Im Header `ShallowWaterRiverActor.h` (T0-3) nach Eigenschaften mit `Bounds`, `Extent`, `Box`, `Domain` oder
  `Override` suchen. Gibt es eine, beschreibe ich die Teilung mit Überlappung neu (8 m Überlappung, Naht in einem Becken, die
  obere Fläche endet unter der Naht, die untere bekommt einen Speisepunkt).
- **Empfehlung bis dahin:** eine SWR je Fluss (wie v3). Lange steile Rinnen nicht teilen, sondern Plan B (Abschnitt 5). Die
  Export-Teilung für Flüsse > 614 m bleibt „vorläufig“ wie in v3.

---

## 5. Frage 5 – Plan B: Was statt SWR in steilen Rinnen?

### 5.1 Kriterium (Vorschlag, Export-Feld `rand_steil.eignung`)

Spiegelgefälle im gleitenden 20-m-Fenster (Stufen zählen mit), zusammenhängende Strecke ≥ 50 m:

| Klasse | Gefälle (20 m) | Werkzeug | Begründung |
|---|---|---|---|
| `swr` | < 15 % | SWR | Flachwassergleichungen gut (< 10 %) bis brauchbar; Befund 9: 102 → 37 m lief |
| `pruefen` | 15–30 % | SWR mit Testbild; Stufen ≥ 1,5 m als Fall mit Schaumobjekten | 16a T1: 40 m mit 36 % liefen (schnell, Schaum) |
| `kaskade_vorschlag` | ≥ 30 % über ≥ 50 m | **Kaskadennetz** + Flowmap + Schaumobjekte + Niagara; SWR erst ab dem Fuß | Druck nicht hydrostatisch (Fehler „erheblich über 20°“ = 36 %) [Fach]; Fallstrahlen 1–3 m sind im Höhenfeld nur Rinnen; CFL-Grenze; Befund 1–4 |

Die Grenzen 15 % / 30 % / 50 m sind vorläufig. Der Rampentest (T4) setzt sie fest.

### 5.2 Werkzeugkette UE 5.8 (Witcher-Qualität)

1. **Fluss bleibt ein `WaterBodyRiver`** von 190 m bis zur Mündung (Ferats Entscheidung). Er liefert Auftrieb, Schwimmen und
   Abfragen, auch in der Steilstrecke.
2. **Steile Rinne (Bergrinne 0–199 m):**
   - **Kaskadennetz aus A15** (`gefaelle_plan.bauen_wasser_A`, schon vorhanden) als Wasseroberfläche.
   - Material mit **Flowmap entlang der Mittellinie** (UV-u = s), zweiphasiges Flowmap-Blending der Normalen, Schaummaske aus
     Lippe/Fuß und Krümmung, Tiefe über Depth Fade.
   - **Schaumobjekte** (Aufprallteppich, Schaumstraßen, Kehrwasser; 16 Nachtrag), **Niagara-Gischt** (Nature Water FX) ab
     Stufen ≥ 1 m, Vorhang ab 3 m (Regel wie 16b).
3. **Übergabe an die SWR am Fuß der Steilstrecke (Speisepunkt):** Weil die SWR nur am ersten Punkt eines Quell-Flusses speist,
   braucht sie dort eine Quelle. Zwei Wege [Ableitung, beide im Test]:
   - **S1 (empfohlen):** Ein kurzer Hilfs-`WaterBodyRiver` (`WBR_<fluss>_SPEISUNG`, 2–3 Punkte, 6–10 m, im Bett am Kopf des
     Durchbruchs) kommt als **zweite Quelle** in die SWR. `affects_landscape` aus, kein eigenes Netz im Spiel. Der Erlenbach
     bleibt Quelle (für Maske und Spline-Höhe), bekommt aber am ersten Punkt eine minimale Tiefe (1–2 cm), damit dort nichts
     eingespeist wird.
   - **S2:** wie heute, die SWR speist oben. Die Bergrinne simuliert mit, wird im Spiel aber vom Kaskadennetz überdeckt. Das
     geht nur, wenn WCBS dort keine zweite Wasserfläche zeichnet. Das ist unwahrscheinlich sauber.
4. **Flache und mittlere Abschnitte** (Durchbruch, Talkaskade bis 30 %, Kiesbett): SWR gebacken, WCBS, wie 16/16f.
5. **Nicht empfohlen:**
   - **Niagara Fluids 2D (Grid 2D SW):** dieselben Flachwassergleichungen, dasselbe Problem auf Steilstrecken, dazu Eigenbau
     der Bodenerfassung.
   - **Niagara Fluids 3D FLIP:** nur für **einen** Schau-Wasserfall mit Simulations-Cache. Für 200 m Rinne zu teuer.
   - **Fluid Flux** (kostenpflichtig): wirbt mit „besserer Qualität auf Hängen“ in 2.0 [Blog]. Bleibt draußen (Entscheidung 16).
   - **Gebackene Flowmaps aus einer Offline-Simulation** (Houdini o. Ä.): Qualität wie Kaskadennetz, aber eine neue Pipeline.
     Erst, wenn das Kaskadennetz nicht reicht.

---

## 6. Testplan (Reihenfolge, Werte, Messgröße)

**Grundsatz:** erst ansehen, ohne zu simulieren (Stufe 0), dann die Bilanz messen (Stufe 1), dann je Ursache ein Lauf. Jeder
Lauf: Werte setzen → **Reset** → 120 s laufen lassen → Messung. Ein „Bake“ nur zum Auslesen mit `swr_dump_baked`.

**Messgrößen** (wie bisher aus der gebackenen Textur, 1-m-Raster):
- **V(t)**: Wasservolumen Σ Tiefe × 1 m² in der ganzen Fläche und je Abschnitt (Bergrinne, Durchbruch, Talkaskade, Kies), bei
  t = 30 / 60 / 120 s.
  - Bricht Bake die Simulation ab, je Zeitpunkt einen eigenen Lauf; die Simulation ist deterministisch [vermutlich].
- **Nass-Anteil** je Abschnitt und **Front-s** (letzte nasse Stelle im Bett).
- **Tempo an 5 Lippen** der Bergrinne und an 2 Stellen im Durchbruch (Render State mit Velocity-Debug bzw. Niagara-Partikel).
  Durchfluss Q ≈ Σ(Tiefe × Tempo) quer über die Lippe.
- **Abbruchkante:** s, z, Richtung (Winkel zur x-Achse) und Abstand zum Rechteckrand.

### Stufe 0 – ohne neue Simulation (15 min)

**T0-1 Befund 6 nachmessen (mit richtiger Höhe).** Erwartung: Abweichung < 0,1 m.

```python
import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
akt = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
wb = akt['WBR_F_ERLENBACH']                                       # Label eures C2-Flusses einsetzen
wbc = wb.get_component_by_class(unreal.WaterBodyComponent)
sp = wb.get_component_by_class(unreal.SplineComponent)            # WaterSplineComponent ist eine SplineComponent
W = unreal.SplineCoordinateSpace.WORLD
for i in range(0, sp.get_number_of_spline_points(), 10):
    p = sp.get_location_at_spline_point(i, W)
    for z in (0.0, p.z + 50.0):                                    # alt (z = 0) und neu (Planspiegel + 0,5 m)
        info = wbc.get_water_surface_info_at_location(unreal.Vector(p.x, p.y, z))
        print(i, round(p.z / 100, 2), z, info)                     # Form der Rückgabe wie in eurem Befund 6
```

**T0-2 Geometrie: Extrempunkte, Kante, Arm.**

```python
xs = [(sp.get_location_at_spline_point(i, W), i) for i in range(sp.get_number_of_spline_points())]
for name, f in (('W', lambda t: t[0].x), ('O', lambda t: -t[0].x), ('S', lambda t: t[0].y), ('N', lambda t: -t[0].y)):
    p, i = min(xs, key=f)
    print(name, 'Punkt', i, 'z', round(p.z / 100, 2), 'x,y', round(p.x), round(p.y))
# s je Punkt: sp.get_distance_along_spline_at_spline_point(i) / 100
# dasselbe für den Arm (zweiter Quell-Fluss): erster und letzter Punkt, Abstand zum Erlenbach
```

- Notieren:
  1. Bei welchem s liegen die West-/Ost-Extreme? Liegt eines bei s 199–231 m → Rang 3 sehr wahrscheinlich.
  2. z des Plans bei s = 62 m (Vergleich mit 1.3 j).
  3. Richtung der Abbruchkante aus dem Dump von Befund 1: achsparallel oder senkrecht zum Lauf?
  4. Wo beginnt und endet der Arm?
- Bild `Debug Bottom Contour` quer über den Durchbruch: Überhänge?

**T0-3 Eigenschaften und Texturen auslesen (Namen mit `dir()`, nicht raten).**

```python
swr = next(a for a in eas.get_all_level_actors() if isinstance(a, unreal.ShallowWaterRiver))
c = swr.get_component_by_class(unreal.ShallowWaterRiverComponent)
rt = c.get_editor_property('water_info_texture')
print(rt, [n for n in dir(rt) if any(k in n for k in ('size', 'slice', 'format'))])
for n in ('size_x', 'size_y', 'slices'):                          # vermutete Namen, mit hasattr gesichert
    print(n, rt.get_editor_property(n) if hasattr(rt, n) else '-')
print([n for n in dir(c) if any(k in n.lower() for k in ('throttl', 'bound', 'extent', 'box', 'domain', 'source', 'sink', 'spline'))])
zonen = [a for a in eas.get_all_level_actors() if isinstance(a, unreal.WaterZone)]
for z in zonen:
    print(z.get_actor_label(), z.get_actor_location(),
          [n for n in dir(z) if any(k in n.lower() for k in ('extent', 'tessell', 'half', 'capture', 'resolution', 'ground', 'height'))])
```

- Dann die gefundenen Felder mit `get_editor_property` ausgeben: Zonen-Ausdehnung und -Lage, lokale Tessellation (an/aus,
  Größe), 16/32 Bit, `capture_z_offset` (Python-Name belegt [Doku]).
- **Prüfen:**
  - Deckt die Zone (bzw. das Tessellations-Fenster) das SWR-Rechteck 118 × 741 m ganz ab?
  - Liegt ein Rand bei s ≈ 62 m?
  - Ist die Water-Info-Textur der SWR ≤ 512 Texel (dann passt 1.3 g zu Befund 4)?
- **Header lesen (eure lokale Installation, nur lesen):**

```powershell
$h = "C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Experimental\WaterAdvanced\Source\WaterAdvanced\Public"
Select-String -Path "$h\*.h" -Pattern "UPROPERTY|UFUNCTION" -Context 0,2 | Select-String -Pattern "Bounds|Extent|Throttl|Source|Sink|Spline|WaterInfo|Capture"
```

Pfad an eure Installation anpassen. Bitte die Treffer mit den Kommentaren (Tooltips) schicken.

### Stufe 1 – Bilanz (2 Läufe, je 5 min)

| Lauf | Einstellungen (sonst wie heute) | Erwartung, wenn … | Messung |
|---|---|---|---|
| **T1-1** | `remove` **0**, `match_height` **0**, `source` 300 cm | Quelle speist kaum → Rinne füllt sich langsam oder nur oben; Lippen-Tempo ≈ 0 | V(t) je Abschnitt, Front-s, Lippen-Tempo |
| **T1-2** | wie T1-1, `match_height` 0,02 | Nachfüllen hält die Becken voll → Rinne 99 % wie Befund 2, Lippen-Tempo ≈ 0 | dto. |

- **Auswertung:**
  - Steigt V(t) in T1-1 nicht über das Rinnenvolumen und hat die Front nach 120 s den Durchbruch nicht erreicht → **Quelle**
    (Rang 2).
  - Fällt V(t) nach Erreichen einer Stelle nicht weiter, obwohl Wasser dorthin fließt → **Verlust** (Rang 3/4). Der Ort ist
    die Stelle, an der das Lippen-Tempo noch > 0 ist, dahinter aber trocken.

### Stufe 2 – Quelle und Rand (2 Läufe)

| Lauf | Änderung | Erfolg, wenn | Messung |
|---|---|---|---|
| **T2-1** | Spline 10 m die Felsrinne hinauf verlängern; Quellbecken 4–6 m waagrecht, H 0,3 m; `source` 300–400 cm; erster Punkt ohne +0,3 m; sonst T1-1 | Q (aus V(t) vor Erreichen des Durchbruchs) 0,5–1 m³/s; Lippen-Tempo 1–2,5 m/s; Front erreicht den Durchbruch | V(t), Front-s, Q |
| **T2-2** | nur wenn T0-2 einen Extrempunkt bei s 199–231 zeigt: Hilfs-River „Rahmen“ (2 Punkte, 10 m außerhalb der Ecken des Soll-Rahmens aus dem Export `rand_steil.rahmen_cm`, z 5 m **unter** dem Gelände, Tiefe 1 cm) als zusätzliche Quelle | Rechteck wächst, Front läuft über s 231 hinaus | `swr_info` (Rechteck), Front-s |

- **T2-2 ist ein Behelf [Ableitung]:** Ein River unter dem Gelände sollte nichts einspeisen, vergrößert aber das Rechteck. Speist
  er doch, sofort abbrechen. Dann bleibt nur, den Lauf selbst um den Extrempunkt zu verlegen, oder eine echte Rand-Einstellung aus
  dem Header (T0-3).

### Stufe 3 – Spline-Information (3 Läufe)

| Lauf | Änderung | Deutung |
|---|---|---|
| **T3-1** Teilfläche Bergrinne | Kopie des Erlenbachs, nur Punkte s 0–240 (Vorlauf aus T2-1), eigene SWR, `remove` 50, `match_height` 0,02 | Kante bleibt bei s ≈ 62 → Höhe/Steilheit (1.3 j, Zeilen 1–3). Kante verschwindet → Ausdehnung der Water-Info/Zone (Zeilen 4–5) |
| **T3-2** Water Zone | 32 Bit (`bHalfPrecisionTexture` aus), lokale Tessellation aus bzw. Fenster ≥ Rechteck + 100 m, `CaptureZOffset` + 50 m; an der SWR `bDisableCPUThrottling` an; Reset | Kante wandert oder verschwindet → Zonen-Ursache; welche Änderung es war, in Einzelschritten (erst Tessellation, dann Offset, dann 32 Bit) |
| **T3-3** z-Lage | SWR-Akteur (nur ihn) um +50 m und −50 m in z verschieben, Reset | Kante wandert → 3D-Bezugshöhe (1.3 a); bleibt → nicht |

- **Ziel der Stufe:** Bei `remove` 50 ist das ganze Bett nass. Erst dann `remove` 50 wieder als Sicherheitsnetz nutzen.

### Stufe 4 – Rampentest R (synthetisch, 1 h, entscheidet SWR ja/nein für Steilstrecken)

- **Testkarte** ohne Landschaft. Eine 150 m lange Rampe aus einem skalierten Würfel (`/Engine/BasicShapes/Cube`), Tag
  `SWR_Hindernis`, in `bottom_contour_actors`. Darin eine Rinne aus zwei Wand-Würfeln (Rinne 4 m breit, 1 m tief).
- Darauf ein gerader River (Punkte alle 2 m, Breite 6 m, Tiefe 0,3 m), Quelle mit Vorlauf wie T2-1, eine SWR (Zelle 0,25 m).
- **Gegenprobe zu „Höhe künstlich flach“:** Eine Kopie des Geländes ist nicht nötig. Die Rampe trennt Höhe und Steilheit sauber.

| Variante | Fuß der Rampe | Gefälle | Stufen | Läufe |
|---|---|---|---|---|
| R1 | z 40 m | 10 % | keine | `remove` 0 / 50 |
| R2 | z 40 m | 40 % | keine | `remove` 0 / 50 |
| R3 | z 190 m | 40 % | keine | `remove` 50 |
| R4 | z 40 m | 40 % | 1,5 m alle 6 m (waagrechte Becken) | `remove` 0 / 50; `speed`/`steps` 10/10 und 5/20 |

- **Messung je Lauf:** Front-s nach 120 s, Nass-Anteil, Q, Tempo, Abbruchkante (s, z).
- **Deutung:**
  - R1 gut, R2 schlecht → Steilheit. R2 gut, R3 schlecht → absolute Höhe. R2 gut, R4 schlecht → Stufen bzw. Zeitschritt.
  - Alle gut → die Ursache liegt in eurem Level (Zone, Arm, Rand) und nicht in der SWR.
- **Python für die Rampe** (Namen belegt: `spawn_actor_from_class`, `set_actor_scale3d`, `StaticMeshComponent.set_static_mesh`):

```python
import math, unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
def rampe(fuss_z_m, gefaelle, laenge_m=150.0, breite_m=20.0, dicke_m=2.0, x0_m=0.0):
    w = math.degrees(math.atan(gefaelle))
    mitte_z = fuss_z_m + 0.5 * laenge_m * gefaelle
    a = eas.spawn_actor_from_class(unreal.StaticMeshActor,
                                   unreal.Vector(x0_m * 100, 0, mitte_z * 100 - dicke_m * 50), unreal.Rotator(0, w, 0))
    a.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube.Cube'))
    a.set_actor_scale3d(unreal.Vector(laenge_m / math.cos(math.radians(w)), breite_m, dicke_m))   # Würfel = 1 m
    a.set_editor_property('tags', [unreal.Name('SWR_Hindernis')])
    a.set_actor_label('RAMPE_%d_%d' % (fuss_z_m, round(gefaelle * 100)))
    return a
# Vorzeichen des Pitch so wählen, dass die Rampe zum Fuß hin fällt (Bild prüfen). River und SWR mit eurem Bau-Werkzeug,
# Quelle oben mit Vorlauf (T2-1).
```

### Stufe 5 – Numerik und Reibung (2 Läufe, mit dem besten Stand aus Stufe 2/3)

| Lauf | Änderung | Erfolg, wenn |
|---|---|---|
| **T5-1** | `sim_speed`/`num_steps` 5/20 statt 10/10 | Lippen-Tempo ruhiger, keine Löcher/Spitzen; Front gleich weit |
| **T5-2** | Niagara-Kopie: Friction × 0,5 (bzw. zurück auf Standard, falls × 2 gesetzt) | Lippen-Überfall dicker als 5 cm, Q steigt |

### Stufe 6 – Auflösung der Water-Info (1 Lauf, nur wenn T0-3 ≤ 512 Texel zeigt)

- Auflösung der Zone verdoppeln (bzw. die Einstellung, die T0-3 als Auflösung der SWR-Water-Info zeigt).
- Mit `match_height` 2 messen: Wasserstand in der Rinne gegen Plan.
- Erwartung nach 1.3 g: Der Überstand von +1,4 m halbiert sich.

### Reihenfolge und Abbruch

```
T0-1 → T0-2 → T0-3 → T1-1 → T1-2 → T2-1 → (T2-2) → T3-1 → T3-2 → T3-3 → T4 (R1–R4) → T5-1 → T5-2 → (T6)
```

- Nach **T2-1**: Läuft das Wasser durch (Front im Kies, Q ≥ 0,5 m³/s), sind Stufe 3 und 4 nur noch für `remove` 50 nötig.
- Nach **T3-1/T3-2**: Ist die Kante weg, `remove` 50 wieder als Netz.
- Nach **T4**: Kriterium 5.1 festlegen.
  - Fällt R2/R4 durch → Plan B für die Bergrinne.
  - Laufen alle → Bergrinne bleibt SWR mit den Werten aus 4.1.

**Bitte zurückmelden:** T0-1 (3 Zahlen), T0-2 (Extrempunkte mit s, z bei s 62, Richtung der Kante, Arm), T0-3 (Zonenfelder,
Texturgröße, Header-Treffer), V(t)-Tabellen aus T1/T2, Bilder Front und Kante, Ergebnisse R1–R4.

---

## 7. Export: Diagnose `rand_steil` (Regeln v9)

Ob die Abhilfen (Vorlauf, Rahmen, Speisepunkt, Grenzen 15/30 %) wirken, ist noch nicht getestet. Deshalb gibt es **keine neue
Bau-Regel**, nur eine **Diagnose je SWR-Bereich**. Spline, SWR-Werte, `sim_vorgaben` und Fingerabdrücke bleiben gleich.

**Neu je `swr_bereiche[]` → `rand_steil`:**

| Feld | Inhalt |
|---|---|
| `rechteck_ue_cm` | Box der Splinepunkte **ohne** Breite (UE-Rechteck nach Befund 8) |
| `anfang` | Seite und Abstand des ersten Punkts zum UE-Rechteck, halbe Breite, `zu_nah` (< 10 m); `art` quelle bzw. teilstueck |
| `kontakte` | Punktfolgen, deren halbe Breite über das UE-Rechteck ragt: Seite, s-Bereich, Länge, größter Überstand, z, `am_ende` (beginnt in den ersten bzw. endet in den letzten 10 m des Bereichs) |
| `rahmen_cm`, `rahmen_m` | Soll-Rechteck: jedes Bett ± (halbe Breite + 5 m) |
| `hoehenspanne_m`, `z_m` | größte − kleinste Spline-Höhe im Bereich |
| `gefaelle_fenster_max` (+ s) | größtes Spiegelgefälle im 20-m-Fenster |
| `steilstrecken` | Strecken ≥ 50 m mit Gefälle ≥ 30 % (`kaskade`) bzw. 15–30 % (`pruefen`): s, Länge, dz, mittleres Gefälle |
| `eignung` | `swr` / `pruefen` / `kaskade_vorschlag` |

Grenzen in `fluss_sim_regeln.json` → `swr.rand_steil`: `rand_zugabe_m` 5, `quelle_abstand_min_m` 10, `fenster_m` 20,
`gefaelle_pruefen` 0,15, `gefaelle_kaskade` 0,30, `strecke_min_m` 50. Status: „Vorschlag 16g, nur Diagnose“.

**Hinweis zum Rechteck:**
- Der Export rechnet die Zelle weiter mit der Box **± halbe Breite** (`rechteck_m`, wie bisher).
- Befund 8 sagt: UE nimmt die Box **ohne** Breite. Dann ist die echte Zelle etwas kleiner als im Export. Ich ändere das erst nach
  eurer Bestätigung (Rückfrage 3), weil sich sonst Auflösungen und `sim_vorgaben` vieler SWR ändern.

**Lauf (2-m-Daten, Scratchpad):**
Gefälle-Planer `--alle` (123 Läufe, 0 FEHLER), Sehens-Planer für alle 15 Biome, `bachbett_roh`, dann der Export
zweimal. Ergebnis: 187 Gewässer, 199 SWR-Bereiche, 762 Fälle, wie in v8.

| Größe (`zusammenfassung.json` → `swr_rand_steil`) | Wert |
|---|---|
| Quellen < 10 m vom UE-Rechteck | **187 von 187** (alle < 1 m, Median 0,00 m) |
| SWR-Bereiche mit Bett über dem Rechteckrand **mitten im Lauf** | **76** (98 Stellen; dazu die Stellen an Quelle und Mündung, zusammen 826) |
| Höhenspanne je SWR-Bereich | Median 11,6 m, größte 155,7 m; 20 über 50 m, 3 über 100 m |
| Eignung | `swr` 129, `pruefen` 52, `kaskade_vorschlag` **18** |
| Länge der Kaskaden-Strecken / Prüf-Strecken | 1 454 m / 7 229 m |
| steilste (Kaskaden-Länge, größtes 20-m-Gefälle, Höhenspanne) | `F_ERLENBACH_T00` 164 m (52 %, 68 m); `B_R_P4_M2_04` 152 m (94 %, 156 m); `SW_gletscher_06_gletschertoepfe_klammbach_oben` 138 m (164 %, 94 m); `B_K8_ELFENFALL_01` 118 m (117 %, 118 m); `B_R2_R_P4_M2_01` 92 m (81 %, 109 m) |

- **Erlenbach in den 2-m-Daten** (`F_ERLENBACH_T00`, beginnt bei 104 m, also ohne eure neue Bergrinne):
  - Kaskaden-Strecke s 23–187 m mit 33 % im Mittel.
  - Die Quelle liegt am Südrand.
  - **Am Westrand ragt das Bett von s 160 bis 323 m bis zu 16 m über das UE-Rechteck.**
  - Eure lokale 1-m-Fassung ist länger und beginnt höher. Ob es dort eine gleiche Stelle bei s ≈ 200–231 m gibt, zeigt T0-2.
- **Folgerung:** Die Quelle am Rand ist kein Einzelfall von C2. Sie betrifft **jede** SWR, weil die Quelle fast immer der
  höchste und damit äußerste Punkt ist. Die Abhilfe aus T2-1 (Vorlauf) gilt deshalb für alle Gewässer, sobald sie getestet ist.
- **Unverändert:** Ohne `rand_steil` ist `F_ERLENBACH/fluss_sim.json` gleich v8 (geprüft). `back_liste_auszug.json` mit
  Fingerabdrücken und `sim_vorgaben` ist byte-gleich, `vorschlaege.json` ebenso.

**Prüfer** (`fluss_sim_pruefen.py`):
- rechnet `rand_steil` je SWR-Bereich neu; eine Abweichung ist ein FEHLER;
- prüft Steilstrecken (Länge, Lage im Simulationsbereich) und den Rahmen (schließt das UE-Rechteck ein);
- meldet zwei HINWEIS-Zeilen: Rand und Steil.

- **Prüfer:** 0 FEHLER, 0 WARNUNG, 72 HINWEIS (70 wie v8 + Rand + Steil). Zwei Exportläufe sind byte-gleich (183 Dateien).
- **Gegenproben** (Exit 1):

  | Gegenprobe | Ergebnis |
  |---|---|
  | `rand_steil.eignung` von Hand auf `swr` gesetzt (`F_ERLENBACH_T00`) | 1 FEHLER („weicht von der Neurechnung ab: eignung“) |
  | `rand_steil` entfernt | 1 FEHLER („rand_steil fehlt“) |

- **Beispiele neu** unter `antworten/fluss_sim/`: `F_ERLENBACH`, Karsee, Elfentreppe, `zusammenfassung.json`. README um
  „Ergänzungen 16g“ ergänzt.

---

## Quellen

Alle Web-Seiten waren aus der Cloud nicht lesbar (DNS bzw. Proxy 403). Die Inhalte stammen aus Suchmaschinen-Auszügen.

**Epic (Doku, API):**
- [AWaterZone (API)](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/AWaterZone): `ZoneExtent`,
  `WaterHeightExtents`, `GroundZMin`, `CaptureZOffset`, `bHalfPrecisionTexture` [Doku]
- [unreal.WaterZone (Python)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterZone):
  `capture_z_offset` [Doku]
- [FWaterInfoTextureRenderingParams](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/FSceneView/FWaterInfoTextureRenderingParams):
  `WaterZoneExtents`, `WaterHeightExtents`, `GroundZMin`, `CaptureZ` [Doku]
- [FWaterZoneActorDefaults](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterEditor/FWaterZoneActorDefaults):
  `RenderTargetResolution` [Doku]
- [Water Meshing System and Surface Rendering](https://dev.epicgames.com/documentation/unreal-engine/water-meshing-system-and-surface-rendering-in-unreal-engine):
  Local Tessellation, `LocalTessellationExtent`, gleitendes Fenster der WaterInfoTexture [Doku]
- [UShallowWaterRiverComponent (API)](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent):
  `bMatchSpline`, `MatchSplineHeightAmount`, `RemoveOutsideSplineAmount`, `bDisableCPUThrottling` [Doku]
- [unreal.ShallowWaterRiverComponent (Python)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent),
  [unreal.ShallowWaterRiver](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiver) [Doku]
- [UWaterBodyComponent::FindInputKeyClosestToWorldLocation](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterBodyComponent/FindInputKeyClosestToWorldLocati-),
  [TryQueryWaterInfoClosestToWorldLocation](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterBodyComponent/TryQueryWaterInfoClosestToWorldL-),
  [QueryWaterInfoClosestToWorldLocation (4.27)](https://docs.unrealengine.com/4.27/en-US/API/Plugins/Water/AWaterBody/QueryWaterInfoClosestToWorldLoca-/index.html) [Doku]
- [Niagara Fluids Reference](https://dev.epicgames.com/documentation/unreal-engine/niagara-fluids-reference-in-unreal-engine),
  [Fluid Simulation Overview](https://dev.epicgames.com/documentation/unreal-engine/fluid-simulation-in-unreal-engine---overview):
  Shallow-Water-Vorlage, 2D-Gitter [Doku]
- Devon Penney, „Baked River Simulations – Parameter Reference“ und „Overview and Quick Start“
  ([Forum-Faden](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112)): Inhalt nur
  über Ferats Zusammenfassung [Epic lokal]

**Epic-Forum (Auszüge):**
- [ShallowWaterRiver simulation does not initialize in UE 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772)
- [Shallow water plugin not working in 5.8](https://forums.unrealengine.com/t/shallow-water-plugin-not-working-in-5-8/2763339)
- [ShallowWaterRiver and Landscape („water wall“)](https://forums.unrealengine.com/t/shallowwaterriver-and-landscape/2818892)
- [ShallowWaterRiver (japanisch, zwei SWR an einer Verbindung)](https://forums.unrealengine.com/t/shallowwaterriver/2738013)
- [UE 5.7 Water Plugin – Baking fails after adding an additional WaterRiver](https://forums.unrealengine.com/t/ue-5-7-water-plugin-baking-fails-after-adding-an-additional-waterriver/2732713/2)
- [ShallowWaterRiver Collision](https://forums.unrealengine.com/t/shallowwaterriver-collision/2734514)
- [waterzone (japanisch, Local Tessellation in großen Welten)](https://forums.unrealengine.com/t/waterzone/2719663)
- [Unreal Fest Orlando 2025: „Chasing Waterfalls“ (Matt Oztalay)](https://forums.unrealengine.com/t/2539568): einziger
  Wasser-Vortrag im Suchergebnis, ohne SWR-Bezug
- [UE-175251 (Water Zone Extent bei 8K-Landschaft)](https://issues.unrealengine.com/issue/UE-175251) [Bug]

**Fachliteratur (Auszüge):**
- Flachwassergleichungen auf steilem Gelände, Gültigkeit „< 10 %“, Abweichungen über 20°:
  [UCLouvain, research.dial](https://research.dial.uclouvain.be/handle/2078.5/248990);
  J. D. Fenton, [The long wave equations for arbitrary slopes](https://www.johndfenton.com/Papers/05-The-long-wave-equations-for-arbitrary-slopes.pdf)
- Montgomery & Buffington (1997), *Channel-reach morphology in mountain drainage basins*
  ([USDA-PDF](https://fs.usda.gov/rm/boise/publications/watershed/rmrs_1997_montomeryr001.pdf)); Gefällebereiche nach
  Sekundärquelle [Fach]
- Lehrbuchwissen (nicht neu recherchiert): Manning-Strickler, Grenztiefe h_c = (q²/g)^(1/3), Überfall q = 1,705 H^1,5,
  CFL-Bedingung, Half-Float-Raster (10 Bit Mantisse)
- Fluid Flux 2.0 („better simulation quality on slopes“): [80.lv](https://80.lv/articles/fluid-flux-a-cool-water-simulation-system-for-unreal-engine/) [Blog]

**Projekt:**
- `auftraege/16g-…`, `auftraege/16f-rueckfrage-epic-parameter-lokal.md`
- `antworten/16a-…` (T1 36 %, Bodenerfassung, 65 504), `16b-…` (Höhen ≤ 332 m), `16c-…` (Rechteck um die Quell-Flüsse,
  zwei SWR), `16e-…` (`MaxFlowVelocity` = Kodierung), `16f-…` (Parameter, Friction × 2), `13g-…`/A15 (Kaskadennetz)
- `skripte/fluss_sim/` (Regeln v9, Export, Prüfer, README)

---

## Rückfragen

1. **Speisepunkt für Plan B:**
   - Ist ein kurzer Hilfs-River (`WBR_<fluss>_SPEISUNG`, 6–10 m, unsichtbar, nur zweite Quelle der SWR) mit „Fluss bleibt ein
     Fluss“ vereinbar? Der Erlenbach selbst bliebe ungeteilt.
   - Falls nein, bleibt nur S2 (SWR speist oben, Kaskadennetz überdeckt die Rinne).
2. **Der Arm:** Wo liegen Anfang und Ende des zweiten Quell-Flusses (s am Erlenbach, Höhe)? Wozu dient er (Rechteck vergrößern,
   Mulde füllen)? Ein Lauf ohne ihn (T1-1) trennt Rang 4 ab.
3. **UE-Rechteck ohne Breite (Befund 8):**
   - Bitte an einer zweiten SWR bestätigen (`swr_info` gegen `rand_steil.rechteck_ue_cm` aus dem Export).
   - Dann rechne ich `rechteck_m`, Auflösung und Zelle im Export ohne Breite. Bei wenigen SWR wird die Auflösung kleiner.
4. **Friction/Dissipation:** Habt ihr in der Niagara-Kopie schon × 2 / × 1,5 (16f) gesetzt? Dann gilt T5-2 als „zurück auf
   Standard“.
5. **Zeit:** Läuft die Spielzeit in den 90 s mit `sim_speed` 10 zehnfach? Dann ist die gemessene Speisung ≈ 0,35 m³/s, sonst
   ≈ 3,5 m³/s (2.2).
6. **Grenzen 15 % / 30 % / 50 m** in `rand_steil`: nach dem Rampentest (T4) festlegen. Bis dahin ist es nur eine Liste.
