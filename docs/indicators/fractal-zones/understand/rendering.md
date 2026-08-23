# Darstellung und Marker

Die Rendering-Modi ändern nur den Renderplan, nicht die berechneten Levels.

| Modus | Darstellung | Zweck |
|---|---|---|
| Adaptive | effizienter Viewport-Index und Cache | Standard für Alltag und große Historien |
| Full | vollständiger Referenzpfad | Vergleich und Diagnose |
| Active focus | inaktive Zustände mit konfigurierbarer Deckkraft | aktive Levels hervorheben |

Es gibt ausdrücklich **kein Clustering, Zusammenlegen, Sampling oder Unterdrücken**. Der optionale Preisbereichsfilter ist rein visuell und löscht nichts.

Offene Linien können bis zum aktuellen Kerzenende oder um Minuten/Kerzen nach rechts projiziert werden. Der Line-End-Marker sitzt dagegen auf der aktuellen Kerze plus seinem eigenen Offset – nicht am projizierten Zukunftsende.

Marker für Break, RoleChange, Event und End besitzen getrennte Sichtbarkeit, Farben, X/Y-Offsets und Schriftgrößen. `Font size=0` bedeutet Hoststandard.

<div data-fz-simulator="rendering-modes"></div>

Weiter: [Rendering, Marker und Historie konfigurieren](../configure/rendering-and-history.md).
