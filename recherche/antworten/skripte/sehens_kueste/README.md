# sehens_kueste – Sehenswürdigkeiten-Planer Küste (Auftrag 13, Phase 2)

Baut die 8 Küsten-Orte aus `antworten/sehens/kueste/standorte.json` nach `sehens_kueste_regeln.json`
(Katalog `sehens/kueste/katalog.md` inkl. „Abgleich Inventar 13d“, `asset_bedarf.json`, Entscheidungen Ferat in
`sehens-STATUS.md`) im Lieferformat `vorlagen/SEHENS_FORMAT.md`. Muster: [`../sehens_bergwald/`](../sehens_bergwald/),
Schema: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md). Inventar: 13d (Coast & Dunes,
Nature Water FX, Mountain vollständig).

```
python -I recherche/antworten/skripte/sehens_kueste/sehens_kueste.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/kueste] [--gruppen]
python -I sehens_kueste.py --basis <production>      # lokal: 1 m aus export/unreal/welt, Ausgabe dort
```

Eigener Code (alles andere sind Regeln):

- `KuesteKontext` (Unterklasse von `rezept.OrtKontext`):
  - `boden_min_m` (nur Akteure): Pfeilerfüße, Stümpfe und Brandungsblöcke stehen auf der gestempelten
    Brandungsplattform unter dem Meeresspiegel. Foliage bleibt bei der Lib-Regel > −0,3 m.
  - `boden_ab_m`: Sicherheitsabstand für Foliage an steilen Stempelkanten (1-m-Umrechnung im Prüfer).
  - Meer (Gelände nach Stempel < 0 m) zählt als Wasser: Plattform, Torgang und Blasloch-Gang sind keine „Senke ohne Wasser“.
- Hooks: `hook_tuempel_anker` (11 Tümpel auf der Gezeitenbank), `hook_seefall_ende` (Fallfuß = Meeresspiegel),
  `hook_duene` (Dünenkamm mit `Stempel.damm`, Luv flach, Lee steil).
- Nach dem Bauen prüft der Planer die vier Fundstücke mit `verdeckung.py` (Stempel + Stücke): alle **verdeckt**
  (Seefall, Gezeitenbank, Dünenkamm, Blasloch – Verdeckung durch Kliffkante/Schulter, also durch das Bestandsgelände).

## Testlauf 2 m (11.10.2026, ~43 s, zweimal byteidentisch)

Planer 0 FEHLER / 0 WARNUNG. Prüfer (`orte.json` + `sw_kueste`, mit Daten und Inventar 13d): **0 FEHLER, 0 WARNUNG**,
2 HINWEISE (Nadeltor |Δ| 49 m begründet, 26 Kiesel ganz im Boden).

| Ort | Inst. | Koll. | Akteure | Held / Begl. / Schutt / Kleinzeug / Bewuchs / Kontakt | Wasser | Effekte | Stempel |
|---|---|---|---|---|---|---|---|
| 01 Die Alten | 881 | 45 | 35 | 3 / 6 / 39 / 650 / 50 / 136 | Meer | 3 Niagara (Impact, Wake), Nebel, 7 Decals | 13,4 m |
| 02 Vogelinsel | 1 452 | 146 | 11 | 4 / 7 / 90 / 930 / 122 / 242 | Meer | NS_feather (fest, E03), 9 Decals | 17,0 m |
| 03 Nadeltor | 704 | 38 | 30 | 4 / 4 / 22 / 420 / 40 / 206 | Meer, Torgang | Impact + Wake, Nebel, 5 Decals | 49,2 m (begr.) |
| 04 Seefall | 978 | 133 | 14 | 2 / 6 / 81 / 500 / 106 / 228 (+8 Bachsteine) | Wasserfall 54 m | Waterfall_Large, Impact_Large, Stream_Small, Nebel, 8 Decals | 17,9 m |
| 05 Gezeitenbank | 1 645 | 229 | 11 | 4 / 7 / 94 / 910 / 45 / 345 (+90 Tümpelsteine) | 11 Tümpel (see) | 12 Decals | 7,1 m |
| 06 Kreidewand | 1 587 | 227 | 12 | 3 / 9 / 127 / 994 / 53 / 313 | Meer | 11 Decals | 29,4 m |
| 07 Dünenkamm | 1 641 | 73 | 9 | 2 / 7 / 70 / 882 / 520 / 166 | Meer | NS_leaf opt., 11 Decals | 4,3 m |
| 08 Blasloch | 451 | 93 | 13 | 2 / 5 / 96 / 156 / 83 / 101 | Schacht + Gang (Meer) | Geyser_Large, Impact_Medium, Nebel, 5 Decals | 15,7 m |

Alle Orte unter §9. Felder: A5 3 982, A6 1 503, B5 126, B6 49, H2 3 633, H3 46 Instanzen.
Material-Instanzen 5 von 6: `MI_EL_SW_Brandungsfels`, `_Guano`, `_Kreide`, `_Windstill`, `_Schwarzfels`.

## Umsetzung der Orte

