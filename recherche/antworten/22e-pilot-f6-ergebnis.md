# Antwort 22e – Pilot F6: Entfernen bestanden, Ersatz wird in F6 nachgebessert (Kiesel-Haufen, Trockengras auf Wiese), dann Ausweitung in Wellen

Gelesen: recherche/auftraege/22e-pilot-f6-ergebnis.md @ a9453c696c7b4dd39994c5c6ad100265244146bc (Commit c06d3b4)

Stand 19.10.2026. Bezug: Antworten 22 (41e3ca5) §4.2, §4.3, §6.2; 22b (3256039) §1.3, §4.1, §7; 22d (cd9a79e) §2, §4; Sitzregeln 23.1–23.4.
Bearbeiter: Cloud-Recherche. Bereich: Wasserpflanzen-Regel 22.2, Pilot F6, Ersatz `trockenbett22` r003.
Alle sechs Bilder unter `bilder/platzierung/pilot_f6/` habe ich selbst angesehen (§1).

## Kurzfazit

1. **Pilot-Urteil – beantwortet:** Der **Entfernen-Pfad ist bestanden.** Die formalen Kriterien 1–4 und 6 sind belegt, und in der
   Draufsicht stand keine der beurteilbaren entfernten Instanzen sichtbar richtig. Der **Ersatz-Pfad ist noch nicht bestanden.**
   Die beiden Bildbefunde stimmen; ich sehe sie in den Bildern genauso. Beide gehen auf unsere eigenen Regeln zurück, nicht auf die
   Ausführung (§3, §4).
   - Bei Kriterium 5 sind 2 der 20 entfernten Instanzen von oben nicht beurteilbar (Weidenkrone). Das Abbruchkriterium liegt bei
     ≥ 2 sichtbar richtigen von 20. Diese zwei müssen daher noch angesehen werden (§2).
2. **Kiesel-Haufen – beantwortet:** Ja, das wird eine eigene Klasse `kiesel_haufen` in Sitzregeln **23.5**:
   - eingraben 10–20 % der Haufenhöhe statt 40–60 %;
   - die Basiskante bleibt unsichtbar;
   - Haufen nur in der Bettsohle, nicht als Streu auf der Schlammkruste.

   Die 342 gesetzten Ersatz-Kiesel werden per Protokoll angehoben (§3). Fehler: Unsere Regel 23.1 hat Haufen wie Einzelkiesel
   behandelt.
3. **Trockengras auf grüner Wiese – beantwortet:** Ersatz gibt es nur noch auf **kahlem Boden**. Wo das alte Bett heute bewachsen
   ist, wird **gar nicht ersetzt**, auch nicht mit einer anderen Gruppe. Das entspricht der Logik von 22 §4.2: Der Boden trägt dort
   schon Bewuchs. Die Schwelle wird an den bekannten Bildstellen in F6 festgelegt (§4). Fehler: 22 §6.2 hat den Ersatz nur nach
   `d_alt` gesetzt und den heutigen Bewuchs nicht geprüft.
4. **Ausweitung – beantwortet, mit Bedingung:** Ja, aber erst nach der Nachbesserung T22-F6-2 in F6. Sonst würden beide Bildfehler
   in alle Felder getragen. Danach geht es in Wellen weiter, zuerst nur Standardbiome mit V0 ≤ 2 %. Wüste und Canyon (D4/D6) folgen
   als zweiter Pilot nach `houdini_bleibt`, wie in 22d §2 vorgesehen (§5).
5. **lily-Nachrunde – beantwortet:** Ja, starten, H5 zuerst mit einer 20er-Stichprobe von oben und schräg. Sie berührt keine Felder
   der Welle 1 und kann deshalb unabhängig laufen (§6).
6. **Nächste Handlung:** T22-F6-2 in F6 (§7).

---

## 1. Bildbefund (selbst angesehen)

