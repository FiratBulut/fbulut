# Antwort zu Auftrag 14 – Nature Water FX an Wasserfällen und Bachstufen

Stand 11.10.2026. Plan maschinenlesbar in [`wasser_fx/plan.json`](wasser_fx/plan.json), erzeugt mit
[`wasser_fx/plan_erzeugen.py`](wasser_fx/plan_erzeugen.py) aus `vorlagen/daten/wasser_fx/*.json`. Geprüft wurde er mit
[`wasser_fx/plan_pruefen.py`](wasser_fx/plan_pruefen.py): **271 OK, 1 WARNUNG (Konflikt mit Auftrag 13, s. u.), 0 FEHLER**.
Kennzeichnung: **[ungeprüft]** = nirgends belegt, im Editor nachsehen. **[Annahme]** = Wert, mit dem ich bis zur Prüfung rechne.
**[Ableitung]** = aus Daten oder früherer Recherche gefolgert.

## Kurzfazit

- **Die Vorhänge bleiben überall, Nature Water FX ergänzt sie nur.** Zwei harte Gründe: Die Epic-Flussstücke haben an jeder C2-Kante
  eine Lücke von 1,3–3 m, und die schließt nur der Vorhang. Außerdem endet Niagara je nach System bei 30–150 m (Cull). Jenseits
  davon muss der Vorhang allein tragen. `NS_Waterfall_Small` ersetzt den Stufen-Vorhang deshalb nicht. Er läuft als Strähnen-Akzent
  über dem Vorhang, zuerst als Probe an C2 S01.
- **Große Fälle WF_K1 und WF_K8:** je das Trio des Herstellers, `NS_Waterfall_Large` an der Lippe, `NS_Impact_Large` an `gischt`
  und `NS_Wake_Large` auf dem Becken (3 von 3). Dazu weniger und dunklerer Schaum im Vorhang (`MI_EL_Wasserfall`), weil das Weiß
  am Fuß jetzt aus der Gischt kommt.
- **C2 (12 Stufen auf 140 m):** 10 Systeme in 5 Stufengruppen mit je ≤ 3 Systemen. Abwechselnd Impact und Stream, `NS_Waterfall_Small`
  nur an den zwei großen Stufen S01 und S07 (S07 optional). Kurze Cull-Distanzen (30/45 m) halten die Zahl gleichzeitig aktiver
  Systeme an jedem Standort am Bach bei **≤ 6** (geprüft an ~590 Betrachterpunkten). S02, S06, S08 und S10 bekommen kein System,
  dort bleiben Vorhang und Schaumscheibe.
- **H4 (2 Schnellen):** je `NS_Stream_Medium`, optional `NS_Wake_Small` im Kehrwasser unter S01. Die Schnellen-Haut bleibt ausgeblendet.
- **Material:** Gegen die „weißen Kacheln" hilft am Stufen-Vorhang: Schaum runter (0,45 → 0,3), Strähnen und Randdurchsicht rauf,
  Deckkraft 0,5, `Schaum_Leuchten` 0. Ein MI gilt für das ganze C2-Netz, einzelne Stufen lassen sich nicht getrennt einstellen.
- **Klang:** Nur `CUE_Water_Stream_I…X` (City_Nature_Sounds) sind im Inventar, ein echtes Wasserfall-Tosen fehlt (Lücke). Geplant
  sind 11 Klang-Orte mit unterschiedlichen Cues nebeneinander.
- **Konflikt gefunden:** Der Tundra-Planer (Auftrag 13) setzt `tundra_06_das_aufeis` mitten auf die C2-Kaskade. Sein
  `NS_Stream_Small` liegt **1,3 m** neben unserem S07-Aufprall, sein neuer „quellbach" auf dem Erlenbach. Das braucht eine Entscheidung (Rückfrage 1).
- **Ungeprüft:** die Namen der User-Parameter, die Größe der Systeme bei Skala 1, die lokale Fließachse und die Sim-Targets der Systeme.
  Alles dafür steht als Prüfliste am Ende. Die Skalen sind so gewählt, dass zu hoch fallende Partikel unschädlich sind: Unter dem
  Wasserspiegel zeichnet UE 5.8 Translucent ohnehin nicht.

---

## 1. Was über Nature Water FX bekannt ist

