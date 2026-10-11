# Auftrag 13h – Bildbefund erster Sehens-Pilot im Editor (Bergwald B5: Säulenhain + Karsee)

Stand 11.10.2026, 23:45. Der Pilot lief **technisch vollständig** durch: Gelände je Feld, Graskarten 0 Fehler, Karsee 586 m², 3 Fallvorhänge,
Houdini-Maske, Freihalten 465, 5 620 Instanzen und 29 Akteure, Material, 16 Effekte. Gerechnet wurde mit dem Planerstand **vor 13f**, mit lokalen
Übergangslösungen. Bilder: [`bilder/sehens_pilot1/`](../bilder/sehens_pilot1/). Im Vorher/Nachher-Bogen steht links vorher, rechts nachher.

**Gestalterisch ist das Ergebnis noch nicht gut.** Die Befunde gelten wohl auch für den Stand 13f, bitte prüfen:

## Karsee (bergwald_06)

1. **Senkrechte, glatte Erdwände.** Der Stempel (bis −10,6 m) schneidet die Karwand fast senkrecht aus dem Hang. Auf diesen Flächen zeigt das
   Landschaftsmaterial gestreckte, senkrechte Streifen (UV-Dehnung). Dazu kommt ein flacher, waagrechter Absatz. Der Eindruck ist **Steinbruch statt Kar**
   (Bilder `…karsee_anmarsch`, `…karsee_held`). Wunsch:
   - Neue Flächen steiler als ~45° nur dort, wo sie mit **Fels-Akteuren verkleidet** werden: Klippen- oder Wandnetze (Megascans Cliff, Basalt, Mountain-Wand)
     in Reihen, so wie bei den Uferklippen in A15. Sonst flacher stempeln (Schutthalde 30–35° mit Geröll-Lage und Blöcken).
   - Die Karwand ist natürlich gegliedert: Rinnen, Absätze, Schuttkegel am Fuß, Moos und Schneereste oben. Keine ebene Stufe.
   - Seeufer an der Auslaufseite flach (Schwelle aus Felsbuckeln), an der Rückwand steil mit Fels.
2. **Seefarbe `schwarz_spiegel`** in der tiefen, schattigen Mulde wirkt wie ein **schwarzes Loch/Schacht** (`…karsee_nah`). Vorschlag: `tiefblau`
   oder `smaragd` mit Spiegelung (echte Karseen sind klar und dunkelblau), oder die Mulde so öffnen, dass Himmel und Hang sich spiegeln.
3. Im See liegen um die Felsinsel grün-schwarz **gestreifte Formen** (`…karsee_nah`). Vermutlich ein Material- oder Netzfehler bei mir, lokal in Prüfung.
   Falls die Insel bzw. die Kiefer als Akteur unter dem Spiegel steckt: bitte Inselkrone ≥ 0,3 m über den Spiegel.

## Säulenhain (bergwald_03)

4. **Kamera `nah` steht in einer neuen Baumkrone** und zeigt nur Nadeln (`…saeulenhain_nah`). Bitte Kameras gegen die eigenen neuen Akteure prüfen:
   Abstand ≥ Kronenradius + 2 m und freie Sichtlinie.
5. **Aus der `fern`-Kamera (C4) ist kein Unterschied zu sehen.** Ein Leuchtfeuer muss aus 300–800 m als Silhouette lesbar sein: Riesentannen deutlich
   über dem Bestand (≥ 1,5 × Nachbarhöhe), Lichtung oder Saum davor, kein Bestand in der Sichtachse.
6. Aus `held` und `anmarsch` wirkt der Hain fast wie vorher: neue Tannen mischen sich in den Kiefernbestand. Wunsch: Kontrast zum Bestand, etwa reiner
   Riesentannen-Kern mit Säulenstämmen, Unterholz entfernt (Hallenwald), Lichtstreifen, Altholz am Boden.

## Allgemein für alle Planer

- Neue steile Geländeflächen nie ohne Verkleidung. Eine Prüfer-Regel wäre gut: Neigung nach dem Stempel > 45° auf > 20 m² ohne Fels-Akteur → FEHLER.
- Kameras: freie Sicht prüfen (Strahl gegen neue Akteure und Bestandsbäume), Leuchtfeuer aus der Fernkamera als Silhouette.

Lokal rechne ich als Nächstes mit 13f neu und baue nach eurer Antwort einen zweiten Pilot.

## Nachtrag 12.10. 01:00 – Ursache der grünen Streifen (Punkt 3)

Diagnose im Editor: Es ist kein Materialfehler. Zwei Felsblöcke des Plans liegen knapp **unter** dem Seespiegel (256,17 m), etwa 4 m vom Seemittelpunkt:
`SWBE_B5_023` (SM_MossyForestBoulder_04, Pivot 252,28 m) und `SWBE_B5_022` (SM_NordicBoulder_01 mit MI_EL_SW_Klammfels_Nass, Pivot 252,10 m).
Ihr helles Moos scheint durch das fast schwarze Wasser und wird von den Wellen in grelle Streifen gebrochen. Bitte Blöcke im See entweder deutlich über den Spiegel
(Inselkrone ≥ 0,3 m) oder tiefer als 1,5 m unter den Spiegel setzen, nie knapp darunter. Das gilt auch für die anderen Planer.
