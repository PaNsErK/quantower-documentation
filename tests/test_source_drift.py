from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_fractal_zones_source_drift",
    ROOT / "tools/check_fractal_zones_source_drift.py",
)
drift = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(drift)


class FractalZonesSourceDriftTests(unittest.TestCase):
    def load_contract(self) -> dict[str, object]:
        return json.loads((ROOT / "docs/data/fractal-zones-source-contract.json").read_text(encoding="utf-8"))

    def load_manifest(self) -> dict[str, object]:
        return json.loads((ROOT / "docs/data/public-indicator-manifest.json").read_text(encoding="utf-8"))

    def test_sanitized_contract_is_self_consistent(self) -> None:
        contract = self.load_contract()
        manifest = self.load_manifest()
        drift.validate_contract_coupling(contract, manifest)

    def test_setting_fact_digest_detects_documentation_drift(self) -> None:
        manifest = self.load_manifest()
        original = drift.compute_setting_fact_digest(manifest)
        settings = manifest["settings"]
        assert isinstance(settings, list)
        settings[0]["default"] = 31
        self.assertNotEqual(original, drift.compute_setting_fact_digest(manifest))

    def test_contract_digest_is_domain_separated_and_stable(self) -> None:
        contract = self.load_contract()
        digest = drift.compute_contract_digest(contract)
        self.assertEqual(contract["contract_digest"], digest)
        self.assertEqual(64, len(digest))

    def test_missing_source_is_closed_without_path_disclosure(self) -> None:
        contract = self.load_contract()
        manifest = self.load_manifest()
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(drift.SourceContractError) as caught:
                drift.verify_source(Path(temporary), contract, manifest)
        self.assertEqual("unsafe_or_ambiguous_source", caught.exception.state)
        self.assertNotIn(temporary, str(caught.exception))

    def test_string_symbol_resolution_closes_split_setting_names(self) -> None:
        source = 'private static readonly string Name = "Re" + "testConfirmationMinutes";'
        self.assertEqual("RetestConfirmationMinutes", drift.resolve_string_symbols(source)["Name"])

    def test_terminal_fzrui_source_contracts_are_required(self) -> None:
        indicator = '''
            new SettingItemDouble("InactiveStateOpacity", 0.35, 660) {
                Minimum = 0.10, Maximum = 1.00, Increment = 0.05, DecimalPlaces = 2
            });
            new SettingItemDateTime("CalculationStartTime", value, 830) {
                UseEnabilityToggler = true, Enabled = calculationStartTimeUtc.HasValue
            });
        '''
        host_tests = '''
            ActiveFocusOpacityUsesTwoDecimalHostMetadata();
            opacity.Value - 0.35; opacity.Increment - 0.05; opacity.DecimalPlaces == 2;
            CalculationStartTime setting.UseEnabilityToggler;
            ExplicitCalculationStartRemainsUtcStable();
            ClearingCalculationStartReturnsToInitialRangeMode();
        '''
        drift.validate_fzrui_contracts(indicator, host_tests)
        with self.assertRaises(drift.SourceContractError):
            drift.validate_fzrui_contracts(indicator.replace("DecimalPlaces = 2", ""), host_tests)


if __name__ == "__main__":
    unittest.main()
