# Verbindliche Konventionen für alle Verteilungs-Planer (Korrektur Runde 1, 10.10.2026)

Gilt für alle zwölf Planer in `antworten/skripte/` (felsgruppen, mittelschicht, spuren, nordkueste, aue, heide_tundra, hochgebirge,
elfenwald, sumpf, dschungel, lava, wueste_ergaenzung). Grundlage: `auftraege/verteilung-korrektur-runde1.md` und `vorlagen/FORMAT.md`.

## 1. Zuständigkeit strikt nach Biom-Zellen

- Biom je Zelle: `eigner.r8` + `welt.json["kacheln"][k]["rezept"]`. Kennzahl **0 = Weltgelände → `aue`**, Vulkanregion → `lava`.
  Nur wenn `eigner.r8` fehlt, gilt als Fallback das dominante Feldbiom aus `daten/biome_je_feld.json` (mit Hinweis im Log).
- Jeder Biom-Planer hat eine feste Liste `biome_eigen` (z. B. nordkueste = fjord, kueste, bergwald; aue = aue; heide_tundra = heide, tundra;
  hochgebirge = gletscher, frost; elfenwald = elfenwald; sumpf = sumpf; dschungel = dschungel; lava = lava; wueste_ergaenzung = wueste, canyon, oedland).
- Bebaut werden nur Zellen, deren Biom in `biome_eigen` liegt, plus ein **weicher Übergangssaum von 30 m** nach außen: Dichtefaktor fällt linear
  von 1 (an der Biomgrenze) auf 0 (30 m außerhalb). Berechnung über Distanztransformation der Zuständigkeitsmaske (NumPy, z. B. iterative
  Dilatation oder separierbare Minimum-Filter), keine Python-Zellschleifen.
- Ist der Anteil der eigenen Biome im Fenster (Feld + Rand) **< 2 %**, schreibt der Planer einen **leeren plan.json** (`instanzen: 0`, keine f32)
  und meldet das in einer Zeile. Nie mit Text statt plan.json beenden.
- Bezug für Anteil und Saum sind die **Landzellen** des Fensters (ohne `karte_wasser`), damit Meer/Seen mit Kennzahl 0 den aue-Anteil nicht
  aufblähen und keinen Saum ins Wasser ziehen. Der Planer nennt den Bezug in `plan.json["biome_fenster_bezug"]` (z. B. "land"). Ergänzt nach aue-Korrektur.
- Querschnitts-Planer (felsgruppen, mittelschicht, spuren) sind für alle Biome zuständig (`biome_eigen` = alle 15), wählen aber Palette und
  Dichten je Zelle nach Biom.

## 2. plan.json: zusätzliche Pflichtschlüssel (alle Planer)

```
"biome_fenster":   {"lava": 0.968, "bergwald": 0.03, ...}   # Anteile aller Biome im Fenster, Summe ≈ 1
"zellen_zustaendig": 123456                                 # Zellen im Feld (ohne Rand), die der Planer bebauen darf (inkl. Saum)
"biome_eigen":     ["fjord", "kueste", "bergwald"]
"kollision_anzahl": 1234                                    # Instanzen mit kollision=true (Deckel 3 000)
```
Weiterhin `instanzen`, `dateien` (mit `ebene`), `entfernen`, `ft_ordner`, `ft_praefix` nach FORMAT §3.

## 3. Budget (hart)

- ≤ 60 000 Instanzen je Feld und Planer-Ebene, davon ≤ 3 000 mit Kollision. Überschreitung → deterministische Ausdünnung nach Priorität
  (Hash-basiert), Warnung im Log, nie stillschweigend. Zielwert 45 000–52 000, damit Echtdaten (mehr Bäume als Synthetik) nicht sofort deckeln.
- Kleinzeug (Laub, Zweige, Kiesel) bevorzugt an Landschafts-Gras abgeben, wenn das Budget knapp wird (Hinweis im plan.json `hinweise`).

## 4. Ebenen-Abgrenzung (Doppelungen vermeiden)

- **mittelschicht_plan.py** (Teil D) ist der einzige Planer für die generischen Mittelschicht-Klassen in allen Biomen:
  `strauch, jungbaum, farn, totholz_liegend, totholz_stumpf, totholz_ast, hochstaude, grasbueschel, beere, pilz`.
  Er liest je Biom Palette und Dichtefaktoren aus `mittelschicht_regeln.json["biome"][<biom>]` und zusätzlich, falls vorhanden,
  `mittelschicht_overrides` aus `<thema>_regeln.json` des zuständigen Biom-Planers (gleicher Ordner wie die eigene Regeldatei; Schlüssel:
  `palette` je Klasse, `faktor` je Klasse, `zusatzklassen`). Die Overrides gewinnen.
