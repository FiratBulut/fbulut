# Antwort 16h-6t – Die Platte ist der alte Fluss selbst, nicht ein Darstellungsfehler; kein Subsystem-Umweg, gleich Rollout-Pilot 1; vorher ein kurzer Höhenvergleich, der das Entfernen absichert; 4096 nicht als Pauschalregel

Gelesen: recherche/auftraege/16h-nachtrag6t-wasserplatte-ursache-alter-c3-fluss.md @ e227c0fd0f79fe0a384ec11b517a4248980486c2 (Commit 8cf1a80)

Stand 19.10.2026. Bezug: 16h-6s (0bcecb5), 16h-6r (e8fa4d7). Bearbeiter: Cloud-Recherche. Bilder `bilder/swr_p2/muendung_t9_t10_zsp.jpg` und
`pie_muendung_wasserplatte.png` selbst angesehen.

## Kurzfazit

1. **Korrektur 6s (unser Fehler):** Unsere Hypothese H1 war falsch. Wir hatten einen veralteten Boden-Bezug der SWR angenommen und die Stufen
   dem 1-m-Raster der Simulation zugeschrieben. T1–T6 sind sauber negativ, T9 zeigt den wahren Verursacher: Die Platte gehört zum alten Epic-Fluss
   `C3_Fluss_F_ERLENBACH_2`. Die Stufen kommen aus der Wasser-Info der Zone C3 (1,18 m je Pixel). Die negativen Tests bleiben als belegter
   Ausschluss stehen.
2. **Frage 1 – beantwortet, ein Punkt wartet auf Beleg:**
   - Ein Epic-Fluss zeichnet eine **flache Wasserfläche über die ganze Splinebreite**. Wo das Gelände tiefer liegt als diese Fläche, sieht man
     Wasser über trockenem Boden. Am Splinerand endet die Fläche dann in der Luft, mit senkrechter Kante. Das ist kein Startfehler, sondern
     Geometrie: Der Kopf wurde am 13.10. auf bis zu 22 m verbreitert, und das Bett liegt heute 0,3–0,6 m tiefer als der Spiegel.
   - **Im Spiel: ja.** Das PIE-Bild zeigt die Platte.
   - **Warum `rebuild_native_body` oder eine Landschaftsänderung den Rand glättet, ein Zonen-Neuaufbau aber nicht – zwei Erklärungen, offen:**
     - **H-A:** Der alte Fluss gräbt per Wasser-Pinsel in die Landschaft. Erst eine Neuberechnung der Landschaftsebenen formt das Ufer an den
       verbreiterten Kopf an, und das nur im Speicher.
     - **H-B:** Die eigenen Darstellungsnetze des Flusses sind gespeichert veraltet. Nur der Neuaufbau des Flusses erneuert sie, das bloße
       Neuzeichnen der Wasser-Info nicht.
   - **Einstellung:** Keine gefunden, die das behebt. Für Geometrie gibt es keine.
3. **Frage 2 – beantwortet: kein Subsystem, gleich Rollout-Pilot 1.**
   - Ein Neuaufbau beim Start hilft im Spiel nicht, falls H-A gilt: Landschaftspinsel sind ein Editorwerkzeug.
   - In beiden Fällen würde er die zu breite, zu hohe Fläche nicht beseitigen, und mit Pilot 1 wäre er toter Code.
   - Vor dem Entfernen des alten Flusses kommt ein Höhenvergleich (T11, §5). Gilt H-A, kann das Entfernen das Gelände unter dem gebackenen
     p2-Bett verändern.
4. **Frage 3 – wartet auf Beleg, wahrscheinlich Fernfläche:**
   - 40 km passt zur Fernfläche der Wasserzone (`FarDistanceMeshExtent`, Fernnetz bis zum Horizont).
   - Für Binnenzonen ohne Meer ist sie unnötig. Kosten: Die Zone wird nie weggeschnitten, möglicherweise zeichnet sie eine flache Fernfläche,
     und sie kann die World-Partition-Zuordnung verschieben.
   - Prüfung je Zone, wenige Minuten (§3).
