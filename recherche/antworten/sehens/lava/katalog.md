# Lava – 8 Sehenswürdigkeiten (Auftrag 13, Phase 1, Biom-Agent B7)

Stand 11.10.2026 · Daten: `vorlagen/daten/sehens` (2 m) · Werkzeuge: `antworten/skripte/sehens_lib` · Dateien in diesem Ordner:
`standorte.json` (5 Orte, Prüfer 0 FEHLER), `standorte_kratersteig.json` (3 Orte + Pfadvorschlag), `asset_bedarf.json`, `<id>.png` je Ort.

## Das Wichtigste vorweg: Der Vulkan hat keinen Weg

Das Lava-Biom (2,37 km², Felder C5/C6/C7, Rand B6/B7/D6/D7) ist zu zwei Dritteln **der Vulkan**: Kegel bis 381 m, Gipfelkrater
(Boden 344–351 m, Rand 365–377 m), eine Kraterreihe am Nordostfuß, ein Westplateau aus Asche mit einem jungen Strom bis zur Küste.
**Auf keinem dieser Teile liegt ein Weg.** Wege gibt es nur im Norden (Zalas verborgene Stadt, Archivpfad, Weg bei „Labor drei“).

| Abstand zum nächsten Weg | Fläche im Biom |
|---|---|
| ≤ 300 m | 0,33 km² |
| ≤ 400 m (Prüfer: > 400 m = FEHLER) | 0,46 km² |
| ≤ 800 m | 1,02 km² |
| größter Abstand | 1 793 m |

In der regelkonformen Zone (60–400 m vom Weg, ≥ 150 m von Zalas Stadt/Archiv, im Biom) passen bei ≥ 350 m Abstand **höchstens 5 Orte**
(3 000 zufällige Greedy-Packungen, keine mit 6). Diese Zone ist die alte Mooslava-Ebene nördlich des Vulkans – kein Wald: im ganzen
Biom stehen nur 292 Baumzellen (4 m), das dunkle Muster in den Karten ist Moos/Lavafels-Netz.

**Lösung (Ferat entscheidet):**
- **5 Orte heute regelkonform** in `standorte.json` (lava_01–05): Prüfer **0 FEHLER**; 2 WARNUNGEN „Abstand zum Weg 324 / 393 m“
  (lava_01, lava_02 – anders nicht packbar) und „5 Orte (Soll 8)“.
- **3 Orte am Vulkan** in `standorte_kratersteig.json` (lava_06–08): gelten nur, wenn der vorgeschlagene **Kratersteig** als Weg
  gebaut wird (Start am Ende des Archivpfads, X −2366 / Y 884 m). Gegen Wege + Steig gerechnet erfüllen sie alle Regeln (Abstand
  107–148 m, Sicht, Erreichbarkeit ≤ 25°). Gegen die heutigen Wege meldet der Prüfer je 1 FEHLER (661–936 m) – deshalb liegen sie
  bewusst nicht in `standorte.json`.

| Kratersteig | Länge | max. Steigung | mittel | Verlauf |
|---|---|---|---|---|
| Ast Ost | 624 m | 22,1° | 4,8° | Archivpfad → Südrand des Blockstroms (≥ 100 m an lava_01 vorbei) → Fuß der Kraterreihe |
| Ast West | 898 m | 11,0° | 3,5° | Archivpfad → Mooslava → Westplateau → oberhalb der Schlucht → junger Strom |

Breite 1,5 m, Bodenlage Kies/Erde als Band, auf Lavafels Trittsteine. Der Steig hält ≥ 90 m Abstand zu allen 8 Ortsmitten
(lava_01–05 bleiben also auch mit Steig regelkonform). Wird er nicht gebaut, bleibt das Biom bei 5 Orten.

## Übersicht

| ID | Name | Art | Form | Feld | X / Y (m) | Weg | Status |
|---|---|---|---|---|---|---|---|
| lava_01_schwarze_mauer | Die Schwarze Mauer | Leuchtfeuer | erkaltete Stromkante + Schlotturm (Hornito) | C6 | −2084 / 1045 | 324 m | regelkonform (WARNUNG Weg) |
| lava_02_schwefelgrund | Schwefelgrund | Leuchtfeuer | Fumarolenfeld mit Schwefelquellen | C6 | −2394 / 1276 | 393 m | regelkonform (WARNUNG Weg) |
| lava_03_kraterkinder | Die Kraterkinder | Leuchtfeuer | Pseudokrater mit Kraterteichen | C5 | −2140 / 690 | 291 m | regelkonform |
| lava_04_roehrenfenster | Das Röhrenfenster | Fundstück | eingestürzte Lavaröhre mit Farnoase | C5 | −1792 / 780 | 286 m | regelkonform |
| lava_05_klare_spalte | Die Klare Spalte | Fundstück | Gjá – offene Riftspalte mit Grundwasser | C6 | −2604 / 982 | 242 m | regelkonform |
| lava_06_kraterreihe | Die Kraterreihe | Leuchtfeuer | Schlackenkegel auf einer Eruptionsspalte | C6 | −1790 / 1345 | 148 m (Steig) | nur mit Kratersteig |
| lava_07_basaltorgel | Die Basaltorgel | Fundstück | Basaltsäulenwand in einer Schlucht | B6 | −2795 / 1390 | 107 m (Steig) | nur mit Kratersteig |
| lava_08_glutauge | Das Glutauge | Fundstück | Glutfenster in junger Stricklava | B6 | −2745 / 1740 | 118 m (Steig) | nur mit Kratersteig |

Mischung: alle 8 → 4 Leuchtfeuer / 4 Fundstücke. Im offenen, baumlosen Biom sind positive Formen (Wand, Kegel, Dampf) zwangsläufig
von weitem sichtbar; alle Fundstücke sind deshalb **Hohlformen** (Grube, Spalte, Schlucht), die man erst an der Kante sieht.
Eine Zeitreihe erzählt das Biom: alter, bemooster Strom (01, 04, 05) → Nachwirkung (02) → junger Vulkan (06, 07, 08).

**Abgrenzung zu anderen Biomen:** Alle Formen sind vulkanisch (Lavastrom, Röhre, Rift, Schlacke, Fumarolen, Säulenbasalt, Glut).
Bewusst nicht übernommen: Geysir/warme Quelle (gletscher/tundra), Schlammvulkane/Schlammtöpfe (oedland/sumpf), Höllentor-Gaskrater
(oedland), Regenbogenhang (Dopplung mit oedland: Bemalte Hügel), Säulenhöhle am Meer (kueste: Grotte), Basalt-Blockufer (fjord).
Andere `katalog.md` lagen beim Schreiben noch nicht vor; geprüft gegen Katalog v1 und Download-Liste. Nächster fremder Ort:
aue_03_schwalbenwand, 608 m von lava_03.

