# Aktueller Stand

Die Dokumentation enthält die aktuelle, quellvalidierte öffentliche Beschreibung von **Fractal Zones v2**. Sie trennt bewusst historische Runtime-Evidenz von aktuellen Source-Contract-Erweiterungen.

| Fläche | Zustand |
|---|---|
| Produktinventar | 56 Setting-Zeilen, 7 LineOptions, 70 atomare Controls, 2 Aktionen |
| Historische Runtime-Evidenz | FZCP v1–v4: FZ-001..FZ-102, GT-01..GT-180, MVA-01..MVA-25; erhalten, nicht umgedeutet |
| Aktueller Source Contract | FZCP-v5: FZ-103..FZ-112, GT-181..GT-220, FZCP-v5/MVA-26..37 |
| Aktueller Source Contract | FZCP-v6: FZ-113..FZ-116, GT-221..GT-234, FZCP-v6/MVA-38..45 |
| Aktueller Runtime-Status | `sourceValidatedRuntimePending` |
| UI-Inventur | `runtime_inventory_partial_confirmed_with_residuals` |
| Benutzerabnahme | `manual_acceptance_complete=false` |

`runtime_acceptance_complete=false` heißt nicht, dass die historische Evidenz verschwunden wäre. Es verhindert lediglich, dass V5/V6 ohne eine eigene Runtime-Prüfung als bestanden ausgegeben werden. MVA-IDs sind immer `suite_qualified`, damit gleichlautende Nummern aus verschiedenen Suites nicht verwechselt werden.

Die nicht-tradende UI-Inventur hat die produktseitigen Settings, LineOptions, Sichtbarkeitszweige, alle vier Calculation-Range-Modi und das native Calculation-Start-Feld im zugehörigen Zweig bestätigt. Die vollständige geerbte `base.Settings`-Union und ein öffentlicher Versionswert wurden nicht in der sanitisierten Evidenz erfasst; `base_settings_union` und `indicator_version` bleiben deshalb `not_captured_in_sanitized_evidence`.

## Aktuelle Erweiterungen

- **Vier** Calculation-Range-Modi statt drei, einschließlich `Dynamic active-level price range`.
- Dynamischer Historienhorizont: gesamte belegbare Providerhistorie oder `Bounded days` (Standard 365).
- Expected-side V2: Resistance bewertet die obere und Support die untere erwartete Seite. Eine doppelseitige Dochtbar erzeugt keinen zweiten Commit.
- Neun Selektoren werden versionsrobust gelesen und nur definierte Auswahlwerte werden übernommen.
- Lange Historie wird in Blöcken verarbeitet; keine synthetischen Minuten und maximal ein DirectReload-Fallback.
- Persistenzquoten: 256 MiB Live-State pro Identity, 1 GiB pro Prozess, 512 MiB Persistenz pro Identity und 4 GiB je Root. QuotaExceeded pausiert nur optionale Restore-Point-Writes.

## Offenes UI-Residual

Die Engine verwendet `expected_side_v2`. Eine möglicherweise abweichende historische Tooltip-Formulierung wird als `source_confirmed_runtime_ui_pending` geführt, bis die separate UI-Inventur die Host-Präsentation belegt. Sie darf die Engine-Regel nicht überschreiben.
