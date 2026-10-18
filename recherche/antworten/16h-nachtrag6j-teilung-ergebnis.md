# Antwort 16h Nachtrag 6j – Teilungsbefund gedeutet (Lippenschatten), Variante A verworfen, Stencil-Messdesign, Rinnsal sichtbar machen

Gelesen: recherche/auftraege/16h-nachtrag6j-teilung-ergebnis.md @ a49de2d42844b7e0b1488209f1a0dccc872f2d44 (Commit 8749f1c)

Stand 18.10.2026. Bezug, ebenfalls gelesen:
- `recherche/auftraege/16h-nachtrag6i-baked-sim-tests-stand.md` @ 11c254f0c95defaa25c481ed4047bf7c68625309 (Commit 999ddfe), nur §1–§3
- `recherche/auftraege/daten/swr_teilung_plan_lokal.md` @ 5e2b390570e1507babdccc05de5e055085f79863 (Commit 999ddfe)
- Planbasis der Rechnung in §1.1: `recherche/antworten/p2_bett/bettplan_p2.json` @ 0013ef4a1922330462308bc7dbad8729ae6a1ef3,
  `talkaskade_soll.f32` @ b6f4e2a48fe045ac9e7fdcbb4846ede85cd9153b, `talkaskade_zonen.u8` @ 8d006acdc26852775efc75583baab32f0cfea422
- Messregeln: `recherche/vorlagen/pruefung.md` @ 5daf4a9187ba35288dc4838f9461118e0960d068 (Commit eeedefb)

Die Frage zum Betrieb von BAKED_SIM (6i) beantworte ich hier nicht; dafür gibt es eine getrennte Antwort.

**Kennzeichnung:** [Ferat] eure Messung · [Rechnung] von mir aus den Plandateien gerechnet, das Skript steht in §1.1 · [Projekt] Regel
oder Befund im Repo · [Suchauszug] nur Suchauszug; Epic-Doku, Epic-Forum, Issue-Tracker und Archiv waren aus der Cloud nicht abrufbar
(DNS bzw. Proxy 403, 18.10.) · [Ableitung] geschlossen, nicht belegt · [zu prüfen] API-Name oder CVar nicht belegt, vor Gebrauch im Editor
abfragen · **anzulegen** = Asset gibt es noch nicht.

## Kurzfazit

1. **§1 (a) – 25 % bei 9 cm sind nicht die Grenze der Simulation.** Den tiefen Teil erklärt am besten das Nachfüllen auf die
   **eindimensionale Spline-Höhe** neben schrägen Lippen. Diese Zone nenne ich hier **„Lippenschatten“** (Definition in §1.1).
   Status: **wartet auf Beleg T6j-A** (Auswertung vorhandener Dumps, ohne Editor). Ob die Zellen dort sonst trocken wären, zeigt **T6j-B**.
   - **Rechnung aus dem Plan:** Wird jede Bandzelle bis zur Spline-Höhe gefüllt, sind bei > 10 cm **12,8 %** des Bands nass.
     T01 misst **13,1 %** [Ferat].
   - Wasser auf dem Plan-Spiegel plus eine plausible Überfallhöhe von 0,2 m ergäbe nur 1,9 %.
   - Die Differenz bei 1–2 cm (29,8 bzw. 25,9 % gegen 13,6 %) sind dünne Filme.
   - **Folge für den Hebel:** Der Boden-Trick in der 6g-Form (Schulter + 0,1 m) hilft im Lippenschatten kaum (13,6 → 12,5 %).
   - Nächster Hebel ist ein **schmales Spline-Band nur in der Talkaskade** (T6j-C), ohne Teilung und am ganzen SWR.
2. **§1 (b) – Variante A: verworfen**, ohne Test, aus Gründen der Bauweise.
   - Die ganze SWR rechnet und zeichnet die Talkaskade weiter, samt ihrem 78,6-%-Band, denn ihre Rechenfläche hängt an den
     Quell-Wasserkörpern (6i §3).
   - Eine zweite SWR darüber kann dieses Wasser nicht wegnehmen. Im WCBS-Weg zeichnet je Kachel nur eine Wasserkomponente (Forum,
     trockene Streifen bzw. fehlendes Netz).
   - Wieder öffnen nur mit neuer Evidenz: eine Eigenschaft, die einen Bereich aus der Rechnung oder dem Zeichnen einer SWR ausnimmt.
3. **§1 (c) – keine der beiden Quellen ist brauchbar: verworfen.**
   - Die Kopie mit Einlauf aus dem Nichts hat einen Abfluss, den ihre eigene Quelle und das Nachfüllen bestimmen, nicht der Oberlauf.
   - Den ganzen Fluss als `source_river_water_bodies` einzutragen, vergrößert die Rechenfläche wieder auf das 740-m-Rechteck
     (6i §3). Eine SWR selbst kann man dort nicht eintragen, nur `WaterBodyRiver`.
4. **§4.2 – Pixelmessung: beantwortet (Messdesign).** Der Werkzeugumbau wartet auf die Kontrollfälle KF1–KF7.
   - Gemessen wird im **Hauptbild statt in der SceneCapture**: Post-Process-Material mit Klassenfarben, `HighResShot`, Zählung offline.
   - Pflicht ist die **Verdeckungsregel CustomDepth ≈ SceneDepth**. Die CustomDepth-Schicht ignoriert Verdeckung durch Objekte ohne
     CustomDepth. Das ist ein naheliegender Grund für K1 = 100 %.
   - Gras hat laut Suche keine CustomDepth-Option. Es wird deshalb als „unklassifiziert“ gezählt und per Differenzbild getrennt.
   - Nanite schreibt CustomDepth/Stencil laut Presse zu 5.2. Für 5.6 gibt es aber eine Gegenmeldung, also entscheidet KF3 lokal.
5. **Nachtrag – Rinnsal: beantwortet.**
   - **Nicht** 0,8 m Mindestbreite: Sichtbar wird das Rinnsal nicht durch Breite, sondern weil das Gras an seinem Rand **niedriger**
     wird. Eine 0,4-m-Grashöhe verdeckt aus 10 m Abstand einen 2,4 m breiten Streifen.
   - Vorschlag **„Rinnenkopf“**: die ersten 10–15 m mit niedrigem, nassem Saum, nasser Rinne aus Lage und Decal und 3–6 Kieseln.
     Die SWR bleibt bei 0,4 m.
   - Rückfall: 0,6 m wie bei der Felsquelle, nur wenn das Wasser danach kantig wirkt.
