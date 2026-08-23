# Update und Rollback

## Vor dem Update

- Aktuelles Paket und dessen Dateiliste sichern.
- Wichtige Settings oder Presets dokumentieren.
- Quantower regulär schließen.
- Zielbestand und neues Manifest vergleichen.

## Nach dem Update

1. Exakt die erwarteten Dateien und ein flaches Layout prüfen.
2. Quantower starten und Status `Ready` abwarten.
3. Fixed Start, Preisquelle, Marker-Offsets, Boundary und Range-Modus kontrollieren.
4. Bei Bedarf die [Benutzer-Testmatrix](../test/v2-remediation-user-matrix.md) verwenden.

## Rollback

Bei Ladefehler, Hashabweichung oder gemischtem Layout Quantower regulär schließen und **das vollständige** vorherige Paket wiederherstellen. Keine Einzeldateien aus unterschiedlichen Generationen mischen. Sidecar-Artefakte nicht blind löschen: Ein ungültiger Zustand wird fail-closed verworfen und aus kanonischen MIN1-Daten neu aufgebaut.
