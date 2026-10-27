# Antwort 25 – Offene Schalen-Netze, große Platten (PG1), Wasserwände an SWR-Stufen, Erlenbach-Verzweigung

Gelesen: recherche/auftraege/25-schalen-platten-wasserwand-verzweigung.md @ 0ee93788c08db0183dc68d406eaf038e02e5d173 (Commit db438b8)

Stand 27.10.2026. Bearbeiter: Cloud-Recherche. Bereiche: Sitzprüfung (offene Netze, PG1), gebackene SWR p2/UL, Kiesfächer C3.
Neue Regelversionen: **`steine_sitz_regeln.json` 23.13** (Blöcke `nachtrag_23_12` und `nachtrag_23_13`) und
**`gewaesser_biome_regeln.json` v3** (Block `nachtrag_25`). Beide sind lokal ausdrücklich zu übernehmen.

> **Korrektur zu Antwort 24:** Die Kragarm-Regel 23.12 aus 24 §7.1 stand nur im Text, nicht in der JSON. Sie steht jetzt als
> `nachtrag_23_12` in `steine_sitz_regeln.json`; PG1 (§B) verweist darauf.

## Kurzfazit

Ferats Vorgabe „Tempo vor Absicherung“ gilt. Die laufenden PM-Entscheide **bleiben stehen**, mit drei Korrekturen:
- A1: ein Median-Kriterium;
- B7: eine Lauflängen-Grenze statt reiner 5 %;
- C8: zuerst ein 15-Minuten-Test von Epics eigenem Materialplatz, vor C++.

| Nr. | Frage | Urteil | Status |
|---|---|---|---|
| 1 | Dünne Schalen +1 cm | **bestätigt mit Zusatz:** jeder Randpunkt ≤ +1 cm **und** Median ≤ 0 cm (Kontakt). So „klebt“ der Kiesel wie von Ferat verlangt | beantwortet |
| 2 | Spalt ≤ 3 cm | **reparieren**, nur per z-Absenkung (bis −2 cm bzw. Dünnregel), Grenze Einbettung ≤ 60 % der Höhe; im gebackenen Bett nur melden | beantwortet |
| 3 | Wurzeln/Stümpfe offen | **23.10 gilt sinngemäß**, aber nur für Öffnungen ≥ 3 cm Durchmesser; Reparatur z ≤ 15 cm oder Netztausch; nie entfernen | beantwortet |
| 4 | Kulisse/Wandmodule mit freiem Rand | **Felsfuß/Haldenblock davor**, nur wo der Rand von begehbaren Punkten sichtbar ist (23.10 `kulisse.sichtbarkeit`); sonst melden | beantwortet |
| 5 | Netztausch | **freigegeben** (geschlossen, gleiche Familie oder ΔY ≤ 0,10, ±20 % je Achse, danach Sitz- und Wiederholungsprüfung) | beantwortet |
| 6 | Steilhang > 35°, L > 3 m | **PM-Plan bestätigt:** S3 nur mit weiterem Fehler. Die 1 795 übrigen prüft eine Reihen-Regel (Nr. 7); 12 Kontrollbilder entscheiden, ob mehr nötig ist | beantwortet, Bild offen |
| 7 | Rand 5 %, Ausbiss-Reihen | 5 % nur mit **Lauflänge ≤ 15 cm** zusammenhängend und max. +1 cm. Ausbiss-Reihen **nicht ausnehmen**, neue FEHLER-Art `dachziegel_reihe` | beantwortet |
| 8 | Weg A Material | **Erst Epics Platz `BakedSimMaterial` richtig belegen** (MI auf `SW_Water_Material_River_Niagara_Cached`, nicht auf unserem Water-Body-Master). Wirkt das, braucht Weg A kein C++ und keine Systemkopie. Sonst Systemkopie über die Projekteinstellung | wartet auf Test T25-C0 |
| 9 | Stufen < 0,8 m, NS-Zahl | Haut erst **ab 0,5 m** und ≥ 45°-Fläche; darunter nur Schaum (Material bzw. Decal). NS: **höchstens 3 je 50-m-Fenster**, nach Fallhöhe gewählt, nicht je Stufe | beantwortet |
| 10 | Pfütze zudecken | **vertretbar als Zwischenstand**; p2 nicht neu backen. Bedingungen: Abfrage-Test, Randkontrolle, Zudecken als Höhenplan sichern; Neubacken erst im ohnehin geplanten 16h-Bettschritt | beantwortet |
| 11 | Abflussaufteilung | **passt** zu 24 `gletscher.verzweigt`. Nicht die Breite entscheidet, sondern der **Zulauf je SWR** (eigene Quelle). Kriterien gegen „trocken“ in §D.2 | beantwortet |

