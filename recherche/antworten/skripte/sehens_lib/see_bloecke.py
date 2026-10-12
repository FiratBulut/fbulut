"""see_bloecke.py - Auftrag 13h, Nachtrag 12.10. 01:00 (Ferat): Bloecke in geplanten Seen nie knapp unter dem Spiegel.

Befund (Karsee, Punkt 3): Zwei Felsbloecke lagen knapp unter dem Seespiegel; ihr helles Moos schien durch das Wasser
und wurde von den Wellen in grelle Streifen gebrochen. Regel fuer alle Planer (Koordinator): Stuecke >= 0,5 m in einem
geplanten See/Becken (Fels, Steine, Holz, Wurzeln, Moos - keine Pflanzen, die durch den Spiegel wachsen) ragen entweder
heraus (Oberkante >= Spiegel + 0,3 m) oder liegen ganz tiefer als 1,5 m unter dem Spiegel (Oberkante <= Spiegel - 1,5 m).
Zugefrorene Seen ("eis") sind ausgenommen. Ausnahme: Gruppen mit "teilweise_ueberflutet": true (z. B. Uferbloecke, die durch den Spiegel stossen) - sie stehen in
orte.json je Ort unter "teilweise_ueberflutet" (Gruppennamen), der Pruefer laesst sie aus.

  korrigieren(ctx)                                  Planer (rezept.baue, nach den Gruppen): Stuecke heben/senken/entfernen
  pruefe_orte_see_bloecke(d, welt, sw_ordner, inv)  Pruefer: FEHLER je Ort mit Anzahl und Beispiel
"""

import numpy as np

UEBER_M = 0.3
UNTER_M = 1.5
MIN_GROESSE_M = 0.5
MAX_HEBEN_M = 0.8
KEINE_ROLLEN = ("pflanze", "baum")
import re as _re
PFLANZE = _re.compile(r"(fern|grass|reed|rush|plant|bush|shrub|lily|lotus|sedge|cattail|rohrkolben|binse|seerose|"
                      r"petasites|horsetail|kelp|algae|weed|flower|tree|pine|fir_|willow)", _re.I)


def _oberkante(info, q, s, z_cm):
    from . import instanzen as _ins
    P = _ins.gedrehte_box(info, q, s)
    return (z_cm + float(P[:, 2].max())) / 100.0, (z_cm + float(P[:, 2].min())) / 100.0


def _seen(ort_wasser):
    out = []
    for w in ort_wasser or []:
        if w.get("eis"):
            continue                       # zugefroren: Stuecke liegen auf dem Eis
        if w.get("typ") == "see" and w.get("umriss_cm") and isinstance(w.get("spiegel_cm"), (int, float)):
            out.append((np.asarray(w["umriss_cm"], np.float64)[:, :2] / 100.0, float(w["spiegel_cm"]) / 100.0, w.get("id")))
    return out


def _im_band(top, spiegel):
    return spiegel - UNTER_M < top < spiegel + UEBER_M


def meer_reste(ctx):
    """Kleinzeug/Kontakt mit Bodenkontakt, das im 1-m-Raster des Pruefers knapp im Meer laege (Boden < -0,3 m an
    steilen Plattformkanten): Boden an vier Punkten +-0,6 m pruefen, bei < -0,25 m entfernen."""
    from . import stempel as _stm
    from . import sehens_pruefen as _sp
    st = ctx.stempel
    if st is None or not st.delta.size or float(np.abs(st.delta).max()) < 0.01:
        return
    # Boden genau wie der Pruefer: Welt bilinear + 1-m-Delta (nach_1m) bilinear
    bp = _sp.BodenNachStempel.__new__(_sp.BodenNachStempel)
    bp.welt = ctx.welt
    bp.deltas = [(list(st.fe.fenster_ij_1m()), _stm.nach_1m(st.delta, st.z))]
    weg = set()
    for e in ctx.ebene.stuecke:
        if e.get("ort") != ctx.id or e.get("z_frei") or e.get("ebene") not in ("kleinzeug", "kontakt", "bewuchs", "schutt"):
            continue
        x, y = e["x"] / 100.0, e["y"] / 100.0
        if float(ctx.boden(x, y)) > 1.5:
            continue
        if float(bp.hoehe(x, y)) < -0.25:
            weg.add(id(e))
    if weg:
        ctx.ebene.stuecke = [e for e in ctx.ebene.stuecke if id(e) not in weg]
        for gn in list(ctx.gruppen):
            ctx.gruppen[gn] = [s_ for s_ in ctx.gruppen[gn] if id(s_.get("stueck")) not in weg]
        ctx.melde("HINWEIS", "%d Kleinstuecke an der Meereskante entfernt (Boden im 1-m-Raster < -0,3 m, 13h)" % len(weg))


