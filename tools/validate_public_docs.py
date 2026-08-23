#!/usr/bin/env python3
"""Fail-closed validation for the public Fractal Zones documentation."""

from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".venv", "site", "site-offline", "output", "__pycache__", ".pytest_cache"}
ALLOWED_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".css", ".js", ".py", ".txt", ".in"}
ALLOWED_SUFFIXLESS = {".gitignore", ".python-version"}
DENIED_PATH_PARTS = {".codex", ".agents", ".obsidian", "attachments", "logs", "serilog", "sidecars", "checkpoints"}
PRIVATE_PATTERNS = {
    "absolute_windows_path": re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|Program Files|codex_worktrees|Windows)\b"),
    "private_repo_name": re.compile(r"(?i)\bQT_Coding_Suite\b|\bquantower-coding-suite\b"),
    "private_user_marker": re.compile(r"(?i)\bWinnickiDavid\b|\bWINNIC\b"),
    "private_control_plane": re.compile(r"(?i)(?:^|[/\\])(?:EXECPLAN|PROJECT_STATUS|NEXT_WORK_QUEUE|PROJECT_GOVERNANCE|governance\.yml)(?:$|[/\\])"),
    "credential_assignment": re.compile(r"(?i)\b(?:token|password|secret|api[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "runtime_identifier": re.compile(r"(?i)\b(?:PID|HWND)\s*[:=]\s*[0-9A-Fx-]+"),
    "raw_log_extension": re.compile(r"(?i)\.slog\b"),
}
NETWORK_PATTERNS = {
    "fetch": re.compile(r"\bfetch\s*\("), "xhr": re.compile(r"\bXMLHttpRequest\b"),
    "websocket": re.compile(r"\bWebSocket\b"), "beacon": re.compile(r"\bsendBeacon\b"),
    "eventsource": re.compile(r"\bEventSource\b"), "remote_import": re.compile(r"\bimport\s*\(\s*['\"]https?://"),
}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def relative_files(root: Path, *, include_generated: bool = False) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if not include_generated and any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.is_symlink():
            fail(f"symbolic links are forbidden: {relative.as_posix()}")
        if path.is_file():
            files.append(path)
    return sorted(files)


