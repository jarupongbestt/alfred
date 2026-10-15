# Applying the Harness to a Project

This document is the implementation protocol for an agent asked to “apply this
agent harness” to another repository. Applying means integrating selected
workflow responsibilities into the target repository's native agent setup. It
does not mean installing this repository.

## Important: this is a concept, not a fixed folder template

This repository is a portable concept and specification, not a package, starter
template, or canonical target-repository layout. The folders and filenames shown
below are **illustrative adapter targets**, not a required directory tree. The
portable concept defines responsibilities, workflow, permissions, artifacts, and
knowledge rules. Each platform and target repository may map those responsibilities
to different paths or native configuration.

The source `skills/` directory is a library of portable skill definitions. Every
catalog entry that is materialized must come from an actual
`skills/<name>/SKILL.md`. Applying an adapter translates selected definitions into
the target platform's native skill directory; it does not copy the source
`skills/` directory wholesale.

Never copy, fork, install, or reproduce the `agent-harness` repository wholesale
in a target repository. In particular, do not automatically copy its root files
or its `adapters/`, `knowledge/`, `prompts/`, `schemas/`, or `skills/` trees.
First inspect the target repository, identify the platform(s) it actually uses,
and create only target-native files and directories needed for the approved setup.
Reuse or adapt an individual concept only when the mapping and approval process
below explicitly permits it.

### Output-shape invariant

The result of an application must be a **native projection**, not a copy of this
repository's shape. Before approval, show the projected target tree and compare it
with the source tree. If the projection reproduces this repository's root-level
`adapters/`, `knowledge/`, `prompts/`, `schemas/`, or `skills/` directories without
an independent target-repository reason, the application has failed and must stop.

For current first-party conventions, a Codex projection commonly separates its
destinations: repository instructions remain in root `AGENTS.md`, project-scoped
custom agents use `.codex/agents/*.toml`, and repository skills use
`.agents/skills/<name>/SKILL.md`. Do not move the entire concept under `.codex/`;
`.codex/` is only used for destinations that Codex actually recognizes, such as
project configuration or custom-agent definitions.

A Claude Code projection commonly uses root `CLAUDE.md` (or an existing supported
project instruction location), `.claude/agents/*.md` for custom subagents, and
`.claude/skills/<name>/SKILL.md` for project skills. Do not use `.cluade/`, and do
not create a second instruction tree when an existing `AGENTS.md` can be imported
or otherwise reused under the approved map.

These examples are research anchors, not defaults. The applying agent must still
verify the exact destination and load/invocation mechanism for the identified
platform version and operating mode before placing either path in a map.

## Native convention discovery gate

Native convention discovery is a mandatory, read-only gate before concept
mapping, target file-map proposal, or any write. It applies when the target uses
Codex, Claude, OpenCode, Hermes, or any other platform. The applying agent must
not infer a convention from this repository's examples, from a familiar
filename, or from a path that happens to exist.

Before creating a concept map, the applying agent must identify and record:

- the platform name, platform version or release/channel, operating mode (for
  example local, hosted, cloud, plugin, or integration mode), and host runtime
  and version;
- the target repository, its current instruction/configuration files, existing
  agent and subagent mechanisms, skills, test/check commands, knowledge paths,
  and relevant working-tree or project constraints; and
- the host's actual capabilities and conventions by inspecting the host and
  researching current first-party documentation and, where relevant,
  first-party source or released implementation details.

If the platform version, operating mode, or host runtime cannot be established,
that fact is an unresolved discovery gap and the gate fails. A concise discovery
record should make the evidence auditable. Use the same canonical fields in
prose, YAML, and the artifact contract, for example:

```yaml
capability: specialist_delegation
status: verified                 # verified | unknown | blocked
source_url: https://first-party.example/docs/native-conventions
source_path: null                # exactly one of source_url/source_path
accessed_date: YYYY-MM-DD
applicable_platform_version: "release-or-channel"
applicable_operating_mode: local
finding: "The host supports isolated specialist sessions"
confidence: high
exact_native_destination: "exact verified native destination"
mechanism: "exact load, invoke, or enforcement mechanism"
verification_evidence_ref: "source-1 or exact verification command/record"
```

