# Korrektur Runde 4 zu Auftrag 11: Meer fehlt in der Wassermaske (10.10. 21:40 lokal)

Projekt Eldarien, UE 5.8.3. Priorität **hoch** (betrifft alle Planer). Bilder `bilder/biom2/` (B7, J6: Bäume und Sträucher stehen im flachen Meer).

**Ursache:** `karte_wasser.r8` enthält nur Süßwasser (Flüsse, Seen, Bäche, Teiche) – das **Meer nicht** (Stichprobe: 0,2 % der Zellen unter −2 m
sind dort markiert). `FORMAT.md` §2 hatte es falsch beschrieben, Entschuldigung. Die Planer setzen deshalb auf den Meeresboden: gemessen in den
gesetzten Plänen `mittelschicht` A5 96 % der Instanzen unter 0 m, `aue` 51 % (176 k), `wueste_ergaenzung` 20 %, `spuren` A5 39 %; `nordkueste`
bis 4 664 je Feld.

**Bitte in allen 12 Planern:** Meer = `hoehe.f32 < 0,0` UND `karte_wasser == 0` (Meeresspiegel = 0 m). Dort nichts setzen; an der Küste nur die
Rollen `wasserkante`/`strand` bis 0,3 m Höhe, darunter nichts (Ausnahme: ausdrücklich Meeres-Rollen wie Tang/Muscheln am Strand, falls gewünscht,
nur zwischen −0,3 und +0,3 m). Lokal habe ich vorläufig gefiltert (`scripts/cloud_skripte/meer_filter.py`, 314 322 Instanzen aus 61 Feld-Plänen
entfernt); nach eurer Korrektur rechne ich neu und vergleiche die Zahlen. `FORMAT.md` korrigiere ich.
