# Planer-Anleitung: Sehenswürdigkeiten-Planer je Biom (Auftrag 13, Phase 2)

Mit dieser Anleitung schreibt ihr die 14 übrigen Biom-Planer nach demselben Muster wie der Referenzplaner
**`skripte/sehens_bergwald/`**. Die Planer enthalten fast keinen eigenen Code: Jeder Ort ist ein **Rezept** in
`sehens_<biom>_regeln.json`, und die Bibliothek `sehens_lib` baut daraus das Lieferformat `vorlagen/SEHENS_FORMAT.md`.
Python-Code braucht ihr nur für Formen, die sich nicht als Regel ausdrücken lassen (Hooks).

Pflichtlektüre vorher: `vorlagen/SEHENS_FORMAT.md` (ganz), `vorlagen/FORMAT.md` §3, `auftraege/13-…` (Abschnitt
„Witcher-Qualität“), `13b`, `13c`, euer `sehens/<biom>/katalog.md` + `asset_bedarf.json` (inkl. „Abgleich 13b/13c“).

---

## 1. Was ein Planer liefert

| Was | Wohin (Lauf mit `--aus X`) | Format |
|---|---|---|
| `orte.json` (alle 8 Orte) | `X/orte.json` | SEHENS_FORMAT §2 (+ Erweiterungen, unten) |
| Geländestempel | `X/gelaende/<id>.f32` | §3, Δ in m, float32, **immer 1 m**, Rand 0 |
| Bodenlagen | `X/lagen/<id>_<Lage>.r8` | §3, uint8 0–255, **immer 1 m** |
| Instanzen + Akteure | `X/sw_<biom>/<Feld>/plan.json` + `<Schlüssel>.f32` | §4 / FORMAT.md §3 (10 float32 je Instanz) |
| Testbilder | `antworten/sehens/<biom>/test_<id>.png` (`--bild --bild-ordner`) | Draufsicht |

Ins Repo kommen **nur** `skripte/sehens_<biom>/sehens_<biom>.py`, `sehens_<biom>_regeln.json`, eine kurze `README.md`
im Planerordner und die Testbilder. Die Planausgabe des Testlaufs bleibt im Scratchpad
(`…/scratchpad/a13/p2/<biom>/`).

Aufruf (wie die Auftrag-11-Planer, SEHENS_FORMAT §1):

```
python -I recherche/antworten/skripte/sehens_<biom>/sehens_<biom>.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <scratchpad>/a13/p2/<biom> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/<biom>]
```

Ohne `--daten2m` liest der Planer die 1-m-Originale aus `<basis>/export/unreal/welt/` und schreibt nach
`export/unreal/welt/sehens/<biom>/` bzw. `export/unreal/welt/sw_<biom>/` (so läuft er lokal bei Claude/Ferat).

## 2. Aufbau eines Planers

1. `skripte/sehens_bergwald/` als Vorlage kopieren, `BIOM = "<biom>"` setzen, Dateinamen anpassen.
2. `HOOKS` leeren oder durch eigene ersetzen (Signatur `f(ctx)`, siehe §5). Sonst nichts am Ablauf ändern.
3. Je Ort aus `standorte.json` einen Block unter `"orte"` in der Regeldatei anlegen (Schema §3). Der Planer bricht ab,
   wenn ein Ort kein Rezept hat.
4. Testen (§7), Bilder ansehen, Regeln nachschärfen, wieder testen.

Ablauf in `rezept.OrtKontext.baue()` (Reihenfolge ist wichtig für Referenzen):

```
anker -> linien -> anker_danach -> Hook "anker"
-> gelaende.ops -> Seebecken (wasser/see mit becken) -> Hook "nach_gelaende" -> Bachlinien (+ Rinnen) -> fertig()
-> wasser (see/bach/wasserfall) -> gruppen (in Listenreihenfolge!) -> Hook "gruppen"
-> pfad (Bodenband, Trittsteine, Stufen) -> lagen -> effekte/klaenge/freiraeume -> Hook "ende"
-> (schreibe_biom) budget/Ausdünnen -> orte.json-Eintrag, Dateien, Ebene
```

Gruppen sehen nur Gruppen, die **vor** ihnen stehen (Kontaktzonen, „auf Gruppe“, `z_bezug`). Also: Held → Begleiter →
Schutt → Bewuchs → Kleinzeug → Kontakt.

## 3. Regeln-JSON-Schema

### 3.1 Oberste Ebene

```json
{"_doku": {...}, "biom": "bergwald", "seed": 1302,
 "paletten": {"kiesel": ["SM_stone_04", "SM_stone_06"], ...},
 "materialwuensche": [{"name": "MI_EL_SW_<Kurz>", "basis": "<Master>", "parameter": {...}, "fuer": ["SM_..."]}],
 "orte": {"<ort_id>": { ...Rezept... }}}
```

- `paletten`: benannte Netzlisten; überall, wo `palette` steht, darf ein Paletten-Name stehen.
- `materialwuensche`: ≤ 6 je Biom (§7). Nur Master aus `M_EL_Fels_MS`, `M_EL_Fels_Auflage`, `M_EL_Fels_Sand`,
  `M_EL_Klippe_RVT`, `M_EL_Pflanze`, `M_EL_Eis4`, `M_EL_Wasserfall2`, `M_MS_Decal`, `M_MS_Base`, nur deren Parameter
  (`vorlagen/daten/material_parameter.json`; der Planer prüft das). Jeder Wunsch landet in `orte.json` beim ersten Ort,
  der ihn benutzt; Gruppen verweisen mit `"material": "MI_EL_SW_…"` darauf.
- Ort-Feld `warnung_akzeptiert: {"lagen_fenster": "<Begruendung>"}` (E49): das Lagenfenster > 400 m (nur Leuchtfeuer,
  Grenze 600 m) meldet der Prüfer dann als HINWEIS mit Begründung statt als WARNUNG.

### 3.2 Rezept eines Orts

| Schlüssel | Inhalt |
|---|---|
| `kurz`, `marker` | Kurzbeschreibung (§2), Kartenmarker `{"titel", "text", "entdeckung_m"}` – Ton: Dark Fantasy, 1–2 Sätze |
| `budget` | Katalog-Richtwerte (nur Vergleich, HINWEIS bei > 125 %). Harte Grenzen §9 setzt die Lib (Ausdünnen). |
| `budget_grenzen` | optional schärfere harte Grenzen `{"instanzen", "kollision", "akteure"}` |
| `assets_wunsch` | `[{"paket": "<Name wie downloadliste.json>", "statt_jetzt": "<Ersatz aus dem Bestand>"}]` |
| `anker`, `linien`, `anker_danach` | benannte Punkte/Linien (3.3) |
| `gelaende` | Fenster + Werkzeuge (3.4) |
| `wasser` | `see`, `bach`, `wasserfall` (3.5) |
| `gruppen` | Instanzen je Detail-Ebene (3.6) |
| `lagen` | Bodenlagen (3.7) |
| `pfad` | Pfad-Bodenband aus `standorte.json` (3.8) |
| `effekte`, `klaenge`, `freiraeume` | (3.9) |
| beliebige weitere Schlüssel | für eigene Hooks (z. B. `gasse` beim Windwurf) |

### 3.3 Punkte, Richtungen, Anker, Linien

