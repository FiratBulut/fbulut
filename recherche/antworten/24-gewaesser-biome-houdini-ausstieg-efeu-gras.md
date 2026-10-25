# Antwort 24 – Gewässer je Biom als Regeldatei; Aue als Pilot 2; Wasserfälle als Unreal-Vorhang mit Nature Water FX; Efeu nur in feuchten Waldbiomen; Gras unter Fels per Ausschluss-Boxen; Punkte 8–10

Gelesen: recherche/auftraege/24-gewaesser-biome-houdini-ausstieg-efeu-gras.md @ ccf640483cf171f9324188c73a0f64ba94df10af (Commit 2806444)

Stand 25.10.2026. Bearbeiter: Cloud-Recherche. Bereich: Gewässer aller Biome nach dem Erlenbach-Muster, Seen, Wasserfälle, Efeu,
Landschafts-Gras an Felsen, Kragarm-Regel, Kante, T11.

**Weitere gelesene Eingaben:** 16h (Hauptantwort), 16h-6f, 6h, 6i, 6t; 17; 18; 23f; 23i; `verteilung-KONVENTIONEN.md`;
`bachbett_ufer_regeln.json`; `skripte/sehens_lib/bachbett_regeln.json`; `steine_sitz_regeln.json` (23.1–23.11);
`vorlagen/daten/biome_je_feld.json`, `sehens/wasser_welt.json`, `sehens/baeche_alle.json`, `sehens/teiche.json`,
`wasser_fx/wasserfaelle.json`; `fluss_sim/zusammenfassung.json`.

**Kennzeichnung:** [Ferat] euer Befund · [Projekt] Daten bzw. Regeln im Repo · [Quelle] Engine-Quelltext · [Doku]/[Forum] Epic-Seiten,
nur als Suchauszug (`dev.epicgames.com` und die Foren sind aus der Cloud gesperrt) · [Fach] Literatur · [Ableitung] gerechnet oder
geschlossen · [Gestaltung] gesetzt · **zu prüfen** = lokal klären.

**Lieferung:**

| Datei | Inhalt |
|---|---|
| [`gewaesser_biome_regeln.json`](gewaesser_biome_regeln.json) | 13 Biom-Regelsätze (Bett, Lagen je Zone, Deckung, Totholz, Vegetation, Wassermaterial), Seen, Wasserfälle, Efeu, Gras unter Fels, Rollout |
| [`skripte/gewaesser_biome/gewaesser_biome_regeln_erzeugen.py`](skripte/gewaesser_biome/gewaesser_biome_regeln_erzeugen.py) | erzeugt die JSON und prüft sie. Ergebnis: Selbsttest OK (56 Lagenmischungen, 13 Biome). Zwei Läufe sind byte-gleich. Drei absichtlich eingebaute Fehler werden erkannt (Summe 105, MI-Name doppelt belegt, unbekannte Lage) |

---

## Kurzfazit

1. **A1 Bäche/Flüsse je Biom – beantwortet** (Regeln in der JSON, Kurzfassung §1.3).
   - Die Bettform hängt am Gefälle (Montgomery & Buffington). Das Biom wählt nur die bevorzugten Formen und den Belag.
   - Die SWR-Werte hängen an Breite und Länge, nicht am Biom. p2-Werte bleiben; Zelle = B/12 zwischen 0,15 und 0,40 m.
   - Neu sind je Biom die Lagen in vier Zonen, Deckungsfaktoren zur Talkaskade und ein eigenes Wassermaterial als Kind von
     `MI_EL_SWR_Bergbach`, mit gerechneter Helligkeit des Grundes.
   - Totholz und Uferstreifen bleiben in `bachbett_regeln.json` und werden nur verwiesen.
2. **A2 Seen – beantwortet.**
   - Epic-See mit `affects_landscape = False`, Rand 0,5–2 m im Gelände versteckt.
   - Genau ein Wasserkörper je Becken: Ferats „See im See“ ist sehr wahrscheinlich Epic-See plus Houdini-Spiegel.
     `wasser_welt.json` nennt als Quelle „Houdini-Spiegel, wo Becken hält“ [Projekt].
   - Uferform nach Hangneigung, Verlandungsreihe für das Flachwasser.
   - Bach-Anschluss: Der See ist Senke, Spline 5–10 m in den See. Ob die SWR einen See als Senke annimmt, ist in 5.8 nicht
     dokumentiert (**zu prüfen**, §2.3).
3. **A3 Wasserfälle ohne Houdini – beantwortet.**
   - Vorhang bzw. Kaskade als Netz, in Unreal erzeugt (Spline-Band oder Geometry Script), mit dem vorhandenen Material
     `MI_EL_Wasserfall`.
   - Nature Water FX an Lippe und Fuß; SWR als Zulauf und Becken.
   - Ein Epic-Fluss über die Kante ist keine Option (zerfällt in Teilflächen [Forum, 14b]).
   - Mindestregeln für Abwurf, Strahlzerfall, Becken und Herkunft (17) stehen in §3. Damit können eure Aufträge 175–184 anlaufen.
4. **A4 Rollout – beantwortet: Pilot 2 = Aue.**
   - Die Aue hat 33 % aller Laufmeter (14,7 von 44,6 km).
   - Sie schließt im Feld C3 (61 % Aue) direkt an die p2-Mündung an.
   - Sie bringt die Gegenformen zum Bergbach (Furt-Kolk, Mäander, Kiesbank) und den ersten See-Anschluss.
   - Danach Sumpf (66 % der Seefläche), dann Elfenwald (erster Wasserfall).
5. **B5 Efeu – beantwortet.**
   - Viel im Elfenwald, mäßig in Aue (Hartholzaue) und Dschungel, wenig im Bergwald und an der Nordküste (Schattenseiten), kaum in
     der Heide.
   - **Nie** in Tundra, Gletscher, Frost, Lava, Wüste, Canyon und Ödland.
   - Ruinen und Mauern samt den 11 Demo-Bauteilen setzen wir **nicht**: Es gilt „nur Landschaft, keine menschlichen Spuren“.
6. **B6 Sitzregel Efeu – beantwortet.**
   - Anliegen: 5 × 5 Strahlen, mindestens 85 % ≤ 3 cm, kein Strahl > 8 cm.
   - Immer mit Bodenanschluss; nicht auf Schnee bzw. auf Schnee-Oberseiten.
   - Nie spiegeln (23.11).
7. **C7 Gras unter Fels – beantwortet mit Testauftrag.**
   - Landschafts-Gras wird je Landschafts-Vertex abgetastet (8 Bit, bilinear) [Quelle 5.3.2]. Dichte-Sperren und RVT im Grass Output
     kommen deshalb grundsätzlich nicht unter etwa 1 m. Das erklärt eure 75 %/91 %.
   - Feiner geht es mit **`ALandscapeProxy::AddExclusionBox`**: Ausschluss je Gras-Instanz, achsparallele Boxen, Neuaufbau automatisch.
   - Nachteile: nur C++, keine Speicherung, die Boxen müssen je Sitzung gemeldet werden.
   - Rückfall: PCG-Gras mit `Difference` gegen die Fels-Kollision.
