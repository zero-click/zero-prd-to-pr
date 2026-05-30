# UX Design Framework

## Purpose

Transform product requirements into a practical UI/UX design brief that defines what the interface should look, feel, and behave like. Capture the user's vision through guided discovery, not impose design decisions.

## Input

- PRD (functional requirements, user journeys, personas)
- System architecture (to understand technical constraints on UI)
- Any existing UI references, brand guidelines, or inspiration from user

## Methodology

### 1. Core Principle: Elicit, Never Impose

Your role is to **capture** the user's/product's design intent, not to author your own vision:
- Ask open-ended questions ("tell me about X") over multiple choice
- When you find yourself proposing specific UI patterns unprompted — stop
- Render options only when seeing alternatives helps the user decide
- Infer-and-confirm is fine ("I'm assuming mobile-first — right?")

### 2. Dual-Spine Model

Create two complementary documents:

**DESIGN.md — Visual Identity Spine**
- Brand & Style (personality, mood)
- Colors (primary, secondary, semantic, dark mode)
- Typography (scale, hierarchy, fonts)
- Layout (grid, spacing, breakpoints)
- Elevation & Depth (shadows, layers)
- Shapes (border radius, icons style)
- Component Tokens (buttons, inputs, cards — visual properties)
- Do's and Don'ts (visual rules)

**EXPERIENCE.md — Behavioral Spine**
- Foundation (form-factor, UI system/framework)
- Information Architecture (navigation, page hierarchy, surface inventory)
- Voice & Tone (copy style, error messages, empty states)
- Component Behavior (interactions, animations, transitions)
- States (loading, empty, error, success, disabled)
- Interactions (gestures, keyboard shortcuts, drag-and-drop)
- Accessibility (WCAG level, screen reader, contrast)
- Key Flows (primary user journeys with screen-by-screen detail)

### 3. Surface Closure Rule

The design is complete when:
- Every user need maps to a screen/surface through a journey
- Every surface has at least one journey landing there
- No orphan screens (surfaces that exist but no journey reaches them)
- No dead-end journeys (flows that need a surface that doesn't exist)

### 4. Named-Protagonist Journeys

Structure user flows around real people in real scenarios:
- Give the protagonist a name and context (Mary, mom of three; Skeeter on Android)
- Number each step
- Include the "climax beat" — the moment of value delivery
- Note emotional state at each step (frustrated → curious → satisfied)

## Output Structure

```markdown
# UI/UX Design Brief — [Feature/Product]

## Design Direction
[Overall visual and interaction philosophy in 2-3 sentences]

## DESIGN.md (Visual Identity)
### Brand & Style
[Personality, mood, inspirations]

### Colors
| Role | Value | Usage |
|------|-------|-------|

### Typography
[Scale, hierarchy, font choices]

### Layout
[Grid system, spacing scale, breakpoints]

### Components
[Key component visual specifications]

## EXPERIENCE.md (Behavior)
### Information Architecture
[Navigation structure, page hierarchy]

### Key Flows
#### Flow 1: [Protagonist] — [Scenario]
1. **[Screen/Surface]** — [What user sees, what they do]
2. **[Screen/Surface]** — [Transition, state change]
3. **[Screen/Surface]** — [Climax: value delivered]

### States
[Loading, empty, error, success patterns]

### Accessibility
[WCAG level, key considerations]

## Surface Inventory
| Surface | Purpose | Reached By |
|---------|---------|-----------|

## Open Design Questions
[Decisions that need user/stakeholder input]
```

## Quality Criteria

- Design decisions traced back to user needs (not arbitrary aesthetic choices)
- Surface closure: every need has a surface, every surface has a journey
- Accessibility considered from the start, not bolted on
- Component specifications are design-system-ready (not vague "nice button")
- Key flows cover happy path AND error/edge states
- Visual identity is consistent (no conflicting style directions)
