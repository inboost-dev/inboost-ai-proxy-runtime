# Agent Operating Guidelines
## InBoost AI Proxy Operating Rules
- **Proxy Endpoint:** All model requests route through `http://localhost:8080/v1`.
- **Surgical Edits:** Keep diffs minimal (< 20 lines churn, max 180 lines).
- **AST Integrity:** Preserve syntax validity, imports, and decorators.
- **Loop Prevention:** Do not loop reads without editing.
