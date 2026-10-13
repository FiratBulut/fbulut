# Antwort zu 16h Nachtrag 5 – V19, Wasseroberfläche, trockener Kies, Ausschlussregeln, Mündung, SWR-Tiefen

Stand 13.10.2026. Grundlage: `auftraege/16h-nachtrag5-ufer-c2-c4-lagen.md` (c3b218d), Bilder `bilder/swr_p2/basecolor_t500.png`,
`v18_lagen_vorher_nachher.jpg`, `kant_vorher_jetzt.jpg`, `kant_vorher_nachher_1/_2.jpg`, `muendung_kante_vorher_nachher.jpg`,
Ferats Parameterliste `bilder/swr_p2/mi_el_swr_klar_parameter.txt` und Graph-Dump `antworten/fluss_sim/p2_lokal/master_graph_schaum8.json`.

**Kennzeichnung:** [Befund] Ferats Messung, [Graph] aus dem Graph-Dump, [Forum] Epic-Forum als Suchauszug, [Fach] Physik,
[Ableitung] geschlossen, [Gestaltung] Entscheidung, [unsicher] im Test klären.

---

## Kurzfazit

1. **V19: nicht bauen.**
   - Der Grund unter Wasser liegt mit Y 0,067 weit unter unserem Ziel (≤ 0,15). **Unsere Annahme „der Boden ist der Hebel“ ist
     damit erledigt.**
   - Gegen den kleinen Rest-Warmton (R 0,078 > G 0,065 > B 0,051) genügt der vorhandene Regler `Entsaettigung_Nass` 0,35 → 0,5.
     Das kostet keine Knoten.
   - Das V19-Skript bleibt als Schalter für später liegen (`V19_Staerke` 0).
2. **Hauptpunkt Wasseroberfläche: Ferats Deutung stimmt.**
   - Bei Augenhöhe spiegelt Wasser den Himmel physikalisch richtig, bei 10 m Abstand mit etwa 35 % [Fach].
   - Falsch ist nur, dass die Spiegelung **milchig und marmoriert** aussieht statt klar.
   - Wahrscheinliche Ursachen: unser **eigener ELD-Wirbel** (`ELD_Wirbel_Normal` 0,9, `ELD_Wirbel_Staerke` 0,85, im Master
     [Graph]), zu viele Normal-Lagen und eine unscharfe Himmelsspiegelung.
   - Vorschlag, ergänzend zu Ferats A/B mit Rauheit und Sim-Normale:
     - **D** eine 5-Minuten-Diagnose der Spiegelquelle;
     - **W1** ELD-Wirbel aus;
     - **W2** weitere Normal-Lagen ruhiger;
     - **W3** Fresnel später;
     - **W4** Sonnenglanz.
   - Das Wasser bleibt glänzend; nichts davon macht es stumpf.
3. **Trockener Kies 0,13:**
   - Unser Ziel 0,30–0,40 war für hellen Alpenkies gedacht und ist **für dieses Tal zu hoch**. Neues Ziel: **0,13–0,22**.
   - Die Tal-Tönung nimmt nur etwa 13 % Helligkeit, macht den Kies aber orange; die goldenen Hänge bleiben.
   - Heller machen wäre falsch: Genau ein heller Kies hat den „sandigen Graben“ gemacht.
4. **Bestätigungen:**
   - Gras-Fuß auf Schulterhöhe ist richtig gemeint.
   - Ferats Ausschlussregeln sind gut. **Unser Fehler:** Die Lippenzone als Band war fürs Ufer zu breit (84 % der Talkaskade).
     Neu in `bachbett_ufer_regeln.json` → `C_ufer.ausschluss_16h5`: nur Steine im Hauptstrahl (|s − s_Lippe| ≤ 0,75 m, d ≤ 0,5 m),
     dazu Überdeckung, zu tief, im Wasser.
   - Neue Regel „flache Steine nur bis 35°“ im Plan: 33 → 14 flache Steine. Selbsttest 0 FEHLER, Plan 0 FEHLER, byte-gleich.
   - Schutzabstand mit 34 Zellen: erwartet, weil die Bäche 8–10 m breit sind.
   - Danke für die Korrektur des Gras-Faktors.
5. **Mündung:** `lokaler_kopf` auf s 20/31/38 m, 36,80/36,78/36,64 m, Breiten 6/11/14 nachgezogen.
   - `F_ERLENBACH` 603,7 m, Fingerabdruck `ad5b1a2801f9…`; **nur dieses Gewässer neu backen**.
   - Prüfer 0 FEHLER, zwei Läufe byte-gleich.
   - Die Overlap-Priorität (p2 12 / C3 10) gehört nicht in die Back-Liste. Der Export gibt Hauptläufen 10 und Zuflüssen weniger,
     p2 liegt immer darüber. Vermerkt in `ersetzt.json`.
