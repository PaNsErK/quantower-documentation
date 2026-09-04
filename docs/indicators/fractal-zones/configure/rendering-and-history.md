# Rendering, Marker und Historie konfigurieren

## Rendering-Modi

- **Adaptive** (Standard): Viewport-Index und Cache wählen den effizienten Renderplan.
- **Full**: direkte Vollprojektion als Referenzweg.
- **Active focus**: Provisional und BrokenWatch erhalten die konfigurierbare Inaktiv-Deckkraft; Active bleibt voll sichtbar.

Alle Modi bewahren dieselben vorhandenen Segmente und aktivierten Annotationen. Es gibt kein Clustering, Merging, Sampling oder Suppression.

<div data-fz-simulator="rendering-modes"></div>

## Status und offene Linien

Der Host-Status ist über den Indikatornamen bzw. die Statusdarstellung einsehbar; ein produktseitiger `ShowStatusOverlay`-Schalter gehört nicht zum aktuellen Inventar. Offene Linien enden finite an der aktuellen Bar, nach Minuten oder nach zeitbasierten Chartkerzen. Der Line-End-Marker bleibt an der aktuellen Candle verankert.

## Marker

End, Break und Role-change haben eigene Sichtbarkeiten und Farben. Marker können am Ereignis und/oder am aktuellen Linienende erscheinen. Event und Line-end besitzen getrennte X-Modi. `DPI pixels` hält den Bildschirmabstand ungefähr konstant; `Chart candles` hält den zeitbasierten Candle-Abstand. `Font size=0` nutzt die Hostschrift.

## Calculation range

| Modus | Aktive Unterfelder | Verhalten |
|---|---|---|
| Fixed lookback days | Fixed lookback, Standard 90 | kalenderbasierter Ursprung, beim Append eingefroren |
| Fixed calculation start | Calculation start | Plattformzeitzone in der UI, intern UTC; nicht für die Inventur ändern |
| Chart loaded range plus warm-up | Warm-up mode; bei Manual Additional days | Standard für neue Instanzen |
| Dynamic active-level price range | Active-level price range, Dynamic history horizon, optional Dynamic history days | Scope an offenen Solid-Levels und Providerhistorie ausrichten |

Automatic Warm-up verwendet ein Drittel der geladenen Chartdauer, auf ganze Tage aufgerundet und auf 2–30 Kalendertage begrenzt. Die dynamische Range ist kein optischer Filter: Sie verändert weder die segmenttreue Renderregel noch die No-Cluster-Regel.

<div data-fz-simulator="history-range"></div>

Für die genaue Scope-Entscheidung siehe [Dynamische Historie](../understand/dynamic-history.md); der Umgang mit großen zusammenhängenden Lücken ist unter [Mehrblock-Historie](../understand/multiblock-history.md) beschrieben.

## Checkpoint und Deep Verify

`Enable semantic replay checkpoint` ist standardmäßig an. Current und Previous werden fail-closed validiert; stale oder corrupt führt zum Raw Rebuild aus MIN1. `Verify full history now…` startet einen asynchronen Single-Flight-Job. Er publiziert bei sauberem Ergebnis keine neue Generation; Dirty Blocks laufen über den normalen Offscreen-Replay. `Cancel` beendet nur den optionalen Job und niemals eine zwingende Recovery.
