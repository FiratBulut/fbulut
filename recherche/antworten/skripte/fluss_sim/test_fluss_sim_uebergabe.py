"""Regressionen der Exportsperre; keine Unreal-Simulation oder Projektabnahme.

Aufruf: python -m unittest discover -s recherche/antworten/skripte/fluss_sim -p "test_*.py" -v
"""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock

import fluss_sim_export as fx
import fluss_sim_pruefen as fp


def plan(anzahl=1):
    # Absichtlich ohne neue Metadaten: auch alte Dateien muessen gesperrt werden.
    return {"id": "TEST_BACH", "swr_bereiche": [
        {"geteilt": anzahl > 1, "swr": {"begrenzung": {
            "art": "rechteck_teil" if anzahl > 1 else "rechteck_um_fluss"}}}
        for _ in range(anzahl)]}


class UebergabeTests(unittest.TestCase):
    def assertGesperrt(self, g):
        self.assertTrue(fx.export_sperrgruende([g]))
        befunde = []
        # Direkter Aufruf muss ebenfalls ohne Geometrie-Neuberechnung ablehnen.
        fp.pruefe_swr(g, None, None, {}, befunde)
        self.assertTrue(any(st == fp.FEHLER for st, _, _ in befunde))

    def test_alter_teilungsplan(self):
        self.assertGesperrt(plan(2))

    def test_teilungskennzeichen_entfernen_umgeht_sperre_nicht(self):
        g = plan(2)
        for e in g["swr_bereiche"]:
            e.pop("geteilt")
            e["swr"].pop("begrenzung")
        self.assertGesperrt(g)

    def test_einzelnes_rest_teilstueck(self):
        g = plan(2)
        g["swr_bereiche"].pop()
        self.assertGesperrt(g)

    def test_teilrechteck_ohne_geteilt_flag(self):
        g = plan()
        g["swr_bereiche"][0]["swr"]["begrenzung"]["art"] = "rechteck_teil"
        self.assertGesperrt(g)

    def test_fehlende_bereiche(self):
        self.assertGesperrt({"id": "LEER"})

    def test_ungeteilte_struktur_bleibt_zulaessig_und_unveraendert(self):
        g = plan()
        vorher = copy.deepcopy(g)
        self.assertEqual(fx.export_sperrgruende([g]), [])
        befunde = []
        self.assertTrue(fp.pruefe_swr_ausfuehrbarkeit(g, befunde))
        self.assertEqual(befunde, [])
        self.assertEqual(g, vorher)

    def test_leere_exportauswahl(self):
        self.assertTrue(fx.export_sperrgruende([]))

    def test_pruefer_einstieg_lehnt_alte_datei_ab(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp, "fluss_sim.json")
            p.write_text(json.dumps({"format": fx.FORMAT_VERSION, "gewaesser": [plan(2)]}), encoding="utf-8")
            vorher = p.read_bytes()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = fp.main([tmp])
            self.assertEqual(code, 1)
            self.assertIn("TEST_BACH", out.getvalue())
            self.assertIn("nach Vorpruefung abgebrochen", out.getvalue())
            self.assertIn("UNREAL-NACHWEIS: NICHT GEPRUEFT", out.getvalue())
            self.assertEqual(p.read_bytes(), vorher)

    def test_pruefer_leerer_ordner_ist_keine_erfolgreiche_pruefung(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(fp.main([tmp]), 1)

    def test_formaler_erfolg_ist_keine_unreal_abnahme(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = fp.abschluss({fp.FEHLER: 0, fp.WARNUNG: 0, fp.HINWEIS: 0})
        self.assertEqual(code, 0)
        self.assertIn("FORMALE PLANPRUEFUNG: BESTANDEN", out.getvalue())
        self.assertIn("UNREAL-NACHWEIS: NICHT GEPRUEFT", out.getvalue())

    def test_gemischter_export_schreibt_nichts_und_erhaelt_altdaten(self):
        # Nur Welt-/Planerzugriff ersetzen. Echter main-Pfad, echte Sperre und echter
        # Dateischreiber bleiben aktiv. Der zweite Eintrag sperrt den ganzen Lauf.
        from sehens_lib import daten
        gewaesser = [dict(plan(), rel="kurz/fluss_sim.json"),
                     dict(plan(2), id="LANGER_BACH", rel="lang/fluss_sim.json")]
        info = dict(toepfe=[], sehens_seen=[], teile_welt=0, teile_plan=0,
                    teile_roh=0, sehens_baeche=0, fortsetzungen=[])
        ginfo = dict(addiert=0, ohne=0, gebaut=[], lauf_json_ungebaut=[])
        with tempfile.TemporaryDirectory() as tmp, contextlib.ExitStack() as stack:
            alt = Path(tmp, "fluss_sim.json")
            alt.write_bytes(b"alter Stand unveraendert")
            stack.enter_context(patch.object(daten, "lade", return_value=Mock(wasser_welt={}, baeche=[])))
            stack.enter_context(patch.object(fx, "Masse"))
            stack.enter_context(patch.object(fx, "Pool"))
            stack.enter_context(patch.object(fx, "Gelaende", return_value=Mock(deltas=[])))
            stack.enter_context(patch.object(fx, "gelaende_laden", return_value=ginfo))
            stack.enter_context(patch.object(fx, "gewaesser_bilden", return_value=(gewaesser, [], None, info)))
            stack.enter_context(patch.object(fx, "baue_gewaesser_v3", side_effect=lambda g, *_: g))
            schreiben = stack.enter_context(patch.object(fx, "schreibe_json", wraps=fx.schreibe_json))
            out = stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            self.assertEqual(fx.main(["--aus", str(Path(tmp, "neu")), "--ohne-erkennung"]), 1)
            schreiben.assert_not_called()
            self.assertEqual(alt.read_bytes(), b"alter Stand unveraendert")
            self.assertEqual(list(Path(tmp).iterdir()), [alt])
            self.assertIn("LANGER_BACH", out.getvalue())
            self.assertIn("Bestehende Ausgaben wurden nicht aktualisiert", out.getvalue())


if __name__ == "__main__":
    unittest.main()
