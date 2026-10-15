# Assistant Working Agreement

This repository is durable working context for an assistant. Treat `knowledge/`
as curated memory, not as a conversation transcript or temporary task state.

## Communication

Use the user's language, natural language mix, and preferred tone. Lead with
the outcome or action, use familiar words and clear actors, and keep each
paragraph focused. Preserve facts, evidence, uncertainty, conditions, and
obligations. Keep technical names, code, paths, commands, and quoted text exact.

For long or complex explanations, plans, summaries, and reports, use
[human-readable-communication](.codex/skills/human-readable-communication/SKILL.md).
This skill supports simple English, Thai, and mixed-language writing.

## Startup

At the beginning of every task:

1. Read [knowledge/main.md](knowledge/main.md).
2. Read and apply [anti-overengineering](.codex/skills/anti-overengineering/SKILL.md)
   before planning or acting.
3. Identify the relevant project domain and read its `index.md` Navigation Hints.
4. Read the relevant topic and focused `source_refs` before broader searches.
   If navigation is absent, stale, contradictory, or insufficient, record the
   evidence and reason for a narrow expansion. For knowledge-system maintenance,
   use [the adoption map](docs/knowledge/adoption.md) instead of inventing a domain.
5. Read [knowledge/log.md](knowledge/log.md) only when history, contradictions,
   recurring failures, prior decisions, or lint context matter.

`knowledge/_example/` and `knowledge/_template/` are non-authoritative
scaffolding. If `knowledge/domain/` exists as a structural example, it is also
non-authoritative. Create real project domains directly under `knowledge/`.

Use the `knowledge-base` skill when creating, changing, reconciling, or
validating durable knowledge. Its canonical path is
`.codex/skills/knowledge-base/SKILL.md`.

## Knowledge-management adoption scope

