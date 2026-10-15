# Portable Artifact Contracts

These are logical contracts. Adapters may represent them as JSON, YAML, Markdown,
or native tool results, but the fields and meaning should remain compatible.

## Evidence Record

Evidence records use the same fields in discovery, concept/file mapping, and
native post-write verification. Exactly one of `source_url` or `source_path`
must identify the source; `source_path` is an exact host or first-party source
path, not an inferred or illustrative path. `verification_evidence_ref` points
to the exact command, native diagnostic, effective-configuration view,
registration/API result, session/delegation check, or evidence record used for
verification.

```yaml
evidence_id: evidence-123
status: verified              # verified | unknown | blocked
source_url: https://first-party.example/docs/native-conventions
source_path: null             # use instead of source_url when a URL is not applicable
accessed_date: YYYY-MM-DD
applicable_platform_version: "release-or-channel"
applicable_operating_mode: local
finding: "The host recognizes the native mechanism"
confidence: high              # high | medium | low
exact_native_destination: "exact verified destination or null"
mechanism: "exact load, invoke, enforce, or verification mechanism"
verification_evidence_ref: "exact command, source, or evidence reference"
```

`source_url` and `source_path` are mutually exclusive and one is required.
`applicable_platform_version`, `applicable_operating_mode`, `finding`, and
`confidence` are required for every material finding. Low-confidence, stale, or
contradictory evidence has `status: unknown` or `status: blocked` and cannot
authorize a mapping or write.

## Native Discovery

Native Convention Discovery is a read-only prerequisite for concept mapping,
file-map proposals, and writes. It records the actual host and target
inventory, rather than prescribing a platform layout. A discovery has status
`verified` only when the relevant evidence and destinations are verified;
`unknown` records an unresolved convention, and `blocked` records a condition
that requires stopping before a write.

```yaml
discovery_id: discovery-123
run_id: run-123
status: unknown              # verified | unknown | blocked
platform: codex
platform_version: "release-or-channel"
operating_mode: local        # local | hosted | cloud | plugin | integration | other
host_runtime:
  name: runtime-name
  version: "runtime-version"
target_inventory:
  repository_root: /path/to/target
  instruction_files: []
  native_configuration: []
  agent_subagent_mechanisms: []
  skills: []
  checks: []
  knowledge_paths: []
  run_state_paths: []
  constraints: []
target_layout:
  status: unknown              # verified | unknown | blocked
  native_projection_preview: []
  source_tree_reproduction: unknown  # true | false | unknown
  unapproved_source_tree_paths: []
  verification_evidence_ref: null
host_capabilities:
  - capability: delegate
    status: verified       # verified | unknown | blocked
    finding: "Host can invoke isolated specialist sessions"
    evidence_refs: [source-1]
first_party_sources:
  - source_id: source-1
    status: verified       # verified | unknown | blocked
    source_url: https://first-party.example/docs/native-conventions
    source_path: null      # exact first-party path when a URL is not applicable
    accessed_date: YYYY-MM-DD
    applicable_platform_version: "release-or-channel"
    applicable_operating_mode: local
    finding: "The host loads the verified native mechanism"
    confidence: high       # high | medium | low
    verification_evidence_ref: source-1
capability_destinations:
  - capability: main_agent_bootstrap
    status: verified       # verified | unknown | blocked
    exact_native_destination: "exact verified destination"
    mechanism: "exact load, invoke, or enforcement mechanism"
    verification_evidence_ref: source-1
    evidence_refs: [source-1]
  - capability: write_files
    status: unknown
    exact_native_destination: null
    mechanism: null
    verification_evidence_ref: null
    evidence_refs: []
    unknown_blocker_reason: "The host convention could not be established"
unknown_blocker_reasons:
  - capability: write_files
    status: unknown       # unknown | blocked
    reason: "Missing or contradictory first-party evidence"
    required_action: "Ask for the missing information or report the run blocked"
```

