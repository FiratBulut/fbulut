# Antwort 16h Nachtrag 5b – Wasseroberfläche G0–G4 (13.10.2026)

Bezug: `auftraege/16h-nachtrag5b-wasseroberflaeche.md`, Bild `bilder/swr_p2/wasser_oberflaeche_g0_g4.jpg`, Nachtrag 5 §2.2 (D, W1–W4),
Nachtrag 2 (Streuung). Ergänzung von Ferat: Das Wassermaterial aus „Rural Australia“ wird geprüft. Deshalb gelten die Werte für
`MI_EL_SWR_Klar` hier nur als **Zwischenstand**. Für das alte Material gibt es keine weitere lange Testreihe.

## Kurzfazit

1. **Zwischenstand setzen:**
   - `Sim Velocity Normal Strength` **5**. Der Wirbel wird ruhiger, das ist ohne Nachteil (G2/G4).
   - `Water Roughness` **0,10**. Das ist ein Kompromiss zwischen 0,04 und 0,12 nach Ferats Leitlinie „nicht stumpf“.
   - Specular bleibt bei 0,225 / 0,225.
   - Die Streuung bleibt unverändert.
2. **Die Wirkung der Rauheit ist nicht sauber belegt.**
   - Ich habe das JPG auf Augenhöhe ausgemessen (§1). G1 ist in beiden Augenhöhe-Bildern die Aufnahme mit dem **hellsten Himmel**. Kühler wirkt dort vor allem G1.
   - G4 hat ebenfalls Rauheit 0,12, aber einen dunkleren Himmel. Bei t500 ist G4 so warm wie G0.
   - Den kühleren Eindruck von G1 erklärt also möglicherweise der Himmel und nicht die Rauheit. Deshalb setze ich nicht 0,12 fest.
   - Unsere Erwartung aus N5 (0,02–0,03, also schärfer) ist damit **ebenfalls nicht gestützt**. Ich ziehe sie bis zur Messung zurück.
3. **Ferats Deutung zu Specular stimmt zur Hälfte.**
   - Dass `Water Specular` kaum wirkt, passt zur Physik und ist kein WCBS-Sonderfall: Bei flachem Blick bestimmt Fresnel die Spiegelung, der Specular-Wert kaum.
   - Brechung und Streuung sind als Quelle des Golds dagegen unwahrscheinlich. Plausibler ist die **Spiegelung der sonnigen, goldgelben Talhänge**, und das ist eine Spiegelung (§2).
4. **Reihenfolge:**
   1. Himmel und Belichtung einfrieren.
   2. Eine faire Aufnahme machen: G0, Zwischenstand Z und später das fremde Material mit denselben Kameras.
   3. Darauf W1 testen (ELD-Wirbel aus, eine Aufnahme).
   4. D nur, wenn das Gold bleibt.

   Die Messung in Schritt 2 dient zugleich als Vergleichsbasis für Rural Australia.
5. **Die beiden genannten Hebel:**
   - `Fluidsim Normal Strength` ist nach unserer Einordnung aus 16a/16e die Interaktion um die Spielfigur und deshalb **kein Hebel** für das Bachbild.
   - `Water Fresnel Roughness` (im MI-Dump 0,1) ist ein möglicher Hebel für genau den flachen Blick. Seine Wirkung ist nicht belegt. Er gehört nur in die faire Aufnahme, wenn Z nicht reicht.

## 1. Auswertung G0–G4 (Messung aus dem JPG)

Grundlagen der Messung:
- Ausgewertet ist nur das JPG, also tonemapped und komprimiert. Die Zahlen sind relativ und nur Anhaltspunkte.
- Linearisiert mit sRGB.
- Bereiche:
  - „Wasser nah“: unteres Bildmittel, 70–97 % der Höhe und 25–75 % der Breite.
  - „Himmel“: 3–15 % der Höhe, Mitte.
- Messgrößen:
  - R/B: Rot zu Blau, je höher, desto goldener.
  - K: Leuchtdichte-Streuung durch Mittelwert, ein Maß für die Struktur.

| Kamera | | G0 | G1 (R 0,12) | G2 (N 5) | G3 (Spec 0,12) | G4 (R 0,12 + N 5) |
|---|---|---|---|---|---|---|
| t430 Auge | Wasser nah R/B | 2,37 | **1,60** | 2,42 | 2,33 | 2,20 |
| | Himmel Y | 0,46 | **0,68** | 0,45 | 0,42 | 0,53 |
| | Wasser nah K | 0,41 | 0,35 | 0,41 | 0,44 | 0,41 |
| t500 Auge | Wasser nah R/B | 2,74 | **2,25** | 2,64 | 2,94 | 2,76 |
| | Himmel Y | 0,33 | **0,45** | 0,35 | 0,35 | 0,28 |
| t550 / t500 schräg | Wasser nah R/B | 1,73–2,57 | ≈ G0 | ≈ G0 | ≈ G0 | schräg 3,15* |

