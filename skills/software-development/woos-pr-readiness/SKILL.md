---
name: woos-pr-readiness
description: Final pre-PR readiness gate for Hermes workflow. Confirms diff quality, verification visibility, and commit/PR discipline.
version: 1.1.0
author: Hermes ECC Profile
license: MIT
---

# Woosley PR Readiness

## Purpose

Confirm work is ready for commit/PR handoff.

## Required Invocation (hard gate)

- MUST invoke ECC `verification-loop` first.
- If `verification-loop` is not invoked, return `NOT_RUN` and stop.
- If unavailable, return `BLOCKED` and stop.
- Do not replace with manual "looks good" checks only.

## Contract

- Check git diff/status is understood and scoped
- Check verification outcomes are explicitly reported
- Check conventional commit and PR test plan readiness
- Return `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output fields (required):
  - `verification_skill_used: verification-loop`
  - `verification_summary`
