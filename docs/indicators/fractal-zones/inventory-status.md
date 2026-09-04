# Inventarstatus

## Produktseitiges Inventar

| Größe | Wert |
|---|---:|
| Setting-Zeilen | 56 |
| Aktionen | 2 |
| LineOptions-Zeilen | 7 |
| Atomare Produkt-Controls | 70 |
| Sichtbarkeitszweige | 13 |

Die [vollständige Tabelle](configure/index.md) ist die öffentliche Referenz für ID, Label, Standard, Bereich, Optionen und Sichtbarkeit.

## Geerbte base.Settings

Die 11 sichtbaren Basiszeilen mit höchstens 25 atomaren Controls sind eine **historische Host-Beobachtung**. Die nicht-tradende Runtime-Inventur hat die produktseitigen Settings, LineOptions und ihre Sichtbarkeitszweige bestätigt, aber keine vollständige aktuelle `base.Settings`-Union sanitisiert erfasst. Deshalb bleibt `base_settings_union=not_captured_in_sanitized_evidence`; aus den vorhandenen Angaben wird keine vollständige Host-UI-Garantie abgeleitet.

## Versions- und Help-Zustand

- `indicator_version_state=current_source_validated_runtime_inventory_pending` und `version_ui_state=not_captured_in_sanitized_evidence`.
- Der native Help-Befehl war im beobachteten Host-Kontext vorhanden, aber deaktiviert und wurde nicht ausgeführt: `help_link_state=confirmed_disabled_current_host_context_not_executed`.
- Es wird weder eine öffentliche Buildnummer noch eine private Installationsidentität erfunden.
