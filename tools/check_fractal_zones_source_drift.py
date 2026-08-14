#!/usr/bin/env python3
"""Validate the public Fractal Zones contract against a local source checkout.

The checker is intentionally one-way: it reads a caller-supplied source root,
emits only closed aggregate facts, and never prints or persists source paths,
source text, repository metadata, commits, or source-file hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs/data/fractal-zones-source-contract.json"
MANIFEST_PATH = ROOT / "docs/data/public-indicator-manifest.json"
EXCLUDED_SOURCE_PARTS = {
    ".git",
    ".vs",
    ".venv",
    "bin",
    "obj",
    "external",
    "packages",
    "site",
    "site-offline",
}
SETTING_DIGEST_DOMAIN = b"fz-public-setting-facts-v1\0"
CONTRACT_DIGEST_DOMAIN = b"fz-public-source-contract-v1\0"


class SourceContractError(RuntimeError):
    """Closed failure that is safe to show without a local path."""

    def __init__(self, state: str, message: str) -> None:
        super().__init__(message)
        self.state = state


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SourceContractError("unsafe_or_ambiguous_source", "JSON root must be an object")
    return value


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def setting_fact_projection(manifest: dict[str, object]) -> list[dict[str, object]]:
    settings = manifest.get("settings")
    if not isinstance(settings, list):
        raise SourceContractError("documentation_drift", "public settings inventory is not an array")
    keys = ("id", "default", "range_or_options", "visibility", "atomic_controls")
    return [{key: item[key] for key in keys} for item in settings if isinstance(item, dict)]


def compute_setting_fact_digest(manifest: dict[str, object]) -> str:
    return hashlib.sha256(SETTING_DIGEST_DOMAIN + canonical_json(setting_fact_projection(manifest))).hexdigest()


def compute_contract_digest(contract: dict[str, object]) -> str:
    payload = dict(contract)
    payload.pop("contract_digest", None)
    return hashlib.sha256(CONTRACT_DIGEST_DOMAIN + canonical_json(payload)).hexdigest()


def validate_contract_coupling(
    contract: dict[str, object],
    manifest: dict[str, object],
) -> None:
    expected_setting_digest = compute_setting_fact_digest(manifest)
    if contract.get("setting_fact_digest") != expected_setting_digest:
        raise SourceContractError("documentation_drift", "setting facts differ from the sanitized source contract")
    expected_contract_digest = compute_contract_digest(contract)
    if contract.get("contract_digest") != expected_contract_digest:
        raise SourceContractError("documentation_drift", "sanitized source-contract digest differs")
    coupling = manifest.get("source_contract")
    if not isinstance(coupling, dict):
        raise SourceContractError("documentation_drift", "public manifest does not reference the source contract")
    if coupling.get("contract_digest") != expected_contract_digest:
        raise SourceContractError("documentation_drift", "public manifest source-contract digest differs")
    if coupling.get("setting_fact_digest") != expected_setting_digest:
        raise SourceContractError("documentation_drift", "public manifest setting-fact digest differs")


def iter_source_files(root: Path, suffix: str) -> Iterable[Path]:
    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        directories[:] = sorted(
            directory
            for directory in directories
            if directory.lower() not in EXCLUDED_SOURCE_PARTS
            and not (Path(current) / directory).is_symlink()
        )
        for filename in sorted(filenames):
            if not filename.endswith(suffix):
                continue
            path = Path(current) / filename
            if path.is_symlink() or not path.is_file():
                continue
            yield path


def discover_unique_text(root: Path, marker: str) -> str:
    matches: list[str] = []
    for path in iter_source_files(root, ".cs"):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if marker in text:
            matches.append(text)
    if len(matches) != 1:
        raise SourceContractError(
            "unsafe_or_ambiguous_source",
            f"source role {marker!r} resolved to {len(matches)} candidates",
        )
    return matches[0]


def discover_unique_json(root: Path, predicate: Callable[[dict[str, object]], bool], role: str) -> dict[str, object]:
    matches: list[dict[str, object]] = []
    for path in iter_source_files(root, ".json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict) and predicate(value):
            matches.append(value)
    if len(matches) != 1:
        raise SourceContractError(
            "unsafe_or_ambiguous_source",
            f"source role {role!r} resolved to {len(matches)} candidates",
        )
    return matches[0]


def resolve_string_symbols(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    pattern = re.compile(
        r"private\s+static\s+readonly\s+string\s+(?P<name>[A-Za-z_]\w*)\s*=\s*(?P<expr>(?:\"[^\"]*\"\s*\+?\s*)+);"
    )
    for match in pattern.finditer(text):
        result[match.group("name")] = "".join(re.findall(r'\"([^\"]*)\"', match.group("expr")))
    return result


def extract_setting_ids(indicator_text: str) -> tuple[list[str], int, int]:
    symbols = resolve_string_symbols(indicator_text)
    names: list[str] = []
    constructor_pattern = re.compile(
        r"new\s+SettingItem(?:Integer|Double|Boolean|DateTime|Action|SelectorLocalized)\s*\(\s*(?:\"(?P<literal>[^\"]+)\"|(?P<symbol>[A-Za-z_]\w*))",
        re.S,
    )
    for match in constructor_pattern.finditer(indicator_text):
        value = match.group("literal") or symbols.get(match.group("symbol") or "")
        if value:
            names.append(value)
    states = re.findall(r'AddLineSettings\s*\(\s*settings\s*,\s*\"([^\"]+)\"', indicator_text)
    for state in states:
        names.extend((f"{state}TopLineOptions", f"{state}BottomLineOptions"))
    action_count = len(re.findall(r"new\s+SettingItemAction\s*\(", indicator_text))
    line_option_count = len(states) * 2
    return names, action_count, line_option_count


def require_patterns(text: str, patterns: Iterable[str], role: str) -> None:
    for pattern in patterns:
        if not re.search(pattern, text, re.S):
            raise SourceContractError("documentation_drift", f"required {role} contract fact is absent")


def setting_block(text: str, setting_name: str) -> str:
    start = text.find(f'"{setting_name}"')
    if start < 0:
        raise SourceContractError("documentation_drift", f"setting {setting_name} is absent")
    brace = text.find("{", start)
    end = text.find("});", brace)
    if brace < 0 or end < 0:
        raise SourceContractError("unsafe_or_ambiguous_source", f"setting {setting_name} block is ambiguous")
    return text[brace : end + 1]


def validate_fzrui_contracts(indicator: str, host_tests: str) -> None:
    opacity_block = setting_block(indicator, "InactiveStateOpacity")
    require_patterns(
        opacity_block,
        (
            r"Minimum\s*=\s*0\.10",
            r"Maximum\s*=\s*1\.00",
            r"Increment\s*=\s*0\.05",
            r"DecimalPlaces\s*=\s*2",
        ),
        "FZRUI-01 setting",
    )
    require_patterns(
        host_tests,
        (
            r"ActiveFocusOpacityUsesTwoDecimalHostMetadata",
            r"opacity\.DecimalPlaces\s*==\s*2",
            r"opacity\.Increment\s*-\s*0\.05",
            r"opacity\.Value\s*-\s*0\.35",
        ),
        "FZRUI-01 host regression",
    )

    start_block = setting_block(indicator, "CalculationStartTime")
    require_patterns(
        start_block,
        (r"UseEnabilityToggler\s*=\s*true", r"Enabled\s*=\s*calculationStartTimeUtc\.HasValue"),
        "FZRUI-02 setting",
    )
    require_patterns(
        host_tests,
        (
            r"CalculationStartTime.*UseEnabilityToggler",
            r"ExplicitCalculationStartRemainsUtcStable",
            r"ClearingCalculationStartReturnsToInitialRangeMode",
        ),
        "FZRUI-02 host regression",
    )


def expected_sequence(prefix: str, count: int, width: int) -> list[str]:
    return [f"{prefix}-{index:0{width}d}" for index in range(1, count + 1)]


def verify_source(root: Path, contract: dict[str, object], manifest: dict[str, object]) -> dict[str, object]:
    if not root.is_dir():
        raise SourceContractError("unsafe_or_ambiguous_source", "source root is unavailable")

    source_root = root / "src"
    test_root = root / "tests"
    if not source_root.is_dir() or not test_root.is_dir():
        raise SourceContractError("unsafe_or_ambiguous_source", "required source roles are unavailable")
    indicator = discover_unique_text(source_root, "public sealed class FractalZonesIndicator")
    break_contract = discover_unique_text(source_root, "public sealed record FractalZonesBreakSettings")
    lifecycle_contract = discover_unique_text(source_root, "public sealed record FractalZonesLifecycleSettings")
    host_tests = discover_unique_text(test_root, "internal static class FractalZonesHostTests")
    source_snapshot = discover_unique_json(
        test_root,
        lambda value: value.get("documentType") == "sourceSnapshot"
        and value.get("packId") == "qtcs-fractal-zones-conformance-v2",
        "FZCP source snapshot",
    )
    composite_manifest = discover_unique_json(
        test_root,
        lambda value: value.get("documentType") == "compositeManifest"
        and value.get("packId") == "qtcs-fractal-zones-conformance-v2",
        "FZCP composite manifest",
    )

    inventory = contract["inventory"]
    if not isinstance(inventory, dict):
        raise SourceContractError("documentation_drift", "source-contract inventory is invalid")
    setting_ids, action_count, line_option_count = extract_setting_ids(indicator)
    expected_ids = inventory["setting_ids"]
    if len(setting_ids) != len(set(setting_ids)):
        raise SourceContractError("documentation_drift", "duplicate product setting IDs detected")
    if set(setting_ids) != set(expected_ids):
        raise SourceContractError("documentation_drift", "product setting ID inventory changed")
    if action_count != inventory["product_owned_actions"]:
        raise SourceContractError("documentation_drift", "product action count changed")
    if line_option_count != inventory["line_option_rows"]:
        raise SourceContractError("documentation_drift", "line-option row count changed")
    if len(setting_ids) != inventory["product_owned_setting_rows"]:
        raise SourceContractError("documentation_drift", "product setting-row count changed")
    atomic_count = len(setting_ids) + (line_option_count * 2)
    if atomic_count != inventory["maximum_atomic_controls"]:
        raise SourceContractError("documentation_drift", "product atomic-control count changed")

    require_patterns(
        indicator,
        (
            r"DefaultMaturityBeforeMinutes\s*=\s*30\s*;",
            r"DefaultMaturityAfterMinutes\s*=\s*30\s*;",
            r"DefaultInitialHistoryDays\s*=\s*90\s*;",
            r"MaximumLineWidth\s*=\s*10\s*;",
            r"enableReplayCheckpoint\s*;",
            r"inactiveStateOpacity\s*=\s*0\.35\s*;",
            r"showEndMarker\s*=\s*true\s*;",
            r"showBreakMarkers\s*;",
            r"showRoleMarkers\s*=\s*true\s*;",
            r"FractalZonesRenderingMode\.Adaptive",
            r"FractalZonesCalculationRangeMode\.FixedInitialHistoryDays",
            r"CreateLineOptions\(Color\.Green,\s*LineStyle\.Dot\)",
            r"CreateLineOptions\(Color\.Red,\s*LineStyle\.Dot\)",
            r"CreateLineOptions\(Color\.Green,\s*LineStyle\.Solid\)",
            r"CreateLineOptions\(Color\.Red,\s*LineStyle\.Solid\)",
            r"CreateLineOptions\(Color\.Green,\s*LineStyle\.Dash\)",
            r"CreateLineOptions\(Color\.Red,\s*LineStyle\.Dash\)",
            r"SettingItemRelationVisibility\(\"RenderingMode\",\s*activeFocusMode\)",
            r"SettingItemRelationVisibility\(\"CalculationRangeMode\",\s*fixedRange\)",
            r"SettingItemRelationVisibility\(\"BreakDistanceMode\",\s*atrSelect,\s*percentSelect\)",
        ),
        "indicator",
    )
    require_patterns(
        break_contract,
        (
            r"DistanceMode\s*\{\s*get;\s*init;\s*\}\s*=\s*FractalZonesBreakDistanceMode\.OneMinuteAtr",
            r"AtrPeriodMinutes\s*\{\s*get;\s*init;\s*\}\s*=\s*60",
            r"BreakAtrMultiplier\s*\{\s*get;\s*init;\s*\}\s*=\s*0\.5",
            r"MinimumBreakDistanceTicks\s*\{\s*get;\s*init;\s*\}\s*=\s*2",
            r"BreakDistancePercent\s*\{\s*get;\s*init;\s*\}\s*=\s*0\.05",
            r"FixedBreakDistanceTicks\s*\{\s*get;\s*init;\s*\}\s*=\s*2",
            r"BreakConfirmationMinutes\s*\{\s*get;\s*init;\s*\}\s*=\s*5",
            r"MinimumMinutesBetweenBreaks\s*\{\s*get;\s*init;\s*\}\s*=\s*5",
        ),
        "break-setting",
    )
    require_patterns(
        lifecycle_contract,
        (
            r"ConfirmationMinutes\s*\{\s*get;\s*init;\s*\}\s*=\s*5",
            r"TerminateOnCurrentRoleBreakNumber\s*\{\s*get;\s*init;\s*\}\s*=\s*3",
        ),
        "lifecycle-setting",
    )

    validate_fzrui_contracts(indicator, host_tests)
    require_patterns(host_tests, (r"atrMultiplier\.DecimalPlaces\s*==\s*2", r"distancePercent\.DecimalPlaces\s*==\s*2"), "numeric display test")

    requirements = source_snapshot.get("requirements")
    traces = source_snapshot.get("goldenTraces")
    acceptances = source_snapshot.get("manualAcceptances")
    conformance = contract["conformance"]
    if not isinstance(conformance, dict):
        raise SourceContractError("documentation_drift", "source-contract conformance inventory is invalid")
    if requirements != expected_sequence("FZ", int(conformance["requirements_count"]), 3):
        raise SourceContractError("documentation_drift", "FZCP requirement sequence changed")
    if traces != expected_sequence("GT", int(conformance["golden_trace_count"]), 2):
        raise SourceContractError("documentation_drift", "FZCP golden-trace sequence changed")
    if acceptances != expected_sequence("MVA", int(conformance["manual_acceptance_count"]), 2):
        raise SourceContractError("documentation_drift", "FZCP manual-acceptance sequence changed")
    if composite_manifest.get("contractState") != "contractValidationAndBetaReadiness":
        raise SourceContractError("documentation_drift", "FZCP composite contract state changed")

    return {
        "status": "no_drift",
        "setting_rows": len(setting_ids),
        "product_actions": action_count,
        "line_option_rows": line_option_count,
        "maximum_atomic_controls": atomic_count,
        "requirements": len(requirements),
        "golden_traces": len(traces),
        "manual_acceptances": len(acceptances),
        "residuals": {
            "FZRUI-01": "runtime_confirmed_fixed",
            "FZRUI-02": "host_presentation_limitation_confirmed",
        },
        "sanitization": "passed",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check sanitized Fractal Zones documentation drift")
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--validate-contract-only", action="store_true")
    args = parser.parse_args(argv)
    try:
        contract = load_json(args.contract)
        manifest = load_json(args.manifest)
        validate_contract_coupling(contract, manifest)
        if args.validate_contract_only:
            result = {"status": "no_drift", "contract_only": True, "sanitization": "passed"}
        else:
            if args.source_root is None:
                raise SourceContractError("unsafe_or_ambiguous_source", "source root is required")
            result = verify_source(args.source_root.resolve(), contract, manifest)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError, SourceContractError) as exc:
        state = exc.state if isinstance(exc, SourceContractError) else "unsafe_or_ambiguous_source"
        print(json.dumps({"status": state, "message": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 2 if state == "documentation_drift" else 3
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
