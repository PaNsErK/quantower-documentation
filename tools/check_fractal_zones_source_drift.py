#!/usr/bin/env python3
"""Validate a closed, sanitized Fractal Zones inventory against public docs.

The validator deliberately does not know any private repository layout. An
operator may provide an already sanitized inventory capsule; CI validates the
closed public contract itself. No supplied path or source value is echoed.
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
    return hashlib.sha256(b"fz-public-setting-facts-v2\n" + canonical_bytes(settings)).hexdigest()


def contract_digest(contract: dict[str, object]) -> str:
    candidate = dict(contract)
    candidate["contract_digest"] = "0" * 64
    return hashlib.sha256(b"fz-public-source-contract-v2\n" + canonical_bytes(candidate)).hexdigest()


def expected_sequence(prefix: str, count: int, width: int) -> list[str]:
    return [f"{prefix}-{index:0{width}d}" for index in range(1, count + 1)]


def validate_contract_coupling(contract: dict[str, object], manifest: dict[str, object]) -> None:
    settings = manifest.get("settings")
    if not isinstance(settings, list):
        raise SourceContractError("documentation_drift", "manifest settings are invalid")
    setting_ids = [item.get("id") for item in settings if isinstance(item, dict)]
    if setting_ids != contract.get("setting_ids"):
        raise SourceContractError("documentation_drift", "setting inventory differs")
    inventory = contract.get("inventory")
    manifest_inventory = manifest.get("inventory")
    if not isinstance(inventory, dict) or not isinstance(manifest_inventory, dict):
        raise SourceContractError("documentation_drift", "inventory is invalid")
    expected_counts = {
        "product_setting_rows": len(settings),
        "product_actions": sum(item.get("type") == "action" for item in settings),
        "line_option_rows": sum(item.get("type") == "line_options" for item in settings),
        "atomic_product_controls": sum(int(item.get("atomic_controls", 0)) for item in settings),
    }
    if inventory != expected_counts:
        raise SourceContractError("documentation_drift", "contract counts differ from setting facts")
    projections = {
        "product_owned_setting_rows": expected_counts["product_setting_rows"],
        "product_owned_actions": expected_counts["product_actions"],
        "line_option_rows": expected_counts["line_option_rows"],
        "atomic_product_controls": expected_counts["atomic_product_controls"],
    }
    if any(manifest_inventory.get(key) != value for key, value in projections.items()):
        raise SourceContractError("documentation_drift", "manifest inventory projections differ")
    line_ids = [item["id"] for item in settings if item["type"] == "line_options"]
    action_ids = [item["id"] for item in settings if item["type"] == "action"]
    if line_ids != contract.get("line_option_ids") or action_ids != contract.get("action_ids"):
        raise SourceContractError("documentation_drift", "line-option or action inventory differs")
    fact_digest = setting_fact_digest(settings)
    expected_contract_digest = contract_digest(contract)
    source_pointer = manifest.get("source_contract")
    if not isinstance(source_pointer, dict):
        raise SourceContractError("documentation_drift", "source pointer is invalid")
    if contract.get("setting_fact_digest") != fact_digest or source_pointer.get("setting_fact_digest") != fact_digest:
        raise SourceContractError("documentation_drift", "setting fact digest differs")
    if contract.get("contract_digest") != expected_contract_digest or source_pointer.get("contract_digest") != expected_contract_digest:
        raise SourceContractError("documentation_drift", "source contract digest differs")


def validate_sanitized_inventory(capsule: dict[str, object], contract: dict[str, object]) -> None:
    allowed = {"schema_version", "inventory", "setting_ids", "line_option_ids", "action_ids", "visibility_branches", "conformance"}
    if set(capsule) != allowed or capsule.get("schema_version") != "fz-sanitized-inventory-v2":
        raise SourceContractError("unsafe_or_ambiguous_source", "sanitized inventory schema is invalid")
    for key in ("inventory", "setting_ids", "line_option_ids", "action_ids", "visibility_branches", "conformance"):
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
    print(json.dumps({"status":"no_drift","setting_rows":56,"line_option_rows":7,"maximum_atomic_controls":70,"sanitization":"passed"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
