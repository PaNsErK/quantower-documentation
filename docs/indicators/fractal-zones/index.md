# Fractal Zones

<div class="fz-safety" role="note" aria-label="Sicherheitsgrenze">
<strong>Nicht-tradender Indikator:</strong> Fractal Zones berechnet und zeichnet Chart-Level. Er platziert, ändert oder storniert keine Orders und verändert weder Konto noch Position, Portfolio, Verbindung oder Strategie.
</div>

<section markdown="1" class="fz-topic" data-topic="FZT-01" data-modes="understand">

## Zweck und Sicherheitsgrenze

<div markdown="1" class="fz-depth" data-depth="short">

Fractal Zones findet zeitnormalisierte Swing-Hochs und Swing-Tiefs und führt daraus horizontale Level mit nachvollziehbarem Lebenszyklus fort.

</div>

<div markdown="1" class="fz-depth" data-depth="practice">

Eine Linie beginnt **provisorisch**, wird nach zeitlicher Reife **aktiv**, kann nach bestätigten Brüchen **historisch beobachtet**, durch einen Retest wieder **aktiviert** und schließlich exakt **beendet** werden. Der Chart-Timeframe ändert die zugrunde liegende MIN1-Entscheidungslogik nicht.

Die Farben kennzeichnen den Ursprung: Top standardmäßig Grün, Bottom standardmäßig Rot. Ein späterer Rollenwechsel ändert die Farbe absichtlich nicht.

</div>

<div markdown="1" class="fz-depth" data-depth="technical">

Die öffentliche Dokumentation trennt drei Ebenen:

- **Produktsemantik:** MIN1-Slots, Sessionkalender, Fraktal-, Break-, Retest-, Rollen- und Endzustände.
- **Chartprojektion:** segmenttreue Linien, Marker, Viewport-Index und Render-Plan-Cache ohne Semantikverlust.
- **Betriebssicherheit:** ContinuityDataEpoch, Offscreen-Replay, atomarer Generation-Swap, Sidecar-Restore und Deep Verify.

</div>

</section>

## Schnellstart

1. Lies [Zeit- und Fraktallogik](understand/time-and-fractals.md).
2. Vergleiche danach den [Zustandsablauf](understand/lifecycle.md).
3. Prüfe vor manuellen Änderungen [alle Einstellungen](configure/index.md).
4. Arbeite die [interaktive Testsuite](test/manual-suite.md) in einem sicheren, nicht-tradenden Chart ab.

--8<-- "docs/includes/diagrams/lifecycle.md"

<div class="fz-inventory-pending" role="status">
<strong>Inventarstatus:</strong> Bestätigt sind 29 produktseitige Setting-Zeilen, 6 LineOptions-Zeilen, 11 geerbte Quantower-Basiszeilen und zusammen bis zu 66 atomare Bedienelemente. Zwei begrenzte Runtime-Residuals bleiben transparent dokumentiert.
</div>
