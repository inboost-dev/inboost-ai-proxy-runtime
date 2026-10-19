#!/usr/bin/env python3
"""Builds standalone native stripped binaries for InBoost AI Proxy.

Supports:
- Linux x86_64: `inboost-proxy-linux-x86_64`
- macOS arm64 (Apple Silicon): `inboost-proxy-darwin-arm64`
- macOS x86_64 (Intel): `inboost-proxy-darwin-x86_64`

Usage:
    python3 scripts/build_standalone.py [--output-dir dist] [--target-os auto|darwin|linux] [--arch auto|arm64|x86_64]
"""
from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROXY_REPO = REPO_ROOT.parent / "inboost-ai-proxy"


def detect_platform() -> tuple[str, str]:
    os_name = platform.system().lower()
    if "darwin" in os_name:
        os_target = "darwin"
    elif "linux" in os_name:
        os_target = "linux"
    else:
        os_target = "generic"

    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        arch_target = "arm64"
    elif machine in ("x86_64", "amd64"):
        arch_target = "x86_64"
    else:
        arch_target = machine

    return os_target, arch_target


def build_binary(
    output_dir: Path,
    target_os: str = "auto",
    arch: str = "auto",
    dry_run: bool = False,
) -> Path:
    auto_os, auto_arch = detect_platform()
    final_os = auto_os if target_os == "auto" else target_os
    final_arch = auto_arch if arch == "auto" else arch

    binary_name = f"inboost-proxy-{final_os}-{final_arch}"
    output_dir.mkdir(parents=True, exist_ok=True)
    target_binary = output_dir / binary_name

    print(f"[*] Building standalone binary: {binary_name} (OS: {final_os}, Arch: {final_arch})")

    # Locate proxy entry point
    entry_point = PROXY_REPO / "src" / "inboost_proxy" / "app.py"
    if not entry_point.exists():
        entry_point = REPO_ROOT / "src" / "inboost_proxy" / "app.py"

    pyinstaller_bin = shutil.which("pyinstaller")
    if not pyinstaller_bin:
        print("[!] PyInstaller is not installed in the current environment.", file=sys.stderr)
        print("    Install it via: pip install pyinstaller", file=sys.stderr)
        if dry_run or not entry_point.exists():
            print(f"[+] Dry run: Simulating target output {target_binary}")
            target_binary.write_bytes(b"\x7fELF" if final_os == "linux" else b"\xcf\xfa\xed\xfe")
            return target_binary
        sys.exit(1)

    pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"] if shutil.which("pyinstaller") or True else ["pyinstaller"]

    # Gather search paths
    paths = [
        str(PROXY_REPO / "src"),
        str(REPO_ROOT.parent / "inboost-ai-core" / "src"),
        str(REPO_ROOT.parent / "agent-tool-parser" / "src"),
    ]
    existing_paths = [p for p in paths if Path(p).exists()]

    hidden_imports = [
        "uvicorn",
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
        "fastapi",
        "pydantic",
        "inboost_proxy",
        "inboost_core",
        "inboost_router",
        "agent_tool_parser",
    ]

    cmd = pyinstaller_cmd + [
        "--onefile",
        "--name",
        binary_name,
        "--distpath",
        str(output_dir),
        "--clean",
        "--noconfirm",
    ]
    for p in existing_paths:
        cmd.extend(["--paths", p])
    for hi in hidden_imports:
        cmd.extend(["--hidden-import", hi])
    cmd.append(str(entry_point))

    print(f"[*] Running PyInstaller: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    # Post-processing: strip symbols
    strip_bin = shutil.which("strip")
    if strip_bin and target_binary.exists():
        print(f"[*] Stripping symbols from {target_binary.name}...")
        try:
            subprocess.run([strip_bin, str(target_binary)], check=True)
        except Exception as e:
            print(f"    Warning: symbol stripping failed: {e}", file=sys.stderr)

    # Post-processing for macOS: ad-hoc codesign
    if final_os == "darwin" and target_binary.exists():
        codesign_bin = shutil.which("codesign")
        if codesign_bin:
            print(f"[*] Ad-hoc code signing macOS binary: {target_binary.name}...")
            try:
                subprocess.run([codesign_bin, "--force", "--deep", "--sign", "-", str(target_binary)], check=True)
            except Exception as e:
                print(f"    Warning: codesign failed: {e}", file=sys.stderr)

    print(f"[✓] Standalone binary ready at: {target_binary} ({target_binary.stat().st_size:,} bytes)")
    return target_binary


def main() -> None:
    parser = argparse.ArgumentParser(description="InBoost Standalone Binary Builder (macOS & Linux)")
    parser.add_argument("--output-dir", default="dist", help="Output directory for compiled binary")
    parser.add_argument("--target-os", choices=["auto", "darwin", "linux"], default="auto", help="Target OS")
    parser.add_argument("--arch", choices=["auto", "arm64", "x86_64"], default="auto", help="Target architecture")
    parser.add_argument("--dry-run", action="store_true", help="Simulate build without PyInstaller")
    args = parser.parse_args()

    build_binary(
        output_dir=Path(args.output_dir),
        target_os=args.target_os,
        arch=args.arch,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
