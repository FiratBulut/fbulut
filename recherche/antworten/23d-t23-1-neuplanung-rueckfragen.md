# Antwort 23d – Deckung als Vereinigung, Lage statt Brett, Ring-Negativfall C6, Herkunft per Planausgabe, Messweg T23-0: Regeln 23.4

Gelesen: recherche/auftraege/23d-t23-1-neuplanung-rueckfragen.md @ 13a40ede53c92b887fcbce0995ae6624814c6828 (Commit d259a3a)

Stand 19.10.2026. Bearbeiter: Cloud-Recherche. Bereich: Rückfragen 1–6 aus T23-1 (C2), Weltzählung 23.3, Korrektur 23b.
**Im Projekt ist hier nichts geprüft oder angewendet.** Gerechnet habe ich nur offline auf Repo-Daten (Plan der Talkaskade, synthetischer Ring).

**Lieferung:**
- dieses Dokument;
- `recherche/antworten/steine_sitz_regeln.json` **Version 23.4**, neuer Block `nachtrag_23_4`.
  - **23.4 ist eine neue Version.** Lokal eingefroren ist 23.3 als `regeln_23c_cda6ceb0`. Dieser Stand bleibt gültig, bis die
    Projektleitung 23.4 ausdrücklich übernimmt.
  - Alle Schlüssel aus 23.1–23.3 sind unverändert.
  - Die drei Referenzcodes laufen mit der 23.4-Datei je zweimal mit unveränderter Signatur: `64a654746495eca8` (33 Fälle),
    `dabb50741db8b9ac` (49 Fälle) und `b4ebdb213b2f71ba` (14 Fälle).
  - Die neuen Regeln stehen noch nicht im Referenzcode. Rolle 1 setzt sie um.

**Bezug, ebenfalls gelesen (Commit d259a3a):**
- `antworten/23-steine-organisch-im-boden.md` @ e59924ba88b1e24579646389eb5e843cffd657e4 (§2, §10, §13 Code, §14)
- `antworten/23b-wiederholung-spiegeln-weisse-steine.md` @ 8437f810b1963f0953fa84e156e3d1d1262de0d5 (§3, §6)
- `antworten/23c-verteilungsmuster-schwebend-rundgang.md` @ 5c20bccfe6b1d64aca4300afe59a7b979852fe89 (§1–§3, §6, §11)
- `auftraege/23c-verteilungsmuster-schwebend-rundgang.md` @ 9a1f7cdc2df71225a5aaead70ad27cd7d0f68f71
- `antworten/steine_sitz_regeln.json` (Stand 23.3) @ 92f543b4ce1ed39048fdf9ca107bbba7b78d00eb
- `antworten/20-detailgrad-bachufer-felsen.md` @ 6d1b257239957030d05c4415d67bed1f20240e9b
- `skripte/detailgrad/detailgrad_plan.py` @ df77ea8cd39e612d3fcbb794157d49321d1e56e2 (`bedeckung()` Z. 621, `dichte()` Z. 1172)
- `skripte/detailgrad/detailgrad_regeln.json` @ 50922354c40a152a4cd9b84a31445d88f83f31d8
- `skripte/detailgrad/plan_p2_talkaskade.json` @ e1d91ccdea99f441073a8d74f611cf6fc6308b9d
- `antworten/21-detailgrad-landschaft-felsdeckung.md` @ 32f301737f1b63bf4931dc22b4c85c80c25169df (§(a))
- `antworten/16h-nachtrag6k-t6j-ergebnisse.md` @ bd2ee3191705d425ce7d96a826143f2de3b26667 (§6)
- `skripte/felsgruppen_plan.py` @ be2a3fe40cd3bedd3dd2eeaebaf76707cf41e4b5 (`_saum` Z. 3517–3551, `gid`)
- Bilder, selbst angesehen:
  - `bilder/platzierung/lage4/weiss_material_vorher_nachher.jpg` @ 474018663c8588bcef2a214e78c4eaf151e270af
  - `L4R_C6_L4_34_gegen_C6.jpg` @ 81928b119ccf9caeb50aa6d9933d022e870a8810

**Kennzeichnung:**
- [Repo] Daten oder Code im Repository
- [Rechnung] von mir offline gerechnet
- [Bild] eigene Ansicht
- [S] nur Suchauszug
- [Ableitung] geschlossen, nicht belegt
- [Gestaltung] Zielwert für das Witcher/RDR2-Ziel, im Pilot zu bestätigen

## Kurzfazit

