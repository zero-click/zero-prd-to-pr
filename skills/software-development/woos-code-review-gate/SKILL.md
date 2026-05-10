---
name: woos-code-review-gate
description: Independent code/security review gate for Hermes workflow. Uses ECC code-reviewer and security-reviewer where applicable.
version: 1.1.0
author: Hermes ECC Profile
license: MIT
---

# Woosley Code Review Gate

## Purpose

Enforce independent review before PR readiness.

## Required reviewers

- Always: ECC `code-reviewer`
- Security-sensitive scope: ECC `security-reviewer` (additional)

## Required Invocation (hard gate)

- MUST invoke `code-reviewer` for every code change.
- MUST invoke `security-reviewer` when scope includes auth, input handling, secrets, payments, external callbacks, or sensitive data flows.
- If required reviewer is not invoked, return `NOT_RUN` and stop.
- If required reviewer is unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or non-whitelisted reviewer.

## Contract

- Input: current diff + linked artifacts (PRD/design/capability)
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output content: blocking and non-blocking findings
- Output fields (required):
  - `reviewers_used`
  - `code_reviewer_status`
  - `security_reviewer_status` (when required)
  - `blocking_findings`

Gate passes only when all required reviewers are clear.
