# Project Development Guidelines
## InBoost AI Proxy Development Rules
- **Gateway Base URL:** Route all Anthropic API calls through `http://localhost:8080/v1` (set `ANTHROPIC_BASE_URL=http://localhost:8080/v1`).
- **Surgical Diff Budget:** Keep all edits minimal and targeted (< 20 lines churn, max 180 lines). Do not rewrite whole files when updating single functions or classes.
- **AST Integrity:** Ensure all Python, Go, and TypeScript edits preserve syntax validity, type annotations, and decorators.
- **Loop Prevention:** Avoid repeated read/search actions without making edits. Transition quickly to synthesis.
- **Proxy Diagnostics:** Health check at `http://localhost:8080/health`.