**Punkt-Referenz** (`bei`, `punkte`, …): `"mitte"` · `"<anker>"` · `[dx, dy]` (m relativ zur Ortsmitte, **+Y = Süden**) ·
`{"pos_m": [x, y]}` (Welt) · `{"von": ref, "richtung": rspec, "abstand_m": d}` · `{"anker": name, "versatz_m": [dx, dy]}` ·
`{"auf_linie": name, "t": 0.3}` bzw. `{"auf_linie": name, "s_m": 12, "seite_m": 5}` (+ = links in Laufrichtung).

**Richtung** (`rspec`, Kompassgrad: 0 = Nord, 90 = Ost): Zahl · `"hangab"` · `"hangauf"` · `"zu:<ref>"` · `"von:<ref>"` ·
`{"basis": rspec, "plus": 90}` · Name einer Linie (deren Richtung Anfang → Ende) · benannte Richtung aus `anker`
(`{"richtung_von": rspec}`).

**Anker-Suchen** (`{"suche": ...}`, auf dem Bestandsgelände): `hoechster`/`tiefster`/`steilster`/`flachster` im `r_m` um `bei`
· `rinne` (größte Einzugsfläche im Ring `r_m: [a, b]`, optional `sektor: [g0, g1]`, ohne Bestandswasser) ·
`hangauf_bis` (von `bei` hangauf, bis `hoehe_m` über dem Start oder `max_m`).

**Linien** (`linien`): `{"punkte": [ref, ...]}` · `{"abwaerts_von": ref, "laenge_m": L}` (steilster Abstieg = Tiefenlinie,
z. B. Klammachse) · `{"quer": ref, "richtung": rspec, "laenge_m": L}`. Jede Linie erzeugt Anker `<name>_anfang`,
`<name>_ende` und die Richtung `<name>`. **Auto-Anker** eines Sees: `<see>_mitte`, `<see>_auslass`.

### 3.4 Gelände (`gelaende`)

```json
"gelaende": {"fenster_m": [140, 140], "rand_m": 10, "bei": "mitte",
             "ist_wasser": false, "ist_wasser_r_m": 45, "wasser_frei": false, "schutz": true,
             "begruendung": "nur wenn |Delta| > 40 m oder Bestandswasser geaendert wird",
             "ops": [{"op": "mulde", "bei": ref, "radius_m": 8, "tiefe_m": 2, "rand_m": 6, "boden": 0.4,
                      "streckung": [1.6, 1], "richtung": rspec, "modus": "add", "ziel_z": "boden-2"}, ...]}
```

| `op` | Felder |
|---|---|
| `mulde` | `radius_m`, `tiefe_m` (oder `ziel_z` = absolute Sohle), `boden` (Anteil flache Sohle), `streckung`, `richtung` |
| `kuppe` | `radius_m`, `hoehe_m`, `plateau`, `streckung`, `richtung` |
| `rinne` | `punkte` (Refs oder Linienname), `breite_m`, `tiefe_m` oder `sohle: [z0, z1]` (fallend, nur absenken) |
| `terrasse` | `radius_m`, `ziel_z` (`"boden"`, `"boden+1.5"`, Zahl, `"see:<id>+0.5"`), `streckung`, `richtung` |
| `abbruch` | `punkte` (Kante), `hoehe_m`, `breite_m` (steile Zone, ≥ 2 Zellen!), `reichweite_m`, `seite` links/rechts (wird höher), `verteilung` oben/unten/beide |
| `glaetten` | `radius_m`, `staerke` 0–1, `sigma_m` |
| `buckel` | `radius_m`, `amplitude_m`, `wellenlaenge_m` (Halde, Blockfeld) |

`modus` (Blending mit dem Bestand): `add` (relativ, Standard), `min` (nur absenken – Bestand bleibt, wo er tiefer ist),
`max` (nur anheben), `setzen` (Ziel beidseitig). Am Ende: Rand Δ = 0 mit weichem Übergang (≥ 8 m), keine Änderung
≤ 3 m an Wegen und am Bestandswasser – außer `ist_wasser: true` (der Ort IST dieses Wasser, im Radius
`ist_wasser_r_m`). |Δ| > 40 m ist erlaubt (Ferat 11.10.), braucht aber `begruendung`. Der Planer warnt bei geschlossenen
Senken ohne Wasser.
Gewollte Hohlformen ohne Wasser (Gaskrater, Schluckloch, Endpfanne) bekommen `"senke_begruendung": "<Grund>"` im
`gelaende`-Block – dann meldet der Planer die Senke nur als HINWEIS (Erweiterung, optional).

### 3.5 Wasser (`wasser`, §5)

```json
{"typ": "see", "id": "karsee", "bei": ref, "r_m": 5 | "becken": {"a_m": 17, "b_m": 11, "richtung": 60,
   "ufer_m": 6, "freibord_m": 0.5, "boden": 0.45, "auslass": "auto" | grad | null, "lippe_m": 1.5,
   "einpassen": {"r_such_m": 10, "schritt_m": 2, "richtungen": [0, 20, ...]}},
 "spiegel": "boden+0.2" | 258.5 | "see:<id>", "spiegel_rand_min": -0.1, "tiefe_m": 3.5, "farbe": "schwarz_spiegel"}
{"typ": "bach", "id": "abfluss", "abfluss_von": "<see>" | "von": ref | "punkte": [...], "bis_see": "<see>",
 "laenge_m": 50, "breite_m": 2, "tiefe_cm": 30, "farbe": "klar", "quelle": false, "muendung": "auto"|"versickert"|id,
 "rinne": {"tiefe_m": 0.4, "breite_m": 2}}
{"typ": "wasserfall", "id": "fall", "kante": [ref, ref], "becken": "<see>" | "fuss": ref, "breite_m": 3.5}
```

- Jeder `see` wird als Becken gestempelt: innen Sohle (nur absenken), außen ein Uferring rundum über dem Spiegel
  (nur anheben), im Abfluss nur eine schmale Lippe. `einpassen` sucht Mitte, Richtung und Spiegel mit dem kleinsten
  Erdbau. Der Umriss ist automatisch gegen den Uhrzeigersinn.
- `bach.abfluss_von` folgt vom Auslass dem steilsten Abstieg bis zum Bestandswasser; `muendung: auto` sucht die
  Bach-Kennung in `baeche_alle.json`. Der Wasserspiegel fällt stetig; Stufen > 0,8 m werden Fälle.
- Farben: `klar`, `tuerkis`, `tiefblau`, `smaragd`, `moorbraun`, `schwarz_spiegel`, `gletschermilch`, `thermal`, `rostrot`,
  `salzweiss`.

### 3.6 Gruppen (`gruppen`, §4) – das Herz des Rezepts

