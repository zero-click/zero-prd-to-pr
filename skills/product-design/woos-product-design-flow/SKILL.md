---
name: woos-product-design-flow
description: "Stage 2 orchestrator: take a version from the product roadmap and produce PRD + UI direction + build handoff. Uses sub-agents for creative/review work and direct script-assisted execution for mechanical checks."
version: 4.1.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, design, prd, handoff, review-gate, ui, orchestrator]
    stage: 2
    flow: woos-idea-to-delivery
---

# Product Design Flow (Orchestrator)

> **🚨 STOP. Read this section FIRST. It overrides any instinct to use the same execution mode for every step.**
>
> You are an ORCHESTRATOR. You dispatch sub-agents for creative authoring and independent review steps.
> You execute bounded direct steps yourself when they are deterministic, checklist-driven, or script-assisted.
> You do NOT turn every step into a sub-agent.
>
> Before EVERY step: output a Pre-flight block (see below). No pre-flight = invalid execution.

## ⛔ Enforcement Rules (NON-NEGOTIABLE)

These rules prevent the orchestrator from cutting corners. Violating any of them makes the entire flow invalid.

### P0: Pre-flight Checkpoint (MANDATORY — NEW)

Before executing ANY step, you MUST output this block in the conversation:

```
┌─────────────────────────────────────────────────────┐
│ 🛫 PRE-FLIGHT: Step <N> — <Name>                    │
├─────────────────────────────────────────────────────┤
│ Persona:    <file path or "none"> → reading...      │
│ Knowledge:  <file path(s) or "none"> → reading...   │
│ Template:   <file path or "none">                   │
│ Execution:  <sub-agent | direct | script-assisted>  │
│ Input:      <file path(s)>                          │
│ Output:     <file path>                             │
├─────────────────────────────────────────────────────┤
│ ✅ Persona loaded: <line count> lines               │
│ ✅ Knowledge loaded: <line count> lines             │
│ ✅ Template loaded: <line count> lines / N/A        │
├─────────────────────────────────────────────────────┤
│ Executing declared path...                          │
└─────────────────────────────────────────────────────┘
```

**Rules:**
- If you cannot produce this block → you have NOT read the files → STOP and read them
- The line counts prove you actually read the files (not faking it)
- After this block, the NEXT action must be executing the declared path: either dispatching the named sub-agent or running the direct/script-assisted step
- Direct steps must stay bounded to ranking, extraction, comparison, or checklist output. If you start re-authoring PRD/UI/handoff content, STOP.

### P1: Orchestrator Does NOT Create Creative Artifacts

You MUST NOT write requirements, PRDs, UI briefs, review verdicts, or handoff content yourself. Those artifacts belong to sub-agents or independent reviewers.

The orchestrator MAY directly execute only bounded steps that do not benefit from context isolation:
- Step 1 (scope selection)
- Step 3 (priority ranking)
- Step 7 (analyze gate)
- Step 9 (readiness check)
- Step 10 (integration gate)

**Self-check:** If you are writing new product prose beyond a ranking/checklist/comparison report, you are doing the sub-agent's job. Stop and dispatch instead.

### P2: No Step Merging

Each step produces its own output file. You MUST NOT combine steps (e.g., writing requirements + PRD in one pass). Each step uses one declared execution path and one output.

### P3: Output Validation Gate

After EVERY step, before advancing to the next, verify:
1. Output file EXISTS at the declared path
2. Output file contains ALL required sections (check H2 headings)
3. If validation fails → rerun the declared execution path, do NOT proceed

**Required sections by step:**

| Step | Required H2 Sections |
|------|---------------------|
| Step 2 (Requirements) | `## Problem Statement`, `## Goals`, `## User Stories`, `## Non-Goals`, `## Constraints`, `## Risks & Unknowns` |
| Step 4 (PRD) | `## Background`, `## User Personas`, `## Functional Requirements`, `## Non-Functional Requirements`, `## User Flows`, `## Edge Cases`, `## Non-Goals`, `## Success Metrics` |
| Step 9 (Readiness) | `## Checklist`, `## Verdict` |

### P4: Review Prompt Must Include Full Checklist

