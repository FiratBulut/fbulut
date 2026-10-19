# Antwort 23e – Stufe B: nur sichtbare Lücke zählt; Zonen ab der sichtbaren Wasserkante; K1, 0,55 m² und Herkunft geklärt

Gelesen: recherche/auftraege/23e-deckung-stufe-b-rueckfragen.md @ 2af5e9f154dac3e87862204c315c3f4ba637109e (Commit cd500c2)

Stand 19.10.2026. Bezug: Antwort 23d (8dce6ec) §1.3/§1.4, Regeln 23.4 (`regeln_23d_1efa9f8e`), Referenzcode aus Antwort 23 (Selbsttest
`64a654746495eca8`), `skripte/detailgrad/detailgrad_regeln.json` (20). Bearbeiter: Cloud-Recherche. Bereich: Sitzprüfung Stufe B, Deckung C2.
Neue Regelversion **23.6** (Block `nachtrag_23_6` in `steine_sitz_regeln.json`); lokal ausdrücklich zu übernehmen.

## Kurzfazit

1. **Lücke in Stufe B – beantwortet:** Weder Perzentil noch „nur bodennahe Zellen“. Beide verstecken echte talseitige Lücken oder machen
   das Urteil von der Netzform abhängig. Neu ist: **Luft unter dem Stein zählt nur, wenn sie mit dem Umriss verbunden ist**, also von
   außen sichtbar.
   - Ein Hohlraum unter einem eingegrabenen Felsen, rundum vom Gelände abgeschlossen, ist kein Fehler.
   - Den Patch habe ich am Referenzcode gerechnet (§1). Der bisherige Selbsttest bleibt bei `64a654746495eca8`; die 5 neuen Fälle bestehen.
   - Der alte Weg macht genau euren Befund: eingegrabener Fels mit hochgewölbter Unterseite → FEHLER Lücke +0,19 m.
2. **Kante fast ganz nass – beantwortet:** Die Zonen werden **ab der sichtbaren Wasserkante des gespeicherten Stands** gemessen, so
   wie es 20 schon für die Zählungen vorschreibt. Wasserzellen gehören nie in den Nenner.
   - Eine zu 66 % nasse „Kante“ zeigt, dass ab der Bettkante des Plans gemessen wurde. Dort steht das Breite-5-Wasser darüber.
   - Steine ins Wasser gehören **nicht** in diesen Schritt (Bett und SWR-Hindernis, nach T6N1, eigener Bake).
   - Für Hänge über 38° ist Fels-Lage statt Geröll-Lage zulässig, sofern das Bild keine gestreckte Textur zeigt (§2).
3. **K1-Grenze – beantwortet:** Gezählt wird je 10 m Wasserkante und Seite, im Band 0–3 m (Kante und Ufer zusammen), nur trocken.
   Unter Wasser zählt nichts. Ein Haufen-Netz (23.5) zählt als **eine** Instanz seiner Größe; `SmallStonesPack_01` ist also K2 (§3).
4. **0,55 m² – beantwortet:** Das war unsere grobe Budgetschätzung in 23d §1.3, keine Regel. Der Planer rechnet keine Stückzahl aus dem
   Fehlbetrag. Er setzt Stück für Stück, rechnet die Vereinigung neu und hört beim Zonenziel oder an einer Grenze auf (§4).
5. **Herkunft der Misch-Kürzel – beantwortet:**
   - Zuerst die protokollierten Reparatur-Versätze zurückrechnen.
   - Danach Rekonstruktion nur im Plan-Modus (ohne Import) mit Kontrolle an einer Schicht, deren Original-Plan vorliegt.
   - Erreicht die Kontrolle nicht ≥ 99 %: Fensterregeln nach 23.4 (§5).
6. **Lokaler Vorschlag mit 1 155 Lagen abgelehnt: bestätigt.** Der Fehlbetrag gilt aber erst nach der Neuberechnung ab der Wasserkante.
   **Kein Planer-Neulauf mit den Zahlen aus §1 des Auftrags** (§6).
7. **Nächste Handlung:** T23e-1, Zonen ab der Wasserkante, offline mit beiden Dumps (§6).

---

## 1. Stufe B: sichtbare Lücke statt größter Lücke

### 1.1 Zwei mögliche Ursachen, getrennt am synthetischen Fall

