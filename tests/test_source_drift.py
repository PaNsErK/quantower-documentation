from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("drift", ROOT / "tools/check_fractal_zones_source_drift.py")
drift = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(drift)


class SourceDriftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = drift.load_json(ROOT / "docs/data/fractal-zones-source-contract.json")
        self.manifest = drift.load_json(ROOT / "docs/data/public-indicator-manifest.json")

    def test_contract_coupling_passes(self) -> None:
        drift.validate_contract_coupling(self.contract, self.manifest)

    def test_setting_drift_fails(self) -> None:
        changed = dict(self.manifest)
        changed["settings"] = list(self.manifest["settings"][:-1])
        with self.assertRaises(drift.SourceContractError):
            drift.validate_contract_coupling(self.contract, changed)

    def test_sanitized_capsule_is_closed(self) -> None:
        capsule = {"schema_version":"fz-sanitized-inventory-v2"}
        for key in ("inventory","setting_ids","line_option_ids","action_ids","visibility_branches","conformance"):
            capsule[key] = self.contract[key]
        drift.validate_sanitized_inventory(capsule, self.contract)
        capsule["private_path"] = "forbidden"
        with self.assertRaises(drift.SourceContractError):
            drift.validate_sanitized_inventory(capsule, self.contract)


if __name__ == "__main__":
    unittest.main()
