"""Eingabepruefung, Auswahlkontext und abgeschlossene Exportpakete (ohne Unreal)."""
import hashlib
import json
import os
from pathlib import Path
import tempfile


MANIFEST = "paket.json"
PRUEFPROFIL = "pruefprofil.json"
QUELLGEOMETRIE = "quellgeometrie.json"
QUELLOPTIONEN = ("gefaelle", "sehens", "sw_ordner", "roh", "einbau")


class PaketFehler(ValueError):
    pass


def quellgeometrie(daten):
    """Inhalt der Geometrieplaene, unabhaengig von Ablagepfad und JSON-Einrueckung.

    Kein Vollabdruck der Binaerdaten oder des Unreal-Projekts.
    """
    return {"format": "fluss_sim_quellgeometrie_v1", "sha256": {
        name: hashlib.sha256(json.dumps(wert, ensure_ascii=True, sort_keys=True,
                                       separators=(",", ":"), allow_nan=False).encode()).hexdigest()
        for name, wert in sorted(daten.items())}}


def pruefe_quellgeometrie(aus, manifest, ist, uebergabe=False):
    if not manifest or QUELLGEOMETRIE not in manifest.get("dateien_sha256", {}):
        if uebergabe:
            raise PaketFehler("Paket ohne Quellgeometrie-Nachweis: fuer die Uebergabe neu exportieren")
        return
    soll = json.loads((Path(aus) / QUELLGEOMETRIE).read_text(encoding="utf-8"))
    if (not isinstance(soll, dict) or set(soll) != {"format", "sha256"} or
            soll.get("format") != "fluss_sim_quellgeometrie_v1" or
            not isinstance(soll.get("sha256"), dict) or not soll["sha256"] or
            any(not isinstance(v, str) or len(v) != 64 or any(c not in "0123456789abcdef" for c in v)
                for v in soll["sha256"].values())):
        raise PaketFehler("Ungueltiger Quellgeometrie-Nachweis")
    if ist is None:
        raise PaketFehler("Quellgeometrie kann ohne Weltdaten nicht geprueft werden")
    abweichend = sorted(k for k in set(soll["sha256"]) | set(ist["sha256"])
                       if soll["sha256"].get(k) != ist["sha256"].get(k))
    if abweichend:
        raise PaketFehler("Quellgeometrie geaendert (%d): %s. Eingabestand klaeren und neu exportieren." %
                          (len(abweichend), ", ".join(abweichend[:8])))


def pruefprofil(argumente, export=False):
    """Pfadunabhaengiger Pruefumfang; keine Behauptung identischer Projektinhalte."""
    daten = "daten1m" if getattr(argumente, "daten1m", None) else (
        "daten2m" if getattr(argumente, "daten2m", None) or export else None)
    return {"format": "fluss_sim_pruefprofil_v1", "daten": daten,
            "quelloptionen": sorted(k for k in QUELLOPTIONEN if getattr(argumente, k, None)),
            "gebaut": sorted(set(getattr(argumente, "gebaut", None) or [])),
            "ohne_erkennung": bool(getattr(argumente, "ohne_erkennung", False)),
            "regeln_sha256": hashlib.sha256(Path(argumente.regeln).read_bytes()).hexdigest()}