def read_utf8(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        fail(f"UTF-8 BOM is forbidden: {path}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"invalid UTF-8: {path}") from exc
    # LF identity for newly authored files is enforced by the transaction's
    # exact-scope gate. The public baseline contains unchanged CRLF files
    # outside that scope, which are still safe UTF-8 input.
    if text != unicodedata.normalize("NFC", text):
        fail(f"non-NFC text: {path}")
    if any(marker in text for marker in ("\u00c3", "\u00c2", "\ufffd")):
        fail(f"possible mojibake: {path}")
    return text


def assert_safe_text(text: str, label: str) -> None:
    for name, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(text):
            fail(f"{name} detected in {label}")


def load_json(path: Path) -> object:
    return json.loads(read_utf8(path))


def validate_json_instance(instance_path: Path, schema_path: Path) -> None:
    errors = sorted(
        Draft202012Validator(load_json(schema_path), format_checker=FormatChecker()).iter_errors(load_json(instance_path)),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        fail(f"schema validation failed: {instance_path.name}: {errors[0].message}")


def load_source_drift_module():
    spec = importlib.util.spec_from_file_location("source_drift", ROOT / "tools/check_fractal_zones_source_drift.py")
    if spec is None or spec.loader is None:
        fail("source drift module unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_source_tree(root: Path = ROOT) -> None:
    for path in relative_files(root):
        relative = path.relative_to(root)
        if {part.lower() for part in relative.parts} & DENIED_PATH_PARTS:
            fail(f"denied path class: {relative.as_posix()}")
        if path.suffix.lower() not in ALLOWED_SUFFIXES and path.name not in ALLOWED_SUFFIXLESS:
            fail(f"unsupported public source file: {relative.as_posix()}")
        text = read_utf8(path)
        # This validator necessarily contains the denylist literals it applies
        # to every other public source file.
        if relative.as_posix() != "tools/validate_public_docs.py":
            assert_safe_text(text, relative.as_posix())
        if path.suffix.lower() == ".js":
            for name, pattern in NETWORK_PATTERNS.items():
                if pattern.search(text):
                    fail(f"custom JavaScript network primitive {name}: {relative.as_posix()}")


def sequence(prefix: str, count: int, width: int) -> list[str]:
    return [f"{prefix}-{index:0{width}d}" for index in range(1, count + 1)]


def validate_manifest_and_coverage(root: Path = ROOT) -> None:
    manifest_path = root / "docs/data/public-indicator-manifest.json"
    contract_path = root / "docs/data/fractal-zones-source-contract.json"
    runtime_path = root / "docs/data/fractal-zones-runtime-acceptance.json"
    validate_json_instance(manifest_path, root / "schemas/public-indicator-manifest.schema.json")
    validate_json_instance(contract_path, root / "schemas/fractal-zones-source-contract.schema.json")
    validate_json_instance(runtime_path, root / "schemas/fractal-zones-runtime-acceptance.schema.json")
    manifest = load_json(manifest_path)
    contract = load_json(contract_path)
    runtime = load_json(runtime_path)
    if not all(isinstance(item, dict) for item in (manifest, contract, runtime)):
        fail("closed contract root is invalid")
    load_source_drift_module().validate_contract_coupling(contract, manifest)
    settings = manifest["settings"]
    ids = [item["id"] for item in settings]
    anchors = [item["documentation_anchor"] for item in settings]
    if len(ids) != 56 or len(set(ids)) != 56 or sum(item["atomic_controls"] for item in settings) != 70:
        fail("setting inventory must be exactly 56 rows and 70 atomic controls")
    if sum(item["type"] == "line_options" for item in settings) != 7 or sum(item["type"] == "action" for item in settings) != 2:
        fail("line-option or action count differs")
    if len(manifest["base_settings"]) != 11 or sum(item["atomic_controls"] for item in manifest["base_settings"]) != 25:
        fail("version-bound base.Settings observation differs")
    page_ids = [item["id"] for item in manifest["pages"]]
    if page_ids != sequence("FZT", 27, 2):
        fail("page IDs must be FZT-01 through FZT-27")
    for item in manifest["pages"]:
        if not (root / "docs" / item["page"]).is_file():
            fail(f"missing documented page: {item['page']}")
    fzmt = load_json(root / "docs/includes/manual-test-catalog.json")
    user = load_json(root / "docs/includes/fractal-zones-v2-remediation-user-test-catalog.json")
    catalog_schema = root / "schemas/manual-test-catalog.schema.json"
    validate_json_instance(root / "docs/includes/manual-test-catalog.json", catalog_schema)
    validate_json_instance(root / "docs/includes/fractal-zones-v2-remediation-user-test-catalog.json", catalog_schema)
    if [item["id"] for item in fzmt] != sequence("FZMT", 24, 2):
        fail("FZMT suite must remain FZMT-01 through FZMT-24")
    if [item["id"] for item in user] != [f"FZV2-RM-{index:03d}" for index in range(1, 20)]:
        fail("user suite must be FZV2-RM-001 through FZV2-RM-019")
    if any("result" in item or "note" in item for item in user):
        fail("pending user catalog must not contain results or notes")
    if manifest["conformance"] != {"packs":["v1","v2","v3","v4"],"requirements_count":102,"golden_trace_count":180,"manual_acceptance_count":25,"sequence_state":"contiguous_closed"}:
        fail("conformance projection differs")
    if runtime["soak"] != {"elapsed_seconds":2700.009,"process_samples":188,"responsive_samples":188,"ui_usable":True,"host_hang_or_crash_observed":False}:
        fail("runtime soak facts differ")
    if [item["class"] for item in runtime["ranges"]] != ["10k","30k","approximately_130k"]:
        fail("runtime range classes differ")
    docs_text = "\n".join(read_utf8(path) for path in (root / "docs").rglob("*.md"))
    for anchor in anchors:
        count = docs_text.count(f'id="{anchor}"') + docs_text.count(f'id={anchor}') + docs_text.count(f'{{ #{anchor} }}')
        if count != 1:
            fail(f"setting anchor must occur exactly once: {anchor} ({count})")
    required_phrases = ["manual_acceptance_complete=false", "runtime_acceptance_complete=true", "pending_user_evaluation"]
    public_status = read_utf8(root / "README.md") + read_utf8(root / "docs/index.md") + read_utf8(root / "docs/indicators/fractal-zones/current-state.md")
    for phrase in required_phrases:
        if phrase not in public_status:
            fail(f"public status phrase missing: {phrase}")
    if "inoffiziell" not in public_status.lower():
        fail("unofficial publication notice missing")


def validate_workflow(root: Path = ROOT) -> None:
    path = root / ".github/workflows/pages.yml"
    workflow = yaml.safe_load(read_utf8(path))
    if workflow.get("permissions") != {}:
        fail("workflow top-level permissions must be empty")
    trigger = workflow.get("on") or workflow.get(True)
    if not isinstance(trigger, dict) or "pull_request" not in trigger or "push" not in trigger:
        fail("workflow triggers differ")
    jobs = workflow.get("jobs", {})
    if set(jobs) != {"build", "deploy"}:
        fail("workflow job inventory differs")
    if jobs["build"].get("permissions") != {"contents":"read"} or jobs["deploy"].get("permissions") != {"pages":"write","id-token":"write"}:
        fail("workflow permissions differ")
    for job in jobs.values():
        for step in job.get("steps", []):
            uses = step.get("uses")
            if uses and not re.fullmatch(r"[^@]+@[0-9a-f]{40}", uses):
                fail(f"workflow action is not SHA-pinned: {uses}")

    build_commands = [
        line.strip()
        for step in jobs["build"].get("steps", [])
        for line in str(step.get("run", "")).splitlines()
        if line.strip()
    ]
    expected_order = [
        "python tools/validate_public_docs.py source",
        "python -m unittest discover -s tests -p 'test_*.py' -v",
        "python -m mkdocs build --strict",
        "python -m mkdocs build --strict -f mkdocs.offline.yml",
        "python tools/validate_public_docs.py generated --site-root site --offline-root site-offline",
    ]
    for command in expected_order:
        if build_commands.count(command) != 1:
            fail(f"workflow validation command inventory differs: {command}")
    if any(command.startswith("python tools/validate_public_docs.py all") for command in build_commands):
        fail("workflow must keep source and generated validation in separate ordered stages")
    positions = [build_commands.index(command) for command in expected_order]
    if positions != sorted(positions):
        fail("workflow validation and build order differs")


class ResourceHTMLParser(HTMLParser):
    RESOURCE_ATTRIBUTES = {"script":"src","img":"src","source":"src","iframe":"src","link":"href"}
    def __init__(self) -> None:
        super().__init__(); self.external_resources: list[str] = []; self.internal_links: list[str] = []
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs); attribute = self.RESOURCE_ATTRIBUTES.get(tag); value = values.get(attribute, "") if attribute else ""
        is_runtime_resource = tag != "link" or "stylesheet" in str(values.get("rel", "")).lower()
        if is_runtime_resource and value.startswith(("http://","https://","//")):
            self.external_resources.append(f"{tag}:{value}")
        if tag == "a":
            href = values.get("href", ""); parsed = urlsplit(href)
            if href and not parsed.scheme and not parsed.netloc and parsed.path:
                self.internal_links.append(href)


def validate_generated_internal_link(root: Path, source: Path, href: str) -> None:
    raw = unquote(urlsplit(href).path).replace("\\", "/")
    if raw.startswith("/quantower-documentation/"):
        candidate = root / raw.removeprefix("/quantower-documentation/")
    elif raw.startswith("/"):
        candidate = root / raw.lstrip("/")
    else:
        candidate = source.parent / raw
    candidate = candidate.resolve(); resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        fail(f"generated link escapes root: {href}")
    if candidate.is_dir(): candidate = candidate / "index.html"
    elif not candidate.suffix:
        candidate = candidate / "index.html" if (candidate / "index.html").is_file() else candidate.with_suffix(".html")
    if not candidate.is_file(): fail(f"broken generated internal link: {source.relative_to(root)} -> {href}")


def resolve_safe_root(value: str, label: str) -> Path:
    candidate = (ROOT / value).resolve()
    if candidate == ROOT or ROOT not in candidate.parents or not candidate.is_dir():
        fail(f"{label} is unsafe or missing")
    return candidate


def validate_generated_site(site_root: Path, offline_root: Path) -> None:
    for root in (site_root, offline_root):
        html_files = list(root.rglob("*.html"))
        if not html_files: fail(f"generated site has no HTML: {root}")
        for path in relative_files(root, include_generated=True):
            relative = path.relative_to(root).as_posix()
            if relative == "sitemap.xml.gz":
                assert_safe_text(gzip.decompress(path.read_bytes()).decode("utf-8"), f"generated:{relative}")
                continue
            if path.suffix.lower() in {".html",".css",".js",".json",".svg",".txt",".xml"}:
                text = path.read_text(encoding="utf-8")
                assert_safe_text(text, f"generated:{relative}")
            if path.suffix.lower() == ".html":
                parser = ResourceHTMLParser(); parser.feed(path.read_text(encoding="utf-8"))
                if parser.external_resources: fail(f"external runtime asset: {relative}")
                for href in parser.internal_links: validate_generated_internal_link(root, path, href)


def validate_fixtures(root: Path = ROOT) -> None:
    validate_json_instance(root / "tests/fixtures/manual-result-v2-valid.json", root / "schemas/manual-test-result.schema.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("mode", choices=["source","generated","all"]); parser.add_argument("--site-root", default="site"); parser.add_argument("--offline-root", default="site-offline"); args = parser.parse_args(argv)
    try:
        if args.mode in {"source","all"}:
            validate_source_tree(ROOT); validate_manifest_and_coverage(ROOT); validate_workflow(ROOT); validate_fixtures(ROOT)
        if args.mode in {"generated","all"}:
            validate_generated_site(resolve_safe_root(args.site_root,"site root"), resolve_safe_root(args.offline_root,"offline root"))
    except (ValidationError, OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr); return 1
    print(f"validation passed: {args.mode}"); return 0


if __name__ == "__main__":
    raise SystemExit(main())
