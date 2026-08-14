#!/usr/bin/env python3
"""Run the bounded Fractal Zones documentation maintenance workflow.

The source checkout is read-only and its location is never included in output.
Only closed status, step identifiers, aggregate counts, and sanitization state
are emitted.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)


def run_closed(step: str, command: list[str]) -> tuple[bool, str]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return completed.returncode == 0, step


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the closed Fractal Zones documentation update gate")
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--skip-build", action="store_true", help="Run contract and unit checks without site builds")
    args = parser.parse_args(argv)

    drift_command = [
        str(PYTHON),
        "tools/check_fractal_zones_source_drift.py",
        "--source-root",
        str(args.source_root.resolve()),
    ]
    drift = subprocess.run(
        drift_command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    try:
        drift_result = json.loads(drift.stdout.strip())
    except json.JSONDecodeError:
        drift_result = {"status": "unsafe_or_ambiguous_source", "sanitization": "failed"}
    drift_state = drift_result.get("status")
    if drift.returncode != 0 or drift_state != "no_drift":
        public_state = drift_state if drift_state in {"documentation_drift", "unsafe_or_ambiguous_source"} else "unsafe_or_ambiguous_source"
        print(json.dumps({"status": public_state, "failed_step": "source_drift", "sanitization": "passed"}, sort_keys=True))
        return 2

    steps: list[tuple[str, list[str]]] = [
        ("publication_guard", [str(PYTHON), "tools/validate_public_docs.py", "source"]),
        ("unit_tests", [str(PYTHON), "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"]),
    ]
    if not args.skip_build:
        steps.extend(
            [
                ("online_build", [str(PYTHON), "-m", "mkdocs", "build", "--strict"]),
                ("offline_build", [str(PYTHON), "-m", "mkdocs", "build", "--strict", "-f", "mkdocs.offline.yml"]),
                ("generated_site", [str(PYTHON), "tools/validate_public_docs.py", "generated"]),
            ]
        )
    for step, command in steps:
        passed, _ = run_closed(step, command)
        if not passed:
            print(json.dumps({"status": "documentation_drift", "failed_step": step, "sanitization": "passed"}, sort_keys=True))
            return 2

    residual_states = drift_result.get("residuals", {})
    expected_residual_states = {
        "FZRUI-01": "runtime_confirmed_fixed",
        "FZRUI-02": "host_presentation_limitation_confirmed",
    }
    if residual_states != expected_residual_states:
        print(json.dumps({"status": "documentation_drift", "failed_step": "runtime_findings", "sanitization": "passed"}, sort_keys=True))
        return 2
    status = "no_drift"
    print(
        json.dumps(
            {
                "status": status,
                "source_contract": "no_drift",
                "setting_rows": drift_result.get("setting_rows"),
                "line_option_rows": drift_result.get("line_option_rows"),
                "maximum_atomic_controls": drift_result.get("maximum_atomic_controls"),
                "sanitization": "passed",
                "manual_acceptance_complete": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
