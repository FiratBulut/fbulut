# Antwort zu 16g Nachtrag – Ursache gefunden: Wasser-Info der Water Zone zu grob

Stand 13.10.2026. Grundlage sind Ferats Nachtrag `auftraege/16g-nachtrag-ursache-gefunden.md` (07:05), unsere Antwort
[`16g-swr-steiler-bergbach.md`](16g-swr-steiler-bergbach.md) und `skripte/fluss_sim/` (jetzt Regeln v10).

**Kennzeichnung:**
- [Befund N]: Ferats Messung aus dem Nachtrag
- [Doku]: Epic-API- bzw. Python-Doku, nur als Suchauszug (`dev.epicgames.com` ist aus der Cloud weiter gesperrt, DNS-Fehler)
- [Forum]: Epic-Forum, Suchauszug
- [14b], [16g]: frühere Antworten im Repo
- [Ableitung]: aus Belegen und Befunden geschlossen und gerechnet
- [unsicher]: nicht belegt, im Test klären

---

## Kurzfazit

1. **Die Ursache ist bestätigt.** Befund 1 unserer 16g-Antwort trifft zu (Rang 1 der Ursachen): Die Spline-Information
   (innen/außen und Höhe) kommt aus einer 2D-Textur, und die war zu grob.
   - `C2_Wasserzone`: 1208 m / 1024 = **1,18 m je Pixel**. Das 1,6–2,4 m breite Bett ist 1–2 Pixel breit, liegt schräg im
     Raster und bekommt Lücken. Dort fehlt der SWR der Fluss: kein Nachfüllen, `remove_outside` löscht, die Front steht.
   - Mit 4096 (0,29 m je Pixel) ist das Bett **zu 99,9 % nass bis s 780**. Die Tiefe in der Mitte (0,44–0,64 m) liegt nahe am
     Plan (0,53–0,69 m) [Befund 4096-Lauf].
2. **Neue Regel im Export (v10):** Pixel der Wasser-Info ≤ **schmalste Bachbreite / 6** (Ferats Regel).
   - Je SWR-Bereich gibt der Export jetzt die schmalste Breite, die größte zulässige Pixelgröße und die größte Zone je
     Auflösung aus („Zone ≤ X m bei 4096“).
   - Für eine 1208-m-Zone nennt er die nötige Auflösung.
3. **C2 (1208 m):**
   - Ein 2-m-Bach braucht 0,33 m je Pixel, also **4096**.
   - Ein 1,6-m-Bett braucht streng nach der Regel 0,27 m, also eine Zone von **höchstens 1092 m** bei 4096. Mit 1208 m bei 4096
     liegen 5,4 Pixel quer über dem Bett, und Ferats Lauf zeigt, dass das reicht.
   - Empfehlung: C2 auf 4096 lassen (gemessen gut). Für neue Zonen gilt die Regel mit 6. Die Rückfrage 1 klärt, ob 5 statt 6
     genügt.
4. **Welt (9,6 × 7,1 km), Vorschlag aus den 2-m-Daten:** **29 Zonen.**
   - Eine Grundzone `WZ_WELT` (4096², 2,34 m je Pixel) für Seen, Meer und die 6 breiten Flüsse ab 14 m.
   - Dazu 28 feine Zonen für 181 Bäche und schmale Flüsse: 0,1–4 km groß, Auflösung je Achse 256–4096, 0,09–1,9 m je Pixel.
   - Jedes Gewässer bekommt seine Zone als `WaterZoneOverride`.
   - Speicher, wenn alle Zonen geladen sind: **1 427 MB in RGBA16F bzw. 2 854 MB in RGBA32F**. Das Format ist unbekannt, Ferat
     bitte nachsehen (Rückfrage 2).
   - Mit World Partition sind nur die Zonen in der Nähe geladen, wenn die Zone räumlich geladen wird [unsicher, Rückfrage 3].
5. **Der Vorschlag gilt erst nach einem lokalen Lauf auf 1 m.** Die 2-m-Plan-Breiten sind teils viel breiter als das lokale
   Bett: Der Erlenbach ist in den 2-m-Daten mindestens 12,7 m breit, lokal 1,6–2,4 m. Der Export rechnet lokal mit den
   echten Breiten neu.
6. **Damit erledigt aus 16g:**
   - Stillstand, Abbruchkante bei s 62, Front bei s 231 und fehlendes Nachfüllen.
   - Testplan-Stufen 0–5.
   - Plan B als Pflicht: Er bleibt nur, wenn das Bild es braucht.
   - Die Eignungsklassen im Export (`swr`/`pruefen`/`kaskade_vorschlag`) sind jetzt **Info**.
   - Der 10-m-Vorlauf an der Quelle ist nur noch eine **Option**.
