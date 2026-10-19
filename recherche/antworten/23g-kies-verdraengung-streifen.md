# Antwort 23g – Kies-Verdrängung auf 11 cm (0,08-gleichwertig); Sitzprüfung misst künftig gegen die verdrängte Oberfläche; V18c zuerst, Planer im Plan-Modus parallel

Gelesen: recherche/auftraege/23g-kies-verdraengung-streifen.md @ bbcd90e1a1b6616c7f2b9fadcc9b62f70fd5e425 (Commit ae0affa)

Stand 19.10.2026. Bezug: Antwort 23f §4 und Witcher-Liste Punkt 2 (Commit 39fb460), Regeln 23.8, jetzt **23.9** (Block `nachtrag_23_9`).
Bearbeiter: Cloud-Recherche. Bereich: Landschaftsmaterial V18b/V18bs → V18c, Sitzprüfung. Bild `bilder/platzierung/streifen/str_reihe.jpg` selbst
angesehen (§1).

## Kurzfazit

1. **Unser Fehler in 23f §4:** Wir hatten die Streifen einer RVT-Überblendung an *Rundstein-Netzen* zugeschrieben. Es sind keine Netze,
   sondern Nanite-verdrängte Landschaft. Eure Zensus-Projektion und der Editor-Test belegen das.
2. **Zielwert – beantwortet: 0,08** (Kies-Hub 11,2 cm, `Disp_Anteil_Kies` = 0,25).
   - In den Nahansichten zeigen sich bei 0,11 noch verschmierte Flanken, bei 0,08 kaum noch.
   - Aus Spielerhöhe sind 0,11 und 0,08 gleichwertig.
   - 0 wirkt aufgemalt.
   - Gate für die Weltumsetzung: Flanken > 45° ≤ 10 %, Streckung p99 ≤ 2,5, kein Streifen an den drei Kameras (§1).
3. **Fels – beantwortet:** Ja, mit denselben Kennzahlen prüfen, aber nur auf flachen Felsflächen (Hang < 20°). Dort greift die
   Seitenprojektion nicht. Den Hub nur senken, wenn das Gate verfehlt wird (§2).
4. **Sitzprüfung – beantwortet:** Die Verdrängung kommt in den Bezug. Die Restunsicherheit von ± 5,6 cm bei 0,08 liegt über den Toleranzen
   von Stein (3 cm) und Kiesel (1,5 cm).
   - Neu (23.9): Bezugsfläche S = H + Σ Hub × (T − c) × w statt H, wo der Hub ≥ 2 cm beträgt.
   - Prüfung zuerst mit einer Tiefenaufnahme (K33).
   - Auf Kies ≥ 0,5 werden keine Kiesel-Netze mehr gesetzt; die Lage zeigt den Kies dort selbst (§3).
5. **Reihenfolge – beantwortet:**
   - Zuerst V18c bauen: Vorgabe bitgleich, dann Pilot in C2, danach 3–4 Kiesfelder mit Bild, dann weltweit.
   - Der Planer-Neulauf im Plan-Modus darf parallel rechnen. Vor dem Schreiben in die Welt wird er gegen S mit dem neuen Hub geprüft (§4).

---

## 1. Zielwert (Bildurteil, selbst angesehen)

| Kamera | Ist 0,225 | 0,11 | 0,08 | 0 |
|---|---|---|---|---|
| C2_64801 | starke senkrechte Streifen an den „Steinen“ | an einigen Flanken noch Schlieren | Schlieren fast weg, Relief bleibt | flach, Platte liegt sichtbar auf ebenem Boden |
| nah, Sonne im Rücken | Steine wirken „geschmolzen“ | vorne links noch deutlich verschmiert | vorne noch leichte Schlieren, sonst ruhig | flach, liest sich wie Pflaster |
| Spielerhöhe | Streifen im Vordergrund | ruhig, plastisch | ruhig, plastisch, kaum Unterschied zu 0,11 | flach, wirkt aufgemalt |

**Entscheidung 0,08:**

- Das Kriterium „aus Spielerhöhe nicht erkennbar“ erfüllen beide Werte.
- In Nahansichten (Klettern, Hocken, Zwischensequenzen) bleibt bei 0,11 ein Rest; bei 0,08 kaum.
- Eure Kennzahlen stützen das: Flanken > 45° 9 % statt 17 %, Streckung p99 2,5 statt 3,3.

