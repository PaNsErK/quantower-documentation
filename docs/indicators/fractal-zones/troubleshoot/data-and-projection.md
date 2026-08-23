# Daten, Start und Projektion

## Keine Linien

Prüfe zuerst, ob genügend gültige MIN1-Historie für Maturity und Warm-up vorhanden ist. `ChartLoadedRangePlusWarmup` berechnet nur geladenen Bereich plus Vorlauf; ein enger Chart kann deshalb bewusst weniger Historie enthalten als RollingLookbackDays.

## Weniger Linien als erwartet

Schalte den Preisbereichsfilter aus. Er ist rein visuell. Vergleiche Adaptive mit Full; beide müssen dieselben Levels zeigen. Prüfe außerdem, ob du nur Active focus betrachtest und inaktive Segmente durch niedrige Deckkraft übersiehst.

## CalculationStart

Bei `FixedStartUtc` wird die Auswahl im Host in Plattformzeitzone präsentiert, intern aber eindeutig nach UTC konvertiert. Clear entfernt den Wert. Ein unset-Wert darf den Bootstrap nicht dauerhaft blockieren.

## Datenlücke

`Incomplete` und `SuspendedByDataGap` sind recoverable. Der Indikator behält die letzte gute Generation, isoliert die neue DataEpoch und veröffentlicht erst nach vollständigem Replay.
