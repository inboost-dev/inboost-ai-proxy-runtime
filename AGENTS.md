# Agent Operating Guidelines
## InBoost AI Proxy Operating Rules
- **Proxy Endpoint:** All model requests route through `http://localhost:8080/v1`.
- **Surgical Edits:** Keep diffs minimal (< 20 lines churn, max 180 lines).
- **AST Integrity:** Preserve syntax validity, imports, and decorators.
- **Loop Prevention:** Do not loop reads without editing.

## Mandatory Local Acceleration & Zero-Noise Tooling
To eliminate context token bloat, prevent message rate limit exhaustion, and maintain sub-millisecond developer feedback loops, all AI assistants and coding agents MUST leverage the following local tools:
- **Structural Search & Refactoring (`ast-grep` / `sg`):** Invoke `ast-grep run --pattern '<pattern>' [path]` instead of blind grep to match syntax nodes without noise.
- **Sub-Millisecond Rust Linting (`ruff` & `biome`):** Run `ruff check [path]` (< 2 ms) for Python and `biome check [path]` (< 2 ms) for JS/TS before submitting patches.
- **Repository Architectural Mapping (`Graphify` & `RepoMap`):** Run `repomap [path]` to inspect class/function signatures without loading full file bodies; query `graphify-out/graph.json` or run `graphify query "<question>"` for multi-module architectures.
- **Runtime Test Offload (`InBoost Local`):** Run tests via `inboost-local run <command>` to crush failures (-95%) and localize AST repair ranges.
