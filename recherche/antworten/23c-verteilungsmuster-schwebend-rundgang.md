# Antwort 23c – Verteilungsmuster, Ringe, hängende Eiszapfen und Fremdfarbe: ein Regelsatz 23.3 mit 23 und 23b

Gelesen: recherche/auftraege/23c-verteilungsmuster-schwebend-rundgang.md @ 9a1f7cdc2df71225a5aaead70ad27cd7d0f68f71 (Commit 7f5f317)

Stand 18.10.2026. Bearbeiter: Cloud-Recherche. Nachtrag zu 23 (Sitz) und 23b (Wiederholung, Material).
**Im Projekt ist hier nichts geprüft oder angewendet.** Der Code in §10 lief nur synthetisch in der Cloud.

**Lieferung:**
- dieses Dokument;
- `recherche/antworten/steine_sitz_regeln.json` auf **23.3**: nur Zusätze, Liste unter `aenderungen`;
- Prüfcode `verteilung_23c.py` in §10. `sitz_pruefung.py` (23) und `wiederholung_23b.py` (23b) bleiben unverändert.

**Bezug (Commit 7f5f317), gelesen:**
- `antworten/23-steine-organisch-im-boden.md` @ e59924ba88b1e24579646389eb5e843cffd657e4 (§1–§15), `antworten/23b-wiederholung-spiegeln-weisse-steine.md`
  @ 8437f810b1963f0953fa84e156e3d1d1262de0d5, `antworten/steine_sitz_regeln.json` (23.2) @ 06de88121a8a240792cdefada114fbcb1b43e900,
  `vorlagen/pruefung.md` @ 5daf4a9187ba35288dc4838f9461118e0960d068.
- Planer: `skripte/felsgruppen_plan.py` @ be2a3fe40cd3bedd3dd2eeaebaf76707cf41e4b5, `felsgruppen_regeln.json` @ ca1138e677915061897f96b0d710caa04bb1716e,
  `lava_plan.py` @ 347754e80da7d0b65be202d9b085d50cb5670e9d, `lava_regeln.json` @ 173892c9609671dea0d3bba7f787164456af544e,
  `spuren_plan.py` @ 18fdcaee12ba8d1b782a8422230587eef4855b64, `hochgebirge_plan.py` @ 5b1e2fcecf6f58a762244df149d74797dc1f65b6,
  `hochgebirge_regeln.json` @ 18e2118abbb924414fb7f96a699bc0348a13851b, `wueste_ergaenzung_regeln.json` @ 616f920de90688e78f8ff1cd0ab72cce390cfbb6.
- Daten: `vorlagen/daten/netze_masse.json` @ c337d5bb6082f7098e05738dde6596557f0de386, `material_parameter.json`
  @ 16d1511f96f8e01fa2bfcf71042b912b638a2b54, `fluss_sim/p2_lokal/fels_ms_lesen.json` @ 8267f9aaff81e36d496760687c4249ba11c1a6f4.
- Begriffe aus `20-detailgrad-bachufer-felsen.md` @ 6d1b2572…, `21-detailgrad-landschaft-felsdeckung.md` @ 32f30173…,
  `bildkritik-witcher-messlatte.md` @ f839cd35….
- Bilder, alle neun selbst angesehen: `bilder/platzierung/lage4/` (B5_08 04248d61, B5_27 2b9d9b64, C2_01 bea49cea, C2_02 dff063a7, C5_16 a39ba09c,
  C6_28 174b3583, C6_34 81928b11, E2_24 837ee3be, H3_17 586411d2).

**Kennzeichnung:** [V] Vollseite gelesen · [S] nur Suchauszug · [Repo] Code oder Daten im Repository · [Bild] eigene Ansicht ·
[Ableitung] geschlossen, nicht belegt · [Gestaltung] Zielwert für das Witcher/RDR2-Ziel, im Pilot zu kalibrieren · **neu** bzw.
**geändert** = Änderung gegenüber 23.2.

## Kurzfazit

1. **Natürliche Verteilung (Frage 1): beantwortet; Zielwerte sind Gestaltungswerte und noch nicht kalibriert.**
   - Gemessen wird im 50-m-Fenster je Klasse und Planerschicht.
   - Kennzahlen: Clark-Evans R mit Randkorrektur nach Donnelly, Ripley L(r) − r, leere 10-m-Zellen, Streuungsindex VMR, Anteil des
     häufigsten Netzes, Größenexponent b, Ausrichtung Rbar2 und Ringdetektor.
   - R > 1,10 ist überall FEHLER. Die Zielbereiche je Biom stehen in §2.4.
2. **Ringe (Frage 2): Quellen im Code gefunden; auflösen.**
   - Am wahrscheinlichsten für C6_34 ist die Opferstätte aus `lava_regeln.json`: 8–12 Schlackenbrocken auf einem Ring mit r = 3 m.
     `spuren_plan.py` Z. 1865–1867 setzt sie mit festem Radius und gleichmäßigen Winkeln. Die Säule in der Mitte fehlt im Bild.
   - Zweite Quelle: Kieselsäume aus `felsgruppen_plan.py` Z. 3517–3551 bleiben stehen, wenn ihr Hauptstück wegfällt.
   - Erklärte Spuren-Ringe bleiben nur mit Mittelobjekt. Alle anderen Ringe werden aufgelöst (§3).
3. **Hängendes (Frage 3): beantwortet; Ursache im Planer gefunden.**
   - Die Eiszapfen werden senkrecht über dem Geländepunkt angehoben: z = Gelände + 0,85 × Höhe (`hochgebirge_plan.py` Z. 968–969).
     Der Yaw ist zufällig.
   - An einer 60°-Wand ergibt das 0,49 m Luft je Meter Zapfen. Auf Gratzellen stehen die Zapfen über der Kante. Das ist sehr
     wahrscheinlich der „Zaun am Horizont“.
   - Neue Prüfung mit Line-Traces und Ortsregel: nur unter Überhang oder an einer Simskante (§4).
4. **Fremdfarbe (Frage 4): Regel beantwortet; der Messweg für die Landschaftslagen ist anzulegen.**
   - Verglichen wird in CIELAB mit dem Untergrund am Ort (§5).
   - Reparatur: zuerst die MI-`Toenung`/`Helligkeit` im Kind-MI je Biom, dann ein Netz der Gesteinsfamilie, zuletzt entfernen.
5. **Reparatur (Frage 5): beantwortet.**
   - Entfernen kommt vor dem Versetzen. Neu gruppiert wird nur über den Planer.
   - Grenzen: höchstens 35 % je 50-m-Fenster und 15 % je Feld entfernen.
   - Gilt für mehr als 30 % der Fenster einer Schicht FEHLER, wird die Schicht neu geplant (wie 23 §10.3).
   - Die Gesamtreihenfolge aus 23, 23b und 23c steht in §6.
6. **Code: geliefert und nur synthetisch geprüft.**
   - Ergebnis zweimal und mit `--regeln`: `SELBSTTEST OK  Regeln 23.3  Faelle 14  Signatur b4ebdb213b2f71ba`.
   - 23 behält mit der 23.3-Datei `64a654746495eca8`, 23b behält `dabb50741db8b9ac`.
   - Der Ringdetektor fand in einer Zusatzserie 24 von 28 eingesetzten Ringen, bei 1 Fehlalarm in 60 Zufallsfenstern (§10).
7. **Bildbefund: zu allen neun Bildern zugeordnet (§1).** Asset-Namen sind Kandidaten, bis der Zensus sie bestätigt.

**Nächste Handlung (genau eine, lokal):** **T23c-0.** Selbsttests ausführen, dann die neun Rundgang-Stellen nur lesend messen.
Projektdaten werden nicht geändert (§12).

---

## 1. Bildbefund [Bild] und Zuordnung

| Bild (Feld) | Was ich sehe | Regel 23.3 | wahrscheinliche Quelle (zu prüfen) |
|---|---|---|---|
| C6_28 (C6; laut `wueste_ergaenzung_regeln.json` „lava 99 %“, nicht Ödland) | Dichtes Feld schwarzer Lavabrocken. Größen gemischt, aber wenige Formen; alle stehen gleich aufrecht. Flächig ohne Lücken bis zum Rand | R, leer, VMR (§2.4 lava), Netzanteil, Neigungsstreuung | `lava_plan.py` schlacke (3–8 je Gruppe, r 2,2 m, Z. 1012–1020) und felsgruppen lava (biom_faktor 1,6): Gruppenscheiben überlappen und ergeben eine Fläche |
| C6_34 (Gegenprobe) | Etwa 10 dunkle Schlackenbrocken gleichmäßig auf einem Kreis mit r ≈ 3 m, die Mitte ist leer. Helle Kiesel liegen in Bögen und sind hell auf dunklem Sand | Ring (§3), Farbe Kiesel gegen Lavasand (§5) | Opferstätte `opferstaette_steinkreis` ohne `opferstaette_saeule`. Kandidat für die hellen Kiesel: SmallStonesPack_08–14 der Lava-Klasse kiesel; laut `kiesel_ersatz_hinweis` sollen sie dunkel sein |
| C5_16 (C5: aue mit 31 % lava) | Schwarze Lavaklumpen einzeln und gleichmäßig auf grüner Wiese mit Heide | Fremdgestein (§2.3), Farbe fremd (§5) | Lava-Klassen im 30-m-Saum zur Aue (`lava_regeln` erwartung C5 „Lava-Teil + 30-m-Saum“) |
| B5_27 (Bergwald) | Etwa 30 gleich lange, gesägte Stammstücke kreuz und quer, ohne Teller und ohne Äste | Totholz-Verteilung (§2.3), Wiederholung 23.2 (Stamm ≤ 1 je 30 m) | Totholz von mittelschicht oder felsdeckung `baumgruppen_B5`; das Netz ist zu prüfen |
| B5_08 (KLIP) | Ocker-rötlicher Felsblock auf einem sehr hellen, grauweißen Hang | Farbe gleiches/fremdes Gestein (§5) | Kandidat rote Findlinge (`netz_nur_biome`: nur canyon/oedland/wueste/lava) oder ein Klippen-MI; zu prüfen |
| H3_17 (NORD, Elfenwald) | Zwei graue Felsplatten mit überlaufenden Wurzeln auf braunem Laubboden. Sie wirken „zerknüllt“, ohne Moos | Farbe fremd (§5); Sitz 23.1 Klasse `totholz_wurzel` (≤ 10°) | Kandidaten `FT_EL_NORD_MossyForestRoots_01/02` bzw. `Pine_roots_*` (Inventar); zu prüfen |
| E2_24 (E2) | Weiße, untexturierte Eiszapfen mit Querbalken stehen frei vor der Felswand. Oben an der Kante steht eine Reihe gleicher Teile gegen den Himmel | Hängend (§4), Material | `hochgebirge` Klasse eiszapfen bzw. felsgruppen `zusatzklassen.eis`; `M_Eldarien_Eis` ohne Parameter/Texturen [Repo] |
| C2_01 (DETA) | Lange Platte liegt wie ein Brett schräg über dem Ufer; Platten stehen schräg | 23.1 Platte (unverändert) | Detailgrad `platte` (23 §1.3) |
| C2_02 (P2BE) | Von oben: Uferblöcke als Reihe gleich großer Klötze in gleichem Abstand und gleicher Drehung | **neu:** Reihe (Abstands-CV) §2.3; 23.2 Wiederholung | p2bett bzw. kantenufer_p2 Uferblöcke |