The discovery record must cite each material finding with exactly one source URL
or exact host/source path, `accessed_date`, `applicable_platform_version`,
`applicable_operating_mode`, `finding`, `confidence`, and
`verification_evidence_ref`. For every portable capability that will be `reuse`d
or `translate`d, the record must also name the exact verified native destination
and the mechanism that makes the host load, invoke, or enforce it. A destination
may be an existing target file, a platform-specific configuration location, a
host setting, an API, or a native session/agent mechanism; it must not be
presented as a file path unless the evidence verifies that it is one.

Discovery has per-destination status using only `verified`, `unknown`, or
`blocked`. Discovery is `verified` only when every relevant destination and its
evidence is verified. Stale, contradictory, or low-confidence evidence makes
the affected evidence and destination `unknown` or `blocked`; it cannot support
`approval.decision: proceed` or any target write.

Evidence must be current and mutually consistent with the identified platform
version and operating mode. Unknown, stale, or contradictory evidence means the
discovery gate has failed: do not create a concept map or promote a guessed
destination into a file map, and do not write. Stop and ask for the missing
information or report the application as `blocked`, including the unresolved
capability and evidence gap. Do not resolve such a gap by copying an example
path or by treating an unverified fallback as native.

### Missing or ambiguous host identity

If the platform, platform version, operating mode, or host runtime is missing or
ambiguous, the applying agent may perform only minimal read-only clarification
needed to identify that fact (for example, inspect a host version/about view or
ask the user for the exact value). It must not create a concept map, propose or
promote a target file map, request approval to proceed, or write while that
ambiguity remains. If the identity cannot be established after that minimal
read-only clarification, the application is `blocked` before mapping and before
any target write.

The examples `.claude/`, `.codex/`, `.agents/`, `CLAUDE.md`, and `AGENTS.md`
are illustrative source material only. They are not universal prescriptions,
defaults, or evidence of support on any platform or version. The same applies
to every path in the illustrative mapping table below. A table entry may be
used only after discovery independently verifies the destination and mechanism
for the actual host.

## Application protocol

### Choose an adoption scope

Applying the harness is a selection, not an all-or-nothing installation. After
the read-only discovery gate, identify the smallest set of capabilities that
meets the user's request. Offer these scopes when the request does not already
specify one:

| Scope | Includes | Does not imply |
|---|---|---|
| Full workflow | Lifecycle, specialist roles, artifacts, approval, verification, and knowledge management with post-review assessment and retention; run-state storage when required | Copying this repository's directory layout or every optional capability |
| Selected capability | Only the named capability, such as knowledge management | Installing lifecycle stages, agents, or run-state storage |
| Selected roles | Only the named roles and their required contracts/skills | Installing unrelated roles or the full lifecycle |

For every selected item, record `reuse`, `translate`, `reference`, or `omit`,
its dependencies, and the target-native destination/mechanism where applicable.
Record every unselected or omitted item with a reason such as user choice,
existing equivalent, or unsupported host feature. Do not silently expand scope.
When the user selects Planner plus Builder/Implementer, include only the minimal
Main Agent coordinator needed to route their work and enforce the approval gate;
explain this dependency and do not install other lifecycle roles by implication.
Full-workflow adoption includes knowledge management automatically: Main Agent,
Intake, and Planner use configured navigation and `knowledge-base`, and after
review the Knowledge Curator assesses every run and retains eligible durable
learning. There is no separate per-run opt-in. Knowledge management can also be
selected by itself and must not imply lifecycle, agent, model, or run-state
installation. A selected-role or capability scope without knowledge may omit its
skills and integration only as outside adoption scope, with an explicit reason.

Inspect the target project and platform before asking scope or configuration
questions. Ask only questions still unresolved by that inspection and relevant
to the selected scope. A full workflow can require a coordinator/model policy;
a knowledge-only setup generally needs the knowledge location and write/lint
policy, not agent model choices or run-state configuration. Do not ask blanket
model, knowledge, or run-state questions for capabilities the user did not select.
If a required decision is already evident from the target's existing setup,
preserve it and record the evidence rather than asking again.

When the user asks to apply this harness:

1. Complete the read-only Native Convention Discovery gate above. Inspect both
   the target repository and the host, identify the platform version, operating
   mode, and host runtime, research current first-party documentation/source,
   and record the required evidence before any concept mapping or file-map
   proposal. Existing instructions and configuration are inputs to preserve,
   adapt, or explicitly migrate; they are not a reason to duplicate them.