6. **SWR-Tiefe Talkaskade 0,47 statt 0,69 m: kein Problem** für einen 3,9 m breiten steilen Bach.
   - Ursachen: breiteres Bett nach dem Zurücklegen, Rate 0,3, Band = Bett + 2 m; Plan-Tiefe aus dem alten Kasten-Profil.
   - Optionaler Test: Tiefe getrennt nach Becken und Rinnen.

---

## 1. V19 (Frage 4.1)

| Messung [Befund] | Y | Ziel | Bewertung |
|---|---|---|---|
| unter Wasser | 0,067 (0,042–0,117) | ≤ 0,15 | erfüllt, eher dunkel |
| nasses Band | 0,063 | ≤ 0,25 | erfüllt |
| RGB unter Wasser | 0,078 / 0,065 / 0,051 | grau-nass ≈ 1,05 : 1 : 0,95 | noch warm (1,2 : 1 : 0,78) |

**Entscheidung:** V19 nicht bauen. Mit V19 fiele der Grund auf 0,04–0,05; das wäre fast schwarz.
- Den Warmton nimmt V18 mit `Entsaettigung_Nass` **0,35 → 0,5** weiter zurück (vorhandener Regler, 0 Knoten).
- Am Grund wird das R:B-Verhältnis damit etwa 1,1 : 0,88 [Ableitung, linear gemischt].
- Den Schalter für später dokumentieren: V19-Skript (50 Knoten, 0 Texturen) liegt fertig; `V19_Staerke` 0. Bauen nur, wenn ein anderes
  Tal (heller Kies, ohne Tönung) es braucht.

**Unsere Fehlannahme offen:** Seit Nachtrag 1 haben wir den Boden als Haupthebel behandelt (Ersetzung, Tönung, Lagen, V19). Für den
Boden stimmte das, und V18 hat es gelöst. Der verbleibende helle, milchige Eindruck auf Augenhöhe kommt von der **Wasseroberfläche**
(Abschnitt 2).

## 2. Wasseroberfläche (Frage 4.2)

### 2.1 Prüfung der Deutung

- **Fresnel bei flachem Blick** [Fach]: Reflexionsgrad von Wasser (n 1,33), unpolarisiert:
  - etwa 2 % senkrecht, 6 % bei 60°, 13 % bei 70°, 35 % bei 80° vom Lot.
  - Bei 1,7 m Augenhöhe liegt ein Punkt 5 m entfernt bei etwa 71°, 10 m entfernt bei etwa 80°.
  - **Weiter weg spiegelt Wasser also richtigerweise viel Himmel.** 2–4 m vor der Kamera (50–67°) sollte der Grund aber klar
    durchscheinen.
- **Was falsch aussieht** [Befund Bilder]: Auch die nahe Fläche ist hell und hat **Wirbelmuster**. Eine echte Spiegelung wäre ein
  klares, ruhig gebrochenes Bild von Himmel und Ufern.
- Mögliche Gründe:
  1. **Unser eigener ELD-Wirbel:** `ELD_Wirbel_Normal` 0,9, `ELD_Wirbel_Staerke` 0,85, `ELD_Wirbel_Groesse` 140,
     `ELD_Wirbel_Zug` 1,3 liegen **im Master** [Graph]. Der Name sagt Wirbel-Normalen; das passt genau zu „Wirbelmuster“
     [Ableitung].
  2. Zu viele Normal-Lagen zugleich: `Sim Velocity Normal Strength` 15, `Default Near Normal Strength` 0,25,
     `Default Distant Normal Strength` 0,3 / B 0,25, `WPO Flowmap` 6, `River Normal Flatness` 0,5. Sie liegen in Epics Funktionen,
     nicht im Master [Graph]; die genaue Wirkung ist nicht belegt.
  3. **Unscharfe Himmelsspiegelung** (Rauheit 0,04 plus Normalen): Ein heller, unscharfer Himmel liest sich als Milch.
  4. **Spiegelquelle:**
     - Laut Forum werden Lumen-Reflexionen für Single Layer Water erst ab 5.1 unterstützt [Forum, alt]. Ohne Lumen bzw. SSR
       spiegelt das Wasser den Sky-Light-Würfel statt der goldenen Ufer.
     - Laut Forum ist das Sonnenlicht im SLW-Glanz nicht verschattet [Forum]. Dann glänzt das Wasser auch im Schatten.