1. **Korrektur 23b: Unsere Ursache war falsch.**
   - 23b §6 nannte `skjsL_tier_0`, `texndcpda_tier_0` und `SM_beach_driftwood_01` als Ursache der weißen Steine.
   - Die Ursache waren `xjijbgx_tier_0` (Fab-Raw-MI ohne Textur), `pjtsT`, `xf3odif`/`xfplcbf` und das Gras `wk2oaeyqx`.
   - Unser Fehlschluss: „kein gemessenes Y“ hieß nur „nicht gemessen“, nicht „weiß“.
   - Die Entscheidung „Material reparieren, Steine behalten“ bleibt. **Die Reparatur ist lokal erledigt und im Bild bestätigt** (§0).
2. **Dichteverlust (Frage 1): entschieden.**
   - „Felsdeckung 130–139 %“ aus 20 ist eine Summe der Grundflächen mit Überlappung, keine Deckung. Sie entfällt als Ziel.
   - Neues Ziel ist die **Vereinigung je Zone** mit Bildkriterium. Die Unionswerte aus 20 (Kante 0,75, Ufer 0,65) bleiben gültig.
   - Rechnung: Im Plan liefern die Planer-Platten 0,62–0,65 der Kantendeckung. Ohne sie bleiben 0,23 [Rechnung].
   - Das Ziel stand also zum großen Teil auf genau den Brettern, die 23 entfernt.
   - Ausgleich: **Kombination.** Erst Lage Geröll/Felsplatte, wo Bretter und Kleinschutt-Flächen weggefallen sind, dann Netze ≥ 1 m mit
     Sitzregeln. Kleinzeug nur in Grenzen.
3. **Ring C6 (Frage 2): entschieden, kein Ring.**
   - Unser Abbruchkriterium aus 23c fiel auf unseren eigenen Bildfehler zurück; es entfällt. C6_34 wird Negativfall.
   - Der Ringtest bekommt drei Zusatzbedingungen: radiale Streuung relativ ≤ 0,10, Achsverhältnis ≥ 0,6, Mitte leer.
   - Die Gruppe wird aufgelockert, aber nur beim Planer-Neulauf (WARNUNG `gruppe_einheitlich`), nicht per Werkzeug.
4. **Misch-Kürzel (Frage 3): entschieden.**
   - Neu geplant wird weiter je Planerschicht und Feld, nicht je Fenster.
   - Die Herkunft klärt ein Lookup gegen die Planausgaben. Bleibt sie unklar, ist es ein Fensterproblem in den Grenzen von 23c.
   - Zuerst kommen die 19 eindeutigen Schichten.
5. **Gruppenkohärenz (Frage 4): zulässig, mit Bedingungen.**
   - Für DETA gibt es eine echte Gruppen-ID: Planspalte `haufen` [Repo].
   - Die Nachbarschaft dient nur als Ersatz: relativ zur Größe des Hauptstücks, nur in derselben Schicht, Gruppe ab 3 Begleitern.
   - Entfernt wird nur, wenn das Hauptstück selbst FEHLER hat; sonst WARNUNG.
6. **Messweg T23-0 (Frage 5): entschieden.**
   - R1: Stufe B für Fels, Platte und Totholz ja; Stein nur für Grenzfälle; Kiesel und Kleinschutt nein.
   - R2: Träger als gedrehte Box bestätigt, neu nur innerhalb der Kern-Ellipse.
   - R3: Dreiecksmodell bestätigt. Die Richtung der Diagonale ist nicht belegt; sie wird mit dem neuen Fall K31 bestimmt.
   - R4: `e_hoehe` mit H bestätigt, so steht es in 23.
7. **T23b-S (Frage 6): Der Lava-Block reicht.** Bedingungen: Nanite aus, unsymmetrische Normalmap, Kollision. Ersatz wäre eine Testkopie
   mit Nanite aus.
8. **Weltzählung 23.3: nur Diagnose.**
   - `netz_anteil` gilt je Planerschicht ab 23.4 nur als WARNUNG.
   - Vor jeder Weltreparatur wird an bekannt guten Fenstern kalibriert (T23c-1).

**Nächste Handlung (genau eine, lokal, offline):** **T23d-D** – Deckung C2 als Vereinigung in fünf Zuständen rechnen, mit dem Plan als
Kontrollfall, und den 1 155-Vorschlag an den Kriterien in §1.4 messen (§8).

---

## 0. Bildbefund weiße Steine [Bild]

- **C2-Paare (`WMR_C2_xjijbgx_DETA`, `L4_26_wiede`, `t430_schraeg`) und B5-Halde:** Vorher sehe ich weiße, flache Flecken zwischen den
  Ufersteinen und am Hang. Nachher sind sie grau-braun und fügen sich ein.
- **B4 `pjtsT`:** Bei dieser Bildgröße sehe ich keinen sicheren Unterschied.
- **Nachher in t430:** Mitte links bleibt ein kleiner weißer Punkt. Er wirkt wie eine Blüte, nicht wie ein Stein. Mit der
  BaseColor-Pufferansicht genügt eine Bestätigung; das ist kein Auftrag.
