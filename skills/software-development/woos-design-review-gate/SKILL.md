---
name: woos-design-review-gate
description: Independent feature design review gate for Hermes workflow. Uses ECC architect review and returns PASS or REQUEST_CHANGES.
version: 1.1.0
author: Hermes ECC Profile
license: MIT
---

# Woosley Design Review Gate

## Purpose

Run a strict design review gate before coding starts.

## Required reviewer

- ECC `architect`

## Required Invocation (hard gate)

- MUST invoke `architect`.
- If not invoked, return `NOT_RUN` and stop.
- If unavailable, return `BLOCKED` and stop.
- Do not replace with self-review or non-whitelisted reviewer.

## Contract

- Input: design doc path + linked PRD/capability artifacts
- Output status: `PASS` | `REQUEST_CHANGES` | `NOT_RUN` | `BLOCKED`
- Output content: concrete mismatches, risks, and required revisions
- Output fields (required):
  - `reviewer_used: architect`
  - `blocking_findings`
