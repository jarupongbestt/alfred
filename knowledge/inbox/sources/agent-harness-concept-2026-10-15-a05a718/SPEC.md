# Portable Agent Harness Specification

Status: concept
Version: 0.3.0

## 1. Purpose

The Portable Agent Harness defines a common workflow for software-development
agents without depending on a particular agent runtime, model provider, or tool
protocol.

The harness standardizes:

- lifecycle and stage order
- agent responsibilities
- structured artifacts
- approval and safety gates
- model routing
- testing and review policy
- knowledge-base usage
- final run reporting

Platform adapters translate these rules into Claude, Codex, OpenCode, Hermes, or
another agent's native instructions and tools.

## 2. Design principles

1. **Main Agent owns orchestration; subagents own specialist work.** The Main
   Agent delegates work, holds distilled state, manages approval, and decides how
   to recover from failure. It must not be interpreted as the only agent in the
   workflow.
2. **Plan before editing.** Every task that changes project behavior has a plan.
3. **Approval before implementation.** The user approves the plan before any
   implementation begins.
4. **Small isolated contexts.** Each specialist receives only the ticket, relevant
   knowledge, scope, and task-specific inputs.
5. **Skills are reusable.** Roles describe responsibility; skills describe methods.
   Every portable skill listed by the harness has a corresponding
   `skills/<name>/SKILL.md` source definition. A catalog entry alone is not an
   installable skill.
6. **Mechanical checks are not LLM reasoning.** Running tests, linting, formatting,
   and schema validation should use scripts or native tools where possible.
7. **Least privilege.** An agent receives only the tools and write scope required
   for its role.
8. **The user owns irreversible version-control actions.** The default harness does
   not commit, push, merge, or create releases.
9. **Knowledge compounds.** Durable decisions and discoveries are recorded for
   future tasks; temporary session state is not treated as knowledge.

10. **English coordinates agents; the user language coordinates the conversation.**
    Internal reasoning, delegation payloads, role prompts, and subagent artifacts
    use English. User-facing responses follow the language of the request and may
    be hybrid when the user is multilingual.

The Main Agent leads user-facing messages with the outcome, action, or decision,
using familiar words, clear actors, focused topics, and stable terms. Conditions
stay beside the action they govern. Follow the user's language, natural language
mix, and preferred tone; preserve meaning, evidence, uncertainty, obligations,
and exact technical names, code, paths, commands, quoted text, and artifact fields.
Short messages use the bootstrap's lightweight communication policy. For long or
complex explanations, user-facing Plan presentations, and reports, the Main Agent
loads [`human-readable-communication`](skills/human-readable-communication/SKILL.md).
This is a presentation method, not an automatic rewrite of specialist English
artifacts or a guarantee that the underlying content is true. It does not alter
roles, artifact fields, approval gates, or the lifecycle.

The workflow is intentionally multi-agent. A conforming adapter must provide a way
to invoke specialist subagents, or explicitly report that the host lacks that
capability. A single-agent fallback may preserve the role boundaries and artifact
contracts, but it is a platform limitation—not the harness's default operating
model.

## 3. Workflow

### 3.0 Native projection when applying the concept

This repository is source material for adapters, not an installable directory
template. An application to another repository must first perform read-only
native convention discovery, then produce a target-native layout preview and
source-tree-copy audit before requesting approval. The preview must name the
exact verified destination and load, invocation, or enforcement mechanism for
each `reuse` or `translate` entry.

The applying agent must not reproduce this repository's root `adapters/`,
`knowledge/`, `prompts/`, `schemas/`, or `skills/` directories merely to preserve
its shape. It should translate only the approved responsibilities into the
target platform's native configuration. If the host supports the current Codex
conventions, that can mean root `AGENTS.md`, `.codex/agents/`, and
`.agents/skills/`; if it supports the current Claude Code conventions, that can
mean `CLAUDE.md`, `.claude/agents/`, and `.claude/skills/`. The actual run must
verify those destinations and must stop when evidence is missing or the proposed
layout is source-shaped.