- Formal (427 ok / 0 weiß) und im Bild ist die Reparatur bestätigt. Die Regel `textur_fehlt` aus 23b §6 bleibt die Prüfung für neue Netze.

## 1. Dichteverlust im Uferband (Frage 1)

### 1.1 Was das Ziel aus 20 misst [Repo]

- `detailgrad_plan.py` `dichte()` rechnet die „Felsdeckung (Obergrenze)“ so: **Summe** der Kastengrundflächen × Skala² geteilt durch die
  Bandfläche, „Überlappung mitgezählt“.
- 139,1 % links und 129,6 % rechts im Plan sind also keine Deckung. Werte über 100 % entstehen nur durch Überlappung und Durchdringung.
  Das hatten 6j/6k schon für die Halde festgehalten (Summe 145 %, Vereinigung 77 %).
- Dieselbe Datei misst mit `bedeckung()` die **Vereinigung**: eine boolesche Maske auf dem 10-cm-Raster.
  Die Ziele `bedeckung_stein_min` (Kante 0,75, Ufer 0,65, Hang 0,30) sind also echte Deckung. Sie bleiben gültig.

### 1.2 Wie viel davon an den Brettern hing [Rechnung]

Nachgerechnet habe ich `bedeckung()` auf `plan_p2_talkaskade.json` (s 390–578, je Seite):

| Zone | Vereinigung Plan links / rechts | Summe/Vereinigung | ohne Rolle `platte` |
|---|---|---|---|
| Kante 0–1 m | 0,88 / 0,85 (Plan meldet Median 0,88) | 1,7 / 1,6 | **0,23 / 0,23** |
| Ufer 1–3 m | 0,81 / 0,78 (0,79) | 1,5 | 0,46 / 0,42 |
| Hang 3–10 m | 0,35 / 0,35 (0,34) | 1,2 | 0,22 / 0,19 |

**Zuordnung zum Zensus:**
- Die Planrolle `platte` hat 1 172 Einträge. Genauso viele zählt T23-1 in der Klasse „DETA kleinschutt“.
- Die fünf DETA-Klassen ergeben zusammen 6 981 Instanzen. Genau so viele Planeinträge tragen eine `haufen`-Nummer.
- Beide Gleichheiten sprechen dafür, dass DETA in C2 aus diesem Plan stammt [Rechnung, Indiz].
- Der Planer füllte die Kante laut Code „Kanten-Platten bis zur Bedeckung“ (Z. 512).
- **Folgerung:** Das Ziel aus 20 war zum großen Teil mit den Brettern erfüllt, die 23 jetzt entfernt (1 099 von 1 172 weggelassen).
  Der −41 %-Verlust an Grundfläche ist deshalb erwartbar und kein Fehler der Sitzregeln.
- Instanzen −10 %, Fläche −41 %: Es fallen die großen flachen Stücke weg, nicht das Kleinzeug.

**Noch offen:**
- „1 421 → 840 m²“ lässt sich nicht mit dem Plan vergleichen, solange Bandbreite und Fußabdruck nicht genannt sind.
  Plan 0–10 m: 2 × 1 885 m² Fläche, Summe ≈ 5 060 m².
- Die 806 Instanzen „Hindernis offen“ (DETA 634, P2BE 172) sind nicht verloren. Sie zählen bis zum Hindernis-Schritt als vorhanden.

### 1.3 Entscheidung: Kombination in fester Reihenfolge

1. **Lage statt Brett** (23 §10.1 Schritt 5, jetzt verbindlich):
   - Grundriss jeder entfernten Kleinschutt-Fläche bzw. Planer-Platte plus 0,3 m wird als Lage gemalt: Geröll, auf flachem Fels Felsplatte.
   - Formel `neu = max(alt, ziel)` wie 21. Nur trocken und bei Hang ≤ 38°.
   - Das stellt genau die verlorene Fläche wieder her, ohne Netz und ohne Sitzrisiko.
2. **Netze ≥ 1 m mit Sitzregeln:**
   - Liegende Platten nur, wo die Planarität ≤ 0,5 T ist (23 §11).
   - An Böschungen ≥ 30° nehmen Blöcke 1–1,5 m, 30–50 % eingegraben, die Plätze der Bretter ein.
   - Grob: Kante 0,23 → 0,50 braucht +2,7 m² je 10 m und Seite. Das sind **≈ 4–6 Stücke ≥ 1 m** (Fußabdruck ≈ 0,55 m² nach
     Überlappung) [Rechnung, grob].
   - Hochgerechnet ≈ 190 Stücke für die Talkaskade, im Budget von C2 (45 000 / 3 000 aus 20).
3. **Kleinzeug nur in Grenzen:** K2 bis höchstens 85 je 10 m und Seite (20). K1 unter 0,1 m wird Lage, nicht Netz.
4. **Decals** nur für Lagenränder und Nasslinie (`M_MS_Decal` vorhanden, 23); nie als Deckung gezählt.