---

## A. Offene Schalen-Netze

### A.1 Dünne Schalen 2–10 cm (Frage 1)

- **Warum −2 cm hier falsch wäre:** Bei 3,6 cm Dicke (`SM_stone_04`) sind −2 cm schon 55 % der Höhe; der Stein verschwindet.
  Bei dünnen Schalen sieht man den Spalt nicht durch die Dicke, sondern nur als Schattenlinie am Rand.
- **Regel (23.13 `schalen_offen.duenn`):**
  - Öffnung gegen die Auflage-Normale (o·n ≤ −0,7) wie so-r001;
  - jeder offene Randpunkt ≤ **+1 cm** über S bzw. Träger;
  - **neu:** Median aller Randpunkte ≤ **0 cm**.
- **Grund für den Median:** Mit „≤ +1 cm“ allein darf ein Kiesel überall genau 1 cm schweben. Das ist Ferats „klebt nicht am Boden“.
  Der Median erzwingt, dass mindestens die Hälfte des Randes aufliegt oder leicht einsinkt („ein wenig in der Erde“).
- **Reparatur:** z senken, bis der Median 0 cm erreicht ist; höchstens auf 30 % der Dicke Einbettung.

### A.2 Spalt ≤ 3 cm bei richtiger Öffnung (Frage 2)

- **Reparieren**, denn diese Fälle sind nach so-r001 schon FEHLER. 1–3 cm Spalt liest als dunkle Linie bis etwa 15 m.
- **Nur z-Absenkung** bis zur Grenze der eigenen Klasse (dick: alle Randpunkte ≤ −2 cm; dünn: A.1). Dabei gilt höchstens
  60 % der Höhe eingebettet, sonst Netztausch (A.5). Kein Drehen, kein Versetzen.
- **Ausnahme:** Instanzen mit Kollision in Bettzellen eines gebackenen SWR (p2, UL) **nur melden**, Anwendung mit dem nächsten Bake
  (23.10 `bestand_trockene_bettzellen`, 23 §6). Ohne Kollision darf auch dort gesenkt werden: Die SWR sieht nur Kollision und Gelände.
- **Aufwand:** z-Verschiebung je Instanz, reversibel über das Protokoll.

### A.3 Wurzeln und Stümpfe (Frage 3)

- **Gilt sinngemäß.** Man sieht auch hier in ein hohles Netz, nur ist die Öffnung oft ein Rohr (Wurzelende).
- **Einschränkung:** Gezählt werden nur offene Ränder, deren Öffnung ≥ 3 cm Durchmesser hat (größte Ausdehnung der Randschleife).
  Dünne Wurzelspitzen mit offenem Ende sind ab 5 m nicht zu sehen.
- **Reparatur** (Entfernen bleibt lokal verboten):
  1. z bis −15 cm, solange der Stumpf ≥ 70 % seiner Höhe zeigt;
  2. sonst Netztausch (A.5);
  3. sonst melden. Das gilt auch für 7 120 sichtbare Stümpfe.

### A.4 Kulisse ≥ 15 m und Wandmodule 4–15 m mit freiem Rand (Frage 4)

- **Erst Sichtbarkeit**, dann Bauteil: Es zählt nur ein Rand, den man von begehbaren Punkten sieht (23.10 `kulisse.sichtbarkeit`,
  10-m-Raster, 1,7 m Augenhöhe, bis 200 m). Nicht sichtbar: melden.
- **Sichtbar:** einen **Felsfuß** oder **Haldenblock** davorsetzen. Das ist auch fachlich richtig, denn am Fuß einer Wand liegt Schutt
  (Halde, Schüttwinkel 33–37°, 23 `HALDE`).
  - Bauteil: geschlossenes Netz derselben Familie oder ΔY ≤ 0,10;
  - Sitz nach den normalen Regeln (Block ≥ 1 m: Kragarm 23.12);
  - Deckt der Block alle Randpunkte für alle sichtbaren Rasterpunkte? Nachrechnen mit demselben Sichtstrahl.