Intake must complete before Planner starts. Planner creates the full Plan, with
all slices and dependencies, before presenting it for approval; do not alternate
between planning a slice and implementing it. After approval, only Test Engineer
and Implementer/Builder invocations may overlap active specialist work. Schedule
ready invocations concurrently only when approved scopes, files, resources,
mutable state, and ordering constraints do not conflict. If a Builder depends on
Test Engineer output, run that pair in sequence. All Test Engineer/Builder work
must finish before Verifier starts. Verifier, Reviewer, Knowledge Curator, and all
other specialists run without overlapping active specialist work. Ordinary
implementation, test, lint, build, acceptance, or verification failures retry
the affected Builder slice within its bounded budget, then escalate; they never
restart Intake or Planning. Re-plan only for explicit human feedback or objective
evidence that the approved Plan or its assumptions are invalid or materially
changed, and renew approval after a material Plan change.

### 3.1 User Request

Before Intake, the Main Agent classifies the message by meaning and conversation
context, not punctuation. Answer ordinary informational questions, explanations,
discussion, and status requests directly. Allow only a minimal read-only lookup
needed for the answer; do not create a new run, Ticket, Plan, specialist invocation,
or full lifecycle for that conversation. Ordinary conversation is not a
full-workflow execution run and does not require per-message knowledge curation.
Clear action requests, including "can you fix this?", and substantial explicitly
requested audits or research route to execution.

During active authorized work, answer questions and then resume the same run and
preserve its artifacts. A question alone does not cancel work, restart it, or
trigger stage re-entry. Changed requirements follow the exact existing
`workflow.reentry` triggers with recorded evidence and renewed approval for a
material Plan change.

Interpret short affirmatives such as "Ok" in context: after a factual explanation,
they acknowledge it without authorizing edits; after a concrete actionable
proposal, they select that approach and advance necessary authorized Intake and
Planning, with edits still waiting for complete Plan approval; after an actual
approval request for a presented complete Plan, they explicitly approve the Plan
and work proceeds without a duplicate approval request. Approach selection alone
is not approval of a Plan that has not been presented in full.

For an execution request pursuing a new independent objective,
the Main Agent may create a new run and assign it a `run_id`. Continue the existing
run when the conversation pursues the same objective. Questions, clarifications,
approvals, selection of an approach, and transitions from research to
implementation do not by themselves start a new run. Retain the `run_id`, Ticket,
Plan, and run state; revise the Ticket or Plan only when a permitted trigger
applies. Record routine progress and task results in the existing run state.
Creating a run must never bypass stage re-entry rules.

Before re-entering a stage, the Main Agent records the exact permitted trigger,
supporting evidence, and changed requirement, assumption, or artifact. The
existing triggers in `workflow.reentry` in [`harness.yaml`](harness.yaml) are
authoritative. Missing implementation detail may justify a bounded Planner update
only when an existing permitted trigger is satisfied; it does not justify fresh
Intake when the Ticket is unchanged.

### 3.2 Intake

Intake starts only for an execution request routed by the Main Agent or a permitted,
evidence-backed Intake re-entry. Direct conversation does not invoke this stage.

The Main Agent delegates Intake to the Intake Agent. In the full workflow, Main
Agent, Intake, and Planner load `knowledge-base` and follow the target project's
configured or existing knowledge navigation entry before defining scope and plans.
The same rule applies to partial adoption that includes knowledge management;
partial scopes without it may explicitly omit this dependency. `knowledge/main.md`
is this repository's example path, not a target-project default. Intake consults the
target's configured action log only when historical activity, contradictions,
recurring failures, audit, or lint context is relevant. It identifies the change
type, scope, acceptance criteria, risk, confidence, and whether clarification is
required.

