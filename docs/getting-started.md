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

The kit includes `knowledge-base` for project memory and
`human-readable-communication` for clear explanations, plans, summaries, and
reports. The communication skill follows the user's language, including Thai
and mixed-language messages, and preserves technical names and meaning.

## 3. Start the knowledge base

The `knowledge/_example/` pages are fictional scaffolding. Remove or replace them before treating this repository as persistent memory. Create one domain folder per coherent subject, add an `index.md`, and link it from `knowledge/main.md`. Keep `_template/` as reusable scaffolding; neither templates nor examples are project facts.

For external material, preserve the original unchanged under the domain's `sources/` folder before writing a source-backed summary under `derived/`. Put internal decisions and discoveries under `self/`. If the project domain is unclear, hold the original under `knowledge/inbox/sources/` until it is triaged.

Substantive context from the user, including narrative updates, should trigger the `knowledge-base` skill and a reusable knowledge update when needed; a separate request to save is unnecessary. Preserve tentative statements as tentative, honor an explicit request not to save, and keep temporary task status out of durable knowledge.

Before finishing substantive or non-trivial work, assess whether to update existing knowledge, consolidate it, create a distinct topic, or skip a write. Check affected references and contradictions, log actual durable changes in `knowledge/log.md`, and run a knowledge linter if one is available. Report saved locations or a concrete blocker when capture was needed.

## 4. Add environment variables only when needed

`.env.example` is intentionally generic. Add only the names and safe placeholder values needed by your projects. Never put real keys or tokens in it. Keep real `.env` files local; they are ignored by Git.

For authorized credential use, load only required allowlisted variables into process memory, prefer existing process variables, and never evaluate `.env` as code or pass secrets as command-line arguments. Follow the full sensitive-configuration rules in `AGENTS.md`.

## 5. Grow scripts and skills deliberately

Keep shared setup scripts in `scripts/`. Group project scripts under `scripts/<topic>/`, keep helpers beside their callers, and document entry points in `scripts/README.md`. Update imports, repository-root resolution, examples, and knowledge references when moving scripts. Create a skill under `.codex/skills/<skill-name>/SKILL.md` only when a repeatable workflow benefits from dedicated instructions. Maintain skills in the canonical folder; the compatibility junctions are not separate copies.