**Begründung:**
- Ohne Lage bräuchte die Kante 0,85 sichtbar aus Netzen allein. Das sind ≈ 11 Blöcke je 10 m Kante [Rechnung, grob]. Die Kante sähe wie eine Mauer aus,
  und die Reihen-CV-Regel aus 23c würde greifen.
- Die Praxis „Lage plus Decals plus wenige Hero-Netze“ für RDR2/Witcher konnte ich mit keiner Erstquelle belegen. Die Suche fand nur
  Forenvermutungen [S] und Epics Witcher-4-Demo: Kleinzeug zur Laufzeit aus Gelände- und Biomdaten [S, 22].
  Die Entscheidung stützt sich deshalb auf die Rechnung oben, nicht auf diese Praxis.

### 1.4 Ziele (23.4 `nachtrag_23_4.deckung`) [Gestaltung, Unionswerte aus 20]

| Zone | sichtbar (Netz ∪ Lage ≥ 0,5) | davon Netz-Vereinigung | Erde |
|---|---|---|---|
| Kante 0–1 m | ≥ 0,85 (Prallhang ≥ 0,90) | ≥ 0,50 (Prallhang ≥ 0,60) | ≤ 5 % |
| Ufer 1–3 m | ≥ 0,75 | ≥ 0,40 | ≤ 10 % |
| Hang 3–10 m | Rest aus Fels-/Geröll-Lage, Moos, Gras (20) | ≥ 0,25 | ≤ 10 % |

- **Lage gegen Netz:** Die Lage trägt in Kante und Ufer höchstens 0,35. Im Hang unbegrenzt.
- **Kleinzeug:** K1 höchstens 10 Netze je 10 m und Seite. K2 höchstens 85 je 10 m und Seite; im Band 0–3 m ≤ 2,8 je m², im Hang ≤ 0,5 je m².
- **Überlappungsfaktor** Summe/Vereinigung als WARNUNG: Kante ≤ 1,6, sonst ≤ 1,4. Der Plan lag an der Kante bei 1,6–1,7.
- **Bild** an den festen Kameras von 23 §14:
  - Steine 0,3–1 m sichtbar ≥ 20 je 10 m (t430/t500);
  - nackte Erde 0–3 m ≤ 10 %;
  - keine Platte wie ein Brett;
  - keine Lagenkante als gerade Linie.

**Der lokale Vorschlag mit 1 155 Grundrissen** wird nicht nach Inhalt beurteilt, sondern ist angenommen, wenn alle Punkte erfüllt sind:

| # | Kriterium |
|---|---|
| a | jedes Stück vor dem Schreiben mit `sitz_pruefung` 0 FEHLER; 23.2-Wiederholung und 23.3-Reihe/Ring ohne FEHLER |
| b | Zonenziele der Tabelle als Vereinigung erreicht, gerechnet mit Zustand D aus §8 als Basis, also Lage zuerst |
| c | Überlappungsfaktor in den Grenzen; Kleinzeug-Dichten eingehalten |
| d | kein Stück an SWR-Hindernissen oder im Wasser, solange T6N1 offen ist; kein Stück auf gesperrten Orten |
| e | Anteil Netze ≥ 1 m an der neuen Netz-Vereinigung ≥ 0,5 (wie `anteil_felsdeckung_ab_1m_min` aus 20, jetzt auf die Vereinigung bezogen) |

Er wird abgelehnt, wenn er die Kante überwiegend mit K2/K3 füllt (Punkt e) oder wenn Zustand D die Ziele schon erreicht.
Im zweiten Fall sind die Netze unnötig.

## 2. „Ring“ in C6 (Frage 2)

**Bild [Bild]:**
- Etwa 11 dunkle Schlackenbrocken liegen in einem offenen Oval. Ein Brocken liegt innen.
- Die Größen sind fast gleich (geschätzt 0,3–0,5 m), es gibt kein dominantes Stück, die Abstände sind ähnlich.
- Daneben liegen helle Kiesel in kleinen Bögen. Das ist der Farbbefund aus 23c §5, unverändert.
- Von schräg wirkt die Gruppe rund. Euer Maß von oben ist maßgeblich.

**Korrektur 23c:**
- Wir hatten aus dem Schrägbild „Kreis r ≈ 3 m, Mitte leer“ gelesen und die Opferstätte als wahrscheinlichste Quelle genannt.
  Beides ist nicht belegt.
- Der Detektor 23.3 hat richtig nichts gefunden: Mitte belegt, Fit-RMS 0,75 m weit über max(0,15; 0,6 w).
- Das Abbruchkriterium „Ring in C6_34 nicht gefunden“ (23c §11) **entfällt**. C6_34 wird Negativfall, K25 bleibt Positivfall.

