---
name: woos-workflow-memory
description: Capture and reuse failure/rework patterns from workflow runs to improve unattended reliability over time.
version: 1.0.0
author: Hermes Profile
license: MIT
---

# Woos Workflow Memory

## Purpose

Create a persistent learning loop so the workflow gets more reliable across runs.

## Capture Schema

- `run_id`
- `feature_scope`
- `failures` (type, gate, root cause)
- `rework_events`
- `effective_fixes`
- `preventive_rules`
- `handoff_events`

## Required Behavior

1. Record every `REQUEST_CHANGES` and `BLOCKED` event.
2. Distill reusable guidance into short, actionable rules.
3. Feed preventive guidance into the next requirement/design/review cycle.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `memory_entries_written`
- `preventive_guidance`
- `followup_actions`