Each `first_party_sources` record must contain `status`, exactly one of
`source_url` or `source_path`, `accessed_date`,
`applicable_platform_version`, `applicable_operating_mode`, `finding`, and
`confidence`, and `verification_evidence_ref`. Each material finding must
reference current, mutually consistent first-party evidence. Each capability
that is reused or translated must have a verified `exact_native_destination`,
`mechanism`, and
`verification_evidence_ref`. Every destination has its own `status`; discovery
is `verified` only when all relevant destinations and their evidence are
verified. Unknown, unsupported, stale, contradictory, or low-confidence
evidence must be `unknown` or `blocked` and must not be promoted into a file
map. Unknown destinations cannot be guessed. Illustrative paths such as
`.claude/`, `.codex/`, `.agents/`, `CLAUDE.md`, and `AGENTS.md` are not evidence
of a native convention. Native verification is required after an approved write;
file existence alone is insufficient, and the result belongs in the Run Summary.
This contract does not create platform config files or hardcode a universal
native layout.

`target_layout` is required for an application that writes files. The preview
must show the target-native destinations before approval. `source_tree_reproduction`
must be `false`, and `unapproved_source_tree_paths` must be empty, before the
application may proceed. A value of `true` or `unknown` blocks approval and target
writes; an existing target path may be retained only when the inventory and map
give it an independent reason.

## Concept Map

The Concept Map preserves the portable concept while recording how the actual
host supports it. Every covered concept has exactly one action: `reuse`,
`translate`, `reference`, or `omit`. `reuse` and `translate` require a verified
exact native destination, mechanism, and linked discovery evidence.

```yaml
concept_map_id: concept-map-123
discovery_id: discovery-123
status: unknown               # verified | unknown | blocked; an unknown entry is illustrative
skill_materializations:
  - skill: context-engineering
    selection_status: materialized # materialized | reused_existing | omitted | unsupported
    materialization_source:
      kind: local_definition      # upstream_direct | local_definition | local_adaptation | target_existing_definition
      repository: https://github.com/jarupongbestt/agent-harness
      path: skills/context-engineering/SKILL.md
      ref: HEAD                   # mutable name only; record the resolved SHA below
      resolved_commit_sha: "<full 40-character SHA resolved at application time>"
      accessed_date: YYYY-MM-DD
      adapted_from: null          # required for local_adaptation; records upstream influence, not a second materialized source
    compatibility:
      status: compatible           # compatible | adapted | incompatible | not_applicable
      precedence_contracts: [lifecycle, approval, roles, no_commit, concurrency, artifact_contracts]
      decisions: []
    supporting_assets:
      required: []                # records use {path, purpose}
      included: []                # records use {path, destination}
      omitted: []                 # each omission requires {path, reason}
    fallback:
      used: false
      from_source: null
      to_source: null
      reason: null
    omission:
      omitted: false
      reason: null
entries:
  - concept: workflow_lifecycle
    action: translate          # reuse | translate | reference | omit
    status: verified           # per-destination status
    source_material_refs: [portable-source-1]
    exact_native_destination: "target-native bootstrap or session mechanism"
    mechanism: "host mechanism that loads or invokes the concept"
    discovery_evidence_refs: [source-1]
    verification_evidence_ref: source-1
    omission_reason: null
  - concept: unsupported_capability
    action: omit
    status: unknown
    source_material_refs: [portable-source-2]
    exact_native_destination: null
    mechanism: null
    discovery_evidence_refs: [source-2]
    verification_evidence_ref: null
    omission_reason: "The host does not expose the required capability"
  - concept: source_workflow
    action: reference
    status: verified
    source_material_refs: [portable-source-1]
    exact_native_destination: null
    mechanism: null
    discovery_evidence_refs: []
    verification_evidence_ref: null
    omission_reason: null
```

Each application artifact records one `skill_materializations` item for each
selected or explicitly omitted skill. A `materialized` or `reused_existing`
skill has exactly one `materialization_source`; never materialize both a local
definition and an upstream candidate for the same skill. Resolve and record the
source's full commit SHA and `accessed_date` at application time. Candidate
branches such as `main` are mutable references, not locks; do not carry a
research-time SHA forward as the application's source pin. If an upstream body
must be changed to meet harness compatibility rules, use `kind: local_adaptation`
and record the upstream influence under `adapted_from` rather than calling it a
direct upstream materialization.

