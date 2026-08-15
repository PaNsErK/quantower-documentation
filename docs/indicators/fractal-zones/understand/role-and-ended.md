# Retest, Rollenwechsel und Ende

--8<-- "docs/includes/diagrams/role-change.md"

## Interaktives Chartlabor: Retest, Rolle und Ende

Schalte zwischen den fachlich unterschiedlichen Ergebnissen um und gehe den Ablauf schrittweise durch. Entscheidend ist nicht nur, wo der Kurs liegt, sondern welches Ereignis bereits bestätigt wurde.

<div class="fz-simulator" data-fz-simulator="role-ended">
<p><strong>Ohne JavaScript:</strong> RoleChange ändert die aktuelle Rolle, RoleReaffirmation bestätigt sie. Re-arm verhindert Doppelbestätigungen; Ended beendet die Linie exakt am terminalen Commit.</p>
</div>

*Realitätsnahes synthetisches Szenario; keine Live-, Konto- oder Handelsdaten.*

<section markdown="1" class="fz-topic" data-topic="FZT-14" data-modes="understand">

## RetestPending und Re-arm

<div markdown="1" class="fz-depth" data-depth="short">Nur der Kontakt einer realen geschlossenen Bar startet einen Retest.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Der Markt muss die neue Seite für die eingestellte Retestdauer bestätigen. Eine Rückkehr in die Neutralzone setzt auch diesen Timer strikt zurück.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Synthetische NoEvent-Slots dürfen Zeit fortschreiben, aber keinen Preis-Kontakt erzeugen. Re-arm verhindert sofortige Mehrfachbestätigung desselben Kontakts.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-15" data-modes="understand">

## RoleChange und RoleReaffirmation

<div markdown="1" class="fz-depth" data-depth="short">Beide machen die Linie wieder Active/Solid; nur RoleChange ändert die aktuelle Rolle.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Wird ehemaliger Support nach Bruch von unten bestätigt, kann er Resistance werden. Bestätigt ein Retest dieselbe Rolle, ist es eine RoleReaffirmation.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Bei echtem RoleChange wird `CurrentRoleBreakCount` zurückgesetzt. `LifetimeBreakCount` bleibt erhalten. RoleReaffirmation setzt den Rollen-Zähler nicht durch eine künstliche Rollenänderung zurück.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-16" data-modes="understand troubleshoot">

## Zähler und Gegenbruch-Priorität

<div markdown="1" class="fz-depth" data-depth="short">Lifetime zählt alle committed breaks; CurrentRole nur die Brüche der aktuellen Rolle.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Ein Gegenbruch, der während eines Retestversuchs bestätigt wird, gewinnt nach der festgelegten Reducer-Priorität. Dadurch entstehen keine zwei widersprüchlichen Zustände im selben Slot.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Commit-Reihenfolge: eingefrorene Grenze prüfen, Break atomar committen, Zähler aktualisieren, Terminalregel prüfen und erst danach eine mögliche Ended-Projektion setzen.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-17" data-modes="understand test">

## Ended und exaktes Linienende

<div markdown="1" class="fz-depth" data-depth="short">Beim konfigurierten current-role break endet die Linie exakt am Commit-Zeitpunkt.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Mit Standardwert 3 sind zwei weitere Beobachtungen möglich. Der dritte committed Bruch der aktuellen Rolle beendet die Linie vollständig.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Ended ist terminal und unveränderlich. Es existiert bewusst kein Ended-LineStyle: Nach `EndTimeUtc` wird kein Liniensegment gezeichnet; optional bleibt nur der Endmarker.</div>

</section>
