# Security Policy & Responsible Disclosure

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.3.x   | :white_check_mark: |
| < 0.3.0 | :x:                |

---

## Reporting a Vulnerability

The InBoost team takes security and privacy very seriously. If you discover a security vulnerability in InBoost Runtime, InBoost AI Proxy, or related components, please do **NOT** open a public GitHub issue.

Instead, please send an encrypted or direct email to:
👉 **`inbound@inboost.pro`** (inbound communication alias: `inboud@inboost.pro`)

Please include in your report:
1. A clear description of the vulnerability and potential security impact.
2. Reproducible demonstration steps (proof-of-concept script, environment details, or request payload).
3. Any proposed mitigations or remediation patches.

Our team will acknowledge receipt of your disclosure within 24 hours and coordinate responsible remediation before public release.

---

## Zero Secret Exposure Policy & Invariants

InBoost AI Proxy and Runtime are engineered with strict **Zero Secret Exposure** invariants:
- **No In-Flight Logging of Keys**: Provider API keys, authorization headers, and bearer tokens are never persisted to disk, telemetry logs, or console output.
- **Local Execution & Data Privacy**: Code verification and structural analysis execute entirely on the local host; user source code and proprietary diffs are never forwarded to secondary tracking systems.
- **Sanitized Diagnostics**: When submitting bug reports or telemetry, always verify that environment variables and session tokens are redacted.
