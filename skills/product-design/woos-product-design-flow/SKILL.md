---
name: woos-product-design-flow
description: "Stage 2 orchestrator: take a version from the product roadmap and produce PRD + UI direction + build handoff. Dispatches sub-agents per step with domain knowledge."
version: 4.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, design, prd, handoff, review-gate, ui, orchestrator]
    stage: 2
    flow: woos-idea-to-delivery-v2
---

# Product Design Flow (Orchestrator)

## Purpose

Transform one version from the product roadmap into a build-ready product handoff. This is **Stage 2** of the woos-idea-to-delivery flow. Run once per version.

Focus: define WHAT to build and WHY. Technical architecture (HOW) is engineering's job.

## Role

This file defines an **orchestrator** — a thin state machine that:
1. Tracks which step we're on (via `run-manifest.yaml`)
2. Dispatches sub-agents with the right persona + knowledge
3. Collects outputs, decides next step
4. Handles review fix loops

## Project Root Requirement

All file paths (`docs/`) are relative to a **project root directory** which MUST be a git repository.

## When to Use

- User says "start V1" / "design this feature" / "ready to build X"
- Product roadmap exists and a version has been selected

## Prerequisites

- `docs/product/<project>-roadmap.md` exists (from Stage 1)

## Modes

| Mode | When | Gate Reviews | Handoff |
|------|------|-------------|---------|
| **Standard** | Default. Multi-feature, UX matters | PRD Review + UI Review + Analyze | Full |
| **Lite** | Small scope, obvious UX, low risk | None (self-check) | 4 fields only |

---

## Steps — Standard Mode

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
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/prd.md` |
| **Input** | `docs/product/<project>-roadmap.md` § target version |
| **Output** | `docs/prd/<feature>-requirements.md` |

Produce structured requirements:
- Goals and constraints
- Acceptance criteria (machine-checkable where possible)
- Non-goals
- Risk assumptions and unknowns

---

### Step 3: Priority Ranking

| | |
|---|---|
| **Sub-agent** | ✅ |
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | _(persona sufficient — ranking is judgment, not methodology)_ |
| **Input** | `docs/prd/<feature>-requirements.md` |
| **Output** | `docs/prd/<feature>-requirements.md` → appends `## Priority Ranking` |

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
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/prd.md` + `references/bmad/templates/prd-template.md` |
| **Input** | `docs/prd/<feature>-requirements.md` (including Priority Ranking) |
| **Output** | `docs/prd/<feature>.md` |

Write full PRD (P0 requirements get full detail, P2 gets brief mention):
- User stories with acceptance criteria
- Functional and non-functional requirements
- Edge cases and error handling
- User flows (text-based)

---

### Step 5: PRD Review Gate

| | |
|---|---|
| **Sub-agent** | ✅ (independent reviewer) |
| **Persona** | `references/bmad/personas/prd-validator.toml` |
| **Knowledge** | `references/bmad/frameworks/validate-prd.md` + `references/bmad/templates/prd-validation-checklist.md` |
| **Input** | `docs/prd/<feature>.md` + `docs/prd/<feature>-requirements.md` |
| **Output** | `docs/reviews/<feature>-prd-review-rN.md` |

**Checklist:**

| # | Criterion | Fix Hint |
|---|-----------|----------|
| P1 | Value-traced | Add "User value: …" line linking each requirement to a user outcome |
| P2 | AC testable | Rewrite as "Given X, When Y, Then Z" or add measurable threshold |
| P3 | Non-goals effective | Make specific enough to reject a concrete feature request |
| P4 | Edge cases covered | Add "What if…" for: empty state, error, timeout, concurrent access |
| P5 | Real user behavior | Replace developer-centric language with user-observable actions |
| P6 | No contradictions | Identify conflicts; pick one, move the other to non-goals |

**Review findings format:**
```markdown
# PRD Review — Round N