7. **Offen sind nur Feinwerte:**
   - Überlauf neben dem Bett, Schaum, Tempo.
   - `remove_outside_spline_amount` **50 wieder testen**, weil das Band jetzt sauber gerastert ist.
   - Quellspeisung messen.
   - Testreihe in Abschnitt 4.
8. **Export und Prüfer:**
   - Der Prüfer meldet 0 FEHLER, 0 WARNUNG, 74 HINWEIS.
   - Zwei Läufe sind byte-gleich (184 Dateien).
   - `back_liste.json`, `vorschlaege.json` und alle **Fingerabdrücke sind unverändert**: Es muss nichts neu gebacken werden.
   - Mit `--zonen` (bekannte Zonen) meldet der Prüfer FEHLER bei Pixel > Breite / 6. Für C2 bei 1024 sind das 7 FEHLER, bei
     4096 keiner.

---

## 1. Abgleich mit der 16g-Antwort

| 16g | Aussage | Stand jetzt |
|---|---|---|
| Rang 1 | Die Spline-Information der SWR kommt aus einer 2D-Textur (Water-Info der SWR bzw. der Zone) und fehlt ab s ≈ 62 m bzw. ist dort falsch | **bestätigt.** Es war die Auflösung der Zonen-Water-Info |
| 1.3 g | „Eine schmale steile Rinne ist bei groben Texeln nur 1–2 Texel breit“; Höhenfehler = Texel × Gefälle; C2-Zone 1,18 m | **bestätigt** (Ferat: 1–2 Pixel, Lücken) |
| 1.3 g | Die gerade Kante spricht für einen Textur- oder Zonenrand bzw. eine Höhenlinie | **falsch gedeutet.** Die Kante wanderte mit Splineform und -breite, also waren es Rasterlücken [Befund] |
| Rang 2/3 | Kaum Durchfluss, Abfluss über den Rechteckrand, Quelle halb außerhalb | **nachrangig.** Mit 4096 läuft das Bett bis s 780 voll, obwohl die Quelle unverändert am Rand liegt [Ableitung; Rückfrage 4] |
| Rang 5–7 | Reibung, Zeitschritt, 16 Bit | nicht die Ursache; Reibung und Zeitschritt bleiben Feinwerte |
| Stufe 6 | Auflösung der Water-Info verdoppeln, „nur wenn T0-3 ≤ 512 Texel zeigt“ | **zu spät eingeordnet.** Dieser Lauf hätte an den Anfang gehört. Bei 1024 lagen schon nur 1–2 Pixel quer über dem Bett |
| Befund 6 | Abfrage mit z = 0 liefert talwärts versetzte Punkte | bleibt gültig (unabhängig von der Zone) |

**Lehre für die Regeln:**
- Bisher hat der Export nur die **Simulationszelle** geprüft (Bach 0,25–0,40 m).
- Die **Wasser-Info** ist eine zweite, oft viel gröbere Auflösung. Sie bestimmt, wo die SWR „Fluss“ sieht.
- Die neue Regel prüft deshalb genau diese Auflösung.

---

## 2. Die Regel und die Zahlen

### 2.1 Regel (Export `swr.water_info`, Regeln v10)

**Pixel der Wasser-Info der zuständigen Zone ≤ schmalste Bachbreite / 6.**
- Pixel = Zonen-Ausdehnung / `render_target_resolution`, je Achse; maßgeblich ist der größere Wert.
- Breite = `RiverWidth` der Splinepunkte im SWR-Bereich, also das Plan-Bett. Ist die Spline lokal breiter (Bett + 2 m), ist
  die Regel strenger als nötig, nie zu lasch.

| schmalste Breite | Pixel ≤ | Zone ≤ (1024) | Zone ≤ (2048) | Zone ≤ (4096) | Auflösung in 1208-m-Zone |
|---|---|---|---|---|---|
| 0,7 m (Rinnsal Erlenbruch) | 0,117 m | 119 m | 239 m | **478 m** | 16 384 (nicht möglich) |
| 1,6 m (Erlenbach, Rinne lokal) | 0,267 m | 273 m | 546 m | **1 092 m** | 8 192 (bei 4096: 5,4 Pixel quer) |
| 2,0 m | 0,333 m | 341 m | 683 m | **1 365 m** | **4096** |
| 2,4 m | 0,400 m | 410 m | 819 m | 1 638 m | 4096 |
| 3,0 m | 0,500 m | 512 m | 1 024 m | 2 048 m | 4096 |
| 5,0 m | 0,833 m | 853 m | 1 707 m | 3 413 m | 2048 |
| 14 m | 2,33 m | 2 389 m | 4 779 m | 9 557 m | 1024 (Grundzone reicht) |

