from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "tools/validate_public_docs.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class PublicationGuardTests(unittest.TestCase):
    def test_manifest_and_coverage_pass(self) -> None:
        validator.validate_manifest_and_coverage(ROOT)

    def test_current_inventory_is_exact(self) -> None:
        manifest = validator.load_json(ROOT / "docs/data/public-indicator-manifest.json")
        ids = {item["id"] for item in manifest["settings"]}
        self.assertEqual(56, len(manifest["settings"]))
        self.assertEqual(70, sum(item["atomic_controls"] for item in manifest["settings"]))
        self.assertEqual(7, sum(item["type"] == "line_options" for item in manifest["settings"]))
        self.assertEqual(2, sum(item["type"] == "action" for item in manifest["settings"]))
        self.assertTrue({"DynamicActiveLevelRangePercent", "DynamicHistoryHorizonMode", "DynamicHistoryBoundedDays"} <= ids)
        self.assertFalse({"ShowStatusOverlay", "EnablePriceRelevanceFilter", "PriceRelevancePercent"} & ids)

    def test_historical_and_current_runtime_states_are_not_conflated(self) -> None:
        manifest = validator.load_json(ROOT / "docs/data/public-indicator-manifest.json")
        self.assertFalse(manifest["publication"]["runtime_acceptance_complete"])
        self.assertFalse(manifest["publication"]["manual_acceptance_complete"])
        self.assertEqual("sourceValidatedRuntimePending", manifest["conformance"]["current_source_suites"][0]["runtime_state"])

    def test_three_test_suites_are_separate_and_contiguous(self) -> None:
        fzmt = validator.load_json(ROOT / "docs/includes/manual-test-catalog.json")
        historical = validator.load_json(ROOT / "docs/includes/fractal-zones-v2-remediation-user-test-catalog.json")
        current = validator.load_json(ROOT / "docs/includes/fractal-zones-current-user-test-catalog.json")
        self.assertEqual([f"FZMT-{index:02d}" for index in range(1, 25)], [item["id"] for item in fzmt])
        self.assertEqual([f"FZV2-RM-{index:03d}" for index in range(1, 20)], [item["id"] for item in historical])
        self.assertEqual([f"FZCURRENT-{index:03d}" for index in range(1, 13)], [item["id"] for item in current])
        self.assertTrue(all("result" not in item and "note" not in item for item in historical + current))

    def test_historical_runtime_facts_are_retained(self) -> None:
        runtime = validator.load_json(ROOT / "docs/data/fractal-zones-runtime-acceptance.json")
        historical = runtime["historical_v1_to_v4"]
        self.assertEqual(2700.009, historical["soak"]["elapsed_seconds"])
        self.assertEqual(188, historical["soak"]["responsive_samples"])
        self.assertEqual("accepted_persistence_quota_and_efficiency_risk", historical["residual_warning"]["classification"])
        self.assertEqual(["FZCP-v5", "FZCP-v6"], [item["suite_id"] for item in runtime["current_v5_v6"]])

    def test_v3_result_passes_and_wrong_namespace_fails(self) -> None:
        schema = validator.load_json(ROOT / "schemas/manual-test-result.schema.json")
        valid = validator.load_json(ROOT / "tests/fixtures/manual-result-current-valid.json")
        invalid = validator.load_json(ROOT / "tests/fixtures/manual-result-current-invalid-suite.json")
        self.assertFalse(list(validator.Draft202012Validator(schema).iter_errors(valid)))
        self.assertTrue(list(validator.Draft202012Validator(schema).iter_errors(invalid)))

    def test_manual_test_runtime_uses_v3_and_preserves_local_migration(self) -> None:
        script = validator.read_utf8(ROOT / "docs/assets/javascripts/manual-tests.js")
        self.assertIn('"fzdocs.manual-test-state.v3." + suiteId', script)
        self.assertIn('"fzdocs.manual-test-state.v2." + suiteId', script)
        self.assertIn('suiteId !== "FZMT" && suiteId !== "FZV2-RM" && suiteId !== "FZCURRENT"', script)
        self.assertIn('"fz-manual-test-result-v3"', script)

    def test_current_simulator_inventory_is_registered(self) -> None:
        script = validator.read_utf8(ROOT / "docs/assets/javascripts/fractal-zones-simulators.js")
        for simulator in ("break-boundary", "role-ended", "timeframe-parity", "lifecycle", "rendering-modes", "break-source", "history-range", "dynamic-history", "multiblock-history"):
            self.assertIn(f'"{simulator}"', script)

    def test_product_title_and_version_axes_are_unambiguous(self) -> None:
        overview = validator.read_utf8(ROOT / "docs/indicators/fractal-zones/index.md")
        current_state = validator.read_utf8(ROOT / "docs/indicators/fractal-zones/current-state.md")
        self.assertEqual("# Fractal Zones", overview.splitlines()[0])
        self.assertNotIn("# Fractal Zones v2", overview)
        for expected in (
            "Sichtbarer Produktname",
            "Interne Produktgeneration",
            "Öffentlicher Dokumentationsvertrag",
            "Aktuellster FZCP Source Contract",
            "Öffentliche Buildversion",
        ):
            self.assertIn(expected, current_state)

    def test_statusbar_excludes_heading_permalink_text(self) -> None:
        script = validator.read_utf8(ROOT / "docs/assets/javascripts/fractal-zones.js")
        self.assertIn("function headingLabel(heading)", script)
        self.assertIn('copy.querySelectorAll(".headerlink")', script)
        self.assertIn("permalink.remove();", script)
        self.assertIn("page.textContent = headingLabel(heading);", script)
        self.assertNotIn("page.textContent = heading.textContent", script)

    def test_source_tree_rejects_private_or_network_content(self) -> None:
        with self.assertRaises(validator.ValidationError):
            validator.assert_safe_text("C:" + "/Users/Example/private.txt", "fixture")
        self.assertIsNotNone(validator.NETWORK_PATTERNS["fetch"].search("fetch('/collect')"))

    def test_generated_link_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); source = root / "guide" / "index.html"; source.parent.mkdir(); source.write_text("safe", encoding="utf-8")
            with self.assertRaises(validator.ValidationError):
                validator.validate_generated_internal_link(root, source, "../../missing/")

    def test_workflow_remains_least_privilege_and_pinned(self) -> None:
        validator.validate_workflow(ROOT)


if __name__ == "__main__":
    unittest.main()