Euer Beispiel C2:1989 liegt in Stufe A 31,6 cm im Boden und hat in Stufe B +39,3 cm Lücke. Möglich sind zwei Ursachen:

- **U1 – Messweg:** Die Hülle aus Eckpunkten nimmt in Zellen ohne Unterseiten-Punkt einen Flanken- oder Oberseitenpunkt.
- **U2 – Geometrie:** Die Unterseite ist im Kern tatsächlich hochgewölbt, z. B. eine Scan-Unterseite mit Mulde. Unter einem
  eingegrabenen Felsen entsteht dann ein **abgeschlossener Hohlraum**, den man von außen nicht sieht.

Rechnung mit einem Fels-Ellipsoid 1,6 × 1,2 × 1,0 m, Hülle einmal aus Eckpunkten und einmal aus Dreiecken:

| Fall | Hülle | alte Lücke (Kern-Max) | sichtbare Lücke 23.6 | Hohlraum-Anteil |
|---|---|---:|---:|---:|
| SB1 grob vernetzt (10 × 6), 35 cm im Boden | Ecken / Dreiecke | −0,28 / −0,23 | keine | 0 |
| SB2 fein (48 × 24), 35 cm im Boden | Ecken / Dreiecke | −0,28 / −0,25 | keine | 0 |
| SB3 fein, Unterkante 8 cm über Boden | Ecken / Dreiecke | +0,15 / +0,18 | +0,15 / +0,18 → **FEHLER** | 0 |
| SB4 fein, 30°-Hang, talseitig unterschnitten | Ecken / Dreiecke | +0,18 / +0,25 | +0,18 / +0,25 → **FEHLER** | 0 |
| SB5 fein, 35 cm im Boden, Unterseite innen 0,5 m hochgewölbt | Ecken / Dreiecke | **+0,19 → FEHLER** | keine → ok | 0,52 / 0,54 |

**Befund:**

- Die grobe Vernetzung erzeugt hier **keine** Scheinlücke; U1 ist damit nicht belegt. Die Dreiecks-Hülle ist trotzdem genauer (mehr
  Zellen) und wird bevorzugt, wenn Indizes exportiert sind.
- SB5 reproduziert euren Befund: eingegraben, aber FEHLER Lücke. Das passt auch zu eurer Zählung „bei 40 von 91 Netzen > 50 % der
  Zellen über 5 cm über dem tiefsten Punkt“.
- **Ursache ist wahrscheinlich U2 [Hypothese].** Bestätigt wird sie in T23e-2 (§6).

### 1.2 Regel 23.6 (`nachtrag_23_6.stufe_b_luecke`)

- **Lücke (Stufe B):** größtes d über die Kern-Zellen, die über Zellen mit d > 3 cm mit dem Umriss der Hülle verbunden sind
  (4er-Nachbarschaft). Umriss heißt: Die Zelle hat einen Nachbarn ohne Treffer.
- Die Verbindung wird über die **volle** Hülle gesucht. Der Kern (0,6 × halbe Box) bleibt die Messfläche.
- **Hohlraum-Anteil:** nur als Diagnose berichten, ohne Urteil.
- **Deckung:** unverändert. FEHLER Deckung gibt es weiter nur zusammen mit einer Lücke über 3 cm; eingeschlossene Hohlräume lösen ihn
  also nicht mehr aus.
- **Erhalten bleiben:** schwebende Stücke (SB3) und die talseitige Fels-Lücke (SB4, 23 §3). Ein Perzentil hätte gerade diese versteckt.

### 1.3 Patch auf den Referenzcode

Eingabe ist der Codeblock aus Antwort 23 wörtlich, mit LF-Zeilenenden. Bricht ein `assert` ab, stimmt die Eingabe nicht.

```
python -I patch_23_6.py sitz_pruefung.py sitz_pruefung_23_6.py
python -I sitz_pruefung_23_6.py --selbsttest        # muss weiter "Signatur 64a654746495eca8" zeigen
python -I sitz_pruefung_23_6.py --selbsttest-23-6   # SELBSTTEST 23.6 OK  Faelle 10
```

Optional: `inst.dreiecke = [(i, j, k), …]` setzen (Indizes in `punkte`); dann wird die Hülle aus Dreiecken gebildet. Die Hülle je Netz
cachen, denn sie hängt nicht von der Instanz ab.