- **Nicht** in SWR-Bettzellen ohne neuen Bake.

### A.5 Netztausch statt Entfernen (Frage 5)

- **Freigegeben.** Ziel-Typ per Typ-Lesung je Feld wie PG1 §B.4.
- **Bedingungen:**
  - Ziel ist geschlossen, oder seine Öffnung erfüllt nach dem Tausch so-r001;
  - gleiche Familie oder ΔY ≤ 0,10 (23.10 `wand_module`);
  - L, B, T je ±20 %;
  - danach volle Sitzprüfung und **Wiederholung 23.2** (`planer_wiederholung.mindestabstand_gleiches_netz`).
- **Ferats „vier gleiche Steine nebeneinander“:** Der Tausch darf diese Lage nicht erzeugen. Deshalb gehört die Wiederholungsprüfung
  nach dem Tausch zum Schritt. Sie fällt nicht weg, weil der Ort bleibt.

---

## B. Große Platten ≥ 2 m (PG1)

### B.1 Steilhang (Frage 6)

- **PM-Plan bestätigt:** In S3 (Bergfelder) nur Platten > 3 m am Hang > 35° **mit** weiterem Fehler ersetzen (`--nur-steil-mit-fehler`).
- **Begründung:**
  - Eine große, hangparallele, ≥ 30 % eingebettete Platte am Steilhang liest als Felsausbiss, nicht als losgelöste Platte.
  - Loses Material bleibt über etwa 35° nicht liegen (Schüttwinkel, 23 `HALDE`). Eine eingebettete Platte ist aber kein loses Material.
- **Was Ferat stört, ist die Reihe:** Gleich geneigte Platten nebeneinander sehen aus wie Dachziegel. Das fängt B.2 auch bei den
  1 795 sonst gut sitzenden.
- **Kontrolle:**
  - 12 Bilder: 6 Felder mit den meisten der 1 795 (B5, B4, H3, I4, H4 …), je 2 Kameras aus 20–40 m;
  - zeigen ≥ 3 der 12 Bilder Platten, die nicht als Fels lesen (schwebend, gestapelt, Brett), dann die volle Ersetzung (2 068);
  - sonst bleibt es bei 547.

### B.2 Rand-Toleranz und Ausbiss-Reihen (Frage 7)

**Rand-Toleranz:**
- 5 % ist bei großen Platten zu grob: Eine Platte 2 × 1 m hat rund 6 m Rand, also etwa 120 Randpunkte im 5-cm-Abstand. 5 % können
  eine einzige zusammenhängende Lücke von 30 cm sein, und die sieht man.
- **Regel (23.13 `pg1.rand`):** ≤ 5 % der Randpunkte über der Grenze (−2 cm), **und** keine zusammenhängende Strecke > 15 cm,
  **und** kein Punkt > +1 cm über S.

**Ausbiss-Reihen: nicht ausnehmen.**
- Echte Schichtausbisse sind durchgehende Bänder mit Fugen, keine einzelnen gestapelten Platten (23 `ausbiss`: verborgen ≥ 0,5,
  freie Kante ≤ min(0,5 L; 0,6 m)).
- **Neue FEHLER-Art `dachziegel_reihe`.** Sie gilt, wenn alle drei Bedingungen erfüllt sind:
  1. ≥ 3 Platten ≥ 2 m im 15-m-Fenster;
  2. Fallrichtung ±15°, Fallwinkel ±10°;
  3. jede überlappt die nächste hangab mit sichtbarer Kante > 0,6 m.
- **Reparatur:**
  1. jede zweite tiefer (verborgen ≥ 0,5);
  2. sonst eine gegen einen Block tauschen;
  3. sonst entfernen.
- Die echten Dachziegel im Wasser (Imbrikation, 23 `dachziegel`, 8–30°) betrifft das **nicht**. Dort ist die Reihe gewollt; Grenze
  bleibt die lange Achse ≤ 45° zur Strömung (PG1).

**Restliche PG1-Annahmen:** bestätigt.
- hangparallel ≤ 10°;
- eingebettet ≥ 30 % der Dicke;
- Kragarm 23.12;
- Ausnahmen 23.3 und 23 §6 gelten für PG1 nicht.

