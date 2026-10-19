# Antwort 22f-2 – ToadRush ist eine Zwergbinse wechselfeuchter Schlammböden: braun auf Riss-Schlamm ist richtig; eigene Regel statt Lehm-Prüfung

Gelesen: recherche/auftraege/22f-2-toadrush-test-ergebnis.md @ 3e2bd6ca97a2bc0eb5b60227c91db7788b7e94b9 (Commit e694b43)

Stand 19.10.2026. Bezug: Antwort 22f (fdd7f1a) §2, §3.6; 22 §3 (Binsen-Regel); 22e (3c99edc). Bearbeiter: Cloud-Recherche.
Bereich: Wasserpflanzen-Regel 22.x, Klasse `SM_ToadRush_*`, Pilot F6.

## Kurzfazit

1. **Unser Fehler in 22f §2:** Wir hatten den braunen Büschel im Kreis als r003-Trockengras gedeutet und daraus U-a/U-b abgeleitet. Euer Lookup
   zeigt, dass es die behaltene ToadRush ist. Unsere Bilddeutung war falsch; Kriterium 5 „behalten“ ist erfüllt.
2. **Soll ToadRush grün wirken? Nein, braun ist richtig.**
   - *Juncus bufonius* (Krötenbinse) ist eine **einjährige** Zwergbinse.
   - Sie wächst auf offenem, feuchtem Boden, an Teichrändern, in zeitweise überfluteten Senken und Fahrspuren. Ihre Gesellschaften erscheinen
     gerade in der **Austrocknungsphase** temporärer Tümpel.
   - Die Pflanze ist hellgrün oder an offenen Standorten rötlich, die Kapseln sind braun.
   - Ein kleiner brauner Büschel auf trockenem Riss-Schlamm ist damit das richtige Bild und kein Materialfehler. Die Quellen stehen unten.
3. **Folge für die Regel:** ToadRush ist kein Zeiger für Dauerwasser wie Rohrkolben, sondern für **wechselfeuchten, offenen Schlamm**. Neu
   ist eine eigene Klasse in 22.3 (§1):
   - Auf Lehm oder Schlamm ≥ 0,5 bei Hang ≤ 8° steht sie richtig, auch im Trockenbett.
   - Auf Wiese fern vom Wasser bleibt sie ein Verstoß.
4. **T22-L0 eingrenzen:** Lehm-Gewicht 0 prüfen wir **nur für Rohrkolben**. Für ToadRush zählt Lehm als richtiger Standort (§2).
5. **F6:** Im Piloten wurden ToadRush aus Trockenbetten entfernt (z. B. sp_14, 17, 19, 20). Wer auf Lehm oder Schlamm stand, wird aus der
   Sicherung zurückgeholt; Ersatz an denselben Orten entfällt. Das fließt in r005 ein. Zuerst wird lesend gezählt (§3).

---

## 1. Regel 22.3: Klasse `zwergbinse` (`SM_ToadRush_*`)

| Lage | Urteil |
|---|---|
| Lehm + Schlamm ≥ 0,5 **und** Hang ≤ 8° (temporärer Tümpel, Trockenbett, Senke) | ok (Standort) |
| Uferband nach 22 §3 (bis 15 m und 1,5 m über dem Spiegel) | ok wie bisher |
| im Wasser, Tiefe > 0,10 m | Verstoß „zu_tief“ (Zwergbinse, kein Röhricht) |
| Wiese oder Gras-Lagen ≥ 0,45 fern vom Wasser (> 15 m), keine Mulde | Verstoß wie bisher |

- **Grund:** Zwergbinsen-Gesellschaften brauchen offenen, konkurrenzarmen Boden, der zeitweise nass ist. Dichte Wiese ist nicht ihr
  Standort; ein trocken gefallener Schlammboden schon.
- Die Schwellen sind Gestaltungswerte für das Bild, keine botanischen Messwerte. 0,45 Gras entspricht der F6-Kalibrierung aus r004.
- Rohrkolben bleiben bei der Regel aus 22/22.2: nur nasse Senke oder Uferband, nicht auf Riss-Schlamm.

## 2. T22-L0 anpassen (läuft gerade)