**Sichtmessung:** `sicht.py`, Wegpunkte alle 20 m, Gelände + `baumhoehe_4m`. Leuchtfeuer: Wegpunkte im Ring 300–800 m, die ≥ 30 %
der Silhouette sehen. Fundstück: (a) heute, Silhouette über Flur; (b) **Einblick in die Hohlform** (Grund bis Flur) mit dem
geplanten Stempel von allen Wegpunkten ≤ 400 m – maßgeblich, weil das Fundstück unter der Flur liegt. Kameras nach SEHENS_FORMAT
§8 (Stand 13:00): `_anmarsch`/`_nah` Hoch −170 mit echtem Ziel, `_held` teils −170, `_fern` +170.

---

## lava_01_schwarze_mauer – Die Schwarze Mauer (Leuchtfeuer)

**Was man sieht:** Aus dem grünen Moospolster steigt unvermittelt eine schwarze Wand aus Blocklava, 6–9 m hoch, 140 m lang, in
Wellen vor- und zurückspringend – die erstarrte Stirn eines alten Stroms, der hier stehen blieb. Auf einem Vorsprung der Front ragt
ein 10 m hoher, zerfranster **Schlotturm** (Hornito) wie ein Finger auf; daneben ein kleinerer Zwilling. Vor der Wand ein Saum aus
abgebrochenen Blöcken, in den Fugen kriecht graugrünes Zackenmützenmoos hoch. Am Fuß steht ein toter, silbergrauer Baum, den der
Strom einst umflossen hat.
**Vorbild:** Stromfronten von Eldhraun und Holuhraun (Island), Hornitos am Kīlauea; Spiel: Mt. Gelmir (Elden Ring) als dunkle
Lavaküste, Hellblade II (Island-Fotogrammetrie) für Moos auf Lava.
**Standort:** C6, X −2084 / Y 1045 m, Boden 47,3 m. Westfront des alten Blockstroms (Lavafels 47 %, Moos 41 %): Profil y = 1010:
41,0 → 49,7 m (Stufe 8,7 m), y = 1040: 6,1 m, y = 1050: 5,3 m; Hang an der Front bis 45°. Weg 324 m (Archivpfad), Zalas Archiv
258 m, Biominneres 394 m. Näher an den Weg geht nicht: lava_03 (359 m) und lava_02 (387 m) begrenzen.
**Sicht:** 37 von 52 Wegpunkten im Ring 300–800 m sehen ≥ 30 % (Zielhöhe 16 m = Front + Schlotturm), mittlerer Anteil 0,57,
lesbar bis 785 m; bester Fernblick vom Pfad unterhalb Zalas Stadt (X −2506 / Y 624, 596 m, Anteil 1,0).
**Komposition und Anmarsch:** Vom Archivpfad sieht man die Wand als dunklen Strich über dem Moos, der Schlotturm bricht die Linie.
Zugang 351 m ohne Pfadbau (max. 20,2°, Mittel 4,9°). `_held` 33 m westlich im Moos, Blick nach Osten: Vordergrund Moospolster und
Blockschutt, Mitte Wand, Schlotturm als Blickziel gegen den Himmel, rechts dahinter die Vulkanflanke.
**Detail-Ebenen:** Held 1 – Schlotturm `SM_IcelandicLavaSpire_01` × 1,8 (≈ 9,6 m) + `SM_IcelandicLavaSpire_03` × 1,3 als Zwilling,
30 % eingegraben. Begleiter 6–8 – Wandschollen `SM_lava_wall_01/02/03/09` (6–7 m) schräg in der Front, `SM_lava_b_rock_01/02`
(4–5 m) als abgesackte Blöcke. Schutt 120–180 – `SM_lava_m_rock_01…08`, `SM_lava_s_rock_01…05` als Schuttsaum 8–15 m vor der
Front (Ursache: Abbrechen der Stirn), grobe Blöcke unten, feine oben. Kleinzeug Hunderte – `SM_lava_s_rock_06/07/08`,
`SM_SmallStonesPack_08…14`. Bewuchs nach Ursache – Moospolster (`SM_moss_01/02`, `SM_MossClump_01/03/05`, Lage Moos) vor der Front
und auf schattigen Blockoberseiten (`MI_EL_SW_Lava_Moos`), Pioniere in Spalten der Krone (`SM_dwarf_pine_small_01/02`,
`SM_wk2oaeyqx_VarB/C`), toter Baum `Fir_08_Dead_NoBillboard` am Fuß (Natur erzählt: vom Strom eingeschlossen), trockene Zweige
`SM_DryBranches_04/07`. Kontaktzone – Blöcke 30–45 % eingegraben, Moos kriecht an der Wand bis 1,5 m hoch, Kiesrand im Schuttsaum.
**Wasser, Effekte, Licht:** kein Wasser, keine Glut (kalter, alter Strom). Westseitige Wand im Licht, Schlagschatten der Blöcke.
**Geländeänderung:** Rücken +3 m entlang der Front (Band 10 m, Rand 7 m) → Wand 8–12 m; Fenster ca. 200 × 220 m.
**Assets:** Bestand wie oben (alle in `netze.csv`). Wunsch: „Tundra Icelandic Rock Cluster“ (neu, C) für bemooste Kontaktblöcke;
Ersatz `SM_lava_m_rock_*` + `MI_EL_SW_Lava_Moos`.
**Aufwand und Risiko:** mittel. Risiko: Texel-Dichte des 1,8-fach skalierten Lava-Spire; Gefahr „Mauer wie Bauwerk“ → Front in
Lappen und Rinnen brechen, nie gerade.
Budget (Richtwert): ~7 000 Instanzen (900 Kollision), 30 Akteure, 0 Lichter, 0 Niagara, 3 Decals.

## lava_02_schwefelgrund – Schwefelgrund (Leuchtfeuer)