def korrigieren(ctx):
    """Fels-/Steinstuecke >= 0,8 m im Seeumriss mit Oberkante im Band (Spiegel - 1,5 m, Spiegel + 0,3 m):
    flaches Wasser -> heben, bis die Oberkante 0,35 m ueber dem Spiegel liegt (hoechstens 0,8 m, ruht dann auf dem
    Seegrund: z_frei), sonst entfernen; tiefes Wasser -> so weit absenken, dass die Oberkante 1,55 m unter dem Spiegel
    liegt, solange das Stueck nicht ganz im Grund verschwindet, sonst entfernen."""
    from . import steilwand as _sw
    meer_reste(ctx)
    # zugefrorene Seen ("eis"): dort liegt alles AUF dem Eis - die Regel gilt nur fuer offenes Wasser
    eis = {w.get("id") for w in ctx.r.get("wasser") or [] if w.get("typ") == "see" and w.get("eis")}
    seen = [(np.asarray(sv["umriss_m"], np.float64), float(sv["spiegel_m"]), sid) for sid, sv in ctx.see.items()
            if not sv.get("klein") and sid not in eis]
    if not seen:
        return
    weg, gehoben, gesenkt = set(), 0, 0
    frei = sorted({g["name"] for g in ctx.r.get("gruppen") or [] if g.get("teilweise_ueberflutet")})
    ctx.teilweise_ueberflutet = frei
    for e in ctx.ebene.stuecke:
        if e.get("ort") != ctx.id or e.get("rolle") in KEINE_ROLLEN or e.get("gruppe") in frei:
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
    frei = set()
    for o in d.get("orte") or []:
        for U, sp, sid in _seen(o.get("wasser")):
            seen.append((o.get("id"), U, sp, sid))
        for gn in o.get("teilweise_ueberflutet") or []:
            frei.add("%s_%s" % (o.get("id"), gn))
    if not seen:
        return []
    funde = {}
    for feld, (plan, arr) in sorted(_ins.lies_ebene(sw_ordner).items()):
        stuecke = []
        for e in plan.get("akteure") or []:
            if e.get("klasse") in frei:
                continue
            stuecke.append((e.get("pfad") or e["netz"], e["x"], e["y"], e["z"], (e["qx"], e["qy"], e["qz"], e["qw"]),
                            (e["sx"], e["sy"], e["sz"])))
        for key, dd in (plan.get("dateien") or {}).items():
            a = arr.get(key)
            if a is None or a.ndim != 2 or not len(a):
                continue
            if any(t in str(dd.get("gruppe", "")) for t in ("wasser", "pfad")):
                continue
            orte_d = list((dd.get("orte") or {}).keys())
            if dd.get("rolle") and any("%s_%s" % (o_, dd["rolle"]) in frei for o_ in orte_d):
                continue
            for r in a:
                stuecke.append((dd.get("pfad", key), float(r[0]), float(r[1]), float(r[2]),
                                (float(r[3]), float(r[4]), float(r[5]), float(r[6])), (float(r[7]), float(r[8]), float(r[9]))))
        for pfad, x, y, z, q, s in stuecke:
            if PFLANZE.search(str(pfad).rsplit("/", 1)[-1]):
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
        b.append(("FEHLER", oid, "see %s: %d Stuecke mit der Oberkante knapp unter dem Spiegel (z. B. %s %.2f m) - "
                                 "Moos scheint als Streifen durch (13h Nachtrag: >= +0,3 m oder <= -1,5 m, sonst teilweise_ueberflutet)" % (sid, len(f), n, t)))
    return b