6. **B5 – quittiert.** Die Regel „Fab Raw nur mit MI_EL-Überschreibung“ ist richtig.
   - **Felsdeckung 176 % ist keine Deckung**, sondern die Summe der Fußflächen (wie RA2 378 %).
   - Bitte die Vereinigung (≤ 100 %) wie in 21 §(a) melden, sonst ist sie nicht mit den 79/61/83 % des Prüfers vergleichbar.

---

## 1. Uferstufe nach dem Teilungsbefund

### 1.1 (a) Grenze der Simulation oder Nachfüll-Artefakt?

**Was die Zahlen hergeben** [Ferat]:

| Lauf | Zelle | Band > 1 / 2 / 5 / 10 cm | Gefälle über die Schwellen |
|---|---|---|---|
| ganze SWR | 36,7 cm | 83,0 / 78,6 / 65,1 / 45,9 % | flach: tiefes Wasser neben dem Bett |
| T01 | 8,7 cm | 29,8 / 25,9 / 19,4 / 13,1 % | steiler, aber 13 % bleiben über 10 cm |

Die feine Zelle wirkt stark, belegt ist das: Bei > 10 cm sinkt das Band von 45,9 auf 13,1 %. Entscheidend ist der Rest bei > 10 cm.
Dafür habe ich drei Annahmen über die Höhe des Wasserspiegels gegen den Plan gerechnet.

**Rechnung** [Rechnung, Skript unten]:
- **Grundlage:** Bettplan 6c/6f, Rasterzellen 0,5 × 0,25 m, Spline aus den 237 `spline_stufenpunkte` (linear).
- **Boden:** Untergrenze `z_min` = Spiegel + Uferstufe in Uferstufe und Schulter (Zonen 5/6, 73 % des Bands).
- **Böschung:** Zone 7 (27 % des Bands, ohne `z_min`) ist als trocken angenommen.
- **Band:** 0,25–2 m hinter der Kante wie `pruefband`.

| Annahme für den Wasserspiegel | Band nass > 1 / 2 / 5 / 10 cm |
|---|---|
| **H1: Spline-Höhe (u = 0) quer über das ganze Band** (Nachfüllen füllt bis dorthin) | **13,7 / 13,6 / 13,4 / 12,8 %** |
| H1 + 5 cm | 14,7 / 14,4 / 13,8 / 13,4 % |
| H2: Plan-Spiegel je Zelle + 0,10 m (Überfallhöhe) | 1,5 / 1,2 / 0,6 / 0,0 % |
| H2: Plan-Spiegel + 0,20 m | 5,5 / 5,2 / 3,8 / 1,9 % |
| H2: Plan-Spiegel + 0,25 m | 11,3 / 10,7 / 5,9 / 3,8 % |
| **gemessen T01** [Ferat] | **29,8 / 25,9 / 19,4 / 13,1 %** |

**Lesart** [Ableitung]:
- **Der tiefe Teil (> 10 cm) passt nur zu H1.**
  - H1 sagt 12,8 % vorher, gemessen sind 13,1 %.
  - H2 bräuchte über 0,3 m Überhöhung, um 13 % bei > 10 cm zu erreichen. Dann müsste aber auch das Band bei > 2 cm bei etwa 30 % liegen
    und flach über die Schwellen verlaufen.
  - Bei H1 sind die nassen Zellen zu **100 %** Zellen, in denen die Spline mehr als 5 cm über dem örtlichen Plan-Spiegel liegt.
    Das ist der **Lippenschatten**: das Ufer neben dem unteren Becken einer schrägen Lippe. Die Spline steht an diesem s noch auf dem
    oberen Spiegel (Lippenwinkel im Plan 6,7 / 21,6 / 32° = min / Median / max, Seitenwechsel 76 %).
  - Der Lippenschatten deckt **16,6 % des Bands**. Die Spline liegt dort im Median 0,55 m über dem Boden, im p90 1,17 m.
- **Der flache Teil (1–5 cm) kommt dazu:** etwa 12 Prozentpunkte. Das sind dünne Filme auf der Schulter (Gitter, Zahlenwerte).
  Gegen sie helfen Kantengras und Ufersteine (6g §3).
- **Darum ist „Grenze der Simulation“ die falsche Schublade.**
  - Die Simulation macht, was das Nachfüllen verlangt: Jede Zelle innerhalb der Spline-Breite wird bis zur Spline-Höhe aufgefüllt.
    Die Spline kennt quer nur eine Höhe.
  - Laut Epic-Leitfaden (in 16f lokal gelesen) füllt die Rate dort nach, wo die Simulation unter der Spline-Höhe liegt.
  - Dass dies auf die Spline-Breite begrenzt ist, schließe ich aus dem Gegenstück „Remove Water Outside Spline“ [Ableitung].
  - Euer Verdacht „Nachfüllen 0,3 auch im feinen Teil“ trifft also den Mechanismus. Der Grund liegt aber nicht im Reset an sich,
    sondern in der Kombination aus Nachfüllen und eindimensionaler Spline-Höhe.
- **Vorbehalte:**
  - Der Boden ist eine Plan-Untergrenze. Das eingebaute Gelände kann höher liegen, dann wären die Vorhersagen Obergrenzen.
  - Ob die T01-Spline genau die Stufenpunkte trägt, prüft 6f: Spline-Z an den Lippen ±3 cm.
  - Nach 5 min ist T01 nicht nachweislich eingeschwungen. Bei feineren Zellen schreitet ein expliziter Löser je Echtzeit-Minute
    vermutlich weniger Simulationszeit voran (CFL) [Ableitung].
  - Bett 99,9 % nass und Kolk-p90 0,80 m sprechen dafür, dass das Nachfüllen die Zellen schon gefüllt hat. Ein Stabilitätsnachweis
    fehlt aber (`pruefung.md`).

**Skript für die Vorhersage und die Lippenschatten-Maske** (läuft so mit den Repo-Dateien; Python, NumPy):