When dispatching a review sub-agent, include the COMPLETE checklist table in the prompt. The reviewer must check ALL criteria, not just "look for issues."

```
You are reviewing: [file path]
Check EVERY row. For EACH row, state ✅ or ❌ with specific finding.
Do NOT skip rows. Do NOT give blanket passes.
[paste full checklist table]
If any ❌ → result is REQUEST_CHANGES.
```

### P5: No Silent Step Skipping

If a step fails → FIX and retry, do NOT skip. Legitimately skippable steps:
- Step 6 (UI Brief) — only if user confirms "no UI"
- Step 10 (Integration) — only if single feature

### P6: Review Cannot Self-Validate

The same agent that authored a document MUST NOT review it. Reviews always use a fresh sub-agent dispatch with independent context.

---

## Purpose

Transform one version from the product roadmap into a build-ready product handoff. This is **Stage 2** of the woos-idea-to-delivery flow. Run once per version.

Focus: define WHAT to build and WHY. Technical architecture (HOW) is engineering's job.

## Project Root Requirement

All file paths (`docs/`) are relative to a **project root directory** which MUST be a git repository.

## When to Use

- User says "start V1" / "design this feature" / "ready to build X"
- Product roadmap exists and a version has been selected

## Prerequisites

- `docs/product/<project>-roadmap.md` exists (from Stage 1)
- **🚦 Human Approval Gate has passed** — user has reviewed full roadmap + architecture and explicitly said "start PRD" or equivalent. If you're invoking this skill and the user hasn't approved yet, STOP and go back to present the files.

## Modes

| Mode | When | Steps | Reviews |
|------|------|-------|---------|
| **Lite** | Small scope, obvious, 1-2 days work | Mission → Tasks → AC → Handoff | None |
| **Standard** | Single feature, moderate complexity | Requirements → PRD → PRD Review → Handoff | 1 (PRD Review) |
| **Strict** | Multi-feature version, high uncertainty, UX-heavy | Full pipeline: Priority → PRD → Review → UI → Review → Analyze → Handoff → Integration | All gates |

**How to choose:**
- Is it a one-liner change or tiny feature? → **Lite**
- Is it a single feature with clear scope? → **Standard**
- Is it a full version release with multiple features? → **Strict**

---

## Steps — Strict Mode

The orchestrator runs **per feature** in a loop:

```
Step 1: Select Version → extract feature list
  → For each feature:
      Steps 2–9 (Requirements → Readiness)
  → After ALL features pass Step 9:
      Step 10: Version Integration Gate
```

### Step 1: Select Version Scope

| | |
|---|---|
| **Sub-agent** | ❌ (orchestrator does this directly) |
| **Input** | `docs/product/<project>-roadmap.md` |
| **Output** | _(confirmed version name — stored in run-manifest)_ |

Read roadmap, extract target version. Confirm with user:
- Feature list and boundaries
- Non-goals
- Success metrics

---

### Step 2: Requirement Contract

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/persona-pm.md` |
| **Knowledge** | `references/framework-prd.md` |
| **Template** | `templates/requirements-template.md` |
| **Input** | `docs/product/<project>-roadmap.md` § target version |
| **Output** | `docs/prd/<version>/<feature>-requirements.md` |

Produce structured requirements following the template. Mark uncertain items with `[NEEDS CLARIFICATION: ...]`.
- Goals and constraints
- Acceptance criteria (machine-checkable where possible)
- Non-goals
- Risk assumptions and unknowns

**⚠️ This step MUST produce a separate file.** Do NOT fold requirements into the PRD. The requirements file is the input to Step 3 (Priority Ranking) which appends to it.

---

### Step 3: Priority Ranking

| | |
|---|---|
| **Sub-agent** | ❌ (orchestrator does this directly) |
| **Persona** | `references/persona-pm.md` (read directly; no separate dispatch) |
| **Knowledge** | `references/framework-prd.md` |
| **Execution** | Direct skill step — append only `## Priority Ranking` to the existing requirements file |
| **Input** | `docs/prd/<version>/<feature>-requirements.md` |
| **Output** | `docs/prd/<version>/<feature>-requirements.md` → appends `## Priority Ranking` |

