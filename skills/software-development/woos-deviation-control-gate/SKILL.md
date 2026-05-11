---
name: woos-deviation-control-gate
description: Block unresolved implementation drift against PRD/design/capability artifacts.
version: 1.0.0
author: Hermes Profile
license: MIT
---

# Woos Deviation Control Gate

## Purpose

Stop silent drift between planned intent and final implementation.

## Required Inputs

- Approved PRD
- Approved design artifact
- Capability contract
- Current implementation diff and test results

## Drift Classification

- `none`
- `intentional_documented`
- `intentional_undocumented`
- `unintentional`

## Hard Gate Rules

- `intentional_undocumented` or `unintentional` => `REQUEST_CHANGES`.
- `intentional_documented` only passes when all affected artifacts are updated.
- Unknown artifact baseline => `BLOCKED`.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `deviation_findings`
- `deviation_type`
- `artifact_update_required`
- `artifact_update_status`