Hinweis zu C6: Laut Repo ist C6 ein Lavafeld. Ödland liegt nur in den Rändern von D6 (`wueste_ergaenzung_regeln.json`, C6-Hinweis). Für C6
gelten deshalb die Ziele für lava.

---

## 2. Natürliche Verteilung (Frage 1)

### 2.1 Gestaltungsregeln

| Regel | Inhalt | Beleg |
|---|---|---|
| Gruppen und Lücken | Steine liegen in Gruppen um Ursachen: Felskopf, Wandfuß, Rinne, Uferkante, Moräne. Dazwischen liegt Freifläche. Gruppenscheiben bedecken ≤ 15 % der Fläche, Dichte mit Wertrauschen 20–60 m moduliert | [S] gleichmäßige Dichte wirkt künstlich, natürliche Bestände sind fleckig. [Repo] bildkritik: „keine Clusterung“ war Befund Nr. 1 |
| Dichteverlauf | Halde: unten mehr und größere Blöcke (Anzahl unten/oben ≥ 1,5, Median-L ≥ 1,3). Ufer: Dichte 0–3 m ≥ 2 × der Dichte 3–10 m | [S] Yosemite: Blockvolumen nimmt hangab zu. [Repo] 20 Uferband |
| gemischte Größen | Potenzgesetz N(>L) ~ L^−b mit b 1,8–3,0; Länge p90/p10 ≥ 2,5; je Gruppe ein dominantes Stück | [Repo] 20: K3 : K4 = 6–12 ≈ b 1,6–2,2; [S] Sturzvolumina folgen Potenzgesetzen |
| Netzvielfalt | im 50-m-Fenster ≥ 4 Netze je Klasse, häufigstes ≤ 35 %. Im 15-m-Fenster gilt 23.2 | [Repo] 23b §5 Familie |
| Ausrichtung | Halde: Langachsen Rbar2 ≥ 0,25, Mittel ± 25° zur Falllinie. Stämme in Windwurfgruppen gemeinsam (Rbar2 ≥ 0,4), Einzelstücke frei | [S] Halden-Fabric hangab (Alaska, Montana); Totholz [Gestaltung] |
| Neigung | Stein/Fels nicht alle gleich aufrecht: Streuung lokale Z gegen Normale ≥ 6° | [Gestaltung], Bild C6_28 |
| Fremdgestein | nur auf seinen Lagen (≥ 50 %) oder ≤ 5 m davon, als Kette am Rand | [Gestaltung], Bild C5_16 |
| Totholz | Längen gemischt (p90/p10 ≥ 2), Schnittflächen nur ≤ 30 m von Weg/Holzschlag, liegend 20–80 Stück je ha im Bergwald, FEHLER über 200 | [Gestaltung]; [S] Totholz-Studie: räumlich eher gleichmäßig über Geländeklassen, Hauptursache Wind |

### 2.2 Kennzahlen (Code §10, JSON `verteilung.kennzahlen`)

| Kennzahl | Definition | Urteil |
|---|---|---|
| Clark-Evans R | mittlerer NN-Abstand / Erwartung bei Zufall. Donnelly: E = 0,5 √(A/n) + (0,0514 + 0,0412/√n) · P/n [V spatstat-Quelle]; bei Masken mit Anteil < 0,9 Randkorrektur 5 m | R ≈ 1 zufällig, < 1 geklumpt, > 1 geordnet [S]. **FEHLER R > 1,10**; WARNUNG außerhalb des Biom-Bereichs |
| L(r) − r | L = √(K/π), K mit isotroper Randkorrektur (Kreisumfangsanteil im Fenster), r = 1, 2, 4, 8 m [S] | FEHLER „gleichmäßig“: L(1) − 1 ≤ −0,3 m und R > 1,10. WARNUNG „ohne Gruppen“: max L(r) − r (r 2–8 m) < +0,3 m |
| leer, VMR | 10-m-Zellen der Maske: Anteil leerer Zellen; Varianz/Mittel der Zellzahl | unter `leer_min`/`vmr_min` des Bioms: WARNUNG |
| Netzanteil | häufigstes Netz / n, Zahl der Netze | FEHLER > 35 % oder < 4 Netze (n ≥ 20) |
| Größe | MLE b = n / Σ ln(L/0,3 m) (kumulativ), p90/p10 | FEHLER p90/p10 < 2,5; WARNUNG b außerhalb 1,8–3,0 |
| Ausrichtung | Achsdaten, Winkel verdoppelt: Rbar2, Rayleigh-p, mittel cos 2(θ − Fall) | Halde/Windwurf siehe §2.1 |
| Reihe | Abstands-CV entlang Ufer/Wandfuß | FEHLER CV < 0,35 (Zufall ≈ 1) |
| Ring | §3.3 | FEHLER Ring, WARNUNG Bogen |

**Fenster und Mindestzahlen:**
- 50 × 50 m, Schritt 25 m, nur auf der Maske der Klasse; die Fläche A ist die Maskenfläche.
- Bänder schmaler als 15 m (Ufer, Strandwall, Wandfuß) werden längs bewertet: Reihe-CV und Dichte je 10 m, kein 2D-R.
- Mindestzahlen: Clark-Evans n ≥ 30, L(r) n ≥ 50, Netzanteil n ≥ 20, Größe n ≥ 50 (ab 0,3 m), Ausrichtung n ≥ 15 längliche Stücke
  (L/B ≥ 1,5). Darunter gilt „nicht bewertet“, nicht „bestanden“ (pruefung.md).
- Klassen: fels, stein, kiesel, totholz_stamm und „stein+fels“ (L ≥ 0,3 m), je Planerschicht und gemeinsam.

### 2.3 Neue Regeln für die Bildfälle

- **C6_28, gleichmäßiges Lavafeld:** FEHLER, wenn R > 1,10, sonst WARNUNG bei leer < 0,25 oder Neigungsstreuung < 6°. Netzanteil prüfen.
- **C5_16, Lava auf Wiese:** FEHLER `fremdgestein` außerhalb Lava-Lagen + 5 m. Dazu die Farbe fremd (§5).
- **B5_27, Stammstücke:** FEHLER bei p90/p10 < 2 oder mehr als 200 Stück je ha. Gleiches Netz > 1 je 30 m bleibt 23.2-Wiederholung.
- **C2_02, Uferblock-Reihe:** FEHLER bei Reihe-CV < 0,35.

### 2.4 Zielwerte je Biom (Stein+Fels ≥ 0,3 m, 50-m-Fenster) [Gestaltung]

| Biom | R Ziel | leer ≥ | VMR ≥ | Besonderheit |
|---|---|---|---|---|
| aue, heide, sumpf | 0,45–0,80 | 0,50 | 2,0 | Steine an Ufer, Kies, Felsköpfen; Wiese bleibt frei |
| bergwald | 0,55–0,85 | 0,35 | 1,5 | Halden-Gradient; Felsköpfe |
| elfenwald, dschungel | 0,50–0,80 / 0,50–0,85 | 0,40 | 1,5 | Gruppen an Wurzeln und Felsköpfen |
| tundra | 0,50–0,85 | 0,40 | 1,5 | Findlinge einzeln oder in Gruppen |
| gletscher | 0,65–0,95 | 0,20 | 1,2 | Moränenwälle, Blockfeld |
| canyon, oedland | 0,60–0,90 / 0,55–0,90 | 0,30 | 1,3 / 1,5 | Hangfuß, Rinnen |
| wueste | 0,60–0,95 | 0,35 | 1,3 | Kiesel-Pflaster (nur kiesel, Lage Kies) bis 1,15 |
| lava | 0,60–0,90 | 0,25 | 1,3 | Aa-Blockfeld auf Lavafels ≥ 50 % bis 1,00, leer ab 0,10 |
| frost | 0,60–0,90 | 0,30 | 1,3 | |
| kueste, fjord | 0,60–0,95 | 0,30 | 1,3 | Strandwall als Band bewerten |

Die Spanne 0,6–0,9 für Felsfelder ist Projektvorgabe aus dem Auftrag. Eine Literaturzahl für R in Blockfeldern fand ich nicht
(Suche ohne Treffer, §Quellen). Darum Kalibrierung in T23c-1 an Ferats Urteil: je Biom 3 gute und 3 schlechte Fenster.

---

## 3. Ringe (Frage 2)

### 3.1 Herkunft im Code [Repo]

| Quelle | Mechanismus | passt zu C6_34? |
|---|---|---|
| `lava_regeln.json` `spuren_overrides.zusatzklassen.opferstaette_steinkreis` + `spuren_plan.py` `sf_zusatzklassen` (ab Z. 1799), **Z. 1865–1867** | `anordnung: "ring"` → `rr = rad` (fest 3,0 m), Winkel 2πk/n ± 0,15 rad; 8–12 `SM_lava_s_rock_06/07` mit 0,35–0,55 m; max 1 je Feld. Mitte = `opferstaette_saeule` (`SM_Column_02`, Akteur, **eigene** Zusatzklasse); Punkt aus `lava_plan.py` Z. 947–958, 25 m hangab vom Spire | **ja:** Zahl, Radius, Gleichabstand, Gesteinsfarbe. Die Säule fehlt im Bild |
| `spuren_plan.py` `_ring` Z. 1478–1495 | Steinkreis r 6–11 m (Z. 1497–1515), Hügelgrab r 4–7 m (Z. 1517–1532), Opferstätte-Ensemble r 3 m (Z. 1744–1750) | erklärte Spuren |
| `felsgruppen_plan.py` `_saum` Z. 3517–3551 | Kiesel im Kranz r_m + 0,5…2,0 m um jedes große Stück (65 % hangab). `budget` (Z. 4017 ff.) dünnt Rollen getrennt aus, Kiesel nach Instanz-Hash. `netz_biom_pruefung` (Z. 3950–3986) lässt Stücke ohne Ersatz entfallen. Damit kann der Saum ohne Mitte stehen bleiben | möglich für die hellen Kieselbögen |
| `felsgruppen_plan.py` Z. 2961–2981 | Formgruppen-Satelliten am Rand der Hero-Ellipse; ohne Hero (Akteur) bleibt ein Bogen | große Stücke, nicht C6_34 |
| `lava_plan.py` Z. 1012–1020 | Gruppenglieder gleichverteilt in der Scheibe (`rad · √u`) | kein Ring |
| Foliage-Pinsel | keine Spur im Repo; die Schichten sind geplant (FT-Präfixe) | unwahrscheinlich |

Eine Dokufrage nebenbei: `spuren_overrides._doku` sagt „spuren_plan.py liest diesen Block noch nicht“. Z. 1865 liest `anordnung` aber.
Ob die Säule als Akteur im Level steht, klärt T23c-0.

### 3.2 Urteil: auflösen, mit einer Ausnahme

1. **Erklärter Ring** (Steinkreis, Opferstätte, Hügelgrab, Feuerstelle): Er bleibt nur mit Mittelobjekt innerhalb von 0,3 r, Höhe ≥ 1 m
   (bei der Feuerstelle das Feuerstellen-Netz). Er zählt höchstens `max_je_feld` und ist Sperre für die Reparatur. Ohne Mitte ist er FEHLER
   `ring_mitte_fehlt`. **Reparatur:** die Mitte setzen, nicht die Steine bewegen.