def pruefe_pruefprofil(aus, manifest, argumente):
    """Keine stillschweigend reduzierte Pruefung eines neuen Pakets zulassen."""
    if not manifest or PRUEFPROFIL not in manifest.get("dateien_sha256", {}):
        if getattr(argumente, "uebergabe", False):
            raise PaketFehler("Paket ohne Pruefprofil: fuer die Uebergabe mit aktuellem Exporter neu erzeugen")
        return
    soll = json.loads((Path(aus) / PRUEFPROFIL).read_text(encoding="utf-8"))
    ist = pruefprofil(argumente)
    if (not isinstance(soll, dict) or set(soll) != set(ist) or
            soll.get("format") != ist["format"] or soll.get("daten") not in ("daten1m", "daten2m") or
            not isinstance(soll.get("quelloptionen"), list) or
            any(k not in QUELLOPTIONEN for k in soll["quelloptionen"]) or
            not isinstance(soll.get("gebaut"), list) or not all(isinstance(k, str) for k in soll["gebaut"]) or
            type(soll.get("ohne_erkennung")) is not bool or
            not isinstance(soll.get("regeln_sha256"), str) or len(soll["regeln_sha256"]) != 64 or
            any(k not in "0123456789abcdef" for k in soll["regeln_sha256"])):
        raise PaketFehler("Ungueltiges Pruefprofil")
    if soll == ist:
        return
    abweichend = ", ".join(k for k in ist if soll[k] != ist[k])
    flags = ["--" + soll["daten"]] + ["--" + k.replace("_", "-") for k in soll["quelloptionen"]]
    if soll["gebaut"]:
        flags += ["--gebaut " + " ".join(soll["gebaut"])]
    if soll["ohne_erkennung"]:
        flags += ["--ohne-erkennung"]
    raise PaketFehler("Pruefprofil abweichend (%s). Erwartete Optionen: %s; Regeln-SHA256: %s. "
                      "Passende lokale Quellpfade angeben; bei absichtlich geaendertem Stand neu exportieren." %
                      (abweichend, " ".join(flags), soll["regeln_sha256"]))


def pruefe_ordner(argumente):
    for name in ("gefaelle", "sehens", "sw_ordner", "roh", "einbau", "daten1m", "daten2m"):
        wert = getattr(argumente, name, None)
        if wert and not Path(wert).is_dir():
            raise PaketFehler("--%s: Ordner fehlt: %s" % (name.replace("_", "-"), wert))
    if getattr(argumente, "daten1m", None) and getattr(argumente, "daten2m", None):
        raise PaketFehler("--daten1m und --daten2m nicht gleichzeitig verwenden")


def neues_ziel(aus):
    ziel = Path(os.path.abspath(aus))
    if os.path.lexists(ziel):
        raise PaketFehler("Ausgabeziel existiert bereits: %s. Einen neuen Paketordner angeben; Altstand bleibt erhalten." % ziel)
    return ziel


def schreibe_atomar(pfad, text):
    """Vorhandene Datei erst nach vollstaendigem Schreiben ersetzen."""
    ziel = Path(pfad)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=ziel.parent, prefix=".fluss_sim-", delete=False) as f:
            temp = f.name
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, ziel)
    finally:
        if temp and os.path.exists(temp):
            os.unlink(temp)


def _json(pfad, daten):
    schreibe_atomar(pfad, json.dumps(daten, ensure_ascii=True, sort_keys=True, indent=2, allow_nan=False) + "\n")


def _relativ(name):
    p = Path(name)
    if p.is_absolute() or p.drive or ".." in p.parts or not p.parts:
        raise PaketFehler("Ungueltiger Paketpfad: %s" % name)
    return p


