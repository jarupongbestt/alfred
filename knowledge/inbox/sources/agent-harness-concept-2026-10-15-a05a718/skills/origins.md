# Skill Origins and Provenance

This registry explains where the skill concepts came from. It is deliberately
explicit because the harness is intended to be copied or adapted by Claude, Codex,
OpenCode, Hermes, and other agents.

The skills are not claimed to be copied verbatim from any one runtime. `Adapted`
means the concept is based on a named source and rewritten for the portable
harness. `Synthesized` means it combines the referenced harness design with common
software-engineering practice. `Domain extension` means it is a placeholder for a
project-specific capability, not a skill supplied by this repository.

The table below records historical concept provenance: why this repository has a
skill and what it retains. It does not select the source to materialize in an
adopter project. That per-application choice belongs in the application artifact's
`materialization_source` and must follow the candidate registry in
[`../harness.yaml`](../harness.yaml). A matching upstream slug is only a candidate;
it does not establish authorship, origin, equivalence, or compatibility.

## Materialization source policy

- Every selected skill gets exactly one `materialization_source`. Never install
  the local definition and an upstream candidate as duplicate copies of the same
  skill.
- The `addyosmani/agent-skills` `main` references in `harness.yaml` are mutable
  candidate refs, not pinned sources. At application time, inspect the selected
  source and record its resolved full commit SHA and access date in the
  application artifact. Do not treat a research-time SHA as an installation lock.
- Exact same-slug direct candidates are listed for `context-engineering`,
  `test-driven-development`, `security-and-hardening`,
  and `doubt-driven-development`. They are candidates, not presumed compatible.
- `source-driven-development` remains local by default. Its upstream same-slug
  candidate is a narrower optional method for framework-documentation decisions,
  not an automatic replacement.
- `clarification`, `specification`, `task-decomposition`, `root-cause`,
  `code-review`, and `incremental-implementation` remain local by default.
  `interview-me`, `idea-refine`, `spec-driven-development`,
  `planning-and-task-breakdown`, `debugging-and-error-recovery`, and
  `code-review-and-quality` are optional methods only, not automatic equivalents.
- `incremental-implementation` stays local because the upstream same-slug skill
  includes per-slice verify/commit behavior that conflicts with this harness's
  execution and no-commit rules.
- The harness lifecycle, approval gates, role boundaries, no-commit default,
  concurrency policy, and artifact contracts override generic upstream methods.
  If adopting an upstream body requires changing its content to meet those rules,
  record the materialization as a `local_adaptation` with its upstream influence
  in provenance; do not claim the changed body is a direct upstream copy.
- Inspect selected upstream skill folders for supporting files. Record required,
  included, and omitted assets. If a source is incompatible or unavailable, record
  the fallback source and reason, or record an explicit omission reason.

