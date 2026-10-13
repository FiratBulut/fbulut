# 16h Nachtrag – Materialtest Talkaskade: Wasserwerte ändern fast nichts, das Bodenmaterial legt hellen Kies unters Wasser

Stand 13.10.2026, 11:15. Bezug: `16h-erlenbach-p2-talkaskade-ufer-wasser.md` §3 (Befund B).

## 1. Test (nur Speicher, gleiche 4 Kameras, Bilder `bilder/swr_p2/wv_varianten.jpg`)

| Variante | Absorption (Sichtweite cm) | Scattering (Farbe × Stärke) | Foam Opacity | Water Roughness | Sim Velocity Normal Strength |
|---|---|---|---|---|---|
| A (bis heute) | 400 / 900 / 750 | (0,2; 0,3; 0,28) × 0,1 | 0,5 | 0,02 | 40 |
| B (16a) | 250 / 1430 / 2000 | (0,6; 0,8; 1,0) × 0,12 | 0,5 | 0,02 | 40 |
| C (16f umgerechnet) | 222 / 1000 / 1250 | (0,5; 1; 1) × 0,02 | 0,5 | 0,02 | 40 |
| D | wie C | wie C | **0** | 0,02 | 40 |
| E (16f §5.2 vollständig) | wie C | wie C | 0,5 | **0,04** | **15** |

**Ergebnis:**
- Bei 0,4–0,6 m Tiefe sehen A, B und C fast gleich aus. Absorption und Streuung sind hier nicht der Hebel.
- D: Die hellen Flecken bleiben. Es sind die Steine im Bett, verzerrt durch die Wellen, kein Schaum.
- E: etwas ruhiger, sonst kaum anders.
- **Gesetzt und gespeichert (11:14): Variante F = E mit Foam Opacity 0.** Begründung: Ferat wollte am 12.10. keinen Schaum in den Bächen,
  und `FoamAtten` fehlt in unserem Master. Rückweg: Variante A0.

## 2. Ursache des hellen, sandigen Betts: das Landschaftsmaterial

Im Landschaftsmaterial (V12 bis V17) gibt es seit dem 05.10. die Funktion **„Ufer und Gewässergrund“** (Zielbild K2: helle Kiesufer). Sie liest
die Wasserspiegel-Karte `T_Eldarien_Wasserspiegel_2m` (Tiefe = Spiegel − Gelände):
- **Bett:** Ab 5 cm Tiefe (voll ab 15 cm) wird der Grund durch die Kies-Textur ersetzt, × `Ufer_Farbe` (0,95; 0,93; 0,88).
- **Uferband:** Von 30 cm unter bis 60 cm über dem Spiegel ebenfalls Kies, nur auf flachem Gelände (Normal-Z > 0,86), fleckig (Rauschen 17 m).
- **Stärke:** `Ufer_Staerke` 0,85.
- **Nässe:** `Nass_Abdunkeln` (V17-Instanz 0,55), `Nass_Breite_cm` 150, `Nass_Staerke` 2,5, `Nass_Spiegel` 1. Unter Wasser voll, also Farbe × 0,55
  und Rauheit 0,35.

Die Wasserspiegel-Karte kennt den p2-Bach erst seit heute 10:47 (Alt-Wasser-Reinigung). Seitdem malt das Material unter den ganzen Bach hellen
Kies. Vorher lag dort laut Lagen ohnehin Kies/Geröll (Bachdekor). Beides ergibt einen hellen, beigen Grund. Unter klarem Wasser und warmem Licht
wirkt er goldbraun und sandig.

Die Parameter gelten **weltweit** (eine Instanz `MI_Eldarien_Landschaft_V12` für alle Gewässer).

**Frage B2:**
1. Welche Werte für Witcher-Bachbetten: dunkler, nasse Steine, gemischte Körnung?
2. Weltweit ändern, oder brauchen Bäche eine eigene Steuerung? Ein Weg wäre ein zweiter Kanal in der Spiegel-Textur, z. B. „Bach“ gegen „Fluss/See“.
3. Soll die Kies-Ersetzung unter Wasser die Bachdekor-Lagen (Kies 41, Geröll 33, Schlamm 8, Fels 7) überhaupt übermalen?

## 3. Nebenbefunde

- **Alte Flussfelsen:** 16 `C2_Flussfels_*` (große Blöcke des alten 30-m-Flusses) stehen noch am alten Lauf. Zwei davon liegen im p2-Bett
  (`_006` 1,9 m, `_002` 2,4 m von der Mitte). Sie fehlen in den SWR-Hindernissen, das Wasser läuft durch sie hindurch.
- Die Klänge `C2_Ton_Fluss_01/02/05` liegen zufällig auf dem neuen Bach (0,3–2,3 m). Ihre Lautstärke ist für einen 30-m-Fluss ausgelegt.
