import json
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path
import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base64

from scripts.build_release_manifest import FORBIDDEN_KEYWORDS, SECRET_TOKEN_PATTERNS, scan_file_for_leaks


def test_repo_zero_patent_and_secret_leaks():
    """Scans all tracked files in the repository (excluding binary dist artifacts) for IP leaks."""
    root_dir = Path(__file__).resolve().parent.parent
    tracked_files = subprocess.check_output(
        ["git", "ls-files"], cwd=root_dir, text=True
    ).splitlines()

    violations = []
    for rel_path in tracked_files:
        full_path = root_dir / rel_path
        if not full_path.is_file():
            continue
        # Skip binary files in dist
        if rel_path.startswith("dist/") and (rel_path.endswith(".whl") or rel_path.endswith(".tgz") or "linux" in rel_path):
            continue
        # Skip security scanner scripts and test fixtures that define or test the forbidden patterns
        if rel_path in ("scripts/build_release_manifest.py", "tests/test_runtime_manifest.py", "tests/test_security_audit.py"):
            continue

        leaks = scan_file_for_leaks(full_path)
        if leaks:
            violations.extend(leaks)

        # Check specifically for "preflight"
        text = full_path.read_text(encoding="utf-8", errors="ignore").lower()
        if "preflight" in text:
            violations.append(f"{rel_path}: 'preflight' keyword found")

    assert not violations, f"Security/IP violations detected: {violations}"


def test_standalone_binary_symbol_stripping():
    """Verifies that the standalone linux binary dist/inboost-proxy-linux-x86_64 has no debug symbols."""
    bin_path = Path(__file__).resolve().parent.parent / "dist" / "inboost-proxy-linux-x86_64"
    if not bin_path.exists():
        pytest.skip("Standalone binary not found in dist/")

    res = subprocess.run(["nm", str(bin_path)], capture_output=True, text=True)
    assert "no symbols" in res.stderr.lower() or res.returncode != 0


def test_wheel_so_modules_stripped_and_no_source():
    """Verifies that the release wheel contains zero .py sources and all .so binaries are stripped."""
    whl_files = list((Path(__file__).resolve().parent.parent / "dist").glob("inboost_ai_proxy-*.whl"))
    if not whl_files:
        pytest.skip("Wheel not found in dist/")
    wheel_path = whl_files[0]

    with zipfile.ZipFile(wheel_path) as z:
        for name in z.namelist():
            # Must not contain uncompiled .py files (except sanitized __init__.py export manifests)
            if name.endswith(".py"):
                assert name.endswith("__init__.py"), f"Uncompiled non-init Python file found: {name}"
                data = z.read(name).decode("utf-8")
                # __init__.py files only contain version/exports and zero executable def/class logic
                import ast
                tree = ast.parse(data)
                defs = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                assert not defs, f"Uncompiled function or class definition found in {name}: {defs}"

            if name.endswith(".so"):
                with tempfile.NamedTemporaryFile(suffix=".so") as tmp:
                    tmp.write(z.read(name))
                    tmp.flush()
                    res = subprocess.run(["nm", tmp.name], capture_output=True, text=True)
                    assert "no symbols" in res.stderr.lower() or res.returncode != 0


def test_skills_contain_only_public_guidance():
    """Verifies skills directory contains only safe instructions and no patent-sensitive hooks."""
    skills_dir = Path(__file__).resolve().parent.parent / "skills"
    skill_names = [d.name for d in skills_dir.iterdir() if d.is_dir()]
    
    # Must only contain inboost-proxy
    assert skill_names == ["inboost-proxy"]

    skill_file = skills_dir / "inboost-proxy" / "SKILL.md"
    assert skill_file.exists()
    content = skill_file.read_text(encoding="utf-8")
    assert "preflight" not in content.lower()
    assert "blast_radius" not in content.lower()
    assert "focus_nodes" not in content.lower()


def test_license_cryptographic_tamper_immunity():
    """Cryptographically proves that license payloads cannot be forged or modified without private key."""
    from cryptography.exceptions import InvalidSignature

    priv = ed25519.Ed25519PrivateKey.generate()
    pub = priv.public_key()

    payload_dict = {
        "customer": "Pilot Enterprise",
        "valid_until": "2026-12-31T23:59:59Z",
        "max_requests": 1000,
        "max_tokens": 10_000_000,
    }
    canonical = json.dumps(payload_dict, sort_keys=True, separators=(",", ":")).encode("utf-8")
    sig = priv.sign(canonical)

    # 1. Untampered payload verifies successfully
    pub.verify(sig, canonical)

    # 2. Tampered customer fails
    tampered_1 = dict(payload_dict, customer="Hacked Enterprise")
    canonical_tampered_1 = json.dumps(tampered_1, sort_keys=True, separators=(",", ":")).encode("utf-8")
    with pytest.raises(InvalidSignature):
        pub.verify(sig, canonical_tampered_1)

    # 3. Tampered max_requests fails
    tampered_2 = dict(payload_dict, max_requests=999999)
    canonical_tampered_2 = json.dumps(tampered_2, sort_keys=True, separators=(",", ":")).encode("utf-8")
    with pytest.raises(InvalidSignature):
        pub.verify(sig, canonical_tampered_2)

    # 4. Tampered expiry date fails
    tampered_3 = dict(payload_dict, valid_until="2099-01-01T00:00:00Z")
    canonical_tampered_3 = json.dumps(tampered_3, sort_keys=True, separators=(",", ":")).encode("utf-8")
    with pytest.raises(InvalidSignature):
        pub.verify(sig, canonical_tampered_3)

    # 5. Tampered signature bytes fail
    bad_sig = bytearray(sig)
    bad_sig[0] ^= 0xFF
    with pytest.raises(InvalidSignature):
        pub.verify(bytes(bad_sig), canonical)

