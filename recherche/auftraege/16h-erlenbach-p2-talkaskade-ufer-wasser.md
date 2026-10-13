# Auftrag 16h – Erlenbach p2: Talkaskade wirkt wie ein sandiger Graben (Ufer, Wasserfarbe, Material-Einheiten)

Stand 13.10.2026, 11:15. Bezug: 16f (Plugin-Bett, Material), 16g (SWR im steilen Bergbach, gelöst: Wasserzone 4096).

## 1. Stand Erlenbach p2

- Lauf vom Berg: Quelle 190 m in der D2-Felsrinne, 788 m bis in den C3-Fluss, Bett mit dem Water-Plugin gegraben (Kasten-U,
  3 Durchgänge), Bachdekor 21 448 Teile, SWR gebacken (WCBS), **Bett zu 99,9 % nass**, Tiefe Mitte 0,47–0,64 m.
- Abschnitte (s in m): Bergrinne 0–199, Durchbruch 199–390, **Talkaskade 390–579**, Kiesbett 579–728, Mündung bis 788.
- Ferat (12.10.): Quelle, Bergrinne und Schlucht „sehen gut aus“. Die Schwachstelle ist die Talkaskade.
- Bilder: `bilder/swr_p2/p2x_bogen.jpg` (5 Abschnitte), `bilder/swr_p2/tk_mit_ohne_wasser.jpg` (Talkaskade, links mit Wasser,
  rechts Wasser ausgeblendet), `bilder/swr_p2/altwasser_vorher_nachher.png` (Draufsicht, siehe 2).

## 2. Befund A (lokal behoben, technisch): Reste der alten Gewässer

Die alten Epic-Flüsse `F_ERLENBACH_1_C2`, `F_ERLENBACH_1V_C2` und `F_ERLENBACH_2_C2` (23–39 m breit, Houdini-Stand) sowie der Bach
`B_R3_K10_TUNDRA_01` existieren nicht mehr. Ihre Spuren standen aber noch in den Weltdaten:
- Gras-Dichten `v_*` = 0,
- `karte_wasser` = 255 (Nässe, „kein Gras“),
- Wasserspiegel-Karte (Gras nur über dem Spiegel).

Folge: Um Talkaskade und Kiesbett lag ein 25–35 m breiter kahler Streifen. Lokal behoben mit `scripts/swr/altwasser_reinigen_p2.py`:
- Dichten aus der natürlichen Umgebung aufgefüllt (17 094 + 915 Zellen).
- `karte_wasser` nach der Bachdekor-Regel aus dem p2-Wasser neu gerechnet.
- Spiegel ohne die alten Flüsse, mit p2-Wasser.
- Danach Texturen und Gras-Karten neu gebaut.

`wasser_welt.json` führt die drei Flüsse noch. Bitte in euren Planern als „ersetzt durch Erlenbach p2“ behandeln.

**Frage A:** Im alten Flussbett liegen weiterhin Bodenlagen **Kies/Geröll** (Ufer der alten Flüsse):

| Abschnitt | 6–12 m vom p2-Bett | 12–20 m | 20–30 m |
|---|---|---|---|
| Talkaskade | Kies 22, Geröll 20, Fels 9, Felsplatte 9, Moos 21 | Trockengras 27, Wiese 23, Moos 18, Heide 13, Kies 3 | Heide 27, Wiese 25, Trockengras 20 |
| Kiesbett | Wiese 24, Kies 22, Heide 21 | Kies 26, Wiese 23 | Kies 40, Trockengras 18 |

Sollen diese Streifen als **trockenes Schotterbett** bleiben oder wie die Umgebung werden? Wenn ja: mit welcher Mischung?
Technisch geht beides. Wir würden die Lagen über die bewährte Kette schreiben (`s38 lagen`).

## 3. Befund B: Das Wasser verdeckt das steinige Bett (Material)

- **Ohne Wasser** (rechts in `tk_mit_ohne_wasser.jpg`) sieht man Bachsteine, Geröll und nassen Kies.
- **Mit Wasser** (links) liegt darüber eine goldbraune, milchige Fläche. Die Steine verschwimmen, es bleiben helle Flecken.
- **Gesucht:** klares Wasser mit sichtbarem Grund (16f §4: Becken 1,5 m, Grund bei 1 m deutlich).

