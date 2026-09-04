# Rendering und Historie lernen

## Rendering-Modi vergleichen

Nutze denselben Chartausschnitt nacheinander mit Adaptive, Full und Active focus. Preise, Segmentgrenzen und aktivierte Marker müssen gleich bleiben. Unterschiede dürfen nur Renderweg und in Active focus die Inaktiv-Deckkraft betreffen.

## Vier Historienmodi

- `Chart loaded range plus warm-up`: geladener Chartbereich plus automatisch oder manuell bestimmter Vorlauf.
- `Fixed lookback days`: rollierendes Zeitfenster; Standardwert der Tage ist 90.
- `Fixed calculation start`: expliziter Start; Eingabe erscheint in Plattformzeitzone, intern wird UTC verwendet.
- `Dynamic active-level price range`: Scope um offene Solid-Levels; Zielband standardmäßig ±10,00 %, mit Provider- oder Tageshorizont.

<div data-fz-simulator="history-range"></div>

## Pan/Zoom-Test

Verschiebe und zoome den Chart. Der Viewport-Index soll nur die Darstellung beschleunigen, ohne Levels zu löschen. Dynamische Historie begrenzt Berechnung und Veröffentlichung, nicht die segmenttreue Darstellung: Es gibt kein Clustering, Merging, Sampling oder Suppression.