| Bild | Befund | Folge |
|---|---|---|
| `f6_typisch_d5` Zeilen 1–3 | Der grüne Rohrkolben-Horst auf Riss-Schlamm ist weg, an seiner Stelle stehen niedrige, helle Büschel. In Zeile 3 sind die dunklen Horste am Steinbett entfernt. | Ziel „kein grüner Rohrkolben auf Riss-Schlamm“ erfüllt |
| `f6_typisch_d5` Zeilen 4–5 (D5) | Brücke und Röhrichtsaum am gebauten Wasser stimmen in vorher und nachher überein. | Kontroll- und Vergleichsstelle erfüllt |
| `kpb1_kiesel_zoom` | Zeile 1: Auf dem Steinbett sind Kiesel vom Bettmaterial nicht zu unterscheiden. Das wäre auch ohne Eingraben so und ist kein Fehler. In Zeile 2 (Riss-Schlamm) und Zeile 3 (Erde) sieht man je nur ein einzelnes Steinchen; die Haufen sind nicht zu erkennen. | §3 |
| `kpb_vergleich` | Bei gras4 und gras5 auf Riss-Schlamm sind die Trockengrasmatten als braune Streu zu sehen; das ist der stärkste Teil des Ersatzes. Bei gras2 neben dem Wasser liegt die Matte als runde Scheibe. In kiesel_luecke und kiesel_winkel ist nachher nichts zu sehen. In ast_hohl ist der Ast kaum auszumachen. | §3, §4; Mattenform → Witcher-Liste |
| `wpld_weg_0/1` | sp_04, sp_06 und sp_08 zeigen runde braune Scheiben in grüner Wiese. **Zusätzlich sp_15** mit demselben Muster, schwächer. sp_07 und sp_11 sind von der Weidenkrone verdeckt. sp_01 steht auf Meeressand; die Entfernung ist richtig. Bei sp_05 ist der Boden nachher deutlich heller und grauer. | §2, §4 |
| `wpld_bleibt` | Die meisten Paare stimmen überein. sp_22, sp_29, sp_34 und sp_39 sind von der Krone verdeckt. **sp_31 unterscheidet sich sichtbar:** Pflanzen am linken Rand und Schatten sind anders. Ein ToadRush als `ok_feucht` auf Riss-Schlamm ist zudem auffällig. Bei sp_36 und sp_38 ist die Beleuchtung anders. | §2 |

Mehrere Bildpaare unterscheiden sich in Licht und Schatten (sp_05, sp_36, sp_38, kpb gras4/gras5). Für die nächsten Vergleiche
deshalb nicht nur dieselbe Kamera, sondern auch **dieselbe Sonnenstellung und feste Belichtung** verwenden. Sonst lassen sich
Bodenfarbe und Ersatz nicht trennen.

## 2. Kriterien 22b §1.3: unser Urteil

| Nr | Urteil Team | Urteil Cloud | Begründung |
|---|---|---|---|
| 1–4, 6 | erfüllt | **erfüllt** | Die Belege sind vollständig berichtet: Zensus nach Neustart, Sicherungszeilen, Protokollzeilen, Rücknahme 12/12 transformgleich, Speicherbelege, nachgeprüfte Werkzeuge. Selbst nachrechnen kann ich das nicht; es liegen nur eure Zahlen vor. |
| 5 Fehlalarm | erfüllt | **wartet auf 6 Ansichten** | 18 von 20 entfernten sind beurteilbar, 0 standen richtig. Die 2 verdeckten (sp_07, sp_11) entscheiden mit: Stünden beide richtig, wäre die Abbruchgrenze (≥ 2 von 20) erreicht. Bei den behaltenen sind 4 verdeckt (sp_22, 29, 34, 39). sp_31 muss geklärt werden. |
| 7 Bild | teilweise | **teilweise → nach T22-F6-2** | Kies auf Schlamm und Erde ist nicht sichtbar (§3), Trockengras liegt als Scheiben in der Wiese (§4) |
| Abbruch | nicht ausgelöst | **nicht ausgelöst, aber noch nicht bewiesen** | siehe Kriterium 5 |

**Die verdeckten Ansichten nachholen:**

- Kamera unter der Krone, etwa 1,5–2 m über Grund, um 45° geneigt, auf den Instanzort.
- Ein Raster-Urteil ersetzt die Ansicht nicht; es kann sie nur ergänzen. Kriterium 5 verlangt ausdrücklich, dass man es sieht.
- **sp_31:** Prüfen, ob die behaltene Instanz `ToadRush_02` nachher noch an ihrem Ort steht und was sich am linken Bildrand
  verändert hat. Bei den Nachbarn ist das z. B. eine Entfernung oder ein Ersatz; die ID steht in den Protokollzeilen im Umkreis von 3 m.
  Außerdem die Rasterwerte (`nass`, `mulde`, `d_alt`) nennen, aus denen `ok_feucht` folgte.
- Fehlt die behaltene Instanz, ist das ein Fehlalarm nach Kriterium 5. Dann wird nicht ausgeweitet, sondern die Ursache gesucht.