```python
# lippenschatten.py  –  python -I lippenschatten.py <repo>/recherche/antworten/p2_bett <ausgabeordner>
import json, sys, numpy as np
R, OUT = sys.argv[1].rstrip('/') + '/', sys.argv[2].rstrip('/') + '/'
d = json.load(open(R + 'bettplan_p2.json'))
zmin, zmax, gew, spg, abt, kante = np.fromfile(R + 'talkaskade_soll.f32', '<f4').reshape(6, 384, 101)
zon = np.fromfile(R + 'talkaskade_zonen.u8', np.uint8).reshape(384, 101)
s = 389.0 + 0.5 * np.arange(384)                                  # s0 389 m, ds 0,5 m; u0 -12,5 m, du 0,25 m
P = np.array(d['spline_stufenpunkte']['punkte'])
spl = np.repeat(np.interp(s, P[:, 0], P[:, 1])[:, None], 101, 1)  # lineare Stufenpunkt-Spline, quer konstant
band = (kante >= 0.25) & (kante <= 2.0) & np.isin(zon, [5, 6, 7])
ok = band & np.isfinite(zmin)                                     # Zonen 5/6 mit Boden-Untergrenze
f = ok.sum() / band.sum()                                         # Zone 7 als trocken angenommen
schatten = ok & ((spl - spg) > 0.05)
for name, lvl in (('H1 Spline', spl), ('H2 Plan+0,20', spg + 0.20)):
    t = lvl - zmin
    print(name, ' / '.join(f'{100*f*np.mean(t[ok] > x):.1f}' for x in (0.01, 0.02, 0.05, 0.10)))
print('Lippenschatten am Band %.1f %%' % (100 * schatten.sum() / band.sum()))
m = np.zeros((384, 101), np.uint8); m[band] = 2; m[schatten] = 3   # 1 bleibt frei, 2 = Band, 3 = Band im Lippenschatten
m.tofile(OUT + 'talkaskade_lippenschatten.u8')                    # gleiches Raster wie talkaskade_zonen.u8
```

Erwartete Ausgabe: `H1 Spline 13.7 / 13.6 / 13.4 / 12.8`, `H2 Plan+0,20 5.5 / 5.2 / 3.8 / 1.9`, `Lippenschatten am Band 16.6 %`.

#### Unterscheidende Tests (alle am ganzen SWR oder an vorhandenen Dumps, keine Teilung)

| Test-ID | Was | Aufwand | Erwartung H1 (Nachfüllen + Spline) | Erwartung H2/H3 (Überfall bzw. Gitter/Film) | Entscheidung |
|---|---|---|---|---|---|
| **T6j-A** | Maske oben über `p2_bett_welt.py` wie Prüfband-Wert 2 in die Welt bringen (Wert 3 = Lippenschatten). Für die **vorhandenen** Dumps T01 (8,7 cm) und ganze SWR (36,7 cm) ausgeben: Anteil nass > 2/10 cm getrennt nach Maske 2/3; in nassen Bandzellen Median von (Sim-Spiegel − Spline-Z) und (Sim-Spiegel − Plan-Spiegel) | 30–60 min, ohne Editor | T01: **≥ 70 %** der > 10-cm-Zellen in Maske 3; dort Sim-Spiegel − Spline-Z im Median ±5 cm; außerhalb der Maske > 10 cm ≤ 3 % | > 10-cm-Zellen gleichmäßig in Maske 2 und 3 verteilt; Sim-Spiegel folgt dem Plan-Spiegel + h (h ≈ 0,15–0,25 m wie 6i §4) bzw. nur Filme 1–5 cm | H1 bestätigt → T6j-C direkt. Uneindeutig → T6j-B |
| **T6j-B** | Nachfüllen umschalten (s. u.). B0: Setzt die Änderung von `match_spline_height_amount` die Simulation zurück? B1 (falls nein): 5 min mit 0,3, bis zwei Dumps im Abstand von 3 min um < 1 Prozentpunkt abweichen; dann 0 setzen, Dumps nach +2/+5/+10 min. B2 (falls B0 zurücksetzt): zwei Läufe ab Reset mit 0,3 und 0,4, je bis stabil | B1 ≈ 25 min, B2 ≈ 2 × 15 min | B1: Band in Maske 3 fällt in 5 min um ≥ 50 % (relativ), Bett Talkaskade ≥ 97 %. B2: mit 0,4 steigt Maske 3 um ≥ 3 Prozentpunkte, Maske 2 bleibt | Band in Maske 3 ändert sich < 3 Prozentpunkte | H1 → T6j-C. Sonst: Löser-/Gittergrenze bei 37 cm; Kriterium 6g §3 (0,25–1 m ≤ 30 %, 1–2 m ≤ 5 %) + Kantengras |
| **T6j-C** (Hebel) | Spline-Breite **nur s 389–580** = Bett + 0,5 m statt Bett + 2 m; Rest wie heute, ganze SWR 36,7 cm, Reset LIVE_SIM, bis stabil, Bake, BAKED_SIM | ≈ 30 min | Band > 10 cm in Maske 3 fällt deutlich (≥ 50 % relativ); Bett ≥ 99 %, Front 788 | keine Wirkung → H1 falsch | Ziel nach 6g §3 für 37 cm prüfen. Mit Wirkung **und** Front 788 als Regel-Vorschlag an Ferat (Ausnahme zu `band_zugabe_m` 2) |
| T6j-D (optional) | `resolution_max_axis` **4096** am ganzen SWR (6g Variante D, keine Teilung): nur prüfen, ob die Engine es annimmt (SimRes/SimDx aus `swr_info`) | 10 min | – | – | SimRes 4096 → Lauf mit Front-Protokoll (Abbruch: Front 3 min ohne Fortschritt). Geklemmt → D verworfen |

**Abbruchbedingungen:** Bett der Talkaskade < 97 % (der Zulauf versiegt, die Messung gilt nicht mehr) oder Front talab rückläufig → letzten
gültigen Dump verwenden. Alles nur im Speicher; Rückweg wie bisher: Level ohne Speichern neu laden, dann steht wieder die gebackene ganze SWR.

**Risiken T6j-C** [Projekt]:
- F2 (C2, Band = Bett) blieb bei s 59 stehen. Die Regel „Pixel ≤ Band/12“ wird mit Bett (2,9 m) + 0,5 m bei 0,29 m/Pixel nur
  knapp gehalten (11,7 Pixel).
- Darum nur in der Talkaskade, wo das eingeschnittene Bett die Front führt (6g §2, Ableitung).
- Bleibt die Front stehen: Bett + 1 m testen (6f §2 Schritt 3).

