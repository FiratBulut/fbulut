"""Reserve a local image execution once; never generate, publish, or unlock anything."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid


DEFAULT_ROOT = Path(
    "D:/Das Lied der Asche/ELDARIEN_ENVIRONMENT_SKILLS_V1/production/source/asset_pipeline"
)
MARKER = "ausfuehrung.json"
RESERVED_WINDOWS_NAMES = {"con", "prn", "aux", "nul"} | {
    f"{prefix}{number}" for prefix in ("com", "lpt") for number in range(1, 10)
}


class StartError(Exception):
    pass


def output_directory(root, asset_id, revision):
    if (
        not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", asset_id)
        or len(asset_id) > 80
        or asset_id in RESERVED_WINDOWS_NAMES
    ):
        raise StartError("Invalid asset ID; use a short lowercase slug, not a device name.")
    if not re.fullmatch(r"r[0-9]{3}", revision) or revision == "r000":
        raise StartError("Revision must be r001 through r999.")
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise StartError("Asset root is not a directory.")
    target = root / asset_id / "codex" / revision
    if not target.resolve().is_relative_to(root):
        raise StartError("Output path leaves the asset root through a directory link.")
    return target


def reserve(root, asset_id, revision, owner, input_file):
    if not owner.strip() or len(owner) > 200:
        raise StartError("A concrete session/run owner is required (up to 200 characters).")
    target = output_directory(root, asset_id, revision)
    source = Path(input_file).resolve(strict=True)
    if not source.is_file():
        raise StartError("Frozen input is not a file.")
    frozen = source.read_bytes()
    if not frozen.strip():
        raise StartError("Frozen input is empty.")
    if target.exists() and any(item.name != MARKER for item in target.iterdir()):
        raise StartError("Output directory already contains files; recover the existing delivery first.")
    record = {
        "schema": 1,
        "asset_id": asset_id,
        "revision": revision,
        "owner": owner,
        "execution_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_sha256": hashlib.sha256(frozen).hexdigest(),
    }
    target.mkdir(parents=True, exist_ok=True)
    target = output_directory(root, asset_id, revision)
    marker = target / MARKER
    try:
        # Exclusive creation, not a check-then-write: only one contender can win.
        with marker.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(record, handle, ensure_ascii=True, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise StartError(
            "Execution marker already exists. Do not start a new generation; inspect and recover."
        ) from exc
    # A partial marker from an interrupted write intentionally stays and blocks retries.
    return record


def inspect(root, asset_id, revision):
    target = output_directory(root, asset_id, revision)
    marker = target / MARKER
    if not marker.resolve().is_relative_to(Path(root).resolve(strict=True)):
        raise StartError("Execution marker leaves the asset root.")
    record = json.loads(marker.read_text(encoding="utf-8"))
    if (
        not isinstance(record, dict)
        or record.get("schema") != 1
        or record.get("asset_id") != asset_id
        or record.get("revision") != revision
        or not isinstance(record.get("owner"), str)
        or not record["owner"].strip()
        or not re.fullmatch(r"[0-9a-f]{64}", str(record.get("input_sha256", "")))
        or not record.get("execution_id")
    ):
        raise StartError("Execution marker is invalid; keep it and clarify the previous run.")
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("reserve", "inspect"))
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--asset-id", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--owner")
    parser.add_argument("--input", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.action == "reserve":
            if not args.owner or not args.input:
                raise StartError("reserve requires --owner and --input.")
            record = reserve(args.root, args.asset_id, args.revision, args.owner, args.input)
        else:
            record = inspect(args.root, args.asset_id, args.revision)
        print(json.dumps(record, ensure_ascii=True))
        return 0
    except (StartError, OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc), "start_allowed": False}, ensure_ascii=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
