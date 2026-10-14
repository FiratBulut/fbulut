# 16h Nachtrag 6j – Ergebnis Teilungstest (drei Flusskopien), Pixelmessung, offene Punkte

Stand 15.10.2026, 01:20. Bezug 6g, 6i (999ddfe). Alles im Speicher getestet, nichts gespeichert; Stand auf Platte = ganze SWR mit BAKED_SIM.

## 1. Teilungstest „Variante C light“ (drei Flusskopien T00/T01/T02, je eigene SWR, res 2048, je 5 min Live-Sim, dann Bake)

| Teil | s | Zelle | Bake nass | Befund |
|---|---|---|---|---|
| T00 oben | 0–393 | 18,4 cm | 12,6 % | **Front bleibt bei s 131 stehen** (Bergrinne; wie früher bei zu feinen/engen Einstellungen) |
| T01 Talkaskade | 386–581 | 8,7 cm | 10,4 % | läuft durch; **Band 0,25–2 m nass 25,9 % (> 2 cm) statt 78,8 %; bei > 10 cm 13,1 %; Bett 99,9 %; Tiefe p90 0,80 m (vorher 0,59)** |
| T02 unten + Arm | 575–788 | 9,7 cm | 33,6 % | läuft, aber **trocken s 582–589** (Anlaufstrecke der Kopie; Band wurde am Arm statt am Teilfluss gesetzt) |

Nähte (vereinigtes 1-m-Raster `swr_dumps_vereinen.py`): s 385–393 Spiegelsprung median 32 cm, p90 67 cm (Ziel ≤ 2; T00 kommt dort gar nicht
an); s 575–583 keine Überlappung, 8 m trocken. Band je Schwelle (Talkaskade): 29,8 / 25,9 / 19,4 / 13,1 % bei > 1 / 2 / 5 / 10 cm.

**Lesart:** Die feine Zelle wirkt wie erwartet (78,8 → 25,9 %, Kolke erreichen 0,8 m), aber das 5-%-Ziel wird auch mit 9 cm nicht erreicht,
und die Teilung reißt den Bach an den Nähten auf. Verworfen (harter Neustart ohne Speichern); der ganze Bach bleibt mit 37-cm-Zellen und BAKED_SIM.

**Fragen:** (a) Ist 25 % bei 9 cm das Ende der Simulation (dann Boden-Trick/Band schmaler als nächste Stufe) oder liegt es an unserem Reset
(Nachfüllen 0,3 auch im feinen Teil)? (b) Variante A statt C: ganze SWR behalten (zeichnet oben/unten) und nur die Talkaskade als eigene
Flusskopie+SWR mit höherer Zeichenpriorität darüber – Risiko Konkurrenz; Prüfpunkte? (c) Hat die Talkaskade allein als Kopie eine brauchbare
Quelle (Einlauf bei s 386 aus dem Nichts, `source_size` 300)? Oder Quelle = ganze SWR als `source_river_water_bodies` (Forum-Muster)?

## 2. Pixelmessung (6h §2), erste echte Werte, Modus „SceneDepth + Ausblenden je Klasse“

| Kamera | Netz % | Fels | Pflanze | Himmel |
|---|---|---|---|---|
| K1 Talblick (C5) | 19,7 | 4,3 | 15,5 | 18,3 |
| K2 Haldenfuß | **5,1** | 5,1 | 0,0 | 0 |
| K3 Schrofen | 73,6 | 42,4 | 31,2 | 5,3 |

K2 ist offensichtlich falsch (Bild voller Felsnetze): `hide_component` blendet Nanite-Netze in der SceneCapture nicht aus → Werte unbrauchbar.
Wir wechseln auf den CustomDepth-Stencil-Weg (euer Vorschlag) und messen neu. K3 (73,6 %) ist plausibel, aber ungeeicht.

## 3. Pilot B5-Ost gebaut (Bilder folgen mit der Messung)

Gesetzt: Klippenband 2 229 + Turm, Halde 1 202 + 6 Hero, Platten 2 692, Baumgruppen 758; 1 631 Altbestand-Bäume entfernt; Lagen Geröll/Fels/
Felsplatte; Zensus Fenster: Felsdeckung (OG) 176 %, 14,7 Netze/100 m². Störung: weiße, papierflache Quadrate auf Simsen (K2) – kein Netz des
Pilots (alle Gruppen einzeln ausgeblendet, ohne Wirkung); Verdacht Niagara-Sprites/Decals der Sehens-Effekte `SW_B5_bergwald_06_karsee`. Prüfung folgt.
Rückfrage 1 (Front-Achse der Bänder) steht noch aus (K3 zeigt Bänder plausibel hangab).

## 4. Bitte

1. §1 (a)–(c): Weg zur Uferstufe nach dem Teilungsbefund (feine Zelle hilft, reicht nicht; Nähte brechen).
2. Prüfpunkte für den Stencil-Weg der Pixelmessung (Nanite, Foliage-HISM, Gras).