| Skill | Origin type | Origin source(s) | What this harness keeps |
|---|---|---|---|
| `context-engineering` | Adapted | [template-harness](https://github.com/jarupongbestt/template-harness) | Small, role-specific contexts and distilled state in the Main Agent |
| `specification` | Synthesized | [template-harness](https://github.com/jarupongbestt/template-harness); requirements-engineering practice | Tickets and acceptance criteria that can be checked |
| `clarification` | Synthesized | [template-harness](https://github.com/jarupongbestt/template-harness); interview and idea-refinement practice | Resolve material ambiguity; use concise interviewing and refine rough ideas only as needed |
| `root-cause` | Adapted | [template-harness](https://github.com/jarupongbestt/template-harness) investigation workflow | Evidence-first tracing from symptom to cause; it is a reusable skill, not a permanent agent |
| `task-decomposition` | Adapted | [template-harness](https://github.com/jarupongbestt/template-harness) | Ordered, small, independently verifiable task slices |
| `source-driven-development` | Adapted | [knowledge-base](https://github.com/jarupongbestt/knowledge-base) | Navigate relevant knowledge and cite evidence before making decisions |
| `incremental-implementation` | Adapted | [template-harness](https://github.com/jarupongbestt/template-harness) | One approved slice at a time, smallest coherent change, no silent scope expansion |
| `test-driven-development` | Synthesized | [template-harness](https://github.com/jarupongbestt/template-harness); test-design / acceptance-criteria practice | Tests are derived from behavior and are separated from the Implementer's design |
| `code-review` | Synthesized | [template-harness](https://github.com/jarupongbestt/template-harness); standard code-review practice | Independent review of correctness, scope, regressions, and test quality |
| `security-and-hardening` | Synthesized | [template-harness](https://github.com/jarupongbestt/template-harness); standard secure-development practice | Risk-based scrutiny of sensitive boundaries and unsafe assumptions |
| `documentation-and-adrs` | Local adaptation | [knowledge-base](https://github.com/jarupongbestt/knowledge-base) | Record durable decisions, constraints, procedures, and recurring failures |
| `harness-artifacts` | Synthesized | [agent-harness](https://github.com/jarupongbestt/agent-harness) | Preserve structured artifact contracts and evidence fields across roles |
| `knowledge-base` | Adapted | [knowledge-base](https://github.com/jarupongbestt/knowledge-base) | Navigate, update, and lint the durable knowledge tree |
| `karpathy-guidelines` | Synthesized | [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876); [portable skill reference](https://github.com/multica-ai/andrej-karpathy-skills/tree/main/skills/karpathy-guidelines) | Think before acting, choose the simplest sufficient solution, keep edits surgical, and verify observable outcomes; rewritten as a concise portable skill |
| `doubt-driven-development` | Adapted | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main/skills/doubt-driven-development) | Main-Agent orchestration that sends a minimal packet for fresh-context adversarial review, reconciles evidence, and bounds follow-up; no mandatory external CLI/model |
| `human-readable-communication` | Local adaptation | [danyuchn/asd-ste100-skill v0.4.0](https://github.com/danyuchn/asd-ste100-skill/blob/7d4a135a199a5d7447c4886bcd7ffe742a627bc9/SKILL.md) | Familiar words, clear actors, focused topics, stable terms, and conditions beside actions; rewritten as a relaxed, language-aware Main Agent presentation method that preserves meaning and harness contracts |
| `frontend-ui` | Domain extension | Project-specific | Optional domain capability; no portable source is prescribed |
| `api-design` | Domain extension | Project-specific | Optional domain capability; no portable source is prescribed |
| `database-migrations` | Domain extension | Project-specific | Optional domain capability; no portable source is prescribed |
| `data-pipelines` | Domain extension | Project-specific | Optional domain capability; no portable source is prescribed |
| `cloud-infrastructure` | Domain extension | Project-specific | Optional domain capability; no portable source is prescribed |
| `observability` | Domain extension | Project-specific | Optional domain capability; no portable source is prescribed |

## Human-readable communication adaptation

The upstream influence is `danyuchn/asd-ste100-skill`, `SKILL.md` v0.4.0,
resolved at commit `7d4a135a199a5d7447c4886bcd7ffe742a627bc9` and accessed
2026-10-02. The inspected source assets were `SKILL.md`,
`references/writing-rules.md`, `examples/before-after.md`, `scripts/ste-lint.py`,
and `LICENSE`. This is a `local_adaptation`, not a direct upstream copy or an
ASD-STE100 compliance claim. Its materialization default is the single
[local definition](human-readable-communication/SKILL.md); the four existing
direct candidates retain their policies. Applications still resolve the chosen
local source and supporting assets before approval.

The adaptation retains the clarity principles while removing an approved English
dictionary requirement, strict English grammar, and enforced word caps. English
20-word instruction and 25-word description targets are optional editing prompts.
An informal "80%" aim is not a measured score. Thai and mixed-language prose use
natural local phrasing, with longer sentences or passive voice where useful.
Meaning, evidence, uncertainty, and obligations take priority over brevity.

Supporting-asset decisions:

- `LICENSE`: required and included as
  [human-readable-communication/LICENSE](human-readable-communication/LICENSE),
  preserving the full MIT notice and `Copyright (c) 2026 Dustin Yuchen Teng`.
- `references/writing-rules.md`: omitted; its strict English summary is replaced
  by the self-contained, relaxed local method.
- `examples/before-after.md`: omitted; some examples change obligation or add
  content, which conflicts with meaning preservation.
- `scripts/ste-lint.py`: omitted; hard English word caps and punctuation checks
  are incompatible with the approved multilingual method. No replacement linter
  or automatic rewriting mechanism is introduced.

## Provenance rules for future skills

Every new skill should add one row here with:

- an origin type
- a stable URL, file path, or explicit `project-specific` declaration
- a short description of what was adopted
- any meaningful rewrite or limitation

If a skill is derived from multiple sources, list all of them. If the sources
conflict, preserve the conflict for review instead of attributing a single source
to a blended rule.

## Documentation and ADRs local source

`documentation-and-adrs` materializes the single local
[definition](documentation-and-adrs/SKILL.md). Its historical influence remains
[knowledge-base](https://github.com/jarupongbestt/knowledge-base); this change does
not claim an upstream copy, invented pinned SHA, or new authorship. The local
adaptation supplies the harness's metadata, ADR lifecycle, human decision evidence,
and final-write integrity rules. The registry has no upstream candidate or local
fallback for this method. Applications resolve the actual selected local revision
and assets before approval. Include or translate the required ADR template and
knowledge contract through the approved native adapter map. Applicable final-write
checks remain mandatory, using a compatible existing target checker, translated
checks, or the optional Python 3.10+ standard-library reference checker. Only selection
of that reference checker requires its runtime and target layout/check command.
Illustrative ADR, log, and layout assets may remain references or be omitted with
reasons; inventory all dispositions and rewrite or remove projected links. Checker
maintainer tests are not automatically created, run, or copied into target projects.