2. **Begleiter ohne Hauptstück** (Saum, Satelliten, gleiche gid): FEHLER. Die Begleiter werden entfernt oder das Hauptstück neu gesetzt.
   **Neu: Gruppenkohärenz.** Fällt ein Hauptstück, auch durch die 23-Reparatur, fallen seine Begleiter mit, außer ≤ 2 m liegt ein anderes
   Stück ≥ 1 m.
3. **Unerklärter Ring:** ≥ 50 % der Glieder in einem zusammenhängenden Bogen ≥ 150° entfernen. Die Reste bilden eine Gruppe auf einer
   Seite. Versatz nur in den 23.1-Grenzen. Danach findet der Detektor nichts, und im Rest gibt es keine Lücke > 120°.

### 3.3 Ringdetektor (Code `ringe`)

- **Suche:** Hough-artig über Mitte × Radius. Grobraster 0,5 m, r 1,5–12 m. Verfeinerung ± 0,5 m in Schritten von 0,125 m, danach
  Kåsa-Kreisfit.
- **Ring (FEHLER), alle Bedingungen:**
  - Band ± w (w = max(0,25 m; 0,08 r)) mit ≥ 8 Gliedern;
  - Band ≥ 4 × dichter als Fenster und Außenband, Poisson-Restwahrscheinlichkeit ≤ 1e-7;
  - Inneres ≤ 0,15 × Banddichte und ≤ 1,5 × Umgebung + 2;
  - Winkelabstände gleichmäßig: CV ≤ 0,6, größte Lücke ≤ 90°;
  - Fit-RMS ≤ max(0,15 m; 0,6 w).
- **Bogen (WARNUNG):** ≥ 6 zusammenhängende 30°-Sektoren, n ≥ 9, ≥ 6 × dichter.
- **Grenzen:**
  - Der Detektor läuft je Klasse und je Planerschicht, denn ein dichter fremder Hintergrund senkt die Empfindlichkeit.
  - Ringe mit 8 Gliedern und Abständen > 2,5 m werden oft nicht gefunden.
  - Fehlalarm synthetisch etwa 1 in 60 Fenstern. Jeder Fund wird deshalb im Bild bestätigt, bevor repariert wird.

---

## 4. Hängende Netze (Frage 3)

**Befund [Repo]:**
- `SM_EISZAPFEN_1–9` haben den Pivot oben (Z max +0,05…+0,07 m, Z min −0,75…−0,87 m bei `_1/_5`). Die dünne Achse ist Y (≈ 0,2 m), also
  der Rücken. Das Material ist `M_Eldarien_Eis`.
- `hochgebirge_regeln.json` `klassen.eiszapfen` (Z. 1186–1250): `z_versatz_anteil` 0,85, `kippen` 0, `yaw` „zufall“, `hang_min_grad` 55.
- `hochgebirge_plan.py` Z. 968–969 rechnet z = z0 + Höhe · Skala · 0,85, also senkrecht über dem Zellpunkt.
- felsgruppen `zusatzklassen.eis` macht dasselbe: Z. 3887–3888 schaltet die Schwebeprüfung ab, Z. 3908–3909 setzt Z = Welt-Z, Z. 3926 rechnet z.
- Folge: Der waagrechte Spalt zur Wand beträgt 0,85 h / tan(Hang). Bei 60° sind das 0,49 m je Meter Zapfen, bei 75° 0,23 m. Der Rücken zeigt
  zufällig zur Wand. Auf Grat- und Kantenzellen liegt die Oberkante über dem Gelände; das Netz steht frei gegen den Himmel.
- `M_Eldarien_Eis` hat laut `material_parameter.json` keine Parameter, keine Texturen und 0 Instanzen. Das erklärt das flache Weiß im Bild.

**„Zaunartige weiße Teile am Horizont“:** Das sind sehr wahrscheinlich dieselben Eiszapfen-Netze. Ein Querbalken mit senkrechten Zapfen liest
sich in der Reihe wie ein Zaun. Sie stehen auf Kantenzellen über der Kante [Bild + Ableitung].
**Prüfung:** Instanzen `SM_EISZAPFEN_*` mit Oberkante > max. Gelände im Umkreis 2 m + 0,1 m oder ohne Treffer nach oben: FEHLER `schwebt_frei`.

**Regeln (neu, JSON `haengend`):**

| Punkt | Regel | Begründung |
|---|---|---|
| welche Netze | Eiszapfen und Eisvorhänge; weitere nur mit `haengend: true` je Netz (anzulegen) | — |
| Ort | nur unter einer Überhang-Unterseite (Felsnetz, Klippen-/Schalen-Akteur) oder an einer Simskante: oben ≤ 35°, unten ≥ 70°, Kante ≤ 0,3 m vom Pivot. An 55–85°-Wänden ohne Sims keine freien Zapfen, höchstens anliegende Eisglasur. Nie auf Graten ohne Oberkante | [S] Zapfen wachsen, wo Schmelz- oder Sickerwasser an eine Kante läuft und abtropft, auch an Felsen und Sickerstellen. Das Höhenfeld kennt keinen Überhang |
| Kontakt oben | 5 Punkte der Oberkante, Trace Welt +Z bis 0,3 m: ≥ 70 % treffen ≤ 5 cm; kein Treffer = `schwebt_frei` | — |
| Eindringtiefe | Oberkante 2–10 cm im Fels | verdeckt die Fuge, ohne die Zapfen zu verkürzen [Gestaltung] |
| Wand | waagrecht entlang −Rücken: Wand ≤ 5 cm an der Oberkante; Spitze 0–40 cm vor der Wand, nicht darin | — |
| Lot | Zapfenachse ≤ 5° zur Welt-Z (Schwerkraft) | Zapfen wachsen lotrecht [S] |
| Rücken | ≤ 30° zur waagrechten Wandnormale | — |
| Boden | Spitze ≥ 0,1 m über Boden oder Eis | — |
| Material | ein MI mit Durchscheinen, Rauheit und Normal ist anzulegen. Mit gebundenen Texturen ist Eis von 23.2 Helligkeit/`untexturiert_verdacht` ausgenommen | [Repo] |
| Foliage-Weg | Align to Normal richtet nur zum Boden aus. Hängende Stücke setzt ein Skript mit Haltepunkt-Suche | [S] Epic FoliageType |

---

## 5. Fremdfarbe (Frage 4)

**Messweg (JSON `farbe_untergrund.messweg`):**
- **A Datenweg.** Modul = Mittel der wirksamen BaseColor, wie `stein_albedo.json` (Y_wirksam, dazu RGB), mal MI-`Toenung` mal
  `Helligkeit`. In `M_EL_Fels_MS` sind das ein VectorParameter (Standard Weiß) und ein ScalarParameter (Standard 1,0)
  (`fels_ms_lesen.json`); MS2 ist die Kopie, die Verdrahtung ist zu prüfen. Boden = Lagengewichte unter Grundriss + 1 m × Mittel-BaseColor
  je Landschaftslage. Dafür ist `landschaft_lagen_albedo.json` **anzulegen**; die Lagen-Albedo liegt im Repo nicht vor.
- **B Bildweg** zur Kontrolle: Pufferansicht BaseColor, Modulpixel gegen einen Ring 0,5–2 m um den Grundriss.
- Umrechnung: lineares RGB → XYZ (D65) → L\*a\*b\*. Zum Vergleich mit 23b: Y 0,07 ≈ L\* 32, Y 0,22 ≈ L\* 54, Y 0,35 ≈ L\* 66.

| Fall | ok | WARNUNG | FEHLER |
|---|---|---|---|
| gleiches Gestein (Lage Fels, Geröll, Kies, Lavafels/-sand desselben Gesteins: Halde, Blockfeld, Moräne) | ΔE76 ≤ 12, \|ΔL\*\| ≤ 10, Δh ≤ 25° | darüber | ΔE76 > 20 |
| anderer Untergrund (Wiese, Waldboden, Sand) | Kontrast erlaubt | — | \|ΔL\*\| > 35 (`helligkeit`) oder Δh > 30° bei C\*_Modul ≥ 15 (`farbton`) |
| Bunttonvergleich | nur, wenn beide C\* ≥ 8 | | |
| Biompalette | zusätzlich die Fels-Lage des Bioms als Bezug für das Gestein (anzulegen) | | |

Die Wahrnehmungsschwelle liegt bei ΔE76 etwa 2,3 [S]. Die Grenzen hier sind Gestaltungswerte für Spieldistanz und Licht. Der Selbsttest
deckt sie ab: rötlich auf grau ΔE 31,6 ist FEHLER, Lava auf Wiese ΔL\* −38 ist FEHLER.

**Reparatur (Reihenfolge):**
1. **Tönung:** nur bei kleinem Abstand (\|ΔL\*\| ≤ 15, Δh ≤ 40°). Ein Kind-MI je Biom, wie die vorhandenen
   `MI_EL_HugeNordicCoastalCliff_01_<biom>`. Nie das gemeinsame MI ändern.
2. **Netztausch** in der Gesteinsfamilie des Bioms (23.2 `familie`), wenn die Textur selbst fremd ist, z. B. rote Findlinge außerhalb
   canyon/oedland/wueste/lava (`netz_nur_biome`).
3. **Entfernen,** wenn es keinen Ersatz gibt und das Fremdgestein außerhalb seiner Lagen liegt.

**Fälle:**
- B5_08: zuerst prüfen, ob das Netz ein roter Findling ist. Wenn ja, Netztausch. Der Hang ist selbst sehr hell; das gehört zur Landschaftslage,
  nicht zu dieser Regel.
- H3_17: graue Wurzelplatte auf braunem Laub. Moos-Tönung im Kind-MI oder ein MossyForestRoots-Netz mit Moos.
- C6_34: helle Kiesel auf Lavasand. Laut `kiesel_ersatz_hinweis` dunkles MI.

---

## 6. Reparatur (Frage 5)

**Ausdünnen und neu gruppieren oder einzeln versetzen?**
- Verteilungsfehler betreffen das Fenster, nicht die einzelne Instanz. Deshalb wird **ausgedünnt** (entfernen) und **über den Planer neu
  gruppiert**.
- Einzeln versetzt wird nur innerhalb der 23.1-Grenzen min(0,5 m; 0,25 L). Mehr Versatz ist Neuplanung, denn das Werkzeug „umsetzen“ soll
  keine Komposition bauen.

| Grenze | Wert |
|---|---|
| entfernt je 50-m-Fenster | ≤ 35 % der Klasse |
| entfernt je Feld | ≤ 15 % (W2 aus 23 §14.4); im Pilotfenster ≤ 25 % (23 §14.2) |
| Neuplanung | > 30 % der Fenster einer Schicht mit Verteilungs-FEHLER oder > 30 % Instanz-FEHLER einer Klasse (23 §10.3) |
| behalten | Hero ≥ 2 m, Akteure, Sehens-Orte, erklärte Ringe mit Mitte, SWR-Hindernisse, Ausbiss-Gruppen |
| Ausdünnen | in Lückenzonen (Wertrauschen 20–40 m, untere 30–40 %), kleinste und häufigste Netze zuerst, bis R und leer im Ziel |
| Drehen | Stein/Fels Yaw frei, danach Sitz 23.1 neu. Stamm um die Mitte ≤ 60° nur mit beiden Auflagen |