## 3. Kiesel-Haufen: Klasse `kiesel_haufen` (Sitzregeln 23.5)

**Was falsch war:** 23.1 kennt für Kleinzeug unter 0,3 m nur die Klasse `kiesel` mit 40–60 % Eingraben. Das passt für einen
Einzelstein. `SM_SmallStonesPack_01` ist 0,26 × 0,18 × 0,16 m groß (23, Referenzliste) und besteht aus vielen kleinen Steinen auf
einer flachen Basis. Bei 50 % liegen 8 cm des Haufens unter dem Boden, und es ragen nur die obersten Steinchen heraus. Genau das
zeigt `kpb1_kiesel_zoom`.

**Neu, in `steine_sitz_regeln.json` Block `nachtrag_23_5`:**

| Teil | Regel |
|---|---|
| Erkennung | bestätigt `SM_SmallStonesPack_01/03` (Bildbefund 22e). `SmallStonesPack_02` und `_04` bis `_14` sind **zu prüfen**, darunter die Ufer-Kiesel `FT_EL_UF_SmallStonesPack_<nn>_gruen_kiesel` aus 22b §4.1. Prüfweg: Inselzahl im Netz-Export oder eine Nahaufnahme; ab 8 getrennten Inseln mit gemeinsamer Unterkante gilt `kiesel_haufen`. Vorrang vor `kiesel`. |
| Eingraben | 10–20 % der Haufenhöhe; FEHLER unter 5 % oder über 30 %. Gegenprobe am Einzelstein: 0,3–0,5 × Steinhöhe. Bei Pack_01 sind das etwa 1,6–3,2 cm. |
| Basis | Die Umrisskante darf nirgends sichtbar sein: Lücke ≤ 1,5 cm wie bei `kiesel` |
| Neigung | Träger ≤ 25° (wie `kiesel`) |
| Lage | **nur in der Bettsohle** (Tiefenlinie, `d_alt = 0`) und an Innenkurven, nicht als Streu auf der Riss-Schlamm-Fläche |
| Wasser | In Wasserzellen keine Haufen setzen |

**Grund für die Lage [Fach, allgemeine Sedimentologie, ohne Einzelbeleg]:** Ein Bach legt Kies dort ab, wo er fließt, also in der
Sohle und auf Bänken an der Innenseite. Trockenrisse entstehen dagegen dort, wo Feinmaterial in stillem Wasser abgesetzt wurde und
austrocknete. Kies, der lose auf der Schlammkruste liegt, passt deshalb nicht zusammen. Das erklärt auch, warum „Bett zeigt Kies“
im Bild schwer zu erfüllen war: In F6 ist die Sohle oft schon Steinbett (`kpb1` Zeile 1). Dort zeigt das Material den Kies; auf
dem Schlamm gehört keiner hin.

**Bestand in F6:** Die 342 Ersatz-Kiesel werden über das Protokoll angehoben: `dz = (0,50 − 0,15) × T × Skala_z`. Liegt ein Haufen
außerhalb der Sohle (`d_alt > 0`) auf Riss-Schlamm, wird er gelöscht statt angehoben. Rücknahme ist jeweils die alte Transform aus
dem Protokoll. 4 neue synthetische Prüffälle stehen im Block.

**Kriterium 7 neu gelesen:** „Das Bett zeigt Kies und Trockengras“ heißt nach dieser Korrektur:

- Die Sohle zeigt Kies, durch das Material oder durch erkennbare Haufen.
- Die Riss-Schlamm-Fläche zeigt Trockengras.
- Kies auf der Kruste ist keine Pflicht und kein Ziel.

## 4. Trockengras nur auf kahlem Boden (Regel 22.3)

**Was falsch war:** 22 §6.2 hat Ersatz gesetzt, sobald `d_alt ≤ 5 m` galt. Ob das alte Bett heute schon bewachsen ist, wurde nicht
geprüft. Auf grüner Wiese wird eine Trockengrasmatte zur runden braunen Scheibe (sp_04, 06, 08, 15).

**Neue Bedingung für jede Ersatzgruppe:** Gesetzt wird nur, wenn der Boden **kahl** ist. Ist er bewachsen, gibt es **keinen
Ersatz**. Der Boden trägt dann bereits Bewuchs; das ist dieselbe Begründung wie „fern im Trockenen“ (22 §4.2). Eine grüne Ersatzgruppe
würde nur Instanzen hinzufügen.

