# Lernpfad 5: Recovery verstehen

**Dauer:** 25–45 Minuten. **Ziel:** Sichere Degradierung und Wiederherstellung einordnen, ohne absichtlich Daten oder Sidecars zu beschädigen.

## Zustandskarte

| Zustand | Bedeutung | Was weiterläuft |
|---|---|---|
| Complete | veröffentlichte Generation ist vollständig | Berechnung und Rendering |
| Incomplete | Nachweis oder Historie reicht vorübergehend nicht | letzte vollständige Generation bleibt nutzbar |
| SuspendedByDataGap | StrictFailClosed hat eine relevante Lücke erkannt | kontrollierter Retry/Backoff, keine Teilpublikation |
| QuotaExceeded | optionale Persistenz passt nicht in die Quote | Berechnung, Rendering und bestmögliche Crashrotation |

Eine reparierte Historie wird offscreen neu abgespielt. Erst wenn Revisionstoken, Ledger und Generation konsistent sind, erfolgt ein atomarer Swap. DATA GAP- und EPOCH-Marker erklären den Übergang.

## Sidecar und Restore

Mit `Enable semantic replay checkpoint=false` ist die optionale Persistenz standardmäßig aus. Bei Aktivierung gilt fail-closed: `Current → Previous → geschützter Restore Point → Rohneuaufbau`. Ungültige oder unbekannte Artefakte werden nicht teilweise übernommen.

Aktuelle Persistenzdefaults sind 512 MiB je `StateIdentity` und 4 GiB je Sidecar-Root. Quota-aware Admission und Hysterese-Recovery dürfen niemals berechnete oder gerenderte Linien reduzieren.

## Deep Verify sicher einordnen

- `Verify full history now…` startet einen optionalen asynchronen Single-Flight-Job.
- `Cancel full-history verify` beendet nur diesen optionalen Job, niemals zwingende Recovery.
- Eine saubere Prüfung erzeugt keine neue Generation.
- Nicht verfügbare Historie verändert weder die veröffentlichte Generation noch den DataStatus.

Für diesen Lernpfad genügt es, die Actions und Diagnostik zu verstehen. Führe die Actions erst im späteren vollständigen manuellen Test aus.

**Zurücksetzen:** `Enable semantic replay checkpoint=false`; keine Action ausführen.

**Vertiefung:** [Kontinuität und Wiederherstellung](../understand/recovery.md) · [Performance und Sidecar diagnostizieren](../troubleshoot/performance-and-sidecar.md)
