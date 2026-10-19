# Antwort 23h – Haufen nach Form, Wandmodule ohne Durchdringungsfehler, Kulisse ab 15 m nach Halt und Sichtbarkeit, offene Netze über den offenen Rand

Gelesen: recherche/auftraege/23h-dreiecke-stufe-b-rueckfragen.md @ 71048a7b553ab08d786321fffe7fbb86858dd345 (Commit 82304f6)

Stand 19.10.2026. Bezug: Antworten 23e/23f/23g, 22f §3.7, Regeln 23.9 (`regeln_23i_d3ce026a`). Bearbeiter: Cloud-Recherche. Bereich: Sitzprüfung
Stufe B in C2, Wandfelsen, Haufen-Netze. Neue Regelversion **23.10** (Block `nachtrag_23_10`); lokal ausdrücklich zu übernehmen.

## Kurzfazit

1. **SmallStonesPack – beantwortet:** Unser Kriterium „ab 8 getrennten Inseln“ war die falsche Prüfgröße; ein Haufen kann als eine
   geschlossene Hülle modelliert sein. Das war unser Fehler (22f §3.7). Neu entscheidet die **Form** aus den Dreiecken:
   - flache Basis: ≥ 60 % der Unterseite ≤ 1 cm an der Ausgleichsebene;
   - mindestens 5 Kuppen oben;
   - kalibriert an `_01`/`_03`, die nach Bild Haufen sind.

   Das gilt nur noch außerhalb von Kies ≥ 0,5 (23.9). Die Form bestimmt das Eingraben, die Größe bestimmt Toleranzen und Zählung (§1).
2. **Wandmodule – beantwortet:** Zwei Felsen ≥ 4 m derselben Familie oder gleicher Helligkeit dürfen sich durchdringen. Das ist der Zweck
   von Klippenmodulen. Statt FEHLER `durchdringung` gibt es nur eine **WARNUNG „naht“** bei Splittern unter 10 cm oder fremder Farbe (§2).
3. **55360 / 21633 – beantwortet:** Ab **15 m** sind Felsen Kulisse, keine Stücke. Geprüft wird auf Halt (Kontakt unten oder als Klemmblock
   an zwei Seiten) und darauf, ob die Luft von begehbaren Punkten aus sichtbar ist.
   - Nur sichtbare Luft ohne Halt ist FEHLER.
   - Reparatur: zuerst Netztausch, dann Drehen oder Versetzen in der Wand, als Letztes Entfernen (§3).
   - 55360 sah in 23f im Bild wie ein Klemmblock aus; das prüft die Halt-Regel jetzt messbar.
4. **Offene Netze – beantwortet:** Hohlraum und Deckung sind bei ihnen bedeutungslos. Entscheidend ist der **offene Rand**: Liegt er überall
   ≥ 2 cm unter der Bezugsfläche, ist das Netz ok. Ragt er heraus, sieht man in das Netz hinein, also FEHLER „offener_rand“. Code mit
   Würfeltest in §4.
5. **C2:85197 – beantwortet:** Ab 15 cm Lücke entscheiden die Dreiecke allein, also gilt FEHLER. Vorher ist zu prüfen, ob das Netz offen ist;
   dann gilt Punkt 4. Ein Bild aus der Ferne ist eine Bestätigung, keine Bedingung (§5).
6. **30 Stücke in trockenen Bettzellen – beantwortet:** Sie **bleiben**. Sie sind Teil des Bakes `T6N1b_2`. Neues mit Kollision wird dort
   nicht gesetzt. Der Bestand wird im 16h-Bettschritt mit neuem Bake bewertet (§6).
7. **Zonen auf `T6N1b_2`:** Die Kantenverschiebung beträgt 0,06 m, der Plan bleibt. Damit ist 6q §3 erledigt.

---

## 1. Haufen nach Form (Regel 23.10 `haufen_nach_form`)

| Merkmal (Dreiecks-Hülle, 1-cm-Raster) | Haufen | Einzelkiesel |
|---|---|---|
| (a) Unterseite: Anteil der Zellen ≤ 1 cm über der Ausgleichsebene der Unterseite | ≥ 60 % (flache Basis) | klein (runde Unterseite) |
| (b) Oberseite: lokale Maxima mit ≥ 1 cm Prägnanz | ≥ 5 | 1–2 |

- **Kalibrierung:** `_01` und `_03` müssen als Haufen gelten (Bild `kpb1_kiesel_zoom`). Trennen (a) und (b) sie nicht von einem Einzelkiesel,
  dann eine Nahaufnahme je Netz.