```python
# patch_23_6.py
"""Patch 23.6 (Antwort 23e) auf den Referenzcode aus Antwort 23 (sitz_pruefung): Stufe-B-Luecke nur, wenn mit dem Umriss verbunden.
Aufruf: python -I patch_23_6.py sitz_pruefung.py sitz_pruefung_23_6.py   (Eingabe = Codeblock aus 23 woertlich, LF)."""
import sys
src = open(sys.argv[1], encoding="utf-8").read()
def rep(alt, neu):
    global src
    assert src.count(alt) == 1, alt[:60]
    src = src.replace(alt, neu)

rep('def messe(i, welt, insts):\n', '''def huelle_zellen(punkte, zelle=0.10):
    """23.6: untere Huelle aus Eckpunkten wie untere_huelle, aber je Zelle (i, j) und ohne Kern."""
    x0 = min(p[0] for p in punkte); y0 = min(p[1] for p in punkte); z = {}
    for p in punkte:
        k = (int((p[0] - x0) / zelle), int((p[1] - y0) / zelle))
        if k not in z or p[2] < z[k][2]: z[k] = p
    return z

def huelle_dreiecke(punkte, dreiecke, zelle=0.10):
    """23.6: je Zellmitte der tiefste Schnitt einer Senkrechten mit einem Dreieck (Strahl von unten); bevorzugt, wenn Indizes vorliegen."""
    x0 = min(p[0] for p in punkte); y0 = min(p[1] for p in punkte); z = {}
    for ia, ib, ic in dreiecke:
        a, b, c = punkte[ia], punkte[ib], punkte[ic]
        det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(det) < 1e-14: continue
        for i in range(max(0, int((min(a[0], b[0], c[0]) - x0) / zelle) - 1), int((max(a[0], b[0], c[0]) - x0) / zelle) + 1):
            px = x0 + (i + 0.5) * zelle
            for j in range(max(0, int((min(a[1], b[1], c[1]) - y0) / zelle) - 1), int((max(a[1], b[1], c[1]) - y0) / zelle) + 1):
                py = y0 + (j + 0.5) * zelle
                l1 = ((b[1] - c[1]) * (px - c[0]) + (c[0] - b[0]) * (py - c[1])) / det
                l2 = ((c[1] - a[1]) * (px - c[0]) + (a[0] - c[0]) * (py - c[1])) / det
                if l1 < -1e-9 or l2 < -1e-9 or 1 - l1 - l2 < -1e-9: continue
                pz = l1 * a[2] + l2 * b[2] + (1 - l1 - l2) * c[2]
                if (i, j) not in z or pz < z[(i, j)][2]: z[(i, j)] = (px, py, pz)
    return z

def luecke_sichtbar(i, welt, insts, kern, zelle=0.10):
    """23.6 Stufe B: groesstes d ueber die Kern-Zellen ohne eingeschlossene Hohlraeume. Luft zaehlt nur, wenn sie ueber Zellen mit
    d > kontakt mit dem Umriss der Huelle verbunden ist (4er-Nachbarschaft). Rueckgabe (luecke_max, hohl_anteil)."""
    tri = getattr(i, "dreiecke", None)
    zel = huelle_dreiecke(i.punkte, tri, zelle) if tri else huelle_zellen(i.punkte, zelle)
    d = {}
    for k, p in zel.items():
        w = i.welt(p); d[k] = w[2] - traeger(welt, insts, i, w[0], w[1], w[2])[0]
    tol = R["tol"]["kontakt"]; offen = {k for k, v in d.items() if v > tol}; nb = ((1, 0), (-1, 0), (0, 1), (0, -1))
    erreicht = {k for k in offen if any((k[0] + a, k[1] + b) not in d for a, b in nb)}; st = list(erreicht)
    while st:
        k = st.pop()
        for a, b in nb:
            n = (k[0] + a, k[1] + b)
            if n in offen and n not in erreicht: erreicht.add(n); st.append(n)
    xs = [p[0] for p in i.punkte]; ys = [p[1] for p in i.punkte]
    cx, cy, hx, hy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (max(xs) - min(xs)) / 2, (max(ys) - min(ys)) / 2
    kz = [k for k, p in zel.items() if kern is None or ((p[0] - cx) / hx) ** 2 + ((p[1] - cy) / hy) ** 2 <= kern * kern]
    sicht = [d[k] for k in kz if k in erreicht or d[k] <= tol]
    hohl = sum(1 for k in kz if k in offen and k not in erreicht) / max(1, len(kz))
    return (max(sicht) if sicht else tol), hohl

def messe(i, welt, insts):
''')
rep('''    m["luecke_max"] = max(d); m["deckung"] = sum(1 for v in d if v <= tol["kontakt"]) / len(d)
''', '''    m["luecke_max"] = max(d); m["deckung"] = sum(1 for v in d if v <= tol["kontakt"]) / len(d)
    if i.punkte and not duenn and not i.klasse.startswith("totholz"):   # 23.6: Fels/Stein/Kiesel in Stufe B nur sichtbare Luecke
        m["luecke_max"], m["hohl_anteil"] = luecke_sichtbar(i, welt, insts, kern)
''')
rep('''def lade_regeln(pfad):''', '''def selbsttest_23_6():
    """SB1-SB5 (Regeln 23.6 nachtrag_23_6.stufe_b_luecke.pruef_faelle); Gelaende wie selbsttest()."""
    welt = Welt(Raster(gelaende, 41, 41), lambda x, y: None, lambda x, y: (0.0, 1.0))
    def ellipsoid(a, b, c, nu, nv, z0, beule=0.0):
        P = [(0.0, 0.0, -c)]; T = []
        for iv in range(1, nv):
            v = math.pi * iv / nv
            for iu in range(nu):
                u = 2 * math.pi * iu / nu; x, y, z = a * math.sin(v) * math.cos(u), b * math.sin(v) * math.sin(u), -c * math.cos(v)
                if z < 0 and (x / a) ** 2 + (y / b) ** 2 < 0.16: z += beule          # Hohlraum: Unterseite innen hochgewoelbt
                P.append((x, y, z))
        P.append((0.0, 0.0, c)); top = len(P) - 1; r = lambda iv, iu: 1 + (iv - 1) * nu + iu % nu
        for iu in range(nu): T.append((0, r(1, iu + 1), r(1, iu))); T.append((top, r(nv - 1, iu), r(nv - 1, iu + 1)))
        for iv in range(1, nv - 1):
            for iu in range(nu): T += [(r(iv, iu), r(iv, iu + 1), r(iv + 1, iu + 1)), (r(iv, iu), r(iv + 1, iu + 1), r(iv + 1, iu))]
        P = [(x, y, z + c) for x, y, z in P]                                   # Pivot am tiefsten Punkt
        return P, T
    BX = ((-0.8, -0.6, 0.0), (0.8, 0.6, 1.0)); t30 = math.tan(math.radians(30)); I = []; soll = {}
    for nr, (nu, nv, beule, pos, u) in {
            "SB1": (10, 6, 0.0, (33, 4, 10.0 - 0.35), "ok"), "SB2": (48, 24, 0.0, (36, 4, 10.0 - 0.35), "ok"),
            "SB3": (48, 24, 0.0, (33, 8, 10.08), "FEHLER"), "SB4": (48, 24, 0.0, (3.0, 15.0, 10 + t30 * 3.0 - 0.10), "FEHLER"),
            "SB5": (48, 24, 0.5, (36, 8, 10.0 - 0.35), "ok")}.items():
        P, T = ellipsoid(0.8, 0.6, 0.5, nu, nv, 0.0, beule)
        for weg in ("e", "d"):
            inst = Inst(nr + weg, "SM_Test_SB", pos, (0, 0, 0), 1.0, BX[0], BX[1], "fels", punkte=P)
            if weg == "d": inst.dreiecke = T
            I.append(inst); soll[nr + weg] = u
    erg = {}; fehl = []
    for weg in ("e", "d"):                                                     # getrennt, sonst durchdringen sich die Paare
        J = [x for x in I if x.nr.endswith(weg)]; erg.update({k: (v, J) for k, v in pruefe(J, welt).items()})
    for nr, u in soll.items():
        (iu, f, w), J = erg[nr]
        if iu != u or (u == "FEHLER" and "luecke" not in f): fehl.append((nr, u, iu, f))
        m = messe(next(x for x in J if x.nr == nr), welt, J)[0]
        print("%-4s %-7s %-22s luecke %+.3f  hohl %.2f" % (nr, iu, ",".join(f) or "-", m["luecke_max"], m.get("hohl_anteil", 0.0)))
    for z in fehl: print("ABWEICHUNG", z)
    print(("SELBSTTEST 23.6 OK" if not fehl else "SELBSTTEST 23.6 FEHLGESCHLAGEN") + "  Faelle %d" % len(soll))
    return not fehl

def lade_regeln(pfad):''')
rep('''ap.add_argument("--selbsttest", action="store_true")''', '''ap.add_argument("--selbsttest", action="store_true"); ap.add_argument("--selbsttest-23-6", action="store_true")''')
rep('''    if a.selbsttest: raise SystemExit(0 if selbsttest() else 1)''', '''    if a.selbsttest: raise SystemExit(0 if selbsttest() else 1)
    if a.selbsttest_23_6: raise SystemExit(0 if selbsttest_23_6() else 1)''')
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(src)
print("patch 23.6 ok")
```

