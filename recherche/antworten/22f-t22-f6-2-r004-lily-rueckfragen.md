# Antwort 22f – Kriterium 5 erfüllt, aber drei „behaltene“ Ansichten zeigen den falschen Ort; r005 mit Strand-Regel; Kiesel nach Tabelle; Haufenmaß war unser Fehler

Gelesen: recherche/auftraege/22f-t22-f6-2-r004-lily-rueckfragen.md @ ecb5f0a5480cc453dc397a4a9c578cc8b0621ff6 (Commit f2c2f88)

Stand 19.10.2026. Bezug: Antwort 22e (3c99edc), Sitzregeln 23.5 (`regeln_23e_d5cc8d04`), jetzt 23.8. Bearbeiter: Cloud-Recherche.
Bereich: Pilot F6 (T22-F6-2), Ersatz `trockenbett22` r004, lily-Nachrunde. Bild `bilder/platzierung/pilot_f6/t22f62_verdeckt_12.jpg` selbst
angesehen (§2).

## Kurzfazit

1. **Kriterium 5 (entfernte Stichprobe) – beantwortet, erfüllt:** Die 20 entfernten Stichproben sind sp_01–sp_20. Verdeckt waren davon nur
   sp_07 und sp_11; beide stehen auf trockenem Boden. Damit sind **20/20 beurteilt und 0 standen sichtbar richtig.**
2. **sp_22, 29, 34, 39 gehören zur Stichprobe der *behaltenen* Pflanzen** (`wpld_bleibt`), nicht zu den entfernten. sp_29 ist deshalb kein
   Grenzfall einer Entfernung.
   - **Neuer Befund:** Bei sp_22, sp_34 und sp_39 steht im roten Kreis ein brauner r003-Trockengrasbüschel und **keine ToadRush**.
   - Ersatz wird am Ort einer *entfernten* Instanz gesetzt. Die Kameras zeigen also wahrscheinlich den Ort einer entfernten Pflanze und nicht
     den der behaltenen; falsch wäre dann die Koordinatenliste.
   - Die andere Möglichkeit wäre, dass eine behaltene Pflanze fehlt; dagegen spricht euer Zensus-Abgleich (0 außerhalb der Auswahl).
   - Das ist zuerst zu klären, lesend (§2).
3. **lily-Schrägsicht – beantwortet:** Sie ist nicht nachträglich nötig. Die Entscheidungsregel aus 22e §6 war „weiter, wenn höchstens 1 von
   20 auf trockener Bult steht“. Selbst wenn der Grenzfall als trocken zählt, ist sie erfüllt. Die Schrägsicht hätte die Entscheidung nicht
   geändert (§1).
4. **Kiesel: Die Tabelle gilt** (Sohle; Innenkurven, sobald eine Erkennung existiert). r004 mit 1 Haufen ist richtig. Der Abschnitt
   „Bestand“ in 22e §3 und das Erfolgskriterium „342 Haufen“ in §7 widersprachen der Tabelle. Das war unser Fehler (§3.1).
5. **Kahl-Lagen:** Alle unbewachsenen Lagen gelten als kahl, also auch Geröll; r004 bleibt so. Neu ist nur: **kein Trockengras auf Fels,
   Felsplatte oder Sandstein ≥ 0,5** (ohne Boden kein Gras). Äste bleiben dort zulässig (§3.2).
6. **Schwellen B:** Es gilt die Mitte der Kalibriergruppen (r004). Die festen Werte in 22e waren Platzhalter vor der Kalibrierung (§3.3).
7. **Meer-Regel:** Sie gilt nur noch für **Strand**: Sand-Lage ≥ 0,5 **und** ≤ 15 m von Meer-Wasserzellen. Trockenbetten an Mündungen auf
   Geröll oder Erde bekommen Ersatz. Das ergibt eine neue Revision r005 (§3.4).
8. **Haufenmaß – unser Fehler:** `SM_SmallStonesPack_01` misst laut `vorlagen/daten/netze_masse.json` 13,1 × 9,2 × 8,3 cm. Unsere
   0,26 × 0,18 × 0,16 m waren um Faktor 2 zu groß. r004 rechnet richtig mit 8,3 cm. Regeln 23.8 korrigieren die Texte (§3.5).
9. **Lehm in der Nassmaske:** Wahrscheinlich ja, Lehm sollte heraus. Das wird zuerst lesend geprüft, für T22 und nicht für den Sumpfplaner (§3.6).
10. **Weitere Haufen-Netze:** `_08` und `_10` gelten wie `_01`/`_03` als Haufen. `_02` und `_04`–`_07` werden per Nahaufnahme oder
    Dreiecks-Export (T23e-3) bestimmt, je nachdem, was zuerst vorliegt. Für F6 blockiert das nichts (§3.7).
