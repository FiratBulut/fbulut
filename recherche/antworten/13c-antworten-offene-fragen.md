# Antwort auf Auftrag 13c – Umsetzung der Entscheidungen

Stand 11.10.2026, nachmittags

## Kurzfazit

- **Jede Entscheidung aus 13c ist eingearbeitet.** Sie steht in `antworten/sehens/<biom>/katalog.md` (Abschnitt „Abgleich mit Inventar 13b und
  Entscheidungen 13c“) und maschinenlesbar in `asset_bedarf.json` → `abgleich_13b_13c.entscheidungen_13c`.
- **Pfade:** Ein anderer Agent hat die Steige von Lava, Gletscher, Frost und Fjord als `"pfade"` in die jeweilige `standorte.json` überführt.
  Das Schema steht in `antworten/skripte/sehens_lib/README.md`, Abschnitt „Pfade (Auftrag 13c)“. Den Stand trägt der Koordinator in
  `sehens-STATUS.md` nach. Die `standorte*.json` habe ich nicht angefasst.
- **Decal-Textur für die Brutröhren** (aue_03) liegt vor: `sehens/aue/decal_brutroehren.png` (RGBA 1024², nahtlos in X) und
  `decal_brutroehren_n.png`.
- **Cenote** (dschungel_04) ist jetzt ein eigener `see` mit `farbe: tuerkis`, **Tausendfuß** ist gestrichen.
- **Material-Instanzen** stehen je Biom in einer Tabelle, nirgends mehr als 6.

## Je Frage: was umgesetzt wurde und wo

### Allgemein

| Frage / Entscheidung | Umsetzung | Datei |
|---|---|---|
| Neues Inventar nutzen | Alle 8 Biome der ersten Welle abgeglichen. Je Ort stehen vorhandene Netze, Niagara-Systeme, Blueprints und Klänge mit echtem Pfad und Maßen. Jeder Name ist gegen `netze.csv` und `inventar_extra.json` geprüft. | `sehens/*/asset_bedarf.json` (`abgleich_13b_13c.vorhanden`), `sehens/*/katalog.md` |
| Pfade erwünscht | Ein anderer Agent hat die Steige als `"pfade"` (`id`, `art`, `breite_cm`, Punkte) in `standorte.json` überführt. Den Stand trägt der Koordinator nach. | `sehens/{lava,gletscher,frost,fjord}/standorte.json`, `skripte/sehens_lib/README.md` |
| Bildwünsche | Bleiben wie in den `asset_bedarf.json`; Ferat macht sie, sobald der Editor frei ist. | unverändert |
| Material-Instanzen ≤ 6 je Biom | Je Biom eine Tabelle „Material-Instanzen (n von höchstens 6)“. Alle Parameter sind gegen `material_parameter.json` geprüft. Stand: aue 6, bergwald 4 (bisher nur im Katalog, jetzt auch in `asset_bedarf.json`), lava 6, elfenwald 5, dschungel 0, gletscher 3, frost 3, fjord 2. | `sehens/*/katalog.md`, `asset_bedarf.json` → `materialwuensche` |

### elfenwald / dschungel

