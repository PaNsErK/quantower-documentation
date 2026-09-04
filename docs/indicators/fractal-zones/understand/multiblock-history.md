# Mehrblock-Historie

Lange Historien werden in begrenzten Blöcken verarbeitet. Dadurch bleibt die Arbeit planbar, auch wenn ein Anbieter die Daten nicht in einem Abruf liefert.

--8<-- "docs/includes/diagrams/multiblock-history.md"

<div data-fz-simulator="multiblock-history"></div>

## Verbindliche Grenzen

- Ein Block umfasst höchstens 30.000 erwartete Minuten.
- Aus dem Cache wird höchstens einmal ein `DirectReload` versucht; einen dritten Weg gibt es nicht.
- Datenlücken werden nie mit synthetischen Minuten gefüllt.
- Eine unvollständige Historie geht über den recoverable-Incomplete-/Epoch-Pfad und ersetzt keine vollständige veröffentlichte Generation.

Beispiel: Liefert ein Provider nur die jüngsten Blöcke, kann die aktuelle Zone weiterhin darstellbar sein. Der Status bleibt trotzdem ehrlich: Für den nicht belegbaren früheren Teil gilt `Incomplete`, nicht „vollständig geprüft“.