Das „Brett über Wasser“ (4) ist immer FEHLER: Eine Platte mit beiden Enden auf Ufern und Luft darunter ist ein Bauwerk.
Das widerspricht Ferats Regel „keine menschlichen Spuren“.

---

## C. Wasserwände an den Stufen

### C.1 Ist Weg A nötig? Epics Materialplatz (Frage 8)

**Belegt (Epic-API, Suchauszug):**
- `UShallowWaterRiverComponent` (Header `ShallowWaterRiverActor.h`, Plugin WaterAdvanced) hat in der Kategorie **Rendering** drei
  Materialplätze, alle vom Typ `UMaterialInstance`, editierbar:
  - `BakedSimMaterial`;
  - `BakedSimRiverToLakeTransitionMaterial`;
  - `BakedSimRiverToOceanTransitionMaterial`.
- Laut Python-Doku 5.5 ist das Simulationssystem `river_sim_system` eine `NiagaraComponent`. Welches System sie nutzt, lässt sich in
  den **Projekteinstellungen** (Water → Shallow Water Simulation) festlegen.

**Beobachtung aus dem Forum** (Thread zur Parameter-Referenz):
- Änderungen an der Materialinstanz kommen erst nach **Reset** der Simulation an.

**Euer Befund und meine Lesart:**
- `MI_EL_SWR_Klar` liegt am Platz `baked_sim_material` (16h-6g).
- Seine Kette ist aber `MI_Eldarien_Wasser_Fluss → … → M_Eldarien_Wasser_Schaum8`, also der **Water-Body-Master**
  (`recherche/bilder/swr_p2/mi_el_swr_klar_parameter.txt`).
- Der Niagara-Renderer zeichnet dagegen mit `SW_Water_Material_River_Niagara_Cached`. Dieser Master liest die gebackenen Gitterdaten
  und ist für Niagara freigegeben.
- **Hypothese H1:** Die Komponente reicht `BakedSimMaterial` an den Renderer weiter. Ein Material ohne passende Eltern bzw. ohne
  Niagara-Nutzung fällt dabei auf den Standard zurück, oder die Übergabe passiert nur bei Reset bzw. `UpdateRenderState`.
- **H2:** Der Platz ist ohne Wirkung, der Renderer nimmt immer sein Systemmaterial.
- Unsere Erfahrung „wirkt gebacken nicht“ unterscheidet H1 und H2 nicht.
- Im Projekt liegt schon `MI_Eldarien_Wasser_FlussSim` mit Eltern `…_River_Niagara_Cached` (`inventar_extra.json`).

**Test T25-C0** (15 min, im Speicher, nicht speichern):
1. MI-Kopie von `MI_Eldarien_Wasser_FlussSim` (bzw. neues MI auf `/WaterAdvanced/Niagara/Materials/SW_Water_Material_River_Niagara_Cached`)
   mit einem Signal: `Water Albedo` rot (1, 0, 0) oder `Absorption` 1 000.
2. Am p2-SWR `baked_sim_material` auf diese MI setzen.
3. `render_state` BAKED_SIM → LIVE_SIM → BAKED_SIM umschalten, **ohne Reset und ohne Bake**. Ob ein Reset den Bake verwirft, ist
   nicht belegt; deshalb kommt er in diesem Test nicht vor.
4. Lesen:
   - Bild;
   - `NiagaraFunctionLibrary.get_all_emitters(nc.get_asset())` → `used_renderer_materials`;
   - Materialname am Renderer im Detailfenster der Niagara-Komponente („Override Parameters“).

| Ergebnis | Folge |
|---|---|
| Signal sichtbar (H1) | **Weg A ohne C++:** Kopie des Masters `SW_Water_Material_River_Niagara_Cached` nach `/Game/Eldarien/Welt/Wasser/SWR/`, dort Weißwasser (C.2) und unsere Farben; MI davon als `BakedSimMaterial` je SWR. Kein Eingriff ins Niagara-System |
| Signal erst nach Reset | wie oben, aber Reset ist Pflicht. Vorher die Bake-Daten sichern bzw. prüfen, ob Reset sie verwirft; sonst neu backen |
| kein Signal (H2) | **Weg A mit Systemkopie:** `Grid2D_SW_River` nach `/Game` kopieren, Renderer-Material in der Kopie ersetzen, Kopie in den **Projekteinstellungen** als SWR-System eintragen (Feldname dort ablesen). C++ nur, falls die Einstellung fehlt oder nicht je SWR wirken soll. Kein Neu-Simulieren, aber Neu-Laden der Karte |

