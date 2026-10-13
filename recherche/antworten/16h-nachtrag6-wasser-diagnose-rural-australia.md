# Antwort zu 16h Nachtrag 6 – Diagnose D, W1–W3, N1–N4, S2/S6, Rural-Australia-Wasser, Plugin „Water Dynamics“, nasse Steine

Stand 13.10.2026. Grundlage: `auftraege/16h-nachtrag6-wasser-diagnose-rural-australia.md` (0e9e00e), Bilder
`bilder/swr_p2/diagnose_d.jpg`, `varianten_w.jpg`, `varianten_w_nah.jpg`, `varianten_n.jpg`, `boden_braun_s0_s5.jpg`,
`boden_braun_s6.jpg`, `rural_australia_material_test.jpg`, Graph-Dump `antworten/fluss_sim/p2_lokal/master_graph_schaum8.json`,
Parameterliste `bilder/swr_p2/mi_el_swr_klar_parameter.txt`, unsere Antworten 16f, 16h N2/N4/N5/N5b und 18.

**Kennzeichnung:**
- [Befund] Ferats Test oder Messung
- [Bild] eigene Messung im JPG (tonemapped, nur relativ)
- [Graph] aus dem Graph-Dump, [MI] aus der Parameterliste
- [Doku-Auszug] Epic-Doku, nur als Suchauszug gelesen (dev.epicgames.com war aus der Cloud nicht erreichbar)
- [Auszug] Suchauszug einer Sekundärquelle
- [Projekt] frühere Recherche im Repo
- [Ableitung] eigene Schlussfolgerung, nicht belegt
- [unsicher] im Editor prüfen

---

## Kurzfazit

1. **Ferats Befund stimmt, und wir lagen daneben.**
   - Das Marmor-Milchige war zum großen Teil der **helle Grund**, gebrochen durch die Normalen. Meine Messung bestätigt das:
     - Ohne sichtbares Wasser (RA1) ist der Bett-Bereich nah vor der Kamera schon **80–98 %** so hell wie mit unserem Wasser (RA0).
     - Mit S6 halbiert sich die Helligkeit dort (Y 0,42 → 0,20 bei t430).
   - Unsere Fehler:
     - **N5:** Wir haben „der Boden ist der Hebel“ für erledigt erklärt. Unser Ziel „BaseColor unter Wasser ≤ 0,15“ war für dieses Licht viel zu hell, und V19 („fast schwarz“) haben wir zu früh verworfen.
     - **18:** „Hebel sind die Normalen, nicht die Rauheit“ war falsch. Die Normalen formen das Muster, sichtbar wird es aber erst durch den hellen Grund. Die Rauheit wirkt dabei messbar, wenn auch wenig.
2. **Endstand der Wasser-Instanz** (`MI_EL_SWR_Klar`, „nicht stumpf“):
   - ELD-Wirbel aus (W1, wie in S6);
   - `Water Roughness` **0,025**;
   - `Sim Velocity Normal Strength` **5**;
   - `Refraction` 1,15 → **1,10**;
   - alles andere bleibt.
   - Der dunkle Grund aus S6 bleibt im Landschaftsmaterial.
   - Die 0,10 aus N5b ziehe ich zurück.
3. **Rural Australia (Frage 1): Drei Prinzipien lassen sich in Single Layer Water übernehmen, das Material selbst nicht.**
   - **Normalen nah flach** (neu V20a): ein Faktor über `PixelDepth` auf die fertige Normale. 8 Knoten, 0 Texturen, wirkt auch mit der gebackenen SWR.
   - **Grund am Ufer abdunkeln:** Das hat Ferat mit S2 schon gemacht. Fast mit Rural Australias eigenem Farbton: (0,20; 0,14; 0,09) gegen (0,224; 0,165; 0,106).
     - In SLW gibt es dafür den Eingang `Color Scale Behind Water` (V20b).
     - Er dunkelt alles hinter dem Wasser ab, auch Steine, und hängt nicht vom 2-m-Raster ab.
   - **Kaustik:** optional, niedrige Priorität (V20c). Am besten als Lichtfunktion der Sonne, maskiert mit der Spiegel-Karte, sonst über `Color Scale Behind Water`.
   - **Unsichtbares Wasser im Test:** Am wahrscheinlichsten ist die Deckkraft aus der gemalten Maske, die auf unserem Water-Body-Netz 0 ergibt. Prüfbar mit konstanter Deckkraft (§2.5).
4. **Water Dynamics (Frage 2): jetzt nicht.**
   - Die Doku war aus der Cloud nicht erreichbar. Die Suche fand weder ein Fab-Listing noch einen Preis oder Erfahrungen.
   - Nach Ferats Doku-Auszug sprechen dagegen:
     - 10–11 ms CPU;
     - „few active rivers per level“;
     - keine Zusammenflüsse;
     - kein Backen.
   - Übernehmen lassen sich als Ideen: Kaustik nach Sonnenrichtung (V20c) und Klarheits-Voreinstellungen als Kind-Instanzen. Schaum-Transport brauchen wir nicht.
5. **Nasse Steine (Frage 3):**
   - Eine Materialfunktion `MF_EL_Nasslinie` (neu) für Bachdekor-Steine und Totholz.
     - Die Spiegelhöhe kommt aus der **vorhandenen** `T_Eldarien_Wasserspiegel_2m`.
     - Unter Spiegel + 8 cm: Albedo × 0,5, Entsättigung 0,3, Rauheit 0,2; Übergang bis + 20 cm.
   - **Grund-Ton im Bach ab 0 cm statt ab 5 cm:** ja, voll ab 6 cm.
   - Für die Lippen zusätzlich V20b, weil das 2-m-Raster an Stufen die Tiefe unterschätzt.
