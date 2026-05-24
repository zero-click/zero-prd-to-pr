# Implementation Readiness Framework

## Purpose

Validate that all planning artifacts (PRD, epics, stories, architecture) are complete, consistent, and sufficient for engineering to begin implementation without ambiguity.

## Input

- PRD (functional and non-functional requirements)
- Epics & Stories (with acceptance criteria)
- System Architecture (components, boundaries, decisions)
- UX Design Brief (if applicable)

## Methodology

### 1. Four-Layer Validation

Check each layer in order. A failure at any layer blocks proceeding.

**Layer 1: PRD Completeness**
- Every FR has acceptance criteria that are testable
- Every NFR has a measurable target (number, not adjective)
- No TBD / placeholder sections remaining
- Open questions either resolved or explicitly deferred with rationale
- Success metrics defined with specific targets

**Layer 2: Epic Coverage**
- Every FR maps to exactly one epic (use coverage map)
- No orphan FRs (requirements that no epic addresses)
- No orphan epics (epics that don't trace back to FRs)
- Epic dependencies are acyclic and explicitly ordered

**Layer 3: Architecture Alignment**
- Every epic maps to specific architecture components
- No epic requires a component that doesn't exist in architecture
- Communication patterns between components are defined for each epic's needs
- Data entities referenced in FRs have a defined storage location

**Layer 4: Story Quality**
- Every story has testable acceptance criteria
- Stories are small enough to implement in a single work session
- Dependencies between stories are explicitly stated
- Edge cases from PRD are covered by at least one story's acceptance criteria

### 2. Traceability Matrix

Build a complete trace from requirement to implementation:

```
FR-1 → Epic 1 → Story 1.1 → Component: Auth Service → Test: AC-1.1.1
FR-2 → Epic 1 → Story 1.2 → Component: Auth Service → Test: AC-1.2.1
...
```

Any broken chain = gap that must be resolved before handoff.

### 3. Gap Documentation

For each gap found:
- **What's missing**: Specific description
- **Impact**: What would go wrong if engineering starts without this
- **Severity**: Critical (blocks all work) / High (blocks specific epic) / Medium (causes rework)
- **Recommendation**: Who should fix this and how

### 4. Final Verdict

- **READY** — All layers pass, traceability complete, no critical/high gaps
- **READY WITH CAVEATS** — Minor gaps documented, engineering can start with awareness
- **NOT READY** — Critical or high gaps exist, specific fixes required before handoff

## Output Structure

```markdown
# Implementation Readiness Report

## Summary
**Verdict**: [READY / READY WITH CAVEATS / NOT READY]
**Date**: [assessment date]

## Layer Results
| Layer | Status | Issues Found |
|-------|--------|-------------|
| PRD Completeness | ✅/❌ | [count] |
| Epic Coverage | ✅/❌ | [count] |
| Architecture Alignment | ✅/❌ | [count] |
| Story Quality | ✅/❌ | [count] |

## Traceability Matrix
| FR | Epic | Story | Component | Status |
|----|------|-------|-----------|--------|
| FR-1 | Epic 1 | Story 1.1 | Auth | ✅ |
| FR-2 | Epic 1 | Story 1.2 | Auth | ✅ |
| FR-3 | Epic 2 | — | — | ❌ Gap |

## Gaps
### Critical
[None / list with impact and recommendation]

### High
[None / list with impact and recommendation]

### Medium
[None / list]

## Recommendations
[Ordered list of actions to reach READY status]
```

## Quality Criteria

- All four layers explicitly assessed (no skipping)
- Every gap has severity, impact, and recommendation (not just "something is missing")
- Traceability matrix is complete (covers ALL FRs)
- Verdict is honest — don't say READY if high gaps exist
- Assessment is based on artifacts as they ARE, not as they should be
