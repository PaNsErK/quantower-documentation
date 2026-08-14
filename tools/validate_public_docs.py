#!/usr/bin/env python3
"""Fail-closed validation for the public documentation candidate."""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".venv", "site", "site-offline", "output", "__pycache__", ".pytest_cache"}
ALLOWED_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".css", ".js", ".py", ".txt", ".in"}
ALLOWED_SUFFIXLESS = {".gitignore", ".python-version"}
DENIED_PATH_PARTS = {".codex", ".agents", ".obsidian", "attachments", "logs", "serilog", "sidecars", "checkpoints"}
TEXT_MOJIBAKE = ("\u00c3", "\u00c2", "\ufffd")
PRIVATE_TEXT_PATTERNS = {
    "absolute_windows_path": re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|Program Files|codex_worktrees|Windows)\b"),
    "private_repo_name": re.compile(r"(?i)\bQT_Coding_Suite\b"),
    "private_user_marker": re.compile(r"(?i)\bWinnickiDavid\b|\bWINNIC\b"),
    "private_control_plane": re.compile(r"(?i)(?:^|[/\\])(?:EXECPLAN|PROJECT_STATUS|NEXT_WORK_QUEUE|PROJECT_GOVERNANCE|governance\.yml)(?:$|[/\\])"),
    "credential_assignment": re.compile(r"(?i)\b(?:token|password|secret|api[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "runtime_identifier": re.compile(r"(?i)\b(?:PID|HWND)\s*[:=]\s*[0-9A-Fx-]+"),
    "raw_log_extension": re.compile(r"(?i)\." r"slog\b"),
}
CUSTOM_JS_NETWORK_PATTERNS = {
    "fetch": re.compile(r"\bfetch\s*\("),
    "xhr": re.compile(r"\bXMLHttpRequest\b"),
    "websocket": re.compile(r"\bWebSocket\b"),
    "beacon": re.compile(r"\bsendBeacon\b"),
    "eventsource": re.compile(r"\bEventSource\b"),
    "remote_import": re.compile(r"\bimport\s*\(\s*['\"]https?://"),
}
SVG_DENY_PATTERNS = {
    "script": re.compile(r"<\s*script\b", re.I),
    "foreign_object": re.compile(r"<\s*foreignObject\b", re.I),
    "event_handler": re.compile(r"\son[a-z]+\s*=", re.I),
    "external_reference": re.compile(r"(?:href|src)\s*=\s*['\"]https?://", re.I),
    "javascript_url": re.compile(r"javascript\s*:", re.I),
}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def relative_files(root: Path, *, include_generated: bool = False) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts) and not include_generated:
            continue
        if path.is_symlink():
            fail(f"symbolic links are forbidden: {relative.as_posix()}")
        if path.is_file():
            if not include_generated and getattr(path.stat(), "st_nlink", 1) > 1:
                fail(f"hard links are forbidden: {relative.as_posix()}")
            files.append(path)
    return sorted(files)


