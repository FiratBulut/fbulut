# sehens_aue – Planer Sehenswürdigkeiten Aue (Auftrag 13, Phase 2)

Baut die 8 Aue-Orte aus `antworten/sehens/aue/standorte.json` nach `sehens_aue_regeln.json`
(Katalog `sehens/aue/katalog.md` inkl. „Abgleich 13b/13c“, `asset_bedarf.json`, Inventar 13d) im Lieferformat
`vorlagen/SEHENS_FORMAT.md`. Muster: [`../sehens_bergwald/`](../sehens_bergwald/), Anleitung
[`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_aue/sehens_aue.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/aue]
python -I sehens_aue.py --basis <production>      # lokal: 1 m aus export/unreal/welt, Ausgabe dort
```

Leitidee: Jeder Ort erzählt eine Kraft des Flusses – er nagt (Schwalbenwand), baut (Treibholzwerder), verlässt sein
Bett (Mondarm, Lilienrinne), speist (Blautopf), düngt und überflutet (Lianenhalle, Die Alte), und wer ihn staut (Biberstau).

Eigener Code (alles andere sind Regeln):
- Hook `wand` (Schwalbenwand): Ober-/Fußkante, Terrasse und Wandfuß als Parallelen zur Wandlinie (aus der steilsten
  Stelle je Querprofil der 2-m-Daten).
- Hook `spiegel` (Mondarm): Der Altwasser-Spiegel steht in keiner Datei (teiche.json kennt nur den Westarm) → Median der
  Uferzellen von `karte_wasser` (2 m: 14,19 m); Seerosen liegen darauf (`z_bezug: "z:auto"`).
- `zugang_punkte` (Biberstau): Der Fußweg aus Phase 1 lief durch den neuen Teich → um das Südufer herumgeführt
  (Endpunkt am Weg unverändert).
- Regel `verdeckung` (Mondarm): Prüfung mit `sehens_lib.verdeckung` (Stempel + geplantes Gehölz) gegen alle Wegpunkte.

## Testlauf 2 m (11.10.2026, ~70 s, zwei Läufe byteidentisch)

Je Feld: C4 3 645, C5 2 193, D5 1 452, E5 8 594, F4 4 185 Instanzen (weit unter 60 000).

Planer 0 FEHLER / 0 WARNUNG; Prüfer (`orte.json` + `sw_aue`) **0 FEHLER, 0 WARNUNG**, nur HINWEISE (Brutröhren-Decal
noch ohne Material, Instanzen im Bestandswasser = gewollte Ufer-/Wassergruppen, Hainbuche braucht den Material-Fix sw_*).

| Ort | Instanzen | Koll. | Akteure | Held / Begl. / Schutt / Kleinzeug / Bewuchs / Kontakt | Wasser | Effekte | Stempel |
|---|---|---|---|---|---|---|---|
| 01 Biberstau | 1 846 | 80 | 14 | 9 / 75 / 60 / 1 136 / 123 / 433 (+24 Treibknüppel) | Stauteich `moorbraun` (Spiegel 35,9 m) + Überlauf | NS_Stream_Small, NS_Impact_Small, Nebel, 3 Decals | 2,2 m |
| 02 Die Alte | 1 799 | 44 | 14 | 1 / 7 / 40 / 979 / 662 / 116 | Bach bleibt | NS_Sparkling_Noise (opt.), 4 Decals | 0,6 m |
| 03 Schwalbenwand | 2 193 | 110 | 31 | 10 / 21 / 115 / 970 / 410 / 675 | 2 Pfützen in der Altrinne | Brutröhren-Decal (eigene Textur), Lehm-/Nass-Decals | 1,7 m |
| 04 Treibholzwerder | 3 356 | 154 | 24 | 17 / 7 / 136 / 1 800 / 269 / 1 128 | Bestand | NS_Wake_Medium, Nassband, 6 Decals | 0,8 m |
| 05 Lilienrinne | 4 060 | 45 | 1 | 1 015 / 228 / 61 / 960 / 1 514 / 207 (+70 Tümpelkiesel) | Tümpel `klar` | Bodennebel, 5 Decals | 1,5 m |
| 06 Mondarm | 2 630 | 119 | 9 | 322 / 9 / 40 / 1 048 / 792 / 416 | Bestand (Spiegel ~14,2 m) | Nebel, 4 Decals | – |
| 07 Blautopf | 1 641 | 65 | 8 | 5 / 2 / 40 / 758 / 404 / 412 (+9 Grund) | Quelltopf `tiefblau` 9 m + Quellbach | NS_Wake_Small, Nebel, 3 Decals | 10,4 m |
| 08 Lianenhalle | 2 544 | 61 | 10 | 56 / 12 / 77 / 1 437 / 695 / 276 | – | Spot (Lichtschacht), Nebel, NS_leaf, 7 Decals | – |

Alle Orte weit unter §9. Material-Instanzen 6 von 6: `MI_EL_SW_Lehmwand`, `_Kalk_Moos`, `_Ufer_Nass`, `_Weiderich`,
`_Treibholz`, `_Brutroehren` (Decal, Texturen `sehens/aue/decal_brutroehren*.png`).

## Witcher-Qualität – was die Regeln bauen

- **Biberstau:** `see` mit Becken (Stauteich, Spiegel 35,9 m = Damm 1,6 m über dem Bach), Dammbogen flussab gewölbt
  (Stämme als Akteure, Äste, Reisig, Schlamm-Lage), Burg auf Schlammsockel, 3 ertrunkene Fichten im Teich, Espe mit
  Krone im Wasser, Nagestümpfe mit Spänen und Stockausschlägen, Röhricht nur am Einlauf.
- **Die Alte:** Schwarzpappel ×1,3 (13c), Wurzelhügel, Wurzelanläufe bis ans Bachufer, Starkast mit Pilzen, dunkler
  Brennnessel-/Holunderring unter der Traufe, drei Blumeninseln auf der Sonnenseite, drei Jungeichen (`SM_dry_oak_*`).
- **Schwalbenwand:** Lehmwand aus `SM_LS_beach_cliff_02_*` (×1,3 in Z, MI_EL_SW_Lehmwand) entlang der echten 9-m-Stufe,
  Abbruchkante oben, Kante +1,3 m, kippende Pappel mit Wurzelteller, zwei Schuttkegel (unten gröber), Wurzelvorhang,
  Altrinne mit Restwasser-Pfützen, Pestwurz, Schachtelhalm; Brutröhren als eigenes Decal (7×, oberes Wanddrittel).
- **Treibholzwerder:** Verklausung in drei Lagen (`z_bezug: oben:`) am flussaufwärts gerichteten Inselkopf,
  gestrandeter Baum mit hochkant gestelltem Wurzelteller, Weiden im Strömungsschatten, Kies nach Größe sortiert
  (Gradient), Pioniere nur auf der Fahne, Nassband rund um die Insel.
- **Lilienrinne:** Flutrinne entlang der Tiefenlinie (Sohle fällt stetig), Tümpel, goldenes Band, purpurne Inseln
  (MI_EL_SW_Weiderich), Spülsaum quer zur Rinne in Fließrichtung, Feuchtegradient Binsen → Lilien → Pestwurz → Wiese.
- **Mondarm:** Seerosenfelder in beiden Buchten, liegende Weide mit Austrieb, Wurzeln am Uferabbruch, **220-m-
  Ufergehölz-Gürtel** (13c) in zwei versetzten Bögen mit Lücke für den Zugang → Verdeckungsprüfung: **verdeckt** (Kern +
  4 Proben, 0 von ~48 Wegpunkten).
- **Blautopf:** Trichter 9 m (`see` mit Becken, `ist_wasser`, begründet), halbrunde Kalkwand (Steig an der Ostseite
  bleibt frei), überhängende Buche, versunkener Stamm in 7,3 m Tiefe, Kalkplatten-Kragen, Farne/Efeu/Moos.
- **Lianenhalle:** vier Altbäume als Torpfosten, Lianenvorhang in zwei Lagen (11 m), Genist an allen Stämmen auf 1,65 m,
  Schlammlinie als Decal in 1,75 m (alle gleich hoch), Frühlingsteppich, Lichtschacht + Nebel.

## Grenzen und offene Punkte

- Front-/Schauseite der Lehmwand (`front_achse +y`) und der Kalkwand sind Annahmen – Prüfbild `_held` entscheidet.
- Mondarm-Spiegel ist geschätzt (14,19 m aus den Uferzellen); Seerosen ggf. im Editor nachziehen.
- Nature Water FX, Coast & Dunes und Mountain sind seit 13d echt eingesetzt (Bach-/Fall-Effekte, Nassband- und
  Lehm-Decals, `material_hinweis` M_River_Water_Translucent). Weiter fehlend: Stieleiche, tote Eiche, Erlen, Driftwood,
  große Kalkfelsen, Forest Fungi, Niagara-Laub (in `assets_wunsch`).
- Pfadbänder werden auf das Lagenfenster gekappt; der volle Fußweg steht in `orte.json["pfad"]`.