Do this in the current feature context. Do NOT spawn a fresh PM sub-agent just to reread the same requirements file.

Rank requirements by priority using one framework:

| Framework | When | How |
|-----------|------|-----|
| MoSCoW | Small scope, clear stakeholders | Must / Should / Could / Won't |
| RICE | Data-available, competing features | Reach × Impact × Confidence ÷ Effort |
| Kano | UX-heavy, user delight matters | Must-have / Performance / Delighter |
| Story Mapping | Complex flows | Backbone → Walking Skeleton → Nice-to-have |

**Must produce:**
1. Ranked list with priority tier (P0 must-ship, P1 should-ship, P2 nice-to-have)
2. Trade-off rationale for P1/P2 items
3. Cut-line: what's IN vs DEFERRED

---

### Step 4: PRD Authoring

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/persona-pm.md` |
| **Knowledge** | `references/framework-prd.md` + `references/template-prd-template.md` |
| **Template** | `templates/prd-template.md` |
| **Input** | `docs/prd/<version>/<feature>-requirements.md` (including Priority Ranking) |
| **Output** | `docs/prd/<version>/<feature>.md` |

Write full PRD following the template. Mark uncertain items with `[NEEDS CLARIFICATION: ...]`.
P0 requirements get full detail, P2 gets brief mention:
- User stories with acceptance criteria
- Functional and non-functional requirements
- Edge cases and error handling
- User flows (text-based)

**⚠️ Template is mandatory, not advisory.** After authoring, the orchestrator runs P3 structural check. If ANY template section is missing, this step is re-dispatched until all sections are present.

---

### Step 5: PRD Review Gate

| | |
|---|---|
| **Sub-agent** | ✅ (independent reviewer) |
| **Persona** | `references/persona-prd-validator.md` |
| **Knowledge** | `references/template-prd-validation-checklist.md` |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/prd/<version>/<feature>-requirements.md` + `docs/product/<project>-architecture.md` |
| **Output** | `docs/reviews/<version>/<feature>-prd-review-rN.md` |

**⚠️ PRD Review has TWO phases (both mandatory):**

**Phase A — Structural Completeness (P3 enforcement):**

Before content review, verify ALL required sections exist per template:
- `## Background` ✅/❌
- `## User Personas` ✅/❌
- `## Functional Requirements` (with `**User value:**` per FR) ✅/❌
- `## Non-Functional Requirements` ✅/❌
- `## User Flows` (at least 1 flow diagram) ✅/❌
- `## Edge Cases` (table format, ≥ 4 cases) ✅/❌
- `## Non-Goals` ✅/❌
- `## Success Metrics` (≥ 2 measurable metrics) ✅/❌

If ANY section is missing → **immediate REQUEST_CHANGES** without proceeding to Phase B.

**Phase B — Content Quality Checklist:**

| # | Criterion | Fix Hint |
|---|-----------|----------|
| P1 | Value-traced | Add "User value: …" line linking each requirement to a user outcome |
| P2 | AC testable | Rewrite as "Given X, When Y, Then Z" or add measurable threshold |
| P3 | Non-goals effective | Make specific enough to reject a concrete feature request |
| P4 | Edge cases covered | Add "What if…" for: empty state, error, timeout, concurrent access |
| P5 | Real user behavior | Replace developer-centric language with user-observable actions |
| P6 | No internal contradictions | Identify conflicts within this PRD; resolve or move to non-goals |
| P7 | Architecture reference check | Cross-check constants, state definitions, and API routes against `docs/product/<project>-architecture.md`. If PRD diverges from architecture, **annotate the divergence** (do NOT treat as failure). Divergences are surfaced to the human reviewer for final decision. |

**⚠️ P7 special rule — Architecture is a REFERENCE, not a constraint:**

Architecture.md (from Discovery) represents the architect's best recommendation at that point. During Product Design, new information may surface that makes divergence appropriate. P7 violations do NOT count toward PASS/FAIL. Instead:
- ✅ = PRD aligns with architecture (no action needed)
- 📐 = PRD diverges from architecture — annotate WHY, surface to human review
- Divergences are collected in a `## Architecture Divergences` section at the end of the review

