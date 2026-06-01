---
name: woos-prd-authoring
description: Write the per-feature PRD from the ranked requirements contract using the mandatory PRD template.
version: 1.1.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, prd, authoring, design-flow]
    related_skills:
      - woos-product-design-flow
      - woos-requirement-contract
      - woos-product-prd-review-gate
---

# PRD Authoring

## Purpose

Convert the ranked requirements contract into a full PRD for one feature.

## Required Load Set (mandatory)

- `references/framework-prd.md`
- `references/template-prd-template.md`
- `templates/prd-template.md`
- `docs/prd/<version>/<feature>-requirements.md`

If any required file is not loaded, return `BLOCKED`.

## Conditional Load Set (upstream dependencies)

When the orchestrator provides upstream interface summaries, also load:

- `docs/prd/<version>/<upstream-feature>-interface.md` for each declared upstream dependency

When referencing shared concepts (status enums, data models, event types, API endpoints), use the exact definitions from upstream interface summaries. Do NOT invent alternate names for concepts already defined upstream.

## Pitfalls and Fix Loop Guidance

- Do not point downstream PRD dependency sections at upstream full PRDs when the shared contract should live in an `*-interface.md` summary. If the summary is missing, create/update the upstream interface summary first, then cite that summary as the dependency source.
- Do not leave must-ship numeric thresholds vague when a stable upstream product number already exists. Replace placeholders like `v1 threshold` or `product threshold` with the exact value in both the requirements contract and PRD.
- When a feature introduces new shared downstream concepts that later features will consume (new states, event types, idempotency keys, canonical IDs), create its interface summary before moving to the next feature so review gates validate against the stable contract snapshot rather than the whole PRD.

## Output

- `docs/prd/<version>/<feature>.md`

## Required Sections

1. `## Background`
2. `## User Personas`
3. `## Functional Requirements`
4. `## Non-Functional Requirements`
5. `## User Flows`
6. `## Edge Cases`
7. `## Non-Goals`
8. `## Success Metrics`

## Authoring Rules

- Follow the template exactly
- Give full detail to `P0` scope; keep `P2` brief
- Mark unresolved items as `[NEEDS CLARIFICATION: ...]`
- Do not embed review verdicts or gate outcomes in the PRD itself
- When a P0 mutation needs retry safety, define the **canonical idempotency contract explicitly** in the PRD and requirements (field name + uniqueness scope + replay behavior). Do not write vague phrases like "same request retried" or "duplicate replay" without specifying the key (for example a caller-supplied request ID) and the tuple used to recognize a replay.
- When a feature extends a previously summarized shared interface (new enum values, event types, or API replay fields), coordinate that extension with the relevant upstream `*-interface.md` summary rather than silently diverging from it inside the PRD alone.
- When documenting rejection/audit behavior, separate **pre-validation/auth failures** from **post-evaluation business rejections** if they have different audit visibility rules; otherwise review gates will correctly flag a contradiction.

## Action/Mutation Feature Pitfall

Features that introduce **state-mutating actions** (cancel, retry, reassign, unblock, delete, approve, reject) are particularly prone to missing NFRs and edge cases because the author focuses on the action definitions and happy-path flows. The PRD review gate will flag these gaps as FAIL_AND_REWORK.

**Always include for action/mutation features:**

- **Non-Functional Requirements** — idempotency (key + window + replay behavior), concurrency control (first-commit-wins vs last-writer-wins), latency targets, and auditability guarantees.
- **Edge Cases table** — concurrent mutations on the same entity, invalid pre-state attempts, partial failures (state mutated but event append failed), and cross-feature conflicts (e.g., operator cancel arriving simultaneously with agent completion).
- **Event payload details** — each mutation's audit event must list explicit payload fields (not just "action-specific payload"). Sparse payloads get flagged by review gates.

**Common rework pattern:** PRD defines FRs for each action but omits §5 (NFRs) and §6 (Edge Cases) entirely, or lists them as stubs without concrete thresholds. The review gate rejects; author patches them in; second review passes.

## Known Subagent Limitations

When delegated to a subagent for PRD writing, two failure modes are common:

1. **Timeout at 600s** — The subagent exceeds the 10-minute timeout when the PRD is long or requires extensive research across multiple documents.
2. **Output truncation** — The subagent's response is capped at the model's output token limit (typically 8K–16K tokens). Complex PRDs with multiple FRs, detailed acceptance criteria, and full edge-case tables easily exceed this.

**Fallback strategy for orchestrators:**

If the subagent fails due to timeout or truncation:
- Do NOT retry the same subagent with the identical goal — it will hit the same wall.
- Instead, fall back to orchestrator-direct authoring using `write_file` and `execute_code`. The orchestrator can write the PRD directly since it already has the requirements contract and architecture in context.
- Alternatively, if retrying via subagent, split the work: have the subagent write a shorter PRD (e.g. focus on P0 FRs only, skip appendices) and have the orchestrator add remaining sections directly.

An orchestrator writing the PRD directly is always preferable to repeated subagent failures that stall the pipeline.
