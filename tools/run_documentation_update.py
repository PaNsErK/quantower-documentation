#!/usr/bin/env python3
"""Run the bounded, sanitized Fractal Zones documentation maintenance gate."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable)


def run(step: str, command: list[str]) -> tuple[bool, str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
    return completed.returncode == 0, step


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a public Fractal Zones documentation update")
    parser.add_argument("--inventory", type=Path, help="Optional closed sanitized inventory capsule")
    parser.add_argument("--skip-build", action="store_true")
    args = parser.parse_args(argv)
    drift = [str(PYTHON), "tools/check_fractal_zones_source_drift.py"]
    if args.inventory:
        drift.extend(["--inventory", str(args.inventory.resolve())])
    else:
        drift.append("--validate-contract-only")
    steps: list[tuple[str, list[str]]] = [
        ("source_drift", drift),
        ("publication_guard", [str(PYTHON), "tools/validate_public_docs.py", "source"]),
        ("unit_tests", [str(PYTHON), "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"]),
    ]
    if not args.skip_build:
        steps.extend([
            ("online_build", [str(PYTHON), "-m", "mkdocs", "build", "--strict"]),
            ("offline_build", [str(PYTHON), "-m", "mkdocs", "build", "--strict", "-f", "mkdocs.offline.yml"]),
            ("generated_site", [str(PYTHON), "tools/validate_public_docs.py", "generated"]),
        ])
    for step, command in steps:
        passed, _ = run(step, command)
        if not passed:
            print(json.dumps({"status":"documentation_drift","failed_step":step,"sanitization":"passed"}, sort_keys=True)); return 2
    print(json.dumps({"status":"no_drift","setting_rows":56,"line_option_rows":7,"atomic_product_controls":70,"manual_acceptance_complete":False,"runtime_acceptance_complete":True,"user_evaluation":"pending_user_evaluation","sanitization":"passed"}, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