**Faustregel [Ableitung]:** Ein Kiesel ragt aus seinem Bett höchstens etwa um seinen halben Durchmesser heraus. Ein Hub über dem halben
mittleren Steindurchmesser der Höhentextur erzeugt Körper, die höher als breit sind. Deren Flanken muss die Draufsicht-Projektion strecken.
Bei 31,5 cm Hub ist das offensichtlich. Den mittleren Steindurchmesser in `T_ground_big_pebbles_01` bei 2,5 m Kachel bitte einmal messen
(**zu prüfen**). Liegt er bei etwa 20–25 cm, bestätigt er 0,08.

**Gate für die Weltumsetzung (23.9 `verdraengung_ziel`):**

- Flanken > 45° ≤ 10 % der Kiesfläche;
- Streckung p99 ≤ 2,5;
- an den drei Kameras keine erkennbaren senkrechten Streifen.

## 2. Fels und andere Lagen

- **Dieselbe Ursache, anderer Ort:** Auf steilen Felsflanken greift die Seitenprojektion. Auf **flachen** Felsflächen werden die
  verdrängten Buckel dagegen von oben projiziert und gestreckt, genau wie beim Kies.
- **Messen:** Flanken > 45° und Streckung p99 je Lage, nur auf Zellen mit Hang < 20° und Lagengewicht ≥ 0,5. Dazu ein Bild an 2 festen
  Kameras auf flachem Fels.
- Den Hub nur senken, wenn das Gate aus §1 verfehlt wird. Fels darf mehr Relief behalten als Kies; die Grenze liegt bei den Flanken und
  nicht bei der Höhe.
- Die übrigen Lagen mit ≤ 8 cm brauchen keine Prüfung. Bei 8 cm Hub ist die Streckung auf flachem Boden gering [Ableitung].

**Ursache an der Wurzel (zu prüfen, nicht jetzt):** Die Projektionswahl hängt an der unverdrängten Normale. Wählte sie nach der
verdrängten Normale, griffe die Seitenprojektion an den Buckelflanken. Ob die Materialkette bei Nanite-Tessellation die verdrängte Normale
vor der Projektionswahl kennt, ist offen. Das lohnt erst, wenn mehr Hub gewünscht ist.

## 3. Sitzprüfung gegen die sichtbare Oberfläche (Regel 23.9)

**Warum nicht nur „Hub klein“:** Bei 0,08 schwankt die sichtbare Oberfläche um ± 5,6 cm um `hoehe.f32`. Die Toleranzen liegen bei Stein
(Lücke 3 cm) und Kiesel (1,5 cm) darunter, bei Fels (5–6 cm) gleichauf. Die Urteile auf Kiesflächen wären also Rauschen.

**Regel (`nachtrag_23_9.verdraengung_bezug`):**

- S(x, y) = H(x, y) + Σ_l Hub_l × (T_l(x, y) − c) × w_l(x, y).
  - T_l ist die Höhentextur aus Welt-XY mit der Kachel des Materials.
  - c ist die Verdrängungsmitte. Laut eurer Formel 0,5; am Material bestätigen.
- S ersetzt H in Träger, Eingraben, Lücke, Deckung, Kante und Planarität, wo Σ Hub × w ≥ 2 cm. Wasser und Lagen-Malerei bleiben auf H.
- **K33, Validierung vor Gebrauch:**
  - Aufbau: SceneCapture2D, orthografisch von oben, SceneDepth, über 5 × 5 m Kies und 5 × 5 m Felsplatte; nur im Testlevel, nichts
    speichern.
  - Soll: RMS(Tiefe − S) ≤ 1,5 cm und deutlich kleiner als RMS(Tiefe − H).
  - Sonst S nicht verwenden und melden.
  - Line-Traces taugen dafür nicht, weil sie die unverdrängte Kollision treffen.
- **Kiesel auf Kies:** Auf Lage Kies ≥ 0,5 werden keine `kiesel`- oder `kiesel_haufen`-Netze mehr gesetzt; die Lage zeigt den Kies schon.
  Bestehende dort werden geprüft, aber nicht ergänzt.

**Referenz-Hülle (selbst ausgeführt, Kurzprobe mit konstanter und wechselnder Textur):**

Ebene Textur ergibt S = H. Wechseltextur mit 11,2 cm Hub ergibt ± 5,6 cm. Liegt Hub × Gewicht unter 2 cm, bleibt S = H.

