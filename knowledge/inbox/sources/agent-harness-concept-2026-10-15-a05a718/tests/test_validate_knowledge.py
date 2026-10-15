"""Acceptance tests for the public knowledge validator API and CLI.

Fixtures declare their own classification paths. They intentionally do not use
the source repository's example knowledge tree or validator internals.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


sys.dont_write_bytecode = True
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "validate_knowledge.py"
CLASSIFICATIONS = (
    "raw_source_dirs", "source_companion_files", "template_dirs",
    "example_dirs", "index_files", "navigation_files", "log_files",
)


def layout(**overrides):
    result = {"version": 1, **{name: [] for name in CLASSIFICATIONS}}
    result.update(overrides)
    return result


def metadata(**overrides):
    result = {
        "type": "self",
        "description": "A focused reusable observation.",
        "source_refs": [{"kind": "url", "target": "https://example.org/evidence"}],
        "updated": "2026-10-14",
        "status": "current",
    }
    result.update(overrides)
    return result


def page(fields=None, body="# Topic\n\nA supported observation.\n"):
    # JSON is a YAML subset; explicit strings avoid accidental date coercion.
    return "---\n" + json.dumps(metadata() if fields is None else fields, ensure_ascii=False) + "\n---\n\n" + body


ADR_BODY = "\n".join(
    "## " + heading + "\n\nRecorded explanation.\n"
    for heading in (
        "Context", "Decision", "Reasons", "Rejected alternatives",
        "Consequences", "Open questions", "History", "Supersession",
    )
)


class KnowledgeValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("knowledge_validator_public_api", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        cls.validate = staticmethod(module.validate_knowledge)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="knowledge-acceptance-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repository"
        self.knowledge = self.repo / "memory-store"
        self.knowledge.mkdir(parents=True)
        self.config = layout()
        self.write("topic.md", page())

    def write(self, relative, content):
        target = self.knowledge / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def diagnostics(self, config=None):
        result = self.validate(self.repo, self.knowledge, self.config if config is None else config)
        self.assertIsInstance(result, list)
        for diagnostic in result:
            self.assertIsInstance(diagnostic, dict)
            for key in ("path", "code", "message"):
                self.assertIsInstance(diagnostic.get(key), str)
                self.assertTrue(diagnostic[key], diagnostic)
        return result

    def assertValid(self):
        self.assertEqual([], self.diagnostics())

    def assertInvalid(self, relative=None):
        result = self.diagnostics()
        self.assertTrue(result, "invalid fixture was certified as valid")
        if relative is not None:
            self.assertTrue(any(relative in item["path"] for item in result), result)
        return result

    def test_minimal_valid_topic_and_none_layout(self):
        self.assertValid()
        self.assertEqual([], self.validate(self.repo, self.knowledge, None))

    def test_metadata_types_and_ordinary_statuses(self):
        for kind in ("self", "derived", "source-companion"):
            for status in ("draft", "current"):
                with self.subTest(kind=kind, status=status):
                    self.write("topic.md", page(metadata(type=kind, status=status)))
                    self.assertValid()

    def test_required_metadata_fields(self):
        self.assertValid()
        for key in metadata():
            with self.subTest(key=key):
                fields = metadata()
                del fields[key]
                self.write("topic.md", page(fields))
                self.assertInvalid("topic.md")

    def test_invalid_metadata_shapes(self):
        cases = {
            "type": ["unknown", 1, None],
            "description": ["", "two\nlines", [], None],
            "source_refs": [[], "evidence", ["evidence"], None],
            "updated": ["2026-02-30", "14/10/2026", "<date>", 20261014, None],
            "status": ["Accepted", "unknown", None],
        }
        for field, values in cases.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    self.write("topic.md", page(metadata(**{field: value})))
                    self.assertInvalid("topic.md")

    def test_frontmatter_requires_delimiters_and_mapping(self):
        for content in ("# No metadata\n", "---\ntype: self\n", "---\n- self\n---\n", "---\nnull\n---\n"):
            with self.subTest(content=content):
                self.write("topic.md", content)
                self.assertInvalid("topic.md")

    def test_yaml_duplicate_keys_and_unsafe_tags_rejected(self):
        valid_yaml = (
            "type: self\ndescription: Observation\nsource_refs:\n"
            "  - kind: url\n    target: https://example.org\n"
            "updated: 2026-10-14\nstatus: current\n"
        )
        self.write("topic.md", "---\n" + valid_yaml + "---\n")
        self.assertValid()  # Valid unquoted dates preserve semantic compatibility.
        for bad in (
            valid_yaml + "status: draft\n",
            valid_yaml.replace("description: Observation", "description: !!python/object/apply:os.system ['echo unsafe']"),
            valid_yaml.replace("    target: https://example.org", "    target: https://example.org\n    target: https://other.example.org"),
        ):
            with self.subTest(bad=bad):
                self.write("topic.md", "---\n" + bad + "---\n")
                self.assertInvalid("topic.md")

    def test_reference_kinds_and_targets(self):
        self.write("proof.txt", "retained evidence")
        (self.repo / "outside-knowledge.txt").write_text("project evidence", encoding="utf-8")
        refs = [
            {"kind": "local", "target": "proof.txt"},
            {"kind": "local", "target": "."},
            {"kind": "artifact", "target": "../outside-knowledge.txt"},
            {"kind": "url", "target": "https://example.org:443/path?q=value#fragment"},
            {"kind": "command", "target": "git diff --check"},
        ]
        self.write("topic.md", page(metadata(source_refs=refs)))
        self.assertValid()
        for ref in (
            {"kind": "unknown", "target": "proof.txt"},
            {"kind": "local", "target": ""}, {"kind": "local", "target": 4},
            {"target": "proof.txt"}, {"kind": "url"},
            {"kind": "local", "target": "missing.md"},
            {"kind": "artifact", "target": "run-123"},
            {"kind": "url", "target": "ftp://example.org/file"},
            {"kind": "url", "target": "https:///missing-host"},
        ):
            with self.subTest(ref=ref):
                self.write("topic.md", page(metadata(source_refs=[ref])))
                self.assertInvalid("topic.md")

    def test_reference_resolution_is_page_relative_and_percent_decoded(self):
        self.write("nested/proof file.txt", "evidence")
        self.write("nested/topic.md", page(metadata(source_refs=[{"kind": "artifact", "target": "proof%20file.txt"}])))
        self.assertValid()

    def test_local_reference_cannot_escape_repository(self):
        (self.base / "secret.txt").write_text("outside", encoding="utf-8")
        for target in ("../../secret.txt", "%2e%2e/%2e%2e/secret.txt", str(self.base / "secret.txt")):
            with self.subTest(target=target):
                self.write("topic.md", page(metadata(source_refs=[{"kind": "local", "target": target}])))
                self.assertInvalid("topic.md")

    def test_symlink_reference_uses_realpath_containment(self):
        secret = self.base / "secret.txt"
        secret.write_text("outside", encoding="utf-8")
        (self.knowledge / "escaped.txt").symlink_to(secret)
        self.write("topic.md", page(metadata(source_refs=[{"kind": "artifact", "target": "escaped.txt"}])))
        self.assertInvalid("topic.md")

    def test_commands_are_never_executed(self):
        marker = self.repo / "should-never-exist"
        command = f"touch {marker}"
        self.write("topic.md", page(metadata(source_refs=[{"kind": "command", "target": command}])))
        self.diagnostics()
        self.assertFalse(marker.exists())

    def test_supported_markdown_links_titles_angles_and_encoded_targets(self):
        self.write("proof file.txt", "evidence")
        body = '# Topic\n[plain](proof%20file.txt) [angle](<proof file.txt>) [title](proof%20file.txt "Evidence")\n'
        self.write("topic.md", page(body=body))
        self.assertValid()

    def test_supported_unicode_duplicate_heading_and_html_anchors(self):
        self.write("anchors.md", page(body="# Café 世界!\n# Repeated\n# Repeated\n<a id=\"Exact-ID\"></a>\n"))
        for fragment in ("caf%C3%A9-%E4%B8%96%E7%95%8C", "repeated", "repeated-1", "Exact-ID"):
            with self.subTest(fragment=fragment):
                self.write("topic.md", page(body=f"# Topic\n[anchor](anchors.md#{fragment})\n"))
                self.assertValid()
        self.write("topic.md", page(metadata(source_refs=[{"kind": "local", "target": "anchors.md#repeated-1"}])))
        self.assertValid()

    def test_missing_markdown_target_and_anchor_are_errors(self):
        for target in ("absent.md", "topic.md#absent"):
            with self.subTest(target=target):
                self.write("topic.md", page(body=f"# Topic\n[broken]({target})\n"))
                self.assertInvalid("topic.md")

    def test_inline_and_fenced_code_are_ignored(self):
        body = (
            "# Topic\n`[not a link](absent.md)`\n"
            "```markdown\n[not a link](absent.md)\n```\n"
            "~~~markdown\n[not a link](absent.md)\n~~~\n"
        )
        self.write("topic.md", page(body=body))
        self.assertValid()

    def test_frontmatter_inert_command_is_not_markdown_prose(self):
        # R1: exact independently reproduced reviewer fixture.
        self.write("topic.md", (
            '---\n{"type": "self", "description": "Observation", '
            '"source_refs": [{"kind": "command", "target": "printf \'[sample](absent.md)\'"}, '
            '{"kind": "url", "target": "https://example.org"}], '
            '"updated": "2026-10-14", "status": "current"}\n---\n# Topic\n'
        ))
        self.assertValid()

    def test_log_body_prose_link_is_checked_outside_yaml_fence(self):
        # R2: empty valid Entries must not exempt the log's ordinary prose.
        self.config = layout(log_files=["actions.md"])
        self.write("actions.md", "# Actions\n[missing](absent.md)\n## Entries\n```yaml\n[]\n```\n")
        self.assertInvalid("actions.md")

    def test_unequal_backtick_runs_cannot_hide_broken_prose_link(self):
        # R3: the unmatched single run cannot close at part of a double run.
        self.write("topic.md", (
            '---\n{"type": "self", "description": "Observation", '
            '"source_refs": [{"kind": "url", "target": "https://example.org"}], '
            '"updated": "2026-10-14", "status": "current"}\n---\n'
            '# Topic\n` unmatched\n[broken](absent.md)\n``some literal``\n'
        ))
        self.assertInvalid("topic.md")

    def test_complete_equal_length_multiline_backticks_are_code(self):
        for code in (
            '`literal\n[missing](absent.md)\ncontinued`',
            '``literal ` single\n[missing](absent.md)\ncontinued``',
            '```literal `` double\n[missing](absent.md)\ncontinued```',
        ):
            with self.subTest(code=code):
                # Start the inline span within a prose line, not as a fence.
                self.write("topic.md", page(body="# Topic\nExample " + code + " end.\n"))
                self.assertValid()

    def test_code_span_does_not_hide_following_prose_link(self):
        self.write("topic.md", page(body="# Topic\nExample ``literal ` tick`` [broken](absent.md)\n"))
        self.assertInvalid("topic.md")

    def test_plain_id_text_is_not_an_html_anchor(self):
        # R4: exact reviewer fixture has text, but no HTML element or heading.
        self.write("topic.md", (
            '---\n{"type": "self", "description": "Observation", '
            '"source_refs": [{"kind": "url", "target": "https://example.org"}], '
            '"updated": "2026-10-14", "status": "current"}\n---\n'
            '# Topic\nid="fake"\n[broken](#fake)\n'
        ))
        self.assertInvalid("topic.md")

    def test_frontmatter_id_text_is_not_a_markdown_anchor(self):
        self.write("topic.md", (
            '---\ntype: self\ndescription: \'Observation id="metadata-only"\'\n'
            'source_refs:\n  - kind: url\n    target: https://example.org\n'
            'updated: 2026-10-14\nstatus: current\n---\n'
            '# Topic\n[broken](#metadata-only)\n'
        ))
        self.assertInvalid("topic.md")

    def test_explicit_html_element_id_defines_anchor(self):
        self.write("topic.md", page(body='# Topic\n<span id="real">Evidence</span>\n[valid](#real)\n'))
        self.assertValid()

    def test_unsupported_link_and_fragment_forms_are_diagnosed(self):
        self.write("plain.txt", "Heading\n")
        self.write("setext.md", page(body="Setext Heading\n==============\n"))
        self.write("file(part).txt", "evidence")
        bodies = (
            "[reference][proof]\n\n[proof]: topic.md\n",
            "[nested](file(part).txt)\n",
            r"[escaped](file\(part\).txt)" + "\n",
            "[setext](setext.md#setext-heading)\n",
            "[nonmarkdown](plain.txt#heading)\n",
        )
        for body in bodies:
            with self.subTest(body=body):
                self.write("topic.md", page(body="# Topic\n" + body))
                self.assertInvalid("topic.md")

    def test_ordinary_supersession_requires_existing_typed_replacement(self):
        self.write("replacement.md", page())
        self.write("topic.md", page(metadata(status="superseded", superseded_by={"kind": "local", "target": "replacement.md"})))
        self.assertValid()
        for replacement in (None, "replacement.md", {"kind": "url", "target": "https://example.org"}, {"kind": "command", "target": "echo evidence"}, {"kind": "artifact", "target": "missing.md"}):
            with self.subTest(replacement=replacement):
                fields = metadata(status="superseded")
                if replacement is not None:
                    fields["superseded_by"] = replacement
                self.write("topic.md", page(fields))
                self.assertInvalid("topic.md")

    def test_adr_proposed_and_accepted_evidence(self):
        self.write("decision.txt", "Actual retained human decision evidence.")
        self.write("topic.md", page(metadata(type="adr", status="Proposed"), ADR_BODY))
        self.assertValid()
        decision = {"actor": "Human reviewer", "decided_at": "2026-10-14", "evidence_ref": {"kind": "artifact", "target": "decision.txt"}}
        self.write("topic.md", page(metadata(type="adr", status="Accepted", human_decision=decision), ADR_BODY))
        self.assertValid()
        for changes in (
            {"actor": ""}, {"decided_at": "2026-02-30"},
            {"evidence_ref": {"kind": "command", "target": "echo approved"}},
            {"evidence_ref": {"kind": "url", "target": "https://example.org"}},
            {"evidence_ref": {"kind": "artifact", "target": "missing.txt"}},
        ):
            with self.subTest(changes=changes):
                invalid = {**decision, **changes}
                self.write("topic.md", page(metadata(type="adr", status="Accepted", human_decision=invalid), ADR_BODY))
                self.assertInvalid("topic.md")
        self.write("topic.md", page(metadata(type="adr", status="Accepted"), ADR_BODY))
        self.assertInvalid("topic.md")

    def test_adr_superseded_and_deprecated_require_reason_history_and_replacement(self):
        self.write("replacement.md", page(metadata(type="adr", status="Proposed"), ADR_BODY))
        cases = (
            metadata(type="adr", status="Superseded", superseded_by={"kind": "artifact", "target": "replacement.md"}),
            metadata(type="adr", status="Deprecated", deprecation_reason="The underlying requirement ended."),
        )
        for fields in cases:
            with self.subTest(status=fields["status"]):
                self.write("topic.md", page(fields, ADR_BODY))
                self.assertValid()
                self.write("topic.md", page(fields, ADR_BODY.replace("## History", "## Previous records")))
                self.assertInvalid("topic.md")
                incomplete = dict(fields)
                del incomplete["superseded_by" if fields["status"] == "Superseded" else "deprecation_reason"]
                self.write("topic.md", page(incomplete, ADR_BODY))
                self.assertInvalid("topic.md")

    def test_adr_ordinary_status_is_invalid(self):
        self.write("topic.md", page(metadata(type="adr", status="current"), ADR_BODY))
        self.assertInvalid("topic.md")

    def test_explicit_nonstandard_raw_directory_is_uninterpreted(self):
        self.write("imports-unparsed/broken.md", "---\nunsafe: !!python/object/apply:os.system ['false']\n---\n[broken](absent.md)\n")
        self.config = layout(raw_source_dirs=["imports-unparsed"])
        self.assertValid()

    def test_raw_companion_and_navigation_exceptions_are_explicit(self):
        self.write("imports/source.md", "raw arbitrary source text")
        self.write("imports/notes.md", page(metadata(type="source-companion")))
        self.write("imports/menu.md", "# Sources\n[Source](source.md)\n")
        self.config = layout(raw_source_dirs=["imports"], source_companion_files=["imports/notes.md"], navigation_files=["imports/menu.md"])
        self.assertValid()
        self.write("imports/notes.md", page(metadata(type="self")))
        self.assertInvalid("imports/notes.md")
        self.write("imports/notes.md", page(metadata(type="source-companion")))
        self.write("imports/menu.md", "[broken](missing.md)\n")
        self.assertInvalid("imports/menu.md")

    def test_configured_templates_allow_placeholders_but_require_shapes(self):
        self.config = layout(template_dirs=["patterns"])
        fields = metadata(updated="<YYYY-MM-DD>", source_refs=[{"kind": "local", "target": "<evidence-path>"}])
        self.write("patterns/topic.md", page(fields))
        self.assertValid()
        del fields["description"]
        self.write("patterns/topic.md", page(fields))
        self.assertInvalid("patterns/topic.md")

    def test_template_real_references_and_links_are_checked(self):
        self.config = layout(template_dirs=["patterns"])
        fields = metadata(updated="<YYYY-MM-DD>", source_refs=[{"kind": "local", "target": "missing.txt"}])
        self.write("patterns/topic.md", page(fields))
        self.assertInvalid("patterns/topic.md")
        fields["source_refs"] = [{"kind": "local", "target": "<evidence-path>"}]
        self.write("patterns/topic.md", page(fields, "# Topic\n[broken](missing.txt)\n"))
        self.assertInvalid("patterns/topic.md")

    def test_actual_pages_and_examples_have_no_placeholder_exemption(self):
        self.write("topic.md", page(metadata(updated="<YYYY-MM-DD>")))
        self.assertInvalid("topic.md")
        self.write("topic.md", page())
        self.config = layout(example_dirs=["illustrations"])
        self.write("illustrations/example.md", page(metadata(example=True)))
        self.assertValid()
        for fields in (metadata(), metadata(example=False), metadata(example=True, updated="<YYYY-MM-DD>")):
            with self.subTest(fields=fields):
                self.write("illustrations/example.md", page(fields))
                self.assertInvalid("illustrations/example.md")

    def test_special_filenames_do_not_infer_exemptions(self):
        for name in ("README.md", "index.md", "main.md", "log.md", "_template/topic.md", "sources/raw.md"):
            with self.subTest(name=name):
                target = self.write(name, "# Unclassified page\n")
                self.assertInvalid(name)
                target.unlink()

    def test_navigation_pages_check_links_without_topic_metadata(self):
        self.write("start.md", "# Start\n[Topic](topic.md)\n")
        self.config = layout(navigation_files=["start.md"])
        self.assertValid()
        self.write("start.md", "# Start\n[Broken](missing.md)\n")
        self.assertInvalid("start.md")

    def test_index_hints_table_and_explicit_empty_state(self):
        self.config = layout(index_files=["guide.md"])
        for content in (
            "# Guide\n\n## Navigation Hints\n\n| Task | Target |\n| --- | --- |\n| Find topic | [Topic](topic.md) |\n",
            "# Guide\n\n## Navigation Hints\n\nNo navigation hints yet.\n",
        ):
            with self.subTest(content=content):
                self.write("guide.md", content)
                self.assertValid()

    def test_index_hints_missing_broken_untyped_and_multiple_targets(self):
        self.config = layout(index_files=["guide.md"])
        for content in (
            "# Guide\n",
            "## Navigation Hints\nNothing currently.\n",
            "## Navigation Hints\n| Task | Target |\n| --- | --- |\n| Find | topic.md |\n",
            "## Navigation Hints\n| Task | Target |\n| --- | --- |\n| Find | [Missing](absent.md) |\n",
            "## Navigation Hints\n| Task | Target |\n| --- | --- |\n| Find | [Remote](https://example.org) |\n",
            "## Navigation Hints\n| Task | Target |\n| --- | --- |\n| Find | [One](topic.md) [Two](topic.md) |\n",
        ):
            with self.subTest(content=content):
                self.write("guide.md", content)
                self.assertInvalid("guide.md")

    def test_index_inside_template_uses_index_rules(self):
        self.write("patterns/guide.md", "# Guide\n## Navigation Hints\nNo navigation hints yet.\n")
        self.config = layout(template_dirs=["patterns"], index_files=["patterns/guide.md"])
        self.assertValid()
        self.write("patterns/guide.md", "# Guide\n")
        self.assertInvalid("patterns/guide.md")

    def log_entry(self, **overrides):
        result = {
            "timestamp": "2026-10-14T01:02:03Z", "action": "update",
            "paths": ["memory-store/topic.md"],
            "evidence": [{"kind": "artifact", "target": "../check.txt"}],
            "checks": [{"status": "passed", "reason": "Check completed successfully.", "command": "python check.py", "evidence": [{"kind": "artifact", "target": "../check.txt"}]}],
            "run_id": "fixture-run", "summary": "Recorded change.",
        }
        result.update(overrides)
        return result

    def write_log(self, entries):
        (self.repo / "check.txt").write_text("retained result", encoding="utf-8")
        self.config = layout(log_files=["actions.md"])
        self.write("actions.md", "# Actions\n\n## Entries\n\n```yaml\n" + json.dumps(entries) + "\n```\n")

    def test_log_empty_entries_and_examples_outside_entries(self):
        self.write_log([])
        self.assertValid()
        self.write("actions.md", "# Actions\n## Format example\n```yaml\n- timestamp: <date>\n```\n## Entries\n```yaml\n[]\n```\n")
        self.assertValid()

    def test_log_valid_actions_and_check_statuses(self):
        for action in ("create", "update", "merge", "split", "reconcile", "lint"):
            with self.subTest(action=action):
                self.write_log([self.log_entry(action=action)])
                self.assertValid()
        for status in ("failed", "blocked", "not_run", "not_applicable"):
            with self.subTest(status=status):
                check = {"status": status, "reason": "A recorded reason."}
                if status == "failed":
                    check.update(command="python check.py", evidence=[{"kind": "artifact", "target": "../check.txt"}])
                self.write_log([self.log_entry(checks=[check])])
                self.assertValid()

    def test_log_required_fields_and_schema(self):
        for key in ("timestamp", "action", "paths", "evidence", "checks"):
            with self.subTest(key=key):
                entry = self.log_entry()
                del entry[key]
                self.write_log([entry])
                self.assertInvalid("actions.md")
        for changes in (
            {"timestamp": "2026-10-14T01:02:03+00:00"}, {"timestamp": "2026-02-30T01:02:03Z"},
            {"timestamp": "<timestamp>"}, {"action": "delete"},
            {"paths": ["missing.md"]}, {"paths": ["../secret.txt"]},
            {"evidence": []}, {"evidence": ["result"]}, {"checks": []},
            {"checks": [{"status": "unknown", "reason": "Reason"}]},
            {"checks": [{"status": "not_run", "reason": ""}]},
        ):
            with self.subTest(changes=changes):
                self.write_log([self.log_entry(**changes)])
                self.assertInvalid("actions.md")

    def test_log_passed_failed_need_exact_command_and_evidence(self):
        for status in ("passed", "failed"):
            for changes in ({"command": ""}, {"evidence": []}, {"evidence": [{"kind": "artifact", "target": "missing.txt"}]}, {"command": "<command>"}):
                with self.subTest(status=status, changes=changes):
                    check = {"status": status, "reason": "Recorded result.", "command": "python check.py", "evidence": [{"kind": "artifact", "target": "../check.txt"}]}
                    check.update(changes)
                    self.write_log([self.log_entry(checks=[check])])
                    self.assertInvalid("actions.md")

    def test_layout_invalid_fields_types_versions_missing_duplicates_and_escapes(self):
        self.write("patterns/pattern.md", page())
        (self.base / "outside").mkdir()
        invalid = (
            {"version": 2}, {"version": "1"}, {"version": True},
            {"unknown_field": []}, {"raw_source_dirs": "patterns"},
            {"raw_source_dirs": [1]}, {"raw_source_dirs": ["absent"]},
            {"raw_source_dirs": ["patterns", "patterns"]},
            {"raw_source_dirs": ["../../outside"]},
            {"template_dirs": ["patterns"], "example_dirs": ["patterns"]},
            {"navigation_files": ["topic.md"], "log_files": ["topic.md"]},
            {"source_companion_files": ["topic.md"], "navigation_files": ["topic.md"]},
        )
        for changes in invalid:
            with self.subTest(changes=changes):
                result = self.diagnostics(layout(**changes))
                self.assertTrue(any(item["code"] == "CONFIG_INVALID" for item in result), result)

    def test_layout_symlink_escape_is_configuration_error(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.knowledge / "unbounded").symlink_to(outside, target_is_directory=True)
        result = self.diagnostics(layout(raw_source_dirs=["unbounded"]))
        self.assertTrue(any(item["code"] == "CONFIG_INVALID" for item in result), result)

    def test_diagnostics_deterministic_and_validation_read_only(self):
        self.write("topic.md", page(body="# Topic\n[Missing](missing.md)\n"))
        self.write("other.md", "# Missing metadata\n")
        before = self.snapshot()
        first = self.diagnostics()
        self.assertTrue(first)
        self.assertEqual(first, self.diagnostics())
        self.assertEqual(before, self.snapshot())

    def snapshot(self):
        return {str(p.relative_to(self.repo)): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.repo.rglob("*") if p.is_file()}

    def cli(self, *extra, cwd=None, no_site=False):
        args = [sys.executable, "-B"]
        if no_site:
            args.append("-S")
        args.extend([str(SCRIPT), "--repo-root", str(self.repo), "--knowledge-root", str(self.knowledge), *extra])
        return subprocess.run(args, cwd=cwd or self.base, text=True, capture_output=True, timeout=15)

    def test_cli_valid_invalid_and_read_only(self):
        config_path = self.base / "layout.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        before = self.snapshot()
        valid = self.cli("--layout", "layout.json", cwd=self.base)
        self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
        self.assertEqual(before, self.snapshot())
        self.write("topic.md", "# Missing metadata\n")
        before = self.snapshot()
        invalid = self.cli("--layout", "layout.json", cwd=self.base)
        self.assertEqual(1, invalid.returncode, invalid.stdout + invalid.stderr)
        self.assertIn("topic.md", invalid.stdout + invalid.stderr)
        self.assertEqual(before, self.snapshot())

    def test_cli_configuration_and_invocation_errors_exit_two(self):
        config_path = self.base / "layout.yaml"
        for content in (
            "version: 2\n", "version: 1\nversion: 1\n",
            "version: !!python/object/apply:os.system ['false']\n",
        ):
            with self.subTest(content=content):
                config_path.write_text(content, encoding="utf-8")
                result = self.cli("--layout", str(config_path))
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        result = self.cli("--layout", "missing-layout.yaml")
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        result = self.cli("--unknown-option")
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)

    def test_stdlib_api_and_cli_startup_without_dependency_environment(self):
        # The fixture is unrelated to the source checkout and has no manifest.
        unrelated = self.base / "unrelated-working-directory"
        unrelated.mkdir()
        self.assertFalse((self.repo / "requirements-knowledge.txt").exists())
        before = self.snapshot()
        program = (
            "import importlib.util, pathlib, sys; "
            "assert 'site' not in sys.modules; "
            "spec=importlib.util.spec_from_file_location('public_checker', sys.argv[1]); "
            "module=importlib.util.module_from_spec(spec); "
            "sys.modules[spec.name]=module; spec.loader.exec_module(module); "
            "result=module.validate_knowledge(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])); "
            "assert result == [], result"
        )
        result = subprocess.run(
            [sys.executable, "-B", "-S", "-c", program, str(SCRIPT), str(self.repo), str(self.knowledge)],
            cwd=unrelated, text=True, capture_output=True, timeout=15,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        result = self.cli(cwd=unrelated, no_site=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, self.snapshot())
        self.write("topic.md", "# Missing metadata\n")
        before = self.snapshot()
        result = self.cli(cwd=unrelated, no_site=True)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("METADATA_INVALID", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertEqual(before, self.snapshot())
        self.assertFalse(list(self.repo.rglob("__pycache__")))

    def readable_metadata(self):
        return (
            "type: self\ndescription: Observation\nsource_refs:\n"
            "  - kind: url\n    target: https://example.org/evidence\n"
            "updated: 2026-10-14\nstatus: current\n"
        )

    def write_frontmatter(self, content, body="# Topic\n"):
        self.write("topic.md", "---\n" + content + "\n---\n" + body)

    def assertParseDiagnostic(self, code, relative):
        before = self.snapshot()
        result = self.diagnostics()
        matching = [item for item in result if item["code"] == code and relative in item["path"]]
        self.assertTrue(matching, result)
        self.assertNotIn("Traceback", str(result))
        self.assertEqual(result, self.diagnostics())
        self.assertEqual(before, self.snapshot())
        return matching

    def test_readable_block_metadata_comments_blank_lines_and_crlf(self):
        content = "# Metadata comment\n\n" + self.readable_metadata().replace(
            "description: Observation", "description: Observation # inline comment"
        ) + "\n# End comment\n"
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=repr(newline)):
                self.write("topic.md", ("---\n" + content + "---\n# Topic\n").replace("\n", newline))
                self.assertValid()

    def test_readable_nested_adr_human_decision_mapping(self):
        self.write("decision.txt", "Actual human approval.")
        content = self.readable_metadata().replace("type: self", "type: adr").replace("status: current", "status: Accepted")
        content += (
            "human_decision:\n  actor: Human reviewer\n  decided_at: 2026-10-14\n"
            "  evidence_ref:\n    kind: artifact\n    target: decision.txt\n"
        )
        self.write_frontmatter(content, ADR_BODY)
        self.assertValid()

    def test_readable_nested_log_sequence_mappings_and_evidence(self):
        self.write_log([])
        content = (
            "- timestamp: 2026-10-14T01:02:03Z\n  action: update\n"
            "  paths:\n    - memory-store/topic.md\n  evidence:\n"
            "    - kind: artifact\n      target: ../check.txt\n  checks:\n"
            "    - status: passed\n      reason: Completed successfully.\n"
            "      command: python check.py\n      evidence:\n"
            "        - kind: artifact\n          target: ../check.txt\n"
            "  run_id: fixture-run\n  summary: Recorded change.\n"
        )
        self.write("actions.md", "# Actions\n## Entries\n```yaml\n" + content + "```\n")
        self.assertValid()

    def test_flow_and_multiline_json_containers_are_accepted(self):
        variants = (
            self.readable_metadata().replace(
                "source_refs:\n  - kind: url\n    target: https://example.org/evidence",
                "source_refs: [{kind: url, target: 'https://example.org/evidence'}]",
            ) + "extra: {empty_list: [], empty_map: {}, nested: [{value: [1, 2]}]}\n",
            self.readable_metadata() + "extra:\n  - scalar\n  - [one, two]\n  -\n    - nested\n    - {kind: inert}\n",
            "{type: self, description: Observation, source_refs: [{kind: url, target: https://example.org/evidence}], updated: 2026-10-14, status: current}",
            json.dumps(metadata(extra={"nested": [{"empty": [], "map": {}}]}), indent=2),
        )
        for content in variants:
            with self.subTest(content=content):
                self.write_frontmatter(content)
                self.assertValid()
        self.write_log([self.log_entry()])
        self.write("actions.md", "# Actions\n## Entries\n```yaml\n" + json.dumps([self.log_entry()], indent=2) + "\n```\n")
        self.assertValid()

    def test_public_cli_accepts_readable_block_and_flow_layout(self):
        config_path = self.base / "layout.yaml"
        self.write("start.md", "# Start\n[Topic](topic.md)\n")
        for content in (
            "version: 1\nnavigation_files:\n  - start.md\nraw_source_dirs: []\n",
            "{version: 1, navigation_files: [start.md], raw_source_dirs: []}",
            json.dumps(layout(navigation_files=["start.md"]), indent=2),
        ):
            with self.subTest(content=content):
                config_path.write_text(content, encoding="utf-8")
                before = self.snapshot()
                result = self.cli("--layout", str(config_path), no_site=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_quoted_strings_unicode_escapes_and_doubled_quotes(self):
        targets = (
            ("proof 世界.txt", '"proof \\u4e16\\u754c.txt"'),
            ("it's proof.txt", "'it''s proof.txt'"),
            ('a "quote".txt', '"a \\"quote\\".txt"'),
            ("back\\slash.txt", '"back\\\\slash.txt"'),
        )
        for filename, scalar in targets:
            with self.subTest(filename=filename):
                self.write(filename, "retained evidence")
                content = self.readable_metadata().replace("kind: url", "kind: local").replace("https://example.org/evidence", scalar)
                content = content.replace("description: Observation", "'description': 'Café 世界 # literal: punctuation'")
                content = content.replace("updated: 2026-10-14", 'updated: "\\u0032\\u0030\\u0032\\u0036-10-14"')
                self.write_frontmatter(content)
                self.assertValid()

    def test_plain_strings_preserve_urls_dates_paths_and_placeholders(self):
        self.write("proof:part.txt", "evidence")
        content = self.readable_metadata().replace("https://example.org/evidence", "https://example.org:443/a?q=yes#fragment # comment")
        content += "extra_date: 2026-10-14\nextra_timestamp: 2026-10-14T01:02:03Z\n"
        self.write_frontmatter(content)
        self.assertValid()
        content = self.readable_metadata().replace("kind: url", "kind: local").replace("https://example.org/evidence", "./proof:part.txt")
        self.write_frontmatter(content)
        self.assertValid()
        self.config = layout(template_dirs=["patterns"])
        self.write("patterns/template.md", "---\n" + self.readable_metadata().replace("2026-10-14", "<YYYY-MM-DD>").replace("kind: url", "kind: local").replace("https://example.org/evidence", "<evidence-path>") + "---\n# Pattern\n")
        self.assertValid()

    def test_boolean_null_and_finite_number_scalars_keep_semantic_types(self):
        # Description is a string field: recognized typed scalars must not pass.
        for value in ("true", "FALSE", "True", "null", "NULL", "~", "0", "-2", "+7", "1.5", "-0.25", "1e3", "-2.5E-2"):
            with self.subTest(value=value):
                self.write_frontmatter(self.readable_metadata().replace("description: Observation", "description: " + value))
                self.assertParseDiagnostic("METADATA_INVALID", "topic.md")
        self.config = layout(example_dirs=["illustrations"])
        for value in ("true", "TRUE", "True"):
            with self.subTest(boolean=value):
                self.write_frontmatter(self.readable_metadata())
                self.write("illustrations/example.md", "---\n" + self.readable_metadata() + "example: " + value + "\n---\n# Example\n")
                self.assertValid()

    def test_quoted_and_inert_syntax_marker_text_remains_strings(self):
        marker = self.repo / "should-never-exist"
        quoted = ("!tag", "&anchor", "*alias", "<<", "|", ">", "---", "...", "%YAML 1.2", "yes", "NO", "on", "off", "0x10", ".nan", "001", "[x,]", "{x:}")
        for value in quoted:
            with self.subTest(quoted=value):
                self.write_frontmatter(self.readable_metadata().replace("description: Observation", "description: " + json.dumps(value)))
                self.assertValid()
        for command in (
            f"touch {marker}", "echo !tag &anchor *alias << | > --- ... %YAML",
            "printf yes/no/on/off", "echo https://example.org/x#fragment",
            "echo 0x10 001 .nan", "printf '[sample](absent.md)'",
        ):
            with self.subTest(command=command):
                content = self.readable_metadata().replace("kind: url", "kind: command").replace("https://example.org/evidence", command)
                self.write_frontmatter(content)
                self.assertValid()
        self.assertFalse(marker.exists())

    def test_duplicate_keys_rejected_in_block_flow_and_json_at_all_depths(self):
        base = self.readable_metadata()
        cases = (
            base + "status: draft\n",
            base + "extra:\n  same: first\n  same: second\n",
            base + "extra:\n  - nested:\n      same: first\n      same: second\n",
            base + "extra: {same: first, same: second}\n",
            base + "extra: [{nested: {same: first, same: second}}]\n",
            base + "extra: {'same': first, same: second}\n",
            json.dumps(metadata())[:-1] + ', "status": "draft"}',
            json.dumps(metadata())[:-1] + ', "extra": {"same": 1, "same": 2}}',
            json.dumps(metadata())[:-1] + ', "extra": [{"nested": {"same": 1, "same": 2}}]}',
        )
        for content in cases:
            with self.subTest(content=content):
                self.write_frontmatter(content)
                result = self.assertParseDiagnostic("METADATA_INVALID", "topic.md")
                self.assertIn("duplicate", str(result).lower())

    def unsupported_yaml_cases(self):
        return (
            "extra: !custom text", "extra: !!str text", "extra: &anchor text", "extra: *alias",
            "extra: {<<: {key: value}}", "extra: |\n  folded", "extra: >\n  folded",
            "...\nextra: text", "%YAML 1.2\nextra: text", "extra:\n  ---\n  value: text",
            "? [complex, key]\n: value", "1: value", "true: value", "null: value", "'': value",
            "extra:\n   child: text", "extra:\n\tchild: text", "extra:\n- item",
            "extra: 'unterminated", 'extra: "unterminated', 'extra: "bad\\q"',
            "extra: 'first' trailing", 'extra: "first" trailing', "extra: first\n  folded",
            "extra: 'first\n  second'", 'extra: "first\n  second"',
            "extra: [first,]", "extra: [,first]", "extra: [first second,]",
            "extra: [first,,second]", "extra: [first", "extra: {key: value,}",
            "extra: {key: value other: text}", "extra: {key value}", "extra: {key:}",
            "extra: {key: value", "extra: [first] garbage", "extra: [first}\n",
            "extra: [\n  first\n]", "extra: yes", "extra: No", "extra: ON", "extra: off",
            "extra: 01", "extra: +01", "extra: 0x10", "extra: 0o10", "extra: 0b10",
            "extra: 1:20", "extra: .nan", "extra: -.inf", "extra: Infinity", "extra: 1e999",
            '{"extra": NaN}', '{"extra": Infinity}', '{"extra": -Infinity}',
        )

    def test_unsupported_frontmatter_is_typed_fail_closed_and_inert(self):
        marker = self.repo / "should-never-exist"
        cases = self.unsupported_yaml_cases() + (f"extra: !!python/object/apply:os.system ['touch {marker}']",)
        for fragment in cases:
            with self.subTest(fragment=fragment):
                if fragment.startswith('{"'):
                    content = json.dumps(metadata())[:-1] + ", " + fragment[1:]
                else:
                    content = self.readable_metadata() + fragment + "\n"
                self.write_frontmatter(content)
                self.assertParseDiagnostic("METADATA_INVALID", "topic.md")
        self.assertFalse(marker.exists())

    def test_log_unsupported_syntax_returns_log_invalid(self):
        self.write_log([])
        cases = (
            "!!seq []", "&entries []", "*entries", "|\n  []", "---\n[]", "%YAML 1.2\n[]",
            "[first,]", "[{same: one, same: two}]", '[{"same": 1, "same": 2}]',
            "- extra: yes", "- extra:\n   wrong: indentation", "- extra: .nan",
            '[["bad\\q"]]',
        )
        for content in cases:
            with self.subTest(content=content):
                self.write("actions.md", "# Actions\n## Entries\n```yaml\n" + content + "\n```\n")
                self.assertParseDiagnostic("LOG_INVALID", "actions.md")

    def test_cli_layout_unsupported_syntax_is_config_error_without_traceback(self):
        config_path = self.base / "layout.yaml"
        cases = (
            "version: 1\nversion: 1", "version: 1\nraw_source_dirs: &empty []",
            "version: 1\nraw_source_dirs: *empty", "version: 1\n<<: {version: 1}",
            "version: 1\nraw_source_dirs: !!seq []", "version: 1\nraw_source_dirs: |\n  []",
            "%YAML 1.2\nversion: 1", "version: 1\n---\nversion: 1", "version: 1\n...",
            "version: 1\nraw_source_dirs:\n   - text", "version: 1\nraw_source_dirs:\n\t- text",
            "version: 1\nraw_source_dirs: [text,]", "version: 1\nraw_source_dirs: [text",
            'version: 1\nraw_source_dirs: ["bad\\q"]', "version: 01", "version: yes", "version: .nan",
            '{"version": 1, "raw_source_dirs": [{"x": 1, "x": 2}]}',
        )
        for content in cases:
            with self.subTest(content=content):
                config_path.write_text(content, encoding="utf-8")
                before = self.snapshot()
                result = self.cli("--layout", str(config_path), no_site=True)
                output = result.stdout + result.stderr
                self.assertEqual(2, result.returncode, output)
                self.assertIn("CONFIG_INVALID", output)
                self.assertNotIn("Traceback", output)
                self.assertEqual(before, self.snapshot())

    def test_reader_size_limit_counts_utf8_bytes_and_returns_typed_errors(self):
        # Stay just inside the limit; large plain/quoted strings are single line.
        under = json.dumps(metadata(description="a" * (1024 * 1024 - 512)))
        self.write_frontmatter(under)
        self.assertValid()
        for content in (json.dumps(metadata(description="a" * (1024 * 1024 + 128))), json.dumps(metadata(description="界" * 350000), ensure_ascii=False)):
            with self.subTest(bytes=len(content.encode("utf-8"))):
                self.write_frontmatter(content)
                result = self.assertParseDiagnostic("METADATA_INVALID", "topic.md")
                self.assertRegex(str(result).lower(), r"size|limit|large|mib|bytes")
        self.write_frontmatter(self.readable_metadata())
        self.write_log([])
        self.write("actions.md", "# Actions\n## Entries\n```yaml\n" + " " * (1024 * 1024 + 128) + "[]\n```\n")
        result = self.assertParseDiagnostic("LOG_INVALID", "actions.md")
        self.assertRegex(str(result).lower(), r"size|limit|large|mib|bytes")
        config_path = self.base / "layout.yaml"
        config_path.write_text(" " * (1024 * 1024 + 128) + '{"version": 1}', encoding="utf-8")
        result = self.cli("--layout", str(config_path), no_site=True)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("CONFIG_INVALID", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertRegex((result.stdout + result.stderr).lower(), r"size|limit|large|mib|bytes")

    def test_reader_container_depth_boundary_and_typed_errors(self):
        # The root metadata mapping plus 63 lists has 64 container levels.
        for count in (63, 64):
            content = self.readable_metadata() + "extra: " + "[" * count + "0" + "]" * count + "\n"
            self.write_frontmatter(content)
            with self.subTest(levels=count + 1):
                if count == 63:
                    self.assertValid()
                else:
                    result = self.assertParseDiagnostic("METADATA_INVALID", "topic.md")
                    self.assertRegex(str(result).lower(), r"depth|nest|limit")
        self.write_frontmatter(self.readable_metadata())
        self.write_log([])
        self.write("actions.md", "# Actions\n## Entries\n```yaml\n" + "[" * 65 + "0" + "]" * 65 + "\n```\n")
        result = self.assertParseDiagnostic("LOG_INVALID", "actions.md")
        self.assertRegex(str(result).lower(), r"depth|nest|limit")
        config_path = self.base / "layout.yaml"
        config_path.write_text('{"version": 1, "raw_source_dirs": ' + "[" * 64 + "0" + "]" * 64 + "}", encoding="utf-8")
        result = self.cli("--layout", str(config_path), no_site=True)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("CONFIG_INVALID", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertRegex((result.stdout + result.stderr).lower(), r"depth|nest|limit")

    def test_block_and_multiline_json_container_depth_limit(self):
        for count in (63, 64):
            nested = 0
            for _ in range(count):
                nested = [nested]
            json_content = json.dumps(metadata(extra=nested), indent=2)
            block_content = self.readable_metadata() + "extra:\n" + "".join("  " * level + "child:\n" for level in range(1, count)) + "  " * count + "leaf: text\n"
            for syntax, content in (("json", json_content), ("block", block_content)):
                with self.subTest(syntax=syntax, levels=count + 1):
                    self.write_frontmatter(content)
                    if count == 63:
                        self.assertValid()
                    else:
                        self.assertParseDiagnostic("METADATA_INVALID", "topic.md")

    def test_numeric_separators_rejected_unquoted_and_preserved_as_text(self):
        # S1: separators in any numeric component are unsupported syntax.
        tokens = ("1.2_3", "0.0_1", "+1.2_3", "-0.0_1", "1e1_0", "-1E+1_0")
        for token in tokens:
            with self.subTest(unquoted=token):
                self.write_frontmatter(self.readable_metadata().replace("description: Observation", "description: " + token))
                self.assertParseDiagnostic("METADATA_INVALID", "topic.md")
            for text in (json.dumps(token), "Measured " + token + " samples"):
                with self.subTest(text=text):
                    self.write_frontmatter(self.readable_metadata().replace("description: Observation", "description: " + text))
                    self.assertValid()

    def test_quotes_inside_plain_block_flow_and_command_scalars_are_inert(self):
        # S2: a quote inside a plain token does not open a quoted scalar.
        for text in ('The 6 " sample', "The 6 ' sample"):
            for suffix in ("", " # ignored comment with [ punctuation"):
                with self.subTest(block=text, suffix=suffix):
                    self.write_frontmatter(self.readable_metadata().replace("description: Observation", "description: " + text + suffix))
                    self.assertValid()
            with self.subTest(flow=text):
                self.write_frontmatter("{type: self, description: " + text + ", source_refs: [{kind: url, target: https://example.org/evidence}], updated: 2026-10-14, status: current}")
                self.assertValid()
            for reference in (
                "source_refs:\n  - kind: command\n    target: printf " + text,
                "source_refs: [{kind: command, target: printf " + text + "}]",
            ):
                with self.subTest(command=reference):
                    self.write_frontmatter(self.readable_metadata().replace("source_refs:\n  - kind: url\n    target: https://example.org/evidence", reference))
                    self.assertValid()

    def test_decoded_unpaired_surrogates_are_metadata_parse_errors(self):
        # S3: input bytes are UTF-8; the malformed code points arise on decode.
        invalid = (chr(0xD800), chr(0xDFFF), chr(0xD800) + "x", chr(0xD800) * 2, chr(0xDC00) + chr(0xD800))
        for value in invalid:
            contents = (
                self.readable_metadata().replace("kind: url", "kind: local").replace("https://example.org/evidence", json.dumps(value)),
                json.dumps(metadata(extra={"nested": [{"value": value}]})),
                json.dumps(metadata(extra={"nested": [{value: "inert"}]})),
            )
            for index, content in enumerate(contents):
                with self.subTest(codepoints=[ord(c) for c in value], form=index):
                    self.write_frontmatter(content)
                    result = self.assertParseDiagnostic("METADATA_INVALID", "topic.md")
                    self.assertRegex(str(result).lower(), r"surrogate|unicode|utf")
        self.write("proof 😀.txt", "retained evidence")
        self.write_frontmatter(self.readable_metadata().replace("kind: url", "kind: local").replace("https://example.org/evidence", '"proof \\ud83d\\ude00.txt"'))
        self.assertValid()

    def test_decoded_surrogates_in_log_values_and_keys_are_typed(self):
        self.write_log([])
        value = chr(0xD800)
        entry = self.log_entry()
        contents = (
            json.dumps([{**entry, "extra": {"nested": [{"value": value}]}}]),
            json.dumps([{**entry, "extra": {"nested": [{value: "inert"}]}}]),
            json.dumps([entry], indent=2).replace('"Recorded change."', '"\\ud800"'),
        )
        for content in contents:
            with self.subTest(content=content):
                self.write("actions.md", "# Actions\n## Entries\n```yaml\n" + content + "\n```\n")
                result = self.assertParseDiagnostic("LOG_INVALID", "actions.md")
                self.assertRegex(str(result).lower(), r"surrogate|unicode|utf")
        content = json.dumps([self.log_entry(summary="Recorded 😀 change.")], ensure_ascii=True)
        self.write("actions.md", "# Actions\n## Entries\n```yaml\n" + content + "\n```\n")
        self.assertValid()

    def test_decoded_surrogates_in_cli_layout_are_typed_config_errors(self):
        config_path = self.base / "layout.yaml"
        value = chr(0xD800)
        contents = (
            'version: 1\nraw_source_dirs: ["\\ud800"]',
            json.dumps(layout(raw_source_dirs=[value])),
            json.dumps({**layout(), "extra": {"nested": [{value: "inert"}]}}),
        )
        for content in contents:
            with self.subTest(content=content):
                config_path.write_text(content, encoding="utf-8")
                result = self.cli("--layout", str(config_path), no_site=True)
                output = result.stdout + result.stderr
                self.assertEqual(2, result.returncode, output)
                self.assertIn("CONFIG_INVALID", output)
                self.assertNotIn("Traceback", output)
                self.assertRegex(output.lower(), r"surrogate|unicode|utf")
        self.write("imports-😀/source.md", "raw source")
        config_path.write_text(json.dumps(layout(raw_source_dirs=["imports-😀"]), ensure_ascii=True), encoding="utf-8")
        result = self.cli("--layout", str(config_path), no_site=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_inline_flow_comments_do_not_count_as_container_depth(self):
        # S4: punctuation inside a comment cannot consume container levels.
        config_path = self.base / "layout.yaml"
        for comment in ("[" * 65, "{" * 65, '[{"unterminated' * 65):
            with self.subTest(comment=comment):
                config_path.write_text("{version: 1} # " + comment, encoding="utf-8")
                before = self.snapshot()
                result = self.cli("--layout", str(config_path), no_site=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_positive_mixed_explicit_layout(self):
        self.write("unparsed/source.md", "# Raw\n[irrelevant](missing.md)\n")
        self.write("unparsed/companion.md", page(metadata(type="source-companion", source_refs=[{"kind": "local", "target": "source.md"}])))
        self.write("unparsed/menu.md", "# Source navigation\n[Raw](source.md)\n")
        self.write("patterns/topic.md", page(metadata(updated="<YYYY-MM-DD>", source_refs=[{"kind": "local", "target": "<source-path>"}])))
        self.write("patterns/index.md", "# Patterns\n## Navigation Hints\nNo navigation hints yet.\n")
        self.write("illustrations/topic.md", page(metadata(example=True)))
        self.write("guide.md", "# Guide\n## Navigation Hints\n| Task | Target |\n| --- | --- |\n| Read topic | [Topic](topic.md) |\n")
        self.write("start.md", "# Start\n[Guide](guide.md)\n")
        self.write("actions.md", "# Log\n## Entries\n```yaml\n[]\n```\n")
        self.config = layout(
            raw_source_dirs=["unparsed"], source_companion_files=["unparsed/companion.md"],
            template_dirs=["patterns"], example_dirs=["illustrations"],
            index_files=["guide.md", "patterns/index.md"],
            navigation_files=["start.md", "unparsed/menu.md"], log_files=["actions.md"],
        )
        self.assertValid()


if __name__ == "__main__":
    unittest.main()
