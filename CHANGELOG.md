# Changelog

All notable changes to the InBoost Runtime & Proxy distribution will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.3.1] - 2026-10-07

### Security & Hardening
- **Mandatory Community Quota Enforcement**: Strictly enforce Community tier limits (`CommunityQuotaManager`) on all non-Pro runtime instances.
- Prevented bypass via `INBOOST_ENABLE_COMMUNITY_TIER=false` or configuration overrides: non-Pro runtimes automatically ignore disable flags and cap quotas to canonical bounds (`CANONICAL_COMMUNITY_LIMITS`).
- Prevented client-side quota inflation attacks by capping free and daily limits at canonical invariants.

### Added
- SWE-bench Verified 10-Task Evaluation Workflow (`.github/workflows/swebench-eval.yml`): automated A/B comparative benchmark running Claude Code directly vs. Claude Code + InBoost AI Proxy on SiliconFlow, publishing real-time scoreboards to GitHub Actions Step Summary.
- 2-Arms Comparative Evaluation Runner (`scripts/run_swebench_2arms.py`): turnkey evaluation harness measuring patch success rates, 0-byte diff rescue, SLM compute offload, loop interception, and inference spend delta.
- SWE-bench Verified Cohort 10 Dataset (`configs/swebench_cohort_10.json`): balanced benchmark cohort across requests, flask, pytest, seaborn, astropy, pylint, xarray, and scikit-learn.
- Claude Code Auto Mode Server bypass (`CLAUDE_CODE_AUTO_MODE_SERVER=0`) to ensure reliable local proxy dispatch without external classifier timeout.
- Third-Party Agent Integration Guide (`docs/THIRD_PARTY_AGENT_INTEGRATION_GUIDE.md`) covering OpenHands, Cursor, Claude Code, Cline, and Aider.
- Ready-to-use SiliconFlow International configuration profile (`configs/proxy_config.siliconflow.yaml`) with DeepSeek-V4 Pro and Flash presets.
- Default Anthropic upstream configuration updated to Claude 3.7 Sonnet (`claude-3-7-sonnet-20250219`).
- Interactive Login Autostart Prompt: `install.sh` prompts user to enable automatic startup on login, configuring systemd user service (`~/.config/systemd/user/inboost-proxy.service`) and shell login hooks.
- Default User Configuration in `~/.inboost/config.yaml`: installer automatically creates and binds configuration in `~/.inboost/config.yaml` with clear L1 (fast exploration) and L2 (deep reasoning) model targets.
- Hardened Binary-Level Community Quotas: removed user-facing `community` settings block from `configs/proxy_config.yaml`, strictly locking tier limits to internal binary enforcement and updating URLs to `https://inboost.pro/ai-proxy`.
- Offline-First Local Artifact Discovery: `install.sh` automatically checks for precompiled binaries, wheels, and npm packages in `dist/` and `bin/`, eliminating remote download failures when running from repository clones.
- Automatic Background Daemon & Health Verification: `install.sh` launches `inboost-proxy` daemon automatically in the background with `nohup`, monitors `/health` for initialization, exports `ANTHROPIC_BASE_URL="http://127.0.0.1:8080"`, and writes process PID and logs to `~/.inboost/`.
- Fixed Setuptools Flat-Layout Conflict: configured `[tool.setuptools] packages = []` in `pyproject.toml` to prevent editable/standard build failures when `skills/` and `configs/` directories are present.
- Universal Agent Environment CI Workflow: `.github/workflows/agent-integration-test.yml` validating unattended installation, skill discovery, and end-to-end SiliconFlow inference across Claude Code, Cursor, and OpenHands in clean Ubuntu runners.
- Universal IDE & Agent Skills Auto-Installer: native provisioning for Claude Code (`~/.claude/skills`, `CLAUDE.md`, commands), Cursor (`.cursor/rules/*.mdc`, `.cursorrules`, `~/.cursorrules`), OpenHands (`.openhands/microagents`, `AGENTS.md`), Cline (`.clinerules`), Windsurf, and Antigravity.
- Native NPM Runtime Distribution: added `package.json`, `bin/inboost-proxy.js`, and bundled skills directory to runtime repository, supporting resilient `npx inboost-proxy` execution.
- Multi-Stage Fallback Architecture: `bin/inboost-proxy.js` upgraded with recursive self-invocation guard and embedded Node.js HTTP gateway fallback.
- Recompiled Standalone Binary: updated `dist/inboost-proxy-linux-x86_64` and release manifest with native `--install-skills` and non-blocking headless modes.
- Native macOS Standalone Binary Builds: automated compilation and distribution for `inboost-proxy-darwin-arm64` (Apple Silicon M1-M4) and `inboost-proxy-darwin-x86_64` (Intel x86_64) alongside `inboost-proxy-linux-x86_64`.
- Multi-Platform GitHub Actions Matrix: `.github/workflows/release.yml` upgraded to cross-compile and verify Linux and macOS binaries on isolated clean runners (`ubuntu-latest`, `macos-14`, `macos-13`).
- Standalone Binary Build Utility: `scripts/build_standalone.py` implementing PyInstaller compilation, symbol stripping, and macOS ad-hoc codesigning.
- Hardened Cryptographic Installer: `install.sh` enhanced with direct binary downloads, SHA-256 verification against official `checksums.txt`, secure `mktemp -d` temp isolation, and automatic macOS quarantine removal.
- Deep Decompressing Archive Leak Scanner: `scripts/build_release_manifest.py` and `scripts/verify_release.py` upgraded with native ZIP/WHL and TGZ decompression inspection, eliminating false-negative blindspots in compressed release artifacts.
- Official SWE-bench Verified 30 Cohort evaluation and Single-Shot Verification report (`benchmarks/SWEBENCH_VERIFIED_30_REPORT.md`).
- Standardized SWE-bench Verified task cohort configuration (`configs/swebench_cohort_30.json`) and gateway configuration (`configs/proxy_config.yaml`).
- Comprehensive benchmark telemetry collection and evaluation runs tracking.
- Trust Boundary Management and Context Separation architecture mitigating semantic backdoors (addressing Habr #1086966).
- Added SWE-bench Verified 2-arms comparative evaluation harness (`scripts/run_swebench_2arms.py`).
- Structured issue templates for Claude Code, Cursor, and OpenHands integrations.

### Changed
- Standardized architecture documentation and benchmark reports to modern **L0 / L1 / L2** cognitive runtime tiering (L0 Local CPU Core, L1 Fast SLM 7B, L2 Deep Heavy GPU).
- Transitioned repository access to **Public Pilot** distribution hub (`Access: Public Pilot`).
- Clarified security model: syntactic discipline is paired with isolated semantic verification and immutable policy sourcing.
- Consolidated all inquiries, support, and licensing requests to GitHub Issues and `inbound@inboost.pro`.
- Standardized enterprise SLA requirements to Commercial Pro License AND Bring-Your-Own-Key (BYOK) mode.
- Formalized Community Edition terms: explicit consent for anonymized telemetry collection and comprehensive disclaimer of liability for third-party inference servers.


## [0.3.0] - 2026-10-02

### Added
- One-line npm & pipx global installation (`npm install -g inboost-proxy`, `npx inboost-proxy`, `pipx install inboost-ai-proxy`).
- Community freemium tier with 10 free pristine tasks and 20 sponsored tasks.
- Educational value HUD reporting cost savings, latency improvements, and trajectory stability.
- Broad upstream gateway support across OpenRouter, GigaChat, and standard OpenAI/Anthropic compatible endpoints.
- Automated code repair engine and repository context optimization.

### Changed
- Standardized official portal URLs to `https://inboost.pro`.
- Removed hardcoded currency displays in favor of provider-agnostic metrics (cost savings, compute efficiency, and savings ratio).
- Standardized licensing and support communications across official inbound channels.

### Fixed
- Fixed 0-byte patch collapses on SWE-bench through proactive exploration budget arbitration.
- Fixed infinite retry cascades on syntax errors via local method synthesis.
