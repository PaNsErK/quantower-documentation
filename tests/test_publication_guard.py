from __future__ import annotations

import importlib.util
import json
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
        self.assertEqual(56, len(manifest["settings"]))
        self.assertEqual(70, sum(item["atomic_controls"] for item in manifest["settings"]))
        self.assertEqual(7, sum(item["type"] == "line_options" for item in manifest["settings"]))
        self.assertEqual(2, sum(item["type"] == "action" for item in manifest["settings"]))

    def test_runtime_and_user_acceptance_are_not_conflated(self) -> None:
        manifest = validator.load_json(ROOT / "docs/data/public-indicator-manifest.json")
        self.assertTrue(manifest["publication"]["runtime_acceptance_complete"])
        self.assertFalse(manifest["publication"]["manual_acceptance_complete"])
        self.assertEqual("pending_user_evaluation", manifest["publication"]["user_evaluation"])

    def test_fzmt_and_user_suites_are_separate_and_contiguous(self) -> None:
        fzmt = validator.load_json(ROOT / "docs/includes/manual-test-catalog.json")
        user = validator.load_json(ROOT / "docs/includes/fractal-zones-v2-remediation-user-test-catalog.json")
        self.assertEqual([f"FZMT-{index:02d}" for index in range(1, 25)], [item["id"] for item in fzmt])
        self.assertEqual([f"FZV2-RM-{index:03d}" for index in range(1, 20)], [item["id"] for item in user])
        self.assertTrue(all("result" not in item and "note" not in item for item in user))

    def test_runtime_facts_are_closed(self) -> None:
        runtime = validator.load_json(ROOT / "docs/data/fractal-zones-runtime-acceptance.json")
        self.assertEqual(2700.009, runtime["soak"]["elapsed_seconds"])
        self.assertEqual(188, runtime["soak"]["responsive_samples"])
        self.assertEqual("accepted_persistence_quota_and_efficiency_risk", runtime["residual_warning"]["classification"])

    def test_valid_result_passes_and_wrong_namespace_fails(self) -> None:
        schema = validator.load_json(ROOT / "schemas/manual-test-result.schema.json")
        valid = validator.load_json(ROOT / "tests/fixtures/manual-result-v2-valid.json")
        invalid = validator.load_json(ROOT / "tests/fixtures/manual-result-v2-invalid-suite.json")
        self.assertFalse(list(validator.Draft202012Validator(schema).iter_errors(valid)))
        self.assertTrue(list(validator.Draft202012Validator(schema).iter_errors(invalid)))

    def test_manual_test_runtime_separates_suites_and_limits_legacy_migration(self) -> None:
        script = validator.read_utf8(ROOT / "docs/assets/javascripts/manual-tests.js")
        self.assertIn('"fzdocs.manual-test-state.v2." + suiteId', script)
        self.assertIn('suiteId === "FZMT"', script)
        self.assertIn('suiteId !== "FZMT" && suiteId !== "FZV2-RM"', script)
        self.assertIn('value.suite_id !== suiteId', script)

    def test_current_simulator_inventory_is_registered(self) -> None:
        script = validator.read_utf8(ROOT / "docs/assets/javascripts/fractal-zones-simulators.js")
        for simulator in ("break-boundary", "role-ended", "timeframe-parity", "lifecycle", "rendering-modes", "break-source", "history-range"):
            self.assertIn(f'"{simulator}"', script)

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
