# Daten, Start und Projektion diagnostizieren

<section markdown="1" class="fz-topic" data-topic="FZT-36" data-modes="troubleshoot">

## Leere Projektion und Datenlücken

<div markdown="1" class="fz-depth" data-depth="short">Leere Linien bedeuten nicht automatisch einen Paint-Fehler. Zuerst Bootstrap, History, Session und Projection prüfen.</div>

<div markdown="1" class="fz-depth" data-depth="practice">

| Beobachtung | Wahrscheinliche Ebene | Nächste sichere Prüfung |
|---|---|---|
| `CalculationStartUnavailable` | Start/Session | Startmodus, Plattformzeit und Sessionkalender prüfen |
| `Incomplete` | History | Fehlende Slot-Evidenz und Recovery-Zustand prüfen |
| `SuspendedByDataGap` | Continuity | Retry/Backoff und Epoch-Marker beobachten |
| Segmente = 0 bei Complete | Fraktal/Range | Maturity, Zeitraum und strikte Extreme prüfen |
| Segmente > 0, nichts sichtbar | Projektion/Paint | Viewport, Render-Plan und LastPaintOutcome prüfen |

</div>

<div markdown="1" class="fz-depth" data-depth="technical">

Ein erlaubter Diagnoseauszug besteht nur aus geschlossenem Status, Zählern und sanitisierten Präfixen wie FZDIAG/FZCONT. Unknown oder widersprüchlicher Evidence-State ist kein PASS. Ein fehlgeschlagener Bootstrap darf die Hostoberfläche nicht werfen oder blockieren; er bleibt recoverable und gedrosselt.

</div>

</section>

## Kein Absturz bei gelegentlicher Datenungenauigkeit

`Incomplete` ist ein Datenqualitätszustand, kein globaler Programmabbruch. Die zuletzt vollständig publizierte Generation bleibt nutzbar. Erst nach vollständigem Replay und erneuter Source-Prüfung wird atomar umgeschaltet.