| Frage / Entscheidung | Umsetzung | Datei |
|---|---|---|
| 0,9-km-Serpentinenpfad zum Nebelhain: ja | Als Entscheidung vermerkt. Der Pfad gehört in `standorte.json` → `pfade` (anderer Agent bzw. Koordinator). | `sehens/elfenwald/katalog.md` |
| Mondtor-Bogen aus `SM_Cliff_01*`: ja | Sturz `SM_Cliff_01b`, Pfeiler `SM_Cliff_01c`. Die Fugen schließen Geröll, Moos und Decal, den Sockel ein Geländestempel. Neu: Kalkschutt `Limestone_Rocks_ubqwdheda_High` unter dem Tor. | `sehens/dschungel/katalog.md`, `asset_bedarf.json` |
| Rot getönte Buchenblatt-Instanz: ja, als Kopie | `MI_EL_SW_Rotlaub` und `MI_EL_SW_Rotlaub_Boden` haben den Hinweis „neue Instanz als Kopie; Original-Buchenblatt-Materialien bleiben unverändert“. Fallendes Laub: `NS_leaf` (Kopie, rot). | `sehens/elfenwald/asset_bedarf.json`, `katalog.md` |
| Cenote: eigener `see`, `farbe: tuerkis` | Im Ortstext von `tiefblau` auf **`tuerkis`** geändert; Spiegel unabhängig vom Meer. Das Meerwasser im Schacht bleibt Ferats Bildwunsch. | `sehens/dschungel/katalog.md` (dschungel_04), `asset_bedarf.json` |
| Tropenpflanzen im Bestand | Den von Ferat genannten Bestand vermerkt. Electric Dreams bleibt in der Download-Liste (B, kostenlos, Top 1 der fehlenden Pakete). | `sehens/dschungel/katalog.md`, `sehens-downloadliste.md` |
| „Tausendfuß“ streichen: ja | Gestrichen, ersetzt durch dschungel_08 Sinterhalle. Auch aus allen „wofür“-Feldern der Download-Liste entfernt. | `sehens/dschungel/katalog.md`, `downloadliste.json` |
| Leuchten mit Bestand | Leuchtsporen `NS_Sparkling_Glow` (elfenwald_01), Pollen `NS_Sparkling_Noise` (_06), Sporenstaub `NS_Sparkling` (_07), Nebelfetzen `BP_FogBankCard` (_02) – alles optional, als Kopie. | `sehens/elfenwald/…` |

### aue

| Frage / Entscheidung | Umsetzung | Datei |
|---|---|---|
| Die Alte jetzt mit Bestand | Held ist `SM_Poplar_tree_06_Optimised` ×1,3 (≈ 34,5 m, Schwarzpappel). `SM_dry_oak_0*` sind im Inventar, aber nur 3,9–9,0 m hoch und kein Nanite; als Held bräuchten sie ×3 und mehr. Sie bleiben Jungeichen und Begleiter. | `sehens/aue/katalog.md`, `asset_bedarf.json` |
| Eichenpaket in B | „Quercus Robur (Stieleiche) – Nanite & Impostor“ steht in B (Top 3 der fehlenden Pakete); die tote Stieleiche in C. | `sehens-downloadliste.md`, `downloadliste.json` |
| Erlen nicht im Bestand → Weiden/Pappeln/Birken | Ersatz je Ort: `SM_Poplar_tree_02/03_Optimised`, `Big_Tree_Birch_01`, `Big_Tree_Willow_01/02`, `SM_grey_willow_01–04`, `SM_Poplar_plant_A/C_00`. Die Erlen bleiben ein Wunsch in der Download-Liste. Laut Rückmeldung B8 ist das **B** (Held von sumpf_05 Erlenbruch), es wird aber nicht auf sie gewartet. | `sehens/aue/asset_bedarf.json`, `downloadliste.json` |
| 220 m Ufergehölz am Mondarm: ja | Gürtel aus Weiden, Pappeln und Birke mit einem Saum aus Strauchweiden. Dazu Seerosen `Rembrandt_Water_Lily_*` (VarA–G) als Held. | `sehens/aue/katalog.md`, `asset_bedarf.json` |
| Eigene Decal-Textur Brutröhren: ja | Erzeugt und beschrieben (siehe unten). Materialwunsch `MI_EL_SW_Brutroehren` auf `M_MS_Decal`; das Material legt Ferat an. Zusätzlich neu als Lehmwand: `SM_LS_beach_cliff_02_A/B/C` (16–23 × 6,6 m). | `sehens/aue/decal_brutroehren*.png`, `katalog.md` |

**Decal Brutröhren:**
- **Größe:** 1 Kachel = 200 × 200 cm (5,12 px/cm). Das Decal hat `groesse_cm` [30, 200, 200].
- **Inhalt:** 52 dunkle, ovale Röhren mit 6–9 cm Breite in sechs unregelmäßigen, gewellten Reihen. Dazu ausgetretene Lehmlippen, ein
  Schmutzhalo und bei 18 Röhren leichte Kotspuren.
- **Transparenz:** Außerhalb der Röhren ist das Decal transparent.
- **Projektion:** senkrecht auf die Wand, nur im oberen Wanddrittel, 6–8 Decals je Wand; dank Nahtlosigkeit in X auch nebeneinander setzbar.
- **Normal-Map:** in DirectX-/UE-Konvention.
- **Skript:** liegt nur im Scratchpad, nicht im Repo.

