# Dokumentation pflegen

Dieser Workflow hält die öffentliche Fractal-Zones-Dokumentation aktuell, ohne private Quellinhalte in das öffentliche Repository zu übernehmen. Er ist bewusst leichter als eine Produktentwicklung: ein kleiner Branch, ein geschlossener Drift-Check, zielgerichtete redaktionelle Änderungen und ein normaler Pull Request.

## Wann ist eine Aktualisierung nötig?

- Ein Setting, Default, Bereich, Sichtbarkeitszweig oder LineOptions-Control ändert sich.
- FZCP-Anforderungen, Golden Traces oder manuelle Akzeptanzen ändern sich.
- Ein Runtime-Residual wird bestätigt, repariert oder neu klassifiziert.
- Lernpfade, Beispiele oder Troubleshooting müssen an Produktverhalten angepasst werden.

## Lokaler Ablauf

1. Verwende einen berechtigten lokalen Checkout der Produktquelle ausschließlich read-only.
2. Starte den Update-Runner mit `--source-root` auf diesen Checkout.
3. Bei `documentation_drift` passe zuerst das geschlossene Manifest, den Source Contract und die betroffenen Seiten konsistent an.
4. Führe den Runner erneut aus. Erst danach darf ein Dokumentations-PR entstehen.
5. Der manuelle Quantower-Abnahmestatus bleibt unverändert, bis die interaktive Testsuite tatsächlich vollständig abgeschlossen wurde.

Der Runner gibt ausschließlich geschlossene Zustände aus:

| Status | Bedeutung | Nächste Aktion |
|---|---|---|
| `no_drift` | Vertrag und Dokumentation stimmen überein | normaler Review |
| `documentation_drift` | öffentliche Fakten oder Validierung weichen ab | Dokumentation gezielt aktualisieren |
| `runtime_confirmation_required` | statische Fakten stimmen; eine Hostdarstellung bleibt offen | getrennte Runtime-Prüfung planen |
| `unsafe_or_ambiguous_source` | Quelle fehlt, ist mehrdeutig oder nicht sicher auswertbar | sicher stoppen und Quelle klären |

## Veröffentlichungsgrenze

Erlaubt sind aggregierte Produktfakten, öffentliche Dokumentation, geschlossene Statuswerte und sanitisiertes Testmaterial. Nicht erlaubt sind absolute lokale Pfade, private Quelltexte, private Repository-Namen oder Metadaten, Branches, Commits, Rohdatei-Hashes, Logs, Konten oder sensible Runtime-Daten.

## Review-Checkliste

- [ ] Public Manifest und Source Contract sind schema-validiert und digest-gekoppelt.
- [ ] Alle betroffenen Settings und Lernpfade wurden aktualisiert.
- [ ] `manual_acceptance_complete=false` bleibt bestehen, solange die manuelle Suite offen ist.
- [ ] Online- und Offline-Build sind strict grün.
- [ ] Interne Links, responsive Darstellung und Tastatur-/Accessibility-Grundfunktionen sind geprüft.
- [ ] Der generierte Site-Baum enthält keine externen Runtime-Assets oder private Metadaten.
- [ ] Der PR verändert nur öffentliche Dokumentationsflächen.

Die Produktkorrektur für FZRUI-01 und die Hostbestätigung für FZRUI-02 gehören weiterhin in getrennte Produkt-/Runtime-Slices; dieser Workflow repariert keinen Indikatorcode.
