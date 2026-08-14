# Inventarstatus

| Oberfläche | Status | Aussage |
|---|---|---|
| 29 produktseitige Setting-Zeilen | `confirmed_current_product_source` | IDs, Defaults, Bereiche, Optionen und Relations sind dokumentiert. |
| 6 LineOptions / bis zu 41 atomare Controls | `confirmed_current_product_source` | Style, Breite und Farbe werden je Top/Bottom und Zustand gezählt. |
| `base.Settings`-Union | `runtime_inventory_pending` | TimeFrameConfig und UpdateType sind statisch möglich; konkrete Sichtbarkeit ist noch offen. |
| Indikatorversion in Quantower | `runtime_inventory_pending` | Noch kein stabiler öffentlicher Produktversionsanker. |
| `HelpLink` / nativer Menüort | `runtime_inventory_pending` | API-Fähigkeit ist belegt; konkrete UI-Präsentation ist noch offen. |
| Vollständige Quantower-UI-Behauptung | `false` | Wird erst nach dem getrennten Runtime-Inventar erlaubt. |

## Erforderliches Runtime-Inventar

Der spätere Test muss den Settings-Dialog im Defaultzustand und in jedem Abhängigkeitszweig erfassen: ATR, Percent, Fixed ticks, Active focus, alle Rendering-Modi, beide Range-Modi und Calculation start aus/an. Pro Zeile werden Name, Text, Typ, Gruppe, Default, Min/Max, Increment, Dimension, Enabled, Visible, Relation und Auswahlwerte verglichen.
