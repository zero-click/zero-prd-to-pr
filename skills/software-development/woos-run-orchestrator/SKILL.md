---
name: woos-run-orchestrator
description: Orchestrate autonomous workflow runs with queueing, concurrency, timeout, and retry controls.
version: 1.0.0
author: Hermes Profile
license: MIT
---

# Woos Run Orchestrator

## Purpose

Provide execution control plane for near-unattended workflow runs.

## Required Runtime Policy

- `queue_policy`: FIFO | priority
- `max_concurrency`
- `timeout_seconds` per stage
- `retry_policy` (attempts + backoff)
- `cancellation_policy`

## Execution Contract

1. Admit run with a unique run id.
2. Assign stage ownership and dependencies.
3. Enforce timeout/retry policy.
4. Emit stage status transitions.
5. Trigger failure state machine and human handoff when needed.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `run_id`
- `stage_statuses`
- `timeouts`
- `retries`
- `handoff_triggered`

