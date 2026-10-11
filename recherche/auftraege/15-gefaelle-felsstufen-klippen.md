# Auftrag 15: Steile Fluss- und Bachstrecken natürlich machen – Felsstufen, Klippen, Wasserfälle (11.10.2026, 16:30)

## Ferats Beobachtung

„Bei Flüssen und Bächen ist die Steigung zu viel. Sobald es eine gewisse Steigung hat, soll es Klippen geben, sonst sieht es unnatürlich aus.
Die Cloud soll genau analysieren und Claude genau sagen, wo er Klippen machen soll usw.“

## Messung (meine, `vorlagen/daten/gefaelle/steile_strecken.json`, Wasserspiegel aus `vorlagen/daten/sehens/wasser_welt.json` + `baeche_alle.json`)

| | gesamt | > 2 % | > 5 % | > 10 % | > 20 % | > 30 % |
|---|---|---|---|---|---|---|
| Flüsse (27 Abschnitte) | 11,5 km | 3,30 km | 1,77 km | 1,05 km | 0,23 km | 0,07 km |
| Bäche (168, ohne ersetzte) | 32,8 km | 24,68 km | 17,90 km | 11,05 km | 3,49 km | 1,18 km |

161 zusammenhängende steile Strecken mit ≥ 1,5 m Fall (Flüsse > 4 %, Bäche > 10 %): 19 Fluss-, 142 Bach-Strecken. Die größten: Bäche in H3
(`B_R_P4_M2_04` 134 m Fall auf 573 m, Ø 23 %, max 63 %; `B_K8_ELFENFALL_01` 115 m auf 448 m), D2, B3, B6, E2, G3; Flüsse `F_ERLENBACH_1V_C2` (57 m auf 181 m,
schon mit Stufen gebaut, siehe unten) und `F_ELFENFLUSS_3_H4` (45 m auf 418 m). Heute laufen alle diese Strecken als **glatte, schräge Wasserrampe**
den Hang hinunter – Epic Water zeichnet eine geneigte Fläche, das wirkt unnatürlich (Bilder `bilder/wasser_fx/KASKADE1_*`, `STUFEN1_*`, `bilder/sehens13/*`).

## Was in der Natur passiert (bitte als Regelwerk ausarbeiten, mit Quellen)

- **Step-Pool-Folgen** (Bäche 5–30 %): ruhige Becken (≤ 2–3 %) abwechselnd mit Stufen aus Blöcken/Felsriegeln, Stufenhöhe ~ 0,5–3 m, Abstand
  ~ 1–4 Bachbreiten; **Kaskaden** über Blockwerk; **Fälle** an anstehendem Fels (Felsstufe/Klippe 2–15 m) mit Kolk darunter.
- **Klammen/Schluchten** (> 30 %): senkrechte Wände, Wasserfall-Kette, Gumpen, verkeilte Blöcke.
- **Flüsse** (4–15 %): Stromschnellen mit Blöcken, Katarakte, einzelne Stufen; Wasserspiegel nie als lange Schräge.
- Wo ist der Fels? Härteres Gestein bildet die Stufe (Schichtkante); unterhalb Schuttkegel, Blöcke, Prallhang. Bitte biomgerecht
  (Bergwald/Gletscher: Granit/Gneis, Canyon/Wüste: geschichteter Sandstein, Lava: Basalt, Elfenwald: bemooster Fels, Karst: Kalk).

## Was ich schon kann (Erfahrung C2/H4, Auftrag 12/14)

- Bach an jeder Stufe in **eigene Epic-Flussstücke** teilen (Lücke ≥ 1,2 m, keine Überlappung) – funktioniert (C2: 11 Stücke).
- **Vorhang-Netz** über die Kante + Schaumscheibe + Schaum in der Schaumkarte – Material ist noch zu weiß (wird mit Auftrag 14 / Nature Water FX
  ersetzt bzw. ergänzt: `NS_Waterfall_*`, `NS_Impact_*`, `NS_Stream_*`).
- Gelände per Delta-Höhen im 1-m-Raster ändern (Bett eintiefen, Stufe/Klamm ausformen) – je Feld in zwei Phasen, Pflanzen/Akteure werden mitgezogen.
- Felsen/Blöcke als Akteure oder Foliage setzen (Format `vorlagen/FORMAT.md` §3), Bodenlagen (Kies/Geröll/Fels/Moos) im Bett und am Ufer.

## Lieferung (bitte wie bei den Sehenswürdigkeiten: Regelwerk + Planer-Skript, lokal lauffähig auf 1 m)

1. `antworten/15-gefaelle.md`: Regelwerk (Schwellen je Art/Biom, Stufenhöhen, Abstände, Fels-Typen je Biom, Quellen) + **Prioritätenliste der 161 Strecken**
   (sichtbar vom Weg / an Sehenswürdigkeiten zuerst; dafür habt ihr die Sichtlinien aus `sehens_lib`) – Pilot: die 20 wichtigsten.
2. Planer `antworten/skripte/gefaelle/gefaelle_plan.py` (+ `gefaelle_regeln.json`), Aufruf `python -I gefaelle_plan.py [--laeufe ID …] [--daten2m …]`,
   Ausgabe je Lauf `export/unreal/welt/gefaelle/<lauf>/plan.json`:
   - `spiegel_neu_cm`: neue, **stufenförmige** Wasserlinie `[[x, y, z, breite_cm], …]` (Becken flach; Stufe = zwei Punkte ≤ 1 m auseinander),
   - `stufen`: je Stufe `lippe_cm` (Polylinie quer über den Bach), `fuss_z_cm`, `fall_m`, `art` (fall | kaskade | schnelle),
   - `gelaende`: Delta-Höhen-Datei + `fenster_ij` (wie `vorlagen/SEHENS_FORMAT.md` §3: Bett, Kolk, Felsstufe, Klamm),
   - `lagen` (wie SEHENS_FORMAT §3), `instanzen`/`akteure` (Felsriegel, Lippenfelsen, Blöcke, Schutt – Netze nur aus `daten/netze.csv`),
   - `effekte`: Nature-Water-FX je Stufe (wie SEHENS_FORMAT §6, `typ: niagara`), höchstens 3 je Stufe, Cull 40–60 m.
3. Kameras je Pilot-Strecke (`_vorher`/`_nachher`, Augenhöhe `Hoch = -170`, SEHENS_FORMAT §8).

Wichtig: Wasserspiegel nie steigend; Teilstücke in der Draufsicht nicht überlappend; vorhandene Wege, Orte und Sehenswürdigkeiten respektieren
(`daten/sehens/weg_2m.png`, `ort_2m.png`, eure `standorte.json`). Kein Projekt-Quellcode ins Repo; Formate sind hier beschrieben.
