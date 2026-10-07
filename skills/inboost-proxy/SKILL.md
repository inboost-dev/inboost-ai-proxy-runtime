---
name: inboost-proxy
description: "InBoost AI Proxy integration skill for Claude Code, Cursor, Cline, OpenHands, and Antigravity. Directs coding assistants to proxy inference through http://localhost:8080/v1, enforces surgical diff budgets (<= 180 lines, prefer < 20 lines), leverages L0 CPU AST pre-validation, avoids repetitive file-reading loops, and monitors daily quotas."
category: tool-integration
risk: safe
tags: [inboost, proxy, router, ast, diff-budget, claude-code, cursor, openhands]
---

# InBoost AI Proxy Integration Skill

## Overview
This skill integrates your AI coding assistant (Claude Code, Cursor IDE, Cline, Roo Code, OpenHands, Antigravity) with the local **InBoost AI Proxy** runtime (`http://localhost:8080/v1`).

The proxy acts as an intelligent cognitive execution arbiter between your editor and upstream LLM providers (SiliconFlow, Anthropic, OpenAI):
- **High-Performance Dynamic Routing:** Automatically balances fast exploration models with deep reasoning models.
- **Surgical Diff Budget:** Rejects runaway edits (> 180 lines) and eliminates 0-byte surrender failures.
- **Deterministic AST Integrity:** Syntax pre-validation on local CPU before commits.
- **Loop Prevention:** Detects and interrupts repetitive file-reading loops.
- **Cache Hit Maximization:** Canonicalizes volatile tokens to increase prompt cache reuse.

---

## Operating Invariants for Coding Assistants

When this skill is active, assistants must strictly adhere to the following 6 rules:

### 1. Endpoint Configuration
- **Claude Code:** Ensure `ANTHROPIC_BASE_URL` is set to `http://localhost:8080` and `CLAUDE_CODE_AUTO_MODE_SERVER=0`.
- **Cursor IDE:** In *Settings -> Models -> OpenAI API*, set *Override Base URL* to `http://localhost:8080/v1`.
- **OpenHands / Aider:** Set `base_url = "http://localhost:8080/v1"`.

### 2. Targeted Exploration Discipline
- **Stack Trace & Symbol Priority:** Prioritize inspecting files, functions, or modules explicitly mentioned in error messages, stack traces, test outputs, or issue descriptions before searching the broader codebase.
- **Fast Transition to Modification:** Limit exploratory read/search operations to <= 3 steps. Once the relevant function or error location is identified, transition immediately to targeted code modifications.
- **Avoid Broad Scans:** Avoid blind whole-repository scans (`find .`, `grep -r`) when the fault location can be inferred directly from context or logs.

### 3. Surgical Diff Budgeting (DiffBudgetGate)
- Keep all modifications targeted and surgical (target < 20 lines churn, hard ceiling <= 180 lines).
- Never replace entire source files when editing specific functions or classes.
- The proxy automatically rejects diffs > 180 lines or empty 0-byte submissions.

### 4. Deterministic AST Integrity (ASTGuard)
- All Python, Go, and TypeScript/JavaScript patches undergo instant pre-commit syntax validation.
- Preserve all `@staticmethod`, `@classmethod`, decorators, indentation levels, and import statements.

### 5. Loop Prevention (LoopBreaker)
- Never read or search the same file more than 3 times without making an edit.
- If context is acquired, immediately transition to synthesis (`str_replace`, `write_file`, or editing).

### 6. Verification & Immediate Completion
- Immediately after applying a code change, inspect `git diff` or execute targeted reproducing tests to confirm accuracy.
- When the fix is verified and syntactically valid, finalize and submit the solution immediately without redundant exploratory steps.

---

## Quotas and Diagnostics
- **Free Community Tier:** 30 tasks per day (resets daily at 00:00 UTC).
- **Health Check:** `curl -s http://localhost:8080/health`
- **Session Telemetry:** `curl -s http://localhost:8080/v1/telemetry`
- **Documentation & Pro Upgrade:** https://github.com/inboost-dev/inboost-ai-proxy-runtime
