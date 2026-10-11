# sehens_tundra – Sehenswürdigkeiten-Planer Tundra (Auftrag 13, Phase 2)

Baut die 8 Tundra-Orte aus `antworten/sehens/tundra/standorte.json` (inkl. `pfade`) nach `sehens_tundra_regeln.json`
(Katalog `sehens/tundra/katalog.md`, `asset_bedarf.json`, Entscheidungen Ferat, Inventar 13d) im Lieferformat
`vorlagen/SEHENS_FORMAT.md`. Muster: `../sehens_bergwald/`, Schema: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_tundra/sehens_tundra.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/tundra] [--ohne-sicht]
python -I sehens_tundra.py --basis <production>      # lokal: 1 m aus export/unreal/welt, Ausgabe dort
```

Eigener Code (Hooks, alles andere sind Regeln):
- `gelaende.daemme` → `Stempel.damm` (Wälle/Gräben: Pingo-Risse, Strandwall/Eisschubwall, Uferwälle am Wabenmoor)
- Zugang: `pfad_cm` endet am Ufer bzw. `pfad.ende_r_m` vor der Mitte (nicht über den Held oder ins Wasser)
- Fließtreppe: Solifluktionsloben (Lauffläche steigt zur Stirn, Stirn 3,5 m steil) + Anker an den Stirnen
- Steinringe: ~20 sortierte Ringe (verwackeltes Sechseckgitter, große Steine auf dem Ring, Grus innen)
- Wabenmoor: Eiskeilpolygone (Voronoi: Randwall, Graben, eingesenkte Mitte, 7 Tümpel als `see`, Grabenanker)
- Ende: Verdeckung der Fundstücke vom Weg/Pfad mit Stempel + geplanten Stücken (`sehens_lib/verdeckung.py`) → HINWEIS

## Testlauf 2 m (11.10.2026, ~75 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer (orte.json + sw_tundra, mit Daten und Inventar) **0 FEHLER, 0 WARNUNG**, 3 HINWEIS
(Flechte-Decal-Wunsch ohne Netz u. a.).

| Ort | Inst. | Koll. | Akt. | Held/Begl./Schutt/Klein/Bewuchs/Kontakt | Wasser, Effekte | Stempel |
|---|---|---|---|---|---|---|
| 01 Pingo | 3 598 | 106 | 8 | 1/7/119/474/2 549/423 | Kratersee smaragd; 3 Decals | 4,6 m |
| 02 Wanderer | 1 890 | 46 | 8 | 1/10/59/700/775/319 | 4 Decals | 0,8 m |
| 03 Eiswand | 2 345 | 151 | 51 | 20/31/133/673/1 210/299 | Rinnsal (versickert), Nebel, 9 Decals | 11,3 m |
| 04 Fließtreppe | 4 204 | 65 | 6 | 1/155/290/1 150/2 045/562 | Schmelzfaden über die Stirnen; 2 Decals | 1,7 m |
| 05 Trunkener Grund | 2 106 | 96 | 31 | 20/11/23/1 220/390/400 | See moorbraun + Abfluss, Nebel, 4 Decals | 4,1 m |
| 06 Schneetälchen | 3 544 | 32 | 6 | Altschnee (Blutschnee)/Wehen/Protalus-Wall/Moos/Zwergweiden/Kiessaum | Schmelzwassertümpel + Abfluss; 4 Decals | 1,8 m |
| 07 Steinringe | 2 615 | 62 | 4 | 178/4/490/744/757/446 | 6 Decals | 5,9 m |
| 08 Wabenmoor | 4 123 | 59 | 2 | 4/2/60/1 560/1 936/560 | 7 Tümpel; 6 Decals | 3,7 m |

Verdeckung (Wege + Pfade ≤ 400 m, Kern + 4 Proben): Trunkener Grund, Schneetälchen, **Steinringe** (heute 29–35 Wegpunkte)
und **Wabenmoor** (heute bis 21) sind mit Plan **vollständig verdeckt** – Steinringe durch Terrasse −1,5 m, alten
Strandwall +3,8 m (W–N–O) und Eisschubwall +2,4 m (seewärts, Lücke SSO zum Strand); Wabenmoor durch Uferwall/Levee
mit Weidengebüsch West und Ost (+1,5/+2,4 m) und Böschungssaum Nord.

Materialwünsche (6): `MI_EL_SW_Grundeis`, `_Blutschnee`, `_Landkartenflechte`, `_Flechte_Decal`, `_Altschnee`, `_Torf`.

## Grenzen und offene Punkte

- Eiswand: Kopfwand aus Ice-Cliff-Schalen, Schauseite als `+y` angenommen – Prüfbild `_held` entscheidet. Durchbruch
  durch den Küstenwall senkt bis 11,3 m (Abfluss des Kessels zum Strand). Senken im Kessel = gewollte Setzungsmulden.
- tundra_06: **Aufeis gestrichen** (lag auf der gebauten Erlenbach-Kaskade C2, Auftrag 14; kein anderer glaubwürdiger Schluchtort)
  → *Das Schneetälchen* (X −182 / Y −1962) am Schneefeldrand; `tundra_pfad_das_aufeis` entfällt.
- Wollgras fehlt im Bestand → weiße Windröschen ×0,4 zwischen Binsen. Brandung fehlt (Wind-Cue).
- `senke_begruendung` an Pingo (Kratersee), Eiswand, Trunkener Grund, Steinringe (Strandwall-Swale), Wabenmoor (Polygonmitten).
- **E19:** `tundra_pfad_der_trunkene_grund` streift den 150-m-Puffer von ROMAN_LOC_018 (nicht die Stadtfläche) – Feld
  `warnung_akzeptiert` in `standorte.json`, der Prüfer meldet es als HINWEIS. Nach dem Bau der Stadt prüfen, ob der
  Pfadanfang ein Gebäude schneidet (sonst Start 30–40 m nach Westen).
- **E34:** Die Ice-Cliff-Schalen der Eiswand behalten `M_MS_Base_Trm`; `orte.json` listet sie unter `material_fix_ausnahmen`.
- **E20/E21:** Katalogfragen 1–3 entschieden (Aufeis entfällt, Thermokarstsee bleibt, Steinringe Fundstück, 4/4).
