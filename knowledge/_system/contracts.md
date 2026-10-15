---
type: self
description: Knowledge metadata, lifecycle, action-log and outcome contracts
source_refs:
  - kind: local
    target: ../inbox/sources/agent-harness-concept-2026-10-15-a05a718/schemas/artifacts.md
updated: "2026-10-15"
status: current
---

# Knowledge maintenance contracts

This is the local projection of the knowledge-only contracts at
agent-harness-concept commit `a05a718dd96218abd077adc258b9bf484121a929`
(v0.3.0), accessed 2026-10-15. See the [adoption map](adoption.md) for provenance,
native destinations, protections, and asset decisions. Load the
[knowledge-base method](../../.codex/skills/knowledge-base/SKILL.md) for retrieval
and curation, and [Documentation and ADRs](../../.codex/skills/documentation-and-adrs/SKILL.md)
when assessing durable learning or maintaining decisions. These methods run in
the current assistant; this adoption does not require specialist agents.

## Knowledge Outcome

After substantive or non-trivial work, assess relevant existing knowledge and
return these seven fields in a retained task result or report. A concise user-facing
summary may link the complete result instead of displaying YAML each time.

```yaml
applicable: true
status: no_change
reason: "Assessment found no eligible new durable learning beyond existing knowledge"
evidence: []
files_changed: []
checks:
  - status: not_applicable
    reason: "No knowledge writes were needed and no configured check applies"
remaining_work: []
```

All seven fields are mandatory. `reason` is a nonempty explanation.
Use `applicable: true` for this project's knowledge-enabled work. `outside_scope`
and `applicable: false` apply only to an explicitly selected adoption scope that
excludes knowledge management; they cannot excuse omitted required behavior here.

- `updated`: eligible evidence-backed writes are complete in approved paths and
  all applicable final-write checks passed. If no check applies, explain why.
- `no_change`: assessment actually found only duplicate, temporary, unsupported,
  code-obvious, or otherwise non-durable information. Empty writes alone do not
  establish that assessment.
- `blocked`: required evidence cannot be assessed, paths or rules are unresolved,
  writes failed, or applicable required checks failed or cannot run. Report completed
  partial writes separately and make `remaining_work` nonempty. Do not report this
  as no learning or completed retention.

`evidence` contains typed references to assessed findings and existing knowledge.
`files_changed` lists completed writes, including partial writes for blocked work.
Lists may be empty only when the status and explanation justify that.

`checks` is a nonempty list. Each check has `status` and a nonempty `reason`.
Allowed statuses are `passed`, `failed`, `blocked`, `not_run`, and `not_applicable`.
`passed`/`failed` also require the exact `command` and typed `evidence` referencing
retained output. A required `not_run` check cannot satisfy completion; unavailability
means blocked, not inapplicable. A scope/configuration reason is required for
`not_applicable`.

Run [the configured check](../../scripts/knowledge/check.sh) after **all final
writes**, including metadata, hints, indexes, and the log. Earlier passing checks
do not certify later writes. Keep final output outside the maintained knowledge
tree and report it in the outcome; avoid an endless chain of self-certifying log
edits. Mechanical success does not prove claim truth or human acceptance.

## Typed references

`source_refs` is a nonempty list of mappings with `kind` and `target`:
`local`, `url`, `command`, or `artifact`. Local/artifact targets are page-relative,
must exist, and remain within the repository after symlink resolution. An artifact
identifies an exact retained file, without a fragment. HTTP(S) URLs need a hostname.
Commands are inert provenance: never execute them just to validate a reference,
and never treat a command alone as supporting evidence. Preserve claim-level
explanations of applicability, source dates, versions, and uncertainty in the body.

## Topic lifecycle

Write maintained topic frontmatter as block-style YAML, matching the templates:
plain mapping keys, two-space indentation, and block sequences for references.
Use the same style for the maintained `.yaml` layout and YAML action-log entries.
The checker accepts JSON-shaped input for compatibility; that is not the authoring
style for these human-maintained YAML surfaces. Keep ISO date/timestamp values
as quoted strings and preserve existing values when only normalizing formatting.

Ordinary topics require YAML `type`, one-line `description`, nonempty typed
`source_refs`, actual ISO `updated` date, and `status`. Types are `self`, `derived`,
`adr`, and `source-companion`. Ordinary statuses are `draft`, `current`, and
`superseded`; a superseded topic has a typed local/artifact `superseded_by` naming
an existing replacement. `current` identifies the maintained topic, not verified
production behavior or current external facts. A metadata migration date does not
re-date source access or imply fresh verification of claims.

Templates use explicit `<...>` replacement values with required shapes. Only
explicitly configured template paths get placeholder date/reference exemptions;
nonplaceholder references still resolve. Configured example topics need complete
real metadata, `example: true`, and an illustrative notice. They never prove project
decisions. Indexes, logs, navigation, companions, raw sources, examples and templates
are classified explicitly in [the layout](../validation-layout.yaml),
not inferred from filenames. ADR lifecycle is maintained in the
[ADR method](../../.codex/skills/documentation-and-adrs/SKILL.md).

## Action log

Actual new actions go in the `## Entries` YAML list in
[knowledge/log.md](../log.md). Keep historical prose unchanged.
Do not manufacture timestamps, acceptance, or check outcomes for older events.

```yaml
- timestamp: "<actual UTC YYYY-MM-DDTHH:MM:SSZ>"
  action: update
  paths:
    - "<existing repo-root-relative path>"
  evidence:
    - kind: artifact
      target: "<page-relative retained evidence file>"
  checks:
    - status: passed
      reason: "<what the actual check established>"
      command: "<exact command run>"
      evidence:
        - kind: artifact
          target: "<page-relative retained check output>"
```

This block is a schema illustration, not an event to append. Actions are `create`,
`update`, `merge`, `split`, `reconcile`, and `lint`. Timestamps are actual UTC ISO
values ending `Z`. Paths are existing repository-relative paths. Evidence is typed
and page-relative to the log. Check statuses follow Knowledge Outcome rules above.
Record one concise action for the actual durable change; no transcript or routine
no-op log entries. Final validation still runs after that entry is written.