11. **Nächste Handlung:** T22-F6-2 abschließen: zuerst die drei Ansichten, dann r005, Nachprüfung und Setzen (§4).

---

## 1. lily-Nachrunde

- **Formal sauber:** 2 016 entfernt, alle aus der Auswahl, 0 außerhalb und 0 hinzugekommen, Rückweg je Feld gesichert.
- **Schrägsicht nicht nachholen.** Sie sollte entscheiden, ob in H5 mehr als 1 von 20 auf trockener Bult steht. Mit 19 klar im Wasser und
  1 Grenzfall ist die Regel auch dann erfüllt, wenn der Grenzfall als „trocken“ zählt. Eine Nachprüfung, die das Urteil nicht ändern kann,
  bringt nichts.
- **E5:** Die 94 Landpflanzen im jetzt gebauten Bach, darunter 11 Bäume und 9 Büsche, sind nach der v3-Regel richtig entfernt. Eine Draufsicht
  auf den Bach danach ist aber sinnvoll. Wo Bäume im Bett standen, kann am Ufer eine Lücke im Gehölz entstehen (siehe Witcher-Liste).

## 2. Verdeckte Ansichten (selbst angesehen)

**Zuordnung nach `wpld_weg_0/1` und `wpld_bleibt` aus 22e:**

- entfernt: sp_01–sp_20;
- behalten: sp_21–sp_40.

| Ort | Stichprobe | Bild (rotes Kreuz = Ziel) | Urteil |
|---|---|---|---|
| sp_07 | entfernt | trockener Sand-/Erdboden unter der Weide | stand falsch → Entfernung richtig |
| sp_11 | entfernt | trockener Riss-Schlamm | stand falsch → Entfernung richtig |
| sp_22 | **behalten** (`ToadRush_00`, feucht) | im Kreis ein brauner Trockengrasbüschel mit Ast, keine ToadRush | **Ort prüfen** |
| sp_29 | **behalten** (`Rohrkolben_Jung`, feucht) | dichtes Röhricht mit Kolben; die Pflanze steht im Bestand | unverändert, plausibel |
| sp_34 | **behalten** (`ToadRush_02`, feucht) | im Kreis ein brauner Büschel auf Riss-Schlamm, keine ToadRush | **Ort prüfen** |
| sp_39 | **behalten** (`ToadRush_00`, feucht) | im Kreis ein brauner Büschel auf Riss-Schlamm, keine ToadRush | **Ort prüfen** |

**Kriterium 5:**

- **Entfernt:** 20/20 beurteilt, 0 standen sichtbar richtig. Der Abbruch (≥ 2) ist nicht ausgelöst.
- **Behalten:** 3 Ansichten zeigen nicht die behaltene Pflanze. Sie zählen deshalb noch nicht.

**Zwei mögliche Ursachen, ein lesender Test:**

- **U-a, Koordinatenliste:** Die Kameras haben die Liste der *entfernten* Pflanzen benutzt. Dafür spricht der braune Büschel im Kreis: Ersatz
  steht am Ort der ersten entfernten Instanz ± 0,5 m.
- **U-b, Pflanze fehlt:** Die behaltene Pflanze fehlt. Dagegen spricht der Zensus-Abgleich, der 0 Entfernungen außerhalb der Auswahl zeigt.

**Test:** Die Instanz-IDs von sp_22/34/39 aus `wpld_bleibt` im aktuellen Zensus nachschlagen und mit der Kameraposition vergleichen.

- **Erwartung bei U-a:** Die ID existiert, und ihr Ort liegt mehr als 0,5 m vom Kreis entfernt. Dann die 3 Kameras auf diesen Ort neu
  stellen; erwartet wird die grüne ToadRush.
- **Erwartung bei U-b:** Die ID fehlt. Dann ist das ein Fehlalarm nach Kriterium 5. Nicht setzen und nicht ausweiten, sondern die Ursache
  in der Entfernungskette suchen.

**Nebenbefund:** Behaltene ToadRush „feucht“ auf trockenem Riss-Schlamm (sp_31, sp_34 laut Liste) passen zu Frage 6 (§3.6).

## 3. Antworten zu den Fragen

### 3.1 Kiesel-Lage (Frage 1)

- **Die Tabelle gilt:** Haufen nur in der Bettsohle (`d_alt = 0`), später auch an Innenkurven.
  - **Außerhalb der Sohle auf Riss-Schlamm:** Dort ist Kies falsch.
  - **Außerhalb der Sohle auf Geröll:** Haufen bringen dort nichts. Sie sind vom Steinbett nicht zu unterscheiden (`kpb1_kiesel_zoom`
    Zeile 1) und kosten nur Instanzen.
