# sehens_canyon – Sehenswürdigkeiten-Planer Canyon (Auftrag 13, Phase 2)

Baut die 8 Canyon-Orte aus `antworten/sehens/canyon/standorte.json` nach `sehens_canyon_regeln.json` (Katalog
`sehens/canyon/katalog.md`, `asset_bedarf.json` inkl. `abgleich_13d`, Inventar 13d) im Lieferformat
`vorlagen/SEHENS_FORMAT.md`. Muster: [`../sehens_bergwald/`](../sehens_bergwald/), Schema: [`../sehens_lib/PLANER_ANLEITUNG.md`](../sehens_lib/PLANER_ANLEITUNG.md).

```
python -I recherche/antworten/skripte/sehens_canyon/sehens_canyon.py --daten2m recherche/vorlagen/daten/sehens \
       --aus <Ordner> [--ort ID ...] [--bild --bild-ordner recherche/antworten/sehens/canyon] [--ohne-sicht]
python -I sehens_canyon.py --basis <production>      # lokal: 1 m aus export/unreal/welt, Ausgabe dort
```

Eigener Code: Hook `daemme` (Wälle/Gräben mit `stempel.damm`, Regel `gelaende.daemme`) und die Verdeckungsprüfung aller
Fundstücke mit `sehens_lib.verdeckung` (Gelände nach Stempel + geplante Felsen, Wege inkl. aller Pfade; Regel `verdeckung`
legt Kern/Proben fest). Alles andere steht in den Regeln.

## Testlauf 2 m (11.10.2026, ~56 s, zwei Läufe byteidentisch)

Planer 0 FEHLER / 0 WARNUNG; Prüfer (`orte.json` + `sw_canyon`) **0 FEHLER, 0 WARNUNG**, 6 HINWEIS (eigenes Decal optional,
Beschreibung in `fuer`).

| Ort | Inst. | Koll. | Akteure | Stempel | Held / Besonderheit |
|---|---|---|---|---|---|
| 01 Sonnenfenster | 2 511 | 185 | 11 | 1,5 m | Bogen: 2 Pfeiler `vjqiaa2qx` (Formation Layered) + Sturz `vceoferfa` (Cliff Layered XL 03, Unterkante 6,5 m), Finne `vb1mbdega` |
| 02 Wäger | 1 457 | 72 | 9 | 2,6 m | Sockel `ulbwebv` (Spire Large 05, schmal), Kopf `SM_RockSandstone_040` (Deckstein), gefallener Bruder + Schleifspur |
| 03 Rote Stufe | 4 687 | 272 | 29 | 5,5 m | 3 Etagen Desert Western Cliff/Formation Layered entlang der Stufe, Simskanten `vbvqbbofa`, Überhang, 3 Kegel |
| 04 Flüsterschlucht | 1 779 | 96 | 26 | 13,6 m | Kerbe bis −17 m entlang des Bachs (ist_wasser), Wände `venuafk` beidseitig (gekippt), Klemmblöcke, Bach + 25-m-Fall, NS_Waterfall_Small/Impact_Small/Stream_Small |
| 05 Hoodoo-Kessel | 2 668 | 145 | 42 | 18,1 m | Kessel bis 13 m unter den Rand (absolute Sohle, Canyonboden unberührt), 12 Hoodoos aus Spires + 3 Riesen `vh3oagiga`, Decksteine |
| 06 Kolke | 1 580 | 63 | 14 | 1,6 m | 6 Kolke (`see`, klar) auf Slickrock (Desert Ground Patches), Rinnen, Binsenkranz, Nassband |
| 07 Smaragdgumpe | 1 215 | 78 | 14 | 8,0 m | Alkoven −5 m + Riegel +8 m, Gumpe `smaragd` + Abfluss + Fadenfall 31 m, NS_Waterfall_Medium/Impact_Medium/Stream_Small, hängender Garten |
| 08 Welle | 1 190 | 65 | 2 | 10,2 m | Mulde (absolute Sohle) mit Abfluss SW, Platten aus Desert Ground/Slate Patches, Schichtwand `vb1mbdega`, eigenes Decal `decal_welle.png` |

Je Feld: C4 4 690, D4 12 397 Instanzen. Verdeckung (Fundstücke 04–08): alle **verdeckt** (0 Wegpunkte mit Sicht > 15 %),
04 und 08 erst mit dem Stempel (heute sichtbar). Materialwünsche 5/6: `Canyon_Rotband`, `_Gumpenmoos`, `_Sandfuss`,
`_Deckstein` (nur Bestands-Sandstein; Desert-Western-Netze behalten ihre Fab-Materialien) und `Welle_Streifen`
(M_MS_Decal + `antworten/sehens/canyon/decal_welle.png`/`_n.png`, prozedural).

## Grenzen und offene Punkte

- **E25:** Canyonsteig nur Reserve (Katalogvermerk); ersetzt einen Ort am Mündungsfall, falls einer im Editorbild durchfällt.
  **E33:** uldubik/uk5ebcp werden neu geladen; bis 5/5 Dateien da sind, bleiben die Ersatznetze (Sperre in `inventar.py`).

- Pivot/Schauseite der Desert-Western-Netze unbekannt (`netze_masse.json` hat sie nicht): Pivot unten Mitte, `front_achse +y`
  angenommen – Editorbild prüfen (besonders Bogen 01, Spaltwände 04, Alkoven 07).
- Gewollte Hohlformen (Spalt-Kolk 04, Kesselkolke 05, Tinajas 06, Alkovenkolke 07, Simsmulden 03) tragen `senke_begruendung`.
- `uldubik_tier_0`/`uk5ebcp_tier_0` (13d unvollständig) werden nicht gesetzt (Lib meldet sie jetzt als FEHLER).
- Hollowstone Canyon (Kauf offen) und Wadi Rum/Procedural Rocks stehen weiter in `assets_wunsch`.
- **13f:** `ranken` mit `z_frei` (A6). canyon_07: der Abfluss der Gumpe folgt der geplanten `abflusslinie` und versickert
  nach ~30 m vor der Weg-Schutzzone (vorher lief der steilste Abstieg in den Alkoven zurück und versickerte nach 12 m).
