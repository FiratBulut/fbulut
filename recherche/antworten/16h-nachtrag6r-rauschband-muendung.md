# Antwort 16h-6r – Schwelle = max(Rauschband, 1 Stufe); Sägezahn-Test mit Klammer um den Ist-Offset, `UseBakedSim` getrennt; neue Referenz T6N1b_2 statt Ursachensuche

Gelesen: recherche/auftraege/16h-nachtrag6r-rauschband-muendung.md @ 04499b5fd73062e8d9b2b8213faf5e35c7be3b1d (Commit 2a27e52)

Stand 19.10.2026. Bezug: Antwort 16h-6q (1868e8f) §1, §2, §4, §5. Bearbeiter: Cloud-Recherche. Bereich: SWR p2, gespeicherter Stand `T6N1b_2`,
Wassermaterial `M_Eldarien_Wasser_Schaum8` / `MI_EL_SWR_Klar`.

## Kurzfazit

1. **Zwei Fehler von uns in 6q:**
   - Wir hatten angenommen, T6N1_2 gegen T6M3A_2 enthalte den Einfluss der Breite. Beide liefen mit Breite 1.
   - Wir hatten erwartet, das Rauschband an der Mündung liege deutlich über einer Rundungsstufe. Es liegt genau auf einer Stufe.

   Eure Messung ersetzt beides.
2. **Befundschwelle – beantwortet:**
   - Für Zonenwerte (Median, p95, Anteile) gilt **max(p95 der Zone, 1 Half-Float-Stufe der Zone)**.
   - Für Einzeltexel und Einzelkolke gilt **max(p99 der Zone, 1 Stufe)**. In der Bergrinne sind das 8 cm.
   - Die nachträglich ergänzte Stufenregel von Rolle 1 ist damit bestätigt (§1).
3. **Mündung – beantwortet:** R1 am Auslass ist belegt. Die letzten 20 m vor dem Auslass gehen in keine Entscheidung ein. An der Simulation
   ist nichts zu tun. Die Ost-Arm-Fläche liegt im Band (p95 eine Stufe); sie wird nicht weiter untersucht.
4. **Sägezahn-Test – beantwortet:**
   - `Water Opacity Mask Offset` in einer Klammer um den Ist-Wert −24: −48 / −12 / 0, dazu die Kontrolle −24.
   - Zuerst nur dieser eine Parameter. `UseBakedSim` als **eigene** zweite Variable mit allen vier Kameras, weil er das Wasserbild auch an
     den Kolken ändern kann.
   - Zulässig ist, was den Sägezahn nimmt und K1/K4/K5 nicht verschlechtert (§2).
5. **T6N1_2 gegen T6M3A_2 – beantwortet:** Nicht weiter klären. Referenz für K-Kolk ist ab jetzt der gespeicherte Stand `T6N1b_2`; damit spielt
   der alte Unterschied für keine künftige Entscheidung eine Rolle. Höchstens die Eingabe-Manifeste beider Läufe einmal vergleichen, ohne
   neuen Lauf (§3).
6. **Nächste Handlung:** Sägezahn-Test nur im Speicher, wie der Streifen-Test (§4).

---

## 1. Schwelle für Befunde

| Größe | Schwelle „Befund“ | Grund |
|---|---|---|
| Zonenwert (Median/p95 \|ΔW\|, \|ΔG\|) | > max(p95 Zone, 1 Stufe) | Dort, wo p95 = 0 ist, misst sonst jede Rundung einen Befund |
| Anteil `sichtbar_1`-Wechsel, G1, G3, Kernbett | > 2 × Rauschanteil der Zone (z. B. Talkaskade > 0,2 %) | Wechselanteile sind Zählungen und haben eine eigene Streuung |
| Einzeltexel, einzelner Kolk | > max(p99 Zone, 1 Stufe) | Ein Einzelwert muss am Rand der Verteilung gemessen werden, nicht in ihrer Mitte |
| letzte 20 m vor dem Auslass | keine Entscheidung | R1 belegt (55,6 % der Texel im 0–5-m-Band weichen ab) |

- Die Stufe bestimmt sich je Zone aus dem Wertebereich der gespeicherten Größe; sie ist also nicht überall 0,25 cm.
- K-Kolk bleibt unverändert. Ein Kolk über 4 cm liegt in der Talkaskade über p99 (2 cm), die Regel ist also mit dem Band verträglich.

## 2. Sägezahn: Test mit dem Tiefeneingang

**Annahme zur Wirkung [Annahme, aus eurer Beschreibung]:** `WaterOpacityMaskFromDepth` macht flaches Wasser durchsichtig. Die Zähne des
Sägezahns sind die Randtexel mit wenigen Zentimetern Wasser. Werden sie durchsichtig, verschwindet die Kante.