8. **D8 Kragarm-Regel – bestätigt, mit Präzisierung.**
   - Die Grenzen stehen schon in `steine_sitz_regeln.json` (Klasse `fels`: bergseits 0,05 m, talseits min(0,15 h; 0,30 m)). Nur der
     Referenzcode prüfte sie nicht.
   - Neu und richtig sind die senkrechte Messung und die 10-%-Flächengrenze. Beides wird Regel 23.12 und gilt weltweit für v4,
     Abgrenzung in §6.
9. **D9 Kante – korrigiert: Das reicht nicht.**
   - 23.11 verlangt für den Landschritt *sichtbar* ≥ 0,75. Real erreicht ist 0,556.
   - Meine Aussage in 23i („0,42/0,77 → erfüllt“) beruhte auf dem nie eingebauten Lagen-Plan und ist **falsch**.
   - Der Lagen-Plan wird nachgezogen: Er ändert keine Höhe und braucht keinen Bake.
10. **D10 T11 – bestätigt: Entfernen ist geländeneutral.**
    - Zwei Dinge sind vor dem Löschen zu beachten:
      - **p2s Senke lesen.** Ist der alte Fluss die Senke von p2, verliert p2 beim Löschen seine Senke. Zuerst die neue Fortsetzung
        als Senke setzen.
      - **Keinen WaterBrushManager anlegen**, solange Körper mit `affects_landscape = True` existieren.
    - Naht an s 788 mit 5–10 m Überlappung (§7).

---

## 1. Bäche und Flüsse je Biom (Frage 1)

### 1.1 Was für alle Biome gilt

**Bettform nach Gefälle** [Fach, Montgomery & Buffington 1997; Chin 1989; Abrahams et al. 1995; Leopold & Wolman 1957]:

| Form | Gefälle | Kennwerte |
|---|---|---|
| Kaskade | 8–30 % | Blöcke ≥ 0,5 B übereinander, Becken < 1 B |
| Stufe-Becken | 3–8 % | Stufenabstand 1–4 B; Stufenhöhe/Abstand = 1–2 × Gefälle |
| Flachbett | 1–3 % | gleichmäßige Sohle, kaum Becken |
| Furt-Kolk | 0,1–2 % | Kolkabstand 5–7 B, Kiesbank am Gleithang |
| Mäander | < 1 % | Wellenlänge 10–14 B, Krümmungsradius 2–3 B; nur auf Talboden < 2° und breiter als 6 B |
| über 30 % | – | kein SWR-Bett mehr, sondern Wasserfall-Regeln (§3) |

**Breite aus dem Einzugsgebiet** (Richtwert für neue Läufe und zur Prüfung bestehender Betten):
- B = 1,5 × 2,5 × A^0,45 und D = 0,25 × A^0,30, mit A in km².
- Die Exponenten sind die Größenordnung regionaler Kurven [Fach]. Der Spielfaktor 1,5 ist Gestaltung: Die Inseln sind klein (17).
- Biomfaktor auf B: Wüste 1,6, Gletscher 1,8, Sumpf 1,3, Dschungel 1,4, Canyon 1,3.

**SWR** (unabhängig vom Biom, Bezug p2):
- Nachfüllen 0,3, `smoothing_width` 1.
- Zelle = clamp(B/12; 0,15; 0,40) m. Heute liegt der Median bei 0,244 m.
- Auflösung bis 2048; längere Läufe werden mit einer Naht im Becken geteilt.
- BAKED_SIM nur dort, wo WCBS sichtbar versagt und die gemessene Summe im Wasserbudget von 1,5 ms bleibt (6i §1.2).
- Wasserzone nach Regel 6t §4.

**Zonen und Deckung:**
- Zonen wie 23.4: Bett, Kante 0–1 m, Ufer 1–3 m, Hang 3–10 m, Saum 10–30 m.
- Die Talkaskaden-Ziele (Kante Netz 0,50 / sichtbar 0,85, Ufer 0,40 / 0,75, Hang Netz 0,25) sind der Faktor 1,0.
- Jedes Biom nennt einen Faktor dazu. „Sichtbar“ zählt je Biom eigene Belag-Lagen (`kantenbelag`), im Sumpf etwa Schlamm, Moos und
  Algen statt Geröll.

### 1.2 Wassermaterial je Biom

- Jede Farbe ist eine Kind-Instanz von `MI_EL_SWR_Bergbach`; geändert werden nur Absorption und Streuung.
- Absorption ist die Sichtweite je Farbe in cm [Ferat]. Herleitung:
  - reines Wasser nach Pope & Fry: Rot 0,34, Grün 0,057, Blau 0,009 je m;
  - Huminstoffe nach a(λ) = a440·exp(−S(λ−440)), S ≈ 0,016;
  - „sichtbar gefärbt“ ab a440 > 3/m [Fach].
- Y ist die Helligkeit des Grundes bei 0,3 bzw. 1,0 m Tiefe, mit Lichtweg 2 × Tiefe (Rechenweg 16h-6f) [Ableitung].

| Biom | MI (neu anzulegen) | Absorption cm R/G/B | Streuung × E16 | Y 0,3 m | Y 1,0 m | Bild |
|---|---|---|---|---|---|---|
| Nordic, Bergwald | `MI_EL_SWR_Bergbach` (vorhanden) | 160/650/850 | 1 | 0,87 | 0,64 | klar, grünblauer Kolk |
| Aue | `MI_EL_SWR_Aue` | 260/400/100 | 3, grünlich | 0,82 | 0,54 | grünlich trüb |
| Elfenwald | `MI_EL_SWR_Elfenklar` | 220/1100/900 | 0,7, türkis | 0,91 | 0,74 | sehr klar, türkis |
| Heide | `MI_EL_SWR_Moorbach` | 210/160/35 | 1, bernstein | 0,67 | 0,29 | bernstein, Sand golden |
| Tundra | `MI_EL_SWR_Tundra` | 190/500/300 | 1 | 0,85 | 0,59 | klar, leicht braun |
| Gletscher | `MI_EL_SWR_Gletscher` | 300/1000/900 | **8**, weiß-cyan | 0,92 | 0,75 | milchig türkis |
| Frost | `MI_EL_SWR_Frost` | 300/1000/900 | 6 | 0,92 | 0,75 | wie Gletscher, klarer |
| Lava | `MI_EL_SWR_Lavaklar` | 260/1500/1800 | 0,5 | 0,93 | 0,79 | kristallklar |
| Nordküste | `MI_EL_SWR_Fjordbach` | 200/800/500 | 1 | 0,89 | 0,68 | klar, leicht braun |
| Sumpf | `MI_EL_SWR_Moor` | 130/50/10 | 1,5, braun | 0,35 | 0,06 | Tee, Grund ab ≈ 0,2 m weg |
| Wüste | `MI_EL_SWR_Wuestenklar` | 250/1400/1600 | 0,5 | 0,92 | 0,78 | sehr klar |
| Dschungel | `MI_EL_SWR_Dschungel` | 200/280/50 | 3, grün | 0,76 | 0,43 | grünlich trüb |

