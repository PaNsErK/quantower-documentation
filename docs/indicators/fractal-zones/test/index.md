# Teststrategie

Die Abnahme ist bewusst in drei Klassen getrennt:

| Klasse | Kennung | Aktueller Stand |
|---|---|---|
| automatisierte Konformität | FZ-001…102, GT-01…180, MVA-01…25 | vollständig und geschlossen |
| öffentliche Lern-/Regressionstests | FZMT-01…24 | lokal im Browser speicherbar |
| neue subjektive Benutzerprüfung | FZV2-RM-001…019 | `pending_user_evaluation` |

`runtime_acceptance_complete=true` beschreibt die technische Laufzeitabnahme. `manual_acceptance_complete=false` bleibt korrekt, bis die 19 neuen Benutzerfälle tatsächlich durchgeführt wurden. Keiner dieser Zustände wird aus dem anderen abgeleitet.

--8<-- "docs/includes/diagrams/runtime-vs-user-acceptance.md"

- [Regression und Lernen](manual-suite.md)
- [Technische Runtime-Abnahme](runtime-acceptance.md)
- [Offene Benutzer-Testmatrix](v2-remediation-user-matrix.md)