- **Form gegen Größe:**
  - Die Form bestimmt das Eingraben: Haufen 10–20 %, Basis unsichtbar.
  - Die Größe (L × Skala) bestimmt Toleranzen und Zählung.
  - Die 1 055 SmallStonesPack-Instanzen der Größe „stein“ werden also wie Haufen eingegraben, mit den Lücken-Toleranzen für Stein. Ein
    Haufen bleibt ein Haufen, auch wenn er groß skaliert ist.
- **Geltung:** Nur außerhalb von Kies ≥ 0,5. Dort zeigt die Lage den Kies (23.9).

## 2. Wandmodule (Regel 23.10 `wand_module`)

Die Regel `durchdringung` aus 23 sollte verhindern, dass zwei Blöcke wie ein verschmolzener Körper wirken. Bei Klippenmodulen ist genau das
gewollt: Sie bilden zusammen eine Wand.

| Paar | Urteil |
|---|---|
| beide ≥ 4 m **und** gleiche Familie (Netzname ohne Ziffernsuffix) oder Helligkeitsunterschied ≤ 0,10 Y | keine `durchdringung` |
| … aber ein Teil tritt mit < 0,10 m Dicke durch die Oberfläche des anderen (Splitter) | WARNUNG „naht“ |
| … verschiedene Familien und Y-Differenz > 0,10 | WARNUNG „naht“ (Farbnaht sichtbar) |
| ein Stück < 4 m | `durchdringung` wie bisher |

- Die 64 Wandfelsen, die die Überhang-Bedingungen erfüllen und nur an `durchdringung` hängen, werden damit zur WARNUNG „ueberhang“.
- Die Naht-Warnungen werden im Bild an je einer Kamera pro Wandgruppe beurteilt.

## 3. Kulisse ab 15 m (Regel 23.10 `kulisse`)

**Warum eine Grenze:** Die Sitzregeln (Eingraben, Lücke im Kern) beschreiben Stücke, die auf dem Boden liegen. Ein Fels von 21,7 m bzw.
32,1 m ist ein Baustein einer Klippe. Bei ihm zählt, ob er gehalten wirkt und ob man unter ihn sieht.

| Prüfung | Festlegung |
|---|---|
| Halt | Kontakt (d ≤ 5 cm) unten mit Gelände oder Fels ≥ 4 m, **oder** seitlich an zwei gegenüberliegenden Stellen (Kontaktsektoren ≥ 120° auseinander im Grundriss): Klemmblock |
| Sichtbarkeit | Raster 10 m über begehbare Punkte (Hang ≤ 35°, Augenhöhe 1,7 m, bis 200 m). Die Luft unter dem Stück ist nur dann FEHLER, wenn sie von dort aus sichtbar ist; sonst WARNUNG |
| Reparatur | 1. Netztausch gegen eine Variante mit passender Basis. 2. Drehen oder Versetzen in der Wand, bis Halt erfüllt ist. 3. Entfernen, wenn die Wand ohne das Stück im Bild geschlossen bleibt |

- **55360:** In 23f §4 wirkte es im Bild wie ein Block zwischen zwei Wänden. Der Kontaktanteil 0,11 misst nur die Unterseite. Die
  Seitenkontakte entscheiden, ob es ein Klemmblock ist.
- **21633** (Kontakt 0,34): Halt und Sichtbarkeit rechnen.
- Erst danach entscheidet die Reparaturreihenfolge.

## 4. Offene Netze (Regel 23.10 `offene_netze`)

- **Fehlt der Boden,** treffen die Strahlen von unten die Innenseite der Oberschale. Der „Hohlraum“ ist dann das Netzinnere, und Hohlraum ≈ 1
  bei Deckung ≈ 0 sagt nichts aus.
- **Sichtbar ist nur der offene Rand.** Liegt er über dem Boden, sieht man durch das Loch ins Innere; Rückseiten werden dabei weggelassen.
- **Regel:**
  - Randpunkte aller offenen Kanten alle 5 cm prüfen. Alle müssen ≤ −0,02 m unter der Bezugsfläche S liegen (23.9) bzw. unter dem Träger.
  - Sonst FEHLER „offener_rand“.
  - Für offene Netze geht diese Regel vor `luecke` und `deckung`.
- **C2:102247:** nach dieser Regel neu urteilen.

Selbst ausgeführt: Würfeltest. Geschlossen ergibt 0 Randpunkte. Ohne Boden ergeben sich 4 offene Kanten, alle auf z = 0. Texturnähte werden
vorher verschweißt.