Intake completes its Ticket before Planner starts. The Main Agent resolves any
critical clarification before dispatching Planner. If an answer changes the
Ticket, Intake completes the corresponding Ticket update before Planner begins.

For bugfixes or unclear failures, Intake loads the `root-cause` skill and performs a
bounded investigation itself. It must distinguish evidence from assumptions.

Intake runs once per run by default. The Main Agent may re-enter Intake only when
user clarification changes the Ticket, or when newly discovered facts provide
evidence that the Ticket is mismatched. The reason and resulting Ticket change
must be recorded. An implementation, test, lint, or verification failure alone
does not justify another Intake pass.

### 3.3 Clarify

Clarify is a Main Agent responsibility. It asks the user only when the Ticket lacks
information needed to produce a reliable plan. No implementation or detailed
planning occurs while critical ambiguity remains.

When clarification changes the Ticket, the Main Agent records the changed
requirements and may perform the bounded Intake re-entry described in section 3.2.
Clarification that does not change the Ticket does not restart Intake or Planning.

### 3.4 Plan

Only after Intake is complete and required clarification is resolved, the Main
Agent delegates planning to the Planner Agent. The Planner reads the
Ticket, relevant knowledge pages, source references, and test-impact information. It
creates an ordered list of small task slices.

For bugfixes, the Planner loads `root-cause` when Intake evidence is incomplete,
contradictory, or insufficient to justify the proposed plan, including when the
proposed change depends on an unverified cause.

The Planner returns the complete Plan before approval: every slice includes
files, dependencies, acceptance criteria, difficulty, and test requirements.
The Plan also identifies scopes, resources, mutable state, and ordering
constraints. Do not begin implementation and then plan remaining slices as work
proceeds. A slice is ready when its declared dependencies are complete and its
approved execution scope does not conflict with other work scheduled at the same
time.

Planning runs once per run by default. The Main Agent may re-enter Planning only
after explicit human feedback on the Plan, or after evidence shows that the Plan
is objectively incomplete, contradictory, out of scope, or invalidated by a
changed Ticket, acceptance criterion, dependency, permission, or platform
assumption. A normal implementation or test failure does not by itself justify
re-planning. Any materially changed Plan requires renewed user approval before
editing resumes.

### 3.5 User Approval

The Main Agent presents a concise, plain-language plan and asks:

```text
Proceed with this plan?

1. Proceed
2. Ask / adjust
```

If the user asks for changes, the Main Agent sends feedback to the Planner and
repeats the approval step. No agent may edit project files before approval.

Approval authorizes only the complete reviewed Plan and its declared scopes.
After approval, the Main Agent builds the dependency-aware execution graph. Only
Test Engineer and Builder invocations may overlap: multiple ready, non-conflicting
test or implementation slices may run concurrently. If implementation depends
on a Test Engineer's output, sequence that pair. Do not run Verifier, Reviewer,
Knowledge Curator, or another specialist during active Test Engineer/Builder
work. After that work settles, run verification, then review, serially. A re-plan
or material scope change pauses further edits under the old approval and requires
a new approval decision.

### 3.6 Test Engineering

When required, the Main Agent delegates this stage to the Test Engineer, who
loads `test-driven-development`.

For a feature or bugfix without matching coverage, the Test Engineer creates or
extends tests from the acceptance criteria. It should not depend on the
Implementer's implementation approach.

Test Engineering dependencies are per slice, not global. Test Engineering is a
prerequisite for a Builder only when that slice's implementation depends on its
output. Independent Test Engineer and Builder invocations may run concurrently
after approval when files, resources, mutable state, dependencies, and ordering
do not conflict. These are the only specialist roles allowed to overlap; no
Verifier, Reviewer, Knowledge Curator, or other specialist runs during this
work. Test Engineers do not modify production code.

For refactors, existing tests are used as regression protection. Cosmetic changes
may use a smoke or visual check instead of a new unit test.

