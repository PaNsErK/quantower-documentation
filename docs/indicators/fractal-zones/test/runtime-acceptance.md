# Technische Runtime-Abnahme

`runtime_acceptance_complete=true`

Die aktuelle veröffentlichte Evidenz bestätigt Build, automatisierte Tests, FZCP v1–v4, ein 9/9-Deployment, Laufzeitverhalten und MVA-17…25. Der Host blieb in einem 2.700,009-Sekunden-Soak bei 188 von 188 Stichproben responsiv.

Fünfzehn frühere Benutzerprüfungen wurden in diesem Lauf bewusst nicht wiederholt. Ihre Einzelheiten werden hier weder erfunden noch als neue FZV2-RM-Fälle dupliziert.

## Reproduzierbare Größenklassen

| Klasse | effektive MIN1-Bars | Laufzeit | Working Set |
|---|---:|---:|---:|
| 10k | 14.400 | ca. 10 s | 691 MiB |
| 30k | 28.800 | ca. 15 s | 678 MiB |
| ≈130k | 129.600 | unter 30 s | 981 MiB |

Die Werte sind Evidenz des geprüften Systems, keine universelle Hardwaregarantie.

## Akzeptierte nichtblockierende Warnung

Im Persistenz-Stresstest wurde QuotaExceeded ausgelöst. Optionale Writes pausierten wie vorgesehen; Berechnung und sichtbare Projektion blieben funktionsfähig. Diese Warnung ist dokumentiert und darf nicht als bestanden verschwinden.