**Warum nicht gleich C++:**
- Ein eigenes Plugin, das das Renderer-Material setzt, muss jede Engine-Version mitgehen.
- Beide Epic-Wege sind Inhalt, keine Code-Pflege [Ableitung].

**Weg B** (Stufen-Haut) bleibt der Rückfall.
- Er braucht den Dump nach jedem Bake neu, liegt sonst aber völlig in unserer Hand.
- Läuft er heute gut, schadet er nicht: Haut und Weg A schließen sich nicht aus.
- Bei Erfolg von Weg A die Haut nur an Stufen ≥ 1,5 m behalten. Dort trägt sie das Volumen des Falls, Weg A nur die Farbe.

### C.2 Weißwasser über die Neigung (Material, für Weg A)

- **Prinzip:** Die gebackene Stufe ist eine Rampe von 30–63°. An ihr soll Wasser weiß werden, oben durchsichtig bleiben, unten eine
  Schaumschürze zeigen (euer `MI_EL_Stufenfall_Schnelle` macht dasselbe auf der Haut).
- **Neigung je Pixel:** Normale aus `ddx`/`ddy` der Weltposition.
  - Bei Zelle 36,7 cm wird sie facettiert. Deshalb wird nur die Maske daraus gebildet, nicht die Lichtnormale.
  - Die Lichtnormale bleibt die des Masters.

```hlsl
// Custom-Knoten "EL_Steilmaske" (Pixel-Shader), Eingaenge: WPos (Absolute World Position), A0 = 0.866 (cos 30), A1 = 0.707 (cos 45)
float3 n = normalize(cross(ddy(WPos), ddx(WPos)));     // Vorzeichen je nach Achse; abs(n.z) nimmt es heraus
float  c = abs(n.z);                                   // 1 = flach, 0 = senkrecht
return saturate((A0 - c) / max(A0 - A1, 1e-3));        // 0 unter 30 Grad, 1 ab 45 Grad
```

- **Verwendung:** `Weiss = max(Steilmaske, MasterFoam)`. Damit wirken:
  - BaseColor in Richtung Schaumfarbe;
  - Opacity bzw. Absorption hoch (undurchsichtig);
  - Roughness 0,5;
  - Normalstärke ×0,3.
- **Schaumschürze:** in Fließrichtung 0,5–1,5 m unter dem Rampenfuß.
  - Gebacken ist dort der Schaum 0. Deshalb kommt sie aus einer zweiten Maske: Steilmaske aus der **Höhe 1 m stromauf**, wenn der
    Master die Gitterhöhe als Textur liest. Das ist **zu prüfen** am kopierten Graph.
  - Sonst ein Decal-Band je Stufe aus dem Dump (wie die Haut, nur flach).
- **Farbe:** eure Werte aus dem Befund (Schaumfarbe grün 0,39/0,76/0,56) sind Epics Standard und erklären das „grüne Glas“.
  - Für Weißwasser neutral 0,85/0,87/0,86 (wie `ELD_Schaum_Farbe`).
  - Für das Wasser die `MI_EL_SWR_*`-Werte aus 24 §1.2.
  - Die Einheiten im Niagara-Master sind **zu prüfen**: Absorption 20,8/25/24,7 sieht nach 1/m aus, unsere Werte sind Sichtweiten in cm.
    Umrechnung a [1/m] ≈ 100 / Sichtweite [cm] nur, wenn eine Signalprobe (Absorption ×10 → deutlich dunkler) das bestätigt.

### C.3 Stufen unter 0,8 m und Nature Water FX (Frage 9)

| Fallhöhe | Fläche ≥ 45° in der Stufe | Darstellung |
|---|---|---|
| < 0,5 m | egal | nur Schaum: Weg A Steilmaske bzw. Decal-Schürze; keine Haut, kein NS |
| 0,5–0,8 m | ≥ 0,5 m² | Haut (Weg B) oder Weg A; kein NS |
| 0,5–0,8 m | < 0,5 m² | nur Schaum |
| 0,8–1,0 m | – | Haut/Weg A; `NS_Stream_Small` nur an Schaustellen |
| ≥ 1,0 m | – | Haut/Weg A + `NS_Impact_Small` nach Budget |

