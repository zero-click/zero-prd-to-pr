---
name: woos-setup-rules
description: Setup project rule routing for Hermes by generating `AGENTS.md` from imported rule packs in profile `rules/ecc-import`.
version: 1.0.0
author: Hermes Profile
license: MIT
---

# Woos Setup Rules

## Purpose

Configure project-level rule routing so Hermes can apply language-appropriate rules consistently.

## When to Use

- New repository onboarding
- Profile upgrade after rule-pack sync
- Mixed-language project setup
- Rule routing drift or ambiguity

## Preconditions

- Coding profile has imported rules under: `~/.hermes/profiles/coding/rules/ecc-import/`
- If missing, run installer with rules sync enabled.

## Workflow

1. Detect active languages in the current repository.
2. Select rule packs:
   - Always include `common`.
   - Include language packs only when corresponding file types exist.
3. Resolve profile rules root (default: `~/.hermes/profiles/coding/rules/ecc-import`).
4. Expand selected packs into concrete rule file paths under the profile rules root.
5. Create or update project `AGENTS.md` with executable routing instructions:
   - Explicitly instruct agent to read listed rule files before coding
   - Include real file paths (profile location), not repo-relative placeholders
   - Keep mixed-language precedence policy deterministic
6. Ensure every listed file actually exists; otherwise return `REQUEST_CHANGES`.

## Output Contract

Return:

- `status`: `PASS` | `REQUEST_CHANGES` | `BLOCKED`
- `routing_file`: path of updated `AGENTS.md`
- `rule_packs_used`: list of selected packs
- `rule_files_loaded`: concrete rule file paths inserted into `AGENTS.md`
- `notes`: any unresolved ambiguity

## Recommended `AGENTS.md` Routing Template

```markdown
## Rule Routing

Before starting coding work in this project, read these rule files first:

- `~/.hermes/profiles/coding/rules/ecc-import/common/coding-style.md`
- `~/.hermes/profiles/coding/rules/ecc-import/common/testing.md`
- `~/.hermes/profiles/coding/rules/ecc-import/common/security.md`
- `~/.hermes/profiles/coding/rules/ecc-import/common/code-review.md`
- `~/.hermes/profiles/coding/rules/ecc-import/python/coding-style.md`
- `~/.hermes/profiles/coding/rules/ecc-import/python/testing.md`

Routing policy:

- Always include `common/*` rules.
- Add language pack files based on detected languages in this repo.
- For mixed-language interface changes, apply the stricter rule at boundaries.
```
