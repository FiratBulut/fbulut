# Antwort zu Auftrag 13i – Nachtest 13f auf 1 m

Stand 12.10.2026. Bearbeitet: K1–K8, K10, aus K9 frost_01 `fuer`, gletscher_01-Furtstrecke und elfenwald_04 `zulauf`.
Die übrigen K9-Punkte (organische Formen, Terrassen, Kamera bergwald_06) macht der 13h-Agent. K1 bis K4 waren als
Vorfassung schon in `5d88d44` (WIP-Commit) gepusht. Endstand: siehe Commit-Hinweis am Ende.

## Kurzfazit

- **K1 behoben:**
  - Das Querprofil senkt außerhalb der Wasserkante höchstens `tiefe + 0,5 m` ab. Ab Netzrand + Uferring läuft die
    Absenkung über 2 m weich auf 0 aus, zu den Linienenden auch.
  - Bei R entsteht keine Wand mehr, an den Enden keine Radialkante.
  - Jeder Bach meldet seine Absenkung > 0,3 m abseits von Netzrand + Uferring + Böschung als `profil_absenkung_aussen`
    (Prüfer: FEHLER). In allen 15 Biomen ist das 0.
  - gletscher_03: 33 000 m³ weniger Abtrag neben dem Bach, statt bis 65 m tief (2-m-Daten).
- **K2 behoben:** Liegt der Pivot in der Netzmitte (bmin_z·sz < −0,25 · Höhe), steht die Netz-Unterkante auf dem Boden.
- **K3 behoben:** Stücke bis 1 cm an einer Feldgrenze rücken 1 cm ins Feld. Das Feld kommt aus dem float32-Wert.
- **K4 behoben:** Ein unerreichbares Epic-Ziel wird verworfen (automatisch weiter bzw. `versickert`). Ein Abfluss
  liegt nie über dem Seespiegel.
- **K5 behoben:**
  - Der Fuß liegt 0,5 m hinter der Lippe, das Becken ist ab dem Fuß ≥ 3 m lang.
  - Lippe, Höhe und Zahl der Stufen sind gleich (Vergleich gegen c945f93: 30 Bäche „nur Fuß verschoben“, 7 „gleich“).
  - Bei 5 Bächen geht die Schluss-Stufe am See in der letzten Stufe auf.
- **K6 behoben:**
  - Jede Zelle mit |Δ| > 0,3 m bekommt eine Bodenlage. An steilen Stellen ist das der Fels des Bioms, sonst Geröll
    bzw. die Bodenlage des Bioms.
  - Prüferregel aus 15e: eine Zelle ohne Lage ist FEHLER.
- **K7 behoben:** Alle Lagen werden vor dem Schreiben auf höchstens 150 je 1-m-Nachbarzelle begrenzt (nur nach außen
  ergänzt).
- **K8 behoben:**
  - Der Prüfer misst das Seeufer jetzt 1 m außerhalb des Umrisses, alle 0,5 m.
  - Der Planer hält dort mindestens Spiegel + 0,1 m.
- **K9 (meine Teile):** `fuer` von MI_EL_SW_Schwarzeis nennt nur noch Netze. Die Seen stehen in `fuer_wasser`. Steile
  Furtstrecken (> 15 %) werden `durchlass`.
- **K10:** in der synthetischen 1-m-Welt 0 FEHLER.
- **Ergebnis:** In meinen Punkten 0 FEHLER auf 2 m und synthetisch auf 1 m, siehe „Prüfergebnis“.
- **Was noch FEHLER meldet:**
  - die neuen 13h-Regeln (Kamera, Leuchtfeuer, Steilflächen); ihre Behebung macht der 13h-Agent;
  - auf 2 m kueste A5: ein Kiesel im Meer, Ursache noch offen (s. u.).

## K1 – Querprofil schneidet in steile Hänge

**Befund wie beschrieben:**
- `tiefe_max_m` war das Maximum über den ganzen Bach. Daraus machte `bach.reichweite` ein R bis 30 m.
- Die 35°-Böschung senkte bis R alles ab. Bei R stand eine Wand, an den Linienenden gab es Radialkanten.

