# Inventarstatus

| Oberfläche | Status | Aussage |
|---|---|---|
| 29 produktseitige Setting-Zeilen | `confirmed_current_product_source` | IDs, Defaults, Bereiche, Optionen und Relations sind dokumentiert. |
| 6 LineOptions / bis zu 41 atomare Controls | `confirmed_current_product_source` | Style, Breite und Farbe werden je Top/Bottom und Zustand gezählt. |
| `base.Settings`-Union | `runtime_inventory_confirmed` | 11 geerbte Zeilen mit bis zu 25 atomaren Controls sind erfasst. |
| Gesamte Settings-Union | `runtime_inventory_confirmed` | Bis zu 40 Zeilen beziehungsweise 66 atomare Controls. |
| Geladene Bundle-Version | `confirmed_from_loaded_bundle` | `1.0.0+90389555f55237713593a16f63195c900972a898`; keine eigene UI-Anzeige. |
| `HelpLink` / nativer Menüort | `not_available_empty_getter` | Die API ist vorhanden, Fractal Zones liefert aktuell aber keinen Link; der native Befehl ist deshalb nicht nutzbar. |
| Sichtbarkeitszweige | `runtime_inventory_confirmed` | Drei Break-Modi, drei Rendering-Modi und beide Calculation-Range-Modi wurden geschlossen verglichen. |
| Sanitisiertes Quell-Drift-Gate | `current_source_validated_sanitized` | Geschlossene Produktfakten werden lokal geprüft; private Pfade, Quelltext, Commits und Roh-Hashes werden nicht veröffentlicht. |
| Uneingeschränkte Quantower-UI-Behauptung | `false` | Die beiden gezielten FZRUI-Befunde sind geschlossen; der vollständige manuelle Quantower-Abnahmetest bleibt offen. |

## Bestätigte `base.Settings`-Union

| Gruppe | Runtime-Element | Aktueller Wert und Optionen | Controls |
|---|---|---|---:|
| VIEW | Position on chart | `Over chart`; außerdem `On chart background`, `New sub window` | 1 |
| VIEW | Use indicator values in window "Auto" scaling mode | `false` | 1 |
| TIMEFRAME VISIBILITY | Seconds | aktiviert; 1–9.999 | 3 |
| TIMEFRAME VISIBILITY | Minutes | aktiviert; 1–9.999 | 3 |
| TIMEFRAME VISIBILITY | Hours | aktiviert; 1–9.999 | 3 |
| TIMEFRAME VISIBILITY | Days | aktiviert; 1–999 | 3 |
| TIMEFRAME VISIBILITY | Weeks | aktiviert; 1–99 | 3 |
| TIMEFRAME VISIBILITY | Month | aktiviert; 1–99 | 3 |
| TIMEFRAME VISIBILITY | Years | aktiviert; 1–99 | 3 |
| TIMEFRAME VISIBILITY | Additional on the specified aggregation | Action `ADD AGGREGATION` | 1 |
| BASE | UpdateType | `On tick`; außerdem `On bar close` | 1 |

Es erschienen keine zusätzlichen `LinesSeries`- oder `LinesLevels`-Gruppen.

## Bestätigte Sichtbarkeitsregeln

| Auswahl | Sichtbar | Verborgen |
|---|---|---|
| One-minute ATR | ATR period, ATR multiplier, Minimum break distance | Percent und Fixed ticks |
| Percent of level | Minimum break distance, Break distance (%) | ATR period, ATR multiplier und Fixed ticks |
| Fixed ticks | Fixed break distance | ATR-, Percent- und Minimum-Felder |
| Adaptive oder Full | Rendering mode | Inactive state opacity |
| Active focus | Rendering mode und Inactive state opacity | – |
| Fixed initial history days | Initial range, Calculation start, Replay checkpoint, Verify und Cancel | – |
| Chart loaded range plus warm-up | nur Calculation range mode aus der Produktgruppe History | die fünf übrigen History-Zeilen |

## Geschlossene Runtime-Befunde

1. **FZRUI-01 – `runtime_confirmed_fixed`:** Quantower zeigt `Inactive state opacity` als `0,35` mit zwei Dezimalstellen. Ein Spinner-Schritt ergibt `0,40`, der Rückweg `0,35`. Nur die vorgesehene Deckkraft ändert sich; Linienauswahl, Level- und Zustandssemantik bleiben gleich.
2. **FZRUI-02 – `host_presentation_limitation_confirmed`:** Quantower BusinessLayer 1.146.17.0 zeigt den DateTime-Editor, bewahrt den Wert und deaktiviert `Initial range` bei aktivem Start. Ein separater nativer Enable-Toggler wird trotz korrektem Quellvertrag nicht dargestellt. UTC-, Clear- und Roundtrip-Semantik bleiben durch Hosttests bestätigt.

## Drift-Status richtig lesen

`no_drift` bedeutet, dass die geschlossenen Produktfakten, die öffentliche Inventur und der FZCP-Umfang übereinstimmen. Es ist **kein** Ersatz für den noch offenen vollständigen manuellen Quantower-Abnahmetest. `documentation_drift` verlangt eine bewusste Dokumentationsanpassung; `unsafe_or_ambiguous_source` stoppt ohne Veröffentlichung.
