# Auftrag 23f – T23e-1 Schritt 1 und T23e-2 gerechnet und gegengeprüft; drei Regelfragen vor dem Planer-Neulauf

Stand 19.10.2026, 04:10 PC-Uhr. Bezug: Antwort 23e (91a4043), Regeln 23.6 (lokal eingefroren als `regeln_23f_2ae02a28`).
Rolle 1 offline. Danach unabhängige Gegenprüfung durch zwei Opus-Prüfer und ein Gesamturteil: **bestätigt mit Mängeln** (Mängel unten).

## 1. Patch 23.6

Der Patch lief wörtlich auf den Referenzcode, ohne assert-Abbruch.

- Selbsttests: `64a654746495eca8` (33 Fälle), „SELBSTTEST 23.6 OK Faelle 10“, 23b `dabb50741db8b9ac`, 23c `b4ebdb213b2f71ba`.
- Beide Prüfer haben das selbst ausgeführt; der Patch ist byte-gleich mit dem Codeblock (diff leer).
- `netz_huellen` enthält keine Dreiecks-Indizes (höchstens 2 000 Eckpunkte je Netz). Gerechnet wurde deshalb mit der Eckpunkt-Hülle.

## 2. T23e-1 Schritt 1: Nass-Anteil der alten Kantenzone (ab Bettkante), Talkaskade s 390–578

`sichtbar_1` = G > 0,1 cm und W − H > 1 cm (6m §3). Dumps: B5 = `T6N1_0` (gespeicherter Stand, Breite 5, BAKED_SIM, SHA c5b91e97…), B1 = `T6N1_2`
(Breite 1, nicht gespeichert, SHA 4b85a372…).

| Zone | Seite | B5 sichtbar_1 | B1 sichtbar_1 |
|---|---|---:|---:|
| Kante 0–1 m | links | 0,293 | 0,315 |
| Kante 0–1 m | rechts | 0,448 | 0,449 |
| Ufer 1–3 m | links | 0,015 | 0,017 |
| Ufer 1–3 m | rechts | 0,019 | 0,019 |
| Hang | beide | 0,000 | 0,000 |

- **Die 66 % aus 23e §1 waren ein Messweg-Artefakt.** Das in r002 benutzte 1-m-Raster `*_sim_spiegel.f32` ist „Gelände + Tiefe G“, nicht die
  Wasseroberfläche (`swr_dump_lesen.py` Z. 70–73). Nachgerechnet ergibt der alte Weg genau 0,662/0,664. Die Beschriftung „SWR-Oberfläche − Gelände“ in
  23e war falsch; das war unser Fehler.
- **Die Breite wirkt kaum auf die sichtbare Wasserkante** (+2 pp links, ±0 rechts). Sie wirkt stark auf G: G > 5 cm in der Kante 0,82/0,86 → 0,46/0,53.
- Euer Fall „Bleibt er bei Breite 1 hoch, steht das Wasser wirklich über der geplanten Bettkante“ trifft rechts zu (45 %). Der Bezug auf die
  Wasserkante ist damit nötig.
- 78 % der Kantenzellen speichern die Oberfläche nur in 2-cm-Schritten, 48–49 % sogar in 4-cm-Schritten. Wirkung auf die Anteile höchstens ±5 pp.
- Kontrollfall Plan unverändert: 12 Werte höchstens 0,0043 vom Soll.

## 3. T23e-1 Schritt 2–3 (VORLÄUFIG, Breite 5; T6N1 ist weder gespeichert noch verworfen, T6N1b wird vorbereitet)

Zonen ab dem Rand der `sichtbar_1`-Zellen. Die neue Kante liegt im Median 0,75 m (links) / 0,95 m (rechts) hinter der Bettkante (p10–p90 −0,35…1,65 m).

| Zone | Netz D | sichtbar D | Anteil > 38° | Fehlbetrag m² je 10 m |
|---|---:|---:|---:|---:|
| Kante links / rechts | 0,34 / 0,33 | 0,69 / 0,68 | 0,40 / 0,47 | 2,3 / 2,4 |
| Ufer links / rechts | 0,38 / 0,37 | 0,73 / 0,72 | 0,24 / 0,31 | 0,3 / 0,6 |
| Hang links / rechts | 0,11 / 0,11 | 0,40 / 0,41 | 0,17 / 0,12 | 10,5 / 11,0 (Netz 0,11 statt 0,25) |

K1 im Band 0–3 m (trocken, je 10 m und Seite): 4,2 / 4,0 (Grenze 10). K2: 56 / 53 (Grenze 85). Ein Vergleichslauf mit B1 ändert fast nichts.
Dieses Ergebnis geht nicht in den Planer, bis der Stand gespeichert ist (eure Abbruchregel §6).

## 4. T23e-2: Stufe B mit 23.6 in C2

| | Stufe B 23.4 | Stufe B 23.6 |
|---|---:|---:|
| FEHLER C2 gesamt | 21 628 | 21 555 |
| davon Fels | 2 868 | 2 795 |
| Talkaskade gesamt | 6 939 | 6 938 |

