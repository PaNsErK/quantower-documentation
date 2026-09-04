# Maturity und Break Engine konfigurieren

## Maturity

`Before` und `After` zählen erwartete **offene Ein-Minuten-Session-Slots**, nicht Chartkerzen. 30/30 bedeutet: Ein Kandidat benötigt 30 gültige Minuten links und 30 rechts. Auf einem 5-Minuten-Chart bleiben es dieselben 60 MIN1-Slots.

## Distanzmodus

| Modus | Formel | Sinnvoll wenn |
|---|---|---|
| One-minute ATR | max(ATR × Multiplikator, Mindestticks) | Volatilität und Instrumente stark variieren |
| Percent of level | max(Level × Prozent, Mindestticks) | relative Preisbewegung maßgeblich ist |
| Fixed ticks | feste Tickzahl | ein instrumentspezifischer Abstand gewollt ist |

Die Distanz wird nach außen auf das zum Preisband gültige Tickraster quantisiert. Dadurch wird die effektive Grenze nie versehentlich enger.

## Preisquelle und erwartete Seite

- **Close**: Der Schlusskurs einer geschlossenen MIN1-Bar muss jenseits der erwarteten, quantisierten Break-Grenze liegen.
- **High/Low**: Für Resistance bewertet die Engine die obere, für Support die untere erwartete Seite. Ein Docht auf der anderen Seite erzeugt keinen zweiten Commit.

`AmbiguousBothSides` kann in älteren Daten-/Kompatibilitätsdarstellungen vorkommen, ist aber keine aktuelle Expected-side-V2-Entscheidungsregel. Die Engine rät keine Richtung aus einer beidseitigen Candle.

<div data-fz-simulator="break-source"></div>

## Null ist ein echter Wert

`ATR multiplier = 0`, `Minimum break distance = 0`, `Break distance (%) = 0`, `Fixed break distance = 0` und `Break confirmation = 0` sind gültig. Bei effektiver Distanz null zählt der Grenzkontakt. ATR-Multiplikator null benötigt kein ATR-Warm-up. Bestätigung null committed im ersten qualifizierenden geschlossenen Session-Slot.

## Timer, Reset und Cooldown

Ein qualifizierter Übertritt startet `BreakPending`. Jede Rückkehr in die Neutralzone setzt den Timer sofort zurück. Ein Reset-Slot darf nicht zugleich einen neuen Versuch starten. Nach einem committed Break blockiert der Cooldown weitere Commits bis zum Ende des konfigurierten Minutenabstands.

--8<-- "docs/includes/diagrams/break-reset.md"