### 2.2 Testreihe (ergänzt Ferats A/B mit Rauheit und `Sim Velocity Normal Strength`)

Alle Werte in `MI_EL_SWR_Klar`, nicht speichern, Kameras t430/t500/t550 auf Augenhöhe, dazu einmal 2–4 m vor der Kamera.

| Nr | Was | Werte | Erwartung | Woran erkennbar |
|---|---|---|---|---|
| **D** Diagnose (5 min) | Spiegelquelle trennen | (a) Show-Flag *Specular* aus; (b) Sky Light Intensität 0 (bzw. Show-Flag *SkyLighting* aus); (c) Directional Light *Specular Scale* 0; (d) `r.Lumen.Reflections.Allow` 0 / 1 und `r.SSR.Quality` 0 / 3 [Namen unsicher; mit `DumpConsoleCommands Reflection` bzw. `DumpConsoleCommands SingleLayer` prüfen] | (a) ohne Milch = sicher Reflexion; (b) weg = Himmels-Würfel; (c) weg = Sonne; (d) ändert sich mit Lumen/SSR = Spiegelung aus der Szene | welche Stufe die Milch nimmt |
| **W1** ELD-Wirbel aus | eigener Teil | `ELD_Wirbel_Normal` 0,9 → **0**, `ELD_Wirbel_Staerke` 0,85 → **0**, `ELD_Schaum_Normal` 0,6 → **0** (Schaum ist ohnehin aus) | Wirbelmuster weg, die Fläche bleibt glänzend | gleiche Kamera, Wirbel ja/nein |
| **W2** ruhigere Normal-Lagen | Epic-Normalen außer der Sim-Normale (die testet Ferat) | `Default Near Normal Strength` 0,25 → **0,12**, `Default Distant Normal Strength` 0,3 → **0,15**, `…StrengthB` 0,25 → **0,12**, `River Normal Flatness` 0,5 → **0,8**, `WPO Flowmap` 6 → **3** | Ufer und Himmel werden als zusammenhängendes Spiegelbild erkennbar; Glanzpunkte bleiben, kleiner | Ränder der Spiegelung von Hang und Bäumen sichtbar |
| **W3** Fresnel später | Spiegelung erst bei flacherem Blick | `Water Fresnel Exponenth` 5 → **7**, `Water Fresnel Specular` 0,225 → **0,18** [Wirkung nicht belegt, im Dump nachsehen] | 2–6 m vor der Kamera klar und durchsichtig, Ferne spiegelt weiter, also nicht stumpf | Grund im Vordergrund sichtbar |
| **W4** Sonnenglanz | nur wenn D (c) die Milch nimmt | `Water Specular` 0,225 → **0,18**, `Anisotropy` 0,1 → **0** | weniger heller Streifen im Gegenlicht | t550 (Gegenlicht) |

- **Nicht empfohlen:**
  - Rauheit hoch (mattiert, macht stumpf; Ferats Grundsatz);
  - mehr Streuung (wirkt nach T0 kaum und würde trüben);
  - Sonnen-*Specular Scale* global senken (trifft alle Oberflächen).
- **Kombination nach dem Test:** W1 sicher. Dazu W2 oder W3, je nachdem was den Vordergrund klarer macht. Rauheit nach Ferats A/B;
  unsere Erwartung ist **0,02–0,03** (schärfer statt matter).
- **Parameter-Dump** (wenn W2/W3 unklar bleiben): Mit eurem Graph-Werkzeug die Ketten von `Water Roughness`, `Water Specular`,
  `Water Fresnel Roughness`, `Water Fresnel Specular`, `Water Fresnel  Exponenth`, `Default Near Normal Strength`,
  `River Normal Flatness`, `Sim Velocity Normal Strength`, `ELD_Wirbel_*` bis zum Ausgang ausgeben.
  - Die Epic-Parameter stecken in den Funktionen (`WaterTextureSurface`, `SetWaveAttributes`, `WaterRiverFlowmaps`), nicht im
    Master [Graph].

## 3. Trockener Kies 0,13 (Frage 4.3)

- **Einordnung:**
  - Unser Ziel 0,30–0,40 entsprach trockenem, hellem Kalk- und Granitkies.
  - Verwitterter, flechtiger Gebirgskies liegt eher bei 0,15–0,25.
  - Der gemessene Kies hat Y 0,129 und RGB 0,162/0,122/0,074, ist also deutlich orange.
