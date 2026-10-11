# Antwort zu Auftrag 15b – Korrektur nach dem 1-m-Test: Ufer am Kaskadennetz-Rand

Stand 11.10.2026. Die korrigierte Fassung ist Commit **`93ca592`**. Der Planer-Code steht in `4257017`, `93ca592`
enthält ihn. Die Vorfassung `4600fb1` (nur C2) ist damit überholt.

## Kurzfazit

- **Die Ursache ist bestätigt.** Der Stempel senkte das Gelände genau an der Netzkante. Es kamen vier Ursachen zusammen,
  siehe Abschnitt 1.
- **Gewählt ist Variante „Bett schmaler“.**
  - Die Wasserkante liegt 0,3–0,5 m innerhalb der halben Breite. Die Böschung steigt mit 35° durch die Wasserkante,
    ein Uferring liegt auf Spiegel + 0,15 m.
  - Bett und Kolke sind nie breiter als das Netz. Das Netz endet immer auf der Böschung über dem Spiegel.
- **1-m-Test:**

  | Prüfung | Läufe | Beckenpunkte | FEHLER vorher | FEHLER nachher |
  |---|---|---|---|---|
  | Pilotläufe auf den 1-m-Fenstern | 19 | 1 502 (Ufer links/rechts, Bett) | 29 | **0** |

  - Zwei Läufe ergeben byteidentische Ausgaben.
  - Es bleibt 1 WARNUNG „Bestand“ bei F_ERLENBACH_2V_D3: An 2 Proben liegt das alte Ufer 1,3 m unter dem neuen
    Spiegel.
- **Alle 161 Strecken auf 2 m:** 0 FEHLER, 27 WARNUNG. Das sind Niagara-Grenze, Beckengefälle 2–3 % und Bestand.
- **Neue Option `--hoehe1m-fenster DIR`** für Planer und Prüfer. Bett- und Uferprüfung rechnen damit exakt auf 1 m:
  altes Gelände aus den Fenstern + 1-m-Delta, bilinear.

## 1. Ursache (bestätigt)

1. **Stufe im Querprofil an der Wasserkante.**
   - Das Bett lag bis zur halben Breite flach (Kern = 0,5 · Breite = halbe Breite). Der Übergangsbereich war damit
     leer, und gleich daneben sprang das Gelände auf Spiegel + 0,05 m.
   - Das 1-m-Gelände ist bilinear. Der Netzrand (halbe Breite + 0,4 m) liegt zwischen einer tiefen Bettzelle und einer
     Uferzelle und landete deshalb auf oder unter dem Spiegel.
   - Auf 2 m war es noch schlimmer: Das Delta wurde von 2 m auf 1 m interpoliert. Mit dem alten Planer lagen auf den
     1-m-Fenstern bei C2 10 von 15 Beckenpunkten zu tief.
2. **Projektion auf die nächste Laufstelle an Stufen.** Zellen neben dem Oberbecken, die schon hinter der Lippe
   liegen, bekamen das Profil des Unterbeckens. Das Ufer wurde dort um die Fallhöhe abgesenkt.
   - Beispiel C2 k = 63: Das Ufer liegt 6 m tiefer.
3. **Fortsetzung als „Zufluss“.**
   - F_ERLENBACH_3_D3, der 75 m breite Nachfolger von D3, beginnt am Ende von D3. Er wurde als Zufluss erkannt, und
     sein „Endstück“ wurde als 75 m breite Rinne auf 11,12 m gestempelt.
   - Das ist die ebene Fläche bei k = 74/81: beidseitig 11,12 m. Es ist ein echter Fehler, wie im Auftrag vermutet.
   - Ebenso erkannt wurde F_ERLENBACH_1_C2 als Vorgänger am Anfang von C2.
4. **Breitensprünge** an Wandzonen (Klamm-Sohle, Becken) bis 1,5 m auf wenigen Metern. Ein Netzpunkt mit schmaler
   Breite hatte neben sich eine breitere Absenkung.

Dazu kam der Prüfer: Er zählte „Bestand“ schon dann, wenn das alte Ufer unter dem **alten** Spiegel lag. Bei D3 ist
das immer so, weil das Epic-Wasser über dem Gelände liegt.

## 2. Was geändert wurde

Alles steht in `skripte/gefaelle/gefaelle_plan.py`, `gefaelle_pruefen.py` und `gefaelle_daten.py`. Die Lib ist
unverändert.

1. **Querprofil (`profil_T`, `wasserkante`).**
   - Die Wasserkante liegt bei halbe Breite − min(0,5 m; max(0,3 m; 0,3 · halbe Breite)).
   - Die Böschung steigt mit 35° unter Wasser bis zum Spiegel und darüber weiter. Außerhalb der halben Breite gilt
     mindestens die Uferwand mit dem Uferwinkel (Uferklippe, Fall, Klamm steiler).
   - Bettbreite = Breite − 2 · (Tiefe / tan 35° + Kantenabstand). Kolke sind dadurch nie breiter als das Wasser.
   - **Begründung für diese Variante statt „Netz = nasse Breite“:**
     - Das Netz bleibt so breit wie die River-Splines ober- und unterhalb. Es gibt keine Breitensprünge an der
       0,5-m-Überlappung und kein Netz, das in alte Mulden ausläuft (D3).
     - Das Wasser endet an einer flachen Böschung, wie an einem echten Bach. Das Netz verschwindet 0,7–0,9 m hinter der
       Wasserkante unter dem Ufer.
     - Die Werte sind auf 1 m sicher: Bei bilinearer Abfrage ergibt das Profil am Netzrand im ungünstigsten Fall
       Spiegel + 0,13 m bei 0,5 m Kantenabstand und Spiegel + 0,10 m bei 0,3 m (schmale Bäche). Nachgerechnet ist das
       über alle Rasterlagen und Richtungen.