**Ringtest 23.4** (`ringe_23_4`): Ring ist FEHLER nur, wenn alle 23.3-Bedingungen gelten und zusätzlich:
- **radiale Streuung relativ:** RMS(d_i − r)/r ≤ 0,10. Damit gilt die Grenze für jeden Radius gleich; die absolute 0,15 m war bei
  r = 12 m zu weit und bei r = 1,5 m zu eng.
- **Achsverhältnis** b/a aus den zweiten Momenten der Glieder ≥ 0,6;
- **Mitte leer:** In der Ellipse mit 0,5 × den Halbachsen liegt höchstens 1 Stück derselben Klasse und Schicht.
- **WARNUNG `ringartig`** bei 0,10–0,18 mit leerer Mitte: Bild bestätigen, nicht entfernen.

**Prüfung [Rechnung]:**
- Synthetischer Ring r = 3 m, 10 Steine, ±0,15 rad und σ = 8 cm: RMS/r 0,032, b/a 0,97 → Ring.
- Oval 5,8 × 2,8 m mit Stein in der Mitte: Kreis-Fit r 2,17 m, RMS 0,77 m (gemessen wurden 0,75 m), RMS/r 0,35, b/a 0,48 → kein Ring.

**Auflockern? Ja, aber nicht per Werkzeug.**
- Keine Entfernungsregel trifft zu: kein Ring, und das Fenster mit n ≈ 11 liegt unter den Mindestzahlen aus 23c §2.2.
- Ein Entfernen nach Augenmaß würde die Grenzen aus 23c umgehen.
- Neu ist die WARNUNG `gruppe_einheitlich`: ≥ 6 Stein/Fels einer Schicht, NN-Abstand ≤ 1,5 m, L p90/p10 < 1,6, kein Stück ≥ 1,5 × Median.
  Sie geht als Planerhinweis in den Neulauf der Schicht.
- Dort gilt 23c §8: ein dominantes Stück, 1,5–2,5 × Median, Begleiter nach Potenzgesetz.
- Die Herkunft (`lava_plan` schlacke oder Opferstätte) liefert der Lookup aus §3, statt einer weiteren Vermutung.

## 3. Misch-Kürzel (Frage 3)

**Entscheidung:** Neu geplant wird weiter **je Planerschicht und Feld**, denn Planer laufen je Feld und können kein Fenster einzeln neu
setzen. Das Fenster bleibt die Einheit für Diagnose und für Ausdünnen per Werkzeug.

**Zuordnung (`herkunft_zuordnung`):**
1. Jede Planausgabe wird in Weltlage umgerechnet, mit der Transformation ihres Welt-Setzers (für DETA `p2_bett_welt.py --instanzen-plan`, 20).
2. Eine Zensus-Instanz gehört zu einem Planeintrag, wenn das Netz gleich ist und der XY-Abstand ≤ 0,10 m. z wird nicht verglichen,
   weil der Welt-Setzer es ändert.
3. Genau ein Treffer heißt eindeutig. 0 oder ≥ 2 Treffer heißen unklar.
4. Ein Fenster × Klasse gehört einem Planer, wenn ≥ 80 % seiner Instanzen eindeutig dort hinführen.
5. **Unklar heißt Fensterproblem:**
   - nur Werkzeugschritte in den 23c-Grenzen: ≤ 35 % je 50-m-Fenster, ≤ 15 % je Feld, im Pilotfenster ≤ 25 %;
   - keine Neuplanung aus unklarer Herkunft;
   - braucht ein Fenster mehr, kommt es auf die Liste „Neuplanung offen, Herkunft klären“.

**Reihenfolge:**
1. Die 19 eindeutigen Schichten, **soweit ihr Listengrund ein 23.1-Instanz-FEHLER > 30 % ist**.
   Schichten, die nur über unkalibrierte Verteilungskennzahlen (`netz_anteil`, `einheitsgroesse`, `ce_gleichmaessig`) auf die Liste
   kamen, warten auf T23c-1 (§7).
2. Zensus neu ziehen, Misch-Fenster neu bewerten. Viele Misch-Fehler hängen an denselben Netzen und verschwinden mit (1) [Ableitung].
3. Den Rest als Fensterproblem behandeln.

## 4. Gruppenkohärenz ohne Gruppen-ID (Frage 4)

**Vorrang hat die echte ID** [Repo]:
- `plan_p2_talkaskade.json` hat die Spalte `haufen` (6 981 von 7 661 Einträgen: schutt 3 730, stein 1 333, platte 1 172, kies 282,
  stapel 210, block 166 …).
- Über den Lookup aus §3 ist das für DETA die Gruppen-ID. Die 212 Kiesel in C2 werden deshalb zuerst über `haufen` neu bestimmt.
- `felsgruppen_plan.py` führt intern `gid` (Z. 2949, 3550). Ob die Ausgabe sie enthält, zeigt der Lookup.