2. Read this repository's [`AGENTS.md`](AGENTS.md), [`SPEC.md`](SPEC.md), adapter
   requirements, role prompts, artifact contracts, and skill provenance registry
   as source material for translation. Do not treat any source path as a path to
   copy into the target.
3. Inventory relevant concepts and existing equivalents after discovery, without
   yet proposing target writes. Identify capability and role dependencies that
   affect the user's requested scope.
4. Confirm the adoption scope (full workflow, selected capabilities, and/or
   selected roles) only if the request and inspection do not establish it. Ask
   only for unresolved choices required by that scope, such as how to handle a
   conflicting instruction file, a needed coordinator/model policy, or a new
   knowledge location when no usable knowledge system exists. Preserve existing
   model, knowledge, and run-state policies when they already fit. Knowledge
   location changes require explicit user approval; an existing compatible
   knowledge system can be reused without creating a new layout.
5. Create the target-specific concept map and propose a small platform-specific
   file map derived only from the target inventory, selected scope, and verified
   discovery evidence. Get explicit user approval for the map, selected scope,
   and any required model, knowledge, or run-state decisions before writing,
   generating, installing, or changing anything in the target. A guessed, stale,
   or contradictory destination must not appear in the map.
   Include a native layout preview and a source-tree-copy audit in the approval
   packet. For each selected skill, resolve its source using the candidate and
   default policy in [`harness.yaml`](harness.yaml), compatibility-review the
   actual source body, and inspect its required supporting assets before asking
   for approval. The approval packet must name the exact selected source,
   repository, path, resolved full commit SHA, access date, compatibility
   decision, required assets, and included/translated/referenced/omitted dispositions
   with reasons for each skill. A branch such
   as `main` is a mutable lookup reference, not the revision approval is based
   on. Approval is invalid if the preview is source-shaped, any destination
   lacks verified evidence, or any selected skill source/revision is unresolved.
6. After approval, create or change only files listed in the approved target file
   map, plus files required by an explicitly documented platform convention that
   the map names. If the approved map conflicts with discovery or the host
   cannot load the named mechanism, stop before writing and ask or report
   `blocked`; do not silently substitute a path. Do not create a
   source-repository-shaped tree, unapproved role files, or duplicate existing
   instructions. The bootstrap must tell the host to use specialist subagents
   when supported.
7. Translate or selectively reuse the role prompts and skills named in the map;
   do not copy this concept's example paths blindly. Select only the skills
   required or conditionally mapped to selected roles and the skills needed by
   selected capabilities; a conditional invocation trigger controls when a role
   uses a skill, not whether it is installed. Do not install skills for
   unselected roles or capabilities. For each selected skill, use exactly one
   definition and follow its `harness.yaml` materialization policy: the four
   direct candidates
   (`context-engineering`, `test-driven-development`, `security-and-hardening`,
   and `doubt-driven-development`) default to the
   upstream `SKILL.md` at a resolved full commit SHA when compatibility review
   passes. Use that skill's local definition only as a recorded fallback when
   the upstream candidate is unavailable or has a source-specific format or
   compatibility issue, and the host can load the local definition natively.
   Lack of a native skill mechanism is not a fallback condition: get approval
   for a translation into a supported native mechanism or explicitly omit the
   skill as unsupported. Other skills follow their local defaults and
   optional-method mappings in `harness.yaml`; a same-slug candidate or alias
   is not automatic equivalence.

   Read the chosen `SKILL.md` and recursively inspect its linked files and
   references. Include every required skill-local asset and any required
   repository-level asset (including root-level `references/` where the source
   expects it); a per-skill install command may omit repository-level assets.
   Record which assets are required and each included, translated, referenced, or
   omitted disposition with reasons. Rewrite or remove links to assets not retained.
   Re-check the
   selected source against harness lifecycle, approval, roles, no-commit,
   concurrency, and artifact contracts. These contracts take precedence over
   generic skill methods. If the body itself must be changed to comply, classify
   the single selected definition as a `local_adaptation` and record its upstream
   influence; do not call it a direct upstream copy or also install a second
   definition.

   If the host has no native skill mechanism, get approval for a translation
   into a supported native mechanism or explicitly omit the skill as
   unsupported; do not silently use a local definition as a substitute. Never
   substitute a different source or method silently. Do not leave prompts
   referring to an unavailable or omitted skill. A catalog row without a source
   definition is an adapter error and must be reported, not silently skipped.
   `documentation-and-adrs` uses its local `local_adaptation`, preserving its
   knowledge-base influence. Resolve its actual local revision and assets before
   approval. Include or translate required ADR templates and knowledge rules into
   approved native destinations and rewrite links. Map applicable final-write
   integrity checks to a compatible existing target checker, translated checks, or
   the optional reference checker. Required failed or unavailable checks remain
   `blocked`. Selecting the reference checker requires Python 3.10+ standard library
   only, an actual target classification layout, and a mapped check command; Python
   is not required for other adoptions. Its maintainer tests are not automatically
   created, run, or copied into the target. Illustrative ADR, log, and layout assets
   may remain references or be omitted with a reason. Do not leave projected links
   dangling or copy the example tree.
   Preserve canonical role retrieval and final-write check obligations even when
   upstream context-engineering is selected.

