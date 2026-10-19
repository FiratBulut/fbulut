# Antwort 16h-6q – T6N1b angenommen; Laufstreuung einmal als Rauschband aus vorhandenen Dumps messen; T6N1b_2 ist jetzt Bezug

Gelesen: recherche/auftraege/16h-nachtrag6q-t6n1b-gespeichert-laufstreuung.md @ 1e19b94ba45026e0c176ae3fc1b7686e3d0f21ec (Commit 7012f26)

Stand 19.10.2026. Bezug: 16h-6p (8455b38) §1–§4, 6o (f2bb485) §4.2/§4.3, Antworten 23e/23f (Zonenbezug). Bearbeiter: Cloud-Recherche.
Bereich: SWR p2, gespeicherter Stand `T6N1b_2` (Breite 1). Bild `bilder/swr_p2/t6n1b_bildpaare.jpg` selbst angesehen (§4).

## Kurzfazit

1. **T6N1b ist angenommen.** Alle Tore und K-Kolk sind bestanden, der Stand ist gespeichert und nach Neuladen bitgleich bestätigt. Damit
   sind die Punkte aus 6o §4.3 frei:
   - Breite 1 gilt für die SWR p2.
   - Kantenbewuchs ist frei.
   - Der 16h-Bettschritt (Steine im Wasser, neuer Bake) ist frei.
2. **Auslegung N2 – bestätigt:** Für den Zielbereich in K-Kolk gilt dieselbe Lesart wie bei G2′a: eine Half-Float-Stufe Toleranz und die
   Gelände-Ausnahmen {3, 30}. 6p hätte das ausdrücklich nennen müssen.
3. **Frage 1 – beantwortet:** K-Kolk gegen den Referenzlauf bleibt das Tor. Das Rauschband wird **einmal** gemessen, aus den Dumps, die es
   schon gibt: T6N1_2 und T6N1b_2 haben dieselben Eingaben. Ein dritter Lauf ist nicht nötig. Künftig gilt eine Abweichung nur als Befund,
   wenn sie über dem Rauschband ihrer Zone liegt (§1).
4. **Frage 2 – wartet auf Beleg:** Zwei Ursachen sind möglich: der Rand zum C3-Fluss (Senke/Nachfüllen) und die Empfindlichkeit an
   Nass-trocken-Fronten in flachem, breitem Wasser. Dieselbe Differenzkarte unterscheidet sie offline (§2). Die Zeitschritt-Vermutung wird
   nur verfolgt, wenn eine Entscheidung an der Mündung davon abhängt.
5. **Frage 3 – beantwortet:** Ja, `T6N1b_2` ist ab jetzt der Bezug für die Zonen der Steinplanung (23f).
   - Weil die Breite die sichtbare Wasserkante kaum verschiebt (23f), wird keine Neuplanung erwartet.
   - Gemessen wird die Verschiebung der Kante gegen T6N1_0; über 0,3 m im Median wird neu geplant.
6. **Neuer Bildbefund:** An der Mündung ist der Sägezahn-Rand am rechten Ufer mit Breite 1 über eine längere Strecke sichtbar. Das ist
   kein Grund zurückzugehen, aber ein eigener Punkt: der Rand im Wassermaterial (§4).

---

## 1. Rauschband aus T6N1_2 gegen T6N1b_2

Beide Läufe haben dieselbe Kette und dieselbe Breite 1. Ihre Differenz ist deshalb reines Laufrauschen, ohne Parameteränderung. Der
Vergleich T6N1_2 gegen T6M3A_2 in eurer Tabelle enthält dagegen auch den Einfluss der Breite.

**Rechnung (offline, je Zone: Talkaskade s 390–578, Bergrinne, Mündung s 700–788, Rest):**

- p50, p95 und p99 von |ΔW| über nasse Texel (`sichtbar_1` in beiden);
- Anteil der Texel mit `sichtbar_1`-Wechsel (nass ↔ trocken);
- dasselbe für G.

**Gebrauch:**

- **Rauschband einer Zone** = p95 |ΔW|.
- Eine künftige Abweichung zwischen Referenz und neuem Lauf gilt in einer Zone erst als Befund, wenn sie dort p95 überschreitet. G1, G3,
  Kernbett und Front erhalten ihre Spanne aus dem Wechselanteil.
- **K-Kolk bleibt das Tor** für die Kolke; das Rauschband ersetzt es nicht.

**Erwartung [Annahme]:** In der Talkaskade liegt p95 unter einer Half-Float-Stufe, an der Mündung deutlich darüber.

## 2. Woher die Streuung an der Mündung kommt

| Ursache | Erwartetes Bild der Differenzkarte |
|---|---|
| R1 Rand/Senke zum C3-Fluss | \|ΔW\| fällt mit dem Abstand zur Auslassgrenze ab und ist am Rand am größten; auch tiefe Texel weichen ab |
| R2 Nass-trocken-Fronten | \|ΔW\| sitzt an Texeln mit kleiner Tiefe (G < 5 cm) und an `sichtbar_1`-Wechseln, unabhängig vom Abstand zum Rand |

**Rechnung mit T6N1_2 gegen T6N1b_2:**

- \|ΔW\| gegen den Abstand zur Auslassgrenze (Binning in 5 m);
- \|ΔW\| gegen die Tiefe G (Binning 0–2, 2–5, 5–20, > 20 cm).

**Folge je Ergebnis:**

