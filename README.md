# Inoffizielle Quantower-Dokumentation

Öffentliche, **inoffizielle** Dokumentation für Quantower-Komponenten. Der aktuelle Schwerpunkt ist **Fractal Zones v2**.

Status: `public_beta_user_evaluation_pending`

- `runtime_acceptance_complete=true`: Build, vollständige Tests, FZCP v1–v4, 9/9-Deployment, MVA-17..25 und der 45-Minuten-Soak sind technisch abgeschlossen.
- `manual_acceptance_complete=false`: Die abschließende Benutzerabnahme ist noch nicht abgeschlossen.
- `user_evaluation=pending_user_evaluation`: 19 klar getrennte Fälle warten auf die Bewertung durch den Benutzer.

Die Website funktioniert online und offline ohne Analytics, Telemetrie, Remote-Fonts, CDN-Skripte oder Runtime-Netzwerk-API. Lokaler Testfortschritt bleibt im Browser und wird nur auf ausdrücklichen Wunsch exportiert.

## Lokal prüfen

```text
python tools/run_documentation_update.py
```

Das Projekt enthält keine Quantower-Binärdateien, privaten Quelltexte, Rohlogs oder Trading-Daten.
