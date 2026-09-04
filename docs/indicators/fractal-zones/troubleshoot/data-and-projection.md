# Daten, Start und Projektion

## Keine Linien

Prüfe zuerst, ob genügend gültige MIN1-Historie für Maturity und Warm-up vorhanden ist. `Chart loaded range plus warm-up` berechnet nur geladenen Bereich plus Vorlauf; ein enger Chart kann daher bewusst weniger Historie enthalten als `Fixed lookback days`. Im dynamischen Modus begrenzen offene Active/Solid-Levels zusätzlich den Scope.

## Weniger Linien als erwartet

Vergleiche Adaptive mit Full; beide müssen dieselben Levels zeigen. Prüfe außerdem, ob Active focus inaktive Segmente durch niedrige Deckkraft schwerer lesbar macht. Dynamische Historie ist kein visueller Filter und darf keine Linie durch Clustering, Merging, Sampling oder Suppression entfernen.

## Calculation start

Bei `Fixed calculation start` wird die Auswahl im Host in Plattformzeitzone präsentiert, intern aber eindeutig nach UTC konvertiert. Clear entfernt den Wert. Ein unset-Wert darf den Bootstrap nicht dauerhaft blockieren. Die Runtime-Inventur liest diesen Wert nur; sie ändert ihn nicht.

## Datenlücke

`Incomplete` und `SuspendedByDataGap` sind recoverable. Der Indikator behält die letzte gute Generation, isoliert die neue DataEpoch und veröffentlicht erst nach vollständigem Replay.
