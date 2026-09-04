# Technische Runtime-Abnahme

`runtime_acceptance_complete=false`

## Historische V1–V4-Evidenz

Die veröffentlichte historische Evidenz bestätigt Build, automatisierte Tests, FZCP v1–v4, ein 9/9-Deployment, Laufzeitverhalten und MVA-17..25. Der Host blieb in einem 2.700,009-Sekunden-Soak bei 188 von 188 Stichproben responsiv.

| Klasse | effektive MIN1-Bars | Laufzeit | Working Set |
|---|---:|---:|---:|
| 10k | 14.400 | ca. 10 s | 691 MiB |
| 30k | 28.800 | ca. 15 s | 678 MiB |
| ≈130k | 129.600 | unter 30 s | 981 MiB |

Diese Werte bleiben historische Evidenz des damals geprüften Systems, keine universelle Hardwaregarantie.

## Aktuelle V5/V6-Grenze

FZCP-v5 und FZCP-v6 sind dokumentationsseitig quellvalidiert, aber **nicht** runtime-validiert: `sourceValidatedRuntimePending`. Erst eine separate nicht-tradende Runtime-Prüfung darf den aktuellen Runtime-Status verändern. Die spätere UI-Inventur allein ist ebenfalls keine vollständige Runtime-Abnahme.

## Akzeptierte historische Warnung

Im Persistenz-Stresstest wurde QuotaExceeded ausgelöst. Optionale Writes pausierten wie vorgesehen; Berechnung und sichtbare Projektion blieben funktionsfähig. Die aktuellen Quotenregeln führen diese Grenze fort, ohne Linien zu reduzieren oder aus dem Chart zu entfernen.