**Nachbarschaft nur als Ersatz (`gruppen_kohaerenz_23_4`):**

| Regel | Wert |
|---|---|
| Hauptstück | Stein/Fels mit L ≥ 1,0 m |
| Begleiter | Kiesel L < 0,3 m **derselben Planerschicht**, eindeutig zugeordnet (§3) |
| Abstand | Mittenabstand 0,8 r_h bis r_h + min(2,0 m; 1,5 r_h), r_h = L/2 des Hauptstücks; bei mehreren das nächste |
| Mindestgruppe | ≥ 3 Begleiter **und** Dichte im Ring ≥ 2 × Dichte derselben Klasse/Schicht in 10 m Umkreis außerhalb |
| Ausnahme (23.3) | bleibt, wenn ≤ 2 m ein anderes Stück ≥ 1 m liegt, das bleibt |

- Der Abstand folgt dem Saum des Planers (r_m + 0,5…2,0 m, `_saum`). Bei kleinen Hauptstücken ist er absichtlich enger.
  Was außerhalb liegt, wird WARNUNG, nicht entfernt.
- **Sicherung:** Per Nachbarschaft wird nur entfernt, wenn das Hauptstück im selben Lauf selbst FEHLER hat und entfernt wird.
- Fehlt das Hauptstück schon oder bleibt es: nur WARNUNG `begleiter_verdacht` und eine Bildprobe.
- Entfernte Begleiter zählen in die 23c-Grenzen.
- **Urteil zu den 212:** zulässig nur, soweit sie diese Regeln erfüllen. Ich erwarte weniger, weil die Schicht-Bedingung und die
  Dichte-Bedingung greifen [Ableitung].

## 5. Messweg T23-0 (Frage 5)

| R | Entscheidung | Begründung |
|---|---|---|
| **R1 Stufe B** | **Ja** für Fels ≥ 1 m, Platte, Totholz-Stamm (Wurzelteller-Ende) und Totholz-Wurzel. **Stein** nur für Instanzen, die in Stufe A allein über Lücke, Deckung oder Eingraben anschlagen (die „≤ 2 % warten auf B“ aus 23 §14.2). **Nein** für Kiesel und Kleinschutt | Kiesel: Toleranz 1,5 + 2 cm Raster bei < 0,3 m Größe; die Box-Abweichung liegt darunter [Ableitung]. Kleinschutt-Flächen sind dünne Karten mit flacher Unterseite. Fels und Platte: runde Flanken bzw. gewölbte Unterseiten erzeugen in Stufe A Scheinlücken; die talseitige Fels-Lücke gibt es nur in B (23 §3) |
| | In T23-0 die Punktwolke **je Netz** (nicht je Instanz) für die Netze von K3–K7, K9–K10 und K16. Stufe B muss dort dasselbe Urteil wie A liefern oder die Abweichung erklären | Der Messweg wird einmal geprüft, bevor er in T23-2 zählt |
| **R2 Träger** | **Bestätigt:** gedrehte Box. So rechnet `oberseite_bei()` schon. **Neu:** Bei Fels- und Stein-Trägern zählt die Oberseite nur in deren Kern-Ellipse (0,6 × halbe Box); in Stufe B die obere Hülle der Träger-Punktwolke | Die Boxecke über einem runden Fels täuscht Kontakt vor. Neuer Fall K32 |
| **R3 Gelände** | **Dreiecksmodell bestätigt**, bilinear entfällt (Korrektur zu 23 §2). Die Richtung der Diagonale ist **nicht belegt**: Ich fand keinen Quellauszug. Sie wird mit dem neuen Fall **K31** bestimmt: Sattel-Quad mit zwei gegenüberliegenden Ecken +0,8 m, Line-Trace in der Mitte. Ergebnis 0,8 oder 0 je nach Diagonale, bilinear wäre 0,4 | Unreal zeichnet Quads als zwei Dreiecke. Ein behobener Fehler UE-264921 „Höhe aus dem falschen Dreieck interpoliert“ (Ziel 5.6) [S, Seite nicht abrufbar] zeigt, dass auch die Höhenabfrage dreiecksbasiert ist. Abweichung bilinear ↔ Dreieck in der Quadmitte = \|h00 − h10 − h01 + h11\|/4. Eure 20 cm entsprechen 0,8 m Verwindung je 1-m-Quad, also Kanten und Knicke, wo der Sitz zählt |
| | Formel für die Diagonale (i,j)–(i+1,j+1): fu ≥ fv → h = h00 + fu(h10 − h00) + fv(h11 − h10), sonst h = h00 + fv(h01 − h00) + fu(h11 − h01). **Voraussetzung:** CollisionMipLevel 0, sonst trifft der Line-Trace eine gröbere Kollision als die Darstellung | Stufe C misst an der Kollision |
| **R4 e_hoehe** | **Mit H bestätigt**, wie 23 §2 und `messe()` in 23 §13. Lücke, Deckung und Schwerpunkt rechnen mit T. Liegt ein Stück auf (> 50 % der Kontakte auf Instanzen), wird `eingrab` nicht beurteilt (`urteil()` in 23 §13) | Eingraben heißt „im Gelände“. Auf einem Träger ist der Sitz über Lücke und Schwerpunkt geregelt |