| Messung | Festlegung |
|---|---|
| A (zuerst) | Zahl der Gras-Instanzen der Mittelschicht im Umkreis von 1,5 m um den Ersatzort. Die Foliage-Typen der Wiesengräser sind lokal zu benennen (**zu prüfen**); der Zensus enthält sie. |
| Kalibrierung A | „Muss gesperrt werden“ an sp_04, sp_06, sp_08 und sp_15. „Muss bleiben“ an den Matten in `kpb` gras4/gras5 und am Ort aus `f6_typisch` Zeile 1. Die Schwelle legt ihr in die Mitte zwischen den beiden Gruppen. Ihr Wert wird vor der Anwendung festgehalten. |
| B (wenn A nicht trennt) | Lagen am Ort: `kahl = Schlamm + Lehm + Kies (+ Riss-Lage, Name zu prüfen) ≥ 0,5` und Gras-Lage < 0,3. Die Lagen-Namen außer Schlamm und Lehm (22 §2, `NASS_LAGEN`) sind lokal zu bestätigen. |
| Abbruch | Trennen weder A noch B die sechs Kalibrierorte: keine Schwelle raten, sondern die Werte melden |
| Meer | Kein Trockenbett-Ersatz ≤ 15 m von Meer-Wasserzellen (Fall sp_01). Den Strand bedient der Küstenplaner (Spülsaum). |

**Bestand in F6:** Die neue Bedingung wird auf die 407 Trockengras-Teile, die Äste und die Schachtelhalme angewendet. Wer durchfällt,
wird über das Protokoll gelöscht; neu gesetzt wird nichts. Gemeldet wird die Zahl je Gruppe.

**Erwartung [Annahme]:** ein Drittel bis die Hälfte, weil F6 zu 96 % Aue ist. Die Zahl entscheidet nichts; sie zeigt nur, wie oft die
alte Regel daneben lag.

## 5. Ausweitung

**Freigabe:** Nach Teamworkflow („Pilotfreigabe vor großflächigen Eingriffen“) gibt Opus-PM frei, gestützt auf die Bilder von
T22-F6-2. Unsere Empfehlung lautet: ausweiten, sobald T22-F6-2 besteht.

**Welle 1, welche Felder:** alle Felder mit T22-0b-Einträgen, die alle folgenden Bedingungen erfüllen:

- Standardbiom (Aue, Bergwald, Elfenwald, Heide);
- V0 ≤ 2 %;
- keine `gesperrt`-Fälle.

**Ausgenommen:**

| Feld | Grund |
|---|---|
| C2 | SWR-Arbeit läuft (22b §3) |
| C4 | V0 13 % (22b §7) |
| H5, I5 | Sumpf und lily-Nachrunde (§6) |
| D4, D6 und weitere Wüsten-, Canyon- und Ödlandfelder | zweiter Pilot nach `houdini_bleibt` (22d §2) |

**Ablauf je Welle:**

- Höchstens 5 Felder oder 5 000 Einträge, je Welle eine Test-ID.
- Felder mit dem höchsten Trockenbett-Anteil zuerst, weil sie F6 am ähnlichsten sind.
- Eingefrorene Liste mit SHA-256, Zensus vorher und nachher, Speicherbeleg je Paket.
- 1-%-Rücknahme und die 20/20-Draufsicht **je Welle** über die Felder verteilt, nicht je Feld. Ansichten unter Baumkronen schräg.
- Kriterium 7 je Feld mit einer festen Kamera am größten Trockenbett, gleiche Sonne.
- Abbruch je Welle wie im Piloten: ≥ 2 von 20 entfernten standen sichtbar richtig, oder ein Speicherbeleg fehlt.
- Ersatz mit 22.3 (§4) und Sitzregeln 23.5 (`kiesel_haufen`).

## 6. lily-Nachrunde

- **Starten: ja.** Nach 22d §4 ist sie eine eigene Runde mit der v3-Regel „Pflanze im Wasser“. Die Ausnahme für Bodenstreu gilt
  wie in v3.
- H5 und I5 gehören nicht zu Welle 1. Die Felder überschneiden sich also nicht, und die Runde kann von einer anderen Rolle parallel
  bearbeitet werden.
- **H5 zuerst:** 20 zufällige lily-Einträge, von oben und schräg aus 1,5–2 m angesehen. Je Eintrag wird beurteilt, ob die Pflanze
  sichtbar in Wasser oder nassem Schlamm steht oder auf einer Bult- bzw. Grasfläche.
