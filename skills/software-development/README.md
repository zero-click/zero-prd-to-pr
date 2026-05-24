# Software Development Workflow

A gated engineering workflow for AI coding agents. Receives a build handoff from the product design pipeline, decomposes into stories, and delivers a production-ready PR through TDD, review gates, and requirement traceability.

## Purpose

This is **Stage 3** of the idea-to-delivery pipeline. It ensures:

- Engineering receives a fully-defined handoff (no product-phase work here)
- Work is decomposed into independent, verifiable stories
- Every story is implemented via TDD (RED → GREEN → REFACTOR)
- Requirements are traced end-to-end: PRD → design → code → test
- Design issues flow back to product via DCR (Design Change Request)

## Quick Start

1. Ensure a build handoff exists at `docs/handoff/<version>/<feature>.md`
2. The agent activates `woos-development-workflow` (entry point skill)
3. The workflow auto-selects Lite/Standard/Strict based on handoff complexity
4. Follow the gated flow — each gate must PASS before the next begins

**Prerequisite:** Product design pipeline must have completed. No handoff = BLOCKED.

## Workflow Flowchart

```
                     ┌───────────────────────┐
                     │  Build Handoff        │
                     │  (from product stage) │
                     └───────────┬───────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Bootstrap                   │
                  │  Run Orchestrator + Git      │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 0: Handoff Intake      │
                  │  Validate handoff, record    │
                  │  version in run-manifest     │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 1: Feature Design      │
                  │  Technical design artifact   │
                  │  (architecture, data, API)   │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 1R: Design Review      │
                  │  Independent architect       │
                  │  review (PASS/REQUEST_CHANGES)│
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 2: Story Decomposition │
                  │  Break handoff into 3-8      │
                  │  independent stories (DAG)   │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 3: Story Execution     │
                  │  Loop (per story):           │
                  │                              │
                  │  ┌────────────────────────┐  │
                  │  │ 3.1 TDD (RED→GREEN)   │  │
                  │  │ 3.2 Implement          │  │
                  │  │ 3.3 Verify (test+lint) │  │
                  │  │ 3.4 Story AC Gate      │  │
                  │  └─────────┬──────────────┘  │
                  │            │                  │
                  │    PASS → next story          │
                  │    FAIL 3x → mark blocked     │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 4: Executable          │
                  │  Acceptance                  │
                  │  All AC → executable checks  │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 5: Deviation Control   │
                  │  Implementation vs handoff   │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 6: Requirement         │
                  │  Traceability                │
                  │  PRD → design → code → test │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 7: Code/Security       │
                  │  Review                      │
                  │  Fresh context, no self-review│
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Gate 8: PR Readiness        │
                  │  Traceability matrix + PR    │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  Workflow Memory Update      │
                  │  Capture patterns for reuse  │
                  └──────────────┬──────────────┘
                                 │
                      ┌──────────▼──────────┐
                      │    PR Created ✅    │
                      └─────────────────────┘

  On design issue at any gate:
  ┌─────────────────────────────────────────┐
  │  DCR → docs/feedback/<feature>-dcr.md   │
  │  → back to product pipeline for fix     │
  └─────────────────────────────────────────┘
```

## Gate Breakdown

### Gate 0 — Handoff Intake

**What:** Validate the build handoff from product pipeline.

- Confirm file exists at `docs/handoff/<version>/<feature>.md`
- Verify required sections: Mission, Requirements, AC, User Flows, Build Tasks, Verification Plan
- Record handoff version in run-manifest for traceability
- If handoff missing → BLOCKED, redirect to product pipeline

### Gate 1 — Feature Design

**What:** Produce the technical design artifact.

- **Skill:** `woos-feature-design`
- Output: `docs/design/<feature>.md`
- Covers: architecture, data model, interfaces, risk, rollout/rollback
- Baseline/deviation fields must be complete
- If Strict mode + API endpoints: triggers API Design Review (`api-design`)

### Gate 1R — Design Review

**What:** Independent review of the design.

- **Skill:** `woos-design-review-gate`
- Dispatches `architect` in fresh context (no self-review)
- Uses `woos-review-context` for cumulative findings
- Escalates to `woos-human-handoff` after 3 failed rounds

