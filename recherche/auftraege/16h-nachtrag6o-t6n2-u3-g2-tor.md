# Nachtrag 6o – Prüftor P6N: U2 mit Breite 1, T6N2 mit Breite 2 verfehlt G2 → U3; Frage zum Tor G2

Stand 18.10.2026, 19:58 PC-Uhr. Bezug: Antwort 16h-N6n (73b2ac5) §2.3–2.5. Rohdaten: `auftraege/daten/6o/` (Bericht Rolle 1, Ausgaben).

## 1. Ergebnisse

| Lauf | Breite | G1 sichtbar_5 Band (≤ 16 %) | G2 Kolke gegen Breite 5 | G3 Bett nass_sim (≥ 97 %) | Kernbett sichtbar_1 | Urteil |
|---|---|---|---|---|---|---|
| T6M3A_2 (Dump 18:14) | 1 | 10,70 % | Median \|ΔW\| 4,0 cm, max 50 cm, 10 Kolke > 5 cm | 99,84 % | 100 % | **U2** |
| T6N2_2 (Dump 19:52, nur Speicher) | 2 | 10,70 % | Median \|ΔW\| 4,0 cm, max 48 cm, 10 Kolke > 5 cm | 99,36 % | 100 % | **verfehlt → U3** |
| T6L2B_2 (Basis, gespeichert) | 5 | 10,47 % | – | 54,24 % (trägt bei 5 nicht, 6n §3) | 97,6 % (6 Fehlzellen) | – |

Weitere Zahlen aus T6N2: Bett nass 99,7 %, Front 788 m, stabil nach zwei Dumps (größte Änderung 0,2 pp). Band-Median Simulationsboden
minus Gelände −14,1 cm (Basis −62,3, Breite 1 −3,5). Kolktiefe 0,8–1,35 m: Breite 2 23/24, Breite 5 24/24. Unter 0,8 m liegt bei Breite 2 nur Nr. 3
mit 0,68 m (bei 5: 0,80 m).

Nach 6n §2.3 gilt damit **U3: bei Breite 5 bleiben**. Der gespeicherte Stand hat Breite 5 und BAKED_SIM. T6N2 lag nur im Speicher und wird mit
einem Neustart ohne Speichern verworfen.

## 2. Diagnose von Rolle 1: G2 misst die Zeichnung, nicht den Löser

- Bei Breite 1 passt die Ausgabe an allen 24 Kolkpunkten zum Löser: W − G − F liegt bei −0,1 bis −3,9 cm.
- Bei Breite 5 liegt W an diesen Punkten bis **+53 cm** über Kontur plus Tiefe. Die Glättung zieht den oberen Beckenspiegel in die Mulde.
- Ein Offline-Nachbau der Glättung aus dem Niagara-Asset erzeugt aus dem Breite-1-Löserzustand den echten Breite-5-Dump eines anderen
  Laufs. Die Abweichung beträgt im Median 0,25 cm, das 90-%-Quantil 4 cm, also eine Half-Float-Stufe. Dieselben 6 Kernbett-Fehlzellen
  entstehen. Eine messbare Rückwirkung der Glättung in den Löser gibt es damit nicht.
- **Die Vorhersage aus dem Nachbau für Breite 2 traf ein:** vorhergesagt waren G1 und G3 bestanden, Kernbett 100 %, G2 verfehlt mit 9 Kolken
  über 5 cm und höchstens 48 cm. Gemessen wurden 10 Kolke, höchstens 48 cm.
- Grund: Bei Breite 2 tragen nur die vier diagonalen Nachbarn bei. Ihr Gewicht ist in Kolken fast 0. Erst bei Breite 5 wirken Nachbarn bis
  5 Zellen, und ihr Gewicht steigt mit dem Höhenunterschied.
- An 4 der 6 Kernbett-Fehlzellen zeigt Breite 5 sichtbar trockenen Grund (W − H −3,7 bis −13,7 cm), obwohl der Löser dort 24–50 cm Wasser führt.

**Folge:** Die „tieferen Kolke“ bei Breite 5 sind gezeichnet, nicht gerechnet. G2 vergleicht damit Breite 1 oder 2 gegen ein Darstellungsartefakt.

## 3. Fragen

1. **Ist G2 das richtige Tor**, wenn ΔW die Glättung bei Breite 5 misst? Vorschlag zur Prüfung: an den Kolkpunkten W − G − F ≤ 5 cm, also
   Ausgabe gleich Löser, und die Löser-Kolktiefe G + F − H im Zielbereich 0,8–1,35 m.
2. Wenn G2 bleibt: Dann entscheidet nach 6n §2.3 Ferat zwischen Kolktiefe und Kernbett. Bitte eine kurze, für Ferat verständliche
   Gegenüberstellung mit den beiden Bildpaaren aus 6n §2.2 als Grundlage. Wir legen ihm die Frage erst nach eurer Antwort vor.
3. Wenn G2 ersetzt wird: Gilt dann Breite 1 oder Breite 2 als Kandidat für den Speicherlauf T6N1 (6n §2.5)? Breite 2 hat im Kernbett und in G1
   dieselben Werte wie 1, im Bett 99,36 statt 99,84 %.

## 4. Stand im Editor

Nichts gespeichert. Bilder der T6N2-Kette: `T6N2_0BAKED5_*`, `T6N2_1LIVE1_*` und gebacken mit Breite 2, gleiche Kameras wie 6n.
