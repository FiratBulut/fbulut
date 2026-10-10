# Antwort zu Korrektur Runde 2 (Auftrag 11)

Stand: 10.10.2026. Alle vier Befunde sind umgesetzt. Getestet ist nur synthetisch in der Cloud, nicht mit Echtdaten. Einzelstand:
`verteilung-STATUS.md`, Abschnitt „Runde 2“. Jeder geänderte Bericht hat einen Abschnitt „Korrektur Runde 2“.

## Kurzfazit

1. **Mittelschicht:** unverändert in der Wirkung. Neu ist nur, dass hohe Klassen in Sichtachsen lichter stehen. Gesamt G4 −0,6 %,
   im Sichtkorridor −30 %.
2. **Felsgruppen als Form:** neu aufgebaut. Weniger, größere Gruppen mit Hauptfels 4,5–8,5 m und eng gestaffelten Blöcken. Felskrone als
   Kette auf dem Grat, Blockstrom unter Wänden über 50°. Flache Platten nie mehr auf Gras. Kleinmaterial nur noch bis 2 m um Felsstücke.
3. **Gesperrte Netze:** `SM_Column_03` und `SM_Main_Arch_01` sind aus allen Paletten entfernt. felsgruppen, mittelschicht und spuren führen
   zusätzlich eine Sperrliste `gesperrt` und filtern alle Overrides damit. Ersatz: `SM_Column_02`, `SM_Wall_01`.
4. **Spuren:** je Feld 1–3 Ensembles mit 3–6 Teilen an Wegen und Orten. Verstreute Einzelteile stark reduziert.

## Was sich ändert

| Planer | Änderung | Synthetischer Test |
|---|---|---|
| felsgruppen | Hauptfels-Maßstab aus Zielhöhe durch Netzhöhe, bis 2,5 bei Megascans; 3–5 Satelliten 1,5–4 m im Abstand ≤ 1,5 × Hauptfels-Radius; Grat-Kette, Blockstrom; ganze Gruppen statt Satelliten ausgedünnt | A5-artig: Gruppen 2 381 → 515, Instanzen 39 802 → 10 696, Hauptfels Median 5,8 m, Gruppenbreite Median 24,7 m |
| felsgruppen | Platten nur auf `lage_Kies`/`Geroell`/`Fels`/`Felsplatte` ≥ 100 und nur wo Gras/Wiese nicht stärker ist; ≥ 50 % eingegraben, an der Normale | Platten auf Gras 691 → 0 (A5-artig), 817 → 0 (B4) |
| felsgruppen | Kleinmaterial < 0,5 m nur im 2-m-Kontaktsaum | Anteil außerhalb Saum 34 % → 0 % |
| Biom-Planer | dieselbe Platten-Regel, wo sie selbst Platten setzen; Kiesel nur auf Fels-/Geröll-Lagen, Wegen, Ufern | nordkueste Strandplatten 13 → 4, hochgebirge Schneeflecken 6 000 → 1 505, Kiesel-Teppich in vier Planern → 0 |
| Biom-Planer | Blöcke > 0,8 m an felsgruppen abgegeben | elfenwald `bachblock`, `uferfelsstufe`; lava `basaltsaeule` |
| spuren | Ensembles: Wegkreuz, Mauerrest mit Steinmann, Rastplatz, Ortsrand, Schrein, Ruinenrast; Anker Ortsrand, Kreuzung, Wegknick mit Aussicht; Standort mit freier Sicht bevorzugt | je 3 Ensembles in A5 und G4; Einzelteile A5 57 → 11, G4 40 → 12 |
| mittelschicht | Faktor 0,5 in Kegeln vom Weg zu Blickzielen und Lichtungsmitten, 0,6 am offenen Lichtungsrand, 0,5 um Ensembles | G4 45 408 → 45 139 |

Alle Läufe waren doppelt byteidentisch, die Logs reines ASCII, alle Skripte `py_compile`-sauber.

## Neue Reihenfolge beim Planen

lava, felsgruppen, übrige Biom-Planer, **spuren vor mittelschicht**. mittelschicht liest die Ensembles aus dem Spuren-Plan als Blickziele.
Die Reihenfolge beim Setzen bleibt: felsgruppen, Biom-Planer, mittelschicht, spuren. `assets-taxonomie.json` sollte lokal in `daten/`
liegen, sonst wählt spuren die Ensemble-Typen nur nach den Biomlisten.

## Bitte lokal prüfen

1. **A5 neu setzen** und die Prüfkamera `grat_300m` aus `felsgruppen/A5/plan.json` (`pruefkameras`) gegen `CLOUD1_A5_rundgang` halten.
2. **Gruppenzahl:** Sie sinkt auf 22–29 % statt auf 50 %. Wirkt der Grat zu leer, in `felsgruppen_regeln.json` `klassen.band.raster_m` oder
   `klassen.fuss.strom_abstand_m` verkleinern.
3. **Hauptfels:** höchstens etwa 7,6 m statt 10 m, wegen der Fußbreitengrenze von 14 m. Soll er größer werden, diese Grenze anheben.
4. **Ensembles:** Sie wirken auf 20–80 m vom Weg. Auf 300 m bleiben 1–2 m hohe Teile klein, das ist erwartet.
5. **Wüste und Lava** bekommen keine Ensembles; dort bleiben ihre eigenen Sonderformen.

## Offen

- Die Klasse `wand` (Kliffschalen) ist unverändert.
- Die Kammschwellen für die Grat-Kette sind nur synthetisch abgestimmt.
- Flache `MossyRocks`-Platten in lava `flechtenstein` und elfenwald `moosstein_bach` standen nicht auf der Liste und sind unverändert.
