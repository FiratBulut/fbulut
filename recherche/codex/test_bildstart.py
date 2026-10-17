"""Offline failure probes; never touch the production root or invoke image tools."""

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import bildstart


class ImageStartTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-image-start-test-")
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "input.md"
        self.source.write_text("A grey rock. Reference SHA-256: test-fixture.", encoding="utf-8")

    def tearDown(self):
        # Cleanup is limited to the exact temporary directory created by this test.
        assert self.root == Path(self.temp.name).resolve()
        assert self.root.name.startswith("codex-image-start-test-")
        self.temp.cleanup()

    def reserve(self, **kwargs):
        args = dict(root=self.root, asset_id="test-rock", revision="r001",
                    owner="test-session/run-1", input_file=self.source)
        args.update(kwargs)
        return bildstart.reserve(**args)

    def test_record_matches_frozen_input(self):
        record = self.reserve()
        self.assertEqual(record["input_sha256"], hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertEqual(record, bildstart.inspect(self.root, "test-rock", "r001"))

    def test_duplicate_owner_is_not_permission_to_generate_again(self):
        first = self.reserve()
        with self.assertRaises(bildstart.StartError):
            self.reserve()
        self.assertEqual(first, bildstart.inspect(self.root, "test-rock", "r001"))

    def test_changed_input_does_not_overwrite_existing_reservation(self):
        first = self.reserve()
        self.source.write_text("Different image prompt", encoding="utf-8")
        with self.assertRaises(bildstart.StartError):
            self.reserve(owner="another-session")
        self.assertEqual(first, bildstart.inspect(self.root, "test-rock", "r001"))

    def test_existing_delivery_blocks_new_reservation(self):
        target = bildstart.output_directory(self.root, "test-rock", "r001")
        target.mkdir(parents=True)
        (target / "image.png").write_bytes(b"existing-result")
        with self.assertRaises(bildstart.StartError):
            self.reserve()

    def test_invalid_paths_and_device_names(self):
        for bad in ("../escape", "a/b", "a\\b", "con", "nul", "com1", "lpt9", "A", "x."):
            with self.subTest(asset=bad), self.assertRaises(bildstart.StartError):
                self.reserve(asset_id=bad)
        for bad in ("r000", "r1", "../r001", "r1000"):
            with self.subTest(revision=bad), self.assertRaises(bildstart.StartError):
                self.reserve(revision=bad)

    def test_missing_input_does_not_reserve(self):
        with self.assertRaises(OSError):
            self.reserve(input_file=self.root / "missing.md")
        self.assertFalse((self.root / "test-rock").exists())

    def test_empty_input_and_owner_are_rejected(self):
        with self.assertRaises(bildstart.StartError):
            self.reserve(owner=" ")
        self.source.write_text(" ", encoding="utf-8")
        with self.assertRaises(bildstart.StartError):
            self.reserve()

    def test_incomplete_marker_still_blocks(self):
        target = bildstart.output_directory(self.root, "test-rock", "r001")
        target.mkdir(parents=True)
        (target / bildstart.MARKER).write_text("", encoding="utf-8")
        with self.assertRaises(bildstart.StartError):
            self.reserve()
        with self.assertRaises(ValueError):
            bildstart.inspect(self.root, "test-rock", "r001")

    def test_failed_flush_keeps_marker(self):
        with patch.object(bildstart.os, "fsync", side_effect=OSError("simulated interruption")):
            with self.assertRaises(OSError):
                self.reserve()
        with self.assertRaises(bildstart.StartError):
            self.reserve()

    def test_marker_for_other_revision_is_rejected(self):
        self.reserve()
        marker = self.root / "test-rock/codex/r001" / bildstart.MARKER
        data = json.loads(marker.read_text(encoding="utf-8"))
        data["revision"] = "r002"
        marker.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(bildstart.StartError):
            bildstart.inspect(self.root, "test-rock", "r001")

    def test_two_processes_only_one_can_reserve(self):
        command = [sys.executable, str(Path(bildstart.__file__).resolve()), "reserve",
                   "--root", str(self.root), "--asset-id", "test-rock", "--revision", "r001",
                   "--owner", "parallel-test", "--input", str(self.source)]
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: subprocess.run(command, capture_output=True), range(2)))
        self.assertEqual(sorted(r.returncode for r in results), [0, 2])

    def test_directory_link_escape_is_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        allowed = self.root / "allowed"
        allowed.mkdir()
        link = allowed / "test-rock"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            if os.name != "nt":
                self.skipTest(f"Directory symlinks unavailable: {exc}")
            environment = dict(os.environ, CODEX_TEST_LINK=str(link), CODEX_TEST_TARGET=str(outside))
            result = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                 "New-Item -ItemType Junction -Path $env:CODEX_TEST_LINK "
                 "-Target $env:CODEX_TEST_TARGET -ErrorAction Stop | Out-Null"],
                capture_output=True, env=environment,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
            self.assertTrue(link.is_junction())
        try:
            with self.assertRaises(bildstart.StartError):
                self.reserve(root=allowed)
        finally:
            assert link.parent == allowed and link.resolve() == outside
            if link.is_junction():
                link.rmdir()  # Removes only the verified junction, not its target.
            else:
                link.unlink()
        self.assertTrue(outside.is_dir())


if __name__ == "__main__":
    unittest.main()
