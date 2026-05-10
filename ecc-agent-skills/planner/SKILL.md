---
name: planner
description: Planning specialist skill adapted from ECC planner agent. Use for feature implementation planning, dependency sequencing, and risk-aware execution plans.
origin: ECC-agent-adapter
ecc_source_repo: affaan-m/everything-claude-code
ecc_source_path: agents/planner.md
ecc_source_commit: 0e9f613fd196f6d4157765b17d39c2c42ebbf564
---

# Planner

## When to Use

- Before implementing non-trivial features
- When a task spans multiple files or phases
- When ordering and dependencies are unclear

## Input Contract

- Feature goal and scope
- Existing constraints (architecture, policy, timelines if provided)
- Relevant artifact paths (PRD/design/capability docs)

## Workflow

1. Clarify objective, boundaries, and success criteria.
2. Identify impacted components and dependency order.
3. Produce phased implementation steps with concrete actions.
4. Call out risks, edge cases, and required validations.

## Output Contract

Return in this structure:

```text
STATUS: PASS | REQUEST_CHANGES | NOT_RUN | BLOCKED
SUMMARY: one-paragraph plan summary
PHASES:
- phase name + ordered steps
DEPENDENCIES:
- explicit prerequisite mapping
RISKS:
- risk + mitigation
BLOCKING_FINDINGS:
- empty or concrete blockers
```

Use `REQUEST_CHANGES` when input ambiguity prevents safe planning.
Use `BLOCKED` when required inputs/artifacts are unavailable.