Pixel quer über das Bett in C2 (1208 m) [Ableitung]:

| Bett | 1024 (1,18 m) | 2048 (0,59 m) | 4096 (0,295 m) |
|---|---|---|---|
| 1,6 m | **1,4** | 2,7 | **5,4** |
| 2,0 m | 1,7 | 3,4 | 6,8 |
| 2,4 m | 2,0 | 4,1 | 8,1 |
| Band Bett + 2 m (3,6–4,4 m) | 3,1–3,7 | 6,1–7,5 | 12–15 |

- Gemessen: **1,4 Pixel → Lücken, 5,4 Pixel → 99,9 % nass.**
- Wo die Grenze dazwischen liegt, zeigt Lauf F6 (2048 = 2,7 Pixel). Danach lässt sich der Teiler 6 bestätigen oder auf 5
  senken (`breite_teiler` in den Regeln).

### 2.2 C2 (bekannte Zone 1208 × 1208 m)

- **Ab sofort 4096.** Das ist Ferats getestete Einstellung: 0,295 m je Pixel, 128 MB in RGBA16F.
- **Streng nach der Regel** reicht das für Betten ab 1,77 m. Für das 1,6-m-Bett im Erlenbach gibt es zwei Wege:
  - (a) **Teiler 5** akzeptieren (gemessen gut).
  - (b) Zone auf ≤ 1092 m verkleinern oder auf den Erlenbach zuschneiden. Ein Beispiel ist ein Rechteck um das Bett + 10 m,
    in den 2-m-Daten etwa 320 × 990 m → 2048 × 4096 → 0,24 m je Pixel, 64 MB statt 128 MB [Ableitung].
- **Achtung:** Ein Water Body gehört zu **einer** Zone [14b: `WaterZoneOverride` bzw. `overlap_priority`]. Das ganze Bett des
  Erlenbachs bis zur Mündung muss deshalb in seiner Zone liegen.
  - Mit der angenommenen Lage (Mitte von Feld C2) ragt der Erlenbach in den 2-m-Daten bis 484 m aus der Zone
    (Prüfer-WARNUNG).
  - Ferats Lauf war bis s 780 nass. Die echte Zone liegt also anders, oder der lokale Lauf ist anders (Rückfrage 4).

### 2.3 Weltzonen-Vorschlag (`fluss_sim/wasserzonen.json`, 2-m-Daten)

**Vorgehen** (deterministisch, `zonen_vorschlag` im Export):
1. **Grundzone `WZ_WELT`** über die ganze Welt (9 577 × 7 057 m, 4096 × 4096 → 2,34 m je Pixel, `overlap_priority` 0).
   - Sie nimmt alle Gewässer auf, deren schmalste Breite ≥ 14 m ist: `F_HAUPTFLUSS_1/2/3`, `F_DSCHUNGELFLUSS`,
     `F_GLETSCHERTAL`, `F_CANYONBACH`.
   - Sie trägt auch Seen und Meer (nicht im Export).
2. **Feine Zonen `WZ_Fnn`** (`overlap_priority` 10). Die übrigen Gewässer werden nach geforderter Pixelgröße (die strengsten
   zuerst) gierig gruppiert:
   - Ein Gewässer kommt in die Zone, deren Speicher dadurch am wenigsten wächst.
   - Bedingung 1: Die Zone hält danach mit ≤ 4096 je Achse noch die Regel für alle ihre Gewässer.
   - Bedingung 2: Der Zuwachs ist nicht größer als eine eigene Zone + 32 MB (`zone_aufschlag_mb`).
   - Sonst bekommt das Gewässer eine neue Zone.
   - Zone = Rechteck um alle Betten + 10 m; Auflösung je Achse = kleinste Zweierpotenz, die die Regel erfüllt.
3. Jedes Gewässer bekommt `water_body.water_zone_vorschlag` = seine Zone. Im Editor als **`WaterZoneOverride`** setzen, weil sich
   feine Zonen untereinander (26 Paare) und mit der Grundzone überlappen.

**Ergebnis (2-m-Daten, 187 Gewässer, 199 SWR-Bereiche):**

