"""sehens_lib - gemeinsame Bibliothek fuer Auftrag 13 (Sehenswuerdigkeiten, 8 je Biom).

Eigene Implementierung nach vorlagen/FORMAT.md, vorlagen/SEHENS_FORMAT.md und
vorlagen/daten/sehens/legende.json. Nur NumPy + Pillow (SciPy optional, wird genutzt falls
vorhanden). Deterministisch, ASCII-Logs.

Module:
  daten       Laden 2 m (PNG) / 1 m (f32/r8), Legende, Koordinaten Pixel <-> Welt, Fenster
  gelaende    Hang, Exposition, Kruemmung, TPI, Abfluss (D8, Senken fuellen), Stufen,
              Landformen, Distanzen (Weg/Ort/Wasser/Meer/Stadt), Cache (.npy)
  sicht       Sichtlinien Weg -> Ort (Gelaende + Baumhoehe), beste Blickposition, Verdeckung
  kandidaten  Kandidatensuche je Biom, Merkmale, Abstandsauswahl, Erreichbarkeit (Dijkstra)
  zeichnen    Draufsicht-PNG je Ort
  format      Schreiber standorte.json (Phase 1) und orte.json (Phase 2), Kameras
  sehens_pruefen  Pruefer gegen SEHENS_FORMAT (+ globale Abstaende ueber alle Biome; Phase 2: orte.json + sw_<biom>)
  Phase 2 (Auftrag 13, PLANER_ANLEITUNG.md):
  inventar    Asset-Inventar (netze.csv, Bounds, Sperre, Niagara/Decals/Klaenge, Material-Parameter), Asset-Pruefung
  stempel     Gelaendestempel (Mulde, Kuppe, Rinne, Terrasse, Abbruch, Seebecken) + Bodenlagen, 1-m-Dateien
  instanzen   Quaternionen, Platzierung (Eingraben, Hangnormale), Streuung/Cluster/Kontaktzonen, Ebene sw_<biom>
  rezept      Ort aus Regel-Block bauen (Anker, Gelaende, Wasser, Gruppen, Lagen, Pfad, Effekte, Budget) + schreiben
  vorschau    Testbild test_<id>.png

Einbinden (auch mit python -I, das den Skriptordner NICHT in sys.path setzt):
    import sys, os
    sys.path.insert(0, "<repo>/antworten/skripte")
    from sehens_lib import daten, gelaende, sicht, kandidaten, zeichnen
    from sehens_lib import format as sfmt
"""

import sys as _sys
import time as _time

__version__ = "1.0"   # Cache-Fingerabdruck (gelaende.py) - nur bei geaenderter Gelaende-Rechnung erhoehen

_UML = {"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss",
        "–": "-", "—": "-", "→": "->", "≤": "<=", "≥": ">=", "×": "x", "°": " Grad",
        "„": '"', "“": '"', "”": '"', "’": "'", "…": "..."}


def ascii_text(s):
    """Wandelt Text in reines ASCII (Umlaute ausgeschrieben)."""
    s = str(s)
    for k, v in _UML.items():
        s = s.replace(k, v)
    return s.encode("ascii", "replace").decode("ascii")


_STILL = False


def still(an=True):
    """Logs abschalten (z. B. in Schleifen)."""
    global _STILL
    _STILL = bool(an)


def log(*teile):
    """ASCII-Log nach stdout."""
    if _STILL:
        return
    msg = " ".join(ascii_text(t) for t in teile)
    _sys.stdout.write("[sehens_lib] " + msg + "\n")
    _sys.stdout.flush()


class Uhr:
    """Kleine Stoppuhr: with Uhr("Schritt"): ...  -> loggt Laufzeit."""

    def __init__(self, name, ausgabe=True):
        self.name = name
        self.ausgabe = ausgabe
        self.sek = 0.0

    def __enter__(self):
        self._t0 = _time.perf_counter()
        return self

    def __exit__(self, *a):
        self.sek = _time.perf_counter() - self._t0
        if self.ausgabe:
            log("%-40s %7.2f s" % (self.name, self.sek))
        return False