**Was man sieht:** Am Fuß des Vulkans liegt eine flache Mulde, in der der Boden ocker, schwefelgelb und gebleicht ist. Aus zwei
Rissen (NO–SW, parallel zur Kraterreihe) zischen 6–9 Fumarolen; ein 3 m hoher, gelb verkrusteter **Dampfschlot** schickt eine
weiße Säule 20–30 m hoch. Zwei milchig-türkise **Schwefelquellen** dampfen in kleinen Becken mit gelbem Rand. Um die Mulde ein
toter Saum: gebleichte Halme, kein Moos.
**Vorbild:** Hverir/Námaskarð am Fuß des Námafjall (Island), Solfatara (Pozzuoli); Spiel: Fumarolen und Schwefelquellen in
Eastmarch (Skyrim), Farbigkeit wie DA:I.
**Standort:** C6, X −2394 / Y 1276 m, Boden 49,7 m. Nordfuß des Vulkans, flache Hangmulde (TPI100 −2,55 m, Hang 15°), Moos 51 %,
Wiese 24 %, Lavafels-Rippen 24 %. Weg 393 m (WARNUNG, Zone ≤ 400 m; weiter nach Norden ginge nur auf Kosten von lava_01/05),
Archiv 334 m, Wasser 573 m (Quellen bekommen eigenes Becken).
**Sicht:** 22 von 22 Wegpunkten im Ring sehen ≥ 30 % der 25-m-Dampfsäule, mittlerer Anteil 0,64, bis 798 m; `_fern` vom Weg
unter Zalas Stadt (X −2496 / Y 490, 793 m).
**Komposition und Anmarsch:** Vom Archivpfad steht die Dampfsäule vor der dunklen Vulkanflanke – das zieht. Zugang 405 m ohne
Pfadbau (max. 19,8°). `_held` 70 m südlich hangauf, Blick nach Norden über das gelbe Feld, Dampf vor der grünen Mooslava-Ebene.
**Detail-Ebenen:** Held – Dampfschlot (Hügel +2,8 m mit Krater, Krone aus `SM_lava_b_rock_04` + `SM_lava_m_rock_05` mit
`MI_EL_SW_Schwefelkruste`). Begleiter 6–9 – Fumarolen-Mündungen aus `SM_lava_m_rock_01/02/07` als Steinringe, zwei Quellbecken.
Schutt 60–100 – gebleichte, verkrustete `SM_lava_s_rock_01…05` an den Rissen. Kleinzeug – `SM_SmallStonesPack_*`,
`SM_dead_grass_01…03`. Bewuchs nach Ursache – im Kern nichts (Hitze, Säure), Ring tote Halme, außen Moos/Wiese wie heute.
Kontaktzone – Decals Schwefel gelb (`MI_EL_SW_Schwefel_Decal`), Ocker/Weiß, Nassränder `MI_Leakage_*` an den Quellen.
**Wasser:** 2 `see` (Quelltöpfe), `farbe` thermal, Ø 7 m und 10 m, 0,6 m tief, Ufer mit Kiesring und gelbem Rand.
**Effekte, Licht:** Niagara Dampfsäule + 6–9 kleine Fahnen (optional, Lava & Volcano Set / Niagara Examples), `lokaler_nebel` 2× in
der Mulde (Dichte 0,08, weiß-gelblich). Keine Glut. Dampf trägt auch bei fester Sonne.
**Geländeänderung:** Mulde −1,6 m (42 × 30 m, Rand weich), Schlothügel +2,8 m; Lagen Lehm, Erde, Kies. Fenster 150 × 150 m.
Keine abflusslose Senke: die tiefste Stelle füllt das Quellbecken.
**Assets:** Bestand wie oben; Pakete Lava & Volcano (A, schon gekauft – Dampf/Rauch-Niagara), Niagara Examples (A),
Fantasy Ambiences (B, Zischen). Ersatz ohne Download: 2 Nebelvolumen + Decals.
**Aufwand und Risiko:** mittel. Risiko: ohne Niagara fehlt die Fernwirkung (dann kein echtes Leuchtfeuer) → Download A nötig.
Budget: ~4 000 Instanzen (300 Kollision), 20 Akteure, 0 Lichter, 3 Niagara, 2 Nebel, 10 Decals.

## lava_03_kraterkinder – Die Kraterkinder (Leuchtfeuer)

**Was man sieht:** In einer schwarzen Aschensenke am Rand der grünen Aue sitzen fünf kleine, runde Kegel wie Kinder um ein Feuer,
3,5–7,5 m hoch, jeder mit einem Krater oben; in den zwei größten steht schwarzes, spiegelndes Wasser. Ihre Flanken sind von Moos
und Gras überwachsen, die Kraterränder schwarz-rot. Aus dem großen Kraterteich sickert ein Rinnsal nach Norden zum Bach.
**Vorbild:** Pseudokrater von Skútustaðir am Mývatn (Lava floss über nassen Grund, Dampfexplosionen); Spiel: Hellblade II
(isländische Kraterlandschaften).
**Standort:** C5, X −2140 / Y 690 m, Boden 18,2 m. Geschlossene Lavasand-Senke (Lavasand 97 %, Senkentiefe 3,9 m, Einzugsfläche
0,36 km²), Ränder 22–26 m, Boden 16–18 m; Bach der Aue 130 m nördlich – genau die Lage, in der Pseudokrater entstehen (Lava auf
nassem Grund). Weg 291 m (Weg bei „Labor drei“), Zalas Stadt 210 m, Biominneres 40 m.
**Sicht:** 26 von 130 Wegpunkten im Ring sehen ≥ 30 % der Kegelgruppe (Zielhöhe 8 m), bis 772 m; bester Blick vom Pfad unter Zalas
Stadt (375 m, Anteil 0,8). Ein bescheidenes Leuchtfeuer: Hügelgruppe mit Dellen am Horizont, nicht hoch.
**Komposition und Anmarsch:** Zugang 293 m ohne Pfadbau (max. 14,6°). `_held` vom Südrand der Senke (Augenhöhe), Blick nach Norden:
Kegel im Mittelgrund, Kraterteich spiegelt, dahinter das Grün der Aue und der Bach.
**Detail-Ebenen:** Held – größter Kegel mit Teich (Ø 34 m). Begleiter 4 – weitere Kegel (Stempel). Schutt 80–150 – Schlacke am
Kraterrand `SM_lava_m_rock_02/07`, `SM_lava_s_rock_03…08`, Schweißschlacken `SM_lava_wall_06/07/08`. Kleinzeug –
`SM_SmallStonesPack_*`, `SM_stone_05…07`. Bewuchs nach Ursache – Flanken grün (älter, feucht): `SM_wk2oaeyqx_VarA…I`,
`SM_grey_willow_01…04` (Kriechweiden) an den Teichen, `SM_Rohrkolben_Horst_1…6` sparsam am Teichrand, Moos `SM_MossClump_*`;
Kraterränder kahl (Wind). Kontaktzone – Nassband am Teich (`MI_Leakage_*`), Kiesring.
**Wasser:** 2 `see` in den Kratern (`schwarz_spiegel`, Ø 12 m, 1,5 m tief), 1 `bach` als Überlauf (Breite 0,6 m, `muendung` =
Aue-Bach nördlich, Gefälle stetig).
**Effekte, Licht:** `lokaler_nebel` 1× dünn über den Teichen (Dichte 0,03). Keine Glut.
**Geländeänderung:** 5 Kegelstempel (+3,5 … +7,5 m, Krater −2 … −5 m), Fenster ca. 200 × 180 m, Δ max 7,5 m; Krater mit Wasser
gefüllt (keine trockenen geschlossenen Senken: die drei kleinen Krater flach, 2 m, mit Moosboden und Rinne).
**Assets:** Bestand wie oben; Coast & Dunes Decals (B, Nassband), Icelandic Sand With Pebbles (C), Tundra Icelandic Rock Cluster (C).
**Aufwand und Risiko:** mittel. Risiko: Nähe zu Zalas Stadt (210 m) – Silhouetten der Ruinen dürfen nicht ins `_held`-Bild.
Budget: ~6 000 Instanzen (400 Kollision), 10 Akteure, 0 Lichter, 0 Niagara, 1 Nebel, 4 Decals.

