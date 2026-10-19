import subprocess
import time
import urllib.request
from pathlib import Path
import pytest


def test_standalone_binary_version_and_help():
    dist_dir = Path(__file__).resolve().parent.parent / "dist"
    binary_path = dist_dir / "inboost-proxy-linux-x86_64"
    if not binary_path.exists():
        pytest.skip("Standalone binary not found in dist/")

    # Test --version
    res_ver = subprocess.run([str(binary_path), "--version"], capture_output=True, text=True)
    assert res_ver.returncode == 0
    assert "inboost-proxy v0.3.3" in res_ver.stdout or "inboost-proxy v0.3.3" in res_ver.stderr

    # Test --help
    res_help = subprocess.run([str(binary_path), "--help"], capture_output=True, text=True)
    assert res_help.returncode == 0
    assert "inboost-proxy" in res_help.stdout


def test_standalone_binary_live_health():
    dist_dir = Path(__file__).resolve().parent.parent / "dist"
    binary_path = dist_dir / "inboost-proxy-linux-x86_64"
    if not binary_path.exists():
        pytest.skip("Standalone binary not found in dist/")

    test_port = 8092
    proc = subprocess.Popen(
        [str(binary_path), "--port", str(test_port), "--no-prompt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    passed = False
    try:
        for _ in range(25):
            time.sleep(0.4)
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{test_port}/health", timeout=1) as resp:
                    if resp.status == 200:
                        passed = True
                        break
            except Exception:
                pass
    finally:
        proc.terminate()
        proc.wait()

    assert passed, f"Standalone binary failed to serve /health on port {test_port}"