2. **Uferring (`ring_ziel`).**
   - Ab der Wasserkante steigt der Ring mit 35° auf Spiegel + 0,15 m und bleibt so bis Netzrand + 1,5 m. Danach läuft
     er 1:2 aus.
   - Er hebt nur, wo das Gelände zu tief ist, höchstens um 1 m.
   - Neben dem Fuß einer Stufe gilt außerhalb der halben Breite 1,5 m lang der Oberwasser-Spiegel (`ufer_z`). Das ist
     die Seitenwand des Falls. Der Stempel senkt das Ufer an der Netzkante so nie unter Spiegel + 0,1 m.
3. **1-m-Feinschliff (`feinschliff_1m`).**
   - Das Delta wird auf dem 1-m-Ausgaberaster gegen das alte 1-m-Gelände nachgezogen: im Wasser exakt das Querprofil,
     außen der Uferring.
   - Die Schutzfaktoren für Orte, Wege, fremdes Wasser und Fensterrand gelten weiter. Zufluss-Mündungen bleiben offen.
   - Lokal ist das alte Gelände die 1-m-Welt selbst. In der Cloud kommt es aus `--hoehe1m-fenster`, sonst aus 2 m
     bilinear.
   - Die geschriebene `gelaende/*.f32` ist dieses 1-m-Delta.
4. **Breite** ändert sich höchstens um 0,2 m je m. Es wird nur verbreitert, nie verengt.
5. **Fortsetzungen** desselben Gewässers sind keine Zuflüsse mehr. Das gilt für einen Vorgänger, der am Anfang endet,
   für einen Nachfolger am Ende und für Abzweige. Sie bekommen kein Endstück und keine Rinne.
6. **Beckenpunkte dicht.** Das Kaskadennetz beschreibt Becken jetzt alle ≤ 2 m. Bei C2 sind es 63 statt 15 Punkte.
   Netzrand, Bett- und Uferprüfung erfassen damit das ganze Becken.
7. **Prüfer.**
   - Das Bett wird über die mittleren 60 % der Breite gemittelt (nasses Bett), statt über 90 %.
   - „Bestand“ zählt nur noch, wenn das **alte** Ufer an derselben Stelle tiefer liegt als neuer Spiegel + 0,1 m − 1 m,
     also auch der Uferring es nicht erreichen kann. Alles andere ist FEHLER. Das gilt im Planer und in
     `gefaelle_pruefen.py`.
8. **Bettfehler B_R_P4_M2_04_KN0** ist behoben. Ursachen waren die Uferzellen der 15-m-Fallwand in der Bettmittelung
   und der Oberwasser-Ring innerhalb der Wasserbreite. Jetzt: 0 von 235 Beckenpunkten.

## 3. Ergebnis je Lauf auf 1 m

Die Spalten bedeuten:

- **Befund 15b:** Ufer-Proben zu tief, lokal, alter Planer (ac4da85).
- **vorher Cloud:** alter Planer (7c522eb), geprüft mit `--hoehe1m-fenster`. Angegeben sind Ufer / Bett zu tief und
  die FEHLER.
- **nachher:** Fassung 93ca592, ebenfalls mit `--hoehe1m-fenster`.

