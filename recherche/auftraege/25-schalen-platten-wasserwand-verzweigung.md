# Auftrag 25 – Offene Schalen-Netze, große Platten (PG1), Wasserwände an SWR-Stufen, Erlenbach-Verzweigung

Stand 27.10.2026 05:50. Bezug: 23.10 `offene_netze` (Antwort 23h §4), 23.11/23.12 (Kragarm), 24 §3/§7/§9, 16h-6n/6p (smoothing 1, K-Kolk).

## Kontext (Ferat 26.10. abends, Bilder C2-Talkaskade)

- Ferat: „flache, innen hohle Steine – eine Seite Stein-Textur, die andere hohl“; „Kiesel sind flach und müssen am Boden kleben, ein Teil sichtbar,
  ein wenig in der Erde“; „4 identische Steine nebeneinander sehen nicht natürlich aus“; Platten liegen wie Dachziegel, eine als Brett über dem Wasser;
  dünne weiße Striche im Bach; grünes „Glas“ mit senkrechten Wänden an den Stufen.
- Ferat ab 26.10.: Tempo vor Absicherung, der PM entscheidet knappe Fälle selbst; die Cloud wird danach informiert. Alles unten Entschiedene läuft
  schon – bitte bestätigen oder korrigieren, dann ziehen wir nach.

## A. Offene Schalen-Netze (lokal: `schalen_offen/r001`)

Befund: 122 von 269 Sitzklassen-Netzen sind offene Schalen (113 nach lokal −Z offen, 9 Wandmodule hinten offen), 10 teiloffen; 216 259 Instanzen,
davon nach Schätzung 36 525 sichtbar falsch (Rand > 3 cm über dem Boden bzw. Öffnung seitlich/oben). Regel so-r001: Öffnung gegen die Auflage-Normale
(o·n ≤ −0,7), dicke Schalen (≥ 10 cm entlang der Öffnung): jeder offene Randpunkt ≤ −2 cm unter Gelände/Träger.
Umgesetzt: Pilot C2 573, Stufe 1 G4/H4/B4 3 841 (gespeichert, nach Neuladen bestätigt); Stufe 2 (24 Felder) ist eingereiht.

1. **Dünne Schalen (2–10 cm, z. B. `SM_stone_04` 3,6 cm):** PM-Entscheid: Öffnung nach unten + Rand ≤ **+1 cm** über dem Boden (kein sichtbarer Spalt)
   genügt, statt −2 cm (das ginge nur durch Vergraben). Richtig?
2. **Spalt ≤ 3 cm** bei richtiger Öffnung (36 067 Instanzen): nur melden oder auch reparieren?
3. **Wurzeln/Stümpfe** mit offener Unterseite (11 339 bzw. 7 120 sichtbar): gilt 23.10 gleich? Lokal werden sie nie entfernt, nur gemeldet.
4. **Kulisse ≥ 15 m / Wandmodule 4–15 m** mit frei hängendem Rand (drehen verboten nach 23.7): Felsfuß/Haldenblock davorsetzen oder nur melden?
5. **Netztausch** statt Entfernen (geschlossenes Netz gleicher Familie/Form, ±20 %): freigeben? Ziel-Typ lokal per Typ-Lesung je Feld (wie A/PG1 §B.4).

## B. Große Platten ≥ 2 m (lokal: `platten_gross/r001`, Regel PG1)

Weltzählung: 8 342 Platten ≥ 2 m (22 Netze, 47 Felder), **3 587 FEHLER** in 41 Feldern. 21 von 22 Plattennetzen sind offene Schalen.
Gründe (Mehrfachnennung): Steilhang > 35° und L > 3 m 2 626 (davon 1 795 nur deswegen, sonst gut sitzend), offener Rand über dem Boden 1 684,
Neigung > 10° gegen die Geländenormale 973, Kragarm (23.12) 325, Einbettung < 30 % 288, quer im Bach 27. Klassen: Dachziegel 723, hochkant 255,
Brett über Wasser 4, im Wasser 335. Je Feld: B5 624, B4 383, H3 362, I4 326, H4 250 …

PG1 (PM-Annahmen in Klammern): hangparallel ≤ 10°; eingebettet ≥ 30 % der Dicke; offener Rand ≤ 5 % der Randpunkte nicht ≥ 2 cm unter dem Boden
(Annahme statt „jeder Punkt“); Kragarm nach 23.12 (< 10 % des Grundrisses mit > 30 cm Luft); **Hang > 35° → keine Platte > 3 m** (verkleinern ≤ 3 m,
sonst durch Block gleicher Typ-Eigenschaften ersetzen, sonst entfernen); im Wasser lange Achse ≤ 45° zur Strömung. 23.3 „Hero ≥ 2 m bleibt“ und
23 §6 „Hindernis nur z/Drehung“ gelten für PG1 nicht (SWR-Nacharbeit danach). Geometrische Ausbiss-Reihen (121) werden nicht ausgenommen.

