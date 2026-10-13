# Antwort zu 16h Nachtrag 4 – V18, Bachgrund ohne neue Texturen, Mündung

Stand 13.10.2026. Grundlage: `auftraege/16h-nachtrag4-v18-muendung.md` (3338f15), Bilder `bilder/swr_p2/v18_vorher_nachher.jpg` und
`muendung_vorher_nachher.jpg`, unsere Antworten [16h-Nachtrag 2](16h-nachtrag2-tl-t0-kasten.md) (Tönung, Texturen, Lagen unter dem
Spiegel) und [16h-Nachtrag 3](16h-nachtrag3-teile-a-c1-t3-schaum.md) (Kopf-Kürzung v12).

**Kennzeichnung:** [Befund] Ferats Messung bzw. Bild, [Projekt] eigene Rechnung, [Forum] Epic-Forum als Suchauszug,
[Ableitung] geschlossen, [Gestaltung] Entscheidung, [unsicher] im Test klären.

---

## Kurzfazit

1. **V18 wirkt.** Das Bett ist grauer, der Uferstreifen nass und dunkel, die Tal-Tönung am Wasser weg. Dazu kosten die
   23 Knoten nur 27 Anweisungen und keinen Sampler.
   - Der Rest „Kies hell-beige im warmen Licht“ hat zwei Hebel: Die Kies-Ersetzung läuft im Bach noch mit **0,25** statt 0,
     und die Kies-Lage selbst ist zu hell und warm.
   - **Sofort (0 Kosten):** `Ufer_Staerke` Bach **0**.
   - Ziel: Grundfarbe (BaseColor-Puffer) unter Wasser Y ≤ 0,15, im nassen Band ≤ 0,25.
   - Das Licht bleibt.
2. **V19 ohne neue Texturen: Der Texturtausch ist die SRV-Grenze jetzt nicht wert.**
   - Stattdessen Tönung je Lage unter Wasser: nach der Lagenmischung ein Faktor aus den Lagengewichten (`LandscapeLayerSample`
     liest die schon gebundenen Gewichtskarten).
     - Kies × (0,62; 0,65; 0,68), Geroell × (0,72; 0,75; 0,78), Sand × (0,60; 0,62; 0,64), Fels/Felsplatte × (0,85; 0,88; 0,90);
     - dazu Entsättigung Kies 0,5.
   - Kosten: etwa 25–30 Anweisungen, **0 Sampler, 0 SRV** [Ableitung, im Material-Stat prüfen].
   - Neue Texturen nur später und nur als **Tausch statt Zusatz** (0 SRV, wirkt aber weltweit) oder über Texture-Arrays.
3. **Reihenfolge:**
   1. `Ufer_Staerke` 0, dann BaseColor messen.
   2. **Lagen unter dem Spiegel über `s38 lagen`**: kein Shader-Aufwand. Es kann aber Gewichtskarten und Lagen-Texturen je
      Teil kosten, deshalb danach den SRV-Prüflauf.
   3. V19-Tönung je Lage.
   4. Ein Texturtausch nur, wenn es dann noch beige ist.
4. **Mündung:** Die Reparatur ist richtig.
   - Die schmale Kante von oben ist die harte Anfangskante des C3-Water-Body neben dem p2-Wasser.
   - Abhilfe: C3 3–5 m früher **unter** dem p2-Wasser beginnen lassen, gleiche Höhe (36,80 m), Startbreite = p2-Breite; p2 mit
     höherer `Overlap Material Priority`.
   - **Export nachgezogen:** `muendung_anschluss.lokaler_kopf` übernimmt Ferats Kopfpunkte (s 24/31/38 m, 36,80/36,72/36,64 m,
     Breiten 7/11/14 m, danach 17/22/26/25 m); p2-Spiegel 36,80 m.
   - `F_ERLENBACH` beginnt bei s 24 m auf 36,80 m, 623,7 → **599,7 m**. Prüfer 0 FEHLER, zwei Läufe byte-gleich. Neu backen: `F_ERLENBACH` (`576f7efc4372…`), `B_R2_K10_TUNDRA_01` und `_02` (nur Objektteil).
   - Unsere 2-m-Weltdaten müssen den 54-m³-Graben nicht kennen. Lokal liest der Export die 1-m-Höhen mit dem Graben.