6. **Step-Pools (Frage 4):** beantwortet die getrennte Antwort `16h-nachtrag6c-becken-kuenstlich.md`.

---

## 1. Diagnose D, W1–W3, N1–N4, S2/S6

### 1.1 Was die Tests zeigen

| Test | Befund | Was daraus folgt |
|---|---|---|
| D (Da–De) | Gold kommt mit der Lumen-Spiegelung (Dd grauer, De wie D0), die Sonne ist es nicht (Dc) [Befund] | Ferats Deutung stimmt: Das **Gold in der Ferne** ist die Lumen-Spiegelung von Hängen und Himmel. W4 entfällt zu Recht |
| W1 | wirkt am stärksten, kühler, weniger Gold [Befund] | Unser ELD-Wirbel hat die Spiegelung verwischt, wie in N5 vermutet |
| W2, W3, N1–N4 | ändern das Muster nah vor der Kamera **nicht** [Befund] | Die Normal-Regler sind **nicht** der Hebel gegen das Nah-Muster |
| Rauheit 0,025 | wie W1, etwas schärfer [Befund] | Die Rauheit wirkt, wenn auch schwach |
| S1 | Wasser braun: kaum Wirkung [Befund] | bei ≈ 0,5 m Tiefe färbt die Absorption kaum (wie T0) |
| **S2/S6** | Grund dunkelbraun: Milch weitgehend weg [Befund] | **Der Grund ist der Haupthebel** für den Nahbereich |

**Meine Messung** [Bild]:
- Messfeld: unteres Bildmittel, 72–97 % der Höhe und 30–70 % der Breite.
- Werte: Leuchtdichte Y nach sRGB-Linearisierung und K = Streuung / Mittel.

| Kamera | RA0 (unser Wasser) | RA1 (Wasser unsichtbar = nur Grund) | S0 | **S6** |
|---|---|---|---|---|
| t430 Auge | Y 0,41, K 0,39 | Y 0,35, K 0,51 | Y 0,42, K 0,37 | **Y 0,20**, K 0,81 |
| t500 Auge | Y 0,40, K 0,26 | Y 0,32, K 0,43 | – | (S6-Bild bei t500 zeigt eine Draufsicht) |
| t550 Auge | Y 0,44, K 0,42 | Y 0,43, K 0,50 | Y 0,46, K 0,43 | Y 0,29, K 0,66 |

- **Der Grund allein liefert schon 80–98 % der Helligkeit**, die man nah vor der Kamera „im Wasser“ sieht. Das Wasser legt etwa 20 % darauf und senkt die Struktur (K 0,51 → 0,39), es wirkt also wie ein Schleier.
- S6 halbiert die Helligkeit. K steigt, weil die hellen Bachdekor-Steine jetzt vor dem dunklen Grund stehen (Frage 3).
- Grenzen der Messung: Belichtung und Himmel waren nicht eingefroren, RA1 ist kein exakter „Grund ohne Wasser“, und Zeilen und Kameras gelten nur grob. Die Richtung ist aber eindeutig.

**Warum die Normal-Regler nichts tun** [Graph, MI, unsicher]:
- `Default Near/Distant Normal Strength`, `Water Distant Normal Offset/Length` (über `CameraDepthFade`) gehen in `WaterTextureSurface`.
- Dort hängt auch der Schalter `Enable Waves`, und der steht in `MI_EL_SWR_Klar` auf **False**.
- Gut möglich, dass dieser Zweig für unsere Flüsse gar nicht wirkt. Das würde erklären, warum W2 und N4 nichts ändern.
- Die tatsächlich wirksamen Bewegungsnormalen sind die aus `WaterRiverFlowmaps` (SWR-Strömung, `Sim Velocity Normal Strength`) und unser ELD-Wirbel.
- Nicht weiter an den Default-Normal-Reglern drehen.

### 1.2 Wo unsere Antworten daneben lagen

| Antwort | Unsere Aussage | Richtig ist |
|---|---|---|
| N5 Kurzfazit 1 | „Unsere Annahme ‚der Boden ist der Hebel‘ ist erledigt“ (BaseColor 0,067 ≤ 0,15) | **Falsch.** Der Boden war weiter der Haupthebel. Unser Zielwert 0,15 galt für die Farbe des Grunds an sich. Für klares, flaches Wasser auf Augenhöhe unter hoher Sonne ist er zu hell, weil der Grund nah vor der Kamera fast ungedämpft durchscheint |
| N5 §1 | V19 nicht bauen, „0,04–0,05 wäre fast schwarz“ | **Falsch eingeschätzt.** S2 liegt vermutlich in genau diesem Bereich (Kies × (0,20; 0,14; 0,09) × Nässe [Ableitung]) und sieht richtig aus. Bitte BaseColor von S6 messen (Rückfrage 1); das wird das neue Ziel |
| 18 Kurzfazit 3, §3.1 | „Unter Lumen spiegelt SLW wie ein Spiegel, deshalb sind die Normalen der Hebel, nicht die Rauheit“ | **Zur Hälfte falsch.** Die Normalen erzeugen das Muster (W1 hilft), sichtbar wird es aber durch den hellen Grund. Die Rauheit wirkt messbar (0,025 schärfer). Das Doku-Zitat „forced to mirror“ beschreibt die Lumen-Spiegelung, nicht den ganzen Glanz |
| N5b Kurzfazit 1 | Zwischenstand Rauheit 0,10 | zurückgezogen; die Tests sprechen für niedrig und scharf (1.3) |
| N5b, N5 | Gold = Spiegelung der Hänge, `Fluidsim Normal Strength` kein Hebel | **bestätigt** (D, N1) |
| N2 | Die Flecken sind Steine, verzerrt durch die Normalen | bestätigt; die Steine leuchten jetzt erst recht (Frage 3) |