Selbst ausgeführt: Hauptselbsttest `SELBSTTEST OK  Regeln 23.1  Faelle 33  Signatur 64a654746495eca8`, danach
`SELBSTTEST 23.6 OK  Faelle 10` mit den Werten der Tabelle in §1.1. Gegenprobe mit dem alten Lückenweg: SB5 wird FEHLER (deckung, luecke).

## 2. Kante fast ganz nass

**Was schiefging:** Die Zonen kante/ufer/hang in 23.4 haben den Bezug nicht genannt. 20 legt ihn in `detailgrad_regeln.json` fest:
„Zählungen je 10 m und Seite im Band 0–3 m **ab der Wasserkante**“. Der Plan rechnet dagegen ab der Bettkante (`d = m außen ab der
Bettkante`). Im Plan ist beides gleich, in der Welt nicht.

Eine Kantenzone, die zu 66 % sichtbar nass ist, kann nur ab der Bettkante gemessen sein. Das gespeicherte Wasser steht über ihr.

**Regel 23.6 (`zonen_bezug`):**

| Punkt | Festlegung |
|---|---|
| Wasserkante | Rand der Zellen `sichtbar_1` (nass und W − H > 0,01) des **gespeicherten** Wasserstands, mit Dump-ID |
| Zonen | Kante 0–1 m, Ufer 1–3 m, Hang 3–10 m landwärts ab dieser Kante; Wasserzellen nie im Nenner |
| Kontrollfall Plan | bleibt auf der Bettkante; er prüft nur die Rechnung (eure 12 Werte ≤ 0,004 gelten weiter) |
| > 38° | keine Geröll-Lage (Schüttwinkel). Lage `Fels` als anstehender Fels zulässig, wenn eine feste Kamera keine gestreckte Textur zeigt (**zu prüfen**, ob das Landschaftsmaterial dort triplanar oder gestreckt mappt). Sonst nur Netz. Die Zielwerte bleiben. |
| Steine ins Wasser | **nicht in diesem Schritt.** Dachziegel und Keystones im nassen Saum sind Bett und SWR-Hindernis; sie ändern den Bake. Das ist ein eigener 16h-Schritt nach gespeichertem T6N1. |