- Ob die Maske die Tiefe aus der Szenentiefe nimmt (Wasserfläche gegen Grund) oder aus G, wisst ihr erst nach dem Test.
- Im ersten Fall wirkt sie unabhängig von BAKED_SIM.

**Ablauf:** nur im Speicher, Kopie von `MI_EL_SWR_Klar`, danach Neustart ohne Speichern, 0 ungespeichert bestätigen.

| Stufe | Offset | Zweck |
|---|---:|---|
| Kontrolle | −24 (Ist) | Testweg gültig, Bild = Ist |
| A | −48 | eine Richtung |
| B | −12 | andere Richtung |
| C | 0 | Grenzwert |

- Das Vorzeichen der Wirkung ist unbekannt. Deshalb liegt die Klammer auf beiden Seiten des Ist-Werts. Erst wenn eine Richtung wirkt, wird in
  ihr nachgestuft.
- **Kameras:** Mündung, K1, K4, K5, gleiches Licht (wie 6q: Sonne −24°/−20°, 100 000 lx).
- **Erfolg:**
  - An der Mündungskamera ist der Sägezahn nicht mehr als Treppe lesbar.
  - K4/K5: Klarheit und dunkle Stufen unverändert, keine neuen durchsichtigen Löcher im tiefen Wasser.
  - K1 ohne neue Lücke.
- **Abbruch bzw. anderer Weg:** Wirkt keine Stufe auf den Sägezahn, dann ist er Geometrie und keine Deckkraftfrage. Dann den Rand durch einen
  feuchten Saum bzw. eine Nasslinie am Ufer verdecken (RVT/Decal). Schaum bleibt ausgeschlossen.

**`UseBakedSim`:**

- Erst nach dem Offset-Test, als eigener Schritt mit dem besten Offset: an und aus, an allen vier Kameras.
- Zulässig ist er nur, wenn sich außer dem Rand nichts sichtbar ändert, also Kolk-Farbe, Klarheit und Strömungsnormalen gleich bleiben.
- Was der Schalter im Master sonst noch umschaltet, ist im Graphen nachzusehen (**zu prüfen**). Wir kennen den Master nicht.

## 3. T6N1_2 gegen T6M3A_2

- Die 27 % über dem Band zeigen: Die Eingaben beider Läufe unterscheiden sich. Für die Abnahme spielt das keine Rolle mehr:
  - T6N1b ist gespeichert und mit K-Kolk gegen T6M3A_2 bestanden; die Talkaskade liegt im Band.
  - Künftige Läufe werden gegen `T6N1b_2` verglichen.
- **Billigster Schritt, optional:** die festgehaltenen Eingaben (Hindernisliste, Spline-Stand, Parameter) beider Läufe per SHA vergleichen.
  Findet sich ein Unterschied, wird er im Bericht vermerkt. Kein neuer Lauf.

## 4. Nächste Handlung (eine, im Editor nur im Speicher)

**Sägezahn-Test nach §2:** zuerst Kontrolle und drei Offset-Stufen, dann `UseBakedSim` als zweiter Schritt.

- **Ergebnis:** Bildreihe mit 4 Kameras × Stufen und Urteil nach den Erfolgskriterien.
- **Ein Wert ist erst nach Bildbefund und Freigabe festzulegen**, mit Speicherbeleg für das MI. Die Rücknahme ist der alte Wert.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Weicher Wasserrand:** Durchsichtiges Flachwasser am Ufer und eine Nasslinie nehmen der Mündung den Simulationsraster-Look. Das ist der
   größte sichtbare Gewinn bei kleinstem Eingriff.
2. **Kantenbewuchs** an den nassen Kanten (frei seit 6q).
3. **Steine im Wasser** (16h-Bettschritt, neuer Bake) und **Kolk 36 auf Planspiegel** (6o §1.3).

## Quellen

- `recherche/auftraege/16h-nachtrag6r-rauschband-muendung.md` (Commit 2a27e52)
- `recherche/antworten/16h-nachtrag6q-t6n1b-gespeichert-laufstreuung.md` §1, §2, §4 (Commit 1868e8f)
- `recherche/antworten/16h-nachtrag6p-t6n1-kolk25.md` §1, K-Kolk (Commit 8455b38)
- Wirkung von `WaterOpacityMaskFromDepth` nur laut Auftrag §5 („laut Epic“). Eine Websuche nach dem Funktionsnamen fand keine Quelle, die ihn
  beschreibt; deshalb ist der Test als Klammer angelegt. Nur verwandt: Epic-Issue UE-170168, wonach eine tiefenbasierte Opacity Mask bei
  niedriger Schattenqualität verschwindet (<https://issues.unrealengine.com/issue/UE-170168>). Beim Test daher die Schattenqualität der
  Kamera festhalten.

## Rückfragen

Keine.
