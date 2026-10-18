# Antwort 23b – Erkennbare Wiederholung, Spiegeln, weiße Steine, Stamm mit Wurzelteller: Regeln 23.2

Gelesen: recherche/auftraege/23b-wiederholung-spiegeln-weisse-steine.md @ 3457153480318106b022c1ececb9183f899a546c (Commit f38a710)

Stand 18.10.2026. Bearbeiter: Cloud-Recherche. Nachtrag zu 23 (Prüfung v4, Werkzeug „umsetzen“, Planer, Pilot C2).
**Hier ist nichts im Projekt geprüft oder angewendet.** Der Code in §10 lief nur synthetisch in der Cloud.

**Lieferung:** dieses Dokument; `steine_sitz_regeln.json` auf **23.2** (nur Zusätze, Liste unter `aenderungen`); Prüfcode-Delta
`wiederholung_23b.py` (§10).

**Bezug (Commit 264a4d8):**
- `23-steine-organisch-im-boden.md` @ e59924ba88b1e24579646389eb5e843cffd657e4; Regeln 23.1 @ 9204740206626a0efbb16b4e39b5082ff016f5f7.
- `auftraege/16h-nachtrag6j-teilung-ergebnis.md` @ a49de2d42844b7e0b1488209f1a0dccc872f2d44 (Z. 49–50, `ukjhcamga`);
  `antworten/16h-nachtrag6i-baked-sim-tests-stand.md` @ b3582ca1c2e105c43cbb346c06418a212d133e4b (§4/§5).
- `material_parameter.json` @ 16d1511f96f8e01fa2bfcf71042b912b638a2b54, `netze_masse.json` @ c337d5bb6082f7098e05738dde6596557f0de386,
  `stein_albedo.json` @ de519d4e95d022dc9da5a5757719d756f3436f86, `helle_steine_p2.json` @ d2c2da602d9d29c7f65885a9948b757b2b94925e,
  `p2_bett_regeln.json` @ 79702dfb1ccfb627ede2f31fa5de144c305c28f8.
- Bild, selbst angesehen: `ferat_wiederholung_c2_bett_2026-10-18.jpg` @ b4711ae0ba3b64f2d2e645dbc5e1a308a4deffd3.

**Kennzeichnung:** [S] = nur Suchauszug (Epic-Seiten und Foren aus der Cloud per DNS nicht erreichbar) · [Repo] · [Bild] = eigene Ansicht ·
[Ableitung] = geschlossen, nicht belegt · [Test] = nur lokal klärbar.

## Kurzfazit

1. **Wiederholung erkennbar – beantwortet, Kalibrierung offen (T23b-1).** Gemessen werden ρ = Mittenabstand/Größe und θ = Drehdifferenz
   aus dem FQuat (über die Netzsymmetrie minimiert). Fels: FEHLER bei ρ < 3 und θ < 45°. Stein: FEHLER bei ρ < 2 und θ < 30°.
   Kiesel: nur Doppelte. Gruppe: ≥ 3 ähnliche Felsen in 15 m ergeben FEHLER.
2. **Spiegeln – fachlich meist unbedenklich, technisch in 5.8 nicht belegt.** Nur X oder Y negativ, nie Z. Gesperrt bis zum
   Einzeltest T23b-S. Allein wirkt Spiegeln nur halb, denn Spiegelbilder werden als dasselbe Objekt erkannt [S].
3. **Reihenfolge – beantwortet, gegenüber Ferats Vorschlag geändert:** drehen → spiegeln *mit* Drehung → Netz tauschen → Skala ergänzend
   → versetzen/entfernen. Skala bei Wiederholung: Fels/Stein/Holz 0,85–1,15, Achsverhältnis ≤ 1,10. Platte/Kleinschutt bleiben 0,8–1,0 wie in 23.
4. **Planerregel – beantwortet (§5).** Mindestabstand je Netz, Yaw gleichverteilt, Spiegeln p = 0,5 nach Freigabe, Deckel je 15-m-Fenster,
   Familienrotation.
5. **Weiße Steine – Verdacht durch Repo-Daten gestützt, im Projekt unbestätigt.** `skjsL_tier_0` (103 gesetzt) und `texndcpda_tier_0` haben
   **kein gemessenes Y**. `M_MS_Base` hat als Standardtextur `T_DefaultColor`, wie bei `ukjhcamga`.
   - Entscheidung: Material reparieren, Steine behalten.
   - Helligkeit trocken: WARNUNG ab Y 0,22, FEHLER ab 0,35. Nass: WARNUNG ab 0,09, FEHLER ab 0,15.
6. **Stamm mit Wurzelteller auf dem Bettgrund – entschieden: FEHLER** (Regel 23 bleibt). Ein Stamm, der länger ist als das Gerinne breit,
   wird nicht transportiert [S]. Den Teller aufs Ufer setzen, sonst entfernen; ein Treibholz-Netz sofort entfernen.
7. **Code und JSON – geliefert, nur synthetisch geprüft:** `SELBSTTEST OK  Regeln 23.2  Faelle 49  Signatur dabb50741db8b9ac`. Der 23-Code
   behält mit der 23.2-Datei seine Signatur `64a654746495eca8`.

**Nächste Handlung (genau eine, lokal):** **T23b-0** – Einzeltest Spiegeln plus nur lesende Zählung der Wiederholungs- und
Materialkandidaten in C2 (§11).

---

## 1. Bildbefund [Bild]

| Stelle | Beobachtung | Urteil 23.2 | dazu nach 23 |
|---|---|---|---|
| oben Mitte | zwei große, hellbraune Felsplatten (geschätzt 4–6 m) lehnen direkt nebeneinander; Neigung, Drehung und Größe gleich | Paar ρ ≈ 0,5–1, θ ≈ 0–10° → **FEHLER** | Sind es Platten (T/B ≤ 0,35), stehen sie schräg ohne Ausbiss-Gruppe (2 < 3) → FEHLER `winkel` |
| links | zwei runde, aufrechte Blöcke gleicher Form, Abstand etwa 1–1,5 Größen | Paar Fels → **FEHLER** | – |
| Bett | 6–7 **rein weiße**, schattierte Steine ohne Struktur (links Mitte rund ~0,5 m, unten Mitte flach, oben rechts, Splitter in der Mitte) | `textur_fehlt` / `untexturiert_verdacht` | – |
| rechts | große, sehr helle Platte mit Struktur | Helligkeit, Warnband | – |
| quer | heller, fast rindenloser Stamm von den Ufersteinen rechts schräg hinab; links Wurzelanlauf auf nassem Bettgrund mit glatter, ockerfarbener Scheibe; keine Wurzelgrube am Ufer | §7 → **FEHLER** | Teller im Wasser; Farbe wie Treibholz |

Die weiße Linie mit Querstrichen ist die Spline im Editor und wurde nicht bewertet.

## 2. Wann ist eine Wiederholung erkennbar? (Frage 1)

Eingaben aus dem Zensus: Netz, Klasse (23 `klasse_aus`), Lage, FQuat (x, y, z, w), Skala je Achse, Grenzen aus `netze_masse.json`.

