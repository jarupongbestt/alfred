# Personal Assistant Starter Kit

A project-neutral starter for an assistant that can work across your projects and maintain useful, traceable knowledge over time.

Includes these skills:

- [knowledge-base](.codex/skills/knowledge-base/SKILL.md) — capture, navigate, and curate reusable project knowledge.
- [documentation-and-adrs](.codex/skills/documentation-and-adrs/SKILL.md) — preserve consequential decisions, lifecycle history, and human decision evidence.
- [anti-overengineering](.codex/skills/anti-overengineering/SKILL.md) — keep the approach proportional while completing required behavior.
- [human-readable-communication](.codex/skills/human-readable-communication/SKILL.md) — clear explanations and reports in simple English, Thai, or the user's language.

Starter source: [assistant-starter-kit](https://github.com/jarupong-mts/assistant-starter-kit/tree/f403cb6227efd15d0bb4c2b5d0c8bef0935b69d0), commit `f403cb6227efd15d0bb4c2b5d0c8bef0935b69d0`, accessed 2026-10-03.

## Get started

1. Read [AGENTS.md](AGENTS.md) and personalize the working agreement.
2. Read [knowledge/_system/getting-started.md](knowledge/_system/getting-started.md).
3. Read `knowledge/main.md` for real project domains. Only `_example/` and `_template/` are scaffolding.
4. Add project-specific environment variable names to `.env.example` when needed. Never put real secrets there.
5. Add reusable workflow skills under `.codex/skills/`.
6. On Windows, run `./scripts/setup-skills-links.ps1` after cloning to create `.agents/skills` and `.claude/skills` junctions to `.codex/skills`.

## Layout

- `AGENTS.md` — canonical assistant and repository instructions.
- `CLAUDE.md` — imports `AGENTS.md` for Claude Code.
- `.codex/skills/` — canonical skill files.
- `.agents/skills` and `.claude/skills` — compatibility links to the canonical skill folder; junctions on Windows and symbolic links on macOS/Linux.
- `knowledge/` — navigation, reusable templates, and clearly labeled examples.
- `scripts/` — shared setup and project scripts.
- `docs/` — project concepts, PRDs, design specs, and deliverable documentation.
- `knowledge/_system/` — assistant setup and knowledge-system operating guidance.
- `.env.example` — commented guide only; each user defines their own variables.

The pages under `knowledge/_example/` are fictional scaffolding; real project
context belongs in the domains listed by `knowledge/main.md`. Keep credentials
out of knowledge. The complete knowledge-management capability is mapped to the
pinned upstream version in [the adoption record](knowledge/_system/adoption.md).
Run `sh scripts/knowledge/check.sh` after the final knowledge write.

## Keep project memory local

This distribution contains the working agreement, skills, documentation, scripts,
reusable templates, fictional examples, and the pinned public upstream reference.
Project-domain navigation starts empty; the action log records starter maintenance only. `.gitignore` excludes new
real knowledge domains, other inbox sources, and generated outputs by default.
Review `git diff --cached` before publishing. Navigation, logs, and other already
tracked files can still contain real context after use; review their contents too.