**Lehre für uns:** Gegen „milchig“ hilft zuerst der Kontrast Grund zu Ufer, erst danach die Oberfläche. Ein Messwert der Grundfarbe allein sagt
wenig, wenn das Licht hoch und hart ist. Künftig messen wir gegen das Ufer im selben Bild (wie in N5b §4).

### 1.3 Empfehlung Endstand

**`MI_EL_SWR_Klar`:**

| Parameter | heute (S6) | **Endstand** | Begründung |
|---|---|---|---|
| `ELD_Wirbel_Normal` / `ELD_Wirbel_Staerke` / `ELD_Schaum_Normal` | 0 / 0 / 0 | **0 / 0 / 0** | W1 wirkt am stärksten [Befund] |
| `Water Roughness` | 0,04 | **0,025** | getestet: wie W1, etwas schärfer [Befund]. Das ist „nicht stumpf“. Flackern Glanzpunkte in Bewegung, dann 0,03 |
| `Sim Velocity Normal Strength` | 5 (falls Z gesetzt), sonst 15 | **5** | G2: nur ruhiger, ohne Nachteil [Befund N5b]. Wirken Rinnen im Video tot, dann über V20a (fern) oder später „Normalen nach Tempo“ (18 §3.1) anheben, nicht global |
| `Refraction` | 1,15 | **1,10** | weniger Versatz des Grunds; Rural Australia nutzt 1,1. Einfluss auf das Muster bisher nicht messbar (N3), deshalb niedrige Priorität [Ableitung] |
| `Water Specular`, `Water Fresnel *` | 0,225 / unverändert | **unverändert** | G3 wirkungslos, physikalisch passend (N5b §2) |
| `Fluidsim Normal Strength`, `Default Near Normal Strength` | Testwerte zurück | **1 / 0,25** (Ausgangswerte) | wirkungslos (N1, N4) |
| Absorption, Streuung | „klar wie F“ | **unverändert** | S1: Farbe des Wassers wirkt bei dieser Tiefe kaum |

**Landschaftsmaterial (V18):** `Ufer_Staerke_Bach` 1,0, `Ufer_Farbe_Bach` (0,20; 0,14; 0,09) und `Entsaettigung_Nass` 0,5 bleiben (S6).
Neu ist nur die Schwelle „ab 0 cm“ für Bäche (§4.3).

**Nicht tun:** die Rauheit hochsetzen (Rural Australia nutzt 0,8, siehe §2.1), mehr Streuung, den Specular-Wert der Sonne global senken.

---

## 2. Frage 1 – Prinzipien aus `M_Water_01` für `M_Eldarien_Wasser_Schaum8`

### 2.1 Warum Rural Australia gut aussieht (aus Ferats Werten)

[Ableitung aus Ferats Editor-Werten, Material selbst nicht gelesen]:
- **Dunkel statt Spiegel:**
  - Grundfarbe 0,016; der Untergrund wird bis 2,5 m vom Ufer mit (0,224; 0,165; 0,106) multipliziert.
  - Rauheit 0,8: Die Spiegelung ist breit verwischt.
  - Das Wasser liest sich über Dunkelheit und Tiefe, nicht über klare Spiegelbilder.
- **Nah fast flach** (0,02): Der Grund nah vor der Kamera wird kaum verzerrt, also entsteht kein Marmor. Fern (0,5) und am Streifwinkel (1,4 bei Exponent 9) bricht die Fläche die Spiegelung auf.
- **Kaustik** gibt dem flachen Grund Leben, ohne Normalen.
- **Eine Maske von Hand** steuert Deckkraft und Trübung je Stelle.

Diese Lösung ist für eine **Translucent-Ebene in einer festen Karte** gebaut. Rauheit 0,8 und die gemalte Maske passen nicht zu SLW mit
SWR-Strömung und Lumen-Spiegelung, die Prinzipien aber schon.

**Hinweis** [MI]: Unsere Instanz hat bereits `Far Normal Fresnel Power` **9**. Das ist derselbe Exponent wie Rural Australias Streifwinkel-Term.
Der Streifwinkel-Teil steckt also schon in Epics Funktionen. Nachbauen müssen wir nur „nah flach“.

### 2.2 Was davon in Single Layer Water übertragbar ist