| Punkt | Befund | Beleg |
|---|---|---|
| Anbieter, Preis | SHOGUN GAMES, Fab „From $44.99", 5,0 (2 Bewertungen) | Fab-Kategorie Liquid (Suchauszug) |
| Inhalt | Fountain ×5, Geyser ×3, Stream ×3, Waterfall ×3; „The water impact and surface wakes are separate Niagara systems" | Fab-Listing (Suchauszug) |
| Zahl | 20 Niagara-Systeme, 7 Emitter, 6 Materialien, 11 Texturen; deckt sich mit unserem Inventar (20 × `/Game/NatureWaterFX/FX/NS_*`) | Marketplace-Seite (Suchauszug) + `inventar_extra.json` |
| Emitter | „GPU and CPU": gemischt, je System unbekannt | Marketplace (Suchauszug) |
| User-Parameter | „All Niagara FX systems have User controlled variables for Customization of each individual part of the effect". **Namen nicht veröffentlicht.** | Fab-Listing (Suchauszug) |
| Verhalten | „optimized", „loop continuously"; das Demovideo nutzt die Rural-Australia-Umgebung (nicht enthalten) | Fab-Listing (Suchauszug) |
| Engine | 4.27 und 5.x laut Händlerseiten, 5.8 nicht belegt; das Paket läuft bei Ferat in 5.8.3 | [ungeprüft] |
| Größen, Bounds, LOD, Sound | nirgends angegeben | [ungeprüft] |

Fab, docs.unrealengine.com und unrealengine.com waren per WebFetch nicht erreichbar (DNS). Alles oben stammt aus Suchauszügen.
Drittseiten mit Paket-Downloads habe ich bewusst weder genutzt noch verlinkt.

**Annahmen für die Skala [Annahme, ungeprüft]**, Größe bei Skala 1 (in `plan.json → einstellungen_alle.skala_annahme_m`):

| System | Small | Medium | Large |
|---|---|---|---|
| Waterfall (Breite × Höhe) | 3 × 5 m | 6 × 15 m | 12 × 30 m |
| Impact / Wake (Ø) | 3 m | 6 m | 12 m |
| Stream (Breite × Länge) | 2 × 5 m | 4 × 10 m | 8 × 20 m |

Regel: `skala = Zielmaß / gemessenes Maß`. Gemessen wird das System im Editor (Fixed Bounds oder sichtbare Breite). Die Höhe eines
Falls bestimmen Schwerkraft und Lebensdauer, nicht die Skala. Bei 57 m Fall braucht ein Partikel ≈ 3,4 s (Physik). Ist die
Lebensdauer kürzer, endet der Strahl vorher. Das ist kein Fehler, denn der Vorhang trägt weiter. Wer es länger will, nimmt einen
User-Parameter für Lebensdauer oder Spawn-Höhe, falls es einen gibt.

## 2. Konventionen im Plan

- **Ort** in Welt-cm. **Drehung** wie in der Bergwald-Klamm (`sehens_lib/rezept.py`, `q_yaw_kompass`): Die lokale +X-Achse des
  Systems zeigt in Fließrichtung. `rot_q = [x, y, z, w]` (reine Z-Drehung), dazu `yaw_ue_grad` (Unreal-Rotator) und `kompass_grad`
  (0 = Nord = −Y). **Falls das Paket lokal +Y als Fließrichtung nutzt**, setzt man `einstellungen_alle.yaw_korrektur_grad` einmal
  für alle auf −90 [ungeprüft, ein Blick im Niagara-Editor reicht].
- **Herleitung der Orte:**
  - Kante C2 = vorletzter Punkt des oberen Flussstücks. Das Stück endet laut `stufen_fluss_teile.json` 0,5 m hinter der Kante, das
    passt zu `kante_s_m` (S01: 2,59 m nach der Lippe).
  - Aufprall C2 = `gischt_cm` (x, y), z = Spiegel des unteren Flussstücks + 10 cm. Die Gischt liegt 0,2–0,6 m hinter dem Fußpunkt.
  - Große Fälle: Lippe aus `lippe`, Gischt aus `gischt`, z = Beckenspiegel + 10 cm.
- Für **alle** Systeme: GPU (CPU-Emitter des Pakets nicht umbauen, nur messen), Cast Shadow **aus**, Translucency Sort Priority **2**
  (Vorhang 0, Schaum 1), Max Draw Distance = `cull_m` × 100, HLOD aus.

## 3. Große Fälle

### WF_K1 – Wasserfall West (B4)

Daten: Lippe (−311 731, −62 444), Spiegel 263,41 m, 14,9 m breit, Fall 56,9 m, Richtung (0,753, 0,658). Fuß (−310 794, −61 624).
Gischt (−310 606, −61 459, 20 804). Becken 20 654 cm, 1 321 m². **Nur 14 von 27 Vorhangspalten treffen das Becken**, die linken
13 setzen auf Gelände auf (213 m).