**Warum zuerst beide Dumps:** Das gespeicherte Wasser ist heute BAKED_SIM mit Breite 5. Breite 5 extrapoliert den Spiegel in trockene
Zellen; daher kam der „Deckel“ (6n/6o). Ein Teil der 66 % ist deshalb vermutlich dieses Artefakt [Hypothese]. T6N1 mit Breite 1 ist
dafür der Prüfstand (6p).

- Sinkt der Nass-Anteil der alten Kantenzone mit dem T6N1-Dump deutlich, ist die Glättung die Hauptursache. Dann rückt die Wasserkante
  mit dem Speichern von T6N1 zurück an den Plan.
- Bleibt er bei Breite 1 hoch, steht das Wasser wirklich über der geplanten Bettkante. Dann ist der Bezug auf die Wasserkante erst
  recht nötig.

Rechnen auf dem Breite-5-Stand ergäbe einen Fehlbetrag für ein Wasser, das es nach T6N1 nicht mehr gibt.

## 3. K1-Grenze

| Frage | Antwort |
|---|---|
| je Zone oder je Seite? | je **10 m Wasserkante und Seite**, im Band 0–3 m (Kante und Ufer zusammen), wie 20 |
| Kiesel unter Wasser? | **zählen nicht.** Das Band liegt landwärts der Wasserkante. Kiesel < 0,15 m im Wasser sind nach `farbe.reparatur` (23) ohnehin zu entfernen |
| Klasse | nach L × Skala des Netzes: K1 0,03–0,1 m, K2 0,1–0,3 m |
| Haufen | Ein `kiesel_haufen` (23.5, z. B. `SmallStonesPack_01/03`, L 0,26 m) zählt als **eine K2-Instanz**, nicht als K1 |
| Ersatz-Kiesel reißen die Grenze | K1 wird im Band 0–3 m als **Kies-Lage** oder als Haufen-Netz umgesetzt, nicht als Einzelnetze (23d §1.3 Punkt 3) |