`supporting_assets.required` lists non-skill files needed by the selected source;
`included` records those actually materialized, and each `omitted` asset needs
an exact path and reason. `fallback.used` is true only when the preferred source
was unavailable or incompatible and a different single source was selected;
record both sources and the reason. If no skill source is materialized, use an
applicable `selection_status`, set `materialization_source: null`, and set
`omission.omitted: true` with a reason. Never report a silent fallback or
omission.

An `omit` entry must include `omission_reason`. A `reference` entry points to
source material without creating a target destination; `source_material_refs`
are not native evidence refs and do not establish host support. A concept map with
`unknown` or `blocked` status cannot authorize approval to proceed or any target
write.

## Target File Map

The Target File Map is the approved, target-specific projection of the Concept
Map. It is created only after verified discovery and explicit user approval.

```yaml
file_map_id: file-map-123
concept_map_id: concept-map-123
status: unknown               # verified | unknown | blocked; an unknown entry is illustrative
layout_audit:
  status: unknown              # verified | unknown | blocked
  native_projection_preview: []
  source_tree_reproduction: unknown
  unapproved_source_tree_paths: []
  verification_evidence_ref: null
entries:
  - file_map_entry_id: file-1
    concept: workflow_lifecycle
    action: translate          # reuse | translate | reference | omit
    status: verified           # per-destination status
    source_material_refs: [portable-source-1]
    exact_native_destination: "exact target file, setting, API, or session"
    mechanism: "exact native load, invoke, or enforcement mechanism"
    discovery_evidence_refs: [source-1]
    verification_evidence_ref: source-1
    omission_reason: null
  - file_map_entry_id: file-2
    concept: unsupported_capability
    action: omit
    status: unknown
    source_material_refs: [portable-source-2]
    exact_native_destination: null
    mechanism: null
    discovery_evidence_refs: [source-2]
    verification_evidence_ref: null
    omission_reason: "No verified native destination exists"
```

Every `reuse` or `translate` entry must identify the exact destination and
mechanism and link to discovery evidence. Every `reference` or `omit` entry
must not invent a destination; every `omit` entry must state its reason. Each
entry has a per-destination `status`, using only `verified`, `unknown`, or
`blocked`.

`layout_audit.status` may be `verified` only when the preview is target-native,
`source_tree_reproduction` is `false`, and no unapproved source-tree path is
listed. A missing, failed, or unknown layout audit forbids approval with
`decision: proceed` and forbids target writes.

Unknown or blocked discovery, mapping, or file-map entries forbid approval with
`decision: proceed` and forbid target writes. Stale, contradictory, or
low-confidence evidence is not a valid basis for a verified entry.

## Ticket

```yaml
ticket_id: task-123
run_id: run-123
request: "Add Google OAuth login"
change_type: feature        # feature | bugfix | refactor | cosmetic | research | documentation
scope_hints:
  - knowledge/auth/index.md
target_refs:
  - src/auth/
acceptance_criteria:
  - "Users can sign in with Google"
  - "Invalid callback state is rejected"
tier: 2                     # 0 | 1 | 2
confidence: medium          # high | medium | low
clarification_needed: false
clarification_questions: []
assumptions: []
```

## Plan

