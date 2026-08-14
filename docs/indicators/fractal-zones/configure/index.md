# Alle Einstellungen

Die aktuelle Produktquelle erzeugt **29 eigene Setting-Zeilen** in neun Gruppen. Sechs LineOptions-Zeilen enthalten je drei Bedienelemente – Style, Breite und Farbe. Damit gibt es höchstens **41 atomare Produkt-Bedienwerte**.

<div class="fz-inventory-pending" role="status">
<strong>Runtime-Abgrenzung:</strong> Quantower stellt zuerst <code>base.Settings</code> bereit und Fractal Zones hängt seine eigenen Zeilen an. Bestätigt sind 11 geerbte Zeilen mit bis zu 25 atomaren Controls. Zusammen umfasst die geschlossene Runtime-Union damit bis zu 40 Zeilen und 66 Controls. Zwei begrenzte Darstellungsfragen bleiben im <a href="../inventory-status/">Inventarstatus</a> ausgewiesen.
</div>

## Von Quantower geerbte Einstellungen

| Bereich | Zeilen | Atomare Controls | Enthaltene Bedienung |
|---|---:|---:|---|
| View | 2 | 2 | Position auf dem Chart und Auto-Skalierung |
| Timeframe Visibility | 8 | 22 | sieben aktivierte Zeitrahmenbereiche plus zusätzliche Aggregation |
| UpdateType | 1 | 1 | On tick oder On bar close |
| **Summe `base.Settings`** | **11** | **25** | bestätigte Runtime-Union |

## Gruppen

| Gruppe | Zeilen | Seite |
|---|---:|---|
| Fractal Maturity | 2 | [Maturity und Break Engine](maturity-and-break.md) |
| Break Engine | 8 | [Maturity und Break Engine](maturity-and-break.md) |
| Lifecycle | 2 | [Lifecycle und Linien](lifecycle-and-lines.md) |
| Provisional / Active / Historical Line Settings | 6 | [Lifecycle und Linien](lifecycle-and-lines.md) |
| Rendering | 2 | [Rendering, Marker und Historie](rendering-and-history.md) |
| Markers | 3 | [Rendering, Marker und Historie](rendering-and-history.md) |
| History | 6 | [Rendering, Marker und Historie](rendering-and-history.md) |

## Empfohlener Einstieg

Für den ersten manuellen Lauf zunächst alle Standards unverändert lassen. Danach immer nur **eine Setting-Familie** ändern und das erwartete Ergebnis in der [Testsuite](../test/manual-suite.md) festhalten.
