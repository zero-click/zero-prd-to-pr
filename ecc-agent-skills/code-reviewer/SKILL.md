---
name: code-reviewer
description: Independent code quality and correctness review skill adapted from ECC code-reviewer agent.
origin: ECC-agent-adapter
ecc_source_repo: affaan-m/everything-claude-code
ecc_source_path: agents/code-reviewer.md
ecc_source_commit: 48b883d7412914b04c8b185d9a82685b105d1734
---

# Code Reviewer

## When to Use

- After any code change and before PR readiness
- When a gate requires independent review findings

## Input Contract

- Current diff or changed files
- Linked context artifacts (PRD/design/capability) when relevant

## Workflow

1. Inspect changed scope and surrounding code context.
2. Review for correctness, reliability, security impact, and maintainability.
3. Prioritize real defects over style noise.
4. Consolidate findings into actionable items.

## Output Contract

```text
STATUS: PASS | REQUEST_CHANGES | NOT_RUN | BLOCKED
SUMMARY: review verdict
BLOCKING_FINDINGS:
- concrete defects requiring fix
NON_BLOCKING_FINDINGS:
- improvements/suggestions
```

Rules:

- `PASS` only when no blocking findings remain.
- `REQUEST_CHANGES` when blocking findings exist.