- **Weiter in H5,** wenn höchstens 1 von 20 auf einer trockenen Bult steht. Bei ≥ 2 zuerst die Nassmaske für lily prüfen; die
  Bult-Zone ist dann zu großzügig als Wasser gezählt. Erst danach reparieren.

## 7. Nächste Handlung (eine, lokal): T22-F6-2 in F6

**Reihenfolge innerhalb des Tests:**

1. Nur lesend: die 6 verdeckten Ansichten (sp_07, sp_11, sp_22, sp_29, sp_34, sp_39) unter der Krone nachholen und sp_31 klären
   (§2). Das zuerst, weil es den Piloten noch kippen kann.
2. Kiesel-Haufen nach 23.5 anheben bzw. löschen (§3).
3. Trockengras-Bedingung kalibrieren, festhalten und anwenden (§4).

**Erfolg:**

- Kriterium 5 mit 20/20 beurteilt, ≤ 1 entfernte stand sichtbar richtig; sp_31 erklärt.
- 342 Haufen mit 10–20 % eingegraben, Lücke ≤ 1,5 cm, keiner auf Riss-Schlamm außerhalb der Sohle.
- In `kpb1` Zeilen 2–3 neu: Haufen als Gruppe erkennbar oder dort gelöscht.
- An sp_04, 06, 08, 15 keine Scheibe mehr; die Matten bei gras4/gras5 und in `f6_typisch` bleiben.
- T22 in F6 weiter mit 0 Verstößen; Zensus nach Neustart reproduziert; Speicherbeleg je Paket.
- Bilder mit gleicher Kamera, Sonne und Belichtung.

**Abbruch:**

- ≥ 2 von 20 standen richtig → nicht ausweiten, die Regel prüfen.
- Die Kalibrierorte trennen sich nicht → nur Schritt 2 anwenden, Werte melden.
- Ein Speicherbeleg fehlt.

**Danach:** Freigabe durch Opus-PM, dann Welle 1 (§5).

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Kies dort, wo Wasser ihn hinlegt:** Streifen in Fließrichtung in der Sohle und Bänke an Innenkurven statt gleichmäßiger
   Streuung. Erst das macht ein Trockenbett als ehemaligen Bach lesbar.
2. **Trockengras ohne Scheibenform:** Die Matten etwas länglich setzen (Skala 1 × 1,3–1,8, lange Achse entlang des Betts), zu 2–3
   überlappend mit 0,3–0,6 m Versatz. So wird der Umriss unregelmäßig. Die runde Scheibe ist auch auf Schlamm das auffälligste
   Restmerkmal (gras2) [Gestaltung].
3. **Vertrockneter Rohrkolben (anzulegen, 22 §6.2):** Ein brauner, geknickter Horst als Restbestand am Bettrand erzählt „hier war
   Wasser“ stärker als jede Streu. Dafür einen Bildauftrag an Codex und danach die Blender-Ableitung.
4. **Übergang Bett → Wiese:** ein Saum aus höherem trockenem Gras am Bettrand statt einer harten Grenze zwischen Riss-Schlamm und Grün.

## Quellen

- `recherche/auftraege/22e-pilot-f6-ergebnis.md` (Commit c06d3b4) und `recherche/bilder/platzierung/pilot_f6/*.jpg` (6 Bilder, selbst
  angesehen)
- `recherche/antworten/22-wasserpflanzen-fern-vom-wasser.md` §2, §4.2, §4.3, §6.2 (Commit 41e3ca5)
- `recherche/antworten/22b-wasserpflanzen-t22-0-rueckfragen.md` §1.3, §3, §4.1, §7 (Commit 3256039)
- `recherche/antworten/22d-t22-0b-ergebnis.md` §2, §4 (Commit cd9a79e)
- `recherche/antworten/23-steine-organisch-im-boden.md`: Klasse `kiesel`, Referenzmaße `SM_SmallStonesPack_01` (Commit 264a4d8)
- `recherche/antworten/steine_sitz_regeln.json`: jetzt 23.5, Block `nachtrag_23_5`
- `recherche/TEAM_WORKFLOW.md` „Feste Prüfeingaben, Nachprüfung und Pilotfreigabe“; `recherche/vorlagen/pruefung.md`

## Rückfragen

Keine, die den nächsten Schritt ändern. Die Lagen- und Grasnamen in §4 und die Haufen-Prüfung der übrigen `SmallStonesPack`-Netze
sind lokal feststellbar.