- **Gletscher:** Die Milchigkeit kommt aus der Streuung, nicht aus der Absorption. Gletschermehl verursacht etwa zwei Drittel der
  Lichtschwächung (Rose et al. 2014). Y zeigt deshalb nur die Absorption, und der Wert 8 ist ein Startwert [Gestaltung].
- **Streuung:** Wie das Material RGB × A verrechnet, ist weiter offen (16h B.1). Deshalb steht die Streuung als Faktor zu E16 da,
  nicht als absolute Zahl.
- **Absorption und Tiefe:** Bei flachen Bächen färbt die Absorption kaum (16h, 6h). Sichtbar wird sie in Becken ab etwa 0,8 m sowie in
  Sumpf und Heide.

### 1.3 Kurzfassung je Biom

| Biom (intern) | Bettform | Bett / Kante (Hauptlagen) | Deckung Kante·Ufer·Hang | Ufer und Vegetation |
|---|---|---|---|---|
| **Nordic-Mischwald** (tundra/bergwald, p2) | Stufe-Becken, Kaskade | Geröll, Kies, Fels / Geröll, Moos, Kies | 1,0 · 1,0 · 1,0 | wie p2; Erle, Weide, Birke; keine Bäume < 1 m an der Kante |
| **Bergwald** | Stufe-Becken, Kaskade | Geröll, Kies, Fels / Moos, Geröll | 1,0 · 0,9 · 0,8 | Farn, Hochstauden × 1,4; Erle, Esche; Moos auf Blöcken in der Spritzzone |
| **Aue** | Furt-Kolk, Mäander | Kies, Sand, Schlamm / Kies, Schlamm, Sand | 0,5 · 0,4 · 0,2 | Erdanriss am Prallhang, breite Kiesbank; Röhricht am Gleithang; Weichholz 0–15 m, Hartholz dahinter |
| **Elfenwald** | Stufe-Becken, Furt-Kolk | Kies, Geröll, Algen / Moos 50 | 0,9 · 0,8 · 0,6 | Wurzelvorhänge, Farn × 1,6, Pilze; Moos auf jedem Block in 0–3 m |
| **Heide** | Furt-Kolk, Mäander | Sand, Kies, Schlamm / Erde, Moos, Sand | 0,4 · 0,3 · 0,3 | Torfkante 0,3–0,8 m mit Grasnarben-Überhang; Binsen; einzelne Birken |
| **Tundra** | Flachbett, Stufe-Becken | Geröll, Kies / Moos, Geröll | 0,8 · 0,7 · 0,6 | Moospolster bis an die Kante, Zwergweiden; keine Erdanrisse |
| **Gletscher** | Kaskade, Flachbett; Sander verzweigt (2–4 Arme) | Geröll, Kies, Schlamm | 1,0 · 1,0 · 0,8 | kein Bewuchs, Moränenböschungen 30–35° |
| **Frost** | Kaskade, Flachbett | Geröll, Kies / Eis, Geröll, Schnee | 0,8 · 0,6 · 0,5 | Randeis 0,3–1,5 m in ruhigen Abschnitten; kein Bewuchs |
| **Lava** | Kaskade, Stufe-Becken | Lavafels, Lavasand | 0,8 · 0,7 · 0,6 | Läufe nur auf altem Gestein bzw. aus Quellen am Lavarand (17); Moospolster × 1,5 |
| **Nordküste** (fjord, kueste) | Kaskade, Stufe-Becken | Geröll, Fels, Kies | 1,0 · 0,9 · 0,8 | Mündung als Geröllfächer über den Strand, Treibholz nur dort; Meer nach KONVENTIONEN §1b |
| **Sumpf** | Mäander, Furt-Kolk | Schlamm 60 / Schlamm, Moos, Algen | 0,15 · 0,1 · 0,1 | keine Böschung; Deckung aus Wurzeln, Totholz und Bulten, Steine ≤ 1 je 20 m; Röhricht × 2; Bäume bis 0,3 m Wassertiefe |
| **Wüste** (wueste, canyon, oedland) | Flachbett, Furt-Kolk | Sand 55 / Sand, Lehm | 0,5 · 0,4 · 0,4 | breite Sandsohle, Wasser nur in 30–60 % davon; Felsbecken unter Canyon-Stufen; grüne Galerie × 2 als einziger Bewuchs |
| **Dschungel** | Furt-Kolk, Mäander | Schlamm, Lehm / Lehm, Schlamm, Laub | 0,3 · 0,3 · 0,3 | Lehmufer 45–80° mit Wurzeln, Brettwurzeln; Kronen und Lianen hängen 1–3 m über das Wasser |

- Die Klassen `roehricht`, `moospolster` und `liane` sind Sonderformen der Biom-Planer (KONVENTIONEN §4).
- Die übrigen Klassen kommen aus `mittelschicht`. Die Faktoren gelten auf deren Biomdichte.
- Paletten nennt die JSON bewusst nicht; Asset-Namen bleiben bei den Planern.

---

## 2. Seen (Frage 2)

### 2.1 Bau

- **Ein Wasserkörper je Becken:**
  - Im Umriss plus 20 m zuerst alle Houdini-Netze und Houdini-Spiegel entfernen, dann den Epic-See bauen.
  - Die Bestandsaufnahme der Houdini-Reste (euer Nachtrag) sollte je See beide Zahlen nennen: Epic-Körper und Houdini-Netze.
- **`affects_landscape = False`**, weil die Landschaft bleibt.
  - Alle Splinepunkte liegen auf einer Höhe [Doku].
  - Der Spline liegt 0,5–2 m außerhalb der Wasserlinie, sodass der Rand im Gelände endet (6t).
- **Spiegel:** Überlauf (tiefster Punkt der Umrandung) − 3 cm, wie die Teich-Regel in `teiche.json`.
- **Gefrorene Seen** (`eis: true`, Frost): kein Wasserkörper, sondern eine Eisfläche.

### 2.2 Ufer und Flachwasser

| Uferform | Hang | Lagen 0–1 m | Röhricht |
|---|---|---|---|
| Flachufer | 0–8° | Schlamm 35, Sand 30, Kies 20, Gras 15 | ja |
| Kiesufer | 8–20° | Kies 50, Geröll 25, Sand 25 | nur in Buchten |
| Steilufer | 20–35° | Geröll 40, Erde 30, Moos 30 | nein |
| Felsufer | > 35° | Fels 60, Geröll 25, Moos 15 | nein |

**Verlandungsreihe:**
- Seggen und Binsen −0,3 bis +0,1 m.
- Schilf 0–1,0 m Wassertiefe, als Gürtel 3–15 m breit, mit Lücken alle 20–60 m.
- Rohrkolben 0,2–1,3 m. Rohrkolben steht tiefer als Schilf (Photosynthetica 2021) [Fach]; die Meterwerte sind Gestaltung.
- Schwimmblatt 0,5–2,5 m, nur in windstillen Buchten von Seen < 5 ha.
- Kein Bewuchs an wellenoffenen Ufern (Fetch > 300 m) und an Felsufern.

Die Faktoren je Biom stehen in der JSON (`seen.biom`), etwa Sumpf Röhricht 1,5, Gletscher 0.

### 2.3 Bach an den See anschließen

