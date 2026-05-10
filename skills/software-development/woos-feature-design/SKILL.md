---
name: woos-feature-design
description: Create implementation-ready feature technical design after PRD and capability contract are available.
version: 1.1.0
author: Hermes Profile
license: MIT
---

# Woos Feature Design

## Purpose

Produce a technical design artifact that is precise enough for TDD and implementation.

## Required Invocation (hard gate)

- MUST invoke `architect` to produce/revise the design.
- For high-complexity scope, also invoke `planner` to validate decomposition and sequencing.
- If required invocation is missing, return `NOT_RUN` and stop.
- If required component is unavailable, return `BLOCKED` and stop.
- Do not substitute with undocumented ad-hoc design notes.

## Contract

- Input: approved PRD + capability contract
- Output file: `docs/design/<feature>.md` (or project convention)
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output fields (required):
  - `design_owner: architect`
  - `review_dependencies` (e.g., planner for complex scope)
- Required sections:
  - Overview
  - Architecture
  - Interface/API contracts
  - Data model implications
  - Security considerations
  - Test strategy
  - Rollout/rollback
  - Risks