```yaml
plan_id: plan-123
ticket_id: task-123
summary: "Add server-side OAuth state handling and callback validation"
execution:
  scheduler: dependency_aware
  parallel_independent_slices: true
  lifecycle:
    intake_complete_before_planner: true
    full_plan_complete_before_approval: true
    full_plan_complete_before_implementation: true
  parallel_specialist_roles: [test_engineer, implementer]
  specialist_overlap_constraints:
    only_listed_roles_may_overlap_active_specialist_work: true
    dependencies_must_be_ready: true
    scopes_files_resources_mutable_state_and_ordering_must_not_conflict: true
    sequence_builder_after_test_when_builder_depends_on_test_output: true
    verifier_reviewer_knowledge_curator_and_other_specialists_overlap_active_work: false
    all_test_engineer_and_implementer_work_completes_before_verification: true
    verification_completes_before_review: true
  default_mode: in_place_uncommitted
  retry_policy:
    max_retries_per_slice: 2
    retry_on:
      - verification_test_failure
      - acceptance_failure_with_valid_scope
      - verification_lint_failure
      - verification_build_failure
      - verification_check_failure
      - verifier_failure
    replan_only_on:
      - invalid_plan
      - scope_change
      - acceptance_criteria_change
      - dependency_invalidation
      - permission_invalidation
      - platform_invalidation
    ordinary_failure_route: retry_affected_implementer_slice
    ordinary_failures_restart_intake_or_planner: false
    exhausted_retry_route: escalate
    replan_requires_explicit_feedback_or_objective_plan_invalidation: true
    material_replan_requires_renewed_approval: true
  reentry_policy:
    intake:
      default_passes: 1
      allowed_triggers:
        - user_clarification_changes_ticket
        - newly_discovered_ticket_mismatch
    planner:
      default_passes: 1
      full_plan_before_approval: true
      full_plan_before_implementation: true
      allowed_triggers:
        - explicit_human_plan_feedback
        - invalid_plan
        - scope_change
        - acceptance_criteria_change
        - dependency_invalidation
        - permission_invalidation
        - platform_invalidation
tasks:
  - task_id: slice-1
    description: "Store OAuth state server-side"
    files:
      - src/auth/state.ts
    level: hard              # easy | hard
    depends_on: []            # readiness requires every listed dependency to complete
    parallel_eligible: true   # eligible only when ready and non-conflicting
    conflict_checks:
      files:
        - tests/auth/state.test.ts # test_subtask.file is part of conflict scope
      resources: []           # shared mutable resources require serialization
      state: []               # conflicting mutable state requires serialization
      ordering: []            # explicit ordering constraints require serialization
    acceptance:
      - "State expires after five minutes"
      - "State is single-use"
    test_subtask:
      action: create          # create | extend | none
      file: tests/auth/state.test.ts
      cases:
        - "expired state is rejected"
  - task_id: slice-2
    description: "Validate state in the callback"
    files:
      - src/auth/callback.ts
    level: easy
    depends_on: [slice-1]
    parallel_eligible: true
    conflict_checks:
      files: []
      resources: []
      state: []
      ordering: [slice-1]
    acceptance:
      - "Invalid state returns an authorization error"
regression_tests: []
assumptions: []
```

`depends_on` defines readiness: a task with no dependencies is ready when the
full Plan is approved, and a task with dependencies is ready only after all
listed tasks complete. `parallel_eligible` permits concurrent scheduling only
for Test Engineer and Implementer invocations after readiness and conflict
checks pass. A Builder that depends on test output waits for that Test Engineer
task. Overlapping files, shared resources, conflicting mutable state, or ordering
constraints serialize the affected tasks; `test_subtask.file` is part of the
slice's scheduled file scope and must be included in `conflict_checks.files` or
equivalent conflict analysis. Verifier, Reviewer, Knowledge Curator, and other
specialists never overlap active specialist work; verification follows all
test/build work, and review follows verification. These fields describe the
contract and do not implement a scheduler.

## Task Result

```yaml
task_id: slice-1
status: completed       # completed | failed | blocked | needs-replan
attempt: 1
retry:
  is_retry: false
  retry_of_attempt: null
  reason: null
recovery_state: pass     # pass | retry_implementer | replan | escalate | user_input
files_changed:
  - src/auth/state.ts
tests_run:
  - tests/auth/state.test.ts
summary: "Added expiring, single-use server-side state storage"
concerns: []
root_cause: null
```

## Verification Result