| Auflösung (Pixel) | Zonen | Gewässer | MB je Zone (16F / 32F) | Beispiele (Ausdehnung m, Pixel m) |
|---|---|---|---|---|
| 4096 × 4096 | 3 | 39 | 128 / 256 | `WZ_WELT` (9 577 × 7 057, 2,34); `WZ_F15` (1 279 × 1 174, 0,31, 21 Bäche); `WZ_F20` (1 264 × 1 347, 0,33) |
| 4096 × 2048 bzw. 2048 × 4096 | 10 | 86 | 64 / 128 | `WZ_F10` (1 338 × 454, 0,33); `WZ_F21` (593 × 1 425, 0,35) |
| 4 Mio. Pixel (1024 × 4096, 2048², 4096 × 1024) | 11 | 45 | 32 / 64 | `WZ_F17` (3 949 × 1 208, 1,18, Altarm + Elfenfluss); `WZ_F19` (125 × 188, 0,09, Rinnsal 0,7 m) |
| 2 Mio. Pixel (4096 × 512, 2048 × 1024) | 3 | 14 | 16 / 32 | `WZ_F05` (1 655 × 204, 0,40) |
| ≤ 512 × 512 | 2 | 3 | 1–2 / 2–4 | `WZ_F06` (Erlenbach: 321 × 988, 1,93, wegen 12,7 m Plan-Breite) |
| **Summe** | **29** | **187** | **1 427 / 2 854** | Feine Zonen allein: 1 299 / 2 598 MB; keine über 4096 |

- **Schmalste Breiten** (199 SWR-Bereiche): Minimum 0,7 m, Median 2,83 m. 43 Bereiche liegen bei ≤ 2 m (fast alle genau
  2,0 m = Untergrenze der 2-m-Plan-Breite).
- **In einer 1208-m-Zone** bräuchten die 199 Bereiche folgende Auflösungen:

  | Auflösung | 256 | 512 | 1024 | 2048 | 4096 | 16 384 |
  |---|---|---|---|---|---|---|
  | SWR-Bereiche | 12 | 3 | 5 | 15 | **163** | 1 (Rinnsal) |

  Bei 1024 hätten **179 von 199** weniger als 6 Pixel quer über dem schmalsten Bett.
- **Zum Vergleich** [Ableitung]:
  - Ein festes Raster aus 1208-m-Zonen in 4096 (8 × 6 = 48 Zonen, 6,1 GB in 16F) erfüllt die Regel nicht. Die Gewässer
    laufen über die Feldgrenzen, ein Water Body gehört aber zu einer Zone.
  - Eine einzige Weltzone in 8192 hätte 1,17 m je Pixel, also wieder die C2-Lage von heute.
- **Lokal auf 1 m neu rechnen.** Mit den echten Bettbreiten (1,6 m statt 2 m) werden die feinen Zonen kleiner bzw. feiner. Der
  Export verkleinert sie dann selbst.

### 2.4 Speicher und Kosten

| Auflösung | RGBA16F (8 B je Pixel) | RGBA32F (16 B je Pixel) |
|---|---|---|
| 1024² | 8 MB | 16 MB |
| 2048² | 32 MB | 64 MB |
| 4096² | **128 MB** | 256 MB |
| 8192² | 512 MB | 1 024 MB |

- **Format unbekannt** [Doku]: `bHalfPrecisionTexture` wählt „16 oder 32 Bit je Kanal“.
  - Die Kanalzahl ist aus A12 angenommen: 4 Kanäle (XY Velocity, Z Wasserhöhe, W Bodenhöhe) [14b].
  - Die Zone hält die Info als **Texture-2D-Array** (`WaterInfoTextureArray`, `WaterInfoTextureArrayNumSlices`) [Doku].
    Mehr als ein Slice vervielfacht den Speicher [unsicher].
  - Bitte nachsehen: Zone → *Half Precision Texture*; Größe im Editor mit `memreport -full` oder `stat RHI` vor und nach dem
    Umstellen auf 4096 (Rückfrage 2).
- **Kosten** [Ableitung, 14b]:
  - Die Info-Textur wird beim Laden und bei Änderungen an Water Bodies neu gezeichnet, nicht jedes Bild
    (`r.Water.WaterInfo.ForceUpdateWaterInfoNextFrames` erzwingt das).
  - Teuer ist vor allem der **Speicher der geladenen Zonen**.
  - Die SWR-Kosten (Live-Simulation 0,8–9,7 ms, gebacken ~0,2 ms; 16c) ändern sich durch die Zone nicht.