| Größe je Paar desselben Netzes | Definition |
|---|---|
| s | größte Ausdehnung × \|Skala\| der größeren Instanz (m) |
| ρ | Abstand der Boxmitten in Welt / s (Boxmitte statt Pivot, wegen Slab-Pivot 6i) |
| Spiegelzustand | Produkt der Skalenvorzeichen < 0. Kanonische Drehung R' = R·diag(Vorzeichen), gespiegelt zusätzlich ·diag(1, −1, 1). Damit sind X- und Y-Spiegel bis auf 180° gleich |
| θ | min über g ∈ Symmetrie(Netz) von ∠(R'_iᵀ R'_j g), geodätisch. Symmetrie um lokal Z: 1, 2, 4 oder 0 (rund); bis zur Punktwolke streng 1 |
| σ | Verhältnis der mittleren \|Skala\| − 1 |

θ ist bei aufrechten Netzen und Blick in Augenhöhe praktisch der Yaw-Unterschied, also die Silhouette. Bei liegenden Platten ist es die Drehung
um die Normale, und Spiegeln ändert zusätzlich den Umriss. Die Kippung ist bei Platten durch das Gelände festgelegt (23 §4).

| Klasse | θ „ähnlich“ | FEHLER ρ < | WARNUNG ρ < | Gruppe (Fenster Ø) | Häufung → WARNUNG |
|---|---|---|---|---|---|
| Fels ≥ 1 m | < 45° | 3 | 6 | ≥ 3 ähnliche in 15 m → FEHLER | ≥ 3 gleiche in 15 m |
| Platte liegend ≥ 1 m | < 30° um die Normale | 3 | 5 | ≥ 3 in 15 m → FEHLER | ≥ 4 |
| Stein 0,3–1 m | < 30° | 2 | 4 | ≥ 4 in 5 m → WARNUNG | ein Netz > 40 % bei ≥ 5 Steinen in 15 m |
| Kiesel < 0,3 m | – | – | – | – | ein Netz > 60 % in 5 m |
| Kleinschutt-Fläche | < 30° | – | 1,5 | – | – |
| Stamm / Stumpf | < 45° / < 30° | 2 | 5 / 4 | ≥ 3 in 30 m FEHLER / ≥ 3 in 15 m WARNUNG | Stamm ≥ 2 in 30 m |
| **alle: doppelt** | θ < 5° ∧ ρ < 0,05 ∧ σ < 0,05 → FEHLER | | | | |

**Abstufung:** „nur gespiegelt“ (Netz ohne Spiegelsymmetrie) senkt das Urteil um eine Stufe, ebenso σ ≥ 0,25. Gespiegelt und skaliert
zusammen ergibt „ok“.

**Begründung:**
- Erkennen ist weitgehend unabhängig von Lage, Größe und Links-rechts-Spiegelung (Biederman & Cooper 1991) [S]. Drehung in der Tiefe
  senkt das Erkennen metrischer Formen stark (Biederman & Bar 1999) [S]. Deshalb hilft Drehen voll, Skala und Spiegeln nur halb.
- Große Felsen sind strenger geregelt: Ihre Form fällt auf, und sie stehen auch aus größerer Distanz zusammen im Bild.
- Eine Form ist ab etwa 2° Sehwinkel lesbar, also bis D ≈ 29 s [Ableitung]. Für einen Kiesel von 0,2 m sind das 6 m, und seine Form
  ist generisch.
- Spielpraxis: Wenige Felsnetze reichen, wenn sie gedreht und skaliert werden [S, Neverwinter].

## 3. Spiegeln (Frage 2)

### 3.1 Fachlich

| Fall | Urteil / Regel 23.2 |
|---|---|
| gescannter Fels/Stein, entkoppelt (Megascans/Fab) | unbedenklich, Gestein hat keine lesbare Händigkeit; nach T23b-S erlaubt |
| Moos oder Flechte oben in der Albedo | unbedenklich, bleibt oben |
| Moos oder Flechte auf einer Seite (Nord/Schatten) | betrifft Drehen genauso. `moos_seite` je Netz (anzulegen); Seite ≤ 60° von der Sollrichtung, beim Drehen und beim Spiegeln |
| schräge innere Schichtung, Ausbiss/Band | das sichtbare Fallen kippt gegen die Gruppe. Nur mit `schichtung_ok` (Schichten ∥ Dickenachse), sonst Drehung um die Normale oder Netztausch |
| AO bzw. gerichtetes Licht in der Albedo | AO spiegelt mit, unkritisch. Bei einem Helligkeitsgefälle zwischen den Seiten > 20 %: kein Spiegeln, Yaw nur ±30°. `M_Master_material`-Pakete zuerst messen |
| Stoßseite, Treibholz zur Strömung | Ausrichtung zur Strömung prüfen (wie Dachziegel, 23 §4) |
| Schrift/Decals | im Bestand nicht betroffen |
| Totholz | X/Y unkritisch, nach T23b-S erlaubt; das Teller-Ende bleibt am Ufer |
| **Z negativ** | oben und unten vertauscht (Moos unten, Erdanschnitt oben): **immer FEHLER `spiegel_z`** |

### 3.2 Technisch in UE 5.x

| Punkt | Bekannt | Status |
|---|---|---|
| Wicklung/Culling | Negative Skala dreht die Wicklung um; Einzelnetze gleicht der Renderer aus. UE4-ISM: „nicht unterstützt, anderer Cull-Modus braucht einen eigenen Draw-Call“. UE-76078 (4.22): ISM und Einzelnetz verhalten sich verschieden [S] | für UE5 GPU-Scene/Nanite **nicht belegt** → [Test] |
| Nanite | keine Quelle | [Test], mit Nanite und mit `r.Nanite 0` |
| Foliage ISM/HISM | UE5-Foren: schwarze Artefakte bzw. umgedrehte Normalen; die Gegenmittel „TwoSided aus“ und „TwoSided an“ widersprechen sich [S] | [Test], Painter und Skript-Setzer getrennt |
| Normalmap | Fehler kommen meist von gespiegelten UVs; der Editor gleicht negative Skala aus, der FBX-Export nicht [S] | [Test], WorldNormal-Puffer |
| Kollision | UE-51647 (Convex, behoben 4.19), UE-96052 (gedrehte Formen, behoben 5.0), UE-142739 (Chaos-Shape gespiegelt, behoben 5.0) [S]; Kugeln/Kapseln skalieren nicht ungleichmäßig [S, alt] | [Test], Box/Convex und Complex-as-Simple |
| VSM, Lumen | keine Quelle | [Test] |
| RVT-Fuß | liest Welt-XY und Welt-Z (`Fuss_Z`, `Blend_Hoehe`), daher unabhängig von der Skala [Ableitung]; Risiko nur bei Knoten im Objektraum | [Test], falls das MI RVT nutzt |

### 3.3 Einzeltest T23b-S

- **Aufbau:** Testlevel aus T23-0, gleiches Licht.
- **Netze:** Nanite `SM_LargeFallenTree_01` (`nanite: true`); Nicht-Nanite `SM_mountain_rock_small_01_1`; ein Fab-Raw-Fels erst nach der
  MI-Reparatur.
