# Auftrag 13k – Pilot 2 gebaut (bergwald_03 Säulenhain + bergwald_06 Karsee): Bildbefund; Nachtrag zu 15g

Stand 12.10.2026, 11:25. Gebaut mit eurem Stand 13f/13g/13j (1 m, Treppenbäche mit `wasser_koerper` + `quer` über das A15-Werkzeug). Alle Schritte liefen
ohne FEHLER durch (Gelände B5/C5, See, 3 Treppenbäche, 5 712 Instanzen, 49 Akteure, 18 Effekte). Bilder:
[`bilder/sehens_p2/pilot2_vorher_nachher.jpg`](../bilder/sehens_p2/pilot2_vorher_nachher.jpg) (links vorher, rechts nachher),
[`bilder/sehens_p2/pilot2_baeche.jpg`](../bilder/sehens_p2/pilot2_baeche.jpg) (Treppenbäche: vorher | Schaum 1,0 | Schaum 0,35 | 0,35 mit Vorhängen),
[`bilder/sehens_p2/pilot2_see.jpg`](../bilder/sehens_p2/pilot2_see.jpg) (See: Schaum 1,0 | 0,35 + Vorhänge | Seefarbe gedämpft).

## Zuerst ein Fehler von uns (betrifft auch 15g)

Der Materialschritt im C2-Auftrag hat die Instanz `MI_EL_Kaskade_SLW` beim erneuten Lauf auf ihre Startwerte zurückgesetzt: `Schaum_Menge` 1,0 statt
der in 15g genannten 0,15. **Die Bilder in 15g (C2 Version 2) und die ersten Bilder des Pilots liefen also mit vollem Schaum.** Behoben (Abstimmungsdatei),
jetzt 0,35 / 0,35. Neue C2-Bilder mit 0,35: [`bilder/gefaelle_c2/c2_v2_schaum035.jpg`](../bilder/gefaelle_c2/c2_v2_schaum035.jpg) (links 1,0, rechts 0,35).
Ergebnis: Die weißen Streifen an den Lippen sind weg (`kn0_oben`), die Fallflächen zeigen Struktur statt Weiß (`kn0_nah_s63`). Punkt 1 aus 15g ist
damit schwächer, aber nicht erledigt. **Unverändert bleiben die Becken: grün, deckend, mit geraden Rändern** (`kn0_nah_s119`, `kn0_unten`) – Punkte 2
und 3 aus 15g sind jetzt die wichtigsten.

## Was gut ist

1. **Säulenhain aus dem Anmarsch (`_anmarsch`, C5):** als dunkle, hohe Gruppe klar lesbar gegen die helleren Kiefern – Befund 5/6 aus 13h umgesetzt.
2. **Säulenhain nah:** graue Stämme wie Säulen unter einem dichten Dach – der Hallenwald-Eindruck stimmt.
3. **Karsee:** nicht mehr schwarz, Insel und Becken lesbar; alle drei Treppenbäche sind von Ufer zu Ufer nass (der A15-Weg funktioniert für Sehens-Bäche).

## Was nicht stimmt

1. **Gesägte Stammstücke als „kleinholz“:** `SM_Forest_pine_04_01_log` (449) und `SM_Forest_pine_04_02_log` (472) in bergwald_03 sind 1,25 m lange,
   25 cm dicke, **gesägte** Stücke (Schnittflächen-Material `MI_Pine_lods_ends`). 921 davon unter dem Hain sehen aus wie ein Holzlager (`_nah`).
   Regel bitte: Netze mit Sägeschnitt (`*_log` aus `Mountain_Environment_Set/Details`, Material mit `ends`) nie in Wildnis, nur an Lagern, Holzfällerplätzen,
   Wegen. Kleinholz in wilden Wäldern = Äste (`SM_detail_branches_*`, `SM_OldTreeBranch_*`), Zapfen, Rinde; Totholz = wenige große liegende Stämme
   (`SM_OldFallenTree_*`), in Gruppen unter abgestorbenen Bäumen, hangparallel. Richtwert Altwald: 1–3 liegende Stämme und 5–15 Äste je 100 m², nicht
   gleichmäßig.
2. **Waldboden unter dem Hain einförmig:** eine helle Pflanzenart gleichmäßig verteilt, dazwischen kahler Boden. Witcher-Regel „4–6 Schichten“: Moospolster
   in Flecken, Farne in Gruppen (3–7), Heidelbeer-Inseln, bemooste Steine und Wurzeln. Bitte auch prüfen, ob die Lage unter dem Hain das Landschaftsgras
   dämpft (Nadelstreu).
3. **`_fern`-Kamera des Säulenhains** (660 m südlich) steht selbst im Wald: Vordergrund-Kiefern verdecken den Hain (Bild vorher = nachher). Bitte Kameras auf
   freie Sichtachse prüfen (Gelände UND Baumkronen; z. B. Lichtung oder Gegenhang). Die Frage `Fir_07` auf 570 m (13j Punkt 2) kann ich erst damit beantworten.
4. **Karsee-Rückwand (`_nah`):** weiter glatt mit senkrechten Streifen (gestreckte Landschaftstextur auf > 60°) – der Steinbruch-Eindruck bleibt an dieser
   Wand. Verkleidung bitte bis zur Oberkante, mit Schuttkegel am Fuß.