- **Im Spiel:**
  - Die Grundzone (128 MB in 16F) ist immer geladen, dazu die feinen Zonen in der Nähe.
  - Liegen 2–4 feine Zonen im Ladebereich, sind das etwa 100–400 MB in 16F [Ableitung, wenn Zonen räumlich geladen werden;
    Rückfrage 3].

### 2.5 Was Epic dazu sagt (Recherche, nur Suchauszüge)

- **`AWaterZone::RenderTargetResolution`** ist ein `FIntPoint`, also je Achse getrennt.
  - Doku: „Use Getter to access value since CVar **r.Water.WaterInfo.RenderTargetResolutionMax** may clamp the resolution“
    [Doku].
  - Eine Auflösung über der CVar wird also still gekappt. Den Standardwert der CVar habe ich nicht gefunden.
  - **8192 deshalb nicht vorschlagen.** Erst prüfen, ob die CVar es zulässt (Rückfrage 5), sonst kleinere Zonen.
  - In Python ist die Eigenschaft ab 5.4 nur lesbar, also im Details-Panel setzen [14b].
- **Editor-Vorgabe:** `FWaterZoneActorDefaults::RenderTargetResolution` legt die Auflösung neuer Zonen fest [Doku]. Ältere
  Editor-Einstellungen kennen eine Obergrenze `MaxWaterVelocityAndHeightTextureSize` je Zone [Doku, Version unklar].
- **`ZoneExtent`** („maximum size in local space“, `FVector2D`), **`OverlapPriority`** (höher gewinnt),
  **`bHalfPrecisionTexture`** (16/32 Bit je Kanal), **`CaptureZOffset`** [Doku]. Water Bodies können über
  **`WaterZoneOverride`** fest an eine Zone gebunden werden [14b, Doku].
- **Local Tessellation** (`enable_local_only_tessellation`): Die Info-Textur deckt nur ein gleitendes Fenster um die Kamera
  ab, mit höherer Pixeldichte [Doku].
  - Ein Epic-Forenbeitrag (japanisch) empfiehlt sie für große Welten statt vieler Zonen [Forum].
  - **Für SWR-Backen nicht empfohlen** [unsicher]: Beim Backen muss das Fenster das ganze SWR-Rechteck abdecken. Ferats C2-Zone
    hat sie aus.
- **World Partition:** Die Zone hat `is_spatially_loaded`. An: Sie lädt mit den Streaming-Quellen. Aus: Sie lädt nur über
  Data Layers [Doku]. Ein Forenfaden meldet für 5.3/5.4, dass nicht räumlich geladene Akteure im Standalone-Spiel trotzdem
  räumlich geladen wurden (UE-219132) [Forum].
- **Nicht gefunden:** Eine Epic-Aussage, wie groß eine Zone je Auflösung sein soll, und eine Anleitung für **mehrere Zonen**
  in World Partition. Das Forum kennt nur „unter 512 Einheiten Breite gibt es Auflösungsprobleme; Info-Auflösung erhöhen und
  Zone Extent anpassen“ [Forum, 14b]. Die Regel „Breite / 6“ ist also **Ferats Messung**, kein Epic-Wert.

### 2.6 Export und Prüfer (Regeln v10)

**Export** (`skripte/fluss_sim/`, README „Ergänzungen 16g Nachtrag“):

| Feld | Inhalt |
|---|---|
| `swr_bereiche[].water_info` | `breite_min_m` (+ `breite_min_s_m`), `breite_median_m`, `pixel_max_m` (= Breite / 6), `zone_max_m` {1024, 2048, 4096}, `zone_bekannt` (1208 m: `aufloesung`, `pixel_m`, `ueber_max`, `pixel_quer` je Auflösung) |
| `water_body.water_zone_vorschlag` | Zone des Gewässers (für `WaterZoneOverride`) |
| `wasserzonen.json` (neu) | Zonen mit Rechteck, Zentrum, Ausdehnung, Auflösung, Pixel, schmalstem Gewässer, `overlap_priority`, Speicher 16F/32F, Gewässern und SWR-Bereichen; Summe; Zuordnung Gewässer → Zone |
| `zusammenfassung.json` → `water_info` | Breiten, Pixel, Zonengrößen, Auflösungen in 1208 m, Zonenvorschlag |
| Regeln `swr.water_info` | `breite_teiler` 6, `aufloesung_max` 4096, `zone_bekannt_m` 1208, `zonen.rand_m` 10, `zone_aufschlag_mb` 32, Grundzone 4096², Prioritäten 0/10, Bytes je Pixel |