5. **Frage 4 – beantwortet als Abschätzung, Messung offen:**
   - Grob gerechnet sind es **etwa 128 MiB je Zone bei 4096** (gegenüber 8 MiB bei 1024). Annahme: 4 Kanäle Half-Float; das Format ist in 5.8
     **zu prüfen**.
   - 20–30 Zonen wären dann 2,5–3,75 GiB, falls alle gleichzeitig geladen sind. Das ist nicht tragbar.
   - Die Regel „Breite < 6 m → 4096“ **nicht** übernehmen. Die Auflösung braucht nur, wer in der Zone noch Epic-Wasserkörper mit sichtbarem
     Rand hat. Ob die SWR die Zonen-Auflösung überhaupt nutzt, zeigt ein Test in Pilot 1 (§4).

---

## 1. Was die Bilder zeigen (selbst angesehen)

| Bild | Befund |
|---|---|
| Zeile 1 (vor T9) | Breite Wasserfläche über dem Kies, rechts treppige, glasige Wände, Stufen etwa 1 m |
| Zeile 2 (T9, alter Fluss ausgeblendet) | Kein Wasser an der Kamera. Darunter dunkles, steiniges Bett und die roten Felsen frei. Das gesamte Wasser im Bild stammt vom alten Fluss |
| Zeile 3 (T10, 4096 + Neuaufbau) | Fläche etwa gleich groß, der **Rand trifft das Gelände** ohne Wand. Glatt, aber die Wasserfläche reicht weiter über das Bett als das heutige Gerinne |
| Zeile 4 (4096 gespeichert, nach Neustart) | Kleinere Stufen, aber wieder eine senkrechte Wand. Links etwas breiter als in Zeile 3 |
| PIE-Bild | Figur am Ufer. Davor steht eine glasklare Wasserplatte mit senkrechtem, durchsichtigem Rand über trockenem Kies, deutlich über Bodenhöhe. Hinten ist die Fläche bis an die roten Felsen gefüllt |

**Folgerung:**

- Im Spiel ist der Zustand aus Zeile 4 zu sehen, nicht der aus Zeile 3.
- Der Unterschied zwischen 3 und 4 liegt am Rand: Wand oder Anschluss ans Gelände. Die Ausdehnung ist in beiden Zuständen zu groß für das
  heutige Bett.
- Deshalb ist auch der glatte Zustand kein Ziel. Der alte Kopf passt nicht mehr zur p2-Mündung.

## 2. Frage 1: Mechanismus

**Was sicher ist:**

- Epic-Flüsse werden über die Wasser-Info der Zone gezeichnet. Die Wasserhöhe kommt aus dem Spline, und gezeichnet wird über die Splinebreite.
- Am Rand werden die Gitterpunkte außerhalb des Wassers abgesenkt. Liegt dort die Wasserfläche über dem Gelände, entsteht eine Wand entlang des
  Texelrasters. Daher kommen Stufen von 1,18 m bei 1024 und etwa 0,3 m bei 4096.
- Epic löst das gewöhnlich, indem der Fluss sein Bett per Landschaftspinsel in das Gelände gräbt. Das Ufer steigt dann über den Wasserspiegel, und
  der Rand liegt unter der Erde. Laut Epic-Doku wirkt der Pinsel nur bei aktivierten Landschafts-Bearbeitungsebenen (Quelle unten).

**Warum der Neuaufbau heilt und ForceUpdateWaterInfo nicht – zwei Erklärungen:**

