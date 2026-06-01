---
name: woos-prd-consistency-audit
description: Dedicated analyze gate for PRD and UI brief consistency. Runs script extraction first, then semantic review with evidence-backed findings.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, prd, audit, consistency, gate]
    related_skills:
      - woos-product-design-flow
      - woos-ui-design-brief
---

# PRD Consistency Audit

## Purpose

Run Step 6 of `woos-product-design-flow` as an isolated audit skill.

This skill exists to stop the parent orchestrator from skipping straight to a soft summary like "looks consistent enough."

## Required Invocation (hard gate)

- MUST be invoked as a separate skill
- MUST run `scripts/analyze_gate.py` before semantic review, OR replicate its extraction logic with equivalent precision (see Phase 1 fallback below)
- MUST use the script output as evidence, not as the final verdict
- MUST review every A1-A5 check explicitly
- If script execution is skipped **and** the manual fallback is not followed, return `BLOCKED`

## Required Load Set (mandatory)

Before auditing, load and report:

- `references/framework-implementation-readiness.md`
- `scripts/analyze_gate.py`
- `docs/prd/<version>/<feature>.md`
- `docs/design/<version>/<feature>-ui-brief.md` (if present)

If any required file is not loaded, return `BLOCKED`.

## Conditional Load Set (upstream dependencies)

When the orchestrator provides upstream interface summaries, also load:

- `docs/prd/<version>/<upstream-feature>-interface.md` for each declared upstream dependency

When upstream interface summaries are present, add **A6** to the required checks:

| A6 | Upstream Interface Consistency | All shared concepts used in this feature's PRD/UI match upstream interface definitions (enums, field names, event types, terminology) |

A6 failures count toward `GAPS_FOUND`.

## Output

- `docs/handoff/<version>/<feature>-analyze-report.md`

## Two-Phase Protocol

### Phase 1 — Script Extraction

**Preferred path:** Run `scripts/analyze_gate.py` to extract:

- user stories
- acceptance criteria
- flows
- non-goals
- UI screens
- placeholders
- deterministic hotspot candidates

**Fallback path (when shell execution is unavailable):** Replicate the extraction logic manually using the same algorithms documented in `scripts/_audit_utils.py`. The script's extraction logic is deterministic regex-based — it searches for `As a ... I want to ...` patterns (user stories), `Given/When/Then` BDD checklist items under "Acceptance Criteria" headings (ACs), inline `->` or `→` arrow items under flow section headings (flows), section-titled "Non-Goals"/"Out of Scope" content, "Screen " heading patterns and table-surface listings (UI screens), and `[NEEDS CLARIFICATION]`, `TBD`, `TODO`, `[ASSUMPTION]` regex patterns (placeholders). When using the fallback:

- Read each extraction target's implementation in `_audit_utils.py` to match the algorithm faithfully.
- Report **both** the manual extraction output **and** the fact that shell was unavailable, so the semantic reviewer knows the extraction is hand-run rather than a direct script invocation.
- Do NOT relax extraction standards — the fallback must be as precise as the script.
- Document any extraction uncertainty explicitly (e.g. "could not determine exact count, estimated range").

If neither path can be followed, return `BLOCKED`.

Known script limitations to account for during semantic review:

- FR-based PRDs may legitimately fail user-story extraction when requirements are written as functional requirements plus acceptance criteria rather than `As a ... I want ...` statements.
- Fenced multiline arrow flows may legitimately fail flow extraction when the script only finds inline/bulleted `->` or `→` items.
- UI coverage mismatches may be downstream false positives when story extraction fails first.

### Phase 2 — Semantic Audit

Review the extracted evidence and decide whether script-flagged mismatches are:

- real gaps
- wording differences
- acceptable scope choices

## Required Checks

| # | Check | Pass Condition |
|---|-------|----------------|
| A1 | Requirement Coverage | Every user story has acceptance criteria |
| A2 | AC Testability | Every AC is verifiable without implementation knowledge |
| A3 | Flow Completeness | Flows have clear start/end transitions |
| A4 | Non-goal Alignment | Requirements do not contradict non-goals |
| A5 | UI Coverage | Every UI screen maps to one or more user stories |

## Output Contract (required)

The final report MUST contain a table with these columns:

| Check | Script Evidence | Semantic Judgment | Result |
|------|------------------|-------------------|--------|

Every A1-A5 row must be present.

## Verdicts

- `PASS` — all A1-A5 rows pass after semantic review
- `GAPS_FOUND` — one or more real gaps remain
- `BLOCKED` — script not run, evidence missing, or row coverage incomplete

Important interpretation rule:
- Script extraction failures do **not** automatically force `GAPS_FOUND`. When FR-based requirement structure, fenced multiline flows, or downstream story-extraction misses create false positives, the auditor may still return `PASS` if each affected row is defended with specific semantic evidence from the PRD/UI artifacts.
- For common override patterns and suggested wording, consult `references/semantic-override-cases.md` before writing the final report.

## Fail-Closed Rules

- PASS is forbidden if the report only gives a summary without row-level evidence
- If script output and final judgment disagree, explain why
- If UI brief is absent, A5 must still appear as `N/A` with reason
