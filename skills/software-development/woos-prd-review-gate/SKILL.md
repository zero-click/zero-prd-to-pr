---
name: woos-prd-review-gate
description: Independent PRD review gate for Hermes workflow. Executes planner + architect reviews and returns PASS or REQUEST_CHANGES.
version: 1.1.0
author: Hermes Profile
license: MIT
---

# Woos PRD Review Gate

## Purpose

Run a strict PRD review gate after PRD drafting and before design.

## Required reviewers

1. `planner`
2. `architect`

Both must review the same PRD artifact independently.

## Required Invocation (hard gate)

- MUST invoke `planner` and `architect`.
- If either one is not invoked, return `NOT_RUN` and stop.
- If either one is unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or generic reviewer.

## Contract

- Inputs: PRD path, feature context, constraints
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output content: concrete findings and required edits
- Output fields (required):
  - `reviewers_used: [planner, architect]`
  - `planner_status`
  - `architect_status`
  - `blocking_findings`

If either reviewer requests changes, gate result is `REQUEST_CHANGES`.