| | H-A: Wasser-Pinsel | H-B: veraltete Flussnetze |
|---|---|---|
| Ablauf | Eine Landschaftsänderung oder ein geänderter Fluss löst die Neuberechnung der Bearbeitungsebenen aus. Der Pinsel formt das Ufer an den Kopf vom 13.10. an, nur im Speicher. Gespeichert ist ein älterer Stand | Der Neuaufbau erzeugt die Netze, mit denen der Fluss in die Wasser-Info zeichnet. Gespeichert sind veraltete; ForceUpdateWaterInfo zeichnet nur die vorhandenen neu |
| Voraussetzung | `affects_landscape` am alten Fluss an, ein Pinselverwalter in der Karte. Für den Eintrag `WBR_F_ERLENBACH` im Exportdatensatz steht `false`; für `C3_Fluss_F_ERLENBACH_2` liegt uns kein Wert vor | keine |
| Im Spiel | Pinsel laufen dort nicht, also bleibt die Platte | Bleibt, bis der Fluss neu gespeichert wird |
| Folge für Pilot 1 | Entfernen ändert das Gelände um den alten Fluss, auch unter dem p2-Bett | Entfernen ist geländeneutral |

- Beide Erklärungen beantworten die Frage nach dem Spiel gleich: Im Spiel ist die Platte zu sehen, und der PIE-Befund bestätigt das.
- Sie unterscheiden sich nur darin, wie gefahrlos der alte Fluss entfernt werden kann. Darauf zielt T11 (§5).
- **Einstellung:**
  - Ein Laden der Wasser-Info erst nach dem Streaming würde hier nichts ändern, denn die Platte ist keine Ladefrage. T6 hat das
    Streaming bereits ausgeschlossen.
  - Für `rebuild_native_body` ist die interne Wirkung **zu prüfen** (Projektfunktion, kein Engine-Name).

**Wichtiger Nebenbefund, falls H-A gilt:**

- Jede Landschaftsänderung in C3/D3, die gespeichert wird, schreibt das Graben des alten Flusses mit ins Gelände. Das gilt auch für reine
  Lagenänderungen, wenn sie die Neuberechnung auslösen.
- Das betrifft auch die Bodenlagen-Arbeit aus 22h §3, falls sie in C3/D3 liegt.
- Dann ist das gebackene p2-Bett nicht mehr auf dem Gelände, auf dem es gebacken wurde. Bis T11 also **keine Landschaft in C3/D3 speichern.**

## 3. Frage 3: 40-km-Grenzen

- **Wahrscheinliche Ursache:**
  - Die Fernfläche der Wasserzone (`FarDistanceMeshExtent` an `UWaterMeshComponent` bzw. Zonen-Vorgabe). Sie verlängert das Wassernetz bis zum
    Horizont, gedacht für Meere (16h-HLOD-Antwort, API unten).
  - Die Zonen C2/C3/D2/D3 haben vermutlich keine Fernfläche (604 m = halbe Zonenbreite, passend zu 1024 × 1,18 m).
- **Kosten, alle zu prüfen:**
  1. Die Komponente wird nie per Sichtkegel oder Entfernung verworfen. Das kostet vor allem CPU für den Quadtree, wenig GPU.
  2. Ist ein Fernmaterial gesetzt, zeichnet jede dieser Zonen eine flache Fläche auf ihrer Wasserhöhe bis 40 km. Bei Binnenzonen kann sie in
     Senken sichtbar werden und sich mit anderen Zonen überlagern.
  3. World Partition ordnet Akteure nach ihren Grenzen ein. Eine 40-km-Zone kann in einer großen Zelle oder dauerhaft geladen landen. Dann
     bleiben ihre Texturen ständig im Speicher (wichtig für §4).
- **Prüfung je gemeldeter Zone:**
  - Fernmaterial gesetzt ja/nein, Ausdehnung, Laufzeitzelle bzw. Datenlayer;
  - ein Bild von oben über einer Senke.
