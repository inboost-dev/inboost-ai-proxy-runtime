#!/usr/bin/env python3
"""Builds all npm release packages into dist/ directory:
1. @inboost-dev/inboost-ai-proxy (Organization primary package)
2. @inboost-dev/inboost-proxy (Organization alias package)
3. inboost-ai-proxy (Root primary package)
4. inboost-proxy (Root alias package)
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
BASE_PKG_JSON = REPO_ROOT / "package.json"


PACKAGES = [
    {
        "name": "@inboost-pro/inboost-ai-proxy",
        "description": "Local inference proxy and reliability gateway for Claude Code, Cursor, OpenHands, and Cline",
        "tarball_expected": "inboost-pro-inboost-ai-proxy-0.3.1.tgz",
        "publish_access": "public",
    },
    {
        "name": "@inboost-pro/inboost-proxy",
        "description": "Local inference proxy and reliability gateway for Claude Code, Cursor, OpenHands, and Cline (alias package)",
        "tarball_expected": "inboost-pro-inboost-proxy-0.3.1.tgz",
        "publish_access": "public",
    },
    {
        "name": "inboost-ai-proxy",
        "description": "Local inference proxy and reliability gateway for Claude Code, Cursor, OpenHands, and Cline",
        "tarball_expected": "inboost-ai-proxy-0.3.1.tgz",
        "publish_access": "public",
    },
    {
        "name": "inboost-proxy",
        "description": "Local inference proxy and reliability gateway for Claude Code, Cursor, OpenHands, and Cline (alias package)",
        "tarball_expected": "inboost-proxy-0.3.1.tgz",
        "publish_access": "public",
    },
]


def build_npm_packages():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    orig_content = BASE_PKG_JSON.read_text(encoding="utf-8")
    base_data = json.loads(orig_content)

    built_tarballs = []
    try:
        for pkg in PACKAGES:
            print(f"Building npm package: {pkg['name']}...")
            pkg_data = dict(base_data)
            pkg_data["name"] = pkg["name"]
            pkg_data["description"] = pkg["description"]
            pkg_data["publishConfig"] = {"access": pkg["publish_access"]}
            pkg_data["bin"] = {
                "inboost-proxy": "./bin/inboost-proxy.js",
                "inboost-ai-proxy": "./bin/inboost-proxy.js",
            }

            BASE_PKG_JSON.write_text(json.dumps(pkg_data, indent=2) + "\n", encoding="utf-8")

            res = subprocess.run(
                ["npm", "pack", "--pack-destination", str(DIST_DIR)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            tarball_name = res.stdout.strip().splitlines()[-1]
            tarball_path = DIST_DIR / tarball_name
            print(f"  ✓ Packed: {tarball_path.name} ({tarball_path.stat().st_size / 1024:.1f} KB)")
            built_tarballs.append(tarball_path)

    finally:
        # Default package.json name to @inboost-pro/inboost-ai-proxy with public access
        base_data["name"] = "@inboost-pro/inboost-ai-proxy"
        base_data["publishConfig"] = {"access": "public"}
        base_data["bin"] = {
            "inboost-proxy": "./bin/inboost-proxy.js",
            "inboost-ai-proxy": "./bin/inboost-proxy.js",
        }
        BASE_PKG_JSON.write_text(json.dumps(base_data, indent=2) + "\n", encoding="utf-8")

    print("\nAll npm packages built successfully:")
    for t in built_tarballs:
        print(f"  • {t.name}")


if __name__ == "__main__":
    build_npm_packages()
