# Auftrag 23i – T23-0 Fassung 2 bestanden, Spiegeln nur eingeschränkt brauchbar, Planer-Neulauf C2 nicht abgenommen

Stand 19.10.2026, 12:30 PC-Uhr. Bezug: 23d–23h, Regeln 23.10 lokal `regeln_23j_d659d753`. Alle drei Teile wurden unabhängig nachgeprüft.

## 1. T23-0 Fassung 2 im Testlevel: bestanden (Messweg im Editor belegt)

Werkzeuge r003 (Testlevel, K31-Sattel, K32, K10, Stufe B mit 23.7, Regeln 23.8 mit voller SHA), eingebaut 10:53.

- **K31:** Collision Mip 0, 40 von 40 Linientests treffen, Abweichung 0,0 cm. Die Proben unterscheiden die drei Modelle eindeutig: **Ergebnis = unsere
  Diagonale (i,j)–(i+1,j+1), `projektmodell_passt True`**.
- **Auswertung:** erfolg True, 17 Fälle Stufe A, 8 Fälle Stufe B, 0 Abweichungen, 0 ohne Linientreffer, 0 außer Toleranz. Stufe B ≠ A bei K3/K4/K9/K16
  war so erwartet.
- Bild K8: `SM_SmallStonesPack_01` sieht im Testlevel aus wie **ein einzelner Stein**. Das stützt den Befund aus 23h; eure Haufen-Regel nach Form
  (23.10) rechnen wir als Nächstes an den Dreiecken.

## 2. T23b-S (Spiegeln), Augenschein aller Bögen

Varianten A (Original), B/C (gespiegelt X/Y), D (nicht gespiegelt). V1 = Nanite an, V0 = Nanite aus (Rückfallweg).

| Netz | Akteur V1 | Akteur V0 | Foliage V1 | Foliage V0 |
|---|---|---|---|---|
| `LargeFallenTree_01` (Nanite) | ok | ok | ok | **B/C hohl** (Rückseiten) |
| `stone_09` (kein Nanite) | ok | ok | **B/C fast unsichtbar** (nur ein dünner Bogen) | **B/C fast unsichtbar** |

- **Kollision** der gespiegelten Varianten: komplex überall bestanden. Einfach: `stone_09` bestanden; bei `LargeFallenTree` „nicht prüfbar“, weil das
  Netz keine einfache Kollision hat.
- **Folge:** Gespiegelte **Foliage-Instanzen** zeichnen nur über den Nanite-Weg richtig. Nicht-Nanite-Netze und der Nanite-Rückfallweg zeigen die
  Rückseiten. **Akteure** sind in allen Fällen richtig.
- Bilder: `bilder/platzierung/t23/t23b_spiegel_boegen_1.jpg` (Zeilen: stone_09 Akteur V1, Baum Akteur V1, stone_09 Foliage V0, Baum Foliage V0) und
  `_2.jpg` (stone_09 Foliage V1, Baum Foliage V1, stone_09 Akteur V0, Baum Akteur V0); T23-0: `t23_0_kontrollfaelle.jpg`.
- Die Persistenz nach Neustart wird gerade geprüft und folgt als Nachtrag.

## 3. Planer-Neulauf C2 Talkaskade (Plan-Modus, Regeln 23.7, Zonen T6N1_0, Eckpunkt-Hüllen)

Ergebnis: **nicht abgenommen**, nur Kriterium b (Zonenziele) verfehlt. Alle anderen Kriterien bestehen:
- Sitz 23.7: 0 FEHLER bei 1 230 neuen, 31 veränderten und 2 917 unveränderten Stücken;
- 23.2 und 23.3 ohne FEHLER;
- Überlappung und Kleinzeug in den Grenzen;
- Bettzellen kollisionsfrei;
- Anteil ≥ 1 m an der neuen Netzfläche 0,878;
- Gegenrechnung T6N1_2 ≤ 0,014.

| Zone | Netz l / r | sichtbar l / r | Ziel | Ende |
|---|---|---|---|---|
| Kante | 0,42 / 0,42 | 0,77 / 0,77 | Netz ≥ 0,50, sichtbar ≥ 0,85 | Abbruch bei 520 Stücken (2 × 260) |
| Ufer | 0,39 / 0,36 | 0,74 / 0,71 | ≥ 0,40 / ≥ 0,75 | Abbruch bei 60 Stücken (2 × 30) |
| Hang | 0,22 / 0,21 | – | Netz ≥ 0,25 | keine Plätze mehr (300 Fehlversuche in Folge) |

- **Kante:** Blöcke ≥ 1 m passen fast nie, ohne Wasser- oder Bettzellen zu berühren. Erlaubte Saumsteine bringen netto ≈ 0,08 m² je Stück. Das Ziel
  bräuchte ≈ 960 Stücke (3,7 × 260).
- **Hang:** 676 Stücke gesetzt. Weitere Plätze scheitern an Durchdringung mit Altbestand und an Pflanzen unter dem Stein.
- Mit den Eckpunkt-Hüllen fielen die großen r001-Stapelfelsen unter 23.7 fast alle durch. Die Hang-Deckung sank dadurch vor der Ergänzung von 0,11 auf
  0,04.
- **Nachprüfer-Mängel** (vor jedem Pilot zu beheben):
  - M1: 1 105 Wasser-Stücke stünden auf der r001-Lage statt der Weltlage (Versatz bis 1,2 m, Drehung bis 72°).
  - M2: In den neuen Typen fehlen Material-Overrides (u. a. Fab-Raw `wk2oaeyqx`, das ohne Override weiß rendert).
  - Gesetzt wird nichts.

## 4. Fragen

1. **Kante:** Das Ziel ist mit Stücken an Land nicht erreichbar, weil die Kante zum großen Teil an Wasser und Bettzellen grenzt. Ziel senken, die Kante
   über Lage/Saum statt Netze erfüllen, oder bis zum 16h-Bettschritt warten (Steine im Wasser, neuer Bake)?
2. **Hang:** Darf Bewuchs oder Altbestand weichen (Pflanzen unter geplanten Blöcken, alte Stücke mit Sitz-FEHLER), damit Blöcke ≥ 1 m Platz finden?
3. **Neulauf mit 23.10:** Mit Wandmodulen ohne `durchdringung`, Dreiecks-Hüllen und Bezugsfläche S (23.9) dürften mehr Altbestand-Felsen bleiben und
   mehr Hangplätze frei werden. Neulauf erst nach eurer Antwort zu 1/2, oder sofort?
4. **Spiegeln:**
   - Gilt Spiegeln gegen Wiederholung künftig nur für Akteure und für Nanite-Foliage?
   - Oder ganz ohne Foliage-Spiegeln, weil der Rückfallweg (V0) auch bei Nanite-Netzen hohl zeichnet?
   - Was ersetzt es für Nicht-Nanite-Foliage: Drehung, Netztausch, Maßstabsvarianz?
5. **Wasser-Stücke (M1):** r001-Lage oder Weltlage beibehalten? Kollision in Bettzellen nach Mitte oder Grundriss prüfen?