```json
{"name": "schuttkegel", "ebene": "schutt", "rolle": "fels", "warum": "Ursache in einem Satz",
 "netz": "SM_..." | "palette": ["SM_...", ...] | "<paletten-name>", "gewichte": [2, 1],
 "anzahl": 150 | [5, 8], "dichte_je_m2": 0.3,
 "verteilung": {"typ": "faecher", "bei": "mitte", "richtung": "hangab", "laenge_m": 42, "oeffnung_grad": 55, "t": [0, 1]},
 "abstand_m": 0.9, "meide": "massiv" | "kern" | null,
 "skala": [0.8, 1.2] | "groesse_m": [0.6, 1.2], "groesse_achse": "max"|"z"|"xy", "skala_xyz": [1, 1, 0.8],
 "skala_streuung": 0.1, "gradient": {"von": 0.7, "bis": 1.9},
 "ausrichtung": "normale"|"aufrecht"|"liegend"|"hochkant", "normale_anteil": 1.0, "hochkant_achse": "y"|"x",
 "yaw": "zufall" | rspec, "yaw_streuung_grad": 10, "front_achse": "+x"|"-x"|"+y"|"-y"|"+z"|"-z",
 "kipp_grad": [24, 32], "kipp_richtung": rspec,
 "eingraben": [0.3, 0.45] | "eingraben_m": [0.2, 0.4], "bezug": "min"|"mitte", "zentrieren": true,
 "z_bezug": "oberkante:<gruppe>" | "oben:<gruppe>" | "see:<id>" | "boden+6", "z_versatz_m": -0.4, "oberkante_ueber_m": 2,
 "im_wasser": "nein"|"erlaubt"|"nur"|"egal", "weg_abstand_m": 4, "hang_grad": [0, 35], "hoehe_rel_m": [-5, 5],
 "boden_min_m": -0.3,   # Mindest-Bodenhoehe (Meer); an Kueste/Prielen 0.0, damit Rundung kein 'im Meer' ausloest
 "akteur": true, "kollision": true, "sichtweite": [0, 45000], "schatten": true, "material": "MI_EL_SW_...",
 "mindestens": 10, "aktiv": true, "grund": "warum abgeschaltet"}
```

**Detail-Ebenen** (`ebene`, Witcher-Pflicht): `held` (1–3), `begleiter` (3–12), `schutt` (20–400), `kleinzeug`
(Hunderte–Tausende), `bewuchs`, `kontakt`, außerdem `wasser` (Steine im Bach) und `pfad`. Die Ebene setzt Standards für
Sichtweite, Schatten, Kollision und Ausdünn-Reihenfolge (Kleinzeug zuerst).

**Rollen** (`rolle`) steuern Eingraben und Ausrichtung: `fels` (25–45 % der Höhe, zur Normalen), `stein` (30–50 %),
`stamm` (20–35 %), `wurzel`, `baum` (0,15–0,4 m, fast aufrecht), `pflanze` (2–5 cm, 30 % zur Normalen), `streu`
(Moos, Zweige: 0–2 cm, zur Normalen). Standard-Akteur: `held` immer, `begleiter` ab 2,5 m; Kollision ab 0,8 m bei Fels,
Stein, Baum, Stamm, Wurzel.

**Verteilungen** (`verteilung.typ`):

| Typ | Felder | Wofür |
|---|---|---|
| `punkt`, `punkte` | `bei` bzw. `punkte: [ref, ...]` | Held, Insel, Kippblock |
| `kreis`, `ring` | `bei`, `r_m` (Zahl oder `[innen, außen]`) | Sockel, Ringe (Brandkreis → Jungwuchs) |
| `ellipse` | `bei`, `a_m`, `b_m`, `richtung` | Hain, Terrasse |
| `faecher` | `bei`, `richtung`, `laenge_m`, `start_m`, `oeffnung_grad`, `t: [a, b]` | Schuttkegel, Blockhalde; mit `gradient` nach unten gröber |
| `band` | `punkte` (Refs oder Linie), `breite_m`, `versatz_m`, `t` | Bachbett, Ufer, Pfadsaum |
| `rechteck` | `bei`, `laenge_m`, `breite_m`, `richtung` | Windwurf-Gasse |
| `reihe` | `punkte` (Linie), `abstand_m`, `versatz_m`, `seiten`, `blick: zur_linie`, `front_an_linie` | Klammwände, Uferkanten (Yaw kommt aus der Reihe) |
| `cluster` | `form` (kreis/ring/ellipse/…) + deren Felder, `zentren: [a, b]`, `je: [a, b]`, `radius_m` | Farnhorste, Blüteninseln, Pilzgruppen |
| `um_gruppe` | `gruppe` (Name/Liste), `ring: [0.9, 1.4]` (× Fuß-Ellipse) oder `ring_m: [a, b]` (m um den Pivot), `je`, `seite` (nord/ost/sued/west/Grad/hangab), `seite_staerke` | **Kontaktzonen**: Moos Nordseite, Schutt hangab, Kiessaum, Spaltenbewuchs |
| `auf_gruppe` | `gruppe`, `je`, `anteil: [a, b]` (entlang der langen Achse) | Kiefer auf dem Findling, Jungtannen auf dem Ammenstamm (mit `z_bezug: oben:<gruppe>`) |
| `ufer` | `bei`, `r_m`, `band_m: [a, b]` (Abstand zur Wasserkante, negativ = im Wasser) | Kies, Binsen, Nassband an Bestands- UND geplantem Wasser |
| `anker` | `praefix` (alle Anker `<praefix>*`, Richtungen gleichen Namens = Yaw) | von Hooks gesetzte Positionen |

**Ausrichtung**: `normale` (Z zur Hangnormalen, `normale_anteil`), `aufrecht`, `liegend` (lokale Z-Achse – der Stamm –
waagrecht in Richtung `yaw`, der Pivot liegt am Stammfuß → mit `zentrieren: false` den Stammfuß setzen), `hochkant`
(lokale Y- bzw. X-Achse nach oben: Klippenschale als Nadel, Wurzelteller senkrecht). **`skala_xyz` wirkt in den lokalen
Netzachsen** (wie in Unreal): bei `hochkant` mit Achse `y` ist `skala_xyz[1]` die neue Höhe.

**Höhe**: Standard = Unterseite eingegraben, kein Kontaktpunkt schwebt (`bezug: min`; Pflanzen/Bäume `mitte`). Die
Lib liest den Pivot aus `netze_masse.json` (sonst „unten Mitte“) und gräbt senkrecht zum Hang ein. `z_bezug` setzt
Stücke auf andere (`oben:<gruppe>` = Oberkante des nächsten Stücks der Gruppe, `oberkante:<gruppe>` = des ersten),
in den See (`see:<id>` + `oberkante_ueber_m`, Unterkante im Seegrund) oder verkeilt (`boden+6`); solche Stücke
werden als `z_frei` markiert und vom Prüfer nicht als „schwebt“ gezählt.

**Abstände**: `abstand_m` (untereinander), `meide: massiv` (Standard für Held/Begleiter/Schutt/Bewuchs: nicht in
andere massive Stücke; Kernradius = kurze Fuß-Halbachse, Bäume = Stamm), `kern` (Standard Kleinzeug/Kontakt: nur
nicht im Kern), `null` (bewusst überlappend: Wurzeln über dem Block, Wände in der Klamm). Wege: 4 m (große Stücke),
2,5 m (Kleinzeug); Orte, Meer (< −0,3 m) und Bestandswasser sind gesperrt (außer `im_wasser`).

### 3.7 Bodenlagen (`lagen`, §3)

