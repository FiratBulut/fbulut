# Antwort 22i – Trockengras-Lage bleibt „bewachsen“; fast leerer Ersatz ist richtig; kahl-Liste ja, aber Schnee/Eis ohne Pflanzen-Ersatz; Fels-Regel auch für Schachtelhalm und Lavafels

Gelesen: recherche/auftraege/22i-welle1-ersatz-trockengras-kahl.md @ 61e1eddaaa7f1fd1e0e06ec70d180c81bb9c6429 (Commit a71bbd0)

Stand 20.10.2026. Bezug: 22e (3c99edc) §4, 22f (fdd7f1a) §3.2, 22g (05933d7) §5, `verteilung-lava.md`, `verteilung-wueste.md`,
`verteilung-heide-tundra.md`. Bearbeiter: Cloud-Recherche. Bereich: Regel 22.3b (r008), Ersatz W1-T. Keine Bilder in diesem Auftrag.

## Kurzfazit

1. **Trockengras-Lage – beantwortet: bewachsen, wie in r004/r005.**
   - Das Kahl-Kriterium (22e §4) soll Ersatz nur dort setzen, wo das alte Bett heute **leer** ist. Eine Trockengras-Lage ist nicht leer, sie ist
     der Standort trockener Gräser.
   - Unsere Biom-Planer besetzen genau diese Lage schon mit Grasbüscheln: Wüste und Heide/Tundra mit Faktor ×1,8 bzw. als Profil-Lage, Lava mit
     Faktor 2,0.
   - Ersatz dort würde doppeln und Instanzen kosten, ohne das Bild zu ändern. G5 bleibt bei 7 kahlen Orten, C5 bei 0.
2. **Erweiterte kahl-Liste – beantwortet: ja, mit einer Einschränkung für den Inhalt.**
   - Lavafels, Lavasand, Schnee und Eis sind unbewachsen, also kahl (22f §3.2).
   - **Auf Schnee oder Eis ≥ 0,5 wird aber kein Pflanzen-Ersatz gesetzt** (kein Trockengras, kein Schachtelhalm). Dort wächst nichts sichtbar,
     und ein brauner Büschel auf Schnee wäre derselbe Fehler wie die Scheibe auf der Wiese. Äste bleiben zulässig.
   - Lavasand bleibt voll ersatzfähig.
3. **Fels-Regel – beantwortet: ja, beides.**
   - Schachtelhalm braucht wie Gras einen durchwurzelbaren, feuchten Boden. Auf blankem Fels ist er falsch.
   - Lavafels ist Fels; im Lava-Planer hat er für Gras den Faktor 0,05.
   - Äste bleiben auf Fels und Lavafels zulässig (22f §3.2).
4. **Fast leerer Ersatz – beantwortet: in Ordnung, nichts nachrücken lassen.**
   - Der Ersatz war nie Füllung für jeden entfernten Ort. Er zeigt ein **ausgetrocknetes Bett** dort, wo das Bett noch leer liegt (22 §6.2).
   - Ein Rohrkolben auf Wiese fern vom Wasser war ein Fehlstandort. Die Wiese ohne ihn ist der richtige Zustand; das Landschafts-Gras ist dort
     der Bewuchs.
   - Zusätzliches Gras würde nur Instanzen setzen. Prüfen sollte man stattdessen, ob nach dem Entfernen ein sichtbares Loch bleibt (§4).

---

## 1. Trockengras-Lage

| Gesichtspunkt | Befund |
|---|---|
| Zweck des Kahl-Kriteriums | Ersatz nur, wo das alte Bett leer ist. „Ist er bewachsen, gibt es keinen Ersatz; der Boden trägt dann bereits Bewuchs“ (22e §4) |
| Was die Lage bedeutet | Trockengras ist eine Vegetationslage, kein offener Boden |
| Wer sie heute bedient | Wüste: `grasbueschel` mit Faktor Trockengras ×1,8. Lava: `lagen_faktor` Gras/Trockengras 2,0. Heide/Tundra: Trockengras-Lage steuert das Profil. In G5 (Heide) setzt der Planer dort also schon Büschel |
| Folge bei „kahl“ | G5 72 und C5 27 Orte mit Ersatzgruppen auf einer Fläche, die schon trockene Büschel trägt; Doppelung ohne Bildgewinn |

**Abgrenzung:**

- Wo die Trockengras-Lage unter 0,5 liegt und kahle Lagen (Schlamm, Lehm, Kies, Geröll, Erde, Sand, Lavasand) zusammen ≥ 0,5 erreichen, ist der
  Ort kahl. Die Mischregel aus r005 bleibt unverändert.
- Ob die Trockengras-Lage ein Landschafts-Gras (Grass Type) erzeugt, spielt für die Entscheidung keine Rolle. Hat sie keins, bedient sie der
  Biom-Planer.

## 2. Ersatzfähige Lagen (Regel 22.3c)

Wir trennen jetzt zwei Fragen: Ist der Ort **kahl** (dann darf Ersatz hin), und **welcher Inhalt** passt auf seine Lage?