- **Empfehlung:** Bei Binnenzonen ohne Meer die Fernfläche aus (Ausdehnung 0 bzw. kein Fernmaterial, Feldname in 5.8 **zu prüfen**). Nur die
  Zone, die den Meereshorizont trägt, behält sie. Danach muss die Zonengrenze ≈ halbe Zonenbreite sein.

## 4. Frage 4: Auflösung und Speicher

**Speicher der Wasser-Info**, ohne Mip-Stufen:

| Auflösung | 4 × Half-Float (8 B) | 4 × Float (16 B) | Texel bei 1 208 m Zone |
|---|---:|---:|---:|
| 1024 | 8 MiB | 16 MiB | 1,18 m |
| 2048 | 32 MiB | 64 MiB | 0,59 m |
| 4096 | 128 MiB | 256 MiB | 0,29 m |

- Dazu kommen beim Neuzeichnen kurzzeitig Arbeitstexturen.
- Ob 5.8 mehrere Zonen in einem gemeinsamen Texturfeld gleicher Größe hält, ist **zu prüfen**. Dann würde eine 4096-Zone alle Zonen auf 4096
  heben.
- **Messung:** RHI- bzw. Render-Target-Speicher (`stat RHI`, `memreport -full`) vor und nach dem Umstellen von C3 von 4096 auf 1024 im
  Speicher, Differenz in MiB.

**Regel statt „Breite < 6 m → 4096“:**

1. Die Auflösung richtet sich nur nach **Epic-Wasserkörpern mit sichtbarem Rand** in der Zone. Ziel: Texel ≤ 1/10 der schmalsten solchen
   Breite.
   - Für Seen und breite Flüsse ≥ 6 m reicht 2048.
   - 4096 nur, wo ein schmaler Epic-Fluss dauerhaft bleibt.
2. Nach dem Rollout sind die Bäche SWR. Ob die SWR-Darstellung die Wasser-Info der Zone nutzt, belegt **Z1** in Pilot 1:
   - Nach dem Entfernen des alten Flusses C3 im Speicher auf 1024 stellen und das Bildpaar an der Mündung vergleichen.
   - Bei gleichem Bild C3/D3 zurück auf 1024 (spart etwa 2 × 120 MiB bei Half-Float).
   - Sonst gilt Regel 1 für SWR-Breiten.
3. Ein Rand, der in der Luft endet, ist mit keiner Auflösung zu verstecken; 4096 macht die Stufen nur kleiner (Zeile 4). Die Abhilfe ist ein
   Wasserkörper, dessen Rand im Gelände endet.

## 5. Nächste Handlung: T11, dann Pilot 1

**T11 – Höhenvergleich, nur Speicher, einige Minuten:**

1. Am alten Fluss (C3 und D3) `affects_landscape` lesen; Pinselverwalter (`WaterBrushManager`) in der Karte zählen.
2. Geländehöhe an 30 festen Punkten lesen:
   - 10 am Plattenrand links und rechts;
   - 10 im p2-Bett ≤ 30 m vor der Mündung;
   - 10 Kontrollpunkte 50 m abseits.

   Gelesen wird über eine Landschaftsabfrage oder einen Strahl nur gegen die Landschaft (Funktionsname **zu prüfen**).
3. `rebuild_native_body` am alten Fluss, warten, bis Landschaft und Wasser fertig sind, dann dieselben 30 Höhen erneut lesen.
4. Ohne Speichern PIE an der Mündung starten, Bild wie im Nachtrag.

**Bewertung:**

| Ergebnis | Mechanismus | Folge |
|---|---|---|
| Höhen am Rand oder im p2-Bett ändern sich um ≥ 1 cm | H-A | In Pilot 1 den alten Fluss erst entfernen, wenn ein Höhenabzug vorher/nachher im p2-Bake-Bereich bitgleich ist. Sonst muss der p2-Bake neu, also Teil von Pilot 1 werden. Bis dahin keine Landschaft in C3/D3 speichern |
| Höhen gleich, PIE nach Neuaufbau ohne Platte | H-B | Entfernen ist geländeneutral. Bis zum Pilot genügt optional ein einmaliger Neuaufbau mit Speichern des Flusspakets, ohne Subsystem |
| Höhen gleich, PIE weiter mit Platte | Geometrie, Neuaufbau heilt nur die Editoransicht | Pilot 1 ohne Sonderschritt |

