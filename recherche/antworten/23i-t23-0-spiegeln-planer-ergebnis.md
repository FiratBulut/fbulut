# Antwort 23i – Messweg bestätigt; Foliage nie spiegeln; Kante zweistufig (Land jetzt, Wasserlinie im Bettschritt); FEHLER-Altbestand und niedriger Bewuchs dürfen am Hang weichen; Neulauf sofort mit 23.10/23.11

Gelesen: recherche/auftraege/23i-t23-0-spiegeln-planer-ergebnis.md @ cb38d50ae998da17842bf51aa141d9a65d51f165 (Commit 64beaef)

Stand 19.10.2026. Bezug: 23d–23h, Regeln 23.10 (`regeln_23j_d659d753`), jetzt **23.11** (Block `nachtrag_23_11`). Bearbeiter: Cloud-Recherche.
Bilder `bilder/platzierung/t23/t23_0_kontrollfaelle.jpg`, `t23b_spiegel_boegen_1.jpg`, `_2.jpg` selbst angesehen.

## Kurzfazit

1. **T23-0 Fassung 2 – angenommen:** Der Messweg ist im Editor belegt. K31 bestätigt unsere Diagonale, alle Fälle liegen in der Toleranz.
2. **Korrektur SmallStonesPack (unser Fehler):** Im Bild K8 ist `_01` ein einzelner runder Stein; die Dreiecke aus 23h zeigen eine
   geschlossene Hülle. Unser „Haufen“ aus 22e/23.5 beruhte auf einer falschen Bilddeutung.
   - Neu (23.11): Alle `SmallStonesPack` gelten als `kiesel` mit 40–60 % Eingraben.
   - Die Klasse `kiesel_haufen` bleibt für echte Haufen-Netze bestehen; heute ist keines bekannt.
   - Der eine F6-Kiesel aus r004 wird nach `kiesel` gesetzt.
3. **Spiegeln – beantwortet:** **Foliage nie spiegeln, nur Akteure.** Das zeigen eure Bilder:
   - Stein-Foliage gespiegelt: nur ein dünner Bogen sichtbar.
   - Baum-Foliage auf dem Rückfallweg: hohl.

   Der Rückfallweg greift auch bei Nanite-Netzen, z. B. für Strahlverfolgung oder ohne Nanite. Ersatz: Yaw frei, Skalenvarianz,
   Familienrotation, kleine Neigung, wo der Sitz es erlaubt. Bestehende gespiegelte Foliage wird umgestellt (§2).
4. **Kante – beantwortet:** Die Kante wird **zweistufig** abgenommen. Das Ziel wird nicht gesenkt; die Wasserlinie ist der Ort, wo der Rest
   hingehört.
   - **Landschritt jetzt:** Netz ≥ 0,40, sichtbar ≥ 0,75. Erreicht sind 0,42 und 0,77.
   - **Wasserlinie:** Der Rest bis 0,50/0,85 kommt aus halb eingetauchten Steinen im 16h-Bettschritt mit neuem Bake.
   - Kein Auffüllen mit Saumsteinen; 960 Kleinsteine wären Rauschen (§3).
5. **Hang – beantwortet:** **Ja, mit Grenzen.** Altstücke, die nach 23.10 noch FEHLER haben, dürfen weichen. Ebenso Bewuchs unter 0,5 m im
   Grundriss plus 0,2 m eines neuen Blocks, mit Sicherung. Nicht weichen dürfen:
   - Bäume;
   - Büsche über 0,5 m;
   - Röhricht;
   - Sehens-Bestand;
   - gesperrte Orte (§4).
6. **Neulauf – beantwortet:** **Sofort**, mit 23.10/23.11:
   - Dreiecks-Hüllen;
   - Bezugsfläche S (23.9), sobald K33 bestanden ist; bis dahin H, mit Vermerk;
   - Wandmodule;
   - Hang-Platz nach §4.

   Vorher müssen die Mängel **M1/M2** behoben sein (§5).
7. **M1 – beantwortet:** Bestand immer in der **Weltlage**, nie auf die r001-Planlage zurücksetzen. Kollision in Bettzellen nach **Grundriss**,
   nicht nach Mitte (§5).

---

## 1. T23-0 Fassung 2

- **K31:** 40/40 Treffer, 0,0 cm Abweichung, Modell „Diagonale (i,j)–(i+1,j+1)“. Damit gilt das Dreiecksgelände aus 23.4 als belegt.
- **Stufe A/B:** 0 Abweichungen. Die erwarteten Unterschiede K3/K4/K9/K16 sind erklärt.
- **K8:** siehe Kurzfazit 2. Bei K1/K2 sieht `NordicBeachRockyGround_02` als dunkle Kleinschutt-Fläche erwartungsgemäß aus.

## 2. Spiegeln (Regel 23.11 `spiegeln`)

**Befund (selbst angesehen):**

| Fall | Bild |
|---|---|
| Stein-Foliage V1/V0, gespiegelt (B/C) | nur ein feiner Bogen, der Stein fehlt praktisch |
| Baum-Foliage V0, gespiegelt (B/C) | Umriss mit leerem Inneren |
| alle Akteure | normal |

**Einordnung [Ableitung aus dem Test]:**

- Ein Akteur mit negativer Skala wird mit umgekehrter Dreiecksreihenfolge gezeichnet, deshalb stimmt das Bild.
- Instanzen einer Foliage-Komponente werden auf dem Nicht-Nanite-Weg ohne diese Umkehr gezeichnet. Man sieht dann Rückseiten.
- Nanite behandelt das je Instanz. Sobald aber der Rückfallweg greift, ist der Fehler wieder da: Nanite aus, eine Plattform ohne Nanite,
  Strahlverfolgung mit dem Ersatznetz (**zu prüfen**, welche Wege das Projekt nutzt).
