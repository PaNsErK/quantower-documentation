# Rendering, Marker und Historie einstellen

<section markdown="1" class="fz-topic" data-topic="FZT-30" data-modes="configure">

## Rendering und Marker konfigurieren

<div markdown="1" class="fz-depth" data-depth="short">Rendering verändert Darstellung, niemals Levelidentität oder Zustandsentscheidungen.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Teste Adaptive, Full und Active focus am selben Chart. Anzahl und Zeitgrenzen müssen identisch bleiben.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Render-Plan-Key bindet Generation, Viewport, Modus, Style und Annotationseinstellungen. Ein Cache-Hit darf keine Rebuild-Anforderung auslösen.</div>

</section>

<div class="fz-setting-card" id="setting-rendering-mode">

### Rendering mode · `RenderingMode`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Adaptive</div><div><strong>Optionen:</strong> Adaptive · Full · Active focus</div><div><strong>Sichtbar:</strong> immer</div></div>

Wählt den Darstellungsplan. Beispiel: Active focus ist für dichte Charts hilfreich, Full eignet sich als Referenzvergleich. Kein Modus darf Linien clustern, zusammenlegen oder unterdrücken.

</div>

<div class="fz-setting-card" id="setting-inactive-state-opacity">

### Inactive state opacity · `InactiveStateOpacity`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 0,35</div><div><strong>Bereich:</strong> 0,10–1,00</div><div><strong>Sichtbar:</strong> nur Active focus</div></div>

Deckkraft von Provisional und BrokenWatch in Active focus. Beispiel: 0,20 stellt aktive Solid-Segmente stärker heraus. Active wird nicht ausgeblendet.

</div>

<div class="fz-setting-card" id="setting-show-end-marker">

### Show end marker · `ShowEndMarker`

<div class="fz-setting-meta"><div><strong>Standard:</strong> true</div><div><strong>Typ:</strong> Boolean</div><div><strong>Sichtbar:</strong> immer</div></div>

Zeigt den exakten terminalen Endpunkt. Das Umschalten ist reine Darstellung und löst kein fachliches Replay aus.

</div>

<div class="fz-setting-card" id="setting-show-break-markers">

### Show break markers · `ShowBreakMarkers`

<div class="fz-setting-meta"><div><strong>Standard:</strong> false</div><div><strong>Typ:</strong> Boolean</div><div><strong>Sichtbar:</strong> immer</div></div>

Zeigt committed breaks. Standardmäßig aus, um dichte Charts nicht unnötig zu überladen.

</div>

<div class="fz-setting-card" id="setting-show-role-change-markers">

### Show role-change markers · `ShowRoleChangeMarkers`

<div class="fz-setting-meta"><div><strong>Standard:</strong> true</div><div><strong>Typ:</strong> Boolean</div><div><strong>Sichtbar:</strong> immer</div></div>

Markiert bestätigte RoleChanges. RoleReaffirmation und Rollenwechsel müssen semantisch unterscheidbar bleiben, auch wenn beide zu Active/Solid führen.

</div>

<section markdown="1" class="fz-topic" data-topic="FZT-31" data-modes="configure">

## Historie und Start konfigurieren

<div markdown="1" class="fz-depth" data-depth="short">Standard sind 90 Tage. Alternativ rechnet der Chartbereich plus automatischer Warm-up oder ein expliziter Start.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Für den normalen Vergleich 90 Tage belassen. Chart loaded range plus warm-up kann bei kurzem sichtbarem Ausschnitt schneller sein. Expliziter Start ist für reproduzierbare Untersuchungen.</div>

<div markdown="1" class="fz-depth" data-depth="technical">CalculationStartTime wird in Plattformzeit dargestellt, in UTC gebunden und deaktiviert InitialHistoryDays. Source-identical timeframe reuse verhindert unnötige Neuaufbauten.</div>

</section>

<div class="fz-setting-card" id="setting-calculation-range-mode">

### Calculation range mode · `CalculationRangeMode`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Fixed initial history days</div><div><strong>Optionen:</strong> Fixed · Chart loaded plus warm-up</div><div><strong>Sichtbar:</strong> immer</div></div>

Wählt die Startlogik. Beispiel: Ein 5‑Tage-Chart kann mit Chart loaded range plus warm-up nur den benötigten Ausschnitt und linken Warm-up berechnen.

</div>

<div class="fz-setting-card" id="setting-initial-history-days">

### Initial range (days) · `InitialHistoryDays`

<div class="fz-setting-meta"><div><strong>Standard:</strong> 90</div><div><strong>Bereich:</strong> 1–36.500</div><div><strong>Sichtbar:</strong> nur Fixed; bei explizitem Start deaktiviert</div></div>

Kalendertage zur Ableitung des initialen Rechenstarts. Beispiel: 365 erweitert historische Sicht, erhöht aber Bootstrap- und Speicherarbeit.

</div>

<div class="fz-setting-card" id="setting-calculation-start-time">

### Calculation start · `CalculationStartTime`

<div class="fz-setting-meta"><div><strong>Standard:</strong> deaktiviert</div><div><strong>Typ:</strong> DateTime mit Toggler</div><div><strong>Änderung:</strong> mit Bestätigung</div></div>

Expliziter deterministischer Start. Beispiel: Für einen Vergleich ab Monatsbeginn aktivieren und den sichtbaren Plattformzeitpunkt wählen. Intern wird UTC verwendet.

</div>

<section markdown="1" class="fz-topic" data-topic="FZT-32" data-modes="configure test">

## Checkpoint und Deep Verify bedienen

<div markdown="1" class="fz-depth" data-depth="short">Checkpoint beschleunigt optional; Deep Verify prüft die Historie asynchron und kann sicher abgebrochen werden.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Checkpoint erst in einem getrennten Restart-Test aktivieren. Verify nicht mehrfach klicken; der Single-Flight-Schutz antwortet sicher.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Restore ist hash-, StateIdentity- und ReplayGeneration-gebunden. Dirty Verify-Blöcke gehen durch denselben Offscreen-Replaypfad; ein sauberer Verify erzeugt keine neue Generation.</div>

</section>

<div class="fz-setting-card" id="setting-enable-replay-checkpoint">

### Enable semantic replay checkpoint · `EnableReplayCheckpoint`

<div class="fz-setting-meta"><div><strong>Standard:</strong> false</div><div><strong>Typ:</strong> Boolean</div><div><strong>Sichtbar:</strong> immer</div></div>

Aktiviert die semantische Sidecar- und Crash-Restore-Beschleunigung. Wichtig: Eine ältere Implementierungsnotiz nannte fälschlich `true`; der aktuelle Produktstandard ist eindeutig `false`.

</div>

<div class="fz-setting-card" id="setting-verify-full-history">

### Verify full history now… · `VerifyFullHistoryNow`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Action</div><div><strong>Ausführung:</strong> asynchron, Single-Flight</div><div><strong>Sichtbar:</strong> immer</div></div>

Startet eine Vollhistorienprüfung. Beispiel: Nach Datenanbieter-Revisionsverdacht einmal auslösen und Fortschritt/Diagnostik beobachten.

</div>

<div class="fz-setting-card" id="setting-cancel-full-history">

### Cancel full-history verify · `CancelFullHistoryVerify`

<div class="fz-setting-meta"><div><strong>Standard:</strong> Action</div><div><strong>Wirkung:</strong> nur optionaler manueller Verify</div><div><strong>Sichtbar:</strong> immer</div></div>

Fordert einen sicheren Abbruch an. Pflicht-Recovery wird niemals abgebrochen, und ein Teilresultat wird nicht als vollständige Generation veröffentlicht.

</div>
