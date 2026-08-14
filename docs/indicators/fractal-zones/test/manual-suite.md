# Interaktive manuelle Testsuite

<div class="fz-safety" role="note">
<strong>Lokale und nicht-tradende Testhilfe:</strong> Status und Notizen bleiben im Browserprofil. Ohne aktiviertes Opt-in werden Notizen nicht exportiert. Keine Konto-, Order-, Positions-, Pfad-, Prozess- oder Logdaten eintragen.
</div>

<section markdown="1" class="fz-topic" data-topic="FZT-33" data-modes="test">

## Erstinstallation und Settings testen

<div markdown="1" class="fz-depth" data-depth="short">Zuerst Laden, Sicherheitsgrenze, 29 Produktzeilen und alle Sichtbarkeitszweige prüfen.</div>

<div markdown="1" class="fz-depth" data-depth="practice">FZMT‑01 bis FZMT‑03 bilden das Einstiegsgate. Wenn eine Zeile fehlt oder eine Abhängigkeit falsch sichtbar ist, keine tiefere Semantik als bestanden markieren.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Das Runtime-Inventar muss die statische 29-Zeilen-Menge mit der tatsächlich sichtbaren Union aus Produkt und `base.Settings` abgleichen.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-34" data-modes="test">

## Lifecycle und Darstellung testen

<div markdown="1" class="fz-depth" data-depth="short">FZMT‑04 bis FZMT‑16 prüfen Segmenttreue, Breaks, Retest, Rollen, Ende und Rendergleichheit.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Nutze denselben historischen Abschnitt für A/B-Vergleiche. Ändere nicht gleichzeitig Distanzmodus, Timer, Cooldown und Rendering.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Committed-Zeitpunkte, Segmentgrenzen und Zähler müssen über alle Render-Modi identisch bleiben. Nur Opacity und sichtbare optionale Marker dürfen abweichen.</div>

</section>

<section markdown="1" class="fz-topic" data-topic="FZT-35" data-modes="test">

## Historie, Recovery und Performance testen

<div markdown="1" class="fz-depth" data-depth="short">FZMT‑17 bis FZMT‑24 prüfen Timeframe-Parität, Startlogik, Checkpoint, Verify, Gap-Recovery, Performance und Datenschutz.</div>

<div markdown="1" class="fz-depth" data-depth="practice">Restart- oder Recovery-Tests erst nach vollständig dokumentiertem Ausgangszustand ausführen. Den normalen 90‑Tage-Modus am Ende wiederherstellen.</div>

<div markdown="1" class="fz-depth" data-depth="technical">Runtime-Akzeptanz verlangt einen generationstreuen Vergleich, keinen Teil-Publish, sichere Single-Flight-Aktionen und sanitisiertes FZDIAG/FZPERF/FZPERSIST-Readback.</div>

</section>

<noscript><p class="fz-noscript">JavaScript ist deaktiviert. Die konzeptionelle Dokumentation bleibt vollständig nutzbar; für lokalen Fortschritt und Export bitte JavaScript nur für diese statische Seite aktivieren.</p></noscript>

<div class="fz-test-toolbar">
  <div>
    <label for="fz-test-progress"><strong>Fortschritt</strong></label>
    <progress class="fz-progress" id="fz-test-progress" value="0" max="24"></progress>
    <span id="fz-test-progress-text">0 von 24 Tests bewertet</span>
  </div>
  <label><input type="checkbox" id="fz-export-notes"> Notizen beim Export einschließen</label>
</div>

<div class="fz-test-actions" role="group" aria-label="Testdatenaktionen">
  <button class="fz-button" id="fz-export-json" type="button">JSON exportieren</button>
  <button class="fz-button" id="fz-export-markdown" type="button">Markdown exportieren</button>
  <label class="fz-button" for="fz-import-json">JSON importieren</label>
  <input id="fz-import-json" type="file" accept="application/json,.json" hidden>
  <button class="fz-button fz-button--danger" id="fz-reset-tests" type="button">Lokalen Fortschritt zurücksetzen</button>
</div>

<p class="fz-live-message" id="fz-test-message" role="status" aria-live="polite"></p>

<div id="fz-manual-test-app" class="fz-test-grid"></div>

<script type="application/json" id="fz-manual-test-catalog">
--8<-- "docs/includes/manual-test-catalog.json"
</script>

## Exportvertrag

JSON folgt dem geschlossenen Schema `fz-manual-test-result-v1`. Unbekannte Felder, doppelte Test-IDs, fremde Indikatoridentität, Dateien über 256 KiB und sensible Notizmuster werden lokal abgelehnt. Markdown wird aus demselben validierten Zustand erzeugt.