- **Zulauf (SWR):**
  - Der letzte Splinepunkt liegt 5–10 m im See, und der See ist Senke.
  - Ohne gültige Senke meldet 5.8.3 „no valid sinks“, und die Fläche verschwindet in Live Sim [Forum].
  - Ein See als Senke ist „möglich, aber intern nicht voll unterstützt“, mit Bake-Abstürzen in 5.7 [Forum].
  - **Zu prüfen beim ersten See-Pilot:**
    - Typ der Liste `sink_river_water_bodies` lesen (Name deutet auf Flüsse) und einen See zuweisen.
    - Gelingt der Bake nicht, wird der Fluss Senke, und der See liegt darüber.
  - Sedimentfächer aus Kies und Sand, 1–3 B breit, als Lage in den See; Röhricht seitlich, nicht im Fächerkern.
- **Zulauf (Epic-Fluss):**
  - Der Spline endet im See-Polygon; Übergang über `lake_transition_material` [Doku].
  - Die Farbe des Übergangsmaterials muss von Hand an den See angeglichen werden [Doku].
- **Abfluss:**
  - Die Schwelle aus Geröll und Fels, 2–5 m lang, liegt am tiefsten Randpunkt.
  - SWR-Quelle 3–5 m im See mit Startwasserhöhe = Seespiegel; die ersten 1–2 B als Riffel.

---

## 3. Wasserfälle ohne Houdini (Frage 3)

**Werkzeug:**
- Der Vorhang ist ein Netz, das in Unreal entsteht: ein Spline-Band oder Geometry Script bzw. Modeling-Werkzeuge.
- Es trägt das vorhandene `MI_EL_Wasserfall` mit denselben Vertexfarben (R Tempo, G Fallanteil, B Randfaktor, A Dicke;
  `wasserfaelle.json`). Diese werden jetzt in Unreal aus der Bogenlänge gerechnet.
- Die alten Houdini-Netze `SM_WF_*` kommen weg; das Material bleibt.
- Darauf kommt Nature Water FX (`NS_Waterfall_*`, `NS_Impact_*`, `NS_Stream_*`), Akteur-Konvention wie `wasser_fx/plan.json`.
- Zulauf und Becken sind SWR.
- Epic selbst liefert kein Wasserfall-Werkzeug [Forum]. Dieser Aufbau entspricht dem Stand der Spielgrafik: Netz für den Körper,
  Partikel an Lippe und Fuß [Forum/Blogs, Quellen].

| Typ | Fallhöhe | Neigung | Umsetzung |
|---|---|---|---|
| SWR-Stufe | < 0,8 m | – | nur Gelände im Bett, Schaum aus fluss_sim |
| Kaskade | 0,8–30 m | 45–75° | Band liegt am Fels an (≤ 5 cm), `NS_Stream_*`/`NS_Impact_Small` an Stufen |
| Vorhang | 1,8–60 m | 75–90° | freier Vorhang, `NS_Waterfall_Small/Medium/Large` nach Breite, `NS_Impact_*` am Fuß |
| Schleier | wenig Abfluss oder H > Zerfallslänge | – | dünnes Band, das in Partikel übergeht |

**Mindestregeln:**
- **Herkunft** nach 17 §5 (Pflicht).
- **Abwurf:** x = v₀·√(2H/g). Der Vorhang steht um x vom Fels ab und schneidet unten nie in den Fels.
- **Strahlzerfall:** Lb ≈ 6·q^0,32 m (Horeni; Labor, q < 0,25 m²/s). Unterhalb Lb wird der Vorhang weiß und zerrissen.
- **Becken:** Durchmesser max(2 B; 2,4·√H), Tiefe ≥ max(1 m; 0,6·√H). Gegenprobe WF_K1 (55 m, 15 m breit):
  Durchmesser ≥ max(30; 17,8) = 30 m, Tiefe ≥ 4,4 m. Der Bestand hat Radius 16 m (Durchmesser 32 m) und Tiefe 5 m, die Regel passt
  also [Ableitung].
- **Breite zu Höhe** 0,1–1,0; breiter als H nur bei Flüssen.
- **Lippe** aus festem Fels; Nass- und Moosstreifen 1–3 m neben dem Vorhang (17 §2).
- **Biom:**
  - Gletscher milchig, Eis an der Lippe; Frost teilweise gefroren.
  - Wüste nur Schleier mit Felsbecken; Sumpf ohne Fälle.
  - Dschungel mit doppeltem Bewuchs im Nebelradius.

---

## 4. Rollout-Reihenfolge (Frage 4)

**Gewässer nach dominantem Feldbiom** [Ableitung aus `wasser_welt.json`, `baeche_alle.json`, `teiche.json`]:
- Grundlage ist das dominante Biom je Feld, weil `eigner.r8` in der Cloud fehlt. Die Zahlen sind deshalb nur eine Näherung.
- Die Summe von 44,6 km passt zu den 45,4 km aus fluss_sim.

| Feldbiom | Fluss m | Bach m | Seen | Seefläche ha |
|---|---:|---:|---:|---:|
| Aue | 4 567 | 10 124 | 13 | 5,1 |
| Elfenwald | 2 008 | 7 237 | 3 | 8,0 |
| Heide | 474 | 6 312 | 5 | 1,2 |
| Dschungel | 2 774 | 2 557 | 10 | 1,2 |
| Bergwald | 151 | 2 697 | 8 | 1,7 |
| Gletscher | 450 | 1 804 | 2 | 0,1 |
| Tundra | 649 | 876 | 7 | 0,8 |
| Sumpf | 151 | 128 | 28 | **34,9** |
| Wüste, Ödland, Canyon | 282 | 1 349 | 1 | 0,1 |

**Reihenfolge:**

1. **Pilot 1 Nordic:** p2 fertig, dazu der alte C3/D3-Fluss als SWR-Fortsetzung (§7).
2. **Pilot 2 Aue** unterhalb der p2-Mündung im Feld C3, mit einem der Seen `S_K10_TUNDRA_02–04` (C3) als erstem See-Anschluss.
   - Am schnellsten belastbar, weil die Aue ein Drittel aller Laufmeter hat.
   - Sie prüft die Gegenformen zum Bergbach (Furt-Kolk, Kiesbank, Erdanriss, trübes Wasser).
   - Zulauf, Mündung und See liegen in einem zusammenhängenden Abschnitt.
3. **Sumpf:** Teichverbund H5/I5 mit 66 % der Seefläche; Seeregeln und Moorwasser.
4. **Elfenwald:** Elfenfluss mit dem ersten Fall ohne Houdini.
5. Danach Heide, Dschungel, Bergwald, Hochgebirge, Tundra, Wüste, Lava, Nordküste.

---

## 5. Efeu (Fragen 5 und 6)

**Fachgrundlage:**
- Efeu ist schattentolerant und klettert an Bäumen, Mauern und Felsen hoch. Begrenzt wird er durch Bodenfeuchte, Licht und längere
  Fröste (Metcalfe 2005, nach Zitat) [Fach].
- Ein eigenes Zitat für eine Januar-Isotherme habe ich nicht gefunden. Deshalb gilt keine absolute Höhengrenze, sondern die
  Biomliste. Im Bergwald liegt die Grenze ≥ 80 m unter der lokalen Baumgrenze.

