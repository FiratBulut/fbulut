# Antwort 23 – Steine, Platten und Totholz sitzen organisch im Boden: Sollregeln, Prüfung v4, Reparatur, Planer, Pilot C2

Gelesen: recherche/auftraege/23-steine-organisch-im-boden.md @ ed0dadfb61b51c1646e2b40c5acd9fc6dec71366 (Commit 3199188)

Stand 18.10.2026. Bearbeiter: Cloud-Recherche. Bereich: Sollzustand und Prüfklassen „sitzt organisch im Boden“ (v4) für Steine, Platten,
Kleinschutt-Flächen und Totholz, Reparaturform für das Werkzeug „umsetzen“, Planerregeln, Pilot Talkaskade C2 (s 389–580).
**Hier ist nichts im Projekt geprüft oder angewendet.** Der Prüfcode in §13 lief nur synthetisch in der Cloud.

**Lieferung:**
- dieses Dokument;
- `recherche/antworten/steine_sitz_regeln.json` (Regeln 23.1, maschinenlesbar, gleiche Gliederung wie `bachbett_ufer_regeln.json`);
- Prüfcode `sitz_pruefung.py` als Referenz in §13 (nur Standardbibliothek, `python -I … --selbsttest`).

**Bezug, ebenfalls gelesen (Commit 3199188 bzw. f2bb485 für 6o):**
- `recherche/README.md` @ 778d8a7b8ac17fcaceb262ee8b63e46898ff7051, `recherche/vorlagen/pruefung.md` @ 5daf4a9187ba35288dc4838f9461118e0960d068
- `recherche/antworten/bachbett_ufer_regeln.json` @ 4d92cc4b7c23cb5e678fb053c4b20cc9438312a6 (Formatvorbild, `C_ufer.steine`)
- `recherche/antworten/20-detailgrad-bachufer-felsen.md` @ 6d1b257239957030d05c4415d67bed1f20240e9b (ganz),
  `skripte/detailgrad/detailgrad_regeln.json` @ 50922354c40a152a4cd9b84a31445d88f83f31d8 (`eingraben`, `platten`, `netze_rollen`)
- `skripte/p2_bett/p2_bett_regeln.json` @ 79702dfb1ccfb627ede2f31fa5de144c305c28f8 (`ausstattung_6e.totholz`),
  `skripte/p2_bett/p2_bettplan.py` @ c65918691ffef1214808d17f86ef1bc21cf2a5c2 (Totholz-Setzer)
- `skripte/felsgruppen_regeln.json` @ ca1138e677915061897f96b0d710caa04bb1716e (`rollen`, `platten`)
- `16h-nachtrag6d-steine-coast-inventar.md` @ cc5dae2f38c2b607434486b6947e72ab502c2f8f, `16h-nachtrag6e-ferat-witcher4-fels-master.md`
  @ b331814103d860f3286a8289d02bf586d1c3f165, `auftraege/16h-nachtrag6i-baked-sim-tests-stand.md` @ 11c254f0c95defaa25c481ed4047bf7c68625309 (Slab-Pivot)
- `16h-nachtrag6k-t6j-ergebnisse.md` @ bd2ee3191705d425ce7d96a826143f2de3b26667 (§3.1 „sichtbar“), `16h-nachtrag6n-schritt3a-verschwindet.md`
  @ 845ead7c7fb325736d5fc3464c5b3e3164baf826, `auftraege/16h-nachtrag6o-t6n2-u3-g2-tor.md` @ e3f2f5df927c1b03bd593f0702b09d28dd448e7f,
  `antworten/16h-nachtrag6o-t6n2-u3-g2-tor.md` (Commit f2bb485, Kurzfazit: gespeichert bleibt Breite 5, T6N1 mit Breite 1 wartet auf Ferat)
- `21-detailgrad-landschaft-felsdeckung.md` @ 32f301737f1b63bf4931dc22b4c85c80c25169df, `22-wasserpflanzen-fern-vom-wasser.md`
  @ ec84345704467c938629e71bf0b85c74e0ed1e49 (§6 Reparaturform), `boden-kleinzeug-gras.md` @ 4154ed89737e2b9b0afeaa342ffe164d3a58f665 (RVT)
- Daten: `vorlagen/daten/netze_masse.json` @ c337d5bb6082f7098e05738dde6596557f0de386, `material_parameter.json`
  @ 16d1511f96f8e01fa2bfcf71042b912b638a2b54, `fluss_sim/p2_lokal/helle_steine_p2.json` @ d2c2da602d9d29c7f65885a9948b757b2b94925e,
  `fluss_sim/p2_lokal/stein_albedo.json` @ de519d4e95d022dc9da5a5757719d756f3436f86
- Bilder, selbst angesehen: `bilder/platzierung/c2_talkaskade_t430_2026-10-18.jpg` @ b6ff18680d132c00da3b92ca80f5d929b02b1f1c,
  `c2_talkaskade_m_2026-10-18.jpg` @ 9d618e0d10c40bab89ea70f93879d7747b8dde44, `c2_talkaskade_t500_2026-10-18.jpg` @ e5e642a2328d5138720b6ba305eafeb72f78d282.
  Ferats Bild mit den acht Kreisen liegt mir nicht vor; ich nutze die Tabelle in Auftrag §2.

**Kennzeichnung:** [S] = nur Suchauszug (alle Fachseiten waren aus der Cloud nicht abrufbar, §Quellen) · [Repo] = Regel oder Daten im Repository ·
[Bild] = eigene Ansicht der drei Bilder · [Ableitung] = geschlossen, nicht belegt · [Gestaltung] = Gestaltungswert für das Witcher/RDR2-Ziel ·
[Annahme] = Startwert, im Pilot zu bestätigen.

## Kurzfazit

1. **Sollzustand je Klasse (Frage 1): beantwortet.** Tabelle in §3, Zahlen in `steine_sitz_regeln.json`.
   - Fels ≥ 1 m 25–50 % der Höhe im Boden, Stein 30–50 %, Kiesel 40–60 %, Platte 30–60 % der Dicke, Kleinschutt-Fläche 40–70 % der Dicke.
   - Größte Lücke unter der Unterseite: Kleinschutt 2 cm, Kiesel 1,5 cm, Stein 3 cm, Platte min(¼ Dicke, 4 cm), Fels 5–6 cm.
     In Stufe A (Box + 1-m-Raster) kommen 2 cm Rasterzuschlag dazu.
   - Abweichung zur Geländenormale: Kleinschutt ≤ 5°, Platte ≤ 12°, Stein/Kiesel ≤ 25°, Fels ≤ 30° (nur für flache Steine).
   - „Frei liegend“ ist nur auf Halde (26–40°), Blockfeld, Kiesbank und im Hochwasserbett natürlich, und nur mit Kontakt und getragenem Schwerpunkt.
2. **Platten (Frage 2): beantwortet.** Standard ist **liegend**. Schräg nur in zwei Fällen:
   - **Dachziegel** im Wasser: 8–30° stromauf einfallend, Fuß im Bett.
   - **Ausbiss** nur in erklärten Rollen (Band/Wand): ≥ 30° Hang, ≥ 3 Platten mit gleichem Fallen, ≥ 50 % verborgen.
   - Freie Kante liegend höchstens 0,6 × Dicke + 3 cm. Eine Bodenplatte der Rolle „platte“ wird nie zum Ausbiss erklärt.
3. **Stapel und Auflage (Frage 3): beantwortet.** Getragen heißt: Schwerpunkt in der Kontakthülle mit ≥ 10 % Rand, Auflage ≤ 30° geneigt
   (Kiesel ≤ 25°). Durchdringung bis ⅓ der Dicke zwischen Blöcken ist erlaubt. Eine Platte, die eine andere unter ≥ 20° schneidet, ist FEHLER.
   Die Einstufung „gewollte Stapel“ vom 15.10. ist damit ersetzt: Ein schwebender Stein ohne getragenen Schwerpunkt ist kein Stapel.
4. **Im Wasser (Frage 4): beantwortet.** Gemessen wird am echten Gelände H und am gezeichneten Spiegel W des gespeicherten Stands, nie am
   Dump-Boden. Lücke ≤ 2 cm. Herausragen nur ab 0,4 m Größe und höchstens 0,6 × Höhe. Kleinschutt und Äste liegen auf dem Bett.
5. **Totholz (Frage 5): beantwortet.** Ein Stamm liegt auf (≥ 50 % Kontakt), ist eine Brücke (je Ende ≥ 0,5 m auf dem Ufer, Unterkante
   ≥ 0,10 m über W) oder eine Rampe. Der Schwerpunkt liegt immer zwischen den Stützen. Wurzelteller gehören ans Ufer; in Bächen der
   Talkaskade nie ins Wasser. Welches Ende der Netze der Wurzelteller ist: **wartet auf die Punktwolke** (§7).
6. **Farbe (Frage 6): Regel beantwortet; Zuordnung wartet auf die Farbmessung je Netz.** Nordischer Granit/Gneis ist grau bis graubraun.
   Orange gibt es nur als dünne Patina, nie als ganzer Stein. Weiß als Quarzgeröll höchstens selten. Reparatur: MI tauschen, sonst Netz
   ersetzen, kleine Kiesel im Wasser entfernen. Welches Netz die orangen Steine liefert, ist nicht belegt (Verdacht §8).
7. **Reparatur (Frage 7): beantwortet.** Der Entscheidungsbaum steht in §10.
   - Reihenfolge der Versuche: am Ort neu setzen (z, Drehung), dann Versatz bis min(0,5 m; ¼ L), dann verkleinern (nur Platte/Kleinschutt,
     Faktor 0,8–1,0, nie vergrößern), dann ersetzen, zuletzt entfernen mit Sicherung je Instanz.
   - Reihenfolge der Instanzen: Schicht von unten nach oben, groß vor klein, Totholz nach den Steinen, Farbe zuletzt.
   - Fallen in einer Planerschicht > 30 % einer Klasse durch, wird die Schicht neu geplant statt einzeln repariert.
8. **Planer (Frage 8): beantwortet**, je Planer in §11. Kern: Jeder Setzer rechnet z und Drehung aus der ganzen Unterseite, nicht aus dem
   Pivotpunkt, und ruft vor dem Schreiben dieselbe Prüfung auf.
9. **Prüfkriterien und Pilot (Frage 9): beantwortet.** Ablauf: Messweg T23-0, Trockenlauf T23-1, Reparatur T23-2, Welt in drei Stufen (§14).
   Klassen im Wasser warten auf den gespeicherten Wasserstand nach T6N1.
10. **v2-Fehler korrigiert, Prüfcode geliefert.** „Unterkante über dem höchsten von 5 Bodenpunkten“ ist ersetzt durch Lücke, Deckung,
    Kante, Winkel und Planarität über die ganze Unterseite.
    - Im Selbsttest lässt v2 die 25°-Platte mit einer Bodenecke durch, v4 meldet sie.
    - Cloud-Ergebnis zweimal: `SELBSTTEST OK  Regeln 23.1  Faelle 33  Signatur 64a654746495eca8`, auch mit `--regeln steine_sitz_regeln.json`.
11. **Bildbefund:** In allen drei Bildern sehe ich dieselben Fehlerbilder wie in Ferats Tabelle (§1).
    - Kantenplatten mit Kiestextur stehen fast senkrecht an der Wasserkante.
    - Dünne Platten liegen schräg über dem Gras.
    - Zwei orange Kies-Flächen liegen am rechten Hang von t500.
    - Weiße und orange Einzelsteine liegen im Bett.
    - Ein heller Stamm liegt quer über dem Bach.
    Als wahrscheinlichste Ursache sehe ich die Plattenregel des Detailgrad-Planers: „kipp = Neigung“ über 1,0–7 m große Platten am
    gekrümmten Ufer [Ableitung, §1.3].

**Nächste Handlung (genau eine, lokal):** **T23-0 Messweg.** Im Testlevel 16 Kontrollinstanzen von Hand setzen und mit der v4-Prüfung
(Regeln 23.1) messen. Details in §15.

---

## 1. Bildbefund und Zuordnung zu Ferats Kreisen

### 1.1 Was ich in den drei Bildern sehe [Bild]

| Bild | Stelle | Beobachtung |
|---|---|---|
| t430 (Blick bachauf, leicht erhöht) | linkes Ufer, Mitte bis vorn | Reihen dünner, dunkler Platten stehen schräg bis steil, wie umgekippte Bretter. Vorn links an der Wasserkante stehen 3–4 dunkle Platten mit Kiestextur fast hochkant. |
| t430 | Bett vorn links und Mitte | kleine orange Steine an der Wasserkante und im Wasser, ein weißer Stein links vorn, ein gelb-weißer Brocken links |
| t430 | Mitte, Höhe der dritten Stufe | ein heller Stamm liegt quer über dem Bett; seine Auflage auf den Ufern ist im Bild nicht zu erkennen |
| t430 | rechtes Ufer Mitte | große helle flache Platten liegen schräg auf dem Gras; eine hebt die linke Kante deutlich ab |
| t430 | vorn rechts | dünne Platten ragen schräg aus dem Bett neben einem Grasbüschel im Wasser; dazu ein weißes Stück |
| m (Augenhöhe, bachauf) | linkes Ufer | eine Gruppe dünner Platten mit gleichem, steilem Fallen zum Wasser. Das liest sich fast als Schichtausbiss, aber die Unterkanten enden frei über dem Wasser. |
| m | rechts Mitte | eine dünne braune Platte liegt über dem Gras, ihre Kante steht sichtbar ab; helle runde Steine und ein weißer Stein an der Wasserkante |
| t500 (von oben, bachauf) | beide Ufer | dicht an dicht dünne Platten, gekippt und überlappend wie Schindeln, oft mit freier Kante; an den Stufen stehen Platten quer wie Bretter |
| t500 | rechter Hang | **zwei orange-ockerfarbene dünne Kies-Flächen** (eine oben, eine unten mittig), flach, mit sichtbarer Kante |
| t500 | links unten | eine große helle Platte steht steil schräg in den Bach |
| t500 | Bett | mehrere weiße Kiesel; gelb-olive helle Steine rechts unten im Wasser |

### 1.2 Ferats Kreise in unseren Bildern

Ferats Bild liegt etwas näher als t430. Die Zuordnung ist deshalb wahrscheinlich, nicht sicher.