**Änderung (`bach.absenk_grenze`, `stempel.bach_profil`):**
- Innerhalb der Wasserkante (+ 0,5 Zellen für die bilineare Abfrage in der Mitte) gilt das Bett wie in 13f.
- Außerhalb ist die Absenkung auf `tiefe + 0,5 m` unter dem bisherigen Gelände begrenzt. Ab Uferprüfstelle + 1,5 m
  (Netzrand + Uferring) läuft sie über 2 m weich auf 0. Damit ist R örtlich und nicht mehr das Maximum des Bachs.
- Auf den letzten 2 m zu den Linienenden läuft die Absenkung neben dem Bett ebenfalls weich auf 0.
- Der Uferring hebt wie bisher nur bis Netzrand + 1,5 m und läuft danach 1:2 aus.
- Fallketten gibt es nicht mehr (13g); für die 13f-Stufen gilt dieselbe Grenze.

**Prüferregel wie 15e:**
- `stempel.bach_profil` misst je Bach die Absenkung > 0,3 m außerhalb von Uferprüfstelle + 1,5 m + 0,5/tan 35° + 1 m.
  Sie steht als `profil_absenkung_aussen` im Bach. Planer und Prüfer melden FEHLER.
- Der Stempel misst selbst, weil der Prüfer im Gesamt-Delta die Rezept-Ops (Mulden, Kuppen, Abbrüche) nicht vom
  Bachprofil trennen kann.
- Ergebnis: in allen 15 Biomen 0 m².

**Wirkung auf 2 m** (Abtrag weniger als in c945f93, Zellen > 4 m vom Bach; das Gesamt-Delta enthält auch die
13h-Böschung):

| Ort | weniger Abtrag | alter Stand dort tiefer |
|---|---|---|
| gletscher_03 Moränensee | 33 249 m³ | 2 884 m², bis 64,9 m |
| fjord_02 Schleierwand | 1 832 m³ | 1 260 m², bis 11,8 m |
| gletscher_06 Gletschertöpfe | 1 541 m³ | 2 257 m², bis 6,4 m |
| canyon_04 Flüsterschlucht | 1 538 m³ | 582 m², bis 8,2 m |
| elfenwald_05 Farnschlucht | 1 057 m³ | 638 m², bis 7,7 m |
| fjord_04 Hängetal | 609 m³ | 808 m², bis 12,4 m |

Bei bergwald_06 und wueste_04 überwiegt die neue 13h-Böschung bzw. das gehaltene Seeufer (K8). Das ist kein Abtrag
durch das Bachprofil.

**Hinweis zur Doppelarbeit:**
- Der 13h-Agent hat parallel `steilwand.bach_einschnitt_begrenzen` eingebaut (dieselbe Grenze, nachträglich auf das
  Delta).
- Beide greifen zusammen und widersprechen sich nicht: Seine Kernzone ist breiter als meine Bettzone.
- Später kann eine der beiden wegfallen.

## K2 – Pivot in der Netzmitte

- `instanzen.platziere`, `bezug: mitte`, Fuß ≥ 1,5 m: Gilt bmin_z·sz < −0,25 · Höhe, dann z = Boden(Pivot) − eingraben −
  bmin_z·sz. Die Netz-Unterkante liegt auf dem Boden.
- Netze mit Pivot unten verhalten sich wie bisher.
- Selbsttest: Netz mit Pivot in der Mitte → Unterkante = Boden − eingraben.

## K3 – Feldgrenze

- `instanzen.Ebene.neu`: Stücke ≤ 1 cm an einer Feldgrenze rücken 1 cm ins Feld; das Feld kommt aus dem float32-Wert.
- Die alte Rundung auf 0,1 cm machte aus 97 949,992 cm den Wert 97 950,0 und damit das Nachbarfeld.
- Selbsttest mit genau diesem Wert.

## K4 – Unerreichbares Ziel

