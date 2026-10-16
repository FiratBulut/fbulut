# Antwort 16h Nachtrag 6g – Uferstufe hält in der Simulation nicht: feinere SWR, Nachfüllen nur im Bett, Ziel bei 37-cm-Zellen, Kolktiefe

**Gültigkeitskorrektur 16.10.2026 (in Ferats Auftrag):** Die Teilungsempfehlung in
Kurzfazit 1 und §1 ist historisch, kein aktueller Ausführungsauftrag. Laut
[lokalem Befund 6i §3](../auftraege/16h-nachtrag6i-baked-sim-tests-stand.md) erzeugen mehrere
SWR auf demselben Quellfluss nicht die hier angenommenen getrennten Rechenflächen.
Die anschließende Variante mit Flusskopien wurde in
[6j §1](../auftraege/16h-nachtrag6j-teilung-ergebnis.md) wegen Stillstand und trockener Nähte
verworfen. Der [aktuelle Exporter](skripte/fluss_sim/README.md) sperrt Teilungspläne.
Diese Versuche nicht allein aufgrund der folgenden historischen Empfehlung wiederholen.
Neue Varianten brauchen neue Evidenz bzw. einen ausdrücklich geänderten Testgrund.
Die übrigen Ableitungen und Zahlenziele sind damit weder pauschal widerlegt noch bestätigt;
sie müssen zum verwendeten Build und Messweg passen. Offene Fragen aus 6j bleiben offen.

Stand 13.10.2026. Bezug: `auftraege/16h-nachtrag6g-uferstufe-simulation.md` (Ferat 3b9e6b5), 6f, 6b, 6c, fluss_sim-Regeln (README
`skripte/fluss_sim/README.md`), 16a/16b/16c (Tests und Nähte).

**Kennzeichnung:**
- [Ferat]: eure Messung
- [Projekt]: unsere Regeln bzw. Daten
- [Suchauszug]: Web-Suche; Epic-Doku und Forum sind aus der Cloud nicht abrufbar (DNS), nur die Suchauszüge
- [Rechnung]: aus dem Bettplan gerechnet
- [Ableitung]: geschlossen, nicht belegt

## Kurzfazit

- **Unsere 6f-Annahme war falsch.** „Die Spline verschmiert die Stufen“ war nicht die Hauptursache. Sie erklärt 85 → 78,5 %, mehr nicht.
  - Unsere eigene Rechnung bestätigt das: Füllt man jede Zelle bis zur Spline-Höhe der Mittellinie, liegen nur **12–13 %** des Bands unter Wasser.
  - Das ist der Anteil, den die **schrägen Lippen** gegen eine eindimensionale Spline kosten [Rechnung].
  - Der Rest (65 Prozentpunkte) kommt aus der Simulation selbst. Hauptverdacht sind die 37-cm-Zellen (Ferat), dazu dünne Filme.
- **1. Feinere SWR nur für die Talkaskade:**
  - Belegt ist wenig [Suchauszug]:
    - Jede `ShallowWaterRiver` speichert ihre gebackenen Daten getrennt und nur für ihre Fläche.
    - Mehrere Flüsse bzw. SWR, die um dieselbe Kachel konkurrieren, ergaben im Forum trockene Streifen bzw. ein fehlendes Netz an der Gabelung.
    - Abhilfe dort: mehrere Water Bodies als Quelle und Senke **einer** SWR.
  - Ob zwei SWR denselben Fluss sauber teilen, ist **nicht belegt**. Unsere Teilungsregel (5 geteilte Gewässer, 8 m Überlappung, „lokal testen“) wurde nie gebacken.
  - Deshalb ein Test (§1.3): **Variante B ohne Überlappung der Rechenflächen** (oben / Talkaskade / unten, Nähte in Becken) vor Variante A (zweite SWR über der ersten).
  - Erwartung: Talkaskade ≈ 10 cm Zellen, oben ≈ 19 cm, unten ≈ 10 cm, bei ähnlicher Zellenzahl wie heute.