| Kreis (Auftrag §2) | wo in unseren Bildern | Fehlerklasse (Regeln 23.1) | Messgröße, die anschlägt |
|---|---|---|---|
| 1 Platten steil aus dem Hang, weiße Kiesel obenauf | t430 linkes Ufer Mitte; m linkes Ufer | Platte (kein erklärter Ausbiss), Kiesel auf Träger > 25° | winkel, kante, deckung; traeger_neigung |
| 2 Stamm quer, brauner Klumpen im Wasser | t430 Mitte (Stamm sichtbar; den Klumpen sehe ich nicht sicher) | Stamm Brücke, Wurzelteller | bruecke_auflage, treiben, Wurzelteller im Wasser |
| 3 Platten über dem Gras/schwebend, Gras hindurch | t430 rechts Mitte; m rechts Mitte | Platte bzw. Kleinschutt | luecke, deckung, kante; Gras unter Platte |
| 4 Platte wie ein Brett schräg | t430 rechts (abgehobene Kante); t500 links unten | Platte | winkel, kante |
| 5 große Platten übereinander am Hang, dünne Kiesplatte schwebt | t500 rechtes Ufer | Stapel aus Platten, Kleinschutt | durchdringung (kreuzend), schwerpunkt, luecke |
| 6 dunkle Kiesplatten hochkant im Wasser, orange/weiße Steine | t430 vorn links | Kleinschutt bzw. Kantenplatte im Wasser, Farbe | winkel, kante, treiben; farbe_orange/weiss |
| 7 oranger Stein im Wasser, dünne Äste/Platten unter Wasser neben Rohrkolben | t430 vorn rechts (Grasbüschel im Wasser, schräge dünne Teile) | Farbe, Ast/Kleinschutt unter Wasser | farbe_orange; Kontakt am Bett |
| 8 dünne Kiesplatte schräg aus dem Gras | t500 rechter Hang, t430 rechts | Kleinschutt | planaritaet, kante, winkel |

### 1.3 Wahrscheinliche Herkunft je Planer [Ableitung, lokal am Zensus zu bestätigen]

- **Detailgrad, Rolle `platte`** (`SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_02`, im Plan 1 172 Stück; 20 §3.1):
  - Die Regel „yaw ±90° zum Wasser, kipp = Neigung“ legt eine 3,5–6 m große, fast ebene Platte an einen Punkt der Böschung.
  - Das Ufer der Talkaskade ist gekrümmt: Bett, Wand 40–57°, Schulter. Eine ebene Platte kann ihm nicht folgen. Unten taucht sie ins Bett,
    oben steht sie über der Schulterkante heraus. Das sind die Kreise 3, 4 und 8.
  - z wird an einem Punkt gerechnet (`Gelände − Einbettung × Netzhöhe`), nicht über den Grundriss.
- **Detailgrad, `platte.kante`** (`SM_NordicBeachRockyGround_02`, 1,0–1,5 m, d −0,1…0,6 m):
  - An der Wasserkante ist die „Neigung“ die Bettwand. Mit `kipp = Neigung` steht die Kiesplatte fast hochkant im Wasser. Das ist Kreis 6.
- **Detailgrad, `stapel` und 2. Lage** (`SM_flat_rock_02` 3,99 × 3,22 × 0,86 m, `SM_ground_rock_03_03`):
  - Kippung je Haufen 10–25° und z = Gelände + z_rel.
  - Flache Netze werden so zu schräg übereinandergeschobenen Platten. Das ist Kreis 5.
  - Fugenschutt (K1/K2) landet obenauf, auch auf steilen Platten. Das ist Kreis 1.
- **Bettplan, `totholz.quer_ueber_becken`** (p2_bettplan.py Z. 984–1025):
  - z ist absolut gesetzt: Beckenspiegel + 0,15–0,35 m. Die Lage der Enden zum Ufer wird nicht geprüft.
  - Ein Netz mit Wurzelteller (`SM_FallenSpruceTree_01`, Grenzen −6,37 … +0,93 m, also Pivot an einem Ende) kann den Teller über
    oder in das Wasser legen. Das ist Kreis 2.
  - Bachdekor setzt laut `helle_steine_p2.json` (Stand 13.10.) außerdem `SM_beach_driftwood_01` und `SM_LargeFallenTree_01` ins Bett.
- **Farbe:**
  - Die Namaqualand-Netze sind in Detailgrad-Paletten (K2/K3) und nur mit dem Vorschlag „Namaqualand grau“ (`MI_EL_NL_namaqualand_*`)
    eingeplant. Fehlt diese MI, tragen sie ihr Originalmaterial. Ob das orange ist, ist nicht belegt; `netze_masse.json` hat für sie kein Material.
  - Die weißen Stücke können `SM_mountain_rock_small_01_*` sein (Y 0,229, das hellste Bachnetz, 6d/6e) oder ein anderes helles Netz.
    Das klärt die Farbmessung (§8).

---

## 2. Messgrößen (Definitionen für Rolle 1)

Eingaben je Instanz aus dem Zensus:
- Netz, Foliage-Typ (Ebene), Lage, Drehung als UE-Rotator (Pitch, Yaw, Roll; Achsen wie `FRotationMatrix`) und Skala;
- Netzgrenzen aus `netze_masse.json` (cm → m) mit dem Pivot als Netzursprung. Der Slab-Pivot an der Y-Kante (6i) ist damit automatisch richtig.

Gelände: `hoehe.f32` bilinear. Nanite-Displacement der Landschaft ist aus (21). Wird es eingeschaltet, muss die Prüfung die verschobene Höhe nehmen.

| Größe | Definition | ersetzt / Zweck |
|---|---|---|
| Unterseite (Stufe A) | 7 × 7 Punkte der Box-Unterseite (lokal z = min). Für Stein, Fels und Kiesel nur die Kern-Ellipse mit 0,6 × halber Box, weil Felsen unten nicht kastenförmig sind (wie 16h N5: Auflage 60 % der Hülle) | v2: 5 Bodenpunkte |
| Unterseite (Stufe B) | untere Hülle der Punktwolke: je 10-cm-Zelle des lokalen Grundrisses der tiefste Punkt. Bei Stein und Fels nur in der Kern-Ellipse, denn die Flanke eines runden Steins ist keine Lücke | genauer, sobald die Punktwolke da ist |
| Träger T(x,y) | max(H, Oberseite jeder anderen Fels- oder Holzinstanz, die die Senkrechte unter z + 0,10 m schneidet) | Stein auf Stein |
| d_i | z_i − T(x_i, y_i) | > 0 Lücke, < 0 im Boden |
| **luecke_max** | max d_i über die Unterseite | **neu: tiefster Punkt allein genügt nicht** |
| **deckung** | Anteil der Unterseitenpunkte mit d_i ≤ 3 cm | **neu: Auflage-Anteil statt „eine Ecke berührt“** |
| eingrab_hoehe | (Median H unter der Unterseite − z_min) / (z_max − z_min), z aus den 8 Boxecken bzw. der Punktwolke | Steine, Fels |
| eingrab_dicke | Mittel von clamp(−(z_i − H_i)/T, 0, 1) über die Unterseite | Platten, Kleinschutt |
| winkel | Winkel zwischen der dünnsten Netzachse und der Normale der Ausgleichsebene des Geländes unter der Unterseite | — |
| planaritaet | größte Abweichung des Geländes von dieser Ausgleichsebene unter der Unterseite | große Platten am Knick |
| kante_frei | max(z − H) über 32 Randpunkte der Oberseite | „Kante ragt heraus“ |
| durchdringung | Eindringtiefe zweier gedrehter Boxen (Trennachsen-Test), geteilt durch die kleinere Dicke; dazu der Winkel zwischen den Dickenachsen | Platte durch Platte |
| schwerpunkt_rand | Abstand der Boxmitte zum Rand der konvexen Hülle der Kontaktpunkte der vollen Unterseite, geteilt durch die halbe Grundbreite; < 0 außen | getragen |
| traeger_neigung | Neigung der Oberseite des tragenden Teils (Dickenachse gegen Welt-Z) | rutscht ab |
| treiben | ≥ 50 % der Unterseite über sichtbarem Wasser und luecke_max > 2 cm gegen das echte Bett bzw. einen Träger | Stein im Wasser |
| Totholz-Achse | Punkte alle 0,25 m entlang der langen Achse an der Unterkante. Stützen = Punkte mit d ≤ 3 cm. Kragarm und Brücke daraus (§7) | frei hängendes Holz |

**Wasser:** W ist der gezeichnete Spiegel des zum Prüfzeitpunkt gespeicherten Stands.
- Heute ist das BAKED_SIM mit Breite 5. Nach Ferats Freigabe von T6N1 wird es ggf. Breite 1 (6o). Die Dump-ID wird mitgeschrieben.
- Als Wasser zählen nur Zellen „sichtbar_1“: nass und W − H > 0,01 (6k §3.1).
- Der Dump-Boden R − G auf trockenen Zellen ist kein Boden (6m/6n) und wird nie verwendet.

**Warum v2 versagt:** v2 meldet „schwebend“, wenn die Unterkante über dem höchsten von 5 Bodenpunkten liegt. Eine um 25° gekippte
1,2-m-Platte, deren tiefste Ecke den Boden berührt, hat aber 0,51 m Lücke am anderen Ende. v2 nennt sie „ok“ (Selbsttest F2).
v4 misst die Lücke über die ganze Unterseite und verlangt eine Mindestdeckung.

---

## 3. Regeltabelle je Klasse (Frage 1)

**Erkennung** (Reihenfolge, L ≥ B ≥ T = Ausdehnung × Skala):
1. Name Stumpf, Wurzel oder Holz. Ein Holz-Netz mit L ≥ 2 m und B ≥ 0,2 m ist ein Stamm, sonst ein Ast.
2. Name `*RockyGround*`, `BeachSandWithPebbles`, `DryRiverBed` usw., oder T/L ≤ 0,12 mit L ≥ 1,5 m und T ≤ 0,35 m: Kleinschutt-Fläche.
3. T/B ≤ 0,35: Platte (z. B. `texndcpda_tier_0`, `SM_flat_rock_02`, `SM_ForestRockSlab_01`).
4. sonst Fels (L ≥ 1 m), Stein (0,3–1 m) oder Kiesel (< 0,3 m).

| Klasse | Eingraben (Ziel, FEHLER) | größte Lücke | Deckung (≤ 3 cm) | Winkel zur Geländenormale | freie Kante | frei liegend natürlich, wenn … | Begründung |
|---|---|---|---|---|---|---|---|
| **Fels ≥ 1 m** | 25–50 % der Höhe; FEHLER < 15 %, WARNUNG „versunken“ > 75 % | Kern 6 cm (+2 cm Raster); Punktwolke bergseits 5 cm, talseits ≤ 0,15 h (max 30 cm) | ≥ 60 % im Kern | ≤ 30°, nur wenn T/L < 0,6 | – | Halde 26–40°, Blockfeld, Gleithang-Kiesbank: ≥ 10 % eingegraben, ≥ 3 Kontakte, Schwerpunkt getragen, lange Achse ± 25° zur Falllinie | [Fach] Halden-Klasten liegen mit der Langachse hangabwärts [S]; Keystones sind verkeilt [S]. [Repo] 20: K4 35–50 %, felsgruppen block 25–38 %. [Gestaltung] ⅓ eingegraben liest als „gesetzt“, über ¾ als Geländebeule |
| **Stein 0,3–1 m** | 30–50 %; FEHLER < 20 %, > 80 % | Kern 3 cm (+2); Punktwolke 3 cm | ≥ 70 % | ≤ 25°, wenn T/L < 0,6 | – | Halde, Kiesbank, Hochwasserbett: ≥ 15 % | [Repo] 20: K3 33–50 %, Kontakt ≥ 60 %. [Fach] stabile Lage mit der flachen Seite auf der Unterlage |
| **Kiesel < 0,3 m** | 40–60 %; FEHLER < 25 % | 1,5 cm | ≥ 80 % | ≤ 25° | – | nie frei; auf Stein/Platte nur, wenn der Träger ≤ 25° geneigt ist | [Repo] 20: K2 40–60 %. [Fach] Schüttwinkel um 30–35° [S], also bleibt loses Kleinzeug steiler nicht liegen |
| **Platte (dünn)** | 30–60 % der Dicke; FEHLER < 15 % | min(¼ T, 4 cm) (+2) | ≥ 85 % (Box), ≥ 70 % (Punktwolke) | ≤ 12° (Gestaltung 0–8°) | ≤ 0,6 T + 3 cm | nur als Dachziegel oder erklärter Ausbiss (§4) | [Repo] felsgruppen: Z = Geländenormale, ≥ 50 % eingegraben, Schwebetoleranz 5 cm. [Ableitung] Planarität ≤ 0,5 T als WARNUNG, weil große Platten Knicke nicht abbilden |
| **Kleinschutt-Fläche** | 40–70 % der Dicke; FEHLER < 25 % | 2 cm | ≥ 90 % | ≤ 5° | ≤ 0,5 T + 2 cm | nie; Hang ≤ 38°, Planarität ≤ 0,4 T | [Fach] Halden 30–37° [S]. [Gestaltung] Kiestextur auf einem schrägen Brett ist sofort als Fehler lesbar (Kreise 5, 6, 8) |
| **Totholz Stamm** | 5–35 % des Durchmessers an den Auflagen | zwischen Stützen nur als Brücke/Rampe | ≥ 50 % der Länge, wenn liegend | Achse folgt dem Gelände ± 10°, wenn liegend | – | Brücke/Rampe nach §7 | [Fach] Klassen Brücke, Teilbrücke, lose, vergraben; junge Stämme quer über dem Gerinne [S] |
| **Totholz Ast** | – | – | ≥ 50 % (im Wasser ≥ 70 % oder verkeilt) | – | – | Kragarm ≤ 0,3 L | [Fach] Kleinholz wird ausgerichtet und an Steinen verkeilt [Ableitung aus S] |
| **Totholz Stumpf** | 5–20 cm | talseits ≤ 0,1 D | – | **Achse ≤ 8° zur Welt-Z** (nicht zur Normale) | – | – | Bäume wachsen lotrecht; talseits darf der Wurzelanlauf frei liegen |
| **Totholz Wurzel (flach)** | 20–50 % der Dicke; FEHLER < 10 % | 3 cm | ≥ 75 % | ≤ 10° | – | – | wie Kleinschutt, etwas weicher |

**Gras unter Platten und Kleinschutt (Kreis 3):** Unter dem Grundriss plus 0,3 m wird die Grasdichte-Maske auf 0 gesetzt. Das geht über
dieselbe Maske wie in 6i (`v_gras_*`). Die Landschaftslage ist dort Felsplatte, Geröll oder Kies. Grasbüschel-Instanzen im Grundriss werden
wie in v3 „überdeckt von Felsen“ entfernt.

---

## 4. Platten (Frage 2)