- **Budget je Ort** (24 §9.1: höchstens 3 je Ort, 6 aktiv): „Ort“ ist hier ein **50-m-Fenster** entlang des Laufs, nicht die Stufe.
  - Die Talkaskade hat 78 Stufen ≥ 0,8 m. Mit Cull 50 m wären sonst 15–20 Systeme gleichzeitig aktiv.
  - **Auswahl je Fenster:**
    1. die zwei höchsten Stufen ≥ 1,0 m bekommen `NS_Impact_Small`;
    2. eine Rinne bzw. Stufe 0,8–1,8 m bekommt `NS_Stream_Small`;
    3. der Rest trägt nur Material bzw. Haut.
  - Höchstens 6 gleichzeitig regelt der Effekttyp (`NET_EL_Wasser_Nah`, Signifikanz nach Abstand).
- **Grund für 0,5 m:** Unter 0,5 m löst sich der Strahl bei Bachabflüssen kaum ab. Die gebackene Rampe ist dann 1–2 Zellen lang, die
  Haut wäre kürzer als ihr eigener Rand. Weißwasser liest dort als Schaumband [Ableitung, Gestaltung].
- **Die „dünnen weißen Striche“** in Ferats Bild sind sehr wahrscheinlich Schaumstraßen der SWR an Hindernissen (787 im Export) oder
  der Sekundär-Emitter. Prüfen per Ein- und Ausschalten des Sekundär-Emitters (16a D3). Das ist nicht Teil dieser Frage.

---

## D. Erlenbach-Verzweigung im Kiesfächer C3

### D.1 Gebackenes Wasser zudecken statt p2 neu backen (Frage 10)

**Vertretbar als Zwischenstand.** Gründe:
- p2 ist die abgenommene Referenz (K-Kolk, Rauschband 6r). Ein Neu-Bake kostet die Abnahme und ist im 16h-Bettschritt ohnehin geplant.
- Die gebackene Fläche wird mit Tiefentest gezeichnet. Liegt das Gelände darüber, ist sie unsichtbar; die Kosten sind gering
  (Verdeckung) [Ableitung].

**Bedingungen:**
1. **+7 cm je Landschaftsquad**, nicht je Abtastpunkt:
   - Höchster gebackener Spiegel in jeder Gelände-Masche plus 7 cm.
   - Sonst taucht Wasser zwischen den Stützpunkten auf (bilineare Fläche gegen gekrümmten Spiegel).
   - 7 cm liegt über dem Rauschband (≤ 2 cm).
2. **Abfrage-Test:** `use_baked_sim_for_queries_and_physics` liefert dort weiter Wasser. In PIE eine Figur über die zugedeckte Fläche
   laufen lassen. Nicht erlaubt sind Schwimmen, Platschen oder Nässe-Effekte. Tritt das auf, ist die Fläche aus den Abfragen zu
   nehmen; dann doch Neu-Bake oder schmalerer Ost-Arm.
3. **Rand zum Hauptlauf:**
   - An der Grenze Zudeckung/Hauptlauf entsteht eine Uferkante. Sie muss eine Kiesbank-Kante werden (0,12–0,22 m wie die Arme).
   - Keine senkrechte Stufe.
   - Strömungsschaum, der dort in die neue Böschung zeigt, ist hinnehmbar bis zum Neu-Bake.
4. **Sicherung:** Höhenänderung als eigener Plan (Abtrag 2 512 m³, Auftrag 1 531 m³) mit Vorher-Höhen, damit der Neu-Bake im 16h-Bettschritt
   auf derselben Geländebasis läuft und nichts doppelt angepasst wird.
5. **Nicht verdecken:**
   - Wasser in Bettzellen des Hauptlaufs. Prüfung: Die Zudeckungsmaske schneidet keine Zelle mit Tiefe ≥ 5 cm, die mit dem
     Hauptstrom verbunden ist.
   - Verbundenheit über 4-Nachbarschaft ab der p2-Mittellinie.

