# Interaktive Regression und Lernen

Die 24 FZMT-Fälle unterstützen Lernen und wiederholbare Beobachtung. Fortschritt und Notizen bleiben ausschließlich im lokalen Browser. Export enthält nur die geschlossene Suite, Statuswerte und deine optionalen Notizen.

<div data-manual-test-suite="fzmt-regression-v3"></div>

## Datenschutz und Migration

- Keine Netzwerkübertragung durch das benutzerdefinierte JavaScript.
- Import wird gegen das geschlossene Schema validiert.
- Der alte FZMT-v1/v2-Stand darf nur in die FZMT-Suite migriert werden.
- FZV2-RM und FZCURRENT bleiben eigene Namespaces und erhalten niemals automatisch Ergebnisse aus FZMT.

Die historische V2-Matrix steht separat unter [Offene Benutzer-Testmatrix](v2-remediation-user-matrix.md); die aktuelle V5/V6-Matrix unter [Aktuelle V5/V6-Testmatrix](current-user-matrix.md).

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

<div id="fz-manual-test-app" class="fz-test-grid" data-suite-id="FZMT"></div>

<script type="application/json" id="fz-manual-test-catalog">
--8<-- "docs/includes/manual-test-catalog.json"
</script>