- **2. Nachfüllen nur im Bett:**
  - Eine 0,3-m-**Wand** am Ufer hilft nicht. Das Nachfüllen wirkt je Zelle im Band, eine Wand hält nur Strömung auf [Ableitung]. Der N5-Filter schließt Randhindernisse zu Recht aus.
  - Wirksamer ist der **Boden-Trick**: ein unsichtbarer Streifen (0,6–1,0 m breit, 0,1 m über der Schulter) nur im Bottom Contour. Zellen mit Boden über der Füllhöhe bleiben trocken.
  - Erst nach der feineren SWR testen, als Variante.
- **3. Ziel bei 37 cm:** Band 0,25–2 m ≤ 5 % ist mit 1–2 Zellen Uferstufe **nicht erreichbar**.
  - Für 37 cm schlage ich vor: **Band 0,25–1 m ≤ 30 %, Band 1–2 m ≤ 5 %**, gezählt ab 2 cm Wassertiefe. Den Rest tragen Kantengras und Ufersteine (6e).
  - Mit 10-cm-Zellen gilt das **5-%-Ziel weiter** (> 2 cm).
- **4. Kolktiefe:** **Den Plan nicht vertiefen.**
  - Erst die feinere SWR, dann die tiefste Stelle je Hauptbecken messen (Plan 0,84–1,20 m).
  - Liegt der Median dann noch unter 0,8 m: den Kolkkern breiter machen (Kern r 0,3 → 0,45), nicht tiefer.
  - Heute ändere ich den Plan nicht. Gelände-Hash f274fd1b66d7 bleibt.
- **`remove_outside` 50:** stoppt die Front bei 63 m wie F2 am Vormittag. Für die ganze Spline also **nie**.
  - Mit eigener Talkaskaden-SWR (Variante B) wäre ein Wert nur dort möglich, ohne die obere Front zu stoppen [Ableitung]. Das ist ein letzter Schritt.

## 1. Eigene SWR für die Talkaskade

### 1.1 Wie wir Teilungen im fluss_sim-Export bisher angenommen haben [Projekt]

- **Grundsatz** (Regeln v3 ff.): je Gewässer **ein** `WaterBodyRiver`. Die **Simulation** wird nur geteilt, wenn die Zelle bei 2048 über der Höchstzelle läge (Bach 0,30 m, ungeteilt bis 0,40 m).
- **Geteilt wurden 5 Gewässer** (`<gewaesser>_T00 …`):
  - je Stück eine `ShallowWaterRiver` mit `begrenzung.art = rechteck_teil` (Rechteck des Stücks)
  - **alle mit demselben `WBR_<gewaesser>` als `source_river_water_bodies` und `sink_river_water_bodies`**
- **Nähte:**
  - mindestens 5 m von jeder Stufe und 50 m von Anfang und Ende, bevorzugt in Becken (`naht.art = becken`)
  - Nachbarn **überlappen 8 m** (`s_sim_m`), `back_reihenfolge` von oben nach unten
- **Material:** je SWR `baked_sim_material` = `MI_EL_SWR_Klar`, Water-Body-Material dasselbe. Wer im Überlappbereich zeichnet, war offen.
- **Status:** Dass zwei SWR auf einem Fluss sauber aneinanderstoßen, sollte ein lokaler Test klären (`16-shallow-water-alle-gewaesser.md`, 16a T2-7: Naht ≤ 2 cm). **Dieser Test ist nie gelaufen.** Lokal wurde nur ungeteilt gebacken (16d: lange Bäche lieber ungeteilt mit gröberer Zelle).

**Folge:** Wir haben das Muster, aber keinen Beleg. Genau das prüft der Test in §1.3.

### 1.2 Was zu UE belegt ist [Suchauszug]

| Aussage | Quelle |
|---|---|
| `ShallowWaterRiverComponent` hat `baked_sim_material` (dazu Übergangs- und Unterwasser-Varianten) und `baked_sim` (nur lesbar) | Python-API-Seite `ShallowWaterRiverComponent` |
| `FShallowWaterSimParameters` hat `ResolutionMaxAxis` (int32) und `WorldGridSize`; die Komponente nennt auch `SimRes`, `SimDx`, `SourceSize` | C++-API `FShallowWaterSimParameters`, `UShallowWaterRiverComponent` |
| Die gebackenen Oberflächendaten liegen **je SWR getrennt** und enthalten nur Wasser in deren Fläche | Forum (japanisch), Thread 2738013 |
| Mehrere Flüsse in einer Kachel konkurrieren (trockener Streifen bzw. fehlendes Netz an der Gabelung); Abhilfe: weitere `WaterBodyRiver` als Quelle **und** Senke derselben SWR, Auflösung erhöhen, neu backen (berichtet für 5.7) | Forum (japanisch), Thread 2738013 |
| Nach dem Backen `Render State` zurück auf „Water Component with Baked Sim“ | Forum |
| See/Ozean als Quelle oder Senke in 5.7 instabil, in 5.8 behoben (laut Forum) | Forum, Thread 2838534 |