### lava

| Frage / Entscheidung | Umsetzung | Datei |
|---|---|---|
| Kratersteig bauen: ja → 8 Orte | Vermerkt. Der Pfadverlauf steht als `pfade` in `sehens/lava/standorte.json` (anderer Agent). | `sehens/lava/katalog.md` |
| Wegabstand 324/393 m in Ordnung | Vermerkt. | `sehens/lava/katalog.md` |
| Basaltorgel mit `/Game/Basalt` | Alle 22 Netze sind lava_07 zugeordnet: Wände `Basalt_Basalt_Pillars_Wall/_WallSlope/_WallOverhang_SM`, Bündel `_Pillars_Cluster_High/Low_SM`, Säulen `_Pillar_A–D_SM`/`_Variance_A–D_SM`, Kante `Basalt_Basalt_Cliff_SM` ×3–4, Blöcke. Die Gruppen werden 3–8× skaliert. `MI_EL_SW_Basalt_Saeule` zeigt jetzt auf die Basalt-Netze. | `sehens/lava/asset_bedarf.json`, `katalog.md` |
| (neu) `SM_lava_wall_01–09` fehlen im Inventar | Ersatz bis 13d aus Basalt: Wandschollen `Basalt_Basalt_Cliff_Rock_A_SM`, Deckenlippen `_Pillars_WallOverhang_SM` / `_Cliff_Rock_B_SM` kopfüber, Spaltenwände `_Pillars_Wall_SM`, Krustenplatten `_Cliff_Rock_B_SM`. Die Material-Instanzen sind angepasst. | `sehens/lava/…` |
| Effekte | Dampfsäule `NS_Smoke_Plume`, Fumarolenfahnen und Restdampf `NS_Chimney_Smoke`, Glutfunken `NS_Spark_Continuous` (Kopie, dezent), Kaltluftdunst `BP_FogBankCard`. | `sehens/lava/…` |

### bergwald

| Frage / Entscheidung | Umsetzung | Datei |
|---|---|---|
| Mönch aus `veqnci0db_tier_2`: ja, erster Wurf | Dazu kommen Sockel und Schutt aus `Basalt_Basalt_Cliff_Rock_A_SM`, `Basalt_Basalt_Rock_C/D_SM` und `vdssailfa_tier_2`, getönt mit `MI_EL_SW_Granit_Moos`. Das Prüfbild entscheidet. | `sehens/bergwald/katalog.md`, `asset_bedarf.json` |
| Nicht-Nanite-Nadelbäume liegend (Windwurf) und 2,5× (Säulenhain): ja | Vermerkt. Forest Cretaceous ist ganz gestrichen (Ferat: teuer, sehr schlecht bewertet). Neu als Kleinzeug: `SM_Forest_pine_04_01/02/03_log`. | `sehens/bergwald/…`, `sehens-downloadliste.md` |
| Karsee-Stempel ±6 m: ja | Vermerkt. | `sehens/bergwald/katalog.md` |
| (Nachtrag Ferat) Landschaftsform frei anpassbar | Geländestempel sind **keine feste Grenze**, auch über 40 m hinaus (bisher SEHENS_FORMAT §3: \|Δ\| ≤ 40 m, mehr nur begründet). Die Planer dürfen die Form dort anpassen, wo der Ort sie braucht; die übrigen Regeln aus §3 gelten weiter (weicher Rand, Wege und Wasser schonen, keine Überhänge im Gelände). | diese Datei; SEHENS_FORMAT pflegt der Koordinator |

### Nachträge von Ferat und B4/B5/B8 (während der Arbeit)

- **Nature Water FX** ist gekauft, der Import steht aus. In den Katalogen von bergwald_05, fjord_02/_04, frost_01, dschungel_02, gletscher_06,
  elfenwald_04/_05 und aue_07 vermerkt. Die Systemnamen folgen mit dem nächsten Inventar.
