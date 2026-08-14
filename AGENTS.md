# Documentation repository policy

This repository contains public, static documentation only.

- Keep every page useful without access to a private source repository.
- Never add private repository metadata, local installation paths, logs, screenshots, account data, credentials, secrets, process identifiers, window handles, or trading records.
- Treat `docs/data/public-indicator-manifest.json` as the closed public content contract.
- Any setting, test, schema, JavaScript, workflow, or publishing change must pass `python tools/validate_public_docs.py all` and `python -m unittest discover -s tests -p "test_*.py" -v`.
- Do not add analytics, telemetry, remote fonts, CDNs, external scripts, network APIs, or cross-repository checkout logic.
- Keep the manual-test application local-only. Exported notes are opt-in and must pass the sanitizer.
- Do not claim that the Quantower UI inventory is complete while `indicator_version` or `base_settings_union` is `runtime_inventory_pending`.
- Use German for public user documentation and English for code, identifiers, tests, commits, and workflows.
- Normal editorial changes use lightweight review: focused validation, strict builds, and a local browser check. No project-wide governance files are required here.