### Gate 2 — Story Decomposition

**What:** Break the handoff into independent, verifiable stories.

- Built-in orchestrator procedure (no separate skill)
- Each story covers 1–3 related Build Tasks
- Stories form a DAG (dependency order)
- Output: `.hep/runs/<run_id>/stories/story-NNN.md`
- Target: 3–8 stories per feature

### Gate 3 — Story Execution Loop

**What:** Execute each story with TDD and verification.

Per story (in dependency order):

| Sub-step | Skill | What |
|----------|-------|------|
| 3.1 TDD | `tdd-workflow` | RED → GREEN → REFACTOR |
| 3.2 Implement | `coding-standards` | Minimal, scoped, convention-aligned |
| 3.3 Verify | `verification-loop` | Tests + lint + type check |
| 3.4 Story AC | built-in | Per-story acceptance check |

**Failure isolation:** A blocked story does NOT block independent stories. Blocked stories retry after others complete; if still stuck → DCR.

### Gate 4 — Executable Acceptance

**What:** Full-feature acceptance check after all stories complete.

- **Skill:** `woos-executable-acceptance-gate`
- Maps ALL handoff AC to executable checks
- Missing automation = blocker
- PASS → proceed. REQUEST_CHANGES → back to Gate 3.

### Gate 5 — Deviation Control

**What:** Compare implementation against handoff and design.

- **Skill:** `woos-deviation-control-gate`
- Unresolved deviations block progression
- Intentional deviations require updated artifacts + rationale

### Gate 6 — Requirement Traceability

**What:** Trace from PRD through design to code and tests.

- Built-in procedure (reads PRD + design + implementation)
- Produces traceability table: `PRD AC → Design Spec → Code → Test → Status`
- Classifications: ✅ Aligned, ⚠️ Deviated (with rationale), ❌ Missing, 🆕 Added
- Output: `docs/handoff/<feature>-traceability.md`
- Zero ❌ required for PASS

### Gate 7 — Code/Security Review

**What:** Independent code review in fresh context.

- **Skill:** `woos-code-review-gate`
- Dispatches `code-reviewer` (+ `security-reviewer` if sensitive)
- If Strict: also checks architecture conformance
- Uses `woos-agent-decision` for reviewer conflicts
- 3 rounds without convergence → `woos-human-handoff`

### Gate 8 — PR Readiness

**What:** Final verification and PR creation.

- **Skill:** `woos-pr-readiness`
- All tests pass, lint clean, no unlinked TODOs
- Traceability matrix (requirement → test → code)
- Conventional commit messages
- Creates PR via `gh pr create`

### Post — Workflow Memory

**What:** Capture learnings for future runs.

- **Skill:** `woos-workflow-memory`
- Records: failures, rework causes, story decomposition quality, DCR outcomes
- Persists reusable guidance

## Three Execution Modes

| Mode | When | Gates | Story Loop |
|------|------|-------|------------|
| **Lite** | Low-risk, limited scope, no arch changes | Handoff → Implement → Verify → Review → PR | No decomposition |
| **Standard** | Multi-file, moderate risk (default) | All 9 gates | Full story loop |
| **Strict** | Security-sensitive, high uncertainty | All + API Review + Browser QA + Arch Conformance | Full story loop |

**Mode is determined by handoff complexity**, not chosen manually.

## DCR (Design Change Request)

When engineering discovers a design issue that can't be resolved within scope:

1. Write `docs/feedback/<feature>-dcr.md` (issue, impact, proposed fix, priority)
2. Stop work on affected stories
3. Continue with unaffected stories
4. Product pipeline receives DCR, fixes, and re-issues updated handoff

## Failure Handling

| Situation | Action |
|-----------|--------|
| Handoff missing | BLOCKED → redirect to product pipeline |
| Single story fails 3× | Mark blocked, continue others |
| Build/test fails 2× | `woos-systematic-debugging` |
| Review fails 3× | `woos-human-handoff` escalation |
| Design issue found | DCR → back to product |
| Overall timeout | `woos-failure-state-machine` (retry → degrade → escalate) |
| All stories blocked | `woos-human-handoff` — fundamental design issue |