Material im Spiel: `MI_EL_SWR_Klar` → `MI_Eldarien_Wasser_Fluss` → `MI_Eldarien_Wasser_Basis` → Master `M_Eldarien_Wasser_Schaum8`
(unsere Kopie des Epic-Wassermaterials). Heutige Werte:

| Parameter | Wert | Einheit (lokal bestimmt) |
|---|---|---|
| Absorption | (400, 900, 750, 8) | RGB = **Sichtweite in cm** je Farbe (je größer, desto klarer); A unbekannt |
| Scattering | (0,2; 0,3; 0,28; 0,1) | RGB = Streufarbe, **A = Stärke** |
| Water Albedo | (0,03; 0,03; 0,03; 0,5) | |
| Refraction / Refraction Far | 1,15 / 1,02 | |
| Water Roughness / Specular | 0,02 / 0,225 | |
| Foam Opacity / Foam Boost / Foam powr / SimFoam Contrast | 0,5 / 0,8 / 0,6 / 12 | |
| Sim Velocity Normal Strength / Fluidsim Normal Strength | 40 / 1 | |
| ELD_*-Schaum (eigener DF-Schaum) | ELD_Fels_Schaum 0, ELD_DF_Schaum 1,15, ELD_Strom_Schaum 0,8, ELD_Ufer_Schaum 0,5, ELD_Schaum_Deckkraft 1 | |

Die Absorption (400, 900, 750) habe ich am 12.10. abends selbst als „Variante A, klar-grünlich“ gewählt, damals über dunklem Bett.
Über hellem Kies wirkt sie gelblich. 16a riet zu (250, 1430, 2000). 16f (0,45; 0,10; 0,08) je m entspricht als Sichtweite
(222, 1000, 1250) cm.

**Wichtig für 16f §3.2 und §4:** Unser Master hat diese Parameter **nicht**:
- `FoamAttenMin/Max`, `LowVelocityFoamScale`,
- Scattering Min/Max Velocity, Low Velocity Wave Scale, Wave Atten Min/Max.

Sie gehören zu Epics Baked-Sim-Material. Im Spiel (Render State WCBS) zeichnet aber der Water Body mit unserem Master.

Die vollständige Parameterliste steht in `bilder/swr_p2/mi_el_swr_klar_parameter.txt`.

**Frage B:**
1. Welche Werte für unsere vorhandenen Parameter? Ziel: Grund sichtbar, kein Goldton, leichter Grünstich in tiefen Becken, Weißwasser nur an Stufen.
2. Lohnt es sich, `FoamAtten` und Velocity-Scattering in unseren Master nachzubauen? Wenn ja: Knotenplan in Worten (wir bauen es als Kopie
   mit wenigen Knoten).

Lokal teste ich vorab drei Varianten (heute A, 16a, 16f umgerechnet) mit Bildern. Ergebnis folgt im Nachtrag.

## 4. Befund C: Uferform der Talkaskade (Gestaltung)

- Das Plugin-Bett (Kasten-U, Uferauslauf 1,5 m) schneidet in der Talkaskade 0,5–1,5 m tief in den Hang.
- Die Schnittkanten sind steil und kahl.
- Ihre Farbe kommt aus den Lagen Kies, Geröll, Fels und Felsplatte. Ab 38° Neigung legen sich die V17-Schichtbänder (ocker/rötlich) darüber.
- Aus 5 m Höhe wirkt die Kaskade wie eine **Treppe aus sandigen Kästen** (`p2x_bogen.jpg` Bild 4, `tk_mit_ohne_wasser.jpg` Zeile 2).

**Frage C:** Regeln für die Ufer einer Witcher-Talkaskade, so konkret, dass wir sie umsetzen können:
1. Profil: flacher auslaufen (anderer Uferauslauf, Kurve) oder steil lassen?
2. Lagen auf steilen Uferflächen: welche Mischung? Sollen die Schichtbänder dort aus sein (z. B. erst ab 3 m Wandhöhe)?
3. Bewuchs an der Kante: überhängendes Gras, Moospolster, Wurzeln?
4. Steine: halb eingegrabene Ufersteine an Außenkurven und Stufen?

Bitte Zahlen (Abstände, Anteile, Größen), wie in den Bachdekor-Regeln.
