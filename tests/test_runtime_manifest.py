import json
import pytest
from pathlib import Path

from scripts.build_release_manifest import build_manifest, scan_file_for_leaks
from scripts.verify_release import verify_checksums


def test_manifest_generation_and_verification(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()

    # Create dummy release artifact
    dummy_whl = dist_dir / "inboost_proxy-0.3.0-py3-none-any.whl"
    dummy_whl.write_bytes(b"PK\x03\x04dummy_wheel_binary_content_v0.3.0")

    manifest_file = dist_dir / "release-manifest.json"
    manifest = build_manifest("0.3.0", dist_dir, manifest_file)

    assert manifest["version"] == "0.3.0"
    assert manifest["portal_url"] == "https://inboost.pro/ai-proxy"
    assert len(manifest["artifacts"]) == 1
    assert manifest["artifacts"][0]["name"] == "inboost_proxy-0.3.0-py3-none-any.whl"

    checksums_file = dist_dir / "checksums.txt"
    assert checksums_file.exists()

    # Verify checksums
    assert verify_checksums(checksums_file) is True


def test_leak_detection(tmp_path):
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()

    clean_file = dist_dir / "clean.txt"
    clean_file.write_text("This is clean production documentation.")
    assert scan_file_for_leaks(clean_file) == []

    leaky_file = dist_dir / "leaky.txt"
    leaky_file.write_text("Internal tracking PAT-99 patent filing")
    assert any("PAT-" in l for l in scan_file_for_leaks(leaky_file))


def test_leak_detection_in_compressed_wheel(tmp_path):
    import zipfile
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir(exist_ok=True)

    # 1. Clean wheel
    clean_whl = dist_dir / "clean-0.1.0-py3-none-any.whl"
    with zipfile.ZipFile(clean_whl, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("pkg/__init__.py", "print('hello clean')\n")
        z.writestr("pkg/module.py", "def add(a, b): return a + b\n")
    assert scan_file_for_leaks(clean_whl) == []

    # 2. Leaky wheel with compressed internal file
    leaky_whl = dist_dir / "leaky-0.1.0-py3-none-any.whl"
    with zipfile.ZipFile(leaky_whl, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("pkg/__init__.py", "print('hello')\n")
        z.writestr("pkg/secret.py", "API_KEY = 'sk-ant-1234567890abcdef'\n# PAT-42 filing\n")
    
    leaks = scan_file_for_leaks(leaky_whl)
    assert len(leaks) >= 2
    assert any("sk-ant-" in l for l in leaks)
    assert any("PAT-" in l for l in leaks)


def test_leak_detection_in_compressed_tarball(tmp_path):
    import io
    import tarfile
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir(exist_ok=True)

    leaky_tgz = dist_dir / "leaky-package-1.0.0.tgz"
    with tarfile.open(leaky_tgz, "w:gz") as tar:
        payload = b"// sensitive internal domain\nconst host = 'internal.inboost.local';\n"
        ti = tarfile.TarInfo("package/config.js")
        ti.size = len(payload)
        tar.addfile(ti, io.BytesIO(payload))

    leaks = scan_file_for_leaks(leaky_tgz)
    assert len(leaks) >= 1
    assert any("internal.inboost" in l for l in leaks)

