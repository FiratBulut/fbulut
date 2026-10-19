# Auftrag 23h – Stufe B mit echten Dreiecken (23.7): 100 der 116 wieder ok; SmallStonesPack sind Einzelkiesel; Wandfelsen bleiben; Rückfragen

Stand 19.10.2026, 10:00 PC-Uhr. Bezug: Antworten 23e/23f/23g, 22f §3.7. Regeln 23.9 lokal `regeln_23i_d3ce026a`. Rolle 1 offline, unabhängig nachgeprüft:
„freigegeben mit Bedingungen“.

## 1. Dreiecks-Export (Editor, nur lesend)

- Alle 142 C2-Netze inklusive `SM_SmallStonesPack_01–14` wurden exportiert. Quelle ist RENDER_DATA, also das Nanite-Ersatznetz LOD 0. Fehler: 0.
- Das gerenderte volle Nanite-Netz kann davon abweichen. Fälle mit Lücke unter 15 cm werden deshalb nicht allein nach diesen Dreiecken entschieden.
- **Gefundener Exportfehler:** Bei `SM_dead_log_01–03` liegen die Punkte um Faktor ≈ 20 zu klein vor, in den Dreiecken wie in den alten Hüllen.
  Wahrscheinlich fehlt der Build-Maßstab. Die übrigen 139 Netze passen zu den Editor-Bounds. Die Korrektur läuft. Für Stufe B ohne Folge, denn die drei
  Netze sind `totholz_ast`.

## 2. Stufe B C2

| Fassung | FEHLER gesamt | davon Fels |
|---|---:|---:|
| B 23.4 (Ecken) | 21 628 | 2 868 |
| B 23.6 (Ecken) | 21 555 | 2 795 |
| B 23.7 (Ecken) | 21 540 | 2 780 |
| **B 23.7 (Dreiecke)** | **21 511** | **2 752** |

- Fels/Stein mit Lücke: 1 337 → 467.
- **Die 116:** 100 ok, 0 WARNUNG ueberhang, 16 FEHLER (14 mit Lücke). Alle 8 „Schornsteine“ von `rock_big_01_5` sind weg; U1 ist für sie bestätigt.
- **Neu FEHLER durch Dreiecke:** C2:85197 (Lücke 2,2 → 56,6 cm), keine freie Kamerasicht. Dazu 20417 (6,3 cm) und 35174 (7,4 cm).
- **Offene Netze:** 66 der 142 Netze sind nach dem Verschweißen nicht geschlossen, darunter MossyRockFace_02 (4 der 14 Lücken-FEHLER).
  - Beispiel C2:102247 (L 7,7 m) wird ok, aber nur über Hohlraum-Anteil 0,995 bei Deckung 0,012. Das Netz hat keinen Boden.
- **Wandfels (2 045 Felsen ≥ 4 m):**
  - 64 erfüllen die Überhang-Bedingungen (vorher 213), bleiben aber FEHLER wegen `durchdringung`.
  - FEHLER Lücke: 193 statt 851.
  - **C2:55360** (Lücke 12,0 m, Kontaktanteil 0,11) und **C2:21633** (10,8 m, 0,34) bleiben FEHLER Lücke. Absenken um 1 m oder eine Lage Felsfuß
    reicht bei beiden nicht.

## 3. SmallStonesPack _01–14

- Aus den Dreiecken: Jedes Netz ist **eine geschlossene Hülle**. Die 5–11 „Inseln“ im Export sind Texturnähte.
- Damit gilt nach 22f §3.7 („ab 8 getrennten Inseln“) `kiesel_haufen` für **keines** der 14 Netze. Das widerspricht 23.5 (`_01`/`_03` als Haufen
  bestätigt, nach Bild) und 22f (`_08`/`_10`).
- Das Bild `kpb1_kiesel_zoom` zeigte bei `_01` viele kleine Steine auf flacher Basis. Möglich ist ein zusammenhängend modellierter Haufen; dann
  ist die Inselzahl die falsche Prüfgröße.
- Von 18 925 SmallStonesPack-Instanzen sind 1 055 nach Größe `stein`, nicht `kiesel`.

## 4. Zonen auf dem neuen Wasserstand (6q §3)

- Mit `T6N1b_2` (gespeichert, Paket-SHA passt) verschiebt sich die Kante gegen T6N1_0 im Median um 0,06 / 0,06 m. Der Plan bleibt also.
- Fehlbetrag Kante (Zustand D):
  - mit trockenen Bettzellen 1,8 / 1,9 m² je 10 m;
  - ohne 1,6 / 1,8 m² je 10 m.
- Fehlbetrag Hang: 10,6 / 10,8 m² je 10 m.
- **30 von 39 heutigen Stücken in trockenen Bettzellen** haben Kollision und sind dort nach 23.7 unzulässig.

## 5. Fragen

1. **SmallStonesPack:** Gilt `kiesel_haufen` nach Form (Bild: viele Steine auf gemeinsamer Basis) statt nach Inselzahl? Oder sind sie Einzelkiesel? Mit
   23.9 werden auf Kies ≥ 0,5 ohnehin keine Kiesel mehr gesetzt. Betrifft das nur noch Kiesel außerhalb von Kies?
2. **`durchdringung` zwischen Wandmodulen:** Gilt die Durchdringung auch zwischen Felsen ≥ 4 m, die als Wand zusammengesetzt sind (Klippenmodule
   überlappen absichtlich)? Wenn nicht, welche Bedingung trennt „Wand aus Modulen“ von „Felsen durchdringen sich“?
3. **55360 / 21633 (Wandfelsen, Lücke 11–12 m):** Absenken und Felsfuß reichen nicht. Netztausch oder Entfernen? Gibt es eine Größe, ab der ein Fels nicht
   mehr nach Sitzregeln, sondern als Klippe/Kulisse geprüft wird?
4. **Offene Netze:** Wie sollen „Hohlraum ohne Netzboden“ (Hohlraum-Anteil ≈ 1, Deckung ≈ 0) gewertet werden: als ok (eingegraben), als FEHLER oder
   nur nach Bild?
5. **C2:85197** (56,6 cm, ohne freie Sicht): nach Bild aus größerer Entfernung oder nach Dreiecken allein?
6. **30 unzulässige Stücke in trockenen Bettzellen:** entfernen, oder nur der Planer-Neulauf setzt dort nichts Neues?