The selected capability from
[agent-harness-concept](https://github.com/jarupongbestt/agent-harness-concept)
is complete knowledge management. Include or translate every applicable required
contract and supporting asset into this project's existing native paths;
do not silently reduce it to selected recommendations. Distinguish mandatory
behavior from upstream optional implementations and illustrative assets.
Agent orchestration, model assignments, and run-state storage are outside this
adoption. Verify conformance against a pinned upstream revision before claiming
that the implementation is complete; recording this scope alone is not proof.

The pinned baseline and required asset mapping are maintained in
[docs/knowledge/adoption.md](docs/knowledge/adoption.md). For durable-learning
assessment, load both `knowledge-base` and
[documentation-and-adrs](.codex/skills/documentation-and-adrs/SKILL.md).
Follow the [metadata, log, and Knowledge Outcome contracts](docs/knowledge/contracts.md).
After the final knowledge write, including navigation and log edits, run
`sh scripts/knowledge/check.sh`. Required failed or unavailable checks are
`blocked`; an earlier pass does not certify later writes. Check results do not
prove claim truth or human acceptance. Preserve the target category protections
and explicit source re-sync rules recorded in the adoption map.

## Knowledge layout

```text
knowledge/
├── main.md                 # mandatory startup navigation
├── log.md                  # concise knowledge action log
├── <domain>/               # real project domains
│   ├── index.md            # domain navigation
│   ├── self/               # internal discoveries, decisions, constraints
│   ├── derived/            # faithful source-backed compilations
│   └── sources/            # unchanged external material
├── _template/              # copyable topic templates
└── _example/               # fictional examples, not project facts
```

## Automatic knowledge capture

Substantive project context supplied by the user is an instruction to maintain
project memory, even when phrased as a narrative or progress update. Do not
require a separate "save to knowledge" request. Use the `knowledge-base` skill
and capture reusable additions or corrections before ending the turn:
workflows, system roles and relationships, business rules, scope, decisions,
constraints, definitions, and recurring failure patterns.

General questions, hypothetical brainstorming, status requests, and temporary
task progress normally need no internal or derived knowledge change unless they
establish reusable project context. Judge the substance rather than message
length or whether it contains a question. Raw-source intake still applies to
supplied files and external artifacts. Honor an explicit request not to save.

Record the user's stated understanding as such; preserve tentative plans and
unresolved differences with their evidence instead of promoting them to
confirmed facts. Prefer updating the existing primary topic over creating a
page for each conversation. Follow the task-domain gate in `knowledge/main.md`
when routing the update; uncertainty about one detail need not block capture of
the supported details. Briefly report the saved location or a concrete blocker
at completion.

## Write rules

- Optimize knowledge for accurate answers and easy retrieval, not the amount
  stored. A task may correctly produce no knowledge change.
- Before writing, read related knowledge and identify the reusable gap. Prefer
  improving or consolidating existing pages; create a page only for a distinct
  scope that existing pages cannot reasonably cover.
- Give each topic a clear primary home and link to it instead of repeating its
  explanation. Preserve meaningful differences in scope, version, and context.
- When work exposes duplication, conflicting guidance, stale claims, or poor
  navigation, improve the affected area within the authorized scope. Broader
  reorganization needs evidence of a broader problem.
- Preserve user-provided files and external artifacts unchanged under the
  appropriate domain's `sources/` before extracting or deriving knowledge.
- A derived page must name or link to the exact source path or URL, retain its
  provenance, and record the received or accessed date. If the domain is
  unresolved, hold supplied files under `knowledge/inbox/sources/` and defer
  derivation until triage.
- Never edit or silently replace a raw source. A new version is a new source
  artifact; record its relationship in the derived page or index.
- Put internal discoveries, decisions, constraints, and gotchas in `self/`.
- Put faithful, provenance-backed external knowledge in `derived/`.
- Keep raw external material in `sources/`; protect it from normal edits.
- Keep indexes short and navigational; put details in topic pages.
- Record every durable knowledge change in `knowledge/log.md`.
- Preserve contradictions and uncertainty; never silently overwrite them.
- Keep task-specific state outside durable knowledge, for example under
  `.tmp/tasks/`. Do not store the complete conversation in knowledge.

Before finishing a task that introduces substantive project context, or any
non-trivial task, assess whether it produced a reusable fact, constraint,
decision, procedure, or recurring failure pattern that existing knowledge does
not already cover. Use the `knowledge-base` skill to choose whether to skip,
revise, consolidate, split, or create content. Check the affected area for
duplication, contradictions, and broken references. Update indexes only when
navigation changes, log actual durable changes, and run the configured knowledge
check after the final write. Report the Knowledge Outcome with actual results.
Do not create a topic page merely to repeat an authoritative
rule already maintained in an instruction or skill.

## Sensitive configuration

- Do not manually inspect, display, or copy `.env` contents into conversations,
  tool output, logs, or generated files. Use `.env.example` only to identify
  variable names and expected configuration shape.
- When the user authorizes a script or application to use credentials, load only
  the required allowlisted variables from the project's `.env` into process
  memory. Prefer existing process variables. For Python, access them with
  `os.getenv`; never evaluate `.env` as shell or Python code.
- Never print, log, return, or pass secret values as command-line arguments.
- Do not load `.env` just to inspect configuration or discover unrelated values.

## Skills and scripts

- Group scripts under `scripts/<topic>/` by project domain. Keep the root limited
  to navigation and scripts that are genuinely shared across domains.
- Keep helpers beside their scripts. When moving scripts, update repository-root
  path resolution, imports, examples, and knowledge references.
- Maintain `scripts/README.md` as a concise directory and entry-point guide.
- Keep each skill focused on a repeatable workflow and supporting references.
- Do not place personal or project-specific knowledge in this starter's examples.

## Cross-agent compatibility

Codex discovers repository instructions from `AGENTS.md` and project skills
from `.codex/skills/`. Claude Code reads the root `CLAUDE.md`, which imports
this file. On Windows, `.agents/skills/` and `.claude/skills/` are directory
junctions to `.codex/skills/`; these are compatibility paths, not separate
skill copies.

On macOS and Linux, use symbolic links for the same compatibility paths. Both
links point to `.codex/skills/`, so each skill has one maintained definition.

Create, edit, and maintain project skills in `.codex/skills/` only. Do not
copy skills into the compatibility paths. Keep `AGENTS.md` and skills under
`.codex/skills/` canonical.