- Den Lauf nicht abbrechen. In der Auswertung ToadRush getrennt ausweisen.
- **Entscheidung über Lehm-Gewicht 0 nur an Rohrkolben:** Stehen ≥ 8 der 10 angesehenen Rohrkolben-Fälle auf trockenem Riss-Schlamm, gilt
  Lehm 0 für Rohrkolben.
- ToadRush-Fälle auf Lehm, die unter Lehm 0 zu Verstößen würden, sind nach §1 **ok** und werden nicht entfernt.

## 3. F6: ToadRush aus der Sicherung zurück (lesend zuerst)

1. **Zählen:** Welche ToadRush aus der F6-Sicherung (1 222 Einträge) standen auf Lehm + Schlamm ≥ 0,5 und Hang ≤ 8°? Gesucht sind Zahl
   und Orte.
2. **r005:** Für diese Orte wird der Ersatz gestrichen, wenn er ≤ 0,5 m entfernt liegt. Der Ersatz stand ja am Ort der ersten entfernten
   Instanz. Danach werden die ToadRush aus der Sicherung transformgleich zurückgeholt; der Weg ist durch die 1-%-Rücknahme belegt.
3. **Abnahme:**
   - zurückgeholt = Liste;
   - nach Neustart transformgleich;
   - T22 mit Regel 22.3 in F6 weiter 0 Verstöße;
   - 3 Bilder an zurückgeholten Orten zeigen braune Büschel auf Riss-Schlamm, keine Doppelung mit Ersatz.

**Abbruch:** Liegen mehr als 20 % der zurückgeholten Orte auf Wiese (Gras ≥ 0,45), stimmt die Lagen-Abfrage nicht. Dann nichts zurückholen
und melden.

## 4. Nächste Handlung

Unverändert **T22-F6-2 abschließen** (22f §4). Neu kommen hinzu: der Zählschritt §3.1 vor r005, die ToadRush-Rückholung in r005 und die
Auswertung von T22-L0 nur für Rohrkolben.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Leben auf trockenem Schlamm:** Zwergbinsen-Polster und einzelne Pionierpflanzen auf Riss-Schlamm erzählen „hier stand im Frühjahr
   Wasser“. Das ist glaubwürdiger als nackter Schlamm mit Trockengras-Matten.
2. **Farbabstufung nach Feuchte:** braune und rötliche Zwergbinsen auf trockenem Schlamm, grüne Binsen und Rohrkolben erst an der echten
   Nasslinie.
3. **Ufergehölz am neuen Bach E6_K2** (22f).

## Quellen

- EUNIS (EEA), Habitat 3098 „Dwarf toad-rush communities“: <https://eunis.eea.europa.eu/habitats/3098>. Laut Suchauszug Gesellschaften
  temporärer Tümpel, überfluteter Fahrspuren und zeitweise überschwemmter Böden.
- EUNIS (EEA), Habitat 3099 „Toad-rush swards“: <https://eunis.eea.europa.eu/habitats/3099>. Laut Suchauszug erscheinen sie in der
  Austrocknungsphase temporärer Tümpel.
- NatureSpot, Toad Rush – *Juncus bufonius*: <https://www.naturespot.org/node/806>. Laut Suchauszug einjährig, auf nacktem feuchtem Boden
  und an Teichrändern, Kapsel braun.
- NIWA Factsheet *Juncus bufonius*: <https://niwa.co.nz/sites/default/files/juncus_bufonius_factsheet.pdf>. Laut Suchauszug hellgrün oder
  an offenen Standorten rötlich.
- USGS PlantID *Juncus bufonius*: <https://warcapps.usgs.gov/PlantID/Species/Details/706>. Laut Suchauszug nasse Straßenränder, Gräben und
  Sumpfränder.
- Die Seiten wurden nicht einzeln geöffnet; die Angaben stammen aus den Suchauszügen.
- Projekt: `recherche/antworten/22f-t22-f6-2-r004-lily-rueckfragen.md` §2, §3.6 (Commit fdd7f1a); `22-wasserpflanzen-fern-vom-wasser.md` §3
  (Commit 41e3ca5).

## Rückfragen

Keine.
