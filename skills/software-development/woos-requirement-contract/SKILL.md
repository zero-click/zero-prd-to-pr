---
name: woos-requirement-contract
description: Build a structured requirement contract before PRD/design/coding to reduce ambiguity and enable automated acceptance.
version: 1.0.0
author: Hermes Profile
license: MIT
---

# Woos Requirement Contract

## Purpose

Convert loose requests into a deterministic input contract for autonomous execution.

## Required Input Schema

1. `objective`: user/business outcome
2. `constraints`: technical and policy constraints
3. `acceptance_criteria`: testable, machine-checkable criteria
4. `non_goals`: explicitly out of scope
5. `risks_assumptions`: known risks and assumptions
6. `priority`: must/should/could

## Hard Gate Rules

- If any required field is missing, return `REQUEST_CHANGES`.
- If acceptance criteria are not measurable/testable, return `REQUEST_CHANGES`.
- If external dependency is unknown and blocks design, return `BLOCKED`.

## Output Contract

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `requirement_contract_path`
- `missing_fields`
- `ambiguities`
- `ready_for_prd`: boolean

