# Dokumentation pflegen

Dieser Workflow hält die öffentliche Fractal-Zones-Dokumentation aktuell, ohne private Quellinhalte in das öffentliche Repository zu übernehmen. Er ist bewusst leichter als eine Produktentwicklung: ein kleiner Branch, ein geschlossener Drift-Check, zielgerichtete redaktionelle Änderungen und ein normaler Pull Request.

## Wann ist eine Aktualisierung nötig?

- Ein Setting, Default, Bereich, Sichtbarkeitszweig oder LineOptions-Control ändert sich.
- FZCP-Anforderungen, Golden Traces oder manuelle Akzeptanzen ändern sich.
- Ein Runtime-Residual wird bestätigt, repariert oder neu klassifiziert.
- Lernpfade, Beispiele oder Troubleshooting müssen an Produktverhalten angepasst werden.

## Lokaler Ablauf

1. Verwende einen berechtigten lokalen Checkout der Produktquelle ausschließlich read-only.
2. Erzeuge außerhalb des öffentlichen Repositorys eine geschlossene, sanitisiert geprüfte Inventarkapsel oder validiere den bereits gebundenen Public Contract.
3. Bei `documentation_drift` passe zuerst das geschlossene Manifest, den Source Contract und die betroffenen Seiten konsistent an.
4. Führe den Runner erneut aus. Erst danach darf ein Dokumentations-PR entstehen.
5. Halte technische Runtime-Abnahme, FZMT-Regression und FZV2-RM-Benutzerabnahme als drei getrennte Zustände. Der manuelle Status ändert sich erst nach tatsächlicher Benutzerprüfung.

Der Runner gibt ausschließlich geschlossene Zustände aus:

| Status | Bedeutung | Nächste Aktion |
|---|---|---|
| `no_drift` | Vertrag und Dokumentation stimmen überein | normaler Review |
| `documentation_drift` | öffentliche Fakten oder Validierung weichen ab | Dokumentation gezielt aktualisieren |
| `unsafe_or_ambiguous_source` | Quelle fehlt, ist mehrdeutig oder nicht sicher auswertbar | sicher stoppen und Quelle klären |

## Veröffentlichungsgrenze

Erlaubt sind aggregierte Produktfakten, öffentliche Dokumentation, geschlossene Statuswerte und sanitisiertes Testmaterial. Nicht erlaubt sind absolute lokale Pfade, private Quelltexte, private Repository-Namen oder Metadaten, Branches, Commits, Rohdatei-Hashes, Logs, Konten oder sensible Runtime-Daten.

## Review-Checkliste

- [ ] Public Manifest und Source Contract sind schema-validiert und digest-gekoppelt.
- [ ] Alle betroffenen Settings und Lernpfade wurden aktualisiert.
- [ ] `runtime_acceptance_complete=true` ist durch geschlossene Runtime-Evidenz gedeckt.
- [ ] `manual_acceptance_complete=false` bleibt bestehen, solange FZV2-RM-001…019 offen sind.
- [ ] FZMT und FZV2-RM besitzen getrennte Suite-IDs und LocalStorage-Schlüssel.
- [ ] Online- und Offline-Build sind strict grün.
- [ ] Interne Links, responsive Darstellung und Tastatur-/Accessibility-Grundfunktionen sind geprüft.
- [ ] Der generierte Site-Baum enthält keine externen Runtime-Assets oder private Metadaten.
- [ ] Der PR verändert nur öffentliche Dokumentationsflächen.

Der aktuelle Vertrag umfasst 56 Produktzeilen, sieben LineOptions, 70 atomare Produkt-Controls, zwei Actions und FZCP v1–v4. Der Workflow repariert keinen Indikatorcode und ersetzt keinen vollständigen manuellen Quantower-Abnahmetest.