`{"lage": "Kies", "form": "kreis"|"ring"|"band"|"um_gruppe"|"ufer"|"hang", "bei": ref, "r_m": 10 | [innen, außen],
"wert": 200, "rand_m": 3, "flecken": 0.4, "flecken_m": 6, "streckung": [...], "richtung": rspec}` –
`band` mit `punkte`/`breite_m`; `um_gruppe` mit `gruppe`/`ring`; `ufer` mit `band_m`; `hang` mit `hang_grad: [a, b]`.
Namen exakt wie FORMAT.md §2. Ferat setzt `neu = max(alt, ziel)`; die Lagen steuern auch das GPU-Gras.

### 3.8 Pfad (`pfad`, 13c)

`{"breite_cm": 120–200, "art": "auto", "lagen": {"Erde": 215, "Kies": 120}, "trittsteine": {"palette": ...,
"groesse_m": [0.7, 1.1], "abstand_m": 0.9, "stufen_ab_grad": 22, "stufen_palette": ..., "stufen_groesse_m": [1, 1.6],
"stufen_abstand_m": 3}}`. Quelle: zuerst ein Pfad aus `standorte.json["pfade"]`, dessen `fuer` den Ort nennt (oder
`pfad_id` des Orts), sonst der Fußweg `pfad_cm` des Orts (umgedreht: Weg → Ort). `art: auto` = `serpentine` ab 15 %
Steigung. In `orte.json` steht `"pfad": {"punkte_cm", "breite_cm", "art", ...}` – den Anschnitt rechnet Ferat.
Trittsteine kommen dorthin, wo der Pfad Wasser quert, Felsstufen dorthin, wo er **entlang** steiler als `stufen_ab_grad` ist.
Das Bodenband wird auf das Lagenfenster (≤ 400/600 m) gekappt; der Rest steht nur als `pfad` drin (HINWEIS). `"fenster_max_m": 400`
(optional) kappt das Lagenfenster eines Leuchtfeuers schon bei 400 m (sonst Prüfer-WARNUNG > 400 m).

Geteilte Pfade und Zugänge (Erweiterung, optional): `"abschnitt": "naechster"` nimmt von einem Pfad, den mehrere Orte nutzen
(`fuer`), nur den Abschnitt, der diesem Ort entlang der Bogenlänge am nächsten liegt (Grenzen in der Mitte zwischen den
Projektionen der Orte) – jeder Pfadmeter gehört genau einem Ort, Stufen entstehen nicht doppelt. Dafür übergibt der Planer
`OrtKontext(..., orte_mitten={id: (x_m, y_m)})`. `"zugang": true` (oder `{"breite_cm", "lagen", "trittsteine"}`) legt
zusätzlich den Fußweg `pfad_cm` des Orts (Pfad → Ort) als eigenes Bodenband mit Trittsteinen/Stufen an; in `orte.json` steht
er als `"pfad_zugang"` (gleiches Schema wie `pfad`). `trittsteine.stufen_bis_grad` begrenzt Felsstufen nach oben (steiler:
Kehren aus Ferats Serpentinen-Werkzeug).

Verzweigte Pfade (Erweiterung, optional): `"pfad_id": "<id>"` wählt genau diesen Pfad aus `pfade` (statt des ersten mit
`fuer`/`pfad_id`), `"abschnitt": [von_m, bis_m]` nimmt nur diesen Bogenabschnitt, `"abschnitte": [{"pfad_id", "von_m",
"bis_m"}, ...]` legt weitere Abschnitte (auch anderer Äste) als eigene Bänder mit Stufen an (`orte.json` →
`"pfad_abschnitte"`). So liegt ein verzweigter Pfad Meter für Meter in genau einem Lagenfenster (Beispiel: Ödlandpfad).

### 3.9 Effekte, Klänge, Freiräume

- `{"typ": "punktlicht"|"spotlicht", "bei", "hoehe_m", "intensitaet_cd", "radius_m", "farbe", "kompass", "neigung_grad",
  "kegel_grad", "schatten": false}` – ≤ 4 je Ort, dezent (feste Sonne).
- `{"typ": "lokaler_nebel", "bei", "hoehe_m", "radius_m", "dichte" 0,02–0,2, "farbe", "hoehenabfall"}` – ≤ 2 je Ort.
- `{"typ": "niagara", "asset": "<Name oder Pfad>", "optional": true, "wunsch_paket": "...", "hinweis": "...",
  "credits": "..."}` – ≤ 3 je Ort.
- `{"typ": "decal", "material": "MI_...", "anzahl", "verteilung", "groesse_m": [tief, b, h], "ausrichtung": "boden"|"wand",
  "blick": rspec}` – ≤ 12 je Ort; Material aus `inventar_extra.json["decal_materialien"]`.
  Eigene Decal-Textur (Ferat erlaubt, wenn der Katalog sie nennt): Materialwunsch `MI_EL_SW_<Name>` auf `M_MS_Decal`
  mit `"texturen": {"BaseColorTexture": "<png im Repo>", "NormalTexture": "<..._n.png>"}` (wird nach `orte.json`
  durchgereicht), Decal mit diesem Material, `"optional": true` (bis Ferat es anlegt) und `"textur"`/`"textur_normal"`.
- `klaenge`: `{"asset": "CUE_...", "bei", "radius_m", "lautstaerke", "zweck"}` – nur Naturklänge.
- `freiraeume`: `{"form": "kreis"|"rechteck", "bei", "r_m" | "laenge_m"/"breite_m"/"richtung", "ebenen", "rollen", "grund"}`
  → Hinweis an den Setzer, dort Bestand (Bäume, Sträucher) zu entfernen.

### 3.10 Erweiterungen aus den Koordinator-Entscheidungen (Auftrag 13, `13-entscheidungen-koordinator.md`)

- **Niagara-Kopien (E45):** `{"typ": "niagara", "asset": "NS_EL_SW_<Name>", "kopie_von": "<vorhandenes System>",
  "kopie_aenderungen": {...}, "optional": true}`. Die Lib schreibt `asset` als `/Game/Eldarien/Welt/FX/Sehens/NS_EL_SW_<Name>`
  und `kopie_von` als vollen Pfad des Originals (Original bleibt unberührt). Prüfer: Präfix `NS_EL_SW_` verlangt `kopie_von`
  (FEHLER), `kopie_von` muss im Inventar stehen (FEHLER, mit `optional` HINWEIS). Durchgereicht werden außerdem `bedingung`, `cull_m`.
- **Bestandsbach ersetzen (E10/E11/E39):** `"ersetzt_bestandsbach": {"id": "<Bach-Kennung>", "von": ref, "bis": ref,
  "grund": "..."}` an einem Wasser-Eintrag (`bach`/`see`/`wasserfall`) oder auf Ortsebene (dann mit `"ersetzt_durch"`).
  Die Lib projiziert von/bis auf den Bach aus `baeche_alle.json` und schreibt in `orte.json` je Ort
  `"bestand_ausblenden": [{"art": "bach", "id", "ersetzt_durch", "von_cm", "bis_cm", "von_s_m", "bis_s_m", "laenge_m",
  "bach_laenge_m", "abstand_m", "grund"}]` → Hinweis an den Setzer, diesen Abschnitt des Bestandsbachs auszublenden.
  WARNUNG, wenn der Bach unbekannt ist oder von/bis > 15 m neben dem Bach liegt.
