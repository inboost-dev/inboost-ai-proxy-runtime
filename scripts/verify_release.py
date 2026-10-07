#!/usr/bin/env python3
"""Verifies release assets against checksums.txt and validates security invariants.

Usage:
    python3 scripts/verify_release.py [--checksums dist/checksums.txt]
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from scripts.build_release_manifest import FORBIDDEN_PATTERNS, scan_file_for_leaks


def verify_checksums(checksums_file: Path) -> bool:
    if not checksums_file.exists():
        print(f"Error: {checksums_file} does not exist", file=sys.stderr)
        return False

    base_dir = checksums_file.parent
    lines = checksums_file.read_text(encoding="utf-8").strip().splitlines()
    all_ok = True

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            print(f"Malformed checksum line: {line}", file=sys.stderr)
            all_ok = False
            continue

        expected_hash, filename = parts
        target = base_dir / filename.strip()
        if not target.exists():
            print(f"Missing artifact: {target}", file=sys.stderr)
            all_ok = False
            continue

        # Check hash
        h = hashlib.sha256()
        with open(target, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        actual_hash = h.hexdigest()

        if actual_hash != expected_hash:
            print(f"FAIL: Hash mismatch for {filename} (expected {expected_hash}, got {actual_hash})", file=sys.stderr)
            all_ok = False
        else:
            print(f"OK:   {filename}")

        # Security scan
        from scripts.build_release_manifest import scan_file_for_leaks
        leaks = scan_file_for_leaks(target)
        if leaks:
            for leak in leaks:
                print(f"FAIL: Forbidden pattern detected in {filename}: {leak}", file=sys.stderr)
            all_ok = False


    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Verify release asset checksums and security")
    parser.add_argument("--checksums", default="dist/checksums.txt", help="Path to checksums.txt")
    args = parser.parse_args()

    success = verify_checksums(Path(args.checksums))
    if not success:
        sys.exit(1)
    print("All release assets verified successfully.")


if __name__ == "__main__":
    main()
