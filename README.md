<div align="center">

# InBoost AI Proxy

**A local inference proxy that makes AI coding agents faster, cheaper, and less prone to broken diffs.**

[![Official Portal](https://img.shields.io/badge/Portal-inboost.pro%2Fai--proxy-blue.svg)](https://inboost.pro/ai-proxy)
[![Access: Public Pilot](https://img.shields.io/badge/Access-Public%20Pilot-brightgreen.svg)](https://github.com/inboost-dev/inboost-ai-proxy-runtime)
[![License: InBoost Community / Pro](https://img.shields.io/badge/License-InBoost%20Community%20%2F%20Pro-blue.svg)](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/LICENSE)
[![Release](https://img.shields.io/badge/Release-v0.3.1-orange.svg)](https://github.com/inboost-dev/inboost-ai-proxy-runtime/releases)
[![Zero Secret Exposure](https://img.shields.io/badge/Security-Zero%20Secret%20Exposure-brightgreen.svg)](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/SECURITY.md)

</div>

---

InBoost AI Proxy runs locally as an L7 gateway between your AI coding assistant (Claude Code, Cursor, OpenHands, Cline, Aider) and your upstream LLM providers (Anthropic, OpenAI, SiliconFlow, or local models).

It automatically addresses common failure modes in autonomous coding workflows:
- **Patch Delivery:** Prevents failed or empty diff aborts (0-byte submissions).
- **Code Validity:** Verifies code structure before changes reach your repository.
- **Loop Protection:** Prevents agents from stalling in repetitive exploration cycles.
- **Cost Efficiency:** Optimizes model allocation between routine exploration and complex synthesis.

---

## ⚡ Quickstart

Get InBoost AI Proxy running with Claude Code in under a minute:

### 1. Start the proxy

Choose the installation method that fits your environment:

```bash
# Option A: Run instantly via npx (Zero install, Node.js 18+)
npx @inboost-pro/inboost-ai-proxy

# Option B: One-line native installer (Linux & macOS)
curl -fsSL https://raw.githubusercontent.com/inboost-dev/inboost-ai-proxy-runtime/main/install.sh | bash

# Option C: Global npm install
npm install -g @inboost-pro/inboost-ai-proxy
inboost-proxy start -d

# Option D: Python pip / pipx
pip install inboost-ai-proxy
inboost-proxy start -d
```

### 2. Point your coding assistant to InBoost

#### For Claude Code CLI
```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:8080"
export ANTHROPIC_API_KEY="inboost-local"
export CLAUDE_CODE_AUTO_MODE_SERVER=0

claude
```
*(Your real upstream provider key is stored securely in `~/.inboost/config.yaml`)*

#### For Cursor IDE
In **Settings → Models → OpenAI API**:
1. Enable **Override Base URL**
2. Set URL to: `http://127.0.0.1:8080/v1`

---

## ⚙️ Background Daemon & Service Management

Control the background daemon using standard CLI commands:

```bash
# Start proxy in background (detached mode)
inboost-proxy start -d

# Check daemon health, active models, and PID
inboost-proxy status

# Stop the proxy daemon
inboost-proxy stop

# Enable automatic start on login (Linux systemd --user / macOS launchd)
inboost-proxy service install

# Disable automatic start
inboost-proxy service uninstall
```

---

## 🏛️ Multi-Tier Compute Routing

InBoost dynamically allocates tasks across compute tiers to optimize turnaround speed and inference cost:

| Tier | Engine | Role |
| :--- | :--- | :--- |
| **⚡ L0 Local Engine** | Local Runtime | Protocol normalization and tool call parsing. |
| **🚀 L1 Fast Tier** | High-Speed Models | Codebase exploration, file inspections, and routine edits. |
| **🧠 L2 Deep Tier** | Frontier Reasoning Models | Complex multi-file architectural synthesis and debugging. |

---

## 🧩 Open-Source Dependency: `agent-tool-parser`

InBoost AI Proxy relies heavily on [`agent-tool-parser`](https://github.com/inboost-dev/agent-tool-parser) for extracting and normalizing tool calls from streaming model completions.

---

## 📊 Benchmark Results (SWE-bench Verified 30)

In empirical evaluations across 30 real-world repository tasks from the **SWE-bench Verified Cohort** comparing vanilla autonomous agents against agents running through InBoost AI Proxy:

> **Tip:** You can inspect or trigger the live A/B evaluation workflow anytime in GitHub Actions via [`.github/workflows/swebench-eval.yml`](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/.github/workflows/swebench-eval.yml).

### Performance, Cost & Reliability Scoreboard

| Metric | Baseline (Vanilla Agent) | With InBoost AI Proxy | Practical Value |
| :--- | :--- | :--- | :--- |
| **Patch Resolution Yield** | 19 / 30 (63.3%) | **30 / 30 (100.0%)** | **+36.7% reliable first-attempt patch delivery** |
| **Wasted Runs (0-Byte Aborts)** | 11 / 30 (36.7% wasted spend) | **0 / 30 (0.0% waste)** | **Eliminates wasted compute from empty submissions** |
| **Average Task Turnaround** | 248.5 s (4.1 min) | **111.1 s (1.8 min)** | **2.24x speedup in developer turnaround time** |
| **Batch Time (30 Tasks)** | 124.2 min (~2.1 hours) | **55.5 min (< 1 hour)** | **Over 1 hour saved per batch** |
| **Circular Loops Intercepted** | 0 (loops exhaust token limits) | **42 circular loops stopped** | **Recovers stalled runs and pushes agents to edit** |
| **Net API Spend Reduction** | Baseline cost (100%) | **~43.8% net savings** | **Reduces monthly model provider bills** |
| **Syntax Drift Rate** | Vulnerable to syntax drift | **0 syntax errors** | **Production-ready git diffs ready for review** |

---

## 🎯 Supported Agent Integrations

InBoost works out of the box with major developer assistants:

| Agent / Editor | Endpoint Configuration | Port |
| :--- | :--- | :--- |
| **Claude Code CLI** | `export ANTHROPIC_BASE_URL="http://127.0.0.1:8080"`<br>`export CLAUDE_CODE_AUTO_MODE_SERVER=0` | `8080` |
| **Cursor IDE** | Settings → Models → OpenAI API: set Override Base URL to `http://127.0.0.1:8080/v1` | `8080` |
| **OpenHands** | `LLM_BASE_URL="http://127.0.0.1:8080/v1"` | `8080` |
| **Aider** | `OPENAI_API_BASE="http://127.0.0.1:8080/v1"` | `8080` |
| **Cline / Roo Code** | Base URL: `http://127.0.0.1:8080/v1` | `8080` |

📖 For step-by-step guides, see [docs/THIRD_PARTY_AGENT_INTEGRATION_GUIDE.md](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/docs/THIRD_PARTY_AGENT_INTEGRATION_GUIDE.md).

---

## 💎 Community Edition & Commercial Licensing

InBoost is distributed under an accessible developer model:

| Tier | Task Allowance | Details |
| :--- | :--- | :--- |
| **Free Developer Phase** | Tasks 1 – 10 | 100% free, quiet developer experience. |
| **Sponsored Free Phase** | Tasks 11 – 30 | Full optimization with educational HUD showing savings and cycles prevented. |
| **Daily Quota** | 30 tasks / day | Replenishes daily at 00:00 UTC. |
| **Post-Quota Behavior** | Tasks > 30 | Graceful pass-through forwarding (requests continue without optimization). |
| **InBoost Pro** | Unlimited | Commercial license with zero notices, private throughput, and enterprise SLA. |

> **Note:** Community task allowances, opt-in telemetry terms, and third-party provider policies are detailed in [LEGAL.md](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/LEGAL.md) and [LICENSE](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/LICENSE). Telemetry collection is **strictly disabled by default**, and user code or prompt text is never collected.

To upgrade or obtain an enterprise license:  
👉 **[https://inboost.pro/ai-proxy](https://inboost.pro/ai-proxy)** | Contact: `inbound@inboost.pro`

---

## 🐛 Bug Reports & Issue Conventions

When opening an issue, please use one of our structured templates and title prefixes:

| Prefix | Category | Example |
| :--- | :--- | :--- |
| **`[bug]`** | Bugs, crashes, or provider timeouts | `[bug]: Claude Code hangs on 0-byte diff rejection` |
| **`[feature request]`** | New adapters or CLI flags | `[feature request]: Add streaming support for vLLM` |
| **`[license]`** | Commercial license & pilot inquiries | `[license]: Requesting 60-day pilot extension` |
| **`[other]`** | General questions and feedback | `[other]: Question regarding cache alignment behavior` |

### Security Invariant
When posting logs or terminal outputs:
- **Never** include provider API keys (`sk-...`, Bearer tokens).
- **Never** include proprietary source code.
- Authorization headers are automatically masked in proxy logs.

---

## 📦 Binary Releases & Verification

Standalone native binaries and release packages are published on the [Releases](https://github.com/inboost-dev/inboost-ai-proxy-runtime/releases) page:

* 🍏 **macOS Apple Silicon (M1-M4):** [`inboost-proxy-darwin-arm64`](https://github.com/inboost-dev/inboost-ai-proxy-runtime/releases/latest/download/inboost-proxy-darwin-arm64)
* 🍏 **macOS Intel (x86_64):** [`inboost-proxy-darwin-x86_64`](https://github.com/inboost-dev/inboost-ai-proxy-runtime/releases/latest/download/inboost-proxy-darwin-x86_64)
* 🐧 **Linux (x86_64):** [`inboost-proxy-linux-x86_64`](https://github.com/inboost-dev/inboost-ai-proxy-runtime/releases/latest/download/inboost-proxy-linux-x86_64)
* 🐍 **Python Wheels (PyPI):** `inboost_ai_proxy` and `inboost_proxy` (`cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`)
* 📦 **npm Tarball:** `inboost-ai-proxy-0.3.1.tgz`

To verify artifact integrity using SHA-256 hashes:
```bash
python3 scripts/verify_release.py --checksums dist/checksums.txt
```

---

## 🤝 Contributing

We welcome contributions, bug reports, and provider adapters.  
Please review our [CONTRIBUTING.md](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/CONTRIBUTING.md) guide and ensure commits include DCO 1.1 sign-off (`git commit -s`).

---

## 📄 License & Legal Policies

- **Software License:** [InBoost Free Community Software License v1.1](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/LICENSE) (with Automatic Pro Elevation)
- **Legal Policies & Disclaimers:** [LEGAL.md](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/LEGAL.md) (Terms of Use, Telemetry Policy & Trademark Disclaimers)
- **Third-Party Open-Source Notices:** [THIRD_PARTY_NOTICES.md](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/THIRD_PARTY_NOTICES.md) (Permissive Open-Source Attributions & Licenses)
- **Security Policy:** [SECURITY.md](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/SECURITY.md)
- **Code of Conduct:** [CODE_OF_CONDUCT.md](https://github.com/inboost-dev/inboost-ai-proxy-runtime/blob/main/CODE_OF_CONDUCT.md)
- **Official Portal:** [https://inboost.pro/ai-proxy](https://inboost.pro/ai-proxy)
- **Support & Inquiries:** [GitHub Issues](https://github.com/inboost-dev/inboost-ai-proxy-runtime/issues) or `inbound@inboost.pro`
