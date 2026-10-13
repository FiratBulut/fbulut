# 16h Nachtrag 6 – Diagnose D, Varianten W1–W3, Rural-Australia-Wasser, Plugin „Water Dynamics“ (13.10.2026, 19:10)

Bezug: eure Antwort `antworten/16h-nachtrag5-ufer-c2-c4-lagen.md` (3452dbc) §2.2 und Rückfragen 1–3, unser Nachtrag 5b (A/B G0–G4).

## 1. Erledigt aus eurer Liste (§7)

- `Entsaettigung_Nass` 0,35 → **0,5** an beiden Instanzen (V12/V12s), gespeichert. V19 bleibt ungebaut.
- Diagnose D und Varianten W1–W3 nach §2.2, nur im Speicher, danach alles zurück. Kameras t430/t500/t550 auf Augenhöhe.
- Neuer Uferplan (flache Steine nur bis 35°): noch nicht eingebaut, kommt mit dem nächsten Bau.

## 2. Diagnose D (eure Rückfrage 1): Welche Stufe nimmt die Milch?

Bild `bilder/swr_p2/diagnose_d.jpg` (Spalten D0 … De).

| Stufe | Was | Ergebnis |
|---|---|---|
| D0 | jetzt | golden-milchig, Marmor |
| Da | Szenen-Spiegelungen aus (`r.ReflectionEnvironment 0`, `r.SSR.Quality 0`, `r.Lumen.Reflections.Allow 0`) | Das Wasser wird **weiß-hell** mit harten Glanzwellen, die Ersatz-Spiegelung ist heller als die Szene |
| Db | Himmelslicht 0 | ganze Szene dunkler und wärmer, das Wasser etwas weniger milchig |
| Dc | Sonne `specular_scale` 0 | **kaum Unterschied**, die Sonne ist es also nicht |
| Dac | Da + Dc | wie Da |
| Dd | nur Lumen-Reflexionen aus | etwas grauer und milchiger, die Wellen schärfer |
| De | nur SSR aus | wie D0 |

**Unsere Deutung:**
- Das Gold-Milchige ist die **Lumen-Spiegelung der sonnigen Hänge und des Himmels**, verwischt durch stark verzerrte Normalen.
- Ein Sonnenglanz ist es nicht. W4 lassen wir deshalb weg.

## 3. Varianten W (eure Rückfrage 2)

Bilder `bilder/swr_p2/varianten_w.jpg` (D0, W1, W2, W3, W1+W2, W1+W2+W3, W1 + Rauheit 0,025) und `varianten_w_nah.jpg`
(Ausschnitt nah vor der Kamera).

- **W1 (ELD-Wirbel aus) wirkt am meisten.** Das Wasser wird kühler und grauer, das Gold geht deutlich zurück.
- W2 und W3 allein ändern kaum etwas, W1 + W2 ≈ W1.
- **Rauheit 0,025 statt 0,04:** wie W1, etwas schärfer.
- **In allen Varianten bleibt nah vor der Kamera ein Marmor-Muster.** Es sieht aus wie die Brechung des Grundes durch stark verzerrte
  Normalen.
- Die A/B-Werte aus Nachtrag 5b: Rauheit 0,12 machte es kühler (G1), `Sim Velocity Normal Strength` 5 nur ruhiger (G2), Specular 0,12 fast
  nichts (G3).
- **Laufend:** N1–N4 = W1 + `Fluidsim Normal Strength` 0,3, dazu `Sim Velocity Normal Strength` 5, Brechung 1,05 bzw.
  `Default Near Normal Strength` 0,05. Ergebnis folgt in §6.

## 4. Rural-Australia-Wasser (Ferat: „sieht verdammt gut aus“)