**Review findings format:**
```markdown
# PRD Review — Round N

| # | Criterion | Status | Finding | Fix Hint | Fixed? |
|---|-----------|--------|---------|----------|--------|
| P1 | Value-traced | ✅ | — | — | — |
| P2 | AC testable | ❌ | "AC #3 says 'fast enough'" | Add latency target | ☐ |
| ... | ... | ... | ... | ... | ... |
| P7 | Architecture ref | 📐 | "PRD uses polling; architecture says WebSocket" | — | N/A |

## Architecture Divergences (for human review)
| PRD says | Architecture says | Rationale for divergence |
|----------|------------------|------------------------|
| Polling every 5s | WebSocket push | Simpler for V1; upgrade path clear |

## Summary
PASS: X/6 | FAIL: Y/6 → [PASS | REQUEST_CHANGES]
(P7 divergences noted but do NOT block — human decides)
```

**Fix flow:**
1. If `REQUEST_CHANGES` → dispatch fix agent (pm persona) with findings + PRD
2. Fix agent edits PRD in-place, marks `Fixed? ☑` in findings
3. Re-dispatch reviewer (round N+1)
4. Max 2 rounds → ask user

**Result:** `PASS` → proceed to Step 6

---

### Step 6: UI Design Brief (Optional)

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/persona-ux-designer.md` |
| **Knowledge** | `references/framework-ux-design.md` |
| **Input** | `docs/prd/<version>/<feature>.md` |
| **Output** | `docs/design/<version>/<feature>-ui-brief.md` |

**Skill:** `woos-ui-design-brief`

When the feature has user-facing interface:
- Define screens, layouts, key components
- Define user states (empty, loading, error, success, first-run)
- Establish visual direction
- Optionally generate image concepts

**Trigger:** Before entering Step 6, orchestrator asks user: "Does this feature have user-facing UI?" 
- **Yes** → proceed with Step 6
- **No** → skip Step 6 + 6R, go directly to Step 7

---

### Step 6R: UI Brief Review Gate

| | |
|---|---|
| **Sub-agent** | ✅ (independent reviewer) |
| **Persona** | `references/persona-ux-designer.md` |
| **Knowledge** | `references/framework-ux-validate.md` |
| **Input** | `docs/design/<version>/<feature>-ui-brief.md` + `docs/prd/<version>/<feature>.md` |
| **Output** | `docs/reviews/<version>/<feature>-ui-review-rN.md` |

**Checklist:**

| # | Criterion | Fix Hint |
|---|-----------|----------|
| U1 | Screen coverage | List unmapped user stories; add a screen or flow for each |
| U2 | States complete | Add missing states (empty/loading/error/success) to each screen |
| U3 | Flows connected | Trace each flow end-to-end; add missing transitions or exit points |
| U4 | Visual consistency | Remove contradicting principles; pick one direction |
| U5 | Accessibility realistic | Downgrade to achievable level (AAA→AA); document upgrade timeline |
| U6 | Components sufficient | List screens with no component mapping; add or mark as reuse |
| U7 | Principles actionable | Replace generic ("clean", "modern") with decision-guiding rules |

**Fix flow:** Same protocol. Fix agent uses ux-designer persona. Max 2 rounds.

**Result:** `PASS` → proceed to Step 7

---

### Step 7: Analyze Gate

| | |
|---|---|
| **Sub-agent** | ❌ (orchestrator does this directly) |
| **Persona** | none |
| **Knowledge** | `references/framework-implementation-readiness.md` |
| **Script** | `scripts/analyze_gate.py` |
| **Execution** | Script-assisted direct step — script does extraction/comparison, orchestrator consumes only compact findings + verdict |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/design/<version>/<feature>-ui-brief.md` (if exists) |
| **Output** | `docs/handoff/<version>/<feature>-analyze-report.md` |

This step is mechanical. Run the script, let it write the full report, and keep only the verdict + hotspot list in conversation context.

Cross-artifact consistency check:

| Check | Pass Condition |
|-------|----------------|
| A1: Requirement Coverage | Every user story has AC |
| A2: AC Testability | Every AC verifiable without knowing implementation |
| A3: Flow Completeness | All flows have start/end states |
| A4: Non-goal Alignment | No requirement contradicts non-goals |
| A5: UI Coverage | Every screen maps to ≥1 user story (if UI brief exists) |

**Results:**
- **PASS** → proceed to Step 8
- **GAPS_FOUND** → return to Step 4 (requirement gaps) or Step 6 (UI gaps)

---

### Step 8: Build Handoff Packaging

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/persona-pm.md` |
| **Knowledge** | `references/framework-epics-and-stories.md` |
| **Input** | `docs/prd/<version>/<feature>.md` + `docs/design/<version>/<feature>-ui-brief.md` + `docs/handoff/<version>/<feature>-analyze-report.md` |
| **Output** | `docs/handoff/<version>/<feature>.md` |

**Skill:** `woos-build-handoff`

Package all product artifacts into a single handoff file:
1. Spec versioning (YAML frontmatter)
2. Mission Statement
3. Context (from roadmap)
4. Requirements (user stories + AC + non-goals)
5. User Flows
6. UI Direction (from UI brief, if exists)
7. Build Tasks (product-level breakdown)
8. Verification Plan
9. Open Questions
10. DCR Protocol

**Note:** Technical architecture, data model, API design are NOT in handoff. Engineering decides HOW.

---

### Step 9: Handoff Readiness Check

| | |
|---|---|
| **Sub-agent** | ❌ (orchestrator does this directly) |
| **Knowledge** | `references/framework-implementation-readiness.md` |
| **Template** | `templates/readiness-template.md` |
| **Script** | `scripts/readiness_check.py` |
| **Execution** | Script-assisted direct step — script writes the checklist report, orchestrator only reacts to failing rows |
| **Input** | `docs/handoff/<version>/<feature>.md` |
| **Output** | `docs/reviews/<version>/<feature>-readiness.md` |

This is a checklist step, not a fresh authoring pass. Do NOT dispatch a sub-agent. Run the script against the handoff and use the resulting verdict.

Checklist:
- [ ] All AC are testable
- [ ] Build Tasks map to user stories
- [ ] No unresolved product decisions
- [ ] User flows have no dead ends
- [ ] UI brief covers all interactive features (if applicable)
- [ ] Non-goals clear enough to prevent scope creep
- [ ] DCR protocol specified

**Output file format (matches `templates/readiness-template.md`):**
```markdown
# Readiness Check — <feature>

| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | AC testable | ✅ | — |
| 2 | Tasks → stories | ✅ | — |
| ...

## Unresolved Items
- [Item] — [Why blocked, what decision needed]