```python
# offener_rand.py (23.10) – Randpunkte offener Kanten; lokale Koordinaten in m, danach mit Inst.welt() in die Welt
import math
from collections import Counter

def schweissen(punkte, dreiecke, eps=1e-4):
    """gleiche Positionen (auf eps gerundet) zu einem Index zusammenfassen (Texturnaehte)."""
    key = lambda p: tuple(round(c / eps) for c in p); neu, idx = {}, []
    for p in punkte: idx.append(neu.setdefault(key(p), len(neu)))
    pos = [None] * len(neu)
    for p, i in zip(punkte, idx): pos[i] = p
    return pos, [(idx[a], idx[b], idx[c]) for a, b, c in dreiecke]

def offene_kanten(dreiecke):
    n = Counter(tuple(sorted(e)) for a, b, c in dreiecke for e in ((a, b), (b, c), (c, a)))
    return [e for e, k in n.items() if k == 1]

def randpunkte(punkte, dreiecke, schritt=0.05):
    pos, tri = schweissen(punkte, dreiecke)
    out = []
    for a, b in offene_kanten(tri):
        pa, pb = pos[a], pos[b]; L = math.dist(pa, pb); n = max(1, int(L / schritt))
        out += [tuple(pa[k] + (pb[k] - pa[k]) * t / n for k in range(3)) for t in range(n + 1)]
    return out          # leer = geschlossenes Netz

# Urteil je Instanz:
# rand = [i.welt(p) for p in randpunkte(netz_punkte, netz_dreiecke)]
# offen_fehler = any(p[2] - welt.H(p[0], p[1]) > -0.02 for p in rand)
```

## 5. C2:85197

- Die Lücke ist von 2,2 auf 56,6 cm gesprungen. Das passt zu einer Unterseite, die die ausgedünnte Eckpunkt-Hülle nicht erfasst hatte.
- **Erst prüfen, ob das Netz zu den 66 offenen gehört.** Wenn ja, gilt §4.
- Ist das Netz geschlossen, entscheiden ab 15 cm die Dreiecke (23.10 `dreiecke_entscheiden`) → FEHLER Lücke, reparieren wie üblich.
  - Ein Bild aus 20–40 m mit freier Sicht ist eine Bestätigung, aber keine Bedingung.
  - Eine Abweichung des Nanite-Ersatznetzes um 50 cm wäre ungewöhnlich grob [Annahme].

## 6. Trockene Bettzellen: Bestand bleibt

- 23.7 regelte **neue** Platzierungen. Die 30 Stücke mit Kollision standen schon beim Bake von `T6N1b_2` dort und gehören zu dessen
  Hindernisfeld. Ein Entfernen würde den gespeicherten, abgenommenen Stand verändern.
- **Entscheidung:** Sie bleiben. Der Planer setzt dort nichts Neues mit Kollision. Im 16h-Bettschritt mit neuem Bake werden sie mitbewertet.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Klippen als Komposition:** Modulwände dürfen ineinandergreifen. Entscheidend sind Nähte ohne Farbsprung und Splitter, und am Fuß
   Blockschutt statt Luft.
2. **Keine Löcher in offenen Netzen:** Ein sichtbarer offener Rand wirkt aus der Nähe wie ein Loch und ist schlimmer als eine kleine Lücke.
   Die neue Regel findet ihn gezielt.
3. **Klemmblöcke als Bildmotiv:** In Schluchten wirken verkeilte Blöcke über einem Spalt sehr gut, wenn sie messbar an beiden Wänden anliegen.
4. **Hang 3–10 m** bleibt der größte Fehlbetrag (10,6/10,8 m² je 10 m): Planer-Neulauf mit Stücken ≥ 1 m.

## Quellen

- `recherche/auftraege/23h-dreiecke-stufe-b-rueckfragen.md` (Commit 82304f6)
- `recherche/antworten/23-steine-organisch-im-boden.md`: `durchdringung`, Stapelregeln (Commit 264a4d8)
- `recherche/antworten/23f-t23e-ergebnisse-rueckfragen.md` §2, §4 (Commit 39fb460)
- `recherche/antworten/23g-kies-verdraengung-streifen.md`: Bezugsfläche S (Commit 7386f14)
- `recherche/antworten/22f-t22-f6-2-r004-lily-rueckfragen.md` §3.7 (Commit fdd7f1a)
- `recherche/antworten/steine_sitz_regeln.json`: jetzt 23.10, Block `nachtrag_23_10`

## Rückfragen

Keine, die den nächsten Schritt ändern.
