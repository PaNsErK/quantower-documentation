# Lifecycle und Linien einstellen

<section markdown="1" class="fz-topic" data-topic="FZT-28" data-modes="configure">

## Lifecycle konfigurieren

<div markdown="1" class="fz-depth" data-depth="short">Retestdauer bestätigt Rollenentscheidungen; die terminale Bruchzahl begrenzt die Lebensdauer der aktuellen Rolle.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Standard 5 Minuten und Ende beim dritten current-role break ergeben einen gut nachvollziehbaren Ablauf ohne sofortiges Verschwinden.</div>

<div markdown="1" class="fz-depth" data-depth="technical">RoleChange setzt `CurrentRoleBreakCount` zurück, `LifetimeBreakCount` nie. Der terminale Commit erfolgt vor Ended.</div>

</section>

<div class="fz-setting-card" id="setting-retest-confirmation-minutes">

### Retest confirmation (minutes) · `RetestConfirmationMinutes`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 5 min</div><div><strong>Bereich:</strong> 1–43.200</div><div><strong>Sichtbar:</strong> immer</div></div>

Bestätigungsdauer nach einem realen geschlossenen Bar-Kontakt. Beispiel: Berührt der Markt das Level und hält die neue Seite fünf offene Minuten, wird RoleChange oder RoleReaffirmation committed.

</div>

<div class="fz-setting-card" id="setting-terminate-current-role-break">

### End on current-role break number · `TerminateOnCurrentRoleBreakNumber`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 3</div><div><strong>Bereich:</strong> 1–1.000</div><div><strong>Sichtbar:</strong> immer</div></div>

Beendet die Linie beim angegebenen committed break der aktuellen Rolle. Beispiel: Wert 1 beendet sofort beim ersten Rollenbruch; Wert 3 erlaubt vorher zwei historische Beobachtungsphasen.

</div>

<section markdown="1" class="fz-topic" data-topic="FZT-29" data-modes="configure">

## Linienstile konfigurieren

<div markdown="1" class="fz-depth" data-depth="short">Jeder Zustand hat getrennte Top- und Bottom-LineOptions: Style, Breite und Farbe.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Defaults: Provisional Dot, Active Solid, Historical Dash; Top Grün, Bottom Rot; überall Breite 1.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Zulässige Styles sind `Solid`, `Dash`, `Dot` und `DashDot`. Histogramm, Points, Columns und StepLine werden absichtlich ausgefiltert.</div>

</section>

<div class="fz-setting-card" id="setting-provisional-top-line">

### Provisional · Top line options · `ProvisionalTopLineOptions`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Dot · 1 · Green</div><div><strong>Controls:</strong> Style · Breite · Color Picker</div><div><strong>Sichtbar:</strong> immer</div></div>

Steuert nur provisorische Top-Ursprungslinien. Beispiel: Breite 2 macht Kandidaten deutlicher, ändert aber keine Bestätigung.

</div>

<div class="fz-setting-card" id="setting-provisional-bottom-line">

### Provisional · Bottom line options · `ProvisionalBottomLineOptions`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Dot · 1 · Red</div><div><strong>Controls:</strong> Style · Breite · Color Picker</div><div><strong>Sichtbar:</strong> immer</div></div>

Steuert nur provisorische Bottom-Ursprungslinien. Farbe bleibt bei späterem Rollenwechsel ursprungsstabil.

</div>

<div class="fz-setting-card" id="setting-active-top-line">

### Active · Top line options · `ActiveTopLineOptions`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Solid · 1 · Green</div><div><strong>Controls:</strong> Style · Breite · Color Picker</div><div><strong>Sichtbar:</strong> immer</div></div>

Steuert bestätigte aktive Top-Ursprungslinien. Beispiel: Solid 2 kann für wichtige aktive Level gewählt werden.

</div>

<div class="fz-setting-card" id="setting-active-bottom-line">

### Active · Bottom line options · `ActiveBottomLineOptions`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Solid · 1 · Red</div><div><strong>Controls:</strong> Style · Breite · Color Picker</div><div><strong>Sichtbar:</strong> immer</div></div>

Steuert bestätigte aktive Bottom-Ursprungslinien, unabhängig davon, ob ihre aktuelle Rolle Support oder Resistance ist.

</div>

<div class="fz-setting-card" id="setting-historical-top-line">

### Historical · Top line options · `HistoricalTopLineOptions`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Dash · 1 · Green</div><div><strong>Controls:</strong> Style · Breite · Color Picker</div><div><strong>Sichtbar:</strong> immer</div></div>

Steuert Top-Ursprungslinien in BrokenWatch. Dash signalisiert „gebrochen, weiter beobachtet“.

</div>

<div class="fz-setting-card" id="setting-historical-bottom-line">

### Historical · Bottom line options · `HistoricalBottomLineOptions`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Dash · 1 · Red</div><div><strong>Controls:</strong> Style · Breite · Color Picker</div><div><strong>Sichtbar:</strong> immer</div></div>

Steuert Bottom-Ursprungslinien in BrokenWatch. Ein bestätigter Retest beginnt ab dem Commit wieder ein Active-Solid-Segment.

</div>

!!! note "Kein Ended-Stil"
    Ended besitzt keine LineOptions. Die Linie endet vollständig am `EndTimeUtc`; nur der optionale Endmarker kann sichtbar bleiben.