Die Grenze von 10 bleibt. Der Grund aus 20/16h N6h ist weiterhin „Komposition statt Kleinzeug“: Einzelne Steinchen unter 10 cm lesen
aus Spielerhöhe als Rauschen und kosten Instanzen.

## 4. Woher die 0,55 m² kommen

Der Wert stammt aus unserer Rechnung in 23d §1.3, „grob“: Ein typisches Stück von 1,0–1,2 m hat als Fels-Ellipse × 0,85 etwa
0,47–0,72 m² Fußabdruck. Davon geht an der Kante ein Teil durch Überlappung verloren (Faktor bis 1,6). Daraus ergab sich ≈ 0,55 m² netto.
**Der Wert ist keine Regel** und taugt nur für das Budget.

**Planer (`fussabdruck_schaetzung`):**

- Er setzt Stück für Stück, jedes mit Sitzprüfung.
- Nach jedem Stück rechnet er die Vereinigung nach `deckung.vereinigung` neu.
- Er hört auf, wenn das Zonenziel erreicht ist oder eine Grenze greift: Überlappungsfaktor, Kleinzeug, Reihe/Ring 23.3, Budget
  45 000 / 3 000 je Feld.
- Die Stückzahl ist Ergebnis, nicht Eingabe.
- Euer Fehlbetrag in Stück (≈ 260 / 30 / 480) dient nur als Plausibilitätsprüfung: Weicht der Planer um mehr als Faktor 2 davon ab,
  den Grund nennen.

## 5. Herkunft der Misch-Kürzel (55,5 % eindeutig)

Reihenfolge, je Schritt mit eigenem Ergebnis:

1. **Versätze zurückrechnen (billig, zuerst):** Reparaturen aus v3 und 23 haben Instanzen in XY verschoben. Liegt der Versatz über
   0,10 m, findet der Abgleich sie nicht mehr. Deshalb vor dem Abgleich die protokollierten Versätze zurückrechnen und die Quote neu
   bestimmen.
2. **Rekonstruktion nur im Plan-Modus:** die alten Planer mit den Eingaben ihres Laufdatums (Regel-JSON und Karten in der damaligen
   Revision). Die Plan-JSON kommt in einen eigenen Ordner, es gibt **keinen Import**. Ein Import würde v3- und T22-Entfernungen
   zurückbringen (22b §4). Ob die Planer einen reinen Plan-Lauf ohne Welt-Schreiben anbieten, ist **zu prüfen**; sonst nur die
   Plan-Funktion aufrufen.
3. **Kontrolle vorab:** Rekonstruiert wird zuerst eine Schicht, deren Original-Plan-JSON vorliegt. Sie muss ≥ 99 % der Originaleinträge
   treffen (gleiches Netz, XY ≤ 0,10 m). **Sonst nicht rekonstruieren.** Die Eingaben von damals sind dann nicht mehr herstellbar,
   und jeder Treffer wäre Zufall.
4. Bleibt eine Schicht danach unter 0,8 Zuordnung, gilt `folge_unklar` aus 23.4: nur Werkzeugschritte in den Fenstergrenzen, keine
   Neuplanung.

Schritt 1–3 blockieren nichts. Die Neuplanung von DETA/P2BE in C2 läuft über die eindeutigen Schichten.

## 6. Nächste Handlung (eine, offline, Rolle 1): T23e-1 Zonen ab der Wasserkante

**Eingaben:** Plan `plan_p2_talkaskade.json`, Zensus wie in T23d-D, Regeln 23.6, Dump Breite 5 (gespeichert) und Dump T6N1_2 (Breite 1).

