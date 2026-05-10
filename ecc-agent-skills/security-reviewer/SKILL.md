---
name: security-reviewer
description: Security vulnerability review skill adapted from ECC security-reviewer agent.
origin: ECC-agent-adapter
ecc_source_repo: affaan-m/everything-claude-code
ecc_source_path: agents/security-reviewer.md
ecc_source_commit: 34d8bf806428c8b1a6d9929a54f76c5667420a42
---

# Security Reviewer

## When to Use

- For auth, secrets, input handling, payments, callbacks, or sensitive data flows
- Before PR readiness for security-sensitive scope

## Input Contract

- Current diff or changed files
- Scope description for threat context
- Any security requirements/policies available in repo

## Workflow

1. Check trust boundaries and input validation paths.
2. Review for injection, authz/authn gaps, secret exposure, unsafe external calls, and sensitive logging.
3. Flag exploitable issues with severity and remediation guidance.
4. Return gate-compatible verdict.

## Output Contract

```text
STATUS: PASS | REQUEST_CHANGES | NOT_RUN | BLOCKED
SUMMARY: security verdict
BLOCKING_FINDINGS:
- critical/high findings with remediation
NON_BLOCKING_FINDINGS:
- medium/low improvements
```

Rules:

- `PASS` only when no critical/high unresolved findings remain.
- `REQUEST_CHANGES` when blocking security findings exist.
