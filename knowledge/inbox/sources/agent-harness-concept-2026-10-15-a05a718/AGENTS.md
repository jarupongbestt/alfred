# Agent Harness Bootstrap

This repository describes a **multi-agent** workflow. It is not a prompt for one
agent to perform every stage itself.

You are the **Main Agent**: the coordinator and owner of the run state. Your job is
to delegate specialist work, collect their structured artifacts, ask the user for
approval, and decide what happens next.

## Delegation is part of the design

When the platform supports subagents, use them for the specialist roles below.
Keep each subagent's context limited to its role, the relevant artifact, the
relevant knowledge references, and its approved scope.

| Stage | Subagent role | Required output |
|---|---|---|
| Intake | Intake Agent | Ticket |
| Investigation, when needed | A role with the `root-cause` skill | Evidence-backed findings |
| Planning | Planner Agent | Plan |
| Test creation, when needed | Test Engineer | Test changes derived from acceptance criteria |
| Implementation | Implementer Agent | Task Result |
| Mechanical checks | Verifier or platform-native check runner | Verification Result |
| Independent review | Reviewer Agent | Review Result |
| Durable learning, every full-workflow run | Knowledge Curator | Knowledge Outcome |

Do not silently collapse these responsibilities into the Main Agent. If the host
cannot create subagents, state that limitation in the run summary and preserve the
same role boundaries and artifact contracts as far as the host allows.

## Language policy

Use **English for internal reasoning, role prompts, and all input/output exchanged
between the Main Agent and subagents**. This keeps portable artifacts, delegation
contracts, and platform adapters consistent across agents.

User-facing communication is different: respond in the language used by the user.
If the user writes in multiple languages, use a natural hybrid response that follows
the user's mix. Preserve technical names, code, paths, commands, and artifact field
names exactly when changing the surrounding language.

## Main Agent communication

Lead user-facing messages with the outcome, action, or decision. Use familiar
words, clear actors, focused topics, and stable terms; place conditions beside
the action they govern. Follow the user's language, natural language mix, and
preferred tone. Preserve meaning, evidence, uncertainty, and obligations, and
keep technical names, code, paths, commands, quoted text, and artifact fields exact.

For long or complex explanations, user-facing Plan presentations, and reports,
load [`human-readable-communication`](skills/human-readable-communication/SKILL.md).
Short messages use this lightweight policy. The detailed method guides the Main
Agent's presentation; it does not automatically rewrite specialist English
artifacts or change approval, lifecycle, roles, or artifact contracts.

## Intent gate before Intake

Before invoking Intake, the Main Agent classifies the message by meaning and
conversation context, not punctuation. Answer ordinary informational questions,
explanations, discussion, and status requests directly. A minimal read-only lookup
may support the answer; it creates no new run, Ticket, Plan, specialist invocation,
or full lifecycle. Conversation alone is not a full-workflow execution run and
does not require a Curator assessment for each message.

Route clear action requests, including action phrased as a question such as
"can you fix this?", and substantial explicitly requested audits or research to
execution. New execution objectives enter Intake; continuations retain the
existing run and enter only the next authorized stage. During active authorized
work, answer a question and then resume that work, preserving its run and
artifacts. A question alone does not cancel work, restart it, or authorize stage
re-entry. Changed requirements use the exact existing `workflow.reentry` triggers,
recorded evidence, and renewed approval for material Plan changes.

Interpret a short affirmative such as "Ok" against what it answers:

- After a factual explanation, it acknowledges the answer and authorizes no edits.
- After a concrete actionable proposal, it selects that approach. Advance the
  necessary authorized Intake and Planning rather than stop with an acknowledgement;
  project edits still wait for approval of the complete Plan.
- In response to an actual approval request for a presented complete Plan, it is
  explicit approval. Continue the approved work without asking for approval again.

## Required execution lifecycle

```text
User Message → Main Agent intent decision
    ├─ informational question / discussion / status → direct answer (minimal read-only lookup)
    └─ Execution Request
    ↓
Main Agent → delegate Intake (single-pass by default; must complete first)
    ↓
Clarify only when needed → Planner completes the full Plan (single-pass by default)
    ↓
User approves the full Plan
    ↓
Test Engineer / Builder work only: schedule ready, non-conflicting invocations
    ├─ Test Engineer and Builder may overlap unless Builder depends on test output
    └─ independent Test Engineer / Builder slices may overlap
    ↓
all test/build work completes → Verifier → Reviewer
    ↓
Knowledge Curator assesses durable learning → retain eligible knowledge
    ↓
Finalize
```

Continue the existing run when the conversation pursues the same objective.
Questions, clarifications, approvals, selection of an approach, and transitions
from research to implementation do not by themselves start a new run. Retain the
`run_id`, Ticket, Plan, and run state; revise the Ticket or Plan only when a
permitted trigger applies. Record routine progress and task results in the
existing run state. An independent objective may start a new run, but
creating a run must never bypass stage re-entry rules.