### 3.7 Implement

The Main Agent delegates one approved task slice at a time to each Implementer
invocation. Multiple Implementer invocations, and eligible Test Engineer
invocations, may overlap after approval when slices are dependency-ready and have
no conflicting files, shared resources, mutable state, or ordering requirements.
No Verifier, Reviewer, Knowledge Curator, or other specialist may overlap active
Test Engineer/Implementer work. The Implementer changes only approved scope,
follows acceptance criteria, and returns a structured result.

If implementation reveals that the plan may be incomplete or incorrect, the
Implementer stops and reports evidence. The Main Agent sends work back to Plan
only when that evidence objectively shows the approved Plan or its assumptions
are invalid or materially changed; a material change requires renewed approval.

When an implementation, test, acceptance, lint, build, or verification check
fails, the Implementer loads `root-cause` before retrying. If the approved scope,
acceptance criteria, dependencies, and platform assumptions remain valid, route
the failure directly to the same Implementer slice with failure evidence and
root-cause context. The Implementer reports the cause it addresses rather than
changing code from the latest error message alone. Ordinary failures never invoke
Intake or Planning. After each retry, the relevant work must pass through
verification again before review proceeds.

Each slice has a finite retry budget recorded in the Plan or run state. When the
budget is exhausted, the Main Agent stops automatic retries and escalates with the
attempt history for user input or an explicit blocked result. Exhausted retries do
not trigger re-planning unless the evidence also shows that the approved Plan,
scope, criteria, dependencies, permissions, or platform assumptions are invalid.

### 3.8 Verify

Only after all active Test Engineer and Implementer work is complete, the Main
Agent delegates verification to the Verifier Agent when the platform supports
that role as an isolated subagent. Verify is primarily mechanical. It runs
the narrowest useful checks first, followed by affected regression checks:

- unit and integration tests
- type checks
- lint and formatting checks
- build checks
- acceptance-criteria checks
- direct and dependent regression tests

No specialist work overlaps verification. The Main Agent decides whether a
failure requires a retry, escalation, re-planning, or user input.

The Verifier returns a recommended recovery action with its result. It recommends
`retry_implementer` for an ordinary implementation, test, acceptance, lint,
build, check, or verifier failure when the approved scope, criteria, and
dependency graph remain valid; `replan` only when evidence shows that the Plan or
those assumptions are objectively invalid or materially changed;
`escalate` when the retry budget is exhausted or the failure cannot be safely
classified; `user_input` when a decision is required; and `pass` when verification
succeeds. The affected slice, evidence, and reason for the recommendation must be
included. A normal test failure alone must never be reported as a reason to invoke
the Planner.

### 3.9 Review

After verification completes, the Main Agent delegates review according to risk.
No other specialist overlaps review. The Reviewer independently checks the
changes against the Ticket, approved Plan, acceptance criteria, test results,
security expectations, and scope.

Review depth is risk-based:

- low risk: scope and correctness review
- medium risk: edge cases and regression review
- high risk: independent context, security review, and test-quality review

### 3.10 Knowledge Update

Knowledge management is included in the full workflow, without a separate per-run
opt-in. After review completes, the Main Agent always delegates an assessment to
the Knowledge Curator, serially with other specialist work. The Curator reads
relevant existing knowledge and retains eligible, evidence-backed new learning
in the approved, configured system, updating or merging before creating redundant
material. Partial adoption may select knowledge management independently without
agents, model assignments, or persisted run state. A partial adoption without
knowledge management reports `outside_scope` with a reason. Never write
run-specific learning to this repository's example knowledge tree by default.
Eligible durable information includes:

- architectural decisions
- project conventions
- integration constraints
- recurring failure causes
- security requirements
- testing relationships
- operational procedures

