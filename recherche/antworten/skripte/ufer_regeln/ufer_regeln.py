# -*- coding: utf-8 -*-
"""ufer_regeln.py - Referenz-Umsetzung von antworten/bachbett_ufer_regeln.json (Auftrag 16h) fuer Ferats lokales
Werkzeug (Bachdekor / s38 lagen). Nur Python-Standardbibliothek, keine Unreal-Importe, deterministisch.

  R = lade()                                        Regeln lesen
  pruefe(R)                                         Liste der Regel-Fehler (Summen, Lagen-Namen, Bereiche); leer = ok
  altbett_mischung(R, abschnitt, d_m, gleithang=False, versatz_m=0.0)
                                                    Teil A: Lagen-Prozent im alten Flussband nach Abstand zur Kante,
                                                    weich ueber die Bandgrenzen (versatz_m = Rauschen +-1,5 m je Ort)
  steil_mischung(R, neigung_grad, wandhoehe_m, fels_anstehend=False, nordseite=False)
                                                    Teil C2: Lagen auf Uferboeschungen (None unter 20 Grad)
  schichtband_maske(neigung_grad, wandhoehe_m, fels_anteil)   0..1 (V17-Baender nur auf Fels ab 3 m Wand)
  bachgewicht(R, breite_m), landschaft_wert(R, name, breite_m)  B2: Landschaftsmaterial Bach gegen Welt (Lerp)
  kasten_nah, boeschung_zweistufig, abtrag_m3, strecken_auswahl  16h Nachtrag 2: Kasten nur am Ufer, Zuruecklegen bis
                                                    zum Gelaende (32/38 Grad), Auswahl nach Fels-Anteil und Streckenlaenge
  toenung_neutral_gewicht(h_m, bachgewicht)         16h Nachtrag 2: Tal-Toenung unter Wasser und im Uferband neutral
  stein_an_lippe, flacher_stein_erlaubt             16h Nachtrag 5: Ausschluss am Hauptstrahl, flache Steine nur <= 35 Grad
  kasten_hoehe(querschnitt, grenze_grad=45)         groesste zusammenhaengende Hoehe steiler als grenze_grad
  boeschung_zuruecklegen(querschnitt, d_kante, ziel_grad=32)  Hang ab der Wasserkante zuruecklegen (nur abtragen)

Querschnitt = Liste (d_m, z_m) quer zum Bach, d aufsteigend ab der Wasserkante (aussen positiv).

Aufruf:  python -I recherche/antworten/skripte/ufer_regeln/ufer_regeln.py [--regeln PFAD]   (Selbsttest, Exit 1 bei FEHLER)
"""

import json
import math
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
REGELN_STANDARD = os.path.normpath(os.path.join(HIER, "..", "..", "bachbett_ufer_regeln.json"))


def lade(pfad=None):
    with open(pfad or REGELN_STANDARD, "r", encoding="utf-8") as f:
        return json.load(f)


