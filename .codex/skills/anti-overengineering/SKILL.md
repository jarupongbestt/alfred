---
name: anti-overengineering
description: Keep task scope and effort proportional to the requested outcome. Use when choosing an approach, planning, executing, or reviewing work to prevent oversized solutions, unnecessary process, and continued expansion after the task is complete.
license: MIT
---

# Anti-Overengineering

Complete the user's actual task with the simplest adequate approach. Apply
these decisions throughout the work, including research and organization, not
only code. Keep the checks internal unless a decision needs user input.
Explicit user requirements and applicable project obligations take precedence.

## 1. Think before acting

- Establish the requested outcome, current authorization, and what counts as
  done. A discussion about possible approaches is not automatically a request
  to create files or execute the proposed solution.
- Start with the smallest plausible way to finish. Check whether an existing
  tool, configuration change, direct edit, or manual action already suffices.
  A one-off need does not automatically need a reusable system.
- Ask when an unresolved choice materially changes the result, scope, or
  authorization. For minor reversible details within an authorized task, use
  judgment and state consequential assumptions without interrupting the work.

## 2. Simplicity first

- Prefer existing code, tools, and platform features before adding new ones.
- Add features, dependencies, abstractions, configuration, or automation only
  for a present requirement or a demonstrated obstacle to completing it.
  Hypothetical future use is not enough.
- Allow a small amount of duplication when a shared abstraction would add more
  complexity than it removes. Judge simplicity by clarity and maintenance
  burden, not minimum line count.
- Scale research, planning, documentation, and testing to the actual task and
  risk. Do not create a framework, tracking system, or formal plan merely to
  handle a small task. Required workflow steps still apply.
- Preserve necessary correctness, validation, security, and reliability. A
  solution that omits required behavior is incomplete, even if it is smaller.

## 3. Keep changes surgical

- Make each change serve the requested outcome or a necessary dependency of
  that outcome. Follow existing conventions; remove leftovers introduced by
  your own changes.
- Do not turn a local fix into adjacent cleanup, a redesign, or a new workstream.
  Mention unrelated findings briefly only when they matter to the user.
- Before expanding the approach, identify the concrete requirement or failure
  the added work resolves. If there is none, drop it. If the expansion changes
  the agreed scope, explain the need and discuss it before proceeding.

## 4. Verify, then stop

- Use the smallest meaningful verification that establishes the requested
  result. Reuse existing checks where suitable; add tests when they protect
  behavior that matters, rather than to mirror a trivial edit.
- If verification fails, fix the demonstrated problem. Broaden investigation
  or repeat checks only when new evidence or required checks justify it.
- When the outcome is complete and appropriate checks pass, stop. Do not keep
  polishing, invent new acceptance criteria, or implement optional next steps.
- If blocked, report the concrete blocker and what would resolve it. Do not
  substitute an expanding workaround project for the requested result.
- Report the result, relevant verification, and material limitations concisely.
  Do not narrate this checklist or append a routine improvement backlog.

## Source

Adapted from the four principles in
[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills/blob/64723a49ea6117894304eb491f0d32a60570bf45/skills/karpathy-guidelines/SKILL.md),
commit `64723a49ea6117894304eb491f0d32a60570bf45`, accessed 2026-10-04.
The upstream skill declares MIT. This adaptation extends the guidance beyond
coding and adds proportional effort, discussion boundaries, and a stopping
condition; it replaces blanket clarification and line-count rules with judgment.