**Prüfer:**
- Rechnet `water_info` und `wasserzonen.json` neu; eine Abweichung ist ein FEHLER.
- Prüft je vorgeschlagener Zone die Regel und ob das Bett in der Zone liegt (FEHLER).
- `water_zone_vorschlag` muss passen.
- Zwei HINWEIS-Zeilen (Water-Info, Water Zones).

**Neu: `--zonen DATEI`** (Beispiel `skripte/fluss_sim/zonen_beispiel_c2.json`):
- Bekannte Zonen mit `ausdehnung_m`, `aufloesung` und Lage (`zentrum_cm`, `rechteck_cm` oder `feld`), optional
  `overlap_priority` und `gewaesser` (Override).
- Zuständig ist die Override-Zone, sonst die überlappende Zone mit der höchsten Priorität.
- **Pixel > Breite / 6 = FEHLER** mit nötiger Auflösung bzw. Zonengröße. Bett außerhalb der Zone = WARNUNG.
- Ohne `--zonen` gibt es nur die Empfehlung.

**Lauf** (2-m-Daten, Scratchpad):
- Vorlauf: Gefälle-Planer `--alle` (123 Läufe, 0 FEHLER), 15 Sehens-Planer, `bachbett_roh` (0 FEHLER), dann der Export
  zweimal.
- Ergebnis: 187 Gewässer, 199 SWR-Bereiche, 762 Fälle (wie v9).

| Prüfung | Ergebnis |
|---|---|
| Prüfer (mit Daten, `--vergleich`) | **0 FEHLER, 0 WARNUNG, 74 HINWEIS** (72 wie v9 + Water-Info + Water Zones) |
| Determinismus | 184 Dateien byte-gleich (180 `fluss_sim.json`, `back_liste`, `vorschlaege`, `zusammenfassung`, `wasserzonen`) |
| gegen v9 (alter Code, gleiche Eingaben) | `back_liste.json` und `vorschlaege.json` byte-gleich → **Fingerabdrücke und `sim_vorgaben` unverändert**; in `fluss_sim.json` nur `water_info`, `water_zone_vorschlag`, `rand_steil.status` und `regeln_version` neu |
| `--zonen zonen_beispiel_c2.json` (C2 1208 m, 1024, Mitte Feld C2 angenommen) | 9 SWR-Bereiche zuständig, **7 FEHLER** (z. B. `B_R2_K10_TUNDRA_01`: 1,18 m > 2,0 / 6 = 0,33 m → 4096 oder Zone ≤ 1365 m), 2 WARNUNG (Bett ragt aus der angenommenen Zone, Erlenbach bis 484 m) |
| dieselbe Zone mit 4096 | 0 FEHLER, 2 WARNUNG (wie oben) |
| Gegenproben (Exit 1) | `pixel_max_m` von Hand 0,5 → 2 FEHLER; `WZ_F15` auf 2048² → 19 FEHLER; `water_zone_vorschlag` falsch → 1; `water_info` entfernt → 1 |

**Beispiele neu** unter `antworten/fluss_sim/`: `F_ERLENBACH`, Karsee, Elfentreppe, `zusammenfassung.json`,
`wasserzonen.json`. `back_liste_auszug.json` und `vorschlaege.json` sind gleich geblieben.

---

## 3. Was von 16g erledigt ist und was bleibt