## lava_04_roehrenfenster – Das Röhrenfenster (Fundstück)

**Was man sieht:** Auf dem Moosplateau liegt ein Druckrücken; wer darüber geht, steht plötzlich an einem 26 × 16 m großen,
8 m tiefen Loch. Die Decke einer Lavaröhre ist eingestürzt: an beiden Enden öffnen sich schwarze Röhrenmäuler unter überhängenden
Lavaplatten, am Grund liegt Bruchschutt, über dem eine kleine **Farnoase** wächst – kühl, feucht, grün im schwarzen Stein. Ein
Lichtschacht fällt schräg hinein. Zwei kleine Einsenkungen im Moos zeigen, wohin die Röhre läuft.
**Vorbild:** Einbruchsfenster von Raufarhólshellir und Lofthellir (Island), Thurston Lava Tube (Hawaii); Spiel: Höhleneingänge
Skelliges (Witcher 3) im Licht-/Farnspiel.
**Standort:** C5, X −1792 / Y 780 m, Boden 36,8 m. Rand des Moos-Lavaplateaus über der Wiese (Stromrand 35–37 m, Hang 10–22°,
TPI100 +3,2 m) – Röhren laufen hangab zum Stromrand (nach NO). Wiese 45 %, Moos 37 %. Weg 286 m, Wasser 175 m.
**Verdeckung:** heute (flach, Silhouette 1 m) sieht man den Ort von 6 der 20 Wegpunkte ≤ 400 m – deshalb Druckrücken +3,5 m
zwischen Weg und Fenster. Mit Stempel: **Einblick in die Grube 0 %**, auch ein 1-m-Objekt am wegseitigen Rand 0 % (0 von 20
Wegpunkten). Man findet das Fenster erst auf dem Rücken.
**Komposition und Anmarsch:** Zugang 335 m vom Weg bei „Labor drei“ (max. 13,8°). `_anmarsch` auf dem Zugang, Augenhöhe.
`_held` auf dem Druckrücken (24 m), Blick nach Süden hinab: Farnoase im Lichtschacht, Röhrenmaul als dunkles Blickziel.
**Detail-Ebenen:** Held – Grube + Deckenlippen `SM_lava_wall_01/02/09` kopfüber als Akteure (Überhang ist Netz, kein Gelände).
Begleiter 4–6 – große Deckenbrocken `SM_lava_b_rock_01…04` am Grund. Schutt 60–120 – `SM_lava_m_rock_*` als Bruchkegel unter den
Rändern. Kleinzeug – `SM_lava_s_rock_06…08`, `SM_SmallStonesPack_*`. Bewuchs nach Ursache – Farne nur im kühlen Schacht
(`SM_EagleFern_M_01`, `SM_EagleFern_S_01/02/04`, `SM_foliage_fern_01_1…4`, `SM_Fern_01a/02a`), Moospolster an der schattigen
Nordwand (`SM_moss_01/02`, `SM_MossClump_*`), oben Moos und Wiese wie heute. Kontaktzone – Tropfspuren `MI_Leakage_01…13` an den
Wänden, Moos kriecht über die Kante.
**Wasser, Effekte, Licht:** kein offenes Wasser (Abfluss in die Röhre). `lokaler_nebel` 1× im Schacht (Kaltluft, 0,05).
Keine Lichter – das Dunkel der Röhrenmäuler ist gewollt.
**Geländeänderung:** Grube −8 m (Ellipse 26 × 16 m), Druckrücken +3,5 m, 2 Einsenkungen −1,5/−2 m. Fenster ca. 90 × 90 m.
Die Grube ist eine geschlossene Senke ohne Wasser – begründet: sie entwässert sichtbar in die beiden Röhrenmäuler.
**Assets:** Bestand wie oben; Cave Ambience (B, Tropfen/Hall), Niagara Examples (A, Mist Card); Lücke Lavaröhre ohne Asset.
**Aufwand und Risiko:** mittel–hoch. Risiko: Fugen zwischen Gelände und Deckenlippen → Lippen tief einbinden, Moos-Decal über die
Naht.
Budget: ~3 500 Instanzen (500 Kollision), 25 Akteure, 0 Lichter, 1 Niagara (optional), 1 Nebel, 8 Decals.

## lava_05_klare_spalte – Die Klare Spalte (Fundstück)

**Was man sieht:** Mitten in der Mooslava klafft eine 110 m lange, 4–9 m breite Spalte. 5 m unter der Kante steht Wasser so klar,
dass man 6 m tiefer jeden Block am Grund sieht – türkis in der Mitte, fast schwarz in den Klüften. Die Wände sind senkrecht
geklüfteter Basalt, mit Moos auf jeder Leiste. Über der Engstelle klemmt ein Felsblock; an der Kante steht eine windschiefe Birke.
**Vorbild:** Silfra und Almannagjá (Þingvellir), Grjótagjá; Spiel: Hellblade II.
**Standort:** C6, X −2604 / Y 982 m, Boden 29,6 m. Moos-Lavaebene im Westen (Moos 55 %, Wiese 23 %, Lavafels 17 %, Hang 12°),
Spalte NO–SW (Azimut 40°) parallel zur Eruptionsspalte der Kraterreihe – dieselbe Dehnungsrichtung. Weg 242 m, Zalas Stadt 151 m
(Mitte; die Spalte endet nach SW), Biominneres 46 m.
**Verdeckung:** heute (Silhouette 1 m) max. Anteil 0,36 von 4 der 15 Wegpunkte ≤ 400 m. Die Spalte liegt unter Flur: **Einblick
0,4 %** (max. Anteil 0,004). Die Kante selbst ist offene Moosfläche – auf der Wegseite (NO) deshalb nichts über 0,5 m setzen;
Moos-Tumulus +2,4 m am NO-Ende als Rahmen.
**Komposition und Anmarsch:** Zugang 252 m ohne Pfadbau (max. 14,6°). `_held` am NO-Ende auf dem Tumulus, Blick nach SW die Spalte
entlang (Fluchtpunkt, Wasser leuchtet, Birke als Rahmen). Abstieg über eine Schuttrampe an der Engstelle zum Wasser.
**Detail-Ebenen:** Held – Spalte (Stempel) mit Wänden aus `SM_lava_wall_04/05` senkrecht gereiht (`MI_EL_SW_Basalt_Saeule` nur
als Klufttönung). Begleiter 3–5 – Klemmblock `SM_lava_b_rock_02`, Bruchblöcke `SM_lava_b_rock_01/03` im Wasser (sichtbarer Grund).
Schutt 80–150 – `SM_lava_m_rock_*` an den Wandfüßen und als Rampe. Kleinzeug – `SM_lava_s_rock_06…08` am Ufer. Bewuchs nach
Ursache – Moos auf Leisten (Feuchte), Farne in schattigen Klüften (`SM_foliage_fern_01_*`), eine Windbirke `Big_Tree_Birch_01`
× 0,45 an der Kante (Windflüchter), Kriechweiden `SM_grey_willow_01…04`. Kontaktzone – Nassband an der Wasserlinie (Coast & Dunes
Decals / `MI_Leakage_*`), Moos kriecht über die Kante.
**Wasser:** `see` in der Spalte (`tuerkis`, Spiegel 5 m unter Flur, 6 m tief, Umriss gegen den Uhrzeigersinn), Grundwasser ohne
Zufluss – klar, kein Schaum.
**Effekte, Licht:** keine. Lichtspiel über das Wasser (Kaustik im Wassermaterial, falls vorhanden).
**Geländeänderung:** Rinne −11 m (Breite 6 m, Rand 2,5 m) über 110 m, Tumulus +2,4 m. Fenster ca. 160 × 120 m.
**Assets:** Bestand wie oben; Coast & Dunes Decals (B); Wunsch Tundra Icelandic Rock Cluster (C). Basalt Columns (A) optional für
die Wände.
**Aufwand und Risiko:** hoch. Risiko: Gelände kann keine senkrechten Wände – Wände sind Netze, Fugen zum Gelände sorgfältig decken;
Wasser in schmaler Rinne braucht saubere Ufer-Netze.
Budget: ~5 000 Instanzen (900 Kollision), 45 Akteure, 0 Lichter, 0 Niagara, 0 Nebel, 8 Decals.