## Verdict
**PASS** / **FAIL**
```

**PASS** → handoff ready for engineering (if single feature) or proceed to Step 10 (if multi-feature version)
**FAIL** → return to Step 8 with gaps

---

### Step 10: Version Integration Gate (Cross-Feature Audit)

| | |
|---|---|
| **Sub-agent** | ❌ (orchestrator does this directly) |
| **Persona** | none |
| **Knowledge** | `references/framework-implementation-readiness.md` (traceability discipline) |
| **Script** | `scripts/integration_gate.py` |
| **Execution** | Script-assisted direct step — script reads all version docs, writes the audit report, and returns only compact conflicts to the orchestrator |
| **Input** | **ALL documents for this version** (see Input Scope below) |
| **Output** | `docs/reviews/<version>/integration-report.md` |

**Trigger:** Runs once after ALL features in this version pass Step 9.
**Skip when:** Version has only 1 feature.

#### Input Scope (MUST read all of these)

The integration script MUST read the full content of every document below — not just handoffs:

```
docs/product/<project>-roadmap.md
docs/product/<project>-architecture.md
docs/prd/<version>/<feature>-requirements.md   (× all features)
docs/prd/<version>/<feature>.md                (× all features)
docs/handoff/<version>/<feature>.md            (× all features)
docs/design/<version>/<feature>-ui-brief.md    (× all features, if exists)
```

#### Audit Checklist

**Part A — Shared Concept Consistency:**

| # | Check | Method | Example Failure |
|---|-------|--------|-----------------|
| A1 | State machine unified | Extract all state definitions across features. Every feature that references the same entity MUST use identical states + transitions | Feature B: 7 states vs Feature D: 6 states |
| A2 | Constants consistent | Extract all numeric constants (timeouts, limits, intervals). Same concept MUST have same value everywhere | Heartbeat: 30s in architecture vs 90s in requirements |
| A3 | Data model aligned | Extract all entity schemas/types. Same entity MUST have identical fields across features | Task type has `accepted` in C but not in D |
| A4 | API contract consistent | Extract all endpoint definitions. Same endpoint MUST have consistent request/response schemas, status codes, auth | `POST /start` requires `accepted` state in B but `assigned` in D |
| A5 | Terminology unified | Same concept MUST use same name everywhere | "agent" vs "worker" vs "executor" referring to same entity |

**Part B — Completeness & Traceability:**

| # | Check | Method |
|---|-------|--------|
| B1 | Roadmap → Requirements coverage | Every roadmap feature has a requirements file |
| B2 | Requirements → PRD coverage | Every requirement appears in a PRD |
| B3 | PRD → Handoff coverage | Every PRD user story appears in handoff build tasks |
| B4 | Architecture → PRD alignment | Architecture's component list matches PRD's scope |
| B5 | UI → PRD traceability | Every UI screen/action maps to a PRD user story |

**Part C — Cross-Feature Integration:**

| # | Check | Method |
|---|-------|--------|
| C1 | No AC conflicts | Identify conflicting acceptance criteria between features |
| C2 | User flows connectable | Cross-feature flows have matching entry/exit states |
| C3 | No duplicate effort | Similar functionality across features is merged or explicitly split |
| C4 | Dependency order clear | Build order documented for dependent features |
| C5 | Error handling consistent | Same error scenarios handled the same way across features |

#### Output Format

```markdown
# Version Integration Audit — <version>

## Summary
- Features audited: [list]
- Documents read: [count]
- Result: PASS / CONFLICTS_FOUND

## Part A — Shared Concepts

### State Machine
[extract all state definitions, mark ✅ consistent or ❌ contradicts]

### Constants
| Constant | Doc 1 Value | Doc 2 Value | Status |
|----------|-------------|-------------|--------|
| heartbeat_timeout | 30s (architecture) | 90s (B-requirements) | ❌ |

### Data Model
[compare entity fields across features]

### API Contracts
[compare endpoint definitions]

## Part B — Traceability
[coverage matrix: roadmap → requirements → PRD → handoff]

## Part C — Cross-Feature
[C1-C5 findings]

## Verdict
- **PASS**: No contradictions found
- **CONFLICTS_FOUND**: [list each conflict with fix recommendation]

