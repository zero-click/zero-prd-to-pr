# Software Development Workflow

[English](./README.md) | [中文](./README.zh.md)

The engineering half of the pipeline. Takes the product design artifacts (PRD + roadmap + architecture) and turns them into a merged, production-ready PR through gated TDD and review.

Entry skill: **`woos-development-workflow`**.

## Quick Start

1. Make sure the product inputs exist: PRD, roadmap, architecture. Missing any = `BLOCKED`.
2. Hand the agent off to `woos-development-workflow`.
3. Mode is auto-selected from PRD scope and risk (Lite vs Standard). Each gate must PASS before the next starts.

## Pipeline

```
Product inputs (PRD + roadmap + architecture)
   │
   ▼  Bootstrap   woos-run-orchestrator → git-workflow
   ▼  Gate 0      Product Intake — validate inputs, record in run-manifest
   ▼  Gate 1      Feature Design                   woos-feature-design
   ▼  Gate 1R     Design Review (fresh context)    woos-design-review-gate
   ▼  Gate 2      Story Decomposition → plan.md    woos-story-decomposition
   ▼  Gate 3      Story Loop (per story in DAG order)
   │              ├─ 3.1 TDD             tdd-workflow
   │              ├─ 3.2 Implement       coding-standards
   │              └─ 3.3 Verify          verification-loop
   ▼  Gate 4      Executable Acceptance            woos-executable-acceptance-gate
   ▼  Gate 5      Deviation Control                woos-deviation-control-gate
   ▼  Gate 6      Requirement Traceability         (built-in)
   ▼  Gate 7      Code + Security Review           woos-code-review-gate
   ▼  Gate 8      PR Readiness                     woos-pr-readiness
   ▼  Post        Workflow Memory                  woos-workflow-memory
   ▼
PR created ✅

On unresolvable design issue → DCR → docs/feedback/<version>/<feature-id>-dcr-<NNN>.md
```

## Execution Modes

| Mode | When | Skipped gates |
|------|------|---------------|
| Lite | Low-risk, single small change, no arch impact | Gates 1, 1R, 2, 4, 5, 6 |
| Standard (default) | Anything from a product-design pipeline | none |

Mode is determined by PRD scope and risk, not by the developer.

## Gate-by-Gate

| Gate | Skill | What it produces |
|------|-------|------------------|
| 0 Product Intake | (built-in) | Validates PRD + roadmap + architecture; records paths in `run-manifest.yaml`. First run on a repo: invokes `codebase-onboarding`. |
| 1 Feature Design | `woos-feature-design` | `docs/engineering/<version>/<feature-id>-design.md`. References `api-design` / `database-migrations` / `deployment-patterns` when relevant. Baseline deviations captured via `architecture-decision-records`. |
| 1R Design Review | `woos-design-review-gate` | Independent architect review in fresh context; `PASS` / `REQUEST_CHANGES`. 2 failed rounds → `woos-human-handoff`. |
| 2 Story Decomposition | `woos-story-decomposition` (+ `woos-product-planner` review) | Single per-feature `docs/stories/<version>/<feature-id>/plan.md`: `ID \| AC \| Depends \| Diff Scope`. No per-story narrative documents. |
| 3 Story Loop | `tdd-workflow`, `coding-standards`, `verification-loop` | Per story (DAG order): RED→GREEN→REFACTOR → implement → verify. Conditional: `database-migrations`, `e2e-testing`, `browser-qa`. A blocked story does NOT block independent stories. |
| 4 Executable Acceptance | `woos-executable-acceptance-gate` | Every PRD AC mapped to an executable check. Missing automation = blocker. |
| 5 Deviation Control | `woos-deviation-control-gate` | Implementation vs PRD/architecture/design; unresolved deviations block. Intentional deviation requires ADR. |
| 6 Requirement Traceability | (built-in) | `docs/traceability/<version>/<feature-id>-traceability.md` table: PRD AC → design → code → test → status. Zero ❌ to pass. |
| 7 Code / Security Review | `woos-code-review-gate` → `woos-code-reviewer` (+ `woos-security-reviewer` when triggered, `woos-production-audit` when applicable) | Fresh-context review with knowledge injection (E1). Output is a structured findings table (E2). |
| 8 PR Readiness | `woos-pr-readiness` | Final check: tests green, lint clean, no orphan TODOs, traceability matrix attached. Creates the PR via `gh pr create`. |
| Post Workflow Memory | `woos-workflow-memory` | Persists failure/rework patterns and story-decomposition quality signals for future runs. |