## lava_06_kraterreihe – Die Kraterreihe (Leuchtfeuer, nur mit Kratersteig)

**Was man sieht:** Am Nordostfuß des Vulkans stehen vier Schlackenkegel auf einer schnurgeraden Spalte, wie Perlen auf einer Schnur.
Der größte, ein nach Südwesten offener Hufeisenkegel, ragt 27 m auf; sein Krater ist 16 m tief, innen rostrot, außen schwarz.
Aus dem Kraterboden steigt ein Hauch Restdampf. Zwischen den Kegeln Schweißschlacke und ein Fächer roter Schlacke.
**Vorbild:** Lakagígar (Laki-Spalte), Eldgjá; Spiel: Mt. Gelmir (Elden Ring).
**Standort:** C6, X −1790 / Y 1345 m, Boden 58,6 m. Vorhandene Kegelkette (alte Kachel, im Gelände enthalten): Kraterböden bei
(−1698/1240) 36 m, (−1762/1322) 52 m, (−1804/1340) 56 m, (−1844/1430) 66 m; Hauptkegel-Rand 82 m. Richtung NO–SW (37°).
Heute 737 m vom Weg; zum Kratersteig (Ast Ost) 148 m.
**Sicht (mit Steig):** 27 von 69 Wegpunkten im Ring sehen ≥ 30 % (Zielhöhe 18 m), bis 593 m; `_fern` vom Steig (412 m).
**Komposition und Anmarsch:** Zugang 160 m vom Steigende (max. 14,2°). `_held` am Steigende, Augenhöhe, Blick nach Südosten:
rechts der Hauptkegel (170 m), nach links staffeln sich die kleineren Kegel bis 240 m. `_nah` am Kraterrand des Hauptkegels.
**Detail-Ebenen:** Held – Hauptkegel (Gelände, Rand schärfen). Begleiter 3 – kleinere Kegel. Schutt 150–250 – Schlacke
`SM_lava_m_rock_*`, `SM_lava_s_rock_*`, rote Schlacke mit `MI_EL_SW_Schlacke_Rot`, Spatterfladen `SM_lava_wall_06/07/08`.
Kleinzeug – Lapilli als Lage Lavasand + `SM_SmallStonesPack_*`. Bewuchs nach Ursache – auf dem jungen Kegel fast nichts; Moos nur
an der Nordseite des ältesten (NO-)Kegels, einzelne `SM_wk2oaeyqx_*` in Windschatten. Kontaktzone – Schlacke 40 % eingegraben.
**Wasser, Effekte, Licht:** Restdampf (Lava & Volcano Niagara, optional) + `lokaler_nebel` klein im Krater. Keine Glut.
**Geländeänderung:** Kraterrand +2 m / Krater −2 m schärfen, Lage Lavasand rotbraun über Material. Fenster ca. 300 × 300 m
(Kette 300 m lang).
**Assets:** Bestand; Lava & Volcano (A), Fantasy Ambiences (B).
**Aufwand und Risiko:** niedrig–mittel (Form ist schon da). Risiko: alte Kachel-Optik („Houdini-Kegel“) muss durch Material/Schlacke
natürlich werden – Bildwunsch.
Budget: ~8 000 Instanzen (600 Kollision), 15 Akteure, 0 Lichter, 1 Niagara, 1 Nebel, 4 Decals.

## lava_07_basaltorgel – Die Basaltorgel (Fundstück, nur mit Kratersteig)

**Was man sieht:** Vom Plateau aus nichts. Wer am Rand hinabsteigt, steht in einer kleinen Schlucht vor einer 16–20 m hohen,
leicht gebogenen Wand aus **sechseckigen Basaltsäulen** – oben gefächert wie Orgelpfeifen, unten senkrecht. Am Fuß liegen
abgebrochene Säulenstücke wie gestapelte Stämme; Moos besetzt die Stufen, Sickerwasser zeichnet dunkle Streifen.
**Vorbild:** Gerðuberg und Svartifoss (Island), Stuðlagil; Spiel: Säulenbasalt in Skellige (Witcher 3).
**Standort:** B6, X −2795 / Y 1390 m, Boden 42,3 m. Schlucht zwischen Aschenplateau (55–58 m) und Westhügel (80–95 m): Talboden
40–44 m, Plateaukante 10–14 m bei 30–35°, TPI100 −10,5 m. Biominneres 59 m. Heute 661 m vom Weg; zum Kratersteig (Ast West) 107 m.
**Verdeckung (mit Steig):** heute und mit Stempel **verdeckt**: 0 von 38 Wegpunkten ≤ 400 m sehen die Wand (max. Anteil 0,0) –
sie liegt unter der Plateaukante.
**Komposition und Anmarsch:** Zugang 116 m (max. 24,5°) – über die Kante als kleiner Pfad mit Trittstufen im Schutt (Rampe von
Norden). `_held` auf dem Schluchtboden, Augenhöhe, Blick nach Osten auf die Wand; `_nah` 10 m vor den Säulenfüßen.
**Detail-Ebenen:** Held – Säulenwand (Basalt Columns, 21 Typen) auf 90 m Länge. Begleiter 6–10 – Säulengruppen, gekippte Säulen.
Schutt 100–200 – Säulenstücke in der Halde (Ursache: Frostsprengung). Kleinzeug – `SM_lava_s_rock_06…08`, `SM_stone_05…07`.
Bewuchs – Moospolster auf Stufen und Halde (Nordwand schattig), Farne in Fugen, Gras am Schluchtboden. Kontaktzone –
Sickerstreifen `MI_Leakage_*`, Moos am Wandfuß (`M_EL_Klippe_RVT` Fußblend, `MI_EL_SW_Basalt_Saeule`).
**Wasser, Effekte, Licht:** nur Sickerwasser (Decals). Schlucht im Halbschatten – Säulenkanten fangen Streiflicht.
**Geländeänderung:** Kante +4 m (Band 8 m) → Wand 16–20 m; Fenster ca. 150 × 150 m.
**Assets:** Basalt Columns and Rocks 21 Types – AssetKit PBR (A, ca. 11 €, Ferat entscheidet). Ersatz `SM_lava_wall_04/05`
senkrecht + `SM_IcelandicLavaSpire_01/03` – ohne echte Sechsecke deutlich schwächer.
**Aufwand und Risiko:** mittel mit Paket, hoch ohne. Risiko: Säulen-Paket ohne belegtes Nanite.
Budget: ~4 000 Instanzen (800 Kollision), 70 Akteure, 0 Lichter, 0 Niagara, 0 Nebel, 6 Decals.

