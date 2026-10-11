# Auftrag 15c – Nachtest auf 1 m nach 15b (kurz)

Stand 11.10.2026, 19:45. Claude lokal hat den korrigierten Planer (9ccfe48) mit allen 20 Piloten (19 Läufe) auf den echten 1-m-Daten laufen lassen.

## Ergebnis

- **Planer-Prüfer:** 18 von 19 Läufen haben 0 FEHLER. **C2 hat 0 FEHLER** und wird jetzt lokal gebaut.
- **Rest-FEHLER:** B_R_P4_M2_04_KN0, „Bett an 1 von 132 Beckenpunkten < 0,2 m unter dem Spiegel“. In der Cloud gab es diesen Fehler nicht. Der Unterschied
  kommt wohl daher, dass hier alle Daten in 1 m vorliegen, in der Cloud dagegen 1-m-Fenster plus 2-m-Raster. Bitte prüfen.
- **Eigene Nachmessung** (jede Beckenmittellinie, Netzrand = halbe Breite + 0,4 m, ohne Ausnahmen für Stufennähe oder Mündung):
  16 Läufe ohne Befund. Übrig sind 7 Einzelpunkte. Euer Prüfer schließt sie vermutlich als „nahe Stufe“ oder „Mündung“ aus; das ist in Ordnung,
  wenn es stimmt. Bitte kurz bestätigen:

| Lauf | Netz / k | Seite | X, Y (m) | Spiegel | Ufer neu | Ufer alt | fehlt |
|---|---|---|---|---|---|---|---|
| B_R_P1_M2_01 | KN0 / 212–213 | links | −543,7, −2091 | 29,95–29,98 | 29,66–29,78 | 30,84 | 0,30–0,40 m |
| B_R_P3_M2_01 | KN1 / 127–129 | rechts | 1784, −1714 | 18,06–18,11 | 17,80–18,15 | 19,0–19,1 | bis 0,39 m |
| F_ERLENBACH_2V_D3 | KN0 / 32–33 | links | −1636,7, −1784 | 23,50–23,53 | 23,02–23,24 | 22,0–22,2 | 0,40–0,58 m (Bestand, Uferring 1 m reicht nicht – WARNUNG ok) |

Einzelwerte: [`vorlagen/daten/gefaelle/a15_piloten_1m_befund_nach15b.json`](../vorlagen/daten/gefaelle/a15_piloten_1m_befund_nach15b.json).

## Lokal

- Das Einbau-Werkzeug für C2 entsteht gerade (Kaskadennetz aus `mittellinie` mit adaptivem Rand als Absicherung, `M_EL_Kaskade_SLW`,
  River-Teilung, Zufluss `F_ERLENBACH_1_C2`, Ebene `gefaelle`, Effekte, Kameras).
- Regel lokal: River-Einträge unter 15 m (C2: `R0`, 10,5 m) baue ich nicht als Epic-River, sondern als Rampe im Kaskadennetz (14b: kurze Stücke
  zeichnen trockene Becken). Wenn ihr das im Planer so ausgeben wollt, gern.
- Danach baue ich C2 im Editor, mache Vorher- und Nachher-Bilder und zeige sie Ferat. Erst nach seinem OK baue ich die übrigen 19 Piloten.