5. **Seefarbe `tiefblau`:** wirkt in einem Hochkar wie ein Schwimmbad. Lokal gedämpft getestet (Absorption 8/40/160, Streuung 0,06/0,20/0,45):
   kaum Unterschied (Tiefe etwas dunkler, Ränder weiter leuchtend cyan). Vorschlag: eigene Farbe `bergsee` (dunkles Blaugrün) für Kar- und Bergseen; `tiefblau` nur für Quelltöpfe.
6. **Treppenbäche – Schaummenge im Plan:** In `quer` haben 78–86 % der Einträge Schaum > 0,5 (C2: 16 %), Deckung überall 1,0. Damit ist fast der ganze Bach
   Weißwasser. Wunsch: in Becken und Gumpen klares Wasser (Schaum ≤ 0,2), Schaum am Fallfuß mit Abklingen über 2–4 m, an Lippen und Zungen; steile Flächen
   nicht pauschal 1,0 (die Fall-Optik macht lokal das Material, `M_EL_Kaskade_SLW2` mit Fallstreifen ist in Arbeit).
7. **Vorhänge (Stufen ≥ 3 m, 7 Stück, lokal gebaut):** Der 10,8-m-Fall S00 zeigt von oben echte Wasserstreifen (besser). Von unten bleibt er ein
   flaches, helles Rechteck mit geraden Kanten; die Vorhänge der kleinen Stufen in `zulauf_sued` wirken wie zerknitterte Folie. Die Form der Vorhänge
   verbessere ich lokal (schmaler Strahl statt ganzer Lippenbreite, ausgefranste Ränder, unten in Gischt auslaufend). Von euch bitte: an Stufen
   ≥ 3 m `cull_m` der Aufprall-Effekte 60–80 m statt 20 m (`NS_Impact_Small` ist aus 30 m und mehr sonst unsichtbar), und die Strahlbreite je Stufe
   (`strahl_breite_m`), wenn das Wasser nur einen Teil der Lippe nutzt.

## Nächste Schritte lokal

`M_EL_Kaskade_SLW2` (Tiefe/Deckung aus UV1, Schaum mit Strömungsstruktur, Fallstreifen auf steilen Flächen) bauen und an C2 + Karsee testen. Danach
Pilot 2 mit eurer Korrektur neu (Rückbau-Werkzeug vorhanden).

## Nachtrag 11:45 – Seefarbe und Antworten auf eure Rückfragen zu 15g

**Seefarbe:** Vier Varianten am Karsee: [`bilder/sehens_p2/pilot2_seefarben.jpg`](../bilder/sehens_p2/pilot2_seefarben.jpg) (tiefblau aus dem
Plan | gedämpft | B dunkelblau | **C dunkles Blaugrün**). C wirkt wie ein echter Bergsee und ist jetzt lokal am Karsee gesetzt. Bitte eine eigene Farbe
**`bergsee`** in `FARBEN` aufnehmen (Werte im Format von `wasserfarben.json`, Master `M_Eldarien_Wasser_Schaum8`: Absorption 8 / 45 / 40 / 8,
Scattering 0,06 / 0,22 / 0,14 / 0,08, Albedo 0,35, Rauheit 0,015) und für Kar- und Bergseen nehmen; `tiefblau` nur für Quelltöpfe.

**Zu euren Rückfragen in der 15g-Antwort:**
1. **Opacity:** Im bisherigen `M_EL_Kaskade_SLW` kommt Opacity schon nur aus dem Schaum, nicht aus der Deckung. Das deckende Grün hat eine andere
   Ursache: Das Material gibt 1/Absorption der Fluss-Instanz als Koeffizient aus (24/48/40 cm → 0,042/0,021/0,025 je cm = 4,2/2,1/2,5 je m), also
   10- bis 50-mal mehr als eure Werte (0,40/0,07/0,05 je m). Bei 1,5 m Tiefe ist dort fast alles Licht geschluckt. `M_EL_Kaskade_SLW2` wird gerade
   gebaut: eure Werte je m, dazu ein Skalierungsparameter (Start 0,01 = je cm), Deckung auf Specular und Normalstärke.
2. **Einheit:** bestätige ich mit den ersten SLW2-Bildern (Ziel: Rot bei 1,5 m auf ~55 %).
3. **Buchten C2:** erst einmal eure Standardwerte. Ich baue C2 jetzt als Version 3 mit eurem Plan `0e00d17` (Rückbau von Version 2 läuft) und melde
   nach den Bildern, ob mehr Unruhe nötig ist.

## Nachtrag 12:35 – Einheit der SLW-Koeffizienten geklärt

`M_EL_Kaskade_SLW2` ist gebaut (Opacity nur aus Schaum, eure Werte aus 15g §2.2, Deckung → Specular/Normalstärke) und hängt an allen
Kaskadennetzen. Test am Karsee: [`bilder/sehens_p2/pilot2_slw2_einheit.jpg`](../bilder/sehens_p2/pilot2_slw2_einheit.jpg) (Spalten: altes Material
Schaum 0,35 | mit Vorhängen | SLW2 mit Werten je m × 0,01 | SLW2 mit Werten je m × 1,0). Mit × 1,0 leuchtet schon 20–30 cm tiefes Wasser knallig
türkis, mit × 0,01 bleibt es klar. **UE 5.8 rechnet die SLW-Koeffizienten also je cm**; eure Werte je m gelten mit Faktor 0,01. Der eigentliche Test mit
tiefen Gumpen kommt mit C2 Version 3 (Plan 0e00d17, wird gerade gebaut).
