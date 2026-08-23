# Rendering, Marker und Historie konfigurieren

## Rendering-Modi

- **Adaptive** (Standard): Viewport-Index und Cache wählen den effizienten Renderplan.
- **Full**: direkte Vollprojektion als Referenzweg.
- **Active focus**: Provisional und BrokenWatch erhalten die konfigurierbare Inaktiv-Deckkraft; Active bleibt voll sichtbar.

Alle Modi bewahren dieselben sichtbaren Segmente und aktivierten Annotationen. Es gibt kein Clustering, Merging, Sampling oder Suppression.

<div data-fz-simulator="rendering-modes"></div>

## Status und Preisfilter

`Show status overlay` zeigt Loading, Recalculating, Ready, Incomplete oder Error auch bei leerer Projektion. Der Preisfilter ist standardmäßig aus. Aktiv blendet er Elemente außerhalb des symmetrischen, inklusiven Bereichs um den aktuellen Marktpreis nur in der Anzeigeabfrage aus. Ausschalten bringt sie unverändert zurück; StateIdentity, Replay und Checkpoints bleiben gleich.

## Offene Linien

`Open line end` endet offene Linien finite am Ende der aktuellen Bar, nach 1–10.080 Wall-Clock-Minuten oder nach 1–500 zeitbasierten Chartkerzen. Auf nicht zeitbasierten Charts fällt Chart candles sicher auf Current bar end zurück. Linienende-Marker bleiben an der aktuellen Candle verankert und wandern nicht zum projizierten Zukunftsende.

## Marker

End, Break und Role-change haben eigene Sichtbarkeiten und Farben. Marker können am Ereignis und/oder am aktuellen Linienende erscheinen. Event und Line-end besitzen getrennte X-Modi:

- **DPI pixels**: ungefähr konstanter Bildschirmabstand.
- **Chart candles**: zeitbasierter Candle-Abstand, timeframe-stabil.

Y-Offsets bleiben DPI-basiert. `0` bei Font size verwendet die Hostschrift; explizite Größen sind 6–32 pt. Line-end X startet bei **+1 Chart candle**, Event X bei 0 DPI-Pixel.

## Calculation range

| Modus | Aktive Unterfelder | Verhalten |
|---|---|---|
| Fixed lookback days | Fixed lookback, Standard 90 | kalenderbasierter Ursprung, beim Append eingefroren |
| Fixed calculation start | Calculation start | Anzeige in Plattformzeitzone, intern UTC, Änderung mit Bestätigung |
| Chart loaded range plus warm-up | Warm-up mode; bei Manual Additional days | Standard für neue Instanzen |

Automatic Warm-up verwendet ein Drittel der geladenen Chartdauer, auf ganze Tage aufgerundet und auf 2–30 Kalendertage begrenzt. Manual akzeptiert 0–3.650 zusätzliche Tage; der frühere Wert aus manuellem Warm-up und zwingendem Session-Slot-Preroll gewinnt.

<div data-fz-simulator="history-range"></div>

## Checkpoint und Deep Verify

`Enable semantic replay checkpoint` ist standardmäßig an. Current und Previous werden fail-closed validiert; stale oder corrupt führt zum Raw Rebuild aus MIN1. `Verify full history now…` startet einen asynchronen Single-Flight-Job. Er publiziert bei sauberem Ergebnis keine neue Generation; Dirty Blocks laufen über den normalen Offscreen-Replay. `Cancel` beendet nur den optionalen Job und niemals eine zwingende Recovery.