| Prinzip | Rural Australia (Translucent) | In SLW | Wirkt mit gebackener SWR (WCBS)? |
|---|---|---|---|
| Normalen nah flach, fern stärker | Stärke nach Abstand | **ja**: Faktor über `PixelDepth` auf die fertige Normale (V20a) | **ja.** Das Material wird jedes Bild je Pixel ausgewertet; die gebackenen Daten liefern nur Strömung und Höhe in die Flowmap-Normalen. V20a skaliert das Ergebnis [Ableitung] |
| Streifwinkel stärker | Exponent 9 | **schon vorhanden** (`Far Normal Fresnel Power` 9) [MI] | ja |
| Untergrund am Ufer abdunkeln | Untergrund × Farbe bis 2,5 m | **ja, doppelt**: (a) im Landschaftsmaterial (S2, erledigt), (b) über den SLW-Eingang `Color Scale Behind Water`, der die Helligkeit hinter dem Wasser multipliziert [Doku-Auszug] (V20b) | ja |
| Kaustik | im Wassermaterial | **nur bedingt**: `Color Scale Behind Water` „projiziert keine Kaustik“ [Doku, Projekt `ufer-kies-coast-dunes.md`]. Möglich sind eine Lichtfunktion an der Sonne (Legacy-Pfad) oder ein Muster über `Color Scale Behind Water` (V20c) | ja |
| Rauheit 0,8 | breiter Glanz | **nein**: würde stumpf machen (Ferats Leitlinie); unter Lumen anderer Spiegelweg | – |
| Gemalte Maske | Deckkraft und Trübung je Stelle | **nein**: Unsere Netze kommen aus der Water Zone; Ersatz sind Tiefe und Bachgewicht | – |
| Panning-Normalen (30 m, Tempo 0,1) | feste Richtung | **nein**: Wir haben die Flowmap aus der SWR | – |

### 2.3 Knoten-Skizzen

Alle drei bauen wir als Gruppe „V20 Nahbereich“ im Master, mit Schaltern, die im Ausgangszustand nichts verändern. Die Parameter sind neu, die Namen schlage ich vor.

**V20a – Normalen nah flach** (8 Knoten, 0 Texturen):
1. `PixelDepth` → `Subtract(ELD_Nah_Ende_cm)` → `Divide(ELD_Nah_Uebergang_cm)` → `Saturate` = t
2. `Lerp(ELD_Normal_Nah; 1; t)` = k
3. Direkt vor dem Ausgang: `GetMaterialAttributes` (Normal) = N
4. `Lerp(A = (0; 0; 1); B = N; Alpha = k)` → `Normalize` → `SetMaterialAttributes` (Normal)

| Parameter | Start | Test | Anmerkung |
|---|---|---|---|
| `ELD_Normal_Nah` | 1 (aus) | **0,35** | Rural Australia geht auf 0,02. Für Bäche mit Strömung bleibt nah etwas Bewegung |
| `ELD_Nah_Ende_cm` | 300 | 300 | bis 3 m voll flach |
| `ELD_Nah_Uebergang_cm` | 900 | 900 | bei 12 m volle Stärke (Rural Australia 15–30 m, unsere Bäche sind enger) |

- Der Lerp zu (0; 0; 1) funktioniert im Tangenten- wie im Weltraum, weil die Wasserfläche fast waagrecht liegt [Ableitung].
- **Was es bringt:** SLW verzerrt den Grund über die Normale (Brechung) [Doku-Auszug]. Flacher heißt: Die hellen Steine nah vor der Kamera
  zittern weniger (sichtbar in `boden_braun_s6.jpg` t430). Die Spiegelung in der Ferne bleibt.
- **Prüfung:** t430 Auge, K im Nahfeld gegen S6 und ein 5-s-Video; Rinnen dürfen nicht tot wirken (K5 aus 18).

**V20b – Grund-Ton hinter dem Wasser** (`Color Scale Behind Water`, 7 Knoten, 0 Texturen):
1. `SceneDepthWithoutWater` − `PixelDepth` = Wasserdicke entlang der Blickrichtung d (cm). Der Knoten ist der übliche Weg in SLW-Materialien
   [Projekt `ufer-kies-coast-dunes.md`, unsicher in 5.8].
2. `Saturate(d / ELD_Grund_Rampe_cm)` = r (weicher Rand an der Wasserkante)
3. `Lerp((1; 1; 1); ELD_Grund_Skala; r)` → Eingang **Color Scale Behind Water** am SLW-Ausgang

| Parameter | Start | Test |
|---|---|---|
| `ELD_Grund_Skala` | (1; 1; 1) = aus | **(0,80; 0,78; 0,75)** |
| `ELD_Grund_Rampe_cm` | 5 | 5 |

- Laut Graph-Dump hängt am Eingang `Color Scale Behind Water` kein Parameter. Er steht also wohl auf dem Standardwert [Graph, unsicher].
- **Warum zusätzlich zum Landschaftsmaterial:**
  - Er wirkt auf **alles** unter Wasser, auch auf Steine und Holz.
  - Er gilt dort, wo die SWR-Fläche wirklich liegt, unabhängig vom 2-m-Raster der Spiegel-Karte, und hilft so an den Lippen.
- Er dunkelt auch den S6-Grund um 20 % ab. Wird es zu dunkel, `Ufer_Farbe_Bach` auf (0,24; 0,17; 0,11) anheben.

**V20c – Kaustik** (optional, nach V20a/b, Priorität niedrig wie in 18):
- **Weg 1 (bevorzugt): Lichtfunktion am Directional Light.**
  - Lichtfunktionen der Sonne laufen über den Legacy-Pfad, den Atlas liest das Directional Light nicht [Projekt `ufer-kies-coast-dunes.md`, nach Epic-Doku].
  - Die Lichtfunktion liest die Weltposition: Spiegel aus `T_Eldarien_Wasserspiegel_2m` minus Welt-Z = Tiefe. Kaustik nur bei Tiefe > 0, voll bei 0,2–0,8 m, aus ab 2 m (16f §5.2).
  - Zwei gepannte Kaustik-Lagen, 1,5–3 m Kachel, mit `Min` verbunden.
  - Vorteile: richtig nach Sonnenrichtung, im Schatten automatisch aus, wirkt auf Grund, Steine und Holz.
  - Kosten: ein Vollbild-Durchgang der Sonne mit Lichtfunktion. Vor dem Bauen messen [unsicher].
