# Semantic override cases for PRD/UI consistency audit

Use this reference when `analyze_gate.py` reports gaps but the artifacts may still be semantically consistent.

## 1. FR-style PRDs instead of user-story prose

False-positive pattern:
- Script reports `A1 FAIL` with low or zero story count
- PRD is organized as `FR-1`, `FR-2`, ... with explicit `Acceptance Criteria` blocks

How to judge:
- Treat FR-style structure as valid if each in-scope requirement has concrete, testable acceptance criteria
- Do not require `As a / I want to / so that` wording when the PRD is otherwise implementation-ready

## 2. Fenced multiline arrow flows

False-positive pattern:
- Script under-extracts flows or reports fewer flows than actually exist
- PRD expresses flows as headed sections with multiline arrow transitions instead of bullet lists

How to judge:
- Read the full flow sections semantically
- If the start state, transition, and end outcome are all explicit, count the flow as covered even if the script extraction is partial

## 3. Cascading UI-coverage failures

False-positive pattern:
- Script reports `A5 FAIL` / screen mismatch after `A1` story extraction failed
- UI brief still clearly maps screens to FRs, states, and user flows

How to judge:
- Treat A5 as downstream noise when the root cause is missing story extraction rather than a real UI/PRD mismatch
- Reconstruct traceability manually: screen -> FR -> acceptance criteria -> flow/state coverage

## 4. Interface-contract document instead of UI brief

False-positive pattern:
- Script reports `A5 FAIL` with 0 screens extracted
- The feature's interface document (e.g. `*-interface.md`) is a backend/API contract (endpoints, JSON schemas, event types, state transitions), not a visual UI brief
- UI surfaces are pre-existing (task detail, timeline, etc.) — this feature modifies existing surfaces rather than creating new screens

How to judge:
- Check whether the feature actually introduces new standalone screens or modifies existing surfaces. New screens mean a UI brief is expected; modifications to existing surfaces can be documented via an interface contract alone.
- Confirm that all FRs with UI consequences (status badge, completion section, run history, terminal timeline events) can be mapped to specific pre-existing surfaces.
- Treat the interface-contract doc as sufficient when the feature is infrastructure/backend-driven and modifies rather than creates UI.
- Document the override explicitly: "Interface doc is backend/API contract; UI surfaces (task detail, timeline) are pre-existing; no new screens needed."

Note: This override only applies when the UI surfaces are genuinely pre-existing. If the feature creates new surfaces without a UI brief, that is a real gap.

## Recommended semantic override language

Use wording like:
- "Script-reported A1/A5 failures are attributable to known extractor limitations, not artifact mismatch."
- "FR-style PRD structure is valid under this skill when requirements are explicit and testable."
- "Partial flow extraction does not indicate a real gap when fenced multiline flows are semantically complete."
- "Interface doc is backend/API contract; UI surfaces are pre-existing; no new screens needed."

## Checklist before overriding

Only override the script if all are true:
1. Every in-scope functional requirement has explicit ACs
2. Flows are complete when read semantically
3. UI surfaces can be mapped back to FRs and operator workflows
4. No real non-goal or scope contradictions remain
