---
type: self
description: Pinned knowledge-management adoption map and native operating paths
source_refs:
  - kind: local
    target: ../inbox/sources/agent-harness-concept-2026-10-15-a05a718/manifest.json
updated: "2026-10-15"
status: current
---

# Knowledge-only adoption

This starter adopts the complete knowledge-management capability from
[agent-harness-concept](https://github.com/jarupongbestt/agent-harness-concept/tree/a05a718dd96218abd077adc258b9bf484121a929),
v0.3.0, commit `a05a718dd96218abd077adc258b9bf484121a929`, accessed 2026-10-15.
Required behavior is included or translated below. Agent orchestration, model
assignments, and persisted run state are outside this independently selectable
capability; the current assistant performs its assessment responsibilities.

## Target configuration

| Item | Native destination |
| --- | --- |
| Bootstrap | [AGENTS.md](../../AGENTS.md); Claude adapter imports it through [CLAUDE.md](../../CLAUDE.md) |
| System guidance | [Operating guides](index.md); project concepts and PRDs belong in `docs/` |
| Knowledge root / startup | [knowledge/main.md](../main.md) |
| Domains / categories | No real domains in the starter; `self/`, `derived/`, `sources/` |
| Templates | [knowledge/_template/index.md](../_template/index.md) |
| Action log | [knowledge/log.md](../log.md), structured Entries containing starter maintenance only |
| Classifications | [knowledge/validation-layout.yaml](../validation-layout.yaml) |
| Check command | `sh scripts/knowledge/check.sh` after the final write |
| Runtime | Existing Python 3.10+; wrapper discovers a compatible PATH or bundled interpreter, or uses `KNOWLEDGE_PYTHON` |
| Contracts / outcome | [contracts.md](contracts.md) |
| Verification evidence | [Starter verification](evidence/starter-check.json), generated for this clean export |

Skills are canonical in `.codex/skills/`. Set up `.agents/skills` and
`.claude/skills` as compatibility links using the [setup guide](getting-started.md#2-set-up-skill-compatibility-links);
they are not separate skill copies.
Both knowledge methods remain normally discoverable through SKILL.md frontmatter.
An existing session may need to read a newly added method by its explicit path;
registration in a later fresh skill catalog is not claimed without observation.

## Category protection and evidence

- `self/` contains internal/user-reported facts, constraints, procedures and ADRs.
  Retain user attribution and uncertainty. Ordinary automatic capture remains
  authorized by the working agreement.
- `sources/` contains immutable retained source bytes. Intake manifests and source
  registries authored here are metadata, not upstream raw content; extend them to
  describe new versions without rewriting old source files. The layout explicitly
  classifies only the retained upstream snapshot as raw content initially.
  Register each real source directory in the layout when adding a domain.
- `derived/` contains faithful external compilations. Its substantive content is
  locked against ordinary editorial rewriting: change it only in an explicitly
  authorized source re-sync/analysis scope. A user's request to inspect supplied
  source and update the related knowledge authorizes that scoped re-sync under
  automatic capture; do not repeatedly request the same permission. A new version
  is retained first, then the primary compilation records its source relationship,
  dates, limitations and conflicts. Internal conclusions go in `self/`.
- Mechanical metadata/link migrations that preserve claims, source dates and
  uncertainty are allowed within a maintenance task. They do not assert a fresh
  source review. Raw sources remain unchanged by such migrations.
- `inbox/sources/` is protected raw intake pending domain triage. No domain is
  invented merely to house harness operating rules. Those rules live in the instructions, methods and
  `knowledge/_system/` operating references; the upstream source remains in inbox.
- Templates/examples are explicitly classified scaffolding, not factual evidence.
  Keep task state outside durable knowledge; exact retained verification artifacts
  may live under `knowledge/_system/evidence/` to support this adoption record.

This distribution contains no real project domains, private attachments, outputs,
or local knowledge history. Its project-domain navigation starts empty; its log contains only starter maintenance. The retained
upstream snapshot is public source provenance, not personal project knowledge.

System guidance moved from `docs/` to `knowledge/_system/` on 2026-10-15.
Retained verification reports preserve their original bytes and historical
path strings; current links and classifications use the new locations.

## Methods

Both methods are `local_adaptation` projections from the pinned source above.
The [retained manifest](../inbox/sources/agent-harness-concept-2026-10-15-a05a718/manifest.json)
records exact paths, URLs and hashes. Compatibility review preserves required
contracts, native loading, category protections and the working agreement's
automatic capture scope; paths and supporting references are translated.
The historical knowledge-base influence of `documentation-and-adrs` is retained
by reference to upstream `skills/origins.md` in that snapshot.

| Upstream asset | Disposition / native destination | Reason or translation |
| --- | --- | --- |
| `skills/knowledge-base/SKILL.md` | Translated: [.codex/skills/knowledge-base/SKILL.md](../../.codex/skills/knowledge-base/SKILL.md) | Full retrieval/curation/metadata/log/check/outcome contract; retains source-first intake, contextual domain routing and scoped consolidation rules |
| `skills/documentation-and-adrs/SKILL.md` | Translated: [.codex/skills/documentation-and-adrs/SKILL.md](../../.codex/skills/documentation-and-adrs/SKILL.md) | Single local method; all ADR sections/status/human-evidence requirements retained; paths rewritten |
| `knowledge/_template/adr.md` | Included: [ADR template](../_template/adr.md) | Required structure; actual ADR creation remains conditional on consequential decisions |
| `knowledge/_template/self-topic.md` | Included: [internal template](../_template/self-topic.md) | Complete metadata/reference shapes |
| `knowledge/_template/derived-topic.md` | Included: [derived template](../_template/derived-topic.md) | Provenance and uncertainty retained |
| `knowledge/_template/source-topic.md` | Included: [companion template](../_template/source-topic.md) | Optional companion creation with required metadata when used |
| `knowledge/_template/index.md` | Translated: [index template](../_template/index.md) | Native category navigation and Task / Target hints |
| `knowledge/main.md` | Translated: [starter startup](../main.md) | Empty domain list and retained task-domain gate; required retrieval order |
| `knowledge/log.md` contract | Translated: [log](../log.md) and [entry contract](contracts.md#action-log) | Actual starter maintenance Entries; no private domain history or fabricated events |
| `knowledge/validation-layout.yaml` | Translated: [starter layout](../validation-layout.yaml) | Explicit target paths, raw protection and scaffold classifications |
| `knowledge/README.md` checker/input contract | Translated: [validation guide](validation.md) | Full supported input forms and limitations; native command/paths |
| `scripts/validate_knowledge.py` | Included byte-for-byte: [checker](../../scripts/knowledge/validate_knowledge.py) | Selected optional reference implementation; standard library, read-only |
| Checker runtime/entry point | Native adapter: [check.sh](../../scripts/knowledge/check.sh) | Runtime selection without installation; exit 2 when unavailable |
| `schemas/artifacts.md#Knowledge Outcome` | Translated: [Knowledge Outcome](contracts.md#knowledge-outcome) | All seven fields, status rules, typed evidence and final-check obligations |
| `prompts/knowledge-curator.md` | Responsibilities translated into current-assistant methods/bootstrap | Knowledge-only adoption does not require creating agents, model assignments or run-state files |
| Knowledge rules in `AGENTS.md`, `SPEC.md`, `harness.yaml`, `APPLY.md` | Referenced in retained snapshot; projected by bootstrap, methods and this map | Full knowledge contracts retained; unrelated orchestration contracts outside selected capability |
| `skills/origins.md` | Referenced in retained snapshot | Actual historical provenance; no invented upstream revision or authorship |
| Upstream illustrative ADR | Referenced by ADR method in retained snapshot | Demonstrates Proposed without asserting project acceptance; no fabricated consumer decision |
| Other upstream examples / example tree | Omitted as installation; fictional starter examples retained | Illustrative assets need not be copied; no whole-tree installation |
| `tests/test_validate_knowledge.py` | Retained source, omitted as active consumer tests | Maintainer tests are not automatically required consumer assets; real target checks are configured above |

## Conformance and limits

Required contracts are covered by the destinations above: configured paths and
protections; ordered retrieval/hints and bounded search; durable assessment and
meaning-preserving curation; typed metadata, references and lifecycle; explicit
scaffold classifications; documentation/ADR support; actual logs; final-write
integrity checks; authoritative Knowledge Outcome; and provenance/native loading.
The linked starter verification records structural checks and upstream hashes.
This inventory alone does not prove behavioral conformance or human acceptance.

Mechanical checks validate structure and references, not truth, remote URL
availability, production behavior or human decision authenticity. No historical
domain claims are included. Future domains must preserve their source dates,
caveats and user attributions. No real ADR is asserted by the starter.