- **Varianten:** A (1, 1, 1), B (−1, 1, 1), C (1, −1, 1), D (−1, −1, 1) als Drehkontrolle.
- **Setzwege:** Akteur; Foliage über den Skript-Setzer von „umsetzen“; Foliage-Painter, falls er negative Skala zulässt [Test].

| Prüfung | Bestanden, wenn |
|---|---|
| V1 Normalen | WorldNormal: B/C sind das Spiegelbild von A, keine invertierten oder schwarzen Flächen; Nanite gleich Fallback |
| V2 Schatten | VSM-Umriss = gespiegelter Umriss von A; Eigenschatten ohne Löcher |
| V3 Licht | Lumen ohne dunklen Saum; Normalmap-Details auf derselben Seite beleuchtet wie bei A unter gespiegelter Kamera |
| C1 Line-Trace | je Instanz 16 Strahlen senkrecht und 8 waagrecht, einfach und komplex; Treffer ≤ 1 cm vom gespiegelten Sollpunkt |
| C2 Laufen | Figur auf und gegen B/C: kein Durchfallen, keine unsichtbare Wand; die Collision-Ansicht deckt sich mit dem Netz |
| E1 Persistenz | Speichern, Neuladen und HISM-Neuaufbau erhalten die Vorzeichen; der Zensus liest sie zurück |

**Ergebnis:** Freigabe `spiegeln.freigabe` je Render- und Setzweg. Fällt ein Weg durch, wird dort nicht gespiegelt, sondern das Netz
getauscht. Eine gespiegelte Netzkopie wäre ein eigener Assetauftrag.

## 4. Reihenfolge und Skala (Frage 3)

Geändert wird die kleinere bzw. später gesetzte Instanz. Nach jedem Schritt laufen die Sitzprüfung 23.1 und die Wiederholungsprüfung neu.
1. **Drehen:** Yaw (Platte: um die Normale) auf ≥ θ zu jedem gleichen Netz im Fenster.
2. **Spiegeln + Yaw ≥ 45°**, nur nach der Freigabe.
3. **Netz tauschen** gegen ein Geschwister: gleiches Gestein, gleiche Größenklasse, Grundriss ± 20 %.
4. **Skala** nur ergänzend.
5. **Versetzen** in den XY-Grenzen 23.1, sonst entfernen mit Sicherung.

**Änderung zu Ferats Reihenfolge:** Die Skala kommt nach dem Netztausch, weil die Größe kaum gegen das Wiedererkennen hilft (§2).
Gespiegelt wird nur zusammen mit Drehung. Ausbiss-Gruppen behalten Fallen und Streichen; dort nur Drehung um die Normale, Spiegeln in
der Schichtebene oder Netztausch.

| Skala relativ zum Planer | gleichmäßig | Achsverhältnis | Grund |
|---|---|---|---|
| Fels, Stein, Stamm, Stumpf | 0,85–1,15 | ≤ 1,10 (±10 % je Achse) | Texeldichte ändert sich ≤ 15 %, Größenklasse bleibt |
| Detailscan (Fab Raw 8K, Helden ≥ 2 m nah) | wie oben | ≤ 1,02 | gestreckte Scanstruktur wird sichtbar |
| Kiesel | 0,8–1,25 | ≤ 1,10 | generische Form |
| Platte, Kleinschutt | 0,8–1,0 | 1,0 | **wie 23**: größere Platten folgen dem Gelände schlechter |

**Verhältnis zu 23:**
- 23 §10.1 Schritt 4 („nur verkleinern 0,8–1,0“) gilt weiter für Sitzfehler.
- Die Skalenregel für Wiederholungskorrekturen an Fels, Stein und Holz ist neu; sie ergänzt 23, sie hebt nichts auf.
- Die p2bett-Holzspanne 0,6–1,8 [Repo] bleibt Planervariation. Nach §2 zählt sie nur als „Skala allein“.

## 5. Planerregel gegen Kopien (Frage 4)

Erweiterung des Setzer-Vertrags 23 §11: Vor dem Schreiben laufen `sitz_pruefung` **und** `pruefe_wiederholung` gegen die gesetzten
Instanzen aller Planer im Fenster.

| Regel | Wert |
|---|---|
| Mindestabstand gleiches Netz | ρ_f × s (Stein 2, Fels/Platte 3), außer θ ≥ θ der Klasse |
| Yaw | gleichverteilt 0–360° (Platten um die Normale) |
| Spiegeln | p = 0 bis zur Freigabe, danach 0,5, sofern §3.1 nicht greift |
| Deckel je 15-m-Fenster | Fels ≥ 2 m: 2 gleiche; Fels 1–2 m: 3; Platte ≥ 1 m: 3; Stein: ein Netz ≤ 40 %; Stamm: 1 gleicher je 30 m |
| Familienrotation | Wahl „am längsten nicht benutzt im Fenster“. Familien je Rolle anzulegen, z. B. `SM_mountain_rock_small_01_1–5`, `SM_SmallStonesPack_*`, `SM_stones_01_*`, Namaqualand `_a/_b`. `pjcxN` ist laut Paketname Sandstein → Zugehörigkeit prüfen |

| Planer (23 §11) | Änderung |
|---|---|
| **detailgrad** | K3/K4 mit Familienrotation; im selben Haufen nie zweimal dasselbe Netz; Platten-Yaw um die Normale gleichverteilt |
| **p2bett** | Keystones und Lippen: Querlage fest, Variation über das Netz. Holz: ein Netz je 30 m, Teller am Ufer |
| **kantenufer_p2** | Uferblöcke ρ ≥ 3 je Netz, Familie wechseln |
| **bachdekor_swr** | Steine ≥ 0,3 m: ein Netz ≤ 40 %; `skjsL_tier_0` erst nach der MI-Reparatur; `SM_beach_driftwood_01` gestrichen (23) |
| **felsschalen, felsgruppen** | Helden ≥ 2 m: höchstens 2 je 15 m. Ausbiss/Band: Variation nur in der Schichtebene oder über das Netz |
| **B5-Themen, Biom-Planer** | über `felsgruppen_overrides` (wie 23) |

## 6. Weiße Steine (Frage 5)

**Befund [Repo]:**
- `helle_steine_p2.json`: **Y = null** für `skjsL_tier_0` (bachdekor_swr, uferblock, 103 gesetzt, 84 im Bett), `texndcpda_tier_0` (6)
  und `SM_beach_driftwood_01` (14). Die Albedo-Messung fand für sie also keine BaseColor-Textur.
- `netze_masse.json`: Beide Fab-Netze haben nur ihr Paket-MI (`MI_skjsL`, `MI_texndcpda`). Laut 6i fehlen die Fab-MI `MI_EL_<id>` bis auf
  `MI_EL_Klippe_xjijbgx`; gesetzt wurde mit Paketmaterial.
- `material_parameter.json`: `M_MS_Base` (28 Instanzen) und `M_MS_Decal` haben als Standard-BaseColor `/Fab/Textures/Standard/T_DefaultColor`.
  Das ist das Muster von `ukjhcamga` (Fab Raw, MI auf `M_MS_Base` ohne gebundene Texturen, weiß).