**Gesamtreihenfolge 23 + 23b + 23c (neu, JSON `reparatur_23_3`):**
0. Sperren melden.
1. Asset-Änderungen vorab: MI weißer Steine (23b), Eis-MI, Biom-Kind-MI.
2. Je Schicht entscheiden: neu planen oder reparieren.
3. **Entfernen vor Umsetzen:** Ringe, Begleiter ohne Hauptstück, Ausdünnen. So wird kein Sitz an Stücken repariert, die danach fallen.
4. Sitz 23.1: von unten nach oben, groß vor klein.
5. Wiederholung 23.2 und Netzanteil.
6. Totholz.
7. Hängendes, also nach den Felsen, an denen es hängt.
8. Farbe zuletzt.
9. Verteilung neu messen; die Grenzen oben gelten für die Summe aller Schritte.

---

## 7. Regeln 23.3 – Gesamttabelle

| Bereich | Regel | Zahl | Stand |
|---|---|---|---|
| Sitz je Klasse | Eingraben, Lücke, Deckung, Winkel, Kante (23 §3) | unverändert | 23.1 |
| Platten | liegend; Dachziegel, Ausbiss nur erklärt | unverändert | 23.1 |
| Stapel, Wasser, Totholz | getragen, treiben, Brücke/Rampe, Teller am Ufer | unverändert | 23.1/23.2 |
| Wiederholung | ρ/θ je Klasse, Gruppe, doppelt | unverändert | 23.2 |
| Spiegeln, Skala | X/Y nach T23b-S; 0,85–1,15 | unverändert | 23.2 |
| Helligkeit, untexturiert | trocken 0,22/0,35, nass 0,09/0,15; `textur_fehlt` | **geändert:** Eis mit gebundenen Texturen ausgenommen | 23.2 → 23.3 |
| Verteilung | R ≤ 1,10 (FEHLER), Biom-Bereiche, leer, VMR, L(r) | §2.4 | **neu** |
| Größe | p90/p10 ≥ 2,5 FEHLER; b 1,8–3,0 WARNUNG | §2.2 | **neu** |
| Netzanteil | 50 m: ≥ 4 Netze, ≤ 35 % | ergänzt 23.2 (15 m ≤ 40 %) | **neu** |
| Ausrichtung, Neigung | Halde Rbar2 ≥ 0,25 ± 25°; Neigungsstreuung ≥ 6° | §2.1 | **neu** |
| Reihe | Abstands-CV ≥ 0,35 entlang Bändern | §2.2 | **neu** |
| Fremdgestein | nur auf eigenen Lagen + 5 m | §2.3 | **neu** |
| Totholz-Verteilung | Längen p90/p10 ≥ 2, Schnittflächen nur ≤ 30 m vom Weg, ≤ 200 je ha | §2.1 | **neu** |
| Ringe | Detektor §3.3; erklärt nur mit Mitte | §3 | **neu** |
| Gruppenkohärenz | Begleiter fallen mit dem Hauptstück | §3.2 | **neu** |
| Hängend | Ort Überhang/Sims, Kontakt ≤ 5 cm, Eindringtiefe 2–10 cm, Lot ≤ 5°, Rücken ≤ 30° | §4 | **neu** |
| Farbe Untergrund | ΔE/ΔL\*/Δh nach Fall | §5 | **neu**; 23.1 Palette und 23.2 Helligkeit bleiben |
| Reparatur | Gesamtreihenfolge, Entfernen vor Umsetzen, 35 %/15 % | §6 | **geändert:** Reihenfolge ergänzt |

---

## 8. Planerregeln (Ergänzung zu 23 §11 und 23b §5)

Der Setzer-Vertrag bekommt einen dritten Prüfer: vor dem Schreiben `sitz_pruefung`, `pruefe_wiederholung` **und**
`verteilung_23c` je Fenster.

| Planer | Änderung |
|---|---|
| alle | Gruppenscheiben ≤ 15 % der Fläche; Dichte mit Wertrauschen 20–60 m (leer-Ziel je Biom); Größen je Gruppe nach Potenzgesetz mit einem dominanten Stück; Gruppenkohärenz über gid |
| spuren | `anordnung: ring` und `_ring` nur zusammen mit dem Mittelobjekt in einem Schritt; ohne Mitte entfällt der Ring. Radius ± 10 %, Winkel ± 20° je Stein, 10–25 % fehlend oder umgefallen |
| felsgruppen | `_saum`: Abstand vom Fuß exponentiell (Mittel 0,6 m, 0,2–2,5 m) statt gleichverteilt im Kranz. Saum erst nach `budget` und `netz_biom_pruefung` erzeugen oder mit seiner gid mit ausdünnen. Satelliten entfallen mit dem Hero |
| lava | Gruppenzentren dünn; im Saum zur Aue Lavagestein nur auf Lava-Lagen + 5 m; Opferstätten-Säule prüfen; Kiesel dunkel (MI) |
| hochgebirge / felsgruppen eis | `z_versatz` ersetzen: Haltepunkt suchen (§4 Ort), z = Unterseite − 2…8 cm, Yaw = Rücken zur Wandnormale; ohne Haltepunkt nicht setzen |
| mittelschicht / felsdeckung Totholz | Stammstücke nach §2.1; Längen gemischt; gleiches Netz ≤ 1 je 30 m |
| p2bett / kantenufer_p2 | Uferblöcke nicht in gleichem Abstand: Reihe-CV ≥ 0,35 |

**Wie in 23:** Für Schichten mit geplantem Neulauf wird zuerst der Planer geändert und dann neu gesetzt; dort gibt es keine Einzelreparatur.

---

## 9. Prüffälle gut/schlecht

### 9.1 Synthetisch (Code §10)

Die Sollwerte sind analytisch oder vorgegeben, nicht vom geprüften Algorithmus erzeugt (pruefung.md).

| Nr. | Fall | Soll | Ist (Cloud) |
|---|---|---|---|
| V1a–c | Poisson 400 in 50 × 50 m | R 0,9–1,1 (Rand 0,85–1,15), \|L − r\| ≤ 0,3, kein Ring | R 1,031 / 0,962 / 0,949, L − r ≤ 0,08, 0 Ringe |
| V2 | Thomas κ = 0,016, σ = 1,5, 10 Kinder | R < 0,8; L(3) − 3 = 1,64 ± 0,45 (K analytisch); VMR > 2 | R 0,646; 1,54; VMR 8,8; 0 Ringe |
| V3 | Gitter 2,5 m ± 0,1 | R 2,0 (Quadratgitter), L(1) − 1 = −1 | R 1,890; −1,00 → FEHLER gleichmäßig |
| V4 | Ring r 3 m, 10 Steine, 100 Zufallspunkte | 1 Ring, Mitte und r ± 0,3 m | (20,06; 29,99) r 2,95 |
| V5 | Kieselsaum ohne Hauptstück | FEHLER 14 Begleiter | wie Soll |
| V6 | Opferstätte mit / ohne Säule | ok_erklaert / FEHLER_mitte_fehlt | wie Soll |
| V7 | Netz 70 % / 5 × 20 % | FEHLER / ok | wie Soll |
| V8 | Pareto b = 2,0 / Einheitsgröße | b 2,0 ± 0,15 / FEHLER | b 2,018 / p90/p10 1,16 |
| V9 | Achsen zufällig / Falllinie ± 15° | Rbar2 < 0,15 / > 0,7 | 0,053 / 0,958 |
| V10 | Reihe 1,5 m / exponentiell | FEHLER / ok | CV 0,05 / 0,93 |
| H1–H4 | Wand 60° wie Planer / Überhang / Grat / Achse 40° | FEHLER (Spalt 0,49 m) / ok / FEHLER / FEHLER `achse_lot` | wie Soll |
| U1–U4 | grau auf grau / rötlich auf grau / Lava auf Wiese / Lava auf Lavasand | ok / FEHLER / FEHLER / ok | wie Soll |

**Gegenprobe:** Mit R-Grenze 2,1, Winkel-CV 0,05 und ΔE-FEHLER 40 schlagen V3, V4, V6 und U1–4 fehl.

**Zusatzserie Ringdetektor** (nicht im Selbsttest, Laufzeit):
- 24 von 28 eingesetzten Ringen gefunden (n 8–12, r 1,5–6 m, Hintergrund 50–150 Punkte). Verfehlt wurden 3 × „8 Steine auf r 6 m“ und
  1 × „8 Steine auf r 3 m“.
- In 60 Fenstern ohne Ring (Poisson 150/400, Thomas) gab es 1 Fehlalarm.

### 9.2 Kontrollfälle im Testlevel (ergänzen K1–K24)

Die Sollwerte kommen aus dem Setzen von Hand. Lücken und Abstände werden unabhängig per Line-Trace abgelesen.

| K | Aufbau | Soll |
|---|---|---|
| K25 | 10 × `SM_lava_s_rock_06` von Hand auf einem Kreis r 3 m | Ring, Mitte ± 0,3 m |
| K26 | wie K25 mit `SM_Column_02` in der Mitte, als Spur erklärt | ok_erklaert |
| K27 | 30 Steine auf einem 2,5-m-Gitter | R ≈ 2 (≥ 1,8), FEHLER |
| K28 | `SM_EISZAPFEN_1` unter einem Überhang eines Felsnetzes, Oberkante 4 cm im Fels | ok |
| K29 | `SM_EISZAPFEN_1` wie der Planer an einer 60°-Rampe (z = Gelände + 0,85 h) | FEHLER `schwebt_frei`, Spalt 0,49 × h × Skala ± 2 cm |
| K30 | grauer Stein auf grauer Kieslage, dann mit `Toenung` (1; 0,6; 0,45) | ok / FEHLER farbton (Pufferansicht BaseColor) |

### 9.3 Gut/schlecht im Projekt

| gut | schlecht |
|---|---|
| Blockgruppen am Wandfuß, dazwischen Grasflächen, unten größer | gleichmäßiges Lavafeld bis zum Rand (C6_28) |
| erklärte Opferstätte mit Säule | Steinkreis ohne Mitte (C6_34) |
| Eiszapfen unter einem Sims, eng an der Wand | Eiszapfen frei vor der Wand oder auf dem Grat (E2_24) |
| Lavablöcke als Kette am Stromrand | Lavaklumpen einzeln auf der Wiese (C5_16) |
| wenige lange Stämme mit Teller oder Ästen, Windwurf mit gemeinsamer Richtung | 30 gleiche Stammstücke kreuz und quer (B5_27) |
| graues Gestein auf grauem Schutt | ockerroter Block auf grauem Hang (B5_08) |

---

## 10. Prüfcode `verteilung_23c.py` (Python 3, nur Standardbibliothek)

Diese Datei liegt neben `sitz_pruefung.py` und `wiederholung_23b.py`.

**Cloud-Ergebnis (Python 3.13):**
- `python -I verteilung_23c.py --selbsttest` zweimal und mit `--regeln recherche/antworten/steine_sitz_regeln.json`:
  `SELBSTTEST OK  Regeln 23.3  Faelle 14  Signatur b4ebdb213b2f71ba`, Laufzeit ≈ 9,5 s.
- Mit der 23.3-Datei: 23 `64a654746495eca8`, 23b `dabb50741db8b9ac`, beide unverändert.