| Zustand | wann | Grenzen | Begründung |
|---|---|---|---|
| **liegend** (Standard) | überall, wo kein anderer Fall gilt; immer auf Hängen < 30°, auf Wiese, Terrasse, im Bett ohne Strömungslage | Winkel ≤ 12°, Kante ≤ 0,6 T + 3 cm, Lücke ≤ min(¼ T, 4 cm), Deckung ≥ 85 %, 30–60 % der Dicke im Boden | Platten liegen stabil mit der großen Fläche auf. Bei T = 0,25 m (NordicBeachRockyGround_02) bleiben höchstens 18 cm Kante sichtbar |
| **Dachziegel** (Imbrikation) | ≥ 50 % der Unterseite über sichtbarem Wasser oder im Uferband d ≤ 0,6 m, Fließrichtung bekannt | 8–30° zum Bett; die Normale zeigt waagrecht stromauf (± 45°), das stromab liegende Ende ist das hohe. Stromauf-Hälfte zu ≥ 80 % im Bett. Lücke ≤ min(15 cm; 0,6 T + ½ L sin Winkel), also ein Keil nach stromab. Lange Achse ± 20° parallel (16h C4) oder quer (Kiesel) zur Strömung, nie 30–60° schräg. Überlappung: die stromab liegende Platte steckt mit ihrem Stromauf-Ende **unter** dem Stromab-Ende der oberen, 10–30 % von L | [Fach] a-b-Ebenen fallen stromauf ein; gemessen 22,6–37,6° im Mittel, Wasserschotter Median ≈ 35°, über 50° eher Murgang [S]. [Gestaltung] 8–30°, damit es als Strömungslage und nicht als Brett liest |
| **Ausbiss** (Schicht steht an) | nur Rollen `felsgruppen:band/wand`, `klippenband_B5`, `detailgrad:wand`; Hang ≥ 30°, Lagen Fels/Felsplatte ≥ 50 % im Umkreis | ≥ 3 Platten im Radius 6 m mit gleicher Fallrichtung (± 15°) und gleichem Fallen (± 10°). ≥ 50 % der Mittelfläche verborgen, sichtbare Kante ≤ min(0,5 L; 0,6 m), Dicke ≥ 0,15 m, Streichen ± 20° zur Höhenlinie. Kein Tageslicht unter dem Überstand (Bildprüfung) | [Fach] Schichten zeigen in einer Gruppe einheitliches Streichen und Fallen; steil stehende Schichten laufen gerade über das Gelände [S]. [Gestaltung] Nur erklärte Rollen dürfen stehen |

**Wie viel darf eine Kante überstehen?** Liegend 0,6 T + 3 cm. Dachziegel: der Keil nach stromab, höchstens 15 cm. Ausbiss: min(0,5 L; 0,6 m).

Der Fall „flache Steinplatten ragen steil schräg aus dem Hang“ (Kreis 1) ist danach nur zulässig, wenn alle Ausbiss-Bedingungen gelten.
Die Platten im Bild m links gehören zur Rolle `platte` bzw. `stapel`. Sie sind deshalb FEHLER, obwohl sie fast einheitlich fallen.

---

## 5. Stapel und Auflage (Frage 3)

| Prüfung | Grenze | Begründung |
|---|---|---|
| **getragen** | Schwerpunkt in der konvexen Hülle der Kontaktpunkte (Träger = Gelände oder Instanz), Rand ≥ 10 % der halben Grundbreite; Kontaktanteil Block ≥ 15 %, Platte ≥ 40 %, Kiesel ≥ 30 %; ≥ 3 Kontakte nicht auf einer Linie | Statik: ein Körper liegt, wenn der Schwerpunkt über der Auflage liegt |
| **Neigung der Auflage** | ≤ 30° (Kiesel ≤ 25°) | Reibungs-/Schüttwinkel um 33–37° [S], mit Abstand |
| **2. Lage** | Eingraben in den Boden entfällt; stattdessen in der 1. Lage verkeilt bis 35 % (20) | [Repo] 20: Stapelung im Haufen |
| **Durchdringung Block/Block** | ≤ 35 % der kleineren Dicke | verzahnt liest als ein Körper (20: überlappend 0,35–0,55 × Größe) |
| **Platte in Block** | ≤ 50 % der Plattendicke | Platte unter den Block geschoben |
| **Platte/Platte parallel** (Winkel ≤ 10°) | ≤ 30 % der Dicke, als Schindel | Dachziegel- oder Schichtpaket |
| **Platte/Platte kreuzend** (Winkel ≥ 20°) | ≤ 10 % der Dicke, sonst FEHLER | eine Platte, die eine andere schräg durchsticht, gibt es nicht (Kreis 5) |

**Ab wann wirkt Durchdringung falsch?**
- Wenn eine dünne Kante aus der Oberfläche des anderen Teils austritt (kreuzende Platten).
- Wenn ein Stein mehr als ⅓ seiner Dicke in einem anderen steckt und die Schnittlinie auf einer sichtbaren Fläche liegt.

Die zweite Bedingung prüft das Bild, nicht die Box.

**Folge für C2/B5:** Die Einstufung „gewollte Stapel“ vom 15.10. gilt nicht mehr. Ein Stapel besteht nur, wenn jedes obere Stück getragen ist.

---

## 6. Im Wasser (Frage 4)

| Was | Regel | Begründung |
|---|---|---|
| Messbezug | echtes Gelände H; W = gezeichneter Spiegel (sichtbar_1) des gespeicherten Stands; Dump-ID im Bericht | 6k §3.1, 6m/6n (Dump-Boden ist Artefakt) |
| Eingraben im Bett | Fels 30–50 %, Keystone an Lippen 40–60 %, Stein 30–50 %, Kiesel 50–80 % | [Fach] Keystones verkeilen sich quer, bevorzugt an Engstellen [S]; Bettsteine stecken im Bett (Einbettungsklassen 0–25/…/76–100 % [S]) |
| Lücke | ≤ 2 cm (+2 cm Raster in Stufe A), Deckung ≥ 80 % | klares Wasser zeigt jede Lücke als Schattenfuge |
| Herausragen | erlaubt ab L ≥ 0,4 m, höchstens 0,6 × Höhe. Steine < 0,2 m nur, wenn das Wasser dort < 8 cm tief ist (Film auf der Schnelle). Oberkante nicht innerhalb ± 3 cm um W (WARNUNG, Spiegelrand flimmert) | Stufen und Schnellen zeigen Köpfe der großen Steine; kleine bleiben unter Wasser |
| Kleinschutt-Fläche | liegt auf dem Bett (Lücke ≤ 2 cm auf ≥ 90 %), Bettneigung ≤ 15°, Oberkante ≤ W − 5 cm, nie an Lippen und Stufenwänden | Kreis 6: die Kiesplatte an der Wand ist der Fehler |
| Äste unter Wasser | auf dem Bett mit ≥ 70 % Kontakt oder an einem Stein ≥ 0,3 m auf dessen Stromauf-Seite verkeilt; lange Achse ± 30° zur Strömung; dunkel (Y 0,04–0,08) | Kreis 7 |
| Helligkeit | Y ≈ 0,08 unter Wasser (6d), Nasslinie, nie doppelt abdunkeln | [Repo] 6d/6e |
| SWR-Hindernis | Steine ≥ 0,4 m im Wasser oder ≤ 1 m daneben: im Piloten nur z und Drehung, kein XY, nicht entfernen; Liste für einen eigenen Schritt mit Hindernis-Neubau, Reset und Bake | Änderung am Hindernis ändert das Wasser |

**Abhängigkeit:** Wasser vor Ufer (README). Die Wasser-Klassen (treiben, herausragen) werden erst nach dem gespeicherten Wasserstand aus T6N1
(Breite 1 oder 5) repariert. Die trockenen Klassen können vorher laufen.

---

## 7. Totholz (Frage 5)

| Fall | Regel | Begründung |
|---|---|---|
| **liegend** | ≥ 50 % der Achsenpunkte mit Kontakt, Schwerpunkt zwischen der ersten und letzten Stütze, Kragarm ≤ 0,25 L, 5–35 % des Durchmessers im Boden | Durchhang kann ein starres Netz nicht; deshalb nur Stützenlage und Kragarm |
| **Brücke** (quer über Wasser) | je Ende die äußeren 0,5 m zu ≥ 50 % mit Kontakt auf **trockenem** Ufer hinter der Kante; Unterkante ≥ 0,10 m über W (Ziel 0,15–0,35 wie p2bett); 60–90° zur Strömung; Länge 1,3–2,5 × Wasserbreite | [Fach] junge Stämme liegen quer über kleinen Gerinnen, meist senkrecht dazu, oft jahrelang über dem Bach; das Verhältnis Länge/Breite bestimmt die Verankerung an den Ufern [S] |
| **Rampe** | ein Ende auf dem Ufer, das andere mit Kontakt auf dem Bett, Schwerpunkt dazwischen | Teilbrücke [S] |
| **verboten** | Achsenpunkt über sichtbarem Wasser unter W ohne Bettkontakt (treiben); Schwerpunkt außerhalb der Stützen; ein Ende frei in der Luft mit Kragarm > 0,25 L | Kreis 2 |
| **Wurzelteller** | am Ufer: ≥ 50 % des Tellergrundrisses trocken, ≥ 0,3 m hinter der Wasserkante. Im Wasser nur als Rampe mit ≥ 40 % Bettkontakt und Tiefe ≤ 0,5 × Tellerhöhe. **In der Talkaskade (Bach < 6 m) nie im Wasser** | [Fach] Rekrutierung durch Ufererosion und Windwurf [S]: der Teller bleibt am Ufer |
| **Stumpf** | Achse ≤ 8° zur Welt-Z, 5–20 cm im Boden, talseits Lücke ≤ 0,1 D | Bäume wachsen lotrecht |
| **Netzwahl** | kein `SM_beach_driftwood_01` im Bergbach (Küstenholz, ausgebleicht) | [Gestaltung] |

**Wurzelteller-Ende:** Bei `SM_FallenSpruceTree_01` (−6,37 … +0,93 m in X) und `SM_LargeFallenTree_01` ist das Teller-Ende aus den
Grenzen allein nicht sicher. Regel: Teller-Ende = die Endscheibe (10 % der Länge) mit ≥ 1,8 × Querschnitt der anderen, aus der Punktwolke.
**Wartet auf die Punktwolke** (Stufe B). Bis dahin werden beide Netze in Brücken und Rampen nicht gesetzt.

**Tundra-Talkaskade:** 20 §7 hat entschieden: Referenz 0 Stämme, Bettplan-Totholz 5 bleibt. Mit diesen Regeln bleiben davon nur die,
die als Brücke oder Rampe bestehen. Der Rest wird entfernt, nicht umgesetzt.

---

## 8. Farbe (Frage 6)

| Was | Regel | Begründung |
|---|---|---|
| Palette nordischer Bergbach (Granit/Gneis) | neutral grau bis graubraun. BaseColor-Mittel trocken Y 0,07–0,22, Sättigung (HSV auf sRGB) ≤ 0,25, zwischen 0,12 und 0,25 nur Warmton 20–60°. Unter Wasser Y 0,06–0,09 (Ziel 0,08) | [Repo] 6d; [S] alpine Gerölle grau mit Flechten, Moos und Algenfilm |
| **orange** | Hue 10–45° und Sättigung ≥ 0,35: als ganzer Stein **FEHLER**. Zulässig nur als Patina-Maske im Material: ≤ 30 % der Oberfläche, S ≤ 0,45, Y ≤ 0,12, an der Spiegellinie oder an Sickerstellen, ≤ 5 % der Steine je 50 m | [S] orange Flecken auf Granit entstehen durch umgelagertes Eisen als dünner Hydroxid-Belag; orange Bäche = oxidiertes Eisen. Eine dünne Haut, kein durchgefärbter Kiesel |
| **weiß** | Y ≥ 0,30 trocken bzw. ≥ 0,12 unter Wasser oder ≥ 2 × Median der Nachbarn: WARNUNG. Quarzgeröll höchstens 1 je 20 m, ≤ 0,15 m, nicht gehäuft; sonst FEHLER | [Ableitung] Quarzadern im Gneis sind möglich, aber selten |
| gemessen | `SmallStonesPack` 0,125 (beige, nass × 0,65 → 0,081), `mountain_rock_small` 0,229 (zu hell; trocken × 0,8, unter Wasser × 0,35), Bett 0,067 | 6d |
| Reparatur | (1) Form gut und graues MI vorhanden → MI tauschen (mit Nasslinie, nie doppelt abdunkeln). (2) Textur fest orange/weiß und kein graues MI → Netz gleicher Größenklasse aus der Rollenpalette. (3) Kiesel < 0,15 m im Wasser → entfernen | Budget: Kiesel sind im Überfluss (20: K2 50–65 je 10 m) |

**Messweg:** wie `stein_albedo.json`, aber mit RGB-Mittel und Hue/Sättigung je wirksamem MI. Den Fall „MI fehlt, Originalmaterial aktiv“
gesondert ausweisen. Der Verdacht auf Namaqualand ohne graue MI ist damit in einem Lauf zu klären.

---

## 9. „Sitzt organisch“ heißt auch Material: RVT-Fuß, Nasslinie, Moos, Nanite

- **Geometrie zuerst.** Ein RVT-Übergang versteckt die Fuge, aber keine Lücke: Eine 5-cm-Lücke bleibt als Schatten- und Lichtspalt sichtbar.
  Darum kommt der Materialschritt nach der Prüfung v4.
- **RVT-Fußblend:**
  - Der Weg ist dokumentiert: Landschaft schreibt in ein RVT, das Netzmaterial liest es und blendet zur Netztextur über
    (Epic: RVT für Landschafts- und Objektblend; Polycount-Anleitung [S]).
  - Im Projekt hat `M_EL_Klippe_RVT` die Parameter `Blend_Hoehe` 150 cm und `Blend_Weich` 80 cm (Klippen-Maßstab) [Repo].
    Kinder sind nur `MI_EL_Klippe_xjijdiz/xjijbgx/xfplcbf/xf3odif`; `xjijbgx` steht auch in der Detailgrad-Palette K3.
  - Für Steine braucht es eigene MI-Werte: Blend-Höhe 10–25 % der sichtbaren Höhe, also Kiesel 2–4 cm, Stein 5–15 cm, Fels 15–40 cm,
    Platte 2–5 cm; Weich ≈ ½ davon [Gestaltung].
  - Für `M_EL_Fels_MS2` und `M_Master_material` fehlt der Fußblend: eine Funktion `MF_EL_RVT_Fuss` ist **anzulegen** (wie `MF_EL_Nasslinie`).
  - Unter Wasser kein RVT-Blend, dort gilt die Nasslinie.
- **Vorsicht 5.8:** Ein Forumsbericht meldet, dass das RVT nur die Grundfarbe statt der gemalten Lagen enthält [S]. Vor dem Ausrollen an einem
  Stein prüfen, ob das RVT die Lagen zeigt.
- **Moos oben, Algen unten:** Material-Skizze aus 6e §3 (Moos über WorldNormal.Z, Algen unter der Linie). Liegende Platten bekommen Moos auf
  der Oberseite, nicht an der Kante.