**Schmaler Ost-Arm plus Neu-Bake** wäre die sauberere Endlösung. Sie gehört in den 16h-Bettschritt, nicht vor die Verzweigung.

### D.2 Abflussaufteilung und „nicht trocken wirken“ (Frage 11)

**Passt.**
- Arme 0,35–0,5 B liegen in 24 `gletscher.verzweigt` (0,3–0,6 B).
- Das Gefälle 1,7–2,1 % ist für Sanderarme typisch; 24 nennt < 2 %, die Abweichung am oberen Ende ist unerheblich.

**Wichtig:** Bei zwei getrennten SWR teilt nicht die Hydraulik den Abfluss. Jede SWR bekommt ihren Zulauf aus ihrer eigenen Quelle.
- Die Schwelle 2 cm über dem gebackenen p2-Spiegel heißt: Aus p2 fließt nichts über.
- Der Arm „beginnt“ hinter der Schwelle. Das ist natürlich, denn Sanderarme beginnen oft hinter Kiesbarren mit Sickerzulauf.
- Der Zulauf muss aber so gewählt werden, dass der Arm voll wirkt.

**Richtwerte** (Manning, n 0,035 Kies, h 0,30 m; Rechnung in dieser Antwort):

| Arm | B | Gefälle | v | Froude | Q |
|---|---|---|---|---|---|
| schmal | 2,0 m | 1,7–2,1 % | 1,40–1,56 m/s | 0,82–0,91 | 0,84–0,93 m³/s |
| breit | 3,0 m | 1,7–2,1 % | 1,48–1,64 m/s | 0,86–0,96 | 1,33–1,48 m³/s |

- **Leitfähigkeits-Anteil eines Arms am Hauptlauf** (B 6 m, h 0,35–0,6 m): 0,10–0,37.
  - Drei Arme zusammen 0,4–0,9 des Hauptlaufs. Das ist eine kräftige Verzweigung.
  - Den Zulauf je Arm-SWR auf **0,25 Q_p2** setzen, nicht höher. Sonst wirkt der Hauptlauf daneben schwach, obwohl er bitgleich bleibt.
- **Froude 0,8–1,0** ist gut für das Bild: kräuselnde, stehende Wellen.
  - Über 1,0 drohen in der Simulation Rollwellen bzw. ein Sägezahn (6s).
  - Dann das Gefälle des Arms auf ≤ 1,8 % senken. Nicht verbreitern, das macht ihn flach und trocken.

**Kriterien „wirkt nicht trocken“** (Dump nach dem Bake):
- Tiefe ≥ 0,10 m auf ≥ 80 % der Bettbreite und ≥ 95 % der Armlänge;
- v ≥ 0,5 m/s auf ≥ 90 % der Länge;
- Nasslinie: Lage Nass/Schlamm 0,3–0,5 m über die Wasserlinie hinaus (16h-6i-Master);
- keine Pfütze ≥ 2 m² ohne Verbindung.

**Zusammenfluss mit UL (s 148/185):**
- wie die Naht in 24 §7.3: Überlappung 5–10 m;
- Spiegelunterschied ≤ 2 cm;
- nie an einer Stufe;
- UL ist Senke beider Arme.

---

## Nächste Handlung

**Eine Handlung:** Test **T25-C0** (§C.1).
- Rahmen: 15 min, p2 im Speicher, nichts speichern.
- **Schritte:**
  1. Signal-MI auf `SW_Water_Material_River_Niagara_Cached` als `baked_sim_material` setzen.
  2. `render_state` umschalten.
  3. Bild und `used_renderer_materials` lesen.
- **Erfolg:** Das Signal ist sichtbar, oder der Renderer nennt die neue MI. Dann Weg A als Materialkopie, ohne C++.
- **Fehlschlag:** Weg A mit Systemkopie über die Projekteinstellung.
- **Abbruch:**
  - Die SWR verliert die gebackene Fläche: zurückschalten, Karte nicht speichern.
  - Das Signal erscheint erst nach Reset: zuerst klären, ob Reset den Bake verwirft.

**Warum diese Handlung:** Sie entscheidet, ob für alle Wasserwände an 116 Stufen (p2 86, UL 30) ein Material genügt oder ob pro Bake
eine Haut nachgebaut werden muss. A, B und D laufen unabhängig mit den bestätigten Regeln weiter.

## Was fehlt bis Witcher 4