| Biom | Anteil Felswände ≥ 2 m mit Efeu | Fläche je Wand | Anteil Stämme | Exposition |
|---|---|---|---|---|
| Elfenwald | 50 % | 15–45 % | 50 % | alle |
| Aue | 20 % | 10–30 % | 35 % (Hartholzaue ab 15 m; Weichholz 0–15 m nur 10 %) | alle |
| Dschungel | 30 % | 10–40 % | 25 % (nur ergänzend zu Lianen) | alle |
| Bergwald | 15 % | 5–25 % | 10 % | N, NO, O, NW |
| Sumpf | – | – | 15 % (nur auf Bulten, ≥ 0,5 m über dem Spiegel) | – |
| Nordic-Mischwald | 8 % | 5–15 % | 5 % (nur unter Laubkronen) | N, NO, O |
| Nordküste | 5 % (Wände ≥ 30 m vom Meer) | 5–15 % | 5 % | Schatten, Lee |
| Heide | 3 % (geschützte Nischen) | 5–10 % | – | – |
| **nie** | Tundra, Gletscher, Frost, Lava, Wüste, Canyon, Ödland | | | |

**Bäume:**
- Raue Rinde bevorzugt: Eiche, Esche, Ulme, Ahorn, Pappel, Weide, alte Kiefern.
- Buche nur mit Faktor 0,3, Fichte im dichten Bestand 0,2.
- Nie an Stämmen unter 20 cm.
- Höhe bis 0,3–0,7 × Baumhöhe, nicht in die Krone.

**Wasser:** mindestens 0,5 m über dem Spiegel; Dichte 0–10 m vom Wasser × 1,5, über 50 m × 0,6.

**Sitzregel (Frage 6):**
- **Anliegen:**
  - 5 × 5 Strahlen von der Rückseite entlang der Normale.
  - Mindestens 85 % treffen mit ≤ 3 cm Abstand; kein Strahl hat > 8 cm Luft; Eindringen ≤ 4 cm.
- **Verbunden:**
  - Der untere Rand liegt ≤ 0,3 m über dem Gelände, oder das Netz schließt an ein anderes Efeu-Netz an (≤ 0,2 m).
  - Von oben hängend nur mit Anschluss an Boden bzw. Moos der Felsoberseite. Ein Efeu-Fleck mitten in der Wand liest als
    aufgeklebt.
- **Kein Schnee:** nicht auf Lage Schnee/Eis ≥ 60. Auf Felsmaterial mit Schnee-Oberseite nur Flächen mit Normale z < 0,3.
- **Nicht:** frei in der Luft, über Kanten in den Himmel, im Wasserfall-Vorhang, auf Steinen < 1 m.
- **Setzen:**
  - Als Akteur bzw. ISM mit Snap an die Oberfläche.
  - Foliage-Pinsel nur mit Ausrichtung an der Normale und anschließender Sitzprüfung.
  - Nie spiegeln (23.11).
- **Kosten:** Masked-Karten erzeugen Overdraw bei großen Netzen nahe der Kamera. Sichtweite 60–120 m ist ein Startwert, am ersten
  Pilot messen.

---

## 6. Landschafts-Gras sticht durch Felsen (Frage 7)

**Warum die Dichte-Sperre nicht reicht** [Quelle UE 5.3.2, Spiegel `chenyong2github/UnrealEngine` @ c865e168]:
- Die Grass-Map hat je Komponente `ComponentSizeVerts` Pixel im Format `PF_B8G8R8A8`, also **einen 8-Bit-Wert je Landschafts-Vertex**
  (`LandscapeGrass.cpp` L1271, L1315).
- Jede Instanz liest den Wert bilinear aus den vier Nachbar-Vertices (L2884–2914) und bleibt, wenn Gewicht ≥ Zufall (L2715).
- Bei 1-m-Quads verläuft ein Loch daher linear über etwa 1 m. Ganz weg ist Gras nur dort, wo alle vier Ecken 0 sind.
- Das ist euer Befund: 75 %/91 % Rest, und mit Rand 0 bleiben 52 % plus ein kahler Hof.
- Auch eine RVT im Grass Output schreibt in dieselbe Vertex-Auflösung. Dazu wartet der Pass nicht auf RVT-Seiten (L1628ff).
- Eine CVar für feinere Abtastung gibt es in 5.3.2 nicht (alle `grass.*` geprüft). Für 5.8 ist das **zu prüfen**.

| Weg | feiner als 1 m | Neuaufbau | bleibt gespeichert | Urteil |
|---|---|---|---|---|
| **`ALandscapeProxy::AddExclusionBox(Owner, FBox)`** [Quelle `LandscapeProxy.h` L998–1013; [API](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Landscape/ALandscapeProxy/AddExclusionBox)] | **ja**, Test je Instanz (`IsExcluded`, L2672–2681) | automatisch: betroffene Gras-Komponenten bauen asynchron neu | **nein**; die Boxen liegen in einer statischen Tabelle und müssen je Sitzung neu gemeldet werden | **Empfehlung** |
| Dichte-/Masken-Lage, RVT im Grass Output | nein (Vertex) | Build Grass Maps | ja | verworfen für < 1 m |
| PCG-Gras (`Generate Grass Maps` + `Difference` gegen Fels bzw. `World Ray Hit Query`) | ja (Kollisionsform) | PCG neu erzeugen | Editor-Erzeugung ja | Rückfall: teuer bei dichtem Gras; 5.6-Fehler bei `Difference` mit Get Actor Data [Forum] |
| Gras an Felsen durch Foliage ersetzen | ja | – | ja | nur punktuell; Budget 60 000 je Feld |

**Einschränkungen der Boxen:**
- Nur C++, kein Blueprint-Knoten.
- Nur achsparallel: Ein gedrehter Fels braucht deshalb bis zu 4 Teilboxen (0,5-m-Streifen entlang der langen Achse).
- Die Box muss die Geländehöhe enthalten (z = Gelände −0,2 bis Unterkante Fels +0,3).
- Debug: `grass.DumpExclusionBoxes`, `grass.IgnoreExcludeBoxes`.

**Testablauf T24-G** (Pilot an 20 Felsen der Talkaskade, im Speicher):
1. In 5.8.3 `LandscapeProxy.h` öffnen: Gibt es `AddExclusionBox` noch mit derselben Signatur (1 min)?
2. Eine kleine Editor- bzw. Laufzeitkomponente (C++) meldet für 20 Fels-Instanzen mit Fuß im Gras je 1–4 Boxen mit 5 cm Einzug.
3. Messen:
   - Gras-Rest im Grundriss und in der Durchstich-Zone, wie euer Verfahren mit 75 %/91 %.
   - Breite des kahlen Hofs außen.
   - `stat Foliage` bzw. Gras-Aufbauzeit vorher und nachher.
4. Bildpaar von schräg oben, gleiche Sonne.

**Erfolg:**
- Rest im Grundriss ≤ 5 % und in der Durchstich-Zone ≤ 10 %.
- Kein Hof breiter als 0,15 m.
- Kein messbarer Anstieg der Frame-Zeit.