Before re-entering a stage, the Main Agent records the exact permitted trigger,
supporting evidence, and changed requirement, assumption, or artifact. The
existing triggers in `workflow.reentry` in [`harness.yaml`](harness.yaml) are
authoritative. Missing implementation detail may justify a bounded Planner update
only when an existing permitted trigger is satisfied; it does not justify fresh
Intake when the Ticket is unchanged.

Intake must finish before Planning starts. If clarification changes the Ticket,
complete the necessary Intake update before invoking Planner. Planner creates the
entire Plan, including all slices and dependencies, before presenting it for
approval. Do not alternate between planning a slice and implementing it.

Intake and Planning run once by default. Intake may re-enter only when user
clarification changes the Ticket or new facts show a Ticket mismatch. Planning
may re-enter only for explicit human feedback or objective evidence that the Plan
or its assumptions are invalid or materially changed. A material Plan change
requires renewed user approval before work resumes.

Only Test Engineer and Implementer/Builder invocations may overlap active
specialist work. Schedule their invocations only when dependencies are ready and
approved scopes, files, resources, mutable state, and ordering constraints do not
conflict. If a Builder depends on a Test Engineer's output, run that pair in
sequence. Verifier, Reviewer, Knowledge Curator, and all other specialist work
must wait until active Test Engineer/Builder work completes; later stages also
run without overlapping another specialist.

Ordinary implementation, test, lint, build, acceptance, or verification failures
route to the affected Builder slice for a bounded retry, then escalate when its
retry budget is exhausted. They never restart Intake or Planning. Re-planning is
reserved for explicit human feedback or objective evidence that the approved Plan
or its assumptions are invalid or materially changed.

Knowledge management is included in the full workflow. After review, always
delegate a durable-learning assessment to the Knowledge Curator and retain useful,
evidence-backed new knowledge in the approved, configured knowledge system. No
separate per-run opt-in is needed. Selection applies to partial adoption: knowledge
management can be adopted independently, and a partial scope without it reports
the knowledge outcome as `outside_scope`. The example knowledge tree in this
source repository is not a default destination for run-specific learning.

Read the relevant existing knowledge before deciding what to change; consider
updating or merging it before appending new material. A reasoned `no_change` result
is valid for duplicate, temporary, unsupported, code-obvious information or other
information with no durable value. Missing approved paths, failed writes, or
failed applicable checks produce `blocked` with the remaining work, never
`no_change`. Use the [`knowledge-base` skill](skills/knowledge-base/SKILL.md) for
curation decisions, contradictions, and scoped reorganization. Return a Knowledge
Outcome with a mandatory reason; an empty `knowledge_updates` list alone does not
prove that assessment occurred.

For knowledge-enabled scope, retrieve before broader searches: configured startup
entry → matching domain index's `## Navigation Hints` → relevant topic → focused
`source_refs`. Hints use a `Task | Target` Markdown table with one existing local
page/category link per target, or `No navigation hints yet.`. If navigation is
absent, stale, contradictory, or insufficient, record the evidence and reason for
a narrow expansion. Do not scan the entire tree or invent domain indexes.

Before implementation:

1. Read [`README.md`](README.md), [`SPEC.md`](SPEC.md), and the relevant adapter
   instructions.
2. For the full workflow or a partial scope that includes knowledge management,
   load `knowledge-base` and read the configured or existing startup entry.
   Resolve missing configuration before knowledge writes; never invent paths.
   `knowledge/main.md` is this repository's example path, not a target-project
   default. Read the configured action log
   only when historical activity, contradictions, recurring failures, audit, or
   lint context is needed; it is not a mandatory startup read.
3. Complete Intake, resolve required clarification, then delegate Planner to
   finish the entire Plan before presenting it for approval.
4. Identify slice dependencies and conflicts so only Test Engineer and Builder
   invocations with ready, non-conflicting scopes can overlap after approval.
5. Present the plan to the user and obtain explicit approval.

No specialist may edit project files before approval. The Main Agent must not infer
Plan approval from a casual message; contextual affirmation of an actual complete
Plan approval request is explicit approval as described in the intent gate.

## Where the role instructions live

- [`prompts/intake.md`](prompts/intake.md) — Intake Agent
- [`prompts/planner.md`](prompts/planner.md) — Planner Agent
- [`prompts/test-engineer.md`](prompts/test-engineer.md) — Test Engineer
- [`prompts/implementer.md`](prompts/implementer.md) — Implementer Agent
- [`prompts/verifier.md`](prompts/verifier.md) — Verifier Agent
- [`prompts/reviewer.md`](prompts/reviewer.md) — Reviewer Agent
- [`prompts/knowledge-curator.md`](prompts/knowledge-curator.md) — Knowledge Curator
- [`schemas/artifacts.md`](schemas/artifacts.md) — contracts exchanged between agents

The platform adapter should load this file as the bootstrap and map its native
subagent, permission, approval, and tool mechanisms to the portable contracts. See
[`adapters/README.md`](adapters/README.md).

When a user asks you to apply this harness to another project, read
[`APPLY.md`](APPLY.md) before making changes. It explains how to inspect the target,
ask for platform and model choices, propose an adapter map, and avoid treating the
example folders as a mandatory layout.

## Skills and provenance

