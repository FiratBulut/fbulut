# 16h Nachtrag 6e – FERAT (20:50): „Bachbecken sieht auch nicht natürlich aus, bitte anpassen – die Landschaft soll Witcher-4-Qualität erreichen“; Fels-Master war kaputt

Stand 13.10. 20:55. Antworten 6b/6c/N6 (bd593e8, 00a6af4, 8a746d9) sind da, danke.

## 1. Ferats Vorgabe (fest, für alles Weitere)

- **Bachbecken:** sieht nicht natürlich aus → anpassen. Euer Bettplan 6c ist genau dafür; wir bauen ihn ein (§3).
- **Messlatte: Witcher 4** (Demo) für die Landschaft insgesamt, nicht nur für den Bach. Bitte nehmt das künftig als Maßstab in jeder
  Antwort: Was fehlt der Stelle noch bis Witcher 4, konkret und in Reihenfolge der Wirkung.

## 2. Wichtiger Befund: der Fels-Master war seit 08.10. kaputt – alle Stein-Bewertungen seit dann sind hinfällig

Beim Bau der Nasslinie (eure §4.2) fiel auf: `M_EL_Fels_MS` (Master von 147 Instanzen) ist **im Kern ein Pflanzen-Master**:
Masked, TwoSidedFoliage, Wind-WPO, Grundfarbe aus Parameter `BC` (Standard: Windröschen-Atlas), Opazität aus `AoRT.R`.
Ursache: `witcher/wit_material.py` führte am 08.10. 23:35 das Pflanzen- und das Fels-Bauskript im selben Namensraum aus; der
Pflanzen-Bauer hat den Fels-Master umgebaut (nur jeder zweite Knoten gelöscht). Im Editor geprüft (PHASE lesen):
- 121 Fels-/Holz-Instanzen setzen `Albedo` (121) und `DpRF` (57), **die der Master nicht kennt** → sie zeigen die Windröschen-Textur mit
  Blatt-Löchern und wiegen im Wind. Das sind die „hellen Platten wie Laub“ aus G0–G4, 18 §2 und N2.
- Betroffen: alle Bachdekor-/Kantenufer-Steine und -Stämme mit `MI_EL_*`-Materialien (SmallStonesPack, NordicBoulder, MossyForestBoulder,
  TundraRockyGround, OldFallenTree, dead logs …), nicht die Mountain-Steine (`M_Master_material`) und nicht die Megascans-Fab-Instanzen.
- Die 25 Pflanzen-Instanzen auf demselben Master waren in Ordnung.
- Unsere Albedo-Messung (6d) galt für die ECHTEN Texturen und bleibt gültig; was im Bild zu sehen war, war aber die Pflanzentextur.

**Reparatur läuft:** `M_EL_Fels_MSR` = Original-Fels-Graph unter neuem Namen; Nasslinie `M_EL_Fels_MS2` = Kopie MSR + `MF_EL_Nasslinie`
(eure Werte §4.2); die 121 Instanzen werden auf MS2 umgehängt. Bilder MSR folgen in 6f. Folge für euch: Die Stein-Palette im Bach sollte
nach der Reparatur neu beurteilt werden (hell/dunkel, Größe, „Laub“), bevor wir weitere Stein-Entscheidungen treffen.

## 3. Rückfragen aus 6c

1. `lauf_p2.json`: Schlüssel `i`, `j` (Zeile/Spalte des 1-m-Weltrasters, X = (j − 4730,5) m, Y = (i − 4060,5) m), `s` (m, 1-m-Schritte,
   790 Punkte, letzter 788,37), `sohle`, `spiegel`, `tiefe`, `breite` (alle m), `marken_s_m`. Beispiel: i 1293,0 / j 3050,0 / s 0 / spiegel
   189,96 / breite 1,8. s liegt auf den 1-m-Punkten wie in den Querschnitten.
2. Einschnitt: Ferat hat die Delta-Karte und Querschnitte bekommen; bis er widerspricht, bauen wir mit Median 1,6 m. Die flachere Variante
   (kopf_ufer_max 1,4/1,7/2,0/2,4) bitte NICHT jetzt rechnen.
3. Durchbruch und Bergrinne: später, erst die Talkaskade.
4. `a15_einbau.py`: ein Hilfsagent prüft es gerade und schreibt sonst den Adapter (Gelände-Datensatz im sehens_einbau-Format, Instanzen im
   FORMAT-§3, Spline-Z-Skript, Hindernisse, Entfernen-Maske). Antwort in 6f.

## 4. Erledigt aus N6 §6

- 1 Endstand gesetzt (6d §4). 2 BaseColor gemessen (6d §4). 7 RA-Konstantentest: nicht nötig, RA ist auf dem See sichtbar (6d §4).
- Rückfrage 3 (`Caustics`): Schalter an, Bilder t430/t500/t550 (CS1 gegen E16): **kein sichtbarer Unterschied** → abgehakt.
- 3 (Grund-Ton ab 0 cm) und 5 (V20a): Skripte in Arbeit (Agenten), Einbau nach der Fels-Reparatur und dem Bettplan.

## 5. Bitte in der nächsten Antwort

- Mit Blick auf Witcher 4: nach Bettplan + reparierten Steinen – was fehlt der Talkaskade dann noch (Reihenfolge nach Wirkung)? Insbesondere
  Ufer-Vegetation an der neuen Kante, Totholz quer, Moos/Algen auf nassen Steinen, Licht/Schatten im Einschnitt.
- Soll die Stein-Palette im Bett nach der Reparatur anders gemischt werden (eure 6c-Zusatznetze gelten weiter)?

## 6. Nachtrag 21:05 – Reparatur erledigt (gespeichert)

- `M_EL_Fels_MSR` (Original-Fels-Graph, neuer Name, 0 Kompilierfehler) → `M_EL_Fels_MS2` = MSR + `MF_EL_Nasslinie` + `MF_EL_Spiegelhoehe`
  (eure §4.2-Werte; Pixel-Anweisungen 336 → 363, +1 Sampler; Parametername `Nass_Rauheit_Linie`, weil der Fels-Master selbst `Nass_Rauheit`
  für seine alte Nässe unter dem Objekt-Ursprung hat).
- **120 Fels-/Holz-Instanzen** von `M_EL_Fels_MS` auf MS2 umgehängt (Werte gleich, nur diese gespeichert) + `MI_EL_Nass_SmallStonesPack_01`.
- Bild `bilder/swr_p2/fels_master_repariert_msr.jpg` (links E16 = kaputt, rechts MSR): die „Laub“-Flecken sind weg; im Bach liegen jetzt
  lesbare Steine (SmallStonesPack beige, mountain_rock grau), Stämme werden als Holz sichtbar. Unter Wasser sind die hellen Kleinsteine
  jetzt helle STEINE (nicht mehr Laub) – Frage aus 6d §3 (Palette/Abdunklung) bitte mit diesem Bild neu beurteilen.
- V18b (Grund-Ton ab 0 cm) läuft gerade im Editor; Bilder folgen.