**Lokal:** `--fenster instanzen.json` nimmt eine Liste `{x, y, netz, L, yaw_lang}` in m und Grad je 50-m-Fenster und Klasse. Für 70 Felder
wird eine NumPy-Fassung empfohlen; die Ergebnisse müssen gleich sein (gleiche Selbsttest-Signatur in der Referenz).

```python
# verteilung_23c.py - Verteilung, Ringe, Haengendes, Untergrundfarbe (Antwort 23c, Regeln 23.3). Nur Standardbibliothek.
# Aufruf: python -I verteilung_23c.py --selbsttest [--regeln steine_sitz_regeln.json]
#         python -I verteilung_23c.py --fenster instanzen.json [--regeln ...]   (Liste {x, y, netz, L, yaw_lang, klasse} in m/Grad)
# Ergaenzt sitz_pruefung.py (23) und wiederholung_23b.py (23b); beide bleiben unveraendert.
import argparse, hashlib, json, math, random
from bisect import bisect_left, bisect_right

R = {  # Grenzwerte = steine_sitz_regeln.json "verteilung", "ringe", "haengend", "farbe_untergrund" (Version 23.3)
    "n_min": {"clark_evans": 30, "l_funktion": 50, "netz_50m": 20, "groesse": 50, "ausrichtung": 15},
    "ce_gleichmaessig_fehler": 1.10, "zelle_m": 10.0, "netz_anteil_max_50m": 0.35, "netz_min_50m": 4,
    "groesse_p90_p10_min": 2.5, "groesse_b": [1.8, 3.0], "reihe_cv_fehler": 0.35,
    "ring": {"r": [1.5, 12.0], "r_schritt": 0.25, "gitter_m": 0.5, "w": [0.25, 0.08], "n_min": 8, "dichte_faktor": 4.0,
             "p_max": 1e-7, "p_grob": 1e-3, "innen_max_anteil": 0.15, "innen_dichte_max": 1.5,
             "sektoren": 12, "winkel_cv_max": 0.6, "winkel_luecke_max_grad": 90,
             "sektoren_bogen": 6, "bogen_n_min": 9, "bogen_dichte_faktor": 6.0, "fit_rms_max": 0.15},
    "haengend": {"kontakt_oben_max_m": 0.05, "eindring_m": [0.02, 0.10], "wand_oben_max_m": 0.05, "wand_spitze_max_m": 0.40,
                 "achse_max_grad": 5.0, "ruecken_max_grad": 30.0, "kontakt_anteil_min": 0.7},
    "farbe": {"gleich": {"dL": 10.0, "dE": 12.0, "dE_fehler": 20.0, "dh": 25.0},
              "fremd": {"dL_fehler": 35.0, "dh_fehler": 30.0, "C_min": 8.0}},
}

# ---------------- Raster (Nachbarsuche) ----------------
class Raster:
    def __init__(self, pts, zelle):
        self.z, self.p, self.g = zelle, pts, {}
        for i, (x, y) in enumerate(pts):
            self.g.setdefault((int(math.floor(x / zelle)), int(math.floor(y / zelle))), []).append(i)

    def nahe(self, x, y, r):
        k = int(math.ceil(r / self.z)); cx, cy = int(math.floor(x / self.z)), int(math.floor(y / self.z))
        for i in range(cx - k, cx + k + 1):
            for j in range(cy - k, cy + k + 1):
                for n in self.g.get((i, j), ()):
                    yield n

def nn_abstaende(pts):
    n = len(pts)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    A = max(1e-9, (max(xs) - min(xs)) * (max(ys) - min(ys)))
    ras = Raster(pts, max(0.5, math.sqrt(A / n)))
    out = []
    for i, (x, y) in enumerate(pts):
        r = ras.z
        while True:
            best = min((math.hypot(pts[j][0] - x, pts[j][1] - y) for j in ras.nahe(x, y, r) if j != i), default=None)
            if best is not None and best <= r: out.append(best); break
            r *= 2.0
            if r > 1e6: out.append(float("inf")); break
    return out

# ---------------- Clark-Evans mit Randkorrektur ----------------
def clark_evans(pts, fenster, korrektur="donnelly", rand_m=5.0):
    """R = mittlerer NN-Abstand / Erwartung bei CSR. Donnelly (1978) fuer Rechteckfenster wie spatstat:
    E = 0,5 sqrt(A/n) + (0,0514 + 0,0412/sqrt n) P/n. 'rand': nur Punkte >= rand_m vom Fensterrand (Guard), NN aus allen."""
    x0, y0, x1, y1 = fenster; n = len(pts)
    if n < R["n_min"]["clark_evans"]: return None
    A = (x1 - x0) * (y1 - y0); P = 2 * ((x1 - x0) + (y1 - y0)); lam = n / A
    d = nn_abstaende(pts)
    if korrektur == "rand":
        d = [di for di, (x, y) in zip(d, pts) if min(x - x0, x1 - x, y - y0, y1 - y) >= rand_m]
        E = 0.5 / math.sqrt(lam)
    elif korrektur == "donnelly":
        E = 0.5 * math.sqrt(A / n) + (0.0514 + 0.0412 / math.sqrt(n)) * P / n
    else:
        E = 0.5 / math.sqrt(lam)
    rq = sum(d) / len(d)
    se = 0.26136 / math.sqrt(len(d) * lam)
    return {"R": rq / E, "z": (rq - E) / se, "n": n, "r_mittel": rq}

# ---------------- Ripley K/L, isotrope Randkorrektur ----------------
def _kreis_anteil(x, y, r, f, m=72):
    x0, y0, x1, y1 = f; k = 0
    for t in range(m):
        a = 2 * math.pi * (t + 0.5) / m
        px, py = x + r * math.cos(a), y + r * math.sin(a)
        k += (x0 <= px <= x1 and y0 <= py <= y1)
    return max(k / m, 0.25)

def l_funktion(pts, fenster, radien):
    x0, y0, x1, y1 = fenster; n = len(pts); A = (x1 - x0) * (y1 - y0)
    if n < R["n_min"]["l_funktion"]: return None
    rmax = max(radien); ras = Raster(pts, max(1.0, rmax / 2)); paare = []
    for i, (x, y) in enumerate(pts):
        for j in ras.nahe(x, y, rmax):
            if j == i: continue
            d = math.hypot(pts[j][0] - x, pts[j][1] - y)
            if 0 < d <= rmax: paare.append((d, 1.0 / _kreis_anteil(x, y, d, fenster)))
    out = {}
    for r in radien:
        K = A / (n * (n - 1)) * sum(w for d, w in paare if d <= r)
        out[r] = math.sqrt(K / math.pi) - r
    return out

def thomas_L_soll(r, kappa, sigma):  # analytisch: K = pi r^2 + (1 - exp(-r^2 / 4 sigma^2)) / kappa
    return math.sqrt((math.pi * r * r + (1 - math.exp(-r * r / (4 * sigma * sigma))) / kappa) / math.pi) - r

# ---------------- Quadrat-Zaehlung: Luecken und Streuung ----------------
def quadrate(pts, fenster, zelle=None):
    zelle = zelle or R["zelle_m"]; x0, y0, x1, y1 = fenster
    nx, ny = int((x1 - x0) // zelle), int((y1 - y0) // zelle); c = [0] * (nx * ny)
    for x, y in pts:
        i, j = int((x - x0) // zelle), int((y - y0) // zelle)
        if 0 <= i < nx and 0 <= j < ny: c[i * ny + j] += 1
    m = sum(c) / len(c); v = sum((k - m) ** 2 for k in c) / (len(c) - 1)
    return {"vmr": v / m if m else 0.0, "leer": sum(1 for k in c if k == 0) / len(c)}

# ---------------- Netzanteil, Groesse, Ausrichtung, Reihe ----------------
def netz_anteil(netze):
    if len(netze) < R["n_min"]["netz_50m"]: return None
    z = {}
    for k in netze: z[k] = z.get(k, 0) + 1
    top = max(z.values()) / len(netze)
    urteil = "FEHLER" if top > R["netz_anteil_max_50m"] or len(z) < R["netz_min_50m"] else "ok"
    return {"anteil_max": top, "netze": len(z), "urteil": urteil}

def groesse(L, x_min=0.3):
    xs = sorted(v for v in L if v >= x_min)
    if len(xs) < R["n_min"]["groesse"]: return None
    s = sum(math.log(v / x_min) for v in xs); alpha = 1 + len(xs) / s       # MLE (Clauset et al. 2009), Dichte ~ L^-alpha
    p = lambda q: xs[min(len(xs) - 1, int(q * len(xs)))]
    b = alpha - 1                                                            # kumulativ N(>L) ~ L^-b
    lo, hi = R["groesse_b"]; ratio = p(0.9) / p(0.1)
    urteil = "FEHLER" if ratio < R["groesse_p90_p10_min"] else ("WARNUNG" if not lo <= b <= hi else "ok")
    return {"b": b, "b_se": b / math.sqrt(len(xs)), "p90_p10": ratio, "urteil": urteil}

def ausrichtung(winkel_grad, fall_grad=None):
    """Achsendaten (0-180): Winkel verdoppeln. Rbar2 = mittlere Resultierende, Rayleigh p, Lage zur Falllinie."""
    n = len(winkel_grad)
    if n < R["n_min"]["ausrichtung"]: return None
    c = sum(math.cos(2 * math.radians(a)) for a in winkel_grad) / n
    s = sum(math.sin(2 * math.radians(a)) for a in winkel_grad) / n
    rb = math.hypot(c, s); z = n * rb * rb
    p = math.exp(-z) * (1 + (2 * z - z * z) / (4 * n) - (24 * z - 132 * z ** 2 + 76 * z ** 3 - 9 * z ** 4) / (288 * n * n))
    out = {"Rbar2": rb, "p": min(1.0, max(0.0, p)), "richtung": (math.degrees(math.atan2(s, c)) / 2) % 180}
    if fall_grad is not None:
        out["zur_falllinie"] = sum(math.cos(2 * math.radians(a - fall_grad)) for a in winkel_grad) / n
    return out

def reihe_cv(s_entlang):
    s = sorted(s_entlang); g = [b - a for a, b in zip(s, s[1:])]
    if len(g) < 5: return None
    m = sum(g) / len(g); cv = math.sqrt(sum((x - m) ** 2 for x in g) / (len(g) - 1)) / m
    return {"cv": cv, "urteil": "FEHLER" if cv < R["reihe_cv_fehler"] else "ok"}

# ---------------- Ringdetektor (Hough-Akkumulator ueber Mittelpunkt x Radius) ----------------
def _kasa(p):
    n = len(p); sx = sum(x for x, _ in p) / n; sy = sum(y for _, y in p) / n
    u = [(x - sx, y - sy) for x, y in p]
    suu = sum(a * a for a, _ in u); svv = sum(b * b for _, b in u); suv = sum(a * b for a, b in u)
    suuu = sum(a ** 3 for a, _ in u); svvv = sum(b ** 3 for _, b in u)
    suvv = sum(a * b * b for a, b in u); svuu = sum(b * a * a for a, b in u)
    det = suu * svv - suv * suv
    if abs(det) < 1e-12: return None
    uc = (0.5 * (suuu + suvv) * svv - 0.5 * (svvv + svuu) * suv) / det
    vc = (0.5 * (svvv + svuu) * suu - 0.5 * (suuu + suvv) * suv) / det
    r = math.sqrt(uc * uc + vc * vc + (suu + svv) / n)
    cx, cy = uc + sx, vc + sy
    rms = math.sqrt(sum((math.hypot(x - cx, y - cy) - r) ** 2 for x, y in p) / n)
    return cx, cy, r, rms

def _poisson_rest(k, mu):  # P(N >= k), N ~ Poisson(mu)
    t = math.exp(-mu); c = t
    for i in range(1, k): t *= mu / i; c += t
    return max(0.0, 1.0 - c)

def _ring_bewerten(pts, ras, lam, cx, cy, r, G, streng=True):
    """Kennwerte eines Kandidaten (Mitte cx/cy, Radius r). streng=False: Grobsuche mit breiterem Band (Rasterfehler)."""
    w = max(G["w"][0], G["w"][1] * r) + (0.0 if streng else 0.5 * G["gitter_m"] * math.sqrt(2))
    ri = r - w - min(0.5, 0.5 * w); ro0 = r + w + 0.3; ro1 = ro0 + max(1.5, 0.5 * r)
    mit, ni, no = [], 0, 0
    for j in ras.nahe(cx, cy, ro1):
        d = math.hypot(pts[j][0] - cx, pts[j][1] - cy)
        if r - w <= d <= r + w: mit.append(j)
        elif d < ri: ni += 1
        elif ro0 <= d <= ro1: no += 1
    nr = len(mit)
    if nr < G["n_min"]: return None
    d_ring = nr / (4 * math.pi * r * w); bezug = max(lam, no / (math.pi * (ro1 * ro1 - ro0 * ro0)))
    if d_ring < (G["dichte_faktor"] if streng else 0.5 * G["dichte_faktor"]) * bezug: return None
    if not streng: return d_ring / bezug
    if _poisson_rest(nr, bezug * 4 * math.pi * r * w) > G["p_max"]: return None
    a_in = math.pi * ri * ri
    if ni > G["innen_max_anteil"] * d_ring * a_in or ni > G["innen_dichte_max"] * bezug * a_in + 2: return None
    zs = {}
    for j in mit:
        k = int((math.atan2(pts[j][1] - cy, pts[j][0] - cx) % (2 * math.pi)) / (2 * math.pi) * G["sektoren"]) % G["sektoren"]
        zs[k] = zs.get(k, 0) + 1
    lauf = best = 0
    for k in range(2 * G["sektoren"]):
        lauf = lauf + 1 if (k % G["sektoren"]) in zs else 0; best = max(best, min(lauf, G["sektoren"]))
    wi = sorted(math.atan2(pts[j][1] - cy, pts[j][0] - cx) % (2 * math.pi) for j in mit)
    gaps = [b - a for a, b in zip(wi, wi[1:])] + [wi[0] + 2 * math.pi - wi[-1]]
    gm = 2 * math.pi / nr; gcv = math.sqrt(sum((g - gm) ** 2 for g in gaps) / nr) / gm
    ring = gcv <= G["winkel_cv_max"] and max(gaps) <= math.radians(G["winkel_luecke_max_grad"])
    if not ring and (best < G["sektoren_bogen"] or nr < G["bogen_n_min"] or d_ring < G["bogen_dichte_faktor"] * bezug): return None
    return {"ring": ring, "score": d_ring / bezug, "mit": mit, "sektoren": len(zs), "innen": ni, "w": w}

def ringe(pts, fenster):
    """Hough-artige Suche: Mittelpunkt-Raster x Radius, Grobsuche (breites Band), Verfeinerung +-0,5 m / +-0,5 m in 0,125-m-Schritten,
    Kasa-Kreisfit der Ringglieder. Gefunden wird ein Band, das >= dichte_faktor x dichter ist als Umgebung (Fenster und Aussenband),
    mit Poisson-Restwahrscheinlichkeit <= p_max, leerem Inneren und gleichmaessiger Winkelbelegung."""
    G = R["ring"]; x0, y0, x1, y1 = fenster; n = len(pts)
    if n < G["n_min"]: return []
    lam = n / ((x1 - x0) * (y1 - y0)); ras = Raster(pts, 2.0); rad = []; r = G["r"][0]
    while r <= G["r"][1] + 1e-9: rad.append(r); r += G["r_schritt"]
    grob = []; st = G["gitter_m"]; cx = x0
    while cx <= x1:
        cy = y0
        while cy <= y1:
            ds = sorted(math.hypot(pts[j][0] - cx, pts[j][1] - cy) for j in ras.nahe(cx, cy, G["r"][1] * 1.6 + 2.5))
            for r in rad:                               # Grobsuche: breiteres Band (Rasterfehler), nur Zaehlungen
                w = max(G["w"][0], G["w"][1] * r) + 0.5 * st * math.sqrt(2)
                nr = bisect_right(ds, r + w) - bisect_left(ds, r - w)
                if nr < G["n_min"]: continue
                ro0 = r + w + 0.3; ro1 = ro0 + max(1.5, 0.5 * r)
                no = bisect_right(ds, ro1) - bisect_left(ds, ro0)
                bezug = max(lam, no / (math.pi * (ro1 * ro1 - ro0 * ro0))); erw = bezug * 4 * math.pi * r * w
                if nr >= 0.5 * G["dichte_faktor"] * erw and _poisson_rest(nr, erw) <= G["p_grob"]:
                    grob.append((nr / erw, cx, cy, r))
            cy += st
        cx += st
    grob.sort(key=lambda k: -k[0]); kand = []; gesehen = []
    for sc, gx, gy, gr in grob:
        if any(math.hypot(gx - a, gy - b) < 1.0 and abs(gr - c) < 1.0 for a, b, c in gesehen): continue
        gesehen.append((gx, gy, gr))
        nah = [pts[j] for j in ras.nahe(gx, gy, gr + 2.0)]
        best = None
        for i in range(-4, 5):                      # Verfeinerung: groesste Belegung des strengen Bandes
            for j in range(-4, 5):
                cx, cy = gx + 0.125 * i, gy + 0.125 * j
                ds = sorted(math.hypot(x - cx, y - cy) for x, y in nah)
                for k in range(-4, 5):
                    rr = gr + 0.125 * k; w = max(G["w"][0], G["w"][1] * rr)
                    if rr < G["r"][0]: continue
                    m = bisect_right(ds, rr + w) - bisect_left(ds, rr - w)
                    if best is None or m > best[0]: best = (m, cx, cy, rr)
        if best is None: continue
        e = _ring_bewerten(pts, ras, lam, best[1], best[2], best[3], G)
        if e: kand.append((e["ring"], e["score"], best[1], best[2], best[3], e))
    kand.sort(key=lambda k: (not k[0], -k[1])); fund = []
    for ring, sc, cx, cy, r, e in kand:
        if any(math.hypot(cx - f["x"], cy - f["y"]) < max(2.0, 0.5 * r) for f in fund): continue
        fit = _kasa([pts[j] for j in e["mit"]])
        if fit is None or fit[3] > max(G["fit_rms_max"], 0.6 * e["w"]): continue
        art = "ring" if ring else "bogen"
        fund.append({"art": art, "x": fit[0], "y": fit[1], "r": fit[2], "rms": fit[3], "n": len(e["mit"]), "sektoren": e["sektoren"],
                     "innen": e["innen"], "score": sc, "urteil": "FEHLER" if art == "ring" else "WARNUNG"})
    return fund

def gruppen_kohaerenz(inst):
    """Begleiter (Kieselsaum, Satelliten, Ringsteine) leben mit ihrem Hauptstueck: je gid ohne vorhandenes Hauptstueck die Zahl der Begleiter."""
    haupt = {i["gid"] for i in inst if i["haupt"]}; out = {}
    for i in inst:
        if not i["haupt"] and i["gid"] not in haupt: out[i["gid"]] = out.get(i["gid"], 0) + 1
    return out

def ring_mitte(fund, mittelobjekte, anteil=0.3):
    """Ein Ring ist nur als erklaerte Spur (Steinkreis, Opferstaette, Huegelgrab) zulaessig und nur mit Mittelobjekt (x, y, Hoehe m >= 1)
    innerhalb anteil x r; sonst FEHLER."""
    ok = any(math.hypot(x - fund["x"], y - fund["y"]) <= anteil * fund["r"] and h >= 1.0 for x, y, h in mittelobjekte)
    return "ok_erklaert" if ok else "FEHLER_mitte_fehlt"

# ---------------- Haengende Netze (Eiszapfen, Eisvorhang, Haengewurzeln) ----------------
def haengend(m):
    """m: Messwerte aus Line-Traces je Instanz (lokal): oben_dz = Liste Abstand Oberkante -> Treffer nach Welt +Z (None = kein Treffer),
    eindring = Eindringtiefe der Oberkante (m), wand_oben/wand_spitze = waagrechter Abstand zur Wand (m), achse = Winkel Zapfenachse zu
    Welt -Z (Grad), ruecken = Winkel Netz-Ruecken zur waagrechten Wandnormale (Grad)."""
    H = R["haengend"]; f = []
    tr = [d for d in m["oben_dz"] if d is not None and d <= H["kontakt_oben_max_m"]]
    if not m["oben_dz"] or all(d is None for d in m["oben_dz"]): f.append("schwebt_frei")
    elif len(tr) / len(m["oben_dz"]) < H["kontakt_anteil_min"]: f.append("kontakt_oben")
    if not H["eindring_m"][0] <= m["eindring"] <= H["eindring_m"][1]: f.append("eindringtiefe")
    if m["wand_oben"] is None or m["wand_oben"] > H["wand_oben_max_m"]: f.append("wandabstand")
    if m["wand_spitze"] is not None and not 0.0 <= m["wand_spitze"] <= H["wand_spitze_max_m"]: f.append("spitze")
    if m["achse"] > H["achse_max_grad"]: f.append("achse_lot")
    if m["ruecken"] > H["ruecken_max_grad"]: f.append("ruecken_zur_wand")
    return ("FEHLER" if f else "ok"), f

def planer_spalt(h, z_versatz, hang_grad):  # waagrechter Spalt Pivot -> Wand bei z = Gelaende + z_versatz * h
    return z_versatz * h / math.tan(math.radians(hang_grad))

# ---------------- Farbe Modul gegen Untergrund (CIELAB, D65, linear) ----------------
def lab(rgb_linear):
    r, g, b = rgb_linear
    X = 0.4124 * r + 0.3576 * g + 0.1805 * b; Y = 0.2126 * r + 0.7152 * g + 0.0722 * b; Z = 0.0193 * r + 0.1192 * g + 0.9505 * b
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(X / 0.95047), f(Y), f(Z / 1.08883)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)

def srgb_zu_linear(c):
    return tuple(((v / 255) / 12.92) if v / 255 <= 0.04045 else (((v / 255) + 0.055) / 1.055) ** 2.4 for v in c)

def farbe_untergrund(modul, boden, gleiches_gestein):
    """modul/boden: lineare BaseColor-Mittel (Modul mit wirksamer MI inkl. Toenung x Helligkeit; Boden = Lagen-Mittel unter dem
    Grundriss + 1 m). gleiches_gestein: Lage am Ort ist Fels/Geroell/Kies/Lavafels/Lavasand desselben Gesteins (Halde, Blockfeld)."""
    L1, a1, b1 = lab(modul); L2, a2, b2 = lab(boden)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2); dL = L1 - L2; dE = math.sqrt(dL ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2)
    dh = None
    if min(C1, C2) >= R["farbe"]["fremd"]["C_min"]:
        dh = abs((math.degrees(math.atan2(b1, a1)) - math.degrees(math.atan2(b2, a2)) + 180) % 360 - 180)
    F = R["farbe"]; f = []
    if gleiches_gestein:
        if dE > F["gleich"]["dE_fehler"]: f.append("dE")
        elif abs(dL) > F["gleich"]["dL"] or dE > F["gleich"]["dE"] or (dh is not None and dh > F["gleich"]["dh"]): f.append("dE_warn")
    else:
        if abs(dL) > F["fremd"]["dL_fehler"]: f.append("helligkeit")
        if dh is not None and dh > F["fremd"]["dh_fehler"] and C1 >= 15: f.append("farbton")
    u = "FEHLER" if any(x != "dE_warn" for x in f) else ("WARNUNG" if f else "ok")
    return u, f, {"dL": dL, "dE": dE, "dh": dh}

# ---------------- synthetischer Selbsttest (Sollwerte analytisch bzw. vorgegeben, nicht mit diesem Code erzeugt) ----------------
def _gauss(rng):
    u1, u2 = max(rng.random(), 1e-12), rng.random()
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

def _poisson(rng, n, f):
    return [(f[0] + rng.random() * (f[2] - f[0]), f[1] + rng.random() * (f[3] - f[1])) for _ in range(n)]

def _thomas(rng, eltern, kinder, sigma, f):
    out = []
    for _ in range(eltern):
        px, py = f[0] + rng.random() * (f[2] - f[0]), f[1] + rng.random() * (f[3] - f[1])
        for _ in range(kinder):
            x, y = px + sigma * _gauss(rng), py + sigma * _gauss(rng)
            if f[0] <= x <= f[2] and f[1] <= y <= f[3]: out.append((x, y))
    return out

def selbsttest():
    F = (0.0, 0.0, 50.0, 50.0); rng = random.Random(23003); erg = []; fehl = []

    def fall(nr, ok, wert):
        erg.append((nr, ok, wert)); print("%-5s %-6s %s" % (nr, "ok" if ok else "FALSCH", wert))
        if not ok: fehl.append(nr)

    # V1 Poisson (CSR): Soll R = 1, L(r) - r = 0, keine Ringe
    zuf = [_poisson(rng, 400, F) for _ in range(3)]
    for k, p in enumerate(zuf):
        ce = clark_evans(p, F); cg = clark_evans(p, F, "rand"); L = l_funktion(p, F, [1, 2, 4]); rg = ringe(p, F)
        fall("V1%s" % "abc"[k], 0.9 <= ce["R"] <= 1.1 and 0.85 <= cg["R"] <= 1.15 and max(abs(v) for v in L.values()) <= 0.3 and not rg,
             "R %.3f (Rand 5 m %.3f) L-r %s Ringe %d" % (ce["R"], cg["R"], ",".join("%.2f" % v for v in L.values()), len(rg)))
    # V2 Thomas (geklumpt): kappa 40/2500, sigma 1,5, 10 Kinder; Soll L(3)-3 = 1,64 (analytisch), R < 0,8, keine Ringe
    th = _thomas(rng, 40, 10, 1.5, F); ce = clark_evans(th, F); L = l_funktion(th, F, [3]); q = quadrate(th, F)
    ls = thomas_L_soll(3, 40 / 2500, 1.5); rg = ringe(th, F)
    fall("V2", ce["R"] < 0.8 and abs(L[3] - ls) <= 0.45 and q["vmr"] > 2 and not rg,
         "R %.3f L(3)-3 %.2f Soll %.2f VMR %.1f Ringe %d" % (ce["R"], L[3], ls, q["vmr"], len(rg)))
    # V3 Gitter 2,5 m (+-0,1 m): Soll R = 2,0 (Quadratgitter, analytisch ohne Rand), L(1)-1 = -1 (kein Paar < 2,3 m)
    gi = [(1.25 + 2.5 * i + 0.1 * (2 * rng.random() - 1), 1.25 + 2.5 * j + 0.1 * (2 * rng.random() - 1)) for i in range(20) for j in range(20)]
    ce = clark_evans(gi, F); L = l_funktion(gi, F, [1]); q = quadrate(gi, F)
    fall("V3", 1.85 <= ce["R"] <= 2.05 and L[1] <= -0.95 and q["vmr"] < 0.2 and ce["R"] > R["ce_gleichmaessig_fehler"],
         "R %.3f (Soll 2,0) L(1)-1 %.2f VMR %.2f -> FEHLER gleichmaessig" % (ce["R"], L[1], q["vmr"]))
    # V4 Ring r 3 m, 10 Steine, Mitte (20, 30), auf Poisson-Hintergrund 100 Punkte: Soll Ring, Mitte +-0,3 m, r +-0,3 m
    ring = [(20 + 3 * math.cos(a) + 0.08 * _gauss(rng), 30 + 3 * math.sin(a) + 0.08 * _gauss(rng))
            for a in (2 * math.pi * k / 10 + 0.15 * (2 * rng.random() - 1) for k in range(10))]
    p4 = _poisson(rng, 100, F) + ring; rg = [f for f in ringe(p4, F) if f["art"] == "ring"]
    t = [f for f in rg if math.hypot(f["x"] - 20, f["y"] - 30) <= 0.3 and abs(f["r"] - 3) <= 0.3]
    fall("V4", len(t) == 1 and len(rg) == 1, "Ringe %d, Treffer %s" % (len(rg), ["(%.2f, %.2f) r %.2f n %d" % (f["x"], f["y"], f["r"], f["n"]) for f in t]))
    # V5 Kieselsaum, dessen Hauptstueck entfernt wurde (Budget/Biomsperre/Reparatur): Begleiter ohne Haupt -> FEHLER
    g = [{"gid": 1, "haupt": True}] + [{"gid": 1, "haupt": False}] * 12 + [{"gid": 2, "haupt": False}] * 14
    k = gruppen_kohaerenz(g)
    fall("V5", k == {2: 14}, "Begleiter ohne Hauptstueck je gid %s" % k)
    # V6 Opferstaette (spuren anordnung ring, r 3 m, 10 Steine) mit / ohne Saeule in der Mitte
    st = [(20 + 3 * math.cos(2 * math.pi * k / 10), 30 + 3 * math.sin(2 * math.pi * k / 10)) for k in range(10)]
    f6 = ringe(_poisson(rng, 60, F) + st, F)
    m1 = [ring_mitte(f, [(20.0, 30.0, 3.1)]) for f in f6]; m0 = [ring_mitte(f, []) for f in f6]
    fall("V6", len(f6) == 1 and m1 == ["ok_erklaert"] and m0 == ["FEHLER_mitte_fehlt"], "%d Ring, mit Saeule %s, ohne %s" % (len(f6), m1, m0))
    # V7 Netzanteil: 100 Steine, ein Netz 70 % / fuenf Netze je 20 %
    a = netz_anteil(["A"] * 70 + ["B"] * 10 + ["C"] * 10 + ["D"] * 10); b = netz_anteil(["A", "B", "C", "D", "E"] * 20)
    fall("V7", a["urteil"] == "FEHLER" and b["urteil"] == "ok", "%.2f %s / %.2f %s" % (a["anteil_max"], a["urteil"], b["anteil_max"], b["urteil"]))
    # V8 Groesse: Pareto kumulativ b = 2,0 ab 0,3 m (n 2000): Soll b 2,0 +- 0,15; Einheitsgroesse 1,0-1,2 m: FEHLER
    par = [0.3 * (1 - rng.random()) ** (-1 / 2.0) for _ in range(2000)]; g1 = groesse(par)
    g2 = groesse([1.0 + 0.2 * rng.random() for _ in range(200)])
    fall("V8", abs(g1["b"] - 2.0) <= 0.15 and g1["urteil"] == "ok" and g2["urteil"] == "FEHLER",
         "b %.3f (Soll 2,0) p90/p10 %.1f / Einheit p90/p10 %.2f %s" % (g1["b"], g1["p90_p10"], g2["p90_p10"], g2["urteil"]))
    # V9 Ausrichtung: gleichverteilt (Soll Rbar2 ~ 0, p > 0,05) / Falllinie 30 Grad +- 15 (Soll Rbar2 > 0,7, zur Falllinie > 0,7)
    u = ausrichtung([180 * rng.random() for _ in range(200)], 30.0)
    h = ausrichtung([30 + 15 * (2 * rng.random() - 1) for _ in range(60)], 30.0)
    fall("V9", u["p"] > 0.05 and u["Rbar2"] < 0.15 and h["Rbar2"] > 0.7 and h["zur_falllinie"] > 0.7,
         "zufall Rbar2 %.3f p %.2f / halde Rbar2 %.3f Falllinie %.2f" % (u["Rbar2"], u["p"], h["Rbar2"], h["zur_falllinie"]))
    # V10 Reihe am Ufer: 1,5 m +- 0,1 (CV ~ 0,04) FEHLER / Exponential (CV ~ 1) ok
    r1 = reihe_cv([1.5 * k + 0.1 * (2 * rng.random() - 1) for k in range(20)])
    s = 0.0; ex = []
    for _ in range(20): s += -1.5 * math.log(1 - rng.random()); ex.append(s)
    r2 = reihe_cv(ex)
    fall("V10", r1["urteil"] == "FEHLER" and r2["urteil"] == "ok", "CV %.2f / %.2f" % (r1["cv"], r2["cv"]))
    # H1-H4 Haengen: Planerspalt bei 60 Grad, h 1 m, z_versatz 0,85 = 0,49 m (analytisch 0,85/tan 60)
    sp = planer_spalt(1.0, 0.85, 60.0)
    h1 = haengend({"oben_dz": [None] * 5, "eindring": 0.0, "wand_oben": sp, "wand_spitze": sp, "achse": 0.0, "ruecken": 70.0})
    h2 = haengend({"oben_dz": [0.01, 0.0, 0.02, 0.01, 0.03], "eindring": 0.04, "wand_oben": 0.02, "wand_spitze": 0.15, "achse": 2.0, "ruecken": 10.0})
    h3 = haengend({"oben_dz": [None] * 5, "eindring": 0.0, "wand_oben": None, "wand_spitze": None, "achse": 0.0, "ruecken": 0.0})
    h4 = haengend({"oben_dz": [0.01, 0.01, 0.02, 0.0, 0.01], "eindring": 0.05, "wand_oben": 0.02, "wand_spitze": 0.10, "achse": 40.0, "ruecken": 5.0})
    fall("H1-4", abs(sp - 0.85 / math.tan(math.radians(60))) < 1e-9 and h1[0] == "FEHLER" and "schwebt_frei" in h1[1] and h2[0] == "ok"
         and h3[0] == "FEHLER" and h4[1] == ["achse_lot"],
         "Spalt %.2f m; Wand 60 %s; Ueberhang %s; Grat %s; schief %s" % (sp, h1[1], h2[0], h3[1], h4[1]))
    # U1-U4 Farbe: grau auf grauer Halde / roetlich auf grau / schwarze Lava auf Wiese / Lava auf Lavasand
    grau, halde = srgb_zu_linear((128, 126, 122)), srgb_zu_linear((135, 133, 128))
    rot = srgb_zu_linear((170, 110, 80)); lava, wiese, sand = srgb_zu_linear((40, 38, 38)), srgb_zu_linear((95, 140, 60)), srgb_zu_linear((55, 50, 48))
    u1 = farbe_untergrund(grau, halde, True); u2 = farbe_untergrund(rot, halde, True)
    u3 = farbe_untergrund(lava, wiese, False); u4 = farbe_untergrund(lava, sand, True)
    fall("U1-4", [u1[0], u2[0], u3[0], u4[0]] == ["ok", "FEHLER", "FEHLER", "ok"],
         "%s / %s dE %.1f / %s %s dL %.1f / %s" % (u1[0], u2[0], u2[2]["dE"], u3[0], u3[1], u3[2]["dL"], u4[0]))
    sig = hashlib.sha256(json.dumps(erg).encode()).hexdigest()[:16]
    print(("SELBSTTEST OK" if not fehl else "SELBSTTEST FEHLGESCHLAGEN %s" % fehl) + "  Regeln 23.3  Faelle %d  Signatur %s" % (len(erg), sig))
    return not fehl

def lade_regeln(pfad):
    j = json.load(open(pfad, encoding="utf-8"))
    v = j.get("verteilung")
    if not v: raise SystemExit("Regeldatei ohne 'verteilung' (Version < 23.3)")
    for k in ("n_min", "ce_gleichmaessig_fehler", "zelle_m", "netz_anteil_max_50m", "netz_min_50m", "groesse_p90_p10_min", "groesse_b", "reihe_cv_fehler"):
        R[k] = v["kennzahlen"][k]
    R["ring"] = j["ringe"]["detektor"]; R["haengend"] = j["haengend"]["pruefung"]; R["farbe"] = j["farbe_untergrund"]["grenzen"]

def fenster_pruefen(pfad):
    inst = json.load(open(pfad, encoding="utf-8")); xs = [i["x"] for i in inst]; ys = [i["y"] for i in inst]
    f = (min(xs), min(ys), max(xs), max(ys)); pts = list(zip(xs, ys))
    print(json.dumps({"clark_evans": clark_evans(pts, f), "L": l_funktion(pts, f, [1, 2, 4, 8]), "quadrate": quadrate(pts, f),
                      "netz": netz_anteil([i["netz"] for i in inst]), "groesse": groesse([i["L"] for i in inst if "L" in i]),
                      "ausrichtung": ausrichtung([i["yaw_lang"] for i in inst if "yaw_lang" in i]), "ringe": ringe(pts, f)}, indent=1))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--selbsttest", action="store_true"); ap.add_argument("--regeln"); ap.add_argument("--fenster")
    a = ap.parse_args()
    if a.regeln: lade_regeln(a.regeln)
    if a.selbsttest: raise SystemExit(0 if selbsttest() else 1)
    if a.fenster: fenster_pruefen(a.fenster); raise SystemExit(0)
    ap.print_help()
```