def paket_id(manifest):
    """Inhaltsidentitaet ohne Ordnername oder wechselnden Pruefstatus; keine Signatur."""
    basis = {k: manifest.get(k) for k in ("format", "umfang", "dateien_sha256")}
    text = json.dumps(basis, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def paket_schreiben(aus, dateien, umfang, pruefen):
    """Nur neuen Ordner publizieren; Fehler lassen Ziel und bisherigen Stand unangetastet.

    dateien: relative Pfade -> fertig serialisierter Text. pruefen(stage) liefert Exit-Code.
    Der temporaere Ordner liegt unmittelbar unter dem expliziten Ziel-Elternordner.
    """
    ziel = neues_ziel(aus)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".fluss_sim-", dir=ziel.parent) as tmp:
        stage = Path(tmp).resolve()
        if stage.parent != ziel.parent.resolve():
            raise PaketFehler("Temporaerer Paketordner ausserhalb des Ziel-Elternordners")
        summen = {}
        for rel, text in sorted(dateien.items()):
            p = _relativ(rel)
            if p.as_posix() == MANIFEST:
                raise PaketFehler("paket.json ist fuer das Manifest reserviert")
            schreibe_atomar(stage / p, text)
            summen[p.as_posix()] = hashlib.sha256((stage / p).read_bytes()).hexdigest()
        manifest = {"format": "fluss_sim_paket_v2", "umfang": umfang, "dateien_sha256": summen,
                    "formal": "ausstehend", "unreal": "nicht_geprueft"}
        manifest["paket_id"] = paket_id(manifest)
        _json(stage / MANIFEST, manifest)
        if pruefen(str(stage)) != 0:
            raise PaketFehler("Formale Paketpruefung fehlgeschlagen; kein neuer Export veroeffentlicht")
        nachher = lies_manifest(stage)
        if nachher != manifest:
            raise PaketFehler("Paketmanifest waehrend der Pruefung veraendert; Export abgebrochen")
        manifest["formal"] = "bestanden"
        _json(stage / MANIFEST, manifest)
        neues_ziel(aus)
        # Kein Ersetzen/Mischen bestehender Pakete. Gleicher Datentraeger, ein Rename.
        os.rename(stage, ziel)
    return manifest["paket_id"]


def lies_manifest(aus, uebergabe=False):
    """Inventar und Bytes pruefen; alte Exporte ohne Manifest bleiben separat pruefbar."""
    root = Path(aus)
    if not (root / MANIFEST).exists():
        if uebergabe:
            raise PaketFehler("Uebergabe braucht ein abgeschlossenes Paket mit paket.json")
        return None
    m = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if not isinstance(m, dict) or m.get("format") not in ("fluss_sim_paket_v1", "fluss_sim_paket_v2"):
        raise PaketFehler("Unbekanntes Paketformat")
    if m["format"] == "fluss_sim_paket_v2" and m.get("paket_id") != paket_id(m):
        raise PaketFehler("Paket-ID passt nicht zu Umfang/Dateimanifest")
    if uebergabe and (m["format"] != "fluss_sim_paket_v2" or m.get("formal") != "bestanden" or
                      root.name.startswith(".fluss_sim-")):
        raise PaketFehler("Kein fertiges v2-Uebergabepaket; Altformat oder Zwischenstand neu exportieren")
    soll = m.get("dateien_sha256")
    if not isinstance(soll, dict) or not soll:
        raise PaketFehler("Leeres/ungueltiges Dateimanifest")
    ist = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p != root / MANIFEST}
    if ist != set(soll):
        raise PaketFehler("Paketdateien unvollstaendig oder fremde Dateien vorhanden")
    for rel, digest in soll.items():
        p = root / _relativ(rel)
        if p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            raise PaketFehler("Paketdatei veraendert: " + rel)
    return m