- **Kontakt-Begleiter:** 20 verlangt 3–6 Steine und 6–12 Schutt um jeden Block sowie Gras in Ritzen. Diese Begleiter tragen den Übergang
  stärker als jeder Shader.
- **Nanite:** Die Platten-Netze (`TundraRockyGround`, `NordicBeachRockyGround`, `ErodedRockyGround`) sind laut `netze_masse.json` nicht
  Nanite. Das betrifft die Kosten, nicht den Sitz. Die Prüfung arbeitet auf Grenzen und Punktwolke und ist vom Renderweg unabhängig.
  Der Bildvergleich im Piloten prüft danach Nanite- und Nicht-Nanite-Netze getrennt (pruefung.md).
- **Kleinschutt am Hang:** Statt dicker Schutt-Netze auf > 20° besser die Landschaftslage Kies/Geröll oder ein Decal (`M_MS_Decal` steht im
  Materialbestand) [Ableitung]. Ein Netz mit Dicke muss flach liegen; eine Lage hat keine Kante.

---

## 10. Reparatur (Frage 7)

### 10.1 Entscheidungsbaum je Instanz

```
0  gesperrt (Sehens-Ort, Akteur, V0-Zone)?             -> nur melden
1  SWR-Hindernis (>= 0,4 m im/<= 1 m am Wasser)?       -> nur Schritt 2 ohne XY; sonst Liste "Hindernis-Schritt"
2  neu setzen am Ort: z, Pitch, Roll, Yaw +-20 Grad
     Platte/Kleinschutt: Dickenachse = Normale der Ausgleichsebene (+ Gestaltungsneigung 0-8 Grad),
                         z so, dass eingrab_dicke = Mitte der Zielspanne
     Stein/Fels:         flache Seite zur Normale, z auf Mitte der Zielspanne
     Totholz:            Achse auf die zwei hoechsten Stuetzen legen; Stumpf lotrecht
     -> Pruefung v4 bestanden? fertig
3  Versatz: XY bis min(0,5 m; 0,25 L) (Totholz laengs 0,5 m, quer 0,3 m), 8 Richtungen x 2 Radien, dann wie 2
     verboten: Wechsel nass/trocken, ueber die Uferkante, Lippen-/Hauptstrahlzone, Wege, Mindestabstaende der Planer
     -> bestanden? fertig (bester Kandidat = kleinster Versatz)
4  verkleinern: nur Platte/Kleinschutt, gleichmaessig 0,8-1,0, Groessenklasse bleibt, dann 2-3
5  ersetzen (gleicher Ort, Rollenpalette): kleineres/duenneres Netz;
     Platte -> 2-4 Steine K3; Kleinschutt -> Lage Kies/Geroell + 3-6 K2; Stamm -> kuerzeres Netz als Rampe/liegend
6  entfernen, Sicherung je Instanz wie v3
```

**Skala:** nur verkleinern, Faktor 0,8–1,0, nur Platten und Kleinschutt, gleichmäßig, Größenklasse unverändert. Nie vergrößern:
Größere Platten folgen dem Gelände noch schlechter, und die Texelwirkung ändert sich.

**XY:** ja, aber begrenzt (oben). Ohne Versatz bliebe am Knick oft nur das Entfernen. Mit mehr Versatz verschiebt das Werkzeug die
Komposition der Planer (Haufen-Rhythmus aus 20).

### 10.2 Reihenfolge, wenn Fehler zusammenkommen

1. **Schicht für Schicht von unten.** Zuerst die Instanzen mit Geländekontakt, dann die 2. Lage. Nach jeder Änderung eines Trägers die
   von ihm getragenen neu prüfen. Fällt ein Träger weg, wird das obere Stück wie eine neue 1. Lage behandelt (Schritt 2) oder entfernt.
2. **Groß vor klein:** Fels, Platte, Stein, Kleinschutt, Kiesel. Kleines füllt Fugen relativ zum Großen.
3. **Totholz nach den Steinen**, weil es auf Ufern und Steinen liegt.
4. **Farbe zuletzt**, nur an Instanzen, die bleiben.
5. **Platten übereinander (Kreis 5):** untere Platte zuerst flach legen. Dann die obere: parallel als Schindel (≤ 30 % Dicke Überlappung,
   getragen) oder ersetzen. Eine kreuzende obere Platte wird nicht nachgeführt, sondern ersetzt oder entfernt.

### 10.3 Schicht neu planen statt reparieren

Fallen in einer Planerschicht (Foliage-Typ-Präfix) > 30 % einer Klasse durch, wird diese Klasse nicht einzeln repariert. Dann gilt:
1. die Klasse mit Sicherung entfernen;
2. den Planer mit den Regeln aus §11 neu laufen lassen;
3. neu setzen.

Ich erwarte das für die Detailgrad-Platten der Talkaskade [Ableitung aus §1.3; exakt erst T23-1].

### 10.4 Sicherung (Werkzeug „umsetzen“ von Rolle 4)

Je Instanz eine Zeile im v3-Format, ergänzt um:
- Alt- und Neu-Transformation, Netz, Foliage-Typ, Regelversion 23.1, Test-ID;
- Fehlerklassen vor und nach, Messwerte (luecke_max, deckung, eingrab, winkel, kante, planaritaet), Schritt (2–6), Versatz und Skalenfaktor.

Rücknahme = Zeilen zurückspielen; im Piloten eine 1-%-Stichprobe auf identische Transformation prüfen. Speicherbeleg je Paket.

---

## 11. Planerregeln (Frage 8)

**Gemeinsamer Setzer-Vertrag (alle Planer):**
1. z und Drehung aus der ganzen Unterseite rechnen, nicht aus dem Pivotpunkt. Pivotversatz aus `netze_masse.json` beachten
   (Slab: Körper nur +Y, 1,55 m × Skala, 6i).
2. Vor dem Schreiben `sitz_pruefung` (Regeln 23.1) aufrufen. Bei FEHLER den Entscheidungsbaum §10.1 Schritte 2–5 anwenden, sonst
   verwerfen. Je Instanz ein Feld `sitz` mit den Messwerten ins Plan-JSON schreiben.
3. Gemeinsame Bibliothek `sitz_pruefung` ist **anzulegen** (aus §13). Es gibt keine eigene Schwebe-Logik je Planer mehr.
4. Platten- und Kleinschutt-Foliage-Typen für Handarbeit: Align to Normal an, Align Max Angle 38, Random Pitch ≤ 5°,
   Z Offset = −(0,3…0,6) × T (Eigenschaften laut Epic-Doku [S], Werte [Ableitung]).

| Planer / Thema | Was sich ändert |
|---|---|
| **detailgrad** (Antwort 20) | `platten`: kein `kipp = Neigung` mehr. Platten liegen nach der Ausgleichsebene des Grundrisses. Größe ≤ ebene Fläche: Planarität ≤ 0,5 T über den Grundriss, sonst kleineres Netz bzw. K3-Steine. `platte.kante`: nur bei Böschung < 30° an der Kante, an steileren Wänden Steine/Blöcke. `stapel`/`haufen`: Kippung 10–25° nur für Steine mit T/L ≥ 0,35, nicht für flache Netze (`SM_flat_rock_02`, `SM_ground_rock_03_03` liegen); 2. Lage nur getragen (§5). Fugenschutt nur auf Trägern ≤ 25°. `wand` darf als Ausbiss stehen (§4) |
| **p2bett** (Bettplan) | `totholz`: z nicht mehr absolut aus dem Beckenspiegel. Netzlänge aus Wasserbreite + 2 × (Kante bis 0,5 m dahinter) wählen und beide Auflagen auf trockenem Ufer prüfen; Teller-Ende auf das Ufer; Rampe als zweite Art. Keystones/Lippenblöcke 40–60 % im Bett |
| **kantenufer_p2** | Kiesel-Packs nur auf Flächen ≤ 30° und nicht auf Platten > 25°, 40–60 % eingegraben |
| **bachdekor_swr** | Kleinschutt-Flächen (`SM_TundraRockyGround_01`, `SM_NordicBeachRockyGround_02` als „kies“) im Bett nur bei Bettneigung ≤ 15°, normal ausgerichtet, Oberkante ≤ W − 5 cm, nie an Lippen. Steine im Wasser z aus dem echten H, nie aus dem Dump-Boden. `SM_beach_driftwood_01` streichen; Stämme nur nach den Totholzregeln. Farbe: nur Netze mit grauem MI/Nasslinie |
| **felsschalen** | Rückseite der Schale zu ≥ 60 % mit Kontakt zur Wand (Bildkritik A5); keine Schale auf Hängen < 35° über Gras |
| **felsgruppen** | Plattenregel bleibt (Z = Normale, ≥ 50 %, 5 cm). Neu: Kern-Ellipse/Punktwolke für Blöcke, Durchdringungsgrenzen §5, Ausbiss-Gruppenprüfung für `band`/`wand` |
| **B5-Themen** (21) | `klippenband_B5`: Bänder als Ausbiss-Gruppe (gleiches Fallen ± 10°, ≥ 35 % eingegraben). `halde_B5`: Teppich-Netze nur bis 38° und normal ausgerichtet, Blöcke mit Langachse ± 25° zur Falllinie. `platten_B5`: Platten liegen (≤ 12°), Fugenpflanzen bleiben. `baumgruppen_B5`: 8 tote Bäume und 18 Totholz nach §7 (Stumpf lotrecht, Stamm getragen) |
| **Biom-Planer** (heide_tundra, nordkueste usw.) | über die `felsgruppen_overrides` zentral; keine eigene Regel nötig |

**Reihenfolge-Falle:** Planer, die später neu laufen (detailgrad, p2bett, bachdekor), überschreiben eine Einzelreparatur. Für ihre Schichten
gilt deshalb: erst den Planer ändern, dann neu setzen. Einzelreparatur nur für Schichten ohne geplanten Neulauf.

---

## 12. Prüffälle gut/schlecht

### 12.1 Synthetisch (Cloud, im Code §13)

Die Sollurteile sind von Hand aus der Geometrie abgeleitet, nicht vom Werkzeug erzeugt.

| Nr. | Fall | Soll | Ist (Cloud) |
|---|---|---|---|
| F1 | Platte flach, 50 % der Dicke im Boden | ok | ok |
| F2 | Platte 25° gekippt, eine Ecke berührt den Boden (v2: ok) | FEHLER luecke, winkel, kante | FEHLER deckung, eingrab, kante, luecke, winkel |
| F3 | Platte 10 cm über dem Boden | FEHLER luecke | FEHLER deckung, eingrab, kante, luecke |
| F4 | Platte auf 30°-Hang, normal ausgerichtet, halb im Boden | ok | ok |
| F5 | Platte über konvexem Hangknick | FEHLER luecke, kante | FEHLER deckung, kante, luecke, winkel |
| F6 | Kleinschutt-Fläche 3 × 3 m flach, halb im Boden | ok | ok |
| F7 | Kleinschutt-Fläche über dem Knick | FEHLER planaritaet, kante | FEHLER deckung, kante, luecke, planaritaet, winkel |
| F8 / F9 | Stein 40 % eingegraben / 6 cm schwebend | ok / FEHLER luecke, eingrab | ok / FEHLER deckung, eingrab, luecke |
| F10 | Kiesel auf der 30°-Platte F4 | FEHLER traeger_neigung | FEHLER traeger_neigung |
| F11 / F12 | Stein mittig auf Block / über der Blockkante | ok / FEHLER schwerpunkt, luecke | ok / FEHLER deckung, luecke, schwerpunkt |
| F13 | zwei Platten kreuzen sich unter 40° | FEHLER durchdringung (beide) | FEHLER (beide) |
| F14 / F15 | Stamm als Brücke / Schwerpunkt über dem Wasser, Ende frei | ok / FEHLER schwerpunkt | ok / FEHLER kragarm, schwerpunkt |
| F16 / F17 | Stein 5 cm über dem Bett im Wasser / Stein 40 % im Bett, ragt 6 cm heraus | FEHLER treiben / ok | FEHLER … treiben / ok |
| F18 / F19 | Stumpf 20° schief / lotrecht | FEHLER stumpf_achse / ok | wie Soll |
| F20a–c / F21 | drei Ausbiss-Platten (Rolle band, 70° am 30°-Hang) / dieselbe Platte allein (Rolle platte) | ok / FEHLER winkel | ok (ausbiss) / FEHLER |
| F22 / F23 | Dachziegel 15° stromauf einfallend / stromab einfallend | ok / FEHLER winkel | wie Soll |
| F24 | grau / orange / weiß | ok / FEHLER / WARNUNG | wie Soll |
| F25 / F26 | Stein als Punktwolke (Ellipsoid) 35 % im Boden / 4 cm darüber (Stufe B) | ok / FEHLER luecke | wie Soll |
| Klassen | 12 Bestandsnetze (u. a. `NordicBeachRockyGround_02` → kleinschutt, `ForestRockSlab_01` → platte, `OldTreeBranch_02` → stamm, `BirchTreeStump_01` → stumpf) | wie erwartet | wie erwartet |

### 12.2 Kontrollfälle im Testlevel (für T23-0, von Hand gesetzt)

Bestandsnetze; Sollwert = Setzwert. Lücke und Eingraben werden zusätzlich unabhängig mit einem Line-Trace im Editor abgelesen
(pruefung.md: Sollwert nicht mit demselben Algorithmus).

| K | Netz | Aufbau | Soll |
|---|---|---|---|
| K1 | `SM_NordicBeachRockyGround_02` | flach auf Ebene, z = −12 cm | ok |
| K2 | dasselbe | 20° gekippt, eine Kante auf dem Boden | FEHLER (v2: ok) |
| K3 | `texndcpda_tier_0` | flach, 40 % der Dicke im Boden | ok |
| K4 | dasselbe | auf 30°-Rampe, normal, 40 % | ok |
| K5 | dasselbe | über eine 90°-Kante der Rampe gelegt | FEHLER kante |
| K6 / K7 | `SM_mountain_rock_small_01_1` | 35 % eingegraben / 5 cm schwebend | ok / FEHLER |
| K8 | `SM_SmallStonesPack_01` | auf `texndcpda` mit 30° | FEHLER traeger_neigung |
| K9 / K10 | `SM_stones_01_2` auf `SM_mountain_rock_big_02_1` | mittig / Schwerpunkt über der Kante | ok / FEHLER |
| K11 / K12 | `SM_OldFallenTree_02` (3,57 m) über einem 2-m-Graben | beide Enden auf / Schwerpunkt über dem Graben | ok / FEHLER |
| K13 / K14 | `SM_BirchTreeStump_01` | lotrecht 10 cm / 20° schief | ok / FEHLER |
| K15 | `SM_mountain_rock_small_01_2` | in Wasserbecken mit festem Spiegel, 5 cm über dem Boden | FEHLER treiben |
| K16 | `SM_ForestRockSlab_01` | flach mit Pivot an der Y-Kante, Skala 0,5 | ok (Pivotversatz richtig gelesen) |