---

## 11. Pilot T23c und Einordnung in T23

- **T23c-0 (Messweg):** Selbsttests, K25–K30 und die neun Rundgang-Stellen, nur lesend (§12).
- **T23c-1 (Kalibrierung):** Je Biom 3 gute und 3 schlechte 50-m-Fenster nach Ferats Urteil. Die R-, leer- und ΔE-Grenzen werden so
  gesetzt, dass höchstens 1 von 6 falsch urteilt. Erst danach ist der Stand 23.3 „kalibriert“.
- **T23-1 (Trockenlauf C2):** misst zusätzlich die 23c-Kennzahlen je Schicht. **T23-2** repariert in der Reihenfolge aus §6.
- **W0 (Welt, nur lesend):** Verteilungs-FEHLER je Feld × Schicht. Schichten mit > 30 % FEHLER-Fenstern kommen auf die Neuplanungsliste
  (erwartet: lava schlacke, eiszapfen, Opferstätte).
- **Abbruch:**
  - eine abweichende Signatur;
  - der Ring in C6_34 wird nicht gefunden, oder es gibt in den Gegenproben mehr als 1 Fehlalarm je 10 Fenster;
  - die Line-Trace-Differenz an K28/K29 ist > 2 cm.

  Dann den Messweg klären; es gibt keine Reparatur.

