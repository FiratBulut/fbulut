# Auftrag 13: Sehenswürdigkeiten neu – 8 je Biom, Witcher-Qualität (11.10.2026)

## Ferats Auftrag

- „Alle Sehenswürdigkeiten analysieren und organisch in die Welt setzen. Sie sollen Witcher-Qualität haben, mit vielen Details.“
- „Pro Biom passend **8 Sehenswürdigkeiten** ausdenken und planen und Claude alles Nötige zur Verfügung stellen.“
- „Houdini-Sachen auslassen, wir machen neu.“ → Die alten Houdini-Sehenswürdigkeiten werden ausgeblendet; nichts davon voraussetzen.
- „Ich kann viel mehr Asset-Pakete herunterladen – die Assets berücksichtigen. **Bevor Claude an den Sehenswürdigkeiten arbeitet, bekomme
  ich eine Liste, welche Pakete ich herunterladen soll.**“
- Seine Regel vom 02.10. gilt weiter: **nur Landschaft** – Fels, Wasser, Eis, Feuer, Pflanzen. Keine Ruinen, Bauten, Knochen, nichts von
  Menschenhand. Jeder Ort gehört geologisch und botanisch in sein Biom; keiner kommt in zwei Biomen gleich vor.
  Ideensammlung von damals (13 Biome × 8, von Ferat angenommen): `vorlagen/doku/SEHENS_KATALOG_v1_2026-10-02.md` – übernehmen, verbessern
  oder durch Besseres ersetzen, Hauptsache es passt zum echten Gelände und zu den Assets.

## Ablauf in zwei Phasen

1. **Phase 1 (jetzt):** Entwurf aller 120 Orte, Standorte im echten Gelände, Asset-Bedarf und die **Download-Liste für Ferat**.
   Claude legt Ferat die Liste vor; Ferat lädt; Claude frischt das Inventar auf, pusht es und gibt Bescheid (`auftraege/13b-…`).
2. **Phase 2 (nach den Downloads):** Planer-Skripte im Format `vorlagen/SEHENS_FORMAT.md`, getestet auf den 2-m-Daten. Claude testet lokal
   auf 1 m, setzt im Editor, macht Bilder mit euren Kameras und schickt Korrekturen (wie bei Auftrag 11).

## Die 15 Biome (Fläche Land, Felder mit ≥ 2 % Anteil: `vorlagen/daten/sehens/legende.json`)

| Biom | km² | Biom | km² | Biom | km² |
|---|---|---|---|---|---|
| aue | 6,84 | lava | 2,37 | wueste | 1,43 |
| bergwald | 4,38 | gletscher | 2,15 | canyon | 1,01 |
| elfenwald | 3,66 | oedland | 1,92 | sumpf | 0,99 |
| dschungel | 3,31 | tundra | 1,71 | fjord | 0,90 |
|  |  | heide | 1,59 | kueste | 0,73 |
|  |  |  |  | frost | 0,71 |

- In den Daten sind Biomgrenzen **Rechtecke** (Zuständigkeit früherer Kacheln). Wie ein Ort wirklich aussieht, sagen Boden (`boden_2m`),
  Höhe, Wasser, Bäume und die Bilder – Standorte deshalb im Inneren wählen bzw. dort, wo Boden und Form zum Biom passen.
- Kleine Biome (< 1,2 km²: canyon, sumpf, fjord, kueste, frost): Abstand darf auf 200 m sinken; Orte dürfen bis 150 m über die Biomgrenze
  reichen, wenn die Form dazugehört (Brandungspfeiler vor der Küste, Gletschertor am Rand).

## Was die 8 Orte je Biom sein sollen

- **Mischung:** etwa 3 Leuchtfeuer (von weitem sichtbar, ziehen vom Weg) + 5 Fundstücke (erst aus der Nähe, belohnen Erkunden).
- **Lage aus den Daten, nicht aus dem Bauch:** 80–300 m abseits der Wege (`weg_2m`), nie in Orten (`ort_2m`) und nicht näher als 150 m an
  geplanten Städten (`standorte.json`); ≥ 350 m zueinander; dort, wo das Gelände sie hergibt (Quelltopf am Bachanfang, Schluckloch am
  Bachende, Wasserfall an einer Geländestufe, Felsburg auf einer Kuppe, Hoodoos in einem Erosionskessel, Pingo in der Ebene …). Rechnet
  Hangneigung, Krümmung, Abfluss, Sichtbarkeit selbst aus der Höhe.
- **Leuchtfeuer:** Silhouette von mindestens einem Weg aus 300–800 m lesbar (Sichtlinie über die Höhe + `baumhoehe_4m`). **Fundstück:**
  vom Weg aus nicht zu sehen, öffnet sich beim Näherkommen (Rahmen aus Fels/Bäumen, Senke, Schlucht).