**T6j-D:** Ob D sinnvoll ist, zeigt T00. Dort blieb die Front schon bei 18,4 cm in der Bergrinne bei s 131 stehen. D ist deshalb nur der
Prüfschritt „wird 4096 angenommen“, kein Umbau. 4096 widerspräche außerdem unserer Regel ≤ 2048 (keine Epic-Grenze, 6g §1.2).

**Boden-Trick** (6g §2):
- In der 6g-Form (Schulter + 0,1 m) senkt er H1 nur von 13,6 auf 12,5 % [Rechnung].
- Wirkt er erst nach T6j-C nötig, dann im Lippenschatten auf **Spline-Z + 0,05 m** (median 0,55 m, bis 1,2 m über dem Boden), sonst
  Schulter + 0,1 m.
- Den Netzplan dafür gebe ich erst aus, wenn T6j-A H1 bestätigt.

**Editor-Schritt B0/B1** (vorhandene Werkzeuge `swr_dump.py`, `swr_dump_lesen.py` und `p2bett_pruefband.py` für die Dumps verwenden):

```python
import unreal
NAME = 'SWR_Sim_F_ERLENBACH_1V_C2'
sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
akt = [a for a in sub.get_all_level_actors() if a.get_actor_label() == NAME][0]
c = akt.get_component_by_class(unreal.ShallowWaterRiverComponent)
print('T6J_B vorher', c.get_editor_property('match_spline_height_amount'), c.get_editor_property('render_state'))
c.set_editor_property('match_spline_height_amount', 0.0)  # löst ein PostEditChange aus -> B0: fällt das Bett trocken (Reset)?
print('T6J_B nachher', c.get_editor_property('match_spline_height_amount'))
```

`render_state` muss vorher LIVE_SIM sein (euer Fund: Reset ohne LIVE_SIM simuliert nicht). Die Feldnamen sind die, die euer
`ue_swr_bauen.py swr_einrichten` setzt. Ob `set_editor_property` hier ein Rebuild auslöst, ist [offen]; genau das klärt B0 (Bett nach
30 s noch ≥ 97 % nass = kein Reset).

### 1.2 (b) Variante A (ganze SWR + Talkaskaden-Kopie darüber) – verworfen

Variante A ist eine Teilungsvariante. Nach README und Exporter-Sperre braucht sie neue Evidenz. Die gibt es nicht, und gegen sie sprechen
drei Punkte:

| Punkt | Beleg |
|---|---|
| Die Rechenfläche einer SWR folgt ihren Wasserkörpern; eine Box oder ein Ausschnitt ist nicht einstellbar | [Projekt] 6i §3, Header 5.8 lokal gelesen |
| Die ganze SWR rechnet deshalb die Talkaskade weiter, mit 36,7 cm und **78,6 % Band**. Mit BAKED_SIM (euer Spielzustand, 6i §1) zeichnet sie ihre eigene Fläche. Eine feine SWR darüber kann dieses Wasser nicht verdecken, wo sie selbst trocken ist, und das ist genau das Band | [Ableitung] |
| Mehrere SWR/Flüsse in einer Kachel konkurrieren: Im WCBS-Weg zeichnet je Kachel nur eine Wasserkomponente; trockene Streifen bzw. fehlendes Netz an der Gabelung | [Suchauszug] Forum 2738013 |
| Eine Rangfolge zwischen zwei SWR-Darstellungen (BAKED_SIM) habe ich nicht gefunden; `overlap_material_priority` gilt für Water Bodies | [Suchauszug], offen |

**Wiederaufnahme nur, wenn** eine Eigenschaft bzw. ein Modus nachgewiesen ist, der einen Bereich aus der Rechnung oder dem Zeichnen einer
SWR ausnimmt. Dann wären die Prüfpunkte:
1. Jede SWR einzeln ausblenden (wer zeichnet wo).
2. Band im **Bild** messen (§2), nicht im Dump, weil zwei Schichten übereinander liegen.
3. Spiegelsprung an beiden Enden der feinen SWR ≤ 2 cm.
4. Kein Flackern beim Annähern an t430/t500/t550.

### 1.3 (c) Quelle einer Talkaskaden-Kopie – verworfen

- **Einlauf aus dem Nichts** (`source_size` 300 bei s 386):
  - Der Abfluss im Teil hängt dann an Quelle und Nachfüllen. Er ist nicht der Abfluss, der von oben ankommt.
  - Damit stimmen Überfallhöhen und Beckenspiegel nicht mit dem ganzen Bach überein.
  - T02 zeigt die Folge: 7 m Anlaufstrecke trocken [Ferat].
  - Auch die 25,9 % von T01 sind deshalb nur bedingt auf den ganzen Bach übertragbar. Das Nachfüllen auf Spline-Höhe (H1) ist davon
    aber kaum abhängig.
- **Ganzer Fluss als Quelle** (`source_river_water_bodies` = Original-`WaterBodyRiver`):
  - Die Fläche wird aus den eingetragenen Wasserkörpern berechnet (6i §3). Die Talkaskaden-SWR bekäme also wieder 740 × 117 m und
    36,7 cm Zellen, ohne Gewinn.
  - Das Forum-Muster (mehrere Wasserkörper als Quelle und Senke **einer** SWR) löst Gabelungen. Es verkleinert die Fläche nicht, es
    vergrößert sie.
  - Eine SWR kann man nicht als Quelle eintragen, das Feld nimmt `WaterBodyRiver` [Suchauszug: Einrichtung
    `SourceRiverWaterBodies=(WaterBodyRiver)`].

**Folge für §1:** Feinere Zellen gibt es ohne Teilung nur über T6j-D. Der wirksamste Hebel nach dem Befund ist aber nicht die Zelle,
sondern das Nachfüllen aus dem Lippenschatten zu halten (T6j-C).

---

## 2. Pixelmessung (§4.2): Messdesign für den Umbau

### 2.1 Warum beide bisherigen Wege versagt haben [Ableitung + Suchauszug]

