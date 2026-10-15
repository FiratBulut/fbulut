"""Paketfehler mit echten temporaeren Dateien; keine Unreal-Abnahme."""
import ast
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import fluss_sim_export as fx
import fluss_sim_pruefen as fp
import fluss_sim_paket as pk


def gewaesser(gid, ziel=None, box=None):
    return {"id": gid, "rel": gid + "/fluss_sim.json", "laeufe": [{"id": gid + "_lauf"}],
            "muendung": {"art": "bach", "ziel": ziel} if ziel else {"art": "meer"},
            "swr_bereiche": [{"bereich_cm": box or [0, 0, 100, 100]}]}


class PaketTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.regeln = fx.lese_json(fx.REGELN_STANDARD)

    def pool_laden(self, daten=None, anzahl=1):
        p = self.root / "plan.json"
        p.write_text(json.dumps({"dateien": {"SM_Rock": {"anzahl": anzahl, "pfad": "/Game/SM_Rock"}}}), encoding="utf-8")
        if daten is not None:
            (self.root / "SM_Rock.f32").write_bytes(daten)
        pool = fx.Pool(self.regeln, fx.Masse())
        pool.lade_ebene(str(p), "test/plan.json")
        return pool

    def test_fehlende_instanzdatei_stoppt(self):
        with self.assertRaisesRegex(pk.PaketFehler, "fehlt"):
            self.pool_laden()

    def test_abgeschnittene_instanzdatei_stoppt(self):
        for groesse in (1, 39, 41, 44):
            with self.subTest(bytes=groesse), self.assertRaisesRegex(pk.PaketFehler, "abgeschnitten"):
                self.pool_laden(bytes(groesse))

    def test_falsche_instanzanzahl_stoppt(self):
        with self.assertRaisesRegex(pk.PaketFehler, "Instanzanzahl"):
            self.pool_laden(bytes(40), anzahl=2)

    def test_nan_stoppt(self):
        with self.assertRaisesRegex(pk.PaketFehler, "Ungueltige Instanzdaten"):
            self.pool_laden(np.full(10, np.nan, dtype="<f4").tobytes())

    def test_gueltige_instanz_bleibt_erhalten(self):
        pool = self.pool_laden(np.array([1,2,3,0,0,0,1,1,1,1], dtype="<f4").tobytes())
        self.assertEqual(len(pool.recs), 1)
        self.assertEqual(list(pool.recs[0]["v"][:3]), [1,2,3])

    def test_fehlendes_delta_stoppt(self):
        with self.assertRaisesRegex(pk.PaketFehler, "Delta fehlt"):
            fx.Gelaende(None).delta_hinzu(str(self.root), [{"gelaende": {"datei": "delta.f32", "fenster_ij": [0,0,2,2]}}])

    def test_unlesbarer_laufplan_stoppt(self):
        d = self.root / "LAUF"
        d.mkdir()
        (d / "plan.json").write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(pk.PaketFehler, "nicht lesbar"):
            fx.lauf_plaene(str(self.root))

    def test_expliziter_falscher_eingabeordner_stoppt_beide_einstiege(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(fx.main(["--aus", str(self.root / "neu"), "--gefaelle", str(self.root / "fehlt")]), 1)
            self.assertEqual(fp.main([str(self.root), "--gefaelle", str(self.root / "fehlt")]), 1)
        self.assertFalse((self.root / "neu").exists())

    def test_serialisierungsfehler_erhaelt_altdatei(self):
        p = self.root / "alt.json"
        p.write_bytes(b"alter Stand")
        with self.assertRaises(TypeError):
            fx.schreibe_json(str(p), {"kaputt": object()})
        self.assertEqual(p.read_bytes(), b"alter Stand")

    def test_schreibfehler_erhaelt_altdatei(self):
        p = self.root / "alt.json"
        p.write_bytes(b"alter Stand")
        with patch.object(pk.os, "replace", side_effect=OSError("Datentraegerfehler")), self.assertRaises(OSError):
            fx.schreibe_json(str(p), {"neu": 1})
        self.assertEqual(p.read_bytes(), b"alter Stand")
        self.assertEqual(list(self.root.iterdir()), [p])

    def umfang(self):
        g = gewaesser("A")
        return pk.auswahl_mit_kontext([g], [g], None)[1]

    def test_paket_erst_nach_pruefung_sichtbar(self):
        ziel = self.root / "neu"
        def pruefen(stage):
            self.assertFalse(ziel.exists())
            self.assertEqual((Path(stage) / "daten.json").read_text(), '{"wert": 1}\n')
            self.assertEqual(pk.lies_manifest(stage)["formal"], "ausstehend")
            return 0
        pk.paket_schreiben(str(ziel), {"daten.json": '{"wert": 1}\n'}, self.umfang(), pruefen)
        self.assertEqual(pk.lies_manifest(ziel)["formal"], "bestanden")
        self.assertEqual(list(self.root.iterdir()), [ziel])

    def test_fehlgeschlagene_pruefung_publiziert_nichts(self):
        ziel = self.root / "neu"
        alt = self.root / "alt"
        alt.mkdir()
        (alt / "daten").write_bytes(b"behalten")
        with self.assertRaisesRegex(pk.PaketFehler, "Paketpruefung"):
            pk.paket_schreiben(str(ziel), {"a.json": "{}"}, self.umfang(), lambda _: 1)
        self.assertEqual(list(self.root.iterdir()), [alt])
        self.assertEqual((alt / "daten").read_bytes(), b"behalten")

    def test_abbruch_nach_erster_datei_publiziert_nichts(self):
        echt = pk.schreibe_atomar
        def schreiben(p, text):
            if Path(p).name == "b.json":
                raise OSError("simulierter Schreibabbruch")
            echt(p, text)
        with patch.object(pk, "schreibe_atomar", side_effect=schreiben), self.assertRaises(OSError):
            pk.paket_schreiben(str(self.root / "neu"), {"a.json": "{}", "b.json": "{}"}, self.umfang(), lambda _: 0)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_bestehendes_ziel_nicht_ueberschreiben(self):
        with self.assertRaisesRegex(pk.PaketFehler, "existiert bereits"):
            pk.paket_schreiben(str(self.root), {"a.json": "{}"}, self.umfang(), lambda _: 0)

    def test_manifest_erkennt_aenderung_und_zusaetzliche_datei(self):
        ziel = self.root / "neu"
        pk.paket_schreiben(str(ziel), {"a.json": "{}"}, self.umfang(), lambda _: 0)
        (ziel / "a.json").write_text('{"manuell":1}')
        with self.assertRaisesRegex(pk.PaketFehler, "veraendert"):
            pk.lies_manifest(ziel)
        (ziel / "fremd.json").write_text("{}")
        with self.assertRaisesRegex(pk.PaketFehler, "fremde Dateien"):
            pk.lies_manifest(ziel)

    def test_verbindungen_und_nachbarn_werden_transitiv_aufgenommen(self):
        a = gewaesser("A", "B")
        b = gewaesser("B", box=[1000,0,1100,100])
        c = gewaesser("C", box=[1090,0,1200,100])
        d = gewaesser("D", box=[5000,0,5100,100])
        gs = [a,b,c,d]
        vorher = copy.deepcopy(gs)
        ids, umfang = pk.auswahl_mit_kontext(gs, gs, ["A_lauf"])
        self.assertEqual(ids, {"A","B","C"})
        self.assertEqual(umfang["kontext"], ["B","C"])
        self.assertEqual(umfang["art"], "teil")
        self.assertTrue(umfang["zonen_namespace"].startswith("TEST_"))
        self.assertEqual(gs, vorher)
        # Tatsaechliche Prioritaetsfunktion des Exporters, voller und Teilkontext.
        tree = ast.parse(Path(fx.__file__).read_text(encoding="utf-8"))
        main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_main")
        stufe = next(n for n in main.body if isinstance(n, ast.FunctionDef) and n.name == "stufe")
        ns = {"nach_id": {g["id"]:g for g in gs}}
        exec(compile(ast.Module(body=[stufe], type_ignores=[]), "<stufe>", "exec"), ns)
        erwartet = ns["stufe"](a)
        ns["nach_id"] = {g["id"]:g for g in gs if g["id"] in ids}
        self.assertEqual(ns["stufe"](a), erwartet)
        self.assertEqual(erwartet, 1)

    def test_unbekannte_id_neben_gueltiger_stoppt(self):
        a = gewaesser("A")
        with self.assertRaisesRegex(pk.PaketFehler, "TIPPFEHLER"):
            pk.auswahl_mit_kontext([a], [a], ["A", "TIPPFEHLER"])

    def test_gemeinsame_objekte_auch_ohne_kollision_verbinden(self):
        a, b = gewaesser("A"), gewaesser("B", box=[5000,0,5100,100])
        a["wasser_kollision"] = [{"ref":{"index":0}}]
        b["ohne_wasser_kollision"] = [{"ref":{"index":0}}]
        ids, _ = pk.auswahl_mit_kontext([a,b], [a,b], ["A"])
        self.assertEqual(ids, {"A","B"})

    def test_gemeinsame_ortsdatei_bleibt_vollstaendig(self):
        a, b = gewaesser("A"), gewaesser("B", box=[5000,0,5100,100])
        b["rel"] = a["rel"]
        ids, _ = pk.auswahl_mit_kontext([a,b], [a,b], ["A"])
        self.assertEqual(ids, {"A","B"})

    def test_umfang_passt_nicht_stoppt(self):
        with self.assertRaisesRegex(pk.PaketFehler, "Paketumfang"):
            pk.pruefe_umfang({"umfang": self.umfang()}, {"B": gewaesser("B")})

    def test_export_und_pruefer_voll_und_teil_mit_echter_geometrie(self):
        # Nur Quelldatenzugriff und Terrain ersetzen. Geometrie, Export, Paket,
        # Manifest und komplette formale Pruefung laufen wirklich.
        from sehens_lib import daten
        def quelle(gid, x, y=0, z=1000):
            linie = fx.Linie([0,100], [x,x+10000], [y,y+1000], [z,z-100],
                             [300,300], [100,100], [100,100], [False,False])
            return dict(id=gid, rel=gid+"/fluss_sim.json", kategorie="welt", art="bach", linie=linie,
                        abst=[], extra=dict(effekte=[], strahl={}, vorhang=set(), kaskadennetze=[], ufer_rand=None),
                        laeufe=[dict(id=gid+"_lauf", s_m=[0,100], s_quelle_m=[0,100], herkunft="roh", quelle={})],
                        anfang={"art":"quelle"}, muendung={"art":"meer", "punkt_cm":[x+10000,y+1000,z-100]},
                        roh_bei=lambda _: True, typ_bei=lambda _: "bach")
        welt = SimpleNamespace(wasser_welt={"fluesse":[{"id":k+"_lauf"} for k in "ABC"]}, baeche=[])
        class Terrain:
            def __init__(self, _):
                self.deltas = []
            def raster(self, _):
                return 0., 0., 200., np.zeros((2,2))
        def bilden(*args, **kwargs):
            a, b, c = quelle("A", 0), quelle("B", 10000, 1000, 900), quelle("C", 200000)
            a["muendung"].update(art="bach", ziel="B", ziel_s_m=0)
            return ([a,b,c], [], SimpleNamespace(seen=[]),
                    dict(toepfe={}, sehens_seen=[], teile_welt=3, teile_plan=0, teile_roh=3,
                         sehens_baeche=0, fortsetzungen=[]))
        with patch.object(daten, "lade", return_value=welt), patch.object(fx, "Gelaende", Terrain), \
                patch.object(fx, "gewaesser_bilden", side_effect=bilden):
            for name, optionen, erwartete_ids in (("voll", [], ["A","B","C"]), ("teil", ["--nur","A"], ["A","B"])):
                with self.subTest(umfang=name):
                    out = self.root / name
                    log = io.StringIO()
                    with contextlib.redirect_stdout(log):
                        code = fx.main(["--aus", str(out), "--daten2m", str(self.root), "--ohne-erkennung"] + optionen)
                    self.assertEqual(code, 0, log.getvalue())
                    manifest = pk.lies_manifest(out)
                    self.assertEqual(manifest["umfang"]["gewaesser"], erwartete_ids)
                    self.assertEqual(manifest["umfang"]["art"], name)
                    self.assertEqual(manifest["formal"], "bestanden")
                    a_export = json.loads((out / "A/fluss_sim.json").read_text())["gewaesser"][0]
                    self.assertEqual(a_export["water_body"]["overlap_material_priority"], 9)
                    if name == "teil":
                        wz = json.loads((out / "wasserzonen.json").read_text())
                        self.assertTrue(all(z["id"].startswith("TEST_") for z in wz["zonen"]))
                    with contextlib.redirect_stdout(log):
                        self.assertEqual(fp.main([str(out), "--daten2m", str(self.root), "--ohne-erkennung"]), 0)
            echt = fx.baue_gewaesser_v3
            def kaputt(*args):
                e = echt(*args)
                if e["id"] == "A":
                    e["muendung"]["ziel"] = "FEHLENDES_ZIEL"
                return e
            ziel = self.root / "abgelehnt"
            with patch.object(fx, "baue_gewaesser_v3", side_effect=kaputt), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(fx.main(["--aus", str(ziel), "--daten2m", str(self.root), "--ohne-erkennung"]), 1)
            self.assertFalse(ziel.exists())
            self.assertTrue((self.root / "voll/paket.json").exists())


if __name__ == "__main__":
    unittest.main()
