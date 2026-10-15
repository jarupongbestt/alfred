---
type: self
description: Assistant starter setup and knowledge workflow onboarding
source_refs:
  - kind: local
    target: ../../AGENTS.md
updated: "2026-10-15"
status: current
---

# Getting Started

## 1. Personalize the working agreement

Edit `AGENTS.md` to describe your preferences, boundaries, and repository-specific rules. Keep personal profile information in a dedicated knowledge domain rather than embedding a biography in global instructions.

## 2. Set up skill compatibility links

The canonical skill files live in `.codex/skills/`. On Windows, run from the repository root:

```powershell
.\scripts\setup-skills-links.ps1
```

This creates `.agents/skills` and `.claude/skills` as junctions to `.codex/skills`. It refuses to replace existing paths that are not the expected junctions.

On macOS/Linux, create symbolic links from the repository root:

```sh
mkdir -p .agents .claude
ln -s ../.codex/skills .agents/skills
ln -s ../.codex/skills .claude/skills
```

If these links already exist and point to `.codex/skills`, keep them. Do not
replace an existing unrelated directory. Maintain skills in the canonical
folder only.

The kit includes `knowledge-base` and `documentation-and-adrs` for project memory,
evidence-backed documentation and decision lifecycle, and
`human-readable-communication` for clear explanations, plans, summaries, and
reports. The communication skill follows the user's language, including Thai
and mixed-language messages, and preserves technical names and meaning.

## 3. Start the knowledge base

The `knowledge/_example/` pages are explicitly classified fictional scaffolding.
Keep them separate from the real domains listed in `knowledge/main.md`. Create
one domain folder per coherent subject, add an `index.md` with Navigation Hints,
and link it from `knowledge/main.md`. Register its index and raw source folders
in `knowledge/validation-layout.yaml` before running validation. Use `_template/` for typed topic metadata and
ADR structure; neither templates nor examples are project facts.

For external material, preserve the original unchanged under the domain's `sources/` folder before writing a source-backed summary under `derived/`. Put internal decisions and discoveries under `self/`. If the project domain is unclear, hold the original under `knowledge/inbox/sources/` until it is triaged.

Substantive context from the user, including narrative updates, should trigger the `knowledge-base` skill and a reusable knowledge update when needed; a separate request to save is unnecessary. Preserve tentative statements as tentative, honor an explicit request not to save, and keep temporary task status out of durable knowledge.

Before finishing substantive or non-trivial work, load both knowledge methods and
assess whether to update existing knowledge, consolidate it, create a distinct
topic, or skip a write. Maintain required metadata, typed evidence, Navigation Hints
and actual structured log entries. Run `sh scripts/knowledge/check.sh` after the
final write, including the log, and return the
[Knowledge Outcome](contracts.md#knowledge-outcome). Required failed or
unavailable checks are blocked. The [adoption map](adoption.md) records
the complete knowledge-only scope, source versions, protections and native paths.

## 4. Add environment variables only when needed

`.env.example` is intentionally generic. Add only the names and safe placeholder values needed by your projects. Never put real keys or tokens in it. Keep real `.env` files local; they are ignored by Git.

For authorized credential use, load only required allowlisted variables into process memory, prefer existing process variables, and never evaluate `.env` as code or pass secrets as command-line arguments. Follow the full sensitive-configuration rules in `AGENTS.md`.

## 5. Grow scripts and skills deliberately

Keep shared setup scripts in `scripts/`. Group project scripts under `scripts/<topic>/`, keep helpers beside their callers, and document entry points in `scripts/README.md`. Update imports, repository-root resolution, examples, and knowledge references when moving scripts. Create a skill under `.codex/skills/<skill-name>/SKILL.md` only when a repeatable workflow benefits from dedicated instructions. Maintain skills in the canonical folder; the compatibility junctions are not separate copies.
