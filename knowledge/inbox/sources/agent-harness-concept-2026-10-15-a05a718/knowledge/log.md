# Knowledge Action Log

This log holds concise knowledge actions, not transcripts or routine task progress.
Read it for historical activity, contradictions, recurring failures, audit, or lint
context. No actual events are asserted by this example.

## Entries

```yaml
[]
```

## Entry format (illustrative only)

The example below is a schema guide outside Entries, not an event to append.
Replace every placeholder with observed facts before recording an actual action.
Paths are repository-root-relative existing paths; typed evidence targets are
page-relative. Actions are `create`, `update`, `merge`, `split`, `reconcile`, or
`lint`. Timestamps are actual UTC ISO timestamps ending in `Z`. Optional `run_id`
and `summary` identify the action concisely.

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

Every check has `status` and a nonempty `reason`. Allowed statuses are `passed`,
`failed`, `blocked`, `not_run`, and `not_applicable`; passed/failed require exact
`command` and retained evidence. Required failed or unavailable checks block
retention. `not_applicable` needs a scope/configuration reason, not unavailability.
Never invent timestamps or passes. Check after the final write, including an
appended log entry; earlier checks cannot certify later edits. Keep final output
as retained evidence and report actual results in Knowledge Outcome without
appending an endless series of self-certifying log events.
