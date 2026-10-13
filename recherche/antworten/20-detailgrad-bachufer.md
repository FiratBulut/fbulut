# Antwort 20 – Detailgrad Bachufer (Verweis)

Die vollständige Antwort zu `auftraege/20-detailgrad-bachufer-felsen.md` steht in
**`antworten/20-detailgrad-bachufer-felsen.md`** (gleicher Name wie der Auftrag).

**Kurzfazit:**
- Der Plan für die Talkaskade s 390–578 ist fertig: beide Ufer, je 0–10 m ab der Wasserkante.
  - 7 661 Instanzen, 545 davon mit Kollision; mit dem Bettplan zusammen 8 306 / 694 (18 % / 23 % des Feldbudgets C2).
  - Prüfer: 0 FEHLER, zwei Läufe byte-gleich.
- Ferats Dichte-Zensus (6h) ist eingebaut: große Blöcke gestapelt statt mehr Kleinzeug.
  - Felsdeckung 130–139 % (heute 1,2 %), 47 verschiedene Netze.
- C.3 „Gras 60–80 % über die Kante“ ist ersetzt durch 5–10 % Graslücken am Gleitufer.
- Kein Schaum im Bach außer an Fällen; der „Kragen“ wird die Nasslinie im Steinmaterial.
- Nichts zu kaufen; die Fab-Kandidaten stehen schon in Ferats Bibliothek.

**Dateien** (Ausgabeformat §9):
- `skripte/detailgrad/detailgrad_regeln.json`: Regeln je Biom und Werte für `bachdekor_swr_regeln.json` und `kantenufer_p2`.
- `skripte/detailgrad/plan_p2_talkaskade.json`: Plan im FORMAT-§3-Stil.
- `skripte/detailgrad/detailgrad_plan.py`: Planer, Aufruf `--bild --selbsttest`.
- `skripte/p2_bett/p2_bett_welt.py --instanzen-plan`: setzt den Plan in die Welt.
- Bilder: `detailgrad/querschnitt_ufer.png`, `detailgrad/draufsicht_10m.png`, `detailgrad/stapel_beispiel.png`.
