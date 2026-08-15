# Zeit- und Fraktallogik

## Interaktiver Timeframe-Vergleich

Alle drei Ansichten verwenden dieselben kanonischen MIN1-Daten. Verändere die rechte Reifezeit und die Sessionpause: Die sichtbare Kerzenzahl ändert sich je Timeframe, der fachliche Bestätigungszeitpunkt bleibt identisch.

<div class="fz-simulator" data-fz-simulator="timeframe-parity">
<p><strong>Ohne JavaScript:</strong> 30 offene Sessionminuten entsprechen 30 Ein-Minuten-Kerzen, häufig sechs Fünf-Minuten-Kerzen oder zwei Fünfzehn-Minuten-Kerzen. Geschlossene Sessionminuten werden nicht mitgezählt.</p>
</div>

*Realitätsnahes synthetisches Szenario; keine Live-, Konto- oder Handelsdaten.*

<section markdown="1" class="fz-topic" data-topic="FZT-02" data-modes="understand">

## Kanonische Ein-Minuten-Datenbasis

<div markdown="1" class="fz-depth" data-depth="short">Alle fachlichen Entscheidungen verwenden kanonische Ein-Minuten-Slots. Der sichtbare Chart-Timeframe ist Darstellung, nicht Entscheidungsquelle.</div>

<div markdown="1" class="fz-depth" data-depth="practice">

Beispiel: Bei `Before = 30` und `After = 30` benötigt ein Kandidat 30 offene Sessionminuten links und 30 offene Sessionminuten rechts. Auf einem 5‑Minuten-Chart sind das oft sechs sichtbare Kerzen je Seite; auf einem 1‑Minuten-Chart 30. Die fachliche Zeit bleibt identisch.

</div>

<div markdown="1" class="fz-depth" data-depth="technical">MIN1-Kanonisierung verhindert, dass ein 1m-, 5m- oder Tageschart aus derselben Historienquelle unterschiedliche Level erzeugt. Synthetische Slots dürfen zeitliche Kontinuität repräsentieren, aber keine echten Preisereignisse wie Retestkontakte vortäuschen.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-03" data-modes="understand troubleshoot">

## Session-Slots und Zeitachsen

<div markdown="1" class="fz-depth" data-depth="short">Gezählt werden erwartete offene Sessionminuten, intern eindeutig in UTC.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Wochenenden, Pausen und geschlossene Handelszeiten werden nicht wie normale Marktminuten behandelt. `Calculation start` wird in der aktiven Plattformzeitzone angezeigt und intern nach UTC normalisiert.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Ein validierter Session-Container wird über Bootstrap, History und Rebuild konsistent wiederverwendet. Null-Zeitzonen, Full-Day-Sessions und benutzerdefinierte Sessions dürfen nicht doppelt konvertiert werden.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-04" data-modes="understand">

## Top- und Bottom-Ursprung

<div markdown="1" class="fz-depth" data-depth="short">Ein Top entsteht an einem strikten Hoch, ein Bottom an einem strikten Tief.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Gleich hohe Nachbarwerte erfüllen kein striktes Extrem. Dadurch bleibt die Auswahl deterministisch und erzeugt keine willkürlichen Doppelursprünge.</div>

<div markdown="1" class="fz-depth" data-depth="technical">`OriginType` bleibt über die gesamte Lebensdauer unverändert. Rolle und Ursprung sind getrennte Eigenschaften: Ein Top-Ursprung kann später Support oder Resistance sein, ohne seine Identität oder Farbe zu verlieren.</div>

</section>

## Merksatz

> **Zeit statt Kerzenzahl. Ursprung statt aktueller Rolle. Chart-Timeframe statt neuer Semantik.**