**Erfolg:** ein Wert für `affects_landscape`, eine 30-Punkte-Tabelle vorher/nachher, ein PIE-Bild. Damit ist entschieden, ob Pilot 1 eine
Geländesicherung braucht. Danach Pilot 1 mit Z1 (§4).

**Abbruch:** Ändert schon das Lesen etwas am Gelände (Speicherstatus nicht mehr 0), abbrechen und Neustart ohne Speichern.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Ein Bach von der Quelle bis zur Mündung** ohne Wasserplatte. Ein Wasserrand, der in der Luft endet, ist der gröbste Bildfehler im Tal.
   Rollout-Pilot 1 behebt ihn an der Wurzel.
2. **Ein Gelände, das zum Bake passt:** Kein verborgenes Graben alter Flüsse darf das gebackene Bett nachträglich verschieben (T11).
3. **Speicher für Vegetation statt Wasser-Info:** 1024 bzw. 2048, wo es reicht. Die gesparten Hunderte MiB sind im offenen Tal besser in
   Ufervegetation und Steinen angelegt.

## Quellen

- `recherche/auftraege/16h-nachtrag6t-wasserplatte-ursache-alter-c3-fluss.md` (Commit 8cf1a80), Bilder `bilder/swr_p2/muendung_t9_t10_zsp.jpg`,
  `pie_muendung_wasserplatte.png` (selbst angesehen)
- `recherche/antworten/16h-nachtrag6s-saegezahn-nach-neustart.md` (Commit 0bcecb5), H1 hiermit verworfen
- `recherche/antworten/fluss_sim/gewaesser/F_ERLENBACH/fluss_sim.json`: `WBR_F_ERLENBACH`, `affects_landscape: false`
- `recherche/vorlagen/daten/sehens/wasser_welt.json`: `F_ERLENBACH_2_C2`/`_C3`, Spline-Punkte
- `recherche/antworten/hlod-fernansicht-world-partition.md`: Fernfläche der Wasserzone
- Epic: [Water Body Actors](https://dev.epicgames.com/documentation/unreal-engine/water-body-actors-in-unreal-engine). Wasserkörper graben über
  einen Landscape Brush, nur bei aktivierten Edit Layers.
- Epic: [Landscape Blueprint Brushes](https://dev.epicgames.com/documentation/unreal-engine/landscape-blueprint-brushes-in-unreal-engine)
- Epic API: [UWaterMeshComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/Water/UWaterMeshComponent) (`FarDistanceMeshExtent`),
  [FWaterZoneActorDefaults](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/WaterEditor/FWaterZoneActorDefaults)
  (`FarDistanceMeshExtent`, `RenderTargetResolution`), [WaterZone Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WaterZone)
- Epic Issue [UE-296375](https://issues.unrealengine.com/issue/UE-296375): fehlerhaft gezeichnete WaterInfoTexture führt zu Wasser in Blöcken
  oder an falscher Stelle
- Speicherwerte: eigene Rechnung. Texturformat und gemeinsames Texturfeld in 5.8 nicht belegt, deshalb als Messung in §4.
- Forum [Water Landscape](https://forums.unrealengine.com/t/water-landscape/669122): Das Wassersystem schreibt in die ursprüngliche
  Landschaftsebene.

## Rückfragen

Keine, die den nächsten Schritt ändern. Liegt die Bodenlagen-Arbeit aus 22h §3 in C3/D3 und wurde dort seit dem 13.10. Landschaft gespeichert,
bitte T11 um einen Vergleich gegen die p2-Bake-Höhen ergänzen.