- **Gestrichen:** Realistic Waterfall VFX und Waterfall Pro.
- **Forest Cretaceous** steht unter „Bewusst nicht aufgenommen“.
- **Megascans** gelten als „kostenlos (2024 beansprucht)“.
- **Wird geladen:** Desert Western Cliff, weitere Limestone-Assets und Ancraite „Limestone Rock Set“.
- **Merge B4:**
  - Die entfallenen Gletscher- und Fjord-Wünsche sind aus der Liste genommen.
  - Brandungsgrotte fjord_07 gegen eine Küsten-Grotte: kueste hat keine Grotte (kueste_01–08 ohne Höhle) → keine Dopplung, fjord_07 bleibt.

## Nachträge Ferat (Chat)

Quelle: `sehens-STATUS.md`, Abschnitt „Entscheidungen Ferat (Chat, 11.10. nachmittags)“.

- **Gelände darf frei angepasst werden.** Die Landschaftsform ist keine feste Regel; Geländestempel dürfen auch über 40 m gehen (Beispiel
  −48 m unter dem Nadeltor, kueste_03). Die übrigen Regeln aus SEHENS_FORMAT §3 bleiben: weicher Rand, Wege und Wasser schonen, keine
  Überhänge im Gelände.
- **Klippensteig (Küste) voll bauen:** 4,35 km plus Kap-Pfad (Entscheid Koordinator).
- **Nature Water FX ist gekauft.** Import und Inventar folgen. Eingeplant für Gischt und Wasserfälle an Seefall, Blasloch, Schleierfall,
  Schleierwand und Eisfall.
- **Megascans sind 2024 beansprucht** und damit kostenlos. Desert Western Cliff Layered, weitere Megascans-Limestone-Assets und das kostenlose
  „Limestone Rock Set“ (Ancraite) werden geladen.
- **Forest Cretaceous ist gestrichen** (teuer, schlecht bewertet). Riesenbäume bleiben Bestand plus Skalierung.
- **Brushify – Moorlands Pack ist gestrichen:** Ferat besitzt es nicht und findet es zu teuer.
  - Für Ginster, Wacholder und Wollgras bleibt der Ersatz aus dem Bestand: Sanddorn, gestauchte Jungkiefern, Binsen.
  - In `sehens/heide/asset_bedarf.json` steht an jedem Brushify-Wunsch `status_13b`: „gestrichen (Ferat: zu teuer)“.

## Offene Restfragen

1. **Lava-Wände:** `SM_lava_wall_01–09` fehlen im neuen `netze.csv`. Kommen sie mit der laufenden Lava-&-Volcano-Nachladung zurück? Bis
   dahin planen die Lava-Orte mit Basalt-Ersatz.
2. **Material-Fix:** Behalten die Megascans-Eisnetze ihr `M_MS_Base_Trm` mit Durchscheinen, oder stellt der Fix für `sw_*` auf
   `M_EL_Fels_MS` um? Und dürfen Instanzen auf `M_EL_Klippe_RVT` für Basalt dessen eigene Texturen bekommen (`MI_EL_SW_Basalt_Saeule`,
   `MI_EL_SW_Granit_Moos`)?
3. **Nebel-Blueprints:** Darf der Planer `BP_FogBankCard`/`BP_FogBankVolume` (NiagaraExamples/FX_Fog) als Akteure setzen? Sonst bleibt
   Nebel bei `lokaler_nebel` (§6). B5 hat ebenfalls keinen Nebel-Niagara gefunden.
4. **Tiere als Detail:** Fische (`SM_Fish_Trout/Perch`) in klaren Gewässern und Ameisen (`SM_Anthill`, `SM_anthill_ants_anim_*`) sind als
   optional eingeplant. Ist das mit „nur Landschaft“ vereinbar, oder sollen sie raus?
5. **Fehlgeschlagene Downloads:** Welche Assets stecken hinter `61882812-…` und `6676d940-…`? Aus unserer Liste lässt sich das nicht
   eindeutig zuordnen.
6. **Pfade:** Der Koordinator trägt in `sehens-STATUS.md` nach, welche Steige jetzt in `standorte.json` stehen. Die alten
   `standorte_*.json` sind laut README abgelöst; die Kataloge verweisen noch auf sie.
7. **Mönch:** Granitnadel auf Basaltsockel ist geologisch ein Bruch. Reicht die Tönung (`MI_EL_SW_Granit_Moos`), oder soll der Sockel nur
   aus Klippenstücken bestehen? Das Prüfbild entscheidet.