## lava_08_glutauge – Das Glutauge (Fundstück, nur mit Kratersteig)

**Was man sieht:** Auf dem jungen, schwarz glänzenden Strom des Westplateaus – Stricklava mit Seilen, Zehen und aufgewölbten
Schollen – liegt zwischen zwei Buckeln ein 8 × 6 m großes Loch. 6 m tief darunter fließt dumpf orange **Glut** vorbei, die Luft
darüber flimmert, ein dünner Dampf zieht. In Haarrissen ringsum glimmt es kaum sichtbar. Kein Halm wächst hier.
**Vorbild:** Skylights am Kīlauea (Puʻu ʻŌʻō-Röhren), Fagradalsfjall 2021; Spiel: Muspelheim (God of War) – aber dezent.
**Standort:** B6, X −2745 / Y 1740 m, Boden 64,8 m. Junger Lavastrom (Lavafels 73 %) auf dem flachen Abschnitt des Westplateaus
(Hang 9°, Relief 10,5 m), der Strom reicht weiter bis zur Westküste. Heute 936 m vom Weg; zum Kratersteig 118 m.
**Verdeckung (mit Steig):** **Einblick 0 %** (0 von 18 Wegpunkten ≤ 400 m sehen in den Schacht); die Kante ist offene Lava – dort
nichts über 0,5 m. Die Glut sieht man nur vom Rand.
**Komposition und Anmarsch:** Zugang 126 m (max. 6,8°). `_held` auf dem nordöstlichen Buckel (+1,8 m), Blick schräg in den Schacht;
`_nah` 7 m.
**Detail-Ebenen:** Held – Schacht mit Glut (Lava-Material, Lava & Volcano). Begleiter 2 – Tumuli (Buckel) mit Rissen.
Schutt 40–80 – Krustenplatten `SM_lava_wall_06/07/08` liegend mit `MI_EL_SW_Lava_Glasur`. Kleinzeug – `SM_lava_s_rock_06…08`.
Bewuchs – keiner (zu jung, zu heiß); Kontrast zu 04. Kontaktzone – Glut-Decals (Lava-Set, 3–4 Stück) in Rissen, Rußdecal am Rand.
**Wasser, Effekte, Licht:** 1 `punktlicht` orange [1,0; 0,45; 0,15], 800 cd, Radius 600 cm, kein Schatten, im Schacht; Niagara
Hitzeflimmern + Funken (optional, Lava-Set / Ultimate Niagara). Wirkung im Schatten des Schachts auch bei fester Sonne.
**Geländeänderung:** Schacht −6 m (8 × 6 m), 2 Tumuli +1,4/+1,8 m. Fenster ca. 90 × 90 m.
**Assets:** Lava & Volcano (A, Material + Decals), Ultimate Niagara Environmental VFX (B), Fantasy Ambiences (B).
**Aufwand und Risiko:** mittel. Risiko: Glut zu stark → Kitsch; Intensität klein halten, Bild mit fester Sonne prüfen.
Budget: ~2 500 Instanzen (300 Kollision), 20 Akteure, 1 Licht, 2 Niagara, 0 Nebel, 6 Decals.

---

## Materialwünsche (≤ 6, Details in `asset_bedarf.json`)

`MI_EL_SW_Lava_Moos` (M_EL_Fels_Auflage, grau-grünes Moos) · `MI_EL_SW_Schlacke_Rot` (M_EL_Fels_MS, Tönung rostrot) ·
`MI_EL_SW_Schwefelkruste` (M_EL_Fels_Auflage, gelb in Hohlformen) · `MI_EL_SW_Schwefel_Decal` (M_MS_Decal, Tint gelb) ·
`MI_EL_SW_Basalt_Saeule` (M_EL_Klippe_RVT, kühles Grau) · `MI_EL_SW_Lava_Glasur` (M_EL_Fels_MS, Rauheit 0,35).

## Offene Fragen an Ferat

1. **Kratersteig bauen?** Zwei Äste (624 m + 898 m, max. 22°) vom Archivpfad. Ohne Steig bleibt das Biom bei 5 Orten und der
   Vulkan ohne Ziel. Alternativ: Regel „80–300 m vom Weg“ für das Lava-Biom lockern (dann wäre auch der Gipfelkrater denkbar – der
   Kegel ist aber 30–40° steil und braucht Serpentinen).
2. **Basalt Columns (ca. 11 €)** – nur nötig, wenn lava_07 kommt.
3. **Bildwünsche** (leere Standorte, Kameras in `asset_bedarf.json`): Kraterreihe (alte Kachel heute), Westschlucht, Stromfront,
   Kraterkinder-Senke.

<!-- abgleich-13b13c -->

## Abgleich mit Inventar 13b und Entscheidungen 13c (Stand 11.10.2026)

Neues Inventar: `netze.csv` mit 1 692 Netzen, `inventar_extra.json` mit 73 Niagara-Systemen, 15 Effekt-Blueprints und 46 Klang-Cues. Maschinenlesbar steht alles in `asset_bedarf.json` → `abgleich_13b_13c`. Der Abschnitt ergänzt die Ortsbeschreibungen oben; wo er abweicht, gilt er.

### Entscheidungen aus 13c