\* Bei t500 schräg ist das ganze Bild bei G4 wärmer, auch das Gras (R/B 2,9 → 3,6). Das spricht für schwankendes Licht oder schwankende Belichtung und nicht für das Wasser.

Was sich daraus ablesen lässt:
- In beiden Augenhöhe-Kameras sinkt R/B dort, wo der Himmel heller ist. Am stärksten gilt das für G1. G4 hat dieselbe Rauheit und verliert bei t500 nichts.
- Ferats Eindruck „G4 wie G1“ zeigt sich in den Zahlen **nicht**. Das ist kein Fehler beim Hinsehen: Der Himmel überdeckt den Effekt.
- Im Nahbereich hat G1 bei t430 weniger Struktur (K 0,35 statt 0,41). Das ist ein erstes Zeichen, dass 0,12 schon leicht stumpf macht. Belastbar ist dieses Zeichen nicht.
- Normalstärke 5 (G2/G4) ändert die Farbe nicht und beruhigt nur den Wirbel. Deshalb setze ich sie ohne Vorbehalt.

## 2. Woher das Gold vermutlich kommt (Deutung, nicht gemessen)

- **Fresnel.** Bei Augenhöhe 1,7 m liegt Wasser in 5–10 m Entfernung unter 71–80° zur Flächennormalen.
  - Dort reflektiert Wasser etwa 13–35 %. Senkrecht sind es etwa 2 %.
  - Der Specular-Eingang setzt in UE nur den Wert senkrecht zur Fläche (F0). Zum flachen Winkel hin geht Fresnel ohnehin gegen 1.
  - Daher wirkt G3 kaum. Das deckt sich mit Ferats Beobachtung.
- **Was gespiegelt wird.** Gegenüber liegen sonnenbeschienene, gelbgrüne Hänge, und genau die spiegelt das Wasser. Das ergibt ein „goldenes“ Spiegelbild.
- **Was Rauheit dabei tut.** Rauheit verwischt das Spiegelbild und mischt mehr Himmel hinein. In die Richtung „kühler“ kann sie also wirken, aber nur über die Spiegelung.
- **Hinweis aus dem Bild.** Bei t550 und schräg, also bei steilerem Blick mit wenig Fresnel, sehen alle Varianten gleich aus. Das spricht ebenfalls für die Spiegelung als Quelle. Belegt ist das erst mit D.
- **Streuung (0,5; 1; 1) × 0,02.** Nach unserer Korrektur in N2 ist sie praktisch unsichtbar: Schon A 0,1 auf 0,5 m wirkt nicht milchig. Im Graph geht sie zudem nur schwach ein (Multiply → Add → Divide → Water_Underside). Der Farbton ist eher bläulich.
  - Die Streuung ist **nicht** die Quelle des Golds. Nicht ändern.

## 3. Einordnung in die N5-Testreihe

| Schritt | Zweck | Aufwand |
|---|---|---|
| 0 Himmel und Belichtung einfrieren (§5) | Ohne diesen Schritt ist kein A/B auswertbar | einmalig |
| 1 Faire Aufnahme: G0, **Z** (R 0,10 / N 5), G4 | klärt, ob die Rauheit wirkt; Basis für das fremde Material | 3 × 4 Kameras |
| 2 W1 auf Z: `ELD_Wirbel_Normal` 0, `ELD_Wirbel_Staerke` 0, `ELD_Schaum_Normal` 0 | ist das Wirbelmuster unser eigenes? | 1 Aufnahme |
| 3 D (Quelle der Spiegelung) | nur wenn Z das Gold nicht nimmt | 1–2 Aufnahmen bei t500 Auge |
| – W2–W4 | **ruhen**, bis über das Material entschieden ist | – |

Für die Rauheit gilt nach Schritt 1 eine einfache Regel:
- Ist Z gegenüber G0 bei gleichem Himmel kühler und hat dabei K ≥ 90 % von G0, dann bleibt 0,10.
- Kühlt erst G4, dann 0,12. Dafür muss K ebenfalls ≥ 90 % von G0 bleiben, sonst ist es stumpf.
- Kühlt keine von beiden Varianten, dann zurück auf 0,04. Die Rauheit ist dann nicht der Hebel, und D ist dran.

`Water Fresnel Roughness` ist nur dann der nächste Kandidat (z. B. 0,1 → 0,15). Wie der Parameter im Graph wirkt, ist nicht belegt (er sitzt in einer Epic-Funktion).

## 4. Messung der Szenenfarbe auf Augenhöhe

- **Wo:** die Kameras C2_t430_auge, C2_t500_auge, C2_t550_auge und als Kontrolle t500_schraeg.
  - Am besten als HDR/EXR-Aufnahme oder mit dem Pixel Inspector. Ein JPG reicht nur zur Not.
- **Klassen je Bild:**
  1. Wasser nah, 2–4 m: Blick etwa 50–67° zur Normalen, der Grund soll sichtbar sein.
  2. Wasser fern, 8–15 m: 78–84°, dort dominiert die Spiegelung.
  3. Referenz Ufer: trockener Kies oder Gras im selben Bild.
  4. Referenz Himmel.