- **Weg 2 (billig): Muster in V20b.**
  - `ELD_Grund_Skala` × Lerp(0,8; 1; Kaustik).
  - UV = Wasser-Weltposition XY + Parallaxe zum Grund. Die Sonnenrichtung geht als Versatz −L.xy / L.z × Tiefe ein: L aus dem Knoten
    `SkyAtmosphereLightDirection` [Name unsicher] oder aus einem MPC-Vektor per Blueprint.
  - Nachteil: weiß nichts vom Schatten, also nur schwach einsetzen.
- **Epics eigener Schalter `Caustics`** (`WaterCaustics_GerstnerWaves`) [Graph] hängt an Gerstner-Wellen, die unsere Flüsse nicht haben.
  Wirkung vermutlich gering (18 §3.7). Ein Test mit einem Bild ist billig (Rückfrage 3).
- Die Textur: eine kachelbare Kaustik-Textur aus dem Projekt-Inventar. Einen Namen nenne ich nicht, weil ich keinen prüfen kann.

### 2.4 Wirkt das in der gebackenen SWR-Darstellung?

- **Ja, für alle drei** [Ableitung]. WCBS ersetzt nur die Laufzeit-Simulation durch gebackene Strömung und Höhe. Die Oberfläche zeichnet
  weiter `M_Eldarien_Wasser_Schaum8` in jedem Bild. V20a–c sind reine Pixel-Rechnung auf dem Ergebnis.
- **Grenze:** V20a nimmt nah auch sichtbare Strömung weg. Deshalb 0,35 statt 0,02, und später mit „Normalen nach Tempo“ (18 §3.1) kombinieren.

### 2.5 Warum das Wasser im Test unsichtbar wurde

Belegt ist nur Ferats Befund: Translucent und Default Lit, Deckkraft und Trübung aus einer von Hand bemalten RGB-Maske, auf der p2-Spline
unsichtbar, keine Spiegelung sichtbar. Mögliche Ursachen [Ableitung, nach Wahrscheinlichkeit]:

1. **Maske auf dem falschen Netz.**
   - Die Maske ist für Rural Australias eigenes Fluss-Netz gemalt, als Textur in dessen UVs oder als Vertex-Farbe.
   - Unser Water Body wird als Netz der Water Zone gezeichnet. Es hat weder diese UVs noch diese Farben, deshalb liest die Maske dort
     unpassende Werte, und bei Kanal 0 ist die Deckkraft 0.
   - Dazu passt: Im Bild ist **gar nichts** vom Wasser zu sehen, auch keine Spiegelung.
2. **Ufer-Ausblendung über die Tiefe.**
   - Falls das Material Ufer und Ausblendung (bis 50 cm bzw. 2,5 m) aus der Szenentiefe ableitet, ist unser Bach mit ≈ 0,47 m Tiefe
     überall „Ufer“.
   - Das wäre eine Ausblendung auf ganzer Fläche.
3. **Translucent statt SLW im Water-Body-Slot.**
   - SLW ist ein eigener Durchgang mit eigenen Daten. Laut Doku läuft er mit Opaque oder Masked, nicht mit Translucent [Doku-Auszug].
   - Ob die Water Zone ein Translucent-Material überhaupt richtig zeichnet, ist **nicht belegt**. Ein Grund für ganz unsichtbares Wasser
     ist es eher nicht, weil Translucent dann wenigstens die Spiegelung zeigen müsste.

**Prüfung (2 min, nur Speicher):** In der Kopie die Deckkraft auf die Konstante 0,6 legen, die Trübung auf eine Konstante.
- Wird das Wasser sichtbar, ist es Ursache 1 oder 2.
- Bleibt es unsichtbar, ist es Ursache 3.

Für die Entscheidung ist das zweitrangig. Das Material ersetzen wir nicht, wir übernehmen die Prinzipien (2.2).

---

## 3. Frage 2 – Plugin „Water Dynamics“

### 3.1 Quellenlage

- **Doku nicht erreichbar:** `tsibatov.github.io` wurde vom Proxy der Cloud abgewiesen (403 bzw. DNS). Ein Quell-Repo `tsibatov/water-dynamics` auf GitHub ist nicht zugänglich.
- **Suche** (13.10.2026): Unter „Water Dynamics“ mit Sibatov, Fab, `WDWaterAuthoringLibrary` oder „RockyClear“ fand ich **kein Fab-Listing, keinen Preis, keine Erfahrungsberichte und keine Erwähnung** [Auszug].
  - Gefunden habe ich nur andere Produkte: Dynamic Real Water (FFT-Ozean, laut Listing ohne Flüsse), Fluid Flux, EasyWaterscape.
  - Das deckt sich mit Ferats Befund „auf Fab unter dem Namen nicht gefunden“.
- Alles Folgende stützt sich deshalb **nur auf Ferats Auszug aus der Doku**.

### 3.2 Bewertung für Eldarien [Ableitung aus Ferats Auszug]