## Skill Map

### Local Skills (workflow gates)

| Skill | Role |
|-------|------|
| `woos-development-workflow` | **Entry point** — orchestrator, gate progression |
| `woos-feature-design` | Gate 1 — technical design artifact |
| `woos-design-review-gate` | Gate 1R — independent design review |
| `woos-executable-acceptance-gate` | Gate 4 — machine-checkable done criteria |
| `woos-deviation-control-gate` | Gate 5 — implementation-vs-spec drift blocking |
| `woos-code-review-gate` | Gate 7 — independent code/security review |
| `woos-pr-readiness` | Gate 8 — PR creation and verification |
| `woos-workflow-memory` | Post — persistent pattern capture |
| `woos-run-orchestrator` | Infrastructure — run queue, concurrency, timeout |
| `woos-failure-state-machine` | Infrastructure — retry/degrade/escalation transitions |
| `woos-human-handoff` | Infrastructure — escalation and recovery |
| `woos-review-context` | Infrastructure — cumulative cross-gate findings |
| `woos-agent-decision` | Infrastructure — reviewer conflict resolution |
| `woos-systematic-debugging` | Infrastructure — structured debugging on repeated failures |
| `woos-setup-rules` | Utility — project rule routing setup |

### Imported Skills (from ECC)

| Skill | Gate | Role |
|-------|------|------|
| `git-workflow` | Bootstrap | Branch strategy, commit/PR flow |
| `tdd-workflow` | Gate 3.1 | RED → GREEN → REFACTOR methodology |
| `coding-standards` | Gate 3.2 | Code quality and convention enforcement |
| `verification-loop` | Gate 3.3 | Lint/test/type/build verification |
| `api-design` | Gate 1 (conditional) | REST/GraphQL design patterns |
| `browser-qa` | Gate 3 (conditional) | UI smoke test, visual regression |
| `e2e-testing` | Gate 3 (conditional) | Playwright E2E patterns, Page Object Model |
| `security-review` | Gate 7 | Security checklist: auth, input, secrets, API, payments |
| `architecture-decision-records` | Gate 1 + cross-gate | Structured ADR capture for deviations |
| `database-migrations` | Gate 3 (conditional) | Zero-downtime schema changes, rollback strategies |
| `deployment-patterns` | Gate 1, Gate 8 | CI/CD, Docker, rollback, production readiness |
| `production-audit` | Gate 7 (conditional) | Pre-merge production readiness audit |
| `codebase-onboarding` | Gate 0 (first run) | Codebase analysis and onboarding guide |
| `search-first` | Any gate | Quick research and reference lookup |
| `deep-research` | Any gate | Deep research when needed |
| `dmux-workflows` | Gate 3 (parallel) | Parallel coding lanes via worktrees |

## Key Design Principles

1. **Handoff-first** — no product-phase work here; handoff is the input contract
2. **Story-based decomposition** — large features broken into independently verifiable units
3. **TDD per story** — RED/GREEN/REFACTOR is not optional
4. **Failure isolation** — blocked stories don't cascade; independent work continues
5. **End-to-end traceability** — PRD → design → code → test chain is verified
6. **Bidirectional feedback** — DCR flows back to product when design issues are found
7. **Fresh-context reviews** — no self-review; dispatched in clean sub-agent context
8. **Baseline-first governance** — deviations require ADR + approval

## File Layout

```
<project-root>/
├── .hep/
│   ├── runs/<run_id>/
│   │   ├── run-manifest.yaml          ← gate progress tracking
│   │   └── stories/
│   │       ├── story-001.md           ← generated stories
│   │       └── ...
│   └── review-context/<run_id>.yaml   ← cumulative findings
├── docs/
│   ├── handoff/<version>/<feature>.md ← INPUT (from product)
│   ├── prd/<feature>.md               ← read for traceability
│   ├── design/<feature>.md            ← Gate 1 output
│   ├── feedback/<feature>-dcr.md      ← DCR output (back to product)
│   └── handoff/<feature>-traceability.md ← Gate 6 output
└── (implementation files)
```
