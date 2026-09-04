# Darstellung und Marker

Die Rendering-Modi ändern nur den Renderplan, nicht die berechneten Levels.

| Modus | Darstellung | Zweck |
|---|---|---|
| Adaptive | effizienter Viewport-Index und Cache | Standard für Alltag und große Historien |
| Full | vollständiger Referenzpfad | Vergleich und Diagnose |
| Active focus | inaktive Zustände mit konfigurierbarer Deckkraft | aktive Levels hervorheben |

Es gibt ausdrücklich **kein Clustering, Zusammenlegen, Sampling oder Unterdrücken**. Die dynamische Historie begrenzt Berechnung und Veröffentlichung offener Solid-Level; sie ist kein Renderfilter und löscht keine bereits berechneten Linien.

Offene Linien können bis zum aktuellen Kerzenende oder um Minuten/Kerzen nach rechts projiziert werden. Der Line-End-Marker sitzt dagegen auf der aktuellen Kerze plus seinem eigenen Offset – nicht am projizierten Zukunftsende.

Marker für Break, RoleChange, Event und End besitzen getrennte Sichtbarkeit, Farben, X/Y-Offsets und Schriftgrößen. `Font size=0` bedeutet Hoststandard.

<div data-fz-simulator="rendering-modes"></div>