- **Material-Fix-Ausnahmen (E34):** Benutzt ein Biom Eis-/Schnee-Megascans (`/Game/Fab/Megascans/3D/{Ice_Cliff_*,
  Large_Ice_Cliff_*, Snow_*, Rocky_Snow_Pile_*, Snowy_Rocks_Pile_*, Huge_Snow_Hill_*}`, 33 Netze), steht in `orte.json`
  oben `"material_fix_ausnahmen": {"grund", "netze": [...]}` – diese Netze behalten `M_MS_Base_Trm`.
- **Pivot/Front (E35):** Akteure tragen `pivot_z_anteil`, `pivot_xy_versatz_m`, `front_achse`, `front_quelle`
  (`netze_masse` | `regel` | `standard`) und, solange nicht gemessen, `annahme`. Ein `front_achse` in `netze_masse.json`
  hat Vorrang vor dem Wert in der Regel (heute hat noch kein Netz einen Messwert → Pläne unverändert).
- **Bedingungen/optional:** `effekte` (Decal, Niagara) und `klaenge` reichen `bedingung` durch (z. B. E13 „sobald das MI
  angelegt ist“, E18 „nur wenn das Laub leise ist“); `klaenge` reichen außerdem `optional`, `hinweis`, `ersatz`,
  `wunsch_paket` durch; `freiraeume` reichen `netze` (Netznamen-Muster, z. B. Houdini-Kacheln, E23) und `hinweis` durch.
- **Decal mit eigener MI fest einplanen (E13):** `{"typ": "decal", "material": "MI_EL_SW_<Name>", "optional": false,
  "bedingung": "MI wird angelegt"}` – steht das Material in den `materialwuenschen` des Bioms, meldet Planer/Prüfer nur
  HINWEIS (statt FEHLER „nicht in inventar_extra.json“).
- **Pfad-Warnung akzeptieren (E19):** Pfad in `standorte.json` mit `"warnung_akzeptiert": "<Begründung>"` → der Prüfer meldet
  „schneidet die geplante Stadt“ als HINWEIS.
- **Wassermaterial (E43):** `M_River_Water_Translucent` steht im Inventar nur als Name (Mountain-Set, `inventar.json`);
  ein voller Pfad ist nicht belegt → weiter `material_hinweis`. `inventar.wasser_material_pfad(name)` findet einen Pfad,
  sobald er in `inventar_extra.json["wasser_materialien"]` steht.

### 3.11 Korrekturen nach dem 1-m-Lauf (Auftrag 13f)

Alles additiv; alte Rezepte laufen weiter, bekommen aber das neue Verhalten der Bäche und Lagen.

- **Bäche (A4/A8/A9/A12/A13, Modul `bach.py`)** – jeder `bach` wird jetzt *gestempelt*:
  - Enden: Ein Bach mit `bis_see`/`muendung: <eigener See>` endet **auf dem Umriss** (Spiegel = Seespiegel + 2 cm),
    nie im See; erreicht der Lauf den See nicht, wird er gerade bis ans Ufer verlängert (HINWEIS). `abfluss_von`
    beginnt am Auslass **auf dem Seespiegel** und läuft zuerst radial vom See weg (kein Lauf am Ufer/Damm entlang).
  - Mündung: nur **Epic-Gewässer** (`baeche_alle.json`, `wasser_welt.json` Flüsse/Seen, `teiche.json`). `muendung:
    "auto"` sucht am Ende (halbe Breite + 6 m) und verlängert sonst entlang der Tiefenlinie (`verlaengern_m`, Standard
    40 m; D8 auf dem gefüllten Gelände). Ohne Ziel: `versickert` mit **mindestens 25 m**. Liegt ein Bestandsgewässer
    höher als der Bachanfang, ist es keine Mündung. Ein Bachende liegt nie unter dem Spiegel des Ziels (+ 2 cm).
    `"muendung": "<Epic-Id>"` (z. B. ein Bestandsbach aus `baeche_alle.json`): der Lauf wird entlang der Tiefenlinie
    verlängert und endet an der ersten Stelle dieses Gewässers, deren Spiegel er erreicht (Bachende nie darunter);
    sonst WARNUNG „nicht erreichbar“. Bleibt ein `versickert`-Lauf unter 25 m, wird er ab seinem bisherigen Ende ohne
    Kehre weiter verlängert (Gegenanstieg ≤ 0,5 m, nie neben dem eigenen Lauf); der Lauf davor bleibt Punkt für Punkt
    gleich (Stufen unverändert, Ferat 13g).
    `"muendung_houdini": "<Netz>"` (oder `true` = Name lokal zuordnen) – explizit in einen sichtbaren Houdini-Lauf.
  - Spiegel als **Treppe** (Regelwerk Auftrag 15, `gefaelle_regeln.json`): Becken ≤ 3 %, ≥ 3 m (`becken.laenge_min`,
    `stufen.abstand_L`), Stufen zwei Punkte (Lippe → Fuß 0,5 m). Keine Bündelung zu Fallketten (Ferat 13g: die Stufen
    bleiben wie 13f). In `orte.json` stehen sie explizit:
    `"stufen": [{"lippe_cm": [x, y, z], "fuss_cm": [x, y, z], "fall_m", "art": "schnelle|stufe|fall"}]`.
  - **Querprofil** (15b): Wasserkante innen, Bett = Spiegel − `tiefe_cm`, Böschung 35°, Ufer am Netzrand ≥ Spiegel
    + 5 cm (Uferring Spiegel + 0,2 … 0,5 m, hebt ≤ 2 m; die letzte Zelle innen an der Wasserkante wird bis zur
    Böschung aufgefüllt – die Reserve wirkt nur im Stempel, die Spiegelplanung rechnet wie 13f mit + 0,15 m / ≤ 1 m).
    Der Spiegel liegt 0,3 m unter dem Gelände (eingetieft); liegt eine Uferseite tiefer, sinkt der Spiegel bis 2 m
    tiefer. `"im_bestand_stempeln": true`: der Bach IST ein unbenanntes Bestandsgerinne – der Wasserschutz gilt in
    seinem Korridor (halbe Breite + 3 m) nicht. Fremde Seen samt Uferring werden nicht angeschnitten.
    `"profil": false` schaltet den Stempel für einen Bach ab (nur für Sonderfälle).
  - **Furt** (A13): Quert ein Bach die 3-m-Schutzzone eines Wegs/Orts, läuft er dort flach über den Boden
    (`"furten": [{"von_cm", "bis_cm"}]` im Eintrag); `"furt": {"palette", "groesse_m", "abstand_m"}` legt Trittsteine
    quer zum Bach (Ebene `pfad`).
  - Offene Mündung in Bestandswasser: im Mündungskorridor (letzte 8 m, halbe Breite + 1 m) gilt der Wasserschutz
    nicht (`muendung_offen_ab_cm`); das Gelände am Bestandswasser ändert sich dort höchstens **± 0,5 m**, weich
    auslaufend (2 m), nie in Weg-/Ortszonen (Koordinator 13f).
  - Neue Felder im Bach-Eintrag: `laenge_m`, `muendung_art` (`see_eigen|bach|fluss|see|teich|houdini|versickert`),
    `muendung_spiegel_cm`, `abfluss_von`, `stufen`, `furten`, `muendung_offen_ab_cm`.
  - **13i (Nachtest 1 m):** Das Querprofil senkt außerhalb der Wasserkante höchstens `tiefe + 0,5 m` ab, ab Netzrand +
    Uferring weich auf 0, zu den Linienenden hin auslaufend (K1; Kontrolle `profil_absenkung_aussen`, FEHLER bei
    Absenkung > 0,3 m abseits des Bachs). Es gibt dafür **eine** Funktion, `bach.absenk_grenze`, angewandt in
    `stempel.bach_profil`; Bezug ist das Gelände vor allen Bächen (`min(aktuell, h0 + Δ vor den Bächen)`), so dass
    kreuzende oder parallele Bäche einander nicht vertiefen. Die frühere 13h-Nachbegrenzung
    (`steilwand.bach_einschnitt_begrenzen`) ist entfallen. Der Stufenfuß liegt 0,5 m hinter der Lippe (Becken ab dem Fuß ≥ 3 m); die
    Schluss-Stufe am See geht in der letzten Stufe auf, wenn davor < 3 m Becken blieben (K5). Unerreichbare
    Epic-Mündung → automatisch weiter, ein Abfluss nie über dem Seespiegel (K4). Furtstrecken > 15 % Gefälle werden
    `"art": "durchlass"` (Wasser unter dem Weg, kein Wasserfilm; K9). Seeufer: 1 m hinter dem Umriss ≥ Spiegel
    + 0,1 m (K8, Prüfer misst dort alle 0,5 m).
  - **13g – `wasser_koerper`** (nur Datenformat): Bäche mit einer Stufe ≥ 0,5 m bekommen zusätzlich
    `wasser_koerper_lauf` (`SW_<ortid>_<bachid>`) und `wasser_koerper` im A15/14b-Format: `river` (≥ 15 m außerhalb der
    Stufenstrecken) und `kaskadennetz` je zusammenhängender Stufenstrecke (`mittellinie` [x, y, z, breite, tempo,
    fallanteil, schaum, abstand_bett], `knick`, `rand_ueberstand_m`, `vorhang_an_stufen`, 0,5 m Überlappung, Netz 2 cm
    unter dem River; River < 15 m als Rampe im Netz). Gebaut mit `gefaelle_plan.bauen_wasser_A` (nur importiert) aus den
    vorhandenen `stufen` und dem Spiegel – keine neue Planung. Netzbreite = Wasserbreite im Gelände (mind. Bachbreite).
    Effekte im Netz (`effekte`): `NS_Impact_Small` (Cull 20 m) am Fuß jeder Stufe ≥ 1 m, größte zuerst, höchstens 8
    Niagara je Ort samt Rezept-Niagara; Vorhang nur an einem Einzelabsturz ≥ 3 m. Prüfer: Netzregeln aus
    `gefaelle_pruefen.pruefe_wasser` + Bett (tiefster Punkt ≥ min(0,2 m; halbe `tiefe_cm`)) und Ufer am Netzrand
    ≥ Spiegel + 0,1 m.
