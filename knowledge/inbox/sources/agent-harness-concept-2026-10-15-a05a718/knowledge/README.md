# Knowledge-Base Integration Example

This tree demonstrates durable project memory. It is source material, not a
default target layout or a destination for this repository's run-specific learning.
Discover and preserve a target's existing startup path, categories, protections,
log, and checks; propose missing configuration before writing.

## Included layout

```text
knowledge/
├── main.md
├── log.md
├── validation-layout.yaml
├── domain/
│   ├── index.md
│   ├── self/README.md
│   ├── derived/README.md
│   └── sources/README.md
├── _template/
│   ├── index.md
│   ├── self-topic.md
│   ├── derived-topic.md
│   ├── source-topic.md
│   └── adr.md
└── _example/
    ├── index.md
    ├── self/retry-backoff.md
    ├── self/adr-0001-knowledge-layout.md
    └── derived/field-reference.md
```

There are no actual domain topics or retained raw sources in this example.
`domain/` illustrates categories; never invent corresponding target domains.

## Read and write

Main Agent, Intake, and Planner follow [main.md](main.md), matching domain index
Navigation Hints, a relevant topic, then focused `source_refs` before broader
searches. If navigation is absent, stale, contradictory, or insufficient, record
why a narrow expansion is needed. Read [log.md](log.md) only for history,
contradictions, recurring failures, audit, or lint context.

Retain evidence-backed durable decisions, constraints, procedures, and recurring
failure patterns. Read existing topics first and prefer update/merge over duplicate
pages. Exclude transcripts, task diaries, copied code, and unsupported claims.
Protect raw inputs from normal editing; faithful external compilations are locked
until an explicit re-sync; internal findings and ADRs remain separate. Preserve
unresolved contradictions, provenance, versions, conditions, and exceptions.

Topic frontmatter includes `type`, one-line `description`, nonempty typed
`source_refs`, actual ISO `updated` date, and `status`. Ordinary statuses are
`draft`, `current`, and `superseded`; replacements must exist. See the
[knowledge-base method](../skills/knowledge-base/SKILL.md) and
[ADR method](../skills/documentation-and-adrs/SKILL.md) for precise contracts.
Templates use explicit `<...>` placeholders; actual examples require complete
metadata and `example: true`. Illustrations never prove real project decisions.

