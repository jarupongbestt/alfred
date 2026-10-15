---
type: self
description: Knowledge checker operation, supported inputs and limits
source_refs:
  - kind: local
    target: ../../scripts/knowledge/validate_knowledge.py
updated: "2026-10-15"
status: current
---

# Knowledge validation

The read-only checker is pinned to agent-harness-concept
`a05a718dd96218abd077adc258b9bf484121a929`, accessed 2026-10-15.
Its active script is byte-identical to the retained source; see [adoption](adoption.md).

Run from the repository root:

```sh
sh scripts/knowledge/check.sh
```

The wrapper locates Python 3.10+ on PATH or the existing bundled Codex runtime;
`KNOWLEDGE_PYTHON` may choose an existing interpreter. No packages, installation,
virtual environment, credentials, or network access are needed. An unavailable
runtime is a blocked required check. Exit codes are 0 for valid, 1 for knowledge
errors, and 2 for configuration/operational errors.

The equivalent direct command with a compatible Python interpreter is:

```sh
python3 -B -S scripts/knowledge/validate_knowledge.py --repo-root . --knowledge-root knowledge --layout knowledge/validation-layout.yaml
```

Run after final topic/metadata/index/hints/log writes. The checker never executes
reference commands or checks URL availability. It does not prove claims or human
acceptance. References outside the repository are errors; preserve needed artifacts
inside the repository rather than exempting broken references. See the
[actual classifications](../validation-layout.yaml).

The reader limits below describe this reference implementation, not a narrowed
portable metadata contract. The upstream maintainer regression tests are retained
as source; they are not installed as consumer tests.

## Supported input forms


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

The [explicit layout](../validation-layout.yaml) classifies existing bounded paths
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
