# Auftrag 13j – Antworten auf die Rückfragen aus 13h, neue Netzmaße, Stand lokal

Stand 12.10.2026, 02:50. Danke für 13h, 13i und 15f. Alles ist angekommen.

## Neue Daten: alle Netzmaße gemessen

`vorlagen/daten/netze_masse.json` hat jetzt **1 017 Einträge** (Commit 46bd196). Alle 532 bisher fehlenden Netze der Sehens-Pläne sind im Editor
gemessen: Begrenzungsbox im Netz-Raum und Materialien. Bitte damit rechnen statt mit der Annahme „Pivot unten Mitte“ (E35), vor allem für Pivot und
Unterkante (A3/K2) und für Klippen, Basalt und Mountain-Wände.

## Antworten auf eure Rückfragen

1. **Schauseite der Klippennetze (`front_achse +y`):** Ich prüfe sie an den Bildern des zweiten Pilots (bergwald_06) und melde Netze, deren Schauseite
   nach hinten zeigt, mit Namen. Bis dahin bleibt eure Annahme.
2. **`Fir_07_Forest` auf 570 m:** Wird am `_fern`-Bild des zweiten Pilots geprüft. Ist die Krone zu früh vereinfacht, stelle ich lokal die
   LOD-/Sichtweite ein. Das betrifft nur das Asset, nicht den Plan.
3. **`ist_fels` über Namensmuster:** Für jetzt in Ordnung. Ein Kennzeichen im Inventar (`kategorie: fels|baum|pflanze|…`) liefere ich mit dem
   nächsten Inventar-Lauf mit.
4. **Akteur-Budget (bis 78 je Ort):** Für den Pilot in Ordnung. Regel ab jetzt: Wiederholte Wandmodule desselben Netzes ab 12 Stück als
   Instanzen (Ebene `sw_<biom>`, Typ mit Kollision) statt Akteure. Einzelne Heldenstücke (Fallwand, Nadel, Mutterbaum) bleiben Akteure.
   Richtwert höchstens 50 Akteure je Ort.
5. **sumpf_02 `_fern` (Rohrkolben-Horst im Strahl):** Wird beim Bau von sumpf_02 im Bild geprüft.

## Lokal (12.10. nachts)

- Rückbau des ersten Pilots (B5/C5) und des ersten C2-Baus läuft gerade. Danach plane ich beide auf 1 m mit eurem neuen Stand neu und baue sie.
- **Treppenbäche (13g):** Für den zweiten Pilot fehlt noch eure Ausgabe im A15-Format (`wasser_koerper` mit river + kaskadennetz + `quer`).
  Bis sie da ist, baue ich im Karsee den See, aber noch keine gestuften Zu- und Abflüsse.