| Lauf | Befund 15b (max. fehlt) | vorher Cloud: Ufer / Bett | FEHLER vorher | Beckenpunkte nachher | nachher: Ufer / Bett | Bestand | FEHLER nachher |
|---|---|---|---|---|---|---|---|
| F_ERLENBACH_1V_C2 | 6 (0,86 m) | 10 / 0 | 1 | 63 | 0 / 0 | 0 | **0** |
| F_ERLENBACH_2V_D3 | 5 (3,53 m) | 4 / 0 | 1 | 24 | 0 / 0 | 2 | **0** |
| B_R_P3_M2_01 | 16 (0,45 m) | 8 / 0 | 2 | 157 | 0 / 0 | 0 | **0** |
| B_R_P1_M2_01 | 7 (0,44 m) | 11 / 0 | 1 | 140 | 0 / 0 | 0 | **0** |
| F_ELFENFLUSS_3_H4 | 7 (0,25 m) | 8 / 0 | 1 | 55 | 0 / 0 | 0 | **0** |
| B_R_P0_M2_02 | 2 (0,20 m) | 5 / 0 | 2 | 83 | 0 / 0 | 0 | **0** |
| B_R_P5_P1_03 | 4 (0,18 m) | 3 / 0 | 1 | 58 | 0 / 0 | 0 | **0** |
| B_R_P4_M2_04 | 11 (0,15 m) + Bett 3 von 31 | 21 / 2 | 4 | 235 | 0 / 0 | 0 | **0** |
| B_R_M3_P1_01 | 11 (0,14 m) | 5 / 0 | 1 | 89 | 0 / 0 | 0 | **0** |
| B_R2_R_M1_M1_02 | 3 (0,10 m) | 4 / 0 | 1 | 39 | 0 / 0 | 0 | **0** |
| B_R_P0_M2_03 | 5 (0,09 m) | 7 / 1 | 2 | 118 | 0 / 0 | 0 | **0** |
| B_R_P0_M2_04 | 2 (0,08 m) | 4 / 0 | 2 | 43 | 0 / 0 | 0 | **0** |
| B_R_P5_P1_05 | 3 (0,07 m) | 3 / 0 | 2 | 45 | 0 / 0 | 0 | **0** |
| B_R_M2_P1_02 | 3 (0,05 m) | 7 / 0 | 1 | 78 | 0 / 0 | 0 | **0** |
| B_R_P4_M1_03 | 3 (0,03 m) | 5 / 0 | 1 | 71 | 0 / 0 | 0 | **0** |
| B_K8_ELFENFALL_01 | 0 | 3 / 1 | 3 | 116 | 0 / 0 | 0 | **0** |
| B_R_P0_M2_01 | 0 | 5 / 0 | 1 | 52 | 0 / 0 | 0 | **0** |
| B_R_P1_M2_03 | 0 | 6 / 0 | 1 | 27 | 0 / 0 | 0 | **0** |
| B_R2_R_P0_M2_01 | 0 | 1 / 0 | 1 | 9 | 0 / 0 | 0 | **0** |
| **Summe** | **88** | **120 / 4** | **29** | **1 502** | **0 / 0** | **2** | **0** |

Anmerkungen:

- **Vorher-Werte:** Die Cloud-Werte stammen aus den damals dünnen Beckenpunkten (meist 1–3 je Becken). Der lokale
  Befund hat mehr Punkte, weil die 1-m-Daten mehr Spiegelpunkte haben.
- **Bestand bei D3 (k = 32/33):** Das alte Ufer liegt dort bei 22,0–22,2 m, der neue Spiegel bei 23,5 m. Das
  Epic-Wasser lag hier schon über dem Gelände, und mehr als 1 m Anheben ist nicht erlaubt. Deshalb nur WARNUNG.
- **Zufluss-Mündungen:** Dort ist das Ufer offen und wird nicht geprüft. Das betrifft B_R_P1_M2_01 und B_R_P3_M2_01.

## 4. Aufruf für Claude lokal

```
# Pilotläufe auf 1 m (wie bisher, Ausgabe export/unreal/welt/gefaelle/<lauf>/)
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis .
# nur C2
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --basis . --laeufe F_ERLENBACH_1V_C2
# Prüfer allein
python -I recherche/antworten/skripte/gefaelle/gefaelle_pruefen.py export/unreal/welt/gefaelle --daten1m export/unreal/welt
```

Lokal ist keine neue Option nötig. Der Feinschliff rechnet gegen die 1-m-Welt, und die Prüfung ist auf 1 m ohnehin
exakt.

**Wichtig für das Einbau-Werkzeug:**

- Die `mittellinie` hat jetzt in den Becken alle ≤ 2 m einen Punkt.
- Die Netzbreite bleibt `breite` + 2 × 0,4 m. Ein adaptiver Netzrand ist nicht mehr nötig, schadet aber nicht.
- Das Gelände-Delta `gelaende/*.f32` muss **vor** dem Netz eingebaut werden.

Cloud-Test (2-m-Daten, 1-m-Fenster):

```
python -I recherche/antworten/skripte/gefaelle/gefaelle_plan.py --daten2m recherche/vorlagen/daten/sehens \
    --hoehe1m-fenster recherche/vorlagen/daten/gefaelle/hoehe_1m_fenster --aus <scratchpad>/a15b/plan
python -I recherche/antworten/skripte/gefaelle/gefaelle_pruefen.py <scratchpad>/a15b/plan \
    --daten2m recherche/vorlagen/daten/sehens --hoehe1m-fenster recherche/vorlagen/daten/gefaelle/hoehe_1m_fenster
```

## 5. Grenzen

- **Schmaleres Wasser:** Die sichtbare Wasserfläche ist 0,6–1,0 m schmaler als die Breite in den Daten. Bei einem 4-m-Bach
  sind es etwa 3 m. Das Netz reicht unter die Böschung.
- **Uferring:** Er hebt flache Ufer um bis zu 1 m an (Spiegel + 0,15 m). Wo das alte Ufer tiefer liegt, bleibt es
  „Bestand“ (WARNUNG). Das betrifft nur D3 mit 2 Proben.
- **Cloud-Test:** Die 1-m-Fenster decken die Pilotläufe ab. Für die übrigen Läufe rechnet der Feinschliff in der Cloud
  gegen 2 m bilinear, lokal gegen die echte 1-m-Welt.