## 6. T23b-S ohne Nanite (Frage 6)

**Entscheidung:** Ein Lava-Block mit 1,8 m genügt. Die Größe spielt für den Test keine Rolle. Nötig sind diese Bedingungen:

| Prüfgegenstand | Netz muss … |
|---|---|
| gespiegelte Darstellung (Wicklung, Culling) im Nicht-Nanite-Pfad | Nanite aus haben, belegt im Netz-Editor oder in der Nanite-Visualisierung (dort nicht eingefärbt) |
| Normalen/Tangenten | eine Normalmap mit erkennbar unsymmetrischem Detail haben. Geprüft wird im WorldNormal-Puffer, denn dunkle Lava-Albedo verdeckt Lichtfehler |
| Schatten (VSM) | wie 23b V2, unabhängig vom Netz |
| Kollision | einfache und komplexe Kollision haben (C1/C2 aus 23b) |
| Material | gebundene Texturen haben (kein `T_Default*`) |

- **Ersatz**, falls `SM_lava_m_rock_08` eine Bedingung nicht erfüllt: eine Kopie eines grauen Steins nur im Testordner, an der Kopie
  Nanite aus, nur im Testlevel.
- Projekt-Assets bleiben unverändert. Die Kopie wird danach gelöscht.
- Für den Nanite-Pfad bleibt `SM_LargeFallenTree_01` (23b).

## 7. T23-1 und Weltzählung 23.3

- **C2:** 21 496 von 41 757 Instanzen haben FEHLER (51 %).
  - Alle 8 Kreise sind getroffen. Damit ist der Treffer-Punkt aus 23 §14.2 erfüllt.
  - Noch nicht gemeldet sind die Fehlalarm-Stichprobe (20 gemeldet / 20 bestanden im Bild) und Stufe A gegen Stufe C.
  - `winkel` 5 636 an zufällig gedrehten Kieseln greift nur bei T/L < 0,7, betrifft also flache Kiesel. Ob das im Bild stört, entscheidet
    genau diese Stichprobe. Bei ≥ 3/20 Fehlalarmen gilt der Abbruch aus 23 §14.3.
- **Weltzählung:** `netz_anteil` 16 820 ist größer als die 9 455 Fenster×Schicht mit FEHLER.
  - Die Zähleinheit ist also mindestens Fenster×Schicht×Klasse, und die Fenster überlappen (Schritt 25 m).
  - Bitte die Einheit mitschreiben und Summen nicht als Flächenanteil lesen.
- **Zu streng vor der Kalibrierung: ja.**
  - Je Planerschicht misst `netz_anteil` die Palette eines einzelnen Planers, nicht das, was man sieht.
  - **23.4:** FEHLER nur im gemeinsamen Fenster aller Schichten je Klasse; je Schicht nur WARNUNG als Palettenhinweis.
- **Kalibrierung vor jeder Weltreparatur (T23c-1):** Bekannt gute Fenster sind die Gegenproben aus Auftrag 23c, soweit Ferat sie im
  Bild als gut bestätigt (C6_34 nicht), plus je Biom 3 gute und 3 schlechte Fenster.
- Eine Kennzahl, die in mehr als 1 von 6 guten Fenstern FEHLER meldet, bleibt WARNUNG.
- **Bis dahin ist die Weltzählung Diagnose:** keine Weltreparatur aus Verteilungskennzahlen. Das betrifft auch die Eiszapfen
  (5 595, davon 25 offline frei schwebend). Ihre Prüfung über Line-Traces (23c §4) bleibt davon unberührt.

## 8. Nächste Handlung (genau eine, lokal, offline)

**T23d-D: Deckung C2 als Vereinigung, fünf Zustände, 1 155-Vorschlag an den Kriterien.**
- **Zuständig:** Rolle 1, offline. Budget ≈ 60 min. Keine Projektänderung, kein Editor.
- **Eingaben:**
  - Zensus T23-1 (Talkaskade s 389–580);
  - Datensätze der Neuplanung DETA/P2BE;
  - der 1 155-Vorschlag;
  - `plan_p2_talkaskade.json` als Kontrollfall;
  - Regeln 23.4 `nachtrag_23_4.deckung`, lokal als Entwurf neben dem eingefrorenen 23.3.
