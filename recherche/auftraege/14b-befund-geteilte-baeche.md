# Auftrag 14b: Befund geteilte Bäche – trockene Becken (11.10.2026, 17:30)

Ergänzung zu Auftrag 14 (Nature Water FX) und 15 (Felsstufen). Bilder `bilder/wasser_fx/DEKOR1_*` (nach Bachdekor, 17:20).

- **C2 F_ERLENBACH_1V_C2, in 11 Epic-Flussstücke geteilt (Becken 5–7 m lang, Lücken 1,26–2,95 m):** Die **Becken erscheinen trocken** – man sieht
  Schlamm/Steine des Betts, kaum Wasserfläche (`DEKOR1_C2_Nah_*`, `DEKOR1_C2_KA_K10a_Stufen`). Vor dem Teilen (ein durchgehender Fluss) war Wasser
  sichtbar. Vermutung (ungeprüft): Epic Water zeichnet die Oberfläche über das Wassernetz (Kacheln 24 m, Wasser-Info-Textur ~1 m/Texel); sehr kurze
  Flussstücke werden darin nicht oder nur teilweise abgebildet bzw. eine Kachel zeigt nur einen Wasserkörper. Bitte recherchieren: Mindestlänge/
  -breite eines WaterBodyRiver, Verhalten mehrerer kurzer Bodies in einer Kachel (Overlap/Priority), Abhilfe (z. B. eigene kleine Wasserzone mit
  feinerer Auflösung, `OverlapPriority`, Water Body Lake statt River für Becken, statisches Wassernetz für Becken).
- **Vorhang/Schaumscheibe:** auch mit Deckkraft 0,55/0,45 noch helle, rechteckige Flächen (Kacheln). Die Schaumscheibe in H4 zeigt eine sichtbare
  Rechteckkante (`DEKOR1_H4_Nah_*`).
- **Ich habe C2 deshalb vorerst auf den durchgehenden Fluss zurückgestellt** und alle Stufen-Akteure entfernt (Netze/Materialien bleiben).
  Euer Plan (14/15) soll eine Lösung enthalten, die **sichtbares Wasser in jedem Becken** garantiert; Niagara (Nature Water FX) für Vorhang/Gischt
  ist ausdrücklich erwünscht (Ferat hat es dafür gekauft).