- Von den **116 Felsen**, die in Stufe B von ok auf FEHLER kippten (alle außerhalb der Talkaskade), sind **72 wieder ok**, alle mit Hohlraum-Anteil > 0
  (Median 0,43, kleinster 0,015). Das stützt U2.
- **44 bleiben FEHLER Lücke.** Neue Lücken: 0. Platte, Totholz, Stein, Kiesel unverändert.
- Diagnose-Varianten (keine Regel): Umriss nur zum Außenraum → 83 von 116 ok; Zelle 0,20 m → 96; Zelle 0,30 m → 97.
- Bei den drei 4-m-Felsen `SM_mountain_rock_big_01_5` (C2:20415, 48022, 8827) reicht die Box bis zum Boden. Die „Lücke“ dort ist ein Schornstein in der
  ausgedünnten Hülle (U1 passt).
- **Echte Luft unter zwei Wandfelsen:** C2:55360 (`SM_mountain_rock_big_02_6`, auf 21,7 m skaliert) und C2:21633 (`…_02_3`, 32,1 m). Die Box-Unterkante
  liegt an der Lückenzelle 3,16 m bzw. 1,76 m über dem Gelände. Rolle 1 hatte das zunächst als U1 gedeutet; die Gegenprüfung hat das widerlegt.

**Bilder:** Der erste Bildlauf (10 tiefe Kameras, PM 03:43) ist nicht beweiskräftig.
- Bei 6 von 9 Kameras trifft der Mittelstrahl 0,05–0,52 m vor dem Ziel die Unterseite des eigenen Steins (Eigenverdeckung).
- Eine Kamera (21633) steckte im Nachbarfeld C1 in einer Felswand.
- Wahrscheinlich echte Lücken zeigen C2:48022 (dunkle Höhlung) und C2:64801 (Platte liegt hohl auf Rundsteinen); belegt ist das nicht.
- Rolle 1 baut jetzt Kameras mit freier Sicht in die Lücke, eine Markierung des Ziels (Debug-Box ohne Akteur) und den Export der Dreiecks-Hüllen
  für die 44 (T23e-3). Ergebnis folgt als Nachtrag.
- Bild (rotes Kreuz = Bildmitte = Ziel): `bilder/platzierung/t23e/t23e2_vier_kameras_mitte.jpg` (48022, 64801, 16606, 55360).

## 5. Antworten auf eure „lokal feststellbar“-Punkte

- **Mapping über 38°:** Das Landschaftsmaterial wählt triplanar mit Dither, Seitenprojektion ab ~33°, voll ab ~50°.
  - In der Ferne (über 60–100 m) zeigt ein Hang mit 38–45° aber überwiegend die von oben projizierte RVT, also mit Streckung 1,27–1,41.
  - Wie das im Bild wirkt, ist ungeprüft (feste Kamera nötig).
- **Plan-Modus der alten Planer:** Keiner schreibt nach Unreal.
  - Fast alle schreiben aber fest nach `export/unreal/welt/<Thema>/<Feld>/` und löschen dort vorher.
  - Eigener Ausgabeordner geht über `--aus` (GEFA, DETA, P2BE, HALD), `--basis` (Biom-Planer), `--nur-zaehlen` (WELT), `--nur-statistik` (UF) und
    `--ohne-veroeffentlichen` (SWBE).
  - WIT, BACH, KANT und wueste_bewuchs haben keinen Schalter; dort ginge eine Rekonstruktion nur über eine Kopie der production-Wurzel.

## 6. Fragen

1. **Trockene Bettzellen in der Kante:** Ab der sichtbaren Wasserkante liegen 15,6 % (links) / 11,5 % (rechts) der neuen Kantenfläche noch innerhalb der
   geplanten Bettkante (d < 0, trocken). Sollen sie zur Kante zählen (Steine dürfen dorthin) oder ausgeschlossen werden? 23e §2 sagt „Steine ins Wasser
   nicht in diesem Schritt“; diese Zellen sind aber trocken.
2. **Echte Lücke unter Wandfelsen (55360, 21633):** 23e sagt „talseitige Lücke durch tieferes Eingraben auf der Talseite beheben“. Bei 22–32 m großen
   Wandfelsen mit 1,8–3,2 m Luft würde das den Fels um diese Höhe absenken. Gilt das auch hier, oder kommt eine andere Lösung in Frage (Netz tauschen,
   Felsfuß/Halde davor, Drehung)? Gibt es eine Größengrenze?
3. **2-cm/4-cm-Schritte der gespeicherten Oberfläche:** Reicht `sichtbar_1` (1 cm) als Wasserkante, oder sollen wir `sichtbar_5` als Bezug nehmen? Bei
   `sichtbar_5` liegt die Kante 0,05–0,06 weiter innen (B5 0,25 / 0,39).

## Dateien (lokal, nicht im Repo)

`docs/pruefung/platzierung/lage4/t23e/` (Bericht, SHA256SUMS 42/42, `t23e1/nass_anteil.md`, `t23e1/zonen_B5_gespeichert_T6N1_0/zonen.md`,
`t23e2_stufe_b/C2_stufe_b_23_6.md`), Gegenprüfung `t23e/gegenpruefung/urteil.md`.