**Rechnung:**

1. **Nass-Anteil:** Anteil der alten Kantenzone (ab Bettkante) mit `sichtbar_1`, je Seite, für beide Dumps.
2. **Zustände A–D:** neu auf Zonen ab der Wasserkante, nur trockene Zellen, mit dem **gespeicherten** Stand. Ist T6N1 inzwischen
   gespeichert, ist das Breite 1; sonst Breite 5, dann als vorläufig markiert.
3. **Neuer Fehlbetrag** je Zone und Seite; Anteil > 38° je Zone.

**Erwartung:**

- Der Nass-Anteil sinkt mit Breite 1 deutlich (unter 30 %), wenn die Glättung die Ursache war.
- Der Hang-Fehlbetrag ändert sich wenig, Kante und Ufer stärker.

**Erfolg:**

- Kontrollfall Plan unverändert (12 Werte ≤ 0,004).
- Tabelle Nass-Anteil (Breite 5 / Breite 1) und Tabelle A–D sowie Fehlbetrag mit Dump-ID.

**Abbruch:** Ist der gespeicherte Stand unklar (T6N1 weder gespeichert noch verworfen), nur Schritt 1 liefern. Der Planer-Neulauf
startet erst auf einem gespeicherten Stand.

**Danach:**

- **T23e-2** (offline): Patch 23.6 auf die 142 Netze und die 116 umgekippten Felsen.
  - Erwartet wird, dass die meisten mit Hohlraum-Anteil > 0 wieder ok sind (U2).
  - Bei den verbleibenden die 5 größten Lücken mit tiefer Kamera auf der Seite der größten Lücke ansehen.
  - Zeigt ein Bild dort keine Lücke, die Dreiecks-Hülle für dieses Netz exportieren (U1).
- Danach der Planer-Neulauf mit dem neuen Fehlbetrag.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Steine an der Wasserlinie:** Teils eingetauchte Blöcke mit Nasslinie fallen an Witcher-Bächen am meisten auf. Das ist der
   16h-Schritt nach T6N1 mit neuem Bake, nicht die Deckungsrechnung an Land.
2. **Steile Ufer als anstehender Fels:** Über 38° liest sich eine Felslage mit wenigen großen, eingegrabenen Blöcken natürlich. Ein
   Geröllteppich kann dort nicht liegen.
3. **Komposition statt Streu:** große Ankerstücke ≥ 1 m, K2 in den Fugen, K1 als Kies-Lage. Das hält die K1-Grenze ein und sieht
   ruhiger aus.
4. **Keine schwebenden Felsen bei echten Unterschneidungen:** Stufe B 23.6 hält die talseitige Lücke als FEHLER fest. Sie wird künftig
   durch tieferes Eingraben auf der Talseite behoben, nicht durch eine weichere Regel.

## Quellen

- `recherche/auftraege/23e-deckung-stufe-b-rueckfragen.md` (Commit cd500c2)
- `recherche/antworten/23-steine-organisch-im-boden.md`: Messgrößen §2, Referenzcode, Selbsttest (Commit 264a4d8)
- `recherche/antworten/23d-t23-1-neuplanung-rueckfragen.md` §1.3, §1.4, R1/R2 (Commit 8dce6ec)
- `recherche/antworten/skripte/detailgrad/detailgrad_regeln.json`: Größenklassen K1/K2, Zählnotiz „je 10 m und Seite im Band 0–3 m ab der
  Wasserkante“
- `recherche/antworten/skripte/detailgrad/plan_p2_talkaskade.json`: Koordinaten „d ab der Bettkante“
- `recherche/antworten/16h-nachtrag6p-t6n1-kolk25.md` (Commit 8455b38), `16h-nachtrag6o-…` (f2bb485): Breite 5/1, T6N1
- `recherche/antworten/22b-wasserpflanzen-t22-0-rueckfragen.md` §4: kein Planer-Neulauf mit Import
- `recherche/antworten/steine_sitz_regeln.json`: jetzt 23.6, Block `nachtrag_23_6`

## Rückfragen

Keine, die den nächsten Schritt ändern. Ob das Landschaftsmaterial über 38° gestreckt mappt und ob die Planer einen reinen Plan-Lauf
haben, ist lokal feststellbar.