- **Messgrößen:**
  - Mittelwert des linearen RGB.
  - R/B.
  - K = Leuchtdichte-Streuung durch Mittelwert.
- **Vergleichskriterium, kein Absolutziel:**
  - R/B(Wasser) wird durch R/B(Ufer) im selben Bild geteilt. Das gleicht Licht- und Belichtungsschwankungen aus.
  - Erfolg heißt: Bei Wasser fern sinkt dieser Wert gegenüber G0, und bei Wasser nah bleibt K ≥ 90 % von G0 („nicht stumpf“).
  - Liegt Y(Himmel) zwischen zwei Aufnahmen mehr als 5 % auseinander, ist der Vergleich ungültig.
- Das Messskript kann ich auf Wunsch liefern. Es misst Bereiche in festen Bildanteilen, wie in §1.

## 5. Himmel und Licht festhalten (UE-übliche Wege, Namen im Projekt prüfen)

- Die **Tageszeit fest setzen**, also die Sonne nicht animieren. Falls ein Tageszeit- oder Wettersystem läuft, dieses für die Tests anhalten.
- **Wolken einfrieren:** Die Wind- bzw. Bewegungsgeschwindigkeit des Wolkenmaterials (Volumetric Clouds oder Sky-Material) auf 0 setzen. Wenn das nicht geht, alle Varianten im selben Frame vergleichen, indem man die MI-Werte per Sequencer bzw. Schalter wechselt, ohne dass Zeit vergeht.
- **Belichtung fest:** im Post Process Volume `Metering Mode` auf Manual setzen oder Min/Max EV100 gleich. Sonst gleicht die Auto-Belichtung jede Variante an.
- Nach jedem Wechsel einige Sekunden warten, damit Lumen nachgeführt ist. Erst dann aufnehmen.

## 6. Prüfliste für ein fremdes Wassermaterial (z. B. Rural Australia)

Über das Material aus Rural Australia behaupte ich hier **nichts**. Ich kenne es nicht und habe nichts dazu nachgelesen. Die Liste sagt nur, was Ferat oder der lokale Claude im Projekt nachsehen sollten.

1. **Art des Materials:**
   - Shading Model `SingleLayerWater` oder Translucent bzw. Default Lit?
   - Liegt es als Water-Material auf einem Water Body (River/Lake) oder auf einem eigenen Mesh bzw. einer Ebene?
   - Nur ein SLW-Material im Water-Body-Slot kann mit SWR, den gebackenen Daten (WCBS) und der Water Info Texture zusammenarbeiten. Ein Mesh- oder Translucent-Material folgt der SWR-Strömung nicht.
2. **Eingänge:**
   - Ruft es Epic-Water-Funktionen auf, also `WaterAttributes`, `WaterRiverFlowmaps`, `SampleFluidSimulation`? Das lässt sich im Graph-Dump wie bei unserem Master prüfen.
   - Woher kommen Fließrichtung und Geschwindigkeit: Flowmap-Textur, Spline-Flow, Water Info oder Sim?
   - Woher kommt die Tiefe: SceneDepth oder Water Info?
   - Ohne Geschwindigkeit aus der SWR-Sim gibt es keine Kaskade mit Strömung.
3. **Was beim Umhängen verloren geht:**
   - Absorption als Sichtweite in cm. Das ist unsere 1/x-Konvention, die Einheit des fremden Materials muss man nachrechnen.
   - `ELD_Wirbel_*` und `ELD_Schaum_Normal`.
   - Schaum8 und BeachFoam samt unseren Schaumwerten.
   - Unser Water_Underside.
   - **Bachgewicht und V18-Tönung bleiben**, denn sie sitzen im Landschaftsmaterial. Ihre Abstimmung (nasser, dunkler Grund) ist aber auf unsere Sichtweite ausgelegt und muss nachgeprüft werden.
4. **Technik:**
   - Engine-Version des Projekts gegen 5.8. Per Migrate übernehmen, dabei Abhängigkeiten und Texturen auf Inventar und SRV-Zahl prüfen.
   - Nutzungsbedingungen des Downloads prüfen.
5. **Kosten:** Shader-Statistik (Instruktionen, Textur-Samples) und GPU-Zeit des Wasserdurchgangs (`stat gpu` / ProfileGPU) an t500 Auge, jeweils gegen G0.
6. **Fairer Vergleich:**
   - Dieselben vier Kameras, eingefrorener Himmel, feste Belichtung.
   - Zuerst Sichtweite bzw. Farbe auf unser Ziel bringen, also gleiche Klarheit über Grund. Sonst vergleicht man Wasserfarbe statt Oberfläche.
   - Danach die Messung aus §4: G0, Z und das fremde Material im selben Lauf.

## Rückfragen

1. Gibt es ein Tageszeit- oder Wolkensystem in der Szene, oder ist es nur Sky Atmosphere plus Volumetric Clouds? Davon hängt ab, wie man es einfriert.
2. Soll ich das Messskript für §4 liefern? Es braucht Bilder bzw. EXR der vier Kameras und die Lage der Bereiche.