def glatt01(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def smoothstep(a, b, x):
    return glatt01((x - a) / (b - a)) if b != a else (1.0 if x >= a else 0.0)


def _mischen(teile):
    """teile: [(gewicht, {lage: prozent})] -> {lage: prozent} mit Summe 100 (gerundet auf 0,1)."""
    out = {}
    g_sum = sum(g for g, _ in teile) or 1.0
    for g, m in teile:
        for k, v in m.items():
            out[k] = out.get(k, 0.0) + g * v / g_sum
    return {k: round(v, 1) for k, v in sorted(out.items()) if v > 0.05}


# ----------------------------------------------------------------------------------------------------------------------
# Pruefung der Regeldatei
# ----------------------------------------------------------------------------------------------------------------------
def _alle_mischungen(R):
    A = R["A_altbett"]
    for b in A["baender"]:
        for k in ("talkaskade", "kiesbett", "kiesbett_gleithang", "talkaskade_richtwert", "kiesbett_richtwert"):
            if k in b:
                yield "A_altbett.%s.%s" % (b["name"], k), b[k]
    for kl in R["C_ufer"]["lagen_steil"]["klassen"]:
        yield "C_ufer.lagen_steil.%s" % kl["name"], kl["lagen"]
    if "B2_landschaft_bach" in R:
        yield "B2_landschaft_bach.lagen_unter_spiegel", R["B2_landschaft_bach"]["lagen_unter_spiegel"]


def pruefe(R):
    fehler = []
    namen = set(R["lagen_namen"])
    for wo, m in _alle_mischungen(R):
        s = sum(m.values())
        if abs(s - 100.0) > 1e-6:
            fehler.append("%s: Summe %s statt 100" % (wo, s))
        for k in m:
            if k not in namen:
                fehler.append("%s: Lage %r gibt es nicht (FORMAT.md §2)" % (wo, k))
    bd = R["A_altbett"]["baender"]
    for a, b in zip(bd, bd[1:]):
        if a["d_m"][1] != b["d_m"][0]:
            fehler.append("A_altbett: Baender nicht lueckenlos (%s -> %s)" % (a["name"], b["name"]))
    for kl in R["C_ufer"]["lagen_steil"]["klassen"]:
        lo, hi = kl["neigung_grad"]
        if not 0 <= lo < hi <= 90:
            fehler.append("lagen_steil.%s: neigung_grad %s" % (kl["name"], kl["neigung_grad"]))
    p = R["C_ufer"]["profil"]["material"]["kies_geroell"]
    if not p["winkel_grad"][0] <= p["ziel_grad"] <= p["max_grad"] < 38:
        fehler.append("profil.kies_geroell: ziel/max muessen im Bereich und unter der Schichtband-Schwelle 38 Grad liegen")
    return fehler


# ----------------------------------------------------------------------------------------------------------------------
# Teil A: altes Flussband
# ----------------------------------------------------------------------------------------------------------------------
def _band_mischung(b, abschnitt, gleithang):
    if b["name"] == "umgebung":
        return b.get("%s_richtwert" % abschnitt) or b["talkaskade_richtwert"]
    if gleithang and ("%s_gleithang" % abschnitt) in b:
        return b["%s_gleithang" % abschnitt]
    return b.get(abschnitt) or b["talkaskade"]


def altbett_mischung(R, abschnitt, d_m, gleithang=False, versatz_m=0.0):
    """Lagen-Prozent bei Abstand d_m zur Wasserkante im alten Flussband. abschnitt: 'talkaskade' oder 'kiesbett'
    (andere Abschnitte wie talkaskade). Im Band 'umgebung' gilt lokal der Median der Umgebung; hier der Richtwert."""
    A = R["A_altbett"]
    U = A["uebergang"]
    d = d_m + versatz_m
    bd = A["baender"]
    br = float(U["breite_m"])
    teile = []
    for i, b in enumerate(bd):
        lo, hi = b["d_m"]
        w_in = 1.0 if i == 0 else smoothstep(lo - br / 2.0, lo + br / 2.0, d)
        w_out = 1.0 if i == len(bd) - 1 else 1.0 - smoothstep(hi - br / 2.0, hi + br / 2.0, d)
        w = w_in * w_out
        if w > 1e-6:
            teile.append((w, _band_mischung(b, abschnitt, gleithang)))
    return _mischen(teile)


def gras_dichte_faktor(R, d_m, versatz_m=0.0):
    A = R["A_altbett"]
    br = float(A["uebergang"]["breite_m"])
    d = d_m + versatz_m
    bd = A["baender"]
    f = sum(bd[0]["gras_dichte_faktor"]) / 2.0
    for a, b in zip(bd, bd[1:]):
        t = smoothstep(b["d_m"][0] - br / 2.0, b["d_m"][0] + br / 2.0, d)
        f = f + t * (sum(b["gras_dichte_faktor"]) / 2.0 - f)
    return round(f, 3)


# ----------------------------------------------------------------------------------------------------------------------
# Teil C2: Lagen auf steilen Ufern, Schichtbaender
# ----------------------------------------------------------------------------------------------------------------------
def _klasse(R, name):
    return next(k for k in R["C_ufer"]["lagen_steil"]["klassen"] if k["name"] == name)


def steil_mischung(R, neigung_grad, wandhoehe_m, fels_anstehend=False, nordseite=False):
    """Lagen-Prozent auf Uferboeschungen; None unter 20 Grad (dort Teil A bzw. Umgebung). Weich ueber die Klassengrenzen
    (uebergang_grad), Fels-Wand ab 3 m Wandhoehe bzw. auf anstehendem Fels."""
    L = R["C_ufer"]["lagen_steil"]
    ue = float(L["uebergang_grad"])
    n = float(neigung_grad)
    if n < 20.0 - ue / 2.0:
        return None
    w_steil = smoothstep(45.0 - ue / 2.0, 45.0 + ue / 2.0, n)
    w_mittel = smoothstep(32.0 - ue / 2.0, 32.0 + ue / 2.0, n)
    w_fels = 1.0 if fels_anstehend else smoothstep(2.5, 3.5, wandhoehe_m)
    teile = [((1.0 - w_mittel), _klasse(R, "boeschung_locker")["lagen"]),
             (w_mittel * (1.0 - w_steil), _klasse(R, "boeschung_steil")["lagen"]),
             (w_steil * (1.0 - w_fels), _klasse(R, "erdanriss")["lagen"]),
             (w_steil * w_fels, _klasse(R, "fels_wand")["lagen"])]
    m = _mischen([(g, x) for g, x in teile if g > 1e-6])
    if nordseite:
        plus = float(L["nordseite"]["moos_plus"])
        rest = plus
        for k in ("Trockengras", "Erde"):
            ab = min(m.get(k, 0.0), rest)
            if ab > 0:
                m[k] = round(m[k] - ab, 1)
                rest -= ab
        m["Moos"] = round(m.get("Moos", 0.0) + plus - rest, 1)
        m = {k: v for k, v in sorted(m.items()) if v > 0.05}
    return m


def bachgewicht(R, breite_m):
    """B2: 1 fuer Baeche (<= 6 m), 0 fuer Fluesse/Seen (>= 12 m), weich dazwischen."""
    a, b = R["B2_landschaft_bach"]["bachgewicht_breite_m"]
    return round(1.0 - smoothstep(a, b, breite_m), 4)


def landschaft_wert(R, name, breite_m):
    """B2: Parameter des Landschaftsmaterials als Lerp(Welt, Bach, Bachgewicht)."""
    e = R["B2_landschaft_bach"]["material"][name]
    g = bachgewicht(R, breite_m)
    if isinstance(e["welt"], list):
        return [round(w + g * (bv - w), 4) for w, bv in zip(e["welt"], e["bach"])]
    return round(e["welt"] + g * (e["bach"] - e["welt"]), 4)


def schichtband_maske(neigung_grad, wandhoehe_m, fels_anteil):
    """V17-Schichtbaender: smoothstep(38, 45, Neigung) x smoothstep(3, 4, Wandhoehe) x [Fels+Felsplatte >= 50 %]."""
    if fels_anteil < 0.5:
        return 0.0
    return round(smoothstep(38.0, 45.0, neigung_grad) * smoothstep(3.0, 4.0, wandhoehe_m), 4)


# ----------------------------------------------------------------------------------------------------------------------
# Teil C1: Profil
# ----------------------------------------------------------------------------------------------------------------------
def kasten_hoehe(querschnitt, grenze_grad=45.0):
    """Groesste zusammenhaengende Hoehe (m) der Abschnitte steiler als grenze_grad (Kasten-Pruefung)."""
    t = math.tan(math.radians(grenze_grad))
    best = cur = 0.0
    for (d0, z0), (d1, z1) in zip(querschnitt, querschnitt[1:]):
        dd, dz = d1 - d0, z1 - z0
        if dd > 1e-9 and abs(dz) / dd > t:
            cur += abs(dz)
            best = max(best, cur)
        else:
            cur = 0.0
    return round(best, 3)


def boeschung_zuruecklegen(querschnitt, d_kante, ziel_grad=32.0, korridor_max_m=4.0):
    """Nur abtragen: z_neu = min(z_alt, z_kante + (d - d_kante) * tan(ziel_grad)) fuer d_kante <= d <= d_kante +
    korridor_max_m. z_kante = Hoehe an der Wasserkante (interpoliert)."""
    pts = sorted(querschnitt)
    z_k = None
    for (d0, z0), (d1, z1) in zip(pts, pts[1:]):
        if d0 <= d_kante <= d1:
            z_k = z0 + (z1 - z0) * ((d_kante - d0) / (d1 - d0) if d1 > d0 else 0.0)
            break
    if z_k is None:
        z_k = pts[0][1] if d_kante < pts[0][0] else pts[-1][1]
    t = math.tan(math.radians(ziel_grad))
    out = []
    for d, z in pts:
        if d_kante <= d <= d_kante + korridor_max_m:
            z = min(z, z_k + (d - d_kante) * t)
        out.append((d, round(z, 4)))
    return out


def kasten_nah(querschnitt, d_max_m=4.0, grenze_grad=45.0):
    """16h Nachtrag 2: Kasten nur im Uferbereich (d <= d_max_m ab der Wasserkante). Steile Talhaenge weiter draussen sind
    natuerlich und kein gegrabener Kasten."""
    return kasten_hoehe([p for p in querschnitt if p[0] <= d_max_m + 1e-9], grenze_grad)


def boeschung_zweistufig(querschnitt, d_kante=0.0, grad_unten=32.0, h_wechsel_m=1.5, grad_oben=38.0, korridor_max_m=6.0):
    """16h Nachtrag 2: Hang ab der Wasserkante zuruecklegen, unten grad_unten bis h_wechsel_m ueber der Kante, darueber
    grad_oben, bis die Linie das Gelaende trifft (nur abtragen, hoechstens korridor_max_m). Anders als
    boeschung_zuruecklegen endet der Abtrag am Gelaende, nicht hart am Korridorrand (dort entstand sonst eine neue Stufe).
    Rueckgabe (profil_neu, d_schnitt_m: 0 = nichts zu tun, None = Linie trifft das Gelaende im Korridor nicht -> Uferfels
    statt Abtrag)."""
    pts = sorted(querschnitt)
    z_k = None
    for (d0, z0), (d1, z1) in zip(pts, pts[1:]):
        if d0 <= d_kante <= d1:
            z_k = z0 + (z1 - z0) * ((d_kante - d0) / (d1 - d0) if d1 > d0 else 0.0)
            break
    if z_k is None:
        z_k = pts[0][1] if d_kante < pts[0][0] else pts[-1][1]
    t1, t2 = math.tan(math.radians(grad_unten)), math.tan(math.radians(grad_oben))
    d_w = h_wechsel_m / t1

    def linie(d):
        x = d - d_kante
        return z_k + (x * t1 if x <= d_w else h_wechsel_m + (x - d_w) * t2)

    # letzter Punkt ueber der Linie im Korridor; der Abtrag endet am naechsten Punkt auf bzw. unter der Linie
    ueber = [i for i, (d, z) in enumerate(pts)
             if d_kante < d <= d_kante + korridor_max_m + 1e-9 and z > linie(d) + 1e-9]
    if not ueber:
        return [(d, round(z, 4)) for d, z in pts], 0.0
    nach = [i for i in range(ueber[-1] + 1, len(pts)) if pts[i][1] <= linie(pts[i][0]) + 1e-9]
    d_s = pts[nach[0]][0] if nach else None
    if d_s is None or d_s - d_kante > korridor_max_m:
        return [(d, round(z, 4)) for d, z in pts], None
    out = [(d, round(min(z, linie(d)) if d_kante <= d < d_s else z, 4)) for d, z in pts]
    return out, round(d_s - d_kante, 3)


def abtrag_m3(alt, neu, schritt_m=0.5, abstand_m=2.0):
    """Abtragvolumen eines Querschnitts (m3) bei Abtastung schritt_m und Querschnittsabstand abstand_m."""
    return round(sum(max(z0 - z1, 0.0) for (_, z0), (_, z1) in zip(sorted(alt), sorted(neu))) * schritt_m * abstand_m, 3)


def strecken_auswahl(eintraege, fels_max=0.5, min_folge=3):
    """16h Nachtrag 2: Zuruecklegen nur in zusammenhaengenden Strecken je Seite. eintraege: Liste dicts mit s, seite,
    kasten (bool, nah), fels_anteil (0..1 vor dem Graben, None = unbekannt -> zaehlt als Lockermaterial).
    Rueckgabe Menge (s, seite), die zurueckgelegt werden: Kasten und Fels < fels_max, in Folgen von >= min_folge
    Querschnitten (Abstand 2 m, eine Luecke von einem Querschnitt ueberbrueckt)."""
    out = set()
    for seite in sorted({e["seite"] for e in eintraege}):
        E = sorted((e for e in eintraege if e["seite"] == seite), key=lambda e: e["s"])
        ja = [e["kasten"] and (e.get("fels_anteil") is None or e["fels_anteil"] < fels_max) for e in E]
        # eine Luecke von einem Querschnitt ueberbruecken
        ja2 = list(ja)
        for i in range(1, len(ja) - 1):
            if not ja[i] and ja[i - 1] and ja[i + 1]:
                ja2[i] = True
        i = 0
        while i < len(E):
            if not ja2[i]:
                i += 1
                continue
            j = i
            while j + 1 < len(E) and ja2[j + 1]:
                j += 1
            if j - i + 1 >= min_folge:
                out |= {(E[k]["s"], seite) for k in range(i, j + 1) if ja[k] or ja2[k]}
            i = j + 1
    return out


def stein_an_lippe(s_m, d_m, lippen_s, regel=None):
    """16h Nachtrag 5: Stein im Hauptstrahl einer Lippe? |s - s_lippe| <= 0,75 m und d <= 0,5 m (statt Lippenzonen-Band)."""
    r = regel or {"s_m": 0.75, "d_max_m": 0.5}
    return d_m <= r["d_max_m"] and any(abs(s_m - sl) <= r["s_m"] for sl in lippen_s)


def flacher_stein_erlaubt(hoehe_m, laenge_m, neigung_grad, regel=None):
    """16h Nachtrag 5: flache Netze (Hoehe < 0,35 x Laenge) nur bis 35 Grad Uferneigung."""
    r = regel or {"hoehe_laenge_max": 0.35, "neigung_max_grad": 35.0}
    return not (hoehe_m < r["hoehe_laenge_max"] * laenge_m and neigung_grad > r["neigung_max_grad"])


def toenung_neutral_gewicht(h_m, bachgewicht, band=(0.3, 0.8)):
    """16h Nachtrag 2: Gewicht, mit dem die Houdini-Tal-Toenung auf neutral geht. h_m = Gelaende - Spiegel (m, unter
    Wasser negativ). Unter Wasser 1 (alle Gewaesser), im Uferband bis band[0] voll und bis band[1] auslaufend, dort nur
    mit dem Bachgewicht."""
    unter = 1.0 - smoothstep(-0.05, 0.05, h_m)
    ufer = bachgewicht * (1.0 - smoothstep(band[0], band[1], h_m))
    return round(max(unter, ufer), 4)


# ----------------------------------------------------------------------------------------------------------------------
# Selbsttest
# ----------------------------------------------------------------------------------------------------------------------
def selbsttest(R):
    f = list(pruefe(R))

    def ok(bed, txt):
        if not bed:
            f.append(txt)

    for ab in ("talkaskade", "kiesbett"):
        for d in (0.0, 3.0, 6.0, 9.0, 12.0, 20.0, 40.0):
            for v in (-1.5, 0.0, 1.5):
                m = altbett_mischung(R, ab, d, versatz_m=v)
                ok(abs(sum(m.values()) - 100.0) <= 0.6, "altbett %s d %s: Summe %s" % (ab, d, sum(m.values())))
        ok(altbett_mischung(R, ab, 2.0).get("Kies", 0) + altbett_mischung(R, ab, 2.0).get("Geroell", 0) >= 50,
           "altbett %s: Hochwasserbett ohne Kies/Geroell" % ab)
        ok(altbett_mischung(R, ab, 25.0).get("Kies", 0) <= 5, "altbett %s: Umgebung mit Kies > 5 %%" % ab)
    ok(gras_dichte_faktor(R, 2.0) < gras_dichte_faktor(R, 9.0) < gras_dichte_faktor(R, 20.0) == 1.0, "Grasdichte steigt nicht")
    ok(steil_mischung(R, 10.0, 0.5) is None, "steil unter 20 Grad nicht None")
    for n in (20, 25, 32, 40, 45, 50, 70, 85):
        for h in (0.5, 2.0, 3.0, 5.0):
            for nord in (False, True):
                m = steil_mischung(R, n, h, nordseite=nord)
                ok(m is not None and abs(sum(m.values()) - 100.0) <= 0.6, "steil %s/%s/%s: Summe" % (n, h, nord))
    ok(steil_mischung(R, 60, 1.0).get("Fels", 0) < 10, "Erdanriss mit viel Fels")
    ok(steil_mischung(R, 60, 5.0).get("Fels", 0) >= 40, "hohe Wand ohne Fels")
    ok(schichtband_maske(50, 2.0, 0.9) == 0.0, "Schichtband unter 3 m")
    ok(schichtband_maske(50, 5.0, 0.3) == 0.0, "Schichtband auf Lockermaterial")
    ok(schichtband_maske(50, 5.0, 0.8) == 1.0, "Schichtband auf hoher Felswand fehlt")
    ok(bachgewicht(R, 2.0) == 1.0 and bachgewicht(R, 20.0) == 0.0, "Bachgewicht")
    ok(landschaft_wert(R, "Ufer_Staerke", 2.0) == 0.0 and landschaft_wert(R, "Ufer_Staerke", 30.0) == 0.85, "Ufer_Staerke Bach/Welt")
    kasten = [(0.0, 0.0), (0.3, 1.2), (3.0, 1.4)]          # 76 Grad ueber 1,2 m: Kasten
    ok(kasten_hoehe(kasten) == 1.2, "Kasten nicht erkannt")
    neu = boeschung_zuruecklegen(kasten + [(1.0, 1.25), (2.0, 1.32)], 0.0)
    ok(kasten_hoehe(neu) == 0.0, "Zuruecklegen laesst Kasten stehen: %s" % neu)
    ok(all(z1 <= z0 + 1e-9 for (_, z0), (_, z1) in zip(sorted(kasten + [(1.0, 1.25), (2.0, 1.32)]), neu)),
       "Zuruecklegen hebt an")
    # 16h Nachtrag 2
    hoch = [(0.0, 0.0), (0.5, 1.0), (1.0, 2.0), (1.5, 2.6), (2.0, 3.0), (3.0, 3.1), (4.0, 3.2), (5.0, 3.3), (6.0, 3.4)]
    neu2, ds = boeschung_zweistufig(hoch, 0.0)
    ok(ds is not None and kasten_hoehe([p for p in neu2 if p[0] <= ds + 1.0]) <= 0.6, "zweistufig laesst Kasten: %s" % neu2)
    ok(all(z1 <= z0 + 1e-9 for (_, z0), (_, z1) in zip(hoch, neu2)), "zweistufig hebt an")
    ok(abtrag_m3(hoch, neu2) > 0, "zweistufig ohne Abtrag")
    wand = [(0.0, 0.0), (0.5, 2.0), (1.0, 4.0), (2.0, 6.0), (4.0, 8.0), (6.0, 10.0), (8.0, 12.0)]
    ok(boeschung_zweistufig(wand, 0.0)[1] is None, "hohe Wand muss offen bleiben (Uferfels)")
    ok(kasten_nah([(0.0, 0.0), (1.0, 0.3), (5.0, 1.0), (5.5, 2.5)]) == 0.0, "Talhang weit draussen als Kasten gezaehlt")
    E = [{"s": 2.0 * i, "seite": "links", "kasten": i in (1, 2, 3, 5, 9), "fels_anteil": 0.8 if i == 5 else 0.1}
         for i in range(12)]
    sel = strecken_auswahl(E)
    ok(sel == {(2.0, "links"), (4.0, "links"), (6.0, "links")}, "strecken_auswahl: %s" % sorted(sel))
    ok(toenung_neutral_gewicht(-0.3, 0.0) == 1.0 and toenung_neutral_gewicht(0.2, 1.0) == 1.0
       and toenung_neutral_gewicht(0.2, 0.0) == 0.0 and toenung_neutral_gewicht(1.0, 1.0) == 0.0, "Toenung-Gewicht")
    ok(stein_an_lippe(10.5, 0.3, [10.0]) and not stein_an_lippe(10.5, 0.8, [10.0])
       and not stein_an_lippe(11.0, 0.2, [10.0]), "Lippen-Ausschluss Steine")
    ok(flacher_stein_erlaubt(0.13, 0.52, 30.0) and not flacher_stein_erlaubt(0.13, 0.52, 45.0)
       and flacher_stein_erlaubt(0.3, 0.42, 50.0), "flache Steine")
    return f


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Referenz und Selbsttest fuer bachbett_ufer_regeln.json (16h)")
    ap.add_argument("--regeln", default=None)
    a = ap.parse_args(argv)
    R = lade(a.regeln)
    f = selbsttest(R)
    for x in f:
        print("FEHLER", x)
    print("Beispiele (Prozent):")
    for ab in ("talkaskade", "kiesbett"):
        for d in (2.0, 6.0, 9.0, 12.0, 20.0):
            print("  %-10s d %4.1f m: %s" % (ab, d, altbett_mischung(R, ab, d)))
    for n, h in ((25, 0.8), (38, 1.2), (55, 1.2), (55, 4.0)):
        print("  steil %2d Grad, Wand %.1f m: %s" % (n, h, steil_mischung(R, n, h)))
    print("[ufer_regeln] Selbsttest: %d FEHLER" % len(f))
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
