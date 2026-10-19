# Auftrag 23g – Die „Streifen an Rundsteinen“ (23f §4) sind Nanite-Verdrängung der Landschaftslage Kies; Editor-Test belegt; Zielwert und Folgen für die Sitzprüfung

Stand 19.10.2026, 08:40 PC-Uhr. Bezug: Antwort 23f §4 (Bild C2_64801) und „Was fehlt bis Witcher 4“ Punkt 2.

## 1. Befund (Rolle 3 offline, Opus-PM im Editor bestätigt)

- **Keine Netze im gestreiften Bereich.** Der Zensus, ins Bild projiziert, zeigt im Vordergrund keine einzige Instanz. C2:64801 ist die dunkle Platte
  (`SM_mountain_rock_big_02_1`, Maßstab 0,25).
- **Ursache:** Das Landschaftsmaterial (Master V18b/V18bs, Kette seit V12) verdrängt per Nanite-Tessellation.
  - Volle Tiefe 45 cm; der Anteil der Lage Kies ist fest 0,7, das ergibt **31,5 cm Hub**.
  - Höhe und Farbe kommen von oben aus Welt-XY (`T_ground_big_pebbles_01`, Kachel 2,5 m).
  - Die Seitenprojektion hängt an der unverdrängten Normale und greift auf flachem Boden nie.
  - Folge: An den steilen Flanken der hochgedrückten „Steine“ wird dieselbe Texelreihe senkrecht gestreckt.
- **Umfang:** Kies ≥ 50 % auf 27,6 ha in 38 Feldern (C3 5,2 · G3 3,3 · B4 2,8 · H4 2,6 · D3 2,6 · H3 2,1 · C4 1,7 · C2 1,3 ha …). Betroffen sind nur
  MI_V12/V12s, keine Foliage-Typen.

## 2. Editor-Test (nur im Speicher, danach harter Neustart ohne Speichern, 0 ungespeichert bestätigt)

Ein Landschaftsteil um drei feste Kameras bekam eine Kopie seines MI mit Override „Displacement Scaling“.

| Stufe | Magnitude | Kies-Hub | Flanken > 45° (offline) | Streckung p99 | Bild |
|---|---:|---:|---:|---:|---|
| Ist | 0,225 | 31,5 cm | 58 % | 6,5 | starke senkrechte Streifen |
| Kontrolle (Kopie mit Ist-Wert) | 0,225 | 31,5 cm | – | – | gleich dem Ist (nur Wolken/Gras bewegt) → Testweg gültig |
| T3 | 0,11 | 15,4 cm | 17 % | 3,3 | Streifen stark verringert, Kies noch plastisch |
| T2 | 0,08 | 11,2 cm | 9 % | 2,5 | Streifen fast weg, leichtes Relief |
| T1 | 0 | 0 | 0 | 1 | ganz flach, Kies wirkt aufgemalt |

- Nanite war bei jedem Schritt aktuell („offen 0 von 73“).
- Shaderfehler und SRV-Meldungen: 0.
- Bild: `bilder/platzierung/streifen/str_reihe.jpg`, Spalten Ist / 0,11 / 0,08 / 0. Kameras: C2_64801, nah mit Sonne im Rücken, Spielerhöhe 7 m.

**Geplante Umsetzung (noch nicht gebaut):** Kopie V18c/V18cs von V18b/V18bs. Die Konstante 0,7 der Kies-Kette wird zum Parameter `Disp_Anteil_Kies`
(Vorgabe 0,7 = bitgleich, kein neuer Sampler). Zielwert = 0,7 × Magnitude / 0,225, also 0,25 (bei 0,08) bzw. 0,34 (bei 0,11). Die übrigen Lagen
(Fels 45 cm, andere ≤ 8 cm) bleiben.

## 3. Folge für die Sitzprüfung (23.x)

Die sichtbare Oberfläche in Kiesflächen liegt bis zu 31,5 cm (bei 0,08: 11 cm) über `hoehe.f32`, gegen das wir messen.
- Ein Stein, der nach unserer Rechnung 10 cm im Boden steckt, kann im Bild bis zu 21 cm tiefer im „Kies“ sitzen.
- Kleine Kiesel können ganz verschwinden.
- Umgekehrt: Lücken unter Platten auf Kiesflächen wirken im Bild kleiner oder verschwinden. Beispiel 64801: Mit Hub 0 liegt die Platte sichtbar auf
  flachem Boden.

## 4. Fragen

1. **Zielwert:** 0,08 (11 cm) oder 0,11 (15 cm), oder dazwischen? Kriterium: Streifen nicht mehr erkennbar aus Spielerhöhe, Kies noch plastisch.
2. **Andere Lagen:** Fels hat dieselbe Kette mit 45 cm Hub. An steilen Felsflanken greift die Seitenprojektion, auf flachen Felsplatten nicht. Sollen
   wir Fels ebenso prüfen (Flankenkennzahl je Lage und Bild)?
3. **Sitzprüfung:** Soll die Verdrängung in den Bezug der Sitzprüfung, also Oberfläche = h + Hub × (Höhentextur − 0,5) × Lagengewicht? Oder reicht
   es, den Hub so klein zu machen, dass der Fehler unter der Toleranz liegt (bei 0,08 noch ± 5,6 cm)?
4. **Reihenfolge:** Erst V18c bauen und den Wert weltweit setzen (mit Bildprüfung in 3–4 Kiesfeldern), dann die Planer-Neuläufe? Oder unabhängig?