- [Ableitung] Die weißen Steine sind sehr wahrscheinlich Fab-Raw-Netze mit ungebundenem Paket-MI. Bestätigt ist das erst mit dem Zensus (§11).

**Entscheidung: Material reparieren, Steine behalten.**
- Je Netz `MI_EL_<id>` auf `M_EL_Fels_MS2` mit `T_<id>_8K_B/_N/_ORM` (anzulegen; Kanalbelegung prüfen).
- **Neu in der Reihenfolge:** Das ist eine Asset-Änderung und läuft **vor** T23-2. „Farbe zuletzt“ (23 §10.2) gilt weiter für den Tausch
  einzelner Instanzen.
- Entfernt wird nur, was auch nach den Sitzregeln (23) oder nach §2 durchfällt.
- Ferats Regel „jedes Fab-Raw-Netz braucht ein MI_EL“ wird zur Prüfung: FEHLER `textur_fehlt`, wenn das wirksame MI nicht unter
  `/Game/Eldarien/` liegt oder die BaseColor ungebunden bzw. `T_Default*` ist.

**Prüfer (ein Treffer genügt):**
1. **Material:** MI-Kette bis zum Master, je Texturparameter der wirksame Wert. Ungebunden, gleich der Master-Vorgabe, `T_Default*`,
   `WhiteSquareTexture` oder `DefaultTexture` → FEHLER. Python-Aufrufe (`MaterialEditingLibrary.get_material_instance_texture_parameter_value`
   u. a.) gegen die 5.8-API prüfen.
2. **Messung:** Steht in `stein_albedo.json` kein Y → WARNUNG `ohne_Y`.
3. **Bild:** Instanzmittel Y ≥ 0,6 bei Sättigung ≤ 0,05 → FEHLER `untexturiert_verdacht`.

**Helligkeit eines nordischen Bachsteins** (Mittel-Y der wirksamen BaseColor, linear):

| Zustand | Ziel | WARNUNG | FEHLER | sRGB 8 bit |
|---|---|---|---|---|
| trocken | 0,07–0,22 (wie 23) | 0,22–0,35 | ≥ 0,35 | 0,22 ≈ 129, 0,35 ≈ 160 |
| nass/unter Wasser | 0,06–0,09 (Ziel 0,08, 6d) | 0,09–0,15 | ≥ 0,15 | 0,09 ≈ 85, 0,15 ≈ 108 |
| Quarz-Ausnahme | Kiesel ≤ 0,15 m, ≤ 1 je 20 m | bis 0,45 | darüber | – |

**Herleitung:**
- PBR-Tabellen nennen „rock“ 0,3–0,4 linear (sRGB ≈ 147–168), nass deutlich dunkler; Kohle 0,04, Neuschnee 0,8–0,9 [S]. Einen Wert eigens
  für Granit fand ich nicht.
- Die Bachnetze im Projekt liegen bei 0,087–0,229 [Repo]. Granit oder Gneis mit Flechte und Algenfilm ist dunkler als die Tabellenspitze.
- Daher liegt FEHLER an der unteren Kante heller Gesteine (0,35). Das Warnband beginnt am Palettenende aus 23.
  `SM_mountain_rock_small` (0,229) bleibt WARNUNG.

**Konsistenz mit 23 §8:** „weiß“ relativ (≥ 2 × Median der Nachbarn) und die Quarzregel bleiben. Neu sind die absoluten FEHLER-Grenzen und
`textur_fehlt`.

## 7. Stamm über dem Bett mit Wurzelteller auf dem Grund (Frage 6)

**Fachlich [S]:**
- In kleinen Gerinnen sind Stücke stabil, die länger als die Gerinnebreite sind (Montgomery & Buffington 1993 nach Cenderelli 2023).
- Stämme mit Teller wandern deutlich kürzer als ohne (chilenische Bergbäche).
- Totholz kommt durch Ufererosion und Windwurf ins Gerinne; der Teller bleibt am Abrissufer (23).

**Natürliche Bilder:**
- (a) Windwurf: Teller am Ufer aufgestellt, mit Grube; Stamm als Brücke (23 §7).
- (b) Uferanbruch: Teller mit Erdscholle am Böschungsfuß, Abrisskante darüber, Stamm zur Gegenseite hinauf.
- (c) Teller nach Transport im Gerinne: nur in Flüssen, die breiter sind als der Stamm lang.

**Im Bild passt keines davon:**
- Der Teller steht frei im nassen Bett, ohne Grube und ohne Abriss links.
- Der Stamm ist mindestens so lang wie das Bett breit, also nicht transportfähig.
- Er ist hell und rindenlos wie Treibholz; im bachdekor stehen 14 `SM_beach_driftwood_01`.

**Urteil: FEHLER.**
1. Ist es `SM_beach_driftwood_01`: entfernen (23 `nicht_im_bergbach`).
2. Sonst das Teller-Ende bestimmen (23 §7) und so drehen bzw. versetzen, dass der Teller ≥ 50 % trocken und ≥ 0,3 m hinter der Kante liegt.
   Bedingungen als Brücke: je Ende ≥ 0,5 m Auflage, Unterkante ≥ 0,10 m über W, XY ≤ 0,5 m längs und ≤ 0,3 m quer.
3. Geht das nicht: entfernen (Tundra-Referenz 0 Stämme, 20 §7). Ersatz nur über eine p2bett-Neuplanung (`schraeg_an_lippenende`, Teller am Ufer).

**Neu:** Bild (b) ist als von Hand gesetzter Sehens-Ort zulässig, nicht für Planer: Teller ≥ 50 % an der Böschung, Abrisskante und Grube sichtbar.

## 8. Regeln 23.2 – Ergänzungen

| Regel | Zahl | ändert 23? |
|---|---|---|
| Wiederholung Fels | FEHLER ρ < 3 ∧ θ < 45°; WARNUNG ρ < 6; Gruppe ≥ 3 in 15 m FEHLER; Häufung ≥ 3 WARNUNG | neu |
| Wiederholung Platte | θ < 30° um die Normale; ρ < 3 / < 5; Gruppe ≥ 3 in 15 m | neu |
| Wiederholung Stein | θ < 30°; ρ < 2 / < 4; Gruppe ≥ 4 in 5 m WARNUNG; ein Netz ≤ 40 % | neu |
| Wiederholung Holz | Stamm θ < 45°, ρ < 2 / < 5, ≥ 2 je 30 m WARNUNG; Stumpf wie Stein | neu |
| doppelt (alle) | ρ < 0,05 ∧ θ < 5° ∧ σ < 0,05 → FEHLER | neu |
| Abstufung | nur gespiegelt −1; σ ≥ 0,25 −1 | neu |
| Spiegeln | X oder Y, nie Z (FEHLER); zwei negative Achsen → WARNUNG; Freigabe nach T23b-S, dann p = 0,5 | neu |
| Skala Wiederholung | Fels/Stein/Holz 0,85–1,15, Achsverhältnis ≤ 1,10, Detailscan ≤ 1,02; Platte/Kleinschutt 0,8–1,0 | Ergänzung; 23 §10.1 bleibt für Sitzfehler |
| Reihenfolge | Sitz → Wiederholung (groß vor klein) → Totholz → Farbtausch; MI-Reparatur vorab als Asset-Änderung | MI-Reparatur vorgezogen |
| Helligkeit | trocken WARNUNG 0,22–0,35, FEHLER ≥ 0,35; nass WARNUNG 0,09–0,15, FEHLER ≥ 0,15 | FEHLER-Grenzen neu |
| untexturiert | BaseColor ungebunden/`T_Default*` → FEHLER; Y ≥ 0,6 ∧ S ≤ 0,05 → FEHLER | neu |
| Wurzelteller | in der Talkaskade nie im Wasser; Uferanbruch nur als Sehens-Ort | bestätigt; Ausnahme neu |
| Netzmerkmale (anzulegen) | `symmetrie_z`, `spiegel_sym`, `moos_seite`, `schichtung_ok`, `detailscan`, `familie` | neu |