| Punkt aus 16g | Stand | Was tun |
|---|---|---|
| Stillstand, Kante s 62, Front s 231, kein Nachfüllen im Durchbruch | **erledigt** (Wasser-Info) | C2 auf 4096 lassen; andere Zonen nach `wasserzonen.json` |
| Testplan Stufe 0–5 (Bilanz, Quelle/Rand, Spline-Info, Rampentest, Numerik) | **überholt** (Ferat) | entfällt; Rampentest T4 nur, falls ein Bild Fragen aufwirft |
| Befund 6 (Abfrage mit z = 0) | gilt weiter | Wasserstand immer mit z = Planspiegel abfragen |
| **Überlauf neben dem Bett** | offen | Testreihe F1/F2 |
| **Schaum** | offen | Testreihe F4 (FoamAtten 2,5/4,5 m/s, Niagara-Restrict wie 16f) |
| **Tempo** | offen | Testreihe F5 |
| **Quellspeisung, 10-m-Vorlauf** | **nur noch Option.** Mit 4096 füllt die Quelle die Rinne bis s 780, obwohl sie am Rand liegt [Befund, Rückfrage 4]. Der Export meldet `rand_steil.anfang.zu_nah` weiter als Info | Vorlauf nur, wenn F3 an der Quelle zu wenig Wasser zeigt (erste 30 m flacher als 70 % des Plans) |
| **`remove_outside_spline_amount`** | Regel steht weiter auf **50** (v8). 0 war nur die Diagnose wegen der lückenhaften Maske | **50 wieder testen** (F1). Das Band ist jetzt sauber gerastert, 50 sollte nur noch neben dem Band löschen |
| `match_spline_height_amount` | 0,02 (v8) | in F2 mit 0 / 0,02 / 0,05 |
| **Plan B Kaskade für > 30 %** | **nur noch bei Bedarf.** Die Rinne lief mit 39–64 % Gefälle bis s 780 | nur, wenn ein Bild (Glaswand, Treppe ohne Strahl) es verlangt; Vorhänge warten weiter (16c) |
| Eignung `swr`/`pruefen`/`kaskade_vorschlag` | **Info.** Status in den Regeln und HINWEIS im Prüfer („nur Bildprüfung, Plan B nur bei Bedarf“); Werte unverändert (129 / 52 / 18) | Liste nur noch als Reihenfolge für Bildprüfungen nutzen |
| Rechteck ohne Rand (Befund 8), Rückfrage 3 aus 16g | offen, aber nachrangig | `rechteck_m` weiter mit ± halber Breite; erst nach Bestätigung ändern |
| Teilen der Simulation (16g 4.2) | unverändert | eine SWR je Gewässer |

---

## 4. Feinwerte-Testreihe (C2, Zone 4096; je Lauf Reset, 120 s, dann Messung)

Messgrößen wie 16g: nasser Anteil **im Bett** und **außerhalb des Bands**, Front-s, Tiefe Mitte gegen Plan, Tempo an 5 Lippen.

| Lauf | Änderung (Rest wie Ferats 4096-Lauf) | Erfolg, wenn |
|---|---|---|
| **F1** | `remove_outside_spline_amount` 0 → **50** | Bett weiter ≥ 99 % nass bis zur Mündung; außerhalb des Bands < 1 % nass |
| **F2** | Spline-Breite Bett statt Bett + 2 m; `match_spline_height_amount` 0 / 0,02 / 0,05 | Überlauf neben dem Bett < 5 % der Bandfläche; Tiefe Mitte ≥ 80 % des Plans |
| **F3** | Quelle ohne Vorlauf (heute) gegen 10 m Vorlauf mit Quellbecken (16g 2.3) | ohne Vorlauf: Tiefe in den ersten 30 m ≥ 70 % des Plans → Vorlauf entfällt endgültig |
| **F4** | Schaum: FoamAtten 2,5 / 4,5 m/s bzw. Niagara-Restrict (16f) | Schaum nur an Lippen und Fällen, nicht im ganzen Bett |
| **F5** | Tempo: `sim_speed`/`num_steps` 10/10 gegen 5/20; `tempo_faktor` 1,0 gegen 0,8 | Lippen ruhig, keine Spitzen; Bildeindruck „Wildbach“, nicht „Rutsche“ |
| **F6** | Zone 2048 (0,59 m, 2,7 Pixel quer über 1,6 m) | eicht die Regel: Lücken → Teiler 6 bleibt; keine Lücken → Teiler 5 genügt |
| **F7** | Zwei Zonen überlappend: Grundzone 4096 + feine Zone mit `WaterZoneOverride` für den Erlenbach | Wasser nur einmal gezeichnet (kein doppeltes Netz, kein Flackern); SWR wie in F1 |

**Reihenfolge:** F1 → F2 → F3 → F6 → F7 → F4 → F5. Die Bake-Fingerabdrücke ändern sich durch keinen dieser Werte.
`sim_vorgaben` und Zone sind beim Backen mitzunehmen.

---

## Quellen

Alle Epic-Seiten waren aus der Cloud nicht lesbar (DNS-Fehler). Die Inhalte stammen aus Suchmaschinen-Auszügen.

**Epic (Doku, API):**
- [AWaterZone (API)](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/AWaterZone): `RenderTargetResolution`
  (FIntPoint, „CVar r.Water.WaterInfo.RenderTargetResolutionMax may clamp the resolution“), `ZoneExtent`, `OverlapPriority`,
  `bHalfPrecisionTexture`, `WaterInfoTextureArray`/`NumSlices`, `CaptureZOffset`, Local Tessellation [Doku]