| Punkt | laut Doku (Ferat) | für Eldarien |
|---|---|---|
| CPU | 10–11 ms für 2 Flüsse + 3 Fälle | Bei 60 fps ist das **zwei Drittel des Bild-Budgets** (16,7 ms), in einer offenen Welt mit World Partition, PCG und Gras. Unsere gebackene SWR liegt bei ≈ 0,2 ms (Messung 16) |
| Umfang | „Plan for a few active rivers per level“ | Eldarien hat viele Bäche in einer Welt. Ob „level“ eine WP-Zelle meint und ob man nach Entfernung abschalten kann, steht nicht im Auszug |
| Zusammenflüsse | keine; Fälle verbinden getrennte Flüsse | p2 → C3 ist genau ein Zusammenfluss, die Mündung haben wir gerade mühsam gebaut (N4/N5) |
| Backen | nicht erwähnt | Dann läuft die CPU-Last immer, solange der Fluss aktiv ist |
| Gelände | kein Graben | Kein Nachteil: Wir graben selbst |
| Darstellung | eigene Oberfläche (Art unbekannt) | Ein **zweiter Wasser-Weg** neben Epic Water mit SWR. Doppelte Pflege, und Übergänge an den Rändern der Schau-Stelle |
| Preis und Lizenz | unbekannt | Ferats Regel: kein Geld, solange es gleichwertig kostenlos geht. Ohne Listing ist auch der Lizenzweg unklar |

**Empfehlung: jetzt nicht.**
- **Später höchstens für eine einzige Schau-Stelle** (großer Fall am Startort), und nur wenn alles davon zutrifft:
  1. Fab-Listing mit Preis und Lizenz liegt vor, der Preis ist klein;
  2. Abschalten nach Entfernung oder Schlafen ist dokumentiert;
  3. an der Stelle gemessen < 2 ms CPU;
  4. die Fall-Tests mit SWR, Schaum-Kapseln und Nature Water FX (18 §3.5) reichen dort nachweislich nicht.
- Bis dahin gilt 18: Fälle über die SWR, Nature Water FX (gekauft) und Netz-Vorhänge.

### 3.3 Was wir an Techniken übernehmen

| Technik (laut Auszug) | übernehmen? | wie |
|---|---|---|
| Kaustik nach Sonnenrichtung | **ja, als Idee** | V20c, Weg 1 (Lichtfunktion der Sonne) oder Weg 2 (Versatz −L.xy / L.z × Tiefe) |
| Klarheits-Voreinstellungen (z. B. „RockyClear“, 8 m Sicht) | **ja, billig** | Unsere Absorption ist schon in Sichtweite je Farbe (cm) angegeben [MI]. Die Voreinstellungen werden Kind-Instanzen von `MI_EL_SWR_Klar`: „klar Fels“ = heute (400/900/750 cm), dazu je eine für Humus-Bach und Moor. Wirkt erst in Becken ab ≈ 1 m (S1 zeigt: bei 0,5 m kaum); deshalb erst nach dem neuen Bettplan (6c) |
| Schaum-Transport | **nein** | Ferat: kein Schaum außer an Fällen; die SWR hat eigenen Sim-Schaum, an Fällen nehmen wir die Schaum-Kapseln (16e Option B) |
| Felsen teilen die Strömung | haben wir | Wasser-Kollision der SWR (16a/16f) |
| Python-Werkzeug | – | unsere Kette (`ufer_plan_p2`, s38) deckt das Setzen ab |

---

## 4. Frage 3 – Nasse Steine, Totholz, Grund-Ton ab 0 cm

### 4.1 Woher bekommen Mesh-Materialien die Wasserhöhe?

| Quelle | Beleg | Eignung |
|---|---|---|
| **`T_Eldarien_Wasserspiegel_2m`** | [Projekt] das Landschaftsmaterial liest sie seit V12 für Nässe und Tönung (N2 §1.2) | **erste Wahl**: vorhanden und für alle Gewässer gleich. In einem Mesh-Material kostet sie keinen Landschafts-SRV |
| Water Info Texture (Water Zone) | [Projekt 16g, Doku] gleitendes Fenster um die Ansicht, zur Laufzeit neu gebaut; für Wasser-Materialien gedacht | **nicht empfohlen**: Zugriff aus Mesh-Materialien ist nicht belegt |
| Custom Primitive Data bzw. `PerInstanceCustomData` | Engine-Funktionen für Daten je Komponente bzw. je Instanz [unsicher: in 5.8 im Editor prüfen] | **Rückfall für Lippen**: Der Uferplan kennt den Spiegel je Stein (`h_ueber_spiegel_m`) und kann ihn beim Setzen mitgeben, ganz ohne Raster |

**Fehlerquelle an Stufen** [Ableitung]:
- Die 2-m-Karte wird zwischen den Zellen interpoliert. An einer Lippe mit 0,7–3,7 m Spiegelsprung (6b) zieht die Interpolation den oberen Spiegel nach unten.
- Folge: Direkt an der Lippenkrone hält das Material den Grund für **trocken bzw. flach**. Das ist ein Teil des hellen Lippen-Schleiers.
- Abhilfe für Mesh-Materialien und Landschaft: das Maximum aus 4 Abtastungen bei ±1 m in X und Y nehmen (gleiche Textur, kein neuer SRV), oder V20b.

### 4.2 `MF_EL_Nasslinie` für Bachdekor-Steine und Totholz

**Knoten-Skizze** (Materialfunktion, neu; 1 Textur, etwa 20 Anweisungen [Ableitung]):
1. Die Knoten „Weltposition → UV → Spiegelhöhe“ aus dem Landschaftsmaterial als eigene Funktion `MF_EL_Spiegelhoehe` herauslösen. Ursprung, Ausdehnung, Höhen-Dekodierung und „kein Wasser“ bleiben unverändert, beide Materialien nutzen dieselbe Funktion.
2. `h = WorldPosition.Z − Spiegel` (cm); bei „kein Wasser“ ist h groß, also bleibt der Stein trocken.
3. `nass = 1 − SmoothStep(Nass_Voll_cm; Nass_Rand_cm; h)` (voll nass bis 8 cm über dem Spiegel, trocken ab 20 cm).
4. Optional: `nass × Lerp(1; 0,6; VertexNormalWS.Z)`, damit Oberseiten schneller trocknen. Nur einbauen, wenn es zu gleichmäßig wirkt.
5. Farbe: `Lerp(BC; Lerp(BC; Luminanz(BC); Nass_Entsaettigung) × Nass_Albedo; nass)`
6. Rauheit: `Lerp(R; Nass_Rauheit; nass)`; Specular bleibt.
7. Optional für Lippen: Spiegel = max(4 Abtastungen) (4.1) oder per Instanz.

