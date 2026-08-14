# Performance und Sidecar diagnostizieren

<section markdown="1" class="fz-topic" data-topic="FZT-37" data-modes="troubleshoot">

## Performance, Sidecar und UI

<div markdown="1" class="fz-depth" data-depth="short">Trenne Rechenzeit, Rangewechsel, Paint, Speicher und Persistenzquote. Keine dieser Ebenen darf Linien semantisch reduzieren.</div>

<div markdown="1" class="fz-depth" data-depth="practice">

1. Vergleiche 7/30/90/365 Tage mit identischem Instrument und Modus.
2. Prüfe Rangewechsel und Pan/Zoom getrennt vom Rebuild.
3. Vergleiche Adaptive gegen Full auf identische Linien- und Markerzahl.
4. Prüfe Sidecar-Größe pro stabiler StateIdentity.
5. Bei `QuotaExceeded` beobachten, ob optionale Writes pausieren und später automatisch wieder anlaufen.

</div>

<div markdown="1" class="fz-depth" data-depth="technical">

FZPERF V2 sollte geschlossene Zähler für Canonical-Minute-Verarbeitung, Replay, Viewport-Kandidaten, gezeichnete Segmente, Cache-Hits und Paint-Dauer liefern. Sidecar-Defaults: 512 MiB je Identität, 1 GiB Live State je Prozess und 4 GiB je Root. Pruning schützt Current/Previous, aktive Generationen, Recovery-/Gap-Anker, Capsule-Boundaries, Bootstrap- und Dirty-Replay-Basen. Quota-Erholung nutzt Hysterese; `QuotaExceeded` reduziert nie berechnete oder dargestellte Linien.

</div>

</section>

## Wenn Active focus „weniger“ zeigt

Prüfe zuerst Deckkraft und Farbschema. Active focus darf Provisional und BrokenWatch nur transparenter machen, nicht entfernen. Wenn die Segmentzahl gegenüber Full abweicht, ist das ein Fehler und kein erwartetes Komfortverhalten.

## Wenn das Sidecar schnell wächst

Prüfe, ob StateIdentity bei reinem Timeframe- oder Viewportwechsel stabil bleibt. Unnötig wechselnde Identitäten verhindern Deduplizierung. Danach geschützte Wurzeln, Quarantäne, Orphan Grace und den letzten Prune-Grund prüfen.
