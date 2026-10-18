# Antwort 16h Nachtrag 6p – Kolk 25: Kriterium „je ± 4 cm“ war falsch begründet; T6N1 übernehmen

Gelesen: recherche/auftraege/16h-nachtrag6p-t6n1-kolk25.md @ b4fd18c009c4daddb81c5db60250a899672ccc44 (Commit 86a5adc)

Stand 18.10.2026. Bezug: Antwort 6o (f2bb485) §4.2/§4.3, 6n §2.5. Bearbeiter: Cloud-Recherche. Bereich: SWR p2, Breite 1 (T6N1).
Bild `bilder/swr_p2/t6n1_bildpaare.jpg` selbst angesehen.

## Kurzfazit

1. **Kriterium – beantwortet:** Die Regel „Kolke je ± 4 cm (Laufstreuung)“ aus 6o §4.2 war unser Fehler. Die Streuung war nie gemessen,
   sie war angenommen. Gemessen ist jetzt: 23 Kolke liegen bei 0,0 cm, einer bei 10 cm. Das ist kein Rauschen, sondern ein einzelner Kolk,
   der sich zwischen zwei Läufen anders einpendelt. **Neues Kriterium K-Kolk:**
   - Median |ΔW| ≤ 2 cm;
   - kein Kolk verlässt durch die Abweichung den Zielbereich 0,8–1,35 m;
   - jede Abweichung über 4 cm wird einzeln genannt und muss an einem Stufenfuß liegen (§3).

   **T6N1_2 erfüllt K-Kolk:** Median 0,0 cm, Kolk 25 bleibt mit 1,045 m im Ziel, Stufenfuß bei s 492,1.
2. **T6N1 übernehmen – beantwortet:** Alle verbindlichen Tore sind bestanden (G1, G2′a/b, G3, Kernbett 100 %, Front), dazu K-Kolk, und die
   Bilder sprechen nicht dagegen. Ist T6N1_2 noch im Speicher: speichern. Sonst T6N1b mit derselben Kette laufen lassen und mit K-Kolk
   abnehmen. **Nicht** so lange wiederholen, bis Kolk 25 „passt“; dieser Wert entscheidet nicht über das Speichern (§2).
3. **Kolk 25 – wartet auf Beleg (Diagnose, kein Blocker):** Wahrscheinlich ein Wechselsprung am Stufenfuß mit zwei fast gleichwertigen
   Gleichgewichtslagen. Prüfung offline an den zwei vorhandenen Dumps (§3).
4. **Kolk 36 bleibt offen** (35 cm unter Plan, 6o §1.3). Das ist ein eigener Befund, unabhängig von dieser Entscheidung.

---

## 1. Warum das Kriterium falsch war

6o §4.2 hat „Kolke je ± 4 cm“ als Streuung zwischen zwei Läufen begründet. Gemessen war diese Streuung nie; die 4 cm kamen aus der
Half-Float-Stufe und aus Vorsicht. Nach `vorlagen/pruefung.md` (Messwerkzeuge) braucht eine Toleranz aber einen bekannten Sollwert und
einen belegten Gültigkeitsbereich. Der Vergleich zweier gleich eingestellter Läufe zeigt nun:

- 23 von 24 Kolken sind **bitgleich** (0,0 cm). Wäre die Streuung ein Rauschen, müsste sie an allen Kolken etwas zeigen. Das tut sie nicht.
- Ein Kolk springt um eine diskrete Stufe (+10 cm), bleibt im Zielbereich und wird tiefer.

Das Kriterium sollte zeigen, ob die Kette wieder den geprüften Zustand erreicht, also ob die Einstellungen greifen und nichts
anderes verändert ist. Dafür taugt der Median über alle Kolke. Ein einzelner Kolk, der zwischen zwei Gleichgewichtslagen wechselt, ist eine
Eigenschaft der Strömung an genau diesem Ort und kein Fehler der Kette.

**K-Kolk (ersetzt „je ± 4 cm“ in 6o §4.2):**

| Teil | Grenze | Zweck |
|---|---|---|
| Median \|ΔW\| über 24 Kolke gegen den Vorlauf | ≤ 2 cm | Die Kette reproduziert den geprüften Zustand. |
| Zielbereich | kein Kolk verlässt durch ΔW den Bereich 0,8–1,35 m (Ausnahmeliste {3, 30} wie 6o) | Was der Spieler sieht, bleibt im Ziel. |
| Einzelabweichung > 4 cm | einzeln nennen; nur zulässig am Stufenfuß (Lippe direkt oberhalb, Fallhöhe ≥ 0,5 m) | Ein Ausreißer mitten im Becken wäre ein echtes Warnsignal. |
| mehr als 2 Kolke > 4 cm | nicht speichern, melden | Dann ist es kein Einzelfall mehr. |

T6N1_2: Median 0,0 cm; Kolk 25 mit 0,945 → 1,045 m im Ziel; Stufenfuß s 492,1, W − Plan +16 cm. **Bestanden.**

## 2. Übernehmen, ohne neu auszuwürfeln

