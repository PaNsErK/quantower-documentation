# Recovery lernen

## Drei getrennte Begriffe

- **Checkpoint:** schnelle, wiederaufbaubare Replay-Hilfe.
- **Sidecar:** semantisch validierte, content-addressed Persistenz.
- **Deep Verify:** prüft Historie und löst bei Abweichung Offscreen-Replay aus.

## Sichere Erwartung

Während Recovery bleibt die letzte vollständig veröffentlichte Generation sichtbar. Eine beschädigte oder veraltete Datei wird nicht teilweise übernommen. Bei QuotaExceeded pausieren optionale Restore-Point-Schreibvorgänge, nicht die Levelberechnung.

## Übung

Öffne `Verify full history now…`, beobachte den Single-Flight-Status und brich optional über `Cancel full-history verify` ab. Ein Cancel darf keine partielle Generation veröffentlichen und keine obligatorische Recovery abbrechen.

Siehe [Kontinuität und Wiederherstellung](../understand/recovery.md) für die Restore-Kette.