- **r004 bleibt mit 1 Haufen.** Neue Haufen in der Sohle setzt dieser Pilot nicht. „Bett zeigt Kies“ erfüllt in F6 das Steinbett-Material.
- **Korrektur 22e:**
  - Der Satz in §3 „Bestand“ lautet richtig: „gelöscht, wenn außerhalb der Sohle (`d_alt > 0`)“.
  - Das Erfolgskriterium in §7 lautet richtig: „verbleibende Haufen mit 10–20 % eingegraben, Lücke ≤ 1,5 cm, keiner außerhalb der Sohle“.

### 3.2 Kahl-Lagen (Frage 2)

- **Geröll gilt als kahl.** Das Kahl-Kriterium sollte braune Scheiben auf grüner Wiese verhindern. Auf Geröll, Erde und Sand stört Trockengras
  nicht; trockene Büschel im Kiesbett sind natürlich. Die Liste in 22e §4 B war zu eng. r004 setzt die Absicht richtig um.
- **Neu (22.3):** Kein Trockengras, wo Fels, Felsplatte oder Sandstein ≥ 0,5 liegt, denn auf blankem Fels ohne Boden wächst kein Gras. Äste
  bleiben dort zulässig. r004 meldet dazu die Zahl; ist sie 0, ändert sich nichts.

### 3.3 Schwellen B (Frage 3)

- **Es gilt die Mitte** (K ≥ 0,5075, G < 0,4448). Die festen Werte in 22e waren Startwerte. Eine Kalibrierung an bekannten Orten geht
  vor, und für Messung A hatten wir das ausdrücklich so verlangt; für B gilt dasselbe Prinzip.
- **Beleg:** Der Nachprüfer findet 11 der 23 zusätzlichen Fälle bei G < 0,3 auf Geröll (sp_05/sp_13), nicht auf Wiese. Die feste Schwelle
  hätte also falsch gestrichen.

### 3.4 Meer-Regel (Frage 4)

- **Unser Grund war sp_01:** eine Pflanze am Meeressand. Die Regel war aber zu breit; sie traf Trockenbetten an Mündungen auf Geröll (226)
  und Erde (69).
- **Neu (22.3):** Kein Trockenbett-Ersatz, wenn **Sand ≥ 0,5 und ≤ 15 m von Meer-Wasserzellen**; dort gilt der Strand und der
  Küstenplaner. Sonst gilt die normale Regel. Äste an Mündungen lesen sich ohnehin als Treibholz.
- **Folge:** Revision **r005** = r004 + Strand-Regel + kein Trockengras auf Fels-Lagen (§3.2). Kahl-Bedingung, Hang ≤ 25°, `karte_weg` und
  Wasserzellen gelten unverändert. Erwartung: deutlich mehr als 295 Teile, höchstens 512. Die genaue Zahl entscheidet nichts.

### 3.5 Haufenhöhe (Frage 5)

- `netze_masse.json` nennt für `SM_SmallStonesPack_01` min/max ±6,55 / ±4,62 / ±4,15 cm, also 13,1 × 9,2 × 8,3 cm. Das stimmt mit eurer
  Punktwolke überein.
- Die 0,26 × 0,18 × 0,16 m stammen aus der Klassenliste im Selbsttest von Antwort 23 und sind dort um Faktor 2 falsch.
  - Die Klasse bleibt richtig: L 0,13 m < 0,3 m, also `kiesel` bzw. `kiesel_haufen`, Größenklasse K2.
  - Selbsttest und Signatur sind nicht betroffen.
- In 22e §3 stimmt deshalb „8 cm im Boden“ nicht; richtig sind etwa 4 cm. Der Bildbefund (Haufen verschwinden) bleibt.
- **Regeln 23.8:** Die Texte in `nachtrag_23_5` sind korrigiert: Gegenprobe Einzelstein ≈ 0,8–1,7 cm, Prüffall T 0,083 m. Die Schwellen
  (10–20 % von T) sind unverändert.

### 3.6 Lehm in der Nassmaske (Frage 6)

- **Wahrscheinlich ja:** Lehm zeigt im Bild trockenen Riss-Schlamm. Gerade auf ihm sollten die grünen Rohrkolben weg. Mit Gewicht 0,4
  hält Lehm aber Pflanzen als `ok_feucht` fest.
- **Nur für T22 ändern, nicht im Sumpfplaner** (`sumpf_regeln.json`): Die Nassmaske dort steuert Bulten und Nasswiese, und F6/H5 sind schon
  bearbeitet.