- **Seen**: `tiefe_m` = größte Tiefe nach dem Stempel (`tiefe_regel_m` = Rezept, falls abweichend). Seen < 10 m²
  (A13) werden **Lage/Decal** statt Epic-See: `"klein": {"lage": "Schlamm", "wert": 230, "decal": "MI_…"}`
  (Standard Lage Schlamm, kein Becken). Seeufer unter dem Spiegel ist jetzt FEHLER (Zu-/Abflüsse ausgenommen).
- **Houdini-Wasser ausblenden** (B): `"houdini_ausblenden": [{"netz": "R_M2_P0__WASSER", "see": "<id>",
  "puffer_m": 2} | {"netz", "bach": "<id>", "breite_m": 8} | {"netz", "bei", "r_m"}]` → `orte.json`
  `bestand_ausblenden: [{"art": "houdini", "netz", "umriss_cm", "flaeche_m2", "ersetzt_durch", "grund"}]`.
- **Gelände**: Schutzzone 3 m um Wege **und Orte** hart 0 (gemessen bis zum Zellrand), Übergang erst außerhalb;
  `ist_wasser` hebt nur den Wasserschutz auf. Kleine Senken (< 50 m², < 0,5 m, vom Stempel erzeugt) werden in
  `fertig()` aufgefüllt (A5); `"senken_fuellen": {"max_flaeche_m2", "max_tiefe_m"}` erlaubt größere,
  `false` schaltet ab; gewollte Hohlformen weiter mit `senke_begruendung`.
- **Bäume** (A3): `bezug: mitte` mit Fußradius ≥ 1,5 m steht auf dem Boden am Pivot:
  `z = Boden(Pivot) − eingraben − max(0, bmin_z·sz)`.
- **Wand-/Hängepflanzen** (A6): `"z_frei": true` an der Gruppe (Efeu, Lianen, Luftwurzeln). `plan.json` führt
  `z_frei_index`; der Prüfer zählt diese Stücke weder als „schwebt“ noch als „im Meer“.
- **Materialwünsche** (A7): zusätzlich biomweit oben in `orte.json` als `"materialwuensche_biom"`.
- **Lagen** (13i K6/K7): Jede Zelle mit |Δ| > 0,3 m bekommt eine Bodenlage (Rezeptlage, sonst an steilen Stellen Fels
  des Bioms – Lavafels, Sandstein, Fels –, flach Geröll bzw. Sand/Lavasand/Schlamm/Erde); der Prüfer meldet Zellen ohne
  Lage als FEHLER. Alle Lagen werden vor dem Schreiben auf höchstens 150 je 1-m-Nachbarzelle geglättet (nur nach außen
  ergänzt, auch bei „fleckig“ und kleinen Ringen).
- **Akteur-Budget** (13j): Netze, die in einem Ort ≥ 12-mal als Akteur stehen (Wandmodule, 13h-Verkleidung), werden
  Instanzen der Ebene `sw_<biom>` mit Kollision; Richtwert ≤ 50 Akteure je Ort (Prüfer-HINWEIS). Gruppenfeld
  `"akteur_fest": true` hält wiederholte Heldenstücke als Akteure. Kaskadennetze tragen das 15f-Querprofil `quer`
  (gerade Lippen). `dz_cm` folgt der A15-Konvention (15f-Nachtrag `099f902`): relativ zu `z_cm` des eigenen Punkts,
  die absolute Wasserhöhe `z + dz` ist bei gleichem `s` gleich; der Prüfer übernimmt die A15-Regel aus
  `gefaelle_pruefen.pruefe_wasser` (Import). Liegt ein 13f-Fuß näher als `bogen_x_m` + 5 cm an der Lippe
  (Schluss-Stufe am Laufende), setzt nur das Netz seinen Fußpunkt dorthin; die Stufe selbst bleibt.
  Verkleidung: `"gelaende": {"verkleiden": {"budget_nach_buendeln": true}}` zählt beim Akteur-Budget nur die Akteure,
  die nach dem Bündeln Akteure bleiben (opt-in, z. B. gletscher_06).
- **Instanzen** (13i K2/K3): `bezug: mitte` mit Pivot in der Netzmitte (bmin_z·sz < −0,25 · Höhe) → Netz-Unterkante auf
  den Boden; Stücke bis 1 cm an einer Feldgrenze rücken 1 cm ins Feld, das Feld kommt aus dem float32-Wert.