Epic-Beispiel „Rural Australia“ (5.4, `/Game/RuralAustralia`), Material `M_Water_01`. Werte aus dem Editor:
- Shading: Translucent, Default Lit, `TLM_Surface`, 116 Knoten.
- Normalen nah **0,02**, fern 0,5 (Übergang 15–30 m), am Streifwinkel 1,4 (Exponent 9); Kachelung 30 m, Tempo 0,1.
  Uferwellen bis 50 cm vom Ufer, Stärke 0,3; Wobble 0,4.
- Grundfarbe sehr dunkel (0,016; 0,016; 0,008); Untergrund hinter dem Wasser × (0,224; 0,165; 0,106) bis 2,5 m vom Ufer.
- Kaustik (Kachelung 5 m, Ausblenden 2–10 m), Brechung 1,1 (Pixel Normal Offset), **Rauheit 0,8**.
- Die Deckkraft und die Farbe „trübes Wasser“ kommen aus einer **von Hand bemalten** RGB-Maske (Ufer/dunkel/hell).

**Test am p2:** Kopie mit „Used with Water“ als `water_material` am p2-Fluss (Bild `bilder/swr_p2/rural_australia_material_test.jpg`).
- Ergebnis: **Das Wasser wird unsichtbar**, man sieht das trockene Bett. Vermutlich fehlt die gemalte Maske, sodass die Deckkraft 0 wird.
- Zurückgesetzt, nichts gespeichert.

**Frage 1:** Welche Prinzipien aus `M_Water_01` lohnen sich in unserem Master `M_Eldarien_Wasser_Schaum8`? Gemeint sind:
- Normalen nah fast flach, fern stärker;
- Kaustik am Grund;
- Abdunkeln des Grunds am Ufer.

Bitte mit Knoten-Skizze wie bei V18/V19 und mit der Einschätzung, ob das in der gebackenen SWR-Darstellung (WCBS) überhaupt wirkt.

## 5. Plugin „Water Dynamics“ (Ferats Link)

Doku: https://tsibatov.github.io/water-dynamics/ (Fab-Plugin für UE 5.8 von Timur Sibatov, auf Fab unter dem Namen nicht gefunden).
- **Was es laut Doku kann:** CPU-Flachwasser-Löser für Spline-Flüsse; Felsen mit Kollision teilen die Strömung.
  - Wasserfälle als Schwerkraft-Vorhang mit Schaum, Gischt und Impuls ins Becken.
  - Kaustik am Grund, Voreinstellungen für das Bachbett (RockyClear 8 m Sicht …).
  - Boote und Einschläge, Python-Werkzeug `WDWaterAuthoringLibrary`.
- **Grenzen laut Doku:**
  - Kosten etwa 10–11 ms CPU für 2 Flüsse (62 400 + 16 434 Zellen) und 3 Fälle.
  - „Plan for a few active rivers per level“.
  - Keine Zusammenflüsse; Fälle verbinden getrennte Flüsse oben und unten.
  - Kein Landschafts-Graben; Backen wird nicht erwähnt.

**Frage 2:** Lohnt es sich für Eldarien neben dem gebackenen Epic-SWR? Etwa nur für 2–3 Glanzstellen (große Fälle, Fluss am Startort)?
- Gibt es Erfahrungen, Preise, Backen oder Abschalten nach Entfernung?
- Was können wir aus seinen Techniken übernehmen (Kaustik nach Sonnenrichtung, Klarheits-Voreinstellungen, Schaum-Transport)?

## 6. Ergebnis N1–N4

Bild `bilder/swr_p2/varianten_n.jpg` (D0, W1, N1–N4). Das erste N1-Bild bei t430 ist ein verrutschter Kamerablick, bitte nicht werten.
- **N1–N4 sind wie W1:** etwas kühler, das Marmor-Muster bleibt.
- `Fluidsim Normal Strength`, `Sim Velocity Normal Strength`, Brechung und `Default Near Normal Strength` nehmen das Muster also
  **nicht** weg.

## 7. Ferat: „Boden dunkler machen, dunkelbraun Schlammfarbe“ – umgesetzt und gespeichert