**Werte:**

| Parameter | Steine (`MI_EL_SmallStonesPack_01`) | Totholz | Grundlage |
|---|---|---|---|
| `Nass_Albedo` | **0,50** | **0,55** | nass etwa halb so hell [Projekt N1/N4, Jensen et al. 1999; Lekner & Dorf] |
| `Nass_Entsaettigung` | **0,3** | 0,2 | nimmt das Beige wie `Entsaettigung_Nass` im Grund (0,5); bei Steinen etwas weniger, damit sie nicht grau-tot wirken [Gestaltung] |
| `Nass_Rauheit` | **0,20** | 0,30 | nasser Glanz, „nicht stumpf“ (16f §5.2: 0,2–0,3) |
| `Nass_Voll_cm` / `Nass_Rand_cm` | **8 / 20** | 15 / 30 | Spritz- und Kapillarzone; Holz saugt höher [Ableitung] |

- **Unter Wasser** ist der Stein ganz nass (h < 0). Dazu wirkt V20b, falls gebaut. Die Rauheit ist dort unsichtbar, nur die Farbe zählt.
- **Trockene Teile:** Leuchten die Steine auch trocken (h > 20 cm) neben dem Bach, ist ihre trockene Grundfarbe zu hell.
  - Ziel wie beim trockenen Kies: Y **0,13–0,22** (N5 §3).
  - Liegt die BaseColor-Messung darüber, im MI zusätzlich × 0,75. Der Parametername hängt vom Eltern-Material ab (Rückfrage 2).
- **Ohne Funktion (Sofortlösung, 0 Knoten):**
  - Eine nasse Kind-Instanz für Steine, die **ganz** im Bett liegen: Albedo × 0,5, Rauheit 0,2.
  - Das geht nur, wenn das Eltern-Material Tönungs- und Rauheitsregler hat.
  - Der Name ist frei, z. B. eine Kopie von `MI_EL_SmallStonesPack_01` mit Suffix `_Nass`.
  - Der Planer setzt sie für alle Bachdekor-Steine mit h < 0,1 m. Für Steine, die aus dem Wasser ragen, braucht es die Funktion.
- **Totholz:** dieselbe Funktion im Stamm-Material der Bachdekor-Stämme (z. B. aus `SM_dead_log_03` bzw. Treibholz `FT_SM_beach_driftwood_*`,
  18 §3.8). Moos und Algen auf Holz unter Wasser sind ein späterer Schritt.
- **Kosten:** 1 Abtastung je Pixel auf Steinen und Holz. Mit Nanite unkritisch, weil kein WPO dabei ist [Ableitung]. Material-Stat vor und nach dem Einbau.

### 4.3 Grund-Ton ab 0 cm statt ab 5 cm? **Ja, für Bäche.**

- **Heute:** Die Ersetzung im Bett greift ab 5 cm Tiefe, voll ab 15 cm (16h-Materialtest §2) [Projekt]. Flache Lippen bleiben hell.
- **Neu:** für Bäche über `Lerp(Welt; Bach; Bachgewicht)` wie bei V18:

  | | Beginn | voll | Übergangsbreite |
  |---|---|---|---|
  | Welt (Seen, Flüsse) | 5 cm | 15 cm | 10 cm, unverändert (K2 helle Kiesufer) |
  | **Bach** | **0 cm** | **6 cm** | **6 cm** |

- **Warum keine harte Kante entsteht:** Über dem Spiegel liegt das nasse Band (`Nass_Breite_cm` 50, dunkel). Bei 0 cm gehen nasses Band und
  brauner Grund ineinander über [Ableitung].
- **Nicht über den Spiegel ziehen** (also nicht ab −5 cm): Sonst wird die trockene Böschung braun.
- **Lippen bleiben teils hell** wegen des 2-m-Rasters (4.1). Dafür V20b oder 4 Abtastungen.
- Wenn 6b gelöst ist, fällt auch der dünne Wasserfilm neben dem Bett weg, unter dem heute kein Grund-Ton liegt.

---

## 5. Frage 4 – Step-Pools

Die Antwort `16h-nachtrag6c-becken-kuenstlich.md` behandelt §8 und 6c gesondert (neuer Bettplan Talkaskade). Hier plane ich dazu nichts.
- Berührungspunkt: Die Klarheits-Voreinstellungen (3.3) und die Tiefen-Wirkung der Absorption lohnen erst mit den tieferen, länglichen Becken aus diesem Plan.

---

## 6. Was lokal zu tun ist (Reihenfolge)