- **Lagen** (A11): Ränder ≥ 3 m weich (auch innen bei `ring`/`um_gruppe`/`ufer`); Pfad-Bodenband mit 1 m Übergang
  beidseits und 10 m vor dem Lagenfenster ausgeblendet; alle Lagen laufen am Fensterrand auf 3 m aus.
- **Feldzuordnung** (A10): `s = floor((x_cm + 473050)/100800)`, `r = floor((y_cm + 406050)/100800) + 1` –
  wie Setzer und Landschaftskomponenten (`daten.feld_von_m`, `feld_grenzen_m`, Prüfer).

### 3.12 Steilflächen, Kameras, Leuchtfeuer, Blöcke im See (Auftrag 13h)

Hintergrund ist der Bildbefund des ersten Editor-Pilots: senkrechte, glatte Erdwände, `_nah` in einer Krone,
Leuchtfeuer aus `_fern` nicht lesbar und grüne Streifen von Blöcken knapp unter dem Seespiegel. Alles ist additiv;
alte Rezepte laufen weiter und bekommen das neue Verhalten automatisch.

**Prüfer-Regeln (FEHLER):**
- **Steilflächen:** > 20 m² zusammenhängend mit > 45°, die der Stempel neu geschaffen hat (|Δ| > 0,25 m, mehr als 5°
  steiler als vorher), ohne Fels-Akteur, der die Zellen deckt.
  - „Deckt“ heißt: in der XY-Hülle der gedrehten Bounds und mit der Bodenhöhe zwischen Unter- und Oberkante ± 1 m.
  - Ausgenommen sind Seegrund, Meeresboden und das benetzte Bachbett.
  - Modul: `steilwand.py`.
- **Kameras** (`kamera_frei.py`):
  - nicht im geplanten Wasser und nicht in einem Netz;
  - Abstand zu jedem neuen Baum ≥ Kronenradius + 2 m;
  - freier Strahl gegen neue Netze, Bestandskronen (4 m, ohne Freiräume) und Gelände nach dem Stempel.
- **Leuchtfeuer:** `_fern` muss die Silhouette zeigen. Die Held-Netze müssen ≥ 30 % und ≥ 10 m (oder ganz) über der
  Mindesthöhe liegen; ersatzweise die Ort-Silhouette aus Phase 1 zu ≥ 30 %. Lebende Held-Bäume müssen ≥ 1,5 × so hoch sein
  wie der Bestand (90-%-Wert im Ring bis 35 m, ohne Freiräume). Info: Silhouette vor dem Himmel ja/nein.
- **Blöcke im See** (`see_bloecke.py`): Stücke ≥ 0,5 m (keine Pflanzen) liegen mit der Oberkante ≥ Spiegel + 0,3 m oder
  ≤ Spiegel − 1,5 m. Gruppen mit `"teilweise_ueberflutet": true` sind ausgenommen und stehen in `orte.json` unter
  `teilweise_ueberflutet`.

**Gelände-Block, neue Felder:**

| Feld | Standard | Wirkung |
|---|---|---|
| `max_neigung_grad` | 38 | Böschung nach `fertig()`: Halde am Fuß aufschütten (`max_auftrag_m` 3), dann Kante abtragen (`max_abtrag_m` 3), linear auslaufend, nur wo der Bestand flacher als die Grenze ist. Keine neuen Senken. `false` schaltet aus. |
| `halde` | Lage + Blöcke aus `gefaelle_regeln.json` → `biome.<biom>` | `{"lage", "wert", "bloecke": palette \| false, "dichte_je_m2", "groesse_m"}`; `false` = keine Halde-Lage und keine Blöcke |
| `steil_erlaubt` | – | `[{"bei", "r_m"} \| {"punkte", "breite_m"}]`: gewollte Wand. Die Böschung lässt sie stehen, die Verkleidung muss sie decken. |
| `verkleiden` | an, Wandnetze des Bioms (A15) | `{"palette", "groesse_m", "groesse_achse", "max_anzahl"}` für die automatische Gruppe `wandverkleidung`; `false` = aus. Akteur-Budget: höchstens 78 Akteure je Ort. |
| `rauschen` | – | `{"anteil": 0.25, "wellenlaenge_m": 18}`: organischer Rand für mulde, kuppe, terrasse, rinne, abbruch und damm (auch je `op`). Gilt nicht für Seebecken und Bäche. |

**Weitere Felder:**
- **Gruppen:** `"verteilung": {"typ": "steilwand", "bei", "r_m", "max_anzahl", "versatz_m"}` verkleidet neue
  Steilflächen. Gierig von unten nach oben; die Front zeigt talwärts (`front_achse` je Netz), die Vorderkante liegt auf
  der Wandzelle (wie `front_an_linie`); hohe Wände werden gestapelt (`z_frei`). `"verteilung": {"typ": "halde"}` legt
  Stücke auf die Halde. Gruppen-Flag `"teilweise_ueberflutet": true` (siehe oben).
- **See-Becken:** `"insel": {"versatz_m", "r_m", "ueber_m", "plateau"}` legt eine Geländekuppe ins Becken, die Krone liegt
  `ueber_m` über dem Spiegel (Anker `<see>_insel`).
- **Kameras** (`"kameras"` im Rezept):
  - `{"<art>": {"pos", "ziel" | "ziel_gruppe" + "ziel_richtung", "ziel_hoehe_m", "abstand_m", "richtung", "hoch",
    "grund"}, "fern": {"suche": "wegpunkte"}, "versetzen": true, "standplatz_freiraeumen": true}`.
  - Ohne Regel prüft der Planer alle Kameras und versetzt blockierte selbst: Ring um das Ziel nahe der alten Position,
    dann weiter gefasst. `_fern` bei Leuchtfeuern sucht er an Weg- und Pfadpunkten in 300–800 m, Himmel bevorzugt.
  - Ziele unter dem Boden hebt er an.
  - Eigene Pflanzen am Standplatz räumt er frei.
  - `orte.json` trägt dann `kameras_13h`.

## 4. Bausteine der Bibliothek (für Hooks und Sonderfälle)

```python
from sehens_lib import daten, gelaende, inventar, instanzen, rezept, stempel, vorschau, sehens_pruefen
ctx.anker["name"] = (x, y); ctx.richtungen["name"] = grad       # Anker/Richtungen setzen
ctx.r["gelaende"]["ops"].append({...}); ctx.r["wasser"].append({...})   # im Hook "anker": Rezept erweitern
ctx.boden(x, y), ctx.stempel.normale_bei_m(x, y), ctx.stempel.hang_grad_bei_m(x, y)   # Boden nach Stempel
ctx.im_wasser(x, y), ctx.wasser_abstand(x, y), ctx.welt, ctx.gel (Ganze-Welt-Raster mit Cache)
ctx.gruppe({...Gruppen-dict...})                                 # eine Gruppe jederzeit nachsetzen
stempel.Stempel / Lagen  (mulde, kuppe, rinne, terrasse, abbruch, glaetten, buckel, see_becken / kreis, band, maske)
instanzen.orientierung(...), instanzen.platziere(...), instanzen.streue/cluster/um_stuecke, instanzen.Ebene
inventar.Inventar.lade().netz(name), .asset_pruefen(art, pfad, optional), .material_pruefen(mw)
```

