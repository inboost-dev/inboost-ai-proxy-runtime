# Legal Notice, Disclaimers & Policies

This document sets forth the operational policies, disclaimers, trademark notices, and telemetry terms governing the use of **InBoost AI Proxy** and associated distribution artifacts.

For the complete binding legal agreement, please review the [InBoost Free Community Software License (with Automatic Pro Elevation)](LICENSE).

---

## 1. Discretionary Community Quota & Allocation Terms

The Community Developer tier (including the initial free phase and daily allowance) is provided on an as-is, promotional, and discretionary basis:

1. **Daily Task Quota:** Community users receive a recurring daily allowance of tasks (auto-replenishing at 00:00 UTC). Upon quota exhaustion, requests transition to an un-optimized pass-through bypass mode without session termination.
2. **Reservation of Rights:** InBoost Technologies reserves the right to modify, throttle, re-route, or discontinue community allocations at any time without prior notice or liability.
3. **No Commercial SLA on Community Tier:** Production environments requiring guaranteed throughput, strict contractual SLAs, dedicated capacity, and enterprise support must obtain an **InBoost Commercial Pro License** and configure Bring-Your-Own-Key (BYOK) mode.

---

## 2. Strict Opt-In Telemetry Policy (Privacy Covenant)

InBoost adheres to a strict developer-first privacy standard:

- **Disabled by Default:** Telemetry collection is **strictly disabled by default** and is never gathered without your explicit consent.
- **Explicit Activation Only:** Operational metrics are gathered only when an opt-in environment flag is explicitly defined (such as `INBOOST_TELEMETRY=1` or `INBOOST_COLLECT_TELEMETRY=1`).
- **Purpose of Use:** Any collected operational metrics are utilized solely and exclusively for product improvement purposes (such as refining sub-millisecond CPU routing heuristics, optimizing time-to-first-token latency, and diagnosing upstream error rates).
- **Zero Secret Exposure Guarantee:** User source code, file contents, code diffs, prompt text, and API keys are **never collected, logged, or retained under any circumstances**.

---

## 3. Third-Party Upstream Inference & Infrastructure Disclaimer

1. **Direct Upstream Execution:** Requests routed through InBoost AI Proxy are executed and processed directly by user-configured upstream model providers (e.g., Anthropic, OpenAI, SiliconFlow), third-party inference backends, or local runtimes (e.g., Ollama, vLLM) outside the control or ownership of InBoost Technologies.
2. **Zero Liability for Third-Party Outages:** InBoost Technologies disclaims all liability and assumes no responsibility for third-party hosting infrastructure, server availability, data retention policies of external hosts, latency spikes, or security policies of external model providers. All inference is consumed at your sole and exclusive risk.
3. **Bring-Your-Own-Key (BYOK) Responsibility:** You remain solely responsible for compliance with the terms of service, billing policies, and acceptable use guidelines of your respective upstream API providers.

---

## 4. Trademark & Brand Disclaimer (Nominative Fair Use)

All product names, logos, brands, trademarks, and registered trademarks cited in this repository, software, and documentation are the property of their respective owners.

All company, product, and service names used in this project (including, but not limited to, Anthropic, Claude, Claude Code, Cursor, OpenAI, ChatGPT, DeepSeek, SiliconFlow, OpenHands, Aider, Windsurf, Cline, vLLM, SGLang, Ollama, GitHub, and Apple) are used strictly for identification, compatibility, and descriptive purposes only (nominative fair use).

Use of these names, logos, and brands does not imply endorsement, affiliation, sponsorship, or certification by their respective holders.

---

## 5. Dispute Resolution & Forum Selection

Access to and use of the Software is conditioned upon acceptance of InBoost's exclusive right under Section 11 of the [LICENSE](LICENSE) to designate the dispute resolution forum. Any party that does not agree to these terms is not licensed and must cease all use immediately.

---

## 6. Third-Party Open-Source Software Notices & Licenses

InBoost AI Proxy and accompanying standalone binaries incorporate, link to, or bundle third-party open-source libraries under permissive licenses (including MIT, BSD 3-Clause, Apache 2.0, and PSFL).

All third-party components are strictly permissive and non-copyleft. In compliance with the licensing terms of each third-party project (including `agent-tool-parser`, `FastAPI`, `Uvicorn`, `HTTPX`, `Pydantic`, `PyYAML`, `Cryptography`, and `AnyIO`), full attribution, copyright notices, and license texts are documented in:
👉 **[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)**

---

## 7. Official Contacts & Inquiries

- Official Portal: [https://inboost.pro/ai-proxy](https://inboost.pro/ai-proxy)
- GitHub Repository: [https://github.com/inboost-dev/inboost-ai-proxy-runtime](https://github.com/inboost-dev/inboost-ai-proxy-runtime)
- General Inquiries & Legal Notices: `inbound@inboost.pro` or [GitHub Issues](https://github.com/inboost-dev/inboost-ai-proxy-runtime/issues)
