# Break Engine

Ein kurzer Tick durch ein Level ist noch kein Break. Die Engine trennt **Distanz**, **Preisquelle**, **Bestätigungsdauer**, **strikten Reset** und **Cooldown**.

## ConfirmedSide

Die gewählte Preisquelle muss jenseits der quantisierten Break-Grenze liegen. `Close` bewertet den Schlusskurs; `High/Low` wertet High und Low unabhängig aus und kann `AmbiguousBothSides` liefern. Schwellen werden am variablen TickGrid nach außen quantisiert, damit Rundung nie zu früh bestätigt.

## Drei Distanzmodi

| Modus | Gut geeignet für | Kerngedanke |
|---|---|---|
| One-minute ATR | verschiedene Instrumente und Timeframes | Volatilitätsrelativ auf MIN1-Basis |
| Percent of level | prozentual vergleichbare Märkte | Abstand relativ zum Levelpreis |
| Fixed ticks | feste Markt-/Tick-Konvention | absoluter Abstand in Ticks |

`0` ist bei Distanz und Confirmation eine gültige bewusste Einstellung. `ATR multiplier=0` umgeht die ATR-Warm-up-Abhängigkeit.

Sobald die Preisquelle in die Neutralzone zurückkehrt, wird der Timer **sofort vollständig zurückgesetzt**. Derselbe MIN1-Slot darf nicht neu starten. Nach einem committed Break blockiert der Cooldown schnelle Mehrfachzählungen.

<div data-fz-simulator="break-source"></div>

--8<-- "docs/includes/diagrams/break-reset.md"

Weiter: [Break-Einstellungen](../configure/maturity-and-break.md).
