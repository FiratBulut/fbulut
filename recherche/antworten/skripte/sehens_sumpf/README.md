# sehens_sumpf – Planer Sehenswürdigkeiten Sumpf (Auftrag 13, Phase 2)

Baut die 8 Sumpf-Orte aus `antworten/sehens/sumpf/standorte.json` nach `sehens_sumpf_regeln.json`
(Katalog `sehens/sumpf/katalog.md`, `asset_bedarf.json`, Inventar 13d) im Lieferformat `vorlagen/SEHENS_FORMAT.md`.
Muster: [`../sehens_bergwald/`](../sehens_bergwald/), Anleitung [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_sumpf/sehens_sumpf.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/sumpf]
python -I sehens_sumpf.py --basis <production>      # lokal: 1 m aus export/unreal/welt, Ausgabe dort
```

**Das Wasser:** Der Sumpf ist der Epic-See `T_2954_391` (Spiegel 1,58 m) plus Teiche gleichen Spiegels – keiner davon
steht in `karte_wasser`. Jede Regel lädt sie mit `"bestandswasser": {"seen": "auto"}` (Lib-Erweiterung: nass nur, wo das
Gelände nach dem Stempel unter dem Spiegel liegt). Damit funktionieren `im_wasser`, Ufer-Verteilungen, Nassband und
`z_bezug: "spiegel:T_2954_391"` (treibendes Holz, Seerosen, Riesenblätter). Kein Ort schreibt einen eigenen `see` in den
Epic-See (sonst doppelte Wasserflächen). **Hauptsee bleibt Bestandsfarbe (E09); `schwarz_spiegel` nur für eigene
`see`-Körper** (z. B. die drei Augen in sumpf_04) – ein Wasserkörper hat ein Material, Teilfärbung bräuchte überlappende
Körper. Die alten Farbwünsche stehen nur noch als Hinweis in den Regeln.

Eigener Code (alles andere sind Regeln):
- Hook `zugang` (alle Orte): `standorte.json` hat für den Sumpf weder `pfade` noch `pfad_cm`; der Planer rechnet den
  Fußweg mit `kandidaten.erreichbarkeit` (Ort → nächster Weg), kürzt ihn am Ort auf das erste Ufer (Wasser im Kern bleibt
  frei) und hebt nasse Abschnitte draußen als **Bultenrücken** (Stempel auf Spiegel + 0,22 m, 2,2 m breit, gesäumt von
  Seggenbulten) – kein Steg, keine Menschenspur.
- Regel `verdeckung` (Erlenbruch): Prüfung mit `sehens_lib.verdeckung` (Stempel + geplantes Gehölz) gegen alle Wegpunkte.

## Testlauf 2 m (11.10.2026, ~80 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG, Prüfer (`orte.json` + `sw_sumpf`) **0 FEHLER, 0 WARNUNG, 0 HINWEIS**.
Je Feld: H4 2 001, H5 17 782, I5 1 931 Instanzen (weit unter 60 000).

| Ort | Instanzen | Koll. | Akteure | Held / Begl. / Schutt / Kleinzeug / Bewuchs / Kontakt | Effekte | Stempel |
|---|---|---|---|---|---|---|
| 01 Ertrunkener Wald | 4 943 | 219 | 13 | 47 / 12 / 175 / 2 119 / 1 246 / 1 357 | Nebel, 5 Decals | 0,8 m (Bultenrücken) |
| 02 Weidendom | 2 619 | 100 | 29 | 9 / 20 / 100 / 353 / 1 163 / 1 003 | Nebel, 3 Decals | 0,8 m |
| 03 Reiherhorst | 2 221 | 61 | 3 | 3 / 25 / 80 / 500 / 598 / 1 018 | NS_feather, 5 Decals | 1,3 m |
| 04 Schwingrasen | 2 641 | 23 | 7 | 1 / 7 / 320 / 760 / 922 / 638 | Nebel, 4 Decals | 3,3 m (Augen) |
| 05 Erlenbruch | 2 001 | 336 | 24 | 22 / 24 / 150 / 700 / 667 / 462 | Nebel, 4 Decals | 1,9 m |
| 06 Bultenfeld | 3 458 | 35 | 0 | 292 / 8 / 40 / 1 900 / 661 / 557 | NS_leaf, 2 Decals | 1,0 m |
| 07 Tellerweiher | 2 923 | 34 | 1 | 30 / 46 / 34 / 1 147 / 1 110 / 557 | 1 Decal | – |
| 08 Irrlichtsenke | 908 | 150 | 9 | 5 / 4 / 150 / 377 / 240 / 141 | Nebel, 2× NS_Sparkling_Glow, 2 Punktlichter, 4 Decals | 1,0 m |

| Ort | Held | Kern der Umsetzung |
|---|---|---|
| 01 Ertrunkener Wald | 46 tote Fichten + „weißer Riese“ im Wasser | Bruchstämme (MI_EL_SW_Silberholz), Sumpfzypressen-Füße, 150 Treibholzstücke auf dem Spiegel, Röhricht nur am flachen Rand, Nebel, Bultenrücken 38 m |
| 02 Weidendom | 9 Riesenweiden ×1,3–1,5 im Ring r 24 m auf Kniewurzeln (`SM_SwampCypress_A`) | Wanne bis 0,36 m unter den Spiegel + Innenmulde, Torweide, treibende Zweige, Wasserlinsen/Seerosen innen, Röhrichtgürtel außen, Kronen MI_EL_SW_Weide_Grau |
| 03 Reiherhorst | 3 tote Baumriesen auf der Moosinsel (+0,3 m) | Reisighorste in 9,5 und 12,5 m, gekalkter Boden (Decal), Fallholz, überdüngtes Hochgras, Federn (NS_feather) |
| 04 Schwingrasen | 3 Mooraugen (`schwarz_spiegel`, 3/2,5/2 m tief) + versinkender Birkenstamm | Torfmoos-Polster (MI_EL_SW_Torfmoos), überhängende Moosränder, Moorbirken-Saum |
| 05 Erlenbruch | 22 Bäume auf Wurzelsockeln (0,6–0,9 m hochgesetzt) | Schlenke `moorbraun` + Rinnsal vom Hang, Torbaum mit Wurzelteller, Farn auf jedem Sockel, **Gehölzring r 31–46 m → verdeckt** |
| 06 Bultenfeld | ~300 Seggenbulten in Gruppen | Bulten-Höcker (Stempel), 3 Schlenken `moorbraun`, Grauweiden, Altholz, Samenflug |
| 07 Tellerweiher | 22 Riesenblätter (VarB ×4,0 → 2,5, vorn groß) + Blüten | normale Seerosen hinten, Rohrkolbengürtel, Trauerweide, Treibholz |
| 08 Irrlichtsenke | Nebelbank + Glimmen (NS_Sparkling_Glow ×2, 2 Punktlichter 40/30 cd, E08) | Mulde −0,4 m + Schlammtümpel, tote Bäume als Rahmen, Stümpfe, Pilze |

Material-Instanzen 4 von 6: `MI_EL_SW_Silberholz`, `_Torfmoos`, `_Weide_Grau`, `_Birke_Dunkel`.

## Grenzen und offene Punkte

- Graveyard-Totbäume (`SM_Dead_Tree_*`) haben Blattkarten – Blätter-Slot im Editor ausblenden; Kotflecken
  (`MI_Leakage_08`) im Editor weiß tönen (Hinweise im Ort).
- Reiherhorste sitzen auf fester Höhe neben den Stämmen (Astgabeln sind nicht bekannt) – im Editor an die Gabeln schieben.
- Irrlicht-Punktlichter entschieden (E08): 40 und 30 cd, Radius 5 m, ohne Schatten, gelbgrün – sichtbar bei fester
  Tagsonne, bleiben unter den Leuchtpilzen des Elfenwalds (180–300 cd).
- Tiere (E04): keine; Reiherhorst ohne Fischgräten (E05, Knochen-Regel – der Planer setzt keine).
- Erlen fehlen weiter (Birke/Pappel, 13c); Pfadbänder werden auf das Lagenfenster gekappt.
- **13f:** Erlenring im Osten verdichtet (`erlenring_ost`, 45 Bäume im Ostsektor). Die Schlenke liegt jetzt am tiefsten
  Punkt der Rinne (Anker-Suche), damit das Rinnsal hinein- und nicht bergauf fließt.
- **Nachtrag 13k (Stammausrichtung):** In `treibende_aeste` (Weidendom) bleiben die stehend modellierten
  `Branch_Goat_Willow_Decaying_*` auf `liegend`. Das liegend modellierte `SM_dead_log_02` setzt das Rezept jetzt mit
  `normale` (32 Stück). Vorher stand es senkrecht oder lag auf der Kante. Ergebnis in
  `antworten/13k-pilot2-bildbefund-15g-nachtrag.md`.