## 9. Prüffälle gut/schlecht

**Synthetisch** (Code §10, Sollwerte von Hand; einzeln unter `pruef_faelle_synthetisch` in der JSON):
- W1–W16 Wiederholung, darunter W4 „nur gespiegelt“ → WARNUNG, W5 gespiegelt + 60° → ok, W11 Gruppe → FEHLER, W14 Z → FEHLER,
  W16 spiegelsymmetrisch → FEHLER;
- S1–S7 Skala; M1–M10 Material.

**Kontrollfälle im Testlevel** (ergänzen K1–K16 aus 23 §12.2):

| K | Aufbau | Soll |
|---|---|---|
| K17/K18 | `SM_mountain_rock_big_02_1` zweimal, 9 m Abstand (ρ ≈ 1,9), Yaw 10° / 120° | FEHLER paar / ok |
| K19 | wie K17, die zweite mit Skala (1, −1, 1), gleicher Yaw | WARNUNG |
| K20 | drei `SM_mountain_rock_small_01_1`, Abstand 1,5 m, Yaw 0/5/10 | FEHLER paar |
| K21/K22 | `skjsL_tier_0` mit Paket-MI / mit `MI_EL_skjsL` (anzulegen) | FEHLER textur_fehlt / ok |
| K23 | Stamm mit Teller im Becken / Teller 0,5 m hinter der Kante, als Brücke | FEHLER / ok |
| K24 | Skala (1, 1, −1) | FEHLER spiegel_z |

| gut (Projekt) | schlecht (Ferats Bild) |
|---|---|
| zwei Blöcke einer Familie, verschiedene Netze, verzahnt | zwei gleiche Platten nebeneinander mit gleicher Drehung (oben Mitte) |
| gleiches Netz, 120° gedreht, durch Gras getrennt | Paar gleicher Blöcke (links) |
| grauer, nass dunkler Stein mit Struktur | rein weißer Stein ohne Struktur (Bett) |
| Stamm als Brücke, Teller mit Grube am Ufer | heller Stamm mit Teller auf dem Bettgrund |

## 10. Prüfcode-Delta (Python 3, nur Standardbibliothek)

Eigene Datei neben `sitz_pruefung.py` (23 §13); dieser bleibt unverändert.

**Lokal (Rolle 1):**
- FQuat aus dem Zensus, Klasse aus `klasse_aus`.
- Für 70 Felder einen Gitterindex je Netz vorschalten (Zelle = `gruppe_d`).
- Den wirksamen BaseColor-Pfad je Instanz aus dem Editor-Export an `material_pruefen` geben.

**Cloud-Ergebnis:**
- `python -I wiederholung_23b.py --selbsttest` zweimal und mit `--regeln recherche/antworten/steine_sitz_regeln.json`: Signatur
  `dabb50741db8b9ac`. Der 23-Code mit der 23.2-Datei: `64a654746495eca8`.
- Gegenprobe: Mit Fels-θ 5° und Warnbeginn trocken 0,25 schlagen W1, W7, W11 und M5 fehl.
- Laufzeit 0,04 s.

