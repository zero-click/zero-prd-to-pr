# Product Design Workflow

A skill-driven product design pipeline for AI coding agents. Takes a raw idea from capture through research, PRD, review gates, and delivers engineering-ready PRD/supporting artifacts.

## Purpose

This workflow enforces structured product thinking before code is written. It ensures:

- **WHAT/WHY** is fully defined before engineering decides **HOW**
- Every decision is documented and traceable (roadmap → requirements → PRD → coding agent)
- Quality gates prevent weak specs from reaching engineering
- Cross-feature consistency is validated before build starts

## Quick Start

1. Start a conversation with the agent and describe your idea
2. The agent activates `woos-idea-to-design` (entry point skill)
3. Follow the guided flow — the agent handles orchestration, sub-agent dispatch, and gating

**Trigger phrases:** "I have an idea for...", "let's build...", "design this feature", "start V1"

---

## Workflow Overview

```
Raw Idea
  │
  ▼
┌─────────────────────────────────────────────────────────┐
│ Phase 1: Capture (woos-idea-capture)                    │
│ Output: ideas/<slug>/00-idea-capture.md                 │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Trivially simple?  │
              └──┬──────────────┬───┘
            Yes  │              │  No
                 ▼              ▼
        User confirms    ┌────────────────────────────────┐
        "Lite mode"      │ Phase 2: Discovery             │
                │        │ (woos-product-discovery)        │
                │        │                                 │
                │        │  1. Problem Validation          │
                │        │  2. Market/Competitive Research │
                │        │  3. Roadmap → Review Gate       │
                │        │  4. Architecture → Review Gate  │
                │        └───────────────┬────────────────┘
                │                        │
                │             🚦 Human Approval Gate
                │             (mandatory before PRD)
                │                        │
                │        Mode inferred from roadmap:
                │        • Single feature → Standard
                │        • Multi-feature → Strict
                │                        │
  ┌─────────────▼────────────────────────▼────────────────┐
  │ Phase 3: Product Design Flow                          │
  │ (woos-product-design-flow)                            │
  │                                                       │
  │  Step 1:   Select Version Scope                       │
  │  Step 1.5: Feature Dependency Analysis         [S]    │
  │                                                       │
  │  ┌─ Per Feature (in dependency order) ────────────┐   │
  │  │  Step 2:   Requirement Contract       (+iface) │   │
  │  │  Step 3:   PRD Authoring              (+iface) │   │
  │  │  Step 4:   PRD Review Gate             (+iface) │   │
  │  │  Step 5:   UI Brief                     [S]    │   │
  │  │  Step 5R:  UI Brief Review              [S]    │   │
  │  │  Step 6:   Analyze Gate           [S] (+iface) │   │
  │  │  Step 6.5: Interface Summary Extraction [S]    │   │
  │  │  Step 7:   Integration Gate (incremental) [S]  │   │
  │  └───────────────────────────────────────────────┘   │
  │                                                       │
  └───────────────────────────┬───────────────────────────┘
                             │
                 ┌────────────▼────────────┐
                 │  Engineering Delivery   │
                 │  → Engineering Stage    │
                 └─────────────────────────┘

  [S] = Strict mode only
  (+iface) = receives upstream interface summaries when dependencies exist
```

---

## Phases

### Phase 1 — Capture

| | |
|---|---|
| **Skill** | `woos-idea-capture` |
| **What** | Guided interview to structure raw idea into product intent |
| **Output** | `ideas/<slug>/00-idea-capture.md` |
| **Next** | Trivial → Lite (user confirms); otherwise → Discovery |

### Phase 2 — Discovery

| | |
|---|---|
| **Skill** | `woos-product-discovery` (orchestrator) |
| **What** | Research problem space, produce roadmap + architecture |
| **Output** | `docs/product/<project>-roadmap.md` + `docs/product/<project>-architecture.md` |
| **Next** | 🚦 Human approval → Phase 3 |

Discovery dispatches 4 sub-skills in sequence:

| Step | Skill | Output |
|------|-------|--------|
| 1 | `woos-problem-validation` | Verdict appended to idea capture |
| 2 | `woos-product-research` | `docs/research/<topic>.md` |
| 3 + 3R | `woos-roadmap-authoring` → `woos-roadmap-review-gate` | Roadmap + review |
| 4 + 4R | `woos-architecture-overview` → `woos-architecture-review-gate` | Architecture + review |

### Phase 3 — Design Flow

| | |
|---|---|
| **Skill** | `woos-product-design-flow` (orchestrator) |
| **What** | Turn roadmap into reviewed PRDs + interface summaries per feature |
| **Final output** | `docs/prd/<version>/<feature-id>.md` + `docs/prd/<version>/<feature-id>-interface.md` |

