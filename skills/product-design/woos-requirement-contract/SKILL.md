---
name: woos-requirement-contract
description: Produce the per-feature requirements contract used as the input to priority ranking and PRD authoring.
version: 1.0.0
author: Hermes Profile
license: MIT
metadata:
  hermes:
    tags: [product, requirements, authoring, design-flow]
    related_skills:
      - woos-product-design-flow
      - woos-prd-authoring
---

# Requirement Contract

## Purpose

Turn one selected roadmap feature into a structured requirements file before any ranking or PRD work begins.

## Required Load Set (mandatory)

- `references/framework-prd.md`
- `templates/requirements-template.md`
- **Standard / Strict:** `docs/product/<project>-roadmap.md`
- **Lite:** the idea capture file (`ideas/<slug>.md` for Quick Note, or `ideas/<slug>/00-idea-capture.md` for Guided Interview) in place of the roadmap

If the required input file for the active mode is not loaded, return `BLOCKED`. In Lite mode the absence of `docs/product/<project>-roadmap.md` is expected and is not a BLOCK condition; the orchestrator MUST tell this skill which mode it is running in.

## Conditional Load Set (upstream dependencies)

When the orchestrator identifies upstream dependencies (via Step 1.5), also load:

- `docs/prd/<version>/<upstream-feature-id>-interface.md` for each declared upstream dependency

These interface summaries define shared terminology, enums, data models, and API surfaces that this feature MUST align with. When writing requirements that reference shared concepts, use the exact names and definitions from the upstream interface summary.

## Output

- `docs/prd/<version>/<feature-id>-requirements.md`

## Required Sections

1. `## Problem Statement`
2. `## Goals`
3. `## User Stories`
4. `## Non-Goals`
5. `## Constraints`
6. `## Risks & Unknowns`
7. `## Priority Ranking`

## Authoring Rules

- Follow the template structure exactly
- Keep the file scoped to one feature only
- Mark unresolved items as `[NEEDS CLARIFICATION: ...]`
- Do not fold this output into the PRD
- Include an explicit `P0 / P1 / P2` ranking and ship cut-line in `## Priority Ranking`