**Abbruch:** Die Funktion fehlt in 5.8, oder die Aufbauzeit steigt über 2 ms je Komponentenwechsel. Dann der PCG-Rückfall an
denselben 20 Felsen.

**Bei Erfolg:**
- Die Dichte-0-Sperre bleibt nur unter Felsen ≥ 3 m Grundriss; sonst wieder Biomdichte, damit der kahle Hof verschwindet.
- Die Boxen meldet ein Subsystem beim Laden aus dem Fels-Zensus.

---

## 7. Talkaskade C2 und Mündung (Fragen 8–10)

### 7.1 Kragarm-Regel (Frage 8) – bestätigt, wird 23.12

**Die Werte selbst sind nicht neu.** In `steine_sitz_regeln.json` stehen sie schon unter `klassen.fels.luecke_max_m`:
`punktwolke_bergseite` 0,05, `punktwolke_talseite_anteil_h` 0,15 und `punktwolke_talseite_max` 0,30. Die `_doku` vermerkt dazu:
„Talseitige Grenzen … noch nicht im Referenzcode“ [Projekt].

**Richtig und neu sind zwei Punkte:**
1. **Senkrecht von oben messen:** Ein hangparallel liegender Block (21,5°) zeigt im lokalen Grundriss zu wenig Luft auf der Talseite.
   Gesehen wird aber das Licht, das senkrecht unter dem Block durchgeht.
2. **10-%-Grenze:** Höchstens 10 % des senkrechten Grundrisses dürfen > 30 cm Luft haben. Das fängt lange, dünne Kragarme, die am Rand
   die 30 cm einhalten, aber breit hohl liegen.

**Präzisierung für v4 weltweit:**
- **h** = senkrechte Ausdehnung der Instanz in Weltkoordinaten (z_max − z_min der Punktwolke), nicht die Netzhöhe lokal.
- **Talseite:** Grundrisshälfte mit Gelände unter dem Mittelwert in Falllinienrichtung. Diese Unterscheidung gilt nur ab 10° Hang.
  Darunter gilt rundum die Bergseiten-Grenze 0,05 m im Kern.
- **Gilt für** Klasse `fels` (≥ 1,0 m) und für `stein` ab 0,5 m mit Hang ≥ 10°.
- **Ausnahmen:**
  - Wandfelsen mit Überhang-Warnung (23.7) bleiben WARNUNG.
  - Hängende Stücke (`haengend`) sind ausgenommen.
- **Bestand:** Bestehende Stücke mit neuem FEHLER werden nicht automatisch entfernt. Zuerst mit 23.11 `hang_platz` tiefer setzen
  oder drehen (Yaw), dann neu prüfen.

### 7.2 Kante 0,556/0,555 (Frage 9) – Korrektur

- **23i war falsch.**
  - Ich habe „Landschritt 0,42/0,77 → erfüllt“ geschrieben.
  - Die 0,77 enthielten den nie eingebauten Lagen-Plan aus 23f. Real sind es 0,556/0,555.
  - Das Zwischenziel aus 23.11 (`kante_zweistufig.landschritt`: Netz ≥ 0,40 **und** sichtbar ≥ 0,75) ist also **nicht** erreicht.
- **Netz ≥ 0,40 allein reicht nicht.**
  - „Sichtbar“ ist die Vereinigung aus Netz-Grundrissen und Zellen mit Lage Geröll/Fels/Felsplatte/Kies ≥ 0,5
    (`nachtrag_23_4.deckung.sichtbar`).
  - Der Fehlbetrag (≈ 0,19 je Seite) ist genau der Lagen-Anteil, der nie gemalt wurde.
- **Entscheidung:** Den Lagen-Plan aus 23f jetzt nachziehen, vor dem 16h-Bettschritt.
  - Eine Lage ändert keine Höhe; die SWR sieht sie nicht, solange keine Rauheitskarte aus Lagen eingerichtet ist (23f §1.1,
    **lokal bestätigen**).
  - Kein Bake nötig, reversibel, keine neuen Instanzen.
  - Erde ≤ 0,05 in der Kante beachten.
- **Erfolg:** sichtbar ≥ 0,75 je Seite, Netz bleibt ≥ 0,40, Bildpaar an den zwei festen Kameras.

### 7.3 T11 (Frage 10) – Folge bestätigt, was beim Ersetzen zu beachten ist

**Euer Befund:** `affects_landscape = True`, kein `WaterBrushManager`, 30 Höhen 0,00 cm, PIE weiter mit Platte. Das ist die dritte Zeile
der 6t-Tabelle: **Geometrie**, Entfernen ist geländeneutral [Ferat].
- Ohne Brush-Manager schneidet kein Wasserkörper ins Gelände, auch wenn `affects_landscape` True ist [Ableitung]. Das erklärt
  die 0,00 cm.

**Zu beachten beim Ersetzen:**

1. **Senke von p2 lesen, bevor der alte Fluss weg ist.** `sink_river_water_bodies` an p2 lesen.
   - **Steht dort der alte C3-Fluss, wird die Liste beim Löschen leer.** Dann meldet 5.8.3 „no valid sinks“, und in Live Sim
     verschwindet die Fläche [Forum].
   - Ob BAKED_SIM davon betroffen ist, ist **zu prüfen**: ein Bildpaar und der Rauschband-Vergleich (6r) nach dem Entfernen,
     noch ohne Speichern.
   - Reihenfolge:
     1. Neue Fortsetzung bauen.
     2. Sie als Senke von p2 eintragen.
     3. Alten Fluss entfernen.
     4. p2-Bild prüfen.
   - Ändert sich p2, wird der p2-Bake Teil von Pilot 1 (nicht vorher speichern).
2. **Kein WaterBrushManager**, solange irgendwo Körper mit `affects_landscape = True` stehen. Ein später angelegter Manager würde sie
   alle ins Gelände schneiden.
   - Vorher an allen verbleibenden Epic-Körpern `affects_landscape` auf False setzen. Das ist eine reine Eigenschaft; Höhenprobe
     wie T11.
3. **Naht an s 788:**
   - Die Fortsetzung beginnt 5–10 m stromauf von s 788, also überlappend. Ihre Startwasserhöhe ist die gebackene p2-Höhe an dieser
     Stelle.
   - Beide Bereiche müssen sich in der Überlappung decken: Höhenunterschied ≤ 2 cm (Rauschband-Grenze 6r).
   - Der Naht-Ort ist ein ruhiger Abschnitt bzw. Becken, nie eine Stufe (fluss_sim: 11 Becken-Nähte).
4. **Mündung ins Hauptgewässer:**
   - Der letzte Splinepunkt liegt im Hauptgewässer, und das Hauptgewässer ist Senke.
   - Ist das Hauptgewässer noch ein Epic-Fluss, kommt ein `lake`/`river`-Übergang ohne Wand dazu.
   - Mündung als Sedimentfächer (Kies, Sand), nicht als Kanal.
5. **Zonen:** Nach dem Entfernen Z1 aus 6t §4: C3/D3 im Speicher auf 1024 stellen und das Bildpaar an der Mündung vergleichen.
   Bei gleichem Bild bleiben C3/D3 auf 1024 (spart etwa 2 × 120 MiB bei Half-Float).
