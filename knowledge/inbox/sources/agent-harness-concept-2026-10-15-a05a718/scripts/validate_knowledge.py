#!/usr/bin/env python3
"""Read-only mechanical knowledge checks; references are never executed."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
from collections.abc import Mapping
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

class InputError(ValueError):
    """Malformed or unsupported syntax in the bounded reference YAML reader."""

    def __init__(self, message, line=1):
        super().__init__(f"line {line}: {message}")


MAX_INPUT_BYTES = 1024 * 1024
MAX_CONTAINER_DEPTH = 64


def valid_string(value, line=1):
    """JSON decoders accept lone surrogates; reject them at the input boundary."""
    if isinstance(value, str) and any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise InputError("decoded string contains an unpaired Unicode surrogate", line)
    return value


def scalar(text, line, key=False):
    """Decode one scalar; plain dates and timestamps deliberately remain text."""
    text = text.strip()
    if not text:
        value = None
    elif text[0] == '"':
        try:
            value = json.loads(text)
        except (ValueError, RecursionError) as exc:
            raise InputError("malformed double-quoted string or unsupported escape", line) from exc
        if not isinstance(value, str):
            raise InputError("expected quoted string", line)
    elif text[0] == "'":
        if not re.fullmatch(r"'(?:[^']|'')*'", text):
            raise InputError("malformed single-quoted string", line)
        value = text[1:-1].replace("''", "'")
    else:
        if text.startswith(("!", "&", "*", "|", ">", "?", "%", "@", "`", "]", "}", ",")) or text in {"---", "...", "<<"}:
            raise InputError("unsupported YAML tag, anchor, alias, merge key or scalar syntax", line)
        if re.search(r":(?:\s|$)", text) or text.startswith(("- ", "[", "{")):
            raise InputError("unsupported plain scalar or flow punctuation", line)
        lowered = text.lower()
        if lowered in {"yes", "no", "on", "off"}:
            raise InputError("unsupported ambiguous YAML boolean", line)
        if lowered in {"true", "false"}:
            value = lowered == "true"
        elif lowered in {"null", "~"}:
            value = None
        elif re.fullmatch(r"[+-]?(?:0|[1-9][0-9]*)", text):
            try:
                value = int(text)
            except ValueError as exc:
                raise InputError("integer exceeds supported conversion limit", line) from exc
        elif re.fullmatch(r"[+-]?(?:(?:0|[1-9][0-9]*)\.[0-9]*(?:[eE][+-]?[0-9]+)?|\.[0-9]+(?:[eE][+-]?[0-9]+)?|(?:0|[1-9][0-9]*)[eE][+-]?[0-9]+)", text):
            value = float(text)
            if not math.isfinite(value):
                raise InputError("nonfinite numeric scalar is unsupported", line)
        elif (lowered.lstrip("+-") in {".nan", ".inf", "nan", "inf", "infinity"}
              or ("_" in text and re.fullmatch(r"[+-]?(?:[0-9][0-9_]*(?:\.[0-9_]*)?|\.[0-9][0-9_]*)(?:[eE][+-]?[0-9][0-9_]*)?", text))
              or re.fullmatch(r"[+-]?(?:0[0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?|0[xX][0-9a-fA-F_]+|0[oO][0-7_]+|0[bB][01_]+|[0-9]+(?::[0-9]+)+(?:\.[0-9]+)?|[0-9_]+_[0-9_]*(?:\.[0-9_]+)?(?:[eE][+-]?[0-9_]+)?)", text)):
            raise InputError("unsupported ambiguous numeric scalar", line)
        else:
            value = text
    if key and (not isinstance(value, str) or not value):
        raise InputError("mapping keys must be nonempty strings", line)
    return valid_string(value, line)


def clean_line(text, line):
    """Remove whitespace-separated comments outside quoted scalar tokens."""
    quote, started, block_separator = None, False, False
    # Flow frames remember whether the current token is a mapping key. Quotes
    # inside a plain token are inert, even after spaces (e.g. shell commands).
    flow = []
    i = 0
    while i < len(text):
        char = text[i]
        if quote:
            if char == "\\" and quote == '"':
                i += 2
                continue
            if char == quote:
                if quote == "'" and i + 1 < len(text) and text[i + 1] == "'":
                    i += 2
                    continue
                quote = None
        elif char == "#" and (i == 0 or text[i - 1].isspace()):
            return text[:i].rstrip()
        elif char.isspace():
            pass
        elif char in "\"'" and not started:
            quote = char
            started = True
        elif char in "[{" and not started:
            flow.append([char, char == "{"])
            started = False
        elif flow and char in "]}":
            flow.pop()
            started = True
        elif flow and char == ",":
            flow[-1][1] = flow[-1][0] == "{"
            started = False
        elif flow and char == ":" and flow[-1][1]:
            flow[-1][1] = False
            started = False
        elif not flow and not block_separator and char == ":" and (i + 1 == len(text) or text[i + 1].isspace()):
            block_separator, started = True, False
        elif not started and char == "-" and (i + 1 == len(text) or text[i + 1].isspace()):
            pass
        else:
            started = True
        i += 1
    if quote:
        raise InputError("multiline or malformed quoted scalar is unsupported", line)
    return text.rstrip()


class FlowReader:
    """Single-line YAML flow containers, also used to preflight JSON depth."""

    def __init__(self, text, line, depth):
        self.text, self.line, self.depth, self.pos = text, line, depth, 0

    def spaces(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def token(self, key=False):
        self.spaces()
        start = self.pos
        quote = self.text[self.pos] if self.pos < len(self.text) and self.text[self.pos] in "\"'" else None
        if quote:
            self.pos += 1
            while self.pos < len(self.text):
                char = self.text[self.pos]
                self.pos += 1
                if char == "\\" and quote == '"':
                    self.pos += 1
                elif char == quote:
                    if quote == "'" and self.pos < len(self.text) and self.text[self.pos] == "'":
                        self.pos += 1
                    else:
                        return scalar(self.text[start:self.pos], self.line, key)
            raise InputError("malformed quoted scalar", self.line)
        while self.pos < len(self.text) and self.text[self.pos] not in ",[]{}" and not (key and self.text[self.pos] == ":"):
            self.pos += 1
        token = self.text[start:self.pos].strip()
        if not token:
            raise InputError("missing flow scalar or invalid flow punctuation", self.line)
        return scalar(token, self.line, key)

    def value(self, depth):
        self.spaces()
        if self.pos >= len(self.text):
            raise InputError("missing flow value", self.line)
        opener = self.text[self.pos]
        if opener not in "[{":
            return self.token()
        depth += 1
        if depth > MAX_CONTAINER_DEPTH:
            raise InputError("container depth exceeds 64 levels", self.line)
        closer = "]" if opener == "[" else "}"
        result = [] if opener == "[" else {}
        self.pos += 1
        self.spaces()
        if self.pos < len(self.text) and self.text[self.pos] == closer:
            self.pos += 1
            return result
        while True:
            if opener == "{":
                key = self.token(key=True)
                self.spaces()
                if self.pos >= len(self.text) or self.text[self.pos] != ":":
                    raise InputError("flow mapping requires a colon", self.line)
                self.pos += 1
                if key in result:
                    raise InputError(f"duplicate mapping key: {key}", self.line)
                result[key] = self.value(depth)
            else:
                result.append(self.value(depth))
            self.spaces()
            if self.pos < len(self.text) and self.text[self.pos] == closer:
                self.pos += 1
                return result
            if self.pos >= len(self.text) or self.text[self.pos] != ",":
                raise InputError("flow entries require commas and matching delimiters", self.line)
            self.pos += 1
            self.spaces()
            if self.pos < len(self.text) and self.text[self.pos] == closer:
                raise InputError("trailing flow comma is unsupported", self.line)

    def read(self):
        value = self.value(self.depth)
        self.spaces()
        if self.pos != len(self.text):
            raise InputError("unexpected text after flow value", self.line)
        return value


def mapping_pair(text, line):
    """Find only a block colon separator, outside quotes and flow containers."""
    quote, level, i, started = None, 0, 0, False
    while i < len(text):
        char = text[i]
        if quote:
            if char == "\\" and quote == '"':
                i += 2
                continue
            if char == quote:
                if quote == "'" and i + 1 < len(text) and text[i + 1] == "'":
                    i += 2
                    continue
                quote = None
        elif char in "\"'" and not started:
            quote = char
            started = True
        elif char in "[{":
            level += 1
        elif char in "]}":
            level -= 1
        elif char == ":" and level == 0 and (i + 1 == len(text) or text[i + 1].isspace()):
            return scalar(text[:i], line, key=True), text[i + 1:].strip()
        elif not char.isspace():
            started = True
        i += 1
    return None


class BlockReader:
    """Two-space block mappings/sequences with bounded inline flow values."""

    def __init__(self, text):
        self.lines = []
        for number, raw in enumerate(text.split("\n"), 1):
            raw = raw.removesuffix("\r")
            if "\t" in raw[:len(raw) - len(raw.lstrip())]:
                raise InputError("tabs in block indentation are unsupported", number)
            clean = clean_line(raw, number)
            if not clean.strip():
                continue
            indent = len(clean) - len(clean.lstrip(" "))
            if indent % 2:
                raise InputError("block indentation must use two-space increments", number)
            content = clean[indent:]
            if content in {"---", "..."} or content.startswith("%"):
                raise InputError("YAML directives and document separators are unsupported", number)
            self.lines.append((indent, content, number))
        self.pos = 0

    def inline(self, text, line, depth):
        return FlowReader(text, line, depth).read() if text.startswith(("[", "{")) else scalar(text, line)

    def child(self, value, indent, line, depth):
        if value:
            result = self.inline(value, line, depth)
            if self.pos < len(self.lines) and self.lines[self.pos][0] > indent:
                raise InputError("multiline scalar folding or indentation after an inline value is unsupported", self.lines[self.pos][2])
            return result
        if self.pos < len(self.lines) and self.lines[self.pos][0] > indent:
            if self.lines[self.pos][0] != indent + 2:
                raise InputError("nested block indentation must increase by two spaces", self.lines[self.pos][2])
            return self.block(indent + 2, depth)
        return None

    def block(self, indent, depth):
        line_indent, content, line = self.lines[self.pos]
        if line_indent != indent:
            raise InputError("unexpected block indentation", line)
        sequence = content == "-" or content.startswith("- ")
        pair = None if sequence else mapping_pair(content, line)
        if not sequence and pair is None:
            self.pos += 1
            return self.inline(content, line, depth)
        depth += 1
        if depth > MAX_CONTAINER_DEPTH:
            raise InputError("container depth exceeds 64 levels", line)
        result = [] if sequence else {}
        while self.pos < len(self.lines) and self.lines[self.pos][0] == indent:
            _, content, line = self.lines[self.pos]
            is_sequence = content == "-" or content.startswith("- ")
            if is_sequence != sequence:
                raise InputError("cannot mix block sequence and mapping entries", line)
            if sequence:
                value = content[1:].strip()
                # Reinterpret an item mapping at its logical continuation column.
                if value and mapping_pair(value, line) is not None:
                    self.lines[self.pos] = (indent + 2, value, line)
                    result.append(self.block(indent + 2, depth))
                else:
                    self.pos += 1
                    result.append(self.child(value, indent, line, depth))
            else:
                pair = mapping_pair(content, line)
                if pair is None:
                    raise InputError("block mapping requires colon plus whitespace", line)
                key, value = pair
                if key in result:
                    raise InputError(f"duplicate mapping key: {key}", line)
                self.pos += 1
                result[key] = self.child(value, indent, line, depth)
        return result

    def read(self):
        if not self.lines:
            return None
        result = self.block(0, 0)
        if self.pos != len(self.lines):
            raise InputError("unsupported indentation or multiple root values", self.lines[self.pos][2])
        return result


def safe_load(text):
    """Read the documented subset, not general YAML; never execute input data.

    Supports two-space blocks, single-line flow containers and strict multiline
    JSON. Limits apply before JSON decoding and to combined block/flow depth.
    """
    if len(text.encode("utf-8")) > MAX_INPUT_BYTES:
        raise InputError("input exceeds 1 MiB limit")
    if re.search(r"\r(?!\n)", text):
        raise InputError("only LF and CRLF document line endings are supported")
    # JSON accepts multiline containers. Check nesting before calling its decoder
    # so adversarial depth cannot reach Python's recursion boundary.
    # Comment-only lines surrounding JSON are document whitespace, while JSON
    # itself retains its strict quoting, separators and escaping rules.
    json_text = "\n".join("" if line.lstrip().startswith("#") else line
                          for line in text.split("\n"))
    stripped = json_text.strip()
    if stripped.startswith(("[", "{")):
        # Single-line containers already have a bounded flow reader. Its token
        # lexer removes comments before examining depth, so ignored punctuation
        # cannot affect the limit (and internal plain quotes remain inert).
        if "\n" not in stripped:
            line = json_text.count("\n", 0, len(json_text) - len(json_text.lstrip())) + 1
            return FlowReader(clean_line(stripped, line), line, 0).read()
        depth, quote, escape = 0, None, False
        position = 0
        while position < len(json_text):
            char = json_text[position]
            if quote:
                if escape:
                    escape = False
                elif char == "\\" and quote == '"':
                    escape = True
                elif char == quote:
                    if quote == "'" and position + 1 < len(json_text) and json_text[position + 1] == "'":
                        position += 1
                    else:
                        quote = None
            elif char == '"':
                quote = char
            elif char in "[{":
                depth += 1
                if depth > MAX_CONTAINER_DEPTH:
                    raise InputError("container depth exceeds 64 levels", json_text.count("\n", 0, position) + 1)
            elif char in "]}":
                depth -= 1
            position += 1

        def unique_object(pairs):
            result = {}
            for key, value in pairs:
                valid_string(key)
                if not key:
                    raise InputError("mapping keys must be nonempty strings")
                if key in result:
                    raise InputError(f"duplicate mapping key: {key}")
                result[key] = value
            return result

        def finite_float(value):
            result = float(value)
            if not math.isfinite(result):
                raise InputError("nonfinite JSON number is unsupported")
            return result

        def invalid_constant(value):
            raise InputError(f"nonstandard JSON constant is unsupported: {value}")

        try:
            result = json.loads(json_text, object_pairs_hook=unique_object,
                                parse_float=finite_float, parse_constant=invalid_constant)
            # Visit all decoded string values, including unknown schema fields,
            # before any path, URL, diagnostic or semantic processing can occur.
            pending = [result]
            while pending:
                value = pending.pop()
                valid_string(value)
                if isinstance(value, dict):
                    pending.extend(value.values())
                elif isinstance(value, list):
                    pending.extend(value)
            return result
        except json.JSONDecodeError as exc:
            # Only single-line YAML flow syntax is supported as a fallback.
            if "\n" in stripped:
                raise InputError(f"malformed multiline JSON: {exc.msg}", exc.lineno) from exc
        except (RecursionError, ValueError) as exc:
            if isinstance(exc, InputError):
                raise
            raise InputError("JSON value exceeds supported conversion limits") from exc
    return BlockReader(text).read()


FIELDS = ("raw_source_dirs", "source_companion_files", "template_dirs", "example_dirs",
          "index_files", "navigation_files", "log_files")
ADR_SECTIONS = ("Context", "Decision", "Reasons", "Rejected alternatives", "Consequences",
                "Open questions", "History", "Supersession")
FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)


def markdown_body(text):
    """YAML provenance is data, including strings that resemble Markdown."""
    match = FRONTMATTER.match(text)
    return text[match.end():] if match else text


class HTMLIds(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == "id" and value is not None:
                self.ids.add(value)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def placeholder(value):
    return isinstance(value, str) and bool(re.fullmatch(r"<[^<>\n]+>", value))


def date_valid(value):
    if isinstance(value, dt.date) and not isinstance(value, dt.datetime):
        return True
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def within(path, root):
    return path == root or root in path.parents


def prose(text):
    """Mask code while retaining line boundaries for section/heading parsing."""
    lines, fence = [], None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            lines.append("\n" if line.endswith("\n") else "")
        elif match:
            fence = match[1]
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(line)
    # The lookarounds require complete equal runs. A single unmatched backtick
    # must not consume prose up to part of a later double-backtick delimiter.
    return re.sub(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)",
                  lambda match: re.sub(r"[^\n]", " ", match[0]),
                  "".join(lines), flags=re.S)


class Checker:
    def __init__(self, repo, knowledge, layout):
        self.repo = Path(repo).resolve()
        self.root = Path(knowledge).resolve()
        self.layout = layout
        self.classifications = {key: [] for key in FIELDS}
        self.errors = []

    def error(self, path, code, message):
        self.errors.append({"path": str(path), "code": code, "message": message})

    def configure(self):
        if not self.repo.is_dir() or not self.root.is_dir() or not within(self.root, self.repo):
            self.error(self.root, "CONFIG_INVALID", "Repository and knowledge roots must be existing bounded directories.")
            return False
        layout = {"version": 1} if self.layout is None else self.layout
        if not isinstance(layout, Mapping):
            self.error(self.root, "CONFIG_INVALID", "Layout must be a mapping.")
            return False
        if type(layout.get("version")) is not int or layout.get("version") != 1 or set(layout) - {"version", *FIELDS}:
            self.error(self.root, "CONFIG_INVALID", "Layout requires version 1 and only supported classification fields.")
        for key in FIELDS:
            values = layout.get(key, [])
            if not isinstance(values, list):
                self.error(self.root, "CONFIG_INVALID", f"{key} must be a list.")
                continue
            seen = set()
            for value in values:
                if not nonempty(value):
                    self.error(self.root, "CONFIG_INVALID", f"{key} entries must be nonempty paths.")
                    continue
                path = (self.root / value).resolve()
                directory = key.endswith("_dirs")
                if Path(value).is_absolute() or not within(path, self.root) or not path.exists() or (directory and not path.is_dir()) or (not directory and not path.is_file()):
                    self.error(self.root, "CONFIG_INVALID", f"{key}: invalid or missing bounded {'directory' if directory else 'file'} {value}.")
                elif path in seen:
                    self.error(self.root, "CONFIG_INVALID", f"{key}: duplicate {value}.")
                else:
                    seen.add(path)
                    self.classifications[key].append(path)
        dirs = [(key, path) for key in ("raw_source_dirs", "template_dirs", "example_dirs") for path in self.classifications[key]]
        for i, (a, p) in enumerate(dirs):
            for b, q in dirs[i + 1:]:
                if within(p, q) or within(q, p):
                    self.error(self.root, "CONFIG_INVALID", f"Overlapping directory classifications {a}: {p} and {b}: {q}.")
        files = [(key, path) for key in FIELDS if not key.endswith("_dirs") for path in self.classifications[key]]
        for i, (a, p) in enumerate(files):
            for b, q in files[i + 1:]:
                if p == q:
                    self.error(self.root, "CONFIG_INVALID", f"Contradictory file classifications {a} and {b}: {p}.")
            for kind, directory in dirs:
                if within(p, directory) and ((kind == "raw_source_dirs" and a not in {"source_companion_files", "navigation_files"}) or (kind != "raw_source_dirs" and a not in {"index_files", "navigation_files"})):
                    self.error(self.root, "CONFIG_INVALID", f"Contradictory {a} in {kind}: {p}.")
        return not self.errors

    def classified(self, path, key):
        return any(within(path, directory) for directory in self.classifications[key])

    def read(self, path):
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self.error(path, "OPERATIONAL_ERROR", str(exc))
            return None

    def reference(self, page, ref, template=False, retained=False):
        if not isinstance(ref, Mapping) or not isinstance(ref.get("kind"), str) or ref.get("kind") not in {"local", "artifact", "url", "command"} or not nonempty(ref.get("target")):
            self.error(page, "REFERENCE_INVALID", "Reference requires a supported kind and nonempty target string.")
            return
        kind, target = ref["kind"], ref["target"]
        if retained and kind not in {"local", "artifact"}:
            self.error(page, "REFERENCE_INVALID", "Retained evidence/replacement must be a local or artifact reference.")
            return
        if template and placeholder(target):
            return
        if placeholder(target):
            self.error(page, "REFERENCE_INVALID", "Actual reference cannot be a placeholder.")
            return
        if kind == "command":
            return  # Inert provenance only, never run.
        if kind == "url":
            try:
                parsed = urlsplit(target)
                valid = parsed.scheme in {"http", "https"} and parsed.hostname and not re.search(r"\s", target)
                parsed.port  # Reject malformed port syntax too.
            except ValueError:
                valid = False
            if not valid:
                self.error(page, "URL_INVALID", f"Invalid HTTP(S) URL: {target}")
            return
        self.local(page, target, artifact=kind == "artifact")

    def references(self, page, values, template=False, retained=False):
        if not isinstance(values, list) or not values:
            self.error(page, "REFERENCE_INVALID", "References must be a nonempty list of typed mappings.")
            return
        for value in values:
            self.reference(page, value, template, retained)

    def evidence(self, page, values):
        self.references(page, values)
        if isinstance(values, list) and values and all(isinstance(value, Mapping) and value.get("kind") == "command" for value in values):
            self.error(page, "REFERENCE_INVALID", "Inert commands alone cannot substantiate recorded evidence.")

    def anchors(self, text):
        body = prose(markdown_body(text))
        html_ids = HTMLIds()
        html_ids.feed(body)
        anchors = html_ids.ids
        counts = {}
        for line in body.splitlines():
            match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
            if not match:
                continue
            heading = re.sub(r"<[^>]*>", "", match[1]).lower()
            slug = "".join(c for c in heading if c in "_-" or c.isspace() or unicodedata.category(c)[0] in {"L", "N", "M"})
            slug = re.sub(r"\s+", "-", slug.strip())
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            anchors.add(slug if count == 0 else f"{slug}-{count}")
        return anchors

    def local(self, page, target, artifact=False):
        filename, separator, fragment = target.partition("#")
        filename, fragment = unquote(filename), unquote(fragment)
        if "\x00" in filename or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", filename):
            self.error(page, "REFERENCE_INVALID", f"Invalid local path: {target}")
            return
        resolved = (page.parent / filename).resolve() if filename else page.resolve()
        if not within(resolved, self.repo):
            self.error(page, "PATH_ESCAPE", f"Reference escapes repository: {target}")
        elif not resolved.exists():
            self.error(page, "REFERENCE_MISSING", f"Reference does not exist: {target}")
        elif artifact and (not resolved.is_file() or separator):
            self.error(page, "REFERENCE_INVALID", f"Artifact must identify an exact retained file: {target}")
        elif separator:
            if resolved.suffix.lower() != ".md":
                self.error(page, "MARKDOWN_UNSUPPORTED", f"Fragments on non-Markdown files are unsupported: {target}")
            else:
                text = self.read(resolved)
                if text is not None and fragment not in self.anchors(text):
                    clean = prose(markdown_body(text))
                    code = "MARKDOWN_UNSUPPORTED" if re.search(r"^.+\n {0,3}(?:=+|-+)\s*$", clean, re.M) else "ANCHOR_MISSING"
                    self.error(page, code, f"No supported ATX/HTML anchor for: {target}")

    def inline_links(self, page, text):
        clean = prose(text)
        if re.search(r"\[[^]\n]+\]\[[^]\n]*\]|^ {0,3}\[[^]\n]+\]:", clean, re.M):
            self.error(page, "MARKDOWN_UNSUPPORTED", "Reference-style Markdown links are unsupported.")
        result = []
        for match in re.finditer(r"!?\[[^]\n]*\]\(", clean):
            start = match.end()
            end = clean.find(")", start)
            if end == -1:
                self.error(page, "MARKDOWN_UNSUPPORTED", "Unclosed inline Markdown link.")
                continue
            destination = clean[start:end].strip()
            if "(" in destination or "\\" in destination:
                self.error(page, "MARKDOWN_UNSUPPORTED", "Nested/escaped parentheses destinations are unsupported.")
                continue
            angle = re.fullmatch(r'<([^<>\n]+)>(?:\s+(?:"[^"\n]*"|\x27[^\x27\n]*\x27))?', destination)
            simple = re.fullmatch(r'([^\s<>]+)(?:\s+(?:"[^"\n]*"|\x27[^\x27\n]*\x27))?', destination)
            parsed = angle or simple
            if not parsed:
                self.error(page, "MARKDOWN_UNSUPPORTED", f"Unsupported inline link destination: {destination}")
                continue
            result.append(parsed[1])
        return result

    def links(self, page, text):
        for target in self.inline_links(page, markdown_body(text)):
            kind = "url" if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) else "local"
            self.reference(page, {"kind": kind, "target": target})

    def topic(self, page, text, template, example, companion):
        match = FRONTMATTER.match(text)
        if not match:
            self.error(page, "METADATA_INVALID", "Topic requires opening and closing --- YAML frontmatter.")
            return
        try:
            fields = safe_load(match[1])
        except InputError as exc:
            self.error(page, "METADATA_INVALID", str(exc))
            return
        if not isinstance(fields, Mapping):
            self.error(page, "METADATA_INVALID", "Frontmatter must be a mapping.")
            return
        kind = fields.get("type")
        if not isinstance(kind, str) or kind not in {"self", "derived", "adr", "source-companion"} or (companion and kind != "source-companion"):
            self.error(page, "METADATA_INVALID", "Invalid type (explicit source companions require type source-companion).")
        description = fields.get("description")
        if not nonempty(description) or "\n" in description or "\r" in description:
            self.error(page, "METADATA_INVALID", "description must be a nonempty one-line string.")
        updated = fields.get("updated")
        if not date_valid(updated) and not (template and placeholder(updated)):
            self.error(page, "METADATA_INVALID", "updated must be a valid YYYY-MM-DD date.")
        self.references(page, fields.get("source_refs"), template)
        if example and fields.get("example") is not True:
            self.error(page, "METADATA_INVALID", "Illustrative example pages require example: true.")
        status = fields.get("status")
        if kind == "adr":
            if not isinstance(status, str) or status not in {"Proposed", "Accepted", "Superseded", "Deprecated"}:
                self.error(page, "ADR_INVALID", "ADR status must be Proposed, Accepted, Superseded or Deprecated.")
            body = prose(text[match.end():])
            headings = set(re.findall(r"^ {0,3}#{1,6}\s+([^\n]+?)\s*#*\s*$", body, re.M))
            for heading in ADR_SECTIONS:
                if heading not in headings:
                    self.error(page, "ADR_INVALID", f"ADR section missing: {heading}")
            if status == "Accepted":
                decision = fields.get("human_decision")
                if not isinstance(decision, Mapping):
                    self.error(page, "ADR_INVALID", "Accepted ADR requires human_decision mapping.")
                else:
                    if not nonempty(decision.get("actor")):
                        self.error(page, "ADR_INVALID", "human_decision actor must be nonempty.")
                    if not date_valid(decision.get("decided_at")) and not (template and placeholder(decision.get("decided_at"))):
                        self.error(page, "ADR_INVALID", "human_decision decided_at must be a valid ISO date.")
                    self.reference(page, decision.get("evidence_ref"), template, retained=True)
            if status == "Deprecated" and not nonempty(fields.get("deprecation_reason")):
                self.error(page, "ADR_INVALID", "Deprecated ADR requires deprecation_reason.")
        elif not isinstance(status, str) or status not in {"draft", "current", "superseded"}:
            self.error(page, "METADATA_INVALID", "Ordinary status must be draft, current or superseded.")
        if isinstance(status, str) and status in {"superseded", "Superseded"}:
            self.reference(page, fields.get("superseded_by"), template, retained=True)

    def section(self, text, name):
        match = re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M)
        if not match:
            return None
        rest = text[match.end():]
        end = re.search(r"^#{1,2}\s", rest, re.M)
        return rest[:end.start()] if end else rest

    def hints(self, page, text):
        section = self.section(prose(text), "Navigation Hints")
        if section is None:
            self.error(page, "HINTS_INVALID", "Index requires ## Navigation Hints.")
            return
        if section.strip() == "No navigation hints yet.":
            return
        rows = [line.strip().strip("|").split("|") for line in section.splitlines() if line.strip().startswith("|")]
        if len(rows) < 3 or [cell.strip() for cell in rows[0]] != ["Task", "Target"] or len(rows[1]) != 2 or not all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in rows[1]):
            self.error(page, "HINTS_INVALID", "Navigation Hints requires Task | Target table or explicit empty state.")
            return
        for row in rows[2:]:
            if len(row) != 2 or not row[0].strip():
                self.error(page, "HINTS_INVALID", "Hint rows require a task and one local inline link.")
                continue
            cell = row[1].strip()
            targets = self.inline_links(page, cell)
            if len(targets) != 1 or not re.fullmatch(r"\[[^]\n]+\]\(.*\)", cell) or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", targets[0]):
                self.error(page, "HINTS_INVALID", "Each hint target must be exactly one local inline Markdown link.")
            else:
                self.local(page, targets[0])
                filename = unquote(targets[0].partition("#")[0])
                resolved = (page.parent / filename).resolve() if filename else page.resolve()
                if resolved.exists() and not resolved.is_dir() and resolved.suffix.lower() != ".md":
                    self.error(page, "HINTS_INVALID", "Hint target must identify a Markdown page or category directory.")

    def log(self, page, text):
        section = self.section(text, "Entries")
        if section is None:
            self.error(page, "LOG_INVALID", "Log requires ## Entries with one YAML fenced list.")
            return
        blocks = re.findall(r"^ {0,3}(`{3,}|~{3,})ya?ml\s*\n(.*?)^ {0,3}\1\s*$", section, re.M | re.S)
        if len(blocks) != 1:
            self.error(page, "LOG_INVALID", "Entries requires exactly one YAML fenced list.")
            return
        try:
            entries = safe_load(blocks[0][1])
        except InputError as exc:
            self.error(page, "LOG_INVALID", str(exc))
            return
        if not isinstance(entries, list):
            self.error(page, "LOG_INVALID", "Entries YAML must be a list; [] is valid.")
            return
        for number, entry in enumerate(entries, 1):
            if not isinstance(entry, Mapping):
                self.error(page, "LOG_INVALID", f"Entry {number} must be a mapping.")
                continue
            timestamp = entry.get("timestamp")
            try:
                valid_time = isinstance(timestamp, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", timestamp))
                if valid_time:
                    dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                valid_time = False
            if not valid_time:
                self.error(page, "LOG_INVALID", f"Entry {number} timestamp must be valid UTC ISO ending Z.")
            action = entry.get("action")
            if not isinstance(action, str) or action not in {"create", "update", "merge", "split", "reconcile", "lint"}:
                self.error(page, "LOG_INVALID", f"Entry {number} action is invalid.")
            paths = entry.get("paths")
            if not isinstance(paths, list) or not paths:
                self.error(page, "LOG_INVALID", f"Entry {number} paths must be a nonempty list.")
            else:
                for target in paths:
                    if not nonempty(target) or placeholder(target):
                        self.error(page, "LOG_INVALID", f"Entry {number} path must be an actual repo-relative path.")
                        continue
                    resolved = (self.repo / target).resolve()
                    if Path(target).is_absolute() or not within(resolved, self.repo) or not resolved.exists():
                        self.error(page, "LOG_INVALID", f"Entry {number} path missing or escapes repository: {target}")
            self.evidence(page, entry.get("evidence"))
            checks = entry.get("checks")
            if not isinstance(checks, list) or not checks:
                self.error(page, "LOG_INVALID", f"Entry {number} checks must be a nonempty list.")
                continue
            for check in checks:
                if not isinstance(check, Mapping):
                    self.error(page, "LOG_INVALID", f"Entry {number} check must be a mapping.")
                    continue
                status = check.get("status")
                if not isinstance(status, str) or status not in {"passed", "failed", "blocked", "not_run", "not_applicable"} or not nonempty(check.get("reason")) or placeholder(check.get("reason")):
                    self.error(page, "LOG_INVALID", f"Entry {number} check requires valid status and actual reason.")
                if status in ("passed", "failed"):
                    if not nonempty(check.get("command")) or placeholder(check.get("command")):
                        self.error(page, "LOG_INVALID", f"Entry {number} passed/failed check requires exact command.")
                    self.evidence(page, check.get("evidence"))

    def run(self):
        if not self.configure():
            return self.errors
        paths = set(self.root.rglob("*.md"))
        for key in ("source_companion_files", "index_files", "navigation_files", "log_files"):
            paths.update(self.classifications[key])
        for path in sorted(paths):
            resolved = path.resolve()
            if not within(resolved, self.root):
                self.error(path, "PATH_ESCAPE", "Knowledge page resolves outside the knowledge root.")
                continue
            raw = self.classified(resolved, "raw_source_dirs")
            companion = resolved in self.classifications["source_companion_files"]
            navigation = resolved in self.classifications["navigation_files"]
            if raw and not companion and not navigation:
                continue
            text = self.read(path)
            if text is None:
                continue
            if resolved in self.classifications["log_files"]:
                self.log(path, text)
                self.links(path, text)
                continue
            index = resolved in self.classifications["index_files"]
            if index:
                self.hints(path, text)
            if not navigation and not index:
                self.topic(path, text, self.classified(resolved, "template_dirs"), self.classified(resolved, "example_dirs"), companion)
            self.links(path, text)
        return sorted(self.errors, key=lambda d: (d["path"], d["code"], d["message"]))


def validate_knowledge(repo_root: Path, knowledge_root: Path,
                       layout: Mapping[str, object] | None = None) -> list[dict[str, str]]:
    return Checker(repo_root, knowledge_root, layout).run()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--knowledge-root", required=True, type=Path)
    parser.add_argument("--layout", type=Path)
    args = parser.parse_args()
    try:
        layout = safe_load(args.layout.read_text(encoding="utf-8")) if args.layout else None
        diagnostics = validate_knowledge(args.repo_root, args.knowledge_root, layout)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"CONFIG_INVALID: {exc}", file=sys.stderr)
        return 2
    for diagnostic in diagnostics:
        print("{path}: {code}: {message}".format(**diagnostic))
    if any(d["code"] in {"CONFIG_INVALID", "OPERATIONAL_ERROR"} for d in diagnostics):
        return 2
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