| System | Ort (cm) | Yaw / Kompass | rot_q | Skala | Cull | Bezug |
|---|---|---|---|---|---|---|
| `/Game/NatureWaterFX/FX/NS_Waterfall_Large` | −311 708, −62 424, 26 346 | 41,1° / 131,1° | 0, 0, 0,35142, 0,93622 | 1,24 | 150 m | Lippe + 0,3 m, Spiegel + 5 cm |
| `/Game/NatureWaterFX/FX/NS_Impact_Large` | −310 606, −61 459, 20 664 | 41,1° | dto. | 0,67 | 100 m | gischt, Becken + 10 cm |
| `/Game/NatureWaterFX/FX/NS_Wake_Large` | −310 229, −61 130, 20 657 | 41,1° | dto. | 1,0 | 60 m | gischt + 5 m, Becken + 3 cm |

- Skala Fall = 14,9 m / 12 m. Skala Impact = 8 m Ziel-Ø / 12 m. Ziel ist die Beckenhälfte (7,7 m nass), sonst zerstäubt Gischt über
  trockenem Fels.
- **User-Parameter (Wunsch, Namen [ungeprüft]):** Tint (0,82, 0,86, 0,88), Breite 14,9 m, Lebensdauer so lang, dass ≥ 55 m Fall
  erreicht werden. Am Impact: Nebelhöhe 8–12 m.
- **Klang:** `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_IX_Cue` an der Gischt (+1,5 m), Radius 90 m, Lautstärke 1,0.
  `CUE_Water_Stream_IV_Cue` an der Lippe, Radius 35 m, 0,6. **Lücke:** tiefes Tosen eines 57-m-Falls.

### WF_K8 – Elfenfall (H4)

Daten: Lippe (313 631, −71 477), Spiegel 181,59 m, 16,6 m breit, Fall 53,9 m, Richtung (−0,835, 0,551). Alle 27 Spalten treffen das
Becken (12 770 cm, 1 851 m²). Bild `WASSER3_H4_*`: Der Vorhang brennt in der Sonne weiß aus, der Fuß ist eine harte Linie ohne Gischt.

| System | Ort (cm) | Yaw / Kompass | rot_q | Skala | Cull | Bezug |
|---|---|---|---|---|---|---|
| `/Game/NatureWaterFX/FX/NS_Waterfall_Large` | 313 606, −71 460, 18 164 | 146,6° / 236,6° | 0, 0, 0,95777, 0,28753 | 1,38 | 150 m | Lippe + 0,3 m, Spiegel + 5 cm |
| `/Game/NatureWaterFX/FX/NS_Impact_Large` | 312 458, −70 702, 12 780 | 146,6° | dto. | 1,33 | 100 m | gischt, Becken + 10 cm |
| `/Game/NatureWaterFX/FX/NS_Wake_Large` | 312 041, −70 427, 12 773 | 146,6° | dto. | 1,0 | 60 m | gischt + 5 m, Becken + 3 cm |

- Tint etwas dunkler (0,74, 0,79, 0,81) gegen das Ausbrennen. Impact-Ziel-Ø 16 m (volle Breite).
- **Klang:** wie K1 (`IX` an der Gischt 90 m / 1,0; `IV` an der Lippe 35 m / 0,6). K1 und K8 liegen 6,3 km auseinander, es gibt also
  keine Doppelung.

**Cull bei den großen Fällen:** Antwort 12 empfiehlt für Gischt 40–60 m. Für die zwei Heldenfälle weiche ich begründet ab, sie werden
aus 100–200 m gesehen (Bilder `_weit`). Fall 150 m, Impact 100 m, Wake 60 m. Kosten: höchstens 6 Systeme weltweit, auf die Distanz
mit kleiner Bildfläche [Ableitung]. Ist die GPU-Zeit zu hoch (Prüfliste), geht der Fall auf 100 m und der Impact auf 60 m.

**Empfehlung Vorhang (groß):** **bleibt, NS ergänzt.** Der Vorhang ist die Form, NS bringt Bewegung, Strähnen vor dem Netz und den
Aufprall. Die Aufprall-Scheibe (`MI_EL_Wasserfall_Aufprall`) bleibt für die Ferne jenseits von 100 m, nur leiser.

## 4. Bachstufen C2 – F_ERLENBACH_1V_C2 (12 Stufen)

### Bestand je Stufe (aus den JSON-Daten)