| Befund | wahrscheinliche Ursache | Prüfpunkt |
|---|---|---|
| Ausblenden: K2 5,1 %, obwohl voller Felsnetze | `hide_component` wirkt in der SceneCapture nicht auf Nanite [Ferat]. Ähnliche Meldungen: Nanite umgeht einzelne Ausschluss-Flags (Reflection Capture, 5.7), die SceneCapture zeigt Nanite-Ansichten nicht [Suchauszug] | **Keine SceneCapture mehr.** Im Hauptbild messen |
| Stencil: K1 100 % | CustomDepth testet nur gegen andere CustomDepth-Objekte, nicht gegen die Szene. Hat auch die Landschaft einen Stencil-Wert oder wird „Stencil > 0“ ohne Tiefenvergleich gezählt, wird alles Netz | Verdeckungsregel CustomDepth ≤ SceneDepth · 1,002 + 1 cm; Kontrollfall KF2 |
| Stencil: K2 1,4 % | Nanite schreibt in diesem Weg kein CustomDepth. Presse zu 5.2: Nanite unterstützt Custom Depth/Stencil; Bug UE-171655 (5.1) mit Ziel 5.2 gelöst; Meldung aus 5.6: Nanite-Netz nicht im CustomDepth [Suchauszug] | KF3 (Nanite-Würfel) |
| beide | `r.CustomDepth` nicht 3 (dann kein Stencil), Antialiasing mischt Klassenfarben, Bildschirmprozent ≠ 100 | C1/C5 unten |

### 2.2 Aufbau

1. **Stencil-Werte**, 8 Bit, nur ganze Werte:

   | Wert | Klasse | Wie gesetzt |
   |---|---|---|
   | 1 | Fels/Stein | `PrimitiveComponent.set_render_custom_depth(True)`, `set_custom_depth_stencil_value(1)` auf allen `StaticMeshComponent` der Klasse (eure Zuordnung aus `ue_pixel_messung.py`) |
   | 2 | Pflanze (Bäume, Büsche, Farne als Netz) | dito. Foliage: auf den `FoliageInstancedStaticMeshComponent`-Komponenten der Instanced-Foliage-Akteure (gilt für alle Instanzen eines Typs). Dauerhaft wären die FoliageType-Felder `bRenderCustomDepth`/`CustomDepthStencilValue` (UE-API-Seite, Suchauszug) |
   | 3 | sonstiges Netz | dito |
   | 5 | Wasser | auf den Komponenten von SWR/Water Body versuchen; ob SingleLayerWater CustomDepth schreibt, klärt KF7 |
   | 10 | Landschaft | Landschaftsakteur bzw. seine Komponenten [zu prüfen: Python-Feld `render_custom_depth` am `LandscapeProxy`] |
   | – | Gras (Landscape Grass) | **keine** CustomDepth-Option an `FGrassVariety` gefunden [Suchauszug] → erscheint als „unklassifiziert“ |

   Projekteinstellung bzw. `r.CustomDepth 3` (Stencil). Die Stencil-Werte gelten laut API-Text nur damit.
2. **Post-Process-Material `M_EL_PP_Klassen` (anzulegen):**
   - Domain Post Process, Blendable Location **Replacing the Tonemapper**, nur Emissive.
   - Die Lage läuft bei TSR in Ausgabeauflösung, sonst in Renderauflösung [Suchauszug, Python-API `BlendableLocation`].
   - Eingänge SceneTexture `CustomStencil`, `CustomDepth`, `SceneDepth`.
   - Ausgabe nur 0/1-Kanäle, damit Gamma und 8-Bit-PNG die Farben nicht verschieben.
   - Custom-Knoten (HLSL):
     ```hlsl
     // Eingänge: St = CustomStencil.r, CD = CustomDepth.r, SD = SceneDepth.r (cm), Modus (0 Klassen, 1 Abstand)
     float s = round(St);
     bool vorn = CD <= SD * 1.002 + 1.0;          // nur wenn das Stencil-Objekt das vorderste ist
     if (Modus > 0.5) return SD < 3000 ? float3(1,0,0) : (SD < 15000 ? float3(0,1,0) : float3(0,0,1));
     if (s < 0.5 && SD > 5.0e6) return float3(0,0,0);   // Himmel (Schwelle an KF6 eichen)
     if (s < 0.5 || !vorn)      return float3(1,0,1);   // unklassifiziert: Gras, Objekt ohne Stencil
     if (s == 1)  return float3(1,0,0);                 // Fels
     if (s == 2)  return float3(0,1,0);                 // Pflanze
     if (s == 3)  return float3(0,0,1);                 // sonstiges Netz
     if (s == 5)  return float3(0,1,1);                 // Wasser
     if (s == 10) return float3(1,1,0);                 // Landschaft
     return float3(1,1,1);                              // unbekannter Wert = Fehler
     ```
3. **Aufnahme im Hauptbild:**
   - Kamera aus `blick_bilder.sh`, ungebundenes Post-Process-Volumen mit dem Material nur für die Messung.
   - `r.AntiAliasingMethod 0`, `r.ScreenPercentage 100`, Bewegungsunschärfe aus.
   - `HighResShot 1920x1080`. Die Syntax mit `bMaskUsingCustomDepth`/`bDumpBufferVisualizationTargets` steht in Epics Screenshot-Doku
     [Suchauszug, Doku 4.26].
   - Je Kamera drei Bilder:
     - (a) normales Bild ohne PP-Material
     - (b) Klassen (Modus 0)
     - (c) Abstand (Modus 1)
   - Dazu (d) Klassen mit ausgeblendetem Gras, nur für die Gras-Lesart [zu prüfen: CVar `grass.Enable 0` bzw. Showflag; ein Beleg fehlt,
     Name per Konsole/Autovervollständigen prüfen].
   - World Partition: alle Zellen im Blick geladen, sonst fehlt Foliage.
4. **Auswertung offline** (Zähler, Nenner und Klassen nach `pruefung.md` „Messwerkzeuge“):
   - **Nenner N** = alle Pixel − Himmel − Wasser.
   - **Netzanteil** = (Fels + Pflanze + sonst) / N, auch je Klasse und je Abstandsband (Bild c).
   - **Drei Gras-Lesarten:**
     - G1: Gras zählt als Pflanze (unklassifiziert → Pflanze, nur wenn KF5 zeigt, dass unklassifiziert = Gras).
     - G2: Gras aus dem Nenner nehmen.
     - G3: Gras durchsichtig, Klasse aus Bild (d).
   - **Gültigkeit je Bild:**
     - Pixel ohne reine Farbe ≤ 0,5 %.
     - Weiß (Fehler) = 0.
     - Unklassifiziert in einer Szene ohne Gras ≤ 1 %.
     - Overlay angesehen (Bild b halbtransparent über a).

