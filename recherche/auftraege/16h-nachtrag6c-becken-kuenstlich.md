# 16h Nachtrag 6c – FERAT (19:30): „Riverbecken wirken künstlich: runde Vertiefungen, alle gleich groß und regelmäßig“ – VORRANG

Das ist der Kern von Nachtrag 6 §8 / 6b (Bild `bilder/swr_p2/talkaskade_treppe_von_oben.jpg`). Unsere Plandaten dazu (`lauf_p2.json`,
Talkaskade s 390–579):

- **26 Stufen auf 189 m**, alle **3–4 m** eine; Fall je Stufe 0,68–3,74 m (Mittel ≈ 1,7 m).
- Jedes Becken ist **3–4 m lang und ~4 m breit**, also rund. Tiefe am Fuß 0,76–1,20 m, vor der nächsten Lippe 0,36–0,71 m.
  Die Form selbst stimmt: Der Kolk liegt direkt unter dem Absturz (unsere Behauptung „verkehrt herum“ in 6b war falsch).
- Alle Becken sind mit derselben Brush-Form gegraben (Kurve „Kasten-U“, Falloff 1,5, Rampe 1,5, Tiefe je Spline-Punkt). Dadurch werden sie
  gleich groß und rund.
- **Ufer liegen bündig:** 0,5 m neben der Planbreite liegt das Gelände im Median nur 0,16 m über dem Spiegel (56 % unter 0,2 m);
  Durchbruch 0,06, Kiesbett 0,04 m. Deshalb läuft das Wasser aufs Ufer (6b).

**Auftrag (bitte zuerst):** einen **neuen Bettplan für die p2-Talkaskade** (gern auch Durchbruch und Bergrinne), der natürlich wirkt.
- Euer A15-Planer mit den 15f/15g-Regeln wäre ideal:
  - schräge und gekerbte Lippen, Buchten, Eck- und Randblöcke;
  - **unregelmäßige Abstände** (z. B. 1–4 Bachbreiten, nach dem Gefälle) und unterschiedliche Fallhöhen;
  - Becken **länglich** in Fließrichtung und seitlich versetzt (Talweg pendelt), einzelne längere ruhige Strecken;
  - Stufen aus Blöcken.
- Dazu die Werte aus Antwort 18: **Becken 0,8–1,2 m**, **Uferstufe 0,2–0,5 m** (Spiegel unter der Grasnarbe), Rinnen 0,2–0,4 m.
- Ausgabe im A15-Format (Gelände-Datensatz je Feld wie `sehens_einbau/A15_*`, dazu Spiegel je Meter für die SWR-Spline). Wir bauen ihn
  über `a15_einbau.py` bzw. die s38-Kette ein, legen die Spline-Z auf euren Spiegel und backen neu.
- Die Wasseroberfläche bleibt die SWR (ein Fluss von der Quelle bis zur Mündung, Ferat 12.10.). Die Mündung bleibt bei 36,80 m.
- Bitte vorher eine Delta-Karte und Querschnitte als Bild, damit Ferat die Form sieht, bevor wir graben.

Referenz für Ferats Blick: `bilder/zielbilder/witcher_01.jpg`. Ferat bitten wir um eigene Witcher-3-Aufnahmen von Bergbächen (Antwort 18 §7.13).
