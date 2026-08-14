# Diagnoseweg

Arbeite immer von **Daten und Status** zur **Projektion** und erst danach zur **Darstellung**:

1. Ist der Startanker gesetzt und in UTC plausibel?
2. Ist der Sessionkalender verfügbar?
3. Ist der History-Status Complete, Incomplete oder SuspendedByDataGap?
4. Enthält die veröffentlichte Generation Segmente?
5. Wurde ein Rebuild angefordert und beendet?
6. Hat der Render-Plan sichtbare Segmente für den Viewport?
7. Was meldet `LastPaintOutcome`?

Persistierte, präfixgefilterte und zeitbegrenzte Diagnostik hat Vorrang. Vollständige Logs, lokale Installationspfade und sensible Laufzeitdaten gehören nicht in Testnotizen oder öffentliche Evidenz.

- [Daten, Start und Projektion](data-and-projection.md)
- [Performance und Sidecar](performance-and-sidecar.md)