6. **Fernfläche** bleibt aus (euer Befund, Grenzen 0,6 km): erledigt.

---

## 8. Nächste Handlung

**Eine Handlung:** Pilot 1 abschließen, Schritte 1–4 aus §7.3, im Speicher:
1. Senke von p2 lesen.
2. Neue C3/D3-Fortsetzung als SWR mit `MI_EL_SWR_Bergbach` bauen und als Senke eintragen.
3. Alten Fluss entfernen.
4. Bildpaar p2 und Mündung; Rauschband-Vergleich an p2; dann Z1.

**Erfolg:**
- p2 unverändert (Rauschband).
- Keine Wasserplatte an der Mündung.
- Naht ≤ 2 cm.
- Ein Zonenwert für C3/D3.

**Abbruch:** p2 verliert die Fläche oder ändert sich über das Rauschband hinaus. Dann nicht speichern, den alten Fluss wieder als Senke,
und der p2-Bake kommt in den Pilot.

**Unabhängig und parallel möglich:**
- Lagen-Plan der Kante (§7.2).
- T24-G Gras (§6).
- Auf Grundlage dieser Regeln: Planung des Aue-Piloten und der Fälle 175–184.

---

## 9. Nachtrag 25.10. 20:10 – Nature Water FX fest eingeplant, keine Käufe

Gelesen: recherche/auftraege/24-gewaesser-biome-houdini-ausstieg-efeu-gras.md @ fe98744692a6c10d7ab13ba055d8480401bf5f43 (Commit 72d9f1b)

**Kurzfazit Nachtrag:**
- Nature Water FX ist jetzt in der Regeldatei (v2, Schlüssel `nature_water_fx`) das Partikel-Werkzeug für jede Rolle: Fallkörper,
  Aufprall, Beckenauslauf, Rinne bzw. Überlauf und Strömung an Steinen. Zugeordnet ist nach Größe, Biom und Budget.
- Die Seen- und Uferregeln aus §2 brauchen keine Kaufpakete. Echte Lücken gibt es nur bei Wasserpflanzen: Schwimmblatt, grünes
  Schilf als Netz, tropische Wasserpflanzen, Wasserlinsen. Dazu fehlt ein Wasserfall-Klang.
- Status: beantwortet. Die Lücken warten auf zwei Formprüfungen bzw. eine Gratis-Suche.

### 9.1 Nature Water FX je Rolle

- Die Systeme liegen laut `inventar_extra.json` unter `/Game/NatureWaterFX/FX/`: `NS_Waterfall_`, `NS_Impact_`, `NS_Wake_` und
  `NS_Stream_` je Small/Medium/Large, dazu `NS_Geyser_Small/Large` [Projekt].
- Akteur-Konvention, Effekttypen, Cull und Budget übernehme ich aus `wasser_fx/plan.json` (Auftrag 14):
  - GPU, keine Schatten;
  - `NET_EL_Wasser_Nah` 50 m, `NET_EL_Wasser_Held` 150 m;
  - je Ort höchstens 3 Systeme, gleichzeitig aktiv höchstens 6.

| Rolle | System | Wann | Wo |
|---|---|---|---|
| Fallkörper | `NS_Waterfall_*` | Vorhang ab 1,8 m; das Unreal-Netz bleibt Träger, NS bricht ihn auf | Lippe bis 2/3 der Fallhöhe |
| Aufprall | `NS_Impact_*` | jeder Fall und jede Stufe ab 1,0 m | am Auftreffpunkt (Abwurf x aus §3), nicht am Felsfuß |
| Beckenauslauf, Engstelle | `NS_Wake_*` | Becken unter Fällen ab 5 m, Engstellen mit Tempo > 1,5 m/s | Auslauf bzw. hinter dem Block |
| Rinne, Überlauf | `NS_Stream_*` | Kaskaden, Rinnen über Fels 0,8–1,8 m, Überlauf an Dämmen, Verklausungen und Felsbecken | entlang der Rinne, +X = Fließrichtung |
| Strömung an Steinen | `NS_Wake_Small` | nur Schaustellen: Block ≥ 0,5 B im Hauptstrom bei Tempo > 1,0 m/s, alle 30–60 m | hinter dem Block |

- **Größe:** Gewählt wird die kleinste Stufe, deren Annahme aus `plan.json` (z. B. Waterfall S 3 × 5, M 6 × 15, L 12 × 30 m)
  mindestens 0,8 × Ziel erreicht. Die Skala liegt in 0,8–1,5; darüber die nächste Stufe.
- **Skalen messen:** Die Annahmen sind weiter nicht gemessen [Projekt 14]. Der erste Fall ohne Houdini misst sie einmal.
- **Strömung an Steinen:** Ein System an jedem Stein würde Budget und Bild überladen. Den Rest tragen die Schaumstraßen der SWR
  (787 im Export) [Projekt].
- **Biome:**
  - Sumpf nur `Wake` an Verklausungen; Aue `Wake` an Treibholz, `Stream` an Dämmen.
  - Wüste nur `Stream_Small` an Felsbecken-Überläufen.
  - Frost Skala × 0,7, Gletscher × 1,2.
  - Lava optional `NS_Geyser_*` an heißen Quellen, als eigener Sehens-Ort.
- **Bestand:** Die heutigen 15 Stellen hängen zum Teil an K1/K8 (Gischt). Sie ziehen beim Houdini-Ausstieg mit an die neuen Vorhänge
  um, mit denselben Gruppen aus `plan.json` (`WF_K1`, `WF_K8`).

### 9.2 Seen und Ufer mit vorhandenen Assets

**Abgleich** [Projekt, Namenssuche in `inventar.json` + `inventar_extra.json`, 6 608 Pfade]:

| Bedarf (§2) | vorhanden | Urteil |
|---|---|---|
| Schilfgürtel | Megaplant *Dry Common Reeds* (12, trocken), `GT_Schilf` (Grass Type) | Netze nur trocken; grünes Schilf nah an der Kamera fehlt |
| Rohrkolben | Megaplant Bulrush (`MI_VEGMP_MI_Bulrush_01_Foliage`) | reicht |
| Binsen, Seggen | Megascans ToadRush | reicht für Säume |
| Schachtelhalm | Coast & Dunes `rough_horsetail` | reicht |
| Algen, Wasserlinsen | `MI_Decal_Algae` (Coast & Dunes) | als Decal auf stehendem Wasser prüfen |
| Sumpfbaum | `SM_SwampCypress_A` | reicht für Einzelbäume |
| Schwimmblatt (Seerose) | `SM_lily_01_1/2` (Forest Environment) und `SM_WaterPlant01–04` (CityPark): Form aus dem Namen nicht sicher | **zu prüfen** |
| Kies-/Fels-/Steilufer | rund 2 000 Netze, Megascans, Fab | reicht |

**Echte Lücken** (nur wenn die Formprüfung negativ ist):
1. **Schwimmblatt** für Sumpf, Aue, Elfenwald und Dschungel.
2. **Grünes Schilf als Netz** für Gürtel in Sumpf und Aue.
3. **Tropische Wasser- und Uferpflanzen** (Papyrus-, Lotus-, Wasserhyazinthen-artig) im Dschungel.
4. **Wasserfall-Tosen** als Klang: heute gibt es nur `CUE_Water_Stream_I–X` (`plan.json`, `klang.luecke`).