- **Erst lesend prüfen (T22-L0):**
  - T22 mit Lehm-Gewicht 0 über alle Felder; zählen, wie viele `ok_feucht` dadurch zu Verstößen werden, je Feld.
  - 10 davon in der Draufsicht ansehen.
  - **Entscheidung:** Stehen ≥ 8 von 10 auf trockenem Riss-Schlamm, gilt Lehm 0 ab Welle 1 (Regel 22.3). Sonst bleibt 0,4, und die
    Ausnahmen sind zu benennen.
- sp_31 bleibt so oder so stehen; `ok_feucht` folgt dort aus der Mulde (0,80 m).

### 3.7 Weitere SmallStonesPack-Netze (Frage 7)

- `_08`–`_14` entsprechen in den Maßen `_01`–`_07` (`netze_masse.json`, je Paar bis auf Millimeter gleich). `_08` und `_10` gelten deshalb
  wie `_01`/`_03` als Haufen.
- `_02` und `_04`–`_07` (und damit `_09`, `_11`–`_14`): Haufen oder Einzelstein entscheidet eine Nahaufnahme je Netz oder der
  Dreiecks-Export aus T23e-3, je nachdem, was zuerst vorliegt. Das blockiert F6 nicht (r004 enthält nur 1 Haufen).

## 4. Nächste Handlung (eine, lokal): T22-F6-2 abschließen

1. **Lesend:** sp_22/34/39 nach §2 klären (Zensus-Lookup, gegebenenfalls 3 Kameras neu auf den Ort der behaltenen Instanz).
2. **r005** nach §3.2/§3.4 rechnen, unabhängig nachprüfen lassen, dann setzen. Je Paket ein Speicherbeleg, danach Neustart und Zensus.
3. **Bilder:** sp_04/06/08/15, gras4/gras5/fix_1 und 2 Mündungsorte mit wiederhergestelltem Ersatz. Gleiche Kamera, Sonne und Belichtung.

**Erfolg:**

- Die behaltenen sp_22/34/39 stehen und sind sichtbar.
- r005 ist formal sauber: Zugaben = Protokollzeilen, 0 fremd, Rücknahme-Stichprobe 1 % transformgleich.
- T22 in F6 hat weiter 0 Verstöße.
- Keine Trockengras-Scheibe auf Wiese.

**Abbruch:** Eine behaltene Instanz fehlt (U-b), oder ein Speicherbeleg fehlt. Dann nicht ausweiten.

**Danach:** T22-L0 (lesend), dann Welle 1 nach 22e §5 mit Regel 22.3:

- Kahl = unbewachsen, ohne Trockengras auf Fels;
- Strand-Regel;
- Schwellen aus der Kalibrierung;
- Lehm je nach T22-L0.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Ufergehölz am neuen Bach E6_K2:** Nach dem Entfernen von 11 Bäumen und 9 Büschen aus dem Bett das Ufer prüfen und Gehölz an den Rand
   setzen (Erle oder Weide in der Aue). Ein Bach ohne Ufergehölz wirkt kahl.
2. **Kies dort, wo Wasser ihn ablegt:** Kies-Streifen in der Sohle und Bänke an Innenkurven als spätere Planer-Regel. Der Pilot setzt dafür
   bewusst nichts.
3. **Trockengras als unregelmäßige Fläche** statt runder Matten (22e Witcher-Liste Punkt 2). Mit r005 kommen mehr Matten auf Geröll; dort
   fällt die Scheibenform am stärksten auf.
4. **Feuchte-Abstufung** über eine richtige Nassmaske ohne Lehm (§3.6): grüne Binsen nur dort, wo der Boden nass aussieht.

## Quellen

- `recherche/auftraege/22f-t22-f6-2-r004-lily-rueckfragen.md` (Commit f2c2f88), Bild `bilder/platzierung/pilot_f6/t22f62_verdeckt_12.jpg`
  (selbst angesehen)
- `recherche/antworten/22e-pilot-f6-ergebnis.md` §2–§7 (Commit 3c99edc); Bilder `wpld_weg_0/1.jpg`, `wpld_bleibt.jpg` (Stichproben-Zuordnung)
- `recherche/antworten/22-wasserpflanzen-fern-vom-wasser.md` §2 (`NASS_LAGEN`), §4.3, §6.2 (Commit 41e3ca5)
- `recherche/vorlagen/daten/netze_masse.json`: Einträge `SM_SmallStonesPack_01` bis `_14`
- `recherche/antworten/23-steine-organisch-im-boden.md`: Klassenliste im Selbsttest (Commit 264a4d8)
- `recherche/antworten/steine_sitz_regeln.json`: jetzt 23.8 (Textkorrektur `nachtrag_23_5`)

## Rückfragen

Keine, die den nächsten Schritt ändern.
