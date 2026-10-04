# Personal Assistant Starter Kit

A project-neutral starter for an assistant that can work across your projects and maintain useful, traceable knowledge over time.

Includes three skills:

- [anti-overengineering](.codex/skills/anti-overengineering/SKILL.md) — keep work proportional to the requested outcome.
- [knowledge-base](.codex/skills/knowledge-base/SKILL.md) — capture, navigate, and curate reusable project knowledge.
- [human-readable-communication](.codex/skills/human-readable-communication/SKILL.md) — clear explanations and reports in simple English, Thai, or the user's language.

Starter source: [assistant-starter-kit](https://github.com/jarupong-mts/assistant-starter-kit/tree/f403cb6227efd15d0bb4c2b5d0c8bef0935b69d0), commit `f403cb6227efd15d0bb4c2b5d0c8bef0935b69d0`, accessed 2026-10-03.

## Get started

1. Read [AGENTS.md](AGENTS.md) and personalize the working agreement.
2. Read [docs/getting-started.md](docs/getting-started.md).
3. Add your own knowledge domains under `knowledge/`; the included `_example/` pages are fictional scaffolding.
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
- `docs/` — onboarding and maintenance guidance.
- `.env.example` — commented guide only; each user defines their own variables.

The knowledge examples are fictional scaffolding. Replace them before relying on them; do not add personal facts, private project documents, or credentials to this starter.

## Template scope

This repository contains the starter instructions, reusable skills, knowledge templates, fictional examples, and the shared setup script. Personal project knowledge, knowledge history, project scripts, research documents, and generated outputs are excluded.
