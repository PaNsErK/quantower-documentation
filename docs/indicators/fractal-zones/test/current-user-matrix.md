# Aktuelle V5/V6-Testmatrix

`manual_acceptance_complete=false` · `runtime_acceptance_complete=false` · `sourceValidatedRuntimePending`

Diese lokale Matrix begleitet die aktuellen V5/V6-Erweiterungen. Eine nicht-tradende UI-Teilinventur hat produktseitige Settings, LineOptions und die relevanten Sichtbarkeitszweige bereits bestätigt; sie ist dennoch kein Ersatz für die noch ausstehende Runtime-Abnahme und überträgt keine Daten.

<div class="fz-safety" role="note"><strong>Nicht-tradend und lokal:</strong> Keine Action-Einstellungen auslösen; keine Konto-, Order-, Positions-, Portfolio-, Funds-, Connection- oder Strategy-Flächen öffnen.</div>

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
<div id="fz-manual-test-app" class="fz-test-grid" data-suite-id="FZCURRENT"></div>
<script type="application/json" id="fz-manual-test-catalog">
--8<-- "docs/includes/fractal-zones-current-user-test-catalog.json"
</script>

Die MVA-IDs der Produktkonformität sind stets namespacespezifisch: etwa `FZCP-v5/MVA-26`, nicht nur `MVA-26`.