5. **SRV-Prüflauf:**
   - Das Limit von 64 gilt je Landschaftsteil und zählt Lagen-Texturen und Gewichtskarten [Forum].
   - Wechselt ein Teil auf V18s, muss V18s an der Grenze **dieselbe Farbe** liefern: Nähte an den Teilgrenzen prüfen, vor allem
     im Bach (Bachgewicht > 0).
   - Den Lauf **nach** den neuen Lagen unter dem Spiegel wiederholen.

---

## 1. V18 und der Rest „hell-beige“

### 1.1 Würdigung

- [Befund Bild] Bei t430 und t500 schräg sind Bett und Uferstreifen grauer und dunkler. Bei t500 auf Augenhöhe bleibt der Grund hell.
  Die hellen Flecken sind Kiesel der Kies-Textur unter Wasser.
- Kosten 420 → 447 Anweisungen, Texturen 68 → 69 (Bachgewicht) [Befund]. Das ist günstig; die Umsetzung entspricht dem Plan aus
  Nachtrag 2.

### 1.2 Wo liegt der Hebel?

| Kandidat | Wirkung heute | Hebel | Wert |
|---|---|---|---|
| Kies-Ersetzung im Bach | `Ufer_Staerke` Bach **0,25**: ein Viertel des Grunds bleibt helle Ersatz-Textur | **ja, sofort** | **0** (Nachtrag-1-Antwort: im Bach nicht übermalen; TL nutzte noch 0,25) |
| Kies-Lage (Textur `T_ground_big_pebbles_01`) | hell und warm, auch nass × 0,40 | **ja** | Tönung unter Wasser (2.2): Kies × (0,62; 0,65; 0,68), Entsättigung 0,5 |
| Tönung | am Wasser neutral (V18) | erledigt | – |
| Nässe | `Nass_Abdunkeln` 0,40 | ausgereizt | nicht weiter senken, sonst wird der Grund schwarz |
| Licht | warmes Nachmittagslicht | **nein** | Das Licht gehört zum Bild; die Hänge sollen golden bleiben |
| Wasser | färbt nicht (T0) | nein | – |

**Messung statt Schätzung** (2 min): Buffer Visualization → *Base Color*, Pipette auf den Grund bei t500 auf Augenhöhe.
- Ziel unter Wasser: Y (0,21 R + 0,72 G + 0,07 B) ≤ **0,15**.
- Nasses Band: ≤ 0,25.
- Trockener Kies am Hang: 0,30–0,40.

Nasser Bachkies hat in der Natur etwa die Hälfte der trockenen Albedo [Fach, Jensen et al. 1999, wie Nachtrag 1].

## 2. V19 und SRV

### 2.1 SRV-Fakten