- Deshalb gilt: **Foliage nie spiegeln.**

**Ersatz gegen Wiederholung (Foliage):**

- Yaw frei;
- Skala innerhalb `skala_wiederholung`;
- Familienrotation (23.2);
- Neigung bis 10°, nur wo die Sitzregeln es erlauben;
- Instanzfarbe über PerInstanceRandom, nur wenn das Material das auswertet (**zu prüfen**).

**Bestand:** Gespiegelte Foliage-Instanzen weltweit zählen. Je Instanz das Skala-Vorzeichen positiv setzen, Yaw + 180°, danach Sitzprüfung.
Die alte Transform kommt ins Protokoll. Das ist ein eigenes Paket mit Pilot in einem Feld.

## 3. Kante zweistufig (Regel 23.11 `kante_zweistufig`)

**Warum nicht senken:** Die Kante 0–1 m ab der Wasserlinie ist genau dort, wo bei Witcher-Bächen halb eingetauchte Steine liegen. An Land
ist dafür kaum Platz: Blöcke ≥ 1 m berühren fast immer Wasser- oder Bettzellen. Der fehlende Teil ist ein Bett-Thema und kein Land-Thema.

| Schritt | Ziel je Seite | Stand |
|---|---|---|
| Landschritt (jetzt) | Netz ≥ 0,40, sichtbar ≥ 0,75 | 0,42 / 0,77 → erfüllt |
| Wasserlinie (16h-Bettschritt, neuer Bake) | Netz ≥ 0,50, sichtbar ≥ 0,85 gesamt | offen |

**Kein Auffüllen mit Saumsteinen:** Netto 0,08 m² je Stück hieße etwa 960 Stück. Das wäre Kleinzeug-Rauschen gegen „Komposition statt
Kleinzeug“ (20/16h N6h). Der Abbruch bei 520 war richtig.

## 4. Platz am Hang (Regel 23.11 `hang_platz`)

| Darf weichen | Darf nicht weichen |
|---|---|
| Altstücke mit Sitz-FEHLER nach 23.10 (Dreiecke, S, Wandmodule) | Altstücke ohne FEHLER |
| Foliage < 0,5 m (Gras, Kraut, kleine Farne) im Grundriss + 0,2 m eines neuen Blocks ≥ 1 m | Bäume, Büsche > 0,5 m, Röhricht, Bestand der Sehens-Planer, gesperrte Orte |

- Jede Entfernung mit Sicherung wie bei v3/T22; die Rücknahme muss möglich bleiben.
- **Grund:** Ein Block, der auf Gras liegt, verdeckt dieses Gras ohnehin. Ein FEHLER-Altstück ist schon ein Bildfehler; es durch einen
  regelkonformen Block zu ersetzen verbessert das Bild doppelt.
- **Erwartung [Annahme]:** Mit 23.10 bleiben mehr Altfelsen (Wandmodule, Dreiecke), und die Hang-Deckung fällt nicht mehr auf 0,04. Zusammen
  mit dem freien Platz sollte Netz ≥ 0,25 erreichbar sein.

## 5. Neulauf und M1/M2

**Vor dem Neulauf beheben:**

- **M1:** Bestandsstücke werden in ihrer Weltlage aus dem Zensus geführt. Ein Zurücksetzen auf die r001-Planlage wäre ein unbemerkter
  Eingriff in reparierte Stücke. Kollision in Bettzellen wird nach Grundriss geprüft (Fußabdruck wie `deckung.vereinigung`), nicht nach Mitte.
- **M2:** Jeder neue Foliage-Typ übernimmt die Material-Overrides seines Quelltyps. Prüfung:
  - Liste „Netz → Overrides“ gegen die Quelle, 0 Abweichungen;
  - ein Bild je neuem Typ;
  - kein weißes `wk2oaeyqx`.

**Neulauf (Plan-Modus):**

- Regeln 23.11, Dreiecks-Hüllen, Zonen auf `T6N1b_2`.
- Bezugsfläche S, sobald K33 bestanden ist; bis dahin H, mit Vermerk.
- Hang-Platz nach §4.
- Abnahme 23d a–e, mit der Kante nach §3.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Steine an der Wasserlinie** (16h-Bettschritt): Das schließt die Kante dort, wo das Auge hinschaut.
2. **Hang-Blöcke ≥ 1 m** statt Gras-Flächen. Die Talkaskade liest sich erst dann als Felstal.
3. **Wiederholung ohne Spiegeln:** Familienrotation und Yaw. Mehr Netzvarianten je Familie (Megascans, kostenlos) bringen mehr als jede
   Transform-Variation.

## Quellen

- `recherche/auftraege/23i-t23-0-spiegeln-planer-ergebnis.md` (Commit 64beaef), Bilder `bilder/platzierung/t23/t23_0_kontrollfaelle.jpg`,
  `t23b_spiegel_boegen_1.jpg`, `t23b_spiegel_boegen_2.jpg` (selbst angesehen)
- `recherche/antworten/23d-t23-1-neuplanung-rueckfragen.md` §1.3/§1.4 (Commit 8dce6ec)
- `recherche/antworten/23b-wiederholung-spiegeln-weisse-steine.md`: Spiegeln 23.2 (Commit 4211d1b)
- `recherche/antworten/23h-dreiecke-stufe-b-rueckfragen.md` (Commit 9fb7c21), `23g-kies-verdraengung-streifen.md` (Commit 7386f14)
- `recherche/antworten/steine_sitz_regeln.json`: jetzt 23.11, Block `nachtrag_23_11`

## Rückfragen

Keine, die den nächsten Schritt ändern.