---

## 12. Nächste Handlung (genau eine, lokal)

**T23c-0: Messweg der Prüfung 23.3, nur lesend.**
- **Zuständig:** Projektleitung (Editor, Line-Traces, Pufferansicht) und Rolle 1 (Zensus, Code). Budget ≈ 90 min. Keine Projektänderung.
- **Schritte:**
  1. Alle drei Selbsttests mit `--regeln recherche/antworten/steine_sitz_regeln.json` ausführen.
  2. K25–K30 im Testlevel von T23-0 setzen und messen.
  3. Zensus der neun Rundgang-Stellen ziehen (50-m-Fenster um den Kamerablick). Darauf `verteilung_23c` je Klasse und Schicht laufen lassen,
     außerdem die Gruppenkohärenz über die gid.
  4. **C6_34:** Gibt es einen `opferstaette_vorschlag`-Punkt, und steht `SM_Column_02` dort als Akteur?
  5. **E2_24:** Line-Traces an allen `SM_EISZAPFEN_*` im Blickfeld.
  6. **B5_08 und H3_17:** die Netze und ihr wirksames MI nennen, dazu ein Screenshot der Pufferansicht BaseColor.
- **Erfolg:**
  - Signaturen `64a654746495eca8`, `dabb50741db8b9ac`, `b4ebdb213b2f71ba`; K25–K30 wie Soll.
  - Der Ring in C6_34 ist gefunden und einer Quelle aus §3.1 zugeordnet.
  - Die Eiszapfen in E2 sind als `schwebt_frei` bzw. Spalt gemeldet, und der „Zaun“ ist einem Netz zugeordnet, sonst der Gegenbefund benannt.
  - Je Bild gibt es Urteil und Zahl.
