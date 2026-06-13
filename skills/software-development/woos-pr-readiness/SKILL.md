---
name: woos-pr-readiness
description: Final pre-PR gate. Reruns verification-loop, auto-generates the traceability matrix from the plan's Story Table + test outcomes, confirms commit/PR discipline, then triggers PR creation.
version: 2.0.0
author: Hermes Profile
license: MIT
---

# Woos PR Readiness

## Purpose

Confirm work is ready for commit/PR handoff, and produce the artifacts the PR description needs (traceability matrix + test plan summary).

## Required Invocation (hard gate)

- MUST invoke `verification-loop` first (final pass — Gate 2 already ran it per-story; this run catches any regression introduced after the last story finished).
- If `verification-loop` is not invoked, return `NOT_RUN` and stop.
- If unavailable, return `BLOCKED` and stop.
- Do not replace with manual "looks good" checks only.

## Contract

- Check git diff/status is understood and scoped
- Check verification outcomes are explicitly reported
- Check conventional commit and PR test plan readiness
- Check implementation traceability against approved artifacts that exist for the active mode:
  - **Standard:** PRD, roadmap, architecture, engineering plan, supporting interface/UI artifacts when available.
  - **Lite:** PRD, roadmap, architecture, supporting interface/UI artifacts when available. There is no engineering plan artifact in Lite (Gate 1 is skipped); absence of `engineering-plan` MUST NOT cause `REQUEST_CHANGES` and MUST NOT be fabricated.
- Check artifact updates are complete when intentional deviations exist
- **Produce the traceability matrix** as `docs/traceability/<version>/<feature-id>-traceability.md` (Standard mode only)
- Return `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output fields (required):
  - `verification_skill_used: verification-loop`
  - `verification_summary`
  - `execution_mode: Lite | Standard`
  - `engineering_plan_present: true|false`
  - `traceability_matrix_path` (Standard mode: file path of generated matrix; Lite: omitted)
  - `traceability_matrix_inline` (rendered table for embedding in the PR body)
  - `artifact_sync_status: PASS | REQUEST_CHANGES`
  - `artifact_update_notes`

Gate passes only when `artifact_sync_status` is `PASS`.

## Traceability Matrix Generation (Standard mode)

This skill OWNS the traceability artifact. The matrix is generated mechanically — no LLM judgment required:

1. Read the plan's Story Table at `docs/engineering/<version>/<feature-id>-plan.md`.
2. For every PRD AC in the table's `AC` column:
   - Locate the story row(s) that cover it
   - Locate the test files inside those rows' `Diff Scope`
   - Capture the test runner's PASS/FAIL outcome from the last `verification-loop` run
3. Emit `docs/traceability/<version>/<feature-id>-traceability.md`:

```markdown
# <feature-id> Traceability

| PRD AC | Story | Plan Section | Test File | Test Name | Last Run |
|--------|-------|--------------|-----------|-----------|----------|
| FR-1.a | s01   | Architecture | store/persist_test.go | TestPersist | ✅ PASS |
| FR-1.b | s02   | Architecture | store/persist_test.go | TestPersist_Update | ✅ PASS |
```

4. Embed the same table in the PR body (via `traceability_matrix_inline`).

If any AC has no test or any test failed, return `REQUEST_CHANGES`. (This is a safety net — the `woos-code-review-gate` AC-coverage check should have caught it first.)

## Post-Pass Action (PR creation)

When the gate returns `PASS`, the orchestrator MUST dispatch `git-workflow` to run `gh pr create` using the test plan and traceability matrix produced here. PR creation is NOT performed by this skill; this skill only certifies readiness and produces the matrix. The orchestrator records the resulting PR URL in `run-manifest.yaml` under `gate-4-pr.pr_url`.