| Stufe | Art | Fall gesamt / am Vorhang | Breite Kante | Kante (x, y, z cm) | gischt_cm | Yaw | s (m) | NS geplant |
|---|---|---|---|---|---|---|---|---|
| S00 | Schnelle | 3,26 m auf 10,6 m | 12,9 m (nass) | – | – | 112,4° | 22–32 | Stream_Medium |
| S01 | Fall | 4,09 / 3,26 m | 7,9 m | −174 222, −234 292, 8 802 | −174 382, −233 915, 8 517 | 112,6° | 55,2 | **Waterfall_Small + Impact_Small** |
| S02 | Fall | 3,22 / 3,22 m | 8,2 m | −174 584, −233 556, 8 401 | −174 790, −233 215, 8 124 | 121,1° | 63,5 | – (8 m neben S01) |
| S03 | Fall | 3,36 / 2,44 m | 8,2 m | −175 742, −231 104, 7 575 | −175 865, −230 822, 7 375 | 113,3° | 90,8 | Impact_Small |
| S04 | Fall | 2,18 / 2,18 m | 8,2 m | −176 043, −230 446, 7 275 | −176 174, −230 197, 7 104 | 117,8° | 98,0 | Stream_Small an der Lippe |
| S05 | Fall | 2,29 / 2,29 m | 8,2 m | −176 360, −229 853, 7 007 | −176 494, −229 589, 6 820 | 116,9° | 104,8 | Impact_Small |
| S06 | Fall | 2,07 / 2,07 m | 8,2 m | −176 681, −229 203, 6 701 | −176 798, −228 948, 6 541 | 114,7° | 112,0 | – |
| S07 | Fall | 5,33 / 2,14 m | 8,2 m | −177 259, −227 604, 6 111 | −177 297, −227 338, 5 936 | 98,0° | 129,1 | **Waterfall_Small (opt.) + Impact_Small** |
| S08 | Fall | 2,03 / 2,03 m | 8,4 m | −177 419, −226 906, 5 818 | −177 565, −226 681, 5 654 | 123,3° | 136,3 | – |
| S09 | Fall | 1,84 / 1,84 m | 8,4 m | −177 822, −226 360, 5 550 | −177 959, −226 124, 5 413 | 119,9° | 143,1 | Impact_Small |
| S10 | Fall | 1,95 / 1,95 m | 8,7 m | −178 080, −225 703, 5 311 | −178 126, −225 411, 5 162 | 99,0° | 150,2 | – |
| S11 | Schnelle | 1,62 m auf 4,7 m | 7,1 m (nass) | – | – | 89,1° | 157–162 | Stream_Small |

### Plan (alle Pfade `/Game/NatureWaterFX/FX/…`, Sort 2, kein Schatten)

| Gruppe | Ziel | System | Ort (cm) | Yaw | rot_q (z, w) | Skala | Cull | Bezug | opt. |
|---|---|---|---|---|---|---|---|---|---|
| C2_A | S00 | `NS_Stream_Medium` | −173 192, −236 898, 9 584 | 112,4° | 0,83094, 0,55636 | 1,24 | 45 m | Mitte Lippe–Fuß, Spiegel + 10 cm | nein |
| C2_B | S01 | `NS_Waterfall_Small` | −174 230, −234 273, 8 807 | 112,6° | 0,83198, 0,55481 | 1,0 | 45 m | Kante + 0,2 m, Spiegel + 5 cm | nein (Probe) |
| C2_B | S01 | `NS_Impact_Small` | −174 382, −233 915, 8 486 | 112,6° | 0,83198, 0,55481 | 1,0 | 30 m | gischt_cm, Spiegel unten + 10 cm | nein |
| C2_C | S03 | `NS_Impact_Small` | −175 865, −230 822, 7 341 | 113,3° | 0,83536, 0,54971 | 1,0 | 30 m | gischt_cm | nein |
| C2_C | S04 | `NS_Stream_Small` | −175 996, −230 534, 7 285 | 117,8° | 0,85628, 0,51650 | 1,0 | 30 m | 1 m stromauf der Kante | nein |
| C2_C | S05 | `NS_Impact_Small` | −176 494, −229 589, 6 788 | 116,9° | 0,85210, 0,52337 | 1,0 | 30 m | gischt_cm | nein |
| C2_D | S07 | `NS_Waterfall_Small` | −177 261, −227 584, 6 116 | 98,0° | 0,75463, 0,65615 | 1,0 | 45 m | Kante + 0,2 m | **ja** |
| C2_D | S07 | `NS_Impact_Small` | −177 297, −227 338, 5 907 | 98,0° | 0,75463, 0,65615 | 1,0 | 30 m | gischt_cm | nein |
| C2_E | S09 | `NS_Impact_Small` | −177 959, −226 124, 5 373 | 119,9° | 0,86572, 0,50053 | 1,0 | 30 m | gischt_cm | nein |
| C2_E | S11 | `NS_Stream_Small` | −178 159, −224 754, 4 990 | 89,1° | 0,70148, 0,71269 | 1,29 | 30 m | Mitte Lippe–Fuß | nein |