def auswahl_mit_kontext(gewaesser, eintraege, nur):
    """Hydraulische Verbindungen, gleiche Ortsdateien und ueberlappende SWR-Rahmen einschliessen.

    Gemeinsame Kollisionsobjekte (auch herausgefilterte) verbinden ebenfalls. Auswahl
    erfolgt erst nach Aufbau aller Gewaesser; die Prioritaetsberechnung sieht ganze Ketten.
    """
    ids = {g["id"] for g in gewaesser}
    if len(ids) != len(gewaesser) or [g["id"] for g in gewaesser] != [e["id"] for e in eintraege]:
        raise PaketFehler("Gewaesser-IDs doppelt oder Eintraege unvollstaendig")
    ziel = set()
    for token in nur or []:
        treffer = {g["id"] for g in gewaesser if token == g["id"] or
                   token in {l["id"] for l in g.get("laeufe", [])} or
                   token == (g.get("quelle_sehens") or {}).get("ort")}
        if not treffer:
            raise PaketFehler("Unbekannte --nur-ID: " + token)
        ziel |= treffer
    if not nur:
        ziel = set(ids)

    def fertig(enthalten):
        teil = enthalten != ids
        namespace = "TEST_" + hashlib.sha256("\n".join(sorted(enthalten)).encode()).hexdigest()[:12] + "_" if teil else ""
        umfang = {"art": "teil" if teil else "voll", "ziele": sorted(ziel), "kontext": sorted(enthalten - ziel),
                  "gewaesser": sorted(enthalten), "zonen_namespace": namespace,
                  "laeufe": sorted({l["id"] for e in eintraege if e["id"] in enthalten for l in e.get("laeufe", [])})}
        return enthalten, umfang

    if ziel == ids:
        # Vollauswahl enthaelt bereits jeden Kontext; keine paarweisen Rechteckvergleiche.
        return fertig(set(ids))
    nachbarn = {gid: set() for gid in ids}

    def verbinden(a, b):
        if b in ids and b != a:
            nachbarn[a].add(b)
            nachbarn[b].add(a)

    datei, objekte = {}, {}
    for g, e in zip(gewaesser, eintraege):
        if g["id"] != e["id"]:
            raise PaketFehler("Reihenfolge der Gewaessereintraege stimmt nicht")
        gid = g["id"]
        rel = g["rel"]
        if rel in datei:
            verbinden(gid, datei[rel])
        datei[rel] = gid
        for ende in (e.get("anfang") or {}, e.get("muendung") or {}):
            for feld in ("ziel", "gewaesser"):
                verbinden(gid, ende.get(feld))
        for o in (e.get("wasser_kollision") or []) + (e.get("ohne_wasser_kollision") or []):
            key = json.dumps(o["ref"], sort_keys=True)
            if key in objekte:
                verbinden(gid, objekte[key])
            objekte[key] = gid
    for i, e in enumerate(eintraege):
        for f in eintraege[i + 1:]:
            if any(a[0] <= b[2] and a[2] >= b[0] and a[1] <= b[3] and a[3] >= b[1]
                   for a in (k["bereich_cm"] for k in e.get("swr_bereiche", []) if "bereich_cm" in k)
                   for b in (k["bereich_cm"] for k in f.get("swr_bereiche", []) if "bereich_cm" in k)):
                verbinden(e["id"], f["id"])
    enthalten = set(ziel)
    offen = list(ziel)
    while offen:
        for gid in nachbarn[offen.pop()] - enthalten:
            enthalten.add(gid)
            offen.append(gid)
    return fertig(enthalten)


def pruefe_umfang(manifest, alle):
    if manifest is None:
        return None
    u = manifest.get("umfang") or {}
    if not isinstance(u, dict):
        raise PaketFehler("Ungueltiger Paketumfang")
    for feld in ("gewaesser", "ziele", "kontext", "laeufe"):
        werte = u.get(feld)
        if (not isinstance(werte, list) or
                any(not isinstance(w, str) or not w.strip() for w in werte) or
                len(set(werte)) != len(werte)):
            raise PaketFehler("Ungueltiger Paketumfang: %s muss eine Liste eindeutiger, nicht leerer IDs sein" % feld)
    ids = set(alle)
    if (u.get("art") not in ("voll", "teil") or set(u.get("gewaesser", [])) != ids or
            set(u.get("ziele", [])) | set(u.get("kontext", [])) != ids or not u.get("ziele") or
            set(u.get("ziele", [])) & set(u.get("kontext", [])) or
            set(u.get("laeufe", [])) != {l["id"] for g in alle.values() for l in g.get("laeufe", [])}):
        raise PaketFehler("Paketumfang stimmt nicht mit den Gewaessern ueberein")
    erwartet = "TEST_" + hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()[:12] + "_" if u["art"] == "teil" else ""
    if u.get("zonen_namespace") != erwartet:
        raise PaketFehler("Ungueltiger Namensbereich der Testzonen")
    return u