## Story Plan (Gate 2)

Gate 2 emits one file per feature: `docs/stories/<version>/<feature-id>/plan.md`. A 4-column table is the whole product:

```markdown
| ID  | AC           | Depends | Diff Scope                              |
|-----|--------------|---------|-----------------------------------------|
| s01 | FR-1.a       | -       | store/persist.go, store/persist_test.go |
| s02 | FR-1.b       | s01     | store/persist.go, store/persist_test.go |
| s03 | FR-3.a       | s01     | store/lifecycle.go, store/lifecycle_test.go |
```

Why so thin: PRD AC is the spec, tests inside the diff scope are the verification, `git restore -- <diff_scope>` is the rollback. Story status and failure logs are runtime state in `run-manifest.yaml`. Sizing rule: 1 PRD AC per story (hard cap 3 strongly-coupled AC sharing test setup); no two unordered stories may share a file. See `woos-story-decomposition/SKILL.md` for the authoritative schema.

## Enforcement Rules

Three non-negotiable rules learned from production agent failures:

- **E1 Knowledge Injection** — before dispatching a review sub-agent, the orchestrator MUST inject the relevant skill's full content. A sub-agent with only a role name produces shallow output.
- **E2 Structured Review Output** — every review gate must emit a findings table (severity, category, finding, location, recommendation) + verdict + evidence. A bare "PASS" or "LGTM" is INVALID and triggers a rerun.
- **E3 Conditional Skill Activation** — conditional skills (`browser-qa`, `e2e-testing`, `database-migrations`, `security-review`, etc.) have concrete trigger rules. If the trigger fires, activation is mandatory — not a judgment call.

## Skill Map

**Local (`woos-*`):**
`woos-development-workflow` (entry), `woos-feature-design`, `woos-design-review-gate`, `woos-story-decomposition`, `woos-executable-acceptance-gate`, `woos-deviation-control-gate`, `woos-code-review-gate`, `woos-pr-readiness`, `woos-workflow-memory`, `woos-run-orchestrator`, `woos-failure-state-machine`, `woos-human-handoff`, `woos-review-context`, `woos-agent-decision`, `woos-systematic-debugging`, `woos-architect`, `woos-product-planner`, `woos-code-reviewer`, `woos-security-reviewer`, `woos-production-audit`.

**Imported (`skills/ecc/`):**
`git-workflow`, `tdd-workflow`, `coding-standards`, `verification-loop`, `api-design`, `browser-qa`, `e2e-testing`, `security-review`, `architecture-decision-records`, `database-migrations`, `deployment-patterns`, `codebase-onboarding`.

## DCR (Design Change Request)

When engineering hits a design issue it cannot resolve inside scope:

1. Write `docs/feedback/<version>/<feature-id>-dcr-<NNN>.md` (issue, impact, proposed fix, priority). `NNN` is zero-padded from `001`; never overwrite — always allocate the next free number.
2. Stop affected stories. Continue unaffected ones.
3. Product pipeline updates the PRD and re-issues. Engineering resumes from the affected gate.

## File Layout

```
<project-root>/
├── hep/
│   ├── runs/<run_id>/run-manifest.yaml      ← gate progress + runtime story state
│   └── review-context/<run_id>.yaml         ← cumulative cross-gate findings
└── docs/
    ├── product/<project>-roadmap.md         ← input
    ├── product/<project>-architecture.md    ← input
    ├── prd/<version>/<feature-id>.md        ← input
    ├── prd/<version>/<feature-id>-interface.md     ← optional (Strict)
    ├── design/<version>/<feature-id>-ui-brief.md   ← optional (when UI)
    ├── engineering/<version>/<feature-id>-design.md  ← Gate 1
    ├── stories/<version>/<feature-id>/plan.md       ← Gate 2
    ├── adr/                                  ← ADR captures
    ├── feedback/<version>/<feature-id>-dcr-<NNN>.md  ← DCR
    └── traceability/<version>/<feature-id>-traceability.md  ← Gate 6
```
