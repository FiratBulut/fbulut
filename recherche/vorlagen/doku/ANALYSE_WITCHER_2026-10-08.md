# Zielbild-Analyse 08.10.2026 – Witcher 3 (Next-Gen) und Witcher-4-Technikdemo (UE5)

Ferat schickte am 08.10. abends 7 Bilder (Fluss mit Ruine und Schneebergen; Dorf im Schnee mit Markt; Waldpfad mit Bach und Pferd;
Blick von der Klippe über ein Tal mit Burg; Markt; Tal mit Brücke unter rot-weißen Felswänden; Nadelwald-Schlucht mit Lärchen).
Auftrag: „Landschaft, Bodentexturen, Gras- und Baumdichte, Farbpalette, wie viele Details darin stecken – das wünsche ich mir auch
in Eldarien.“ Städte/Figuren sind nicht gemeint (nur als Hinweis für Bodengestaltung im Ort: Matsch, Schnee, Laub, Stroh).

## Was die Bilder ausmacht

1. **Boden nie einheitlich.** Auf wenigen Metern 4–6 Schichten: Gras, Moos, Erde, Kies, Laub/Nadeln, Schnee. Dazu echtes 3D-Kleinzeug
   (Kiesel, Zweige, Laub, Zapfen, Wurzeln). Übergänge Gras → Fels immer über einen Saum aus Kies und Moos, nie harte Kanten.
   In Orten: zertretener Matsch mit Pfützen, Schnee nur am Rand, Laub und Stroh.
2. **Gras dicht und hoch** (knie- bis hüfthoch), 3–5 Arten gemischt, Farbe wechselt (frischgrün, gelbgrün, trockene Spitzen).
   **Blumen in Inseln** (Bild 1: rote/orange Ähren in Gruppen), nicht gleichmäßig gestreut.
3. **Bäume in Gruppen mit Lichtungen.** Waldrand mit Büschen und Jungbäumen (Saum), alte + junge + tote Bäume, Nadel/Laub gemischt,
   Herbstfarben als Akzent (rostrote Lärchen in Bild 7). Kein Plantagen-Raster.
4. **Felsen in Gruppen** (ein großer + mehrere kleine), halb eingegraben, oben Moos oder Schnee. Bachbetten voller Steine und Kies.
5. **Berge:** scharfe Grate und Türme, Fels mit Farbbändern (rot/ocker/grau), Schnee nur auf Simsen und flachen Stellen
   (Hangneigung!), Nebel und Wolken hängen an Gipfeln und Wasserfällen.
6. **Farbe/Licht:** warmes Sonnenlicht gegen kühle blaue Schatten; starke Luftperspektive (Ferne wird blau-weiß); wenige kräftige
   Akzente (orange Blumen, rote Felsen, Rostlaub) vor Grün und Blau-Weiß. Satt, aber natürlich – nie grau-braun eintönig.
7. **Staffelung:** Vordergrund voller Details, Mitte Büsche/Steine/Bäume, Hintergrund Waldsilhouetten, Ferne Berge im Dunst.
   Immer ein Blickziel (Ruine, Burg, Dorf, Wasserfall), Wege führen dorthin.
8. **Wasser:** klar, Grund sichtbar, Steine ragen heraus, Schaum an Stromschnellen, Spiegelungen; Ufer aus Kies und Felsen.

## Stand Eldarien am 08.10. (ehrlich)

- Boden oft große einfarbige Flächen (C5: grüner Teppich ohne Halme; E6: brauner kahler Boden), kaum 3D-Kleinzeug.
- Landschafts-Gras schwebte auf alten Höhen (Gras-Karten veraltet, behoben ab 08.10. abends – siehe CLAUDE.md).
- Wald gleichmäßig verteilt (E6, G3/G4), wenig Waldrand, wenig Totholz.
- Felsen meist einzeln; Berge grau-kahl, Felstextur wirkt aus 200–400 m wie Kopfsteinpflaster.
- Dunst/Luftperspektive schwach; Flüsse beginnen teils ohne Quelle (E6).

## Umsetzung (Reihenfolge, Kachel für Kachel, Vorher/Nachher-Bilder)

1. Gras-Karten der ganzen Welt neu (läuft 08.10.).
2. Boden: Kleinzeug-Schicht (Kiesel, Zweige, Laub, Zapfen – als Landschafts-Gras, billig) + mehr Mischung der Lagen (Moos/Kies/Laub-Flecken).
3. Gras: dichter und höher, 3–5 Arten je Biom, Blumeninseln über Rauschen geklumpt, Trockengras-Farbvariation.
4. Wald: Gruppen + Lichtungen, Waldsaum (Büsche/Jungbäume), Totholz, Altersmischung, Herbst-Akzente.
5. Felsgruppen (groß + klein, eingegraben) mit Moos-/Schnee-Auflage (`M_EL_Fels_Auflage`).
6. Berge: Schnee auf Simsen (Neigung), Farbbänder, Wolken/Nebel an Gipfeln.
7. Licht: stärkere Luftperspektive, Talnebel, Gischt an Wasserfällen.
8. Flüsse: echte Quellen (Quelltopf, See-Abfluss, Wasserfall), steinige Ufer, Schaum an Stromschnellen.