**Vorgehen nach der Regel „kostenlos vor Kauf“:**
1. `SM_lily_01` und `SM_WaterPlant01–04` einmal ansehen.
2. Dann in den freien Megascans-Freigaben und den Gratis-Paketen auf Fab suchen (water lily, lotus, papyrus, reed, duckweed).
3. Nur was dort fehlt, kommt als Kaufliste mit Preis zu Ferat.

Fluid Flux, River Generator und River-Lake Ecosystem braucht keine Regel aus §1–3.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Ein Wasser je Becken, kein Rand in der Luft.** Doppelte Seen und Platten sind die gröbsten Fehler im Bild; der Houdini-Ausstieg
   mit Pilot 1 behebt sie an der Wurzel.
2. **Biome lesen sich am Wasser.** Gleiche Bäche in jedem Biom wirken generisch. Moorbach-Bernstein, Gletschermilch, Aue mit Kiesbank
   und Erdanriss und die grüne Wüstengalerie geben jedem Gebiet seinen Charakter.
3. **Wasserfälle mit Herkunft und Gewicht:** Lippe aus Fels, Abwurf, zerrissener Strahl, Becken, Nebel. Ein Fall ohne Zulauf zerstört
   die Glaubwürdigkeit (17).
4. **Fels sitzt im Gras:** Ohne Grashalme durch Steine und ohne kahlen Hof (§6) liest der Boden als gewachsen.
5. **Kante voll belegt** (§7.2): Ein sichtbarer Erdstreifen an der Wasserlinie verrät die Platzierung.
6. **Efeu sparsam und verbunden:** Wenige, an Boden angeschlossene Teppiche an Schattenwänden wirken alt. Gleichmäßig gestreuter Efeu
   wirkt wie Deko.

## Quellen

- Engine-Quelltext UE 5.3.2 (öffentlicher Spiegel `chenyong2github/UnrealEngine` @ c865e168d0935b8e5f4bd865ddcc1c733c8ce7cf):
  - `Engine/Source/Runtime/Landscape/Classes/LandscapeProxy.h` L998–1013;
  - `Engine/Source/Runtime/Landscape/Private/LandscapeGrass.cpp` L1271, L1315, L1628ff, L2672–2715, L2884–2914;
  - `Plugins/Experimental/PCG/.../PCGPrimitiveData.cpp` L21–41.
  - https://github.com/chenyong2github/UnrealEngine/blob/c865e168d0935b8e5f4bd865ddcc1c733c8ce7cf/
- Epic API `AddExclusionBox`: https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Landscape/ALandscapeProxy/AddExclusionBox
  (4.26: https://docs.unrealengine.com/4.26/en-US/API/Runtime/Landscape/ALandscapeProxy/AddExclusionBox/index.html)
- PCG Generate Grass Maps (5.7): https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/PCGGenerateGrassMapsSettings?application_version=5.7 ;
  PCG GPU: https://dev.epicgames.com/documentation/unreal-engine/using-pcg-with-gpu-processing-in-unreal-engine ;
  Forum 5.6 Difference: https://forums.unrealengine.com/t/in-ue-5-6-pcg-difference-node-no-longer-removes-points-using-getactordata/2661336
- Water Body Actors (Lake, Transition Material, Blend Min): https://dev.epicgames.com/documentation/unreal-engine/water-body-actors-in-unreal-engine
- `WaterBodyRiver` Python-API (`lake_transition_material`): https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterBodyRiver?application_version=4.27
- Übergänge angleichen [Forum]: https://forums.unrealengine.com/t/water-body-transition-matching/481792
- SWR ohne Senke 5.8.3 [Forum]: https://forums.unrealengine.com/t/wateradvanced-shallowwaterrivercomponent-no-valid-sinks-warning-and-river-disappears-in-5-8-3/2840450
- SWR mit See [Forum]: https://forums.unrealengine.com/t/shallowwaterriver-lake-ocean/2838534
- Single Layer Water: https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine
- Pope & Fry 1997, Absorption reinen Wassers: https://doi.org/10.1364/AO.36.008710
- CDOM-Kurve und Bereiche: https://bg.copernicus.org/articles/14/1215/2017/bg-14-1215-2017.html ; https://www.lccmr.mn.gov/projects/2016/finals/2016_04i_PLOSIron.pdf
- Gletschermehl (Rose et al. 2014): https://researchcommons.waikato.ac.nz/entities/publication/27bfd7c2-cdca-4b1f-aa0b-6341f2128894
- Strahlzerfall (Horeni): https://www.upct.es/hidrom/publicaciones/congresos/CI13.pdf
- Wasserfall-Aufbau in Spielen: https://polycount.com/discussion/74454/waterfall-environment ; https://realtimevfx.com/t/waterfall-thread/18621 ;
  Forum „kein Wasserfall-Preset“: https://forums.unrealengine.com/t/waterfall-creation/685219
- Nature Water FX (Fab): https://fab.com/listings/c34e8871-3585-4381-b21f-1b895814472b
- Schilf/Rohrkolben-Tiefen (Photosynthetica 2021): https://ps.ueb.cas.cz/artkey/phs-202102-0002_comparison-of-water-depth-tolerance-in-two-major-wetland-macrophytes-phragmites-australis-and-typha-angustifol.php
- Efeu: https://en.wikipedia.org/wiki/Hedera_helix ; https://sppaccounts.bsbi.org/content/hedera-helix-0.html ;
  https://www.infoflora.ch/en/flora/hedera-helix.html ; Metcalfe 2005 zitiert in https://www.scielo.br/j/oh/a/pSmkCcppz9DJ3d97k7Tbs3M/?lang=en
- Bettformen: Montgomery & Buffington 1997 (GSA Bull. 109); Chin 1989; Abrahams, Li & Atkinson 1995; Leopold & Wolman 1957 (wie
  `bachbett_ufer_regeln.json`)
- Projekt: 16h, 16h-6f/6h/6i/6r/6t, 17, 18, 23f, 23i, `steine_sitz_regeln.json`, `bachbett_regeln.json`, `bachbett_ufer_regeln.json`,
  `wasser_welt.json`, `teiche.json`, `wasserfaelle.json`, `fluss_sim/zusammenfassung.json`

## Rückfragen

1. **Nordic-Mischwald:** Unser Raster kennt kein eigenes Biom dieses Namens. Ich habe es als Erlenbach-Profil (Tundra/Bergwald-Übergang,
   C2/C3/D2) geführt. Gibt es lokal eine Kennzahl in `eigner.r8`, die es abgrenzt? Ohne Antwort gilt die Regel überall dort, wo Tundra
   an Bergwald grenzt (≤ 100 m).
2. **Ruinen:** Sollen Sehenswürdigkeiten später Ruinen tragen? Dann ergänze ich die Efeu-Regeln für Mauern. Bis dahin werden die
   Demo-Bauteile nicht gesetzt. Das ändert den nächsten Schritt nicht.
