# Kontinuität und Wiederherstellung

<section markdown="1" class="fz-topic" data-topic="FZT-22" data-modes="understand troubleshoot">

## Datenkontinuität und Incomplete

<div markdown="1" class="fz-depth" data-depth="short">Eine begrenzte Datenlücke soll den Indikator nicht abstürzen lassen.</div>

<div markdown="1" class="fz-depth" data-depth="practice">`Incomplete` bedeutet: Für einen Teil der Historie fehlt belastbare Evidenz. Bereits vollständig publizierte Level bleiben stabil; unvollständige neue Ergebnisse werden nicht als vollständig ausgegeben.</div>

<div markdown="1" class="fz-depth" data-depth="technical">StrictFailClosed klassifiziert erwartete Slots, Datenbelege und Recoverability. SyntheticNoEvent darf Kontinuität ohne erfundene Preisereignisse abbilden.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-23" data-modes="understand troubleshoot">

## SuspendedByDataGap und Epoch

<div markdown="1" class="fz-depth" data-depth="short">Eine relevante Lücke suspendiert betroffene Weiterrechnung, nicht die gesamte Oberfläche.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Nach Datenrückkehr startet genau ein kontrollierter Recoverypfad mit Backoff. Eine neue ContinuityDataEpoch trennt die reparierte Generation klar von der alten.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Retry ist Single-Flight. Epoch-Wechsel verhindern, dass spät eintreffende Ergebnisse einer alten Datenbasis eine neue Generation überschreiben.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-24" data-modes="understand troubleshoot">

## Offscreen-Replay und Generation-Swap

<div markdown="1" class="fz-depth" data-depth="short">Reparatur wird vollständig im Hintergrund aufgebaut und erst danach atomar sichtbar.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Während des Replays bleibt die zuletzt gültige Generation sichtbar. Ein teilweises Ergebnis ersetzt sie nie.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Vor Publish werden SourceRevisionToken und LedgerRoot erneut geprüft. Drift verwirft das Ergebnis. Ein erfolgreicher Swap erhält eine neue ReplayGeneration.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-25" data-modes="understand troubleshoot">

## Sidecar, Restore-Kette und Quoten

<div markdown="1" class="fz-depth" data-depth="short">Restore-Reihenfolge: Current → Previous → jüngster gültiger geschützter Restore Point → Rohneuaufbau.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Checkpointing ist standardmäßig aus. Aktiviert beschleunigt es Neustarts, darf aber niemals eine ungültige oder fremde StateIdentity übernehmen. Die aktuellen Persistenzstandards sind 512 MiB je Identität und 4 GiB je Sidecar-Root.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Content-addressed Storage, kanonisches Streaming-JSON, Hash- und StateIdentity-Bindung, Current/Previous-Crashrotation, geschützte Wurzeln und Reachability-Pruning bilden den fail-closed Speichervertrag. `QuotaExceeded` pausiert optionale Restore-Point-Schreibvorgänge; Berechnung und Darstellung laufen weiter.</div>

</section>
