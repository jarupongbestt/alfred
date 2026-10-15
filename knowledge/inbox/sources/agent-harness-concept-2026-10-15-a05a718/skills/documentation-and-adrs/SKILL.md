---
name: documentation-and-adrs
description: Maintain focused durable documentation and ADRs with evidence, lifecycle history, and explicit human decision records.
---

# Documentation and ADRs

This is the local materialization default. Preserve its historical influence from
knowledge-base; source selection and provenance remain separate.

Use the target's discovered/approved knowledge categories and protection policy,
following [knowledge-base](../knowledge-base/SKILL.md). Read relevant existing
knowledge first; update or merge before creating another page. Retain durable,
evidence-backed constraints, procedures, decisions, and recurring failure causes.
Do not retain transcripts, routine diaries, copied code, or unsupported claims.

Write focused pages with complete YAML metadata and typed `source_refs`. Keep
indexes navigational, preserve raw sources, and change locked external compilations
only during an explicit source re-sync. Record versions, limitations, and unresolved
contradictions rather than overwriting the conflicting evidence.

## Architecture decision records

Use an ADR for a consequential decision whose alternatives, rationale, or history
will matter later. Place it in the target's approved internal decision category;
`self/` is only this repository's example. The reusable
[ADR template](../../knowledge/_template/adr.md) provides `Context`, `Decision`,
`Reasons`, `Rejected alternatives`, `Consequences`, `Open questions`, `History`,
and `Supersession`. Keep those sections and earlier history when changing status.

ADR frontmatter uses `type: adr` and the ordinary required metadata. Its statuses
are `Proposed`, `Accepted`, `Superseded`, and `Deprecated`:

- `Proposed` records a proposal without asserting human acceptance.
- `Accepted` requires `human_decision` with nonempty `actor`, actual ISO date
  `decided_at`, and an existing typed local/artifact `evidence_ref`. Read the
  retained human decision evidence; agent inference or a command alone cannot
  establish acceptance.
- `Superseded` requires typed local/artifact `superseded_by` pointing to an
  existing replacement, plus preserved `History` describing the transition.
- `Deprecated` requires nonempty `deprecation_reason` and preserved `History`.

Do not fabricate acceptance, timestamps, source references, or check outcomes.
When no human decision evidence exists, keep a proposal rather than writing an
Accepted record. The [illustrative ADR](../../knowledge/_example/self/adr-0001-knowledge-layout.md)
shows a Proposed record and does not assert a project decision.

Maintain affected metadata, references, indexes, navigation hints, and action
logs. Run the configured knowledge checks after the final write, including logs,
then return the Knowledge Outcome with actual results. Failed or unavailable
required checks are `blocked`; a reasoned assessment with no eligible learning
is `no_change`.

When materializing this method, the adapter must include or translate the required
ADR template and knowledge contract into approved native destinations and rewrite
references. Applicable final-write integrity checks remain mandatory; map them to
a compatible existing target checker, translated checks, or the optional reference
checker. Only selecting that checker requires its Python 3.10+ standard-library
runtime and target-specific layout/check command. Its maintainer tests are not
automatically created, run, or copied by workflow adoption. Inventory included,
translated, referenced, and omitted assets with reasons. The illustrative ADR,
log, and layout are reference examples, not required downstream files. Rewrite or
remove projected links; never install this repository's whole example knowledge tree.