Beispiel: `hook_windwurf_anker` im Bergwald-Planer setzt die Stammfüße einer Sturmgasse, die Wurzelteller und
-löcher und hängt Mulden und Pfützen-Seen an das Rezept an – danach erledigen Regeln den Rest.

## 5. Umgang mit fehlenden Assets

- **Nie Namen erfinden.** Jedes Netz muss in `vorlagen/daten/netze.csv` stehen, jedes Niagara-System/Decal in
  `inventar_extra.json`. Prüft Namen vorher (`inventar.Inventar.lade().netz_pruefen(name)`). Mehrdeutige Namen
  (gleicher Name in zwei Paketen) → vollen Pfad angeben. Gesperrte Netze (`netz_sperre.json`) und Houdini `SW_*` → FEHLER.
- **Paket fehlt noch** (Download-Liste, z. B. Nature Water FX, Forest Fungi): Ersatz aus dem Bestand bauen und in
  `assets_wunsch` `{"paket": "<Name wie downloadliste.json>", "statt_jetzt": "<Ersatz>"}` eintragen.
- **Effekt fehlt**: `niagara` mit einem vorhandenen Ersatz-System (`asset`) und `"optional": true`,
  `"wunsch_paket"`, `"hinweis"`; fehlt auch der Ersatz, das Asset trotzdem nicht erfinden, sondern den Effekt weglassen
  und `lokaler_nebel` nehmen. Der Prüfer meldet ein fehlendes Asset als FEHLER, mit `optional` als HINWEIS.
- **Instanzen können nicht optional sein**: Netze, die erst kommen, gar nicht setzen; Gruppen, über die Ferat noch
  entscheidet (Tiere: offene Frage 8), mit `"aktiv": false, "grund": "..."` im Rezept lassen.
- **Klänge**: `inventar_extra.json` listet nur Beispiele (40 von 316 Waves, 40 von 46 Cues). Fehlt ein Klang dort,
  meldet der Prüfer WARNUNG statt FEHLER. Stadt-/Menschenklänge (Crowd, City, Fireworks …) sind verboten.
- **Material-Instanzen** statt neuer Netze: Tönung, Nässe, Moos-/Schnee-Auflage, Wind aus (`M_EL_Pflanze` `Wind_Staerke`
  0 für liegende Bäume) – ≤ 6 je Biom, nur vorhandene Parameter.
- **Pivot/Front unbekannt** (E35, siehe 3.10): Netze ohne Eintrag in `netze_masse.json` gelten als „Pivot unten Mitte“
  (`"pivot": "angenommen_unten_mitte"` im Akteur). Welche Seite einer Schale die Schauseite ist (`front_achse`), steht in
  keiner Datei – Annahme im Rezept dokumentieren (`hinweis`), das Editorbild entscheidet.

## 6. Witcher-Qualität im Rezept

- Jede Gruppe braucht eine **Ursache** (`warum`): Abbruchkante → Schuttkegel hangab, unten gröber (`faecher` +
  `gradient`); Wasser → Feuchtering (`ufer`); Wind → Windflüchter auf der Leeseite; Brand → Ringe aus Asche, Pionieren,
  Wald.
- **Größenstufen** vollständig: Held (1–3) → Begleiter (3–12) → Schutt (20–400) → Kleinzeug (Hunderte bis Tausende).
  Der Planer meldet fehlende Stufen als HINWEIS; `orte.json["detail_ebenen"]` zählt sie.
- **Kontaktzone** immer: `um_gruppe` mit Moos (`seite: nord`), Kiessaum, Spaltenbewuchs, dazu Lagen `um_gruppe`;
  Felsen 25–45 % eingegraben (Standard), nichts „steht auf“.
- **Wasser** klar mit Steinen im Wasser (`im_wasser: nur`), Kies am Ufer (`ufer` mit `band_m: [-0.8, 2.5]`).
- **Licht und Luft** dezent: ein `lokaler_nebel` in Senken, ein schwacher Spot als Lichtschacht.

## 7. Prüfschritte

1. `python -I .../sehens_lib/selbsttest.py --aus <scratchpad>` – Bibliothek ok (0 FEHLER).
2. Planer auf 2 m: `--daten2m recherche/vorlagen/daten/sehens --aus <scratchpad>/a13/p2/<biom> --bild` – Planer-Log:
   `Planer: 0 FEHLER` und der eingebaute Prüfer `Pruefung orte.json + sw_<biom>: 0 FEHLER`. Warnungen lesen und beheben
   oder im README begründen.
3. Prüfer einzeln: `python -I .../sehens_lib/sehens_pruefen.py --daten2m recherche/vorlagen/daten/sehens --datei
   <aus>/orte.json` (findet `<aus>/sw_<biom>` selbst, sonst `--ebene`).
4. Determinismus: zweimal in zwei Ordner laufen lassen, `diff -r` (ohne Bilder) muss leer sein. Laufzeit ≤ 3 min je Biom.
5. Testbilder `test_<id>.png` ansehen: Held am richtigen Platz? Kontaktzonen sichtbar? Schutt hangab? Wasser mit Ufer?
   Kameras auf das Ziel? Dann `--bild --bild-ordner recherche/antworten/sehens/<biom>`.
6. Budget je Ort (§9) und je Feld (zusammen mit allen Ebenen ≤ 60 000) im Log prüfen.
7. Ins Repo nur Skript, Regeln, README, Testbilder; Ausgabe bleibt im Scratchpad. Standorte und Kataloge **nicht
   ändern** – Korrekturbedarf im Bericht melden.

## 8. Fallstricke (aus dem Bergwald gelernt)

- `skala_xyz` gilt in **lokalen** Netzachsen – bei `hochkant` ist die Höhe `skala_xyz[1]` (Achse y) bzw. `[0]` (Achse x).
- 2-m-Daten: Werkzeugkanten (`abbruch.breite_m`, Seelippen) mindestens 2 Zellen = 4–5 m breit, sonst verwischt die
  Interpolation sie. Lokal auf 1 m wird es schärfer.
- Seen auf Hängen brauchen einen Damm; `einpassen` + `auslass: auto` halten den Erdbau klein. Liegt Bestandswasser im
  See, `gelaende.ist_wasser: true`.
- Lange Stücke (Wände, Stämme) als `meide: null` setzen und Kontaktzonen mit `ring` (Fuß-Ellipse) statt `ring_m`.
- Reihen (`reihe`) mit `front_an_linie: true`, sonst ragt die Wandmitte in die Klamm.
- Liegende Foliage-Bäume: `ausrichtung: liegend`, `zentrieren: false`, Material mit `Wind_Staerke` 0.
- Kleinzeug großzügig (Hunderte bis Tausende) – es kostet wenig, und das Budget dünnt automatisch aus.
- Die Regeldatei ist JSON: keine Kommentare, Gründe in `warum`/`hinweis`/`_doku`.
- 13f: Ein Bach muss ganz im Geländefenster liegen (sonst gekappt, Mündung → `versickert`) – `fenster_m` groß genug
  wählen. Ketten von Töpfen mit `abfluss_von` + `bis_see` verbinden, nicht mit `von: "<see>_auslass"`.
- 13f: Bäche nicht als `punkte` auf einen Grat oder an eine Abbruchkante legen – das Profil kann eine Uferseite nur
  ≤ 2 m anheben; der Prüfer meldet „Ufer unter dem Spiegel“.
