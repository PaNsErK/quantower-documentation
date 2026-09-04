#!/usr/bin/env python3
"""Fail-closed coupling guard for the public Fractal Zones V3 contract.

The guard deliberately consumes only a closed, sanitized capsule. It never
opens a product checkout and never serializes source locations, source text,
runtime identifiers, logs, or hashes into the public documentation tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs/data/fractal-zones-source-contract.json"
MANIFEST_PATH = ROOT / "docs/data/public-indicator-manifest.json"


class SourceContractError(RuntimeError):
    def __init__(self, state: str, message: str) -> None:
        super().__init__(message)
        self.state = state


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def setting_fact_digest(settings: list[dict[str, object]]) -> str:
    return hashlib.sha256(b"fz-public-setting-facts-v3\n" + canonical_bytes(settings)).hexdigest()


def contract_digest(contract: dict[str, object]) -> str:
    candidate = dict(contract)
    candidate["contract_digest"] = "0" * 64
    return hashlib.sha256(b"fz-public-source-contract-v3\n" + canonical_bytes(candidate)).hexdigest()


def expected_counts(settings: list[dict[str, object]]) -> dict[str, int]:
    return {
        "product_setting_rows": len(settings),
        "product_actions": sum(item.get("type") == "action" for item in settings),
        "line_option_rows": sum(item.get("type") == "line_options" for item in settings),
        "atomic_product_controls": sum(int(item.get("atomic_controls", 0)) for item in settings),
    }


def _require(value: bool, message: str) -> None:
    if not value:
        raise SourceContractError("documentation_drift", message)


def validate_contract_coupling(contract: dict[str, object], manifest: dict[str, object]) -> None:
    settings = manifest.get("settings")
    if not isinstance(settings, list) or not all(isinstance(item, dict) for item in settings):
        raise SourceContractError("documentation_drift", "manifest settings are invalid")
    _require(manifest.get("schema_version") == "fz-public-manifest-v3", "manifest schema differs")
    _require(contract.get("schema_version") == "fz-public-source-contract-v3", "source contract schema differs")
    _require(contract.get("source_state") == "current_source_validated_v5_v6_runtime_pending", "source state differs")
    _require(manifest.get("publication", {}).get("runtime_acceptance_complete") is False, "current runtime status is overstated")

    ids = [item.get("id") for item in settings]
    _require(ids == contract.get("setting_ids"), "setting inventory differs")
    _require(contract.get("setting_facts") == settings, "setting facts differ")
    counts = expected_counts(settings)
    _require(contract.get("inventory") == counts, "contract counts differ from setting facts")
    projections = {
        "product_owned_setting_rows": counts["product_setting_rows"],
        "product_owned_actions": counts["product_actions"],
        "line_option_rows": counts["line_option_rows"],
        "atomic_product_controls": counts["atomic_product_controls"],
    }
    manifest_inventory = manifest.get("inventory")
    _require(isinstance(manifest_inventory, dict), "manifest inventory is invalid")
    _require(all(manifest_inventory.get(key) == value for key, value in projections.items()), "manifest inventory projections differ")
    line_ids = [item["id"] for item in settings if item["type"] == "line_options"]
    action_ids = [item["id"] for item in settings if item["type"] == "action"]
    _require(line_ids == contract.get("line_option_ids"), "line option inventory differs")
    _require(action_ids == contract.get("action_ids"), "action inventory differs")

    source_pointer = manifest.get("source_contract")
    _require(isinstance(source_pointer, dict), "source pointer is invalid")
    fact = setting_fact_digest(settings)
    digest = contract_digest(contract)
    _require(contract.get("setting_fact_digest") == fact and source_pointer.get("setting_fact_digest") == fact, "setting fact digest differs")
    _require(contract.get("contract_digest") == digest and source_pointer.get("contract_digest") == digest, "source contract digest differs")
    _require(source_pointer.get("schema_version") == "fz-public-source-contract-v3", "source pointer schema differs")

    conformance = contract.get("conformance")
    _require(isinstance(conformance, dict), "conformance is invalid")
    historical = conformance.get("historical_v1_to_v4")
    current = conformance.get("current_source_suites")
    _require(isinstance(historical, dict) and historical.get("requirements", {}).get("count") == 102, "historical conformance differs")
    _require(isinstance(current, list) and [item.get("suite_id") for item in current if isinstance(item, dict)] == ["FZCP-v5", "FZCP-v6"], "current conformance suites differ")
    _require(all(item.get("runtime_state") == "sourceValidatedRuntimePending" for item in current if isinstance(item, dict)), "current runtime state differs")


def validate_sanitized_inventory(capsule: dict[str, object], contract: dict[str, object]) -> None:
    allowed = {
        "schema_version", "inventory", "setting_ids", "setting_facts", "line_option_ids", "action_ids",
        "visibility_branches", "conformance", "runtime_evidence", "sanitization",
    }
    if set(capsule) != allowed or capsule.get("schema_version") != "fz-sanitized-inventory-v3":
        raise SourceContractError("unsafe_or_ambiguous_source", "sanitized inventory schema is invalid")
    for key in ("inventory", "setting_ids", "setting_facts", "line_option_ids", "action_ids", "visibility_branches", "conformance", "runtime_evidence", "sanitization"):
        if capsule.get(key) != contract.get(key):
            raise SourceContractError("documentation_drift", f"sanitized inventory differs at {key}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate sanitized Fractal Zones documentation drift")
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--validate-contract-only", action="store_true")
    parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args(argv)
    try:
        contract = load_json(args.contract)
        manifest = load_json(args.manifest)
        if not isinstance(contract, dict) or not isinstance(manifest, dict):
            raise SourceContractError("documentation_drift", "public contract is invalid")
        validate_contract_coupling(contract, manifest)
        if args.inventory:
            capsule = load_json(args.inventory)
            if not isinstance(capsule, dict):
                raise SourceContractError("unsafe_or_ambiguous_source", "sanitized inventory is invalid")
            validate_sanitized_inventory(capsule, contract)
        elif not args.validate_contract_only:
            raise SourceContractError("unsafe_or_ambiguous_source", "provide a sanitized inventory or use contract-only validation")
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError, SourceContractError) as exc:
        state = exc.state if isinstance(exc, SourceContractError) else "unsafe_or_ambiguous_source"
        print(json.dumps({"status": state, "sanitization": "passed"}, sort_keys=True))
        return 2 if state == "documentation_drift" else 3
    settings = manifest["settings"]
    print(json.dumps({"status":"no_drift","setting_rows":len(settings),"line_option_rows":sum(item["type"] == "line_options" for item in settings),"maximum_atomic_controls":sum(item["atomic_controls"] for item in settings),"sanitization":"passed"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
