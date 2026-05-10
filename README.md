# hermes-ecc-profile

[中文说明 / Chinese README](./README.zh-CN.md)

Skill-first coding profile for Hermes, with:

- local workflow/gate skills (`woos-*`)
- imported ECC skills (`skills/ecc-import/*`)
- agent-adapter skills (`skills/ecc-agent-skills/*`)

## What this profile installs

1. Local workflow skills:
   - `woos-development-workflow`
   - `woos-prd-authoring`
   - `woos-prd-review-gate`
   - `woos-feature-design`
   - `woos-design-review-gate`
   - `woos-code-review-gate`
   - `woos-pr-readiness`
2. Imported skills:
   - `git-workflow`
   - `search-first`
   - `dmux-workflows`
   - `product-capability`
   - `tdd-workflow`
   - `coding-standards`
   - `verification-loop`
3. Agent-adapter skills:
   - `planner`
   - `architect`
   - `code-reviewer`
   - `security-reviewer`

## Install

```bash
cd /path/to/hermes-ecc-profile
./install-profile.sh
```

The installer will prompt for local ECC repo path.

Optional:

```bash
./install-profile.sh --ecc-path /path/to/ecc --profile-root ~/.hermes/profiles/coding --install-soul
```

Installed layout (default profile root: `~/.hermes/profiles/coding`):

- `skills/software-development/*` (local workflow skills)
- `skills/ecc-import/*` (imported ECC skills)
- `skills/ecc-agent-skills/*` (agent adapters)
- `SOUL.md` (only if `--install-soul`)

## Upgrade flow (ECC changes)

Agent-adapter skills include source tracking fields:

- `ecc_source_repo`
- `ecc_source_path`
- `ecc_source_commit`

When ECC updates, compare the source commit in each adapter skill with current ECC git history. If changed, re-run adapter conversion.

## Rules in Hermes

Hermes does not use an ECC-style standalone `rules/` loader by default.  
Use project context files for rules routing:

- `.hermes.md` / `HERMES.md` (preferred)
- `AGENTS.md`
- `.cursorrules` or `.cursor/rules/*.mdc`

Put global principles in `SOUL.md`, and language/project-specific rules in project context files.