```python
# wiederholung_23b.py - Delta zu sitz_pruefung.py (Antwort 23b, Regeln 23.2): Wiederholung, Spiegeln, Skala, Material/Helligkeit.
# Aufruf: python -I wiederholung_23b.py --selbsttest [--regeln steine_sitz_regeln.json]  (nur Standardbibliothek)
# Eingabe je Instanz wie Zensus: Netz, Klasse (aus sitz_pruefung.klasse_aus), Lage m, Drehung als FQuat (x, y, z, w), Skala je Achse.
import argparse, hashlib, json, math

W = {  # = steine_sitz_regeln.json "wiederholung" (23.2); rho = Mittenabstand / Groesse s, theta Grad
    "fels": {"theta": 45, "rho_f": 3.0, "rho_w": 6.0, "gruppe_d": 15.0, "gruppe_n": 3, "gruppe_urteil": 2, "haeufung_n": 3},
    "platte": {"theta": 30, "rho_f": 3.0, "rho_w": 5.0, "gruppe_d": 15.0, "gruppe_n": 3, "gruppe_urteil": 2, "haeufung_n": 4},
    "stein": {"theta": 30, "rho_f": 2.0, "rho_w": 4.0, "gruppe_d": 5.0, "gruppe_n": 4, "gruppe_urteil": 1, "haeufung_n": 0},
    "totholz_stamm": {"theta": 45, "rho_f": 2.0, "rho_w": 5.0, "gruppe_d": 30.0, "gruppe_n": 3, "gruppe_urteil": 2, "haeufung_n": 2},
    "totholz_stumpf": {"theta": 30, "rho_f": 2.0, "rho_w": 4.0, "gruppe_d": 15.0, "gruppe_n": 3, "gruppe_urteil": 1, "haeufung_n": 0},
    "kleinschutt": {"theta": 30, "rho_f": 0.0, "rho_w": 1.5, "gruppe_d": 0, "gruppe_n": 0, "gruppe_urteil": 0, "haeufung_n": 0},
    "abstufung_skala": 0.25, "doppelt": {"rho": 0.05, "theta": 5, "sigma": 0.05},
    "skala": {"fels": (0.85, 1.15, 1.10), "stein": (0.85, 1.15, 1.10), "kiesel": (0.8, 1.25, 1.10), "platte": (0.8, 1.0, 1.0),
              "kleinschutt": (0.8, 1.0, 1.0), "totholz_stamm": (0.85, 1.15, 1.10), "totholz_stumpf": (0.85, 1.15, 1.10), "detailscan_aniso": 1.02},
    "Y": {"trocken": (0.22, 0.35), "nass": (0.09, 0.15), "untexturiert_Y": 0.6, "untexturiert_s": 0.05},
    "default_textur": ("/Fab/Textures/Standard/T_Default", "/Engine/EngineResources/WhiteSquareTexture", "/Engine/EngineResources/DefaultTexture"),
}
STUFE = ("ok", "WARNUNG", "FEHLER")

def qmul(a, b):
    ax, ay, az, aw = a; bx, by, bz, bw = b
    return (aw*bx + ax*bw + ay*bz - az*by, aw*by - ax*bz + ay*bw + az*bx, aw*bz + ax*by - ay*bx + az*bw, aw*bw - ax*bx - ay*by - az*bz)
def q_achse(achse, grad):
    h = math.radians(grad) / 2; n = math.sqrt(sum(c * c for c in achse))
    return tuple(c / n * math.sin(h) for c in achse) + (math.cos(h),)
def matrix(q):  # Spalten = lokale X, Y, Z in Welt
    x, y, z, w = q
    return ((1 - 2*(y*y + z*z), 2*(x*y - z*w), 2*(x*z + y*w)), (2*(x*y + z*w), 1 - 2*(x*x + z*z), 2*(y*z - x*w)),
            (2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x*x + y*y)))
def mm(a, b): return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def tr(a): return tuple(tuple(a[j][i] for j in range(3)) for i in range(3))
def diag(d): return ((d[0], 0, 0), (0, d[1], 0), (0, 0, d[2]))
def rz(grad):
    c, s = math.cos(math.radians(grad)), math.sin(math.radians(grad)); return ((c, -s, 0), (s, c, 0), (0, 0, 1))
def winkel_rot(a): return math.degrees(math.acos(max(-1.0, min(1.0, (a[0][0] + a[1][1] + a[2][2] - 1) / 2))))

class I:
    def __init__(s, nr, netz, klasse, pos, q, skala, bmin, bmax, sym_z=1, spiegel_sym=False, detailscan=False):
        s.nr, s.netz, s.klasse, s.pos, s.skala, s.sym_z, s.spiegel_sym, s.detailscan = nr, netz, klasse, pos, skala, sym_z, spiegel_sym, detailscan
        sg = tuple(1 if v >= 0 else -1 for v in skala); s.gespiegelt = sg[0] * sg[1] * sg[2] < 0
        s.R = mm(matrix(q), diag(sg)); s.R = mm(s.R, diag((1, -1, 1))) if s.gespiegelt else s.R   # kanonische Drehung (det +1)
        s.groesse = max((bmax[k] - bmin[k]) * abs(skala[k]) for k in range(3)); s.betrag = sum(abs(v) for v in skala) / 3
        c = [(bmin[k] + bmax[k]) / 2 * skala[k] for k in range(3)]; M = matrix(q)
        s.mitte = tuple(pos[i] + sum(M[i][k] * c[k] for k in range(3)) for i in range(3))
        s.z_negativ, s.sg, s.Q = sg[2] < 0, sg, M

def theta(a, b):  # kleinste Drehdifferenz ueber die Symmetrie um lokal Z (sym_z = n-zaehlig; 0 = rotationssymmetrisch)
    if a.sym_z == 0: return winkel_rot(mm(tr(a.R), b.R)) if abs(mm(tr(a.R), b.R)[2][2] - 1) > 1e-9 else 0.0  # nur Kippung zaehlt
    n = max(1, a.sym_z); paare = [(a.R, b.R)] + ([(a.Q, b.Q)] if a.spiegel_sym else [])   # spiegelsymmetrisch: Spiegeln aendert nichts
    return min(winkel_rot(mm(mm(tr(x), y), rz(360.0 * k / n))) for x, y in paare for k in range(n))

def paar(a, b):
    """Urteil 0/1/2 fuer zwei Instanzen desselben Netzes, mit Grund."""
    gross = a if a.groesse >= b.groesse else b; r = W.get(gross.klasse)
    d = math.dist(a.mitte, b.mitte); rho = d / gross.groesse; th = theta(a, b)
    sigma = max(a.betrag, b.betrag) / min(a.betrag, b.betrag) - 1
    D = W["doppelt"]
    if rho < D["rho"] and th < D["theta"] and sigma < D["sigma"] and a.gespiegelt == b.gespiegelt: return 2, "doppelt", rho, th
    if r is None or th >= r["theta"]: return 0, "", rho, th
    stufe = 2 if rho < r["rho_f"] else (1 if rho < r["rho_w"] else 0)
    if stufe and a.gespiegelt != b.gespiegelt and not a.spiegel_sym: stufe -= 1      # Spiegeln allein: eine Stufe
    if stufe and sigma >= W["abstufung_skala"]: stufe -= 1                            # Skala allein: eine Stufe
    return stufe, ("paar" if stufe else ""), rho, th

def pruefe_wiederholung(insts):
    out = {i.nr: [0, set()] for i in insts}; netze = {}
    for i in insts:
        netze.setdefault(i.netz, []).append(i)
        if i.gespiegelt and i.z_negativ: out[i.nr][0] = 2; out[i.nr][1].add("spiegel_z")
        elif not i.gespiegelt and min(i.sg) < 0: out[i.nr][0] = max(out[i.nr][0], 1); out[i.nr][1].add("negativ_ohne_spiegel")
    for netz, L in netze.items():
        aehnlich = {i.nr: set() for i in L}
        for x in range(len(L)):
            for y in range(x + 1, len(L)):
                a, b = L[x], L[y]; st, grund, rho, th = paar(a, b)
                if th < W.get(a.klasse, {"theta": 0})["theta"]: aehnlich[a.nr].add(b.nr); aehnlich[b.nr].add(a.nr)
                for i in (a, b):
                    if st > out[i.nr][0]: out[i.nr][0] = st
                    if grund: out[i.nr][1].add(grund)
        for i in L:
            r = W.get(i.klasse)
            if not r or not r["gruppe_n"]: continue
            nah = [j for j in L if j is not i and math.dist(i.mitte[:2], j.mitte[:2]) <= r["gruppe_d"]]
            gruppe = [j for j in nah if j.nr in aehnlich[i.nr]]
            if len(gruppe) + 1 >= r["gruppe_n"] and all(aehnlich[j.nr] for j in gruppe):
                out[i.nr][0] = max(out[i.nr][0], r["gruppe_urteil"]); out[i.nr][1].add("gruppe")
            elif r["haeufung_n"] and len(nah) + 1 >= r["haeufung_n"]:
                out[i.nr][0] = max(out[i.nr][0], 1); out[i.nr][1].add("haeufung")
    return {k: (STUFE[v[0]], sorted(v[1])) for k, v in out.items()}

def skala_pruefen(klasse, alt, neu, detailscan=False):
    lo, hi, an = W["skala"][klasse]; f = [abs(neu[k]) / abs(alt[k]) for k in range(3)]
    g = (f[0] * f[1] * f[2]) ** (1 / 3); aniso = max(f) / min(f); fe = []
    if not lo - 1e-9 <= g <= hi + 1e-9: fe.append("skala")
    if aniso > (W["skala"]["detailscan_aniso"] if detailscan else an) + 1e-9: fe.append("skala_aniso")
    return fe

def material_pruefen(basecolor_pfad, Y=None, s=None, nass=False):
    """basecolor_pfad = wirksame BaseColor-Textur der MI (None = nicht gebunden); Y/s = gemessenes Mittel (linear, HSV-Saettigung)."""
    if basecolor_pfad is None or basecolor_pfad.startswith(W["default_textur"]): return "FEHLER", "textur_fehlt"
    if Y is None: return "WARNUNG", "ohne_Y"
    if Y >= W["Y"]["untexturiert_Y"] and (s or 0) <= W["Y"]["untexturiert_s"]: return "FEHLER", "untexturiert_verdacht"
    w, f = W["Y"]["nass" if nass else "trocken"]
    return ("FEHLER", "zu_hell") if Y >= f else (("WARNUNG", "hell") if Y >= w else ("ok", ""))

def selbsttest():
    B = ((-1.0, -0.8, 0.0), (1.0, 0.8, 1.2))   # Fels 2,0 x 1,6 x 1,2 m, Pivot unten Mitte
    ST = ((-0.25, -0.2, 0.0), (0.25, 0.2, 0.3)); KI = ((-0.08, -0.06, 0.0), (0.08, 0.06, 0.07)); P = ((-1.2, -0.8, 0.0), (1.2, 0.8, 0.2))
    z = lambda g: q_achse((0, 0, 1), g); E = (1, 1, 1); L = []
    def add(nr, netz, kl, pos, q, sk=E, bb=B, **kw): L.append(I(nr, netz, kl, pos, q, sk, bb[0], bb[1], **kw))
    add("W1a", "SM_A", "fels", (0, 0, 0), z(0)); add("W1b", "SM_A", "fels", (4, 0, 0), z(10))              # rho 2 -> FEHLER
    add("W2a", "SM_B", "fels", (0, 20, 0), z(0)); add("W2b", "SM_B", "fels", (4, 20, 0), z(120))            # gedreht -> ok
    add("W3a", "SM_C", "fels", (0, 40, 0), z(0), sym_z=2); add("W3b", "SM_C", "fels", (4, 40, 0), z(180), sym_z=2)  # C2 -> FEHLER
    add("W4a", "SM_D", "fels", (0, 60, 0), z(0)); add("W4b", "SM_D", "fels", (4, 60, 0), z(0), (1, -1, 1))  # nur gespiegelt -> WARNUNG
    add("W5a", "SM_E", "fels", (0, 80, 0), z(0)); add("W5b", "SM_E", "fels", (4, 80, 0), z(60), (1, -1, 1)) # Spiegel + 60 Grad -> ok
    add("W6a", "SM_F", "fels", (0, 100, 0), z(0)); add("W6b", "SM_F", "fels", (4, 100, 0), z(5), (1.3, 1.3, 1.3))  # nur Skala -> WARNUNG
    add("W7a", "SM_G", "fels", (0, 120, 0), z(0)); add("W7b", "SM_G", "fels", (9, 120, 0), z(10))           # rho 4,5 -> WARNUNG
    add("W8a", "SM_H", "stein", (0, 140, 0), z(0), bb=ST); add("W8b", "SM_H", "stein", (0.8, 140, 0), z(10), bb=ST)  # rho 1,6 FEHLER
    add("W9a", "SM_I", "kiesel", (0, 160, 0), z(0), bb=KI); add("W9b", "SM_I", "kiesel", (0.3, 160, 0), z(0), bb=KI)  # Kiesel ok
    add("W10a", "SM_J", "kiesel", (0, 170, 0), z(0), bb=KI); add("W10b", "SM_J", "kiesel", (0.004, 170, 0), z(1), bb=KI)  # doppelt
    for k, x in enumerate((0, 7, 14)):                                     # Gruppe: rho 3,5 je Paar, aehnlich -> Gruppe FEHLER
        add("W11" + "abc"[k], "SM_K", "fels", (x, 190, 0), z(10 * k))
    for k, (x, g) in enumerate(((0, 0), (7, 120), (14, 240))):             # gleiches Netz, gedreht: nur Haeufung -> WARNUNG
        add("W12" + "abc"[k], "SM_L", "fels", (x, 210, 0), z(g))
    add("W13a", "SM_M", "platte", (0, 230, 0), z(0), bb=P); add("W13b", "SM_M", "platte", (5, 230, 0), z(40), bb=P)   # Platte 40 Grad ok
    add("W14", "SM_N", "fels", (0, 250, 0), z(0), (1, 1, -1))              # Z gespiegelt -> FEHLER
    add("W15", "SM_O", "fels", (0, 270, 0), z(0), (-1, -1, 1))             # zwei negative = Drehung -> WARNUNG
    add("W16a", "SM_P", "fels", (0, 290, 0), z(0), spiegel_sym=True); add("W16b", "SM_P", "fels", (4, 290, 0), z(0), (-1, 1, 1), spiegel_sym=True)
    soll = {"W1a": "FEHLER", "W1b": "FEHLER", "W2a": "ok", "W2b": "ok", "W3a": "FEHLER", "W3b": "FEHLER", "W4a": "WARNUNG", "W4b": "WARNUNG",
            "W5a": "ok", "W5b": "ok", "W6a": "WARNUNG", "W6b": "WARNUNG", "W7a": "WARNUNG", "W7b": "WARNUNG", "W8a": "FEHLER", "W8b": "FEHLER",
            "W9a": "ok", "W9b": "ok", "W10a": "FEHLER", "W10b": "FEHLER", "W11a": "FEHLER", "W11b": "FEHLER", "W11c": "FEHLER",
            "W12a": "WARNUNG", "W12b": "WARNUNG", "W12c": "WARNUNG", "W13a": "ok", "W13b": "ok", "W14": "FEHLER", "W15": "WARNUNG",
            "W16a": "FEHLER", "W16b": "FEHLER"}
    erg = pruefe_wiederholung(L); fehl = [(k, v, erg[k]) for k, v in soll.items() if erg[k][0] != v]
    sk = {"S1": (skala_pruefen("fels", E, (0.9, 0.9, 0.9)), []), "S2": (skala_pruefen("fels", E, (1.2, 1.2, 1.2)), ["skala"]),
          "S3": (skala_pruefen("fels", E, (1.08, 1.0, 1.0)), []), "S4": (skala_pruefen("fels", E, (1.12, 1.0, 1.0)), ["skala_aniso"]),
          "S5": (skala_pruefen("fels", E, (1.04, 1.0, 1.0), True), ["skala_aniso"]), "S6": (skala_pruefen("platte", E, (1.1, 1.1, 1.1)), ["skala"]),
          "S7": (skala_pruefen("fels", E, (-1.0, 1.0, 1.0)), [])}
    fehl += [(k, v[1], v[0]) for k, v in sk.items() if v[0] != v[1]]
    ma = {"M1": (material_pruefen(None), "FEHLER"), "M2": (material_pruefen("/Fab/Textures/Standard/T_DefaultColor"), "FEHLER"),
          "M3": (material_pruefen("/Game/X/T_x_B", 0.85, 0.01), "FEHLER"), "M4": (material_pruefen("/Game/X/T_x_B", 0.14), "ok"),
          "M5": (material_pruefen("/Game/X/T_x_B", 0.229), "WARNUNG"), "M6": (material_pruefen("/Game/X/T_x_B", 0.40), "FEHLER"),
          "M7": (material_pruefen("/Game/X/T_x_B", 0.08, nass=True), "ok"), "M8": (material_pruefen("/Game/X/T_x_B", 0.11, nass=True), "WARNUNG"),
          "M9": (material_pruefen("/Game/X/T_x_B", 0.16, nass=True), "FEHLER"), "M10": (material_pruefen("/Game/X/T_x_B"), "WARNUNG")}
    fehl += [(k, v[1], v[0]) for k, v in ma.items() if v[0][0] != v[1]]
    for k in sorted(erg, key=lambda s: (int("".join(c for c in s if c.isdigit())), s)): print("%-5s %-8s %s" % (k, erg[k][0], ",".join(erg[k][1]) or "-"))
    for z_ in fehl: print("ABWEICHUNG", z_)
    sig = hashlib.sha256(json.dumps([sorted(erg.items()), sorted(sk.items()), sorted(ma.items())], sort_keys=True).encode()).hexdigest()[:16]
    n = len(soll) + len(sk) + len(ma)
    print(("SELBSTTEST OK" if not fehl else "SELBSTTEST FEHLGESCHLAGEN") + "  Regeln 23.2  Faelle %d  Signatur %s" % (n, sig))
    return not fehl

def lade_regeln(pfad):
    with open(pfad, encoding="utf-8") as fh: j = json.load(fh)
    w = j.get("wiederholung")
    if not w: raise SystemExit("Regeldatei ohne 'wiederholung' (Version < 23.2)")
    for kl, r in w["klassen"].items(): W[kl].update({k: r[k] for k in W[kl] if k in r})
    W["abstufung_skala"] = w["abstufung_skala_ab"]; W["doppelt"].update(w["doppelt"])
    for kl, r in j["skala_wiederholung"]["klassen"].items(): W["skala"][kl] = (r["gleichmaessig"][0], r["gleichmaessig"][1], r["aniso_max"])
    W["skala"]["detailscan_aniso"] = j["skala_wiederholung"]["detailscan_aniso_max"]
    h = j["farbe"]["helligkeit_23_2"]; W["Y"].update(trocken=tuple(h["trocken_warnung_fehler"]), nass=tuple(h["nass_warnung_fehler"]))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--selbsttest", action="store_true"); ap.add_argument("--regeln"); a = ap.parse_args()
    if a.regeln: lade_regeln(a.regeln)
    if a.selbsttest: raise SystemExit(0 if selbsttest() else 1)
    ap.print_help()
```

