#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plan_erzeugen.py - Auftrag 14: Nature Water FX an Wasserfaellen und Bachstufen.

Liest  recherche/vorlagen/daten/wasser_fx/{wasserfaelle,stufen_netze,stufen_fluss_teile}.json
       (optional) die Phase-2-Planausgaben aus Auftrag 13 (--sehens13 <Ordner mit <biom>/orte.json>)
Schreibt recherche/antworten/wasser_fx/plan.json  (Format SEHENS_FORMAT.md par. 6, typ "niagara", plus Erweiterungen)

Aufruf (nur Standardbibliothek):
  python -I recherche/antworten/wasser_fx/plan_erzeugen.py [--sehens13 <Ordner>] [--aus <Datei>]

Konventionen (wie sehens_lib/rezept.py, Niagara-Yaw-Logik):
  - Welt-cm, UE-Achsen (X Ost, Y Sued, Z oben). Kompass 0 = Nord = -Y, 90 = Ost = +X.
  - rot_q = [x, y, z, w], reine Drehung um Z, legt die LOKALE +X-Achse des Systems in Fliessrichtung
    (= q_yaw_kompass(kompass) der Lib). yaw_ue_grad = atan2(dy, dx) in Grad (Unreal-Rotator Yaw).
"""
import argparse
import glob
import hashlib
import json
import math
import os

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HIER, "..", "..", ".."))
DATEN = os.path.join(REPO, "recherche", "vorlagen", "daten", "wasser_fx")
FX = "/Game/NatureWaterFX/FX/"
CUE = "/Game/City_Nature_Sounds/CUE/"

# Annahmen fuer die Skala (Groesse der Systeme bei Skala 1). Nirgends veroeffentlicht -> [ungeprueft],
# im Editor die Fixed Bounds bzw. die sichtbare Groesse ablesen und skala = ziel / gemessen neu rechnen.
REF_M = {
    "NS_Waterfall_Small": {"breite": 3.0, "hoehe": 5.0},
    "NS_Waterfall_Medium": {"breite": 6.0, "hoehe": 15.0},
    "NS_Waterfall_Large": {"breite": 12.0, "hoehe": 30.0},
    "NS_Impact_Small": {"durchmesser": 3.0},
    "NS_Impact_Medium": {"durchmesser": 6.0},
    "NS_Impact_Large": {"durchmesser": 12.0},
    "NS_Wake_Small": {"durchmesser": 3.0},
    "NS_Wake_Medium": {"durchmesser": 6.0},
    "NS_Wake_Large": {"durchmesser": 12.0},
    "NS_Stream_Small": {"breite": 2.0, "laenge": 5.0},
    "NS_Stream_Medium": {"breite": 4.0, "laenge": 10.0},
    "NS_Stream_Large": {"breite": 8.0, "laenge": 20.0},
}

CULL_M = {  # Ableitung aus Antwort 12 Teil A (40-60 m), Heldenfaelle begruendet weiter
    "held_fall": 150, "held_aufprall": 100, "held_wake": 60,
    "NS_Waterfall_Small": 45, "NS_Impact_Small": 30, "NS_Stream_Small": 30, "NS_Stream_Medium": 45, "NS_Wake_Small": 30,
}
SORT = 2  # Antwort 12: Vorhang 0, Schaum 1, Gischt (Niagara) 2


def lade(name):
    with open(os.path.join(DATEN, name), encoding="utf-8") as f:
        return json.load(f)


def r(v, n=1):
    return round(float(v), n)


def einheit(dx, dy):
    l = math.hypot(dx, dy)
    return (dx / l, dy / l)


def yaw_ue(d):
    return math.degrees(math.atan2(d[1], d[0]))


def kompass(d):
    return math.degrees(math.atan2(d[0], -d[1])) % 360.0


def quat_yaw(yaw_grad):
    a = math.radians(yaw_grad) / 2.0
    return [0.0, 0.0, round(math.sin(a), 5), round(math.cos(a), 5)]


def eintrag(ziel, gruppe, rolle, name, pos, d, skala, cull, optional, zweck, bezug, user=None, skala_grund=""):
    y = yaw_ue(d)
    return {
        "typ": "niagara",
        "asset": FX + name,
        "pos_cm": [round(pos[0], 1), round(pos[1], 1), round(pos[2], 1)],
        "rot_q": quat_yaw(y),
        "yaw_ue_grad": r(y, 1),
        "kompass_grad": r(kompass(d), 1),
        "skala": r(skala, 2),
        "skala_grund": skala_grund,
        "cull_m": cull,
        "sort_priority": SORT,
        "cast_shadow": False,
        "user_parameter": user or {"ungeprueft": True, "wunsch": {}},
        "ziel": ziel,
        "gruppe": gruppe,
        "rolle": rolle,
        "bezug": bezug,
        "optional": optional,
        "zweck": zweck,
    }


def klang(ziel, cue, pos, radius_m, laut, zweck, luecke=None):
    k = {"ziel": ziel, "asset": CUE + cue, "pos_cm": [round(p, 1) for p in pos], "radius_cm": int(radius_m * 100),
         "lautstaerke": laut, "zweck": zweck, "inhalt_ungeprueft": True}
    if luecke:
        k["luecke"] = luecke
    return k


# ---------------------------------------------------------------- grosse Faelle
def grosse_faelle(wf, eff, kl):
    farbe = {"WF_K1": [0.82, 0.86, 0.88], "WF_K8": [0.74, 0.79, 0.81]}   # K8 liegt in praller Sonne (Bild WASSER3_H4_*)
    for fid in ("WF_K1", "WF_K8"):
        w = wf["wasserfaelle"][fid]
        L, F, G, B = w["lippe"], w["fuss"], w["gischt"], w["becken"]
        d = einheit(*L["richtung_fall"])
        breite = L["breite_m"]
        fall = w["vorhang"]["fallhoehe_m"]
        z_kante = L["spiegel_m"] * 100.0
        z_becken = B["spiegel_cm"]
        # Anteil des Vorhangs, der im Becken aufschlaegt (K1: Spalten 13-26 von 27, links trifft Gelaende)
        sp = w["vorhang"]["spalten"]
        im_becken = sum(a["spalten"][1] - a["spalten"][0] + 1 for a in w["aufprall"] if a["art"] == "becken")
        breite_becken = breite * im_becken / sp
        g = fid
        # 1) Fall an der Kante: 0,3 m vor der Lippe, 5 cm ueber dem Spiegel (Vorhang liegt 3 cm darueber)
        pos = (L["x_cm"] + 30 * d[0], L["y_cm"] + 30 * d[1], z_kante + 5)
        sk = breite / REF_M["NS_Waterfall_Large"]["breite"]
        eff.append(eintrag(fid, g, "fall", "NS_Waterfall_Large", pos, d, sk, CULL_M["held_fall"], False,
                           "Fallstraehnen und Schleier vor dem Vorhang, %.1f m breit, %.1f m Fall" % (breite, fall),
                           "lippe + 0,3 m in Fallrichtung, Spiegel + 5 cm",
                           {"ungeprueft": True, "wunsch": {"Farbe/Tint": farbe[fid], "Breite_m": breite,
                                                           "Lebensdauer": "so, dass Partikel bis %.0f m tief fallen (Fall %.1f m)" % (fall - 2, fall)}},
                           "Breite %.1f m / Annahme 12 m bei Skala 1; Hoehe ergibt sich aus Schwerkraft x Lebensdauer, nicht aus der Skala" % breite))
        # 2) Aufprall an der Gischt-Stelle, auf dem Beckenspiegel
        pos = (G["x_cm"], G["y_cm"], z_becken + 10)
        ziel_d = max(8.0, min(breite_becken, 16.0))
        sk = ziel_d / REF_M["NS_Impact_Large"]["durchmesser"]
        eff.append(eintrag(fid, g, "aufprall", "NS_Impact_Large", pos, d, sk, CULL_M["held_aufprall"], False,
                           "Aufprall-Gischt im Becken (%.1f m der Vorhangbreite treffen das Becken)" % breite_becken,
                           "gischt_cm (x, y), Beckenspiegel + 10 cm",
                           {"ungeprueft": True, "wunsch": {"Farbe/Tint": farbe[fid], "Spawnrate": "Standard",
                                                           "Nebelhoehe_m": "8-12 (Gischtwolke ueber dem Becken)"}},
                           "Ziel-Durchmesser %.1f m / Annahme 12 m" % ziel_d))
        # 3) Oberflaechen-Wellen (Wake) 5 m hinter der Gischt, Richtung Abfluss
        pos = (G["x_cm"] + 500 * d[0], G["y_cm"] + 500 * d[1], z_becken + 3)
        eff.append(eintrag(fid, g, "wake", "NS_Wake_Large", pos, d, 1.0, CULL_M["held_wake"], False,
                           "Schaumringe und Wirbel auf dem Becken (laut Hersteller eigenes System zum Fall)",
                           "gischt_cm + 5 m in Fallrichtung, Beckenspiegel + 3 cm",
                           {"ungeprueft": True, "wunsch": {"Farbe/Tint": farbe[fid]}},
                           "Becken %d m2; Skala 1 als Start" % B["flaeche_m2"]))
        kl.append(klang(fid, "CUE_Water_Stream_IX_Cue", (G["x_cm"], G["y_cm"], z_becken + 150), 90, 1.0,
                        "Fallrauschen am Fuss (wie Bergwald-Klamm)",
                        "Kein echtes Wasserfall-Tosen im Inventar (nur Water_Stream I-X) -> Wunsch: Wasserfall-Klangpaket"))
        kl.append(klang(fid, "CUE_Water_Stream_IV_Cue", (L["x_cm"], L["y_cm"], z_kante + 150), 35, 0.6,
                        "Rauschen an der Kante (oben, fuer Spieler auf dem Zulauf)"))


# ---------------------------------------------------------------- Bachstufen
def stufen_daten(netze, teile):
    """Je Stufe: Kante (vorletzter Punkt des oberen Flussstuecks = Kante, Stueck endet 0,5 m dahinter), Fuss, Gischt."""
    abschnitte = {}
    for f in teile["fluesse"]:
        for a in f["abschnitte"]:
            abschnitte[a["id"]] = a
    aus = {}
    for nid, v in netze["verzeichnis"].items():
        for s in v.get("stufen", []):
            e = {"id": s["id"], "art": s["art"], "fall_m": s["fall_m"], "breite_m": s["breite_m"],
                 "lippe": s["lippe_cm"], "fuss": s["fuss_cm"], "richtung": s.get("richtung"), "gischt": s.get("gischt_cm"),
                 "s_lippe": s["s_lippe_m"], "s_fuss": s["s_fuss_m"], "feld": s["feld"]}
            if "fall_teil" in s:
                ft = s["fall_teil"]
                ob = abschnitte[ft["oberes_stueck"]]["punkte"]
                un = abschnitte[ft["unteres_stueck"]]["punkte"]
                e["kante"] = ob[-2][:3]
                e["unten_anfang"] = un[0][:3]
                e["fall_vorhang_m"] = ft["fall_m"]
                e["breite_kante_m"] = s["vorhang"]["breite_kante_m"]
                e["s_kante"] = s["vorhang"]["kante_s_m"]
            if "schnelle" in s:
                e["schnelle_breite_m"] = s["schnelle"]["breite_mittel_m"]
                e["schnelle_laenge_m"] = s["schnelle"]["laenge_m"]
            if s["id"] not in aus or "kante" in e:
                aus[s["id"]] = e
    # Fliessrichtung je Stufe: Kante -> Anfang unteres Stueck (Fall) bzw. Lippe -> Fuss (Schnelle)
    for e in aus.values():
        if "kante" in e:
            e["d"] = einheit(e["unten_anfang"][0] - e["kante"][0], e["unten_anfang"][1] - e["kante"][1])
        else:
            e["d"] = einheit(e["fuss"][0] - e["lippe"][0], e["fuss"][1] - e["lippe"][1])
    return aus


def mitte(a, b):
    return [(a[i] + b[i]) / 2.0 for i in range(3)]


def c2_h4(st, eff, kl):
    S = lambda i: st["F_ERLENBACH_1V_C2_S%02d" % i]
    nix = {"ungeprueft": True, "wunsch": {"Farbe/Tint": [0.80, 0.84, 0.86], "Spawnrate": "0,6-0,8 x Standard (dichte Kaskade)"}}

    def wf_small(i, grp, opt, zweck):
        e = S(i)
        d = e["d"]
        k = e["kante"]
        pos = (k[0] + 20 * d[0], k[1] + 20 * d[1], k[2] + 5)
        eff.append(eintrag(e["id"], grp, "fall", "NS_Waterfall_Small", pos, d, 1.0, CULL_M["NS_Waterfall_Small"], opt, zweck,
                           "Kante (Ende oberes Flussstueck - 0,5 m) + 0,2 m, Spiegel oben + 5 cm", dict(nix),
                           "Skala 1: Breite ~3 m (Annahme) = Mittelstrang auf %.1f m Vorhang; zu hohe Partikel verschwinden unter dem Spiegel" % e["breite_kante_m"]))

    def impact(i, grp, opt, zweck):
        e = S(i)
        g = e["gischt"]
        pos = (g[0], g[1], e["unten_anfang"][2] + 10)
        eff.append(eintrag(e["id"], grp, "aufprall", "NS_Impact_Small", pos, e["d"], 1.0, CULL_M["NS_Impact_Small"], opt, zweck,
                           "gischt_cm (x, y), Spiegel unteres Flussstueck + 10 cm", dict(nix),
                           "Ziel-Durchmesser ~3 m (Vorhang unten %.1f m breit, Schaumscheibe bleibt)" % e.get("breite_kante_m", 0)))

    def stream_lippe(i, grp, opt, zweck):
        e = S(i)
        d = e["d"]
        k = e["kante"]
        pos = (k[0] - 100 * d[0], k[1] - 100 * d[1], k[2] + 10)
        eff.append(eintrag(e["id"], grp, "stroemung", "NS_Stream_Small", pos, d, 1.0, CULL_M["NS_Stream_Small"], opt, zweck,
                           "Kante - 1,0 m (stromauf), Spiegel oben + 10 cm", dict(nix),
                           "Breite ~2 m (Annahme) = Zunge in der Bachmitte"))

    def stream_schnelle(e, grp, name, opt, zweck, cull):
        m = mitte(e["lippe"], e["fuss"])
        pos = (m[0], m[1], m[2] + 10)
        ref = REF_M[name]["breite"]
        # gleichmaessige Skala: die kleinere von Breiten- und Laengenverhaeltnis (sonst schiesst das System ueber die Schnelle hinaus)
        skala = min(e["schnelle_breite_m"] / ref, e["schnelle_laenge_m"] / REF_M[name]["laenge"])
        eff.append(eintrag(e["id"], grp, "schnelle", name, pos, e["d"], skala, cull, opt, zweck,
                           "Mitte Lippe-Fuss der Schnelle, Spiegel + 10 cm",
                           {"ungeprueft": True, "wunsch": {"Farbe/Tint": [0.80, 0.84, 0.86], "Laenge_m": e["schnelle_laenge_m"],
                                                           "Breite_m": round(e["schnelle_breite_m"], 1)}},
                           "Schnelle %.1f m breit, %.1f m lang; Annahme %s %.0f x %.0f m bei Skala 1 -> min(Breite, Laenge)" % (
                               e["schnelle_breite_m"], e["schnelle_laenge_m"], name, ref, REF_M[name]["laenge"])))

    # C2 - vier Stufengruppen, je <= 3 Systeme
    stream_schnelle(S(0), "C2_A", "NS_Stream_Medium", False, "Schnelle S00 (3,3 m auf 10,6 m, Bach 15-19 m breit)",
                    CULL_M["NS_Stream_Medium"])
    wf_small(1, "C2_B", False, "Probestufe: Fallstraehnen ueber dem Vorhang (3,3 m Fall, zweithoechste Kante)")
    impact(1, "C2_B", False, "Gischt am Fuss von S01")
    # S02 (3,2 m) bewusst ohne Impact: 8 m neben S01, Budget gleichzeitig <= 6 (Schaumscheibe + Vorhang bleiben)
    impact(3, "C2_C", False, "Gischt am Fuss von S03 (2,4 m Fall nach kurzer Schnelle)")
    stream_lippe(4, "C2_C", False, "Wasser zieht ueber die Lippe von S04 (abwechselnd Impact/Stream)")
    impact(5, "C2_C", False, "Gischt am Fuss von S05")
    wf_small(7, "C2_D", True, "Fallstraehnen an S07 (groesste Stufe: 5,3 m mit Schnelle) - erst setzen, wenn die Probe an S01 ueberzeugt")
    impact(7, "C2_D", False, "Gischt am Fuss von S07")
    impact(9, "C2_E", False, "Gischt am Fuss von S09")
    stream_schnelle(S(11), "C2_E", "NS_Stream_Small", False, "Auslauf-Schnelle S11 (1,6 m auf 4,7 m)",
                    CULL_M["NS_Stream_Small"])

    # H4 - zwei Schnellen (Schnellen-Haut bleibt ausgeblendet)
    h0, h1 = st["F_ELFENFLUSS_2_H4_S00"], st["F_ELFENFLUSS_2_H4_S01"]
    stream_schnelle(h0, "H4_A", "NS_Stream_Medium", False, "Schnelle S00 (1,6 m auf 5 m, 11 m breit)",
                    CULL_M["NS_Stream_Medium"])
    stream_schnelle(h1, "H4_A", "NS_Stream_Medium", False, "Schnelle S01 (4,2 m auf 10 m, staerkste Schnelle)",
                    CULL_M["NS_Stream_Medium"])
    d = h1["d"]
    f = h1["fuss"]
    eff.append(eintrag(h1["id"], "H4_A", "wake", "NS_Wake_Small", (f[0] + 150 * d[0], f[1] + 150 * d[1], f[2] + 3), d, 1.0,
                       CULL_M["NS_Wake_Small"], True, "Schaumwirbel im Kehrwasser unter S01 (optional)",
                       "fuss_cm + 1,5 m in Fliessrichtung, Spiegel + 3 cm",
                       {"ungeprueft": True, "wunsch": {"Farbe/Tint": [0.80, 0.84, 0.86]}}, "Skala 1 als Start"))

    # Klaenge (verschiedene Cues nebeneinander, damit nichts phasig doppelt klingt)
    for grp, cue, i, rad, laut, zw in (("C2_A", "CUE_Water_Stream_II_Cue", 0, 30, 0.5, "Schnelle oben"),
                                       ("C2_B", "CUE_Water_Stream_VIII_Cue", 1, 30, 0.7, "Stufen S01/S02"),
                                       ("C2_C", "CUE_Water_Stream_X_Cue", 4, 30, 0.7, "Stufen S03-S06"),
                                       ("C2_D", "CUE_Water_Stream_V_Cue", 7, 30, 0.7, "Stufe S07/S08"),
                                       ("C2_E", "CUE_Water_Stream_I_Cue", 10, 25, 0.5, "Stufen S09-S11, leiser Auslauf")):
        e = S(i)
        p = e.get("gischt") or mitte(e["lippe"], e["fuss"])
        kl.append(klang(e["id"], cue, (p[0], p[1], p[2] + 150), rad, laut, zw))
    for e, cue, zw in ((h0, "CUE_Water_Stream_VI_Cue", "Schnelle S00"), (h1, "CUE_Water_Stream_VII_Cue", "Schnelle S01")):
        p = mitte(e["lippe"], e["fuss"])
        kl.append(klang(e["id"], cue, (p[0], p[1], p[2] + 150), 35, 0.7, zw))


# ---------------------------------------------------------------- Material
def material():
    master = "/Game/Eldarien/Welt/Wasser/Wasserfall_v2/M_EL_Wasserfall2"
    return {
        "hinweis": "Nur Parameter aus material_parameter.json (Master M_EL_Wasserfall2). Ist-Werte der Instanzen stehen dort nicht; "
                   "'ist' nur, wo der Auftrag sie nennt. Ein MI gilt fuer ALLE Stufen eines Netzes (ein Vorhang-Netz fuer C2) - "
                   "stufenweise Werte gehen nicht.",
        "MI_EL_Wasserfall": {
            "pfad": "/Game/Eldarien/Welt/Wasser/Wasserfall_v2/MI_EL_Wasserfall", "master": master, "gilt_fuer": ["WF_K1", "WF_K8"],
            "vorhang": "bleibt, NS ergaenzt",
            "parameter": {"Schaum_Menge": 0.9, "Straehnen_Staerke": 0.8, "Schaum_Leuchten": 0.0, "Rand_Durchsicht": 0.8,
                          "Deckkraft": 0.9, "Tiefenblende_cm": 60.0, "Schaumfarbe": [0.80, 0.84, 0.86, 1.0],
                          "Wasserfarbe": [0.14, 0.22, 0.24, 1.0]},
            "grund": "K8 brennt in der Sonne weiss aus, K1 wirkt flach: weniger und dunklerer Schaum, mehr Straehnen; das Weiss am Fuss "
                     "liefert jetzt NS_Impact_Large."},
        "MI_EL_Wasserfall_Aufprall": {
            "pfad": "/Game/Eldarien/Welt/Wasser/Wasserfall_v2/MI_EL_Wasserfall_Aufprall", "master": master, "gilt_fuer": ["WF_K1", "WF_K8"],
            "parameter": {"Deckkraft": 0.6, "Schaum_Menge": 1.0, "Schaum_Leuchten": 0.0, "Tiefenblende_cm": 40.0},
            "grund": "Scheibe bleibt fuer die Ferne (jenseits Cull 100 m), nah traegt NS_Impact_Large."},
        "MI_EL_Stufenfall_Vorhang": {
            "pfad": "/Game/Eldarien/Welt/Wasser/Stufenfall/MI_EL_Stufenfall_Vorhang", "master": master, "gilt_fuer": ["F_ERLENBACH_1V_C2 S01-S10"],
            "vorhang": "bleibt (deckt die 1,3-3 m Luecken der Flussstuecke, auch jenseits der Cull-Distanz)",
            "ist": {"Deckkraft": 0.55, "Schaum_Menge": 0.45, "quelle": "Auftrag 14 (Stand 16:04), Zuordnung 0,55/0,45 = Vorhang/Schaum angenommen"},
            "parameter": {"Deckkraft": 0.5, "Schaum_Menge": 0.3, "Straehnen_Staerke": 0.85, "Rand_Durchsicht": 0.85,
                          "Schaum_Leuchten": 0.0, "Tiefenblende_cm": 30.0, "Schaumfarbe": [0.80, 0.84, 0.85, 1.0],
                          "Wasserfarbe": [0.12, 0.20, 0.21, 1.0]},
            "falls_probe_S01_gut": {"Deckkraft": 0.4, "Schaum_Menge": 0.2},
            "grund": "Weisse Kacheln = gleichmaessiger Schaum ueber die ganze Flaeche + harte Raender: Schaum runter, Straehnen und "
                     "Randdurchsicht rauf, Glanz statt Leuchten; Gischt/Weiss kommt nah aus NS_Impact_Small."},
        "MI_EL_Stufenfall_Schaum": {
            "pfad": "/Game/Eldarien/Welt/Wasser/Stufenfall/MI_EL_Stufenfall_Schaum", "master": master,
            "gilt_fuer": ["F_ERLENBACH_1V_C2 alle Stufen", "F_ELFENFLUSS_2_H4 Schnellen"],
            "ist": {"Deckkraft": 0.45, "Schaum_Menge": 0.55, "quelle": "Auftrag 14 (Stand 16:04), Zuordnung angenommen"},
            "parameter": {"Deckkraft": 0.4, "Schaum_Menge": 0.5, "Schaum_Leuchten": 0.0, "Tiefenblende_cm": 20.0,
                          "Schaumfarbe": [0.82, 0.86, 0.87, 1.0]},
            "grund": "Scheibe bleibt an allen Stufen (auch ohne Impact), etwas leiser, weil nah NS darueberliegt."},
        "MI_EL_Stufenfall_Schnelle": {
            "pfad": "/Game/Eldarien/Welt/Wasser/Stufenfall/MI_EL_Stufenfall_Schnelle", "master": master,
            "parameter": {}, "grund": "keine Aenderung; H4-Schnellen-Haut bleibt ausgeblendet, NS_Stream_Medium ersetzt sie."},
    }


# ---------------------------------------------------------------- Auftrag 13 (nur Uebersicht)
def sehens13(ordner, eff):
    if not ordner or not os.path.isdir(ordner):
        return None
    aus = {"hinweis": "Nur Uebersicht, NICHT doppelt setzen: diese Effekte liefern die Sehenswuerdigkeiten-Planer (Auftrag 13, Phase 2) "
                      "mit orte.json -> effekte selbst. Uebernommen ist nur, was dort steht (NatureWaterFX-Systeme). "
                      "'Der Atem' ist in Auftrag 13 gestrichen.",
           "quelle": "scratchpad a13/p2/<biom>/orte.json (Cloud-Testlauf 2 m)", "orte": []}
    for f in sorted(glob.glob(os.path.join(ordner, "*", "orte.json"))):
        biom = os.path.basename(os.path.dirname(f))
        if "_" in biom or biom.startswith("bw"):
            continue  # Zwischenlaeufe (aue_lauf1, kueste_b, bw_alt ...) auslassen
        with open(f, "rb") as h:
            roh = h.read()
        d = json.loads(roh.decode("utf-8"))
        for o in d["orte"]:
            fx = [e for e in o.get("effekte", []) if e.get("typ") == "niagara" and "/NatureWaterFX/" in e.get("asset", "")]
            if not fx:
                continue
            aus["orte"].append({
                "biom": biom, "ort": o["id"], "name": o["name"], "felder": o.get("felder"),
                "datei_sha1": hashlib.sha1(roh).hexdigest()[:12], "datei_stand": d.get("stand"),
                "niagara_gesamt": sum(1 for e in o.get("effekte", []) if e.get("typ") == "niagara"),
                "effekte": [_konflikt({k: e[k] for k in ("typ", "asset", "pos_cm", "rot_q", "skala", "optional", "zweck") if k in e}, eff)
                            for e in fx],
                "klaenge": [k for k in o.get("klaenge", []) if "Water" in k.get("asset", "")],
            })
    return aus


def _konflikt(e, eff):
    """Markiert A13-Effekte, die naeher als 150 m an einem A14-Effekt liegen (gleicher Bach = Doppelung)."""
    nah = min(eff, key=lambda x: math.dist(x["pos_cm"], e["pos_cm"]))
    a = math.dist(nah["pos_cm"], e["pos_cm"]) / 100.0
    if a < 150:
        e["konflikt"] = ("%.1f m neben A14 %s (%s, %s). A14 behaelt den Platz; der A13-Planer sollte diesen Effekt "
                         "streichen oder verlegen - Rueckfrage im Bericht." % (a, nah["ziel"], nah["rolle"], nah["asset"].split("/")[-1]))
    return e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sehens13", default=None)
    ap.add_argument("--aus", default=os.path.join(HIER, "plan.json"))
    a = ap.parse_args()
    wf = lade("wasserfaelle.json")
    netze = lade("stufen_netze.json")
    teile = lade("stufen_fluss_teile.json")
    eff, kl = [], []
    grosse_faelle(wf, eff, kl)
    st = stufen_daten(netze, teile)
    c2_h4(st, eff, kl)
    gruppen = {}
    for e in eff:
        gruppen.setdefault(e["gruppe"], []).append(e["ziel"].split("_")[-1] + ":" + e["asset"].split("/")[-1])
    plan = {
        "stand": "2026-10-11",
        "auftrag": "14 - Nature Water FX an Wasserfaellen und Bachstufen",
        "format": "vorlagen/SEHENS_FORMAT.md par. 6 (typ niagara) + cull_m, sort_priority, user_parameter, ziel, gruppe",
        "erzeugt_von": "recherche/antworten/wasser_fx/plan_erzeugen.py",
        "quellen_daten": {n: lade(n).get("stand") for n in ("wasserfaelle.json", "stufen.json", "stufen_netze.json", "stufen_fluss_teile.json")},
        "einstellungen_alle": {
            "akteur": "NiagaraActor im Feld-Ordner Kacheln/<Feld>/Wasser, Label FX14_<ziel>_<rolle>",
            "sim_target": "GPU (CPU-Emitter des Pakets nicht umbauen, nur messen)",
            "cast_shadow": False,
            "translucency_sort_priority": SORT,
            "max_draw_distance_cm": "= cull_m x 100 (Komponente: Max Draw Distance)",
            "effect_type_vorschlag": {"NET_EL_Wasser_Held": {"max_distance_m": 150, "fuer": "WF_K1/WF_K8"},
                                      "NET_EL_Wasser_Nah": {"max_distance_m": 50, "fuer": "Bachstufen"}},
            "hlod": "aus (Include in HLOD = false)",
            "pool": "nicht noetig (fest gesetzte Akteure); nur bei Laufzeit-Spawn PoolingMethod AutoRelease",
            "yaw_konvention": "lokale +X-Achse des Systems = Fliessrichtung (wie Bergwald-Klamm, q_yaw_kompass). "
                              "Zeigt das Paket-System lokal anders (z. B. +Y), yaw_korrektur_grad einmal fuer alle setzen.",
            "yaw_korrektur_grad": 0,
            "skala_annahme_m": REF_M,
        },
        "effekte": eff,
        "gruppen": gruppen,
        "budget": {"je_ort_oder_gruppe_max": 3, "gleichzeitig_aktiv_ziel_max": 6},
        "material": material(),
        "klang": kl,
    }
    s13 = sehens13(a.sehens13, eff)
    if s13:
        plan["sehens13"] = s13
    with open(a.aus, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    print("geschrieben:", a.aus, "-", len(eff), "Niagara,", len(kl), "Klaenge,", len(s13["orte"]) if s13 else 0, "Orte aus A13")


if __name__ == "__main__":
    main()