1. **Endstand setzen** (1.3): Rauheit 0,025, `Sim Velocity Normal Strength` 5, `Refraction` 1,10, Testwerte zurück. Messung wie in N5b §4 an t430/t500/t550 gegen S6.
2. **BaseColor messen** (S6): Grund unter Wasser, nasses Band, ein Bachdekor-Stein trocken und nass. Das gibt die neuen Ziele.
3. **Grund-Ton ab 0 cm** für Bäche (4.3), Bild an einer Lippe der Talkaskade.
4. **`MF_EL_Nasslinie`** in einer Kopie des Stein-Materials, Bild t430 und Lippe; danach Totholz.
5. **V20a** (Normalen nah flach) mit `ELD_Normal_Nah` 0,35; Video 5 s an t430.
6. **V20b** nur, wenn Lippen oder Steine unter Wasser noch hell sind.
7. **Rural-Australia-Kopie:** Deckkraft-Konstanten-Test (2.5), nur zur Klärung, danach löschen.
8. **V20c und `Caustics`-Schalter:** erst nach dem neuen Bettplan (6c).

---

## Quellen

**Projekt**
- Ferats Nachtrag 6 mit Bildern (siehe Kopf), `bilder/swr_p2/mi_el_swr_klar_parameter.txt`, `antworten/fluss_sim/p2_lokal/master_graph_schaum8.json`
- Unsere Antworten `16f-water-plugin-bachbett-recherche.md` §5, `16g-swr-steiler-bergbach.md` (Water Info, gleitendes Fenster),
  `16h-nachtrag-materialtest.md`, `16h-nachtrag2-tl-t0-kasten.md` §1.2, `16h-nachtrag4-v18-muendung.md`, `16h-nachtrag5-ufer-c2-c4-lagen.md`,
  `16h-nachtrag5b-wasseroberflaeche.md`, `18-baeche-witcher-qualitaet-optionen.md`, `ufer-kies-coast-dunes.md` (Lichtfunktion der Sonne, `SceneDepthWithoutWater`)

**Epic-Doku (nur Suchauszüge, Seite aus der Cloud nicht erreichbar)**
- [Single Layer Water Shading Model](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine):
  Opaque/Masked statt Translucent, eigener Durchgang nach der Basis-Beleuchtung, Eingänge Scattering/Absorption/PhaseG/**Color Scale Behind Water**,
  Opacity regelt Volumen gegen Oberfläche, Brechung verzerrt die Probe hinter der Fläche
- [Shading Models](https://dev.epicgames.com/documentation/unreal-engine/shading-models-in-unreal-engine): Eingänge des SLW-Modells (Normal, Refraction, Opacity …)
- [Lumen GI und Reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine) („forced to mirror“, über 18)
- [UWaterBodyComponent API](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterBodyComponent)

**Rural Australia**
- [Fab-Listing Rural Australia](https://www.fab.com/listings/1c1467ce-a2f5-4be1-8988-9069f90a8571) (Suchauszug: Fotogrammetrie, vereinfachte Shader, eigene `DefaultEngine.ini` nötig)
- [80.lv: Underwater caustics in real time](https://80.lv/articles/working-with-underwater-caustics-in-real-time) (Suchauszug: lieber opak statt translucent, Translucent teuer und schlechter beleuchtet)

**Water Dynamics und andere Wasser-Plugins (Suchauszüge, 13.10.2026)**
- [Water Dynamics Doku](https://tsibatov.github.io/water-dynamics/): **nicht erreichbar**; Inhalt nur aus Ferats Auftrag
- Ohne Treffer zu „Water Dynamics“: [Fab Dynamic Real Water](https://www.fab.com/listings/84495b74-94b4-45d1-a08d-2feac2ecb92f),
  [Fab Fluid Flux](https://www.fab.com/listings/196c70cd-1283-4249-bf6b-c3019d1cbe11),
  [Fab Easy Waterscape](https://www.fab.com/listings/ddd28113-6f59-4ba3-bf60-ad7b1920a547?lang=en),
  [Fab Water Physics](https://www.fab.com/listings/bfc6b8a2-967e-45a8-bfa7-d947340992a8),
  [digitalproduction: EasyWaterscape](https://digitalproduction.com/2026/07/14/easywaterscape-brings-fft-water-to-ue5/)

**Nässe**
- [Lekner & Dorf: Why some things are darker when wet](https://www.wgtn.ac.nz/scps/staff/pdf/darkerwhenwet.pdf); Jensen, Legakis, Dorsey 1999, Rendering of Wet Materials (wie N1/N4)

---

## Rückfragen

1. **BaseColor bei S6** (Buffer Visualization → Base Color, Pipette): Grund unter Wasser, nasses Band, ein Bachdekor-Stein trocken. Damit
   ersetzen wir das alte Ziel ≤ 0,15.
2. **Stein-Material:** Welches Eltern-Material hat `MI_EL_SmallStonesPack_01`, und welche Regler hat es (Tönung bzw. Albedo-Faktor, Rauheit)?
   Liegen die Bachdekor-Steine als ISM/HISM oder als einzelne Akteure? Davon hängt ab, ob der Rückfall per Instanz-Daten (4.1) geht.
3. **`Caustics`-Schalter:** Wurde er schon einmal auf True getestet (Hauptantwort 16h, Tabelle der Wasserwerte: `Caustics` True als Test)? Ein Bild bei t430 genügt, um ihn abzuhaken.
4. **Rural Australia:** Nach dem Konstanten-Test (2.5) bitte nur das Ergebnis melden (sichtbar ja/nein). Wichtig für die Doku, nicht für unseren Weg.
5. **Water Dynamics:** Falls Ferat die Doku lokal öffnen kann: Gibt es einen Preis bzw. ein Listing, Abschalten nach Entfernung oder Backen, und
   welche Zellgröße steckt hinter den 62 400 Zellen? Erst dann lohnt eine zweite Bewertung.
