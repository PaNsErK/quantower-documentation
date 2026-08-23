# Maturity und Break Engine konfigurieren

## Maturity

`Before` und `After` zählen erwartete **offene Ein-Minuten-Session-Slots**, nicht Chartkerzen. 30/30 bedeutet: Ein Kandidat benötigt 30 gültige Minuten links und 30 rechts. Auf einem 5-Minuten-Chart bleiben es dieselben 60 MIN1-Slots.

- [Before (minutes)](index.md#setting-maturity-before-minutes): Standard 30.
- [After (minutes)](index.md#setting-maturity-after-minutes): Standard 30.

Größere Werte liefern selektivere, später bestätigte Fraktale. Kleinere Werte reagieren schneller und erzeugen mehr Level.

## Distanzmodus

| Modus | Formel | Sinnvoll wenn |
|---|---|---|
| One-minute ATR | max(ATR × Multiplikator, Mindestticks) | Volatilität und Instrumente stark variieren |
| Percent of level | max(Level × Prozent, Mindestticks) | relative Preisbewegung maßgeblich ist |
| Fixed ticks | feste Tickzahl | ein instrumentspezifischer Abstand gewollt ist |

Die Distanz wird nach außen auf das zum Preisband gültige Tickraster quantisiert. Dadurch wird die effektive Grenze nie versehentlich enger.

## Preisquelle

- **Close**: Nur der Schlusskurs einer geschlossenen MIN1-Bar qualifiziert die Seite.
- **High/Low**: High oder Low darf die Grenze erreichen. Trifft dieselbe Bar beide Seiten, entsteht `AmbiguousBothSides`; der Indikator rät keine Richtung.

<div data-fz-simulator="break-source"></div>

## Null ist ein echter Wert

`ATR multiplier = 0`, `Minimum break distance = 0`, `Break distance (%) = 0`, `Fixed break distance = 0` und `Break confirmation = 0` sind gültig. Bei effektiver Distanz null zählt der Grenzkontakt. ATR-Multiplikator null benötigt kein ATR-Warm-up. Bestätigung null committed im ersten qualifizierenden geschlossenen Session-Slot.

## Timer, Reset und Cooldown

Ein qualifizierter Übertritt startet `BreakPending`. Jede Rückkehr in die neutrale Zone setzt den Timer sofort zurück. Ein Reset-Slot darf nicht zugleich einen neuen Versuch starten. Nach einem committed Break blockiert der Cooldown weitere Commits bis zum Ende des konfigurierten Minutenabstands.

--8<-- "docs/includes/diagrams/break-reset.md"

## Praxisbeispiel

Level 100, ATR 2, Multiplikator 0,5 und Mindestabstand 2 Ticks à 0,25: Rohdistanz 1,0; Mindestdistanz 0,5; maßgeblich ist 1,0. Bei Break confirmation 5 muss die Preisquelle fünf fortlaufende offene Minuten jenseits der eingefrorenen Grenze bleiben.
