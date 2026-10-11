# sehens_heide – Sehenswürdigkeiten-Planer Heide (Auftrag 13, Phase 2)

Baut die 8 Heide-Orte aus `antworten/sehens/heide/standorte.json` (keine `pfade`; Zugänge aus `pfad_cm`) nach
`sehens_heide_regeln.json` (Katalog `sehens/heide/katalog.md`, `asset_bedarf.json`, Entscheidungen Ferat, Inventar 13d)
im Lieferformat `vorlagen/SEHENS_FORMAT.md`. Muster: `../sehens_bergwald/`, Schema: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_heide/sehens_heide.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/heide] [--ohne-sicht]
```

Eigener Code: `gelaende.daemme` (Kesselkranz, Parabeldüne, Kesselrand, Felsrahmen, Klammufer), Zugang endet vor dem Held
bzw. am Ufer (`pfad.ende_r_m`), Verdeckungsprüfung der Fundstücke (`sehens_lib/verdeckung.py`). Alles andere sind Regeln
(Tor-Stapel mit `auf_gruppe` + `z_bezug oben:`).

**Ferat (Brushify abgelehnt):** Ginster = Sanddorn (`MI_EL_SW_Ginster` grün, `MI_EL_SW_Ginstergold` **gelb getönt** – auch
auf weißen Windröschen als Blütenköpfe), Wacholder = schlank skalierte Jungkiefern (`MI_EL_SW_Wacholder`), Wollgras =
Binsen + weiße Windröschen ×0,4. Eigene Decal-Textur `sehens/heide/decal_russ.png` (+ `_n`) für den alten Heidebrand
(Materialwunsch `MI_EL_SW_Russ_Decal`, Decal `optional` bis Ferat es anlegt).

## Testlauf 2 m (11.10.2026, ~75 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer **0 FEHLER, 0 WARNUNG**, 3 HINWEIS (Russ-Decal noch nicht im Inventar).

| Ort | Inst. | Koll. | Akt. | Held/Begl./Schutt/Klein/Bewuchs/Kontakt | Wasser, Effekte | Stempel |
|---|---|---|---|---|---|---|
| 01 Graue Burg | 3 434 | 149 | 13 | 5/6/160/700/957/1 608 | Felsschüssel-Decal | 2,0 m |
| 02 Ginstergold | 6 092 | 2 | 2 | 1/120/8/1 821/3 629/515 | Russ-Decals (eigene Textur) | – |
| 03 Wacholderprozession | 1 585 | 3 | 48 | 1/47/3/645/701/236 | – | 1,2 m |
| 04 Kolk | 3 016 | 22 | 11 | 1/105/22/1 783/858/258 | Kolk schwarz_spiegel, Nebel | 2,2 m |
| 05 Wackelstein | 2 034 | 39 | 14 | 2/12/58/450/661/865 | Felsschüssel-Decal | 3,2 m |
| 06 Wollsackfall | 2 402 | 191 | 30 | Fallstufen/Klammtor/… | Klammbach (3 Stufen), Gumpe, Fall, Auslauf; NS_Waterfall_Small, NS_Impact_Small, NS_Stream_Small; Spot, Nebel | 4,0 m |
| 07 Totengrund | 4 716 | 29 | 4 | 3/7/40/380/3 861/… | – | 4,9 m |
| 08 Windkante | 2 054 | 14 | 17 | 3/14/54/426/1 290/284 | Rippel-Decals (Coast & Dunes) | 4,0 m |

Verdeckung mit Plan: Wackelstein, Totengrund, Windkante **vollständig verdeckt**; Kolk Kern verdeckt, Ost/West-Probe
von 3 bzw. 1 Wegpunkt (wie heute); Wollsackfall Kern 15/124 Wegpunkten (heute 51) – Sicht kommt in der Bachachse von
Norden und Süden/Südwesten; Klammtore aus Riesen-Wollsäcken und dichte Gehölzsäume (Klammkopf, Ausgang) mindern sie.

## Grenzen und offene Punkte

- Wollsackfall ersetzt auf ~100 m den Bestandsbach `B_R2_R_P3_P0_01` (Ort IST dieses Wasser): Sohle in drei Stufen
  (absolute Höhen aus den 2-m-Daten – im 1-m-Lauf prüfen), Wassermaterial nur als `material_hinweis`.
- Tor-Stapel und Wackelstein ruhen per `z_bezug` aufeinander (z_frei) – Fugen im Editorbild prüfen.
- `senke_begruendung`: Burg (Verwitterungsschüsseln), Wacholder (Schlatts), Kolk (Regenmoor), Wackelstein (Felsenkessel),
  Totengrund (Nivationsmulde), Windkante (Deflationsmulde).
