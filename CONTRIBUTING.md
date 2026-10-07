# Contributing to InBoost Runtime

Thank you for your interest in contributing to the InBoost Runtime & Distribution ecosystem!

---

## 1. Code of Conduct & DCO

By contributing, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) and certify that your work complies with the [Developer Certificate of Origin 1.1](DCO.md).

All commits must include a Developer Certificate of Origin sign-off line:
```bash
git commit -s -m "feat(router): add adaptive timeout fallback for slow SLM endpoints"
```

---

## 2. Commit Message Standards

We strictly enforce **Conventional Commits**:
- `feat(...)`: New user-facing feature or enhancement.
- `fix(...)`: Bug fix.
- `docs(...)`: Documentation updates.
- `perf(...)`: Performance improvement.
- `refactor(...)`: Code refactoring without behavior change.
- `test(...)`: Adding or updating test suites.
- `ci(...)`: Build or CI/CD workflow changes.

---

## 3. Reporting Bugs & Asking Questions

- **Bug Reports**: Please open an issue using the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.yml).
- **Feature Requests**: Please use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.yml).
- **Security Invariant**: Never attach private tokens, API keys, passwords, or confidential code in bug reports. Use redacted identifiers (e.g., `<YOUR_API_KEY>`).

---

## 4. Release Asset & Binary Guidelines

- All distributed binaries and wheels in this repository must include valid SHA256 checksums in `checksums.txt`.
- Binaries must be built from tagged release sources using verified, reproducible toolchains.
- Never commit large uncompressed binaries directly into git history; use GitHub Release Assets or external mirrors as directed in `scripts/build_release_manifest.py`.

---

## 5. Inquiries & Community Support

All questions, contributor discussions, bug reports, and commercial inquiries must be submitted through:
- **Official Portal:** [https://inboost.pro/ai-proxy](https://inboost.pro/ai-proxy)
- **GitHub Issues:** [https://github.com/inboost-dev/inboost-ai-proxy-runtime/issues](https://github.com/inboost-dev/inboost-ai-proxy-runtime/issues)
- **Inbound Communications:** `inbound@inboost.pro` (alias: `inboud@inboost.pro`)
