from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_public_docs", ROOT / "tools/validate_public_docs.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class PublicationGuardTests(unittest.TestCase):
    def test_manifest_and_closed_counts_pass(self) -> None:
        validator.validate_manifest_and_coverage(ROOT)

    def test_runtime_inventory_is_closed_and_counted(self) -> None:
        manifest = validator.load_json(ROOT / "docs/data/public-indicator-manifest.json")
        self.assertEqual("runtime_inventory_confirmed", manifest["inventory"]["base_settings_union"])
        self.assertEqual(11, len(manifest["base_settings"]))
        self.assertEqual(25, sum(item["atomic_controls"] for item in manifest["base_settings"]))
        self.assertEqual(40, manifest["inventory"]["maximum_total_setting_rows"])
        self.assertEqual(66, manifest["inventory"]["maximum_total_atomic_controls"])
        self.assertEqual(["FZRUI-01", "FZRUI-02"], [item["id"] for item in manifest["runtime_inventory"]["residuals"]])

    def test_public_beta_status_is_closed_and_manual_acceptance_is_pending(self) -> None:
        manifest = validator.load_json(ROOT / "docs/data/public-indicator-manifest.json")
        self.assertEqual("public_beta_manual_acceptance_pending", manifest["publication"]["status"])
        self.assertFalse(manifest["publication"]["manual_acceptance_complete"])
        self.assertFalse(manifest["publication"]["official_affiliation"])
        self.assertEqual("no_open_source_license", manifest["publication"]["content_license_state"])

    def test_public_beta_and_unofficial_notices_are_visible(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        index = (ROOT / "docs/index.md").read_text(encoding="utf-8")
        indicator = (ROOT / "docs/indicators/fractal-zones/index.md").read_text(encoding="utf-8")
        self.assertIn("public_beta_manual_acceptance_pending", readme)
        self.assertIn("manual_acceptance_complete=false", readme + index)
        self.assertIn("inoffiziell", (readme + index + indicator).lower())

    def test_runtime_pending_state_is_absent_from_public_contracts(self) -> None:
        checked = [
            ROOT / "docs/data/public-indicator-manifest.json",
            ROOT / "schemas/manual-test-result.schema.json",
            ROOT / "tests/fixtures/manual-result-valid.json",
            ROOT / "docs/assets/javascripts/manual-tests.js",
        ]
        for path in checked:
            self.assertNotIn("runtime_inventory_pending", path.read_text(encoding="utf-8"), path)

    def test_topics_use_markdown_in_html_contract(self) -> None:
        docs_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "docs/indicators/fractal-zones").rglob("*.md")
        )
        self.assertNotIn('<section class="fz-topic"', docs_text)
        self.assertNotIn('<div class="fz-depth"', docs_text)

    def test_workflow_is_least_privilege_and_sha_pinned(self) -> None:
        validator.validate_workflow(ROOT)

    def test_valid_manual_result_passes_schema(self) -> None:
        validator.validate_manual_result_fixture(ROOT)

    def test_invalid_manual_result_fixture_is_rejected(self) -> None:
        schema = validator.load_json(ROOT / "schemas/manual-test-result.schema.json")
        instance = validator.load_json(ROOT / "tests/fixtures/manual-result-invalid-extra-field.json")
        errors = list(validator.Draft202012Validator(schema).iter_errors(instance))
        self.assertTrue(errors)

    def test_manual_result_rejects_unknown_field(self) -> None:
        schema = validator.load_json(ROOT / "schemas/manual-test-result.schema.json")
        instance = validator.load_json(ROOT / "tests/fixtures/manual-result-valid.json")
        instance["private_path"] = "forbidden"
        errors = list(validator.Draft202012Validator(schema).iter_errors(instance))
        self.assertTrue(errors)

    def test_absolute_windows_path_is_rejected(self) -> None:
        with self.assertRaises(validator.ValidationError):
            validator.assert_safe_text("C:" + "/Users/Example/private.txt", "fixture")

    def test_secret_assignment_is_rejected(self) -> None:
        with self.assertRaises(validator.ValidationError):
            validator.assert_safe_text("api_" + "key=" + "abcdefghijklmnop", "fixture")

    def test_custom_network_primitive_is_rejected(self) -> None:
        pattern = validator.CUSTOM_JS_NETWORK_PATTERNS["fetch"]
        self.assertIsNotNone(pattern.search("fetch('/collect')"))

    def test_unsafe_svg_is_rejected(self) -> None:
        with self.assertRaises(validator.ValidationError):
            payload = "<svg><scr" + "ipt>alert(1)</scr" + "ipt></svg>"
            validator.validate_svg_text(payload, "fixture")

    def test_external_runtime_asset_is_rejected(self) -> None:
        parser = validator.ResourceHTMLParser()
        parser.feed('<scr' + 'ipt src="http' + 's://example.invalid/app.js"></scr' + 'ipt>')
        self.assertEqual(1, len(parser.external_resources))

    def test_generated_root_cannot_escape_repository(self) -> None:
        with self.assertRaises(validator.ValidationError):
            validator.resolve_safe_root("..", "fixture")

    def test_broken_generated_internal_link_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "guide" / "index.html"
            source.parent.mkdir()
            source.write_text("safe", encoding="utf-8")
            with self.assertRaises(validator.ValidationError):
                validator.validate_generated_internal_link(root, source, "../missing/")

    def test_duplicate_test_ids_are_not_accepted_by_import_contract(self) -> None:
        fixture = json.loads((ROOT / "tests/fixtures/manual-result-valid.json").read_text(encoding="utf-8"))
        fixture["results"].append(dict(fixture["results"][0]))
        ids = [item["test_id"] for item in fixture["results"]]
        self.assertNotEqual(len(ids), len(set(ids)))

    def test_source_tree_rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "target.md").write_text("safe", encoding="utf-8")
            link = root / "link.md"
            try:
                link.symlink_to(root / "target.md")
            except OSError:
                self.skipTest("symlink creation is unavailable")
            with self.assertRaises(validator.ValidationError):
                validator.relative_files(root)


if __name__ == "__main__":
    unittest.main()