### 12.3 Gut/schlecht im Projekt (Bildreferenz)

| gut | schlecht |
|---|---|
| Kantenstein mit Nasslinie, ⅓ im Bett, Schutt in der Fuge, Gras dahinter (20 §1.1) | Kiesplatte hochkant an der Bettwand (t430 vorn links) |
| Platte flach im Hang, nur 5–15 cm Kante, Moos oben | Platte schräg über dem Gras mit abgehobener Kante (t430/m rechts) |
| Schindelpaket parallel, getragen, mit Fallen in einer Richtung | Platten kreuz und quer übereinander (t500 beide Ufer) |
| Stamm quer, beide Enden ≥ 0,5 m auf dem Ufer, bemoost | Stamm mit Ende oder Wurzelteller im Wasser (Kreis 2) |
| graue, nass dunkle Bachsteine | orange Kies-Flächen (t500 rechts), orange/weiße Kiesel im Bett (t430) |

---

## 13. Prüfcode (Referenz, Python 3, nur Standardbibliothek)

**Umfang:**
- Messgrößen §2 in Stufe A (Box) und Stufe B (Punktwolke);
- Klassenurteil §3–§7, Ausbiss-Gruppen, Dachziegel, Durchdringung, Farbe, Klassenerkennung;
- die alte v2-Regel zum Vergleich;
- synthetischer Selbsttest: 41 × 41-m-Welt mit Ebene, 30°-Hang mit konvexem Knick und Bach (Bett 9,0, Spiegel 9,3, Fluss +y), 33 Fälle
  und 12 Netznamen.

**Cloud-Ergebnis:**
- `python -I sitz_pruefung.py --selbsttest` zweimal: `SELBSTTEST OK  Regeln 23.1  Faelle 33  Signatur 64a654746495eca8`;
- mit `--regeln recherche/antworten/steine_sitz_regeln.json` dieselbe Signatur;
- Gegenprobe: In einer Kopie mit Plattenwinkel 45° schlagen F2, F13, F21 und F23 nicht mehr bei `winkel` an (FEHLER bleibt über Lücke und
  Kante). Die Datei wird also wirklich gelesen.
- Laufzeit 0,15 s.

**Lokale Anbindung (Rolle 1):**
- Zensus: Lage in cm → m, Rotator unverändert, Skala je Achse. Netzgrenzen `netze_masse.json` (cm → m). Gelände `hoehe.f32` des Felds plus
  Rand, als `Raster` mit Feldursprung. W aus dem Dump des gespeicherten Stands, nur sichtbar_1.
- Fließrichtung: Tangente von `lauf_p2` in Richtung wachsender s; später das SWR-Geschwindigkeitsfeld.
- `traeger()` sucht hier linear über alle Instanzen. Für 70 Felder ein Gitter-Index (2-m-Zellen, nur Fels-/Holz-Klassen) davorschalten.
- Stufe B: `Inst(..., punkte=[lokale Netzpunkte in m])` aus dem Editor-Export; dann gilt die Lückengrenze ohne Rasterzuschlag.
- Nicht im Code und lokal zu ergänzen: talseitige Fels-Lücke (Stufe B), Wurzelteller-Ende, Gras-Maske unter Platten, Ast-verkeilt-Regel.