**Nicht belegt:**
- ob eine zweite SWR **denselben** Water Body als Quelle nutzen darf, wenn ihre Fläche in der ersten liegt
- wer dann im gemeinsamen Bereich zeichnet

Eine Grenze von 2048 für `ResolutionMaxAxis` ist bei Epic nicht belegt. Sie ist unsere Regel.

### 1.3 Test für Ferat (zuerst Kopie der Karte bzw. Stand sichern)

**Überholt:** Die nachfolgende Empfehlung von Variante B beruht auf der in 6i §3
widerlegten Flächenannahme; Flusskopien wurden danach in 6j §1 verworfen. Siehe
Gültigkeitskorrektur am Dateianfang. Keine erneute Umsetzung aus dieser Anleitung ableiten.

**Zellen** [Rechnung, Rechtecke grob nach eurem Wert ~200 × 30 m]:

| SWR | s | Rechteck (Annahme) | Auflösung | Zelle |
|---|---|---|---|---|
| heute ganz | 0–788 | 740 × 117 m | 2016 × 319 | 0,367 m |
| oben (Variante B) | 0–393 | ~390 m Achse | 2048 | ~0,19 m |
| Talkaskade | 381–587 | ~200 × 30 m | 2048 × ~300 | ~0,10 m |
| unten | 575–788 | ~210 m Achse | 2048 | ~0,10 m |

Die Talkaskade allein hat etwa so viele Zellen (≈ 0,6 Mio.) wie heute der ganze Bach. Oben und unten hängen von der Breite ihrer Rechtecke ab. Kosten fallen beim Backen und im Speicher der gebackenen Texturen an [Ableitung].

**Variante B (empfohlen), drei SWR ohne gemeinsame Mitte:**
1. Alle drei SWR nennen `WBR_ERLENBACH_P2` als Quelle und Senke (wie unsere `rechteck_teil`).
2. Rechenflächen:
   - oben s 0–393 (Naht im Anschlussbecken s 389–393)
   - Talkaskade s 385–583
   - unten s 575–788 (Naht im Kiesbett)
   - Überlappung 4–8 m nur in den Becken.
3. Backen in der Reihenfolge oben → Talkaskade → unten. Vor jedem Bake Reset **mit LIVE_SIM** (euer Fund).

**Variante A (nur falls B nicht geht):**
- Die heutige SWR bleibt ganz, eine zweite nur über s 381–587.
- Das Forum lässt dort Konkurrenz erwarten. Prüft genau, wer zeichnet: SWR einzeln ausblenden, Texturname im `baked_sim_material` der Instanz ansehen.

**Prüfkriterien** (je Variante; Messung wie 6f, Wassertiefe > 2 cm):

| Kriterium | Ziel |
|---|---|
| Front | 788/788 m, Bett ≥ 99 % nass |
| Band 0,25–2 m (Talkaskade) | ≤ 5 % |
| Naht: Spiegelsprung | ≤ 2 cm (16a T2-7); kein trockener Streifen, kein fehlendes Netz |
| Kolk | tiefste Stelle je Hauptbecken, Median ≥ 0,8 m |
| Bild | t430/t500/t550 und `C2_m_talkaskade` ohne Flackern beim Annähern (Forum: „Wasserwand“, die beim Annähern verschwindet) |

**Rückweg:** zusätzliche SWR löschen, die ganze SWR wieder auf die heutige Fläche und Auflösung (2016), Reset mit LIVE_SIM, backen.

**Alternativen, falls zwei SWR auf einem Fluss nicht sauber gehen:**
- **C – eigener `WaterBodyRiver` für s 385–583:**
  - Der obere Fluss ist Quelle, der untere Senke der Talkaskaden-SWR. Das Forum zeigt dieses Muster bei Gabelungen.
  - Gleiches Material, `overlap_material_priority` wie an der Mündung (12/10).
  - Sichtbar bleibt es ein Wasser. Technisch sind es drei Water Bodies, eine Ausnahme vom Grundsatz „ein Fluss je Gewässer“, die Ferat erlauben müsste.