- `_bach_ziel`: Ist ein explizites Epic-Ziel nicht erreichbar, wird es verworfen. Dann gilt die automatische Suche:
  Tiefenlinie bzw. `versickert` ≥ 25 m.
- `_bach_linie`: Liegt das Ziel eines Abflusses über dem Seespiegel, gibt es eine WARNUNG und der Bach endet
  `versickert`; ein Spiegel über W0 kommt nie vor.
- heide_06 `auslauf` steht im Rezept wieder auf `muendung: auto` (13g, Stufen wie 13f). Er beginnt auf dem Seespiegel
  und endet auf 2 m `versickert`.
- Die Stufen bleiben gleich, weil der Fall bei keinem anderen Bach auftritt.

## K5 – Becken < 3 m

**Befund:**
- Der Fuß lag „eine Probe hinter Lippe + 0,5 m“ (`searchsorted`). Bei Proben unter 0,5 m Abstand wurde daraus 1 m,
  und das Becken danach war nur 2,5 m lang.
- Dazu kam die Schluss-Stufe direkt hinter einer Stufe.

**Änderung (`bach.treppe`):**
- Der Fuß liegt an der Probe, die Lippe + 0,5 m am nächsten liegt. Das Becken zählt ab dort, die nächste Lippe liegt
  ≥ 3 m dahinter.
- Spiegel und Stufenhöhe bleiben wie 13f: Der Spiegel springt auf derselben Probe wie bisher, die Höhe wird an der
  bisherigen Fuß-Probe gemessen. Lage (Lippe), Höhe und Zahl bleiben also gleich, nur der Fuß rückt bis 0,5 m näher an
  die Lippe.
- Die Schluss-Stufe am See wird nur gesetzt, wenn davor ≥ 3 m Becken bleiben. Sonst geht sie in der letzten Stufe auf:
  Lippe und Oberwasser bleiben, der Fuß kommt ans Ende auf den Seespiegel.
- Die Stufenzone im Prüfer reicht unterhalb weiter um 0,5 m, wie in 13f mit dem alten Fuß.

**Stufenvergleich** (`stufen_vergleich.py`, neue Klassen „fuss“ und „schluss“, 2 m gegen c945f93):

| Klasse | Bäche | Bedeutung |
|---|---|---|
| gleich | 7 | identisch |
| fuss | 30 | Lippe, Höhen, Zahl gleich; Fuß bis 51 cm näher an der Lippe |
| schluss | 5 | wie fuss, Schluss-Stufe in der letzten aufgegangen: bergwald_06 `zulauf_sued`, `zulauf_west`, elfenwald_04 `zulauf`, fjord_04 `hochtalbach`, gletscher_06 `klammbach_2` |
| anders | 0 | – |

## K6 – Geänderte Zellen ohne Bodenlage

- `rezept._lagen_delta_decken`, am Ende von `lagen_bauen`. Das Lagenfenster entsteht jetzt auch ohne Rezeptlagen,
  sobald |Δ| > 0,3 m vorkommt.
- Wo |Δ| > 0,3 m ist und die Lagen zusammen < 60 von 255 haben:
  - steil (> 35°, weich ab 30°): Fels des Bioms (Lavafels in lava, Sandstein in canyon, sonst Fels);
  - flach: Geröll, in wueste Sand, in lava Lavasand, in sumpf Schlamm, in aue Erde;
  - Gewicht weich nach |Δ| 0,15–0,45 m.
- Prüfer (`sehens_pruefen`, Regel 15e): Zellen mit |Δ| > 0,3 m ohne Lage sind FEHLER.

## K7 – Harte Lagenkanten

- `stempel.kanten_weich` vor dem Schreiben jeder Lage (1 m): höchstens 150 je Nachbarzelle, diagonal 150·√2.
- Es wird nur nach außen ergänzt, der Kern bleibt. Das gilt für alle Formen, auch „fleckig“, kleine Ringe und
  `um_gruppe`.
- Das Pfadband (Erde, 1 m Übergang) bleibt wie in 13f vorgesehen. Wo es 255 erreicht, wird es auf ≥ 2 Zellen
  weich.