- **Anteil der Tönung:**
  - Faktor (1,05; 0,86; 0,77) senkt Y um etwa 13 % und dreht den Ton nach Orange.
  - Ohne Tönung läge der Kies bei etwa Y 0,15 mit RGB ≈ 0,154/0,142/0,096 [Ableitung]. Der Rest ist die Textur selbst
    (`T_ground_big_pebbles_01` ist warm) und die Mischung mit Moos und Erde in der Klasse „Kies + Geröll ≥ 50 %“.
- **Entscheidung:** Ziel für dieses Tal **0,13–0,22**; der heutige Wert ist in Ordnung. **Nicht aufhellen**, sonst kommt der sandige
  Graben zurück.
  - Die Hänge bleiben golden: keine Änderung an der Tönung außerhalb des Wassers.
  - Optional (Nachtrag 2, Gestein-Option): Tönung nur auf Gesteinslagen halbieren. Das macht Kies und Geröll grauer (≈ 1,1 : 1 : 0,85)
    ohne die Hänge. Ferats Entscheidung, nicht nötig.

## 4. Bestätigungen und Regelanpassung

- **Gras-Fuß auf Schulterhöhe: bestätigt.** `h_ueber_spiegel_m` ist die Schulterhöhe. Die Mitte liegt 0,15–0,35 m vor der Schulter,
  der Fuß bleibt auf Schulterhöhe (begrenzt durch das Gelände), der Büschel hängt über die Kante. Das steht jetzt so in
  `bachbett_ufer_regeln.json` (`ueberhaengendes_gras.fuss`).
- **Ferats Ausschlussregeln: gut** (38 im Wasser, 37 + 32 überdeckt, 20 zu tief, 9 Lippe, 2 doppelt).
  - **Unser Fehler:** Wir haben die Lippenzone des Bachbetts (für Holz im Bett gedacht) auch fürs Ufer genannt. Als Band über
    d ≤ 2 m deckte sie bei Stufen alle 5–7 m 84 % der Talkaskade ab.
  - **Neu** `C_ufer.ausschluss_16h5`:
    - Steine im Hauptstrahl |s − s_Lippe| ≤ 0,75 m und d ≤ 0,5 m (Pflanzen an der Lippe erlaubt);
    - Pflanze im Wasser (Gelände < Spiegel − 2 cm);
    - Überdeckung mit Bachdekor-Felsen/Stämmen/Felsschalen (85 % der Hülle; Blöcke dürfen kleine Steine überdecken);
    - zu tief (Oberseite < 25 % der Höhe);
    - Auflage 60 % der Hülle.
  - Funktionen `stein_an_lippe` und `flacher_stein_erlaubt` in `ufer_regeln.py`.
- **Flache Steine:** Ferats 20 „zu tief“ lagen an 40–57°-Ufern. Neue Regel: flache Netze (Höhe < 0,35 × Länge) nur bis 35°.
  - Im Plan neu: `texndcpda_tier_0` 7 → 3, `SM_mountain_rock_small_01_3` 26 → 11, dafür rundere Netze. Summe gleich 1 730.
  - `ufer_plan_p2.py` 0 FEHLER, zwei Läufe byte-gleich; `ufer_regeln.py` Selbsttest 0 FEHLER.
- **Schutzabstand, 34 Zellen:**
  - Erwartet: Die C3-Bäche sind hier 8–10 m breit, die Regel ergibt halbe Breite + 12 m ≈ 16–17 m, also fast die bisherigen 15 m.
  - Das Kiesfeld ist damit wirklich Hochwasserbett der C3-Bäche und bleibt zu Recht.
  - Der Mündungsfächer (523 Zellen zurück auf Schotter) ist richtig.
- **Gras-Faktor doppelt:** Danke für das Finden und Beheben. Keine Aktion nötig.

## 5. Mündung

- **Ferats Umsetzung von Nachtrag 4 §3.2:** Punkt 0 bei dist 20 m (8,7 m unter dem p2-Wasser), 36,80 m, 6 m breit; Punkt 1
  36,78 m; Priorität p2 12 / C3 10. Die Kante ist weicher [Befund].
- Ist sie von oben noch zu ahnen: p2 noch 2–3 m weiter in C3 laufen lassen (bis dist ≈ 31 m). Dann liegt auch Punkt 1 unter p2.

**Export** (`ersetzt.json` → `lokaler_kopf`: s 20/31/38 m, 36,80/36,78/36,64 m, Breiten 6/11/14 m, Folgebreiten bestätigt):