- **Bei R1:** Den Auslass bzw. die Senke im Bericht festhalten. Am Rand nichts mehr messen, was davon abhängt.
- **Bei R2:** Das ist die Physik flacher Fronten. Keine Maßnahme an der Simulation, das Rauschband reicht.

**Zeitschritt:** Ob die Simulation am Editor-Zeitschritt hängt, prüft man nur mit zwei Läufen bei fester Bildrate (`t.MaxFPS`). Dass der
Bake dann bitgleich wird, ist **zu prüfen**. Das lohnt erst, wenn eine Entscheidung an der Mündung an Werten unter dem Rauschband hängt.
Heute ist das nicht der Fall.

## 3. Folgen für die Steinplanung (23e/23f)

- Bezug für die Zonen ist `sichtbar_1` von `T6N1b_2`.
- **Wenn der Planer-Neulauf (Plan-Modus) schon auf T6N1_0 lief:** die Zonen auf T6N1b_2 nachrechnen.
  - Kantenverschiebung im Median ≤ 0,3 m: Der Plan bleibt.
  - Sonst neu planen.
- **Wenn er noch nicht lief:** gleich auf T6N1b_2 rechnen.
- Die Sperre 23d (d) „kein Stück an SWR-Hindernissen oder im Wasser, solange T6N1 offen ist“ entfällt mit dem Speichern.
  - Stücke **mit Kollision im Wasser** bleiben trotzdem dem 16h-Bettschritt vorbehalten, denn sie ändern den Bake.
  - Trockene Bettzellen bleiben kollisionsfrei (23f §1.1).

## 4. Bildbefund (selbst angesehen, `t6n1b_bildpaare.jpg`)

| Kamera | Breite 5 → Breite 1 |
|---|---|
| K1 Ufer | praktisch gleich, keine Treppe |
| K4 Kolk 36 | Weiß an der Stufe verschwindet. Stattdessen liegt dort eine dunkle, nasse Felsfläche, wo der Wasserfilm reißt; ihr Umriss ist kantig. Das liest sich als nasser Fels und ist besser als weißer Schaum ohne Fall. |
| K5 Kolk 3 | Die Stufe ist dunkler, das Wasser klarer; gleichwertig bis besser |
| Mündung | Rechts sieht man in beiden Fassungen eine Sägezahnkante am Ufer. Mit Breite 1 reicht sie über eine längere Strecke stromauf. Breite 5 hatte sie durch die Glättung teilweise verdeckt. |

**Einordnung:** Die Sägezahnkante ist das Texelraster der Simulation an der Nass-trocken-Grenze. Die Glättung zurückzunehmen ist keine
Lösung, denn sie brachte den „Deckel“ (6n). Ansatz ist der Rand im Wassermaterial: Deckkraft bzw. Kante über die Wassertiefe am Rand
ausblenden (Tiefe aus G oder Szenentiefe).

- Ob das SWR-Material dafür einen Tiefen- oder Kanteneingang hat, ist **zu prüfen**.
- Eine Nasslinie bzw. ein feuchter Saum am Ufer (RVT/Decal) verdeckt den Rest.
- Schaum ist im Bach außer an Fällen ausgeschlossen und daher keine Option.

## 5. Nächste Handlung (eine, offline)

**Rauschband und Ursachenkarte aus T6N1_2 gegen T6N1b_2 (§1 und §2 in einem Lauf).**

**Erfolg:**

- Tabelle mit p50/p95/p99 und Wechselanteil je Zone, für W und G.
- Beide Binning-Kurven aus §2 mit Urteil R1 oder R2.
- Rauschband als feste Prüfeingabe mit SHA-256 abgelegt.

**Abbruch:** Weichen die beiden Dumps bitgleich nicht ab, gibt es kein Rauschen bei gleichen Eingaben. Dann melden, denn eure Tabelle
zeigt Abweichungen nur gegen T6M3A_2.

Unabhängig davon und schon frei: Kantenbewuchs (6o §4.3) und die Nachrechnung der Zonen auf T6N1b_2 (§3).

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Wasserrand ohne Sägezahn:** Die Mündung ist ein Schaubild mit weitem Blick. Ein weicher Rand über die Tiefe plus Nasslinie macht den
   größten sichtbaren Unterschied.
2. **Kantenbewuchs an den nassen, scharfen Kanten** (jetzt frei): Moos, Farn und Gras in Fugen über der Wasserlinie.
3. **Steine im Wasser** (16h-Bettschritt, neuer Bake): teils eingetauchte Blöcke an der Wasserlinie und Dachziegel in der Sohle.
4. **Kolk 36 auf Planspiegel** (6o §1.3, weiter offen).

## Quellen

- `recherche/auftraege/16h-nachtrag6q-t6n1b-gespeichert-laufstreuung.md` (Commit 7012f26), Bild `bilder/swr_p2/t6n1b_bildpaare.jpg`
  (selbst angesehen)
- `recherche/antworten/16h-nachtrag6p-t6n1-kolk25.md` §1–§4 (Commit 8455b38)
- `recherche/antworten/16h-nachtrag6o-t6n2-u3-g2-tor.md` §1.3, §4.2, §4.3 (Commit f2bb485)
- `recherche/antworten/16h-nachtrag6n-schritt3a-verschwindet.md`: Deckel durch Glättung (Commit 73b2ac5)
- `recherche/antworten/23f-t23e-ergebnisse-rueckfragen.md` §1.1, §5 (Commit 39fb460)

## Rückfragen

Keine.