```yaml
status: passed          # passed | failed | blocked
affected_task_id: slice-1
affected_slice: slice-1
failure_classification: null  # observed failure: implementation_defect | test_failure | acceptance_failure | lint_failure | build_failure | check_failure | verifier_failure | invalid_plan | scope_change | dependency_invalidation | permission_failure | platform_failure | null
attempt: 1
retry_of_attempt: null
reentry_context: null  # example: {reason: verification_test_failure, prior_attempt: 1}
replan_trigger: null   # optional: null | invalid_plan | scope_change | acceptance_criteria_change | dependency_invalidation | permission_invalidation | platform_invalidation
evidence: []
recommended_action: pass  # retry_implementer | replan | escalate | user_input | pass
checks:
  - name: unit-tests
    status: passed
    command: "npm test -- state.test.ts"
    summary: "8 passed"
failures: []
acceptance_results:
  - criterion: "State is single-use"
    status: passed
```

`failure_classification` describes the observed failure. `replan_only_on` in the
Plan execution policy describes routing triggers; it is not another failure
classification. When a failure maps to a re-plan trigger, Verification Result
may include the optional `replan_trigger` field. Use `permission_failure` →
`permission_invalidation`, `platform_failure` → `platform_invalidation`, and a
criteria conflict → `acceptance_criteria_change`. `replan_trigger` is otherwise
`null` and may contain only one of the trigger names listed in its schema comment.

## Review Result

```yaml
status: approved        # approved | changes-requested | blocked
findings:
  - severity: medium
    title: "Missing concurrent callback test"
    file: tests/auth/callback.test.ts
    recommendation: "Add a test for duplicate callback submission"
```

## Knowledge Outcome

The full workflow requires a post-review Knowledge Curator assessment on every
run, without separate per-run opt-in. This contract also applies to independent
partial adoption of knowledge management, without requiring agents, models, or
run-state storage. Partial scopes without knowledge report `outside_scope`.

```yaml
applicable: true
status: no_change          # updated | no_change | blocked | outside_scope
reason: "Assessment found no eligible new durable learning beyond existing knowledge"
evidence: []               # references to assessed findings and relevant existing knowledge
files_changed: []          # completed writes only, including partial writes if blocked
checks:
  - status: not_applicable
    reason: "No knowledge writes were needed; no configured read-only checks apply"
remaining_work: []         # required, nonempty when blocked
```

All seven fields (`applicable`, `status`, `reason`, `evidence`, `files_changed`,
`checks`, `remaining_work`) are mandatory; lists may be empty only as their
conditions below allow. `reason` is mandatory and nonempty for every status. `applicable` is true for the
full workflow and partial scopes including knowledge management; it is false only
for an adoption scope without knowledge, which must use `outside_scope` and state
that adoption boundary in `reason`. An applicable assessment uses only `updated`,
`no_change`, or `blocked`; full workflow cannot claim `outside_scope`.

`updated` requires completed eligible, evidence-backed writes to the approved
configured system and passed applicable checks. Read relevant existing knowledge,
update or merge before creating redundant material, and preserve native mapping,
provenance, category protection, and approval safeguards. Record check results;
if no checks apply, explain that explicitly. `no_change` requires an actual
assessment with a reason such as duplicate, temporary, unsupported, code-obvious,
or otherwise no durable value. Empty writes alone do not establish assessment.
Missing approved paths, ambiguous write rules, failed writes, failed applicable
checks, unavailable required checks, or inability to assess required evidence are `blocked`, with the blocker
in `reason` and concrete `remaining_work`. Never invent destinations or report
blocked retention as `no_change`. Record completed partial writes separately;
they do not permit an `updated` outcome while required retention or checks remain.

Knowledge `checks` is a nonempty list of mappings with `status` and nonempty
`reason`. Allowed statuses are `passed`, `failed`, `blocked`, `not_run`, and
`not_applicable`. `passed` and `failed` also require the exact `command` and
supporting `evidence` references to retained output. Do not invent results.
`not_run` cannot satisfy an applicable required check; report the overall outcome
as `blocked` until it runs. `not_applicable` needs an explicit scope/configuration
reason; unavailability is not inapplicability. Check after the final topic,
metadata, navigation, and log write; an earlier check cannot certify a later write.
Mechanical success still requires substantive evidence/decision review. Keep
completed partial writes distinct from remaining work.

## Run Summary