```python
# sitz_pruefung.py - Referenz "sitzt organisch im Boden" (Antwort 23, Regeln 23.1). Nur Standardbibliothek.
# Aufruf: python -I sitz_pruefung.py --selbsttest [--regeln steine_sitz_regeln.json]
# Einheiten m und Grad. Drehung wie UE-Rotator (Pitch, Yaw, Roll), Achsen wie FRotationMatrix (Pitch > 0 = +X nach oben).
# Netzgrenzen bmin/bmax im Netzraum in m (netze_masse.json / 100), Pivot = Netzursprung.
import argparse, hashlib, json, math

R = {  # Grenzwerte = steine_sitz_regeln.json "klassen"/"toleranzen" (Version 23.1)
    "tol": {"kontakt": 0.03, "wasser": 0.02, "raster": 0.02, "kern": 0.6, "spiegelrand": 0.03},
    "fels": {"e": (0.15, 0.75), "luecke": 0.06, "luecke_pw": 0.05, "deckung": 0.6, "winkel": 30, "winkel_TL": 0.6},
    "stein": {"e": (0.20, 0.80), "luecke": 0.03, "luecke_pw": 0.03, "deckung": 0.7, "winkel": 25, "winkel_TL": 0.6},
    "kiesel": {"e": (0.25, 0.90), "luecke": 0.015, "luecke_pw": 0.015, "deckung": 0.8, "winkel": 25, "winkel_TL": 0.7, "traeger": 25},
    "platte": {"e_dicke": 0.15, "deckung": 0.85, "winkel": 12},
    "kleinschutt": {"e_dicke": 0.25, "luecke": 0.02, "deckung": 0.9, "winkel": 5, "hang": 38},
    "stamm": {"kontakt": 0.5, "kragarm": 0.25, "ende_m": 0.5, "ende_kontakt": 0.5, "ueber_W": 0.10},
    "ast": {"kontakt": 0.5, "kragarm": 0.30},
    "stumpf": {"achse": 8},
    "ausbiss": {"hang": 30, "n": 3, "radius": 6.0, "richtung": 15, "fallen": 10, "verborgen": 0.5, "dicke": 0.15},
    "dachziegel": {"winkel": (8, 30), "richtung": 45, "deckung_oben": 0.8},
    "stapel": {"rand": 0.1, "durch_block": 0.35, "kreuz_winkel": 20, "kreuz_anteil": 0.10},
    "farbe": {"Y": (0.07, 0.22), "s_max": 0.25, "s_neutral": 0.12, "orange_h": (10, 45), "orange_s": 0.35, "weiss_Y": 0.30},
}
AUSBISS_ROLLEN = {"band", "wand", "klippenband"}

def v_add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def v_sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def v_mul(a, k): return (a[0] * k, a[1] * k, a[2] * k)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def norm(a):
    n = math.sqrt(dot(a, a)); return (a[0] / n, a[1] / n, a[2] / n) if n > 1e-12 else (0.0, 0.0, 0.0)
def winkel(a, b):  # Winkel zwischen Achsen ohne Vorzeichen, Grad
    return math.degrees(math.acos(min(1.0, abs(dot(norm(a), norm(b))))))

def achsen(pitch, yaw, roll):
    p, y, r = (math.radians(v) for v in (pitch, yaw, roll))
    SP, CP, SY, CY, SR, CR = math.sin(p), math.cos(p), math.sin(y), math.cos(y), math.sin(r), math.cos(r)
    return ((CP * CY, CP * SY, SP), (SR * SP * CY - CR * SY, SR * SP * SY + CR * CY, -SR * CP),
            (-(CR * SP * CY + SR * SY), CY * SR - CR * SP * SY, CR * CP))

class Raster:  # 1-m-Raster wie hoehe.f32, bilinear
    def __init__(s, f, nx, ny, x0=0.0, y0=0.0, zelle=1.0):
        s.x0, s.y0, s.z, s.nx, s.ny = x0, y0, zelle, nx, ny
        s.w = [[f(x0 + i * zelle, y0 + j * zelle) for i in range(nx)] for j in range(ny)]
    def __call__(s, x, y):
        u, v = (x - s.x0) / s.z, (y - s.y0) / s.z
        i, j = max(0, min(s.nx - 2, int(math.floor(u)))), max(0, min(s.ny - 2, int(math.floor(v))))
        fu, fv = u - i, v - j
        a, b, c, d = s.w[j][i], s.w[j][i + 1], s.w[j + 1][i], s.w[j + 1][i + 1]
        return (a * (1 - fu) + b * fu) * (1 - fv) + (c * (1 - fu) + d * fu) * fv

class Welt:
    def __init__(s, H, W=None, fluss=None):
        s.H, s.W, s.fluss = H, W, fluss  # W(x,y) -> Spiegel oder None (nur sichtbar_1-Zellen), fluss(x,y) -> Einheitsvektor
    def nass(s, x, y):
        if s.W is None: return None
        w = s.W(x, y)
        return w if (w is not None and w - s.H(x, y) > 0.01) else None

class Inst:
    def __init__(s, nr, netz, pos, rot, skala, bmin, bmax, klasse, rolle="", farbe=None, punkte=None):
        s.nr, s.netz, s.pos, s.klasse, s.rolle, s.farbe, s.punkte = nr, netz, pos, klasse, rolle, farbe, punkte
        s.ax = achsen(*rot)
        s.sk = skala if isinstance(skala, (tuple, list)) else (skala, skala, skala)
        s.bmin, s.bmax = bmin, bmax
        s.ext = [(bmax[k] - bmin[k]) * s.sk[k] for k in range(3)]
        order = sorted(range(3), key=lambda k: s.ext[k])
        s.k_duenn, s.k_lang = order[0], order[2]
        s.T, s.L = s.ext[s.k_duenn], s.ext[s.k_lang]
    def welt(s, q):
        p = s.pos
        for k in range(3): p = v_add(p, v_mul(s.ax[k], q[k] * s.sk[k]))
        return p
    def ecken(s):
        return [s.welt((a, b, c)) for a in (s.bmin[0], s.bmax[0]) for b in (s.bmin[1], s.bmax[1]) for c in (s.bmin[2], s.bmax[2])]
    def mitte(s): return s.welt(tuple((s.bmin[k] + s.bmax[k]) / 2 for k in range(3)))
    def gitter(s, z_lokal, n=7, kern=None):
        pts = []
        for a in range(n):
            for b in range(n):
                fa, fb = a / (n - 1), b / (n - 1)
                if kern is not None and ((2 * fa - 1) ** 2 + (2 * fb - 1) ** 2) > kern * kern: continue
                x = s.bmin[0] + fa * (s.bmax[0] - s.bmin[0]); y = s.bmin[1] + fb * (s.bmax[1] - s.bmin[1])
                pts.append(s.welt((x, y, z_lokal)))
        return pts
    def rand_oben(s, n=8):
        x0, x1, y0, y1, z = s.bmin[0], s.bmax[0], s.bmin[1], s.bmax[1], s.bmax[2]
        r = []
        for i in range(n):
            f = i / n
            r += [s.welt((x0 + f * (x1 - x0), y0, z)), s.welt((x1, y0 + f * (y1 - y0), z)),
                  s.welt((x1 - f * (x1 - x0), y1, z)), s.welt((x0, y1 - f * (y1 - y0), z))]
        return r
    def oberseite_bei(s, x, y):  # senkrechte Linie durch (x,y): hoechster Austrittspunkt aus der Box, sonst None
        t0, t1 = -1e9, 1e9
        for k in range(3):
            o = dot(s.ax[k], v_sub((x, y, 0.0), s.pos)) / s.sk[k]
            d = s.ax[k][2] / s.sk[k]
            if abs(d) < 1e-12:
                if not (s.bmin[k] <= o <= s.bmax[k]): return None
                continue
            a, b = (s.bmin[k] - o) / d, (s.bmax[k] - o) / d
            t0, t1 = max(t0, min(a, b)), min(t1, max(a, b))
        return t1 if t0 <= t1 else None

def untere_huelle(punkte, zelle=0.10, kern=None):
    """Stufe B: je 10-cm-Zelle des lokalen Grundrisses der tiefste Netzpunkt; bei Steinen/Fels nur in der Kern-Ellipse."""
    x0, x1 = min(p[0] for p in punkte), max(p[0] for p in punkte); y0, y1 = min(p[1] for p in punkte), max(p[1] for p in punkte)
    zellen = {}
    for p in punkte:
        k = (int((p[0] - x0) / zelle), int((p[1] - y0) / zelle))
        if k not in zellen or p[2] < zellen[k][2]: zellen[k] = p
    out = list(zellen.values())
    if kern is not None:
        cx, cy, hx, hy = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
        out = [p for p in out if ((p[0] - cx) / hx) ** 2 + ((p[1] - cy) / hy) ** 2 <= kern * kern]
    return out

def traeger(welt, insts, ich, x, y, z):
    """Traegerflaeche: max(Gelaende, Oberseite anderer Instanzen unter z + 0,10). Gibt (hoehe, quelle) zurueck."""
    best, quelle = welt.H(x, y), None
    for o in insts:
        if o is ich: continue
        t = o.oberseite_bei(x, y)
        if t is not None and t <= z + 0.10 and t > best: best, quelle = t, o
    return best, quelle

def ebene(pts):  # Ausgleichsebene z = a x + b y + c, Normale, max. Abweichung
    n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n; mz = sum(p[2] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts); syy = sum((p[1] - my) ** 2 for p in pts); sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    sxz = sum((p[0] - mx) * (p[2] - mz) for p in pts); syz = sum((p[1] - my) * (p[2] - mz) for p in pts)
    det = sxx * syy - sxy * sxy
    a, b = ((sxz * syy - syz * sxy) / det, (syz * sxx - sxz * sxy) / det) if abs(det) > 1e-12 else (0.0, 0.0)
    res = max(abs(p[2] - (mz + a * (p[0] - mx) + b * (p[1] - my))) for p in pts)
    return norm((-a, -b, 1.0)), res

def huelle(pts):  # konvexe Huelle 2D (monotone chain)
    p = sorted(set((round(x, 6), round(y, 6)) for x, y in pts))
    if len(p) < 3: return p
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in p:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0: lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], q) <= 0: hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]

def abstand_innen(poly, x, y):  # > 0 innen (Abstand zum Rand), < 0 aussen
    if len(poly) < 3: return -1.0
    d = 1e9
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        ex, ey = b[0] - a[0], b[1] - a[1]; l = math.hypot(ex, ey)
        s = ((x - a[0]) * ey - (y - a[1]) * ex) / l  # < 0 links (innen bei Gegenuhrzeigersinn)
        d = min(d, -s)
    return d

def obb_durchdringung(a, b):
    ca, cb = a.mitte(), b.mitte()
    ha = [v_mul(a.ax[k], a.ext[k] / 2) for k in range(3)]; hb = [v_mul(b.ax[k], b.ext[k] / 2) for k in range(3)]
    tests = list(a.ax) + list(b.ax) + [cross(i, j) for i in a.ax for j in b.ax]
    t = v_sub(cb, ca); best = 1e9
    for L in tests:
        if dot(L, L) < 1e-10: continue
        L = norm(L)
        ra = sum(abs(dot(h, L)) for h in ha); rb = sum(abs(dot(h, L)) for h in hb)
        ov = ra + rb - abs(dot(t, L))
        if ov <= 0: return 0.0
        best = min(best, ov)
    return best

def messe(i, welt, insts):
    tol = R["tol"]; m = {}
    duenn = i.klasse in ("platte", "kleinschutt", "totholz_wurzel")
    kern = None if (duenn or i.klasse.startswith("totholz")) else tol["kern"]
    unten = [i.welt(q) for q in untere_huelle(i.punkte, 0.10, kern)] if i.punkte else i.gitter(i.bmin[2], 7, kern)
    d, kontakt, quellen, nass_n = [], [], [], 0
    for p in unten:
        t, q = traeger(welt, insts, i, p[0], p[1], p[2])
        d.append(p[2] - t); quellen.append(q)
        if p[2] - t <= tol["kontakt"]: kontakt.append((p[0], p[1], q))
        if welt.nass(p[0], p[1]) is not None: nass_n += 1
    m["luecke_max"] = max(d); m["deckung"] = sum(1 for v in d if v <= tol["kontakt"]) / len(d)
    m["nass_anteil"] = nass_n / len(unten)
    hpts = [(p[0], p[1], welt.H(p[0], p[1])) for p in unten]
    n_t, m["planaritaet"] = ebene(hpts)
    m["hang"] = math.degrees(math.acos(n_t[2]))
    m["winkel"] = winkel(i.ax[i.k_duenn], n_t)
    zs = [c[2] for c in i.ecken()]; hs = sorted(h[2] for h in hpts)
    m["e_hoehe"] = max(0.0, min(1.0, (hs[len(hs) // 2] - min(zs)) / (max(zs) - min(zs))))
    m["e_dicke"] = sum(max(0.0, min(1.0, -(p[2] - welt.H(p[0], p[1])) / i.T)) for p in unten) / len(unten)
    m["kante_frei"] = max(p[2] - welt.H(p[0], p[1]) for p in i.rand_oben())
    auf_inst = [k for k in kontakt if k[2] is not None]
    m["aufliegend"] = len(auf_inst) > 0.5 * max(1, len(kontakt))
    if auf_inst:
        m["traeger_neigung"] = max(math.degrees(math.acos(min(1.0, abs(k[2].ax[k[2].k_duenn][2])))) for k in auf_inst)
    voll = unten if kern is None else i.gitter(i.bmin[2], 7)   # Stuetzflaeche aus der vollen Unterseite
    stuetz = [(p[0], p[1]) for p in voll if p[2] - traeger(welt, insts, i, p[0], p[1], p[2])[0] <= tol["kontakt"]]
    c = i.mitte(); poly = huelle(stuetz)
    halb = 0.5 * min(e for k, e in enumerate(i.ext) if k != i.k_duenn)
    m["schwerpunkt_rand"] = abstand_innen(poly, c[0], c[1]) / halb if len(poly) >= 3 else -1.0
    m["oben_z"] = max(zs); m["h_welt"] = max(zs) - min(zs)
    return m, unten, d

def messe_holz(i, welt, insts):
    """Achsenpunkte alle 0,25 m an der Unterkante entlang der langen Achse."""
    k = i.k_lang; n = max(3, int(i.L / 0.25) + 1); pts = []
    for j in range(n):
        q = [(i.bmin[a] + i.bmax[a]) / 2 for a in range(3)]
        q[k] = i.bmin[k] + (i.bmax[k] - i.bmin[k]) * j / (n - 1); q[2] = i.bmin[2]
        pts.append((i.L * j / (n - 1), i.welt(tuple(q))))
    st, frei_nass = [], []
    for s, p in pts:
        t, _ = traeger(welt, insts, i, p[0], p[1], p[2]); w = welt.nass(p[0], p[1])
        if p[2] - t <= R["tol"]["kontakt"]: st.append((s, w is None))
        elif w is not None: frei_nass.append((s, p[2] - w))
    m = {"kontakt": len(st) / len(pts), "L": i.L}
    if not st: m.update(kragarm=i.L, schwerpunkt_ok=False, bruecke=False); return m
    a, b = min(x[0] for x in st), max(x[0] for x in st); sp = i.L / 2
    m["schwerpunkt_ok"] = a <= sp <= b
    m["kragarm"] = max(a, i.L - b) if m["schwerpunkt_ok"] else min(abs(sp - a), abs(sp - b)) + i.L / 2
    m["bruecke"] = bool(frei_nass) and all(a < x[0] < b for x in frei_nass)
    ende = R["stamm"]["ende_m"]
    m["ende_a"] = sum(1 for x in st if x[0] <= ende and x[1]) / max(1, sum(1 for s, _ in pts if s <= ende))
    m["ende_b"] = sum(1 for x in st if x[0] >= i.L - ende and x[1]) / max(1, sum(1 for s, _ in pts if s >= i.L - ende))
    m["unter_W_min"] = min((x[1] for x in frei_nass), default=None)
    m["treibt"] = any(x[1] < 0 for x in frei_nass)
    return m

def urteil(i, welt, insts):
    f, w = [], []; tol = R["tol"]
    if i.klasse == "totholz_stumpf":
        if winkel(i.ax[2], (0, 0, 1)) > R["stumpf"]["achse"]: f.append("stumpf_achse")
        m, _, _ = messe(i, welt, insts)
        if m["e_hoehe"] <= 0.0: f.append("stumpf_schwebt")
        return f, w, m
    if i.klasse in ("totholz_stamm", "totholz_ast"):
        r = R["stamm"] if i.klasse == "totholz_stamm" else R["ast"]; m = messe_holz(i, welt, insts)
        if not m["schwerpunkt_ok"]: f.append("schwerpunkt")
        if m["kragarm"] > r["kragarm"] * i.L: f.append("kragarm")
        if m.get("treibt"): f.append("treiben")
        if m.get("bruecke"):
            if i.klasse == "totholz_stamm" and min(m["ende_a"], m["ende_b"]) < R["stamm"]["ende_kontakt"]: f.append("bruecke_auflage")
            if m["unter_W_min"] is not None and m["unter_W_min"] < R["stamm"]["ueber_W"]: f.append("bruecke_tief")
        elif m["kontakt"] < r["kontakt"] and "schwerpunkt" not in f: f.append("kontakt")
        return f, w, m
    m, unten, d = messe(i, welt, insts); k = i.klasse
    if k in ("fels", "stein", "kiesel"):
        r = R[k]
        if not m["aufliegend"]:
            if m["e_hoehe"] < r["e"][0]: f.append("eingrab")
            if m["e_hoehe"] > r["e"][1]: w.append("versunken")
        grenze = r["luecke_pw"] if i.punkte else r["luecke"] + tol["raster"]   # Stufe B ohne Rasterzuschlag
        if m["luecke_max"] > grenze: f.append("luecke")
        if m["deckung"] < r["deckung"] and m["luecke_max"] > tol["kontakt"]: f.append("deckung")
        if i.T / i.L < r["winkel_TL"] and m["winkel"] > r["winkel"]: f.append("winkel")
        if m["aufliegend"]:
            if m["schwerpunkt_rand"] < R["stapel"]["rand"]: f.append("schwerpunkt")
            if k == "kiesel" and m.get("traeger_neigung", 0) > r["traeger"]: f.append("traeger_neigung")
            if m.get("traeger_neigung", 0) > 30: f.append("traeger_neigung")
    elif k in ("platte", "kleinschutt"):
        dz = None
        if k == "platte" and m["nass_anteil"] >= 0.5 and welt.fluss is not None:
            c = i.mitte(); fl = welt.fluss(c[0], c[1]); n = i.ax[i.k_duenn]
            n = n if n[2] > 0 else v_mul(n, -1); hz = norm((n[0], n[1], 0.0))
            rz = math.degrees(math.acos(max(-1.0, min(1.0, -(hz[0] * fl[0] + hz[1] * fl[1])))))
            if R["dachziegel"]["winkel"][0] <= m["winkel"] <= R["dachziegel"]["winkel"][1] and rz <= R["dachziegel"]["richtung"]:
                dz = m["winkel"]
        if dz is not None:  # Dachziegel: stromauf-Haelfte im Bett, Keil nach stromab
            c = i.mitte(); fl = welt.fluss(c[0], c[1])
            oben = [dv for p, dv in zip(unten, d) if (p[0] - c[0]) * fl[0] + (p[1] - c[1]) * fl[1] < 0]
            if sum(1 for v in oben if v <= tol["kontakt"]) / max(1, len(oben)) < R["dachziegel"]["deckung_oben"]: f.append("dachziegel_fuss")
            if m["luecke_max"] > min(0.15, 0.6 * i.T + 0.5 * i.L * math.sin(math.radians(dz))) + tol["raster"]: f.append("luecke")
            return f, w, m
        if k == "platte":
            if m["e_dicke"] < R["platte"]["e_dicke"]: f.append("eingrab")
            if m["luecke_max"] > min(0.25 * i.T, 0.04) + tol["raster"]: f.append("luecke")
            if m["deckung"] < R["platte"]["deckung"]: f.append("deckung")
            if m["winkel"] > R["platte"]["winkel"]: f.append("winkel")
            if m["kante_frei"] > 0.6 * i.T + 0.03 + tol["raster"]: f.append("kante")
            if m["planaritaet"] > 0.5 * i.T: w.append("planaritaet")
        else:
            r = R["kleinschutt"]
            if m["e_dicke"] < r["e_dicke"]: f.append("eingrab")
            if m["luecke_max"] > r["luecke"] + tol["raster"]: f.append("luecke")
            if m["deckung"] < r["deckung"]: f.append("deckung")
            if m["winkel"] > r["winkel"]: f.append("winkel")
            if m["kante_frei"] > 0.5 * i.T + 0.02 + tol["raster"]: f.append("kante")
            if m["planaritaet"] > 0.4 * i.T: f.append("planaritaet")
            if m["hang"] > r["hang"]: f.append("hang")
    if k in ("fels", "stein", "kiesel") and m["nass_anteil"] >= 0.5:  # im Wasser: echtes Bett, kein Dump-Boden
        if m["luecke_max"] > tol["wasser"] + tol["raster"]: f.append("treiben")
        c = i.mitte(); wz = welt.nass(c[0], c[1])
        if wz is not None:
            ueber = m["oben_z"] - wz
            if ueber > 0 and i.L < 0.4 and wz - welt.H(c[0], c[1]) >= 0.08: f.append("auftauchen_klein")
            if ueber > 0.6 * m["h_welt"]: f.append("auftauchen")
            if abs(ueber) < tol["spiegelrand"]: w.append("spiegelrand")
    return sorted(set(f)), w, m

def ausbiss_gruppen(insts, welt):
    """Erklaerte Ausbiss-Rollen: >= 3 Platten im Radius 6 m mit gleicher Fallrichtung/-winkel, Hang >= 30, >= 50 % verborgen."""
    A = R["ausbiss"]; kand = []
    for i in insts:
        if i.klasse != "platte" or i.rolle not in AUSBISS_ROLLEN or i.T < A["dicke"]: continue
        m, _, _ = messe(i, welt, insts)
        mid = i.gitter((i.bmin[2] + i.bmax[2]) / 2, 7)
        verborgen = sum(1 for p in mid if p[2] < welt.H(p[0], p[1])) / len(mid)
        n = i.ax[i.k_duenn]; n = n if n[2] > 0 else v_mul(n, -1)
        fallen = math.degrees(math.acos(n[2])); richtung = math.degrees(math.atan2(n[1], n[0]))
        if m["hang"] >= A["hang"] - 0.5 and verborgen >= A["verborgen"]: kand.append((i, fallen, richtung))
    ok = set()
    for i, fa, ri in kand:
        c = i.mitte(); grp = [j for j, fb, rj in kand if math.dist(c[:2], j.mitte()[:2]) <= A["radius"]
               and abs(fa - fb) <= A["fallen"] and abs((ri - rj + 180) % 360 - 180) <= A["richtung"]]
        if len(grp) >= A["n"]: ok.add(i.nr)
    return ok

def farbe(rgb_lin):
    Y = 0.2126 * rgb_lin[0] + 0.7152 * rgb_lin[1] + 0.0722 * rgb_lin[2]
    s = [1.055 * c ** (1 / 2.4) - 0.055 if c > 0.0031308 else 12.92 * c for c in rgb_lin]
    mx, mn = max(s), min(s); sat = 0.0 if mx == 0 else (mx - mn) / mx
    if mx == mn: h = 0.0
    elif mx == s[0]: h = (60 * ((s[1] - s[2]) / (mx - mn))) % 360
    elif mx == s[1]: h = 60 * ((s[2] - s[0]) / (mx - mn)) + 120
    else: h = 60 * ((s[0] - s[1]) / (mx - mn)) + 240
    F = R["farbe"]
    if F["orange_h"][0] <= h <= F["orange_h"][1] and sat >= F["orange_s"]: return "FEHLER", "orange", round(Y, 3)
    if Y >= F["weiss_Y"]: return "WARNUNG", "weiss", round(Y, 3)
    if sat > F["s_max"] or not (F["Y"][0] <= Y <= F["Y"][1]): return "WARNUNG", "palette", round(Y, 3)
    return "ok", "grau", round(Y, 3)

KLEINSCHUTT = ("RockyGround", "BeachSandWithPebbles", "DryRiverBed", "GroundPatch", "ground_patch")
HOLZ = {"stumpf": ("Stump", "stump"), "wurzel": ("Roots", "roots", "root_", "Root_"),
        "holz": ("Branch", "branch", "bark_debris", "log", "Log", "Fallen", "Trunk", "trunk", "driftwood")}

def klasse_aus(netz, ext):
    """Klasse aus Name und Ausdehnung (m, mit Skala); Reihenfolge wie steine_sitz_regeln.json 'erkennung'."""
    T, B, L = sorted(ext)
    if any(m in netz for m in HOLZ["stumpf"]): return "totholz_stumpf"
    if any(m in netz for m in HOLZ["wurzel"]): return "totholz_wurzel"
    if any(m in netz for m in HOLZ["holz"]): return "totholz_stamm" if (L >= 2.0 and B >= 0.2) else "totholz_ast"
    if any(m in netz for m in KLEINSCHUTT) or (T / L <= 0.12 and L >= 1.5 and T <= 0.35): return "kleinschutt"
    if T / B <= 0.35 and L >= 0.3: return "platte"
    return "fels" if L >= 1.0 else ("stein" if L >= 0.3 else "kiesel")

def v2_schwebend(i, welt):  # alte Regel: Unterkante ueber dem hoechsten von 5 Bodenpunkten + 5 cm
    e = i.ecken(); c = i.mitte(); pts = [(p[0], p[1]) for p in e[0::2]][:4] + [(c[0], c[1])]
    return min(p[2] for p in e) > max(welt.H(x, y) for x, y in pts) + 0.05

def pruefe(insts, welt):
    durch = {}
    for a in range(len(insts)):
        for b in range(a + 1, len(insts)):
            A, B = insts[a], insts[b]
            if A.klasse.startswith("totholz") or B.klasse.startswith("totholz"): continue
            tiefe = obb_durchdringung(A, B)
            if tiefe <= 0: continue
            rel = tiefe / min(A.T, B.T); wk = winkel(A.ax[A.k_duenn], B.ax[B.k_duenn])
            beide_platte = A.klasse in ("platte", "kleinschutt") and B.klasse in ("platte", "kleinschutt")
            schlecht = (beide_platte and wk >= R["stapel"]["kreuz_winkel"] and rel > R["stapel"]["kreuz_anteil"]) or \
                       (not beide_platte and rel > R["stapel"]["durch_block"] and min(A.L, B.L) >= 0.3)
            if schlecht: durch.setdefault(A.nr, []).append(B.nr); durch.setdefault(B.nr, []).append(A.nr)
    ausb = ausbiss_gruppen(insts, welt); out = {}
    for i in insts:
        if i.klasse == "platte" and i.nr in ausb: out[i.nr] = ("ok", [], ["ausbiss"]); continue
        f, w, _ = urteil(i, welt, insts)
        if i.nr in durch: f = sorted(set(f) | {"durchdringung"})
        if i.farbe is not None:
            fu, art, _ = farbe(i.farbe)
            if fu == "FEHLER": f = sorted(set(f) | {"farbe_" + art})
            elif fu == "WARNUNG": w = w + ["farbe_" + art]
        out[i.nr] = ("FEHLER" if f else ("WARNUNG" if w else "ok"), f, w)
    return out

# ---------------- synthetischer Selbsttest (Sollwerte von Hand festgelegt, nicht mit diesem Code erzeugt) ----------------
def gelaende(x, y):
    if y < 10: return 10.0                                     # flach
    if y < 20: return 10.0 + math.tan(math.radians(30)) * min(x, 6.0)   # 30-Grad-Hang bis x = 6, dann Terrasse (konvexer Knick)
    if x < 9 or x > 13: return 10.0                            # Bach: Ufer 10,0, Boeschung 9-10 und 12-13, Bett 10-12 auf 9,0
    if x < 10: return 10.0 - (x - 9)
    if x > 12: return 9.0 + (x - 12)
    return 9.0

def selbsttest():
    H = Raster(gelaende, 41, 41)
    welt = Welt(H, lambda x, y: 9.3 if (y >= 20 and 8.0 <= x <= 14.0) else None, lambda x, y: (0.0, 1.0))  # Spiegel 9,3, Fluss +y
    t30 = math.tan(math.radians(30)); P = ((-0.6, -0.4, 0.0), (0.6, 0.4, 0.16))   # Platte 1,2 x 0,8 x 0,16, Pivot unten Mitte
    S = ((-1.5, -1.5, 0.0), (1.5, 1.5, 0.25)); ST = ((-0.25, -0.2, 0.0), (0.25, 0.2, 0.35))
    BL = ((-0.6, -0.5, 0.0), (0.6, 0.5, 0.8)); KI = ((-0.06, -0.05, 0.0), (0.06, 0.05, 0.07))
    LOG = lambda L: ((-L / 2, -0.15, 0.0), (L / 2, 0.15, 0.3))
    I = []
    def add(nr, kl, pos, rot, bb, rolle="", farbe=None): I.append(Inst(nr, "SM_Test_" + kl, pos, rot, 1.0, bb[0], bb[1], kl, rolle, farbe))
    add("F1", "platte", (3, 3, 10.0 - 0.08), (0, 0, 0), P)
    lo = 0.6 * math.sin(math.radians(25))                             # tiefste Ecke beruehrt den Boden
    add("F2", "platte", (8, 3, 10.0 + lo), (25, 0, 0), P)
    add("F3", "platte", (13, 3, 10.10), (0, 0, 0), P)
    n30 = (-math.sin(math.radians(30)), 0, math.cos(math.radians(30)))
    p4 = v_sub((4.0, 12.0, 10 + t30 * 4.0), v_mul(n30, 0.08)); add("F4", "platte", p4, (30, 0, 0), P)
    p5 = v_sub((6.0, 15.0, 10 + t30 * 6.0), v_mul(n30, 0.08)); add("F5", "platte", p5, (30, 0, 0), P)
    add("F6", "kleinschutt", (20, 4, 10.0 - 0.125), (0, 0, 0), S)
    p7 = v_sub((6.0, 17.5, 10 + t30 * 6.0), v_mul(n30, 0.125)); add("F7", "kleinschutt", p7, (30, 0, 0), S)
    add("F8", "stein", (25, 3, 10.0 - 0.14), (0, 0, 0), ST)
    add("F9", "stein", (27, 3, 10.06), (0, 0, 0), ST)
    top4 = v_add(p4, v_mul(n30, 0.16)); add("F10", "kiesel", v_add(top4, v_mul(n30, -0.005)), (30, 0, 0), KI)
    add("F11a", "fels", (31, 3, 10.0 - 0.28), (0, 0, 0), BL); add("F11", "stein", (31, 3, 10.52), (0, 0, 0), ST)
    add("F12a", "fels", (35, 3, 10.0 - 0.28), (0, 0, 0), BL); add("F12", "stein", (35.65, 3, 10.52), (0, 0, 0), ST)
    add("F13a", "platte", (3, 7, 10.0 - 0.08), (0, 0, 0), P); add("F13", "platte", (3, 7, 10.0 - 0.3), (40, 0, 0), P)
    add("F14", "totholz_stamm", (11, 25, 10.0), (0, 0, 0), LOG(6.0))
    add("F15", "totholz_stamm", (9.5, 30, 10.0), (0, 0, 0), LOG(4.0))
    add("F16", "stein", (11, 28, 9.05), (0, 0, 0), ST)
    add("F17", "stein", (11, 33, 9.0 - 0.24), (0, 0, 0), ((-0.4, -0.35, 0.0), (0.4, 0.35, 0.6)))
    SU = ((-0.4, -0.4, 0.0), (0.4, 0.4, 0.9))
    add("F18", "totholz_stumpf", (37, 7, 10.0 - 0.1), (20, 0, 0), SU)
    add("F19", "totholz_stumpf", (39, 7, 10.0 - 0.1), (0, 0, 0), SU)
    AB = ((-0.6, -0.4, 0.0), (0.6, 0.4, 0.2))                           # Ausbiss-Platte 1,2 x 0,8 x 0,2
    for k, y in enumerate((11.5, 13.0, 14.5)):
        add("F20" + "abc"[k], "platte", (2.0, y, 10 + t30 * 2.0 - 0.1), (70, 0, 0), AB, rolle="band")
    add("F21", "platte", (2.0, 18.0, 10 + t30 * 2.0 - 0.1), (70, 0, 0), AB, rolle="")
    # Dachziegel im Bett (Fluss +y): lokale X -> +y (Yaw 90), Pitch +15 hebt das stromab-Ende; stromauf-Haelfte im Bett
    PZ = ((-0.5, -0.3, 0.0), (0.5, 0.3, 0.1))
    add("F22", "platte", (11, 37, 9.0 - 0.02), (15, 90, 0), PZ)
    add("F23", "platte", (11, 39.0, 9.0 - 0.02), (-15, 90, 0), PZ)
    ell = [(0.25 * math.cos(a) * math.sin(b), 0.2 * math.sin(a) * math.sin(b), 0.175 - 0.175 * math.cos(b))   # Ellipsoid-Punktwolke,
           for a in [k * math.pi / 18 for k in range(36)] for b in [k * math.pi / 24 for k in range(25)]]      # tiefster Punkt im Pivot
    I.append(Inst("F25", "SM_Test_PW", (30, 7, 10.0 - 0.35 * 0.35), (0, 0, 0), 1.0, ST[0], ST[1], "stein", punkte=ell))
    I.append(Inst("F26", "SM_Test_PW", (33, 7, 10.04), (0, 0, 0), 1.0, ST[0], ST[1], "stein", punkte=ell))
    add("F24g", "stein", (20, 7, 10.0 - 0.14), (0, 0, 0), ST, farbe=(0.12, 0.12, 0.11))
    add("F24o", "stein", (22, 7, 10.0 - 0.14), (0, 0, 0), ST, farbe=(0.30, 0.12, 0.04))
    add("F24w", "stein", (24, 7, 10.0 - 0.14), (0, 0, 0), ST, farbe=(0.55, 0.55, 0.52))
    soll = {  # (Urteil, Pflichtfehler) - von Hand aus der Geometrie abgeleitet
        "F1": ("ok", []), "F2": ("FEHLER", ["luecke", "winkel", "kante"]), "F3": ("FEHLER", ["luecke"]),
        "F4": ("ok", []), "F5": ("FEHLER", ["luecke", "kante"]), "F6": ("ok", []), "F7": ("FEHLER", ["planaritaet", "kante"]),
        "F8": ("ok", []), "F9": ("FEHLER", ["luecke", "eingrab"]), "F10": ("FEHLER", ["traeger_neigung"]),
        "F11a": ("ok", []), "F11": ("ok", []), "F12a": ("ok", []), "F12": ("FEHLER", ["schwerpunkt", "luecke"]),
        "F13a": ("FEHLER", ["durchdringung"]), "F13": ("FEHLER", ["durchdringung", "winkel"]),
        "F14": ("ok", []), "F15": ("FEHLER", ["schwerpunkt"]), "F16": ("FEHLER", ["treiben"]), "F17": ("ok", []),
        "F18": ("FEHLER", ["stumpf_achse"]), "F19": ("ok", []),
        "F20a": ("ok", []), "F20b": ("ok", []), "F20c": ("ok", []), "F21": ("FEHLER", ["winkel"]),
        "F22": ("ok", []), "F23": ("FEHLER", ["winkel"]),
        "F25": ("ok", []), "F26": ("FEHLER", ["luecke"]), "F24g": ("ok", []), "F24o": ("FEHLER", ["farbe_orange"]), "F24w": ("WARNUNG", []),
    }
    erg = pruefe(I, welt); fehl = []
    for nr, (u, pf) in soll.items():
        iu, f, w = erg[nr]
        if iu != u or any(p not in f for p in pf): fehl.append((nr, u, pf, iu, f, w))
    netze = {"SM_NordicBeachRockyGround_02": ((3.51, 3.43, 0.25), "kleinschutt"), "SM_ForestRockSlab_01": ((7.15, 3.45, 0.66), "platte"),
             "texndcpda_tier_0": ((0.95, 1.34, 0.28), "platte"), "SM_flat_rock_02": ((3.99, 3.22, 0.86), "platte"),
             "SM_mountain_rock_big_02_1": ((4.73, 4.51, 2.62), "fels"), "SM_mountain_rock_small_01_1": ((0.47, 0.52, 0.19), "stein"),
             "SM_SmallStonesPack_01": ((0.26, 0.18, 0.16), "kiesel"), "SM_FallenSpruceTree_01": ((7.3, 1.94, 0.9), "totholz_stamm"),
             "SM_OldTreeBranch_02": ((6.84, 0.6, 0.27), "totholz_stamm"), "SM_branch_01_1": ((1.24, 0.22, 0.12), "totholz_ast"),
             "SM_BirchTreeStump_01": ((0.63, 0.53, 0.9), "totholz_stumpf"), "SM_ForestRoots_01": ((2.36, 1.58, 0.22), "totholz_wurzel")}
    for n, (e, k) in netze.items():
        if klasse_aus(n, e) != k: fehl.append(("klasse", n, klasse_aus(n, e), k))
    v2 = {i.nr: v2_schwebend(i, welt) for i in I if i.nr in ("F2", "F3")}
    if v2 != {"F2": False, "F3": True}: fehl.append(("v2", v2))
    for z in fehl: print("ABWEICHUNG", z)
    sig = hashlib.sha256(json.dumps({k: [v[0], v[1], v[2]] for k, v in sorted(erg.items())}, sort_keys=True).encode()).hexdigest()[:16]
    for nr in sorted(erg, key=lambda s: (int(''.join(c for c in s[1:] if c.isdigit())), s)):
        print("%-5s %-8s %s %s" % (nr, erg[nr][0], ",".join(erg[nr][1]) or "-", ("(" + ",".join(erg[nr][2]) + ")") if erg[nr][2] else ""))
    print("v2 schwebend: F2 %s (Platte 25 Grad mit Bodenecke), F3 %s" % (v2["F2"], v2["F3"]))
    print(("SELBSTTEST OK" if not fehl else "SELBSTTEST FEHLGESCHLAGEN") + "  Regeln 23.1  Faelle %d  Signatur %s" % (len(soll), sig))
    return not fehl

def lade_regeln(pfad):
    with open(pfad, encoding="utf-8") as fh: j = json.load(fh)
    k = j["klassen"]; t = j["toleranzen"]
    R["tol"].update(kontakt=t["kontakt_m"], wasser=t["wasser_m"], raster=t["raster_zuschlag_stufe_a_m"], kern=t["kern_ellipse"], spiegelrand=t["spiegelrand_m"])
    for kl, r in (("fels", k["fels"]), ("stein", k["stein"]), ("kiesel", k["kiesel"])):
        R[kl].update(e=(r["eingrab_hoehe"]["fehler_unter"], r["eingrab_hoehe"]["fehler_ueber"]), deckung=r["deckung_min"], winkel=r["winkel_normale_max"],
                     winkel_TL=r["winkel_gilt_wenn_T_durch_L_unter"], luecke=r["luecke_max_m"]["kern_stufe_a"],
                     luecke_pw=r["luecke_max_m"].get("punktwolke", r["luecke_max_m"].get("punktwolke_bergseite")))
    R["platte"].update(e_dicke=k["platte"]["eingrab_dicke"]["fehler_unter"], deckung=k["platte"]["deckung_min"]["stufe_a"], winkel=k["platte"]["winkel_normale_max"])
    ks = k["kleinschutt"]
    R["kleinschutt"].update(e_dicke=ks["eingrab_dicke"]["fehler_unter"], luecke=ks["luecke_max_m"], deckung=ks["deckung_min"], winkel=ks["winkel_normale_max"], hang=ks["hang_max_grad"])

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--selbsttest", action="store_true"); ap.add_argument("--regeln")
    a = ap.parse_args()
    if a.regeln: lade_regeln(a.regeln)
    if a.selbsttest: raise SystemExit(0 if selbsttest() else 1)
    ap.print_help()
```