| Step | Skill | What It Does |
|------|-------|--------------|
| 1 | (orchestrator) | Select version scope, confirm boundaries |
| 1.5 | (orchestrator) | Dependency analysis — determine feature execution order + interface pass-through plan |
| 2 | `woos-requirement-contract` | Per-feature requirements with P0/P1/P2 cut-line (+upstream interface alignment) |
| 3 | `woos-prd-authoring` | Full PRD from ranked requirements (+upstream interface alignment) |
| 4 | `woos-product-prd-review-gate` | Isolated PRD review → `PASS` / `REQUEST_CHANGES` (+upstream interface check) |
| 5 | `woos-ui-design-brief` | UI direction, screens, interaction patterns |
| 5R | `woos-ui-brief-review` | Isolated UI review → `PASS` / `REQUEST_CHANGES` |
| 6 | `woos-prd-consistency-audit` | Script extraction + semantic audit (+upstream interface check) |
| 6.5 | (orchestrator) | Interface summary extraction — shared concepts for downstream features |
| 7 | `woos-version-integration-audit` | Incremental cross-feature conflict detection (after each 2nd+ feature) |

---

## Execution Modes

| Mode | When | Steps | Gates |
|------|------|-------|-------|
| **Lite** | Trivial, < 2 days | Requirements → PRD | None |
| **Standard** | Single feature, moderate | 1 → 2 → 3 → 4 | PRD Review |
| **Strict** | Multi-feature, UX-heavy, high-risk | 1 → 1.5 → [per feature: 2 → 3 → 4 → 5 → 5R → 6 → 6.5 → 7(incremental)] | All |

Mode is determined automatically:
1. After Capture: trivial → Lite (user confirms)
2. After Discovery:
   - single feature, normal risk → Standard
   - multi-feature, or single-feature UX-heavy / high-risk / high-uncertainty → Strict

---

## Enforcement Rules (P0–P7)

| Rule | Principle |
|------|-----------|
| **P0** | Explicit step dispatch — state skill, inputs, output before each step |
| **P1** | Orchestrator does NOT author — only Steps 1, 1.5, and 6.5 are direct |
| **P2** | No merging or skipping — each step has verified output |
| **P3** | Output validation — file must exist with expected structure/verdict |
| **P4** | No self-review — fresh skill in fresh context for every gate |
| **P5** | Subagent isolation — Steps 4, 5R, 6, 7 run in isolated contexts |
| **P6** | Fix propagation — any fix must grep + sync all affected docs globally |
| **P7** | Upstream interface awareness — downstream features receive upstream interface summaries |

---

## Design Principles

1. **Product defines WHAT/WHY, Engineering decides HOW** — no implementation details in PRD
2. **File-based state** — all artifacts are human-readable markdown, git-trackable
3. **Independent reviewers** — fresh sub-agent context for every review gate
4. **Template-driven** — mandatory structures with `[NEEDS CLARIFICATION: ...]` markers
5. **Human-in-the-loop** — mandatory approval gate between Discovery and Design Flow
6. **Bidirectional feedback** — engineering issues DCR (Design Change Requests) back to product

---

## Knowledge Architecture

Adapted from the [BMAD](https://github.com/bmad-agent/bmad-agent) methodology. Three types of domain knowledge are injected into sub-agent steps:

### Personas

| Persona | Used In | Purpose |
|---------|---------|---------|
| **PM (John)** | Steps 2, 3 | Product thinking — shapes requirements and PRD from user-value perspective |
| **UX Designer (Sally)** | Steps 5, 5R | Interaction patterns, accessibility, information hierarchy |
| **PRD Validator** | Discovery 3R, Step 4 | Critical reviewer — gaps, contradictions, untestable criteria |

### Frameworks

| Framework | Stage | Purpose |
|-----------|-------|---------|
| `framework-prd.md` | Design Flow | Shape → extract → validate cycle for requirements/PRD |
| `framework-ux-design.md` | Design Flow | Dual-spine model, elicit-not-impose |
| `framework-ux-validate.md` | Design Flow | UI brief review methodology |
| `framework-epics-and-stories.md` | Design Flow | User-value grouping, FR coverage tracking |
| `framework-implementation-readiness.md` | Design Flow | Four-layer validation, traceability matrix |
| `framework-market-research.md` | Discovery | Multi-angle research, synthesis |
| `framework-competitive-analysis.md` | Discovery | SWOT, differentiation strategy |
| `framework-customer-pain-points.md` | Discovery | Pain categories, prioritization matrix |
| `framework-create-prd.md` | Discovery | Versioned roadmap discipline |
| `framework-create-architecture.md` | Discovery | Requirements extraction, scale assessment |
| `framework-architecture-validation.md` | Discovery | Coherence, coverage, readiness validation |

### Templates

| Template | Location | Purpose |
|----------|----------|---------|
| `template-prd-template.md` | `woos-prd-authoring` | PRD section structure |
| `template-prd-validation-checklist.md` | `woos-product-prd-review-gate` | Review output format |
| `requirements-template.md` | `woos-requirement-contract` | Requirements contract structure |
