# Zeit- und Fraktallogik

Fractal Zones arbeitet intern mit kanonischen **Ein-Minuten-Session-Slots (MIN1)**. Der Chart-Zeitrahmen verändert weder Maturity noch Break-Timer. Ein 30/30-Fraktal benötigt 30 erwartete offene Minuten vor und nach dem Kandidaten – auf einem 1-, 5- oder 60-Minuten-Chart.

## Kandidat und Bestätigung

1. Ein Hoch oder Tief übertrifft die Werte der linken Maturity-Spanne.
2. Während der rechten Spanne ist das Level **Provisional** und gepunktet.
3. Erst nach vollständiger rechter Reife wird es **Active** und durchgezogen.
4. High und Low dürfen im selben Slot entstehen (`AmbiguousBothSides`); der Indikator rät keine Reihenfolge.

Gesperrte Sessionminuten zählen nicht. Datenlücken führen nicht still zu einer Verkürzung, sondern in den sichtbaren Recovery-Pfad.

## Beispiel

`Before=30`, `After=30`: Ein Kandidat um 10:00 benötigt gültige Session-Slots von ungefähr 09:30 bis 10:30. Erst danach wird das bisher gepunktete Segment beendet und ein neues Active/Solid-Segment begonnen; die Vergangenheit wird nicht rückwirkend umgezeichnet.

Weiter: [Maturity und Break konfigurieren](../configure/maturity-and-break.md).