After approved topic changes, maintain metadata, links, hints/indexes, and actual
log entries, then check the final state. Curator always assesses full-workflow
learning after review and returns the authoritative
[Knowledge Outcome](../schemas/artifacts.md#knowledge-outcome). Missing approved
paths, failed writes, failed checks, and unavailable required checks are `blocked`.
A reasoned `no_change` means assessment found no eligible learning; partial
adoption without knowledge uses `outside_scope`.

## Mechanical validation

Applicable knowledge checks must run after the final knowledge write. An adoption
can reuse a compatible existing target checker, translate compatible checks, or
select the optional [reference checker](../scripts/validate_knowledge.py). Required
checks that fail or cannot run remain `blocked`. Selecting this checker requires
Python 3.10+ standard library only, with no third-party packages, installation step,
or virtual environment. Other adoptions do not require Python.

For the included source example, select a Python 3.10+ interpreter available on the
host (`python3` below) and run from the repository root:

```sh
python3 -B -S scripts/validate_knowledge.py --repo-root . --knowledge-root knowledge --layout knowledge/validation-layout.yaml
```

The [validator](../scripts/validate_knowledge.py) is read-only. Exit codes are
`0` valid, `1` knowledge errors, and `2` invocation/operational/configuration
errors. It validates the supported input forms without duplicate keys, required metadata, local
references, supported Markdown links/anchors, hints, ADR structure, and log entries.
It never executes command references, checks URL availability, proves claim truth,
or authenticates human decisions.

The [maintainer tests](../tests/test_validate_knowledge.py) exercise this provided
tool. They are not workflow-generated test artifacts and are not automatically
created, run, or copied into a consumer project:

```sh
python3 -B -S -m unittest discover -s tests -p test_validate_knowledge.py
```

### Supported input forms

The reference checker reads a bounded YAML subset for frontmatter, fenced log
entries, and CLI layout files; it is not a general YAML implementation. These
reader limits do not narrow the portable metadata/reference contract. A compatible
existing or translated target checker may support broader YAML syntax.

- One UTF-8 document with LF or CRLF, blank lines, and comments is supported.
  Empty content yields no value, then ordinary schema validation determines validity.
  Input is limited to 1 MiB and 64 container levels.
- Block mappings use nonempty string keys and a colon followed by whitespace or
  end of line. Block sequences use a dash followed by whitespace or end of line.
  Nested mappings/lists use consistent two-space structural increments; mapping
  continuation keys in sequence entries align two spaces after the dash. Tabs,
  inconsistent indentation, and indentless nesting are rejected.
- Sequence entries may be scalars, single-line flow containers, or mappings with
  aligned continuation keys and nested values. Single-line flow maps/lists may nest
  and include empty `{}`/`[]`; separators are required and trailing commas rejected.
  Strict JSON maps/lists, including multiline JSON, are supported. Duplicate keys
  are rejected at every block, flow, and JSON depth; complex/nonstring keys and
  JSON `NaN`/`Infinity` are rejected.
- Single-quoted strings use doubled single quotes; double-quoted strings use
  JSON-compatible escapes. Decoded quoted text, Unicode, and punctuation are
  preserved. Plain single-line strings include dates, UTC timestamps, paths, URLs,
  and placeholders. A colon without following whitespace and a hash without
  preceding whitespace remain text. Outside quotes, a whitespace-separated hash
  starts an inline comment; quoted hashes and URL fragments remain text.
- Case-insensitive `true`/`false` are booleans; `null`/`~` yield no value. Signed
  decimal integers and finite decimal/exponent numbers are recognized. Leading-zero
  integers, hex/octal/binary, sexagesimal, and nonfinite numbers are rejected.
  Dates/timestamps remain strings for semantic validation; API mapping inputs may
  still contain `datetime.date` values.
- YAML tags, anchors, aliases, and merge keys used as syntax are rejected; identical
  marker text in quotes or ordinary inert strings remains text. Block scalars,
  multiline scalar folding, explicit complex keys, directives, document separators
  or multiple documents, unquoted `yes`/`no`/`on`/`off`, unsupported escapes,
  malformed quoting, and invalid flow punctuation are rejected.

Malformed or unsupported frontmatter returns `METADATA_INVALID`; log input returns
`LOG_INVALID`; CLI layout input returns `CONFIG_INVALID` and exit `2`. Resource
limits use the same typed routes. Deterministic diagnostics identify the syntax
and line when available rather than guessing or executing parsed values.

The [explicit layout](validation-layout.yaml) classifies existing bounded paths
relative to the knowledge root: raw directories, companions, templates, examples,
indexes, navigation pages, and logs. No filename grants an exemption. Without a
layout these classifications are empty. Inside raw directories only explicitly
classified companions/navigation are interpreted; other raw content remains intact.
Unknown keys, invalid types/version, duplicate/missing/escaping paths, and
contradictory classifications are errors. An index inside a template directory
uses index rules. A normal companion outside raw content uses topic rules.

Local/artifact references are page-relative, must exist, and remain inside the
explicit repository root after symlink resolution. Artifacts name retained files,
not freeform run IDs. URL refs use HTTP(S) with a hostname; commands are inert and
insufficient evidence by themselves. Supported inline Markdown links use simple
destinations, optional angle brackets, and optional titles. Fragment checks support
Markdown ATX headings and explicit HTML IDs, percent decoding, Unicode lowercase
slugs, punctuation removal, whitespace hyphens, and duplicate suffixes. Reference
links, Setext fragment headings, complex nested/escaped parentheses, and fragments
on non-Markdown files are diagnosed as unsupported. Fenced/inline code is ignored.

An applied adapter includes or translates required knowledge rules and ADR structure
into approved native destinations, inventories included/translated/referenced/omitted
assets with reasons, rewrites or removes projected links and commands, and verifies
native loading. Illustrative ADR, log, and layout assets are not mandatory consumer
files; selecting this checker requires an actual target layout and command. It never
needs to copy this entire example tree.