- **D – `ResolutionMaxAxis` über 2048 am ganzen Fluss**, z. B. 4096 → 18 cm. Ob die Engine das annimmt, ist nicht belegt; 4-mal so viele Zellen. Nur als Speicher-Test.
- **E – Auflösung nur durch Teilen:** Ferat erlaubt Teilen ab 600 m, also mit dem Bach ist das Variante B.

## 2. Nachfüllen nur im Bett

**Wie es heute wirkt** [Ferat, 6f/6g]:
- Unter 0,3 bleibt die Front hängen.
- Mit 0,3 wird jede Zelle im Band (Spline-Breite + Zugabe) zur Spline-Höhe aufgefüllt, sofern ihr Boden darunter liegt [Ableitung aus „setzt die Nachbarzellen unter Wasser“].

| Weg | Bewertung |
|---|---|
| **Bettkante als `WH_*`-Wand 0,3 m** | **nein**: Das Nachfüllen wirkt je Zelle hinter der Wand ebenso. Eine Wand trennt nur die Strömung, dahinter bleibt stehendes Wasser hängen. Bei 37 cm ist eine schmale Wand höchstens eine Zelle breit. Der N5-Filter schließt Rand-Hindernisse aus, weil sie den Lauf einengen |
| **Boden-Trick (Bottom Contour)**: unsichtbarer Streifen auf Schulterhöhe + 0,1 m, 0,6–1,0 m breit (≥ 2 Zellen), entlang beider Ufer von der Uferstufe bis 1 m hinter die Kante; an Lippen über die Stufenwand geführt | **ja, als Variante nach der feineren SWR**. Zellen mit Boden über der Füllhöhe bleiben trocken. Er engt das Bett nicht ein (liegt außerhalb), also kein N5-Konflikt. Risiko: Liegt der Streifen in den Wasserlinie-Zellen, wird das Bett schmaler. Deshalb erst ab 0,25 m hinter der Kante. Ich kann den Streifen als Netzplan (s, u, z) aus `talkaskade_soll.f32` ausgeben (Zonen 5/6) |
| **Band schmaler nur in der Talkaskade** | ja, als zweite Variante. Spline-Breite dort = Bettbreite + 0,5 m statt + 2 m. Jetzt mit eingeschnittenem Bett hält das Bett die Front (anders als bei F2 mit bündigem Bett) [Ableitung]. Prüfen: Front 788 |
| `remove_outside` 50 | nein (Front 63 m). Mit eigener Talkaskaden-SWR wäre es nur dort testbar |

**Reihenfolge:**
1. Feinere SWR (§1.3).
2. Band schmaler in der Talkaskade.
3. Boden-Trick.
4. `remove_outside` nur auf der Talkaskaden-SWR.

## 3. Was bei 37-cm-Zellen erreichbar ist

**Rechnung aus dem Plan** [Rechnung], Band 0,25–2 m:

| Annahme | Band unter Wasser |
|---|---|
| Wasser genau auf dem Plan-Spiegel (je Becken waagrecht) | 0,1 % |
| Füllung bis zur Spline-Höhe der Mittellinie (u = 0) | 12,0 % |
| dito + 5 cm (euer „Tick“) | 13,0 % |
| dito, nur Band 0,25–1 m | 17,7 % |

- Die 12–13 % kommen von den **schrägen Lippen**. Neben einer 15–30° schrägen Lippe liegt das Ufer auf einer Seite schon im unteren Becken, die Spline an diesem s aber noch auf dem oberen Spiegel.
- **Die Uferstufe selbst ist 1–2 Zellen breit** (0,25–0,9 m). In einer 37-cm-Zelle mittelt die Simulation Bett und Stufe. Die erste Zelle hinter der Kante liegt dann meist unter Wasser, die zweite oft mit einem dünnen Film [Ableitung].
- Das sind etwa 0,4–0,7 m des 1,75 m breiten Bands, also 20–40 %. Zusammen mit den schrägen Lippen sind **30–45 %** bei 37 cm realistisch.
- Die gemessenen 78,5 % liegen darüber. Der Rest sind vermutlich dünne Filme.
  - **Bitte aus demselben Dump ausgeben:** Anteil nass im Band bei Tiefe > 1 / 2 / 5 / 10 cm.
  - Sieht man bei > 5 cm nur noch 20–30 %, ist der „graue Film“ das eigentliche Bildproblem. Dann helfen Kantengras und Ufersteine mehr als jede Simulationseinstellung.

