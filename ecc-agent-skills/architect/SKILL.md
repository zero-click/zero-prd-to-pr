---
name: architect
description: Architecture review and design skill adapted from ECC architect agent. Use for design validation, trade-off analysis, and system-level decisions.
origin: ECC-agent-adapter
ecc_source_repo: affaan-m/everything-claude-code
ecc_source_path: agents/architect.md
ecc_source_commit: 0e9f613fd196f6d4157765b17d39c2c42ebbf564
---

# Architect

## When to Use

- During feature design and design review gates
- When architecture trade-offs need explicit decisions
- Before implementation for cross-component changes

## Input Contract

- Design artifact path (required for review flows)
- Linked PRD/capability context
- Known constraints (security, scalability, performance, rollout)

## Workflow

1. Assess architecture fit with existing system constraints.
2. Validate interfaces, data implications, and failure paths.
3. Evaluate alternatives and trade-offs.
4. Return concrete changes required before coding.

## Output Contract

```text
STATUS: PASS | REQUEST_CHANGES | NOT_RUN | BLOCKED
SUMMARY: architecture decision summary
KEY_FINDINGS:
- mismatch/risk/decision items
TRADEOFFS:
- decision, pros, cons, alternatives
BLOCKING_FINDINGS:
- empty or concrete blockers
```

Use `REQUEST_CHANGES` if design is incomplete, inconsistent, or risky.
