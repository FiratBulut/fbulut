# sehens_gletscher – Sehenswürdigkeiten-Planer Gletscher (Auftrag 13, Phase 2)

Baut die 8 Gletscher-Orte aus `antworten/sehens/gletscher/standorte.json` nach `sehens_gletscher_regeln.json`
(Katalog `sehens/gletscher/katalog.md` inkl. „Abgleich Inventar 13d“, `asset_bedarf.json`, Entscheidungen
`sehens/entscheidungen.json`) im Lieferformat `vorlagen/SEHENS_FORMAT.md`. Muster: [`../sehens_bergwald/`](../sehens_bergwald/),
Schema: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_gletscher/sehens_gletscher.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--orte ID ...] [--bild --bild-ordner recherche/antworten/sehens/gletscher] [--ohne-sicht]
python -I sehens_gletscher.py --basis <production>      # lokal: 1 m aus export/unreal/welt, Ausgabe dort
```

`sehens_gletscher.py` ist die Vorlage für `sehens_frost.py` und `sehens_fjord.py` (dieselbe Datei, nur der Biomname ist
ersetzt). Eigener Code, alles über Regelschlüssel gesteuert:

| Hook | Regel | Wirkung |
|---|---|---|
| `hook_see_fuellen` | `wasser[see].fuellen {r_such_m, unter_rand_m}` | See füllt eine Bestandsmulde (Spiegel = Überlaufpunkt aus `gelaende.abfluss`), statt sie zu graben |
| `hook_rahmen` | `rahmen [{name, bei, ziel_hoehe_m, richtung_bereich, abstand_m, breite_m, hoehe_min/max_m, …}]` | Sichtwall für Fundstücke: rechnet auf dem Gelände **nach** Stempel die Steigpunkte, die den Ort sehen, und baut einen Damm-Bogen in der nötigen Höhe (gedeckelt); Linie `rahmen_<name>` für Felsen/Gehölz darauf |
| `hook_nach_ops` | `gelaende.nach_ops [damm …]` | Dämme/Wülste nach den Hauptstempeln |
| `hook_ende` | `sicht_kern`, `sicht_probe_m`, `sicht_ziel_m`, `sicht_r_max_m` | Verdeckungsprüfung (`sehens_lib.verdeckung`, Plan inkl. Felsen ≥ 1 m und Bäume) + Liste der Restblicke (Richtung/Abstand/dz); Senken-Meldung; `eis`/`material_wunsch`/`hinweis` der Wasserregeln nach `orte.json` |
| `hook_pfad_regel` | `pfad_regel {eis_boden, eis_max_grad, abstand_zu [{linie: "ort/linie", min_m}]}` | E22: meldet Pfadmeter auf Eis/Schnee steiler als erlaubt und den Mindestabstand zu einer Linie (auch eines anderen Orts) |

## Testlauf 2 m (11.10.2026, ~70 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer (`orte.json` + `sw_gletscher`) **0 FEHLER, 0 WARNUNG** (Lagenfenster 02/05 akzeptiert, E49).

| Ort | Inst. | Koll. | Akteure | Stempel | Held / Besonderheit |
|---|---|---|---|---|---|
| 01 Gletschertor | 3 429 | 258 | 29 | 10,1 m | Séracs-Band aus Ice Cliffs entlang der Bruchkante, Torpfeiler + Sturz (Large Ice Cliff), Gletscherbach (`material_hinweis` M_River_Water_Translucent), NS_Impact_Small + NS_Stream_Small, Nassband `MI_Deca_Wet` (ufer), Freiraum K7 r 170 m |
| 02 Lawinenkegel | 2 212 | 163 | 25 | 4,9 m | Kegel aus `Snow_Hill_vdbmabvva_High`, Lawinenschutt sortiert; natürlicher Kolk unberührt |
| 03 Moränensee | 2 037 | 355 | 7 | 42,2 m | Terrasse 190 m (**begruendung**), See `gletschermilch` eingepasst, Rahmen „riegel“ und „westriegel“, Zugang endet 2,5 m vor dem Wasser, `MI_Deca_Wet_Flat` + `MI_Decal_Rocks_Small` |
| 04 Toteisloch | 2 263 | 61 | 9 | 6,6 m | See füllt die Bestandsmulde (`fuellen`), Pfad endet vor dem Wasser, Rahmen „kesselrand“ |
| 05 Wächte | 1 178 | 97 | 67 | 3,0 m | Wächte aus `Snow_Embankment_uhvifcgfa_High`, Bergschrund als Abbruch, Gletschermühle mit Bach bis „muehle“, Fall (`material_hinweis`), NS_Impact_Small |
| 06 Gletschertöpfe | 1 916 | 374 | 40 | 15,6 m | Strudeltöpfe, Bäche, Auslass 355°, NS_Waterfall_Small + NS_Impact_Small |
| 07 Nunatak | 991 | 197 | 14 | 2,3 m | Felsinsel im Eis, Sichtkern am Fuß (VERDECKT) |
| 08 Gletscherschliff | 1 394 | 213 | 11 | 5,2 m | Rundhöcker mit `SM_flat_rock_01`, Schrammen-Decals; Pfad `gletscher_pfad_nordhang` als Schnee/Kies-Band (E22) |

Je Feld: D1 1 386, D2 6 499, E1 2 109, E2 5 426 Instanzen. Materialwünsche 4/6: `Gletschereis_Tief` (Eis4, nur
`SM_EISZAPFEN_*`), `Fels_Schneekappe`, `Klippe_Gletscherschliff`, `Findling_Flechte`. Die 31 Eis-/Schnee-Megascans behalten
`M_MS_Base_Trm` und stehen über die Lib in `material_fix_ausnahmen` (E34).

**Lagenfenster > 400 m (E49, akzeptiert):** 02 (330 × 414 m) und 05 (286 × 404 m). Beide sind Leuchtfeuer; der
Weststeig-Abschnitt, der ihnen nach `abschnitt: naechster` gehört, ist so lang. Die Regel `warnung_akzeptiert.lagen_fenster`
trägt die Begründung, der Prüfer meldet dann nur einen HINWEIS.

## Verdeckung der Fundstücke (Plan inkl. Wall, Felsen, Bäume; Ziel 3 m)

| Ort | Ergebnis | Rest |
|---|---|---|
| 03 Moränensee | 5 Steigpunkte (heute 10) | NO 44–73° in 209–311 m, **63–179 m höher**; 296°/457 m/+97 |
| 04 Toteisloch | Kern 1 Punkt, Anteil 0,15 | 343°/247 m/+187 |
| 06 Gletschertöpfe | 2 Punkte | 122–128° in 111–129 m, +119…+140 m |
| 07 Nunatak | **verdeckt** | – |
| 08 Gletscherschliff | 10 Punkte (heute 11) | Nordhangsteig direkt darüber (148–162°, 107–231 m, +112…+253 m) und 252–257° in ~600 m |

Die Restblicke kommen steil von oben (Steig über dem Ort). Ein Wall oder Gehölz hilft dort nicht. Das lässt sich nur über
die Steigführung lösen (siehe Bericht, Korrekturbedarf).

## E22/E47 – Steig über Eis

`gletscher_08` prüft `gletscher_pfad_nordhang` (`pfad_regel`). Das Band ist Schnee/Kies (200/135 ≈ 60/40), ohne
Bauwerk. Der Abstand zum Bergschrund (Linie `gletscher_05_die_waechte/bergschrund`) beträgt mindestens **151 m** (Soll ≥ 15 m).
Gletschereis (≤ 12°) berührt der Steig nicht. Er quert 248 m Schneefelder mit 17–30° in Serpentinen; nach **E47** gelten
sie nicht als Gletschereis, Kehren sind dort erlaubt. Die Linie bleibt, die Felsstufen (22–32°) bleiben gesetzt.

## Grenzen

- Pivot/Schauseite: Arbeitsannahme E35 (unten Mitte, +Y). Sobald `netze_masse.json` die Front liefert, einfach neu laufen lassen.
- Houdini-Reste `SM_K7_GLETSCHER__EIS` werden nicht verwendet. Unter 01/02/05 stehen sie als `freiraeume` (E23).
- Für die Schneefahne (05/07) gibt es kein Schnee-Niagara, sie bleibt als optionale `NS_Smoke_Plume`-Stelle. Den Kauf des Niagara-Snow-Pakets empfiehlt die Kaufliste nicht.
- Gewollte Hohlformen tragen `senke_begruendung` (Bergschrund, Strudeltöpfe, Kolke).