**Kriterium:**
- **37 cm:** Band 0,25–1 m ≤ 30 % und Band 1–2 m ≤ 5 %, je bei Tiefe > 2 cm. Die Kante verdecken Kantengras (279, 6e), Moos und Randblöcke.
- **≤ 10 cm (eigene SWR):** Band 0,25–2 m ≤ 5 % bei > 2 cm bleibt.

## 4. Kolktiefe

- **Heute:** Bett-p90 0,59 m [Ferat] ist kein Kolkmaß (6f §4). Die Kolkkerne sind ~0,7 m breit (Kern r < 0,3 bei 2–2,6 m Breite), bei 37 cm also 2 Zellen. Die Simulation glättet sie.
- **Tiefer planen (1,3–1,5 m) nicht:**
  - Mit 37 cm würde nur ein Teil davon ankommen. Die Wände zur Stufe würden steiler, was im Bild als Loch wirkt.
  - Mit 10 cm kommt der Plan ohnehin an.
- **Reihenfolge:**
  1. Feinere SWR.
  2. Tiefste Stelle je Hauptbecken messen (Ellipse aus `becken[].kolk`).
  3. Ist der Median unter 0,8 m: Kern breiter (r 0,3 → 0,45), dann Plan neu (0 FEHLER, byte-gleich).
- Heute keine Änderung. Gelände und Instanzen bleiben auf Stand f5e33b6.

## Was fehlt bis Witcher 4 (Talkaskade, Stand 6g)

Messlatte wie 6e: dichte Vegetation bis an die Kante, Wind, weiches Licht, klare Wasserformen. Die Techdemo ist nur über Suchauszüge belegt.

Nach Wirkung:
1. **Wasser bleibt im Bett:** feinere SWR (§1), sonst Boden-Trick (§2). Ohne das liegt ein grauer Film über Ufer und Gras. Das ist heute der größte Abstand zum Ziel.
2. **Kante verdecken und beleben:** Kantengras, Moos und Farne aus 6e bauen. Selbst mit perfekter Simulation bleibt die Wasserlinie bei 37 cm unscharf.
3. **Wände entdunkeln:** Lagen je Zone (6f §3) und Bach-Ton nach Höhe.
4. **Kolke lesbar:** nach der feineren SWR messen, `MI_EL_SWR_Bergbach` (6f §4).
5. **Blöcke im Maßstab und nass:** 6f §5.
6. Totholz, Fall-Effekte, Licht im Einschnitt (6e).

## Rückfragen

1. Ab welcher Wassertiefe zählt `p2bett_pruefband.py` eine Zelle als nass? Bitte das Band bei 1 / 2 / 5 / 10 cm ausgeben (§3).
2. Wie legt euer Bauwerkzeug die Rechenfläche einer SWR fest (Actor-Box, Spline-Grenzen oder `begrenzung.rechteck_cm`)? Davon hängt ab, ob Variante B ohne Codeänderung geht.
3. Soll ich den Boden-Trick-Streifen (§2) schon jetzt als Netzplan ausgeben, damit er für den Test bereitliegt?

**Quellen** [Suchauszug, Seiten nicht abrufbar]:
[Python-API ShallowWaterRiverComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent),
[FShallowWaterSimParameters](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/FShallowWaterSimParameters),
[UShallowWaterRiverComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent?lang=en-US),
[Forum: ShallowWaterRiver (Gabelung, Quelle/Senke)](https://forums.unrealengine.com/t/shallowwaterriver/2738013),
[Forum: ShallowWaterRiver – Lake/Ocean](https://forums.unrealengine.com/t/shallowwaterriver-lake-ocean/2838534),
[Forum: Baked River Simulations – Parameter Reference](https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112),
[Forum: Simulation startet nicht in 5.7.4](https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772).
