# 16h Nachtrag 4 – V18 eingebaut (Tönung, Bach-Werte, Entsättigung), Mündung repariert (13.10.2026, 13:45)

Bezug: eure Antwort `antworten/16h-nachtrag2-tl-t0-kasten.md` §7, Punkte 1, 2 und 4.

## 1. Landschaftsmaterial V18 (eure Punkte 1 und 2, erster Teil)

- **Neue Datentextur** `T_Eldarien_Bachgewicht_2m`:
  - 2-m-Raster wie die Spiegel-Karte, Bachgewicht = 1 − SmoothStep(6, 12, Breite).
  - Quellen: Flüsse und Bäche ohne die vier ersetzten Läufe, Seen und Meer 0, p2 aus dem gebackenen Wasser mit Plan-Breite.
  - Ins Ufer läuft der Wert weich aus: voll bis 8 m, dann bis 16 m.
- **V18 / V18s** = Kopie V17 / V17s + 23 Knoten (Gruppe „V18 Wasser“):
  - W_unter / W_ufer mit Bachgewicht, `Toenung_Wasser_Neutral` 1;
  - Lerp(Welt, Bach, bg) für `Ufer_Staerke` (0,25), `Ufer_Farbe` (0,60; 0,62; 0,60), `Nass_Abdunkeln` (0,40) und `Nass_Breite_cm` (50);
  - Desaturation der Endfarbe mit `nass × bg × Entsaettigung_Nass` (0,35).
  - Kosten: 420 → 447 Anweisungen, kein neuer Sampler, Texturen 68 → 69 bzw. 51 → 52. 0 Übersetzungsfehler.
- **SRV:** Ein Landschaftsteil (`_504_6_10_0`) kam mit V18 auf 65 SRVs. Es läuft jetzt mit V12s/V18s. Ein Prüflauf über alle 70 Felder
  stellt weitere solche Teile automatisch um und läuft gerade.
- **Gras-Karten:** nicht veraltet (C2: 320 Komponenten, „veraltet 0“). Nanite der geladenen Teile ist aktuell. Ein Welt-Neubau ist also
  nicht nötig.
- **Bild** `bilder/swr_p2/v18_vorher_nachher.jpg` (dieselben 4 Kameras wie TL):
  - Das Bett ist grauer und weniger orange, der Uferstreifen am Wasser dunkel und nass. Am deutlichsten bei t430 und t500 schräg.
  - Noch nicht grau genug: Der Kies-Grund wirkt im warmen Licht weiter hell-beige.

**Frage:** Nächster Schritt nach eurer Liste:
- die Lagen unter dem Spiegel (Geroell 30, Kies 15, Fels 20, Felsplatte 10, Schlamm 12, Algen 13) über die Kette `s38 lagen`, und
- der Tausch der Geröll-/Fels-Textur gegen `T_MossyRockyGround_01` / `T_IcelandicQuarryRock_01`. Das wäre eine V19 mit neuen Texturen und
  kostet SRVs, weil V18 schon nah an 64 ist.

Bitte sagt, ob der Texturtausch die SRV-Grenze wert ist, oder ob ihr eine Variante ohne zusätzliche Texturen seht (z. B. Farbanpassung je Lage
unter Wasser).

## 2. Mündung (euer Punkt 4) – Ferat hatte es im Bild gesehen

Ferat: „von Wasserpfützen wird es ein River plötzlich“. Befund und Umsetzung:

**Befund:**
- p2-Spiegel ab s 744 bis 0,5 m **unter** dem Gelände. Die Mündung war beim Plugin-Graben ausgenommen, ein Sattel bis 36,98 m bildete Pfützen.
- C3-Kopf: 36 m breit bei 37,78 m (Rest von 2_C2).

**Gelände:** p2-Bett ab s 736 bis zur Mündung und entlang der C3-Achse bis dist 40 m weitergegraben.
- Spiegel 36,86 → 36,80 m, Sohle = Spiegel − 0,45 m, Ufer 32°, nur Abtrag (54 m³, max 0,6 m; C2 und C3).

**Wasser:**
- p2-Spline-Z ab s 736 auf den neuen Spiegel gesetzt.
- C3-Kopfpunkte 0–2 nach dist 24/31/38 m verschoben: 36,80/36,72/36,64 m, Breite 7/11/14 m. Danach 17, 22, 26 und 25 m (Auffächern statt Kante).
- Rest von C3 unverändert. SWR neu gebacken: Bett 99,9 % nass, **Front 788/788**.

**Bild** `bilder/swr_p2/muendung_vorher_nachher.jpg`: Von 8 m Höhe sieht man ein durchgehendes Wasserband. Von oben bleibt eine schmale
Anfangskante.

Rückweg: `swr/muendung_wasser.py zurueck`, `hoehe.*.vor_brush_muendung_p2`.

**Hinweis für den Export (`muendung_anschluss`):** Der lokale C3-Fluss beginnt jetzt bei dist ≈ 24 m (bisher 0). F_ERLENBACH bitte
entsprechend kürzen, wenn ihr ihn baut.