def read_utf8(path: Path, *, check_mojibake: bool = True) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        fail(f"UTF-8 BOM is forbidden: {path}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"invalid UTF-8: {path}: {exc}") from exc
    if check_mojibake:
        for marker in TEXT_MOJIBAKE:
            if marker in text:
                fail(f"possible encoding damage {marker!r}: {path}")
    return text


def assert_safe_text(text: str, label: str) -> None:
    for name, pattern in PRIVATE_TEXT_PATTERNS.items():
        if pattern.search(text):
            fail(f"{name} detected in {label}")


def validate_source_tree(root: Path = ROOT) -> None:
    for path in relative_files(root):
        relative = path.relative_to(root)
        lower_parts = {part.lower() for part in relative.parts}
        if lower_parts & DENIED_PATH_PARTS:
            fail(f"denied path class: {relative.as_posix()}")
        if path.suffix.lower() not in ALLOWED_SUFFIXES and path.name not in ALLOWED_SUFFIXLESS:
            fail(f"unsupported public source file: {relative.as_posix()}")
        text = read_utf8(path)
        assert_safe_text(text, relative.as_posix())
        if path.suffix.lower() == ".js":
            for name, pattern in CUSTOM_JS_NETWORK_PATTERNS.items():
                if pattern.search(text):
                    fail(f"custom JavaScript network primitive {name}: {relative.as_posix()}")
        if "<svg" in text.lower():
            validate_svg_text(text, relative.as_posix())


def validate_svg_text(text: str, label: str) -> None:
    for name, pattern in SVG_DENY_PATTERNS.items():
        if pattern.search(text):
            fail(f"unsafe SVG construct {name}: {label}")


def load_json(path: Path) -> object:
    return json.loads(read_utf8(path))


def validate_json_instance(instance_path: Path, schema_path: Path) -> None:
    schema = load_json(schema_path)
    instance = load_json(instance_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    if errors:
        formatted = "; ".join(f"{list(error.absolute_path)}: {error.message}" for error in errors)
        fail(f"schema validation failed for {instance_path.name}: {formatted}")


def validate_manifest_and_coverage(root: Path = ROOT) -> None:
    manifest_path = root / "docs/data/public-indicator-manifest.json"
    schema_path = root / "schemas/public-indicator-manifest.schema.json"
    validate_json_instance(manifest_path, schema_path)
    manifest = load_json(manifest_path)
    assert isinstance(manifest, dict)
    topics = manifest["topics"]
    settings = manifest["settings"]
    manual_tests = manifest["manual_tests"]

    topic_ids = [item["id"] for item in topics]
    setting_ids = [item["id"] for item in settings]
    anchors = [item["documentation_anchor"] for item in settings]
    test_ids = [item["id"] for item in manual_tests]
    for label, values in (("topic", topic_ids), ("setting", setting_ids), ("anchor", anchors), ("manual test", test_ids)):
        if len(values) != len(set(values)):
            fail(f"duplicate {label} identifier")
    if len(topics) != 37 or topic_ids != [f"FZT-{index:02d}" for index in range(1, 38)]:
        fail("topic sequence must be exactly FZT-01 through FZT-37")
    if len(settings) != 29:
        fail("product-owned setting row count must be exactly 29")
    if sum(int(item["atomic_controls"]) for item in settings) != 41:
        fail("atomic setting-control count must be exactly 41")
    if test_ids != [f"FZMT-{index:02d}" for index in range(1, len(test_ids) + 1)]:
        fail("manual-test IDs must form one contiguous sequence")

    docs_text = "\n".join(read_utf8(path) for path in (root / "docs").rglob("*.md"))
    if '<section class="fz-topic"' in docs_text or '<div class="fz-depth"' in docs_text:
        fail("topic and depth containers must opt into Markdown-in-HTML parsing")
    for topic_id in topic_ids:
        if docs_text.count(f'data-topic="{topic_id}"') != 1:
            fail(f"topic marker must occur exactly once: {topic_id}")
    for anchor in anchors:
        anchor_count = docs_text.count(f'id="{anchor}"') + docs_text.count(f'{{ #{anchor} }}')
        if anchor_count != 1:
            fail(f"setting documentation anchor must occur exactly once: {anchor}")
    manual_catalog = load_json(root / "docs/includes/manual-test-catalog.json")
    if manual_catalog != manual_tests:
        fail("embedded manual-test catalog differs from the public manifest")
    manual_page = read_utf8(root / "docs/indicators/fractal-zones/test/manual-suite.md")
    if 'id="fz-manual-test-catalog"' not in manual_page or "docs/includes/manual-test-catalog.json" not in manual_page:
        fail("interactive suite does not embed the validated manual-test catalog")
    for test_id in test_ids:
        if f'"id":"{test_id}"' not in read_utf8(root / "docs/includes/manual-test-catalog.json"):
            fail(f"manual test not embedded in interactive suite: {test_id}")

    claimed_pages = {item["page"] for item in topics}
    for relative in claimed_pages:
        if not (root / "docs" / relative).is_file():
            fail(f"topic references missing page: {relative}")


def validate_workflow(root: Path = ROOT) -> None:
    path = root / ".github/workflows/pages.yml"
    text = read_utf8(path)
    workflow = yaml.safe_load(text)
    if workflow.get("permissions") != {}:
        fail("workflow top-level permissions must be empty")
    trigger = workflow.get("on") or workflow.get(True)
    if not isinstance(trigger, dict) or "pull_request" not in trigger or "push" not in trigger:
        fail("workflow must validate pull requests and main pushes")
    for forbidden in ("pull_request_target", "workflow_run", "repository_dispatch"):
        if forbidden in trigger:
            fail(f"forbidden workflow trigger: {forbidden}")
    jobs = workflow.get("jobs", {})
    if set(jobs) != {"build", "deploy"}:
        fail("workflow must contain exactly build and deploy jobs")
    if jobs["build"].get("permissions") != {"contents": "read"}:
        fail("build job must have contents: read only")
    if jobs["deploy"].get("permissions") != {"pages": "write", "id-token": "write"}:
        fail("deploy job permissions are not least-privilege")
    if jobs["deploy"].get("needs") != "build":
        fail("deploy job must depend on build")
    if jobs["deploy"].get("environment", {}).get("name") != "github-pages":
        fail("deploy environment must be github-pages")
    deploy_steps = jobs["deploy"].get("steps", [])
    if len(deploy_steps) != 1 or "run" in deploy_steps[0]:
        fail("deploy job must contain exactly one action-only step")
    allowed_actions = {
        "actions/checkout": "d23441a48e516b6c34aea4fa41551a30e30af803",
        "actions/setup-python": "ece7cb06caefa5fff74198d8649806c4678c61a1",
        "actions/upload-pages-artifact": "7b1f4a764d45c48632c6b24a0339c27f5614fb0b",
        "actions/deploy-pages": "d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e",
    }
    found: dict[str, str] = {}
    for job in jobs.values():
        for step in job.get("steps", []):
            uses = step.get("uses")
            if not uses:
                continue
            action, separator, sha = uses.partition("@")
            if not separator or not re.fullmatch(r"[0-9a-f]{40}", sha):
                fail(f"action is not pinned to a full SHA: {uses}")
            if action not in allowed_actions or allowed_actions[action] != sha:
                fail(f"unapproved action reference: {uses}")
            found[action] = sha
    if found != allowed_actions:
        fail("workflow action inventory is incomplete")
    if deploy_steps[0].get("uses") != f"actions/deploy-pages@{allowed_actions['actions/deploy-pages']}":
        fail("deploy job may execute only the pinned deploy-pages action")
    denied_workflow_tokens = ("secrets.", "contents: write", "actions: write", "pull-requests: write", "issues: write", "repository:", "submodules: true")
    for token in denied_workflow_tokens:
        if token in text:
            fail(f"forbidden workflow capability: {token}")


def validate_manual_result_fixture(root: Path = ROOT) -> None:
    validate_json_instance(
        root / "tests/fixtures/manual-result-valid.json",
        root / "schemas/manual-test-result.schema.json",
    )


class ResourceHTMLParser(HTMLParser):
    RESOURCE_ATTRIBUTES = {
        "script": "src",
        "img": "src",
        "source": "src",
        "audio": "src",
        "video": "src",
        "iframe": "src",
    }

    def __init__(self) -> None:
        super().__init__()
        self.external_resources: list[str] = []
        self.internal_links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        attribute = self.RESOURCE_ATTRIBUTES.get(tag)
        if attribute and values.get(attribute, "").startswith(("http://", "https://", "//")):
            self.external_resources.append(f"{tag}:{values[attribute]}")
        if tag == "link" and values.get("rel") in {"stylesheet", "preload", "modulepreload"}:
            href = values.get("href", "")
            if href.startswith(("http://", "https://", "//")):
                self.external_resources.append(f"link:{href}")
        if tag == "a":
            href = values.get("href", "")
            parsed = urlsplit(href)
            if href and not parsed.scheme and not parsed.netloc and parsed.path:
                self.internal_links.append(href)


def validate_generated_internal_link(root: Path, source: Path, href: str) -> None:
    parsed = urlsplit(href)
    raw_path = unquote(parsed.path).replace("\\", "/")
    if raw_path.startswith("/quantower-documentation/"):
        candidate = root / raw_path.removeprefix("/quantower-documentation/")
    elif raw_path.startswith("/"):
        candidate = root / raw_path.lstrip("/")
    else:
        candidate = source.parent / raw_path
    candidate = candidate.resolve()
    if candidate != root.resolve() and root.resolve() not in candidate.parents:
        fail(f"generated internal link escapes site root: {source.relative_to(root)} -> {href}")
    if candidate.is_dir():
        candidate = candidate / "index.html"
    elif not candidate.suffix:
        directory_index = candidate / "index.html"
        html_file = candidate.with_suffix(".html")
        candidate = directory_index if directory_index.is_file() else html_file
    if not candidate.is_file():
        fail(f"broken generated internal link: {source.relative_to(root)} -> {href}")


def resolve_safe_root(value: str, label: str) -> Path:
    candidate = (ROOT / value).resolve()
    if candidate == ROOT or ROOT not in candidate.parents:
        fail(f"{label} escapes repository root")
    if not candidate.is_dir():
        fail(f"{label} does not exist: {value}")
    return candidate


def validate_generated_site(site_root: Path, offline_root: Path) -> None:
    for root in (site_root, offline_root):
        html_files = list(root.rglob("*.html"))
        if not html_files:
            fail(f"generated site contains no HTML: {root}")
        for path in relative_files(root, include_generated=True):
            relative = path.relative_to(root).as_posix()
            if relative == "sitemap.xml.gz":
                try:
                    compressed_text = gzip.decompress(path.read_bytes()).decode("utf-8")
                except (OSError, UnicodeDecodeError) as exc:
                    raise ValidationError(f"invalid compressed sitemap: {relative}: {exc}") from exc
                assert_safe_text(compressed_text, f"generated:{relative}")
                continue
            if path.suffix.lower() not in {".html", ".css", ".js", ".json", ".map", ".svg", ".png", ".ico", ".woff", ".woff2", ".txt", ".xml"}:
                fail(f"unexpected generated file type: {relative}")
            if path.suffix.lower() in {".html", ".css", ".js", ".json", ".map", ".svg", ".txt", ".xml"}:
                check_mojibake = path.suffix.lower() == ".html" or relative in {
                    "assets/javascripts/fractal-zones.js",
                    "assets/javascripts/manual-tests.js",
                    "assets/stylesheets/fractal-zones.css",
                }
                text = read_utf8(path, check_mojibake=check_mojibake)
                assert_safe_text(text, f"generated:{relative}")
                if path.suffix.lower() == ".html":
                    parser = ResourceHTMLParser()
                    parser.feed(text)
                    if parser.external_resources:
                        fail(f"external runtime resource in {relative}: {parser.external_resources[0]}")
                    for href in parser.internal_links:
                        validate_generated_internal_link(root, path, href)
        if not (root / "index.html").is_file():
            fail(f"generated site misses index.html: {root}")
        manual_relative = (
            Path("indicators/fractal-zones/test/manual-suite/index.html")
            if root == site_root
            else Path("indicators/fractal-zones/test/manual-suite.html")
        )
        manual_html = read_utf8(root / manual_relative)
        for heading_id in (
            "erstinstallation-und-settings-testen",
            "lifecycle-und-darstellung-testen",
            "historie-recovery-und-performance-testen",
        ):
            if not re.search(rf'<h2\s+id="{heading_id}">', manual_html):
                fail(f"manual suite topic heading was not rendered as h2: {heading_id}")
        if "## Erstinstallation und Settings testen" in manual_html:
            fail("manual suite leaks an unparsed Markdown heading")
    if not (offline_root / "indicators/fractal-zones/test/manual-suite.html").is_file():
        fail("offline build must use file-addressable .html pages")


def validate_markdown_links(root: Path = ROOT) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
    for path in (root / "docs").rglob("*.md"):
        text = read_utf8(path)
        for raw_target in link_pattern.findall(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or target.startswith("<"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                fail(f"broken Markdown link in {path.relative_to(root)}: {target}")


def run_source_checks() -> None:
    validate_source_tree()
    validate_manifest_and_coverage()
    validate_workflow()
    validate_manual_result_fixture()
    validate_markdown_links()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("source")
    subparsers.add_parser("all")
    generated = subparsers.add_parser("generated")
    generated.add_argument("--site-root", default="site")
    generated.add_argument("--offline-root", default="site-offline")
    args = parser.parse_args(argv)
    try:
        if args.command in {"source", "all"}:
            run_source_checks()
        if args.command == "generated":
            validate_generated_site(
                resolve_safe_root(args.site_root, "site root"),
                resolve_safe_root(args.offline_root, "offline root"),
            )
    except (ValidationError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {args.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