`rot_q` ist immer `[0, 0, z, w]`.

- **Skala:**
  - `NS_Waterfall_Small` bleibt bei 1,0: ein ~3 m breiter Mittelstrang [Annahme] auf dem 8,2-m-Vorhang. Ist das System höher als
    die 2,1–3,3 m Fall, verschwindet der Rest unter dem Spiegel.
  - Schnellen: `min(Breite/Ref, Länge/Ref)`, damit das System nicht über die Schnelle hinausschießt.
- **User-Parameter (Wunsch, Namen [ungeprüft]):** Tint (0,80, 0,84, 0,86), Spawnrate 0,6–0,8 × Standard (dichte Kaskade).
- **Bündelung und Budget:**
  - 5 Gruppen mit je ≤ 3 Systemen, C2 gesamt 10 (9 Pflicht + S07-Fall optional).
  - Abwechselnd Impact und Stream (S03 I – S04 S – S05 I), ein Fall nur an S01 (zweithöchste Kante am Vorhang, 3,26 m) und S07
    (größte Stufe insgesamt, 5,33 m).
  - Weil die Stufen 7–8 m auseinander liegen, zählt das Prüfskript für ~590 Betrachterpunkte (Augenhöhe über jedem Flusspunkt und
    8 m seitlich) die Systeme innerhalb ihrer Cull-Distanz: **höchstens 6 gleichzeitig**, also höchstens zwei Gruppen.
  - Dafür liegt der Cull von Small-Impact und Small-Stream bei 30 m (statt 35–40). S02 (3,22 m) habe ich bewusst ausgelassen: mit S02
    waren es im ersten Lauf 7 an einer Stelle.
- **Klang** (Radius 25–30 m, verschiedene Cues gegen Phasing):

  | Gruppe | Cue | Ort | Lautstärke |
  |---|---|---|---|
  | C2_A | `CUE_Water_Stream_II_Cue` | S00 | 0,5 |
  | C2_B | `CUE_Water_Stream_VIII_Cue` | S01-Gischt | 0,7 |
  | C2_C | `CUE_Water_Stream_X_Cue` | S04 | 0,7 |
  | C2_D | `CUE_Water_Stream_V_Cue` | S07 | 0,7 |
  | C2_E | `CUE_Water_Stream_I_Cue` | S10 | 0,5 |

  Was die Cues I–X klingen, habe ich nicht gehört [ungeprüft]. Die Zuordnung folgt der Lesart der A13-Planer (I = Rieseln,
  IX = Fallrauschen …).

**Empfehlung Vorhang (Stufen): bleibt, wird ruhiger, NS ergänzt nah.**
- `NS_Waterfall_Small` kann den Vorhang nicht ersetzen. Ohne Vorhang klafft an jeder Kante die 1,3–3-m-Lücke zwischen den
  Flussstücken. Jenseits von 45 m wäre die Stufe leer, und ein 3-m-System deckt keine 8 m Breite.
- Die weißen Kacheln (Bilder `STUFEN1_*`) kommen von gleichmäßigem Schaum über die ganze Fläche und harten Seitenrändern. Das löst
  das Material (Abschnitt 6), nicht Niagara.
- Überzeugt die Probe an S01, geht der Vorhang global weiter zurück (`falls_probe_S01_gut`: Deckkraft 0,4, Schaum 0,2) und S07
  bekommt seinen Fall.

## 5. H4 – F_ELFENFLUSS_2_H4 (2 Schnellen)

| Gruppe | Ziel | System | Ort (cm) | Yaw / Kompass | rot_q (z, w) | Skala | Cull | opt. |
|---|---|---|---|---|---|---|---|---|
| H4_A | S00 (1,62 m auf 5 m, 9,8 m nass) | `/Game/NatureWaterFX/FX/NS_Stream_Medium` | 285 018, −61 052, 9 550 | 145,5° / 235,5° | 0,95496, 0,29672 | 0,69 | 45 m | nein |
| H4_A | S01 (4,15 m auf 10 m, 8,7 m nass) | `/Game/NatureWaterFX/FX/NS_Stream_Medium` | 281 998, −59 946, 8 814 | 178,4° / 268,4° | 0,99991, 0,01356 | 1,18 | 45 m | nein |
| H4_A | S01 Kehrwasser | `/Game/NatureWaterFX/FX/NS_Wake_Small` | 281 352, −59 929, 8 599 | 178,4° | 0,99991, 0,01356 | 1,0 | 30 m | ja |

