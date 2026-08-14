# Zustandsablauf

--8<-- "docs/includes/diagrams/lifecycle.md"

<section markdown="1" class="fz-topic" data-topic="FZT-05" data-modes="understand">

## Candidate und Provisional

<div markdown="1" class="fz-depth" data-depth="short">Sobald die linke Reife und das strikte Extrem erfüllt sind, entsteht eine sichtbare provisorische Dot-Linie.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Die Linie darf noch verschwinden, wenn rechts innerhalb der Nachlaufzeit ein höheres Top oder tieferes Bottom entsteht. Dot bedeutet deshalb: „sichtbarer Kandidat, noch nicht bestätigt“.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Candidate und Provisional sind fachlich getrennt: Der Kandidat ist die erkannte Extremstelle, Provisional deren vorläufige Chartprojektion. Die Projektion darf keine spätere Bestätigung vorwegnehmen.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-06" data-modes="understand configure">

## Maturity before und after

<div markdown="1" class="fz-depth" data-depth="short">`before` prüft die Zeit links, `after` die Zeit rechts. Beide sind unabhängig konfigurierbar.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Symmetrische 30/30 Minuten sind der Standard. 30/15 reagiert früher, akzeptiert rechts aber weniger Bestätigung. 60/30 verlangt links mehr Marktgeschichte, bestätigt rechts aber weiterhin relativ schnell.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Eine asymmetrische Konfiguration ist erlaubt und deterministisch, solange beide Seiten erwartete offene Sessionminuten zählen. Der Start-Warm-up muss mindestens den linken Reifehorizont plus technische Abhängigkeiten abdecken.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-07" data-modes="understand test">

## Segmenttreue Bestätigung

<div markdown="1" class="fz-depth" data-depth="short">Nach Bestätigung wird nur die Zukunft solid. Die vergangene provisorische Strecke bleibt Dot.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Das verhindert Rückschauverzerrung: Du siehst im Chart weiterhin, wann der Markt das Level tatsächlich noch nicht kennen konnte.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Die Statusänderung erzeugt eine neue Segmentgrenze am Bestätigungszeitpunkt. Ein rückwirkendes Umschreiben des bestehenden Segments ist verboten.</div>

</section>

## Kompakte Zustandsfolge

`Candidate → Provisional/Dot → Active/Solid → BreakPending (intern) → BrokenWatch/Dash → RetestPending (intern) → Active/Solid → Ended`