```python
# pixel_zaehlen.py  –  python -I pixel_zaehlen.py klassen.png [abstand.png]
import sys, json, numpy as np
from PIL import Image
FARBE = {(255,0,0):'fels', (0,255,0):'pflanze', (0,0,255):'netz_sonst', (0,255,255):'wasser',
         (255,255,0):'landschaft', (0,0,0):'himmel', (255,0,255):'unklassifiziert', (255,255,255):'fehler'}
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
q = np.where(a >= 128, 255, 0)
unrein = float(np.mean(np.any(np.abs(a - q) > 8, axis=2)))
n = {k: int(np.all(q == np.array(f), axis=2).sum()) for f, k in FARBE.items()}
gesamt = a.shape[0] * a.shape[1]
N = gesamt - n['himmel'] - n['wasser']
netz = n['fels'] + n['pflanze'] + n['netz_sonst']
aus = {'pixel': n, 'bild_anteil': {k: v / gesamt for k, v in n.items()}, 'unrein_anteil': unrein, 'nenner': N,
       'netz_anteil_G2': netz / max(1, N - n['unklassifiziert']),
       'netz_anteil_G1': (netz + n['unklassifiziert']) / max(1, N),
       'gueltig': unrein <= 0.005 and n['fehler'] == 0}
if len(sys.argv) > 2:                                    # je Abstandsband
    b = np.where(np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(int) >= 128, 255, 0)
    for name, f in (('nah', (255,0,0)), ('mittel', (0,255,0)), ('fern', (0,0,255))):
        m = np.all(b == f, axis=2)
        nn = m.sum() - (m & np.all(q == (0,0,0), axis=2)).sum() - (m & np.all(q == (0,255,255), axis=2)).sum()
        nz = sum((m & np.all(q == f2, axis=2)).sum() for f2 in ((255,0,0), (0,255,0), (0,0,255)))
        aus['netz_anteil_G2_' + name] = float(nz) / max(1, nn)
print(json.dumps(aus, indent=1))
```

### 2.3 Kontrollfälle (vor jeder Projektzahl, in dieser Reihenfolge)

Sollwerte aus der Geometrie, unabhängig vom Zählwerkzeug. Bild 1920 × 1080, horizontales FOV 90° → Brennweite f = 960 px.
Ein Quadrat von a = 200 cm senkrecht im Abstand d = 500 cm ist f · a/d = 384 px breit und hoch, das sind 384² / (1920 · 1080) = **7,11 %**.

| KF | Aufbau (kleines Testlevel) | Soll | Toleranz | wenn verfehlt |
|---|---|---|---|---|
| KF1 | `/Engine/BasicShapes/Cube` ×2 (200 cm), Vorderfläche 500 cm vor der Kamera, Stencil 1; Hintergrund Himmel | Fels 7,11 %, Himmel 92,89 % | ±0,1 Prozentpunkte (Randpixel ≈ 0,07 %) | Grundweg falsch (C1–C5) |
| KF2 | wie KF1, dazu eine Fläche **ohne** CustomDepth 50 × 100 cm in 250 cm Abstand, so gesetzt, dass ihr Bild (192 × 384 px) genau die linke Hälfte des Würfels deckt | Fels 3,56 %, unklassifiziert 3,56 % | ±0,1 | Verdeckungsregel fehlt (Ursache K1 = 100 %) |
| KF3 | wie KF1 mit einer Nanite-Kopie des Würfels (`SM_EL_Testwuerfel_Nanite`, anzulegen) | wie KF1 | ±0,1 | Nanite schreibt hier kein CustomDepth → Rückfall §2.4 |
| KF4 | ein Würfel als Foliage-Instanz (HISM), Stencil am Foliage-Komponenten | wie KF1 | ±0,1 | Foliage-Weg falsch |
| KF5 | ebene Landschaftsfläche, Stencil 10, mit Gras; Bild (d) ohne Gras | unklassifiziert (b) = Gras-Pixel aus (b) − (d); in (d) unklassifiziert ≤ 0,5 % | ±1 | anderes Objekt ohne Stencil im Bild → Klassenliste ergänzen |
| KF6 | Horizontblick: Landschaft unten, Himmel oben | Himmel + Landschaft (+ Gras) = 100 %, Himmelslinie im Overlay sauber | Augenprüfung | SD-Schwelle Himmel anpassen |
| KF7 | Becken mit gebackener SWR (BAKED_SIM) | Wasserfläche als Wasser **oder** sauber als „unklassifiziert“ bekannt | Augenprüfung | Wasser aus dem Nenner nur über eigene Maske (z. B. Wasser-Info), sonst „Wasser nicht gemessen“ |

- **Danach im Projekt:**
  - K2 als Plausibilitätsfall: Netzanteil ≥ 50 % erwartet [Ferat: „voller Felsnetze“], Overlay ansehen.
  - Danach Eichung an RA2.
  - Erst dann K1/K3 und B5P als Zahlen verwenden.
- **Versionsangabe:** Werkzeugversion, Engine 5.8.3, `r.CustomDepth`, AA und Bildschirmprozent je Messung ins JSON schreiben.

### 2.4 Rückfall, falls KF3 scheitert

- **Nur für die Messaufnahme** an den Felsnetzen „Force Disable Nanite“ setzen. Epic beschreibt das je StaticMeshComponent: Es schaltet
  auf das Ersatznetz [Suchauszug, Blueprint-API `SetForceDisableNanite`; Python-Name `set_force_disable_nanite` zu prüfen].
- Laut Forum stellt das Abschalten von Nanite die CustomDepth-Ausgabe wieder her [Suchauszug].
- **Prüfung:** KF3 mit Ersatznetz muss KF1 treffen. Dann je Projektkamera das Normalbild mit und ohne Nanite vergleichen (SceneDepth bzw.
  Silhouette).
  - Abweichung der Netzfläche ≤ 1 Prozentpunkt → brauchbar.
  - Sonst sind die Werte nur „Ersatznetz-Anteil“.
- Danach Nanite wieder an, nicht speichern.

---

## 3. Rinnsal am Bachanfang (Nachtrag, Antwort 19 §3/§6.3)