- **Erreichbar:** Fußweg vom nächsten Weg mit ≤ 25° Steigung, sonst einen kleinen Pfad planen (Bodenlage Erde/Kies als Band, Trittsteine).
- **Stil:** „Dark Fantasy: realistisch, aber wunderschön“ – Weltbau wie The Witcher 3, Farben wie Dragon Age: Inquisition.

## Witcher-Qualität – Pflicht je Ort

1. **Großform und Blickachse:** eine klare Silhouette, Vorder-/Mittel-/Hintergrund, ein Blickziel; der `_held`-Blick ist komponiert.
2. **Größenstufen:** Held (1) → Begleiter (3–8) → Schutt/Geröll (20–200) → Kiesel, Zweige, Laub (Hunderte bis Tausende).
3. **Kontaktzone:** Netze 25–45 % eingegraben, Schuttsaum, Moos/Flechten kriechen hoch (`M_EL_Fels_Auflage`/`M_EL_Klippe_RVT`), Nassband an
   Wasser, Laub in Mulden – nichts „steht auf“ dem Boden.
4. **Bewuchs nach Ursache:** Feuchtering ums Wasser (Seggen, Farn, Moos), Windflüchter an offenen Kanten, Lichtliebende in Lichtungen,
   Pioniere in Spalten, Totholz und Jungwuchs erzählen Sturm, Blitz, Alter.
5. **Wasser:** klar mit sichtbarem Grund, Steine im Wasser, Kies am Ufer, Schaum nur wo es fällt oder strömt.
6. **Licht und Luft:** Nebel in Senken, Dampf an heißen Quellen, Lichtschächte durch Kronenlücken, Glut dezent (feste Sonne, kein Nachtwechsel).
7. **Natur erzählt:** Blitzbaum mit verkohltem Boden und Jungwuchs; Windwurf in eine Richtung; Wildwechsel zur Quelle; gekalkter Vogelfelsen.
8. **Jede Gruppe hat eine Ursache** (Abbruchkante → Schuttkegel darunter; Schmelzwasser → Kiesfächer) – keine Zufallsstreuung.
9. **Messlatte:** `bilder/zielbilder/witcher_01–07.jpg` + `vorlagen/doku/ANALYSE_WITCHER_2026-10-08.md`. **So sieht die Welt heute aus:**
   `bilder/sehens13/` (39 aktuelle Editorbilder, Feld/Biom in `bilder.json`) – ein Ort muss deutlich darüber liegen.

## Assets – Bestand und Downloads

- **Bestand (Stand 11.10. 11:35):** `vorlagen/daten/netze.csv` (1 531 Netze, 976 Nanite; Maße, Dreiecke, Pakete), `inventar.json`,
  `zusammenfassung.md`, `inventar_extra.json` (Decals, eigene Materialien, Wasser-Materialien, Klänge), `material_parameter.json`
  (Parameter unserer Master), `netz_sperre.json`, `netz_check_ergebnis.json`, `netze_masse.json`, Taxonomie `antworten/assets-taxonomie.json`.
  Schon über Fab geladen: `vorlagen/daten/fab_geladen.json`. Frühere Paket-Bewertung: `vorlagen/doku/fab_pakete_bewertung_2026-10-10.md`.
- **Lücken, die ich sehe:** keine Niagara-Systeme (0!), keine Umgebungsklänge, kaum Riesenformen (Riesenbäume, Felsbögen, Basaltsäulen,
  Hoodoos, Pilzfelsen, Sinterterrassen, Eisformationen, Lavaröhren), wenige Wasserpflanzen (Seerosen, Rohrkolben gibt es), keine Salz-/
  Schwefel-/Ruß-Decals.
- **Ferat kann viele weitere Pakete herunterladen.** Durchsucht dafür den öffentlichen Fab-Katalog (fab.com; auch Megascans, kostenlose
  Monatsassets, Epic-Beispielprojekte). Kostenlose Pakete zuerst; kostenpflichtige nur mit Preis und Begründung – **Ferat entscheidet,
  nichts kaufen oder lizenzieren**. Platz ist da (D: 518 GB frei; Grenze 60 GB frei halten).
- **Ferats Fab-Konto:** Ein Login ist für euch nicht möglich. Wenn ihr wissen müsst, ob er ein Paket schon besitzt, vermerkt „prüfen: evtl.
  schon in Bibliothek“ – ich gleiche das mit ihm ab und reiche die Liste als `vorlagen/daten/fab_bibliothek.json` nach.
