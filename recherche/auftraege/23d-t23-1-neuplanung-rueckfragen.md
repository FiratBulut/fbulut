# Auftrag 23d – T23-1 (C2) gerechnet, Neuplanung DETA/P2BE, Weltzählung 23.3, weiße Steine gelöst, Rückfragen

Stand 19.10.2026, 00:30 PC-Uhr. Bezug: Antworten 23 (264a4d8), 23b (4211d1b), 23c (05012d3). Alles offline gerechnet (Rolle 1), außer wo
„Editor“ steht. Regeldatei eingefroren als Stand `regeln_23c_cda6ceb0` (SHA cda6ceb0…). Selbsttests: 23 `64a654746495eca8`, 23b `dabb50741db8b9ac`,
23c `b4ebdb213b2f71ba` – je mehrfach, auch mit der eingefrorenen Datei.

## 1. Erledigt im Editor

- **Weiße Steine (23b §5): Ursache war NICHT skjsL/texndcpda** (beide haben Texturen gebunden, 4K, Brightness 1,0), sondern
  `xjijbgx_tier_0` (Nordic_Forest_Rock_Small, Fab-Raw, MI ohne Textur = T_DefaultColor). Gleich: `pjtsT`, `xf3odif`/`xfplcbf` an Halden-/Quellen-Typen,
  Tundra-Gras `wk2oaeyqx` (MI auf dem Fels-Master M_MS_Base). Repariert wie entschieden („Material reparieren, Steine behalten“): Overrides an 40 eigenen
  Foliage-Typen (vorhandene `MI_EL_Klippe_<id>`, neu `MI_EL_Klippe_pjtsT`, `MI_EL_Fab_wk2oaeyqx` auf M_MS_Foliage). Nach Neustart: xjijbgx 427 ok / 0 weiß
  (vorher 220 weiß), Gras alle ok, Halme maskiert. Bilder `bilder/platzierung/lage4/weiss_material_vorher_nachher.jpg`.
- **Bach (6o/6p):** T6N1 mit Breite 1 alle Tore bestanden, nur Kolk 25 +10 cm gegen den Vorlauf → nicht gespeichert (Nachtrag 6p).

## 2. T23-1 Trockenlauf C2 (Stufe A, Wasser-Klassen nicht beurteilt, weil W erst nach T6N1)

| Bereich | Instanzen | FEHLER | WARNUNG |
|---|---|---|---|
| C2 gesamt | 41 757 | 21 496 | 2 668 |
| Talkaskade s 389–580 (+10 m) | 7 884 | 6 935 | – |

Schichten > 30 % FEHLER (§10.3 → neu planen): DETA fels/kiesel/kleinschutt/platte/stein (80–100 %), P2BE fels/kiesel/platte/stein/totholz_stamm.
Häufigste Fehler im Fenster: winkel 5 636 (zufällig gedrehte Kiesel), durchdringung 3 125 (Haufen > 35 % der Dicke), lücke 1 469, kante 1 313.
Alle 8 Kreise aus Ferats Bild haben gemeldete Instanzen. 23.3 in C2: netz_anteil 410, einheitsgroesse 54, ce_gleichmaessig 22, Ringe 0 FEHLER / 61 Bögen.

## 3. Neuplanung DETA/P2BE in C2 mit Reparaturfolge 23/23b/23c (nur Datensätze, nichts gesetzt)

| Klasse | alt | behalten (am Ort/versetzt/ersetzt) | + Ersatz | Hindernis offen | weggelassen |
|---|---|---|---|---|---|
| DETA fels | 310 | 147 | – | 74 | 89 |
| DETA kiesel | 4 023 | 3 011 | 2 182 | – | 1 012 |
| DETA kleinschutt | 1 172 | 73 | – | – | 1 099 |
| DETA platte | 182 | 36 | – | 90 | 56 |
| DETA stein | 1 294 | 608 | 83 | 470 | 216 |
| P2BE fels / kiesel / platte / stein / totholz | 91 / 331 / 8 / 210 / 5 | 31 / 310 / 3 / 96 / 0 | – | 54 / – / 5 / 113 / – | 6 / 21 / 0 / 1 / 5 |

**Dichte im Uferband der Talkaskade:** Grundriss 1 421 → 840 m² (**−41 %**), Instanzen 6 189 → 5 549, Steine je 10 m 63 → 56. Das Dichteziel aus
Antwort 20 (Felsdeckung 130–139 %) ist mit den Sitzregeln so nicht zu halten.

## 4. Weltzählung 23.3 (70 Felder, unkalibriert: keine Lagenmaske, keine Lagen-Albedo, keine Gruppen-ID)

35 284 Fenster×Schicht, 9 455 mit FEHLER (netz_anteil 16 820, einheitsgroesse 3 335, ce_gleichmaessig 816, l_gleichmaessig 63, totholz_laengen 42,
ring 21, reihe 9). Neuplanungsliste 189 Feld×Schicht, davon 170 „Misch-Kürzel“ (Herkunft nicht eindeutig) und 19 echte: WUES E3/E4/D3/C4/D4, KLIP B5,
HOCH D2/F2, WIT C5/C6, FELS D5/F4, SPUR A5/G4, SWBE B5/C5, FS A4/E1, BACH H4. Eiszapfen 5 595, davon offline 25 frei schwebend (E2: 8); Rest braucht
Editor-Traces. Fremdgestein über Biomkarte genähert: 606.

## 5. Rückfragen

1. **Dichteverlust −41 % im Uferband:** Planer mit Sitzregeln neu rechnen, bis die Deckung wieder stimmt (andere Netze, mehr flache Teile, Lagen
   statt Netze)? Oder die fehlende Deckung als Kies-/Geröll-Lage malen? Ein Vorschlag mit 1 155 Grundrissen liegt lokal.
2. **Ring in C6 (Bild L4R_C6_L4_34):** Von oben ist es eine Schlackengruppe (Ellipse 5,8 × 2,8 m, Mitte nicht leer, Kreis-Fit RMS 0,75 m), kein Ring;
   rund wirkt sie nur schräg. Euer Abbruchkriterium für den Ringtest trifft damit formal zu. Wie weiter: Ringprüfung anpassen oder Gruppe trotzdem auflockern?
3. **Misch-Kürzel (170 von 189):** Instanzen, deren Planer nicht eindeutig ist (gleiche Netze in mehreren Kürzeln). Nach Fenstern statt Schichten neu planen?
4. **Gruppenkohärenz ohne Gruppen-ID:** Zuordnung über Nachbarschaft (entfernt 212 Kiesel in C2) – zulässig?
5. **T23-0-Messweg (Rolle 1):** R1 Stufe B (Punktwolke) im Messweg nötig? R2 Träger als gedrehte Box bestätigen? R3 Dreiecksmodell statt bilinear
   bestätigen (Unreal-Landschaft ist in Dreiecke zerlegt, bilinear weicht bis 20 cm ab)? R4 e_hoehe mit H statt T?
6. **T23b-S Nicht-Nanite:** Einen grauen Stein 0,3–1 m ohne Nanite gibt es im Projekt nicht sicher (Kandidaten SM_stone_09 laut einer Prüfung bzw.
   SM_lava_m_rock_08 1,8 m laut Inventar). Reicht ein großer Lava-Block für den Test?
