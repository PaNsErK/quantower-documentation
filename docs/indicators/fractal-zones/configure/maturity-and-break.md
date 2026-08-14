# Maturity und Break Engine einstellen

<section markdown="1" class="fz-topic" data-topic="FZT-26" data-modes="configure">

## Maturity konfigurieren

<div markdown="1" class="fz-depth" data-depth="short">30/30 Minuten ist ein ausgewogener Start. Kleinere Werte reagieren schneller, größere Werte filtern stärker.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Ändere vor und nach einem Vergleich immer nur eine Seite. Prüfe danach denselben Marktabschnitt auf mehreren Chart-Timeframes.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Die Werte zählen erwartete offene Sessionminuten. Sie skalieren nicht mit der Chartkerzengröße.</div>

</section>

<div class="fz-setting-card" id="setting-maturity-before-minutes">

### Before (minutes) · `MaturityBeforeMinutes`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 30 min</div><div><strong>Bereich:</strong> 1–43.200</div><div><strong>Sichtbar:</strong> immer</div></div>

Legt fest, wie viele erwartete offene Sessionminuten **vor** dem Kandidaten für das strikte Extrem betrachtet werden. Beispiel: 60 verlangt eine längere linke Einordnung und erzeugt meist weniger Kandidaten als 30.

Technik: semantisches Setting; eine Änderung erfordert Replay ab dem passenden Warm-up.

</div>

<div class="fz-setting-card" id="setting-maturity-after-minutes">

### After (minutes) · `MaturityAfterMinutes`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 30 min</div><div><strong>Bereich:</strong> 1–43.200</div><div><strong>Sichtbar:</strong> immer</div></div>

Legt die Bestätigungsdauer **nach** dem Kandidaten fest. Beispiel: 15 bestätigt früher als 30, akzeptiert aber weniger rechte Marktstruktur.

Technik: Die Provisional-Linie bleibt bis zum vollständigen rechten Zeitfenster gepunktet.

</div>

<section markdown="1" class="fz-topic" data-topic="FZT-27" data-modes="configure">

## Break Engine konfigurieren

<div markdown="1" class="fz-depth" data-depth="short">Wähle zuerst den Distanzmodus, dann dessen Parameter, danach Bestätigungszeit und Cooldown.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Für instrument- und timeframeübergreifende Nutzung ist One-minute ATR der Standard. Percent und Fixed ticks bleiben bewusste Alternativen.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Der Modus bestimmt den Rohabstand. Mindestticks, variables TickGrid und outward quantization erzeugen daraus die committed boundary.</div>

</section>

<div class="fz-setting-card" id="setting-break-distance-mode">

### Break distance mode · `BreakDistanceMode`

<div class="fz-setting-meta"><div><strong>Standard:</strong> One-minute ATR</div><div><strong>Optionen:</strong> ATR · Percent · Fixed ticks</div><div><strong>Sichtbar:</strong> immer</div></div>

Bestimmt, wie weit der Preis über das Level hinauslaufen muss. Beispiel: Für ein Portfolio aus ES, Gold und BTC ist ATR meist vergleichbarer; für eine feste Mikrostruktur kann Fixed ticks sinnvoller sein.

</div>

<div class="fz-setting-card" id="setting-atr-period-minutes">

### ATR period (minutes) · `AtrPeriodMinutes`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 60</div><div><strong>Bereich:</strong> 1–43.200</div><div><strong>Sichtbar:</strong> nur ATR</div></div>

Zeitfenster der One-minute ATR. Beispiel: 60 reagiert auf die jüngste Stunde offener Sessiondaten; 240 glättet stärker.

</div>

<div class="fz-setting-card" id="setting-break-atr-multiplier">

### ATR multiplier · `BreakAtrMultiplier`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 0,5</div><div><strong>Bereich:</strong> 0,000001–1.000.000</div><div><strong>Sichtbar:</strong> nur ATR</div></div>

Multipliziert die zeitnormalisierte ATR. Beispiel: ATR 8 Punkte × 0,5 ergibt 4 Punkte Rohabstand, bevor Mindestticks und Quantisierung greifen.

</div>

<div class="fz-setting-card" id="setting-minimum-break-distance-ticks">

### Minimum break distance (ticks) · `MinimumBreakDistanceTicks`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 2</div><div><strong>Bereich:</strong> 1–1.000.000</div><div><strong>Sichtbar:</strong> ATR oder Percent</div></div>

Schützt vor zu kleinen relativen Abständen. Beispiel: Ergibt ATR oder Prozent nur 0,7 Tick, werden mindestens 2 Ticks verlangt.

</div>

<div class="fz-setting-card" id="setting-break-distance-percent">

### Break distance (%) · `BreakDistancePercent`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 0,05 %</div><div><strong>Bereich:</strong> 0,000001–100</div><div><strong>Sichtbar:</strong> nur Percent</div></div>

Berechnet den Rohabstand relativ zum Level. Beispiel: Bei 20.000 Punkten entsprechen 0,05 % genau 10 Punkten, vorbehaltlich Tickquantisierung.

</div>

<div class="fz-setting-card" id="setting-fixed-break-distance-ticks">

### Fixed break distance (ticks) · `FixedBreakDistanceTicks`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 2</div><div><strong>Bereich:</strong> 1–1.000.000</div><div><strong>Sichtbar:</strong> nur Fixed ticks</div></div>

Verwendet immer die feste Anzahl Ticks. Beispiel: Bei Tickgröße 0,25 bedeuten 2 Ticks einen Abstand von 0,50 Preiseinheiten.

</div>

<div class="fz-setting-card" id="setting-break-confirmation-minutes">

### Break confirmation (minutes) · `BreakConfirmationMinutes`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 5 min</div><div><strong>Bereich:</strong> 1–43.200</div><div><strong>Sichtbar:</strong> immer</div></div>

Wie lange die bestätigende Seite gehalten werden muss. Beispiel: Ein 3‑Minuten-Ausflug bei Wert 5 bleibt ein fehlgeschlagener Attempt.

</div>

<div class="fz-setting-card" id="setting-minimum-minutes-between-breaks">

### Minimum between breaks (minutes) · `MinimumMinutesBetweenBreaks`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 5 min</div><div><strong>Bereich:</strong> 0–43.200</div><div><strong>Sichtbar:</strong> immer</div></div>

Cooldown zwischen committed breaks derselben Linie. Beispiel: Nach einem Bruch um 10:00 kann vor 10:05 kein weiterer committed break gezählt werden.

</div>

!!! tip "Sicherer Vergleich"
    Für einen sauberen A/B-Test zuerst nur `BreakDistanceMode` und dessen sichtbare Parameter ändern. Bestätigungszeit und Cooldown unverändert lassen.
