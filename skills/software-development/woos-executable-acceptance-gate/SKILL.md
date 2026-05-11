---
name: woos-executable-acceptance-gate
description: Enforce executable done criteria by mapping requirements to concrete automated checks.
version: 1.0.0
author: Hermes Profile
license: MIT
---

# Woos Executable Acceptance Gate

## Purpose

Ensure "done" is proven by executable checks, not manual confidence.

## Required Mapping

For each requirement or acceptance criterion, provide:

- `requirement_id`
- `check_type` (unit/integration/e2e/lint/type/security/perf/schema)
- `check_command` or test identifier
- `expected_result`
- `status` (pass/fail/not_run)

## Hard Gate Rules

- If a must-have requirement has no executable check, return `REQUEST_CHANGES`.
- If a required check fails, return `REQUEST_CHANGES`.
- If checks cannot run due to environment/tooling, return `BLOCKED`.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `acceptance_trace`: requirement -> check -> result
- `missing_executable_checks`
- `failed_checks`