- [FWaterZoneActorDefaults](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterEditor/FWaterZoneActorDefaults):
  Vorgabe `RenderTargetResolution` [Doku]
- [unreal.WaterZone (Python)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterZone):
  `enable_local_only_tessellation`, `is_spatially_loaded`, `capture_z_offset` [Doku];
  [WaterZone 5.2](https://docs.unrealengine.com/5.2/en-US/PythonAPI/class/WaterZone.html)
- [UWaterEditorSettings](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterEditor/UWaterEditorSettings):
  `MaxWaterVelocityAndHeightTextureSize` [Doku]
- [FWaterInfoTextureRenderingParams](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/FSceneView/FWaterInfoTextureRenderingParams) [Doku]
- [Water Meshing System and Surface Rendering](https://dev.epicgames.com/documentation/unreal-engine/water-meshing-system-and-surface-rendering-in-unreal-engine):
  Zone nötig, große Extents kosten Leistung [Doku]
- [UE-296375](https://issues.unrealengine.com/issue/UE-296375): fehlerhaft gerenderte WaterInfoTexture (Wasser fehlt oder
  „in Blöcken“), VR; Bezug zur Auflösung offen [Bug]

**Epic-Forum (Auszüge):**
- [waterzone (japanisch): Local Tessellation für große Welten](https://forums.unrealengine.com/t/waterzone/2719663)
- [Non-spatially loaded World Partition actor becomes spatially loaded in Standalone](https://forums.unrealengine.com/t/1409411) (UE-219132)
- „Unter 512 Einheiten Breite Auflösungsprobleme“ (Forum, zitiert in [14b](14b-befund-geteilte-baeche.md))

**Projekt:**
- `auftraege/16g-nachtrag-ursache-gefunden.md` (Befunde), [`16g-swr-steiler-bergbach.md`](16g-swr-steiler-bergbach.md)
  (Rang 1, 1.3 g, Testplan), [`14b-befund-geteilte-baeche.md`](14b-befund-geteilte-baeche.md) (Zone, Override, Kanäle A12),
  `16c-…` (SWR-Kosten), `16f-…` (Schaum, Startwerte)
- `skripte/fluss_sim/` (Regeln v10, Export, Prüfer, README, `zonen_beispiel_c2.json`), `fluss_sim/wasserzonen.json`

---

## Rückfragen

1. **Teiler 6 oder 5?**
   - Dein 4096-Lauf hatte am 1,6-m-Bett 5,4 Pixel quer und war 99,9 % nass. Nach Regel 6 müsste die C2-Zone ≤ 1092 m sein.
   - Vorschlag: F6 (2048) laufen lassen. Bleibt es lückenlos, setze ich `breite_teiler` auf 5. Sonst bleibt 6 und C2 bekommt
     eine zugeschnittene Erlenbach-Zone.
2. **Texturformat:**
   - Steht `Half Precision Texture` an der `C2_Wasserzone` auf an (16 Bit) oder aus (32 Bit)?
   - Wie viel Speicher zeigt `memreport -full` bzw. `stat RHI` für die Zone bei 1024 und 4096? Gibt es mehr als einen Slice
     im `WaterInfoTextureArray`?
3. **World Partition:** Ist `Is Spatially Loaded` an der Zone an? Sonst sind alle Zonen immer geladen (1,4 bzw. 2,9 GB beim
   Vorschlag).
4. **Lage und Inhalt von `C2_Wasserzone`:**
   - Bitte Location und Zone Extent nennen; dann trage ich sie in `zonen_beispiel_c2.json` ein.
   - Liegt der Erlenbach bis zur Mündung in dieser Zone, oder hat er eine eigene bzw. einen Override?
   - Lag die Quelle im 4096-Lauf noch 0,2 m vom Rand (dann ist der Vorlauf endgültig nur Option)?
5. **Obergrenze der Auflösung:** Was zeigt die Konsole für `r.Water.WaterInfo.RenderTargetResolutionMax` (Name ohne Wert
   eingeben)? Steht dort ≥ 8192, wäre 8192 für einzelne Zonen möglich (512 MB in 16F). Ich empfehle trotzdem kleinere Zonen.
6. **Lokaler Lauf:** Bitte den Export auf 1 m laufen lassen und den Prüfer mit `--zonen` (eure echten Zonen). Erst dann ist die
   Zonenliste für die Welt verbindlich; die 2-m-Breiten sind zu grob.