- Bevorzugt: Nanite-Netze, UE 5.4+ kompatibel, Fab-Standardlizenz, sinnvolle Größe (GB angeben).

## Phase-1-Lieferung (parallel, bitte zuerst A)

**A. `antworten/sehens-downloadliste.md` + `antworten/sehens/downloadliste.json` – darauf wartet Ferat.** Je Paket: Name, Fab-Link,
Anbieter, Preis (kostenlos/€), Größe (GB), UE-Version, Nanite ja/nein, wofür (Ort-IDs), Priorität **A** (nötig) / **B** (deutlich besser) /
**C** (optional), Ersatz aus dem Bestand. Sortiert: A kostenlos → A kostenpflichtig → B → C; höchstens ~25 Pakete in A+B, Summe GB.
Oben eine Kurzfassung in einfachem Deutsch für Ferat (er ist kein Programmierer): „Lade diese 10 zuerst.“

**B. `antworten/sehens-katalog.md`:** 8 Orte je Biom (120). Je Biom eine Tabelle, dann je Ort ein Absatz: was man sieht; Leuchtfeuer/
Fundstück; Vorbild (real + Spiel); Standort (Feld, X/Y in m, Begründung aus den Daten); Komposition und Anmarsch; Detail-Ebenen (Held,
Begleiter, Schutt, Kleinzeug, Bewuchs, Kontakt); Wasser, Effekte, Licht; Geländeänderung; Assets (Bestand + Wunsch); Aufwand und Risiko.

**C. `antworten/sehens/<biom>/standorte.json`** (Ort-IDs, Mitte, Radius, Art, Kameras nach SEHENS_FORMAT §8) **+ Draufsicht je Ort**
`antworten/sehens/<biom>/<id>.png` (2 m: Gelände, Wege, Wasser, geplante Elemente). Wollt ihr vorab Bilder der leeren Standorte aus dem
Editor: Liste `bildwuensche` in der STATUS-Datei – ich mache sie und pushe nach `bilder/sehens13_standorte/`.

**D. `antworten/sehens-STATUS.md`:** wer arbeitet woran, was fertig ist, offene Fragen.

## Phase-2-Lieferung (nach den Downloads)

- `antworten/skripte/sehens_<biom>/sehens_<biom>.py` + `sehens_<biom>_regeln.json`; eure gemeinsame Bibliothek
  `antworten/skripte/sehens_lib/` (Laden 1 m/2 m, Geländestempel, Instanzschreiber, Vorschau, Prüfer `sehens_pruefen.py` gegen SEHENS_FORMAT).
- Getestet mit `--daten2m vorlagen/daten/sehens`; Testbilder `antworten/sehens/<biom>/test_<id>.png`.

## Vorschlag zur Aufteilung (parallel)

- **A „Baukasten und Koordination“:** gemeinsame Bibliothek, globale Abstände und Sichtlinien, Download-Liste zusammenführen,
  Konflikte zwischen Biomen, Kartenmarker-Liste (`antworten/sehens/marker.json`).
- **Biom-Agenten:** B1 aue · B2 bergwald · B3 elfenwald + dschungel · B4 gletscher + frost + fjord · B5 tundra + heide ·
  B6 canyon + wueste + oedland · B7 lava · B8 kueste + sumpf. Jeder liefert seinen Teil der Download-Liste an A.

## Nicht tun

- Keine Houdini-Netze, -Kacheln oder -Materialien (`SW_*`) verwenden oder voraussetzen.
- Keine Bauwerke, Ruinen, Knochen, Menschenspuren. Keine erfundenen Asset-Namen (nur `netze.csv` oder Download-Liste mit Ersatz).
- Kein Projekt-Quellcode ins Repo kopieren (das Repo ist öffentlich): eure Skripte schreibt ihr selbst nach den Formatbeschreibungen.

## Daten für die Standortsuche (`vorlagen/daten/sehens/`, Kodierung in `legende.json`)

`hoehe_2m.png` (uint16, H = 300 + (v − 32768)/64 m), `biom_2m.png`, `boden_2m.png` (vorherrschende Bodenlage), `weg_2m.png`, `ort_2m.png`,
`wasser_2m.png` (Süßwasser; Meer = Höhe < 0 und kein Süßwasser), `baeume_4m.png` + `baumhoehe_4m.png` (alle gesetzten Bäume, Näherung),
`uebersicht_biome.jpg` (4 m/px mit Gitterfeldern), Vektoren `wasser_welt.json`, `baeche_alle.json`, `teiche.json`, `standorte.json`.
Raster und Koordinaten: `vorlagen/FORMAT.md` §1. Lieferformat: `vorlagen/SEHENS_FORMAT.md`.