## K8 – Seeufer

- **Prüfer** (`sehens_pruefen.ufer_1m`):
  - Proben 1 m außerhalb des Umrisses entlang der äußeren Normale, alle 0,5 m, wie euer Prüfer.
  - Ausgenommen sind Zu- und Abflüsse (erste/letzte 6 m) und das Wasser eines Bachs am Ufer.
  - Auf 1 m FEHLER. Auf 2 m WARNUNG, Probe bei 1,75 m, weil die Probe bei 1 m dort die Seezelle mitmischt.
- **Planer** (`rezept._seeufer_halten`, nach den Bächen, vor `fertig`):
  - Das Band bis 1 m + 0,75 Zellen hinter dem Umriss kommt auf mindestens Spiegel + 0,1 m, danach 1:2 auslaufend,
    nur anheben.
  - Zu- und Abflüsse sowie Bachwasser bleiben offen.
- **Ergebnis:**
  - dschungel_05 und tundra_05 auf 2 m und 1 m ohne Meldung;
  - auf 2 m bleibt eine WARNUNG bei bergwald_06 `karsee` neben dem Abfluss (4 Proben, bis 0,34 m; geschützte
    Bestandswasser-Zellen). Auf 1 m ist sie weg.
- Beim Karsee hebt der Planer neben der Karschwelle bis 6,2 m an. Dort hielt bisher nur der Damm.

## K9 – meine Teile

- **frost_01 `MI_EL_SW_Schwarzeis`:**
  - `fuer` ist jetzt leer, denn das Material liegt auf Seeflächen und nicht auf Netzen.
  - Neues Feld `fuer_wasser`: `frost_02_frostsee/frostsee`, `frost_05_blockgletscher/blasensee`,
    `frost_07_frostblumen/lagune`. Es wird in `orte.json` übernommen; die Beschreibung steht in `hinweis`.
- **gletscher_01 `gletscherbach`, Furtstrecke:**
  - Jede Furt hat jetzt `gefaelle_pct` und `art`.
  - Ab 15 % ist sie `art: durchlass`: Das Wasser läuft unter dem Weg durch (Rohr/Durchlass), dort gibt es keine
    Wasserfläche und keinen Wasserfilm am Steilhang. Das betrifft gletscher_01 (57 %).
  - elfenwald_04 `zulauf` (9 %) bleibt eine Furt.
  - Spiegel und Stufen sind unverändert.

## K10 – Reste im Querprofil

- gletscher_06 `klammbach_oben`, dschungel_02 `quellbach`, wueste_04 `rinnsal`: Reserve über
  - den Uferring + 0,2 m (hebt ≤ 2 m),
  - die aufgefüllte Wasserkantenzelle,
  - die unbegrenzte Bettzone + 0,5 Zellen (K1).
- In der synthetischen 1-m-Welt sind alle drei ohne Meldung. Auf den echten 1-m-Daten bitte nachprüfen.

## Prüfergebnis

(Endstand siehe unten; FEHLER aus den 13h-Regeln „Kamera“, „Leuchtfeuer“, „neu steil ohne Fels-Akteur“ sind
ausgeklammert.)

ERGEBNIS_PLATZHALTER

## Offen / Rückfragen

1. **kueste A5, `SM_NordicBeachRock_01` im Meer (2 m, 1 Instanz):**
   - Der Fehler ist neu seit diesem Stand. Er gehört zu keinem der K-Punkte direkt: kein Bach, K2 betrifft nur
     Fuß ≥ 1,5 m.
   - Vermutlich verschiebt das geänderte Gelände (K8-Ufer bzw. 13h-Böschung) die Zufallsplatzierung des Kleinzeugs.
   - Bitte lokal auf 1 m prüfen; ich sehe es mir an, sobald 13h fertig ist.
2. **Doppelte K1-Begrenzung** (mein `bach.absenk_grenze` und `steilwand.bach_einschnitt_begrenzen` aus 13h): Welche soll
   bleiben?