Nach Wirkung, nur für diesen Vorgang:

1. **Stufen lesen als fallendes Wasser** (C): Grünes „Glas“ an 116 Stufen ist heute der auffälligste Fehler im Bach. Weißwasser an der
   Rampe plus Schaumschürze verwandelt die Talkaskade.
2. **Kein Blick in hohle Netze** (A): 36 525 sichtbar falsche Instanzen weltweit; Stufe 2 schließt die meisten. Kiesel, die kleben
   (Median ≤ 0), statt schweben.
3. **Keine Dachziegel-Reihen am Hang** (B): Die neue Reihen-Regel zielt genau auf Ferats Bild; Einzelplatten dürfen Fels bleiben.
4. **Verzweigter Bach mit eigenem Leben** (D): Arme mit Froude 0,8–1,0 und Nasslinie wirken wie ein Sander. Ohne vollen Zulauf
   wirken sie wie Gräben.
5. **Wiederholung nach jedem Tausch prüfen** (A.5): sonst entstehen beim Reparieren neue Vierer-Reihen.

## Quellen

- `UShallowWaterRiverComponent` (WaterAdvanced, `ShallowWaterRiverActor.h`; `BakedSimMaterial`, `BakedSimRiverToLakeTransitionMaterial`,
  `BakedSimRiverToOceanTransitionMaterial`, Kategorie Rendering, `UMaterialInstance`) [Suchauszug; Seite für die Cloud gesperrt]:
  https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/UShallowWaterRiverComponent
- `EShallowWaterRenderState`: https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterAdvanced/EShallowWaterRenderState
- Python 5.5 `ShallowWaterRiverComponent` (`river_sim_system`, Projekteinstellung; `baked_sim` nur lesbar) [Suchauszug]:
  https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/ShallowWaterRiverComponent?application_version=5.5
- Epic-Tutorial „Baked River Simulations – Parameter Reference“ und Forenfaden (MI-Änderung erst nach Reset) [Suchauszug]:
  https://dev.epicgames.com/community/learning/tutorials/72Lb/unreal-engine-baked-river-simulations-parameter-reference ;
  https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112
- Packaging und Render State „Water Component with Baked Sim“ [Forum, Suchauszug]:
  https://forums.unrealengine.com/t/shallow-water-body-advanced-water-plugin-fails-to-render/2634176
- SWR 5.7.4 Initialisierung [Forum, Suchauszug]: https://forums.unrealengine.com/t/shallowwaterriver-simulation-does-not-initialize-in-unreal-engine-5-7-4/2731772
- Schaum/Weißwasser als Splash, Oberflächenschaum, Blasen [Epic-Community, Suchauszug]: https://dev.epicgames.com/community/learning/tutorials/orJv/welcome-to-niagara-fluids
- Manning-Fließformel; Kies-Rauheit n ≈ 0,03–0,04 (Chow 1959, Open-Channel Hydraulics) [Fach]
- Schüttwinkel, Imbrikation, Ausbiss: `steine_sitz_regeln.json` quellen `HALDE`, `IMBRIKATION` [Projekt]
- Projekt: 16a §B2/D1–D4, 16h-6g §1.1, 16h-6i, 16h-6r/6s, 23h §3–4, 24 §1.2/§7.1/§7.3/§9.1, `recherche/bilder/swr_p2/mi_el_swr_klar_parameter.txt`,
  `vorlagen/daten/inventar_extra.json`

## Rückfragen

1. **Zulauf der Arm-SWR:** Ich nehme an, O1 und O2/U/S haben eigene Quell-Water-Bodies ohne hydraulische Verbindung zu p2. Ist der
   Arm-Quellkörper stattdessen p2 selbst (p2 als `source_river_water_bodies`)? Dann gilt §D.2 trotzdem, aber die Schwelle 2 cm über dem
   Spiegel würde den Zulauf sperren. In dem Fall die Schwelle auf 2 cm **unter** den Spiegel legen.
2. **Ort der Abfrage-Probe D.1-2:** Gibt es lokal schon ein Spielfigur-Testlevel mit Wasser-Abfrage (Schwimmen/Platschen)? Sonst reicht
   `UWaterSubsystem`-Abfrage per Python an 10 Punkten der Zudeckung (Tiefe muss ≤ 0 sein).
