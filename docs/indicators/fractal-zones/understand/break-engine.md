# Break Engine

Ein kurzer Tick durch ein Level ist noch kein Break. Die Engine trennt **Distanz**, **Preisquelle**, **Bestätigungsdauer**, **strikten Reset** und **Cooldown**.

## Expected-side V2

Die gewählte Preisquelle muss jenseits der quantisierten, für das Level erwarteten Seite liegen. `Close` bewertet den Schlusskurs. `High/Low` bewertet für Resistance die obere und für Support die untere Seite. Eine gleiche Candle kann Dochte auf beiden Seiten besitzen; sie erzeugt dadurch weder eine erratene Richtung noch einen zweiten Commit.

Schwellen werden am variablen TickGrid nach außen quantisiert, damit Rundung nie zu früh bestätigt.

## Drei Distanzmodi

| Modus | Gut geeignet für | Kerngedanke |
|---|---|---|
| One-minute ATR | verschiedene Instrumente und Timeframes | volatilitätsrelativ auf MIN1-Basis |
| Percent of level | prozentual vergleichbare Märkte | Abstand relativ zum Levelpreis |
| Fixed ticks | feste Markt-/Tick-Konvention | absoluter Abstand in Ticks |

`0` ist bei Distanz und Confirmation gültig. `ATR multiplier=0` umgeht die ATR-Warm-up-Abhängigkeit.

Sobald die Preisquelle in die Neutralzone zurückkehrt, wird der Timer **sofort vollständig zurückgesetzt**. Derselbe MIN1-Slot darf nicht neu starten. Nach einem committed Break blockiert der Cooldown schnelle Mehrfachzählungen.

<div data-fz-simulator="break-source"></div>

--8<-- "docs/includes/diagrams/break-reset.md"