## 11. Nächste Handlung (genau eine, lokal)

**T23b-0: Einzeltest Spiegeln (T23b-S, §3.3) und nur lesende Zählung der Kandidaten in C2.** Zuständig: Projektleitung im Editor, Rolle 1
für die Zählung. Budget ≈ 90 min. Keine Projektänderung.

**Schritte:**
1. Beide Selbsttests ausführen.
2. T23b-S nach §3.3.
3. Zensus C2 s 389–580 (Fenster wie 23 §14.1): `pruefe_wiederholung` je Klasse und Planerschicht.
4. Den wirksamen BaseColor-Pfad je Netz ausgeben.
5. Treffer in `C2_t430_ferat` (anzulegen) verorten.

**Erfolg:**
- Signaturen gleich; ein eindeutiges T23b-S-Urteil je Render- und Setzweg.
- Beide Paare aus Ferats Bild gemeldet.
- Jeder weiße Stein einer `textur_fehlt`-Instanz zugeordnet, sonst der Gegenbefund benannt.
- Netz und Teller-Ende des Stamms festgestellt; FEHLER/WARNUNG je Klasse gezählt.

**Abbruch:**
- Abweichende Signatur: Ursache melden (Achsen, Reihenfolge im Quaternion).
- Absturz oder Datenverlust in T23b-S: Spiegeln bleibt gesperrt, die Zählung läuft trotzdem.

