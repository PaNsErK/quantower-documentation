# Offene Benutzer-Testmatrix

`manual_acceptance_complete=false` · `pending_user_evaluation`

Diese 19 Fälle prüfen visuelle Lesbarkeit, Bedienbarkeit und subjektive Erwartung der aktuellen V2-Oberfläche. Sie wurden absichtlich nicht aus automatisierten oder älteren FZMT-Ergebnissen vorausgefüllt.

<div data-manual-test-suite="fzv2-remediation-v1"></div>

## Ergebnisregel

Ein Fall erhält erst durch deine tatsächliche Beobachtung `pass`, `fail`, `blocked` oder `improvement`. Export und Import bleiben lokal und suitespezifisch. Die technische Runtime-Abnahme bleibt davon getrennt.

<div class="fz-safety" role="note"><strong>Lokale, nicht-tradende Testhilfe:</strong> Status und Notizen bleiben im Browserprofil. Keine Konto-, Order-, Positions-, Pfad-, Prozess- oder Logdaten eintragen.</div>

<noscript><p>JavaScript ist deaktiviert. Die Inhalte bleiben lesbar; Fortschritt und Export benötigen lokales JavaScript.</p></noscript>

<div class="fz-test-toolbar">
  <div><label for="fz-test-progress"><strong>Fortschritt</strong></label><progress class="fz-progress" id="fz-test-progress" value="0"></progress><span id="fz-test-progress-text"></span></div>
  <label><input type="checkbox" id="fz-export-notes"> Notizen beim Export einschließen</label>
</div>
<div class="fz-test-actions" role="group" aria-label="Testdatenaktionen">
  <button class="fz-button" id="fz-export-json" type="button">JSON exportieren</button>
  <button class="fz-button" id="fz-export-markdown" type="button">Markdown exportieren</button>
  <label class="fz-button" for="fz-import-json">JSON importieren</label><input id="fz-import-json" type="file" accept="application/json,.json" hidden>
  <button class="fz-button fz-button--danger" id="fz-reset-tests" type="button">Lokalen Fortschritt zurücksetzen</button>
</div>
<p class="fz-live-message" id="fz-test-message" role="status" aria-live="polite"></p>

<div id="fz-manual-test-app" class="fz-test-grid" data-suite-id="FZV2-RM"></div>

<script type="application/json" id="fz-manual-test-catalog">
--8<-- "docs/includes/fractal-zones-v2-remediation-user-test-catalog.json"
</script>