- **Abbruch:** abweichende Signatur, oder an K25/K29 ein falsches Urteil. Dann Ursache melden (Achsen, Pivot, Einheiten, Fenster); kein Weltlauf.

**Rückfragen:** keine, die T23c-0 ändern.

---

## Was fehlt bis Witcher 4

Nach Wirkung:
1. **Komposition statt Streuung.**
   - Felsen und Totholz liegen dort, wo eine Ursache sie hinlegt: Wandfuß, Rinne, Ufer, Windwurf. Dazwischen bleibt Ruhe.
   - Ein gleichmäßiges Feld (C6_28, C5_16, B5_27) fällt auf die Distanz stärker auf als jede einzelne Lücke.
   - Die Dichtemodulation und die Gruppenkohärenz in allen Planern sind der größte Hebel.
2. **Keine geometrischen Artefakte:** keine Ringe ohne Grund, keine Reihen, nichts gegen den Himmel. Ein Steinkreis ohne Mitte oder ein
   Eiszapfen-„Zaun“ zerstört eine ganze Ansicht.
3. **Ein Gestein je Ort.** Modulfarbe aus der Lage am Ort, Biom-Kind-MIs, kein Fremdgestein ohne Grund. Dazu die Landschaftslagen-Albedo
   als Datenbasis (anzulegen).
4. **Eis und Wasser mit Material:** ein Eis-MI mit Durchscheinen und Normal statt flachem Weiß; Zapfen nur an Tropfkanten. Echte
   Eisvorhänge oder Eisglasur-Decals für schräge Wände aus dem freien Bestand prüfen, vor jedem Kauf.
5. **Größenhierarchie je Gruppe:** ein dominantes Stück, Begleiter nach Potenzgesetz, Kieselsaum am Fuß statt im Kranz.
6. **Eine Prüfung für alle Planer und später für PCG.** Sitz, Wiederholung und Verteilung laufen vor dem Schreiben, nicht als Nachreparatur.

---

## Quellen (abgerufen 18.10.2026)

**Zugriff:**
- WebFetch scheiterte per DNS bei `rdrr.io`.
- Vollständig gelesen wurde nur die spatstat-Quelldatei [V]. Alles andere ist Suchauszug [S].

**Statistik:**
- [spatstat.explore R/clarkevans.R](https://raw.githubusercontent.com/spatstat/spatstat.explore/master/R/clarkevans.R) [V] – Donnelly:
  `Dpois + (0.0514+0.0412/sqrt(npts))*perim/npts`; Guard- und CDF-Korrektur.
- [spatstat clarkevans, Doku](https://www.rdocumentation.org/packages/spatstat.explore/versions/3.5-2/topics/clarkevans) [S] – R > 1 Ordnung,
  R < 1 Klumpung, Randverzerrung, Donnelly (1978) nur für Rechtecke.
- [Dixon, Ripley's K](https://pdixon.stat.iastate.edu/stat406/RipleyK.pdf) [S] und
  [spatstat Kest](https://www.rdocumentation.org/packages/spatstat/versions/1.18-2/topics/Kest) [S] – K, L = √(K/π), isotrope Randkorrektur,
  L − r > 0 geklumpt.
- Eine Literaturzahl für R in natürlichen Blockfeldern fand ich nicht (Suche „boulder Clark-Evans talus“ ohne Treffer).

**Halden und Blöcke:**
- [NHESS 19, 2249 (2019)](https://nhess.copernicus.org/articles/19/2249/2019/nhess-19-2249-2019.html) [S] – Yosemite: Blockvolumen nimmt hangab
  nichtlinear zu.
- [Alaska DGGS](https://dggs.alaska.gov/pubs/id/28436) [S] – Mehrheit der Haldenblöcke hangab ausgerichtet.
- [Montana, Sacajawea-Kar](https://scholarworks.montana.edu/bitstreams/e54f20bf-a5b1-4470-9b4e-ac4d91ab8d89/download) [S] – schwach
  hangparallel.
- [Dussauge et al. 2003](https://www.isterre.fr/IMG/pdf/DussaugeJGR-2003.pdf) [S] – Sturzvolumina nach Potenzgesetz.
- [Rosetta 67P, arXiv 1512.03193](https://arxiv.org/pdf/1512.03193) [S] – kumulativer Blockexponent Halde −3,9, distal −2,4 (Komet, nur
  Größenordnung).

**Totholz:**
- [Andrews Forest, CWD](https://andrewsforest.oregonstate.edu/sites/default/files/lter/pubs/pdf/pub4294.pdf) [S] – Wind als Hauptursache,
  räumlich gleichmäßig über Geländeklassen.

**Eis:**
- [AMS Glossary: Icicle](https://glossary.ametsoc.org/wiki/Icicle) [S] und [Weather Gamut](https://www.weathergamut.com/2015/02/11/how-icicles-form/)
  [S] – Wasser erreicht eine Kante, tropft ab und friert; auch an Felsen und Sickerstellen.

**Farbe:**
- [colour-science JND CIE1976](https://colour.readthedocs.io/en/latest/generated/colour.difference.JND_CIE1976.html) [S] – ΔE\*ab ≈ 2,3
  (Mahy et al. 1994).

**Unreal und Gestaltung:**
- [Epic FoliageType (Python API)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/FoliageType) [S] – Align to
  Normal, Align Max Angle.
- [Strayspark, procedural scatter](https://www.strayspark.studio/blog/building-believable-biomes-procedural-scatter) [S] – gleichmäßige
  Dichte wirkt künstlich.
- [Blender T84816](https://developer.blender.org/T84816) [S] – verschachtelte Streuung um Elternpunkte.

**Repo:** siehe Bezugsliste oben.