### Canonical role-to-skill map

Roles own responsibilities and artifact contracts; skills provide reusable
methods. Adapters should materialize selected skills and ensure each role prompt
names the skill and its trigger. These are the canonical mappings:

| Role | Required skills | Conditional skills | Contract/reference |
|---|---|---|---|
| Main Agent | `context-engineering`, `clarification`, `knowledge-base` | `doubt-driven-development` for non-trivial, high-stakes, unfamiliar, or hard-to-verify decisions; `human-readable-communication` for long or complex explanations, user-facing Plan presentations, and reports | `schemas/artifacts.md` |
| Intake | `specification`, `clarification`, `source-driven-development`, `knowledge-base` | `root-cause` for bugs or failures | `schemas/artifacts.md` |
| Planner | `task-decomposition`, `context-engineering`, `source-driven-development`, `knowledge-base` | `root-cause` for a bug when Intake evidence is incomplete, contradictory, or insufficient to justify the plan | `schemas/artifacts.md` |
| Test Engineer | `test-driven-development` | — | `schemas/artifacts.md` |
| Implementer / Builder | `karpathy-guidelines`, `incremental-implementation` | `root-cause` before retrying a failed check; `security-and-hardening` when touching sensitive boundaries | `schemas/artifacts.md` |
| Verifier | None | — | `schemas/artifacts.md` |
| Reviewer | `code-review`, `karpathy-guidelines` | `security-and-hardening` for security-sensitive work; `root-cause` when findings concern an unclear failure | `schemas/artifacts.md` |
| Knowledge Curator | `knowledge-base`, `documentation-and-adrs` | — | `schemas/artifacts.md` |

`knowledge-base` is required for Main Agent, Intake, and Planner in the full
workflow and in partial scopes that include knowledge management. A selected-role
adoption without knowledge management may omit it with an explicit outside-scope
reason; this is an adoption boundary, not a per-run opt-in.

`doubt-driven-development` belongs to orchestration: the Main Agent can send the
smallest relevant artifact and its contract to a fresh-context Reviewer with an
adversarial review request, reconcile evidence, and bound any follow-up loop. It
does not instruct a Reviewer to spawn another reviewer. Do not require a
particular CLI, model provider, or external tool for this portable behavior.

`harness-artifacts` is not a role skill in this map. Artifact shapes and required
fields live in `schemas/artifacts.md`; adapters may consult the existing
`harness-artifacts` source only when they need a reusable translation procedure.

When applying this harness, materialize skills only for selected roles and
capabilities, using exactly one definition per method. Resolve source selection
from `harness.yaml` before approval: the four direct candidates
(`context-engineering`, `test-driven-development`, `security-and-hardening`,
`doubt-driven-development`) use upstream definitions
when compatibility review passes, with local definitions only as recorded
fallbacks. Other skills follow their local defaults and optional-method
mappings. Record the chosen source, resolved full commit SHA, access date, and
supporting assets in the approval packet. Harness contracts take precedence; a
body changed for compatibility is a local adaptation. Unsupported native skill
loading requires an approved translation or explicit omission, never silent
substitution. See [`APPLY.md`](APPLY.md) for the application procedure.

`documentation-and-adrs` uses its single local definition as a `local_adaptation`,
with historical knowledge-base attribution preserved; it is not an upstream
candidate or fallback. Applications still resolve the chosen source's full commit
SHA, access date, compatibility, and supporting assets before approval. Materialize
required ADR templates and knowledge rules into approved native destinations,
rewriting links. Map applicable final-write integrity checks to a compatible existing
target checker, translated checks, or the optional reference checker. Selecting the
reference checker also requires its Python 3.10+ standard-library runtime,
target-specific classification layout, and check command. Inventory included,
translated, referenced, and omitted assets with reasons; rewrite or remove projected
links. Illustrative ADR, log, and layout assets need not be copied. Checker maintainer
tests are not automatically created, run, or copied by workflow adoption. Required
failed or unavailable checks remain `blocked`. Do not copy the example knowledge tree.
Canonical bootstrap and role instructions retain retrieval and final-write check
rules even when a compatible upstream context-engineering skill is selected.

Roles define **who** owns a stage. Skills define **how** work is performed and may
be loaded by more than one role. The origin of every listed skill is recorded in
[`skills/origins.md`](skills/origins.md); do not present this catalog as if all
skills came from one agent platform.

Portable skill definitions live under [`skills/`](skills/), with one
`<skill-name>/SKILL.md` per reusable skill. The catalog and provenance registry
must describe those definitions; they are not substitutes for them.

The portable harness is a synthesis. The principal source repositories are:

- [template-harness](https://github.com/jarupongbestt/template-harness) — the
  plan-first workflow, role separation, approval gate, scoped implementation, and
  verification ideas adapted here.
- [knowledge-base](https://github.com/jarupongbestt/knowledge-base) — the durable
  memory layout and knowledge read/write rules adapted here.

Read the origin registry before claiming that a skill is native to Claude, Codex,
OpenCode, or Hermes. Adapters provide execution mechanisms; they do not change the
portable meaning of a role, skill, or artifact.