## Recommended Fix Order
1. [highest priority fix — e.g., unify state machine]
2. ...
```

#### Audit Rules

- The orchestrator/script pair MUST produce a finding for EVERY check (A1-A5, B1-B5, C1-C5) — no skipping
- ANY ❌ in Part A = **CONFLICTS_FOUND** (shared concepts MUST be unified before build)
- Part B gaps = **CONFLICTS_FOUND** (traceability must be complete)
- Part C issues = **CONFLICTS_FOUND** unless explicitly documented as intentional divergence

**Results:**
- **PASS** → all handoffs ready for engineering
- **CONFLICTS_FOUND** → return to conflicting feature's Step 4 (PRD) to resolve, then re-run Steps 5–9 for that feature. If conflict is in architecture/roadmap, fix upstream first.

---

## Steps — Standard Mode

Single feature, one review gate, no UI brief or integration gate.

```
Requirements → PRD → PRD Review → Handoff → Readiness
```

| Step | What | Sub-agent? | Output |
|------|------|:----------:|--------|
| S1 | Requirement Contract | ✅ (pm) | `docs/prd/<version>/<feature>-requirements.md` |
| S2 | PRD Authoring | ✅ (pm) | `docs/prd/<version>/<feature>.md` |
| S3 | PRD Review | ✅ (prd-validator) | `docs/reviews/<version>/<feature>-prd-review-rN.md` |
| S4 | Build Handoff | ✅ (pm) | `docs/handoff/<version>/<feature>.md` |
| S5 | Readiness Check | ❌ orchestrator | `docs/reviews/<version>/<feature>-readiness.md` |

**No:** Priority Ranking, UI Brief, UI Review, Analyze Gate, Integration Gate.
**Fix flow:** Same as Strict — max 2 review rounds on S3.

**⚠️ Standard mode enforcement:**
- S1 MUST produce a separate requirements file (not folded into PRD)
- S2 MUST follow `templates/prd-template.md` — P3 structural check applies
- S3 MUST run Phase A (structural) + Phase B (content) review. No "Conditional Pass."
- S5 MUST produce a readiness output file (not just a mental check)

---

## Steps — Lite Mode

| Step | What |
|------|------|
| L1 | One-sentence Mission |
| L2 | Build Tasks (numbered list) |
| L3 | Acceptance Criteria |
| L4 | Verification |
| L5 | Package into Lite handoff using `woos-build-handoff` |

No review gates, no UI brief, no analyze gate. Self-check only.

---

## State Persistence

### Run Manifest Schema (Stage 2 section)

```yaml
stages:
  product-design-flow:
    status: in_progress
    version: "v1"
    features:
      auth:
        current_step: 9
        steps:
          2-requirements: { status: done, output: "docs/prd/v1/auth-requirements.md" }
          3-priority-ranking: { status: done, output: "docs/prd/v1/auth-requirements.md#priority-ranking" }
          4-prd: { status: done, output: "docs/prd/v1/auth.md" }
          5-prd-review: { status: done, round: 1, result: PASS }
          6-ui-brief: { status: skipped }
          6r-ui-review: { status: skipped }
          7-analyze: { status: done, output: "docs/handoff/v1/auth-analyze-report.md" }
          8-handoff: { status: done, output: "docs/handoff/v1/auth.md" }
          9-readiness: { status: done, result: PASS, output: "docs/reviews/v1/auth-readiness.md" }
      dashboard:
        current_step: 4
        steps:
          2-requirements: { status: done, output: "docs/prd/v1/dashboard-requirements.md" }
          3-priority-ranking: { status: done, output: "docs/prd/v1/dashboard-requirements.md#priority-ranking" }
          4-prd: { status: in_progress, output: "docs/prd/v1/dashboard.md" }
          # ... remaining pending
    integration:
      status: pending  # runs after all features pass step 9
      output: null
```

### Recovery Protocol

Same as Stage 1:
1. Read `run-manifest.yaml`
2. Find first step where `status != done`
3. Check output file → exists/well-formed (mark done) | exists/incomplete (resume) | missing (restart step)
4. Continue

### Update Rules
- Write manifest BEFORE executing a step (`status: in_progress`, plus declared execution path if tracked)
- Write manifest AFTER the step completes (`status: done` + output)
- Reviews record: `round: N`, `result: PASS|REQUEST_CHANGES`

---

## DCR Reception

When coding agent sends a Design Change Request (`docs/feedback/<feature>-dcr.md`):

1. Read DCR — what product assumption is being challenged?
2. Assess impact:
   - **Small change**: Update handoff directly, notify coding agent
   - **Large change**: Return to Step 4 (PRD) or Step 6 (UI brief)
3. Update handoff version number

---

## Checkpoint Control

```yaml
checkpoints:
  - prd-passed      # Pause after PRD Review PASS
  - handoff-ready   # Pause after Readiness PASS