- Ort: Mitte Lippe–Fuß, Spiegel + 10 cm (Wake: Fuß + 1,5 m, + 3 cm). Die Schnellen-Haut (`MI_EL_Stufenfall_Schnelle`) bleibt
  ausgeblendet, `NS_Stream_Medium` ersetzt sie. Die Schaumscheibe bleibt.
- **Klang:** `CUE_Water_Stream_VI_Cue` an S00 und `CUE_Water_Stream_VII_Cue` an S01, je Radius 35 m, Lautstärke 0,7.
- Die H4-Schnellen liegen ~300–340 m vom Elfenfall WF_K8 entfernt, außerhalb jeder Cull-Distanz. Es gibt also keine gemeinsame Sichtgruppe.

## 6. Materialwerte (`plan.json → material`, nur Parameter aus `material_parameter.json`, Master `M_EL_Wasserfall2`)

Die Ist-Werte der Instanzen stehen nicht in `material_parameter.json` (dort nur Master-Standard). Die Zuordnung „Deckkraft 0,55/0,45,
Schaum 0,45/0,55" lese ich als Vorhang/Schaumscheibe [Annahme].

| MI | Gilt für | Empfehlung | Grund |
|---|---|---|---|
| `MI_EL_Wasserfall` | WF_K1, WF_K8 (Vorhang) | `Schaum_Menge` 0,9 · `Straehnen_Staerke` 0,8 · `Schaum_Leuchten` 0,0 · `Rand_Durchsicht` 0,8 · `Deckkraft` 0,9 · `Tiefenblende_cm` 60 · `Schaumfarbe` (0,80, 0,84, 0,86, 1) · `Wasserfarbe` (0,14, 0,22, 0,24, 1) | K8 brennt aus, K1 wirkt flach; das Weiß am Fuß kommt jetzt von NS |
| `MI_EL_Wasserfall_Aufprall` | Aufprall-Scheiben K1/K8 | `Deckkraft` 0,6 · `Schaum_Menge` 1,0 · `Schaum_Leuchten` 0,0 · `Tiefenblende_cm` 40 | bleibt für die Ferne, nah trägt `NS_Impact_Large` |
| `MI_EL_Stufenfall_Vorhang` | C2 S01–S10 (ein Netz) | `Deckkraft` 0,55 → **0,5** · `Schaum_Menge` 0,45 → **0,3** · `Straehnen_Staerke` 0,85 · `Rand_Durchsicht` 0,85 · `Schaum_Leuchten` 0,0 · `Tiefenblende_cm` 30 · `Schaumfarbe` (0,80, 0,84, 0,85, 1) · `Wasserfarbe` (0,12, 0,20, 0,21, 1) | gegen weiße Kacheln: Struktur statt Fläche, weiche Ränder. Tiefenblende 30 statt 60, weil der Vorhang nur 0,5–0,8 m vor dem Bett liegt (Median) und 60 cm ihn sonst großflächig ausblenden [Ableitung] |
| `MI_EL_Stufenfall_Schaum` | Schaumscheiben C2 + H4 | `Deckkraft` 0,45 → **0,4** · `Schaum_Menge` 0,55 → **0,5** · `Schaum_Leuchten` 0,0 · `Tiefenblende_cm` 20 · `Schaumfarbe` (0,82, 0,86, 0,87, 1) | bleibt an allen Stufen, auch ohne Impact |
| `MI_EL_Stufenfall_Schnelle` | C2-Schnellen-Haut, H4 ausgeblendet | keine Änderung | |

Stufenweise unterschiedliche Werte gehen nicht, weil ein Vorhang-Netz alle C2-Stufen trägt. Bräuchte man es doch, wäre das ein neuer
Vertex-Farbkanal und damit ein neuer Bau, also nicht jetzt.

## 7. Leistung

- **Cull:** Effect Types `cull_by_distance` + `max_distance` (Epic-API). Vorschlag (neue Assets, Namen frei):
  - `NET_EL_Wasser_Held`: Max Distance 150 m, für K1/K8.
  - `NET_EL_Wasser_Nah`: 50 m, für die Bachstufen.
  - Zusätzlich je Komponente Max Draw Distance = `cull_m`.
  - Die Effect Type hält die Simulation an, der Draw-Cull nur das Zeichnen [Ableitung].