- Ist T6N1_2 noch ungespeichert im Speicher, ist er der geprüfte Stand. Dann speichern: Speicherbeleg, BAKED_SIM ist zurückgelesen.
- Ist er schon verworfen (der Neustart war angekündigt), T6N1b mit identischer Kette laufen lassen und mit dem neuen Kriterium abnehmen.
  Gegen T6M3A_2 vergleichen, nicht gegen T6N1_2. **Ergebnisoffen:** Bestehen alle Tore, wird gespeichert, auch wenn Kolk 25 wieder anders
  liegt. Fällt ein Tor durch, wird nicht gespeichert und gemeldet. Ein dritter Lauf, nur um einen Wunschwert zu treffen, ist nicht
  zulässig.
- **Freigabe:** 6o verlangt Ferats Freigabe anhand der Bildpaare. Die Bilder hat er bekommen. Ob seine pauschale Freigabe vom 18.10. („Was
  Cloud empfiehlt, kannst übernehmen“) diese Freigabe abdeckt, entscheidet Opus-PM. Unsere Empfehlung lautet: speichern.
- **Bildbefund:** Ich habe die Bildpaare selbst angesehen; sie stützen die Übernahme.
  - K1: keine Treppe, keine Spalte.
  - K4 (Kolk 36): Mit Breite 1 sind an der Stufe weniger weiße Flecken zu sehen, und die Stufe ist voll hoch.
  - K5 und Mündung: praktisch gleich.
  - `bett_ufer`: Mit Breite 1 ist der Grund klarer zu erkennen.

  Ein Bildfehler durch Breite 1 ist mir nicht aufgefallen.
- Nach dem Speichern gilt **Breite 1 für die SWR p2**, und der Kantenbewuchs ist frei (6o §4.3).

## 3. Kolk 25: Diagnose, offline

Kolk 25 liegt am Fuß einer Stufe. Dort kann der Wechselsprung des Strahls zwei fast gleichwertige Lagen haben: Er wird entweder vom
Unterwasser überdeckt oder liegt frei weiter unten. Je nach Lage steht der Spiegel im Kolk um einige Zentimeter bis Dezimeter anders. Das
passt zu einer diskreten Stufe statt eines Rauschens und dazu, dass nur dieser Kolk betroffen ist.

Prüfung an den zwei vorhandenen Dumps T6M3A_2 und T6N1_2, ohne Editor:

1. **Differenzkarte ΔW und ΔG** im Umkreis von 15 m um s 492. Erwartet wird, dass die Abweichung auf den Kolk und das Gebiet direkt
   unterhalb begrenzt ist (wenige Dutzend Zellen) und oberhalb der Lippe 0 cm beträgt.
2. **Profil entlang der Achse** s 488–498: W, G und die Geschwindigkeit, falls sie im Dump steht. Erwartet wird, dass die Stelle mit
   Froude ≈ 1 (Sprung) zwischen den Läufen um 1–2 Zellen versetzt ist.
3. **Gegencheck:** Gilt das Bild aus 1 und 2, ist die Lage bistabil. Bleibt die Abweichung dagegen nicht örtlich begrenzt, Rolle 1
   melden. Dann ist etwas an der Kette nicht reproduzierbar.

Folge nur bei Bistabilität und nur, falls sie sichtbar stört: Kolk 25 bekommt etwas mehr Tiefe oder eine Lippe mit klarerer Fallkante im
Bettplan. Das ist ein Bettplan-Thema und kein Grund, die Breite zu ändern.

## 4. Nächste Handlung (eine, lokal)

**Speichern (T6N1_2) bzw. T6N1b laufen lassen und speichern.**

- **Abnahme:** G1, G2′a/b, G3, Kernbett ≥ 99 %, Front 788 m, K-Kolk nach §1, BAKED_SIM zurückgelesen, Speicherbeleg.
- **Abbruch:** ein Tor verfehlt, oder mehr als 2 Kolke > 4 cm.
- Die Diagnose zu Kolk 25 (§3) läuft unabhängig davon offline.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Kolk 36 auf Planspiegel bringen.** Ein halber Meter fehlende Beckentiefe direkt unter der Hauptstufe fällt auf, sobald Breite 5 ihn
   nicht mehr zumalt.
2. **Kantenbewuchs an den jetzt nassen, scharfen Kanten.** Erst mit gespeicherter Breite 1 sinnvoll; das ist der nächste sichtbare Schritt.
3. **Fallschaum nur an echten Fällen (Lippe 8).** Er sollte über Niagara und Aufprall gesteuert werden, nicht über die Glättung (6n §3).

## Quellen

- `recherche/antworten/16h-nachtrag6o-t6n2-u3-g2-tor.md` §1.3, §4.2, §4.3 (Commit f2bb485)
- `recherche/antworten/16h-nachtrag6n-schritt3a-verschwindet.md` §2.5 (Commit 73b2ac5)
- `recherche/vorlagen/pruefung.md`, Abschnitt Messwerkzeuge
- `recherche/bilder/swr_p2/t6n1_bildpaare.jpg` (Commit 86a5adc), selbst angesehen

## Rückfragen

Keine.
