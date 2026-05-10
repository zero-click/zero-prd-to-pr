---
name: woos-development-workflow
description: Skill-first development workflow for Hermes coding profile. Every gate binds to exactly one skill (local or ECC-imported) with a minimal contract.
version: 1.2.0
author: Hermes ECC Profile
license: MIT
metadata:
  hermes:
    tags: [development, workflow, ecc, skill-first, tdd, review, prd, design]
---

# Woosley Development Workflow (ECC + Hermes)

## Purpose

Use this workflow for non-trivial software work.  
Rule: every gate must invoke exactly one named skill, then satisfy that skill's minimal contract.

ECC-first rule (hard):

1. Prefer ECC skill first.
2. If ECC has no direct skill, use local wrapper skill that explicitly invokes ECC agents.
3. Do not replace an ECC reviewer with generic/self review.
4. If required ECC skill/agent is unavailable, return `BLOCKED` and stop.

## Git Branch/Worktree Policy (ECC-native)

Do not define custom git strategy rules here.

Use ECC skills directly:

- `git-workflow` for branch strategy, commit/PR flow, and merge/rebase conventions.
- `dmux-workflows` for multi-agent parallel execution, pane orchestration, and git worktree isolation.

Minimal contract:

1. Always invoke `git-workflow` before meaningful code changes.
2. Invoke `dmux-workflows` only when running parallel coding lanes.
3. If `dmux-workflows` is active, worktree-per-worker is required.

Core path:

```text
Research -> PRD Draft -> PRD Review -> Capability Contract -> Feature Design -> Design Review -> TDD -> Implement -> Verify -> Code/Security Review -> PR Readiness
```

## Skill Whitelist (local or ECC import only)

Only these skills are allowed in this workflow:

| Step | Skill | Source |
|---|---|---|
| Git Workflow | `git-workflow` | ECC |
| Research | `search-first` | ECC |
| Parallel Orchestration (when needed) | `dmux-workflows` | ECC |
| PRD Draft | `woos-prd-authoring` | local |
| PRD Review | `woos-prd-review-gate` | local |
| Capability Contract | `product-capability` | ECC |
| Feature Design | `woos-feature-design` | local |
| Design Review | `woos-design-review-gate` | local |
| TDD | `tdd-workflow` | ECC |
| Implement | `coding-standards` | ECC |
| Verify | `verification-loop` | ECC |
| Code/Security Review | `woos-code-review-gate` | local |
| PR Readiness | `woos-pr-readiness` | local |

If a required skill is unavailable, status is `BLOCKED` and the workflow stops.

Local wrapper intent:

- `woos-prd-review-gate` wraps ECC `planner` + `architect`
- `woos-feature-design` wraps ECC `architect` (and `planner` for complex scope)
- `woos-design-review-gate` wraps ECC `architect`
- `woos-code-review-gate` wraps ECC `code-reviewer` (+ `security-reviewer` when needed)
- `woos-pr-readiness` wraps ECC `verification-loop`

## Global Gate Status

- `NOT_RUN`: required skill was not invoked
- `BLOCKED`: required skill unavailable
- `REQUEST_CHANGES`: gate failed, revise and rerun same skill
- `PASS`: gate complete

Progression rule:

```text
NOT_RUN/BLOCKED/REQUEST_CHANGES -> PASS -> next gate
```

## Gate Definitions (skill + minimal contract)

### Gate 0 — Research
**Skill:** `search-first` (ECC)  
**Minimal contract:**

1. Reuse options are searched before net-new design.
2. Chosen direction is recorded with a short rationale.

### Gate 1 — PRD Draft
**Skill:** `woos-prd-authoring` (local)  
**Minimal contract:**

1. PRD artifact exists at `docs/prd/<feature>.md` (or repo convention).
2. Core sections and testable AC are present.

### Gate 1R — PRD Review
**Skill:** `woos-prd-review-gate` (local)  
**Minimal contract:**

1. Executes independent PRD review using ECC agents (`planner` + `architect`) via the local gate skill.
2. Returns `PASS` or `REQUEST_CHANGES` with concrete gaps.

### Gate 1.5 — Capability Contract
**Skill:** `product-capability` (ECC)  
**Minimal contract:**

1. Produces implementation-facing capability contract.
2. Captures constraints/invariants/interfaces/open questions.

### Gate 2 — Feature Design
**Skill:** `woos-feature-design` (local)  
**Minimal contract:**

1. Design artifact exists at `docs/design/<feature>.md` (or repo convention).
2. Covers architecture, data, interfaces, risk, rollout/rollback.

### Gate 2R — Design Review
**Skill:** `woos-design-review-gate` (local)  
**Minimal contract:**

1. Executes independent design review using ECC `architect` agent via local gate skill.
2. Returns `PASS` or `REQUEST_CHANGES`.

### Gate 3 — TDD
**Skill:** `tdd-workflow` (ECC)  
**Minimal contract:**

1. RED observed before implementation for behavior changes.
2. GREEN observed after implementation.

### Gate 4 — Implement
**Skill:** `coding-standards` (ECC)  
**Minimal contract:**

1. Changes are minimal, scoped, and convention-aligned.
2. No silent failures or unsafe shortcuts.

### Gate 5 — Verify
**Skill:** `verification-loop` (ECC)  
**Minimal contract:**

1. Relevant lint/test/type/build checks executed.
2. Verification status reported explicitly.

### Gate 6 — Code/Security Review
**Skill:** `woos-code-review-gate` (local)  
**Minimal contract:**

1. Runs ECC `code-reviewer`.
2. Runs ECC `security-reviewer` when scope is security-sensitive.
3. Returns `PASS` or `REQUEST_CHANGES`.

### Gate 7 — PR Readiness
**Skill:** `woos-pr-readiness` (local)  
**Minimal contract:**

1. Diff/status/review/verification readiness is checked.
2. Conventional commit + PR test plan readiness confirmed.

## Stop Conditions

Stop and surface blocker when:

- Required skill was not invoked (`NOT_RUN`)
- Required skill unavailable (`BLOCKED`)
- Gate returns `REQUEST_CHANGES`
- Ambiguity blocks acceptance criteria definition