- **Scalability:** In der Effect Type je Qualitätsstufe „Low/Medium" die Spawnrate auf 0,5 setzen, „High/Epic" auf 1,0. Max Instances
  je Typ: Held 6, Nah 12. Mit Significance-Handler „Distance" werden bei Überzahl die fernsten gekürzt (Epic-API: ohne Handler gilt
  die Grenze nur beim Spawnen).
- **GPU:**
  - GPU-Sim braucht feste Bounds (Antwort 12). Je System prüfen, ob „Fixed Bounds" gesetzt ist, sonst setzen: Fall ≥ Breite ×
    Fallhöhe, Impact ≥ 2 × Ø.
  - CPU-Emitter des Pakets zuerst messen, nicht blind umstellen.
- **Kein Schatten** (bewegte Schattenwerfer invalidieren VSM-Seiten jedes Frame, Antwort 12).
- **Pool:** nicht nötig. Die Systeme sind fest gesetzte NiagaraActor (World Partition lädt sie mit dem Feld). Ein Pool
  (`PoolingMethod` AutoRelease) lohnt nur für Laufzeit-Spawns.
- **Gleichzeitig aktiv:** C2/H4 ≤ 6 (geprüft), große Fälle 3 je Fall. Grobes Messziel für alle Wasser-FX im Bild: ≤ 0,5 ms GPU
  (`stat Niagara`, `profilegpu`) [Ableitung]. Sonst Reihenfolge: optionale weg (S07-Fall, H4-Wake), dann Cull −25 %, dann Spawnrate.
- **Unter Wasser:** Translucent wird unter der SLW-Oberfläche nicht gezeichnet (5.8, Antwort 12). Darum sitzen alle Pivots 3–10 cm
  über dem Spiegel. Teile, die in den Spiegel tauchen, fallen sauber weg.

## 8. Auftrag 13 – Geysir- und Quellorte (nur Übersicht, `plan.json → sehens13`)

**Nicht doppelt setzen:** Diese Effekte liefern die Sehenswürdigkeiten-Planer mit ihrer `orte.json` selbst. Übernommen ist nur, was
dort steht: Phase-2-Läufe im Scratchpad, Stand 11.10. 14:05–14:36, 26 Orte mit NatureWaterFX, alle ≤ 3 Niagara. „Der Atem" ist
gestrichen.

| Ort | NatureWaterFX-Systeme |
|---|---|
| **kueste_08 Das Blasloch** (H2) | `NS_Geyser_Large` (318 500, −238 500, −32), `NS_Impact_Medium` |
| **aue_07 Blautopf** (F4) | `NS_Wake_Small` (116 700, −82 300, 1 941) |
| **kueste_04 Der Seefall** (A5) | `NS_Waterfall_Large`, `NS_Impact_Large`, `NS_Stream_Small` (optional) |
| frost_06 Die Eisküste | 2 × `NS_Geyser_Small` (Skala 0,6/0,45), `NS_Impact_Small` |
| dschungel_02 Turmquelle | `NS_Waterfall_Large`, `NS_Impact_Large`, `NS_Stream_Small` |
| wueste_04 Quelloase | `NS_Stream_Small` |
| Weitere Fälle, Klammen und Bäche | bergwald_05/06, canyon_04/07, dschungel_06/08, elfenwald_04/05/08, frost_01/08, gletscher_01/05/06, heide_06, kueste_01/03, aue_01/04 |
| tundra_06 Das Aufeis | `NS_Stream_Small` (**Konflikt**, s. u.) |