Bilder `bilder/swr_p2/boden_braun_s0_s5.jpg` und `boden_braun_s6.jpg`.

| Stand | Was | Ergebnis |
|---|---|---|
| S1 | Wasser bräunlich (Sichttiefe R 350 / G 180 / B 80 cm, Streuung (0,6; 0,45; 0,3) × 0,02) | kaum Wirkung |
| **S2** | Grund unter Wasser dunkelbraun: `Ufer_Staerke_Bach` 1,0 + `Ufer_Farbe_Bach` (0,20; 0,14; 0,09) | **stark: das Wasser liest sich als Wasser, das Milchige ist weitgehend weg** |
| S3 | S1 + S2 | wie S2, etwas brauner |
| **S6** | S2 + W1 (ELD-Wirbel aus), Wasser klar wie F | **gespeichert** (Ferats Wunsch und eure Empfehlung W1) |

**Befund:** Das Marmor-Milchige war zum großen Teil der **helle Grund, gebrochen durch die Normalen**. Mit dunklem Grund verschwindet es,
obwohl die Normalen gleich sind.

**Neu auffällig:**
- Die Bachdekor-Steinpackungen (`SM_SmallStonesPack_*`, `MI_EL_SmallStonesPack_01`, Skala 2–4) leuchten hell-beige auf dem dunklen Grund.
- An den flachen Stufenlippen bleibt ein heller Schleier, weil der Grund-Ton erst ab 5 cm Tiefe greift (W_unter).

**Frage 3:** Wie bekommen Steine im und am Wasser den nassen, dunklen Ton?
- Möglich wäre ein eigener nasser Material-Satz für Bachdekor-Steine oder ein Tiefen-Abdunkeln im Stein-Material.
- Soll der Grund-Ton schon ab 0 cm Tiefe greifen statt ab 5 cm?

## 8. Ferat (19:00, Bild der Talkaskade von oben): „Sieht das für dich natürlich aus?“

Bild `bilder/swr_p2/talkaskade_treppe_von_oben.jpg` (unser gleicher Blick von oben).

**Unsere Antwort an Ferat: noch nicht.**
1. Die Becken sind **zu gleichmäßig**: fast gleich groß, rund und in gleichen Abständen, wie eine **Treppe aus Schüsseln**. Das kommt aus
   unserem p2-Plan (103 gleichartige Becken-Stufen-Einheiten nach 16f §3.2, über die Spline-Tiefe gegraben).
2. **An jeder Stufe liegt ein heller, weicher Schleier** statt weißem Wildwasser über Steinen.
3. Die **Beckenränder sind glatte Mulden** ohne Blöcke; der Übergang dunkel/hell ist hart.
4. Die dünne weiße Linie in der Mitte ist nach unserer Prüfung **die Spline-Anzeige des Editors**: kein Akteur ausgewählt, sie
   erscheint auch in unseren Prüfbildern. Im Spiel prüfen wir sie noch.

**Frage 4 (Hauptauftrag):** Bitte Regeln für **natürliche Step-Pools** an der p2-Talkaskade (s 390–579) und ggf. der Bergrinne, als Plan im
Bach-Koordinatenformat wie `ufer_plan_p2`:
- unregelmäßige Abstände und Größen, Becken länglich in Fließrichtung, schräge oder gekerbte Lippen;
- Stufen aus Blöcken (Netze, Größen, Einbettung, Fugen);
- Kolk hinter der Lippe, Rand-Blöcke, Übergang Nass → Trocken;
- Schaum oder weißes Wasser nur an den Fällen.

Am besten als Änderung der Spline-Tiefen bzw. der Bett-Höhen (wir graben über Brush oder Höhen-Datensatz) plus Blöcke. Ihr kennt die 15f/15g-Regeln
(gekerbte Lippen, Buchten, Eck-/Randblöcke) für die A15-Kaskaden; passt sie bitte auf p2 an.