**Warum das 0,4-m-Rinnsal im Gras verschwindet** [Ableitung, Geometrie]:
- Ein Grasrand der Höhe h_g vor dem Wasser verdeckt aus Augenhöhe H im Abstand d einen Streifen von etwa h_g · d/H Breite.
- Sichtbar ist das Wasser nur, wenn seine Breite b plus der grasfreie Saum c größer sind.

| Gras h_g | d = 5 m | d = 10 m | d = 20 m |
|---|---|---|---|
| 0,4 m (Wiese) | 1,2 m | 2,4 m | 4,7 m |
| 0,15 m (Moos/Kraut) | 0,4 m | 0,9 m | 1,8 m |

(H = 1,7 m.)

**Folge:**
- 0,8 m statt 0,4 m macht das Rinnsal bei 0,4 m Gras nur bis etwa 3,4 m Abstand sichtbar statt bis 1,7 m. Die Breite ist nicht der Hebel.
- Der Hebel ist ein **niedriger Saum** plus Kontrast (nass, dunkel, glänzend).
- Natürlich bleibt der Anfang schmal: Die häufigste Quellbachbreite ist 32 ± 7 cm (19 §1.1).

**Vorschlag „Rinnenkopf“** (je Anfang, die ersten 10–15 m; Werte als [Annahme] für den Test):

| Baustein | Wert | Mittel im Projekt |
|---|---|---|
| Saum niedrig | Gras ×0 bis b/2 + 0,3 m neben der Mitte, Rampe auf ×1 bei b/2 + 1,0 m; bis s = 15 m, danach ×0,5 bis L/2 | Eure Grasdichte hängt an `v_*.r8` (≈ 2,3 m/Texel, 6i §5), das ist zu grob. Darum im Landschaftsmaterial der Graseingang × (1 − W_rinne), W_rinne = Bachgewicht × (1 − SmoothStep(0,10; 0,30; h)), h = Gelände − Spiegel aus `T_Eldarien_Wasserspiegel_2m`, wie das Uferband W_ufer in 16h-N2 (neuer Zweig, **anzulegen**). Statt Gras zeigt die Fläche Moos (Lage) |
| Rinne | 0,10–0,15 m eingetieft (Water-Brush, wie 19 §3 „Gegenmittel“); Lage Schlamm 50 / Moos 30 / Kies 20 in der Rinne | Lagen-Wunsch wie Quellfassung |
| Nässe | Decal `/Game/Coast_Dunes_Environment_Set/Decals/Materials/MI_Deca_Wet_Flat`, 0,8–1,2 m breit, in 2–3-m-Stücken längs der ersten 5–10 m, Stöße überlappend; an Felsquellen bleibt `MI_Leakage_03` | beide im Inventar (`inventar_extra.json`) |
| Lichtpunkte | 3–6 Kiesel 0,1–0,25 m in der Rinne, ohne Kollision (unter 0,4 m, also kein Hindernis) | Bachdekor-Netze mit MI_EL (Nasslinie) |
| Wasser | SWR-Breite bleibt 0,4 m (Hang/Sicker), Felsquelle 0,6 m; kein Schaum | Regel 19 §1.5 |

- **Sickerquelle:** Dort ist der flächige Nassbereich ohnehin das Bild. Der Bach beginnt am unteren Rand (19 §1.4). Den Rinnenkopf nur am
  Übergang setzen.
- **Prüfung** an euren drei gebauten Fällen (`_kam_anfaenge*.json`), Augenhöhe, d = 5 / 10 / 20 m, vorher/nachher gleiche Kamera:
  - Rinne bzw. Wasserlinie bei 10 m durchgehend über ≥ 70 % der ersten 10 m erkennbar.
  - Bei 20 m als dunkle Linie lesbar.
  - Kein grasfreier „Kanal“, der breiter als 2 m wirkt.
  - Die Bewertung macht, wer die Bilder ansieht. Ich habe keine Bilder dieser Fälle gesehen.
- **Rückfall:** Wirkt das Wasser selbst danach kantig oder blinkt (1–2 SWR-Zellen), b0 auf 0,6 m. Die Wasser-Info-Regel
  wird damit sogar leichter erfüllt ((0,6 + 2)/12 = 0,22 m/Pixel statt 0,20). 0,8 m nicht.
- **Kosten:** etwa 10 Anweisungen im Material, 0 Sampler (Spiegel- und Bachgewicht-Textur sind schon gebunden, V18) [Ableitung,
  Material-Stat prüfen]. Seen und Flüsse müssen gleich bleiben (Bachgewicht 0), mit Vorher-Bild prüfen (`pruefung.md`
  „Auswirkungen auf andere Stellen“).

---

## 4. B5 (Nachtrag 09:00 und §3)

- **Weiße Quadrate:** Befund und Lösung sind schlüssig (`ukjhcamga_tier_0` ohne gebundene Texturen → `MI_EL_Klippe_ukjhcamga` auf
  `M_EL_Klippe_RVT`).
  - Die Regel „jedes Fab-Raw-Netz vor dem Setzen mit MI_EL-Überschreibung“ passt zu 6i §4/§5 (fehlende MIs, 8K-Raw-Sätze).
  - Als Selbstprüfung im Setzer: je Netz alle Material-Slots lesen. Fehlt `MI_EL_` im Namen oder hängt das MI an `M_MS_Base` →
    FEHLER statt Setzen.
- **Felsdeckung (OG) 176 %:**
  - Über 100 % kann nur die **Summe der Fußflächen** sein, nicht die Deckung. 21 §(a) definiert Deckung als Vereinigung ohne
    Doppelzählung; dort Halde Fußflächen 145 %, Deckung 77 %.
  - Bitte beide Werte getrennt benennen. Nur die Vereinigung mit den Prüferzahlen (Halde 79 / Schrofen 61 / Wand 83 %) und dem Ziel
    vergleichen.
- **14,7 Netze je 100 m²** liegen über den RA-Demos (3,8–10,5, 6h §2). Das ist kein Fehler, solange Pixel- und Bildbefund passen.
- Die Pixelmessung von B5P erst nach KF1–KF7 (§2.3) werten.
- Rückfrage 1 (Front-Achse der Bänder) bleibt bei euch offen. Laut K3 zeigen die Bänder hangab, das reicht vorerst.

---

## Was fehlt bis Witcher 4

Messlatte wie 6e: dichte Vegetation bis an die Kante, Wind, weiches Licht, klare Wasserformen. Die Techdemo ist nur über Presse und
Suchauszüge belegt.

