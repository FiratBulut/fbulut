# Auftrag 24 – Gewässer je Biom nach Erlenbach-Muster (Houdini-Wasser komplett weg), Efeu-Einsatz, Gras unter Felsen, offene Punkte T23k/T11

Stand 25.10.2026 17:15. Bezug: 16f, 16h (+ Nachträge 6a–6t), 19, 20, 22i, 23i, 23.11, verteilung-*.md.

## Kontext

- **Ferat 25.10.:** „Löschen, neu machen – das gilt für alle Houdini-Sachen.“ Präzisiert:
  - Die **Landschaft bleibt**, wie sie ist.
  - **Seen und Flüsse** werden mit Unreal-Werkzeugen gebaut, so wie beim Erlenbach. Der Erlenbach ist die Referenz für Flüsse und Bäche, **angepasst an die verschiedenen Biome**.
  - **Houdini-Wasserelemente kommen komplett weg**, auch die Wasserfälle.
  - Ferat sah in einem See einen zweiten See: vermutlich ein Epic-See plus ein Houdini-Wassernetz.
  - **Straßen bleiben.** Seitenstraßen und Wanderwege kommen erst **nach** den Sehenswürdigkeiten (nicht Teil dieses Auftrags).
- **Erlenbach p2** = Referenz:
  - Shallow Water River (SWR), 788 m, von der Quelle im Berghang bis zur Mündung.
  - Bett per Water-Brush (Blend Min) und Bodenlagen nach 16h.
  - Talkaskade mit Becken, Uferband nach 16h/20, Hindernisse für die Simulation.
  - Gebacken, Darstellung BAKED_SIM.
  - Werte: Nachfüllen 0,3, smoothing_width 1, Zone 4096 bei schmalem Bach.
- **Bestandsaufnahme der Houdini-Reste weltweit** läuft lokal. Ergebnis folgt als Nachtrag.
- **Neu im Projekt:** Fab-Paket „Foliage VOL.23 – Ivy (Low Poly)“ (Dekogon):
  - 49 Efeu-Netze von 0,4 bis 11,6 m, modular für Wände, Felsen und Stämme.
  - 11 Demo-Bauteile (Steinmauern, Säulen, Bögen).
  - 2K-Texturen und eigener Master.

## Fragen

### A. Gewässer je Biom (Hauptfrage)

Biome in Eldarien (siehe `verteilung-*.md`): Aue, Dschungel, Elfenwald, Heide/Tundra, Hochgebirge, Lava, Nordküste, Sumpf, Wüste (Namaqualand), dazu Nordic-Mischwald und Bergwald.

1. Bitte je Biom ein **Regelset für Bäche/Flüsse** im Format der vorhandenen Regeldateien (JSON plus Text):
   - Bettprofil (Breite/Tiefe nach Abfluss oder Einzugsgebiet, Uferstufe, Becken/Stufen nach Gefälle).
   - Bodenlagen im Bett und am Ufer nach Abstand zum Wasser.
   - Steine, Kleinschutt, Totholz und Kantenbelag (Deckungsziele je Zone).
   - Ufervegetation (welche Klassen, Dichte, Abstand).
   - Wasser-Materialwerte für die gebackene Darstellung (Absorption, Streuung, Trübung: Wüste klar, Sumpf braun, Dschungel grünlich, Gletscherbach milchig …).
   - SWR-Parameter, die vom Biom oder der Breite abhängen (Nachfüllen, smoothing, Zonenauflösung nach Regel 6t).
2. Das gleiche für **Seen** als Epic WaterBodyLake: Uferprofil, Flachwasserzone, Schilf/Röhricht, Kies-/Felsufer, Wasserwerte. Wie wird ein Bach an einen See angeschlossen (Zulauf/Abfluss)?
3. **Wasserfälle ohne Houdini:** Welches Unreal-Werkzeug (Niagara aus NatureWaterFX, Epic-Wasser plus Mesh-Vorhang, SWR-Stufe)? Mindestregeln für Fallhöhe und Breite, damit es natürlich wirkt. Ferat wartet seit 12.10. auf Wasserfälle nach Cloud-Plan (Aufträge 175–184 liegen wartend).
4. **Reihenfolge des Rollouts:** Mit welchem Biom nach dem Erlenbach (Nordic) als zweitem Pilot anfangen, damit die Regeln am schnellsten belastbar werden?