- **Kratersteig bauen** (lava_06_kraterreihe, lava_07_basaltorgel, lava_08_glutauge): Ja (13c), damit hat das Lava-Biom 8 Orte. Den Pfadverlauf überführt ein anderer Agent nach `standorte.json` (`pfade`, Schema in `skripte/sehens_lib/README.md`).
- **Basaltorgel mit /Game/Basalt** (lava_07_basaltorgel): Das Paket ist gekauft und im Projekt (22 Netze, **kein Nanite**). Säulen haben 0,29 m Querschnitt und 0,15–2,6 m Höhe. Orgelwand aus `Basalt_Basalt_Pillars_Wall_SM`/`_WallSlope_SM`/`_WallOverhang_SM` und `Basalt_Basalt_Pillars_Cluster_High_SM` in Gruppen, Skalierung 3–8× (Säulen dann 0,9–2,3 m). Davor Säulenstümpfe `Basalt_Basalt_Pillar_A–D_SM`/`_Variance_A–D_SM` und Blöcke `Basalt_Basalt_Rock_A–D_SM`. Die Kante bildet `Basalt_Basalt_Cliff_SM` (8,6 × 5,3 × 6,0 m, ×3–4). Weil die Netze nicht Nanite sind, die Akteure zählen (≤ 80) und lieber wenige große Stücke setzen.
- **Wegabstand 324/393 m** (lava_04_roehrenfenster, lava_05_klare_spalte): In Ordnung (13c).

### Neu im Bestand – je Ort

| Ort | Asset | Pfad | Maße (m) | Einsatz |
|---|---|---|---|---|
| lava_01_schwarze_mauer | `Basalt_Basalt_Cliff_Rock_A_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Cliff_Rock_A_SM` | 8,34 × 5,07 × 5,63 | Wandschollen-Ersatz für SM_lava_wall_01/02/03/09 (bis 13d) |
| lava_01_schwarze_mauer | `Basalt_Basalt_Rock_B_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Rock_B_SM` | 1,17 × 1,52 × 0,78 | Schuttsaum |
| lava_02_schwefelgrund | `NS_Smoke_Plume` (Niagara) | `/Game/NiagaraExamples/FX_Smoke/NS_Smoke_Plume` | – | Dampfsäule am Dampfschlot |
| lava_02_schwefelgrund | `NS_Chimney_Smoke` (Niagara) | `/Game/NiagaraExamples/FX_Smoke/NS_Chimney_Smoke` | – | 6–9 kleine Fumarolenfahnen (Kopie, weiß-grau, dünn) |
| lava_03_kraterkinder | `CUE_Water_Stream_II_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Water_Stream_II_Cue` | – | Aue-Bach dahinter (Grundklang) |
| lava_04_roehrenfenster | `Basalt_Basalt_Pillars_WallOverhang_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillars_WallOverhang_SM` | 1,62 × 0,98 × 2,55 | Deckenlippe kopfüber (Ersatz für SM_lava_wall_01/02/09 bis 13d) |
| lava_04_roehrenfenster | `Basalt_Basalt_Cliff_Rock_B_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Cliff_Rock_B_SM` | 7,49 × 5,41 × 1,52 | flache Deckenplatte kopfüber |
| lava_04_roehrenfenster | `BP_FogBankCard` (Blueprint) | `/Game/NiagaraExamples/FX_Fog/BP_FogBankCard` | – | Kaltluftdunst im Schacht (Mist Card, Blueprint) |
| lava_04_roehrenfenster | `CUE_Rain_Dropping_on_various_textures_Cue` (Klang) | `/Game/City_Nature_Sounds/CUE/CUE_Rain_Dropping_on_various_textures_Cue` | – | Tropfen im Röhrenmaul (prüfen, ob es nach Tropfen und nicht nach Regen klingt) |
| lava_05_klare_spalte | `Basalt_Basalt_Pillars_Wall_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillars_Wall_SM` | 1,61 × 0,76 × 2,55 | Spaltenwände senkrecht gereiht (statt SM_lava_wall_04/05) |
| lava_05_klare_spalte | `Basalt_Basalt_Pillars_WallSlope_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillars_WallSlope_SM` | 2,44 × 1,55 × 3,02 | Spaltenwand schräg |
| lava_06_kraterreihe | `NS_Chimney_Smoke` (Niagara) | `/Game/NiagaraExamples/FX_Smoke/NS_Chimney_Smoke` | – | Restdampf im Hauptkrater, dezent |
| lava_07_basaltorgel | `Basalt_Basalt_Pillars_Wall_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillars_Wall_SM` | 1,61 × 0,76 × 2,55 | Orgelwand-Modul ×3–8 |
| lava_07_basaltorgel | `Basalt_Basalt_Pillars_WallSlope_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillars_WallSlope_SM` | 2,44 × 1,55 × 3,02 | Orgelwand schräg |
| lava_07_basaltorgel | `Basalt_Basalt_Pillars_WallOverhang_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillars_WallOverhang_SM` | 1,62 × 0,98 × 2,55 | Orgelwand mit Überhang |
| lava_07_basaltorgel | `Basalt_Basalt_Pillars_Cluster_High_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillars_Cluster_High_SM` | 0,76 × 0,79 × 2,62 | Säulenbündel hoch |
| lava_07_basaltorgel | `Basalt_Basalt_Pillars_Cluster_Low_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillars_Cluster_Low_SM` | 1,09 × 0,93 × 0,62 | Säulenbündel niedrig (Stümpfe) |
| lava_07_basaltorgel | `Basalt_Basalt_Cliff_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Cliff_SM` | 8,61 × 5,31 × 6,02 | Plateaukante ×3–4 |
| lava_07_basaltorgel | `Basalt_Basalt_Cluster_A_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Cluster_A_SM` | 3,43 × 3,83 × 3,21 | Felsgruppe am Fuß |
| lava_07_basaltorgel | `Basalt_Basalt_Cluster_A_Rocks_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Cluster_A_Rocks_SM` | 3,4 × 3,2 × 3,09 | Felsgruppe, Schutt |
| lava_07_basaltorgel | `Basalt_Basalt_Pillar_A_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillar_A_SM` | 0,29 × 0,25 × 0,15 | Säulenstumpf |
| lava_07_basaltorgel | `Basalt_Basalt_Pillar_B_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillar_B_SM` | 0,29 × 0,26 × 0,74 | Säule |
| lava_07_basaltorgel | `Basalt_Basalt_Pillar_C_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillar_C_SM` | 0,29 × 0,26 × 0,91 | Säule |
| lava_07_basaltorgel | `Basalt_Basalt_Pillar_D_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillar_D_SM` | 0,29 × 0,26 × 2,63 | Säule lang (2,6 m → ×8 = 21 m) |
| lava_07_basaltorgel | `Basalt_Basalt_Pillar_Variance_A_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillar_Variance_A_SM` | 0,28 × 0,27 × 0,22 | Säulenstumpf |
| lava_07_basaltorgel | `Basalt_Basalt_Pillar_Variance_B_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillar_Variance_B_SM` | 0,3 × 0,32 × 0,64 | Säule |
| lava_07_basaltorgel | `Basalt_Basalt_Pillar_Variance_C_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillar_Variance_C_SM` | 0,24 × 0,27 × 1,31 | Säule |
| lava_07_basaltorgel | `Basalt_Basalt_Pillar_Variance_D_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Pillar_Variance_D_SM` | 0,26 × 0,29 × 2,28 | Säule lang |
| lava_07_basaltorgel | `Basalt_Basalt_Rock_A_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Rock_A_SM` | 0,81 × 0,86 × 0,67 | Block |
| lava_07_basaltorgel | `Basalt_Basalt_Rock_B_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Rock_B_SM` | 1,17 × 1,52 × 0,78 | Block |
| lava_07_basaltorgel | `Basalt_Basalt_Rock_C_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Rock_C_SM` | 1,31 × 1,19 × 1,67 | Block |
| lava_07_basaltorgel | `Basalt_Basalt_Rock_D_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Rock_D_SM` | 2,1 × 2,29 × 1,36 | Block |
| lava_07_basaltorgel | `Basalt_Basalt_Cliff_Rock_A_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Cliff_Rock_A_SM` | 8,34 × 5,07 × 5,63 | Wandblock |
| lava_07_basaltorgel | `Basalt_Basalt_Cliff_Rock_B_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Cliff_Rock_B_SM` | 7,49 × 5,41 × 1,52 | Platte |
| lava_08_glutauge | `Basalt_Basalt_Cliff_Rock_B_SM` (kein Nanite) | `/Game/Basalt/meshes/Basalt_Basalt_Cliff_Rock_B_SM` | 7,49 × 5,41 × 1,52 | Krustenplatten liegend (statt SM_lava_wall_06/07/08 bis 13d) |
| lava_08_glutauge | `NS_Spark_Continuous` (Niagara) | `/Game/NiagaraExamples/FX_Sparks/NS_Spark_Continuous` | – | Glutfunken über dem Fenster – Kopie, wenige, langsam, orange (optional) |