```yaml
run_id: run-123
ticket_id: task-123
status: completed
files_changed:
  - src/auth/state.ts
  - src/auth/callback.ts
tests:
  passed: 20
  failed: 0
review: approved
reentry:
  intake_count: 1
  planner_count: 1
retries:
  total: 0
  by_task: {}
parallel_groups: []
serialized_conflicts: []
replan_reasons: []
native_discovery:
  status: verified             # verified | unknown | blocked
  discovery_id: discovery-123
  platform: codex
  platform_version: "release-or-channel"
  operating_mode: local
  host_runtime:
    name: runtime-name
    version: "runtime-version"
  source_records:
    - source_id: source-1
      status: verified       # verified | unknown | blocked
      source_url: https://first-party.example/docs/native-conventions
      source_path: null
      accessed_date: YYYY-MM-DD
      applicable_platform_version: "release-or-channel"
      applicable_operating_mode: local
      finding: "The host loads the verified native mechanism"
      confidence: high
      verification_evidence_ref: source-1
  native_destinations:
    - capability: main_agent_bootstrap
      status: verified       # verified | unknown | blocked
      exact_native_destination: "exact verified destination"
      mechanism: "exact load, invoke, or enforcement mechanism"
      verification_evidence_ref: source-1
      evidence_refs: [source-1]
  unknown_conventions: []
  stop_block_reasons: []
approval:
  status: approved            # pending | approved | ask_or_adjust | declined
  decision: proceed            # proceed | ask_or_adjust
  plan_id: plan-123
  recorded_at: YYYY-MM-DD
native_post_write_verification:
  required: true
  status: verified             # verified | unknown | blocked
  records:
    - capability: main_agent_bootstrap
      status: verified          # verified | unknown | blocked; per destination
      exact_native_destination: "exact verified destination"
      mechanism: "native diagnostic, effective-config view, registration/API result, or session check"
      verification_evidence_ref: verification-1
      evidence_id: verification-1
      source_url: null
      source_path: "/exact/path/to/verification-output-or-record"
      accessed_date: YYYY-MM-DD
      applicable_platform_version: "release-or-channel"
      applicable_operating_mode: local
      finding: "Host recognized, loaded, invoked, or enforced the destination"
      confidence: high
      result: verified
  limitations: []
knowledge_outcome:           # required; follows the Knowledge Outcome contract
  applicable: true
  status: no_change
  reason: "Assessment found no eligible new durable learning beyond existing knowledge"
  evidence: []
  files_changed: []
  checks:
    - status: not_applicable
      reason: "No knowledge writes were needed; no configured read-only checks apply"
  remaining_work: []
knowledge_updates: []        # completed knowledge writes; [] alone does not prove assessment
unresolved_risks: []
```

`native_discovery.status`, `unknown_conventions`, and `stop_block_reasons`
report discovery gaps without inventing a destination. `approval` records the
human decision that authorizes the approved Plan. `native_post_write_verification`
is required for every written native destination; every record has its own
`status` and canonical evidence fields. Its overall status is `verified` only
when every written destination has verified evidence. If any record is `unknown`
or `blocked`, the Run Summary must use that status, stop before additional target
writes, and must not claim that the destination was successfully recognized,
loaded, invoked, or enforced. Discovery or mapping with `unknown` or `blocked`
status also forbids `approval.decision: proceed` and target writes. All existing
Run Summary fields retain their prior meanings, including `reentry`, `retries`,
`parallel_groups`, `serialized_conflicts`, and `replan_reasons`.

`knowledge_outcome` is required and uses the Knowledge Outcome contract above.
Include completed writes in `knowledge_updates`, keeping it consistent with
`knowledge_outcome.files_changed`; partial completed writes may be listed for a
`blocked` outcome, with remaining work reported explicitly. An empty list is
valid with a reasoned `no_change`, a `blocked` outcome with no completed writes,
or an explicit `outside_scope` for partial adoption without knowledge. It never
proves assessment by itself. A blocked required knowledge outcome prevents the
Run Summary from claiming `status: completed`. Do not write run-specific learning
to this source repository's example knowledge tree by default.