### B. Efeu (neues Paket)

5. Wo setzen wir Efeu ein, je Biom?
   - Felswände und -blöcke (welche Exposition und Feuchte), Baumstämme (welche Arten), Ruinen/Mauern.
   - Mengen, Höhengrenzen, Abstand zu Wasser.
   - Wo nie: Wüste, Lava, Hochgebirge?
6. Gibt es eine Sitzregel für Efeu-Netze an Felsen (anliegend, keine Luft, nicht durch Schnee)?

### C. Landschafts-Gras sticht durch Felsen

Aus Gras-im-Fels r001 §3, offen seit 19.10.:

- Die Foliage-Pflanzen mit Fuß im Fels sind weltweit entfernt (35 613).
- Das **Landschafts-Gras** (Grass Types aus Lagen) sticht aber weiter an Felsrändern und durch kleine/flache Steine.
- Eine Sperre über die Bewuchs-Dichten (1-m-Raster, 4096er Textur) lässt im Grundriss 75 % und in der Durchstich-Zone 91 % stehen.
- Mit Rand 0 bleiben 52 %, dafür entsteht ein kahler Hof (≈ 0,5 m² je m² Fels).

7. Welcher Mechanismus in UE 5.8 schließt Landschafts-Gras **feiner als 1 m** unter Fels-Netzen aus? Kandidaten: Grass Exclusion Volumes, RVT-Maske im Grass-Output, Gras an Felsen durch Foliage ersetzen. Gesucht sind Kosten, Persistenz und Auflösung.

### D. Offene Punkte aus der Talkaskade C2 (T23k Hang-Blöcke) und Mündung (T11)

8. **Kragarm-Regel (PM-Entscheidung, bitte bestätigen oder korrigieren):**
   - Hang-Blöcke lagen hangparallel (Median 21,5° zur Senkrechten). 40 von 291 ragten talseitig in die Luft, bis 88 cm im Kern.
   - Die Sitzprüfung misst im lokalen Grundriss, die Talseiten-Grenzen der Regeln fehlen im Referenzcode.
   - Neu, senkrecht von oben gemessen: Kern Bergseite ≤ 5 cm, Talseite ≤ min(0,15·h; 30 cm) **und** höchstens 10 % des Grundrisses mit > 30 cm Luft.
   - Gilt das auch weltweit für die Sitzprüfung v4?
9. **Kante „sichtbar“ ist real 0,556/0,555**, nicht 0,77–0,82 wie in 23f/23i gemeldet:
   - Die früheren Werte enthielten einen nie eingebauten Lagen-Plan.
   - Das Netz-Ziel der Kante (≥ 0,40) ist erfüllt.
   - Reicht das bis zum 16h-Bettschritt, oder soll der Lagen-Plan aus 23f nachgezogen werden?
10. **T11 (6t §5) Ergebnis:**
    - `affects_landscape` am alten Fluss C3/D3_Fluss_F_ERLENBACH_2 = **True** (nicht False wie im Export vom 13.10.).
    - Es gibt keinen WaterBrushManager in der Karte.
    - 30 Höhen vorher/nachher `rebuild_native_body`: max. 0,00 cm Unterschied (Rand, Bett, Kontrolle, Grundrauschen).
    - PIE-Bild nachher: weiter Platte → Urteil **Geometrie**.
    - Zonen C2/C3/D3 4096, D2 1024, Fernfläche überall aus (Grenzen 0,6 km).
    - Folge: Entfernen ist geländeneutral. Der alte Fluss wird entfernt und als SWR-Fortsetzung des p2 neu gebaut (Planung läuft lokal).
    - Gibt es dabei etwas zu beachten (Naht p2 s 788, Mündung ins Hauptgewässer)?

## Erwartete Antwort

- Regeldatei(en) für Gewässer je Biom plus Seen (JSON) und eine Kurzfassung je Biom.
- Efeu-Regeln.
- Empfehlung zum Gras-Mechanismus mit Testablauf.
- Bestätigung oder Korrektur der Punkte 8–10.
- Kein Projekt-Quellcode nötig. Lokale Daten liegen beim PM.