### Paketstatus der Wünsche dieses Bioms

| Paket | Status | Orte |
|---|---|---|
| Basalt Columns and Rocks 21 Types – AssetKit PBR | im Projekt (/Game/Basalt/meshes, 22 Netze, kein Nanite) | 07 |
| Cave Ambience | fehlt (Download-Liste) | 04 |
| Coast & Dunes – Environment Set (Decals, Seetang, Stempel neu hinzufügen) | läuft bei Ferat | 03, 05 |
| Fantasy Ambiences (Lava, Höhle, Wind …) | fehlt (Download-Liste) | 02, 06, 08 |
| Free City & Nature Sounds | im Projekt (/Game/City_Nature_Sounds, nur Naturklänge nutzen) | 01, 03, 05 |
| Lava & Volcano – Environment Set (fehlende Teile neu hinzufügen) | läuft bei Ferat | 02, 06, 08 |
| Megascans Icelandic Sand With Pebbles | fehlt (Download-Liste) | 01, 03 |
| Niagara Examples Pack | im Projekt (/Game/NiagaraExamples) | 02, 04 |
| Realistic Starter VFX Pack Vol 2 | gestrichen (Dampf jetzt NS_Smoke_Plume/NS_Chimney_Smoke) | 02 |
| Ultimate Niagara Environmental VFX | fehlt (Download-Liste) | 08 |

### Fehlt weiterhin

- SM_lava_wall_01 … SM_lava_wall_09 (Lava & Volcano) stehen **nicht mehr in netze.csv** (1 692 Netze, Stand 13:25). Vermutlich hängt das an der laufenden Nachladung von Lava & Volcano. Der Katalog nennt sie weiter, bis das Inventar 13d da ist. Bis dahin gilt im Plan der Ersatz aus `/Game/Basalt` (siehe Tabelle) bzw. `SM_lava_b_rock_*`/`SM_lava_m_rock_*`.
- Hitzeflimmern, Lava-Material, 7 Glut-Decals: kommen mit Lava & Volcano (läuft bei Ferat).

### Material-Instanzen (6 von höchstens 6)

| Name | Basis | Parameter | für |
|---|---|---|---|
| `MI_EL_SW_Lava_Moos` | `M_EL_Fels_Auflage` | `Auflage_Farbe` [0,55, 0,66, 0,36, 1], `Auflage_Menge` 0,75, `Auflage_Schwelle` 0,55, `Auflage_Flecken` 0,7, `Toenung` [0,42, 0,4, 0,4, 1] | SM_lava_wall_01 (nach 13d), SM_lava_wall_02 (nach 13d), `SM_lava_b_rock_01`, `SM_lava_m_rock_01`, `Basalt_Basalt_Cliff_Rock_A_SM` |
| `MI_EL_SW_Schlacke_Rot` | `M_EL_Fels_MS` | `Toenung` [0,62, 0,3, 0,22, 1], `Helligkeit` 0,9, `Variation` 0,7 | `SM_lava_m_rock_02`, `SM_lava_s_rock_03`, SM_lava_wall_07 (nach 13d) |
| `MI_EL_SW_Schwefelkruste` | `M_EL_Fels_Auflage` | `Auflage_Farbe` [0,95, 0,82, 0,25, 1], `Auflage_Menge` 0,6, `Auflage_Hohl` 0,85, `Auflage_Rauheit` 0,95 | `SM_lava_m_rock_05`, `SM_lava_s_rock_01`, `SM_lava_b_rock_04` |
| `MI_EL_SW_Schwefel_Decal` | `M_MS_Decal` | `BaseColor Tint` [1, 0,84, 0,3, 1], `Saturation` 1,3, `Min Roughness` 0,7 | Decal (Maske aus MI_Leakage_04) |
| `MI_EL_SW_Basalt_Saeule` | `M_EL_Klippe_RVT` | `Toenung` [0,55, 0,55, 0,58, 1], `Fels_Saettigung` 0,4, `Moos_Menge` 0,35, `Moos_Farbe` [0,6, 0,72, 0,4, 1] | `Basalt_Basalt_Pillars_Wall_SM`, `Basalt_Basalt_Pillars_WallSlope_SM`, `Basalt_Basalt_Pillars_WallOverhang_SM`, `Basalt_Basalt_Pillars_Cluster_High_SM`, `Basalt_Basalt_Cliff_SM` – MI_EL_SW_Basalt_Saeule nur, falls das Basalt-Originalmaterial zu frisch/glatt wirkt; dann Albedo/Normal/ORM aus /Game/Basalt in die Instanz übernehmen (sonst zeigt M_EL_Klippe_RVT die Nordklippen-Textur). |
| `MI_EL_SW_Lava_Glasur` | `M_EL_Fels_MS` | `Rauheit` 0,35, `Specular` 0,6, `Toenung` [0,5, 0,48, 0,52, 1] | `Basalt_Basalt_Cliff_Rock_B_SM`, SM_lava_wall_06/07/08 (nach 13d) |