Nach Wirkung:
1. **Wasser im Bett halten** (Talkaskade):
   - zuerst T6j-A, dann T6j-C (Nachfüllen aus dem Lippenschatten)
   - Ziel nach 6g §3 bei 37 cm, Bild ohne grauen Film neben den Becken
2. **Kantenbewuchs** (6e: Kantengras, Moos, Farne) bis an die Wasserlinie. Er verdeckt die 1–5-cm-Filme (≈ 12 Prozentpunkte des Bands),
   die keine Simulationseinstellung wegnimmt.
3. **Verlässliche Dichtezahl:** Pixelmessung nach §2, erst dann Fels- und Bewuchsdichten in B5 und Talkaskade nachsteuern. Ohne sie ist
   jede Dichteentscheidung geraten.
4. **Bachanfänge lesbar:** Rinnenkopf §3 an den drei Beispielen, danach als Regel für die 81 neuen Köpfe.
5. **Fab-/Mountain-Netze mit Nasslinie und eigenem MI** (6i §4, B5-Regel). Sonst bleiben helle oder texturlose Ausreißer.
6. **Spielzustand absichern:** BAKED_SIM im gepackten Build, Streaming und GPU-Zeit (getrennte Antwort 6i).
7. Fall-Effekte nur an Fällen, Totholz, Licht im Einschnitt (6e/6f).

## Quellen

Abruf 18.10.2026.
- `dev.epicgames.com`, `forums.unrealengine.com`, `issues.unrealengine.com`, `realtimevfx.com` und `web.archive.org`: aus der Cloud nicht
  erreichbar (DNS-Fehler bzw. Proxy 403).
- Alle Web-Angaben sind daher **Suchauszüge**. Für eine Entscheidung tragen nur die lokalen Kontrollfälle.

- Python-API `BlendableLocation` (Replacing the Tonemapper: Auflösung bei TSR/TAAU, lineare Eingänge) – https://docs.unrealengine.com/en-US/PythonAPI/class/BlendableLocation.html ; https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/BlendableLocation
- Post Process Materials – https://dev.epicgames.com/documentation/en-us/unreal-engine/post-process-materials-in-unreal-engine
- Taking Screenshots (HighResShot-Syntax, `bMaskUsingCustomDepth`, `bDumpBufferVisualizationTargets`) – https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine ; https://docs.unrealengine.com/4.26/WorkingWithMedia/TakingScreenshots
- Forum: `r.BufferVisualizationDumpFrames` vor HighResShot setzen – https://forums.unrealengine.com/t/take-screenshot-with-buffer-visualization-in-blueprint/394888
- `UFoliageType` (`bRenderCustomDepth`, `CustomDepthStencilValue` „requires project setting or r.CustomDepth == 3“, `CustomDepthStencilWriteMask`) – https://docs.unrealengine.com/4.27/API/Runtime/Foliage/UFoliageType/index.html ; https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Foliage/UFoliageType
- `FGrassVariety` / `ULandscapeGrassType` (keine CustomDepth-Option im Auszug gefunden; Listen gekürzt, nicht ausgeschlossen) – https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Landscape/FGrassVariety ; Forum 4.16 (CustomDepth für Foliage, Gras offen) – https://forums.unrealengine.com/t/300106
- Nanite und CustomDepth: Forum 5.1 (Commit „Add ability to render Nanite in the custom depth stencil pass“) – https://forums.unrealengine.com/t/5-1-nanite-not-able-to-write-to-stencil-buffers/746933 ; UE-171655 (5.1, Ziel 5.2) – https://issues.unrealengine.com/issue/UE-171655 ; Presse 5.2 („Custom Depth and Stencils“ für Nanite) – https://wccftech.com/unreal-engine-5-2-out-now-adds-improvements-to-anti-stuttering-system-enhances-lumen-and-nanite/amp/ ; Meldung 5.6 (Nanite nicht im CustomDepth) – https://realtimevfx.com/t/custom-depth-on-transperent-material/29629
- Nanite und Ausschluss-Flags bzw. SceneCapture: https://forums.unrealengine.com/t/disabling-visible-in-reflection-capture-is-ignored-on-geometry-using-nanite/2745609 ; https://forums.unrealengine.com/t/nainte-visualize/2642841
- `SetForceDisableNanite` (Ersatznetz je Komponente) – https://dev.epicgames.com/documentation/unreal-engine/BlueprintAPI/Rendering/SetForceDisableNanite
- Shallow Water: Forum 2738013 (Gabelung, eine Wasserkomponente je Kachel, Abhilfe mehrere Water Bodies an einer SWR) – https://forums.unrealengine.com/t/shallowwaterriver/2738013 ; Einrichtung Quelle/Senke (`SourceRiverWaterBodies=(WaterBodyRiver)`) – https://forums.unrealengine.com/t/shallowwaterriver-lake-ocean/2838534 ; Parameter-Leitfaden – https://forums.unrealengine.com/t/tutorial-baked-river-simulations-parameter-reference/2512112 (Inhalt aus 16f, lokal gelesen)
- Witcher-4-Techdemo: wie 6e (CDPR-Presse) – https://press.cdprojektred.com/news/1778/cd-projekt-red-and-epic-games-present-the-witcher-4-unreal-engine-5-tech-demo-at-the-state-of-unreal-2025
- Im Repo: 6i §3 und `swr_teilung_plan_lokal.md` (Header 5.8, Rechteckmodell), 16f (Epic-Parameter lokal), 16g-N2 (Nachfüllrate 0,3,
  Band + 2 m, F2), 6b/6c/6f (Bettplan, Prüfband), 6g (Boden-Trick, 37-cm-Ziel), 19 §1.1/§1.5/§3, 21 §(a) (Deckungsdefinition),
  `inventar_extra.json` (Decals)

## Rückfragen

1. **Saum im Landschaftsmaterial (§3):** Darf der Graseingang des Landschaftsmaterials einen Faktor W_rinne bekommen (neuer Zweig,
   weltweit nur bei Bachgewicht > 0)?
   - Ohne diese Erlaubnis bleibt nur, Gras über die Bewuchskarten auszudünnen. Das ist mit 2,3 m/Texel zu grob für einen Saum von 1 m.
   - Dann würde ich b0 0,6 m und Moosplatten entlang der Rinne vorschlagen.