- **Die Alten:** Ferats Vorgabe – großer Pfeiler aus 3 Stücken übereinander (`SM_MassiveNordicCoastalCliff_01` ×1,45 →
  `veqnci0db_tier_2` hochkant → `SM_MassiveNordicCoastalCliff_01` ×0,82, Kopf ~49 m), Rückschale `veqnci0db_tier_2`;
  kleiner Pfeiler aus 2 Stücken (`SM_MassiveNordicCoastalCliff_01` + `vdssailfa_tier_2` hochkant, 8° zum großen geneigt);
  3 Stümpfe. Gelände: Brandungsplattform −1,6 m, Blocksockel +0,5 m am Fuß (Kontaktzone über Wasser).
- **Vogelinsel:** Guano-Wand (4 Schalen, `MI_EL_SW_Guano`) an der **Kliffseite** (Osten), weil alle Kameras dort stehen;
  Blockstrand +0,7 m am Wandfuß.
- **Nadeltor:** Torgang 8 m breit durch den Höhenfeld-Pfeiler bis −2,6 m (|Δ| 49 m, Ferat frei gegeben, `begruendung`
  gesetzt). Beine `veqnci0db_tier_2` hochkant, Sturz `SM_MassiveNordicCoastalCliff_01` mit Unterkante +8 m (`z:8`),
  darüber `veqnci0db_tier_2`. Achse zwischen `_anmarsch` und `_held` → Blick durch das Tor.
- **Seefall:** Wasserfall 54 m von der Lippe in einen Schaumkessel (−1 m, Rinne zum Meer), Kerbe −0,5 m, Kanzel,
  6 Kliffschalen in Lagen (`z:`), Nature Water FX nach dem Bergwald-Klamm-Vorbild. Wassermaterial nur als
  `material_hinweis` (M_River_Water_Translucent, kein Pfad im Inventar).
- **Gezeitenbank:** Felsbank +1 m (30 × 14 m), 11 Tümpel mit Seetang, Muscheln und Steinen am Grund.
- **Kreidewand:** Abrissnische 62 × 24 m (Gleitfläche fällt von +9 auf +4,2 m zum Strand), weiße Nord- und Kopfwand
  (`MI_EL_SW_Kreide`), Buche mit der Krone im Wasser (`MI_EL_SW_Windstill`), Feuerstein (`MI_EL_SW_Schwarzfels`).
- **Dünenkamm:** Wall +3,7 m mit Luvschürze, begrabene Kiefer (Wanderdüne), Strandhafer in eine Richtung gekämmt.
  Das Dünental dahinter ist eine gewollte Senke (`senke_begruendung`).
- **Blasloch:** Platte über der Bucht, Gang (Rinne) vom Loch bis unter den Meeresspiegel. Felsdächer über dem Gang
  sind Netze (Überhang), die Fontäne ist `NS_Geyser_Large`.

Pfade: Der Klippensteig und der Kap-Pfad werden je Ort abschnittsweise vergeben (`abschnitt`). Beim Kap-Pfad sind die
Bereiche fest gesetzt, weil Dünenkamm und Blasloch beide am Pfadende liegen. Seefall und Gezeitenbank haben zusätzlich
ihren Zugang (`zugang` → `pfad_zugang`). Am Klippensteig gibt es Felsstufen (`SM_flat_rock_04`, `Basalt_Basalt_Rock_B_SM`)
zwischen 22° und 40°; steiler werden es Kehren aus Ferats Werkzeug.

## Grenzen und offene Punkte

- Netze ohne Bounds in `netze_masse.json` (alle Klippenschalen) gelten als „Pivot unten Mitte“. Die Schauseite
  (`front_achse`) ist eine Annahme, das Editorbild entscheidet. Die Unterseite des Tor-Sturzes ist ungeprüft.
- Bei Die Alten, Vogelinsel und Blasloch liegt der eigene Pfadabschnitt außerhalb des Lagenfensters. Ein Pfadband gibt es
  dort nicht; der Abschnitt steht nur in `orte.json["pfad"]` (HINWEIS).
- Klänge: Brandung und Seevögel fehlen. Als Platzhalter laufen `CUE_Water_Stream_*` (Ferat 11.10.: er erzeugt die Klänge
  selbst per KI, Klangpakete nicht geladen; die zweite Brandungsquelle aus E29 entfällt deshalb – ein Asset-Name für
  „Procedural Sea Waves“ ist im Inventar nicht belegt). `assets_wunsch` nennt Wilderness Nature Loops nur noch historisch.
- Vogelwolke `NS_feather` fest (E03): ferne Punkte über der Brutwand in 45 m Höhe, Cull 400 m. Brutwand = Ostflanke (E02).
- Houdini-Steilküste K9 (E23): `freiraeume` mit Rolle `houdini` und den Netzen `SM_K9_STEILKUESTE__FELS/__SEHENS/
  __SEHENS_DECKE` an kueste_01 (r 150 m) und kueste_03 (r 90 m) – nur Kachelteile unter den neuen Pfeilern ausblenden
  (Prüfschritt im Outliner); `__WASSER` bleibt.
- **13f:** `efeu_kante` mit `z_frei` (A6). Tümpel der Gezeitenbank mit r ≥ 1,8 m (≥ 10 m², A13); es passen 4 auf die Bank.
