# Bruchmodi und Lifecycle lernen

## Übung A: Preisquelle

Vergleiche `Close` und `High/Low` auf demselben Level. Close reagiert erst auf den Schlusskurs; High/Low bewertet die für Resistance bzw. Support erwartete Seite. Eine beidseitige Candle erzeugt keinen zweiten Commit. Beobachte nur – ändere keine weiteren Parameter.

<div data-fz-simulator="break-source"></div>

## Übung B: Distanz

| Ziel | Modus | Startwert |
|---|---|---|
| instrumentübergreifend | One-minute ATR | 60 / 0,50 / min. 2 Ticks |
| prozentual | Percent of level | 0,05 % |
| feste Mikrostruktur | Fixed ticks | 2 Ticks |

## Übung C: strikter Reset

Lass einen BreakPending-Timer beginnen, führe den Preis kurz in die Neutralzone und danach erneut hinaus. Der erste Timer muss verworfen sein; im selben Slot darf kein Neustart erfolgen.

## Erwartung

Ein Break ist erst nach Distanz, vollständiger Bestätigungsdauer und atomarem Commit gezählt. Cooldown verhindert schnelle Doppelzählungen. Retest/RoleChange sind ein späterer, eigener Rückkehrpfad.