- **Biom-Planer** (B1–B9) setzen in Schicht 1 **keine** generischen Klassen mehr, sondern nur biomspezifische Sonderformen
  (z. B. Schilfgürtel, Latschen/Krummholz, Heidekraut-Flecken, Lianen/Riesenfarn-Inseln, Moospolster auf Lava, Tang/Treibholz, Dornbusch-Ödland),
  dazu Schicht 0 (Boden), 2 (Baum) und 5 (Wasserkante). Ihre bisherigen generischen Schicht-1-Klassen wandern als `mittelschicht_overrides`
  in ihr Regel-JSON (Palette + Faktor), damit nichts verloren geht. elfenwald behält den Schalter `--mittel zusatz|voll` (Standard `zusatz`).
- **felsgruppen_plan.py** (Teil C) ist der einzige Planer für Felsen > 0,8 m, Felsbänder, Schuttfächer und Geröllsaum; Biom-Planer setzen
  keine fels_block/fels_hero-Klassen, nur `felsgruppen_overrides` (Palette, Faktoren) in ihrem JSON, die felsgruppen_plan.py optional liest.
- **spuren_plan.py** (Teil D) ist der einzige Planer für Spuren von Leben; Biom-Planer liefern `spuren_overrides`.
- Reihenfolge beim Setzen: felsgruppen → Biom-Planer → mittelschicht → spuren (mittelschicht liest die Baum-Ebenen `bestand/`, `elfenwald/`
  usw. als Kronendach, falls vorhanden).

## 5. Ausgabe und Robustheit

- `print()` nur ASCII (keine Umlaute, kein „→“, kein „≤“): Logs werden unter Windows mit cp1252 weiterverarbeitet. Umlaute in Logs als ae/oe/ue/ss.
- Fehlende optionale Dateien → eine Hinweiszeile, weiter; fehlende Pflichtdatei (hoehe.f32, Regeln, netze.csv) → klare Meldung, Exit-Code 2.
- Jeder Lauf deterministisch (zwei Läufe byteidentisch), Laufzeit ≤ 60 s je Feld, keine Unreal-Importe, numba optional.
- Rauchtest in der Cloud nur synthetisch; Echtdaten-Zahlen aus `verteilung-korrektur-runde1.md` als Referenz im Bericht nennen.

## 6. Schema für `zusatzklassen` in Overrides (Nachtrag 10.10. 14:15 UTC)

Biom-Planer dürfen in `felsgruppen_overrides`, `mittelschicht_overrides` und `spuren_overrides` eigene Klassen unter
`zusatzklassen` anlegen (z. B. nordkueste `felsufer`, heide_tundra `blockfeld`, wueste `terrassenkanten`/`felsnadel`,
dschungel `karstfuss`/`karstplatte`, lava Spires, hochgebirge `eis`). Der jeweilige Querschnitts-Planer **muss** diese Klassen
setzen, nur in Zellen des liefernden Bioms (plus Saum). Gemeinsames Mindestschema, alle Schlüssel außer `palette` optional:

```
"<name>": {
  "palette": ["/Game/..."],            # Pflicht, Pfade aus netze.csv
  "rolle": "fels_block",                # Taxonomie-Rolle, steuert Eingraben/Kollision-Standard
  "dichte_je_ha": 4.0,                  # Ziel-Dichte in der zulässigen Maske
  "hang_grad": [20, 60],                # zulässiger Hang
  "hoehe_m": [0, 900],                  # zulässige Geländehöhe
  "wasser_abstand_m": [0, 8],           # Abstand zur Wasserkante (karte_wasser)
  "lagen_min": {"Fels": 60},            # Mindestgewicht 0-255 je Bodenlage
  "kruemmung": "konvex|konkav|egal",
  "massstab": [0.8, 1.4],
  "eingraben_anteil": [0.25, 0.45],
  "gruppe": {"groesse": [1, 4], "radius_m": 6},
  "kollision": true,
  "sichtweite": [0, 0],
  "akteur": false                       # true = als Akteur statt Foliage
}
```
Optional ergänzt (felsgruppen, 10.10.): `"wand_abstand_m": [0, 22]` (Abstand zur Wand ≥ 50°, Rampe [a, b, c, d] möglich) und
`"zonen_faktor": {"fuss": 3, "gipfel": 1.5, "spalte": 0, "wand": 0, "sonst": 1}` mit `"fuss_breite_m": 22` (multipliziert `dichte_je_ha` je Geländezone).
`"z_versatz_anteil": 0.85` (Zahl oder [lo, hi]): hängendes Stück (Pivot oben, z. B. Eisvorhang) – z = Gelände + Anteil × Netzhöhe × Maßstab, aufrecht, ohne Floating-Prüfung.
Unbekannte Schlüssel werden ignoriert und im Log/`plan.json["overrides"]` gemeldet. Biom-Planer passen ihre bisherigen
Zusatzklassen auf dieses Schema an; Querschnitts-Planer lesen es tolerant.
