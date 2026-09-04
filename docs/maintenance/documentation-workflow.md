# Dokumentation pflegen

Dieser Workflow hält die öffentliche Fractal-Zones-Dokumentation aktuell, ohne private Quellinhalte in das öffentliche Repository zu übernehmen. Eine Änderung beginnt mit einem read-only, sanitisierten Source Contract und endet erst nach Contract-, Site- und bei UI-bezogenen Aussagen zusätzlich nach Runtime-Inventur.

## Evidenzklassen nicht vermischen

1. **Historische Runtime-Evidenz** bleibt unverändert als V1–V4-Record erhalten.
2. **Aktuelle Source-Validierung** darf V5/V6 nur als `sourceValidatedRuntimePending` ausweisen.
3. **Runtime-UI-Inventur** prüft Präsentation, Sichtbarkeit, Version und HelpLink; sie ist keine Gesamt-Runtime-Abnahme.
4. **Manuelle Akzeptanz** bleibt unabhängig und lokal. MVA-IDs sind immer `suite_qualified`.

## Lokaler Ablauf

1. Produktquelle nur read-only auswerten und eine geschlossene, sanitierte V3-Kapsel erzeugen.
2. Public Manifest, Source Contract, Current Validation, Testkatalog und betroffene Seiten gemeinsam ändern.
3. Drift Guard, Schema, Unit Tests, strict Online-/Offline-Build und Generated-Site-Check ausführen.
4. Für UI-Behauptungen nur eine explizit autorisierte, nicht-tradende Inventur mit vollständiger Prestate-Wiederherstellung nutzen.
5. Nur evidenzgebundene Korrekturen veröffentlichen.

Erlaubt sind aggregierte Produktfakten, öffentliche Dokumentation, geschlossene Statuswerte und sanitisiertes Testmaterial. Nicht erlaubt sind absolute lokale Pfade, private Quelltexte, private Repository-Namen oder Metadaten, Branches, Commits, Rohdatei-Hashes, Logs, Konten oder sensible Runtime-Daten.

## Review-Checkliste

- [ ] Public Manifest und Source Contract sind schema-validiert und digest-gekoppelt.
- [ ] Alle aktuellen Settings, Sichtbarkeitszweige und vier Calculation-Range-Modi stimmen überein.
- [ ] V1–V4-Evidenz ist als historisch markiert; V5/V6 sind nicht voreilig runtime-validiert.
- [ ] `manual_acceptance_complete=false` bleibt erhalten.
- [ ] Online- und Offline-Build sind strict grün.
- [ ] Generierte Seite enthält keine externen Runtime-Assets oder private Metadaten.
- [ ] Der PR verändert nur öffentliche Dokumentationsflächen.