Alle A13-Effekte liegen ≥ 640 m von unseren entfernt, **außer tundra_06**: Dessen `NS_Stream_Small` (−177 200, −227 300, 5 836)
liegt 1,3 m neben unserem C2-S07-Aufprall. Sein „quellbach" beginnt am Fuß von S07 und läuft quer zum Erlenbach 11 m nach Westen
(Spiegel 58,1 m, 0,9 m unter dem Becken unter S07), und der Ort
(Mitte −176 000, −223 500, r 55 m, „70 m lange, gestufte Eisdecke") überdeckt die untere C2-Kaskade S07–S11. In `plan.json` steht
das als `konflikt`. Unser Plan behält den Platz; Entscheidung siehe Rückfrage 1.

Für A13-Effekte gelten sinngemäß dieselben Einstellungen (GPU, kein Schatten, Sort 2, Cull nach Klasse aus Abschnitt 7). Die Planer
schreiben keine Cull-Werte, das setzt der Setzer.

## 9. Prüfliste für Ferat bzw. Claude lokal (einmal, ~15 min)

1. Ein `NS_Waterfall_Small`, `NS_Impact_Small` und `NS_Stream_Small` in eine leere Szene setzen. Notieren:
   - lokale Fließachse (+X oder +Y?) → `yaw_korrektur_grad`
   - Größe bei Skala 1 → `skala_annahme_m`, danach `plan_erzeugen.py` neu laufen lassen
2. Im Niagara-Editor die **User-Parameter** jedes verwendeten Systems ablesen (Namen, Typ, Standard) und in `user_parameter.wunsch`
   eintragen: Tint, Spawnrate, Breite, Lebensdauer.
3. System-Eigenschaften: Sim Target je Emitter (GPU/CPU), Fixed Bounds, Scalability/Effect Type, Cast Shadow.
4. Probe an C2 S01 (Fall + Impact) mit den neuen Stufen-Vorhang-Werten aus `PIE` oder Highres. Erst danach S07-Fall und die
   `falls_probe_S01_gut`-Werte.
5. `stat Niagara` und `profilegpu` an K8 (Blick wie `WASSER3_H4_WF_K8_weit`) und an C2 S03 (Mitte der Kaskade).
6. Die Cues I–X einmal anhören und die Zuordnung (Rieseln/Rauschen/Tosen) bestätigen. Die Inventarliste zeigt nur 40 von 46 Cues
   und 40 von 316 SoundWaves. Weitere Wasserklänge sind also möglich und sollten aufgelistet werden.

## Quellen

- Nature Water FX (alle Auszüge, Seiten nicht abrufbar):
  - [Fab-Listing](https://www.fab.com/listings/c34e8871-3585-4381-b21f-1b895814472b)
  - [Fab VFX Liquid](https://www.fab.com/category/vfx/liquid)
  - [Marketplace (EN)](https://www.unrealengine.com/marketplace/en-US/product/nature-water-fx)
  - [Marketplace (JA)](https://docs.unrealengine.com/marketplace/ja/product/nature-water-fx)
- Niagara Effect Type und Scalability (Epic-API):
  - [UNiagaraEffectType](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/Niagara/UNiagaraEffectType)
  - [NiagaraSystemScalabilitySettings (Python-API)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/NiagaraSystemScalabilitySettings)
- Projektintern:
  - `antworten/12-recherche-wasser-gpu-schatten.md` Teil A: Translucent unter Wasser, Cull 40–60 m, kein Schatten, Sort 0/1/2
  - `vorlagen/SEHENS_FORMAT.md` §6
  - `vorlagen/daten/material_parameter.json`
  - `vorlagen/daten/inventar_extra.json`
  - `antworten/skripte/sehens_lib/rezept.py` + `instanzen.py` (`q_yaw_kompass`)
  - `antworten/skripte/sehens_bergwald/` (Klamm-Vorbild)

## Rückfragen

1. **tundra_06 „Das Aufeis" liegt auf der C2-Kaskade.** Eisdecke im Sommer auf einem Bach, den wir gerade mit 10 Wasser-FX beleben?
   Vorschlag: Den Ort durch den Tundra-Planer verlegen (oder seinen `quellbach` und `NS_Stream_Small` streichen). Dieser Plan bleibt
   unverändert. Wer entscheidet?
2. **Cull der Heldenfälle 150/100 m** statt 40–60 m. Einverstanden, oder lieber erst messen und dann freigeben?
3. **S02 ohne Niagara** (3,22 m, zweithöchste Kante) wegen des Budgets ≤ 6 gleichzeitig. Ist das Budget weich genug für einen
   7. Impact an S02?
4. Soll ein Wasserfall-Klangpaket (Tosen, Gischt) auf die Download-Liste? Im Inventar gibt es nur Bach-Cues.

## Nachtrag Koordinator (Konflikt tundra_06)

Entschieden: **Die C2-Kaskade hat Vorrang.** `tundra_06_das_aufeis` (Auftrag 13) wird verlegt, mindestens 60 m von allen Stufen- und Gischtpunkten entfernt. Bis zur Verlegung bitte die tundra_06-Effekte aus dem Sehenswürdigkeiten-Plan **nicht** setzen; `plan.json` dieses Auftrags gilt unverändert. Den neuen Standort trägt `sehens-STATUS.md` nach.