```

If `checkpoints: []` → fully autonomous.

At each checkpoint: present summary → wait for user confirmation → proceed or return.

## Handoff to Engineering

On completion:
- Handoff: `docs/handoff/<version>/<feature>.md`
- Analyze report: `docs/handoff/<version>/<feature>-analyze-report.md`
- Tell user: "Product handoff ready. Engineering stage can begin."

## Failure Handling

| Situation | Action |
|-----------|--------|
| Roadmap missing | Redirect to `woos-product-discovery` first |
| Review loops 3x | Ask user for direction |
| Scope too large | Split into multiple handoffs per sub-feature |
| UI brief but no interface | Skip Step 6 **only with explicit user confirmation**, note in handoff |
| Crash mid-step | Recovery protocol from run-manifest |
| Reference/template/script file not found | Fix path (use absolute), rerun the declared step. **NEVER skip.** |
| Script exits non-zero | Fix input assumptions or parser bug, then rerun. Do NOT switch to sub-agent just to bypass the failure. |
| Output validation fails (P3) | Rerun the same declared path with "Missing sections: ..." or parser fix instruction |
| Step produces empty/stub file | Rerun. Stub output = step not done |

### ❌ Explicitly Forbidden Actions

- **Do NOT merge steps** — each step = 1 declared execution path → 1 verified output
- **Do NOT skip a step because it "failed"** — fix the failure and retry
- **Do NOT pass a review without checking every row** — partial review = review not done
- **Do NOT accept "Conditional Pass"** — only PASS or REQUEST_CHANGES exist
- **Do NOT write PRD without the template** — free-form PRD = not a PRD
- **Do NOT use sub-agents for purely mechanical extraction/checklist steps** — that wastes context and hides deterministic checks inside prose

## Skills Used

| Skill | Step |
|-------|------|
| `woos-ui-design-brief` | 6 |
| `woos-build-handoff` | 8 |

## Scripts Used

| Script | Step |
|--------|------|
| `scripts/analyze_gate.py` | 7 |
| `scripts/readiness_check.py` | 9 |
| `scripts/integration_gate.py` | 10 |

---

## Known Anti-Patterns (from real failures)

These are things agents ACTUALLY DO when executing this workflow. Catch yourself:

| Anti-Pattern | Why It's Wrong | Correct Behavior |
|---|---|---|
| Merging Step 2+3 into PRD | Requirements file never exists; priority ranking never done independently | Each step = separate dispatch, separate output file |
| Writing PRD "free-form" | Template sections missing → review can't validate completeness | Copy template, fill each section. Empty section = `[NEEDS CLARIFICATION: reason]` |
| Giving reviewer a vague prompt | "Check for issues" → reviewer only finds 2-3 surface problems | Paste FULL checklist. Require verdict on EVERY row |
| Accepting "Conditional Pass" | Means "partially broken but too lazy to fix" | Only PASS or REQUEST_CHANGES. Conditional = REQUEST_CHANGES |
| Skipping step after file-not-found | The step's output doesn't exist → downstream steps fail silently | Fix path, retry. Never skip |
| Readiness as mental check | No output file → no audit trail, no proof of validation | Write `docs/reviews/<version>/<feature>-readiness.md` |
| Sub-agent reviewing own work | Confirmation bias — author can't see own gaps | Fresh sub-agent with no prior context of authoring |
| Dispatching sub-agent without reading reference files | Sub-agent says "I'm a PM" but has no persona principles, no framework knowledge, no template to follow → shallow generic output | Read persona .md + knowledge .md + template .md → inject verbatim into dispatch prompt (P2) |
| Using a sub-agent for Step 7/9/10 | The agent rereads hundreds of lines just to extract/checklist data → bloated context, weak comparisons | Keep mechanical steps local. Use the script, store the full report on disk, keep only verdict + hotspots in context |
| Carrying every prior feature summary into the next feature | F4 pays token cost for F1-F3, and step discipline degrades under compression | Keep only current feature context plus cross-feature facts that are actually needed |
| Passing full roadmap + architecture + all reviews into every authoring step | Creative work gets buried under irrelevant context and quality drops feature-by-feature | Inject only the current feature inputs and the minimum shared documents required for that step |
| Echoing full script reports back into the main conversation | You pay token cost twice: once to generate the report and again to restate it | Keep the report on disk; summarize only verdict, failing checks, and exact files to revisit |

### Context Cost Management Best Practices

1. Use sub-agents only where persona isolation or reviewer independence matters: Steps 2, 4, 5, 6, 6R, and 8.
2. Keep Step 3 in the orchestrator context — it is bounded judgment on a file that is already open, not a fresh authoring pass.
3. Run Steps 7, 9, and 10 through scripts first. Let the script read the files, write the full markdown report, and return only a compact verdict.
4. Retain only the current feature's live context in conversation. Older feature reports stay on disk unless a later step explicitly needs them.