6. **Steilhang-Regel:** Sollen die 1 795 sonst gut sitzenden langen Platten am Steilhang auch ersetzt werden (S3 Bergfelder: 2 068 statt 547 Entfernungen),
   oder nur die mit weiterem Fehler (`--nur-steil-mit-fehler`)? PM-Plan: Berg-Stufe S3 nur mit weiterem Fehler, bis ihr antwortet.
7. Rand-Toleranz 5 % ok? Ausbiss-Reihen wirklich nicht ausnehmen (Ferats „Dachziegel“ sind genau solche gleich geneigten Reihen)?

## C. Wasserwände an den Stufen der gebackenen SWR (lokal: `wasser/wasserwand/r001`)

Belegt (Leseproben im Editor, Dump-Auswertung):
- In BAKED_SIM zeichnet **nur** Epics Niagara-Komponente `Grid2D_SW_River` mit `SW_Water_Material_River_Niagara_Cached` (Streuung 0,77/1/0,92,
  Absorption 20,8/25/24,7, Albedo 0,083, Schaumfarbe grün 0,39/0,76/0,56). Unsere Wasserkörper sind unsichtbar; `MI_EL_SWR_Klar` wirkt gebacken nicht.
  Python kommt an das Renderer-Material nicht heran.
- Das gebackene Höhenfeld macht aus jeder Stufe eine glatte Rampe von 30–63° (Zelle 36,7 cm, smoothing 1): in der Talkaskade 296 m² ≥ 30°, 125 m² ≥ 45°
  (smoothing 5: 179/25,5 m²). Gebackener Schaum an allen 51 Wandgruppen 0,0. Stufen: p2 86 (78 ≥ 0,8 m, Talkaskade-Median 1,40 m), UL 30 (21 ≥ 0,8 m).
- Lokaler Weg B (gebaut, Bildtest läuft heute): „Stufen-Haut“ = Netz 5–8 cm vor jeder gebackenen Fläche ≥ 30°, Material `MI_EL_Stufenfall_Schnelle`
  (oben durchsichtig, Wand weiß, Schaumschürze unten), 9 Netze / 26 585 Dreiecke, prozedural aus dem Dump; kein Neu-Simulieren.

8. **Weg A:** eigenes Material am Niagara-Renderer der gebackenen SWR (Kopie `Grid2D_SW_River` + Kopie des Epic-Masters `SW_Water_Material` mit
   Weißwasser über die Neigung (ddx/ddy der Weltposition) und eigenen Farben; Setzen per C++ in unserem Plugin). Empfehlenswert, oder gibt es einen
   Epic-Weg (Parameter, Benutzer-Material am SWR-Akteur, NiagaraDataInterface), den wir übersehen?
9. Stufen < 0,8 m: auch Haut, oder nur Schaum (gebacken ist er 0)? Wie viele `NS_Impact_Small`/`NS_Stream_Small` je Stufe (24 §9.1: höchstens 3 je Ort)?

## D. Erlenbach-Verzweigung im Kiesfächer C3 (lokal: `erlenbach2/b_plan/verzweigung_r1`, läuft heute)

Ferats Zeichnung: Hauptlauf bleibt durch die Mitte, dazu oberer Arm (p2 s 605 → Ost-Arm → UL s 148), unterer Arm (p2 s 671 → UL s 185) und Schleife um
eine Kiesinsel. Je Arm 2–3 m breit, 0,30 m tief, Gefälle 1,7–2,1 %, Kiesbank-Ufer 0,12–0,22 m, Abzweig-Schwelle 0,6 m (2 cm über dem gebackenen
Spiegel). Zwei neue SWR (O1 in Zone C2 4096; O2/U/S in Zone D3 2048, Zelle 0,18 m), Werte wie p2. Die „dunkle Pfütze“ (3 540 m²) ist gebackenes
p2-Wasser des 12 m breiten Ost-Arm-Bands; sie wird zugedeckt (Gelände auf gebackenen Spiegel + 7 cm, Median 0,31 m, max 1,23 m), p2/UL bleiben bitgleich.
Gelände: Abtrag 2 512 m³, Auftrag 1 531 m³ in C2/C3/D2/D3.

10. Ist „gebackenes Wasser mit Gelände zudecken“ statt p2 neu zu backen vertretbar, oder sollte der Ost-Arm schmaler werden und p2 neu gebacken werden
    (neue Referenz, neue K-Kolk-Abnahme)?
11. Abflussaufteilung ergibt sich nur aus Breite/Tiefe (Arme 0,35–0,5 B des Hauptlaufs). Passt das zu einem Sander/verzweigten Gletscherbach (24
    gletscher.verzweigt 0,3–0,6 B), oder braucht ein Arm mehr Gefälle/Breite, damit er nicht trocken wirkt?

Antwort bitte als `antworten/25-schalen-platten-wasserwand-verzweigung.md` (+ JSON-Patches für 23.x/24, falls Regeln sich ändern).