| | Nachtrag 4 | **Nachtrag 5** |
|---|---|---|
| `F_ERLENBACH` | 599,7 m ab s 24 m, `576f7efc4372…`, 124 Objekte | **603,7 m ab s 20 m** (36,80 m, 6 m breit), **`ad5b1a2801f9…`**, 125 Objekte, Zelle 0,284 m |
| Zuflüsse `B_R2_K10_TUNDRA_02` / `_01` | s 124,52 / 168,86 | s 128,52 / 172,86 |
| übrige Fingerabdrücke | – | gleich (auch die beiden Tundra-Bäche) |
| Prüfer | 0 FEHLER | **0 FEHLER, 0 WARNUNG, 74 HINWEIS** („Kopf 20,00 m gekürzt“), zwei Läufe byte-gleich |

- **Neu backen:** nur `F_ERLENBACH`.
- Die Beispiele unter `antworten/fluss_sim/` (`F_ERLENBACH`, `zusammenfassung.json`, `wasserzonen.json`, `back_liste_auszug.json`)
  sind neu.
- **Overlap-Priorität:** Sie gehört **nicht** in die Back-Liste und nicht in die SWR-Vorgaben.
  - Der Export setzt sie schon: Hauptlauf `prioritaet_hauptlauf` 10, Zuflüsse darunter.
  - p2 ist nicht im Export. Seine 12 liegen immer über allen Export-Werten.
  - Vermerkt in `ersetzt.json` → `muendung_anschluss.overlap_material_priority` mit der Regel: Ersatz-Läufe lokal ≥ Hauptlauf + 2.

## 6. SWR-Tiefen (Talkaskade 0,47 m statt 0,69 m)

**Bewertung: kein Problem** [Ableitung]:
- Die Plan-Tiefe 0,69 m stammt aus dem Kasten-U-Profil. Nach dem Zurücklegen (C1) ist das Bett an 15 Querschnitten breiter;
  bei gleicher Zufuhr steht das Wasser flacher.
- Rate 0,3 füllt nur bis zur Spline nach. Band = Bett + 2 m lässt Wasser seitlich auslaufen (1 722 Zellen 1–8 m neben dem Bett).
- 0,47 m in der Mitte eines 3,9 m breiten Bachs mit 30 % Gefälle ist für Mittelwasser realistisch. Steile Kaskaden haben flache
  Rinnen und tiefere Becken.
- Kiesbett (0,53 = Plan) und Gesamt (0,54 zu 0,59) passen.

**Optionaler Test** (nur wenn die Becken flach wirken):
- Tiefe getrennt nach Becken (Plan-Tiefe ≥ 0,6) und Rinnen aus dem Dump. Ziel Becken ≥ 0,5 m.
- Wenn nicht: Rate 0,4 (16g F2) für p2 oder Becken der Talkaskade um 0,1–0,2 m vertiefen. Danach Reset + Bake.

## 7. Was lokal zu tun ist

Commit **`@@HASH@@`** holen.

1. `Entsaettigung_Nass` 0,5 (V18, beide Instanzen); V19 bleibt ungebaut.
2. Testreihe 2.2: zuerst D, dann W1 (ELD-Wirbel aus), W2/W3 neben euren A/B; W4 nur nach D (c).
3. Neue Ausschlussregeln und Regel für flache Steine sind im Plan: `ufer_p2/ufer_plan_p2.json` ist neu (flache Steine an steilen
   Ufern getauscht). Bei Gelegenheit neu einbauen.
4. fluss_sim lokal neu exportieren, `F_ERLENBACH` neu backen.

## Quellen

- Ferats Nachtrag 5 mit Messungen und Bildern (siehe Kopf), Graph-Dump des Masters.
- [Epic-Forum: Single Layer Water material does not seem to support UE5 Lumen Reflections](https://forums.unrealengine.com/t/single-layer-water-material-does-not-seem-to-support-ue5-lumen-reflections/244571)
  – Unterstützung ab 5.1 erwartet (Suchauszug, alt).
- [Epic-Forum: Directional Light not occluded in Single Layer Water material](https://forums.unrealengine.com/t/directional-light-not-occluded-in-single-layer-water-material/2232436)
  – Sonne im Wasserglanz unverschattet; Notlösung Specular Scale 0 (Suchauszug).
- [Epic-Forum: strange effects of water surfaces after enabling Lumen](https://forums.unrealengine.com/t/about-the-strange-effects-of-objects-and-water-surfaces-after-enabling-lumen/793171)
  (Suchauszug).
- Fresnel-Reflexion von Wasser (n 1,33): Lehrbuchwerte [Fach].

## Rückfragen

1. Ergebnis der Diagnose D: Welche Stufe nimmt die Milch?
2. Ferats A/B-Werte für Rauheit und Sim-Normale, damit ich W2/W3 darauf abstimme.
3. Falls W2/W3 nicht eindeutig wirken: der Ketten-Dump aus 2.2.