| Lage am Ort (≥ 0,5) | kahl | Trockengras | Schachtelhalm | Äste |
|---|---|---|---|---|
| Schlamm, Lehm, Kies, Geröll, Erde, Sand (nicht Meer, 22.3) | ja | ja | ja (bei `feucht`, wie bisher) | ja |
| Lavasand | ja | ja | ja (bei `feucht`) | ja |
| Fels, Felsplatte, Sandstein, **Lavafels** | ja | **nein** | **nein** | ja |
| **Schnee, Eis** | ja | **nein** | **nein** | ja |
| Wiese, Gras, Laub, Moos, **Trockengras**, Heide | nein | – | – | – |

- **C7:** Bitte die 9 Teile nach dieser Tabelle neu urteilen. Teile auf Lavasand bleiben. Trockengras und Schachtelhalm auf Lavafels, Schnee oder
  Eis fallen weg; Äste dort bleiben.
- **Erwartung:** Es bleiben 2–9 Teile. Die genaue Zahl entscheidet nichts.
- **Selbsttest r008 → r009:**
  - je 1 Fall Trockengras auf Lavasand (ok), auf Lavafels (gestrichen) und auf Schnee (gestrichen);
  - 1 Fall Ast auf Schnee (ok);
  - 1 Fall Schachtelhalm auf Fels (gestrichen).
- **Unabhängige Nachprüfung:** nur diese Fälle; der Rest bleibt byte-gleich mit r008.

## 3. Fels-Regel erweitert

- **Schachtelhalm auf Fels:**
  - Schachtelhalm wächst auf nassen, mineralischen Böden, auch als Erstbesiedler auf Rohböden. Er braucht Wurzelraum.
  - Auf blankem Fels liest er sich wie gestecktes Gras. Deshalb gilt die Regel wie für Trockengras.
- **Lavafels = Fels:** Der Lava-Planer gibt Lavafels für Gras den Faktor 0,05, praktisch null (`verteilung-lava.md`). Unsere Regeln bleiben damit
  einheitlich.

## 4. Fast leerer Ersatz in Welle 1

- **Warum richtig:** Die meisten Welle-1-Orte sind Rohrkolben fern vom Wasser auf Wiese (F4: Wiese 28, Laub 6, Gras 1). Sie waren nie in einem
  Bett. Nach dem Entfernen ist dort Wiese, und das ist der Sollzustand.
- **Nicht nachrücken lassen:**
  - Gras-Instanzen statt Rohrkolben würden die Wiese nicht verbessern, denn das Landschafts-Gras deckt sie schon.
  - Sie würden aber Instanzen, Zensus und Prüfaufwand kosten.
- **Ein Prüfpunkt im Pilot F4:**
  - 10 zufällige entfernte Rohrkolben-Orte auf Wiese, Bild vorher und nachher, gleiche Sonne, von schräg oben.
  - Abnahme: kein sichtbares Loch und keine kahle Scheibe im Gras. Das Landschafts-Gras darf nicht durch eine Foliage-Ausschlussregel
    oder eine gemalte Lage unter dem Rohrkolben fehlen.
  - Zeigen ≥ 2 von 10 ein Loch, ist das eine Lagenfrage, kein Ersatzthema. Dann am Ort die Lage prüfen und erst danach entscheiden.

## 5. Nächste Handlung

Der Plan bleibt wie im Auftrag:

1. Weltreparatur „schwebend“;
2. T22 auf frischen Ständen neu rechnen;
3. W1-T mit **r009** (Tabelle §2) planen und nachprüfen lassen;
4. Einbau Welle 1, mit Pilot F4 zuerst und dem Lochtest aus §4.

**Erfolg:** W1-T mit gezählten Teilen je Feld und Lage, 0 Pflanzen-Ersatz auf Fels, Lavafels, Schnee oder Eis, 0 Ersatz auf Trockengras-Lage,
Lochtest F4 bestanden.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Keine Wasserpflanzen fern vom Wasser:** Welle 1 entfernt 2 087 Fehlstandorte. Das ist der eigentliche Bildgewinn, der Ersatz ist
   Nebensache.
2. **Wiesen ohne Löcher:** Nach dem Entfernen darf keine kahle Stelle bleiben (Lochtest F4).
3. **Trockenbetten nur dort betonen, wo sie leer sind:** Weniger, aber passend gesetzter Ersatz liest sich glaubwürdiger als Streu über
   jede Lage.

## Quellen

- `recherche/auftraege/22i-welle1-ersatz-trockengras-kahl.md` (Commit a71bbd0)
- `recherche/antworten/22e-pilot-f6-ergebnis.md` §4 (Kahl-Bedingung, Commit 3c99edc)
- `recherche/antworten/22f-t22-f6-2-r004-lily-rueckfragen.md` §3.2 (Geröll kahl, kein Trockengras auf Fels, Commit fdd7f1a)
- `recherche/antworten/22-wasserpflanzen-fern-vom-wasser.md` §6.2 (Zweck des Trockenbett-Ersatzes)
- `recherche/antworten/verteilung-lava.md` (`lagen_faktor` Lavafels 0,05, Lavasand 0,4, Gras/Trockengras 2,0)
- `recherche/antworten/verteilung-wueste.md` (`grasbueschel`, Lage Trockengras ×1,8)
- `recherche/antworten/verteilung-heide-tundra.md` (Trockengras-Lage steuert das Profil; G5 = Heide)

## Rückfragen

Keine, die den nächsten Schritt ändern.
