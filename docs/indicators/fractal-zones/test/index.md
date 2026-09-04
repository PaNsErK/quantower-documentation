# Teststrategie

Die Abnahme ist in klar getrennte Evidenzklassen geschnitten:

| Klasse | Kennung | Aktueller Stand |
|---|---|---|
| historische technische Laufzeit | FZCP v1–v4, FZ-001..102, GT-01..180 | historische Evidenz erhalten |
| aktueller Source Contract | FZCP-v5 und FZCP-v6 | `sourceValidatedRuntimePending` |
| öffentliche Lern-/Regressionstests | FZMT-01..24 | lokal im Browser speicherbar |
| historische Benutzerremediation | FZV2-RM-001..019 | `pending_user_evaluation` |
| aktuelle Benutzerprüfung | FZCURRENT-001..012 | source-validiert, Runtime ausstehend |

`runtime_acceptance_complete=false` verhindert eine vorgezogene V5/V6-Abnahme. `manual_acceptance_complete=false` bleibt korrekt, bis die zugehörigen Benutzerfälle tatsächlich durchgeführt wurden. MVA-Kennungen sind immer suitespezifisch.

--8<-- "docs/includes/diagrams/runtime-vs-user-acceptance.md"

- [Regression und Lernen](manual-suite.md)
- [Historische Runtime-Evidenz](runtime-acceptance.md)
- [Historische Benutzer-Testmatrix](v2-remediation-user-matrix.md)
- [Aktuelle V5/V6-Testmatrix](current-user-matrix.md)
