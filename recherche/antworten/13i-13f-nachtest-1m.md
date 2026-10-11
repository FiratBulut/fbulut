# Antwort zu Auftrag 13i – Nachtest 13f auf 1 m (Vorfassung: K1–K4)

Stand 12.10.2026. Vorfassung mit den dringenden Punkten K1 und K2, dazu K3 und K4. K5–K8, K10 und die
K9-Teilpunkte folgen. Commit: siehe Commit-Nachricht dieser Datei (Vorfassung).

## K1 – Querprofil schneidet in steile Hänge

**Befund:**
- `rezept._bach_linie` gab `tiefe_max_m` = Maximum über den ganzen Bach an `stempel.bach_profil`.
- `bach.reichweite` machte daraus R bis 30 m. Die 35°-Böschung senkte bis R alles ab, was höher lag.
- An den Linienenden entstanden gerade Radialkanten (`innen` = 0,01 < sp < L − 0,01).

**Änderung (`stempel.bach_profil`, neue Funktion `bach.absenk_grenze`):**
- Außerhalb der Wasserkante (+ 0,5 Zellen Reserve für die bilineare Abfrage in der Bachmitte) senkt das Profil
  höchstens `tiefe + 0,5 m` unter das bisherige Gelände ab.
- Ab Netzrand + Uferring (Uferprüfstelle + 1,5 m) läuft die Grenze über 2 m weich auf 0 aus. R ist damit örtlich
  begrenzt (≤ Uferprüfstelle + 3,5 m), statt aus dem Maximum des Bachs zu kommen. Die Böschung läuft in den Hang aus,
  bei R entsteht keine Wand.
- Zu den Linienenden hin läuft die Absenkung neben dem Bett auf den letzten 2 m weich auf 0 aus; es gibt keine
  Radialkante mehr.
- Das Bett selbst (innerhalb der Wasserkante) bleibt wie in 13f.
- In Fallstrecken (Spiegel folgt der Hülle) gibt es keinen eigenen Fall mehr: Die Fallketten sind zurückgebaut
  (Ferat 13g). Für die 13f-Stufen gilt dieselbe Grenze.
- Der Ufer-Zwang (Uferring, hebt ≤ 2 m) wirkt wie bisher nur bis Netzrand + 1,5 m, danach im 1:2-Auslauf.

**Prüferregel (15e):**
- Der Stempel misst je Bach die Absenkung > 0,3 m außerhalb von Netzrand + Uferring + Böschung + 1 m.
- Er schreibt sie als `profil_absenkung_aussen` in den Bach-Eintrag. Planer und `sehens_pruefen` melden sie als
  FEHLER.
- Eine reine Geländeprüfung im Prüfer trennt die Rezept-Ops (Mulden, Kuppen, Abbrüche) nicht vom Bachprofil. Deshalb
  misst der Stempel selbst.

**Ergebnis:**
- In allen 15 Biomen auf 2 m und synthetisch auf 1 m keine solche Fläche.
- Die Stufen bleiben gleich: `stufen_vergleich.py` gegen c945f93 ergibt 42 von 42 Bächen „gleich“.

## K2 – Pivot in der Netzmitte (SM_Fern_02a halb im Boden)

**Änderung (`instanzen.platziere`, `bezug: mitte`, Fuß ≥ 1,5 m):**
- Gilt bmin_z·sz < −0,25 · Höhe·sz, dann ist z = Boden(Pivot) − eingraben − bmin_z·sz: Die Netz-Unterkante liegt auf
  dem Boden.
- Netze mit Pivot unten verhalten sich wie bisher.

**Selbsttest:** neuer Fall „Pivot in der Netzmitte → Unterkante = Boden − eingraben“.

## K3 – Stück auf der Feldgrenze

**Änderung (`instanzen.Ebene.neu`):**
- Stücke bis 1 cm an einer Feldgrenze rücken 1 cm ins Feld.
- Das Feld kommt aus dem float32-Wert, ohne Rundung auf 0,1 cm. Die alte Rundung machte aus 97 949,992 cm den Wert
  97 950,0 cm und damit G6 statt G5.

**Selbsttest:** y = 97 949,992 cm landet bei 97 949,00 cm in D5 (Testkoordinate).

## K4 – Unerreichbare Mündung

**Änderung (`rezept._bach_ziel`, `_bach_linie`):**
- Bei einem expliziten Epic-Ziel, das nicht erreichbar ist, verwirft der Planer das Ziel und sucht automatisch weiter:
  Tiefenlinie bzw. `versickert` ≥ 25 m.
- Ein Abfluss bekommt nie einen Spiegel über W0: Liegt das Ziel höher, gibt es eine WARNUNG und der Bach wird
  `versickert`.

**Betroffen:** heide_06 `auslauf` ist im Rezept wieder `muendung: auto` (13g, Stufen wie 13f) und endet auf 2 m
`versickert`. Die Stufen aller Bäche bleiben gleich.

## Offen in dieser Vorfassung

- K5–K8, K10 und die K9-Teilpunkte (frost_01 `fuer`, gletscher_01-Furtstrecke, elfenwald_04 `zulauf`) folgen.
- Neue FEHLER kommen aus den Regeln des 13h-Agenten (Kamera, Leuchtfeuer, Steilflächen), nicht aus K1–K4. Sie
  betreffen auch den Selbsttest, Schritt 10 („Leuchtfeuer“ im Test-Ort).
