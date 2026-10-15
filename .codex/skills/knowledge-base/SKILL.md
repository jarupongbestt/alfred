---
name: knowledge-base
description: Retrieve, write, curate, and validate durable project knowledge with source references and protected raw inputs.
---

# Knowledge Base

Use this method with [AGENTS.md](../../../AGENTS.md), the
[task-domain gate](../../../knowledge/main.md#task-domain-gate), and the
[configured adoption map](../../../knowledge/_system/adoption.md). This starter adopts the
complete knowledge-management capability; the current assistant performs its
assessment responsibilities without requiring specialist agents.

Resolve the target's approved knowledge root, startup entry, categories, protected
areas, action log, and check command from project instructions or the adapter map.
Never infer paths from this repository's example tree. Full workflow includes
knowledge management; a partial adoption without it may omit this method with an
explicit `outside_scope` reason.

## Retrieve before scanning

Main Agent, Intake, and Planner read the configured startup entry, then the
matching domain index's `## Navigation Hints`, the relevant topic, and focused
`source_refs`, before broader project searches. Use hints to constrain scope,
not as proof that a claim is true. When a page or hint is absent, stale,
contradictory, or insufficient, record the evidence and reason for a narrow
expansion. Do not preload the whole knowledge tree or invent domain indexes.
Read the action log only for history, contradictions, recurring failures, audit,
or lint context. Read raw sources only when their exact evidence is needed.

A configured domain index keeps navigation concise. Its `## Navigation Hints`
uses a Markdown table with `Task | Target` columns; each target is one local
inline link to an existing page or category. `No navigation hints yet.` is the
explicit empty state. Topic details belong in topic pages.

## Choose durable changes

Read existing relevant pages and check equivalent meaning before choosing:

- Skip duplicate, temporary, unsupported, code-obvious, or non-durable material.
- Update the existing home for corrections, evidence, or useful qualifications.
- Merge overlap while preserving distinct facts, exceptions, and evidence.
- Split mixed topics only when focused retrieval improves and links survive.
- Create a page when eligible information has no suitable existing home.

Keep decisions, constraints, procedures, and recurring failure patterns that
will help future work. Exclude task diaries, transcripts, copied code, and
unsupported claims. Preserve the target's category rules: internal discoveries
and ADRs, faithful external compilations, and protected raw inputs are distinct.
Locked derived content changes only through an explicitly approved source re-sync;
normal curation must not rewrite raw material. Reorganization stays within scope,
maintains navigation and references, and preserves provenance and exceptions.

Resolve contradictions by comparing evidence, versions, and conditions. Explain
any correction or supersession; preserve unresolved disagreements explicitly.
Do not silently prefer the newest claim.

## Topic and reference contract

Ordinary Markdown knowledge pages have YAML frontmatter with `type`,
`description`, `source_refs`, `updated`, and `status`. `type` is `self`, `derived`,
`adr`, or `source-companion`; `description` is a nonempty single line.
`updated` is an actual `YYYY-MM-DD` date. `source_refs` is a nonempty list of
`{kind: local|url|command|artifact, target: ...}` mappings. Local and artifact
references are page-relative, exist inside the explicit repository root, and
remain contained after symlink resolution; an artifact names an exact retained
file. URL references use HTTP(S) with a hostname. Command references are inert
strings and cannot establish evidence by themselves; use retained output or
another supporting source. Never execute a reference just to validate it.

### Write frontmatter and source_refs

For a new page, use the [internal topic](../../../knowledge/_template/self-topic.md),
[external compilation](../../../knowledge/_template/derived-topic.md),
[source companion](../../../knowledge/_template/source-topic.md), or
[ADR](../../../knowledge/_template/adr.md) template for the chosen category.
Use the [domain-index instructions](../../../knowledge/_template/index.md) when
adding navigation. Register new indexes, raw-source directories and source
companions in the [configured layout](../../../knowledge/validation-layout.yaml);
their names alone do not classify them.

Use block-style YAML, two-space indentation and quoted ISO dates, following this
project's [authoring convention](../../../knowledge/_system/contracts.md#topic-lifecycle).
This internal-topic example shows the required shape; replace every placeholder
with actual supported content before retaining a topic:

```yaml
---
type: self
description: "<One-line durable finding or procedure>"
source_refs:
  - kind: local
    target: "<evidence path relative to this topic>"
updated: "<actual YYYY-MM-DD>"
status: draft
---
```

Choose only the references actually used to support the recorded claims:

| kind | What target identifies | Evidence requirement |
| --- | --- | --- |
| `local` | An existing repository file, relative to the topic, such as `../sources/<file>` | Inspect its relevant content and explain which claim it supports. |
| `url` | The exact HTTP(S) source URL | Record actual access date, version and applicability in the body; retain external inputs according to source-intake rules. |
| `artifact` | An exact retained evidence file, relative to the topic | Use a file path, without a fragment or a freeform run ID. |
| `command` | The exact command text as inert provenance | Pair it with retained output or other supporting evidence; never use or execute the command reference as proof by itself. |

In the body, connect findings to the relevant references and distinguish user
reports, inspected source facts and internal conclusions. Record source access
dates and versions separately from the page's `updated` date. A reference list
or a `current` status alone does not verify a claim. The pinned checker permits
command-only `source_refs` as provenance; separately assess whether each claim
has supporting evidence. For an actual worked metadata
shape, inspect the configured fictional examples; never cite their content as
evidence of real project facts.

Ordinary statuses are `draft`, `current`, and `superseded`; superseded pages name
an existing local/artifact replacement in `superseded_by`. Use the
[Documentation and ADRs method](../documentation-and-adrs/SKILL.md) for ADR
statuses, human decision evidence, and preserved history.

Templates retain required field shapes and use explicit `<...>` placeholders
for values to replace. Only configured template paths receive placeholder date
and reference-existence exemptions; nonplaceholder references still resolve.
Configured example pages require `example: true`, complete real metadata, and
an explicit illustrative notice. Examples are not evidence of project decisions.
Indexes, navigation pages, logs, raw inputs, companions, templates, and examples
are classified by explicit configuration, never by a guessed filename.

## Write, log, then check

After approved edits, maintain affected topic metadata, descriptions, hints,
indexes, links, and the configured action log. Its machine-readable entries use
the format in the [configured log](../../../knowledge/log.md); adapt the approved log
path, never copy fabricated events. Record actual timestamps, actions, evidence,
and check results. A prior check cannot certify a later log write.

Run the configured integrity check **after the final knowledge write**, including
navigation and log edits. Map applicable checks to a compatible existing target
checker, translated checks, or the optional portable
[validator](../../../scripts/knowledge/validate_knowledge.py). That reference implementation
requires Python 3.10+ standard library only and an explicit target classification
layout; the [configured layout](../../../knowledge/validation-layout.yaml) defines the native classifications.
Its bounded YAML input forms, typed parse errors, and resource limits are documented
in the [checker guide](../../../knowledge/_system/validation.md#supported-input-forms); these limits
do not narrow the portable metadata contract or a compatible target checker.
It checks metadata, local links and supported anchors, hints, ADR structure, and log
integrity, rejects duplicate keys, and never executes reference commands or checks
remote availability. Reasoning must still assess truth, relevance, contradictions,
and human evidence.
Required checks that fail or cannot run block retention. If no checks apply,
record the reason explicitly rather than treating an unavailable check as absent.

For a target adapter, include or translate the required knowledge contract into
approved native paths and inventory included, translated, referenced, and omitted
linked assets with reasons. Example log/layout files need not be copied. Selecting
the reference checker requires mapping its runtime, actual target classifications,
and check command; other adoptions do not require Python. Its maintainer tests are
not automatically created, run, or copied into targets. Rewrite or remove projected
links and commands consistently; do not copy the example tree wholesale.

## Report

Return the authoritative [Knowledge Outcome](../../../knowledge/_system/contracts.md#knowledge-outcome)
with `applicable`, `status`, mandatory `reason`, `evidence`, `files_changed`,
`checks`, and `remaining_work`. `updated` requires eligible completed writes and
passed applicable checks after final writes; `no_change` requires an actual
assessment finding no eligible learning. Missing approved paths, ambiguous policy,
failed writes, unavailable required checks, and failed checks are `blocked`, with
completed partial writes and remaining work distinguished. `outside_scope` applies
only to partial adoption excluding knowledge management. Empty writes do not
prove assessment, and this source repository's example tree is never a default
home for run-specific learning.

## Starter source intake and curation

Apply automatic capture of substantive user context from `AGENTS.md`; a separate
save request is unnecessary. Preserve tentative user reports as tentative, honor
an explicit request not to save, and keep temporary task progress outside knowledge.
Start at `knowledge/main.md`. `_template/`, `_example/`, and an illustrative
`domain/` are non-authoritative; never invent a real domain from a broad keyword.
For knowledge-system maintenance use the adoption map rather than creating a
project domain merely to repeat these instructions.

Watch for repeated claims drifting apart, overlapping page scopes, a reader
needing several pages for one answer, failed procedures, unsupported claims,
and task history obscuring current guidance. Inspect the suspected problem
before changing structure; similar wording alone does not prove duplication.

- Choose a primary home based on scope, evidence, and discoverability. Link
  from related pages; a short contextual summary may be useful, but avoid
  maintaining multiple full copies of the same guidance.
- Before merging, preserve unique facts, exceptions, decision rationale, and
  claim-level provenance. Do not collapse differences such as sandbox versus
  production or different API versions into one unconditional statement.
- Keep internal conclusions in `self/` distinct from faithful external material
  in `derived/`; link across them when appropriate. Never consolidate by
  rewriting or deleting raw sources.
- Before moving or retiring a maintained page, find and repair inbound links
  and any generator or script references. For generated content, address its
  generation path so the next run does not restore the problem. Retire an old
  page only after its useful content and references are accounted for; retain a
  short pointer when an external or unknown caller may still need the old path.
- Fix demonstrated local problems within the task's scope. If broader cleanup
  is needed, report the concrete problem and proposed scope without launching
  an unrelated reorganization or creating speculative cleanup inventories.

Compare source authority, directness of evidence, applicable version, and
operating conditions. A newer timestamp alone does not settle a contradiction.
When evidence resolves it, make the applicable current guidance clear and keep
the necessary supersession reason and provenance. Keep historical detail only
when it explains a decision or remains relevant to an older supported context.

When evidence does not resolve it, preserve both claims with their sources and
conditions, mark the uncertainty where the reader encounters the claim, and
state what evidence would settle it. Separate observed facts from inference;
do not promote an assumption to established guidance. Add status or review
dates only when they help judge applicability, and never imply verification
that did not occur.

- Treat every file or external artifact received from the user as raw source
  material first.
- Place it unchanged in the correct project's `knowledge/<domain>/sources/`
  before extracting, summarizing, or deriving anything from it.
- If the domain is unclear, do not derive yet. Ask for the domain or hold the
  file under `knowledge/inbox/sources/` until it is triaged.
- Never edit or silently replace a raw source. Store a new version as a new
  source artifact and record the relationship in the derived page or index.


## Local provenance

Local adaptation of agent-harness-concept `a05a718dd96218abd077adc258b9bf484121a929`
(v0.3.0), accessed 2026-10-15. Native path translations, retained starter rules,
supporting assets and compatibility evidence are in the
[adoption map](../../../knowledge/_system/adoption.md).