---

## 14. Pilot T23-C2 und Ausweitung (Frage 9)

### 14.1 Rahmen

- **Gesamtauftrag:** 23 (Platzierung PLZ-2026-10).
- **Test-IDs:** T23-0 (Messweg), T23-1 (Trockenlauf C2 und Vergleichsstellen, nur lesend), T23-2 (Reparatur C2 s 389–580).
  Ausgangsstand-ID wird lokal vergeben. Stand `vorbereitet → angewendet → geprüft`.
- **Fenster:**
  - C2, Talkaskade s 389–580, Bett plus beide Ufer bis 10 m hinter der Wasserkante;
  - Vergleichsstellen nach pruefung.md: Kiesbett s 579–728 (Anschluss, nur zählen), B5 (dieselben Planer felsgruppen/platten, nur zählen).
- **Feste Kameras, gleiches Licht:** `C2_t430_auge`, `C2_t500_auge`, `C2_t550_auge`, `C2_t500_schraeg`, `C2_tk_becken_auge` (20 §5), die
  drei Kameras der heutigen Bilder t430/m/t500 und neu `C2_t430_ferat` (**anzulegen**: Ferats Blick, näher als t430, bachauf).
  Vorher und nachher.
- **Messweg:**
  - Stufe A für alle Instanzen.
  - Stufe B (Punktwolke) für alle gemeldeten und 10 % der bestandenen.
  - Stufe C: Line-Trace im Editor an 40 Instanzen (20 gemeldet, 20 bestanden), dazu je ein Screenshot von oben und von der Seite.