8. Connect the target project's knowledge base for every full-workflow adoption
   and for partial adoption that includes knowledge management. Preserve and use
   its discovered existing location, navigation, categories, and protection rules.
   The source repository's `knowledge/domain/`
   tree is an example of one possible organization, not a default or required
   destination. If the target has no suitable knowledge system, propose a
   project-appropriate location and structure and obtain approval before creating
   it. Configure the curator and skills with the discovered/approved paths;
   never leave source-example paths hardcoded in target instructions. If
   a partial scope excludes knowledge management, do not create or modify
   knowledge files and report `outside_scope` with a reason. Full workflow must
   configure knowledge management rather than silently omit it. Missing approved
   paths or write rules block retention; never invent a layout. Report a Knowledge
   Outcome with reason: `updated` after writes and applicable checks complete,
   `no_change` after assessment finds no eligible durable learning, or `blocked`
   with remaining work for missing configuration or failed writes/checks. An
   empty `knowledge_updates` list alone cannot prove assessment.
9. Validate the applied adapter, including a native post-write verification that
   the platform actually recognizes, loads, invokes, or enforces each written
   destination and mechanism. File existence alone is not verification. Use the
   host's native diagnostic, effective-configuration view, registration/API
   result, session/delegation check, or equivalent mechanism as appropriate, and
   record one per-destination status (`verified`, `unknown`, or `blocked`), the
   exact mechanism, `verification_evidence_ref`, source URL or exact source path,
   `accessed_date`, `applicable_platform_version`,
   `applicable_operating_mode`, `finding`, and `confidence`. The overall result
   is `verified` only when every written destination has a verified record and
   complete evidence. If native verification cannot be completed or evidence
   fails, mark the affected record `unknown` or `blocked`, stop before additional
   target writes, and report the run as blocked without claiming success.
10. Audit the resulting diff against the approved map and confirm that the
   illustrative source tree was not copied. Report the exact files created,
   changed, or left untouched; each verified native destination and mechanism;
   the discovery evidence (source URL or exact source path, `accessed_date`,
   `applicable_platform_version`, `applicable_operating_mode`, finding, and
   confidence); post-write verification evidence and per-destination status
   (including the exact destination, mechanism, and `verification_evidence_ref`);
   concept-map omissions and reasons;
   model choices; unsupported host capabilities; any blocked or unverified
   items; other validation results; and how to start a run.

Do not begin implementation work in the target project while performing this
installation unless the user separately asks for an implementation task.

## Language policy

Keep internal reasoning and all messages exchanged with subagents in English. This
includes delegation prompts, role instructions, structured artifacts, findings,
and task results. English is the portable coordination language of the harness.

Respond to the user in the language of the user's request. If the request is
multilingual, a hybrid response is allowed and should follow the user's language
mix. Keep code, paths, commands, model identifiers, and schema field names
unchanged.

## Illustrative platform mapping

Use the platform's current documentation and capabilities to confirm the actual
paths. These are examples of where an adapter might live:

| Portable responsibility | Claude example | Codex example | OpenCode example | Hermes example |
|---|---|---|---|---|
| Project bootstrap | `CLAUDE.md` | `AGENTS.md` | OpenCode project config | Hermes project/config file |
| Specialist subagents | `.claude/agents/` | `.codex/agents/` or the host's current agent mechanism | `.opencode/agents/` or native agent mechanism | Native Hermes agent/session mechanism |
| Reusable skills | `.claude/skills/` | `.agents/skills/` or the host's current skill mechanism | `.opencode/skills/` or native skill mechanism | Native Hermes skill mechanism |
| Durable knowledge | `knowledge/` | `knowledge/` | `knowledge/` or an approved compatible path | `knowledge/` or an approved compatible path |
| Temporary run state | `.harness/runs/` | `.harness/runs/` | `.harness/runs/` or native session storage | `.harness/runs/` or native session storage |

The `.claude/`, `.codex/`, and `.agents/` paths above are not interchangeable
standards and are not guaranteed to be supported by every version of a platform.
The adapter must verify the host's current convention before creating them.

For the current evidence behind these examples, consult the official
[Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Codex custom agent](https://learn.chatgpt.com/docs/agent-configuration/subagents),
and [Codex skill](https://learn.chatgpt.com/docs/build-skills) guidance, plus
Claude Code's [instruction](https://code.claude.com/docs/en/memory),
[skill](https://code.claude.com/docs/en/skills), and
[custom subagent](https://code.claude.com/docs/en/agents) guidance. These links
are reference evidence only; discovery must record the source, access date,
platform version, operating mode, and native verification for the actual run.

## What the applying agent should create

Create only the target-native files required to provide the capabilities selected
in the approved map. The following are capability examples, not a mandatory file
list or one-file-per-role layout:

- a platform bootstrap or integration with the target's existing instructions;
- specialist delegation for each required role, using the host's native mechanism;
- role guidance adapted from [`prompts/`](prompts) when the target needs it;
- mappings for the portable skills in [`skills/README.md`](skills/README.md) when
  the target has compatible skill support. The source definitions are the
  corresponding `skills/*/SKILL.md` files, not the catalog alone;
- knowledge integration for full workflow and partial scopes that include it,
  using discovered or approved configuration. Use the knowledge contract and its
  `knowledge/main.md`, `knowledge/log.md`, and domain template/example as source
  material rather than copying unrelated concept files;
- run-state storage only when the target needs persisted execution artifacts and
  the user approves it.

The target may implement these capabilities with zero, one, or several native
files. Do not create a separate file for every role, capability, or example path
unless the target platform requires it and the approved map names it. Do not add
files merely to mirror this repository's `prompts/`, `schemas/`, `skills/`,
`knowledge/`, or `adapters/` directories.

For a selected-role setup, materialize only those role responsibilities and
their dependencies. Contracts can be referenced from the selected bootstrap or
role guidance rather than copied into a schema tree. For a capability-only
setup, materialize only that capability's native integration; in particular,
knowledge management alone does not require a bootstrap lifecycle or specialist
agent unless the user selected one or the host needs a minimal integration point.

Do not create a separate Investigator agent by default. Load `root-cause` as a
skill in the role that needs it unless the target platform has a specific reason to
make investigation a separate subagent.

## Model selection is scope-dependent

When the selected scope needs model assignments and the target does not already
define a suitable policy, the applying agent must ask before generating
platform-specific configuration. Do not ask or add model configuration for
knowledge-only or other scopes that do not create agents. Model names,
availability, pricing, and reasoning controls change over time, so this repository
must not hard-code a permanent model name.

Ask a question like:

```text
Which current model should the Main Agent and each subagent use?

Recommendation: use the smallest current model that is reliable for the role,
with stronger reasoning for planning, security-sensitive work, and independent
review. I can suggest options from the models currently available in your platform.
For example only—not a permanent default—you might choose a current small/fast
Claude model with high reasoning and a current small/fast Codex model with high
reasoning for low-risk work, then use a stronger model for tier-2 work.

Would you like one model for every role, or a tiered model policy?
```

The user may choose one model for all roles or a tiered policy. A tiered policy is
usually more economical:

| Work | Suggested policy |
|---|---|
| Intake, simple checks, bounded implementation | Smallest reliable current model |
| Planning, cross-cutting implementation | Standard or stronger current model |
| Security, data loss risk, low-confidence work, independent review | Strongest approved current model |

These are routing recommendations, not model identifiers. The adapter should
record the user's actual choices in its configuration and final run summary.
