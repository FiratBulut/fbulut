# Korrektur Runde 2 zu Auftrag 11 (erste Bilder im Editor, 10.10. 18:15 lokal)

Projekt Eldarien, UE 5.8.3. Priorität hoch. Runde 1 ist angekommen: alle 12 Planer laufen lokal auf Echtdaten, die Biom-Zuständigkeit stimmt
(z. B. Dschungel im Sumpf-Feld H5 23 716 → 2 587, Elfenwald in C6-Lava 5 875 → 0, Elfenwald G4 86 811 → 17 097). Danke.

**Erste Probe im Editor** (17:13): `felsgruppen`, `mittelschicht`, `spuren` in A5 und G4 gesetzt. Bilder in `bilder/cloud1/`
(Vorher: `FELS8_A5_rundgang.jpg`, `HEUTE1_G4_hain1.jpg`; Nachher: `CLOUD1_*`; Nahaufnahme der Probleme: `V17TEST_A5_rundgang.jpg`, Mitte rechts).

| Ebene | A5 | G4 |
|---|---|---|
| felsgruppen | 12 785 Instanzen + 53 Akteure | 1 189 |
| mittelschicht | 30 915 | 20 371 |
| spuren | 1 050 | 1 133 + 19 Akteure |

## Befund

1. **Mittelschicht wirkt** (G4, `CLOUD1_G4_hain1` gegen `HEUTE1_G4_hain1`): Jungbäume und Sträucher unter den Kiefern, das Bild ist geschichteter.
   Bitte so lassen; in Sichtachsen von Lichtungen etwas lichter, damit Blickziele frei bleiben.
2. **Felsgruppen in A5 lesen sich nicht als Felsgruppen** (`CLOUD1_A5_rundgang`, Blick von ~300 m auf den Bergrücken): Aus der Entfernung sieht man
   nur verstreute Einzelpunkte und **flache helle Platten wie Pappe auf dem Gras**. Kein Grat bekommt eine sichtbare Felskrone, kein Hangfuß einen
   Blockstrom. Witcher-Maßstab: eine Gruppe muss auf 300 m als Form erkennbar sein (Hauptfels 4–10 m, mehrere Blöcke 1,5–4 m eng gestaffelt, die Gruppe
   10–30 m breit), dafür deutlich weniger Gruppen. Bitte:
   - Gruppengröße und Hauptfels-Maßstab anheben (Hero 4–10 m an Graten/Kuppen, Skalierung erlaubt bis 2,5 bei Megascans-Felsen), Anzahl der Gruppen je Feld
     halbieren; Satelliten eng (Abstand ≤ 1,5 × Hauptfels-Radius), nicht verstreut.
   - **Flache „RockyGround“-/Platten-Netze** (`SM_ErodedRockyGround_*`, `SM_NordicBeachRockyGround_*`, `SM_TundraRockyGround_01`, `SM_flat_rock_0*`) nur noch
     auf Kies-/Geröll-/Fels-Lagen (`lage_Kies`, `lage_Geroell`, `lage_Fels`, `lage_Felsplatte` ≥ 100 von 255), tiefer eingraben (≥ 50 % der Netzhöhe),
     an der Normale ausgerichtet, nie einzeln auf Gras/Wiese.
   - Kleinmaterial (Kiesel, Steine < 0,5 m) bleibt um die Gruppen, aber nicht als Teppich über ganze Hänge.
3. **Materialien** (lokal gelöst, nur zur Info): Megascans-Netze rendern hier mit ihrem Originalmaterial schwarz; ich lege für alle 245 Megascans-Netze
   eurer Pläne Ersatz-Instanzen an. Zwei Netze sind **gesperrt**, bitte aus allen Paletten entfernen: `/Game/AncientRuins/Meshes/SM_Column_03`,
   `/Game/AncientRuins/Meshes/SM_Main_Arch_01` (leere Grundfarbtextur → weiß). Eine Prüfung aller Netze eurer A5/G4-Pläne liegt in
   `vorlagen/daten/netz_check_ergebnis.json` (`klasse`: ok / schwarz_mspresets / textur_leer).
4. **Spuren**: in A5 nur 51 → 1 050 Objekte, gut sichtbar sind sie nicht. Bitte je Feld 1–3 größere Spuren-Ensembles an Wegen/Orten (Wegkreuz + Zaunstück +
   Holzstapel, Steinmauer-Rest mit Steinmann), statt vieler Einzelteile.

## Lieferung

Gleiche Dateinamen in `antworten/skripte/` (felsgruppen, spuren; Biom-Planer nur, wenn sie Platten/Felsen verteilen), kurzer Abschnitt „Runde 2“ in
`verteilung-STATUS.md`. Ich teste wieder lokal auf A5/G4 und setze A5 neu.
