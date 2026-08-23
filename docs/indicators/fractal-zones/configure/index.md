# Alle Einstellungen

Diese Referenz ist das vollständige aktuelle Inventar der **56 produktseitigen Einstellungszeilen**. Sie umfasst sieben LineOptions, 70 atomare Controls und zwei Aktionen. Die geerbten Quantower-Basisfelder stehen separat unter [Inventarstatus](../inventory-status.md).

**Leseregel:** Standard ist der Wert einer neuen Instanz. Sichtbarkeit nennt den aktiven UI-Zweig. LineOptions enthalten Stil, Breite und Farbe.

| Gruppe | Einstellung | Typ | Standard | Bereich / Optionen | Sichtbarkeit |
|---|---|---|---|---|---|
<span id=setting-maturity-before-minutes></span>| Fractal Maturity | **Before (minutes)** (MaturityBeforeMinutes) | integer | 30 | 1–43.200 Minuten; Schritt 1 | immer |
<span id=setting-maturity-after-minutes></span>| Fractal Maturity | **After (minutes)** (MaturityAfterMinutes) | integer | 30 | 1–43.200 Minuten; Schritt 1 | immer |
<span id=setting-break-distance-mode></span>| Break Engine | **Break distance mode** (BreakDistanceMode) | selector | One-minute ATR | One-minute ATR | Percent of level | Fixed ticks | immer |
<span id=setting-break-price-source></span>| Break Engine | **Break price source** (BreakPriceSource) | selector | Close | Close | High/Low | immer |
<span id=setting-atr-period-minutes></span>| Break Engine | **ATR period (minutes)** (AtrPeriodMinutes) | integer | 60 | 1–43.200 Minuten; Schritt 1 | nur One-minute ATR |
<span id=setting-break-atr-multiplier></span>| Break Engine | **ATR multiplier** (BreakAtrMultiplier) | double | 0,5 | 0–1.000.000; Schritt 0,05; 2 Dezimalstellen | nur One-minute ATR |
<span id=setting-minimum-break-distance-ticks></span>| Break Engine | **Minimum break distance (ticks)** (MinimumBreakDistanceTicks) | integer | 2 | 0–1.000.000 Ticks; Schritt 1 | One-minute ATR oder Percent of level |
<span id=setting-break-distance-percent></span>| Break Engine | **Break distance (%)** (BreakDistancePercent) | double | 0,05 | 0–100 %; Schritt 0,01; 2 Dezimalstellen | nur Percent of level |
<span id=setting-fixed-break-distance-ticks></span>| Break Engine | **Fixed break distance (ticks)** (FixedBreakDistanceTicks) | integer | 2 | 0–1.000.000 Ticks; Schritt 1 | nur Fixed ticks |
<span id=setting-break-confirmation-minutes></span>| Break Engine | **Break confirmation (minutes)** (BreakConfirmationMinutes) | integer | 5 | 0–43.200 Minuten; Schritt 1 | immer |
<span id=setting-minimum-minutes-between-breaks></span>| Break Engine | **Minimum between breaks (minutes)** (MinimumMinutesBetweenBreaks) | integer | 5 | 0–43.200 Minuten; Schritt 1 | immer |
<span id=setting-retest-confirmation-minutes></span>| Lifecycle | **Retest confirmation (minutes)** (RetestConfirmationMinutes) | integer | 5 | 1–43.200 offene Sessionminuten | immer |
<span id=setting-terminate-current-role-break></span>| Lifecycle | **End on current-role break number** (TerminateOnCurrentRoleBreakNumber) | integer | 3 | 1–1.000; Schritt 1 | immer |
<span id=setting-show-provisional-lines></span>| Line Settings (provisional level) | **Show provisional lines** (ShowProvisionalLines) | boolean | an | true | false | immer |
<span id=setting-provisional-top-line></span>| Line Settings (provisional level) | **Top line options** (ProvisionalTopLineOptions) | line_options | Dot | 1 | Green | Solid | Dash | Dot | DashDot; Breite 1–10; Color Picker | immer |
<span id=setting-provisional-bottom-line></span>| Line Settings (provisional level) | **Bottom line options** (ProvisionalBottomLineOptions) | line_options | Dot | 1 | Red | Solid | Dash | Dot | DashDot; Breite 1–10; Color Picker | immer |
<span id=setting-active-top-line></span>| Line Settings (active level) | **Top line options** (ActiveTopLineOptions) | line_options | Solid | 1 | Green | Solid | Dash | Dot | DashDot; Breite 1–10; Color Picker | immer |
<span id=setting-active-bottom-line></span>| Line Settings (active level) | **Bottom line options** (ActiveBottomLineOptions) | line_options | Solid | 1 | Red | Solid | Dash | Dot | DashDot; Breite 1–10; Color Picker | immer |
<span id=setting-show-break-boundary-line></span>| Current break boundary | **Show current break boundary** (ShowBreakBoundaryLine) | boolean | aus | true | false | immer |
<span id=setting-break-boundary-line></span>| Current break boundary | **Break boundary line options** (BreakBoundaryLineOptions) | line_options | Dot | 1 | Yellow | Solid | Dash | Dot | DashDot; Breite 1–10; Color Picker | immer |
<span id=setting-break-boundary-connector></span>| Current break boundary | **Connect boundary to main line** (ShowBreakBoundaryConnector) | boolean | aus | true | false | immer |
<span id=setting-show-historical-lines></span>| Line Settings (historically continued level) | **Show historical lines** (ShowHistoricalLines) | boolean | an | true | false | immer |
<span id=setting-historical-top-line></span>| Line Settings (historically continued level) | **Top line options** (HistoricalTopLineOptions) | line_options | Dash | 1 | Green | Solid | Dash | Dot | DashDot; Breite 1–10; Color Picker | immer |
<span id=setting-historical-bottom-line></span>| Line Settings (historically continued level) | **Bottom line options** (HistoricalBottomLineOptions) | line_options | Dash | 1 | Red | Solid | Dash | Dot | DashDot; Breite 1–10; Color Picker | immer |
<span id=setting-rendering-mode></span>| Rendering | **Rendering mode** (RenderingMode) | selector | Adaptive | Adaptive | Full | Active focus | immer |
<span id=setting-inactive-state-opacity></span>| Rendering | **Inactive state opacity** (InactiveStateOpacity) | double | 0,35 | 0,10–1,00; Schritt 0,05; 2 Dezimalstellen | nur Active focus |
<span id=setting-show-status-overlay></span>| Rendering | **Show status overlay** (ShowStatusOverlay) | boolean | an | true | false | immer |
<span id=setting-enable-price-filter></span>| Rendering | **Limit rendering to current-price range** (EnablePriceRelevanceFilter) | boolean | aus | true | false | immer |
<span id=setting-price-relevance-percent></span>| Rendering | **Current-price range (+/- %)** (PriceRelevancePercent) | double | 10 | 0–10.000 %; Schritt 0,5; 2 Dezimalstellen | nur wenn Preisfilter aktiv |
<span id=setting-open-line-mode></span>| Rendering | **Open line end** (OpenLineProjectionMode) | selector | Current bar end | Current bar end | Minutes | Chart candles | immer |
<span id=setting-open-line-minutes></span>| Rendering | **Projection (minutes)** (OpenLineProjectionMinutes) | integer | 30 | 1–10.080 Minuten; Schritt 1 | nur Open line end = Minutes |
<span id=setting-open-line-candles></span>| Rendering | **Projection (chart candles)** (OpenLineProjectionCandles) | integer | 3 | 1–500 zeitbasierte Chartkerzen; Schritt 1 | nur Open line end = Chart candles |
<span id=setting-show-end-marker></span>| Markers | **Show end marker** (ShowEndMarker) | boolean | an | true | false | immer |
<span id=setting-end-marker-color></span>| Markers | **End marker color** (TerminationMarkerColor) | color | OrangeRed | Color Picker | immer |
<span id=setting-show-break-markers></span>| Markers | **Show break markers** (ShowBreakMarkers) | boolean | aus | true | false | immer |
<span id=setting-break-marker-color></span>| Markers | **Break marker color** (BreakMarkerColor) | color | Goldenrod | Color Picker | immer |
<span id=setting-show-role-change-markers></span>| Markers | **Show role-change markers** (ShowRoleChangeMarkers) | boolean | an | true | false | immer |
<span id=setting-role-marker-color></span>| Markers | **Role-change marker color** (RoleMarkerColor) | color | DodgerBlue | Color Picker | immer |
<span id=setting-show-markers-at-event></span>| Markers | **Show markers at event** (ShowMarkersAtEvent) | boolean | an | true | false | immer |
<span id=setting-show-markers-at-line-end></span>| Markers | **Show markers at line end** (ShowMarkersAtLineEnd) | boolean | aus | true | false | immer |
<span id=setting-event-marker-offset-mode></span>| Markers | **Event marker X offset mode** (EventMarkerOffsetMode) | selector | DPI pixels | DPI pixels | Chart candles | immer |
<span id=setting-event-marker-offset-x></span>| Markers | **Event marker X offset** (EventMarkerOffsetX) | integer | 0 | -200–200 DPI-Pixel oder Chartkerzen | immer; Einheit folgt Event-X-Modus |
<span id=setting-event-marker-offset-y></span>| Markers | **Event marker Y offset** (EventMarkerOffsetY) | integer | 0 | -200–200 DPI-Pixel | immer |
<span id=setting-line-end-marker-offset-mode></span>| Markers | **Line-end marker X offset mode** (LineEndMarkerOffsetMode) | selector | Chart candles | DPI pixels | Chart candles | immer |
<span id=setting-line-end-marker-offset-x></span>| Markers | **Line-end marker X offset** (LineEndMarkerOffsetX) | integer | 1 | -200–200 DPI-Pixel oder Chartkerzen | immer; Einheit folgt Line-end-X-Modus |
<span id=setting-line-end-marker-offset-y></span>| Markers | **Line-end marker Y offset** (LineEndMarkerOffsetY) | integer | 0 | -200–200 DPI-Pixel | immer |
<span id=setting-event-marker-font-size></span>| Markers | **Event marker font size** (EventMarkerFontSize) | integer | 0 | 0 = Hostschrift; sonst 6–32 pt | immer |
<span id=setting-line-end-marker-font-size></span>| Markers | **Line-end marker font size** (LineEndMarkerFontSize) | integer | 0 | 0 = Hostschrift; sonst 6–32 pt | immer |
<span id=setting-calculation-range-mode></span>| History | **Calculation range mode** (CalculationRangeMode) | selector | Chart loaded range plus warm-up | Fixed lookback days | Fixed calculation start | Chart loaded range plus warm-up | immer |
<span id=setting-initial-history-days></span>| History | **Fixed lookback (days)** (InitialHistoryDays) | integer | 90 | 1–36.500 Kalendertage; Schritt 1 | nur Fixed lookback days |
<span id=setting-calculation-start-time></span>| History | **Calculation start** (CalculationStartTime) | datetime | unset | Plattformzeitzone; intern UTC; Änderung mit Bestätigung | nur Fixed calculation start |
<span id=setting-warmup-mode></span>| History | **Warm-up mode** (WarmupMode) | selector | Automatic | Automatic | Manual | nur Chart loaded range plus warm-up |
<span id=setting-additional-warmup-days></span>| History | **Additional warm-up (days)** (AdditionalWarmupDays) | integer | 0 | 0–3.650 Kalendertage; Schritt 1 | nur Chart loaded range plus warm-up + Manual |
<span id=setting-enable-replay-checkpoint></span>| History | **Enable semantic replay checkpoint** (EnableReplayCheckpoint) | boolean | an | true | false | immer |
<span id=setting-verify-full-history></span>| History | **Verify full history now…** (VerifyFullHistoryNow) | action | action | asynchron, Single-Flight, Fortschritt und sicherer Cancel | immer |
<span id=setting-cancel-full-history></span>| History | **Cancel full-history verify** (CancelFullHistoryVerify) | action | action | beendet nur den optionalen manuellen Verify | immer |

## Schnelle Wege

- [Maturity und Break Engine](maturity-and-break.md): Fraktalerkennung, Preisquelle, Distanz, Timer und Cooldown.
- [Lifecycle und Linien](lifecycle-and-lines.md): Retest, Rollenwechsel, Ende, Stile und Break-Boundary.
- [Rendering, Marker und Historie](rendering-and-history.md): Anzeige, Projektion, Marker, Range, Warm-up und Deep Verify.

## Wichtigste Regeln

- Reine Anzeigeoptionen verändern keine Levelidentität und starten keinen semantischen Replay.
- Semantische Einstellungen erzeugen eine neue Settings-Generation; die letzte gute Projektion bleibt bis zum atomaren Publish sichtbar.
- Null ist bei Break-Distanz und Break-Bestätigung absichtlich gültig.
- Linien werden nicht geclustert, zusammengelegt, gesampelt oder unterdrückt. Der optionale Preisfilter ist eine reversible Anzeigeabfrage.
