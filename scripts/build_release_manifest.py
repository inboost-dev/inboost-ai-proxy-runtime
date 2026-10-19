#!/usr/bin/env python3
"""Builds a cryptographic release manifest and checksums.txt for InBoost Runtime assets.

Usage:
    python3 scripts/build_release_manifest.py [--version VERSION] [--dist-dir DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import re
import tarfile
import zipfile

# Prohibited internal keywords & tokens (strict IP, patent & secret protection)
FORBIDDEN_KEYWORDS = [
    # Internal patent portfolio markers & filings
    "PAT-",
    "rospatent",
    "fips.ru",
    "patent application",
    "pct/ru",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN PRIVATE KEY",
    # Internal infrastructure & credentials
    "internal.inboost",
    "corp.inboost",
]

SECRET_TOKEN_PATTERNS = [
    (re.compile(r"ghp_[a-zA-Z0-9]{10,}"), "ghp_"),
    (re.compile(r"github_pat_[a-zA-Z0-9_]{10,}"), "github_pat_"),
    (re.compile(r"sk-ant-[a-zA-Z0-9_\-]{10,}"), "sk-ant-"),
    (re.compile(r"sk-proj-[a-zA-Z0-9_\-]{10,}"), "sk-proj-"),
    (re.compile(r"sk-live-[a-zA-Z0-9_\-]{10,}"), "sk-live-"),
]

# Kept for backward compatibility with external references / tests
FORBIDDEN_PATTERNS = FORBIDDEN_KEYWORDS + ["sk-ant-", "sk-proj-", "sk-live-", "ghp_", "github_pat_"]


def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def scan_bytes_for_leaks(data: bytes, source_name: str) -> list[str]:
    leaks = []
    text = data.decode("utf-8", errors="ignore")
    text_lower = text.lower()
    for kw in FORBIDDEN_KEYWORDS:
        if kw == "PAT-":
            if "PAT-" in text:
                leaks.append(f"{source_name}:{kw}")
        elif kw.lower() in text_lower:
            leaks.append(f"{source_name}:{kw}")
    for pat, label in SECRET_TOKEN_PATTERNS:
        if pat.search(text):
            leaks.append(f"{source_name}:{label}")
    return leaks


def scan_file_for_leaks(filepath: Path) -> list[str]:
    """Inspects files, archives (zip/whl/tgz), and binaries for prohibited proprietary tokens."""
    leaks = []
    name_lower = filepath.name.lower()

    # 1. Zip / Wheel archives (.whl, .zip)
    if name_lower.endswith((".whl", ".zip")):
        try:
            with zipfile.ZipFile(filepath, "r") as z:
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    # Check filename itself
                    for kw in FORBIDDEN_KEYWORDS:
                        if kw.lower() in info.filename.lower():
                            leaks.append(f"{filepath.name}::{info.filename}:{kw}")
                    for pat, label in SECRET_TOKEN_PATTERNS:
                        if pat.search(info.filename):
                            leaks.append(f"{filepath.name}::{info.filename}:{label}")
                    # Decompress and scan code/text files under 10MB
                    if info.file_size < 10 * 1024 * 1024:
                        try:
                            data = z.read(info.filename)
                            leaks.extend(scan_bytes_for_leaks(data, f"{filepath.name}::{info.filename}"))
                        except Exception:
                            pass
        except zipfile.BadZipFile:
            leaks.extend(scan_bytes_for_leaks(filepath.read_bytes(), filepath.name))
        except Exception as e:
            leaks.append(f"{filepath.name}:archive_read_error:{e}")
        return list(dict.fromkeys(leaks))

    # 2. Tar archives (.tgz, .tar.gz, .tar)
    if name_lower.endswith((".tgz", ".tar.gz", ".tar")):
        try:
            with tarfile.open(filepath, "r:*") as tar:
                for member in tar.getmembers():
                    if not member.isfile():
                        continue
                    for kw in FORBIDDEN_KEYWORDS:
                        if kw.lower() in member.name.lower():
                            leaks.append(f"{filepath.name}::{member.name}:{kw}")
                    for pat, label in SECRET_TOKEN_PATTERNS:
                        if pat.search(member.name):
                            leaks.append(f"{filepath.name}::{member.name}:{label}")
                    if member.size < 10 * 1024 * 1024:
                        try:
                            f = tar.extractfile(member)
                            if f:
                                data = f.read()
                                leaks.extend(scan_bytes_for_leaks(data, f"{filepath.name}::{member.name}"))
                        except Exception:
                            pass
        except (tarfile.TarError, gzip.BadGzipFile) if "gzip" in sys.modules else tarfile.TarError:
            leaks.extend(scan_bytes_for_leaks(filepath.read_bytes(), filepath.name))
        except Exception as e:
            leaks.append(f"{filepath.name}:archive_read_error:{e}")
        return list(dict.fromkeys(leaks))

    # 3. Native binaries and plain files (streaming with overlap)
    try:
        chunk_size = 1024 * 1024
        overlap = 1024
        prev_tail = ""
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                text_chunk = prev_tail + chunk.decode("utf-8", errors="ignore")
                text_chunk_lower = text_chunk.lower()
                for kw in FORBIDDEN_KEYWORDS:
                    if kw == "PAT-":
                        if "PAT-" in text_chunk:
                            leaks.append(f"{filepath.name}:{kw}")
                    elif kw.lower() in text_chunk_lower:
                        leaks.append(f"{filepath.name}:{kw}")
                for pat, label in SECRET_TOKEN_PATTERNS:
                    if pat.search(text_chunk):
                        leaks.append(f"{filepath.name}:{label}")
                prev_tail = text_chunk[-overlap:] if len(text_chunk) >= overlap else text_chunk
    except Exception:
        pass

    return list(dict.fromkeys(leaks))



def build_manifest(version: str, dist_dir: Path, output_file: Path) -> dict:
    version = version.lstrip("v")
    dist_dir.mkdir(parents=True, exist_ok=True)
    artifacts = []
    checksum_lines = []

    for file_path in sorted(dist_dir.glob("*")):
        if (
            file_path.is_file()
            and not file_path.name.endswith(".json")
            and file_path.name != "checksums.txt"
        ):
            checksum = sha256_file(file_path)
            size_bytes = file_path.stat().st_size
            leaks = scan_file_for_leaks(file_path)
            if leaks:
                print(f"[SECURITY ALERT] Leak detected in {file_path.name}: {leaks}", file=sys.stderr)
                sys.exit(1)

            if file_path.name.endswith(".whl"):
                art_type = "wheel"
            elif file_path.name.endswith((".tgz", ".tar.gz", ".tar", ".zip")):
                art_type = "archive"
            elif file_path.name.startswith("inboost-proxy-"):
                art_type = "binary"
            else:
                art_type = "asset"

            entry = {
                "name": file_path.name,
                "sha256": checksum,
                "size_bytes": size_bytes,
                "type": art_type,
            }
            artifacts.append(entry)
            checksum_lines.append(f"{checksum}  {file_path.name}")

    manifest = {
        "version": version,
        "released_at": datetime.now(timezone.utc).isoformat(),
        "portal_url": "https://inboost.pro/ai-proxy",
        "documentation_url": "https://inboost.pro/ai-proxy",
        "issue_tracker": "https://github.com/inboost-dev/inboost-ai-proxy-runtime/issues",
        "artifacts": artifacts,
    }

    output_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    checksums_file = dist_dir / "checksums.txt"
    if checksum_lines:
        checksums_file.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    print(f"Manifest generated: {output_file} ({len(artifacts)} artifacts)")
    return manifest


def main():
    parser = argparse.ArgumentParser(description="InBoost Release Manifest Builder")
    parser.add_argument("--version", default="0.3.1", help="Release version (e.g. 0.3.1)")
    parser.add_argument("--dist-dir", default="dist", help="Directory containing release artifacts")
    parser.add_argument("--output", default="dist/release-manifest.json", help="Output manifest file")
    args = parser.parse_args()

    build_manifest(
        version=args.version,
        dist_dir=Path(args.dist_dir),
        output_file=Path(args.output),
    )


if __name__ == "__main__":
    main()
