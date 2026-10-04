---
name: knowledge-base
description: Maintain durable project knowledge when the user shares or corrects substantive project context, supplies project sources, or asks to navigate, curate, reconcile, or lint knowledge.
---

# Knowledge Base

Help a future reader find an accurate, applicable answer with less effort.
Follow `AGENTS.md` for repository-wide rules; use this workflow to decide whether
and how knowledge should change. No change is a valid outcome.

Apply the automatic knowledge capture rule in [AGENTS.md](../../../AGENTS.md).
A substantive project update activates this skill without an explicit save
request; a general question with no reusable project context usually does not.
Use the [task-domain gate](../../../knowledge/main.md#task-domain-gate) to route
updates, and preserve supported details with their uncertainty.

## Read

- Always read `knowledge/main.md` at run startup.
- Identify the relevant project domain under `knowledge/`, such as `db/` or
  `audit/`, then read that domain's `index.md` and matching topic.
- Treat `knowledge/_example/`, `knowledge/_template/`, and any illustrative
  `knowledge/domain/` folder as non-authoritative scaffolding. Never treat their
  contents as project facts; create real project domains under `knowledge/`.
- Read `knowledge/log.md` only for historical activity, contradictions, recurring
  failures, audit evidence, or lint context.
- Read files under the matching project's `sources/` only when the specific
  external evidence is needed.

## Decide before writing

Identify the future question or decision this knowledge will support, the
evidence behind it, and the gap in existing knowledge. Retain reusable facts,
constraints, decision rationale, proven procedures, and recurring failure
patterns. In progress updates, retain durable changes to scope, workflows,
decisions, and constraints; omit temporary task status and one-off outputs.
Preserve tentative user statements as tentative, with provenance; do not turn
speculation into established guidance.

Search the relevant domain by concept and likely aliases, then read candidate
pages rather than deciding from filenames or search snippets. Expand the search
to related domains only when overlap is plausible; do not audit the whole tree
for every write. Existing instructions and skills may already be the right home
for an operating rule; do not copy them into a new knowledge page.

Choose the smallest change that improves the reader's answer:

| Finding | Action |
| --- | --- |
| Existing content already covers the fact and its conditions | Skip the write; add evidence only if it materially changes confidence or applicability. |
| A topic needs a correction, useful detail, or stronger evidence | Revise its existing primary page. |
| Multiple pages repeat the same guidance for the same scope | Consolidate into a primary page and repair references. |
| A page mixes distinct questions and is difficult to navigate | Split by reader need, keeping shared guidance in one home; length alone is not a reason. |
| Evidence conflicts | Reconcile scope, version, authority, and uncertainty before changing the conclusion. |
| A reusable topic has a distinct scope with no suitable home | Create a page and add the necessary navigation. |

Use judgment rather than treating every row as a required operation. A new
source or a new task does not by itself justify a new derived or internal page.
Raw-source intake below still applies even when no derived page is needed.

## Curate the affected area

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

## Reconcile evidence and time

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

## Source-first intake

- Treat every file or external artifact received from the user as raw source
  material first.
- Place it unchanged in the correct project's `knowledge/<domain>/sources/`
  before extracting, summarizing, or deriving anything from it.
- If the domain is unclear, do not derive yet. Ask for the domain or hold the
  file under `knowledge/inbox/sources/` until it is triaged.
- Never edit or silently replace a raw source. Store a new version as a new
  source artifact and record the relationship in the derived page or index.

## Write

- In each project domain, `self/` holds internal discoveries, decisions,
  constraints, and gotchas.
- In each project domain, `derived/` holds faithful external-source compilations
  and requires provenance, including the exact source path and received or
  accessed date.
- In each project domain, `sources/` holds raw external material and is protected
  from normal edits.
- Indexes hold navigation, not detailed knowledge.
- Update indexes only when navigation changes.

Never silently overwrite contradictions or store the complete conversation.

## Finish

Review the changed pages and affected references for a clear primary answer,
preserved provenance and exceptions, unresolved contradictions, and unnecessary
duplication. Check that new or moved pages are reachable from the appropriate
index and that links and known generation paths still match.

Record one concise action-log entry for the actual durable change, including
consolidation or retirement when relevant. Do not log routine no-op decisions
or create a second topic page to document the same rule. Run the existing
knowledge linter if available and report any remaining limitation accurately.
Mechanical lint can catch structural problems; it cannot prove that two claims
mean the same thing or authorize their automatic consolidation.
