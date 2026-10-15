"""Eingabepruefung, Auswahlkontext und abgeschlossene Exportpakete (ohne Unreal)."""
import hashlib
import json
import os
from pathlib import Path
import tempfile


MANIFEST = "paket.json"


class PaketFehler(ValueError):
    pass


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
        manifest = {"format": "fluss_sim_paket_v1", "umfang": umfang, "dateien_sha256": summen,
                    "formal": "ausstehend", "unreal": "nicht_geprueft"}
        _json(stage / MANIFEST, manifest)
        if pruefen(str(stage)) != 0:
            raise PaketFehler("Formale Paketpruefung fehlgeschlagen; kein neuer Export veroeffentlicht")
        manifest["formal"] = "bestanden"
        _json(stage / MANIFEST, manifest)
        neues_ziel(aus)
        # Kein Ersetzen/Mischen bestehender Pakete. Gleicher Datentraeger, ein Rename.
        os.rename(stage, ziel)


def lies_manifest(aus):
    """Inventar und Bytes pruefen; alte Exporte ohne Manifest bleiben separat pruefbar."""
    root = Path(aus)
    if not (root / MANIFEST).exists():
        return None
    m = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if m.get("format") != "fluss_sim_paket_v1":
        raise PaketFehler("Unbekanntes Paketformat")
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
    if len(ids) != len(gewaesser) or ids != {e["id"] for e in eintraege}:
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
    teil = bool(nur) and enthalten != ids
    # Testzonen einer Teilauswahl duerfen keine globalen WZ_Fxx ueberschreiben.
    namespace = "TEST_" + hashlib.sha256("\n".join(sorted(enthalten)).encode()).hexdigest()[:12] + "_" if teil else ""
    umfang = {"art": "teil" if teil else "voll", "ziele": sorted(ziel), "kontext": sorted(enthalten - ziel),
              "gewaesser": sorted(enthalten), "zonen_namespace": namespace,
              "laeufe": sorted({l["id"] for e in eintraege if e["id"] in enthalten for l in e.get("laeufe", [])})}
    return enthalten, umfang


def pruefe_umfang(manifest, alle):
    if manifest is None:
        return None
    u = manifest.get("umfang") or {}
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