Do not copy conversation transcripts or routine diaries into the knowledge base.
The Curator returns a Knowledge Outcome with a mandatory reason and evidence:
`updated` only after eligible writes and applicable checks complete; `no_change`
after assessment finds only duplicate, temporary, unsupported, code-obvious, or
otherwise non-durable information; or `blocked` with remaining work for missing
approved paths, ambiguous write rules, failed writes, or failed applicable checks.
Do not invent a layout or treat blocked retention as no learning. Preserve native
mapping, category protection, provenance, and approval safeguards. An empty
`knowledge_updates` list alone cannot establish assessment or success.

### 3.11 Finalize

The Main Agent confirms the final scope, test results, review findings, Knowledge
Outcome and reason, completed knowledge updates, unresolved risks, and changed
files. A blocked knowledge outcome leaves required work and prevents a completed
run claim; report the blocker and remaining work. Partial adoption without
knowledge reports `outside_scope` explicitly. It returns control to the user.

## 4. Complexity routing

All execution tasks routed into the lifecycle are planned. Direct conversational
answers do not require a Plan. Complexity only controls model strength and review
depth.

| Tier | Typical task | Routing |
|---|---|---|
| 0 | cosmetic or very small bounded change | junior Planner, junior Implementer, lightweight review |
| 1 | normal feature or refactor | standard Planner, task-level Implementer, normal review |
| 2 | cross-cutting, load-bearing, security, money, data, or low-confidence work | senior Planner, stronger Implementer, independent review |

When uncertain, route upward. The cost of a stronger model is usually lower than
the cost of a wrong plan or missed regression.

## 5. State and permissions

The Main Agent may hold:

- Ticket
- Plan
- approval status
- task results
- verification results
- review findings
- knowledge-update summary

The Main Agent should not carry large raw file contents between stages.

Suggested default permissions:

| Role | Read project | Write source | Write tests | Write knowledge | Git write |
|---|---:|---:|---:|---:|---:|
| Main Agent | yes | no or limited | no | delegated | no |
| Intake | scoped | no | no | no | no |
| Planner | scoped | no | no | no | no |
| Test Engineer | scoped | no | yes | no | no |
| Implementer | scoped | yes | no | no | no |
| Verifier | scoped | no | no | no | no |
| Reviewer | scoped | no | no | no | no |
| Knowledge Curator | relevant | no | no | yes | no |

The exact enforcement mechanism belongs to the adapter.

## 6. Completion criteria

A run is complete when:

- the approved plan was executed or explicitly reported as blocked
- verification results are available
- review is complete or intentionally skipped with a reason
- scope was audited
- the applicable knowledge assessment completed with `updated` or a reasoned
  `no_change`; a partial scope without knowledge reports `outside_scope`
- no unauthorized git action occurred
- the Main Agent returned a final summary

If required knowledge assessment or retention is blocked, finalize with
`status: blocked`, a reason, and the remaining work. This is a blocked result,
not a completed run.

## Knowledge retrieval and integrity

In knowledge-enabled scope, Main Agent, Intake, and Planner retrieve from the
configured startup entry, matching index Navigation Hints, relevant topic, and
focused source_refs before broader searches. Missing, stale, contradictory, or
insufficient navigation permits only a reasoned, recorded narrow expansion.
Hints are a `Task | Target` table with existing local page/category links, or the
explicit empty state `No navigation hints yet.`; do not invent domain indexes.

The knowledge-base method defines typed YAML topic metadata, reference handling,
category protection, and explicit classification. Documentation and ADRs is the
local source default and defines decision status and retained human evidence.
Examples and templates never establish an actual project decision. Read evidence
and reconcile meaning; mechanical validation cannot establish content truth.

Verifier checks knowledge changed by implementation. Curator checks its own
final state after all topic, metadata, index, hint, and log writes, returning
Knowledge Outcome actual results. A required check that fails or cannot run is
`blocked`; earlier passing checks do not certify later writes. Integrity checks
are read-only and never execute reference commands or verify remote URLs.