### 14.2 Erfolg (alle Punkte)

1. **Messweg (T23-0):**
   - Selbsttest lokal mit Signatur `64a654746495eca8`.
   - K1–K16: 0 Urteilsabweichungen; Lücke und Eingraben gegen den Line-Trace ± 1 cm.
2. **Trockenlauf (T23-1):**
   - Stufe A gegen Stufe C an den 40 Stichproben: Lücke Median ≤ 2 cm, p95 ≤ 5 cm.
   - Fehlalarm: von 20 gemeldeten sind ≥ 18 im Bild falsch, von 20 bestandenen ≥ 19 im Bild in Ordnung.
   - Treffer: an jedem der 8 Kreise in `C2_t430_ferat` mindestens eine gemeldete Instanz. Ein Kreis, der sich nicht verorten lässt, wird benannt.
3. **Formal nach T23-2:**
   - Im Fenster 0 FEHLER der Klassen Platte, Kleinschutt, Totholz und Farbe-orange.
   - Für Stein/Fels ≤ 2 % FEHLER, die nur in Stufe A anschlagen und auf Stufe B warten.
   - WARNUNG ≤ 5 %.
   - Sicherungszeilen = geänderte + entfernte Instanzen; 1-%-Rücknahme transformgleich; Speicherbeleg je Paket; neuer Zensus stimmt mit dem
     Protokoll überein.
4. **Bestand:**
   - Entfernt ≤ 25 % der Stein-, Platten- und Holzinstanzen im Fenster.
   - Uferband 0–3 m 3D-Bedeckung weiter ≥ 0,65 (20). Andernfalls wird der Fehlbetrag als Neuplanungs-Auftrag gelistet.
   - Kein XY an SWR-Hindernissen.
5. **Bild (gleiche Kameras):**
   - keine Platte wie ein Brett, außer erklärtem Ausbiss;
   - keine schwebende Platte oder Kies-Fläche;
   - kein oranger oder weißer Stein im Wasser;
   - Stamm mit beiden Enden auf dem Ufer oder entfernt;
   - kein Gras durch Platten;
   - das Kiesbett s 579–728 ist unverändert.

   Technischer und visueller Befund werden getrennt festgehalten.

### 14.3 Abbruch

| Bedingung | Folge |
|---|---|
| T23-0: eine Urteilsabweichung oder Line-Trace-Differenz > 1 cm | kein Projektlauf; Messweg klären |
| T23-1: ≥ 3 von 20 Fehlalarmen oder Stufe-A-p95 > 5 cm | Grenzen bzw. Kern-Ellipse kalibrieren, keine Reparatur |
| eine Planerschicht > 30 % FEHLER einer Klasse | diese Schicht nicht einzeln reparieren; Planer nach §11 ändern und neu setzen (§10.3); die übrigen Schichten laufen weiter |
| Reparatur würde SWR-Hindernisse in XY ändern oder entfernen | diese Instanzen zurückstellen; eigener Schritt mit Hindernis-Neubau, Reset, Bake |
| Wasserstand nicht gespeichert (T6N1 offen) | Wasser-Klassen (treiben, herausragen) nicht reparieren, nur zählen |
| Speichern scheitert oder der neue Zensus weicht ab | aus der Sicherung zurückspielen, melden |
| Vergleichsstelle Kiesbett verschlechtert sich im Bild | Änderung zurücknehmen, Ursache eingrenzen |

### 14.4 Ausweitung auf die Welt

| Stufe | Inhalt | Kriterien |
|---|---|---|
| **W0** | v4 Trockenlauf über alle 70 Felder, nur lesend: Feld × Klasse × Planerschicht × Fehlerart | Laufzeit und Zahlen gemeldet; Schichten > 30 % gehen auf die Neuplanungsliste |
| **W1: 3 Felder** | **B5** (fest: Ferats B5-Themen, felsgruppen/platten/halde/baumgruppen) und die zwei Felder mit den meisten FEHLERN außerhalb C2/B5, eines aus Fels/Platte/Kleinschutt und eines aus Totholz/Wasser | wie Pilot 14.2 Punkte 2–5, je Feld 10 gemeldete und 10 bestandene Instanzen im Bild |
| **W2: Rest** | Bündel ≤ 10 Felder, das nächste erst nach formal bestandenem Vorgänger | FEHLER 0 außer Sperren und erklärten Ausnahmen; WARNUNG ≤ 5 %; Entfernt ≤ 15 % je Feld, darüber Einzelprüfung; je Feld 5 automatische Bildpaare (oben/seitlich), von der Projektleitung angesehen |
| **W3: Nachprüfung** | v4 erneut über alle 70 Felder nach Abschluss und nach jedem späteren Planerlauf | 0 neue FEHLER; neue Fälle führen zur Planerkorrektur, nicht zur Reparaturschleife |

**Reihenfolge:** Planer, die später neu laufen (§11), werden vor W2 geändert. Die Einzelreparatur gilt nur für Schichten ohne Neulauf.

---

## 15. Nächste Handlung (genau eine, lokal)

**T23-0 Messweg der Prüfung v4.**
- **Zuständig:** Rolle 1 (Prüfung) und Projektleitung (Testlevel im Editor). Budget ≈ 60 min.
- **Schritte:**
  1. `python -I sitz_pruefung.py --selbsttest --regeln recherche/antworten/steine_sitz_regeln.json` lokal ausführen.
  2. Im vorhandenen kleinen Testlevel K1–K16 aus §12.2 setzen; sonst eine Ebene, eine 30°-Rampe mit Kante, einen 2-m-Graben und ein
     Becken mit festem Spiegel ergänzen.
  3. Zensus der Testinstanzen ziehen und v4 darauf laufen lassen.
  4. Je K Lücke und Eingraben unabhängig per Line-Trace ablesen.
  - Projektdaten werden nicht geändert.
- **Erfolgskriterium:** Signatur `64a654746495eca8`, 16/16 Urteile wie Soll, Line-Trace-Differenz ≤ 1 cm.
  Danach folgt T23-1 (Trockenlauf C2).
- **Abbruch:** abweichende Signatur oder ein falsches Urteil. Dann Ursache melden (Achsenkonvention, Pivot, Einheiten), keinen Projektlauf.

**Rückfragen:** keine, die T23-0 verändern.

---

## Was fehlt bis Witcher 4

Messlatte wie 6e: dichte, verzahnte Ufer bis an die Kante, weiches Licht, klare Wasserformen. Die Techdemo ist nur über Suchauszüge belegt.
Nach Wirkung:

1. **Kein Teil darf schweben, stehen oder treiben.** Das ist die Grundlage aller weiteren Punkte und Gegenstand dieser Antwort.
   Ferats Bild zeigt: Ein einziges Brett im Bild zerstört die Glaubwürdigkeit des ganzen Ufers.
2. **Übergang Stein–Boden im Material:**
   - RVT-Fuß für alle Steinmaterialien (`MF_EL_RVT_Fuss` anzulegen);
   - Nasslinie auch in `M_Master_material`;
   - Moos oben, Algen unten;
   - Kontaktschatten durch Begleitsteine und Gras in den Ritzen (20).
3. **Ein Gestein je Abschnitt:** grauer Granit/Gneis ohne Fremdfarben. Orange nur als Patina an Sickerstellen.
4. **Strömungslesbares Bett:** Dachziegel-Lage an Schnellen, Keystones an den Lippen, Kleinzeug dunkel auf dem Grund. Dazu die
   Wasserentscheidung aus 6o.
5. **Totholz mit Geschichte:** wenige Brücken und Rampen, bemoost, Teller am Ufer; in der Tundra fast keines.
6. **Eine Quelle der Wahrheit statt Nachreparatur** (wie 22 §9): Planer und spätere PCG lesen dieselbe Sitzprüfung. In der Demo entsteht
   Kleinzeug zur Laufzeit aus Gelände- und Biomdaten [S, 22].
7. **Assets:** Für steile Hänge fehlen dünne Kies- und Schuttdecals bzw. Lagen statt dicker Schutt-Netze. `M_MS_Decal` ist da; Netze aus
   dem freien Bestand vor jedem Kauf.

---

## Quellen (abgerufen 18.10.2026)

**Zugriff:**
- WebFetch scheiterte mit DNS-Fehler bei `en.wikipedia.org`, `people.wou.edu`, `esurf.copernicus.org`, `dev.epicgames.com` und `80.lv`.
- Alle Fachaussagen unten stammen deshalb aus **Suchauszügen [S]**. Keine Vollseite wurde gelesen.
- Zahlen sind als Größenordnung übernommen, nicht als geprüfte Zitate.

**Imbrikation:**
- [Galvin 2002, GSA Annual Meeting](https://gsa.confex.com/gsa/2002AM/webprogram/Paper45012.html) [S] – a-b-Ebenen von Bachgeröll neigen meist stromauf.
- [Gravel fabric in a sub-Himalayan braided stream (IAS)](https://repository.ias.ac.in/67306) [S] – mittlere AB-Neigung 22,6–37,6°, Streuung 8–14°, starke Imbrikation stromauf.
- [Schlunegger & Garefalakis 2018, ESurf 6, 743](https://boris.unibe.ch/119827/1/esurf-6-743-2018.pdf) [S] – Imbrikation in Alpenbächen, Strömungsbedingungen.
- Auszug ohne eindeutige Zuordnung: Median ≈ 35° Wasserschotter, ≈ 47° Debris-Flood, ≈ 65° Murgang (1 007 Klasten) [S].

**Halde:**
- [Wikipedia: Scree](https://en.wikipedia.org/wiki/Scree) [S] – konkav, Maximalneigung = Schüttwinkel der mittleren Korngröße.
- [Wikipedia: Angle of repose](https://en.wikipedia.org/wiki/Angle_of_repose) [S].
- [Francou & Manté, IRD](https://horizon.documentation.ird.fr/exl-doc/pleins_textes/divers19-08/010048761.pdf) [S] – nähert sich 35°.
- [Tuckerman Ravine, Univ. Michigan](https://deepblue.lib.umich.edu/bitstream/2027.42/25798/1/0000360.pdf) [S] und
  [Montana Talus](https://scholarworks.montana.edu/bitstreams/e54f20bf-a5b1-4470-9b4e-ac4d91ab8d89/download) [S] – Blöcke bevorzugt hangabwärts ausgerichtet.

**Step-Pool und Keystones:**
- [ESurf-Preprint 2020-30](https://esurf.copernicus.org/preprints/esurf-2020-30/esurf-2020-30.pdf) [S] – Verkeilen an Engstellen, Stabilität hängt an großen Blöcken.
- [NTNU, Vekveselva](https://ntnuopen.ntnu.no/ntnu-xmlui/handle/11250/2507304) [S] – Keystone-Größe korreliert mit der Stufenhöhe.

**Einbettung:**
- [WV DEP Habitat Assessment](https://dep.wv.gov/WWE/getinvolved/sos/Pages/SOPhabitat.aspx) [S].
- [USACE ERDC TN-EMRRP-SR-36](https://apps.dtic.mil/sti/pdfs/ADA434902.pdf) [S].

**Totholz:**
- [Jones, Daniels & Powell 2011, fRI Research](https://friresearch.ca/resource/abundance-and-function-large-woody-debris-small-headwater-sterams-rocky-mountain-foothills) [S] – Klassen Brücke, Teilbrücke, lose, vergraben.
- [BC Water Tool, Logs über kleinen Bächen](https://www.bcwatertool.ca/info-sources/coast/result.php?q=NTk%3D) [S] – meist senkrecht zum Gerinne, lange über dem Bach.
- [IOP Kraków, Karpatenbach](https://www.iop.krakow.pl/pobierz-publikacje,1869) [S] – Rekrutierung durch Ufererosion/Windwurf; Länge/Breite bestimmt die Verankerung.
- [Minnesota BWSR LWD-Formular](https://www-dev.bwsr.state.mn.us/sites/default/files/2019-09/LWD%20Field%20and%20Data%20Entry%20Form.pdf) [S] – Bridge, Ramp, Submersed, Buried.

**Farbe:**
- [Revista IPT, Fleckenbildung in Granit](https://revista.ipt.br/revistaIPT/en/article/view/126/137) [S] – Fe²⁺ umgelagert als Hydroxid.
- [USGS Alaska, orange Bäche](https://www.usgs.gov/centers/alaska-science-center/multimedia/images?page=10) [S].
- [ZOBODAT, Hochgebirgsbäche](https://www.zobodat.at/pdf/BERI_91_0007-0042.pdf) [S] – Algen, Flechten, Moos auf Bachsteinen.

**Unreal und Gestaltung:**
- [Epic Python API FoliageType](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/FoliageType) [S] – Align to Normal, Align Max Angle, Random Pitch, Z Offset.
- [Epic Virtual Texturing](https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-texturing-in-unreal-engine) [S] und
  [RVT Quick Start](https://dev.epicgames.com/documentation/en-us/unreal-engine/runtimevirtual-texturing-quick-start-in-unreal-engine) [S] – Landschafts- und Objektblend.
- [Polycount, RVT-Blend](https://polycount.com/discussion/comment/2711284) [S].
- [UE-5.8-Forum, RVT nur Grundfarbe](https://forums.unrealengine.com/t/runtime-virtual-texture-only-outputs-landscape-base-color-instead-of-painted-landscape-layers-ue-5-8/2739603) [S].
- [Landscape Architect, Rockin' a Hard Place](https://landscapearchitect.com/landscape-articles/rockin-a-hard-place) [S] – Fels ⅓–½ eingraben, Unterteil unsichtbar.
- Ein Spiele-Breakdown mit Zahlen zum Eingraben fand ich nicht. „⅓ eingegraben“ ist hier Gestaltungswert und Projektregel (20, felsgruppen),
  keine Quelle.

**Repo:** siehe Bezugsliste oben.
