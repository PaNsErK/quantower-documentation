# Bruchlogik

--8<-- "docs/includes/diagrams/break-reset.md"

## Interaktives Chartlabor: Bruchgrenze

Wähle Distanzmodus, Zonenseite und Verlauf. Die gelbe Linie zeigt die tatsächlich zu überschreitende Bruchgrenze. Linienart, Farbe und Breite lassen sich ausschließlich für diese Lernansicht verändern.

<div class="fz-simulator" data-fz-simulator="break-boundary">
<p><strong>Ohne JavaScript:</strong> Bei Resistance liegt die Bruchgrenze oberhalb, bei Support unterhalb des Levels. Fixed ticks bleibt absolut, Percent skaliert mit dem Levelpreis und One-minute ATR mit der MIN1-Volatilität.</p>
</div>

*Realitätsnahes synthetisches Szenario; keine Live-, Konto- oder Handelsdaten.*

<section markdown="1" class="fz-topic" data-topic="FZT-08" data-modes="understand">

## Active und BreakPending

<div markdown="1" class="fz-depth" data-depth="short">Active ist sichtbar solid. BreakPending ist nur ein interner Prüfzustand und erzeugt noch keinen historischen Bruch.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Ein kurzer Spike jenseits der Grenze reicht nicht. Der Preis muss die bestätigende Seite während der eingestellten Minuten halten.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Attempt-Grenzen werden beim Start eingefroren. Erst der Commit erzeugt Zähler-, Segment- und Markerfolgen atomar.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-09" data-modes="understand troubleshoot">

## Neutralzone und strikter Reset

<div markdown="1" class="fz-depth" data-depth="short">Jede Rückkehr in die Neutralzone verwirft den laufenden Timer sofort.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Kehrt der Markt nach zwei von fünf Minuten zurück, beginnt ein späterer Versuch wieder bei null. Im selben MIN1-Slot gibt es keinen verdeckten Neustart.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Der strikte Reset verhindert, dass oszillierende Tickbewegungen kumulativ eine Bestätigung erzeugen. Attempt- und Committed-Boundaries bleiben getrennt.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-10" data-modes="understand configure">

## Drei Bruchdistanz-Modi

<div markdown="1" class="fz-depth" data-depth="short">ATR passt sich Volatilität an, Percent skaliert mit dem Preis, Fixed ticks bleibt absolut.</div>

<div markdown="1" class="fz-depth" data-depth="practice">

| Modus | Sinnvoll für | Standardbeispiel |
|---|---|---|
| One-minute ATR | mehrere Timeframes und volatile Instrumente | 60 Minuten × 0,5, mindestens 2 Ticks |
| Percent of level | preisrelative Vergleichbarkeit | 0,05 %, mindestens 2 Ticks |
| Fixed ticks | exakt bekannte Ticklogik | 2 Ticks |

</div>

<div markdown="1" class="fz-depth" data-depth="technical">One-minute ATR wird aus der kanonischen MIN1-Reihe berechnet und nicht aus Chartkerzen. Percent verwendet den Levelpreis als Basis. Fixed ticks benötigt keine Volatilitätsreihe.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-11" data-modes="understand">

## Variable Tickraster und Quantisierung

<div markdown="1" class="fz-depth" data-depth="short">Die Grenze wird nach außen auf einen handelbaren Preis gerundet.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Bei einem Supportbruch wird die untere Grenze nicht versehentlich nach oben gerundet; bei einem Resistancebruch nicht nach unten.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Das aktive TickGrid kann preisabhängig sein. Outward-Quantisierung und Mindestticks werden in der richtigen Reihenfolge angewendet, sodass die effektive Distanz nie kleiner als gefordert wird.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-12" data-modes="understand configure">

## Bestätigungszeit und Cooldown

<div markdown="1" class="fz-depth" data-depth="short">Standard: 5 Minuten jenseits der Grenze und mindestens 5 Minuten zwischen committed breaks.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Die Bestätigung filtert kurze Ausreißer. Der Cooldown verhindert mehrere neue Brüche, wenn der Markt direkt am Level hin und her schwingt.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Cooldown startet erst am committed break, nicht am Attempt. Fehlgeschlagene Attempts erhöhen keinen committed counter.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-13" data-modes="understand">

## BrokenWatch und historische Fortsetzung

<div markdown="1" class="fz-depth" data-depth="short">Nach einem bestätigten Bruch läuft das Level ab dem Bruch gestrichelt weiter.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Dash bedeutet: „gebrochen, aber weiterhin für Retest und möglichen Rollenwechsel relevant“.</div>

<div markdown="1" class="fz-depth" data-depth="technical">BrokenWatch ist kein Endzustand. Retest- und Gegenbruchlogik bleiben aktiv; ein bestätigter Retest kann die Linie wieder als neues Solid-Segment aktivieren.</div>

</section>
