"""see_bloecke.py - Auftrag 13h, Nachtrag 12.10. 01:00 (Ferat): Bloecke in geplanten Seen nie knapp unter dem Spiegel.

Befund (Karsee, Punkt 3): Zwei Felsbloecke lagen knapp unter dem Seespiegel; ihr helles Moos schien durch das Wasser
und wurde von den Wellen in grelle Streifen gebrochen. Regel fuer alle Planer: Fels/Steine >= 0,8 m in einem geplanten
See ragen entweder deutlich heraus (Oberkante >= Spiegel + 0,3 m) oder liegen tiefer als 1,5 m unter dem Spiegel
(Oberkante <= Spiegel - 1,5 m) - nie dazwischen.

  korrigieren(ctx)                                  Planer (rezept.baue, nach den Gruppen): Stuecke heben/senken/entfernen
  pruefe_orte_see_bloecke(d, welt, sw_ordner, inv)  Pruefer: FEHLER je Ort mit Anzahl und Beispiel
"""

import numpy as np

UEBER_M = 0.3
UNTER_M = 1.5
MIN_GROESSE_M = 0.8
MAX_HEBEN_M = 0.8
FELS_ROLLEN = ("fels", "stein")


def _oberkante(info, q, s, z_cm):
    from . import instanzen as _ins
    P = _ins.gedrehte_box(info, q, s)
    return (z_cm + float(P[:, 2].max())) / 100.0, (z_cm + float(P[:, 2].min())) / 100.0


def _seen(ort_wasser):
    out = []
    for w in ort_wasser or []:
        if w.get("typ") == "see" and w.get("umriss_cm") and isinstance(w.get("spiegel_cm"), (int, float)):
            out.append((np.asarray(w["umriss_cm"], np.float64)[:, :2] / 100.0, float(w["spiegel_cm"]) / 100.0, w.get("id")))
    return out


def _im_band(top, spiegel):
    return spiegel - UNTER_M < top < spiegel + UEBER_M


def korrigieren(ctx):
    """Fels-/Steinstuecke >= 0,8 m im Seeumriss mit Oberkante im Band (Spiegel - 1,5 m, Spiegel + 0,3 m):
    flaches Wasser -> heben, bis die Oberkante 0,35 m ueber dem Spiegel liegt (hoechstens 0,8 m, ruht dann auf dem
    Seegrund: z_frei), sonst entfernen; tiefes Wasser -> so weit absenken, dass die Oberkante 1,55 m unter dem Spiegel
    liegt, solange das Stueck nicht ganz im Grund verschwindet, sonst entfernen."""
    from . import steilwand as _sw
    seen = [(np.asarray(sv["umriss_m"], np.float64), float(sv["spiegel_m"]), sid) for sid, sv in ctx.see.items()
            if not sv.get("klein")]
    if not seen:
        return
    weg, gehoben, gesenkt = set(), 0, 0
    for e in ctx.ebene.stuecke:
        if e.get("ort") != ctx.id or e.get("rolle") not in FELS_ROLLEN:
            continue
        info = ctx.inv.netz(e["pfad"])
        if max(info["groesse_m"]) * max(e["s"]) < MIN_GROESSE_M:
            continue
        x, y = e["x"] / 100.0, e["y"] / 100.0
        for U, sp, sid in seen:
            if not _sw.in_polygon(np.array([x]), np.array([y]), U)[0]:
                continue
            top, unter = _oberkante(info, e["q"], e["s"], e["z"])
            if not _im_band(top, sp):
                break
            grund = float(ctx.boden(x, y))
            if sp - grund < UNTER_M + 0.1:
                dz = sp + UEBER_M + 0.05 - top
                if dz <= MAX_HEBEN_M:
                    e["z"] += dz * 100.0
                    e["z_frei"] = True
                    gehoben += 1
                else:
                    weg.add(id(e))
            else:
                dz = (sp - UNTER_M - 0.05) - top
                if top + dz > grund + 0.15:
                    e["z"] += dz * 100.0
                    gesenkt += 1
                else:
                    weg.add(id(e))
            if id(e) not in weg and e.get("akteur") and e.get("extra"):
                t2, u2 = _oberkante(info, e["q"], e["s"], e["z"])
                e["extra"]["unterkante_z"] = round(u2 * 100.0, 1)
            break
    if weg:
        ctx.ebene.stuecke = [e for e in ctx.ebene.stuecke if id(e) not in weg]
        for gn in list(ctx.gruppen):
            ctx.gruppen[gn] = [s_ for s_ in ctx.gruppen[gn] if id(s_.get("stueck")) not in weg]
    if weg or gehoben or gesenkt:
        ctx.melde("HINWEIS", "Bloecke im See (13h Nachtrag): %d gehoben (Oberkante >= Spiegel + 0,3 m), %d gesenkt "
                             "(<= Spiegel - 1,5 m), %d entfernt - nie knapp unter dem Spiegel" % (gehoben, gesenkt, len(weg)))


def pruefe_orte_see_bloecke(d, welt, sw_ordner, inv):
    """Pruefer: FEHLER, wenn Fels/Steine >= 0,8 m in einem geplanten See mit der Oberkante zwischen Spiegel - 1,5 m
    und Spiegel + 0,3 m liegen (Akteure und Instanzen; Ebenen wasser/pfad ausgenommen)."""
    from . import instanzen as _ins
    from . import steilwand as _sw
    if inv is None or not sw_ordner:
        return []
    seen = []
    for o in d.get("orte") or []:
        for U, sp, sid in _seen(o.get("wasser")):
            seen.append((o.get("id"), U, sp, sid))
    if not seen:
        return []
    funde = {}
    for feld, (plan, arr) in sorted(_ins.lies_ebene(sw_ordner).items()):
        stuecke = []
        for e in plan.get("akteure") or []:
            stuecke.append((e.get("pfad") or e["netz"], e["x"], e["y"], e["z"], (e["qx"], e["qy"], e["qz"], e["qw"]),
                            (e["sx"], e["sy"], e["sz"])))
        for key, dd in (plan.get("dateien") or {}).items():
            a = arr.get(key)
            if a is None or a.ndim != 2 or not len(a):
                continue
            if any(t in str(dd.get("gruppe", "")) for t in ("wasser", "pfad")):
                continue
            for r in a:
                stuecke.append((dd.get("pfad", key), float(r[0]), float(r[1]), float(r[2]),
                                (float(r[3]), float(r[4]), float(r[5]), float(r[6])), (float(r[7]), float(r[8]), float(r[9]))))
        for pfad, x, y, z, q, s in stuecke:
            if not _sw.ist_fels(pfad):
                continue
            try:
                info = inv.netz(pfad)
            except KeyError:
                continue
            if max(info["groesse_m"]) * max(s) < MIN_GROESSE_M:
                continue
            for oid, U, sp, sid in seen:
                if not _sw.in_polygon(np.array([x / 100.0]), np.array([y / 100.0]), U)[0]:
                    continue
                top, _ = _oberkante(info, q, s, z)
                if _im_band(top, sp):
                    f = funde.setdefault((oid, sid), [])
                    f.append((str(pfad).rsplit("/", 1)[-1], top - sp))
                break
    b = []
    for (oid, sid), f in sorted(funde.items()):
        n, t = f[0]
        b.append(("FEHLER", oid, "see %s: %d Fels-/Steinstuecke mit der Oberkante knapp unter dem Spiegel (z. B. %s %.2f m) - "
                                 "Moos scheint als Streifen durch (13h Nachtrag: >= +0,3 m oder <= -1,5 m)" % (sid, len(f), n, t)))
    return b