| Aussage | Beleg |
|---|---|
| Der Fehler „Shader is using too many SRVs (only 64 supported)“ tritt **je Landschaftsteil** auf, wenn dieser mehr als 64 Texturen nutzt. Die Ebenen-Ansicht „Layer Usage“ zeigt die Ursache | [Forum, UE 4.26, Suchauszug](https://forums.unrealengine.com/t/ue4-26-shader-is-using-too-many-srvs-only-64-supported/154906) |
| `MAX_SRVS 64` in `D3D12RHI.h`; ein Hochsetzen scheitert an einer 64-Bit-Maske (`static_assert`) | [Forum, Suchauszug](https://forums.unrealengine.com/t/ue4-26-shader-is-using-too-many-srvs-only-64-supported/154906/14). Für 5.8 nicht geprüft [unsicher] |
| `Shared: Wrap` als Sampler-Quelle löst die Grenze von **16 Samplern**, nicht die SRV-Grenze | [Forum](https://forums.unrealengine.com/t/shader-is-using-too-many-samplers-23-only-16-supported/478724), [Forum](https://forums.unrealengine.com/t/ue4-26-shader-is-using-too-many-srvs-only-64-supported/154906) |
| Gewichtskarten zählen mit: je 4 Lagen eines Teils eine RGBA-Karte | [Ableitung]; deckt sich mit „Layer Usage“ |
| Texture-Arrays: eine `Texture2DArray` ist **ein** SRV für viele Schichten | [Ableitung]; ein Umbau aller Lagen, kein Schritt für jetzt |
| Bindless in UE 5.8 | nicht belegt gefunden [unsicher]; nicht darauf bauen |

### 2.2 Entscheidung: V19 ohne zusätzliche Texturen

**Warum:**
- V18 hat schon einen Teil auf 65 gebracht. `T_MossyRockyGround_01` (BC, N, AoRDp) und `T_IcelandicQuarryRock_01` (BC, AoRDp)
  wären bis zu **+5 SRVs** je Teil, in dem Geröll oder Fels vorkommt. Gerade die Bachteile haben viele Lagen.
- Der Farbfehler ist **Helligkeit und Wärme**, nicht das Muster. Beides lässt sich nach der Mischung ohne Textur korrigieren.

**Knotenskizze** (Gruppe „V19 Lagen unter Wasser“, nach der Lagenmischung, vor der Nässe):
1. `W = W_unter + 0,5 × W_ufer` (aus V18), × `Bachgewicht`, gesättigt (Saturate) → `G`.
2. Je Lage *L* in {Kies, Geroell, Sand, Fels, Felsplatte}: `LandscapeLayerSample(L)` → `w_L` (liest die vorhandene
   Gewichtskarte, kein neuer Sampler).
3. `T = 1 + Σ w_L × (Tint_L − 1)` (Vektoren `V19_Tint_<L>`), dazu `E = Σ w_L × Entsaettigung_L`.
4. `Farbe = Lerp(Farbe; Farbe × T; G)`, danach `Lerp(Farbe; Luminanz(Farbe); G × E)`.

| Lage | `V19_Tint` | Entsättigung | Begründung |
|---|---|---|---|
| Kies | (0,62; 0,65; 0,68) | 0,5 | heller und orangeste Textur |
| Geroell | (0,72; 0,75; 0,78) | 0,35 | orange, etwas dunkler als Kies |
| Sand | (0,60; 0,62; 0,64) | 0,4 | hell |
| Fels, Felsplatte | (0,85; 0,88; 0,90) | 0,2 | Farbe vor Ort prüfen |
| Schlamm, Algen, Moos, Erde | 1 | 0 | schon dunkel |

**Kosten** [Ableitung]:
- je Lage 1 `LandscapeLayerSample` und 2–3 Rechenknoten, also etwa **25–30 Anweisungen** (447 → ~475);
- **0 neue Sampler, 0 neue SRV**, solange alle 5 Lagen schon in der Mischung stehen.

Bitte im Material-Stat prüfen, dass die Zahl der Texturen gleich bleibt. Wenn nicht, die Lage aus dem Tint nehmen.

**Texturtausch später**, wenn nach V19 noch nötig:
- **Tausch statt Zusatz:** Die Geroell-Lage nimmt `T_MossyRockyGround_01` statt `T_ground_stones_01`. Das kostet 0 SRV, ändert aber
  Geroell **weltweit**; das ist eine Entscheidung für Ferat.
- **Zusatz nur über Texture-Arrays** (V20).

### 2.3 Reihenfolge

1. **`Ufer_Staerke` Bach 0** (Instanzwert), BaseColor messen (1.2).
2. **Lagen unter dem Spiegel über `s38 lagen`** (Geroell 30, Kies 15, Fels 20, Felsplatte 10, Schlamm 12, Algen 13). Das ist
   reine Datenarbeit; die Mischung selbst trägt viel zum Grau bei.
   - **Achtung SRV:** Neue Lagen in einem Teil kosten eine Gewichtskarte je 4 Lagen und die Texturen der Lage, wenn der Teil
     sie noch nicht hat (Algen, Felsplatte).
   - Danach den SRV-Prüflauf (Abschnitt 4).
   - Kippt ein Teil über 64: dort Algen → Schlamm und Felsplatte → Fels zusammenlegen. Optisch kostet das wenig.
3. **V19-Tönung je Lage** (2.2).
4. Texturtausch nur, wenn der Grund dann noch beige ist.

## 3. Mündung

### 3.1 Würdigung der Reparatur

- **Richtig erkannt** [Befund]: Der Sattel bis 36,98 m (Mündung beim Plugin-Graben ausgenommen) machte Pfützen.
- Das Weitergraben mit 32°-Ufern, nur Abtrag (54 m³), ist das, was unsere Ufer-Regel will.
- C3-Kopf auf 24/31/38 m mit 7/11/14 m und Auffächern auf 17–26 m: genau die Kopf-Kürzung aus Nachtrag 3, mit besserem Übergang.
- Front 788/788 [Befund].

### 3.2 Die schmale Anfangskante von oben

**Ursache** [Ableitung]: Ein `WaterBodyRiver` beginnt mit einer harten Kante quer zur Spline. Am C3-Kopf liegen zwei Wasserkörper
übereinander: das p2-Wasser (läuft bis s 788 in den Fluss) und der C3-Fluss ab dist 24 m. Ihre Flächen liegen fast gleich hoch,
aber nicht exakt. Von oben sieht man deshalb die Startkante des C3-Netzes als Linie.

**Abhilfe:**

| Maßnahme | Wert |
|---|---|
| C3-Start **unter** das p2-Wasser legen | ersten Punkt 3–5 m stromauf in das p2-Band (dist ≈ 20 m); dort liegt die Kante unter der p2-Fläche |
| gleiche Höhe am Übergang | C3-Punkt 0 = p2-Spiegel an derselben Stelle (36,80 m), Punkt 1 höchstens 2 cm tiefer |
| Startbreite | = p2-Breite dort (≈ 5–7 m), dann wie heute auffächern |
| Vorrang | `Overlap Material Priority` p2 > C3 (z. B. 12 gegen 10): In der Überlappung zeichnet p2, die C3-Kante verschwindet darunter |
| SWR | die C3-SWR (F_ERLENBACH) beginnt mit dem Spline; ihre Quelle liegt im p2-Abfluss, das ist gewollt |

Wenn ihr den Kopf so verschiebt, bitte die neuen Kopfpunkte melden. Sie stehen dann in `ersetzt.json` → `lokaler_kopf`.

### 3.3 Export nachgezogen (`ersetzt.json`, Exporter, Prüfer)

- **`ersetzt.json`** → `ersatz.ERLENBACH_P2.muendung_anschluss`:
  - `p2_spiegel_m` 36,80;
  - neu `lokaler_kopf` mit `s_m` [24, 31, 38], `spiegel_m` [36,80; 36,72; 36,64], `breite_m` [7, 11, 14] und `folge_breite`
    (s 44,5/59,4/74,2/89,0 → 17/22/26/25 m).
  - Annahme: eure Punkte 3–6 sind die Weltpunkte ab s 44,5. Dafür spricht, dass die Punkte 5 und 6 mit 26/25 m übereinstimmen.
    Bitte bestätigen.
- **Exporter** (`kopf_kuerzen`): Mit `lokaler_kopf` beginnt die Linie am ersten Kopfpunkt. Die Kopfpunkte ersetzen die Weltpunkte
  bis s 38 m (x/y auf der Weltlinie interpoliert), danach die Folgebreiten. Ohne `lokaler_kopf` gilt die Regel aus Nachtrag 3.
- **Prüfer:** wie in v12. Der Anfangsspiegel muss ≤ p2-Spiegel + 2 cm sein, der Schnitt zum Lauf passen.

**Lauf** (2-m-Daten, v12 = Stand Nachtrag 3):

| | v12 (Nachtrag 3) | **v12 mit lokalem Kopf** |
|---|---|---|
| `F_ERLENBACH` | 590,1 m, Anfang s 33,57 m auf 36,88 m, Breite wie Welt (36 m), `3fab28f7938b…`, 131 Objekte, Zelle 0,284 m | **599,7 m**, Anfang **s 24 m auf 36,80 m**, Breite 7 → 14 m (danach 17/22/26/25 m), **`576f7efc4372…`**, 124 Objekte, Zelle 0,282 m |
| Zuflüsse `B_R2_K10_TUNDRA_02` / `_01` | s 114,95 / 159,29 | s 124,52 / 168,86 |
| Fingerabdrücke geändert | – | `F_ERLENBACH`, `B_R2_K10_TUNDRA_01` (`27db9408e730…` → `675a9001f930…`, 53 → 51 Objekte), `B_R2_K10_TUNDRA_02` (`a883b260d9da…` → `1fb9cbb66e1d…`, 31 → 30); die übrigen 194 gleich |
| Prüfer | 0 FEHLER, 0 WARNUNG, 74 HINWEIS | **0 FEHLER, 0 WARNUNG, 74 HINWEIS** („Spline beginnt bei 3680,0 cm …, Kopf 24,00 m gekürzt“) |
| Determinismus | – | zwei Läufe byte-gleich |

- **Neu backen:** `F_ERLENBACH`, `B_R2_K10_TUNDRA_01`, `B_R2_K10_TUNDRA_02`. Die beiden Tundra-Bäche ändern sich nur im
  Objektteil, weil am schmaleren Kopf andere Steine im Wasser liegen.
- Die Beispiele unter `antworten/fluss_sim/` (`F_ERLENBACH`, `zusammenfassung.json`, `wasserzonen.json`,
  `back_liste_auszug.json`) sind neu.

### 3.4 Müssen unsere Weltdaten den Graben kennen?

**Nein** [Ableitung]:
- Lokal läuft der Export auf `export/unreal/welt` (1 m). Dort sind die 54 m³ schon in `hoehe.f32` eingetragen; der Rückweg liegt in
  `hoehe.*.vor_brush_muendung_p2`. Fingerabdruck und SWR-Rechteck entstehen also aus dem richtigen Gelände.
- Die 2-m-Cloud-Kopie (`vorlagen/daten/sehens`) ist ein Teststand. Ihre Fingerabdrücke weichen von den lokalen ohnehin ab und
  werden nie gebacken.
- Nur wenn ihr Cloud-Zahlen 1:1 lokal vergleichen wollt, bräuchten wir einen neuen 2-m-Export der Welt.
- Der 16g-§8-Hinweis bleibt richtig (Kürzung umgesetzt) und muss nicht geändert werden.

## 4. SRV-Prüflauf über 70 Felder: worauf achten

1. **Gleiche Farbe in V18 und V18s.** V18s muss dieselben 23 V18-Knoten mit denselben Werten haben. Prüfen:
   - je Feld mit umgestellten Teilen ein Bild entlang einer Grenze V18/V18s, im Bach und trocken;
   - Pipette links und rechts der Grenze (BaseColor), Unterschied ≤ 2 %.
2. **Was V12s weglässt:** Wenn V12s Lagen zusammenlegt oder Detail-Texturen (Makro, Normal) spart, entstehen Nähte bei
   Steinen und Sand, die man im Bach von nah sieht. Die Liste der umgestellten Teile mit ihren Nachbarn notieren.
3. **Teil- statt Feldgrenzen:** Die Grenze verläuft an Landschaftsteilen (Komponenten). Ein Bach, der quer über eine Teilgrenze
   läuft (p2 in C2), zeigt die Naht besonders.
4. **Nach den Lagen unter dem Spiegel noch einmal laufen lassen** (2.3). Neue Lagen in Bachteilen sind der wahrscheinlichste
   Grund für weitere Teile über 64.
5. **Gras und RVT:** Ist RVT an, muss V18s dieselben RVT-Ausgänge schreiben. Gras-Karten nach dem Umstellen neu bauen, nur für die
   betroffenen Teile.
6. **Liste ausgeben:** Feld, Teil, SRV vorher/nachher, Lagen im Teil (Anzahl, Namen). Damit kann ich sagen, welche Lagen man
   zusammenlegen kann.

## 5. Was lokal zu tun ist

Commit **`5fdba07`** holen.

1. `Ufer_Staerke` Bach 0; BaseColor an t500 messen (Ziel Y ≤ 0,15 unter Wasser).
2. Lagen unter dem Spiegel über `s38 lagen`, dann SRV-Prüflauf; Teile über 64 nach 2.3 zusammenlegen.
3. V19 (2.2) ohne neue Texturen; Material-Stat prüfen (Texturen gleich).
4. Mündungskante nach 3.2 (C3-Start unter p2, Vorrang p2); neue Kopfpunkte melden.
5. fluss_sim lokal neu exportieren und neu backen, siehe 3.3.

## Quellen

- Ferats Nachtrag 4 und Bilder (siehe Kopf).
- [Epic-Forum: Shader is using too many SRVs (only 64 supported), UE 4.26](https://forums.unrealengine.com/t/ue4-26-shader-is-using-too-many-srvs-only-64-supported/154906)
  und [#14](https://forums.unrealengine.com/t/ue4-26-shader-is-using-too-many-srvs-only-64-supported/154906/14) – je Teil, `MAX_SRVS`,
  `static_assert` (Suchauszug).
- [Epic-Forum: too many Samplers (only 16 supported)](https://forums.unrealengine.com/t/shader-is-using-too-many-samplers-23-only-16-supported/478724)
  – Shared: Wrap (Suchauszug).
- [Epic-Forum: Landscape material layer limit](https://forums.unrealengine.com/t/landscape-material-layer-limit/356679),
  [Landscape Texture Limits](https://forums.unrealengine.com/t/landscape-texture-limits/88442) (Suchauszug, ältere Versionen).
- Jensen, Legakis, Dorsey 1999, Rendering of Wet Materials (nasse Oberflächen dunkler), wie Nachtrag 1.

## Rückfragen

1. **BaseColor-Messwert** an t500 (unter Wasser, nasses Band, trockener Kies) nach `Ufer_Staerke` 0.
2. **Folgebreiten:** Sind eure C3-Punkte 3–6 die Weltpunkte ab s 44,5 m?
3. **SRV-Liste** nach dem Prüflauf (Abschnitt 4 Punkt 6).