```python
# verdraengung_23_9.py – Huelle um das Welt-Objekt der Sitzpruefung (Referenzcode Antwort 23); H() liefert S
import math

class Lage:
    def __init__(s, textur, breite, hoehe, kachel_m, hub_m, gewicht, mitte=0.5):
        s.t, s.w, s.h, s.k, s.hub, s.g, s.c = textur, breite, hoehe, kachel_m, hub_m, gewicht, mitte  # textur: Zeilen, Werte 0..1
    def wert(s, x, y):                                   # bilinear, wiederholt (Welt-XY / Kachel)
        u = (x / s.k) % 1.0 * s.w - 0.5; v = (y / s.k) % 1.0 * s.h - 0.5
        i0, j0 = math.floor(u), math.floor(v); fu, fv = u - i0, v - j0
        T = lambda i, j: s.t[j % s.h][i % s.w]
        return (T(i0, j0) * (1 - fu) + T(i0 + 1, j0) * fu) * (1 - fv) + (T(i0, j0 + 1) * (1 - fu) + T(i0 + 1, j0 + 1) * fu) * fv
    def versatz(s, x, y):
        return s.hub * (s.wert(x, y) - s.c) * s.g(x, y)

class WeltS:
    """Wie Welt, aber H liefert S. Alles andere (nass, fluss, W) wird durchgereicht."""
    def __init__(s, welt, lagen, schwelle=0.02):
        s._w, s.lagen, s.schwelle = welt, lagen, schwelle
    def __getattr__(s, name): return getattr(s._w, name)
    def H(s, x, y):
        h = s._w.H(x, y)
        if sum(l.hub * l.g(x, y) for l in s.lagen) < s.schwelle: return h
        return h + sum(l.versatz(x, y) for l in s.lagen)
```

Verwendung: `pruefe(insts, WeltS(welt, [Lage(T_kies, 2048, 2048, 2.5, 0.112, gewicht_kies)]))`. Die Höhentextur wird einmal als Graustufen
exportiert. `gewicht_kies` liest `lage_Kies.r8 / 255`. Texturauflösung und -kanal sind lokal zu bestätigen.

**Folge für bisherige Urteile:**

- C2-Urteile auf Kiesflächen (1,3 ha) mit dem neuen Hub und S neu rechnen. Erwartet werden weniger Lücken-FEHLER unter Platten (Beispiel
  64801) und mehr „versunken“ bei kleinen Stücken.
- Die übrigen Flächen bleiben unverändert (S = H).

## 4. Reihenfolge

1. **V18c/V18cs bauen** mit `Disp_Anteil_Kies` als Parameter. Prüfung: bei Vorgabe 0,7 bitgleich zum Ist (Bildvergleich an den 3 Kameras und
   0 Shaderfehler).
2. **Pilot C2:** den Parameter auf 0,25, das Gate aus §1 einhalten, Speicherbeleg für das MI. Rücknahme heißt Parameter zurück.
3. **3–4 Kiesfelder mit Bild** (Vorschlag C3, G3, B4, H4: größte Kiesflächen), dann weltweit.
4. **K33** (Tiefenaufnahme) gegen S mit dem neuen Hub.

**Planer-Neulauf C2 im Plan-Modus:**

- Er darf **parallel** rechnen; er schreibt nichts in die Welt.
- Vor dem Schreiben wird jede Kiesflächen-Platzierung mit `WeltS` und dem gesetzten Hub erneut geprüft.
- In der Talkaskade betrifft das nur die Kiesanteile; die Zonenrechnung (23f) hängt nicht am Hub.

---

## Was fehlt bis Witcher 4

Nach Wirkung geordnet, nur für diesen Vorgang:

1. **Kein Schmelz-Kies:** 0,08 weltweit nimmt die auffälligsten Artefakte aus 27,6 ha Kiesfläche, mit einem Parameter.
2. **Kachelwiederholung 2,5 m:** In der Spieleransicht wirkt das Kiesmuster gleichmäßig. Eine zweite, gedrehte und größer skalierte Abtastung
   als Makro-Variation bricht das Raster. Das ist eine Materialfrage, **zu prüfen**, ob der Master das schon kann.
3. **Echte Steine an Übergängen:** Einzelne Netze von 0,1–0,3 m nur an Rändern (Kies zu Gras, Kies zu Wasser) statt Kiesel auf Kies. Dort
   bricht ein echter Körper die Fläche.

## Quellen

- `recherche/auftraege/23g-kies-verdraengung-streifen.md` (Commit ae0affa), Bild `bilder/platzierung/streifen/str_reihe.jpg` (selbst
  angesehen)
- `recherche/antworten/23f-t23e-ergebnisse-rueckfragen.md` §4 und Witcher-Liste (Commit 39fb460)
- `recherche/antworten/23-steine-organisch-im-boden.md`: Referenzcode (`Welt`, `pruefe`) (Commit 264a4d8)
- `recherche/antworten/steine_sitz_regeln.json`: jetzt 23.9, Block `nachtrag_23_9`

## Rückfragen

Keine, die den nächsten Schritt ändern. Steindurchmesser in der Höhentextur (§1) und Verdrängungsmitte c (§3) sind lokal feststellbar.
