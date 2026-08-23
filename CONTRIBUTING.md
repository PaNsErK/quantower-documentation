# Contributing

Dieses Repository dokumentiert Fractal Zones als inoffizielle öffentliche Beta. Beiträge müssen ausschließlich veröffentlichbare Dokumentationsinhalte enthalten.

## Grundregeln

- Verwende Deutsch für Nutzerinhalte und Englisch für Code, Tests, Commit- und PR-Texte.
- Übernimm keine privaten Pfade, Quelltexte, Repository-Metadaten, Commits, Roh-Hashes, Logs oder sensible Runtime-Daten.
- Ändere `manual_acceptance_complete` nur nach der tatsächlichen Bewertung aller 19 FZV2-RM-Fälle.
- Vermische FZMT-Regression, technische Runtime-Abnahme und FZV2-RM-Benutzerabnahme nicht.
- Bewahre 56 Produktzeilen, sieben LineOptions, 70 atomare Controls und zwei Actions, bis ein neuer geschlossener Contract sie ersetzt.
- Produktkorrekturen gehören nicht in dieses Repository.
- Halte Links, Beispiele und Lernpfade mit dem geschlossenen Public Manifest konsistent.

## Validierung

Führe vor einem Pull Request den in [docs/maintenance/documentation-workflow.md](docs/maintenance/documentation-workflow.md) beschriebenen Workflow aus. Änderungen werden nur integriert, wenn Schema-, Drift-, Unit-, Privacy-, Simulator-, Import/Export-, Strict-Build-, Link-, Accessibility- und Generated-Site-Prüfungen grün sind.

## Pull Requests

Beschreibe Zweck, Änderungen, Auswirkungen und Risiken/Checks. Verwende keine Issue-Closing-Keywords. Der PR muss klein genug bleiben, dass öffentliche Fakten und redaktionelle Änderungen nachvollziehbar geprüft werden können.