**Danach:** `MI_EL_<id>` für die gefundenen Fab-Raw-Netze anlegen; die Wiederholungsreparatur läuft mit T23-2.

## Was fehlt bis Witcher 4

Nach Wirkung:
1. **Kein untexturiertes Material im Bild.** Eine Importsperre (MI_EL Pflicht, Prüfer §6) wirkt für die ganze Welt, nicht nur für C2.
2. **Gleiche Netze sehen verschieden aus.** Weltbezogenes Moos oben, Nasslinie, RVT-Fuß (`MF_EL_RVT_Fuss` anzulegen) und Begleitsteine
   brechen Kopien stärker als Drehen (23 §9).
3. **Mehr Netze je Familie:** ≥ 6 Felsen und ≥ 8 Steine je Gestein, aus dem freien Fab-/Megascans-Bestand, kein Kauf.
4. **Eine Prüfung für alle Planer**, später auch für PCG. Ob es in 5.8 einen PCG-Knoten für Selbstabstand je Netz gibt, ist zu prüfen.
5. **Silhouetten durch Verbünde:** Haufen aus 2–4 Teilen statt Einzelblöcken (20).
6. **Totholz mit Geschichte:** Teller am Ufer mit Grube und Moos; kein Treibholz im Bergbach.

## Quellen (abgerufen 18.10.2026)

WebFetch scheiterte (DNS) bei `issues.unrealengine.com`, `forums.unrealengine.com` und `shinsoj.artstation.com`. Alles ist **Suchauszug [S]**.

**Wahrnehmung:**
- [Biederman & Cooper 1991, Perception 20, 585](https://journals.sagepub.com/doi/pdf/10.1068/p200585) – Erkennen unabhängig von Lage und
  Links-rechts-Orientierung.
- [Biederman & Bar 1999, Vision Research 39, 2885](https://www.nmr.mgh.harvard.edu/publications/journal_articles/2753) – Drehung in der
  Tiefe senkt das Erkennen metrischer Unterschiede.
- [Neverwinter Art-Blog](https://www.arcgames.com/pl/games/neverwinter/news/detail/10090723-art-developer-blog%253A-cold-run) – fünf
  Felsnetze, gedreht und skaliert.

**Unreal, negative Skala:**
- [Forum 397236](https://forums.unrealengine.com/t/are-there-any-issues-with-setting-a-negative-scale-to-a-mesh/397236)
- [UE-51647](https://issues.unrealengine.com/issue/UE-51647), [UE-96052](https://issues.unrealengine.com/issue/UE-96052),
  [UE-142739](https://issues.unrealengine.com/issue/UE-142739), [UE-15682](https://issues.unrealengine.com/issue/UE-15682),
  [UE-76078](https://issues.unrealengine.com/issue/UE-76078)
- [Answers 880097 (FBX)](https://answers.unrealengine.com/questions/880097/view.html)
- [SideFX-Forum (Instanz-Normalen)](https://www.sidefx.com/forum/post/437778/)

**Albedo:**
- [Enscape](https://learn.enscape3d.com/?p=32192), [War Thunder PBR-Wiki](https://old-wiki.warthunder.com/PBR_texture_compliance)
- [Polycount](https://polycount.com/discussion/comment/2705069),
  [Shinsoj-Chart](https://shinsoj.artstation.com/blog/Q9j6/pbr-color-space-conversion-and-albedo-chart)

**Totholz:**
- [Cenderelli 2023, USDA FS](https://seakfhp.org/wp-content/uploads/2023/11/Session-1.5-Beyond-Biology-Recruitment-and-Delivery-of-Wood-CENDERELLI.pdf)
- [ESurf 8, 195 (2020)](https://esurf.copernicus.org/articles/8/195/2020/),
  [FAO Agris, Gangwon-do](https://agris.fao.org/search/zh/records/676559e450e69ae81838a79a)

**Repo:** siehe Bezugsliste oben.
