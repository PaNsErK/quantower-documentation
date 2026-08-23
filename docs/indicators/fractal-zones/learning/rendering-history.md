# Rendering und Historie lernen

## Rendering-Modi vergleichen

Nutze denselben Chartausschnitt nacheinander mit Adaptive, Full und Active focus. Preise, Segmentgrenzen und aktivierte Marker müssen gleich bleiben. Unterschiede dürfen nur Renderweg und in Active focus die Inaktiv-Deckkraft betreffen.

## Historienmodi

- `ChartLoadedRangePlusWarmup`: geladener Chartbereich plus automatisch oder manuell bestimmter Vorlauf.
- `RollingLookbackDays`: rollierendes Zeitfenster; Standardwert der Tage ist 90.
- `FixedStartUtc`: expliziter Start; Eingabe erscheint in Plattformzeitzone, intern wird UTC verwendet.

<div data-fz-simulator="history-range"></div>

## Pan/Zoom-Test

Verschiebe und zoome den Chart. Der Viewport-Index soll nur die Darstellung beschleunigen, ohne Levels zu löschen. Der Preisfilter ist ebenfalls rein visuell. Schalte ihn aus, um die unveränderte Gesamtmenge zu prüfen.