- **Schritte:**
  1. **Kontrollfall:** Vereinigung je Zone und Seite auf dem Plan rechnen, mit dem Fußabdruck wie `bedeckung()`.
     - Soll: Kante 0,88/0,85, Ufer 0,81/0,78, Hang 0,35/0,35;
     - ohne Rolle `platte`: 0,23/0,23, 0,46/0,42, 0,22/0,19 (± 0,02).
  2. Fünf Zustände je Zone und Seite: Netz-Vereinigung, Lagenanteil, sichtbar, Summe/Vereinigung, K1/K2 je 10 m, Stück ≥ 1 m je 10 m.
     - **A** alt (Zensus);
     - **B** Neuplanung;
     - **C** B plus „Hindernis offen“;
     - **D** C plus Lage Geröll/Felsplatte auf den Grundrissen der weggelassenen Kleinschutt-Flächen und Platten (+0,3 m, trocken, ≤ 38°);
     - **E** D plus 1 155-Vorschlag.
  3. Den Vorschlag an den Punkten a–e aus §1.4 messen.
- **Erfolg:**
  - Kontrollfall innerhalb ± 0,02, Tabelle vollständig.
  - Daraus folgt genau eine Entscheidung:
    - D erreicht die Ziele → keine weiteren Netze, nur Lage malen (Pilot);
    - sonst E erfüllt a–e → Vorschlag als Pilot;
    - sonst Fehlbetrag je Zone in Stück ≥ 1 m je 10 m für den Planer-Neulauf.
- **Abbruch:** Kontrollfall weicht > 0,02 ab. Dann zuerst Raster, Fußabdruck oder Bandgrenze klären, keine Deckungsentscheidung.

**Rückfragen:** keine, die T23d-D ändern.

## Was fehlt bis Witcher 4

Nach Wirkung:
1. **Eine steinige Uferkante ohne Bretter.**
   - Heute fehlt nach der Sitzreparatur fast ⅔ der Kantendeckung.
   - Nötig sind eine Geröll/Felsplatten-Lage mit gutem Höhen-Blend und wenige gut sitzende Blöcke. Mehr Kleinzeug ersetzt das nicht.
2. **Übergang Stein–Lage–Boden im Material.**
   - RVT-Fuß an allen Steinen (23), Lagenränder aufgebrochen statt gerader Kanten, Nasslinie.
   - Decals nur dort, wo die Lage allein hart wirkt.
3. **Gruppen mit Hierarchie statt gleichförmiger Haufen** (C6): ein dominantes Stück, Größen nach Potenzgesetz.
   - Jeder Planer schreibt Gruppen-ID und Herkunft in seine Ausgabe. Das beseitigt auch das Misch-Kürzel-Problem an der Wurzel.
4. **Kalibrierte Prüfung vor jeder Weltreparatur.** Kennzahlen, die gute Fenster als schlecht melden, zerstören gute Stellen.
5. **Ein Messweg, der dem Bild entspricht:** Dreiecksgelände, Stufe B für große Stücke, CollisionMipLevel 0.
6. **Assets:** Geröll- und Felsplatten-Lagentexturen in Kantennähe in hoher Qualität, vor jedem Kauf aus dem freien Bestand. Ein grauer
   Nicht-Nanite-Stein ist nur für den Test nötig, nicht für das Ziel.

## Quellen (abgerufen 19.10.2026)

**Repository:** alle oben unter „Gelesen“ und „Bezug“ genannten Dateien.
- Rechnungen in §1.2 und §2: eigene Offline-Skripte auf diesen Daten, nicht im Repo abgelegt.
- Die Selbsttests aus 23/23b/23c habe ich aus den Antwortdateien entnommen und mit der 23.4-Datei je zweimal ausgeführt.

**Web, nur Suchauszüge [S]:**
- UE-264921: Höhenabfrage der Landschaft interpoliert aus dem falschen Dreieck, behoben für 5.6.
  [issues.unrealengine.com/issue/UE-264921](https://issues.unrealengine.com/issue/UE-264921). Seite aus der Cloud nicht erreichbar,
  nur der Suchauszug.
- Landscape Technical Guide: Komponenten und Sektionen aus Quads; zur Diagonale nichts.
  [dev.epicgames.com … landscape-technical-guide](https://dev.epicgames.com/documentation/unreal-engine/landscape-technical-guide-in-unreal-engine)
- RDR2/Witcher, Kleinzeug als Lage oder Decal: keine Erstquelle gefunden, nur Forenvermutungen.
  [polycount 2664599](https://polycount.com/discussion/comment/2664599),
  [polycount 2654251](https://polycount.com/discussion/comment/2654251/)
  - Ein Kommentar dort: Decals ersetzen keine echte Geometrie.
  - Daraus folgt nur die Regel „Decals nicht als Deckung zählen“, keine Studiopraxis.