| # | Criterion | Status | Finding | Fix Hint | Fixed? |
|---|-----------|--------|---------|----------|--------|
| P1 | Value-traced | ✅ | — | — | — |
| P2 | AC testable | ❌ | "AC #3 says 'fast enough'" | Add latency target | ☐ |

## Summary
PASS: X/6 | FAIL: Y/6 → [PASS | REQUEST_CHANGES]
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
| **Persona** | `references/bmad/personas/ux-designer.toml` |
| **Knowledge** | `references/bmad/frameworks/ux-design.md` |
| **Input** | `docs/prd/<feature>.md` |
| **Output** | `docs/design/<feature>-ui-brief.md` |

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
| **Persona** | `references/bmad/personas/ux-designer.toml` |
| **Knowledge** | `references/bmad/frameworks/ux-validate.md` |
| **Input** | `docs/design/<feature>-ui-brief.md` + `docs/prd/<feature>.md` |
| **Output** | `docs/reviews/<feature>-ui-review-rN.md` |

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
| **Sub-agent** | ✅ |
| **Persona** | _(qa — no BMAD persona needed)_ |
| **Knowledge** | `references/bmad/frameworks/implementation-readiness.md` |
| **Input** | `docs/prd/<feature>.md` + `docs/design/<feature>-ui-brief.md` (if exists) |
| **Output** | `docs/handoff/<feature>-vN-analyze-report.md` |

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
| **Persona** | `references/bmad/personas/pm.toml` |
| **Knowledge** | `references/bmad/frameworks/epics-and-stories.md` |
| **Input** | `docs/prd/<feature>.md` + `docs/design/<feature>-ui-brief.md` + analyze report |
| **Output** | `docs/handoff/<feature>-vN.md` |

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
| **Input** | `docs/handoff/<feature>-vN.md` |
| **Output** | _(pass/fail — updates run-manifest)_ |

Checklist:
- [ ] All AC are testable
- [ ] Build Tasks map to user stories
- [ ] No unresolved product decisions
- [ ] User flows have no dead ends
- [ ] UI brief covers all interactive features (if applicable)
- [ ] Non-goals clear enough to prevent scope creep
- [ ] DCR protocol specified

**PASS** → handoff ready for engineering
**FAIL** → return to Step 8 with gaps

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
    version: "V1"
    feature: "<feature-name>"
    current_step: 5
    steps:
      1-select-scope: { status: done }
      2-requirements: { status: done, output: "docs/prd/<feature>-requirements.md" }
      3-priority-ranking: { status: done, output: "docs/prd/<feature>-requirements.md#priority-ranking" }
      4-prd: { status: done, output: "docs/prd/<feature>.md" }
      5-prd-review: { status: in_progress, round: 1, result: REQUEST_CHANGES }
      6-ui-brief: { status: pending }
      6r-ui-review: { status: pending }
      7-analyze: { status: pending }
      8-handoff: { status: pending }
      9-readiness: { status: pending }
```

### Recovery Protocol

Same as Stage 1:
1. Read `run-manifest.yaml`
2. Find first step where `status != done`
3. Check output file → exists/well-formed (mark done) | exists/incomplete (resume) | missing (restart step)
4. Continue

### Update Rules
- Write manifest BEFORE dispatching sub-agent (`status: in_progress`)
- Write manifest AFTER sub-agent returns (`status: done` + output)
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
- Handoff: `docs/handoff/<feature>-vN.md`
- Analyze report: `docs/handoff/<feature>-vN-analyze-report.md`
- Tell user: "Product handoff ready. Engineering stage can begin."

## Failure Handling

| Situation | Action |
|-----------|--------|
| Roadmap missing | Redirect to `woos-product-discovery` first |
| Review loops 3x | Ask user for direction |
| Scope too large | Split into multiple handoffs per sub-feature |
| UI brief but no interface | Skip Step 6, note in handoff |
| Crash mid-step | Recovery protocol from run-manifest |

## Skills Used

| Skill | Step |
|-------|------|
| `woos-ui-design-brief` | 6 |
| `woos-build-handoff` | 8 |
